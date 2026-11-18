# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — NPDM SMOKE — NATIVE PROSPECTIVE DISCREPANCY MEMORY (causal smoke, not TEST897)
#                                                                                                single Google Colab cell
# Frozen Qwen2.5-72B-Instruct NF4 / BF16, one A100-SXM4-80GB, the physical CUT3/H3/K-V SSD cartridge engine of TEST896
# (896.py commit 9454b3db, blob 00b4a6da, SHA-256 badfea0a...0980), pinned engine commit f1007d91. History is locked and
# not reinterpreted: TEST885 NEGATIVE, TEST893 FAIL_NO_GAIN, TEST894 / TEST895 UNDECIDABLE, TEST896 PASS in its log
# (DIRECT_EXPERIENCE_SUPPORTED; guided 4-turn exploration, NOT autonomous; its ZIP / receipt are UNVERIFIED in the repo).
#
# QUESTION (smoke only): when the model writes ITS OWN pre-outcome prediction as a separate native cartridge (before the
# environment acts) and the real outcome arrives later as another cartridge, does that prediction record causally change
# the NEXT native ACT / ACQUIRE / STOP decision, content-specifically and in the direction the observed outcome requires?
# The decision is ALWAYS the model's own greedy tokens (locked 709 answer()); the harness only parses, executes, records.
# NO LoRA / optimizer / training, NO hooks, NO RAG, NO oracle routing, NO answer override, NO external VOI / entropy
# controller, NO outcome text in the query. Prediction records ARE text-derived K/V (model-generated prediction K/V
# replay); the actual outcome is never replayed into the query as text.
# NOT EXECUTED ON GPU BY THE AUTHOR OF THIS CELL. Every number in the report is produced by the run itself.
#
# Inherited unchanged from TEST896: bootstrap / version contract, pinned-source fetch + blob locks + AST extraction with
# hook-token refusal, locked model load with HF revision pin, hook inventory, base SHA-256 integrity + self-tests, P0_A
# forge/rebuild parity, P0_B native vs explicit append parity, forge_record / load_record / mount_from / gen, executed-cell
# identity (v3: against a MANDATORY EXTERNAL PIN, see below), ZIP + SHA256SUMS + read-back + receipt + Drive chain. Engine selections are
# identical to TEST896 (709 / 730 / 757 / 877 / 878 / 873 / test870, commit f1007d91).
# Not used here: TEST896 worlds / parser / arms / decision / statistics / TEXT_CEILING. Gate-4 (transfer) = NOT_RUN.
# RUN PRECONDITION (source identity, fail-closed): before running this cell, store the audited identity of THIS file as
# the Colab secret NPDM_PIN (key icon in the left panel; enable notebook access), value exactly
#   commit=<40 hex>;path=897npdm_smoke.py;blob=<40 hex>;sha256=<64 hex>;bytes=<int>
# taken from the independent audit of the published commit (never computed by this cell). No pin / any mismatch -> the run
# stops with SOURCE_IDENTITY_MISMATCH before the model is loaded.
# =====================================================================================================================
import os, sys, subprocess, importlib.util, importlib.metadata, urllib.request, hashlib, ast, json, time, gc, math
import traceback, platform, types, random, shutil, re
from pathlib import Path
from datetime import datetime, timezone
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')

# ---------------------------------------------------------------------------------------------------------- versions
# Bootstrap record (stdlib only) is created BEFORE the torch check / pip / imports, so a bootstrap failure is recorded.
RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
ROOT = Path(('/content/' if Path('/content').exists() else '/tmp/') + 'NPDM_SMOKE_' + RUN_ID)
ROOT.mkdir(parents=True, exist_ok=True)
LOG = ROOT / 'NPDM_SMOKE.log'; OUT = ROOT / 'NPDM_SMOKE_results.json'; LOG.write_text('')
ZIP_PATH = ROOT.parent / ('NPDM_SMOKE_SONUC_' + RUN_ID + '.zip'); RECEIPT_PATH = ROOT.parent / ('NPDM_SMOKE_SONUC_' + RUN_ID + '_RECEIPT.json')
def _ver(name):
    try: return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError: return None
def _boot_fail(e):
    tb = traceback.format_exc()
    rec = {'test': 'NPDM_SMOKE', 'run_id': RUN_ID, 'status': 'BOOTSTRAP_ERROR', 'error': '%s: %s' % (type(e).__name__, e),
           'traceback': tb, 'installed_versions': {p_: _ver(p_) for p_ in ('torch', 'transformers', 'accelerate', 'bitsandbytes')},
           'technical_verdict': 'NOT_RUN', 'ARTIFACT_STATUS': 'FAIL', 'gpu_model_loaded': False,
           'note': 'stopped before any model / GPU work; Drive not attempted'}
    for path_, txt_ in ((OUT, json.dumps(rec, indent=2)), (RECEIPT_PATH, json.dumps(rec, indent=2))):
        try: tmp_ = Path(str(path_) + '.tmp'); tmp_.write_text(txt_); tmp_.replace(path_)
        except Exception as e2: print('BOOTSTRAP_RECORD_WRITE_FAILED', path_, e2)
    with LOG.open('a') as f_: f_.write('BOOTSTRAP_ERROR %s\n%s\nARTIFACT_STATUS=FAIL\n' % (rec['error'], tb))
    print(tb); print('NPDM_SMOKE BOOTSTRAP_ERROR recorded in', OUT, LOG, RECEIPT_PATH)
    raise SystemExit('NPDM_SMOKE BOOTSTRAP_ERROR: ' + rec['error'])
try:
    # Exact runtime contract. torch 2.14.1+cu130 / CUDA 13.0 / transformers 5.22.1 = the combination recorded in 893.log
    # (TABLE GATE0 RUNTIME) under which this engine, incl. api877, ran on the A100. accelerate 1.16.0 / bitsandbytes 0.50.2 =
    # the versions whose sources K3.1 audited (not recorded in 893.log). torch is never installed or changed by this cell.
    TORCH_REQ = '2.14.1+cu130'; CUDA_REQ = '13.0'
    PINS = {'transformers': '5.22.1', 'accelerate': '1.16.0', 'bitsandbytes': '0.50.2'}
    if _ver('torch') != TORCH_REQ:
        raise SystemExit('NPDM_SMOKE_ENV: torch %s found, %s required (893.log runtime); no torch change is made' % (_ver('torch'), TORCH_REQ))
    _need = [p for p, v in PINS.items() if _ver(p) != v]
    if _need:
        _loaded = [p for p in _need if p in sys.modules]
        if _loaded: raise SystemExit('NPDM_SMOKE_ENV: %s already imported with other versions; restart the runtime and rerun' % _loaded)
        _con = Path('/tmp/NPDM_SMOKE_torch_constraint.txt'); _con.write_text('torch==%s\n' % TORCH_REQ)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', '-c', str(_con)] + ['%s==%s' % (p, PINS[p]) for p in _need])
    _got = {p: _ver(p) for p in list(PINS) + ['torch']}
    if any(_got[p] != v for p, v in PINS.items()) or _got['torch'] != TORCH_REQ:
        raise SystemExit('NPDM_SMOKE_ENV: version contract not met after install: %s' % _got)
    import torch, transformers, accelerate, bitsandbytes
    if torch.__version__ != TORCH_REQ or torch.version.cuda != CUDA_REQ or transformers.__version__ != PINS['transformers'] or \
            accelerate.__version__ != PINS['accelerate'] or bitsandbytes.__version__ != PINS['bitsandbytes']:
        raise SystemExit('NPDM_SMOKE_ENV: imported versions differ from the contract: torch %s cuda %s transformers %s accelerate %s '
                         'bitsandbytes %s' % (torch.__version__, torch.version.cuda, transformers.__version__, accelerate.__version__,
                                              bitsandbytes.__version__))
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    from transformers.cache_utils import DynamicCache
except BaseException as _e:
    if isinstance(_e, KeyboardInterrupt): raise
    _boot_fail(_e)


# --------------------------------------------------------------------------------------------------------- constants
TAG = 'NPDM_SMOKE'; MARKER = 'AKBASCORE SILICON HIPPOCAMPUS — NPDM SMOKE — NATIVE PROSPECTIVE DISCREPANCY MEMORY'
COMMIT = 'f1007d912773f3460536784ff80a215741bc97e9'
RAW_BASE = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/' + COMMIT + '/'
MODEL_ID = 'Qwen/Qwen2.5-72B-Instruct'; CUT = 3; DTYPE = torch.bfloat16; DEV = torch.device('cuda:0')
MODEL_REVISION = '495f39366efef23836d0cfae4fbe635880d2be31'
GPU_NAME_REQ = 'NVIDIA A100-SXM4-80GB'; GPU_CC_REQ = (8, 0)
EXPECTED = (80, 8192, 64, 8, 128); CHUNK = 128; GPU_RESERVE_GIB = 9.0
SEED = 20261118
CART_DIR = ROOT / 'cartridges'; CART_DIR.mkdir(exist_ok=True)
NS_DIRS = {'factual': CART_DIR / 'factual', 'prediction': CART_DIR / 'prediction', 'control': CART_DIR / 'control',
           'quarantine': CART_DIR / 'quarantine', 'twin': CART_DIR / 'twin', 'canary': CART_DIR / 'canary'}
for _d in NS_DIRS.values(): _d.mkdir(exist_ok=True)
DERIVED_DIR = NS_DIRS['control']
EVENTS = ROOT / 'NPDM_SMOKE_events.jsonl'; EVENTS.write_text('')
DRIVE_DIR = None; DRIVE_ERR = {'mount': None, 'backup_failures': 0, 'last': None}
LOCKS = {'709.py': '6c9f8cbb1eeed848d45133d73f0d7676b68e9125', '730.py': 'b1bad9eb3b111b44413f8ef05a3a140ab66a77dd',
         '757.py': '3d88bf8638390995858f23391f1e043faa586835', '873.py': '2e44affa5e0dd462155fb265c331270fb8e7b7e1',
         '877.py': 'a6aa7648e0fb765a8dc9b56b8f79b4dcef5fc772', '878.py': '7842e8675544a0328e3552f059c81b7750068a82',
         'test870.py': 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', '779.py': 'fa7017a87f25ecef6ed2b2954a850599cb25fcd9',
         '893.py': 'd401c7f0baf15dfcabcc6f4239d9616526fe41f2', '893.log': '0f61b967edf48dc7f2874d7b537b8eefec18c50a'}
K31_BLOBS = {'709.py': '6c9f8cbb1eeed848d45133d73f0d7676b68e9125', '757.py': '3d88bf8638390995858f23391f1e043faa586835',
             '779.py': 'fa7017a87f25ecef6ed2b2954a850599cb25fcd9', '878.py': '7842e8675544a0328e3552f059c81b7750068a82',
             '893.py': 'd401c7f0baf15dfcabcc6f4239d9616526fe41f2', '893.log': '0f61b967edf48dc7f2874d7b537b8eefec18c50a'}
HISTORY = {'894.log': ('58bcab13a0a89d4326a7a5b40c184d53a144ad3f', '3aff8f3304bbe8ed08a55fb6adf188b126280203',
                       ('20261118T031507Z', 'TECHNICAL_VERDICT=UNDECIDABLE | STATUS=COMPLETE | ARTIFACT_STATUS=PASS')),
           '895.log': ('dd53d4b81c85c023872214cb8b49e49a3b695a6b', 'a0e8169b896e5afc984d0a4ed24ab74d551e0da2',
                       ('20261118T051416Z', 'TEST895_FINAL TECHNICAL_VERDICT=UNDECIDABLE | STATUS=COMPLETE | ARTIFACT_STATUS=PASS')),
           '896.py': ('9454b3db70cfeceaecb67edf87be490115e32499', '00b4a6dade7e430636740ab53bdb349eb2d79a84', ()),
           '896.log.txt': ('c4ae25177acea4b4c48a7cdc4d3edc4c28e70f7e', 'a01abeb75330ae9ae5c1548a774dffe741771e78',
                           ('20261118T085023Z', 'TEST896_LOG_END SCIENTIFIC_VERDICT=PASS | STATUS=COMPLETE'))}
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
TOL = {'parity_close_rel': 1e-2, 'P_expected': 30, 'chunk_expected': 128}
# Pre-registered abort limits (estimates, fixed before the run; never changed after seeing results). Wall time counts from
# the end of the model load (the experiment); the model load itself is reported separately. These are POST-OPERATION
# guards (checked after each query / forge / append returns): not preemptive timeouts, and no out-of-memory guarantee.
ABORT = {'semantics': 'post-operation guards, not preemptive timeouts, no OOM guarantee', 'experiment_wall_s': 90 * 60, 'gpu_peak_gib': 74.0, 'cartridge_bytes_gib': 12.0, 'disk_free_min_gib': 12.0,
         'cpu_ram_frac': 0.85, 'query_s': 180.0, 'forge_append_s': 60.0}
PROTO = {'seed': SEED, 'budget_decisions': 4, 'max_new_margin_tokens': 4,
         'gate2': 'eligible = first decision after a wrong-predicted ACQUIRE, max 1 per episode; >= 2 eligible; '
                  'C1 (raw-decision specificity) = no wrong-direction change, >= 2 correct-direction, every non-ceiling state '
                  'correct and the outcome-conditioned placebo u (u != p, u != o) gives a different raw decision; C1b (reported) = '
                  'placebo decision also not optimal; C2 = CF_OUTCOME discriminating and tracked; C3a (reported) = FACTUAL_DELETED '
                  'changes the decision; C3b = chosen decision not optimal without the observed outcome AND FACTUAL_DELETED changes '
                  'it AND the new decision is optimal without the outcome; required + changed + not optimal = WRONG_CORRECTION -> '
                  'FAIL. SMOKE_CAUSAL_PASS iff C1, C2 and C3b in every correct state; otherwise with C1 -> SMOKE_CAUSAL_PASS_LIMITED; '
                  'CYCLIC_PRED diagnostic only; smoke canary only, never a scientific PASS',
         'query_upper_bound': '14 x 4 live + 14 x 12 control arms (max 1 eligible state per episode) + 1 twin + 7 DIRECT = 232',
         'gate3': 'first decisions of A1 A2 B1 D1 D2 L1 L2: PASS_SUPPORT iff optimal >= 5/7 and >= 2 more than DIRECT, '
                  'no ACQUIRE in A1 / B1 / L2, no collapse; FAIL iff utility below DIRECT, a forbidden ACQUIRE or collapse'}
MAX_NEW = 24                                     # replaced by the tokenizer-derived bound before the first generation
GATE0 = ('ENV', 'SOURCE', 'EXTRACT', 'MODEL', 'G0_MANIFEST', 'G0_P0_A_PARITY', 'G0_P0_B_PARITY')
GATE1 = ('G1_PARSER_SEMANTICS', 'G1_LIVE_EPISODES', 'G1_REBUILD_FROM_SSD', 'G1_PRE_OUTCOME_TWIN', 'G1_ISOLATION_PROVENANCE',
         'G1_PENDING', 'G1_CONTROL_GEOMETRY', 'G1_DETERMINISM', 'P1_PHYSICAL', 'P7_INTEGRITY')
