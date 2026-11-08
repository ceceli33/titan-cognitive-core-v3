# AKBASCORE SILICON HIPPOCAMPUS — TEST874 — NATIVE CAUSAL STATE RECONCILIATION
# ONE QUESTION: on the TEST873 native KV timeline [M_t2][X2][A][C][X3], the model repeats the failed ACQUIRE in MISSING.
# If the next decision (X3 and its CAR reading) can no longer READ the previous decision state stored in X2, does the
# frozen model choose a corrective action (STOP / REJECT / BACKTRACK) for the failed physical outcome, keep ACCEPT for
# the successful one, and does an equal-size mask on a matched X2 segment fail to do the same?
#   X2 = [t2 copy of the control prompt (identical text is repeated in X3)][t2 state: C,E,R,P,FV,FK,V rows + suffix]
#   T1 no mask (TEST873 T1) | T2 X2 state not readable | T3 matched control: the same number of positions directly
#   before the X2 state (tail of the t2 prompt copy) not readable | T2_FULL whole X2 not readable (reported)
#   M0 Markov [M_t3][X3] | R recorded FV/FK decision.  Mechanism: a 2-D attention mask (0 = key not readable) on
#   every forward after X2 (X3 and the CAR continuations) in all 80 layers. A, C and every KV row stay as computed;
#   masking access is NOT deleting X2 (A and C were computed while X2 was visible). A physical-removal reference
#   (rows removed, RoPE positions kept) checks that the mask means "key removed" in every layer.
#   Before the arms: one numerical diagnostic of the TEST873 one-shot difference (two-step vs one-shot KV, per layer).
#   If T2's own reading is REJECT or BACKTRACK, the engine executes that word once (execute866 on a copy of the loop
#   state) and the model reads the next decision on the same masked timeline. STOP/ACCEPT are the model's own end.
# Python never chooses, forbids or reweights an action. HOW TO RUN (A100 80GB): paste into ONE Colab cell, run once.
import ast as _a874, hashlib as _h874, json as _j874, urllib.request as _u874

ENGINE_URL874 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB874 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc'       # test870.py: the engine run on the A100 (TEST870-873)
MARKER874 = 'AKBASCORE SILICON HIPPOCAMPUS — TEST874'


def blob874(raw):
    return _h874.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def engine_parts874():
    # The GPU-verified engine runs unchanged; only output file/folder names are renamed (each rename counted).
    with _u874.urlopen(_u874.Request(ENGINE_URL874, headers={'User-Agent': 'AKBASCORE-TEST874'}), timeout=240) as r:
        raw = r.read()
    assert blob874(raw) == ENGINE_BLOB874, ('ENGINE_BLOB_MISMATCH', blob874(raw))
    text = raw.decode('utf-8')
    _a874.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST874_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST874_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST874_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('874_engine.log', '874_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST874_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '874_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '874_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST874_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old, parts[where].count(old))
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL874, 'git_blob': blob874(raw), 'sha256': _h874.sha256(raw).hexdigest(),
                   'io_renames': len(renames)}


ENGINE874, ENGINE_INFO874 = engine_parts874()
exec(compile(ENGINE874['prefix'], 'test870.py:prefix', 'exec'), globals())      # console capture, GPU precheck (I/O)
exec(compile(ENGINE874['body'], 'test870.py:engine', 'exec'), globals())        # locked engine definitions (no run)
print('TEST874 ENGINE', _j874.dumps(ENGINE_INFO874, sort_keys=True))


# ============================ TEST874 — pre-registration (fixed before the model is loaded) ============================
# 873.py / 873.log arrive through the locked repository archive (load_sources865, CODELOAD864) and are git-blob checked.
LOCKS864.update({'test870.py': ENGINE_BLOB874, 'Test870.log': 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc',
                 '873.py': '2e44affa5e0dd462155fb265c331270fb8e7b7e1', '873.log': '1c9eb9fca173003eaf45bc7726af13c2817324b7'})
TEST870_MINUTES = 40.0
TEST865_MINUTES = TEST870_MINUTES
WORLDS874 = ('00', '01')
SIDES874 = tuple('I867_%s_%s' % (w, c) for w in WORLDS874 for c in ('MISSING', 'LIVE'))
ARM874, PRE_STEP874, POST_STEP874 = 'V_X', 2, 3
FUNCS873 = ('kv873', 'length873', 'forward873', 'car873', 'resolve_append873', 'append_card873', 'decide873',
            'probs873', 'same873', 'tv873')                # reused unchanged from the GPU-run 873.py (AST selection)
