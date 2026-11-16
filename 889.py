# TEST889 BODY-SHA256 e9dd0542f2253c843d1be37f5e2df515b5f87b5d7ca1164dcbb3a9aff18471fc
# AKBASCORE SILICON HIPPOCAMPUS — TEST889 — EVENT_CLOSED_NATIVE_TRANSITION_APPRAISAL (one Colab cell, one Run, A100-SXM4-80GB)
# Contract: K3.1 "TEST889 Oncesi Nihai Mimari Denetim — DESIGN_LOCKED". One change against TEST888:
#   E_s = [X2_s (contains V_before = V_s)][A_s (the executed native action)][EVALUATION slot + V_after = V_(s+1)]
#   V_(s+1) = the evaluation['rows'] that the locked control_step867 already produces at step s+1, after A_s was executed.
#   Event-closed schedule: E_s is written only when V_(s+1) exists; decision t reads exactly E_(t-2) (t3 E1 .. t6 E4); t1, t2: the
#   native NONE reading; a missing expected event never falls back to an older cartridge (fail-closed).
# The model alone decides: the executed action is the native CAR argmax of the arm's reading, literally through execute866.
# REUSE: 888.py (commit 20bef427, blob c00d8c80) is downloaded, hash-checked and its definitions executed unchanged; it loads
# 887 -> 885 -> test870 -> 873/877/878/881 exactly as in the TEST888 Colab run. New code: the V_after writer / pair / contract /
# reader, the episode loop, the appraisal ledger, the verdict. No training, LoRA, backward, RAG, text replay, hooks, router,
# oracle, answer fixing, UNKNOWN rule, action override, reward. GPU_NOT_RUN_BY_AUTHOR.
import time as _t889
T_CELL889 = _t889.perf_counter()                       # the single 75-minute clock starts here (before any download)
import ast as _a889, copy as _c889, hashlib as _h889, json as _j889, os as _o889, re as _r889, urllib.request as _u889, shutil as _s889
B888_URL889 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
               '20bef427eee3af4c63d2d070a0226bb4c3bcd229/888.py')
B888_BLOB889 = 'c00d8c807231d96d86ed46af7676be04538bdfbd'
B888_SHA889 = '8a30934f4e0dd84b6bc7374549365b1fc1edaac8e1633f94f2f12287a64d1713'
B888_BODY_LOCK889 = '3fb77095546f40bd41ed6b7ead8f9a4b9fb5f0c3dfefb25241ec43d29bdb5ca5'   # canonical body (not the file SHA)
B888_CUT889 = '\n# ============================ single cell execution ============================\n'
B888_RENAMES889 = (('TEST888_HUCRE_CIKTISI', 'TEST889_HUCRE_CIKTISI', 1), ('MyDrive/TEST888_', 'MyDrive/TEST889_', 1),
                   ('TEST888_RUN_', 'TEST889_RUN_', 1), ('888_engine.log', '889_engine.log', 1), ('888_events.jsonl', '889_events.jsonl', 1),
                   ('TEST888_SONUC_', 'TEST889_SONUC_', 1), ('TEST888 ENGINE', 'TEST889 ENGINE', 1), ('TEST888 BASE885', 'TEST889 BASE885', 1),
                   ('TEST888 BASE887', 'TEST889 BASE887', 1), ('/content/TEST888_EPISODE_CARTRIDGES', '/content/TEST889_EPISODE_CARTRIDGES', 1),
                   ('/content/TEST888_PRE_BASE_ERROR_%s.txt', '/content/TEST889_PRE_BASE_ERROR_%s.txt', 2))


def defs888_889(raw):
    # 888.py bytes -> its definition part (everything before its main block); output names renamed (I/O strings only)
    blob = _h889.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()
    assert blob == B888_BLOB889 and _h889.sha256(raw).hexdigest() == B888_SHA889, ('BASE_888_LOCK', blob)
    text = raw.decode('utf-8'); lines = text.split('\n', 1)[1].split('\n')
    body = '\n'.join(l.rstrip() for l in lines if l.strip()) + '\n'
    assert _h889.sha256(body.encode()).hexdigest() == B888_BODY_LOCK889, 'BASE_888_BODY_LOCK'
    assert text.count(B888_CUT889) == 1, 'BASE_888_CUT'
    defs = text[:text.index(B888_CUT889) + 1]
    for old, new, n in B888_RENAMES889:
        assert defs.count(old) == n, ('BASE_888_RENAME', old, defs.count(old))
        defs = defs.replace(old, new)
    _a889.parse(defs)
    return defs, {'url': B888_URL889, 'git_blob': blob, 'sha256': B888_SHA889, 'body_lock': B888_BODY_LOCK889,
                  'definition_lines': defs.count('\n')}


try:
    with _u889.urlopen(_u889.Request(B888_URL889, headers={'User-Agent': 'AKBASCORE-TEST889'}), timeout=240) as _r:
        B888_DEFS889, B888_INFO889 = defs888_889(_r.read())
except BaseException as _exc889:
    import traceback as _tb889
    _p889 = '/content/TEST889_PRE_BASE_ERROR_%s.txt' % _t889.strftime('%Y%m%dT%H%M%SZ', _t889.gmtime())
    try:
        with open(_p889, 'w', encoding='utf-8') as _f889: _f889.write(_tb889.format_exc())
    except OSError: _p889 = 'NOT_WRITTEN'
    print('TEST889 PRE-BASE ERROR (nothing loaded):', type(_exc889).__name__, _exc889, '| traceback:', _p889)
    raise
exec(compile(B888_DEFS889, '888.py:definitions', 'exec'), globals())   # 887 + 885 + engine + console capture + 888 definitions
print('TEST889 BASE888', _j889.dumps(B888_INFO889, sort_keys=True))

# ============================ sealed design (fixed before the model is loaded) ============================
ARMS889 = ('NONE', 'D_TRUE', 'D_WRONG')
LAG889 = 2                          # decision t reads E_(t-2): step_written = t-2, post_appraisal_step = t-1 (event-closed)
RECOVERY_ACTIONS889 = {'ACQUIRE': 'MOUNTED', 'REJECT': 'UNMOUNTED', 'BACKTRACK': 'POINTER_RETRACTED'}
EXEC_ALLOW889 = {'episode889': ('execute866', 'hop865', 'mount865')}
RUNTIME_NEW889 = ('write_appraisal889', 'write_pair889', 'read_contract889', 'read889', 'overlap889', 'donor_v889', 'episode889')
RUNTIME_OLD889 = ('tv_m867', 'finite_m867', 'none_m867', 'negatives_m867', 'summary_m888', 'rowset_m888')
PREREG889 = {
    'test': 'TEST889 EVENT_CLOSED_NATIVE_TRANSITION_APPRAISAL', 'contract': 'K3.1 DESIGN_LOCKED (16 Nov 2026)',
    'base888': B888_INFO889, 'base887': B887_INFO_M888, 'base885': BASE_INFO_M867, 'engine': ENGINE_INFO883, 'head_locks': HEAD883,
    'body': 'E_s = [X2_s incl. V_before=V_s][A_s][SLOTS866 EVALUATION + V_after=V_(s+1)]; V_(s+1) = evaluation rows of the locked '
            'control_step867 at step s+1; re-encoded natively in [B_s][X2_s][A_s] and written by write_exp878 (CUT3 lower K/V + H3)',
    'schedule': {'t1': None, 't2': None, 't3': 'E1', 't4': 'E2', 't5': 'E3', 't6': 'E4', 'rule': 'step_written = t-2, '
                 'post_appraisal_step = t-1; E_(t-1) (V_after = current V_t) is never read; missing expected event -> fail-closed'},
    'arms': ARMS889, 'cells': ['%s_%s' % c for c in CELLS_M867], 'horizon': HORIZON883, 'recovery_extension': 0,
    'donor': 'D_WRONG / WRONG V_after = the NONE episode of world DONOR_M867[w], same condition, EXACT same post_appraisal_step; '
             'missing -> NO_EXACT_POST_STEP_DONOR (that episode ends TECHNICAL_BLOCK, the run completes the remaining episodes for '
             'the record, TECHNICAL_STATUS = TECHNICAL_BLOCK, no PASS); row count fitted only by shape_match867, counts logged',
    'same_state_reads': 'every eligible decision, same B_t, X_t: NONE (explicit [B], == native bitwise), TRUE_FULL and WRONG_FULL '
                        '(xcar878 blind=(), the executed reading of D_TRUE / D_WRONG), TRUE_SHAM (V_after span masked in the kernel '
                        'and restored: same kernel as BLIND), TRUE_BLIND and WRONG_BLIND (V_after span masked); TRUE_BLIND != '
                        'WRONG_BLIND bitwise -> TECHNICAL_BLOCK',
    'first_token_audit': 'raw per-action first-token logits are NOT recorded: the locked xcar878 returns only log_softmax values; '
                         'the per-action first-token log-probabilities are recorded (they differ from the raw logits by one common '
                         'constant, so all between-action logit differences are recoverable); xcar878 is not modified',
    'overlap': 'V_after (source rows / text) vs the current decision appraisal V_t: CURRENT_V_ROW_ECHO (a row of V_after is a row of '
               'V_t) > CURRENT_V_TEXT_REPEAT (same normalized text) > NOVEL; PRIOR_APPRAISAL_REPEAT flagged separately (V_after rows '
               'or text equal the event V_before or an older own appraisal); points are never deleted',
    'dedupe': 'unique point = sha256(world, condition, step, X_sha256, mounted, B tokens, path texts, V_after sha)',
    'tau_tv': TAU_M867, 'min_unique_points': MIN_PAIRS_M867,
    'verdict': {
        'PHYSICAL_READ': 'the 887 rule (verdict_m867)',
        'APPRAISAL_PROVENANCE': 'PASS: >= 1 closure and every closure verified at run time (V_after sha == ledger V of the post step '
                                'of its source episode; X2 V_before sha == ledger V of the action step; A == executed reading == '
                                'EFFECT action; commit after the V_after generation); a failed closure is a TECHNICAL_BLOCK',
        'APPRAISAL_NONREDUNDANCY': 'NOT_MEASURED 0 points; FAIL all CURRENT_V_ROW_ECHO; PASS >= 1 NOVEL; else INCONCLUSIVE',
        'APPRAISAL_CHANNEL': 'TRUE_SHAM vs TRUE_BLIND (same kernel, only V_after visibility differs): PASS if any unique point has '
                             'TV > 0 or a different argmax; FAIL if >= 4 unique points and none; else INCONCLUSIVE',
        'CONTENT_EFFECT': 'TRUE_FULL vs WRONG_FULL on unique points: PASS TV >= tau in both worlds and >= 1 argmax difference; FAIL TV < '
                          'tau everywhere and no argmax difference (>= 4 points); else INCONCLUSIVE; 0 points NOT_MEASURED',
        'OUTCOME_BENEFIT': 'PASS iff both FORK cells Y_D_TRUE=1, Y_NONE=0, Y_D_WRONG=0 and both MISSING cells Y_D_TRUE >= max(Y_NONE, '
                           'Y_D_WRONG) with >= 1 actual D_TRUE read in that MISSING episode; complete binary matrix else NOT_MEASURED; '
                           'otherwise FAIL; OUTCOME_PARTIAL reports a partial gain, never as PASS',
        'NATIVE_RECOVERY': 'events = D_TRUE decisions with an UNKNOWN hop and an actual physical read; recovery = ACQUIRE->MOUNTED, '
                           'REJECT->UNMOUNTED or BACKTRACK->POINTER_RETRACTED AND a following native hop that is not UNKNOWN. PASS: >= 1 '
                           'event and all are recoveries; FAIL: any event is not; NOT_MEASURED: no event. Observation only',
        'all': 'requires TECHNICAL_STATUS COMPLETE and PHYSICAL_READ PASS, else INCONCLUSIVE / NOT_MEASURED',
        'OVERALL': 'PASS iff all seven PASS; TECHNICAL_STATUS != COMPLETE -> that status; any FAIL -> FAIL; else INCONCLUSIVE'},
    'known_limits': ['10_FORK t5: the direct t4->t5 transition (E4) is not readable at t5 (current V5 overlap); no immediate read, '
                     'no UNKNOWN exception, no horizon extension', 'MISSING: if a D episode continues past t3, the NONE donor (STOP '
                     'at t3 in TEST888) has no post-step-4 appraisal -> NO_EXACT_POST_STEP_DONOR -> TECHNICAL_BLOCK (expected risk)'],
    'not_claimed': ['learning (weights are frozen)', 'generalization beyond 2 worlds x 2 conditions', 'GPU success before the run'],
    'budget': '75 min from the first line of this cell; guard883 before every step / write / read set; admit883 before every '
              'episode after the first (1.25 safety, 180 s reserve, 6 GiB free); 12 episodes, horizon 6'}
