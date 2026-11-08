# AKBASCORE SILICON HIPPOCAMPUS — TEST873 — NATIVE CONTINUOUS KV TIMELINE
# ONE QUESTION: when the model's own t2 decision, the physical outcome of that decision and the next decision are kept
# in ONE time-ordered KV cache (instead of rebuilding a fresh context and re-feeding the past as FV/FK soft rows), is
# the next decision more correct, and does it follow the physical outcome rather than the echo of the action word?
# Worlds I867_00 and I867_01, MISSING and LIVE (arm V_X): each loop is replayed bit-exactly against the 869 record.
#   t2 (before the action): timeline = [memory M_t2][t2 decision context X2]; the CAR reading on this cache must equal
#     the recorded t2 reading (candidate continuations are cropped, never committed); then ONLY the tokens of the action
#     the model chose (" ACQUIRE") are committed to the timeline.
#   t3 (after the engine executed the action): the acquired cartridge is appended to the timeline with the locked
#     native_append_direct (SHA-verified load, lower CUT3 K/V RoPE-rephased to the new positions, upper layers computed
#     by the frozen model attending to the timeline, prior rows verified unchanged). The t3 decision context X3 follows
#     WITHOUT FV/FK: question, candidate C, evidence E, relation R, pointer P, the model's own evaluation V, suffix.
#   T1 continuous native | T2 same, the paired world's card appended instead | T3 same card, committed action tokens
#   replaced by " ADVANCE" (same token count) | M0 Markov: X3 on the physical memory only | R: the recorded FV/FK decision.
# Python never chooses, forbids or reweights an action; T2/T3 are counterfactual measurements, never executed.
# HOW TO RUN (A100 80GB): paste this whole file into ONE Colab cell and run it once.
import ast as _a873, hashlib as _h873, json as _j873, urllib.request as _u873

ENGINE_URL873 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB873 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc'       # test870.py: the engine run on the A100 (TEST870-872)
MARKER873 = 'AKBASCORE SILICON HIPPOCAMPUS — TEST873'


def blob873(raw):
    return _h873.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def engine_parts873():
    # The GPU-verified engine runs unchanged; only output file/folder names are renamed (each rename counted).
    with _u873.urlopen(_u873.Request(ENGINE_URL873, headers={'User-Agent': 'AKBASCORE-TEST873'}), timeout=240) as r:
        raw = r.read()
    assert blob873(raw) == ENGINE_BLOB873, ('ENGINE_BLOB_MISMATCH', blob873(raw))
    text = raw.decode('utf-8')
    _a873.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST873_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST873_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST873_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('873_engine.log', '873_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST873_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '873_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '873_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST873_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old, parts[where].count(old))
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL873, 'git_blob': blob873(raw), 'sha256': _h873.sha256(raw).hexdigest(),
                   'io_renames': len(renames)}


ENGINE873, ENGINE_INFO873 = engine_parts873()
exec(compile(ENGINE873['prefix'], 'test870.py:prefix', 'exec'), globals())      # console capture, GPU precheck (I/O)
exec(compile(ENGINE873['body'], 'test870.py:engine', 'exec'), globals())        # locked engine definitions (no run)
print('TEST873 ENGINE', _j873.dumps(ENGINE_INFO873, sort_keys=True))


# ============================ TEST873 — pre-registration (fixed before the model is loaded) ============================
LOCKS864.update({'test870.py': ENGINE_BLOB873, 'Test870.log': 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc',
                 '872.py': 'f04978e780b1cd1b9bbcfe75de1d1df3c2cbad4e', '872.log': '51e454158c74855f7d4dc3575aef419c6a529556'})
