# AKBASCORE SILICON HIPPOCAMPUS — TEST879 — FORK<->FORK SOURCE-RECEIVER CROSSOVER
# One A100-SXM4-80GB Colab cell. Frozen Qwen2.5-72B-Instruct NF4, BF16. Locked engine test870.py (e322ed8) + locked 878.py.
# QUESTION: is TEST878's asymmetric outcome-dependent transfer source-bound, receiver-bound, same-goal-restricted or a
# source x receiver interaction when every receiver has the same provenance (V_X FORK, step 1)?
# Matrix: sources S01, S00 (real MISSING/LIVE Experience-CUT3 pairs) x receivers R01 = I867_01_FORK, R00 = I867_00_FORK.
# Per receiver: BASE, BASE_EXPLICIT. Per cell: FULL_M, FULL_L, C_BLIND_M, C_BLIND_L. Nothing is executed.
# Reuse: the TEST878 capture / write / free / reload / append / persistence / CAR functions are executed byte-identical by
# AST selection from the git-blob-locked 878.py (the file the second TEST878 A100 run executed). New code: the matrix only.
# Never: weight writes, training, hooks, output_hidden_states/attentions, logit edits, action forcing, activation patches.
import ast as _a879, hashlib as _h879, json as _j879, re as _r879, urllib.request as _u879
ENGINE_URL879 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB879, MARKER879 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', 'AKBASCORE SILICON HIPPOCAMPUS — TEST879'

def blob879(raw):
    return _h879.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()

def engine_parts879():
    with _u879.urlopen(_u879.Request(ENGINE_URL879, headers={'User-Agent': 'AKBASCORE-TEST879'}), timeout=240) as r:
        raw = r.read()
    assert blob879(raw) == ENGINE_BLOB879, ('ENGINE_BLOB_MISMATCH', blob879(raw))
    text = raw.decode('utf-8'); _a879.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST879_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST879_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST879_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('879_engine.log', '879_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST879_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '879_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '879_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST879_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old)
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL879, 'git_blob': blob879(raw), 'sha256': _h879.sha256(raw).hexdigest()}

try:
    ENGINE879, ENGINE_INFO879 = engine_parts879()
except BaseException as _exc879:      # console capture starts inside the engine prefix: keep a local record of this failure
    import time as _t879, traceback as _tb879
    _p879 = '/content/TEST879_PRE_ENGINE_ERROR_%s.txt' % _t879.strftime('%Y%m%dT%H%M%SZ', _t879.gmtime())
    try:
        with open(_p879, 'w', encoding='utf-8') as _f879: _f879.write(_tb879.format_exc())
    except OSError: _p879 = 'NOT_WRITTEN'
    print('TEST879 PRE-ENGINE ERROR (before console capture):', type(_exc879).__name__, _exc879, '| traceback:', _p879)
    raise
exec(compile(ENGINE879['prefix'], 'test870.py:prefix', 'exec'), globals())
exec(compile(ENGINE879['body'], 'test870.py:engine', 'exec'), globals())
print('TEST879 ENGINE', _j879.dumps(ENGINE_INFO879, sort_keys=True))

# ============================ locks and pre-registration (fixed before the model is loaded) ============================
LOCKS864.update({'test870.py': ENGINE_BLOB879, 'Test870.log': 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc',
                 '873.py': '2e44affa5e0dd462155fb265c331270fb8e7b7e1', '873.log': '1c9eb9fca173003eaf45bc7726af13c2817324b7',
                 '874.py': '12172001ba3696ad91087a8b34d7995728259e47', '874.log': '1229e3b70440e3887ccf1bd7e3bad51f900f5313',
                 '877.py': 'a6aa7648e0fb765a8dc9b56b8f79b4dcef5fc772', '877.log': 'c4eb58021ed827fb13d5c15fee7c18541f6d4604',
                 '878.py': '7842e8675544a0328e3552f059c81b7750068a82', 'Test_878_log2.log': '2bfc7adc2a8f718c012a6d722a9e0a04a72cbedd'})
TEST878_PREREG879 = '0555ab01d436c0df7e8e1be21aea3170ac0a50d799a528796212298a48dc4103'
# names the selected TEST878 code reads; their values come from the locked 878.py itself (CONSTS878 below)
_a878, _h878, _j878 = _a879, _h879, _j879
ENGINE_BLOB878 = ENGINE_BLOB879
CONSTS878 = ('TEST877_CELL_BLOB878', 'TEST877_PREREG_DEPS878', 'TEST870_MINUTES', 'WORLDS878', 'SOURCES878', 'FORKS878',
             'SIDES874', '_h877', 'ARM878', 'FUNCS873', 'FUNCS874', 'FUNCS877', 'ROPE_TOL878', 'HARD_MIN878', 'PREREG878')
FUNCS878 = ('Partial878', 'Persist878', 'line878', 'source_audit878', 'load878', 'guard878', 'xspan878', 'next_kv878',
            'tsha878', 'write_exp878', 'load_exp878', 'append_exp878', 'xappend878', 'xcar878', 'arm878', 'jsafe878',
            'dif878', 'pa878', 'sig878', 'persist878', 'probe878')