PREREG_SHA889 = _h889.sha256(_j889.dumps(PREREG889, sort_keys=True, default=str).encode()).hexdigest()
STATE889 = {'status': 'NOT_STARTED', 'technical_status': None, 'gates': {}, 'source': {}, 'episodes': [], 'points': [],
            'closures': [], 'negatives': None, 'physical_failure': None, 'post_run': None, 'scores': None, 'verdict': None,
            'blocked_episodes': [], 'error': None, 'traceback': None, 'artifact_errors': [], 'seq': 0}


def gate889(name, status, **info):
    rec = dict(status=status, wall_s=round(_t889.perf_counter() - T_CELL889, 1), **info)
    STATE889['gates'][name] = rec
    print('T889 GATE', name, status, _j889.dumps(rec, sort_keys=True, default=str)[:900], flush=True)
    if status != 'PASS': raise Gate_m867('%s %s' % (name, status))


# ============================ pure functions (CPU-tested at G0) ============================
def body_lock889(src):
    if not isinstance(src, str): return {'ok': False, 'why': 'NO_SOURCE'}
    lines = canon_lines_m867(src)
    if not lines: return {'ok': False, 'why': 'EMPTY_SOURCE'}
    m = _r889.fullmatch(r'#\s*TEST889\s+BODY-SHA256\s+([0-9a-f]{64})', lines[0].strip())
    if not m: return {'ok': False, 'why': 'NO_LOCK_LINE_FIRST', 'first_line_repr': repr(src.lstrip()[:100])}
    got = _h889.sha256(('\n'.join(lines[1:]) + '\n').encode('utf-8')).hexdigest()
    return {'ok': got == m.group(1), 'why': None if got == m.group(1) else 'BODY_HASH_MISMATCH', 'expected': m.group(1),
            'measured': got, 'canonical_lines': len(lines) - 1}


def eligible889(t):
    # the single expected event at decision t: (step_written, post_appraisal_step) or None
    return (t - LAG889, t - 1) if t > LAG889 else None


def expected889(n_steps, end, horizon=None):
    # closures: one per nonterminal step s followed by a CONTROL at s+1 (= expected_cartridges883); reads: decisions t >= 3
    w = expected_cartridges883(n_steps, end, horizon)
    return (None, None) if w is None else (w, max(0, int(n_steps) - LAG889))


def donor_v889(ledger, post_step, ep_id):
    # exact post-appraisal step of the NONE donor; never clamped, never the last record, never another step
    if not ledger or post_step not in ledger:
        raise Gate883('NO_EXACT_POST_STEP_DONOR %s post_step=%s donor_steps=%s' % (ep_id, post_step, sorted(ledger or {})))
    return ledger[post_step]


def read_contract889(entry, card, own_step, ep_id, cdir):
    # per-read contract of a V_after cartridge, checked before the model reads; own_step = step_written + 1 (its own closure step)
    why = []
    prov = entry.get('provenance') if isinstance(entry, dict) else None
    if not isinstance(prov, dict): return ['PROVENANCE_MISSING']
    for k in ('test', 'namespace', 'action', 'spans_body', 'step_written', 'post_appraisal_step', 'episode_id', 'X_sha256', 'V_rows_sha256'):
        if k not in prov: why.append('PROVENANCE_FIELD_MISSING:' + k)
    if why: return why
    if prov['test'] != 'TEST889' or prov['namespace'] != 'EPISODE_ONLY_NOT_A_BANK_CARD': why.append('PROVENANCE_NAMESPACE')
    if prov['action'] in TERMINAL883: why.append('PROVENANCE_TERMINAL_ACTION')
    if prov['episode_id'] != ep_id: why.append('PROVENANCE_EPISODE')
    if prov['step_written'] != own_step - 1: why.append('STEP_WRITTEN %s != %s' % (prov['step_written'], own_step - 1))
    if prov['post_appraisal_step'] != prov['step_written'] + 1: why.append('POST_STEP %s' % prov['post_appraisal_step'])
    eid = 'X889_' + _h889.sha256(_j889.dumps(prov, sort_keys=True, default=str).encode()).hexdigest()[:16]
    if entry.get('id') != eid: why.append('ID_NOT_PROVENANCE_HASH')
    for k in ('id', 'sha256', 'tensor_sha', 'body_tokens', 'pre_C_seal'):
        if card.get(k) != entry.get(k): why.append('MANIFEST_MISMATCH:' + k)
    if not str(entry.get('file', '')).startswith(str(cdir) + _o889.sep): why.append('FILE_OUTSIDE_EPISODE_DIR')
    sp = prov['spans_body']; q = entry.get('body_tokens')
    try:
        x2, a_, v_ = [list(map(int, sp[k])) for k in ('X2', 'A', 'V_AFTER')]
        if not (x2[0] == 0 and x2[1] == a_[0] and a_[1] == v_[0] and 0 < x2[1] < a_[1] < v_[1] and v_[1] == int(q)):
            why.append('SPANS_NOT_CONTIGUOUS_OR_V_END_NE_BODY_TOKENS')
        if list(card.get('V_span_body') or []) != v_: why.append('V_SPAN_MANIFEST_MISMATCH')
    except (KeyError, TypeError, ValueError):
        why.append('SPANS_MALFORMED')
    return why


def overlap889(v_after, v_now, v_before, older):
    # each: {'rows', 'text', 'sha'}; older: list of the episode's earlier own appraisals (excluding v_now)
    now = rowset_m888(v_now['rows']); va = rowset_m888(v_after['rows'])
    norm = lambda s: ' '.join((s or '').split()).lower()
    row_echo, text_rep = bool(va & now), norm(v_after['text']) == norm(v_now['text'])
    prior = [p for p in ([v_before] + list(older)) if p is not None]
    prior_rep = any(bool(va & rowset_m888(p['rows'])) or norm(v_after['text']) == norm(p['text']) for p in prior)
    return {'class': 'CURRENT_V_ROW_ECHO' if row_echo else ('CURRENT_V_TEXT_REPEAT' if text_rep else 'NOVEL'),
            'prior_appraisal_repeat': prior_rep, 'row_echo_rows': len(va & now), 'v_after_text': v_after['text'],
            'v_now_text': v_now['text']}


def recovery889(episodes):
    out = {a: {'events': 0, 'recoveries': 0, 'non_recovery': []} for a in ARMS889}
    for e in episodes:
        steps = e.get('steps', [])
        for i, s in enumerate(steps):
            if e.get('arm') not in out or s.get('hop_kind') != 'UNKNOWN' or not s.get('eligible_read'): continue
            out[e['arm']]['events'] += 1
            nxt = steps[i + 1] if i + 1 < len(steps) else None
            ok = (RECOVERY_ACTIONS889.get(s['action']) is not None and (s.get('effect') or {}).get('effect') == RECOVERY_ACTIONS889[s['action']]
                  and nxt is not None and nxt.get('hop_kind') != 'UNKNOWN')
            if ok: out[e['arm']]['recoveries'] += 1
            else: out[e['arm']]['non_recovery'].append('%s t%d %s %s next=%s' % (e['episode_id'], s['step'], s['action'],
                                                       (s.get('effect') or {}).get('effect'), None if nxt is None else nxt.get('hop_kind')))
    return out


def verdict889(status, physical, points, scores, recovery, closures, missing_reads):
    v = {'TECHNICAL_STATUS': status, 'reasons': {}}
    v['PHYSICAL_READ'] = verdict_m867(status, physical, [], {})['PHYSICAL_READ']
    ok = status == 'COMPLETE' and v['PHYSICAL_READ'] == 'PASS'
    v['APPRAISAL_PROVENANCE'] = ('NOT_MEASURED' if not closures else 'FAIL' if not all(c['ok'] for c in closures) else
                                 'PASS' if ok else 'INCONCLUSIVE')
    U = unique_m888(points); worlds = {p['world'] for p in U}; cls = [p['overlap']['class'] for p in U]
    v['reasons']['points'] = {'raw': len(points), 'unique': len(U), 'worlds': sorted(worlds), 'classes': cls,
                              'prior_appraisal_repeat': sum(1 for p in U if p['overlap']['prior_appraisal_repeat'])}
    if not U: v['APPRAISAL_NONREDUNDANCY'] = 'NOT_MEASURED'
    elif not ok: v['APPRAISAL_NONREDUNDANCY'] = 'INCONCLUSIVE'
    elif all(c == 'CURRENT_V_ROW_ECHO' for c in cls): v['APPRAISAL_NONREDUNDANCY'] = 'FAIL'
    elif 'NOVEL' in cls: v['APPRAISAL_NONREDUNDANCY'] = 'PASS'
    else: v['APPRAISAL_NONREDUNDANCY'] = 'INCONCLUSIVE'
    ch = [p for p in U if p['tv_sham_blind'] > 0 or p['a_true_sham'] != p['a_true_blind']]
    v['reasons']['channel_points'] = len(ch)
    if not U: v['APPRAISAL_CHANNEL'] = 'NOT_MEASURED'
    elif not ok: v['APPRAISAL_CHANNEL'] = 'INCONCLUSIVE'
    elif ch: v['APPRAISAL_CHANNEL'] = 'PASS'
    elif len(U) >= MIN_PAIRS_M867: v['APPRAISAL_CHANNEL'] = 'FAIL'
    else: v['APPRAISAL_CHANNEL'] = 'INCONCLUSIVE'
    eff = {p['world'] for p in U if p['tv_true_wrong'] >= TAU_M867}; diff = [p for p in U if p['a_true'] != p['a_wrong']]
    v['reasons']['content'] = {'worlds_tv_ge_tau': sorted(eff), 'argmax_differs': len(diff),
                               'max_tv_true_wrong': max((p['tv_true_wrong'] for p in U), default=None)}
    if not U: v['CONTENT_EFFECT'] = 'NOT_MEASURED'
    elif not ok or len(U) < MIN_PAIRS_M867: v['CONTENT_EFFECT'] = 'INCONCLUSIVE'
    elif set(WORLDS_M867) <= eff and diff: v['CONTENT_EFFECT'] = 'PASS'
    elif not eff and not diff: v['CONTENT_EFFECT'] = 'FAIL'
    else: v['CONTENT_EFFECT'] = 'INCONCLUSIVE'
    v['presence_points'] = sum(1 for p in U if p['tv_true_none'] >= TAU_M867)
    v['presence_only_points'] = sum(1 for p in U if p['tv_true_none'] >= TAU_M867 and p['a_true'] == p['a_wrong']
                                    and p['tv_true_wrong'] < TAU_M867)
    Y = {'%s_%s_%s' % (a, w, c): (scores or {}).get('%s_%s_%s' % (a, w, c), {}).get('Y') for (w, c) in CELLS_M867 for a in ARMS889}
    v['reasons']['Y'] = Y; v['reasons']['missing_d_true_reads'] = missing_reads
    binary = all(y in (0, 1) for y in Y.values())
    gain = [w for w in WORLDS_M867 if binary and Y['D_TRUE_%s_FORK' % w] == 1 and Y['NONE_%s_FORK' % w] == 0 and Y['D_WRONG_%s_FORK' % w] == 0]
    v['OUTCOME_PARTIAL'] = '%d/2 FORK cells with a D_TRUE-specific gain' % len(gain) if binary else None
    if not ok or not binary or any(not (missing_reads or {}).get(w) for w in WORLDS_M867): v['OUTCOME_BENEFIT'] = 'NOT_MEASURED'
    else:
        miss = all(Y['D_TRUE_%s_MISSING' % w] >= max(Y['NONE_%s_MISSING' % w], Y['D_WRONG_%s_MISSING' % w]) for w in WORLDS_M867)
        v['OUTCOME_BENEFIT'] = 'PASS' if len(gain) == len(WORLDS_M867) and miss else 'FAIL'
    dt = (recovery or {}).get('D_TRUE', {}); v['reasons']['recovery'] = recovery
    if not ok: v['NATIVE_RECOVERY'] = 'INCONCLUSIVE'
    elif not dt.get('events'): v['NATIVE_RECOVERY'] = 'NOT_MEASURED'
    elif dt['recoveries'] == dt['events']: v['NATIVE_RECOVERY'] = 'PASS'
    else: v['NATIVE_RECOVERY'] = 'FAIL'
    seven = [v[k] for k in ('PHYSICAL_READ', 'APPRAISAL_PROVENANCE', 'APPRAISAL_NONREDUNDANCY', 'APPRAISAL_CHANNEL', 'CONTENT_EFFECT',
                            'OUTCOME_BENEFIT', 'NATIVE_RECOVERY')]
    v['OVERALL'] = (status if status != 'COMPLETE' else 'PASS' if all(x == 'PASS' for x in seven) else
                    'FAIL' if 'FAIL' in seven else 'INCONCLUSIVE')
    return v


