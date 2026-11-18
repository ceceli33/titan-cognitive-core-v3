# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST894 — LoRA–CUT3 BACKWARD PREFLIGHT                     single Google Colab cell
# Frozen Qwen2.5-72B-Instruct NF4 / BF16, one A100-SXM4-80GB. Direct continuation of TEST893 (same pinned engine
# commit, same physical CUT3/H3/K-V backbone). TEST893 stays as recorded: PHYSICAL_VALIDITY=PASS, SCIENTIFIC_VALIDITY=
# PASS, OUTCOME=FAIL_NO_GAIN; this cell does not reinterpret it.
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
# Runtime contract: torch 2.14.1+cu130 / CUDA 13.0 / transformers 5.22.1 (893.log), accelerate 1.16.0, bitsandbytes 0.50.2;
# model + tokenizer pinned to HF revision 495f39366efef23836d0cfae4fbe635880d2be31. Base integrity = SHA-256 over raw
# parameter bytes + NF4 quant state + buffers. Records: TEST894.log + TEST894_results.json (atomic, Drive-backed after
# every gate), ZIP + SHA256SUMS + read-back gates + TEST894_RECEIPT; ARTIFACT_STATUS is separate from the verdict.
# =====================================================================================================================
import os, sys, subprocess, importlib.util, importlib.metadata, urllib.request, hashlib, ast, json, time, gc, math
import traceback, platform, types, random, shutil
from pathlib import Path
from datetime import datetime, timezone
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')

# ---------------------------------------------------------------------------------------------------------- versions
# Bootstrap record (stdlib only) is created BEFORE the torch check / pip / imports, so a bootstrap failure is recorded.
RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
ROOT = Path(('/content/' if Path('/content').exists() else '/tmp/') + 'TEST894_' + RUN_ID)
ROOT.mkdir(parents=True, exist_ok=True)
LOG = ROOT / 'TEST894.log'; OUT = ROOT / 'TEST894_results.json'; LOG.write_text('')
ZIP_PATH = ROOT.parent / ('TEST894_SONUC_' + RUN_ID + '.zip'); RECEIPT_PATH = ROOT.parent / ('TEST894_SONUC_' + RUN_ID + '_RECEIPT.json')
def _ver(name):
    try: return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError: return None
def _boot_fail(e):
    tb = traceback.format_exc()
    rec = {'test': 'TEST894', 'run_id': RUN_ID, 'status': 'BOOTSTRAP_ERROR', 'error': '%s: %s' % (type(e).__name__, e),
           'traceback': tb, 'installed_versions': {p_: _ver(p_) for p_ in ('torch', 'transformers', 'accelerate', 'bitsandbytes')},
           'technical_verdict': 'NOT_RUN', 'ARTIFACT_STATUS': 'FAIL', 'gpu_model_loaded': False,
           'note': 'stopped before any model / GPU work; Drive not attempted'}
    for path_, txt_ in ((OUT, json.dumps(rec, indent=2)), (RECEIPT_PATH, json.dumps(rec, indent=2))):
        try: tmp_ = Path(str(path_) + '.tmp'); tmp_.write_text(txt_); tmp_.replace(path_)
        except Exception as e2: print('BOOTSTRAP_RECORD_WRITE_FAILED', path_, e2)
    with LOG.open('a') as f_: f_.write('BOOTSTRAP_ERROR %s\n%s\nARTIFACT_STATUS=FAIL\n' % (rec['error'], tb))
    print(tb); print('TEST894 BOOTSTRAP_ERROR recorded in', OUT, LOG, RECEIPT_PATH)
    raise SystemExit('TEST894 BOOTSTRAP_ERROR: ' + rec['error'])
try:
    # Exact runtime contract. torch 2.14.1+cu130 / CUDA 13.0 / transformers 5.22.1 = the combination recorded in 893.log
    # (TABLE GATE0 RUNTIME) under which this engine, incl. api877, ran on the A100. accelerate 1.16.0 / bitsandbytes 0.50.2 =
    # the versions whose sources K3.1 audited (not recorded in 893.log). torch is never installed or changed by this cell.
    TORCH_REQ = '2.14.1+cu130'; CUDA_REQ = '13.0'
    PINS = {'transformers': '5.22.1', 'accelerate': '1.16.0', 'bitsandbytes': '0.50.2'}
    if _ver('torch') != TORCH_REQ:
        raise SystemExit('TEST894_ENV: torch %s found, %s required (893.log runtime); no torch change is made' % (_ver('torch'), TORCH_REQ))
    _need = [p for p, v in PINS.items() if _ver(p) != v]
    if _need:
        _loaded = [p for p in _need if p in sys.modules]
        if _loaded: raise SystemExit('TEST894_ENV: %s already imported with other versions; restart the runtime and rerun' % _loaded)
        _con = Path('/tmp/TEST894_torch_constraint.txt'); _con.write_text('torch==%s\n' % TORCH_REQ)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', '-c', str(_con)] + ['%s==%s' % (p, PINS[p]) for p in _need])
    _got = {p: _ver(p) for p in list(PINS) + ['torch']}
    if any(_got[p] != v for p, v in PINS.items()) or _got['torch'] != TORCH_REQ:
        raise SystemExit('TEST894_ENV: version contract not met after install: %s' % _got)
    import torch, transformers, accelerate, bitsandbytes
    if torch.__version__ != TORCH_REQ or torch.version.cuda != CUDA_REQ or transformers.__version__ != PINS['transformers'] or \
            accelerate.__version__ != PINS['accelerate'] or bitsandbytes.__version__ != PINS['bitsandbytes']:
        raise SystemExit('TEST894_ENV: imported versions differ from the contract: torch %s cuda %s transformers %s accelerate %s '
                         'bitsandbytes %s' % (torch.__version__, torch.version.cuda, transformers.__version__, accelerate.__version__,
                                              bitsandbytes.__version__))
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    from transformers.cache_utils import DynamicCache
except BaseException as _e:
    if isinstance(_e, KeyboardInterrupt): raise
    _boot_fail(_e)

# --------------------------------------------------------------------------------------------------------- constants
TAG = 'TEST894'; MARKER = 'AKBASCORE SILICON HIPPOCAMPUS — TEST894 — LoRA–CUT3 BACKWARD PREFLIGHT'
COMMIT = 'f1007d912773f3460536784ff80a215741bc97e9'
RAW_BASE = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/' + COMMIT + '/'
MODEL_ID = 'Qwen/Qwen2.5-72B-Instruct'; CUT = 3; DTYPE = torch.bfloat16; DEV = torch.device('cuda:0')
# Hugging Face main of Qwen/Qwen2.5-72B-Instruct (file tree read 2026-11-17: head 495f393 "Update README.md"; weights,
# tokenizer.json, vocab, merges at f689aa0, tokenizer_config.json at a13fff9, config.json at c970f6d — all ancestors).
MODEL_REVISION = '495f39366efef23836d0cfae4fbe635880d2be31'
GPU_NAME_REQ = 'NVIDIA A100-SXM4-80GB'; GPU_CC_REQ = (8, 0)
EXPECTED = (80, 8192, 64, 8, 128); CHUNK = 128; GPU_RESERVE_GIB = 9.0
SEED = 20261117
CART_DIR = ROOT / 'cartridges'; CART_DIR.mkdir(exist_ok=True)
DRIVE_DIR = None; DRIVE_ERR = {'mount': None, 'backup_failures': 0, 'last': None}
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
    'dir_max_frac_of_loss': 0.5,       # well-posed only if each target decrease <= this fraction of the probe loss L0
    'dir_max_step_frac_of_lora_norm': 0.05,  # well-posed only if each step norm <= this fraction of the LoRA norm
    'surrogate_rel_err': 1e-6,         # float64 local surrogate: autograd vs central finite difference
    'vram_reserved_frac_max': 0.95,    # peak reserved / total device memory
    'p6_clean_slack_mib': 256,         # allocated memory after a P6 row cleanup may exceed the pre-P6 baseline by at most this
    'P_expected': 30, 'chunk_expected': 128}
