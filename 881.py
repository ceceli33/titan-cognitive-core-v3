# AKBASCORE SILICON HIPPOCAMPUS — TEST881 — PILOT-0 r2: PHYSICAL C VISIBILITY -> SAME VIS POLICY -> LITERAL ACTION -> REAL STATE
# One A100-SXM4-80GB Colab cell. Frozen Qwen2.5-72B-Instruct NF4, BF16. Locked engine test870.py (e322ed8) + locked 878.py,
# 880.py (store reader only); dependencies from the pinned commit 6bd3c52bf60eea2d4b5a9b5c72d871bae24e3c10, every file blob-locked.
# r2 of 881.py blob 0215da1c (audit fixes): GATE4 executes the action of a fresh recomputation of the SAME masked VIS policy
# (exact equality with the GATE3 VIS reading is required, else nothing is executed); C_BLIND invariance M == L on X and on
# every teacher-forced continuation token (80-layer K/V, hidden, token logps) in all four cells; masked-path and native
# labels separated; executor state separated from model-generated observation; parent-conditioned REAL cartridge with
# reload/append/read parity; crash-safe append-only catalog with recovery and idempotency (CPU fault injection before the
# model is loaded); adapter FFE reported as a lower bound; GATE2+GATE3 fused per cell; full 80-layer seals.
# Layout of every mounted arm: [receiver memory B][E = X2 A C][receiver X]; each arm builds its own cache from immutable
# B+E tensors and computes X and every CAR continuation from layer 0 under its own 2-D visibility mask.
# Never: weight writes, training, hooks, output_hidden_states/attentions, logit edits, action forcing, text replay, outcome
# oracle at runtime, synthetic C in the REAL namespace. Labels (card kinds, node classes) are read only offline.
import ast as _a881, hashlib as _h881, json as _j881, os as _o881, re as _r881, shutil as _s881, tempfile as _tf881
import urllib.request as _u881
ENGINE_URL881 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB881, MARKER881 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', 'AKBASCORE SILICON HIPPOCAMPUS — TEST881 — PILOT-0 r2'
HEAD881, R1_BLOB881 = '6bd3c52bf60eea2d4b5a9b5c72d871bae24e3c10', '0215da1caf48710172bdf968e3ea679a29dfc1af'

def blob881(raw):
    return _h881.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()

def engine_parts881():
    with _u881.urlopen(_u881.Request(ENGINE_URL881, headers={'User-Agent': 'AKBASCORE-TEST881'}), timeout=240) as r:
        raw = r.read()
    assert blob881(raw) == ENGINE_BLOB881, ('ENGINE_BLOB_MISMATCH', blob881(raw))
    text = raw.decode('utf-8'); _a881.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST881_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST881_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST881_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('881_engine.log', '881_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST881_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '881_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '881_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST881_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old)
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL881, 'git_blob': blob881(raw), 'sha256': _h881.sha256(raw).hexdigest()}

try:
    ENGINE881, ENGINE_INFO881 = engine_parts881()
except BaseException as _exc881:      # console capture starts inside the engine prefix: keep a local record of this failure
    import time as _t881, traceback as _tb881
    _p881 = '/content/TEST881_PRE_ENGINE_ERROR_%s.txt' % _t881.strftime('%Y%m%dT%H%M%SZ', _t881.gmtime())
    try:
        with open(_p881, 'w', encoding='utf-8') as _f881: _f881.write(_tb881.format_exc())
    except OSError: _p881 = 'NOT_WRITTEN'
    print('TEST881 PRE-ENGINE ERROR (before console capture):', type(_exc881).__name__, _exc881, '| traceback:', _p881)
    raise
exec(compile(ENGINE881['prefix'], 'test870.py:prefix', 'exec'), globals())
exec(compile(ENGINE881['body'], 'test870.py:engine', 'exec'), globals())
print('TEST881 ENGINE', _j881.dumps(ENGINE_INFO881, sort_keys=True))

# ============================ locks, pinned repository, reused code ============================
CODELOAD864 = 'https://codeload.github.com/ceceli33/titan-cognitive-core-v3/zip/' + HEAD881   # pinned commit, never main
LOCKS864.update({'test870.py': ENGINE_BLOB881, 'Test870.log': 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc',
                 '873.py': '2e44affa5e0dd462155fb265c331270fb8e7b7e1', '873.log': '1c9eb9fca173003eaf45bc7726af13c2817324b7',
                 '874.py': '12172001ba3696ad91087a8b34d7995728259e47', '874.log': '1229e3b70440e3887ccf1bd7e3bad51f900f5313',
                 '877.py': 'a6aa7648e0fb765a8dc9b56b8f79b4dcef5fc772', '877.log': 'c4eb58021ed827fb13d5c15fee7c18541f6d4604',
                 '878.py': '7842e8675544a0328e3552f059c81b7750068a82', 'Test_878_log2.log': '2bfc7adc2a8f718c012a6d722a9e0a04a72cbedd',
                 '879.py': '92f9eb665173986b6c98b42f07eefb3249c861d4', '879.log': 'c1205bc082fb69c68b9f9f4e290808a0dec71fa8',
                 '880.py': '3e6aab5d79af8f75053b0da873d70779406adb74', '880.log': 'adcc0389b359b1dd254887edb1786fd5edff378a'})
REQUIRED_LOCKS881 = {'757.py': '3d88bf8638390995858f23391f1e043faa586835', '841.py': '135b18e5b1ea113579c607cf9eecf49628cf18c2',
                     '851.py': '0f01e73b9ad160c988cfe059e8b5ae5e1f35f65b'}
TEST878_PREREG881 = '0555ab01d436c0df7e8e1be21aea3170ac0a50d799a528796212298a48dc4103'
_a878, _h878, _j878 = _a881, _h881, _j881
ENGINE_BLOB878 = ENGINE_BLOB881
CONSTS878 = ('TEST877_CELL_BLOB878', 'TEST877_PREREG_DEPS878', 'TEST870_MINUTES', 'WORLDS878', 'SOURCES878', 'FORKS878',
             'SIDES874', '_h877', 'ARM878', 'FUNCS873', 'FUNCS874', 'FUNCS877', 'ROPE_TOL878', 'HARD_MIN878', 'PREREG878')
FUNCS878 = ('Partial878', 'Persist878', 'line878', 'source_audit878', 'load878', 'guard878', 'xspan878', 'next_kv878',
            'tsha878', 'write_exp878', 'load_exp878', 'append_exp878', 'xappend878', 'xcar878', 'arm878', 'jsafe878',
            'dif878', 'pa878', 'sig878', 'persist878', 'probe878')
FUNCS880 = ('store_words880',)
BANNED881 = {'register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook', 'output_hidden_states',
             'output_attentions', 'install_all_output_capturing_hooks', 'backward', 'requires_grad_', 'step', 'zero_grad',
             'execute866', 'mount865', 'free865', 'hop865', 'DirectCut3', 'native_append_direct'}
EXEC_ALLOW881 = ('execute866', 'hop865')                    # gate4_881 only: the one real action through the locked executor
ORACLE881 = {'supported851', 'node851', 'world867', 'correct867', 'success867', 'FIXTURE881', 'OFFLINE867', 'worlds829'}
RUNTIME881 = ('make_single_episode_layout881', 'xread881', 'nread881', 'xtrace881', 'zero_slot881', 'cell881',
              'gate4_881', 'store_reading881', 'parent_reuse881', 'full_seal881', 'tsha881')
CELLS881 = (('00', '00'), ('01', '01'), ('01', '00'), ('00', '01'))   # (source world, receiver world); same goal first
EXEC_CELL881, EXEC_COND881 = ('00', '00'), 'LIVE'          # GATE4: the one real execution (fixed before the model is loaded)
WALL_MIN881, PEAK_GIB881, FFE_MAX881, FREE_MIN_GIB881, DISK_MIN_GIB881 = 45.0, 60.0, 120.0, 8.0, 5.0
STORE_PROMPT881 = ('Question: {q}\nThe numerical context contains the action you executed and the candidate and the independent '
                   'answer actually observed after it. Decide whether this action and its real consequence should be kept as a '
                   'physical experience for future decisions. Reply with exactly one word: STORE or DISCARD.')
SLOT_TEXT881 = {'ACTED': 'Executed action numerical state:', 'STORE_SUFFIX': '\nMemory decision:'}
STAGES881 = ('TMP_WRITTEN', 'FILE_RENAMED', 'FILE_FSYNC', 'SIDECAR', 'DIR_FSYNC', 'VERIFIED_RELOAD', 'CATALOG_APPEND',
             'CATALOG_FSYNC', 'CATALOG_DIR_FSYNC', 'COMMITTED')
PREREG881 = {
    'revision': 'r2 of 881.py blob %s' % R1_BLOB881,
    'question': 'does the physically readable real consequence C of one CUT3 experience move the CAR of an independent receiver '
                'in a C-specific, goal-consistent way against a same-layout same-kernel C_BLIND arm; is that same masked VIS '
                'policy then executed literally in the real environment; is a STORE written as a parent-conditioned cartridge',
    'repository': {'head': HEAD881, 'archive': 'codeload zip of the pinned commit; every file git-blob locked'},
    'experiences': {'S00': ['I867_00_MISSING', 'I867_00_LIVE'], 'S01': ['I867_01_MISSING', 'I867_01_LIVE'],
                    'how': 'exact replay of the locked 869 records (a new native run compared with the record at every step; '
                           'no recorded action is ever forced), written by the locked write_exp878, source working state '
                           'freed, reloaded with file + per-tensor SHA-256',
                    'pair': 'MISSING and LIVE share X2 and A bitwise and differ in the real mounted card C (same length)'},
    'receivers': {'R00': 'I867_00_FORK step 1', 'R01': 'I867_01_FORK step 1'},
    'cells': ['%s>%s' % c for c in CELLS881],
    'contract': {'positions': 'B [0,n0), E [n0,n0+q) with X2,A,C in this order (C last: no E row was computed from C), '
                              'X [n0+q, n0+q+L); identical for MISSING and LIVE; OFF_0 has X at [n0, n0+L)',
                 'cartridge': 'H3 + layer 0-3 K/V; lower K re-phased once from P+j to n0+j; V unchanged; layers 4-79 re-computed '
                              'by the locked native append on B (no X row exists then)',
                 'mask': '2-D long mask over [cache][rows], 1 = readable; hidden columns zeroed for X and every continuation '
                         'row of the read; VIS additionally re-opens C inside the built 4-D mask (xspan878 restore)',
                 'continuation': 'each candidate word from a cache cropped back to [B][E][X]; the same 2-D mask per forward'},
    'arms': {'VIS': 'xcar878(blind=C, sham=True): masked kernel, C readable',
             'C_BLIND': 'xtrace881 = xcar878 procedure + K/V/hidden digests (C hidden); checked equal to locked xcar878',
             'EPISODE_OFF': 'blind = E', 'OFF_G_ZERO': 'E rows zero, blind = E', 'OFF_0': 'receiver alone (position control)',
             'FULL_EXPLICIT': 'xcar878(blind=()) (no mask zero)', 'NATIVE_FULL': 'decide874(ranges=[])',
             'NATIVE_C_BLIND': 'decide874(ranges=[C], rows)', 'VIS_REPEAT': 'VIS again',
             'WRONG': 'cross cells: real experience of the other world (other goal)',
             'SHADOW_C_SWAP': 'NOT_RUN by design (the real MISSING/LIVE pair supplies two real C under the same X2/A)'},
    'gate2_per_cell': ['pre-C E rows K and V bitwise M == L, 80 layers', 'C rows: K and V differences reported separately',
                       'C_BLIND M == L: token logps, action, argmax, mass; X K/V 80 layers, X final hidden, every continuation '
                       'token K/V 80 layers + hidden + logp (all four cells)', 'xtrace881 reading == locked xcar878 reading',
                       'native C_BLIND rows M == L (all four cells)', 'same goal: EPISODE_OFF M == L == OFF_G_ZERO; '
                       'FULL_EXPLICIT == NATIVE_FULL', 'receiver B full 80-layer seal unchanged', 'finite'],
    'estimands': {'delta_C(x,a)': 'logp VIS_x(a) - logp C_BLIND_x(a)', 'T(a)': 'delta_C(LIVE,a) - delta_C(MISSING,a)',
                  'generic(a)': 'C_BLIND - EPISODE_OFF', 'slot(a)': 'EPISODE_OFF - OFF_0', 'kernel(a)': 'VIS_M - FULL_EXPLICIT_M',
                  'repeat(a)': 'VIS_M - VIS_REPEAT_M', 'floor': 'per receiver max(5e-5, max|repeat|, max|kernel|)',
                  'norm': 'max over the 6 CAR words of sequence logp'},
    'labels': {'MASKED_PATH_C_SPECIFIC_SIGNAL': 'both same-goal cells: fixture valid, max|T| > floor, T(ACQUIRE) < -floor, '
                                                'max|T| > max|T| of the cross cell into the same receiver (narrow, unchanged)',
               'MASKED_PATH_ARGMAX_CHANGE': 'same-goal cell: argmax_word(VIS_x) != argmax_word(C_BLIND)',
               'MASKED_PATH_EXECUTABLE_ACTION_CHANGE': 'same-goal cell: executable action (abstention applied) differs, both valid',
               'ABSTAIN_CHANGE': 'same-goal cell: abstention status differs',
               'NATIVE_UNMASKED_POLICY_CHANGE': 'signal and argmax(NATIVE_FULL_x) != argmax(NATIVE_C_BLIND) and '
                                                'argmax(NATIVE_FULL_x) == argmax(VIS_x) (masked and native agree)',
               'MASKED_ONLY': 'masked change without the native agreement', 'PATH_PARITY_WEAK': 'max|kernel| >= max|T|',
               'EXPLORATORY': 'actions other than ACQUIRE with |T| > floor (never a pass condition)',
               'TECHNICAL_BLOCK / PREREG_SEMANTIC_FAIL / NOT_RUN_AT_<stage>': 'as named'},
    'gate4': {'cell': '%s>%s' % EXEC_CELL881, 'experience': EXEC_COND881,
              'policy_path': 'VIS_MASKED_XCAR878 recomputed on the same B+E tensors; must equal the GATE3 VIS reading exactly '
                             '(token logps, action, argmax, mass) or nothing is executed (TECHNICAL_BLOCK)',
              'diagnostic': 'NATIVE_FULL (car873 on [B][E][X]) per-action delta to VIS',
              'auxiliary_control_path': 'NATIVE_FULL_AUXILIARY: gen851 control rows on B+E (direction866 input)',
              'candidate_path': 'the receiver hop on B (the observation that preceded the decision), rows SHA == record',
              'write_cache_path': 'PARENT_CONDITIONED_NATIVE_WRITE: [B][E][X2][A][C] native unmasked timeline',
              'claim': 'VIS_SELECTED_ACTION_WITH_NATIVE_AUXILIARY; no pure-VIS end-to-end claim; no VIS > BLIND outcome claim',
              'terminal': 'ACCEPT/STOP/INVALID -> TERMINAL_NO_ENV_TRANSITION, WRITE_NOT_RUN',
              'environment_consequence': 'execute866 ctx/effect transition (mounted set, path)',
              'model_observation': 'post-action hop865 / gen849 rows = MODEL_OBSERVATION / MODEL_EVIDENCE (never an outcome label)',
              'outcome_rule_offline': 'BEHAVIORAL_OUTCOME iff executor state: MOUNTED card of kind second, or UNMOUNTED card of kind '
                                      'fork/decoy, or POINTER_ADVANCED onto a path node of class middle',
              'store': 'two-word STORE/DISCARD reading (locked store_words880 procedure) with STORE_PROMPT881 on the post-action '
                       'environment memory; REAL write only on STORE', 'store_prompt': STORE_PROMPT881,
              'cartridge': 'requires_parent = true; PARENT_CONDITIONED_REUSE = locked persist878 on a fresh rebuild of [B][parent]; '
                           'STANDALONE_DRIFT = [B][new] read, diagnostic only'},
    'persistence': {'stages': list(STAGES881), 'recovery': 'catalog tail repair, dangling pointer = INTEGRITY_BLOCK, orphan with '
                    'valid sidecar re-catalogued, orphan without = quarantine (unique names, never overwritten, never deleted)',
                    'idempotency': 'same id + same SHA = no-op; same id + other SHA = INTEGRITY_BLOCK', 'generation': 'max + 1'},
    'informed_by': '879.log already showed, natively, larger ACQUIRE suppression with the LIVE C than with the MISSING C in both '
                   'same-goal cells: confirmation with path-matched arms, not a blind prediction',
    'budgets': {'wall_min': WALL_MIN881, 'peak_gib': PEAK_GIB881, 'adapter_ffe_lower_bound_max': FFE_MAX881,
                'note': 'ADAPTER_FFE_LOWER_BOUND counts TEST881 adapter forwards only; replay/preflight/generation work is '
                        'TOTAL_GPU_WORK_NOT_FULLY_ACCOUNTED (CALLS849 reported)'},
    'never_reported_here': ['NATURAL_ADDRESSING', 'SF_PARITY', 'QCEP_SUCCESS', 'CLOSED_LOOP_SELF_REUSE'],
    'limits': ['two worlds, four cells, one executed action: a pilot, not a statistic', 'forced mount: no retrieval',
               'a single execution supports no comparative behavioural claim']}
