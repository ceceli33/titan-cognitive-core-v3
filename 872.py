# AKBASCORE SILICON HIPPOCAMPUS — TEST872 — NATIVE RESIDUAL STATE TRANSITION
# ONE HYPOTHESIS: can the real residual change caused by a physical action (h_post - h_pre, same layer, same token
# rows, same positions) change the frozen model's next decision in a way that is specific to the physical outcome?
# World I867_01 (arm V_X): MISSING and LIVE are bit-identical up to the t2 decision (ACQUIRE); then the locked engine
# mounts a different card (MISSING: no link, LIVE: the link). Both loops are replayed bit-exactly against the 869 record.
#   h_pre / h_post: residual entering decoder layer LAYER872 at the last token of [t2 decision context + the model's own
#     action word], computed on the post-action memory with the acquired card masked (pre) / visible (post). Same
#     tokens, same RoPE positions, same memory prefix (append-only, prior_prefix_exact): only the card differs.
#   delta = h_post - h_pre (a physical-outcome residual change, NOT an expectation error).
#   Decision at t3: the locked CAR reading, recomputed layer by layer (hook-free twin of TEST870) with
#     h_junction = h_native + ALPHA872 * delta added at the last row before layer LAYER872; the frozen layers above,
#     norm and lm_head run unchanged. A: no injection (must reproduce the record exactly), B: real delta (MISSING),
#     C: norm-matched random delta (MISSING), D: real delta (LIVE).
# Python never chooses, forbids or reweights an action. No training, hooks, RAG, text replay, routing or forced answers.
# HOW TO RUN (A100 80GB): paste this whole file into ONE Colab cell and run it once.
import ast as _a872, hashlib as _h872, json as _j872, urllib.request as _u872

ENGINE_URL872 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB872 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc'       # test870.py: the cell run on the A100 in TEST870
ENGINE_LOG_BLOB872 = 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc'   # Test870.log (A100, CALIBRATION_PASS)
MARKER872 = 'AKBASCORE SILICON HIPPOCAMPUS — TEST872'


def blob872(raw):
    return _h872.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def engine_parts872():
    # The GPU-verified engine runs unchanged; only output file/folder names are renamed (each rename counted).
    with _u872.urlopen(_u872.Request(ENGINE_URL872, headers={'User-Agent': 'AKBASCORE-TEST872'}), timeout=240) as r:
        raw = r.read()
    assert blob872(raw) == ENGINE_BLOB872, ('ENGINE_BLOB_MISMATCH', blob872(raw))
    text = raw.decode('utf-8')
    _a872.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST872_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST872_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST872_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('872_engine.log', '872_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST872_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '872_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '872_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST872_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old, parts[where].count(old))
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL872, 'git_blob': blob872(raw), 'sha256': _h872.sha256(raw).hexdigest(),
                   'io_renames': len(renames)}


ENGINE872, ENGINE_INFO872 = engine_parts872()
exec(compile(ENGINE872['prefix'], 'test870.py:prefix', 'exec'), globals())      # console capture, GPU precheck (I/O)
exec(compile(ENGINE872['body'], 'test870.py:engine', 'exec'), globals())        # locked engine definitions (no run)
print('TEST872 ENGINE', _j872.dumps(ENGINE_INFO872, sort_keys=True))