TEST870_MINUTES = 40.0
TEST865_MINUTES = TEST870_MINUTES
WORLDS873 = ('00', '01')
SIDES873 = tuple('I867_%s_%s' % (w, c) for w in WORLDS873 for c in ('MISSING', 'LIVE'))
ARM873, PRE_STEP873, POST_STEP873 = 'V_X', 2, 3
ECHO_WORD873 = 'ADVANCE'       # first ACTIONS866 word other than ACQUIRE with the same token count (checked at runtime)
ONE_SHOT_TOL873 = 0.02         # max |dP| over the six actions: [X2][A] committed in two steps vs [X2+A] in one forward
ROPE_TOL873 = 1e-2             # relative L2: appended card's lower keys re-rephased to the M_t3 positions vs M_t3 keys
IMPROVE_MIN873 = 0.20          # MISSING: P(ACQUIRE | R) - P(ACQUIRE | T1) at least this (leaves the repeated ACQUIRE)
LIVE_TOL873 = 0.10             # LIVE: P(ACCEPT | T1) >= P(ACCEPT | R) - this
OUTCOME_TV_MIN873 = 0.10       # card swap must move the decision: TV(T1, T2) >= this on a side of the world
PREREG873 = {
    'question': 'does a native continuous KV timeline (own decision tokens + physical outcome + next decision in one '
                'cache) give a more correct next decision than the FV/FK soft-row history, following the physical '
                'outcome rather than the action-word echo?',
    'sides': SIDES873, 'arm': ARM873, 'steps': [PRE_STEP873, POST_STEP873], 'echo_word': ECHO_WORD873,
    'arms': {'T1': 'timeline [M_t2][X2][own action tokens][own acquired card][X3]',
             'T2': 'timeline [M_t2][X2][own action tokens][paired world card][X3]',
             'T3': 'timeline [M_t2][X2][" %s" tokens][own acquired card][X3]' % ECHO_WORD873,
             'M0': '[M_t3][X3] (Markov, physical memory only)', 'R': 'recorded decision with FV/FK (old method)'},
    'X3': 'control prompt + C, E, R, P, V of t3 (the engine\'s own rows) + review suffix; FV and FK removed',
    'technical': ['t2 CAR on the timeline == recorded t2 CAR (float equality); cache length back to n+L after crops',
                  'committed action tokens == CAR ids of the chosen word; timeline length == M_t2 + X2 + A',
                  'appended card: SHA-verified load, prior rows unchanged (strict_sha), all 80 layers same length, '
                  'lower V == M_t3 card lower V bitwise, lower K re-rephased rel L2 <= %g' % ROPE_TOL873,
                  'T1 rebuilt from an independent copy == T1 (float equality)',
                  'T1 with [X2+A] in one forward vs two steps: max |dP| <= %g' % ONE_SHOT_TOL873,
                  'memory seal and hook audit unchanged'],
    'classification': {'TIMELINE_EFFECT': 'in BOTH worlds: P_acq(R) - P_acq(T1) >= %.2f on MISSING; P_acc(T1) >= '
                                          'P_acc(R) - %.2f on LIVE; on at least one side TV(T1,T2) >= %.2f and '
                                          'TV(T1,T3) < TV(T1,T2)' % (IMPROVE_MIN873, LIVE_TOL873, OUTCOME_TV_MIN873),
                       'NO_TIMELINE_EFFECT': 'technical checks pass but the condition above fails',
                       'TECHNICAL_BLOCK': 'any replay or technical check fails'},
    'reported_not_classified': 'M0 vs T1 (Markov vs timeline), I867_00 escape from the Markov ACQUIRE loop'}
PREREG_SHA873 = sha256_bytes864(_j873.dumps(PREREG873, sort_keys=True).encode('utf-8'))
STATE873 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO873, 'prereg_sha256': PREREG_SHA873, 'source': {},
            'sides': {}, 'blocks': [], 'outcome': None, 'error': None}
PAIR_CARD873 = {}               # side -> the card the paired world acquired at t2 (from the 869 record)
T2_KEEP873 = {}                 # side -> timeline KV lists built at t2


def line873(*parts):
    short864('T873', *parts)


def capture_source873():
    source, how = None, None
    try:
        hist = [t for t in get_ipython().history_manager.input_hist_raw if MARKER873 in t and 'def probe873' in t]
        if hist:
            source, how = hist[-1], 'IPYTHON_CELL'
    except NameError:
        pass
    if source is None and '__file__' in globals():
        with open(globals()['__file__'], encoding='utf-8') as f:
            source, how = f.read(), 'FILE_%RUN'
    assert source and MARKER873 in source, ('EXECUTED_873_SOURCE_NOT_CAPTURED: paste the whole TEST873 code into ONE '
                                            'Colab cell and run that cell')
    tree = _a873.parse(source)
    banned = {'execute866', 'mount865', 'free865', 'hop865', 'parse866', 'register_forward_hook',
              'register_forward_pre_hook', 'install_all_output_capturing_hooks', 'output_hidden_states',
              'output_attentions'}
    for node in tree.body:
        if isinstance(node, _a873.FunctionDef) and node.name.endswith('873') and node.name != 'capture_source873':
            used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in _a873.walk(node)
                    if isinstance(c, _a873.Call)} | {k.arg for k in _a873.walk(node) if isinstance(k, _a873.keyword)}
            assert not (used & banned), ('FIREWALL873', node.name, sorted(used & banned))
    rebinds = [n for n in tree.body if isinstance(n, _a873.Assign) and
               any(getattr(t, 'id', '') == 'xray_point870' for t in n.targets)]
    assert len(rebinds) == 1 and getattr(rebinds[0].value, 'id', None) == 'probe873', 'FIREWALL873_REBIND'
    (ROOT864 / '873.py').write_text(source, encoding='utf-8')
    STATE873['source'] = {'how': how, 'sha256': sha256_bytes864(source.encode('utf-8')),
                          'git_blob': git_blob864(source.encode('utf-8')), 'lines': source.count('\n') + 1,
                          'firewall': 'PASS'}