BANNED879 = {'register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook', 'output_hidden_states',
             'output_attentions', 'install_all_output_capturing_hooks', 'backward', 'requires_grad_', 'step', 'zero_grad',
             'execute866', 'mount865', 'free865', 'hop865', 'DirectCut3', 'native_append_direct'}
CELLS879 = (('01', '01'), ('01', '00'), ('00', '01'), ('00', '00'))     # (source world, receiver world), all pre-registered
PREREG879 = {
    'question': "is TEST878's asymmetric outcome-dependent transfer source-bound, receiver-bound, same-goal-restricted or a "
                'source x receiver interaction under matched FORK receiver provenance',
    'sources': {'S01': ['I867_01_MISSING', 'I867_01_LIVE'], 'S00': ['I867_00_MISSING', 'I867_00_LIVE']},
    'receivers': {'R01': 'I867_01_FORK step 1', 'R00': 'I867_00_FORK step 1'}, 'arm': 'V_X', 'executed_action': 'ACQUIRE',
    'matrix': ['S01>R01 (same goal)', 'S01>R00 (cross)', 'S00>R01 (cross)', 'S00>R00 (same goal)'],
    'never_dropped': 'every cell is run and reported; a NO_TRANSFER cell is a result, not a reason to drop it',
    'cartridges': 'TEST878 Experience-CUT3 [X2][A][C] written by the locked 878.py functions, source working state freed, '
                  'reloaded with file + per-tensor SHA-256',
    'static_gates_before_model_load': 'records exist; sources ADVANCE->ACQUIRE with a real mounted outcome; M/L share the t2 '
                                      'state; outcome cards differ; receiver memory holds no outcome card of the mounted source; '
                                      'receiver state is no source t2/t3 state; goal relation = (source world == receiver world)',
    'runtime_gates': 'TEST878 side gates (capture bitwise, H reproduces TEST873, round trip, seals, hook-free); receiver t1 CAR '
                     'reproduces its record; source pair gates; persistence gate of TEST878 (file/tensor SHA, lower rows '
                     'bitwise, same action, max dp <= 0.10); BASE_EXPLICIT == BASE exactly; per cell: pre-C rows of M and L '
                     'bitwise equal, C_BLIND_M == C_BLIND_L exactly, receiver memory seals unchanged, finite margins',
    'floor': 'per source world: max(5e-5, max over M/L of |m(reconstruction) - m(source)|), as TEST878',
    'transfer': 't(s,r) = all cell gates and |T_seq| > floor_seq(s), T = m(FULL_M) - m(FULL_L) over the 15 CAR margins',
    'mechanism_per_cell': 'OUTCOME_DISCRIMINATED if t; else OUTCOME_ROWS_NOT_READ if max over M/L of |m(FULL) - m(C_BLIND)|_seq '
                          '<= floor_seq(s) (making C readable does not move the decision); else OUTCOME_READ_NOT_DISCRIMINATED',
    'reported_not_gated': ['context X = |m(C_BLIND) - m(BASE)|', 'total |m(FULL) - m(BASE)|', 'direction of T vs the source '
                           'contrast (sig878)', 'arms: action and probabilities', 'reproduction of TEST878: cartridge file '
                           'SHA-256 and the diagonal arms against Test_878_log2.log'],
    'verdict': {'TECHNICAL_BLOCK': 'any gate, replay, record, persistence or integrity failure',
                'PARTIAL_INCONCLUSIVE': 'time/VRAM guard',
                'MATCHED_FORK_OUTCOME_TRANSFER': 'all four cells transfer',
                'SAME_GOAL_RESTRICTED_PATTERN': 'both diagonal cells transfer, both cross cells do not',
                'SOURCE_MAIN_EFFECT': 'one source transfers to both receivers, the other to neither',
                'RECEIVER_MAIN_EFFECT': 'one receiver shows transfer from both sources, the other from neither',
                'SOURCE_BY_RECEIVER_ASYMMETRY': 'any other non-empty pattern',
                'NO_OUTCOME_TRANSFER': 'no cell transfers (+ GENERIC_CONTEXT_INFLUENCE if any |C_BLIND - BASE|_seq > floor)'},
    'reading': {'MATCHED_FORK_OUTCOME_TRANSFER': 'the TEST878 cross-world failure belonged to the T2 receiver, not to the '
                                                 'cartridge or the world pair: receiver state matters, experiences are portable',
                'SAME_GOAL_RESTRICTED_PATTERN': 'outcome transfer is bound to the goal/world shared by episode and receiver',
                'SOURCE_MAIN_EFFECT': 'portability is a property of the source episode',
                'RECEIVER_MAIN_EFFECT': 'the bottleneck is the receiver read interface',
                'SOURCE_BY_RECEIVER_ASYMMETRY': 'episode-receiver compatibility; with two worlds a single failing cross cell '
                                                'cannot be assigned to the source or to the receiver',
                'NO_OUTCOME_TRANSFER': 'TEST878 same-goal transfer not reproduced'},
    'identifiability_note': 'TEST878 already measured both diagonal cells; if they reproduce, only MATCHED, SAME_GOAL_RESTRICTED or '
                            'a one-cell asymmetry are reachable; SOURCE/RECEIVER main effects require a failing diagonal',
    'guards': 'before every load/append/read group: elapsed > 70 min or available VRAM < 8 GiB -> PARTIAL_INCONCLUSIVE',
    'limits': ['no goal appraisal, no action credit, no executed correction, no learning: read-only CAR, forced mount',
               'two worlds, one executed action type (ACQUIRE)']}
