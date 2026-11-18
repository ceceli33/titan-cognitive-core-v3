# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST896 — SELF-GENERATED EXPERIENCE -> PHYSICAL CUT3 CARTRIDGE -> LATER ACTION
#                                                                                                single Google Colab cell
# Frozen Qwen2.5-72B-Instruct NF4 / BF16, one A100-SXM4-80GB. Continuation of TEST885 / TEST893 / TEST894 / TEST895 on the
# same pinned engine commit and the same physical CUT3/H3/K-V backbone. History is locked and not reinterpreted:
# TEST885 NEGATIVE, TEST893 FAIL_NO_GAIN, TEST894 UNDECIDABLE, TEST895 UNDECIDABLE (P4 RESOLUTION_LIMIT).
#
# QUESTION: does the model's OWN Phase-1 experience (4 free turns, intent written before the delayed outcome, every record a
# physical append-only CUT3 cartridge, persisted to SSD and reloaded) change its later goal-conditioned action in a new
# Phase-2 query content-specifically and counterfactual-sensitively?  Native only: NO LoRA, NO optimizer, NO router, NO
# experience text in the query, NO override / correction of the model's output, NO oracle. The environment executes the
# model's literal action; success is scored offline after all live phases.
# NOT EXECUTED ON GPU BY THE AUTHOR OF THIS CELL. Every number in the report is produced by the run itself.
#
# Inherited unchanged from TEST895 (895.py, commit b71ea0ee, blob c253c30d): bootstrap / version contract, pinned-source
# fetch + blob locks + AST extraction with hook-token refusal, model load through the locked 757 model_setup with the HF
# revision pin, hook inventory, base SHA-256 integrity (params + NF4 quant state + buffers) + self-tests, P0_A forge/rebuild
# parity, P0_B native vs explicit append parity, executed-cell identity against the GitHub git trust root, ZIP + SHA256SUMS +
# read-back + receipt + Drive chain. Engine definitions (AST-selected, hook-free), pinned commit f1007d91:
#   709.py  pairs cache_build replace half rope rephase free_gpu ensure_room kv_digest full_kv_seal sentinel answer
#   730.py  sha release DirectCut3 forge_native initialize_native to_gpu seal_cp
#   757.py  model_setup native_append_direct     877.py api877 xattn877 weights_digest877     878.py xspan878 xappend878
#   873.py  kv873 length873                       test870.py cache_kv870
# 709 answer() (greedy decoding over a mounted memory, the engine's own reader) is the ONLY new engine selection.
# Removed (not part of this question): LoRA wrapper, optimizer, autograd / P2-P5, P4 ladder, P6 backward rows.
# New in TEST896: opaque worlds + offline environment, exact parser, 4-turn experience executor, record chain, derived arm
# cartridges, Phase-2 evaluation, isolated TEXT_CEILING line, D/I/U + coverage, paired statistics, pre-registered decision.
# =====================================================================================================================
import os, sys, subprocess, importlib.util, importlib.metadata, urllib.request, hashlib, ast, json, time, gc, math
import traceback, platform, types, random, shutil
from pathlib import Path
from datetime import datetime, timezone
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')

# ---------------------------------------------------------------------------------------------------------- versions
# Bootstrap record (stdlib only) is created BEFORE the torch check / pip / imports, so a bootstrap failure is recorded.
RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
ROOT = Path(('/content/' if Path('/content').exists() else '/tmp/') + 'TEST896_' + RUN_ID)
ROOT.mkdir(parents=True, exist_ok=True)
LOG = ROOT / 'TEST896.log'; OUT = ROOT / 'TEST896_results.json'; LOG.write_text('')
ZIP_PATH = ROOT.parent / ('TEST896_SONUC_' + RUN_ID + '.zip'); RECEIPT_PATH = ROOT.parent / ('TEST896_SONUC_' + RUN_ID + '_RECEIPT.json')
def _ver(name):
    try: return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError: return None
def _boot_fail(e):
    tb = traceback.format_exc()
    rec = {'test': 'TEST896', 'run_id': RUN_ID, 'status': 'BOOTSTRAP_ERROR', 'error': '%s: %s' % (type(e).__name__, e),
           'traceback': tb, 'installed_versions': {p_: _ver(p_) for p_ in ('torch', 'transformers', 'accelerate', 'bitsandbytes')},
           'technical_verdict': 'NOT_RUN', 'ARTIFACT_STATUS': 'FAIL', 'gpu_model_loaded': False,
           'note': 'stopped before any model / GPU work; Drive not attempted'}
    for path_, txt_ in ((OUT, json.dumps(rec, indent=2)), (RECEIPT_PATH, json.dumps(rec, indent=2))):
        try: tmp_ = Path(str(path_) + '.tmp'); tmp_.write_text(txt_); tmp_.replace(path_)
        except Exception as e2: print('BOOTSTRAP_RECORD_WRITE_FAILED', path_, e2)
    with LOG.open('a') as f_: f_.write('BOOTSTRAP_ERROR %s\n%s\nARTIFACT_STATUS=FAIL\n' % (rec['error'], tb))
    print(tb); print('TEST896 BOOTSTRAP_ERROR recorded in', OUT, LOG, RECEIPT_PATH)
    raise SystemExit('TEST896 BOOTSTRAP_ERROR: ' + rec['error'])
try:
    # Exact runtime contract. torch 2.14.1+cu130 / CUDA 13.0 / transformers 5.22.1 = the combination recorded in 893.log
    # (TABLE GATE0 RUNTIME) under which this engine, incl. api877, ran on the A100. accelerate 1.16.0 / bitsandbytes 0.50.2 =
    # the versions whose sources K3.1 audited (not recorded in 893.log). torch is never installed or changed by this cell.
    TORCH_REQ = '2.14.1+cu130'; CUDA_REQ = '13.0'
    PINS = {'transformers': '5.22.1', 'accelerate': '1.16.0', 'bitsandbytes': '0.50.2'}
    if _ver('torch') != TORCH_REQ:
        raise SystemExit('TEST896_ENV: torch %s found, %s required (893.log runtime); no torch change is made' % (_ver('torch'), TORCH_REQ))
    _need = [p for p, v in PINS.items() if _ver(p) != v]
    if _need:
        _loaded = [p for p in _need if p in sys.modules]
        if _loaded: raise SystemExit('TEST896_ENV: %s already imported with other versions; restart the runtime and rerun' % _loaded)
        _con = Path('/tmp/TEST896_torch_constraint.txt'); _con.write_text('torch==%s\n' % TORCH_REQ)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', '-c', str(_con)] + ['%s==%s' % (p, PINS[p]) for p in _need])
    _got = {p: _ver(p) for p in list(PINS) + ['torch']}
    if any(_got[p] != v for p, v in PINS.items()) or _got['torch'] != TORCH_REQ:
        raise SystemExit('TEST896_ENV: version contract not met after install: %s' % _got)
    import torch, transformers, accelerate, bitsandbytes
    if torch.__version__ != TORCH_REQ or torch.version.cuda != CUDA_REQ or transformers.__version__ != PINS['transformers'] or \
            accelerate.__version__ != PINS['accelerate'] or bitsandbytes.__version__ != PINS['bitsandbytes']:
        raise SystemExit('TEST896_ENV: imported versions differ from the contract: torch %s cuda %s transformers %s accelerate %s '
                         'bitsandbytes %s' % (torch.__version__, torch.version.cuda, transformers.__version__, accelerate.__version__,
                                              bitsandbytes.__version__))
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    from transformers.cache_utils import DynamicCache
except BaseException as _e:
    if isinstance(_e, KeyboardInterrupt): raise
    _boot_fail(_e)

# --------------------------------------------------------------------------------------------------------- constants
TAG = 'TEST896'; MARKER = 'AKBASCORE SILICON HIPPOCAMPUS — TEST896 — SELF-GENERATED EXPERIENCE -> PHYSICAL CUT3 CARTRIDGE -> LATER ACTION'
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
# derived-arm cartridges are physical files too, kept next to ROOT (not zipped: ~0.7 MB each); their SHA-256 + tensor
# seals + parent SHA-256 are in the report and the ZIP. Phase-1 / calibration cartridges are inside ROOT (zipped).
DERIVED_DIR = ROOT.parent / ('TEST896_derived_' + RUN_ID); DERIVED_DIR.mkdir(exist_ok=True)
EVENTS = ROOT / 'TEST896_events.jsonl'; EVENTS.write_text('')
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
# History locks (read-only cross-checks; these records are never modified or reinterpreted)
HISTORY = {'894sinirag.py': ('011073e83cf81524f6992718831373897add5979', '10dca846a5115619c21c71d8679f8c5e35e8b6b4', ()),
           '894.log': ('58bcab13a0a89d4326a7a5b40c184d53a144ad3f', '3aff8f3304bbe8ed08a55fb6adf188b126280203',
                       ('20261118T031507Z', 'TECHNICAL_VERDICT=UNDECIDABLE | STATUS=COMPLETE | ARTIFACT_STATUS=PASS', 'GATE P4_NUMERICAL INCONCLUSIVE')),
           '895.py': ('b71ea0ee1d8ea6b467afff20c3dac4957903d397', 'c253c30d1ac0f6350e4d9d784a4918f4f6db53fd', ()),
           '895.log': ('dd53d4b81c85c023872214cb8b49e49a3b695a6b', 'a0e8169b896e5afc984d0a4ed24ab74d551e0da2',
                       ('20261118T051416Z', 'TEST895_FINAL TECHNICAL_VERDICT=UNDECIDABLE | STATUS=COMPLETE | ARTIFACT_STATUS=PASS',
                        'GATE P4_NUMERICAL INCONCLUSIVE | central-difference ladder v2 | T2_under_A:RESOLUTION_LIMIT, T1_under_B:RESOLUTION_LIMIT'))}