CORRECTIVE874 = ('STOP', 'REJECT', 'BACKTRACK')
SHIFT_MIN874 = 0.20        # MISSING, T2 vs T1: corrective mass up AND P(ACQUIRE) down by at least this
LIVE_TOL874 = 0.10         # LIVE, T2: own reading ACCEPT and P(ACCEPT) >= T1 - this
CONTROL_GAP874 = 0.10      # MISSING: corrective mass T2 - T3 at least this, and T3 alone is not a corrective shift
ROPE_TOL874 = 1e-2         # appended card lower keys re-rephased vs M_t3 keys, rel L2 (unchanged from TEST873)
REPRO_TOL874 = 6e-4        # T1 vs the T1 printed (3 decimals) in 873.log
ROUND_TOL874 = 2e-2        # one-shot diagnostic: layers 0-1 rel L2 above this = SEMANTIC (inputs/positions/mask differ)
MASK_RATIO874 = 0.25       # mask semantics: max rel(masked, removed) <= this * max rel(unmasked, removed), X3 rows, 80 layers
PREREG874 = {
    'question': 'does blocking read access to the previous decision state X2 turn the repeated failed ACQUIRE into a '
                'corrective action, keep ACCEPT on LIVE, and differ from an equal-size matched mask?',
    'sides': SIDES874, 'arm': ARM874, 'steps': [PRE_STEP874, POST_STEP874], 'reused_873': FUNCS873,
    'timeline': '[M_t2][X2 = t2 prompt copy + t2 state][A = own ACQUIRE tokens][C = own card, native append][X3]',
    'arms': {'T1': 'no mask', 'T2': 'X2 state (slots+rows+suffix) not readable by X3 and CAR',
             'T3': 'same number of positions directly before the X2 state (tail of the t2 prompt copy) not readable',
             'T2_FULL': 'whole X2 not readable (reported, not classified)', 'M0': '[M_t3][X3]', 'R': 'recorded FV/FK'},
    'mask': '2-D attention mask, 0 on the masked rows, every forward after X2 (X3 + CAR continuations), all 80 layers',
    'one_shot_diagnostic': 'two-step [X2][A] vs one-shot [X2+A] KV per layer and segment, plus one-shot rerun; '
                           'SEMANTIC if M_t2 rows differ or layer 0/1 rel > %g, else NUMERICAL (reported); the TEST873 '
                           'result stays TECHNICAL_BLOCK' % ROUND_TOL874,
    'technical': ['TEST873 t2/t3 checks (CAR == record, crops, commit, card lower V bitwise, lower K rel <= %g, '
                  'T1 rebuild identical, memory seal, hook-free)' % ROPE_TOL874,
                  'segment boundaries verified on the cache lengths', 'T1 == 873.log T1 within %g' % REPRO_TOL874,
                  'car874 with an empty mask == locked car873 (float equality)', 'mask semantics ratio <= %g' % MASK_RATIO874,
                  'timeline base KV seal unchanged by the arms', 'one-shot diagnostic not SEMANTIC'],
    'classification': {'CAUSAL_RECONCILIATION_EFFECT': 'in BOTH worlds: MISSING T2 reading in %s, corrective mass '
                       'T2-T1 >= %.2f and P_acq T1-T2 >= %.2f; LIVE T2 reading ACCEPT, P_acc >= T1-%.2f; MISSING T3 not '
                       'such a shift and corrective mass T2-T3 >= %.2f' % (CORRECTIVE874, SHIFT_MIN874, SHIFT_MIN874,
                                                                           LIVE_TOL874, CONTROL_GAP874),
                       'NO_RECONCILIATION_EFFECT': 'technical checks pass, condition fails',
                       'TECHNICAL_BLOCK': 'replay, cache, mask, position or numerical-semantics check fails'},
    'step2': 'per side, if the T2 reading is REJECT or BACKTRACK: execute866 on a copy of the loop state, engine hop + '
             'evidence + evaluation on the executed memory, commit the action tokens, mask the X2 and X3 states (and the '
             'rejected card rows), read the next CAR decision; STOP/ACCEPT = model end; reported, not classified'}
PREREG_SHA874 = sha256_bytes864(_j874.dumps(PREREG874, sort_keys=True).encode('utf-8'))
STATE874 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO874, 'prereg_sha256': PREREG_SHA874, 'source': {},
            'ref873': {}, 'sides': {}, 'blocks': [], 'outcome': None, 'error': None}
T2_KEEP874, STASH874 = {}, {}


def line874(*parts):
    short864('T874', *parts)


def capture_source874():
    source, how = None, None
    try:
        hist = [t for t in get_ipython().history_manager.input_hist_raw if MARKER874 in t and 'def probe874' in t]
        if hist:
            source, how = hist[-1], 'IPYTHON_CELL'
    except NameError:
        pass
    if source is None and '__file__' in globals():
        with open(globals()['__file__'], encoding='utf-8') as f:
            source, how = f.read(), 'FILE_%RUN'
    assert source and MARKER874 in source, 'EXECUTED_874_SOURCE_NOT_CAPTURED: paste the whole TEST874 code into ONE cell'
    tree = _a874.parse(source)
    banned = {'register_forward_hook', 'register_forward_pre_hook', 'install_all_output_capturing_hooks',
              'output_hidden_states', 'output_attentions', 'mount865', 'free865', 'backward', 'requires_grad_'}
    loop_io = {'execute866', 'hop865', 'feedback869'}          # engine loop I/O: only inside step2_874, on a state copy
    for node in tree.body:
        if isinstance(node, _a874.FunctionDef) and node.name.endswith('874') and node.name != 'capture_source874':
            used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in _a874.walk(node)
                    if isinstance(c, _a874.Call)} | {k.arg for k in _a874.walk(node) if isinstance(k, _a874.keyword)}
            bad = used & (banned if node.name == 'step2_874' else banned | loop_io)
            assert not bad, ('FIREWALL874', node.name, sorted(bad))
    for name, value in (('xray_point870', 'probe874'), ('control_step869', 'stash_control874')):
        rebinds = [n for n in tree.body if isinstance(n, _a874.Assign) and any(getattr(t, 'id', '') == name for t in n.targets)]
        assert len(rebinds) == 1 and getattr(rebinds[0].value, 'id', None) == value, ('FIREWALL874_REBIND', name)
    (ROOT864 / '874.py').write_text(source, encoding='utf-8')
    STATE874['source'] = {'how': how, 'sha256': sha256_bytes864(source.encode('utf-8')),
                          'git_blob': git_blob864(source.encode('utf-8')), 'lines': source.count('\n') + 1, 'firewall': 'PASS'}


def load873_874():
    # the GPU-run TEST873 timeline functions, unchanged (AST selection of the blob-locked 873.py)
    tree = _a874.parse(RAW_SOURCES864['873.py'].decode('utf-8'), filename='873.py')
    nodes = [n for n in tree.body if (isinstance(n, _a874.FunctionDef) and n.name in FUNCS873) or (
        isinstance(n, _a874.Assign) and [getattr(t, 'id', '') for t in n.targets] == ['APPEND873'])]
    assert sorted(getattr(n, 'name', 'APPEND873') for n in nodes) == sorted(FUNCS873 + ('APPEND873',)), 'SELECT_873'
    exec(compile(_a874.fix_missing_locations(_a874.Module(body=nodes, type_ignores=[])), '873.py:selected', 'exec'), globals())


