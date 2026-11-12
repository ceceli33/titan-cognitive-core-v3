# AKBASCORE SILICON HIPPOCAMPUS — TEST880 — NCRA: NATIVE CONSEQUENCE RETRIEVAL AND APPRAISAL (closed-loop engine)
# REVISION r2 (2026-11-12) of 880.py git blob 22d22530: A1 879.log marker, A2 NOT_APPLICABLE rows, A3 empty pre ids in the
# C path; offline verdict/correction tightened (B1/B2); placeholder, round-trip and open-frame provenance (C1-C5).
# Runtime decision flow, CAR, routing, physical capture/write and every gate are unchanged from r1.
# One A100-SXM4-80GB Colab cell. Frozen Qwen2.5-72B-Instruct NF4, BF16. Locked engine test870.py (e322ed8) + locked 878.py.
# ENGINE (one loop, every decision is the model's):
#   OBSERVE (hop865 + evidence) -> close the open episode: comparison U and native STORE/DISCARD -> deficit D -> evaluation
#   -> APPRAISE every currently executable action (expected consequence P_a, relation852(P_a, G)) -> CHOOSE (car867 +
#   reading867) -> EXECUTE the literal word (execute866 for ADVANCE/BACKTRACK; ACQUIRE/REJECT: model direction rows ->
#   hook-free layer-3 query -> PEAK50 over environment cards + experience cartridges + NULL -> one physical mount) -> repeat.
#   A stored experience is a CUT3 cartridge [X2][A][C]: X2 = the real decision input, A = the executed action tokens,
#   C = the real consequence (the mounted card for ACQUIRE of a card, otherwise the rows of the next real observation).
# Never: weight writes, training, hooks, output_hidden_states/attentions, logit edits, action forcing, text replay of
# episodes, labels in the loop. The offline evaluator runs only after every loop has ended.
import ast as _a880, hashlib as _h880, json as _j880, random as _rnd880, re as _r880, urllib.request as _u880
ENGINE_URL880 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB880, MARKER880 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', 'AKBASCORE SILICON HIPPOCAMPUS — TEST880'

def blob880(raw):
    return _h880.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()

def engine_parts880():
    with _u880.urlopen(_u880.Request(ENGINE_URL880, headers={'User-Agent': 'AKBASCORE-TEST880'}), timeout=240) as r:
        raw = r.read()
    assert blob880(raw) == ENGINE_BLOB880, ('ENGINE_BLOB_MISMATCH', blob880(raw))
    text = raw.decode('utf-8'); _a880.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST880_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST880_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST880_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('880_engine.log', '880_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST880_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '880_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '880_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST880_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old)
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL880, 'git_blob': blob880(raw), 'sha256': _h880.sha256(raw).hexdigest()}

try:
    ENGINE880, ENGINE_INFO880 = engine_parts880()
except BaseException as _exc880:      # console capture starts inside the engine prefix: keep a local record of this failure
    import time as _t880, traceback as _tb880
    _p880 = '/content/TEST880_PRE_ENGINE_ERROR_%s.txt' % _t880.strftime('%Y%m%dT%H%M%SZ', _t880.gmtime())
    try:
        with open(_p880, 'w', encoding='utf-8') as _f880: _f880.write(_tb880.format_exc())
    except OSError: _p880 = 'NOT_WRITTEN'
    print('TEST880 PRE-ENGINE ERROR (before console capture):', type(_exc880).__name__, _exc880, '| traceback:', _p880)
    raise
exec(compile(ENGINE880['prefix'], 'test870.py:prefix', 'exec'), globals())
exec(compile(ENGINE880['body'], 'test870.py:engine', 'exec'), globals())
print('TEST880 ENGINE', _j880.dumps(ENGINE_INFO880, sort_keys=True))

# ============================ locks, reused TEST878 code, constants ============================
LOCKS864.update({'test870.py': ENGINE_BLOB880, 'Test870.log': 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc',
                 '873.py': '2e44affa5e0dd462155fb265c331270fb8e7b7e1', '873.log': '1c9eb9fca173003eaf45bc7726af13c2817324b7',
                 '874.py': '12172001ba3696ad91087a8b34d7995728259e47', '874.log': '1229e3b70440e3887ccf1bd7e3bad51f900f5313',
                 '877.py': 'a6aa7648e0fb765a8dc9b56b8f79b4dcef5fc772', '877.log': 'c4eb58021ed827fb13d5c15fee7c18541f6d4604',
                 '878.py': '7842e8675544a0328e3552f059c81b7750068a82', 'Test_878_log2.log': '2bfc7adc2a8f718c012a6d722a9e0a04a72cbedd',
                 '879.py': '92f9eb665173986b6c98b42f07eefb3249c861d4', '879.log': 'c1205bc082fb69c68b9f9f4e290808a0dec71fa8'})
TEST878_PREREG880 = '0555ab01d436c0df7e8e1be21aea3170ac0a50d799a528796212298a48dc4103'
_a878, _h878, _j878 = _a880, _h880, _j880
ENGINE_BLOB878 = ENGINE_BLOB880
CONSTS878 = ('TEST877_CELL_BLOB878', 'TEST877_PREREG_DEPS878', 'TEST870_MINUTES', 'WORLDS878', 'SOURCES878', 'FORKS878',
             'SIDES874', '_h877', 'ARM878', 'FUNCS873', 'FUNCS874', 'FUNCS877', 'ROPE_TOL878', 'HARD_MIN878', 'PREREG878')
FUNCS878 = ('Persist878', 'line878', 'source_audit878', 'load878', 'xspan878', 'next_kv878', 'tsha878', 'write_exp878',
            'load_exp878', 'append_exp878', 'jsafe878')
BANNED880 = {'register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook', 'output_hidden_states',
             'output_attentions', 'install_all_output_capturing_hooks', 'backward', 'requires_grad_', 'zero_grad',
             'DirectCut3', 'native_append_direct'}
# names the loop must never read (offline labels); checked by AST over every runtime function below
ORACLE880 = {'supported851', 'node851', 'correct867', 'success867', 'OFFLINE880', 'evaluate880', 'world867'}
ORACLE_KEYS880 = {'second', 'changed', 'mirror', 'decoy', 'fork', 'third', 'condition', 'world_index', 'middle', 'changed_end',
                  'fork_end', 'decoy_end', 'start', 'ids', 'world'}
RUNTIME880 = ('legal880', 'query880', 'route880', 'rebuild880', 'execute880', 'goal880', 'surprise880', 'store_words880',
              'capture880', 'close_frame880', 'step880', 'loop880')
HORIZON880, HARD_MIN880, LOOP_MIN880, FREE_MIN_GIB880, PARITY_TOL880 = 8, 80.0, 6.0, 8.0, 1e-3
SEED880, WORLDS880 = 8802026, 3
SLOT_TEXT880 = {'GOAL': 'Goal numerical state:', 'DEFICIT': 'Missing information numerical state:',
                'SURPRISE': 'Expectation comparison numerical state:', 'EXPECT': 'Expected consequence numerical state:',
                'OPTION': 'Possible action numerical state:', 'ACTED': 'Executed action numerical state:',
                'GOAL_SUFFIX': '\nGoal:', 'DEFICIT_SUFFIX': '\nMissing:', 'APPRAISE_SUFFIX': '\nExpected consequence:',
                'SURPRISE_SUFFIX': '\nComparison:', 'STORE_SUFFIX': '\nMemory decision:'}
for _w880 in ('ADVANCE', 'ACQUIRE', 'REJECT', 'BACKTRACK', 'ACCEPT', 'STOP'):
    SLOT_TEXT880['OPT_' + _w880] = 'Option %s expected consequence numerical state:' % _w880
PROMPT880 = {
    'GOAL': 'Question: {q}\nBefore reading any evidence, state the goal of this question: the final node that must be '
            'reached and the link that leads to it. If it cannot be named yet, reply UNKNOWN.',
    'DEFICIT': 'Question: {q}\nThe numerical context contains the latest candidate, the independent answer from the mounted '
               'physical evidence, their relation, the current reasoning node when reasoning has advanced, your goal and, '
               'when one exists, your comparison of the last expectation with the last observation. Name the single node '
               'whose outgoing record is still missing for the goal, or NONE if nothing is missing.',
    'APPRAISE': 'Question: {q}\nThe numerical context contains the latest candidate, the independent answer, their relation, '
                'the current reasoning node when reasoning has advanced, your goal, what is missing, and one possible '
                'action. Do not decide. Predict the immediate consequence of executing that action now: the node reasoning '
                'would stand on, or the record that would be obtained or removed, or UNKNOWN.',
    'SURPRISE': 'Question: {q}\nThe numerical context contains your expected consequence before your last action, the '
                'candidate and the independent answer actually observed after it, and your goal. Compare expectation and '
                'observation. Reply MATCH or MISMATCH, then name the node that differs.',
    'STORE': 'Question: {q}\nThe numerical context contains your expected consequence before your last action, the action you '
             'executed, the candidate and the independent answer actually observed after it, your comparison and your '
             'goal. Decide whether this action and its real consequence should be kept as a physical experience for '
             'future decisions. Reply with exactly one word: STORE or DISCARD.'}
CONTROL_INSERT880 = ('The numerical context also contains your goal, what is missing, your comparison of the last expectation '
                     'with the last observation when one exists, and for every action that can be executed now its expected '
                     'consequence. Decide the next reasoning action.')
STORE_WORDS880 = ('STORE', 'DISCARD')
# loop plan: (name, world, condition, catalog view, store enabled). Views are built from catalog snapshots, never from labels.
PLAN880 = (('L1_A_LIVE', 0, 'LIVE', 'FULL', True), ('L2_B_LIVE', 1, 'LIVE', 'FULL', True),
           ('L3_A_FORK', 0, 'FORK', 'FULL', True), ('L4_A_FORK_NO_MEMORY', 0, 'FORK', 'NO_MEMORY', False),
           ('L5_A_FORK_REMOVAL', 0, 'FORK', 'REMOVAL', False), ('L6_A_MISSING', 0, 'MISSING', 'FULL', True),
           ('L7_A_FORK_WRONG_MEMORY', 0, 'FORK', 'WRONG_MEMORY', False), ('L8_A_FORK_KEY_SHUFFLE', 0, 'FORK', 'KEY_SHUFFLE', False))
