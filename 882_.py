# AKBASCORE SILICON HIPPOCAMPUS — TEST882 — MODEL-OWNED C-BLIND ADDRESSING -> PHYSICAL SSD RECALL -> VIS ACTION -> STORE -> D2
# One A100-SXM4-80GB Colab cell. Frozen Qwen2.5-72B-Instruct NF4, BF16 activations/KV, 80 layers, H=8192. TEST881 is not
# modified: this is a new file; every reused definition is AST-selected from git-blob-locked files and never patched.
# ---------------------------------------------------------------------------------------------------------------------------
# SOURCE MANIFEST — repository ceceli33/titan-cognitive-core-v3, pinned commit 88ed5e8034017021a2ecc1409c82ba22e2071c5b
#   (codeload zip of that commit, never main). Git blobs checked at G0 before the model is loaded:
#   test870.py de3c8153 engine | Test870.log e954d658 | 873.py 2e44affa | 873.log 1c9eb9fc | 874.py 12172001 | 874.log 1229e3b7
#   877.py a6aa7648 | 877.log c4eb5802 | 878.py 7842e867 | Test_878_log2.log 2bfc7adc | 879.py 92f9eb66 | 879.log c1205bc0
#   880.py 3e6aab5d | 880.log adcc0389 | 881.py 63466135 (committed TEST881 r2) | 881.log e6e38359 | 757.py 3d88bf86
#   841.py 135b18e5 | 851.py 0f01e73b. The TEST881 GPU log names its executed cell 91c69f11…: a different object from the
#   committed blob 63466135; both are reported, never equated. This cell carries no hash of itself: its blob / SHA-256 are
#   measured at runtime (G0) and written to 882_source_manifest.json before the model is loaded.
# REUSED (AST selection, side-effect free, firewall-scanned): 878 constants + probe878/xspan878/write_exp878/load_exp878/
#   append_exp878/xappend878/xcar878/persist878 …; 880 query880/rows_ok880/sha_rows880/store_words880; 881 RealStore881,
#   xtrace881, cell881, xread881/nread881, full_seal881, make_single_episode_layout881, store_reading881, selftest_mask881 ….
# PREREG (dict PREREG882 below; SHA-256 printed and written before the model is loaded):
#   Z = pre-action decision segments only (no A, no C, no outcome, no id, no candidate list). Write key K = F(Z_source),
#   live query Q = F(Z_live) with the SAME encoder: gen851 on MEMNULL841 with a byte-identical address prompt/suffix ->
#   query880 (index_embeds841 -> xspan878 L0-3 H3 rows) -> unit(rows - mu_addr); mu_addr from the disjoint calibration rows
#   only; score = locked peak50_841 on CPU over SSD-reloaded key sidecars. Need (USE_MEMORY / NO_MEMORY / ABSTAIN) is a
#   separate native reading without candidates. Router: ACCEPT iff s1 > max(s_NULL, tau_neg) and s1 - s2 > delta_tie and
#   no exact duplicate key; empty -> NO_CANDIDATE; never top-2; at most one new native query. tau_neg / delta_tie frozen
#   at G3 from calibration negatives (positives only to detect REVISE_ADDRESS_DOMAIN). Accepted rank-1 -> parent-aware
#   physical mount -> model KEEP/REJECT validation -> TEST881 readout -> D1 VIS execution -> real C -> native STORE/DISCARD
#   -> crash-safe commit with address sidecar -> D2 only if a new cartridge was written. Offline labels only at G9.
# GPU_NOT_RUN_BY_AUTHOR: the author of this cell did not execute it on an A100; nothing here is a GPU measurement.
import ast as _a882, base64 as _b64882, hashlib as _h882, json as _j882, os as _o882, re as _r882, shutil as _s882
import tempfile as _tf882, urllib.request as _u882, math as _m882
import numpy as _np882
_a881, _h881, _j881, _o881, _r881, _s881, _tf881 = _a882, _h882, _j882, _o882, _r882, _s882, _tf882   # module names used by 881 code
ENGINE_URL882 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB882, MARKER882 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', 'AKBASCORE SILICON HIPPOCAMPUS — TEST882 — MODEL-OWNED'
HEAD882 = '88ed5e8034017021a2ecc1409c82ba22e2071c5b'
TEST881_COMMITTED_BLOB882 = '63466135610cedcdaa7c8c462499f987ef6f08cc'
TEST881_EXECUTED_CELL_IN_LOG882 = '91c69f1181f6ea6639d6cffcef4177dfe3ce81a4'


def blob882(raw):
    return _h882.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def engine_parts882():
    with _u882.urlopen(_u882.Request(ENGINE_URL882, headers={'User-Agent': 'AKBASCORE-TEST882'}), timeout=240) as r:
        raw = r.read()
    assert blob882(raw) == ENGINE_BLOB882, ('ENGINE_BLOB_MISMATCH', blob882(raw))
    text = raw.decode('utf-8'); _a882.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST882_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST882_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST882_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('882_engine.log', '882_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST882_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '882_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '882_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST882_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old)
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL882, 'git_blob': blob882(raw), 'sha256': _h882.sha256(raw).hexdigest()}


try:
    ENGINE882, ENGINE_INFO882 = engine_parts882()
except BaseException as _exc882:      # console capture starts inside the engine prefix: keep a local record of this failure
    import time as _t882, traceback as _tb882
    _p882 = '/content/TEST882_PRE_ENGINE_ERROR_%s.txt' % _t882.strftime('%Y%m%dT%H%M%SZ', _t882.gmtime())
    try:
        with open(_p882, 'w', encoding='utf-8') as _f882: _f882.write(_tb882.format_exc())
    except OSError: _p882 = 'NOT_WRITTEN'
    print('TEST882 PRE-ENGINE ERROR (before console capture):', type(_exc882).__name__, _exc882, '| traceback:', _p882)
    raise
exec(compile(ENGINE882['prefix'], 'test870.py:prefix', 'exec'), globals())
exec(compile(ENGINE882['body'], 'test870.py:engine', 'exec'), globals())
print('TEST882 ENGINE', _j882.dumps(ENGINE_INFO882, sort_keys=True))

# ============================ locks, pinned repository, reused code ============================
CODELOAD864 = 'https://codeload.github.com/ceceli33/titan-cognitive-core-v3/zip/' + HEAD882   # pinned commit, never main
LOCKS864.update({'test870.py': ENGINE_BLOB882, 'Test870.log': 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc',
                 '873.py': '2e44affa5e0dd462155fb265c331270fb8e7b7e1', '873.log': '1c9eb9fca173003eaf45bc7726af13c2817324b7',
                 '874.py': '12172001ba3696ad91087a8b34d7995728259e47', '874.log': '1229e3b70440e3887ccf1bd7e3bad51f900f5313',
                 '877.py': 'a6aa7648e0fb765a8dc9b56b8f79b4dcef5fc772', '877.log': 'c4eb58021ed827fb13d5c15fee7c18541f6d4604',
                 '878.py': '7842e8675544a0328e3552f059c81b7750068a82', 'Test_878_log2.log': '2bfc7adc2a8f718c012a6d722a9e0a04a72cbedd',
                 '879.py': '92f9eb665173986b6c98b42f07eefb3249c861d4', '879.log': 'c1205bc082fb69c68b9f9f4e290808a0dec71fa8',
                 '880.py': '3e6aab5d79af8f75053b0da873d70779406adb74', '880.log': 'adcc0389b359b1dd254887edb1786fd5edff378a',
                 '881.py': TEST881_COMMITTED_BLOB882, '881.log': 'e6e38359799faef306bb261ca97fcd6ca2a32ef5'})
REQUIRED_LOCKS882 = {'757.py': '3d88bf8638390995858f23391f1e043faa586835', '841.py': '135b18e5b1ea113579c607cf9eecf49628cf18c2',
                     '851.py': '0f01e73b9ad160c988cfe059e8b5ae5e1f35f65b'}
TEST878_PREREG882 = '0555ab01d436c0df7e8e1be21aea3170ac0a50d799a528796212298a48dc4103'
_a878, _h878, _j878 = _a882, _h882, _j882
ENGINE_BLOB878 = ENGINE_BLOB882
CONSTS878 = ('TEST877_CELL_BLOB878', 'TEST877_PREREG_DEPS878', 'TEST870_MINUTES', 'WORLDS878', 'SOURCES878', 'FORKS878',
             'SIDES874', '_h877', 'ARM878', 'FUNCS873', 'FUNCS874', 'FUNCS877', 'ROPE_TOL878', 'HARD_MIN878', 'PREREG878')
FUNCS878 = ('Partial878', 'Persist878', 'line878', 'source_audit878', 'load878', 'guard878', 'xspan878', 'next_kv878',
            'tsha878', 'write_exp878', 'load_exp878', 'append_exp878', 'xappend878', 'xcar878', 'arm878', 'jsafe878',
            'dif878', 'pa878', 'sig878', 'persist878', 'probe878')
FUNCS880 = ('rows_ok880', 'sha_rows880', 'query880', 'store_words880')
CONSTS881 = ('STORE_PROMPT881', 'SLOT_TEXT881', 'STAGES881')
CLASSES881 = ('Gate881', 'IntegrityBlock881', 'CommitUncertain881', 'RealStore881')
FUNCS881 = ('peak_update881', 'free_gib881', 'kv_gib881', 'timed881', 'seqlp881', 'cont_tokens881', 'same_reading881',
            'tsha881', 'full_seal881', 'make_single_episode_layout881', 'xread881', 'nread881', 'xtrace881', 'zero_slot881',
            'same_rows881', 'cell881', 'store_reading881', 'selftest_mask881')
BANNED882 = {'register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook', 'output_hidden_states',
             'output_attentions', 'install_all_output_capturing_hooks', 'backward', 'requires_grad_', 'step', 'zero_grad',
             'execute866', 'mount865', 'free865', 'hop865', 'DirectCut3', 'native_append_direct'}
RUNTIME_BANNED_CALLS882 = {'eval', 'exec', 'globals', 'vars', 'locals', '__import__', 'compile', 'setattr', 'getattr'}
EXEC_ALLOW882 = {'d1_882': ('execute866', 'hop865'), 'd2_882': ('execute866',)}   # the only real actions, locked executor
ORACLE882 = {'supported851', 'node851', 'world867', 'correct867', 'success867', 'OFFLINE882', 'FIXTURE882', 'OFFLINE867',
             'worlds829', 'offline_evaluate882', 'fixture_seal882', 'calibrate882', 'CAL_PAIRS882', 'world', 'correct',
             'supported', 'second', 'changed', 'mirror', 'decoy', 'utility', 'world_index', 'card_kind', 'relevant'}
PROMPT_BANNED_WORDS882 = ('world', 'correct', 'supported', 'second', 'changed', 'mirror', 'decoy', 'utility', 'fork', 'oracle')
RUNTIME882 = ('rows_np882', 'digest_segments882', 'address_input882', 'addr_prompt_ids882', 'key_blob882', 'key_from_blob882',
              'make_view882', 'route882', 'thresholds_check882', 'resolve_parent882', 'next_attempt882', 'score882',
              'preC882', 'center882', 'words882', 'need882', 'validate882', 'bank_view882', 'mount882', 'layout_at882',
              'readout_single882', 'readout882', 'live_cell882', 'd1_882', 'd2_882')

# ============================ design constants (fixed before the model is loaded) ============================
RECEIVERS882 = ('00', '01')                       # the two TEST881 receivers: I867_<w>_FORK at step 1, own memory B
D1_RECEIVER882 = '00'                             # C1: the one pre-registered execution cell
BANK_ITEMS882 = ('I867_00_LIVE', 'I867_01_LIVE', 'I867_06_LIVE', 'I867_07_LIVE')   # four real physical live candidates
DIAG_ITEMS882 = ('I867_00_MISSING', 'I867_01_MISSING')   # same X2/A, other C: matched readout + duplicate-key diagnostic only
EXTRA882 = ('I867_06_LIVE', 'I867_07_LIVE')       # written by source_probe882 (probe878 source branch, no TEST873 reference)
CAL_WORLDS882 = ('02', '04', '05', '08')          # disjoint calibration contexts: FORK step-1 query vs LIVE step-2 key
DUP_ITEM882 = 'I867_00_MISSING'                   # C7: its pre-C key is computed separately from its own captured Z
SELF_RECALL_ITEM882 = 'I867_02_LIVE'              # write path recomputed through the read path (Ftheta parity)
DELTA_MIN882 = 1e-3                               # floor of delta_tie (score units of peak50 on unit rows)
MAX_RETRY882, MAX_PARENT_DEPTH882 = 1, 2
WALL_MIN882, PEAK_GIB882, FREE_MIN_GIB882, HEADROOM_GIB882, FFE_MAX882, DISK_MIN_GIB882 = 50.0, 64.0, 8.0, 4.0, 120.0, 5.0
ID_SALT882, SHUFFLE_SALT882 = 'TEST882-OPAQUE-ID', 'TEST882-ID-SHUFFLE'
VIEW_FIELDS882 = ('id', 'sha256', 'tensor_sha', 'address_key', 'address_sha256', 'parent_id', 'parent_sha256', 'body_tokens',
                  'requires_parent', 'generation')   # the K3.1 runtime whitelist without 'file' (the resolver reads files)
STAGES882 = ('TMP_WRITTEN', 'FILE_RENAMED', 'FILE_FSYNC', 'ADDRESS_SIDECAR', 'ADDRESS_FSYNC', 'ENTRY_SIDECAR', 'DIR_FSYNC',
             'VERIFIED_RELOAD', 'CATALOG_APPEND', 'CATALOG_FSYNC', 'CATALOG_DIR_FSYNC', 'COMMITTED')
ADDR_PROMPT882 = ('Question: {q}\nThe numerical context contains your current decision state, before any action is taken. Do '
                  'not decide and do not answer. In at most six words, describe the earlier decision state whose recorded real '
                  'consequence would help this decision.')
ADDR_RETRY_PROMPT882 = ('Question: {q}\nThe numerical context contains your current decision state, before any action is taken. '
                        'A first description of the earlier decision state you need did not identify one single physical '
                        'record. Do not decide and do not answer. In at most six words, describe that earlier decision state '
                        'again, more specifically.')
ADDR_SUFFIX882 = '\nEarlier decision state:'
NEED_PROMPT882 = ('Question: {q}\nThe numerical context contains your current decision state, before any action is taken. Before '
                  'you decide the next reasoning action, decide whether a physical record of an earlier decision and its real '
                  'consequence is needed now. Reply with exactly one word: USE_MEMORY, NO_MEMORY or ABSTAIN.')
NEED_SUFFIX882 = '\nMemory need:'
VALID_PROMPT882 = ('Question: {q}\nThe numerical context contains your current decision state. One physical record of an earlier '
                   'decision and its real consequence has been retrieved and mounted in your memory for this decision. Decide '
                   'whether to keep this record for the current decision. Reply with exactly one word: KEEP_MEMORY, '
                   'REJECT_MEMORY or ABSTAIN.')
VALID_SUFFIX882 = '\nRecord decision:'
NEED_WORDS882 = ('USE_MEMORY', 'NO_MEMORY', 'ABSTAIN')
VALID_WORDS882 = ('KEEP_MEMORY', 'REJECT_MEMORY', 'ABSTAIN')
ENCODER882 = 'gen851(MEMNULL841, address prompt, Z, suffix).rows -> query880 (index_embeds841 -> xspan878 L0-3) -> unit(rows - mu_addr)'
VERDICTS882 = ('TECHNICAL_BLOCK', 'REVISE_ADDRESS_DOMAIN', 'NO_NATURAL_NEED_MEMORY', 'NO_MATCH_ABSTENTION',
               'AUTONOMOUS_PHYSICAL_MOUNT', 'AUTONOMOUS_PHYSICAL_MOUNT_OFFLINE_IRRELEVANT', 'OFFLINE_RELEVANT_SELECTION',
               'MEMORY_DEPENDENT_POLICY_CHANGE', 'SUPPORTED_SINGLE_TRANSITION_DESCRIPTIVE', 'NO_STORE_DISCARD',
               'NO_NEW_MEMORY_WRITTEN', 'SELF_REUSE_NOT_RUN', 'PARENT_CONDITIONED_SELF_REUSE_MECHANICAL',
               'SELF_REUSE_POLICY_CHANGE', 'CLOSED_LOOP_NOT_ESTABLISHED')
PREREG882 = {
    'test': 'TEST882 (name given by the user in the TEST882 order of 13 Nov 2026)',
    'question': 'can the frozen model decide by itself that it needs memory, produce its own pre-action address, select the '
                'right physical SSD cartridge without seeing C, refuse a wrong / undecidable mount, read the recalled real C '
                'into its native VIS decision, execute it literally, decide STORE/DISCARD, and re-find a cartridge it wrote',
    'repository': {'head': HEAD882, 'archive': 'codeload zip of the pinned commit; every file git-blob locked',
                   'test881': {'committed_blob': TEST881_COMMITTED_BLOB882, 'executed_cell_blob_in_log': TEST881_EXECUTED_CELL_IN_LOG882,
                               'relation': 'different objects, both reported, never equated'}},
    'address': {'Z': 'state["segments"] of the decision step before its action (question text via the prompt); no A, no C, no '
                     'outcome, no id, no candidate list, no fixture field',
                'encoder': ENCODER882, 'prompt': ADDR_PROMPT882, 'suffix': ADDR_SUFFIX882, 'memory': 'MEMNULL841',
                'mu_addr': 'mean of the raw H3 address rows of the calibration keys and queries only (label free), frozen at G2',
                'null_key': 'query880(MUE845 row) centred with mu_addr', 'score': 'locked peak50_841 on CPU',
                'write_key': 'computed when the cartridge is registered, from the same Z that preceded its action; for a new '
                             'cartridge: the live D1 query computed before the action (no key after STORE)',
                'retry_prompt': ADDR_RETRY_PROMPT882},
    'need': {'prompt': NEED_PROMPT882, 'suffix': NEED_SUFFIX882, 'words': NEED_WORDS882, 'memory': 'receiver B only',
             'reader': 'teacher-forced CROP reader, rule of the locked readers: argmax word unless mass < ABSTAIN_MASS867',
             'rule': 'only USE_MEMORY permits a mount; the route is still computed and logged as DIAGNOSTIC_ROUTE_ONLY'},
    'router': {'view': list(VIEW_FIELDS882), 'opaque_ids': 'M882_ + sha256(catalog id, file sha, salt)[:16]',
               'accept': 's1 > max(s_NULL, tau_neg) and s1 - s2 > delta_tie and no exact duplicate address key at rank 1',
               'tie': 'exact duplicate key or exact score tie at rank 1 -> TIE_NO_MOUNT', 'empty': 'NO_CANDIDATE',
               'top2': 'never', 'retry': 'at most one new native query (retry prompt) after NO_MATCH / tie / model REJECT',
               'tie_break': 'sorted opaque id (not a semantic preference; order / id shuffle controls)'},
    'calibration': {'worlds': CAL_WORLDS882, 'query': 'I867_<w>_FORK step 1', 'key': 'I867_<w>_LIVE step 2',
                    'positives': 'same context (w, w); used only to detect REVISE_ADDRESS_DOMAIN',
                    'negatives': 'all (w, v), v != w', 'tau_neg': 'max calibration negative score',
                    'delta_tie': 'max(%g, 2 x self-recall noise, max over calibration queries of top1 - top2 among negatives)' % DELTA_MIN882,
                    'leave_context_out': 'for each w: thresholds from pairs without w, then route Q_w over the 4 calibration keys',
                    'pass': 'final in-domain positive accepted >= 1, LOO correct >= 1, LOO false mounts == 0, key / query '
                            'shuffle bite, duplicate -> tie, empty -> NO_CANDIDATE, order / id invariance; else REVISE_ADDRESS_DOMAIN'},
    'bank': {'live': BANK_ITEMS882, 'diagnostic_not_routable': DIAG_ITEMS882, 'receivers': RECEIVERS882, 'd1': D1_RECEIVER882},
    'cells': {'C0': 'calibration + threshold freeze', 'C1': 'R00 need / query / route / mount (D1 cell)',
              'C2': 'R01 same bank (goal sensitivity)', 'C3': 'wrong-only bank (relevant one removed), CPU route only',
              'C4': 'empty bank', 'C5': 'key shuffle', 'C6': 'query shuffle (R01 query on the R00 decision)',
              'C7': 'duplicate pre-C key (I867_00_MISSING vs I867_00_LIVE)', 'C8': 'bounded retry, only after a natural no-match / reject',
              'C9': 'wrong rejection: offline view of model validation on naturally irrelevant mounts (NOT_RUN if none)',
              'D1': 'C1 kept mount: VIS recompute exact -> literal executor -> real C -> native STORE/DISCARD -> commit',
              'D2': 'only if D1 committed: next decision state from the D1 observation, own need / query / route over the bank '
                    'with the new cartridge, parent-chain mount, readout, VIS execution; one attempt'},
    'readout': {'D1_matched': 'locked cell881 when the selected cartridge has a same-X2 partner (full TEST881 contract)',
                'single': 'C_BLIND trace vs C-zeroed copy (80-layer X / continuation K/V / hidden / logp bitwise), trace == locked '
                          'xcar878, native C_BLIND, receiver seal, then VIS', 'other_cells': 'single readout only'},
    'mount': ['file SHA + tensor SHA (load_exp878)', 'locked append_exp878', 'n_exact', '80 layers', 'finite', 'prefix rows bitwise',
              'no alias', 'lower V bitwise', 'lower K roundtrip <= ROPE_TOL878', 'explicit xappend878 == native append bitwise',
              'receiver B full 80-layer seal unchanged', 'source-timeline recon (locked persist878) for replayed cartridges'],
    'store': {'stages': list(STAGES882), 'reader': 'locked store_words880 procedure via store_reading881'},
    'verdicts': VERDICTS882,
    'budgets': {'wall_min': WALL_MIN882, 'peak_alloc_gib': PEAK_GIB882, 'free_min_gib': FREE_MIN_GIB882,
                'stage_headroom_gib': HEADROOM_GIB882, 'adapter_ffe_lower_bound_max': FFE_MAX882,
                'ESTIMATED_not_measured': {'peak_gib': '41-46 (K3.1)', 'wall_min': '28-42 (K3.1)',
                                           'adapter_ffe': 'DERIVED ~65-75 without STORE, ~80-90 with STORE + D2 (planning arithmetic, not a measurement)'},
                'note': 'ADAPTER_FFE_LOWER_BOUND counts TEST882 adapter forwards; replay / preflight / locked probe work is '
                        'TOTAL_GPU_WORK_NOT_FULLY_ACCOUNTED (CALLS849 reported)'},
    'limits': ['two receivers, four live candidates, one execution: a pilot, not a statistic',
               'a single supported transition is descriptive, never a comparative advantage',
               'same X2 / different C is information-theoretically undecidable before C: forced tie']}
PREREG_SHA882 = sha256_bytes864(_j882.dumps(PREREG882, sort_keys=True).encode())
STATE882 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO882, 'prereg_sha256': PREREG_SHA882, 'source': {}, 'api': {},
            'selftests': {}, 'ref873': {}, 'targets_static': {}, 'sides': {}, 'experience': {}, 'receivers': {}, 'cells': {},
            'physical': {}, 'address': {}, 'calibration': {}, 'thresholds': {}, 'live': {}, 'controls': {}, 'readout': {},
            'd1': {}, 'd2': {}, 'store': {}, 'bank': {}, 'offline': None,
            'budget': {'adapter_ffe_lower_bound': 0.0, 'ffe_by_kind': {}, 'total_gpu_work_not_fully_accounted': True,
                       'ssd_bytes': 0, 'peak_alloc_gib': 0.0, 'peak_reserved_gib': 0.0, 'arms': {}, 'stages': {}},
            'not_run': [], 'blocks': [], 'verdict': None, 'error': None}
STATE881 = STATE878 = STATE877 = STATE882                 # the selected 877/878/881 functions write here
T2_KEEP878, SRC878, TGT878, EXP878, G881, ARMS881, TRACES881 = {}, {}, {}, {}, {}, {}, {}
SRC882, ZCAP882, EXEC882, ADDR882, FROZEN882, KEEP882, MU882, ADDRESS_DOMAIN882, D1RUN882 = {}, {}, {}, {}, {}, {}, {}, {}, {}
BANKSIDE882, OFFLINE882 = {}, {}
EXEC_CELL881, EXEC_COND881 = (None, None), 'LIVE'        # read by the locked cell881: which grown caches are kept


class Gate882(Exception):
    pass


class Budget882(Exception):
    pass


class Revise882(Exception):
    pass


class Partial878(Exception):                                   # placeholder; replaced by the locked TEST878 class at selection
    pass


def line882(*parts): short864('T882', *parts)