def ref873_874(text):
    # T1 decision (printed, 3 decimals) and one-shot dP per side, from the locked 873.log
    out, side = {}, None
    for line in text.splitlines():
        if line.startswith('T873 POINT '):
            _, _, name, rest = line.split(' ', 3)
            out.setdefault(name, {})['one_shot_max_dp'] = _j874.loads(rest.split(' lengths=')[0])['one_shot_max_dp']
        elif line.startswith('  I867_') and ' | t2 own action ' in line:
            side = line.split()[0]
        else:
            t = line.split()
            if side and len(t) == 16 and t[0] == 'T1' and t[14] == 'dACQ_vs_M0':
                out.setdefault(side, {})['T1'] = {'action': t[1], 'p': {t[i]: float(t[i + 1]) for i in range(2, 14, 2)}}
    assert all('T1' in out.get(s, {}) and 'one_shot_max_dp' in out.get(s, {}) for s in SIDES874), ('REF873', sorted(out))
    return out


# ============================ new computation: masked reads on the timeline ============================
def keep874(env, n, ranges):
    keep = torch.ones(n, dtype=torch.long, device=env['DEV'])
    for a, b in ranges:
        assert 0 <= a < b <= n, ('MASK_RANGE', a, b, n)
        keep[a:b] = 0
    return keep


def forward874(env, cache, Y, pos0, keep, last):
    # forward873 with (a) keep: 0 = cache row not readable (2-D attention mask, every layer) or (b) RoPE positions
    # pos0.. above the physical cache length (removal reference). Returns log-probs of the last `last` rows.
    L, nc = int(Y.shape[0]), int(cache.get_seq_length())
    assert pos0 >= nc and pos0 + L <= int(env['MAX_FUSED_TOKENS']), ('TIMELINE_LENGTH', nc, pos0, L)
    am = torch.ones((1, nc + L), device=env['DEV'], dtype=torch.long)
    if keep is not None:
        assert int(keep.shape[0]) == nc and pos0 == nc, ('KEEP_LENGTH', int(keep.shape[0]), nc, pos0)
        am[0, :nc] = keep
    pos, cpos = torch.arange(pos0, pos0 + L, device=env['DEV']), torch.arange(nc, nc + L, device=env['DEV'])
    with torch.no_grad():
        out = env['model'](inputs_embeds=Y.reshape(1, L, env['H']), past_key_values=cache, attention_mask=am,
                           position_ids=pos.unsqueeze(0), cache_position=cpos, use_cache=True, return_dict=True)
        logp = torch.log_softmax(out.logits[0, -last:].float(), dim=-1)
        del out
    assert int(cache.get_seq_length()) == nc + L, 'TIMELINE_NOT_EXTENDED'
    return logp


def car874(env, cache, X, pos0, keep):
    # car873 procedure (teacher-forced continuations, each cropped) through forward874; returns the reading and the
    # keep vector over [cache][X] for later forwards
    env['budget849']()
    L = int(X.shape[0])
    n1, p1 = int(cache.get_seq_length()) + L, pos0 + L
    assert p1 + max(len(ids) for _, ids in ACTION_IDS867) <= int(env['MAX_FUSED_TOKENS']), ('CONTEXT_LIMIT', p1)
    first = forward874(env, cache, X, pos0, keep, 1)[0]
    keep1 = None if keep is None else torch.cat([keep, torch.ones(L, dtype=keep.dtype, device=keep.device)])
    scores = []
    for word, ids in ACTION_IDS867:
        token_logps = [float(first[ids[0]])]
        if len(ids) > 1:
            m = len(ids) - 1
            lp = forward874(env, cache, env['embed841'](ids[:-1]), p1, keep1, m)
            cache.crop(-m)
            assert int(cache.get_seq_length()) == n1, 'CAR_CROP_LENGTH_MISMATCH_874'
            token_logps += [float(lp[i, ids[i + 1]]) for i in range(m)]
            del lp
        scores.append({'word': word, 'ids': ids, 'token_logps': token_logps,
                       'sequence_logp': float(sum(token_logps)), 'hard_greedy_ids': []})
    top = torch.topk(first, 10)
    return reading867({'scores': scores, 'path': 'CROP', 'fallback_reason': None,
                       'first_top10': {'ids': [int(i) for i in top.indices.tolist()]}, 'X_sha256': None}), keep1


def rows874(env, cache, L):
    return [(k[:, :, -L:].clone(), v[:, :, -L:].clone()) for k, v in (cache_kv870(cache, l) for l in range(int(env['NL'])))]


def decide874(env, kv, X, ranges, rows=False, hold=False):
    # masked arm on its own DynamicCache over the shared timeline tensors (cat/crop never write into them)
    cache = env['cache_build'](list(kv))
    n0 = int(cache.get_seq_length())
    reading, keep1 = car874(env, cache, X, n0, keep874(env, n0, ranges))
    got = rows874(env, cache, int(X.shape[0])) if rows else None
    if not hold:
        del cache
        cache = None
    return reading, got, cache, keep1


def removed874(env, kv, X, ranges):
    # reference: the masked rows physically absent, every other row (and its RoPE position) unchanged
    keep = keep874(env, length873(env, kv), ranges).bool()
    cache = env['cache_build']([(k[:, :, keep, :], v[:, :, keep, :]) for k, v in kv])
    reading, _ = car874(env, cache, X, int(keep.shape[0]), None)
    got = rows874(env, cache, int(X.shape[0]))
    del cache
    return reading, got


def rel874(a, b):
    # per layer: max over K and V of relative L2 (0.0 when bitwise equal)
    out = []
    for pa, pb in zip(a, b):
        r = 0.0
        for x, y in zip(pa, pb):
            if not torch.equal(x, y):
                r = max(r, float(torch.linalg.vector_norm(x.float() - y.float())) /
                        max(float(torch.linalg.vector_norm(y.float())), 1e-30))
        out.append(r)
    return out


