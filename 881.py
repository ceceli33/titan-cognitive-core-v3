# AKBASCORE SILICON HIPPOCAMPUS — TEST881 — PILOT-0: PHYSICAL C VISIBILITY -> NATIVE CAR (single real episode)
# One A100-SXM4-80GB Colab cell. Frozen Qwen2.5-72B-Instruct NF4, BF16. Locked engine test870.py (e322ed8) + locked 878.py,
# 880.py (store reader only), repository pinned to commit 6bd3c52bf60eea2d4b5a9b5c72d871bae24e3c10.
# QUESTION: when the real consequence C of one physical CUT3 experience [X2][A][C] is readable by an independent receiver,
# does the native CAR distribution move in a C-specific, goal-consistent way against a C-BLIND arm that has the same
# positions, the same cache length, the same mask construction and the same (masked) attention kernel?
# Experiences: produced in this cell by the exact replay of the locked 869 records (real ADVANCE -> ACQUIRE executions of
# MISSING and LIVE worlds: same X2 and A, different real mounted card C), written by the locked TEST878 writer, freed,
# reloaded from SSD with file + per-tensor SHA-256. Receivers: I867_00_FORK / I867_01_FORK step 1 (independent states).
# Layout per arm: [receiver memory B][E = X2 A C][receiver X]. Every arm has its own cache built from the immutable
# B+E tensors and computes X and every CAR continuation token from layer 0 under its own visibility mask:
#   VIS     C readable (explicit layers, C first hidden in the 2-D mask then made readable in the 4-D mask: masked kernel)
#   C_BLIND C span hidden from X and every continuation (same explicit masked kernel) - main contrast VIS - C_BLIND
#   EPISODE_OFF whole E hidden; OFF_G_ZERO E rows replaced by zeros and hidden; OFF_0 receiver without E (position control)
# Then one real action: the native VIS reading of the pre-registered cell is executed by the locked executor in the receiver's
# real environment, the real next observation is read, the model's own STORE/DISCARD reading decides a REAL write.
# Never: weight writes, training, hooks, output_hidden_states/attentions, logit edits, action forcing, text replay, outcome
# oracle at runtime, synthetic C in the REAL namespace. Labels (card kinds, hop classes) are read only offline.
import ast as _a881, hashlib as _h881, json as _j881, os as _o881, re as _r881, shutil as _s881, urllib.request as _u881
ENGINE_URL881 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB881, MARKER881 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', 'AKBASCORE SILICON HIPPOCAMPUS — TEST881'
HEAD881 = '6bd3c52bf60eea2d4b5a9b5c72d871bae24e3c10'

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
EXEC_ALLOW881 = ('execute866', 'hop865', 'free865')          # gate4_881 only: the one real action through the locked executor
ORACLE881 = {'supported851', 'node851', 'world867', 'correct867', 'success867', 'FIXTURE881', 'OFFLINE867', 'worlds829'}
RUNTIME881 = ('make_single_episode_layout881', 'xread881', 'nread881', 'xhidden881', 'zero_slot881', 'gate2_881',
              'gate3_881', 'gate4_881', 'atomic_append_real881', 'store_reading881')
CELLS881 = (('00', '00'), ('01', '01'), ('01', '00'), ('00', '01'))   # (source world, receiver world); same goal first
EXEC_CELL881, EXEC_COND881 = ('00', '00'), 'LIVE'          # GATE4: the one real execution (fixed before the model is loaded)
WALL_MIN881, PEAK_GIB881, FFE_MAX881, FREE_MIN_GIB881, DISK_MIN_GIB881 = 45.0, 60.0, 120.0, 8.0, 5.0
STORE_PROMPT881 = ('Question: {q}\nThe numerical context contains the action you executed and the candidate and the independent '
                   'answer actually observed after it. Decide whether this action and its real consequence should be kept as a '
                   'physical experience for future decisions. Reply with exactly one word: STORE or DISCARD.')