SELECT = {'709.py': ('pairs', 'cache_build', 'replace', 'half', 'rope', 'rephase', 'free_gpu', 'ensure_room', 'kv_digest',
                     'full_kv_seal', 'sentinel', 'answer'),
          '730.py': ('sha', 'release', 'DirectCut3', 'forge_native', 'initialize_native', 'to_gpu', 'seal_cp'),
          '757.py': ('model_setup', 'native_append_direct'),
          '877.py': ('api877', 'xattn877', 'weights_digest877'),
          '878.py': ('xspan878', 'xappend878'),
          '873.py': ('kv873', 'length873'),
          'test870.py': ('cache_kv870',)}
FORBIDDEN_TOKENS = ('register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook',
                    'register_backward_hook', 'register_full_backward_pre_hook', 'register_module_forward_hook',
                    'register_module_forward_pre_hook', 'register_hook(')
# Pre-registered technical tolerances (inherited) and TEST896 protocol / decision thresholds (fixed before any GPU number).
TOL = {'parity_close_rel': 1e-2, 'P_expected': 30, 'chunk_expected': 128}
TOL896 = {
    'n_main': 32, 'n_cal': 4, 'phase1_turns': 4, 'world_seed': SEED + 896, 'arm_order_seed': SEED + 897,
    'max_new_tokens': 12,                       # greedy budget of the locked 709 answer(); names are a few tokens
    'wall_budget_s': 4 * 3600,                  # checked at world boundaries -> TECHNICAL_INCOMPLETE (no partial verdict)
    'primary_delta_min': 0.25,                  # PASS: Delta_TP >= 0.25 and Newcombe paired 95% lower > 0
    'min_D': 16, 'min_K2': 16,                  # coverage (K3.1 report 3)
    'exploration_fail_K0_frac': 0.5,            # more than half of the worlds with K = 0 -> FAIL_EXPLORATION
    'placebo_invalid_margin_worlds': 2,         # non-VALID(PLACEBO_P) <= max(non-VALID(NONE), non-VALID(TRUE)) + 2
    'placebo_success_min_frac_of_none': 2.0 / 3.0,   # success(PLACEBO_P) >= 2/3 success(NONE)
    'cf_rate_min': 0.75, 'cf_wilson_lo_min': 0.5,    # CF mechanism PASS
    'cf_fail_wilson_hi_max': 0.75,              # CF mechanism FAIL: n >= 16 and Wilson 95% upper < 0.75
    'readout_adequate_frac': 0.75, 'readout_inadequate_frac': 0.25,   # single-transition probes (K = 2 worlds)
    'text_ceiling_min': 0.75, 'text_min_supported': 8}                # TEXT_CEILING sensitivity for FAIL claims
MAX_NEW = TOL896['max_new_tokens']               # global read by the locked 709 answer()
CRITICAL = ('ENV', 'SOURCE', 'EXTRACT', 'MODEL', 'WORLD_MANIFEST', 'PHASE1_EXPERIENCE', 'PHASE2_EVALUATION', 'P1_PHYSICAL',
            'P7_INTEGRITY')
REQUIRED = ('P0_A_FORGE_REBUILD_PARITY', 'P0_B_EXPLICIT_APPEND_PARITY', 'LIVE_REPEATABILITY', 'REBUILD_FROM_SSD_PARITY',
            'ARM_GEOMETRY')
GATE_ORDER = ('ENV', 'SOURCE', 'EXTRACT', 'MODEL', 'WORLD_MANIFEST', 'P0_A_FORGE_REBUILD_PARITY', 'P0_B_EXPLICIT_APPEND_PARITY',
              'LIVE_REPEATABILITY', 'CALIBRATION', 'PHASE1_EXPERIENCE', 'PHASE2_EVALUATION', 'REBUILD_FROM_SSD_PARITY',
              'ARM_GEOMETRY', 'TEXT_CEILING', 'P1_PHYSICAL', 'P7_INTEGRITY')

R = {'test': 'TEST896', 'stage': 'native self-generated experience -> physical cartridge -> later action', 'run_id': RUN_ID,
     'commit': COMMIT, 'status': 'STARTED', 'checks': [],
     'gates': {g: {'status': 'NOT_RUN', 'reason': None, 'data': {}} for g in GATE_ORDER},
     'history': {'TEST885': 'NEGATIVE (action effect without task success)', 'TEST893': 'FAIL_NO_GAIN',
                 'TEST894': 'UNDECIDABLE (technical bridge)', 'TEST895': 'UNDECIDABLE (P4 RESOLUTION_LIMIT)',
                 'note': 'locked; not modified, not reinterpreted; LoRA / P4 are not part of TEST896'},
     'model_revision': MODEL_REVISION, 'runtime_pins': dict(PINS, torch=TORCH_REQ, cuda=CUDA_REQ),
     'scope': 'native, LoRA-OFF, no training; one sealed 32-world cohort + 4 calibration worlds (not in the statistics)',
     'executed_by_author': False, 'tolerances': TOL, 'protocol': TOL896,
     'tolerances_sha256': hashlib.sha256(json.dumps({'TOL': TOL, 'TOL896': TOL896}, sort_keys=True).encode()).hexdigest()}
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
            for f_ in (LOG, OUT, EVENTS): shutil.copy2(f_, Path(DRIVE_DIR) / f_.name)
        except Exception as e:
            DRIVE_ERR['backup_failures'] += 1; DRIVE_ERR['last'] = '%s: %s' % (type(e).__name__, e)
def check(name, ok, detail=None):
    # same signature/semantics as the 730/757 check() used by the extracted engine definitions
    R['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail}); save()
    log('PASS' if ok else 'FAIL', name, '' if detail is None else json.dumps(detail, default=str)[:600])
    if not ok: raise RuntimeError('CHECK_FAILED:' + name)
class StopT896(Exception): pass
def gate(name, status, reason=None, **data):
    assert status in ('PASS', 'FAIL', 'INCONCLUSIVE', 'DIAGNOSTIC'), status
    R['gates'][name] = {'status': status, 'reason': reason, 'data': data}; save()
    log('GATE', name, status, '' if reason is None else '| ' + str(reason))
    if status == 'FAIL' and name in CRITICAL: raise StopT896(name + ': ' + str(reason))
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
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'AKBASCORE-TEST896'}), timeout=120) as f:
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
# ------------------------------------------------------------------------------------- no-grad mount context (no LoRA)
class MountOff:
    """Every forge / mount / append / reference prefill runs inside this (TEST895 name kept; there is no adapter in TEST896,
    so it is exactly torch.no_grad)."""
    def __enter__(self): self.ng = torch.no_grad(); self.ng.__enter__(); return self
    def __exit__(self, *e): self.ng.__exit__(*e); return False
def ev(kind, **data):
    # append-only event ledger (JSONL); every line is flushed and fsync'ed before the run continues
    line = json.dumps(dict(seq=EVSEQ[0], t_s=round(time.perf_counter() - T0, 3), kind=kind, **data), default=str, sort_keys=True)
    EVSEQ[0] += 1
    with EVENTS.open('a') as f:
        f.write(line + '\n'); f.flush(); os.fsync(f.fileno())