# ============================ firewall (calls, aliases, getattr strings, keywords, subscripts, globals) ============================
def scan882(node, allow=(), runtime=False):
    calls = [c for c in _a882.walk(node) if isinstance(c, _a882.Call)]
    used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in calls}
    used |= {k.arg for k in _a882.walk(node) if isinstance(k, _a882.keyword)}
    alias = BANNED882 - {'step'}                          # a bare name / key 'step' is ordinary data; a call .step() is still refused
    used |= {s.slice.value for s in _a882.walk(node) if isinstance(s, _a882.Subscript) and
             isinstance(s.slice, _a882.Constant) and isinstance(s.slice.value, str)} & alias
    used |= {n.id for n in _a882.walk(node) if isinstance(n, _a882.Name)} & alias
    used |= {n.attr for n in _a882.walk(node) if isinstance(n, _a882.Attribute)} & alias
    used |= {c.args[1].value for c in calls if getattr(c.func, 'id', None) in ('getattr', 'setattr', 'hasattr') and
             len(c.args) > 1 and isinstance(c.args[1], _a882.Constant)} & BANNED882
    bad = (used & BANNED882) - set(allow)
    if runtime:
        bad |= {getattr(c.func, 'id', None) for c in calls} & RUNTIME_BANNED_CALLS882
        bad |= {n.id for n in _a882.walk(node) if isinstance(n, _a882.Name)} & {'globals', 'vars', 'locals', '__builtins__'}
    assert not bad, ('FIREWALL882', getattr(node, 'name', '?'), sorted(bad))


def oracle_scan882(node):
    names = {n.id for n in _a882.walk(node) if isinstance(n, _a882.Name)} | \
            {n.attr for n in _a882.walk(node) if isinstance(n, _a882.Attribute)} | \
            {a.arg for a in _a882.walk(node) if isinstance(a, _a882.arg)}
    keys = {n.value for n in _a882.walk(node) if isinstance(n, _a882.Constant) and isinstance(n.value, str)}
    bad = (names | keys) & ORACLE882
    assert not bad, ('ORACLE_FIREWALL882', getattr(node, 'name', '?'), sorted(bad))


def prompt_lint882(texts):
    bad = []
    for t in texts:
        for w in PROMPT_BANNED_WORDS882:
            if _r882.search(r'\b%s\b' % w, t, flags=_r882.IGNORECASE): bad.append((w, t[:40]))
    return bad


def defs882(tree):
    out = {}
    for n in tree.body:
        if isinstance(n, _a882.FunctionDef): out[n.name] = n
        elif isinstance(n, _a882.ClassDef):
            out[n.name] = n
            for m in n.body:
                if isinstance(m, _a882.FunctionDef): out[n.name + '.' + m.name] = m
    return out


def capture_source882():
    # the RUNNING cell is the last history entry; it carries no self-hash: its blob / SHA-256 are measured here and written to a
    # manifest before the model is loaded (the report and every new cartridge carry them)
    try:
        source, how = get_ipython().history_manager.input_hist_raw[-1], 'IPYTHON_CURRENT_CELL'
    except NameError:
        source = open(__file__, encoding='utf-8').read() if '__file__' in globals() else None; how = 'FILE_%RUN'
    assert source and MARKER882 in source and 'def d1_882' in source, 'EXECUTED_882_SOURCE_NOT_CAPTURED'
    tree = _a882.parse(source); funcs = defs882(tree)
    for name, node in funcs.items():
        base = name.split('.')[-1]
        if isinstance(node, _a882.FunctionDef) and (base.endswith('882') or name.startswith('RealStore882.')):
            scan882(node, EXEC_ALLOW882.get(base, ()), runtime=base in RUNTIME882)
    assert set(RUNTIME882) <= set(funcs), ('RUNTIME_FUNCTIONS_MISSING', sorted(set(RUNTIME882) - set(funcs)))
    for name in RUNTIME882: oracle_scan882(funcs[name])
    lint = prompt_lint882([ADDR_PROMPT882, ADDR_RETRY_PROMPT882, ADDR_SUFFIX882, NEED_PROMPT882, NEED_SUFFIX882, VALID_PROMPT882,
                           VALID_SUFFIX882])
    assert not lint, ('PROMPT_ORACLE_WORDS', lint)
    calls = [n for n in _a882.walk(tree) if isinstance(n, _a882.Call) and getattr(n.func, 'id', None) == 'reproduce_pre859859']
    assert len(calls) == 1, 'MODEL_LOADER_CALL_COUNT_NOT_ONE'
    rs = [n for n in _a882.walk(tree) if isinstance(n, _a882.Assign) and any(getattr(t, 'id', '') == 'xray_point870' for t in n.targets)]
    assert len(rs) == 1 and getattr(rs[0].value, 'id', None) == 'probe882', 'FIREWALL882_REBIND'
    (ROOT864 / 'TEST882.py').write_text(source, encoding='utf-8')
    STATE882['source'] = {'how': how, 'executed_cell_git_blob': git_blob864(source.encode()),
                          'executed_cell_sha256': sha256_bytes864(source.encode()), 'lines': source.count('\n') + 1,
                          'firewall': 'PASS', 'oracle_firewall': 'PASS (%d runtime functions)' % len(RUNTIME882),
                          'prompt_lint': 'PASS', 'self_hash': 'NONE (measured at runtime only)'}
    json_write864('882_source_manifest.json', dict(STATE882['source'], prereg_sha256=PREREG_SHA882, head=HEAD882,
                                                   engine_blob=ENGINE_BLOB882, test881_committed_blob=TEST881_COMMITTED_BLOB882,
                                                   test881_executed_cell_blob_in_log=TEST881_EXECUTED_CELL_IN_LOG882,
                                                   before_model_load=True))


def select_nodes882(name, consts, classes, funcs):
    tree = _a882.parse(RAW_SOURCES864[name].decode(), filename=name)
    cn = [n for n in tree.body if isinstance(n, _a882.Assign) and
          {x.id for t in n.targets for x in _a882.walk(t) if isinstance(x, _a882.Name)} & set(consts)]
    kn = [n for n in tree.body if isinstance(n, _a882.ClassDef) and n.name in classes]
    fn = [n for n in tree.body if isinstance(n, (_a882.FunctionDef, _a882.ClassDef)) and n.name in funcs]
    got = {n.name for n in kn + fn}
    assert got == set(classes) | set(funcs), ('SELECT', name, sorted((set(classes) | set(funcs)) - got))
    return cn, kn, fn


def select_locked882():
    for name, blob in REQUIRED_LOCKS882.items():
        assert LOCKS864.get(name) == blob and git_blob864(RAW_SOURCES864[name]) == blob, ('REQUIRED_LOCK', name)
    for name in ('878.py', '880.py', '881.py', '881.log'):
        assert git_blob864(RAW_SOURCES864[name]) == LOCKS864[name], ('LOCK', name)
    c8, _, f8 = select_nodes882('878.py', CONSTS878, (), FUNCS878)
    for n in f8:
        if isinstance(n, _a882.FunctionDef): scan882(n, ('native_append_direct',) if n.name == 'append_exp878' else ())
    exec(compile(_a882.fix_missing_locations(_a882.Module(c8, [])), '878.py:constants', 'exec'), globals())
    assert sha256_bytes864(_j882.dumps(PREREG878, sort_keys=True).encode()) == TEST878_PREREG882, 'TEST878_PREREG_MISMATCH'
    exec(compile(_a882.fix_missing_locations(_a882.Module(f8, [])), '878.py:selected', 'exec'), globals())
    _, _, f0 = select_nodes882('880.py', (), (), FUNCS880)
    for n in f0: scan882(n)
    exec(compile(_a882.fix_missing_locations(_a882.Module(f0, [])), '880.py:selected', 'exec'), globals())
    c1, k1, f1 = select_nodes882('881.py', CONSTS881, CLASSES881, FUNCS881)
    for n in k1 + f1:
        for m in ([n] if isinstance(n, _a882.FunctionDef) else [x for x in n.body if isinstance(x, _a882.FunctionDef)]):
            scan882(m)
    exec(compile(_a882.fix_missing_locations(_a882.Module(c1 + k1 + f1, [])), '881.py:selected', 'exec'), globals())
    logs = {k: RAW_SOURCES864[f].decode() for k, f in (('878', 'Test_878_log2.log'), ('879', '879.log'), ('880', '880.log'),
                                                       ('881', '881.log'))}
    prov = {'878': all(x in logs['878'] for x in ('NVIDIA A100-SXM4-80GB', 'cell %s | prereg %s' % (LOCKS864['878.py'],
                                                  TEST878_PREREG882[:16]), 'TEST878 | status COMPLETE')),
            '879': all(x in logs['879'] for x in ('NVIDIA A100-SXM4-80GB', 'prereg 6b7d8639d93b2110',
                                                  'TEST879 VERDICT MATCHED_FORK_OUTCOME_TRANSFER', 'status COMPLETE')),
            '880': all(x in logs['880'] for x in ('TEST880 NCRA CLOSED-LOOP ENGINE | GPU NVIDIA A100-SXM4-80GB',
                                                  'TEST880 VERDICT CLOSED_LOOP_NO_SELF_REUSE', 'status COMPLETE')),
            '881': all(x in logs['881'] for x in ('GPU NVIDIA A100-SXM4-80GB | head 6bd3c52bf60e | cell %s' %
                                                  TEST881_EXECUTED_CELL_IN_LOG882, 'TEST881 VERDICT MASKED_PATH_C_SPECIFIC_SIGNAL',
                                                  'status COMPLETE | wall 1472 s'))}
    assert all(prov.values()), ('LOCKED_LOG_PROVENANCE', prov)
    STATE882['source']['reused'] = {'878.py': LOCKS864['878.py'], 'functions878': sorted(FUNCS878), 'constants878': len(c8),
                                    '880.py': LOCKS864['880.py'], 'functions880': sorted(FUNCS880),
                                    '881.py': LOCKS864['881.py'], 'classes881': sorted(CLASSES881), 'functions881': sorted(FUNCS881),
                                    'constants881': len(c1), 'head': HEAD882,
                                    'test881_blobs': {'committed': TEST881_COMMITTED_BLOB882, 'executed_cell_in_log': TEST881_EXECUTED_CELL_IN_LOG882},
                                    'locked_gpu_logs': 'provenance only (string presence in blob-locked logs), not a new runtime PASS'}
    return logs['879']

# ============================ pure core (CPU-testable; no model, no labels) ============================
def rows_np882(r):
    if hasattr(r, 'detach'): r = r.detach().float().cpu().contiguous().numpy()
    return _np882.ascontiguousarray(_np882.asarray(r, dtype=_np882.float32))


def digest_segments882(segments):
    h = _h882.sha256()
    for slot, rows in segments:
        h.update(_j882.dumps([int(x) for x in slot]).encode())
        if rows is None:
            h.update(b'NONE'); continue
        a = rows_np882(rows); h.update(_j882.dumps(list(a.shape)).encode()); h.update(a.tobytes())
    return h.hexdigest()


def address_input882(zcap):
    # the only bytes the address encoder and the need reader may see: the pre-action segments of one captured decision state
    if zcap.get('phase') != 'PRE_ACTION': raise Gate882('ADDRESS_INPUT_NOT_PRE_ACTION')
    segs = [(list(s), r) for s, r in zcap['segments']]
    return segs, digest_segments882(segs)


def addr_prompt_ids882(prompt_ids, tok_ids, q, retry=False):
    pre = list(prompt_ids((ADDR_RETRY_PROMPT882 if retry else ADDR_PROMPT882).format(q=q)))
    post = list(tok_ids(ADDR_SUFFIX882))
    return pre, post, _h882.sha256(_j882.dumps([pre, post]).encode()).hexdigest()


def domain882(memnull_seal, mu_sha, weights):
    d = {'encoder': ENCODER882, 'write_read_prompt': _h882.sha256((ADDR_PROMPT882 + '\x00' + ADDR_SUFFIX882).encode()).hexdigest(),
         'memory': 'MEMNULL841', 'memnull_seal': memnull_seal, 'mu_addr_sha256': mu_sha, 'score': 'peak50_841',
         'weights_digest': weights}
    return _h882.sha256(_j882.dumps(d, sort_keys=True, default=str).encode()).hexdigest(), d


def key_blob882(key, meta):
    a = rows_np882(key); raw = a.tobytes()
    return {'blob': raw, 'meta': dict(meta, shape=list(a.shape), dtype='float32', address_sha256=_h882.sha256(raw).hexdigest())}


def key_from_blob882(blob, shape):
    return _np882.frombuffer(blob, dtype=_np882.float32).reshape(shape).copy()


def make_view882(entries):
    # runtime candidate view: exactly the whitelisted opaque fields, nothing else (no file name, no provenance, no label)
    view = {}
    for e in entries:
        if set(e) != set(VIEW_FIELDS882):
            raise Gate882('VIEW_METADATA_NOT_WHITELISTED %s' % sorted(set(e) ^ set(VIEW_FIELDS882)))
        if e['id'] in view: raise Gate882('VIEW_DUPLICATE_ID ' + str(e['id']))
        view[e['id']] = dict(e)
    return view


def freeze_thresholds882(values, scope, provenance):
    vals = {'tau_neg': float(values['tau_neg']), 'delta_tie': float(values['delta_tie'])}
    if not all(_m882.isfinite(v) for v in vals.values()): raise Gate882('THRESHOLD_NOT_FINITE %s' % vals)
    TH = {'scope': scope, 'values': vals, 'provenance': provenance, 'frozen': True}
    TH['sha256'] = _h882.sha256(_j882.dumps({k: TH[k] for k in ('scope', 'values', 'provenance')}, sort_keys=True,
                                             default=str).encode()).hexdigest()
    if scope == 'LIVE':
        if FROZEN882.get('TH') is not None: raise Gate882('THRESHOLDS_ALREADY_FROZEN')
        FROZEN882['TH'], FROZEN882['sha256'] = TH, TH['sha256']
    return TH


def thresholds_check882(TH, scope):
    if not (isinstance(TH, dict) and TH.get('frozen') is True and TH.get('scope') == scope): raise Gate882('THRESHOLDS_NOT_FROZEN')
    sha = _h882.sha256(_j882.dumps({k: TH[k] for k in ('scope', 'values', 'provenance')}, sort_keys=True,
                                   default=str).encode()).hexdigest()
    if sha != TH['sha256']: raise Gate882('THRESHOLDS_MUTATED')
    if scope == 'LIVE' and (FROZEN882.get('TH') is not TH or FROZEN882.get('sha256') != sha):
        raise Gate882('LIVE_THRESHOLDS_ARE_NOT_THE_FROZEN_ONES')
    return TH['values']['tau_neg'], TH['values']['delta_tie']


def route882(Q, view, null_key, TH, score, exclude=(), scope='LIVE'):
    # CPU router over opaque key sidecars: one rank-1 proposal or a named refusal; it never proposes rank 2
    tau, delta = thresholds_check882(TH, scope)
    rec = {'scope': scope, 'tau_neg': tau, 'delta_tie': delta, 'threshold_sha256': TH['sha256'], 'excluded': sorted(exclude),
           'candidates': [], 'scores': {}, 'null': None, 'top3': [], 'margin': None, 'margin_vs_null': None,
           'decision': None, 'chosen': None, 'reasons': []}
    if Q is None:
        rec['decision'] = 'INVALID_QUERY'; return rec
    ids = sorted(c for c in view if c not in set(exclude)); rec['candidates'] = ids
    if not ids:
        rec['decision'] = 'NO_CANDIDATE'; return rec
    sc = {c: float(score(Q, view[c]['address_key'])) for c in ids}; sn = float(score(Q, null_key))
    rec['scores'], rec['null'] = sc, sn
    if not all(_m882.isfinite(v) for v in list(sc.values()) + [sn]):
        rec['decision'] = 'INVALID_SCORE'; return rec
    ranked = sorted(sc.items(), key=lambda kv: (-kv[1], kv[0])); rec['top3'] = [[c, s] for c, s in ranked[:3]]
    c1, s1 = ranked[0]; many = len(ranked) > 1; s2 = ranked[1][1] if many else None
    rec['margin'] = (s1 - s2) if many else None; rec['margin_vs_null'] = s1 - sn
    why = []
    if any(c != c1 and view[c]['address_sha256'] == view[c1]['address_sha256'] for c in ids): why.append('EXACT_DUPLICATE_KEY')
    if many and s1 == s2: why.append('EXACT_SCORE_TIE')
    if s1 <= sn: why.append('S1_LE_NULL')
    if s1 <= tau: why.append('S1_LE_TAU_NEG')
    if many and s1 - s2 <= delta: why.append('MARGIN_LE_DELTA_TIE')
    rec['reasons'] = why
    if 'EXACT_DUPLICATE_KEY' in why or 'EXACT_SCORE_TIE' in why: rec['decision'] = 'TIE_NO_MOUNT'
    elif 'S1_LE_NULL' in why or 'S1_LE_TAU_NEG' in why: rec['decision'] = 'NO_MATCH'
    elif 'MARGIN_LE_DELTA_TIE' in why: rec['decision'] = 'AMBIGUOUS_NO_MOUNT'
    else: rec['decision'], rec['chosen'] = 'ACCEPT', c1
    return rec


def cal_view882(K):
    return make_view882([{'id': w, 'sha256': 'CALIBRATION_KEY_ONLY', 'tensor_sha': None, 'address_key': K[w],
                          'address_sha256': _h882.sha256(rows_np882(K[w]).tobytes()).hexdigest(), 'parent_id': None,
                          'parent_sha256': None, 'body_tokens': 0, 'requires_parent': False, 'generation': 0} for w in sorted(K)])


def calibrate882(Q, K, null_key, score, noise):
    # G3 only, before the live freeze: the (w, v) relation is a calibration-domain label; it never reaches the live router
    if FROZEN882.get('TH') is not None: raise Gate882('CALIBRATION_AFTER_LIVE_FREEZE')
    W = sorted(Q)
    if sorted(K) != W or len(W) < 3: raise Gate882('CALIBRATION_SET %s %s' % (W, sorted(K)))
    S = {w: {v: float(score(Q[w], K[v])) for v in W} for w in W}; N = {w: float(score(Q[w], null_key)) for w in W}
    if not all(_m882.isfinite(x) for w in W for x in list(S[w].values()) + [N[w]]): raise Gate882('CALIBRATION_NONFINITE')
    def neg_margin(w, drop=()):
        v = sorted((S[w][u] for u in W if u != w and u not in drop), reverse=True)
        return v[0] - v[1] if len(v) > 1 else 0.0
    neg = [S[w][v] for w in W for v in W if v != w]; pos = [S[w][w] for w in W]
    tau = max(neg); delta = max([DELTA_MIN882, 2.0 * float(noise)] + [neg_margin(w) for w in W])
    view = cal_view882(K)
    TH = freeze_thresholds882({'tau_neg': tau, 'delta_tie': delta}, 'CALIBRATION', {'kind': 'in-domain'})
    final = {w: route882(Q[w], view, null_key, TH, score, scope='CALIBRATION') for w in W}
    loo = {}
    for w in W:
        rest = [u for u in W if u != w]
        t_w = max(S[u][v] for u in rest for v in rest if v != u)
        d_w = max([DELTA_MIN882, 2.0 * float(noise)] + [neg_margin(u, (w,)) for u in rest])
        th = freeze_thresholds882({'tau_neg': t_w, 'delta_tie': d_w}, 'CALIBRATION', {'kind': 'leave-context-out', 'out': w})
        loo[w] = route882(Q[w], view, null_key, th, score, scope='CALIBRATION')
    res = {'S': S, 'null': N, 'tau_neg': tau, 'delta_tie': delta, 'noise': float(noise), 'positives': pos, 'negatives': neg,
           'separation_min_pos_minus_max_neg': min(pos) - max(neg),
           'final': {w: {'decision': r['decision'], 'chosen': r['chosen'], 'reasons': r['reasons']} for w, r in final.items()},
           'loo': {w: {'decision': r['decision'], 'chosen': r['chosen'], 'reasons': r['reasons'], 'tau_neg': r['tau_neg'],
                       'delta_tie': r['delta_tie']} for w, r in loo.items()}}
    res['final_positive_accepted'] = sum(1 for w in W if final[w]['chosen'] == w)
    res['final_false_mounts'] = sum(1 for w in W if final[w]['chosen'] not in (None, w))
    res['loo_correct'] = sum(1 for w in W if loo[w]['chosen'] == w)
    res['loo_false_mounts'] = sum(1 for w in W if loo[w]['chosen'] not in (None, w))
    res['separation_pass'] = res['final_positive_accepted'] >= 1 and res['loo_correct'] >= 1 and res['loo_false_mounts'] == 0
    return res


def key_shuffle882(view):
    ids = sorted(view)
    if len(ids) < 2: return None
    return {c: dict(view[c], address_key=view[ids[(i + 1) % len(ids)]]['address_key'],
                    address_sha256=view[ids[(i + 1) % len(ids)]]['address_sha256']) for i, c in enumerate(ids)}


def id_shuffle882(view, salt):
    ren = {c: 'R882_' + _h882.sha256((salt + '|' + c).encode()).hexdigest()[:16] for c in view}
    out = {ren[c]: dict(v, id=ren[c], parent_id=ren.get(v['parent_id'], v['parent_id'])) for c, v in view.items()}
    return out, ren


def order_shuffle882(view):
    return {c: view[c] for c in reversed(list(view))}


def bite882(a, b):
    common = set(a['scores']) & set(b['scores'])
    scores_changed = set(a['scores']) != set(b['scores']) or any(a['scores'][c] != b['scores'][c] for c in common) or \
        a['null'] != b['null']
    decision_changed = a['decision'] != b['decision'] or a['chosen'] != b['chosen']
    return {'scores_changed': bool(scores_changed), 'decision_changed': bool(decision_changed),
            'bite': bool(scores_changed or decision_changed)}


def same_route882(a, b, ren=None):
    m = (lambda c: c) if ren is None else (lambda c: ren.get(c, c))
    return (a['decision'] == b['decision'] and (a['chosen'] is None) == (b['chosen'] is None) and
            (a['chosen'] is None or m(a['chosen']) == b['chosen']) and
            {m(c): s for c, s in a['scores'].items()} == b['scores'] and a['null'] == b['null'])


def resolve_parent882(eid, rows, mounted=(), verify=None):
    # SHA-checked parent chain (root first); depth <= MAX_PARENT_DEPTH882; cycle / dangling / stale = INTEGRITY_BLOCK;
    # an already mounted ancestor is never appended again
    by = {}
    for r in rows:
        if r['id'] in by: raise IntegrityBlock881('DUPLICATE_CATALOG_ID ' + r['id'])
        by[r['id']] = r
    if eid not in by: raise IntegrityBlock881('UNKNOWN_ID ' + str(eid))
    cur = by[eid]; chain = [cur]; seen = {eid}
    while cur.get('requires_parent'):
        pid = cur.get('parent_id')
        if not pid: raise IntegrityBlock881('MISSING_PARENT_ID ' + cur['id'])
        if pid in seen: raise IntegrityBlock881('PARENT_CYCLE ' + cur['id'])
        if pid not in by: raise IntegrityBlock881('DANGLING_PARENT ' + cur['id'])
        p = by[pid]
        if p['sha256'] != cur.get('parent_sha256'): raise IntegrityBlock881('STALE_PARENT_SHA ' + cur['id'])
        if int(p['generation']) >= int(cur['generation']): raise IntegrityBlock881('STALE_PARENT_GENERATION ' + cur['id'])
        chain.insert(0, p); seen.add(pid); cur = p
        if len(chain) > MAX_PARENT_DEPTH882: raise IntegrityBlock881('PARENT_DEPTH %d' % len(chain))
    if verify is not None:
        for r in chain: verify(r)
    ids = [r['id'] for r in chain]; mset = set(mounted)
    if eid in mset: raise IntegrityBlock881('DUPLICATE_APPEND ' + eid)
    pre = [i for i in ids if i in mset]
    if pre != ids[:len(pre)]: raise IntegrityBlock881('MOUNTED_SET_NOT_A_CHAIN_PREFIX')
    return {'chain': ids, 'append': ids[len(pre):], 'already_mounted': pre, 'depth': len(ids)}


def next_attempt882(ledger, outcome):
    # bounded recovery: one new native query at most; there is no branch that mounts a lower-ranked candidate
    if outcome == 'ACCEPT_KEEP': return 'USE'
    if outcome in ('NO_MATCH', 'TIE_NO_MOUNT', 'AMBIGUOUS_NO_MOUNT', 'MODEL_REJECT', 'INVALID_QUERY') and \
            ledger['retries_used'] < MAX_RETRY882:
        ledger['retries_used'] += 1
        return 'NEW_QUERY'
    return 'STOP'


def ffe882(tokens, layers=80, kind='adapter'):
    x = float(tokens) * float(layers) / 80.0 / 256.0; b = STATE882['budget']
    b['adapter_ffe_lower_bound'] += x; b['ffe_by_kind'][kind] = b['ffe_by_kind'].get(kind, 0.0) + x
    return x


def eid882(prov):
    return 'X882_' + _h882.sha256(_j882.dumps(prov, sort_keys=True, default=str).encode()).hexdigest()[:12]


def supported882(effect, card_kind, node_class):
    # OFFLINE (G9) executor-state rule of TEST881; the model observation never enters it
    return bool((effect == 'MOUNTED' and card_kind == 'second') or (effect == 'UNMOUNTED' and card_kind in ('fork', 'decoy')) or
                (effect == 'POINTER_ADVANCED' and node_class == 'middle'))


def d1_skeleton882():
    return {'environment_effect': None, 'model_observation': None, 'model_evidence': None, 'offline': None,
            'store': {'decision': None, 'written': None, 'why': 'NOT_REACHED'}, 'executed': None, 'status': 'NOT_RUN'}