PREREG_SHA881 = sha256_bytes864(_j881.dumps(PREREG881, sort_keys=True).encode())
STATE881 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO881, 'prereg_sha256': PREREG_SHA881, 'source': {}, 'api': {},
            'selftests': {}, 'ref873': {}, 'targets_static': {}, 'sides': {}, 'experience': {}, 'sources': {}, 'fixtures': {},
            'receivers': {}, 'cells': {}, 'measure': {}, 'gate4': {}, 'store': {},
            'budget': {'adapter_ffe_lower_bound': 0.0, 'total_gpu_work_not_fully_accounted': True, 'ssd_bytes': 0,
                       'peak_alloc_gib': 0.0, 'peak_reserved_gib': 0.0, 'arms': {}},
            'not_run': [], 'blocks': [], 'verdict': None, 'error': None}
STATE878 = STATE877 = STATE881                             # the selected 877/878 functions write here
T2_KEEP878, SRC878, TGT878, EXP878, EXEC881, G881, ARMS881, TRACES881 = {}, {}, {}, {}, {}, {}, {}, {}

class Gate881(Exception):
    pass

class Budget881(Exception):
    pass

class IntegrityBlock881(Exception):
    pass

class CommitUncertain881(Exception):
    pass

class Partial878(Exception):                                   # placeholder; replaced by the locked TEST878 class at selection
    pass

def line881(*parts): short864('T881', *parts)

# ============================ firewall (calls, aliases, getattr strings) ============================
def scan881(node, allow=()):
    used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in _a881.walk(node) if isinstance(c, _a881.Call)}
    used |= {k.arg for k in _a881.walk(node) if isinstance(k, _a881.keyword)}
    used |= {s.slice.value for s in _a881.walk(node) if isinstance(s, _a881.Subscript) and
             isinstance(s.slice, _a881.Constant)} & {'native_append_direct', 'DirectCut3'}
    alias = BANNED881 - {'step'}                          # a bare name 'step' is ordinary data; a call .step() is still refused
    used |= {n.id for n in _a881.walk(node) if isinstance(n, _a881.Name)} & alias
    used |= {n.attr for n in _a881.walk(node) if isinstance(n, _a881.Attribute)} & alias
    used |= {c.args[1].value for c in _a881.walk(node) if isinstance(c, _a881.Call) and getattr(c.func, 'id', None) in
             ('getattr', 'setattr', 'hasattr') and len(c.args) > 1 and isinstance(c.args[1], _a881.Constant)} & BANNED881
    bad = (used & BANNED881) - set(allow)
    assert not bad, ('FIREWALL881', getattr(node, 'name', '?'), sorted(bad))

def oracle_scan881(node):
    names = {n.id for n in _a881.walk(node) if isinstance(n, _a881.Name)} | \
            {n.attr for n in _a881.walk(node) if isinstance(n, _a881.Attribute)}
    keys = {n.value for n in _a881.walk(node) if isinstance(n, _a881.Constant) and isinstance(n.value, str)}
    bad = (names | keys) & ORACLE881
    assert not bad, ('ORACLE_FIREWALL881', node.name, sorted(bad))

def capture_source881():
    # the RUNNING cell is the last history entry; the cell carries no self-hash: its blob/SHA-256 are measured here and written
    # to a manifest before the model is loaded (the report and every new cartridge carry them)
    try:
        source, how = get_ipython().history_manager.input_hist_raw[-1], 'IPYTHON_CURRENT_CELL'
    except NameError:
        source = open(__file__, encoding='utf-8').read() if '__file__' in globals() else None; how = 'FILE_%RUN'
    assert source and MARKER881 in source and 'def gate4_881' in source, 'EXECUTED_881_SOURCE_NOT_CAPTURED'
    tree = _a881.parse(source); funcs = {n.name: n for n in tree.body if isinstance(n, _a881.FunctionDef)}
    for name, node in funcs.items():
        if name.endswith('881'): scan881(node, EXEC_ALLOW881 if name == 'gate4_881' else ())
    assert set(RUNTIME881) <= set(funcs), ('RUNTIME_FUNCTIONS_MISSING', sorted(set(RUNTIME881) - set(funcs)))
    for name in RUNTIME881: oracle_scan881(funcs[name])
    calls = [n for n in _a881.walk(tree) if isinstance(n, _a881.Call) and getattr(n.func, 'id', None) == 'reproduce_pre859859']
    assert len(calls) == 1, 'MODEL_LOADER_CALL_COUNT_NOT_ONE'
    rs = [n for n in _a881.walk(tree) if isinstance(n, _a881.Assign) and any(getattr(t, 'id', '') == 'xray_point870' for t in n.targets)]
    assert len(rs) == 1 and getattr(rs[0].value, 'id', None) == 'probe881', 'FIREWALL881_REBIND'
    (ROOT864 / 'TEST881.py').write_text(source, encoding='utf-8')
    STATE881['source'] = {'how': how, 'executed_cell_git_blob': git_blob864(source.encode()),
                          'executed_cell_sha256': sha256_bytes864(source.encode()), 'lines': source.count('\n') + 1,
                          'differs_from_r1': git_blob864(source.encode()) != R1_BLOB881, 'firewall': 'PASS',
                          'oracle_firewall': 'PASS (%d runtime functions)' % len(RUNTIME881)}
    json_write864('881_source_manifest.json', dict(STATE881['source'], prereg_sha256=PREREG_SHA881, head=HEAD881,
                                                   engine_blob=ENGINE_BLOB881, before_model_load=True))

def select_locked881():
    for name, blob in REQUIRED_LOCKS881.items():
        assert LOCKS864.get(name) == blob and git_blob864(RAW_SOURCES864[name]) == blob, ('REQUIRED_LOCK', name)
    tree = _a881.parse(RAW_SOURCES864['878.py'].decode(), filename='878.py')
    consts = [n for n in tree.body if isinstance(n, _a881.Assign) and
              {x.id for t in n.targets for x in _a881.walk(t) if isinstance(x, _a881.Name)} & set(CONSTS878)]
    funcs = [n for n in tree.body if isinstance(n, (_a881.FunctionDef, _a881.ClassDef)) and n.name in FUNCS878]
    assert {n.name for n in funcs} == set(FUNCS878), ('SELECT_878', sorted(set(FUNCS878) - {n.name for n in funcs}))
    for n in funcs:
        if isinstance(n, _a881.FunctionDef): scan881(n, ('native_append_direct',) if n.name == 'append_exp878' else ())
    exec(compile(_a881.fix_missing_locations(_a881.Module(consts, [])), '878.py:constants', 'exec'), globals())
    assert sha256_bytes864(_j881.dumps(PREREG878, sort_keys=True).encode()) == TEST878_PREREG881, 'TEST878_PREREG_MISMATCH'
    exec(compile(_a881.fix_missing_locations(_a881.Module(funcs, [])), '878.py:selected', 'exec'), globals())
    t880 = _a881.parse(RAW_SOURCES864['880.py'].decode(), filename='880.py')
    f880 = [n for n in t880.body if isinstance(n, _a881.FunctionDef) and n.name in FUNCS880]
    assert {n.name for n in f880} == set(FUNCS880), 'SELECT_880'
    for n in f880: scan881(n)
    exec(compile(_a881.fix_missing_locations(_a881.Module(f880, [])), '880.py:selected', 'exec'), globals())
    log8, log9 = RAW_SOURCES864['Test_878_log2.log'].decode(), RAW_SOURCES864['879.log'].decode()
    prov = {'878': all(x in log8 for x in ('NVIDIA A100-SXM4-80GB', 'cell %s | prereg %s' % (LOCKS864['878.py'], TEST878_PREREG881[:16]),
                                          'TEST878 | status COMPLETE')),
            '879': all(x in log9 for x in ('NVIDIA A100-SXM4-80GB', 'prereg 6b7d8639d93b2110',
                                          'TEST879 VERDICT MATCHED_FORK_OUTCOME_TRANSFER', 'status COMPLETE'))}
    assert all(prov.values()), ('LOCKED_LOG_PROVENANCE', prov)
    STATE881['source']['reused'] = {'878.py': LOCKS864['878.py'], 'functions878': sorted(FUNCS878), 'constants878': len(consts),
                                    '880.py': LOCKS864['880.py'], 'functions880': sorted(FUNCS880), 'head': HEAD881,
                                    'locked_gpu_logs': 'provenance only (string presence in blob-locked logs), not a new runtime PASS'}
    return log9

def ref879_881(log9):
    out, key = {}, None
    for l in log9.splitlines():
        m = _r881.match(r'CELL (S\d\d>R\d\d) ', l)
        if m: key = m.group(1); continue
        m = _r881.match(r'\s+(FULL_[ML]|C_BLIND_[ML])\s+(\w+)\s+(.*)$', l)
        if m and key in ('S00>R00', 'S01>R01'):
            out.setdefault(key, {})[m.group(1)] = {k: float(v) for k, v in _r881.findall(r'([A-Z]+)=([0-9.]+)', m.group(3))}
    return out

