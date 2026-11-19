# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST899 BELIEF-TO-POLICY — NATIVE RECURSIVE BELIEF CONSOLIDATION (frozen-state physical replay)
#                                                                                                single Google Colab cell
# Frozen Qwen2.5-72B-Instruct NF4 / BF16, one A100-SXM4-80GB, the physical CUT3/H3/K-V SSD cartridge engine of TEST896 /
# TEST897 (pinned engine commit f1007d91). This cell is the executed TEST897 cell (897npdm_smoke.py, commit 813cdca7, blob
# fbde1d13) with its engine, model load, cartridge functions and artefact chain kept AST-identical (two exceptions, checked
# in GATE1 as exact substitutions: the TEST898 status names in gate() and the TEST899_BP name in _boot_fail()); only the
# experiment body, the constants and the verdict are new. History is locked: TEST897 = NPDM_FAIL (WRONG_DIRECTION_CHANGE, G3 FAIL).
#
# QUESTION (L1 mechanism isolation only): does the archived, model-generated REAL belief change the next native greedy
# decision under exact physical token geometry, and how much of the TEST898 failure is contributed by PRED versus DIRECT
# grammar? Ten native readouts compare F, REAL, two neutral controls and a public-name SWAPPED control. Every B control is
# forged into CUT3/H3/KV, sealed, written and read back from SSD before mounting. F arms receive matched quarantine I/O.
# Inputs: the ORIGINAL TEST897 and TEST898 archives on Drive, opened read-only and never rewritten. Exact geometry is a
# tokenizer-only CPU preflight; UNSAT -> NO_RUN before model load. No padding or relaxed matcher is permitted.
# NO training / LoRA / optimizer / hooks / RAG / oracle routing / answer override / evaluator leakage / future outcome.
# Offline public Bayes runs only after all ten generations. CAR is post-hoc measurement, never action selection.
# NOT EXECUTED ON GPU BY THE AUTHOR OF THIS CELL. GPU EXECUTION NOT VERIFIED.
# AUDIT REVISION (independent review of K3.1 TEST899.py sha256 5b574b6b / blob c4fc3a60, CPU only): token boundaries from the
# token byte strings with the separator space in the first value token (the original rule rejected REAL itself under the
# Qwen2 ByteLevel(trim_offsets=False) tokenizer -> NO_RUN on every run); three two-token neutral words replaced; SWAPPED
# permutes action names only (no renaming of the public goal outcome inside the belief); GATE0C separates UNSAT (NO_RUN)
# from technical errors (FAIL); GATE4 reports DECISION and ACTION levels separately (prediction-slot validity is not an
# action change); the model tokenizer must reproduce the pre-model geometry ids.
#
# RUN: upload this file as TEST899.py to the default branch of ceceli33/titan-cognitive-core-v3, paste it exactly (from the
# Raw view) into one Colab cell on an A100 runtime and press Run. The cell mounts Google Drive and reads
# /content/drive/MyDrive/NPDM_SMOKE_20261118T223234Z/NPDM_SMOKE_SONUC_20261118T223234Z.zip and
# /content/drive/MyDrive/TEST898_NRBC_20261119T090123Z/TEST898_NRBC_SONUC_20261119T090123Z.zip. Source identity is checked
# automatically (fail-closed); both archives and exact geometry are verified on CPU BEFORE the model is loaded.
# =====================================================================================================================
import os, sys, subprocess, importlib.util, importlib.metadata, urllib.request, hashlib, ast, json, time, gc, math
import traceback, platform, types, random, shutil, re
from pathlib import Path
from datetime import datetime, timezone
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True')

# ---------------------------------------------------------------------------------------------------------- versions
# Bootstrap record (stdlib only) is created BEFORE the torch check / pip / imports, so a bootstrap failure is recorded.
RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
ROOT = Path(('/content/' if Path('/content').exists() else '/tmp/') + 'TEST899_BP_' + RUN_ID)
ROOT.mkdir(parents=True, exist_ok=True)
LOG = ROOT / 'TEST899_BP.log'; OUT = ROOT / 'TEST899_BP_results.json'; LOG.write_text('')
ZIP_PATH = ROOT.parent / ('TEST899_BP_SONUC_' + RUN_ID + '.zip'); RECEIPT_PATH = ROOT.parent / ('TEST899_BP_SONUC_' + RUN_ID + '_RECEIPT.json')
def _ver(name):
    try: return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError: return None
def _boot_fail(e):
    tb = traceback.format_exc()
    rec = {'test': 'TEST899_BP', 'run_id': RUN_ID, 'status': 'BOOTSTRAP_ERROR', 'error': '%s: %s' % (type(e).__name__, e),
           'traceback': tb, 'installed_versions': {p_: _ver(p_) for p_ in ('torch', 'transformers', 'accelerate', 'bitsandbytes')},
           'technical_verdict': 'NOT_RUN', 'ARTIFACT_STATUS': 'FAIL', 'gpu_model_loaded': False,
           'note': 'stopped before any model / GPU work; Drive not attempted'}
    for path_, txt_ in ((OUT, json.dumps(rec, indent=2)), (RECEIPT_PATH, json.dumps(rec, indent=2))):
        try: tmp_ = Path(str(path_) + '.tmp'); tmp_.write_text(txt_); tmp_.replace(path_)
        except Exception as e2: print('BOOTSTRAP_RECORD_WRITE_FAILED', path_, e2)
    with LOG.open('a') as f_: f_.write('BOOTSTRAP_ERROR %s\n%s\nARTIFACT_STATUS=FAIL\n' % (rec['error'], tb))
    print(tb); print('TEST899_BP BOOTSTRAP_ERROR recorded in', OUT, LOG, RECEIPT_PATH)
    raise SystemExit('TEST899_BP BOOTSTRAP_ERROR: ' + rec['error'])
try:
    # Exact runtime contract. torch 2.14.1+cu130 / CUDA 13.0 / transformers 5.22.1 = the combination recorded in 893.log
    # (TABLE GATE0 RUNTIME) under which this engine, incl. api877, ran on the A100. accelerate 1.16.0 / bitsandbytes 0.50.2 =
    # the versions whose sources K3.1 audited (not recorded in 893.log). torch is never installed or changed by this cell.
    TORCH_REQ = '2.14.1+cu130'; CUDA_REQ = '13.0'
    PINS = {'transformers': '5.22.1', 'accelerate': '1.16.0', 'bitsandbytes': '0.50.2'}
    if _ver('torch') != TORCH_REQ:
        raise SystemExit('TEST899_BP_ENV: torch %s found, %s required (893.log runtime); no torch change is made' % (_ver('torch'), TORCH_REQ))
    _need = [p for p, v in PINS.items() if _ver(p) != v]
    if _need:
        _loaded = [p for p in _need if p in sys.modules]
        if _loaded: raise SystemExit('TEST899_BP_ENV: %s already imported with other versions; restart the runtime and rerun' % _loaded)
        _con = Path('/tmp/TEST899_BP_torch_constraint.txt'); _con.write_text('torch==%s\n' % TORCH_REQ)
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', '-c', str(_con)] + ['%s==%s' % (p, PINS[p]) for p in _need])
    _got = {p: _ver(p) for p in list(PINS) + ['torch']}
    if any(_got[p] != v for p, v in PINS.items()) or _got['torch'] != TORCH_REQ:
        raise SystemExit('TEST899_BP_ENV: version contract not met after install: %s' % _got)
    import torch, transformers, accelerate, bitsandbytes
    if torch.__version__ != TORCH_REQ or torch.version.cuda != CUDA_REQ or transformers.__version__ != PINS['transformers'] or \
            accelerate.__version__ != PINS['accelerate'] or bitsandbytes.__version__ != PINS['bitsandbytes']:
        raise SystemExit('TEST899_BP_ENV: imported versions differ from the contract: torch %s cuda %s transformers %s accelerate %s '
                         'bitsandbytes %s' % (torch.__version__, torch.version.cuda, transformers.__version__, accelerate.__version__,
                                              bitsandbytes.__version__))
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    from transformers.cache_utils import DynamicCache
except BaseException as _e:
    if isinstance(_e, KeyboardInterrupt): raise
    _boot_fail(_e)


# --------------------------------------------------------------------------------------------------------- constants
TAG = 'TEST899_BP'; MARKER = 'AKBASCORE SILICON HIPPOCAMPUS — TEST899 NATIVE BELIEF-TO-POLICY CAUSAL ISOLATION'
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
EVENTS = ROOT / 'TEST899_BP_events.jsonl'; EVENTS.write_text('')
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
         'test': 'TEST899 L1 native belief-to-policy causal isolation; factual mount and public contract are fixed',
         'estimands': ['same-runtime reproduction of TEST898 F/PRED and REAL/PRED',
                       'PRED versus DIRECT contribution within identical physical mounts',
                       'decision-level content influence under exact token-ID/field-boundary geometry',
                       'neutral baseline stability and correctness-specific preservation'],
         'arms': ['F/PRED','F/DIRECT','REAL/PRED','REAL/PRED repeat','REAL/DIRECT',
                  'NEUTRAL1/PRED','NEUTRAL1/DIRECT','SWAPPED/PRED','NEUTRAL2/PRED','NEUTRAL2/DIRECT'],
         'native_generations_planned': 10,
         'geometry': '134 body tokens; identical (position, id) of every non-content token and identical ordered field token spans; '
                     'token boundaries from the token byte strings (Qwen2 byte-level BPE: the space after FIELD: belongs to the first value '
                     'token); CUT3 slot, P=30, H3/KV layout, append order and query position identical; otherwise NO_RUN; no padding',
         'neutral': 'one-for-one content-token substitution with 8 pre-registered one-token nouns per control (NEUTRAL_WORDS_899); no public '
                    'names, epistemic values, goal/reward or action information; no padding',
         'swapped': 'parser-valid permutation of the public L1 ACTION names inside REAL (outcome names, hence the public goal, unchanged): '
                    'first non-identity permutation in itertools order with a factually wrong core and exact geometry; no hidden mapping',
         'readout': 'locked 709 answer(), native greedy, MAX_NEW = TEST897 manifest value (recomputed in GATE1) for both grammars; '
                    'CAR is post-hoc measurement only',
         'decision_levels': 'DECISION (native grammar decision, INVALID = WASTE) and ACTION (written action prefix) are reported separately; '
                            'the mechanism label uses ACTION for content influence',
         'reproducibility': 'F/PRED and first REAL/PRED raw must equal TEST898; REAL repeat raw and re-tokenized IDs exact; CAR absolute tolerance historical 2e-4, repeat 1e-5',
         'interpretation': 'no B necessity or incremental utility claim because F/PRED is already optimal; no learning/transfer/autonomy claim',
         'scorer_note': '898 lexical GOAL/BUDGET_STOP false negatives are reported, not repaired; parser and evaluator are unchanged'}
MAX_NEW = 24                                     # replaced by the TEST897 manifest value before the first generation
# ------------------------------------------------------------------------------------------------ TEST898 inputs
# Identity of the INPUT archive (TEST897 values recorded by the TEST897 run and its published source; NOT a hash of this cell)
T897 = {'run_id': '20261118T223234Z', 'root': 'NPDM_SMOKE_20261118T223234Z',
        'zip': '/content/drive/MyDrive/NPDM_SMOKE_20261118T223234Z/NPDM_SMOKE_SONUC_20261118T223234Z.zip',
        'drive_results': '/content/drive/MyDrive/NPDM_SMOKE_20261118T223234Z/NPDM_SMOKE_results.json',
        'results_sha256': 'eaeccc4b915d9dd1fc82bd662d3d5f7da7e512f37f6406fd64515945b4c21956', 'results_bytes': 557312,
        'cell_path': '897npdm_smoke.py', 'cell_commit': '813cdca7c53a12ef3791a01cce293e106fb841f3',
        'cell_blob': 'fbde1d130712014070fa6db45ff36f05f9f9d06c', 'cell_sha256': 'f41accd5f71fd1167f6e91d186783517165c4deae270f5193256ef8206b3e0a4',
        'cell_bytes': 132977, 'verdict': 'NPDM_FAIL'}
T898IN = {'run_id': '20261119T090123Z', 'root': 'TEST898_NRBC_20261119T090123Z',
          'zip': '/content/drive/MyDrive/TEST898_NRBC_20261119T090123Z/TEST898_NRBC_SONUC_20261119T090123Z.zip',
          'zip_sha256': '4e722c2ee8a553de1b01d9feb389dd6789a0d49571d8833ca5503fba6223b39b', 'zip_bytes': 59717073,
          'results_sha256': '660e727da72078e8c9b0fc6ffad88e48072380701cc9c4754c546f0a3180172f', 'results_bytes': 183986,
          'events_sha256': 'f3ac810852d50b2dfd4ac5f5dacb94abe427b5ed8e3fb94d0b997e9bbae45f5a', 'events_bytes': 32157,
          'members': 25, 'sha_rows': 24, 'cartridges': 19,
          'real_cid': 'L1_BELIEF_L1_REAL', 'real_file': 'T896_L1_BELIEF_L1_REAL.pt',
          'real_sha256': 'dc919ccc52fac8d02838c8d8f176e90f4c04ea1701ac42a853236fbddd70bbf3', 'real_body_tokens': 134}
T898_REQ_FILES = ('T896_EMPTY.pt',
                  'T896_L1_00_MODEL_INTENT_t1.pt', 'T896_L1_01_MODEL_PREDICTION_t1.pt', 'T896_L1_02_OBSERVED_OUTCOME_t1.pt',
                  'T896_L1_03_MODEL_INTENT_t2.pt', 'T896_L1_04_MODEL_PREDICTION_t2.pt', 'T896_L1_05_OBSERVED_OUTCOME_t2.pt',
                  'T896_L2_00_MODEL_INTENT_t1.pt', 'T896_L2_01_MODEL_PREDICTION_t1.pt', 'T896_L2_02_OBSERVED_OUTCOME_t1.pt',
                  'T896_L3_00_MODEL_INTENT_t1.pt', 'T896_L3_01_MODEL_PREDICTION_t1.pt', 'T896_L3_02_OBSERVED_OUTCOME_t1.pt',
                  'T896_L1_CTRL_FACTUAL_DELETED_05.pt', 'T896_L2_CTRL_PLACEBO_PRED_01.pt', 'T896_L3_CTRL_PLACEBO_PRED_01.pt')
T898_AUDIT_FILES = {'results': 'NPDM_SMOKE_results.json', 'manifest': 'NPDM_SMOKE_public_manifest_SEALED.json',
                    'cell': 'NPDM_SMOKE_cell_source.py', 'events': 'NPDM_SMOKE_events.jsonl', 'log': 'NPDM_SMOKE.log'}
# Names given by the TEST898 contract; GATE0 checks every one against the archived records (any mismatch = BLOCKER)
T898_EXPECT = {'L1': {'discrepancy_t': 2, 'decision_t': 3, 'focal_action': 'QBDGFXVPDHL', 'pred': 'LLRMKGCXHTJ', 'obs': 'WLCQRTSLXJ'},
               'L2': {'discrepancy_t': 1, 'decision_t': 2, 'focal_action': 'RZBBGDWWXN', 'pred': 'CQTZRPXXQSW', 'obs': 'CNGMQRXGVT',
                      'u': 'JGHDDXRDWSRG', 'goal': 'CQTZRPXXQSW'},
               'L3': {'discrepancy_t': 1, 'decision_t': 2, 'focal_action': 'PKCCWRJZPHGS', 'pred': 'VKTRVXDRDDSH', 'obs': 'CZJPSVHNPF',
                      'u': 'MCHZHSBPKC', 'goal': 'VKTRVXDRDDSH'}}
# Optimal sets stated in the contract; ONLY compared with the offline evaluator after all generations (never used before)
T898_TABLE = {'L1': [['ACT', 'QBDGFXVPDHL']], 'L1_FD': [['ACQUIRE', 'FRJVLDCZZDLJK'], ['ACQUIRE', 'QBDGFXVPDHL']],
              'L2': [['ACT', 'SQWLVGDQLTMKD'], ['ACT', 'ZSRWWMFBWPJB']], 'L2_GCF': [['ACT', 'RZBBGDWWXN']],
              'L3': [['ACQUIRE', 'HVPMSVKPSBJW'], ['ACQUIRE', 'XMGTVVSMZNF']], 'L3_GCF': [['ACT', 'PKCCWRJZPHGS']]}
CONSOL_INSTR_898 = ('Do not choose an action now. Write your updated belief state, using only the INFORMATION above and these rules. '
                    'Reply with exactly these seven lines and nothing else, each value written by you:\n'
                    'FACTS: <every action whose outcome you have observed, as action -> outcome>\n'
                    'LAST_PRED: <your most recent prediction and the action it was for>\n'
                    'REL: <how that prediction relates to the outcome that was then observed>\n'
                    'UNKNOWN: <the actions whose outcome you have not observed>\n'
                    'GOAL: <whether you know which action produces the goal outcome, and from which observation>\n'
                    'INFO_VALUE: <whether acquiring an outcome can still give new information, and whether that is worth its cost>\n'
                    'BUDGET_STOP: <the decisions left, and whether stopping now would be better than continuing>')
BELIEF_TPL_898 = 'Step {t}: my own belief state, written after step {t}:\n{B}\n'
# Pre-registered neutral vocabularies (fixed before the run). Each word must be ONE Qwen2 token in the leading-space form
# and the 16 token IDs must be distinct; otherwise NO_RUN (never a silent substitution). Word -> token checked on CPU with
# the Qwen2 vocabulary: K3.1's ' orchard', ' pebble', ' meadow' are two tokens each and were replaced by ' harbor',
# ' violin', ' kettle' at the same positions.
NEUTRAL_WORDS_899 = {'NEUTRAL1': (' cedar', ' marble', ' lantern', ' copper', ' velvet', ' harbor', ' violin', ' canvas'),
                     'NEUTRAL2': (' window', ' pencil', ' river', ' candle', ' silver', ' kettle', ' button', ' paper')}