# ============================ new computation: one KV timeline ============================
def kv873(env, cache):
    # the cache as an owned list of 80 (K, V) pairs (fresh tensors: no aliasing between branches)
    return [tuple(t.clone() for t in cache_kv870(cache, l)) for l in range(int(env['NL']))]


def length873(env, kv):
    lens = {int(k.shape[-2]) for k, _ in kv} | {int(v.shape[-2]) for _, v in kv}
    assert len(lens) == 1 and len(kv) == int(env['NL']), ('TIMELINE_LAYER_LENGTHS', sorted(lens), len(kv))
    return lens.pop()


def forward873(env, cache, Y, n0):
    # append Y to the cache at positions n0.. (same call as the locked car867 forward); returns last-row log-probs
    L = int(Y.shape[0])
    assert int(cache.get_seq_length()) == n0 and n0 + L <= int(env['MAX_FUSED_TOKENS']), ('TIMELINE_LENGTH', n0, L)
    pos = torch.arange(n0, n0 + L, device=env['DEV'])
    with torch.no_grad():
        out = env['model'](inputs_embeds=Y.reshape(1, L, env['H']), past_key_values=cache,
                           attention_mask=torch.ones((1, n0 + L), device=env['DEV'], dtype=torch.long),
                           position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
        first = torch.log_softmax(out.logits[0, -1].float(), dim=-1)
        del out
    assert int(cache.get_seq_length()) == n0 + L, 'TIMELINE_NOT_EXTENDED'
    return first


def car873(env, cache, X):
    # the locked CAR reading (car867 procedure: teacher-forced continuations, each cropped) on an existing timeline;
    # afterwards the cache holds exactly [previous timeline][X]: no candidate continuation is committed
    env['budget849']()
    n0 = int(cache.get_seq_length())
    longest = max(len(ids) for _, ids in ACTION_IDS867)
    assert n0 + int(X.shape[0]) + longest <= int(env['MAX_FUSED_TOKENS']), ('CONTEXT_LIMIT', n0, int(X.shape[0]))
    first = forward873(env, cache, X, n0)
    n1 = n0 + int(X.shape[0])
    scores = []
    with torch.no_grad():
        for word, ids in ACTION_IDS867:
            token_logps = [float(first[ids[0]])]
            if len(ids) > 1:
                m = len(ids) - 1
                p2 = torch.arange(n1, n1 + m, device=env['DEV'])
                out = env['model'](inputs_embeds=env['embed841'](ids[:-1]).reshape(1, m, env['H']), past_key_values=cache,
                                   attention_mask=torch.ones((1, n1 + m), device=env['DEV'], dtype=torch.long),
                                   position_ids=p2.unsqueeze(0), cache_position=p2, use_cache=True, return_dict=True)
                lp = torch.log_softmax(out.logits[0].float(), dim=-1)
                cache.crop(-m)
                assert int(cache.get_seq_length()) == n1, 'CAR_CROP_LENGTH_MISMATCH_873'
                token_logps += [float(lp[i, ids[i + 1]]) for i in range(m)]
                del out, lp
            scores.append({'word': word, 'ids': ids, 'token_logps': token_logps,
                           'sequence_logp': float(sum(token_logps)), 'hard_greedy_ids': []})
    top = torch.topk(first, 10)
    return reading867({'scores': scores, 'path': 'CROP', 'fallback_reason': None,
                       'first_top10': {'ids': [int(i) for i in top.indices.tolist()]}, 'X_sha256': None})


APPEND873 = {}


def resolve_append873(env):
    # Names resolved in the order the locked engine resolves them at call time; every source is logged.
    nad = env['native_append_direct']
    g = nad.__globals__
    b = g.get('__builtins__', {})
    spaces = (('nad_globals', g), ('nad_builtins', b if isinstance(b, dict) else vars(b)),
              ('build_fusion_globals', env['build_fusion'].__globals__), ('env', env))
    diag = {'nad_globals_is_env': g is env, 'nad_file': nad.__code__.co_filename,
            'nad_co_names_has': sorted(set(nad.__code__.co_names) & {'rephase', 'CUT', 'load_verified'})}
    found = {}
    for name in ('load_verified', 'rephase', 'CUT', 'safe_load', 'to_gpu', 'entries'):
        hit = [(w, ns[name]) for w, ns in spaces if name in ns]
        diag[name] = [w for w, _ in hit] or 'MISSING'
        if hit:
            found[name] = hit[0][1]
    assert 'rephase' in found and 'CUT' in found and int(found['CUT']) == 3, ('APPEND_NAMESPACE', diag)
    if 'load_verified' in found:
        assert str(inspect.signature(found['load_verified'])) == '(cid)', ('LOAD_VERIFIED_SIGNATURE', diag)
        load, how = found['load_verified'], 'LOCKED_LOAD_VERIFIED'
    else:
        # 757 load_verified body without its timers: locked safe_load (file + tensor SHA) then locked to_gpu.
        assert all(k in found for k in ('safe_load', 'to_gpu', 'entries')), ('APPEND_LOADER', diag)
        sl, tg, ent = found['safe_load'], found['to_gpu'], found['entries']
        load, how = (lambda cid: (tg(sl(ent[cid])), {})), 'LOCKED_SAFE_LOAD_THEN_TO_GPU'
    diag['loader'] = how
    APPEND873.update({'load': load, 'rephase': found['rephase'], 'CUT': int(found['CUT']), 'diag': diag})
    return diag


def append_card873(env, kv, cid):
    # the locked native append: SHA-verified cartridge, RoPE rephase of the lower CUT3 rows, upper layers by the model
    cp, _ = APPEND873['load'](cid)
    n0 = length873(env, kv)
    grown = env['native_append_direct'](list(kv), cp, strict_sha=True)
    body = int(env['entries'][cid]['body_tokens'])
    assert length873(env, grown) == n0 + body, ('CARD_APPEND_LENGTH', n0, body, length873(env, grown))
    del cp
    return grown, n0


def decide873(env, kv, X):
    cache = env['cache_build'](list(kv))
    reading = car873(env, cache, X)
    total = int(cache.get_seq_length())
    del cache
    return reading, total


def probs873(reading):
    return {w: round(float(p), 6) for w, p in reading['normalized'].items()}


def same873(a, b):
    return [(s['word'], s['token_logps']) for s in a['scores']] == [(s['word'], s['token_logps']) for s in b['scores']]


def tv873(p, q):
    return round(0.5 * sum(abs(p[w] - q[w]) for w in p), 6)


def probe873(env, ctx, record, state, label):
    # Called by the sealed replay tap (return value ignored by the loop). t2: build the timeline before the action.
    # t3: append the physical outcome and read the next decisions.
    side = ctx['spec']['item']
    q = env['QTEXT841'][ctx['spec']['qid']]
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q)))
    post = env['REVIEW_SUFFIX851']
    out = STATE873['sides'].setdefault(side, {'checks': {}, 'arms': {}, 'lengths': {}, 'error': None})
    c = out['checks']
    t0 = time.perf_counter()
    try:
        if ctx['steps'] == PRE_STEP873:
            out['t2_action'] = record['action']
            assert record['action'] == 'ACQUIRE', ('T2_NOT_ACQUIRE', record['action'])
            ids = dict(ACTION_IDS867)
            assert len(ids[ECHO_WORD873]) == len(ids['ACQUIRE']), 'ECHO_WORD_LENGTH'
            X2, _ = env['make_x851'](pre, list(state['segments']), post)
            m2 = [tuple(t.clone() for t in kv) for kv in ctx['memx']]
            n2 = length873(env, m2)
            cache = env['cache_build'](list(m2))
            t2_reading = car873(env, cache, X2)
            c['t2_timeline_car_equals_record'] = same873(t2_reading, record['reading'])
            c['t2_cache_after_crops'] = int(cache.get_seq_length()) == n2 + int(X2.shape[0])
            base = kv873(env, cache)
            keep = {}
            for name, word in (('own', record['action']), ('echo', ECHO_WORD873)):
                branch = env['cache_build'](list(kv873(env, cache) if name == 'echo' else base))
                forward873(env, branch, env['embed841'](ids[word]), n2 + int(X2.shape[0]))
                keep[name] = kv873(env, branch)
                del branch
            one = env['cache_build'](list(m2))
            forward873(env, one, torch.cat([X2, env['embed841'](ids[record['action']])], dim=0), n2)
            keep['one_shot'] = kv873(env, one)
            c['committed_tokens'] = ids[record['action']]
            c['timeline_after_commit'] = length873(env, keep['own']) == n2 + int(X2.shape[0]) + len(ids[record['action']])
            out['lengths'].update({'M_t2': n2, 'X2': int(X2.shape[0]), 'after_commit': length873(env, keep['own'])})
            T2_KEEP873[side] = keep
            del cache, one, base, m2
            assert c['t2_timeline_car_equals_record'] and c['t2_cache_after_crops'] and c['timeline_after_commit'], c
            line873('T2_TIMELINE', side, _j873.dumps({k: c[k] for k in ('t2_timeline_car_equals_record',
                                                                         't2_cache_after_crops', 'timeline_after_commit')}),
                    'lengths=%s' % _j873.dumps(out['lengths']))
            return
        vram0 = vram_begin870()
        keep = T2_KEEP873.pop(side)
        memx, n3 = ctx['memx'], int(ctx['memx'][0][0].shape[-2])
        eff = [e for e in ctx['events'] if e.get('type') == 'EFFECT'][-1]
        card, pair = eff.get('chosen'), PAIR_CARD873[side]
        body = int(env['entries'][card]['body_tokens'])
        out.update({'card': card, 'pair_card': pair})
        c['card_is_last_mounted'] = eff.get('effect') == 'MOUNTED' and list(ctx['M'])[-1] == card
        names = slot_names869(env, list(state['segments']))
        X3, _ = env['make_x851'](pre, [s for s, n in zip(state['segments'], names) if n not in ('FV', 'FK')], post)
        out['X3_segments'] = [n for n in names if n not in ('FV', 'FK')]
        seal0 = prefix_seals865(env, memx)
        hook0 = assert_hook_free859(env, 'T873_before_' + side)
        arms = out['arms']
        arms['R'] = {'action': record['action'], 'p': probs873(record['reading'])}
        r, out['lengths']['M0'] = decide873(env, memx, X3)
        arms['M0'] = {'action': r['action'], 'p': probs873(r)}
        g1, n_before = append_card873(env, keep['own'], card)
        cut, rephase = APPEND873['CUT'], APPEND873['rephase']
        pos_t, pos_m = (torch.arange(a, a + body, device=env['DEV']) for a in (n_before, n3 - body))
        c['card_lower_values_bitwise'] = all(bool(torch.equal(g1[i][1][:, :, n_before:], memx[i][1][:, :, n3 - body:]))
                                             for i in range(cut + 1))
        rel = max(float(torch.linalg.vector_norm((rephase(g1[i][0][:, :, n_before:], pos_t, pos_m).float()
                                                  - memx[i][0][:, :, n3 - body:].float())))
                  / max(float(torch.linalg.vector_norm(memx[i][0][:, :, n3 - body:].float())), 1e-30)
                  for i in range(cut + 1))
        c['card_lower_keys_rephase_rel'] = rel
        c['card_lower_keys_rephase_ok'] = rel <= ROPE_TOL873
        g1b, _ = append_card873(env, [tuple(t.clone() for t in kv) for kv in keep['own']], card)
        r1, out['lengths']['T1'] = decide873(env, g1, X3)
        r1b, _ = decide873(env, g1b, X3)
        c['t1_rebuild_identical'] = same873(r1, r1b)
        arms['T1'] = {'action': r1['action'], 'p': probs873(r1)}
        del g1, g1b
        for name, kv, cid in (('T2', keep['own'], pair), ('T3', keep['echo'], card), ('T1_ONE_SHOT', keep['one_shot'], card)):
            grown, _ = append_card873(env, kv, cid)
            rr, out['lengths'][name] = decide873(env, grown, X3)
            arms[name] = {'action': rr['action'], 'p': probs873(rr)}
            del grown
        c['one_shot_max_dp'] = max(abs(arms['T1']['p'][w] - arms['T1_ONE_SHOT']['p'][w]) for w in arms['T1']['p'])
        c['one_shot_ok'] = c['one_shot_max_dp'] <= ONE_SHOT_TOL873
        hook1 = assert_hook_free859(env, 'T873_after_' + side)
        c['memory_seal_unchanged'] = prefix_seals865(env, memx) == seal0
        c['hook_free'] = not (hook0['hook_count'] or hook1['hook_count'] or hook0['transformers_output_capturing_installed']
                              or hook1['transformers_output_capturing_installed'])
        out['tv'] = {'T1_T2': tv873(arms['T1']['p'], arms['T2']['p']), 'T1_T3': tv873(arms['T1']['p'], arms['T3']['p']),
                     'T1_M0': tv873(arms['T1']['p'], arms['M0']['p']), 'T1_R': tv873(arms['T1']['p'], arms['R']['p'])}
        out['vram'] = vram_end870(vram0)
        del keep
    except Exception as exc:
        out['error'] = '%s: %s' % (type(exc).__name__, str(exc)[:400])
        out['traceback'] = traceback.format_exc()
        short864('T873 POINT_ERROR', side, 't=%d' % ctx['steps'], out['traceback'])
    finally:
        gc.collect()
        env['release']()
    out['seconds_t%d' % ctx['steps']] = round(time.perf_counter() - t0, 3)
    if ctx['steps'] == POST_STEP873 or out['error']:
        line873('POINT', side, _j873.dumps(c, sort_keys=True, default=str), 'lengths=%s' % _j873.dumps(out['lengths']),
                '' if out['error'] is None else 'ERROR=' + out['error'])