# ============================ append-only REAL store with address-key sidecar (pure Python; extends RealStore881) ============================
class RealStore882(RealStore881):
    # <id>.pt + <id>.addr.json (pre-C address key) + <id>.entry.json (address SHA + parent pointer) + catalog.jsonl, one transaction

    @staticmethod
    def write_json_atomic(path, obj):
        tmp = path + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            f.write(_j882.dumps(obj, sort_keys=True)); f.flush(); _o882.fsync(f.fileno())
        _o882.replace(tmp, path)

    @staticmethod
    def read_address(path):
        d = _j882.loads(open(path, encoding='utf-8').read()); blob = _b64882.b64decode(d['b64'])
        if _h882.sha256(blob).hexdigest() != d['address_sha256']: raise IntegrityBlock881('ADDRESS_SIDECAR_SHA ' + path)
        return blob, d

    @staticmethod
    def row882(eid, entry, gen, recovered=False):
        row = {'id': eid, 'file': entry['file'], 'sha256': entry['sha256'], 'address_sha256': entry['address_sha256'],
               'address_file': entry['address_file'], 'entry': entry, 'requires_parent': bool(entry['requires_parent']),
               'parent_id': entry['parent_id'], 'parent_sha256': entry['parent_sha256'], 'generation': gen}
        if recovered: row['recovered'] = True
        return row

    def commit(self, eid, data_dir, write, verify, addr, parent=None, fault=None, existing=None, prewritten=False):
        state = 'START'; ff = (lambda s: None) if fault is None else fault['fn']
        rows, tail = self.read_catalog()
        if tail: raise CommitUncertain881('PARTIAL_CATALOG_TAIL_BEFORE_COMMIT')
        asha = _h882.sha256(addr['blob']).hexdigest()
        hit = [r for r in rows if r['id'] == eid]
        if hit:                                          # idempotency: compare content without touching the committed files
            if existing is None: raise IntegrityBlock881('ID_EXISTS_CONTENT_UNKNOWN ' + eid)
            if tuple(existing) != (hit[0]['sha256'], hit[0]['address_sha256']): raise IntegrityBlock881('ID_EXISTS_DIFFERENT_SHA ' + eid)
            return {'entry': hit[0]['entry'], 'state': 'IDEMPOTENT_NO_OP', 'generation': hit[0]['generation']}
        if parent is not None:
            pr = [r for r in rows if r['id'] == parent[0]]
            if not pr or pr[0]['sha256'] != parent[1]: raise IntegrityBlock881('PARENT_NOT_COMMITTED_OR_STALE ' + str(parent[0]))
        path = _o882.path.join(data_dir, eid + '.pt'); af = _o882.path.join(data_dir, eid + '.addr.json')
        side = _o882.path.join(data_dir, eid + '.entry.json')
        if _o882.path.exists(path) != bool(prewritten) or _o882.path.exists(af) or _o882.path.exists(side):
            raise CommitUncertain881('FILE_STATE_UNEXPECTED ' + eid)
        try:
            entry = dict(write(data_dir)); state = 'FILE_RENAMED'
            assert entry['file'] == path and _o882.path.exists(path), 'WRITER_PATH'
            self.fsync_file(path); state = 'FILE_FSYNC'; ff(state)
            self.write_json_atomic(af, {'id': eid, 'b64': _b64882.b64encode(addr['blob']).decode('ascii'), 'address_sha256': asha,
                                        'meta': addr['meta']}); state = 'ADDRESS_SIDECAR'; ff(state)
            self.fsync_file(af); state = 'ADDRESS_FSYNC'; ff(state)
            entry.update({'address_sha256': asha, 'address_file': af, 'requires_parent': parent is not None,
                          'parent_id': None if parent is None else parent[0], 'parent_sha256': None if parent is None else parent[1]})
            self.write_json_atomic(side, entry); state = 'ENTRY_SIDECAR'; ff(state)
            self.fsync_dir(data_dir); state = 'DIR_FSYNC'; ff(state)
            if self.sha_file(path) != entry['sha256']: raise IntegrityBlock881('WRITTEN_FILE_SHA ' + eid)
            blob, _ = self.read_address(af)
            if blob != addr['blob']: raise IntegrityBlock881('ADDRESS_RELOAD ' + eid)
            verify(entry); state = 'VERIFIED_RELOAD'; ff(state)
            gen = self.generation(rows)
            self.append_line(self.row882(eid, entry, gen), fault); state = 'COMMITTED'
            return {'entry': entry, 'state': state, 'generation': gen}
        except IntegrityBlock881:
            raise
        except BaseException as exc:
            raise CommitUncertain881('%s after %s: %s' % (type(exc).__name__, state, exc))

    def recover(self, verify):
        rep = {'tail_repaired': None, 'quarantined': [], 'recatalogued': [], 'verified': 0}
        rows, tail = self.read_catalog()
        if tail:
            tmp = self.catalog + '.tail'
            with open(tmp, 'wb') as f: f.write(tail); f.flush(); _o882.fsync(f.fileno())
            rep['quarantined'].append(self.quarantine(tmp, 'PARTIAL_CATALOG_TAIL'))
            good = open(self.catalog, 'rb').read()[:-len(tail)]; ctmp = self.catalog + '.rewrite'
            with open(ctmp, 'wb') as f: f.write(good); f.flush(); _o882.fsync(f.fileno())
            _o882.replace(ctmp, self.catalog); self.fsync_dir(self.root); rep['tail_repaired'] = len(tail)
        seen, last = {}, 0
        for r in rows:
            if r['id'] in seen: raise IntegrityBlock881('DUPLICATE_CATALOG_ENTRY ' + r['id'])
            if not _o882.path.exists(r['file']) or self.sha_file(r['file']) != r['sha256']:
                raise IntegrityBlock881('DANGLING_OR_CORRUPT_POINTER ' + r['id'])
            if not r.get('address_file') or not _o882.path.exists(r['address_file']):
                raise IntegrityBlock881('ADDRESS_SIDECAR_MISSING ' + r['id'])
            blob, _ = self.read_address(r['address_file'])
            if _h882.sha256(blob).hexdigest() != r['address_sha256']: raise IntegrityBlock881('ADDRESS_SHA ' + r['id'])
            if r.get('requires_parent') and seen.get(r.get('parent_id')) != r.get('parent_sha256'):
                raise IntegrityBlock881('DANGLING_OR_STALE_PARENT ' + r['id'])
            if int(r['generation']) <= last: raise IntegrityBlock881('GENERATION_NOT_MONOTONIC ' + r['id'])
            last = int(r['generation']); verify(r['entry']); seen[r['id']] = r['sha256']; rep['verified'] += 1
        for d in self.dirs:
            for name in sorted(_o882.listdir(d)):
                p = _o882.path.join(d, name)
                if not _o882.path.exists(p): continue
                if name.endswith('.pt'):
                    eid = name[:-3]
                    if eid in seen: continue
                    side = _o882.path.join(d, eid + '.entry.json'); af = _o882.path.join(d, eid + '.addr.json'); ok = False
                    try:
                        entry = _j882.loads(open(side, encoding='utf-8').read()); blob, _ = self.read_address(af)
                        ok = (entry.get('file') == p and self.sha_file(p) == entry.get('sha256') and entry.get('address_file') == af
                              and entry.get('address_sha256') == _h882.sha256(blob).hexdigest())
                        if ok and entry.get('requires_parent'): ok = seen.get(entry.get('parent_id')) == entry.get('parent_sha256')
                        if ok: verify(entry)
                    except Exception:
                        ok = False
                    if ok:
                        rows2, _ = self.read_catalog()
                        self.append_line(self.row882(eid, entry, self.generation(rows2), recovered=True))
                        seen[eid] = entry['sha256']; rep['recatalogued'].append(eid)
                    else:
                        for x in (p, side, af):
                            if _o882.path.exists(x): rep['quarantined'].append(self.quarantine(x, 'ORPHAN_WITHOUT_VALID_SIDECARS'))
                elif name.endswith('.tmp'):
                    rep['quarantined'].append(self.quarantine(p, 'TEMPORARY_FILE'))
                elif name.endswith('.entry.json') or name.endswith('.addr.json'):
                    base = name[:-len('.entry.json')] if name.endswith('.entry.json') else name[:-len('.addr.json')]
                    if base not in seen and not _o882.path.exists(_o882.path.join(d, base + '.pt')):
                        rep['quarantined'].append(self.quarantine(p, 'SIDECAR_WITHOUT_FILE'))
        rows, tail = self.read_catalog()
        assert not tail and all(_o882.path.exists(r['file']) and _o882.path.exists(r['address_file']) for r in rows), \
            'RECOVERY_POSTCONDITION'
        return rep

    def rows(self):
        rows, tail = self.read_catalog()
        if tail: raise IntegrityBlock881('CATALOG_TAIL_AT_READ')
        return rows


# ============================ verdict linter (pure; reads the run summary only) ============================
def verdict_logic882(s):
    labels, primary = [], None
    if s.get('blocks'): primary = 'TECHNICAL_BLOCK'
    elif not s.get('g3_pass'): primary = 'REVISE_ADDRESS_DOMAIN'
    c1 = s.get('c1') or {}
    if primary is None:
        if c1.get('need') != 'USE_MEMORY': primary = 'NO_NATURAL_NEED_MEMORY'
        elif not c1.get('kept'):
            primary = 'NO_MATCH_ABSTENTION'
            if c1.get('mounted_any'): labels.append('POST_MOUNT_MODEL_REJECT')
        elif c1.get('kept_relevant'): primary = 'AUTONOMOUS_PHYSICAL_MOUNT'
        else: primary = 'AUTONOMOUS_PHYSICAL_MOUNT_OFFLINE_IRRELEVANT'
    if primary in ('AUTONOMOUS_PHYSICAL_MOUNT', 'AUTONOMOUS_PHYSICAL_MOUNT_OFFLINE_IRRELEVANT'):
        if c1.get('first_selection_accepted') and c1.get('first_selection_relevant'): labels.append('OFFLINE_RELEVANT_SELECTION')
        if c1.get('kept_after_retry'): labels.append(c1.get('retry_label') or 'RETRY_ACCEPTED')
        if c1.get('readout_pass') and c1.get('vis_argmax_differs_from_c_blind'): labels.append('MEMORY_DEPENDENT_POLICY_CHANGE')
    d1 = s.get('d1') or {}
    if primary not in ('TECHNICAL_BLOCK', 'REVISE_ADDRESS_DOMAIN'):
        if not d1.get('executed'): labels.append('NO_EXECUTION_NO_ACCEPTED_MEMORY' if not c1.get('kept') else 'NO_EXECUTION')
        elif d1.get('supported'): labels.append('SUPPORTED_SINGLE_TRANSITION_DESCRIPTIVE')
        if d1.get('store') == 'DISCARD': labels.append('NO_STORE_DISCARD')
        if not d1.get('written'): labels += ['NO_NEW_MEMORY_WRITTEN', 'SELF_REUSE_NOT_RUN']
    d2 = s.get('d2') or {}
    mech = bool(d1.get('written') and d2.get('own_cartridge_selected') and d2.get('parent_seal_equal') and d2.get('mount_pass')
                and d2.get('readout_pass') and d2.get('vis_exact') and d2.get('executed_equals_vis'))
    if d1.get('written') and not d2.get('run'): labels.append('SELF_REUSE_NOT_RUN')
    if mech:
        labels.append('PARENT_CONDITIONED_SELF_REUSE_MECHANICAL')
        if d2.get('vis_action') != d2.get('no_memory_action'): labels.append('SELF_REUSE_POLICY_CHANGE')
    else:
        labels.append('CLOSED_LOOP_NOT_ESTABLISHED')
    for c in s.get('controls_did_not_bite') or []: labels.append('CONTROL_DID_NOT_BITE:' + c)
    if s.get('false_mount_wrong_only'): labels.append('FALSE_MOUNT_WRONG_ONLY')
    if s.get('cross_goal_false_mount'): labels.append('CROSS_GOAL_FALSE_MOUNT')
    ctrl_ok = bool(s.get('controls_pass')) and not s.get('controls_did_not_bite')
    mech_go = bool(primary in ('AUTONOMOUS_PHYSICAL_MOUNT', 'AUTONOMOUS_PHYSICAL_MOUNT_OFFLINE_IRRELEVANT') and c1.get('readout_pass')
                   and d1.get('executed') and d1.get('executed_equals_vis') and ctrl_ok)
    sem_go = bool(mech_go and 'OFFLINE_RELEVANT_SELECTION' in labels and s.get('empty_safe') and s.get('tie_safe')
                  and not s.get('false_mount_wrong_only'))
    seen, out = set(), []
    for x in labels:
        if x not in seen: seen.add(x); out.append(x)
    assert primary in VERDICTS882 and all(x.split(':')[0] in VERDICTS882 + LABELS_EXTRA882 for x in out), ('VERDICT_LINT', primary, out)
    return {'verdict': primary, 'labels': out, 'mechanical_go': mech_go, 'semantic_go': sem_go}


LABELS_EXTRA882 = ('POST_MOUNT_MODEL_REJECT', 'RETRY_ACCEPTED', 'RETRY_ACCEPTED_AFTER_FIRST_NO_MATCH',
                   'RETRY_ACCEPTED_AFTER_MODEL_REJECT', 'NO_EXECUTION_NO_ACCEPTED_MEMORY', 'NO_EXECUTION', 'CONTROL_DID_NOT_BITE',
                   'FALSE_MOUNT_WRONG_ONLY', 'CROSS_GOAL_FALSE_MOUNT')

# ============================ CPU-only selftests (a)-(n), before the model is loaded; every entry is a real assertion ============================
def score_py882(Q, K):
    q, k = rows_np882(Q).astype(_np882.float64), rows_np882(K).astype(_np882.float64)
    return float((q @ k.T).max(axis=1).mean())


def entry_py882(cid, key, gen=1, parent=None):
    k = rows_np882(key)
    return {'id': cid, 'sha256': 'F_' + cid, 'tensor_sha': None, 'address_key': k,
            'address_sha256': _h882.sha256(k.tobytes()).hexdigest(), 'parent_id': None if parent is None else parent[0],
            'parent_sha256': None if parent is None else parent[1], 'body_tokens': 1, 'requires_parent': parent is not None,
            'generation': gen}


def rsel882(*a, **k):
    return route882(*a, scope='SELFTEST', **k)


def frozen_py882(tau, delta):
    return freeze_thresholds882({'tau_neg': tau, 'delta_tie': delta}, 'SELFTEST', {'kind': 'selftest'})


def st_a882():
    f = _np882.float32; seg = [([1, 2], _np882.arange(6, dtype=f).reshape(2, 3)), ([3], _np882.ones((1, 3), dtype=f))]
    z = {'phase': 'PRE_ACTION', 'qid': 'q', 'segments': seg, 'post_action': {'A': [5], 'C': _np882.zeros((2, 3), dtype=f)}}
    _, d0 = address_input882(z)
    z_c = dict(z, post_action={'A': [5], 'C': _np882.full((2, 3), 7.0, dtype=f)})
    z_a = dict(z, post_action={'A': [9, 9], 'C': z['post_action']['C']})
    seg_x = [(s, r.copy()) for s, r in seg]; seg_x[0][1][0, 0] += 1e-3
    seg_s = [([1, 4], seg[0][1]), seg[1]]
    res = {'C_change_keeps_key_input': address_input882(z_c)[1] == d0, 'A_change_keeps_key_input': address_input882(z_a)[1] == d0,
           'X2_change_changes_key_input': address_input882(dict(z, segments=seg_x))[1] != d0,
           'slot_change_changes_key_input': address_input882(dict(z, segments=seg_s))[1] != d0}
    try: address_input882(dict(z, phase='POST_ACTION')); res['post_action_input_refused'] = False
    except Gate882: res['post_action_input_refused'] = True
    return res


def st_b882():
    pid = lambda s: [ord(c) % 251 for c in s]; tid = lambda s: [ord(c) % 97 for c in s]
    k = addr_prompt_ids882(pid, tid, 'Q1'); q = addr_prompt_ids882(pid, tid, 'Q1'); r = addr_prompt_ids882(pid, tid, 'Q1', retry=True)
    d1, _ = domain882({'seal': 'a'}, 'mu1', 'w'); d2, _ = domain882({'seal': 'a'}, 'mu1', 'w')
    return {'write_read_prompt_ids_identical': k == q, 'retry_prompt_differs': r[2] != k[2] and r[1] == k[1],
            'domain_deterministic': d1 == d2, 'domain_depends_on_memnull_seal': domain882({'seal': 'b'}, 'mu1', 'w')[0] != d1,
            'domain_depends_on_mu': domain882({'seal': 'a'}, 'mu2', 'w')[0] != d1,
            'domain_depends_on_weights': domain882({'seal': 'a'}, 'mu1', 'w2')[0] != d1,
            'suffix_identical_for_key_and_query': k[1] == q[1] == list(tid(ADDR_SUFFIX882))}


def st_c882():
    e = lambda *v: _np882.array([v], dtype=_np882.float32)
    Q, null = e(1.0, 0.0), e(0.0, 1.0)
    good = make_view882([entry_py882('a', e(0.9, 0.1)), entry_py882('b', e(0.2, 0.8)), entry_py882('c', e(0.1, 0.1))])
    th = frozen_py882(0.3, 0.05); res = {}
    r = rsel882(Q, good, null, th, score_py882); res['accept'] = r['decision'] == 'ACCEPT' and r['chosen'] == 'a'
    dup = make_view882([entry_py882('a', e(0.9, 0.1)), entry_py882('b', e(0.9, 0.1)), entry_py882('c', e(0.1, 0.1))])
    r = rsel882(Q, dup, null, th, score_py882)
    res['exact_duplicate_tie'] = r['decision'] == 'TIE_NO_MOUNT' and 'EXACT_DUPLICATE_KEY' in r['reasons']
    res['empty_no_candidate'] = rsel882(Q, {}, null, th, score_py882)['decision'] == 'NO_CANDIDATE'
    nan = make_view882([entry_py882('a', e(float('nan'), 0.0)), entry_py882('b', e(0.1, 0.1))])
    res['nonfinite_invalid_score'] = rsel882(Q, nan, null, th, score_py882)['decision'] == 'INVALID_SCORE'
    r = rsel882(Q, good, e(5.0, 0.0), th, score_py882)
    res['s1_le_null_no_match'] = r['decision'] == 'NO_MATCH' and 'S1_LE_NULL' in r['reasons']
    r = rsel882(Q, good, null, frozen_py882(0.95, 0.05), score_py882)
    res['s1_le_tau_no_match'] = r['decision'] == 'NO_MATCH' and 'S1_LE_TAU_NEG' in r['reasons']
    close = make_view882([entry_py882('a', e(0.90, 0.1)), entry_py882('b', e(0.89, 0.2))])
    r = rsel882(Q, close, null, th, score_py882)
    res['margin_ambiguous'] = r['decision'] == 'AMBIGUOUS_NO_MOUNT' and 'MARGIN_LE_DELTA_TIE' in r['reasons']
    res['invalid_query'] = rsel882(None, good, null, th, score_py882)['decision'] == 'INVALID_QUERY'
    res['exclude_never_falls_back'] = rsel882(Q, good, null, th, score_py882, exclude=('a',))['chosen'] != 'a'
    return res


def st_d882():
    res = {}
    bad = 'def f882(x):\n    return OFFLINE882[x]\n', 'def f882(x):\n    return CAL_PAIRS882.get(x)\n', \
          "def f882(d):\n    return d['second']\n", 'def f882(relevant):\n    return relevant\n'
    for i, src in enumerate(bad):
        try: oracle_scan882(_a882.parse(src).body[0]); res['oracle_case_%d_refused' % i] = False
        except AssertionError: res['oracle_case_%d_refused' % i] = True
    saved = dict(FROZEN882)
    try:
        FROZEN882.clear(); FROZEN882['TH'] = {'scope': 'LIVE'}
        e = lambda *v: _np882.array([v], dtype=_np882.float32)
        try: calibrate882({'a': e(1, 0), 'b': e(0, 1), 'c': e(1, 1)}, {'a': e(1, 0), 'b': e(0, 1), 'c': e(1, 1)}, e(0, 0),
                          score_py882, 0.0); res['calibration_after_freeze_refused'] = False
        except Gate882: res['calibration_after_freeze_refused'] = True
    finally:
        FROZEN882.clear(); FROZEN882.update(saved)
    import inspect as _ins882
    res['router_signature_has_no_label_input'] = list(_ins882.signature(route882).parameters) == \
        ['Q', 'view', 'null_key', 'TH', 'score', 'exclude', 'scope']
    th = frozen_py882(0.1, 0.01)
    res['thresholds_carry_numbers_only'] = sorted(th['values']) == ['delta_tie', 'tau_neg'] and \
        all(isinstance(v, float) for v in th['values'].values())
    return res


def st_e882():
    e = _np882.zeros((1, 2), dtype=_np882.float32); base = entry_py882('a', e); res = {}
    for k, v in (('role', 'x'), ('file', '/x.pt'), ('world', '00'), ('correct', True)):
        try: make_view882([dict(base, **{k: v})]); res['extra_field_%s_refused' % k] = False
        except Gate882: res['extra_field_%s_refused' % k] = True
    try: make_view882([{k: v for k, v in base.items() if k != 'generation'}]); res['missing_field_refused'] = False
    except Gate882: res['missing_field_refused'] = True
    cases = {'alias': ('def f882():\n    g = execute866\n    g()\n', False), 'getattr': ("def f882(m):\n    getattr(m, 'register_forward_hook')(1)\n", False),
             'attr': ('def f882(m):\n    m.register_forward_hook(1)\n', False), 'kw': ('def f882(m):\n    m(output_hidden_states=True)\n', False),
             'subscript': ("def f882(env):\n    return env['native_append_direct']\n", False),
             'global_access': ("def f882():\n    return globals()['X']\n", True), 'eval': ("def f882(s):\n    return eval(s)\n", True)}
    for k, (src, rt) in cases.items():
        try: scan882(_a882.parse(src).body[0], runtime=rt); res['firewall_%s_refused' % k] = False
        except AssertionError: res['firewall_%s_refused' % k] = True
    try: scan882(_a882.parse('def f882(x):\n    step = x + 1\n    return step\n').body[0]); res['data_name_step_allowed'] = True
    except AssertionError: res['data_name_step_allowed'] = False
    res['real_prompts_clean'] = not prompt_lint882([ADDR_PROMPT882, ADDR_RETRY_PROMPT882, NEED_PROMPT882, VALID_PROMPT882,
                                                     ADDR_SUFFIX882, NEED_SUFFIX882, VALID_SUFFIX882])
    res['oracle_word_in_prompt_detected'] = bool(prompt_lint882(['Describe the second option of this World.']))
    return res


def st_f882():
    row = lambda i, g, p=None, sha=None: {'id': i, 'sha256': sha or ('S' + i), 'generation': g, 'requires_parent': p is not None,
                                          'parent_id': p, 'parent_sha256': None if p is None else 'S' + p}
    def blocked(fn):
        try: fn(); return False
        except IntegrityBlock881: return True
    ok = resolve_parent882('c', [row('p', 1), row('c', 2, 'p')])
    res = {'chain_parent_first': ok['chain'] == ['p', 'c'] and ok['append'] == ['p', 'c'],
           'missing_parent_blocks': blocked(lambda: resolve_parent882('c', [row('c', 2, 'p')])),
           'wrong_parent_sha_blocks': blocked(lambda: resolve_parent882('c', [row('p', 1, sha='OTHER'), row('c', 2, 'p')])),
           'cycle_blocks': blocked(lambda: resolve_parent882('a', [row('a', 2, 'b'), row('b', 1, 'a')])),
           'depth_gt2_blocks': blocked(lambda: resolve_parent882('c', [row('r', 1), row('p', 2, 'r'), row('c', 3, 'p')])),
           'stale_generation_blocks': blocked(lambda: resolve_parent882('c', [row('p', 5), row('c', 2, 'p')])),
           'duplicate_catalog_id_blocks': blocked(lambda: resolve_parent882('p', [row('p', 1), row('p', 1)])),
           'child_already_mounted_blocks': blocked(lambda: resolve_parent882('c', [row('p', 1), row('c', 2, 'p')], mounted=('p', 'c'))),
           'mounted_parent_not_appended_twice': resolve_parent882('c', [row('p', 1), row('c', 2, 'p')], mounted=('p',))['append'] == ['c']}
    return res


