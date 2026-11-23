# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST908 — NATIVE INFORMATION CONTINUITY, EVENT-SOURCED AVAILABILITY, MODEL-SELECTED TWO-SOURCE
# WORKING SET.  Successor of TEST907A r2 (run 20261122T173245Z, commit 139f2410, blob bcee7a28: TECHNICAL PASS,
# XY_PAIR_NOT_REACHED[X: EXPECT=1; Y: EXPECT=1]). That run removed the untrusted cue after step 0 while the prediction was made at
# step 1, so q1(X) == q1(Y) and the mount was equal: equal native predictions were forced by determinism (input equivalence), and
# neither world READ the new PRED / OBS handles. TEST908 changes ONLY the model-facing information surface, never the engine:
#   (1) cue lifecycle, event-sourced: NOTE: <cue> is in q from the first decision until this world's PRED_SEALED event, never after
#       (kappa: CUE_RULE); never in a cartridge, never at F;
#   (2) action availability, event-sourced: "ACTIONS: PROBE_A=AVAILABLE" until ENV_EXECUTED -> OBS_SEALED -> CATALOG_COMMIT exist in
#       this order, "PROBE_A=CONSUMED" after (alpha: AVAIL_RULE); no outcome, recommendation, relevance or next-read hint;
#   (3) A+/A- one-step diagnostic at the first post-commit decision: A+ is the real decision; A- is ONE extra greedy decision on the
#       same mount / W / catalog / task / cue state with the availability value replaced by a presealed equal-length placebo; never
#       dispatched, environment locked, never in a verdict denominator; position-controlled only with equal q length, equal first
#       generated position, equal mount seal and one differing id window (else POSITION_CONFOUNDED_DIAGNOSTIC);
#   (4) reachability / collapse verdicts: PRED_INPUT_COLLAPSE (both ACQUIRE decisions saw equal q ids + mount), XY_PAIR_NOT_REACHED,
#       FORK_NOT_REACHED; arms only if both worlds READ_ADD PRED and OBS themselves. NATIVE_CLOSED_LOOP_PASS is not a TEST908 label.
# Everything else is TEST907A r2 unchanged (pinned 906 r2 engine called by blob; 903 mount_sealed / forge; 709 answer() greedy;
# 904 DecodeTap ids; strict parser; PRED sealed before the environment; OBS sibling on the empty 30-row prefix; 7 one-step arms;
# grounded PRED_CROSS; required-gate completeness; q-id / position replay; executed-source binding).
#
# FILE: 809.py (TEST908 r2 engine + notebook-cell self-capture; experiment remains TEST908).
#   (a) COPY/PASTE THE WHOLE 809.py into ONE EMPTY Colab cell and run that cell. No staged /content/908.py is required.
#       The executing cell's own IPython-registered text is hashed and saved as TEST908_executed_908.py for read-back authentication.
#   (b) %run /content/809.py           (kernel process; Drive auto-mount only AFTER the A100 pre-flight PASS)
#   (c) !python /content/809.py        (child process; mount Drive beforehand in another cell)
#   Offline re-scoring: python 809.py --recompute /content/TEST908_<run_id>/TEST908_results.json
#     VERIFIED (default): 0 only for an authenticated record, 3 = consistent but NOT_AUTHENTICATED, 1 = record problem;
#     --recompute-mode rescore = OFFLINE_RESCORE (scoring only, provenance not certified).
# ORDER (fixed): executed-source identity (local file) -> 906/903/904 pins (GitHub, network only) -> A100 PRE-FLIGHT (906 r2 torch-only
#   gate, then GATE_GPU_PREFLIGHT_908 = zero Drive operations so far; on failure GPU_REQUIRED_A100_TECHNICAL_STOP and Drive is never
#   touched) -> runtime pins -> Drive mount / presence / write-fsync-read-back probe (new MyDrive/TEST908_<run_id>) -> 903 archive,
#   TEST906 and TEST907A reference ZIP / results by pinned SHA (read-only) -> engine sources -> tokenizer -> disk -> sealed manifest ->
#   model -> 906 engine gate -> working-set ABI gate -> panel -> A- diagnostic gate -> arms -> end gate -> verdict -> ZIP + receipt
#   with byte read-back. Exit code (never the scientific verdict): 0 complete + delivered, 2 complete but Drive delivery failed,
#   1 technical abort (also: no A100).
# BUDGET: <= 6 native decisions per world (12) + <= 2 A- diagnostics + 14 arms + <= 2 FULL_REF = <= 30 greedy sequences, <= 65
#   generated ids each (<= 1950); 2 environment calls; 2 PRED + 2 OBS forges (+ <= 2 FULL_REF); created objects <= 16 MiB; GPU peak
#   hard abort 74 GiB; 903 guard limits unchanged.
# GPU CANDIDATE, NOT GPU-VERIFIED. NOT EXECUTED ON GPU BY ITS AUTHOR (GPU_NOT_RUN_BY_AUTHOR).
# =====================================================================================================================
import os, sys, json, hashlib, re, time, shutil, subprocess, zipfile, types, traceback, importlib.util, stat, marshal, copy
from pathlib import Path
from datetime import datetime, timezone
sys.dont_write_bytecode = True

TAG = 'TEST908'
REVISION = ('r2-cell-native: TEST908 = TEST907A r2 (blob bcee7a28) + event-sourced cue lifecycle (NOTE until PRED_SEALED) + event-sourced PROBE_A '
            'availability (AVAILABLE -> CONSUMED after ENV -> OBS seal -> catalog commit) + first post-commit A+/A- one-step diagnostic '
            '(presealed equal-length placebo) + PRED_INPUT_COLLAPSE verdict + staged-file source identity + A100-before-Drive guard')
MARKER = 'AKBASCORE SILICON HIPPOCAMPUS — TEST908 — native information continuity, event-sourced availability, model-selected two-source working set'
LABEL = 'GPU CANDIDATE, NOT GPU-VERIFIED'
SRC_REPO = 'ceceli33/titan-cognitive-core-v3'
SRC_URL = 'https://github.com/' + SRC_REPO
SELF_FILE = '809.py'
SRC906 = {'file': '906.py', 'commit': '471aa0d2f4fcdf56922135a24c03faa71c8efa35', 'git_blob': '96fe390dc1e8b8c1a43c802db533992e64291439',
          'sha256': '2e6a8b9d515e5481bf9f60a8e00f5582c85fef85e23e1feec32efaf98bb32cc9'}
SRC903 = {'file': '903.py', 'commit': 'ad228a29aacfc485377ed1d1a7aecae4d3201488', 'git_blob': 'f883d3dfa4c493bab4e4dc41b5743b30102ebd37',
          'sha256': '97fce064f5dafc18455d05ab015b9a476b063c801b7206401afbdfde1bc73ebc'}
SRC904 = {'file': '904.py', 'commit': 'ad228a29aacfc485377ed1d1a7aecae4d3201488', 'git_blob': '2ffacbec3b089759c89bf843d3725d617113d0ce',
          'sha256': 'c2d894d79f9d411bc8a8f7f2821fbcf3c67e41fd9f5b897d7f1e52a0cd20423b'}
ENGINE_BLOBS_908 = {'709.py': '6c9f8cbb1eeed848d45133d73f0d7676b68e9125', '730.py': 'b1bad9eb3b111b44413f8ef05a3a140ab66a77dd',
                     '757.py': '3d88bf8638390995858f23391f1e043faa586835'}      # must equal 903 ENGINE_BLOBS (checked at the ABI gate)
RUN906 = {'run_id': '20261121T140711Z', 'verdict': 'NRB_PHYSICAL_CAUSAL_READOUT[8/8; 4/4]', 'reads': 64, 'source_commit': SRC906['commit'],
          'log_git_blob': '8dfcb797ee91a095ae5a096a607c87ea417abd12', 'zip_name': 'TEST906_SONUC_20261121T140711Z.zip',
          'receipt_name': 'TEST906_SONUC_20261121T140711Z_RECEIPT.json', 'results_member': 'TEST906_20261121T140711Z/TEST906_results.json',
          'zip_sha256': 'cdc008e08386b36cb9d41c351832cd5d3efb0ba29d96900cce9b244d375ddc0d',
          'results_sha256': '1436e0e3cbe9df427561372b3c489cac648fd2945be3708f8751da78bbd7dd97',
          'evidence': ('verdict and read count from 906.log on GitHub; TEST908 author (2026-11-22): results.json and receipt downloaded read-only '
                       'from Drive (results SHA-256 equal; receipt names this ZIP SHA); ZIP size 56,823,741 equal, ZIP bytes NOT downloaded by the '
                       'author; re-verified read-only by GATE_REF906_908 at run time')}
MYDRIVE = Path('/content/drive/MyDrive')
DEFAULT_ARCHIVE_903 = '/content/drive/MyDrive/TEST903_20261120T192235Z'
DEFAULT_REF906_DIR = '/content/drive/MyDrive/TEST906_20261121T140711Z'
SRC907A = {'file': '907A.py', 'role': 'derived_from (908 = r2 + named edits, build_908.py)', 'commit': '139f2410a2e8ae742d7233a71e58fdc2943f0749',
           'git_blob': 'bcee7a280cc68d1b86ebabc2acfbc596d2f06541', 'sha256': 'b608407695788859b16b738c408f94ba6c26957e55379159747ef36c1c1fdcc0'}
RUN907A = {'run_id': '20261122T173245Z', 'verdict': 'XY_PAIR_NOT_REACHED[X: EXPECT=1; Y: EXPECT=1]', 'source_commit': SRC907A['commit'],
           'source_git_blob': SRC907A['git_blob'], 'log_git_blob': 'ea5417f328877f2858808a22baaf659eef69bcef',
           'zip_name': 'TEST907A_SONUC_20261122T173245Z.zip', 'receipt_name': 'TEST907A_SONUC_20261122T173245Z_RECEIPT.json',
           'results_member': 'TEST907A_20261122T173245Z/TEST907A_results.json',
           'zip_sha256': 'eb06adf2792548bc334934f07c947f1fa9d85a4c260395fa65df4e5f829d1086',
           'results_sha256': '68a67ab0747a5f163bdd15d7c4fa2b9dd9d04080dd47f1b00263345149ff8057',
           'evidence': ('TEST908 author (2026-11-22): results.json (94,171 bytes), events.jsonl, log and receipt downloaded read-only from Drive; results '
                        'SHA-256 equal; receipt names this ZIP SHA; ZIP size 30,137,222 equal; ZIP bytes NOT downloaded by the author (tool limit); '
                        'results member name derived from the r2 finalize_artifacts code; re-verified read-only by GATE_REF907A_908 at run time')}
DEFAULT_REF907A_DIR = '/content/drive/MyDrive/TEST907A_20261122T173245Z'

# ===================================================================================================== sealed design constants
P_PREFIX = 30; COMPILE_PROBE = 65; MAX_COMPILE = 64                     # = 906 r2 (decision budget: 64 storable ids + 1 stop detection)
WORLDS = ('X', 'Y'); OTHER_WORLD = {'X': 'Y', 'Y': 'X'}
TASK_TEXT = ('TASK: A device has two switches, A and B, and exactly one of them works. Decide which one works.\n'
             'You can test switch A once with PROBE_A. The test result is 1 if switch A works and 0 if it does not.\n'
             'Your memory is a catalog of sealed cartridges. Only the cartridges in your WORKING MEMORY are shown to you above as INFORMATION, in that order.\n'
             'Rule: before ACCEPT, every prediction in working memory that an observation in working memory contradicts must be corrected with REVISE.\n'
             'Reply with exactly one command and nothing else; keep any text or reason to a few words:\n'
             'READ_ADD(handle)  add a catalog cartridge to working memory (at most 3)\n'
             'READ_DEL(handle)  remove a cartridge from working memory\n'
             'READ_CLEAR()  empty working memory\n'
             'ACQUIRE(PROBE_A,EXPECT=e)  run the test once; e is 0 or 1, the result you predict before seeing it\n'
             'WRITE(handle,"text")  store a note under a new handle\n'
             'REVISE(handle,CITES[h1,h2],"text")  store a correction under a new handle, citing the prediction and the observation\n'
             'ACCEPT(A) or ACCEPT(B)  give the final answer\n'
             'STOP("reason")  end without an answer')
# trap 1 (908): the ONLY difference between X and Y. The NOTE is in q from the first decision until this world's PRED_SEALED event
# (CUE_RULE), absent afterwards; never in a cartridge, never at F.
CUES = {'X': 'Unverified hint from an earlier operator: switch A is probably the one that works.',
        'Y': 'Unverified hint from an earlier operator: switch A is probably not the one that works.'}
AVAIL_PREFIX = 'ACTIONS: '; AVAIL_ACTION = 'PROBE_A'; AVAIL_STATES = ('AVAILABLE', 'CONSUMED')
PLACEBO_CANDIDATES = ('UNSTATED', 'NOT_SHOWN', 'UNLISTED', 'OMITTED')     # A- value (no availability information); the tokenizer gate seals one
PLACEBO_WINDOW_MAX = 4                                                     # max width of the single differing q-id window A+ vs A-
FORBIDDEN_SURFACE_WORDS = ('read', 'recommend', 'next', 'expect', 'result', 'outcome', 'answer', 'revise', 'accept', 'correct', 'relevant', 'qk7',
                           'tb2', 'mz4', 'works', 'true', 'false', 'contradict', 'confirm')
CUE_RULE = ('kappa = 1 (NOTE: <cue of the world> in q) until the PRED_SEALED event of this branch exists; 0 forever after; event-sourced '
            '(never the step index, the parsed action or the outcome)')
AVAIL_RULE = ('ACTIONS: PROBE_A=AVAILABLE until ENV_EXECUTED -> OBS_SEALED -> CATALOG_COMMIT exist in this order in the branch events; '
              'PROBE_A=CONSUMED after; never from a parsed ACQUIRE alone; never an outcome, a recommendation or a handle')
TRUTH = {'A': 0, 'B': 1}; ANSWER = 'B'; ENV_ACTIONS = ('PROBE_A',)
OBS_TEMPLATE = '\nOBSERVATION: PROBE_A returned {o}.\n'               # environment record; no prediction, EXPECT or contradiction label
HANDLES = {'decoy': 'MZ4', 'pred': 'QK7', 'obs': 'TB2'}              # opaque, fixed before the model; identical in X and Y
DECOY_SOURCE = {'group': ['NS-A', 'R0'], 'archive_key': 'E_IND', 'why': 'archived 903 observation record of another episode (NATIVE, 19 body rows)'}
CATALOG_FIELDS = ('handle', 'kind', 'origin', 'episode', 'event_seq', 'cause', 'cites')
CATALOG_KINDS = ('PRED', 'OBS', 'REV', 'NOTE'); CATALOG_ORIGINS = ('MODEL', 'ENV', 'ARCHIVE')
FORBIDDEN_CATALOG_WORDS = ('expect', 'outcome', 'result', 'correct', 'relevant', 'important', 'recommend', 'read_next', 'answer', 'contradict',
                           'confirm', 'true', 'false', 'works', 'score', 'utility', 'evaluat')
FORBIDDEN_CUE_WORDS = ('expect', 'answer', 'evaluat', 'outcome', 'result', 'contradict', 'revise', 'accept', 'probe', 'acquire', 'observation',
                       '=0', '=1', 'cartridge', 'catalog')
WS_CAPACITY = 3; MAX_PREFIX_CALLS = 6
ARM_NAMES = ('BOTH_NATIVE', 'P_ONLY', 'O_ONLY', 'NONE', 'ORDER_REV', 'PRED_CROSS', 'FILE_SHAM')
_H = r'[A-Za-z][A-Za-z0-9_\-]{0,15}'
GRAMMAR = {'READ_ADD': r'READ_ADD\(\s*(?P<handle>%s)\s*\)' % _H, 'READ_DEL': r'READ_DEL\(\s*(?P<handle>%s)\s*\)' % _H, 'READ_CLEAR': r'READ_CLEAR\(\s*\)',
           'ACQUIRE': r'ACQUIRE\(\s*(?P<action>PROBE_A)\s*,\s*EXPECT\s*=\s*(?P<expect>[01])\s*\)',
           'WRITE': r'WRITE\(\s*(?P<handle>%s)\s*,\s*"(?P<text>[^"\n]*)"\s*\)' % _H,
           'REVISE': r'REVISE\(\s*(?P<handle>%s)\s*,\s*CITES\s*\[\s*(?P<cites>%s(?:\s*,\s*%s)*)\s*\]\s*,\s*"(?P<text>[^"\n]*)"\s*\)' % (_H, _H, _H),
           'ACCEPT': r'ACCEPT\(\s*(?P<answer>[AB])\s*\)', 'STOP': r'STOP\(\s*"(?P<reason>[^"\n]*)"\s*\)'}
GRAMMAR_RE = {k: re.compile(v) for k, v in GRAMMAR.items()}
PARSER_RULE = ('the decision text is tok.decode(DecodeTap ids) (VALID ids contain no special id); only leading / trailing whitespace is '
               'removed; the WHOLE remainder must match exactly one GRAMMAR entry (re.fullmatch); anything else (two commands, prose, a '
               'trailing period, an unknown environment action, a missing quote) is INVALID_NATIVE_ACTION. No snippet extraction, no '
               'repair, no retry, no scoring of alternatives.')
BUDGET = {'prefix_calls_per_world': [1, MAX_PREFIX_CALLS], 'prefix_calls_max': 2 * MAX_PREFIX_CALLS, 'avail_diagnostic_max': 2,
          'arm_reads': 2 * len(ARM_NAMES), 'fullref_reads_max': 2, 'greedy_sequences_max': 30, 'generated_ids_max_each': COMPILE_PROBE,
          'generated_ids_max': 30 * COMPILE_PROBE, 'pred_forges': 2, 'obs_forges': 2, 'fullref_forges_max': 2, 'env_calls': 2,
          'created_object_bytes_max': 16 * 2**20, 'gpu_peak_abort_gib': 74.0,
          'note': 'TEST908 table: 12 prefix + 2 A- diagnostic + 14 arms + <= 2 FULL_REF = <= 30 sequences; no minimum is a success condition'}
VERDICT_LABELS = ('TECHNICAL_MISMATCH', 'GPU_REQUIRED_A100_TECHNICAL_STOP', 'XY_PAIR_NOT_REACHED', 'NATIVE_SELECTION_UNREACHABLE', 'FORK_NOT_REACHED',
                  'NO_IDENTIFIABLE_ADDRESS', 'CONTEXT_MISSING', 'INVENTORY_OMISSION', 'PHYSICAL_READOUT_FAILURE', 'PHYSICAL_ATTRIBUTION_FAILURE',
                  'GEOMETRY_NOT_EXCHANGEABLE', 'ORDER_NOT_EXCHANGEABLE', 'UNGROUNDED_REVISE', 'INVALID_NATIVE_ACTION', 'WS_CAPACITY_INVALID',
                  'BUDGET_ABORT', 'CONTROL_UNAVAILABLE', 'PRED_INPUT_COLLAPSE', 'POSITION_CONFOUNDED_DIAGNOSTIC', 'TEST908_NATIVE_TWO_SOURCE_GAIN',
                  'TEST908_NO_GAIN')
TASK_TEXT_SHA256 = 'e912b6ddb7f7bff6fd8ee491c6a706e1b56a11e2ed8e9dd4f69f7a39d655bc9e'
DESIGN_SHA256 = '0ea40283bcb96792b3dd21cf5d5b0331d23158f12600e2aa69b27f298961c0fb'                                            # cues, truth, observation template, handles, grammar, catalog rule
CRITICAL_908 = ('GATE_SOURCES_908', 'GATE_EXECUTED_SOURCE', 'GATE_GPU_PREFLIGHT_908', 'GATE_REF906_908', 'GATE_REF907A_908', 'GATE_TOKENIZER_908',
                 'GATE_MANIFEST_908', 'GATE_WS_ABI_908', 'GATE_PREFIX_908', 'GATE_AVAIL_908', 'GATE_ARMS_908', 'GATE_FULLREF_908', 'GATE_END_908')
# every gate a COMPLETE run passes; --recompute authenticates a record only if all are PASS (record AND event log)
REQUIRED_PASS_GATES = ('GATE_SOURCES_908', 'GATE_EXECUTED_SOURCE', 'GATE_GPU_PREFLIGHT_906', 'GATE_GPU_PREFLIGHT_908', 'GATE_RUNTIME_PINS', 'GATE_ENV',
                       'GATE_VRAM_FREE', 'GATE_DRIVE_PRESENT', 'GATE_DRIVE', 'GATE_ARCHIVE_906', 'GATE_REF906_908', 'GATE_REF907A_908',
                       'GATE_SOURCE_EXTRACT', 'GATE_ARCHIVE_TENSORS_906', 'GATE_TOKENIZER_PRE_MODEL', 'GATE_TOKENIZER_908', 'GATE_DISK_906',
                       'GATE_MANIFEST_908', 'MODEL', 'GATE_ENGINE_906', 'GATE_WS_ABI_908', 'GATE_PREFIX_908', 'GATE_AVAIL_908', 'GATE_ARMS_908',
                       'GATE_FULLREF_908', 'GATE_END_908')
DRIVE_GATES = ('GATE_DRIVE_PRESENT', 'GATE_DRIVE', 'GATE_ARCHIVE_906', 'GATE_REF906_908', 'GATE_REF907A_908')   # 908: only after the A100 pre-flight
GATE_STATUSES = ('PASS', 'FAIL', 'DIAGNOSTIC')                       # the only statuses 903 gate() can record


def required_gate_status(gates, technical_blockers=None, events=None, required=None):
    """r2 (P2-A): the ONE technical gate rule of the live verdict, --recompute (both modes) and authenticate_record. PASS only if
    the gate record is a dict, every recorded gate has a known status and none is FAIL, every REQUIRED_PASS_GATES member is present
    with status exactly PASS, and there is no technical blocker. With an event list (live: this run's events file; verified recompute:
    the run's events file) every required gate must also have a PASS event and only PASS / DIAGNOSTIC events, and every recorded gate's
    LAST event must equal its recorded status. Extra (non-required) gates may be PASS or DIAGNOSTIC; FAIL / unknown / malformed fails."""
    req = REQUIRED_PASS_GATES if required is None else tuple(required); why = []
    if not isinstance(gates, dict): return False, ['GATES_NOT_A_DICT']
    for name, g in sorted(gates.items()):
        st = g.get('status') if isinstance(g, dict) else None
        if st not in GATE_STATUSES: why.append('GATE_RECORD_MALFORMED:%s' % name)
        elif st == 'FAIL': why.append('GATE_FAIL:%s' % name)
    for name in req:
        g = gates.get(name); st = g.get('status') if isinstance(g, dict) else None
        if g is None: why.append('GATE_MISSING:%s' % name)
        elif st != 'PASS': why.append('GATE_NOT_PASS:%s:%s' % (name, st))
    if technical_blockers: why.append('TECHNICAL_BLOCKERS:%d' % len(technical_blockers))
    if events is not None:
        gev = {}
        for e in events:
            if isinstance(e, dict) and e.get('kind') == 'GATE': gev.setdefault(e.get('name'), []).append(e.get('status'))
        for name in req:
            evs = gev.get(name, [])
            if 'PASS' not in evs or any(x not in ('PASS', 'DIAGNOSTIC') for x in evs): why.append('GATE_EVENT_CHAIN:%s:%s' % (name, evs))
        for name, g in sorted(gates.items()):
            evs = gev.get(name, [])
            if isinstance(g, dict) and (not evs or evs[-1] != g.get('status')): why.append('GATE_EVENT_LAST_NE_RECORD:%s:%s' % (name, evs[-1:]))
    return not why, why


def read_events(path):
    """the run's append-only events file as a list (None if it cannot be read: the caller then fails closed)."""
    try: return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]
    except Exception: return None


# functions of the pinned 906 module that 908 CALLS (by name; never redefined here: 906 read_path_isolation reads their source)
REUSED_906 = ('gpu_preflight', 'vram_gate', 'ensure_drive_906', 'drive_presence', 'archive_gate', 'archive_tensors_gate', 'disk_gate', 'engine_gate',
              'compile_z', 'forge_z', '_guard', 'rope_move_np', 'cos_np', 'rope_config', 'bind_903', 'read_path_isolation', 'duplicate_top_level')
ISOLATION_NAMES_906 = ('read_mount', '_gen_and_diag', '_seals', 'compile_z', 'forge_z', '_guard')


def sha_b(b): return hashlib.sha256(b).hexdigest()


def sha_s(s): return sha_b(s.encode('utf-8'))


def blob_b(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


def canon(v): return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(',', ':'), default=list)


def jsha(v): return sha_s(canon(v))


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(4 << 20), b''): h.update(c)
    return h.hexdigest()


class Stop908(Exception):
    """technical stop (never a scientific result); the message names the gate / object."""


def design_view():
    return {'cues': CUES, 'truth': TRUTH, 'answer': ANSWER, 'env_actions': list(ENV_ACTIONS), 'obs_template': OBS_TEMPLATE, 'handles': HANDLES,
            'decoy': DECOY_SOURCE, 'catalog_fields': list(CATALOG_FIELDS), 'grammar': GRAMMAR, 'ws_capacity': WS_CAPACITY, 'max_prefix_calls': MAX_PREFIX_CALLS,
            'arms': list(ARM_NAMES), 'parser_rule': PARSER_RULE,
            'avail': {'prefix': AVAIL_PREFIX, 'action': AVAIL_ACTION, 'states': list(AVAIL_STATES), 'placebo_candidates': list(PLACEBO_CANDIDATES),
                      'window_max': PLACEBO_WINDOW_MAX, 'forbidden': list(FORBIDDEN_SURFACE_WORDS)}, 'cue_rule': CUE_RULE, 'avail_rule': AVAIL_RULE}