PREREG880 = {
    'goal': 'first closed-loop native engine: goal, deficit, appraisal of executable actions, native choice, literal execution, '
            'real observation, comparison, native STORE/DISCARD of a physical CUT3 [X2][A][C] experience, self-addressed reuse',
    'model': 'frozen Qwen2.5-72B-Instruct NF4 / BF16; one load; no weight write, no hook, no text replay, no labels in the loop',
    'retrieval': 'ACQUIRE/REJECT: model direction rows (direction866) -> index_embeds841 -> explicit layers 0..3 (xspan878) over '
                 'MEMNULL841 -> centred unit H3 query -> peak50_841 against environment-card keys, experience keys (same '
                 'construction: unit(h[P:] - MU841)) and a NULL key (MUE845 through the same path); NULL wins ties; top-3 and '
                 'NULL score logged; one candidate mounted; one active experience; candidates rejected in this loop excluded',
    'router_sees': 'opaque ids, numerical keys, mounted / rejected / capacity state; never world, condition, role, answer, '
                   'recency or utility',
    'appraisal': 'for every executable action (sandbox legality only) gen851 predicts the immediate consequence P_a; '
                 'R_a = relation852(P_a, G); [embed(a), P_a, R_a] enter the final car867 context in ACTIONS866 order',
    'store': 'two-word native reading (STORE / DISCARD) after the next real observation; writer only on STORE; '
             'C = mounted card (ACQUIRE of a card, TEST878 path) or the next real observation rows; P_a never written as C',
    'plan': [list(p) for p in PLAN880],
    'views': {'FULL': 'every verified experience in the catalog', 'NO_MEMORY': 'no experience',
              'REMOVAL': 'catalog snapshot before L3 minus every experience L3 mounted (NOT_APPLICABLE if none)',
              'WRONG_MEMORY': 'snapshot before L3 minus the experiences stored in world-A loops (NOT_APPLICABLE if none remain)',
              'KEY_SHUFFLE': 'snapshot before L3 with experience keys rotated by one (NOT_APPLICABLE below two)'},
    'counterfactual_loops_store': False,
    'horizon': '%d executed actions; time/VRAM/INVALID/HORIZON are mechanical ends, never a model STOP; the frame of the '
               'last action before HORIZON has no observed consequence: OPEN_AT_HORIZON, never written, never counted' % HORIZON880,
    'hook_scope': 'new code (query880, capture880, close_frame880) is hook-free: explicit layer statements, no forward hooks, '
                  'no output_hidden_states; locked reused paths (mount865/native_append_direct, physical_commit forging, '
                  'the pointer_query865 parity reference) keep their locked DirectCut3 method swap; not rewritten here',
    'placeholders': 'empty goal rows or empty P_a are replaced by MUE845 and flagged (goal_placeholder, P_placeholder); a '
                    'placeholder is never reported as a prediction or as an observed consequence',
    'fallback': 'top-3 sequential applicability fallback NOT enabled in this run (only after an observed rank-1 failure)',
    'verdict': {'TECHNICAL_BLOCK': 'preflight, parity, integrity or engine error',
                'PARTIAL': 'L3 (the full-catalog FORK loop) did not run',
                'CLOSED_LOOP_NO_STORE': 'loops ran; the model never chose STORE (or no write passed its gates)',
                'CLOSED_LOOP_NO_SELF_REUSE': 'experiences stored; L3 never physically mounted one stored by another loop',
                'CLOSED_LOOP_REUSE_INCONCLUSIVE_UNMATCHED_PREFIX': 'L3 reused; no executed control (L4/L5) reproduces the L3 decision '
                                                                  'inputs bitwise up to and including the reuse step',
                'CLOSED_LOOP_REUSE_NO_BEHAVIOUR_CHANGE': 'L3 reused; a matched control executes the same actions and terminal '
                                                         'decision after the reuse step',
                'CLOSED_LOOP_REUSE_BEHAVIOUR_CHANGE_UNSUPPORTED': 'matched control diverges after the reuse step, but the L3 '
                                                                  'end is not an offline-supported success',
                'CLOSED_LOOP_MEMORY_DEPENDENT_BEHAVIOUR': 'L3 physically mounted a self-addressed experience; a matched control '
                                                          '(L4 no memory or L5 that experience removed) has bitwise-equal X up '
                                                          'to and including the reuse step, then a different executed model action '
                                                          'or model terminal decision; and L3 ends in an offline-supported success'},
    'verdict_rules': ['the primary reuse reference is the first L3 MOUNTED_EXPERIENCE of an experience stored by another loop',
                      'L6 reuse is reported separately (REUSE_OBSERVED_NO_MATCHED_CONTROL); never combined with L3 differences',
                      'mount/effect label differences alone are never behavioural success',
                      'mechanical success (STORE written, SSD reload, self-addressed mount) is reported apart from behaviour',
                      'evaluator labels are read only after every loop has ended'],
    'correction_rule': 'offline only: after an adverse hop (fork_end / decoy_end / UNKNOWN / OTHER), a correction needs a real '
                       'state transition: BACKTRACK removing that node from the path, REJECT unmounting the card that produces '
                       'that node, or ACQUIRE mounting followed by a hop of a different class; NO_EFFECT never counts; '
                       'consequence_linked_correction additionally needs the supported end; otherwise post_adverse_action '
                       'only or INCONCLUSIVE',
    'acceptance_reported': ['non-oracle routing records', 'CONTROL = reading = EFFECT', 'adverse observation then a real '
                            'correcting transition and supported end', 'matched-prefix counterfactuals (no-memory / removal / '
                            'wrong-memory / key-shuffle) with first divergence step', 'STORE -> SSD reload -> self-addressed '
                            'reuse (mechanical)', 'MISSING: model STOP'],
    'limits': ['one-step credit only', 'single run, few loops: a first working instance, not a statistic',
               'success is judged offline after all loops']}

PREREG_FIXED880 = '5d24abe0d44967f5c771141ab722b66d338553f3f06b0e9dff9a84cc54bbed39'   # sha256 of PREREG880 r2
STATE880 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO880, 'prereg_sha256': None, 'revision': 'r2', 'source': {}, 'api': {}, 'ref873': {},
            'preflight': {}, 'worlds': {}, 'catalog': {'order': [], 'entries': {}, 'origin': {}, 'rejected': {}}, 'loops': [], 'offline': {},
            'blocks': [], 'verdict': None, 'error': None}
STATE878 = STATE877 = STATE880
EXP878, OFFLINE880, CATKEYS880 = {}, {}, {}

class Gate880(Exception):
    pass

def line880(*parts): short864('T880', *parts)

def scan880(node, allow=()):
    used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in _a880.walk(node) if isinstance(c, _a880.Call)}
    used |= {k.arg for k in _a880.walk(node) if isinstance(k, _a880.keyword)}
    used |= {s.slice.value for s in _a880.walk(node) if isinstance(s, _a880.Subscript) and
             isinstance(s.slice, _a880.Constant)} & {'native_append_direct', 'DirectCut3'}
    bad = (used & BANNED880) - set(allow)
    assert not bad, ('FIREWALL880', getattr(node, 'name', '?'), sorted(bad))

def oracle_scan880(node):
    names = {n.id for n in _a880.walk(node) if isinstance(n, _a880.Name)}
    keys = {n.value for n in _a880.walk(node) if isinstance(n, _a880.Constant) and isinstance(n.value, str)}
    bad = (names & ORACLE880) | (keys & (ORACLE_KEYS880 | ORACLE880))
    assert not bad, ('ORACLE_FIREWALL880', node.name, sorted(bad))

def capture_source880():
    try:
        hist = [t for t in get_ipython().history_manager.input_hist_raw if MARKER880 in t and 'def loop880' in t]
        source, how = hist[-1], 'IPYTHON_CELL'
    except (NameError, IndexError):
        source = open(__file__, encoding='utf-8').read() if '__file__' in globals() else None; how = 'FILE_%RUN'
    assert source and MARKER880 in source, 'EXECUTED_880_SOURCE_NOT_CAPTURED'
    tree = _a880.parse(source); funcs = {n.name: n for n in tree.body if isinstance(n, _a880.FunctionDef)}
    for name, node in funcs.items():
        if name.endswith('880'): scan880(node)
    assert set(RUNTIME880) <= set(funcs), ('RUNTIME_FUNCTIONS_MISSING', sorted(set(RUNTIME880) - set(funcs)))
    for name in RUNTIME880: oracle_scan880(funcs[name])
    calls = [n for n in _a880.walk(tree) if isinstance(n, _a880.Call) and getattr(n.func, 'id', None) == 'reproduce_pre859859']
    assert len(calls) == 1, 'MODEL_LOADER_CALL_COUNT_NOT_ONE'
    (ROOT864 / 'TEST880.py').write_text(source, encoding='utf-8')
    STATE880['source'] = {'how': how, 'executed_cell_git_blob': git_blob864(source.encode()),
                          'executed_cell_sha256': sha256_bytes864(source.encode()), 'lines': source.count('\n') + 1,
                          'firewall': 'PASS', 'oracle_firewall': 'PASS (%d runtime functions)' % len(RUNTIME880)}