def st_g882():
    # RoPE re-phase principle on a synthetic tensor (float64 and float32): P+j -> n0+j -> P+j roundtrip; a wrong target is detected
    rng = _np882.random.default_rng(882); d = 16; inv = 1.0 / (1e6 ** (_np882.arange(0, d, 2) / d))
    def rot(x, pos, sign=1.0):
        ang = sign * _np882.outer(pos, inv); c, s = _np882.cos(ang).astype(x.dtype), _np882.sin(ang).astype(x.dtype)
        x1, x2 = x[:, :d // 2], x[:, d // 2:]
        return _np882.concatenate([x1 * c - x2 * s, x1 * s + x2 * c], axis=-1)
    reph = lambda x, a, b: rot(rot(x, a, -1.0), b)
    P, n0, q = 30, 412, 64; pa, pb = _np882.arange(P, P + q), _np882.arange(n0, n0 + q)
    res = {}
    for dt in (_np882.float64, _np882.float32):
        k = rng.standard_normal((q, d)).astype(dt); back = reph(reph(k, pa, pb), pb, pa)
        rel = float(_np882.linalg.norm(back - k) / _np882.linalg.norm(k)); res['roundtrip_rel_%s' % dt.__name__] = rel
        wrong = reph(reph(k, pa, pb), pb + 1, pa)
        res['wrong_position_rel_%s' % dt.__name__] = float(_np882.linalg.norm(wrong - k) / _np882.linalg.norm(k))
    res['roundtrip_within_tol'] = max(res['roundtrip_rel_float64'], res['roundtrip_rel_float32']) <= 1e-5
    res['wrong_position_detected'] = min(res['wrong_position_rel_float64'], res['wrong_position_rel_float32']) > 1e-2
    k = rng.standard_normal((q, d)); pc = _np882.arange(900, 900 + q)
    res['rephase_composes'] = bool(_np882.allclose(reph(reph(k, pa, pb), pb, pc), reph(k, pa, pc), atol=1e-10))
    res['rephase_preserves_norm'] = bool(_np882.allclose(_np882.linalg.norm(reph(k, pa, pb), axis=1), _np882.linalg.norm(k, axis=1)))
    return res


def st_i882():
    res, root = {}, _tf882.mkdtemp(prefix='t882_store_selftest_')
    def writer(content, eid, crash=None):
        def w(d):
            p = _o882.path.join(d, eid + '.pt'); tmp = p + '.tmp'
            with open(tmp, 'wb') as f: f.write(content); f.flush(); _o882.fsync(f.fileno())
            if crash == 'TMP_WRITTEN': raise RuntimeError('INJECTED TMP_WRITTEN')
            _o882.replace(tmp, p)
            if crash == 'FILE_RENAMED': raise RuntimeError('INJECTED FILE_RENAMED')
            return {'id': eid, 'file': p, 'sha256': _h882.sha256(content).hexdigest()}
        return w
    def verify(entry):
        if RealStore882.sha_file(entry['file']) != entry['sha256']: raise IntegrityBlock881('VERIFY')
    addr = lambda b: {'blob': b'KEY-' + b, 'meta': {'selftest': True}}
    def invariants(st):
        rows, tail = st.read_catalog(); ids = [r['id'] for r in rows]
        files = [n for d in st.dirs for n in _o882.listdir(d) if n.endswith('.pt')]
        return (not tail and len(ids) == len(set(ids)) and all(RealStore882.sha_file(r['file']) == r['sha256'] for r in rows)
                and sorted(n[:-3] for n in files) == sorted(ids) and all(_o882.path.exists(r['address_file']) for r in rows)
                and not [n for d in st.dirs for n in _o882.listdir(d) if n.endswith('.tmp')])
    after = ('ENTRY_SIDECAR', 'DIR_FSYNC', 'VERIFIED_RELOAD', 'CATALOG_APPEND', 'CATALOG_FSYNC', 'CATALOG_DIR_FSYNC')
    try:
        for stage in STAGES882[:-1]:
            d = _o882.path.join(root, stage); st = RealStore882(d, [_o882.path.join(d, 'data')]); data = st.dirs[0]
            st.commit('base', data, writer(b'base', 'base'), verify, addr(b'base'))
            crash = stage if stage in ('TMP_WRITTEN', 'FILE_RENAMED') else None
            def fn(s, stage=stage):
                if s == stage: raise RuntimeError('INJECTED ' + s)
            fault = None if crash else {'fn': fn, 'partial': stage == 'CATALOG_APPEND'}
            outcome = 'NO_EXCEPTION'
            try: st.commit('x', data, writer(b'payload-x', 'x', crash), verify, addr(b'x'), parent=('base', _h882.sha256(b'base').hexdigest()), fault=fault)
            except CommitUncertain881: outcome = 'UNCERTAIN'
            rep = st.recover(verify); rows, _ = st.read_catalog(); ids = [r['id'] for r in rows]
            gens = [r['generation'] for r in rows]
            ok = (outcome == 'UNCERTAIN' and invariants(st) and ('x' in ids) == (stage in after) and ids.count('x') <= 1 and
                  'base' in ids and gens == sorted(gens) and len(set(gens)) == len(gens))
            if 'x' in ids: ok = ok and [r for r in rows if r['id'] == 'x'][0]['parent_id'] == 'base'
            res['crash_' + stage] = {'pass': ok, 'catalogued_after_recovery': 'x' in ids,
                                     'recovery': {k: (len(v) if isinstance(v, list) else v) for k, v in rep.items()}}
        d = _o882.path.join(root, 'idem'); st = RealStore882(d, [_o882.path.join(d, 'data')]); data = st.dirs[0]
        a = st.commit('e', data, writer(b'one', 'e'), verify, addr(b'one'))
        b = st.commit('e', data, writer(b'one', 'e'), verify, addr(b'one'),
                      existing=(_h882.sha256(b'one').hexdigest(), _h882.sha256(b'KEY-one').hexdigest()))
        def block(fn):
            try: fn(); return False
            except IntegrityBlock881: return True
        c = block(lambda: st.commit('e', data, writer(b'two', 'e'), verify, addr(b'two'),
                                    existing=(_h882.sha256(b'two').hexdigest(), _h882.sha256(b'KEY-two').hexdigest())))
        c2 = block(lambda: st.commit('e', data, writer(b'one', 'e'), verify, addr(b'other'),
                                     existing=(_h882.sha256(b'one').hexdigest(), _h882.sha256(b'KEY-other').hexdigest())))
        rows, _ = st.read_catalog()
        res['idempotency'] = {'pass': a['state'] == 'COMMITTED' and b['state'] == 'IDEMPOTENT_NO_OP' and c and c2 and len(rows) == 1}
        res['parent_not_committed_blocks'] = {'pass': block(lambda: st.commit('k', data, writer(b'k', 'k'), verify, addr(b'k'),
                                                                               parent=('nope', 'x')))}
        st.commit('f', data, writer(b'three', 'f'), verify, addr(b'three')); rows, _ = st.read_catalog()
        res['generation_monotonic'] = {'pass': [r['generation'] for r in rows] == [1, 2]}
        q1 = _o882.path.join(data, 'z.pt'); open(q1, 'wb').write(b'a'); st.recover(verify)
        open(q1, 'wb').write(b'b'); st.recover(verify); names = sorted(_o882.listdir(st.qdir))
        res['quarantine_no_overwrite'] = {'pass': len([n for n in names if n.startswith('z.pt.q')]) == 2 and
                                          open(_o882.path.join(st.qdir, 'z.pt.q000'), 'rb').read() == b'a'}
        open(_o882.path.join(data, 'y.addr.json'), 'w').write('{}'); st.recover(verify)
        res['orphan_address_sidecar_quarantined'] = {'pass': not _o882.path.exists(_o882.path.join(data, 'y.addr.json'))}
        af = [r for r in st.read_catalog()[0] if r['id'] == 'f'][0]['address_file']; good = open(af).read()
        dd = _j882.loads(good); dd['b64'] = _b64882.b64encode(b'TAMPERED').decode('ascii'); open(af, 'w').write(_j882.dumps(dd))
        res['address_tamper_blocks'] = {'pass': block(lambda: st.recover(verify))}
        dd = _j882.loads(good); dd['b64'] = _b64882.b64encode(b'FORGED').decode('ascii')
        dd['address_sha256'] = _h882.sha256(b'FORGED').hexdigest(); open(af, 'w').write(_j882.dumps(dd))   # self-consistent forgery
        res['forged_address_vs_catalog_blocks'] = {'pass': block(lambda: st.recover(verify))}
        open(af, 'w').write(good)
        d2 = _o882.path.join(root, 'orphan_forged'); s2 = RealStore882(d2, [_o882.path.join(d2, 'data')]); dat2 = s2.dirs[0]
        def fv(s):
            if s == 'VERIFIED_RELOAD': raise RuntimeError('INJECTED')
        try: s2.commit('o', dat2, writer(b'o', 'o'), verify, addr(b'o'), fault={'fn': fv, 'partial': False})
        except CommitUncertain881: s2_uncertain = True
        oaf = _o882.path.join(dat2, 'o.addr.json'); od = _j882.loads(open(oaf).read())
        od['b64'] = _b64882.b64encode(b'OTHER').decode('ascii'); od['address_sha256'] = _h882.sha256(b'OTHER').hexdigest()
        open(oaf, 'w').write(_j882.dumps(od)); rep2 = s2.recover(verify)
        res['orphan_with_foreign_address_quarantined'] = {'pass': not rep2['recatalogued'] and not s2.read_catalog()[0] and
                                                          not _o882.path.exists(_o882.path.join(dat2, 'o.pt'))}
        _o882.replace(_o882.path.join(data, 'f.pt'), _o882.path.join(root, 'moved_away.pt'))
        res['dangling_pointer_blocks'] = {'pass': block(lambda: st.recover(verify))}
        d = _o882.path.join(root, 'corrupt'); st = RealStore882(d, [_o882.path.join(d, 'data')])
        open(st.catalog, 'wb').write(b'{"id": "a"}\nnot-json\n{"id": "b"}\n')
        res['corrupt_middle_line_blocks'] = {'pass': block(lambda: st.read_catalog())}
        d = _o882.path.join(root, 'dangling_parent'); st = RealStore882(d, [_o882.path.join(d, 'data')]); data = st.dirs[0]
        st.commit('p', data, writer(b'p', 'p'), verify, addr(b'p'))
        st.commit('c', data, writer(b'c', 'c'), verify, addr(b'c'), parent=('p', _h882.sha256(b'p').hexdigest()))
        rows = st.read_catalog()[0]; open(st.catalog, 'wb').write((_j882.dumps(rows[1], sort_keys=True) + '\n').encode())
        res['dangling_parent_in_catalog_blocks'] = {'pass': block(lambda: st.recover(verify))}
    finally:
        _s882.rmtree(root, ignore_errors=True)
    return {k: v['pass'] for k, v in res.items()}, res


def st_j882():
    led = {'retries_used': 0}; seq = [next_attempt882(led, 'NO_MATCH'), next_attempt882(led, 'NO_MATCH'), next_attempt882(led, 'MODEL_REJECT')]
    led2 = {'retries_used': 0}; seq2 = [next_attempt882(led2, 'MODEL_REJECT'), next_attempt882(led2, 'TIE_NO_MOUNT')]
    outs = {next_attempt882({'retries_used': 0}, o) for o in ('NO_MATCH', 'TIE_NO_MOUNT', 'AMBIGUOUS_NO_MOUNT', 'MODEL_REJECT',
                                                            'INVALID_QUERY', 'NO_CANDIDATE', 'INVALID_SCORE', 'ACCEPT_KEEP')}
    return {'first_no_match_gets_one_new_query': seq[0] == 'NEW_QUERY', 'second_retry_refused': seq[1:] == ['STOP', 'STOP'],
            'reject_then_tie_stops': seq2 == ['NEW_QUERY', 'STOP'], 'ledger_bounded': led['retries_used'] == 1 == led2['retries_used'],
            'no_lower_rank_branch_exists': outs <= {'NEW_QUERY', 'STOP', 'USE'},
            'empty_bank_never_retried': next_attempt882({'retries_used': 0}, 'NO_CANDIDATE') == 'STOP'}


def st_k882():
    saved = dict(STATE882['budget'])
    try:
        STATE882['budget'] = {'adapter_ffe_lower_bound': 0.0, 'ffe_by_kind': {}}
        a = ffe882(352, 80, 'append'); g = ffe882(300 + 8, 80, 'gen'); x = ffe882(50, 4, 'lower')
        tot = STATE882['budget']['adapter_ffe_lower_bound']
        return {'full_80_layer_append': abs(a - 352 / 256.0) < 1e-12, 'multi_token_generation': abs(g - 308 / 256.0) < 1e-12,
                'lower_layers_counted_by_layer': abs(x - 50 * 4 / 80.0 / 256.0) < 1e-12, 'total_is_sum': abs(tot - (a + g + x)) < 1e-12,
                'per_kind_recorded': sorted(STATE882['budget']['ffe_by_kind']) == ['append', 'gen', 'lower']}
    finally:
        STATE882['budget'] = saved


def st_l882():
    sk = d1_skeleton882(); p = {'parent': 'X', 'action': 'ADVANCE', 'address_sha256': 'k'}
    return {'executor_observation_offline_separate': len({'environment_effect', 'model_observation', 'offline'} & set(sk)) == 3,
            'store_record_separate': set(sk['store']) == {'decision', 'written', 'why'},
            'supported_from_executor_state_only': supported882('POINTER_ADVANCED', None, 'middle') and
            not supported882('POINTER_ADVANCED', None, None) and not supported882('NO_EFFECT', 'second', 'middle'),
            'unknown_observation_never_supported': not supported882(None, None, 'UNKNOWN'),
            'provenance_seal_sensitive': eid882(p) != eid882(dict(p, action='ACQUIRE')) and eid882(p) == eid882(dict(p)),
            'provenance_seal_covers_address_key': eid882(p) != eid882(dict(p, address_sha256='k2'))}


def st_m882():
    saved = dict(FROZEN882); res = {}
    try:
        FROZEN882.clear(); e = lambda *v: _np882.array([v], dtype=_np882.float32)
        v = make_view882([entry_py882('a', e(1.0, 0.0))])
        try: route882(e(1.0, 0.0), v, e(0.0, 1.0), {'scope': 'LIVE'}, score_py882); res['route_before_freeze_refused'] = False
        except Gate882: res['route_before_freeze_refused'] = True
        th = freeze_thresholds882({'tau_neg': 0.1, 'delta_tie': 0.01}, 'LIVE', {'kind': 'selftest'})
        res['route_after_freeze_runs'] = route882(e(1.0, 0.0), v, e(0.0, 1.0), th, score_py882)['decision'] == 'ACCEPT'
        try: freeze_thresholds882({'tau_neg': 0.0, 'delta_tie': 0.0}, 'LIVE', {}); res['second_freeze_refused'] = False
        except Gate882: res['second_freeze_refused'] = True
        th2 = _j882.loads(_j882.dumps(th)); th2['values']['tau_neg'] = -1.0
        try: route882(e(1.0, 0.0), v, e(0.0, 1.0), th2, score_py882); res['mutated_copy_refused'] = False
        except Gate882: res['mutated_copy_refused'] = True
        th['values']['tau_neg'] = -1.0
        try: route882(e(1.0, 0.0), v, e(0.0, 1.0), th, score_py882); res['in_place_mutation_refused'] = False
        except Gate882: res['in_place_mutation_refused'] = True
    finally:
        FROZEN882.clear(); FROZEN882.update(saved)
    return res


def st_n882():
    rng = _np882.random.default_rng(1882); keys = {c: rng.standard_normal((3, 8)).astype(_np882.float32) for c in 'abcde'}
    for c in keys: keys[c] /= _np882.linalg.norm(keys[c], axis=1, keepdims=True)
    Q = keys['c'] + 0.05 * rng.standard_normal((3, 8)).astype(_np882.float32); null = _np882.zeros((1, 8), dtype=_np882.float32)
    view = make_view882([entry_py882(c, keys[c]) for c in sorted(keys)]); th = frozen_py882(0.0, 1e-3)
    r0 = rsel882(Q, view, null, th, score_py882); r_ord = rsel882(Q, order_shuffle882(view), null, th, score_py882)
    sv, ren = id_shuffle882(view, SHUFFLE_SALT882); r_id = rsel882(Q, sv, null, th, score_py882)
    ks = rsel882(Q, key_shuffle882(view), null, th, score_py882)
    other = rsel882(keys['a'], view, null, th, score_py882)
    return {'order_shuffle_invariant': same_route882(r0, r_ord), 'id_shuffle_invariant': same_route882(r0, r_id, ren),
            'key_shuffle_bites': bite882(r0, ks)['bite'], 'query_shuffle_bites': bite882(r0, other)['bite'],
            'ids_carry_no_content': all(c.startswith('R882_') and len(c) == 21 for c in sv),
            'baseline_accepts_its_own_key': r0['decision'] == 'ACCEPT' and r0['chosen'] == 'c'}


def run_selftests882():
    tests = {'a_preC_key_input': st_a882, 'b_prompt_domain_memnull': st_b882, 'c_router_null_tie_empty_margin': st_c882,
             'd_calibration_labels_cannot_reach_runtime': st_d882, 'e_whitelist_and_firewall': st_e882, 'f_parent_dag': st_f882,
             'g_rope_rephase_roundtrip': st_g882, 'i_crash_safe_store_with_address_sidecar': st_i882,
             'j_retry_limit_no_top2': st_j882, 'k_ffe_accounting': st_k882, 'l_provenance_and_separation': st_l882,
             'm_threshold_freeze': st_m882, 'n_order_and_id_shuffle': st_n882}
    out, bad = {}, []
    for name, fn in tests.items():
        try:
            r = fn()
            if isinstance(r, tuple): r, detail = r; STATE882['selftests'][name + '_detail'] = detail
            out[name] = r
            if not all(v is True for k, v in r.items() if not k.startswith(('roundtrip_rel', 'wrong_position_rel'))): bad.append(name)
        except BaseException as exc:
            out[name] = {'error': '%s: %s' % (type(exc).__name__, exc)}; bad.append(name)
    if 'selftest_mask881' in globals():                   # (h) the locked TEST881 mask principle test (torch SDPA on CPU)
        try:
            out['h_mask_restore_c_blind_scope'] = {k: v for k, v in selftest_mask881().items() if k != 'scope'}
            STATE882['selftests'].pop('mask', None)
        except BaseException as exc:
            out['h_mask_restore_c_blind_scope'] = {'error': '%s: %s' % (type(exc).__name__, exc)}; bad.append('h_mask')
    else:
        out['h_mask_restore_c_blind_scope'] = {'error': 'selftest_mask881 not selected'}; bad.append('h_mask')
    STATE882['selftests'].update(out)
    if bad: raise Gate882('G0_CPU_SELFTEST_FAIL %s' % bad)
    return out

# ============================ budget, timing, records ============================
def guard882(stage, need_gib=0.0):
    peak_update881(); el = (time.perf_counter() - T_START882) / 60.0; free = free_gib881(); b = STATE882['budget']
    b['stages'][stage] = {'wall_min': round(el, 2), 'free_gib': round(free, 2), 'peak_alloc_gib': round(b['peak_alloc_gib'], 3),
                          'adapter_ffe_lower_bound': round(b['adapter_ffe_lower_bound'], 2), 'calls849': int(env882['CALLS849'])
                          if 'env882' in globals() else None, 'ssd_bytes': b['ssd_bytes']}
    why = [x for x, bad in (('WALL %.1f>%.0f min' % (el, WALL_MIN882), el > WALL_MIN882),
                            ('VRAM_FREE %.2f<%.1f GiB' % (free, FREE_MIN_GIB882 + need_gib), free < FREE_MIN_GIB882 + need_gib),
                            ('PEAK %.2f>%.0f GiB' % (b['peak_alloc_gib'], PEAK_GIB882), b['peak_alloc_gib'] > PEAK_GIB882),
                            ('ADAPTER_FFE %.1f>%.0f' % (b['adapter_ffe_lower_bound'], FFE_MAX882),
                             b['adapter_ffe_lower_bound'] > FFE_MAX882)) if bad]
    if why: raise Budget882('%s: %s' % (stage, '; '.join(why)))


def arm_record882(cell, cond, arm, reading, spans):
    rec = {'cell': cell, 'source': cond, 'arm': arm, 'action': reading['action'], 'argmax_word': reading.get('argmax_word'),
           'abstain': reading.get('abstain'), 'mass': reading.get('mass'), 'normalized': reading.get('normalized'), 'mask_spans': spans,
           'scores': [{'word': s['word'], 'ids': list(s['ids']), 'token_logps': s['token_logps'],
                       'sequence_logp': s['sequence_logp']} for s in reading['scores']]}
    ARMS881.setdefault(cell, {})['%s_%s' % (arm, cond)] = rec
    with open(ROOT864 / '882_arms.jsonl', 'a', encoding='utf-8') as f:
        f.write(_j882.dumps(rec, sort_keys=True, default=str) + '\n')
    return rec


guard881, ffe881, line881, arm_record881 = guard882, ffe882, line882, arm_record882   # I/O + budget helpers of the selected 881 code


def decision_log882(rec):
    with open(ROOT864 / '882_decisions.jsonl', 'a', encoding='utf-8') as f:
        f.write(_j882.dumps(jsafe878(rec), sort_keys=True) + '\n')


def reading_view882(r):
    return {k: r.get(k) for k in ('action', 'argmax_word', 'abstain', 'mass', 'normalized')}


# ============================ runtime: model-owned address (write key == live query procedure) ============================
def score882(Q, K):
    return float(PEAK882[0](Q, K))


def seg_tokens882(pre, segments, post):
    return len(pre) + sum(len(s) + (0 if r is None else int(r.shape[0])) for s, r in segments) + len(post or [])


def preC882(env, zcap, retry=False):
    segs, zsha = address_input882(zcap)
    q = env['QTEXT841'][zcap['qid']]
    pre, post, psha = addr_prompt_ids882(env['prompt_ids'], TOKIDS882[0], q, retry)
    out = env['gen851'](env['MEMNULL841'], pre, segs, post); check_output_h863(out, 'T882_ADDRESS')
    ffe882(seg_tokens882(pre, segs, post) + len(out.get('toks') or []), 80, 'address_generation')
    R = out['rows']
    rec = {'z_sha256': zsha, 'prompt_sha256': psha, 'retry_prompt': bool(retry), 'text': out['text'],
           'qid_sha256': sha256_bytes864(zcap['qid'].encode()),
           'template_sha256': _h882.sha256(((ADDR_RETRY_PROMPT882 if retry else ADDR_PROMPT882) + '\x00' + ADDR_SUFFIX882).encode()).hexdigest(),
           'rows': int(R.shape[0]) if (R is not None and R.ndim == 2) else 0, 'memory': 'MEMNULL841'}
    if not (rows_ok880(R) and bool(torch.isfinite(R).all())):
        rec['status'] = 'INVALID_ADDRESS_ROWS'
        return None, rec
    raw, info = query880(env, R)
    ffe882(len(env['IDXPRE841']) + int(R.shape[0]) + len(env['IDXPOST841']), APPEND873['CUT'] + 1, 'address_h3')
    rec.update({'rows_sha256': info['rows_sha256'], 'raw_sha256': info['query_sha256'], 'status': 'OK'})
    return raw, rec


def center882(env, raw, mu):
    return None if raw is None else env['unit841'](raw.float() - mu).contiguous()


def words882(env, memx, X, words):
    # teacher-forced reading of a closed word set with the rule of the locked readers (argmax word unless the mass of the set
    # is below ABSTAIN_MASS867); one forward of X, every continuation from the same cache, cropped back (CROP path)
    env['budget849'](); model, dev = env['model'], env['DEV']; L, n, Hd = int(X.shape[0]), int(memx[0][0].shape[-2]), int(env['H'])
    assert n + L + max(len(ids) for _, ids in words) <= int(env['MAX_FUSED_TOKENS']), ('CONTEXT_LIMIT', n, L)
    one = lambda m: torch.ones((1, m), device=dev, dtype=torch.long)
    with torch.no_grad():
        cache = env['cache_build'](list(memx)); pos = torch.arange(n, n + L, device=dev)
        out = model(inputs_embeds=X.reshape(1, L, Hd), past_key_values=cache, attention_mask=one(n + L),
                    position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
        first = torch.log_softmax(out.logits[0, -1].float(), dim=-1); del out
        scores = []
        for word, ids in words:
            lps = [float(first[ids[0]])]
            if len(ids) > 1:
                m = len(ids) - 1; E = env['embed841'](ids[:-1]); p2 = torch.arange(n + L, n + L + m, device=dev)
                out = model(inputs_embeds=E.reshape(1, m, Hd), past_key_values=cache, attention_mask=one(n + L + m),
                            position_ids=p2.unsqueeze(0), cache_position=p2, use_cache=True, return_dict=True)
                lp = torch.log_softmax(out.logits[0].float(), dim=-1); lps += [float(lp[i, ids[i + 1]]) for i in range(m)]
                del out, lp, E; cache.crop(-m)
                assert int(cache.get_seq_length()) == n + L, 'WORDS_CROP_LENGTH'
            scores.append({'word': word, 'ids': list(ids), 'token_logps': lps, 'sequence_logp': float(sum(lps))})
        del cache, first
    ffe882(L + sum(len(ids) - 1 for _, ids in words), 80, 'word_reading')
    mass = sum(_m882.exp(s['sequence_logp']) for s in scores); best = max(scores, key=lambda s: s['sequence_logp'])
    low = mass < ABSTAIN_MASS867
    return {'decision': 'ABSTAIN' if low else best['word'], 'why': 'LOW_MASS' if low else 'ARGMAX', 'mass': mass, 'scores': scores,
            'argmax_word': best['word'], 'normalized': {s['word']: _m882.exp(s['sequence_logp']) / mass for s in scores} if mass > 0 else {},
            'path': 'CROP_TEACHER_FORCED', 'memory_tokens': n, 'X_tokens': L}


def need882(env, memx, zcap):
    segs, zsha = address_input882(zcap); q = env['QTEXT841'][zcap['qid']]
    pre = list(env['prompt_ids'](NEED_PROMPT882.format(q=q))); X, _ = env['make_x851'](pre, segs, NEED_SUFFIX_IDS882)
    r = words882(env, memx, X, NEED_IDS882)
    r.update({'z_sha256': zsha, 'X_sha256': tsha881(X), 'reading': 'NEED_MEMORY (not the action CAR)', 'candidates_shown': 0,
              'prompt_sha256': _h882.sha256(_j882.dumps([pre, NEED_SUFFIX_IDS882]).encode()).hexdigest()})
    del X
    return r


def validate882(env, grown, zcap):
    segs, zsha = address_input882(zcap); q = env['QTEXT841'][zcap['qid']]
    pre = list(env['prompt_ids'](VALID_PROMPT882.format(q=q))); X, _ = env['make_x851'](pre, segs, VALID_SUFFIX_IDS882)
    r = words882(env, grown, X, VALID_IDS882)
    r.update({'z_sha256': zsha, 'X_sha256': tsha881(X), 'reading': 'POST_MOUNT_READOUT_VALIDATION (model only)',
              'veto': r['decision'] == 'REJECT_MEMORY'})
    del X
    return r


def bank_view882(store, salt):
    # SSD -> CPU: only the pre-C key sidecars and the whitelisted catalog fields are read; opaque ids hide catalog names
    rows = store.rows(); op = {r['id']: 'M882_' + _h882.sha256(('%s|%s|%s' % (salt, r['id'], r['sha256'])).encode()).hexdigest()[:16]
                               for r in rows}
    entries, omap = [], {}
    for r in rows:
        blob, d = store.read_address(r['address_file'])
        if d['meta'].get('domain') != ADDRESS_DOMAIN882.get('id'): raise Gate882('ADDRESS_DOMAIN_MISMATCH ' + op[r['id']])
        STATE882['budget']['ssd_bytes'] += len(blob)
        key = torch.from_numpy(key_from_blob882(blob, d['meta']['shape']))
        entries.append({'id': op[r['id']], 'sha256': r['sha256'], 'tensor_sha': r['entry'].get('tensor_sha'), 'address_key': key,
                        'address_sha256': r['address_sha256'], 'parent_id': op.get(r['parent_id']) if r['parent_id'] else None,
                        'parent_sha256': r['parent_sha256'], 'body_tokens': int(r['entry']['body_tokens']),
                        'requires_parent': bool(r['requires_parent']), 'generation': int(r['generation'])})
        omap[op[r['id']]] = r
    return make_view882(entries), omap, rows


# ============================ runtime: parent-aware physical mount ============================
def mount882(env, base_mem, rows, tag):
    cut, P, CH, dev, NL = APPEND873['CUT'], int(env['P']), EXP878['CHUNK'], env['DEV'], int(env['NL'])
    rephase = APPEND873['rephase']; seal_B = full_seal881(base_mem)['all']; mem = base_mem; recs = []
    for j, row in enumerate(rows):
        guard882('mount_%s_%d' % (tag, j), HEADROOM_GIB882)
        cp = load_exp878(env, row['entry']); q = int(cp['body_tokens']); n0 = length873(env, mem)
        STATE882['budget']['ssd_bytes'] += int(row['entry']['bytes'])
        g = append_exp878(env, mem, cp); ffe882(q, 80, 'mount_append')
        r = {'catalog_id': row['id'], 'file_sha256': row['sha256'], 'tensor_sha': row['entry']['tensor_sha'], 'positions': [n0, n0 + q],
             'body_tokens': q, 'generation': row['generation'], 'memory_before_full_seal': full_seal881(mem)['all']}
        r['n_exact'] = length873(env, g) == n0 + q
        r['all_80_layers'] = len(g) == NL
        r['finite'] = all(bool(torch.isfinite(t[:, :, n0:]).all()) for kv in g for t in kv)
        r['prefix_rows_bitwise'] = all(torch.equal(a[t][:, :, :n0], b[t]) for a, b in zip(g, mem) for t in (0, 1))
        r['no_alias'] = not any(a[0] is b[0] or a[1] is b[1] for a, b in zip(g, mem))
        r['lower_V_bitwise'] = all(torch.equal(g[i][1][:, :, n0:], cp['lower'][i][1][:, :, P:P + q]) for i in range(cut + 1))
        rt = 0.0
        for i in range(cut + 1):
            k = g[i][0][:, :, n0:n0 + q]; back = []
            for st in range(0, q, CH):
                e = min(q, st + CH)
                back.append(rephase(k[:, :, st:e], torch.arange(n0 + st, n0 + e, device=dev), torch.arange(P + st, P + e, device=dev)))
            back = torch.cat(back, dim=-2); ref = cp['lower'][i][0][:, :, P:P + q]
            rt = max(rt, float(torch.linalg.vector_norm(back.float() - ref.float())) / max(float(torch.linalg.vector_norm(ref.float())), 1e-30))
            del back
        r['rope_roundtrip_rel'] = rt; r['rope_ok'] = rt <= ROPE_TOL878
        gx = xappend878(env, mem, cp, ()); ffe882(q, 80, 'mount_explicit_parity')
        r['explicit_equals_native_append_bitwise'] = all(torch.equal(a[t], b[t]) for a, b in zip(g, gx) for t in (0, 1))
        del gx, cp
        r['pass'] = all(r[k] for k in ('n_exact', 'all_80_layers', 'finite', 'prefix_rows_bitwise', 'no_alias', 'lower_V_bitwise',
                                       'rope_ok', 'explicit_equals_native_append_bitwise'))
        recs.append(r)
        prev, mem = mem, g
        if prev is not base_mem: del prev                # an intermediate [B][parent] is released once the child is built on it
        if not r['pass']: break
    b_ok = full_seal881(base_mem)['all'] == seal_B
    ok = len(recs) == len(rows) and all(x['pass'] for x in recs) and b_ok
    rec = {'chain': [x['catalog_id'] for x in recs], 'elements': recs, 'B_full_seal_unchanged': b_ok, 'pass': ok,
           'n_exact': all(x['n_exact'] for x in recs), 'all_80_layers': all(x['all_80_layers'] for x in recs),
           'prefix_seal': all(x['prefix_rows_bitwise'] for x in recs) and b_ok,
           'rope_roundtrip': max([x['rope_roundtrip_rel'] for x in recs] or [None])}
    if not ok:
        del mem; gc.collect(); torch.cuda.empty_cache()
        return None, rec
    return mem, rec


def layout_at882(env, n0, entry, L):
    q = int(entry['body_tokens']); sp = entry['provenance']['spans_body']
    lay = {'n0': n0, 'q': q, 'L': L, 'E': [n0, n0 + q], 'X2': [n0 + sp['X2'][0], n0 + sp['X2'][1]],
           'A': [n0 + sp['A'][0], n0 + sp['A'][1]], 'C': [n0 + sp['C'][0], n0 + sp['C'][1]], 'X': [n0 + q, n0 + q + L]}
    lay['N'] = n0 + q + L
    assert lay['X2'][0] == n0 and lay['X2'][1] == lay['A'][0] and lay['A'][1] == lay['C'][0] and lay['C'][1] == n0 + q, ('LAYOUT', lay)
    assert lay['N'] + max(len(ids) for _, ids in ACTION_IDS867) <= int(env['MAX_FUSED_TOKENS']), ('MAX_FUSED_TOKENS', lay['N'])
    lay['sha256'] = sha256_bytes864(_j882.dumps(lay, sort_keys=True).encode())
    return lay


def readout_single882(env, key, X, Ly, g, seal_mem, seal_ref):
    # TEST881 readout without a matched partner: C_BLIND (only the C span hidden) against a C-zeroed copy, bitwise on the X
    # rows and every teacher-forced continuation over all 80 layers; trace == locked xcar878; then the VIS reading
    C = Ly['C']; guard882('readout_' + key, HEADROOM_GIB882 + kv_gib881(g))
    Gs = STATE882['cells'][key] = {'relation': 'SINGLE_NO_MATCHED_PARTNER', 'layout': Ly, 'gate2': {},
                                   'g_full_seal': {'L': full_seal881(g)['all']}}
    ck = Gs['gate2']
    rd, tr = timed881(key + '_CBLIND_TRACE_L', xtrace881, env, g, X, [C]); arm_record882(key, 'L', 'C_BLIND', rd, [C])
    gz = zero_slot881(env, g, C[0], C[1])
    rz, tz = timed881(key + '_CBLIND_TRACE_ZEROC', xtrace881, env, gz, X, [C]); del gz
    arm_record882(key, 'ZEROC', 'C_BLIND', rz, [C])
    ck['C_BLIND_reading_invariant_to_C_content'] = same_reading881(rd, rz)
    ck['C_BLIND_X_KV_80_layers_bitwise'] = tr['X']['kv'] == tz['X']['kv']
    ck['C_BLIND_X_final_hidden_bitwise'] = tr['X']['hidden'] == tz['X']['hidden']
    ck['C_BLIND_continuations_KV_hidden_logp_bitwise'] = tr['continuations'] == tz['continuations']
    ck['C_BLIND_masks_and_positions_equal'] = tr['X']['mask_sha256'] == tz['X']['mask_sha256'] and \
        tr['X']['positions'] == tz['X']['positions'] == Ly['X']
    TRACES881[key] = {'L': tr, 'ZEROC': tz}
    lk = xread881(env, g, X, [C], False, key + '_CBLIND_LOCKED'); ck['trace_adapter_equals_locked_xcar878'] = same_reading881(rd, lk)
    nb, _ = nread881(env, g, X, [C], True, key + '_NCBLIND_L'); arm_record882(key, 'L', 'NATIVE_C_BLIND', nb, [C])
    ck['receiver_B_full_80_layer_seal_unchanged'] = full_seal881(seal_mem)['all'] == seal_ref
    ck['finite'] = all(_m882.isfinite(x) for a in ARMS881[key].values() for s_ in a['scores'] for x in s_['token_logps'])
    Gs['gate2_pass'] = all(ck.values())
    line882('G5', key, Gs['relation'], 'pass=%s' % Gs['gate2_pass'], _j882.dumps(ck, sort_keys=True))
    if not Gs['gate2_pass']: raise Gate882('G5_READOUT_FAIL %s %s' % (key, sorted(k for k, v in ck.items() if not v)))
    arm_record882(key, 'L', 'VIS', xread881(env, g, X, [C], True, key + '_VIS_L'), [C])
    Gs['g_full_seal_after_reads'] = {'L': full_seal881(g)['all']}
    if Gs['g_full_seal_after_reads'] != Gs['g_full_seal']: raise Gate882('GROWN_CACHE_MUTATED ' + key)
    return Gs


def readout882(env, cell, r, row, g):
    # D1 cell with a same-X2 partner: the locked cell881 (full TEST881 contract, it rebuilds both grown caches itself);
    # otherwise the single readout on the mounted cache
    global EXEC_CELL881
    T = TGT878[('FORK', r)]; side = BANKSIDE882.get(row['id']); partner = side.replace('_LIVE', '_MISSING') if side else None
    if r == D1_RECEIVER882 and side in SRC878 and partner in SRC878:
        s = side.split('_')[1]; key = '%s>%s' % (s, r); EXEC_CELL881 = (s, r)
        cell881(env, s, r)
        Gs = STATE882['cells'][key]
        Gs['resolver_mount_equals_readout_mount'] = Gs['g_full_seal']['L'] == full_seal881(g)['all']
        if not Gs['resolver_mount_equals_readout_mount']: raise Gate882('RESOLVER_MOUNT_NE_READOUT_MOUNT ' + key)
        G881[key].pop('M', None); gc.collect(); torch.cuda.empty_cache()
        out = {'key': key, 'path': 'CELL881_MATCHED', 'g': G881[key]['L'], 'C': Gs['layout']['C'], 'gate2': Gs['gate2'], 'pass': Gs['gate2_pass']}
    else:
        key = '%s_R%s_%s' % (cell, r, row['id'][-8:])
        Ly = layout_at882(env, length873(env, T['m']), row['entry'], int(T['X'].shape[0]))
        Gs = readout_single882(env, key, T['X'], Ly, g, T['m'], STATE882['receivers'][r]['B_full_seal'])
        out = {'key': key, 'path': 'SINGLE', 'g': g, 'C': Ly['C'], 'gate2': Gs['gate2'], 'pass': Gs['gate2_pass']}
    A = ARMS881[key]; out['VIS'] = reading_view882(A['VIS_L']); out['C_BLIND'] = reading_view882(A['C_BLIND_L'])
    out['vis_argmax_differs_from_c_blind'] = A['VIS_L']['argmax_word'] != A['C_BLIND_L']['argmax_word']
    out['vis_action_differs_from_c_blind'] = A['VIS_L']['action'] != A['C_BLIND_L']['action']
    return out


# ============================ runtime: one live cell (need -> query -> route -> mount -> validation; bounded retry) ============================
def live_cell882(env, cell, r):
    T = TGT878[('FORK', r)]; zc = ZCAP882[T['item']]; R = STATE882['receivers'][r]
    out = STATE882['live'][cell] = {'receiver': r, 'item': T['item'], 'attempts': [], 'need': None, 'kept': None}
    base = {'cell': cell, 'prereg_sha256': PREREG_SHA882, 'executed_cell_git_blob': STATE882['source'].get('executed_cell_git_blob'),
            'weights_digest': WEIGHTS0_878, 'B_full_seal': R['B_full_seal'], 'X2_sha256': zc['z_sha256'], 'X_sha256': R['X_sha256'],
            'offline': 'SEALED_UNTIL_ALL_LIVE_WORK_ENDS'}
    guard882('need_' + cell, HEADROOM_GIB882)
    need = need882(env, T['m'], zc); out['need'] = need
    nrec = {'decision': need['decision'], 'why': need['why'], 'mass': need['mass'], 'normalized': need['normalized'],
            'scores': [{k: s[k] for k in ('word', 'ids', 'token_logps', 'sequence_logp')} for s in need['scores']],
            'X_sha256': need['X_sha256'], 'prompt_sha256': need['prompt_sha256']}
    addr = ADDR882['live'][r]; ledger = {'retries_used': 0}; rejected = []; retry = 0
    while True:
        view, omap, rows = bank_view882(STORE_BANK882, ID_SALT882)
        rt = route882(addr['key'], view, NULL_KEY882[0], FROZEN882['TH'], score882, exclude=tuple(rejected))
        att = dict(base, retry=retry, need=nrec, route=rt, mount=None, validation=None, readout=None,
                   query=dict(addr['rec'], key_sha256=addr.get('key_sha256'), domain=ADDRESS_DOMAIN882['id']),
                   execution={'status': 'NOT_RUN', 'action': None, 'effect': None},
                   store={'decision': None, 'written': None, 'why': 'NOT_REACHED'})
        out['attempts'].append(att)
        if need['decision'] != 'USE_MEMORY':
            att['use'] = 'DIAGNOSTIC_ROUTE_ONLY'; att['outcome'] = 'NO_MOUNT_NEED_' + need['decision']; decision_log882(att)
            break
        if rt['decision'] != 'ACCEPT':
            att['outcome'] = 'NO_MOUNT_' + rt['decision']; decision_log882(att)
            nxt = next_attempt882(ledger, rt['decision'])
        else:
            row = omap[rt['chosen']]; res = resolve_parent882(row['id'], rows, mounted=())
            by = {x['id']: x for x in rows}; chain = [by[i] for i in res['append']]
            g, mrec = mount882(env, T['m'], chain, cell)
            att['mount'] = dict(mrec, resolver=res)
            if g is None:
                att['outcome'] = 'MOUNT_GATES_FAILED'; decision_log882(att)
                raise Gate882('MOUNT_GATES_FAIL %s %s' % (cell, _j882.dumps(mrec, default=str)[:600]))
            S = SRC878.get(BANKSIDE882.get(row['id'])) or SRC882.get(BANKSIDE882.get(row['id']))
            if S is not None and row['id'] not in STATE882['physical'].setdefault('recon', {}):
                guard882('recon_' + cell, HEADROOM_GIB882)
                rc = persist878(env, S); ffe882(3 * int(S['entry']['body_tokens']) + int(S['X3'].shape[0]) + cont_tokens881(), 80, 'recon')
                STATE882['physical']['recon'][row['id']] = {k: v for k, v in rc.items() if k != 'arm'}
                if not rc['pass']: raise Gate882('SOURCE_TIMELINE_RECON_FAIL ' + row['id'])
            att['mount']['source_timeline_recon'] = STATE882['physical'].get('recon', {}).get(row['id'], 'NOT_APPLICABLE_NEW_CARTRIDGE')
            val = validate882(env, g, zc); att['validation'] = {k: val[k] for k in ('decision', 'why', 'mass', 'normalized', 'veto')}
            if val['veto']:
                del g; gc.collect(); torch.cuda.empty_cache()
                att['restore'] = {'B_full_seal_unchanged': full_seal881(T['m'])['all'] == R['B_full_seal'], 'grown_cache_released': True}
                if not att['restore']['B_full_seal_unchanged']: raise Gate882('RESTORE_NOT_EXACT ' + cell)
                att['outcome'] = 'MODEL_REJECT_RESTORED'; decision_log882(att); rejected.append(rt['chosen'])
                nxt = next_attempt882(ledger, 'MODEL_REJECT')
            else:
                att['outcome'] = 'MOUNT_KEPT'
                out['kept'] = {'attempt': len(out['attempts']) - 1, 'opaque': rt['chosen'], 'catalog_id': row['id'], 'row': row,
                               'retry': retry, 'after': [a['outcome'] for a in out['attempts'][:-1]]}
                KEEP882[cell] = g
                return out
        if nxt != 'NEW_QUERY': break
        retry += 1; guard882('retry_query_' + cell, HEADROOM_GIB882)
        raw, rec = preC882(env, zc, retry=True); k = center882(env, raw, MU882['mu'])
        addr = {'raw': raw, 'key': k, 'rec': rec, 'key_sha256': None if k is None else _h882.sha256(rows_np882(k).tobytes()).hexdigest()}
        out.setdefault('retry_queries', []).append(dict(rec, key_sha256=addr['key_sha256']))
    return out


# ============================ D1: same VIS policy, literal action, real C, native STORE, parent-aware write with address key ============================
def d1_882(env, cell):
    L = STATE882['live'][cell]; kept = L['kept']; rd = STATE882['readout'][cell]; r = L['receiver']
    T = TGT878[('FORK', r)]; Ex = EXEC882.get(T['item']); row = kept['row']; key = rd['key']; g = KEEP882[cell]; C = rd['C']
    out = STATE882['d1']; out.update(d1_skeleton882()); ck = out['checks'] = {}
    out.update({'cell': cell, 'readout_key': key, 'parent_catalog_id': row['id'], 'claim': 'VIS_SELECTED_ACTION_AFTER_MODEL_OWNED_RECALL'})
    if Ex is None: raise Gate882('D1_RECEIVER_CONTEXT_NOT_CAPTURED')
    guard882('d1', HEADROOM_GIB882)
    cut, dev, Hd = APPEND873['CUT'], env['DEV'], int(env['H']); q = env['QTEXT841'][T['qid']]; X = T['X']
    stored = ARMS881[key]['VIS_L']
    ck['decision_memory_seal_unchanged'] = full_seal881(g)['all'] == STATE882['cells'][key]['g_full_seal']['L']
    ck['readout_gate_passed'] = bool(rd['pass'])
    vis = xread881(env, g, X, [C], True, 'D1_VIS_recompute')
    ck['VIS_recompute_equals_GATE3_VIS'] = same_reading881(vis, stored)
    out['policy'] = {'path': 'VIS_MASKED_XCAR878', 'action': vis['action'], 'argmax_word': vis['argmax_word'], 'abstain': vis['abstain'],
                     'mass': vis['mass'], 'normalized': vis['normalized'], 'sequence_logp': seqlp881(vis)}
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
    X_chk, _ = env['make_x851'](pre, list(Ex['segments']), post); ck['X_rebuilt_equals_receiver_X'] = bool(torch.equal(X_chk, X)); del X_chk
    m2 = [tuple(t.clone() for t in kv) for kv in g]; n2, L2 = length873(env, m2), int(X.shape[0])
    cache = env['cache_build'](list(m2)); ffe882(L2 + cont_tokens881(), 80, 'd1_native_full')
    nat = car873(env, cache, X)
    out['native_full_diagnostic'] = {'action': nat['action'], 'argmax_word': nat['argmax_word'],
                                     'delta_native_minus_VIS': {w: seqlp881(nat)[w] - seqlp881(vis)[w] for w in seqlp881(vis)},
                                     'same_action_as_VIS': nat['action'] == vis['action'], 'role': 'DIAGNOSTIC (never the executed action)'}
    action = vis['action']; out['vis_action'] = action
    out['provenance'] = {'B_full_seal': full_seal881(T['m'])['all'], 'decision_memory_full_seal': full_seal881(g)['all'],
                         'qid_sha256': sha256_bytes864(T['qid'].encode()), 'X_sha256': tsha881(X), 'mounted_before': list(T['mounted']),
                         'path_rows_sha256': [env['stats849'](p['rows'])['sha256'] for p in Ex['path']],
                         'action_token_ids': list(dict(ACTION_IDS867).get(action, [])), 'parent_catalog_id': row['id'],
                         'parent_sha256': row['sha256'], 'retrieval': {'opaque': kept['opaque'], 'retry': kept['retry']}}
    if not all(ck.values()):
        out['status'] = 'TECHNICAL_BLOCK_BEFORE_EXECUTION'; del cache, m2
        raise Gate882('D1_POLICY %s' % sorted(k for k, v in ck.items() if not v))
    if action in ('INVALID', 'ACCEPT', 'STOP'):
        out['status'] = 'TERMINAL_NO_ENV_TRANSITION'; out['store'] = {'decision': None, 'written': None, 'why': 'TERMINAL_ACTION'}
        del cache, m2
        return out
    h, kind = hop865(env, T['m'], T['qid'], len(Ex['path']), Ex['path'][-1]['rows'] if Ex['path'] else None)
    ffe882(len(h.get('toks') or []), 80, 'd1_hop_generation')
    c_rows_sha = env['stats849'](h['rows'].detach().float().cpu())['sha256']
    ck['candidate_text_reproduces_record'] = h['text'] == Ex['candidate_text']
    ck['candidate_rows_sha_reproduces_record'] = c_rows_sha == (Ex['state_sha256'] or {}).get('C')
    out['provenance'].update({'candidate_text': h['text'], 'candidate_rows_sha256': c_rows_sha, 'candidate_memory': 'B'})
    legacy = env['gen851'](g, pre, list(Ex['segments']), post); check_output_h863(legacy, 'T882_CONTROL_ROWS')
    ffe882(seg_tokens882(pre, list(Ex['segments']), post) + len(legacy.get('toks') or []), 80, 'd1_control_rows')
    out['auxiliary'] = {'path': 'NATIVE_FULL_AUXILIARY', 'generated_text': legacy['text']}
    own = env['cache_build'](list(kv873(env, cache))); del cache
    A = dict(ACTION_IDS867)[action]; la = len(A); EA = env['embed841'](A)
    forward873(env, own, EA, n2 + L2); keep = kv873(env, own); del own; ffe882(la, 80, 'd1_action_rows')
    one = lambda n: torch.ones((1, n), device=dev, dtype=torch.long)
    cl = env['cache_build'](list(m2))
    hx = xspan878(env, cl, X.reshape(1, L2, Hd), one(n2 + L2), 0, cut + 1)
    ha = xspan878(env, cl, EA.reshape(1, la, Hd), one(n2 + L2 + la), 0, cut + 1); ffe882(L2 + la, cut + 1, 'd1_lower_explicit')
    ck['X2A_explicit_lower_KV_bitwise'] = all(torch.equal(x, y) for i in range(cut + 1) for x, y in zip(cache_kv870(cl, i), keep[i]))
    nk = [next_kv878(env, hx, n2), next_kv878(env, ha, n2 + L2)]; ref = keep[cut + 1]
    ck['X2A_h3_next_layer_KV_bitwise'] = all(torch.equal(nk[j][t], ref[t][:, :, a:b]) for j, (a, b) in
                                             enumerate(((n2, n2 + L2), (n2 + L2, n2 + L2 + la))) for t in (0, 1))
    del nk, m2
    if not all(ck.values()):
        out['status'] = 'TECHNICAL_BLOCK_BEFORE_EXECUTION'
        raise Gate882('D1_PRE_EXECUTION %s' % sorted(k for k, v in ck.items() if not v))
    ctx = {'spec': dict(Ex['spec']), 'arm': ARM878, 'M': list(T['mounted']), 'memx': g, 'path': [dict(p) for p in Ex['path']],
           'events': [], 'mount_records': [], 'acquisitions': 0, 'rejections': 0, 'addresses': 0, 'steps': Ex['steps']}
    execute866(env, ctx, action, h, legacy, {'segments': list(Ex['segments'])})       # the literal VIS word, locked executor
    eff = ctx['events'][-1]
    out['environment_effect'] = {k: eff.get(k) for k in ('action', 'effect', 'chosen', 'mounted_before', 'mounted_after',
                                                         'path_after', 'direction_text')}
    out['executed'] = out['environment_effect']; out['status'] = 'EXECUTED'
    out['provenance'].update({'mounted_after': list(ctx['M']), 'path_after_rows_sha256': [env['stats849'](p['rows'].detach().float().cpu())['sha256']
                                                                                          for p in ctx['path']]})
    ck['executed_equals_VIS_action'] = eff.get('action') == action
    ck['mount_integrity'] = all(m['n_exact'] and m['all_80_layers'] and m['finite'] for m in ctx['mount_records'])
    post_mem_is_env = ctx['memx'] is not g
    obs_mem = ctx['memx'] if post_mem_is_env else T['m']     # E is decision-time only: environment memory after the action
    out['provenance']['post_action_memory'] = 'MOUNT865_REBUILT' if post_mem_is_env else 'B_UNCHANGED'
    k1 = len(ctx['path']); h1, kind1 = hop865(env, obs_mem, T['qid'], k1, ctx['path'][-1]['rows'] if k1 else None)
    ev1 = env['gen849'](obs_mem, list(env['prompt_ids'](env['EVIDENCE851'].format(q=q))), None, env['ANSWER_SUFFIX851'])
    check_output_h863(ev1, 'T882_EVIDENCE'); ffe882(len(h1.get('toks') or []) + len(ev1.get('toks') or []), 80, 'd1_observation')
    c_new, e_new = h1['rows'].detach().float().cpu(), ev1['rows'].detach().float().cpu()
    out['model_observation'] = {'label': 'MODEL_OBSERVATION', 'hop_text': h1['text'], 'hop_kind': kind1, 'rows': int(c_new.shape[0])}
    out['model_evidence'] = {'label': 'MODEL_EVIDENCE', 'text': ev1['text'], 'rows': int(e_new.shape[0])}
    D1RUN882.update({'T': T, 'q': q, 'ctx': ctx, 'g': g, 'obs_mem': obs_mem, 'c_new': c_new, 'e_new': e_new, 'h1': h1,
                     'decision_seal': out['provenance']['decision_memory_full_seal'], 'Ex': Ex})
    if not all(ck.values()): raise Gate882('D1_POST_EXECUTION %s' % sorted(k for k, v in ck.items() if not v))
    if not (c_new.ndim == 2 and c_new.shape[0] and e_new.ndim == 2 and e_new.shape[0]):
        out['store'] = {'decision': None, 'written': None, 'why': 'EMPTY_OBSERVATION_ROWS'}; del keep, cl, hx, ha
        return out
    sr = store_reading881(env, obs_mem, q, env['embed841'](A).detach().float().cpu(), c_new, e_new)
    out['store'] = {'decision': sr['decision'], 'mass': sr['mass'], 'normalized': sr['normalized'], 'written': None, 'why': None}
    if sr['decision'] != 'STORE':
        out['store']['why'] = 'MODEL_' + str(sr['decision']); del keep, cl, hx, ha
        return out
    n1 = n2 + L2 + la; P = int(env['P'])
    Y, _ = env['make_x851'](env['C_SLOT851'], [([], c_new), (env['E_SLOT851'], e_new)], []); body = int(Y.shape[0])
    own2 = env['cache_build'](list(keep)); forward873(env, own2, Y, n1); gH = kv873(env, own2); del own2
    h3c = xspan878(env, cl, Y.reshape(1, body, Hd), one(n1 + body), 0, cut + 1); ffe882(body, 80 + cut + 1, 'd1_write_C')
    ck['C_explicit_lower_KV_bitwise'] = all(torch.equal(a_[:, :, n1:], b_[:, :, n1:n1 + body]) for i in range(cut + 1)
                                            for a_, b_ in zip(cache_kv870(cl, i), gH[i]))
    ck['C_h3_next_layer_KV_bitwise'] = all(torch.equal(a_, b_[:, :, n1:n1 + body]) for a_, b_ in zip(next_kv878(env, h3c, n1), gH[cut + 1]))
    if not all(ck.values()):
        out['store']['why'] = 'WRITE_GATE_FAILED'; raise Gate882('D1_C_GATES %s' % sorted(k for k, v in ck.items() if not v))
    A0 = ADDR882['live'][r]
    prov = {'namespace': 'REAL', 'test': 'TEST882', 'requires_parent': True, 'parent_catalog_id': row['id'], 'parent_sha256': row['sha256'],
            'receiver_item': T['item'], 'receiver_step': Ex['steps'], 'receiver_B_full_seal': out['provenance']['B_full_seal'],
            'decision_memory_full_seal': out['provenance']['decision_memory_full_seal'], 'source_prefix_tokens': n2,
            'source_storage_positions': [n2, n1 + body], 'cartridge_positions': [P, P + n1 + body - n2], 'cut': cut,
            'qid_sha256': out['provenance']['qid_sha256'], 'action': action, 'action_token_ids': list(A), 'effect': eff.get('effect'),
            'chosen': eff.get('chosen'), 'C_kind': 'NEXT_MODEL_OBSERVATION', 'spans_body': {'X2': [0, L2], 'A': [L2, L2 + la],
                                                                                           'C': [L2 + la, L2 + la + body]},
            'decision_policy_path': 'VIS_MASKED_XCAR878', 'write_cache_path': 'PARENT_CONDITIONED_NATIVE_WRITE',
            'store_reading': {'decision': sr['decision'], 'mass': sr['mass']}, 'weights_digest': WEIGHTS0_878,
            'engine_git_blob': ENGINE_BLOB882, 'head': HEAD882, 'cell_git_blob': STATE882['source'].get('executed_cell_git_blob'),
            'address_domain': ADDRESS_DOMAIN882['id'], 'address_sha256': A0['key_sha256'], 'address_z_sha256': A0['rec']['z_sha256'],
            'address_prompt_sha256': A0['rec']['prompt_sha256'], 'address_computed': 'G4 live query, before the action',
            'contains': 'native h3 + L0-3 K/V of [X2][A][C] only; meaningful only after [B][parent]'}
    eid = eid882(prov)
    blob = key_blob882(A0['key'], {'domain': ADDRESS_DOMAIN882['id'], 'z_sha256': A0['rec']['z_sha256'],
                                   'prompt_sha256': A0['rec']['prompt_sha256'], 'rows_sha256': A0['rec'].get('rows_sha256'),
                                   'raw_sha256': A0['rec'].get('raw_sha256'), 'mu_addr_sha256': MU882['sha256'],
                                   'computed': 'BEFORE_ACTION'})
    def write(d):
        global EXP_DIR878
        old, EXP_DIR878 = EXP_DIR878, BANK_DATA882
        try: return write_exp878(env, eid, gH, torch.cat([hx, ha, h3c], dim=1), n2, n1 + body, L2 + la, prov)
        finally: EXP_DIR878 = old
    verify = lambda e: load_exp878(env, e) and None
    try:
        res = STORE_BANK882.commit(eid, str(BANK_DATA882), write, verify, blob, parent=(row['id'], row['sha256']))
    except CommitUncertain881 as exc:
        out['store'].update({'written': None, 'why': 'COMMIT_UNCERTAIN', 'commit_error': str(exc)})
        out['store']['recovery'] = STORE_BANK882.recover(verify)
        raise Gate882('D1_COMMIT_UNCERTAIN (recovered: %s)' % _j882.dumps(out['store']['recovery'], default=str))
    entry = res['entry']; STATE882['budget']['ssd_bytes'] += int(entry['bytes'])
    out['store'].update({'written': {k: entry[k] for k in ('id', 'file', 'sha256', 'bytes', 'body_tokens', 'roundtrip_K_rel', 'pre_C_seal',
                                                          'address_sha256', 'parent_id', 'parent_sha256')}, 'why': 'REAL_WRITE_COMMITTED'})
    out['store']['written']['generation'] = res['generation']; out['store']['transaction'] = res['state']
    if entry['roundtrip_K_rel'] > ROPE_TOL878: raise Gate882('D1_ROUNDTRIP %.3e' % entry['roundtrip_K_rel'])
    D1RUN882['child_id'] = eid
    del keep, cl, hx, ha, h3c, Y, gH; gc.collect(); torch.cuda.empty_cache()
    return out


# ============================ D2: next decision from the D1 observation, own retrieval of the new cartridge ============================
def d2_882(env):
    run = D1RUN882; out = STATE882['d2']; ck = out['checks'] = {}; T, q, ctx = run['T'], run['q'], run['ctx']
    out.update({'run': True, 'status': 'STARTED', 'attempts': 1, 'retry': 'NONE (one pre-registered attempt)'})
    B2 = run['obs_mem']; out['base_memory'] = 'D1_RECEIVER_B' if B2 is T['m'] else 'POST_ACTION_ENVIRONMENT_MEMORY'
    c_new, e_new = run['c_new'], run['e_new']; rel = env['relation852'](c_new, e_new)
    rel = rel.detach().float().cpu() if hasattr(rel, 'detach') else rel
    Z2 = [(env['C_SLOT851'], c_new), (env['E_SLOT851'], e_new), (env['R_SLOT852'], rel)]
    if ctx['path']: Z2.append((SLOTS866['POINTER'], ctx['path'][-1]['rows'].detach().float().cpu()))
    zc2 = {'phase': 'PRE_ACTION', 'qid': T['qid'], 'segments': Z2, 'step': 'D2'}
    zc2['z_sha256'] = digest_segments882(Z2)
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
    X2d, _ = env['make_x851'](pre, Z2, post); L2 = int(X2d.shape[0])
    guard882('d2', HEADROOM_GIB882)
    nm, _, _, _ = decide874(env, B2, X2d, []); ffe882(L2 + cont_tokens881(), 80, 'd2_no_memory')
    out['no_memory_counterfactual'] = dict(reading_view882(nm), role='READ_ONLY_COUNTERFACTUAL (never executed)')
    need = need882(env, B2, zc2); out['need'] = {k: need[k] for k in ('decision', 'why', 'mass', 'normalized')}
    raw, arec = preC882(env, zc2); key = center882(env, raw, MU882['mu'])
    out['query'] = dict(arec, key_sha256=None if key is None else _h882.sha256(rows_np882(key).tobytes()).hexdigest())
    view, omap, rows = bank_view882(STORE_BANK882, ID_SALT882)
    rt = route882(key, view, NULL_KEY882[0], FROZEN882['TH'], score882); out['route'] = rt
    chosen = omap[rt['chosen']]['id'] if rt.get('chosen') else None
    out['own_cartridge_selected'] = chosen is not None and chosen == run.get('child_id')
    rec = {'cell': 'D2', 'retry': 0, 'B_full_seal': full_seal881(B2)['all'], 'X2_sha256': zc2['z_sha256'], 'need': out['need'],
           'query': out['query'], 'route': rt, 'mount': None, 'readout': None, 'execution': {'status': 'NOT_RUN'},
           'store': {'decision': None, 'written': None, 'why': 'D2_NO_STORE_BY_DESIGN'}, 'offline': 'SEALED_UNTIL_ALL_LIVE_WORK_ENDS'}
    if need['decision'] != 'USE_MEMORY' or rt['decision'] != 'ACCEPT':
        out['status'] = 'D2_NO_MOUNT_NEED_%s_ROUTE_%s' % (need['decision'], rt['decision']); decision_log882(rec); del X2d
        return out
    res = resolve_parent882(chosen, rows, mounted=()); by = {x['id']: x for x in rows}; chain = [by[i] for i in res['append']]
    g2, mrec = mount882(env, B2, chain, 'D2'); out['mount'] = dict(mrec, resolver=res); rec['mount'] = out['mount']
    if g2 is None:
        decision_log882(rec); raise Gate882('D2_MOUNT_GATES_FAIL %s' % _j882.dumps(mrec, default=str)[:600])
    out['mount_pass'] = True
    out['parent_seal_equal'] = len(mrec['elements']) == 2 and mrec['elements'][-1]['memory_before_full_seal'] == run['decision_seal']
    val = validate882(env, g2, zc2); out['validation'] = {k: val[k] for k in ('decision', 'why', 'mass', 'normalized', 'veto')}
    if val['veto']:
        del g2; gc.collect(); torch.cuda.empty_cache(); out['status'] = 'D2_MODEL_REJECT_RESTORED'; decision_log882(rec)
        return out
    n0 = mrec['elements'][-1]['positions'][0]
    Ly = layout_at882(env, n0, chain[-1]['entry'], L2)
    Gs = readout_single882(env, 'D2', X2d, Ly, g2, B2, rec['B_full_seal'])
    out['readout_pass'] = bool(Gs['gate2_pass']); stored = ARMS881['D2']['VIS_L']
    vis = xread881(env, g2, X2d, [Ly['C']], True, 'D2_VIS_recompute')
    out['vis_exact'] = ck['VIS_recompute_equals_readout_VIS'] = same_reading881(vis, stored)
    out['vis_action'] = vis['action']; out['no_memory_action'] = nm['action']
    out['policy'] = reading_view882(vis); rec['readout'] = {'gate2': Gs['gate2'], 'VIS': out['policy'],
                                                           'C_BLIND': reading_view882(ARMS881['D2']['C_BLIND_L'])}
    if not out['vis_exact']:
        out['status'] = 'TECHNICAL_BLOCK_BEFORE_EXECUTION'; decision_log882(rec); raise Gate882('D2_VIS_RECOMPUTE_NOT_EXACT')
    if vis['action'] in ('INVALID', 'ACCEPT', 'STOP'):
        out['status'] = 'TERMINAL_NO_ENV_TRANSITION'; out['executed_equals_vis'] = None
        rec['execution'] = {'status': 'TERMINAL_NO_ENV_TRANSITION', 'action': vis['action'], 'effect': None}; decision_log882(rec)
        return out
    legacy = env['gen851'](g2, pre, Z2, post); check_output_h863(legacy, 'T882_D2_CONTROL_ROWS')
    ffe882(seg_tokens882(pre, Z2, post) + len(legacy.get('toks') or []), 80, 'd2_control_rows')
    ctx['memx'] = g2; ctx['steps'] = int(ctx['steps']) + 1; n_ev = len(ctx['events'])
    execute866(env, ctx, vis['action'], run['h1'], legacy, {'segments': Z2})
    eff = ctx['events'][-1] if len(ctx['events']) > n_ev else {}
    out['environment_effect'] = {k: eff.get(k) for k in ('action', 'effect', 'chosen', 'mounted_before', 'mounted_after', 'path_after')}
    out['executed_equals_vis'] = eff.get('action') == vis['action']; out['status'] = 'EXECUTED'
    rec['execution'] = {'status': 'EXECUTED', 'action': vis['action'], 'effect': eff.get('effect')}; decision_log882(rec)
    del X2d, g2; gc.collect(); torch.cuda.empty_cache()
    return out

# ============================ static gates from the locked 869 records (no CAR result is read) ============================
def targets882(refs):
    ctl = lambda item: [e for e in refs[(item, ARM878)]['events'] if e['type'] == 'CONTROL']
    canon = lambda d: _j882.dumps(d, sort_keys=True)
    items = list(SOURCES878) + list(FORKS878) + list(EXTRA882) + ['I867_%s_%s' % (w, c) for w in CAL_WORLDS882 for c in ('FORK', 'LIVE')]
    for item in items:
        if (item, ARM878) not in refs: raise Gate882('RECORD_MISSING ' + item)
    src = {}
    for item in BANK_ITEMS882 + DIAG_ITEMS882:
        cs = ctl(item)
        if len(cs) < POST_STEP878 or [x['record']['action'] for x in cs[:2]] != ['ADVANCE', ACTION878]: raise Gate882('T2_PATH ' + item)
        eff = [e for e in refs[(item, ARM878)]['events'] if e['type'] == 'EFFECT' and e.get('effect') == 'MOUNTED']
        if not (eff and eff[0].get('action') == ACTION878): raise Gate882('OUTCOME_EFFECT ' + item)
        src[item] = {'card': eff[0]['chosen'], 't2_state_sha256': cs[PRE_STEP878 - 1]['record']['state_sha256'],
                     'world_index': refs[(item, ARM878)]['world_index']}
    for w in ('00', '01'):
        M, L = src['I867_%s_MISSING' % w], src['I867_%s_LIVE' % w]
        if canon(M['t2_state_sha256']) != canon(L['t2_state_sha256']): raise Gate882('T2_STATE_NOT_SHARED ' + w)
        if M['card'] == L['card']: raise Gate882('OUTCOME_CARDS_EQUAL ' + w)
    rec = {}
    for r in RECEIVERS882:
        item = 'I867_%s_FORK' % r; cs = ctl(item)
        if len(cs) < FORK_STEP878: raise Gate882('FORK_STEP_MISSING ' + item)
        f = cs[FORK_STEP878 - 1]; ev = refs[(item, ARM878)]['events']; ix = ev.index(f)
        nxt = next((e for e in ev[ix + 1:] if e['type'] == 'EFFECT'), None)
        rec[r] = {'item': item, 'mounted': list(f['mounted']), 'state_sha256': f['record']['state_sha256'],
                  'world_index': refs[(item, ARM878)]['world_index'], 'recorded_action': f['record']['action'],
                  'recorded_effect': None if nxt is None else {k: nxt.get(k) for k in ('action', 'effect', 'chosen')}}
    cal = {}
    for w in CAL_WORLDS882:
        fk, lv = ctl('I867_%s_FORK' % w), ctl('I867_%s_LIVE' % w)
        if len(fk) < FORK_STEP878 or len(lv) < PRE_STEP878: raise Gate882('CALIBRATION_STEPS ' + w)
        cal[w] = {'world_index': refs[('I867_%s_FORK' % w, ARM878)]['world_index'], 'key_action': lv[PRE_STEP878 - 1]['record']['action'],
                  'query_action': fk[FORK_STEP878 - 1]['record']['action']}
        if refs[('I867_%s_LIVE' % w, ARM878)]['world_index'] != cal[w]['world_index']: raise Gate882('CALIBRATION_PAIR_CONTEXT ' + w)
    live_idx = {v['world_index'] for v in rec.values()} | {v['world_index'] for v in src.values()}
    cal_idx = [v['world_index'] for v in cal.values()]
    if len(set(cal_idx)) != len(cal_idx) or set(cal_idx) & live_idx: raise Gate882('CALIBRATION_NOT_DISJOINT')
    cards = {v['card'] for k, v in src.items() if k in BANK_ITEMS882}
    shas = {canon(v['t2_state_sha256']) for v in src.values()}
    for r, v in rec.items():
        if set(v['mounted']) & cards: raise Gate882('RECEIVER_ALREADY_HOLDS_A_BANK_OUTCOME R' + r)
        if canon(v['state_sha256']) in shas: raise Gate882('RECEIVER_IS_A_SOURCE_STATE R' + r)
    return {'sources': src, 'receivers': rec, 'calibration': cal, 'disjoint': True}


# ============================ replay taps: TEST878 probe, extra source adapter, pre-action Z capture ============================
def source_probe882(env, ctx, record, state, label):
    # probe878 source branch for sources without a TEST873 reference (same gates otherwise; the locked writer writes the file)
    side = ctx['spec']['item']; qid = ctx['spec']['qid']
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=env['QTEXT841'][qid]))); post = env['REVIEW_SUFFIX851']
    out = STATE882['sides'].setdefault(side, {'checks': {}, 'error': None, 'adapter': 'source_probe882'}); c = out['checks']
    try:
        ids = dict(ACTION_IDS867); dev = env['DEV']; cut = APPEND873['CUT']; Hd = int(env['H'])
        if ctx['steps'] == PRE_STEP878:
            segs2 = list(state['segments']); X2, _ = env['make_x851'](pre, segs2, post); L2 = int(X2.shape[0])
            m2 = [tuple(t.clone() for t in kv) for kv in ctx['memx']]; n2 = length873(env, m2)
            cache = env['cache_build'](list(m2)); c['t2_CAR_equals_record'] = same873(car873(env, cache, X2), record['reading'])
            c['t2_crops'] = int(cache.get_seq_length()) == n2 + L2
            own = env['cache_build'](list(kv873(env, cache))); del cache
            A = ids[record['action']]; la = len(A); EA = env['embed841'](A)
            forward873(env, own, EA, n2 + L2); keep_own = kv873(env, own); del own
            c['commit_length'] = length873(env, keep_own) == n2 + L2 + la
            cl = env['cache_build'](list(m2)); one = lambda n: torch.ones((1, n), device=dev, dtype=torch.long)
            hx = xspan878(env, cl, X2.reshape(1, L2, Hd), one(n2 + L2), 0, cut + 1)
            ha = xspan878(env, cl, EA.reshape(1, la, Hd), one(n2 + L2 + la), 0, cut + 1)
            c['explicit_lower_KV_bitwise'] = all(torch.equal(x, y) for i in range(cut + 1)
                                                 for x, y in zip(cache_kv870(cl, i), keep_own[i]))
            nk = [next_kv878(env, hx, n2), next_kv878(env, ha, n2 + L2)]; ref = keep_own[cut + 1]
            c['h3_next_layer_KV_bitwise'] = all(torch.equal(nk[j][t], ref[t][:, :, a:b]) for j, (a, b) in
                                                enumerate(((n2, n2 + L2), (n2 + L2, n2 + L2 + la))) for t in (0, 1))
            del cl, nk
            ffe882(L2 + cont_tokens881() + la, 80, 'source_probe'); ffe882(L2 + la, cut + 1, 'source_probe_lower')
            assert all(c.values()), ('T2_GATES', c)
            T2_KEEP878[side] = {'own': keep_own, 'A_ids': A, 't2_action': record['action'], 'h3': torch.cat([hx, ha], dim=1),
                                'm2': m2, 'X2': X2, 'L2': L2, 'la': la, 'n2': n2, 'mounted': list(ctx['M'])}
            return
        if ctx['steps'] != POST_STEP878: return
        z = T2_KEEP878.pop(side)
        memx = ctx['memx']; eff = [e for e in ctx['events'] if e.get('type') == 'EFFECT'][-1]; card = eff.get('chosen')
        body = int(env['entries'][card]['body_tokens']); n3 = int(memx[0][0].shape[-2]); P = int(env['P'])
        c['card_mounted'] = eff.get('effect') == 'MOUNTED' and list(ctx['M'])[-1] == card
        names = slot_names869(env, list(state['segments']))
        X3, _ = env['make_x851'](pre, [s for s, n in zip(state['segments'], names) if n not in ('FV', 'FK')], post)
        seal0 = prefix_seals865(env, memx); hook0 = assert_hook_free859(env, 'T882_before_' + side)
        gH, n_before = append_card873(env, z['own'], card); del z['own']
        x3s = n_before + body; n2, L2, la = z['n2'], z['L2'], z['la']
        c['timeline'] = n_before == n2 + L2 + la
        rephase = APPEND873['rephase']
        c['lower_V_bitwise'] = all(torch.equal(gH[i][1][:, :, n_before:], memx[i][1][:, :, n3 - body:]) for i in range(cut + 1))
        rope = max(float(torch.linalg.vector_norm(rephase(gH[i][0][:, :, n_before:], torch.arange(n_before, x3s, device=dev),
            torch.arange(n3 - body, n3, device=dev)).float() - memx[i][0][:, :, n3 - body:].float())) /
            max(float(torch.linalg.vector_norm(memx[i][0][:, :, n3 - body:].float())), 1e-30) for i in range(cut + 1))
        c['lower_K_rephase'] = rope <= ROPE_TOL878; out['lower_K_rephase_rel'] = rope
        rH, _, _, _ = decide874(env, gH, X3, [])
        out['H_reference'] = 'NO_TEST873_REFERENCE (not in SIDES874): H is the reference of the later persist878 recon'
        cpc, _ = APPEND873['load'](card)
        c['card_rows'] = int(cpc['n']) - P == body and cpc['book_id'] == card
        h3 = torch.cat([z['h3'], cpc['h'][:, P:, :].to(dev)], dim=1); del cpc
        prov = {'item': side, 'arm': ARM878, 'step_pre': PRE_STEP878, 'step_post': POST_STEP878, 'qid': qid,
                'goal_text_sha256': sha256_bytes864(env['QTEXT841'][qid].encode()), 'pre_action_state_sha256': STATIC_T2_SHA882[side],
                'action': z['t2_action'], 'action_token_ids': list(z['A_ids']), 'outcome_cartridge': card,
                'outcome_cartridge_file_sha256': env['entries'][card].get('sha256'), 'mounted_before': z['mounted'],
                'spans_body': {'X2': [0, L2], 'A': [L2, L2 + la], 'C': [L2 + la, L2 + la + body]},
                'source_storage_positions': [n2, x3s], 'cartridge_positions': [P, P + x3s - n2], 'source_prefix_seal': seal0,
                'engine_git_blob': ENGINE_BLOB882, 'cell_git_blob': STATE882['source'].get('executed_cell_git_blob'),
                'weights_digest': WEIGHTS0_878, 'writer': 'locked write_exp878 (via source_probe882)',
                'contains': 'native h3 + L0-3 K/V of [X2][A][C] only'}
        eid = eid882(prov)
        entry = write_exp878(env, eid, gH, h3, n2, x3s, L2 + la, prov)
        c['roundtrip_K'] = entry['roundtrip_K_rel'] <= ROPE_TOL878
        c['memory_seal'] = prefix_seals865(env, memx) == seal0
        hook1 = assert_hook_free859(env, 'T882_after_' + side)
        c['hook_free'] = not any(x['hook_count'] or x['transformers_output_capturing_installed'] for x in (hook0, hook1))
        ffe882(body + int(X3.shape[0]) + cont_tokens881(), 80, 'source_probe')
        out.update({'role': 'SOURCE', 'card': card, 'H': arm878(rH), 'experience': eid, 'experience_bytes': entry['bytes'],
                    'roundtrip_K_rel': entry['roundtrip_K_rel'], 'X3_len': int(X3.shape[0])})
        assert all(c.values()), ('SIDE_GATES', c)
        STATE882['experience'][eid] = entry
        SRC882[side] = {'side': side, 'cond': 'LIVE', 'm2': z['m2'], 'X3': X3.detach().cpu(), 'H': arm878(rH), 'm': marg877(rH),
                        'entry': entry, 'n2': n2, 'L2': L2, 'la': la, 'body': body, 'qid': qid, 'card': card,
                        'A_ids': list(z['A_ids']), 't2_action': z['t2_action']}
        del gH, h3, z, X3, rH; gc.collect(); torch.cuda.empty_cache()
        line882('SOURCE', side, _j882.dumps({k: out[k] for k in ('card', 'H', 'experience', 'experience_bytes', 'X3_len')}, sort_keys=True))
    except Exception as exc:
        out['error'] = '%s: %s' % (type(exc).__name__, str(exc)[:400]); out['traceback'] = traceback.format_exc()
        (ROOT864 / ('882_%s_t%d_traceback.txt' % (side, ctx['steps']))).write_text(out['traceback'], encoding='utf-8')
        line882('POINT_ERROR', side, 't=%d' % ctx['steps'], out['error'])


