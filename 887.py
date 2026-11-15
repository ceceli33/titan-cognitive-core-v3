# TEST887 BODY-SHA256 6aac45b07bcde5e21bee4407e06a9d721f26aeabfbbd1fff096fa4bf0fa84dc5
# AKBASCORE SILICON HIPPOCAMPUS — TEST887 — MINIMAL PHYSICAL CARTRIDGE PROBE (one Colab cell, one Run, A100-SXM4-80GB)
# Question: does a physical CUT3/H3/KV experience cartridge, written to SSD from a real native step, SHA-verified and reloaded
# independently, change the next native CAR action distribution through its CONTENT (not through its mere presence / geometry)?
# At one and the same decision state (same B, same X, same six candidate actions, same explicit read path xcar878 blind=()):
#   NONE  = [B]            (no cartridge; must equal the native control_step867 reading bitwise at every step)
#   TRUE  = [B][E_true]    (E = [X2][A][C]: X2/A of the previous native step, C = the real next observation)
#   WRONG = [B][E_wrong]   (same X2/A rows bitwise, same token geometry, C = a real observation of ANOTHER world, same step)
# Physical outcome: three trajectories per cell (NONE / TRUE / WRONG drive the literal locked execute866); success is scored
# only after all live work, by the locked evaluator in a separate offline env (oracle keys are not in the live env).
# REUSE, NOT REWRITE: the definitions of 885.py (GPU run 2026-11-14: G0-G6 PASS) are downloaded from an exact commit, checked
# against git blob + SHA-256, and executed unchanged: locked engine test870.py (e322ed8e / de3c8153), locks at 3d75f289,
# 873/877/878/881 selected by AST, episode cleanup / read contract / experience writer / offline evaluator of 885.
# NEW here: the three-reading paired probe (read887 / none887 / write_pair887 / episode887), a body-hash self-lock, finite
# and call-parity gates, a determinism (independent SSD reload) null control, cartridge corruption negatives, a sealed verdict.
# No training, LoRA, optimizer, backward, RAG, text replay, hooks, hidden states, router, forced action, answer fixing.
# GPU_NOT_RUN_BY_AUTHOR.
import time as _t887
T_CELL887 = _t887.perf_counter()                       # the single 75-minute clock starts here (before any download)
import ast as _a887, hashlib as _h887, json as _j887, os as _o887, re as _r887, urllib.request as _u887, shutil as _s887
BASE_URL887 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
               '99d05ecf48a77b0edaaf188e01be2806f39b0bf4/885.py')
BASE_BLOB887 = '51900159fd9787771d9b67ec435fe5071f3650d1'
BASE_SHA887 = '41ee03f54dfa056a520ad74ff0231b4bd4a5157baa51698df37eca4c01fdb336'
BASE_CUT887 = '# ============================ single cell execution ============================'
BASE_RENAMES887 = (("TEST885_HUCRE_CIKTISI", "TEST887_HUCRE_CIKTISI", 1), ("MyDrive/TEST885_", "MyDrive/TEST887_", 1),
                   ("TEST885_RUN_", "TEST887_RUN_", 2), ("885_engine.log", "887_engine.log", 2),
                   ("885_events.jsonl", "887_events.jsonl", 2), ("TEST885_SONUC_", "TEST887_SONUC_", 1))


def base_definitions887(raw):
    # 885.py bytes -> its definition part (everything before the 885 main block), output names renamed (I/O only)
    blob = _h887.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()
    assert blob == BASE_BLOB887 and _h887.sha256(raw).hexdigest() == BASE_SHA887, ('BASE_885_LOCK', blob)
    text = raw.decode('utf-8')
    assert text.count(BASE_CUT887) == 1, 'BASE_885_CUT'
    defs = text[:text.index(BASE_CUT887)]
    for old, new, n in BASE_RENAMES887:
        assert defs.count(old) == n, ('BASE_885_RENAME', old, defs.count(old))
        defs = defs.replace(old, new)
    _a887.parse(defs)
    return defs, {'url': BASE_URL887, 'git_blob': blob, 'sha256': BASE_SHA887, 'definition_lines': defs.count('\n')}


try:
    with _u887.urlopen(_u887.Request(BASE_URL887, headers={'User-Agent': 'AKBASCORE-TEST887'}), timeout=240) as _r:
        BASE887, BASE_INFO887 = base_definitions887(_r.read())
except BaseException as _exc887:
    import traceback as _tb887
    _p887 = '/content/TEST887_PRE_BASE_ERROR_%s.txt' % _t887.strftime('%Y%m%dT%H%M%SZ', _t887.gmtime())
    try:
        with open(_p887, 'w', encoding='utf-8') as _f887: _f887.write(_tb887.format_exc())
    except OSError: _p887 = 'NOT_WRITTEN'
    print('TEST887 PRE-BASE ERROR (nothing loaded):', type(_exc887).__name__, _exc887, '| traceback:', _p887)
    raise
exec(compile(BASE887, '885.py:definitions', 'exec'), globals())     # engine download + console capture + 885 definitions
print('TEST887 BASE', _j887.dumps(BASE_INFO887, sort_keys=True))
CART_ROOT883 = '/content/TEST887_EPISODE_CARTRIDGES'                 # episode-only cartridges (never bank cards), deleted