xray_point870 = probe873      # the sealed replay tap calls this name at the declared steps; its return value is ignored


def outcome873():
    reps = {r.get('item'): r for r in STATE870['replays']}
    blocks = list(STATE873['blocks'])
    need_checks = ('t2_timeline_car_equals_record', 't2_cache_after_crops', 'timeline_after_commit', 'card_is_last_mounted',
                   'card_lower_values_bitwise', 'card_lower_keys_rephase_ok', 't1_rebuild_identical', 'one_shot_ok',
                   'memory_seal_unchanged', 'hook_free')
    for side in SIDES873:
        s = STATE873['sides'].get(side)
        if reps.get(side, {}).get('ok') is not True:
            blocks.append('REPLAY_NOT_EXACT:' + side)
        if not s or s.get('error') or any(a not in s.get('arms', {}) for a in ('R', 'M0', 'T1', 'T2', 'T3')):
            blocks.append('INCOMPLETE:' + side)
        elif not all(s['checks'].get(k) for k in need_checks):
            blocks.append('CHECK:%s:%s' % (side, [k for k in need_checks if not s['checks'].get(k)]))
    res = {'blocks': blocks, 'worlds': {}}
    if blocks:
        res['outcome'] = 'TECHNICAL_BLOCK'
    else:
        ok_all = True
        for w in WORLDS873:
            m, l = STATE873['sides']['I867_%s_MISSING' % w], STATE873['sides']['I867_%s_LIVE' % w]
            improve = m['arms']['R']['p']['ACQUIRE'] - m['arms']['T1']['p']['ACQUIRE']
            live = l['arms']['T1']['p']['ACCEPT'] - l['arms']['R']['p']['ACCEPT']
            outcome_sides = [s for s in (m, l) if s['tv']['T1_T2'] >= OUTCOME_TV_MIN873 and s['tv']['T1_T3'] < s['tv']['T1_T2']]
            row = {'missing_acquire_drop_vs_R': round(improve, 4), 'live_accept_change_vs_R': round(live, 4),
                   'outcome_following_sides': len(outcome_sides),
                   'missing_acquire_T1_vs_M0': round(m['arms']['T1']['p']['ACQUIRE'] - m['arms']['M0']['p']['ACQUIRE'], 4),
                   'tv_missing': m['tv'], 'tv_live': l['tv']}
            row['pass'] = improve >= IMPROVE_MIN873 and live >= -LIVE_TOL873 and len(outcome_sides) >= 1
            ok_all = ok_all and row['pass']
            res['worlds'][w] = row
        res['outcome'] = 'TIMELINE_EFFECT' if ok_all else 'NO_TIMELINE_EFFECT'
    STATE873['outcome'] = res
    return res