def probe882(env, ctx, record, state, label):
    side = ctx['spec']['item']; step = ctx['steps']
    if (label, step) in (('T2_EXPERIENCE', PRE_STEP878), ('T1_TARGET', FORK_STEP878), ('Z_CAL_QUERY', FORK_STEP878),
                         ('Z_CAL_KEY', PRE_STEP878)):
        segs = [(list(s_), r_.detach().float().cpu().clone()) for s_, r_ in state['segments']]
        ZCAP882[side] = {'phase': 'PRE_ACTION', 'step': step, 'qid': ctx['spec']['qid'], 'segments': segs,
                         'z_sha256': digest_segments882(segs), 'record_action': record.get('action'),
                         'state_sha256': record.get('state_sha256'), 'mounted': list(ctx['M'])}
    if side in SOURCES878 or side in FORKS878:
        probe878(env, ctx, record, state, label)
    elif side in EXTRA882:
        source_probe882(env, ctx, record, state, label)
    if side in FORKS878 and step == FORK_STEP878:
        EXEC882[side] = {'spec': {k: (list(v) if isinstance(v, (list, tuple)) else v) for k, v in ctx['spec'].items() if k != 'xray'},
                         'segments': [(list(s_), r_.detach().float().cpu().clone()) for s_, r_ in state['segments']],
                         'path': [{'rows': p['rows'].detach().float().cpu().clone(), 'text': p['text']} for p in ctx['path']],
                         'steps': ctx['steps'], 'candidate_text': record.get('candidate_text'),
                         'state_sha256': record.get('state_sha256')}