PREREG_SHA879 = sha256_bytes864(_j879.dumps(PREREG879, sort_keys=True).encode())
STATE879 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO879, 'prereg_sha256': PREREG_SHA879, 'source': {}, 'api': {},
            'ref873': {}, 'ref878': {}, 'targets_static': {}, 'sides': {}, 'experience': {}, 'sources': {}, 'receivers': {},
            'cells': {}, 'blocks': [], 'verdict': None, 'error': None}
STATE878 = STATE877 = STATE879                             # the selected 877/878 functions write here
T2_KEEP878, SRC878, TGT878, EXP878 = {}, {}, {}, {}

class Gate879(Exception):
    pass

def line879(*parts): short864('T879', *parts)

def scan879(node, allow=()):
    used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in _a879.walk(node) if isinstance(c, _a879.Call)}
    used |= {k.arg for k in _a879.walk(node) if isinstance(k, _a879.keyword)}
    used |= {s.slice.value for s in _a879.walk(node) if isinstance(s, _a879.Subscript) and
             isinstance(s.slice, _a879.Constant)} & {'native_append_direct', 'DirectCut3'}
    bad = (used & BANNED879) - set(allow)
    assert not bad, ('FIREWALL879', getattr(node, 'name', '?'), sorted(bad))

def capture_source879():
    try:
        hist = [t for t in get_ipython().history_manager.input_hist_raw if MARKER879 in t and 'def cell879' in t]
        source, how = hist[-1], 'IPYTHON_CELL'
    except (NameError, IndexError):
        source = open(__file__, encoding='utf-8').read() if '__file__' in globals() else None; how = 'FILE_%RUN'
    assert source and MARKER879 in source, 'EXECUTED_879_SOURCE_NOT_CAPTURED'
    tree = _a879.parse(source)
    for node in tree.body:
        if isinstance(node, _a879.FunctionDef) and node.name.endswith('879'):
            scan879(node)
    calls = [n for n in _a879.walk(tree) if isinstance(n, _a879.Call) and getattr(n.func, 'id', None) == 'reproduce_pre859859']
    assert len(calls) == 1, 'MODEL_LOADER_CALL_COUNT_NOT_ONE'
    rs = [n for n in _a879.walk(tree) if isinstance(n, _a879.Assign) and any(getattr(t, 'id', '') == 'xray_point870' for t in n.targets)]
    assert len(rs) == 1 and getattr(rs[0].value, 'id', None) == 'probe878', 'FIREWALL879_REBIND'
    (ROOT864 / 'TEST879.py').write_text(source, encoding='utf-8')
    STATE879['source'] = {'how': how, 'executed_cell_git_blob': git_blob864(source.encode()),
                          'executed_cell_sha256': sha256_bytes864(source.encode()), 'lines': source.count('\n') + 1,
                          'firewall': 'PASS'}

def select878_879():
    # TEST878 constants and functions, unchanged, from the blob-locked 878.py; that file must be the GPU-run file:
    # its pre-registration reproduces the TEST878 hash and the second A100 log ran exactly this blob.
    tree = _a879.parse(RAW_SOURCES864['878.py'].decode(), filename='878.py')
    consts = [n for n in tree.body if isinstance(n, _a879.Assign) and
              {x.id for t in n.targets for x in _a879.walk(t) if isinstance(x, _a879.Name)} & set(CONSTS878)]
    funcs = [n for n in tree.body if isinstance(n, (_a879.FunctionDef, _a879.ClassDef)) and n.name in FUNCS878]
    assert {n.name for n in funcs} == set(FUNCS878), ('SELECT_878', sorted(set(FUNCS878) - {n.name for n in funcs}))
    for n in funcs:
        if isinstance(n, _a879.FunctionDef): scan879(n, ('native_append_direct',) if n.name == 'append_exp878' else ())
    exec(compile(_a879.fix_missing_locations(_a879.Module(consts, [])), '878.py:constants', 'exec'), globals())
    assert sha256_bytes864(_j879.dumps(PREREG878, sort_keys=True).encode()) == TEST878_PREREG879, 'TEST878_PREREG_MISMATCH'
    exec(compile(_a879.fix_missing_locations(_a879.Module(funcs, [])), '878.py:selected', 'exec'), globals())
    log = RAW_SOURCES864['Test_878_log2.log'].decode()
    for needle in ('NVIDIA A100-SXM4-80GB', 'cell %s | prereg %s' % (LOCKS864['878.py'], TEST878_PREREG879[:16]),
                   'TEST878 VERDICT ACTION_INFORMATION_DEPENDENT_TRANSFER', 'TEST878 | status COMPLETE'):
        assert needle in log, ('TEST878_LOG_NOT_THE_EXPECTED_GPU_RUN', needle)
    STATE879['source']['test878'] = {'file_git_blob': LOCKS864['878.py'], 'prereg_reproduced': TEST878_PREREG879[:16],
                                     'constants': len(consts), 'functions': len(funcs), 'gpu_log': 'Test_878_log2.log'}
    return log