# ============================ TEST872 — pre-registration (fixed before the model is loaded) ============================
LOCKS864.update({'test870.py': ENGINE_BLOB872, 'Test870.log': ENGINE_LOG_BLOB872})
TEST870_MINUTES = 30.0
TEST865_MINUTES = TEST870_MINUTES
WORLD872 = 1
ITEMS872 = {'MISSING': 'I867_01_MISSING', 'LIVE': 'I867_01_LIVE'}
ARM872, PRE_STEP872, POST_STEP872 = 'V_X', 2, 3
LAYER872 = 65            # residual entering decoder layer 65 (= output of layers 0..64; X-Ray index 65); fixed in advance
ALPHA872 = 1.0           # intervention scale: the measured change is added once; fixed, never searched
NORM_RATIO_MAX872 = 1.0  # ||ALPHA * delta|| / ||h_native|| above this -> TECHNICAL_BLOCK (no silent normalisation)
RANDOM_SEED872 = 872001
EFFECT_MIN872 = 0.20     # real delta must lower P(ACQUIRE) at the failed acquisition by at least this ...
MARGIN_MIN872 = 0.10     # ... and by at least this more than the random delta,
RANDOM_FRACTION872 = 0.5  # ... while the random delta does at most this fraction of the real effect,
LIVE_TOL872 = 0.10       # ... and in LIVE the native action and its probability (+-0.10) are kept.
PREREG872 = {
    'hypothesis': 'the real residual change caused by a physical action changes the next decision in a way specific '
                  'to the physical outcome',
    'world': ITEMS872, 'arm': ARM872, 'steps': [PRE_STEP872, POST_STEP872], 'layer': LAYER872, 'alpha': ALPHA872,
    'measurement': 'residual entering layer %d, last token of [t2 decision context + own action word tokens], on the '
                   't3 memory with the acquired card masked (pre) / visible (post); delta = post - pre' % LAYER872,
    'injection': 'at the t3 decision, last row, before layer %d: h <- h + alpha * delta; layers %d..79, norm, lm_head '
                 'and the CAR continuation run unchanged' % (LAYER872, LAYER872),
    'conditions': {'A': 'MISSING, no injection (must equal the recorded CAR exactly)',
                   'B': 'MISSING, real delta', 'C': 'MISSING, random delta, same shape and norm as B (seed %d)'
                   % RANDOM_SEED872, 'D': 'LIVE, real delta (LIVE native = no injection, must equal the record)'},
    'noop': 'delta of two independent passes on identical inputs == 0 bitwise; no-injection CAR == record bitwise',
    'outcomes': {'TRANSITION_EFFECT': 'r_B = P_acq(A) - P_acq(B) >= %.2f and r_B - r_C >= %.2f and |r_C| <= %.1f r_B '
                                      'and LIVE keeps its native action with |dP| <= %.2f' % (
                                          EFFECT_MIN872, MARGIN_MIN872, RANDOM_FRACTION872, LIVE_TOL872),
                 'NO_TRANSITION_EFFECT': 'otherwise, with all technical checks passing',
                 'TECHNICAL_BLOCK': 'any replay, no-op, alignment, mask, norm, seal or hook check fails'},
    'limits': ['one world: an engineering signal, not a population estimate',
               'delta is a physical-outcome residual change, not an expectation error']}
PREREG_SHA872 = sha256_bytes864(_j872.dumps(PREREG872, sort_keys=True).encode('utf-8'))
STATE872 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO872, 'prereg_sha256': PREREG_SHA872, 'source': {},
            't2': {}, 'sides': {}, 'blocks': [], 'outcome': None, 'error': None}


def line872(*parts):
    short864('T872', *parts)


def capture_source872():
    source, how = None, None
    try:
        hist = [t for t in get_ipython().history_manager.input_hist_raw if MARKER872 in t and 'def probe872' in t]
        if hist:
            source, how = hist[-1], 'IPYTHON_CELL'
    except NameError:
        pass
    if source is None and '__file__' in globals():
        with open(globals()['__file__'], encoding='utf-8') as f:
            source, how = f.read(), 'FILE_%RUN'
    assert source and MARKER872 in source, ('EXECUTED_872_SOURCE_NOT_CAPTURED: paste the whole TEST872 code into ONE '
                                            'Colab cell and run that cell')
    tree = _a872.parse(source)
    banned = {'execute866', 'mount865', 'free865', 'hop865', 'parse866', 'register_forward_hook',
              'register_forward_pre_hook', 'install_all_output_capturing_hooks', 'output_hidden_states',
              'output_attentions'}
    for node in tree.body:
        if isinstance(node, _a872.FunctionDef) and node.name.endswith('872') and node.name != 'capture_source872':
            used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in _a872.walk(node)
                    if isinstance(c, _a872.Call)} | {k.arg for k in _a872.walk(node) if isinstance(k, _a872.keyword)}
            assert not (used & banned), ('FIREWALL872', node.name, sorted(used & banned))
    rebinds = [n for n in tree.body if isinstance(n, _a872.Assign) and
               any(getattr(t, 'id', '') == 'xray_point870' for t in n.targets)]
    assert len(rebinds) == 1 and getattr(rebinds[0].value, 'id', None) == 'probe872', 'FIREWALL872_REBIND'
    (ROOT864 / '872.py').write_text(source, encoding='utf-8')
    STATE872['source'] = {'how': how, 'sha256': sha256_bytes864(source.encode('utf-8')),
                          'git_blob': git_blob864(source.encode('utf-8')), 'lines': source.count('\n') + 1,
                          'firewall': 'PASS'}