def select878_880():
    tree = _a880.parse(RAW_SOURCES864['878.py'].decode(), filename='878.py')
    consts = [n for n in tree.body if isinstance(n, _a880.Assign) and
              {x.id for t in n.targets for x in _a880.walk(t) if isinstance(x, _a880.Name)} & set(CONSTS878)]
    funcs = [n for n in tree.body if isinstance(n, (_a880.FunctionDef, _a880.ClassDef)) and n.name in FUNCS878]
    assert {n.name for n in funcs} == set(FUNCS878), ('SELECT_878', sorted(set(FUNCS878) - {n.name for n in funcs}))
    for n in funcs:
        if isinstance(n, _a880.FunctionDef): scan880(n, ('native_append_direct',) if n.name == 'append_exp878' else ())
    exec(compile(_a880.fix_missing_locations(_a880.Module(consts, [])), '878.py:constants', 'exec'), globals())
    assert sha256_bytes864(_j880.dumps(PREREG878, sort_keys=True).encode()) == TEST878_PREREG880, 'TEST878_PREREG_MISMATCH'
    exec(compile(_a880.fix_missing_locations(_a880.Module(funcs, [])), '878.py:selected', 'exec'), globals())
    log = RAW_SOURCES864['Test_878_log2.log'].decode()
    for needle in ('NVIDIA A100-SXM4-80GB', 'cell %s | prereg %s' % (LOCKS864['878.py'], TEST878_PREREG880[:16]),
                   'TEST878 | status COMPLETE'):
        assert needle in log, ('TEST878_LOG_NOT_THE_EXPECTED_GPU_RUN', needle)
    log9 = RAW_SOURCES864['879.log'].decode()
    for needle in ('NVIDIA A100-SXM4-80GB', 'prereg 6b7d8639d93b2110', 'TEST879 VERDICT MATCHED_FORK_OUTCOME_TRANSFER',
                   'status COMPLETE'):        # 879.log records the executed-cell blob 06db4aa0, not the committed 92f9eb66
        assert needle in log9, ('TEST879_LOG_NOT_THE_EXPECTED_GPU_RUN', needle)
    STATE880['source']['reused'] = {'878.py': LOCKS864['878.py'], 'functions': sorted(FUNCS878), 'constants': len(consts),
                                    'test879_run': 'MATCHED_FORK_OUTCOME_TRANSFER (879.log, locked)'}

def elapsed_min880():
    return (time.perf_counter() - T_START880) / 60.0

def vram_gib880():
    return (torch.cuda.mem_get_info()[0] + torch.cuda.memory_reserved() - torch.cuda.memory_allocated()) / 2**30

def rows_ok880(r):
    return r is not None and r.ndim == 2 and int(r.shape[0]) > 0

def sha_rows880(env, r):
    return None if r is None else env['stats849'](r)['sha256']

# ============================ setup (offline construction; the loop never reads OFFLINE880) ============================
def forge880(env):
    # three new worlds in one bank, forged with the locked templates and the locked physical_commit; names are new
    rng = _rnd880.Random(SEED880); alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    repo_text = '\n'.join(v.decode('utf-8', 'ignore') for v in RAW_SOURCES864.values())
    taken = set(env['NAMES841']) | {c.split('_', 1)[-1] for c in env['entries']}
    def code():
        while True:
            c = ''.join(rng.choice(alphabet) for _ in range(9))
            if c not in taken and c not in repo_text:
                taken.add(c); return c
    worlds = []
    for wi in range(WORLDS880):
        w = {'world': 'DOMAIN_' + code()}
        for key in ('start', 'middle', 'end', 'changed_end', 'decoy_end', 'fork_end', 'end3'): w[key] = code()
        w['ids'] = {}; worlds.append(w)
    contents = [(wi, kind) for wi in range(WORLDS880) for kind in NEW_KINDS867]; rng.shuffle(contents); bank = []
    for wi, kind in contents:
        cid = 'E880_' + code(); a, b = REL867[kind]
        env['physical_commit'](cid, BODY_TEMPLATE867.format(world=worlds[wi]['world'], a=worlds[wi][a], b=worlds[wi][b]))
        cp = env['safe_load'](env['entries'][cid])
        assert int(cp['n']) == int(env['P']) + int(env['entries'][cid]['body_tokens']) and cp['book_id'] == cid
        env['KEYS841'][cid] = env['unit841'](cp['h'][0, int(env['P']):, :].to(env['DEV']).float() - env['MU841'])
        del cp
        worlds[wi]['ids'][kind] = cid; bank.append(cid)
    specs = {}
    for wi, w in enumerate(worlds):
        qid = w['world'] + '_N880'; env['QTEXT841'][qid] = QUESTION_TEMPLATE867.format(world=w['world'], start=w['start'])
        for cond in ('LIVE', 'FORK', 'MISSING'):
            initial = [w['ids']['first'], w['ids']['fork']] if cond == 'FORK' else [w['ids']['first']]
            pool = [c for c in sorted(bank) if c not in initial]
            if cond == 'MISSING': pool = [c for c in pool if c not in (w['ids']['second'], w['ids']['changed'])]
            specs[(wi, cond)] = {'item': 'T880_%d_%s' % (wi, cond), 'qid': qid, 'initial': initial, 'pool': pool}
    OFFLINE880.update({'worlds': worlds, 'bank': sorted(bank)})
    names = [w[k] for w in worlds for k in w if k != 'ids'] + bank
    STATE880['worlds'] = {'count': WORLDS880, 'seed': SEED880, 'cards': len(bank),
                          'names_absent_from_locked_sources': all(n.split('_', 1)[-1] not in repo_text for n in names)}
    assert STATE880['worlds']['names_absent_from_locked_sources']
    return specs

def tokenize880(env):
    S = {k: list(env['tok'](v, add_special_tokens=False).input_ids) for k, v in SLOT_TEXT880.items()}
    assert all(S.values()), 'EMPTY_SLOT880'
    W = [(w, list(env['tok'](' ' + w, add_special_tokens=False).input_ids)) for w in STORE_WORDS880]
    assert all(ids for _, ids in W) and W[0][1][0] != W[1][1][0], ('STORE_WORDS_FIRST_TOKEN', W)
    assert CONTROL_PROMPT866.count('Decide the next reasoning action.') == 1, 'CONTROL_PROMPT_ANCHOR'
    STATE880['preflight']['tokens'] = {'store_words': {w: ids for w, ids in W}, 'slots': {k: len(v) for k, v in S.items()}}
    return S, W

# ============================ runtime: retrieval (hook-free query, NULL rival) ============================
def query880(env, rows):
    # index_embeds841(rows) -> the model's own layers 0..3 restated statement by statement (xspan878) over MEMNULL841:
    # the layer-3 rows of the address positions. No capture bridge, no layer list swap, no hook.
    assert rows_ok880(rows) and rows.dtype == torch.float32 and rows.device.type == 'cpu' and bool(torch.isfinite(rows).all())
    emb = env['index_embeds841'](rows.to(env['DEV'])); L = int(emb.shape[0]); cut = APPEND873['CUT']
    null = env['MEMNULL841']; n = int(null[0][0].shape[-2])
    cache = env['cache_build'](list(null[:cut + 1]))
    h = xspan878(env, cache, emb.reshape(1, L, int(env['H'])), torch.ones((1, n + L), device=env['DEV'], dtype=torch.long), 0, cut + 1)
    a = len(env['IDXPRE841']); q = h[0, a:a + int(rows.shape[0])].detach().float().cpu()
    assert bool(torch.isfinite(q).all()), 'QUERY_NOT_FINITE'
    del cache, h, emb
    return q, {'rows_sha256': sha_rows880(env, rows), 'query_sha256': sha_rows880(env, q), 'rows': int(rows.shape[0])}

def route880(env, query, candidates, keys, null_key):
    Q = env['unit841'](query.to(env['DEV']).float() - env['MU841'])
    scores = {c: float(env['peak50_841'](Q, keys[c])) for c in sorted(candidates)}
    null = float(env['peak50_841'](Q, null_key))
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    chosen = ranked[0][0] if ranked and ranked[0][1] > null else None
    return {'chosen': chosen, 'top3': [[c, s] for c, s in ranked[:3]], 'null_score': null, 'n_candidates': len(scores),
            'candidates': sorted(scores), 'margin_vs_null': (ranked[0][1] - null) if ranked else None}

def rebuild880(env, ctx, M, exp, tag):
    # environment memory through the locked mount chain, then at most one experience through the locked native append
    old_env, old_mem = ctx['env_memx'], ctx['memx']
    prior = old_env if (old_env is not None and ctx['M'] and list(M[:len(ctx['M'])]) == list(ctx['M'])) else None
    env_memx, rec = mount865(env, M, tag, prior=prior)
    memx, seal_ok = env_memx, None
    if exp is not None:
        cp = load_exp878(env, CATALOG880['entries'][exp]); memx = append_exp878(env, env_memx, cp); del cp
        seal_ok = prefix_seals865(env, memx, int(env_memx[0][0].shape[-2])) == prefix_seals865(env, env_memx)
        assert seal_ok, ('RECEIVER_PREFIX_SEAL', tag)
    ctx['env_memx'], ctx['memx'], ctx['M'], ctx['exp'] = env_memx, memx, list(M), exp
    rec = dict(rec, experience=exp, experience_prefix_seal=seal_ok); ctx['mount_records'].append(rec)
    free865(env, old_mem if old_mem is not old_env else None, old_env)
    return rec

def legal880(ctx, view):
    # sandbox legality only (what the executor can physically do now); never a preference
    acc = [c for c in ctx['spec']['pool'] if c not in ctx['M'] and c not in ctx['rejected']]
    if ctx['exp'] is None: acc += [x for x in view['experiences'] if x not in ctx['rejected']]
    legal = ['ADVANCE']
    if acc: legal.append('ACQUIRE')
    if ctx['M'] or ctx['exp'] is not None: legal.append('REJECT')
    if ctx['path']: legal.append('BACKTRACK')
    return [a for a in ACTIONS866 if a in legal + ['ACCEPT', 'STOP']], acc