# ============================ runtime (model) ============================
def write_appraisal889(env, E, v_rows, cdir, meta):
    # the 885 writer procedure with the body [EVALUATION slot][V_after rows] instead of [C][E]; physical format: locked write_exp878
    global EXP_DIR878
    cut, dev, Hd = APPEND873['CUT'], env['DEV'], int(env['H']); n1 = E['n2'] + E['L2'] + E['la']
    one = lambda n: torch.ones((1, n), device=dev, dtype=torch.long)
    Y, _ = env['make_x851'](SLOTS866['EVALUATION'], [([], v_rows)], []); body = int(Y.shape[0])
    own2 = env['cache_build'](list(E['keep'])); forward873(env, own2, Y, n1); gH = kv873(env, own2); del own2
    h3v = xspan878(env, E['cl'], Y.reshape(1, body, Hd), one(n1 + body), 0, cut + 1)
    ck = dict(E['checks'])
    ck['V_explicit_lower_KV_bitwise'] = all(torch.equal(a[:, :, n1:], b[:, :, n1:n1 + body]) for i in range(cut + 1)
                                            for a, b in zip(cache_kv870(E['cl'], i), gH[i]))
    ck['V_h3_next_layer_KV_bitwise'] = all(torch.equal(a, b[:, :, n1:n1 + body]) for a, b in zip(next_kv878(env, h3v, n1), gH[cut + 1]))
    ffe883(body, 80 + cut + 1, 'experience_V')
    if not all(ck.values()): raise Gate883('PHYSICAL_APPRAISAL_WRITE_GATES %s' % sorted(k for k, x in ck.items() if not x))
    prov = dict(meta, test='TEST889', namespace='EPISODE_ONLY_NOT_A_BANK_CARD', requires_parent=False, action=E['action'],
                action_token_ids=E['A'], X_sha256=E['X_sha256'], source_prefix_tokens=E['n2'], post_appraisal_step=meta['step_written'] + 1,
                spans_body={'X2': [0, E['L2']], 'A': [E['L2'], E['L2'] + E['la']], 'V_AFTER': [E['L2'] + E['la'], E['L2'] + E['la'] + body]},
                V_kind='NATIVE_EVALUATION_ROWS_OF_THE_NEXT_STEP (control_step867)', V_rows_sha256=env['stats849'](v_rows)['sha256'],
                weights_digest=WEIGHTS0_878, engine_git_blob=ENGINE_BLOB883, head=HEAD883, cell_git_blob=STATE883['source'].get('executed_cell_git_blob'))
    eid = 'X889_' + _h889.sha256(_j889.dumps(prov, sort_keys=True, default=str).encode()).hexdigest()[:16]
    old, EXP_DIR878 = EXP_DIR878, type(ROOT864)(cdir)
    try:
        entry = write_exp878(env, eid, gH, torch.cat([E['hx'], E['ha'], h3v], dim=1), E['n2'], n1 + body, E['L2'] + E['la'], prov)
    finally:
        EXP_DIR878 = old
    if entry['roundtrip_K_rel'] > ROPE_TOL878: raise Gate883('PHYSICAL_APPRAISAL_ROUNDTRIP %.3e' % entry['roundtrip_K_rel'])
    rec = {k: entry[k] for k in ('id', 'sha256', 'bytes', 'body_tokens', 'roundtrip_K_rel', 'pre_C_seal')}
    rec.update({'tensor_sha': entry.get('tensor_sha'), 'V_span_body': prov['spans_body']['V_AFTER'], 'checks': ck,
                'step_written': meta['step_written'], 'post_appraisal_step': prov['post_appraisal_step'], 'V_rows_sha256': prov['V_rows_sha256']})
    with open(ROOT864 / 'TEST889_cards_manifest.jsonl', 'a', encoding='utf-8') as f:
        f.write(_j889.dumps(dict(rec, **{k: meta[k] for k in ('episode_id', 'world_index', 'condition', 'arm', 'cartridge_role')},
                                 v_source=meta.get('v_source')), sort_keys=True, default=str) + '\n')
    del gH, h3v, Y
    return entry, rec


def write_pair889(env, pend, v_true, donor_rec, step, cdir, key):
    # TRUE and WRONG from two independent prepare_experience883 of the same executed step; only V_after differs
    dv = donor_rec['rows']; n = int(v_true['rows'].shape[0])
    vw = shape_match867(env, dv, n)
    fit = {'donor_rows': int(dv.shape[0]), 'retained': min(int(dv.shape[0]), n), 'padded_mue': max(0, n - int(dv.shape[0])),
           'true_rows': n, 'donor_sha': donor_rec['sha'], 'donor_episode': donor_rec['episode_id'], 'donor_step': donor_rec['step']}
    meta = dict(key, step_written=step - 1)
    tw = _t889.perf_counter()
    et, rt = write_appraisal889(env, pend['true'], v_true['rows'], cdir, dict(meta, cartridge_role='TRUE',
                                v_source={'episode_id': key['episode_id'], 'step': step, 'sha': v_true['sha']}))
    ew, rw = write_appraisal889(env, pend['wrong'], vw, cdir, dict(meta, cartridge_role='WRONG', v_source=fit))
    geo = {'body_tokens_equal': rt['body_tokens'] == rw['body_tokens'],
           'spans_equal': et['provenance']['spans_body'] == ew['provenance']['spans_body'],
           'X2_A_rows_bitwise_equal': rt['pre_C_seal'] == rw['pre_C_seal'],
           'action_tokens_equal': et['provenance']['action_token_ids'] == ew['provenance']['action_token_ids'],
           'different_files': et['file'] != ew['file']}
    if not all(geo.values()): raise Gate883('PHYSICAL_GEOMETRY_MATCH %s' % sorted(k for k, x in geo.items() if not x))
    geo['V_rows_differ'] = et['provenance']['V_rows_sha256'] != ew['provenance']['V_rows_sha256']     # reported, never forced
    return {'true': (et, rt), 'wrong': (ew, rw), 'geometry': geo, 'fit': fit, 'write_s': round(_t889.perf_counter() - tw, 3)}


def read889(env, B, entry, card, X, own_step, ep_id, cdir, b_tokens, first, modes):
    # one SSD reload + one native append, then the requested reads on the same [B][E]: FULL blind=(), SHAM (V_after masked in the
    # kernel and restored), BLIND (V_after masked); the locked xcar878 is called unchanged
    why = read_contract889(entry, card, own_step, ep_id, cdir)
    if why: raise Gate883('PHYSICAL_READ_CONTRACT %s step_written=%s: %s' % (ep_id, own_step - 1, why))
    n0 = length873(env, B)
    if n0 != b_tokens: raise Gate883('PHYSICAL_B_LENGTH %d != %d' % (n0, b_tokens))
    seal0 = full_seal881(B)['all'] if first else None
    try:
        cp = load_exp878(env, entry)
    except Persist878 as exc:
        raise Gate883('PHYSICAL_RELOAD %s: %s' % (ep_id, exc))
    q = int(cp['body_tokens']); g = append_exp878(env, B, cp); ffe883(q, 80, 'experience_mount')
    sp = entry['provenance']['spans_body']['V_AFTER']; V = [n0 + int(sp[0]), n0 + int(sp[1])]
    rec = {'cartridge': entry['id'], 'n_exact': length873(env, g) == n0 + q, 'v_span_inside': n0 <= V[0] < V[1] == n0 + q,
           'prefix_rows_bitwise': bool(torch.equal(g[0][0][:, :, :n0], B[0][0]) and torch.equal(g[-1][1][:, :, :n0], B[-1][1]))}
    if first:
        gx = xappend878(env, B, cp, ()); ffe883(q, 80, 'experience_mount_parity')
        rec['explicit_equals_native_append_bitwise'] = all(torch.equal(a[t], b[t]) for a, b in zip(g, gx) for t in (0, 1)); del gx
        rec['B_full_seal_unchanged'] = full_seal881(B)['all'] == seal0
    out = {}
    for m in modes:
        c0 = int(env['CALLS849'])
        out[m] = xcar878(env, g, X, () if m == 'FULL' else [V], m == 'SHAM'); ffe883(int(X.shape[0]) + cont_tokens881(), 80, 'decision_read')
        rec['calls_' + m] = int(env['CALLS849']) - c0; rec['finite_' + m] = finite_m867(out[m])
    del g, cp
    bad = sorted(k for k, x in rec.items() if isinstance(x, bool) and not x)
    if bad: raise Gate883('PHYSICAL_READ_GATES %s %s: %s' % (ep_id, entry['id'], bad))
    return out, rec