GATE_ORDER = GATE0 + GATE1[:-2] + ('G2_CAUSAL_PREDICTION_USE', 'G3_POLICY_SUPPORT', 'G4_TRANSFER') + GATE1[-2:]
CRITICAL = GATE0 + GATE1
REQUIRED = ()
R = {'test': 'NPDM_SMOKE', 'stage': 'native prospective discrepancy memory, causal smoke', 'run_id': RUN_ID,
     'commit': COMMIT, 'status': 'STARTED', 'checks': [],
     'gates': {g: {'status': 'NOT_RUN', 'reason': None, 'data': {}} for g in GATE_ORDER},
     'history': {'TEST885': 'NEGATIVE', 'TEST893': 'FAIL_NO_GAIN', 'TEST894': 'UNDECIDABLE', 'TEST895': 'UNDECIDABLE',
                 'TEST896': 'PASS in log (DIRECT_EXPERIENCE_SUPPORTED, guided exploration); artefacts UNVERIFIED',
                 'note': 'locked; not modified, not reinterpreted'},
     'model_revision': MODEL_REVISION, 'runtime_pins': dict(PINS, torch=TORCH_REQ, cuda=CUDA_REQ),
     'scope': 'smoke: 6 live + 7 diagnostic-prefix + 1 pending episodes; not a cohort, not TEST897, not transfer, not VOI',
     'executed_by_author': False, 'tolerances': TOL, 'abort_limits': ABORT, 'protocol': PROTO,
     'tolerances_sha256': hashlib.sha256(json.dumps({'TOL': TOL, 'ABORT': ABORT, 'PROTO': PROTO}, sort_keys=True).encode()).hexdigest()}
T0 = time.perf_counter()
# ----------------------------------------------------------------------------------------------------------- logging
def log(*xs):
    s = ' '.join(str(x) for x in xs); print(s, flush=True)
    with LOG.open('a') as f: f.write(s + '\n')
SAVE_T = [0.0]
def save(force=True):
    # atomic local write + progressive Drive backup of log + JSON + events (TEST870 style). NPDM_SMOKE: the engine's per-forge
    # check() calls save(False): those writes are throttled (local at most every 15 s, no Drive copy), so ~1100 cartridge
    # forges do not re-copy the growing report to Drive. Every gate / world boundary / exception still forces both.
    # The events JSONL is fsync'ed per event independently of this, so no record is lost between saves.
    if not force and time.perf_counter() - SAVE_T[0] < 15.0: return
    SAVE_T[0] = time.perf_counter()
    R['drive_backup'] = dict(DRIVE_ERR, dir=DRIVE_DIR)
    tmp = OUT.with_suffix('.json.tmp'); tmp.write_text(json.dumps(R, ensure_ascii=False, indent=2, default=str)); tmp.replace(OUT)
    if DRIVE_DIR is not None and force:
        try:
            for f_ in (LOG, OUT, EVENTS): shutil.copy2(f_, Path(DRIVE_DIR) / f_.name)
        except Exception as e:
            DRIVE_ERR['backup_failures'] += 1; DRIVE_ERR['last'] = '%s: %s' % (type(e).__name__, e)