def execute880(env, ctx, view, action, candidate, control, state):
    if action in ('ADVANCE', 'BACKTRACK'):
        return execute866(env, ctx, action, candidate, control, state)        # locked literal pointer execution
    spec = ctx['spec']; k = len(ctx['path'])
    row = {'type': 'EFFECT', 'action': action, 'k': k, 'decision_source': 'MODEL', 'mounted_before': list(ctx['M']),
           'experience_before': ctx['exp']}
    direction = direction866(env, ctx['memx'], spec['qid'], action, state, control)
    row['direction_text'] = direction['text'].strip()
    if action == 'ACQUIRE': _, cands = legal880(ctx, view)
    else: cands = list(ctx['M']) + ([ctx['exp']] if ctx['exp'] is not None else [])
    effect = None
    if not cands: effect = 'NO_EFFECT_BANK_EXHAUSTED' if action == 'ACQUIRE' else 'NO_EFFECT_EMPTY_MEMORY'
    elif not rows_ok880(direction['rows']): effect = 'NO_EFFECT_EMPTY_DIRECTION'
    else:
        query, qinfo = query880(env, direction['rows'].detach().float().cpu())
        route = route880(env, query, cands, view['keys'], NULL_KEY880); ctx['addresses'] += 1
        row.update({'query': qinfo, 'route': route}); chosen = route['chosen']; row['chosen'] = chosen
        tag = '880_%s_%s_%d' % (action[0], ctx['name'], ctx['steps'])
        if chosen is None: effect = 'NO_EFFECT_NULL_SELECTED'
        elif action == 'ACQUIRE' and chosen in CATALOG880['entries']:
            row['mount'] = rebuild880(env, ctx, ctx['M'], chosen, tag); effect = 'MOUNTED_EXPERIENCE'; ctx['acquisitions'] += 1
            ctx['used_experiences'].append(chosen)
        elif action == 'ACQUIRE':
            row['mount'] = rebuild880(env, ctx, ctx['M'] + [chosen], ctx['exp'], tag); effect = 'MOUNTED'; ctx['acquisitions'] += 1
        elif chosen in CATALOG880['entries']:
            row['mount'] = rebuild880(env, ctx, ctx['M'], None, tag); effect = 'UNMOUNTED_EXPERIENCE'
            ctx['rejected'].add(chosen); ctx['rejections'] += 1
        else:
            row['mount'] = rebuild880(env, ctx, [c for c in ctx['M'] if c != chosen], ctx['exp'], tag); effect = 'UNMOUNTED'
            ctx['rejected'].add(chosen); ctx['rejections'] += 1
    row.update({'effect': effect, 'mounted_after': list(ctx['M']), 'experience_after': ctx['exp'],
                'path_after': [p['text'] for p in ctx['path']]})
    ctx['events'].append(row)
    line880('EFFECT', ctx['name'], 't=%d' % ctx['steps'], action, effect, 'dir=%r' % row['direction_text'][:24],
            'chosen=%s' % row.get('chosen'), 'top3=%s null=%.4f' % (_j880.dumps((row.get('route') or {}).get('top3')),
            (row.get('route') or {}).get('null_score') or float('nan')))
    return effect

# ============================ runtime: native states ============================
def goal880(env, qid):
    g = env['gen849'](env['MEMNULL841'], list(env['prompt_ids'](PROMPT880['GOAL'].format(q=env['QTEXT841'][qid]))), None,
                      SLOT880['GOAL_SUFFIX'])
    check_output_h863(g, 'T880_GOAL')
    rows = g['rows'].detach().float().cpu()
    if not rows_ok880(rows): rows = env['MUE845'].detach().float().cpu().reshape(1, -1)   # mechanical placeholder, logged
    return rows, g['text'], int(g['rows'].shape[0])

def surprise880(env, ctx, frame, c_new, e_new):
    segs = [(SLOT880['EXPECT'], frame['P']), (env['C_SLOT851'], c_new), (env['E_SLOT851'], e_new), (SLOT880['GOAL'], ctx['G'])]
    u = env['gen851'](ctx['memx'], list(env['prompt_ids'](PROMPT880['SURPRISE'].format(q=ctx['q']))), segs, SLOT880['SURPRISE_SUFFIX'])
    check_output_h863(u, 'T880_SURPRISE')
    return u['rows'].detach().float().cpu(), u['text']