LIVE_LENGTHS = (64, 256); LONG_TARGET_TOKENS = 2000
CRITICAL = ('ENV', 'SOURCE', 'EXTRACT', 'MODEL', 'P0_C_WRAPPER_OFF_IDENTITY', 'P0_D_ZERO_LORA_IDENTITY', 'P1_PHYSICAL',
            'P2_LIVE_AUTOGRAD', 'P3_GRADIENT', 'P7_INTEGRITY')
REQUIRED = ('P0_A_FORGE_REBUILD_PARITY', 'P0_B_EXPLICIT_APPEND_PARITY', 'P4_NUMERICAL', 'P5_TRAIN_INFER', 'P6_RESOURCE')
GATE_ORDER = ('ENV', 'SOURCE', 'EXTRACT', 'MODEL', 'P0_A_FORGE_REBUILD_PARITY', 'P0_B_EXPLICIT_APPEND_PARITY',
              'P0_C_WRAPPER_OFF_IDENTITY', 'P0_D_ZERO_LORA_IDENTITY', 'P1_PHYSICAL', 'P2_LIVE_AUTOGRAD', 'P3_GRADIENT',
              'P4_NUMERICAL', 'P5_TRAIN_INFER', 'P6_RESOURCE', 'P7_INTEGRITY', 'S8_CONTENT_DEPENDENCE', 'P8_READABILITY')

R = {'test': 'TEST894', 'stage': 'LoRA-CUT3 backward preflight', 'run_id': RUN_ID, 'commit': COMMIT, 'status': 'STARTED',
     'checks': [], 'gates': {g: {'status': 'NOT_RUN', 'reason': None, 'data': {}} for g in GATE_ORDER},
     'context': {'previous_test': 'TEST893', 'test893_final': 'VERDICT=FAIL PHYSICAL_VALIDITY=PASS SCIENTIFIC_VALIDITY=PASS '
                 'OUTCOME=FAIL_NO_GAIN (893.log, cross-checked in SOURCE; not reinterpreted)', 'engine_commit': COMMIT},
     'model_revision': MODEL_REVISION, 'runtime_pins': dict(PINS, torch=TORCH_REQ, cuda=CUDA_REQ),
     'scope': 'technical feasibility only; not a learning / semantic / native-behaviour / autonomy result',
     'executed_by_author': False, 'tolerances': TOL,
     'tolerances_sha256': hashlib.sha256(json.dumps(TOL, sort_keys=True).encode()).hexdigest()}
T0 = time.perf_counter()

# ----------------------------------------------------------------------------------------------------------- logging
def log(*xs):
    s = ' '.join(str(x) for x in xs); print(s, flush=True)
    with LOG.open('a') as f: f.write(s + '\n')
def save():
    # atomic local write after every check / gate / exception, then a progressive Drive backup of log + JSON (TEST870 style)
    R['drive_backup'] = dict(DRIVE_ERR, dir=DRIVE_DIR)
    tmp = OUT.with_suffix('.json.tmp'); tmp.write_text(json.dumps(R, ensure_ascii=False, indent=2, default=str)); tmp.replace(OUT)
    if DRIVE_DIR is not None:
        try:
            for f_ in (LOG, OUT): shutil.copy2(f_, Path(DRIVE_DIR) / f_.name)
        except Exception as e:
            DRIVE_ERR['backup_failures'] += 1; DRIVE_ERR['last'] = '%s: %s' % (type(e).__name__, e)
def check(name, ok, detail=None):
    # same signature/semantics as the 730/757 check() used by the extracted engine definitions
    R['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail}); save()
    log('PASS' if ok else 'FAIL', name, '' if detail is None else json.dumps(detail, default=str)[:600])
    if not ok: raise RuntimeError('CHECK_FAILED:' + name)
class StopT894(Exception): pass
def gate(name, status, reason=None, **data):
    assert status in ('PASS', 'FAIL', 'INCONCLUSIVE', 'DIAGNOSTIC'), status
    R['gates'][name] = {'status': status, 'reason': reason, 'data': data}; save()
    log('GATE', name, status, '' if reason is None else '| ' + str(reason))
    if status == 'FAIL' and name in CRITICAL: raise StopT894(name + ': ' + str(reason))
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
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'AKBASCORE-TEST894'}), timeout=120) as f:
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
class LoRAProj894(torch.nn.Module):
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
def hook_inventory(root=None):
    root = model if root is None else root
    mm = torch.nn.modules.module
    glob = {n: len(getattr(mm, n, None) or {}) for n in ('_global_forward_hooks', '_global_forward_pre_hooks',
            '_global_backward_hooks', '_global_backward_pre_hooks', '_global_forward_hooks_always_called')}
    mods = {'_forward_hooks': 0, '_forward_pre_hooks': 0, '_backward_hooks': 0, '_backward_pre_hooks': 0}; where = []
    inst_forward = []; hf = 0
    for name, m in root.named_modules():
        for a in mods:
            d = getattr(m, a, None)
            if d: mods[a] += len(d); where.append([name, a, len(d)])
        # an instance 'forward' that is just the class method re-bound (730 DirectCut3.__exit__ does this) is benign
        if 'forward' in m.__dict__ and getattr(m.__dict__['forward'], '__func__', None) is not type(m).forward:
            inst_forward.append(name)
        if hasattr(m, '_hf_hook'): hf += 1
    tens = 0
    for p in root.parameters():
        for a in ('_backward_hooks', '_post_accumulate_grad_hooks'):
            d = getattr(p, a, None)
            if d: tens += len(d)
    torch_hooks = sum(glob.values()) + sum(mods.values()) + tens
    return {'torch_hooks_total': torch_hooks, 'global': glob, 'module': mods, 'tensor': tens, 'where': where[:20],
            'instance_forward_overrides': inst_forward[:20], 'instance_forward_override_count': len(inst_forward),
            'accelerate_hf_hook_modules': hf}
def hooks_clean(inv):
    # fail-closed: no PyTorch hook, no Accelerate _hf_hook, no persistent instance-forward override (benign re-binds excluded)
    return inv['torch_hooks_total'] == 0 and inv['accelerate_hf_hook_modules'] == 0 and inv['instance_forward_override_count'] == 0
# --- base integrity: real SHA-256 over raw bytes, streamed in 64 MiB device->host blocks (no full-size copies) ---------
BLK = 64 << 20
def _stream(h, t):
    v = t.detach().contiguous().reshape(-1).view(torch.uint8)
    for st in range(0, v.numel(), BLK): h.update(v[st:st + BLK].cpu().numpy().tobytes())
def _qs_items(qs, pre='qs'):
    # canonical NF4 quantization state of one Linear4bit weight: tensors + metadata, nested (double-quant) state included
    if qs is None or getattr(qs, 'absmax', None) is None: raise RuntimeError('NF4_QUANT_STATE_MISSING ' + pre)
    items = [(pre + '.' + a, getattr(qs, a, None)) for a in ('absmax', 'code', 'offset', 'blocksize', 'quant_type', 'dtype', 'shape', 'nested')]
    if getattr(qs, 'state2', None) is not None: items += _qs_items(qs.state2, pre + '.state2')
    return items