def oneshot874(env, m2, X2, a_ids, two):
    # TEST873 open gate: two-step [X2][A] (car873 forward + crops, then the action forward) vs one-shot [X2+A]
    n2, L2, la = length873(env, m2), int(X2.shape[0]), len(a_ids)
    runs = []
    for _ in range(2):
        one = env['cache_build']([tuple(t.clone() for t in kv) for kv in m2])
        forward873(env, one, torch.cat([X2, env['embed841'](a_ids)], dim=0), n2)
        runs.append(kv873(env, one))
        del one
    segs = (('M_t2', 0, n2), ('X2', n2, n2 + L2), ('A', n2 + L2, n2 + L2 + la))
    per = {s: rel874([(k[:, :, a:b], v[:, :, a:b]) for k, v in two], [(k[:, :, a:b], v[:, :, a:b]) for k, v in runs[0]])
           for s, a, b in segs}
    first = next(({'layer': l, 'segment': s, 'rel': per[s][l]} for l in range(int(env['NL'])) for s, _, _ in segs
                  if per[s][l] > 0), None)
    rerun = all(torch.equal(x, y) for p, q in zip(runs[0], runs[1]) for x, y in zip(p, q))
    del runs[1]
    semantic = any(per['M_t2']) or any(per[s][l] > ROUND_TOL874 for s in ('X2', 'A') for l in (0, 1))
    diag = {'class': 'SEMANTIC' if semantic else ('NUMERICAL_ORDER_DETERMINISTIC' if rerun else
                                                  'NUMERICAL_ORDER_NONDETERMINISTIC'),
            'first_difference': first, 'one_shot_rerun_bitwise': rerun, 'dtype': str(two[0][0].dtype),
            'layer0': {s: per[s][0] for s in per}, 'layer1': {s: per[s][1] for s in per},
            'max': {s: [max(per[s]), per[s].index(max(per[s]))] for s in per}, 'last_layer': {s: per[s][-1] for s in per},
            'calls_two_step': [{'q_len': L2, 'cache_position': [n2, n2 + L2 - 1], 'mask': 'ones(%d)' % (n2 + L2),
                                'then': 'CAR continuations, each cropped'},
                               {'q_len': la, 'cache_position': [n2 + L2, n2 + L2 + la - 1], 'mask': 'ones(%d)' % (n2 + L2 + la)}],
            'calls_one_shot': [{'q_len': L2 + la, 'cache_position': [n2, n2 + L2 + la - 1], 'mask': 'ones(%d)' % (n2 + L2 + la)}],
            'positions_equal': list(range(n2, n2 + L2)) + list(range(n2 + L2, n2 + L2 + la)) == list(range(n2, n2 + L2 + la))}
    return diag, runs[0]


def card_range874(env, cid, m2_cards, card, seg):
    # rows of a rejected card on the timeline: M_t2 bodies in mount order (cspans834 convention) or the appended C
    if cid == card:
        return tuple(seg['C'])
    pos = int(env['P'])
    for c in m2_cards:
        b = int(env['entries'][c]['body_tokens'])
        if c == cid:
            return pos, pos + b
        pos += b
    raise AssertionError(('REJECTED_CARD_NOT_ON_TIMELINE', cid))


def stash_control874(env, ctx, candidate, pointer, feedback):
    # pass-through of the locked control_step869: keeps the t3 objects that execute866 needs for step 2
    out = _LOCKED_CONTROL_STEP874(env, ctx, candidate, pointer, feedback)
    if ctx['spec']['item'] in SIDES874 and ctx['steps'] + 1 == POST_STEP874:
        STASH874[ctx['spec']['item']] = {'candidate': candidate, 'control': out[0], 'state': out[2]}
    return out


def step2_874(env, ctx, side, state, action, cache3, keep3, seg, m2_cards, card, pre, post):
    # the model's own T2 word, executed once by the engine on a copy of the loop state; next decision on the timeline
    st = STASH874.pop(side, None)
    assert st is not None and st['state'] is state, 'STASH_NOT_T3_STATE'
    ids = dict(ACTION_IDS867)
    ctx2 = dict(ctx, M=list(ctx['M']), path=list(ctx['path']), events=list(ctx['events']),
                mount_records=list(ctx['mount_records']), own_states=list(ctx['own_states']),
                prev_state=state['own_state'], memx=[tuple(t.clone() for t in kv) for kv in ctx['memx']])
    effect = execute866(env, ctx2, action, st['candidate'], st['control'], state)
    row = ctx2['events'][-1]
    res = {'action_t3': action, 'effect': effect, 'chosen': row.get('chosen'), 'mounted_after': list(ctx2['M']),
           'path_after': [p['text'] for p in ctx2['path']]}
    n3 = int(cache3.get_seq_length())
    forward874(env, cache3, env['embed841'](ids[action]), n3, keep3, 1)        # commit the executed word
    drop = [tuple(seg['X2_state']), tuple(seg['X3_state'])]
    if effect == 'UNMOUNTED':
        drop.append(card_range874(env, res['chosen'], m2_cards, card, seg))
    kv4 = [cache_kv870(cache3, l) for l in range(int(env['NL']))]
    k = len(ctx2['path'])
    pointer = None if k == 0 else ctx2['path'][-1]['rows']
    h4, kind = hop865(env, ctx2['memx'], ctx2['spec']['qid'], k, pointer)
    res['hop4'] = h4['text']
    if kind != 'EMPTY_OUTPUT':
        feedback, _ = feedback869(env, ctx2)
        control4, record4, state4 = _LOCKED_CONTROL_STEP874(env, ctx2, h4, pointer, feedback)
        if control4 is None:
            res['end'] = 'NATIVE_EMPTY_STATE'
        else:
            names = slot_names869(env, list(state4['segments']))
            X4, _ = env['make_x851'](pre, [s for s, n in zip(state4['segments'], names) if n not in ('FV', 'FK')], post)
            r4, _, _, _ = decide874(env, kv4, X4, drop)
            m4, _ = decide873(env, ctx2['memx'], X4)
            res.update({'T2_step4': {'action': r4['action'], 'p': probs873(r4)}, 'M0_step4': {'action': m4['action'],
                        'p': probs873(m4)}, 'R_step4': {'action': record4['action'], 'p': probs873(record4['reading'])},
                        'masked': drop, 'lengths': {'timeline': n3 + len(ids[action]), 'X4': int(X4.shape[0])}})
    else:
        res['end'] = 'NATIVE_EMPTY_OUTPUT'
    del kv4, ctx2['memx']
    return res


