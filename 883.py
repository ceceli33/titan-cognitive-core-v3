# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — LoRA–CUT3 BACKWARD PREFLIGHT (LCP)                       single Google Colab cell
# Frozen Qwen2.5-72B-Instruct NF4 / BF16, one A100-SXM4-80GB.
#
# SCOPE: technical feasibility ONLY. At most 3 optimizer steps, used solely to verify gradient flow and one real
# LoRA update. A PASS here is NOT a learning, semantic-reading, native-behaviour or autonomy result.
# NOT EXECUTED ON GPU BY THE AUTHOR OF THIS CELL. Every number in the report is produced by the run itself.
#
# Contract (instruction §5): every prefix / cartridge forge / mount / upper-K/V rebuild runs with ADAPTER OFF under
# torch.no_grad (constant base K/V). Only live query/readout tokens run with ADAPTER ON and autograd. Train and
# inference use the same base-OFF-prefix + LoRA-ON-live-query regime. A runtime guard raises if LoRA is enabled
# while a mount is active. No hooks, no RAG, no prompt replay, no output/action override, no oracle routing.
#
# Engine sources are pinned to commit f1007d912773f3460536784ff80a215741bc97e9 and verified by git-blob SHA-1.
# Hook-free engine definitions are AST-selected (never the hooked 709 forge_stream / initialize / append paths):
#   709.py  pairs cache_build replace half rope rephase free_gpu ensure_room kv_digest full_kv_seal sentinel
#   730.py  sha release DirectCut3 forge_native initialize_native to_gpu seal_cp
#   757.py  model_setup native_append_direct            (the engine's model loader and locked native append)
#   877.py  api877 xattn877 weights_digest877           (explicit no-hook attention, installed-source audit)
#   878.py  xspan878 xappend878                         (explicit no-hook append reference)
#   873.py  kv873 length873       test870.py  cache_kv870
# LoRA: transparent in-place wrapper around the native q/k/v/o Linear4bit modules (no PEFT): y = W0 x + (a/r) B A x.
# =====================================================================================================================
import os, sys, subprocess, importlib.util, importlib.metadata, urllib.request, hashlib, ast, json, time, gc, math
import traceback, platform, types, random, shutil
from pathlib import Path
from datetime import datetime, timezone
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')

# ---------------------------------------------------------------------------------------------------------- versions
def _ver(name):
    try: return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError: return None
def _vt(s):
    out = []
    for x in str(s).split('+')[0].split('.')[:3]:
        d = ''.join(c for c in x if c.isdigit()); out.append(int(d) if d else 0)
    return tuple(out + [0] * (3 - len(out)))
REQ_LCP = {'transformers': ('transformers>=5.18,<6', (5, 18, 0), (6, 0, 0)), 'accelerate': ('accelerate>=1.15', (1, 15, 0), None),
           'bitsandbytes': ('bitsandbytes>=0.50', (0, 50, 0), None)}
for _pkg, (_spec, _lo, _hi) in REQ_LCP.items():
    _v = _ver(_pkg)
    _ok = _v is not None and _vt(_v) >= _lo and (_hi is None or _vt(_v) < _hi)
    if not _ok:
        if _pkg in sys.modules:
            raise SystemExit('LCP_ENV: %s %s already imported in this kernel; restart the runtime and rerun' % (_pkg, _v))
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', _spec])
import torch, transformers, accelerate, bitsandbytes
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from transformers.cache_utils import DynamicCache

# --------------------------------------------------------------------------------------------------------- constants
TAG = 'LCP'
RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
COMMIT = 'f1007d912773f3460536784ff80a215741bc97e9'
RAW_BASE = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/' + COMMIT + '/'
MODEL_ID = 'Qwen/Qwen2.5-72B-Instruct'; CUT = 3; DTYPE = torch.bfloat16; DEV = torch.device('cuda:0')
EXPECTED = (80, 8192, 64, 8, 128); CHUNK = 128; GPU_RESERVE_GIB = 9.0
SEED = 20261117
ROOT = Path('/content/AKBASCORE_LCP_' + RUN_ID if Path('/content').exists() else '/tmp/AKBASCORE_LCP_' + RUN_ID)
CART_DIR = ROOT / 'cartridges'; ROOT.mkdir(parents=True, exist_ok=True); CART_DIR.mkdir(exist_ok=True)
LOG = ROOT / 'LCP_PREFLIGHT.log'; OUT = ROOT / 'LCP_PREFLIGHT_results.json'; LOG.write_text('')
# Git blob SHA-1 of every engine file this cell reads (pinned commit). K3.1's six reported IDs are cross-checked below.
LOCKS = {'709.py': '6c9f8cbb1eeed848d45133d73f0d7676b68e9125', '730.py': 'b1bad9eb3b111b44413f8ef05a3a140ab66a77dd',
         '757.py': '3d88bf8638390995858f23391f1e043faa586835', '873.py': '2e44affa5e0dd462155fb265c331270fb8e7b7e1',
         '877.py': 'a6aa7648e0fb765a8dc9b56b8f79b4dcef5fc772', '878.py': '7842e8675544a0328e3552f059c81b7750068a82',
         'test870.py': 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', '779.py': 'fa7017a87f25ecef6ed2b2954a850599cb25fcd9',
         '893.py': 'd401c7f0baf15dfcabcc6f4239d9616526fe41f2', '893.log': '0f61b967edf48dc7f2874d7b537b8eefec18c50a'}
K31_BLOBS = {'709.py': '6c9f8cbb1eeed848d45133d73f0d7676b68e9125', '757.py': '3d88bf8638390995858f23391f1e043faa586835',
             '779.py': 'fa7017a87f25ecef6ed2b2954a850599cb25fcd9', '878.py': '7842e8675544a0328e3552f059c81b7750068a82',
             '893.py': 'd401c7f0baf15dfcabcc6f4239d9616526fe41f2', '893.log': '0f61b967edf48dc7f2874d7b537b8eefec18c50a'}
SELECT = {'709.py': ('pairs', 'cache_build', 'replace', 'half', 'rope', 'rephase', 'free_gpu', 'ensure_room', 'kv_digest',
                     'full_kv_seal', 'sentinel'),
          '730.py': ('sha', 'release', 'DirectCut3', 'forge_native', 'initialize_native', 'to_gpu', 'seal_cp'),
          '757.py': ('model_setup', 'native_append_direct'),
          '877.py': ('api877', 'xattn877', 'weights_digest877'),
          '878.py': ('xspan878', 'xappend878'),
          '873.py': ('kv873', 'length873'),
          'test870.py': ('cache_kv870',)}
FORBIDDEN_TOKENS = ('register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook',
                    'register_backward_hook', 'register_full_backward_pre_hook', 'register_module_forward_hook',
                    'register_module_forward_pre_hook', 'register_hook(')
# LoRA (instruction §6: first candidate)
LORA_R = 8; LORA_ALPHA = 16; LORA_TARGETS = ('q_proj', 'k_proj', 'v_proj', 'o_proj'); LR = 1e-4; OPT_STEPS = 3
# Pre-registered tolerances (fixed before any GPU number exists; logged with SHA-256 at start).
TOL = {
    'parity_close_rel': 1e-2,          # non-bitwise but value-close native parity -> INCONCLUSIVE (kernel), never PASS
    'label_alignment_nats': 0.05,      # teacher-forced first-target log-prob vs suffix-only next-token log-prob
    'train_infer_pass_nats': 0.10,     # bf16 eps 2^-8 at |logit|~10-30 is ~0.04-0.12 per logit; target log-prob gap
    'train_infer_inconclusive_nats': 0.50,
    'dir_targets_nats': (0.02, 0.10),  # predicted first-order loss decrease for the two directional probes
    'dir_ratio_band': (0.25, 4.0),     # actual/predicted for the smaller probe
    'dir_fail_increase_nats': 0.005,   # FAIL only if BOTH probes increase the loss by more than this
    'surrogate_rel_err': 1e-6,         # float64 local surrogate: autograd vs central finite difference
    'vram_reserved_frac_max': 0.95,    # peak reserved / total device memory
    'P_expected': 30, 'chunk_expected': 128}
