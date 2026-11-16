# TEST888 BODY-SHA256 3fb77095546f40bd41ed6b7ead8f9a4b9fb5f0c3dfefb25241ec43d29bdb5ca5
# AKBASCORE SILICON HIPPOCAMPUS — TEST888 — DEFERRED TRANSITION CARTRIDGE (one Colab cell, one Run, A100-SXM4-80GB)
# Question: if the native CAR decision at step t reads the physical CUT3/H3/KV transition cartridge of an EARLIER step,
#   E_(t-3) = [X2_(t-3)][A_(t-3)][O_(t-2)]  (the model's own past state, its own executed action, the observation that followed)
# instead of the immediately preceding one (887/TEST867: E_(t-1) whose C = O_t is also inside X_t), does its CONTENT change the
# next native action, does that improve the physical outcome, and does the model recover after UNKNOWN hops?
# REUSE, NOT REWRITE: the definitions of '887 (1).py' (= TEST867, Colab A100 2026-11-15: COMPLETE, PHYSICAL_READ PASS) are
# downloaded from an exact commit, checked against git blob + SHA-256 and executed unchanged; they in turn download 885.py
# (blob 51900159), the locked engine test870.py (e322ed8e / de3c8153) and the locks at 3d75f289. Reused unchanged: the 887
# writer (write_pair_m867: TRUE / WRONG cartridges of every nonterminal step, donor rule), reader (read_m867), NONE parity
# (none_m867), corruption negatives, finite / TV, the 887 + 885 CPU selftests, the 885 cleanup / contract / evaluator.
# NEW here (only): the fixed delay queue (DELAY=3, sealed, never tuned), the deferred read with a separate fail-closed delay
# check, IMMEDIATE and C-blind controls (measured, never executed), a row-origin / text overlap measure, unique-state dedupe,
# raw six-action summaries, the recovery observation and a sealed six-field verdict.
# No training, LoRA, optimizer, backward, RAG, text replay, hooks, hidden states, router, forced action, answer fixing.
# GPU_NOT_RUN_BY_AUTHOR.
import time as _t888
T_CELL_M888 = _t888.perf_counter()                     # the single 75-minute clock starts here (before any download)
import ast as _a888, hashlib as _h888, json as _j888, os as _o888, re as _r888, urllib.request as _u888, shutil as _s888
B887_URL_M888 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 '3a3bcbd73278e6ed96eeccae9eb1b9865c30c5ce/887%20%281%29.py')
B887_BLOB_M888 = '4e3cc41a03a930c17e926e09ce1cdb580e205d2d'
B887_SHA_M888 = 'ce4a0052b2af73cafe68ccdd1a91b34327f2ccc351ca770aa639669bb9d44087'
B887_CUT_M888 = '\n# ============================ single cell execution ============================\n'
B887_RENAMES_M888 = (('"TEST867_HUCRE_CIKTISI"', '"TEST888_HUCRE_CIKTISI"', 1), ('"MyDrive/TEST867_"', '"MyDrive/TEST888_"', 1),
                     ('"TEST867_RUN_"', '"TEST888_RUN_"', 1), ('"867_engine.log"', '"888_engine.log"', 1),
                     ('"867_events.jsonl"', '"888_events.jsonl"', 1), ('"TEST867_SONUC_"', '"TEST888_SONUC_"', 1),
                     ('"print(\'TEST867 ENGINE\'"', '"print(\'TEST888 ENGINE\'"', 1), ("print('TEST867 BASE'", "print('TEST888 BASE885'", 1),
                     ("'/content/TEST867_EPISODE_CARTRIDGES'", "'/content/TEST888_EPISODE_CARTRIDGES'", 1),
                     ("'/content/TEST867_PRE_BASE_ERROR_%s.txt'", "'/content/TEST888_PRE_BASE_ERROR_%s.txt'", 1))


def defs887_m888(raw):
    # '887 (1).py' bytes -> its definition part (everything before its main block); output names renamed (I/O strings only)
    blob = _h888.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()
    assert blob == B887_BLOB_M888 and _h888.sha256(raw).hexdigest() == B887_SHA_M888, ('BASE_887_LOCK', blob)
    text = raw.decode('utf-8')
    assert text.count(B887_CUT_M888) == 1, 'BASE_887_CUT'
    defs = text[:text.index(B887_CUT_M888) + 1]
    for old, new, n in B887_RENAMES_M888:
        assert defs.count(old) == n, ('BASE_887_RENAME', old, defs.count(old))
        defs = defs.replace(old, new)
    _a888.parse(defs)
    return defs, {'url': B887_URL_M888, 'git_blob': blob, 'sha256': B887_SHA_M888, 'definition_lines': defs.count('\n')}


try:
    with _u888.urlopen(_u888.Request(B887_URL_M888, headers={'User-Agent': 'AKBASCORE-TEST888'}), timeout=240) as _r:
        B887_M888, B887_INFO_M888 = defs887_m888(_r.read())
except BaseException as _exc888:
    import traceback as _tb888
    _p888 = '/content/TEST888_PRE_BASE_ERROR_%s.txt' % _t888.strftime('%Y%m%dT%H%M%SZ', _t888.gmtime())
    try:
        with open(_p888, 'w', encoding='utf-8') as _f888: _f888.write(_tb888.format_exc())
    except OSError: _p888 = 'NOT_WRITTEN'
    print('TEST888 PRE-BASE ERROR (nothing loaded):', type(_exc888).__name__, _exc888, '| traceback:', _p888)
    raise
exec(compile(B887_M888, '887 (1).py:definitions', 'exec'), globals())   # 885 + engine + console capture + 887 definitions
print('TEST888 BASE887', _j888.dumps(B887_INFO_M888, sort_keys=True))

# ============================ sealed design (fixed before the model is loaded) ============================
DELAY_M888 = 3                     # decision t reads E_(t-3) (step_written = t-3, written at step t-2, C = O_(t-2)); never tuned
ARMS_M888 = ('NONE', 'D_TRUE', 'D_WRONG')
NONRECOVERY_M888 = ('ADVANCE', 'ACCEPT')   # after an UNKNOWN hop: advancing onto / accepting 'UNKNOWN' (observation only)
EXEC_ALLOW_M888 = {'episode_m888': ('execute866', 'hop865', 'mount865')}
RUNTIME_NEW_M888 = ('summary_m888', 'rowset_m888', 'overlap_m888', 'read_blind_m888', 'episode_m888')
RUNTIME_887_M888 = ('tv_m867', 'finite_m867', 'none_m867', 'read_m867', 'write_pair_m867', 'negatives_m867')
PREREG_M888 = {
    'test': 'TEST888 deferred transition cartridge', 'base887': B887_INFO_M888, 'base885': BASE_INFO_M867, 'engine': ENGINE_INFO883,
    'head_locks': HEAD883, 'delay': DELAY_M888, 'cells': ['%s_%s' % c for c in CELLS_M867], 'arms_executed': ARMS_M888,
    'horizon': HORIZON883, 'tau_tv': TAU_M867, 'min_unique_points': MIN_PAIRS_M867, 'donor': DONOR_M867,
    'mechanism': 'every nonterminal step t-1 -> E_(t-1) TRUE (C = real O_t) and WRONG (C = other world, same step, shape_match867) '
                 'written to SSD by the unchanged 887 writer; decision t >= 4 reads E_(t-3) TRUE (D_TRUE arm) or WRONG (D_WRONG arm) '
                 'with read_m867 (xcar878 blind=()); t < 4 (no eligible cartridge): the native NONE reading (bitwise == native)',
    'delay_check': 'read_contract883 is called with the cartridge OWN contract step (step_written + 1); then separately and '
                   'fail-closed: decision_step - step_written == DELAY',
    'controls_measured_not_executed': 'at the first eligible decision of every D_TRUE episode: IMMEDIATE E_(t-1) TRUE / WRONG '
        '(the 887 interface), and D_TRUE / D_WRONG C-blind (xcar878 blind=[C span]); D_TRUE_CBLIND != D_WRONG_CBLIND bitwise '
        '-> TECHNICAL_BLOCK (information outside C); first eligible decision of every D episode: independent SSD reload of '
        'D_TRUE must be bitwise identical',
    'overlap': 'deferred TRUE C = O_(t-2) vs current X: ROW_ECHO = a row of its candidate / evidence rows is bitwise one of the '
               'current candidate / evidence / pointer rows; TEXT_REPEAT = same decoded hop text as the current hop or pointer, '
               'or same evidence text; else NOVEL. Points are never deleted',
    'dedupe': 'unique point = sha256(world, condition, step, X_sha256, mounted cards, B tokens, path texts, D_TRUE tensor_sha)',
    'verdict': {
        'PHYSICAL_READ': 'the 887 rule (verdict_m867): reads, gates, negatives, restore, isolation, post-run integrity',
        'NONREDUNDANCY': 'NOT_MEASURED: 0 unique eligible points. PASS: COMPLETE + PHYSICAL PASS, >= 4 unique points in both worlds '
                         'and every point NOVEL. FAIL: every point ROW_ECHO. Else INCONCLUSIVE',
        'CONTENT_EFFECT': 'on unique points, D_TRUE vs D_WRONG. NOT_MEASURED: 0 points. PASS (COMPLETE + PHYSICAL PASS, >= 4 points): '
                          'TV >= tau in both worlds and >= 1 argmax difference. FAIL: TV < tau everywhere and no argmax difference. '
                          'Else INCONCLUSIVE',
        'OUTCOME_BENEFIT': 'COMPLETE + PHYSICAL PASS + 12 binary Y: PASS iff both FORK cells Y_D_TRUE=1, Y_NONE=0, Y_D_WRONG=0 and '
                           'both MISSING cells Y_D_TRUE >= max(Y_NONE, Y_D_WRONG); else FAIL; OUTCOME_PARTIAL = FORK cells with that '
                           'gain (a partial gain is never called PASS); otherwise NOT_MEASURED',
        'RECOVERY': 'decisions t >= 4 after an UNKNOWN hop. NOT_MEASURED: D_TRUE has none. FAIL: D_TRUE chose ADVANCE / ACCEPT on '
                    'one of them. PASS: D_TRUE never did and NONE did at least once at t >= 4. Else INCONCLUSIVE (no contrast). '
                    'Requires COMPLETE + PHYSICAL PASS, else INCONCLUSIVE. Observation only: no action is ever changed',
        'descriptive': 'PRESENCE (TV(D_TRUE,NONE) >= tau points), ECHO_CONTRAST (TV(IMMEDIATE_TRUE,NONE) vs TV(D_TRUE,NONE)), '
                       'C_READ_CHANNEL (D_TRUE full vs C-blind), content on NOVEL points only, WRONG truncation / padding',
        'OVERALL': 'PASS iff all six PASS; TECHNICAL_STATUS != COMPLETE -> that status; any FAIL -> FAIL; else INCONCLUSIVE'},
    'expected_from_887_trajectories': 'D arms equal NONE for t < 4 (bitwise NONE parity), so MISSING cells that STOP at t = 3 '
                                      'give no eligible point (their outcome check is then vacuous); 10_FORK t = 4 is expected to '
                                      'be ROW_ECHO (pointer = candidate of the step-2 ADVANCE = C of E_1); the evidence rows are '
                                      'regenerated bitwise identically while no card is mounted (gen849 depends only on memory and '
                                      'question), so evidence ROW_ECHO is expected wherever no ACQUIRE happened between t-2 and t',
    'not_claimed': ['learning (persistent, predictive)', 'generalization beyond 2 worlds x 2 conditions', 'that any delay is '
                    'optimal', 'GPU success before the run'],
    'budget': '75 min from the first line of this cell: guard883 before every step and every read pair, admit883 before every '
              'episode after the first; a budget stop never yields PASS'}