def store_words880(env, memx, X):
    # teacher-forced two-word reading (STORE / DISCARD), car867 rule: arg-max unless the two words keep < 0.5 of the mass
    env['budget849'](); L, n, Hd = int(X.shape[0]), int(memx[0][0].shape[-2]), int(env['H'])
    longest = max(len(ids) for _, ids in WORDS880)
    assert n + L + longest <= int(env['MAX_FUSED_TOKENS']), ('CONTEXT_LIMIT', n, L)
    one = lambda m: torch.ones((1, m), device=env['DEV'], dtype=torch.long)
    with torch.no_grad():
        cache = env['cache_build'](list(memx)); pos = torch.arange(n, n + L, device=env['DEV'])
        out = env['model'](inputs_embeds=X.reshape(1, L, Hd), past_key_values=cache, attention_mask=one(n + L),
                           position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
        first = torch.log_softmax(out.logits[0, -1].float(), dim=-1); del out, cache
        scores = []
        for word, ids in WORDS880:
            lps = [float(first[ids[0]])]
            if len(ids) > 1:
                m = len(ids) - 1; fresh = env['cache_build'](list(memx)); Y = torch.cat([X, env['embed841'](ids[:-1])], dim=0)
                p2 = torch.arange(n, n + L + m, device=env['DEV'])
                out = env['model'](inputs_embeds=Y.reshape(1, L + m, Hd), past_key_values=fresh, attention_mask=one(n + L + m),
                                   position_ids=p2.unsqueeze(0), cache_position=p2, use_cache=True, return_dict=True)
                lp = torch.log_softmax(out.logits[0, L:].float(), dim=-1); lps += [float(lp[i, ids[i + 1]]) for i in range(m)]
                del out, fresh, lp
            scores.append({'word': word, 'token_logps': lps, 'sequence_logp': float(sum(lps))})
    mass = sum(math.exp(s['sequence_logp']) for s in scores)
    best = max(scores, key=lambda s: s['sequence_logp'])
    return {'decision': best['word'] if mass >= ABSTAIN_MASS867 else 'ABSTAIN', 'mass': mass, 'scores': scores,
            'normalized': {s['word']: math.exp(s['sequence_logp']) / mass for s in scores} if mass > 0 else {}}

# ============================ runtime: episode capture and physical write ============================
def capture880(env, ctx, X2, reading, action):
    # [memory][X2][A] on its own timeline (car873 + commit, as TEST878); X2/A layer-3 rows by the explicit forward; bitwise gates
    cut, dev, Hd = APPEND873['CUT'], env['DEV'], int(env['H'])
    m2 = [tuple(t.clone() for t in kv) for kv in ctx['memx']]; n2, L2 = length873(env, m2), int(X2.shape[0])
    cache = env['cache_build'](list(m2)); g = {'X2_CAR_equals_decision': same873(car873(env, cache, X2), reading)}
    own = env['cache_build'](list(kv873(env, cache))); del cache
    A = dict(ACTION_IDS867)[action]; la = len(A); EA = env['embed841'](A)
    forward873(env, own, EA, n2 + L2); keep = kv873(env, own); del own
    one = lambda n: torch.ones((1, n), device=dev, dtype=torch.long)
    cl = env['cache_build'](list(m2))
    hx = xspan878(env, cl, X2.reshape(1, L2, Hd), one(n2 + L2), 0, cut + 1)
    ha = xspan878(env, cl, EA.reshape(1, la, Hd), one(n2 + L2 + la), 0, cut + 1)
    g['explicit_lower_KV_bitwise'] = all(torch.equal(x, y) for i in range(cut + 1) for x, y in zip(cache_kv870(cl, i), keep[i]))
    nk = [next_kv878(env, hx, n2), next_kv878(env, ha, n2 + L2)]; ref = keep[cut + 1]
    g['h3_next_layer_KV_bitwise'] = all(torch.equal(nk[j][t], ref[t][:, :, a:b]) for j, (a, b) in
                                        enumerate(((n2, n2 + L2), (n2 + L2, n2 + L2 + la))) for t in (0, 1))
    del nk, m2
    return {'keep': keep, 'cl': cl, 'h3': torch.cat([hx, ha], dim=1), 'n2': n2, 'L2': L2, 'la': la, 'A': list(A),
            'action': action, 'gates': g}

def close_frame880(env, ctx, view, frame, c_new, e_new, U, u_text):
    # one-step credit: the executed action and the observation that really followed it; native STORE / DISCARD
    rec = {'step': frame['step'], 'action': frame['action'], 'effect': frame['effect'], 'capture_gates': frame['cap']['gates'],
           'P_placeholder': frame['P_placeholder']}
    segs = [(SLOT880['EXPECT'], frame['P']), (SLOT880['ACTED'], frame['act_rows']), (env['C_SLOT851'], c_new),
            (env['E_SLOT851'], e_new), (SLOT880['SURPRISE'], U), (SLOT880['GOAL'], ctx['G'])]
    X, _ = env['make_x851'](list(env['prompt_ids'](PROMPT880['STORE'].format(q=ctx['q']))),
                            [(s, r) for s, r in segs if rows_ok880(r)], SLOT880['STORE_SUFFIX'])
    rd = store_words880(env, ctx['memx'], X); del X
    rec['store_reading'] = rd; rec['comparison_text'] = u_text
    cap = frame['cap']; ok = all(cap['gates'].values())
    if rd['decision'] == 'STORE' and view['store'] and ok:
        cut, dev, Hd, P = APPEND873['CUT'], env['DEV'], int(env['H']), int(env['P'])
        n2, L2, la = cap['n2'], cap['L2'], cap['la']; n1 = n2 + L2 + la
        if frame['effect'] == 'MOUNTED':                                  # ACQUIRE of a card: the TEST878 outcome path
            card = frame['chosen']; gH, n_before = append_card873(env, cap['keep'], card); body = int(env['entries'][card]['body_tokens'])
            cpc, _ = APPEND873['load'](card); h3c = cpc['h'][:, P:, :].to(dev); del cpc
            g = {'timeline': n_before == n1, 'card_rows': int(h3c.shape[1]) == body}; kind = 'MOUNTED_CARD'
        else:                                                             # the next real observation, native rows
            Y, _ = env['make_x851'](env['C_SLOT851'], [([], c_new), (env['E_SLOT851'], e_new)], []); body = int(Y.shape[0])
            own = env['cache_build'](list(cap['keep'])); forward873(env, own, Y, n1); gH = kv873(env, own); del own
            h3c = xspan878(env, cap['cl'], Y.reshape(1, body, Hd), torch.ones((1, n1 + body), device=dev, dtype=torch.long), 0, cut + 1)
            g = {'explicit_lower_KV_bitwise_C': all(torch.equal(x, y[:, :, n1:n1 + body]) for i in range(cut + 1)
                                                    for x, y in zip([t[:, :, n1:] for t in cache_kv870(cap['cl'], i)], gH[i])),
                 'h3_next_layer_KV_bitwise_C': all(torch.equal(a_, b_[:, :, n1:n1 + body]) for a_, b_ in
                                                   zip(next_kv878(env, h3c, n1), gH[cut + 1]))}
            kind = 'NEXT_OBSERVATION'; del Y
        rec['C_gates'] = g
        if all(g.values()):
            prov = {'loop': ctx['name'], 'item': ctx['spec']['item'], 'qid_sha256': sha256_bytes864(ctx['spec']['qid'].encode()),
                    'step': frame['step'], 'action': frame['action'], 'action_token_ids': cap['A'], 'effect': frame['effect'],
                    'C_kind': kind, 'chosen': frame.get('chosen'), 'spans_body': {'X2': [0, L2], 'A': [L2, L2 + la], 'C': [L2 + la, L2 + la + body]},
                    'pre_state_sha256': frame['pre_sha'], 'prediction_sha256': sha_rows880(env, frame['P']),
                    'prediction_is_placeholder': frame['P_placeholder'],
                    'observation_sha256': {'C': sha_rows880(env, c_new), 'E': sha_rows880(env, e_new)},
                    'parent_experience': frame['parent'], 'parent_experience_sha256': (CATALOG880['entries'].get(frame['parent']) or {}).get('sha256'),
                    'store_reading': {'decision': rd['decision'], 'mass': rd['mass']}, 'weights_digest': WEIGHTS0_880,
                    'engine_git_blob': ENGINE_BLOB880, 'cell_git_blob': STATE880['source'].get('executed_cell_git_blob'),
                    'contains': 'native h3 + L0-3 K/V of [X2][A][C] only'}
            eid = 'X880_' + sha256_bytes864(_j880.dumps(prov, sort_keys=True).encode())[:12]
            entry = write_exp878(env, eid, gH, torch.cat([cap['h3'], h3c], dim=1), n2, n1 + body, L2 + la, prov)
            cp = load_exp878(env, entry)                                   # SSD reload: file + every tensor SHA-256
            key = env['unit841'](cp['h'][0, P:, :].to(dev).float() - env['MU841']); del cp
            ok_rt = entry['roundtrip_K_rel'] <= ROPE_TOL878
            if ok_rt:
                CATALOG880['entries'][eid] = entry; CATKEYS880[eid] = key
                STATE880['catalog']['order'].append(eid); STATE880['catalog']['origin'][eid] = ctx['name']
                STATE880['catalog']['entries'][eid] = {k: entry[k] for k in ('file', 'sha256', 'bytes', 'body_tokens', 'roundtrip_K_rel')}
                ctx['stored'].append(eid)
            else:                                                        # file stays on disk (append-only); not addressable
                STATE880['catalog']['rejected'][eid] = {'file': entry['file'], 'sha256': entry['sha256'], 'bytes': entry['bytes'],
                                                        'tensor_sha': entry['tensor_sha'], 'roundtrip_K_rel': entry['roundtrip_K_rel'],
                                                        'reason': 'ROUNDTRIP_FAILED rel > ROPE_TOL878', 'loop': ctx['name']}
                rec['why_not_written'] = 'ROUNDTRIP_FAILED_FILE_KEPT_NOT_ADDRESSABLE'
            rec.update({'stored': eid if ok_rt else None, 'roundtrip_K_rel': entry['roundtrip_K_rel'], 'bytes': entry['bytes']})
        else:
            rec['stored'] = None; rec['why_not_written'] = 'C_GATE_FAILED'
        del gH, h3c
    else:
        rec['stored'] = None; rec['why_not_written'] = ('MODEL_' + rd['decision'] if rd['decision'] != 'STORE' else
                                                        'STORE_DISABLED_IN_COUNTERFACTUAL' if not view['store'] else 'CAPTURE_GATE_FAILED')
    for t in ('keep', 'cl', 'h3'): cap.pop(t, None)
    gc.collect(); torch.cuda.empty_cache()
    line880('FRAME', ctx['name'], 't=%d' % frame['step'], frame['action'], frame['effect'], 'cmp=%r' % u_text[:32],
            'store=%s mass=%.2f' % (rd['decision'], rd['mass']), 'written=%s' % rec.get('stored'))
    return rec

# ============================ runtime: one step and the loop ============================
def step880(env, ctx, view, h, pointer):
    q = ctx['q']; memx = ctx['memx']
    c = h['rows'].detach().float().cpu()
    ev = env['gen849'](memx, list(env['prompt_ids'](env['EVIDENCE851'].format(q=q))), None, env['ANSWER_SUFFIX851'])
    check_output_h863(ev, 'T880_EVIDENCE'); e = ev['rows'].detach().float().cpu()
    if not rows_ok880(c) or not rows_ok880(e): return None
    U, u_text = None, None
    if ctx['frame'] is not None:                                        # the real observation after the last executed action
        U, u_text = surprise880(env, ctx, ctx['frame'], c, e)
        ctx['frames'].append(close_frame880(env, ctx, view, ctx['frame'], c, e, U, u_text)); ctx['frame'] = None
    r = env['relation852'](c, e)
    segs = [(env['C_SLOT851'], c), (env['E_SLOT851'], e), (env['R_SLOT852'], r)]
    if pointer is not None: segs.append((SLOTS866['POINTER'], pointer))
    segs.append((SLOT880['GOAL'], ctx['G']))
    if rows_ok880(U): segs.append((SLOT880['SURPRISE'], U))
    d = env['gen851'](memx, list(env['prompt_ids'](PROMPT880['DEFICIT'].format(q=q))), segs, SLOT880['DEFICIT_SUFFIX'])
    check_output_h863(d, 'T880_DEFICIT'); D = d['rows'].detach().float().cpu()
    if rows_ok880(D): segs.append((SLOT880['DEFICIT'], D))
    v = env['gen851'](memx, list(env['prompt_ids'](EVALUATION_PROMPT866.format(q=q))), segs, SLOTS866['EVALUATION_SUFFIX'])
    check_output_h863(v, 'T880_EVALUATION'); V = v['rows'].detach().float().cpu()
    legal, _ = legal880(ctx, view); appraisal, P = {}, {}
    for a in legal:                                                      # hypothetical only: nothing is executed here
        act = env['embed841'](dict(ACTION_IDS867)[a]).detach().float().cpu()
        pa = env['gen851'](memx, list(env['prompt_ids'](PROMPT880['APPRAISE'].format(q=q))), segs + [(SLOT880['OPTION'], act)],
                           SLOT880['APPRAISE_SUFFIX'])
        check_output_h863(pa, 'T880_APPRAISE_' + a); Pa = pa['rows'].detach().float().cpu()
        rows = [act] + ([Pa, env['relation852'](Pa, ctx['G'])] if rows_ok880(Pa) else [])
        P[a] = (Pa, torch.cat(rows, dim=0).contiguous())
        appraisal[a] = {'text': pa['text'], 'rows': int(Pa.shape[0]), 'sha256': sha_rows880(env, Pa)}
    aseg = list(segs)
    if ctx['prev'] is not None:
        aseg += [(SLOTS867['PREV_EVALUATION'], ctx['prev']['V']), (env['K_SLOT851'], ctx['prev']['K'])]
    aseg.append((SLOTS866['EVALUATION'], V))
    aseg += [(SLOT880['OPT_' + a], P[a][1]) for a in ACTIONS866 if a in P]
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q).replace('Decide the next reasoning action.', CONTROL_INSERT880)))
    legacy = env['gen851'](memx, pre, aseg, env['REVIEW_SUFFIX851'])    # native control rows: direction866 + next feedback
    check_output_h863(legacy, 'T880_CONTROL_ROWS')
    X, _ = env['make_x851'](pre, aseg, env['REVIEW_SUFFIX851'])
    reading = reading867(car867(env, memx, pre, aseg, env['REVIEW_SUFFIX851']))
    rec = {'step': ctx['steps'] + 1, 'k': len(ctx['path']), 'candidate': h['text'], 'evidence': ev['text'], 'deficit': d['text'],
           'evaluation': v['text'], 'comparison': u_text, 'legal': legal, 'appraisal': appraisal, 'action': reading['action'],
           'reading': {k_: reading[k_] for k_ in ('action', 'argmax_word', 'abstain', 'mass', 'normalized', 'margin_logp', 'path')},
           'scores': reading['scores'], 'mounted': list(ctx['M']), 'experience': ctx['exp'],
           'state_sha256': {'C': sha_rows880(env, c), 'E': sha_rows880(env, e), 'D': sha_rows880(env, D), 'V': sha_rows880(env, V),
                            'U': sha_rows880(env, U), 'G': sha_rows880(env, ctx['G']), 'X': sha_rows880(env, X.float().cpu())}}
    return {'rec': rec, 'X': X, 'reading': reading, 'legacy': legacy, 'state': {'segments': aseg}, 'P': P,
            'own': {'V': V, 'K': legacy['rows'].detach().float().cpu()}}