SLOT_TEXT881 = {'ACTED': 'Executed action numerical state:', 'STORE_SUFFIX': '\nMemory decision:'}
PREREG881 = {
    'question': 'does the physically readable real consequence C of one CUT3 experience move the native CAR of an '
                'independent receiver in a C-specific, goal-consistent way, against a path-matched C-BLIND arm',
    'repository': {'head': HEAD881, 'archive': 'codeload zip of the pinned commit; every file git-blob locked'},
    'experiences': {'S00': ['I867_00_MISSING', 'I867_00_LIVE'], 'S01': ['I867_01_MISSING', 'I867_01_LIVE'],
                    'how': 'exact replay of the locked 869 records (real executions), written by the locked write_exp878, '
                           'source working state freed, reloaded with file + per-tensor SHA-256 (locked load_exp878)',
                    'pair': 'per world the MISSING and LIVE experiences share X2 and A bitwise (pre-C seal) and differ only '
                            'in the real mounted card C (same token length)'},
    'receivers': {'R00': 'I867_00_FORK step 1', 'R01': 'I867_01_FORK step 1'},
    'cells': ['%s>%s' % c for c in CELLS881],
    'layout': '[B][E=X2,A,C][X]; X positions identical in every arm with E; OFF_0 has no E (position control only)',
    'arms': {'VIS': 'xcar878(blind=C, sham=True): C hidden in the 2-D mask, readable again in the built 4-D mask',
             'C_BLIND': 'xcar878(blind=C, sham=False): C hidden from X and every continuation token at every layer',
             'EPISODE_OFF': 'xcar878(blind=E)', 'OFF_G_ZERO': 'E rows replaced by zeros, blind=E',
             'OFF_0': 'receiver alone, explicit and native', 'FULL_EXPLICIT': 'xcar878(blind=()) == decide874 parity',
             'VIS_REPEAT': 'VIS again (repeat noise)', 'NATIVE_FULL / NATIVE_C_BLIND': 'decide874 (TEST879 arms, reported)',
             'WRONG': 'cross cells: real experience of the other world (other goal) in the same receiver',
             'SHADOW_C_SWAP': 'NOT_RUN by design: the real MISSING/LIVE pair already supplies two real C under the same X2/A; '
                              'a synthetic C of identical length would have to be fabricated',
             'POSITIVE / ADVERSE': 'LIVE experience C = mounted card that is the needed second link (positive); MISSING '
                                   'experience C = a mounted card that is not (adverse); verified offline before any read'},
    'gate2': ['C_BLIND(M) == C_BLIND(L): CAR token logps exact', 'native C_BLIND rows: receiver X K/V of all 80 layers bitwise '
              'equal (M vs L)', 'explicit final hidden of X under C_BLIND bitwise equal (M vs L)', 'EPISODE_OFF(M) == '
              'EPISODE_OFF(L) == OFF_G_ZERO exact', 'pre-C rows of E bitwise equal (M vs L)', 'FULL_EXPLICIT == NATIVE_FULL '
              'exact', 'OFF_0 explicit == native exact', 'receiver memory seal unchanged', 'C span from cartridge provenance'],
    'estimands': {'delta_C(x,a)': 'seq logp VIS_x(a) - C_BLIND(a)', 'T(a)': 'delta_C(LIVE,a) - delta_C(MISSING,a)',
                  'generic(a)': 'C_BLIND(a) - EPISODE_OFF(a)', 'slot(a)': 'EPISODE_OFF(a) - OFF_0(a)',
                  'kernel(a)': 'VIS_M(a) - FULL_EXPLICIT_M(a)', 'repeat(a)': 'VIS_M(a) - VIS_REPEAT_M(a)',
                  'floor': 'per receiver: max(5e-5, max_a |repeat|, max_a |kernel|)', 'norm': 'max over the 6 CAR words'},
    'signal_rule': 'C_SPECIFIC_READOUT_SIGNAL iff in BOTH same-goal cells: fixture valid, max|T| > floor, T(ACQUIRE) < -floor '
                   '(the positive real outcome lowers further acquisition relative to the adverse one) and max|T| > max|T| of '
                   'the cross cell into the same receiver (WRONG goal)',
    'policy_rule': 'NATIVE_POLICY_CHANGE iff signal and in a same-goal cell argmax(VIS_x) != argmax(C_BLIND) for x in {M, L}',
    'gate4': {'cell': '%s>%s' % EXEC_CELL881, 'experience': EXEC_COND881,
              'action': 'locked car873 reading on [B][E][X] (native, unmasked); INVALID/ACCEPT/STOP: terminal, nothing executed',
              'execution': 'locked execute866 in a copy of the receiver context captured at its replay step; E is decision-time '
                           'only: the post-action memory is the environment memory without E',
              'consequence': 'real next hop + evidence on the post-action memory', 'store': 'two-word STORE/DISCARD reading '
                             '(locked store_words880 procedure) with STORE_PROMPT881; REAL write only on STORE',
              'outcome_rule_offline': 'BEHAVIORAL_OUTCOME iff the real next hop class is end or the executed action mounted '
                                      'the second-link card; compared descriptively with the recorded no-memory execution',
              'store_prompt': STORE_PROMPT881},
    'informed_by': '879.log already showed, natively, larger ACQUIRE suppression with the LIVE C than with the MISSING C in both '
                   'same-goal cells: this pilot is a confirmation with path-matched arms and new controls, not a blind prediction',
    'budgets': {'wall_min': WALL_MIN881, 'peak_gib': PEAK_GIB881, 'ffe_max': FFE_MAX881,
                'ffe': '(query tokens x layers / 80) / 256 over TEST881 adapter forwards; replay forwards counted by CALLS849'},
    'labels': ['TECHNICAL_BLOCK', 'C_SPECIFIC_READOUT_SIGNAL', 'NATIVE_POLICY_CHANGE', 'BEHAVIORAL_OUTCOME',
               'BEHAVIORAL_OUTCOME_NOT_SUPPORTED', 'SEMANTIC_FAIL', 'NOT_RUN'],
    'never_reported_here': ['NATURAL_ADDRESSING', 'SF_PARITY', 'QCEP_SUCCESS', 'CLOSED_LOOP_SELF_REUSE'],
    'limits': ['two worlds, four cells, one executed action: a pilot, not a statistic', 'forced mount: no retrieval',
               'a single execution supports no comparative behavioural claim']}
PREREG_SHA881 = sha256_bytes864(_j881.dumps(PREREG881, sort_keys=True).encode())
STATE881 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO881, 'prereg_sha256': PREREG_SHA881, 'source': {}, 'api': {},
            'ref873': {}, 'targets_static': {}, 'sides': {}, 'experience': {}, 'sources': {}, 'fixtures': {}, 'receivers': {},
            'gate2': {}, 'gate3': {}, 'measure': {}, 'gate4': {}, 'budget': {'ffe': 0.0, 'ssd_bytes': 0, 'events_ms': {}},
            'not_run': [], 'blocks': [], 'verdict': None, 'error': None}
STATE878 = STATE877 = STATE881                             # the selected 877/878 functions write here
T2_KEEP878, SRC878, TGT878, EXP878, EXEC881, G881, ARMS881 = {}, {}, {}, {}, {}, {}, {}

class Gate881(Exception):
    pass

class Budget881(Exception):
    pass

class Partial878(Exception):                                   # placeholder; replaced by the locked TEST878 class at selection
    pass

def line881(*parts): short864('T881', *parts)

def scan881(node, allow=()):
    used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in _a881.walk(node) if isinstance(c, _a881.Call)}
    used |= {k.arg for k in _a881.walk(node) if isinstance(k, _a881.keyword)}
    used |= {s.slice.value for s in _a881.walk(node) if isinstance(s, _a881.Subscript) and
             isinstance(s.slice, _a881.Constant)} & {'native_append_direct', 'DirectCut3'}
    bad = (used & BANNED881) - set(allow)
    assert not bad, ('FIREWALL881', getattr(node, 'name', '?'), sorted(bad))

def oracle_scan881(node):
    names = {n.id for n in _a881.walk(node) if isinstance(n, _a881.Name)} | \
            {n.attr for n in _a881.walk(node) if isinstance(n, _a881.Attribute)}
    keys = {n.value for n in _a881.walk(node) if isinstance(n, _a881.Constant) and isinstance(n.value, str)}
    bad = (names | keys) & ORACLE881
    assert not bad, ('ORACLE_FIREWALL881', node.name, sorted(bad))

def capture_source881():
    try:
        hist = [t for t in get_ipython().history_manager.input_hist_raw if MARKER881 in t and 'def gate4_881' in t]
        source, how = hist[-1], 'IPYTHON_CELL'
    except (NameError, IndexError):
        source = open(__file__, encoding='utf-8').read() if '__file__' in globals() else None; how = 'FILE_%RUN'
    assert source and MARKER881 in source, 'EXECUTED_881_SOURCE_NOT_CAPTURED'
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
                          'firewall': 'PASS', 'oracle_firewall': 'PASS (%d runtime functions)' % len(RUNTIME881)}