if sha_s(TASK_TEXT) != TASK_TEXT_SHA256: raise Stop908('TASK_TEXT_CHANGED')
if jsha(design_view()) != DESIGN_SHA256: raise Stop908('DESIGN_CHANGED')


def compile_status(gen_ids, special_ids):
    """precedence (r2): not a list of non-negative int -> INVALID; empty -> INVALID; ANY special id (any position, also inside 65)
    -> INVALID; more than the probe budget -> INVALID; exactly 65 non-special ids (no stop within 64) -> CAPACITY_LIMIT; else VALID."""
    if not isinstance(gen_ids, list) or not all(isinstance(i, int) and not isinstance(i, bool) for i in gen_ids): return 'COMPILER_INVALID', 'IDS_NOT_A_LIST_OF_INT'
    if any(i < 0 for i in gen_ids): return 'COMPILER_INVALID', 'NEGATIVE_ID'
    if len(gen_ids) == 0: return 'COMPILER_INVALID', 'EMPTY'
    sp = sorted(set(gen_ids) & set(special_ids))
    if sp: return 'COMPILER_INVALID', 'SPECIAL_IDS %s' % sp
    if len(gen_ids) > COMPILE_PROBE: return 'COMPILER_INVALID', 'MORE_IDS_THAN_THE_PROBE_BUDGET'
    if len(gen_ids) == COMPILE_PROBE: return 'CAPACITY_LIMIT', 'NO_STOP_WITHIN_%d' % MAX_COMPILE
    return 'VALID', None


# ===================================================================================================== model-facing surface (pure)
def catalog_entry(handle, kind, origin, episode, event_seq, cause=None, cites=None):
    """metadata only: handle, kind, origin, episode, event order, cause link, cites. No content, EXPECT, outcome or label."""
    if kind not in CATALOG_KINDS or origin not in CATALOG_ORIGINS: raise ValueError('CATALOG_KIND_OR_ORIGIN %s %s' % (kind, origin))
    return {'handle': handle, 'kind': kind, 'origin': origin, 'episode': episode, 'event_seq': int(event_seq), 'cause': cause, 'cites': list(cites) if cites else None}


def render_entry(e):
    if tuple(sorted(e)) != tuple(sorted(CATALOG_FIELDS)): raise ValueError('CATALOG_FIELDS %s' % sorted(e))
    s = '%s kind=%s origin=%s episode=%s event=%d cause=%s cites=%s' % (e['handle'], e['kind'], e['origin'], e['episode'], e['event_seq'], e['cause'] or '-',
                                                                       ','.join(e['cites']) if e['cites'] else '-')
    if any(w in s.lower() for w in FORBIDDEN_CATALOG_WORDS): raise ValueError('CATALOG_FORBIDDEN_WORD %r' % s)
    return s


def build_q(task_text, cue, avail, catalog_view, ws):
    """the 709 QUESTION of one decision (908): sealed task text; the untrusted NOTE while the cue is live (cue is not None: from the
    first decision until this world's PRED_SEALED event, CUE_RULE); one event-sourced action-availability line (AVAIL_RULE; a
    presealed placebo value only for the A- diagnostic); the metadata catalog in commit order; the ordered working memory. Nothing
    else: no earlier generated text, no outcome, no recommendation."""
    if avail not in AVAIL_STATES and avail not in PLACEBO_CANDIDATES: raise ValueError('AVAIL_VALUE %r' % (avail,))
    lines = [task_text] + (['NOTE: ' + cue] if cue is not None else []) + [AVAIL_PREFIX + AVAIL_ACTION + '=' + avail]
    lines += ['CATALOG:'] + ([render_entry(e) for e in catalog_view] or ['(empty)'])
    lines.append('WORKING MEMORY: ' + (', '.join(ws) if ws else '(empty)'))
    return '\n'.join(lines)


def cue_live(events):
    """kappa (CUE_RULE): True until this branch's event list holds a PRED_SEALED event, False forever after. Derived from events only
    (never from the step index, a parsed action or the outcome)."""
    return not any(isinstance(e, dict) and e.get('kind') == 'PRED_SEALED' for e in events)


def availability(events):
    """alpha (AVAIL_RULE): 'CONSUMED' only if ENV_EXECUTED, OBS_SEALED and CATALOG_COMMIT occur in this order in this branch's events;
    else 'AVAILABLE'. A parsed ACQUIRE, a PRED seal or an environment call alone never consumes."""
    kinds = [e.get('kind') if isinstance(e, dict) else None for e in events]
    try:
        i = kinds.index('ENV_EXECUTED'); j = kinds.index('OBS_SEALED', i + 1); kinds.index('CATALOG_COMMIT', j + 1)
    except ValueError:
        return AVAIL_STATES[0]
    return AVAIL_STATES[1]


def parse_action(text):
    """strict full-output parser (PARSER_RULE). Returns {'op': ...} or {'op': 'INVALID', 'why': ...}."""
    if not isinstance(text, str): return {'op': 'INVALID', 'why': 'NO_TEXT'}
    s = text.strip()
    hits = [(k, m) for k, m in ((k, r.fullmatch(s)) for k, r in GRAMMAR_RE.items()) if m]
    if len(hits) != 1: return {'op': 'INVALID', 'why': 'NO_GRAMMAR_MATCH' if not hits else 'AMBIGUOUS_GRAMMAR'}
    k, m = hits[0]; d = {'op': k}
    for f, v in m.groupdict().items():
        if f == 'expect': v = int(v)
        if f == 'cites': v = [x.strip() for x in v.split(',')]
        d[f] = v
    return d


def ws_apply(ws, act, known):
    """the working-set transition of one parsed READ command (pure; never chooses, sorts, completes or evicts)."""
    op = act.get('op'); ws = tuple(ws)
    if op == 'READ_ADD':
        h = act['handle']
        if h not in known: return ws, 'UNKNOWN_HANDLE_INVALID'
        if h in ws: return ws, 'WS_DUPLICATE_NOOP'
        if len(ws) >= WS_CAPACITY: return ws, 'WS_CAPACITY_INVALID'
        return ws + (h,), 'WS_ADDED'
    if op == 'READ_DEL':
        h = act['handle']
        if h not in known: return ws, 'UNKNOWN_HANDLE_INVALID'
        if h not in ws: return ws, 'WS_DEL_ABSENT_INVALID'
        return tuple(x for x in ws if x != h), 'WS_REMOVED'
    if op == 'READ_CLEAR': return (), 'WS_CLEARED'
    return ws, 'WS_UNCHANGED'


def fork_condition(ws):
    return HANDLES['pred'] in ws and HANDLES['obs'] in ws


def slots_of(ents):
    """dynamic multi-slot geometry of a mount: target t_i = 30 + sum_{j<i} m_j; CHILD source = pos0, NATIVE source = P (757)."""
    out = []; at = P_PREFIX
    for e in ents:
        if e['kind'] == 'CHILD': m, s0 = int(e['n']), int(e['pos0'])
        elif e['kind'] == 'NATIVE': m, s0 = int(e['body_tokens']), P_PREFIX
        else: raise Stop908('UNKNOWN_KIND %s' % e.get('kind'))
        out.append({'m': m, 'source_pos0': s0, 'target_pos0': at}); at += m
    return out, at


class Env908:
    """sandbox environment: receives the action name only (never EXPECT, the model text, an evaluator or a confidence). TOTAL counts
    every step of every instance of this run (a branch cannot hide a call behind a fresh instance)."""
    TOTAL = [0]

    def __init__(self, truth, locked=False): self._truth = dict(truth); self.calls = []; self.locked = locked

    def step(self, action):
        if self.locked: raise Stop908('ENV_CALL_IN_BRANCH')
        if action not in ENV_ACTIONS: raise Stop908('ENV_UNKNOWN_ACTION %r' % action)
        if self.calls: raise Stop908('ENV_SECOND_CALL')
        Env908.TOTAL[0] += 1; self.calls.append(action); return int(self._truth['A'])

    def clone(self, locked=True):
        e = Env908(self._truth, locked); e.calls = list(self.calls); return e


class Branch:
    """copy-on-write state of one native trajectory, fork arm or A- diagnostic: ordered W, branch-local catalog, handle -> object map,
    environment snapshot, own event list, own counters, own namespace for new files. Sealed objects are shared read-only. (908) fork()
    copies the parent's event list, so the child's cue / availability projection equals the parent's at the fork point; the child's
    own events follow index inherited_events."""
    def __init__(self, bid, world, ws, catalog, env, hmap, namespace, events=None):
        self.bid = bid; self.world = world; self.ws = tuple(ws); self.catalog = copy.deepcopy(list(catalog)); self.env = env
        self.hmap = dict(hmap); self.dir = Path(namespace); self.events = copy.deepcopy(list(events or [])); self.inherited_events = len(self.events)
        self.counters = {'decisions': 0, 'generated_ids': 0}

    def fork(self, bid, namespace):
        return Branch(bid, self.world, self.ws, self.catalog, self.env.clone(locked=True), self.hmap, namespace, events=self.events)


def arm_keys(arm, ws, hmap, other_hmap, sham):
    """(handle, object key) of every mounted slot of a fork arm, from the F snapshot only."""
    hp, ho = HANDLES['pred'], HANDLES['obs']
    if arm == 'BOTH_NATIVE': return [(h, hmap[h]) for h in ws]
    if arm == 'P_ONLY': return [(hp, hmap[hp])]
    if arm == 'O_ONLY': return [(ho, hmap[ho])]
    if arm == 'NONE': return []
    if arm == 'ORDER_REV': return [(h, hmap[h]) for h in reversed(ws)]
    if arm == 'PRED_CROSS': return [(h, other_hmap[hp] if h == hp else hmap[h]) for h in ws]
    if arm == 'FILE_SHAM': return [(h, sham[hmap[h]]) for h in ws]
    raise Stop908('UNKNOWN_ARM ' + arm)


DECISION_PATH = {'build_q': ['task_text', 'cue', 'avail', 'catalog_view', 'ws'], 'cue_live': ['events'], 'availability': ['events'], 'render_entry': ['e'],
                 'parse_action': ['text'], 'ws_apply': ['ws', 'act', 'known'], 'fork_condition': ['ws'], 'arm_keys': ['arm', 'ws', 'hmap', 'other_hmap', 'sham'],
                 'catalog_entry': ['handle', 'kind', 'origin', 'episode', 'event_seq', 'cause', 'cites']}
DECISION_PATH_ALLOWED = {'CATALOG_FIELDS', 'CATALOG_KINDS', 'CATALOG_ORIGINS', 'FORBIDDEN_CATALOG_WORDS', 'render_entry', 'GRAMMAR_RE', 'HANDLES', 'WS_CAPACITY',
                         'Stop908', 'ValueError', 'isinstance', 'str', 'int', 'len', 'list', 'tuple', 'sorted', 'any', 'dict', 'reversed', 'set',
                         'AVAIL_PREFIX', 'AVAIL_ACTION', 'AVAIL_STATES', 'PLACEBO_CANDIDATES'}


def decision_path_isolation():
    """the functions that build what the model sees, parse what it wrote and apply it may read only the sealed design constants
    (symbol tables + parameter lists); the decision itself is the pinned 906 compile_z (its own isolation is 906's engine gate)."""
    import symtable, inspect, textwrap
    try: return _decision_path_isolation(symtable, inspect)
    except Exception as e: return {'ok': False, 'error': '%s: %s' % (type(e).__name__, e)}


def _decision_path_isolation(symtable, inspect):
    out = {}
    for name, params in DECISION_PATH.items():
        f = globals()[name]; src = func_src(f); t = symtable.symtable(src, name, 'exec').get_children()[0]
        g = sorted({x.get_name() for x in t.get_symbols() if x.is_global()})
        out[name] = {'globals': g, 'not_allowed': sorted(set(g) - DECISION_PATH_ALLOWED), 'params_ok': list(inspect.signature(f).parameters) == params}
    src = func_src(Env908); cls = symtable.symtable(src, 'Env908', 'exec').get_children()[0]
    step = [c for c in cls.get_children() if c.get_name() == 'step'][0]
    out['Env908.step'] = {'params': list(step.get_parameters()), 'params_ok': list(step.get_parameters()) == ['self', 'action'],
                           'globals': sorted({x.get_name() for x in step.get_symbols() if x.is_global()})}
    out['Env908.step']['not_allowed'] = sorted(set(out['Env908.step']['globals']) - {'Stop908', 'ENV_ACTIONS', 'int', 'Env908'})
    own = _own_top_names(); out['no_906_isolation_name_redefined'] = own is not None and not [n for n in ISOLATION_NAMES_906 + REUSED_906 if n in own]
    out['ok'] = all(v['params_ok'] and not v['not_allowed'] for k, v in out.items() if isinstance(v, dict)) and out['no_906_isolation_name_redefined']
    return out


def func_src(f):
    """source of a 908 function / class: from the verified executed bytes (exec() in a kernel has no file), else inspect."""
    import ast, inspect, textwrap
    b = getattr(X, 'SELF_BYTES', None)
    if b:
        src = b.decode('utf-8')
        for n in ast.parse(src).body:
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == f.__name__: return ast.get_source_segment(src, n)
    return textwrap.dedent(inspect.getsource(f))


def _own_top_names():
    """top-level def / class names of the executing 908 bytes (None if the bytes are unknown: the check then fails closed)."""
    import ast
    b = getattr(X, 'SELF_BYTES', None)
    if not b and globals().get('__file__') and Path(globals()['__file__']).is_file(): b = Path(globals()['__file__']).read_bytes()
    return {n.name for n in ast.parse(b.decode('utf-8')).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))} if b else None


# ===================================================================================================== evaluator (pure, offline; never on the read path)
def classify_action(act, mounted, answer=ANSWER):
    """class of one parsed F decision. REVISE citing both PRED and OBS = CONTRADICTION_MARKED (grounded iff every cited handle is
    physically mounted in that arm); ACCEPT(answer) = CONFIRMED. The correct final answer alone is never a two-source signal."""
    op = act.get('op'); hp, ho = HANDLES['pred'], HANDLES['obs']
    if op == 'INVALID': return {'class': 'INVALID_NATIVE_ACTION', 'grounded': None}
    if op == 'REVISE':
        c = set(act['cites']); return {'class': 'CONTRADICTION_MARKED' if {hp, ho} <= c else 'REVISE_MISCITED', 'grounded': c <= set(mounted)}
    if op == 'ACCEPT': return {'class': 'CONFIRMED' if act['answer'] == answer else 'WRONG_ACCEPT', 'grounded': None}
    return {'class': {'READ_ADD': 'READ_MORE', 'READ_DEL': 'READ_MORE', 'READ_CLEAR': 'READ_MORE', 'ACQUIRE': 'ACQUIRE_AGAIN', 'WRITE': 'WRITE', 'STOP': 'STOP'}[op],
            'grounded': None}


def pattern(contra, confirm, need_grounded=True):
    """the contradiction / confirmation distinction: contradiction world marked (grounded), confirmation world confirmed."""
    return (contra['class'] == 'CONTRADICTION_MARKED' and (contra['grounded'] is True or not need_grounded)) and confirm['class'] == 'CONFIRMED'


def cross_follows_prediction(contra_cross, confirm_cross):
    """r2 (P1): PRED_CROSS puts the OTHER world's physical prediction in the PRED slot. It follows the physical prediction only if
    the confirmation world (now holding the contradicting PRED tensor) marks the contradiction with a GROUNDED REVISE citing PRED and
    OBS (every cited handle mounted in that arm: the same pattern() rule as BOTH_NATIVE) and the contradiction world (now holding the
    confirming PRED) gives ACCEPT(answer). A class flip carried by an ungrounded REVISE is 'UNGROUNDED' (never 'FOLLOWS')."""
    if pattern(confirm_cross, contra_cross): return 'FOLLOWS'
    if pattern(confirm_cross, contra_cross, need_grounded=False): return 'UNGROUNDED'
    return 'NOT_FOLLOWED'


def address_identifiable(man):
    """trap: equal model-facing metadata (handle aside) for a relevant and the decoy handle makes 'correct addressing' a coin flip."""
    ce = man['catalog_entries']; key = lambda e: tuple((f, json.dumps(e[f])) for f in CATALOG_FIELDS if f != 'handle')
    return all(key(ce[r]) != key(ce['decoy']) for r in ('pred', 'obs'))


def prefix_summary(P):
    """per world: valid ACQUIRE?, its EXPECT and cell, fork reached?, end reason, A- diagnostic present (from the raw prefix record)."""
    acq = [d for d in P.get('decisions', []) if (d.get('action') or {}).get('op') == 'ACQUIRE' and (d.get('dispatch') or {}).get('result') == 'ACQUIRED']
    return {'acquired': bool(acq), 'expect': acq[0]['action']['expect'] if acq else None, 'acquire_cell': acq[0].get('cell_id') if acq else None,
            'fork': P.get('fork') is not None, 'end': P.get('end'), 'calls': len(P.get('decisions', [])), 'avail_diag': bool(P.get('avail_diag'))}


def _window_ok(a, b):
    """A+ / A- q ids: equal length and exactly one contiguous differing window of at most PLACEBO_WINDOW_MAX ids."""
    if not (_id_list(a) and _id_list(b)) or len(a) != len(b): return False
    diff = [k for k in range(len(a)) if a[k] != b[k]]
    return bool(diff) and diff[-1] - diff[0] + 1 <= PLACEBO_WINDOW_MAX


def position_controlled(plus, minus):
    """the A- record is position-controlled against its A+ decision iff equal q length, a single differing id window, equal first
    generated position and the same physical mount seal and keys (otherwise POSITION_CONFOUNDED_DIAGNOSTIC)."""
    pm, mm = (plus or {}).get('mount') or {}, (minus or {}).get('mount') or {}
    return bool(_window_ok((plus or {}).get('q_ids'), (minus or {}).get('q_ids')) and pm.get('first_generated_position') == mm.get('first_generated_position')
                and _hex(pm.get('mount_seal_sha256')) and pm.get('mount_seal_sha256') == mm.get('mount_seal_sha256') and pm.get('keys') == mm.get('keys'))


def pred_input_collapse(Rj):
    """F1: the two worlds' ACQUIRE decisions saw the same model input (q ids AND mount seal): equal native predictions are then forced by
    determinism; a state-continuity defect, never a model result. None if not both acquired or the inputs differ."""
    A = {}
    for w in WORLDS:
        acq = [d for d in ((Rj.get('prefix') or {}).get(w) or {}).get('decisions', []) if (d.get('action') or {}).get('op') == 'ACQUIRE'
               and (d.get('dispatch') or {}).get('result') == 'ACQUIRED']
        if not acq: return None
        A[w] = acq[0]
    same = A['X'].get('q_ids') == A['Y'].get('q_ids') and (A['X'].get('mount') or {}).get('mount_seal_sha256') == (A['Y'].get('mount') or {}).get('mount_seal_sha256')
    return {'X': A['X'].get('cell_id'), 'Y': A['Y'].get('cell_id'), 'q_ids_sha256': A['X'].get('q_ids_sha256')} if same else None


def cue_continuity(man, Rj):
    """per world: the cue was in the input of the ACQUIRE (prediction) decision, absent after the PRED seal and at F; live decisions."""
    out = {}
    for w in WORLDS:
        P = (Rj.get('prefix') or {}).get(w) or {}; D = P.get('decisions', []); c = man['cues'][w]
        ai = next((i for i, d in enumerate(D) if (d.get('dispatch') or {}).get('result') == 'ACQUIRED'), None)
        out[w] = {'cue_in_prediction_input': ai is not None and c in (D[ai].get('q') or ''),
                  'cue_after_pred_seal': ai is not None and any(c in (d.get('q') or '') for d in D[ai + 1:]),
                  'cue_at_F': c in ((P.get('fork') or {}).get('q_F') or ''), 'live_decisions': sum(1 for d in D if d.get('cue_live') is True)}
    return out


def avail_summary(Rj):
    """A+ / A- one-step diagnostic per world (reported separately; never a verdict condition, never a two-source signal). 908 r2 (P2-3): the
    label names the exact surface substitution (CONSUMED -> sealed placebo); it is not a measurement of availability as a whole."""
    out = {}
    for w in WORLDS:
        P = (Rj.get('prefix') or {}).get(w) or {}; a = P.get('avail_diag')
        if not a: out[w] = {'label': 'NOT_REACHED'}; continue
        plus = next((d for d in P.get('decisions', []) if d.get('cell_id') == a.get('plus_cell')), {})
        po, mo = (plus.get('action') or {}).get('op'), (a.get('action') or {}).get('op'); pc = a.get('position_controlled') is True
        sub_ = '%s->%s' % (plus.get('avail'), str(a.get('avail') or '').replace('PLACEBO:', ''))     # 908 r2 (P2-3): the exact intervention
        if not pc: lab = 'POSITION_CONFOUNDED_DIAGNOSTIC[%s; A+=%s; A-=%s]' % (sub_, po, mo)
        elif po == mo: lab = 'NO_ONE_STEP_ACTION_CHANGE_UNDER_%s[both %s]' % (sub_.replace('->', '_TO_'), po)
        else: lab = 'ONE_STEP_SURFACE_SUBSTITUTION_EFFECT[%s; A+=%s; A-=%s]' % (sub_, po, mo)
        out[w] = {'plus_cell': a.get('plus_cell'), 'plus_op': po, 'plus_raw': plus.get('raw'), 'minus_op': mo, 'minus_raw': a.get('raw'),
                  'position_controlled': pc, 'placebo': a.get('avail'), 'label': lab}
    return out


def exchangeability(man, Rj):
    """trap 2 / trap 1: at F the two worlds must differ ONLY by the PRED tensors: same q_F (text and ids), same handle order, same slot
    kinds / lengths / source and target positions, OBS tensors bit-equal. Native order differences are never sorted away."""
    F = {w: (Rj['prefix'].get(w) or {}).get('fork') for w in WORLDS}; why = []
    if not all(F.values()): return {'ok': False, 'order_ok': None, 'why': ['FORK_MISSING']}
    a, b = F['X'], F['Y']
    order_ok = a['ws'] == b['ws']
    if not order_ok: why.append('ORDER: X %s Y %s' % (a['ws'], b['ws'])) if sorted(a['ws']) == sorted(b['ws']) else why.append('WS_SET: X %s Y %s' % (a['ws'], b['ws']))
    if (a.get('q_F') != b.get('q_F') or a['q_F_sha256'] != b['q_F_sha256'] or a['q_F_ids_sha256'] != b['q_F_ids_sha256'] or not _id_list(a.get('q_F_ids'))
            or a.get('q_F_ids') != b.get('q_F_ids') or a.get('q_F_tokens') != b.get('q_F_tokens')): why.append('Q_F_DIFFERS')   # r2: text, ids, length
    O = Rj.get('objects') or {}
    def sl(f):
        if not all(f['hmap'].get(h) in O for h in f['ws']): return None
        ents = [O[f['hmap'][h]] for h in f['ws']]; return [(s['m'], s['source_pos0'], s['target_pos0'], e['kind']) for e, s in zip(ents, slots_of(ents)[0])]
    if order_ok and (sl(a) is None or sl(a) != sl(b)): why.append('SLOT_GEOMETRY')
    po, pw = [O.get(F[w]['hmap'].get(HANDLES['obs'])) or {} for w in WORLDS], [O.get(F[w]['hmap'].get(HANDLES['pred'])) or {} for w in WORLDS]
    if not (po[0].get('tensor_seal_sha256') and po[0].get('tensor_seal_sha256') == po[1].get('tensor_seal_sha256') and po[0].get('ids_sha256') == po[1].get('ids_sha256')):
        why.append('OBS_TENSOR_SEAL')
    if not (pw[0].get('n') == pw[1].get('n') and pw[0].get('pos0') == pw[1].get('pos0') == P_PREFIX): why.append('PRED_LENGTH_OR_POS0')
    return {'ok': not why, 'order_ok': order_ok, 'why': why}


def fullref_trigger(man, Rj, roles):
    """pre-registered: FULL_REF for both worlds iff both forks were reached, the worlds are exchangeable, all 14 arms were read and
    the BOTH_NATIVE contradiction / confirmation pattern is NOT present (the reference then separates readout from task failure)."""
    A = Rj.get('arms') or {}
    if roles is None or not exchangeability(man, Rj)['ok']: return []
    if not all((A.get(w, {}).get(a) or {}).get('status') == 'READ' for w in WORLDS for a in ARM_NAMES): return []
    c = {w: classify_action(A[w]['BOTH_NATIVE']['action'], A[w]['BOTH_NATIVE']['mounted_handles']) for w in WORLDS}
    return [] if pattern(c[roles['contra']], c[roles['confirm']]) else list(WORLDS)


def roles_of(S):
    """the contradiction world is the one whose NATIVE prediction differs from the (shared) outcome; assigned from the model's own
    EXPECT values, never from the cue."""
    e = {w: S[w]['expect'] for w in WORLDS}
    if None in e.values() or e['X'] == e['Y']: return None
    c = [w for w in WORLDS if e[w] != TRUTH['A']][0]; return {'contra': c, 'confirm': OTHER_WORLD[c]}