def probe874(env, ctx, record, state, label):
    # Called by the sealed replay tap (return value ignored). t2: timeline + one-shot diagnostic. t3: arms.
    side = ctx['spec']['item']
    q = env['QTEXT841'][ctx['spec']['qid']]
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q)))
    post = env['REVIEW_SUFFIX851']
    out = STATE874['sides'].setdefault(side, {'checks': {}, 'arms': {}, 'lengths': {}, 'error': None})
    c, arms = out['checks'], out['arms']
    t0 = time.perf_counter()
    try:
        ids = dict(ACTION_IDS867)
        if ctx['steps'] == PRE_STEP874:
            out['t2_action'] = record['action']
            assert record['action'] == 'ACQUIRE', ('T2_NOT_ACQUIRE', record['action'])
            segs = list(state['segments'])
            X2, _ = env['make_x851'](pre, segs, post)
            L2, lp = int(X2.shape[0]), len(pre)
            assert lp + sum(len(s) + (0 if r is None else int(r.shape[0])) for s, r in segs) + len(post) == L2, 'X2_LAYOUT'
            assert lp >= L2 - lp, ('MATCHED_CONTROL_TOO_SHORT', lp, L2 - lp)
            m2 = [tuple(t.clone() for t in kv) for kv in ctx['memx']]
            n2 = length873(env, m2)
            cache = env['cache_build'](list(m2))
            c['t2_timeline_car_equals_record'] = same873(car873(env, cache, X2), record['reading'])
            c['t2_cache_after_crops'] = int(cache.get_seq_length()) == n2 + L2
            own = env['cache_build'](list(kv873(env, cache)))
            del cache
            forward873(env, own, env['embed841'](ids['ACQUIRE']), n2 + L2)
            keep_own = kv873(env, own)
            del own
            c['timeline_after_commit'] = length873(env, keep_own) == n2 + L2 + len(ids['ACQUIRE'])
            c['committed_tokens'] = ids['ACQUIRE']
            out['one_shot_diagnostic'], one = oneshot874(env, m2, X2, ids['ACQUIRE'], keep_own)
            c['one_shot_not_semantic'] = out['one_shot_diagnostic']['class'] != 'SEMANTIC'
            T2_KEEP874[side] = {'own': keep_own, 'one_shot': one, 'n2': n2, 'L2': L2, 'lp': lp, 'm2_cards': list(ctx['M'])}
            out['lengths'].update({'M_t2': n2, 'X2': L2, 'X2_task_prompt': lp, 'X2_state': L2 - lp, 'A': len(ids['ACQUIRE'])})
            del m2
            assert c['t2_timeline_car_equals_record'] and c['t2_cache_after_crops'] and c['timeline_after_commit'], c
            line874('T2_TIMELINE', side, 'lengths=%s' % _j874.dumps(out['lengths']),
                    'one_shot=%s' % _j874.dumps(out['one_shot_diagnostic'], sort_keys=True))
            return
        vram0 = vram_begin870()
        keep = T2_KEEP874.pop(side)
        n2, L2, lp = keep['n2'], keep['L2'], keep['lp']
        memx, n3 = ctx['memx'], int(ctx['memx'][0][0].shape[-2])
        eff = [e for e in ctx['events'] if e.get('type') == 'EFFECT'][-1]
        card = eff.get('chosen')
        body = int(env['entries'][card]['body_tokens'])
        out['card'] = card
        c['card_is_last_mounted'] = eff.get('effect') == 'MOUNTED' and list(ctx['M'])[-1] == card
        names = slot_names869(env, list(state['segments']))
        segs3 = [s for s, n in zip(state['segments'], names) if n not in ('FV', 'FK')]
        X3, _ = env['make_x851'](pre, segs3, post)
        L3 = int(X3.shape[0])
        assert lp + sum(len(s) + (0 if r is None else int(r.shape[0])) for s, r in segs3) + len(post) == L3, 'X3_LAYOUT'
        seal0 = prefix_seals865(env, memx)
        hook0 = assert_hook_free859(env, 'T874_before_' + side)
        arms['R'] = {'action': record['action'], 'p': probs873(record['reading'])}
        r, _ = decide873(env, memx, X3)
        arms['M0'] = {'action': r['action'], 'p': probs873(r)}
        g, n_before = append_card873(env, keep['own'], card)
        cut, rephase = APPEND873['CUT'], APPEND873['rephase']
        pos_t, pos_m = (torch.arange(a, a + body, device=env['DEV']) for a in (n_before, n3 - body))
        c['card_lower_values_bitwise'] = all(bool(torch.equal(g[i][1][:, :, n_before:], memx[i][1][:, :, n3 - body:]))
                                             for i in range(cut + 1))
        c['card_lower_keys_rephase_rel'] = max(
            float(torch.linalg.vector_norm(rephase(g[i][0][:, :, n_before:], pos_t, pos_m).float()
                                           - memx[i][0][:, :, n3 - body:].float()))
            / max(float(torch.linalg.vector_norm(memx[i][0][:, :, n3 - body:].float())), 1e-30) for i in range(cut + 1))
        c['card_lower_keys_rephase_ok'] = c['card_lower_keys_rephase_rel'] <= ROPE_TOL874
        g_seal = prefix_seals865(env, g)
        x3s = n_before + body
        seg = {'M_t2': [0, n2], 'X2': [n2, n2 + L2], 'X2_task_prompt': [n2, n2 + lp], 'X2_state': [n2 + lp, n2 + L2],
               'A': [n2 + L2, n_before], 'C': [n_before, x3s], 'X3': [x3s, x3s + L3], 'X3_state': [x3s + lp, x3s + L3]}
        out['segments'] = seg
        r1, total1 = decide873(env, g, X3)
        arms['T1'] = {'action': r1['action'], 'p': probs873(r1)}
        c['segments_on_cache'] = (n_before == n2 + L2 + len(ids['ACQUIRE']) and length873(env, g) == x3s and
                                  total1 == x3s + L3)
        gb, _ = append_card873(env, [tuple(t.clone() for t in kv) for kv in keep['own']], card)
        c['t1_rebuild_identical'] = same873(r1, decide873(env, gb, X3)[0])
        del gb
        go, _ = append_card873(env, keep['one_shot'], card)
        ro, _ = decide873(env, go, X3)
        arms['T1_ONE_SHOT'] = {'action': ro['action'], 'p': probs873(ro)}
        m2_cards = keep['m2_cards']
        del go, keep
        ref = STATE874['ref873'][side]['T1']
        c['t1_reproduces_873'] = r1['action'] == ref['action'] and all(
            abs(arms['T1']['p'][w] - ref['p'][w]) <= REPRO_TOL874 for w in ref['p'])
        s = L2 - lp
        masks = {'T2': [(n2 + lp, n2 + L2)], 'T3': [(n2 + lp - s, n2 + lp)], 'T2_FULL': [(n2, n2 + L2)]}
        out['masks'] = masks
        r1x, rows1, _, _ = decide874(env, g, X3, [], rows=True)
        c['car874_empty_mask_equals_car873'] = same873(r1x, r1)
        r2, rows2, cache3, keep3 = decide874(env, g, X3, masks['T2'], rows=True, hold=True)
        arms['T2'] = {'action': r2['action'], 'p': probs873(r2)}
        for name in ('T3', 'T2_FULL'):
            rr, _, _, _ = decide874(env, g, X3, masks[name])
            arms[name] = {'action': rr['action'], 'p': probs873(rr)}
        rd, rowsd = removed874(env, g, X3, masks['T2'])
        mr, ur = rel874(rows2, rowsd), rel874(rows1, rowsd)
        out['mask_check'] = {'max_rel_masked_vs_removed': max(mr), 'max_rel_unmasked_vs_removed': max(ur),
                             'layer1_masked_vs_removed': mr[1], 'layer1_unmasked_vs_removed': ur[1],
                             'max_dp_masked_vs_removed': max(abs(arms['T2']['p'][w] - probs873(rd)[w]) for w in arms['T2']['p'])}
        c['mask_semantics_ok'] = max(mr) <= MASK_RATIO874 * max(ur)
        del rows1, rows2, rowsd
        c['timeline_base_unchanged'] = prefix_seals865(env, g) == g_seal
        out['step2'] = {'run': False, 'reason': 'T2 reading %s: %s' % (r2['action'], 'model end (terminal word)' if r2[
            'action'] in ('STOP', 'ACCEPT') else 'no corrective word to execute')}
        if r2['action'] in ('REJECT', 'BACKTRACK'):
            out['step2'] = dict(step2_874(env, ctx, side, state, r2['action'], cache3, keep3, seg, m2_cards, card, pre,
                                          post), run=True)
        del cache3, g
        STASH874.pop(side, None)
        hook1 = assert_hook_free859(env, 'T874_after_' + side)
        c['memory_seal_unchanged'] = prefix_seals865(env, memx) == seal0
        c['hook_free'] = not (hook0['hook_count'] or hook1['hook_count'] or hook0['transformers_output_capturing_installed']
                              or hook1['transformers_output_capturing_installed'])
        out['one_shot_dp'] = round(max(abs(arms['T1']['p'][w] - arms['T1_ONE_SHOT']['p'][w]) for w in arms['T1']['p']), 6)
        out['vram'] = vram_end870(vram0)
    except Exception as exc:
        out['error'] = '%s: %s' % (type(exc).__name__, str(exc)[:400])
        out['traceback'] = traceback.format_exc()
        line874('POINT_ERROR', side, 't=%d' % ctx['steps'], out['error'])
    finally:
        gc.collect()
        env['release']()
    out['seconds_t%d' % ctx['steps']] = round(time.perf_counter() - t0, 3)
    if ctx['steps'] == POST_STEP874 or out['error']:
        line874('POINT', side, _j874.dumps(c, sort_keys=True, default=str), 'lengths=%s' % _j874.dumps(out['lengths']),
                '' if out['error'] is None else 'ERROR=' + out['error'])