LIVE_LENGTHS = (64, 256); LONG_TARGET_TOKENS = 2000
CRITICAL = ('ENV', 'SOURCE', 'EXTRACT', 'MODEL', 'P0_C_WRAPPER_OFF_IDENTITY', 'P0_D_ZERO_LORA_IDENTITY', 'P1_PHYSICAL',
            'P2_LIVE_AUTOGRAD', 'P3_GRADIENT', 'P7_INTEGRITY')
REQUIRED = ('P0_A_FORGE_REBUILD_PARITY', 'P0_B_EXPLICIT_APPEND_PARITY', 'P4_NUMERICAL', 'P5_TRAIN_INFER', 'P6_RESOURCE')
GATE_ORDER = ('ENV', 'SOURCE', 'EXTRACT', 'MODEL', 'P0_A_FORGE_REBUILD_PARITY', 'P0_B_EXPLICIT_APPEND_PARITY',
              'P0_C_WRAPPER_OFF_IDENTITY', 'P0_D_ZERO_LORA_IDENTITY', 'P1_PHYSICAL', 'P2_LIVE_AUTOGRAD', 'P3_GRADIENT',
              'P4_NUMERICAL', 'P5_TRAIN_INFER', 'P6_RESOURCE', 'P7_INTEGRITY', 'S8_CONTENT_DEPENDENCE', 'P8_READABILITY')

R = {'test': 'AKBASCORE_LCP_PREFLIGHT', 'run_id': RUN_ID, 'commit': COMMIT, 'status': 'STARTED', 'checks': [],
     'gates': {g: {'status': 'NOT_RUN', 'reason': None, 'data': {}} for g in GATE_ORDER},
     'scope': 'technical feasibility only; not a learning / semantic / native-behaviour / autonomy result',
     'executed_by_author': False, 'tolerances': TOL,
     'tolerances_sha256': hashlib.sha256(json.dumps(TOL, sort_keys=True).encode()).hexdigest()}
T0 = time.perf_counter()

# ----------------------------------------------------------------------------------------------------------- logging
def log(*xs):
    s = ' '.join(str(x) for x in xs); print(s, flush=True)
    with LOG.open('a') as f: f.write(s + '\n')
def save():
    tmp = OUT.with_suffix('.json.tmp'); tmp.write_text(json.dumps(R, ensure_ascii=False, indent=2, default=str)); tmp.replace(OUT)
def check(name, ok, detail=None):
    # same signature/semantics as the 730/757 check() used by the extracted engine definitions
    R['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail}); save()
    log('PASS' if ok else 'FAIL', name, '' if detail is None else json.dumps(detail, default=str)[:600])
    if not ok: raise RuntimeError('CHECK_FAILED:' + name)
class StopLCP(Exception): pass
def gate(name, status, reason=None, **data):
    assert status in ('PASS', 'FAIL', 'INCONCLUSIVE', 'DIAGNOSTIC'), status
    R['gates'][name] = {'status': status, 'reason': reason, 'data': data}; save()
    log('GATE', name, status, '' if reason is None else '| ' + str(reason))
    if status == 'FAIL' and name in CRITICAL: raise StopLCP(name + ': ' + str(reason))
def gpu_mem():
    torch.cuda.synchronize(); f, t = torch.cuda.mem_get_info()
    return {'free_gib': round(f / 2**30, 3), 'allocated_gib': round(torch.cuda.memory_allocated() / 2**30, 3),
            'reserved_gib': round(torch.cuda.memory_reserved() / 2**30, 3),
            'peak_allocated_gib': round(torch.cuda.max_memory_allocated() / 2**30, 3),
            'peak_reserved_gib': round(torch.cuda.max_memory_reserved() / 2**30, 3), 'total_gib': round(t / 2**30, 3)}
def gitblob(b): return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_path(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(4 << 20), b''): h.update(c)
    return h.hexdigest()

# ------------------------------------------------------------------------------------------- pinned source handling
def fetch_pinned(name, limit=2_000_000):
    url = RAW_BASE + name
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'AKBASCORE-LCP'}), timeout=120) as f:
        b = f.read(limit + 1)
    if len(b) > limit: raise RuntimeError('SOURCE_TOO_LARGE ' + name)
    return b
def extract_selected(fname, raw, names, namespace):
    # AST-select top-level definitions by name (each exactly once), refuse hook tokens, exec into the cell namespace.
    src = raw.decode('utf-8'); tree = ast.parse(src, filename=fname)
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    counts = {k: sum(1 for n in nodes if n.name == k) for k in names}
    if any(c != 1 for c in counts.values()): raise RuntimeError('SELECT_COUNT %s %s' % (fname, counts))
    seg = {n.name: ast.get_source_segment(src, n) for n in nodes}
    bad = {k: [t for t in FORBIDDEN_TOKENS if t in s] for k, s in seg.items()}
    if any(bad.values()): raise RuntimeError('HOOK_TOKEN_IN_SELECTED_SOURCE %s %s' % (fname, bad))
    exec(compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])), fname + ':selected', 'exec'), namespace)
    return {k: hashlib.sha256(s.encode()).hexdigest()[:16] for k, s in seg.items()}

# ------------------------------------------------------------------------------------------------- LoRA (no PEFT)
LORA_STATE = {'enabled': False, 'mount_active': False, 'calls_on': 0, 'calls_off': 0}
class LoRAProjLCP(torch.nn.Module):
    """y = base(x) + (alpha/r) * (x A^T) B^T. base = the native Linear4bit module, called unchanged.
    Disabled: returns base(x) itself (bitwise base). Never active while a mount is active (runtime guard)."""
    def __init__(self, base, r, alpha, name, gen):
        super().__init__()
        self.base = base; self.r = int(r); self.scale = float(alpha) / float(r); self.lcp_name = name
        fin, fout = int(base.in_features), int(base.out_features); bound = 1.0 / math.sqrt(fin)   # kaiming_uniform(a=sqrt 5)
        A = (torch.rand((self.r, fin), generator=gen, dtype=torch.float32) * 2.0 - 1.0) * bound
        self.lora_A = torch.nn.Parameter(A.to(DEV)); self.lora_B = torch.nn.Parameter(torch.zeros((fout, self.r), dtype=torch.float32, device=DEV))
    @property
    def weight(self): return self.base.weight            # engine checksums (709 sentinel) read <proj>.weight
    @property
    def in_features(self): return self.base.in_features
    @property
    def out_features(self): return self.base.out_features
    @staticmethod
    def lora_delta(x, A, B, scale): return (x @ A.t()) @ B.t() * scale
    def forward(self, x):
        y = self.base(x)
        if not LORA_STATE['enabled']:
            LORA_STATE['calls_off'] += 1; return y
        if LORA_STATE['mount_active']: raise RuntimeError('LORA_ENABLED_DURING_MOUNT')
        LORA_STATE['calls_on'] += 1
        return y + self.lora_delta(x.to(torch.float32), self.lora_A, self.lora_B, self.scale).to(y.dtype)
class MountOff:
    """Every forge / mount / upper rebuild / reference prefill runs inside this: adapter OFF + no_grad + guard."""
    def __enter__(self):
        self.prev = LORA_STATE['enabled']; LORA_STATE['enabled'] = False; LORA_STATE['mount_active'] = True
        self.ng = torch.no_grad(); self.ng.__enter__(); return self
    def __exit__(self, *e):
        self.ng.__exit__(*e); LORA_STATE['mount_active'] = False; LORA_STATE['enabled'] = self.prev; return False