def select_locked881():
    # TEST878 constants/functions and the TEST880 two-word reader, unchanged, from the blob-locked files
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
    log8 = RAW_SOURCES864['Test_878_log2.log'].decode()
    for needle in ('NVIDIA A100-SXM4-80GB', 'cell %s | prereg %s' % (LOCKS864['878.py'], TEST878_PREREG881[:16]),
                   'TEST878 | status COMPLETE'):
        assert needle in log8, ('TEST878_LOG_NOT_THE_EXPECTED_GPU_RUN', needle)
    log9 = RAW_SOURCES864['879.log'].decode()
    for needle in ('NVIDIA A100-SXM4-80GB', 'prereg 6b7d8639d93b2110', 'TEST879 VERDICT MATCHED_FORK_OUTCOME_TRANSFER',
                   'status COMPLETE'):
        assert needle in log9, ('TEST879_LOG_NOT_THE_EXPECTED_GPU_RUN', needle)
    STATE881['source']['reused'] = {'878.py': LOCKS864['878.py'], 'functions878': sorted(FUNCS878), 'constants878': len(consts),
                                    '880.py': LOCKS864['880.py'], 'functions880': sorted(FUNCS880), 'head': HEAD881}
    return log9

def ref879_881(log9):
    # TEST879 native arm probabilities of the two same-goal cells (reported reproduction only, never gated)
    out, key = {}, None
    for l in log9.splitlines():
        m = _r881.match(r'CELL (S\d\d>R\d\d) ', l)
        if m: key = m.group(1); continue
        m = _r881.match(r'\s+(FULL_[ML]|C_BLIND_[ML])\s+(\w+)\s+(.*)$', l)
        if m and key in ('S00>R00', 'S01>R01'):
            out.setdefault(key, {})[m.group(1)] = {k: float(v) for k, v in _r881.findall(r'([A-Z]+)=([0-9.]+)', m.group(3))}
    return out

def targets881(refs):
    # static gates from the locked 869 records only (no CAR result is read): the TEST879 rules
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
        f = cs[FORK_STEP878 - 1]
        ev = refs[(item, ARM878)]['events']; ix = ev.index(f)
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

# ============================ budget, timing, accounting ============================
def guard881(stage):
    el = (time.perf_counter() - T_START878) / 60.0
    free = (torch.cuda.mem_get_info()[0] + torch.cuda.memory_reserved() - torch.cuda.memory_allocated()) / 2**30
    peak = torch.cuda.max_memory_allocated() / 2**30
    why = [x for x, bad in (('WALL %.1f>%.0f min' % (el, WALL_MIN881), el > WALL_MIN881),
                            ('VRAM_FREE %.2f<%.0f GiB' % (free, FREE_MIN_GIB881), free < FREE_MIN_GIB881),
                            ('PEAK %.2f>%.0f GiB' % (peak, PEAK_GIB881), peak > PEAK_GIB881),
                            ('FFE %.1f>%.0f' % (STATE881['budget']['ffe'], FFE_MAX881), STATE881['budget']['ffe'] > FFE_MAX881)) if bad]
    if why: raise Budget881('%s: %s' % (stage, '; '.join(why)))

def ffe881(tokens, layers=80):
    STATE881['budget']['ffe'] += float(tokens) * float(layers) / 80.0 / 256.0

def timed881(tag, fn, *args, **kwargs):
    s, e = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
    s.record(); out = fn(*args, **kwargs); e.record(); torch.cuda.synchronize()
    STATE881['budget']['events_ms'][tag] = round(float(s.elapsed_time(e)), 2)
    return out

def seqlp881(reading):
    return {s['word']: float(s['sequence_logp']) for s in reading['scores']}

def cont_tokens881():
    return sum(len(ids) - 1 for _, ids in ACTION_IDS867)

def arm_record881(cell, cond, arm, reading, spans):
    rec = {'cell': cell, 'source': cond, 'arm': arm, 'action': reading['action'], 'argmax_word': reading.get('argmax_word'),
           'mass': reading.get('mass'), 'normalized': reading.get('normalized'), 'mask_spans': spans,
           'scores': [{'word': s['word'], 'ids': list(s['ids']), 'token_logps': s['token_logps'],
                       'sequence_logp': s['sequence_logp']} for s in reading['scores']]}
    ARMS881.setdefault(cell, {})['%s_%s' % (arm, cond)] = rec
    with open(ROOT864 / '881_arms.jsonl', 'a', encoding='utf-8') as f:
        f.write(_j881.dumps(rec, sort_keys=True, default=str) + '\n')
    return rec

# ============================ adapter: layout, reads, masks (runtime; no labels) ============================
def make_single_episode_layout881(env, T, S):
    # [B][E][X] in absolute storage coordinates (= RoPE positions); C span from the cartridge provenance
    n0, q = length873(env, T['m']), int(S['entry']['body_tokens'])
    sp = S['entry']['provenance']['spans_body']; L = int(T['X'].shape[0])
    lay = {'n0': n0, 'q': q, 'L': L, 'E': [n0, n0 + q], 'X2': [n0 + sp['X2'][0], n0 + sp['X2'][1]],
           'A': [n0 + sp['A'][0], n0 + sp['A'][1]], 'C': [n0 + sp['C'][0], n0 + sp['C'][1]], 'X': [n0 + q, n0 + q + L]}
    lay['N'] = n0 + q + L
    assert lay['X2'][0] == n0 and lay['X2'][1] == lay['A'][0] and lay['A'][1] == lay['C'][0] and lay['C'][1] == n0 + q, \
        ('LAYOUT_SPANS', lay)                              # C is the last segment of E: no E row was computed from C
    assert lay['C'][1] - lay['C'][0] == int(S['body']) and sp['C'][1] == q, ('C_SPAN_PROVENANCE', lay, S['body'])
    assert lay['N'] + max(len(ids) for _, ids in ACTION_IDS867) <= int(env['MAX_FUSED_TOKENS']), ('MAX_FUSED_TOKENS', lay['N'])
    lay['sha256'] = sha256_bytes864(_j881.dumps(lay, sort_keys=True).encode())
    return lay

def xread881(env, kv, X, blind, sham, tag):
    # explicit-layer CAR (locked xcar878): own cache from the immutable kv; X and every continuation under `blind`
    ffe881(int(X.shape[0]) + cont_tokens881())
    return timed881(tag, xcar878, env, kv, X, [tuple(b) for b in blind], sham)

def nread881(env, kv, X, ranges, rows, tag):
    # native-model CAR (locked decide874) with the same 2-D keep mask on X and every continuation
    ffe881(int(X.shape[0]) + cont_tokens881())
    r, got, _, _ = timed881(tag, decide874, env, kv, X, [tuple(b) for b in ranges], rows)
    return r, got

def xhidden881(env, kv, X, blind):
    # explicit 80-layer forward of X only (no continuation) under `blind`: SHA-256 of the final hidden rows
    ffe881(int(X.shape[0])); cache = env['cache_build'](list(kv)); nc = int(cache.get_seq_length()); L = int(X.shape[0])
    am = torch.ones((1, nc + L), device=env['DEV'], dtype=torch.long)
    for a, b in blind: am[0, a:b] = 0
    h = xspan878(env, cache, X.reshape(1, L, int(env['H'])), am, 0, int(env['NL']), (), ())
    digest = _h881.sha256(h.detach().float().cpu().contiguous().numpy().tobytes()).hexdigest()
    del cache, h
    return digest