def ref878_879(log):
    # TEST878 run-2 values for the reproduction report (not gated): cartridge file SHA-256 and the same-goal arms
    sha = dict(_r879.findall(r'VERIFIED_CARTRIDGE (X878_\d\d_[A-Z]+) \{"bytes": \d+, "sha256_now": "([0-9a-f]{64})"', log))
    arms, w, panel = {}, None, None
    for raw in log.splitlines():
        l = raw[len('  TEST878 | '):] if raw.startswith('  TEST878 | ') else raw
        m = _r879.match(r'WORLD (\d\d) status', l)
        if m: w, panel = m.group(1), None; continue
        m = _r879.match(r'  PANEL (\w+)', l)
        if m: panel = m.group(1); continue
        m = _r879.match(r'    (BASE|FULL_[ML]|C_BLIND_[ML])\s+(\w+)\s+(.*)$', l)
        if m and w and panel == 'SAME_GOAL':
            arms.setdefault(w, {})[m.group(1)] = {'action': m.group(2), 'p': {k: float(v) for k, v in
                                                  _r879.findall(r'([A-Z]+)=([0-9.]+)', m.group(3).split(' | ')[0])}}
    assert len(sha) == 4 and all(len(arms.get(x, {})) == 5 for x in WORLDS878), ('REF878', sorted(sha), {k: len(v) for k, v in arms.items()})
    return {'cartridge_sha256': sha, 'same_goal_arms': arms}

def targets879(refs):
    # static matrix gates from the locked 869 records only (no CAR result is read)
    for item in SOURCES878 + FORKS878:
        if (item, ARM878) not in refs: raise Gate879('RECORD_MISSING ' + item)
    ctl = lambda item: [e for e in refs[(item, ARM878)]['events'] if e['type'] == 'CONTROL']
    src, rec, cells = {}, {}, {}
    for w in WORLDS878:
        cards, shas, t2 = [], [], {}
        for cnd in ('MISSING', 'LIVE'):
            item = 'I867_%s_%s' % (w, cnd); cs = ctl(item)
            if [x['record']['action'] for x in cs[:2]] != ['ADVANCE', ACTION878]: raise Gate879('T2_PATH ' + item)
            eff = [e for e in refs[(item, ARM878)]['events'] if e['type'] == 'EFFECT' and e.get('effect') == 'MOUNTED']
            if not (eff and eff[0].get('action') == ACTION878): raise Gate879('OUTCOME_EFFECT ' + item)
            cards.append(eff[0]['chosen']); shas += [cs[1]['record']['state_sha256'], cs[2]['record']['state_sha256']]; t2[cnd] = cs[1]
        if t2['MISSING']['record']['state_sha256'] != t2['LIVE']['record']['state_sha256']: raise Gate879('T2_STATE_NOT_SHARED ' + w)
        if cards[0] == cards[1]: raise Gate879('OUTCOME_CARDS_EQUAL ' + w)
        src[w] = {'cards': cards, 'shas': shas, 'world_index': refs[('I867_%s_MISSING' % w, ARM878)]['world_index']}
    all_shas = {s for w in WORLDS878 for s in src[w]['shas']}
    for r in WORLDS878:
        item = 'I867_%s_FORK' % r; cs = ctl(item)
        if len(cs) < FORK_STEP878: raise Gate879('FORK_STEP_MISSING ' + item)
        f = cs[FORK_STEP878 - 1]
        rec[r] = {'item': item, 'step': FORK_STEP878, 'mounted': list(f['mounted']), 'state_sha256': f['record']['state_sha256'],
                  'world_index': refs[(item, ARM878)]['world_index'], 'recorded_action': f['record']['action']}
    for s, r in CELLS879:
        why = []
        if set(rec[r]['mounted']) & set(src[s]['cards']): why.append('SOURCE_OUTCOME_CARD_MOUNTED')
        if rec[r]['state_sha256'] in all_shas: why.append('RECEIVER_IS_A_SOURCE_STATE')
        if (rec[r]['world_index'] == src[s]['world_index']) != (s == r): why.append('GOAL_RELATION')
        cells['%s>%s' % (s, r)] = {'relation': 'SAME_GOAL' if s == r else 'CROSS', 'independent': not why, 'why': why}
    bad = {k: v['why'] for k, v in cells.items() if not v['independent']}
    if bad: raise Gate879('RECEIVER_NOT_INDEPENDENT %s' % _j879.dumps(bad))
    return {'sources': src, 'receivers': rec, 'cells': cells}