# ============================ sealed design (fixed before the model is loaded) ============================
ACTIONS887 = ('ADVANCE', 'ACQUIRE', 'REJECT', 'BACKTRACK', 'ACCEPT', 'STOP')
WORLDS887 = ('10', '09')                     # = first two of select_worlds883() (885 salt rule; checked at G0)
CELLS887 = tuple((w, c) for w in WORLDS887 for c in ('MISSING', 'FORK'))
DONOR887 = {'10': '09', '09': '10'}          # WRONG C of world w = real observation of the other world, same condition, same step
ARMS887 = ('NONE', 'TRUE', 'WRONG')          # whose reading is executed by the locked execute866
TAU887 = 0.05                                # sealed total-variation threshold over the six normalized action probabilities
MIN_PAIRS887 = 4                             # fewer valid paired points: CONTENT is never PASS or FAIL
EXEC_ALLOW887 = {'episode887': ('execute866', 'hop865', 'mount865')}
RUNTIME887 = ('tv887', 'finite887', 'none887', 'read887', 'write_pair887', 'negatives887', 'episode887')
PREREG887 = {
    'test': 'TEST887 minimal physical cartridge probe', 'base': BASE_INFO887, 'engine': ENGINE_INFO883, 'head_locks': HEAD883,
    'question': 'physical write / SSD / independent reload / native read of a CUT3/H3/KV cartridge, and whether its CONTENT '
                'changes the next native CAR action distribution at an identical decision state',
    'conditions_at_each_decision_t>=2': {'NONE': '[B] xcar878 blind=() (== native control_step867 reading, bitwise, else block)',
                                         'TRUE': '[B][E_true] xcar878 blind=()', 'WRONG': '[B][E_wrong] xcar878 blind=()'},
    'cartridges': 'E = [X2][A][C] by the locked writer (write_experience883 -> write_exp878) from two independent '
                  'prepare_experience883 of the same native step; TRUE C = the real next observation (hop + evidence rows); '
                  'WRONG C = the real observation of world DONOR887[w], same condition, same step index (last step if shorter), '
                  'fitted to the TRUE row counts by the locked shape_match867 (truncate / pad with MUE845)',
    'geometry_gate': 'TRUE and WRONG: equal body_tokens, equal spans, pre_C_seal equal (X2/A rows bitwise), C rows differ, '
                     'different files; otherwise TECHNICAL_BLOCK',
    'null_controls': ['NONE == native reading bitwise at every step of TRUE / WRONG episodes',
                      'first paired point of every TRUE / WRONG episode: TRUE re-read after an independent SSD reload must be '
                      'bitwise identical (same_reading881), otherwise TECHNICAL_BLOCK (measurement failure, never an exclusion)',
                      'TRUE and WRONG reads: equal model-call counts', 'every reading finite (no NaN / Inf), six actions'],
    'physical_negatives': 'first TRUE cartridge of the run: byte-corrupted copy and wrong tensor SHA must both be refused by '
                          'the locked load_exp878',
    'cells': ['%s_%s' % c for c in CELLS887], 'arms': ARMS887, 'horizon': HORIZON883, 'tau_tv': TAU887,
    'min_pairs': MIN_PAIRS887,
    'verdict': {
        'PHYSICAL_READ': 'PASS: >=1 TRUE and >=1 WRONG read, every write / read / append / parity / geometry / negative gate '
                         'passed, every episode restored and isolated, bank / MEMNULL / weights / hooks unchanged after the run. '
                         'FAIL: a physical gate failed or the post-run integrity failed or was not reached. NOT_RUN: no read',
        'CONTENT_CAUSAL_EFFECT': 'only with TECHNICAL_STATUS COMPLETE and PHYSICAL_READ PASS, over >= MIN_PAIRS paired points. '
                                 'PASS: TV(TRUE,WRONG) >= tau in both worlds and the argmax action of TRUE != WRONG in at least '
                                 'one point. FAIL: TV(TRUE,WRONG) < tau everywhere and no action difference. Else INCONCLUSIVE',
        'OUTCOME_BENEFIT': 'only with COMPLETE and the full 4 cells x 3 arms with natural ends and binary Y. PASS: both FORK cells '
                           'Y_TRUE=1, Y_NONE=0, Y_WRONG=0 and both MISSING cells Y_TRUE >= Y_NONE. Else FAIL. Incomplete: NOT_MEASURED',
        'presence_effect': 'TV(TRUE,NONE) reported separately; a presence effect without a content effect is not a content claim'},
    'not_claimed': ['learning (persistent, predictive)', 'generalization beyond 2 worlds x 2 conditions', 'that TRUE C carries '
                    'information absent from X (C also appears in the current state segments)', 'GPU success before the run'],
    'budget': '75 min from the first line of this cell (T_CELL887): guard883 before every step, every read and every episode, '
              'admit883 before every episode after the first; a budget stop never yields PASS for CONTENT or OUTCOME'}
PREREG_SHA887 = _h887.sha256(_j887.dumps(PREREG887, sort_keys=True, default=str).encode()).hexdigest()
STATE887 = {'status': 'NOT_STARTED', 'technical_status': None, 'gates': {}, 'source': {}, 'episodes': [], 'pairs': [],
            'negatives': None, 'physical_failure': None, 'post_run': None, 'scores': None, 'verdict': None, 'error': None,
            'traceback': None, 'artifact_errors': []}


class Gate887(Exception):
    pass


def gate887(name, status, **info):
    rec = dict(status=status, wall_s=round(_t887.perf_counter() - T_CELL887, 1), **info)
    STATE887['gates'][name] = rec
    print('T887 GATE', name, status, _j887.dumps(rec, sort_keys=True, default=str)[:900], flush=True)
    if status != 'PASS': raise Gate887('%s %s' % (name, status))


# ============================ pure functions (CPU-testable) ============================
def body_lock887(src):
    # first line '# TEST887 BODY-SHA256 <hex>' locks every following byte (CRLF -> LF, trailing whitespace of the cell ignored):
    # appended code, an edited line or code above the lock line all fail
    if not isinstance(src, str): return {'ok': False, 'why': 'NO_SOURCE'}
    s = src.replace('\r\n', '\n')
    head, _, rest = s.partition('\n')
    m = _r887.fullmatch(r'# TEST887 BODY-SHA256 ([0-9a-f]{64})', head)
    if not m: return {'ok': False, 'why': 'NO_LOCK_LINE_ON_LINE_1'}
    body = rest.rstrip() + '\n'
    got = _h887.sha256(body.encode('utf-8')).hexdigest()
    return {'ok': got == m.group(1), 'why': None if got == m.group(1) else 'BODY_HASH_MISMATCH', 'expected': m.group(1),
            'measured': got, 'lines': body.count('\n') + 1}


def tv887(a, b):
    return 0.5 * sum(abs(float(a['normalized'][w]) - float(b['normalized'][w])) for w in ACTIONS887)


def finite887(r):
    import math
    try:
        if sorted(s['word'] for s in r['scores']) != sorted(ACTIONS887) or set(r['normalized']) != set(ACTIONS887): return False
        vals = [x for s in r['scores'] for x in s['token_logps']] + [s['sequence_logp'] for s in r['scores']] + \
            [r['normalized'][w] for w in ACTIONS887] + [r['mass']]
        return all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in vals)
    except (KeyError, TypeError):
        return False


def verdict887(status, physical, pairs, scores):
    # physical: dict of boolean physical facts (None = not reached); pairs: paired points; scores: {episode_id: {'Y', 'end'}}
    v = {'TECHNICAL_STATUS': status, 'reasons': {}}
    if physical.get('reads_true', 0) == 0 or physical.get('reads_wrong', 0) == 0:
        v['PHYSICAL_READ'] = 'FAIL' if physical.get('physical_failure') else 'NOT_RUN'
    else:
        facts = {k: physical.get(k) for k in ('no_physical_failure', 'negatives_refused', 'post_run_integrity', 'cleanup_clean')}
        v['PHYSICAL_READ'] = 'PASS' if all(x is True for x in facts.values()) else 'FAIL'
        v['reasons']['physical_facts'] = facts
    ok_run = status == 'COMPLETE' and v['PHYSICAL_READ'] == 'PASS'
    worlds = {p['world'] for p in pairs}
    eff_worlds = {p['world'] for p in pairs if p['tv_true_wrong'] >= TAU887}
    act_diff = [p for p in pairs if p['action_true'] != p['action_wrong']]
    v['reasons']['content'] = {'pairs': len(pairs), 'worlds_with_pairs': sorted(worlds), 'worlds_tv_ge_tau': sorted(eff_worlds),
                               'action_differs_points': len(act_diff),
                               'max_tv_true_wrong': max((p['tv_true_wrong'] for p in pairs), default=None)}
    if not ok_run or len(pairs) < MIN_PAIRS887:
        v['CONTENT_CAUSAL_EFFECT'] = 'INCONCLUSIVE'
    elif set(WORLDS887) <= eff_worlds and act_diff:
        v['CONTENT_CAUSAL_EFFECT'] = 'PASS'
    elif not eff_worlds and not act_diff:
        v['CONTENT_CAUSAL_EFFECT'] = 'FAIL'
    else:
        v['CONTENT_CAUSAL_EFFECT'] = 'INCONCLUSIVE'
    v['presence_effect_points'] = sum(1 for p in pairs if p['tv_true_none'] >= TAU887)
    Y = {'%s_%s_%s' % (a, w, c): (scores or {}).get('%s_%s_%s' % (a, w, c), {}).get('Y') for (w, c) in CELLS887 for a in ARMS887}
    v['reasons']['Y'] = Y
    if not ok_run or any(y not in (0, 1) for y in Y.values()):
        v['OUTCOME_BENEFIT'] = 'NOT_MEASURED'
    else:
        fork = all(Y['TRUE_%s_FORK' % w] == 1 and Y['NONE_%s_FORK' % w] == 0 and Y['WRONG_%s_FORK' % w] == 0 for w in WORLDS887)
        miss = all(Y['TRUE_%s_MISSING' % w] >= Y['NONE_%s_MISSING' % w] for w in WORLDS887)
        v['OUTCOME_BENEFIT'] = 'PASS' if fork and miss else 'FAIL'
    return v