PREREG_SHA_M888 = _h888.sha256(_j888.dumps(PREREG_M888, sort_keys=True, default=str).encode()).hexdigest()
STATE_M888 = {'status': 'NOT_STARTED', 'technical_status': None, 'gates': {}, 'source': {}, 'episodes': [], 'points': [],
              'controls': [], 'negatives': None, 'physical_failure': None, 'post_run': None, 'scores': None, 'verdict': None,
              'error': None, 'traceback': None, 'artifact_errors': []}


def gate_m888(name, status, **info):
    rec = dict(status=status, wall_s=round(_t888.perf_counter() - T_CELL_M888, 1), **info)
    STATE_M888['gates'][name] = rec
    print('T888 GATE', name, status, _j888.dumps(rec, sort_keys=True, default=str)[:900], flush=True)
    if status != 'PASS': raise Gate_m867('%s %s' % (name, status))


# ============================ pure functions (CPU-testable) ============================
def body_lock_m888(src):
    # the 887 paste-stable lock (canon_lines_m867), for a '# TEST888 BODY-SHA256 <hex>' first non-empty line
    if not isinstance(src, str): return {'ok': False, 'why': 'NO_SOURCE'}
    lines = canon_lines_m867(src)
    if not lines: return {'ok': False, 'why': 'EMPTY_SOURCE'}
    m = _r888.fullmatch(r'#\s*TEST888\s+BODY-SHA256\s+([0-9a-f]{64})', lines[0].strip())
    if not m: return {'ok': False, 'why': 'NO_LOCK_LINE_FIRST', 'first_line_repr': repr(src.lstrip()[:100])}
    got = _h888.sha256(('\n'.join(lines[1:]) + '\n').encode('utf-8')).hexdigest()
    return {'ok': got == m.group(1), 'why': None if got == m.group(1) else 'BODY_HASH_MISMATCH', 'expected': m.group(1),
            'measured': got, 'canonical_lines': len(lines) - 1}


def summary_m888(r):
    # raw six-action record of one native CAR reading (for the log; never fed back into a decision)
    return {'action': r['action'], 'p': {w: float(r['normalized'][w]) for w in ACTIONS_M867}, 'mass': float(r['mass']),
            'margin_logp': r.get('margin_logp'), 'first_logp': {s['word']: float(s['token_logps'][0]) for s in r['scores']},
            'seq_logp': {s['word']: float(s['sequence_logp']) for s in r['scores']}}


def rowset_m888(*tensors):
    out = set()
    for t in tensors:
        if t is None: continue
        try: a = t.detach().cpu().contiguous().numpy()
        except AttributeError: a = t                  # already an array (CPU tests)
        for row in a: out.add(_h888.sha256(row.tobytes()).hexdigest())
    return out


def overlap_m888(past, cur, pointer_rows, pointer_text):
    # past / cur: {'c', 'e', 'hop', 'evid'}; exact row origin first, then decoded text; never used to choose anything
    now = rowset_m888(cur['c'], cur['e'], pointer_rows)
    echo_c, echo_e = rowset_m888(past['c']) & now, rowset_m888(past['e']) & now
    hop_rep = (past['hop'] or '').strip() in {(cur['hop'] or '').strip(), (pointer_text or '').strip()}
    evid_rep = (past['evid'] or '').strip() == (cur['evid'] or '').strip()
    return {'row_echo_rows': len(echo_c | echo_e), 'candidate_row_echo': bool(echo_c), 'evidence_row_echo': bool(echo_e),
            'hop_text_repeat': hop_rep, 'evidence_text_repeat': evid_rep,
            'class': 'ROW_ECHO' if echo_c or echo_e else ('TEXT_REPEAT' if hop_rep or evid_rep else 'NOVEL'),
            'past_hop': (past['hop'] or '').strip(), 'cur_hop': (cur['hop'] or '').strip(), 'pointer': pointer_text}


def unique_m888(points):
    seen, out = set(), []
    for p in points:
        if p['unique_key'] not in seen: seen.add(p['unique_key']); out.append(p)
    return out