# ============================ new computation: hook-free layer-by-layer pass with one residual read/write point =========
def pass872(env, memx, Y, am, stop_at=None, inject=None):
    # Same calls and arguments as the GPU-verified twin870 (mask870, rotary_emb, layer_call870). Returns the residual
    # entering layer LAYER872 at the last row (before any injection), and, unless stopped there, the cache and the
    # first-token log-probabilities. inject (H,) is added to that row in float32 and cast back to the model dtype.
    base = env['model'].model
    L = int(Y.shape[0])
    n = int(memx[0][0].shape[-2])
    with torch.no_grad():
        cache = env['cache_build'](list(memx))
        pos = torch.arange(n, n + L, device=env['DEV'])
        pid2 = pos.unsqueeze(0)
        x3 = Y.reshape(1, L, env['H'])
        mask = mask870(base, x3, am, cache, pos, pid2)
        pe = base.rotary_emb(x3, pid2)
        h, h_row = x3, None
        for li, layer in enumerate(base.layers):
            if li == LAYER872:
                h_row = h[0, -1].clone()
                if stop_at == LAYER872:
                    del cache, mask, pe, h
                    return h_row, None, None
                if inject is not None:
                    h = h.clone()
                    h[0, -1] = (h[0, -1].float() + inject.to(h.device).float()).to(h.dtype)
            h = layer_call870(layer, h, mask, pid2, cache, pos, pe)
        first = torch.log_softmax(env['model'].lm_head(base.norm(h))[0, -1].float(), dim=-1)
        del h, mask, pe
    return h_row, cache, first


def car872(env, memx, pre, segments, post, inject=None):
    # car867 with its first forward replaced by pass872; the continuation of multi-token action words is car867's own
    # CROP path on the resulting cache (the injected row's keys/values in layers >= LAYER872 stay in that cache).
    env['budget849']()
    X, _ = env['make_x851'](pre, segments, post)
    L = int(X.shape[0])
    n = int(memx[0][0].shape[-2])
    longest = max(len(ids) for _, ids in ACTION_IDS867)
    assert n + L + longest <= env['MAX_FUSED_TOKENS'], ('CONTEXT_LIMIT', n, L)
    am = torch.ones((1, n + L), device=env['DEV'], dtype=torch.long)
    h_native, cache, first = pass872(env, memx, X, am, inject=inject)
    env['COUNT834']['probe_forwards'] += 1
    scores, top = [], torch.topk(first, 10)
    with torch.no_grad():
        for word, ids in ACTION_IDS867:
            token_logps = [float(first[ids[0]])]
            if len(ids) > 1:
                m = len(ids) - 1
                p2 = torch.arange(n + L, n + L + m, device=env['DEV'])
                out = env['model'](inputs_embeds=env['embed841'](ids[:-1]).reshape(1, m, env['H']), past_key_values=cache,
                                   attention_mask=torch.ones((1, n + L + m), device=env['DEV'], dtype=torch.long),
                                   position_ids=p2.unsqueeze(0), cache_position=p2, use_cache=True, return_dict=True)
                lp = torch.log_softmax(out.logits[0].float(), dim=-1)
                cache.crop(-m)
                assert int(cache.get_seq_length()) == n + L, 'CROP_LENGTH_MISMATCH_872'
                env['COUNT834']['probe_forwards'] += 1
                token_logps += [float(lp[i, ids[i + 1]]) for i in range(m)]
                del out, lp
            scores.append({'word': word, 'ids': ids, 'token_logps': token_logps,
                           'sequence_logp': float(sum(token_logps)), 'hard_greedy_ids': []})
        del cache
    car = {'scores': scores, 'path': 'CROP', 'fallback_reason': None,
           'first_top10': {'ids': [int(i) for i in top.indices.tolist()]}, 'X_sha256': None}
    return reading867(car), h_native


def norm872(v):
    return float(torch.linalg.vector_norm(v.detach().float().cpu()))


def probs872(reading):
    return {w: round(float(p), 6) for w, p in reading['normalized'].items()}


def same_logps872(a, b):
    return [(s['word'], s['token_logps']) for s in a['scores']] == [(s['word'], s['token_logps']) for s in b['scores']]