# ============================ runtime (model) ============================
def none887(env, B, X, native):
    # no cartridge: the explicit read path on [B]; must equal the native control_step867 reading bitwise (no forcing)
    r = xcar878(env, B, X, (), False); ffe883(int(X.shape[0]) + cont_tokens881(), 80, 'decision_read')
    if not finite887(r): raise Gate883('PHYSICAL_NONFINITE_NONE_READING')
    if not same_reading881(r, native): raise Gate883('PHYSICAL_NONE_PARITY explicit=%s native=%s' % (r['action'], native['action']))
    return r


def read887(env, B, entry, card, X, step, ep_id, cdir, b_tokens, first):
    # one physical read: manifest contract, SSD reload (file + tensor SHA, locked), native append, explicit read on [B][E]
    why = read_contract883(entry, card, step, ep_id, cdir)
    if why: raise Gate883('PHYSICAL_READ_CONTRACT %s t%d: %s' % (ep_id, step, why))
    n0 = length873(env, B)
    if n0 != b_tokens: raise Gate883('PHYSICAL_B_LENGTH %d != %d' % (n0, b_tokens))
    seal0 = full_seal881(B)['all'] if first else None
    try:
        cp = load_exp878(env, entry)
    except Persist878 as exc:
        raise Gate883('PHYSICAL_RELOAD %s t%d: %s' % (ep_id, step, exc))
    q = int(cp['body_tokens']); g = append_exp878(env, B, cp); ffe883(q, 80, 'experience_mount')
    rec = {'cartridge': entry['id'], 'n_exact': length873(env, g) == n0 + q,
           'prefix_rows_bitwise': bool(torch.equal(g[0][0][:, :, :n0], B[0][0]) and torch.equal(g[-1][1][:, :, :n0], B[-1][1]))}
    if first:
        gx = xappend878(env, B, cp, ()); ffe883(q, 80, 'experience_mount_parity')
        rec['explicit_equals_native_append_bitwise'] = all(torch.equal(a[t], b[t]) for a, b in zip(g, gx) for t in (0, 1)); del gx
        rec['B_full_seal_unchanged'] = full_seal881(B)['all'] == seal0
    c0 = int(env['CALLS849'])
    reading = xcar878(env, g, X, (), False); ffe883(int(X.shape[0]) + cont_tokens881(), 80, 'decision_read')
    rec['calls'] = int(env['CALLS849']) - c0
    del g, cp
    rec['finite'] = finite887(reading)
    bad = sorted(k for k, x in rec.items() if isinstance(x, bool) and not x)
    if bad: raise Gate883('PHYSICAL_READ_GATES %s t%d %s: %s' % (ep_id, step, entry['id'], bad))
    return reading, rec


def write_pair887(env, pend, c_rows, e_rows, donor_obs, step, cdir, key, prev_id):
    # TRUE and WRONG cartridges from the same native step (two independent prepare_experience883); only C differs
    if not donor_obs: raise Gate883('NO_DONOR_OBSERVATION %s' % key['episode_id'])
    dc, de = donor_obs[min(step, len(donor_obs)) - 1]
    cw, ew = shape_match867(env, dc, int(c_rows.shape[0])), shape_match867(env, de, int(e_rows.shape[0]))
    meta = dict(key, step_written=step - 1, episode_prev_cartridge=prev_id)
    tw = _t887.perf_counter()
    try:
        et, rt = write_experience883(env, pend[0], c_rows, e_rows, cdir, dict(meta, cartridge_role='TRUE'))
        ew_, rw = write_experience883(env, pend[1], cw, ew, cdir, dict(meta, cartridge_role='WRONG',
                                                                      donor_world=DONOR887[str(key['world_index']).zfill(2)]))
    except Gate883 as exc:
        raise Gate883('PHYSICAL_WRITE %s' % exc)
    geo = {'body_tokens_equal': rt['body_tokens'] == rw['body_tokens'],
           'spans_equal': et['provenance']['spans_body'] == ew_['provenance']['spans_body'],
           'X2_A_rows_bitwise_equal': rt['pre_C_seal'] == rw['pre_C_seal'],
           'C_rows_differ': (et['provenance']['C_rows_sha256'], et['provenance']['E_rows_sha256']) !=
                            (ew_['provenance']['C_rows_sha256'], ew_['provenance']['E_rows_sha256']),
           'different_files': rt['sha256'] != rw['sha256'] and et['file'] != ew_['file']}
    if not all(geo.values()): raise Gate883('PHYSICAL_GEOMETRY_MATCH %s' % sorted(k for k, x in geo.items() if not x))
    return {'true': (et, rt), 'wrong': (ew_, rw), 'geometry': geo, 'write_s': round(_t887.perf_counter() - tw, 3)}