# ============================ phase 2: sources (floors) and the four-cell matrix ============================
def sources879(env):
    out, idx = {}, pa878(ACTION878)
    for w in WORLDS878:
        M, L = SRC878.get('I867_%s_MISSING' % w), SRC878.get('I867_%s_LIVE' % w)
        R = STATE879['sources'].setdefault(w, {})
        if M is None or L is None: raise Gate879('SOURCE_EXPERIENCE_NOT_CAPTURED ' + w)
        R['gates'] = g = {'same_t2_spans': (M['n2'], M['L2'], M['la']) == (L['n2'], L['L2'], L['la']),
                          'same_action_tokens': M['A_ids'] == L['A_ids'] and M['t2_action'] == L['t2_action'] == ACTION878,
                          'real_cards_differ': M['card'] != L['card'], 'same_C_length': M['body'] == L['body'],
                          'pre_C_cartridge_rows_bitwise': M['entry']['pre_C_seal'] == L['entry']['pre_C_seal'],
                          'same_goal': M['qid'] == L['qid']}
        if not all(g.values()): raise Gate879('SOURCE_PAIR_GATES %s %s' % (w, _j879.dumps(g)))
        c = dif878(M['m'], L['m'])
        R['contrast'] = c; R['norm_all15'] = {k: nrm877(c[k]) for k in c}
        R['norm_action5'] = {k: nrm877([c[k][i] for i in idx]) for k in c}
        R['persistence'] = {S['cond']: persist878(env, S) for S in (M, L)}
        if not all(r['pass'] for r in R['persistence'].values()): raise Gate879('PERSISTENCE_FAIL ' + w)
        R['floor'] = floor = {k: max(SIG_MIN878, max(r['noise'][k] for r in R['persistence'].values())) for k in ('first', 'seq')}
        out[w] = (M, L, c, floor)
        line879('SOURCE', w, 'floor seq=%.5f' % floor['seq'], '|c| seq=%.4f' % R['norm_all15']['seq'],
                'persist', _j879.dumps({k: [r['pass'], round(r['max_dp'], 5)] for k, r in R['persistence'].items()}))
    return out, idx

def cell879(env, M, L, T, base, c, idx, floor, seal0):
    n0 = length873(env, T['m']); L2, la, q = M['L2'], M['la'], int(M['entry']['body_tokens'])
    a1, c1 = n0 + L2 + la, n0 + q
    rd, pre = {}, {}
    for S in (M, L):
        cnd = S['cond'][0]; guard878('cell_%s_%s' % (T['item'], S['side']))
        cp = load_exp878(env, S['entry']); g = append_exp878(env, T['m'], cp); del cp
        pre[cnd] = [[env['kv_digest'](k[:, :, n0:a1]), env['kv_digest'](v[:, :, n0:a1])] for k, v in g]
        rd['FULL_' + cnd] = decide874(env, g, T['X'], [])[0]
        rd['C_BLIND_' + cnd] = decide874(env, g, T['X'], [(a1, c1)])[0]; del g
    m = {k: marg877(r) for k, r in rd.items()}; mb = marg877(base)
    gates = {'pre_C_rows_bitwise_M_eq_L': pre['M'] == pre['L'], 'C_BLIND_M_equals_L': same873(rd['C_BLIND_M'], rd['C_BLIND_L']),
             'receiver_memory_unchanged': prefix_seals865(env, T['m']) == seal0,
             'finite_margins': all(math.isfinite(x) for v_ in list(m.values()) + [mb] for k in ('first', 'seq') for x in v_[k])}
    Tc = dif878(m['FULL_M'], m['FULL_L']); nT = {k: nrm877(Tc[k]) for k in Tc}
    norm = lambda a, b: {k: nrm877(sub877(a[k], b[k])) for k in ('first', 'seq')}
    inc = {x: norm(m['FULL_' + x], m['C_BLIND_' + x]) for x in 'ML'}
    transfer = all(gates.values()) and nT['seq'] > floor['seq']
    if not all(gates.values()): mech = 'TECHNICAL'
    elif transfer: mech = 'OUTCOME_DISCRIMINATED'
    elif max(inc[x]['seq'] for x in 'ML') <= floor['seq']: mech = 'OUTCOME_ROWS_NOT_READ'
    else: mech = 'OUTCOME_READ_NOT_DISCRIMINATED'
    arms = {k: arm878(r) for k, r in rd.items()}
    return {'target': {k: T[k] for k in ('item', 'step', 'qid', 'mounted', 'X_len')}, 'spans': {'E': [n0, c1], 'C': [a1, c1]},
            'reads': len(rd), 'gates': gates, 'arms': arms, 'contrast_T': Tc, 'norm_T': nT, 'floor': floor,
            'ratio_T_to_floor_seq': nT['seq'] / floor['seq'], 'transfer': transfer, 'mechanism': mech,
            'context_C_BLIND_minus_BASE': norm(m['C_BLIND_M'], mb), 'outcome_increment_FULL_minus_C_BLIND': inc,
            'total_FULL_minus_BASE': {x: norm(m['FULL_' + x], mb) for x in 'ML'}, 'signature_vs_source': sig878(Tc, c, idx),
            'max_dp_FULL_M_vs_L': max(abs(arms['FULL_M']['p'][w] - arms['FULL_L']['p'][w]) for w in arms['FULL_M']['p'])}