def _digest_items(h, items):
    for k, v in items:
        if torch.is_tensor(v): h.update(('%s|T|%s|%s;' % (k, v.dtype, tuple(v.shape))).encode()); _stream(h, v)
        else: h.update(('%s|V|%r;' % (k, v)).encode())
def integrity_digest(params, q4mods, bufs):
    h = hashlib.sha256(); t_ = time.perf_counter(); nb = 0
    for name, p in params:
        h.update(('P|%s|%s|%s;' % (name, p.dtype, tuple(p.shape))).encode()); _stream(h, p.data); nb += p.numel() * p.element_size()
    for name, m in q4mods: _digest_items(h, [('Q|' + name + '|' + k, v) for k, v in _qs_items(m.weight.quant_state)])
    for name, b in bufs: h.update(('B|%s|%s|%s;' % (name, b.dtype, tuple(b.shape))).encode()); _stream(h, b)
    return {'sha256': h.hexdigest(), 'param_tensors': len(params), 'nf4_quant_states': len(q4mods), 'buffers': len(bufs),
            'param_bytes': nb, 'seconds': round(time.perf_counter() - t_, 1)}
def integrity_selftest(q4mod):
    # small CPU-only mutation checks; the model's own tensors are never modified
    def sha_of(items): h = hashlib.sha256(); _digest_items(h, items); return h.hexdigest()
    x = (torch.arange(600) % 256).to(torch.uint8); y = x.clone(); y[10], y[261] = int(x[261]), int(x[10])
    old = lambda z: (int(z.to(torch.int64).sum()), int((z.to(torch.int64) * ((torch.arange(z.numel()) % 251) + 1)).sum()))
    swap = {'old_block_sum_collides': old(x) == old(y), 'sha256_detects': sha_of([('x', x)]) != sha_of([('x', y)])}
    real0 = sha_of(_qs_items(q4mod.weight.quant_state))
    cp_ = [(k, v.detach().cpu().clone() if torch.is_tensor(v) else v) for k, v in _qs_items(q4mod.weight.quant_state)]
    base = sha_of(cp_); ia = [i for i, (k, _) in enumerate(cp_) if k.endswith('.absmax')][0]
    ab = [(k, v.clone() if torch.is_tensor(v) else v) for k, v in cp_]; t2 = ab[ia][1].reshape(-1); t2[0] = t2[0] + 1
    ib = [i for i, (k, _) in enumerate(cp_) if k == 'qs.blocksize'][0]
    md = list(cp_); md[ib] = (md[ib][0], (md[ib][1] or 0) + 1)
    res = {'byte_swap_i_i+251': swap, 'absmax_mutation_detected': sha_of(ab) != base, 'metadata_mutation_detected': sha_of(md) != base,
           'cpu_copy_equals_live': base == real0, 'live_quant_state_untouched': sha_of(_qs_items(q4mod.weight.quant_state)) == real0}
    res['pass'] = swap['sha256_detects'] and res['absmax_mutation_detected'] and res['metadata_mutation_detected'] and \
        res['cpu_copy_equals_live'] and res['live_quant_state_untouched']
    return res
def hook_selftest():
    # the inventory must flag an Accelerate hook and must NOT flag a completed 730 DirectCut3 enter/exit (CPU dummy module)
    from accelerate.hooks import add_hook_to_module, remove_hook_from_module, ModelHook
    m = torch.nn.Sequential(torch.nn.Linear(2, 2)); clean0 = hooks_clean(hook_inventory(m))
    with DirectCut3(m[0], 'capture', collector=[]): m(torch.zeros(1, 2))
    after_dc3 = hooks_clean(hook_inventory(m))
    add_hook_to_module(m[0], ModelHook()); flagged = not hooks_clean(hook_inventory(m)); remove_hook_from_module(m[0])
    return {'clean_dummy': clean0, 'directcut3_restored_is_clean': after_dc3, 'accelerate_hook_flagged': flagged,
            'pass': clean0 and after_dc3 and flagged}
class _PinnedRevision:
    """Binds MODEL_REVISION into the unchanged 757 model_setup() calls (it resolves AutoTokenizer / AutoModelForCausalLM
    through this cell's globals); refuses any other revision."""
    def __init__(self, cls): self.cls = cls
    def from_pretrained(self, mid, *a, **kw):
        if mid != MODEL_ID or kw.get('revision', MODEL_REVISION) != MODEL_REVISION: raise RuntimeError('MODEL_REVISION_CONTRACT')
        kw['revision'] = MODEL_REVISION; PINNED_CALLS.append([self.cls.__name__, mid, kw['revision']])
        return self.cls.from_pretrained(mid, *a, **kw)