def probe872(env, ctx, record, state, label):
    # Called by the sealed replay tap (its return value is ignored by the loop). t2: keep the decision context and the
    # model's own action. t3: measure delta and read the decision under the declared conditions.
    item, side = ctx['spec']['item'], ('MISSING' if ctx['spec']['item'].endswith('MISSING') else 'LIVE')
    q = env['QTEXT841'][ctx['spec']['qid']]
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q)))
    post = env['REVIEW_SUFFIX851']
    if ctx['steps'] == PRE_STEP872:
        STATE872['t2'][side] = {'pre': pre, 'segments': [(s, r) for s, r in state['segments']], 'action': record['action']}
        line872('T2_CONTEXT_KEPT', item, 'own action=%s' % record['action'])
        return
    t0 = time.perf_counter()
    vram0 = vram_begin870()
    out = {'item': item, 'checks': {}, 'conditions': {}, 'norms': {}, 'error': None}
    STATE872['sides'][side] = out
    c = out['checks']
    try:
        t2 = STATE872['t2'][side]
        memx, n_post = ctx['memx'], int(ctx['memx'][0][0].shape[-2])
        eff = [e for e in ctx['events'] if e.get('type') == 'EFFECT'][-1]
        card = eff.get('chosen')
        mount = eff.get('mount') or {}
        body = int(env['entries'][card]['body_tokens'])
        mounted = list(ctx['M'])
        c['t2_action'] = t2['action']
        c['acquired_card'] = card
        c['card_is_last_mounted'] = eff.get('effect') == 'MOUNTED' and mounted[-1] == card
        c['prior_prefix_exact'] = mount.get('prior_prefix_exact') is True and int(mount.get('n', -1)) == n_post
        c['spans_add_up'] = int(env['P']) + sum(int(env['entries'][x]['body_tokens']) for x in mounted) == n_post
        c['mount_order_sealed'] = SEALS865.get(tuple(mounted)) == prefix_seals865(env, memx)
        c['card_span'] = [n_post - body, n_post]
        assert all(c[k] for k in ('card_is_last_mounted', 'prior_prefix_exact', 'spans_add_up', 'mount_order_sealed')), c
        a_ids = dict(ACTION_IDS867)[t2['action']]
        X2, _ = env['make_x851'](t2['pre'], t2['segments'], post)
        Y = torch.cat([X2, env['embed841'](a_ids)], dim=0)
        am_post = torch.ones((1, n_post + int(Y.shape[0])), device=env['DEV'], dtype=torch.long)
        am_pre = am_post.clone()
        am_pre[0, n_post - body:n_post] = 0
        seal0 = prefix_seals865(env, memx)
        hook0 = assert_hook_free859(env, 'T872_before_' + item)
        h_post, _, _ = pass872(env, memx, Y, am_post, stop_at=LAYER872)
        h_post2, _, _ = pass872(env, memx, Y, am_post, stop_at=LAYER872)
        h_pre, _, _ = pass872(env, memx, Y, am_pre, stop_at=LAYER872)
        delta = (h_post.float() - h_pre.float()).cpu()
        c['noop_delta_bitwise_zero'] = bool(torch.equal(h_post, h_post2))
        c['mask_changes_state'] = norm872(delta) > 0.0
        out['norms'].update({'h_pre': norm872(h_pre), 'h_post': norm872(h_post), 'delta': norm872(delta),
                             'noop_delta': norm872(h_post2.float() - h_post.float())})
        out['delta'] = delta
        del h_post2, X2, Y
        native, h_native = car872(env, memx, pre, list(state['segments']), post, inject=None)
        c['noop_injection_equals_record'] = same_logps872(native, record['reading'])
        out['norms']['h_native_t3'] = norm872(h_native)
        out['norms']['ratio'] = ALPHA872 * out['norms']['delta'] / max(out['norms']['h_native_t3'], 1e-30)
        c['norm_ratio_ok'] = out['norms']['ratio'] <= NORM_RATIO_MAX872
        out['conditions']['A' if side == 'MISSING' else 'LIVE_NATIVE'] = {'action': native['action'], 'p': probs872(native)}
        assert c['noop_delta_bitwise_zero'] and c['noop_injection_equals_record'] and c['mask_changes_state'] and \
            c['norm_ratio_ok'], ('NOOP_OR_SCALE_CHECK_FAILED', c, out['norms'])
        injections = {'B': delta, 'C': None} if side == 'MISSING' else {'D': delta}
        if side == 'MISSING':
            g = torch.Generator(device='cpu').manual_seed(RANDOM_SEED872)
            rnd = torch.randn(int(delta.shape[0]), generator=g, dtype=torch.float32)
            injections['C'] = rnd * (norm872(delta) / norm872(rnd))
            out['norms']['random_delta'] = norm872(injections['C'])
        for name, vec in injections.items():
            reading, _ = car872(env, memx, pre, list(state['segments']), post, inject=ALPHA872 * vec)
            out['conditions'][name] = {'action': reading['action'], 'p': probs872(reading)}
        hook1 = assert_hook_free859(env, 'T872_after_' + item)
        c['memory_seal_unchanged'] = prefix_seals865(env, memx) == seal0
        c['hook_free'] = not (hook0['hook_count'] or hook1['hook_count'] or hook0['transformers_output_capturing_installed']
                              or hook1['transformers_output_capturing_installed'])
    except Exception as exc:
        out['error'] = '%s: %s' % (type(exc).__name__, str(exc)[:400])
        out['traceback'] = traceback.format_exc()
        short864('T872 POINT_ERROR', item, out['traceback'])
    finally:
        gc.collect()
        env['release']()
    out['seconds'] = round(time.perf_counter() - t0, 3)
    out['vram'] = vram_end870(vram0)
    line872('POINT', item, _j872.dumps({k: v for k, v in c.items()}, sort_keys=True, default=str),
            'norms=%s' % _j872.dumps({k: round(v, 4) for k, v in out['norms'].items()}, sort_keys=True),
            's=%.1f' % out['seconds'], '' if out['error'] is None else 'ERROR=' + out['error'])