def zero_slot881(env, kv, a, b):
    # new tensors: rows a:b of every layer K/V replaced by zeros (the immutable source tensors are not written)
    out = []
    for k, v in kv:
        k2, v2 = k.clone(), v.clone(); k2[:, :, a:b] = 0; v2[:, :, a:b] = 0; out.append((k2, v2))
    return out

def same_rows881(ra, rb):
    return len(ra) == len(rb) and all(torch.equal(x[0], y[0]) and torch.equal(x[1], y[1]) for x, y in zip(ra, rb))

# ============================ GATE1: sources (real experiences), persistence, fixtures ============================
def sources881(env):
    for w in WORLDS878:
        M, L = SRC878.get('I867_%s_MISSING' % w), SRC878.get('I867_%s_LIVE' % w)
        R = STATE881['sources'].setdefault(w, {})
        if M is None or L is None: raise Gate881('SOURCE_EXPERIENCE_NOT_CAPTURED ' + w)
        R['gates'] = g = {'same_t2_spans': (M['n2'], M['L2'], M['la']) == (L['n2'], L['L2'], L['la']),
                          'same_action_tokens': M['A_ids'] == L['A_ids'] and M['t2_action'] == L['t2_action'] == ACTION878,
                          'real_cards_differ': M['card'] != L['card'], 'same_C_length': M['body'] == L['body'],
                          'pre_C_cartridge_rows_bitwise': M['entry']['pre_C_seal'] == L['entry']['pre_C_seal'],
                          'same_goal': M['qid'] == L['qid'], 'real_namespace': all(str(EXP_DIR878) in S['entry']['file'] for S in (M, L))}
        if not all(g.values()): raise Gate881('SOURCE_PAIR_GATES %s %s' % (w, _j881.dumps(g)))
        guard881('persist_' + w)
        R['persistence'] = {S['cond']: persist878(env, S) for S in (M, L)}
        STATE881['budget']['ssd_bytes'] += sum(int(S['entry']['bytes']) for S in (M, L))
        ffe881(4 * (int(M['entry']['body_tokens']) + int(M['X3'].shape[0])))
        if not all(r['pass'] for r in R['persistence'].values()): raise Gate881('PERSISTENCE_FAIL ' + w)
        line881('SOURCE', w, 'gates', _j881.dumps(g, sort_keys=True), 'persist',
                _j881.dumps({k: [r['pass'], round(r['max_dp'], 5)] for k, r in R['persistence'].items()}))

def fixture_seal881(env, by_key):
    # OFFLINE labels, sealed before any receiver read: which mounted card each experience's C is (never used at runtime)
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

# ============================ GATE2: masks, invariance, parity ============================
def gate2_881(env):
    for r in WORLDS878:
        T = TGT878.get(('FORK', r))
        if T is None: raise Gate881('RECEIVER_NOT_CAPTURED_OR_RECORD_NOT_REPRODUCED R' + r)
        guard881('receiver_' + r); seal0 = prefix_seals865(env, T['m'])
        b_nat, _ = nread881(env, T['m'], T['X'], [], False, 'R%s_OFF0_native' % r)
        b_x = xread881(env, T['m'], T['X'], (), False, 'R%s_OFF0_explicit' % r)
        STATE881['receivers'][r] = {'item': T['item'], 'qid_sha256': sha256_bytes864(T['qid'].encode()), 'mounted': T['mounted'],
                                    'X_len': T['X_len'], 'memory_tokens': length873(env, T['m']), 'seal0': seal0,
                                    'OFF0_explicit_equals_native': same873(b_nat, b_x)}
        arm_record881('R' + r, '-', 'OFF_0', b_x, [])
        if not STATE881['receivers'][r]['OFF0_explicit_equals_native']: raise Gate881('OFF0_EXPLICIT_NOT_NATIVE R' + r)
    for s, r in CELLS881:
        key = '%s>%s' % (s, r); T = TGT878[('FORK', r)]; same_goal = s == r
        M, L = SRC878['I867_%s_MISSING' % s], SRC878['I867_%s_LIVE' % s]
        if (T['qid'] == M['qid']) != same_goal or set(T['mounted']) & {M['card'], L['card']}: raise Gate881('RUNTIME_INDEPENDENCE ' + key)
        lay = {c: make_single_episode_layout881(env, T, S) for c, S in (('M', M), ('L', L))}
        if {k: v for k, v in lay['M'].items() if k != 'sha256'} != {k: v for k, v in lay['L'].items() if k != 'sha256'}:
            raise Gate881('LAYOUT_M_NE_L ' + key)
        Ly = lay['M']; C, E = Ly['C'], Ly['E']; X = T['X']
        guard881('gate2_' + key); g = {}
        for c, S in (('M', M), ('L', L)):
            cp = load_exp878(env, S['entry']); STATE881['budget']['ssd_bytes'] += int(S['entry']['bytes'])
            g[c] = timed881('%s_append_%s' % (key, c), append_exp878, env, T['m'], cp); del cp
            ffe881(Ly['q'], 76)
            if g[c] is T['m'] or any(a[0] is b[0] for a, b in zip(g[c], T['m'])): raise Gate881('ALIAS_RECEIVER_MEMORY ' + key)
        G881[key] = g
        G = STATE881['gate2'][key] = {'relation': 'SAME_GOAL' if same_goal else 'CROSS', 'layout': Ly, 'checks': {}}
        ck = G['checks']
        ck['pre_C_rows_bitwise_M_eq_L'] = all(torch.equal(a[0][:, :, E[0]:C[0]], b[0][:, :, E[0]:C[0]]) and
                                             torch.equal(a[1][:, :, E[0]:C[0]], b[1][:, :, E[0]:C[0]]) for a, b in zip(g['M'], g['L']))
        ck['C_rows_differ_M_vs_L'] = not all(torch.equal(a[1][:, :, C[0]:C[1]], b[1][:, :, C[0]:C[1]]) for a, b in zip(g['M'], g['L']))
        cb = {c: xread881(env, g[c], X, [C], False, '%s_CBLIND_%s' % (key, c)) for c in 'ML'}
        for c in 'ML': arm_record881(key, c, 'C_BLIND', cb[c], [C])
        ck['C_BLIND_M_equals_L_exact'] = same873(cb['M'], cb['L'])
        if same_goal:
            nb = {c: nread881(env, g[c], X, [C], True, '%s_NCBLIND_%s' % (key, c)) for c in 'ML'}
            for c in 'ML': arm_record881(key, c, 'NATIVE_C_BLIND', nb[c][0], [C])
            ck['native_C_BLIND_M_equals_L_exact'] = same873(nb['M'][0], nb['L'][0])
            ck['native_C_BLIND_receiver_X_KV_80_layers_bitwise'] = same_rows881(nb['M'][1], nb['L'][1]); del nb
            ck['C_BLIND_final_hidden_bitwise'] = xhidden881(env, g['M'], X, [C]) == xhidden881(env, g['L'], X, [C])
            eo = {c: xread881(env, g[c], X, [E], False, '%s_EOFF_%s' % (key, c)) for c in 'ML'}
            z = zero_slot881(env, g['M'], E[0], E[1])
            oz = xread881(env, z, X, [E], False, '%s_OFFGZERO' % key); del z
            for c in 'ML': arm_record881(key, c, 'EPISODE_OFF', eo[c], [E])
            arm_record881(key, '-', 'OFF_G_ZERO', oz, [E])
            ck['EPISODE_OFF_M_eq_L_eq_OFF_G_ZERO_exact'] = same873(eo['M'], eo['L']) and same873(eo['M'], oz)
            fx = xread881(env, g['M'], X, (), False, '%s_FULLX_M' % key); fn, _ = nread881(env, g['M'], X, [], False, '%s_NFULL_M' % key)
            arm_record881(key, 'M', 'FULL_EXPLICIT', fx, []); arm_record881(key, 'M', 'NATIVE_FULL', fn, [])
            ck['FULL_EXPLICIT_equals_NATIVE_FULL_exact'] = same873(fx, fn)
            fnl, _ = nread881(env, g['L'], X, [], False, '%s_NFULL_L' % key); arm_record881(key, 'L', 'NATIVE_FULL', fnl, [])
        ck['receiver_memory_unchanged'] = prefix_seals865(env, T['m']) == STATE881['receivers'][r]['seal0']
        ck['finite'] = all(math.isfinite(x) for rd in ARMS881[key].values() for s_ in rd['scores'] for x in s_['token_logps'])
        G['pass'] = all(ck.values())
        line881('GATE2', key, G['relation'], 'pass=%s' % G['pass'], _j881.dumps(ck, sort_keys=True))
        if not G['pass']: raise Gate881('GATE2_FAIL %s %s' % (key, _j881.dumps({k: v for k, v in ck.items() if not v})))