def targets881(refs):
    # static gates from the locked 869 records only (no CAR result is read)
    for item in SOURCES878 + FORKS878:
        if (item, ARM878) not in refs: raise Gate881('RECORD_MISSING ' + item)
    ctl = lambda item: [e for e in refs[(item, ARM878)]['events'] if e['type'] == 'CONTROL']
    src, rec, cells = {}, {}, {}
    for w in WORLDS878:
        cards, shas, t2 = [], [], {}
        for cnd in ('MISSING', 'LIVE'):
            item = 'I867_%s_%s' % (w, cnd); cs = ctl(item)
            if [x['record']['action'] for x in cs[:2]] != ['ADVANCE', ACTION878]: raise Gate881('T2_PATH ' + item)
            eff = [e for e in refs[(item, ARM878)]['events'] if e['type'] == 'EFFECT' and e.get('effect') == 'MOUNTED']
            if not (eff and eff[0].get('action') == ACTION878): raise Gate881('OUTCOME_EFFECT ' + item)
            cards.append(eff[0]['chosen']); shas += [cs[1]['record']['state_sha256'], cs[2]['record']['state_sha256']]; t2[cnd] = cs[1]
        if t2['MISSING']['record']['state_sha256'] != t2['LIVE']['record']['state_sha256']: raise Gate881('T2_STATE_NOT_SHARED ' + w)
        if cards[0] == cards[1]: raise Gate881('OUTCOME_CARDS_EQUAL ' + w)
        src[w] = {'cards': cards, 'shas': shas, 'world_index': refs[('I867_%s_MISSING' % w, ARM878)]['world_index']}
    canon = lambda d: _j881.dumps(d, sort_keys=True)
    all_shas = {canon(s) for w in WORLDS878 for s in src[w]['shas']}
    for r in WORLDS878:
        item = 'I867_%s_FORK' % r; cs = ctl(item)
        if len(cs) < FORK_STEP878: raise Gate881('FORK_STEP_MISSING ' + item)
        f = cs[FORK_STEP878 - 1]; ev = refs[(item, ARM878)]['events']; ix = ev.index(f)
        nxt_eff = next((e for e in ev[ix + 1:] if e['type'] == 'EFFECT'), None)
        nxt_hop = next((e for e in ev[ix + 1:] if e['type'] == 'HOP'), None)
        rec[r] = {'item': item, 'step': FORK_STEP878, 'mounted': list(f['mounted']), 'state_sha256': f['record']['state_sha256'],
                  'world_index': refs[(item, ARM878)]['world_index'], 'recorded_action': f['record']['action'],
                  'recorded_effect': None if nxt_eff is None else {k: nxt_eff.get(k) for k in ('action', 'effect', 'chosen')},
                  'recorded_next_hop_raw': None if nxt_hop is None else nxt_hop.get('raw')}
    for s, r in CELLS881:
        why = []
        if set(rec[r]['mounted']) & set(src[s]['cards']): why.append('SOURCE_OUTCOME_CARD_MOUNTED')
        if canon(rec[r]['state_sha256']) in all_shas: why.append('RECEIVER_IS_A_SOURCE_STATE')
        if (rec[r]['world_index'] == src[s]['world_index']) != (s == r): why.append('GOAL_RELATION')
        cells['%s>%s' % (s, r)] = {'relation': 'SAME_GOAL' if s == r else 'CROSS', 'independent': not why, 'why': why}
    bad = {k: v['why'] for k, v in cells.items() if not v['independent']}
    if bad: raise Gate881('RECEIVER_NOT_INDEPENDENT %s' % _j881.dumps(bad))
    return {'sources': src, 'receivers': rec, 'cells': cells}