def negatives887(env, entry):
    # the locked loader must refuse a byte-corrupted copy and a wrong tensor SHA; the intact file reloads
    bad = entry['file'] + '.corrupt'
    _s887.copyfile(entry['file'], bad)
    with open(bad, 'r+b') as f:
        f.seek(_o887.path.getsize(bad) // 2); b = f.read(1); f.seek(-1, 1); f.write(bytes([b[0] ^ 0xFF]))
    out = {}
    try: load_exp878(env, dict(entry, file=bad)); out['corrupt_file_refused'] = False
    except Persist878 as exc: out['corrupt_file_refused'] = 'FILE_SHA' in str(exc)
    finally: _o887.remove(bad)
    try: load_exp878(env, dict(entry, tensor_sha={'h': '0' * 64, 'lower': []})); out['wrong_tensor_sha_refused'] = False
    except Persist878 as exc: out['wrong_tensor_sha_refused'] = 'TENSOR_SHA' in str(exc)
    g = load_exp878(env, entry); out['intact_reload_ok'] = g is not None; del g
    if not all(out.values()): raise Gate883('PHYSICAL_NEGATIVES %s' % out)
    return out


def episode887(env, spec, arm, ep_id, horizon, donor_obs):
    # one natural episode; arm selects whose reading is executed (NONE = native, TRUE, WRONG); TRUE / WRONG episodes also
    # record the paired NONE / TRUE / WRONG readings at every decision with a cartridge. Executor: locked execute866 only.
    key = {'world_index': int(spec['world_index']), 'condition': spec['condition'], 'arm': arm, 'episode_id': ep_id}
    ctx = {'spec': spec, 'arm': 'NO_FEEDBACK', 'M': list(spec['initial']), 'memx': None, 'path': [], 'prev_state': None,
           'own_states': [], 'events': [], 'mount_records': [], 'acquisitions': 0, 'rejections': 0, 'addresses': 0,
           'steps': 0, 'hops': 0, 'donor_item': None}
    cdir = _o887.path.join(CART_ROOT883, ep_id)
    out = dict(key, item=spec['item'], steps=[], pairs=[], obs=[], end=None, accepted=None, error=None, cartridges=[],
               wrong_cartridges=[])
    pend, last, t0, calls0, initial_seal, interrupted, step_sum = None, None, _t887.perf_counter(), int(env['CALLS849']), None, None, 0.0
    try:
        try:
            _o887.makedirs(cdir, exist_ok=False)
            q = env['QTEXT841'][spec['qid']]; pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
            ctx['memx'], mount = mount865(env, ctx['M'], 'TEST887_L0_%s_%s' % (arm, spec['item'])); ctx['mount_records'].append(mount)
            initial_seal = prefix_seals865(env, ctx['memx'])
            while out['end'] is None:
                if ctx['steps'] >= horizon: out['end'] = 'HORIZON_%d' % horizon; break
                if not budget_left865(env, STEP_CALLS867): out['end'] = 'RESOURCE_BUDGET'; break
                guard883('%s_t%d' % (ep_id, ctx['steps'] + 1)); ts = _t887.perf_counter(); sc0 = int(env['CALLS849'])
                k = len(ctx['path']); pointer = None if k == 0 else ctx['path'][-1]['rows']
                h, kind = hop865(env, ctx['memx'], spec['qid'], k, pointer); ctx['hops'] += 1
                ctx['events'].append({'type': 'HOP', 'k': k, 'kind_logged_only': kind, 'raw': h['text'], 'mounted': list(ctx['M']),
                                      'decision_source': 'MODEL'})
                if kind == 'EMPTY_OUTPUT': out['end'] = 'NATIVE_EMPTY_OUTPUT'; break
                feedback, fb_info = feedback867(env, ctx)
                control, record, state = control_step867(env, ctx, h, pointer, feedback)
                if control is None: out['end'] = 'NATIVE_EMPTY_STATE'; break
                ctx['steps'] += 1; t = ctx['steps']; B = ctx['memx']; X, _ = env['make_x851'](pre, state['segments'], post)
                c_rows, e_rows = state['segments'][0][1], state['segments'][1][1]
                st = dict(key, step=t, hop=h['text'], state_sha256=record['state_sha256'], X_sha256=tsha881(X),
                          B_tokens=length873(env, B), native=reading_view883(record['reading']))
                if not finite887(record['reading']): raise Gate883('PHYSICAL_NONFINITE_NATIVE_READING %s t%d' % (ep_id, t))
                cache = None
                if arm == 'NONE':
                    reading = record['reading']; out['obs'].append((c_rows, e_rows))
                else:
                    cache = env['cache_build'](list(B)); nat = car873(env, cache, X); ffe883(int(X.shape[0]) + cont_tokens881(), 80, 'native_read')
                    if not same_reading881(nat, record['reading']): raise Gate883('PHYSICAL_X_PARITY car873 != control_step867 %s t%d' % (ep_id, t))
                    r_none = none887(env, B, X, record['reading'])
                    reading = r_none
                    if pend is not None:
                        guard883('%s_t%d_pair' % (ep_id, t))
                        last = write_pair887(env, pend, c_rows, e_rows, donor_obs, t, cdir, key,
                                             out['cartridges'][-1]['id'] if out['cartridges'] else None)
                        pend = None
                        out['cartridges'].append(last['true'][1]); out['wrong_cartridges'].append(last['wrong'][1])
                        if STATE887['negatives'] is None: STATE887['negatives'] = negatives887(env, last['true'][0])
                        first = not out['pairs']; tr = _t887.perf_counter()
                        r_true, rt = read887(env, B, last['true'][0], last['true'][1], X, t, ep_id, cdir, st['B_tokens'], first)
                        r_wrong, rw = read887(env, B, last['wrong'][0], last['wrong'][1], X, t, ep_id, cdir, st['B_tokens'], first)
                        if rt['calls'] != rw['calls']: raise Gate883('PHYSICAL_CALL_PARITY TRUE %s != WRONG %s' % (rt['calls'], rw['calls']))
                        pair = dict(key, world='%02d' % key['world_index'], step=t, action_none=r_none['action'],
                                    action_true=r_true['action'], action_wrong=r_wrong['action'],
                                    tv_true_wrong=tv887(r_true, r_wrong), tv_true_none=tv887(r_true, r_none),
                                    tv_wrong_none=tv887(r_wrong, r_none),
                                    p_none=dict(r_none['normalized']), p_true=dict(r_true['normalized']), p_wrong=dict(r_wrong['normalized']),
                                    cartridge_true=rt['cartridge'], cartridge_wrong=rw['cartridge'],
                                    body_tokens=int(last['true'][1]['body_tokens']), geometry=last['geometry'], read_true=rt, read_wrong=rw)
                        if first:
                            r_rep, _ = read887(env, B, last['true'][0], last['true'][1], X, t, ep_id, cdir, st['B_tokens'], False)
                            pair['repeat_reload_bitwise'] = same_reading881(r_true, r_rep); pair['tv_repeat'] = tv887(r_true, r_rep)
                            if not pair['repeat_reload_bitwise']: raise Gate883('PHYSICAL_REPEAT_NOT_BITWISE %s t%d tv=%.3g' % (ep_id, t, pair['tv_repeat']))
                        out['pairs'].append(pair)
                        with open(ROOT864 / 'pairs.jsonl', 'a', encoding='utf-8') as f: f.write(_j887.dumps(jsafe878(pair), sort_keys=True) + '\n')
                        st['exp_op'] = exp_op883(ep_id, t, arm, int(last['true'][1]['body_tokens']), last['write_s'],
                                                 round(_t887.perf_counter() - tr, 3))
                        reading = r_true if arm == 'TRUE' else r_wrong
                        last = None
                action = reading['action']
                st.update({'reading': reading_view883(reading), 'action': action, 'decision_source': 'MODEL_CAR_READING_' + arm,
                           'differs_from_native': action != record['action']})
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
                st['seconds'] = round(_t887.perf_counter() - ts, 3); st['calls'] = int(env['CALLS849']) - sc0; step_sum += st['seconds']
                out['steps'].append(st)
                with open(ROOT864 / 'decisions.jsonl', 'a', encoding='utf-8') as f: f.write(_j887.dumps(jsafe878(st), sort_keys=True) + '\n')
                line883('STEP', ep_id, 't=%d' % t, 'hop=%r' % h['text'], 'exec=%s' % action, 'native=%s' % record['action'],
                        'pair=%s' % ('%s/%s/%s tv_tw=%.3f' % (out['pairs'][-1]['action_none'], out['pairs'][-1]['action_true'],
                                     out['pairs'][-1]['action_wrong'], out['pairs'][-1]['tv_true_wrong'])
                                     if out['pairs'] and out['pairs'][-1]['step'] == t else '-'),
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
            if str(exc).startswith('PHYSICAL_'): STATE887['physical_failure'] = str(exc)[:500]
        except Exception as exc:
            out['end'], out['error'], out['traceback'] = 'EXECUTION_ERROR', '%s: %s' % (type(exc).__name__, exc), traceback.format_exc()
        except BaseException as exc:
            out['end'], out['error'], interrupted = 'INTERRUPTED', '%s: %s' % (type(exc).__name__, exc), exc
    finally:
        pend = last = None
        cleanup883(env, ctx, out, spec, arm, cdir, initial_seal, interrupted is not None)
    contract = event_contract883(ctx['events'])
    controls = [e for e in ctx['events'] if e['type'] == 'CONTROL']
    exp_cards = expected_cartridges883(ctx['steps'], out['end'], horizon) if arm != 'NONE' else 0
    out.update({'final_mounted': list(ctx['M']), 'n_steps': ctx['steps'], 'actions': [c['action'] for c in controls],
                'effects': [e['effect'] for e in ctx['events'] if e['type'] == 'EFFECT'], 'acquisitions': ctx['acquisitions'],
                'event_contract': {x: contract[x] for x in ('ok', 'problems', 'controls', 'effects')},
                'executed_equals_reading': bool(contract['ok'] and [c['action'] for c in controls] == [s['action'] for s in out['steps']]),
                'cartridges_expected': exp_cards, 'mount_integrity': mount_ok883(ctx['mount_records']),
                'cartridge_cardinality_ok': exp_cards is not None and len(out['cartridges']) == exp_cards == len(out['wrong_cartridges'])
                                            and len(out['pairs']) == exp_cards,
                'seconds': round(_t887.perf_counter() - t0, 1), 'calls': int(env['CALLS849']) - calls0})
    out['overhead_s'] = round(out['seconds'] - step_sum, 1)
    STATE883['budget']['episode_overhead_s'].append(out['overhead_s'])
    line883('EPISODE', ep_id, 'end=%s' % out['end'], 'actions=%s' % '>'.join(out['actions']), 'accepted=%r' % out['accepted'],
            'pairs=%d' % len(out['pairs']), 'cards=%d+%d/%s' % (len(out['cartridges']), len(out['wrong_cartridges']), exp_cards),
            'restore=%s' % out['exact_restore_vs_first_mount'], 'contract=%s' % contract['ok'], 's=%.0f' % out['seconds'],
            '' if not out['error'] else 'ERROR=' + str(out['error'])[:300])
    if out.get('traceback'): short864(out['traceback'])
    rec = {x: y for x, y in out.items() if x not in ('steps', 'obs', 'pairs')}
    with open(ROOT864 / 'episodes.jsonl', 'a', encoding='utf-8') as f: f.write(_j887.dumps(jsafe878(rec), sort_keys=True) + '\n')
    STATE887['episodes'].append(out); STATE887['pairs'] += out['pairs']
    if interrupted is not None: raise interrupted
    if out['end'] in ('BUDGET_STOP', 'RESOURCE_BUDGET'): raise Budget883(out['error'] or out['end'])
    natural_empty = out['end'] in ('NATIVE_EMPTY_OUTPUT', 'NATIVE_EMPTY_STATE') and not controls
    bad = {'end': out['end'] in ('TECHNICAL_BLOCK', 'EXECUTION_ERROR', 'PHYSICAL_CONTEXT_LIMIT'),
           'restore': out['exact_restore_vs_first_mount'] is not True, 'mount': not out['mount_integrity'],
           'contract': not (out['executed_equals_reading'] or natural_empty), 'isolated': not out['isolated_after_episode'],
           'cleanup': bool(out['cleanup_errors']), 'cardinality': not (out['cartridge_cardinality_ok'] or natural_empty)}
    if any(bad.values()):
        phys = any(bad[x] for x in ('restore', 'mount', 'isolated', 'cleanup', 'cardinality'))
        raise Gate883('%sEPISODE_INTEGRITY %s %s err=%s' % ('PHYSICAL_' if phys else '', ep_id, sorted(x for x, y in bad.items() if y), str(out['error'])[:300]))
    return out


# ============================ G0 source capture + CPU selftests of the new layer ============================
def capture887():
    try:
        src, how = get_ipython().history_manager.input_hist_raw[-1], 'IPYTHON_CURRENT_CELL'
    except NameError:
        src, how = (open(__file__, encoding='utf-8').read() if '__file__' in globals() else None), 'FILE'
    lock = body_lock887(src)
    if not lock['ok']: raise Gate887('SOURCE_SELF_LOCK %s (paste the parts into ONE cell, in order, unchanged)' % lock)
    tree = _a887.parse(src)
    funcs = {n.name: n for n in tree.body if isinstance(n, _a887.FunctionDef)}
    for name, node in funcs.items(): scan883(node, EXEC_ALLOW887.get(name, ()))
    missing = sorted(set(RUNTIME887) - set(funcs))
    if missing: raise Gate887('RUNTIME_FUNCTIONS_MISSING %s' % missing)
    for name in RUNTIME887: oracle_scan883(funcs[name])
    count = lambda f: sum(1 for n in _a887.walk(tree) if isinstance(n, _a887.Call) and getattr(n.func, 'id', None) == f)
    facts = {'reproduce_pre859859_calls': count('reproduce_pre859859'), 'execute866_calls': count('execute866'),
             'input_calls': count('input'), 'rearm_budget865_calls': count('rearm_budget865')}
    if facts != {'reproduce_pre859859_calls': 1, 'execute866_calls': 1, 'input_calls': 0, 'rearm_budget865_calls': 1}:
        raise Gate887('SOURCE_FACTS %s' % facts)
    raw = src.encode('utf-8')
    (ROOT864 / 'TEST887.py').write_bytes(raw)
    STATE887['source'] = {'how': how, 'executed_cell_git_blob': git_blob864(raw), 'executed_cell_sha256': sha256_bytes864(raw),
                          'body_lock': lock, 'facts': facts, 'firewall': 'PASS', 'oracle_firewall': 'PASS %d' % len(RUNTIME887)}
    STATE883['source'] = {'executed_cell_git_blob': STATE887['source']['executed_cell_git_blob']}   # cartridge provenance field
    json_write864('TEST887_source_manifest.json', dict(STATE887['source'], base=BASE_INFO887, engine=ENGINE_INFO883, head=HEAD883,
                                                       prereg_sha256=PREREG_SHA887, before_model_load=True))
    print('T887 SOURCE blob=%s sha256=%s body_lock=%s' % (STATE887['source']['executed_cell_git_blob'],
                                                         STATE887['source']['executed_cell_sha256'], lock['measured']), flush=True)


def st887():
    def rd(p, lp=-0.5):
        return {'action': max(p, key=p.get), 'mass': 0.9, 'normalized': dict(p),
                'scores': [{'word': w, 'token_logps': [lp], 'sequence_logp': lp} for w in ACTIONS887]}
    u = {w: 1 / 6 for w in ACTIONS887}; a = dict(u, ADVANCE=0.5, ACQUIRE=0.1); b = dict(u, ACQUIRE=0.5, ADVANCE=0.1)
    r = {}
    r['tv_zero_on_equal'] = tv887(rd(a), rd(a)) == 0.0
    r['tv_value'] = abs(tv887(rd(a), rd(b)) - 0.4) < 1e-12
    r['finite_ok'] = finite887(rd(a))
    for nm, bad in (('nan', float('nan')), ('pinf', float('inf')), ('ninf', float('-inf'))):
        x = rd(a); x['scores'][2]['token_logps'] = [bad]; y = rd(a); y['normalized']['STOP'] = bad
        r['nonfinite_%s_refused' % nm] = not finite887(x) and not finite887(y)
    m = rd(a); m['scores'] = m['scores'][:5]; r['missing_action_refused'] = not finite887(m)
    s = rd(a); s['normalized']['STOP'] = None; r['none_value_refused'] = not finite887(s)
    body = 'x = 1\nprint(x)\n'; lk = '# TEST887 BODY-SHA256 ' + _h887.sha256(body.encode()).hexdigest()
    r['lock_exact_ok'] = body_lock887(lk + '\n' + body)['ok']
    r['lock_trailing_whitespace_ok'] = body_lock887(lk + '\r\n' + body.replace('\n', '\r\n') + '\n \n\t')['ok']
    r['lock_suffix_refused'] = not body_lock887(lk + '\n' + body + 'print("extra")\n')['ok']
    r['lock_edit_refused'] = not body_lock887(lk + '\n' + body.replace('1', '2'))['ok']
    r['lock_prefix_refused'] = not body_lock887('import os\n' + lk + '\n' + body)['ok']
    r['lock_missing_refused'] = not body_lock887(body)['ok'] and not body_lock887(None)['ok']
    # verdict rules
    phys = {'reads_true': 4, 'reads_wrong': 4, 'no_physical_failure': True, 'negatives_refused': True, 'post_run_integrity': True,
            'cleanup_clean': True}
    def pr(w, tvw, at, aw, tvn=0.0):
        return {'world': w, 'tv_true_wrong': tvw, 'tv_true_none': tvn, 'action_true': at, 'action_wrong': aw}
    Yf = lambda tf, nf, wf, tm=1, nm=1: {'%s_%s_%s' % (arm, w, c): {'Y': {('TRUE', 'FORK'): tf, ('NONE', 'FORK'): nf,
                                         ('WRONG', 'FORK'): wf, ('TRUE', 'MISSING'): tm, ('NONE', 'MISSING'): nm,
                                         ('WRONG', 'MISSING'): 0}[(arm, c)]} for (w, c) in CELLS887 for arm in ARMS887}
    P = [pr('10', 0.3, 'ACQUIRE', 'ADVANCE'), pr('10', 0.01, 'ADVANCE', 'ADVANCE'), pr('09', 0.2, 'STOP', 'STOP'),
         pr('09', 0.0, 'ADVANCE', 'ADVANCE')]
    v = verdict887('COMPLETE', phys, P, Yf(1, 0, 0))
    r['verdict_pass'] = (v['PHYSICAL_READ'], v['CONTENT_CAUSAL_EFFECT'], v['OUTCOME_BENEFIT']) == ('PASS', 'PASS', 'PASS')
    Z = [pr('10', 0.01, 'ADVANCE', 'ADVANCE'), pr('10', 0.0, 'ACQUIRE', 'ACQUIRE'), pr('09', 0.02, 'STOP', 'STOP'),
         pr('09', 0.0, 'ADVANCE', 'ADVANCE', 0.4)]
    v = verdict887('COMPLETE', phys, Z, Yf(0, 0, 0))
    r['verdict_content_fail_presence_only'] = v['CONTENT_CAUSAL_EFFECT'] == 'FAIL' and v['presence_effect_points'] == 1 and \
        v['OUTCOME_BENEFIT'] == 'FAIL'
    r['verdict_one_world_inconclusive'] = verdict887('COMPLETE', phys, P[:2] + Z[2:], Yf(1, 0, 0))['CONTENT_CAUSAL_EFFECT'] == 'INCONCLUSIVE'
    r['verdict_tv_without_action_change_inconclusive'] = verdict887('COMPLETE', phys, [dict(p, action_wrong=p['action_true']) for p in P],
                                                                    Yf(1, 0, 0))['CONTENT_CAUSAL_EFFECT'] == 'INCONCLUSIVE'
    r['verdict_too_few_pairs_inconclusive'] = verdict887('COMPLETE', phys, P[:3], Yf(1, 0, 0))['CONTENT_CAUSAL_EFFECT'] == 'INCONCLUSIVE'
    v = verdict887('BUDGET_STOP', phys, P, Yf(1, 0, 0))
    r['verdict_budget_stop_never_pass'] = v['CONTENT_CAUSAL_EFFECT'] == 'INCONCLUSIVE' and v['OUTCOME_BENEFIT'] == 'NOT_MEASURED'
    v = verdict887('COMPLETE', dict(phys, negatives_refused=False), P, Yf(1, 0, 0))
    r['verdict_physical_fail_blocks_content'] = v['PHYSICAL_READ'] == 'FAIL' and v['CONTENT_CAUSAL_EFFECT'] == 'INCONCLUSIVE'
    v = verdict887('COMPLETE', dict(phys, post_run_integrity=None), P, Yf(1, 0, 0))
    r['verdict_post_run_not_reached_fail'] = v['PHYSICAL_READ'] == 'FAIL'
    r['verdict_no_reads_not_run'] = verdict887('TECHNICAL_BLOCK', {'reads_true': 0, 'reads_wrong': 0}, [], {})['PHYSICAL_READ'] == 'NOT_RUN'
    sc = Yf(1, 0, 0); sc['WRONG_09_FORK'] = {'Y': None}
    r['verdict_missing_Y_not_measured'] = verdict887('COMPLETE', phys, P, sc)['OUTCOME_BENEFIT'] == 'NOT_MEASURED'
    r['verdict_wrong_also_succeeds_fail'] = verdict887('COMPLETE', phys, P, Yf(1, 0, 1))['OUTCOME_BENEFIT'] == 'FAIL'
    r['verdict_missing_harm_fail'] = verdict887('COMPLETE', phys, P, Yf(1, 0, 0, tm=0, nm=1))['OUTCOME_BENEFIT'] == 'FAIL'
    # firewall facts on the new runtime layer
    for nm, src in (('hook', 'def f(m):\n    m.register_forward_hook(1)\n'), ('backward', 'def f(l):\n    l.backward()\n'),
                    ('executor', 'def f(e):\n    execute866(e, 1, 2, 3, 4, 5)\n')):
        try: scan883(_a887.parse(src).body[0]); r['firewall_%s_refused' % nm] = False
        except AssertionError: r['firewall_%s_refused' % nm] = True
    try: oracle_scan883(_a887.parse("def f(env):\n    return env['supported851']\n").body[0]); r['oracle_key_refused'] = False
    except AssertionError: r['oracle_key_refused'] = True
    r['worlds_rule'] = tuple(select_worlds883()[:2]) == WORLDS887
    r['donor_is_other_world'] = all(DONOR887[w] != w and DONOR887[w] in WORLDS887 for w in WORLDS887)
    r['prereg_sha_stable'] = PREREG_SHA887 == _h887.sha256(_j887.dumps(PREREG887, sort_keys=True, default=str).encode()).hexdigest()
    try:   # locked shape_match867 (donor row fitting): truncate / pad with MUE845 (needs torch; NOT_RUN on a host without it)
        import torch as _tt
        env_ = {'MUE845': _tt.full((4,), 7.0)}; rows = _tt.arange(12, dtype=_tt.float32).reshape(3, 4)
        r['donor_fit_truncate'] = _tt.equal(shape_match867(env_, rows, 2), rows[:2])
        p_ = shape_match867(env_, rows, 5)
        r['donor_fit_pad_mue'] = tuple(p_.shape) == (5, 4) and _tt.equal(p_[:3], rows) and bool((p_[3:] == 7.0).all())
    except ImportError:
        r['donor_fit_truncate'] = r['donor_fit_pad_mue'] = 'NOT_RUN_NO_TORCH'
    return r


# ============================ single cell execution ============================
T_START878 = T_START883 = T_CELL887
ORACLE_VAULT883 = None; OFFLINE_DIGEST_G1_885 = None; VAULT_FP885 = None
try:
    STATE887['status'] = 'G0'; capture887()
    json_write864('TEST887_prereg.json', {'prereg': PREREG887, 'sha256': PREREG_SHA887, 'written_before_model_load': True})
    load_sources865(); select_locked883()
    du = _s887.disk_usage(str(ROOT864))
    if du.free / 2**30 < 5.0: raise Gate887('DISK_FREE %.1f GiB' % (du.free / 2**30))
    STATE883['write_probe'] = write_probe883(ROOT864)
    if not all(STATE883['write_probe'].values()): raise Gate887('WRITE_PROBE %s' % STATE883['write_probe'])
    source_audit878(); load878(); run_selftests883()               # the 885 CPU selftests, unchanged
    STATE887['selftest'] = st887()
    json_write864('TEST887_cpu_selftest.json', STATE887['selftest'])
    if not all(v is True or v == 'NOT_RUN_NO_TORCH' for v in STATE887['selftest'].values()):
        raise Gate887('CPU_SELFTEST_887 %s' % sorted(k for k, v in STATE887['selftest'].items() if v is not True))
    STATE883['live_scan'] = live_path_scan883([ENGINE883['body']] + [RAW_SOURCES864[n].decode() for n in ('873.py', '878.py', '881.py')])
    if not STATE883['live_scan']['ok']: raise Gate887('LIVE_PATH_ORACLE_SCAN %s' % STATE883['live_scan'])
    feasibility_audit864(); audit_contracts865(); load_spine864()
    if not (CC_GPU_OK and 'A100' in str(CC_GPU.get('name')) and CC_GPU.get('total_gib', 0) >= 78.0): raise Gate887('A100_80GB_REQUIRED %s' % CC_GPU)
    gate887('G0', 'PASS', selftests_885=sorted(STATE883['selftests']), selftest_887=len(STATE887['selftest']),
            prereg_sha256=PREREG_SHA887, disk_free_gib=round(du.free / 2**30, 1))
    STATE887['status'] = 'G1'                                       # model + native backbone: the 885 G1 chain, unchanged calls
    env883, original_error883, original_trace883, reproduction883 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace883; TWO_JOB_VERIFICATION864 = verify_two_job859(env883, original_trace883)
    assert_hook_free859(env883, 'T887_before_native'); OFFLINE_DIGEST_G1_885 = install_offline_evaluator859(env883)
    if OFFLINE_DIGEST_G1_885 != EVAL_DIGEST885: raise Gate887('EVALUATOR_DIGEST_G1 %s' % OFFLINE_DIGEST_G1_885)
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
    if tuple(w_ for w_, _ in ACTION_IDS867) != ACTIONS887: raise Gate887('NATIVE_VOCABULARY %s' % [w_ for w_, _ in ACTION_IDS867])
    assert not any(p_.requires_grad for p_ in env883['model'].parameters()), 'NOT_FROZEN'
    assert_hook_free859(env883, 'T887_before_points')
    STATE883['model_contract'] = model_contract883(env883, CC_GPU)
    if not STATE883['model_contract']['ok']: raise Gate887('MODEL_CONTRACT %s' % STATE883['model_contract']['checks'])
    if _o887.path.exists(CART_ROOT883): _s887.rmtree(CART_ROOT883)
    _o887.makedirs(CART_ROOT883); EXP_DIR878 = type(ROOT864)(CART_ROOT883)
    gate887('G1', 'PASS', chunk=EXP878['CHUNK'], P=int(env883['P']), model_contract=STATE883['model_contract']['checks'],
            bank_digest=digest883, weights_digest=WEIGHTS0_878)
    by_key883 = build_specs869(env883)
    ORACLE_VAULT883 = seal_oracle883(env883); VAULT_FP885 = vault_fingerprint885(ORACLE_VAULT883)   # live work without oracle keys
    STATE887['status'] = 'RUN'
    assert CALL_ALLOWANCE865 == 3000, ('CALL_ALLOWANCE865', CALL_ALLOWANCE865)
    now_ = _t887.perf_counter(); plan_ = g2_budget_plan883(now_, T_START883, WALL_S883)
    if plan_ is None: raise Budget883('NO_TIME_LEFT_AFTER_G1')
    T0_865 = plan_['T0_865']; TEST865_MINUTES = plan_['TEST865_MINUTES']
    rearm_budget865(env883)                                         # +30 min engine margin; the 75 min wall is guard883 / admit883
    if budget_left865(env883, STEP_CALLS867) is not True: raise Budget883('RESOURCE_BUDGET_AT_RUN_START')
    plan887 = [('NONE', w_, c_) for (w_, c_) in CELLS887] + [(a_, w_, c_) for (w_, c_) in CELLS887 for a_ in ('TRUE', 'WRONG')]
    obs887 = {}
    for i_, (a_, w_, c_) in enumerate(plan887):
        if i_: admit883('E%02d_%s_%s_%s' % (i_, a_, w_, c_), len(plan887) - i_)
        donor_ = None if a_ == 'NONE' else obs887.get((DONOR887[w_], c_))
        ep_ = episode887(env883, by_key883[(int(w_), c_)], a_, '%s_%s_%s' % (a_, w_, c_), HORIZON883, donor_)
        if a_ == 'NONE': obs887[(w_, c_)] = ep_['obs']
        ep_['obs'] = len(ep_['obs'])                                # rows stay in obs887 only
    STATE887['status'] = 'POST'
    STATE887['post_run'] = {'bank_digest_unchanged': records_digest861(env883) == digest883,
                            'memnull_seal_unchanged': physical_seal863(env883, env883['MEMNULL841']) == null_seal883,
                            'weights_unchanged': weights_digest877(env883) == WEIGHTS0_878,
                            'hooks_zero': hook_audit859(env883, 'T887_final')['hook_count'] == 0,
                            'model_contract_ok': model_contract883(env883, CC_GPU)['ok']}
    if not all(STATE887['post_run'].values()): raise Gate883('PHYSICAL_POST_RUN_INTEGRITY %s' % STATE887['post_run'])
    oenv887, ev887 = evaluator_env885(env883, ORACLE_VAULT883, OFFLINE_DIGEST_G1_885, VAULT_FP885)
    STATE887['scores'] = episode_scores885(oenv887, by_key883, STATE887['episodes']); STATE887['evaluator'] = ev887
    del oenv887
    STATE887['technical_status'] = 'COMPLETE'
except Budget883 as exc:
    STATE887['technical_status'] = 'BUDGET_STOP'; STATE887['error'] = str(exc)
except BaseException as exc:
    STATE887['technical_status'] = 'INTERRUPTED' if isinstance(exc, (KeyboardInterrupt, SystemExit)) else 'TECHNICAL_BLOCK'
    STATE887['error'] = '%s: %s' % (type(exc).__name__, exc); STATE887['traceback'] = traceback.format_exc()
    if str(exc).startswith('PHYSICAL_') and not STATE887['physical_failure']: STATE887['physical_failure'] = str(exc)[:500]
    print('TEST887 ERROR at', STATE887['status'], STATE887['error'][:400], file=ERROR_CONSOLE864, flush=True)
    print(STATE887['traceback'], file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        if _o887.path.exists(CART_ROOT883):
            left_ = sorted(_o887.listdir(CART_ROOT883)); _s887.rmtree(CART_ROOT883)
            if left_: STATE883['cleanup_errors'].append({'episode_id': 'CART_ROOT', 'errors': ['LEFTOVER %s' % left_[:20]]})
    except BaseException as exc: STATE883['cleanup_errors'].append({'episode_id': 'CART_ROOT', 'errors': ['%s: %s' % (type(exc).__name__, exc)]})
    pairs_ = STATE887['pairs']
    phys_ = {'reads_true': len(pairs_), 'reads_wrong': len(pairs_), 'physical_failure': STATE887['physical_failure'],
             'no_physical_failure': STATE887['physical_failure'] is None,
             'negatives_refused': None if STATE887['negatives'] is None else all(STATE887['negatives'].values()),
             'post_run_integrity': None if STATE887['post_run'] is None else all(STATE887['post_run'].values()),
             'cleanup_clean': not STATE883['cleanup_errors']}
    try:
        STATE887['verdict'] = verdict887(STATE887['technical_status'] or 'TECHNICAL_BLOCK', phys_, pairs_, STATE887['scores'])
    except BaseException as exc:
        STATE887['verdict'] = {'TECHNICAL_STATUS': 'TECHNICAL_BLOCK', 'PHYSICAL_READ': 'FAIL', 'CONTENT_CAUSAL_EFFECT': 'INCONCLUSIVE',
                               'OUTCOME_BENEFIT': 'NOT_MEASURED', 'reasons': {'verdict_error': '%s: %s' % (type(exc).__name__, exc)}}
    eps_ = STATE887['episodes']
    report887 = {
        'test': 'TEST887', 'verdict': STATE887['verdict'], 'physical_facts': phys_, 'error': STATE887['error'],
        'hashes': {'executed_cell': STATE887['source'], 'base_885': BASE_INFO887, 'engine': ENGINE_INFO883, 'prereg_sha256': PREREG_SHA887,
                   'head_locks': HEAD883, 'weights_digest': globals().get('WEIGHTS0_878'), 'bank_digest': globals().get('digest883')},
        'gates': STATE887['gates'], 'negatives': STATE887['negatives'], 'post_run': STATE887['post_run'],
        'counters': {'episodes': len(eps_), 'steps': sum(e_['n_steps'] for e_ in eps_ if e_.get('n_steps') is not None),
                     'paired_points': len(pairs_), 'cartridges_true': sum(len(e_['cartridges']) for e_ in eps_),
                     'cartridges_wrong': sum(len(e_['wrong_cartridges']) for e_ in eps_),
                     'ssd_bytes': sum(int(c_.get('bytes') or 0) for e_ in eps_ for c_ in e_['cartridges'] + e_['wrong_cartridges']),
                     'calls849': globals().get('env883', {}).get('CALLS849') if isinstance(globals().get('env883'), dict) else None,
                     'wall_s': round(_t887.perf_counter() - T_CELL887, 1),
                     'peak_alloc_gib': STATE883['budget'].get('peak_alloc_gib'), 'ffe_by_kind': STATE883['budget'].get('ffe_by_kind')},
        'cells': {'%s_%s' % (w_, c_): {a_: next(({'end': e_['end'], 'actions': e_['actions'], 'effects': e_['effects'],
                                                 'accepted': e_['accepted'], 'final_mounted': e_['final_mounted'],
                                                 'Y': (STATE887['scores'] or {}).get(e_['episode_id'], {}).get('Y')}
                                                for e_ in eps_ if e_['episode_id'] == '%s_%s_%s' % (a_, w_, c_)), None)
                                         for a_ in ARMS887} for (w_, c_) in CELLS887},
        'pairs': [{k_: p_[k_] for k_ in ('episode_id', 'step', 'action_none', 'action_true', 'action_wrong', 'tv_true_wrong',
                                          'tv_true_none', 'tv_wrong_none', 'body_tokens')} for p_ in pairs_],
        'cleanup_errors': STATE883['cleanup_errors'], 'evaluator': STATE887.get('evaluator'),
        'not_claimed': PREREG887['not_claimed'], 'gpu_note': 'GPU_NOT_RUN_BY_AUTHOR (cell author); GPU_RUN_THIS_TEST if this is a Colab console'}
    try:
        if STATE887['traceback']: (ROOT864 / 'TEST887_traceback.txt').write_text(STATE887['traceback'], encoding='utf-8')
        json_write864('TEST887_final_report.json', jsafe878(report887) if 'jsafe878' in globals() else _j887.loads(_j887.dumps(report887, default=str)))
        p_ = ROOT864 / 'TEST887_final_report.json'
        if _j887.loads(p_.read_text(encoding='utf-8'))['verdict']['TECHNICAL_STATUS'] != STATE887['verdict']['TECHNICAL_STATUS']:
            raise OSError('READ_BACK_MISMATCH')
        STATE887['report_sha256'] = sha256_bytes864(p_.read_bytes())
    except BaseException as exc:
        STATE887['artifact_errors'].append('%s: %s' % (type(exc).__name__, exc))
        STATE887['verdict'] = dict(STATE887['verdict'], TECHNICAL_STATUS='ARTIFACT_FAILURE', PHYSICAL_READ='FAIL',
                                   CONTENT_CAUSAL_EFFECT='INCONCLUSIVE', OUTCOME_BENEFIT='NOT_MEASURED')
    v_ = STATE887['verdict']
    print('=' * 110)
    print('TEST887 | PHYSICAL_READ=%s | CONTENT_CAUSAL_EFFECT=%s | OUTCOME_BENEFIT=%s | TECHNICAL_STATUS=%s' % (
        v_['PHYSICAL_READ'], v_['CONTENT_CAUSAL_EFFECT'], v_['OUTCOME_BENEFIT'], v_['TECHNICAL_STATUS']))
    for p_ in pairs_:
        print('PAIR %-20s t=%d NONE=%-9s TRUE=%-9s WRONG=%-9s TV(T,W)=%.3f TV(T,N)=%.3f body=%d' % (
            p_['episode_id'], p_['step'], p_['action_none'], p_['action_true'], p_['action_wrong'], p_['tv_true_wrong'],
            p_['tv_true_none'], p_['body_tokens']))
    for k_, c_ in report887['cells'].items():
        print('CELL %-11s' % k_, ' | '.join('%s:%s Y=%s' % (a_, '>'.join((c_[a_] or {}).get('actions') or []), (c_[a_] or {}).get('Y'))
                                           for a_ in ARMS887))
    print('reasons', _j887.dumps(v_.get('reasons'), default=str)[:1500])
    print('error', STATE887['error'], '| artifact_errors', STATE887['artifact_errors'], '| report sha256', STATE887.get('report_sha256'))
    print('=' * 110, flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE883['suffix'], 'test870.py:suffix', 'exec'), globals())     # ZIP + SHA256SUMS + testzip + Drive copy (locked I/O)
try:                                                                          # delivery receipt beside the ZIP (outside it)
    import zipfile as _z887
    with _z887.ZipFile(CC_ZIP) as _zz: _zip_ok = _zz.testzip() is None
    _zsha = _h887.sha256(CC_ZIP.read_bytes()).hexdigest()
    _rc = {'zip': str(CC_ZIP), 'zip_sha256': _zsha, 'zip_testzip_ok': _zip_ok, 'verdict': STATE887['verdict'],
           'drive_dir': CC_DRIVE_DIR, 'drive_zip_sha256_equal': None}
    if CC_DRIVE_DIR is not None:
        _dz = _o887.path.join(CC_DRIVE_DIR, _o887.path.basename(str(CC_ZIP)))
        _rc['drive_zip_sha256_equal'] = _o887.path.exists(_dz) and _h887.sha256(open(_dz, 'rb').read()).hexdigest() == _zsha
    _rp = str(CC_ZIP).replace('.zip', '_RECEIPT.json')
    with open(_rp, 'w', encoding='utf-8') as _f: _f.write(_j887.dumps(_rc, sort_keys=True, default=str, indent=1))
    if CC_DRIVE_DIR is not None: _s887.copy2(_rp, CC_DRIVE_DIR)
    print('TEST887 RECEIPT', _j887.dumps(_rc, sort_keys=True, default=str)[:600])
    if not _zip_ok or _rc['drive_zip_sha256_equal'] is False: print('TEST887 ARTIFACT_INCOMPLETE: ZIP or Drive copy not verified')
except BaseException as _exc:
    print('TEST887 ARTIFACT_INCOMPLETE: receipt failed', type(_exc).__name__, _exc)