class Adapter:
    def __init__(self, on): self.on = bool(on)
    def __enter__(self):
        if LORA_STATE['mount_active']: raise RuntimeError('ADAPTER_SWITCH_INSIDE_MOUNT')
        self.prev = LORA_STATE['enabled']; LORA_STATE['enabled'] = self.on; return self
    def __exit__(self, *e): LORA_STATE['enabled'] = self.prev; return False

# --------------------------------------------------------------------------------------------- inventory / checksums
def hook_inventory():
    mm = torch.nn.modules.module
    glob = {n: len(getattr(mm, n, None) or {}) for n in ('_global_forward_hooks', '_global_forward_pre_hooks',
            '_global_backward_hooks', '_global_backward_pre_hooks', '_global_forward_hooks_always_called')}
    mods = {'_forward_hooks': 0, '_forward_pre_hooks': 0, '_backward_hooks': 0, '_backward_pre_hooks': 0}; where = []
    inst_forward = []; hf = 0
    for name, m in model.named_modules():
        for a in mods:
            d = getattr(m, a, None)
            if d: mods[a] += len(d); where.append([name, a, len(d)])
        # an instance 'forward' that is just the class method re-bound (730 DirectCut3.__exit__ does this) is benign
        if 'forward' in m.__dict__ and getattr(m.__dict__['forward'], '__func__', None) is not type(m).forward:
            inst_forward.append(name)
        if hasattr(m, '_hf_hook'): hf += 1
    tens = 0
    for p in model.parameters():
        for a in ('_backward_hooks', '_post_accumulate_grad_hooks'):
            d = getattr(p, a, None)
            if d: tens += len(d)
    torch_hooks = sum(glob.values()) + sum(mods.values()) + tens
    return {'torch_hooks_total': torch_hooks, 'global': glob, 'module': mods, 'tensor': tens, 'where': where[:20],
            'instance_forward_overrides': inst_forward[:20], 'instance_forward_override_count': len(inst_forward),
            'accelerate_hf_hook_modules': hf}
def full_checksum(params):
    # non-cryptographic full-coverage checksum of the raw storage bytes of every base parameter (GPU, 16M-byte blocks)
    h = hashlib.sha256(); BL = 1 << 24
    w = (torch.arange(BL, device=DEV, dtype=torch.int32) % 251) + 1
    for name, p in params:
        v = p.data.detach().contiguous().reshape(-1).view(torch.uint8); n = v.numel(); s1 = 0; s2 = 0
        for st in range(0, n, BL):
            b = v[st:st + BL].to(torch.int32); s1 += int(b.sum(dtype=torch.int64)); s2 += int((b * w[:b.numel()]).sum(dtype=torch.int64))
        h.update(('%s|%s|%d|%d|%d;' % (name, str(p.dtype), n, s1, s2)).encode())
    return h.hexdigest()
def seals_equal(a, b): return len(a) == len(b) and all(x == y for x, y in zip(a, b))
def kv_compare(a, b):
    # per-layer: bitwise (byte SHA), value-equal, max abs / rel difference
    bit = val = 0; mabs = 0.0; mrel = 0.0
    for (ka, va), (kb, vb) in zip(a, b):
        for x, y in ((ka, kb), (va, vb)):
            y = y.to(x.device)
            if tuple(x.shape) != tuple(y.shape): return {'shape_mismatch': [list(x.shape), list(y.shape)]}
            bit += int(kv_digest(x) == kv_digest(y)); val += int(torch.equal(x, y))
            d = (x.float() - y.float()).abs(); mabs = max(mabs, float(d.max()))
            mrel = max(mrel, float(torch.linalg.vector_norm(d)) / max(float(torch.linalg.vector_norm(x.float())), 1e-30))
    return {'tensors': 2 * len(a), 'bitwise_equal': bit, 'value_equal': val, 'max_abs': mabs, 'max_rel_l2': mrel}
def tri(cmp):
    if 'shape_mismatch' in cmp: return 'FAIL'
    if cmp['bitwise_equal'] == cmp['tensors']: return 'PASS'
    if cmp['max_rel_l2'] <= TOL['parity_close_rel']: return 'INCONCLUSIVE'
    return 'FAIL'