def matrix879(env, src, idx):
    for r in WORLDS878:
        T = TGT878.get(('FORK', r))
        if T is None: raise Gate879('RECEIVER_NOT_CAPTURED_OR_RECORD_NOT_REPRODUCED R' + r)
        guard878('receiver_' + r); seal0 = prefix_seals865(env, T['m'])
        base = decide874(env, T['m'], T['X'], [])[0]; bx = xcar878(env, T['m'], T['X'], (), False)
        R = STATE879['receivers'][r] = {'item': T['item'], 'qid': T['qid'], 'mounted': T['mounted'], 'X_len': T['X_len'],
                                        'memory_tokens': length873(env, T['m']), 'BASE': arm878(base),
                                        'BASE_EXPLICIT_equals_BASE': same873(base, bx)}
        del bx
        if not R['BASE_EXPLICIT_equals_BASE']: raise Gate879('BASE_EXPLICIT_NOT_EQUAL_BASE R' + r)
        for s in WORLDS878:
            M, L, c, floor = src[s]; key = '%s>%s' % (s, r)
            if (T['qid'] == M['qid']) != (s == r) or set(T['mounted']) & {M['card'], L['card']}:
                raise Gate879('RUNTIME_INDEPENDENCE ' + key)
            cell = STATE879['cells'][key] = cell879(env, M, L, T, base, c, idx, floor, seal0)
            cell['relation'] = 'SAME_GOAL' if s == r else 'CROSS'
            line879('CELL', key, cell['relation'], 'transfer=%s' % cell['transfer'], cell['mechanism'],
                    '|T| seq=%.4f floor=%.4f' % (cell['norm_T']['seq'], floor['seq']), 'gates=%s' % all(cell['gates'].values()))

def reproduction879():
    # reported only: deterministic stack -> the cartridges and the diagonal cells should equal TEST878 run 2
    ref = STATE879['ref878']; out = {'cartridge_file_sha256_equal': {}, 'diagonal_arms_max_abs_dp': {}}
    for eid, e in STATE879['experience'].items(): out['cartridge_file_sha256_equal'][eid] = ref['cartridge_sha256'].get(eid) == e['sha256']
    for w in WORLDS878:
        cell, old = STATE879['cells'].get('%s>%s' % (w, w)), ref['same_goal_arms'][w]
        if not cell: continue
        now = dict(cell['arms'], BASE=STATE879['receivers'][w]['BASE'])
        out['diagonal_arms_max_abs_dp'][w] = max(abs(now[a]['p'][k] - old[a]['p'][k]) for a in old for k in old[a]['p'])
    out['reproduces_TEST878'] = all(out['cartridge_file_sha256_equal'].values()) and \
        len(out['diagonal_arms_max_abs_dp']) == 2 and all(v <= 6e-5 for v in out['diagonal_arms_max_abs_dp'].values())
    return out

def verdict879():
    blocks = list(STATE879['blocks']); reps = {r.get('item'): r for r in STATE870['replays']}
    for side, s in STATE879['sides'].items():
        if s.get('error'): blocks.append('POINT_ERROR:' + side)
        if reps.get(side, {}).get('ok') is not True: blocks.append('REPLAY_NOT_EXACT:' + side)
    C = STATE879['cells']; t = {k: C[k]['transfer'] for k in C}
    if blocks or len(C) != 4 or not all(all(C[k]['gates'].values()) for k in C):
        v = 'TECHNICAL_BLOCK'
    else:
        n, diag, cross = sum(t.values()), [t['01>01'], t['00>00']], [t['01>00'], t['00>01']]
        rows = {s: [t['%s>%s' % (s, r)] for r in WORLDS878] for s in WORLDS878}
        cols = {r: [t['%s>%s' % (s, r)] for s in WORLDS878] for r in WORLDS878}
        full_or_none = lambda d: sorted(sum(x) for x in d.values()) == [0, 2]
        if n == 4: v = 'MATCHED_FORK_OUTCOME_TRANSFER'
        elif n == 0:
            v = 'NO_OUTCOME_TRANSFER'
            if any(C[k]['context_C_BLIND_minus_BASE']['seq'] > C[k]['floor']['seq'] for k in C): v += '+GENERIC_CONTEXT_INFLUENCE'
        elif all(diag) and not any(cross): v = 'SAME_GOAL_RESTRICTED_PATTERN'
        elif full_or_none(rows): v = 'SOURCE_MAIN_EFFECT'
        elif full_or_none(cols): v = 'RECEIVER_MAIN_EFFECT'
        else: v = 'SOURCE_BY_RECEIVER_ASYMMETRY'
    STATE879['verdict'] = {'verdict': v, 'blocks': blocks, 'matrix_transfer': t,
                           'mechanism': {k: C[k]['mechanism'] for k in C},
                           'reading': PREREG879['reading'].get(v.split('+')[0]),
                           'limits': PREREG879['limits']}
    return STATE879['verdict']