xray_point870 = probe872      # the sealed replay tap calls this name at the declared steps; its return value is ignored


def outcome872():
    M, Lv = STATE872['sides'].get('MISSING') or {}, STATE872['sides'].get('LIVE') or {}
    reps = {r.get('item'): r for r in STATE870['replays']}
    blocks = list(STATE872['blocks'])
    for side, s, need in (('MISSING', M, ('A', 'B', 'C')), ('LIVE', Lv, ('LIVE_NATIVE', 'D'))):
        if reps.get(ITEMS872[side], {}).get('ok') is not True:
            blocks.append('REPLAY_NOT_EXACT:' + side)
        if not s or s.get('error') or any(k not in s.get('conditions', {}) for k in need):
            blocks.append('POINT_INCOMPLETE:' + side)
        elif not (s['checks'].get('memory_seal_unchanged') and s['checks'].get('hook_free')):
            blocks.append('INTEGRITY:' + side)
    res = {'blocks': blocks}
    if not blocks:
        cm, cl = M['conditions'], Lv['conditions']
        r_b = cm['A']['p']['ACQUIRE'] - cm['B']['p']['ACQUIRE']
        r_c = cm['A']['p']['ACQUIRE'] - cm['C']['p']['ACQUIRE']
        act = cl['LIVE_NATIVE']['action']
        live_ok = cl['D']['action'] == act and abs(cl['D']['p'][act] - cl['LIVE_NATIVE']['p'][act]) <= LIVE_TOL872
        dm, dl = M['delta'], Lv['delta']
        res.update({'r_B': round(r_b, 4), 'r_C': round(r_c, 4), 'live_native_action': act, 'live_kept': live_ok,
                    'B_minus_C': {w: round(cm['B']['p'][w] - cm['C']['p'][w], 4) for w in cm['B']['p']},
                    'B_minus_A': {w: round(cm['B']['p'][w] - cm['A']['p'][w], 4) for w in cm['B']['p']},
                    'D_minus_LIVE_NATIVE': {w: round(cl['D']['p'][w] - cl['LIVE_NATIVE']['p'][w], 4) for w in cl['D']['p']},
                    'cos_delta_MISSING_LIVE': round(float(torch.nn.functional.cosine_similarity(dm, dl, dim=0)), 4)})
        effect = r_b >= EFFECT_MIN872 and r_b - r_c >= MARGIN_MIN872 and abs(r_c) <= RANDOM_FRACTION872 * r_b and live_ok
        res['outcome'] = 'GECIS ETKISI VAR' if effect else 'GECIS ETKISI YOK'
    else:
        res['outcome'] = 'TEKNIK ENGEL'
    STATE872['outcome'] = res
    return res