def evaluate_908(man, Rj, technical_ok, isolation_ok=True, technical_why=None):
    """RAW / TECHNICAL / EVALUABLE / SCIENTIFIC, fail-closed, in this precedence (VERDICT_RULES in the manifest). The A+/A- availability
    diagnostic and the cue continuity are reported separately (raw / availability_diagnostic) and never decide the scientific verdict."""
    S = {w: prefix_summary(Rj['prefix'].get(w) or {}) for w in WORLDS}; A = Rj.get('arms') or {}
    probs = integrity_908(man, Rj); roles = roles_of(S); ex = exchangeability(man, Rj) if all(S[w]['fork'] for w in WORLDS) else None
    cls = {w: {a: classify_action(r['action'], r['mounted_handles']) if (r or {}).get('status') == 'READ' else None for a, r in A.get(w, {}).items()} for w in WORLDS}
    ungrounded = sorted('%s/%s' % (w, a) for w in WORLDS for a, c in cls[w].items() if c and c['grounded'] is False)
    ids = lambda w, a: (A.get(w, {}).get(a) or {}).get('gen_ids'); ms = lambda w, a: ((A.get(w, {}).get(a) or {}).get('mount') or {}).get('mount_seal_sha256')
    raw = {'prefix': S, 'roles': roles, 'arm_classes': cls, 'ungrounded_revise': ungrounded, 'exchangeability': ex,
           'cue_continuity': cue_continuity(man, Rj), 'availability': avail_summary(Rj)}
    tech = {'technical_ok': bool(technical_ok), 'isolation_ok': bool(isolation_ok), 'integrity_problems': probs}
    AD = [(Rj['prefix'].get(w) or {}).get('avail_diag') for w in WORLDS]
    gen = sum(int(d.get('n_generated') or 0) for w in WORLDS for d in (Rj['prefix'].get(w) or {}).get('decisions', [])) + \
          sum(int((r or {}).get('n_generated') or 0) for w in WORLDS for r in A.get(w, {}).values()) + sum(int((r or {}).get('n_generated') or 0) for r in (Rj.get('fullref') or {}).values()) + \
          sum(int((a or {}).get('n_generated') or 0) for a in AD)
    nseq = sum(len((Rj['prefix'].get(w) or {}).get('decisions', [])) for w in WORLDS) + sum(1 for w in WORLDS for r in A.get(w, {}).values() if (r or {}).get('status') == 'READ') + \
           sum(1 for r in (Rj.get('fullref') or {}).values() if (r or {}).get('status') == 'READ') + sum(1 for a in AD if a)
    raw['counts'] = {'greedy_sequences': nseq, 'generated_ids': gen, 'avail_diagnostics': sum(1 for a in AD if a)}
    detail = lambda d: '[%s]' % '; '.join('%s: %s' % kv for kv in d.items())
    def out(v, why=None, evaluable=False):
        return {'raw': raw, 'technical': tech, 'evaluable': {'ok': evaluable, 'why': why}, 'scientific': {'verdict': v}, 'verdict': v, 'integrity_problems': probs,
                'availability_diagnostic': raw['availability']}
    fr = Rj.get('first_failed_gate') or ((Rj.get('top') or {}).get('first_failed_gate'))
    tech['technical_why'] = list(technical_why or [])
    if not technical_ok:
        if fr in ('GATE_GPU_PREFLIGHT_906', 'GATE_GPU_PREFLIGHT_908'): return out('GPU_REQUIRED_A100_TECHNICAL_STOP', 'technical')
        return out('TECHNICAL_MISMATCH[first failed gate %s]' % fr if fr or not technical_why else 'TECHNICAL_MISMATCH[%s]' % '; '.join(technical_why[:3]), 'technical')
    if not isolation_ok: return out('TECHNICAL_MISMATCH[DECISION_PATH_ISOLATION]', 'isolation')
    if probs: return out('TECHNICAL_MISMATCH[INTEGRITY %d: %s]' % (len(probs), '; '.join(probs[:3])), 'integrity')
    if nseq > BUDGET['greedy_sequences_max'] or gen > BUDGET['generated_ids_max']: return out('BUDGET_ABORT[sequences %d, ids %d]' % (nseq, gen), 'budget')
    if not address_identifiable(man): return out('NO_IDENTIFIABLE_ADDRESS', 'address')
    if not all(S[w]['acquired'] for w in WORLDS): return out('NATIVE_SELECTION_UNREACHABLE' + detail({w: S[w]['end'] for w in WORLDS if not S[w]['acquired']}), 'no native prediction')
    col = pred_input_collapse(Rj)
    if col: return out('PRED_INPUT_COLLAPSE' + detail(col), 'the two prediction inputs are identical (state-continuity defect)')
    if roles is None: return out('XY_PAIR_NOT_REACHED' + detail({w: 'EXPECT=%s' % S[w]['expect'] for w in WORLDS}), 'no opposite native predictions')
    if not all(S[w]['fork'] for w in WORLDS): return out('FORK_NOT_REACHED' + detail({w: S[w]['end'] for w in WORLDS if not S[w]['fork']}), 'fork')
    if not ex['ok']:
        return out(('ORDER_NOT_EXCHANGEABLE' if ex['order_ok'] is False and any(x.startswith('ORDER') for x in ex['why']) else 'GEOMETRY_NOT_EXCHANGEABLE') + detail({'why': ', '.join(ex['why'])}), 'exchangeability')
    miss = ['%s/%s:%s' % (w, a, (A.get(w, {}).get(a) or {}).get('status')) for w in WORLDS for a in ARM_NAMES if (A.get(w, {}).get(a) or {}).get('status') != 'READ']
    if miss: return out('CONTROL_UNAVAILABLE' + detail({'arms': ', '.join(miss)}), 'controls')
    att = []
    for w in WORLDS:
        if ids(w, 'FILE_SHAM') != ids(w, 'BOTH_NATIVE') or ms(w, 'FILE_SHAM') != ms(w, 'BOTH_NATIVE'): att.append('FILE_SHAM_%s' % w)
    for a in ('O_ONLY', 'NONE'):
        if ms('X', a) == ms('Y', a) and ids('X', a) != ids('Y', a): att.append('%s_X_NE_Y_SAME_MOUNT' % a)
        if ms('X', a) != ms('Y', a): att.append('%s_MOUNT_X_NE_Y' % a)
    if att: return out('PHYSICAL_ATTRIBUTION_FAILURE' + detail({'why': ', '.join(att)}), 'attribution', True)
    C, K = cls[roles['contra']], cls[roles['confirm']]
    if not pattern(C['BOTH_NATIVE'], K['BOTH_NATIVE']) and pattern(C['BOTH_NATIVE'], K['BOTH_NATIVE'], need_grounded=False):
        return out('UNGROUNDED_REVISE' + detail({'BOTH_NATIVE': 'contradiction mark cites an unmounted handle (%s)' % ', '.join(ungrounded)}), 'both ungrounded', True)
    if not pattern(C['BOTH_NATIVE'], K['BOTH_NATIVE']):
        F = Rj.get('fullref') or {}
        if all((F.get(w) or {}).get('status') == 'READ' for w in WORLDS):
            fc = {w: classify_action(F[w]['action'], F[w]['mounted_handles'] + [HANDLES['pred'], HANDLES['obs']]) for w in WORLDS}
            raw['fullref_classes'] = fc
            if pattern(fc[roles['contra']], fc[roles['confirm']]): return out('PHYSICAL_READOUT_FAILURE' + detail({'BOTH': '%s/%s' % (C['BOTH_NATIVE']['class'], K['BOTH_NATIVE']['class']), 'FULL_REF': 'pattern present (diagnostic)'}), 'readout', True)
        if ids('X', 'BOTH_NATIVE') == ids('Y', 'BOTH_NATIVE'): return out('CONTEXT_MISSING' + detail({'BOTH': 'X and Y identical: %s' % C['BOTH_NATIVE']['class']}), 'prediction ignored', True)
        return out('TEST908_NO_GAIN' + detail({'BOTH': 'contra %s / confirm %s' % (C['BOTH_NATIVE']['class'], K['BOTH_NATIVE']['class'])}), 'no pattern', True)
    single = [a for a in ('P_ONLY', 'O_ONLY', 'NONE') if pattern(C[a], K[a], need_grounded=False)]
    if single: return out('TEST908_NO_GAIN' + detail({'SINGLE_SOURCE_EXPLAINS': ', '.join(single)}), 'single source', True)
    cross = cross_follows_prediction(C['PRED_CROSS'], K['PRED_CROSS'])
    if cross == 'UNGROUNDED':
        return out('UNGROUNDED_REVISE' + detail({'PRED_CROSS': 'class flip carried by a REVISE citing an unmounted handle (%s)' % ', '.join(ungrounded)}), 'cross ungrounded', True)
    if cross != 'FOLLOWS':
        return out('PHYSICAL_ATTRIBUTION_FAILURE' + detail({'PRED_CROSS': 'contra %s / confirm %s' % (C['PRED_CROSS']['class'], K['PRED_CROSS']['class'])}), 'cross', True)
    orv = sum(1 for x in (C['ORDER_REV']['class'] == 'CONTRADICTION_MARKED', K['ORDER_REV']['class'] == 'CONFIRMED') if x)
    return out('TEST908_NATIVE_TWO_SOURCE_GAIN[BOTH 2/2; PRED_CROSS 2/2; FILE_SHAM 2/2; single-source 0/3; ORDER_REV %d/2 reported]' % orv, None, True)


VERDICT_RULES_908 = {
    'precedence': ['technical gates (GPU_REQUIRED_A100_TECHNICAL_STOP if the first failed gate is an A100 pre-flight gate, else TECHNICAL_MISMATCH)',
                   'decision-path isolation', 'record integrity (integrity_908: incl. cue lifecycle, availability and A- replay)', 'BUDGET_ABORT',
                   'NO_IDENTIFIABLE_ADDRESS (catalog design)', 'NATIVE_SELECTION_UNREACHABLE (a world without a valid native ACQUIRE)',
                   'PRED_INPUT_COLLAPSE (both ACQUIRE decisions saw identical q ids and mount seal: a state-continuity defect)',
                   'XY_PAIR_NOT_REACHED (native EXPECT values not opposite although the inputs differed)',
                   'FORK_NOT_REACHED (PRED and OBS not both in W by the model\'s own READ_ADD within 6 decisions)',
                   'ORDER_NOT_EXCHANGEABLE / GEOMETRY_NOT_EXCHANGEABLE (q_F, handle order, slots, OBS tensors, PRED length)',
                   'CONTROL_UNAVAILABLE (an arm not read)', 'PHYSICAL_ATTRIBUTION_FAILURE (FILE_SHAM ids or mount differ from BOTH; O_ONLY / NONE '
                   'differ between X and Y under the same mount)', 'no BOTH pattern: PHYSICAL_READOUT_FAILURE if FULL_REF shows it, CONTEXT_MISSING if '
                   'BOTH X and Y are identical, else TEST908_NO_GAIN', 'TEST908_NO_GAIN[SINGLE_SOURCE_EXPLAINS] if P_ONLY / O_ONLY / NONE show the '
                   'pattern (no grounding required)', 'UNGROUNDED_REVISE if BOTH_NATIVE shows the pattern only with a REVISE citing an '
                   'unmounted handle (908; r2 scored this TEST908_NO_GAIN: never positive either way)', 'UNGROUNDED_REVISE if PRED_CROSS flips the classes only through a REVISE that cites an unmounted handle',
                   'PHYSICAL_ATTRIBUTION_FAILURE if PRED_CROSS does not follow the physical prediction', 'TEST908_NATIVE_TWO_SOURCE_GAIN'],
    'pattern': 'contradiction world BOTH_NATIVE = REVISE citing PRED and OBS (every cited handle mounted); confirmation world BOTH_NATIVE = ACCEPT(B)',
    'pred_cross': ('PRED_CROSS follows the physical prediction iff the confirmation world (holding the other PRED) gives a grounded REVISE citing '
                   'PRED and OBS and the contradiction world gives ACCEPT(B); ORDER_REV is reported only (classes, no verdict weight)'),
    'availability_diagnostic': ('reported separately per world: NOT_REACHED / NO_ONE_STEP_ACTION_CHANGE_UNDER_CONSUMED_TO_<placebo>[both op] / '
                                'ONE_STEP_SURFACE_SUBSTITUTION_EFFECT[CONSUMED-><placebo>; A+=op; A-=op] (position-controlled) / '
                                'POSITION_CONFOUNDED_DIAGNOSTIC[...]; only the named surface substitution is measured (not availability as a whole: '
                                'CONSUMED vs AVAILABLE differ in length); never learning, retrieval, a fork or a two-source signal; never a verdict input'),
    'technical': ('required_gate_status(): every REQUIRED_PASS_GATES member present and PASS, no FAIL / malformed gate, no technical blocker, '
                  'gate event chain consistent; the same function in the live verdict, --recompute and authentication'),
    'never': ('a technical PASS as a scientific PASS; arms=0 as success; a correct final answer alone; a one-step arm as a trajectory; a REVISE token '
              'as a closed loop: NATIVE_CLOSED_LOOP_PASS is not a TEST908 label; TEST908 never re-labels TEST907A'),
    'scope': 'cue continuity + event-sourced availability + one-step two-source native readout of a model-selected ordered working set; not '
             'revision writing / re-reading, STOP calibration, multi-episode memory or transfer (TEST909+)'}


# ===================================================================================================== integrity (offline replay of the raw record)
def _keyset(ents_keyed, O):
    return [[h, k, (O.get(k) or {}).get('sha256'), (O.get(k) or {}).get('tensor_seal_sha256')] for h, k in ents_keyed]      # lists: equal after JSON


def _id_list(v):
    return isinstance(v, list) and len(v) > 0 and all(isinstance(i, int) and not isinstance(i, bool) and i >= 0 for i in v)


def q_ids_problems(ids, sha, n, cid, what='Q'):
    """r2 (P2-B): the stored token-id list is the evidence; its SHA-256 and its length are recomputed from it. This is STORED-ID
    SELF-CONSISTENCY, not an independent BPE re-tokenisation (offline recompute has no tokenizer); independent tokenizer evidence is the
    pre-model GATE_TOKENIZER_908 binding of the first decision (manifest q0_ids_sha256) and of q_F (manifest qF_tokens)."""
    if not _id_list(ids): return [cid + ':%s_IDS_MISSING' % what]
    out = []
    if sha != sha_s(json.dumps(ids)): out.append(cid + ':%s_IDS_SHA' % what)
    if n != len(ids): out.append(cid + ':%s_TOKENS' % what)
    return out


def integrity_908(man, Rj):
    """offline replay: parser, working-set transitions, catalog commits, q text (908: cue lifecycle + availability), fork point, object
    provenance (prediction ids = decision ids, empty-prefix parents, event order, observation = template of the environment outcome),
    the A- diagnostic (q, mount, no dispatch, position control), arm mounts from the F snapshot, sham / cross tensor identities,
    environment calls, FULL_REF trigger. Every difference is a problem."""
    bad = []; O = Rj.get('objects') or {}; A = Rj.get('arms') or {}; empty = Rj.get('empty_mount_seal_sha256')
    if not _hex(empty) or empty != ((((Rj.get('gates') or {}).get('GATE_WS_ABI_908') or {}).get('data') or {}).get('empty_mount_seal_sha256')):
        bad.append('EMPTY_MOUNT_SEAL_NOT_RECORDED_BY_THE_ABI_GATE')
    def chk(c, why):
        if not c: bad.append(why)
    def dec_ok(d, cid):
        st, _ = compile_status(d.get('gen_ids'), man['special_ids'])
        chk(st == d.get('compile_status'), cid + ':COMPILE_STATUS')
        if st == 'VALID':
            chk(isinstance(d.get('decoded'), str) and (d.get('raw') or '') == d['decoded'].strip(), cid + ':RAW_NE_DECODED')
            chk(parse_action(d.get('decoded')) == d.get('action'), cid + ':PARSE_REPLAY')
        else: chk((d.get('action') or {}).get('op') == 'INVALID', cid + ':INVALID_NOT_RECORDED')
        chk(d.get('gen_ids_sha256') == sha_s(json.dumps(d.get('gen_ids'))), cid + ':IDS_SHA')
        chk(d.get('q_sha256') == sha_s(d.get('q') or ''), cid + ':Q_SHA')
        mk = (d.get('mount') or {}).get('keys') or []
        sl, tot = slots_of([O[k] for _, k in mk]) if all(k in O for _, k in mk) else (None, None)
        chk(sl is not None and d['mount'].get('mount_tokens') == tot and d['mount'].get('slots') == sl, cid + ':MOUNT_GEOMETRY')
        chk(d['mount'].get('trace') == _keyset(mk, O), cid + ':MOUNT_TRACE')
        g_ = d.get('gen_ids') or []; chk(d.get('n_generated') == len(g_) + (1 if len(g_) < COMPILE_PROBE else 0), cid + ':GEN_COUNT')
        bad.extend(q_ids_problems(d.get('q_ids'), d.get('q_ids_sha256'), d.get('q_tokens'), cid))
        mt = d['mount'].get('mount_tokens')
        chk(isinstance(mt, int) and isinstance(d.get('q_tokens'), int) and d['mount'].get('first_generated_position') == mt + d['q_tokens'],
            cid + ':FIRST_GENERATED_POSITION')
    plc = (man.get('placebo') or {}).get('value')
    for w in WORLDS:
        P = Rj['prefix'].get(w) or {}; D = P.get('decisions', []); ws = (); cat = [man['catalog_entries']['decoy']]; hmap = {HANDLES['decoy']: 'ARCHIVE/DECOY'}
        acq = 0; end = None; fork = None; envc = 0; kappa = True; alpha = AVAIL_STATES[0]; first_post = None
        chk(len(D) <= MAX_PREFIX_CALLS, w + ':PREFIX_TOO_LONG')
        for i, d in enumerate(D):
            cid = d.get('cell_id', '%s/%d' % (w, i)); dec_ok(d, cid)
            chk(d.get('q') == build_q(man['task_text'], man['cues'][w] if kappa else None, alpha, cat, ws), cid + ':Q_REPLAY')
            chk(d.get('cue_live') is kappa and d.get('avail') == alpha, cid + ':CUE_AVAIL_RECORD')
            q_ = d.get('q') or ''
            chk((man['cues'][w] in q_) == kappa, cid + (':CUE_MISSING_BEFORE_PRED_SEAL' if kappa else ':CUE_LEAK_AFTER_PRED_SEAL'))
            chk(man['cues'][OTHER_WORLD[w]] not in q_, cid + ':OTHER_WORLD_CUE')
            if i == 0: chk(d.get('q_ids_sha256') == (man.get('q0_ids_sha256') or {}).get(w), cid + ':Q0_IDS_NE_PRE_MODEL_TOKENIZER')
            pre = ((man.get('q_pre_ids_sha256') or {}).get(w) or {}).get(','.join(ws))
            if kappa and alpha == AVAIL_STATES[0] and len(cat) == 1:
                chk(pre is not None and d.get('q_ids_sha256') == pre, cid + ':Q_PRE_IDS_NE_PRE_MODEL_TOKENIZER')
            if alpha == AVAIL_STATES[1] and first_post is None: first_post = (i, copy.deepcopy(cat), tuple(ws))
            chk(tuple(d.get('ws_before') or ()) == ws and d['mount']['keys'] == [[h, hmap.get(h)] for h in ws], cid + ':WS_BEFORE')
            act = d.get('action') or {}; op = act.get('op'); res = (d.get('dispatch') or {}).get('result')
            if end is not None: bad.append(cid + ':DECISION_AFTER_END'); break
            if op == 'INVALID': end = 'INVALID_NATIVE_ACTION:' + str(act.get('why')); chk(res == 'INVALID', cid + ':DISPATCH'); continue
            if op in ('READ_ADD', 'READ_DEL', 'READ_CLEAR'):
                ws2, r = ws_apply(ws, act, {e['handle'] for e in cat}); chk(r == res and list(ws2) == d['dispatch'].get('ws_after'), cid + ':WS_REPLAY')
                if r.endswith('_INVALID'): end = r; continue
                ws = ws2
                if fork_condition(ws): end = 'FORK'; fork = i
                continue
            if op == 'ACQUIRE':
                if acq: chk(res == 'OUT_OF_SCOPE_SECOND_ACQUIRE', cid + ':SECOND_ACQUIRE'); end = 'OUT_OF_SCOPE_SECOND_ACQUIRE'; continue
                acq += 1; dp = d.get('dispatch') or {}; kp, ko = dp.get('pred_key'), dp.get('obs_key'); op_, oo = O.get(kp) or {}, O.get(ko) or {}
                chk(res == 'ACQUIRED' and kp == '%s/PRED' % w and ko == '%s/OBS' % w, cid + ':ACQUIRE_DISPATCH')
                chk(op_.get('ids_sha256') == d.get('gen_ids_sha256') and op_.get('n') == len(d.get('gen_ids') or []), cid + ':PRED_IDS_NE_DECISION_IDS')
                chk(op_.get('expect') == act.get('expect'), cid + ':PRED_EXPECT_NE_DECISION')
                chk(op_.get('pos0') == P_PREFIX and op_.get('parent_mount_seal_sha256') == empty and op_.get('parents') == [], cid + ':PRED_PARENT_NOT_EMPTY_PREFIX')
                chk(oo.get('pos0') == P_PREFIX and oo.get('parent_mount_seal_sha256') == empty and oo.get('parents') == [], cid + ':OBS_PARENT_NOT_EMPTY_PREFIX')
                o = dp.get('outcome'); chk(o == man['truth']['A'], cid + ':OUTCOME_NE_ENVIRONMENT_TRUTH')
                chk(oo.get('ids_sha256') == sha_s(json.dumps(man['obs_ids'].get(str(o)))) and oo.get('n') == len(man['obs_ids'].get(str(o)) or []), cid + ':OBS_NOT_THE_TEMPLATE')
                ev_ = dp.get('events') or {}
                chk(all(isinstance(ev_.get(k), int) for k in ('pred_sealed', 'env_executed', 'obs_sealed', 'catalog_commit')) and
                    ev_['pred_sealed'] < ev_['env_executed'] < ev_['obs_sealed'] < ev_['catalog_commit'], cid + ':EVENT_ORDER')
                nxt = D[i + 1] if i + 1 < len(D) else None
                if nxt is not None: chk(isinstance(nxt.get('event_index'), int) and nxt['event_index'] > ev_.get('catalog_commit', 10**9), cid + ':NEXT_DECISION_BEFORE_COMMIT')
                envc += 1; hmap.update({HANDLES['pred']: kp, HANDLES['obs']: ko}); kappa = False; alpha = AVAIL_STATES[1]
                cat = cat + [man['catalog_entries']['pred'], man['catalog_entries']['obs']]; chk(list(ws) == dp.get('ws_after'), cid + ':ACQUIRE_CHANGED_WS')
                continue
            end = ('MODEL_%s_BEFORE_FORK' % op) if op in ('ACCEPT', 'STOP') else 'OUT_OF_SCOPE_%s_BEFORE_FORK' % op; chk(res == end, cid + ':DISPATCH')
        if end is None: end = 'MAX_PREFIX_CALLS' if len(D) == MAX_PREFIX_CALLS else 'INCOMPLETE'
        chk(end == P.get('end'), w + ':END_REPLAY %s != %s' % (end, P.get('end')))
        chk(envc == P.get('env_calls'), w + ':ENV_CALLS')
        a = P.get('avail_diag')
        if first_post is None: chk(not a, w + ':AVAIL_DIAG_WITHOUT_POST_COMMIT_DECISION')
        else:
            j, cj, wj = first_post; dj = D[j]; chk(bool(a), w + ':AVAIL_DIAG_MISSING')
            if a:
                acid = str(a.get('cell_id')); dec_ok(a, acid)
                chk(a.get('plus_cell') == dj.get('cell_id') and a.get('phase') == 'AVAIL_DIAGNOSTIC', acid + ':PLUS_CELL')
                chk(plc in PLACEBO_CANDIDATES and a.get('avail') == 'PLACEBO:%s' % plc and a.get('q') == build_q(man['task_text'], None, plc, cj, wj), acid + ':Q_MINUS_REPLAY')
                chk(a.get('cue_live') is False and man['cues'][w] not in (a.get('q') or ''), acid + ':CUE_IN_A_MINUS')
                chk(a['mount'].get('keys') == dj['mount'].get('keys') and a['mount'].get('mount_seal_sha256') == dj['mount'].get('mount_seal_sha256'), acid + ':MOUNT_NE_A_PLUS')
                chk(a.get('env_calls_in_branch') == 0 and a.get('dispatched') is False and a.get('diagnostic_only') is True and 'dispatch' not in a, acid + ':DIAGNOSTIC_DISPATCHED')
                chk(a.get('branch_id') != dj.get('branch_id'), acid + ':SHARED_BRANCH')
                pc = position_controlled(dj, a); chk(a.get('position_controlled') is pc, acid + ':POSITION_CONTROL_FLAG')
                if pc: chk((man.get('placebo') or {}).get('position_controlled_preseal') is True, acid + ':POSITION_CONTROL_WITHOUT_PRESEAL')
        f = P.get('fork')
        chk((fork is None) == (f is None), w + ':FORK_REPLAY')
        if f is not None and fork is not None:
            chk(f.get('step') == fork and f.get('ws') == list(ws) and f.get('hmap') == hmap and f.get('catalog') == cat, w + ':FORK_SNAPSHOT')
            chk(not kappa and alpha == AVAIL_STATES[1], w + ':FORK_BEFORE_COMMIT')
            chk(f.get('q_F') == build_q(man['task_text'], None, AVAIL_STATES[1], cat, ws) and f.get('q_F_sha256') == sha_s(f.get('q_F') or ''), w + ':Q_F_REPLAY')
            chk(all(c not in (f.get('q_F') or '') for c in man['cues'].values()), w + ':CUE_AT_F')
            bad.extend(q_ids_problems(f.get('q_F_ids'), f.get('q_F_ids_sha256'), f.get('q_F_tokens'), w + ':FORK', 'Q_F'))
            qft = (man.get('qF_tokens') or {}).get(','.join(f.get('ws') or []))
            chk(qft is not None and f.get('q_F_tokens') == qft, w + ':Q_F_TOKENS_NE_PRE_MODEL_TOKENIZER')
            chk([D[j]['action'].get('handle') for j in f.get('read_provenance', [])] and all(D[j]['action'].get('op') == 'READ_ADD' for j in f.get('read_provenance', []))
                and {D[j]['action']['handle'] for j in f.get('read_provenance', [])} >= {HANDLES['pred'], HANDLES['obs']}, w + ':FORK_READ_PROVENANCE')
    S = {w: prefix_summary(Rj['prefix'].get(w) or {}) for w in WORLDS}
    run_arms_expected = roles_of(S) is not None and all(S[w]['fork'] for w in WORLDS)
    for w in WORLDS:
        aw = A.get(w) or {}
        if not run_arms_expected: chk(not aw, w + ':ARMS_WITHOUT_PRECONDITION'); continue
        f = Rj['prefix'][w]['fork']; fo = Rj['prefix'][OTHER_WORLD[w]]['fork']; sham = (Rj.get('sham_map') or {}).get(w) or {}
        bids = set()
        for a in ARM_NAMES:
            r = aw.get(a); cid = '%s/ARM/%s' % (w, a)
            if r is None: bad.append(cid + ':MISSING'); continue
            chk(r.get('one_step') is True and r.get('arm') == a, cid + ':ARM_LABEL')
            chk(r.get('branch_id') not in bids, cid + ':BRANCH_ID_SHARED'); bids.add(r.get('branch_id'))
            chk(r.get('env_calls_in_branch') == 0, cid + ':ENV_IN_BRANCH')
            if a == 'PRED_CROSS':
                pm, qm = O.get(f['hmap'][HANDLES['pred']]) or {}, O.get(fo['hmap'][HANDLES['pred']]) or {}
                if not (pm.get('n') == qm.get('n') and pm.get('pos0') == qm.get('pos0')):
                    chk(r.get('status') == 'NOT_RUN_GEOMETRY_NOT_EXCHANGEABLE', cid + ':CROSS_GEOMETRY'); continue
            want = arm_keys(a, tuple(f['ws']), f['hmap'], fo['hmap'], sham)
            chk(r.get('status') == 'READ', cid + ':NOT_READ')
            if r.get('status') != 'READ': continue
            dec_ok(r, cid); chk(r.get('q') == f['q_F'], cid + ':Q_NE_Q_F')
            chk(r.get('q_ids') == f.get('q_F_ids') and r.get('q_ids_sha256') == f.get('q_F_ids_sha256') and r.get('q_tokens') == f.get('q_F_tokens'),
                cid + ':Q_IDS_NE_Q_F_IDS')
            chk(r['mount']['keys'] == [list(x) for x in want], cid + ':ARM_MOUNT_RULE')
            chk(r.get('mounted_handles') == [h for h, _ in want], cid + ':MOUNTED_HANDLES')
            if a == 'FILE_SHAM':
                for h, k in want:
                    src = O.get(f['hmap'][h]) or {}; cp_ = O.get(k) or {}
                    chk(cp_.get('tensor_seal_sha256') == src.get('tensor_seal_sha256') and cp_.get('sha256') != src.get('sha256') and k != f['hmap'][h], cid + ':SHAM_COPY_' + h)
            if a == 'PRED_CROSS':
                k = dict(want)[HANDLES['pred']]; chk(k == fo['hmap'][HANDLES['pred']] and (O.get(k) or {}).get('tensor_seal_sha256') != (O.get(f['hmap'][HANDLES['pred']]) or {}).get('tensor_seal_sha256'),
                                                   cid + ':CROSS_TENSOR_NOT_SWAPPED')
    trig = fullref_trigger(man, Rj, roles_of(S)) if run_arms_expected else []
    FR = Rj.get('fullref') or {}
    chk(sorted(FR) == sorted(trig), 'FULLREF_TRIGGER_REPLAY %s != %s' % (sorted(FR), trig))
    for w, r in FR.items():
        f = Rj['prefix'][w]['fork']; k = '%s/FULLREF' % w; o = O.get(k) or {}
        acq = [d for d in Rj['prefix'][w]['decisions'] if (d.get('dispatch') or {}).get('result') == 'ACQUIRED']
        ids = fullref_ids(f['ws'], acq[0]['gen_ids'] if acq else [], man['obs_ids'][str(man['truth']['A'])])
        chk(o.get('ids_sha256') == sha_s(json.dumps(ids)) and o.get('pos0') == P_PREFIX and o.get('parent_mount_seal_sha256') == empty, w + ':FULLREF_OBJECT')
        if r.get('status') == 'READ':
            dec_ok(r, w + '/FULLREF'); chk(r.get('q') == f['q_F'] and r['mount']['keys'] == [['FULLREF', k]], w + ':FULLREF_MOUNT')
            chk(r.get('q_ids') == f.get('q_F_ids'), w + ':FULLREF_Q_IDS_NE_Q_F_IDS')
    for k, o in O.items():
        chk(_hex(o.get('sha256')) and _hex(o.get('tensor_seal_sha256')), 'OBJECT_SEALS:' + k)
    created = sum(int(o.get('bytes') or 0) for k, o in O.items() if o.get('created'))
    chk(created <= BUDGET['created_object_bytes_max'], 'CREATED_BYTES %d' % created)
    return bad