def loop880(env, name, spec, view):
    ctx = {'name': name, 'spec': spec, 'arm': 'NCRA_' + name, 'q': env['QTEXT841'][spec['qid']], 'M': [], 'exp': None,
           'memx': None, 'env_memx': None, 'path': [], 'events': [], 'mount_records': [], 'acquisitions': 0, 'rejections': 0,
           'addresses': 0, 'steps': 0, 'hops': 0, 'prev': None, 'frame': None, 'frames': [], 'rejected': set(), 'stored': [],
           'used_experiences': []}
    end, accepted, error, trace = None, None, None, None
    t0, calls0 = time.perf_counter(), int(env['CALLS849'])
    try:
        rebuild880(env, ctx, list(spec['initial']), None, '880_L0_' + name)
        seal0 = prefix_seals865(env, ctx['memx'])
        ctx['G'], g_text, g_rows = goal880(env, spec['qid'])
        line880('BEGIN', name, 'mount=%s' % '|'.join(ctx['M']), 'pool=%d experiences=%d store=%s' % (
            len(spec['pool']), len(view['experiences']), view['store']), 'goal=%r' % g_text[:40])
        while end is None:
            if ctx['steps'] >= HORIZON880: end = 'OBSERVATION_HORIZON'; break
            if elapsed_min880() > HARD_MIN880 or vram_gib880() < FREE_MIN_GIB880 or not budget_left865(env, 40):
                end = 'RESOURCE_BUDGET'; break
            k = len(ctx['path']); pointer = None if k == 0 else ctx['path'][-1]['rows']
            h, kind = hop865(env, ctx['memx'], spec['qid'], k, pointer); ctx['hops'] += 1
            ctx['events'].append({'type': 'HOP', 'k': k, 'raw': h['text'], 'kind_logged_only': kind, 'mounted': list(ctx['M']),
                                  'experience': ctx['exp']})
            if kind == 'EMPTY_OUTPUT': end = 'NATIVE_EMPTY_OUTPUT'; break
            out = step880(env, ctx, view, h, pointer)
            if out is None: end = 'NATIVE_EMPTY_STATE'; break
            ctx['steps'] += 1; rec = out['rec']; action = rec['action']
            ctx['events'].append({'type': 'CONTROL', 'step': ctx['steps'], 'action': action, 'record': rec, 'decision_source': 'MODEL'})
            top3 = sorted(out['reading']['normalized'].items(), key=lambda kv: -kv[1])[:3]
            line880('STEP', name, 't=%d k=%d' % (ctx['steps'], k), 'hop=%r' % h['text'][:24], 'missing=%r' % rec['deficit'][:20],
                    'legal=%s' % ','.join(rec['legal']), 'CAR=' + '|'.join('%s:%.2f' % (w, p) for w, p in top3),
                    'mass=%.2f' % out['reading']['mass'], 'exec=%s' % action)
            if action == 'INVALID': end = 'MODEL_INVALID_ACTION'; break
            if action == 'ACCEPT': end, accepted = 'MODEL_ACCEPT', h['text'].strip(); break
            if action == 'STOP': end = 'MODEL_STOP'; break
            cap = capture880(env, ctx, out['X'], out['reading'], action)
            Pexec = out['P'].get(action, (None, None))[0]
            parent = ctx['exp']; pre_sha = rec['state_sha256']
            ctx['prev'] = out['own']
            effect = execute880(env, ctx, view, action, h, out['legacy'], out['state'])
            last = ctx['events'][-1] if ctx['events'] and ctx['events'][-1].get('type') == 'EFFECT' else {}
            ctx['frame'] = {'step': ctx['steps'], 'action': action, 'effect': effect, 'chosen': last.get('chosen'), 'cap': cap,
                            'P_placeholder': not rows_ok880(Pexec),
                            'P': Pexec if rows_ok880(Pexec) else env['MUE845'].detach().float().cpu().reshape(1, -1),
                            'act_rows': env['embed841'](cap['A']).detach().float().cpu(), 'parent': parent, 'pre_sha': pre_sha}
            del out
    except Exception as exc:
        error, trace = type(exc).__name__ + ': ' + str(exc)[:400], traceback.format_exc()
        end = 'EXECUTION_ERROR'
        (ROOT864 / ('880_%s_traceback.txt' % name)).write_text(trace, encoding='utf-8')
    if ctx['frame'] is not None:                                        # the last executed action has no observed consequence
        ctx['frames'].append({'step': ctx['frame']['step'], 'action': ctx['frame']['action'], 'effect': ctx['frame']['effect'],
                              'P_placeholder': ctx['frame']['P_placeholder'], 'stored': None, 'complete': False,
                              'why_not_written': 'OPEN_AT_HORIZON' if end == 'OBSERVATION_HORIZON' else 'OPEN_NO_OBSERVATION_' + str(end)})
        ctx['frame'] = None
    controls = [e for e in ctx['events'] if e['type'] == 'CONTROL']; effects = [e for e in ctx['events'] if e['type'] == 'EFFECT']
    executed = [c for c in controls if c['action'] not in ('ACCEPT', 'STOP', 'INVALID')]
    result = {'name': name, 'item': spec['item'], 'view': view['name'], 'end': end, 'accepted_candidate': accepted,
              'goal_text': locals().get('g_text'), 'goal_rows': locals().get('g_rows'),
              'goal_placeholder': locals().get('g_rows') == 0, 'path': [p['text'] for p in ctx['path']], 'final_mounted': list(ctx['M']),
              'final_experience': ctx['exp'], 'steps': ctx['steps'], 'actions': [c['action'] for c in controls],
              'effects': [e['effect'] for e in effects], 'used_experiences': list(ctx['used_experiences']),
              'stored': list(ctx['stored']), 'frames': ctx['frames'], 'events': ctx['events'],
              'literal_execution': len(executed) == len(effects) and all(c['action'] == e['action'] == c['record']['reading']['action']
                                                                          for c, e in zip(executed, effects)),
              'mount_integrity': all(m['n_exact'] and m['all_80_layers'] and m['finite'] and m['prior_prefix_exact'] is not False
                                     and m.get('experience_prefix_seal') is not False for m in ctx['mount_records']),
              'error': error, 'traceback': trace}
    try:
        free865(env, ctx['memx'] if ctx['memx'] is not ctx['env_memx'] else None, ctx['env_memx']); ctx['memx'] = ctx['env_memx'] = None
        rm, _ = mount865(env, spec['initial'], '880_LR_' + name)
        result['exact_restore'] = prefix_seals865(env, rm) == locals().get('seal0'); free865(env, rm)
    except Exception as exc:
        result['exact_restore'] = False; result['restore_error'] = type(exc).__name__ + ': ' + str(exc)
    result['seconds'] = round(time.perf_counter() - t0, 1); result['calls'] = int(env['CALLS849']) - calls0
    line880('END', name, 'end=%s' % end, 'accepted=%r' % accepted, 'actions=%s' % '>'.join(result['actions']),
            'effects=%s' % '>'.join(str(x) for x in result['effects']), 'used=%s' % result['used_experiences'],
            'stored=%s' % result['stored'], 's=%.0f calls=%d' % (result['seconds'], result['calls']),
            '' if error is None else 'ERROR=' + error)
    return result

# ============================ orchestration (views are experimenter-side, built from catalog snapshots) ============================
def view880(kind, snapshot, l3_used, a_world_stored):
    exps = list(STATE880['catalog']['order']) if kind == 'FULL' else list(snapshot)
    note = None
    if kind == 'NO_MEMORY': exps = []
    elif kind == 'REMOVAL':
        exps = [x for x in snapshot if x not in set(l3_used)]; note = None if l3_used else 'NOT_APPLICABLE_L3_MOUNTED_NO_EXPERIENCE'
    elif kind == 'WRONG_MEMORY':
        exps = [x for x in snapshot if x not in set(a_world_stored)]
        note = None if (exps and a_world_stored) else 'NOT_APPLICABLE_NO_WRONG_OR_NO_RIGHT_MEMORY'
    keys = {c: v for c, v in env880['KEYS841'].items()}
    keys.update({x: CATKEYS880[x] for x in exps})
    if kind == 'KEY_SHUFFLE':
        if len(exps) < 2: note = 'NOT_APPLICABLE_FEWER_THAN_TWO_EXPERIENCES'
        else: keys.update({x: CATKEYS880[exps[(i + 1) % len(exps)]] for i, x in enumerate(exps)})
    return {'name': kind, 'experiences': exps, 'keys': keys, 'store': kind == 'FULL', 'note': note}