def report872():
    print('=' * 100)
    print('TEST872 — NATIVE RESIDUAL STATE TRANSITION | GPU %s | engine test870.py %s | source %s (%s)' % (
        CC_GPU.get('name'), ENGINE_BLOB872, STATE872['source'].get('git_blob'), STATE872['source'].get('how')))
    print('layer %d (residual entering decoder layer %d) | alpha %.2f | prereg %s' % (LAYER872, LAYER872, ALPHA872,
                                                                                    PREREG_SHA872))
    for side in ('MISSING', 'LIVE'):
        s = STATE872['sides'].get(side)
        if not s:
            print('  %s: not reached' % side)
            continue
        c = s['checks']
        print('  %s %s | t2 own action %s -> acquired card %s span %s | noop_delta_zero=%s noop_injection=record:%s '
              'prior_prefix_exact=%s seal=%s hooks_free=%s' % (side, s['item'], c.get('t2_action'), c.get('acquired_card'),
                                                            c.get('card_span'), c.get('noop_delta_bitwise_zero'),
                                                            c.get('noop_injection_equals_record'),
                                                            c.get('prior_prefix_exact'), c.get('memory_seal_unchanged'),
                                                            c.get('hook_free')))
        print('     norms %s' % _j872.dumps({k: round(v, 4) for k, v in s['norms'].items()}, sort_keys=True))
        for name, r in s['conditions'].items():
            print('     %-12s %-9s ' % (name, r['action']) + '  '.join('%s %.3f' % (w, r['p'][w]) for w in (
                'STOP', 'ACQUIRE', 'REJECT', 'BACKTRACK', 'ADVANCE', 'ACCEPT')))
        print('     s=%.1f vram_overhead_gib=%s%s' % (s['seconds'], s['vram'].get('xray_overhead_allocated_gib', 'NA'),
                                                    '' if not s.get('error') else '  ERROR ' + s['error']))
    o = STATE872['outcome'] or {}
    print('  RESULT', _j872.dumps({k: v for k, v in o.items() if k != 'outcome'}, sort_keys=True))
    print('TEST872 OUTCOME %s | status %s | wall %.0f s | peak GPU %.2f GiB' % (
        o.get('outcome'), STATE872['status'], time.perf_counter() - T_START872,
        max(STATE870['costs'].get('session_peak_allocated_bytes', 0),
            torch.cuda.max_memory_allocated() if torch.cuda.is_available() else 0) / 2**30))
    print('delta = physical-outcome residual change, not an expectation error; one world = engineering signal only.')
    print('GPU EXECUTION NOT VERIFIED BY THE CODE AUTHOR before this run.')
    print('=' * 100)