def verdict_m888(status, physical, points, scores, recovery, controls):
    v = {'TECHNICAL_STATUS': status, 'reasons': {}}
    v['PHYSICAL_READ'] = verdict_m867(status, physical, [], {})['PHYSICAL_READ']
    ok = status == 'COMPLETE' and v['PHYSICAL_READ'] == 'PASS'
    U = unique_m888(points); worlds = {p['world'] for p in U}
    cls = [p['overlap_true']['class'] for p in U]
    v['reasons']['points'] = {'raw': len(points), 'unique': len(U), 'worlds': sorted(worlds), 'classes': cls,
                              'candidate_row_echo': sum(1 for p in U if p['overlap_true'].get('candidate_row_echo')),
                              'evidence_row_echo': sum(1 for p in U if p['overlap_true'].get('evidence_row_echo'))}
    if not U: v['NONREDUNDANCY'] = 'NOT_MEASURED'
    elif not ok: v['NONREDUNDANCY'] = 'INCONCLUSIVE'
    elif all(c == 'ROW_ECHO' for c in cls): v['NONREDUNDANCY'] = 'FAIL'
    elif len(U) >= MIN_PAIRS_M867 and set(WORLDS_M867) <= worlds and all(c == 'NOVEL' for c in cls): v['NONREDUNDANCY'] = 'PASS'
    else: v['NONREDUNDANCY'] = 'INCONCLUSIVE'
    def content(P):
        eff = {p['world'] for p in P if p['tv_dt_dw'] >= TAU_M867}; diff = [p for p in P if p['a_dt'] != p['a_dw']]
        return eff, diff
    eff, diff = content(U)
    v['reasons']['content'] = {'worlds_tv_ge_tau': sorted(eff), 'argmax_differs': len(diff),
                               'max_tv_dt_dw': max((p['tv_dt_dw'] for p in U), default=None)}
    if not U: v['CONTENT_EFFECT'] = 'NOT_MEASURED'
    elif not ok or len(U) < MIN_PAIRS_M867: v['CONTENT_EFFECT'] = 'INCONCLUSIVE'
    elif set(WORLDS_M867) <= eff and diff: v['CONTENT_EFFECT'] = 'PASS'
    elif not eff and not diff: v['CONTENT_EFFECT'] = 'FAIL'
    else: v['CONTENT_EFFECT'] = 'INCONCLUSIVE'
    nov = [p for p in U if p['overlap_true']['class'] == 'NOVEL']; e2, d2 = content(nov)
    v['content_on_novel_points'] = {'points': len(nov), 'worlds_tv_ge_tau': sorted(e2), 'argmax_differs': len(d2)}
    v['presence_points'] = sum(1 for p in U if p['tv_dt_none'] >= TAU_M867)
    ec = [(c['tv_imm_true_none'], c['tv_dt_none']) for c in controls]
    v['echo_contrast'] = {'n': len(ec), 'pairs_imm_vs_deferred': ec,
                          'immediate_minus_deferred_median': (sorted(a - b for a, b in ec)[len(ec) // 2] if ec else None)}
    v['c_read_channel'] = None if not controls else ('PRESENT' if any(c['tv_full_cblind_true'] > 0 or c['a_full'] != c['a_cblind']
                                                                    for c in controls) else 'ABSENT')
    Y = {'%s_%s_%s' % (a, w, c): (scores or {}).get('%s_%s_%s' % (a, w, c), {}).get('Y') for (w, c) in CELLS_M867 for a in ARMS_M888}
    v['reasons']['Y'] = Y
    gain = [w for w in WORLDS_M867 if Y['D_TRUE_%s_FORK' % w] == 1 and Y['NONE_%s_FORK' % w] == 0 and Y['D_WRONG_%s_FORK' % w] == 0]
    v['OUTCOME_PARTIAL'] = '%d/2 FORK cells with a D_TRUE-specific gain' % len(gain) if all(y in (0, 1) for y in Y.values()) else None
    v['missing_cells_with_eligible_points'] = sorted({'%s_%s' % (p['world'], p['condition']) for p in U if p['condition'] == 'MISSING'})
    if not ok or any(y not in (0, 1) for y in Y.values()): v['OUTCOME_BENEFIT'] = 'NOT_MEASURED'
    else:
        miss = all(Y['D_TRUE_%s_MISSING' % w] >= max(Y['NONE_%s_MISSING' % w], Y['D_WRONG_%s_MISSING' % w]) for w in WORLDS_M867)
        v['OUTCOME_BENEFIT'] = 'PASS' if len(gain) == len(WORLDS_M867) and miss else 'FAIL'
    R = recovery or {}; dt, nn = R.get('D_TRUE', {}), R.get('NONE', {})
    v['reasons']['recovery'] = R
    if not ok: v['RECOVERY'] = 'INCONCLUSIVE'
    elif not dt.get('unknown_steps'): v['RECOVERY'] = 'NOT_MEASURED'
    elif dt.get('violations'): v['RECOVERY'] = 'FAIL'
    elif nn.get('violations'): v['RECOVERY'] = 'PASS'
    else: v['RECOVERY'] = 'INCONCLUSIVE'
    six = [v[k] for k in ('PHYSICAL_READ', 'NONREDUNDANCY', 'CONTENT_EFFECT', 'OUTCOME_BENEFIT', 'RECOVERY')]
    v['OVERALL'] = (status if status != 'COMPLETE' else 'PASS' if all(x == 'PASS' for x in six) else
                    'FAIL' if 'FAIL' in six else 'INCONCLUSIVE')
    return v


def recovery_m888(episodes):
    out = {a: {'unknown_steps': 0, 'violations': 0, 'where': []} for a in ARMS_M888}
    for e in episodes:
        for s in e.get('steps', []):
            if s['step'] >= DELAY_M888 + 1 and s.get('hop_kind') == 'UNKNOWN' and e['arm'] in out:
                out[e['arm']]['unknown_steps'] += 1
                if s['action'] in NONRECOVERY_M888:
                    out[e['arm']]['violations'] += 1; out[e['arm']]['where'].append('%s t%d %s' % (e['episode_id'], s['step'], s['action']))
    return out


# ============================ runtime (model) ============================
def read_blind_m888(env, B, entry, card, X, cstep, ep_id, cdir, b_tokens):
    # C-blind control on the same appended cartridge: X2 / A readable, the C span masked (locked xcar878 blind=[C], TEST883 CBLIND)
    why = read_contract883(entry, card, cstep, ep_id, cdir)
    if why: raise Gate883('PHYSICAL_READ_CONTRACT_CBLIND %s: %s' % (ep_id, why))
    n0 = length873(env, B)
    if n0 != b_tokens: raise Gate883('PHYSICAL_B_LENGTH %d != %d' % (n0, b_tokens))
    try:
        cp = load_exp878(env, entry)
    except Persist878 as exc:
        raise Gate883('PHYSICAL_RELOAD_CBLIND %s: %s' % (ep_id, exc))
    q = int(cp['body_tokens']); g = append_exp878(env, B, cp); ffe883(q, 80, 'experience_mount')
    sp = entry['provenance']['spans_body']; C = [n0 + int(sp['C'][0]), n0 + int(sp['C'][1])]
    ok = length873(env, g) == n0 + q and n0 <= C[0] < C[1] == n0 + q
    reading = xcar878(env, g, X, [C], False); ffe883(int(X.shape[0]) + cont_tokens881(), 80, 'decision_read')
    del g, cp
    if not ok or not finite_m867(reading): raise Gate883('PHYSICAL_CBLIND_READ_GATES %s %s' % (ep_id, entry['id']))
    return reading


def episode_m888(env, spec, arm, ep_id, horizon, donor_obs):
    # one natural episode; arm = NONE (native reading executed), D_TRUE or D_WRONG (from t >= DELAY+1 the deferred E_(t-DELAY)
    # reading is executed; before, the NONE reading). Every nonterminal step is still written as TRUE + WRONG cartridges.
    key = {'world_index': int(spec['world_index']), 'condition': spec['condition'], 'arm': arm, 'episode_id': ep_id}
    ctx = {'spec': spec, 'arm': 'NO_FEEDBACK', 'M': list(spec['initial']), 'memx': None, 'path': [], 'prev_state': None,
           'own_states': [], 'events': [], 'mount_records': [], 'acquisitions': 0, 'rejections': 0, 'addresses': 0,
           'steps': 0, 'hops': 0, 'donor_item': None}
    cdir = _o888.path.join(CART_ROOT883, ep_id)
    out = dict(key, item=spec['item'], steps=[], points=[], controls=[], obs=[], end=None, accepted=None, error=None,
               cartridges=[], wrong_cartridges=[])
    seen = []                                    # own observations by step (rows + decoded text), for overlap only
    written = {}                                 # step_written -> 887 write_pair result (TRUE / WRONG entries and cards)
    pend, t0, calls0, initial_seal, interrupted, step_sum = None, _t888.perf_counter(), int(env['CALLS849']), None, None, 0.0
    try:
        try:
            _o888.makedirs(cdir, exist_ok=False)
            q = env['QTEXT841'][spec['qid']]; pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
            ctx['memx'], mount = mount865(env, ctx['M'], 'TEST888_L0_%s_%s' % (arm, spec['item'])); ctx['mount_records'].append(mount)
            initial_seal = prefix_seals865(env, ctx['memx'])
            while out['end'] is None:
                if ctx['steps'] >= horizon: out['end'] = 'HORIZON_%d' % horizon; break
                if not budget_left865(env, STEP_CALLS867): out['end'] = 'RESOURCE_BUDGET'; break
                guard883('%s_t%d' % (ep_id, ctx['steps'] + 1)); ts = _t888.perf_counter(); sc0 = int(env['CALLS849'])
                k = len(ctx['path']); pointer = None if k == 0 else ctx['path'][-1]['rows']
                ptext = None if k == 0 else ctx['path'][-1]['text']
                h, kind = hop865(env, ctx['memx'], spec['qid'], k, pointer); ctx['hops'] += 1
                ctx['events'].append({'type': 'HOP', 'k': k, 'kind_logged_only': kind, 'raw': h['text'], 'mounted': list(ctx['M']),
                                      'decision_source': 'MODEL'})
                if kind == 'EMPTY_OUTPUT': out['end'] = 'NATIVE_EMPTY_OUTPUT'; break
                feedback, fb_info = feedback867(env, ctx)
                control, record, state = control_step867(env, ctx, h, pointer, feedback)
                if control is None: out['end'] = 'NATIVE_EMPTY_STATE'; break
                ctx['steps'] += 1; t = ctx['steps']; B = ctx['memx']; X, _ = env['make_x851'](pre, state['segments'], post)
                c_rows, e_rows = state['segments'][0][1], state['segments'][1][1]
                cur = {'c': c_rows, 'e': e_rows, 'hop': record['candidate_text'], 'evid': record['evidence_text']}
                seen.append(cur)
                st = dict(key, step=t, hop=h['text'], hop_kind=kind, pointer=ptext, state_sha256=record['state_sha256'],
                          X_sha256=tsha881(X), B_tokens=length873(env, B), native=reading_view883(record['reading']))
                if not finite_m867(record['reading']): raise Gate883('PHYSICAL_NONFINITE_NATIVE_READING %s t%d' % (ep_id, t))
                cache = None
                if arm == 'NONE':
                    reading = record['reading']; out['obs'].append((c_rows, e_rows))
                else:
                    cache = env['cache_build'](list(B)); nat = car873(env, cache, X); ffe883(int(X.shape[0]) + cont_tokens881(), 80, 'native_read')
                    if not same_reading881(nat, record['reading']): raise Gate883('PHYSICAL_X_PARITY car873 != control_step867 %s t%d' % (ep_id, t))
                    r_none = none_m867(env, B, X, record['reading']); reading = r_none
                    if pend is not None:                       # E_(t-1): written now (C = O_t), as in 887; read only if deferred
                        guard883('%s_t%d_write' % (ep_id, t))
                        w = write_pair_m867(env, pend, c_rows, e_rows, donor_obs, t, cdir, key,
                                            out['cartridges'][-1]['id'] if out['cartridges'] else None)
                        pend = None; written[t - 1] = w
                        out['cartridges'].append(w['true'][1]); out['wrong_cartridges'].append(w['wrong'][1])
                        if STATE_M888['negatives'] is None: STATE_M888['negatives'] = negatives_m867(env, w['true'][0])
                    sw = t - DELAY_M888
                    if sw in written:                          # eligible: the fixed-delay transition cartridge exists
                        guard883('%s_t%d_pair' % (ep_id, t)); d = written[sw]
                        cstep = int(d['true'][0]['provenance']['step_written']) + 1
                        if t - int(d['true'][0]['provenance']['step_written']) != DELAY_M888 or \
                                int(d['wrong'][0]['provenance']['step_written']) != sw:
                            raise Gate883('PHYSICAL_DELAY_CONTRACT %s t%d step_written=%s' % (ep_id, t, d['true'][0]['provenance']['step_written']))
                        first = not out['points']; tr = _t888.perf_counter()
                        r_dt, rt = read_m867(env, B, d['true'][0], d['true'][1], X, cstep, ep_id, cdir, st['B_tokens'], first)
                        r_dw, rw = read_m867(env, B, d['wrong'][0], d['wrong'][1], X, cstep, ep_id, cdir, st['B_tokens'], first)
                        if rt['calls'] != rw['calls']: raise Gate883('PHYSICAL_CALL_PARITY D_TRUE %s != D_WRONG %s' % (rt['calls'], rw['calls']))
                        past = seen[sw + 1 - 1]                # O_(sw+1) = observation of step t-2 (seen is 0-based by step)
                        dc, de = donor_obs[min(sw + 1, len(donor_obs)) - 1]
                        pt = dict(key, world='%02d' % key['world_index'], step=t, delay=t - sw, a_none=r_none['action'],
                                  a_dt=r_dt['action'], a_dw=r_dw['action'], tv_dt_dw=tv_m867(r_dt, r_dw),
                                  tv_dt_none=tv_m867(r_dt, r_none), tv_dw_none=tv_m867(r_dw, r_none),
                                  none=summary_m888(r_none), d_true=summary_m888(r_dt), d_wrong=summary_m888(r_dw),
                                  overlap_true=overlap_m888(past, cur, pointer, ptext),
                                  wrong_fit={'donor_c': int(dc.shape[0]), 'donor_e': int(de.shape[0]), 'true_c': int(past['c'].shape[0]),
                                             'true_e': int(past['e'].shape[0])},
                                  cartridge_true=rt['cartridge'], cartridge_wrong=rw['cartridge'], step_written=sw,
                                  body_tokens=int(d['true'][1]['body_tokens']), geometry=d['geometry'], read_true=rt, read_wrong=rw)
                        pt['unique_key'] = _h888.sha256(_j888.dumps([pt['world'], spec['condition'], t, st['X_sha256'], list(ctx['M']),
                                                                     st['B_tokens'], [p['text'] for p in ctx['path']],
                                                                     d['true'][1]['tensor_sha']], sort_keys=True, default=str).encode()).hexdigest()
                        if first:
                            r_rep, _ = read_m867(env, B, d['true'][0], d['true'][1], X, cstep, ep_id, cdir, st['B_tokens'], False)
                            pt['repeat_reload_bitwise'] = same_reading881(r_dt, r_rep)
                            if not pt['repeat_reload_bitwise']: raise Gate883('PHYSICAL_REPEAT_NOT_BITWISE %s t%d' % (ep_id, t))
                        if first and arm == 'D_TRUE':          # controls: measured, never executed
                            im = written[t - 1]
                            r_it, _ = read_m867(env, B, im['true'][0], im['true'][1], X, t, ep_id, cdir, st['B_tokens'], False)
                            r_iw, _ = read_m867(env, B, im['wrong'][0], im['wrong'][1], X, t, ep_id, cdir, st['B_tokens'], False)
                            r_bt = read_blind_m888(env, B, d['true'][0], d['true'][1], X, cstep, ep_id, cdir, st['B_tokens'])
                            r_bw = read_blind_m888(env, B, d['wrong'][0], d['wrong'][1], X, cstep, ep_id, cdir, st['B_tokens'])
                            ctl = dict(key, world=pt['world'], step=t, imm_true=summary_m888(r_it), imm_wrong=summary_m888(r_iw),
                                       cblind_true=summary_m888(r_bt), cblind_wrong=summary_m888(r_bw),
                                       tv_imm_true_none=tv_m867(r_it, r_none), tv_imm_true_wrong=tv_m867(r_it, r_iw),
                                       tv_dt_none=pt['tv_dt_none'], cblind_equal_bitwise=same_reading881(r_bt, r_bw),
                                       tv_full_cblind_true=tv_m867(r_dt, r_bt), a_full=r_dt['action'], a_cblind=r_bt['action'],
                                       overlap_immediate=overlap_m888(seen[t - 1], cur, pointer, ptext))
                            out['controls'].append(ctl)
                            with open(ROOT864 / 'controls.jsonl', 'a', encoding='utf-8') as f: f.write(_j888.dumps(jsafe878(ctl), sort_keys=True) + '\n')
                            if not ctl['cblind_equal_bitwise']: raise Gate883('PHYSICAL_CBLIND_LEAK %s t%d' % (ep_id, t))
                        out['points'].append(pt)
                        with open(ROOT864 / 'points.jsonl', 'a', encoding='utf-8') as f: f.write(_j888.dumps(jsafe878(pt), sort_keys=True) + '\n')
                        st['exp_op'] = exp_op883(ep_id, t, arm, int(d['true'][1]['body_tokens']), d['write_s'], round(_t888.perf_counter() - tr, 3))
                        reading = r_dt if arm == 'D_TRUE' else r_dw
                        st['deferred'] = {'step_written': sw, 'class': pt['overlap_true']['class'], 'a_none': pt['a_none'],
                                          'a_dt': pt['a_dt'], 'a_dw': pt['a_dw'], 'tv_dt_dw': round(pt['tv_dt_dw'], 4)}
                action = reading['action']
                st.update({'reading': reading_view883(reading), 'action': action, 'decision_source': 'MODEL_CAR_READING_' + arm,
                           'differs_from_native': action != record['action'],
                           'nonrecovery_after_unknown': kind == 'UNKNOWN' and action in NONRECOVERY_M888})
                ctx['events'].append({'type': 'CONTROL', 'k': k, 'step': t, 'action': action, 'decision_source': 'MODEL',
                                      'mounted': list(ctx['M']), 'state_sha256': record['state_sha256'], 'f1_arm': arm})
                terminal = action in TERMINAL883
                if arm != 'NONE' and not terminal:
                    pend = (prepare_experience883(env, cache, B, X, action), prepare_experience883(env, cache, B, X, action))
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
                st['seconds'] = round(_t888.perf_counter() - ts, 3); st['calls'] = int(env['CALLS849']) - sc0; step_sum += st['seconds']
                out['steps'].append(st)
                with open(ROOT864 / 'decisions.jsonl', 'a', encoding='utf-8') as f: f.write(_j888.dumps(jsafe878(st), sort_keys=True) + '\n')
                dd = st.get('deferred')
                line883('STEP', ep_id, 't=%d' % t, 'hop=%r' % h['text'], 'exec=%s' % action, 'native=%s' % record['action'],
                        'deferred=%s' % ('E%d %s N/T/W=%s/%s/%s tv_tw=%.3f' % (dd['step_written'], dd['class'], dd['a_none'], dd['a_dt'],
                                                                         dd['a_dw'], dd['tv_dt_dw']) if dd else '-'),
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
            if str(exc).startswith('PHYSICAL_'): STATE_M888['physical_failure'] = str(exc)[:500]
        except Exception as exc:
            out['end'], out['error'], out['traceback'] = 'EXECUTION_ERROR', '%s: %s' % (type(exc).__name__, exc), traceback.format_exc()
        except BaseException as exc:
            out['end'], out['error'], interrupted = 'INTERRUPTED', '%s: %s' % (type(exc).__name__, exc), exc
    finally:
        pend = None; written.clear(); seen.clear()
        cleanup883(env, ctx, out, spec, arm, cdir, initial_seal, interrupted is not None)
    contract = event_contract883(ctx['events'])
    controls = [e for e in ctx['events'] if e['type'] == 'CONTROL']
    exp_w = expected_cartridges883(ctx['steps'], out['end'], horizon) if arm != 'NONE' else 0
    exp_p = (max(0, ctx['steps'] - DELAY_M888) if exp_w is not None else None) if arm != 'NONE' else 0
    out.update({'final_mounted': list(ctx['M']), 'n_steps': ctx['steps'], 'actions': [c['action'] for c in controls],
                'effects': [e['effect'] for e in ctx['events'] if e['type'] == 'EFFECT'], 'acquisitions': ctx['acquisitions'],
                'event_contract': {x: contract[x] for x in ('ok', 'problems', 'controls', 'effects')},
                'executed_equals_reading': bool(contract['ok'] and [c['action'] for c in controls] == [s['action'] for s in out['steps']]),
                'writes_expected': exp_w, 'points_expected': exp_p, 'mount_integrity': mount_ok883(ctx['mount_records']),
                'cardinality_ok': exp_w is not None and len(out['cartridges']) == exp_w == len(out['wrong_cartridges'])
                                  and len(out['points']) == exp_p,
                'seconds': round(_t888.perf_counter() - t0, 1), 'calls': int(env['CALLS849']) - calls0})
    out['overhead_s'] = round(out['seconds'] - step_sum, 1)
    STATE883['budget']['episode_overhead_s'].append(out['overhead_s'])
    line883('EPISODE', ep_id, 'end=%s' % out['end'], 'actions=%s' % '>'.join(out['actions']), 'accepted=%r' % out['accepted'],
            'points=%d/%s' % (len(out['points']), exp_p), 'writes=%d+%d/%s' % (len(out['cartridges']), len(out['wrong_cartridges']), exp_w),
            'restore=%s' % out['exact_restore_vs_first_mount'], 'contract=%s' % contract['ok'], 's=%.0f' % out['seconds'],
            '' if not out['error'] else 'ERROR=' + str(out['error'])[:300])
    if out.get('traceback'): short864(out['traceback'])
    rec = {x: y for x, y in out.items() if x not in ('steps', 'obs', 'points', 'controls')}
    with open(ROOT864 / 'episodes.jsonl', 'a', encoding='utf-8') as f: f.write(_j888.dumps(jsafe878(rec), sort_keys=True) + '\n')
    STATE_M888['episodes'].append(out); STATE_M888['points'] += out['points']; STATE_M888['controls'] += out['controls']
    if out['exact_restore_vs_first_mount'] is False and not STATE_M888['physical_failure']:
        STATE_M888['physical_failure'] = 'PHYSICAL_RESTORE_FALSE %s' % ep_id
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


# ============================ G0 source capture + CPU selftests of the new layer ============================
def capture_m888():
    try:
        src, how = get_ipython().history_manager.input_hist_raw[-1], 'IPYTHON_CURRENT_CELL'
    except NameError:
        src, how = (open(__file__, encoding='utf-8').read() if '__file__' in globals() else None), 'FILE'
    lock = body_lock_m888(src)
    if not lock['ok']:
        try:
            if isinstance(src, str): (ROOT864 / 'TEST888_captured_cell.txt').write_text(src, encoding='utf-8')
        except OSError: pass
        raise Gate_m867('SOURCE_SELF_LOCK %s (how=%s, chars=%s; paste the parts into ONE cell, in order, unchanged)' % (
            lock, how, len(src) if isinstance(src, str) else None))
    tree, t887 = _a888.parse(src), _a888.parse(B887_M888)
    funcs = {n.name: n for n in tree.body if isinstance(n, _a888.FunctionDef)}
    f887 = {n.name: n for n in t887.body if isinstance(n, _a888.FunctionDef)}
    for name, node in funcs.items(): scan883(node, EXEC_ALLOW_M888.get(name, ()))
    missing = sorted(set(RUNTIME_NEW_M888) - set(funcs)) + sorted(set(RUNTIME_887_M888) - set(f887))
    if missing: raise Gate_m867('RUNTIME_FUNCTIONS_MISSING %s' % missing)
    for name in RUNTIME_NEW_M888: oracle_scan883(funcs[name])
    for name in RUNTIME_887_M888: scan883(f887[name]); oracle_scan883(f887[name])
    count = lambda f: sum(1 for n in _a888.walk(tree) if isinstance(n, _a888.Call) and getattr(n.func, 'id', None) == f)
    facts = {'reproduce_pre859859_calls': count('reproduce_pre859859'), 'execute866_calls': count('execute866'),
             'input_calls': count('input'), 'rearm_budget865_calls': count('rearm_budget865')}
    if facts != {'reproduce_pre859859_calls': 1, 'execute866_calls': 1, 'input_calls': 0, 'rearm_budget865_calls': 1}:
        raise Gate_m867('SOURCE_FACTS %s' % facts)
    raw = src.encode('utf-8')
    (ROOT864 / 'TEST888.py').write_bytes(raw)
    STATE_M888['source'] = {'how': how, 'executed_cell_git_blob': git_blob864(raw), 'executed_cell_sha256': sha256_bytes864(raw),
                            'body_lock': lock, 'facts': facts, 'firewall': 'PASS', 'oracle_firewall': 'PASS %d+%d' % (
                                len(RUNTIME_NEW_M888), len(RUNTIME_887_M888))}
    STATE883['source'] = {'executed_cell_git_blob': STATE_M888['source']['executed_cell_git_blob']}
    json_write864('TEST888_source_manifest.json', dict(STATE_M888['source'], base887=B887_INFO_M888, base885=BASE_INFO_M867,
                                                       engine=ENGINE_INFO883, head=HEAD883, prereg_sha256=PREREG_SHA_M888,
                                                       before_model_load=True))
    print('T888 SOURCE blob=%s sha256=%s body_lock=%s' % (STATE_M888['source']['executed_cell_git_blob'],
                                                         STATE_M888['source']['executed_cell_sha256'], lock['measured']), flush=True)


def st_m888():
    import numpy as _np
    r = {}
    body = 'x = 1\nif x:\n    print(x)\n'; lk = '# TEST888 BODY-SHA256 ' + _h888.sha256(body.encode()).hexdigest()
    r['lock_ok'] = body_lock_m888(lk + '\n' + body)['ok']
    r['lock_paste_whitespace_ok'] = body_lock_m888(' ' + lk + '  \r\n\r\n' + body.replace('\n', ' \r\n'))['ok']
    r['lock_suffix_refused'] = not body_lock_m888(lk + '\n' + body + 'print(2)\n')['ok']
    r['lock_edit_refused'] = not body_lock_m888(lk + '\n' + body.replace('1', '2'))['ok']
    r['lock_887_header_refused'] = not body_lock_m888(lk.replace('TEST888', 'TEST867') + '\n' + body)['ok']
    A = _np.arange(12, dtype=_np.float32).reshape(3, 4); Bm = A + 100
    r['rowset_counts_rows'] = len(rowset_m888(A, A[:1])) == 3
    o = overlap_m888({'c': A, 'e': Bm, 'hop': ' X ', 'evid': 'e1'}, {'c': Bm[:1] + 1, 'e': Bm[2:] + 1, 'hop': 'Y', 'evid': 'e2'}, A[1:2], 'Z')
    r['overlap_pointer_row_echo'] = o['class'] == 'ROW_ECHO' and o['row_echo_rows'] == 1 and o['candidate_row_echo'] and not o['evidence_row_echo']
    o = overlap_m888({'c': A, 'e': Bm, 'hop': 'X', 'evid': 'e1'}, {'c': A + 1, 'e': Bm, 'hop': 'Q', 'evid': 'e1'}, None, 'Z')
    r['overlap_static_evidence_echo'] = o['class'] == 'ROW_ECHO' and o['evidence_row_echo'] and not o['candidate_row_echo']
    o = overlap_m888({'c': A, 'e': Bm, 'hop': ' X ', 'evid': 'e1'}, {'c': A + 1, 'e': Bm + 1, 'hop': 'Q', 'evid': 'e2'}, None, 'X')
    r['overlap_pointer_text_repeat'] = o['class'] == 'TEXT_REPEAT' and o['hop_text_repeat']
    o = overlap_m888({'c': A, 'e': Bm, 'hop': 'X', 'evid': 'e1'}, {'c': A + 1, 'e': Bm + 1, 'hop': 'Q', 'evid': 'e2'}, A + 7, 'Z')
    r['overlap_novel'] = o['class'] == 'NOVEL'
    # verdict rules
    phys = {'reads_true': 6, 'reads_wrong': 6, 'no_physical_failure': True, 'negatives_refused': True, 'post_run_integrity': True,
            'cleanup_clean': True}
    def P(w, step, tv, at, aw, cls='NOVEL', tvn=0.3, cond='FORK', key=None):
        return {'world': w, 'condition': cond, 'step': step, 'tv_dt_dw': tv, 'tv_dt_none': tvn, 'a_dt': at, 'a_dw': aw,
                'overlap_true': {'class': cls}, 'unique_key': key or '%s%s%d%s' % (w, cond, step, at)}
    def Yf(dtf, nf, dwf, dtm=1, nm=1, dwm=1):
        m = {('D_TRUE', 'FORK'): dtf, ('NONE', 'FORK'): nf, ('D_WRONG', 'FORK'): dwf, ('D_TRUE', 'MISSING'): dtm,
             ('NONE', 'MISSING'): nm, ('D_WRONG', 'MISSING'): dwm}
        return {'%s_%s_%s' % (a, w, c): {'Y': m[(a, c)]} for (w, c) in CELLS_M867 for a in ARMS_M888}
    rec_pass = {'D_TRUE': {'unknown_steps': 2, 'violations': 0}, 'NONE': {'unknown_steps': 2, 'violations': 1}}
    ctl = [{'tv_imm_true_none': 0.8, 'tv_dt_none': 0.3, 'tv_full_cblind_true': 0.1, 'a_full': 'ACQUIRE', 'a_cblind': 'ACQUIRE'}]
    U = [P('10', 4, 0.3, 'ACQUIRE', 'ADVANCE'), P('10', 5, 0.01, 'STOP', 'STOP'), P('09', 4, 0.2, 'ACCEPT', 'ACCEPT'), P('09', 5, 0.0, 'A', 'A')]
    v = verdict_m888('COMPLETE', phys, U, Yf(1, 0, 0), rec_pass, ctl)
    r['verdict_all_pass'] = v['OVERALL'] == 'PASS' and v['OUTCOME_PARTIAL'].startswith('2/2') and v['c_read_channel'] == 'PRESENT'
    v = verdict_m888('COMPLETE', phys, U + [dict(U[0])], Yf(1, 0, 0), rec_pass, ctl)
    r['dedupe_duplicate_point'] = v['reasons']['points']['unique'] == 4 and v['reasons']['points']['raw'] == 5
    v = verdict_m888('COMPLETE', phys, [dict(p, overlap_true={'class': 'ROW_ECHO'}) for p in U], Yf(1, 0, 0), rec_pass, ctl)
    r['all_row_echo_nonredundancy_fail'] = v['NONREDUNDANCY'] == 'FAIL' and v['OVERALL'] == 'FAIL'
    v = verdict_m888('COMPLETE', phys, [U[0], dict(U[1], overlap_true={'class': 'TEXT_REPEAT'})] + U[2:], Yf(1, 0, 0), rec_pass, ctl)
    r['some_overlap_inconclusive'] = v['NONREDUNDANCY'] == 'INCONCLUSIVE' and v['content_on_novel_points']['points'] == 3
    v = verdict_m888('COMPLETE', phys, U, Yf(1, 0, 0, dtm=0, nm=1), rec_pass, ctl)
    r['missing_harm_outcome_fail'] = v['OUTCOME_BENEFIT'] == 'FAIL'
    v = verdict_m888('COMPLETE', phys, U, Yf(1, 0, 1), rec_pass, ctl)
    r['wrong_also_succeeds_fail_partial0'] = v['OUTCOME_BENEFIT'] == 'FAIL' and v['OUTCOME_PARTIAL'].startswith('0/2')
    Y1 = Yf(1, 0, 0); Y1['D_TRUE_09_FORK'] = {'Y': 0}
    v = verdict_m888('COMPLETE', phys, U, Y1, rec_pass, ctl)
    r['partial_gain_never_pass'] = v['OUTCOME_BENEFIT'] == 'FAIL' and v['OUTCOME_PARTIAL'].startswith('1/2')
    v = verdict_m888('COMPLETE', phys, U, Yf(1, 0, 0), {'D_TRUE': {'unknown_steps': 2, 'violations': 1}, 'NONE': {'violations': 1}}, ctl)
    r['recovery_violation_fail'] = v['RECOVERY'] == 'FAIL'
    v = verdict_m888('COMPLETE', phys, U, Yf(1, 0, 0), {'D_TRUE': {'unknown_steps': 0}}, ctl)
    r['recovery_none_not_measured'] = v['RECOVERY'] == 'NOT_MEASURED'
    v = verdict_m888('COMPLETE', phys, U, Yf(1, 0, 0), {'D_TRUE': {'unknown_steps': 2, 'violations': 0}, 'NONE': {'violations': 0}}, ctl)
    r['recovery_no_contrast_inconclusive'] = v['RECOVERY'] == 'INCONCLUSIVE'
    v = verdict_m888('BUDGET_STOP', phys, U, Yf(1, 0, 0), rec_pass, ctl)
    r['budget_stop_never_pass'] = v['OVERALL'] == 'BUDGET_STOP' and 'PASS' not in (v['CONTENT_EFFECT'], v['OUTCOME_BENEFIT'],
                                                                                     v['RECOVERY'], v['NONREDUNDANCY'])
    v = verdict_m888('COMPLETE', phys, [], Yf(0, 0, 0), {}, [])
    r['no_points_not_measured'] = v['CONTENT_EFFECT'] == 'NOT_MEASURED' and v['NONREDUNDANCY'] == 'NOT_MEASURED'
    v = verdict_m888('COMPLETE', phys, U[:3], Yf(1, 0, 0), rec_pass, ctl)
    r['three_points_content_inconclusive'] = v['CONTENT_EFFECT'] == 'INCONCLUSIVE'
    v = verdict_m888('COMPLETE', phys, [dict(p, tv_dt_dw=0.0, a_dw=p['a_dt']) for p in U], Yf(0, 0, 0), rec_pass,
                     [dict(ctl[0], tv_full_cblind_true=0.0)])
    r['no_content_fail_and_channel_absent'] = v['CONTENT_EFFECT'] == 'FAIL' and v['c_read_channel'] == 'ABSENT'
    v = verdict_m888('COMPLETE', dict(phys, negatives_refused=False), U, Yf(1, 0, 0), rec_pass, ctl)
    r['physical_fail_blocks_all'] = v['PHYSICAL_READ'] == 'FAIL' and v['CONTENT_EFFECT'] == 'INCONCLUSIVE' and v['OVERALL'] == 'FAIL'
    eps = [{'arm': 'D_TRUE', 'episode_id': 'e', 'steps': [{'step': 3, 'hop_kind': 'UNKNOWN', 'action': 'ADVANCE'},
                                                          {'step': 4, 'hop_kind': 'UNKNOWN', 'action': 'ADVANCE'},
                                                          {'step': 5, 'hop_kind': 'NODE', 'action': 'ACCEPT'},
                                                          {'step': 6, 'hop_kind': 'UNKNOWN', 'action': 'ACQUIRE'}]}]
    rc = recovery_m888(eps)['D_TRUE']
    r['recovery_counts_only_t_ge_4_unknown'] = rc['unknown_steps'] == 2 and rc['violations'] == 1
    for nm, src in (('hook', 'def f(m):\n    m.register_forward_hook(1)\n'), ('executor', 'def f(e):\n    execute866(e, 1, 2, 3, 4, 5)\n')):
        try: scan883(_a888.parse(src).body[0]); r['firewall_%s_refused' % nm] = False
        except AssertionError: r['firewall_%s_refused' % nm] = True
    r['delay_sealed_3'] = DELAY_M888 == 3 and PREREG_M888['delay'] == 3
    r['prereg_sha_stable'] = PREREG_SHA_M888 == _h888.sha256(_j888.dumps(PREREG_M888, sort_keys=True, default=str).encode()).hexdigest()
    return r


# ============================ single cell execution ============================
T_START878 = T_START883 = T_CELL_M888
ORACLE_VAULT883 = None; OFFLINE_DIGEST_G1_885 = None; VAULT_FP885 = None
try:
    STATE_M888['status'] = 'G0'; capture_m888()
    json_write864('TEST888_prereg.json', {'prereg': PREREG_M888, 'sha256': PREREG_SHA_M888, 'written_before_model_load': True})
    load_sources865(); select_locked883()
    du = _s888.disk_usage(str(ROOT864))
    if du.free / 2**30 < 5.0: raise Gate_m867('DISK_FREE %.1f GiB' % (du.free / 2**30))
    STATE883['write_probe'] = write_probe883(ROOT864)
    if not all(STATE883['write_probe'].values()): raise Gate_m867('WRITE_PROBE %s' % STATE883['write_probe'])
    source_audit878(); load878(); run_selftests883()               # the 885 CPU selftests, unchanged
    STATE_M888['selftest'] = {'887': st_m867(), '888': st_m888()}  # the 887 CPU selftests, unchanged, + the new layer
    json_write864('TEST888_cpu_selftest.json', STATE_M888['selftest'])
    bad_ = sorted('%s/%s' % (g_, k) for g_, d_ in STATE_M888['selftest'].items() for k, v in d_.items()
                  if not (v is True or v == 'NOT_RUN_NO_TORCH'))
    if bad_: raise Gate_m867('CPU_SELFTEST %s' % bad_)
    STATE883['live_scan'] = live_path_scan883([ENGINE883['body']] + [RAW_SOURCES864[n].decode() for n in ('873.py', '878.py', '881.py')])
    if not STATE883['live_scan']['ok']: raise Gate_m867('LIVE_PATH_ORACLE_SCAN %s' % STATE883['live_scan'])
    feasibility_audit864(); audit_contracts865(); load_spine864()
    if not (CC_GPU_OK and 'A100' in str(CC_GPU.get('name')) and CC_GPU.get('total_gib', 0) >= 78.0): raise Gate_m867('A100_80GB_REQUIRED %s' % CC_GPU)
    gate_m888('G0', 'PASS', selftests_885=sorted(STATE883['selftests']), selftest_887=len(STATE_M888['selftest']['887']),
              selftest_888=len(STATE_M888['selftest']['888']), prereg_sha256=PREREG_SHA_M888, disk_free_gib=round(du.free / 2**30, 1))
    STATE_M888['status'] = 'G1'                                     # model + native backbone: the 885/887 G1 chain, unchanged calls
    env883, original_error883, original_trace883, reproduction883 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace883; TWO_JOB_VERIFICATION864 = verify_two_job859(env883, original_trace883)
    assert_hook_free859(env883, 'T888_before_native'); OFFLINE_DIGEST_G1_885 = install_offline_evaluator859(env883)
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
    assert not any(p_.requires_grad for p_ in env883['model'].parameters()), 'NOT_FROZEN'
    assert_hook_free859(env883, 'T888_before_points')
    STATE883['model_contract'] = model_contract883(env883, CC_GPU)
    if not STATE883['model_contract']['ok']: raise Gate_m867('MODEL_CONTRACT %s' % STATE883['model_contract']['checks'])
    if _o888.path.exists(CART_ROOT883): _s888.rmtree(CART_ROOT883)
    _o888.makedirs(CART_ROOT883); EXP_DIR878 = type(ROOT864)(CART_ROOT883)
    gate_m888('G1', 'PASS', chunk=EXP878['CHUNK'], P=int(env883['P']), model_contract=STATE883['model_contract']['checks'],
              bank_digest=digest883, weights_digest=WEIGHTS0_878)
    by_key883 = build_specs869(env883)
    ORACLE_VAULT883 = seal_oracle883(env883); VAULT_FP885 = vault_fingerprint885(ORACLE_VAULT883)   # live work without oracle keys
    STATE_M888['status'] = 'RUN'
    assert CALL_ALLOWANCE865 == 3000, ('CALL_ALLOWANCE865', CALL_ALLOWANCE865)
    now_ = _t888.perf_counter(); plan_ = g2_budget_plan883(now_, T_START883, WALL_S883)
    if plan_ is None: raise Budget883('NO_TIME_LEFT_AFTER_G1')
    T0_865 = plan_['T0_865']; TEST865_MINUTES = plan_['TEST865_MINUTES']
    rearm_budget865(env883)                                         # +30 min engine margin; the 75 min wall is guard883 / admit883
    if budget_left865(env883, STEP_CALLS867) is not True: raise Budget883('RESOURCE_BUDGET_AT_RUN_START')
    plan_m888 = [('NONE', w_, c_) for (w_, c_) in CELLS_M867] + [(a_, w_, c_) for (w_, c_) in CELLS_M867 for a_ in ('D_TRUE', 'D_WRONG')]
    obs_m888 = {}
    for i_, (a_, w_, c_) in enumerate(plan_m888):
        if i_: admit883('E%02d_%s_%s_%s' % (i_, a_, w_, c_), len(plan_m888) - i_)
        donor_ = None if a_ == 'NONE' else obs_m888.get((DONOR_M867[w_], c_))
        ep_ = episode_m888(env883, by_key883[(int(w_), c_)], a_, '%s_%s_%s' % (a_, w_, c_), HORIZON883, donor_)
        if a_ == 'NONE': obs_m888[(w_, c_)] = ep_['obs']
        ep_['obs'] = len(ep_['obs'])                                # rows stay in obs_m888 only
    STATE_M888['status'] = 'POST'
    STATE_M888['post_run'] = {'bank_digest_unchanged': records_digest861(env883) == digest883,
                              'memnull_seal_unchanged': physical_seal863(env883, env883['MEMNULL841']) == null_seal883,
                              'weights_unchanged': weights_digest877(env883) == WEIGHTS0_878,
                              'hooks_zero': hook_audit859(env883, 'T888_final')['hook_count'] == 0,
                              'model_contract_ok': model_contract883(env883, CC_GPU)['ok']}
    if not all(STATE_M888['post_run'].values()): raise Gate883('PHYSICAL_POST_RUN_INTEGRITY %s' % STATE_M888['post_run'])
    oenv_m888, ev_m888 = evaluator_env885(env883, ORACLE_VAULT883, OFFLINE_DIGEST_G1_885, VAULT_FP885)
    STATE_M888['scores'] = episode_scores885(oenv_m888, by_key883, STATE_M888['episodes']); STATE_M888['evaluator'] = ev_m888
    del oenv_m888
    STATE_M888['technical_status'] = 'COMPLETE'
except Budget883 as exc:
    STATE_M888['technical_status'] = 'BUDGET_STOP'; STATE_M888['error'] = str(exc)
except BaseException as exc:
    STATE_M888['technical_status'] = 'INTERRUPTED' if isinstance(exc, (KeyboardInterrupt, SystemExit)) else 'TECHNICAL_BLOCK'
    STATE_M888['error'] = '%s: %s' % (type(exc).__name__, exc); STATE_M888['traceback'] = traceback.format_exc()
    if str(exc).startswith('PHYSICAL_') and not STATE_M888['physical_failure']: STATE_M888['physical_failure'] = str(exc)[:500]
    print('TEST888 ERROR at', STATE_M888['status'], STATE_M888['error'][:400], file=ERROR_CONSOLE864, flush=True)
    print(STATE_M888['traceback'], file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        if _o888.path.exists(CART_ROOT883):
            left_ = sorted(_o888.listdir(CART_ROOT883)); _s888.rmtree(CART_ROOT883)
            if left_: STATE883['cleanup_errors'].append({'episode_id': 'CART_ROOT', 'errors': ['LEFTOVER %s' % left_[:20]]})
    except BaseException as exc: STATE883['cleanup_errors'].append({'episode_id': 'CART_ROOT', 'errors': ['%s: %s' % (type(exc).__name__, exc)]})
    if STATE_M888['post_run'] is None and isinstance(globals().get('env883'), dict) and 'digest883' in globals():
        try:                                       # post-run integrity also after a budget stop or a non-physical block
            STATE_M888['post_run'] = {'bank_digest_unchanged': records_digest861(env883) == digest883,
                                      'memnull_seal_unchanged': physical_seal863(env883, env883['MEMNULL841']) == null_seal883,
                                      'weights_unchanged': weights_digest877(env883) == WEIGHTS0_878,
                                      'hooks_zero': hook_audit859(env883, 'T888_final')['hook_count'] == 0,
                                      'model_contract_ok': model_contract883(env883, CC_GPU)['ok'], 'computed_in': 'finally'}
        except BaseException as exc:
            STATE_M888['post_run'] = {'error': '%s: %s' % (type(exc).__name__, exc)}
    pts_, eps_ = STATE_M888['points'], STATE_M888['episodes']
    phys_ = {'reads_true': len(pts_), 'reads_wrong': len(pts_), 'physical_failure': STATE_M888['physical_failure'],
             'no_physical_failure': STATE_M888['physical_failure'] is None,
             'negatives_refused': None if STATE_M888['negatives'] is None else all(STATE_M888['negatives'].values()),
             'post_run_integrity': None if STATE_M888['post_run'] is None else all(v is True for k, v in STATE_M888['post_run'].items()
                                                                                    if k != 'computed_in') and 'error' not in STATE_M888['post_run'],
             'cleanup_clean': not STATE883['cleanup_errors']}
    try:
        STATE_M888['verdict'] = verdict_m888(STATE_M888['technical_status'] or 'TECHNICAL_BLOCK', phys_, pts_, STATE_M888['scores'],
                                             recovery_m888(eps_), STATE_M888['controls'])
    except BaseException as exc:
        STATE_M888['verdict'] = {'TECHNICAL_STATUS': 'TECHNICAL_BLOCK', 'PHYSICAL_READ': 'FAIL', 'NONREDUNDANCY': 'INCONCLUSIVE',
                                 'CONTENT_EFFECT': 'INCONCLUSIVE', 'OUTCOME_BENEFIT': 'NOT_MEASURED', 'RECOVERY': 'INCONCLUSIVE',
                                 'OVERALL': 'TECHNICAL_BLOCK', 'reasons': {'verdict_error': '%s: %s' % (type(exc).__name__, exc)}}
    U_ = unique_m888(pts_)
    report_m888 = {
        'test': 'TEST888', 'verdict': STATE_M888['verdict'], 'physical_facts': phys_, 'error': STATE_M888['error'],
        'hashes': {'executed_cell': STATE_M888['source'], 'base887': B887_INFO_M888, 'base885': BASE_INFO_M867, 'engine': ENGINE_INFO883,
                   'prereg_sha256': PREREG_SHA_M888, 'head_locks': HEAD883, 'weights_digest': globals().get('WEIGHTS0_878'),
                   'bank_digest': globals().get('digest883')},
        'gates': STATE_M888['gates'], 'negatives': STATE_M888['negatives'], 'post_run': STATE_M888['post_run'],
        'counters': {'episodes': len(eps_), 'steps': sum(e_['n_steps'] for e_ in eps_ if e_.get('n_steps') is not None),
                     'points_raw': len(pts_), 'points_unique': len(U_), 'controls': len(STATE_M888['controls']),
                     'cartridges_true': sum(len(e_['cartridges']) for e_ in eps_), 'cartridges_wrong': sum(len(e_['wrong_cartridges']) for e_ in eps_),
                     'ssd_bytes': sum(int(c_.get('bytes') or 0) for e_ in eps_ for c_ in e_['cartridges'] + e_['wrong_cartridges']),
                     'calls849': globals().get('env883', {}).get('CALLS849') if isinstance(globals().get('env883'), dict) else None,
                     'wall_s': round(_t888.perf_counter() - T_CELL_M888, 1),
                     'peak_alloc_gib': STATE883['budget'].get('peak_alloc_gib'), 'ffe_by_kind': STATE883['budget'].get('ffe_by_kind')},
        'cells': {'%s_%s' % (w_, c_): {a_: next(({'end': e_['end'], 'actions': e_['actions'], 'effects': e_['effects'],
                                                 'accepted': e_['accepted'], 'final_mounted': e_['final_mounted'],
                                                 'Y': (STATE_M888['scores'] or {}).get(e_['episode_id'], {}).get('Y')}
                                                for e_ in eps_ if e_['episode_id'] == '%s_%s_%s' % (a_, w_, c_)), None)
                                         for a_ in ARMS_M888} for (w_, c_) in CELLS_M867},
        'points_unique': [{k_: p_[k_] for k_ in ('episode_id', 'step', 'step_written', 'a_none', 'a_dt', 'a_dw', 'tv_dt_dw', 'tv_dt_none',
                                                 'tv_dw_none', 'overlap_true', 'wrong_fit', 'body_tokens', 'none', 'd_true', 'd_wrong',
                                                 'unique_key')} for p_ in U_],
        'controls': STATE_M888['controls'], 'cleanup_errors': STATE883['cleanup_errors'], 'evaluator': STATE_M888.get('evaluator'),
        'not_claimed': PREREG_M888['not_claimed'], 'gpu_note': 'GPU_NOT_RUN_BY_AUTHOR (cell author); GPU_RUN_THIS_TEST if this is a Colab console'}
    try:
        if STATE_M888['traceback']: (ROOT864 / 'TEST888_traceback.txt').write_text(STATE_M888['traceback'], encoding='utf-8')
        json_write864('TEST888_final_report.json', jsafe878(report_m888) if 'jsafe878' in globals() else _j888.loads(_j888.dumps(report_m888, default=str)))
        p_ = ROOT864 / 'TEST888_final_report.json'
        if _j888.loads(p_.read_text(encoding='utf-8'))['verdict']['TECHNICAL_STATUS'] != STATE_M888['verdict']['TECHNICAL_STATUS']:
            raise OSError('READ_BACK_MISMATCH')
        STATE_M888['report_sha256'] = sha256_bytes864(p_.read_bytes())
    except BaseException as exc:
        STATE_M888['artifact_errors'].append('%s: %s' % (type(exc).__name__, exc))
        STATE_M888['verdict'] = dict(STATE_M888['verdict'], TECHNICAL_STATUS='ARTIFACT_FAILURE', OVERALL='ARTIFACT_FAILURE', PHYSICAL_READ='FAIL',
                                     NONREDUNDANCY='INCONCLUSIVE', CONTENT_EFFECT='INCONCLUSIVE', OUTCOME_BENEFIT='NOT_MEASURED',
                                     RECOVERY='INCONCLUSIVE')
    v_ = STATE_M888['verdict']
    print('=' * 110)
    print('TEST888 | %s' % ' | '.join('%s=%s' % (k_, v_.get(k_)) for k_ in ('TECHNICAL_STATUS', 'PHYSICAL_READ', 'NONREDUNDANCY',
                                                                          'CONTENT_EFFECT', 'OUTCOME_BENEFIT', 'RECOVERY', 'OVERALL')))
    print('OUTCOME_PARTIAL=%s | presence_points=%s | c_read_channel=%s | echo_contrast=%s | novel=%s' % (
        v_.get('OUTCOME_PARTIAL'), v_.get('presence_points'), v_.get('c_read_channel'),
        _j888.dumps(v_.get('echo_contrast'), default=str)[:300], v_.get('content_on_novel_points')))
    for p_ in U_:
        print('POINT %-18s t=%d E%d %-11s NONE=%-9s D_TRUE=%-9s D_WRONG=%-9s TV(T,W)=%.3f TV(T,N)=%.3f margin T/W=%s/%s fit=%s' % (
            p_['episode_id'], p_['step'], p_['step_written'], p_['overlap_true']['class'], p_['a_none'], p_['a_dt'], p_['a_dw'],
            p_['tv_dt_dw'], p_['tv_dt_none'], p_['d_true']['margin_logp'], p_['d_wrong']['margin_logp'], p_['wrong_fit']))
        print('      p(NONE)=%s' % {k_: round(x_, 3) for k_, x_ in p_['none']['p'].items()})
        print('      p(D_T) =%s' % {k_: round(x_, 3) for k_, x_ in p_['d_true']['p'].items()})
        print('      p(D_W) =%s' % {k_: round(x_, 3) for k_, x_ in p_['d_wrong']['p'].items()})
    for c_ in STATE_M888['controls']:
        print('CONTROL %s t=%d IMM_T=%s IMM_W=%s CBLIND_T=%s CBLIND_W=%s equal=%s TV(IMM_T,N)=%.3f TV(D_T,N)=%.3f TV(D_T,CBLIND)=%.3f imm_overlap=%s' % (
            c_['episode_id'], c_['step'], c_['imm_true']['action'], c_['imm_wrong']['action'], c_['cblind_true']['action'],
            c_['cblind_wrong']['action'], c_['cblind_equal_bitwise'], c_['tv_imm_true_none'], c_['tv_dt_none'], c_['tv_full_cblind_true'],
            c_['overlap_immediate']['class']))
    for k_, c_ in report_m888['cells'].items():
        print('CELL %-11s' % k_, ' | '.join('%s:%s Y=%s' % (a_, '>'.join((c_[a_] or {}).get('actions') or []), (c_[a_] or {}).get('Y'))
                                           for a_ in ARMS_M888))
    print('reasons', _j888.dumps(v_.get('reasons'), default=str)[:1500])
    print('error', STATE_M888['error'], '| artifact_errors', STATE_M888['artifact_errors'], '| report sha256', STATE_M888.get('report_sha256'))
    print('=' * 110, flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE883['suffix'], 'test870.py:suffix', 'exec'), globals())     # ZIP + SHA256SUMS + testzip + Drive copy (locked I/O)
try:                                                                          # delivery receipt beside the ZIP (outside it)
    import zipfile as _z888
    with _z888.ZipFile(CC_ZIP) as _zz: _zip_ok = _zz.testzip() is None
    _zsha = _h888.sha256(CC_ZIP.read_bytes()).hexdigest()
    _rc = {'zip': str(CC_ZIP), 'zip_sha256': _zsha, 'zip_testzip_ok': _zip_ok, 'verdict': {k_: STATE_M888['verdict'].get(k_) for k_ in (
               'TECHNICAL_STATUS', 'PHYSICAL_READ', 'NONREDUNDANCY', 'CONTENT_EFFECT', 'OUTCOME_BENEFIT', 'RECOVERY', 'OVERALL')},
           'drive_dir': CC_DRIVE_DIR, 'drive_zip_sha256_equal': None}
    if CC_DRIVE_DIR is not None:
        _dz = _o888.path.join(CC_DRIVE_DIR, _o888.path.basename(str(CC_ZIP)))
        _rc['drive_zip_sha256_equal'] = _o888.path.exists(_dz) and _h888.sha256(open(_dz, 'rb').read()).hexdigest() == _zsha
    _rp = str(CC_ZIP).replace('.zip', '_RECEIPT.json')
    with open(_rp, 'w', encoding='utf-8') as _f: _f.write(_j888.dumps(_rc, sort_keys=True, default=str, indent=1))
    if CC_DRIVE_DIR is not None: _s888.copy2(_rp, CC_DRIVE_DIR)
    print('TEST888 RECEIPT', _j888.dumps(_rc, sort_keys=True, default=str)[:600])
    if not _zip_ok or _rc['drive_zip_sha256_equal'] is False: print('TEST888 ARTIFACT_INCOMPLETE: ZIP or Drive copy not verified')
except BaseException as _exc:
    print('TEST888 ARTIFACT_INCOMPLETE: receipt failed', type(_exc).__name__, _exc)