def evaluate880(env):
    # OFFLINE ONLY (after every loop): labels of the forged worlds. Loops that did not execute are skipped with their reason.
    worlds = OFFLINE880['worlds']; out = {}
    adverse_cls = ('fork_end', 'decoy_end', 'UNKNOWN', 'OTHER')            # changed_end is supported when 'changed' is mounted
    card_of = {'fork_end': 'fork', 'decoy_end': 'decoy'}
    for r in STATE880['loops']:
        if r.get('end') in ('NOT_RUN', 'NOT_APPLICABLE') or 'events' not in r or 'literal_execution' not in r:
            out[r['name']] = {'executed': False, 'end': r.get('end'), 'note': r.get('note')}; continue
        w = worlds[r['world']]; cond = r['condition']
        correct = r['end'] == 'MODEL_ACCEPT' and bool(r.get('accepted_candidate')) and bool(
            env['supported851'](r['accepted_candidate'], w, set(r['final_mounted'])))
        success = r['end'] == 'MODEL_STOP' if cond == 'MISSING' else correct
        ev = r['events']; hops = []; adverse = []
        for i, e in enumerate(ev):
            if e['type'] != 'HOP': continue
            cls = env['node851'](e['raw'], w); hops.append(cls)
            if cls in adverse_cls: adverse.append({'event': i, 'hop': len(hops) - 1, 'class': cls, 'text': str(e['raw']).strip()})
        for a in adverse:
            after = [(j, e) for j, e in enumerate(ev) if j > a['event']]
            a['post_adverse_actions'] = [e['action'] for _, e in after if e['type'] == 'CONTROL']
            a['post_adverse_effects'] = [e['effect'] for _, e in after if e['type'] == 'EFFECT']
            link = None
            for j, e in after:
                if e['type'] != 'EFFECT' or str(e.get('effect') or '').startswith('NO_EFFECT'): continue
                if e['action'] == 'BACKTRACK' and e['effect'] == 'POINTER_RETRACTED' and \
                        str(e.get('removed_node') or '').strip().upper() == a['text'].upper():
                    link = {'type': 'BACKTRACK_REMOVED_ADVERSE_NODE', 'event': j}
                elif e['action'] == 'REJECT' and e['effect'] in ('UNMOUNTED', 'UNMOUNTED_EXPERIENCE') and \
                        e.get('chosen') not in (e.get('mounted_after') or []) and e.get('chosen') != e.get('experience_after'):
                    src = w['ids'].get(card_of.get(a['class'], ''), None)
                    link = ({'type': 'REJECT_UNMOUNTED_SOURCE_CARD', 'event': j} if src is not None and e.get('chosen') == src else
                            {'type': 'REJECT_UNMOUNTED_UNLINKED', 'event': j, 'inconclusive': True})
                elif e['action'] == 'ACQUIRE' and e['effect'] in ('MOUNTED', 'MOUNTED_EXPERIENCE'):
                    nxt = [env['node851'](x['raw'], w) for x in ev[j + 1:] if x['type'] == 'HOP'][:1]
                    link = ({'type': 'ACQUIRE_MOUNT_THEN_HOP_CLASS_CHANGED', 'event': j, 'next_hop': nxt[0]}
                            if nxt and nxt[0] != a['class'] else
                            {'type': 'ACQUIRE_MOUNT_NO_CHANGE_OBSERVED', 'event': j, 'next_hop': nxt[0] if nxt else None,
                             'inconclusive': True})
                if link is not None and not link.get('inconclusive'): break
            a['transition'] = link
            a['status'] = ('CONSEQUENCE_LINKED_CORRECTION' if link and not link.get('inconclusive') and success else
                           'TRANSITION_WITHOUT_SUPPORTED_END' if link and not link.get('inconclusive') else
                           'INCONCLUSIVE' if link else 'POST_ADVERSE_ACTION_ONLY' if a['post_adverse_actions'] else 'NO_ACTION_AFTER')
        out[r['name']] = {'executed': True, 'success': success, 'correct_accept': correct, 'end': r['end'], 'hop_classes': hops,
                          'adverse': adverse,
                          'consequence_linked_correction': any(a['status'] == 'CONSEQUENCE_LINKED_CORRECTION' for a in adverse)}
    return out

def reuse_ref880(r):
    # first physical mount of an experience stored by ANOTHER loop: (step, experience id, mount record) or None
    step = None
    for e in r.get('events', []):
        if e['type'] == 'CONTROL': step = e['step']
        if e['type'] == 'EFFECT' and e.get('effect') == 'MOUNTED_EXPERIENCE' and \
                STATE880['catalog']['origin'].get(e.get('chosen')) not in (None, r['name']):
            return {'step': step, 'experience': e['chosen'], 'origin': STATE880['catalog']['origin'][e['chosen']],
                    'mount': {k: (e.get('mount') or {}).get(k) for k in ('n', 'n_exact', 'experience', 'experience_prefix_seal')},
                    'route': {k: (e.get('route') or {}).get(k) for k in ('top3', 'null_score', 'margin_vs_null')}}
    return None

def compare880(full, cf, ref):
    # matched prefix = the control's decision input X is bitwise equal at every step up to and including the reuse step
    xs = lambda r: [e['record']['state_sha256']['X'] for e in r['events'] if e['type'] == 'CONTROL']
    a, b = xs(full), xs(cf); s0 = ref['step']
    out = {'reuse_step': s0, 'full_actions': full['actions'], 'cf_actions': cf['actions'], 'full_end': full['end'], 'cf_end': cf['end']}
    out['first_X_mismatch_step'] = next((i + 1 for i, (x, y) in enumerate(zip(a, b)) if x != y), None)
    out['matched_prefix'] = len(a) >= s0 and len(b) >= s0 and a[:s0] == b[:s0] and full['actions'][:s0] == cf['actions'][:s0]
    div = next((i + 1 for i, (x, y) in enumerate(zip(full['actions'], cf['actions'])) if i >= s0 and x != y), None)
    model_end = lambda e: str(e).startswith('MODEL_')
    term = full['end'] != cf['end'] and (model_end(full['end']) or model_end(cf['end']))
    out['first_executed_divergence_step'] = div
    out['terminal_model_decision_differs'] = bool(term and div is None)
    out['effects_differ_only'] = full['effects'] != cf['effects'] and div is None and not term
    out['post_reuse_behaviour_differs'] = bool(out['matched_prefix'] and (div is not None or term))
    return out

def verdict880():
    L = {r['name']: r for r in STATE880['loops']}; off = STATE880['offline']; blocks = list(STATE880['blocks'])
    ran = [r for r in L.values() if r.get('end') not in ('NOT_RUN', 'NOT_APPLICABLE') and 'literal_execution' in r]
    not_ran = {n: {'end': r.get('end'), 'note': r.get('note')} for n, r in L.items() if r not in ran}
    for r in ran:
        if r['end'] == 'EXECUTION_ERROR': blocks.append('EXECUTION_ERROR:' + r['name'])
        if not r['literal_execution']: blocks.append('LITERAL_EXECUTION:' + r['name'])
        if not r['mount_integrity'] or r.get('exact_restore') is not True: blocks.append('MOUNT_INTEGRITY:' + r['name'])
        for f in r.get('frames', []):
            if f.get('capture_gates') and not all(f['capture_gates'].values()): blocks.append('CAPTURE_GATE:%s:t%s' % (r['name'], f['step']))
            if f.get('C_gates') and not all(f['C_gates'].values()): blocks.append('C_GATE:%s:t%s' % (r['name'], f['step']))
    stored = list(STATE880['catalog']['order'])
    full = L.get('L3_A_FORK'); full = full if full in ran else None
    ref = reuse_ref880(full) if full else None
    l6 = L.get('L6_A_MISSING'); l6_ref = reuse_ref880(l6) if l6 in ran else None
    cmp = {}
    if ref:
        for n in ('L4_A_FORK_NO_MEMORY', 'L5_A_FORK_REMOVAL', 'L7_A_FORK_WRONG_MEMORY', 'L8_A_FORK_KEY_SHUFFLE'):
            r = L.get(n)
            cmp[n] = compare880(full, r, ref) if r in ran else {'executed': False, 'end': (r or {}).get('end'), 'note': (r or {}).get('note')}
            if n == 'L5_A_FORK_REMOVAL' and r in ran:
                cmp[n]['reference_experience_removed'] = ref['experience'] not in r.get('experiences_visible', [])
    primary = [n for n in ('L4_A_FORK_NO_MEMORY', 'L5_A_FORK_REMOVAL') if cmp.get(n, {}).get('matched_prefix') and
               (n != 'L5_A_FORK_REMOVAL' or cmp[n].get('reference_experience_removed'))]
    full_success = bool((off.get('L3_A_FORK') or {}).get('success'))
    if blocks: v = 'TECHNICAL_BLOCK'
    elif full is None: v = 'PARTIAL'
    elif not stored: v = 'CLOSED_LOOP_NO_STORE'
    elif ref is None: v = 'CLOSED_LOOP_NO_SELF_REUSE'
    elif not primary: v = 'CLOSED_LOOP_REUSE_INCONCLUSIVE_UNMATCHED_PREFIX'
    elif not any(cmp[n]['post_reuse_behaviour_differs'] for n in primary): v = 'CLOSED_LOOP_REUSE_NO_BEHAVIOUR_CHANGE'
    elif not full_success: v = 'CLOSED_LOOP_REUSE_BEHAVIOUR_CHANGE_UNSUPPORTED'
    else: v = 'CLOSED_LOOP_MEMORY_DEPENDENT_BEHAVIOUR'
    mech = {'stored_experiences': len(stored), 'rejected_roundtrip': sorted(STATE880['catalog'].get('rejected', {})),
            'ssd_reload_sha_verified_for_catalog': len(stored),
            'self_addressed_reuse_L3': ref, 'L6_reuse': ({'status': 'REUSE_OBSERVED_NO_MATCHED_CONTROL', **l6_ref} if l6_ref else None),
            'complete_frames': sum(1 for r in ran for f in r.get('frames', []) if 'store_reading' in f),
            'open_frames': sum(1 for r in ran for f in r.get('frames', []) if f.get('complete') is False),
            'model_store_readings': sum(1 for r in ran for f in r.get('frames', []) if (f.get('store_reading') or {}).get('decision') == 'STORE')}
    acc = {'non_oracle_routing_logged': all('route' in e for r in ran for e in r['events'] if e['type'] == 'EFFECT'
                                            and e['action'] in ('ACQUIRE', 'REJECT') and e['effect'] not in
                                            ('NO_EFFECT_BANK_EXHAUSTED', 'NO_EFFECT_EMPTY_MEMORY', 'NO_EFFECT_EMPTY_DIRECTION')),
           'literal_execution_all_loops': all(r['literal_execution'] for r in ran),
           'consequence_linked_correction': sorted(n for n, x in off.items() if x.get('consequence_linked_correction')),
           'mechanical': mech, 'counterfactuals_vs_L3': cmp, 'matched_primary_controls': primary,
           'L3_offline_supported_success': full_success, 'not_executed_loops': not_ran,
           'missing_model_stop': (off.get('L6_A_MISSING') or {}).get('end') == 'MODEL_STOP',
           'solvable_success': {n: off[n].get('success') for n in ('L1_A_LIVE', 'L2_B_LIVE', 'L3_A_FORK') if n in off}}
    STATE880['verdict'] = {'verdict': v, 'blocks': blocks, 'acceptance': acc, 'definition': PREREG880['verdict'].get(v)}
    return STATE880['verdict']