# ============================ TEST872 — SINGLE CELL EXECUTION ============================
T_START872 = time.perf_counter()
try:
    STATE872['status'] = 'GATE0'
    capture_source872()
    json_write864('872_prereg.json', {'prereg': PREREG872, 'sha256': PREREG_SHA872, 'before_model_load': True})
    line872('GATE0 SOURCE', _j872.dumps(STATE872['source'], sort_keys=True), 'prereg', PREREG_SHA872)
    load_sources865()                                     # engine locks + test870.py + Test870.log, git-blob verified
    STATE865['gates']['GATE0_SOURCE'] = {'status': 'PASS', 'locks': len(LOCKS864)}
    log870 = RAW_SOURCES864['Test870.log'].decode('utf-8')
    assert 'XR870 CALIBRATION CALIBRATION_PASS' in log870 and 'NVIDIA A100' in log870, 'TEST870_LOG_NOT_A_PASS'
    feasibility_audit864()
    audit_contracts865()
    load_spine864()
    REFS872 = load_records870()                           # 869 full records (SHA-256, strict JSON)
    for side, item in ITEMS872.items():                   # the declared t2 identity and own action, from the record
        ctl = [e['record'] for e in REFS872[(item, ARM872)]['events'] if e['type'] == 'CONTROL']
        assert ctl[PRE_STEP872 - 1]['action'] == 'ACQUIRE', ('T2_NOT_ACQUIRE', item)
    sha = lambda it, k: [e['record'] for e in REFS872[(it, ARM872)]['events'] if e['type'] == 'CONTROL'][1]['state_sha256'][k]
    assert all(sha(ITEMS872['MISSING'], k) == sha(ITEMS872['LIVE'], k) for k in ('C', 'E', 'V', 'FV', 'FK')), 'T2_NOT_SHARED'
    line872('GATE0 PASS', 'MISSING and LIVE share the t2 state in the record; t2 own action ACQUIRE')
    STATE872['status'] = 'GATE1'
    assert CC_GPU_OK, ('GPU_PRECHECK_NOT_A100_80GB_WITH_40GIB_FREE', CC_GPU)
    env872, original_error872, original_trace872, reproduction872 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace872
    TWO_JOB_VERIFICATION864 = verify_two_job859(env872, original_trace872)
    assert_hook_free859(env872, 'T872_before_native_regression')
    install_offline_evaluator859(env872)
    native872 = native_sequences860(env872)
    NATIVE_REGRESSION864 = native_regression864(env872, native872)
    verify_864_reference865(NATIVE_REGRESSION864)
    ANALYSIS864 = run_analysis863(env872, native872)
    assert len(STATE863['restores']) == 3 and all(r['exact'] for r in STATE863['restores']), 'ORIGINAL_EXACT_RESTORE'
    digest872 = records_digest861(env872)
    null_seal872 = physical_seal863(env872, env872['MEMNULL841'])
    runtime_contracts865(env872)
    runtime_preflight865(env872, reproduction872)
    rearm_budget865(env872)
    make_slots866(env872)
    SLOTS867['PREV_EVALUATION'] = list(env872['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env872)
    assert LAYER872 < len(env872['model'].model.layers), 'LAYER_OUT_OF_RANGE'
    assert_hook_free859(env872, 'T872_before_points')
    line872('GATE1 PASS', 'model_load_s=%.0f' % (time.perf_counter() - T_START872))
    STATE872['status'] = 'RUNNING'
    T0_865 = time.perf_counter()
    by_key872 = build_specs869(env872)
    for side in ('MISSING', 'LIVE'):                     # MISSING first: C needs the MISSING delta norm
        rep872 = run_replay870(env872, {'id': side, 'item': ITEMS872[side], 'arm': ARM872,
                                        'targets': {PRE_STEP872: 'T2_DECISION', POST_STEP872: 'T3_DECISION'}},
                               by_key872, REFS872)
        if not rep872['ok']:
            STATE872['blocks'].append('REPLAY_NOT_EXACT:%s %s' % (side, _j872.dumps(rep872['mismatch'], default=str)[:300]))
            break
    # ====== OFFLINE: no model call below ======
    hook872 = hook_audit859(env872, 'T872_final')
    if records_digest861(env872) != digest872 or physical_seal863(env872, env872['MEMNULL841']) != null_seal872 or \
            hook872['hook_count'] or hook872['transformers_output_capturing_installed']:
        STATE872['blocks'].append('POST_RUN_INTEGRITY')
    STATE872['status'] = 'COMPLETE'
    outcome872()
except BaseException as exc:
    STATE872['error'] = '%s: %s' % (type(exc).__name__, exc)
    STATE872['traceback'] = traceback.format_exc()
    STATE872['status'] = 'FAILED_AT_' + str(STATE872['status'])
    STATE872['outcome'] = {'outcome': 'TEKNIK ENGEL', 'blocks': ['EXCEPTION: ' + STATE872['error'][:300]]}
    print(STATE872['traceback'], file=ERROR_CONSOLE864, flush=True)
    short864('TEST872 FULL TRACEBACK', STATE872['traceback'])
finally:
    try:
        keep = {k: v for k, v in STATE872.items() if k not in ('t2', 'sides')}
        keep['sides'] = {s: {k: v for k, v in d.items() if k != 'delta'} for s, d in STATE872['sides'].items()}
        keep['replays'] = STATE870['replays']
        json_write864('872_result.json', json.loads(json.dumps(keep, default=str, allow_nan=False)))
        torch.save({s: d['delta'] for s, d in STATE872['sides'].items() if 'delta' in d}, ROOT864 / '872_delta.pt')
    except Exception as _exc872:
        print('RESULT_WRITE_FAILED', type(_exc872).__name__, _exc872, file=ERROR_CONSOLE864, flush=True)
    report872()
    if not EVENTS_FILE866.closed:
        EVENTS_FILE866.close()
    LOG_FILE864.close()
exec(compile(ENGINE872['suffix'], 'test870.py:suffix', 'exec'), globals())      # package, Drive copy, download (I/O)