# ------------------------------------------------------------------------------------------------------ live path
def live(mem, ctx_ids, tgt_ids, grad=False, train=False, adapter=False):
    """Live query/readout forward over a FRESH cache built from constant base K/V (or no prefix if mem is None).
    Teacher forcing: input = ctx_ids + tgt_ids; target j is predicted by the hidden state at len(ctx)-1+j.
    Returns per-target log-probs (graph-attached if grad), selected log-softmax rows (CPU fp32), counts."""
    n0 = 0 if mem is None else int(mem[0][0].shape[-2])
    ids = list(ctx_ids) + list(tgt_ids); L = len(ids); pidx = [len(ctx_ids) - 1 + j for j in range(len(tgt_ids))]
    assert len(tgt_ids) >= 1 and pidx[0] >= 0
    cache = DynamicCache() if mem is None else cache_build(list(mem))
    pos = torch.arange(n0, n0 + L, device=DEV)
    was_training = model.training; model.train(bool(train))
    on0 = LORA_STATE['calls_on']; off0 = LORA_STATE['calls_off']
    try:
        with Adapter(adapter), (torch.enable_grad() if grad else torch.no_grad()):
            out = model.model(input_ids=torch.tensor([ids], device=DEV), past_key_values=cache,
                              attention_mask=torch.ones((1, n0 + L), device=DEV, dtype=torch.long),
                              position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
            hs = out.last_hidden_state[0, pidx, :]
            logits = model.lm_head(hs).float(); lsm = torch.log_softmax(logits, dim=-1)
            lp = lsm.gather(1, torch.tensor(tgt_ids, device=DEV).unsqueeze(1)).squeeze(1)
        cache_len = int(cache.get_seq_length())
    finally:
        model.train(was_training)
    res = {'lp': lp, 'lsm': lsm.detach().cpu(), 'logits': logits.detach().cpu(), 'argmax': lsm.argmax(-1).tolist(),
           'n0': n0, 'L': L, 'cache_len': cache_len, 'calls_on': LORA_STATE['calls_on'] - on0,
           'calls_off': LORA_STATE['calls_off'] - off0}
    del out, hs, cache
    return res
def lp_sum(mem, ctx, tgt, adapter):
    r = live(mem, ctx, tgt, grad=False, train=False, adapter=adapter); v = float(r['lp'].sum()); del r; return v

# ======================================================================================================== RUN
try:
    log('=' * 112); log('AKBASCORE SILICON HIPPOCAMPUS — LoRA–CUT3 BACKWARD PREFLIGHT', RUN_ID, '| commit', COMMIT)
    log('SCOPE: feasibility only. PASS != learning / semantic reading / native behaviour / autonomy.'); log('=' * 112)
    log('TOLERANCES', json.dumps(TOL, sort_keys=True), 'sha256', R['tolerances_sha256'])
    # ---------------------------------------------------------------------------------------------------- ENV
    env = {'python': platform.python_version(), 'torch': torch.__version__, 'cuda': torch.version.cuda,
           'transformers': transformers.__version__, 'accelerate': accelerate.__version__, 'bitsandbytes': bitsandbytes.__version__,
           'cuda_available': torch.cuda.is_available(), 'device_count': torch.cuda.device_count()}
    if env['cuda_available']:
        pr = torch.cuda.get_device_properties(0); env.update(gpu=torch.cuda.get_device_name(0), gpu_bytes=int(pr.total_memory))
    R['env'] = env; log('ENV', json.dumps(env))
    env_ok = env['cuda_available'] and env['device_count'] == 1 and 'A100' in env.get('gpu', '') and env.get('gpu_bytes', 0) >= 70 * 2**30
    gate('ENV', 'PASS' if env_ok else 'FAIL', None if env_ok else 'requires exactly one A100 80GB', **env)
    random.seed(SEED); torch.manual_seed(SEED); torch.cuda.manual_seed_all(SEED)
    # ------------------------------------------------------------------------------------------------- SOURCE
    RAW = {}; blobs = {}
    for name in LOCKS:
        RAW[name] = fetch_pinned(name); blobs[name] = gitblob(RAW[name])
    k31 = {n: {'k31': v, 'actual': blobs[n], 'match': blobs[n] == v} for n, v in K31_BLOBS.items()}
    lock = {n: {'lock': v, 'actual': blobs[n], 'match': blobs[n] == v} for n, v in LOCKS.items()}
    g1 = [l for l in RAW['893.log'].decode('utf-8', 'replace').splitlines() if l.startswith('T893 GATE G1 PASS')]
    g1d = json.loads(g1[0].split('T893 GATE G1 PASS', 1)[1].strip()) if len(g1) == 1 else {}
    src_ok = all(x['match'] for x in lock.values()) and all(x['match'] for x in k31.values()) and \
        g1d.get('P') == TOL['P_expected'] and g1d.get('chunk') == TOL['chunk_expected']
    gate('SOURCE', 'PASS' if src_ok else 'FAIL', None if src_ok else 'blob lock / K3.1 blob / 893.log G1 cross-check failed',
         locks=lock, k31_blob_check=k31, log893_G1={'P': g1d.get('P'), 'chunk': g1d.get('chunk'), 'gpu_wall_s': g1d.get('wall_s')})
    # ------------------------------------------------------------------------------------------------ EXTRACT
    MOD877 = {}; STATE877 = {'api': {}}; _h877 = hashlib
    sel = {}
    for fname, names in SELECT.items(): sel[fname] = extract_selected(fname, RAW[fname], names, globals())
    APPEND873 = {'CUT': CUT, 'rephase': rephase}; EXP878 = {'CHUNK': CHUNK}
    ans709 = ast.get_source_segment(RAW['709.py'].decode(), [n for n in ast.parse(RAW['709.py'].decode()).body
                                                              if isinstance(n, ast.FunctionDef) and n.name == 'answer'][0])
    SUFFIX_HEAD, SUFFIX_TAIL = '\nQUESTION:\n', '\n\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n'
    sfx_ok = ("suffix='\\nQUESTION:\\n'+question+'\\n\\nANSWER:\\n<|im_end|>\\n<|im_start|>assistant\\n'" in ans709)
    gate('EXTRACT', 'PASS' if sfx_ok else 'FAIL', None if sfx_ok else '709 answer() suffix literal changed',
         selected_ast_sha16=sel, hook_tokens_refused=list(FORBIDDEN_TOKENS), live_suffix_source='709.py answer()')
    # -------------------------------------------------------------------------------------------------- MODEL
    t = time.perf_counter(); model_setup(); load_s = round(time.perf_counter() - t, 1)
    hooks_load = hook_inventory()
    base_params = [(n, p) for n, p in model.named_parameters()]
    model_ok = (P == TOL['P_expected'] and all(not p.requires_grad for _, p in base_params) and not model.training
                and hooks_load['torch_hooks_total'] == 0 and model.config._attn_implementation == 'sdpa'
                and float(getattr(model.config, 'attention_dropout', 0.0)) == 0.0)
    gate('MODEL', 'PASS' if model_ok else 'FAIL', None if model_ok else 'P / frozen / eval / hooks / sdpa / dropout',
         load_s=load_s, P=P, prefix_sha256=sha_bytes(PREFIX.encode()), base_param_tensors=len(base_params),
         hooks=hooks_load, gpu=gpu_mem(), model_revision=getattr(model.config, '_commit_hash', None))
    ENV = {'model': model, 'DEV': DEV, 'P': P, 'NL': NL, 'H': H, 'cache_build': cache_build}
    api_err = None
    try: api877(ENV)
    except Exception as e: api_err = '%s: %s' % (type(e).__name__, e)
    log('API877', 'OK' if api_err is None else api_err, json.dumps(STATE877.get('api', {}), default=str))
    W0 = {'sentinel': sentinel(), 'weights877': weights_digest877(ENV)}
    t = time.perf_counter(); W0['full'] = full_checksum(base_params); W0['full_s'] = round(time.perf_counter() - t, 1)
    log('BASE_CHECKSUMS', json.dumps(W0))
    # ------------------------------------------------------------------------------------- preflight-only records
    # Same record body as 841 body841; fresh opaque names (829 alphabet) private to this preflight (never H1 data).
    rng = random.Random(SEED + 1); ALPH = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    def code(): return ''.join(rng.choice(ALPH) for _ in range(9))
    def body(dom, a, b): return 'Evidence record. Domain: ' + dom + '\n' + 'Directed relation: ' + a + ' -> ' + b + '.\n'
    def ntok(s): return len(tok(s, add_special_tokens=False).input_ids)
    for attempt in range(1, 5001):
        D, S, T1, T2, D2, U, V = 'DOMAIN_' + code(), code(), code(), code(), 'DOMAIN_' + code(), code(), code()
        if len({D, S, T1, T2, D2, U, V}) < 7: continue
        bA, bB, bW = body(D, S, T1), body(D, S, T2), body(D2, U, V)
        if ntok(T1) == ntok(T2) and ntok(bA) == ntok(bB) == ntok(bW): break
    else: raise RuntimeError('GEOMETRY_NAMES_NOT_FOUND')
    QUESTION = 'In domain ' + D + ', the directed relation that starts at ' + S + ' ends at which node? Reply with only the node name.'
    SUFFIX = SUFFIX_HEAD + QUESTION + SUFFIX_TAIL
    sfx_ids = tok(SUFFIX, add_special_tokens=False).input_ids
    t1_ids, t2_ids = tok(T1, add_special_tokens=False).input_ids, tok(T2, add_special_tokens=False).input_ids
    def contains(seq, sub): return any(seq[i:i + len(sub)] == sub for i in range(len(seq) - len(sub) + 1))
    leak_ok = T1 not in SUFFIX and T2 not in SUFFIX and not contains(sfx_ids, t1_ids) and not contains(sfx_ids, t2_ids)
    long_parts = []
    while ntok(''.join(long_parts)) < LONG_TARGET_TOKENS: long_parts.append(body('DOMAIN_' + code(), code(), code()))
    bLONG = ''.join(long_parts)
    R['records'] = {'name_attempts': attempt, 'domain': D, 'start': S, 'T1': T1, 'T2': T2, 'placebo_domain': D2,
                    'tokens': {'body': ntok(bA), 'target': len(t1_ids), 'suffix': len(sfx_ids), 'long_body': ntok(bLONG)},
                    'leak_free': leak_ok, 'note': 'preflight-only names; exclude from any later H1 split'}
    log('RECORDS', json.dumps(R['records']))
    # --------------------------------------------------------------------------------------- forge + file seals
    CP = {}; ENTRY = {}
    for cid, text in (('A', bA), ('B', bB), ('W', bW), ('NONE', ''), ('LONG', bLONG)):
        ids = tok(text, add_special_tokens=False).input_ids if text else []
        with MountOff(): cp, secs = forge_native(ids, 'LCP_' + RUN_ID + '_' + cid)
        path = CART_DIR / ('LCP_' + RUN_ID + '_' + cid + '.pt'); tmp = Path(str(path) + '.tmp')
        assert not path.exists(), 'APPEND_ONLY'
        torch.save(cp, tmp); tmp.replace(path)
        CP[cid] = cp; ENTRY[cid] = {'file': str(path), 'sha256': sha_path(path), 'tensor_seal': seal_cp(cp), 'n': cp['n'],
                                    'body_tokens': cp['body_tokens'], 'forge_s': secs}
        log('FORGED', cid, 'n', cp['n'], 'sha256', ENTRY[cid]['sha256'][:16], 'forge_s', secs)
    # ------------------------------------------------------------------------------------ mounts (adapter OFF)
    def mount_init(cid):
        with MountOff(): return list(initialize_native(to_gpu(CP[cid])))
    def mount_append(mem, cid):
        with MountOff(): return list(native_append_direct(list(mem), to_gpu(CP[cid]), strict_sha=True))
    MEM = {c: mount_init(c) for c in ('A', 'B', 'W', 'NONE')}
    MEM['LONG_A'] = mount_append(mount_init('LONG'), 'A'); MEM['XL'] = mount_append(MEM['LONG_A'], 'LONG')
    SEAL = {k: full_kv_seal(v) for k, v in MEM.items()}
    rg_mem = any(t.requires_grad for m in MEM.values() for kv in m for t in kv)
    log('MOUNTS', json.dumps({k: int(v[0][0].shape[-2]) for k, v in MEM.items()}), 'gpu', json.dumps(gpu_mem()))
    # ---------------------------------------------------------------------------- P0 (before any LoRA object exists)
    with MountOff():
        ids_A = list(PIDS) + tok(bA, add_special_tokens=False).input_ids; cache = None
        for st in range(0, len(ids_A), CHUNK):                    # reference = forge_native's own loop, keeping the cache
            piece = ids_A[st:st + CHUNK]; ensure_room(len(piece) + 512); pos = torch.arange(st, st + len(piece), device=DEV)
            out = model(input_ids=torch.tensor([piece], device=DEV), past_key_values=cache,
                        attention_mask=torch.ones((1, st + len(piece)), device=DEV, dtype=torch.long),
                        position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
            cache = out.past_key_values; del out
        REF_A = [(k.detach().clone(), v.detach().clone()) for k, v in pairs(cache)]; del cache
    lower_cmp = kv_compare(REF_A[:CUT + 1], [(k.to(DEV), v.to(DEV)) for k, v in CP['A']['lower']])
    upper_cmp = kv_compare(REF_A[CUT + 1:], MEM['A'][CUT + 1:])
    st_a = 'PASS' if tri(lower_cmp) == tri(upper_cmp) == 'PASS' else ('FAIL' if 'FAIL' in (tri(lower_cmp), tri(upper_cmp)) else 'INCONCLUSIVE')
    gate('P0_A_FORGE_REBUILD_PARITY', st_a, 'full-text prefill K/V vs forged lower K/V + H3-injected native upper rebuild',
         lower_L0_3=lower_cmp, upper_L4_79=upper_cmp); del REF_A
    if st_a == 'FAIL': raise StopLCP('P0_A native parity FAIL')
    if api_err is None:
        nat = mount_append(MEM['A'], 'B')
        with MountOff(): exp = list(xappend878(ENV, list(MEM['A']), to_gpu(CP['B']), ()))
        cmp_b = kv_compare(nat, exp); st_b = tri(cmp_b)
        gate('P0_B_EXPLICIT_APPEND_PARITY', st_b, 'locked native append (757) vs explicit no-hook append (878/877)', compare=cmp_b)
        del nat, exp
        if st_b == 'FAIL': raise StopLCP('P0_B native parity FAIL')
    else:
        gate('P0_B_EXPLICIT_APPEND_PARITY', 'INCONCLUSIVE', 'api877 installed-source audit failed: ' + api_err)
    base_A1 = live(MEM['A'], sfx_ids, t1_ids); base_A2 = live(MEM['A'], sfx_ids, t1_ids); base_B = live(MEM['B'], sfx_ids, t2_ids)
    repeat_eq = torch.equal(base_A1['logits'], base_A2['logits'])
    log('LIVE_REPEATABILITY_BASE', repeat_eq)
    # ---------------------------------------------------------------------------------------------- LoRA install
    gen = torch.Generator(device='cpu').manual_seed(SEED + 2); LORA = []; base_ids = {}
    for i, layer in enumerate(model.model.layers):
        sa = layer.self_attn
        for nm in LORA_TARGETS:
            b = getattr(sa, nm)
            if not isinstance(b, bitsandbytes.nn.Linear4bit): raise RuntimeError('NOT_LINEAR4BIT L%d.%s' % (i, nm))
            base_ids['L%d.%s' % (i, nm)] = id(b); w = LoRAProjLCP(b, LORA_R, LORA_ALPHA, 'L%d.%s' % (i, nm), gen)
            setattr(sa, nm, w); LORA.append(w)
    LORA_PARAMS = [p for w in LORA for p in (w.lora_A, w.lora_B)]; LORA_IDS = {id(p) for p in LORA_PARAMS}
    install_ok = (len(LORA) == NL * len(LORA_TARGETS) and all(id(getattr(model.model.layers[int(w.lcp_name[1:].split('.')[0])].self_attn,
                  w.lcp_name.split('.')[1]).base) == base_ids[w.lcp_name] for w in LORA))
    BASE_ONLY = [(n, p) for n, p in model.named_parameters() if id(p) not in LORA_IDS]
    trainable = [n for n, p in model.named_parameters() if p.requires_grad]
    adapter_set_ok = len(BASE_ONLY) == len(base_params) and len(trainable) == len(LORA_PARAMS) and \
        all(id(p) in LORA_IDS for _, p in model.named_parameters() if p.requires_grad)
    n_lora = sum(p.numel() for p in LORA_PARAMS); hooks_install = hook_inventory()
    log('LORA_INSTALLED', len(LORA), 'modules', n_lora, 'params', 'adapter_set_ok', adapter_set_ok, 'hooks', hooks_install['torch_hooks_total'])
    if not (install_ok and adapter_set_ok and hooks_install['torch_hooks_total'] == 0): raise StopLCP('LORA_INSTALL_CONTRACT')
    # -------------------------------------------------------------------------------- P0.C wrapper-off identity
    remount = mount_init('A'); seal_re = full_kv_seal(remount); del remount
    off_A = live(MEM['A'], sfx_ids, t1_ids, adapter=False)
    c_eq = seals_equal(seal_re, SEAL['A']) and torch.equal(off_A['logits'], base_A1['logits'])
    c_abs = float((off_A['logits'] - base_A1['logits']).abs().max())
    st_c = 'PASS' if c_eq else ('INCONCLUSIVE' if c_abs <= TOL['parity_close_rel'] * float(base_A1['logits'].abs().max()) else 'FAIL')
    gate('P0_C_WRAPPER_OFF_IDENTITY', st_c, 'installed-but-disabled LoRA vs no-LoRA: re-mount seal and live logits',
         remount_seal_equal=seals_equal(seal_re, SEAL['A']), live_logits_equal=torch.equal(off_A['logits'], base_A1['logits']),
         live_max_abs=c_abs, base_repeatable=repeat_eq, wrapper_calls_off=off_A['calls_off'], wrapper_calls_on=off_A['calls_on'])
    # ------------------------------------------------------------------------- P0.D zero-effect LoRA ON identity
    on0_A = live(MEM['A'], sfx_ids, t1_ids, adapter=True)
    d_abs = float((on0_A['logits'] - base_A1['logits']).abs().max()); d_eq = torch.equal(on0_A['logits'], base_A1['logits'])
    native_path = on0_A['calls_on'] == NL * len(LORA_TARGETS) and on0_A['calls_off'] == 0
    st_d = ('PASS' if d_eq else ('INCONCLUSIVE' if d_abs <= TOL['parity_close_rel'] * float(base_A1['logits'].abs().max()) else 'FAIL'))
    if not native_path: st_d = 'FAIL'
    gate('P0_D_ZERO_LORA_IDENTITY', st_d, 'B=0 LoRA ON vs base on the same mounted cartridge; every wrapper on the native path',
         logits_equal=d_eq, max_abs=d_abs, wrapper_calls_on_per_forward=on0_A['calls_on'], expected_calls=NL * len(LORA_TARGETS))
    # ------------------------------------------------------- S8 / P8 diagnostics with adapter OFF (before any update)
    def content_matrix(adapter):
        mtx = {}
        for m in ('A', 'B', 'W', 'NONE'):
            mtx[m] = {'lp_T1': lp_sum(MEM[m], sfx_ids, t1_ids, adapter), 'lp_T2': lp_sum(MEM[m], sfx_ids, t2_ids, adapter)}
            mtx[m]['margin_T1_minus_T2'] = mtx[m]['lp_T1'] - mtx[m]['lp_T2']
        mtx['content_contrast_A_minus_B'] = mtx['A']['margin_T1_minus_T2'] - mtx['B']['margin_T1_minus_T2']
        return mtx
    S8_OFF = content_matrix(False)
    text_ctx = list(PIDS) + tok(bA, add_special_tokens=False).input_ids + list(sfx_ids)
    text_up = {'lp_T1': lp_sum(None, text_ctx, t1_ids, False), 'lp_T2': lp_sum(None, text_ctx, t2_ids, False)}
    P8 = {'off_forced_choice_A_correct': S8_OFF['A']['lp_T1'] > S8_OFF['A']['lp_T2'],
          'off_forced_choice_B_correct': S8_OFF['B']['lp_T2'] > S8_OFF['B']['lp_T1'],
          'text_upper_bound_A': text_up, 'text_upper_bound_correct': text_up['lp_T1'] > text_up['lp_T2'],
          'mounted_minus_text_lp_T1': S8_OFF['A']['lp_T1'] - text_up['lp_T1'], 'n': 2,
          'note': 'inference-only, n=2, preflight-only names: not H1 data, not a headroom estimate'}
    gate('P8_READABILITY', 'DIAGNOSTIC', 'base-OFF native cartridge readout ceiling / text upper bound (descriptive)', **P8)
    # ------------------------------------------------------------------------------------------- P2 live autograd
    first_tf = float(off_A['lp'][0])
    n0 = int(MEM['A'][0][0].shape[-2])
    with torch.no_grad(), Adapter(False):
        # independent path 1: suffix ONLY (no target token in the input), installed model() head, last position
        pos = torch.arange(n0, n0 + len(sfx_ids), device=DEV); cache = cache_build(list(MEM['A']))
        o1 = model(input_ids=torch.tensor([list(sfx_ids)], device=DEV), past_key_values=cache,
                   attention_mask=torch.ones((1, n0 + len(sfx_ids)), device=DEV, dtype=torch.long),
                   position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
        first_next = float(torch.log_softmax(o1.logits[0, -1, :].float(), dim=-1)[t1_ids[0]]); del o1, cache
        # independent path 2: installed model() logits over suffix+target at the positions live() uses
        ids = list(sfx_ids) + list(t1_ids); pos = torch.arange(n0, n0 + len(ids), device=DEV); cache = cache_build(list(MEM['A']))
        full = model(input_ids=torch.tensor([ids], device=DEV), past_key_values=cache,
                     attention_mask=torch.ones((1, n0 + len(ids)), device=DEV, dtype=torch.long),
                     position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
        pidx = [len(sfx_ids) - 1 + j for j in range(len(t1_ids))]
        fl = full.logits[0, pidx, :].float().cpu()
        head_parity = torch.equal(fl, off_A['logits']); head_abs = float((fl - off_A['logits']).abs().max())
        tf_full = [float(torch.log_softmax(fl[j], dim=-1)[t1_ids[j]]) for j in range(len(t1_ids))]
        del full, cache, fl
    g_probe = live(MEM['A'], sfx_ids, t1_ids, grad=True, train=True, adapter=True)
    loss = -g_probe['lp'].mean()
    graph_ok = bool(loss.requires_grad and loss.grad_fn is not None and torch.isfinite(loss).item())
    del g_probe, loss
    tf_gap = max(abs(a - float(b)) for a, b in zip(tf_full, off_A['lp']))
    p2_ok = (graph_ok and leak_ok and abs(first_tf - first_next) <= TOL['label_alignment_nats'] and
             tf_gap <= TOL['label_alignment_nats'] and
             (head_parity or head_abs <= TOL['parity_close_rel'] * float(off_A['logits'].abs().max())) and
             off_A['cache_len'] == off_A['n0'] + off_A['L'])
    gate('P2_LIVE_AUTOGRAD', 'PASS' if p2_ok else 'FAIL', None if p2_ok else 'graph / leak / label alignment / head path / cache length',
         graph_attached=graph_ok, leak_free=leak_ok, first_target_teacher_forced=first_tf, first_target_next_token=first_next,
         teacher_forced_lp_via_model_head=tf_full, teacher_forced_lp_via_live=[float(x) for x in off_A['lp']],
         lm_head_path_equal=head_parity, lm_head_path_max_abs=head_abs, n0=off_A['n0'], live_len=off_A['L'],
         cache_len_after=off_A['cache_len'], target_positions='len(ctx)-1+j predicts target[j]')
    # ------------------------------------------------------------------------------------------ P3 three updates
    A0 = [p.detach().clone() for p in LORA_PARAMS]
    opt = torch.optim.AdamW(LORA_PARAMS, lr=LR, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0)
    opt_ids = {id(p) for g_ in opt.param_groups for p in g_['params']}
    steps = []; examples = (('A', t1_ids), ('B', t2_ids), ('A', t1_ids))
    for s, (m, tg) in enumerate(examples[:OPT_STEPS], 1):
        opt.zero_grad(set_to_none=True); torch.cuda.reset_peak_memory_stats(); tf = time.perf_counter()
        r_ = live(MEM[m], sfx_ids, tg, grad=True, train=True, adapter=True); loss = -r_['lp'].mean()
        torch.cuda.synchronize(); t_f = time.perf_counter() - tf; tb = time.perf_counter(); loss.backward(); torch.cuda.synchronize(); t_b = time.perf_counter() - tb
        base_grad_none = all(p.grad is None for _, p in BASE_ONLY)
        gA = [float(w.lora_A.grad.norm()) if w.lora_A.grad is not None else 0.0 for w in LORA]
        gB = [float(w.lora_B.grad.norm()) if w.lora_B.grad is not None else 0.0 for w in LORA]
        finite = all(math.isfinite(x) for x in gA + gB); total = math.sqrt(sum(x * x for x in gA + gB))
        per_layer = [round(math.sqrt(sum(x * x for x in gA[i * 4:(i + 1) * 4] + gB[i * 4:(i + 1) * 4])), 8) for i in range(NL)]
        to = time.perf_counter(); opt.step(); torch.cuda.synchronize(); t_o = time.perf_counter() - to
        steps.append({'step': s, 'mount': m, 'loss': float(loss), 'base_grad_none': base_grad_none, 'finite': finite,
                      'total_grad_norm': total, 'A_nonzero_modules': sum(x > 0 for x in gA), 'B_nonzero_modules': sum(x > 0 for x in gB),
                      'per_layer_grad_norm': per_layer, 'forward_s': round(t_f, 3), 'backward_s': round(t_b, 3),
                      'optimizer_s': round(t_o, 3), 'peak': gpu_mem(), 'calls_on': r_['calls_on']})
        log('P3_STEP', s, m, 'loss %.5f' % float(loss), 'grad %.4e' % total, 'A_nz', steps[-1]['A_nonzero_modules'],
            'B_nz', steps[-1]['B_nonzero_modules'], 'f/b/o s', steps[-1]['forward_s'], steps[-1]['backward_s'], steps[-1]['optimizer_s'])
        del r_, loss
    opt.zero_grad(set_to_none=True)
    delta = [float((p.detach() - a).norm()) for p, a in zip(LORA_PARAMS, A0)]
    changed = sum(x > 0 for x in delta)
    p3_ok = (all(x['base_grad_none'] and x['finite'] and x['total_grad_norm'] > 0 for x in steps) and changed >= 1 and
             opt_ids == LORA_IDS and all(not p.requires_grad for _, p in BASE_ONLY))
    gate('P3_GRADIENT', 'PASS' if p3_ok else 'FAIL', None if p3_ok else 'base grad / finiteness / zero grad / no update / optimizer set',
         steps=steps, lora_tensors_changed=changed, lora_tensors=len(LORA_PARAMS), lora_params=n_lora,
         delta_norm_A_total=math.sqrt(sum(d * d for d in delta[0::2])), delta_norm_B_total=math.sqrt(sum(d * d for d in delta[1::2])),
         note='B=0 init: A gradients are zero at step 1 by construction; not a failure')
    del A0
    # --------------------------------------------------------------------------- S8 content dependence, adapter ON
    S8_ON = content_matrix(True)
    geo = {'body_tokens_equal_A_B_W': ntok(bA) == ntok(bB) == ntok(bW), 'target_tokens_equal': len(t1_ids) == len(t2_ids),
           'mount_lengths': {m: int(MEM[m][0][0].shape[-2]) for m in ('A', 'B', 'W', 'NONE')}}
    gate('S8_CONTENT_DEPENDENCE', 'DIAGNOSTIC' if geo['body_tokens_equal_A_B_W'] and geo['target_tokens_equal'] else 'INCONCLUSIVE',
         'computational dependence on cartridge content (not semantic interpretation evidence)',
         geometry=geo, adapter_off=S8_OFF, adapter_on_after_3_steps=S8_ON,
         adapter_effect_A_lp_T1=S8_ON['A']['lp_T1'] - S8_OFF['A']['lp_T1'],
         content_effect_off=S8_OFF['content_contrast_A_minus_B'], content_effect_on=S8_ON['content_contrast_A_minus_B'],
         note='NONE = forge prefix only (different length); W = equal-geometry placebo (other domain)')
    # -------------------------------------------------------------------------------------- P5 train/infer parity
    tr = live(MEM['A'], sfx_ids, t1_ids, grad=True, train=True, adapter=True)
    tr_lsm = tr['lsm']; tr_arg = tr['argmax']; del tr
    inf = live(MEM['A'], sfx_ids, t1_ids, grad=False, train=False, adapter=True)
    gap_t = float((tr_lsm.gather(1, torch.tensor(t1_ids).unsqueeze(1)) - inf['lsm'].gather(1, torch.tensor(t1_ids).unsqueeze(1))).abs().max())
    gap_row = float((tr_lsm - inf['lsm']).abs().max()); arg_eq = tr_arg == inf['argmax']
    st5 = 'PASS' if gap_t <= TOL['train_infer_pass_nats'] and arg_eq else ('INCONCLUSIVE' if gap_t <= TOL['train_infer_inconclusive_nats'] else 'FAIL')
    gate('P5_TRAIN_INFER', st5, 'same base-OFF prefix, cartridge and LoRA state: train-mode autograd vs eval no_grad live forward',
         target_logprob_max_gap=gap_t, row_logsoftmax_max_gap=gap_row, argmax_equal=arg_eq,
         regime='base-OFF prefix + LoRA-ON live query (runtime guard)', full_lora_on_prefix='NOT_COMPUTED (forbidden by contract §5)',
         dropout={'attention_dropout': float(getattr(model.config, 'attention_dropout', 0.0)), 'lora_dropout': 0.0})
    del inf, tr_lsm
    # ---------------------------------------------------------------------------------------- P4 numerical sanity
    w79 = LORA[-1]; gs = torch.Generator(device='cpu').manual_seed(SEED + 3)
    x = torch.randn((4, w79.in_features), generator=gs, dtype=torch.float64); u = torch.randn((4, w79.out_features), generator=gs, dtype=torch.float64)
    Aq = w79.lora_A.detach().cpu().double().clone().requires_grad_(True)
    Bq = (torch.randn((w79.out_features, LORA_R), generator=gs, dtype=torch.float64) * 1e-3).requires_grad_(True)
    f = (u * LoRAProjLCP.lora_delta(x, Aq, Bq, w79.scale)).sum(); f.backward()
    dA = torch.randn(Aq.shape, generator=gs, dtype=torch.float64); dB = torch.randn(Bq.shape, generator=gs, dtype=torch.float64)
    an = float((Aq.grad * dA).sum() + (Bq.grad * dB).sum()); eps = 1e-6
    with torch.no_grad():
        fp = float((u * LoRAProjLCP.lora_delta(x, Aq + eps * dA, Bq + eps * dB, w79.scale)).sum())
        fm = float((u * LoRAProjLCP.lora_delta(x, Aq - eps * dA, Bq - eps * dB, w79.scale)).sum())
    fd = (fp - fm) / (2 * eps); sur_err = abs(an - fd) / max(abs(an), 1e-30)
    snap = [p.detach().clone() for p in LORA_PARAMS]
    gp = live(MEM['A'], sfx_ids, t1_ids, grad=True, train=True, adapter=True); l_ = -gp['lp'].mean()
    grads = torch.autograd.grad(l_, LORA_PARAMS, allow_unused=True); del gp, l_
    grads = [torch.zeros_like(p) if g_ is None else g_ for g_, p in zip(grads, LORA_PARAMS)]
    gn2 = float(sum((g_.double() ** 2).sum() for g_ in grads))
    L0 = -lp_sum(MEM['A'], sfx_ids, t1_ids, True) / len(t1_ids); probes = []
    for dlt in TOL['dir_targets_nats']:
        eta = dlt / max(gn2, 1e-30)
        with torch.no_grad():
            for p, g_ in zip(LORA_PARAMS, grads): p.sub_(eta * g_)
        L1 = -lp_sum(MEM['A'], sfx_ids, t1_ids, True) / len(t1_ids)
        with torch.no_grad():
            for p, s_ in zip(LORA_PARAMS, snap): p.copy_(s_)
        probes.append({'predicted_delta': -dlt, 'actual_delta': L1 - L0, 'ratio': (L1 - L0) / -dlt, 'eta': eta})
    restored = all(torch.equal(p.detach(), s_) for p, s_ in zip(LORA_PARAMS, snap)); del snap, grads
    lo, hi = TOL['dir_ratio_band']
    if sur_err > TOL['surrogate_rel_err'] or not restored: st4 = 'FAIL'
    elif all(pp['actual_delta'] > TOL['dir_fail_increase_nats'] for pp in probes): st4 = 'FAIL'
    elif all(pp['actual_delta'] < 0 for pp in probes) and lo <= probes[0]['ratio'] <= hi: st4 = 'PASS'
    else: st4 = 'INCONCLUSIVE'
    gate('P4_NUMERICAL', st4, 'float64 local surrogate (LoRA math, CPU) + real-NF4-engine directional loss probe',
         surrogate_rel_err=sur_err, surrogate_where='CPU float64, LoRAProjLCP.lora_delta only (no 72B)',
         directional_where='real NF4 72B, base-OFF mount A, eval no_grad loss before/after a -eta*g LoRA step, restored',
         grad_norm=math.sqrt(gn2), loss_L0=L0, probes=probes, params_restored=restored)
    # ------------------------------------------------------------------------------------------- P6 resources
    def filler(n):
        s = (' ' + T1 + ' -> ' + T2 + '.') * (n // 3 + 8); ids_ = tok(s, add_special_tokens=False).input_ids[:n]; assert len(ids_) == n; return ids_
    res = []
    for pname in ('A', 'LONG_A', 'XL'):
        for Ltot in LIVE_LENGTHS:
            row = {'prefix': pname, 'prefix_tokens': int(MEM[pname][0][0].shape[-2]), 'live_tokens': Ltot}
            try:
                if Ltot <= len(sfx_ids): raise RuntimeError('LIVE_LENGTH_SHORTER_THAN_SUFFIX')
                tg = filler(Ltot - len(sfx_ids)); opt.zero_grad(set_to_none=True); release()
                torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
                tc = time.perf_counter(); cb = cache_build(list(MEM[pname])); torch.cuda.synchronize(); row['cache_build_s'] = round(time.perf_counter() - tc, 4); del cb
                tf = time.perf_counter(); r_ = live(MEM[pname], sfx_ids, tg, grad=True, train=True, adapter=True)
                l_ = -r_['lp'].mean(); torch.cuda.synchronize(); row['forward_s'] = round(time.perf_counter() - tf, 3)
                tb = time.perf_counter(); l_.backward(); torch.cuda.synchronize(); row['backward_s'] = round(time.perf_counter() - tb, 3)
                row['prefix_kv_copy_gib_est'] = round(row['prefix_tokens'] * NL * KVH * HD * 2 * 2 / 2**30, 4)
                row.update(peak=gpu_mem(), oom=False); del r_, l_
            except torch.cuda.OutOfMemoryError as e:
                row.update(oom=True, error=str(e)[:300])
            except Exception as e:
                row.update(oom=False, error='%s: %s' % (type(e).__name__, str(e)[:300]))
            opt.zero_grad(set_to_none=True); release(); res.append(row); log('P6', json.dumps(row, default=str))
    total = env['gpu_bytes'] / 2**30
    ok_rows = [r_ for r_ in res if not r_.get('oom') and 'error' not in r_]
    first_ok = any(r_['prefix'] == 'A' and r_['live_tokens'] == LIVE_LENGTHS[0] for r_ in ok_rows)
    all_ok = len(ok_rows) == len(res) and all(r_['peak']['peak_reserved_gib'] <= TOL['vram_reserved_frac_max'] * total for r_ in ok_rows)
    ref = [r_ for r_ in ok_rows if r_['prefix'] == 'LONG_A' and r_['live_tokens'] == LIVE_LENGTHS[-1]]
    opt_s = max(x['optimizer_s'] for x in steps)
    upd_30 = int(1800 / (ref[0]['forward_s'] + ref[0]['backward_s'] + opt_s)) if ref else None
    gate('P6_RESOURCE', 'PASS' if all_ok else ('INCONCLUSIVE' if first_ok else 'FAIL'),
         None if all_ok else 'OOM / error / reserved VRAM above limit in at least one configuration',
         rows=res, optimizer_step_s_max=opt_s, model_load_s=load_s, est_updates_per_30min_LONG_A_256=upd_30,
         gradient_checkpointing='OFF (not attempted in this preflight)', batch=1)
    # ---------------------------------------------------------------------------------------- P1 / P7 final
    seals_end = {k: full_kv_seal(v) for k, v in MEM.items()}
    files_end = {c: sha_path(ENTRY[c]['file']) == ENTRY[c]['sha256'] for c in ENTRY}
    tensor_end = {c: seal_cp(CP[c]) == ENTRY[c]['tensor_seal'] for c in ENTRY}
    p1_ok = (not rg_mem and all(seals_equal(seals_end[k], SEAL[k]) for k in MEM) and all(files_end.values()) and all(tensor_end.values())
             and not any(t.requires_grad for m in MEM.values() for kv in m for t in kv))
    gate('P1_PHYSICAL', 'PASS' if p1_ok else 'FAIL', None if p1_ok else 'mount / file / tensor seal changed or requires_grad on K/V',
         runtime_mount_seals_unchanged={k: seals_equal(seals_end[k], SEAL[k]) for k in MEM}, cartridge_file_sha_unchanged=files_end,
         cartridge_tensor_seal_unchanged=tensor_end, kv_requires_grad=rg_mem, entries=ENTRY)
    hooks_end = hook_inventory()
    # base_params keeps the ORIGINAL names and the same Parameter objects (wrapping renames q_proj.weight -> q_proj.base.weight)
    same_objects = {id(p) for _, p in base_params} == {id(p) for _, p in BASE_ONLY}
    W1 = {'sentinel': sentinel(), 'weights877': weights_digest877(ENV), 'full': full_checksum(base_params)}
    lora_digest = hashlib.sha256(''.join(kv_digest(p.detach()) for p in LORA_PARAMS).encode()).hexdigest()
    f3 = model.model.layers[CUT].forward
    dc3_restored = getattr(f3, '__func__', None) is type(model.model.layers[CUT]).forward
    p7_ok = (same_objects and W1['sentinel'] == W0['sentinel'] and W1['weights877'] == W0['weights877'] and W1['full'] == W0['full'] and
             hooks_end['torch_hooks_total'] == 0 and hooks_install['torch_hooks_total'] == 0 and dc3_restored and
             hooks_end['instance_forward_override_count'] == hooks_load['instance_forward_override_count'] and
             all(not p.requires_grad for _, p in BASE_ONLY) and src_ok)
    gate('P7_INTEGRITY', 'PASS' if p7_ok else 'FAIL', None if p7_ok else 'base checksum / hooks / DirectCut3 restore / freeze',
         base_param_objects_unchanged=same_objects,
         base_checksums_start=W0, base_checksums_end=W1, lora_state_sha256=lora_digest, hooks_after_load=hooks_load,
         hooks_after_install=hooks_install, hooks_end=hooks_end, directcut3_restored=dc3_restored,
         lora_wrapper_calls={'on': LORA_STATE['calls_on'], 'off': LORA_STATE['calls_off']}, adapter_state_file='NOT_WRITTEN')
    R['status'] = 'COMPLETE'
except StopLCP as e:
    R['status'] = 'STOPPED_CRITICAL'; R['stop_reason'] = str(e); log('STOP', str(e))
except Exception as e:
    R['status'] = 'ERROR'; R['error'] = '%s: %s' % (type(e).__name__, e); R['traceback'] = traceback.format_exc()[-20000:]
    log('ERROR', R['error']); log(R['traceback'])
finally:
    G = R['gates']
    crit_fail = [g for g in CRITICAL if G[g]['status'] == 'FAIL'] + [g for g in REQUIRED if G[g]['status'] == 'FAIL' and g != 'P6_RESOURCE']
    not_done = [g for g in CRITICAL + REQUIRED if G[g]['status'] == 'NOT_RUN']
    soft = [g for g in CRITICAL + REQUIRED if G[g]['status'] == 'INCONCLUSIVE'] + (['P6_RESOURCE'] if G['P6_RESOURCE']['status'] == 'FAIL' else [])
    if crit_fail: verdict = 'NOT_FEASIBLE'
    elif R['status'] != 'COMPLETE' or not_done or soft: verdict = 'UNDECIDABLE'
    else: verdict = 'FEASIBLE'
    R['verdict'] = verdict; R['elapsed_s'] = round(time.perf_counter() - T0, 1)
    try: R['gpu_final'] = gpu_mem()
    except Exception: pass
    save()
    log('=' * 112)
    for g in GATE_ORDER: log('%-30s %-13s %s' % (g, G[g]['status'], G[g]['reason'] or ''))
    summary = {'verdict': verdict, 'status': R['status'], 'gates': {g: G[g]['status'] for g in GATE_ORDER},
               'commit': COMMIT, 'run_id': RUN_ID, 'elapsed_s': R['elapsed_s'],
               'scope': 'feasibility only; not learning / semantic / native-behaviour / autonomy evidence'}
    log('LCP_SUMMARY ' + json.dumps(summary, sort_keys=True))
    log('RESULT_JSON', OUT, '| LOG', LOG)
    drive = Path('/content/drive/MyDrive')
    if drive.exists():
        try:
            dst = drive / ('AKBASCORE_LCP_' + RUN_ID); dst.mkdir(parents=True, exist_ok=True)
            for f_ in (OUT, LOG): shutil.copy2(f_, dst / f_.name)
            same = all(sha_path(dst / f_.name) == sha_path(f_) for f_ in (OUT, LOG))
            log('DRIVE_COPY', dst, 'sha_equal', same)
        except Exception as e: log('DRIVE_COPY_FAILED', type(e).__name__, e)
    else: log('DRIVE_COPY NOT_RUN (Drive not mounted)')
    log('=' * 112)