xray_point870 = probe874              # the sealed replay tap calls this name at the declared steps (return ignored)
_LOCKED_CONTROL_STEP874 = control_step869
control_step869 = stash_control874     # pass-through: identical return value, the replay compares every step bit-exactly


def corr874(p):
    return sum(p[w] for w in CORRECTIVE874)


def outcome874():
    reps = {r.get('item'): r for r in STATE870['replays']}
    blocks = list(STATE874['blocks'])
    need = ('t2_timeline_car_equals_record', 't2_cache_after_crops', 'timeline_after_commit', 'one_shot_not_semantic',
            'card_is_last_mounted', 'card_lower_values_bitwise', 'card_lower_keys_rephase_ok', 'segments_on_cache',
            't1_rebuild_identical', 't1_reproduces_873', 'car874_empty_mask_equals_car873', 'mask_semantics_ok',
            'timeline_base_unchanged', 'memory_seal_unchanged', 'hook_free')
    for side in SIDES874:
        s = STATE874['sides'].get(side)
        if reps.get(side, {}).get('ok') is not True:
            blocks.append('REPLAY_NOT_EXACT:' + side)
        if not s or s.get('error') or any(a not in s.get('arms', {}) for a in ('R', 'M0', 'T1', 'T2', 'T3', 'T2_FULL')):
            blocks.append('INCOMPLETE:' + side)
        elif not all(s['checks'].get(k) for k in need):
            blocks.append('CHECK:%s:%s' % (side, [k for k in need if not s['checks'].get(k)]))
    res = {'blocks': blocks, 'worlds': {}}
    if blocks:
        res['outcome'] = 'TECHNICAL_BLOCK'
        STATE874['outcome'] = res
        return res
    ok_all = True
    for w in WORLDS874:
        m, l = STATE874['sides']['I867_%s_MISSING' % w]['arms'], STATE874['sides']['I867_%s_LIVE' % w]['arms']
        t1, t2, t3, m0 = (m[a]['p'] for a in ('T1', 'T2', 'T3', 'M0'))
        row = {'missing_T2_reading': m['T2']['action'], 'missing_corr_T2_minus_T1': round(corr874(t2) - corr874(t1), 4),
               'missing_acq_T1_minus_T2': round(t1['ACQUIRE'] - t2['ACQUIRE'], 4),
               'missing_corr_T2_minus_T3': round(corr874(t2) - corr874(t3), 4),
               'missing_corr_T3_minus_T1': round(corr874(t3) - corr874(t1), 4),
               'missing_corr_T2_minus_M0': round(corr874(t2) - corr874(m0), 4),
               'live_T2_reading': l['T2']['action'], 'live_acc_T2_minus_T1': round(l['T2']['p']['ACCEPT'] - l['T1']['p']['ACCEPT'], 4),
               'tv_T2_missing_vs_live': tv873(t2, l['T2']['p'])}
        row['corrective'] = (m['T2']['action'] in CORRECTIVE874 and row['missing_corr_T2_minus_T1'] >= SHIFT_MIN874 and
                             row['missing_acq_T1_minus_T2'] >= SHIFT_MIN874)
        row['live_kept'] = l['T2']['action'] == 'ACCEPT' and row['live_acc_T2_minus_T1'] >= -LIVE_TOL874
        row['control_differs'] = not (m['T3']['action'] in CORRECTIVE874 and row['missing_corr_T3_minus_T1'] >= SHIFT_MIN874) \
            and row['missing_corr_T2_minus_T3'] >= CONTROL_GAP874
        row['pass'] = row['corrective'] and row['live_kept'] and row['control_differs']
        ok_all = ok_all and row['pass']
        res['worlds'][w] = row
    res['outcome'] = 'CAUSAL_RECONCILIATION_EFFECT' if ok_all else 'NO_RECONCILIATION_EFFECT'
    STATE874['outcome'] = res
    return res