def check(name, ok, detail=None):
    # same signature/semantics as the 730/757 check() used by the extracted engine definitions
    R['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail}); save(bool(not ok))
    log('PASS' if ok else 'FAIL', name, '' if detail is None else json.dumps(detail, default=str)[:600])
    if not ok: raise RuntimeError('CHECK_FAILED:' + name)
class StopT896(Exception): pass
def gate(name, status, reason=None, **data):
    assert status in ('PASS', 'FAIL', 'INCONCLUSIVE', 'DIAGNOSTIC', 'NOT_RUN', 'SMOKE_CAUSAL_PASS', 'SMOKE_CAUSAL_PASS_LIMITED', 'PASS_SUPPORT', 'INCONCLUSIVE_SUPPORT'), status
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
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'AKBASCORE-NPDM_SMOKE'}), timeout=120) as f:
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
    """Every forge / mount / append / reference prefill runs inside this (TEST895 name kept; there is no adapter in NPDM_SMOKE,
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


# ===================================================================== NPDM pure logic (no torch; CPU-tested by AST extraction)
# Native Prospective Discrepancy Memory smoke. Everything in this block is plain Python and has NO access to any hidden
# mapping: public contract, record grammar, strict parser, episode runner (orchestration only), arm derivation, ledger
# tickets, environment factory (mapping only inside its closure), public-Bayes evaluator and the gate engine.
import itertools as _it
CODE_ALPH_NPDM = 'BCDFGHJKLMNPQRSTVWXZ'
# The PRIMARY marker fixes the token length of every action / outcome / prediction field; SECONDARY markers (used only as
# outcome / prediction field fillers in control arms) take the first pre-registered candidate with the same token length.
PRIMARY_MARKER_NPDM = 'PREDICTION_WITHHELD'
SECONDARY_CANDIDATES_NPDM = {
    'outcome_withheld': ('OUTCOME_WITHHELD', 'OUTCOME_NOT_SHOWN', 'WITHHELD_OUTCOME', 'OUTCOME_REMOVED', 'OUTCOME_HIDDEN_HERE',
                         'OUTCOME_LEFT_OUT', 'NO_OUTCOME_SHOWN', 'OUTCOME_OMITTED', 'OUTCOME_NOT_GIVEN')}
STATUS_MARKERS_NPDM = {'pending': 'OUTCOME_PENDING', 'none': 'OUTCOME_NONE'}     # protocol facts, never replaced by an arm
# model-visible record templates: (kind) -> segments; '{F}' fields are tokenized separately (geometry = field lengths)
REC_TPL_NPDM = {
    'PRIOR_OBSERVATION':   ('Observation given at the start of this episode: action ', '{A}', ' produces outcome ', '{O}', '.\n'),
    'MODEL_INTENT':        ('Step {t}: I chose {K} ', '{A}', '.\n'),
    'MODEL_PREDICTION':    ('Step {t}: before the outcome was observed, I predicted outcome ', '{P}', '.\n'),
    'OBSERVED_OUTCOME':    ('Step {t}: the observed outcome was ', '{O}', '.\n'),
    'OUTCOME_STATUS':      ('Step {t}: outcome status ', '{S}', '.\n'),
    'MODEL_STOP':          ('Step {t}: I chose STOP.\n',),
    'MODEL_ABSTAIN':       ('Step {t}: I abstained.\n',),
    'MODEL_INVALID':       ('Step {t}: my output was not a valid decision.\n',)}
FACTUAL_KINDS_NPDM = ('PRIOR_OBSERVATION', 'MODEL_INTENT', 'OBSERVED_OUTCOME', 'OUTCOME_STATUS', 'MODEL_STOP', 'MODEL_ABSTAIN', 'MODEL_INVALID')
PREDICTION_KINDS_NPDM = ('MODEL_PREDICTION',)
QUERY_TPL_NPDM = ('ENVIRONMENT RULES. Actions: {acts}. Outcomes: {outs}. Each action always produces the same outcome and '
                  'different actions produce different outcomes; all {nperm} assignments of outcomes to actions were equally '
                  'likely at the start. Goal outcome: {g}. ACQUIRE <action> shows the outcome of that action, costs {c}, gives '
                  'no reward and the episode continues. ACT <action> ends the episode with reward 1 if its outcome is the goal '
                  'outcome, otherwise 0. STOP ends the episode with reward 0. Decisions left: {left}. The INFORMATION above is '
                  'your own memory of this episode (it may be empty). ')
GRAMMAR_NPDM = {'PRED': 'Reply exactly as: ACT <action> PREDICTION <outcome you expect>, or ACQUIRE <action> PREDICTION '
                        '<outcome you expect>, or STOP.',
                'DIRECT': 'Reply exactly as: ACT <action>, or ACQUIRE <action>, or STOP.'}
LEAK_NAMES_NPDM = ('mapping', 'vault', 'world_id', 'arm', 'seed', 'evaluator', 'pi_', 'secret')
# immutable arm specification for the counterfactual controls (never executed in the environment, never written live)
ARMS_NPDM = (
    ('NPDM',             'PRED',   'facts + the model\'s own pre-outcome predictions (the frozen live state, rebuilt from SSD)'),
    ('NO_PRED',          'PRED',   'PRIMARY: only the FOCAL prediction record removed (one record shorter)'),
    ('PRED_MASK',        'PRED',   'PRIMARY: focal prediction field replaced by PREDICTION_WITHHELD (equal per-field geometry)'),
    ('PLACEBO_PRED',     'PRED',   'PRIMARY, OUTCOME-CONDITIONED OFFLINE COUNTERFACTUAL: focal prediction p -> the unique public outcome u '
                                   'with u != p and u != o (o = observed outcome read from the frozen ledger); equal geometry'),
    ('CYCLIC_PRED',      'PRED',   'diagnostic only (outcome-blind): focal prediction rotated o_i -> o_(i+1); collision / no-collision strata'),
    ('NO_PRED_ALL',      'PRED',   'secondary: every prediction record removed'),
    ('PLACEBO_PRED_ALL', 'PRED',   'secondary: every valid prediction rotated o_i -> o_(i+1)'),
    ('FACTUAL_DELETED',  'PRED',   'focal observed outcome replaced by OUTCOME_WITHHELD (equal geometry)'),
    ('CF_OUTCOME',       'PRED',   'counterfactual: focal observed outcome replaced by a public-consistent alternative, prediction unchanged'),
    ('MATCHED_FORGE_IO', 'PRED',   'NO_PRED mount; focal prediction re-forged into quarantine, not mounted (extra forge/IO determinism only)'),
    ('DIRECT',           'DIRECT', 'NO_PRED_ALL mount, decision-only grammar (format baseline, format-confounded)'),
    ('ORDER_PERM',       'PRED',   'NPDM mount, public action/outcome lists in the query cyclically permuted (diagnostic)'))

def choose_markers_npdm(ntok):
    out = {'prediction_withheld': PRIMARY_MARKER_NPDM}; n = ntok(PRIMARY_MARKER_NPDM)   # field length of every name / marker
    for k, cands in SECONDARY_CANDIDATES_NPDM.items():
        m = [c for c in cands if ntok(c) == n]
        if not m: raise RuntimeError('MARKER_GEOMETRY_NOT_FOUND %s (needs %d tokens)' % (k, n))
        out[k] = m[0]
    out['field_ntok'] = n
    return out

def _code_npdm(rng, ntok, n_target, used, tries=300000):
    for _ in range(tries):
        s = ''.join(rng.choice(CODE_ALPH_NPDM) for _ in range(rng.randint(3, 24)))
        if ntok(s) != n_target or s in used or any(s in u or u in s for u in used): continue
        used.add(s); return s
    raise RuntimeError('NAME_GEOMETRY_NOT_FOUND n=%d' % n_target)

# episode plan (pre-registered). kind: live = K0 start, the model's own trajectory; diag = public prefix given at the start
# (labelled PRIOR_OBSERVATION, never called model experience); 'rel' fixes the prefix relative to the hidden goal.
EPISODE_PLAN_NPDM = (
    ('L1', 'live', 0.1, None), ('L2', 'live', 0.8, None), ('L3', 'live', 0.1, None), ('L4', 'live', 0.8, None),
    ('L5', 'live', 0.1, None), ('L6', 'live', 0.1, None),
    ('A1', 'diag', 0.1, 'K1_GOAL_KNOWN'), ('A2', 'diag', 0.1, 'K1_GOAL_UNKNOWN'), ('B1', 'diag', 0.8, 'SAME_AS:A2'),
    ('D1', 'diag', 0.1, 'K2_GOAL_FIRST'), ('D2', 'diag', 0.1, 'SAME_AS:D1:GOAL_SECOND'),
    ('A2L', 'diag', 0.1, 'K1_GOAL_UNKNOWN'), ('B1L', 'diag', 0.8, 'SAME_AS:A2L'),
    ('P1', 'pending', 0.1, None))
BUDGET_NPDM = 4

def make_episodes_npdm(seed, ntok, markers):
    """All random draws before the model runs. Returns (public, vault): public[eid] = model-visible contract + prefix
    observations; vault[eid] = mapping and bookkeeping for the environment / offline evaluator only."""
    import random as _r
    rng = _r.Random(seed); used = set(markers[k] for k in ('prediction_withheld', 'outcome_withheld')) | set(STATUS_MARKERS_NPDM.values())
    public, vault = {}, {}
    for eid, kind, cost, rel in EPISODE_PLAN_NPDM:
        g2 = None
        if rel and rel.startswith('SAME_AS'):
            base = rel.split(':')[1]; pb, vb = public[base], vault[base]
            acts, outs, mp, prefix = list(pb['actions']), list(pb['outcomes']), dict(vb['mapping']), [tuple(x) for x in pb['prefix']]
            goal = vb['goal2'] if rel.endswith('GOAL_SECOND') else pb['goal']
            act_order, out_order = list(pb['actions']), list(pb['outcomes'])
        else:
            acts = [_code_npdm(rng, ntok, markers['field_ntok'], used) for _ in range(3)]
            outs = [_code_npdm(rng, ntok, markers['field_ntok'], used) for _ in range(3)]
            perm = list(outs); rng.shuffle(perm); mp = dict(zip(acts, perm)); inv = {o: a for a, o in mp.items()}
            goal = rng.choice(outs); prefix = []
            if rel == 'K1_GOAL_KNOWN': prefix = [(inv[goal], goal)]
            elif rel == 'K1_GOAL_UNKNOWN':
                a = rng.choice([x for x in acts if mp[x] != goal]); prefix = [(a, mp[a])]
            elif rel == 'K2_GOAL_FIRST':
                two = rng.sample(acts, 2); prefix = [(two[0], mp[two[0]]), (two[1], mp[two[1]])]; goal = mp[two[0]]; g2 = mp[two[1]]
            act_order = acts[:]; rng.shuffle(act_order); out_order = outs[:]; rng.shuffle(out_order)
        public[eid] = {'actions': tuple(act_order), 'outcomes': tuple(out_order), 'goal': goal, 'cost': cost,
                       'budget': BUDGET_NPDM, 'prefix': tuple(tuple(p) for p in prefix), 'kind': kind}
        vault[eid] = {'mapping': mp, 'goal2': g2, 'rel': rel, 'pending_steps': 1 if kind == 'pending' else 0}
    return public, vault

def contract_npdm(pub):  # the ONLY object the query builder receives (no mapping, no episode id)
    return {k: pub[k] for k in ('actions', 'outcomes', 'goal', 'cost', 'budget')}

def query_npdm(contract, left, grammar, rot=0):
    acts = list(contract['actions']); outs = list(contract['outcomes'])
    if rot: acts = acts[rot:] + acts[:rot]; outs = outs[rot:] + outs[:rot]
    return QUERY_TPL_NPDM.format(acts=', '.join(acts), outs=', '.join(outs), nperm=len(list(_it.permutations(outs))),
                                 g=contract['goal'], c=('%.1f' % contract['cost']), left=left) + GRAMMAR_NPDM[grammar]

def segments_npdm(rec):
    out = []
    for s in REC_TPL_NPDM[rec['kind']]:
        if s == '{A}': out.append(rec['A'])
        elif s == '{O}': out.append(rec['O'])
        elif s == '{P}': out.append(rec['P'])
        elif s == '{S}': out.append(rec['S'])
        else: out.append(s.format(t=rec.get('t', 0), K=rec.get('K', '')))
    return out

def record_ids_npdm(rec, tok_ids):
    out = []
    for s in segments_npdm(rec): out += list(tok_ids(s))
    return out

def geometry_npdm(records, tok_ids): return [[len(tok_ids(s)) for s in segments_npdm(r)] for r in records]

def parse_npdm(text, contract, grammar):
    """Strict public grammar, no correction. Tokens are whitespace-separated; ONE trailing period on the last token is
    tolerated. PRED grammar: ACT|ACQUIRE <public action> PREDICTION <public outcome>, or STOP. A missing prediction, an
    UNKNOWN prediction or a non-outcome prediction is NOT allowed by the public grammar -> the whole output is INVALID (no
    environment step, no reward, a decision is consumed). ABSTAIN / UNKNOWN as the whole output = ABSTAIN (no environment).
    DIRECT grammar: ACT|ACQUIRE <public action>, or STOP."""
    s = (text or '').strip(); toks = s.split()
    if toks and toks[-1].endswith('.'): toks[-1] = toks[-1][:-1]
    r = {'status': 'INVALID', 'kind': None, 'action': None, 'prediction': None, 'pred_status': 'NONE'}
    acts, outs = set(contract['actions']), set(contract['outcomes'])
    if len(toks) == 1 and toks[0] == 'STOP': r.update(status='STOP', kind='STOP'); return r
    if len(toks) == 1 and toks[0] in ('ABSTAIN', 'UNKNOWN'): r.update(status='ABSTAIN', kind='ABSTAIN'); return r
    if len(toks) < 2 or toks[0] not in ('ACT', 'ACQUIRE') or toks[1] not in acts: return r
    if grammar == 'DIRECT':
        if len(toks) != 2: return r
        r.update(status='VALID', kind=toks[0], action=toks[1], pred_status='NOT_REQUESTED'); return r
    if len(toks) == 4 and toks[2] == 'PREDICTION' and toks[3] in outs:
        r.update(status='VALID', kind=toks[0], action=toks[1], prediction=toks[3], pred_status='VALID'); return r
    r['pred_status'] = 'MISSING' if len(toks) == 2 else ('UNKNOWN' if len(toks) == 4 and toks[2] == 'PREDICTION' and toks[3] == 'UNKNOWN'
                                                        else 'MALFORMED')
    return r

class LedgerNPDM:
    """Append-only record ledger of one episode. A ticket for env.step exists only after the intent AND the prediction
    record of the current step were sealed (file written + SHA recorded) and are the two newest records."""
    def __init__(self, clock): self.recs = []; self.clock = clock; self.events = []
    def add(self, rec, ent):
        self.recs.append((rec, ent, self.clock())); return len(self.recs) - 1
    def ticket(self, step):
        if len(self.recs) < 2: raise RuntimeError('TICKET_WITHOUT_RECORDS')
        (ri, ei, ti), (rp, ep, tp) = self.recs[-2], self.recs[-1]
        if ri['kind'] != 'MODEL_INTENT' or rp['kind'] != 'MODEL_PREDICTION' or ri['t'] != step or rp['t'] != step:
            raise RuntimeError('TICKET_ORDER_VIOLATION')
        if not (ei.get('sha256') and ep.get('sha256')): raise RuntimeError('TICKET_UNSEALED')
        return {'step': step, 'intent_sha256': ei['sha256'], 'prediction_sha256': ep['sha256'], 'sealed_ns': tp, 'used': False}

def make_env_npdm(mapping, goal, pending_steps, clock):
    """Environment: the hidden mapping lives only in this closure. step() requires a sealed ticket and records the
    env_step_start time; a pending outcome is released only by resolve(ticket)."""
    mp = dict(mapping); state = {'closed': False, 'pending': None, 'pend_left': int(pending_steps), 'log': []}
    def step(kind, action, ticket):
        if state['closed']: raise RuntimeError('ENV_CLOSED')
        if ticket is None or ticket.get('used'): raise RuntimeError('ENV_STEP_WITHOUT_FRESH_TICKET')
        ticket['used'] = True; t0 = clock()
        if t0 <= ticket['sealed_ns']: raise RuntimeError('ENV_STEP_NOT_AFTER_SEAL')
        o = mp[action]; reward = (1 if o == goal else 0) if kind == 'ACT' else 0
        if kind == 'ACT': state['closed'] = True
        rec = {'kind': kind, 'action': action, 'env_step_start_ns': t0, 'reward': reward}
        if state['pend_left'] > 0:
            state['pend_left'] -= 1; state['pending'] = (o, ticket['step']); rec['status'] = 'PENDING'; state['log'].append(rec)
            return {'status': 'PENDING', 'env_step_start_ns': t0, 'reward': reward, 'terminal': kind == 'ACT'}
        rec['status'] = 'OUTCOME'; state['log'].append(rec)
        return {'status': 'OUTCOME', 'outcome': o, 'env_step_start_ns': t0, 'reward': reward, 'terminal': kind == 'ACT'}
    def resolve(step_):
        if state['pending'] is None or state['pending'][1] != step_: raise RuntimeError('ENV_NOTHING_PENDING')
        o = state['pending'][0]; state['pending'] = None
        return {'status': 'OUTCOME', 'outcome': o, 'arrival_ns': clock()}
    return {'step': step, 'resolve': resolve, 'log': state['log'], 'is_closed': lambda: state['closed']}

def run_episode_npdm(pub, env, decide, write, markers, clock, grammar='PRED'):
    """Orchestration only (CPU-testable): decide(query) -> raw text; write(rec) -> sealed entry dict. Order per ACT/ACQUIRE:
    intent sealed -> prediction (or marker) sealed -> ticket -> env.step -> [pending status sealed -> resolve] -> observed
    outcome sealed. STOP: model stop record, no environment. ABSTAIN / INVALID: record + OUTCOME_NONE, no environment, a
    decision is consumed. Budget exhaustion is a harness event, not a model STOP."""
    c = contract_npdm(pub); L = LedgerNPDM(clock); trace = []; payoff = 0.0; t = 0; closed = False
    for a, o in pub['prefix']:
        rec = {'kind': 'PRIOR_OBSERVATION', 'A': a, 'O': o, 't': 0}; L.add(rec, write(rec))
    while t < pub['budget'] and not closed:
        t += 1; q = query_npdm(c, pub['budget'] - t + 1, grammar); raw = decide(q); p = parse_npdm(raw, c, grammar)
        step = {'t': t, 'query': q, 'raw': raw, 'parsed': p, 'records': []}
        def W(rec):
            ent = write(rec); i = L.add(rec, ent); step['records'].append({'kind': rec['kind'], 'i': i, 'sha256': ent.get('sha256'), 'ns': L.recs[i][2]}); return ent
        if p['status'] == 'STOP':
            W({'kind': 'MODEL_STOP', 't': t}); closed = True; step['env'] = None
        elif p['status'] in ('ABSTAIN', 'INVALID'):
            W({'kind': 'MODEL_ABSTAIN' if p['status'] == 'ABSTAIN' else 'MODEL_INVALID', 't': t})
            W({'kind': 'OUTCOME_STATUS', 'S': STATUS_MARKERS_NPDM['none'], 't': t}); step['env'] = None
        else:
            W({'kind': 'MODEL_INTENT', 'K': p['kind'], 'A': p['action'], 't': t})
            if grammar == 'PRED': W({'kind': 'MODEL_PREDICTION', 'P': p['prediction'], 't': t, 'pred_status': 'VALID'})
            tk = L.ticket(t) if grammar == 'PRED' else {'step': t, 'sealed_ns': L.recs[-1][2], 'used': False}
            r = env['step'](p['kind'], p['action'], tk); step['env'] = dict(r)
            if r['status'] == 'PENDING':
                W({'kind': 'OUTCOME_STATUS', 'S': STATUS_MARKERS_NPDM['pending'], 't': t})
                r2 = env['resolve'](t); step['env_resolved'] = dict(r2); o = r2['outcome']
            else: o = r['outcome']
            ent = W({'kind': 'OBSERVED_OUTCOME', 'O': o, 't': t})
            step['outcome'] = o; step['outcome_seal_ns'] = step['records'][-1]['ns']
            if step['outcome_seal_ns'] <= r['env_step_start_ns']: raise RuntimeError('OUTCOME_SEALED_BEFORE_ENV_STEP')
            payoff -= pub['cost'] if p['kind'] == 'ACQUIRE' else 0.0
            if p['kind'] == 'ACT': payoff += r['reward']; closed = True
        trace.append(step)
    return {'trace': trace, 'ledger': [(rec, ent.get('sha256'), ns) for rec, ent, ns in L.recs], 'payoff': payoff,
            'closed_by': ('MODEL' if closed else 'BUDGET_EXHAUSTED')}

def cf_outcome_npdm(records, pub, focus_t):
    """Pre-registered counterfactual outcome for the focal step: the first outcome after the observed one in the cyclic
    PUBLIC outcome order that (i) differs from the observed outcome, (ii) differs from the focal prediction (the step keeps a
    discrepancy) and (iii) keeps every other fact consistent with a bijection. Uses only public records (no hidden mapping).
    Returns None when no such outcome exists (CF not applicable)."""
    outs = list(pub['outcomes']); F = facts_npdm(records); it = {r['t']: r['A'] for r in records if r['kind'] == 'MODEL_INTENT'}
    obs = [r['O'] for r in records if r['kind'] == 'OBSERVED_OUTCOME' and r['t'] == focus_t][0]
    pred = [r['P'] for r in records if r['kind'] == 'MODEL_PREDICTION' and r['t'] == focus_t][0]
    a = it[focus_t]; others = {(x, o) for x, o in F if not (x == a and o == obs)}
    for k in range(1, len(outs)):
        o2 = outs[(outs.index(obs) + k) % len(outs)]
        if o2 in (obs, pred): continue
        if any(o == o2 and x != a for x, o in others) or any(x == a and o != o2 for x, o in others): continue
        return o2
    return None

def placebo_u_npdm(records, pub, focus_t):
    """Primary placebo target: the UNIQUE public outcome u with u != p (focal prediction) and u != o (focal observed outcome,
    read only from the frozen records). Returns None if p or o is not a public outcome, p == o, or u is not unique
    (never a fallback). Outcome-conditioned: it uses o, which is already a mounted factual record (no hidden information)."""
    outs = list(pub['outcomes'])
    p = [r['P'] for r in records if r['kind'] == 'MODEL_PREDICTION' and r.get('t') == focus_t]
    o = [r['O'] for r in records if r['kind'] == 'OBSERVED_OUTCOME' and r.get('t') == focus_t]
    if len(p) != 1 or len(o) != 1 or p[0] not in outs or o[0] not in outs or p[0] == o[0]: return None
    u = [x for x in outs if x != p[0] and x != o[0]]
    return u[0] if len(u) == 1 else None

def derive_arm_npdm(arm, records, pub, markers, focus_t):
    """Control mounts from the SAME frozen live state (records up to the eligible decision). Returns new record dicts with
    'src' and 'changed'; originals are not modified. focus_t = the discrepancy step. Focal arms touch only that step."""
    outs = list(pub['outcomes']); res = []
    cf = cf_outcome_npdm(records, pub, focus_t) if arm == 'CF_OUTCOME' else None
    if arm == 'CF_OUTCOME' and cf is None: return None
    u = placebo_u_npdm(records, pub, focus_t) if arm == 'PLACEBO_PRED' else None
    if arm == 'PLACEBO_PRED' and u is None: return None                 # technical: no fallback to any other placebo
    for i, r in enumerate(records):
        nr = dict(r); ch = False; pr = r['kind'] == 'MODEL_PREDICTION'; focal = r.get('t') == focus_t
        if pr and (arm in ('NO_PRED_ALL', 'DIRECT') or (focal and arm in ('NO_PRED', 'MATCHED_FORGE_IO'))): continue
        if pr and focal and arm == 'PRED_MASK': nr['P'] = markers['prediction_withheld']; ch = True
        if pr and focal and arm == 'PLACEBO_PRED':
            if u == r['P'] or any(x['kind'] == 'OBSERVED_OUTCOME' and x.get('t') == focus_t and x['O'] == u for x in records):
                raise RuntimeError('PLACEBO_U_ASSERTION u == p or u == o')
            nr['P'] = u; ch = True
        if pr and (arm == 'PLACEBO_PRED_ALL' or (focal and arm == 'CYCLIC_PRED')): nr['P'] = outs[(outs.index(r['P']) + 1) % len(outs)]; ch = True
        if r['kind'] == 'OBSERVED_OUTCOME' and focal and arm == 'FACTUAL_DELETED': nr['O'] = markers['outcome_withheld']; ch = True
        if r['kind'] == 'OBSERVED_OUTCOME' and focal and arm == 'CF_OUTCOME': nr['O'] = cf; ch = True
        nr['src'] = i; nr['changed'] = ch; res.append(nr)
    return res

def twin_verdict_npdm(tw):
    """Pre-outcome twin canary. tw must contain all four keys; anything missing / partial -> never PASS."""
    keys = ('raw_identical', 'intent_tensor_seal_identical', 'prediction_tensor_seal_identical', 'futures_differ')
    if not tw or not tw.get('applicable'): return 'INCONCLUSIVE', 'NO_VALID_ACT_OR_ACQUIRE_FIRST_DECISION'
    if any(k not in tw for k in keys): return 'INCONCLUSIVE', 'TWIN_METADATA_INCOMPLETE'
    if all(tw[k] is True for k in keys): return 'PASS', 'IDENTICAL_PRE_OUTCOME_STATE_DIFFERENT_FUTURES'
    return 'FAIL', 'MISMATCH:' + ','.join(k for k in keys if tw[k] is not True)

# ------------------------------------------------------------------------------- offline evaluator (public Bayes only)
def facts_npdm(records, outcomes=None):
    # observed (action, outcome) pairs: prefix observations + observed outcomes of ACQUIRE/ACT intents (same step); with
    # 'outcomes' given, only public outcome names count (OUTCOME_WITHHELD / OUTCOME_PENDING are not facts)
    F = set(); intent = {}
    for r in records:
        if r['kind'] == 'PRIOR_OBSERVATION': F.add((r['A'], r['O']))
        if r['kind'] == 'MODEL_INTENT': intent[r['t']] = r['A']
        if r['kind'] == 'OBSERVED_OUTCOME' and r['t'] in intent and r['O'] not in (STATUS_MARKERS_NPDM['pending'],) and (outcomes is None or r['O'] in outcomes):
            F.add((intent[r['t']], r['O']))
    return frozenset(F)

def bayes_npdm(contract, F, left):
    """Exact public-Bayes values under the uniform prior over the bijections consistent with F. Returns {decision: Q} for
    ACT a / ACQUIRE a / STOP, plus 'WASTE' (invalid / abstain: a decision is consumed) and the optimal set (tol 1e-9)."""
    acts, outs, g, c = list(contract['actions']), list(contract['outcomes']), contract['goal'], float(contract['cost'])
    maps = [dict(zip(acts, p)) for p in _it.permutations(outs)]
    memo = {}
    def cons(Fs): return [m for m in maps if all(m[a] == o for a, o in Fs)]
    def V(Fs, b):
        if b <= 0: return 0.0
        k = (Fs, b)
        if k in memo: return memo[k]
        v = max(Q(Fs, b).values()); memo[k] = v; return v
    def Q(Fs, b):
        ms = cons(Fs); q = {'STOP': 0.0}
        for a in acts:
            q[('ACT', a)] = sum(1.0 for m in ms if m[a] == g) / len(ms)
            q[('ACQUIRE', a)] = -c + sum(V(frozenset(Fs | {(a, m[a])}), b - 1) for m in ms) / len(ms)
        return q
    q = Q(frozenset(F), left); q['WASTE'] = V(frozenset(F), left - 1); best = max(v for k, v in q.items() if k != 'WASTE')
    return {'Q': q, 'V': best, 'optimal': sorted([k for k, v in q.items() if k != 'WASTE' and abs(v - best) < 1e-9], key=str)}

def decision_key_npdm(p):
    if p['status'] == 'VALID': return (p['kind'], p['action'])
    if p['status'] == 'STOP': return 'STOP'
    return 'WASTE'

def eligible_states_npdm(episodes):
    """Pre-registered: in every episode, the FIRST decision t+1 that follows an ACQUIRE at step t whose prediction was
    VALID and differs from the observed outcome (a natural, model-generated discrepancy). At most one state per episode."""
    out = []
    for eid, ep in episodes.items():
        tr = ep['trace']
        for i, st in enumerate(tr[:-1]):
            p = st['parsed']
            if p['status'] == 'VALID' and p['kind'] == 'ACQUIRE' and p['pred_status'] == 'VALID' and st.get('outcome') and p['prediction'] != st['outcome']:
                out.append({'eid': eid, 'discrepancy_t': st['t'], 'decision_t': tr[i + 1]['t'], 'predicted': p['prediction'], 'observed': st['outcome']})
                break
    return out

def gate2_npdm(states):
    """states: dicts with 'z' {arm: decision key or None}, 'optimal' (real facts), 'optimal_fd' (facts without the focal
    outcome), 'optimal_cf' (counterfactual facts, None if CF not applicable), 'q' / 'q_fd' (public Q-values, str keys),
    'cyclic_collision' (diagnostic rotation == observed).
    (a) causal effect of the FOCAL prediction: NPDM differs from BOTH focal absence controls (NO_PRED and PRED_MASK).
    (b) direction: NPDM in the optimal set while both focal absence controls are not (correct) / the reverse (wrong).
    Claims, judged separately:
      C1  raw-decision specificity: the focal prediction changed the next decision into the optimal set, and the
          outcome-conditioned placebo u produced a DIFFERENT raw decision (placebo may still be optimal);
      C1b correctness specificity (reported, never required): in addition the placebo decision is NOT optimal;
      C2  outcome dependence: CF_OUTCOME discriminating AND tracked;
      C3a outcome-deletion sensitivity (reported only): FACTUAL_DELETED changed the decision;
      C3b corrective factual necessity: fd_decision_required AND fd_changed AND fd_in_optimal_fd.
    A correct state with fd_decision_required and fd_changed but the FD decision outside optimal_fd is a WRONG
    CORRECTION -> FAIL (pre-registered; applies to every correct state). fd_decision_required=False -> C3b NOT_TESTABLE.
    Full SMOKE_CAUSAL_PASS only if C1, C2 and C3b hold in EVERY correct state; otherwise (with C1) SMOKE_CAUSAL_PASS_LIMITED.
    The full verdict is a RAW-DECISION specificity claim; C1b is shown next to it. Rule order: see the branches."""
    rows = []
    S = lambda O: set(map(str, O or []))
    for s in states:
        z, O = s['z'], S(s['optimal']); ins = lambda a: str(z.get(a)) in O
        eff = z['NPDM'] != z['NO_PRED'] and z['NPDM'] != z['PRED_MASK']
        ceiling = ins('NPDM') and ins('NO_PRED') and ins('PRED_MASK')
        correct = eff and ins('NPDM') and not ins('NO_PRED') and not ins('PRED_MASK')
        wrong = eff and not ins('NPDM') and (ins('NO_PRED') or ins('PRED_MASK'))
        Ofd = S(s.get('optimal_fd')); q, qfd = s.get('q') or {}, s.get('q_fd') or {}
        cf_app = s.get('optimal_cf') is not None and z.get('CF_OUTCOME') is not None
        cf_disc = cf_app and S(s['optimal_cf']) != O
        pl_av = z.get('PLACEBO_PRED') is not None; cy_av = z.get('CYCLIC_PRED') is not None
        rows.append(dict(eid=s['eid'], effect=eff, correct=correct, wrong=wrong, ceiling=ceiling,
                         placebo_available=pl_av, placebo_same=pl_av and z['PLACEBO_PRED'] == z['NPDM'],
                         placebo_changed=pl_av and z['PLACEBO_PRED'] != z['NPDM'], placebo_optimal=pl_av and ins('PLACEBO_PRED'),
                         cyclic_available=cy_av, cyclic_collision=bool(s.get('cyclic_collision')), cyclic_same=cy_av and z['CYCLIC_PRED'] == z['NPDM'],
                         fd_q_changed=any(abs(q.get(k, 0.0) - qfd.get(k, 0.0)) > 1e-12 for k in set(q) | set(qfd)),
                         fd_optset_changed=O != Ofd, fd_disjoint=not (O & Ofd),
                         fd_decision_required=str(z['NPDM']) not in Ofd,          # chosen decision is not optimal without the outcome
                         fd_changed=z['FACTUAL_DELETED'] != z['NPDM'], fd_in_optimal_fd=str(z['FACTUAL_DELETED']) in Ofd,
                         fd_corrective=(str(z['NPDM']) not in Ofd) and z['FACTUAL_DELETED'] != z['NPDM'] and str(z['FACTUAL_DELETED']) in Ofd,
                         fd_wrong_correction=(str(z['NPDM']) not in Ofd) and z['FACTUAL_DELETED'] != z['NPDM'] and str(z['FACTUAL_DELETED']) not in Ofd,
                         cf_applicable=cf_app, cf_discriminating=cf_disc, cf_tracks=(str(z.get('CF_OUTCOME')) in S(s.get('optimal_cf'))) if cf_app else None,
                         matched_equals_nopred=z['MATCHED_FORGE_IO'] == z['NO_PRED'], order_perm_same=z['ORDER_PERM'] == z['NPDM'],
                         marker_or_geometry_effect=z['PRED_MASK'] != z['NO_PRED'], direct_format_effect=z['DIRECT'] != z['NO_PRED_ALL'],
                         all_history_effect=z['NPDM'] != z['NO_PRED_ALL'], all_history_placebo_same=z['PLACEBO_PRED_ALL'] == z['NPDM']))
    n = len(rows); nc = sum(r['correct'] for r in rows); ne = sum(r['effect'] for r in rows)
    cnt = lambda k, rs=None: sum(1 for r in (rows if rs is None else rs) if r[k])
    res = {'n_eligible': n, 'n_effect': ne, 'n_correct': nc, 'n_wrong': sum(r['wrong'] for r in rows),
           'n_ceiling': sum(r['ceiling'] for r in rows), 'rows': rows, 'flags': [],
           'counts': {k: cnt(k) for k in ('cf_applicable', 'cf_discriminating', 'cf_tracks', 'fd_q_changed', 'fd_optset_changed', 'fd_disjoint',
                                           'fd_decision_required', 'fd_changed', 'fd_in_optimal_fd', 'fd_corrective', 'fd_wrong_correction',
                                           'placebo_available', 'placebo_same', 'placebo_changed',
                                           'placebo_optimal', 'cyclic_collision', 'cyclic_same')},
           'cyclic_strata': {'collision': {'n': cnt('cyclic_collision'), 'same': sum(1 for r in rows if r['cyclic_collision'] and r['cyclic_same'])},
                             'no_collision': {'n': n - cnt('cyclic_collision'), 'same': sum(1 for r in rows if not r['cyclic_collision'] and r['cyclic_same'])}},
           'claims': {'C1_raw_decision_specificity': 'NOT_DEMONSTRATED', 'C1b_correctness_specificity': 'NOT_DEMONSTRATED',
                      'C2_outcome_dependence': 'NOT_DEMONSTRATED', 'C3a_outcome_deletion_sensitivity': 'NOT_DEMONSTRATED',
                      'C3b_corrective_factual_necessity': 'NOT_DEMONSTRATED'}}
    def fin(v, why): res.update(verdict=v, reason=why); return res
    if n < 2: return fin('INCONCLUSIVE', 'FEWER_THAN_2_ELIGIBLE_STATES')
    if any(r['wrong'] for r in rows): return fin('FAIL', 'WRONG_DIRECTION_CHANGE')
    if ne == 0:
        if all(r['ceiling'] for r in rows): return fin('INCONCLUSIVE', 'CEILING_NO_PRED_ALREADY_OPTIMAL')
        return fin('FAIL', 'NO_CAUSAL_EFFECT_OF_PREDICTION')
    usable = [r for r in rows if r['effect'] and r['placebo_available']]
    if usable and all(r['placebo_same'] for r in usable): return fin('FAIL', 'PLACEBO_REPRODUCES_EFFECT')
    cr = [r for r in rows if r['correct']]; req = [r for r in cr if r['fd_decision_required']]
    if len(req) >= 2 and all(not r['fd_changed'] for r in req): return fin('FAIL', 'EFFECT_WITHOUT_OBSERVED_OUTCOME')
    if any(r['fd_wrong_correction'] for r in cr): return fin('FAIL', 'WRONG_CORRECTION_AFTER_FACTUAL_DELETION')
    noncei = [r for r in rows if not r['ceiling']]
    if not (nc >= 2 and all(r['correct'] for r in noncei)): return fin('INCONCLUSIVE', 'MIXED_OR_INSUFFICIENT_CORRECT_DIRECTION')
    if any(not r['placebo_available'] for r in cr): return fin('INCONCLUSIVE', 'PLACEBO_U_UNAVAILABLE')
    if any(r['placebo_same'] for r in cr): return fin('INCONCLUSIVE', 'PLACEBO_NOT_SPECIFIC_IN_SOME_STATE')
    if any(r['fd_decision_required'] and not r['fd_changed'] for r in cr): return fin('INCONCLUSIVE', 'OUTCOME_NOT_NECESSARY_IN_SOME_STATE')
    if any(r['cf_discriminating'] and not r['cf_tracks'] for r in cr): return fin('INCONCLUSIVE', 'COUNTERFACTUAL_OUTCOME_NOT_TRACKED')
    tri = lambda k: 'DEMONSTRATED_IN_SMOKE' if all(r[k] for r in cr) else ('PARTIAL_%d_OF_%d' % (cnt(k, cr), len(cr)) if any(r[k] for r in cr) else 'NOT_TESTED')
    po = cnt('placebo_optimal', cr)
    res['claims'] = {'C1_raw_decision_specificity': 'DEMONSTRATED_IN_SMOKE',
                     'C1b_correctness_specificity': 'DEMONSTRATED_IN_SMOKE' if po == 0 else 'NOT_DEMONSTRATED_PLACEBO_OPTIMAL_IN_%d_OF_%d' % (po, len(cr)),
                     'C2_outcome_dependence': tri('cf_discriminating'), 'C3a_outcome_deletion_sensitivity': tri('fd_changed'),
                     'C3b_corrective_factual_necessity': tri('fd_corrective')}
    res['c3b_not_testable_states'] = sum(1 for r in cr if not r['fd_decision_required'])
    res['flags'] = [('ORDER_SENSITIVE' if any(not r['order_perm_same'] for r in rows) else 'ORDER_INVARIANT_IN_SMOKE'),
                    'PLACEBO_OUTCOME_CONDITIONED_OFFLINE', 'CF_RESULTS_APPLY_TO_TESTED_SUBSET_ONLY', 'FULL_VERDICT_IS_RAW_DECISION_SPECIFICITY']
    if res['claims']['C2_outcome_dependence'] == res['claims']['C3b_corrective_factual_necessity'] == 'DEMONSTRATED_IN_SMOKE':
        return fin('SMOKE_CAUSAL_PASS', 'C1_C2_C3B_DEMONSTRATED_IN_EVERY_CORRECT_STATE')
    return fin('SMOKE_CAUSAL_PASS_LIMITED', 'C1_DEMONSTRATED_C2_OR_C3B_NOT_DEMONSTRATED_IN_EVERY_CORRECT_STATE')

def gate3_npdm(first):
    """first: list of dicts with Q (decision -> public value), optimal set, z_pred, z_direct, cost, kind label.
    Supporting only; never replaces Gate-2."""
    n = len(first); val = lambda f, z: f['Q'].get(z, f['Q']['WASTE']) if z != 'WASTE' else f['Q']['WASTE']
    opt_p = sum(str(f['z_pred']) in set(map(str, f['optimal'])) for f in first)
    opt_d = sum(str(f['z_direct']) in set(map(str, f['optimal'])) for f in first)
    u_p = sum(val(f, f['z_pred']) for f in first); u_d = sum(val(f, f['z_direct']) for f in first)
    acq_bad = [f['label'] for f in first if f['must_not_acquire'] and isinstance(f['z_pred'], tuple) and f['z_pred'][0] == 'ACQUIRE']
    collapse = len({str(f['z_pred']) for f in first}) == 1 and n > 1
    res = {'n': n, 'optimal_pred_grammar': opt_p, 'optimal_direct': opt_d, 'utility_pred_grammar': u_p, 'utility_direct': u_d,
           'forbidden_acquire': acq_bad, 'collapse': collapse}
    if u_p < u_d - 1e-12 or acq_bad or collapse: res['verdict'] = 'FAIL'
    elif opt_p >= max(5, n - 2) and opt_p - opt_d >= 2: res['verdict'] = 'PASS_SUPPORT'
    else: res['verdict'] = 'INCONCLUSIVE_SUPPORT'
    return res

FAILURE_POINT_NPDM = {
    'C1_C2_C3B_DEMONSTRATED_IN_EVERY_CORRECT_STATE': 'none in this smoke (only a canary; raw-decision specificity only; a pre-registered paired cohort is the next step)',
    'C1_DEMONSTRATED_C2_OR_C3B_NOT_DEMONSTRATED_IN_EVERY_CORRECT_STATE': 'prediction effect shown, but outcome dependence (C2) or corrective factual necessity (C3b) is not demonstrated in every correct state (see claims)',
    'WRONG_CORRECTION_AFTER_FACTUAL_DELETION': 'without the observed outcome the decision changed, but to a decision that is NOT optimal for the remaining facts',
    'PLACEBO_U_UNAVAILABLE': 'technical: the outcome-conditioned placebo u (u != p, u != o) could not be built; no fallback',
    'FEWER_THAN_2_ELIGIBLE_STATES': 'too few natural wrong-predicted ACQUIRE steps: the model rarely ACQUIREd or its predictions were right',
    'WRONG_DIRECTION_CHANGE': 'the prediction record pulled the decision AWAY from what the observed outcome requires (prediction bias)',
    'CEILING_NO_PRED_ALREADY_OPTIMAL': 'facts alone already gave the optimal decision; the prediction record had nothing to fix',
    'NO_CAUSAL_EFFECT_OF_PREDICTION': 'the prediction record did not change the next decision (native readout ignores it)',
    'PLACEBO_REPRODUCES_EFFECT': 'the change is not content-specific: the other wrong prediction (placebo u) does the same',
    'EFFECT_WITHOUT_OBSERVED_OUTCOME': 'the change does not depend on the observed outcome (prediction alone drives it)',
    'PLACEBO_NOT_SPECIFIC_IN_SOME_STATE': 'in some correct state the placebo prediction produced the same decision',
    'OUTCOME_NOT_NECESSARY_IN_SOME_STATE': 'in some correct state the chosen decision is not optimal without the observed outcome, yet deleting it did not change the decision',
    'COUNTERFACTUAL_OUTCOME_NOT_TRACKED': 'with a different (public-consistent) observed outcome the decision did not follow the new optimal set',
    'MIXED_OR_INSUFFICIENT_CORRECT_DIRECTION': 'mixed effects: some changes not in the correct direction',
    'GATE1_NOT_PASS': 'runtime / provenance / reload / geometry gate did not pass; no causal reading'}

def answers_npdm(gates, g2, g3):
    phys = ('G0_P0_A_PARITY', 'G0_P0_B_PARITY', 'G1_REBUILD_FROM_SSD', 'P1_PHYSICAL', 'P7_INTEGRITY')
    rows = g2.get('rows') or []
    return {
        'Q1_physical_memory_worked': {'answer': all(gates.get(g) == 'PASS' for g in phys), 'gates': {g: gates.get(g) for g in phys}},
        'Q2_prediction_sealed_before_outcome': {'answer': gates.get('G1_LIVE_EPISODES') == 'PASS' and gates.get('G1_PRE_OUTCOME_TWIN') == 'PASS',
                                                'gates': {g: gates.get(g) for g in ('G1_LIVE_EPISODES', 'G1_PRE_OUTCOME_TWIN', 'G1_PENDING')}},
        'Q3_prediction_record_changed_next_decision': {'states_with_effect': g2.get('n_effect'), 'eligible_states': g2.get('n_eligible')},
        'Q4_change_in_direction_required_by_observed_outcome': {'correct': g2.get('n_correct'), 'wrong': g2.get('n_wrong'), 'ceiling': g2.get('n_ceiling'),
                                                                'fd_corrective': (g2.get('counts') or {}).get('fd_corrective'),
                                                                'fd_wrong_correction': (g2.get('counts') or {}).get('fd_wrong_correction'),
                                                                'c3b_not_testable_states': g2.get('c3b_not_testable_states')},
        'Q5_raw_decision_specificity_vs_placebo': {'claim_scope': 'raw-decision specificity; correctness specificity = C1b', 'placebo_u_reproduced': sum(1 for r in rows if r['placebo_same'] and r['effect']), 'effects': g2.get('n_effect'),
                                           'placebo_u_optimal': sum(1 for r in rows if r.get('placebo_optimal') and r['effect']),
                                           'cyclic_diagnostic_strata': g2.get('cyclic_strata'), 'claims': g2.get('claims')},
        'Q6_policy_support_gate3': g3.get('verdict'),
        'Q7_most_likely_failure_point': FAILURE_POINT_NPDM.get(g2.get('reason'), g2.get('reason'))}

# ======================================================================================================== RUN
try:
    log('=' * 112); log(MARKER, RUN_ID, '| engine commit', COMMIT, '| continuation of TEST893 (FAIL_NO_GAIN, unchanged)')
    log('SCOPE: feasibility only. PASS != learning / semantic reading / native behaviour / autonomy.'); log('=' * 112)
    log('TOLERANCES', json.dumps(TOL, sort_keys=True), 'sha256', R['tolerances_sha256'])
    # executed-cell identity, single cell. MANDATORY EXTERNAL PIN (fail-closed). The cell never trusts a moving name (main,
    # HEAD, last-touch) and never embeds a hash of itself. The expected identity comes from OUTSIDE the cell, as one string
    #   NPDM_PIN = 'commit=<40 hex>;path=897npdm_smoke.py;blob=<40 hex>;sha256=<64 hex>;bytes=<int>'
    # read from the Colab secret NPDM_PIN (google.colab.userdata) or, if that is unavailable, the environment variable
    # NPDM_PIN; if both exist they must be identical. The values are the ones the independent audit computed for the
    # published commit. Every check below must hold, otherwise the run stops HERE, before ENV / model load / any GPU work:
    #   pin present and well-formed; path == SRC_FILE exactly (no other file, no case variant, no absolute path, no '..',
    #   no directory, no backslash); the pinned commit object exists (fetched by SHA if needed); its tree has exactly one
    #   entry at that literal path, a regular file (mode 100644/100755, type blob; a submodule / symlink / tree is refused)
    #   whose object id == pinned blob; git blob id recomputed over the fetched bytes == pinned blob; SHA-256 == pinned;
    #   byte count == pinned; the raw channel at the pinned commit is byte-identical; the executed cell (IPython history)
    #   equals the pinned bytes after ONE canonicalization only: leading and trailing b'\n' removed on both sides (run
    #   20261118T014044Z: a pasted cell gained one leading newline and lost the final one). Interior bytes, CRLF and spaces
    #   are compared exactly. Whether main still points at the pinned commit is recorded, never used as trust.
    SRC_REPO = 'ceceli33/titan-cognitive-core-v3'; SRC_FILE = '897npdm_smoke.py'
    ec = {'status': 'NOT_CAPTURED', 'identity_match': False, 'src_file': SRC_FILE, 'checks': {}}
    _ck = ec['checks']
    try:
        _hist = list(globals()['get_ipython']().history_manager.input_hist_raw)
        _cell = [x for x in _hist if MARKER in x and 'def integrity_selftest' in x][-1]
        (ROOT / 'NPDM_SMOKE_cell_source.py').write_text(_cell, encoding='utf-8'); _cb = _cell.encode('utf-8')
        ec.update(status='CAPTURED', sha256=sha_bytes(_cb), git_blob=gitblob(_cb), git_blob_with_final_newline=gitblob(_cb + b'\n'),
                  lines=_cell.count('\n') + 1, file=str(ROOT / 'NPDM_SMOKE_cell_source.py'))
    except Exception as e:
        ec['capture_error'] = '%s: %s' % (type(e).__name__, e)
    _ck['cell_captured'] = ec['status'] == 'CAPTURED'
    # ---- external pin
    _pins = {}
    try:
        from google.colab import userdata as _ud
        _v = _ud.get('NPDM_PIN')
        if _v: _pins['colab_secret'] = _v.strip()
    except Exception as e:
        ec['pin_colab_error'] = '%s: %s' % (type(e).__name__, str(e)[:120])
    if os.environ.get('NPDM_PIN'): _pins['environment'] = os.environ['NPDM_PIN'].strip()
    ec['pin_channels'] = sorted(_pins)
    _ck['pin_present'] = bool(_pins)
    _ck['pin_channels_agree'] = len(set(_pins.values())) <= 1
    _PIN_RX = r'commit=([0-9a-f]{40});path=([^;]+);blob=([0-9a-f]{40});sha256=([0-9a-f]{64});bytes=([1-9][0-9]{0,9})'
    _m = re.fullmatch(_PIN_RX, next(iter(_pins.values()))) if _pins and _ck['pin_channels_agree'] else None
    _ck['pin_well_formed'] = _m is not None
    pin = dict(zip(('commit', 'path', 'blob', 'sha256', 'bytes'), _m.groups())) if _m else None
    if pin: pin['bytes'] = int(pin['bytes'])
    ec['pin'] = pin
    _ck['pin_path_is_src_file'] = bool(pin) and pin['path'] == SRC_FILE and '/' not in pin['path'] and '\\' not in pin['path'] and '..' not in pin['path']
    if all(_ck.values()):
        try:
            _gd = ROOT.parent / ('NPDM_SMOKE_srcid_' + RUN_ID); _genv = dict(os.environ, GIT_TERMINAL_PROMPT='0')
            _git = lambda *a: subprocess.run(['git', '--literal-pathspecs'] + list(a), check=True, capture_output=True, timeout=180, env=_genv).stdout
            _url = 'https://github.com/' + SRC_REPO
            _git('clone', '-q', '--filter=blob:none', '--no-checkout', _url, str(_gd))
            try: _t = _git('-C', str(_gd), 'cat-file', '-t', pin['commit']).decode().strip()
            except subprocess.CalledProcessError:
                _git('-C', str(_gd), 'fetch', '-q', '--filter=blob:none', 'origin', pin['commit'])
                _t = _git('-C', str(_gd), 'cat-file', '-t', pin['commit']).decode().strip()
            _ck['commit_object_exists'] = _t == 'commit'
            _ent = [e for e in _git('-C', str(_gd), 'ls-tree', '-z', pin['commit'], '--', SRC_FILE).decode('utf-8', 'replace').split('\0') if e]
            ec['tree_entries'] = _ent
            _meta, _, _pth = (_ent[0].partition('\t') if len(_ent) == 1 else ('', '', ''))
            _mode, _typ, _oid = (_meta.split(' ') + ['', '', ''])[:3]
            _ck['tree_single_entry_exact_path'] = len(_ent) == 1 and _pth == SRC_FILE
            _ck['tree_entry_regular_file'] = _mode in ('100644', '100755') and _typ == 'blob'
            _ck['tree_blob_equals_pin'] = _oid == pin['blob']
            _pb = _git('-C', str(_gd), 'cat-file', 'blob', _oid) if _ck['tree_entry_regular_file'] else b''
            _ck['recomputed_blob_equals_pin'] = gitblob(_pb) == pin['blob']
            _ck['sha256_equals_pin'] = sha_bytes(_pb) == pin['sha256']
            _ck['bytes_equal_pin'] = len(_pb) == pin['bytes']
            with urllib.request.urlopen(urllib.request.Request('https://raw.githubusercontent.com/%s/%s/%s' % (SRC_REPO, pin['commit'], SRC_FILE),
                                                               headers={'User-Agent': 'AKBASCORE-NPDM_SMOKE'}), timeout=120) as f_:
                _rb = f_.read()
            _ck['raw_channel_equal'] = _rb == _pb
            try:
                _git('-C', str(_gd), 'merge-base', '--is-ancestor', pin['commit'], 'origin/HEAD'); _anc = True
            except subprocess.CalledProcessError: _anc = False
            ec['published'] = {'repo': SRC_REPO, 'commit': pin['commit'], 'path': SRC_FILE, 'tree_mode': _mode, 'tree_blob': _oid,
                               'blob_of_bytes': gitblob(_pb), 'sha256': sha_bytes(_pb), 'bytes': len(_pb),
                               'commit_reachable_from_default_branch_RECORD_ONLY': _anc}
            ec['canonicalization'] = "strip leading/trailing b'\\n' on both sides only; interior bytes compared exactly"
            if ec['status'] == 'CAPTURED':
                _cc, _pc = _cb.strip(b'\n'), _pb.strip(b'\n')
                _ck['executed_cell_equals_pinned_bytes'] = bool(_pb) and _cc == _pc
                ec['boundary_newlines'] = {'cell_leading': len(_cb) - len(_cb.lstrip(b'\n')), 'cell_trailing': len(_cb) - len(_cb.rstrip(b'\n')),
                                           'published_leading': len(_pb) - len(_pb.lstrip(b'\n')), 'published_trailing': len(_pb) - len(_pb.rstrip(b'\n'))}
                if _cc != _pc:
                    _i = next((k for k in range(min(len(_cc), len(_pc))) if _cc[k] != _pc[k]), min(len(_cc), len(_pc)))
                    ec['first_difference'] = {'offset_after_canonicalization': _i, 'line': _cc[:_i].count(b'\n') + 1,
                                              'cell_bytes': _cc[_i:_i + 40].decode('utf-8', 'replace'), 'published_bytes': _pc[_i:_i + 40].decode('utf-8', 'replace')}
            shutil.rmtree(_gd, ignore_errors=True)
        except Exception as e:
            ec['published_error'] = '%s: %s' % (type(e).__name__, str(e)[:300]); _ck['repository_checks_completed'] = False
    _REQ = ('cell_captured', 'pin_present', 'pin_channels_agree', 'pin_well_formed', 'pin_path_is_src_file', 'commit_object_exists',
            'tree_single_entry_exact_path', 'tree_entry_regular_file', 'tree_blob_equals_pin', 'recomputed_blob_equals_pin',
            'sha256_equals_pin', 'bytes_equal_pin', 'raw_channel_equal', 'executed_cell_equals_pinned_bytes')
    ec['failed_checks'] = [k for k in _REQ if _ck.get(k) is not True] + [k for k, v in _ck.items() if k not in _REQ and v is not True]
    ec['identity_match'] = not ec['failed_checks']
    R['executed_cell'] = ec
    log('EXECUTED_CELL', json.dumps(R['executed_cell']))
    if not ec['identity_match']:                         # fail-closed BEFORE ENV, the model load and any GPU work
        raise StopT896('SOURCE_IDENTITY_MISMATCH %s' % json.dumps({k: ec.get(k) for k in ('status', 'failed_checks', 'capture_error', 'pin_colab_error', 'published_error', 'first_difference')}, default=str))
    # ---------------------------------------------------------------------------------------------------- ENV
    env = {'python': platform.python_version(), 'torch': torch.__version__, 'cuda': torch.version.cuda,
           'transformers': transformers.__version__, 'accelerate': accelerate.__version__, 'bitsandbytes': bitsandbytes.__version__,
           'cuda_available': torch.cuda.is_available(), 'device_count': torch.cuda.device_count()}
    if env['cuda_available']:
        pr = torch.cuda.get_device_properties(0)
        env.update(gpu=torch.cuda.get_device_name(0), gpu_bytes=int(pr.total_memory), compute_capability=[pr.major, pr.minor])
    # full runtime manifest (record, not a new lock): the four pinned packages are enforced above; the transitive ones that
    # matter for tokenisation / loading are logged so a run can be compared with TEST895's working combination
    R['runtime_manifest'] = {d_.metadata['Name']: d_.version for d_ in importlib.metadata.distributions() if d_.metadata['Name']}
    env['transitive'] = {k_: _ver(k_) for k_ in ('tokenizers', 'huggingface-hub', 'safetensors', 'numpy', 'sentencepiece', 'regex')}
    R['env'] = env; log('ENV', json.dumps(env))
    env_ok = (env['cuda_available'] and env['device_count'] == 1 and env.get('gpu') == GPU_NAME_REQ and
              tuple(env.get('compute_capability', ())) == GPU_CC_REQ and env.get('gpu_bytes', 0) >= 79 * 2**30)
    gate('ENV', 'PASS' if env_ok else 'FAIL', None if env_ok else 'requires exactly one %s (cc %s)' % (GPU_NAME_REQ, GPU_CC_REQ), **env)
    random.seed(SEED); torch.manual_seed(SEED); torch.cuda.manual_seed_all(SEED)
    # Drive early (TEST870 method): mounted before the long model load so log + JSON are backed up after every gate
    try:
        from google.colab import drive as _gdrive
        _gdrive.mount('/content/drive'); DRIVE_DIR = '/content/drive/MyDrive/NPDM_SMOKE_' + RUN_ID; os.makedirs(DRIVE_DIR, exist_ok=True)
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
                                                           headers={'User-Agent': 'AKBASCORE-NPDM_SMOKE'}), timeout=120) as f_:
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
    # transformers 5.22.1 leaves config._commit_hash empty (NPDM_SMOKE run 20261118T014044Z: null). Revision evidence is therefore:
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
    # ======================================================================================== NPDM smoke experiment
    T_EXP = time.perf_counter(); R['model_load_s'] = round(T_EXP - T0, 1)
    METRICS = {'forge_s': [], 'append_s': [], 'reload_s': [], 'query_s': [], 'mount_tokens': [], 'episode_elapsed_s': {}}
    def _cpu_ram_frac():
        try:
            mi = {l.split(':')[0]: int(l.split()[1]) for l in open('/proc/meminfo') if l.split(':')[0] in ('MemTotal', 'MemAvailable')}
            return 1.0 - mi['MemAvailable'] / mi['MemTotal']
        except Exception: return 0.0
    def guard(op, dt=None):
        # pre-registered abort limits -> TECHNICAL_INCOMPLETE (no scientific result); checked after every expensive operation
        why = []
        if time.perf_counter() - T_EXP > ABORT['experiment_wall_s']: why.append('EXPERIMENT_WALL')
        if torch.cuda.max_memory_allocated() / 2**30 > ABORT['gpu_peak_gib']: why.append('GPU_PEAK')
        if sum(Path(e['file']).stat().st_size for e in CART_INDEX) / 2**30 > ABORT['cartridge_bytes_gib']: why.append('CARTRIDGE_BYTES')
        if _cpu_ram_frac() > ABORT['cpu_ram_frac']: why.append('CPU_RAM')
        if dt is not None and op == 'query' and dt > ABORT['query_s']: why.append('QUERY_TIME')
        if dt is not None and op in ('forge', 'append') and dt > ABORT['forge_append_s']: why.append('FORGE_APPEND_TIME')
        if why: raise StopT896('ABORT_TECHNICAL_INCOMPLETE %s at %s' % (why, op))
    def tok_ids(s): return list(tok(s, add_special_tokens=False).input_ids)
    def ntok(s): return len(tok_ids(s))
    _free = shutil.disk_usage(str(ROOT)).free / 2**30; R['disk_free_gib_before_experiment'] = round(_free, 1)
    if _free < ABORT['disk_free_min_gib']: raise StopT896('ABORT_TECHNICAL_INCOMPLETE DISK_FREE_%.1f_GIB' % _free)
    # ------------------------------------------------------------------ G0 MANIFEST: public contract + sealed vault commitment
    MK = choose_markers_npdm(ntok)
    PUB, VAULT = make_episodes_npdm(SEED + 897, ntok, MK)
    _vb = json.dumps(VAULT, sort_keys=True, default=str).encode(); VAULT_COMMIT = sha_bytes(_vb)   # hash only, file at the end
    _gram = ['ACQUIRE %s PREDICTION %s' % (a, o) for p_ in PUB.values() for a in p_['actions'] for o in p_['outcomes']]
    MAX_NEW = max(ntok(x) for x in _gram) + PROTO['max_new_margin_tokens']      # fixed BEFORE the first generation
    qs_all = [query_npdm(contract_npdm(p_), l_, g_, r_) for p_ in PUB.values() for l_ in range(1, 5) for g_ in ('PRED', 'DIRECT') for r_ in (0, 1)]
    indep = [e for e, k, c, r in EPISODE_PLAN_NPDM if not (r and r.startswith('SAME_AS'))]
    names_ = [n for e in indep for n in list(PUB[e]['actions']) + list(PUB[e]['outcomes'])]
    mkn = [MK[k] for k in ('prediction_withheld', 'outcome_withheld')]
    _static = {}
    for fn_ in ('contract_npdm', 'query_npdm', 'segments_npdm', 'record_ids_npdm', 'parse_npdm', 'run_episode_npdm'):
        _co = globals()[fn_].__code__; _nm = set(_co.co_names) | set(_co.co_varnames) | {c for c in _co.co_consts if isinstance(c, str)}
        for c_ in _co.co_consts:
            if hasattr(c_, 'co_names'): _nm |= set(c_.co_names) | set(c_.co_varnames)
        _static[fn_] = sorted({w for w in LEAK_NAMES_NPDM for n_ in _nm if isinstance(n_, str) and w in n_.lower()})
    wm = {'names_unique_disjoint': len(names_) == len(set(names_)),
          'no_name_contains_another': not any(a != b and a in b for a in names_ + mkn for b in names_),
          'field_lengths': all(ntok(n) == MK['field_ntok'] for n in names_ + mkn),
          'names_decode_roundtrip': all(tok.decode(tok_ids(n)) == n for n in names_ + mkn),
          'record_heads_constant_per_kind': all(len({len(tok_ids(seg_.format(t=t_, K=k_))) for t_ in range(0, 5)}) == 1
                                                for kind_, tpl_ in REC_TPL_NPDM.items() for seg_ in tpl_ if '{' in seg_ and seg_ not in ('{A}', '{O}', '{P}', '{S}')
                                                for k_ in ('ACT', 'ACQUIRE')),
          'queries_no_episode_id_or_evaluator_words': not any(re.search(r'produces outcome|observed outcome|vault|seed|mapping|PLACEBO|NO_PRED|MASK|\b(%s)\b' % '|'.join(PUB), q_, re.I) for q_ in qs_all),
          'static_leak_canary_runtime_builders': not any(_static.values()),
          'prefix_consistent_with_vault': all(VAULT[e]['mapping'][a] == o for e in PUB for a, o in PUB[e]['prefix'])}
    MANIFEST = {'public_contract': PUB, 'markers': MK, 'record_templates': REC_TPL_NPDM, 'query_template': QUERY_TPL_NPDM,
                'grammar': GRAMMAR_NPDM, 'arms': ARMS_NPDM, 'episode_plan': EPISODE_PLAN_NPDM, 'abort': ABORT, 'protocol': PROTO,
                'max_new_tokens': MAX_NEW, 'evaluator_vault_sha256_commitment': VAULT_COMMIT}
    MANIFEST_PATH = ROOT / 'NPDM_SMOKE_public_manifest_SEALED.json'
    _mb = json.dumps(MANIFEST, sort_keys=True, indent=1, default=str).encode(); MANIFEST_PATH.write_bytes(_mb); MANIFEST_SHA = sha_bytes(_mb)
    R['world_manifest'] = {'file': str(MANIFEST_PATH), 'sha256': MANIFEST_SHA, 'vault_commitment_sha256': VAULT_COMMIT, 'markers': MK,
                           'max_new_tokens': MAX_NEW}
    ev('PUBLIC_MANIFEST_SEALED', sha256=MANIFEST_SHA, vault_commitment=VAULT_COMMIT)
    gate('G0_MANIFEST', 'PASS' if all(wm.values()) else 'FAIL', None if all(wm.values()) else 'failed: ' + ', '.join(k for k, v in wm.items() if not v),
         checks=wm, static_leak=_static, sha256=MANIFEST_SHA)
    # ------------------------------------------------------------------ physical record cartridges (TEST896 functions)
    CART_INDEX = []; R['cartridges'] = CART_INDEX
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
        if sha_path(ent['file']) != ent['sha256']: raise StopT896('CARTRIDGE_FILE_SHA_CHANGED ' + ent['cid'])
        cp = torch.load(ent['file'], map_location='cpu', weights_only=True)
        if seal_cp(cp) != ent['tensor_seal']: raise StopT896('CARTRIDGE_TENSOR_SEAL_CHANGED ' + ent['cid'])
        return cp
    with MountOff(): CP_EMPTY, _s = forge_native([], 'T896_' + RUN_ID + '_EMPTY')
    _pe = CART_DIR / 'T896_EMPTY.pt'; torch.save(CP_EMPTY, _pe)
    EMPTY_ENT = {'cid': 'EMPTY', 'file': str(_pe), 'sha256': sha_path(_pe), 'tensor_seal': seal_cp(CP_EMPTY), 'n': CP_EMPTY['n'], 'role': 'empty'}
    CART_INDEX.append(EMPTY_ENT)
    def mount_from(cps):
        with MountOff():
            mem = list(initialize_native(to_gpu(CP_EMPTY)))
            for cp in cps: mem = list(native_append_direct(list(mem), to_gpu(cp), strict_sha=True))
        return mem
    def gen(mem, q):
        s0 = full_kv_seal(mem)
        with torch.no_grad(): out_ = answer(mem, q)
        if full_kv_seal(mem) != s0: raise StopT896('MOUNT_CHANGED_BY_QUERY')
        return out_
    EMPTY_SEAL = full_kv_seal(mount_from([]))
    def forge_npdm(rec, cid, parents, where, role, query_sha=None):
        # forge_record unchanged; NPDM provenance metadata added to the same index entry (never model-visible)
        ids = record_ids_npdm(rec, tok_ids); t_ = time.perf_counter()
        cp, ent = forge_record(ids, cid, parents.get('global'), role, where)
        dt = time.perf_counter() - t_; METRICS['forge_s'].append(round(dt, 3)); guard('forge', dt)
        ent.update(record_kind=rec['kind'], turn=rec.get('t'), namespace=where.name, factual_parent_sha256=parents.get('factual'),
                   prediction_parent_sha256=parents.get('prediction'), linked_intent_sha256=parents.get('intent'),
                   global_parent_sha256=parents.get('global'), monotonic_ns=time.monotonic_ns(), query_sha256=query_sha)
        ev('CARTRIDGE_PROVENANCE', cid=cid, **{k: ent[k] for k in ('record_kind', 'turn', 'namespace', 'factual_parent_sha256',
                                                                   'prediction_parent_sha256', 'linked_intent_sha256', 'global_parent_sha256')})
        return cp, ent
    def append_live(mem, cp):
        t_ = time.perf_counter()
        with MountOff(): m2 = list(native_append_direct(list(mem), to_gpu(cp), strict_sha=True))
        dt = time.perf_counter() - t_; METRICS['append_s'].append(round(dt, 3)); guard('append', dt); return m2
    def timed_gen(mem, q):
        t_ = time.perf_counter(); o_ = gen(mem, q); dt = time.perf_counter() - t_
        METRICS['query_s'].append(round(dt, 3)); METRICS['mount_tokens'].append(int(mem[0][0].shape[-2])); guard('query', dt); return o_
    # ------------------------------------------------------------------ G0 P0 parity on NPDM record grammar (inherited checks)
    _e0 = PUB['A2']; _a0 = list(_e0['actions']); _o0 = list(_e0['outcomes'])
    _p0recs = [{'kind': 'PRIOR_OBSERVATION', 'A': _a0[0], 'O': _o0[0], 't': 0}, {'kind': 'MODEL_INTENT', 'K': 'ACQUIRE', 'A': _a0[1], 't': 1},
               {'kind': 'MODEL_PREDICTION', 'P': _o0[1], 't': 1}, {'kind': 'OBSERVED_OUTCOME', 'O': _o0[2], 't': 1}]
    body0 = [i for r in _p0recs for i in record_ids_npdm(r, tok_ids)]
    with MountOff(): CP_P0, _ = forge_native(body0, 'T896_' + RUN_ID + '_P0A')
    with MountOff():
        MEM_P0 = list(initialize_native(to_gpu(CP_P0)))
        ids_A = list(PIDS) + body0; cache = None
        for st in range(0, len(ids_A), CHUNK):
            piece = ids_A[st:st + CHUNK]; ensure_room(len(piece) + 512); pos = torch.arange(st, st + len(piece), device=DEV)
            out = model(input_ids=torch.tensor([piece], device=DEV), past_key_values=cache,
                        attention_mask=torch.ones((1, st + len(piece)), device=DEV, dtype=torch.long),
                        position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
            cache = out.past_key_values; del out
        REF_A = [(k.detach().clone(), v.detach().clone()) for k, v in pairs(cache)]; del cache
    lower_cmp = kv_compare(REF_A[:CUT + 1], [(k.to(DEV), v.to(DEV)) for k, v in CP_P0['lower']])
    upper_cmp = kv_compare(REF_A[CUT + 1:], MEM_P0[CUT + 1:])
    st_a = 'PASS' if tri(lower_cmp) == tri(upper_cmp) == 'PASS' else ('FAIL' if 'FAIL' in (tri(lower_cmp), tri(upper_cmp)) else 'INCONCLUSIVE')
    gate('G0_P0_A_PARITY', st_a, 'NPDM record grammar: full-text prefill K/V vs forged lower K/V + native upper rebuild',
         lower_L0_3=lower_cmp, upper_L4_79=upper_cmp, body_tokens=len(body0)); del REF_A, MEM_P0, CP_P0; release()
    with MountOff():
        cpA, _ = forge_native(record_ids_npdm(_p0recs[1], tok_ids), 'T896_' + RUN_ID + '_P0B_A')
        cpB, _ = forge_native(record_ids_npdm(_p0recs[2], tok_ids), 'T896_' + RUN_ID + '_P0B_B')
        memA = list(initialize_native(to_gpu(cpA)))
    if api_err is None:
        with MountOff():
            nat = list(native_append_direct(list(memA), to_gpu(cpB), strict_sha=True)); exp = list(xappend878(ENV, list(memA), to_gpu(cpB), ()))
        cmp_b = kv_compare(nat, exp); gate('G0_P0_B_PARITY', tri(cmp_b), 'prediction record: locked native append (757) vs explicit append (878/877)', compare=cmp_b)
        del nat, exp
    else:
        gate('G0_P0_B_PARITY', 'INCONCLUSIVE', 'api877 installed-source audit failed: ' + api_err)
    del memA, cpA, cpB; release()
    for g_ in GATE0:
        if R['gates'][g_]['status'] != 'PASS': raise StopT896('GATE0_NOT_PASS %s=%s' % (g_, R['gates'][g_]['status']))
    # ------------------------------------------------------------------ G1 parser + ACT/ACQUIRE semantics (pure, in-cell)
    _c = contract_npdm(PUB['L1']); _A = list(_c['actions']); _O = list(_c['outcomes'])
    _fx = [('ACT %s PREDICTION %s' % (_A[0], _O[1]), 'PRED', 'VALID', 'VALID'), ('ACQUIRE %s PREDICTION %s.' % (_A[2], _O[0]), 'PRED', 'VALID', 'VALID'),
           ('  ACT   %s\nPREDICTION %s ' % (_A[1], _O[2]), 'PRED', 'VALID', 'VALID'),
           ('STOP', 'PRED', 'STOP', 'NONE'), ('STOP.', 'PRED', 'STOP', 'NONE'), ('ABSTAIN', 'PRED', 'ABSTAIN', 'NONE'), ('UNKNOWN', 'PRED', 'ABSTAIN', 'NONE'),
           ('ACT ZZZQ PREDICTION %s' % _O[0], 'PRED', 'INVALID', 'NONE'), ('ACT %s ACQUIRE %s' % (_A[0], _A[1]), 'PRED', 'INVALID', 'MALFORMED'),
           ('ACT %s PREDICTION %s PREDICTION %s' % (_A[0], _O[0], _O[1]), 'PRED', 'INVALID', 'MALFORMED'),
           ('ACT %s' % _A[0], 'PRED', 'INVALID', 'MISSING'), ('ACQUIRE %s' % _A[0], 'PRED', 'INVALID', 'MISSING'),
           ('ACT %s PREDICTION BOGUS' % _A[0], 'PRED', 'INVALID', 'MALFORMED'), ('ACQUIRE %s PREDICTION BOGUS' % _A[0], 'PRED', 'INVALID', 'MALFORMED'),
           ('ACQUIRE %s PREDICTION UNKNOWN' % _A[1], 'PRED', 'INVALID', 'UNKNOWN'), ('ACT %s PREDICTION %s because' % (_A[0], _O[0]), 'PRED', 'INVALID', 'MALFORMED'),
           ('STOP PREDICTION %s' % _O[0], 'PRED', 'INVALID', 'NONE'), ('ACT %s' % _A[0], 'DIRECT', 'VALID', 'NOT_REQUESTED'),
           ('ACT %s PREDICTION %s' % (_A[0], _O[0]), 'DIRECT', 'INVALID', 'NONE')]
    _fxr = [(t_, parse_npdm(t_, _c, g_)['status'] == s_ and parse_npdm(t_, _c, g_)['pred_status'] == p_) for t_, g_, s_, p_ in _fx]
    _mal = {}
    for _bad in ('ACT %s' % _A[0], 'ACT %s PREDICTION BOGUS' % _A[0], 'ACQUIRE %s' % _A[0], 'ACQUIRE %s PREDICTION BOGUS' % _A[0],
                 'ACQUIRE %s PREDICTION UNKNOWN' % _A[0]):
        _ev = make_env_npdm(VAULT['L1']['mapping'], PUB['L1']['goal'], 0, time.monotonic_ns); _recs = []
        _o = run_episode_npdm(PUB['L1'], _ev, (lambda it: (lambda q: next(it)))(iter([_bad, 'STOP'])),
                              lambda r, R_=_recs: (R_.append(r), {'sha256': sha_bytes(json.dumps(r, sort_keys=True).encode())})[1], MK, time.monotonic_ns, 'PRED')
        _mal[_bad] = _ev['log'] == [] and _o['payoff'] == 0 and [r_['kind'] for r_ in _recs][:2] == ['MODEL_INVALID', 'OUTCOME_STATUS'] and \
            _recs[1]['S'] == STATUS_MARKERS_NPDM['none'] and len(_o['trace']) == 2 and 'Decisions left: 3' in _o['trace'][1]['query']
    _clk = time.monotonic_ns; _inv = {o: a for a, o in VAULT['L1']['mapping'].items()}
    _env = make_env_npdm(VAULT['L1']['mapping'], PUB['L1']['goal'], 0, _clk); _L = LedgerNPDM(_clk)
    _L.add({'kind': 'MODEL_INTENT', 't': 1, 'A': _inv[PUB['L1']['goal']], 'K': 'ACQUIRE'}, {'sha256': 'x'}); _L.add({'kind': 'MODEL_PREDICTION', 't': 1, 'P': _O[0]}, {'sha256': 'y'})
    _r1 = _env['step']('ACQUIRE', _inv[PUB['L1']['goal']], _L.ticket(1))
    _L.add({'kind': 'MODEL_INTENT', 't': 2, 'A': _inv[PUB['L1']['goal']], 'K': 'ACT'}, {'sha256': 'x2'}); _L.add({'kind': 'MODEL_PREDICTION', 't': 2, 'P': _O[0]}, {'sha256': 'y2'})
    _r2 = _env['step']('ACT', _inv[PUB['L1']['goal']], _L.ticket(2))
    try: _env['step']('ACT', _A[0], {'step': 3, 'sealed_ns': 0, 'used': False}); _closed_ok = False
    except RuntimeError: _closed_ok = True
    try: make_env_npdm(VAULT['L1']['mapping'], PUB['L1']['goal'], 0, _clk)['step']('ACQUIRE', _A[0], None); _noticket_ok = False
    except RuntimeError: _noticket_ok = True
    sem = {'acquire_goal_outcome_no_reward_continues': _r1['reward'] == 0 and not _r1['terminal'],
           'act_goal_reward_terminal': _r2['reward'] == 1 and _r2['terminal'], 'env_closed_after_act': _closed_ok,
           'env_refuses_step_without_ticket': _noticket_ok}
    del _env, _L
    gate('G1_PARSER_SEMANTICS', 'PASS' if all(x for _, x in _fxr) and all(sem.values()) and all(_mal.values()) else 'FAIL',
         'strict parser fixtures; malformed PRED output -> no environment, no reward, OUTCOME_NONE, one decision consumed; ACT/ACQUIRE/STOP semantics',
         parser_fixtures=[[t_, x] for t_, x in _fxr], malformed_never_reach_environment=_mal, semantics=sem)
    # ------------------------------------------------------------------ live episodes (the model's own decisions)
    EPS = {}; LIVE_FINAL = {}; EP_ENTS = {}
    for eid, kind, cost, rel in EPISODE_PLAN_NPDM:
        t_ep = time.perf_counter(); pub = PUB[eid]
        st = {'mem': mount_from([]), 'ents': [], 'last': {'global': None, 'factual': None, 'prediction': None, 'intent': None}, 'q': None}
        if full_kv_seal(st['mem']) != EMPTY_SEAL: raise StopT896('EPISODE_START_NOT_EMPTY ' + eid)
        def write(rec, st=st, eid=eid):
            ns_ = 'prediction' if rec['kind'] in PREDICTION_KINDS_NPDM else 'factual'
            par = dict(st['last']); cid = '%s_%02d_%s_t%d' % (eid, len(st['ents']), rec['kind'], rec.get('t', 0))
            cp, ent = forge_npdm(rec, cid, par, NS_DIRS[ns_], 'live_' + ns_ if kind != 'diag' or rec['kind'] != 'PRIOR_OBSERVATION' else 'diagnostic_prefix', st['q'])
            st['mem'] = append_live(st['mem'], cp); del cp
            st['ents'].append(ent); st['last']['global'] = ent['sha256']; st['last'][ns_] = ent['sha256']
            if rec['kind'] == 'MODEL_INTENT': st['last']['intent'] = ent['sha256']
            ev('RECORD_SEALED', eid=eid, rec=rec, sha256=ent['sha256'], namespace=ns_); return ent
        def decide(q, st=st, eid=eid):
            st['q'] = sha_bytes(q.encode()); s_before = full_kv_seal(st['mem'])
            raw = timed_gen(st['mem'], q)
            ev('MODEL_DECISION', eid=eid, query_sha256=st['q'], raw=raw, raw_sha256=sha_bytes((raw or '').encode()),
               mount_seal_before=sha_bytes(json.dumps(s_before).encode()), mount_tokens=int(st['mem'][0][0].shape[-2])); return raw
        env = make_env_npdm(VAULT[eid]['mapping'], pub['goal'], VAULT[eid]['pending_steps'], time.monotonic_ns)
        ep = run_episode_npdm(pub, env, decide, write, MK, time.monotonic_ns, 'PRED')
        ep['env_log'] = env['log']; ep['label'] = 'live_episode' if kind in ('live', 'pending') else 'diagnostic_state_probe'
        EPS[eid] = ep; EP_ENTS[eid] = st['ents']; LIVE_FINAL[eid] = full_kv_seal(st['mem'])
        METRICS['episode_elapsed_s'][eid] = round(time.perf_counter() - t_ep, 1)
        ev('EPISODE_CLOSED', eid=eid, closed_by=ep['closed_by'], payoff=ep['payoff'],
           decisions=[[s_['parsed']['status'], s_['parsed']['kind'], s_['parsed']['action'], s_['parsed']['prediction'], s_.get('outcome')] for s_ in ep['trace']])
        log('EPISODE', eid, ep['label'], 'cost', cost, 'closed_by', ep['closed_by'], 'payoff %.2f' % ep['payoff'],
            json.dumps([[s_['raw'], s_['parsed']['status'], s_.get('outcome')] for s_ in ep['trace']]))
        del st['mem']; release(); save()
    R['episodes'] = {e: {'label': v['label'], 'closed_by': v['closed_by'], 'payoff': v['payoff'],
                         'trace': [{k: s_.get(k) for k in ('t', 'query', 'raw', 'parsed', 'env', 'env_resolved', 'outcome', 'outcome_seal_ns', 'records')} for s_ in v['trace']],
                         'ledger': [[r_, sh_, ns_] for r_, sh_, ns_ in v['ledger']], 'env_log': v['env_log']} for e, v in EPS.items()}
    order_ok = all(s_['records'][0]['ns'] < s_['records'][1]['ns'] < s_['env']['env_step_start_ns'] < s_['outcome_seal_ns']
                   for v in EPS.values() for s_ in v['trace'] if s_.get('env'))
    gate('G1_LIVE_EPISODES', 'PASS' if order_ok and len(EPS) == len(EPISODE_PLAN_NPDM) else 'FAIL',
         'every ACT/ACQUIRE: intent seal < prediction seal < env_step_start < outcome seal; terminal ACT/STOP; invalid not corrected',
         n_episodes=len(EPS), decisions=sum(len(v['trace']) for v in EPS.values()))
    # ------------------------------------------------------------------ G1 rebuild from SSD, isolation, provenance, pending
    rb = {}
    for eid in EPS:
        t_ = time.perf_counter(); cps = [load_record(e) for e in EP_ENTS[eid]]; METRICS['reload_s'].append(round(time.perf_counter() - t_, 3))
        m_ = mount_from(cps); rb[eid] = full_kv_seal(m_) == LIVE_FINAL[eid]; del m_, cps; release(); guard('reload')
    gate('G1_REBUILD_FROM_SSD', 'PASS' if all(rb.values()) else 'FAIL', 'every episode mount rebuilt from its SSD files == live mount (80-layer K/V seals)', episodes=rb)
    prov = {'predictions_only_in_prediction_namespace': all((e['namespace'] == 'prediction') == (e['record_kind'] == 'MODEL_PREDICTION') for ents in EP_ENTS.values() for e in ents),
            'no_prediction_in_observed_outcome': all(r_['kind'] != 'OBSERVED_OUTCOME' or r_['O'] in PUB[eid]['outcomes'] for eid, v in EPS.items() for r_, _, _ in v['ledger']),
            'parent_chain_global': all(ents[i]['global_parent_sha256'] == (ents[i - 1]['sha256'] if i else None) for ents in EP_ENTS.values() for i in range(len(ents))),
            'prediction_linked_to_its_intent': all(e['linked_intent_sha256'] is not None for ents in EP_ENTS.values() for e in ents if e['record_kind'] == 'MODEL_PREDICTION'),
            'episodes_start_from_empty_mount': True, 'disjoint_names_independent_episodes': wm['names_unique_disjoint']}
    gate('G1_ISOLATION_PROVENANCE', 'PASS' if all(prov.values()) else 'FAIL', 'namespaces, parents, no prediction as observed fact, empty start per episode', checks=prov)
    # pending: (1) the live P1 episode (environment delays its first outcome; data, depends on the model's choice) and
    # (2) a SCRIPTED technical canary (fixed harness strings, NOT a model decision, never scored, own namespace) so that the
    # physical pending path is always exercised: intent, prediction, OUTCOME_PENDING status, then the observed outcome.
    _cpub = dict(PUB['P1']); _ca = list(_cpub['actions']); _co_ = list(_cpub['outcomes'])
    _script = iter(['ACQUIRE %s PREDICTION %s' % (_ca[0], _co_[0]), 'STOP'])
    _cst = {'mem': mount_from([]), 'ents': [], 'prev': None}
    def _cwrite(rec, st=_cst):
        cp, ent = forge_npdm(rec, 'CANARY_%02d_%s' % (len(st['ents']), rec['kind']), {'global': st['prev']}, NS_DIRS['canary'], 'technical_canary')
        st['mem'] = append_live(st['mem'], cp); st['ents'].append(ent); st['prev'] = ent['sha256']; return ent
    _cenv = make_env_npdm(VAULT['P1']['mapping'], _cpub['goal'], 1, time.monotonic_ns)
    _cep = run_episode_npdm(_cpub, _cenv, lambda q: next(_script), _cwrite, MK, time.monotonic_ns, 'PRED')
    _ck = [r_['kind'] for r_ in _cep['trace'][0]['records']]; del _cst['mem']; release()
    _pt = EPS['P1']['trace'][0] if EPS['P1']['trace'] else None
    _live_p = None if (_pt is None or not _pt.get('env')) else (_pt['env']['status'] == 'PENDING' and [r_['kind'] for r_ in _pt['records']][:4] ==
                                                               ['MODEL_INTENT', 'MODEL_PREDICTION', 'OUTCOME_STATUS', 'OBSERVED_OUTCOME'])
    _can_ok = _ck[:4] == ['MODEL_INTENT', 'MODEL_PREDICTION', 'OUTCOME_STATUS', 'OBSERVED_OUTCOME'] and _cep['trace'][0]['env']['status'] == 'PENDING' and \
        _cep['trace'][0]['env_resolved']['arrival_ns'] > _cep['trace'][0]['env']['env_step_start_ns']
    gate('G1_PENDING', 'PASS' if _can_ok and _live_p is not False else 'FAIL',
         'pending status sealed, outcome released only by resolve(), no query while pending (scripted canary always; live P1 if it stepped)',
         canary_records=_ck, live_P1_pending_ok=_live_p)
    # ------------------------------------------------------------------ G1 pre-outcome twin (two different futures)
    # Pre-registered: the first episode in plan order whose FIRST model decision is a VALID ACT/ACQUIRE (a technical canary;
    # the model's raw decision is never forced). No such episode -> INCONCLUSIVE (Gate-1 stops).
    _tw = {'applicable': False}
    _te = [e for e, k, c, r in EPISODE_PLAN_NPDM if EPS[e]['trace'] and EPS[e]['trace'][0]['parsed']['status'] == 'VALID']
    if _te:
        _tid = _te[0]; _t0 = EPS[_tid]['trace'][0]; _p1 = _t0['parsed']; _npre = len(PUB[_tid]['prefix'])
        _m0 = mount_from([load_record(e) for e in EP_ENTS[_tid][:_npre]]); _raw2 = timed_gen(_m0, _t0['query']); del _m0; release()
        _ri = {'kind': 'MODEL_INTENT', 'K': _p1['kind'], 'A': _p1['action'], 't': 1}
        _rp = {'kind': 'MODEL_PREDICTION', 'P': _p1['prediction'], 't': 1, 'pred_status': 'VALID'}
        _ci, _ei = forge_record(record_ids_npdm(_ri, tok_ids), _tid + '_TWIN_intent', None, 'twin', NS_DIRS['twin'])
        _cp_, _ep_ = forge_record(record_ids_npdm(_rp, tok_ids), _tid + '_TWIN_prediction', _ei['sha256'], 'twin', NS_DIRS['twin'])
        _oL = list(PUB[_tid]['outcomes']); _alt = {a: _oL[(_oL.index(o) + 1) % 3] for a, o in VAULT[_tid]['mapping'].items()}  # environment-side other future
        _envB = make_env_npdm(_alt, PUB[_tid]['goal'], 0, time.monotonic_ns); _LB = LedgerNPDM(time.monotonic_ns)
        _LB.add(_ri, _ei); _LB.add(_rp, _ep_); _rB = _envB['step'](_p1['kind'], _p1['action'], _LB.ticket(1))
        _tw = {'applicable': True, 'episode': _tid, 'raw_identical': _raw2 == _t0['raw'],
               'intent_tensor_seal_identical': _ei['tensor_seal'] == EP_ENTS[_tid][_npre]['tensor_seal'],
               'prediction_tensor_seal_identical': _ep_['tensor_seal'] == EP_ENTS[_tid][_npre + 1]['tensor_seal'],
               'future_A': _t0.get('outcome'), 'future_B': _rB['outcome'], 'futures_differ': _t0.get('outcome') != _rB['outcome']}
        del _ci, _cp_
    _tv, _tr = twin_verdict_npdm(_tw)
    gate('G1_PRE_OUTCOME_TWIN', _tv, _tr, twin=_tw)
    for g_ in ('G1_PARSER_SEMANTICS', 'G1_LIVE_EPISODES', 'G1_REBUILD_FROM_SSD', 'G1_ISOLATION_PROVENANCE', 'G1_PENDING', 'G1_PRE_OUTCOME_TWIN'):
        if R['gates'][g_]['status'] != 'PASS': raise StopT896('GATE1_NOT_PASS %s=%s' % (g_, R['gates'][g_]['status']))
    # ------------------------------------------------------------------ counterfactual control mounts (never executed)
    ELIG = eligible_states_npdm(EPS); CTRL = []; geo_bad = []; det = []
    EQ_GEO = ('PRED_MASK', 'PLACEBO_PRED', 'CYCLIC_PRED', 'PLACEBO_PRED_ALL', 'FACTUAL_DELETED', 'CF_OUTCOME', 'ORDER_PERM')
    for s in ELIG:
        eid = s['eid']; pub = PUB[eid]; led = EPS[eid]['ledger']; ents = EP_ENTS[eid]
        cut = [i for i, (r_, sh_, ns_) in enumerate(led) if r_.get('t') == s['decision_t'] and r_['kind'] != 'PRIOR_OBSERVATION'][0]
        frozen = [r_ for r_, sh_, ns_ in led[:cut]]; left = pub['budget'] - s['decision_t'] + 1
        live_raw = [x for x in EPS[eid]['trace'] if x['t'] == s['decision_t']][0]['raw']
        base_cps = [load_record(e) for e in ents[:cut]]; geo0 = geometry_npdm(frozen, tok_ids); z = {}; raws = {}; ntoks = {}; armrec = {}
        for arm, gram, _desc in ARMS_NPDM:
            q = query_npdm(contract_npdm(pub), left, gram, 1 if arm == 'ORDER_PERM' else 0)
            if arm in ('NPDM', 'ORDER_PERM'): ar = [dict(r_, src=i, changed=False) for i, r_ in enumerate(frozen)]
            else: ar = derive_arm_npdm(arm, frozen, pub, MK, s['discrepancy_t'])
            if ar is None: z[arm] = None; raws[arm] = None; ev('CONTROL_NOT_APPLICABLE', eid=eid, arm=arm); continue
            armrec[arm] = ar
            if arm in EQ_GEO and geometry_npdm(ar, tok_ids) != geo0: geo_bad.append([eid, arm])
            cps = []
            for r_ in ar:
                if not r_['changed']: cps.append(base_cps[r_['src']])
                else:
                    cp, _ent = forge_npdm(r_, '%s_CTRL_%s_%02d' % (eid, arm, r_['src']), {'global': ents[r_['src']]['sha256']}, NS_DIRS['control'], 'control_' + arm)
                    cps.append(cp)
            if arm == 'MATCHED_FORGE_IO':          # focal prediction re-forged into quarantine, NOT mounted (forge/IO only)
                for i, r_ in enumerate(frozen):
                    if r_['kind'] == 'MODEL_PREDICTION' and r_['t'] == s['discrepancy_t']:
                        forge_npdm(r_, '%s_QUAR_%02d' % (eid, i), {'global': ents[i]['sha256']}, NS_DIRS['quarantine'], 'quarantine')
            m_ = mount_from(cps); ntoks[arm] = int(m_[0][0].shape[-2]); raw = timed_gen(m_, q); del m_, cps; release()
            raws[arm] = raw; z[arm] = decision_key_npdm(parse_npdm(raw, contract_npdm(pub), gram))
            ev('CONTROL_DECISION', eid=eid, arm=arm, raw=raw, decision=str(z[arm]), mount_tokens=ntoks[arm])
        det.append({'eid': eid, 'npdm_rebuilt_equals_live': raws['NPDM'] == live_raw, 'matched_forge_io_equals_no_pred': raws['MATCHED_FORGE_IO'] == raws['NO_PRED'],
                    'equal_geometry_mount_tokens': len({ntoks[a] for a in ('NPDM',) + EQ_GEO if a in ntoks}) == 1})
        _fc = [r_['P'] for r_ in armrec['CYCLIC_PRED'] if r_['kind'] == 'MODEL_PREDICTION' and r_.get('t') == s['discrepancy_t']]
        CTRL.append(dict(s, z=z, raws=raws, mount_tokens=ntoks, frozen_records=frozen, left=left, arm_records={a: armrec[a] for a in ('FACTUAL_DELETED', 'CF_OUTCOME') if a in armrec},
                         placebo_u=placebo_u_npdm(frozen, pub, s['discrepancy_t']), cyclic_placebo=_fc,
                         cyclic_collision=_fc == [s['observed']], facts=sorted(facts_npdm(frozen, pub['outcomes']))))
        del base_cps; release(); save()
    gate('G1_CONTROL_GEOMETRY', 'PASS' if not geo_bad and all(d['equal_geometry_mount_tokens'] for d in det) else 'FAIL',
         'PRED_MASK / PLACEBO_PRED (u) / CYCLIC_PRED / PLACEBO_PRED_ALL / FACTUAL_DELETED / CF_OUTCOME / ORDER_PERM: equal per-field token geometry and mount length '
         '(equal token counts are not equal semantics or attention exposure)', mismatches=geo_bad, states=len(CTRL))
    gate('G1_DETERMINISM', 'PASS' if all(d['npdm_rebuilt_equals_live'] and d['matched_forge_io_equals_no_pred'] for d in det) else 'FAIL',
         'NPDM rebuilt from SSD reproduces the live raw decision; MATCHED_FORGE_IO == NO_PRED (extra quarantine forge/IO, not a fully matched compute trace)',
         states=det)
    # ------------------------------------------------------------------ Gate-3 DIRECT baseline at the 7 first-decision states
    G3S = []
    for eid in ('A1', 'A2', 'B1', 'D1', 'D2', 'L1', 'L2'):
        pub = PUB[eid]; ents = EP_ENTS[eid]; npre = len(pub['prefix'])
        m_ = mount_from([load_record(e) for e in ents[:npre]]); rawd = timed_gen(m_, query_npdm(contract_npdm(pub), pub['budget'], 'DIRECT')); del m_; release()
        G3S.append({'eid': eid, 'raw_pred_grammar': EPS[eid]['trace'][0]['raw'], 'raw_direct': rawd,
                    'z_pred': decision_key_npdm(EPS[eid]['trace'][0]['parsed']), 'z_direct': decision_key_npdm(parse_npdm(rawd, contract_npdm(pub), 'DIRECT'))})
    # ================================================================== OFFLINE EVALUATOR (after every live / control phase)
    VAULT_PATH = ROOT / 'NPDM_SMOKE_evaluator_vault.json'; VAULT_PATH.write_bytes(_vb)
    g1_ok = all(R['gates'][g_]['status'] == 'PASS' for g_ in GATE1[:-2])        # fail-closed: any Gate-1 part not PASS -> no causal reading
    for c_ in CTRL:
        _cc = contract_npdm(PUB[c_['eid']]); _ou = PUB[c_['eid']]['outcomes']
        _b0 = bayes_npdm(_cc, frozenset(tuple(x) for x in c_['facts']), c_['left'])
        _bf = bayes_npdm(_cc, facts_npdm(c_['arm_records']['FACTUAL_DELETED'], _ou), c_['left'])
        c_['optimal'] = _b0['optimal']; c_['optimal_fd'] = _bf['optimal']
        c_['q'] = {str(k): v for k, v in _b0['Q'].items()}; c_['q_fd'] = {str(k): v for k, v in _bf['Q'].items()}
        c_['optimal_cf'] = bayes_npdm(_cc, facts_npdm(c_['arm_records']['CF_OUTCOME'], _ou), c_['left'])['optimal'] if 'CF_OUTCOME' in c_['arm_records'] else None
        c_['subtype'] = 'GOAL_REVEALED_BY_OBSERVED_OUTCOME' if c_['observed'] == PUB[c_['eid']]['goal'] else 'GOAL_NOT_REVEALED'
        c_['source'] = EPS[c_['eid']]['label']
    G2 = gate2_npdm(CTRL) if g1_ok else {'verdict': 'NOT_RUN', 'reason': 'GATE1_NOT_PASS'}
    for f_ in G3S:
        pub = PUB[f_['eid']]; b_ = bayes_npdm(contract_npdm(pub), frozenset(pub['prefix']), pub['budget'])
        f_.update(Q=b_['Q'], optimal=b_['optimal'], label=f_['eid'], must_not_acquire=f_['eid'] in ('A1', 'B1', 'L2'))
    G3 = gate3_npdm(G3S) if g1_ok else {'verdict': 'NOT_RUN'}
    for f_ in G3S: f_['Q'] = {str(k): v for k, v in f_.get('Q', {}).items()}      # JSON-safe report copy (after scoring)
    _st2 = {'SMOKE_CAUSAL_PASS': 'SMOKE_CAUSAL_PASS', 'SMOKE_CAUSAL_PASS_LIMITED': 'SMOKE_CAUSAL_PASS_LIMITED', 'FAIL': 'FAIL', 'INCONCLUSIVE': 'INCONCLUSIVE', 'NOT_RUN': 'NOT_RUN'}[G2['verdict']]
    gate('G2_CAUSAL_PREDICTION_USE', _st2, G2.get('reason'), result={k: v for k, v in G2.items()},
         eligible=[{k: v for k, v in c_.items() if k not in ('frozen_records',)} for c_ in CTRL])
    gate('G3_POLICY_SUPPORT', G3['verdict'], 'supporting only; never replaces Gate-2', result=G3, states=G3S)
    gate('G4_TRANSFER', 'NOT_RUN', 'cross-world transfer is out of scope for this smoke')
    R['controls'] = CTRL; R['gate3_states'] = G3S; R['metrics'] = METRICS
    R['vault'] = {'file': str(VAULT_PATH), 'sha256': sha_path(VAULT_PATH), 'matches_commitment': sha_path(VAULT_PATH) == VAULT_COMMIT}
    ev('OFFLINE_EVALUATION_DONE', gate2=G2['verdict'], gate3=G3['verdict'])
    # ---------------------------------------------------------------------------------------- P1 / P7 final
    files_end = {e['cid']: sha_path(e['file']) == e['sha256'] for e in CART_INDEX}
    empty_end = seal_cp(CP_EMPTY) == EMPTY_ENT['tensor_seal']
    p1_ok = all(files_end.values()) and empty_end and len(files_end) == len(CART_INDEX)
    gate('P1_PHYSICAL', 'PASS' if p1_ok else 'FAIL', None if p1_ok else 'a cartridge file SHA-256 changed after it was written',
         cartridge_files=len(CART_INDEX), files_unchanged=sum(files_end.values()), changed=[k for k, v in files_end.items() if not v],
         empty_tensor_seal_unchanged=empty_end, cartridge_bytes=sum(Path(e['file']).stat().st_size for e in CART_INDEX))
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
    # ---------------------------------------------------------------- verdict: G0 -> G1 -> G2 (fail-closed), G3 support, G4 NOT_RUN
    G_ = R['gates']; R['metrics'] = METRICS; R['gpu_peak'] = gpu_mem()
    tech = 'PASS' if all(G_[g]['status'] == 'PASS' for g in GATE0 + GATE1) else (
        'FAIL' if any(G_[g]['status'] == 'FAIL' for g in GATE0 + GATE1) else 'INCONCLUSIVE')
    _v2 = G_['G2_CAUSAL_PREDICTION_USE']['status']
    DEC = {'VERDICT': ('NPDM_' + _v2) if tech == 'PASS' else 'TECHNICAL_' + ('INVALID' if tech == 'FAIL' else 'INCONCLUSIVE'),
           'subcodes': [G2.get('reason'), 'G3=' + G3['verdict'], 'G4=NOT_RUN'], 'claims': G2.get('claims'), 'gate2': G2, 'gate3': G3, 'technical': tech}
    R['decision'] = DEC; R['technical_status'] = tech
    R['answers'] = answers_npdm({g: G_[g]['status'] for g in GATE_ORDER}, G2 if isinstance(G2, dict) else {}, G3)
    for k_, v_ in R['answers'].items(): log('ANSWER', k_, json.dumps(v_, default=str))
    log('DECISION', json.dumps({'VERDICT': DEC['VERDICT'], 'subcodes': DEC['subcodes'], 'claims': DEC['claims'],
                                'gate2': {k: G2.get(k) for k in ('verdict', 'reason', 'n_eligible', 'n_effect', 'n_correct', 'n_wrong', 'n_ceiling')}}, default=str))
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
        _sr = str(R.get('stop_reason', ''))
        sci = 'TECHNICAL_INCOMPLETE' if 'ABORT_TECHNICAL_INCOMPLETE' in _sr else ('TECHNICAL_INCONCLUSIVE' if '=INCONCLUSIVE' in _sr else 'TECHNICAL_INVALID')
    verdict = sci
    if 'answers' not in R:
        try: R['answers'] = answers_npdm({g: G[g]['status'] for g in GATE_ORDER}, {}, {'verdict': 'NOT_RUN'})
        except Exception: pass
    R['verdict'] = verdict; R['verdict_scope'] = 'smoke canary only: this cell, this runtime, 14 small episodes; not a cohort, not VOI, not transfer, not autonomy'
    R['elapsed_s'] = round(time.perf_counter() - T0, 1)
    try: R['gpu_final'] = gpu_mem()
    except Exception: pass
    log('=' * 112)
    for g in GATE_ORDER: log('%-30s %-20s %s' % (g, G[g]['status'], G[g]['reason'] or ''))
    summary = {'verdict': verdict, 'subcodes': (R.get('decision') or {}).get('subcodes'), 'status': R['status'],
               'technical_status': R.get('technical_status'), 'gates': {g: G[g]['status'] for g in GATE_ORDER},
               'commit': COMMIT, 'model_revision': MODEL_REVISION, 'run_id': RUN_ID, 'elapsed_s': R['elapsed_s'],
               'scope': 'NPDM causal smoke; SMOKE_CAUSAL_PASS is never a scientific PASS'}
    log('NPDM_SMOKE_SUMMARY ' + json.dumps(summary, sort_keys=True, default=str))
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
                all(k_ in listed for k_ in ('NPDM_SMOKE_results.json', 'NPDM_SMOKE.log', 'NPDM_SMOKE_events.jsonl', 'NPDM_SMOKE_public_manifest_SEALED.json',
                                             'NPDM_SMOKE_evaluator_vault.json', 'NPDM_SMOKE_cell_source.py'))
            # every cartridge written in the run (Phase 1, calibration, derived arms) must be in the ZIP with its recorded SHA-256
            _ci = [e_ for e_ in (R.get('cartridges') or [])]
            AG['all_cartridges_in_zip'] = all(listed.get(Path(e_['file']).relative_to(ROOT).as_posix()) == e_['sha256'] for e_ in _ci)
            AG['cartridges_expected'] = len(_ci)
            AG['sha256sums_rows'] = len(rows)
            AG['report_in_zip_is_read_back_report'] = listed.get('NPDM_SMOKE_results.json') == rep_sha
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
    log('NPDM_SMOKE_LOG_END SCIENTIFIC_VERDICT=%s | STATUS=%s | ZIP_CORE=%s | CELL_IDENTITY_MATCH=%s | final ARTIFACT_STATUS: '
        'receipt + console' % (verdict, R['status'], core, AG['cell_identity_match']))
    AG['final_log_sha256'] = sha_path(LOG); AG['drive_final_log'] = AG['drive_final_report'] = 'NOT_RUN'
    if DRIVE_DIR is not None:
        for key_, src_ in (('drive_final_log', LOG), ('drive_final_report', OUT)):
            try:
                dst_ = Path(DRIVE_DIR) / src_.name; shutil.copy2(src_, dst_); AG[key_] = dst_.read_bytes() == src_.read_bytes()
            except Exception as e:
                AG[key_] = False; AG[key_ + '_error'] = '%s: %s' % (type(e).__name__, e)
    AG.setdefault('all_cartridges_in_zip', False)
    fails = [k for k in ('report_written_read_back', 'zip_testzip', 'sha256sums', 'report_in_zip_is_read_back_report',
                         'all_cartridges_in_zip', 'cell_identity_match') if AG[k] is not True]
    if DRIVE_DIR is not None: fails += [k for k in ('drive', 'drive_final_log', 'drive_final_report') if AG[k] is not True]
    ART_STATUS = 'FAIL' if fails else ('PASS' if DRIVE_DIR is not None else 'INCOMPLETE_DRIVE_NOT_MOUNTED')
    # priority 1 (technical AND artefact integrity): a verdict whose artefacts are not verified is not a reportable verdict
    FINAL = verdict if ART_STATUS == 'PASS' else 'TECHNICAL_INCONCLUSIVE_ARTIFACT'
    receipt = {'test': 'NPDM_SMOKE', 'run_id': RUN_ID, 'scientific_verdict': verdict, 'final_verdict': FINAL,
               'subcodes': summary.get('subcodes'), 'technical_status': R.get('technical_status'), 'status': R['status'],
               'answers': R.get('answers'),
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
    print('NPDM_SMOKE_FINAL FINAL_VERDICT=%s | SCIENTIFIC_VERDICT=%s | SUBCODES=%s | TECHNICAL_STATUS=%s | STATUS=%s | ARTIFACT_STATUS=%s' % (
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