EVSEQ = [0]
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
def live(mem, ctx_ids, tgt_ids):
    """TEST895 live() without the adapter: teacher-forced readout over a FRESH cache built from the mounted K/V (or no
    prefix if mem is None). Target j is predicted by the hidden state at len(ctx)-1+j. Diagnostic NLL only."""
    n0 = 0 if mem is None else int(mem[0][0].shape[-2])
    ids = list(ctx_ids) + list(tgt_ids); L = len(ids); pidx = [len(ctx_ids) - 1 + j for j in range(len(tgt_ids))]
    assert len(tgt_ids) >= 1 and pidx[0] >= 0
    cache = DynamicCache() if mem is None else cache_build(list(mem))
    pos = torch.arange(n0, n0 + L, device=DEV)
    with torch.no_grad():
        out = model.model(input_ids=torch.tensor([ids], device=DEV), past_key_values=cache,
                          attention_mask=torch.ones((1, n0 + L), device=DEV, dtype=torch.long),
                          position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
        hs = out.last_hidden_state[0, pidx, :]
        logits = model.lm_head(hs).float(); lsm = torch.log_softmax(logits, dim=-1)
        lp = lsm.gather(1, torch.tensor(tgt_ids, device=DEV).unsqueeze(1)).squeeze(1)
    res = {'lp': [float(x) for x in lp], 'logits': logits.detach().cpu(), 'n0': n0, 'L': L, 'cache_len': int(cache.get_seq_length())}
    del out, hs, cache, lsm, lp
    return res

# ================================================================ TEST896 pure logic (no torch; CPU-tested by AST extraction)
# Everything in this block is plain Python: world generation, records, derived-arm cartridges, information content (D/I/U),
# parser, paired statistics and the pre-registered decision function. GPU code only calls these functions.
CODE_ALPH896 = 'BCDFGHJKLMNPQRSTVWXZ'          # consonants only: opaque names, no English words
# Markers. PRIMARY markers are fixed (OUTCOME_PENDING approved for PLACEBO_P; ACTION_UNRECORDED for A-C+/A-C-); their token
# lengths define the name lengths. The two SECONDARY markers (invalid action / no outcome) take the first candidate, in this
# pre-registered order, whose token length equals the corresponding primary length (fail-closed if none does), so that every
# field of every record has the same token length in every world and every arm (OTHER_WORLD geometry included).
PRIMARY_MARKERS896 = {'outcome_pending': 'OUTCOME_PENDING', 'action_unrecorded': 'ACTION_UNRECORDED'}
SECONDARY_CANDIDATES896 = {
    'action_invalid': ('ACTION_INVALID', 'INVALID_ACTION', 'NO_VALID_ACTION', 'INVALID', 'ACTION_NOT_VALID', 'NO_ACTION',
                       'INVALID_ACTION_OUTPUT', 'ACTION_WAS_INVALID', 'NO_VALID_ACTION_GIVEN', 'ACTION_OUTPUT_INVALID',
                       'NOT_A_VALID_ACTION', 'INVALID_ACTION_GIVEN', 'NO_VALID_ACTION_WAS_GIVEN'),
    'outcome_none': ('OUTCOME_NONE', 'NO_OUTCOME', 'NO_OUTCOME_PRODUCED', 'NONE_PRODUCED', 'OUTCOME_NOT_PRODUCED', 'NO_RESULT',
                     'NO_OUTCOME_OCCURRED', 'NOTHING_HAPPENED', 'NO_OUTCOME_WAS_PRODUCED', 'OUTCOME_ABSENT', 'NO_EFFECT',
                     'NO_OUTCOME_AT_ALL', 'OUTCOME_DID_NOT_OCCUR')}
RECORD_TPL896 = {'intent': ('Turn {t}: I chose action ', '.\n'), 'outcome': ('Turn {t}: the outcome was ', '.\n')}
AXIOMS896 = ('Available actions: {x}, {y}. Possible outcomes: {p}, {q}. Each action always produces the same outcome, and the '
             'two actions produce different outcomes. The INFORMATION above is your own memory of earlier turns in this '
             'environment (it may be empty).')
EXPLORE896 = 'Try to learn the outcome of each action.'          # B2, identical in every world and every Phase-1 condition
Q1_TAIL896 = ' Which action do you take now? Reply with only the action name.'
Q2_GOAL896 = ' Goal: obtain the outcome {g}.'
PROBE896 = ('According to the INFORMATION above, which outcome followed the action {x}? Reply with only the outcome name.')
MAIN_ARMS896 = ('NONE', 'TRUE', 'PLACEBO_P', 'PLACEBO_OFFALPHA', 'DELETED', 'OTHER_WORLD', 'A+C-', 'A-C+', 'A-C-')
# 'CF' is not a separate cartridge: it is the A+C- cartridge (identical bytes) scored under pi_CF = sigma o pi.
EQUAL_GEOMETRY_ARMS896 = ('PLACEBO_P', 'PLACEBO_OFFALPHA', 'OTHER_WORLD', 'A+C-', 'A-C+', 'A-C-')

def choose_markers896(ntok):
    out = dict(PRIMARY_MARKERS896)
    for sec, prim in (('action_invalid', 'action_unrecorded'), ('outcome_none', 'outcome_pending')):
        m = [c for c in SECONDARY_CANDIDATES896[sec] if ntok(c) == ntok(out[prim])]
        if not m: raise RuntimeError('MARKER_GEOMETRY_NOT_FOUND %s (needs %d tokens)' % (sec, ntok(out[prim])))
        out[sec] = m[0]
    out['action_ntok'] = ntok(out['action_unrecorded']); out['outcome_ntok'] = ntok(out['outcome_pending'])
    return out

def _code896(rng, ntok, n_target, used, tries=200000):
    for _ in range(tries):
        s = ''.join(rng.choice(CODE_ALPH896) for _ in range(rng.randint(3, 24)))
        if ntok(s) != n_target or s in used: continue
        if any(s in u or u in s for u in used): continue          # no name contains another (parser / leak safety)
        used.add(s); return s
    raise RuntimeError('NAME_GEOMETRY_NOT_FOUND n=%d' % n_target)

def make_worlds896(seed, n_main, n_cal, ntok, markers):
    # Every random draw is made here, before the model produces anything. pub = what the model may see; vault = the
    # offline environment / evaluator only (pi, goal, offalpha relabel). The goal is revealed only in the Phase-2 query.
    import random as _r
    rng = _r.Random(seed); used = set(markers[k] for k in ('action_unrecorded', 'action_invalid', 'outcome_pending', 'outcome_none'))
    worlds = []
    for i in range(n_main + n_cal):
        wid = ('W%02d' % i) if i < n_main else ('C%02d' % (i - n_main))
        a = [_code896(rng, ntok, markers['action_ntok'], used) for _ in range(2)]
        o = [_code896(rng, ntok, markers['outcome_ntok'], used) for _ in range(2)]
        x = [_code896(rng, ntok, markers['outcome_ntok'], used) for _ in range(2)]
        swap = rng.random() < 0.5
        pi = {a[0]: o[1], a[1]: o[0]} if swap else {a[0]: o[0], a[1]: o[1]}
        goal = rng.choice(o)
        act_order = a[:]; rng.shuffle(act_order); out_order = o[:]; rng.shuffle(out_order)
        off = {o[0]: x[1], o[1]: x[0]} if rng.random() < 0.5 else {o[0]: x[0], o[1]: x[1]}   # independent of pi
        worlds.append({'wid': wid, 'calibration': i >= n_main,
                       'pub': {'actions': act_order, 'outcomes': out_order},
                       'vault': {'pi': pi, 'goal': goal, 'offalpha': off}})
    perm = list(range(n_main)); rng.shuffle(perm)
    partner = {perm[j]: perm[(j + 1) % n_main] for j in range(n_main)}          # cyclic: a derangement for n_main >= 2
    for i in range(n_main): worlds[i]['other_world'] = worlds[partner[i]]['wid']
    return worlds

def sigma896(pub, o):       # outcome swap within the world alphabet
    p, q = pub['outcomes']; return q if o == p else (p if o == q else o)

def q_phase1_896(pub):
    x, y = pub['actions']; p, q = pub['outcomes']
    return AXIOMS896.format(x=x, y=y, p=p, q=q) + ' ' + EXPLORE896 + Q1_TAIL896

def q_phase2_896(pub, goal):
    x, y = pub['actions']; p, q = pub['outcomes']
    return AXIOMS896.format(x=x, y=y, p=p, q=q) + Q2_GOAL896.format(g=goal) + Q1_TAIL896

def q_probe896(pub, action):     # diagnostic single-transition readout; same public axioms as Phase 1 / Phase 2
    x, y = pub['actions']; p, q = pub['outcomes']
    return AXIOMS896.format(x=x, y=y, p=p, q=q) + ' ' + PROBE896.format(x=action)

def segments896(rec):
    head, tail = RECORD_TPL896[rec['kind']]
    return (head.format(t=rec['turn']), rec['field'], tail)

def record_ids896(rec, tok_ids):    # per-segment tokenization: geometry is controlled by the field token length alone
    out = []
    for s in segments896(rec): out += list(tok_ids(s))
    return out

def geometry896(records, tok_ids): return [[len(tok_ids(s)) for s in segments896(r)] for r in records]

def parse896(text, allowed):
    # exact, pre-registered: strip whitespace, ONE pair of surrounding quotes/backticks/asterisks, ONE trailing period
    s = (text or '').strip()
    for q in ('**', '`', '"', "'"):
        if len(s) >= 2 * len(q) and s.startswith(q) and s.endswith(q): s = s[len(q):-len(q)].strip(); break
    if s.endswith('.'): s = s[:-1].strip()
    if s in allowed: return 'VALID', s
    if s.upper().startswith('UNKNOWN'): return 'ABSTAIN', None
    return 'INVALID', None

def phase1_world896(pub, env_step, decide, on_record, markers, turns):
    # the model's own free trajectory: decide(query) -> raw text; the intent record is written BEFORE the environment acts;
    # the outcome is written afterwards as a separate record. Invalid output is never corrected.
    q = q_phase1_896(pub); records = []; log_ = []
    for t in range(1, turns + 1):
        raw = decide(q); cat, act = parse896(raw, pub['actions'])
        rec_i = {'turn': t, 'kind': 'intent', 'field': act if cat == 'VALID' else markers['action_invalid']}
        on_record(rec_i); records.append(rec_i)
        o = env_step(act) if cat == 'VALID' else markers['outcome_none']
        rec_o = {'turn': t, 'kind': 'outcome', 'field': o}
        on_record(rec_o); records.append(rec_o)
        log_.append({'turn': t, 'raw': raw, 'category': cat, 'action': act, 'outcome': o})
    return records, log_

def prepared_records896(pub, pi):
    # calibration only (not in the cohort): actions in presentation order x, y, x, y with their true outcomes
    recs = []
    for t, a in enumerate([pub['actions'][0], pub['actions'][1]] * 2, 1):
        recs += [{'turn': t, 'kind': 'intent', 'field': a}, {'turn': t, 'kind': 'outcome', 'field': pi[a]}]
    return recs

def derive_arm896(arm, records, pub, markers, offalpha=None, other_records=None):
    # returns NEW record dicts (originals are never modified) with 'src' = index of the source record and 'changed'
    acts, outs = set(pub['actions']), set(pub['outcomes'])
    if arm == 'NONE': return []
    if arm == 'OTHER_WORLD': return [dict(r, src=('OTHER', i), changed=False) for i, r in enumerate(other_records)]
    res = []
    for i, r in enumerate(records):
        f = r['field']; valid_o = r['kind'] == 'outcome' and f in outs; valid_a = r['kind'] == 'intent' and f in acts
        nf = f
        if arm == 'TRUE': pass
        elif arm == 'PLACEBO_P':
            if valid_o: nf = markers['outcome_pending']
        elif arm == 'PLACEBO_OFFALPHA':
            if valid_o: nf = offalpha[f]
        elif arm == 'DELETED':
            if valid_o: continue
        elif arm in ('A+C-', 'A-C-'):
            if valid_o: nf = sigma896(pub, f)
            if arm == 'A-C-' and valid_a: nf = markers['action_unrecorded']
        elif arm == 'A-C+':
            if valid_a: nf = markers['action_unrecorded']
        else: raise ValueError(arm)
        res.append({'turn': r['turn'], 'kind': r['kind'], 'field': nf, 'src': i, 'changed': nf != f})
    return res

def experience896(records, pub):
    # E = set of (action, outcome) transitions present in these records (both fields valid world names, same turn)
    acts, outs = set(pub['actions']), set(pub['outcomes'])
    it = {r['turn']: r['field'] for r in records if r['kind'] == 'intent' and r['field'] in acts}
    oc = {r['turn']: r['field'] for r in records if r['kind'] == 'outcome' and r['field'] in outs}
    return sorted({(it[t], oc[t]) for t in it if t in oc})

def info_label896(E, goal, mapping, pub):
    # D = the correct transition is in E; I = not in E but forced by E under the public bijection axiom; U = otherwise
    a_star = [a for a, o in mapping.items() if o == goal][0]
    if (a_star, goal) in E: return 'D'
    if E:
        a, o = E[0]; other_a = [x for x in pub['actions'] if x != a][0]
        implied = {a: o, other_a: sigma896(pub, o)}
        if implied.get(a_star) == goal: return 'I'
    return 'U'

def coverage896(E): return len({a for a, _ in E})

def score896(category, action, mapping, goal): return int(category == 'VALID' and mapping.get(action) == goal)

# ------------------------------------------------------------------------------------------- paired statistics
Z95_896 = 1.959963984540054
def wilson896(k, n, z=Z95_896):
    if n == 0: return (0.0, 1.0)
    p = k / n; den = 1 + z * z / n; c = (p + z * z / (2 * n)) / den
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / den
    return (max(0.0, c - h), min(1.0, c + h))

def newcombe_paired896(y1, y2, z=Z95_896):
    # Newcombe (1998) method 10: paired difference p1 - p2 from Wilson score limits of each margin + phi correlation
    assert len(y1) == len(y2) and len(y1) > 0
    n = len(y1); a = sum(1 for u, v in zip(y1, y2) if u and v); b = sum(1 for u, v in zip(y1, y2) if u and not v)
    c = sum(1 for u, v in zip(y1, y2) if v and not u); d = n - a - b - c
    p1, p2 = (a + b) / n, (a + c) / n; l1, u1 = wilson896(a + b, n, z); l2, u2 = wilson896(a + c, n, z)
    den = ((a + b) * (c + d) * (a + c) * (b + d)) ** 0.5
    phi = (a * d - b * c) / den if den > 0 else 0.0
    dl = ((p1 - l1) ** 2 - 2 * phi * (p1 - l1) * (u2 - p2) + (u2 - p2) ** 2)
    du = ((u1 - p1) ** 2 - 2 * phi * (u1 - p1) * (p2 - l2) + (p2 - l2) ** 2)
    th = p1 - p2
    return {'n': n, 'a': a, 'b': b, 'c': c, 'd': d, 'p1': p1, 'p2': p2, 'diff': th, 'phi': phi,
            'lo': max(-1.0, th - max(dl, 0.0) ** 0.5), 'hi': min(1.0, th + max(du, 0.0) ** 0.5)}

def mcnemar_exact896(b, c):
    import math as _m
    n = b + c
    if n == 0: return 1.0
    k = min(b, c); cdf = sum(_m.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * cdf)

# ------------------------------------------------------------------------------------------- decision (pre-registered)
def rate896(xs): return (sum(xs) / len(xs)) if xs else 0.0

def decide896(tech, W, T):
    """tech: 'PASS' | 'FAIL' | 'INCONCLUSIVE' (technical + physical gates). W: list of main-world dicts with
    K, label (D/I/U), Y{arm}, cat{arm}, readable (K=2 worlds: all four single-transition probes correct), text_label, text_Y.
    T: thresholds. Priority (frozen): 1 technical / artefact, 2 exploration / coverage, 3 primary TRUE - PLACEBO_P,
    4 content + counterfactual mechanism. Returns dict with VERDICT, SUBCODES and every number used."""
    out = {'stage_reached': 0, 'subcodes': []}
    n = len(W)
    if tech != 'PASS':
        out.update(VERDICT='TECHNICAL_INVALID' if tech == 'FAIL' else 'TECHNICAL_INCONCLUSIVE', stage_reached=1); return out
    out['stage_reached'] = 2
    nK = {k: sum(1 for w in W if w['K'] == k) for k in (0, 1, 2)}; nL = {l: sum(1 for w in W if w['label'] == l) for l in 'DIU'}
    out['coverage'] = {'n_worlds': n, 'K0': nK[0], 'K1': nK[1], 'K2': nK[2], 'D': nL['D'], 'I': nL['I'], 'U': nL['U']}
    Y = lambda arm, ws=W: [w['Y'][arm] for w in ws]
    bad = lambda arm: sum(1 for w in W if w['cat'][arm] != 'VALID')
    rates = {arm: rate896(Y(arm)) for arm in W[0]['Y']} if W else {}
    out['rates'] = rates; out['non_valid_counts'] = {arm: bad(arm) for arm in W[0]['cat']} if W else {}
    prim = newcombe_paired896(Y('TRUE'), Y('PLACEBO_P')); prim['mcnemar_exact_p'] = mcnemar_exact896(prim['b'], prim['c'])
    out['primary'] = prim
    out['subset_delta'] = {l: (rate896(Y('TRUE', [w for w in W if w['label'] == l])) - rate896(Y('PLACEBO_P', [w for w in W if w['label'] == l])),
                               sum(1 for w in W if w['label'] == l)) for l in 'DIU'}
    sup = [w for w in W if w.get('text_label') in ('D', 'I')]
    out['text_ceiling'] = {'n_supported': len(sup), 'success_rate': rate896([w['text_Y'] for w in sup]),
                           'adequate': len(sup) >= T['text_min_supported'] and rate896([w['text_Y'] for w in sup]) >= T['text_ceiling_min']}
    pv_inv = bad('PLACEBO_P') <= max(bad('NONE'), bad('TRUE')) + T['placebo_invalid_margin_worlds']
    pv_rate = rates['PLACEBO_P'] >= T['placebo_success_min_frac_of_none'] * rates['NONE']
    out['placebo_validity'] = {'invalid_rule_ok': pv_inv, 'success_rule_ok': pv_rate}
    # ---- 2 exploration / coverage
    if nK[0] > T['exploration_fail_K0_frac'] * n:
        out.update(VERDICT='FAIL_EXPLORATION', subcodes=['NO_VALID_EXPERIENCE_K0']); return out
    cov = []
    if nK[2] < T['min_K2']: cov.append('K1_INSUFFICIENT_COUNTERFACTUAL_COVERAGE' if nK[1] >= nK[0] else 'K0_INSUFFICIENT_COVERAGE')
    if nL['D'] < T['min_D']: cov.append('D_BELOW_MIN')
    if cov: out.update(VERDICT='INCONCLUSIVE_COVERAGE', subcodes=cov); return out
    # ---- 3 primary
    out['stage_reached'] = 3
    if not (pv_inv and pv_rate):
        out.update(VERDICT='INCONCLUSIVE_PLACEBO_VALIDITY', subcodes=[k for k, v in out['placebo_validity'].items() if not v]); return out
    if not (prim['diff'] >= T['primary_delta_min'] and prim['lo'] > 0):
        if prim['hi'] < T['primary_delta_min']:
            if not out['text_ceiling']['adequate']:
                out.update(VERDICT='INCONCLUSIVE_SENSITIVITY', subcodes=['TEXT_CEILING_NOT_ADEQUATE']); return out
            ci = (rates['TRUE'] - rates['NONE'] >= T['primary_delta_min'] and
                  (rates['PLACEBO_P'] - rates['NONE'] >= T['primary_delta_min'] or rates['OTHER_WORLD'] - rates['NONE'] >= T['primary_delta_min']))
            out.update(VERDICT='FAIL_CONTENT_INDEPENDENT' if ci else 'FAIL_NO_MEANINGFUL_GAIN'); return out
        out.update(VERDICT='INCONCLUSIVE_PRIMARY', subcodes=['CI_INCLUDES_0_OR_EFFECT_BELOW_MIN']); return out
    # ---- 4 mechanism
    out['stage_reached'] = 4
    E = [w for w in W if w['K'] == 2]
    S = [int(w['Y']['TRUE'] == 1 and w['Y']['CF'] == 1) for w in E]
    lo, hi = wilson896(sum(S), len(S)); rd = rate896([int(bool(w.get('readable'))) for w in E])
    out['cf'] = {'n': len(S), 'k': sum(S), 'rate': rate896(S), 'wilson_lo': lo, 'wilson_hi': hi, 'readable_fraction': rd}
    if len(S) < T['min_K2']: out.update(VERDICT='INCONCLUSIVE_MECHANISM', subcodes=['CF_N_BELOW_MIN']); return out
    if not (rate896(S) >= T['cf_rate_min'] and lo > T['cf_wilson_lo_min']):
        if hi < T['cf_fail_wilson_hi_max']:
            if rd >= T['readout_adequate_frac']: out.update(VERDICT='FAIL_MEMORY_UPDATE_USE'); return out
            if rd <= T['readout_inadequate_frac']: out.update(VERDICT='FAIL_ENCODING_READOUT'); return out
            out.update(VERDICT='INCONCLUSIVE_MECHANISM', subcodes=['READOUT_PARTIAL']); return out
        out.update(VERDICT='INCONCLUSIVE_MECHANISM', subcodes=['CF_CI_WIDE']); return out
    if not rates['TRUE'] > rates['A-C+']: out.update(VERDICT='FAIL_OUTCOME_ONLY'); return out
    pat = {'TRUE>NONE': rates['TRUE'] > rates['NONE'], 'TRUE>OTHER_WORLD': rates['TRUE'] > rates['OTHER_WORLD'],
           'A+C+>A+C-': rates['TRUE'] > rates['A+C-'], 'A+C+>A-C+': rates['TRUE'] > rates['A-C+']}
    out['secondary_pattern'] = pat
    if not all(pat.values()): out.update(VERDICT='INCONCLUSIVE_SECONDARY_PATTERN', subcodes=[k for k, v in pat.items() if not v]); return out
    dD, nD = out['subset_delta']['D']; dI, nI = out['subset_delta']['I']
    lab = 'DIRECT_EXPERIENCE_SUPPORTED' if nD and dD >= T['primary_delta_min'] else (
        'INFERENCE_MEDIATED_EXPERIENCE' if nI and dI >= T['primary_delta_min'] else 'BENEFIT_NOT_LOCALIZED_TO_D_OR_I')
    out.update(VERDICT='PASS', subcodes=[lab]); return out

# ======================================================================================================== RUN
try:
    log('=' * 112); log(MARKER, RUN_ID, '| engine commit', COMMIT, '| continuation of TEST893 (FAIL_NO_GAIN, unchanged)')
    log('SCOPE: feasibility only. PASS != learning / semantic reading / native behaviour / autonomy.'); log('=' * 112)
    log('TOLERANCES', json.dumps(TOL, sort_keys=True), 'sha256', R['tolerances_sha256'])
    # executed-cell identity, single cell. Trust root = the git objects of the repository, not this cell: the commit that
    # main points to and the blob id its tree records for 896.py (both hashed by git over the committed bytes; git
    # verifies the objects it fetches). The file is also fetched as raw bytes at that commit (second channel) and must be
    # byte-identical. The executed cell (IPython history) must equal the committed bytes after ONE canonicalization only:
    # leading and trailing '\n' characters are removed from both sides (run 20261118T014044Z: the pasted cell = one extra
    # leading newline + no final newline, otherwise byte-identical). Nothing inside the text is changed. The cell never derives an expected hash from its
    # own text; commit + blob + SHA-256 are recorded for comparison with the externally announced audited identity.
    SRC_REPO = 'ceceli33/titan-cognitive-core-v3'; SRC_FILE = '896.py'
    ec = {'status': 'NOT_CAPTURED', 'identity_match': False}
    try:
        _hist = list(globals()['get_ipython']().history_manager.input_hist_raw)
        _cell = [x for x in _hist if MARKER in x and 'def integrity_selftest' in x][-1]
        (ROOT / 'TEST896_cell_source.py').write_text(_cell, encoding='utf-8'); _cb = _cell.encode('utf-8')
        ec.update(status='CAPTURED', sha256=sha_bytes(_cb), git_blob=gitblob(_cb), git_blob_with_final_newline=gitblob(_cb + b'\n'),
                  lines=_cell.count('\n') + 1, file=str(ROOT / 'TEST896_cell_source.py'))
    except Exception as e:
        ec['capture_error'] = '%s: %s' % (type(e).__name__, e)
    try:
        _gd = ROOT.parent / ('TEST896_srcid_' + RUN_ID); _genv = dict(os.environ, GIT_TERMINAL_PROMPT='0')
        _git = lambda *a: subprocess.run(['git'] + list(a), check=True, capture_output=True, timeout=180, env=_genv).stdout
        _git('clone', '-q', '--depth', '1', '--filter=blob:none', '--no-checkout', 'https://github.com/' + SRC_REPO, str(_gd))
        _c = _git('-C', str(_gd), 'rev-parse', 'HEAD').decode().strip()
        _b = _git('-C', str(_gd), 'rev-parse', 'HEAD:' + SRC_FILE).decode().strip()
        _pb = _git('-C', str(_gd), 'cat-file', 'blob', _b)
        with urllib.request.urlopen(urllib.request.Request('https://raw.githubusercontent.com/%s/%s/%s' % (SRC_REPO, _c, SRC_FILE),
                                                           headers={'User-Agent': 'AKBASCORE-TEST896'}), timeout=120) as f_:
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
        _gdrive.mount('/content/drive'); DRIVE_DIR = '/content/drive/MyDrive/TEST896_' + RUN_ID; os.makedirs(DRIVE_DIR, exist_ok=True)
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
    hist = {}
    for fn_, (cm_, bl_, must_) in HISTORY.items():
        with urllib.request.urlopen(urllib.request.Request('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/%s/%s' % (cm_, fn_),
                                                           headers={'User-Agent': 'AKBASCORE-TEST896'}), timeout=120) as f_:
            b_ = f_.read(2_000_001)
        t_ = b_.decode('utf-8', 'replace')
        hist[fn_] = {'commit': cm_, 'lock': bl_, 'actual': gitblob(b_), 'match': gitblob(b_) == bl_,
                     'history_ok': all(m_ in t_ for m_ in must_)}
    hist_ok = all(v['match'] and v['history_ok'] for v in hist.values())
    src_ok = hist_ok and all(x['match'] for x in lock.values()) and all(x['match'] for x in k31.values()) and \
        g1d.get('P') == TOL['P_expected'] and g1d.get('chunk') == TOL['chunk_expected'] and fin_ok
    gate('SOURCE', 'PASS' if src_ok else 'FAIL', None if src_ok else 'blob lock / K3.1 blob / 893.log G1 / TEST893_FINAL / TEST894-895 history lock cross-check failed',
         locks=lock, k31_blob_check=k31, log893_G1={'P': g1d.get('P'), 'chunk': g1d.get('chunk'), 'gpu_wall_s': g1d.get('wall_s')},
         test893_final_line=fin893[0][:200] if fin893 else None, history_locks=hist)
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
    # transformers 5.22.1 leaves config._commit_hash empty (TEST896 run 20261118T014044Z: null). Revision evidence is therefore:
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
    # ======================================================================================== TEST896 experiment
    def budget(where):
        if time.perf_counter() - T0 > TOL896['wall_budget_s']: raise StopT896('TIME_BUDGET exceeded at ' + where)
    def tok_ids(s): return list(tok(s, add_special_tokens=False).input_ids)
    def ntok(s): return len(tok_ids(s))
    # ------------------------------------------------------------------------ WORLD MANIFEST (sealed before Phase 1)
    MARKERS = choose_markers896(ntok)
    WORLDS = make_worlds896(TOL896['world_seed'], TOL896['n_main'], TOL896['n_cal'], ntok, MARKERS)
    BYID = {w['wid']: w for w in WORLDS}; MAIN = [w for w in WORLDS if not w['calibration']]; CAL = [w for w in WORLDS if w['calibration']]
    names = [n for w in WORLDS for n in w['pub']['actions'] + w['pub']['outcomes'] + list(w['vault']['offalpha'].values())]
    mk_names = [MARKERS[k] for k in ('action_unrecorded', 'action_invalid', 'outcome_pending', 'outcome_none')]
    q_all = [q_phase1_896(w['pub']) for w in WORLDS] + [q_phase2_896(w['pub'], w['vault']['goal']) for w in WORLDS] + \
        [q_probe896(w['pub'], a) for w in WORLDS for a in w['pub']['actions']]
    wm = {'names_unique': len(names) == len(set(names)) == 6 * len(WORLDS),
          'no_name_contains_another': not any(a != b and a in b for a in names + mk_names for b in names + mk_names),
          'action_lengths': all(ntok(a) == MARKERS['action_ntok'] for w in WORLDS for a in w['pub']['actions']),
          'outcome_lengths': all(ntok(o) == MARKERS['outcome_ntok'] for w in WORLDS for o in w['pub']['outcomes'] + list(w['vault']['offalpha'].values())),
          'marker_lengths': ntok(MARKERS['action_invalid']) == MARKERS['action_ntok'] and ntok(MARKERS['outcome_none']) == MARKERS['outcome_ntok'],
          'names_decode_roundtrip': all(tok.decode(tok_ids(n)) == n for n in names + mk_names),
          'record_heads_constant': all(len({len(tok_ids(RECORD_TPL896[k][0].format(t=t))) for t in range(1, TOL896['phase1_turns'] + 1)}) == 1
                                       for k in RECORD_TPL896),
          'other_world_derangement': sorted(w['other_world'] for w in MAIN) == sorted(w['wid'] for w in MAIN) and all(w['other_world'] != w['wid'] for w in MAIN),
          'phase1_queries_no_goal_word': all('Goal' not in q_phase1_896(w['pub']) for w in WORLDS),
          'queries_no_relabel_names': not any(x in q for w in WORLDS for x in w['vault']['offalpha'].values() for q in q_all),
          'queries_no_record_text': not any(('Turn ' in q) or ('I chose action' in q) or ('the outcome was' in q) for q in q_all),
          'explore_sentence_B2': EXPLORE896 == 'Try to learn the outcome of each action.' and all(EXPLORE896 in q_phase1_896(w['pub']) for w in WORLDS)}
    MANIFEST = {'seed': TOL896['world_seed'], 'markers': MARKERS, 'worlds': WORLDS, 'record_templates': RECORD_TPL896,
                'axioms': AXIOMS896, 'explore': EXPLORE896, 'q1_tail': Q1_TAIL896, 'q2_goal': Q2_GOAL896, 'probe': PROBE896,
                'arms': MAIN_ARMS896, 'equal_geometry_arms': EQUAL_GEOMETRY_ARMS896, 'protocol': TOL896,
                'note': 'pub = what the model may see in a query; vault = offline environment / evaluator only'}
    MANIFEST_PATH = ROOT / 'TEST896_world_manifest_SEALED.json'
    _mb = json.dumps(MANIFEST, sort_keys=True, indent=1).encode(); MANIFEST_PATH.write_bytes(_mb); MANIFEST_SHA = sha_bytes(_mb)
    R['world_manifest'] = {'file': str(MANIFEST_PATH), 'sha256': MANIFEST_SHA, 'markers': MARKERS,
                           'public': {w['wid']: w['pub'] for w in WORLDS}}   # the vault itself is reported only after Phase 2
    ev('WORLD_MANIFEST_SEALED', sha256=MANIFEST_SHA, n_worlds=len(WORLDS))
    gate('WORLD_MANIFEST', 'PASS' if all(wm.values()) else 'FAIL', None if all(wm.values()) else 'failed: ' + ', '.join(k for k, v in wm.items() if not v),
         checks=wm, sha256=MANIFEST_SHA, markers=MARKERS)
    # ------------------------------------------------------------------------------ physical record cartridges
    CART_INDEX = []
    def forge_record(ids, cid, parent_sha, role, where):
        with MountOff(): cp, secs = forge_native(list(ids), 'T896_' + RUN_ID + '_' + cid)
        path = where / ('T896_' + cid + '.pt'); tmp = Path(str(path) + '.tmp')
        if path.exists(): raise StopT896('APPEND_ONLY_VIOLATION ' + str(path))
        torch.save(cp, tmp); tmp.replace(path)
        ent = {'cid': cid, 'file': str(path), 'sha256': sha_path(path), 'tensor_seal': seal_cp(cp), 'n': cp['n'],
               'body_tokens': cp['body_tokens'], 'parent_sha256': parent_sha, 'role': role, 'forge_s': secs,
               'ids_sha256': sha_bytes(json.dumps(list(ids)).encode())}
        CART_INDEX.append(ent); ev('CARTRIDGE', **{k: v for k, v in ent.items() if k != 'tensor_seal'})
        return cp, ent
    def load_record(ent):
        # SSD reload: file SHA-256 and tensor seal must equal the values recorded when the cartridge was written
        if sha_path(ent['file']) != ent['sha256']: raise StopT896('CARTRIDGE_FILE_SHA_CHANGED ' + ent['cid'])
        cp = torch.load(ent['file'], map_location='cpu', weights_only=True)
        if seal_cp(cp) != ent['tensor_seal']: raise StopT896('CARTRIDGE_TENSOR_SEAL_CHANGED ' + ent['cid'])
        return cp
    with MountOff(): CP_EMPTY, _s = forge_native([], 'T896_' + RUN_ID + '_EMPTY')
    _pe = CART_DIR / 'T896_EMPTY.pt'; torch.save(CP_EMPTY, _pe)
    EMPTY_ENT = {'cid': 'EMPTY', 'file': str(_pe), 'sha256': sha_path(_pe), 'tensor_seal': seal_cp(CP_EMPTY), 'n': CP_EMPTY['n'], 'role': 'empty'}
    CART_INDEX.append(EMPTY_ENT)
    def mount_from(cps):
        # the SAME procedure for every arm: EMPTY (P-token prefix) mount + locked native append of each record in order
        with MountOff():
            mem = list(initialize_native(to_gpu(CP_EMPTY)))
            for cp in cps: mem = list(native_append_direct(list(mem), to_gpu(cp), strict_sha=True))
        return mem
    def gen(mem, q):
        # the locked 709 answer(): greedy, MAX_NEW tokens, stops at EOS / <|im_end|>; the mount must be unchanged by the query
        s0 = full_kv_seal(mem)
        with torch.no_grad(): out_ = answer(mem, q)
        if full_kv_seal(mem) != s0: raise StopT896('MOUNT_CHANGED_BY_QUERY')
        return out_
    def text_mem(ids):
        # TEXT_CEILING only: plain full-text prefill (the TEST895 P0_A reference loop); no forge, no cartridge, no append
        with MountOff():
            cache = None
            for st in range(0, len(ids), CHUNK):
                piece = ids[st:st + CHUNK]; ensure_room(len(piece) + 512); pos = torch.arange(st, st + len(piece), device=DEV)
                out = model(input_ids=torch.tensor([piece], device=DEV), past_key_values=cache,
                            attention_mask=torch.ones((1, st + len(piece)), device=DEV, dtype=torch.long),
                            position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
                cache = out.past_key_values; del out
            m_ = [(k.detach().clone(), v.detach().clone()) for k, v in pairs(cache)]; del cache
        return m_
    def nll_actions(mem, pub, q):
        sfx = tok_ids(SUFFIX_HEAD + q + SUFFIX_TAIL)
        return {a: sum(live(mem, sfx, tok_ids(a))['lp']) for a in pub['actions']}
    # ----------------------------------------------------------------- P0 on calibration records (inherited checks)
    C0 = CAL[0]; PREP = {w['wid']: prepared_records896(w['pub'], w['vault']['pi']) for w in CAL}
    body0 = [i for r in PREP[C0['wid']] for i in record_ids896(r, tok_ids)]
    with MountOff(): CP_P0, _ = forge_native(body0, 'T896_' + RUN_ID + '_P0A')
    with MountOff():
        MEM_P0 = list(initialize_native(to_gpu(CP_P0)))
        ids_A = list(PIDS) + body0; cache = None
        for st in range(0, len(ids_A), CHUNK):                    # reference = forge_native's own loop, keeping the cache
            piece = ids_A[st:st + CHUNK]; ensure_room(len(piece) + 512); pos = torch.arange(st, st + len(piece), device=DEV)
            out = model(input_ids=torch.tensor([piece], device=DEV), past_key_values=cache,
                        attention_mask=torch.ones((1, st + len(piece)), device=DEV, dtype=torch.long),
                        position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
            cache = out.past_key_values; del out
        REF_A = [(k.detach().clone(), v.detach().clone()) for k, v in pairs(cache)]; del cache
    lower_cmp = kv_compare(REF_A[:CUT + 1], [(k.to(DEV), v.to(DEV)) for k, v in CP_P0['lower']])
    upper_cmp = kv_compare(REF_A[CUT + 1:], MEM_P0[CUT + 1:])
    st_a = 'PASS' if tri(lower_cmp) == tri(upper_cmp) == 'PASS' else ('FAIL' if 'FAIL' in (tri(lower_cmp), tri(upper_cmp)) else 'INCONCLUSIVE')
    gate('P0_A_FORGE_REBUILD_PARITY', st_a, 'full-text prefill K/V vs forged lower K/V + H3-injected native upper rebuild',
         lower_L0_3=lower_cmp, upper_L4_79=upper_cmp, body_tokens=len(body0)); del REF_A, MEM_P0
    if st_a == 'FAIL': raise StopT896('P0_A native parity FAIL')
    r0 = [i for i in record_ids896(PREP[C0['wid']][0], tok_ids)]; r1 = [i for i in record_ids896(PREP[C0['wid']][1], tok_ids)]
    with MountOff(): cpA, _ = forge_native(r0, 'T896_' + RUN_ID + '_P0B_A'); cpB, _ = forge_native(r1, 'T896_' + RUN_ID + '_P0B_B')
    with MountOff(): memA = list(initialize_native(to_gpu(cpA)))
    if api_err is None:
        with MountOff():
            nat = list(native_append_direct(list(memA), to_gpu(cpB), strict_sha=True))
            exp = list(xappend878(ENV, list(memA), to_gpu(cpB), ()))
        cmp_b = kv_compare(nat, exp); st_b = tri(cmp_b)
        gate('P0_B_EXPLICIT_APPEND_PARITY', st_b, 'locked native append (757) vs explicit no-hook append (878/877)', compare=cmp_b)
        del nat, exp
        if st_b == 'FAIL': raise StopT896('P0_B native parity FAIL')
    else:
        gate('P0_B_EXPLICIT_APPEND_PARITY', 'INCONCLUSIVE', 'api877 installed-source audit failed: ' + api_err)
    del memA, cpA, cpB, CP_P0; release()
    # ---------------------------------------------------------------- live repeatability of the decision path
    _m = mount_from([]); _q = q_phase1_896(C0['pub'])
    g1_, g2_ = gen(_m, _q), gen(_m, _q); sfx_ = tok_ids(SUFFIX_HEAD + _q + SUFFIX_TAIL); a_ = tok_ids(C0['pub']['actions'][0])
    l1_, l2_ = live(_m, sfx_, a_), live(_m, sfx_, a_)
    rep_ok = g1_ == g2_ and torch.equal(l1_['logits'], l2_['logits'])
    gate('LIVE_REPEATABILITY', 'PASS' if rep_ok else 'INCONCLUSIVE', 'same mount + same query twice: greedy text and teacher-forced logits',
         greedy_equal=g1_ == g2_, logits_equal=torch.equal(l1_['logits'], l2_['logits']), example_output=g1_)
    del _m, l1_, l2_; release()
    # ---------------------------------------------------------------- CALIBRATION (prepared K = 2 records; NOT in the cohort)
    CALR = {}
    for w in CAL:
        budget('calibration ' + w['wid']); pub = w['pub']; prev = None; cps = []; cents = []
        for k, r in enumerate(PREP[w['wid']]):
            cp, ent = forge_record(record_ids896(r, tok_ids), '%s_CAL_%02d_%s_t%d' % (w['wid'], k, r['kind'], r['turn']), prev, 'calibration', CART_DIR)
            cps.append(cp); cents.append(ent); prev = ent['sha256']
        res = {}
        for arm in ('NONE', 'TRUE', 'PLACEBO_P', 'A+C-'):
            ar = derive_arm896(arm, PREP[w['wid']], pub, MARKERS, w['vault']['offalpha'], None)
            acps = [cps[r['src']] if not r['changed'] else forge_record(record_ids896(r, tok_ids), '%s_CAL_%s_%02d' % (w['wid'], arm.replace('+', 'p').replace('-', 'm'), r['src']),
                    cents[r['src']]['sha256'], 'calibration_' + arm, DERIVED_DIR)[0] for r in ar]
            mem = mount_from(acps); raw = gen(mem, q_phase2_896(pub, w['vault']['goal']))
            probes = {a: gen(mem, q_probe896(pub, a)) for a in pub['actions']} if arm in ('TRUE', 'A+C-') else None
            res[arm] = {'raw': raw, 'parsed': parse896(raw, pub['actions']), 'probes': probes}; del mem, acps; release()
        tm = text_mem(list(PIDS) + [i for r in PREP[w['wid']] for i in record_ids896(r, tok_ids)])
        res['TEXT'] = {'raw': gen(tm, q_phase2_896(pub, w['vault']['goal']))}; res['TEXT']['parsed'] = parse896(res['TEXT']['raw'], pub['actions'])
        del tm, cps; release()
        CALR[w['wid']] = res; ev('CALIBRATION_WORLD', wid=w['wid'], result=res)
    gate('CALIBRATION', 'DIAGNOSTIC', 'prepared complete K = 2 records (both actions, true outcomes); smoke + readout diagnostic; NOT in the cohort',
         results=CALR)
    # ---------------------------------------------------------------- PHASE 1: the model's own 4 free turns per world
    P1 = {}; P1_MEM_CPU = {}
    for w in MAIN:
        budget('phase1 ' + w['wid']); wid = w['wid']; pub = w['pub']
        st = {'mem': mount_from([]), 'ents': [], 'prev': None}
        def on_record(rec, st=st, wid=wid):
            k = len(st['ents'])
            cp, ent = forge_record(record_ids896(rec, tok_ids), '%s_P1_%02d_%s_t%d' % (wid, k, rec['kind'], rec['turn']), st['prev'], 'phase1', CART_DIR)
            with MountOff(): st['mem'] = list(native_append_direct(list(st['mem']), to_gpu(cp), strict_sha=True))
            st['ents'].append(ent); st['prev'] = ent['sha256']; ev('RECORD_APPENDED', wid=wid, k=k, rec=rec, sha256=ent['sha256'])
        def env_step(a, w=w): return w['vault']['pi'][a]        # the environment executes the model's literal action
        recs, lg = phase1_world896(pub, env_step, lambda q, st=st: gen(st['mem'], q), on_record, MARKERS, TOL896['phase1_turns'])
        E_ = experience896(recs, pub)
        P1[wid] = {'records': recs, 'turns': lg, 'ents': st['ents'], 'K': coverage896(E_), 'E': E_,
                   'final_mount_tokens': int(st['mem'][0][0].shape[-2]), 'final_seal': full_kv_seal(st['mem'])}
        P1_MEM_CPU[wid] = [(k.cpu(), v.cpu()) for k, v in st['mem']]
        ev('PHASE1_WORLD', wid=wid, turns=lg, K=P1[wid]['K'], chain=[e['sha256'] for e in st['ents']])
        log('PHASE1', wid, 'K', P1[wid]['K'], 'turns', json.dumps([[t_['category'], t_['action'], t_['outcome']] for t_ in lg]))
        del st['mem']; release(); save()
    chain_ok = all(len(P1[w['wid']]['records']) == 2 * TOL896['phase1_turns'] and
                   all(P1[w['wid']]['ents'][i]['parent_sha256'] == (P1[w['wid']]['ents'][i - 1]['sha256'] if i else None) for i in range(len(P1[w['wid']]['ents'])))
                   for w in MAIN)
    R['phase1'] = {wid: {k: v for k, v in d.items() if k not in ('final_seal',)} for wid, d in P1.items()}
    gate('PHASE1_EXPERIENCE', 'PASS' if chain_ok else 'FAIL', None if chain_ok else 'record chain / parent hash / record count',
         K_distribution={k: sum(1 for d in P1.values() if d['K'] == k) for k in (0, 1, 2)},
         non_valid_turns=sum(1 for d in P1.values() for t_ in d['turns'] if t_['category'] != 'VALID'))
    # ---------------------------------------------------------------- PHASE 2: one goal-conditioned decision per arm
    P2 = {}; rng_arm = random.Random(TOL896['arm_order_seed']); geo_bad = []; rebuild = {}
    for w in MAIN:
        budget('phase2 ' + w['wid']); wid = w['wid']; pub = w['pub']; ow = w['other_world']
        true_cps = [load_record(e) for e in P1[wid]['ents']]                   # SSD reload of the world's own experience
        geo_true = geometry896(P1[wid]['records'], tok_ids); q2 = q_phase2_896(pub, w['vault']['goal'])
        arms = list(MAIN_ARMS896); rng_arm.shuffle(arms); P2[wid] = {'arm_order': arms}
        for arm in arms:
            ar = derive_arm896(arm, P1[wid]['records'], pub, MARKERS, w['vault']['offalpha'], P1[ow]['records'])
            geo = geometry896(ar, tok_ids)
            if arm in EQUAL_GEOMETRY_ARMS896 and geo != geo_true: geo_bad.append([wid, arm])
            cps = []; dents = []
            for r in ar:
                if arm == 'OTHER_WORLD': cps.append(load_record(P1[ow]['ents'][r['src'][1]]))
                elif not r['changed']: cps.append(true_cps[r['src']])
                else:
                    cp, ent = forge_record(record_ids896(r, tok_ids), '%s_%s_%02d_%s_t%d' % (wid, arm.replace('+', 'p').replace('-', 'm'), r['src'], r['kind'], r['turn']),
                                           P1[wid]['ents'][r['src']]['sha256'], 'derived_' + arm, DERIVED_DIR)
                    cps.append(cp); dents.append(ent['sha256'])
            mem = mount_from(cps); n_tok = int(mem[0][0].shape[-2])
            if arm == 'TRUE':
                ref_ = [(k.to(DEV), v.to(DEV)) for k, v in P1_MEM_CPU[wid]]
                rebuild[wid] = {'seal_equal': full_kv_seal(mem) == P1[wid]['final_seal']}
                if not rebuild[wid]['seal_equal']: rebuild[wid]['compare'] = kv_compare(ref_, mem)
                del ref_
            raw = gen(mem, q2); cat, act = parse896(raw, pub['actions'])
            rec = {'raw': raw, 'category': cat, 'action': act, 'mount_tokens': n_tok, 'geometry_equal_true': geo == geo_true,
                   'records': ar, 'derived_cartridges': dents, 'nll_action': nll_actions(mem, pub, q2)}
            if arm in ('TRUE', 'A+C-') and P1[wid]['K'] == 2:
                rec['probes'] = {a: gen(mem, q_probe896(pub, a)) for a in pub['actions']}
            P2[wid][arm] = rec; ev('PHASE2_DECISION', wid=wid, arm=arm, raw=raw, category=cat, action=act, mount_tokens=n_tok)
            del mem, cps; release()
        del true_cps; release()
        log('PHASE2', wid, json.dumps({a: P2[wid][a]['category'] + ':' + str(P2[wid][a]['action']) for a in MAIN_ARMS896}))
        save()
    R['phase2'] = P2
    gate('PHASE2_EVALUATION', 'PASS' if all(set(MAIN_ARMS896) <= set(P2[w['wid']]) for w in MAIN) else 'FAIL', 'every arm evaluated in every world',
         worlds=len(P2))
    rb_ok = all(v['seal_equal'] for v in rebuild.values()) and len(rebuild) == len(MAIN)
    rb_close = all(v['seal_equal'] or tri(v['compare']) == 'INCONCLUSIVE' for v in rebuild.values())
    gate('REBUILD_FROM_SSD_PARITY', 'PASS' if rb_ok else ('INCONCLUSIVE' if rb_close else 'FAIL'),
         'TRUE mount rebuilt from the SSD files == the live Phase-1 mount (bitwise K/V seals, 80 layers)', worlds=rebuild)
    len_ok = all(P2[w['wid']][a]['mount_tokens'] == P2[w['wid']]['TRUE']['mount_tokens'] for w in MAIN for a in EQUAL_GEOMETRY_ARMS896)
    gate('ARM_GEOMETRY', 'PASS' if not geo_bad and len_ok else 'FAIL', 'equal token count and positions per record field for the equal-geometry arms',
         mismatches=geo_bad, mount_lengths_equal=len_ok,
         deleted_vs_placebo_p='DELETED and PLACEBO_P carry the same (zero) outcome information and the same intents; DELETED is shorter')
    del P1_MEM_CPU
    # ---------------------------------------------------------------- TEXT_CEILING: isolated own trajectory, text in context
    TXT = {}
    for w in MAIN:
        budget('text ' + w['wid']); pub = w['pub']; ts = {'ids': list(PIDS)}
        def on_text(rec, ts=ts): ts['ids'] += record_ids896(rec, tok_ids)
        def dec_text(q, ts=ts):
            m_ = text_mem(ts['ids']); o_ = gen(m_, q); del m_; release(); return o_
        trecs, tlg = phase1_world896(pub, lambda a, w=w: w['vault']['pi'][a], dec_text, on_text, MARKERS, TOL896['phase1_turns'])
        raw = dec_text(q_phase2_896(pub, w['vault']['goal'])); cat, act = parse896(raw, pub['actions'])
        TXT[w['wid']] = {'records': trecs, 'turns': tlg, 'raw': raw, 'category': cat, 'action': act}
        ev('TEXT_CEILING_WORLD', wid=w['wid'], turns=tlg, raw=raw, category=cat, action=act)
    R['text_ceiling'] = TXT
    gate('TEXT_CEILING', 'DIAGNOSTIC', 'isolated: own text trajectory + text-in-context decision; never mounted, never in a native arm',
         K_distribution={k: sum(1 for wid_, d in TXT.items() if coverage896(experience896(d['records'], BYID[wid_]['pub'])) == k) for k in (0, 1, 2)})
    # ---------------------------------------------------------------- OFFLINE EVALUATION (after every live phase)
    WREC = []
    for w in MAIN:
        wid = w['wid']; pub = w['pub']; V = w['vault']; picf = {a: sigma896(pub, o) for a, o in V['pi'].items()}
        E_ = P1[wid]['E']; K_ = P1[wid]['K']
        Y = {arm: score896(P2[wid][arm]['category'], P2[wid][arm]['action'], V['pi'], V['goal']) for arm in MAIN_ARMS896}
        Y['CF'] = score896(P2[wid]['A+C-']['category'], P2[wid]['A+C-']['action'], picf, V['goal'])
        cat = {arm: P2[wid][arm]['category'] for arm in MAIN_ARMS896}; cat['CF'] = cat['A+C-']
        readable = None
        if K_ == 2:
            pt = P2[wid]['TRUE']['probes']; pc = P2[wid]['A+C-']['probes']
            readable = all(parse896(pt[a], pub['outcomes'])[1] == V['pi'][a] for a in pub['actions']) and \
                all(parse896(pc[a], pub['outcomes'])[1] == picf[a] for a in pub['actions'])
        tE = experience896(TXT[wid]['records'], pub)
        WREC.append({'wid': wid, 'K': K_, 'label': info_label896(E_, V['goal'], V['pi'], pub),
                     'label_cf': info_label896(experience896(derive_arm896('A+C-', P1[wid]['records'], pub, MARKERS), pub), V['goal'], picf, pub),
                     'Y': Y, 'cat': cat, 'readable': readable, 'text_K': coverage896(tE),
                     'text_label': info_label896(tE, V['goal'], V['pi'], pub),
                     'text_Y': score896(TXT[wid]['category'], TXT[wid]['action'], V['pi'], V['goal']),
                     'nll_margin_true_minus_other': {arm: P2[wid][arm]['nll_action'][[a for a, o in V['pi'].items() if o == V['goal']][0]] -
                                                     P2[wid][arm]['nll_action'][[a for a, o in V['pi'].items() if o != V['goal']][0]] for arm in MAIN_ARMS896}})
    R['offline'] = {'worlds': WREC, 'vault': {w['wid']: w['vault'] for w in WORLDS}, 'calibration_scored': {
        wid: {arm: score896(v[arm]['parsed'][0], v[arm]['parsed'][1], BYID[wid]['vault']['pi'] if arm != 'A+C-' else
              {a: sigma896(BYID[wid]['pub'], o) for a, o in BYID[wid]['vault']['pi'].items()}, BYID[wid]['vault']['goal'])
              for arm in v} for wid, v in CALR.items()}}
    R['cartridges'] = CART_INDEX
    ev('OFFLINE_EVALUATION_DONE', n=len(WREC))
    # ---------------------------------------------------------------------------------------- P1 / P7 final
    files_end = {e['cid']: sha_path(e['file']) == e['sha256'] for e in CART_INDEX}
    empty_end = seal_cp(CP_EMPTY) == EMPTY_ENT['tensor_seal']
    p1_ok = all(files_end.values()) and empty_end and len(files_end) == len(CART_INDEX)
    gate('P1_PHYSICAL', 'PASS' if p1_ok else 'FAIL', None if p1_ok else 'a cartridge file SHA-256 changed after it was written',
         cartridge_files=len(CART_INDEX), files_unchanged=sum(files_end.values()), changed=[k for k, v in files_end.items() if not v],
         empty_tensor_seal_unchanged=empty_end, phase1_and_calibration_dir=str(CART_DIR), derived_dir=str(DERIVED_DIR))
    hooks_end = hook_inventory()
    W1 = {'sentinel': sentinel(), 'weights877': weights_digest877(ENV), 'integrity': integrity_digest(base_params, Q4MODS, BUFS)}
    same_objects = {id(p) for _, p in base_params} == {id(p) for _, p in model.named_parameters()}
    lora_absent = not any('lora' in n.lower() for n, _ in model.named_parameters()) and \
        not any('lora' in type(m).__name__.lower() or 'peft' in type(m).__module__.lower() for m in model.modules())
    f3 = model.model.layers[CUT].forward
    dc3_restored = getattr(f3, '__func__', None) is type(model.model.layers[CUT]).forward
    p7_ok = (same_objects and W1['sentinel'] == W0['sentinel'] and W1['weights877'] == W0['weights877'] and
             W1['integrity']['sha256'] == W0['integrity']['sha256'] and hooks_clean(hooks_load) and hooks_clean(hooks_end) and
             dc3_restored and hst['pass'] and ist['pass'] and rev_ok and lora_absent and
             all(not p.requires_grad for _, p in model.named_parameters()) and src_ok)
    gate('P7_INTEGRITY', 'PASS' if p7_ok else 'FAIL',
         None if p7_ok else 'base SHA-256 (params + NF4 quant state + buffers) / hooks / DirectCut3 restore / selftests / revision / LoRA-OFF / freeze',
         base_param_objects_unchanged=same_objects, hook_selftest=hst, integrity_selftest=ist, model_revision_ok=rev_ok,
         base_checksums_start=W0, base_checksums_end=W1, hooks_after_load=hooks_load, hooks_end=hooks_end,
         directcut3_restored=dc3_restored, lora_absent=lora_absent)
    # ---------------------------------------------------------------- pre-registered decision (priority 1 -> 4)
    G_ = R['gates']
    tech = 'FAIL' if any(G_[g]['status'] == 'FAIL' for g in CRITICAL + REQUIRED) else (
        'PASS' if all(G_[g]['status'] == 'PASS' for g in CRITICAL + REQUIRED) else 'INCONCLUSIVE')
    DEC = decide896(tech, WREC, TOL896)
    R['decision'] = DEC; R['technical_status'] = tech
    log('DECISION', json.dumps({k: DEC.get(k) for k in ('VERDICT', 'subcodes', 'stage_reached', 'coverage', 'primary', 'placebo_validity',
                                                       'text_ceiling', 'cf', 'secondary_pattern', 'subset_delta', 'rates')}, default=str))
    R['status'] = 'COMPLETE'
except StopT896 as e:
    R['status'] = 'STOPPED_CRITICAL'; R['stop_reason'] = str(e); log('STOP', str(e))
except Exception as e:
    R['status'] = 'ERROR'; R['error'] = '%s: %s' % (type(e).__name__, e); R['traceback'] = traceback.format_exc()[-20000:]
    log('ERROR', R['error']); log(R['traceback'])
finally:
    G = R['gates']
    sci = (R.get('decision') or {}).get('VERDICT')
    if R['status'] != 'COMPLETE' or sci is None:
        sci = 'TECHNICAL_INCOMPLETE' if 'TIME_BUDGET' in str(R.get('stop_reason', '')) else 'TECHNICAL_INVALID'
    verdict = sci
    R['verdict'] = verdict; R['verdict_scope'] = 'this cell, this runtime, this 32-world cohort; native LoRA-OFF; not autonomy'
    R['elapsed_s'] = round(time.perf_counter() - T0, 1)
    try: R['gpu_final'] = gpu_mem()
    except Exception: pass
    log('=' * 112)
    for g in GATE_ORDER: log('%-30s %-13s %s' % (g, G[g]['status'], G[g]['reason'] or ''))
    summary = {'verdict': verdict, 'subcodes': (R.get('decision') or {}).get('subcodes'), 'status': R['status'],
               'technical_status': R.get('technical_status'), 'gates': {g: G[g]['status'] for g in GATE_ORDER},
               'commit': COMMIT, 'model_revision': MODEL_REVISION, 'run_id': RUN_ID, 'elapsed_s': R['elapsed_s'],
               'scope': 'native self-generated experience benefit; not autonomy, not LoRA, not routing'}
    log('TEST896_SUMMARY ' + json.dumps(summary, sort_keys=True, default=str))
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
                all(k_ in listed for k_ in ('TEST896_results.json', 'TEST896.log', 'TEST896_events.jsonl', 'TEST896_world_manifest_SEALED.json'))
            AG['sha256sums_rows'] = len(rows)
            AG['report_in_zip_is_read_back_report'] = listed.get('TEST896_results.json') == rep_sha
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
    log('TEST896_LOG_END SCIENTIFIC_VERDICT=%s | STATUS=%s | ZIP_CORE=%s | CELL_IDENTITY_MATCH=%s | final ARTIFACT_STATUS: '
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
    # priority 1 (technical AND artefact integrity): a verdict whose artefacts are not verified is not a reportable verdict
    FINAL = verdict if ART_STATUS == 'PASS' else 'TECHNICAL_INCONCLUSIVE_ARTIFACT'
    receipt = {'test': 'TEST896', 'run_id': RUN_ID, 'scientific_verdict': verdict, 'final_verdict': FINAL,
               'subcodes': summary.get('subcodes'), 'technical_status': R.get('technical_status'), 'status': R['status'],
               'artifact_gates': AG, 'gates': summary['gates'], 'report': str(OUT),
               'report_sha256': rep_sha, 'zip': str(ZIP_PATH), 'zip_sha256': zip_sha, 'final_log': str(LOG), 'drive_dir': DRIVE_DIR,
               'drive_mount_error': DRIVE_ERR['mount'], 'drive_backup_failures': DRIVE_ERR['backup_failures'],
               'engine_commit': COMMIT, 'model_revision': MODEL_REVISION, 'runtime_pins': R['runtime_pins'],
               'executed_cell': R.get('executed_cell'), 'previous': R['history'], 'world_manifest_sha256': (R.get('world_manifest') or {}).get('sha256'),
               'derived_cartridge_dir': str(DERIVED_DIR),
               'note': 'final_verdict = scientific_verdict only when ARTIFACT_STATUS = PASS (decision priority 1)'}
    def _write_receipt(status_):
        b_ = json.dumps(dict(receipt, ARTIFACT_STATUS=status_, final_verdict=(verdict if status_ == 'PASS' else 'TECHNICAL_INCONCLUSIVE_ARTIFACT'), artifact_failures=list(fails)), indent=2, default=str, sort_keys=True).encode()
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
    FINAL = verdict if ART_STATUS == 'PASS' else 'TECHNICAL_INCONCLUSIVE_ARTIFACT'
    print('TEST896_FINAL FINAL_VERDICT=%s | SCIENTIFIC_VERDICT=%s | SUBCODES=%s | TECHNICAL_STATUS=%s | STATUS=%s | ARTIFACT_STATUS=%s' % (
        FINAL, verdict, summary.get('subcodes'), R.get('technical_status'), R['status'], ART_STATUS))
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