BRANCH_EVENT_KINDS = ('DECISION_BEGIN', 'PRED_SEAL_BEGIN', 'PRED_SEALED', 'ENV_EXECUTED', 'OBS_SEALED', 'CATALOG_COMMIT', 'FORK_SNAPSHOT')   # ev908 kinds
BRANCH_EVENT_FIELDS = ('cell_id', 'key', 'sha256', 'action', 'outcome', 'handles')       # the ev908 fields copied into a branch list


def event_chain_problems(Rj, events, surface=True):
    """908 r2 (P2-2): pure offline replay of the append-only event log against the record (no model / torch / Drive). Schema (903 ev +
    ev908): global events {seq, kind, branch?, ...}; a branch list holds, for every ev908 event of that branch, {index = global seq, kind,
    and the BRANCH_EVENT_FIELDS present}; the global DECISION event (decide) is global-only; OBJECT events carry entry. Checks: seq = 0..N-1;
    every branch list = inherited prefix of its world's NATIVE list (+ inherited_events) followed by the exact projection of the global ev908
    events of that branch (same seq, kind, fields); every decision record has its DECISION_BEGIN and DECISION (ids, mount, op) events; every
    native ACQUIRE has DECISION -> PRED_SEAL_BEGIN -> OBJECT(PRED) -> PRED_SEALED -> ENV_EXECUTED -> OBJECT(OBS) -> OBS_SEALED -> CATALOG_COMMIT
    with the recorded keys, file SHAs, action, outcome and handles; ENV_EXECUTED only in NATIVE branches and as many as env calls; with
    surface=True the recorded cue_live / avail of every native decision and of the A- diagnostic equal cue_live() / availability() replayed
    from the branch events before it, and A- / arm / FULL_REF branches hold one own DECISION_BEGIN only. Returns problems (empty = coherent)."""
    if not isinstance(events, list) or not events: return ['EVENTS_MISSING']
    if not all(isinstance(e, dict) for e in events): return ['EVENTS_MALFORMED']
    bad = []
    if [e.get('seq') for e in events] != list(range(len(events))): bad.append('EVENT_SEQ_NOT_0_TO_N-1')
    G = {}
    for e in events:
        if isinstance(e.get('seq'), int): G.setdefault(e['seq'], e)
    B = Rj.get('branches')
    if not isinstance(B, dict): return bad + ['BRANCHES_MISSING']
    gb = {}
    for e in events:
        if e.get('branch') is not None and e.get('kind') in BRANCH_EVENT_KINDS: gb.setdefault(e['branch'], []).append(e)
    for bid in sorted(set(gb) - set(B)): bad.append('EVENTS_OF_UNRECORDED_BRANCH:%s' % bid)
    own_of = {}
    for bid, rec in sorted(B.items()):
        evs = rec.get('events') if isinstance(rec, dict) else None
        if not isinstance(evs, list) or not all(isinstance(e, dict) for e in evs): bad.append('BRANCH_EVENTS_MISSING:' + bid); continue
        inh = rec.get('inherited_events')
        if inh is None:
            if surface: bad.append('BRANCH_INHERITED_MISSING:' + bid); continue
            inh = 0
        if not isinstance(inh, int) or isinstance(inh, bool) or inh < 0 or inh > len(evs): bad.append('BRANCH_INHERITED_RANGE:' + bid); continue
        parent = '%s/NATIVE' % str(bid).split('/')[0]
        if bid == parent:
            if inh != 0: bad.append('NATIVE_BRANCH_INHERITS:' + bid)
        else:
            pev = (B.get(parent) or {}).get('events') if isinstance(B.get(parent), dict) else None
            if not isinstance(pev, list) or evs[:inh] != pev[:inh]: bad.append('INHERITED_NE_PARENT_PREFIX:' + bid)
        own = evs[inh:]; own_of[bid] = own; glob = gb.get(bid, [])
        if [e.get('index') for e in own] != [g.get('seq') for g in glob]: bad.append('BRANCH_PROJECTION_NE_GLOBAL:' + bid); continue
        for e, g in zip(own, glob):
            if e.get('kind') != g.get('kind') or any((f in e) != (f in g) or (f in e and e[f] != g[f]) for f in BRANCH_EVENT_FIELDS):
                bad.append('BRANCH_EVENT_FIELDS_NE_GLOBAL:%s:%s' % (bid, e.get('index')))
    def dec(d, bid):
        cid = d.get('cell_id'); i = d.get('event_index'); g = G.get(i) if isinstance(i, int) else None
        if not g or g.get('kind') != 'DECISION_BEGIN' or g.get('cell_id') != cid or g.get('branch') != bid: bad.append('DECISION_BEGIN_EVENT:%s' % cid); return None
        dd = [e for e in events if e.get('kind') == 'DECISION' and e.get('cell_id') == cid and e.get('branch') == bid]
        if (len(dd) != 1 or not isinstance(dd[0].get('seq'), int) or dd[0]['seq'] <= i or dd[0].get('ids_sha256') != d.get('gen_ids_sha256')
                or dd[0].get('mount') != (d.get('mount') or {}).get('mount_seal_sha256') or dd[0].get('op') != (d.get('action') or {}).get('op')):
            bad.append('DECISION_EVENT:%s' % cid); return None
        return dd[0]['seq']
    P = Rj.get('prefix') or {}; O = Rj.get('objects') or {}; envs = 0
    objs = [e for e in events if e.get('kind') == 'OBJECT' and isinstance(e.get('entry'), dict)]
    want = (('pred_begin', 'PRED_SEAL_BEGIN'), ('pred_sealed', 'PRED_SEALED'), ('env_executed', 'ENV_EXECUTED'), ('obs_sealed', 'OBS_SEALED'),
            ('catalog_commit', 'CATALOG_COMMIT'))
    for w in WORLDS:
        Pw = P.get(w) or {}; bid = '%s/NATIVE' % w; bev = ((B.get(bid) or {}).get('events') or []) if isinstance(B.get(bid), dict) else []
        for d in Pw.get('decisions', []):
            cid = d.get('cell_id')
            if d.get('branch_id') != bid: bad.append('DECISION_BRANCH:%s' % cid)
            ds = dec(d, bid)
            if surface:
                pre = [e for e in bev if isinstance(e.get('index'), int) and isinstance(d.get('event_index'), int) and e['index'] < d['event_index']]
                if d.get('cue_live') is not cue_live(pre) or d.get('avail') != availability(pre): bad.append('CUE_AVAIL_NE_EVENT_REPLAY:%s' % cid)
            dp = d.get('dispatch') or {}
            if dp.get('result') != 'ACQUIRED': continue
            ev_ = dp.get('events') or {}; gs = {k: G.get(ev_.get(k)) if isinstance(ev_.get(k), int) else None for k, _ in want}
            if any(gs[k] is None or gs[k].get('kind') != kind or gs[k].get('branch') != bid for k, kind in want): bad.append('ACQUIRE_EVENT_KINDS:%s' % cid); continue
            idx = [ev_[k] for k, _ in want]
            if idx != sorted(set(idx)) or ds is None or not ds < idx[0]: bad.append('ACQUIRE_EVENT_ORDER:%s' % cid)
            if gs['pred_begin'].get('cell_id') != cid: bad.append('PRED_SEAL_BEGIN_CELL:%s' % cid)
            po, oo = O.get(dp.get('pred_key')) or {}, O.get(dp.get('obs_key')) or {}
            if gs['pred_sealed'].get('key') != dp.get('pred_key') or gs['pred_sealed'].get('sha256') != po.get('sha256'): bad.append('PRED_SEALED_EVENT:%s' % cid)
            if gs['env_executed'].get('action') != ENV_ACTIONS[0] or gs['env_executed'].get('outcome') != dp.get('outcome'): bad.append('ENV_EXECUTED_EVENT:%s' % cid)
            if gs['obs_sealed'].get('key') != dp.get('obs_key') or gs['obs_sealed'].get('sha256') != oo.get('sha256'): bad.append('OBS_SEALED_EVENT:%s' % cid)
            if gs['catalog_commit'].get('handles') != [HANDLES['pred'], HANDLES['obs']]: bad.append('CATALOG_COMMIT_EVENT:%s' % cid)
            for key, lo, hi in ((dp.get('pred_key'), idx[0], idx[1]), (dp.get('obs_key'), idx[2], idx[3])):
                m_ = [e for e in objs if e['entry'].get('key') == key]
                if len(m_) != 1 or not lo < m_[0].get('seq', -1) < hi or m_[0]['entry'].get('sha256') != (O.get(key) or {}).get('sha256'): bad.append('OBJECT_EVENT:%s' % key)
        f = Pw.get('fork')
        if f:
            g = G.get(f.get('event_index')) if isinstance(f.get('event_index'), int) else None
            if not g or g.get('kind') != 'FORK_SNAPSHOT' or g.get('branch') != bid or g.get('handles') != f.get('ws'): bad.append('FORK_SNAPSHOT_EVENT:%s' % w)
        envs += int(Pw.get('env_calls') or 0)
        a = Pw.get('avail_diag')
        if a:
            abid = a.get('branch_id'); dec(a, abid); rec = B.get(abid) if isinstance(B.get(abid), dict) else {}
            inh = rec.get('inherited_events'); evs = rec.get('events') if isinstance(rec.get('events'), list) else []
            inherited = evs[:inh] if isinstance(inh, int) else []
            plus = next((d for d in Pw.get('decisions', []) if d.get('cell_id') == a.get('plus_cell')), {})
            if plus.get('event_index') not in [e.get('index') for e in inherited]: bad.append('A_MINUS_NOT_FORKED_AFTER_A_PLUS:%s' % w)
            if surface and (a.get('cue_live') is not cue_live(inherited) or availability(inherited) != AVAIL_STATES[1]): bad.append('A_MINUS_INHERITED_REPLAY:%s' % w)
            if [e.get('kind') for e in own_of.get(abid, [{}])] != ['DECISION_BEGIN']: bad.append('A_MINUS_BRANCH_EVENTS:%s' % w)
    for src in [r for aw in (Rj.get('arms') or {}).values() for r in aw.values()] + list((Rj.get('fullref') or {}).values()):
        if (src or {}).get('status') != 'READ': continue
        dec(src, src.get('branch_id'))
        if [e.get('kind') for e in own_of.get(src.get('branch_id'), [{}])] != ['DECISION_BEGIN']: bad.append('BRANCH_OWN_EVENTS:%s' % src.get('branch_id'))
    envg = [e for e in events if e.get('kind') == 'ENV_EXECUTED']
    if len(envg) != envs or any(not str(e.get('branch', '')).endswith('/NATIVE') for e in envg): bad.append('ENV_EXECUTED_COUNT_OR_BRANCH')
    return bad


HEX64 = re.compile(r'^[0-9a-f]{64}$')
def _hex(v): return isinstance(v, str) and bool(HEX64.match(v))


def fullref_ids(ws, pred_ids, obs_ids):
    """FULL_REF content: the PRED ids and the OBS ids in their native W relative order, one continuous sequence."""
    return [i for h in ws if h in (HANDLES['pred'], HANDLES['obs']) for i in (pred_ids if h == HANDLES['pred'] else obs_ids)]


def generation_seal(Rj):
    rows = [(d.get('cell_id'), d.get('gen_ids'), d.get('raw')) for w in WORLDS for d in (Rj.get('prefix', {}).get(w) or {}).get('decisions', [])]
    rows += [(r.get('cell_id'), r.get('gen_ids'), r.get('raw')) for w in WORLDS for a, r in sorted(((Rj.get('arms') or {}).get(w) or {}).items())]
    rows += [(r.get('cell_id'), r.get('gen_ids'), r.get('raw')) for w, r in sorted((Rj.get('fullref') or {}).items())]
    rows += [('Q_IDS', d.get('cell_id'), d.get('q_ids')) for w in WORLDS for d in (Rj.get('prefix', {}).get(w) or {}).get('decisions', [])]
    rows += [('Q_IDS', r.get('cell_id'), r.get('q_ids')) for w in WORLDS for a, r in sorted(((Rj.get('arms') or {}).get(w) or {}).items())]
    rows += [('Q_IDS', r.get('cell_id'), r.get('q_ids')) for w, r in sorted((Rj.get('fullref') or {}).items())]
    rows += [('Q_F_IDS', w, ((Rj.get('prefix', {}).get(w) or {}).get('fork') or {}).get('q_F_ids')) for w in WORLDS]
    AD = [((Rj.get('prefix', {}).get(w) or {}).get('avail_diag') or {}) for w in WORLDS]          # 908: the A- diagnostics are sealed too
    rows += [('AVAIL_MINUS', a.get('cell_id'), a.get('gen_ids'), a.get('raw'), a.get('q_ids')) for a in AD if a]
    return jsha(rows)


def isolation_from_gates(gates):
    """both isolation checks as RECORDED by their gates (906 engine gate: compile / forge / read path; 908 ABI gate: decision path).
    The live verdict and --recompute use the same rule."""
    g = lambda n: bool(((((gates or {}).get(n) or {}).get('data') or {}).get('isolation') or {}).get('ok'))
    return g('GATE_ENGINE_906') and g('GATE_WS_ABI_908')


def verify_run_record(Rj, man_bytes, ev):
    out = []
    if Rj.get('status') == 'COMPLETE':
        for f in ('manifest_sha256', 'generation_sealed_sha256'):
            if not Rj.get(f): out.append(f.upper() + '_MISSING')
    if Rj.get('manifest_sha256') and Rj['manifest_sha256'] != sha_b(man_bytes): out.append('MANIFEST_SHA_MISMATCH')
    if Rj.get('generation_sealed_sha256') and Rj['generation_sealed_sha256'] != generation_seal(Rj): out.append('GENERATION_SEAL_MISMATCH')
    st = Rj.get('evaluation') or {}
    if st:
        if st.get('verdict') != ev['verdict']: out.append('STORED_VERDICT_DIFFERS')
        if canon((st.get('raw') or {}).get('arm_classes')) != canon(ev['raw'].get('arm_classes')): out.append('STORED_ARM_CLASSES_DIFFER')
        if canon((st.get('raw') or {}).get('prefix')) != canon(ev['raw'].get('prefix')): out.append('STORED_PREFIX_SUMMARY_DIFFERS')
        if canon(st.get('availability_diagnostic')) != canon(ev.get('availability_diagnostic')): out.append('STORED_AVAILABILITY_DIAGNOSTIC_DIFFERS')
        if canon((st.get('raw') or {}).get('cue_continuity')) != canon(ev['raw'].get('cue_continuity')): out.append('STORED_CUE_CONTINUITY_DIFFERS')
    return out


def report_lines(ev):
    v = ev['verdict']; raw = ev['raw']; L = ['TEST908 VERDICT: %s (cue continuity + availability + one-step two-source native readout only; %s)' % (v, LABEL)]
    for w in WORLDS:
        s = raw['prefix'][w]; L.append('PREFIX %s: calls %s | ACQUIRE %s EXPECT=%s | fork %s | end %s' % (w, s['calls'], s['acquired'], s['expect'], s['fork'], s['end']))
    for w in WORLDS:
        c = (raw.get('cue_continuity') or {}).get(w) or {}
        L.append('CUE %s: in prediction input %s | after PRED seal %s | at F %s | live decisions %s' % (w, c.get('cue_in_prediction_input'),
                 c.get('cue_after_pred_seal'), c.get('cue_at_F'), c.get('live_decisions')))
    for w in WORLDS:
        a = (raw.get('availability') or {}).get(w) or {}
        L.append('AVAIL %s (diagnostic, not a verdict): %s' % (w, a.get('label')))
    L.append('ROLES (from native EXPECT): %s | EXCHANGEABLE: %s' % (raw['roles'], raw['exchangeability']))
    for w in WORLDS:
        c = raw['arm_classes'].get(w) or {}
        if c: L.append('ARMS %s: ' % w + ' | '.join('%s=%s%s' % (a, (c.get(a) or {}).get('class'), '' if (c.get(a) or {}).get('grounded') is not False else '(UNGROUNDED_REVISE)') for a in ARM_NAMES))
    if raw.get('fullref_classes'): L.append('FULL_REF (diagnostic): %s' % {w: c['class'] for w, c in raw['fullref_classes'].items()})
    L.append('counts: %s | technical %s | evaluable %s' % (raw['counts'], ev['technical']['technical_ok'], ev['evaluable']))
    return L


# ===================================================================================================== run infrastructure (TEST906 r2 copies + 908)
X = types.SimpleNamespace(); M3 = M4 = m3 = M6 = None; RUN_ID = ROOT = LOG = OUT = EVENTS = None; R = None; DRIVE_DIR = None; T0 = time.perf_counter()


def config(argv):
    import argparse
    ap = argparse.ArgumentParser(add_help=False); colab = Path('/content').exists()
    d = {'out_root': '/content' if colab else '/tmp', 'src_dir': '', 'repo_dir': '/content/titan-cognitive-core-v3' if colab else '',
         'archive_dir': DEFAULT_ARCHIVE_903, 'zip': '', 'receipt': '', 'ref906_dir': DEFAULT_REF906_DIR, 'ref907a_dir': DEFAULT_REF907A_DIR, 'recompute': '', 'recompute_mode': 'verified',
         'drive': 'required' if colab else 'auto'}
    for k, v in d.items(): ap.add_argument('--' + k.replace('_', '-'), default=os.environ.get('T908_' + k.upper(), v))
    a, _ = ap.parse_known_args(list(argv)); return {k: getattr(a, k) for k in d}


def fetch_source(cfg, work, pin):
    cands = [Path(cfg[k]) / pin['file'] for k in ('src_dir', 'repo_dir') if cfg.get(k)]
    for p in cands:
        if p.is_file() and blob_b(p.read_bytes()) == pin['git_blob']: b = p.read_bytes(); break
    else:
        rd = Path(cfg['repo_dir']) if cfg.get('repo_dir') and Path(cfg['repo_dir']).exists() else Path(work).parent / 'TEST908_repo_blobs'
        env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
        if not (rd / '.git').exists() and not (rd / 'HEAD').exists():
            subprocess.run(['git', 'clone', '-q', '--filter=blob:none', '--no-checkout', SRC_URL, str(rd)], check=True, capture_output=True, timeout=900, env=env)
        b = subprocess.run(['git', '-C', str(rd), 'cat-file', 'blob', pin['git_blob']], check=True, capture_output=True, timeout=300, env=env).stdout
    if blob_b(b) != pin['git_blob'] or sha_b(b) != pin['sha256']: raise Stop908('SOURCE_IDENTITY ' + pin['file'])
    p = Path(work) / pin['file']; p.write_bytes(b); return p


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def _norm_code(co):
    consts = tuple(_norm_code(c) if isinstance(c, types.CodeType) else c for c in co.co_consts)
    return co.replace(co_filename='', co_consts=consts, co_firstlineno=1, co_linetable=b'', co_exceptiontable=co.co_exceptiontable)


def code_digest(funcs):
    return sha_b(b''.join(marshal.dumps(_norm_code(f.__code__)) for f in funcs))


def _top_functions(b):
    import ast
    return [n.name for n in ast.parse(b).body if isinstance(n, ast.FunctionDef)]


REPO_908 = '/content/809.py'


def _execution_mode(own_file, g):
    f = str(own_file or '')
    if 'ipykernel' in f or f.startswith('<ipython-input'): return 'NOTEBOOK_CELL'
    if g.get('__file__'): return 'SCRIPT_OR_%RUN'
    if f in ('<string>', '<stdin>', ''): return 'EXEC_STRING'
    return 'EXEC_COMPILED_WITH_FILENAME'


def git_provenance(path):
    """HEAD commit / committed blob of the executed file when it lives in a git checkout (diagnostic: published vs executed)."""
    try:
        d = str(Path(path).parent); env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
        head = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True, timeout=30, env=env).stdout.strip()
        tree = subprocess.run(['git', '-C', d, 'ls-tree', 'HEAD', '--', Path(path).name], capture_output=True, text=True, timeout=30, env=env).stdout.split()
        return {'head': head or None, 'committed_blob': tree[2] if len(tree) >= 3 else None}
    except Exception as e:
        return {'error': '%s: %s' % (type(e).__name__, e)}


def _cell_text(own_file):
    """the text IPython compiled for the running notebook cell (IPython registers every cell's text in linecache). Runs before the
    namespace clean-up, so it calls builtins through the builtins module only."""
    import linecache, builtins as B
    for cache in (linecache.cache, B.getattr(linecache, '_ipython_cache', None) or {}):
        e = cache.get(own_file)
        if B.isinstance(e, B.tuple) and B.len(e) >= 3 and B.isinstance(e[2], B.list) and e[2]: return ''.join(e[2])
    return None


def _canon_lines(text):
    """the ONLY normalisation before the notebook comparison: line endings, and blank lines at the very start / end of the cell."""
    lines = text.splitlines()
    while lines and not lines[0].strip(): lines.pop(0)
    while lines and not lines[-1].strip(): lines.pop()
    return lines