# ============================ GATE3: readout ============================
def gate3_881(env):
    for s, r in CELLS881:
        key = '%s>%s' % (s, r); T = TGT878[('FORK', r)]; X = T['X']; g = G881[key]; C = STATE881['gate2'][key]['layout']['C']
        guard881('gate3_' + key)
        for c in 'ML':
            arm_record881(key, c, 'VIS', xread881(env, g[c], X, [C], True, '%s_VIS_%s' % (key, c)), [C])
        if s == r:
            arm_record881(key, 'M', 'VIS_REPEAT', xread881(env, g['M'], X, [C], True, '%s_VISREP_M' % key), [C])
        STATE881['gate3'][key] = {'reads_done': sorted(ARMS881[key])}
        line881('GATE3', key, 'arms=%d' % len(ARMS881[key]))
        if (s, r) != EXEC_CELL881:
            del G881[key]; gc.collect(); torch.cuda.empty_cache()

def measure881():
    # OFFLINE: estimands, floors, pre-registered rules (fixtures read here, after every read)
    W = [w for w, _ in ACTION_IDS867]; out = {}; lp = lambda key, name: seqlp881(ARMS881[key][name])
    norm = lambda d: max(abs(x) for x in d.values())
    for s, r in CELLS881:
        key = '%s>%s' % (s, r); vm, vl, cb = lp(key, 'VIS_M'), lp(key, 'VIS_L'), lp(key, 'C_BLIND_M')
        d = {'delta_C_M': {a: vm[a] - cb[a] for a in W}, 'delta_C_L': {a: vl[a] - cb[a] for a in W}}
        d['T'] = {a: d['delta_C_L'][a] - d['delta_C_M'][a] for a in W}
        d['argmax'] = {k: ARMS881[key][k]['action'] for k in ('VIS_M', 'VIS_L', 'C_BLIND_M')}
        d['probs'] = {k: ARMS881[key][k]['normalized'] for k in ('VIS_M', 'VIS_L', 'C_BLIND_M')}
        if s == r:
            eo, off0, fx, rep = lp(key, 'EPISODE_OFF_M'), seqlp881_off0(r), lp(key, 'FULL_EXPLICIT_M'), lp(key, 'VIS_REPEAT_M')
            d['generic'] = {a: cb[a] - eo[a] for a in W}; d['slot'] = {a: eo[a] - off0[a] for a in W}
            d['kernel'] = {a: vm[a] - fx[a] for a in W}; d['repeat'] = {a: vm[a] - rep[a] for a in W}
            d['floor'] = max(SIG_MIN878, norm(d['repeat']), norm(d['kernel']))
            d['visible_C_differs_M_vs_L'] = vm != vl
        out[key] = d
    for s, r in CELLS881:
        key = '%s>%s' % (s, r); d = out[key]; fl = out['%s>%s' % (r, r)]['floor']; d['floor_used'] = fl
        d['norm_T'] = norm(d['T']); d['T_exceeds_floor'] = d['norm_T'] > fl
    rules = {}
    for w in WORLDS878:
        key, cross = '%s>%s' % (w, w), [k for k in out if k.endswith('>' + w) and not k.startswith(w + '>')][0]
        d = out[key]; fx = FIXTURE881.get(w, {})
        rules[key] = {'fixture_valid': bool(fx.get('valid')), 'norm_T_gt_floor': d['norm_T'] > d['floor'],
                      'T_ACQUIRE_lt_minus_floor': d['T']['ACQUIRE'] < -d['floor'],
                      'norm_T_gt_cross': d['norm_T'] > out[cross]['norm_T'], 'cross_cell': cross}
        rules[key]['pass'] = all(v for k, v in rules[key].items() if k != 'cross_cell')
        rules[key]['argmax_change'] = {x: d['argmax']['VIS_' + x] != d['argmax']['C_BLIND_M'] for x in 'ML'}
    signal = all(rules[k]['pass'] for k in rules)
    policy = signal and any(any(v['argmax_change'].values()) for v in rules.values())
    STATE881['measure'] = {'cells': out, 'rules': rules, 'C_SPECIFIC_READOUT_SIGNAL': signal, 'NATIVE_POLICY_CHANGE': policy}
    return STATE881['measure']

def seqlp881_off0(r):
    return seqlp881(ARMS881['R' + r]['OFF_0_-'])

# ============================ GATE4: one real action, real consequence, model STORE, atomic REAL write ============================
def store_reading881(env, memx, q, act_rows, c_new, e_new):
    X, _ = env['make_x851'](list(env['prompt_ids'](STORE_PROMPT881.format(q=q))),
                            [(SLOTS881['ACTED'], act_rows), (env['C_SLOT851'], c_new), (env['E_SLOT851'], e_new)],
                            SLOTS881['STORE_SUFFIX'])
    ffe881(int(X.shape[0]) + max(len(ids) for _, ids in WORDS880))
    r = store_words880(env, memx, X); del X
    return r