def report880():
    print('=' * 112)
    print('TEST880 NCRA CLOSED-LOOP ENGINE | GPU %s | cell %s | prereg %s' % (CC_GPU.get('name'),
          STATE880['source'].get('executed_cell_git_blob'), (STATE880.get('prereg_sha256') or '')[:16]))
    print('PREFLIGHT %s' % _j880.dumps({k: v for k, v in STATE880['preflight'].items() if k != 'tokens'}, sort_keys=True, default=str)[:900])
    for r in STATE880['loops']:
        o = STATE880['offline'].get(r['name'], {})
        print('LOOP %-24s end=%-20s actions=%s effects=%s used=%s stored=%s success=%s adverse=%s linked_correction=%s note=%s' % (
              r['name'], r.get('end'), '>'.join(r.get('actions', [])), '>'.join(str(x) for x in r.get('effects', [])),
              r.get('used_experiences'), r.get('stored'), o.get('success'),
              [(a['hop'], a['class'], a['status']) for a in o.get('adverse', [])], o.get('consequence_linked_correction'),
              r.get('note')))
        for e in r.get('events', []):
            if e['type'] == 'EFFECT' and e.get('route'):
                print('    route t%s %s -> %s | top3 %s | null %.4f | candidates %d' % (e.get('k'), e['action'], e.get('chosen'),
                      _j880.dumps(e['route']['top3']), e['route']['null_score'], e['route']['n_candidates']))
        for f in r.get('frames', []):
            sr = f.get('store_reading') or {}
            print('    frame t%s %s %s store=%s mass=%s written=%s %s' % (f.get('step'), f.get('action'), f.get('effect'),
                  sr.get('decision'), None if sr.get('mass') is None else round(sr['mass'], 3), f.get('stored'), f.get('why_not_written') or ''))
    print('CATALOG (append-only) %s | roundtrip-rejected (files kept) %s' % (_j880.dumps(STATE880['catalog']['origin'], sort_keys=True),
          sorted(STATE880['catalog'].get('rejected', {}))))
    v = STATE880['verdict'] or {}
    print('ACCEPTANCE %s' % _j880.dumps(v.get('acceptance'), sort_keys=True, default=str))
    print('TEST880 VERDICT %s | blocks %s' % (v.get('verdict'), v.get('blocks')))
    print('MEANING: %s' % v.get('definition'))
    print('LIMITS: %s' % '; '.join(PREREG880['limits']))
    print('status %s | wall %.0f s | peak GPU %.2f GiB | GPU_EXECUTION_NOT_VERIFIED_BY_AUTHOR' % (STATE880['status'],
          time.perf_counter() - T_START880, torch.cuda.max_memory_allocated() / 2**30 if torch.cuda.is_available() else 0.0))
    print('=' * 112)

T_START880 = T_START878 = time.perf_counter()
CATALOG880 = {'entries': {}}
try:
    STATE880['status'] = 'G0_SOURCE'; capture_source880()
    PREREG_SHA880 = sha256_bytes864(_j880.dumps(PREREG880, sort_keys=True).encode()); STATE880['prereg_sha256'] = PREREG_SHA880
    assert PREREG_SHA880 == PREREG_FIXED880, ('PREREG_R2_CHANGED', PREREG_SHA880)   # contract fixed before any run
    json_write864('880_prereg.json', {'prereg': PREREG880, 'sha256': PREREG_SHA880, 'before_model_load': True})
    line880('G0 PREREG', PREREG_SHA880)
    load_sources865(); select878_880(); source_audit878(); load878()
    STATE880['ref873'] = ref873_874(RAW_SOURCES864['873.log'].decode())
    feasibility_audit864(); audit_contracts865(); load_spine864()
    line880('G0 SOURCE PASS', _j880.dumps(STATE880['source'], sort_keys=True))
    STATE880['status'] = 'G1_PREFLIGHT'; assert CC_GPU_OK, ('GPU_PRECHECK', CC_GPU)
    env880, original_error880, original_trace880, reproduction880 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace880; TWO_JOB_VERIFICATION864 = verify_two_job859(env880, original_trace880)
    assert_hook_free859(env880, 'T880_before_native'); install_offline_evaluator859(env880)
    native880 = native_sequences860(env880); NATIVE_REGRESSION864 = native_regression864(env880, native880)
    verify_864_reference865(NATIVE_REGRESSION864); ANALYSIS864 = run_analysis863(env880, native880)
    assert len(STATE863['restores']) == 3 and all(r['exact'] for r in STATE863['restores'])
    digest880 = records_digest861(env880); null_seal880 = physical_seal863(env880, env880['MEMNULL841'])
    runtime_contracts865(env880); runtime_preflight865(env880, reproduction880); rearm_budget865(env880); make_slots866(env880)
    SLOTS867['PREV_EVALUATION'] = list(env880['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env880); resolve_append873(env880); api877(env880); WEIGHTS0_880 = weights_digest877(env880)
    chunk880 = [ns['CHUNK'] for ns in (env880['build_fusion'].__globals__, env880) if 'CHUNK' in ns]
    assert chunk880 and int(chunk880[0]) > 0 and all(k in env880 for k in ('P', 'to_gpu', 'kv_digest', 'entries', 'peak50_841',
        'physical_commit', 'index_embeds841', 'MEMNULL841', 'MUE845', 'supported851', 'node851')), 'ENGINE_NAMESPACE'
    EXP878['CHUNK'] = int(chunk880[0])
    EXP_DIR878 = ROOT864 / 'experience_cut3'; EXP_DIR878.mkdir(parents=True, exist_ok=False)
    SLOT880, WORDS880 = tokenize880(env880)
    # query-path parity: hook-free explicit layers 0..3 == the GPU-verified bypass path (same rows)
    probe_rows880 = env880['MUE845'].detach().float().cpu().reshape(1, -1).repeat(3, 1)
    qx880, _ = query880(env880, probe_rows880); qb880, _ = pointer_query865(env880, probe_rows880)
    rel880 = float(torch.linalg.vector_norm(qx880 - qb880)) / max(float(torch.linalg.vector_norm(qb880)), 1e-30)
    STATE880['preflight']['query_parity'] = {'bitwise': bool(torch.equal(qx880, qb880)), 'rel': rel880, 'tol': PARITY_TOL880}
    if rel880 > PARITY_TOL880: raise Gate880('QUERY_PATH_PARITY rel=%.3e' % rel880)
    NULL_Q880, _ = query880(env880, env880['MUE845'].detach().float().cpu().reshape(1, -1))
    NULL_KEY880 = env880['unit841'](NULL_Q880.to(env880['DEV']).float() - env880['MU841'])
    assert_hook_free859(env880, 'T880_before_loops')
    line880('G1 PREFLIGHT PASS', _j880.dumps(STATE880['api'], sort_keys=True), 'parity=%s' % _j880.dumps(STATE880['preflight']['query_parity']),
            'CHUNK=%d P=%d' % (EXP878['CHUNK'], int(env880['P'])), 'model_load_s=%.0f' % (time.perf_counter() - T_START880))
    STATE880['status'] = 'SETUP'; T0_865 = time.perf_counter(); SPECS880 = forge880(env880)
    line880('SETUP', _j880.dumps(STATE880['worlds'], sort_keys=True))
    STATE880['status'] = 'LOOPS'; snapshot880, l3_used880 = None, []
    for name880, wi880, cond880, kind880, _store880 in PLAN880:
        if name880 == 'L3_A_FORK': snapshot880 = list(STATE880['catalog']['order'])
        a_stored880 = [x for x, o in STATE880['catalog']['origin'].items() if o in ('L1_A_LIVE',) and x in (snapshot880 or [])]
        view = view880(kind880, snapshot880 or [], l3_used880, a_stored880)
        row = {'name': name880, 'world': wi880, 'condition': cond880, 'view': kind880, 'experiences_visible': view['experiences'],
               'note': view['note']}
        if view['note']:
            row.update(end='NOT_APPLICABLE', actions=[], effects=[], events=[], frames=[]); STATE880['loops'].append(row)
            line880('LOOP_NOT_APPLICABLE', name880, view['note']); continue
        if elapsed_min880() + LOOP_MIN880 > HARD_MIN880 or vram_gib880() < FREE_MIN_GIB880:
            row.update(end='NOT_RUN', actions=[], effects=[], events=[], frames=[]); STATE880['loops'].append(row)
            line880('LOOP_NOT_RUN', name880, 'budget'); continue
        res = loop880(env880, name880, SPECS880[(wi880, cond880)], view); row.update(res); STATE880['loops'].append(row)
        if name880 == 'L3_A_FORK': l3_used880 = list(res['used_experiences'])
        json_write864('880_catalog.json', jsafe878(STATE880['catalog']))
    hook880 = hook_audit859(env880, 'T880_final')
    if records_digest861(env880) != digest880 or physical_seal863(env880, env880['MEMNULL841']) != null_seal880 or \
            hook880['hook_count'] or hook880['transformers_output_capturing_installed'] or weights_digest877(env880) != WEIGHTS0_880:
        STATE880['blocks'].append('POST_RUN_INTEGRITY')
    STATE880['status'] = 'OFFLINE'; STATE880['offline'] = evaluate880(env880)
    STATE880['status'] = 'COMPLETE'; verdict880()
except BaseException as exc:
    STATE880['error'] = '%s: %s' % (type(exc).__name__, exc); STATE880['traceback'] = traceback.format_exc()
    STATE880['status'] = 'FAILED_AT_' + str(STATE880['status'])
    STATE880['verdict'] = {'verdict': 'TECHNICAL_BLOCK', 'blocks': ['EXCEPTION: ' + STATE880['error'][:300]]}
    (ROOT864 / '880_traceback.txt').write_text(STATE880['traceback'], encoding='utf-8')
    print('TEST880 ERROR', STATE880['error'][:300], '| full traceback:', ROOT864 / '880_traceback.txt', file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        payload880 = dict(STATE880, preregistration=PREREG880)
        json_write864('880_result.json', jsafe878(payload880) if 'jsafe878' in globals() else
                      json.loads(json.dumps(payload880, default=str)))
        json_write864('880_catalog.json', json.loads(json.dumps(STATE880['catalog'], default=str)))
    except Exception as exc: print('RESULT_WRITE_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    try: report880()
    except Exception as exc: print('REPORT_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE880['suffix'], 'test870.py:suffix', 'exec'), globals())