PINNED_CALLS = []
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
    log('=' * 112); log(MARKER, RUN_ID, '| engine commit', COMMIT, '| continuation of TEST893 (FAIL_NO_GAIN, unchanged)')
    log('SCOPE: feasibility only. PASS != learning / semantic reading / native behaviour / autonomy.'); log('=' * 112)
    log('TOLERANCES', json.dumps(TOL, sort_keys=True), 'sha256', R['tolerances_sha256'])
    # executed-cell identity, single cell. Trust root = the git objects of the repository, not this cell: the commit that
    # main points to and the blob id its tree records for 894sinirag.py (both hashed by git over the committed bytes; git
    # verifies the objects it fetches). The file is also fetched as raw bytes at that commit (second channel) and must be
    # byte-identical. The executed cell (IPython history) must equal the committed bytes after ONE canonicalization only:
    # leading and trailing '\n' characters are removed from both sides (run 20261118T014044Z: the pasted cell = one extra
    # leading newline + no final newline, otherwise byte-identical). Nothing inside the text is changed. The cell never derives an expected hash from its
    # own text; commit + blob + SHA-256 are recorded for comparison with the externally announced audited identity.
    SRC_REPO = 'ceceli33/titan-cognitive-core-v3'; SRC_FILE = '894sinirag.py'
    ec = {'status': 'NOT_CAPTURED', 'identity_match': False}
    try:
        _hist = list(globals()['get_ipython']().history_manager.input_hist_raw)
        _cell = [x for x in _hist if MARKER in x and 'def integrity_selftest' in x][-1]
        (ROOT / 'TEST894_cell_source.py').write_text(_cell, encoding='utf-8'); _cb = _cell.encode('utf-8')
        ec.update(status='CAPTURED', sha256=sha_bytes(_cb), git_blob=gitblob(_cb), git_blob_with_final_newline=gitblob(_cb + b'\n'),
                  lines=_cell.count('\n') + 1, file=str(ROOT / 'TEST894_cell_source.py'))
    except Exception as e:
        ec['capture_error'] = '%s: %s' % (type(e).__name__, e)
    try:
        _gd = ROOT.parent / ('TEST894_srcid_' + RUN_ID); _genv = dict(os.environ, GIT_TERMINAL_PROMPT='0')
        _git = lambda *a: subprocess.run(['git'] + list(a), check=True, capture_output=True, timeout=180, env=_genv).stdout
        _git('clone', '-q', '--depth', '1', '--filter=blob:none', '--no-checkout', 'https://github.com/' + SRC_REPO, str(_gd))
        _c = _git('-C', str(_gd), 'rev-parse', 'HEAD').decode().strip()
        _b = _git('-C', str(_gd), 'rev-parse', 'HEAD:' + SRC_FILE).decode().strip()
        _pb = _git('-C', str(_gd), 'cat-file', 'blob', _b)
        with urllib.request.urlopen(urllib.request.Request('https://raw.githubusercontent.com/%s/%s/%s' % (SRC_REPO, _c, SRC_FILE),
                                                           headers={'User-Agent': 'AKBASCORE-TEST894'}), timeout=120) as f_:
            _rb = f_.read()
        ec['published'] = {'repo': SRC_REPO, 'commit': _c, 'tree_blob': _b, 'blob_of_bytes': gitblob(_pb), 'sha256': sha_bytes(_pb),
                           'bytes': len(_pb), 'raw_channel_equal': _rb == _pb}
        _pub_ok = gitblob(_pb) == _b and _rb == _pb
        ec['canonicalization'] = "strip leading/trailing b'\\n' on both sides only; interior bytes compared exactly"
        if ec['status'] == 'CAPTURED':
            _cc, _pc = _cb.strip(b'\n'), _pb.strip(b'\n')
            ec['identity_match'] = _pub_ok and _cc == _pc
            ec['boundary_newlines'] = {'cell_leading': len(_cb) - len(_cb.lstrip(b'\n')), 'cell_trailing': len(_cb) - len(_cb.rstrip(b'\n')),
                                       'published_leading': len(_pb) - len(_pb.lstrip(b'\n')), 'published_trailing': len(_pb) - len(_pb.rstrip(b'\n'))}
            if _cc != _pc:
                _i = next((k for k in range(min(len(_cc), len(_pc))) if _cc[k] != _pc[k]), min(len(_cc), len(_pc)))
                ec['first_difference'] = {'offset_after_canonicalization': _i, 'line': _cc[:_i].count(b'\n') + 1,
                                          'cell_bytes': _cc[_i:_i + 40].decode('utf-8', 'replace'), 'published_bytes': _pc[_i:_i + 40].decode('utf-8', 'replace')}
        shutil.rmtree(_gd, ignore_errors=True)
    except Exception as e:
        ec['published_error'] = '%s: %s' % (type(e).__name__, str(e)[:300])
    R['executed_cell'] = ec
    log('EXECUTED_CELL', json.dumps(R['executed_cell']))
    # ---------------------------------------------------------------------------------------------------- ENV
    env = {'python': platform.python_version(), 'torch': torch.__version__, 'cuda': torch.version.cuda,
           'transformers': transformers.__version__, 'accelerate': accelerate.__version__, 'bitsandbytes': bitsandbytes.__version__,
           'cuda_available': torch.cuda.is_available(), 'device_count': torch.cuda.device_count()}
    if env['cuda_available']:
        pr = torch.cuda.get_device_properties(0)
        env.update(gpu=torch.cuda.get_device_name(0), gpu_bytes=int(pr.total_memory), compute_capability=[pr.major, pr.minor])
    R['env'] = env; log('ENV', json.dumps(env))
    env_ok = (env['cuda_available'] and env['device_count'] == 1 and env.get('gpu') == GPU_NAME_REQ and
              tuple(env.get('compute_capability', ())) == GPU_CC_REQ and env.get('gpu_bytes', 0) >= 79 * 2**30)
    gate('ENV', 'PASS' if env_ok else 'FAIL', None if env_ok else 'requires exactly one %s (cc %s)' % (GPU_NAME_REQ, GPU_CC_REQ), **env)
    random.seed(SEED); torch.manual_seed(SEED); torch.cuda.manual_seed_all(SEED)
    # Drive early (TEST870 method): mounted before the long model load so log + JSON are backed up after every gate
    try:
        from google.colab import drive as _gdrive
        _gdrive.mount('/content/drive'); DRIVE_DIR = '/content/drive/MyDrive/TEST894_' + RUN_ID; os.makedirs(DRIVE_DIR, exist_ok=True)
        log('DRIVE_BACKUP_DIR', DRIVE_DIR)
    except Exception as e:
        DRIVE_DIR = None; DRIVE_ERR['mount'] = '%s: %s' % (type(e).__name__, e)
        log('DRIVE_NOT_MOUNTED', DRIVE_ERR['mount'], '| local files are kept in', ROOT, '(download them at the end)')
    save()
    # ------------------------------------------------------------------------------------------------- SOURCE
    RAW = {}; blobs = {}
    for name in LOCKS:
        RAW[name] = fetch_pinned(name); blobs[name] = gitblob(RAW[name])
    k31 = {n: {'k31': v, 'actual': blobs[n], 'match': blobs[n] == v} for n, v in K31_BLOBS.items()}
    lock = {n: {'lock': v, 'actual': blobs[n], 'match': blobs[n] == v} for n, v in LOCKS.items()}
    g1 = [l for l in RAW['893.log'].decode('utf-8', 'replace').splitlines() if l.startswith('T893 GATE G1 PASS')]
    g1d = json.loads(g1[0].split('T893 GATE G1 PASS', 1)[1].strip()) if len(g1) == 1 else {}
    fin893 = [l for l in RAW['893.log'].decode('utf-8', 'replace').splitlines() if l.startswith('TEST893_FINAL VERDICT=')]
    fin_ok = len(fin893) == 1 and all(s in fin893[0] for s in ('VERDICT=FAIL', 'PHYSICAL_VALIDITY=PASS', 'SCIENTIFIC_VALIDITY=PASS',
                                                              'OUTCOME=FAIL_NO_GAIN'))
    src_ok = all(x['match'] for x in lock.values()) and all(x['match'] for x in k31.values()) and \
        g1d.get('P') == TOL['P_expected'] and g1d.get('chunk') == TOL['chunk_expected'] and fin_ok
    gate('SOURCE', 'PASS' if src_ok else 'FAIL', None if src_ok else 'blob lock / K3.1 blob / 893.log G1 / TEST893_FINAL cross-check failed',
         locks=lock, k31_blob_check=k31, log893_G1={'P': g1d.get('P'), 'chunk': g1d.get('chunk'), 'gpu_wall_s': g1d.get('wall_s')},
         test893_final_line=fin893[0][:200] if fin893 else None)
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
    AutoTokenizer, AutoModelForCausalLM = _PinnedRevision(transformers.AutoTokenizer), _PinnedRevision(transformers.AutoModelForCausalLM)
    t = time.perf_counter(); model_setup(); load_s = round(time.perf_counter() - t, 1)
    from huggingface_hub import hf_hub_download
    rev_files = {}
    for fn in ('config.json', 'tokenizer.json', 'tokenizer_config.json', 'model.safetensors.index.json'):
        pth = hf_hub_download(MODEL_ID, fn, revision=MODEL_REVISION)
        rev_files[fn] = {'sha256': sha_path(pth), 'in_pinned_snapshot': ('/snapshots/%s/' % MODEL_REVISION) in pth.replace('\\', '/')}
    # transformers 5.22.1 leaves config._commit_hash empty (TEST894 run 20261118T014044Z: null). Revision evidence is therefore:
    # both from_pretrained calls went through the pin with MODEL_REVISION, and every weight shard named by the pinned index
    # plus config / tokenizer files resolves inside snapshots/<MODEL_REVISION>. A non-empty _commit_hash must still match.
    from huggingface_hub import try_to_load_from_cache
    _snap = '/snapshots/%s/' % MODEL_REVISION
    _shards = sorted(set(json.loads(Path(hf_hub_download(MODEL_ID, 'model.safetensors.index.json', revision=MODEL_REVISION)).read_text())['weight_map'].values()))
    _sp = {f_: try_to_load_from_cache(MODEL_ID, f_, revision=MODEL_REVISION) for f_ in _shards}
    shards_ok = len(_shards) > 0 and all(isinstance(v, str) and _snap in v.replace('\\', '/') and os.path.exists(v) for v in _sp.values())
    calls_ok = sorted(c[0] for c in PINNED_CALLS) == ['AutoModelForCausalLM', 'AutoTokenizer'] and all(c[2] == MODEL_REVISION for c in PINNED_CALLS)
    _ch = getattr(model.config, '_commit_hash', None)
    rev_ok = calls_ok and shards_ok and all(v['in_pinned_snapshot'] for v in rev_files.values()) and _ch in (None, MODEL_REVISION)
    hooks_load = hook_inventory(); hst = hook_selftest()
    base_params = [(n, p) for n, p in model.named_parameters()]
    Q4MODS = [(n, m) for n, m in model.named_modules() if isinstance(m, bitsandbytes.nn.Linear4bit)]
    BUFS = [(n, b) for n, b in model.named_buffers()]
    ist = integrity_selftest(Q4MODS[0][1])
    mc = {'P_is_30': P == TOL['P_expected'], 'base_frozen': all(not p.requires_grad for _, p in base_params), 'eval_mode': not model.training,
          'hooks_clean': hooks_clean(hooks_load), 'hook_selftest': hst['pass'], 'integrity_selftest': ist['pass'],
          'model_revision': rev_ok, 'nf4_modules_present': len(Q4MODS) > 0,
          'sdpa': getattr(model.config, '_attn_implementation', None) == 'sdpa',
          'attention_dropout_zero': float(getattr(model.config, 'attention_dropout', 0.0)) == 0.0}
    model_ok = all(mc.values())
    gate('MODEL', 'PASS' if model_ok else 'FAIL', None if model_ok else 'failed conditions: ' + ', '.join(k for k, v in mc.items() if not v),
         conditions=mc, revision_evidence={'pinned_calls': PINNED_CALLS, 'shards': len(_shards), 'shards_in_pinned_snapshot': shards_ok,
                                           'config_commit_hash': _ch},
         load_s=load_s, P=P, prefix_sha256=sha_bytes(PREFIX.encode()), base_param_tensors=len(base_params), nf4_modules=len(Q4MODS),
         buffers=len(BUFS), hooks=hooks_load, hook_selftest=hst, integrity_selftest=ist, gpu=gpu_mem(),
         model_revision_expected=MODEL_REVISION, model_revision_loaded=getattr(model.config, '_commit_hash', None),
         revision_files=rev_files, tokenizer_commit_hash=getattr(tok, 'init_kwargs', {}).get('_commit_hash'))
    ENV = {'model': model, 'DEV': DEV, 'P': P, 'NL': NL, 'H': H, 'cache_build': cache_build}
    api_err = None
    try: api877(ENV)
    except Exception as e: api_err = '%s: %s' % (type(e).__name__, e)
    log('API877', 'OK' if api_err is None else api_err, json.dumps(STATE877.get('api', {}), default=str))
    W0 = {'sentinel': sentinel(), 'weights877': weights_digest877(ENV), 'integrity': integrity_digest(base_params, Q4MODS, BUFS)}
    log('BASE_INTEGRITY', json.dumps(W0))
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
        with MountOff(): cp, secs = forge_native(ids, 'T894_' + RUN_ID + '_' + cid)
        path = CART_DIR / ('T894_' + RUN_ID + '_' + cid + '.pt'); tmp = Path(str(path) + '.tmp')
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
    if st_a == 'FAIL': raise StopT894('P0_A native parity FAIL')
    if api_err is None:
        nat = mount_append(MEM['A'], 'B')
        with MountOff(): exp = list(xappend878(ENV, list(MEM['A']), to_gpu(CP['B']), ()))
        cmp_b = kv_compare(nat, exp); st_b = tri(cmp_b)
        gate('P0_B_EXPLICIT_APPEND_PARITY', st_b, 'locked native append (757) vs explicit no-hook append (878/877)', compare=cmp_b)
        del nat, exp
        if st_b == 'FAIL': raise StopT894('P0_B native parity FAIL')
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
            base_ids['L%d.%s' % (i, nm)] = id(b); w = LoRAProj894(b, LORA_R, LORA_ALPHA, 'L%d.%s' % (i, nm), gen)
            setattr(sa, nm, w); LORA.append(w)
    LORA_PARAMS = [p for w in LORA for p in (w.lora_A, w.lora_B)]; LORA_IDS = {id(p) for p in LORA_PARAMS}
    install_ok = (len(LORA) == NL * len(LORA_TARGETS) and all(id(getattr(model.model.layers[int(w.lcp_name[1:].split('.')[0])].self_attn,
                  w.lcp_name.split('.')[1]).base) == base_ids[w.lcp_name] for w in LORA))
    BASE_ONLY = [(n, p) for n, p in model.named_parameters() if id(p) not in LORA_IDS]
    trainable = [n for n, p in model.named_parameters() if p.requires_grad]
    adapter_set_ok = len(BASE_ONLY) == len(base_params) and len(trainable) == len(LORA_PARAMS) and \
        all(id(p) in LORA_IDS for _, p in model.named_parameters() if p.requires_grad)
    n_lora = sum(p.numel() for p in LORA_PARAMS); hooks_install = hook_inventory()
    log('LORA_INSTALLED', len(LORA), 'modules', n_lora, 'params', 'adapter_set_ok', adapter_set_ok, 'hooks_clean', hooks_clean(hooks_install))
    if not (install_ok and adapter_set_ok and hooks_clean(hooks_install)): raise StopT894('LORA_INSTALL_CONTRACT')
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
        tw = time.perf_counter(); opt.zero_grad(set_to_none=True); torch.cuda.reset_peak_memory_stats(); tf = time.perf_counter()
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
                      'optimizer_s': round(t_o, 3), 'step_wall_s': round(time.perf_counter() - tw, 3), 'peak': gpu_mem(),
                      'calls_on': r_['calls_on']})
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
    f = (u * LoRAProj894.lora_delta(x, Aq, Bq, w79.scale)).sum(); f.backward()
    dA = torch.randn(Aq.shape, generator=gs, dtype=torch.float64); dB = torch.randn(Bq.shape, generator=gs, dtype=torch.float64)
    an = float((Aq.grad * dA).sum() + (Bq.grad * dB).sum()); eps = 1e-6
    with torch.no_grad():
        fp = float((u * LoRAProj894.lora_delta(x, Aq + eps * dA, Bq + eps * dB, w79.scale)).sum())
        fm = float((u * LoRAProj894.lora_delta(x, Aq - eps * dA, Bq - eps * dB, w79.scale)).sum())
    fd = (fp - fm) / (2 * eps); sur_err = abs(an - fd) / max(abs(an), 1e-30)
    snap = [p.detach().clone() for p in LORA_PARAMS]; probes = []; probe_err = None; gn2 = float('nan'); L0 = float('nan')
    # Probe loss = counterfactual readout T2 under mount A. Run 20261118T021423Z probed the trained target T1, whose loss
    # was ~2e-5 nats (saturated): a 0.02 / 0.1 nat first-order decrease was impossible (loss >= 0) and eta = delta/|g|^2
    # gave steps 5.7x / 28x the whole LoRA norm. T2 under A is not saturated; the function under test (LoRA backward of
    # the live readout loss on the real NF4 engine) is the same. Parameters are restored bitwise afterwards.
    PT = t2_ids; lora_norm = math.sqrt(float(sum((p.detach().double() ** 2).sum() for p in LORA_PARAMS)))
    try:
        gp = live(MEM['A'], sfx_ids, PT, grad=True, train=True, adapter=True); l_ = -gp['lp'].mean()
        grads = torch.autograd.grad(l_, LORA_PARAMS, allow_unused=True); del gp, l_
        grads = [torch.zeros_like(p) if g_ is None else g_ for g_, p in zip(grads, LORA_PARAMS)]
        gn2 = float(sum((g_.double() ** 2).sum() for g_ in grads))
        L0 = -lp_sum(MEM['A'], sfx_ids, PT, True) / len(PT)
        for dlt in TOL['dir_targets_nats']:
            eta = dlt / max(gn2, 1e-30)
            with torch.no_grad():
                for p, g_ in zip(LORA_PARAMS, grads): p.sub_(eta * g_)
            L1 = -lp_sum(MEM['A'], sfx_ids, PT, True) / len(PT)
            with torch.no_grad():
                for p, s_ in zip(LORA_PARAMS, snap): p.copy_(s_)
            probes.append({'predicted_delta': -dlt, 'actual_delta': L1 - L0, 'ratio': (L1 - L0) / -dlt, 'eta': eta,
                           'step_norm': eta * math.sqrt(gn2), 'well_posed': dlt <= TOL['dir_max_frac_of_loss'] * L0 and
                           eta * math.sqrt(gn2) <= TOL['dir_max_step_frac_of_lora_norm'] * lora_norm})
    except Exception as e:
        probe_err = '%s: %s' % (type(e).__name__, str(e)[:300])
    finally:
        grads = None
        with torch.no_grad():
            for p, s_ in zip(LORA_PARAMS, snap): p.copy_(s_)
        restored = all(torch.equal(p.detach(), s_) for p, s_ in zip(LORA_PARAMS, snap)); del snap; release()
    lo, hi = TOL['dir_ratio_band']
    if sur_err > TOL['surrogate_rel_err'] or not restored: st4 = 'FAIL'
    elif probe_err is not None or len(probes) != len(TOL['dir_targets_nats']): st4 = 'INCONCLUSIVE'
    elif not all(pp['well_posed'] for pp in probes): st4 = 'INCONCLUSIVE'      # outside the first-order regime: no verdict
    elif all(pp['actual_delta'] > TOL['dir_fail_increase_nats'] for pp in probes): st4 = 'FAIL'
    elif all(pp['actual_delta'] < 0 for pp in probes) and lo <= probes[0]['ratio'] <= hi: st4 = 'PASS'
    else: st4 = 'INCONCLUSIVE'
    gate('P4_NUMERICAL', st4, 'float64 local surrogate (LoRA math, CPU) + real-NF4-engine directional loss probe',
         surrogate_rel_err=sur_err, surrogate_where='CPU float64, LoRAProj894.lora_delta only (no 72B)',
         directional_where='real NF4 72B, base-OFF mount A, eval no_grad loss before/after a -eta*g LoRA step, restored',
         grad_norm=math.sqrt(gn2) if gn2 == gn2 else None, loss_L0=L0, probes=probes, params_restored=restored, probe_error=probe_err,
         probe_target='T2 under mount A (counterfactual, not saturated)', lora_param_norm=lora_norm)
    if not restored: raise StopT894('P4: LoRA parameters not restored bitwise after the directional probe')
    # ------------------------------------------------------------------------------------------- P6 resources
    def filler(n):
        s = (' ' + T1 + ' -> ' + T2 + '.') * (n // 3 + 8); ids_ = tok(s, add_special_tokens=False).input_ids[:n]; assert len(ids_) == n; return ids_
    res = []; p6_stop = None
    opt.zero_grad(set_to_none=True); release(); torch.cuda.synchronize(); base_alloc = torch.cuda.memory_allocated()
    for pname in ('A', 'LONG_A', 'XL'):
        for Ltot in LIVE_LENGTHS:
            row = {'prefix': pname, 'prefix_tokens': int(MEM[pname][0][0].shape[-2]), 'live_tokens': Ltot}
            if p6_stop is not None:
                row.update(status='NOT_RUN', reason=p6_stop); res.append(row); log('P6', json.dumps(row, default=str)); continue
            r_ = l_ = cb = None; tw = time.perf_counter()
            try:
                if Ltot <= len(sfx_ids): raise RuntimeError('LIVE_LENGTH_SHORTER_THAN_SUFFIX')
                tg = filler(Ltot - len(sfx_ids)); torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
                tc = time.perf_counter(); cb = cache_build(list(MEM[pname])); torch.cuda.synchronize(); row['cache_build_s'] = round(time.perf_counter() - tc, 4); cb = None
                tf = time.perf_counter(); r_ = live(MEM[pname], sfx_ids, tg, grad=True, train=True, adapter=True)
                l_ = -r_['lp'].mean(); torch.cuda.synchronize(); row['forward_s'] = round(time.perf_counter() - tf, 3)
                tb = time.perf_counter(); l_.backward(); torch.cuda.synchronize(); row['backward_s'] = round(time.perf_counter() - tb, 3)
                row['prefix_kv_copy_gib_est'] = round(row['prefix_tokens'] * NL * KVH * HD * 2 * 2 / 2**30, 4)
                row.update(peak=gpu_mem(), oom=False, status='OK')
            except torch.cuda.OutOfMemoryError as e:
                row.update(oom=True, status='OOM', error=str(e)[:300])
            except Exception as e:
                row.update(oom=False, status='ERROR', error='%s: %s' % (type(e).__name__, str(e)[:300]))
            finally:
                r_ = l_ = cb = None; opt.zero_grad(set_to_none=True); release(); torch.cuda.synchronize()
                row['row_wall_s'] = round(time.perf_counter() - tw, 3)
                row['allocated_after_cleanup_gib'] = round(torch.cuda.memory_allocated() / 2**30, 3)
                row['clean_after'] = torch.cuda.memory_allocated() <= base_alloc + TOL['p6_clean_slack_mib'] * 2**20
                if not row['clean_after']: p6_stop = 'GPU_STATE_NOT_CLEAN_AFTER_%s_%d' % (pname, Ltot)
            res.append(row); log('P6', json.dumps(row, default=str))
    total = env['gpu_bytes'] / 2**30
    ok_rows = [r_ for r_ in res if r_.get('status') == 'OK']
    first = res[0]
    all_ok = len(ok_rows) == len(res) and p6_stop is None and \
        all(r_['peak']['peak_reserved_gib'] <= TOL['vram_reserved_frac_max'] * total for r_ in ok_rows)
    first_oom_clean = first.get('status') == 'OOM' and first.get('clean_after') is True
    ref = [r_ for r_ in ok_rows if r_['prefix'] == 'LONG_A' and r_['live_tokens'] == LIVE_LENGTHS[-1]]
    opt_s = max(x['optimizer_s'] for x in steps); step_wall = max(x['step_wall_s'] for x in steps)
    upd_30 = int(1800 / (ref[0]['row_wall_s'] + opt_s)) if ref else None
    gate('P6_RESOURCE', 'PASS' if all_ok else ('FAIL' if first_oom_clean else 'INCONCLUSIVE'),
         None if all_ok else ('smallest configuration OOM on a clean GPU state' if first_oom_clean else
                              'OOM / error / unclean GPU state / reserved VRAM above limit in at least one configuration'),
         rows=res, p6_stop=p6_stop, baseline_allocated_gib=round(base_alloc / 2**30, 3), optimizer_step_s_max=opt_s,
         p3_full_step_wall_s_max=step_wall, model_load_s=load_s,
         est_updates_per_30min_LONG_A_256_from_full_row_wall=upd_30,
         budget_note='row wall = cache build + forward + backward + cleanup; plus optimizer step. Evaluation time is NOT '
                     'included and must be reserved separately before any H1 budget',
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
    W1 = {'sentinel': sentinel(), 'weights877': weights_digest877(ENV), 'integrity': integrity_digest(base_params, Q4MODS, BUFS)}
    lora_digest = hashlib.sha256(''.join(kv_digest(p.detach()) for p in LORA_PARAMS).encode()).hexdigest()
    f3 = model.model.layers[CUT].forward
    dc3_restored = getattr(f3, '__func__', None) is type(model.model.layers[CUT]).forward
    p7_ok = (same_objects and W1['sentinel'] == W0['sentinel'] and W1['weights877'] == W0['weights877'] and
             W1['integrity']['sha256'] == W0['integrity']['sha256'] and hooks_clean(hooks_load) and hooks_clean(hooks_install) and
             hooks_clean(hooks_end) and dc3_restored and hst['pass'] and ist['pass'] and rev_ok and
             all(not p.requires_grad for _, p in BASE_ONLY) and src_ok)
    gate('P7_INTEGRITY', 'PASS' if p7_ok else 'FAIL',
         None if p7_ok else 'base SHA-256 (params + NF4 quant state + buffers) / hooks / DirectCut3 restore / selftests / revision / freeze',
         base_param_objects_unchanged=same_objects, hook_selftest=hst, integrity_selftest=ist, model_revision_ok=rev_ok,
         base_checksums_start=W0, base_checksums_end=W1, lora_state_sha256=lora_digest, hooks_after_load=hooks_load,
         hooks_after_install=hooks_install, hooks_end=hooks_end, directcut3_restored=dc3_restored,
         lora_wrapper_calls={'on': LORA_STATE['calls_on'], 'off': LORA_STATE['calls_off']}, adapter_state_file='NOT_WRITTEN')
    R['status'] = 'COMPLETE'
except StopT894 as e:
    R['status'] = 'STOPPED_CRITICAL'; R['stop_reason'] = str(e); log('STOP', str(e))
except Exception as e:
    R['status'] = 'ERROR'; R['error'] = '%s: %s' % (type(e).__name__, e); R['traceback'] = traceback.format_exc()[-20000:]
    log('ERROR', R['error']); log(R['traceback'])
finally:
    G = R['gates']
    crit_fail = [g for g in CRITICAL if G[g]['status'] == 'FAIL'] + [g for g in REQUIRED if G[g]['status'] == 'FAIL' and g != 'P6_RESOURCE']
    not_done = [g for g in CRITICAL + REQUIRED if G[g]['status'] == 'NOT_RUN']
    soft = [g for g in CRITICAL + REQUIRED if G[g]['status'] == 'INCONCLUSIVE'] + (['P6_RESOURCE'] if G['P6_RESOURCE']['status'] == 'FAIL' else [])
    # NOT_FEASIBLE_THIS_CONFIGURATION names THIS implementation / configuration only; it is not an impossibility claim
    if crit_fail: verdict = 'NOT_FEASIBLE_THIS_CONFIGURATION'
    elif R['status'] != 'COMPLETE' or not_done or soft: verdict = 'UNDECIDABLE'
    else: verdict = 'FEASIBLE'
    R['verdict'] = verdict; R['verdict_scope'] = 'this cell, this runtime, this LoRA configuration; not a statement about the architecture'
    R['elapsed_s'] = round(time.perf_counter() - T0, 1)
    try: R['gpu_final'] = gpu_mem()
    except Exception: pass
    log('=' * 112)
    for g in GATE_ORDER: log('%-30s %-13s %s' % (g, G[g]['status'], G[g]['reason'] or ''))
    summary = {'verdict': verdict, 'status': R['status'], 'gates': {g: G[g]['status'] for g in GATE_ORDER},
               'commit': COMMIT, 'model_revision': MODEL_REVISION, 'run_id': RUN_ID, 'elapsed_s': R['elapsed_s'],
               'scope': 'feasibility only; not learning / semantic / native-behaviour / autonomy evidence'}
    log('TEST894_SUMMARY ' + json.dumps(summary, sort_keys=True))
    save()                                                     # last write of the report; it is not modified after this line
    # ------------------------------------------- artifacts (TEST870/889/892 contract: ZIP + SHA256SUMS + receipt + Drive)
    import zipfile
    AG = {'report_written_read_back': False, 'zip_testzip': False, 'sha256sums': False, 'report_in_zip_is_read_back_report': False,
          'drive': 'NOT_RUN'}
    rep_sha = zip_sha = None
    try:
        rb = OUT.read_bytes(); json.loads(rb.decode('utf-8')); rep_sha = sha_bytes(rb); AG['report_written_read_back'] = True
        files = sorted(f_ for f_ in ROOT.rglob('*') if f_.is_file() and not f_.name.endswith('.tmp'))
        sums = ['%s  %s' % (sha_path(f_), f_.relative_to(ROOT).as_posix()) for f_ in files]
        with zipfile.ZipFile(ZIP_PATH, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for f_ in files: z.write(f_, arcname=ROOT.name + '/' + f_.relative_to(ROOT).as_posix())
            z.writestr(ROOT.name + '/SHA256SUMS.txt', '\n'.join(sums) + '\n')
        with zipfile.ZipFile(ZIP_PATH) as z:
            AG['zip_testzip'] = z.testzip() is None
            names = z.namelist(); root_ = ROOT.name
            lines = z.read(root_ + '/SHA256SUMS.txt').decode('utf-8').split('\n')
            rows = [l_.split('  ', 1) for l_ in (lines[:-1] if lines and lines[-1] == '' else lines)]
            hexs = lambda x: len(x) == 64 and all(c in '0123456789abcdef' for c in x)
            okm = bool(rows) and all(len(r_) == 2 and hexs(r_[0]) and r_[1] == r_[1].strip() and '\\' not in r_[1] and
                                     all(seg not in ('', '.', '..') for seg in r_[1].split('/')) for r_ in rows) and \
                len({r_[1] for r_ in rows}) == len(rows)
            listed = {r_[1]: r_[0] for r_ in rows} if okm else {}
            members = [n_[len(root_) + 1:] for n_ in names if not n_.endswith('/')] if all(n_.startswith(root_ + '/') for n_ in names) else None
            AG['sha256sums'] = okm and members is not None and len(members) == len(set(members)) and \
                set(members) - {'SHA256SUMS.txt'} == set(listed) and \
                all(sha_bytes(z.read(root_ + '/' + rel)) == h_ for rel, h_ in listed.items()) and \
                all(k_ in listed for k_ in ('TEST894_results.json', 'TEST894.log'))
            AG['sha256sums_rows'] = len(rows)
            AG['report_in_zip_is_read_back_report'] = listed.get('TEST894_results.json') == rep_sha
        zip_sha = sha_path(ZIP_PATH)
        if DRIVE_DIR is not None:
            try:
                dz = Path(DRIVE_DIR) / ZIP_PATH.name; shutil.copy2(ZIP_PATH, dz); AG['drive'] = sha_path(dz) == zip_sha
            except Exception as e:
                AG['drive'] = False; AG['drive_error'] = '%s: %s' % (type(e).__name__, e)
    except Exception as e:
        AG['artifact_error'] = '%s: %s' % (type(e).__name__, e)
    core = all(AG[k] is True for k in ('report_written_read_back', 'zip_testzip', 'sha256sums', 'report_in_zip_is_read_back_report'))
    AG['cell_identity_match'] = bool((R.get('executed_cell') or {}).get('identity_match'))
    # Fixed, terminating order: (1) final log lines, LOG frozen (console print only afterwards); (2) Drive copies of the
    # final log and report byte-verified; (3) ARTIFACT_STATUS; (4) receipt written, read back byte-for-byte, Drive copy
    # SHA-verified. On a receipt failure the receipt is rewritten ONCE with ARTIFACT_STATUS=FAIL and an unverified Drive
    # receipt copy is removed, so no file claims PASS without verification. The receipt does not contain its own hash.
    log('LOCAL FILES  :', ROOT, '|', ZIP_PATH if ZIP_PATH.exists() else 'ZIP NOT CREATED', '|', RECEIPT_PATH)
    log('DRIVE        :', DRIVE_DIR if DRIVE_DIR is not None else 'DRIVE_NOT_MOUNTED (%s)' % DRIVE_ERR['mount'])
    log('TEST894_LOG_END TECHNICAL_VERDICT=%s | STATUS=%s | ZIP_CORE=%s | CELL_IDENTITY_MATCH=%s | final ARTIFACT_STATUS: '
        'receipt + console' % (verdict, R['status'], core, AG['cell_identity_match']))
    AG['final_log_sha256'] = sha_path(LOG); AG['drive_final_log'] = AG['drive_final_report'] = 'NOT_RUN'
    if DRIVE_DIR is not None:
        for key_, src_ in (('drive_final_log', LOG), ('drive_final_report', OUT)):
            try:
                dst_ = Path(DRIVE_DIR) / src_.name; shutil.copy2(src_, dst_); AG[key_] = dst_.read_bytes() == src_.read_bytes()
            except Exception as e:
                AG[key_] = False; AG[key_ + '_error'] = '%s: %s' % (type(e).__name__, e)
    fails = [k for k in ('report_written_read_back', 'zip_testzip', 'sha256sums', 'report_in_zip_is_read_back_report',
                         'cell_identity_match') if AG[k] is not True]
    if DRIVE_DIR is not None: fails += [k for k in ('drive', 'drive_final_log', 'drive_final_report') if AG[k] is not True]
    ART_STATUS = 'FAIL' if fails else ('PASS' if DRIVE_DIR is not None else 'INCOMPLETE_DRIVE_NOT_MOUNTED')
    receipt = {'test': 'TEST894', 'run_id': RUN_ID, 'technical_verdict': verdict, 'status': R['status'],
               'artifact_gates': AG, 'gates': summary['gates'], 'report': str(OUT),
               'report_sha256': rep_sha, 'zip': str(ZIP_PATH), 'zip_sha256': zip_sha, 'final_log': str(LOG), 'drive_dir': DRIVE_DIR,
               'drive_mount_error': DRIVE_ERR['mount'], 'drive_backup_failures': DRIVE_ERR['backup_failures'],
               'engine_commit': COMMIT, 'model_revision': MODEL_REVISION, 'runtime_pins': R['runtime_pins'],
               'executed_cell': R.get('executed_cell'), 'previous': 'TEST893 FAIL_NO_GAIN (unchanged)',
               'note': 'ARTIFACT_STATUS is separate from the technical verdict; a missing Drive copy is not a LoRA backward failure'}
    def _write_receipt(status_):
        b_ = json.dumps(dict(receipt, ARTIFACT_STATUS=status_, artifact_failures=list(fails)), indent=2, default=str, sort_keys=True).encode()
        tmp_ = RECEIPT_PATH.with_suffix('.json.tmp'); tmp_.write_bytes(b_); tmp_.replace(RECEIPT_PATH)
        rb_ = RECEIPT_PATH.read_bytes()
        return rb_ == b_ and json.loads(rb_.decode('utf-8'))['ARTIFACT_STATUS'] == status_, sha_bytes(b_)
    def _drive_receipt(sha_):
        dr_ = Path(DRIVE_DIR) / RECEIPT_PATH.name; shutil.copy2(RECEIPT_PATH, dr_); return sha_path(dr_) == sha_
    receipt_ok = drive_rc = False; rc_sha = None
    for attempt_ in (1, 2):                                   # at most two writes; the second one can only say FAIL
        try:
            receipt_ok, rc_sha = _write_receipt(ART_STATUS)
            drive_rc = receipt_ok and (DRIVE_DIR is None or _drive_receipt(rc_sha))
        except Exception as e:
            receipt_ok = drive_rc = False; fails.append('receipt_attempt%d: %s: %s' % (attempt_, type(e).__name__, e))
        if receipt_ok and drive_rc: break
        if attempt_ == 1:
            fails.append('receipt_local_read_back' if not receipt_ok else 'receipt_drive_sha256'); ART_STATUS = 'FAIL'
    if DRIVE_DIR is not None and not drive_rc:
        try: os.remove(Path(DRIVE_DIR) / RECEIPT_PATH.name)
        except FileNotFoundError: pass
        except Exception as e: print('RECEIPT_INVALIDATION_FAILED', Path(DRIVE_DIR) / RECEIPT_PATH.name, '%s: %s' % (type(e).__name__, e),
                                     '| this Drive file is NOT a verified receipt; ignore it')
    receipt_state = 'VERIFIED'
    if not receipt_ok:                     # no unverified receipt (e.g. an earlier PASS one) may remain on local disk
        ART_STATUS = 'FAIL'; receipt_state = 'REMOVED_UNVERIFIED'
        for f_ in (RECEIPT_PATH, RECEIPT_PATH.with_suffix('.json.tmp')):
            try:
                if f_.exists(): os.remove(f_)
            except Exception as e:
                receipt_state = 'UNVERIFIED_FILE_COULD_NOT_BE_REMOVED'
                print('RECEIPT_INVALIDATION_FAILED', f_, '%s: %s' % (type(e).__name__, e), '| this file is NOT a verified receipt; ignore it')
    print('TEST894_FINAL TECHNICAL_VERDICT=%s | STATUS=%s | ARTIFACT_STATUS=%s' % (verdict, R['status'], ART_STATUS))
    print('RECEIPT      :', RECEIPT_PATH, 'sha256=%s' % rc_sha, 'local_verified=%s' % receipt_ok,
          'drive_verified=%s' % (drive_rc if DRIVE_DIR is not None else 'DRIVE_NOT_MOUNTED'), 'receipt_state=%s' % receipt_state)
    print('FINAL LOG    :', LOG, 'sha256=%s' % AG['final_log_sha256'], '| ARTIFACT FAILURES:', fails or 'none')
    try:
        from google.colab import files as _cfiles
        for f_ in (ZIP_PATH,) + ((RECEIPT_PATH,) if receipt_ok else ()):
            if f_.exists(): _cfiles.download(str(f_))
        print('Automatic downloads started; the same files are kept under', ROOT.parent, 'and (if mounted) in', DRIVE_DIR)
    except Exception as e:
        print('Automatic download not available (%s); the files are under %s' % (type(e).__name__, ROOT.parent))
    print('=' * 112)