# ============================ append-only REAL store: transaction, recovery, idempotency (pure Python) ============================
class RealStore881:
    # catalog.jsonl at root; data files <id>.pt with sidecar <id>.entry.json in data directories; quarantine/ never overwritten
    def __init__(self, root, data_dirs):
        self.root = str(root); self.dirs = [str(d) for d in data_dirs]
        self.catalog = _o881.path.join(self.root, 'catalog.jsonl'); self.qdir = _o881.path.join(self.root, 'quarantine')
        for d in [self.root, self.qdir] + self.dirs: _o881.makedirs(d, exist_ok=True)

    @staticmethod
    def fsync_file(path):
        fd = _o881.open(path, _o881.O_RDONLY)
        try: _o881.fsync(fd)
        finally: _o881.close(fd)

    @staticmethod
    def fsync_dir(path):
        fd = _o881.open(path, _o881.O_RDONLY)
        try: _o881.fsync(fd)
        finally: _o881.close(fd)

    @staticmethod
    def sha_file(path):
        h = _h881.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(1 << 22), b''): h.update(chunk)
        return h.hexdigest()

    def quarantine(self, path, why):
        base = _o881.path.basename(path); n = 0
        while True:
            dst = _o881.path.join(self.qdir, '%s.q%03d' % (base, n))
            if not _o881.path.exists(dst): break
            n += 1
        _o881.replace(path, dst); self.fsync_dir(self.qdir); self.fsync_dir(_o881.path.dirname(path))
        return {'from': path, 'to': dst, 'why': why}

    def read_catalog(self):
        if not _o881.path.exists(self.catalog): return [], b''
        raw = open(self.catalog, 'rb').read(); rows, good = [], 0
        for line in raw.split(b'\n')[:-1]:
            try: rows.append(_j881.loads(line.decode('utf-8')))
            except ValueError: raise IntegrityBlock881('CATALOG_CORRUPT_LINE %d' % len(rows))
            good += len(line) + 1
        return rows, raw[good:]

    def generation(self, rows):
        return max([int(r.get('generation', 0)) for r in rows] + [0]) + 1

    def append_line(self, row, fault=None):
        line = (_j881.dumps(row, sort_keys=True) + '\n').encode('utf-8')
        with open(self.catalog, 'ab') as f:
            if fault is not None and fault.get('partial'):
                f.write(line[:len(line) // 2]); f.flush(); fault['fn']('CATALOG_APPEND')
            f.write(line); f.flush()
            if fault is not None: fault['fn']('CATALOG_APPEND')
            _o881.fsync(f.fileno())
        if fault is not None: fault['fn']('CATALOG_FSYNC')
        self.fsync_dir(self.root)
        if fault is not None: fault['fn']('CATALOG_DIR_FSYNC')

    def recover(self, verify):
        rep = {'tail_repaired': None, 'quarantined': [], 'recatalogued': [], 'verified': 0}
        rows, tail = self.read_catalog()
        if tail:
            tmp = self.catalog + '.tail'
            with open(tmp, 'wb') as f: f.write(tail); f.flush(); _o881.fsync(f.fileno())
            rep['quarantined'].append(self.quarantine(tmp, 'PARTIAL_CATALOG_TAIL'))
            good = open(self.catalog, 'rb').read()[:-len(tail)]; ctmp = self.catalog + '.rewrite'
            with open(ctmp, 'wb') as f: f.write(good); f.flush(); _o881.fsync(f.fileno())
            _o881.replace(ctmp, self.catalog); self.fsync_dir(self.root); rep['tail_repaired'] = len(tail)
        seen = {}
        for r in rows:
            if r['id'] in seen:
                if seen[r['id']] != r['sha256']: raise IntegrityBlock881('DUPLICATE_ID_DIFFERENT_SHA ' + r['id'])
                raise IntegrityBlock881('DUPLICATE_CATALOG_ENTRY ' + r['id'])
            seen[r['id']] = r['sha256']
            if not _o881.path.exists(r['file']) or self.sha_file(r['file']) != r['sha256']:
                raise IntegrityBlock881('DANGLING_OR_CORRUPT_POINTER ' + r['id'])
            verify(r['entry']); rep['verified'] += 1
        for d in self.dirs:
            for name in sorted(_o881.listdir(d)):
                p = _o881.path.join(d, name)
                if name.endswith('.pt'):
                    eid = name[:-3]
                    if eid in seen: continue
                    side = _o881.path.join(d, eid + '.entry.json'); entry = None
                    if _o881.path.exists(side):
                        try: entry = _j881.loads(open(side, encoding='utf-8').read())
                        except ValueError: entry = None
                    ok = entry is not None and entry.get('file') == p and self.sha_file(p) == entry.get('sha256')
                    if ok:
                        try: verify(entry)
                        except Exception: ok = False
                    if ok:
                        rows2, _ = self.read_catalog()
                        self.append_line({'id': eid, 'file': p, 'sha256': entry['sha256'], 'entry': entry,
                                          'generation': self.generation(rows2), 'recovered': True})
                        seen[eid] = entry['sha256']; rep['recatalogued'].append(eid)
                    else:
                        rep['quarantined'].append(self.quarantine(p, 'ORPHAN_WITHOUT_VALID_SIDECAR'))
                        if _o881.path.exists(side): rep['quarantined'].append(self.quarantine(side, 'ORPHAN_SIDECAR'))
                elif name.endswith('.tmp'):
                    rep['quarantined'].append(self.quarantine(p, 'TEMPORARY_FILE'))
                elif name.endswith('.entry.json') and name[:-len('.entry.json')] not in seen and \
                        not _o881.path.exists(_o881.path.join(d, name[:-len('.entry.json')] + '.pt')):
                    rep['quarantined'].append(self.quarantine(p, 'SIDECAR_WITHOUT_FILE'))
        rows, tail = self.read_catalog()
        assert not tail and all(_o881.path.exists(r['file']) for r in rows), 'RECOVERY_POSTCONDITION'
        return rep

    def commit(self, eid, data_dir, write, verify, fault=None, existing=None, prewritten=False):
        # write(data_dir) must create data_dir/<eid>.pt (tmp + rename) and return the entry; nothing is moved on failure.
        # prewritten=True registers a file the locked writer already produced (the replayed source cartridges)
        state = 'START'; ff = (lambda s: None) if fault is None else fault['fn']
        rows, tail = self.read_catalog()
        if tail: raise CommitUncertain881('PARTIAL_CATALOG_TAIL_BEFORE_COMMIT')
        hit = [r for r in rows if r['id'] == eid]
        if hit:                                          # idempotency: compare content without touching the committed file
            if existing is None: raise IntegrityBlock881('ID_EXISTS_CONTENT_UNKNOWN ' + eid)
            if existing != hit[0]['sha256']: raise IntegrityBlock881('ID_EXISTS_DIFFERENT_SHA ' + eid)
            return {'entry': hit[0]['entry'], 'state': 'IDEMPOTENT_NO_OP', 'generation': hit[0]['generation']}
        path = _o881.path.join(data_dir, eid + '.pt')
        if _o881.path.exists(path) != bool(prewritten): raise CommitUncertain881('FILE_STATE_UNEXPECTED ' + eid)
        try:
            entry = write(data_dir); state = 'FILE_RENAMED'
            assert entry['file'] == path and _o881.path.exists(path), 'WRITER_PATH'
            self.fsync_file(path); state = 'FILE_FSYNC'; ff(state)
            side = _o881.path.join(data_dir, eid + '.entry.json'); stmp = side + '.tmp'
            with open(stmp, 'w', encoding='utf-8') as f:
                f.write(_j881.dumps(entry, sort_keys=True)); f.flush(); _o881.fsync(f.fileno())
            _o881.replace(stmp, side); state = 'SIDECAR'; ff(state)
            self.fsync_dir(data_dir); state = 'DIR_FSYNC'; ff(state)
            if self.sha_file(path) != entry['sha256']: raise IntegrityBlock881('WRITTEN_FILE_SHA ' + eid)
            verify(entry); state = 'VERIFIED_RELOAD'; ff(state)
            gen = self.generation(rows)
            self.append_line({'id': eid, 'file': path, 'sha256': entry['sha256'], 'entry': entry, 'generation': gen},
                             fault); state = 'COMMITTED'
            return {'entry': entry, 'state': state, 'generation': gen}
        except IntegrityBlock881:
            raise
        except BaseException as exc:
            raise CommitUncertain881('%s after %s: %s' % (type(exc).__name__, state, exc))

def selftest_store881():
    # CPU-only fault injection on a throw-away directory (never the REAL namespace)
    res, root = {}, _tf881.mkdtemp(prefix='t881_store_selftest_')
    def writer(content, eid, crash=None):
        def w(d):
            p = _o881.path.join(d, eid + '.pt'); tmp = p + '.tmp'
            with open(tmp, 'wb') as f: f.write(content); f.flush(); _o881.fsync(f.fileno())
            if crash == 'TMP_WRITTEN': raise RuntimeError('INJECTED TMP_WRITTEN')
            _o881.replace(tmp, p)
            if crash == 'FILE_RENAMED': raise RuntimeError('INJECTED FILE_RENAMED')
            return {'id': eid, 'file': p, 'sha256': _h881.sha256(content).hexdigest()}
        return w
    def verify(entry):
        if RealStore881.sha_file(entry['file']) != entry['sha256']: raise IntegrityBlock881('VERIFY')
    def invariants(st):
        rows, tail = st.read_catalog(); ids = [r['id'] for r in rows]
        files = [n for d in st.dirs for n in _o881.listdir(d) if n.endswith('.pt')]
        return (not tail and len(ids) == len(set(ids)) and all(RealStore881.sha_file(r['file']) == r['sha256'] for r in rows)
                and sorted(n[:-3] for n in files) == sorted(ids) and not [n for d in st.dirs for n in _o881.listdir(d) if n.endswith('.tmp')])
    try:
        for stage in STAGES881[:-1]:
            d = _o881.path.join(root, stage); st = RealStore881(d, [_o881.path.join(d, 'data')]); data = st.dirs[0]
            st.commit('base', data, writer(b'base', 'base'), verify)
            crash = stage if stage in ('TMP_WRITTEN', 'FILE_RENAMED') else None
            def fn(s, stage=stage):
                if s == stage: raise RuntimeError('INJECTED ' + s)
            fault = None if crash else {'fn': fn, 'partial': stage == 'CATALOG_APPEND'}
            outcome = 'NO_EXCEPTION'
            try: st.commit('x', data, writer(b'payload-x', 'x', crash), verify, fault)
            except CommitUncertain881 as e: outcome = 'UNCERTAIN'
            rep = st.recover(verify); rows, _ = st.read_catalog(); ids = [r['id'] for r in rows]
            expect_cat = stage in ('SIDECAR', 'DIR_FSYNC', 'VERIFIED_RELOAD', 'CATALOG_APPEND', 'CATALOG_FSYNC', 'CATALOG_DIR_FSYNC')
            ok = outcome == 'UNCERTAIN' and invariants(st) and ('x' in ids) == expect_cat and ids.count('x') <= 1 and 'base' in ids
            gens = [r['generation'] for r in rows]; ok = ok and gens == sorted(gens) and len(set(gens)) == len(gens)
            res['crash_' + stage] = {'pass': ok, 'catalogued_after_recovery': 'x' in ids, 'recovery': {k: (len(v) if isinstance(v, list) else v)
                                                                                                    for k, v in rep.items()}}
        d = _o881.path.join(root, 'idem'); st = RealStore881(d, [_o881.path.join(d, 'data')]); data = st.dirs[0]
        a = st.commit('e', data, writer(b'one', 'e'), verify)
        b = st.commit('e', data, writer(b'one', 'e'), verify, existing=_h881.sha256(b'one').hexdigest())
        try: st.commit('e', data, writer(b'two', 'e'), verify, existing=_h881.sha256(b'two').hexdigest()); c = False
        except IntegrityBlock881: c = True
        rows, _ = st.read_catalog()
        res['idempotency'] = {'pass': a['state'] == 'COMMITTED' and b['state'] == 'IDEMPOTENT_NO_OP' and c and len(rows) == 1}
        st.commit('f', data, writer(b'three', 'f'), verify); rows, _ = st.read_catalog()
        res['generation_monotonic'] = {'pass': [r['generation'] for r in rows] == [1, 2]}
        q1 = _o881.path.join(data, 'z.pt'); open(q1, 'wb').write(b'a'); r1 = st.recover(verify)
        open(q1, 'wb').write(b'b'); r2 = st.recover(verify)
        names = sorted(_o881.listdir(st.qdir))
        res['quarantine_no_overwrite'] = {'pass': len([n for n in names if n.startswith('z.pt.q')]) == 2 and
                                          open(_o881.path.join(st.qdir, 'z.pt.q000'), 'rb').read() == b'a'}
        _o881.replace(_o881.path.join(data, 'f.pt'), _o881.path.join(root, 'moved_away.pt'))
        try: st.recover(verify); dang = False
        except IntegrityBlock881: dang = True
        res['dangling_pointer_blocks'] = {'pass': dang}
        d = _o881.path.join(root, 'corrupt'); st = RealStore881(d, [_o881.path.join(d, 'data')])
        open(st.catalog, 'wb').write(b'{"id": "a"}\nnot-json\n{"id": "b"}\n')
        try: st.read_catalog(); cor = False
        except IntegrityBlock881: cor = True
        res['corrupt_middle_line_blocks'] = {'pass': cor}
    finally:
        _s881.rmtree(root, ignore_errors=True)
    STATE881['selftests']['store'] = res
    bad = [k for k, v in res.items() if not v['pass']]
    if bad: raise Gate881('STORE_SELFTEST_FAIL %s' % bad)
    return res

def selftest_mask881():
    # CPU principle test of the 2-D readable mask (1 = readable) + causal order + restore, with torch SDPA on a toy cache:
    # C content must not reach X when hidden; restore == full; a fully hidden slot is content-independent
    g = torch.Generator().manual_seed(881); B, E0, C0, E1, L = 4, 4, 7, 9, 3; N = E1 + L
    q = torch.randn(1, 2, L, 8, generator=g); base = torch.randn(1, 2, N, 8, generator=g); val = torch.randn(1, 2, N, 8, generator=g)
    def run(k, v, hide, restore=()):
        allow = torch.ones(L, N, dtype=torch.bool)
        for i in range(L): allow[i, E1 + i + 1:] = False
        am = torch.ones(N, dtype=torch.bool)
        for a, b in hide: am[a:b] = False
        m = allow & am.unsqueeze(0)
        for a, b in restore: m[:, a:b] = allow[:, a:b]
        return torch.nn.functional.scaled_dot_product_attention(q, k, v, attn_mask=m.unsqueeze(0).unsqueeze(0))
    k2, v2 = base.clone(), val.clone(); k2[:, :, C0:E1] += 3.0; v2[:, :, C0:E1] -= 2.0
    kz, vz = base.clone(), val.clone(); kz[:, :, E0:E1] = 0; vz[:, :, E0:E1] = 0
    res = {'C_blind_content_invariant': bool(torch.equal(run(base, val, [(C0, E1)]), run(k2, v2, [(C0, E1)]))),
           'restore_equals_full': bool(torch.allclose(run(base, val, [(C0, E1)], [(C0, E1)]), run(base, val, []), atol=1e-6)),
           'hidden_slot_content_invariant': bool(torch.equal(run(base, val, [(E0, E1)]), run(kz, vz, [(E0, E1)]))),
           'visible_C_changes_output': not bool(torch.equal(run(base, val, []), run(k2, v2, []))),
           'scope': 'principle of the mask semantics only; the model path is gated on the GPU'}
    STATE881['selftests']['mask'] = res
    if not all(v for k, v in res.items() if k != 'scope'): raise Gate881('MASK_SELFTEST_FAIL %s' % res)
    return res

def selftest_firewall881():
    cases = {'alias': 'def f881():\n    g = execute866\n    g()\n', 'getattr': "def f881(m):\n    getattr(m, 'register_forward_hook')(1)\n",
             'attr': 'def f881(m):\n    m.register_forward_hook(1)\n', 'kw': 'def f881(m):\n    m(output_hidden_states=True)\n'}
    res = {}
    for k, src in cases.items():
        try: scan881(_a881.parse(src).body[0]); res[k] = False
        except AssertionError: res[k] = True
    ok_src = 'def f881(x):\n    step = x + 1\n    return step\n'
    try: scan881(_a881.parse(ok_src).body[0]); res['data_name_step_allowed'] = True
    except AssertionError: res['data_name_step_allowed'] = False
    STATE881['selftests']['firewall'] = res
    if not all(res.values()): raise Gate881('FIREWALL_SELFTEST_FAIL %s' % res)
    return res

# ============================ budget, timing, memory accounting ============================
def peak_update881():
    b = STATE881['budget']
    b['peak_alloc_gib'] = max(b['peak_alloc_gib'], torch.cuda.max_memory_allocated() / 2**30)
    b['peak_reserved_gib'] = max(b['peak_reserved_gib'], torch.cuda.max_memory_reserved() / 2**30)

def free_gib881():
    return (torch.cuda.mem_get_info()[0] + torch.cuda.memory_reserved() - torch.cuda.memory_allocated()) / 2**30

def guard881(stage, need_gib=0.0):
    peak_update881(); el = (time.perf_counter() - T_START878) / 60.0; free = free_gib881(); b = STATE881['budget']
    why = [x for x, bad in (('WALL %.1f>%.0f min' % (el, WALL_MIN881), el > WALL_MIN881),
                            ('VRAM_FREE %.2f<%.1f GiB' % (free, FREE_MIN_GIB881 + need_gib), free < FREE_MIN_GIB881 + need_gib),
                            ('PEAK %.2f>%.0f GiB' % (b['peak_alloc_gib'], PEAK_GIB881), b['peak_alloc_gib'] > PEAK_GIB881),
                            ('ADAPTER_FFE %.1f>%.0f' % (b['adapter_ffe_lower_bound'], FFE_MAX881),
                             b['adapter_ffe_lower_bound'] > FFE_MAX881)) if bad]
    if why: raise Budget881('%s: %s' % (stage, '; '.join(why)))

def ffe881(tokens, layers=80):
    STATE881['budget']['adapter_ffe_lower_bound'] += float(tokens) * float(layers) / 80.0 / 256.0

def kv_gib881(kv):
    return sum(t.numel() * t.element_size() for pair in kv for t in pair) / 2**30

def timed881(tag, fn, *args, **kwargs):
    peak_update881(); torch.cuda.reset_peak_memory_stats()
    a0, r0 = torch.cuda.memory_allocated(), torch.cuda.memory_reserved()
    s, e = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
    s.record(); out = fn(*args, **kwargs); e.record(); torch.cuda.synchronize()
    STATE881['budget']['arms'][tag] = {'ms': round(float(s.elapsed_time(e)), 2), 'alloc_before_gib': round(a0 / 2**30, 3),
                                      'alloc_after_gib': round(torch.cuda.memory_allocated() / 2**30, 3),
                                      'peak_alloc_gib': round(torch.cuda.max_memory_allocated() / 2**30, 3),
                                      'reserved_before_gib': round(r0 / 2**30, 3),
                                      'peak_reserved_gib': round(torch.cuda.max_memory_reserved() / 2**30, 3)}
    peak_update881()
    return out

def seqlp881(reading):
    return {s['word']: float(s['sequence_logp']) for s in reading['scores']}

def cont_tokens881():
    return sum(len(ids) - 1 for _, ids in ACTION_IDS867)

def same_reading881(a, b):
    # same873 compares token logps only: action, argmax word, abstention and mass are compared here as well
    return bool(same873(a, b) and a.get('action') == b.get('action') and a.get('argmax_word') == b.get('argmax_word') and
                a.get('abstain') == b.get('abstain') and a.get('mass') == b.get('mass'))

def arm_record881(cell, cond, arm, reading, spans):
    rec = {'cell': cell, 'source': cond, 'arm': arm, 'action': reading['action'], 'argmax_word': reading.get('argmax_word'),
           'abstain': reading.get('abstain'), 'mass': reading.get('mass'), 'normalized': reading.get('normalized'), 'mask_spans': spans,
           'scores': [{'word': s['word'], 'ids': list(s['ids']), 'token_logps': s['token_logps'],
                       'sequence_logp': s['sequence_logp']} for s in reading['scores']]}
    ARMS881.setdefault(cell, {})['%s_%s' % (arm, cond)] = rec
    with open(ROOT864 / '881_arms.jsonl', 'a', encoding='utf-8') as f:
        f.write(_j881.dumps(rec, sort_keys=True, default=str) + '\n')
    return rec

# ============================ adapter: layout, digests, reads (runtime; no labels) ============================
def tsha881(t):
    return _h881.sha256(t.detach().contiguous().cpu().view(torch.uint8).numpy().tobytes()).hexdigest()

def full_seal881(kv):
    layers = [[tsha881(k), tsha881(v)] for k, v in kv]
    return {'layers': len(layers), 'tokens': int(kv[0][0].shape[-2]),
            'all': _h881.sha256(_j881.dumps(layers).encode()).hexdigest(), 'per_layer': layers}

def make_single_episode_layout881(env, T, S):
    n0, q = length873(env, T['m']), int(S['entry']['body_tokens'])
    sp = S['entry']['provenance']['spans_body']; L = int(T['X'].shape[0])
    lay = {'n0': n0, 'q': q, 'L': L, 'E': [n0, n0 + q], 'X2': [n0 + sp['X2'][0], n0 + sp['X2'][1]],
           'A': [n0 + sp['A'][0], n0 + sp['A'][1]], 'C': [n0 + sp['C'][0], n0 + sp['C'][1]], 'X': [n0 + q, n0 + q + L]}
    lay['N'] = n0 + q + L
    assert lay['X2'][0] == n0 and lay['X2'][1] == lay['A'][0] and lay['A'][1] == lay['C'][0] and lay['C'][1] == n0 + q, \
        ('LAYOUT_SPANS', lay)
    assert lay['C'][1] - lay['C'][0] == int(S['body']) and sp['C'][1] == q, ('C_SPAN_PROVENANCE', lay, S['body'])
    assert lay['N'] + max(len(ids) for _, ids in ACTION_IDS867) <= int(env['MAX_FUSED_TOKENS']), ('MAX_FUSED_TOKENS', lay['N'])
    lay['sha256'] = sha256_bytes864(_j881.dumps(lay, sort_keys=True).encode())
    return lay

def xread881(env, kv, X, blind, sham, tag):
    ffe881(int(X.shape[0]) + cont_tokens881())
    return timed881(tag, xcar878, env, kv, X, [tuple(b) for b in blind], sham)

def nread881(env, kv, X, ranges, rows, tag):
    ffe881(int(X.shape[0]) + cont_tokens881())
    r, got, _, _ = timed881(tag, decide874, env, kv, X, [tuple(b) for b in ranges], rows)
    return r, got

def xtrace881(env, kv, X, blind):
    # the xcar878 procedure step by step (own cache, explicit layers, same 2-D mask for X and every continuation, crop after
    # each candidate) + bitwise digests: X K/V of all 80 layers, X final (pre-norm) hidden, and for every continuation token
    # its 80-layer K/V, hidden and logp. Read-only: no score or action is altered.
    model, NL = env['model'], int(env['NL']); cache = env['cache_build'](list(kv)); n0 = int(cache.get_seq_length())
    env['budget849'](); L = int(X.shape[0]); n1 = n0 + L
    assert n1 + max(len(ids) for _, ids in ACTION_IDS867) <= int(env['MAX_FUSED_TOKENS']), ('CONTEXT_LIMIT', n1)
    def fwd(Y):
        m, nc = int(Y.shape[0]), int(cache.get_seq_length())
        am = torch.ones((1, nc + m), device=env['DEV'], dtype=torch.long)
        for a, b in blind: am[0, a:b] = 0
        h = xspan878(env, cache, Y.reshape(1, m, int(env['H'])), am, 0, NL, (), ())
        with torch.no_grad(): lp = torch.log_softmax(model.lm_head(model.model.norm(h))[0].float(), dim=-1)
        return h, lp, nc, m, am
    h, lp, _, _, am = fwd(X); first = lp[-1]
    tr = {'X': {'kv': [[tsha881(k[:, :, n0:n1]), tsha881(v[:, :, n0:n1])] for k, v in (cache_kv870(cache, i) for i in range(NL))],
                'hidden': tsha881(h), 'mask_sha256': tsha881(am), 'positions': [n0, n1]}, 'continuations': {}}
    del h, lp; scores = []
    for word, ids in ACTION_IDS867:
        token_logps = [float(first[ids[0]])]
        if len(ids) > 1:
            m = len(ids) - 1; h, lp, nc, _, am = fwd(env['embed841'](ids[:-1]))
            token_logps += [float(lp[i, ids[i + 1]]) for i in range(m)]
            tr['continuations'][word] = {'kv': [[tsha881(k[:, :, nc:nc + m]), tsha881(v[:, :, nc:nc + m])] for k, v in
                                                (cache_kv870(cache, i) for i in range(NL))],
                                         'hidden': tsha881(h), 'logps': token_logps[1:], 'positions': [nc, nc + m],
                                         'mask_sha256': tsha881(am)}
            cache.crop(-m); assert int(cache.get_seq_length()) == n1, 'TRACE_CROP_LENGTH'
            del h, lp
        scores.append({'word': word, 'ids': ids, 'token_logps': token_logps, 'sequence_logp': float(sum(token_logps)),
                       'hard_greedy_ids': []})
    top = torch.topk(first, 10); del cache
    rd = reading867({'scores': scores, 'path': 'CROP', 'fallback_reason': None,
                     'first_top10': {'ids': [int(i) for i in top.indices.tolist()]}, 'X_sha256': None})
    ffe881(L + cont_tokens881())
    return rd, tr

def zero_slot881(env, kv, a, b):
    out = []
    for k, v in kv:
        k2, v2 = k.clone(), v.clone(); k2[:, :, a:b] = 0; v2[:, :, a:b] = 0; out.append((k2, v2))
    return out

def same_rows881(ra, rb):
    return len(ra) == len(rb) and all(torch.equal(x[0], y[0]) and torch.equal(x[1], y[1]) for x, y in zip(ra, rb))

# ============================ GATE1: sources, persistence, fixtures ============================
def sources881(env):
    for w in WORLDS878:
        M, L = SRC878.get('I867_%s_MISSING' % w), SRC878.get('I867_%s_LIVE' % w)
        R = STATE881['sources'].setdefault(w, {})
        if M is None or L is None: raise Gate881('SOURCE_EXPERIENCE_NOT_CAPTURED ' + w)
        R['gates'] = g = {'same_t2_spans': (M['n2'], M['L2'], M['la']) == (L['n2'], L['L2'], L['la']),
                          'same_action_tokens': M['A_ids'] == L['A_ids'] and M['t2_action'] == L['t2_action'] == ACTION878,
                          'real_cards_differ': M['card'] != L['card'], 'same_C_length': M['body'] == L['body'],
                          'pre_C_cartridge_rows_bitwise': M['entry']['pre_C_seal'] == L['entry']['pre_C_seal'],
                          'C_cartridge_sha_differ': M['entry']['sha256'] != L['entry']['sha256'],
                          'same_goal': M['qid'] == L['qid'], 'real_namespace': all(str(EXP_DIR878) in S['entry']['file'] for S in (M, L))}
        if not all(g.values()): raise Gate881('SOURCE_PAIR_GATES %s %s' % (w, _j881.dumps(g)))
        guard881('persist_' + w)
        R['persistence'] = {S['cond']: persist878(env, S) for S in (M, L)}
        for S in (M, L):
            ffe881(3 * int(S['entry']['body_tokens']) + int(S['X3'].shape[0]) + cont_tokens881())
            STATE881['budget']['ssd_bytes'] += int(S['entry']['bytes'])
            reg = STORE881.commit(S['entry']['id'], str(EXP_DIR878), lambda d, S=S: S['entry'],
                                  lambda e: load_exp878(env, e) and None, prewritten=True)   # written by the locked writer
            R.setdefault('catalog', {})[S['cond']] = {'state': reg['state'], 'generation': reg['generation']}
        if not all(r['pass'] for r in R['persistence'].values()): raise Gate881('PERSISTENCE_FAIL ' + w)
        line881('SOURCE', w, 'gates', _j881.dumps(g, sort_keys=True), 'persist',
                _j881.dumps({k: [r['pass'], round(r['max_dp'], 5)] for k, r in R['persistence'].items()}))

def fixture_seal881(env, by_key):
    # OFFLINE labels, sealed before any receiver read (never used at runtime)
    out = {}
    for w in WORLDS878:
        spec = by_key[(int(w), 'MISSING')]; ids = world867(env, spec)['ids']; kind = {v: k for k, v in ids.items()}
        M, L = SRC878['I867_%s_MISSING' % w], SRC878['I867_%s_LIVE' % w]
        out[w] = {'LIVE_card_kind': kind.get(L['card'], 'OTHER'), 'MISSING_card_kind': kind.get(M['card'], 'OTHER')}
        out[w]['valid'] = out[w]['LIVE_card_kind'] == 'second' and out[w]['MISSING_card_kind'] not in ('second', 'changed')
        out[w]['positive'], out[w]['adverse'] = 'LIVE', 'MISSING'
    FIXTURE881.update(out)
    STATE881['fixtures'] = {'rows': out, 'sha256': sha256_bytes864(_j881.dumps(out, sort_keys=True).encode()),
                            'sealed_before_reads': True}
    json_write864('881_fixtures.json', STATE881['fixtures'])
    return out

# ============================ GATE2 + GATE3 fused per cell ============================
def receivers881(env):
    for r in WORLDS878:
        T = TGT878.get(('FORK', r))
        if T is None: raise Gate881('RECEIVER_NOT_CAPTURED_OR_RECORD_NOT_REPRODUCED R' + r)
        guard881('receiver_' + r)
        b_nat, _ = nread881(env, T['m'], T['X'], [], False, 'R%s_OFF0_native' % r)
        b_x = xread881(env, T['m'], T['X'], (), False, 'R%s_OFF0_explicit' % r)
        STATE881['receivers'][r] = {'item': T['item'], 'qid_sha256': sha256_bytes864(T['qid'].encode()), 'mounted': T['mounted'],
                                    'X_len': T['X_len'], 'X_sha256': tsha881(T['X']), 'memory_tokens': length873(env, T['m']),
                                    'B_full_seal': full_seal881(T['m'])['all'], 'OFF0_explicit_equals_native': same_reading881(b_nat, b_x)}
        arm_record881('R' + r, '-', 'OFF_0', b_x, [])
        if not STATE881['receivers'][r]['OFF0_explicit_equals_native']: raise Gate881('OFF0_EXPLICIT_NOT_NATIVE R' + r)

def cell881(env, s, r):
    key = '%s>%s' % (s, r); T = TGT878[('FORK', r)]; same_goal = s == r; X = T['X']
    M, L = SRC878['I867_%s_MISSING' % s], SRC878['I867_%s_LIVE' % s]
    if (T['qid'] == M['qid']) != same_goal or set(T['mounted']) & {M['card'], L['card']}: raise Gate881('RUNTIME_INDEPENDENCE ' + key)
    lay = {c: make_single_episode_layout881(env, T, S) for c, S in (('M', M), ('L', L))}
    if {k: v for k, v in lay['M'].items() if k != 'sha256'} != {k: v for k, v in lay['L'].items() if k != 'sha256'}:
        raise Gate881('LAYOUT_M_NE_L ' + key)
    Ly = lay['M']; C, E = Ly['C'], Ly['E']
    guard881('cell_' + key, need_gib=2 * Ly['N'] * 0.3125 / 1024)
    g = {}
    for c, S in (('M', M), ('L', L)):
        cp = load_exp878(env, S['entry']); STATE881['budget']['ssd_bytes'] += int(S['entry']['bytes'])
        g[c] = timed881('%s_append_%s' % (key, c), append_exp878, env, T['m'], cp); del cp
        ffe881(Ly['q'], 80)
        if g[c] is T['m'] or any(a[0] is b[0] or a[1] is b[1] for a, b in zip(g[c], T['m'])): raise Gate881('ALIAS_RECEIVER_MEMORY ' + key)
    G881[key] = g
    Gs = STATE881['cells'][key] = {'relation': 'SAME_GOAL' if same_goal else 'CROSS', 'layout': Ly, 'gate2': {}, 'gate3': {},
                                   'g_full_seal': {c: full_seal881(g[c])['all'] for c in 'ML'}}
    ck = Gs['gate2']
    ck['pre_C_K_bitwise_M_eq_L'] = all(torch.equal(a[0][:, :, E[0]:C[0]], b[0][:, :, E[0]:C[0]]) for a, b in zip(g['M'], g['L']))
    ck['pre_C_V_bitwise_M_eq_L'] = all(torch.equal(a[1][:, :, E[0]:C[0]], b[1][:, :, E[0]:C[0]]) for a, b in zip(g['M'], g['L']))
    Gs['C_rows_differ'] = {'K_layers': sum(not torch.equal(a[0][:, :, C[0]:C[1]], b[0][:, :, C[0]:C[1]]) for a, b in zip(g['M'], g['L'])),
                           'V_layers': sum(not torch.equal(a[1][:, :, C[0]:C[1]], b[1][:, :, C[0]:C[1]]) for a, b in zip(g['M'], g['L'])),
                           'C_cartridge_sha': [M['entry']['sha256'], L['entry']['sha256']]}
    ck['C_rows_differ_M_vs_L'] = Gs['C_rows_differ']['V_layers'] > 0 or Gs['C_rows_differ']['K_layers'] > 0
    tb = {}
    for c in 'ML':
        rd, tr = timed881('%s_CBLIND_TRACE_%s' % (key, c), xtrace881, env, g[c], X, [C])
        arm_record881(key, c, 'C_BLIND', rd, [C]); tb[c] = (rd, tr)
    TRACES881[key] = {c: tb[c][1] for c in 'ML'}
    ck['C_BLIND_M_equals_L_reading'] = same_reading881(tb['M'][0], tb['L'][0])
    ck['C_BLIND_X_KV_80_layers_bitwise'] = tb['M'][1]['X']['kv'] == tb['L'][1]['X']['kv']
    ck['C_BLIND_X_final_hidden_bitwise'] = tb['M'][1]['X']['hidden'] == tb['L'][1]['X']['hidden']
    ck['C_BLIND_continuations_KV_hidden_logp_bitwise'] = tb['M'][1]['continuations'] == tb['L'][1]['continuations']
    ck['C_BLIND_masks_and_positions_equal'] = tb['M'][1]['X']['mask_sha256'] == tb['L'][1]['X']['mask_sha256'] and \
        tb['M'][1]['X']['positions'] == tb['L'][1]['X']['positions'] == Ly['X']
    lk = xread881(env, g['M'], X, [C], False, '%s_CBLIND_LOCKED_M' % key)
    ck['trace_adapter_equals_locked_xcar878'] = same_reading881(tb['M'][0], lk); del tb, lk
    nb = {c: nread881(env, g[c], X, [C], True, '%s_NCBLIND_%s' % (key, c)) for c in 'ML'}
    for c in 'ML': arm_record881(key, c, 'NATIVE_C_BLIND', nb[c][0], [C])
    ck['native_C_BLIND_M_equals_L_reading'] = same_reading881(nb['M'][0], nb['L'][0])
    ck['native_C_BLIND_X_KV_80_layers_bitwise'] = same_rows881(nb['M'][1], nb['L'][1]); del nb
    if same_goal:
        eo = {c: xread881(env, g[c], X, [E], False, '%s_EOFF_%s' % (key, c)) for c in 'ML'}
        guard881('zero_slot_' + key, need_gib=kv_gib881(g['M']) + Ly['N'] * 0.3125 / 1024)
        z = zero_slot881(env, g['M'], E[0], E[1]); oz = xread881(env, z, X, [E], False, '%s_OFFGZERO' % key); del z
        for c in 'ML': arm_record881(key, c, 'EPISODE_OFF', eo[c], [E])
        arm_record881(key, '-', 'OFF_G_ZERO', oz, [E])
        ck['EPISODE_OFF_M_eq_L_eq_OFF_G_ZERO'] = same_reading881(eo['M'], eo['L']) and same_reading881(eo['M'], oz); del eo, oz
        fx = xread881(env, g['M'], X, (), False, '%s_FULLX_M' % key)
        for c in 'ML':
            fn, _ = nread881(env, g[c], X, [], False, '%s_NFULL_%s' % (key, c)); arm_record881(key, c, 'NATIVE_FULL', fn, [])
            if c == 'M': ck['FULL_EXPLICIT_equals_NATIVE_FULL'] = same_reading881(fx, fn)
        arm_record881(key, 'M', 'FULL_EXPLICIT', fx, []); del fx
    ck['receiver_B_full_80_layer_seal_unchanged'] = full_seal881(T['m'])['all'] == STATE881['receivers'][r]['B_full_seal']
    ck['finite'] = all(math.isfinite(x) for rd in ARMS881[key].values() for s_ in rd['scores'] for x in s_['token_logps'])
    Gs['gate2_pass'] = all(ck.values())
    line881('GATE2', key, Gs['relation'], 'pass=%s' % Gs['gate2_pass'], _j881.dumps(ck, sort_keys=True))
    if not Gs['gate2_pass']: raise Gate881('GATE2_FAIL %s %s' % (key, _j881.dumps({k: v for k, v in ck.items() if not v})))
    guard881('gate3_' + key)                               # GATE3 reads of this cell only after its GATE2 passed
    for c in 'ML': arm_record881(key, c, 'VIS', xread881(env, g[c], X, [C], True, '%s_VIS_%s' % (key, c)), [C])
    if same_goal: arm_record881(key, 'M', 'VIS_REPEAT', xread881(env, g['M'], X, [C], True, '%s_VISREP_M' % key), [C])
    Gs['gate3']['reads'] = sorted(ARMS881[key])
    Gs['g_full_seal_after_reads'] = {c: full_seal881(g[c])['all'] for c in 'ML'}
    if Gs['g_full_seal_after_reads'] != Gs['g_full_seal']: raise Gate881('GROWN_CACHE_MUTATED ' + key)
    line881('GATE3', key, 'arms=%d' % len(ARMS881[key]))
    if (s, r) != EXEC_CELL881: del G881[key]
    del g; gc.collect(); torch.cuda.empty_cache()

def measure881():
    # OFFLINE: estimands, floors, pre-registered rules and separated labels (fixtures read here, after every read)
    W = [w for w, _ in ACTION_IDS867]; out = {}; lp = lambda key, name: seqlp881(ARMS881[key][name])
    norm = lambda d: max(abs(x) for x in d.values())
    for s, r in CELLS881:
        key = '%s>%s' % (s, r); vm, vl, bm, bl = lp(key, 'VIS_M'), lp(key, 'VIS_L'), lp(key, 'C_BLIND_M'), lp(key, 'C_BLIND_L')
        d = {'delta_C_M': {a: vm[a] - bm[a] for a in W}, 'delta_C_L': {a: vl[a] - bl[a] for a in W}}
        d['T'] = {a: d['delta_C_L'][a] - d['delta_C_M'][a] for a in W}
        d['readings'] = {k: {x: ARMS881[key][k][x] for x in ('action', 'argmax_word', 'abstain', 'mass', 'normalized')}
                         for k in ARMS881[key]}
        if s == r:
            eo, off0, fx, rep = lp(key, 'EPISODE_OFF_M'), seqlp881(ARMS881['R' + r]['OFF_0_-']), lp(key, 'FULL_EXPLICIT_M'), lp(key, 'VIS_REPEAT_M')
            d['generic'] = {a: bm[a] - eo[a] for a in W}; d['slot'] = {a: eo[a] - off0[a] for a in W}
            d['kernel'] = {a: vm[a] - fx[a] for a in W}; d['repeat'] = {a: vm[a] - rep[a] for a in W}
            d['floor'] = max(SIG_MIN878, norm(d['repeat']), norm(d['kernel']))
            d['native_minus_VIS'] = {x: {a: lp(key, 'NATIVE_FULL_' + x)[a] - lp(key, 'VIS_' + x)[a] for a in W} for x in 'ML'}
        out[key] = d
    for s, r in CELLS881:
        key = '%s>%s' % (s, r); d = out[key]; fl = out['%s>%s' % (r, r)]['floor']; d['floor_used'] = fl
        d['norm_T'] = norm(d['T']); d['T_exceeds_floor'] = d['norm_T'] > fl
        d['exploratory_actions_beyond_floor'] = sorted(a for a in W if a != 'ACQUIRE' and abs(d['T'][a]) > fl)
    rules, labels = {}, set()
    for w in WORLDS878:
        key, cross = '%s>%s' % (w, w), [k for k in out if k.endswith('>' + w) and not k.startswith(w + '>')][0]
        d = out[key]; fx = FIXTURE881.get(w, {}); A = ARMS881[key]
        rules[key] = {'fixture_valid': bool(fx.get('valid')), 'norm_T_gt_floor': d['norm_T'] > d['floor'],
                      'T_ACQUIRE_lt_minus_floor': d['T']['ACQUIRE'] < -d['floor'],
                      'norm_T_gt_cross': d['norm_T'] > out[cross]['norm_T'], 'cross_cell': cross}
        rules[key]['pass'] = all(v for k, v in rules[key].items() if k != 'cross_cell')
        ch = {}
        for x in 'ML':
            v_, b_ = A['VIS_' + x], A['C_BLIND_' + x]; nf, nb = A['NATIVE_FULL_' + x], A['NATIVE_C_BLIND_' + x]
            ch[x] = {'argmax': v_['argmax_word'] != b_['argmax_word'],
                     'executable': v_['action'] != b_['action'] and 'INVALID' not in (v_['action'], b_['action']),
                     'abstain': v_['abstain'] != b_['abstain'],
                     'native': nf['argmax_word'] != nb['argmax_word'] and nf['argmax_word'] == v_['argmax_word']}
        rules[key]['changes'] = ch
        rules[key]['path_parity_weak'] = norm(d['kernel']) >= d['norm_T']
    signal = all(rules[k]['pass'] for k in rules)
    any_ = lambda f: any(rules[k]['changes'][x][f] for k in rules for x in 'ML')
    if signal: labels.add('MASKED_PATH_C_SPECIFIC_SIGNAL')
    if any_('argmax'): labels.add('MASKED_PATH_ARGMAX_CHANGE')
    if any_('executable'): labels.add('MASKED_PATH_EXECUTABLE_ACTION_CHANGE')
    if any_('abstain'): labels.add('ABSTAIN_CHANGE')
    if signal and any_('native'): labels.add('NATIVE_UNMASKED_POLICY_CHANGE')
    if any_('argmax') and not any_('native'): labels.add('MASKED_ONLY')
    if any(rules[k]['path_parity_weak'] for k in rules): labels.add('PATH_PARITY_WEAK')
    STATE881['measure'] = {'cells': out, 'rules': rules, 'signal': signal, 'labels': sorted(labels)}
    return STATE881['measure']

# ============================ GATE4: same VIS policy, literal action, real transition, model STORE, parent-aware write ============================
def store_reading881(env, memx, q, act_rows, c_new, e_new):
    X, _ = env['make_x851'](list(env['prompt_ids'](STORE_PROMPT881.format(q=q))),
                            [(SLOTS881['ACTED'], act_rows), (env['C_SLOT851'], c_new), (env['E_SLOT851'], e_new)],
                            SLOTS881['STORE_SUFFIX'])
    L = int(X.shape[0]); ffe881(L + sum(L + len(ids) - 1 for _, ids in WORDS880 if len(ids) > 1))
    r = store_words880(env, memx, X); del X
    return r

def parent_reuse881(env, T, parent, entry, gH, n2, L2, la, X):
    # PARENT_CONDITIONED_REUSE: fresh [B][parent] rebuild (must equal the decision memory seal), then the locked persist878
    # (reload SHA, lower rows bitwise, explicit == native append, probe CAR vs the original timeline). STANDALONE_DRIFT: [B][new].
    out = {}
    H, _, _, _ = decide874(env, gH, X, []); ffe881(int(X.shape[0]) + cont_tokens881())
    cpp = load_exp878(env, parent['entry']); g2 = append_exp878(env, T['m'], cpp); del cpp; ffe881(int(parent['entry']['body_tokens']), 80)
    out['parent_rebuild_seal_equal'] = full_seal881(g2)['all'] == STATE881['cells']['%s>%s' % EXEC_CELL881]['g_full_seal'][EXEC_COND881[0]]
    S = {'side': 'GATE4_NEW', 'n2': n2, 'entry': entry, 'm2': g2, 'X3': X.detach(), 'L2': L2, 'la': la,
         'H': {'p': probs873(H), 'action': H['action']}, 'm': marg877(H)}
    rec = persist878(env, S); ffe881(3 * int(entry['body_tokens']) + int(X.shape[0]) + cont_tokens881())
    out['persist878'] = {k: v for k, v in rec.items() if k != 'arm'}
    out['PARENT_CONDITIONED_REUSE_PASS'] = bool(rec['pass'] and out['parent_rebuild_seal_equal'])
    del g2, S
    cpn = load_exp878(env, entry); gs = append_exp878(env, T['m'], cpn); del cpn; ffe881(int(entry['body_tokens']), 80)
    rs, _, _, _ = decide874(env, gs, X, []); ffe881(int(X.shape[0]) + cont_tokens881()); del gs
    ph, ps = probs873(H), probs873(rs)
    out['STANDALONE_DRIFT'] = {'max_dp_vs_parent_timeline': max(abs(ph[w] - ps[w]) for w in ph), 'action_parent_timeline': H['action'],
                               'action_standalone': rs['action'], 'meaning': 'diagnostic of parent dependence, never a reuse PASS'}
    return out

def gate4_881(env):
    s, r = EXEC_CELL881; key = '%s>%s' % (s, r); T = TGT878[('FORK', r)]; S = SRC878['I867_%s_%s' % (s, EXEC_COND881)]
    Ex = EXEC881.get(T['item']); out = STATE881['gate4']; ck = out['checks'] = {}
    out['claim'] = 'VIS_SELECTED_ACTION_WITH_NATIVE_AUXILIARY'
    out['paths'] = {k: PREREG881['gate4'][k] for k in ('policy_path', 'diagnostic', 'auxiliary_control_path', 'candidate_path',
                                                       'write_cache_path')}
    if Ex is None: raise Gate881('GATE4_RECEIVER_CONTEXT_NOT_CAPTURED')
    guard881('gate4', need_gib=3.0)
    cut, dev, Hd = APPEND873['CUT'], env['DEV'], int(env['H']); q = env['QTEXT841'][T['qid']]; X = T['X']
    c0 = EXEC_COND881[0]; g = G881[key][c0]; C = STATE881['cells'][key]['layout']['C']
    ck['decision_memory_seal_unchanged'] = full_seal881(g)['all'] == STATE881['cells'][key]['g_full_seal'][c0]
    vis = xread881(env, g, X, [C], True, 'GATE4_VIS_recompute')                 # the SAME masked VIS policy, recomputed
    stored = ARMS881[key]['VIS_' + c0]
    ck['VIS_recompute_equals_GATE3_VIS'] = same_reading881(vis, stored)
    out['policy'] = {'path': 'VIS_MASKED_XCAR878', 'action': vis['action'], 'argmax_word': vis['argmax_word'],
                     'abstain': vis['abstain'], 'mass': vis['mass'], 'normalized': vis['normalized'],
                     'sequence_logp': seqlp881(vis)}
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
    X_chk, _ = env['make_x851'](pre, list(Ex['segments']), post); ck['X_rebuilt_equals_receiver_X'] = bool(torch.equal(X_chk, X))
    m2 = [tuple(t.clone() for t in kv) for kv in g]; n2, L2 = length873(env, m2), int(X.shape[0])
    cache = env['cache_build'](list(m2)); ffe881(L2 + cont_tokens881())
    nat = car873(env, cache, X)                               # NATIVE_FULL diagnostic + the parent-conditioned write timeline
    out['native_full_diagnostic'] = {'action': nat['action'], 'argmax_word': nat['argmax_word'],
                                     'delta_native_minus_VIS': {w: seqlp881(nat)[w] - seqlp881(vis)[w] for w in seqlp881(vis)},
                                     'same_action_as_VIS': nat['action'] == vis['action']}
    action = vis['action']; out['native_action'] = action
    out['provenance'] = {'B_full_seal': full_seal881(T['m'])['all'], 'decision_memory_full_seal': full_seal881(g)['all'],
                         'qid_sha256': sha256_bytes864(T['qid'].encode()), 'X_sha256': tsha881(X), 'mounted_before': list(T['mounted']),
                         'path_rows_sha256': [env['stats849'](p['rows'])['sha256'] for p in Ex['path']],
                         'action_token_ids': list(dict(ACTION_IDS867).get(action, [])), 'parent_experience': S['entry']['id']}
    if not all(ck.values()):
        out['executed'] = None; out['status'] = 'TECHNICAL_BLOCK_BEFORE_EXECUTION'; del cache, m2
        raise Gate881('GATE4_POLICY %s' % sorted(k for k, v in ck.items() if not v))
    if action in ('INVALID', 'ACCEPT', 'STOP'):
        out['executed'] = None; out['status'] = 'TERMINAL_NO_ENV_TRANSITION'; out['write'] = 'WRITE_NOT_RUN'; del cache, m2
        return out
    h, kind = hop865(env, T['m'], T['qid'], len(Ex['path']), Ex['path'][-1]['rows'] if Ex['path'] else None)
    ffe881(len(h.get('toks') or []))
    c_rows_sha = env['stats849'](h['rows'].detach().float().cpu())['sha256']
    ck['candidate_text_reproduces_record'] = h['text'] == Ex['candidate_text']
    ck['candidate_rows_sha_reproduces_record'] = c_rows_sha == (Ex['state_sha256'] or {}).get('C')
    out['provenance'].update({'candidate_text': h['text'], 'candidate_rows_sha256': c_rows_sha, 'candidate_memory': 'B'})
    legacy = env['gen851'](g, pre, list(Ex['segments']), post); check_output_h863(legacy, 'T881_CONTROL_ROWS')
    ffe881(L2 + len(legacy.get('toks') or [])); out['auxiliary'] = {'path': 'NATIVE_FULL_AUXILIARY', 'generated_text': legacy['text']}
    own = env['cache_build'](list(kv873(env, cache))); del cache
    A = dict(ACTION_IDS867)[action]; la = len(A); EA = env['embed841'](A)
    forward873(env, own, EA, n2 + L2); keep = kv873(env, own); del own; ffe881(la)
    one = lambda n: torch.ones((1, n), device=dev, dtype=torch.long)
    cl = env['cache_build'](list(m2))
    hx = xspan878(env, cl, X.reshape(1, L2, Hd), one(n2 + L2), 0, cut + 1)
    ha = xspan878(env, cl, EA.reshape(1, la, Hd), one(n2 + L2 + la), 0, cut + 1); ffe881(L2 + la, cut + 1)
    ck['X2A_explicit_lower_KV_bitwise'] = all(torch.equal(x, y) for i in range(cut + 1) for x, y in zip(cache_kv870(cl, i), keep[i]))
    nk = [next_kv878(env, hx, n2), next_kv878(env, ha, n2 + L2)]; ref = keep[cut + 1]
    ck['X2A_h3_next_layer_KV_bitwise'] = all(torch.equal(nk[j][t], ref[t][:, :, a:b]) for j, (a, b) in
                                             enumerate(((n2, n2 + L2), (n2 + L2, n2 + L2 + la))) for t in (0, 1))
    del nk, m2
    if not all(ck.values()):
        out['executed'] = None; out['status'] = 'TECHNICAL_BLOCK_BEFORE_EXECUTION'
        raise Gate881('GATE4_PRE_EXECUTION %s' % sorted(k for k, v in ck.items() if not v))
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
    check_output_h863(ev1, 'T881_EVIDENCE'); ffe881(len(h1.get('toks') or []) + len(ev1.get('toks') or []))
    c_new, e_new = h1['rows'].detach().float().cpu(), ev1['rows'].detach().float().cpu()
    out['model_observation'] = {'label': 'MODEL_OBSERVATION', 'hop_text': h1['text'], 'hop_kind': kind1, 'rows': int(c_new.shape[0])}
    out['model_evidence'] = {'label': 'MODEL_EVIDENCE', 'text': ev1['text'], 'rows': int(e_new.shape[0])}
    out['write'] = 'WRITE_NOT_RUN'
    if not (c_new.ndim == 2 and c_new.shape[0] and e_new.ndim == 2 and e_new.shape[0]):
        out['store'] = {'decision': None, 'why': 'EMPTY_OBSERVATION_ROWS'}; del keep, cl, hx, ha; return out
    sr = store_reading881(env, obs_mem, q, env['embed841'](A).detach().float().cpu(), c_new, e_new)
    out['store'] = {'decision': sr['decision'], 'mass': sr['mass'], 'normalized': sr['normalized']}
    if sr['decision'] != 'STORE':
        out['write'] = 'NO_STORE_' + str(sr['decision']); del keep, cl, hx, ha; return out
    n1 = n2 + L2 + la; P = int(env['P'])
    Y, _ = env['make_x851'](env['C_SLOT851'], [([], c_new), (env['E_SLOT851'], e_new)], []); body = int(Y.shape[0])
    own2 = env['cache_build'](list(keep)); forward873(env, own2, Y, n1); gH = kv873(env, own2); del own2
    h3c = xspan878(env, cl, Y.reshape(1, body, Hd), one(n1 + body), 0, cut + 1); ffe881(body, 80 + cut + 1)
    ck['C_explicit_lower_KV_bitwise'] = all(torch.equal(a_[:, :, n1:], b_[:, :, n1:n1 + body]) for i in range(cut + 1)
                                            for a_, b_ in zip(cache_kv870(cl, i), gH[i]))
    ck['C_h3_next_layer_KV_bitwise'] = all(torch.equal(a_, b_[:, :, n1:n1 + body]) for a_, b_ in zip(next_kv878(env, h3c, n1), gH[cut + 1]))
    if not all(ck.values()):
        out['write'] = 'WRITE_GATE_FAILED'; raise Gate881('GATE4_C_GATES %s' % sorted(k for k, v in ck.items() if not v))
    prov = {'namespace': 'REAL', 'test': 'TEST881', 'requires_parent': True, 'parent_experience': S['entry']['id'],
            'parent_experience_sha256': S['entry']['sha256'], 'receiver_item': T['item'], 'receiver_step': Ex['steps'],
            'receiver_B_full_seal': out['provenance']['B_full_seal'], 'decision_memory_full_seal': out['provenance']['decision_memory_full_seal'],
            'source_prefix_tokens': n2, 'source_storage_positions': [n2, n1 + body], 'cartridge_positions': [P, P + n1 + body - n2],
            'cut': cut, 'qid_sha256': out['provenance']['qid_sha256'], 'action': action, 'action_token_ids': list(A),
            'effect': eff.get('effect'), 'chosen': eff.get('chosen'), 'C_kind': 'NEXT_MODEL_OBSERVATION',
            'spans_body': {'X2': [0, L2], 'A': [L2, L2 + la], 'C': [L2 + la, L2 + la + body]},
            'decision_policy_path': 'VIS_MASKED_XCAR878', 'auxiliary_control_path': 'NATIVE_FULL_GEN851',
            'write_cache_path': 'PARENT_CONDITIONED_NATIVE_WRITE', 'store_reading': {'decision': sr['decision'], 'mass': sr['mass']},
            'weights_digest': WEIGHTS0_878, 'engine_git_blob': ENGINE_BLOB881, 'head': HEAD881,
            'cell_git_blob': STATE881['source'].get('executed_cell_git_blob'), 'layout_sha256': STATE881['cells'][key]['layout']['sha256'],
            'contains': 'native h3 + L0-3 K/V of [X2][A][C] only; meaningful only after [B][parent]'}
    eid = 'X881_' + sha256_bytes864(_j881.dumps(prov, sort_keys=True).encode())[:12]
    def write(d):
        global EXP_DIR878
        old, EXP_DIR878 = EXP_DIR878, REAL_GATE4_DIR881
        try: return write_exp878(env, eid, gH, torch.cat([hx, ha, h3c], dim=1), n2, n1 + body, L2 + la, prov)
        finally: EXP_DIR878 = old
    try:
        res = STORE881.commit(eid, str(REAL_GATE4_DIR881), write, lambda e: load_exp878(env, e) and None)
    except CommitUncertain881 as exc:
        out['write'] = 'COMMIT_UNCERTAIN'; out['commit_error'] = str(exc)
        out['recovery'] = STORE881.recover(lambda e: load_exp878(env, e) and None)
        raise Gate881('GATE4_COMMIT_UNCERTAIN (recovered: %s)' % _j881.dumps(out['recovery'], default=str))
    entry = res['entry']; out['write'] = 'REAL_WRITE_COMMITTED'; STATE881['budget']['ssd_bytes'] += int(entry['bytes'])
    out['written'] = {k: entry[k] for k in ('id', 'file', 'sha256', 'bytes', 'body_tokens', 'roundtrip_K_rel', 'pre_C_seal')}
    out['written']['generation'] = res['generation']
    if entry['roundtrip_K_rel'] > ROPE_TOL878: raise Gate881('GATE4_ROUNDTRIP %.3e' % entry['roundtrip_K_rel'])
    del keep, cl, hx, ha, h3c, Y; gc.collect(); torch.cuda.empty_cache()
    guard881('parent_reuse', need_gib=2.0)
    out['reuse'] = parent_reuse881(env, T, S, entry, gH, n2, L2, la, X); del gH
    if not out['reuse']['PARENT_CONDITIONED_REUSE_PASS']: raise Gate881('PARENT_CONDITIONED_REUSE_FAIL')
    gc.collect(); torch.cuda.empty_cache()
    return out

def eval_gate4_881(env, by_key):
    # OFFLINE: the outcome is read from the executor state only; the model observation is a separate diagnostic
    G = STATE881['gate4']
    if not G.get('executed'): return
    r = EXEC_CELL881[1]; spec = by_key[(int(r), 'FORK')]; w = world867(env, spec); kind = {v: k for k, v in w['ids'].items()}
    e = G['environment_effect']; mk = kind.get(e.get('chosen'))
    node = env['node851'](e['path_after'][-1], w) if (e.get('effect') == 'POINTER_ADVANCED' and e.get('path_after')) else None
    supported = (e.get('effect') == 'MOUNTED' and mk == 'second') or (e.get('effect') == 'UNMOUNTED' and mk in ('fork', 'decoy')) or \
                (e.get('effect') == 'POINTER_ADVANCED' and node == 'middle')
    rec = STATE881['targets_static']['receivers'][r]
    G['offline'] = {'executor_effect': e.get('effect'), 'card_kind': mk, 'advanced_node_class': node, 'supported': supported,
                    'model_observation_class_diagnostic': env['node851'](G['model_observation']['hop_text'], w),
                    'recorded_no_memory_execution': {'action': rec['recorded_action'], 'effect': rec['recorded_effect'],
                                                     'effect_card_kind': kind.get((rec['recorded_effect'] or {}).get('chosen'))},
                    'meaning': 'single execution: descriptive, no VIS > BLIND outcome claim'}

# ============================ replay tap: TEST878 probe + the receiver context for GATE4 ============================
def probe881(env, ctx, record, state, label):
    probe878(env, ctx, record, state, label)
    side = ctx['spec']['item']
    if side.endswith('_FORK') and ctx['steps'] == FORK_STEP878 and side.split('_')[1] == EXEC_CELL881[1]:
        EXEC881[side] = {'spec': {k: (list(v) if isinstance(v, (list, tuple)) else v) for k, v in ctx['spec'].items() if k != 'xray'},
                         'segments': [(list(s_), r_.detach().float().cpu().clone()) for s_, r_ in state['segments']],
                         'path': [{'rows': p['rows'].detach().float().cpu().clone(), 'text': p['text']} for p in ctx['path']],
                         'steps': ctx['steps'], 'candidate_text': record.get('candidate_text'),
                         'state_sha256': record.get('state_sha256')}

# ============================ verdict and report ============================
def verdict881():
    blocks = list(STATE881['blocks']); reps = {r_.get('item'): r_ for r_ in STATE870['replays']}
    for side, s_ in STATE881['sides'].items():
        if s_.get('error'): blocks.append('POINT_ERROR:' + side)
        if reps.get(side, {}).get('ok') is not True: blocks.append('REPLAY_NOT_EXACT:' + side)
    labels = []
    if blocks: v = 'TECHNICAL_BLOCK'
    elif not STATE881.get('measure'): v = 'NOT_RUN'
    else:
        m = STATE881['measure']; labels = list(m['labels'])
        if not m['signal']: labels.insert(0, 'PREREG_SEMANTIC_FAIL')
        g4 = STATE881['gate4']
        if g4.get('status') == 'TERMINAL_NO_ENV_TRANSITION': labels.append('TERMINAL_NO_ENV_TRANSITION')
        if g4.get('offline'): labels.append('BEHAVIORAL_OUTCOME' if g4['offline']['supported'] else 'BEHAVIORAL_OUTCOME_NOT_SUPPORTED')
        if g4.get('write'): labels.append(g4['write'])
        if (g4.get('reuse') or {}).get('PARENT_CONDITIONED_REUSE_PASS'): labels.append('PARENT_CONDITIONED_REUSE_PASS')
        if g4.get('claim') and g4.get('executed'): labels.append(g4['claim'])
        v = 'MASKED_PATH_C_SPECIFIC_SIGNAL' if m['signal'] else 'PREREG_SEMANTIC_FAIL'
    STATE881['verdict'] = {'verdict': v, 'labels': labels, 'blocks': blocks, 'not_run': STATE881['not_run'],
                           'never_reported': PREREG881['never_reported_here'], 'limits': PREREG881['limits']}
    return STATE881['verdict']

def report881():
    W = [w for w, _ in ACTION_IDS867]
    print('=' * 112)
    print('TEST881 PILOT-0 r2 | GPU %s | head %s | cell %s | prereg %s' % (CC_GPU.get('name'), HEAD881[:12],
          STATE881['source'].get('executed_cell_git_blob'), PREREG_SHA881[:16]))
    print('SELFTESTS %s' % _j881.dumps({k: (v if k != 'store' else {kk: vv['pass'] for kk, vv in v.items()})
                                       for k, v in STATE881['selftests'].items()}, sort_keys=True))
    print('FIXTURES %s' % _j881.dumps(STATE881.get('fixtures', {}).get('rows'), sort_keys=True))
    for r, R in STATE881['receivers'].items():
        print('RECEIVER R%s %s memory=%s X=%s OFF0_explicit==native %s' % (r, R['item'], R['memory_tokens'], R['X_len'],
              R['OFF0_explicit_equals_native']))
    for key, G in STATE881['cells'].items():
        print('CELL %s %-9s gate2=%s layout E=%s C=%s X=%s C_rows_differ=%s' % (key, G['relation'], G.get('gate2_pass'),
              G['layout']['E'], G['layout']['C'], G['layout']['X'], _j881.dumps({k: v for k, v in G['C_rows_differ'].items() if k != 'C_cartridge_sha'})))
        print('    GATE2 %s' % _j881.dumps(G['gate2'], sort_keys=True))
        for name, a in sorted(ARMS881.get(key, {}).items()):
            print('    %-18s %-9s %s' % (name, a['action'], ' '.join('%s=%.4f' % (w_, (a['normalized'] or {}).get(w_, float('nan'))) for w_ in W)))
    m = STATE881.get('measure') or {}
    for key, d in (m.get('cells') or {}).items():
        print('MEASURE %s |T|=%.4f floor=%.5f T=%s exploratory=%s' % (key, d['norm_T'], d['floor_used'],
              _j881.dumps({a: round(x, 4) for a, x in d['T'].items()}), d['exploratory_actions_beyond_floor']))
        for extra in ('delta_C_M', 'delta_C_L', 'generic', 'slot', 'kernel', 'repeat'):
            if extra in d: print('    %-9s %s' % (extra, _j881.dumps({a: round(x, 5) for a, x in d[extra].items()})))
    print('RULES %s' % _j881.dumps(m.get('rules'), sort_keys=True))
    print('GATE4 %s' % _j881.dumps(STATE881.get('gate4'), sort_keys=True, default=str)[:4000])
    b = STATE881['budget']
    print('BUDGET ADAPTER_FFE_LOWER_BOUND=%.1f/%.0f TOTAL_GPU_WORK_NOT_FULLY_ACCOUNTED calls849=%s ssd_bytes=%d peak_alloc=%.2f GiB '
          'peak_reserved=%.2f GiB' % (b['adapter_ffe_lower_bound'], FFE_MAX881, env881['CALLS849'] if 'env881' in globals() else None,
                                      b['ssd_bytes'], b['peak_alloc_gib'], b['peak_reserved_gib']))
    v = STATE881['verdict'] or {}
    print('TEST881 VERDICT %s | labels %s | blocks %s | not_run %s' % (v.get('verdict'), v.get('labels'), v.get('blocks'), v.get('not_run')))
    print('LIMITS: %s' % '; '.join(PREREG881['limits']))
    print('status %s | wall %.0f s | GPU_EXECUTION_NOT_VERIFIED_BY_AUTHOR' % (STATE881['status'], time.perf_counter() - T_START878))
    print('=' * 112)

# ============================ single cell execution ============================
FIXTURE881 = {}
T_START878 = time.perf_counter()
try:
    STATE881['status'] = 'GATE0_SOURCE'; capture_source881()
    json_write864('881_prereg.json', {'prereg': PREREG881, 'sha256': PREREG_SHA881, 'before_model_load': True})
    line881('GATE0 PREREG', PREREG_SHA881, 'cell', STATE881['source']['executed_cell_git_blob'])
    selftest_firewall881(); selftest_store881(); selftest_mask881()
    line881('GATE0 CPU SELFTESTS PASS', _j881.dumps({k: list(v) for k, v in STATE881['selftests'].items()}))
    du = _s881.disk_usage(str(ROOT864)); STATE881['budget']['disk_free_gib'] = round(du.free / 2**30, 1)
    if du.free / 2**30 < DISK_MIN_GIB881: raise Gate881('DISK_FREE %.1f GiB' % (du.free / 2**30))
    load_sources865(); log879 = select_locked881(); xray_point870 = probe881
    source_audit878(); load878(); STATE881['ref873'] = ref873_874(RAW_SOURCES864['873.log'].decode())
    STATE881['ref879'] = ref879_881(log879)
    feasibility_audit864(); audit_contracts865(); load_spine864(); REFS881 = load_records870()
    STATE881['targets_static'] = targets881(REFS881)
    STATIC_T2_SHA878 = {s: [e['record'] for e in REFS881[(s, ARM878)]['events'] if e['type'] == 'CONTROL'][PRE_STEP878 - 1]['state_sha256']
                        for s in SOURCES878}
    line881('GATE0 SOURCE PASS', _j881.dumps({k: v for k, v in STATE881['source'].items() if k != 'reused'}, sort_keys=True))
    STATE881['status'] = 'GATE0_PREFLIGHT'; assert CC_GPU_OK, ('GPU_PRECHECK', CC_GPU)
    env881, original_error881, original_trace881, reproduction881 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace881; TWO_JOB_VERIFICATION864 = verify_two_job859(env881, original_trace881)
    assert_hook_free859(env881, 'T881_before_native'); install_offline_evaluator859(env881)
    native881 = native_sequences860(env881); NATIVE_REGRESSION864 = native_regression864(env881, native881)
    verify_864_reference865(NATIVE_REGRESSION864); ANALYSIS864 = run_analysis863(env881, native881)
    assert len(STATE863['restores']) == 3 and all(r_['exact'] for r_ in STATE863['restores'])
    digest881 = records_digest861(env881); null_seal881 = physical_seal863(env881, env881['MEMNULL841'])
    runtime_contracts865(env881); runtime_preflight865(env881, reproduction881); rearm_budget865(env881); make_slots866(env881)
    SLOTS867['PREV_EVALUATION'] = list(env881['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env881); resolve_append873(env881); api877(env881); WEIGHTS0_878 = weights_digest877(env881)
    chunk881 = [ns['CHUNK'] for ns in (env881['build_fusion'].__globals__, env881) if 'CHUNK' in ns]
    assert chunk881 and int(chunk881[0]) > 0 and all(k in env881 for k in ('P', 'to_gpu', 'kv_digest', 'entries', 'make_x851',
        'gen851', 'gen849', 'C_SLOT851', 'E_SLOT851', 'EVIDENCE851', 'ANSWER_SUFFIX851', 'REVIEW_SUFFIX851', 'stats849')), 'ENGINE_NAMESPACE'
    EXP878['CHUNK'] = int(chunk881[0])
    REAL_DIR881 = ROOT864 / 'REAL_NAMESPACE_881'; SHADOW_DIR881 = ROOT864 / 'SHADOW_NAMESPACE_881'
    EXP_DIR878 = REAL_DIR881 / 'replayed_sources'; REAL_GATE4_DIR881 = REAL_DIR881 / 'gate4'
    for d_ in (EXP_DIR878, REAL_GATE4_DIR881, SHADOW_DIR881): d_.mkdir(parents=True, exist_ok=False)
    STORE881 = RealStore881(REAL_DIR881, [EXP_DIR878, REAL_GATE4_DIR881])
    SLOTS881 = {k: list(env881['tok'](v, add_special_tokens=False).input_ids) for k, v in SLOT_TEXT881.items()}
    WORDS880 = [(w_, list(env881['tok'](' ' + w_, add_special_tokens=False).input_ids)) for w_ in ('STORE', 'DISCARD')]
    assert all(SLOTS881.values()) and WORDS880[0][1][0] != WORDS880[1][1][0], ('STORE_TOKENS', WORDS880)
    STATE881['tokens'] = {'actions': {w_: ids for w_, ids in ACTION_IDS867}, 'store_words': dict(WORDS880),
                          'sha256': sha256_bytes864(_j881.dumps([ACTION_IDS867, WORDS880], sort_keys=True).encode())}
    assert not any(p.requires_grad for p in env881['model'].parameters()), 'NOT_FROZEN'
    assert_hook_free859(env881, 'T881_before_points')
    line881('GATE0 PREFLIGHT PASS', _j881.dumps(STATE881['api'], sort_keys=True), 'CHUNK=%d P=%d' % (EXP878['CHUNK'], int(env881['P'])),
            'model_load_s=%.0f' % (time.perf_counter() - T_START878))
    STATE881['status'] = 'GATE1_PHYSICAL'; T0_865 = time.perf_counter(); by_key881 = build_specs869(env881)
    plan881 = [(s_, {PRE_STEP878: 'T2_EXPERIENCE', POST_STEP878: 'T3_EXPERIENCE'}) for s_ in SOURCES878] + \
              [(s_, {FORK_STEP878: 'T1_TARGET'}) for s_ in FORKS878]
    for side881, tg881 in plan881:
        guard881('replay_' + side881)
        rep881 = run_replay870(env881, {'id': side881, 'item': side881, 'arm': ARM878, 'targets': tg881}, by_key881, REFS881)
        T2_KEEP878.pop(side881, None)
        if not rep881['ok']: STATE881['blocks'].append('REPLAY_NOT_EXACT:' + side881)
    if STATE881['blocks']: raise Gate881('GATE1_REPLAY %s' % STATE881['blocks'])
    json_write864('881_experience_manifest.json', jsafe878(STATE881['experience']))
    sources881(env881); fixture_seal881(env881, by_key881)
    STATE881['store']['recovery_after_gate1'] = STORE881.recover(lambda e: load_exp878(env881, e) and None)
    STATE881['status'] = 'GATE2_3_CELLS'; receivers881(env881)
    for s881, r881 in CELLS881: cell881(env881, s881, r881)
    measure881()
    STATE881['status'] = 'GATE4_EXECUTION'
    try:
        gate4_881(env881); eval_gate4_881(env881, by_key881)
    finally:
        G881.clear(); gc.collect(); torch.cuda.empty_cache()
    STATE881['store']['recovery_final'] = STORE881.recover(lambda e: load_exp878(env881, e) and None)
    hook881 = hook_audit859(env881, 'T881_final')
    if records_digest861(env881) != digest881 or physical_seal863(env881, env881['MEMNULL841']) != null_seal881 or \
            hook881['hook_count'] or hook881['transformers_output_capturing_installed'] or weights_digest877(env881) != WEIGHTS0_878:
        STATE881['blocks'].append('POST_RUN_INTEGRITY')
    for r881 in WORLDS878:
        if full_seal881(TGT878[('FORK', r881)]['m'])['all'] != STATE881['receivers'][r881]['B_full_seal']:
            STATE881['blocks'].append('RECEIVER_B_FINAL_SEAL R' + r881)
    STATE881['status'] = 'COMPLETE'; verdict881()
except Budget881 as exc:
    STATE881['error'] = str(exc); STATE881['not_run'].append('NOT_RUN_AT_%s: %s' % (STATE881['status'], exc))
    STATE881['status'] = 'NOT_RUN_AT_' + str(STATE881['status']); verdict881()
except Partial878 as exc:
    STATE881['error'] = str(exc); STATE881['not_run'].append('NOT_RUN_AT_%s (TEST878 guard): %s' % (STATE881['status'], exc))
    STATE881['status'] = 'NOT_RUN_AT_' + str(STATE881['status']); verdict881()
except BaseException as exc:
    STATE881['error'] = '%s: %s' % (type(exc).__name__, exc); STATE881['traceback'] = traceback.format_exc()
    STATE881['blocks'].append('%s: %s' % (STATE881['status'], STATE881['error'][:300]))
    STATE881['status'] = 'FAILED_AT_' + str(STATE881['status'])
    STATE881['verdict'] = {'verdict': 'TECHNICAL_BLOCK', 'labels': [], 'blocks': list(STATE881['blocks']),
                           'not_run': STATE881['not_run'], 'source_head': HEAD881, 'engine_blob': ENGINE_BLOB881}
    (ROOT864 / '881_traceback.txt').write_text(STATE881['traceback'], encoding='utf-8')
    print('TEST881 ERROR', STATE881['error'][:300], '| full traceback:', ROOT864 / '881_traceback.txt', file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        json_write864('881_traces.json', TRACES881)
        json_write864('881_result.json', jsafe878(dict(STATE881, replays=STATE870['replays'], prereg=PREREG881)) if 'jsafe878' in globals()
                      else json.loads(json.dumps(dict(STATE881, replays=STATE870['replays']), default=str)))
    except Exception as exc: print('RESULT_WRITE_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    try: report881()
    except Exception as exc: print('REPORT_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE881['suffix'], 'test870.py:suffix', 'exec'), globals())