def episode889(env, spec, arm, ep_id, horizon, donor_ledger):
    # one natural episode. NONE: the native reading is executed and the native appraisals are ledgered (donor source). D_TRUE /
    # D_WRONG: every nonterminal step s is closed at s+1 with V_(s+1) (TRUE own, WRONG exact-step donor) and written; decision
    # t >= 3 executes the arm's FULL reading of E_(t-2); t1, t2 execute the NONE reading (== native bitwise).
    key = {'world_index': int(spec['world_index']), 'condition': spec['condition'], 'arm': arm, 'episode_id': ep_id}
    ctx = {'spec': spec, 'arm': 'NO_FEEDBACK', 'M': list(spec['initial']), 'memx': None, 'path': [], 'prev_state': None,
           'own_states': [], 'events': [], 'mount_records': [], 'acquisitions': 0, 'rejections': 0, 'addresses': 0,
           'steps': 0, 'hops': 0, 'donor_item': None}
    cdir = _o889.path.join(CART_ROOT883, ep_id)
    out = dict(key, item=spec['item'], steps=[], points=[], closures=[], vledger={}, end=None, accepted=None, error=None,
               cartridges=[], wrong_cartridges=[])
    led = {}                                   # step -> {'rows', 'text', 'sha', 'seq'} own native appraisals
    written, pend = {}, None
    t0, calls0, initial_seal, interrupted, step_sum = _t889.perf_counter(), int(env['CALLS849']), None, None, 0.0
    try:
        try:
            _o889.makedirs(cdir, exist_ok=False)
            q = env['QTEXT841'][spec['qid']]; pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
            ctx['memx'], mount = mount865(env, ctx['M'], 'TEST889_L0_%s_%s' % (arm, spec['item'])); ctx['mount_records'].append(mount)
            initial_seal = prefix_seals865(env, ctx['memx'])
            while out['end'] is None:
                if ctx['steps'] >= horizon: out['end'] = 'HORIZON_%d' % horizon; break
                if not budget_left865(env, STEP_CALLS867): out['end'] = 'RESOURCE_BUDGET'; break
                guard883('%s_t%d' % (ep_id, ctx['steps'] + 1)); ts = _t889.perf_counter(); sc0 = int(env['CALLS849'])
                k = len(ctx['path']); pointer = None if k == 0 else ctx['path'][-1]['rows']
                ptext = None if k == 0 else ctx['path'][-1]['text']; m_before = list(ctx['M'])
                h, kind = hop865(env, ctx['memx'], spec['qid'], k, pointer); ctx['hops'] += 1
                ctx['events'].append({'type': 'HOP', 'k': k, 'kind_logged_only': kind, 'raw': h['text'], 'mounted': list(ctx['M']),
                                      'decision_source': 'MODEL'})
                if kind == 'EMPTY_OUTPUT': out['end'] = 'NATIVE_EMPTY_OUTPUT'; break
                feedback, fb_info = feedback867(env, ctx)
                control, record, state = control_step867(env, ctx, h, pointer, feedback)
                if control is None: out['end'] = 'NATIVE_EMPTY_STATE'; break     # no V_t: a pending E_(t-1) stays open
                ctx['steps'] += 1; t = ctx['steps']; B = ctx['memx']; X, _ = env['make_x851'](pre, state['segments'], post)
                slot, v_rows = state['segments'][-1]
                if list(slot) != list(SLOTS866['EVALUATION']): raise Gate883('APPRAISAL_SEGMENT_NOT_LAST %s t%d' % (ep_id, t))
                STATE889['seq'] += 1
                led[t] = {'rows': v_rows, 'text': record['evaluation_text'], 'sha': record['state_sha256']['V'], 'seq': STATE889['seq'],
                          'episode_id': ep_id, 'step': t}
                if env['stats849'](v_rows)['sha256'] != led[t]['sha']: raise Gate883('APPRAISAL_PROVENANCE_V_SHA %s t%d' % (ep_id, t))
                with open(ROOT864 / 'TEST889_native_appraisals.jsonl', 'a', encoding='utf-8') as f:
                    f.write(_j889.dumps(jsafe878(dict(key, step=t, seq=led[t]['seq'], V_sha256=led[t]['sha'], V_rows=int(v_rows.shape[0]),
                        text=record['evaluation_text'], state_sha256=record['state_sha256'], X_sha256=tsha881(X),
                        mounted_before=m_before, path_before=[p['text'] for p in ctx['path']], hop=h['text'], hop_kind=kind,
                        evaluation_generation=record['full']['evaluation'],
                        R_sha256=env['stats849'](state['segments'][2][1])['sha256'],
                        P_sha256=None if pointer is None else env['stats849'](pointer)['sha256'])), sort_keys=True) + '\n')
                st = dict(key, step=t, hop=h['text'], hop_kind=kind, pointer=ptext, state_sha256=record['state_sha256'],
                          X_sha256=tsha881(X), B_tokens=length873(env, B), native=reading_view883(record['reading']), eligible_read=False)
                if not finite_m867(record['reading']): raise Gate883('PHYSICAL_NONFINITE_NATIVE_READING %s t%d' % (ep_id, t))
                cache = None
                if arm == 'NONE':
                    reading = record['reading']; out['vledger'][t] = led[t]
                else:
                    cache = env['cache_build'](list(B)); nat = car873(env, cache, X); ffe883(int(X.shape[0]) + cont_tokens881(), 80, 'native_read')
                    if not same_reading881(nat, record['reading']): raise Gate883('PHYSICAL_X_PARITY car873 != control_step867 %s t%d' % (ep_id, t))
                    r_none = none_m867(env, B, X, record['reading']); reading = r_none
                    if pend is not None:                       # closure of E_(t-1) by the real V_t, then SSD commit
                        guard883('%s_t%d_close' % (ep_id, t)); s_ = pend['step']
                        donor = donor_v889(donor_ledger, t, ep_id)
                        w = write_pair889(env, pend, led[t], donor, t, cdir, key)
                        STATE889['seq'] += 1
                        cl = {'episode_id': ep_id, 'step_written': s_, 'post_appraisal_step': t, 'commit_seq': STATE889['seq'],
                              'checks': {'v_after_is_post_step_ledger': w['true'][0]['provenance']['V_rows_sha256'] == led[t]['sha'],
                                         'v_before_is_action_step_ledger': pend['v_before_sha'] == led[s_]['sha'],
                                         'x2_is_action_step_input': pend['true']['X_sha256'] == pend['X_sha256'] == pend['wrong']['X_sha256'],
                                         'action_is_executed_reading_and_effect': pend['action'] == pend['effect_action'] == w['true'][0]['provenance']['action'],
                                         'action_tokens_are_native_ids': list(w['true'][0]['provenance']['action_token_ids']) == list(dict(ACTION_IDS867)[pend['action']]),
                                         'commit_after_v_after_generation': led[t]['seq'] < STATE889['seq'],
                                         'donor_exact_step': w['fit']['donor_step'] == t,
                                         'donor_sha_is_ledger': w['wrong'][0]['provenance']['v_source']['donor_sha'] == donor['sha']}}
                        cl['ok'] = all(cl['checks'].values())
                        out['closures'].append(cl)
                        with open(ROOT864 / 'TEST889_controls.jsonl', 'a', encoding='utf-8') as f: f.write(_j889.dumps(jsafe878(dict(cl, kind='CLOSURE', fit=w['fit'], geometry=w['geometry'])), sort_keys=True) + '\n')
                        if not cl['ok']: raise Gate883('PHYSICAL_APPRAISAL_PROVENANCE %s %s' % (ep_id, sorted(k_ for k_, x in cl['checks'].items() if not x)))
                        written[s_] = w; pend = None
                        out['cartridges'].append(w['true'][1]); out['wrong_cartridges'].append(w['wrong'][1])
                        if STATE889['negatives'] is None: STATE889['negatives'] = negatives_m867(env, w['true'][0])
                    ev = eligible889(t)
                    if ev is not None:                         # the single expected event; no fallback
                        sw, ps = ev
                        if sw not in written: raise Gate883('PHYSICAL_EXPECTED_EVENT_MISSING %s t%d E%d' % (ep_id, t, sw))
                        guard883('%s_t%d_read' % (ep_id, t)); d = written[sw]; pv = d['true'][0]['provenance']
                        if not (pv['step_written'] == sw and pv['post_appraisal_step'] == ps < t and
                                d['wrong'][0]['provenance']['step_written'] == sw):
                            raise Gate883('PHYSICAL_EVENT_ELIGIBILITY %s t%d %s/%s' % (ep_id, t, pv['step_written'], pv['post_appraisal_step']))
                        first = not out['points']; tr = _t889.perf_counter()
                        rT, cT = read889(env, B, d['true'][0], d['true'][1], X, sw + 1, ep_id, cdir, st['B_tokens'], first, ('FULL', 'SHAM', 'BLIND'))
                        rW, cW = read889(env, B, d['wrong'][0], d['wrong'][1], X, sw + 1, ep_id, cdir, st['B_tokens'], first, ('FULL', 'BLIND'))
                        if cT['calls_FULL'] != cW['calls_FULL'] or cT['calls_BLIND'] != cW['calls_BLIND']:
                            raise Gate883('PHYSICAL_CALL_PARITY %s t%d' % (ep_id, t))
                        blind_eq = same_reading881(rT['BLIND'], rW['BLIND'])
                        va = {'rows': led[ps]['rows'], 'text': led[ps]['text'], 'sha': led[ps]['sha']}
                        pt = dict(key, world='%02d' % key['world_index'], step=t, step_written=sw, post_appraisal_step=ps,
                                  a_none=r_none['action'], a_true=rT['FULL']['action'], a_wrong=rW['FULL']['action'],
                                  a_true_sham=rT['SHAM']['action'], a_true_blind=rT['BLIND']['action'], a_wrong_blind=rW['BLIND']['action'],
                                  tv_true_wrong=tv_m867(rT['FULL'], rW['FULL']), tv_true_none=tv_m867(rT['FULL'], r_none),
                                  tv_wrong_none=tv_m867(rW['FULL'], r_none), tv_sham_blind=tv_m867(rT['SHAM'], rT['BLIND']),
                                  tv_full_sham_kernel=tv_m867(rT['FULL'], rT['SHAM']), tv_blind_none=tv_m867(rT['BLIND'], r_none),
                                  blind_true_equals_wrong_bitwise=blind_eq,
                                  none=summary_m888(r_none), true_full=summary_m888(rT['FULL']), true_sham=summary_m888(rT['SHAM']),
                                  true_blind=summary_m888(rT['BLIND']), wrong_full=summary_m888(rW['FULL']), wrong_blind=summary_m888(rW['BLIND']),
                                  overlap=overlap889(va, led[t], led.get(sw), [led[j] for j in sorted(led) if j < sw]),
                                  donor_fit=d['fit'], v_rows_differ=d['geometry']['V_rows_differ'], body_tokens=int(d['true'][1]['body_tokens']),
                                  cartridge_true=cT['cartridge'], cartridge_wrong=cW['cartridge'], read_true=cT, read_wrong=cW)
                        pt['unique_key'] = _h889.sha256(_j889.dumps([pt['world'], spec['condition'], t, st['X_sha256'], list(ctx['M']),
                                                                     st['B_tokens'], [p['text'] for p in ctx['path']], va['sha']],
                                                                    sort_keys=True, default=str).encode()).hexdigest()
                        if first:
                            rR, _ = read889(env, B, d['true'][0], d['true'][1], X, sw + 1, ep_id, cdir, st['B_tokens'], False, ('FULL',))
                            pt['repeat_reload_bitwise'] = same_reading881(rT['FULL'], rR['FULL'])
                        with open(ROOT864 / 'TEST889_points.jsonl', 'a', encoding='utf-8') as f: f.write(_j889.dumps(jsafe878(pt), sort_keys=True) + '\n')
                        with open(ROOT864 / 'TEST889_controls.jsonl', 'a', encoding='utf-8') as f:
                            f.write(_j889.dumps(jsafe878({'kind': 'READ', 'episode_id': ep_id, 'step': t, 'blind_true_equals_wrong_bitwise': blind_eq,
                                                          'repeat_reload_bitwise': pt.get('repeat_reload_bitwise'), 'read_true': cT,
                                                          'read_wrong': cW, 'negatives': STATE889['negatives']}), sort_keys=True) + '\n')
                        out['points'].append(pt)
                        if not blind_eq: raise Gate883('PHYSICAL_AFTER_BLIND_LEAK %s t%d' % (ep_id, t))
                        if first and not pt['repeat_reload_bitwise']: raise Gate883('PHYSICAL_REPEAT_NOT_BITWISE %s t%d' % (ep_id, t))
                        st['exp_op'] = exp_op883(ep_id, t, arm, int(d['true'][1]['body_tokens']), d['write_s'], round(_t889.perf_counter() - tr, 3))
                        reading = rT['FULL'] if arm == 'D_TRUE' else rW['FULL']; st['eligible_read'] = True
                        st['event'] = {'E': sw, 'class': pt['overlap']['class'], 'a_none': pt['a_none'], 'a_true': pt['a_true'],
                                       'a_wrong': pt['a_wrong'], 'tv_tw': round(pt['tv_true_wrong'], 4), 'tv_sb': round(pt['tv_sham_blind'], 4)}
                action = reading['action']
                st.update({'reading': reading_view883(reading), 'action': action, 'decision_source': 'MODEL_CAR_READING_' + arm,
                           'differs_from_native': action != record['action']})
                ctx['events'].append({'type': 'CONTROL', 'k': k, 'step': t, 'action': action, 'decision_source': 'MODEL',
                                      'mounted': list(ctx['M']), 'state_sha256': record['state_sha256'], 'f1_arm': arm})
                terminal = action in TERMINAL883
                if arm != 'NONE' and not terminal:
                    pend = {'true': prepare_experience883(env, cache, B, X, action), 'wrong': prepare_experience883(env, cache, B, X, action),
                            'step': t, 'action': action, 'X_sha256': tsha881(X), 'v_before_sha': led[t]['sha'], 'effect_action': None}
                del cache
                if action == 'INVALID': out['end'] = 'MODEL_INVALID_ACTION'
                elif action == 'ACCEPT': out['end'], out['accepted'] = 'MODEL_ACCEPT', h['text'].strip()
                elif action == 'STOP': out['end'] = 'MODEL_STOP'
                else:
                    ctx['prev_state'] = state['own_state']; n_ev = len(ctx['events'])
                    execute866(env, ctx, action, h, control, state)
                    eff = ctx['events'][-1]
                    st['effect'] = {x: eff.get(x) for x in ('action', 'effect', 'chosen', 'mounted_before', 'mounted_after', 'path_after')}
                    st['effect']['executed_equals_reading'] = bool(eff.get('type') == 'EFFECT' and eff.get('action') == action and
                                                                   len(ctx['events']) == n_ev + 1)
                    if not st['effect']['executed_equals_reading']: raise Gate883('EFFECT_CONTRACT at %s t%d' % (ep_id, t))
                    if pend is not None: pend['effect_action'] = eff.get('action')
                st['seconds'] = round(_t889.perf_counter() - ts, 3); st['calls'] = int(env['CALLS849']) - sc0; step_sum += st['seconds']
                out['steps'].append(st)
                with open(ROOT864 / 'TEST889_decisions.jsonl', 'a', encoding='utf-8') as f: f.write(_j889.dumps(jsafe878(st), sort_keys=True) + '\n')
                ev_ = st.get('event')
                line883('STEP', ep_id, 't=%d' % t, 'hop=%r' % h['text'], 'exec=%s' % action, 'native=%s' % record['action'],
                        'event=%s' % ('E%d %s N/T/W=%s/%s/%s tv_tw=%.3f tv_sb=%.3f' % (ev_['E'], ev_['class'], ev_['a_none'], ev_['a_true'],
                                     ev_['a_wrong'], ev_['tv_tw'], ev_['tv_sb']) if ev_ else '-'),
                        'effect=%s' % (st.get('effect') or {}).get('effect'), 's=%.1f' % st['seconds'])
                STATE883['budget']['nofb_step_seconds' if arm == 'NONE' else 'step_seconds'].append(st['seconds'])
        except AssertionError as exc:
            if exc.args and isinstance(exc.args[0], tuple) and exc.args[0] and exc.args[0][0] == 'CONTEXT_LIMIT':
                out['end'] = 'PHYSICAL_CONTEXT_LIMIT'; out['error'] = str(exc)
            else:
                out['end'], out['error'], out['traceback'] = 'EXECUTION_ERROR', '%s: %s' % (type(exc).__name__, exc), traceback.format_exc()
        except Budget883 as exc:
            out['end'], out['error'] = 'BUDGET_STOP', str(exc)
        except Gate883 as exc:
            out['end'], out['error'], out['traceback'] = 'TECHNICAL_BLOCK', str(exc), traceback.format_exc()
            if str(exc).startswith('PHYSICAL_'): STATE889['physical_failure'] = str(exc)[:500]
        except Exception as exc:
            out['end'], out['error'], out['traceback'] = 'EXECUTION_ERROR', '%s: %s' % (type(exc).__name__, exc), traceback.format_exc()
        except BaseException as exc:
            out['end'], out['error'], interrupted = 'INTERRUPTED', '%s: %s' % (type(exc).__name__, exc), exc
    finally:
        out['open_pending_at_end'] = None if pend is None else pend['step']
        pend = None; written.clear(); led.clear()
        cleanup883(env, ctx, out, spec, arm, cdir, initial_seal, interrupted is not None)
    contract = event_contract883(ctx['events'])
    controls = [e for e in ctx['events'] if e['type'] == 'CONTROL']
    exp_w, exp_r = expected889(ctx['steps'], out['end'], horizon) if arm != 'NONE' else (0, 0)
    out.update({'final_mounted': list(ctx['M']), 'n_steps': ctx['steps'], 'actions': [c['action'] for c in controls],
                'effects': [e['effect'] for e in ctx['events'] if e['type'] == 'EFFECT'], 'acquisitions': ctx['acquisitions'],
                'event_contract': {x: contract[x] for x in ('ok', 'problems', 'controls', 'effects')},
                'executed_equals_reading': bool(contract['ok'] and [c['action'] for c in controls] == [s['action'] for s in out['steps']]),
                'writes_expected': exp_w, 'reads_expected': exp_r, 'mount_integrity': mount_ok883(ctx['mount_records']),
                'cardinality_ok': exp_w is not None and len(out['cartridges']) == exp_w == len(out['wrong_cartridges']) == len(out['closures'])
                                  and len(out['points']) == exp_r,
                'seconds': round(_t889.perf_counter() - t0, 1), 'calls': int(env['CALLS849']) - calls0})
    out['overhead_s'] = round(out['seconds'] - step_sum, 1)
    STATE883['budget']['episode_overhead_s'].append(out['overhead_s'])
    line883('EPISODE', ep_id, 'end=%s' % out['end'], 'actions=%s' % '>'.join(out['actions']), 'accepted=%r' % out['accepted'],
            'reads=%d/%s' % (len(out['points']), exp_r), 'closures=%d+%d/%s' % (len(out['cartridges']), len(out['wrong_cartridges']), exp_w),
            'open_pending=%s' % out['open_pending_at_end'], 'restore=%s' % out['exact_restore_vs_first_mount'], 'contract=%s' % contract['ok'],
            's=%.0f' % out['seconds'], '' if not out['error'] else 'ERROR=' + str(out['error'])[:300])
    if out.get('traceback'): short864(out['traceback'])
    rec = {x: y for x, y in out.items() if x not in ('steps', 'points', 'vledger', 'closures')}
    with open(ROOT864 / 'episodes.jsonl', 'a', encoding='utf-8') as f: f.write(_j889.dumps(jsafe878(rec), sort_keys=True) + '\n')
    STATE889['episodes'].append(out); STATE889['points'] += out['points']; STATE889['closures'] += out['closures']
    if out['exact_restore_vs_first_mount'] is False and not STATE889['physical_failure']:
        STATE889['physical_failure'] = 'PHYSICAL_RESTORE_FALSE %s' % ep_id
    if interrupted is not None: raise interrupted
    if out['end'] in ('BUDGET_STOP', 'RESOURCE_BUDGET'): raise Budget883(out['error'] or out['end'])
    natural_empty = out['end'] in ('NATIVE_EMPTY_OUTPUT', 'NATIVE_EMPTY_STATE') and not controls
    bad = {'end': out['end'] in ('TECHNICAL_BLOCK', 'EXECUTION_ERROR', 'PHYSICAL_CONTEXT_LIMIT'),
           'restore': out['exact_restore_vs_first_mount'] is not True, 'mount': not out['mount_integrity'],
           'contract': not (out['executed_equals_reading'] or natural_empty), 'isolated': not out['isolated_after_episode'],
           'cleanup': bool(out['cleanup_errors']), 'cardinality': not (out['cardinality_ok'] or natural_empty)}
    if any(bad.values()):
        phys = (str(out['error'] or '').startswith('PHYSICAL_') if bad['end'] else
                any(bad[x] for x in ('restore', 'mount', 'isolated', 'cleanup')))
        raise Gate883('%sEPISODE_INTEGRITY %s PRIMARY=%s %s err=%s' % ('PHYSICAL_' if phys else '', ep_id, out['end'] if bad['end'] else None,
                                                                     sorted(x for x, y in bad.items() if y), str(out['error'])[:300]))
    return out