def report879():
    words = ('ADVANCE', 'ACQUIRE', 'REJECT', 'BACKTRACK', 'ACCEPT', 'STOP'); f3 = lambda xs: ' '.join('%.3f' % x for x in xs)
    print('=' * 110)
    print('TEST879 FORK<->FORK SOURCE-RECEIVER CROSSOVER | GPU %s | cell %s | prereg %s | api %s' % (CC_GPU.get('name'),
          STATE879['source'].get('executed_cell_git_blob'), PREREG_SHA879[:16], _j879.dumps(STATE879['api'].get('transformers'))))
    for w, R in STATE879['sources'].items():
        print('SOURCE S%s gates %s' % (w, _j879.dumps(R.get('gates'), sort_keys=True)))
        if 'floor' in R:
            print('  |c| all15 seq=%.4f action5 seq=%.4f | floor first=%.5f seq=%.5f' % (R['norm_all15']['seq'],
                  R['norm_action5']['seq'], R['floor']['first'], R['floor']['seq']))
        for cnd, p in (R.get('persistence') or {}).items():
            print('  PERSIST %-7s pass=%s lower_bitwise=%s action_same=%s max_dp=%.5f noise seq=%.4f explicit_append_bitwise=%s' % (
                  cnd, p['pass'], p['lower_rows_bitwise'], p['action_same'], p['max_dp'], p['noise']['seq'],
                  p['explicit_append_equals_native_bitwise']))
    for r, R in STATE879['receivers'].items():
        print('RECEIVER R%s %s memory=%s X=%s mounted=%s BASE_EXPLICIT==BASE %s | BASE %-9s %s' % (r, R['item'], R['memory_tokens'],
              R['X_len'], R['mounted'], R['BASE_EXPLICIT_equals_BASE'], R['BASE']['action'],
              ' '.join('%s=%.4f' % (x, R['BASE']['p'][x]) for x in words)))
    for key in ('01>01', '01>00', '00>01', '00>00'):
        x = STATE879['cells'].get(key)
        if not x: print('CELL S%s>R%s NOT_RUN' % tuple(key.split('>'))); continue
        print('CELL S%s>R%s %-9s transfer=%s mechanism=%s | |T| first=%.4f seq=%.4f | floor seq=%.4f | ratio %.2f | gates %s' % (
              key[:2], key[3:], x['relation'], x['transfer'], x['mechanism'], x['norm_T']['first'], x['norm_T']['seq'],
              x['floor']['seq'], x['ratio_T_to_floor_seq'], _j879.dumps(x['gates'], sort_keys=True)))
        for arm, a in x['arms'].items():
            print('    %-9s %-9s %s' % (arm, a['action'], ' '.join('%s=%.4f' % (w_, a['p'][w_]) for w_ in words)))
        print('    T M-L seq(15) %s' % f3(x['contrast_T']['seq']))
        print('    context |C_BLIND-BASE| seq=%.4f | outcome increment |FULL-C_BLIND| seq M=%.4f L=%.4f | total |FULL-BASE| seq '
              'M=%.4f L=%.4f | max dp FULL M vs L %.4f' % (x['context_C_BLIND_minus_BASE']['seq'],
              x['outcome_increment_FULL_minus_C_BLIND']['M']['seq'], x['outcome_increment_FULL_minus_C_BLIND']['L']['seq'],
              x['total_FULL_minus_BASE']['M']['seq'], x['total_FULL_minus_BASE']['L']['seq'], x['max_dp_FULL_M_vs_L']))
        s = x['signature_vs_source']['seq']
        print('    direction vs source c: cos_all15=%.3f cos_A=%.3f rho_A=%.3f selectivity=%.3f' % (s['cos_all15'], s['cos_A'],
              s['rho_A'], s['action_selectivity']))
    v = STATE879['verdict'] or {}
    t = v.get('matrix_transfer') or {}
    if t:
        print('MATRIX (transfer)      R01       R00')
        for s_ in WORLDS878: print('  S%s              %-9s %-9s' % (s_, t.get(s_ + '>01'), t.get(s_ + '>00')))
    print('REPRODUCTION OF TEST878 (reported) %s' % _j879.dumps(STATE879.get('reproduction'), sort_keys=True))
    print('TEST879 VERDICT %s | mechanism %s | blocks %s' % (v.get('verdict'), _j879.dumps(v.get('mechanism'), sort_keys=True),
          v.get('blocks')))
    print('READING (pre-registered): %s' % v.get('reading'))
    print('LIMITS: %s' % '; '.join(PREREG879['limits']))
    print('status %s | wall %.0f s | peak GPU %.2f GiB | GPU_EXECUTION_NOT_VERIFIED_BY_AUTHOR' % (STATE879['status'],
          time.perf_counter() - T_START878, torch.cuda.max_memory_allocated() / 2**30 if torch.cuda.is_available() else 0.0))
    print('=' * 110)

class Partial878(Exception):                                   # placeholder; replaced by the locked TEST878 class at selection
    pass