def atomic_append_real881(env, eid, gH, h3, n2, x3s, pre_rows, prov):
    # locked write_exp878 (tmp + rename) into the REAL namespace, then fsync file + directory, SSD reload with every SHA,
    # then one fsynced catalog line. Any failure: the files are moved to quarantine (never deleted), the gate fails.
    global EXP_DIR878
    old_dir, EXP_DIR878 = EXP_DIR878, REAL_GATE4_DIR881
    path = REAL_GATE4_DIR881 / (eid + '.pt'); tmp = REAL_GATE4_DIR881 / (eid + '.pt.tmp')
    try:
        entry = write_exp878(env, eid, gH, h3, n2, x3s, pre_rows, prov)
        fd = _o881.open(str(path), _o881.O_RDONLY); _o881.fsync(fd); _o881.close(fd)
        dfd = _o881.open(str(REAL_GATE4_DIR881), _o881.O_RDONLY); _o881.fsync(dfd); _o881.close(dfd)
        g = load_exp878(env, entry); del g
        if entry['roundtrip_K_rel'] > ROPE_TOL878: raise Gate881('ROUNDTRIP_K %.3e' % entry['roundtrip_K_rel'])
        line = _j881.dumps({'id': eid, 'namespace': 'REAL', 'file': entry['file'], 'sha256': entry['sha256'],
                            'tensor_sha': entry['tensor_sha'], 'bytes': entry['bytes'], 'parent': prov.get('parent_experience'),
                            'catalog_generation': 1}, sort_keys=True)
        with open(REAL_CATALOG881, 'a', encoding='utf-8') as f:
            f.write(line + '\n'); f.flush(); _o881.fsync(f.fileno())
        return entry
    except BaseException:
        QUARANTINE881.mkdir(parents=True, exist_ok=True)
        for p in (path, tmp):
            if p.exists(): _o881.replace(str(p), str(QUARANTINE881 / p.name))
        raise
    finally:
        EXP_DIR878 = old_dir

def gate4_881(env):
    s, r = EXEC_CELL881; key = '%s>%s' % (s, r); T = TGT878[('FORK', r)]; S = SRC878['I867_%s_%s' % (s, EXEC_COND881)]
    Ex = EXEC881.get(T['item'])
    if Ex is None: raise Gate881('GATE4_RECEIVER_CONTEXT_NOT_CAPTURED')
    guard881('gate4'); out = STATE881['gate4']; ck = out['checks'] = {}
    cut, dev, Hd = APPEND873['CUT'], env['DEV'], int(env['H']); q = env['QTEXT841'][T['qid']]; X = T['X']
    g = G881[key][EXEC_COND881[0]]
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
    X_chk, _ = env['make_x851'](pre, list(Ex['segments']), post); ck['X_rebuilt_equals_receiver_X'] = bool(torch.equal(X_chk, X))
    m2 = [tuple(t.clone() for t in kv) for kv in g]; n2, L2 = length873(env, m2), int(X.shape[0])
    cache = env['cache_build'](list(m2)); ffe881(L2 + cont_tokens881())
    rd = car873(env, cache, X)                               # the model-native reading with the experience physically present
    out['reading'] = {'action': rd['action'], 'normalized': rd['normalized'], 'mass': rd['mass'],
                      'scores': [{'word': x['word'], 'sequence_logp': x['sequence_logp']} for x in rd['scores']]}
    out['native_FULL_equals_car873'] = same873(rd, ARMS881[key]['NATIVE_FULL_%s' % EXEC_COND881[0]]) if \
        ('NATIVE_FULL_%s' % EXEC_COND881[0]) in ARMS881[key] else None
    legacy = env['gen851'](g, pre, list(Ex['segments']), post); check_output_h863(legacy, 'T881_CONTROL_ROWS')
    ffe881(L2 + 8); out['generated_control_text'] = legacy['text']
    h, kind = hop865(env, T['m'], T['qid'], len(Ex['path']), Ex['path'][-1]['rows'] if Ex['path'] else None)
    ffe881(64); ck['candidate_reproduces_record'] = h['text'] == Ex['candidate_text']
    action = rd['action']; out['native_action'] = action
    if action in ('INVALID', 'ACCEPT', 'STOP') or not all(ck.values()):
        out['executed'] = None; out['terminal_or_blocked'] = action if all(ck.values()) else 'GATE4_CHECKS'
        del cache, m2; return out
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
    ctx = {'spec': dict(Ex['spec']), 'arm': ARM878, 'M': list(T['mounted']), 'memx': g, 'path': [dict(p) for p in Ex['path']],
           'events': [], 'mount_records': [], 'acquisitions': 0, 'rejections': 0, 'addresses': 0, 'steps': Ex['steps']}
    execute866(env, ctx, action, h, legacy, {'segments': list(Ex['segments'])})       # the literal model word, locked executor
    eff = ctx['events'][-1]; out['executed'] = {k: eff.get(k) for k in ('action', 'effect', 'chosen', 'mounted_before',
                                                                        'mounted_after', 'path_after', 'direction_text')}
    ck['executed_equals_native_action'] = eff.get('action') == action
    ck['mount_integrity'] = all(m['n_exact'] and m['all_80_layers'] and m['finite'] for m in ctx['mount_records'])
    obs_mem = T['m'] if ctx['memx'] is g else ctx['memx']   # E is decision-time only: environment memory after the action
    k1 = len(ctx['path']); h1, kind1 = hop865(env, obs_mem, T['qid'], k1, ctx['path'][-1]['rows'] if k1 else None)
    ev1 = env['gen849'](obs_mem, list(env['prompt_ids'](env['EVIDENCE851'].format(q=q))), None, env['ANSWER_SUFFIX851'])
    check_output_h863(ev1, 'T881_EVIDENCE'); ffe881(128)
    c_new, e_new = h1['rows'].detach().float().cpu(), ev1['rows'].detach().float().cpu()
    out['observation'] = {'hop_text': h1['text'], 'hop_kind': kind1, 'evidence_text': ev1['text'],
                          'C_rows': int(c_new.shape[0]), 'E_rows': int(e_new.shape[0])}
    if not (c_new.ndim == 2 and c_new.shape[0] and e_new.ndim == 2 and e_new.shape[0]):
        out['store'] = {'decision': None, 'why': 'EMPTY_OBSERVATION_ROWS'}; out['written'] = None
        del keep, cl, hx, ha; return out
    act_rows = env['embed841'](A).detach().float().cpu()
    sr = store_reading881(env, obs_mem, q, act_rows, c_new, e_new)
    out['store'] = {'decision': sr['decision'], 'mass': sr['mass'], 'normalized': sr['normalized']}
    out['written'] = None
    if sr['decision'] == 'STORE' and all(ck.values()):
        n1 = n2 + L2 + la; P = int(env['P'])
        Y, _ = env['make_x851'](env['C_SLOT851'], [([], c_new), (env['E_SLOT851'], e_new)], []); body = int(Y.shape[0])
        own2 = env['cache_build'](list(keep)); forward873(env, own2, Y, n1); gH = kv873(env, own2); del own2
        h3c = xspan878(env, cl, Y.reshape(1, body, Hd), one(n1 + body), 0, cut + 1); ffe881(body, 80 + cut + 1)
        ck['C_explicit_lower_KV_bitwise'] = all(torch.equal(a_[:, :, n1:], b_[:, :, n1:n1 + body]) for i in range(cut + 1)
                                                for a_, b_ in zip(cache_kv870(cl, i), gH[i]))
        ck['C_h3_next_layer_KV_bitwise'] = all(torch.equal(a_, b_[:, :, n1:n1 + body]) for a_, b_ in
                                               zip(next_kv878(env, h3c, n1), gH[cut + 1]))
        if all(ck.values()):
            prov = {'namespace': 'REAL', 'test': 'TEST881', 'receiver_item': T['item'], 'receiver_step': Ex['steps'],
                    'qid_sha256': sha256_bytes864(T['qid'].encode()), 'parent_experience': S['entry']['id'],
                    'parent_experience_sha256': S['entry']['sha256'], 'action': action, 'action_token_ids': list(A),
                    'effect': eff.get('effect'), 'chosen': eff.get('chosen'), 'C_kind': 'NEXT_OBSERVATION',
                    'spans_body': {'X2': [0, L2], 'A': [L2, L2 + la], 'C': [L2 + la, L2 + la + body]},
                    'source_storage_positions': [n2, n1 + body], 'cartridge_positions': [P, P + n1 + body - n2],
                    'store_reading': {'decision': sr['decision'], 'mass': sr['mass']}, 'weights_digest': WEIGHTS0_878,
                    'engine_git_blob': ENGINE_BLOB881, 'head': HEAD881, 'cell_git_blob': STATE881['source'].get('executed_cell_git_blob'),
                    'layout_sha256': STATE881['gate2'][key]['layout']['sha256'], 'contains': 'native h3 + L0-3 K/V of [X2][A][C] only'}
            eid = 'X881_' + sha256_bytes864(_j881.dumps(prov, sort_keys=True).encode())[:12]
            entry = atomic_append_real881(env, eid, gH, torch.cat([hx, ha, h3c], dim=1), n2, n1 + body, L2 + la, prov)
            out['written'] = {k: entry[k] for k in ('id', 'file', 'sha256', 'bytes', 'body_tokens', 'roundtrip_K_rel', 'pre_C_seal')}
            STATE881['budget']['ssd_bytes'] += int(entry['bytes'])
        del gH, h3c, Y
    del keep, cl, hx, ha
    gc.collect(); torch.cuda.empty_cache()
    return out