def _ipython_rewrites(ip, text, filename):
    """None when IPython compiled this text as written: no inherited `from __future__ import annotations` and no AST transformer
    that changes it (input transformers would already show up as a text difference)."""
    import ast, __future__
    flags = getattr(getattr(ip, 'compile', None), 'flags', 0) or 0
    fut = [f for f in ('annotations', 'barry_as_FLUFL') if flags & getattr(__future__, f).compiler_flag]
    if fut: return 'an earlier cell enabled `from __future__ import %s`; restart the session (Runtime > Restart session)' % ', '.join(fut)
    if getattr(ip, 'ast_transformers', None):
        try: same = ast.dump(ip.transform_ast(ast.parse(text, filename))) == ast.dump(ast.parse(text, filename))
        except Exception as e: return 'IPython AST transformer failed on 908: %s: %s' % (type(e).__name__, e)
        if not same: return 'IPython AST transformers %s change the code' % [type(t).__name__ for t in ip.ast_transformers]
    return None


def _clean_shadowed_builtins(g, text):
    """an earlier cell's `len = ...` would change what 908 calls: builtins that 908 uses but the notebook namespace redefines are
    removed from the namespace (a clean process has none); a functools.wraps wrapper of the builtin itself (IPython's open) stays.
    Returns (removed, removed_but_used_by_top_level_code): the second ones already acted while the cell defined its constants.
    Runs before the clean-up is complete, so it calls builtins through the builtins module only."""
    import builtins as B, symtable
    top = symtable.symtable(text, 'cell', 'exec'); defined = {s.get_name() for s in top.get_symbols() if s.is_assigned() or s.is_imported()}
    at_top = {s.get_name() for s in top.get_symbols() if s.is_referenced()}
    used, todo = B.set(), [top]
    while todo:
        t = todo.pop(); todo.extend(t.get_children())
        used |= {s.get_name() for s in t.get_symbols() if s.is_referenced() and (s.is_global() or t.get_type() == 'module')}
    gone = []
    for n in B.sorted(used - defined):
        if n.startswith('__') or not B.hasattr(B, n) or n not in g: continue
        v, real = g[n], B.getattr(B, n)
        if v is real or B.getattr(v, '__wrapped__', None) is real: continue
        del g[n]; gone.append(n)
    return gone, [n for n in gone if n in at_top]


def staged_self():
    """the staged 908 file (/content/908.py or $T908_SELF): bytes + identity. 908 is not taken from GitHub (it is not published there)."""
    p = Path(os.environ.get('T908_SELF') or REPO_908)
    if not p.is_file() or p.is_symlink(): raise Stop908('STAGED_908_NOT_FOUND %s' % p)
    b = p.read_bytes(); return b, {'path': str(p), 'sha256': sha_b(b), 'git_blob': blob_b(b), 'bytes': len(b)}


def _notebook_identity(g, own_file, out, staged=None):
    """TEST908 r2 cell-native: accept the ENTIRE executing Colab cell as its own source, WITHOUT requiring a staged file.
    Fail closed unless IPython provides the currently compiled cell text, all top-level functions were created by this
    exact cell, and no AST/future-feature rewriting or stale builtin shadowing occurred. Capture and SHA-256 / Git-blob
    seal that cell text; package the actual captured bytes for independent read-back authentication. No GitHub fetch,
    staged /content file, Drive access, or alternate source substitution is involved in this cell identity decision.
    """
    def fail(method, reason): return dict(out, file=None, method=method, reason=reason), None
    text = _cell_text(own_file)
    if text is None: return fail('NOTEBOOK_CELL_TEXT_UNAVAILABLE', 'IPython has no source text registered for %s' % own_file)
    gone, at_top = _clean_shadowed_builtins(g, text); out['namespace_builtins_removed'] = gone
    if at_top: return fail('NOTEBOOK_BUILTINS_SHADOWED', 'an earlier cell redefined %s, which this cell used while defining its constants; '
                           'restart the session (Runtime > Restart session) and paste 809.py again' % at_top)
    try: names = _top_functions(text.encode('utf-8'))
    except Exception as e: return fail('NOTEBOOK_CELL_INVALID_SOURCE', '%s: %s' % (type(e).__name__, str(e)[:300]))
    stale = [n for n in names if not (isinstance(g.get(n), types.FunctionType) and g[n].__code__.co_filename == own_file)]
    if not names or stale: return fail('NOTEBOOK_FUNCTIONS_NOT_FROM_THIS_CELL', 'top-level functions not defined by this cell: %s' % stale[:8])
    ip = g.get('get_ipython') or getattr(sys.modules.get('builtins'), 'get_ipython', None)
    if ip is None and 'IPython' in sys.modules: ip = getattr(sys.modules['IPython'], 'get_ipython', None)
    ip = ip() if callable(ip) else None
    if ip is None: return fail('NOTEBOOK_NO_IPYTHON', 'a notebook cell file name but no IPython shell')
    why = _ipython_rewrites(ip, text, own_file)
    if why: return fail('NOTEBOOK_CODE_REWRITTEN', why)
    b = text.encode('utf-8')
    out['cell_sha256'] = sha_b(b)
    out['cell_lines'] = len(_canon_lines(text))
    return dict(out, file='NOTEBOOK_CELL ' + str(own_file), sha256=sha_b(b), git_blob=blob_b(b), bytes=len(b),
                functions_checked=len(names), method='NOTEBOOK_CELL_SELF_CAPTURE',
                normalisation='none; exact IPython-registered cell UTF-8 bytes',
                code_digest=code_digest([g[n] for n in names]), git={'head': None, 'committed_blob': None, 'note': 'notebook cell; no local Git checkout required'}), b


def executed_source_identity(g=None, cfg=None, published=None):
    """the 908 source that is actually executing, in one of two accepted ways (everything else fails closed):
    NOTEBOOK_CELL: the whole 809.py pasted into one cell; capture the CURRENT IPython-compiled cell text with no staged file.
    SCRIPT: `!python 809.py` / an equivalent real `%run`: __name__ is __main__, argv[0], __file__ and the running function's filename
    identify the same non-symlink file, read once with a before/after stat check; two different existing 908 candidates fail.
    Candidate files are NEVER exec'd; exec strings and imports are refused."""
    g = g if g is not None else globals(); own = g.get('executed_source_identity')
    own_file = getattr(getattr(own, '__code__', None), 'co_filename', None); mode = _execution_mode(own_file, g)
    out = {'execution_mode': mode, 'code_filename': own_file, 'candidates': [], 'tried': []}
    def fail(method, reason): return dict(out, file=None, method=method, reason=reason), None
    if mode == 'NOTEBOOK_CELL':
        return _notebook_identity(g, own_file, out)
    if mode != 'SCRIPT_OR_%RUN' or g.get('__name__') != '__main__' or not g.get('__file__'):
        return fail('NOT_FOUND', '809 must run from one notebook cell containing ALL of 809.py, or as a saved file in its own __main__ '
                    'process; exec strings and imports are not accepted')
    paths = [Path(str(x)) for x in (own_file, g.get('__file__'), sys.argv[0] if sys.argv else None) if x]
    if len(paths) != 3:
        return fail('NOT_FOUND', 'code filename, __file__ and argv[0] are required')
    try:
        resolved = [p.resolve(strict=True) for p in paths]
    except OSError as e:
        return fail('NOT_FOUND', 'executed source is not a saved file: %s' % e)
    if len(set(resolved)) != 1 or any(p.is_symlink() for p in paths):
        return fail('AMBIGUOUS', 'code filename, __file__ and argv[0] must be the same non-symlink file: %s' % [str(p) for p in paths])
    p = paths[0]; st0 = p.stat()
    if not stat.S_ISREG(st0.st_mode): return fail('NOT_FOUND', 'executed source is not a regular file')
    b = p.read_bytes(); st1 = p.stat()
    if (st0.st_dev, st0.st_ino, st0.st_size, st0.st_mtime_ns) != (st1.st_dev, st1.st_ino, st1.st_size, st1.st_mtime_ns):
        return fail('SOURCE_CHANGED_DURING_READ', 'executed file changed while its bytes were read')
    names = _top_functions(b)
    if not names or not all(isinstance(g.get(n), types.FunctionType) for n in names):
        return fail('NOT_FOUND', 'running namespace does not contain every top-level function from the executed file')
    out['candidates'].append({'path': str(p), 'sha256': sha_b(b), 'result': 'DIRECT_FILE_MATCH'}); out['tried'].append(str(p))
    for c in (os.environ.get('T908_SELF'), REPO_908):
        if not c: continue
        q = Path(c)
        try:
            if q.resolve() == resolved[0] or not q.is_file(): continue
            qb = q.read_bytes(); row = {'path': c, 'sha256': sha_b(qb)}; out['candidates'].append(row); out['tried'].append(c)
            if qb != b:
                return fail('AMBIGUOUS', 'different 908.py candidates: %s' % [(str(p), sha_b(b)[:12]), (c, sha_b(qb)[:12])])
            row['result'] = 'SAME_BYTES'
        except OSError as e:
            return fail('SOURCE_READ_ERROR', '%s: %s' % (c, e))
    return dict(out, file=str(resolved[0]), sha256=sha_b(b), git_blob=blob_b(b), bytes=len(b), functions_checked=len(names),
                method='direct___main___file', code_digest=code_digest([g[n] for n in names]), git=git_provenance(p)), b


def _drive_mount_info(root, mountinfo_text=None):
    """Linux mount record for Colab Drive: a real mount at root, FUSE filesystem and a Drive source. A look-alike directory fails."""
    root = os.path.abspath(str(root))
    try: text = Path('/proc/self/mountinfo').read_text() if mountinfo_text is None else mountinfo_text
    except OSError as e: return False, {'error': '%s: %s' % (type(e).__name__, e)}
    for line in text.splitlines():
        left, sep, right = line.partition(' - ')
        if not sep: continue
        a = left.split(); b = right.split()
        if len(a) < 5 or len(b) < 2: continue
        mp = a[4].replace('\\040', ' ').replace('\\011', '\t').replace('\\012', '\n').replace('\\134', '\\')
        fstype, source = b[0], b[1]
        if mp == root:
            ok = (fstype == 'fuse' or fstype.startswith('fuse.')) and 'drive' in source.lower()
            return ok, {'mountpoint': mp, 'fstype': fstype, 'source': source, 'ok': ok}
    return False, {'error': 'NO_MOUNTINFO_RECORD', 'mountpoint': root}


def _forbidden_roots(mountinfo_text=None):
    """908 r2 (P2-4): Drive roots that no pre-A100 path may reach: /content/drive and every FUSE Drive mount point listed in
    /proc/self/mountinfo (reading /proc is not a Drive operation)."""
    roots = {'/content/drive'}
    try: text = Path('/proc/self/mountinfo').read_text() if mountinfo_text is None else mountinfo_text
    except OSError: text = ''
    for line in text.splitlines():
        left, sep, right = line.partition(' - ')
        a = left.split(); b = right.split()
        if sep and len(a) >= 5 and len(b) >= 2 and (b[0] == 'fuse' or b[0].startswith('fuse.')) and 'drive' in b[1].lower():
            roots.add(os.path.normpath(a[4].replace('\\040', ' ')))
    return sorted(roots)


def _under(p, roots):
    return any(p == r or p.startswith(r.rstrip('/') + '/') for r in roots)


def safe_local_path(path, roots, cwd, lstat=None, readlink=None):
    """resolve path component by component (symlinks followed, '..' applied to the RESOLVED prefix) without ever touching a forbidden
    root: every candidate prefix is checked lexically BEFORE lstat; a symlink target is re-checked lexically before it is entered;
    missing components are not stat'ed further. Returns (resolved, None) or (None, reason)."""
    lstat = lstat or os.lstat; readlink = readlink or os.readlink
    if not isinstance(path, str) or not path: return None, 'EMPTY_PATH'
    full = path if path.startswith('/') else cwd.rstrip('/') + '/' + path
    parts = [c for c in full.split('/')]; cur = '/'; hops = 0; missing = False
    while parts:
        c = parts.pop(0)
        if c in ('', '.'): continue
        if c == '..': cur = os.path.dirname(cur) or '/'; continue
        nxt = (cur.rstrip('/') + '/' + c)
        if _under(nxt, roots): return None, 'DRIVE_PATH %s' % nxt
        if missing: cur = nxt; continue
        try: st = lstat(nxt)
        except FileNotFoundError: missing = True; cur = nxt; continue
        except OSError as e: return None, 'LSTAT_ERROR %s: %s' % (nxt, type(e).__name__)
        if stat.S_ISLNK(st.st_mode):
            hops += 1
            if hops > 40: return None, 'SYMLINK_LOOP %s' % nxt
            t = readlink(nxt)
            if t.startswith('/'): cur = '/'
            parts = [x for x in t.split('/')] + parts
            continue
        cur = nxt
    if _under(cur, roots): return None, 'DRIVE_PATH %s' % cur
    return cur, None


def preflight_path_policy(cfg, g=None, roots=None, cwd=None, lstat=None, readlink=None):
    """908 r2 (P2-4): runs BEFORE init_run and every other file operation. Every path used before the A100 pre-flight - cwd, out_root,
    src_dir, repo_dir and (ONLY for script execution) optional staged source / script file must resolve (safe_local_path) to a
    LOCAL path outside every Drive root, also through symlinks / parent symlinks / '..' / relative paths. In a pasted notebook
    cell no staged file is read or required. Violation -> technical stop
    before any file is written (no Drive I/O). The post-A100 Drive paths (903 archive, references, run archive) are not pre-A100 paths."""
    g = g if g is not None else globals(); roots = roots if roots is not None else _forbidden_roots()
    try: cwd = cwd or os.getcwd()
    except OSError as e: return {'ok': False, 'problems': ['CWD_UNAVAILABLE %s' % type(e).__name__], 'roots': roots, 'resolved': {}}
    chk = [('cwd', cwd), ('out_root', cfg.get('out_root'))]
    chk += [(k, cfg.get(k)) for k in ('src_dir', 'repo_dir') if cfg.get(k)]
    own = g.get('executed_source_identity')
    own_file = getattr(getattr(own, '__code__', None), 'co_filename', None)
    if _execution_mode(own_file, g) != 'NOTEBOOK_CELL':
        chk.append(('staged_source', os.environ.get('T908_SELF') or REPO_908))
        if g.get('__file__'): chk.append(('executed_file', str(g['__file__'])))
    probs, res = [], {}
    for name, p in chk:
        r, why = safe_local_path(str(p) if p is not None else '', roots, cwd, lstat, readlink)
        if why: probs.append('%s: %s' % (name, why))
        else: res[name] = r
    return {'ok': not probs, 'problems': probs, 'roots': roots, 'resolved': res}


def drive_guard(op):
    """TEST908 order contract: no Google Drive mount / presence probe / read / write before GATE_GPU_PREFLIGHT_906 and
    GATE_GPU_PREFLIGHT_908 passed in this process (X.A100_PASS). Every Drive-touching step calls this first; a violation is a
    technical stop (and nothing has been sent to Drive)."""
    if getattr(X, 'A100_PASS', False) is not True:
        X.DRIVE_VIOLATION = op; raise Stop908('DRIVE_BEFORE_A100_PREFLIGHT ' + op)
    X.DRIVE_OPS.append(op)


def _in_kernel():
    """True inside a live IPython kernel (a notebook cell or %run), False in a '!python' child process or a plain interpreter."""
    try:
        import IPython
        return IPython.get_ipython() is not None
    except Exception:
        return False


def ensure_drive_908(cfg, mode):
    """after the A100 pre-flight only: the pinned 906 ensure_drive_906 mounts Drive when this code runs inside the Colab kernel (a
    notebook cell or %run); a '!python' child process cannot mount (mount Drive in a separate cell before). GATE_DRIVE_PRESENT and
    GATE_DRIVE judge the result; nothing is assumed."""
    drive_guard('ensure_drive')
    return M6.ensure_drive_906(cfg, 'NOTEBOOK_CELL' if (mode == 'NOTEBOOK_CELL' or _in_kernel()) else mode)


def drive_after_a100(events):
    """event-log order check (live end gate and --recompute authentication): GATE_GPU_PREFLIGHT_908 PASS precedes every Drive gate."""
    seq = [(e.get('name'), e.get('status')) for e in (events or []) if isinstance(e, dict) and e.get('kind') == 'GATE']
    names = [n for n, _ in seq]
    if ('GATE_GPU_PREFLIGHT_908', 'PASS') not in seq: return False
    i = seq.index(('GATE_GPU_PREFLIGHT_908', 'PASS'))
    return all(n not in names[:i] for n in DRIVE_GATES)


def preflight_908_status(pf, drive_ops, violation):
    """GATE_GPU_PREFLIGHT_908 rule: PASS only if the pinned 906 A100 pre-flight passed AND no Drive operation / violation happened before."""
    ok = pf == 'PASS' and not drive_ops and violation is None
    return ok, None if ok else 'GPU_REQUIRED_A100_TECHNICAL_STOP: A100 pre-flight %s; Drive operations before it: %s; violation %s' % (pf, drive_ops, violation)


def init_run(cfg):
    global RUN_ID, ROOT, LOG, OUT, EVENTS, R
    RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'); ROOT = Path(cfg['out_root']) / ('TEST908_' + RUN_ID); ROOT.mkdir(parents=True, exist_ok=False)
    LOG = ROOT / 'TEST908.log'; OUT = ROOT / 'TEST908_results.json'; EVENTS = ROOT / 'TEST908_events.jsonl'
    for f in (LOG, EVENTS): f.write_text('')
    X.A100_PASS = False; X.DRIVE_OPS = []; X.DRIVE_VIOLATION = None
    R = {'test': TAG, 'revision': REVISION, 'marker': MARKER, 'label': LABEL, 'run_id': RUN_ID, 'status': 'STARTED', 'executed_by_author': False,
         'top': {'first_failed_gate': None, 'technical_verdict': None, 'verdict': None, 'availability_diagnostic': None},
         'sources_pinned': {'906': SRC906, '903': SRC903, '904': SRC904, 'engine_blobs': ENGINE_BLOBS_908}, 'derived_from': SRC907A,
         'run_906': RUN906, 'run_907A': RUN907A, 'budget': BUDGET, 'gates': {}, 'checks': [], 'technical_blockers': [], 'config': dict(cfg),
         'prefix': {}, 'arms': {}, 'fullref': {}, 'sham_map': {}, 'objects': {}, 'rope_reference': [], 'branches': {}, 'drive_ops': X.DRIVE_OPS}


def bind_engine():
    """the pinned 906 r2 module runs on THIS run's engine, record and files (module globals only; its bytes are unchanged)."""
    for k, v in dict(M3=M3, m3=M3, M4=M4, X=X, R=R, ROOT=ROOT, RUN_ID=RUN_ID, LOG=LOG, OUT=OUT, EVENTS=EVENTS, T0=T0).items(): setattr(M6, k, v)
    M6.bind_903(M3)                                                       # 906 r2: 903 writes into this run's files; CRITICAL += CRITICAL_906
    M3.CRITICAL = tuple(M3.CRITICAL) + CRITICAL_908


def log(*a): M3.log(*a)


def gate(*a, **k): M3.gate(*a, **k)


def drive_gate(cfg):
    global DRIVE_DIR
    drive_guard('drive_gate')
    mounted, mount_info = _drive_mount_info(MYDRIVE.parent)
    mounted = bool(mounted and MYDRIVE.is_dir())
    if cfg.get('drive') == 'required' and not mounted:
        gate('GATE_DRIVE', 'FAIL', 'Drive delivery required but a real Drive/FUSE /content/drive mount with MyDrive is not available: %s. '
             'Run `from google.colab import drive; drive.mount("/content/drive")` in a separate notebook cell, then start 908 again.' % mount_info)
    probe = None
    if mounted and cfg.get('drive') != 'off':
        DRIVE_DIR = str(MYDRIVE / ('TEST908_' + RUN_ID)); os.makedirs(DRIVE_DIR, exist_ok=False)
        data = os.urandom(4096); pp = Path(DRIVE_DIR) / '.TEST908_write_probe'
        try:
            with open(pp, 'wb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
            probe = sha_b(pp.read_bytes()) == sha_b(data); pp.unlink()
        except OSError as e: probe = False; X.PROBE_ERR = '%s: %s' % (type(e).__name__, e)
        if not probe: gate('GATE_DRIVE', 'FAIL', 'Drive write / read-back probe failed in %s (%s)' % (DRIVE_DIR, getattr(X, 'PROBE_ERR', 'sha mismatch')))
        M3.DRIVE_DIR = DRIVE_DIR; M3.save(force=True)
    gate('GATE_DRIVE', 'PASS', None, mode=cfg.get('drive'), mounted=mounted, mount_info=mount_info, dir=DRIVE_DIR, write_read_back_probe=probe)


def drive_copy(src, dst_dir): return M3.drive_copy_verified(src, dst_dir) if M3 is not None else (False, 'NO_ENGINE')


def finalize_artifacts(cfg=None):
    """local artefacts (always kept) -> ZIP copy + read-back -> FINAL receipt copy + byte read-back. The receipt copied to Drive is
    the final one: on success the local and Drive receipts are byte-identical; on failure the local receipt states the failure and
    a failure receipt is attempted on Drive so that both say the same."""
    R['finished_utc'] = datetime.now(timezone.utc).isoformat(); R['elapsed_s'] = round(time.perf_counter() - T0, 1)
    try: M3.save() if M3 and M3.R is R else OUT.write_text(json.dumps(R, ensure_ascii=False, indent=1, default=str))
    except Exception as e: print('RESULTS_WRITE_FAILED', e)
    AG = {}
    try:
        rep = sha_file(OUT); AG['report_written_read_back'] = json.loads(OUT.read_text())['run_id'] == RUN_ID
        files = sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name != 'SHA256SUMS.txt' and not p.name.endswith('.tmp'))
        (ROOT / 'SHA256SUMS.txt').write_text('\n'.join('%s  %s' % (sha_file(p), p.relative_to(ROOT).as_posix()) for p in files) + '\n')
        zp = ROOT.parent / ('TEST908_SONUC_%s.zip' % RUN_ID)
        with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in files + [ROOT / 'SHA256SUMS.txt']: z.write(p, ROOT.name + '/' + p.relative_to(ROOT).as_posix())
        with zipfile.ZipFile(zp) as z:
            AG['zip_testzip'] = z.testzip() is None
            rows = [l.split('  ', 1) for l in z.read(ROOT.name + '/SHA256SUMS.txt').decode().split('\n') if l]
            AG['sha256sums'] = all(sha_b(z.read(ROOT.name + '/' + rel)) == h for h, rel in rows) and len(rows) == len(files)
            AG['report_in_zip_is_read_back_report'] = sha_b(z.read(ROOT.name + '/' + OUT.name)) == rep
        AG['zip'] = str(zp); AG['zip_sha256'] = sha_file(zp)
    except Exception as e:
        AG['artifact_error'] = '%s: %s' % (type(e).__name__, e)
    local_ok = all(AG.get(k) is True for k in ('report_written_read_back', 'zip_testzip', 'sha256sums', 'report_in_zip_is_read_back_report'))
    mode = (cfg or R.get('config') or {}).get('drive', 'auto'); requested = mode == 'required' or (mode == 'auto' and DRIVE_DIR is not None)
    D = {'requested': requested, 'mode': mode, 'dir': DRIVE_DIR, 'zip_copied_read_back': None, 'receipt': 'FINAL_SELF_VERIFIED_BY_BYTE_READ_BACK', 'error': None,
         'live_backup_failures': (getattr(M3, 'DRIVE_ERR', {}) or {}).get('backup_failures') if M3 else None}
    if requested and DRIVE_DIR is None and getattr(X, 'A100_PASS', False) is not True:
        D['error'] = 'DRIVE_NOT_TOUCHED_A100_PREFLIGHT_NOT_PASSED'                # no Drive stat / probe at all before the A100 gate
    elif requested and DRIVE_DIR is None:
        really_mounted = _drive_mount_info(MYDRIVE.parent)[0] and MYDRIVE.is_dir()
        D['error'] = ('DRIVE_NOT_ATTEMPTED_RUN_STOPPED_BEFORE_GATE_DRIVE' if really_mounted and 'GATE_DRIVE' not in R['gates']
                      else 'DRIVE_REQUIRED_BUT_NOT_MOUNTED')
    elif requested and local_ok:
        ok, err = drive_copy(Path(AG['zip']), DRIVE_DIR); D['zip_copied_read_back'] = ok
        if not ok: D['error'] = 'ZIP: %s' % err
    if not local_ok: st = 'FAIL_LOCAL_ARTIFACTS'
    elif not requested: st = 'LOCAL_ONLY_DRIVE_NOT_REQUESTED'
    elif D['error'] and D['error'].startswith('DRIVE_NOT_TOUCHED'): st = 'GPU_STOP_DRIVE_NOT_TOUCHED'
    elif D['error'] and D['error'].startswith('DRIVE_REQUIRED_BUT_NOT_MOUNTED'): st = 'DRIVE_NOT_MOUNTED'
    elif D['error'] and D['error'].startswith('DRIVE_NOT_ATTEMPTED'): st = 'DRIVE_NOT_ATTEMPTED_RUN_STOPPED_EARLY'
    elif D['error']: st = 'DRIVE_ZIP_NOT_DELIVERED'
    else: st = 'PASS'                                                    # final, valid only together with the byte read-back below
    receipt = {'test': TAG, 'run_id': RUN_ID, 'status': R.get('status'), 'top': R.get('top'), 'artifacts': AG, 'drive': D, 'artifact_status': st,
               'results_sha256': sha_file(OUT) if AG.get('report_written_read_back') else None}
    rp = ROOT.parent / ('TEST908_SONUC_%s_RECEIPT.json' % RUN_ID); body = json.dumps(receipt, indent=1, default=str); rp.write_text(body)
    if requested and DRIVE_DIR is not None and local_ok:
        ok, err = drive_copy(rp, DRIVE_DIR)
        if ok:
            try: ok = (Path(DRIVE_DIR) / rp.name).read_text() == body
            except Exception as e: ok, err = False, '%s: %s' % (type(e).__name__, e)
            if not ok and not err: err = 'READ_BACK_MISMATCH'
        if not ok:
            if st == 'PASS': receipt['artifact_status'] = 'DRIVE_RECEIPT_NOT_DELIVERED'
            receipt['drive'] = dict(D, error=(D['error'] + '; ' if D['error'] else '') + 'RECEIPT: %s' % err); body = json.dumps(receipt, indent=1, default=str); rp.write_text(body)
            ok2, _ = drive_copy(rp, DRIVE_DIR)                            # best effort: Drive then carries the same failure state
            try: receipt_drive_state = 'EQUAL' if ok2 and (Path(DRIVE_DIR) / rp.name).read_text() == body else 'ABSENT_OR_STALE'
            except Exception: receipt_drive_state = 'ABSENT_OR_STALE'
            X.RECEIPT_DRIVE_STATE = receipt_drive_state
        else: X.RECEIPT_DRIVE_STATE = 'EQUAL'
    else: X.RECEIPT_DRIVE_STATE = 'NOT_COPIED'
    X.RECEIPT = receipt
    print('TEST908 ARTIFACTS', json.dumps({'artifact_status': receipt['artifact_status'], 'drive_receipt': X.RECEIPT_DRIVE_STATE, 'zip': AG.get('zip')}, default=str), flush=True)
    return receipt