T_START878 = time.perf_counter()
try:
    STATE879['status'] = 'G0_SOURCE'; capture_source879()
    json_write864('879_prereg.json', {'prereg': PREREG879, 'sha256': PREREG_SHA879, 'before_model_load': True})
    line879('G0 PREREG', PREREG_SHA879)
    load_sources865(); log878 = select878_879(); xray_point870 = probe878
    source_audit878(); load878(); STATE879['ref873'] = ref873_874(RAW_SOURCES864['873.log'].decode())
    STATE879['ref878'] = ref878_879(log878)
    feasibility_audit864(); audit_contracts865(); load_spine864(); REFS879 = load_records870()
    STATE879['targets_static'] = targets879(REFS879)
    STATIC_T2_SHA878 = {s: [e['record'] for e in REFS879[(s, ARM878)]['events'] if e['type'] == 'CONTROL'][PRE_STEP878 - 1]['state_sha256']
                        for s in SOURCES878}
    line879('G0 SOURCE PASS', _j879.dumps(STATE879['source'], sort_keys=True))
    line879('G0 MATRIX', _j879.dumps(STATE879['targets_static']['cells'], sort_keys=True))
    STATE879['status'] = 'G1_PREFLIGHT'; assert CC_GPU_OK, ('GPU_PRECHECK', CC_GPU)
    env879, original_error879, original_trace879, reproduction879_ = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace879; TWO_JOB_VERIFICATION864 = verify_two_job859(env879, original_trace879)
    assert_hook_free859(env879, 'T879_before_native'); install_offline_evaluator859(env879)
    native879 = native_sequences860(env879); NATIVE_REGRESSION864 = native_regression864(env879, native879)
    verify_864_reference865(NATIVE_REGRESSION864); ANALYSIS864 = run_analysis863(env879, native879)
    assert len(STATE863['restores']) == 3 and all(r['exact'] for r in STATE863['restores'])
    digest879 = records_digest861(env879); null_seal879 = physical_seal863(env879, env879['MEMNULL841'])
    runtime_contracts865(env879); runtime_preflight865(env879, reproduction879_); rearm_budget865(env879); make_slots866(env879)
    SLOTS867['PREV_EVALUATION'] = list(env879['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env879); resolve_append873(env879); api877(env879); WEIGHTS0_878 = weights_digest877(env879)
    chunk879 = [ns['CHUNK'] for ns in (env879['build_fusion'].__globals__, env879) if 'CHUNK' in ns]
    assert chunk879 and int(chunk879[0]) > 0 and all(k in env879 for k in ('P', 'to_gpu', 'kv_digest', 'entries')), 'EXPERIENCE_NAMESPACE'
    EXP878['CHUNK'] = int(chunk879[0])
    EXP_DIR878 = ROOT864.parent / ('TEST879_EXPERIENCE_CUT3_' + STAMP864); EXP_DIR878.mkdir(parents=True, exist_ok=False)
    assert_hook_free859(env879, 'T879_before_points')
    line879('G1 PREFLIGHT PASS', _j879.dumps(STATE879['api'], sort_keys=True), 'CHUNK=%d P=%d' % (EXP878['CHUNK'], int(env879['P'])),
            'model_load_s=%.0f' % (time.perf_counter() - T_START878))
    STATE879['status'] = 'REPLAY'; T0_865 = time.perf_counter(); by_key879 = build_specs869(env879)
    plan879 = [(s, {PRE_STEP878: 'T2_EXPERIENCE', POST_STEP878: 'T3_EXPERIENCE'}) for s in SOURCES878] + \
              [(s, {FORK_STEP878: 'T1_TARGET'}) for s in FORKS878]
    for side, tg in plan879:
        guard878('replay_' + side)
        rep = run_replay870(env879, {'id': side, 'item': side, 'arm': ARM878, 'targets': tg}, by_key879, REFS879)
        T2_KEEP878.pop(side, None)
        if not rep['ok']: STATE879['blocks'].append('REPLAY_NOT_EXACT:' + side)
    json_write864('879_experience_manifest.json', jsafe878(STATE879['experience']))
    STATE879['status'] = 'MATRIX'
    src879, idx879 = sources879(env879)
    matrix879(env879, src879, idx879)
    hook = hook_audit859(env879, 'T879_final')
    if records_digest861(env879) != digest879 or physical_seal863(env879, env879['MEMNULL841']) != null_seal879 or \
            hook['hook_count'] or hook['transformers_output_capturing_installed'] or weights_digest877(env879) != WEIGHTS0_878:
        STATE879['blocks'].append('POST_RUN_INTEGRITY')
    STATE879['reproduction'] = reproduction879()
    STATE879['status'] = 'COMPLETE'; verdict879()
except Partial878 as exc:
    STATE879['error'] = str(exc); STATE879['status'] = 'PARTIAL_AT_' + str(STATE879['status'])
    STATE879['verdict'] = {'verdict': 'PARTIAL_INCONCLUSIVE', 'blocks': [], 'why': str(exc)}
except BaseException as exc:
    STATE879['error'] = '%s: %s' % (type(exc).__name__, exc); STATE879['traceback'] = traceback.format_exc()
    STATE879['status'] = 'FAILED_AT_' + str(STATE879['status'])
    STATE879['verdict'] = {'verdict': 'TECHNICAL_BLOCK', 'blocks': ['EXCEPTION: ' + STATE879['error'][:300]]}
    (ROOT864 / '879_traceback.txt').write_text(STATE879['traceback'], encoding='utf-8')
    print('TEST879 ERROR', STATE879['error'][:300], '| full traceback:', ROOT864 / '879_traceback.txt', file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        json_write864('879_result.json', jsafe878(dict(STATE879, replays=STATE870['replays'])) if 'jsafe878' in globals()
                      else json.loads(json.dumps(dict(STATE879, replays=STATE870['replays']), default=str)))
    except Exception as exc: print('RESULT_WRITE_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    try: report879()
    except Exception as exc: print('REPORT_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE879['suffix'], 'test870.py:suffix', 'exec'), globals())