xray_point870 = probe882


# ============================ G1: replays, physical cartridges, Z capture ============================
def g1_replays882(env, by_key, refs):
    global EXP_DIR878
    plan = [(s, {PRE_STEP878: 'T2_EXPERIENCE', POST_STEP878: 'T3_EXPERIENCE'}) for s in list(SOURCES878) + list(EXTRA882)] + \
           [(s, {FORK_STEP878: 'T1_TARGET'}) for s in FORKS878] + \
           [('I867_%s_FORK' % w, {FORK_STEP878: 'Z_CAL_QUERY'}) for w in CAL_WORLDS882] + \
           [('I867_%s_LIVE' % w, {PRE_STEP878: 'Z_CAL_KEY'}) for w in CAL_WORLDS882]
    STATE882['physical']['replay_plan'] = [[s, sorted(t.items())] for s, t in plan]
    try:
        for side, tg in plan:
            guard882('replay_' + side)
            EXP_DIR878 = DIAG_DATA882 if side.endswith('_MISSING') else BANK_DATA882
            rep = run_replay870(env, {'id': side, 'item': side, 'arm': ARM878, 'targets': tg}, by_key, refs)
            T2_KEEP878.pop(side, None)
            if not rep['ok']: STATE882['blocks'].append('REPLAY_NOT_EXACT:' + side)
    finally:
        EXP_DIR878 = BANK_DATA882
    for side, s in STATE882['sides'].items():
        if s.get('error'): STATE882['blocks'].append('POINT_ERROR:' + side)
    if STATE882['blocks']: raise Gate882('G1_REPLAY %s' % STATE882['blocks'])