# ============================ G0 source capture + CPU selftests ============================
def capture889():
    try:
        src, how = get_ipython().history_manager.input_hist_raw[-1], 'IPYTHON_CURRENT_CELL'
    except NameError:
        src, how = (open(__file__, encoding='utf-8').read() if '__file__' in globals() else None), 'FILE'
    lock = body_lock889(src)
    if not lock['ok']:
        try:
            if isinstance(src, str): (ROOT864 / 'TEST889_captured_cell.txt').write_text(src, encoding='utf-8')
        except OSError: pass
        raise Gate_m867('SOURCE_SELF_LOCK %s (how=%s; paste the parts into ONE cell, in order, unchanged)' % (lock, how))
    tree, tb = _a889.parse(src), _a889.parse(B888_DEFS889 + '\n' + B887_M888)
    funcs = {n.name: n for n in tree.body if isinstance(n, _a889.FunctionDef)}
    fold = {n.name: n for n in tb.body if isinstance(n, _a889.FunctionDef)}
    for name, node in funcs.items(): scan883(node, EXEC_ALLOW889.get(name, ()))
    missing = sorted(set(RUNTIME_NEW889) - set(funcs)) + sorted(set(RUNTIME_OLD889) - set(fold))
    if missing: raise Gate_m867('RUNTIME_FUNCTIONS_MISSING %s' % missing)
    for name in RUNTIME_NEW889: oracle_scan883(funcs[name])
    for name in RUNTIME_OLD889: scan883(fold[name]); oracle_scan883(fold[name])
    redefined = sorted(set(funcs) & set(fold))
    if redefined: raise Gate_m867('LOCKED_FUNCTION_REDEFINED %s' % redefined)
    count = lambda f: sum(1 for n in _a889.walk(tree) if isinstance(n, _a889.Call) and getattr(n.func, 'id', None) == f)
    ep = funcs['episode889']
    action_assigns = [n for n in _a889.walk(ep) if isinstance(n, _a889.Assign) and any(isinstance(x, _a889.Name) and x.id == 'action' for x in n.targets)]
    ex_calls = [n for n in _a889.walk(ep) if isinstance(n, _a889.Call) and getattr(n.func, 'id', None) == 'execute866']
    facts = {'reproduce_pre859859_calls': count('reproduce_pre859859'), 'execute866_calls': count('execute866'),
             'input_calls': count('input'), 'rearm_budget865_calls': count('rearm_budget865'),
             'action_assigned_only_from_reading': [_a889.unparse(n.value) for n in action_assigns] == ["reading['action']"],
             'execute866_gets_that_action': len(ex_calls) == 1 and _a889.unparse(ex_calls[0].args[2]) == 'action',
             'no_event_fallback': not any(isinstance(n, _a889.Call) and any(isinstance(x, _a889.Name) and x.id == 'written' for x in n.args)
                                          for n in _a889.walk(ep))}
    if facts != {'reproduce_pre859859_calls': 1, 'execute866_calls': 1, 'input_calls': 0, 'rearm_budget865_calls': 1,
                 'action_assigned_only_from_reading': True, 'execute866_gets_that_action': True, 'no_event_fallback': True}:
        raise Gate_m867('SOURCE_FACTS %s' % facts)
    raw = src.encode('utf-8')
    (ROOT864 / 'TEST889.py').write_bytes(raw)
    STATE889['source'] = {'how': how, 'executed_cell_git_blob': git_blob864(raw), 'executed_cell_sha256': sha256_bytes864(raw),
                          'body_lock': lock, 'facts': facts, 'firewall': 'PASS', 'oracle_firewall': 'PASS %d+%d' % (len(RUNTIME_NEW889), len(RUNTIME_OLD889))}
    STATE883['source'] = {'executed_cell_git_blob': STATE889['source']['executed_cell_git_blob']}
    json_write864('TEST889_source_locks.json', dict(STATE889['source'], base888=B888_INFO889, base887=B887_INFO_M888, base885=BASE_INFO_M867,
                                                    engine=ENGINE_INFO883, head=HEAD883, prereg_sha256=PREREG_SHA889, before_model_load=True))
    print('T889 SOURCE blob=%s sha256=%s body_lock=%s' % (STATE889['source']['executed_cell_git_blob'],
                                                         STATE889['source']['executed_cell_sha256'], lock['measured']), flush=True)