ZIP_LIMITS_898 = {'max_members': 20000, 'max_member_bytes': 1073741824, 'max_total_bytes': 25769803776, 'max_ratio': 200}   # 1 GiB / 24 GiB; fixed before the run
MAX_NEW_B = 256                                   # consolidation generation length (fixed before the run)
ABORT['consolidation_s'] = 600.0                  # post-operation guard for one B_t generation
NS_DIRS.update(belief=CART_DIR / 'belief', cf=CART_DIR / 'cf')
for _d in NS_DIRS.values(): _d.mkdir(exist_ok=True)
GATE0 = ('ENV', 'SOURCE', 'EXTRACT', 'GATE0_ARCHIVE', 'GATE0B_898_ARCHIVE', 'GATE0C_GEOMETRY', 'MODEL', 'GATE1_ENGINE')
GATE1 = ('GATE2_PHYSICAL_CONTROLS', 'GATE3_READOUT', 'GATE0_ARCHIVE_END', 'P1_PHYSICAL', 'P7_INTEGRITY')
GATE_ORDER = GATE0 + GATE1[:2] + ('GATE4_OFFLINE_EVALUATION',) + GATE1[2:]
CRITICAL = GATE0 + GATE1
REQUIRED = ()
R = {'test': 'TEST899_BP', 'stage': 'L1 native belief-to-policy causal isolation with exact token geometry', 'run_id': RUN_ID,
     'commit': COMMIT, 'status': 'STARTED', 'checks': [],
     'gates': {g: {'status': 'NOT_RUN', 'reason': None, 'data': {}} for g in GATE_ORDER},
     'history': {'TEST885': 'NEGATIVE', 'TEST893': 'FAIL_NO_GAIN', 'TEST894': 'UNDECIDABLE', 'TEST895': 'UNDECIDABLE',
                 'TEST896': 'PASS in log (DIRECT_EXPERIENCE_SUPPORTED, guided exploration); artefacts UNVERIFIED',
                 'TEST897': 'NPDM_FAIL (WRONG_DIRECTION_CHANGE, G3 FAIL); input of this run', 'note': 'locked; not modified, not reinterpreted'},
     'model_revision': MODEL_REVISION, 'runtime_pins': dict(PINS, torch=TORCH_REQ, cuda=CUDA_REQ),
     'scope': 'L1 mechanism isolation only; not learning, not transfer, not autonomy, not incremental utility', 'input_archive': T897, 'input_archive_898': None,
     'executed_by_author': False, 'tolerances': TOL, 'abort_limits': ABORT, 'protocol': PROTO,
     'tolerances_sha256': hashlib.sha256(json.dumps({'TOL': TOL, 'ABORT': ABORT, 'PROTO': PROTO}, sort_keys=True).encode()).hexdigest()}
R['input_archive_898'] = T898IN
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
    assert status in ('PASS', 'FAIL', 'INCONCLUSIVE', 'DIAGNOSTIC', 'NOT_RUN', 'SMOKE_CAUSAL_PASS', 'SMOKE_CAUSAL_PASS_LIMITED', 'PASS_SUPPORT', 'INCONCLUSIVE_SUPPORT',
                      'NRBC_SCREEN_SUPPORT', 'NRBC_SCREEN_INCONCLUSIVE', 'NRBC_SCREEN_FAIL'), status
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
                         'OUTCOME_LEFT_OUT', 'NO_OUTCOME_SHOWN', 'OUTCOME_OMITTED', 'OUTCOME_NOT_GIVEN',
                         'OUTCOME_WAS_WITHHELD', 'OUTCOME_NOT_REVEALED')}   # last two: 7 Qwen2 tokens, = PREDICTION_WITHHELD
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
# ---------------------------------------------------------------------------- TEST899 BELIEF-TO-POLICY pure functions (no model, no vault)
B_FIELDS_898 = ('FACTS', 'LAST_PRED', 'REL', 'UNKNOWN', 'GOAL', 'INFO_VALUE', 'BUDGET_STOP')
# Pre-registered, task-general lexical classes for the five non-factual fields (reported per belief; the model's text is
# never edited). Order matters where one pattern contains another (negations are tested first).
REL_RX_898 = (('MISMATCH', r"\b(did not match|didn't match|does not match|doesn't match|not match|mismatch\w*|differ\w*|different|wrong|incorrect|"
                           r"not the same|not correct|not as predicted)\b"),
              ('UNKNOWN', r"\b(unknown|not observed|withheld|not known|no outcome|not shown|not available|cannot compare|can't compare)\b"),
              ('MATCH', r"\b(match(?:ed|es)?|same|correct|as predicted|confirmed)\b"))
INFO_RX_898 = (('NOT_WORTH', r"\b(not worth|no new information|not useful|unnecessary|no need|not needed|no value|not valuable|no further information|"
                             r"not beneficial|cannot give new information|can't give new information)\b"),
               ('WORTH', r"\b(worth|useful|valuable|beneficial|new information)\b"))
STOP_RX_898 = (('CONTINUE', r"\b(would not be better|is not better|not better|should not stop|shouldn't stop|do not stop|don't stop)\b"),
               ('STOP', r"\b(stopping (?:now )?(?:would be|is) better|should stop|better to stop|stop now)\b"),
               ('CONTINUE', r"\bcontinu\w*\b"))
NEG_KNOW_RX_898 = r"\b(not known|unknown|do not know|don't know|not yet|no action|none|not observed)\b"
NUM_WORDS_898 = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}

def ledger_files_898(R7, eid, n):
    """TEST897 archive schema (LedgerNPDM / run_episode_npdm): R7['episodes'][eid]['ledger'][i] = [record, sha256, ledger_ns]
    (ledger_ns = monotonic clock of the ledger append), R7['cartridges'] = forge index entries. The i-th ledger record is
    bound to its cartridge ONLY through the SHA-256: exactly one index entry, and that entry must agree on record kind, turn,
    namespace (prediction / factual, also the parent directory), cid = '<eid>_<ii>_<kind>_t<t>' (= the file name), role, the
    global parent chain (previous ledger SHA) and strictly increasing ledger / forge times. Anything missing, ambiguous or
    different raises (fail-closed). Returns [{'file', 'sha256', 'cid', 'namespace'}] for the first n records."""
    led = ((R7.get('episodes') or {}).get(eid) or {}).get('ledger')
    if not isinstance(led, list) or len(led) < n: raise RuntimeError('LEDGER_MISSING_OR_SHORT %s' % eid)
    by_sha = {}
    for c in R7.get('cartridges') or []: by_sha.setdefault(c.get('sha256'), []).append(c)
    out = []; prev_sha = prev_ns = prev_mono = None
    for i in range(n):
        x = led[i]
        if not (isinstance(x, (list, tuple)) and len(x) == 3 and isinstance(x[0], dict) and isinstance(x[1], str) and
                re.fullmatch(r'[0-9a-f]{64}', x[1]) is not None and isinstance(x[2], int) and not isinstance(x[2], bool)):
            raise RuntimeError('LEDGER_SCHEMA %s[%d]: expected [record, sha256, ledger_ns]' % (eid, i))
        rec, sh, ns = x
        cands = by_sha.get(sh, [])
        if len(cands) != 1: raise RuntimeError('LEDGER_SHA_MATCHES_%d_INDEX_ENTRIES %s[%d] %s' % (len(cands), eid, i, sh[:16]))
        c = cands[0]; kind = rec.get('kind')
        ns_exp = 'prediction' if kind == 'MODEL_PREDICTION' else 'factual'
        cid_exp = '%s_%02d_%s_t%d' % (eid, i, kind, rec.get('t', 0))
        f_ = str(c.get('file', '')).replace('\\', '/'); fname = f_.rsplit('/', 1)[-1]; pdir = f_.rsplit('/', 2)[-2] if f_.count('/') >= 1 else ''
        chk = {'record_kind': c.get('record_kind') == kind, 'turn': c.get('turn') == rec.get('t'),
               'namespace': c.get('namespace') == ns_exp and pdir == ns_exp, 'cid_and_file_name': c.get('cid') == cid_exp and fname == 'T896_' + cid_exp + '.pt',
               'role': c.get('role') == 'live_' + ns_exp, 'global_parent_chain': c.get('global_parent_sha256') == prev_sha,
               'ledger_time_increasing': prev_ns is None or ns > prev_ns,
               'forge_time_increasing': isinstance(c.get('monotonic_ns'), int) and (prev_mono is None or c['monotonic_ns'] > prev_mono)}
        bad = [k for k, v in chk.items() if not v]
        if bad: raise RuntimeError('LEDGER_INDEX_MISMATCH %s[%d] %s: %s' % (eid, i, cid_exp, ', '.join(bad)))
        out.append({'file': fname, 'sha256': sh, 'cid': c['cid'], 'namespace': ns_exp})
        prev_sha, prev_ns, prev_mono = sh, ns, c['monotonic_ns']
    if len({o_['file'] for o_ in out}) != n or len({o_['sha256'] for o_ in out}) != n: raise RuntimeError('LEDGER_FILES_NOT_UNIQUE %s' % eid)
    return out

def parse_belief_898(text):
    """Strict, pre-registered: exactly seven non-empty lines, in the fixed order, each 'FIELD: value' with a non-empty value.
    Nothing is repaired or filled in by the harness; anything else is INVALID."""
    lines = [l.strip() for l in (text or '').strip().split('\n') if l.strip()]
    out = {}
    if len(lines) != len(B_FIELDS_898): return {'valid': False, 'why': 'LINE_COUNT_%d' % len(lines), 'fields': out}
    for f, l in zip(B_FIELDS_898, lines):
        if not l.startswith(f + ':'): return {'valid': False, 'why': 'FIELD_ORDER_' + f, 'fields': out}
        v = l[len(f) + 1:].strip()
        if not v: return {'valid': False, 'why': 'EMPTY_' + f, 'fields': out}
        out[f] = v
    return {'valid': True, 'why': None, 'fields': out}

def names_in_order_898(text, names):
    # public names are pairwise non-overlapping (TEST897 generator: no name contains another), so plain find() is exact
    hits = []
    for n in names:
        i = text.find(n)
        while i >= 0: hits.append((i, n)); i = text.find(n, i + len(n))
    return [n for i, n in sorted(hits)]

def belief_facts_898(fields, pub):
    """(action, outcome) pairs stated in the FACTS line: each public action name paired with the next public outcome name
    before the next action name."""
    acts, outs = list(pub['actions']), list(pub['outcomes'])
    pairs = set(); a = None
    for n in names_in_order_898(fields.get('FACTS', ''), acts + outs):
        if n in acts: a = n
        elif a is not None: pairs.add((a, n)); a = None
    return pairs

def belief_truth_898(records, pub):
    """Ground truth for the reconciliation fields, from the records the model saw (general, not state-specific): the last
    MODEL_PREDICTION, the action of the MODEL_INTENT of the same step, and REL = MATCH / MISMATCH against the observed outcome of
    that step, or UNKNOWN if that outcome is absent or is not a public outcome name (withheld)."""
    preds = [r for r in records if r['kind'] == 'MODEL_PREDICTION']
    if not preds: return {'last_pred': None, 'last_pred_action': None, 'rel_true': 'UNKNOWN'}
    lp = preds[-1]; t = lp['t']
    act = [r['A'] for r in records if r['kind'] == 'MODEL_INTENT' and r['t'] == t]
    obs = [r['O'] for r in records if r['kind'] == 'OBSERVED_OUTCOME' and r['t'] == t and r['O'] in pub['outcomes']]
    return {'last_pred': lp['P'], 'last_pred_action': act[0] if act else None, 'last_pred_t': t,
            'rel_true': 'UNKNOWN' if not obs else ('MATCH' if obs[0] == lp['P'] else 'MISMATCH')}

def lex_class_898(text, table):
    t = (text or '').lower()
    for cls, rx in table:
        if re.search(rx, t): return cls
    return 'UNCLASSIFIED'

def belief_eval_898(parsed, pub, true_facts, last_pred, last_pred_action, rel_true, left, optimal):
    """Offline evaluation of ONE belief, in separate dimensions that are never merged:
    syntax (strict parser) / factual core (FACTS + UNKNOWN exact) / reconciliation (LAST_PRED names the last prediction and its
    action, REL lexical class == true relation) / goal status / decision relevance (INFO_VALUE and BUDGET_STOP lexical class
    == the public-Bayes optimal set, BUDGET_STOP names the decisions left). Policy effect is measured by the readouts, not here."""
    if not parsed.get('valid'):
        return {'syntax_valid': False, 'why': parsed.get('why'), 'core_correct': False, 'reconciliation_correct': False, 'goal_correct': False,
                'decision_relevance_correct': False, 'all_fields_correct': False}
    f = parsed['fields']; facts = belief_facts_898(f, pub); tf = {tuple(x) for x in true_facts}
    acts = list(pub['actions'])
    unk = set(names_in_order_898(f['UNKNOWN'], acts)); true_unk = {a for a in acts if a not in {x for x, _ in tf}}
    lp_ok = (last_pred in f['LAST_PRED'] and last_pred_action in f['LAST_PRED']) if last_pred else None
    rel_cls = lex_class_898(f['REL'], REL_RX_898)
    # GOAL: known (some observed action produced the goal) -> that action is named; not known -> a not-known expression is present
    # and no action whose outcome is UNOBSERVED is named (naming an observed non-goal action as evidence is allowed)
    gact = [a for a, o in tf if o == pub['goal']]
    if gact: goal_ok = gact[0] in f['GOAL']
    else: goal_ok = (re.search(NEG_KNOW_RX_898, f['GOAL'].lower()) is not None and
                     not (set(names_in_order_898(f['GOAL'], acts)) & set(true_unk)))
    # INFO_VALUE / BUDGET_STOP truth from the public-Bayes optimal set of the belief's own world; a tie across classes accepts both
    okeys = {key_898(x) for x in optimal}
    n_acq = sum(1 for k in okeys if k.startswith("('ACQUIRE'"))
    info_true = 'WORTH' if n_acq == len(okeys) else ('NOT_WORTH' if n_acq == 0 else 'INDIFFERENT')
    stop_true = 'STOP' if okeys == {'STOP'} else ('CONTINUE' if 'STOP' not in okeys else 'INDIFFERENT')
    info_cls, stop_cls = lex_class_898(f['INFO_VALUE'], INFO_RX_898), lex_class_898(f['BUDGET_STOP'], STOP_RX_898)
    left_named = (re.search(r'(?<![\d.])%d(?![\d.])' % left, f['BUDGET_STOP']) is not None or
                  re.search(r'\b%s\b' % NUM_WORDS_898.get(left, '#'), f['BUDGET_STOP'].lower()) is not None)
    r = {'syntax_valid': True, 'facts_stated': sorted(facts), 'facts_true': sorted(tf), 'facts_correct': facts == tf,
         'unknown_stated': sorted(unk), 'unknown_true': sorted(true_unk), 'unknown_correct': unk == true_unk,
         'core_correct': facts == tf and unk == true_unk,
         'last_pred_correct': lp_ok, 'rel_class': rel_cls, 'rel_true': rel_true, 'rel_correct': rel_cls == rel_true,
         'goal_known_true': bool(gact), 'goal_correct': bool(goal_ok),
         'info_class': info_cls, 'info_true': info_true,
         'info_correct': info_cls == info_true or (info_true == 'INDIFFERENT' and info_cls in ('WORTH', 'NOT_WORTH')),
         'stop_class': stop_cls, 'stop_true': stop_true,
         'stop_correct': stop_cls == stop_true or (stop_true == 'INDIFFERENT' and stop_cls in ('STOP', 'CONTINUE')), 'left_named': left_named}
    r['reconciliation_correct'] = bool(lp_ok) and r['rel_correct']
    r['decision_relevance_correct'] = r['info_correct'] and r['stop_correct'] and left_named
    r['all_fields_correct'] = r['core_correct'] and r['reconciliation_correct'] and r['goal_correct'] and r['decision_relevance_correct']
    return r

def key_898(z):
    return str(tuple(z)) if isinstance(z, (list, tuple)) else str(z)

def in_opt_898(z, O):
    return z is not None and key_898(z) in {key_898(x) for x in (O or [])}

class NoRun899(Exception): pass

def enc899(text):
    """Token IDs and EXACT char offsets of every token, derived from the token byte strings themselves (decode of each single
    token, concatenated, must reproduce the text byte-for-byte; ASCII text, so byte offset == char offset). The HF
    offset_mapping depends on the post-processor trim_offsets setting (Qwen2: ByteLevel(trim_offsets=False)); it is kept as
    audit metadata only and is never the boundary definition."""
    if not text.isascii(): raise NoRun899('BELIEF_TEXT_NOT_ASCII')
    ids = list(tok(text, add_special_tokens=False).input_ids)
    pieces = [tok.decode([i], clean_up_tokenization_spaces=False) for i in ids]
    if ''.join(pieces) != text: raise NoRun899('TOKEN_BYTES_DO_NOT_REPRODUCE_TEXT')
    offs, c = [], 0
    for p_ in pieces: offs.append((c, c + len(p_))); c += len(p_)
    return ids, offs