def g1_physical882(env):
    P = STATE882['physical']; P['cartridges'] = {}
    for side in BANK_ITEMS882 + DIAG_ITEMS882:
        S = SRC878.get(side) or SRC882.get(side); z = ZCAP882.get(side)
        if S is None: raise Gate882('SOURCE_EXPERIENCE_NOT_CAPTURED ' + side)
        if z is None or z['step'] != PRE_STEP878 or z['record_action'] != ACTION878: raise Gate882('PRE_ACTION_Z_NOT_CAPTURED ' + side)
        cp = load_exp878(env, S['entry']); del cp; STATE882['budget']['ssd_bytes'] += int(S['entry']['bytes'])
        P['cartridges'][side] = {'id': S['entry']['id'], 'sha256': S['entry']['sha256'], 'bytes': S['entry']['bytes'],
                                 'body_tokens': S['entry']['body_tokens'], 'roundtrip_K_rel': S['entry']['roundtrip_K_rel'],
                                 'reload': 'FILE_AND_TENSOR_SHA_PASS', 'z_sha256': z['z_sha256']}
    for w in ('00', '01'):
        M, L = SRC878['I867_%s_MISSING' % w], SRC878['I867_%s_LIVE' % w]
        g = {'same_t2_spans': (M['n2'], M['L2'], M['la']) == (L['n2'], L['L2'], L['la']),
             'same_action_tokens': M['A_ids'] == L['A_ids'] and M['t2_action'] == L['t2_action'] == ACTION878,
             'real_cards_differ': M['card'] != L['card'], 'pre_C_cartridge_rows_bitwise': M['entry']['pre_C_seal'] == L['entry']['pre_C_seal'],
             'C_cartridge_sha_differ': M['entry']['sha256'] != L['entry']['sha256'],
             'pre_action_Z_bitwise_equal': ZCAP882['I867_%s_MISSING' % w]['z_sha256'] == ZCAP882['I867_%s_LIVE' % w]['z_sha256'],
             'live_in_bank_namespace': str(BANK_DATA882) in L['entry']['file'], 'missing_in_diag_namespace': str(DIAG_DATA882) in M['entry']['file']}
        P['pair_' + w] = g
        if not all(g.values()): raise Gate882('SOURCE_PAIR_GATES %s %s' % (w, _j882.dumps(g)))
    for item in ['I867_%s_FORK' % r for r in RECEIVERS882] + ['I867_%s_%s' % (w, c) for w in CAL_WORLDS882 for c in ('FORK', 'LIVE')]:
        if item not in ZCAP882: raise Gate882('PRE_ACTION_Z_NOT_CAPTURED ' + item)
    for side in DIAG_ITEMS882:                       # matched partners: catalogued, never addressable (no address sidecar)
        S = SRC878[side]
        reg = STORE_DIAG882.commit(S['entry']['id'], str(DIAG_DATA882), lambda d, S=S: S['entry'],
                                   lambda e: load_exp878(env, e) and None, prewritten=True)
        P.setdefault('diag_catalog', {})[side] = {'state': reg['state'], 'generation': reg['generation']}
    line882('G1 PASS', _j882.dumps({k: v for k, v in P.items() if k.startswith('pair_')}, sort_keys=True))


def fixture_seal882(env, by_key, refs):
    # OFFLINE labels, sealed before the first live decision; no runtime function reads them
    F = {'bank': {}, 'diag': {}, 'receivers': {}}
    for cat, side in sorted(BANKSIDE882.items()) + [(SRC878[s]['entry']['id'], s) for s in DIAG_ITEMS882]:
        spec = by_key[(int(side.split('_')[1]), side.split('_')[2])]; kinds = {v: k for k, v in world867(env, spec)['ids'].items()}
        S = SRC878.get(side) or SRC882.get(side)
        F['bank' if cat in BANKSIDE882 else 'diag'][cat] = {'item': side, 'world_index': refs[(side, ARM878)]['world_index'],
                                                            'card': S['card'], 'card_kind': kinds.get(S['card'], 'OTHER')}
    for r in RECEIVERS882:
        F['receivers'][r] = {'item': 'I867_%s_FORK' % r, 'world_index': refs[('I867_%s_FORK' % r, ARM878)]['world_index']}
    F['sealed_sha256'] = sha256_bytes864(_j882.dumps(F, sort_keys=True).encode()); F['sealed_before_live'] = True
    OFFLINE882.clear(); OFFLINE882.update(F)
    json_write864('882_fixtures_sealed.json', F)
    return F['sealed_sha256']


# ============================ G2: address domain, keys, SSD registration ============================
def g2_address882(env):
    A = STATE882['address']; A['records'] = {}; raws = {}
    for w in CAL_WORLDS882:
        for kind, item in (('Q', 'I867_%s_FORK' % w), ('K', 'I867_%s_LIVE' % w)):
            guard882('address_' + item, HEADROOM_GIB882)
            raw, rec = preC882(env, ZCAP882[item]); A['records'][item] = rec
            if raw is None: raise Revise882('CALIBRATION_ADDRESS_INVALID ' + item)
            raws[(kind, w)] = raw
    raw_sr, rec_sr = preC882(env, ZCAP882[SELF_RECALL_ITEM882]); A['records']['SELF_RECALL'] = rec_sr
    w0 = SELF_RECALL_ITEM882.split('_')[1]; base = raws[('K', w0)]
    if raw_sr is None: raise Revise882('SELF_RECALL_ADDRESS_INVALID')
    A['self_recall_raw_bitwise'] = bool(raw_sr.shape == base.shape and torch.equal(raw_sr, base))
    mu = torch.cat([raws[k] for k in sorted(raws)], dim=0).mean(dim=0)
    MU882.update({'mu': mu, 'sha256': _h882.sha256(rows_np882(mu).tobytes()).hexdigest(), 'rows': int(sum(int(v.shape[0]) for v in raws.values()))})
    dom, d = domain882(STATE882['memnull_seal'], MU882['sha256'], WEIGHTS0_878)
    ADDRESS_DOMAIN882.update({'id': dom, 'definition': d})
    rn, _ = query880(env, env['MUE845'].detach().float().cpu().reshape(1, -1)); ffe882(len(env['IDXPRE841']) + 1 + len(env['IDXPOST841']), 4, 'address_h3')
    NULL_KEY882[0] = center882(env, rn, mu)
    KC = {w: center882(env, raws[('K', w)], mu) for w in CAL_WORLDS882}; QC = {w: center882(env, raws[('Q', w)], mu) for w in CAL_WORLDS882}
    ksr = center882(env, raw_sr, mu)
    noise = max([abs(score882(ksr, KC[w0]) - score882(KC[w0], KC[w0]))] + [abs(score882(QC[w], ksr) - score882(QC[w], KC[w0])) for w in QC])
    ADDR882['cal'] = {'Q': QC, 'K': KC, 'noise': noise}
    A.update({'mu_addr_sha256': MU882['sha256'], 'mu_rows': MU882['rows'], 'domain': dom, 'self_recall_score_noise': noise,
              'null_key_sha256': _h882.sha256(rows_np882(NULL_KEY882[0]).tobytes()).hexdigest()})
    keys = {}
    for item in BANK_ITEMS882 + (DUP_ITEM882,):
        guard882('address_' + item, HEADROOM_GIB882)
        raw, rec = preC882(env, ZCAP882[item]); A['records'][item] = rec
        k = center882(env, raw, mu)
        keys[item] = None if k is None else {'key': k, 'rec': rec, 'key_sha256': _h882.sha256(rows_np882(k).tobytes()).hexdigest()}
    canon_recs = [r for r in A['records'].values() if not r['retry_prompt']]
    by_q = {}
    for r_ in canon_recs: by_q.setdefault(r_['qid_sha256'], set()).add(r_['prompt_sha256'])
    A['write_read_prompt_identical'] = len({r_['template_sha256'] for r_ in canon_recs}) == 1 and all(len(v) == 1 for v in by_q.values())
    A['dup_key_bitwise_equal_to_live'] = bool(keys[DUP_ITEM882] and keys['I867_00_LIVE'] and
                                              torch.equal(keys[DUP_ITEM882]['key'], keys['I867_00_LIVE']['key']))
    A['not_addressable'] = [i for i in BANK_ITEMS882 if keys[i] is None]
    verify = lambda e: load_exp878(env, e) and None
    for item in BANK_ITEMS882:
        if keys[item] is None: continue
        S = SRC878.get(item) or SRC882.get(item); eid = S['entry']['id']
        blob = key_blob882(keys[item]['key'], {'domain': dom, 'z_sha256': keys[item]['rec']['z_sha256'],
                                               'prompt_sha256': keys[item]['rec']['prompt_sha256'], 'rows_sha256': keys[item]['rec']['rows_sha256'],
                                               'raw_sha256': keys[item]['rec']['raw_sha256'], 'mu_addr_sha256': MU882['sha256'],
                                               'computed': 'FROM_THE_PRE_ACTION_Z_OF_THE_SOURCE_DECISION'})
        reg = STORE_BANK882.commit(eid, str(BANK_DATA882), lambda d, S=S: dict(S['entry']), verify, blob, prewritten=True)
        BANKSIDE882[eid] = item; A.setdefault('catalog', {})[item] = {'id': eid, 'state': reg['state'], 'generation': reg['generation'],
                                                                      'address_sha256': blob['meta']['address_sha256']}
    view, omap, rows = bank_view882(STORE_BANK882, ID_SALT882)
    STATE882['bank']['opaque_to_catalog'] = {op: r['id'] for op, r in omap.items()}
    reload_ok = all(torch.equal(view[op]['address_key'], keys[BANKSIDE882[r['id']]]['key']) for op, r in omap.items())
    dag = {r['id']: resolve_parent882(r['id'], rows)['depth'] for r in rows}
    A['G2'] = {'write_read_prompt_identical': A['write_read_prompt_identical'], 'ssd_key_reload_bitwise': reload_ok,
               'parent_dag_roots': all(v == 1 for v in dag.values()), 'bank_size': len(view),
               'memnull_seal_unchanged': physical_seal863(env, env['MEMNULL841']) == STATE882['memnull_seal'],
               'C_blind_provenance_dup_Z_equal': ZCAP882[DUP_ITEM882]['z_sha256'] == ZCAP882['I867_00_LIVE']['z_sha256'],
               'self_recall_raw_bitwise': A['self_recall_raw_bitwise'], 'keys_finite': all(bool(torch.isfinite(v['address_key']).all())
                                                                                         for v in view.values())}
    ADDR882['dup'] = keys[DUP_ITEM882]; ADDR882['bank_keys'] = keys
    line882('G2', _j882.dumps(A['G2'], sort_keys=True), 'domain', dom[:16], 'mu', MU882['sha256'][:16], 'noise=%.3e' % noise)
    if not all(A['G2'].values()): raise Gate882('G2_ADDRESS_DOMAIN %s' % sorted(k for k, v in A['G2'].items() if not v))


# ============================ G3: disjoint calibration, threshold freeze, control bite ============================
def g3_calibrate882(env):
    C = ADDR882['cal']; cal = calibrate882(C['Q'], C['K'], NULL_KEY882[0], score882, C['noise'])
    TH = freeze_thresholds882({'tau_neg': cal['tau_neg'], 'delta_tie': cal['delta_tie']}, 'LIVE',
                              {'mu_addr_sha256': MU882['sha256'], 'domain': ADDRESS_DOMAIN882['id'], 'calibration_worlds': list(CAL_WORLDS882),
                               'rule': [PREREG882['calibration']['tau_neg'], PREREG882['calibration']['delta_tie']]})
    view = cal_view882(C['K']); W = sorted(C['Q']); null = NULL_KEY882[0]
    base = {w: route882(C['Q'][w], view, null, TH, score882) for w in W}
    ks = key_shuffle882(view)
    kb = {w: bite882(base[w], route882(C['Q'][w], ks, null, TH, score882)) for w in W}
    qb = {w: bite882(base[w], route882(C['Q'][W[(i + 1) % len(W)]], view, null, TH, score882)) for i, w in enumerate(W)}
    w0 = W[0]; dupv = make_view882(list(view.values()) + [dict(view[w0], id='DUP_' + w0)])
    sv, ren = id_shuffle882(view, SHUFFLE_SALT882)
    ctrl = {'key_shuffle_bite': any(v['bite'] for v in kb.values()), 'query_shuffle_bite': any(v['bite'] for v in qb.values()),
            'duplicate_key_tie': route882(C['Q'][w0], dupv, null, TH, score882)['decision'] == 'TIE_NO_MOUNT',
            'empty_no_candidate': route882(C['Q'][w0], {}, null, TH, score882)['decision'] == 'NO_CANDIDATE',
            'order_invariant': all(same_route882(base[w], route882(C['Q'][w], order_shuffle882(view), null, TH, score882)) for w in W),
            'id_invariant': all(same_route882(base[w], route882(C['Q'][w], sv, null, TH, score882), ren) for w in W)}
    out = {k: v for k, v in cal.items()}; out.update({'controls': ctrl, 'key_bites': kb, 'query_bites': qb,
                                                       'frozen_threshold_sha256': TH['sha256'], 'tau_neg': TH['values']['tau_neg'],
                                                       'delta_tie': TH['values']['delta_tie']})
    did_not_bite = [k for k in ('key_shuffle_bite', 'query_shuffle_bite') if not ctrl[k]]
    out['controls_did_not_bite'] = ['G3_' + k.replace('_bite', '').upper() for k in did_not_bite]
    mech = all(ctrl[k] for k in ('duplicate_key_tie', 'empty_no_candidate', 'order_invariant', 'id_invariant'))
    out['pass'] = bool(cal['separation_pass'] and not did_not_bite and mech)
    STATE882['calibration'] = out
    STATE882['thresholds'] = {'values': TH['values'], 'sha256': TH['sha256'], 'scope': TH['scope'], 'provenance': TH['provenance']}
    json_write864('882_thresholds_frozen.json', dict(STATE882['thresholds'], frozen_before_live=True))
    line882('G3', 'tau_neg=%.5f delta_tie=%.5f' % (TH['values']['tau_neg'], TH['values']['delta_tie']),
            'final_pos=%d loo_correct=%d loo_false=%d sep=%.5f' % (cal['final_positive_accepted'], cal['loo_correct'],
                                                                  cal['loo_false_mounts'], cal['separation_min_pos_minus_max_neg']),
            _j882.dumps(ctrl, sort_keys=True), 'pass=%s' % out['pass'])
    if not mech: raise Gate882('G3_ROUTER_MECHANICS %s' % ctrl)
    if not out['pass']: raise Revise882('G3_CALIBRATION separation=%s did_not_bite=%s' % (cal['separation_pass'], did_not_bite))


# ============================ G4: receivers, live queries, CPU controls, live cells ============================
def receivers882(env):
    for r in RECEIVERS882:
        T = TGT878.get(('FORK', r))
        if T is None or T['item'] not in EXEC882 or T['item'] not in ZCAP882: raise Gate882('RECEIVER_NOT_CAPTURED R' + r)
        guard882('receiver_' + r)
        nm, _ = nread881(env, T['m'], T['X'], [], False, 'R%s_NO_MEMORY_native' % r)
        arm_record882('R' + r, '-', 'NO_MEMORY', nm, [])
        STATE882['receivers'][r] = {'item': T['item'], 'qid_sha256': sha256_bytes864(T['qid'].encode()), 'mounted': T['mounted'],
                                    'X_len': T['X_len'], 'X_sha256': tsha881(T['X']), 'memory_tokens': length873(env, T['m']),
                                    'B_full_seal': full_seal881(T['m'])['all'], 'no_memory_CAR': reading_view882(nm),
                                    'z_sha256': ZCAP882[T['item']]['z_sha256']}


def g4_queries882(env):
    ADDR882['live'] = {}
    for r in RECEIVERS882:
        guard882('live_query_' + r, HEADROOM_GIB882)
        raw, rec = preC882(env, ZCAP882['I867_%s_FORK' % r]); k = center882(env, raw, MU882['mu'])
        ADDR882['live'][r] = {'raw': raw, 'key': k, 'rec': rec, 'key_sha256': None if k is None else _h882.sha256(rows_np882(k).tobytes()).hexdigest()}
        STATE882['address'].setdefault('live', {})[r] = dict(rec, key_sha256=ADDR882['live'][r]['key_sha256'])
    recs = STATE882['address']['records']           # same question: the live read prompt must be the write prompt byte for byte
    STATE882['address']['live_prompt_equals_write_prompt'] = all(
        STATE882['address']['live'][r]['prompt_sha256'] == recs['I867_%s_LIVE' % r]['prompt_sha256'] and
        STATE882['address']['live'][r]['template_sha256'] == recs['I867_%s_LIVE' % r]['template_sha256'] for r in RECEIVERS882)
    if not STATE882['address']['live_prompt_equals_write_prompt']: raise Gate882('G2_LIVE_PROMPT_NE_WRITE_PROMPT')


def g4_controls882(env):
    TH, null = FROZEN882['TH'], NULL_KEY882[0]; view, omap, rows = bank_view882(STORE_BANK882, ID_SALT882)
    Q = {r: ADDR882['live'][r]['key'] for r in RECEIVERS882}; out = STATE882['controls']; dnb = []
    base = {r: route882(Q[r], view, null, TH, score882) for r in RECEIVERS882}
    out['base'] = {r: {k: base[r][k] for k in ('decision', 'chosen', 'top3', 'null', 'margin', 'reasons')} for r in RECEIVERS882}
    out['C3'] = {}
    for r in RECEIVERS882:                           # experimenter-built control bank: the source of this receiver's goal removed
        rel = [op for op, row in omap.items() if BANKSIDE882.get(row['id']) == 'I867_%s_LIVE' % r]
        v3 = {op: e for op, e in view.items() if op not in rel}
        r3 = route882(Q[r], v3, null, TH, score882); out['C3'][r] = {k: r3[k] for k in ('decision', 'chosen', 'top3', 'null', 'reasons')}
    out['C4'] = route882(Q[D1_RECEIVER882], {}, null, TH, score882)['decision']
    ks = key_shuffle882(view)
    out['C5'] = {r: (bite882(base[r], route882(Q[r], ks, null, TH, score882)) if (ks is not None and Q[r] is not None) else 'NOT_RUN')
                 for r in RECEIVERS882}
    out['C6'] = bite882(base['00'], route882(Q['01'], view, null, TH, score882)) if all(v is not None for v in Q.values()) else 'NOT_RUN'
    if any(v != 'NOT_RUN' and not v['bite'] for v in out['C5'].values()): dnb.append('C5_KEY_SHUFFLE')
    if out['C6'] != 'NOT_RUN' and not out['C6']['bite']: dnb.append('C6_QUERY_SHUFFLE')
    dup = ADDR882.get('dup'); lv = [op for op, row in omap.items() if BANKSIDE882.get(row['id']) == 'I867_00_LIVE']
    if dup and lv:
        M = SRC878[DUP_ITEM882]['entry']
        dv = make_view882([view[lv[0]], {'id': 'M882_DUP_' + M['sha256'][:11], 'sha256': M['sha256'], 'tensor_sha': M['tensor_sha'],
                                         'address_key': dup['key'], 'address_sha256': dup['key_sha256'], 'parent_id': None,
                                         'parent_sha256': None, 'body_tokens': int(M['body_tokens']), 'requires_parent': False,
                                         'generation': 0}])
        r7 = route882(Q[D1_RECEIVER882], dv, null, TH, score882)
        out['C7'] = {'decision': r7['decision'], 'reasons': r7['reasons'], 'exact_duplicate': dup['key_sha256'] == view[lv[0]]['address_sha256'],
                     'scores': r7['scores']}
    else:
        out['C7'] = {'decision': 'NOT_RUN', 'why': 'DUPLICATE_ITEM_HAS_NO_VALID_ADDRESS'}
    sv, ren = id_shuffle882(view, SHUFFLE_SALT882)
    out['order_invariant'] = all(same_route882(base[r], route882(Q[r], order_shuffle882(view), null, TH, score882)) for r in RECEIVERS882)
    out['id_invariant'] = all(same_route882(base[r], route882(Q[r], sv, null, TH, score882), ren) for r in RECEIVERS882)
    out['controls_did_not_bite'] = dnb
    out['empty_safe'] = out['C4'] == 'NO_CANDIDATE'
    out['tie_safe'] = out['C7']['decision'] in ('TIE_NO_MOUNT', 'AMBIGUOUS_NO_MOUNT', 'NO_MATCH')
    out['pass'] = bool(out['empty_safe'] and out['C7']['decision'] != 'ACCEPT' and out['order_invariant'] and out['id_invariant'])
    line882('G4 CONTROLS', _j882.dumps({k: out[k] for k in ('C4', 'order_invariant', 'id_invariant', 'controls_did_not_bite', 'empty_safe',
                                                           'tie_safe', 'pass')}, sort_keys=True), 'C7', out['C7']['decision'])
    if not out['pass']: raise Gate882('G4_ROUTER_CONTROLS %s' % {k: out[k] for k in ('C4', 'C7', 'order_invariant', 'id_invariant')})


def g4_cells882(env):
    for cell, r in (('C2', '01'), ('C1', D1_RECEIVER882)):
        out = live_cell882(env, cell, r)
        k = out.get('kept')
        line882('G4', cell, 'R' + r, 'need=%s' % out['need']['decision'],
                'routes=%s' % [a['route']['decision'] for a in out['attempts']], 'kept=%s' % (None if not k else k['opaque']))
        if not k: continue
        g = KEEP882[cell]; att = out['attempts'][k['attempt']]
        rd = readout882(env, cell, r, k['row'], g); g_use = rd.pop('g')
        if g_use is not g:                           # matched readout rebuilt the same cartridge: keep that one, drop the resolver copy
            KEEP882[cell] = g_use; g = None; gc.collect(); torch.cuda.empty_cache()
        STATE882['readout'][cell] = rd
        att['readout'] = {x: rd[x] for x in ('key', 'path', 'gate2', 'VIS', 'C_BLIND', 'pass', 'vis_argmax_differs_from_c_blind')}
        if cell != 'C1':                             # a non-execution cell keeps nothing on the GPU
            decision_log882(att); KEEP882.pop(cell, None); g = g_use = None; gc.collect(); torch.cuda.empty_cache()
        else:
            g = g_use = None                             # D1 reaches its cache through KEEP882 only