def exit_code(receipt):
    if R.get('status') != 'COMPLETE' or R.get('technical_verdict') != 'PASS': return 1
    return 0 if receipt.get('artifact_status') in ('PASS', 'LOCAL_ONLY_DRIVE_NOT_REQUESTED') else 2


def status_line(rc, receipt):
    t = R.get('top') or {}; a = receipt.get('artifact_status'); d = receipt.get('drive') or {}
    drive = 'PASS' if a == 'PASS' else ('NOT_REQUESTED' if a == 'LOCAL_ONLY_DRIVE_NOT_REQUESTED' else 'FAILED[%s: %s]' % (a, d.get('error')))
    head = {0: 'TAMAMLANDI', 2: 'TAMAMLANDI_TESLIM_HATASI'}.get(rc, 'TEKNIK_HATA')
    return 'TEST908 DURUM: %s | EXIT=%d | TECHNICAL=%s | VERDICT=%s | GREEDY=%s | DRIVE=%s | FIRST_GATE=%s | RESULTS=%s' % (
        head, rc, t.get('technical_verdict'), t.get('verdict'), getattr(X, 'NSEQ', None), drive, t.get('first_failed_gate'), OUT)


def kernel_cleanup(g):
    """Colab kernel exec(): an earlier TEST903..908 exec leaves its engine module (holding a 72B model) in globals; drop only those
    references (906 r2 logic; 908 also knows TEST908 and keeps its own M6)."""
    gone = [n for n, v in list(g.items()) if isinstance(v, types.ModuleType) and getattr(v, 'TAG', None) in ('TEST903', 'TEST904', 'TEST905', 'TEST906', 'TEST907A', 'TEST908')
            and n not in ('M3', 'M4', 'm3', 'M6')]
    for n in gone: del g[n]
    for a in ('last_type', 'last_value', 'last_traceback', 'last_exc'):
        if hasattr(sys, a): setattr(sys, a, None)
    import gc; gc.collect()
    if 'torch' in sys.modules:
        try: sys.modules['torch'].cuda.empty_cache()
        except Exception: pass
    return gone


def receipt_problems(rp, test, run, zip_sha_disk, results_sha_member):
    """908 r2 (P2-1): a reference receipt is REQUIRED and must be a non-empty JSON object of the r2 receipt schema (fields as written by
    finalize_artifacts: test, run_id, artifact_status, results_sha256, artifacts.zip_sha256 / zip_testzip / sha256sums) naming exactly the
    pinned run, the pinned results SHA (= the ZIP member) and the pinned ZIP SHA (= the file on disk). Missing / unreadable / malformed /
    any difference -> problems (never a default PASS)."""
    p = Path(rp)
    if not p.is_file(): return ['RECEIPT_MISSING']
    try: b = p.read_bytes()
    except Exception as e: return ['RECEIPT_UNREADABLE %s' % type(e).__name__]
    try: rj = json.loads(b)
    except Exception: return ['RECEIPT_NOT_JSON']
    if not isinstance(rj, dict) or not rj: return ['RECEIPT_NOT_AN_OBJECT']
    why = []
    if rj.get('test') != test: why.append('RECEIPT_TEST')
    if rj.get('run_id') != run['run_id']: why.append('RECEIPT_RUN_ID')
    if rj.get('artifact_status') != 'PASS': why.append('RECEIPT_ARTIFACT_STATUS')
    rs = rj.get('results_sha256')
    if not (_hex(rs) and rs == run['results_sha256'] and rs == results_sha_member): why.append('RECEIPT_RESULTS_SHA')
    art = rj.get('artifacts')
    if not isinstance(art, dict): why.append('RECEIPT_ARTIFACTS_MISSING'); return why
    zs = art.get('zip_sha256')
    if not (_hex(zs) and zs == run['zip_sha256'] and zs == zip_sha_disk): why.append('RECEIPT_ZIP_SHA')
    if art.get('zip_testzip') is not True or art.get('sha256sums') is not True: why.append('RECEIPT_ARTIFACT_CHECKS')
    return why


def ref906_gate(cfg):
    """TEST906 reference identity, READ-ONLY (files opened for reading only, never written / renamed): the ZIP by pinned SHA-256 (+ testzip),
    its results member by pinned SHA-256 with the recorded run id / technical PASS / verdict, and the REQUIRED receipt (receipt_problems)."""
    drive_guard('ref906_gate')
    d = Path(cfg.get('ref906_dir') or DEFAULT_REF906_DIR); zp = d / RUN906['zip_name']; rp = d / RUN906['receipt_name']; G = {'dir': str(d)}
    if not zp.is_file(): gate('GATE_REF906_908', 'FAIL', 'TEST906 reference ZIP not found: %s (expected next to its receipt in MyDrive/TEST906_%s/; nothing is '
                              'written there)' % (zp, RUN906['run_id']), **G)
    G['zip_sha256'] = sha_file(zp); G['zip_sha256_equal'] = G['zip_sha256'] == RUN906['zip_sha256']
    try:
        with zipfile.ZipFile(zp) as z:
            G['zip_testzip'] = z.testzip() is None
            b = z.read(RUN906['results_member']); G['results_sha256'] = sha_b(b); G['results_sha256_equal'] = G['results_sha256'] == RUN906['results_sha256']
            r = json.loads(b); r = r if isinstance(r, dict) else {}
            G['verdict'] = (r.get('top') or {}).get('verdict'); G['verdict_equal'] = G['verdict'] == RUN906['verdict']
            G['technical_pass'] = r.get('technical_verdict') == 'PASS' and r.get('run_id') == RUN906['run_id']
    except Exception as e: G['zip_error'] = '%s: %s' % (type(e).__name__, e)
    G['receipt_problems'] = receipt_problems(rp, 'TEST906', RUN906, G.get('zip_sha256'), G.get('results_sha256'))
    ok = (all(G.get(k) is True for k in ('zip_sha256_equal', 'zip_testzip', 'results_sha256_equal', 'verdict_equal', 'technical_pass'))
          and not G['receipt_problems'] and 'zip_error' not in G)
    X.REF906 = G
    gate('GATE_REF906_908', 'PASS' if ok else 'FAIL', None if ok else 'TEST906 reference identity differs from the pinned record: %s' % G, **G)


def ref907a_gate(cfg):
    """TEST907A r2 reference identity (the run this test repairs), READ-ONLY (opened 'rb'; never written / renamed / deleted): the ZIP
    by pinned SHA-256 (+ testzip), its results member by pinned SHA-256 with the recorded run id, technical PASS and verdict, and the
    receipt naming the same results and ZIP. Any difference: technical stop before the model."""
    drive_guard('ref907a_gate')
    d = Path(cfg.get('ref907a_dir') or DEFAULT_REF907A_DIR); zp = d / RUN907A['zip_name']; rp = d / RUN907A['receipt_name']; G = {'dir': str(d)}
    if not zp.is_file(): gate('GATE_REF907A_908', 'FAIL', 'TEST907A reference ZIP not found: %s (expected in MyDrive/TEST907A_%s/; nothing is '
                              'written there)' % (zp, RUN907A['run_id']), **G)
    G['zip_sha256'] = sha_file(zp); G['zip_sha256_equal'] = G['zip_sha256'] == RUN907A['zip_sha256']
    try:
        with zipfile.ZipFile(zp) as z:
            G['zip_testzip'] = z.testzip() is None
            b = z.read(RUN907A['results_member']); G['results_sha256'] = sha_b(b); G['results_sha256_equal'] = G['results_sha256'] == RUN907A['results_sha256']
            r = json.loads(b); r = r if isinstance(r, dict) else {}; G['verdict'] = (r.get('top') or {}).get('verdict'); G['verdict_equal'] = G['verdict'] == RUN907A['verdict']
            G['technical_pass'] = r.get('technical_verdict') == 'PASS' and r.get('run_id') == RUN907A['run_id']
    except Exception as e: G['zip_error'] = '%s: %s' % (type(e).__name__, e)
    G['receipt_problems'] = receipt_problems(rp, 'TEST907A', RUN907A, G.get('zip_sha256'), G.get('results_sha256'))     # 908 r2: same rule as TEST906
    ok = (all(G.get(k) is True for k in ('zip_sha256_equal', 'zip_testzip', 'results_sha256_equal', 'verdict_equal', 'technical_pass'))
          and not G['receipt_problems'] and 'zip_error' not in G)
    X.REF907A = G
    gate('GATE_REF907A_908', 'PASS' if ok else 'FAIL', None if ok else 'TEST907A reference identity differs from the pinned record: %s' % G, **G)


def surface_tokinfo(enc, decoy_cat, cat_pred, cat_obs):
    """pure (908): the model-facing surfaces sealed before the model, from enc(q) = the pinned tokenizer ids of SUFFIX_HEAD + q +
    SUFFIX_TAIL. First-decision q of X / Y; every pre-prediction state reachable before any ACQUIRE (W = () or (MZ4), catalog = decoy,
    cue live, PROBE_A=AVAILABLE) must differ X vs Y (else PRED_INPUT_COLLAPSE_PRE_MODEL); the A- placebo = the FIRST of
    PLACEBO_CANDIDATES whose q ids have the A+ (PROBE_A=CONSUMED) length with one differing window <= PLACEBO_WINDOW_MAX for both
    post-commit W states reachable before a fork; q_F token counts for every ordered W holding PRED and OBS. Returns (info, problems)."""
    bad = []; d, p, o = HANDLES['decoy'], HANDLES['pred'], HANDLES['obs']
    for v in AVAIL_STATES + PLACEBO_CANDIDATES:
        if any(x in v.lower() for x in FORBIDDEN_SURFACE_WORDS): bad.append('SURFACE_FORBIDDEN_WORD ' + v)
    q0 = {w: build_q(TASK_TEXT, CUES[w], AVAIL_STATES[0], [decoy_cat], ()) for w in WORLDS}
    if q0['X'] == q0['Y']: bad.append('XY_ILL_POSED_IDENTICAL_INITIAL_INPUT')
    q0_ids = {w: enc(q0[w]) for w in WORLDS}
    pre = {w: {','.join(ws): sha_s(json.dumps(enc(build_q(TASK_TEXT, CUES[w], AVAIL_STATES[0], [decoy_cat], ws)))) for ws in ((), (d,))} for w in WORLDS}
    if any(pre['X'][k] == pre['Y'][k] for k in pre['X']): bad.append('PRED_INPUT_COLLAPSE_PRE_MODEL')
    full = [decoy_cat, cat_pred, cat_obs]; trials = {}; chosen = None
    for v in PLACEBO_CANDIDATES:
        trials[v] = all(_window_ok(enc(build_q(TASK_TEXT, None, AVAIL_STATES[1], full, ws)), enc(build_q(TASK_TEXT, None, v, full, ws))) for ws in ((), (d,)))
        if trials[v] and chosen is None: chosen = v
    placebo = {'value': chosen or PLACEBO_CANDIDATES[0], 'position_controlled_preseal': chosen is not None, 'trials': trials, 'window_max': PLACEBO_WINDOW_MAX,
               'rule': 'first candidate (presealed order) whose A- q ids equal the A+ length with one differing window, for W in ((), (%s,))' % d}
    orders = [(p, o), (o, p)] + [t for t in ((d, p, o), (d, o, p), (p, d, o), (o, d, p), (p, o, d), (o, p, d))]
    qf_tokens = {','.join(ws): len(enc(build_q(TASK_TEXT, None, AVAIL_STATES[1], full, ws))) for ws in orders}
    info = {'q0_sha256': {w: sha_s(q0[w]) for w in WORLDS}, 'q0_ids_sha256': {w: sha_s(json.dumps(q0_ids[w])) for w in WORLDS},
            'q0_tokens': {w: len(q0_ids[w]) for w in WORLDS}, 'q_pre_ids_sha256': pre, 'qF_tokens': qf_tokens, 'placebo': placebo}
    return info, bad


def tokenizer_gate():
    """pinned tokenizer, before the model: RoPE config (pinned config.json), special / stop / pad ids, observation ids for both
    outcomes (equal length, no special id), the two canonical predictions (equal length), the handles, the cue word rules, grammar
    round trips and the 908 model-facing surfaces (surface_tokinfo: X / Y first and pre-prediction inputs differ, A- placebo, q_F)."""
    m = M3; tk = m.transformers.AutoTokenizer.from_pretrained(m.MODEL_ID, revision=m.MODEL_REVISION, trust_remote_code=False); bad = []
    from huggingface_hub import hf_hub_download
    X.ROPE_PRE = M6.rope_config(types.SimpleNamespace(**json.loads(Path(hf_hub_download(m.MODEL_ID, 'config.json', revision=m.MODEL_REVISION)).read_text())))
    if not (X.ROPE_PRE['theta'] and X.ROPE_PRE['default']): bad.append('ROPE_CONFIG %s' % X.ROPE_PRE)
    stop = [tk.eos_token_id, tk.convert_tokens_to_ids('<|im_end|>')]
    special = sorted(set(int(i) for i in (getattr(tk, 'all_special_ids', None) or [])) |
                     {int(i) for i, t in (getattr(tk, 'added_tokens_decoder', None) or {}).items() if getattr(t, 'special', False)})
    if any(s_ is None for s_ in stop) or not set(stop) <= set(special): bad.append('STOP_IDS_NOT_IN_SPECIAL_IDS %s' % stop)
    obs = {str(o): list(tk(OBS_TEMPLATE.format(o=o), add_special_tokens=False).input_ids) for o in (0, 1)}
    if len(obs['0']) != len(obs['1']) or set(obs['0'] + obs['1']) & set(special): bad.append('OBS_IDS')
    if any(tk.decode(v) != OBS_TEMPLATE.format(o=k) for k, v in obs.items()): bad.append('OBS_DECODE_ROUNDTRIP')
    canon_p = {e: list(tk('ACQUIRE(PROBE_A,EXPECT=%d)' % e, add_special_tokens=False).input_ids) for e in (0, 1)}
    if len(canon_p[0]) != len(canon_p[1]): bad.append('CANONICAL_PREDICTIONS_UNEQUAL_LENGTH %s' % {k: len(v) for k, v in canon_p.items()})
    for w, c in CUES.items():
        if any(x in c.lower() for x in FORBIDDEN_CUE_WORDS): bad.append('CUE_FORBIDDEN_WORD ' + w)
    if CUES['X'] == CUES['Y']: bad.append('XY_ILL_POSED_IDENTICAL_INITIAL_INPUT')
    enc = lambda q: list(tk(m.SUFFIX_HEAD + q + m.SUFFIX_TAIL, add_special_tokens=False).input_ids)
    surf, sbad = surface_tokinfo(enc, X.DECOY_CAT, X.CAT['pred'], X.CAT['obs']); bad += sbad
    hand = {h: list(tk(h, add_special_tokens=False).input_ids) for h in HANDLES.values()}
    for txt in ('ACCEPT(A)', 'ACCEPT(B)', 'READ_ADD(%s)' % HANDLES['pred'], 'REVISE(R1,CITES[%s,%s],"x")' % (HANDLES['pred'], HANDLES['obs'])):
        ids = list(tk(txt, add_special_tokens=False).input_ids)
        if tk.decode(ids) != txt or len(ids) > MAX_COMPILE or parse_action(tk.decode(ids))['op'] == 'INVALID': bad.append('GRAMMAR_ROUNDTRIP %r' % txt)
    nl = list(tk('\n', add_special_tokens=False).input_ids)
    X.TOKINFO = dict(surf, special_ids=special, stop_ids=stop, obs_ids=obs, canonical_prediction_ids={str(k): v for k, v in canon_p.items()}, handle_ids=hand,
                     pad_id=nl[0] if len(nl) == 1 else None)
    X.PLACEBO = surf['placebo']
    gate('GATE_TOKENIZER_908', 'PASS' if not bad else 'FAIL', None if not bad else {'problems': bad}, **{k: v for k, v in X.TOKINFO.items() if k != 'special_ids'},
         special_ids=len(special))
    del tk


def build_manifest():
    """everything the panel will do and every rule that scores it, sealed (file + SHA) before the model is loaded."""
    return {'test': TAG, 'revision': REVISION, 'label': LABEL, 'sources': {'906': SRC906, '903': SRC903, '904': SRC904, 'engine_blobs': ENGINE_BLOBS_908},
            'derived_from': SRC907A, 'run_906': RUN906, 'run_907A': RUN907A, 'task_text': TASK_TEXT, 'task_text_sha256': TASK_TEXT_SHA256,
            'design_sha256': DESIGN_SHA256, 'design': design_view(), 'cues': CUES, 'truth': TRUTH, 'answer': ANSWER, 'obs_ids': X.TOKINFO['obs_ids'],
            'special_ids': X.TOKINFO['special_ids'], 'stop_ids': X.TOKINFO['stop_ids'],
            'catalog_entries': {'decoy': X.DECOY_CAT, 'pred': X.CAT['pred'], 'obs': X.CAT['obs']},
            'decoy_object': {k: X.OBJ['ARCHIVE/DECOY'][k] for k in ('cid', 'sha256', 'tensor_seal_sha256', 'kind', 'n', 'body_tokens')},
            'q0_sha256': X.TOKINFO['q0_sha256'], 'q0_ids_sha256': X.TOKINFO['q0_ids_sha256'], 'q_pre_ids_sha256': X.TOKINFO['q_pre_ids_sha256'],
            'qF_tokens': X.TOKINFO['qF_tokens'], 'placebo': X.TOKINFO['placebo'], 'budget': BUDGET,
            'q_id_evidence': ('every decision stores q_ids (pinned tokenizer, live); offline replay recomputes q_ids_sha256 / q_tokens / '
                              'first_generated_position = mount_tokens + q_tokens from them; independent pre-model tokenizer evidence: q0_ids_sha256, '
                              'q_pre_ids_sha256 (every pre-prediction state), qF_tokens (every ordered W with PRED and OBS)'),
            'suffix': {'head': M3.SUFFIX_HEAD, 'tail': M3.SUFFIX_TAIL}, 'decision': 'pinned 906 compile_z: fresh mount_sealed(W) + 709 answer() greedy, 65 ids max, DecodeTap',
            'cue_rule': CUE_RULE, 'avail_rule': AVAIL_RULE,
            'avail_diagnostic': ('at the FIRST decision of a world whose availability is CONSUMED (the first post-commit decision), after the real (A+) '
                                 'decision: ONE greedy decision on the same mount keys (same W, catalog, task, cue state), q identical except the '
                                 'availability value replaced by the sealed placebo; never dispatched, environment locked, W / catalog / handle map '
                                 'unchanged, not an arm, not in any verdict denominator; position_controlled iff equal q length, one differing id '
                                 'window <= %d, equal first_generated_position and equal mount seal / keys, else POSITION_CONFOUNDED_DIAGNOSTIC' % PLACEBO_WINDOW_MAX),
            'fork_rule': 'F = the first decision index after which PRED and OBS are both in W by the model\'s own READ_ADD commands; snapshot before the next generation',
            'prefix_rule': ('per world <= %d native decisions; INVALID / unknown handle / capacity / READ_DEL of an absent handle end the prefix (fail closed, '
                            'no retry); duplicate READ_ADD is a no-op; a second ACQUIRE (no second environment call, no automatic READ, no repair), WRITE, '
                            'REVISE, ACCEPT or STOP before F ends the prefix; the NOTE (cue) lives until PRED_SEALED (CUE_RULE)' % MAX_PREFIX_CALLS),
            'arms': {'names': list(ARM_NAMES), 'q': 'q_F of the world for every arm (only the physical mount differs)', 'precondition': 'XY pair reached and both forks reached',
                     'PRED_CROSS': 'other world PRED in the same slot; run only with equal n and pos0 (else NOT_RUN_GEOMETRY_NOT_EXCHANGEABLE)',
                     'FILE_SHAM': 'every W object copied to an alias file with another book id (tensor seal equal, file SHA different)', 'one_step': True},
            'fullref_rule': fullref_trigger.__doc__.strip(), 'fullref_object': 'one forge on the empty prefix of PRED ids + OBS ids in the native W relative order; diagnostic only',
            'classification': classify_action.__doc__.strip(), 'verdict_rules': VERDICT_RULES_908, 'verdict_labels': list(VERDICT_LABELS),
            'trap_1': ('identical input + greedy decoding = identical output. TEST907A r2 dropped the cue after step 0 and predicted at step 1 with '
                       'q1(X) == q1(Y) and the same mount: equal EXPECT was forced. TEST908 keeps the NOTE in q until this world\'s PRED_SEALED '
                       'event; q_pre_ids_sha256 (pre-model) proves every pre-prediction input differs X vs Y; the cue never enters a cartridge and '
                       'q_F must be byte-identical X vs Y. Equal EXPECT with different inputs = XY_PAIR_NOT_REACHED (nothing retried or assigned); '
                       'equal inputs at the ACQUIRE decisions = PRED_INPUT_COLLAPSE.'),
            'trap_2': 'BOTH_NATIVE mounts the native W order; ORDER_REV is its reverse; different native orders in X and Y are ORDER_NOT_EXCHANGEABLE (never sorted).',
            'trap_3': ('the dependent variable is the contradiction / confirmation distinction (REVISE citing PRED+OBS vs ACCEPT(B)), not the final answer: B is '
                       'correct in both worlds and is inferable from the observation alone; a single-source arm showing the pattern is NO_GAIN.'),
            'limitations': ['catalog-order permutation is not run on GPU (count binding); addressing is a precondition, not the claim',
                            'one environment action (PROBE_A) per world; a second ACQUIRE is out of scope (no second environment call)',
                            'REVISE content is not scored; REVISE writing / re-reading / STOP are TEST909+',
                            'an A+/A- action difference is a one-step surface effect, not learning, retrieval or a fork',
                            'a Colab !python child process cannot mount Drive (mount it before, or use %run)']}


def manifest_gate():
    man = build_manifest()
    b = json.dumps(man, indent=1, sort_keys=True, default=list).encode(); p = ROOT / 'TEST908_manifest.json'; p.write_bytes(b)
    X.MAN_SHA = sha_b(b); X.MAN_PATH = p
    pre = man['q_pre_ids_sha256']
    ok = (address_identifiable(man) and len(ARM_NAMES) == 7 and BUDGET['greedy_sequences_max'] == 30 and BUDGET['generated_ids_max'] == 30 * COMPILE_PROBE
          and man['q0_sha256']['X'] != man['q0_sha256']['Y'] and all(pre['X'][k] != pre['Y'][k] for k in pre['X'])
          and man['placebo']['value'] in PLACEBO_CANDIDATES and len(man['qF_tokens']) == 8)
    gate('GATE_MANIFEST_908', 'PASS' if ok else 'FAIL', None if ok else 'manifest design', sha256=X.MAN_SHA, written_before_model=True,
         placebo=man['placebo'])
    del man


# ===================================================================================================== physical layer (pinned 906 / 903 functions)
def ev908(br, kind, **data):
    """one event: global append-only stream (903 ev, seq index) + the branch's own list. Returns the event index."""
    i = int(M3.EVSEQ[0]); M3.ev(kind, branch=br.bid if br is not None else None, **data)
    if br is not None: br.events.append(dict(index=i, kind=kind, **{k: v for k, v in data.items() if k in ('cell_id', 'key', 'sha256', 'action', 'outcome', 'handles')}))
    return i


def save_object(cp, key, where, meta):
    """append-only, read-only file of one created cartridge (906 save_obj / _save_child logic, 908 names, branch namespace)."""
    m = M3; where.mkdir(parents=True, exist_ok=True); path = where / ('T908_%s.pt' % key.replace('/', '_')); tmp = Path(str(path) + '.tmp')
    if path.exists(): raise Stop908('APPEND_ONLY ' + str(path))
    raw = cp['h'].numel() * cp['h'].element_size() + sum(k.numel() * k.element_size() + v.numel() * v.element_size() for k, v in cp['lower'])
    m.torch.save(cp, tmp); tmp.replace(path); os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    seal = m.seal_cp(cp)
    ent = dict(meta, key=key, cid='T908_' + key.replace('/', '_'), file=str(path), sha256=sha_file(path), bytes=path.stat().st_size, kind='CHILD', n=int(cp['n']),
               body_tokens=int(cp['body_tokens']), pos0=int(cp['pos0']), tensor_seal=seal, tensor_seal_sha256=jsha(seal), raw_bytes=raw, created=True)
    if ent['bytes'] > M6.TOL906['file_bytes_max_factor'] * raw + M6.TOL906['file_bytes_slack']: raise Stop908('OBJECT_FILE_BYTES ' + key)
    m.CART_INDEX.append(ent); X.OBJ[key] = ent; R['objects'][key] = {k: v for k, v in ent.items() if k not in ('tensor_seal', 'geometry')}
    M3.ev('OBJECT', entry={k: v for k, v in ent.items() if k not in ('tensor_seal', 'geometry')}); return ent