def st889():
    import numpy as _np
    r = {}
    body = 'x = 1\nif x:\n    print(x)\n'; lk = '# TEST889 BODY-SHA256 ' + _h889.sha256(body.encode()).hexdigest()
    r['lock_ok'] = body_lock889(lk + '\n' + body)['ok']
    r['lock_wrong_hash_refused'] = not body_lock889(lk[:-1] + ('0' if lk[-1] != '0' else '1') + '\n' + body)['ok']
    r['lock_suffix_refused'] = not body_lock889(lk + '\n' + body + 'print(2)\n')['ok']
    r['lock_888_header_refused'] = not body_lock889(lk.replace('TEST889', 'TEST888') + '\n' + body)['ok']
    r['schedule_t1_t6'] = [eligible889(t) for t in range(1, 7)] == [None, None, (1, 2), (2, 3), (3, 4), (4, 5)]
    r['schedule_never_current_post_step'] = all(eligible889(t)[1] < t for t in range(3, 7))
    r['closures_natural_ends'] = [expected889(n, e, 6) for n, e in ((3, 'MODEL_STOP'), (6, 'HORIZON_6'), (5, 'MODEL_ACCEPT'), (1, 'MODEL_STOP'))] == \
        [(2, 1), (5, 4), (4, 3), (0, 0)]
    r['closures_undefined_on_technical_end'] = expected889(4, 'TECHNICAL_BLOCK', 6) == (None, None)
    L = {1: {'rows': 1, 'sha': 'a', 'step': 1, 'episode_id': 'N'}, 2: {'rows': 2, 'sha': 'b', 'step': 2, 'episode_id': 'N'},
         3: {'rows': 3, 'sha': 'c', 'step': 3, 'episode_id': 'N'}}
    r['donor_exact_step'] = donor_v889(L, 3, 'e')['sha'] == 'c'
    for nm, (led, stp) in (('short_donor_no_clamp', (L, 4)), ('no_donor', ({}, 2)), ('none_donor', (None, 2))):
        try: donor_v889(led, stp, 'e'); r['donor_%s_refused' % nm] = False
        except Gate883 as exc: r['donor_%s_refused' % nm] = 'NO_EXACT_POST_STEP_DONOR' in str(exc)
    # read contract on a synthetic V_after entry
    prov = {'test': 'TEST889', 'namespace': 'EPISODE_ONLY_NOT_A_BANK_CARD', 'action': 'ADVANCE', 'step_written': 2, 'post_appraisal_step': 3,
            'episode_id': 'EP', 'X_sha256': 'x', 'V_rows_sha256': 'v', 'spans_body': {'X2': [0, 10], 'A': [10, 12], 'V_AFTER': [12, 20]}}
    mk = lambda p: 'X889_' + _h889.sha256(_j889.dumps(p, sort_keys=True, default=str).encode()).hexdigest()[:16]
    ent = {'id': mk(prov), 'provenance': prov, 'sha256': 's', 'tensor_sha': 't', 'body_tokens': 20, 'pre_C_seal': 'p',
           'file': _o889.path.join('/cd', 'f.pt')}
    card = {k: ent[k] for k in ('id', 'sha256', 'tensor_sha', 'body_tokens', 'pre_C_seal')}; card['V_span_body'] = [12, 20]
    r['contract_ok'] = read_contract889(ent, card, 3, 'EP', '/cd') == []
    bad = {'wrong_episode': (ent, card, 3, 'EP2', '/cd'), 'wrong_own_step': (ent, card, 4, 'EP', '/cd'), 'wrong_dir': (ent, card, 3, 'EP', '/other'),
           'manifest_sha': (ent, dict(card, sha256='z'), 3, 'EP', '/cd'), 'v_span': (ent, dict(card, V_span_body=[11, 20]), 3, 'EP', '/cd')}
    for nm, args in bad.items(): r['contract_%s_refused' % nm] = bool(read_contract889(*args))
    p2 = dict(prov, test='TEST883'); r['contract_old_test_refused'] = bool(read_contract889(dict(ent, provenance=p2, id=mk(p2)), card, 3, 'EP', '/cd'))
    p3 = dict(prov, post_appraisal_step=2); r['contract_post_step_refused'] = bool(read_contract889(dict(ent, provenance=p3, id=mk(p3)), card, 3, 'EP', '/cd'))
    p4 = dict(prov, action='STOP'); r['contract_terminal_refused'] = bool(read_contract889(dict(ent, provenance=p4, id=mk(p4)), card, 3, 'EP', '/cd'))
    r['contract_tampered_provenance_refused'] = bool(read_contract889(dict(ent, provenance=dict(prov, V_rows_sha256='w')), card, 3, 'EP', '/cd'))
    p5 = dict(prov, spans_body={'X2': [0, 10], 'A': [10, 12], 'V_AFTER': [13, 20]})
    r['contract_gap_span_refused'] = bool(read_contract889(dict(ent, provenance=p5, id=mk(p5)), card, 3, 'EP', '/cd'))
    A = _np.arange(12, dtype=_np.float32).reshape(3, 4)
    V = lambda rows, text: {'rows': rows, 'text': text, 'sha': str(rows.sum())}
    r['overlap_row_echo'] = overlap889(V(A, 'a'), V(_np.concatenate([A[:1], A[1:] + 9]), 'b'), None, [])['class'] == 'CURRENT_V_ROW_ECHO'
    r['overlap_text_repeat'] = overlap889(V(A, 'Supported  step'), V(A + 1, 'supported step'), None, [])['class'] == 'CURRENT_V_TEXT_REPEAT'
    o = overlap889(V(A, 'x'), V(A + 1, 'y'), V(A, 'z'), [])
    r['overlap_novel_with_prior_flag'] = o['class'] == 'NOVEL' and o['prior_appraisal_repeat']
    r['overlap_novel_clean'] = overlap889(V(A, 'x'), V(A + 1, 'y'), V(A + 2, 'z'), [V(A + 3, 'w')]) == dict(
        overlap889(V(A, 'x'), V(A + 1, 'y'), V(A + 2, 'z'), [V(A + 3, 'w')]), **{'class': 'NOVEL', 'prior_appraisal_repeat': False})
    rd = {'action': 'ACQUIRE', 'mass': 0.9, 'margin_logp': 0.5, 'normalized': {w: 1 / 6 for w in ACTIONS_M867},
          'scores': [{'word': w, 'token_logps': [-1.0 - i], 'sequence_logp': -1.0 - i} for i, w in enumerate(ACTIONS_M867)]}
    keep = _c889.deepcopy(rd); sm = summary_m888(rd)
    r['audit_summary_does_not_change_reading'] = rd == keep and sm['action'] == rd['action'] and \
        [sm['first_logp'][w] for w in ACTIONS_M867] == [s['token_logps'][0] for s in rd['scores']]
    # recovery
    E = lambda steps, arm='D_TRUE': {'arm': arm, 'episode_id': 'e', 'steps': steps}
    S = lambda t, kind, a, eff, el=True: {'step': t, 'hop_kind': kind, 'action': a, 'effect': None if eff is None else {'effect': eff}, 'eligible_read': el}
    rc = recovery889([E([S(3, 'UNKNOWN', 'BACKTRACK', 'POINTER_RETRACTED'), S(4, 'NODE', 'ADVANCE', 'POINTER_ADVANCED')])])['D_TRUE']
    r['recovery_backtrack_with_followup'] = rc == {'events': 1, 'recoveries': 1, 'non_recovery': []}
    cases = {'stop': [S(3, 'UNKNOWN', 'STOP', None)], 'accept': [S(3, 'UNKNOWN', 'ACCEPT', None)],
             'advance': [S(3, 'UNKNOWN', 'ADVANCE', 'POINTER_ADVANCED'), S(4, 'NODE', 'STOP', None)],
             'no_effect': [S(3, 'UNKNOWN', 'ACQUIRE', 'NO_EFFECT_BANK_EXHAUSTED'), S(4, 'NODE', 'STOP', None)],
             'no_followup': [S(6, 'UNKNOWN', 'ACQUIRE', 'MOUNTED')],
             'followup_unknown': [S(3, 'UNKNOWN', 'REJECT', 'UNMOUNTED'), S(4, 'UNKNOWN', 'STOP', None)]}
    for nm, steps in cases.items():
        x = recovery889([E(steps)])['D_TRUE']; r['recovery_%s_not_recovery' % nm] = x['events'] >= 1 and x['recoveries'] == 0
    r['recovery_needs_eligible_read'] = recovery889([E([S(2, 'UNKNOWN', 'BACKTRACK', 'POINTER_RETRACTED', False), S(3, 'NODE', 'STOP', None)])])['D_TRUE']['events'] == 0
    # verdict
    phys = {'reads_true': 8, 'reads_wrong': 8, 'no_physical_failure': True, 'negatives_refused': True, 'post_run_integrity': True, 'cleanup_clean': True}
    def P(w, t, tv, at, aw, cls='NOVEL', sb=0.2, cond='FORK'):
        return {'world': w, 'condition': cond, 'step': t, 'tv_true_wrong': tv, 'tv_true_none': 0.3, 'a_true': at, 'a_wrong': aw,
                'tv_sham_blind': sb, 'a_true_sham': at, 'a_true_blind': at, 'overlap': {'class': cls, 'prior_appraisal_repeat': False},
                'unique_key': '%s%s%d%s' % (w, cond, t, at)}
    def Yf(tf, nf, wf, tm=1, nm=1, wm=1):
        m = {('D_TRUE', 'FORK'): tf, ('NONE', 'FORK'): nf, ('D_WRONG', 'FORK'): wf, ('D_TRUE', 'MISSING'): tm, ('NONE', 'MISSING'): nm, ('D_WRONG', 'MISSING'): wm}
        return {'%s_%s_%s' % (a, w, c): {'Y': m[(a, c)]} for (w, c) in CELLS_M867 for a in ARMS889}
    U = [P('10', 3, 0.3, 'ACQUIRE', 'ADVANCE'), P('10', 4, 0.01, 'STOP', 'STOP'), P('09', 3, 0.2, 'BACKTRACK', 'BACKTRACK'), P('09', 4, 0.0, 'A', 'A')]
    REC = {'D_TRUE': {'events': 1, 'recoveries': 1}}; CL = [{'ok': True}]; MR = {'10': 1, '09': 1}
    v = verdict889('COMPLETE', phys, U, Yf(1, 0, 0), REC, CL, MR)
    r['verdict_all_pass'] = v['OVERALL'] == 'PASS'
    r['verdict_partial_09_gain_fail'] = verdict889('COMPLETE', phys, U, dict(Yf(1, 0, 0), D_TRUE_10_FORK={'Y': 0}), REC, CL, MR)['OUTCOME_BENEFIT'] == 'FAIL'
    r['verdict_wrong_also_gains_fail'] = verdict889('COMPLETE', phys, U, Yf(1, 0, 1), REC, CL, MR)['OUTCOME_BENEFIT'] == 'FAIL'
    r['verdict_missing_zero_reads_not_pass'] = verdict889('COMPLETE', phys, U, Yf(1, 0, 0), REC, CL, {'10': 1, '09': 0})['OUTCOME_BENEFIT'] == 'NOT_MEASURED'
    r['verdict_missing_harm_fail'] = verdict889('COMPLETE', phys, U, Yf(1, 0, 0, tm=0), REC, CL, MR)['OUTCOME_BENEFIT'] == 'FAIL'
    v = verdict889('TECHNICAL_BLOCK', phys, U, Yf(1, 0, 0), REC, CL, MR)
    r['verdict_block_never_pass'] = v['OVERALL'] == 'TECHNICAL_BLOCK' and 'PASS' not in [v[k] for k in ('APPRAISAL_CHANNEL', 'CONTENT_EFFECT', 'OUTCOME_BENEFIT', 'NATIVE_RECOVERY')]
    v = verdict889('BUDGET_STOP', phys, U, Yf(1, 0, 0), REC, CL, MR); r['verdict_budget_never_pass'] = v['OVERALL'] == 'BUDGET_STOP'
    r['verdict_provenance_fail_overall_fail'] = verdict889('COMPLETE', phys, U, Yf(1, 0, 0), REC, [{'ok': False}], MR)['OVERALL'] == 'FAIL'
    v = verdict889('COMPLETE', phys, [dict(p, tv_sham_blind=0.0) for p in U], Yf(1, 0, 0), REC, CL, MR)
    r['verdict_no_channel_fail'] = v['APPRAISAL_CHANNEL'] == 'FAIL' and v['OVERALL'] == 'FAIL'
    v = verdict889('COMPLETE', phys, [dict(p, overlap={'class': 'CURRENT_V_ROW_ECHO', 'prior_appraisal_repeat': False}) for p in U], Yf(1, 0, 0), REC, CL, MR)
    r['verdict_all_echo_nonredundancy_fail'] = v['APPRAISAL_NONREDUNDANCY'] == 'FAIL'
    v = verdict889('COMPLETE', phys, [dict(p, overlap={'class': 'CURRENT_V_TEXT_REPEAT', 'prior_appraisal_repeat': True}) for p in U], Yf(1, 0, 0), REC, CL, MR)
    r['verdict_text_repeats_inconclusive'] = v['APPRAISAL_NONREDUNDANCY'] == 'INCONCLUSIVE'
    v = verdict889('COMPLETE', phys, [dict(p, tv_true_wrong=0.0, a_wrong=p['a_true']) for p in U], Yf(1, 0, 0), REC, CL, MR)
    r['verdict_presence_only_content_fail'] = v['CONTENT_EFFECT'] == 'FAIL' and v['presence_only_points'] == 4
    r['verdict_recovery_fail'] = verdict889('COMPLETE', phys, U, Yf(1, 0, 0), {'D_TRUE': {'events': 2, 'recoveries': 1}}, CL, MR)['NATIVE_RECOVERY'] == 'FAIL'
    r['verdict_recovery_not_measured'] = verdict889('COMPLETE', phys, U, Yf(1, 0, 0), {'D_TRUE': {'events': 0}}, CL, MR)['NATIVE_RECOVERY'] == 'NOT_MEASURED'
    v = verdict889('COMPLETE', phys, U + [dict(U[0])], Yf(1, 0, 0), REC, CL, MR)
    r['verdict_raw_and_unique_kept'] = v['reasons']['points']['raw'] == 5 and v['reasons']['points']['unique'] == 4
    r['verdict_empty_points'] = verdict889('COMPLETE', phys, [], Yf(0, 0, 0), {}, [], MR)['CONTENT_EFFECT'] == 'NOT_MEASURED'
    # budget / admission constants and the empty-history rule
    r['admission_empty_history_refused'] = cell_admission883(0.0, [], [], 1) == (False, None)
    r['budget_constants'] = (WALL_S883, SAFETY883, OFFLINE_RESERVE_S883, FREE_MIN_GIB883, HORIZON883, CALL_ALLOWANCE865) == (4500, 1.25, 180, 6.0, 6, 3000) \
        if 'CALL_ALLOWANCE865' in globals() else 'NOT_RUN_ENGINE_CONSTANT'
    r['firewall_executor_refused'] = False
    try: scan883(_a889.parse('def f(e):\n    execute866(e, 1, 2, 3, 4, 5)\n').body[0])
    except AssertionError: r['firewall_executor_refused'] = True
    r['prereg_sha_stable'] = PREREG_SHA889 == _h889.sha256(_j889.dumps(PREREG889, sort_keys=True, default=str).encode()).hexdigest()
    return r