def eval_gate4_881(env, by_key):
    # OFFLINE: label of the real consequence; descriptive comparison with the recorded no-memory execution
    G = STATE881['gate4']
    if not G.get('executed'): return
    r = EXEC_CELL881[1]; spec = by_key[(int(r), 'FORK')]; w = world867(env, spec); kind = {v: k for k, v in w['ids'].items()}
    cls = env['node851'](G['observation']['hop_text'], w); mk = kind.get(G['executed'].get('chosen'), None)
    rec = STATE881['targets_static']['receivers'][r]
    G['offline'] = {'next_hop_class': cls, 'mounted_card_kind': mk,
                    'supported': cls == 'end' or (G['executed'].get('effect') == 'MOUNTED' and mk == 'second'),
                    'recorded_no_memory': {'action': rec['recorded_action'], 'effect': rec['recorded_effect'],
                                           'effect_card_kind': kind.get((rec['recorded_effect'] or {}).get('chosen')),
                                           'next_hop_class': env['node851'](rec['recorded_next_hop_raw'] or '', w)}}

# ============================ replay tap: TEST878 probe + the receiver context for GATE4 ============================
def probe881(env, ctx, record, state, label):
    probe878(env, ctx, record, state, label)
    side = ctx['spec']['item']
    if side.endswith('_FORK') and ctx['steps'] == FORK_STEP878 and side.split('_')[1] == EXEC_CELL881[1]:
        EXEC881[side] = {'spec': {k: (list(v) if isinstance(v, (list, tuple)) else v) for k, v in ctx['spec'].items() if k != 'xray'},
                         'segments': [(list(s_), r_.detach().float().cpu().clone()) for s_, r_ in state['segments']],
                         'path': [{'rows': p['rows'].detach().float().cpu().clone(), 'text': p['text']} for p in ctx['path']],
                         'steps': ctx['steps'], 'candidate_text': record.get('candidate_text')}

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
        m = STATE881['measure']
        labels.append('C_SPECIFIC_READOUT_SIGNAL' if m['C_SPECIFIC_READOUT_SIGNAL'] else 'SEMANTIC_FAIL')
        if m['NATIVE_POLICY_CHANGE']: labels.append('NATIVE_POLICY_CHANGE')
        g4 = STATE881['gate4']
        if g4.get('offline'): labels.append('BEHAVIORAL_OUTCOME' if g4['offline']['supported'] else 'BEHAVIORAL_OUTCOME_NOT_SUPPORTED')
        v = labels[0]
    STATE881['verdict'] = {'verdict': v, 'labels': labels, 'blocks': blocks, 'not_run': STATE881['not_run'],
                           'never_reported': PREREG881['never_reported_here'], 'limits': PREREG881['limits']}
    return STATE881['verdict']