def report873():
    W = ('STOP', 'ACQUIRE', 'ADVANCE', 'ACCEPT', 'REJECT', 'BACKTRACK')
    print('=' * 104)
    print('TEST873 — NATIVE CONTINUOUS KV TIMELINE | GPU %s | engine test870.py %s | source %s (%s) | prereg %s' % (
        CC_GPU.get('name'), ENGINE_BLOB873, STATE873['source'].get('git_blob'), STATE873['source'].get('how'),
        PREREG_SHA873[:16]))
    for side in SIDES873:
        s = STATE873['sides'].get(side)
        if not s:
            print('  %s: not reached' % side)
            continue
        print('  %s | t2 own action %s -> card %s (pair card %s) | lengths %s' % (
            side, s.get('t2_action'), s.get('card'), s.get('pair_card'), _j873.dumps(s['lengths'])))
        print('     checks %s' % _j873.dumps(s['checks'], sort_keys=True, default=str))
        m0 = (s['arms'].get('M0') or {}).get('p')
        for name in ('R', 'M0', 'T1', 'T2', 'T3', 'T1_ONE_SHOT'):
            a = s['arms'].get(name)
            if a:
                dm = '' if not m0 else '  dACQ_vs_M0 %+.3f' % (a['p']['ACQUIRE'] - m0['ACQUIRE'])
                print('     %-11s %-9s ' % (name, a['action']) + '  '.join('%s %.3f' % (w, a['p'][w]) for w in W) + dm)
        print('     TV %s | s_t2=%s s_t3=%s vram_overhead_gib=%s%s' % (
            _j873.dumps(s.get('tv')), s.get('seconds_t2'), s.get('seconds_t3'),
            (s.get('vram') or {}).get('xray_overhead_allocated_gib', 'NA'), '' if not s.get('error') else '  ERROR ' + s['error']))
    o = STATE873['outcome'] or {}
    print('  RESULT', _j873.dumps({k: v for k, v in o.items() if k != 'outcome'}, sort_keys=True))
    print('TEST873 OUTCOME %s | status %s | wall %.0f s | peak GPU %.2f GiB' % (
        o.get('outcome'), STATE873['status'], time.perf_counter() - T_START873,
        max(STATE870['costs'].get('session_peak_allocated_bytes', 0),
            torch.cuda.max_memory_allocated() if torch.cuda.is_available() else 0) / 2**30))
    print('One t2 -> t3 transition per side: a single decision change is not autonomous recursive reasoning.')
    print('GPU EXECUTION NOT VERIFIED BY THE CODE AUTHOR before this run.')
    print('=' * 104)