def report874():
    W = ('ACQUIRE', 'BACKTRACK', 'REJECT', 'STOP', 'ACCEPT', 'ADVANCE')
    print('=' * 104)
    print('TEST874 — NATIVE CAUSAL STATE RECONCILIATION | GPU %s | engine %s | source %s (%s) | prereg %s' % (
        CC_GPU.get('name'), ENGINE_BLOB874[:12], STATE874['source'].get('git_blob'), STATE874['source'].get('how'),
        PREREG_SHA874[:16]))
    for side in SIDES874:
        s = STATE874['sides'].get(side)
        if not s:
            print('  %s: not reached' % side)
            continue
        d = s.get('one_shot_diagnostic') or {}
        print('  %s | t2 %s -> card %s | lengths %s' % (side, s.get('t2_action'), s.get('card'), _j874.dumps(s['lengths'])))
        print('     segments %s' % _j874.dumps(s.get('segments')))
        for name in ('R', 'M0', 'T1', 'T1_ONE_SHOT', 'T2', 'T3', 'T2_FULL'):
            a = s['arms'].get(name)
            if a:
                print('     %-11s %-9s ' % (name, a['action']) + '  '.join('%s %.3f' % (w, a['p'][w]) for w in W) +
                      '  corr %.3f' % corr874(a['p']))
        print('     one-shot dP %s (873: %s) | diagnostic %s first=%s rerun_bitwise=%s layer0=%s' % (
            s.get('one_shot_dp'), STATE874['ref873'].get(side, {}).get('one_shot_max_dp'), d.get('class'),
            _j874.dumps(d.get('first_difference')), d.get('one_shot_rerun_bitwise'), _j874.dumps(d.get('layer0'))))
        print('     mask check %s' % _j874.dumps(s.get('mask_check')))
        print('     step2 %s' % _j874.dumps(s.get('step2'), default=str))
        bad = [k for k, v in s['checks'].items() if v is False]
        print('     integrity %s | s_t3=%s | vram peak %s GiB%s' % ('PASS' if not bad else 'FAIL ' + str(bad), s.get('seconds_t3'),
              (s.get('vram') or {}).get('peak_allocated_gib', 'NA'), '' if not s.get('error') else '  ERROR ' + s['error']))
    o = STATE874['outcome'] or {}
    for w, row in (o.get('worlds') or {}).items():
        print('  WORLD %s %s' % (w, _j874.dumps(row, sort_keys=True)))
    if o.get('blocks'):
        print('  BLOCKS %s' % _j874.dumps(o['blocks']))
    print('TEST874 OUTCOME %s | status %s | wall %.0f s | peak GPU %.2f GiB' % (
        o.get('outcome'), STATE874['status'], time.perf_counter() - T_START874,
        max(STATE870['costs'].get('session_peak_allocated_bytes', 0),
            torch.cuda.max_memory_allocated() if torch.cuda.is_available() else 0) / 2**30))
    print('T2/T3 are counterfactual reads; step 2 executes only the model\'s own T2 word on a copy of the loop state.')
    print('GPU EXECUTION NOT VERIFIED BY THE CODE AUTHOR before this run.')
    print('=' * 104)