# ============================ single cell execution ============================
T_START878 = T_START883 = T_CELL889
ORACLE_VAULT883 = None; OFFLINE_DIGEST_G1_885 = None; VAULT_FP885 = None
try:
    STATE889['status'] = 'G0'; capture889()
    json_write864('TEST889_prereg.json', {'prereg': PREREG889, 'sha256': PREREG_SHA889, 'written_before_model_load': True})
    load_sources865(); select_locked883()
    du = _s889.disk_usage(str(ROOT864))
    if du.free / 2**30 < 5.0: raise Gate_m867('DISK_FREE %.1f GiB' % (du.free / 2**30))
    STATE883['write_probe'] = write_probe883(ROOT864)
    if not all(STATE883['write_probe'].values()): raise Gate_m867('WRITE_PROBE %s' % STATE883['write_probe'])
    source_audit878(); load878(); run_selftests883()               # the 885 CPU selftests, unchanged
    STATE889['selftest'] = {'887': st_m867(), '888': st_m888(), '889': st889()}
    json_write864('TEST889_cpu_selftest.json', STATE889['selftest'])
    bad_ = sorted('%s/%s' % (g_, k) for g_, d_ in STATE889['selftest'].items() for k, v in d_.items()
                  if not (v is True or v in ('NOT_RUN_NO_TORCH', 'NOT_RUN_ENGINE_CONSTANT')))
    if bad_: raise Gate_m867('CPU_SELFTEST %s' % bad_)
    STATE883['live_scan'] = live_path_scan883([ENGINE883['body']] + [RAW_SOURCES864[n].decode() for n in ('873.py', '878.py', '881.py')])
    if not STATE883['live_scan']['ok']: raise Gate_m867('LIVE_PATH_ORACLE_SCAN %s' % STATE883['live_scan'])
    feasibility_audit864(); audit_contracts865(); load_spine864()
    if not (CC_GPU_OK and 'A100' in str(CC_GPU.get('name')) and CC_GPU.get('total_gib', 0) >= 78.0): raise Gate_m867('A100_80GB_REQUIRED %s' % CC_GPU)
    gate889('G0', 'PASS', selftests_885=sorted(STATE883['selftests']), selftests={g_: len(d_) for g_, d_ in STATE889['selftest'].items()},
            prereg_sha256=PREREG_SHA889, disk_free_gib=round(du.free / 2**30, 1))
    STATE889['status'] = 'G1'                                       # model + native backbone: the 885/887/888 G1 chain, unchanged calls
    env883, original_error883, original_trace883, reproduction883 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace883; TWO_JOB_VERIFICATION864 = verify_two_job859(env883, original_trace883)
    assert_hook_free859(env883, 'T889_before_native'); OFFLINE_DIGEST_G1_885 = install_offline_evaluator859(env883)
    if OFFLINE_DIGEST_G1_885 != EVAL_DIGEST885: raise Gate_m867('EVALUATOR_DIGEST_G1 %s' % OFFLINE_DIGEST_G1_885)
    native883 = native_sequences860(env883); NATIVE_REGRESSION864 = native_regression864(env883, native883)
    verify_864_reference865(NATIVE_REGRESSION864); ANALYSIS864 = run_analysis863(env883, native883)
    assert len(STATE863['restores']) == 3 and all(r_['exact'] for r_ in STATE863['restores'])
    digest883 = records_digest861(env883); null_seal883 = physical_seal863(env883, env883['MEMNULL841'])
    runtime_contracts865(env883); runtime_preflight865(env883, reproduction883); make_slots866(env883)
    SLOTS867['PREV_EVALUATION'] = list(env883['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env883); resolve_append873(env883); api877(env883); WEIGHTS0_878 = weights_digest877(env883)
    chunk883 = [ns['CHUNK'] for ns in (env883['build_fusion'].__globals__, env883) if 'CHUNK' in ns]
    assert chunk883 and int(chunk883[0]) > 0 and all(k in env883 for k in (
        'P', 'to_gpu', 'entries', 'make_x851', 'gen851', 'gen849', 'C_SLOT851', 'E_SLOT851', 'REVIEW_SUFFIX851', 'stats849',
        'MUE845', 'MEMNULL841', 'relation852', 'R_SLOT852', 'QTEXT841') + ORACLE_ENV_KEYS883), 'ENGINE_NAMESPACE'
    EXP878['CHUNK'] = int(chunk883[0])
    if tuple(w_ for w_, _ in ACTION_IDS867) != ACTIONS_M867: raise Gate_m867('NATIVE_VOCABULARY %s' % [w_ for w_, _ in ACTION_IDS867])
    if not SLOTS866.get('EVALUATION'): raise Gate_m867('EVALUATION_SLOT_MISSING')
    assert not any(p_.requires_grad for p_ in env883['model'].parameters()), 'NOT_FROZEN'
    assert_hook_free859(env883, 'T889_before_points')
    STATE883['model_contract'] = model_contract883(env883, CC_GPU)
    if not STATE883['model_contract']['ok']: raise Gate_m867('MODEL_CONTRACT %s' % STATE883['model_contract']['checks'])
    if _o889.path.exists(CART_ROOT883): _s889.rmtree(CART_ROOT883)
    _o889.makedirs(CART_ROOT883); EXP_DIR878 = type(ROOT864)(CART_ROOT883)
    gate889('G1', 'PASS', chunk=EXP878['CHUNK'], P=int(env883['P']), model_contract=STATE883['model_contract']['checks'],
            bank_digest=digest883, weights_digest=WEIGHTS0_878, evaluation_slot_tokens=len(SLOTS866['EVALUATION']))
    by_key883 = build_specs869(env883)
    ORACLE_VAULT883 = seal_oracle883(env883); VAULT_FP885 = vault_fingerprint885(ORACLE_VAULT883)   # live work without oracle keys
    STATE889['status'] = 'RUN'
    assert CALL_ALLOWANCE865 == 3000, ('CALL_ALLOWANCE865', CALL_ALLOWANCE865)
    now_ = _t889.perf_counter(); plan_ = g2_budget_plan883(now_, T_START883, WALL_S883)
    if plan_ is None: raise Budget883('NO_TIME_LEFT_AFTER_G1')
    T0_865 = plan_['T0_865']; TEST865_MINUTES = plan_['TEST865_MINUTES']
    rearm_budget865(env883)                                         # +30 min engine margin; the 75 min wall is guard883 / admit883
    if budget_left865(env883, STEP_CALLS867) is not True: raise Budget883('RESOURCE_BUDGET_AT_RUN_START')
    plan889 = [('NONE', w_, c_) for (w_, c_) in CELLS_M867] + [(a_, w_, c_) for (w_, c_) in CELLS_M867 for a_ in ('D_TRUE', 'D_WRONG')]
    ledger889 = {}
    for i_, (a_, w_, c_) in enumerate(plan889):
        if i_: admit883('E%02d_%s_%s_%s' % (i_, a_, w_, c_), len(plan889) - i_)
        try:
            ep_ = episode889(env883, by_key883[(int(w_), c_)], a_, '%s_%s_%s' % (a_, w_, c_), HORIZON883,
                             None if a_ == 'NONE' else ledger889.get((DONOR_M867[w_], c_)))
        except Gate883 as exc_:                   # a missing exact-step donor blocks this episode only; the run stays TECHNICAL_BLOCK
            if 'NO_EXACT_POST_STEP_DONOR' in str(exc_) and not str(exc_).startswith('PHYSICAL_'):
                STATE889['blocked_episodes'].append({'episode': '%s_%s_%s' % (a_, w_, c_), 'reason': str(exc_)[:400]}); continue
            raise
        if a_ == 'NONE': ledger889[(w_, c_)] = ep_['vledger']
        ep_['vledger'] = len(ep_['vledger'])                        # rows stay in ledger889 only
    STATE889['status'] = 'POST'
    STATE889['post_run'] = {'bank_digest_unchanged': records_digest861(env883) == digest883,
                            'memnull_seal_unchanged': physical_seal863(env883, env883['MEMNULL841']) == null_seal883,
                            'weights_unchanged': weights_digest877(env883) == WEIGHTS0_878,
                            'hooks_zero': hook_audit859(env883, 'T889_final')['hook_count'] == 0,
                            'model_contract_ok': model_contract883(env883, CC_GPU)['ok']}
    if not all(STATE889['post_run'].values()): raise Gate883('PHYSICAL_POST_RUN_INTEGRITY %s' % STATE889['post_run'])
    oenv889, ev889 = evaluator_env885(env883, ORACLE_VAULT883, OFFLINE_DIGEST_G1_885, VAULT_FP885)
    STATE889['scores'] = episode_scores885(oenv889, by_key883, STATE889['episodes']); STATE889['evaluator'] = ev889
    del oenv889
    STATE889['technical_status'] = 'TECHNICAL_BLOCK' if STATE889['blocked_episodes'] else 'COMPLETE'
    if STATE889['blocked_episodes']: STATE889['error'] = 'NO_EXACT_POST_STEP_DONOR in %d episode(s)' % len(STATE889['blocked_episodes'])
except Budget883 as exc:
    STATE889['technical_status'] = 'BUDGET_STOP'; STATE889['error'] = str(exc)
except BaseException as exc:
    STATE889['technical_status'] = 'INTERRUPTED' if isinstance(exc, (KeyboardInterrupt, SystemExit)) else 'TECHNICAL_BLOCK'
    STATE889['error'] = '%s: %s' % (type(exc).__name__, exc); STATE889['traceback'] = traceback.format_exc()
    if str(exc).startswith('PHYSICAL_') and not STATE889['physical_failure']: STATE889['physical_failure'] = str(exc)[:500]
    print('TEST889 ERROR at', STATE889['status'], STATE889['error'][:400], file=ERROR_CONSOLE864, flush=True)
    print(STATE889['traceback'], file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        if _o889.path.exists(CART_ROOT883):
            left_ = sorted(_o889.listdir(CART_ROOT883)); _s889.rmtree(CART_ROOT883)
            if left_: STATE883['cleanup_errors'].append({'episode_id': 'CART_ROOT', 'errors': ['LEFTOVER %s' % left_[:20]]})
    except BaseException as exc: STATE883['cleanup_errors'].append({'episode_id': 'CART_ROOT', 'errors': ['%s: %s' % (type(exc).__name__, exc)]})
    if STATE889['post_run'] is None and isinstance(globals().get('env883'), dict) and 'digest883' in globals():
        try:
            STATE889['post_run'] = {'bank_digest_unchanged': records_digest861(env883) == digest883,
                                    'memnull_seal_unchanged': physical_seal863(env883, env883['MEMNULL841']) == null_seal883,
                                    'weights_unchanged': weights_digest877(env883) == WEIGHTS0_878,
                                    'hooks_zero': hook_audit859(env883, 'T889_final')['hook_count'] == 0,
                                    'model_contract_ok': model_contract883(env883, CC_GPU)['ok'], 'computed_in': 'finally'}
        except BaseException as exc:
            STATE889['post_run'] = {'error': '%s: %s' % (type(exc).__name__, exc)}
    pts_, eps_ = STATE889['points'], STATE889['episodes']
    phys_ = {'reads_true': len(pts_), 'reads_wrong': len(pts_), 'physical_failure': STATE889['physical_failure'],
             'no_physical_failure': STATE889['physical_failure'] is None,
             'negatives_refused': None if STATE889['negatives'] is None else all(STATE889['negatives'].values()),
             'post_run_integrity': None if STATE889['post_run'] is None else all(v is True for k, v in STATE889['post_run'].items()
                                                                                  if k != 'computed_in') and 'error' not in STATE889['post_run'],
             'cleanup_clean': not STATE883['cleanup_errors']}
    mreads_ = {w_: sum(1 for p_ in pts_ if p_['world'] == w_ and p_['condition'] == 'MISSING' and p_['arm'] == 'D_TRUE') for w_ in WORLDS_M867}
    try:
        STATE889['verdict'] = verdict889(STATE889['technical_status'] or 'TECHNICAL_BLOCK', phys_, pts_, STATE889['scores'],
                                         recovery889(eps_), STATE889['closures'], mreads_)
    except BaseException as exc:
        STATE889['verdict'] = {'TECHNICAL_STATUS': 'TECHNICAL_BLOCK', 'PHYSICAL_READ': 'FAIL', 'OVERALL': 'TECHNICAL_BLOCK',
                               'reasons': {'verdict_error': '%s: %s' % (type(exc).__name__, exc)}}
    U_ = unique_m888(pts_)
    report889 = {
        'test': 'TEST889', 'verdict': STATE889['verdict'], 'physical_facts': phys_, 'error': STATE889['error'],
        'blocked_episodes': STATE889['blocked_episodes'],
        'hashes': {'executed_cell': STATE889['source'], 'base888': B888_INFO889, 'base887': B887_INFO_M888, 'base885': BASE_INFO_M867,
                   'engine': ENGINE_INFO883, 'prereg_sha256': PREREG_SHA889, 'head_locks': HEAD883,
                   'weights_digest': globals().get('WEIGHTS0_878'), 'bank_digest': globals().get('digest883')},
        'gates': STATE889['gates'], 'negatives': STATE889['negatives'], 'post_run': STATE889['post_run'],
        'counters': {'episodes': len(eps_), 'steps': sum(e_['n_steps'] for e_ in eps_ if e_.get('n_steps') is not None),
                     'points_raw': len(pts_), 'points_unique': len(U_), 'closures': len(STATE889['closures']),
                     'cartridges': sum(len(e_['cartridges']) + len(e_['wrong_cartridges']) for e_ in eps_),
                     'ssd_bytes': sum(int(c_.get('bytes') or 0) for e_ in eps_ for c_ in e_['cartridges'] + e_['wrong_cartridges']),
                     'open_pending_at_end': {e_['episode_id']: e_.get('open_pending_at_end') for e_ in eps_ if e_['arm'] != 'NONE'},
                     'missing_d_true_reads': mreads_,
                     'calls849': globals().get('env883', {}).get('CALLS849') if isinstance(globals().get('env883'), dict) else None,
                     'wall_s': round(_t889.perf_counter() - T_CELL889, 1), 'peak_alloc_gib': STATE883['budget'].get('peak_alloc_gib')},
        'cells': {'%s_%s' % (w_, c_): {a_: next(({'end': e_['end'], 'actions': e_['actions'], 'effects': e_['effects'],
                                                 'accepted': e_['accepted'], 'final_mounted': e_['final_mounted'],
                                                 'Y': (STATE889['scores'] or {}).get(e_['episode_id'], {}).get('Y')}
                                                for e_ in eps_ if e_['episode_id'] == '%s_%s_%s' % (a_, w_, c_)), None)
                                         for a_ in ARMS889} for (w_, c_) in CELLS_M867},
        'points_unique': [{k_: p_[k_] for k_ in ('episode_id', 'step', 'step_written', 'post_appraisal_step', 'a_none', 'a_true', 'a_wrong',
                                                 'a_true_sham', 'a_true_blind', 'tv_true_wrong', 'tv_true_none', 'tv_sham_blind', 'tv_full_sham_kernel',
                                                 'overlap', 'donor_fit', 'v_rows_differ', 'body_tokens', 'none', 'true_full', 'wrong_full',
                                                 'true_sham', 'true_blind', 'unique_key')} for p_ in U_],
        'closures': STATE889['closures'], 'cleanup_errors': STATE883['cleanup_errors'], 'evaluator': STATE889.get('evaluator'),
        'known_limits': PREREG889['known_limits'], 'not_claimed': PREREG889['not_claimed'],
        'gpu_note': 'GPU_NOT_RUN_BY_AUTHOR (cell author); GPU_RUN_THIS_TEST if this is a Colab console'}
    try:
        if STATE889['traceback']: (ROOT864 / 'TEST889_traceback.txt').write_text(STATE889['traceback'], encoding='utf-8')
        json_write864('TEST889_final_report.json', jsafe878(report889))
        p_ = ROOT864 / 'TEST889_final_report.json'
        if _j889.loads(p_.read_text(encoding='utf-8'))['verdict']['TECHNICAL_STATUS'] != STATE889['verdict']['TECHNICAL_STATUS']:
            raise OSError('READ_BACK_MISMATCH')
        STATE889['report_sha256'] = sha256_bytes864(p_.read_bytes())
    except BaseException as exc:
        STATE889['artifact_errors'].append('%s: %s' % (type(exc).__name__, exc))
        STATE889['verdict'] = dict(STATE889['verdict'], TECHNICAL_STATUS='ARTIFACT_FAILURE', OVERALL='ARTIFACT_FAILURE')
    v_ = STATE889['verdict']; K_ = ('TECHNICAL_STATUS', 'PHYSICAL_READ', 'APPRAISAL_PROVENANCE', 'APPRAISAL_NONREDUNDANCY', 'APPRAISAL_CHANNEL',
                                    'CONTENT_EFFECT', 'OUTCOME_BENEFIT', 'NATIVE_RECOVERY', 'OVERALL')
    print('=' * 110)
    print('TEST889 | %s' % ' | '.join('%s=%s' % (k_, v_.get(k_)) for k_ in K_))
    print('OUTCOME_PARTIAL=%s | presence_points=%s | presence_only=%s | blocked=%s' % (v_.get('OUTCOME_PARTIAL'), v_.get('presence_points'),
                                                                                   v_.get('presence_only_points'), STATE889['blocked_episodes']))
    for p_ in U_:
        print('POINT %-18s t=%d E%d %-21s NONE=%-9s TRUE=%-9s WRONG=%-9s SHAM/BLIND=%s/%s TV(T,W)=%.3f TV(T,N)=%.3f TV(S,B)=%.4f fit=%s/%s+%s' % (
            p_['episode_id'], p_['step'], p_['step_written'], p_['overlap']['class'], p_['a_none'], p_['a_true'], p_['a_wrong'],
            p_['a_true_sham'], p_['a_true_blind'], p_['tv_true_wrong'], p_['tv_true_none'], p_['tv_sham_blind'],
            p_['donor_fit']['donor_rows'], p_['donor_fit']['true_rows'], p_['donor_fit']['padded_mue']))
        for nm_ in ('none', 'true_full', 'wrong_full', 'true_blind'):
            print('      p(%-10s)=%s margin=%.3f' % (nm_, {k_: round(x_, 3) for k_, x_ in p_[nm_]['p'].items()}, p_[nm_]['margin_logp']))
    for k_, c_ in report889['cells'].items():
        print('CELL %-11s' % k_, ' | '.join('%s:%s Y=%s' % (a_, '>'.join((c_[a_] or {}).get('actions') or []), (c_[a_] or {}).get('Y')) for a_ in ARMS889))
    print('reasons', _j889.dumps(v_.get('reasons'), default=str)[:1800])
    print('error', STATE889['error'], '| artifact_errors', STATE889['artifact_errors'], '| report sha256', STATE889.get('report_sha256'))
    print('=' * 110, flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE883['suffix'], 'test870.py:suffix', 'exec'), globals())     # ZIP + SHA256SUMS + testzip + Drive copy (locked I/O)
try:                                                                          # delivery receipt beside the ZIP (outside it)
    import zipfile as _z889
    with _z889.ZipFile(CC_ZIP) as _zz: _zip_ok = _zz.testzip() is None
    _zsha = _h889.sha256(CC_ZIP.read_bytes()).hexdigest()
    _rc = {'zip': str(CC_ZIP), 'zip_sha256': _zsha, 'zip_testzip_ok': _zip_ok, 'verdict': {k_: STATE889['verdict'].get(k_) for k_ in K_},
           'drive_dir': CC_DRIVE_DIR, 'drive_zip_sha256_equal': None}
    if CC_DRIVE_DIR is not None:
        _dz = _o889.path.join(CC_DRIVE_DIR, _o889.path.basename(str(CC_ZIP)))
        _rc['drive_zip_sha256_equal'] = _o889.path.exists(_dz) and _h889.sha256(open(_dz, 'rb').read()).hexdigest() == _zsha
    _rp = str(CC_ZIP).replace('.zip', '_RECEIPT.json')
    with open(_rp, 'w', encoding='utf-8') as _f: _f.write(_j889.dumps(_rc, sort_keys=True, default=str, indent=1))
    if CC_DRIVE_DIR is not None: _s889.copy2(_rp, CC_DRIVE_DIR)
    print('TEST889 RECEIPT', _j889.dumps(_rc, sort_keys=True, default=str)[:600])
    if not _zip_ok or _rc['drive_zip_sha256_equal'] is False: print('TEST889 ARTIFACT_INCOMPLETE: ZIP or Drive copy not verified')
except BaseException as _exc:
    print('TEST889 ARTIFACT_INCOMPLETE: receipt failed', type(_exc).__name__, _exc)