# ============================ TEST873 — SINGLE CELL EXECUTION ============================
T_START873 = time.perf_counter()
try:
    STATE873['status'] = 'GATE0'
    capture_source873()
    json_write864('873_prereg.json', {'prereg': PREREG873, 'sha256': PREREG_SHA873, 'before_model_load': True})
    line873('GATE0 SOURCE', _j873.dumps(STATE873['source'], sort_keys=True), 'prereg', PREREG_SHA873)
    load_sources865()                         # engine locks + test870.py + Test870.log + 872.py + 872.log (git blobs)
    STATE865['gates']['GATE0_SOURCE'] = {'status': 'PASS', 'locks': len(LOCKS864)}
    for name, needles in (('Test870.log', ('XR870 CALIBRATION CALIBRATION_PASS', 'NVIDIA A100')),
                          ('872.log', ('TEST872 OUTCOME', 'status COMPLETE', 'NVIDIA A100'))):
        text = RAW_SOURCES864[name].decode('utf-8')
        assert all(x in text for x in needles), ('LOCKED_LOG_NOT_A_COMPLETE_GPU_RUN', name)
    feasibility_audit864()
    audit_contracts865()
    load_spine864()
    REFS873 = load_records870()
    for w in WORLDS873:
        cards = {}
        for cnd in ('MISSING', 'LIVE'):
            ev = REFS873[('I867_%s_%s' % (w, cnd), ARM873)]['events']
            ctl = [e['record'] for e in ev if e['type'] == 'CONTROL']
            assert [x['action'] for x in ctl[:2]] == ['ADVANCE', 'ACQUIRE'], ('T2_PATH', w, cnd)
            cards[cnd] = [e for e in ev if e['type'] == 'EFFECT'][PRE_STEP873 - 1]['chosen']
            STATE873.setdefault('t2_sha', {})[(w, cnd)] = ctl[PRE_STEP873 - 1]['state_sha256']
        assert STATE873['t2_sha'][(w, 'MISSING')] == STATE873['t2_sha'][(w, 'LIVE')], ('T2_NOT_SHARED', w)
        PAIR_CARD873['I867_%s_MISSING' % w], PAIR_CARD873['I867_%s_LIVE' % w] = cards['LIVE'], cards['MISSING']
    STATE873.pop('t2_sha')
    line873('GATE0 PASS', 'paired cards %s' % _j873.dumps(PAIR_CARD873, sort_keys=True))
    STATE873['status'] = 'GATE1'
    assert CC_GPU_OK, ('GPU_PRECHECK_NOT_A100_80GB_WITH_40GIB_FREE', CC_GPU)
    env873, original_error873, original_trace873, reproduction873 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace873
    TWO_JOB_VERIFICATION864 = verify_two_job859(env873, original_trace873)
    assert_hook_free859(env873, 'T873_before_native_regression')
    install_offline_evaluator859(env873)
    native873 = native_sequences860(env873)
    NATIVE_REGRESSION864 = native_regression864(env873, native873)
    verify_864_reference865(NATIVE_REGRESSION864)
    ANALYSIS864 = run_analysis863(env873, native873)
    assert len(STATE863['restores']) == 3 and all(r['exact'] for r in STATE863['restores']), 'ORIGINAL_EXACT_RESTORE'
    digest873 = records_digest861(env873)
    null_seal873 = physical_seal863(env873, env873['MEMNULL841'])
    runtime_contracts865(env873)
    runtime_preflight865(env873, reproduction873)
    rearm_budget865(env873)
    make_slots866(env873)
    SLOTS867['PREV_EVALUATION'] = list(env873['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env873)
    line873('GATE1 APPEND NAMESPACE', _j873.dumps(resolve_append873(env873), sort_keys=True))
    assert_hook_free859(env873, 'T873_before_points')
    line873('GATE1 PASS', 'model_load_s=%.0f' % (time.perf_counter() - T_START873))
    STATE873['status'] = 'RUNNING'
    T0_865 = time.perf_counter()
    by_key873 = build_specs869(env873)
    for side in SIDES873:
        rep873 = run_replay870(env873, {'id': side, 'item': side, 'arm': ARM873,
                                        'targets': {PRE_STEP873: 'T2_DECISION', POST_STEP873: 'T3_DECISION'}},
                               by_key873, REFS873)
        T2_KEEP873.pop(side, None)
        if not rep873['ok']:
            STATE873['blocks'].append('REPLAY_NOT_EXACT:%s %s' % (side, _j873.dumps(rep873['mismatch'], default=str)[:300]))
    # ====== OFFLINE: no model call below ======
    hook873 = hook_audit859(env873, 'T873_final')
    if records_digest861(env873) != digest873 or physical_seal863(env873, env873['MEMNULL841']) != null_seal873 or \
            hook873['hook_count'] or hook873['transformers_output_capturing_installed']:
        STATE873['blocks'].append('POST_RUN_INTEGRITY')
    STATE873['status'] = 'COMPLETE'
    outcome873()
except BaseException as exc:
    STATE873['error'] = '%s: %s' % (type(exc).__name__, exc)
    STATE873['traceback'] = traceback.format_exc()
    STATE873['status'] = 'FAILED_AT_' + str(STATE873['status'])
    STATE873['outcome'] = {'outcome': 'TECHNICAL_BLOCK', 'blocks': ['EXCEPTION: ' + STATE873['error'][:300]]}
    print(STATE873['traceback'], file=ERROR_CONSOLE864, flush=True)
    short864('TEST873 FULL TRACEBACK', STATE873['traceback'])
finally:
    try:
        keep873 = dict(STATE873, replays=STATE870['replays'])
        json_write864('873_result.json', json.loads(json.dumps(keep873, default=str, allow_nan=False)))
    except Exception as _exc873:
        print('RESULT_WRITE_FAILED', type(_exc873).__name__, _exc873, file=ERROR_CONSOLE864, flush=True)
    report873()
    if not EVENTS_FILE866.closed:
        EVENTS_FILE866.close()
    LOG_FILE864.close()
exec(compile(ENGINE873['suffix'], 'test870.py:suffix', 'exec'), globals())      # package, Drive copy, download (I/O)