def forge_on_empty(ids, key, where, meta):
    """906 forge_z([], ids): fresh empty-prefix mount (30 rows), only ids forwarded at 30..30+m-1; H3 + L0-L3 rows of ids."""
    cp, geo, ms, n0 = M6.forge_z([], list(ids), 'T908_%s_%s' % (RUN_ID, key.replace('/', '_')))
    sch = M3.child_schema(cp)
    if not sch['ok'] or n0 != P_PREFIX or int(cp['pos0']) != P_PREFIX or int(cp['n']) != len(ids) or ms != X.EMPTY_MOUNT_SEAL:
        raise Stop908('FORGE_ON_EMPTY %s schema=%s n0=%s pos0=%s n=%s empty_mount_equal=%s' % (key, sch['ok'], n0, cp['pos0'], cp['n'], ms == X.EMPTY_MOUNT_SEAL))
    ent = save_object(cp, key, where, dict(meta, ids_sha256=sha_s(json.dumps(list(ids))), parents=[], parent_mount_seal_sha256=ms, geometry=geo)); del cp
    M3.load_record(ent)                                                    # file SHA + tensor seal re-read from disk
    return ent


def decide(br, q, cell_id, phase, keyed):
    """one native decision on a FRESH mount of the given (handle, object key) slots: pinned 906 compile_z (709 answer() greedy,
    65 ids max, DecodeTap exact ids, mount unchanged, guards); then compile_status, exact decode of the ids, strict parse."""
    ents = [X.OBJ[k] for _, k in keyed]; sl, tot = slots_of(ents)
    i = ev908(br, 'DECISION_BEGIN', cell_id=cell_id)
    ids, raw, info = M6.compile_z(ents, q)
    if info['mount_tokens'] != tot: raise Stop908('MOUNT_GEOMETRY %s %s != %s' % (cell_id, info['mount_tokens'], tot))
    st, why = compile_status(ids, X.TOKINFO['special_ids'])
    decoded = M3.tok.decode(ids) if st == 'VALID' else None
    act = parse_action(decoded) if st == 'VALID' else {'op': 'INVALID', 'why': 'COMPILE_STATUS_%s:%s' % (st, why)}
    qids = list(M3.tok(M3.SUFFIX_HEAD + q + M3.SUFFIX_TAIL, add_special_tokens=False).input_ids)
    gen = len(ids) + (1 if len(ids) < COMPILE_PROBE else 0); br.counters['decisions'] += 1; br.counters['generated_ids'] += gen
    rec = {'cell_id': cell_id, 'world': br.world, 'branch_id': br.bid, 'phase': phase, 'event_index': i, 'q': q, 'q_sha256': sha_s(q), 'q_ids': qids, 'q_ids_sha256': sha_s(json.dumps(qids)),
           'q_tokens': len(qids), 'ws_before': list(br.ws), 'mounted_handles': [h for h, _ in keyed],
           'mount': {'keys': [[h, k] for h, k in keyed], 'trace': _keyset(keyed, R['objects']), 'slots': sl, 'mount_tokens': info['mount_tokens'],
                     'mount_seal_sha256': info['mount_seal_sha256'], 'first_generated_position': info['mount_tokens'] + len(qids)},
           'gen_ids': ids, 'gen_ids_sha256': sha_s(json.dumps(ids)), 'n_generated': gen, 'raw': raw, 'decoded': decoded, 'compile_status': st, 'status_reason': why,
           'action': act, 'decide_s': info.get('compile_s'), 't_s': round(time.perf_counter() - T0, 1)}
    X.NSEQ = getattr(X, 'NSEQ', 0) + 1; X.NGEN = getattr(X, 'NGEN', 0) + gen
    if X.NSEQ > BUDGET['greedy_sequences_max'] or X.NGEN > BUDGET['generated_ids_max']: raise Stop908('BUDGET_ABORT sequences %d ids %d' % (X.NSEQ, X.NGEN))
    M3.ev('DECISION', cell_id=cell_id, branch=br.bid, ids_sha256=rec['gen_ids_sha256'], mount=info['mount_seal_sha256'], op=act.get('op'))
    log('DECIDE %-26s W=%-16s -> %-10s %r' % (cell_id, ','.join(br.ws) or '()', act.get('op'), (raw or '')[:90])); M3.save(False)
    return rec


def seal_prediction_and_observe(br, rec, act):
    """t1 PRED forge of the EXACT decision ids on the empty prefix -> written + re-read (SHA, tensor seal) -> t2 environment with
    the action name only -> t3 OBS forge of the template of the outcome on the empty prefix (PRED not mounted) -> t4 catalog."""
    w = br.world; e = {}
    e['pred_begin'] = ev908(br, 'PRED_SEAL_BEGIN', cell_id=rec['cell_id'])
    ep = forge_on_empty(rec['gen_ids'], '%s/PRED' % w, br.dir, {'role': 'PRED', 'world': w, 'decision_cell': rec['cell_id'], 'expect': act['expect'],
                                                                  'origin': 'MODEL'})
    e['pred_sealed'] = ev908(br, 'PRED_SEALED', key=ep['key'], sha256=ep['sha256'])
    if cue_live(br.events) or br.events[-1].get('kind') != 'PRED_SEALED': raise Stop908('ENV_BEFORE_PRED_SEAL ' + w)   # 908: order guard
    outcome = br.env.step(act['action'])
    e['env_executed'] = ev908(br, 'ENV_EXECUTED', action=act['action'], outcome=outcome)
    ids_o = X.TOKINFO['obs_ids'][str(outcome)]
    eo = forge_on_empty(ids_o, '%s/OBS' % w, br.dir, {'role': 'OBS', 'world': w, 'outcome': outcome, 'origin': 'ENV', 'cause_event': e['env_executed']})
    e['obs_sealed'] = ev908(br, 'OBS_SEALED', key=eo['key'], sha256=eo['sha256'])
    br.catalog += [dict(X.CAT['pred']), dict(X.CAT['obs'])]; br.hmap[HANDLES['pred']] = ep['key']; br.hmap[HANDLES['obs']] = eo['key']
    e['catalog_commit'] = ev908(br, 'CATALOG_COMMIT', handles=[HANDLES['pred'], HANDLES['obs']])
    return {'result': 'ACQUIRED', 'pred_key': ep['key'], 'obs_key': eo['key'], 'outcome': outcome, 'events': e, 'ws_after': list(br.ws)}


def run_prefix(w):
    """the native trajectory of one world up to F (or its native end); nothing is completed, sorted or retried by the harness. (908)
    q of every decision = build_q(task, cue while cue_live(events), availability(events), catalog, W); at the first decision whose
    availability is CONSUMED the A- diagnostic runs once (avail_diagnostic; never dispatched)."""
    br = Branch('%s/NATIVE' % w, w, (), [X.DECOY_CAT], Env908(TRUTH), {HANDLES['decoy']: 'ARCHIVE/DECOY'}, ROOT / 'branches' / w / 'NATIVE')
    P = {'world': w, 'decisions': [], 'end': None, 'fork': None, 'env_calls': 0, 'avail_diag': None}; acquired = False; X.BR[w] = br
    for step in range(MAX_PREFIX_CALLS):
        kappa = cue_live(br.events); alpha = availability(br.events)
        q = build_q(TASK_TEXT, CUES[w] if kappa else None, alpha, br.catalog, br.ws)
        rec = decide(br, q, 'T908/%s/PREFIX/%02d' % (w, step), 'PREFIX', [(h, br.hmap[h]) for h in br.ws]); rec.update(cue_live=kappa, avail=alpha)
        P['decisions'].append(rec)
        if alpha == AVAIL_STATES[1] and P['avail_diag'] is None: P['avail_diag'] = avail_diagnostic(br, rec)
        act = rec['action']; op = act['op']
        if op == 'INVALID': rec['dispatch'] = {'result': 'INVALID'}; P['end'] = 'INVALID_NATIVE_ACTION:%s' % act['why']; break
        if op in ('READ_ADD', 'READ_DEL', 'READ_CLEAR'):
            ws2, res = ws_apply(br.ws, act, {e['handle'] for e in br.catalog}); rec['dispatch'] = {'result': res, 'ws_after': list(ws2)}
            if res.endswith('_INVALID'): P['end'] = res; break
            br.ws = ws2
            if fork_condition(br.ws):
                P['end'] = 'FORK'; qf = build_q(TASK_TEXT, CUES[w] if cue_live(br.events) else None, availability(br.events), br.catalog, br.ws)
                qids = list(M3.tok(M3.SUFFIX_HEAD + qf + M3.SUFFIX_TAIL, add_special_tokens=False).input_ids)
                prov = [i for i, d in enumerate(P['decisions']) if d['action'].get('op') == 'READ_ADD' and (d.get('dispatch') or {}).get('result') == 'WS_ADDED']
                P['fork'] = {'step': step, 'ws': list(br.ws), 'hmap': dict(br.hmap), 'catalog': copy.deepcopy(br.catalog), 'q_F': qf, 'q_F_sha256': sha_s(qf),
                             'q_F_ids': qids, 'q_F_ids_sha256': sha_s(json.dumps(qids)), 'q_F_tokens': len(qids), 'read_provenance': prov,
                             'event_index': ev908(br, 'FORK_SNAPSHOT', handles=list(br.ws)), 'env_calls': len(br.env.calls)}
                break
            continue
        if op == 'ACQUIRE':
            if acquired: rec['dispatch'] = {'result': 'OUT_OF_SCOPE_SECOND_ACQUIRE'}; P['end'] = 'OUT_OF_SCOPE_SECOND_ACQUIRE'; break
            rec['dispatch'] = seal_prediction_and_observe(br, rec, act); acquired = True; continue
        P['end'] = ('MODEL_%s_BEFORE_FORK' % op) if op in ('ACCEPT', 'STOP') else 'OUT_OF_SCOPE_%s_BEFORE_FORK' % op; rec['dispatch'] = {'result': P['end']}; break
    else:
        P['end'] = 'MAX_PREFIX_CALLS'
    P['env_calls'] = len(br.env.calls); R['branches'][br.bid] = {'events': br.events, 'counters': br.counters, 'dir': str(br.dir), 'inherited_events': br.inherited_events}
    log('PREFIX %s: %d decisions | end %s | W %s | A- %s' % (w, len(P['decisions']), P['end'], list(br.ws), (P['avail_diag'] or {}).get('raw')))
    return P


def avail_diagnostic(br, rec):
    """A- (diagnostic only) at the first post-commit decision rec (A+): ONE greedy decision on the SAME mount keys as A+ with q equal
    to A+ except the availability value = the sealed placebo. Copy-on-write branch, environment locked, never dispatched; the main
    branch's W / catalog / handle map / environment are verified unchanged (else technical stop)."""
    w = br.world; ws0, cat0, hm0, env0 = tuple(br.ws), canon(br.catalog), dict(br.hmap), Env908.TOTAL[0]
    kappa = cue_live(br.events)
    q = build_q(TASK_TEXT, CUES[w] if kappa else None, X.PLACEBO['value'], br.catalog, br.ws)
    dbr = br.fork('%s/AVAIL_MINUS' % w, ROOT / 'branches' / w / 'AVAIL_MINUS')
    a = decide(dbr, q, 'T908/%s/AVAIL/MINUS' % w, 'AVAIL_DIAGNOSTIC', [tuple(x) for x in rec['mount']['keys']])
    a.update(plus_cell=rec['cell_id'], avail='PLACEBO:' + X.PLACEBO['value'], cue_live=kappa, diagnostic_only=True, dispatched=False,
             env_calls_in_branch=Env908.TOTAL[0] - env0)
    a['position_controlled'] = position_controlled(rec, a)
    if tuple(br.ws) != ws0 or canon(br.catalog) != cat0 or dict(br.hmap) != hm0 or a['env_calls_in_branch'] != 0:
        raise Stop908('AVAIL_DIAGNOSTIC_CHANGED_THE_MAIN_STATE ' + w)
    R['branches'][dbr.bid] = {'events': dbr.events, 'counters': dbr.counters, 'dir': str(dbr.dir), 'inherited_events': dbr.inherited_events}
    log('AVAIL %s: A+ %s | A- %s | position_controlled %s' % (w, rec['action'].get('op'), a['action'].get('op'), a['position_controlled']))
    return a