def report881():
    W = [w for w, _ in ACTION_IDS867]
    print('=' * 112)
    print('TEST881 PILOT-0 C VISIBILITY -> NATIVE CAR | GPU %s | head %s | cell %s | prereg %s' % (CC_GPU.get('name'), HEAD881[:12],
          STATE881['source'].get('executed_cell_git_blob'), PREREG_SHA881[:16]))
    print('FIXTURES %s' % _j881.dumps(STATE881.get('fixtures', {}).get('rows'), sort_keys=True))
    for r, R in STATE881['receivers'].items():
        print('RECEIVER R%s %s memory=%s X=%s OFF0_explicit==native %s' % (r, R['item'], R['memory_tokens'], R['X_len'],
              R['OFF0_explicit_equals_native']))
    for key, G in STATE881['gate2'].items():
        print('GATE2 %s %-9s pass=%s layout E=%s C=%s X=%s | %s' % (key, G['relation'], G.get('pass'), G['layout']['E'],
              G['layout']['C'], G['layout']['X'], _j881.dumps(G['checks'], sort_keys=True)))
        for name, a in sorted(ARMS881.get(key, {}).items()):
            print('    %-18s %-9s %s' % (name, a['action'], ' '.join('%s=%.4f' % (w_, (a['normalized'] or {}).get(w_, float('nan'))) for w_ in W)))
    m = STATE881.get('measure') or {}
    for key, d in (m.get('cells') or {}).items():
        print('MEASURE %s |T|=%.4f floor=%.5f T=%s dC_M=%s dC_L=%s' % (key, d['norm_T'], d['floor_used'],
              _j881.dumps({a: round(x, 4) for a, x in d['T'].items()}), _j881.dumps({a: round(x, 4) for a, x in d['delta_C_M'].items()}),
              _j881.dumps({a: round(x, 4) for a, x in d['delta_C_L'].items()})))
        for extra in ('generic', 'slot', 'kernel', 'repeat'):
            if extra in d: print('    %-8s %s' % (extra, _j881.dumps({a: round(x, 5) for a, x in d[extra].items()})))
    print('RULES %s' % _j881.dumps(m.get('rules'), sort_keys=True))
    print('GATE4 %s' % _j881.dumps(STATE881.get('gate4'), sort_keys=True, default=str)[:3000])
    b = STATE881['budget']
    print('BUDGET ffe=%.1f/%.0f ssd_bytes=%d calls849=%s' % (b['ffe'], FFE_MAX881, b['ssd_bytes'], env881['CALLS849'] if 'env881' in globals() else None))
    v = STATE881['verdict'] or {}
    print('TEST881 VERDICT %s | labels %s | blocks %s | not_run %s' % (v.get('verdict'), v.get('labels'), v.get('blocks'), v.get('not_run')))
    print('LIMITS: %s' % '; '.join(PREREG881['limits']))
    print('status %s | wall %.0f s | peak allocated %.2f GiB | peak reserved %.2f GiB | GPU_EXECUTION_NOT_VERIFIED_BY_AUTHOR' % (
          STATE881['status'], time.perf_counter() - T_START878, torch.cuda.max_memory_allocated() / 2**30 if torch.cuda.is_available() else 0.0,
          torch.cuda.max_memory_reserved() / 2**30 if torch.cuda.is_available() else 0.0))
    print('=' * 112)

# ============================ single cell execution ============================
FIXTURE881 = {}
T_START878 = time.perf_counter()
try:
    STATE881['status'] = 'GATE0_SOURCE'; capture_source881()
    json_write864('881_prereg.json', {'prereg': PREREG881, 'sha256': PREREG_SHA881, 'before_model_load': True})
    line881('GATE0 PREREG', PREREG_SHA881)
    du = _s881.disk_usage(str(ROOT864)); STATE881['budget']['disk_free_gib'] = round(du.free / 2**30, 1)
    if du.free / 2**30 < DISK_MIN_GIB881: raise Gate881('DISK_FREE %.1f GiB' % (du.free / 2**30))
    load_sources865(); log879 = select_locked881(); xray_point870 = probe881
    source_audit878(); load878(); STATE881['ref873'] = ref873_874(RAW_SOURCES864['873.log'].decode())
    STATE881['ref879'] = ref879_881(log879)
    feasibility_audit864(); audit_contracts865(); load_spine864(); REFS881 = load_records870()
    STATE881['targets_static'] = targets881(REFS881)
    STATIC_T2_SHA878 = {s: [e['record'] for e in REFS881[(s, ARM878)]['events'] if e['type'] == 'CONTROL'][PRE_STEP878 - 1]['state_sha256']
                        for s in SOURCES878}
    line881('GATE0 SOURCE PASS', _j881.dumps(STATE881['source'], sort_keys=True))
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
        'gen851', 'gen849', 'C_SLOT851', 'E_SLOT851', 'EVIDENCE851', 'ANSWER_SUFFIX851', 'REVIEW_SUFFIX851')), 'ENGINE_NAMESPACE'
    EXP878['CHUNK'] = int(chunk881[0])
    REAL_DIR881 = ROOT864 / 'REAL_NAMESPACE_881'; SHADOW_DIR881 = ROOT864 / 'SHADOW_NAMESPACE_881'
    EXP_DIR878 = REAL_DIR881 / 'replayed_sources'; REAL_GATE4_DIR881 = REAL_DIR881 / 'gate4'
    QUARANTINE881 = REAL_DIR881 / 'quarantine'; REAL_CATALOG881 = REAL_DIR881 / 'catalog.jsonl'
    for d_ in (EXP_DIR878, REAL_GATE4_DIR881, SHADOW_DIR881): d_.mkdir(parents=True, exist_ok=False)
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
    STATE881['status'] = 'GATE2_MASK'; gate2_881(env881)
    STATE881['status'] = 'GATE3_READOUT'; gate3_881(env881); measure881()
    STATE881['status'] = 'GATE4_EXECUTION'
    try:
        gate4_881(env881); eval_gate4_881(env881, by_key881)
    finally:
        G881.clear(); gc.collect(); torch.cuda.empty_cache()
    hook881 = hook_audit859(env881, 'T881_final')
    if records_digest861(env881) != digest881 or physical_seal863(env881, env881['MEMNULL841']) != null_seal881 or \
            hook881['hook_count'] or hook881['transformers_output_capturing_installed'] or weights_digest877(env881) != WEIGHTS0_878:
        STATE881['blocks'].append('POST_RUN_INTEGRITY')
    g4c = STATE881['gate4'].get('checks') or {}
    if g4c and not all(g4c.values()): STATE881['blocks'].append('GATE4_CHECKS %s' % sorted(k for k, v in g4c.items() if not v))
    STATE881['status'] = 'COMPLETE'; verdict881()
except Budget881 as exc:
    STATE881['error'] = str(exc); STATE881['not_run'].append('BUDGET_ABORT_AT_%s: %s' % (STATE881['status'], exc))
    STATE881['status'] = 'NOT_RUN_AT_' + str(STATE881['status']); verdict881()
except Partial878 as exc:
    STATE881['error'] = str(exc); STATE881['not_run'].append('TEST878_GUARD_AT_%s: %s' % (STATE881['status'], exc))
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
        json_write864('881_result.json', jsafe878(dict(STATE881, replays=STATE870['replays'], prereg=PREREG881)) if 'jsafe878' in globals()
                      else json.loads(json.dumps(dict(STATE881, replays=STATE870['replays']), default=str)))
    except Exception as exc: print('RESULT_WRITE_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    try: report881()
    except Exception as exc: print('REPORT_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE881['suffix'], 'test870.py:suffix', 'exec'), globals())
