# AKBASCORE SILICON HIPPOCAMPUS — TEST875 — NATIVE SELECTIVE-WRITE / FULL-READ RECONCILIATION
# One A100-SXM4-80GB Colab cell. The locked engine is loaded once; only C's L4-L79 write is counterfactual.
import ast as _a874, hashlib as _h874, json as _j874, urllib.request as _u874
ENGINE_URL875 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB875, MARKER875 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', 'AKBASCORE SILICON HIPPOCAMPUS — TEST875'

def blob875(raw):
    return _h874.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()

def engine_parts875():
    with _u874.urlopen(_u874.Request(ENGINE_URL875, headers={'User-Agent': 'AKBASCORE-TEST875'}), timeout=240) as r:
        raw = r.read()
    assert blob875(raw) == ENGINE_BLOB875, ('ENGINE_BLOB_MISMATCH', blob875(raw))
    text = raw.decode('utf-8'); _a874.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST875_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST875_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST875_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('875_engine.log', '875_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST875_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '875_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '875_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST875_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old)
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL875, 'git_blob': blob875(raw), 'sha256': _h874.sha256(raw).hexdigest()}

ENGINE875, ENGINE_INFO875 = engine_parts875()
exec(compile(ENGINE875['prefix'], 'test870.py:prefix', 'exec'), globals())
exec(compile(ENGINE875['body'], 'test870.py:engine', 'exec'), globals())
print('TEST875 ENGINE', _j874.dumps(ENGINE_INFO875, sort_keys=True))
LOCKS864.update({'test870.py': ENGINE_BLOB875, 'Test870.log': 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc',
                 '873.py': '2e44affa5e0dd462155fb265c331270fb8e7b7e1',
                 '873.log': '1c9eb9fca173003eaf45bc7726af13c2817324b7',
                 '874.py': '12172001ba3696ad91087a8b34d7995728259e47'})
TEST870_MINUTES = TEST865_MINUTES = 55.0
WORLDS875 = ('00', '01'); SIDES875 = SIDES874 = tuple('I867_%s_%s' % (w, c) for w in WORLDS875 for c in ('MISSING', 'LIVE'))
ARM875, PRE_STEP875, POST_STEP875 = 'V_X', 2, 3
FUNCS873 = ('kv873', 'length873', 'forward873', 'car873', 'resolve_append873', 'append_card873', 'decide873',
            'probs873', 'same873', 'tv873')
CORRECTIVE875 = ('STOP', 'REJECT', 'BACKTRACK'); ARMS875 = ('H', 'W', 'WP', 'H-O0', 'W-O0')
ROPE_TOL875, REPRO_TOL875, ROUND_TOL875 = 1e-2, 6e-4, 2e-2
ROUND_TOL874 = ROUND_TOL875; ONE_SHOT_TOL875 = 2e-2
SHIFT_MIN875, LIVE_TOL875, CONTROL_GAP875, EFFECT_TV875 = .20, .10, .10, .10
PREREG875 = {'timeline': '[M_t2][X2_task_prompt][X2_state][A][C][X3]', 'sides': SIDES875, 'arms': ARMS875,
    'W_write_mask': 'X2_state+A, C upper L4-L79 only', 'WP_write_mask': 'equal-length immediately preceding task-prompt tail',
    'read': 'H/W/WP full causal; O0 masks C for X3 and every cropped CAR continuation',
    'gates': {'identity_cache_rel_max': ROUND_TOL875, 'identity_and_O0_CAR_dp': REPRO_TOL875,
              'one_shot_dp': ONE_SHOT_TOL875, 'lower_K_rephase': ROPE_TOL875},
    'correction': {'corrective': CORRECTIVE875, 'shift_min': SHIFT_MIN875, 'live_tolerance': LIVE_TOL875,
                   'matched_control_gap': CONTROL_GAP875, 'effect_TV_or_argmax': EFFECT_TV875},
    'continuation': 'only model-native W=REJECT/BACKTRACK; new MOUNTED outcome uses X3_state+A selective write; X4 full read',
    'classes': ['SELECTIVE_WRITE_CORRECTION', 'WRITE_EFFECT_WITHOUT_CORRECTION', 'NO_SELECTIVE_WRITE_EFFECT',
                'NONSPECIFIC_MASK_EFFECT', 'TECHNICAL_BLOCK']}