def geometry899(text, raw):
    """Exact physical token geometry of one belief record. Field value region = [colon end, line end): in Qwen2 byte-level
    BPE the single space after 'FIELD:' is fused with the first value token (' ACQUIRE' -> 'ĠAC' ...), so the value region
    starts AT that space. Every token lies entirely inside one value region or entirely outside all of them; the colon token
    ends exactly where the value region begins; the line break after each value is a non-content token. Content = tokens of
    the value regions; non-content = template prefix, field names, colons, line breaks (compared as exact (position, id))."""
    ids, offs = enc899(text)
    if text.count(raw) != 1: raise NoRun899('RAW_NOT_UNIQUE_IN_TEXT')
    start = text.index(raw); spans = []; cursor = start; lines = raw.split('\n')
    if len(lines) != len(B_FIELDS_898): raise NoRun899('BELIEF_LINE_COUNT_%d' % len(lines))
    for field, line in zip(B_FIELDS_898, lines):
        if not (line.startswith(field + ': ') and text.startswith(line, cursor)): raise NoRun899('FIELD_BOUNDARY_NOT_EXACT ' + field)
        vs = cursor + len(field) + 1; ce = cursor + len(line)
        pos = [i for i, (a, b) in enumerate(offs) if a >= vs and b <= ce and b > a]
        overlap = [i for i, (a, b) in enumerate(offs) if a < ce and b > vs and b > a]
        if not pos or pos != overlap or pos != list(range(pos[0], pos[-1] + 1)) or offs[pos[0]][0] != vs or offs[pos[-1]][1] != ce:
            raise NoRun899('TOKEN_CROSSES_FIELD_BOUNDARY ' + field)
        if pos[0] == 0 or offs[pos[0] - 1][1] != vs: raise NoRun899('COLON_TOKEN_NOT_ADJACENT ' + field)
        spans.append({'field': field, 'char': [vs, ce], 'token': [pos[0], pos[-1] + 1], 'n': len(pos)})
        cursor = ce + 1
    if cursor != len(text) or text[start + len(raw):] != '\n': raise NoRun899('BELIEF_TEMPLATE_TRAILING_BOUNDARY_MISMATCH')
    content = {i for s in spans for i in range(s['token'][0], s['token'][1])}
    noncontent = [[i, x] for i, x in enumerate(ids) if i not in content]
    return {'ids': ids, 'offsets': offs, 'spans': spans, 'content_positions': sorted(content),
            'noncontent_sha256': sha_bytes(json.dumps(noncontent).encode()), 'sha256': sha_bytes(text.encode())}

def geometry_signature899(geo):
    return [(s['field'], list(s['token']), s['n']) for s in geo['spans']]

def assert_same_geometry899(ref, other, label):
    if (len(other['ids']) != len(ref['ids']) or geometry_signature899(other) != geometry_signature899(ref) or
        other['noncontent_sha256'] != ref['noncontent_sha256']):
        raise NoRun899('EXACT_GEOMETRY_UNSAT ' + label)

def neutral899(real_text, real_raw, ref, words):
    repl = []
    for w in words:
        ids, _ = enc899(w)
        if len(ids) != 1: raise NoRun899('NEUTRAL_CANDIDATE_NOT_ONE_TOKEN ' + w)
        if ids[0] in repl: raise NoRun899('NEUTRAL_CANDIDATE_TOKEN_NOT_UNIQUE ' + w)
        repl.append(ids[0])
    if len(repl) != len(words): raise NoRun899('NEUTRAL_ONE_TOKEN_VOCABULARY_INSUFFICIENT')
    ids = list(ref['ids'])
    for j, p in enumerate(ref['content_positions']): ids[p] = repl[j % len(repl)]
    text = tok.decode(ids, clean_up_tokenization_spaces=False)
    ids2, _ = enc899(text)
    if ids2 != ids: raise NoRun899('NEUTRAL_DECODE_REENCODE_NOT_EXACT')
    prefix = real_text[:real_text.index(real_raw)]
    if not (text.startswith(prefix) and text.endswith('\n')): raise NoRun899('NEUTRAL_TEMPLATE_CHANGED')
    raw = text[len(prefix):-1]; parsed = parse_belief_898(raw)
    if not parsed['valid']: raise NoRun899('NEUTRAL_NOT_PARSER_VALID')
    forbidden = re.compile(r'\b(act|acquire|stop|goal|reward|known|unknown|correct|incorrect|match|mismatch|worth|continue|yes|no|not|better)\b', re.I)
    for field, value in parsed['fields'].items():
        if forbidden.search(value) or re.search(r'\d', value) or any(n in value for n in PUB['L1']['actions'] + PUB['L1']['outcomes']):
            raise NoRun899('NEUTRAL_SEMANTIC_OR_PUBLIC_NAME_LEAK ' + field)
    return text, raw, geometry899(text, raw)

def swapped899(real_text, real_raw, ref, pub, true_facts):
    """Pre-registered SWAPPED control: the public ACTION names inside REAL are permuted; outcome names (and therefore the
    public goal outcome) are kept, so the control is a coherent but factually wrong belief (wrong action -> outcome
    attribution, wrong goal-producing action, wrong UNKNOWN). Permutations are tried in itertools order of the public action
    list, identity excluded; the first one that is parser-valid, has a factual core different from the public frozen facts
    and has exactly the REAL token geometry is used. Only public names and the already-public frozen facts are used."""
    import itertools
    acts = list(pub['actions'])
    def rotate(text, mp):
        if '\x00' in text: raise NoRun899('NUL_IN_BELIEF_TEXT')
        tmp = text
        for i, k in enumerate(mp): tmp = tmp.replace(k, '\x00%d\x00' % i)
        for i, k in enumerate(mp): tmp = tmp.replace('\x00%d\x00' % i, mp[k])
        return tmp
    tried = []
    for ap in itertools.permutations(acts):
        if list(ap) == acts: continue
        am = dict(zip(acts, ap)); raw = rotate(real_raw, am); text = BELIEF_TPL_898.format(t=2, B=raw)
        tried.append(list(ap)); parsed = parse_belief_898(raw)
        if not parsed['valid']: continue
        if belief_facts_898(parsed['fields'], pub) == {tuple(x) for x in true_facts}: continue
        geo = geometry899(text, raw)
        if (len(geo['ids']) == len(ref['ids']) and geometry_signature899(geo) == geometry_signature899(ref) and
                geo['noncontent_sha256'] == ref['noncontent_sha256']):
            return text, raw, geo, {'action_permutation': am, 'outcome_permutation': 'IDENTITY', 'tried': tried}
    raise NoRun899('SWAPPED_EXACT_GEOMETRY_UNSAT_AFTER_5_PREREGISTERED_ACTION_PERMUTATIONS')

def action_prefix899(raw, contract):
    """Offline, descriptive: the ACTION the model wrote, independent of the prediction slot. STOP -> 'STOP';
    'ACT|ACQUIRE <public action> ...' -> [kind, action] (whatever follows); anything else -> None. Read from the model's own
    text after all generations; never used for, or fed back into, any decision."""
    toks = (raw or '').strip().split()
    if toks and toks[-1].endswith('.'): toks[-1] = toks[-1][:-1]
    if toks == ['STOP']: return 'STOP'
    if len(toks) >= 2 and toks[0] in ('ACT', 'ACQUIRE') and toks[1] in set(contract['actions']): return [toks[0], toks[1]]
    return None

def classify899(rows, OPT, contract, swapped_goal_action):
    """Pre-registered TEST899 GATE4 table. rows[(arm, grammar)] = {'gen','raw','decision','parse_status','pred_status'}.
    Two levels are kept apart: DECISION = the native grammar decision (an INVALID output, e.g. PRED with an UNKNOWN
    prediction, is WASTE) and ACTION = the action prefix the model wrote (independent of the prediction slot). A decision
    change whose action prefix is unchanged is a PREDICTION-SLOT VALIDITY change, not a policy (action) change."""
    def k_(z): return key_898(tuple(z) if isinstance(z, list) else z)
    def ak(a): return None if a is None else k_(a)
    sc = {}
    for (arm, gr), g in rows.items():
        z = tuple(g['decision']) if isinstance(g['decision'], list) else g['decision']; a = action_prefix899(g['raw'], contract)
        sc[(arm, gr)] = {'gen': g['gen'], 'decision_key': k_(z), 'optimal': in_opt_898(z, OPT), 'action_prefix': a,
                         'action_prefix_optimal': a is not None and (a == 'STOP' and 'STOP' in {k_(x) for x in OPT} or
                                                                     a != 'STOP' and in_opt_898(tuple(a), OPT)),
                         'parse_status': g['parse_status'], 'pred_status': g['pred_status']}
    def pair(a, b):
        A, B = sc[a], sc[b]; dch = A['decision_key'] != B['decision_key']; ach = ak(A['action_prefix']) != ak(B['action_prefix'])
        rch = rows[a]['raw'] != rows[b]['raw']
        return {'a': A['gen'], 'b': B['gen'], 'decision_changed': dch, 'action_changed': ach, 'raw_changed': rch,
                'type': 'ACTION' if ach else ('PRED_SLOT_VALIDITY_ONLY' if dch else ('RAW_ONLY' if rch else 'NONE')),
                'a_decision': A['decision_key'], 'b_decision': B['decision_key'], 'a_action': ak(A['action_prefix']), 'b_action': ak(B['action_prefix'])}
    cp = {n: pair(('REAL', 'PRED'), (n, 'PRED')) for n in ('NEUTRAL1', 'SWAPPED', 'NEUTRAL2')}
    cd = {n: pair(('REAL', 'DIRECT'), (n, 'DIRECT')) for n in ('NEUTRAL1', 'NEUTRAL2')}
    gp = {n: pair((n, 'PRED'), (n, 'DIRECT')) for n in ('F', 'REAL', 'NEUTRAL1', 'NEUTRAL2')}
    grammar_contribution = (not sc[('REAL', 'PRED')]['optimal']) and sc[('REAL', 'DIRECT')]['optimal'] and sc[('F', 'DIRECT')]['optimal']
    content_dec = any(v['decision_changed'] for v in list(cp.values()) + list(cd.values()))
    content_act = any(v['action_changed'] for v in list(cp.values()) + list(cd.values()))
    cond = {'grammar_contribution': grammar_contribution,
            'grammar_effect_type_REAL': gp['REAL']['type'],
            'decision_content_influence_PRED': any(v['decision_changed'] for v in cp.values()),
            'decision_content_influence_DIRECT': any(v['decision_changed'] for v in cd.values()),
            'action_content_influence_PRED': any(v['action_changed'] for v in cp.values()),
            'action_content_influence_DIRECT': any(v['action_changed'] for v in cd.values()),
            'neutral_baseline_stable': all(sc[('NEUTRAL1', g)]['decision_key'] == sc[('NEUTRAL2', g)]['decision_key'] for g in ('PRED', 'DIRECT')),
            'neutral_baseline_stable_action': all(ak(sc[('NEUTRAL1', g)]['action_prefix']) == ak(sc[('NEUTRAL2', g)]['action_prefix']) for g in ('PRED', 'DIRECT')),
            'all_four_PRED_nonoptimal_geometry_pattern': all(not sc[(n, 'PRED')]['optimal'] for n in ('REAL', 'NEUTRAL1', 'SWAPPED', 'NEUTRAL2')),
            'correctness_specific_content_preservation': sc[('REAL', 'PRED')]['optimal'] and
                                                         all(not sc[(n, 'PRED')]['optimal'] for n in ('NEUTRAL1', 'SWAPPED', 'NEUTRAL2')),
            'correctness_specific_content_preservation_action': sc[('REAL', 'PRED')]['action_prefix_optimal'] and
                                                                all(not sc[(n, 'PRED')]['action_prefix_optimal'] for n in ('NEUTRAL1', 'SWAPPED', 'NEUTRAL2')),
            'swapped_follows_swapped_belief': ak(sc[('SWAPPED', 'PRED')]['action_prefix']) == k_(('ACT', swapped_goal_action)) if swapped_goal_action else None}
    if grammar_contribution and content_act: v = 'MECHANISM_GRAMMAR_AND_CONTENT'
    elif grammar_contribution: v = 'MECHANISM_GRAMMAR_CONTRIBUTION'
    elif content_act: v = 'MECHANISM_CONTENT_INFLUENCE'
    elif content_dec: v = 'MECHANISM_CONTENT_AFFECTS_PRED_SLOT_VALIDITY_ONLY'
    else: v = 'MECHANISM_NO_DECISION_LEVEL_EFFECT'
    return {'verdict': v, 'conditions': cond, 'scores': {'%s/%s' % k: x for k, x in sc.items()}, 'content_pairs_PRED': cp,
            'content_pairs_DIRECT': cd, 'grammar_pairs': gp}

def car_close899(a, b, tol):
    if a['n_tokens'] != b['n_tokens'] or len(a['token_logp']) != len(b['token_logp']): return False
    vals = a['token_logp'] + b['token_logp']
    if not all(math.isfinite(float(x)) for x in vals): return False
    if max((abs(float(x) - float(y)) for x, y in zip(a['token_logp'], b['token_logp'])), default=0.0) > tol: return False
    if abs(float(a['sum_logp']) - float(b['sum_logp'])) > tol: return False
    return all(k in a['first_token_logp'] and k in b['first_token_logp'] and
               abs(float(a['first_token_logp'][k]) - float(b['first_token_logp'][k])) <= tol for k in ('ACT','ACQUIRE','STOP'))

def classify_898(S):
    """Pre-registered verdict table. S[eid] (eid in L1 L2 L3): O, z_real, z_sham, z_filter (this runtime), b_real (belief eval),
    sham_valid, geometry_equal; L1 adds z_fd / z_fd_f (FD with / without B_t), O_fd, fd_leak, focal_action; L2 / L3 add z_pa / z_pa_f,
    O_pa, z_gcf / z_gcf_f, O_gcf (with / without B_t, same factual mount, query, grammar and settings).
    Conditions: c1 L1 REAL optimal and FD (with B) clean; c2 L2 and L3 REAL optimal while FILTER_ONLY is not; c3 correctness
    specificity: in L2 and L3 the SHAM decision is NOT optimal (raw content sensitivity = SHAM != REAL is reported separately);
    c4a system-level outcome tracking with B (PA and GCF optimal and different); c4b that tracking is attributable to B_t (the same
    PA / GCF pair WITHOUT B does not track); c5 REAL beliefs core-correct (FACTS + UNKNOWN). Order: c1 c2 c4a c4b c5 must hold
    ('core'); then, if the L2 / L3 content comparison is not testable (SHAM invalid or REAL / SHAM belief token counts unequal) ->
    NRBC_SCREEN_INCONCLUSIVE (never FAIL for an untestable comparison); else c3 decides SUPPORT / FAIL. Not core -> FAIL."""
    lab = {}; st = {}
    for e in ('L1', 'L2', 'L3'):
        s = S[e]; L = []
        real_ok, filt_ok = in_opt_898(s['z_real'], s['O']), in_opt_898(s['z_filter'], s['O'])
        sham_ok = in_opt_898(s.get('z_sham'), s['O'])
        same_rf = s['z_real'] is not None and key_898(s['z_real']) == key_898(s['z_filter'])
        if s['z_real'] is None: L.append('REAL_NOT_RUN_B_INVALID')
        elif key_898(s['z_real']) in ('WASTE', 'STOP') and not real_ok: L.append('REAL_ACTION_INVALID_OR_STOP_POLICY_FAIL')
        if real_ok and filt_ok and same_rf: L.append('REAL_EQUALS_FILTER_OPTIMAL_NO_INCREMENT_SHOWN')
        if (not real_ok) and same_rf: L.append('REAL_EQUALS_FILTER_NONOPTIMAL_NO_INCREMENT')
        inc = real_ok and not filt_ok
        if inc: L.append('INCREMENTAL_OVER_FILTER')
        if real_ok and filt_ok and not same_rf: L.append('REAL_AND_FILTER_BOTH_OPTIMAL_DIFFERENT')
        if (not real_ok) and filt_ok and s['z_real'] is not None: L.append('REAL_WORSE_THAN_FILTER')
        b_ok = bool((s.get('b_real') or {}).get('core_correct'))
        if b_ok and not real_ok and s['z_real'] is not None: L.append('B_CORE_CORRECT_ACTION_WRONG_POLICY_READOUT_FAIL')
        if (not b_ok) and real_ok: L.append('B_CORE_WRONG_ACTION_RIGHT_ATTRIBUTION_FAIL')
        testable = bool(s.get('sham_valid')) and bool(s.get('geometry_equal'))
        sham_rep = s['z_real'] is not None and s.get('z_sham') is not None and key_898(s['z_sham']) == key_898(s['z_real'])
        raw_sens = testable and s['z_real'] is not None and s.get('z_sham') is not None and not sham_rep
        corr_spec = testable and real_ok and not sham_ok
        if not testable: L.append('CONTENT_COMPARISON_INCONCLUSIVE')
        else:
            if sham_rep: L.append('CONTENT_SPECIFIC_NOT_SHOWN_SHAM_EQUALS_REAL')
            if raw_sens and sham_ok: L.append('RAW_CONTENT_SENSITIVITY_BUT_SHAM_ALSO_OPTIMAL_NOT_CORRECTNESS_SPECIFIC')
            if raw_sens and not real_ok and not sham_ok: L.append('CONTENT_SENSITIVE_NOT_USEFUL')
            if corr_spec: L.append('CORRECTNESS_SPECIFIC_USEFUL_CORRECTION')
        x = {'real_ok': real_ok, 'filter_ok': filt_ok, 'incremental': inc, 'b_real_core_correct': b_ok, 'content_testable': testable,
             'sham_ok': sham_ok, 'sham_reproduces_real': sham_rep, 'raw_content_sensitivity': raw_sens, 'correctness_specific': corr_spec}
        if e == 'L1':
            act_focal = key_898(s.get('z_fd')) == key_898(('ACT', s['focal_action']))
            fd_ok = in_opt_898(s.get('z_fd'), s.get('O_fd')) and not s.get('fd_leak') and not act_focal
            if s.get('fd_leak') or act_focal: L.append('FD_LEAKAGE_OR_BRANCH_CONTAMINATION_FAIL')
            elif not fd_ok: L.append('FD_NOT_OPTIMAL_WITHOUT_OUTCOME')
            x.update(fd_ok=fd_ok, fd_filter_ok=in_opt_898(s.get('z_fd_f'), s.get('O_fd')),
                     fd_b_changes_decision=s.get('z_fd') is not None and key_898(s.get('z_fd')) != key_898(s.get('z_fd_f')))
        else:
            pa_ok, gcf_ok = in_opt_898(s.get('z_pa'), s.get('O_pa')), in_opt_898(s.get('z_gcf'), s.get('O_gcf'))
            paf_ok, gcff_ok = in_opt_898(s.get('z_pa_f'), s.get('O_pa')), in_opt_898(s.get('z_gcf_f'), s.get('O_gcf'))
            same_cf = s.get('z_pa') is not None and key_898(s.get('z_pa')) == key_898(s.get('z_gcf'))
            same_cf_f = s.get('z_pa_f') is not None and key_898(s.get('z_pa_f')) == key_898(s.get('z_gcf_f'))
            track_b = pa_ok and gcf_ok and not same_cf; track_nob = paf_ok and gcff_ok and not same_cf_f
            if same_cf: L.append('OUTCOME_TRACKING_FAIL_PA_EQUALS_GCF')
            if track_nob: L.append('TRACKING_PRESENT_WITHOUT_B_NOT_ATTRIBUTABLE_TO_B')
            if track_b and not track_nob: L.append('TRACKING_ATTRIBUTABLE_TO_B')
            x.update(pa_ok=pa_ok, gcf_ok=gcf_ok, pa_filter_ok=paf_ok, gcf_filter_ok=gcff_ok, cf_track=track_b, cf_track_without_b=track_nob,
                     cf_track_attributable_to_b=track_b and not track_nob,
                     gcf_b_necessary=gcf_ok and not gcff_ok, pa_b_necessary=pa_ok and not paf_ok)
        lab[e] = L; st[e] = x
    cond = {'c1_L1_real_and_fd_clean': st['L1']['real_ok'] and st['L1']['fd_ok'],
            'c2_L2_L3_incremental_over_filter': st['L2']['incremental'] and st['L3']['incremental'],
            'c3_L2_L3_correctness_specific': (st['L2']['correctness_specific'] and st['L3']['correctness_specific'])
                                             if (st['L2']['content_testable'] and st['L3']['content_testable']) else None,
            'c4a_system_level_outcome_tracking': st['L2']['cf_track'] and st['L3']['cf_track'],
            'c4b_tracking_attributable_to_b': st['L2']['cf_track_attributable_to_b'] and st['L3']['cf_track_attributable_to_b'],
            'c5_b_real_core_correct': all(st[e]['b_real_core_correct'] for e in ('L1', 'L2', 'L3'))}
    testable_decisive = st['L2']['content_testable'] and st['L3']['content_testable']
    core = all(cond[k] for k in ('c1_L1_real_and_fd_clean', 'c2_L2_L3_incremental_over_filter', 'c4a_system_level_outcome_tracking',
                                 'c4b_tracking_attributable_to_b', 'c5_b_real_core_correct'))
    if core and not testable_decisive: v, why = 'NRBC_SCREEN_INCONCLUSIVE', 'CONTENT_SPECIFICITY_UNTESTABLE_SHAM_INVALID_OR_GEOMETRY_UNEQUAL'
    elif core and cond['c3_L2_L3_correctness_specific']: v, why = 'NRBC_SCREEN_SUPPORT', 'CORRECTNESS_SPECIFIC_B_INCREMENT_WITH_B_ATTRIBUTABLE_TRACKING'
    else: v, why = 'NRBC_SCREEN_FAIL', 'FAILED: ' + ', '.join(k for k, ok_ in cond.items() if ok_ is False) + (
        '' if testable_decisive else ' (c3 UNTESTABLE: SHAM invalid or geometry unequal)')
    claims = {'raw_content_sensitivity': {e: st[e]['raw_content_sensitivity'] for e in ('L1', 'L2', 'L3')},
              'correctness_specific_useful_correction': {e: st[e]['correctness_specific'] for e in ('L1', 'L2', 'L3')},
              'system_level_outcome_tracking': {e: st[e]['cf_track'] for e in ('L2', 'L3')},
              'b_attributable_outcome_tracking': {e: st[e]['cf_track_attributable_to_b'] for e in ('L2', 'L3')},
              'fd_b_changes_decision': st['L1']['fd_b_changes_decision'],
              'b_necessary_for_optimal_decision': {'PA': {e: st[e]['pa_b_necessary'] for e in ('L2', 'L3')},
                                                   'GCF': {e: st[e]['gcf_b_necessary'] for e in ('L2', 'L3')},
                                                   'FD': st['L1']['fd_ok'] and not st['L1']['fd_filter_ok']}}
    return {'verdict': v, 'reason': why, 'conditions': cond, 'content_testable_L2_L3': testable_decisive, 'labels': lab, 'state': st, 'claims': claims}