def sham_copies(w, f):
    """FILE_SHAM: every W object in an alias file with another book id; tensors unchanged (seal equal), file SHA different."""
    m = M3; torch = m.torch; out = {}; d = ROOT / 'branches' / w / 'FILE_SHAM'; d.mkdir(parents=True, exist_ok=True)
    for h in f['ws']:
        src = X.OBJ[f['hmap'][h]]; key = '%s/SHAM/%s' % (w, h); dst = d / ('T908_%s.pt' % key.replace('/', '_'))
        if dst.exists(): raise Stop908('APPEND_ONLY ' + str(dst))
        obj = m.load_record(src); obj['book_id'] = 'T908_SHAM_%s_%s' % (w, h); seal = m.seal_cp(obj); torch.save(obj, dst); del obj
        os.chmod(dst, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        e = dict(src, key=key, cid='T908_' + key.replace('/', '_'), file=str(dst), sha256=sha_file(dst), bytes=dst.stat().st_size, sham_of=src['key'], created=True,
                 role='FILE_SHAM_COPY', sham_role=src.get('role'))
        if jsha(seal) != src['tensor_seal_sha256'] or e['sha256'] == src['sha256']: raise Stop908('SHAM_COPY ' + key)
        m.CART_INDEX.append(e); X.OBJ[key] = e; R['objects'][key] = {k: v for k, v in e.items() if k not in ('tensor_seal', 'geometry')}; out[src['key']] = key
    return out


def ws_rope_reference(key, ents):
    """multi-slot child mount vs an independent float64 RoPE: every layer holds 30 + sum m rows; prefix rows bit-equal to the empty
    mount; per slot, L0-L3 V rows bit-equal to the stored V and K rows = stored K moved source -> target once (cos >= 906 tolerance);
    moved twice is a diagnostic. Upper layers are rebuilt by the engine and are not compared (no reference exists)."""
    import numpy as np
    m = M3; torch = m.torch; sl, tot = slots_of(ents)
    t_ = time.perf_counter(); mem = m.mount_sealed(ents); M6._guard('append', time.perf_counter() - t_)
    t_ = time.perf_counter(); emp = m.mount_sealed([]); M6._guard('append', time.perf_counter() - t_)
    rows_ok = all(int(k.shape[-2]) == tot and int(v.shape[-2]) == tot for k, v in mem) and len(mem) == len(emp)
    prefix_ok = all(torch.equal(a[:, :, :P_PREFIX, :], c) and torch.equal(b[:, :, :P_PREFIX, :], d) for (a, b), (c, d) in zip(mem, emp))
    worst, dbl, v_ok = 1.0, -1.0, True
    for e, s in zip(ents, sl):
        cp = m.load_record(e); off = 0 if e['kind'] == 'CHILD' else P_PREFIX; src = list(range(s['source_pos0'], s['source_pos0'] + s['m']))
        dst = list(range(s['target_pos0'], s['target_pos0'] + s['m']))
        for li in range(4):
            ks, vs = cp['lower'][li]; ks = ks[:, :, off:off + s['m'], :]; vs = vs[:, :, off:off + s['m'], :]
            km = mem[li][0][:, :, s['target_pos0']:s['target_pos0'] + s['m'], :].float().cpu().numpy(); vm = mem[li][1][:, :, s['target_pos0']:s['target_pos0'] + s['m'], :]
            ref = M6.rope_move_np(ks.float().numpy().astype(np.float64), src, dst, X.ROPE_THETA, m.HD)
            worst = min(worst, M6.cos_np(km, ref)); v_ok = v_ok and torch.equal(vm.cpu(), vs.to(vm.dtype))
            if src != dst: dbl = max(dbl, M6.cos_np(km, M6.rope_move_np(ref, src, dst, X.ROPE_THETA, m.HD)))
        del cp
    ms = m.jsha(m.full_kv_seal(mem)); del mem, emp; m.release()
    ok = rows_ok and prefix_ok and v_ok and worst >= M6.TOL906['rope_reference_cos_min']
    r = {'mount': key, 'slots': sl, 'rows_all_layers': rows_ok, 'prefix_bitwise': prefix_ok, 'v_unchanged_bitwise': v_ok, 'min_cos_single_vs_reference': worst,
         'max_cos_vs_double_DIAGNOSTIC': dbl, 'mount_seal_sha256': ms, 'ok': ok}
    R['rope_reference'].append(r); return r


def ws_abi_gate():
    """before the panel, on archived 903 objects (no experiment object exists yet): ordered two-child mounts in both orders and a
    NATIVE+CHILD mount against the float64 RoPE reference, a repeat mount (exact fresh reload), the empty-prefix mount seal, the
    pinned decision budget, engine blobs, DynamicCache API, compile_status equal to 906, and the 908 decision-path isolation."""
    m = M3; g = X.GROUPS[tuple(DECOY_SOURCE['group'])]; G = {}
    t_ = time.perf_counter(); emp = m.mount_sealed([]); M6._guard('append', time.perf_counter() - t_); X.EMPTY_MOUNT_SEAL = m.jsha(m.full_kv_seal(emp)); del emp; m.release()
    a, b, d = g['C1_H1'], g['C1_HG'], g['E_IND']
    for x in (a, b, d): x.setdefault('tensor_seal_sha256', jsha(x['tensor_seal']))
    r1 = ws_rope_reference('ABI/C1_H1+C1_HG', [a, b]); r2 = ws_rope_reference('ABI/C1_HG+C1_H1', [b, a]); r3 = ws_rope_reference('ABI/E_IND+C1_H1', [d, a])
    r4 = ws_rope_reference('ABI/C1_H1+C1_HG#repeat', [a, b])
    G.update(two_child_order_ab=r1['ok'], two_child_order_ba=r2['ok'], native_plus_child=r3['ok'], repeat_mount_bitwise=r1['mount_seal_sha256'] == r4['mount_seal_sha256'],
             order_changes_physical_mount_DIAGNOSTIC=r1['mount_seal_sha256'] != r2['mount_seal_sha256'])
    G['decision_budget_is_906'] = M6.COMPILE_PROBE == COMPILE_PROBE == 65 and M6.MAX_COMPILE == MAX_COMPILE == 64
    G['engine_blobs_equal_903'] = dict(m.ENGINE_BLOBS) == ENGINE_BLOBS_908
    G['dynamic_cache_api'] = all(hasattr(m.DynamicCache, x) for x in ('update', 'get_seq_length'))
    G['transformers_major_5'] = str(m.transformers.__version__).split('.')[0] == '5'
    G['compile_status_equal_906'] = _same_function(compile_status, M6.compile_status)
    G['suffix_is_709'] = (m.SUFFIX_HEAD + 'Q' + m.SUFFIX_TAIL) == '\nQUESTION:\nQ\n\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n'
    iso = decision_path_isolation(); G['decision_path_isolated'] = iso['ok']; X.DP_ISOLATION_OK = iso['ok']
    G['isolation_906_ok'] = bool(getattr(X, 'ISOLATION_OK', False))
    fail = [k for k, v in G.items() if isinstance(v, bool) and not k.endswith('_DIAGNOSTIC') and v is not True]
    R['empty_mount_seal_sha256'] = X.EMPTY_MOUNT_SEAL
    gate('GATE_WS_ABI_908', 'PASS' if not fail else 'FAIL', None if not fail else 'failed: %s' % fail, checks=G, isolation=iso, empty_mount_seal_sha256=X.EMPTY_MOUNT_SEAL)


def _same_function(f, g):
    import ast, inspect, textwrap
    try: return ast.dump(ast.parse(textwrap.dedent(func_src(f)))) == ast.dump(ast.parse(textwrap.dedent(inspect.getsource(g))))
    except Exception: return False


def run_arms():
    """7 one-step arms per world from the F snapshot (copy-on-write branches, environment locked, q = q_F)."""
    X.SHAM = {w: sham_copies(w, R['prefix'][w]['fork']) for w in WORLDS}; R['sham_map'] = X.SHAM
    for w in WORLDS:
        f = R['prefix'][w]['fork']; fo = R['prefix'][OTHER_WORLD[w]]['fork']; base = X.BR[w]; R['arms'][w] = {}
        for a in ARM_NAMES:
            br = base.fork('%s/ARM/%s' % (w, a), ROOT / 'branches' / w / a); cid = 'T908/%s/ARM/%s' % (w, a)
            if a == 'PRED_CROSS':
                pm, qm = X.OBJ[f['hmap'][HANDLES['pred']]], X.OBJ[fo['hmap'][HANDLES['pred']]]
                if not (pm['n'] == qm['n'] and pm['pos0'] == qm['pos0']):
                    R['arms'][w][a] = {'cell_id': cid, 'arm': a, 'one_step': True, 'branch_id': br.bid, 'status': 'NOT_RUN_GEOMETRY_NOT_EXCHANGEABLE', 'env_calls_in_branch': 0}
                    log('ARM %s -> NOT_RUN (PRED lengths %s / %s)' % (cid, pm['n'], qm['n'])); continue
            keyed = arm_keys(a, tuple(f['ws']), f['hmap'], fo['hmap'], X.SHAM[w]); env0 = Env908.TOTAL[0]
            ents = [X.OBJ[k] for _, k in keyed]
            if ents: rr = ws_rope_reference('%s/%s' % (w, a), ents)
            else: rr = {'ok': True}
            if not rr['ok']: gate('GATE_ARMS_908', 'FAIL', 'arm mount geometry / RoPE failed: %s' % rr)
            rec = decide(br, f['q_F'], cid, 'ARM', keyed)
            rec.update(arm=a, one_step=True, status='READ', env_calls_in_branch=Env908.TOTAL[0] - env0, rope_ok=rr['ok'])
            R['arms'][w][a] = rec; R['branches'][br.bid] = {'events': br.events, 'counters': br.counters, 'dir': str(br.dir), 'inherited_events': br.inherited_events}


def run_fullref():
    """pre-registered trigger (manifest read back, after every arm is sealed): one continuous forge of PRED+OBS ids per world."""
    b = X.MAN_PATH.read_bytes()
    if sha_b(b) != X.MAN_SHA: raise Stop908('MANIFEST_CHANGED')
    man = json.loads(b); R['main_generation_sealed_sha256'] = generation_seal(R)
    S = {w: prefix_summary(R['prefix'][w]) for w in WORLDS}; trig = fullref_trigger(man, R, roles_of(S)) if roles_of(S) and all(S[w]['fork'] for w in WORLDS) else []
    for w in trig:
        f = R['prefix'][w]['fork']; br = X.BR[w].fork('%s/FULLREF' % w, ROOT / 'branches' / w / 'FULLREF')
        acq = [d for d in R['prefix'][w]['decisions'] if (d.get('dispatch') or {}).get('result') == 'ACQUIRED'][0]
        ids = fullref_ids(f['ws'], acq['gen_ids'], man['obs_ids'][str(man['truth']['A'])])
        ent = forge_on_empty(ids, '%s/FULLREF' % w, br.dir, {'role': 'FULLREF_DIAGNOSTIC', 'world': w, 'origin': 'DIAGNOSTIC'})
        rec = decide(br, f['q_F'], 'T908/%s/FULLREF' % w, 'FULLREF', [('FULLREF', ent['key'])])
        rec.update(status='READ', diagnostic_only=True); R['fullref'][w] = rec
        R['branches'][br.bid] = {'events': br.events, 'counters': br.counters, 'dir': str(br.dir), 'inherited_events': br.inherited_events}
    del man
    gate('GATE_FULLREF_908', 'PASS' if len(R['fullref']) <= BUDGET['fullref_reads_max'] else 'FAIL', None, triggered=trig)


def run_panel():
    X.BR = {}; X.NSEQ = 0; X.NGEN = 0; Env908.TOTAL[0] = 0
    for w in WORLDS: R['prefix'][w] = run_prefix(w)
    S = {w: prefix_summary(R['prefix'][w]) for w in WORLDS}
    ok = all(P['end'] is not None for P in R['prefix'].values()) and all(P['env_calls'] <= 1 for P in R['prefix'].values())
    gate('GATE_PREFIX_908', 'PASS' if ok else 'FAIL', None if ok else 'prefix record incomplete', summary=S)
    AD = {w: R['prefix'][w].get('avail_diag') for w in WORLDS}
    okA = (all(a is None or (a.get('env_calls_in_branch') == 0 and a.get('dispatched') is False and a.get('diagnostic_only') is True) for a in AD.values())
           and sum(1 for a in AD.values() if a) <= BUDGET['avail_diagnostic_max'] and Env908.TOTAL[0] == sum(P['env_calls'] for P in R['prefix'].values()))
    gate('GATE_AVAIL_908', 'PASS' if okA else 'FAIL', None if okA else 'A- diagnostic dispatched or over budget', placebo=X.PLACEBO,
         diagnostics={w: None if a is None else {'plus_cell': a.get('plus_cell'), 'op': (a.get('action') or {}).get('op'), 'position_controlled': a.get('position_controlled')} for w, a in AD.items()})
    if roles_of(S) is not None and all(S[w]['fork'] for w in WORLDS): run_arms()
    else: log('ARMS NOT RUN (pre-registered precondition): roles %s, forks %s' % (roles_of(S), {w: S[w]['fork'] for w in WORLDS}))
    n = sum(len(v) for v in R['arms'].values())
    gate('GATE_ARMS_908', 'PASS' if n in (0, 2 * len(ARM_NAMES)) else 'FAIL', None if n in (0, 14) else 'arms %d' % n, arms=n,
         rope_ok=all(r['ok'] for r in R['rope_reference']), scientific_note='arms=0 is technical accounting only, never a scientific success')
    run_fullref()


def end_gate():
    mm = M3; torch = mm.torch
    created = [o for o in X.OBJ.values() if o.get('created')]
    G = {'sentinel_equal': mm.sentinel() == X.W0['sentinel'], 'integrity_equal': mm.integrity_digest(mm.base_params, mm.Q4MODS, mm.BUFS)['sha256'] == X.W0['integrity']['sha256'],
         'hooks_clean': mm.hooks_clean(mm.hook_inventory()), 'files_unchanged': all(sha_file(e['file']) == e['sha256'] for e in mm.CART_INDEX),
         'greedy_sequences_within_30': X.NSEQ <= BUDGET['greedy_sequences_max'], 'generated_ids_within_1950': X.NGEN <= BUDGET['generated_ids_max'],
         'env_calls_within_2': sum(P['env_calls'] for P in R['prefix'].values()) == Env908.TOTAL[0] <= BUDGET['env_calls'],
         'avail_diagnostics_within_2': sum(1 for P in R['prefix'].values() if P.get('avail_diag')) <= BUDGET['avail_diagnostic_max'],
         'pred_obs_forges_within_4': sum(1 for o in created if o.get('role') in ('PRED', 'OBS')) <= BUDGET['pred_forges'] + BUDGET['obs_forges'],
         'fullref_forges_within_2': sum(1 for o in created if o.get('role') == 'FULLREF_DIAGNOSTIC') <= BUDGET['fullref_forges_max'],
         'created_bytes_within_16MiB': sum(o['bytes'] for o in created) <= BUDGET['created_object_bytes_max'],
         'drive_only_after_a100': X.DRIVE_VIOLATION is None and drive_after_a100(read_events(EVENTS) or [])}
    M6._guard('end')                                                   # final wall / GPU peak / CPU RAM / cartridge bytes, BEFORE any PASS
    peak = torch.cuda.max_memory_allocated() / 2**30; G['gpu_peak_within_abort'] = peak <= mm.ABORT['gpu_peak_gib'] == BUDGET['gpu_peak_abort_gib']
    ok = all(G.values()); gate('GATE_END_908', 'PASS' if ok else 'FAIL', None if ok else [k for k, v in G.items() if not v], gpu_peak_gib=round(peak, 2),
                               abort_limits=dict(mm.ABORT), **G)


def write_verdict():
    b = X.MAN_PATH.read_bytes()
    if sha_b(b) != X.MAN_SHA: raise Stop908('MANIFEST_CHANGED')
    man = json.loads(b); R['manifest_sha256'] = X.MAN_SHA
    gates_ok, gate_why = required_gate_status(R['gates'], R['technical_blockers'], events=read_events(EVENTS) or [])
    R['required_gate_problems'] = gate_why
    R['generation_sealed_sha256'] = generation_seal(R)
    iso = isolation_from_gates(R['gates']) and bool(getattr(X, 'DP_ISOLATION_OK', False)) and bool(getattr(X, 'ISOLATION_OK', False))
    ev = evaluate_908(man, R, gates_ok, isolation_ok=iso, technical_why=gate_why)
    probs = verify_run_record(dict(R, status='COMPLETE', evaluation=None), b, ev)
    R['event_chain_problems'] = event_chain_problems(R, read_events(EVENTS) or [])          # 908 r2 (P2-2): live replay of the event log
    probs = probs + ['EVENT_CHAIN:' + x for x in R['event_chain_problems']]
    tv = 'PASS' if gates_ok and not ev['integrity_problems'] and not probs and iso else 'TECHNICAL_UNDECIDABLE'
    if tv != 'PASS':                                                                           # 908 r2 (P3-2): one atomic verdict
        if not ev['verdict'].startswith(('TECHNICAL_MISMATCH', 'GPU_REQUIRED')): ev['verdict'] = 'TECHNICAL_MISMATCH[%s]' % ('; '.join((probs + gate_why)[:3]) or 'gates')
        ev['scientific'] = {'verdict': ev['verdict'], 'withheld_DIAGNOSTIC': (ev.get('scientific') or {}).get('verdict')}
        ev['evaluable'] = {'ok': False, 'why': 'technical'}
    R.update(evaluation=ev, technical_verdict=tv, run_record_problems=probs)
    R['top'].update(technical_verdict=tv, verdict=ev['verdict'], integrity_problems=ev['integrity_problems'][:50] + probs,
                    availability_diagnostic={w: (ev['availability_diagnostic'].get(w) or {}).get('label') for w in WORLDS})
    L = report_lines(ev) + (['RUN RECORD: ' + '; '.join(probs)] if probs else [])
    (ROOT / 'TEST908_verdict.txt').write_text('\n'.join(L) + '\nRecompute: python 908.py --recompute TEST908_results.json\n')
    for l in L: log(l)
    return tv


def gpu_main(cfg):
    global M3, M4, m3, M6
    work = ROOT / 'sources'; work.mkdir()
    X.STAGED_BYTES = None; X.OBJ = {}; ident, b = executed_source_identity(cfg=cfg); R['executed_source'] = ident; X.SELF_BYTES = b
    if b is not None:
        (work / 'TEST908_executed_908.py').write_bytes(b)
        ident['executed_file_sha256'] = sha_b(b); ident['executed_file_git_blob'] = blob_b(b)
    if b is not None and X.STAGED_BYTES is not None: (work / 'TEST908_staged_908.py').write_bytes(X.STAGED_BYTES)
    p6 = fetch_source(cfg, work, SRC906); p3 = fetch_source(cfg, work, SRC903); p4 = fetch_source(cfg, work, SRC904)      # GitHub / network only, no Drive
    M4 = load_module(p4, 'akbas_test904_engine'); M3 = m3 = M4.load_903(p3); M6 = load_module(p6, 'akbas_test906_engine'); bind_engine()
    if M4.TAG != 'TEST904' or M4.R is not None or M6.TAG != 'TEST906' or M6.REVISION[:2] != 'r2' or M6.RUN_ID != RUN_ID: raise Stop908('MODULE_STATE')
    M3.log('=' * 112); M3.log(MARKER, '| run', RUN_ID, '|', LABEL)
    gate('GATE_SOURCES_908', 'PASS', None, src906=SRC906, src903=SRC903, src904=SRC904, derived_from=SRC907A, reused_906=list(REUSED_906),
         modules_main_not_run=M3.R is R and M4.R is None)
    how = ('Paste the WHOLE 809.py into ONE EMPTY Colab cell and run only that cell; NO /content/908.py staging is needed'
           if ident.get('execution_mode') == 'NOTEBOOK_CELL' else 'Save 809.py as %s and start it in its own __main__: %%run %s (kernel; Drive '
           'auto-mount after A100 pre-flight) or !python %s (mount Drive beforehand)' % (REPO_908, REPO_908, REPO_908))
    gate('GATE_EXECUTED_SOURCE', 'PASS' if b is not None else 'FAIL', None if b is not None else
         '%s [%s; mode %s; checked %s]. %s' % (ident.get('method'), ident.get('reason'), ident.get('execution_mode'),
                                               [(x['path'], x.get('result')) for x in ident.get('candidates', [])], how), identity=ident)
    R['kernel_cleanup'] = kernel_cleanup(globals())
    R['status'] = 'GPU_PREFLIGHT'; M6.gpu_preflight()                   # A100 first (906 r2 function, torch only); FAIL stops here (critical gate)
    pf = (R['gates'].get('GATE_GPU_PREFLIGHT_906') or {}).get('status'); ok8, why8 = preflight_908_status(pf, X.DRIVE_OPS, X.DRIVE_VIOLATION)
    gate('GATE_GPU_PREFLIGHT_908', 'PASS' if ok8 else 'FAIL', why8, a100_gate='GATE_GPU_PREFLIGHT_906', a100_status=pf, drive_ops_before=list(X.DRIVE_OPS),
         rule='no Drive mount / probe / read / write before this gate')
    X.A100_PASS = True                                                  # from here on drive_guard() admits Drive operations
    M3.boot_runtime(); M3.env_gate(); M6.vram_gate()
    X.MOUNT = ensure_drive_908(cfg, ident.get('execution_mode')); drive_guard('drive_presence'); ok_d, why_d = M6.drive_presence(cfg)
    gate('GATE_DRIVE_PRESENT', 'PASS' if ok_d else 'FAIL', None if ok_d else
         'Drive delivery is required but %s (automatic mount: %s). A !python child process cannot mount Drive: in a notebook cell run '
         'from google.colab import drive; drive.mount("/content/drive", force_remount=True), then start 908 again (or use %%run)' % (why_d, X.MOUNT),
         state=why_d, mode=cfg.get('drive'), mount=X.MOUNT)
    drive_gate(cfg)                                                       # new MyDrive/TEST908_<run_id>: write / fsync / read-back probe
    drive_guard('archive_903')
    try: M6.archive_gate(cfg)
    except M6.Stop906 as e: gate('GATE_ARCHIVE_906', 'FAIL', str(e))
    ref906_gate(cfg); ref907a_gate(cfg)
    M3.PINNED_CALLS = []
    SRC = M3.obtain_sources(cfg, work); R['sources'] = {n: {'sha256': sha_b(x), 'git_blob': blob_b(x)} for n, x in SRC.items()}
    M3.source_extract_gate(SRC); M6.archive_tensors_gate(); bind_design()
    M3.tokenizer_pre_model_gate(); tokenizer_gate(); M6.disk_gate(); manifest_gate()   # manifest (panel, surfaces, arms, rules) BEFORE the model
    M3.model_gate(); M6.engine_gate(); ws_abi_gate()
    R['status'] = 'PANEL'; run_panel(); end_gate(); tv = write_verdict()
    R['status'] = 'COMPLETE' if tv == 'PASS' else 'TECHNICAL_INVALID'


def bind_design():
    """the decoy (archived 903 object) and the catalog metadata of the three model-facing handles (no content)."""
    d = X.GROUPS[tuple(DECOY_SOURCE['group'])][DECOY_SOURCE['archive_key']]
    X.OBJ['ARCHIVE/DECOY'] = dict(d, key='ARCHIVE/DECOY', tensor_seal_sha256=jsha(d['tensor_seal']), created=False)
    R['objects']['ARCHIVE/DECOY'] = {k: v for k, v in X.OBJ['ARCHIVE/DECOY'].items() if k not in ('tensor_seal',)}
    X.DECOY_CAT = catalog_entry(HANDLES['decoy'], 'OBS', 'ARCHIVE', 'E0', 1)
    X.CAT = {'pred': catalog_entry(HANDLES['pred'], 'PRED', 'MODEL', 'E1', 1), 'obs': catalog_entry(HANDLES['obs'], 'OBS', 'ENV', 'E1', 1, cause=HANDLES['pred'])}


def main(argv=None):
    cfg = config(sys.argv[1:] if argv is None else argv)
    if cfg.get('recompute'): return recompute(cfg['recompute'], cfg)
    pol = preflight_path_policy(cfg)                                    # 908 r2 (P2-4): before ANY file operation
    if not pol['ok']:
        print('TEST908_TECHNICAL_STOP PREFLIGHT_PATH_POLICY: %s (roots %s); nothing was written, Drive not touched' % (pol['problems'], pol['roots']), flush=True)
        print('TEST908 DURUM: TEKNIK_HATA | EXIT=1 | TECHNICAL=TECHNICAL_UNDECIDABLE | VERDICT=TECHNICAL_MISMATCH[PREFLIGHT_PATH_POLICY] | DRIVE=NOT_TOUCHED', flush=True)
        return 1
    init_run(cfg); R['path_policy'] = pol
    try: gpu_main(cfg)
    except BaseException as e:
        tb = traceback.format_exc(); stopped = isinstance(e, Stop908) or type(e).__name__ in ('StopT896', 'Stop904', 'Stop906')
        R.update(status='TECHNICAL_ABORT' if stopped else ('INTERRUPTED' if isinstance(e, KeyboardInterrupt) else 'ERROR'),
                 technical_verdict='TECHNICAL_UNDECIDABLE', error='%s: %s' % (type(e).__name__, str(e)[:3000]), traceback=tb)
        fg = R['top']['first_failed_gate']
        R['top'].update(technical_verdict='TECHNICAL_UNDECIDABLE', verdict='GPU_REQUIRED_A100_TECHNICAL_STOP' if fg in ('GATE_GPU_PREFLIGHT_906', 'GATE_GPU_PREFLIGHT_908') else 'TECHNICAL_MISMATCH')   # 908 r2 (P3-1)
        if fg is None: R['top']['first_failed_gate'] = 'ABORT: ' + str(e)[:200]
        (ROOT / 'TEST908_traceback.txt').write_text(tb); print('TEST908_TECHNICAL_STOP', R['error'][:1500], flush=True)
        with LOG.open('a') as f: f.write('TEST908_TECHNICAL_STOP ' + R['error'][:1500] + '\n')
        if isinstance(e, KeyboardInterrupt): finalize_artifacts(cfg); raise
    receipt = finalize_artifacts(cfg); rc = exit_code(receipt); line = status_line(rc, receipt); print(line, flush=True)
    with LOG.open('a') as f: f.write(line + '\n')
    return rc


HEX40 = re.compile(r'^[0-9a-f]{40}$')


def executed_source_binding(es, src_dir):
    """method-independent binding of the packaged executed-source file to the recorded identity. ALWAYS: the file exists and its SHA-256 /
    git blob equal executed_file_sha256 / executed_file_git_blob (recorded by gpu_main from the bytes it wrote). direct___main___file:
    those equal the identity sha256 / git_blob. NOTEBOOK_CELL_SELF_CAPTURE: captured cell text is THE recorded source and
    its packaged exact bytes must match the cell SHA, identity SHA and Git-blob. Legacy NOTEBOOK_CELL_EQUALS_STAGED_FILE
    records retain their original verification path. Any other method fails.
    Evidence-set consistency, not an external cryptographic signature."""
    d = Path(src_dir); ef = d / 'TEST908_executed_908.py'; es = es or {}; m = es.get('method'); why = []
    if not ef.is_file(): return ['EXECUTED_SOURCE_FILE_MISSING']
    for f in ('sha256', 'executed_file_sha256'):
        if not _hex(es.get(f)): why.append('EXECUTED_SOURCE_FIELD_MISSING:' + f)
    for f in ('git_blob', 'executed_file_git_blob'):
        if not (isinstance(es.get(f), str) and HEX40.match(es[f])): why.append('EXECUTED_SOURCE_FIELD_MISSING:' + f)
    if why: return why
    b = ef.read_bytes()
    if sha_b(b) != es['executed_file_sha256']: why.append('EXECUTED_SOURCE_SHA')
    if blob_b(b) != es['executed_file_git_blob']: why.append('EXECUTED_SOURCE_BLOB')
    if m == 'direct___main___file':
        if es['executed_file_sha256'] != es['sha256'] or es['executed_file_git_blob'] != es['git_blob']: why.append('DIRECT_IDENTITY_NE_EXECUTED_FILE')
    elif m == 'NOTEBOOK_CELL_SELF_CAPTURE':
        if es['executed_file_sha256'] != es['sha256'] or es['executed_file_git_blob'] != es['git_blob']:
            why.append('NOTEBOOK_CELL_IDENTITY_NE_EXECUTED_FILE')
        if es.get('cell_sha256') != es['executed_file_sha256']: why.append('NOTEBOOK_CELL_SHA_NE_EXECUTED_FILE')
        if not isinstance(es.get('functions_checked'), int) or es['functions_checked'] < 1: why.append('NOTEBOOK_FUNCTION_COUNT_INVALID')
    elif m == 'NOTEBOOK_CELL_EQUALS_STAGED_FILE':
        gf = d / 'TEST908_staged_908.py'
        if es.get('cell_sha256') != es['executed_file_sha256']: why.append('NOTEBOOK_CELL_SHA_NE_EXECUTED_FILE')
        if not gf.is_file(): why.append('STAGED_FILE_MISSING')
        else:
            g = gf.read_bytes()
            if sha_b(g) != es['sha256'] or blob_b(g) != es['git_blob']: why.append('STAGED_FILE_NE_RECORDED_IDENTITY')
            if _canon_lines(b.decode('utf-8', 'replace')) != _canon_lines(g.decode('utf-8', 'replace')): why.append('NOTEBOOK_CELL_NE_STAGED_FILE')
    else: why.append('EXECUTED_SOURCE_METHOD_UNKNOWN:%s' % m)
    return why


def authenticate_record(Rj, run_dir, man_bytes):
    """record authentication for --recompute (verified mode): evidence-set identity, NOT a re-execution of the GPU run (906 r2 logic,
    908 names / gates / counts)."""
    why = []; d = Path(run_dir); gates = Rj.get('gates') or {}
    if Rj.get('status') != 'COMPLETE' or Rj.get('technical_verdict') != 'PASS': why.append('RECORD_NOT_COMPLETE_PASS')
    if d.name != 'TEST908_%s' % Rj.get('run_id'): why.append('RUN_DIR_NE_RUN_ID')
    sp = Rj.get('sources_pinned') or {}
    if sp.get('906') != SRC906 or sp.get('903') != SRC903 or sp.get('904') != SRC904: why.append('SOURCE_PINS')
    ev = []
    try: ev = [json.loads(l) for l in (d / 'TEST908_events.jsonl').read_text().splitlines() if l.strip()]
    except Exception as e: why.append('EVENTS_UNREADABLE %s' % type(e).__name__)
    why += required_gate_status(gates, Rj.get('technical_blockers'), events=ev)[1]     # r2 (P2-A): the same rule as the live verdict
    abi = ((gates.get('GATE_WS_ABI_908') or {}).get('data') or {}).get('isolation') or {}
    if not abi.get('ok'): why.append('DECISION_PATH_ISOLATION_NOT_OK')
    if not ((((gates.get('GATE_ENGINE_906') or {}).get('data') or {}).get('isolation')) or {}).get('ok'): why.append('ISOLATION_906_NOT_OK')
    if not drive_after_a100(ev): why.append('DRIVE_GATE_BEFORE_A100_PREFLIGHT')
    if ((gates.get('GATE_GPU_PREFLIGHT_908') or {}).get('data') or {}).get('drive_ops_before') != []: why.append('DRIVE_OPS_BEFORE_A100')
    why += ['EVENT_CHAIN:' + x for x in event_chain_problems(Rj, ev)]                 # 908 r2 (P2-2)
    if Rj.get('manifest_sha256') != sha_b(man_bytes): why.append('MANIFEST_SHA')
    es = Rj.get('executed_source') or {}; ef = d / 'sources' / 'TEST908_executed_908.py'
    why += executed_source_binding(es, d / 'sources')                       # r2 (P2-C): every method
    sums = d / 'SHA256SUMS.txt'
    if not sums.is_file(): why.append('SHA256SUMS_MISSING')
    else:
        rows = [l.split('  ', 1) for l in sums.read_text().splitlines() if l.strip()]
        for h, rel in rows:
            f = d / rel
            if not f.is_file() or sha_file(f) != h: why.append('SHA256SUMS_MISMATCH:' + rel)
        listed = {rel for _, rel in rows}
        needs = ['TEST908_results.json', 'TEST908_manifest.json', 'TEST908_events.jsonl', 'sources/TEST908_executed_908.py']
        if es.get('method') == 'NOTEBOOK_CELL_EQUALS_STAGED_FILE': needs.append('sources/TEST908_staged_908.py')
        for need in needs:
            if need not in listed: why.append('SHA256SUMS_DOES_NOT_LIST:' + need)
    marker = '/TEST908_%s/' % Rj.get('run_id')
    for key, o in (Rj.get('objects') or {}).items():
        fs = str(o.get('file', ''))
        if marker not in fs: why.append('OBJECT_OUTSIDE_RUN:' + key); continue
        f = d / fs.split(marker)[-1]
        if not f.is_file() or sha_file(f) != o.get('sha256'): why.append('OBJECT_FILE:' + key)
    rc = [p_ for p_ in (d.parent / ('TEST908_SONUC_%s_RECEIPT.json' % Rj.get('run_id')), d / ('TEST908_SONUC_%s_RECEIPT.json' % Rj.get('run_id'))) if p_.is_file()]
    if not rc: why.append('RECEIPT_NOT_FOUND')
    else:
        try:
            rj = json.loads(rc[0].read_text())
            if rj.get('results_sha256') != sha_file(d / 'TEST908_results.json') or rj.get('run_id') != Rj.get('run_id'): why.append('RECEIPT_DOES_NOT_NAME_THESE_RESULTS')
        except Exception as e: why.append('RECEIPT_UNREADABLE %s' % type(e).__name__)
    return not why, why


def record_schema_problems(Rj, man):
    """908 r2 (P3-3): structural check of a record / manifest before any scoring (field name in every problem; nothing is filled in)."""
    why = []
    if not isinstance(Rj, dict): return ['RECORD_NOT_AN_OBJECT']
    if not isinstance(man, dict): return ['MANIFEST_NOT_AN_OBJECT']
    for k in ('cues', 'task_text', 'catalog_entries', 'truth', 'obs_ids', 'special_ids'):
        if k not in man: why.append('MANIFEST_FIELD_MISSING:' + k)
    for k, t in (('prefix', dict), ('objects', dict), ('gates', dict), ('arms', dict), ('fullref', dict), ('branches', dict), ('sources_pinned', dict)):
        if not isinstance(Rj.get(k), t): why.append('RECORD_FIELD_%s:%s' % ('MISSING' if k not in Rj else 'TYPE', k))
    P = Rj.get('prefix') if isinstance(Rj.get('prefix'), dict) else {}
    for w in WORLDS:
        Pw = P.get(w)
        if not isinstance(Pw, dict): why.append('RECORD_FIELD:prefix.%s' % w); continue
        D = Pw.get('decisions')
        if not isinstance(D, list): why.append('RECORD_FIELD:prefix.%s.decisions' % w); continue
        for i, d in enumerate(D):
            if not isinstance(d, dict) or not isinstance(d.get('mount'), dict) or not isinstance(d['mount'].get('keys'), list) or not isinstance(d.get('action'), dict):
                why.append('RECORD_FIELD:prefix.%s.decisions[%d]' % (w, i))
        for f in ('avail_diag', 'fork'):
            if Pw.get(f) is not None and not isinstance(Pw.get(f), dict): why.append('RECORD_FIELD:prefix.%s.%s' % (w, f))
    for w, aw in (Rj.get('arms') or {}).items() if isinstance(Rj.get('arms'), dict) else []:
        if not isinstance(aw, dict) or not all(isinstance(r, dict) for r in aw.values()): why.append('RECORD_FIELD:arms.%s' % w)
    return why


def recompute(path, cfg=None):
    """re-score from the raw records + the run's manifest (no model, no torch, no GPU, no Drive mount, no 906 import). OFFLINE_RESCORE
    (--recompute-mode rescore): scoring and record self-consistency only, 0 if consistent. VERIFIED (default): the same + authenticate_record
    (incl. the event-chain replay); 0 ONLY if authenticated; 3 if consistent but NOT_AUTHENTICATED; 1 on problems. 908 r2 (P3-3): an
    unreadable / malformed record or manifest is a structured problem (field named) with exit 1 - never a traceback, never a PASS."""
    def fail(why):
        print('RECOMPUTE: MALFORMED_RECORD')
        for x in why: print('RUN RECORD PROBLEM:', x)
        print('AUTHENTICATION: NOT_AUTHENTICATED (MALFORMED_RECORD)'); return 1
    try:
        p = Path(path); Rj = json.loads(p.read_text()); b = (p.parent / 'TEST908_manifest.json').read_bytes(); man = json.loads(b)
    except Exception as e: return fail(['UNREADABLE %s: %s' % (type(e).__name__, str(e)[:300])])
    sp = record_schema_problems(Rj, man)
    if sp: return fail(sp)
    try: return _recompute_checked(p, Rj, b, man, cfg)
    except Exception as e: return fail(['MALFORMED_FIELD %s: %s' % (type(e).__name__, str(e)[:300])])


def _recompute_checked(p, Rj, b, man, cfg):
    mode = (cfg or {}).get('recompute_mode', 'verified')
    gates = Rj.get('gates') or {}
    evs = read_events(p.parent / 'TEST908_events.jsonl') if mode != 'rescore' else None
    gates_ok, gate_why = required_gate_status(gates, Rj.get('technical_blockers'), events=(evs or []) if mode != 'rescore' else None)
    iso = isolation_from_gates(gates)
    ev = evaluate_908(man, Rj, gates_ok and Rj.get('technical_verdict') == 'PASS', isolation_ok=iso, technical_why=gate_why)
    probs = verify_run_record(Rj, b, ev); consistent = not probs and not ev['integrity_problems']
    print('RECOMPUTE MODE: %s' % ('OFFLINE_RESCORE (scoring only; provenance NOT certified)' if mode == 'rescore' else 'VERIFIED (rescore + record authentication)'))
    print('RECOMPUTED %s | record problems: %d' % (ev['verdict'], len(probs) + len(ev['integrity_problems'])))
    for l in report_lines(ev): print(l)
    for x in probs + ev['integrity_problems']: print('RUN RECORD PROBLEM:', x)
    if mode == 'rescore':
        print('AUTHENTICATION: NOT_ATTEMPTED (OFFLINE_RESCORE)'); return 0 if consistent else 1
    auth, why = authenticate_record(Rj, p.parent, b)
    print('AUTHENTICATION: %s' % ('AUTHENTICATED_RECORD' if auth else 'UNVERIFIED_GATE_CHAIN / NOT_AUTHENTICATED: ' + '; '.join(why[:40])))
    if not consistent: return 1
    return 0 if auth else 3


if __name__ == '__main__':
    _rc = main(None)
    if _rc and 'get_ipython' not in globals(): sys.exit(_rc)