PREREG_SHA875 = sha256_bytes864(_j874.dumps(PREREG875, sort_keys=True).encode())
STATE875 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO875, 'prereg_sha256': PREREG_SHA875, 'source': {},
            'ref873': {}, 'sides': {}, 'blocks': [], 'outcome': None, 'error': None}
T2_KEEP875, STASH875 = {}, {}

def line875(*parts): short864('T875', *parts)
def capture_source875():
    try:
        hist = [t for t in get_ipython().history_manager.input_hist_raw if MARKER875 in t and 'def probe875' in t]
        source, how = hist[-1], 'IPYTHON_CELL'
    except (NameError, IndexError):
        source = open(__file__, encoding='utf-8').read() if '__file__' in globals() else None; how = 'FILE_%RUN'
    assert source and MARKER875 in source, 'EXECUTED_875_SOURCE_NOT_CAPTURED'
    tree = _a874.parse(source); banned = {'register_forward_hook', 'register_forward_pre_hook',
        'install_all_output_capturing_hooks', 'output_hidden_states', 'output_attentions', 'backward', 'requires_grad_'}
    for node in tree.body:
        if isinstance(node, _a874.FunctionDef) and node.name.endswith('875') and node.name != 'capture_source875':
            used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in _a874.walk(node) if isinstance(c, _a874.Call)} | {k.arg for k in _a874.walk(node) if isinstance(k, _a874.keyword)}
            bad = used & banned
            if node.name != 'step2_875': bad |= used & {'execute866', 'hop865', 'feedback869', 'mount865', 'free865'}
            assert not bad, ('FIREWALL875', node.name, sorted(bad))
    calls = [n for n in _a874.walk(tree) if isinstance(n, _a874.Call) and getattr(n.func, 'id', None) == 'reproduce_pre859859']
    assert len(calls) == 1, 'MODEL_LOADER_CALL_COUNT_NOT_ONE'
    for name, value in (('xray_point870', 'probe875'), ('control_step869', 'stash_control875')):
        rs = [n for n in tree.body if isinstance(n, _a874.Assign) and any(getattr(t, 'id', '') == name for t in n.targets)]
        assert len(rs) == 1 and getattr(rs[0].value, 'id', None) == value, ('FIREWALL875_REBIND', name)
    (ROOT864 / '875.py').write_text(source, encoding='utf-8')
    STATE875['source'] = {'how': how, 'sha256': sha256_bytes864(source.encode()), 'git_blob': git_blob864(source.encode()),
                          'lines': source.count('\n') + 1, 'firewall': 'PASS'}