# ============================ TEST874 — SINGLE CELL EXECUTION ============================
T_START874 = time.perf_counter()
try:
    STATE874['status'] = 'GATE0'
    capture_source874()
    json_write864('874_prereg.json', {'prereg': PREREG874, 'sha256': PREREG_SHA874, 'before_model_load': True})
    line874('GATE0 SOURCE', _j874.dumps(STATE874['source'], sort_keys=True), 'prereg', PREREG_SHA874)
    load_sources865()                         # engine locks + test870.py + Test870.log + 873.py + 873.log (git blobs)
    STATE865['gates']['GATE0_SOURCE'] = {'status': 'PASS', 'locks': len(LOCKS864)}
    for name, needles in (('Test870.log', ('XR870 CALIBRATION CALIBRATION_PASS', 'NVIDIA A100')),
                          ('873.log', ('TEST873 OUTCOME', 'status COMPLETE', 'NVIDIA A100'))):
        assert all(x in RAW_SOURCES864[name].decode('utf-8') for x in needles), ('LOCKED_LOG_NOT_A_COMPLETE_GPU_RUN', name)
    load873_874()
    STATE874['ref873'] = ref873_874(RAW_SOURCES864['873.log'].decode('utf-8'))
    feasibility_audit864()
    audit_contracts865()
    load_spine864()
    REFS874 = load_records870()
    for w in WORLDS874:
        sha = {}
        for cnd in ('MISSING', 'LIVE'):
            ctl = [e['record'] for e in REFS874[('I867_%s_%s' % (w, cnd), ARM874)]['events'] if e['type'] == 'CONTROL']
            assert [x['action'] for x in ctl[:2]] == ['ADVANCE', 'ACQUIRE'], ('T2_PATH', w, cnd)
            sha[cnd] = ctl[PRE_STEP874 - 1]['state_sha256']
        assert sha['MISSING'] == sha['LIVE'], ('T2_NOT_SHARED', w)
    line874('GATE0 PASS', 'ref873 %s' % _j874.dumps(STATE874['ref873'], sort_keys=True))
    STATE874['status'] = 'GATE1'
    assert CC_GPU_OK, ('GPU_PRECHECK_NOT_A100_80GB_WITH_40GIB_FREE', CC_GPU)
    env874, original_error874, original_trace874, reproduction874 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace874
    TWO_JOB_VERIFICATION864 = verify_two_job859(env874, original_trace874)
    assert_hook_free859(env874, 'T874_before_native_regression')
    install_offline_evaluator859(env874)
    native874 = native_sequences860(env874)
    NATIVE_REGRESSION864 = native_regression864(env874, native874)
    verify_864_reference865(NATIVE_REGRESSION864)
    ANALYSIS864 = run_analysis863(env874, native874)
    assert len(STATE863['restores']) == 3 and all(r['exact'] for r in STATE863['restores']), 'ORIGINAL_EXACT_RESTORE'
    digest874 = records_digest861(env874)
    null_seal874 = physical_seal863(env874, env874['MEMNULL841'])
    runtime_contracts865(env874)
    runtime_preflight865(env874, reproduction874)
    rearm_budget865(env874)
    make_slots866(env874)
    SLOTS867['PREV_EVALUATION'] = list(env874['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env874)
    line874('GATE1 APPEND NAMESPACE', _j874.dumps(resolve_append873(env874), sort_keys=True))
    assert_hook_free859(env874, 'T874_before_points')
    line874('GATE1 PASS', 'model_load_s=%.0f' % (time.perf_counter() - T_START874))
    STATE874['status'] = 'RUNNING'
    T0_865 = time.perf_counter()
    by_key874 = build_specs869(env874)
    for side in SIDES874:
        rep874 = run_replay870(env874, {'id': side, 'item': side, 'arm': ARM874,
                                        'targets': {PRE_STEP874: 'T2_TIMELINE', POST_STEP874: 'T3_ARMS'}},
                               by_key874, REFS874)
        T2_KEEP874.pop(side, None)
        STASH874.pop(side, None)
        if not rep874['ok']:
            STATE874['blocks'].append('REPLAY_NOT_EXACT:%s %s' % (side, _j874.dumps(rep874['mismatch'], default=str)[:300]))
    # ====== OFFLINE: no model call below ======
    hook874 = hook_audit859(env874, 'T874_final')
    if records_digest861(env874) != digest874 or physical_seal863(env874, env874['MEMNULL841']) != null_seal874 or \
            hook874['hook_count'] or hook874['transformers_output_capturing_installed']:
        STATE874['blocks'].append('POST_RUN_INTEGRITY')
    STATE874['status'] = 'COMPLETE'
    outcome874()
except BaseException as exc:
    STATE874['error'] = '%s: %s' % (type(exc).__name__, exc)
    STATE874['traceback'] = traceback.format_exc()
    STATE874['status'] = 'FAILED_AT_' + str(STATE874['status'])
    STATE874['outcome'] = {'outcome': 'TECHNICAL_BLOCK', 'blocks': ['EXCEPTION: ' + STATE874['error'][:300]]}
    (ROOT864 / '874_traceback.txt').write_text(STATE874['traceback'], encoding='utf-8')
    print('TEST874 ERROR %s | full traceback: %s' % (STATE874['error'][:300], ROOT864 / '874_traceback.txt'),
          file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        keep874_ = dict(STATE874, replays=STATE870['replays'])
        json_write864('874_result.json', json.loads(json.dumps(keep874_, default=str, allow_nan=False)))
    except Exception as _exc874:
        print('RESULT_WRITE_FAILED', type(_exc874).__name__, _exc874, file=ERROR_CONSOLE864, flush=True)
    report874()
    if not EVENTS_FILE866.closed:
        EVENTS_FILE866.close()
    LOG_FILE864.close()
exec(compile(ENGINE874['suffix'], 'test870.py:suffix', 'exec'), globals())      # package, Drive copy, download (I/O)