# ============================ G9: offline evaluator (after every live decision; nothing flows back) ============================
def offline_evaluate882(env, by_key):
    F = OFFLINE882; omap = STATE882['bank'].get('opaque_to_catalog') or {}
    if not F.get('sealed_sha256'): return None
    def rel(r, cat):
        if cat is None: return None
        b = F['bank'].get(cat)
        if b is None: return 'NEW_CARTRIDGE' if cat == D1RUN882.get('child_id') else None
        return b['world_index'] == F['receivers'][r]['world_index']
    cells = {}
    for cell, L in STATE882['live'].items():
        r = L['receiver']; atts = L['attempts']; first = atts[0]['route'] if atts else {}
        fcat = omap.get(first.get('chosen')) if first.get('chosen') else None
        mounts = [{'retry': a['retry'], 'catalog_id': (a['mount'].get('chain') or [None])[-1], 'outcome': a.get('outcome'),
                   'validation': (a.get('validation') or {}).get('decision')} for a in atts if a.get('mount')]
        for m in mounts: m['relevant'] = rel(r, m['catalog_id'])
        kept = L.get('kept'); kcat = kept['catalog_id'] if kept else None
        cells[cell] = {'receiver': r, 'need': L['need']['decision'] if L.get('need') else None, 'first_route_decision': first.get('decision'),
                       'first_selection_catalog_id': fcat, 'first_selection_relevant': rel(r, fcat),
                       'first_selection_is_diagnostic_only': (L.get('need') or {}).get('decision') != 'USE_MEMORY', 'mounts': mounts,
                       'kept_catalog_id': kcat, 'kept_relevant': rel(r, kcat), 'kept_retry': kept['retry'] if kept else None,
                       'retries': len(L.get('retry_queries') or [])}
    ctrl = STATE882.get('controls') or {}
    c3 = {r: v.get('decision') for r, v in (ctrl.get('C3') or {}).items()}
    c2 = cells.get('C2', {})
    wrong = [(c, m) for c, v in cells.items() for m in v['mounts'] if m['relevant'] is False]
    out = {'cells': cells, 'C3_wrong_only_decisions': c3, 'false_mount_wrong_only': any(d == 'ACCEPT' for d in c3.values()),
           'cross_goal_false_mount': c2.get('kept_relevant') is False or (c2.get('first_route_decision') == 'ACCEPT' and
                                                                          c2.get('first_selection_relevant') is False and
                                                                          not c2.get('first_selection_is_diagnostic_only')),
           'C8_retry': {c: v['retries'] for c, v in cells.items()} if any(v['retries'] for v in cells.values()) else 'NOT_RUN_NO_NATURAL_NO_MATCH_OR_REJECT',
           'C9_wrong_rejection': 'NOT_RUN_NO_NATURAL_WRONG_MOUNT' if not wrong else
           {'wrong_mounts': len(wrong), 'model_rejected': sum(1 for _, m in wrong if m['validation'] == 'REJECT_MEMORY'),
            'detail': [{'cell': c, 'catalog_id': m['catalog_id'], 'validation': m['validation']} for c, m in wrong]},
           'fixture_sha256': F['sealed_sha256']}
    for tag, G in (('d1', STATE882['d1']), ('d2', STATE882['d2'])):
        if G.get('status') != 'EXECUTED': continue
        r = D1_RECEIVER882; spec = by_key[(int(r), 'FORK')]; w = world867(env, spec); kind = {v: k for k, v in w['ids'].items()}
        e = G['environment_effect']; mk = kind.get(e.get('chosen'))
        node = env['node851'](e['path_after'][-1], w) if (e.get('effect') == 'POINTER_ADVANCED' and e.get('path_after')) else None
        out[tag] = {'executor_effect': e.get('effect'), 'card_kind': mk, 'advanced_node_class': node, 'supported': supported882(e.get('effect'), mk, node),
                    'meaning': 'single execution: descriptive, no comparative claim'}
        if tag == 'd1':
            out[tag]['model_observation_class_diagnostic'] = env['node851'](G['model_observation']['hop_text'], w)
            out[tag]['recorded_no_memory_execution'] = STATE882['targets_static']['receivers'][r]
    if STATE882['d2'].get('run'):
        out['d2_selection'] = {'own_cartridge_selected': STATE882['d2'].get('own_cartridge_selected'),
                               'chosen_catalog_id': None if not STATE882['d2'].get('route', {}).get('chosen') else
                               (STATE882['bank'].get('opaque_to_catalog') or {}).get(STATE882['d2']['route']['chosen'])}
    STATE882['offline'] = out
    json_write864('882_offline.json', jsafe878(out))
    return out


# ============================ verdict and report ============================
def summary882():
    off = STATE882.get('offline') or {}; oc = off.get('cells') or {}; L1 = STATE882['live'].get('C1') or {}
    atts = L1.get('attempts') or []; kept = L1.get('kept'); o1 = oc.get('C1') or {}; rd = STATE882['readout'].get('C1') or {}
    d1, d2, ctrl, cal = STATE882['d1'] or {}, STATE882['d2'] or {}, STATE882.get('controls') or {}, STATE882.get('calibration') or {}
    need = (L1.get('need') or {}).get('decision')
    blocks = list(STATE882['blocks'])
    if 'pass' not in cal and STATE882['status'] != 'COMPLETE': blocks.append('NOT_RUN_BEFORE_G3_COMPLETE')
    c1 = {'need': need, 'kept': bool(kept), 'mounted_any': any(a.get('mount') for a in atts), 'kept_relevant': o1.get('kept_relevant') is True,
          'first_selection_accepted': bool(atts) and atts[0]['route']['decision'] == 'ACCEPT' and need == 'USE_MEMORY',
          'first_selection_relevant': o1.get('first_selection_relevant') is True, 'kept_after_retry': bool(kept) and kept['retry'] > 0,
          'retry_label': None if not kept or kept['retry'] == 0 else ('RETRY_ACCEPTED_AFTER_MODEL_REJECT' if 'MODEL_REJECT_RESTORED' in kept['after']
                                                                      else 'RETRY_ACCEPTED_AFTER_FIRST_NO_MATCH'),
          'readout_pass': bool(rd.get('pass')), 'vis_argmax_differs_from_c_blind': bool(rd.get('vis_argmax_differs_from_c_blind'))}
    st = d1.get('store') or {}
    d1s = {'executed': d1.get('status') == 'EXECUTED', 'executed_equals_vis': (d1.get('checks') or {}).get('executed_equals_VIS_action') is True,
           'supported': (off.get('d1') or {}).get('supported') is True, 'store': st.get('decision'), 'written': bool(st.get('written'))}
    d2s = {k: d2.get(k) for k in ('run', 'own_cartridge_selected', 'parent_seal_equal', 'mount_pass', 'readout_pass', 'vis_exact',
                                  'executed_equals_vis', 'vis_action', 'no_memory_action')}
    return {'blocks': blocks, 'g3_pass': cal.get('pass') is True, 'c1': c1, 'd1': d1s, 'd2': d2s,
            'controls_did_not_bite': list(cal.get('controls_did_not_bite') or []) + list(ctrl.get('controls_did_not_bite') or []),
            'controls_pass': ctrl.get('pass') is True, 'false_mount_wrong_only': off.get('false_mount_wrong_only') is True,
            'cross_goal_false_mount': off.get('cross_goal_false_mount') is True, 'empty_safe': ctrl.get('empty_safe') is True,
            'tie_safe': ctrl.get('tie_safe') is True}


def verdict882():
    s = summary882(); v = verdict_logic882(s)
    v.update({'blocks': s['blocks'], 'not_run': list(STATE882['not_run']), 'limits': PREREG882['limits'], 'summary': s,
              'gpu': 'GPU_NOT_RUN_BY_AUTHOR (this file); a run of it is the only GPU evidence'})
    STATE882['verdict'] = v
    return v


def report882():
    W = [w for w, _ in ACTION_IDS867] if 'ACTION_IDS867' in globals() else []
    print('=' * 112)
    print('TEST882 | GPU %s | head %s | cell %s | prereg %s' % (CC_GPU.get('name'), HEAD882[:12],
          STATE882['source'].get('executed_cell_git_blob'), PREREG_SHA882[:16]))
    print('SELFTESTS %s' % _j882.dumps({k: (all(x is True for kk, x in v.items() if not kk.startswith(('roundtrip_rel', 'wrong_position_rel')))
                                            if isinstance(v, dict) and 'error' not in v else v) for k, v in STATE882['selftests'].items()
                                        if not k.endswith('_detail')}, sort_keys=True, default=str))
    A = STATE882.get('address') or {}
    print('G2 ADDRESS %s domain=%s' % (_j882.dumps(A.get('G2'), sort_keys=True), str(A.get('domain'))[:16]))
    C = STATE882.get('calibration') or {}
    if C:
        print('G3 CALIBRATION tau_neg=%s delta_tie=%s final_pos=%s loo_correct=%s loo_false=%s separation=%s pass=%s controls=%s' % (
            C.get('tau_neg'), C.get('delta_tie'), C.get('final_positive_accepted'), C.get('loo_correct'), C.get('loo_false_mounts'),
            C.get('separation_min_pos_minus_max_neg'), C.get('pass'), _j882.dumps(C.get('controls'), sort_keys=True)))
        for w, row in (C.get('S') or {}).items():
            print('    Q%s %s null=%.5f' % (w, ' '.join('K%s=%.5f' % (v, s_) for v, s_ in sorted(row.items())), C['null'][w]))
    for r, R in STATE882['receivers'].items():
        print('RECEIVER R%s %s memory=%s X=%s NO_MEMORY=%s' % (r, R['item'], R['memory_tokens'], R['X_len'], _j882.dumps(R['no_memory_CAR'], default=str)))
    for cell, L in STATE882['live'].items():
        n = L.get('need') or {}
        print('LIVE %s R%s need=%s mass=%.4f normalized=%s' % (cell, L['receiver'], n.get('decision'), n.get('mass') or 0.0,
              _j882.dumps({k: round(v, 4) for k, v in (n.get('normalized') or {}).items()})))
        for a in L['attempts']:
            rt = a['route']
            print('    retry=%d route=%s chosen=%s top3=%s null=%s margin=%s reasons=%s outcome=%s validation=%s' % (
                a['retry'], rt['decision'], rt['chosen'], _j882.dumps(rt['top3']), rt['null'], rt['margin'], rt['reasons'],
                a.get('outcome'), (a.get('validation') or {}).get('decision')))
    print('CONTROLS %s' % _j882.dumps({k: v for k, v in (STATE882.get('controls') or {}).items() if k != 'base'}, sort_keys=True, default=str)[:3000])
    for cell, rd in STATE882['readout'].items():
        print('READOUT %s %s path=%s pass=%s VIS=%s C_BLIND=%s' % (cell, rd['key'], rd['path'], rd['pass'], _j882.dumps(rd['VIS'], default=str),
                                                                  _j882.dumps(rd['C_BLIND'], default=str)))
    print('D1 %s' % _j882.dumps(jsafe878(STATE882.get('d1') or {}), sort_keys=True)[:3500])
    print('D2 %s' % _j882.dumps(jsafe878(STATE882.get('d2') or {}), sort_keys=True)[:2500])
    print('OFFLINE %s' % _j882.dumps(jsafe878(STATE882.get('offline') or {}), sort_keys=True)[:2500])
    b = STATE882['budget']
    print('BUDGET ADAPTER_FFE_LOWER_BOUND=%.1f/%.0f by_kind=%s TOTAL_GPU_WORK_NOT_FULLY_ACCOUNTED calls849=%s ssd_bytes=%d '
          'peak_alloc=%.2f GiB peak_reserved=%.2f GiB' % (b['adapter_ffe_lower_bound'], FFE_MAX882,
          _j882.dumps({k: round(v, 2) for k, v in b['ffe_by_kind'].items()}, sort_keys=True),
          env882['CALLS849'] if 'env882' in globals() else None, b['ssd_bytes'], b['peak_alloc_gib'], b['peak_reserved_gib']))
    v = STATE882['verdict'] or {}
    print('TEST882 VERDICT %s | labels %s | mechanical_go %s | semantic_go %s | blocks %s | not_run %s' % (
        v.get('verdict'), v.get('labels'), v.get('mechanical_go'), v.get('semantic_go'), v.get('blocks'), v.get('not_run')))
    print('LIMITS: %s' % '; '.join(PREREG882['limits']))
    print('status %s | wall %.0f s | GPU_NOT_RUN_BY_AUTHOR (cell author); this console is the run record' % (
        STATE882['status'], time.perf_counter() - T_START882))
    print('=' * 112)


# ============================ single cell execution ============================
FIXTURE882 = {}
NULL_KEY882, PEAK882, TOKIDS882 = [None], [None], [None]
T_START878 = T_START882 = time.perf_counter()
try:
    STATE882['status'] = 'G0_SOURCE'; capture_source882()
    json_write864('882_prereg.json', {'prereg': PREREG882, 'sha256': PREREG_SHA882, 'before_model_load': True})
    line882('G0 PREREG', PREREG_SHA882, 'cell', STATE882['source']['executed_cell_git_blob'])
    load_sources865(); log879 = select_locked882()
    STATE882['status'] = 'G0_CPU_SELFTESTS'; run_selftests882()
    line882('G0 CPU SELFTESTS PASS', _j882.dumps(sorted(k for k in STATE882['selftests'] if not k.endswith('_detail'))))
    du = _s882.disk_usage(str(ROOT864)); STATE882['budget']['disk_free_gib'] = round(du.free / 2**30, 1)
    if du.free / 2**30 < DISK_MIN_GIB882: raise Gate882('DISK_FREE %.1f GiB' % (du.free / 2**30))
    source_audit878(); load878(); STATE882['ref873'] = ref873_874(RAW_SOURCES864['873.log'].decode())
    feasibility_audit864(); audit_contracts865(); load_spine864(); REFS882 = load_records870()
    STATE882['targets_static'] = targets882(REFS882)
    ctl882 = lambda s_: [e for e in REFS882[(s_, ARM878)]['events'] if e['type'] == 'CONTROL']
    STATIC_T2_SHA878 = {s_: ctl882(s_)[PRE_STEP878 - 1]['record']['state_sha256'] for s_ in SOURCES878}
    STATIC_T2_SHA882 = {s_: ctl882(s_)[PRE_STEP878 - 1]['record']['state_sha256'] for s_ in EXTRA882}
    line882('G0 SOURCE PASS', _j882.dumps({k: v for k, v in STATE882['source'].items() if k != 'reused'}, sort_keys=True))
    STATE882['status'] = 'G0_PREFLIGHT'
    assert CC_GPU_OK and 'A100' in str(CC_GPU.get('name')) and CC_GPU.get('total_gib', 0) >= 78.0, ('A100_80GB_REQUIRED', CC_GPU)
    env882, original_error882, original_trace882, reproduction882 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace882; TWO_JOB_VERIFICATION864 = verify_two_job859(env882, original_trace882)
    assert_hook_free859(env882, 'T882_before_native'); install_offline_evaluator859(env882)
    native882 = native_sequences860(env882); NATIVE_REGRESSION864 = native_regression864(env882, native882)
    verify_864_reference865(NATIVE_REGRESSION864); ANALYSIS864 = run_analysis863(env882, native882)
    assert len(STATE863['restores']) == 3 and all(r_['exact'] for r_ in STATE863['restores'])
    digest882 = records_digest861(env882); null_seal882 = physical_seal863(env882, env882['MEMNULL841'])
    STATE882['memnull_seal'] = null_seal882           # own key: the locked api877 replaces STATE['api']
    runtime_contracts865(env882); runtime_preflight865(env882, reproduction882); rearm_budget865(env882); make_slots866(env882)
    SLOTS867['PREV_EVALUATION'] = list(env882['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env882); resolve_append873(env882); api877(env882); WEIGHTS0_878 = weights_digest877(env882)
    chunk882 = [ns['CHUNK'] for ns in (env882['build_fusion'].__globals__, env882) if 'CHUNK' in ns]
    assert chunk882 and int(chunk882[0]) > 0 and all(k in env882 for k in (
        'P', 'to_gpu', 'kv_digest', 'entries', 'make_x851', 'gen851', 'gen849', 'C_SLOT851', 'E_SLOT851', 'EVIDENCE851',
        'ANSWER_SUFFIX851', 'REVIEW_SUFFIX851', 'stats849', 'peak50_841', 'unit841', 'MUE845', 'MEMNULL841', 'IDXPRE841',
        'IDXPOST841', 'index_embeds841', 'relation852', 'R_SLOT852', 'node851')), 'ENGINE_NAMESPACE'
    EXP878['CHUNK'] = int(chunk882[0])
    PEAK882[0] = env882['peak50_841']; TOKIDS882[0] = lambda t_: list(env882['tok'](t_, add_special_tokens=False).input_ids)
    REAL_DIR882 = ROOT864 / 'REAL_NAMESPACE_882'; BANK_DATA882 = REAL_DIR882 / 'bank'
    DIAG_DIR882 = ROOT864 / 'DIAG_NAMESPACE_882'; DIAG_DATA882 = DIAG_DIR882 / 'matched'
    for d_ in (BANK_DATA882, DIAG_DATA882): d_.mkdir(parents=True, exist_ok=False)
    EXP_DIR878 = BANK_DATA882
    STORE_BANK882 = RealStore882(REAL_DIR882, [BANK_DATA882]); STORE_DIAG882 = RealStore881(DIAG_DIR882, [DIAG_DATA882])
    SLOTS881 = {k: TOKIDS882[0](v) for k, v in SLOT_TEXT881.items()}
    WORDS880 = [(w_, TOKIDS882[0](' ' + w_)) for w_ in ('STORE', 'DISCARD')]
    NEED_IDS882 = [(w_, TOKIDS882[0](' ' + w_)) for w_ in NEED_WORDS882]
    VALID_IDS882 = [(w_, TOKIDS882[0](' ' + w_)) for w_ in VALID_WORDS882]
    NEED_SUFFIX_IDS882, VALID_SUFFIX_IDS882 = TOKIDS882[0](NEED_SUFFIX882), TOKIDS882[0](VALID_SUFFIX882)
    for ws_ in (WORDS880, NEED_IDS882, VALID_IDS882):
        assert all(ids_ for _, ids_ in ws_) and len({ids_[0] for _, ids_ in ws_}) == len(ws_), ('WORD_FIRST_TOKENS', ws_)
    assert all(SLOTS881.values()) and NEED_SUFFIX_IDS882 and VALID_SUFFIX_IDS882, 'EMPTY_SLOT_TOKENS'
    STATE882['tokens'] = {'actions': {w_: ids_ for w_, ids_ in ACTION_IDS867}, 'store': dict(WORDS880), 'need': dict(NEED_IDS882),
                          'validation': dict(VALID_IDS882), 'sha256': sha256_bytes864(_j882.dumps([ACTION_IDS867, WORDS880, NEED_IDS882,
                                                                                                   VALID_IDS882], sort_keys=True).encode())}
    assert not any(p_.requires_grad for p_ in env882['model'].parameters()), 'NOT_FROZEN'
    assert_hook_free859(env882, 'T882_before_points')
    line882('G0 PREFLIGHT PASS', _j882.dumps(STATE882['api'], sort_keys=True, default=str)[:600],
            'CHUNK=%d P=%d' % (EXP878['CHUNK'], int(env882['P'])), 'model_load_s=%.0f' % (time.perf_counter() - T_START882))
    STATE882['status'] = 'G1_PHYSICAL'; T0_865 = time.perf_counter(); by_key882 = build_specs869(env882)
    g1_replays882(env882, by_key882, REFS882); g1_physical882(env882)
    json_write864('882_experience_manifest.json', jsafe878(STATE882['experience']))
    STATE882['status'] = 'G2_ADDRESS'; g2_address882(env882)
    STATE882['offline_fixture_sha256'] = fixture_seal882(env882, by_key882, REFS882)
    STATE882['store']['recovery_after_G2'] = STORE_BANK882.recover(lambda e: load_exp878(env882, e) and None)
    STATE882['status'] = 'G3_CALIBRATION'; g3_calibrate882(env882)
    STATE882['status'] = 'G4_LIVE'; receivers882(env882); g4_queries882(env882); g4_controls882(env882); g4_cells882(env882)
    if STATE882['live'].get('C1', {}).get('kept'):
        STATE882['status'] = 'G6_G7_D1'
        att882 = STATE882['live']['C1']['attempts'][STATE882['live']['C1']['kept']['attempt']]
        try:
            d1_882(env882, 'C1')
        finally:
            D = STATE882['d1']
            att882['execution'] = {'status': D.get('status'), 'action': D.get('vis_action'),
                                   'effect': (D.get('environment_effect') or {}).get('effect'), 'checks': D.get('checks'),
                                   'model_observation': D.get('model_observation')}
            att882['store'] = D.get('store'); decision_log882(att882)
        if (STATE882['d1'].get('store') or {}).get('written'):
            STATE882['status'] = 'G8_D2'; d2_882(env882)
        else:
            STATE882['d2'] = {'run': False, 'status': 'SELF_REUSE_NOT_RUN', 'why': 'NO_NEW_CARTRIDGE_WRITTEN_IN_D1'}
    else:
        STATE882['d1'] = dict(d1_skeleton882(), status='NOT_RUN', why='NO_ACCEPTED_KEPT_MEMORY_IN_C1')
        STATE882['d2'] = {'run': False, 'status': 'SELF_REUSE_NOT_RUN', 'why': 'NO_D1_EXECUTION'}
    KEEP882.clear(); G881.clear(); D1RUN882.clear(); gc.collect(); torch.cuda.empty_cache()
    STATE882['status'] = 'G9_OFFLINE'; offline_evaluate882(env882, by_key882)
    STATE882['store']['recovery_final'] = STORE_BANK882.recover(lambda e: load_exp878(env882, e) and None)
    hook882 = hook_audit859(env882, 'T882_final')
    if records_digest861(env882) != digest882 or physical_seal863(env882, env882['MEMNULL841']) != null_seal882 or \
            hook882['hook_count'] or hook882['transformers_output_capturing_installed'] or weights_digest877(env882) != WEIGHTS0_878:
        STATE882['blocks'].append('POST_RUN_INTEGRITY')
    for r882 in RECEIVERS882:
        if full_seal881(TGT878[('FORK', r882)]['m'])['all'] != STATE882['receivers'][r882]['B_full_seal']:
            STATE882['blocks'].append('RECEIVER_B_FINAL_SEAL R' + r882)
    STATE882['status'] = 'COMPLETE'; verdict882()
except Revise882 as exc:
    STATE882['error'] = str(exc); STATE882['calibration'].setdefault('pass', False)
    STATE882['not_run'].append('LIVE_CELLS_NOT_RUN: REVISE_ADDRESS_DOMAIN (%s)' % exc)
    STATE882['status'] = 'REVISE_AT_' + str(STATE882['status']); verdict882()
except (Budget882, Partial878) as exc:
    STATE882['error'] = str(exc); STATE882['not_run'].append('NOT_RUN_AT_%s: %s' % (STATE882['status'], exc))
    STATE882['status'] = 'NOT_RUN_AT_' + str(STATE882['status'])
    try:
        KEEP882.clear(); G881.clear(); D1RUN882.clear(); gc.collect(); torch.cuda.empty_cache()
        if 'by_key882' in globals() and OFFLINE882.get('sealed_sha256'): offline_evaluate882(env882, by_key882)
    except Exception as exc2: STATE882['not_run'].append('OFFLINE_AFTER_BUDGET_STOP_FAILED: %s' % exc2)
    verdict882()
except BaseException as exc:
    STATE882['error'] = '%s: %s' % (type(exc).__name__, exc); STATE882['traceback'] = traceback.format_exc()
    STATE882['blocks'].append('%s: %s' % (STATE882['status'], STATE882['error'][:300]))
    STATE882['status'] = 'FAILED_AT_' + str(STATE882['status'])
    try: verdict882()
    except Exception: STATE882['verdict'] = {'verdict': 'TECHNICAL_BLOCK', 'labels': [], 'blocks': list(STATE882['blocks'])}
    (ROOT864 / '882_traceback.txt').write_text(STATE882['traceback'], encoding='utf-8')
    print('TEST882 ERROR', STATE882['error'][:300], '| full traceback:', ROOT864 / '882_traceback.txt', file=ERROR_CONSOLE864, flush=True)
    print(STATE882['traceback'], file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        json_write864('882_traces.json', TRACES881)
        json_write864('882_result.json', jsafe878(dict(STATE882, replays=STATE870['replays'], prereg=PREREG882)) if 'jsafe878' in globals()
                      else json.loads(json.dumps(dict(STATE882, replays=STATE870['replays']), default=str)))
    except Exception as exc: print('RESULT_WRITE_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    try: report882()
    except Exception as exc: print('REPORT_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE882['suffix'], 'test870.py:suffix', 'exec'), globals())