def load875():
    names = ('load873_874', 'ref873_874', 'keep874', 'forward874', 'car874', 'rows874', 'decide874', 'rel874', 'oneshot874')
    tree = _a874.parse(RAW_SOURCES864['874.py'].decode(), filename='874.py')
    nodes = [n for n in tree.body if isinstance(n, _a874.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    exec(compile(_a874.fix_missing_locations(_a874.Module(body=nodes, type_ignores=[])), '874.py:selected', 'exec'), globals())
    load873_874()

def mask875(env, q, k, q0, block):
    qp = q0 + torch.arange(q, device=env['DEV']); kp = torch.arange(k, device=env['DEV'])
    allowed = qp[:, None] >= kp[None, :]
    if block is not None: allowed[:, block[0]:block[1]] = False
    assert bool(allowed.any(dim=-1).all()), 'FULLY_MASKED_QUERY'
    ans = torch.zeros((1, 1, q, k), dtype=env['DTYPE'], device=env['DEV'])
    return ans.masked_fill_(~allowed, torch.finfo(env['DTYPE']).min)

def append875(env, kv, cid, block):
    # Locked native_append_direct body; the sole computational change is its explicit 4-D causal additive SDPA mask.
    assert getattr(env['model'].config, '_attn_implementation', None) == 'sdpa', 'SDPA_REQUIRED'
    cp, _ = APPEND873['load'](cid); g = env['native_append_direct'].__globals__
    n = lambda name: g[name] if name in g else env[name]
    memory = list(kv); oldn = length873(env, memory); P, CUT, NL = int(n('P')), int(n('CUT')), int(n('NL'))
    q = int(cp['n'] - P); assert q > 0 and (block is None or 0 <= block[0] < block[1] <= oldn)
    body, seals, old_lower = cp['h'][:, P:, :], n('full_kv_seal')(memory), tuple(memory[:CUT + 1])
    upper = env['cache_build'](memory)
    for i in range(NL): memory[i] = None
    gc.collect()
    with n('DirectCut3')(n('model').model.layers[CUT], 'inject', source=body) as bridge:
        for st in range(0, q, int(n('CHUNK'))):
            m = min(int(n('CHUNK')), q - st); n('ensure_room')(m + 512); bridge.offset = st
            pos = torch.arange(oldn + st, oldn + st + m, device=env['DEV'])
            am = mask875(env, m, oldn + st + m, oldn + st, block)
            out = n('model')(inputs_embeds=torch.zeros((1, m, env['H']), device=env['DEV'], dtype=env['DTYPE']),
                past_key_values=upper, attention_mask=am, position_ids=pos.unsqueeze(0), cache_position=pos,
                use_cache=True, return_dict=True)
            upper = out.past_key_values; del out, am
    grown = list(n('pairs')(upper))
    for i in range(CUT + 1):
        ok, ov = old_lower[i]; k, v = cp['lower'][i]; shifted = []
        for st in range(0, q, int(n('CHUNK'))):
            end = min(q, st + int(n('CHUNK')))
            shifted.append(n('rephase')(k[:, :, P + st:P + end], torch.arange(P + st, P + end, device=env['DEV']),
                                        torch.arange(oldn + st, oldn + end, device=env['DEV'])))
        grown[i] = (torch.cat([ok] + shifted, dim=-2), torch.cat((ov, v[:, :, P:, :]), dim=-2))
    for i, ((nk, nv), (kh, vh)) in enumerate(zip(grown, seals)):
        assert n('kv_digest')(nk[:, :, :oldn]) == kh and n('kv_digest')(nv[:, :, :oldn]) == vh, ('PREFIX_CHANGED', i)
    assert len(grown) == NL and length873(env, grown) == oldn + q
    del upper, old_lower, cp
    return grown, oldn

def dp875(a, b): return max(abs(float(a['normalized'][w]) - float(b['normalized'][w])) for w in a['normalized'])
def seg875(kv, a, b, layers):
    return [(kv[i][0][:, :, a:b], kv[i][1][:, :, a:b]) for i in layers]
def arm875(reading): return {'action': reading['action'], 'p': probs873(reading)}
def corr875(p): return sum(p[w] for w in CORRECTIVE875)
def tv875(a, b): return .5 * sum(abs(a['p'][w] - b['p'][w]) for w in a['p'])

def stash_control875(env, ctx, candidate, pointer, feedback):
    out = _LOCKED_CONTROL_STEP875(env, ctx, candidate, pointer, feedback)
    if ctx['spec']['item'] in SIDES875 and ctx['steps'] + 1 == POST_STEP875:
        STASH875[ctx['spec']['item']] = {'candidate': candidate, 'control': out[0], 'state': out[2]}
    return out

def step2_875(env, ctx, side, state, action, cache3, keep3, seg, pre, post):
    st = STASH875.pop(side, None); assert st is not None and st['state'] is state
    ids = dict(ACTION_IDS867)
    ctx2 = dict(ctx, M=list(ctx['M']), path=list(ctx['path']), events=list(ctx['events']),
                mount_records=list(ctx['mount_records']), own_states=list(ctx['own_states']), prev_state=state['own_state'],
                memx=[tuple(t.clone() for t in kv) for kv in ctx['memx']])
    effect = execute866(env, ctx2, action, st['candidate'], st['control'], state); row = ctx2['events'][-1]
    res = {'run': True, 'action': action, 'effect': effect, 'chosen': row.get('chosen'), 'new_outcome': None}
    n3 = int(cache3.get_seq_length()); forward874(env, cache3, env['embed841'](ids[action]), n3, keep3, 1)
    kv4 = [cache_kv870(cache3, l) for l in range(int(env['NL']))]; del cache3
    n_action = n3 + len(ids[action])
    if effect == 'MOUNTED':
        block = (seg['X3_state'][0], n_action); cid = row.get('chosen'); assert cid
        kv4, n4 = append875(env, kv4, cid, block); assert n4 == n_action
        res['new_outcome'] = {'card': cid, 'write_mask_X3_state_A': block, 'read': 'FULL_CAUSAL'}
    k = len(ctx2['path']); pointer = None if k == 0 else ctx2['path'][-1]['rows']
    h4, kind = hop865(env, ctx2['memx'], ctx2['spec']['qid'], k, pointer); res['hop4'] = h4['text']
    if kind == 'EMPTY_OUTPUT': res['end'] = 'NATIVE_EMPTY_OUTPUT'
    else:
        feedback, _ = feedback869(env, ctx2); control4, record4, state4 = _LOCKED_CONTROL_STEP875(env, ctx2, h4, pointer, feedback)
        if control4 is None: res['end'] = 'NATIVE_EMPTY_STATE'
        else:
            names = slot_names869(env, list(state4['segments']))
            X4, _ = env['make_x851'](pre, [s for s, n in zip(state4['segments'], names) if n not in ('FV', 'FK')], post)
            r4, _ = decide874(env, kv4, X4, [])
            res['X4_W_policy'] = {'action': r4['action'], 'p': probs873(r4), 'read_mask': []}
    del kv4, ctx2['memx']
    return res

def probe875(env, ctx, record, state, label):
    side = ctx['spec']['item']; q = env['QTEXT841'][ctx['spec']['qid']]
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
    out = STATE875['sides'].setdefault(side, {'checks': {}, 'arms': {}, 'lengths': {}, 'error': None})
    c, arms, t0 = out['checks'], out['arms'], time.perf_counter()
    try:
        ids = dict(ACTION_IDS867)
        if ctx['steps'] == PRE_STEP875:
            out['t2_action'] = record['action']; assert record['action'] == 'ACQUIRE'
            segs2 = list(state['segments']); X2, _ = env['make_x851'](pre, segs2, post); L2, lp = int(X2.shape[0]), len(pre)
            assert lp + sum(len(x) + (0 if r is None else int(r.shape[0])) for x, r in segs2) + len(post) == L2, 'X2_LAYOUT'
            m2 = [tuple(t.clone() for t in kv) for kv in ctx['memx']]; n2 = length873(env, m2)
            cache = env['cache_build'](list(m2)); c['t2_CAR_equals_record'] = same873(car873(env, cache, X2), record['reading'])
            c['t2_crops'] = int(cache.get_seq_length()) == n2 + L2
            own = env['cache_build'](list(kv873(env, cache))); del cache
            forward873(env, own, env['embed841'](ids['ACQUIRE']), n2 + L2); keep_own = kv873(env, own); del own
            c['commit_length'] = length873(env, keep_own) == n2 + L2 + len(ids['ACQUIRE'])
            out['one_shot_diagnostic'], one = oneshot874(env, m2, X2, ids['ACQUIRE'], keep_own)
            c['one_shot_not_semantic'] = out['one_shot_diagnostic']['class'] != 'SEMANTIC'
            T2_KEEP875[side] = {'own': keep_own, 'one': one, 'n2': n2, 'L2': L2, 'lp': lp}
            out['lengths'].update({'M_t2': n2, 'X2': L2, 'X2_task_prompt': lp, 'X2_state': L2 - lp, 'A': len(ids['ACQUIRE'])})
            assert c['t2_CAR_equals_record'] and c['t2_crops'] and c['commit_length']; del m2
            return
        vram0 = vram_begin870(); z = T2_KEEP875.pop(side); n2, L2, lp = z['n2'], z['L2'], z['lp']
        memx = ctx['memx']; eff = [e for e in ctx['events'] if e.get('type') == 'EFFECT'][-1]; card = eff.get('chosen')
        body = int(env['entries'][card]['body_tokens']); n3 = int(memx[0][0].shape[-2]); out['card'] = card
        c['card_mounted'] = eff.get('effect') == 'MOUNTED' and list(ctx['M'])[-1] == card
        names = slot_names869(env, list(state['segments']))
        segs3 = [s for s, n in zip(state['segments'], names) if n not in ('FV', 'FK')]
        X3, _ = env['make_x851'](pre, segs3, post)
        L3 = int(X3.shape[0]); assert lp + sum(len(x) + (0 if r is None else int(r.shape[0])) for x, r in segs3) + len(post) == L3, 'X3_LAYOUT'
        seal0 = prefix_seals865(env, memx); hook0 = assert_hook_free859(env, 'T875_before_' + side)
        gH, n_before = append_card873(env, z['own'], card); rH, totalH = decide873(env, gH, X3); arms['H'] = arm875(rH)
        x3s = n_before + body; seg = {'X2_state': [n2 + lp, n2 + L2], 'A': [n2 + L2, n_before],
                                      'C': [n_before, x3s], 'X3_state': [x3s + lp, x3s + L3]}; out['segments'] = seg
        c['segments'] = n_before == n2 + L2 + len(ids['ACQUIRE']) and length873(env, gH) == x3s and totalH == x3s + L3
        cut, rephase = APPEND873['CUT'], APPEND873['rephase']
        c['lower_V_bitwise'] = all(torch.equal(gH[i][1][:, :, n_before:], memx[i][1][:, :, n3 - body:]) for i in range(cut + 1))
        rope = max(float(torch.linalg.vector_norm(rephase(gH[i][0][:, :, n_before:], torch.arange(n_before, x3s, device=env['DEV']),
            torch.arange(n3 - body, n3, device=env['DEV'])).float() - memx[i][0][:, :, n3 - body:].float())) /
            max(float(torch.linalg.vector_norm(memx[i][0][:, :, n3 - body:].float())), 1e-30) for i in range(cut + 1))
        c['lower_K_rephase'] = rope <= ROPE_TOL875
        gB, _ = append_card873(env, [tuple(t.clone() for t in kv) for kv in z['own']], card)
        c['H_rebuild'] = same873(rH, decide873(env, gB, X3)[0]); del gB
        ref = STATE875['ref873'][side]['T1']; c['H_reproduces_873'] = rH['action'] == ref['action'] and all(
            abs(arms['H']['p'][w] - ref['p'][w]) <= REPRO_TOL875 for w in ref['p'])
        gO, _ = append_card873(env, z['one'], card); rO, _ = decide873(env, gO, X3); one_dp = dp875(rH, rO)
        c['one_shot_dp'] = one_dp <= ONE_SHOT_TOL875 and c['one_shot_not_semantic']; del gO, rO
        assert c['card_mounted'] and c['H_rebuild'] and c['one_shot_dp'] and c['H_reproduces_873'] and c['lower_V_bitwise'] and c['lower_K_rephase'] and c['segments']
        # Identity calibration must pass on this timeline before any selective write.
        gI, _ = append875(env, z['own'], card, None); rI, _ = decide873(env, gI, X3)
        irel = rel874(seg875(gH, n_before, x3s, range(int(env['NL']))), seg875(gI, n_before, x3s, range(int(env['NL']))))
        idp = dp875(rH, rI); c['identity_cache'] = max(irel) <= ROUND_TOL875
        c['identity_CAR'] = rI['action'] == rH['action'] and idp <= REPRO_TOL875
        out['calibration'] = {'I_action': rI['action'], 'I_p': probs873(rI), 'cache_max_rel': max(irel), 'CAR_max_dp': idp,
                              'one_shot_max_dp': one_dp, 'locked_873_one_shot_max_dp': STATE875['ref873'][side]['one_shot_max_dp']}
        del gI, rI; assert c['identity_cache'] and c['identity_CAR'], 'TECHNICAL_BLOCK_IDENTITY'
        w0, w1 = n2 + lp, n_before; wp0 = w0 - (w1 - w0); assert wp0 >= n2
        gW, _ = append875(env, z['own'], card, (w0, w1)); gWP, _ = append875(env, z['own'], card, (wp0, w0))
        out['write_masks'] = {'W': [w0, w1], 'WP': [wp0, w0]}; assert w1 - w0 == w0 - wp0
        c['write_lower_bitwise'] = all(torch.equal(x, y) for g in (gW, gWP) for i in range(4)
            for x, y in zip(seg875(gH, n_before, x3s, [i])[0], seg875(g, n_before, x3s, [i])[0]))
        c['L4_C_invariant'] = all(torch.equal(x, y) for x, y in zip(seg875(gH, n_before, x3s, [4])[0],
                                                                     seg875(gW, n_before, x3s, [4])[0]))
        out['W_L5plus_C_max_rel'] = max(rel874(seg875(gH, n_before, x3s, range(5, 80)), seg875(gW, n_before, x3s, range(5, 80))))
        rHx, rowsH, _, _ = decide874(env, gH, X3, [], rows=True); c['empty_read_equals_native'] = same873(rH, rHx)
        rW, rowsW, cache3, keep3 = decide874(env, gW, X3, [], rows=True, hold=True); arms['W'] = arm875(rW)
        rWP, rowsWP, _, _ = decide874(env, gWP, X3, [], rows=True); arms['WP'] = arm875(rWP)
        rHO, rowsHO, _, _ = decide874(env, gH, X3, [seg['C']], rows=True); arms['H-O0'] = arm875(rHO)
        rWO, rowsWO, _, _ = decide874(env, gW, X3, [seg['C']], rows=True); arms['W-O0'] = arm875(rWO)
        c['X3_lower_H_W_WP'] = all(torch.equal(x, y) for rows in (rowsW, rowsWP) for i in range(4) for x, y in zip(rowsH[i], rows[i]))
        o0dp, o0rel = dp875(rHO, rWO), max(rel874(rowsHO, rowsWO))
        c['O0_null'] = rHO['action'] == rWO['action'] and o0dp <= REPRO_TOL875 and o0rel <= ROUND_TOL875
        out['O0'] = {'CAR_max_dp': o0dp, 'X3_cache_max_rel': o0rel}; assert c['O0_null'], 'TECHNICAL_BLOCK_O0_DIVERGENCE'
        g_seal = prefix_seals865(env, gH, n_before)
        c['timeline_unchanged'] = g_seal == prefix_seals865(env, gW, n_before) == prefix_seals865(env, gWP, n_before)
        c['memory_seal'] = prefix_seals865(env, memx) == seal0
        assert all(c[k] for k in ('write_lower_bitwise', 'L4_C_invariant', 'empty_read_equals_native',
                                  'X3_lower_H_W_WP', 'timeline_unchanged', 'memory_seal')), 'TECHNICAL_BLOCK_BEFORE_CONTINUATION'
        out['step2'] = {'run': False, 'reason': 'W=%s; no physical corrective continuation' % rW['action']}
        if rW['action'] in ('REJECT', 'BACKTRACK'):
            out['step2'] = step2_875(env, ctx, side, state, rW['action'], cache3, keep3, seg, pre, post)
        else: del cache3
        del rowsH, rowsW, rowsWP, rowsHO, rowsWO, gH, gW, gWP, z
        STASH875.pop(side, None); hook1 = assert_hook_free859(env, 'T875_after_' + side)
        c['hook_free'] = not any(x['hook_count'] or x['transformers_output_capturing_installed'] for x in (hook0, hook1))
        out['vram'] = vram_end870(vram0)
    except Exception as exc:
        out['error'] = '%s: %s' % (type(exc).__name__, str(exc)[:400]); out['traceback'] = traceback.format_exc()
        (ROOT864 / ('875_%s_t%d_traceback.txt' % (side, ctx['steps']))).write_text(out['traceback'], encoding='utf-8')
        line875('POINT_ERROR', side, 't=%d' % ctx['steps'], out['error'])
    finally:
        gc.collect(); env['release'](); out['seconds_t%d' % ctx['steps']] = round(time.perf_counter() - t0, 3)
    line875('POINT', side, _j874.dumps(c, sort_keys=True, default=str), '' if not out['error'] else out['error'])

xray_point870 = probe875
_LOCKED_CONTROL_STEP875 = control_step869
control_step869 = stash_control875

def outcome875():
    reps = {r.get('item'): r for r in STATE870['replays']}; blocks = list(STATE875['blocks'])
    need = ('t2_CAR_equals_record', 't2_crops', 'commit_length', 'one_shot_not_semantic', 'card_mounted', 'segments',
            'lower_V_bitwise', 'lower_K_rephase', 'H_rebuild', 'H_reproduces_873', 'one_shot_dp', 'identity_cache', 'identity_CAR',
            'write_lower_bitwise', 'L4_C_invariant', 'empty_read_equals_native', 'X3_lower_H_W_WP', 'O0_null',
            'timeline_unchanged', 'memory_seal', 'hook_free')
    for side in SIDES875:
        s = STATE875['sides'].get(side)
        if reps.get(side, {}).get('ok') is not True: blocks.append('REPLAY_NOT_EXACT:' + side)
        if not s or s.get('error') or any(a not in s.get('arms', {}) for a in ARMS875): blocks.append('INCOMPLETE:' + side)
        elif not all(s['checks'].get(k) for k in need): blocks.append('CHECK:%s:%s' % (side, [k for k in need if not s['checks'].get(k)]))
    res = {'blocks': blocks, 'worlds': {}}
    if blocks: res['outcome'] = 'TECHNICAL_BLOCK'; STATE875['outcome'] = res; return res
    effects, nonspecific, correction = False, False, True
    for w in WORLDS875:
        m, l = (STATE875['sides']['I867_%s_%s' % (w, c)]['arms'] for c in ('MISSING', 'LIVE'))
        def corrective(a): return m[a]['action'] in CORRECTIVE875 and corr875(m[a]['p']) - corr875(m['H']['p']) >= SHIFT_MIN875 and m['H']['p']['ACQUIRE'] - m[a]['p']['ACQUIRE'] >= SHIFT_MIN875
        wc, pc = corrective('W'), corrective('WP'); live = l['W']['action'] == 'ACCEPT' and l['W']['p']['ACCEPT'] >= l['H']['p']['ACCEPT'] - LIVE_TOL875
        gap = corr875(m['W']['p']) - corr875(m['WP']['p']) >= CONTROL_GAP875
        we = any(m[a]['action'] != m['H']['action'] or tv875(m[a], m['H']) >= EFFECT_TV875 for a in ('W',))
        wp_similar = tv875(m['W'], m['WP']) < EFFECT_TV875 and m['W']['action'] == m['WP']['action'] and tv875(m['WP'], m['H']) >= EFFECT_TV875
        live_similar = tv875(l['W'], l['WP']) < EFFECT_TV875 and l['W']['action'] == l['WP']['action'] and (tv875(l['WP'], l['H']) >= EFFECT_TV875 or l['WP']['action'] != l['H']['action'])
        row = {'W_corrective': wc, 'WP_corrective': pc, 'LIVE_W_ACCEPT_kept': live, 'specificity_gap': gap,
               'W_effect': we, 'WP_similar_effect': wp_similar, 'LIVE_WP_similar_effect': live_similar}; res['worlds'][w] = row
        effects |= we or tv875(l['W'], l['H']) >= EFFECT_TV875 or l['W']['action'] != l['H']['action']
        nonspecific |= pc or wp_similar or live_similar; correction &= wc and live and not pc and gap and not wp_similar and not live_similar
    res['outcome'] = ('SELECTIVE_WRITE_CORRECTION' if correction else 'NONSPECIFIC_MASK_EFFECT' if nonspecific else
                      'WRITE_EFFECT_WITHOUT_CORRECTION' if effects else 'NO_SELECTIVE_WRITE_EFFECT')
    STATE875['outcome'] = res; return res

def report875():
    words = ('ACQUIRE', 'BACKTRACK', 'REJECT', 'STOP', 'ACCEPT', 'ADVANCE')
    print('=' * 100); print('TEST875 | GPU', CC_GPU.get('name'), '| source', STATE875['source'].get('git_blob'), '| prereg', PREREG_SHA875[:16])
    for side in SIDES875:
        s = STATE875['sides'].get(side)
        if not s: print(side, 'not reached'); continue
        print(side, 't2', s.get('t2_action'), 'card', s.get('card'), 'lengths', _j874.dumps(s['lengths']))
        for name in ARMS875:
            if name in s['arms']:
                a = s['arms'][name]; print('  %-5s %-9s' % (name, a['action']), ' '.join('%s=%.3f' % (w, a['p'][w]) for w in words), 'corr=%.3f' % corr875(a['p']))
        print('  calibration', _j874.dumps(s.get('calibration'), sort_keys=True), 'O0', _j874.dumps(s.get('O0'), sort_keys=True))
        print('  continuation', _j874.dumps(s.get('step2'), default=str), 'ERROR', s.get('error'))
    o = STATE875['outcome'] or {}; print('WORLDS', _j874.dumps(o.get('worlds'), sort_keys=True), 'BLOCKS', o.get('blocks'))
    directions = {'TECHNICAL_BLOCK': 'Önce cache/mask/one-shot bütünlüğü; mekanizma iddiası yok.',
        'NO_SELECTIVE_WRITE_EFFECT': 'En küçük sonraki yön A: X2_state bilgisinin C upper yazımına girip girmediğini ölç.',
        'WRITE_EFFECT_WITHOUT_CORRECTION': 'En küçük sonraki yön B: full-read CAR eylem eşleşmesini incele; maskeyi büyütme.',
        'NONSPECIFIC_MASK_EFFECT': 'En küçük sonraki yön A/B: bağlam silme ile seçici yazımı ayır; reconciliation iddiası yok.',
        'SELECTIVE_WRITE_CORRECTION': 'Yalnız modelin seçtiği fiziksel devamı doğrula; selective-write/full-read adayını koru.'}
    print('NEXT', directions.get(o.get('outcome'), 'Yön yok'))
    print('TEST875 OUTCOME', o.get('outcome'), '| status', STATE875['status'], '| wall %.0fs' % (time.perf_counter() - T_START875),
          '| peak GPU %.2f GiB' % (max(STATE870['costs'].get('session_peak_allocated_bytes', 0),
          torch.cuda.max_memory_allocated() if torch.cuda.is_available() else 0) / 2**30))
    print('GPU EXECUTION BY CODE AUTHOR: NOT_EXECUTED; behavioral failure is not a technical PASS.')

T_START875 = time.perf_counter()
try:
    STATE875['status'] = 'GATE0'; capture_source875()
    json_write864('875_prereg.json', {'prereg': PREREG875, 'sha256': PREREG_SHA875, 'before_model_load': True})
    load_sources865(); load875(); STATE875['ref873'] = ref873_874(RAW_SOURCES864['873.log'].decode())
    for name, needles in (('Test870.log', ('XR870 CALIBRATION CALIBRATION_PASS', 'NVIDIA A100')),
                          ('873.log', ('TEST873 OUTCOME', 'status COMPLETE', 'NVIDIA A100'))):
        assert all(x in RAW_SOURCES864[name].decode() for x in needles), ('LOCKED_LOG_NOT_COMPLETE', name)
    feasibility_audit864(); audit_contracts865(); load_spine864(); REFS875 = load_records870()
    for w in WORLDS875:
        sha = {}
        for cnd in ('MISSING', 'LIVE'):
            ctl = [e['record'] for e in REFS875[('I867_%s_%s' % (w, cnd), ARM875)]['events'] if e['type'] == 'CONTROL']
            assert [x['action'] for x in ctl[:2]] == ['ADVANCE', 'ACQUIRE']; sha[cnd] = ctl[PRE_STEP875 - 1]['state_sha256']
        assert sha['MISSING'] == sha['LIVE']
    STATE875['status'] = 'GATE1'; assert CC_GPU_OK, ('GPU_PRECHECK', CC_GPU)
    env875, original_error875, original_trace875, reproduction875 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace875; TWO_JOB_VERIFICATION864 = verify_two_job859(env875, original_trace875)
    assert_hook_free859(env875, 'T875_before_native'); install_offline_evaluator859(env875)
    native875 = native_sequences860(env875); NATIVE_REGRESSION864 = native_regression864(env875, native875)
    verify_864_reference865(NATIVE_REGRESSION864); ANALYSIS864 = run_analysis863(env875, native875)
    assert len(STATE863['restores']) == 3 and all(r['exact'] for r in STATE863['restores'])
    digest875 = records_digest861(env875); null_seal875 = physical_seal863(env875, env875['MEMNULL841'])
    runtime_contracts865(env875); runtime_preflight865(env875, reproduction875); rearm_budget865(env875); make_slots866(env875)
    SLOTS867['PREV_EVALUATION'] = list(env875['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env875); resolve_append873(env875)
    assert getattr(env875['model'].config, '_attn_implementation', None) == 'sdpa'
    assert not any(p.requires_grad for p in env875['model'].parameters())
    assert_hook_free859(env875, 'T875_before_points'); STATE875['status'] = 'RUNNING'; T0_865 = time.perf_counter()
    by_key875 = build_specs869(env875)
    for side in SIDES875:
        rep = run_replay870(env875, {'id': side, 'item': side, 'arm': ARM875,
            'targets': {PRE_STEP875: 'T2_TIMELINE', POST_STEP875: 'T3_SELECTIVE_WRITE'}}, by_key875, REFS875)
        T2_KEEP875.pop(side, None); STASH875.pop(side, None)
        if not rep['ok']: STATE875['blocks'].append('REPLAY_NOT_EXACT:' + side)
    hook = hook_audit859(env875, 'T875_final')
    if records_digest861(env875) != digest875 or physical_seal863(env875, env875['MEMNULL841']) != null_seal875 or hook['hook_count'] or hook['transformers_output_capturing_installed']:
        STATE875['blocks'].append('POST_RUN_INTEGRITY')
    STATE875['status'] = 'COMPLETE'; outcome875()
except BaseException as exc:
    STATE875['error'] = '%s: %s' % (type(exc).__name__, exc); STATE875['traceback'] = traceback.format_exc()
    STATE875['status'] = 'FAILED_AT_' + str(STATE875['status'])
    STATE875['outcome'] = {'outcome': 'TECHNICAL_BLOCK', 'blocks': ['EXCEPTION: ' + STATE875['error'][:300]]}
    (ROOT864 / '875_traceback.txt').write_text(STATE875['traceback'], encoding='utf-8')
    print('TEST875 ERROR', STATE875['error'][:300], '| full traceback:', ROOT864 / '875_traceback.txt', file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        result = dict(STATE875, replays=STATE870['replays'])
        json_write864('875_result.json', json.loads(json.dumps(result, default=str, allow_nan=False)))
    except Exception as exc: print('RESULT_WRITE_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    report875()
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE875['suffix'], 'test870.py:suffix', 'exec'), globals())