try:
    log('=' * 112); log(MARKER, RUN_ID, '| engine commit', COMMIT, '| inputs', T897['run_id'], T898IN['run_id'], '(read-only, unchanged)')
    log('SCOPE: L1 mechanism isolation only. No learning / transfer / autonomy / B necessity / incremental utility claim.'); log('=' * 112)
    log('TOLERANCES', json.dumps(TOL, sort_keys=True), 'sha256', R['tolerances_sha256'])
    # executed-cell identity, single cell. AUTOMATIC and fail-closed: no manual pin, and the cell never contains a hash of
    # itself. The expected identity is derived at run time from the published GitHub repository only: the executed cell must
    # be byte-identical to the file TEST899.py that the default branch publishes right now. Checks (all required):
    #   the default branch resolves to a commit object; the immutable commit that last wrote SRC_FILE is resolved from it;
    #   in that commit (and in the default-branch tree) there is exactly one entry at that literal path, a regular file
    #   (mode 100644/100755, type blob; submodule / symlink / tree refused) with the same blob id in both trees; the git blob
    #   id recomputed over the fetched bytes equals the tree blob; the raw channel at that commit is byte-identical; the
    #   executed cell (IPython history) equals those bytes after ONE canonicalization only: leading and trailing b'\n'
    #   removed on both sides (a pasted cell may gain a leading newline and lose the final one). Interior bytes, CRLF and
    #   spaces are compared exactly. SHA-256, byte count, commit and blob of the verified file are computed here from the
    #   fetched git objects and written to the receipt; no identity from an earlier version is used. Any failure -> the run
    #   stops HERE, before ENV / model load / any GPU work.
    SRC_REPO = 'ceceli33/titan-cognitive-core-v3'; SRC_FILE = 'TEST899.py'
    ec = {'status': 'NOT_CAPTURED', 'identity_match': False, 'src_file': SRC_FILE, 'checks': {}, 'mode': 'AUTOMATIC_FROM_PUBLISHED_DEFAULT_BRANCH'}
    _ck = ec['checks']
    try:
        _hist = list(globals()['get_ipython']().history_manager.input_hist_raw)
        _cell = [x for x in _hist if MARKER in x and 'def integrity_selftest' in x][-1]
        (ROOT / 'TEST899_BP_cell_source.py').write_text(_cell, encoding='utf-8'); _cb = _cell.encode('utf-8')
        ec.update(status='CAPTURED', sha256=sha_bytes(_cb), git_blob=gitblob(_cb), git_blob_with_final_newline=gitblob(_cb + b'\n'),
                  lines=_cell.count('\n') + 1, file=str(ROOT / 'TEST899_BP_cell_source.py'))
    except Exception as e:
        ec['capture_error'] = '%s: %s' % (type(e).__name__, e)
    _ck['cell_captured'] = ec['status'] == 'CAPTURED'
    try:
        _gd = ROOT.parent / ('TEST899_BP_srcid_' + RUN_ID); _genv = dict(os.environ, GIT_TERMINAL_PROMPT='0')
        _git = lambda *a: subprocess.run(['git', '--literal-pathspecs'] + list(a), check=True, capture_output=True, timeout=180, env=_genv).stdout
        _url = 'https://github.com/' + SRC_REPO
        _git('clone', '-q', '--filter=blob:none', '--no-checkout', _url, str(_gd))
        _head = _git('-C', str(_gd), 'rev-parse', '--verify', 'origin/HEAD^{commit}').decode().strip()
        _commit = _git('-C', str(_gd), 'log', '-1', '--format=%H', _head, '--', SRC_FILE).decode().strip()
        _ck['commit_object_exists'] = bool(re.fullmatch(r'[0-9a-f]{40}', _commit or '')) and _git('-C', str(_gd), 'cat-file', '-t', _commit).decode().strip() == 'commit'
        _lt = lambda c: [e for e in _git('-C', str(_gd), 'ls-tree', '-z', c, '--', SRC_FILE).decode('utf-8', 'replace').split('\0') if e]
        _ent, _enth = _lt(_commit), _lt(_head)
        ec['tree_entries'] = _ent
        _meta, _, _pth = (_ent[0].partition('\t') if len(_ent) == 1 else ('', '', ''))
        _mode, _typ, _oid = (_meta.split(' ') + ['', '', ''])[:3]
        _ck['tree_single_entry_exact_path'] = len(_ent) == 1 and _pth == SRC_FILE
        _ck['tree_entry_regular_file'] = _mode in ('100644', '100755') and _typ == 'blob'
        _ck['default_branch_publishes_same_blob'] = _enth == _ent
        _pb = _git('-C', str(_gd), 'cat-file', 'blob', _oid) if _ck['tree_entry_regular_file'] else b''
        _ck['recomputed_blob_equals_tree_blob'] = bool(_pb) and gitblob(_pb) == _oid
        with urllib.request.urlopen(urllib.request.Request('https://raw.githubusercontent.com/%s/%s/%s' % (SRC_REPO, _commit, SRC_FILE),
                                                           headers={'User-Agent': 'AKBASCORE-TEST899_BP'}), timeout=120) as f_:
            _rb = f_.read()
        _ck['raw_channel_equal'] = bool(_pb) and _rb == _pb
        ec['published'] = {'repo': SRC_REPO, 'default_branch_commit': _head, 'commit': _commit, 'path': SRC_FILE, 'tree_mode': _mode,
                           'tree_blob': _oid, 'blob_of_bytes': gitblob(_pb), 'sha256': sha_bytes(_pb), 'bytes': len(_pb)}
        ec['canonicalization'] = "strip leading/trailing b'\\n' on both sides only; interior bytes compared exactly"
        if ec['status'] == 'CAPTURED':
            _cc, _pc = _cb.strip(b'\n'), _pb.strip(b'\n')
            _ck['executed_cell_equals_published_bytes'] = bool(_pb) and _cc == _pc
            ec['boundary_newlines'] = {'cell_leading': len(_cb) - len(_cb.lstrip(b'\n')), 'cell_trailing': len(_cb) - len(_cb.rstrip(b'\n')),
                                       'published_leading': len(_pb) - len(_pb.lstrip(b'\n')), 'published_trailing': len(_pb) - len(_pb.rstrip(b'\n'))}
            if _cc != _pc:
                _i = next((k for k in range(min(len(_cc), len(_pc))) if _cc[k] != _pc[k]), min(len(_cc), len(_pc)))
                ec['first_difference'] = {'offset_after_canonicalization': _i, 'line': _cc[:_i].count(b'\n') + 1,
                                          'cell_bytes': _cc[_i:_i + 40].decode('utf-8', 'replace'), 'published_bytes': _pc[_i:_i + 40].decode('utf-8', 'replace')}
        shutil.rmtree(_gd, ignore_errors=True)
    except Exception as e:
        ec['published_error'] = '%s: %s' % (type(e).__name__, str(e)[:300]); _ck['repository_checks_completed'] = False
    _REQ = ('cell_captured', 'commit_object_exists', 'tree_single_entry_exact_path', 'tree_entry_regular_file',
            'default_branch_publishes_same_blob', 'recomputed_blob_equals_tree_blob', 'raw_channel_equal', 'executed_cell_equals_published_bytes')
    ec['failed_checks'] = [k for k in _REQ if _ck.get(k) is not True] + [k for k, v in _ck.items() if k not in _REQ and v is not True]
    ec['identity_match'] = not ec['failed_checks']
    R['executed_cell'] = ec
    log('EXECUTED_CELL', json.dumps(R['executed_cell']))
    if not ec['identity_match']:                         # fail-closed BEFORE ENV, the model load and any GPU work
        raise StopT896('SOURCE_IDENTITY_MISMATCH %s' % json.dumps({k: ec.get(k) for k in ('status', 'failed_checks', 'capture_error', 'published_error', 'first_difference')}, default=str))
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
        _gdrive.mount('/content/drive'); DRIVE_DIR = '/content/drive/MyDrive/TEST899_BP_' + RUN_ID; os.makedirs(DRIVE_DIR, exist_ok=True)
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
                                                           headers={'User-Agent': 'AKBASCORE-TEST899_BP'}), timeout=120) as f_:
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
    # ============================================================ GATE0 ARCHIVE (CPU only; the model is NOT loaded yet)
    # The ORIGINAL TEST897 archive is opened read-only from Drive. Only the 5 audit files and the 16 required cartridges are
    # extracted (byte copies) into a separate input directory OUTSIDE this run's ROOT (so they are never re-packed into the
    # TEST898 ZIP); the evaluator vault is never extracted. Any mismatch -> GATE0_ARCHIVE FAIL -> stop before the model load.
    import zipfile as _zf
    A0 = {}; ARCH = {}; ARCH_CP = {}; ARCH_ENT = {}; A0_ERR = []
    INPUT_DIR = ROOT.parent / ('TEST897_INPUT_' + RUN_ID); INPUT_DIR.mkdir(parents=True, exist_ok=False)
    _jn = lambda x: json.loads(json.dumps(x, sort_keys=True, default=str))                # tuple -> list normalisation
    try:
        _zp = Path(T897['zip']); A0['zip_exists'] = _zp.is_file()
        A0['zip_sha256_start'] = sha_path(_zp); A0['zip_bytes'] = _zp.stat().st_size
        with _zf.ZipFile(_zp, 'r') as z:
            # size / count limits from the central directory BEFORE any member is decompressed (testzip decompresses everything);
            # zipfile never yields more than the declared file_size and checks each CRC, so the declared sizes bound the work
            _inf = z.infolist(); _rt = T897['root']
            A0['zip_member_count'] = len(_inf); A0['zip_uncompressed_total'] = sum(i_.file_size for i_ in _inf)
            A0['zip_uncompressed_max_member'] = max([i_.file_size for i_ in _inf] or [0])
            A0['zip_limits'] = dict(ZIP_LIMITS_898)
            A0['zip_within_limits'] = (0 < len(_inf) <= ZIP_LIMITS_898['max_members'] and A0['zip_uncompressed_total'] <= ZIP_LIMITS_898['max_total_bytes'] and
                                       A0['zip_uncompressed_max_member'] <= ZIP_LIMITS_898['max_member_bytes'] and
                                       A0['zip_uncompressed_total'] <= ZIP_LIMITS_898['max_ratio'] * max(1, sum(i_.compress_size for i_ in _inf)))
            A0['zip_no_symlinks_or_special'] = all(((i_.external_attr >> 16) & 0o170000) in (0, 0o100000, 0o040000) for i_ in _inf)
            A0['zip_no_encryption'] = all(not (i_.flag_bits & 0x1) for i_ in _inf)
            if not (A0['zip_within_limits'] and A0['zip_no_symlinks_or_special'] and A0['zip_no_encryption']):
                raise RuntimeError('ZIP_LIMITS_OR_MEMBER_TYPE_VIOLATED members=%d total=%d max_member=%d' % (
                    len(_inf), A0['zip_uncompressed_total'], A0['zip_uncompressed_max_member']))
            A0['zip_crc_testzip'] = z.testzip() is None
            _names = z.namelist()
            A0['zip_members_safe'] = all(n.startswith(_rt + '/') and '..' not in n.split('/') and not n.startswith('/') and '\\' not in n
                                         and ':' not in n for n in _names)
            A0['zip_members_unique'] = len(_names) == len(set(_names))
            _sums_raw = z.read(_rt + '/SHA256SUMS.txt').decode('utf-8')
            _rows = [l_.split('  ', 1) for l_ in _sums_raw.split('\n') if l_]
            SUMS = {r_[1]: r_[0] for r_ in _rows if len(r_) == 2}
            A0['sha256sums_wellformed'] = len(SUMS) == len(_rows) and all(re.fullmatch(r'[0-9a-f]{64}', h_) for h_ in SUMS.values())
            _carts = {}
            for n in _names:
                b_ = n.rsplit('/', 1)[-1]
                if n.startswith(_rt + '/cartridges/') and b_ in T898_REQ_FILES: _carts.setdefault(b_, []).append(n)
            A0['required_cartridges_present_once'] = sorted(_carts) == sorted(T898_REQ_FILES) and all(len(v) == 1 for v in _carts.values())
            _mem = {k: _rt + '/' + v for k, v in T898_AUDIT_FILES.items()}; _mem.update({b_: v[0] for b_, v in _carts.items() if len(v) == 1})
            for k, m in _mem.items():
                if m not in _names: A0_ERR.append('MISSING ' + m); continue
                data_ = z.read(m); rel_ = m[len(_rt) + 1:]
                dst_ = INPUT_DIR / rel_; dst_.parent.mkdir(parents=True, exist_ok=True); dst_.write_bytes(data_)
                ARCH[k] = {'member': m, 'path': str(dst_), 'sha256': sha_bytes(data_), 'bytes': len(data_), 'sha256sums': SUMS.get(rel_)}
        A0['all_required_extracted'] = all(k in ARCH for k in list(T898_AUDIT_FILES) + list(T898_REQ_FILES))
        A0['extracted_match_sha256sums'] = A0['all_required_extracted'] and all(v['sha256'] == v['sha256sums'] for v in ARCH.values())
        # results.json: the ZIP copy (SHA256SUMS-verified) must be the contract file, or equal it in every section used here
        R7z = json.loads(Path(ARCH['results']['path']).read_text())
        A0['results_zip_copy_sha256'] = ARCH['results']['sha256']
        if ARCH['results']['sha256'] == T897['results_sha256']:
            R7 = R7z; A0['results_identity'] = 'ZIP_COPY_EQUALS_CONTRACT_SHA256'
        else:
            _dp = Path(T897['drive_results']); _db = _dp.read_bytes() if _dp.is_file() else b''
            A0['results_drive_copy_sha256'] = sha_bytes(_db); A0['results_drive_copy_bytes'] = len(_db)
            if sha_bytes(_db) != T897['results_sha256'] or len(_db) != T897['results_bytes']: raise RuntimeError('RESULTS_JSON_CONTRACT_SHA256_NOT_FOUND')
            R7 = json.loads(_db.decode('utf-8'))
            _secs = ('run_id', 'commit', 'model_revision', 'runtime_pins', 'executed_cell', 'world_manifest', 'cartridges', 'episodes', 'controls', 'decision')
            A0['results_zip_vs_drive_sections_equal'] = {k: _jn(R7z.get(k)) == _jn(R7.get(k)) for k in _secs}
            if not all(A0['results_zip_vs_drive_sections_equal'].values()): raise RuntimeError('RESULTS_ZIP_AND_DRIVE_COPIES_DIFFER')
            A0['results_identity'] = 'DRIVE_COPY_EQUALS_CONTRACT_SHA256_AND_ZIP_COPY_SECTIONS_EQUAL'
        A0['run_identity'] = (R7.get('run_id') == T897['run_id'] and R7.get('status') == 'COMPLETE' and R7.get('commit') == COMMIT and
                              (R7.get('decision') or {}).get('VERDICT') == T897['verdict'] and R7.get('technical_status') == 'PASS')
        A0['model_revision_equal'] = R7.get('model_revision') == MODEL_REVISION
        A0['runtime_pins_equal'] = _jn(R7.get('runtime_pins')) == _jn(R['runtime_pins'])
        _e7, _e8 = R7.get('env') or {}, R.get('env') or {}
        A0['runtime_env_equal'] = {k: _e7.get(k) == _e8.get(k) for k in ('torch', 'cuda', 'transformers', 'accelerate', 'bitsandbytes', 'gpu')}
        # transitive runtime differences: REPORTED (tokenisation equality is checked directly in GATE1 on the archived token ids);
        # any difference makes the reused TEST897 history NOT_COMPARABLE in GATE4, it never enters a same-runtime comparison
        _t7, _t8 = _e7.get('transitive') or {}, _e8.get('transitive') or {}
        A0['transitive_diff'] = {k: {'TEST897': _t7.get(k), 'TEST898': _t8.get(k)} for k in sorted(set(_t7) | set(_t8)) if _t7.get(k) != _t8.get(k)}
        _rm7, _rm8 = R7.get('runtime_manifest') or {}, R.get('runtime_manifest') or {}
        A0['runtime_manifest_recorded_897'] = bool(_rm7)
        A0['runtime_manifest_diff'] = {'added': sorted(set(_rm8) - set(_rm7)), 'removed': sorted(set(_rm7) - set(_rm8)),
                                       'changed': {k: [_rm7[k], _rm8[k]] for k in sorted(set(_rm7) & set(_rm8)) if _rm7[k] != _rm8[k]}}
        A0['runtime_manifest_equal'] = bool(_rm7) and not any(A0['runtime_manifest_diff'].values())
        log('RUNTIME_DIFF_VS_TEST897', json.dumps({'transitive': A0['transitive_diff'], 'manifest': A0['runtime_manifest_diff']}, default=str)[:4000])
        # executed TEST897 source: archived cell == published blob fbde1d13 (fetched now at its commit) after the same canonicalization
        _ec7 = R7.get('executed_cell') or {}; _pub7 = _ec7.get('published') or {}
        A0['t897_identity_recorded'] = (_ec7.get('identity_match') is True and _pub7.get('commit') == T897['cell_commit'] and
                                        _pub7.get('tree_blob') == T897['cell_blob'] and _pub7.get('sha256') == T897['cell_sha256'] and
                                        _pub7.get('bytes') == T897['cell_bytes'] and _pub7.get('path') == T897['cell_path'])
        with urllib.request.urlopen(urllib.request.Request('https://raw.githubusercontent.com/%s/%s/%s' % (SRC_REPO, T897['cell_commit'], T897['cell_path']),
                                                           headers={'User-Agent': 'AKBASCORE-TEST898'}), timeout=120) as f_:
            _src7b = f_.read()
        A0['t897_source_published_blob'] = gitblob(_src7b) == T897['cell_blob'] and sha_bytes(_src7b) == T897['cell_sha256']
        _cell7b = Path(ARCH['cell']['path']).read_bytes()
        A0['t897_archived_cell_equals_published'] = _cell7b.strip(b'\n') == _src7b.strip(b'\n')
        SRC897 = _src7b.decode('utf-8')
        # public manifest (model-visible contract only) and its templates == the templates of this cell
        _mb = Path(ARCH['manifest']['path']).read_bytes(); MAN = json.loads(_mb.decode('utf-8'))
        A0['manifest_sha256_equal_recorded'] = sha_bytes(_mb) == (R7.get('world_manifest') or {}).get('sha256')
        A0['manifest_templates_equal_this_cell'] = (_jn(MAN.get('record_templates')) == _jn(REC_TPL_NPDM) and _jn(MAN.get('query_template')) == _jn(QUERY_TPL_NPDM)
                                                    and _jn(MAN.get('grammar')) == _jn(GRAMMAR_NPDM))
        PUB = MAN['public_contract']; MK = MAN['markers']
        # cartridges: archive SHA-256 == SHA256SUMS == recorded index; torch.load(weights_only) on CPU; engine seal_cp == recorded seal;
        # structure / dtype / finiteness / token counts
        CI7 = {}
        for e_ in R7['cartridges']:
            CI7.setdefault(Path(e_['file']).name, []).append(e_)
        A0['index_entries_unique'] = all(len(CI7.get(b_, [])) == 1 for b_ in T898_REQ_FILES)
        _cc = {}
        for b_ in T898_REQ_FILES:
            ent_ = CI7[b_][0]; ARCH_ENT[b_] = ent_
            cp_ = torch.load(ARCH[b_]['path'], map_location='cpu', weights_only=True)
            n_ = int(cp_['n'])
            c_ = {'sha256_index': ARCH[b_]['sha256'] == ent_['sha256'],
                  'tensor_seal': _jn(seal_cp(cp_)) == _jn(ent_['tensor_seal']),
                  'keys': set(cp_) == {'h', 'lower', 'n', 'p', 'body_tokens', 'book_id'},
                  'n_p_body': n_ == ent_['n'] and cp_['p'] == TOL['P_expected'] and int(cp_['body_tokens']) == n_ - cp_['p'] and
                              ('body_tokens' not in ent_ or int(ent_['body_tokens']) == int(cp_['body_tokens'])),
                  'h_shape_dtype': tuple(cp_['h'].shape) == (1, n_, EXPECTED[1]) and cp_['h'].dtype == DTYPE,
                  'lower_layers': len(cp_['lower']) == CUT + 1 and all(tuple(k_.shape) == (1, EXPECTED[3], n_, EXPECTED[4]) and
                                                                         tuple(v_.shape) == (1, EXPECTED[3], n_, EXPECTED[4]) and
                                                                         k_.dtype == DTYPE and v_.dtype == DTYPE for k_, v_ in cp_['lower']),
                  'finite': bool(torch.isfinite(cp_['h']).all()) and all(bool(torch.isfinite(k_).all()) and bool(torch.isfinite(v_).all())
                                                                           for k_, v_ in cp_['lower'])}
            _cc[b_] = c_; ARCH_CP[b_] = cp_
        A0['cartridge_checks'] = {b_: all(c_.values()) for b_, c_ in _cc.items()}
        A0['cartridges_all_pass'] = all(A0['cartridge_checks'].values())
        if not A0['cartridges_all_pass']: A0['cartridge_check_detail'] = {b_: c_ for b_, c_ in _cc.items() if not all(c_.values())}
        # the three eligible states, their records, their cartridges and the contract names
        CT = {c_['eid']: c_ for c_ in R7['controls']}
        A0['eligible_states_exactly_L1_L2_L3'] = sorted(CT) == ['L1', 'L2', 'L3']
        LED = {e: R7['episodes'][e]['ledger'] for e in ('L1', 'L2', 'L3')}
        FRZ = {}; FRZ_FILES = {}; _nm = {}; A0['ledger_mapping'] = {}
        for e, x in T898_EXPECT.items():
            c_ = CT[e]; fr_ = c_['frozen_records']; FRZ[e] = fr_
            _lm = ledger_files_898(R7, e, len(fr_))              # ledger SHA -> unique index entry (fail-closed)
            A0['ledger_mapping'][e] = _lm; FRZ_FILES[e] = [d_['file'] for d_ in _lm]
            _u = placebo_u_npdm(fr_, PUB[e], x['discrepancy_t'])
            _nm[e] = (c_['discrepancy_t'] == x['discrepancy_t'] and c_['decision_t'] == x['decision_t'] and c_['predicted'] == x['pred'] and
                      c_['observed'] == x['obs'] and _jn(fr_) == _jn([r_ for r_, sh_, ns_ in LED[e][:len(fr_)]]) and
                      all(f_ in T898_REQ_FILES for f_ in FRZ_FILES[e]) and
                      [r_['A'] for r_ in fr_ if r_['kind'] == 'MODEL_INTENT' and r_['t'] == x['discrepancy_t']] == [x['focal_action']] and
                      c_['z'].get('NPDM') is not None and c_['z'].get('NO_PRED_ALL') is not None and c_['left'] == PUB[e]['budget'] - x['decision_t'] + 1 and
                      ('u' not in x or (_u == x['u'] == c_.get('placebo_u') and PUB[e]['goal'] == x['goal'])))
        # the SHA bound by the ledger is the SHA of the extracted file bytes AND of the index entry selected by file name
        A0['ledger_sha_equals_archive_files'] = all(d_['file'] in ARCH and ARCH[d_['file']]['sha256'] == d_['sha256'] == ARCH_ENT[d_['file']]['sha256']
                                                    for e in A0['ledger_mapping'] for d_ in A0['ledger_mapping'][e])
        A0['ledger_mapping_all'] = sorted(A0['ledger_mapping']) == ['L1', 'L2', 'L3']
        A0['contract_names_match_archive'] = _nm
        A0['contract_names_all'] = all(_nm.values())
    except Exception as e:
        A0_ERR.append('%s: %s' % (type(e).__name__, str(e)[:400])); A0['traceback'] = traceback.format_exc()[-6000:]
    _a0_keys = ('zip_exists', 'zip_within_limits', 'zip_no_symlinks_or_special', 'zip_no_encryption', 'zip_crc_testzip', 'zip_members_safe', 'zip_members_unique', 'sha256sums_wellformed', 'required_cartridges_present_once',
                'all_required_extracted', 'extracted_match_sha256sums', 'run_identity', 'model_revision_equal', 'runtime_pins_equal',
                't897_identity_recorded', 't897_source_published_blob', 't897_archived_cell_equals_published', 'manifest_sha256_equal_recorded',
                'manifest_templates_equal_this_cell', 'index_entries_unique', 'cartridges_all_pass', 'eligible_states_exactly_L1_L2_L3', 'ledger_mapping_all',
                'ledger_sha_equals_archive_files', 'contract_names_all')
    _a0_fail = [k for k in _a0_keys if A0.get(k) is not True] + [k for k, v in (A0.get('runtime_env_equal') or {'runtime_env_equal': False}).items() if v is not True]
    R['input_archive_check'] = dict(A0, errors=A0_ERR, input_dir=str(INPUT_DIR), extracted={k: {kk: vv for kk, vv in v.items() if kk != 'path'} for k, v in ARCH.items()})
    _inm = {k: {'member': v['member'], 'sha256': v['sha256'], 'bytes': v['bytes']} for k, v in ARCH.items()}
    (ROOT / 'TEST899_BP_input_manifest.json').write_text(json.dumps({'archive': T897, 'zip_sha256': A0.get('zip_sha256_start'), 'files': _inm,
                                                                         'results_identity': A0.get('results_identity'),
                                                                         'gate0_failed_checks': _a0_fail, 'gate0_errors': A0_ERR}, indent=1, sort_keys=True))
    gate('GATE0_ARCHIVE', 'PASS' if not _a0_fail and not A0_ERR else 'FAIL',
         None if not _a0_fail and not A0_ERR else 'BLOCKER: ' + ', '.join(_a0_fail + A0_ERR)[:1500], checks=A0, errors=A0_ERR)
    # ------------------------------------------------ TEST898 input archive: independent, read-only, CPU only
    A8 = {}; ARCH8 = {}; ARCH8_CP = {}
    try:
        _z8 = Path(T898IN['zip']); A8['zip_exists'] = _z8.is_file()
        A8['zip_sha256'] = sha_path(_z8); A8['zip_bytes'] = _z8.stat().st_size
        A8['zip_identity'] = A8['zip_sha256'] == T898IN['zip_sha256'] and A8['zip_bytes'] == T898IN['zip_bytes']
        IN8 = ROOT.parent / ('TEST898_INPUT_' + RUN_ID); IN8.mkdir(parents=True, exist_ok=False)
        with _zf.ZipFile(_z8, 'r') as z:
            inf = z.infolist(); names = z.namelist(); rt = T898IN['root']
            A8['member_count_exact'] = len(inf) == T898IN['members']
            A8['members_unique'] = len(names) == len(set(names))
            A8['members_safe'] = all(n.startswith(rt + '/') and not n.startswith('/') and '..' not in n.split('/') and '\\' not in n and ':' not in n for n in names)
            A8['no_symlinks_special'] = all(((i.external_attr >> 16) & 0o170000) in (0, 0o100000, 0o040000) for i in inf)
            A8['no_encryption'] = all(not (i.flag_bits & 1) for i in inf)
            A8['within_limits'] = (len(inf) <= ZIP_LIMITS_898['max_members'] and sum(i.file_size for i in inf) <= ZIP_LIMITS_898['max_total_bytes'] and
                                   max(i.file_size for i in inf) <= ZIP_LIMITS_898['max_member_bytes'] and
                                   sum(i.file_size for i in inf) <= ZIP_LIMITS_898['max_ratio'] * max(1, sum(i.compress_size for i in inf)))
            A8['crc'] = z.testzip() is None
            sr = z.read(rt + '/SHA256SUMS.txt').decode(); rows = [x.split('  ',1) for x in sr.splitlines() if x]
            sums = {r[1]: r[0] for r in rows if len(r) == 2}
            A8['sha_rows_exact'] = len(rows) == T898IN['sha_rows'] and len(sums) == len(rows)
            A8['sha_all_members'] = all(sha_bytes(z.read(rt + '/' + rel)) == h for rel, h in sums.items())
            A8['sha_member_set_exact'] = set(sums) == {n[len(rt)+1:] for n in names if not n.endswith('/')} - {'SHA256SUMS.txt'}
            req = {'results': rt + '/TEST898_NRBC_results.json', 'events': rt + '/TEST898_NRBC_events.jsonl'}
            cart_members = [n for n in names if n.startswith(rt + '/cartridges/') and n.endswith('.pt')]
            A8['cartridge_member_count_exact'] = len(cart_members) == T898IN['cartridges']
            for key, member in req.items():
                data = z.read(member); rel = member[len(rt)+1:]
                dst = IN8 / rel; dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(data)
                ARCH8[key] = {'path': str(dst), 'member': member, 'sha256': sha_bytes(data), 'bytes': len(data), 'sha256sums': sums.get(rel)}
            for member in cart_members:
                data = z.read(member); rel = member[len(rt)+1:]; dst = IN8 / rel
                dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(data)
                ARCH8[Path(member).name] = {'path': str(dst), 'member': member, 'sha256': sha_bytes(data), 'bytes': len(data), 'sha256sums': sums.get(rel)}
        A8['results_identity'] = ARCH8['results']['sha256'] == T898IN['results_sha256'] and ARCH8['results']['bytes'] == T898IN['results_bytes']
        A8['events_identity'] = ARCH8['events']['sha256'] == T898IN['events_sha256'] and ARCH8['events']['bytes'] == T898IN['events_bytes']
        A8['extracted_match_sha256sums'] = all(v['sha256'] == v['sha256sums'] for v in ARCH8.values())
        R8 = json.loads(Path(ARCH8['results']['path']).read_text())
        A8['run_identity'] = (R8.get('run_id') == T898IN['run_id'] and R8.get('status') == 'COMPLETE' and R8.get('commit') == COMMIT and
                              R8.get('model_revision') == MODEL_REVISION and R8.get('verdict') == 'NRBC_SCREEN_FAIL' and R8.get('technical_status') == 'PASS')
        A8['runtime_pins_equal'] = _jn(R8.get('runtime_pins')) == _jn(R['runtime_pins'])
        A8['runtime_env_equal'] = all((R8.get('env') or {}).get(k) == (R.get('env') or {}).get(k) for k in ('torch','cuda','transformers','accelerate','bitsandbytes','gpu'))
        _tr8, _tr9 = (R8.get('env') or {}).get('transitive') or {}, (R.get('env') or {}).get('transitive') or {}
        A8['runtime_transitive_equal'] = all(_tr8.get(k) == _tr9.get(k) and _tr9.get(k) is not None for k in
                                             ('tokenizers','huggingface-hub','safetensors','numpy','sentencepiece','regex'))
        ci8 = {}
        for ent in R8.get('cartridges', []): ci8.setdefault(Path(ent['file']).name, []).append(ent)
        A8['index_19_unique'] = len(ci8) == T898IN['cartridges'] and all(len(v) == 1 for v in ci8.values())
        checks8 = {}
        for base, ents in ci8.items():
            ent = ents[0]; cp = torch.load(ARCH8[base]['path'], map_location='cpu', weights_only=True); n = int(cp['n'])
            c = {'file_sha': ARCH8[base]['sha256'] == ent['sha256'],
                 'tensor_seal': _jn(seal_cp(cp)) == _jn(ent['tensor_seal']),
                 'keys': set(cp) == {'h','lower','n','p','body_tokens','book_id'},
                 'n_p_body': n == ent['n'] and cp['p'] == 30 and int(cp['body_tokens']) == n - 30,
                 'h': tuple(cp['h'].shape) == (1,n,8192) and cp['h'].dtype == DTYPE,
                 'lower': len(cp['lower']) == 4 and all(tuple(k.shape) == (1,8,n,128) and tuple(v.shape) == (1,8,n,128) and k.dtype == DTYPE and v.dtype == DTYPE for k,v in cp['lower']),
                 'finite': bool(torch.isfinite(cp['h']).all()) and all(bool(torch.isfinite(k).all()) and bool(torch.isfinite(v).all()) for k,v in cp['lower'])}
            checks8[base] = all(c.values())
            if base == T898IN['real_file']: ARCH8_CP['REAL'] = cp; ARCH8_REAL_ENT = ent
        A8['tensor_seals_19'] = len(checks8) == 19 and all(checks8.values())
        A8['real_identity'] = (ARCH8_REAL_ENT['cid'] == T898IN['real_cid'] and ARCH8_REAL_ENT['sha256'] == T898IN['real_sha256'] and
                               int(ARCH8_CP['REAL']['body_tokens']) == 134)
        g0 = R8['generations'][0]
        REAL_RAW = g0['raw'].strip(); REAL_TEXT = BELIEF_TPL_898.format(t=2, B=REAL_RAW)
        A8['real_generation_contract'] = (g0['gen'] == 'C1' and g0['branch'] == 'L1_REAL' and g0['parsed_valid'] is True and
                                          g0['belief_record_tokens'] == 134 and g0['reloaded_from_ssd'] is True and
                                          g0['cartridge_sha256'] == T898IN['real_sha256'] and
                                          sha_bytes(REAL_TEXT.encode()) == ARCH8_REAL_ENT['text_sha256'])
        A8['real_all_fields_correct_recorded'] = (R8.get('offline',{}).get('beliefs',{}).get('L1_REAL',{}).get('all_fields_correct') is True)
        HIST8 = {g['arm'] + '_' + g['eid']: g for g in R8['generations'] if g.get('type') == 'READOUT'}
        HIST_F = HIST8['FILTER_ONLY_MATCHED_IO_L1']; HIST_REAL = HIST8['REAL_L1']
        A8['historical_baseline_contract'] = (HIST_F['mount_tokens'] == 98 and HIST_REAL['mount_tokens'] == 232 and
                                               HIST_F['car']['greedy_consistent'] is True and HIST_REAL['car']['greedy_consistent'] is True)
    except Exception as e:
        A8['exception'] = '%s: %s' % (type(e).__name__, e); A8['traceback'] = traceback.format_exc()[-6000:]
    R['input_archive_898_check'] = A8
    _req8 = ('zip_exists','zip_identity','member_count_exact','members_unique','members_safe','no_symlinks_special','no_encryption','within_limits','crc',
             'sha_rows_exact','sha_all_members','sha_member_set_exact','cartridge_member_count_exact','results_identity','events_identity','extracted_match_sha256sums','run_identity',
             'runtime_pins_equal','runtime_env_equal','runtime_transitive_equal','index_19_unique','tensor_seals_19','real_identity','real_generation_contract',
             'real_all_fields_correct_recorded','historical_baseline_contract')
    _fail8 = [k for k in _req8 if A8.get(k) is not True]
    _in8m = {k: {'member': v['member'], 'sha256': v['sha256'], 'bytes': v['bytes']} for k,v in ARCH8.items()}
    (ROOT / 'TEST899_BP_898_input_manifest.json').write_text(json.dumps({'archive': T898IN, 'checks': A8, 'files': _in8m, 'failed': _fail8}, indent=1, sort_keys=True))
    gate('GATE0B_898_ARCHIVE', 'PASS' if not _fail8 and 'exception' not in A8 else 'FAIL',
         None if not _fail8 and 'exception' not in A8 else 'TEST898 ARCHIVE BLOCKER: ' + ','.join(_fail8) + ' ' + A8.get('exception',''), checks=A8)
    # --------------------------------------------- GATE0C: pinned tokenizer-only exact geometry, CPU only; no model load
    GEO = {}; BELIEFS899 = {}
    try:
        from huggingface_hub import hf_hub_download as _hf_geo
        tok = _PinnedRevision(transformers.AutoTokenizer).from_pretrained(MODEL_ID, revision=MODEL_REVISION)
        _tj = _hf_geo(MODEL_ID, 'tokenizer.json', revision=MODEL_REVISION)
        GEO['tokenizer_in_pinned_snapshot'] = ('/snapshots/%s/' % MODEL_REVISION) in _tj.replace('\\', '/')
        _tjm7 = (((R7.get('gates') or {}).get('MODEL', {}).get('data', {}).get('revision_files') or {}).get('tokenizer.json') or {})
        GEO['tokenizer_json_same_as_897'] = sha_path(_tj) == _tjm7.get('sha256')
        REAL_RAW = REAL_RAW.strip(); REAL_TEXT = BELIEF_TPL_898.format(t=2, B=REAL_RAW)
        _ids_real = list(tok(REAL_TEXT, add_special_tokens=False).input_ids)      # = TEST898 tok_ids(text), checked BEFORE any geometry rule
        GEO['real_134_tokens'] = len(_ids_real) == T898IN['real_body_tokens'] == 134
        GEO['real_ids_match_898_cartridge'] = sha_bytes(json.dumps(_ids_real).encode()) == ARCH8_REAL_ENT.get('ids_sha256')
        GEO['real_text_matches_898_cartridge'] = sha_bytes(REAL_TEXT.encode()) == ARCH8_REAL_ENT.get('text_sha256')
        _bad_in0 = [k for k in ('tokenizer_in_pinned_snapshot', 'tokenizer_json_same_as_897', 'real_134_tokens', 'real_ids_match_898_cartridge',
                                'real_text_matches_898_cartridge') if GEO.get(k) is not True]
        if _bad_in0: raise RuntimeError('GEOMETRY_INPUT_CONTRACT_FAILED ' + ','.join(_bad_in0))
        REAL_GEO = geometry899(REAL_TEXT, REAL_RAW)
        if REAL_GEO['ids'] != _ids_real: raise RuntimeError('GEOMETRY_TOKENIZATION_DIFFERS_FROM_TEST898_TOK_IDS')
        BELIEFS899['REAL'] = {'text': REAL_TEXT, 'raw': REAL_RAW, 'geo': REAL_GEO, 'construction': 'ARCHIVED_TEST898_NATIVE_GREEDY_B'}
        # audit only: the HF offset_mapping convention of this tokenizer (never used as the boundary definition)
        _hfo = [tuple(map(int, x)) for x in tok(REAL_TEXT, add_special_tokens=False, return_offsets_mapping=True).offset_mapping]
        GEO['hf_offset_mapping_equals_token_byte_offsets_AUDIT'] = _hfo == REAL_GEO['offsets']
        _nid = [tuple(tok(w, add_special_tokens=False).input_ids) for k_ in ('NEUTRAL1', 'NEUTRAL2') for w in NEUTRAL_WORDS_899[k_]]
        GEO['neutral_16_words_one_token_distinct'] = all(len(x) == 1 for x in _nid) and len(set(_nid)) == 16
        for name, words in (('NEUTRAL1', NEUTRAL_WORDS_899['NEUTRAL1']), ('NEUTRAL2', NEUTRAL_WORDS_899['NEUTRAL2'])):
            text_, raw_, geo_ = neutral899(REAL_TEXT, REAL_RAW, REAL_GEO, words)
            assert_same_geometry899(REAL_GEO, geo_, name)
            BELIEFS899[name] = {'text': text_, 'raw': raw_, 'geo': geo_, 'construction': 'PREREGISTERED_ONE_FOR_ONE_NEUTRAL_TOKEN_SUBSTITUTION'}
        text_, raw_, geo_, perm_ = swapped899(REAL_TEXT, REAL_RAW, REAL_GEO, PUB['L1'], sorted(facts_npdm(FRZ['L1'], PUB['L1']['outcomes'])))
        assert_same_geometry899(REAL_GEO, geo_, 'SWAPPED')
        BELIEFS899['SWAPPED'] = {'text': text_, 'raw': raw_, 'geo': geo_, 'construction': 'PREREGISTERED_PUBLIC_NAME_PERMUTATION',
                                 'permutation': perm_}
        GEO['all_four_exact_geometry'] = all(geometry_signature899(BELIEFS899[k]['geo']) == geometry_signature899(REAL_GEO) and
                                             BELIEFS899[k]['geo']['noncontent_sha256'] == REAL_GEO['noncontent_sha256'] and
                                             len(BELIEFS899[k]['geo']['ids']) == 134 for k in BELIEFS899)
        GEO['swapped_core_differs'] = belief_facts_898(parse_belief_898(BELIEFS899['SWAPPED']['raw'])['fields'], PUB['L1']) != facts_npdm(FRZ['L1'], PUB['L1']['outcomes'])
        GEO['no_hidden_mapping_used'] = True  # DECLARATION (not a test): constructors receive only REAL text, public L1 names and the public frozen facts
        _geo_inputs = ('tokenizer_in_pinned_snapshot', 'tokenizer_json_same_as_897', 'real_134_tokens', 'real_ids_match_898_cartridge',
                       'real_text_matches_898_cartridge')
        _geo_req = _geo_inputs + ('neutral_16_words_one_token_distinct', 'all_four_exact_geometry', 'swapped_core_differs', 'no_hidden_mapping_used')
        _bad_in = [k for k in _geo_inputs if GEO.get(k) is not True]
        if _bad_in: raise RuntimeError('GEOMETRY_INPUT_CONTRACT_FAILED ' + ','.join(_bad_in))   # wrong tokenizer / REAL: technical, not UNSAT
        _geo_bad = [k for k in _geo_req if GEO.get(k) is not True]
        if _geo_bad: raise NoRun899('GEOMETRY_PRECHECK_FAILED ' + ','.join(_geo_bad))
        GEO['status'] = 'SAT'
    except NoRun899 as e:                        # a genuine geometry / control-construction impossibility: NO_RUN
        GEO['status'] = 'UNSAT'; GEO['reason'] = '%s: %s' % (type(e).__name__, e); GEO['traceback'] = traceback.format_exc()[-6000:]
    except Exception as e:                       # download / tokenizer / input contract failure: TECHNICAL, never labelled UNSAT
        GEO['status'] = 'ERROR'; GEO['reason'] = '%s: %s' % (type(e).__name__, e); GEO['traceback'] = traceback.format_exc()[-6000:]
    _gm = {'status': GEO.get('status'), 'checks': {k: v for k, v in GEO.items() if k not in ('status','traceback')},
           'geometry_definition': 'token IDs length, ordered field token spans and non-content token IDs exact; char offsets audit-only; no padding',
           'beliefs': {k: {'text_sha256': v['geo']['sha256'], 'ids_sha256': sha_bytes(json.dumps(v['geo']['ids']).encode()),
                           'ids': v['geo']['ids'], 'spans': v['geo']['spans'], 'noncontent_sha256': v['geo']['noncontent_sha256'],
                           'raw': v['raw'], 'construction': v['construction'], 'permutation': v.get('permutation')}
                       for k, v in BELIEFS899.items()}}
    (ROOT / 'TEST899_BP_geometry_manifest.json').write_text(json.dumps(_gm, indent=1, sort_keys=True))
    R['geometry_preflight'] = _gm
    if GEO.get('status') == 'ERROR':
        gate('GATE0C_GEOMETRY', 'FAIL', 'GEOMETRY_PREFLIGHT_TECHNICAL_ERROR ' + str(GEO.get('reason')), checks=GEO)   # raises StopT896
    if GEO.get('status') != 'SAT':
        R['gates']['GATE0C_GEOMETRY'] = {'status': 'NO_RUN', 'reason': GEO.get('reason'), 'data': {'checks': GEO}}
        save(); log('GATE GATE0C_GEOMETRY NO_RUN', GEO.get('reason')); raise NoRun899(GEO.get('reason'))
    gate('GATE0C_GEOMETRY', 'PASS', 'all four 134-token physical B records satisfiable before model load', checks=GEO)
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
    calls_ok = sorted(c[0] for c in PINNED_CALLS) == ['AutoModelForCausalLM', 'AutoTokenizer', 'AutoTokenizer'] and all(c[2] == MODEL_REVISION for c in PINNED_CALLS)
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
    # ============================================================ GATE1 ENGINE (model loaded; tokenizer / readout settings / content)
    G1 = {}
    _m7 = (R7.get('gates') or {}).get('MODEL', {}).get('data', {})
    G1['tokenizer_json_same_as_897'] = rev_files['tokenizer.json']['sha256'] == ((_m7.get('revision_files') or {}).get('tokenizer.json') or {}).get('sha256')
    G1['config_json_same_as_897'] = rev_files['config.json']['sha256'] == ((_m7.get('revision_files') or {}).get('config.json') or {}).get('sha256')
    G1['prefix_sha256_same_as_897'] = sha_bytes(PREFIX.encode()) == _m7.get('prefix_sha256')
    G1['P_equal'] = P == TOL['P_expected'] and all(int(ARCH_CP[b_]['p']) == P for b_ in T898_REQ_FILES)
    # readout generation settings = TEST897 controls: MAX_NEW from the sealed manifest, recomputed with this tokenizer
    MAX_NEW_A = int(MAN['max_new_tokens'])
    _gram = ['ACQUIRE %s PREDICTION %s' % (a, o) for p_ in PUB.values() for a in p_['actions'] for o in p_['outcomes']]
    G1['max_new_recomputed_equal_897'] = max(ntok(x) for x in _gram) + PROTO['max_new_margin_tokens'] == MAX_NEW_A
    G1['markers_7_tokens'] = all(ntok(MK[k]) == MK['field_ntok'] for k in ('prediction_withheld', 'outcome_withheld'))
    MAX_NEW = MAX_NEW_A
    R['readout_settings'] = {'max_new_tokens': MAX_NEW_A, 'grammar': 'PRED and DIRECT, fixed per arm', 'query': 'query_npdm(contract, left, grammar, rot=0)',
                             'decoding': 'greedy, locked 709 answer()', 'belief_construction': 'archived REAL plus deterministic exact-geometry controls; no consolidation generation'}
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
    # ------------------------------------------------------------------ GATE1 (continued): archived cartridges are the replay source
    # token content of every archived record cartridge == the record the TEST897 ledger / control derivation says it holds
    _rec_of = {}
    for e in ('L1', 'L2', 'L3'):
        for i, r_ in enumerate(FRZ[e]): _rec_of[FRZ_FILES[e][i]] = r_
    _rec_of['T896_L1_CTRL_FACTUAL_DELETED_05.pt'] = derive_arm_npdm('FACTUAL_DELETED', FRZ['L1'], PUB['L1'], MK, 2)[5]
    _rec_of['T896_L2_CTRL_PLACEBO_PRED_01.pt'] = derive_arm_npdm('PLACEBO_PRED', FRZ['L2'], PUB['L2'], MK, 1)[1]
    _rec_of['T896_L3_CTRL_PLACEBO_PRED_01.pt'] = derive_arm_npdm('PLACEBO_PRED', FRZ['L3'], PUB['L3'], MK, 1)[1]
    _ids_ok = {}
    for b_, r_ in _rec_of.items():
        ids_ = record_ids_npdm(r_, tok_ids)
        _ids_ok[b_] = sha_bytes(json.dumps(list(ids_)).encode()) == ARCH_ENT[b_].get('ids_sha256') and len(ids_) == int(ARCH_CP[b_]['body_tokens'])
    G1['cartridge_token_content'] = _ids_ok; G1['cartridge_token_content_all'] = len(_ids_ok) == 15 and all(_ids_ok.values())
    G1['ctrl_records'] = {k: {kk: vv for kk, vv in _rec_of[k].items()} for k in _rec_of if 'CTRL' in k}
    # engine identity against the archived, executed TEST897 source: every top-level definition is AST-identical except two,
    # and those two differ ONLY by the listed exact text substitutions (gate(): the TEST898 status names; _boot_fail(): the
    # TEST899_BP test name in the bootstrap record); *_898 functions are new; the inline cartridge functions block is verbatim
    def _defs(src_):
        return {n.name: ast.dump(n) for n in ast.parse(src_).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    def _def_src(src_, name_):
        return [ast.get_source_segment(src_, n) for n in ast.parse(src_).body if isinstance(n, ast.FunctionDef) and n.name == name_][0]
    _d7, _d8 = _defs(SRC897), _defs(_cell)
    _diff = sorted(k for k in _d7 if _d8.get(k) != _d7[k]); _new = sorted(set(_d8) - set(_d7))
    G1['ast_changed_defs'] = _diff; G1['ast_new_defs'] = _new
    _ALLOWED_898 = {'_boot_fail': (("'NPDM_SMOKE'", "'TEST899_BP'"), ("'NPDM_SMOKE BOOTSTRAP_ERROR", "'TEST899_BP BOOTSTRAP_ERROR")),
                    'gate': (("'INCONCLUSIVE_SUPPORT'), status", "'INCONCLUSIVE_SUPPORT',\n                      'NRBC_SCREEN_SUPPORT', "
                                                                 "'NRBC_SCREEN_INCONCLUSIVE', 'NRBC_SCREEN_FAIL'), status"),)}
    def _subst_ok(name_):
        t_ = _def_src(SRC897, name_)
        for a_, b_ in _ALLOWED_898[name_]:
            if a_ not in t_: return False
            t_ = t_.replace(a_, b_)
        return ast.dump(ast.parse(t_)) == ast.dump(ast.parse(_def_src(_cell, name_)))
    G1['ast_changes_exactly_allowed_substitutions'] = {k: _subst_ok(k) for k in _ALLOWED_898}
    G1['ast_identical_except_allowed'] = (_diff == sorted(_ALLOWED_898) and all(G1['ast_changes_exactly_allowed_substitutions'].values())
                                          and all(k.endswith('_898') or k.endswith('899') for k in _new))
    _ia = _cell.index("    CART_INDEX = []; R['cartridges'] = CART_INDEX")
    _ib = _cell.index("guard('query', dt); return o_\n", _ia) + len("guard('query', dt); return o_\n")
    G1['cartridge_functions_block_verbatim_in_897'] = _cell[_ia:_ib] in SRC897
    _ja = _cell.index("    def guard(op, dt=None):"); _jb = _cell.index("    def ntok(s): return len(tok_ids(s))\n", _ja)
    G1['guard_tok_ids_block_verbatim_in_897'] = _cell[_ja:_jb] in SRC897
    # the ARCHIVED EMPTY becomes the mount base of every TEST898 mount (no fresh EMPTY is ever mounted). Whether the EMPTY forged
    # in this runtime reproduces the archived tensors is a DIAGNOSTIC of cross-runtime forge drift (it feeds the TEST897
    # comparability flag in GATE4); it is NOT a gate condition, because no TEST898 comparison uses a freshly forged base.
    G1['fresh_empty_forge_equals_archived_empty_DIAGNOSTIC'] = _jn(seal_cp(CP_EMPTY)) == _jn(ARCH_ENT['T896_EMPTY.pt']['tensor_seal'])
    CP_EMPTY = ARCH_CP['T896_EMPTY.pt']
    EMPTY_ENT = {'cid': 'EMPTY_ARCHIVED_TEST897', 'file': ARCH['T896_EMPTY.pt']['path'], 'tensor_seal': seal_cp(CP_EMPTY)}   # P1: unchanged to the end
    # one archived record re-forged from its token ids reproduces the archived tensors (diagnostic of the same physical forge)
    with MountOff(): _cpr, _ = forge_native(record_ids_npdm(_rec_of['T896_L1_00_MODEL_INTENT_t1.pt'], tok_ids), 'T896_' + RUN_ID + '_REFORGE_DIAG')
    G1['reforge_L1_00_equals_archived_DIAGNOSTIC'] = _jn(seal_cp(_cpr)) == _jn(ARCH_ENT['T896_L1_00_MODEL_INTENT_t1.pt']['tensor_seal']); del _cpr; release()
    FIL = {'L1': ['T896_L1_00_MODEL_INTENT_t1.pt', 'T896_L1_02_OBSERVED_OUTCOME_t1.pt', 'T896_L1_03_MODEL_INTENT_t2.pt', 'T896_L1_05_OBSERVED_OUTCOME_t2.pt'],
           'L2': ['T896_L2_00_MODEL_INTENT_t1.pt', 'T896_L2_02_OBSERVED_OUTCOME_t1.pt'],
           'L3': ['T896_L3_00_MODEL_INTENT_t1.pt', 'T896_L3_02_OBSERVED_OUTCOME_t1.pt']}
    G1['filter_mount_equals_897_no_pred_all_records'] = {e: _jn([r_ for r_ in derive_arm_npdm('NO_PRED_ALL', FRZ[e], PUB[e], MK, T898_EXPECT[e]['discrepancy_t'])]) ==
                                                          _jn([dict(_rec_of[b_], src=FRZ_FILES[e].index(b_), changed=False) for b_ in FIL[e]]) for e in FIL}
    _m1 = mount_from([ARCH_CP[b_] for b_ in FIL['L1']]); _s1 = full_kv_seal(_m1); del _m1; release()
    _m2 = mount_from([ARCH_CP[b_] for b_ in FIL['L1']]); _s2 = full_kv_seal(_m2); del _m2; release()
    G1['mount_deterministic'] = _s1 == _s2
    G1['gpu_free_gib'] = gpu_mem()['free_gib']; G1['vram_preflight'] = G1['gpu_free_gib'] >= GPU_RESERVE_GIB
    _g1_req = ('tokenizer_json_same_as_897', 'config_json_same_as_897', 'prefix_sha256_same_as_897', 'P_equal', 'max_new_recomputed_equal_897',
               'markers_7_tokens', 'cartridge_token_content_all', 'ast_identical_except_allowed', 'cartridge_functions_block_verbatim_in_897',
               'guard_tok_ids_block_verbatim_in_897', 'mount_deterministic', 'vram_preflight')
    G1['required_checks'] = list(_g1_req); G1['diagnostic_checks'] = ['fresh_empty_forge_equals_archived_empty_DIAGNOSTIC', 'reforge_L1_00_equals_archived_DIAGNOSTIC']
    _g1_fail = [k for k in _g1_req if G1.get(k) is not True] + [e for e, v in G1['filter_mount_equals_897_no_pred_all_records'].items() if v is not True]
    gate('GATE1_ENGINE', 'PASS' if not _g1_fail else 'FAIL', None if not _g1_fail else 'failed: ' + ', '.join(_g1_fail), checks=G1)

    def car_logp_898(mem, q, raw):
        # teacher-forced log-probabilities of the re-tokenized generated text on the SAME mount and the SAME suffix as the
        # locked 709 answer(); one extra forward, the mount is checked unchanged. Measurement only (never used for a decision).
        s0 = full_kv_seal(mem)
        sids = list(tok(SUFFIX_HEAD + q + SUFFIX_TAIL, add_special_tokens=False).input_ids); gids = tok_ids(raw)
        n_ = int(mem[0][0].shape[-2]); ids_ = sids + gids
        with MountOff():
            cache = cache_build(mem); pos = torch.arange(n_, n_ + len(ids_), device=DEV)
            out = model(input_ids=torch.tensor([ids_], device=DEV), past_key_values=cache, attention_mask=torch.ones((1, n_ + len(ids_)), device=DEV, dtype=torch.long),
                        position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
            lp = torch.log_softmax(out.logits[0, len(sids) - 1:len(ids_)].float(), -1).cpu()
            del out, cache
        release()
        if full_kv_seal(mem) != s0: raise StopT896('MOUNT_CHANGED_BY_LOGP')
        firsts = {w: tok_ids(w)[0] for w in ('ACT', 'ACQUIRE', 'STOP')}
        tl = [float(lp[i, g]) for i, g in enumerate(gids)]
        return {'sum_logp': round(sum(tl), 6), 'token_logp': [round(x, 6) for x in tl], 'n_tokens': len(gids),
                'greedy_consistent': all(int(lp[i].argmax()) == g for i, g in enumerate(gids)),
                'first_token_logp': {w: round(float(lp[0, i]), 6) for w, i in firsts.items()},
                'first_token_ids_distinct': len(set(firsts.values())) == 3}
    # ============================================================ GATE2 PHYSICAL CONTROLS (no native generation here)
    BRANCH = {}; GENS = []; CHAIN899 = []; _chain_sha = ARCH_ENT[FRZ_FILES['L1'][-1]]['sha256']
    for name in ('REAL', 'NEUTRAL1', 'SWAPPED', 'NEUTRAL2'):
        bg = BELIEFS899[name]; ids = list(bg['geo']['ids'])
        cp_, ent_ = forge_record(ids, 'L1_B899_' + name, _chain_sha, 'belief_to_policy_' + name, NS_DIRS['belief'])
        CHAIN899.append(ent_); _chain_sha = ent_['sha256']
        ent_.update(branch=name, parents_sha256=[ARCH_ENT[x]['sha256'] for x in FIL['L1']],
                    text_sha256=bg['geo']['sha256'], namespace='belief', exact_geometry_with='REAL')
        if name == 'REAL':
            ent_['archived_898_sha256'] = T898IN['real_sha256']
            ent_['reforged_tensor_seal_equals_898'] = _jn(seal_cp(cp_)) == _jn(ARCH8_REAL_ENT['tensor_seal'])
        del cp_; release()
        cp2 = load_record(ent_)                         # physical SSD readback: file SHA-256 + full H3/K/V tensor seal
        BRANCH[name] = {'cp': cp2, 'ent': ent_, 'text': bg['text'], 'raw': bg['raw'], 'geo': bg['geo']}
        ev('B899_PHYSICAL', branch=name, cid=ent_['cid'], sha256=ent_['sha256'], ids_sha256=ent_['ids_sha256'],
           reloaded_from_ssd=True, reforged_tensor_seal_equals_898=ent_.get('reforged_tensor_seal_equals_898'))
    G2 = {'planned_b_records': 4, 'forged_and_reloaded': len(BRANCH),
          'real_reforge_tensor_seal_equals_898': BRANCH['REAL']['ent'].get('reforged_tensor_seal_equals_898') is True,
          'all_134_tokens': all(int(v['cp']['body_tokens']) == 134 and int(v['cp']['n']) == 164 for v in BRANCH.values()),
          'all_file_sha_readback': all(sha_path(v['ent']['file']) == v['ent']['sha256'] for v in BRANCH.values()),
          'all_exact_token_geometry': all(geometry_signature899(v['geo']) == geometry_signature899(REAL_GEO) and
                                          v['geo']['noncontent_sha256'] == REAL_GEO['noncontent_sha256'] for v in BRANCH.values()),
          # the tokenizer object loaded with the model must give the SAME ids as the pre-model geometry tokenizer
          'model_tokenizer_reproduces_preflight_ids': all(tok_ids(v['text']) == list(v['geo']['ids']) for v in BRANCH.values())}
    G2['ok'] = G2['planned_b_records'] == G2['forged_and_reloaded'] == 4 and all(v for k, v in G2.items() if k not in ('planned_b_records','forged_and_reloaded','ok'))
    gate('GATE2_PHYSICAL_CONTROLS', 'PASS' if G2['ok'] else 'FAIL',
         'four B records forged, sealed, written and reloaded; REAL reforge must reproduce the TEST898 tensor seal', counts=G2,
         beliefs={k: {'cid': v['ent']['cid'], 'sha256': v['ent']['sha256'], 'tensor_seal': v['ent']['tensor_seal']} for k,v in BRANCH.items()})

    # ============================================================ GATE3 READOUT (exactly 10 native greedy generations)
    READ = [('F','PRED',None,'REAL'), ('F','DIRECT',None,'REAL'),
            ('REAL','PRED','REAL',None), ('REAL_REPEAT','PRED','REAL',None), ('REAL','DIRECT','REAL',None),
            ('NEUTRAL1','PRED','NEUTRAL1',None), ('NEUTRAL1','DIRECT','NEUTRAL1',None),
            ('SWAPPED','PRED','SWAPPED',None), ('NEUTRAL2','PRED','NEUTRAL2',None), ('NEUTRAL2','DIRECT','NEUTRAL2',None)]
    for ai, (arm, grammar, bname, qname) in enumerate(READ):
        pub = PUB['L1']; left = CT['L1']['left']; q = query_npdm(contract_npdm(pub), left, grammar, rot=0)
        labels = list(FIL['L1']); cps = [ARCH_CP[x] for x in labels]; mount_shas = [ARCH_ENT[x]['sha256'] for x in labels]
        g_ = {'gen': 'A%d' % (ai + 1), 'type': 'READOUT', 'arm': arm, 'eid': 'L1', 'grammar': grammar, 'belief': bname,
              'factual_mount': list(labels), 'query_sha256': sha_bytes(q.encode()), 'max_new_tokens': MAX_NEW_A,
              'reused': False, 'stop_reason': 'NOT_RECORDED_BY_LOCKED_709_ANSWER'}
        if qname is not None:                         # matched physical forge/write/readback I/O, quarantined and NEVER mounted
            cpq, entq = forge_record(list(BRANCH[qname]['geo']['ids']), 'L1_QUAR_%s_%s' % (arm, grammar), _chain_sha,
                                     'quarantine_matched_io', NS_DIRS['quarantine'])
            CHAIN899.append(entq); _chain_sha = entq['sha256']
            del cpq; release(); _qr = load_record(entq); del _qr
            g_.update(quarantine_cartridge=entq['cid'], quarantine_sha256=entq['sha256'], quarantine_of=qname)
        if bname is not None:
            cps.append(BRANCH[bname]['cp']); labels.append('BELIEF:' + BRANCH[bname]['ent']['cid'])
            mount_shas.append(BRANCH[bname]['ent']['sha256'])
        mem = mount_from(cps); mtok = int(mem[0][0].shape[-2])
        g_['mount'] = labels; g_['input_cartridge_sha256'] = mount_shas; g_['mount_tokens'] = mtok
        _qt9 = time.perf_counter(); raw = timed_gen(mem, q); _gen_dt9 = time.perf_counter() - _qt9
        lp = car_logp_898(mem, q, raw); gpu_after = gpu_mem(); del mem; release()
        p_ = parse_npdm(raw, contract_npdm(pub), grammar); z_ = decision_key_npdm(p_)
        rids = tok_ids(raw)                              # explicitly RE-TOKENIZED text IDs, not claimed to be original generated IDs
        g_.update(status='RUN', raw=raw, gen_s=round(_gen_dt9, 3), retokenized_ids=rids, retokenized_ids_sha256=sha_bytes(json.dumps(rids).encode()),
                  retokenized_token_count=len(rids), parse_status=p_['status'], pred_status=p_.get('pred_status'),
                  parsed=p_, decision=list(z_) if isinstance(z_, tuple) else z_, decision_class='WASTE' if z_ == 'WASTE' else key_898(z_),
                  raw_contains_UNKNOWN='UNKNOWN' in (raw or '').split(), car=lp, gpu_after=gpu_after)
        GENS.append(g_); R['generations'] = GENS
        ev('READOUT', **{k: v for k, v in g_.items() if k not in ('car','retokenized_ids','gpu_after')}); save()
        log('READOUT', g_['gen'], arm, grammar, '->', raw, '| mount_tokens', mtok, '| decision', g_['decision'])
    by = {(g_['arm'], g_['grammar']): g_ for g_ in GENS}
    mount_pairs = {}
    for arm in ('REAL','NEUTRAL1','NEUTRAL2'):
        mount_pairs[arm] = (by[(arm,'PRED')]['input_cartridge_sha256'] == by[(arm,'DIRECT')]['input_cartridge_sha256'] and
                            by[(arm,'PRED')]['mount_tokens'] == by[(arm,'DIRECT')]['mount_tokens'] == 232 and
                            by[(arm,'PRED')]['max_new_tokens'] == by[(arm,'DIRECT')]['max_new_tokens'])
    content_pairing = {}
    for name in ('NEUTRAL1','SWAPPED','NEUTRAL2'):
        gr = 'PRED'; a9, b9 = by[('REAL',gr)], by[(name,gr)]
        content_pairing[name] = (a9['factual_mount'] == b9['factual_mount'] and a9['query_sha256'] == b9['query_sha256'] and
                                 a9['input_cartridge_sha256'][:4] == b9['input_cartridge_sha256'][:4] and
                                 a9['input_cartridge_sha256'][4] != b9['input_cartridge_sha256'][4] and
                                 a9['mount_tokens'] == b9['mount_tokens'] == 232 and a9['max_new_tokens'] == b9['max_new_tokens'])
    for name in ('NEUTRAL1','NEUTRAL2'):
        a9, b9 = by[('REAL','DIRECT')], by[(name,'DIRECT')]
        content_pairing[name + '_DIRECT'] = (a9['factual_mount'] == b9['factual_mount'] and a9['query_sha256'] == b9['query_sha256'] and
                                 a9['input_cartridge_sha256'][:4] == b9['input_cartridge_sha256'][:4] and
                                 a9['input_cartridge_sha256'][4] != b9['input_cartridge_sha256'][4] and
                                 a9['mount_tokens'] == b9['mount_tokens'] == 232 and a9['max_new_tokens'] == b9['max_new_tokens'])
    REPRO = {
        'F_PRED_raw_equals_898': by[('F','PRED')]['raw'] == HIST_F['raw'],
        'F_PRED_mount_equals_898': by[('F','PRED')]['mount_tokens'] == HIST_F['mount_tokens'] == 98,
        'F_PRED_car_close_898_2e-4': car_close899(by[('F','PRED')]['car'], HIST_F['car'], 2e-4),
        'REAL_PRED_raw_equals_898': by[('REAL','PRED')]['raw'] == HIST_REAL['raw'],
        'REAL_PRED_mount_equals_898': by[('REAL','PRED')]['mount_tokens'] == HIST_REAL['mount_tokens'] == 232,
        'REAL_PRED_car_close_898_2e-4': car_close899(by[('REAL','PRED')]['car'], HIST_REAL['car'], 2e-4),
        'F_DIRECT_raw_equals_897': by[('F','DIRECT')]['raw'] == CT['L1']['raws']['DIRECT'],
        'REAL_repeat_raw_exact': by[('REAL_REPEAT','PRED')]['raw'] == by[('REAL','PRED')]['raw'],
        'REAL_repeat_retokenized_ids_exact': by[('REAL_REPEAT','PRED')]['retokenized_ids'] == by[('REAL','PRED')]['retokenized_ids'],
        'REAL_repeat_car_close_1e-5': car_close899(by[('REAL_REPEAT','PRED')]['car'], by[('REAL','PRED')]['car'], 1e-5),
        'all_B_mounts_232': all(g_['mount_tokens'] == 232 for g_ in GENS if g_['belief'] is not None),
        'both_F_mounts_98_and_identical': all(g_['mount_tokens'] == 98 for g_ in GENS if g_['arm'] == 'F') and
                                          by[('F','PRED')]['input_cartridge_sha256'] == by[('F','DIRECT')]['input_cartridge_sha256'],
        'all_car_greedy_consistent': all(g_['car']['greedy_consistent'] is True for g_ in GENS),
        'all_car_first_action_tokens_distinct': all(g_['car']['first_token_ids_distinct'] is True for g_ in GENS)}
    G3 = {'planned': 10, 'run': len(GENS), 'grammar_pairs_mount_exact': mount_pairs,
          'content_pairs_exact_except_B': content_pairing, 'historical_and_repeat_reproduction': REPRO,
          'invalid': sum(g_['parse_status'] == 'INVALID' for g_ in GENS),
          'abstain': sum(g_['parse_status'] == 'ABSTAIN' for g_ in GENS),
          'stop': sum(g_['parse_status'] == 'STOP' for g_ in GENS),
          'unknown_prediction': sum(g_['pred_status'] == 'UNKNOWN' for g_ in GENS),
          'waste': sum(g_['decision'] == 'WASTE' for g_ in GENS)}
    G3['ok'] = (G3['planned'] == G3['run'] == len(READ) and len(content_pairing) == 5 and
                all(content_pairing.values()) and all(mount_pairs.values()) and all(REPRO.values()))
    gate('GATE3_READOUT', 'PASS' if G3['ok'] else 'FAIL',
         '10/10 native generations; same-runtime history, REAL repeat and mount pairing fail-closed', counts=G3)

    # ============================================================ GATE4 OFFLINE EVALUATION (only after all 10 generations)
    norm = lambda z: tuple(z) if isinstance(z, list) else z
    pub = PUB['L1']; cc = contract_npdm(pub); left = CT['L1']['left']
    true_facts = facts_npdm(FRZ['L1'], pub['outcomes']); BAYES = bayes_npdm(cc, true_facts, left); OPT = BAYES['optimal']
    contract_ok = sorted(map(key_898, OPT)) == sorted(map(key_898, T898_TABLE['L1']))
    if not contract_ok: raise StopT896('L1_PUBLIC_BAYES_CONTRACT_TABLE_MISMATCH')
    _rows = {(g_['arm'] if g_['arm'] != 'REAL_REPEAT' else 'REAL_REPEAT', g_['grammar']): g_ for g_ in GENS}
    _swp = parse_belief_898(BELIEFS899['SWAPPED']['raw'])
    _swp_goal = [a_ for a_, o_ in belief_facts_898(_swp['fields'], pub) if o_ == pub['goal']] if _swp['valid'] else []
    C899 = classify899(_rows, OPT, cc, _swp_goal[0] if len(_swp_goal) == 1 else None)
    mech = C899['verdict']
    SCORE = {}
    for g_ in GENS:
        x_ = C899['scores']['%s/%s' % (g_['arm'], g_['grammar'])]
        SCORE[g_['gen']] = dict(x_, arm=g_['arm'], grammar=g_['grammar'], raw=g_['raw'], decision=g_['decision'],
                                unknown_raw_token=g_['raw_contains_UNKNOWN'])
    content_pred, content_direct, grammar_pairs = C899['content_pairs_PRED'], C899['content_pairs_DIRECT'], C899['grammar_pairs']
    grammar_contribution = C899['conditions']['grammar_contribution']; neutral_stable = C899['conditions']['neutral_baseline_stable']
    correctness_preservation = C899['conditions']['correctness_specific_content_preservation']
    tr = belief_truth_898(FRZ['L1'], pub)
    BEL = {}
    for name, v in BRANCH.items():
        BEL[name] = dict(belief_eval_898(parse_belief_898(v['raw']), pub, sorted(true_facts), tr['last_pred'],
                                         tr['last_pred_action'], tr['rel_true'], left, OPT), text_sha256=v['geo']['sha256'])
    CLS = {'verdict': mech, 'contract_table_agrees_with_evaluator': contract_ok, 'conditions': C899['conditions'],
           'grammar_pairs': grammar_pairs, 'content_pairs_PRED': content_pred, 'content_pairs_DIRECT': content_direct,
           'interpretation': {'raw_difference_is_not_policy_effect': True,
                              'neutral_divergence_limits_baseline_interpretation': not neutral_stable,
                              'B_necessity_or_incremental_utility_estimable': False,
                              'reason_no_incremental_utility': 'F/PRED is already optimal in the reproduced TEST898 L1 state',
                              'learning_transfer_autonomy_claimed': False,
                              'decision_vs_action': 'DECISION = native grammar decision (INVALID = WASTE); ACTION = written action prefix; '
                                                    'a decision change with an unchanged action prefix is a prediction-slot validity change',
                              'grammar_claim_scope': 'one state, one sample per arm, same mount and query except the grammar line: '
                                                     'descriptive within-state contrast, not a general causal grammar effect'},
           'scorer_limitations_898': {'unchanged': True,
               'GOAL': "NEG_KNOW_RX_898 lacks the standalone word 'no'; e.g. 'no, from no observation' can be a false negative",
               'BUDGET_STOP': "STOP_RX_898 does not recognize the terse pattern '<n>, no'; reported as UNCLASSIFIED, never repaired"}}
    R['offline'] = {'public_facts': sorted(true_facts), 'public_bayes': {'Q': {key_898(k): v for k,v in BAYES['Q'].items()},
                    'V': BAYES['V'], 'optimal': sorted(map(key_898, OPT))}, 'scores': SCORE, 'beliefs': BEL, 'classification': CLS}
    ev('OFFLINE_EVALUATION_DONE', verdict=mech, conditions=CLS['conditions'])
    gate('GATE4_OFFLINE_EVALUATION', 'DIAGNOSTIC', mech, conditions=CLS['conditions'], claims=CLS['interpretation'])
    for g_ in GENS: log('DECISION_SCORE', g_['gen'], json.dumps(SCORE[g_['gen']], sort_keys=True))
    # ------------------------------------------------------------------ the input archive was not modified by this run
    _end = {'zip_897_sha256_unchanged': sha_path(Path(T897['zip'])) == A0['zip_sha256_start'],
            'zip_898_sha256_unchanged': sha_path(Path(T898IN['zip'])) == T898IN['zip_sha256'],
            'extracted_897_inputs_unchanged': all(sha_path(v['path']) == v['sha256'] for v in ARCH.values()),
            'extracted_898_inputs_unchanged': all(sha_path(v['path']) == v['sha256'] for v in ARCH8.values()),
            'archived_897_cartridge_tensors_unchanged': all(_jn(seal_cp(ARCH_CP[b_])) == _jn(ARCH_ENT[b_]['tensor_seal']) for b_ in T898_REQ_FILES),
            'archived_898_REAL_tensor_unchanged': _jn(seal_cp(ARCH8_CP['REAL'])) == _jn(ARCH8_REAL_ENT['tensor_seal'])}
    gate('GATE0_ARCHIVE_END', 'PASS' if all(_end.values()) else 'FAIL', None if all(_end.values()) else 'input archive changed during the run', **_end)
    R['generation_budget'] = {'consolidation': 0, 'readout_run': sum(1 for g_ in GENS if g_.get('status') == 'RUN'),
                              'planned_readout': 10, 'planned': 10, 'native_generations_run': len(GENS),
                              'note': 'B controls are archived REAL or deterministic token substitutions; no new B generation is performed'}
    R['metrics'] = METRICS
    # ---------------------------------------------------------------------------------------- P1 / P7 final
    files_end = {e['cid']: sha_path(e['file']) == e['sha256'] for e in CART_INDEX}
    empty_end = seal_cp(CP_EMPTY) == EMPTY_ENT['tensor_seal']
    chain899_ok = (len(CHAIN899) == 6 and len({e['cid'] for e in CHAIN899}) == 6 and
                   all(e['parent_sha256'] == (ARCH_ENT[FRZ_FILES['L1'][-1]]['sha256'] if i == 0 else CHAIN899[i-1]['sha256'])
                       for i,e in enumerate(CHAIN899)))
    p1_ok = all(files_end.values()) and empty_end and chain899_ok and len(files_end) == len(CART_INDEX)
    gate('P1_PHYSICAL', 'PASS' if p1_ok else 'FAIL', None if p1_ok else 'a cartridge file SHA-256 changed after it was written',
         cartridge_files=len(CART_INDEX), files_unchanged=sum(files_end.values()), changed=[k for k, v in files_end.items() if not v],
         empty_tensor_seal_unchanged=empty_end, append_only_chain899=chain899_ok, cartridge_bytes=sum(Path(e['file']).stat().st_size for e in CART_INDEX))
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
    # ---------------------------------------------------------------- verdict: every technical gate PASS, then the GATE4 screen
    G_ = R['gates']; R['metrics'] = METRICS; R['gpu_peak'] = gpu_mem()
    TECH_GATES = tuple(g for g in GATE_ORDER if g != 'GATE4_OFFLINE_EVALUATION')
    tech = 'PASS' if all(G_[g]['status'] == 'PASS' for g in TECH_GATES) else 'FAIL'
    DEC = {'VERDICT': CLS['verdict'] if tech == 'PASS' else 'TECHNICAL_INVALID',
           'subcodes': [k + '=' + str(v) for k,v in CLS['conditions'].items()],
           'conditions': CLS['conditions'], 'claims': CLS['interpretation'], 'technical': tech,
           'failed_technical_gates': [g for g in TECH_GATES if G_[g]['status'] != 'PASS'],
           'scope': 'L1 mechanism isolation only; descriptive single-state evidence, not learning, transfer, autonomy, B necessity or incremental utility'}
    R['decision'] = DEC; R['technical_status'] = tech
    R['answers'] = {'Q1_archives_geometry_engine': {g: G_[g]['status'] for g in ('GATE0_ARCHIVE','GATE0B_898_ARCHIVE','GATE0C_GEOMETRY','GATE1_ENGINE','GATE0_ARCHIVE_END')},
                    'Q2_generation_counts': G_['GATE3_READOUT']['data'].get('counts'),
                    'Q3_same_runtime_reproduction': G3['historical_and_repeat_reproduction'],
                    'Q4_grammar_contribution': CLS['conditions']['grammar_contribution'],
                    'Q5_decision_level_content_influence': {'PRED': content_pred, 'DIRECT': content_direct},
                    'Q6_neutral_baseline_stable': neutral_stable,
                    'Q7_correctness_specific_content_preservation': correctness_preservation,
                    'Q8_B_necessity_or_incremental_utility': 'NOT_ESTIMABLE_F_PRED_ALREADY_OPTIMAL',
                    'Q9_CAR_scope': 'post-hoc teacher-forced generated-text logp only; no alternative action-sequence or prediction-slot distribution'}
    for k_, v_ in R['answers'].items(): log('ANSWER', k_, json.dumps(v_, default=str))
    log('DECISION', json.dumps({'VERDICT': DEC['VERDICT'], 'subcodes': DEC['subcodes'], 'conditions': DEC['conditions']}, default=str))
    R['status'] = 'COMPLETE'
except NoRun899 as e:
    R['status'] = 'NO_RUN'; R['stop_reason'] = str(e); log('NO_RUN', str(e))
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
        sci = ('NO_RUN' if R['status'] == 'NO_RUN' else ('TECHNICAL_INCOMPLETE' if 'ABORT_TECHNICAL_INCOMPLETE' in _sr else ('TECHNICAL_INCONCLUSIVE' if '=INCONCLUSIVE' in _sr else 'TECHNICAL_INVALID')))
    verdict = sci
    if 'answers' not in R:
        R['answers'] = {}
    R['verdict'] = verdict; R['verdict_scope'] = 'L1 mechanism isolation only: this cell and runtime; not learning, transfer, autonomy, B necessity or incremental utility'
    R['elapsed_s'] = round(time.perf_counter() - T0, 1)
    try: R['gpu_final'] = gpu_mem()
    except Exception: pass
    log('=' * 112)
    for g in GATE_ORDER: log('%-30s %-20s %s' % (g, G[g]['status'], G[g]['reason'] or ''))
    summary = {'verdict': verdict, 'subcodes': (R.get('decision') or {}).get('subcodes'), 'status': R['status'],
               'technical_status': R.get('technical_status'), 'gates': {g: G[g]['status'] for g in GATE_ORDER},
               'commit': COMMIT, 'model_revision': MODEL_REVISION, 'run_id': RUN_ID, 'elapsed_s': R['elapsed_s'],
               'scope': 'TEST899 L1 belief-to-policy mechanism isolation; diagnostic verdict is not a scientific PASS'}
    log('TEST899_BP_SUMMARY ' + json.dumps(summary, sort_keys=True, default=str))
    save()                                                     # last write of the report; it is not modified after this line
    # ------------------------------------------- artifacts (TEST870/889/892 contract: ZIP + SHA256SUMS + receipt + Drive)
    import zipfile
    AG = {'report_written_read_back': False, 'zip_testzip': False, 'sha256sums': False, 'required_files': False, 'report_in_zip_is_read_back_report': False,
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
            AG['sha256sums_detail'] = {'rows_wellformed': okm, 'members_unique': members is not None and len(members) == len(set(members)),
                                       'members_equal_rows': members is not None and set(members) - {'SHA256SUMS.txt'} == set(listed),
                                       'row_hashes_verified': okm and all(sha_bytes(z.read(root_ + '/' + rel)) == h_ for rel, h_ in listed.items())}
            AG['sha256sums'] = all(AG['sha256sums_detail'].values())
            _req = ['TEST899_BP_results.json', 'TEST899_BP.log', 'TEST899_BP_events.jsonl']
            if (R.get('executed_cell') or {}).get('status') == 'CAPTURED': _req.append('TEST899_BP_cell_source.py')
            if G['GATE0_ARCHIVE']['status'] != 'NOT_RUN': _req.append('TEST899_BP_input_manifest.json')
            if G['GATE0B_898_ARCHIVE']['status'] != 'NOT_RUN': _req.append('TEST899_BP_898_input_manifest.json')
            if G['GATE0C_GEOMETRY']['status'] != 'NOT_RUN': _req.append('TEST899_BP_geometry_manifest.json')
            AG['required_files_expected'] = _req; AG['required_files_missing'] = [k_ for k_ in _req if k_ not in listed]
            AG['required_files'] = not AG['required_files_missing']
            # every cartridge written in the run (Phase 1, calibration, derived arms) must be in the ZIP with its recorded SHA-256
            _ci = [e_ for e_ in (R.get('cartridges') or [])]
            AG['all_cartridges_in_zip'] = all(listed.get(Path(e_['file']).relative_to(ROOT).as_posix()) == e_['sha256'] for e_ in _ci)
            AG['cartridges_expected'] = len(_ci)
            AG['sha256sums_rows'] = len(rows)
            AG['report_in_zip_is_read_back_report'] = listed.get('TEST899_BP_results.json') == rep_sha
        zip_sha = sha_path(ZIP_PATH)
        if DRIVE_DIR is not None:
            try:
                dz = Path(DRIVE_DIR) / ZIP_PATH.name; shutil.copy2(ZIP_PATH, dz); AG['drive'] = sha_path(dz) == zip_sha
            except Exception as e:
                AG['drive'] = False; AG['drive_error'] = '%s: %s' % (type(e).__name__, e)
    except Exception as e:
        AG['artifact_error'] = '%s: %s' % (type(e).__name__, e)
    core = all(AG[k] is True for k in ('report_written_read_back', 'zip_testzip', 'sha256sums', 'required_files', 'report_in_zip_is_read_back_report'))
    AG['cell_identity_match'] = bool((R.get('executed_cell') or {}).get('identity_match'))
    # Fixed, terminating order: (1) final log lines, LOG frozen (console print only afterwards); (2) Drive copies of the
    # final log and report byte-verified; (3) ARTIFACT_STATUS; (4) receipt written, read back byte-for-byte, Drive copy
    # SHA-verified. On a receipt failure the receipt is rewritten ONCE with ARTIFACT_STATUS=FAIL and an unverified Drive
    # receipt copy is removed, so no file claims PASS without verification. The receipt does not contain its own hash.
    log('LOCAL FILES  :', ROOT, '|', ZIP_PATH if ZIP_PATH.exists() else 'ZIP NOT CREATED', '|', RECEIPT_PATH)
    log('DRIVE        :', DRIVE_DIR if DRIVE_DIR is not None else 'DRIVE_NOT_MOUNTED (%s)' % DRIVE_ERR['mount'])
    log('TEST899_BP_LOG_END SCIENTIFIC_VERDICT=%s | STATUS=%s | ZIP_CORE=%s | CELL_IDENTITY_MATCH=%s | final ARTIFACT_STATUS: '
        'receipt + console' % (verdict, R['status'], core, AG['cell_identity_match']))
    AG['final_log_sha256'] = sha_path(LOG); AG['drive_final_log'] = AG['drive_final_report'] = 'NOT_RUN'
    if DRIVE_DIR is not None:
        for key_, src_ in (('drive_final_log', LOG), ('drive_final_report', OUT)):
            try:
                dst_ = Path(DRIVE_DIR) / src_.name; shutil.copy2(src_, dst_); AG[key_] = dst_.read_bytes() == src_.read_bytes()
            except Exception as e:
                AG[key_] = False; AG[key_ + '_error'] = '%s: %s' % (type(e).__name__, e)
    AG.setdefault('all_cartridges_in_zip', False)
    fails = [k for k in ('report_written_read_back', 'zip_testzip', 'sha256sums', 'required_files', 'report_in_zip_is_read_back_report',
                         'all_cartridges_in_zip', 'cell_identity_match') if AG[k] is not True]
    if DRIVE_DIR is not None: fails += [k for k in ('drive', 'drive_final_log', 'drive_final_report') if AG[k] is not True]
    ART_STATUS = 'FAIL' if fails else ('PASS' if DRIVE_DIR is not None else 'INCOMPLETE_DRIVE_NOT_MOUNTED')
    # priority 1 (technical AND artefact integrity): a verdict whose artefacts are not verified is not a reportable verdict
    FINAL = verdict if ART_STATUS == 'PASS' else 'TECHNICAL_INCONCLUSIVE_ARTIFACT'
    receipt = {'test': 'TEST899_BP', 'run_id': RUN_ID, 'scientific_verdict': verdict, 'final_verdict': FINAL,
               'subcodes': summary.get('subcodes'), 'technical_status': R.get('technical_status'), 'status': R['status'],
               'answers': R.get('answers'),
               'artifact_gates': AG, 'gates': summary['gates'], 'report': str(OUT),
               'report_sha256': rep_sha, 'zip': str(ZIP_PATH), 'zip_sha256': zip_sha, 'final_log': str(LOG), 'drive_dir': DRIVE_DIR,
               'drive_mount_error': DRIVE_ERR['mount'], 'drive_backup_failures': DRIVE_ERR['backup_failures'],
               'engine_commit': COMMIT, 'model_revision': MODEL_REVISION, 'runtime_pins': R['runtime_pins'],
               'executed_cell': R.get('executed_cell'), 'previous': R['history'], 'input_archive_897': R.get('input_archive_check', {}).get('results_identity'),
               'input_archive_898': R.get('input_archive_898_check', {}).get('results_identity'),
               'geometry_preflight': (R.get('geometry_preflight') or {}).get('status'),
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
    print('TEST899_BP_FINAL FINAL_VERDICT=%s | SCIENTIFIC_VERDICT=%s | SUBCODES=%s | TECHNICAL_STATUS=%s | STATUS=%s | ARTIFACT_STATUS=%s' % (
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
