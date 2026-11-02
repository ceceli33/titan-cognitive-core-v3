# AKBASCORE SILICON HIPPOCAMPUS — TEST845: NATIVE COGNITIVE CONTROL JUNCTION (pointer-state recurrence over CUT3 memory)
# Single Colab cell, one A100-80GB, frozen Qwen2.5-72B-Instruct NF4. Engine chain (all fetched and git-blob verified at
# run time): 844.py (GPU-completed TEST841-R driver, blob 783dbca9) -> 841.py (GPU-completed engine, blob 135b18e5) ->
# 829 / 834 / 779 / 730 / 757 / 840 / v2 610-627. The 844 driver is executed with its panel, hypotheses, run tail and
# offline phase replaced; its IMCL / STANDARD code is reused verbatim as control arms. The 841 job loop is cut out as in 844.
# JUNCTION: the model's own one-hop output (M2-soft rows of its "next node" generation) is carried across turns as the
#   layer-0 input of the next hop computation over the physically mounted CUT3 memory. The model's literal output decides:
#   a node name -> advance; UNKNOWN -> its own pointer addresses a new physical card (PEAK50, class B); a card that leaves
#   the output UNKNOWN is unmounted; after 3 such cards the hop is a dead end -> the evidence of the previous hop is
#   retracted (provenance or counterfactual attribution) and the path backtracks; dead end at the start -> abstain.
#   The number of hops is the model's own one-digit plan for the question; Python only counts (class C).
# Arms (same question, start, bank, hop budget): JUNCTION | OFF (no state) | ZERO (mean-embedding state) | SWAP (partner
# world's state) | REVERSE (own state, row order reversed) | IMCL (844 external law) | STANDARD (one answer pass).
# No GPU execution or result is claimed by the code author.
import urllib.request, hashlib, ast
URL845 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/844.py"
LOCK845 = "783dbca9ebab722a0a5826aa708c4f152f8d7ad7"   # 844.py git blob (GPU-completed TEST841-R driver)
with urllib.request.urlopen(urllib.request.Request(URL845, headers={"User-Agent": "AKBASCORE-TEST845"}), timeout=180) as f_:
    raw845 = f_.read(200001)
assert hashlib.sha1(b"blob %d\0" % len(raw845) + raw845).hexdigest() == LOCK845, "STOP_844_SOURCE_CHANGED"
D845 = raw845.decode("utf-8").replace("TEST841R", "TEST845").replace("T41R|", "T845|")
def rp845(s, a, b, n=1):
    assert s.count(a) == n, ("PATCH_ANCHOR_845", a[:70], s.count(a))
    return s.replace(a, b)
def cut845(s, a, b, new):
    assert s.count(a) == 1 and s.count(b) >= 1, ("CUT_ANCHOR_845", a[:60], b[:60])
    i = s.index(a); k = s.index(b, i)
    return s[:i] + new + s[k:]

# ---------------- PANEL: jobs (fresh seed; sealed before any model call) ----------------
PANEL845 = r'''STARTS41R = ('LIVE', 'FORK', 'BRIDGED', 'MISSING', 'HOP3')
ARMS41R = ('JUNCTION', 'IMCL', 'STANDARD', 'OFF', 'ZERO', 'SWAP', 'REVERSE')
JARMS845 = ('JUNCTION', 'OFF', 'ZERO', 'SWAP', 'REVERSE')
DCONDS845 = ('D_SUFF', 'D_MIRROR', 'D_FIRST', 'D_IRREL', 'D_FORKF', 'D_CONFLICT', 'D3_PAIR', 'D3_FULL')
def job41r(qid, role, bank, arm, start, partner, kind='LOOP', designs=(), own=None):
    j = 'J845_' + ''.join(_rng841.choice('0123456789ABCDEF') for _ in range(12))
    JOBS841.append({'job': j, 'kind': kind, 'qid': qid, 'mount': [], 'bank': list(bank), 'frame': 'A', 'arm': arm,
                    'start': list(start), 'partner': partner, 'designs': [list(d) for d in designs], 'own': own})
    EVALKEY841[j] = role
    return j
DIAG845, JUN845 = {}, {}
for wi, w in enumerate(worlds829):
    ids = w['ids']; far = worlds829[((BLOCKOF841[wi] + 1) % NBLOCK841) * BLOCK841 + wi % BLOCK841]['ids']; q = QID841[wi]
    q3 = w['world'] + '_H3'
    des = [(q, [ids['first'], ids['second']], 2), (q, [ids['first'], ids['mirror']], 2), (q, [ids['first']], 2),
           (q, [ids['first'], far['second']], 2), (q, [ids['fork'], ids['first']], 2),
           (q, [ids['first'], ids['second'], ids['changed']], 2), (q3, [ids['first'], ids['second']], 3),
           (q3, [ids['first'], ids['second'], ids['third']], 3)]
    DIAG845[wi] = job41r(q, {'world': wi, 'cond': 'DIAG', 'arm': 'DIAG', 'conds': list(DCONDS845)}, [], 'DIAG', [], None,
                         kind='DIAG', designs=des)
for wi, w in enumerate(worlds829):
    pw = ((BLOCKOF841[wi] + 1) % NBLOCK841) * BLOCK841 + wi % BLOCK841
    job41r(QID841[wi], {'world': wi, 'cond': 'DIAGV', 'arm': 'DIAGV'}, [], 'DIAGV', [], DIAG845[pw], kind='DIAGV', own=DIAG845[wi])
for arm in ARMS41R:                                   # JUNCTION first: SWAP partners must exist
    for wi, w in enumerate(worlds829):
        B = BANKS841[BLOCKOF841[wi]]; ids = w['ids']
        pw = ((BLOCKOF841[wi] + 1) % NBLOCK841) * BLOCK841 + wi % BLOCK841        # partner: other bank, same slot
        for st in STARTS41R:
            start = {'FORK': [ids['fork']], 'BRIDGED': [ids['first_bridged']]}.get(st, [])
            drop = {'MISSING': (ids['second'], ids['changed']), 'BRIDGED': (ids['first'],), 'HOP3': (ids['mirror'],)}.get(st, ())
            jid = job41r(w['world'] + '_H3' if st == 'HOP3' else QID841[wi], {'world': wi, 'cond': st, 'arm': arm},
                         [c for c in B['v0'] if c not in drop], arm, start, JUN845.get((st, pw)) if arm == 'SWAP' else None)
            if arm == 'JUNCTION':
                JUN845[(st, wi)] = jid
assert all(j['partner'] for j in JOBS841 if j['arm'] in ('SWAP', 'DIAGV')), 'SWAP_PARTNER'
JOBS841.sort(key=lambda j: ({'DIAG': 0, 'DIAGV': 1}.get(j['kind'], 2 if j['arm'] == 'JUNCTION' else 3), _rng841.random()))
assert len(JOBS841) == len(EVALKEY841) == len(worlds829) * (2 + len(STARTS41R) * len(ARMS41R)), 'JOB_COUNT'
'''
COST845 = r'''def cost_upper841(tok_of, p_):
    mx = max(tok_of.values()); K = K_ECHO841; NJ = len(JOBS841); f6 = fus_upper841(CAP845 + 1, mx, p_); nq = 2 * len(worlds829)
    up = {'fusion_forwards': 6 * fus_upper841(2, mx, p_) + NMG845 * f6, 'capture_forwards': 0,
          'probe_forwards': 12 + NVG841 + NEG841 + NAG841 + NHG845 + nq, 'rank_forwards': 0,
          'bypass_forwards': 8 + NEG841 + NHG845 + nq,
          'generation_forwards': 1 + 3 * K + NEG841 * (K - 1) + NJ * MAX_NEW_ANS841 + NHG845 * (K845 - 1) + nq * 2}
    sec = MARGIN841 * (up['fusion_forwards'] * SEC_FUSION841 + up['generation_forwards'] * SEC_GEN841 +
                       up['bypass_forwards'] * SEC_BYPASS841 + up['probe_forwards'] * SEC_PROBE841 + 120.0 + len(tok_of) * 2.0)
    return {'numeric_upper': up, 'jobs': NJ, 'physical_cartridges': len(tok_of), 'bank_cartridges': len(ALLBANK841),
            'max_memory_tokens': p_ + (CAP845 + 1) * mx, 'minutes_upper_excluding_model_load': round(sec / 60.0, 1),
            'cost_model': 'global caps: %d signal / %d echo / %d action / %d hop computations / %d mounts; fusion %.2f s, token %.2f s, '
                          'bypass %.2f s, probe %.2f s, x%.2f margin' % (NVG841, NEG841, NAG841, NHG845, NMG845, SEC_FUSION841, SEC_GEN841,
                                                                       SEC_BYPASS841, SEC_PROBE841, MARGIN841)}'''

# ---------------- PRE-REGISTERED HYPOTHESES AND CRITERIA (fixed before any GPU result) ----------------
HYP845 = {
    'question': ('Can a recurrent control state made of the frozen model\'s own one-hop output, carried across turns as its '
                 'layer-0 input over physically mounted CUT3 memory, replace the global answer-confidence readout of IMCL and '
                 'make search, retraction, abstention and 2-/3-link completion follow the evidence?'),
    'diagnosis_844': ['V and G are a global, single-pass readout: MISSING [S->M, E->M] V=+10.6 answers MIDDLE; [D->S, S->F] '
                      'V=+5.8 answers FORK_END; other-world cards raise V (G>0 for 75/113 wrong candidates, median +0.875).',
                      'V is terminal, not progress: HOP3 cue candidates G -0.1..-1.6 -> immediate UNKNOWN in 9/12.',
                      'Local computation is reliable: echo next link 23/25; credit by substitution inside a complete chain '
                      'retracted wrong cards 21/21; chain-mounted loops answered 22/22.',
                      'LIVE and FORK share identical trajectories when the cue picks the fork: the 6 IMCL corrections are 3 '
                      'distinct computations; YOKED (another case\'s decisions) reached 20/48 vs IMCL 22/48.'],
    'frames': {'plan': 'Question: {q}\nHow many directed links must be followed from the start node to answer the question? '
                       'Reply with one digit only.',
               'hop0': 'Use only mounted physical evidence. Follow directed links. Question: {q}\nName the node reached by '
                       'following exactly one directed link from the start node of the question. If the mounted evidence has no '
                       'such link, reply UNKNOWN. Reply with the node name only.',
               'hop': 'Use only mounted physical evidence. Follow directed links. Question: {q}\nThe current node is given '
                      'below. Name the node reached by following exactly one directed link from the current node. If the mounted '
                      'evidence has no such link, reply UNKNOWN. Reply with the node name only.',
               'slots': ['Links:', 'Current node:', '\nNext node:', 'Next node:']},
    'law': {'state': 'R_k = M2-soft rows of the model\'s own hop-k generation (K=8, end-token cut) re-entered at layer 0',
            'decisions': 'node name -> advance; UNKNOWN -> own state addresses a card; UNKNOWN after mount -> unmount; 3 failed '
                         'cards -> dead end -> retract previous hop evidence and backtrack; dead end at hop 0 -> abstain; '
                         'plan digit reached -> answer = last node (model text)',
            'budgets': 'S=3 cards per hop, <=14 hop computations per loop, <=5 mounted cards (mechanical, class C)'},
    'arms': {'JUNCTION': 'own state', 'OFF': 'state slot empty', 'ZERO': 'state = mean embedding row x len(R)',
             'SWAP': 'state = partner world\'s junction state at the same hop', 'REVERSE': 'own rows in reversed order',
             'IMCL': '844 external law (verbatim)', 'STANDARD': 'one greedy answer pass on the start memory'},
    'levels': {
        'L1_NUMERIC_CAUSALITY': 'designed S->M,M->E: hop-1 output with OFF / ZERO / SWAP / REVERSE state differs from the own-state '
                                'output (argmax token differs or own-token probability shifts >= 0.5) in >= 10/12 for every variant.',
        'L2_EVIDENCE_SENSITIVITY': 'own state: S->M,M->E hop-1 = END >= 10/12 AND S->M only hop-1 = UNKNOWN >= 10/12 AND '
                                   'S->M,E->M hop-1 = UNKNOWN >= 9/12 AND each variant gives END on S->M,M->E in <= 6/12.',
        'L3_BEHAVIOURAL_CONTROL': 'JUNCTION grounded-correct answers (48 answerable) >= IMCL + 6 AND >= best of OFF/ZERO/SWAP/'
                                  'REVERSE + 6 AND MISSING abstains >= 9/12 AND wrong entity answers (60) <= 6.',
        'L4_AUTONOMOUS_RECURSION': 'scope: model outputs drive every hop; fixed frames and mechanical budgets. JUNCTION HOP3 '
                                   'grounded >= 8/12 AND >= every other arm + 3 AND plan correct >= 10/12 for both question '
                                   'types AND L2 PASS.'},
    'criteria': {
        'MODEL_DERIVED_ADDRESS': 'JUNCTION searches at hop >= 1 whose true current node is X route to a card with source X in >= 75% of >= 10.',
        'MODEL_NATIVE_ERROR_DETECTION': 'JUNCTION hop outputs: UNKNOWN when the mounted memory has no out-edge from the true current '
                                        'node, a node when it has one: precision of UNKNOWN >= 85% AND recall >= 75% (>= 20 each) '
                                        'AND designed S->M,E->M hop-1 UNKNOWN >= 9/12.',
        'MODEL_NATIVE_CORRECTION': 'PATH_CORRECTED = a path node off every valid chain, later a grounded-correct answer. JUNCTION >= 6 '
                                   'AND >= each other arm + 4; NOT_DEMONSTRATED if < 6 JUNCTION loops produced a wrong path node.',
        'MODEL_NATIVE_RESEARCH_DECISION': 'JUNCTION answerable loops that mounted a valid chain >= 38/48 AND searches issued while the '
                                          'needed out-edge was already mounted <= 15% of searches.',
        'MODEL_NATIVE_STOP_DECISION': 'JUNCTION MISSING abstains >= 9/12 AND false abstentions on answerable <= 6/48 AND HOP3 '
                                      'answers END after two hops <= 2/12.',
        'AUTONOMOUS_RECURSIVE_REASONING': 'equals L4.',
        'control_effect_rule': 'if JUNCTION grounded-correct exceeds the best of OFF/ZERO/SWAP/REVERSE by < 3, every MODEL_NATIVE '
                               'verdict, L3 and L4 become NOT_DEMONSTRATED.'},
    'decision': 'YETERSİZ KANIT on budget stop. DEVAM if L2 and L3 PASS. DUR if own-state S->M only hop-1 UNKNOWN < 6/12 or '
                'S->M,E->M hop-1 UNKNOWN < 6/12 (local link verification absent: pointer-state control eliminated for this model '
                'without training) or the control effect rule fires. Otherwise YETERSİZ KANIT.',
    'classes': {'plan digit, hop outputs (names / UNKNOWN), answer text, echo, V': 'A (model computation, applied literally)',
                'PEAK50 routing, attribution rule (first card whose NULL-substitution changes the hop token), IMCL law': 'B (fixed rule)',
                'mount / unmount / exclusion / S=3 / budgets / hop counting / memo reuse': 'C (mechanical)'},
    'not_measured_deferred': ['non-synthetic memories', 'chains longer than three links', 'model-written frames',
                              'conflict resolution policy (reported only)', 'a learned control state']}

# ---------------- RUN TAIL (after the reused 844 definitions; replaces the 844 job loop) ----------------
RUN845 = r'''D829['limitations845'] = [
    'The hop / plan frames and the slot texts are fixed by the experimenter (class B); they carry no name or answer.',
    'Unmount after an UNKNOWN, S=3 cards per hop, the hop budget and hop counting are mechanical (class C).',
    'The state is re-entered through the vocabulary channel (M2-soft rows); direct residual transfer (D1) failed in TEST841.',
    'No GPU execution or result is claimed by the code author.']
FR845 = HYP841['frames']
gate829('FRAMES_CONTAIN_NO_PANEL_NAME', not any(nm in t_ for nm in [x for v in cards829.values() for x in v.replace('.', ' ').split()
        if len(x) == 9 and x.isupper()] for t_ in [FR845['plan'], FR845['hop0'], FR845['hop']] + FR845['slots']))
gate829('DESIGNS_PHYSICAL', all(c in entries for j in JOBS841 for d in j['designs'] for c in d[1]))
SLOT845 = [list(tok(x, add_special_tokens=False).input_ids) for x in FR845['slots']]
UNKS845 = {int(tok(x, add_special_tokens=False).input_ids[0]) for x in ('UNKNOWN', ' UNKNOWN')}
acc845 = None
for s0_845 in range(0, int(E841.shape[0]), 8192):
    b_ = E841[s0_845:s0_845 + 8192].float().sum(dim=0)
    acc845 = b_ if acc845 is None else acc845 + b_
MUE845 = (acc845 / float(E841.shape[0])).to(DTYPE)
del acc845
HOPM845, PLAN845 = {}, {}
CNT845 = {'hop': 0, 'hop_hit': 0}
def end845(t_):
    return t_ == int(tok.eos_token_id) or '\n' in tok.decode([t_])
def gen845(memx, pre, rows, post):
    parts = [embed841(pre)] + ([rows.to(DEV).to(DTYPE)] if rows is not None and rows.shape[0] else []) + ([embed841(post)] if post else [])
    X = torch.cat(parts, dim=0); L = int(X.shape[0]); n = int(memx[0][0].shape[-2]); cache = cache_build(list(memx))
    pos = torch.arange(n, n + L, device=DEV)
    with torch.no_grad():
        out = model(inputs_embeds=X.reshape(1, L, H), past_key_values=cache, attention_mask=torch.ones((1, n + L), device=DEV, dtype=torch.long),
                    position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
        logits = out.logits[0, -1].float()
        del out
    COUNT834['probe_forwards'] += 1
    R, toks, info = [], [], []
    for t in range(K845):
        p = torch.softmax(logits, dim=-1); top = torch.topk(p, 20)
        info.append({'ids': [int(x) for x in top.indices.tolist()], 'p': [round(float(x), 5) for x in top.values.tolist()],
                     'H': round(float(-(p * p.clamp_min(1e-30).log()).sum()), 4)})
        toks.append(info[-1]['ids'][0])
        if end845(toks[-1]):
            break
        v = (p.to(E841.dtype).reshape(1, -1) @ E841).reshape(-1); R.append(v.to(DTYPE))
        if t + 1 < K845:
            x = n + L + t
            with torch.no_grad():
                out = model(inputs_embeds=v.to(DTYPE).reshape(1, 1, H), past_key_values=cache,
                            attention_mask=torch.ones((1, x + 1), device=DEV, dtype=torch.long), position_ids=torch.tensor([[x]], device=DEV),
                            cache_position=torch.tensor([x], device=DEV), use_cache=True, return_dict=True)
                logits = out.logits[0, -1].float()
                del out
            COUNT834['generation_forwards'] += 1
    del cache
    kend = len(R)
    text = tok.decode([t_ for t_ in toks if not end845(t_)])
    return {'rows': torch.stack(R).float().cpu() if R else torch.zeros((0, H)), 'text': text, 'toks': toks[:kend],
            'tok1': toks[0], 'p1': info[0]['p'][0], 'H1': info[0]['H'], 'top1': info[0], 'kend': kend}
def rkey845(rows):
    return None if rows is None else hashlib.sha1(rows.float().numpy().tobytes() + str(tuple(rows.shape)).encode()).hexdigest()
def hop845(q, m, k, rows):
    key = (q, key_r41(m), k == 0, rkey845(rows))
    if key in HOPM845:
        CNT845['hop_hit'] += 1
        return HOPM845[key]
    if CNT845['hop'] >= NHG845:
        raise BudgetR41('GLOBAL_HOP_CAP')
    memx = memx_r41(m)
    if k == 0:
        h = gen845(memx, list(prompt_ids(FR845['hop0'].format(q=QTEXT841[q]))) + SLOT845[3], None, None)
    else:
        h = gen845(memx, list(prompt_ids(FR845['hop'].format(q=QTEXT841[q]))) + SLOT845[1], rows, SLOT845[2])
    t_ = h['text'].strip().upper()
    h['unk'] = (not t_) or t_.startswith('UNKNOWN')
    HOPM845[key] = h; CNT845['hop'] += 1
    return h
def plan845(q):
    if q not in PLAN845:
        h = gen845(MEMNULL841, list(prompt_ids(FR845['plan'].format(q=QTEXT841[q]))) + SLOT845[0], None, None)
        d_ = [ch for ch in h['text'] if ch.isdigit()]
        PLAN845[q] = {'text': h['text'], 'N': int(d_[0]) if d_ and d_[0] != '0' else None}
    return PLAN845[q]
def state845(arm, path, k, par):
    own = path[k - 1]['rows']
    if arm == 'JUNCTION':
        return own
    if arm == 'OFF':
        return torch.zeros((0, H))
    if arm == 'ZERO':
        return MUE845.float().cpu().reshape(1, H).repeat(max(1, int(own.shape[0])), 1)
    if arm == 'REVERSE':
        return torch.flip(own, dims=[0])
    pr = [np.asarray(par[x]) for x in sorted(par, key=lambda z: int(z[3:])) if x.startswith('ptr') and int(x[3:]) <= k - 1] if par else []
    return torch.tensor(pr[-1], dtype=torch.float32) if pr else MUE845.float().cpu().reshape(1, H).repeat(max(1, int(own.shape[0])), 1)
def addr845(q, m, rows, bank, X):
    ex = set(X) | set(m)
    if not [c for c in bank if c not in ex]:
        return None
    if rows is None or not rows.shape[0]:
        return route_r41(q, m, 'CUE', bank, X)
    hi, ms_ = h3_bypass841(MEMNULL841, embeds=index_embeds841(rows.to(DEV)))
    r = route841(hi[len(IDXPRE841):len(IDXPRE841) + int(rows.shape[0])], bank, ex); del hi
    sc = sorted(r['scores'].values(), reverse=True)
    return {'via': 'STATE', 'chosen': r['chosen'], 'margin': round(sc[0] - (sc[1] if len(sc) > 1 else 0.0), 5), 'n_cand': len(sc)}
def attrib845(q, M, kk, path, arm, par):
    used = {p_['evid'] for p_ in path if p_['evid']}
    rows = None if kk == 0 else state845(arm, path, kk, par)
    for i_, c_ in enumerate(M):
        if c_ in used:
            continue
        h2 = hop845(q, M[:i_] + [NULL829] + M[i_ + 1:], kk, rows)
        if h2['text'].strip() != path[kk]['text'].strip():
            return c_
    return None
def jloop845(j):
    q = j['qid']; arm = j['arm']; bank = j['bank']; M = list(j['start']); X = []; steps = []; path = []; end = None
    par = ROWS841.get(j['partner']) if arm == 'SWAP' else None
    if arm == 'SWAP' and par is None:
        raise RuntimeError('SWAP_PARTNER_ROWS_MISSING')
    pl = plan845(q); N = pl['N']; tries = {}; pend = None; nh = 0
    say_r41('PLAN', j['job'], arm, 'model plan text=%r -> hops=%s' % (pl['text'][:12], N))
    if N is None:
        end = 'PLAN_INVALID'
    while end is None:
        k = len(path)
        if k == N:
            end = 'PATH_COMPLETE'; break
        if nh >= HMAX845:
            end = 'BUDGET_STOP'; break
        rows = None if k == 0 else state845(arm, path, k, par)
        m0 = list(M); h = hop845(q, M, k, rows); nh += 1
        st = {'k': k, 'mem': m0, 'out': h['text'], 'tok1': h['tok1'], 'p1': h['p1'], 'H1': h['H1'], 'unk': h['unk'],
              'state': 'none' if rows is None else '%s:%d' % (arm, int(rows.shape[0]))}
        if not h['unk']:
            path.append({'rows': h['rows'], 'text': h['text'], 'tok1': h['tok1'], 'evid': pend, 'mem': m0})
            st['dec'] = 'ADVANCE'; pend = None; tries[k + 1] = 0; ex_ = 'path +%r' % h['text'][:20]
        else:
            if pend is not None:
                M.remove(pend); X.append(pend); st['unmounted'] = pend; pend = None
            if tries.get(k, 0) < SMAX845 and len(M) < CAP845:
                a_ = addr845(q, M, rows, bank, X)
                if a_ is None:
                    tries[k] = SMAX845; st['dec'] = 'NO_CANDIDATE'; ex_ = 'no candidate'
                else:
                    M.append(a_['chosen']); pend = a_['chosen']; tries[k] = tries.get(k, 0) + 1
                    st.update({'dec': 'SEARCH', 'cand': a_['chosen'], 'via': a_['via'], 'margin': a_['margin']})
                    ex_ = 'MOUNT %s (%s) via %s margin=%.4f' % (a_['chosen'], rel_r41(a_['chosen']), a_['via'], a_['margin'])
            else:
                if k == 0:
                    st['dec'] = 'ABSTAIN'; end = 'ABSTAIN'; ex_ = 'dead end at the start: abstain (UNKNOWN)'
                else:
                    e_ = path[k - 1]['evid'] or attrib845(q, M, k - 1, path, arm, par)
                    if e_ is not None and e_ in M:
                        M.remove(e_); X.append(e_); st['retracted'] = e_
                    path.pop(); tries[k] = 0; st['dec'] = 'DEAD_END_BACKTRACK'
                    ex_ = 'dead end: retract %s, back to hop %d' % (rel_r41(e_) if e_ else 'nothing', k - 1)
            if 'unmounted' in st:
                ex_ = 'UNMOUNT %s | ' % rel_r41(st['unmounted']) + ex_
        steps.append(st)
        say_r41('HOP', j['job'], arm, 'k%d' % k, 'MEM=' + mem_r41(m0), 'STATE=' + st['state'],
                'OUT=%r p1=%.3f H1=%.2f%s' % (h['text'][:24], h['p1'], h['H1'], ' (UNKNOWN)' if h['unk'] else ''),
                'DECISION=' + st['dec'] + ' (model output)', 'EXEC=' + ex_, 'NEXT=' + mem_r41(M))
    pa = path[-1]['text'] if end == 'PATH_COMPLETE' else ('UNKNOWN' if end == 'ABSTAIN' else None)
    fa = answer_r41(q, M)
    say_r41('END', j['job'], arm, 'END=' + end + (' (mechanical)' if end in ('BUDGET_STOP', 'PLAN_INVALID') else ''),
            'POINTER_ANSWER=%r' % (pa or '')[:40], 'FRAME_ANSWER=%r' % fa[:40], 'PATH=' + '>'.join(repr(p_['text'][:12]) for p_ in path),
            'FINAL=' + mem_r41(M))
    rows_ = {('ptr%d' % i_): p_['rows'].numpy().astype(np.float32) for i_, p_ in enumerate(path)} if arm == 'JUNCTION' else {}
    return {'job': j['job'], 'kind': 'LOOP', 'qid': q, 'arm': arm, 'steps': steps, 'end': end, 'pointer_answer': pa,
            'answer_raw': fa, 'path': [p_['text'] for p_ in path], 'plan': pl, 'final_mounted': M, 'excluded': X,
            'hops': nh}, rows_
def diag845(j):
    out, rows_ = [], {}
    for di, (q, m, nhop) in enumerate(j['designs']):
        sg = sig_r41(q, m); pl = plan845(q); hs = []; rows = None
        for k in range(nhop):
            h = hop845(q, m, k, rows); hs.append({'k': k, 'out': h['text'], 'tok1': h['tok1'], 'p1': h['p1'], 'H1': h['H1'],
                                                    'unk': h['unk'], 'top1': h['top1']})
            if k == 0 and di in (0, 2):
                rows_['d%d_h0' % di] = h['rows'].numpy().astype(np.float32)
            if h['unk']:
                break
            rows = h['rows']
        out.append({'i': di, 'qid': q, 'mount': m, 'sig': sg, 'plan': pl, 'hops': hs})
        say_r41('DIAG', j['job'], 'd%d' % di, 'MEM=' + mem_r41(m), 'V=%+.2f ans1=%s' % (sg['V'], tk_r41(sg['top'])), 'PLAN=%r' % pl['text'][:8],
                'HOPS=' + ' > '.join('%r%s' % (x['out'][:14], '(U)' if x['unk'] else '') for x in hs))
    return {'job': j['job'], 'kind': 'DIAG', 'designs': out}, rows_
def diagv845(j):
    own = ROWS841.get(j['own']) or {}; par = ROWS841.get(j['partner']) or {}; dj = REC841.get(j['own'])
    if dj is None or not own or not par:
        raise RuntimeError('DIAGV_INPUT_MISSING')
    out = []
    for di in (0, 2):
        q, m, _ = dj['designs'][di]['qid'], dj['designs'][di]['mount'], None
        r0 = torch.tensor(np.asarray(own['d%d_h0' % di])); rp = torch.tensor(np.asarray(par['d%d_h0' % di]))
        for vn, rv in (('OWN', r0), ('OFF', torch.zeros((0, H))), ('ZERO', MUE845.float().cpu().reshape(1, H).repeat(max(1, int(r0.shape[0])), 1)),
                       ('SWAP', rp), ('REVERSE', torch.flip(r0, dims=[0]))):
            h = hop845(q, m, 1, rv)
            out.append({'d': di, 'variant': vn, 'out': h['text'], 'tok1': h['tok1'], 'p1': h['p1'], 'unk': h['unk'], 'top1': h['top1']})
            say_r41('DIAGV', j['job'], 'd%d' % di, vn, 'MEM=' + mem_r41(m), 'OUT=%r p1=%.3f%s' % (h['text'][:20], h['p1'], ' (UNKNOWN)' if h['unk'] else ''))
    return {'job': j['job'], 'kind': 'DIAGV', 'variants': out}, {}
say_r41('PREREG', 'S=%d HMAX=%d CAP=%d K=%d caps=%d/%d/%d/%d' % (SMAX845, HMAX845, CAP845, K845, NVG841, NEG841, NAG841, NHG845),
        'DECISION_RULE=' + HYP841['decision'])
for k_, v_ in list(HYP841['levels'].items()) + list(HYP841['criteria'].items()):
    say_r41('PREREG', k_, v_)
UPPER_CHECK841 = {}
t_run841 = time.perf_counter()
nj845 = len(JOBS841); stp845 = max(1, nj845 // 12)
log829('TEST845_PROGRESS', 'JOBS', 0, '/', nj845)
for ji845, j845 in enumerate(JOBS841):
    if j845['job'] not in REC841:
        if (time.perf_counter() - T0_841) / 60.0 > HARD_BUDGET_MIN841:
            BUDGET_STOP841 = True; log829('TEST845_BUDGET_STOP', 'job', ji845, 'of', nj845); break
        fn845 = (diag845 if j845['kind'] == 'DIAG' else diagv845 if j845['kind'] == 'DIAGV' else
                 (lambda j_: (loop_r41(j_), {})) if j845['arm'] in ('IMCL', 'STANDARD') else jloop845)
        try:
            if not UPPER_CHECK841:
                with CallCount841() as ccu845:
                    rec845, rows845 = fn845(j845)
                UPPER_CHECK841 = ccu845.summary()
                gate829('CUT3_MOUNT_AND_ANSWER_RUN_UPPER_LAYERS', UPPER_CHECK841['upper_min'] >= 1 and UPPER_CHECK841['lm_head'] >= 1,
                        UPPER_CHECK841)
            else:
                rec845, rows845 = fn845(j845)
        except BudgetR41 as eb845:
            BUDGET_STOP841 = True; log829('TEST845_BUDGET_STOP', str(eb845), 'job', ji845, 'of', nj845); break
        REC841[j845['job']] = rec845; ROWS841[j845['job']] = rows845; save_job841(j845['job'], rec845, rows845)
    if (ji845 + 1) % stp845 == 0 or ji845 + 1 == nj845:
        log829('TEST845_PROGRESS', 'JOBS', ji845 + 1, '/', nj845)
while LRU_R41:
    evict_r41()
D829['memo841R'] = dict(CNT_R41, states=len(SIG_R41), echo_states=len(ECHO_R41), hop=CNT845['hop'], hop_hit=CNT845['hop_hit'])
log829('TEST845_MEMO', json.dumps(D829['memo841R']))
'''

# ---------------- OFFLINE EVALUATION (labels are read only after the marker) ----------------
OFF845 = r'''
log829('TEST845_OFFLINE_START')
CATN_R = ('END', 'ALT_END', 'END3', 'MIDDLE', 'START', 'FORK_END', 'DECOY', 'BRIDGE_MID', 'BRIDGE_END')
NMK_R = ('end', 'changed_end', 'end3', 'middle', 'start', 'fork_end', 'decoy_end', 'bridge_mid', 'bridge_end')
ANSW_R = ('LIVE', 'FORK', 'BRIDGED', 'HOP3')
NODE_R = dict(zip(NMK_R, CATN_R))
def role_r(c, wi):
    if c not in CONTENT841:
        return 'NULL' if c == NULL829 else 'UNK'
    cw, k_, v_ = CONTENT841[c]
    return ('OWN_' if cw == wi else 'OTHER_') + k_.upper()
def tcat_r(t_, w):
    u = (t_ or '').upper(); cls = [c for c, k_ in zip(CATN_R, NMK_R) if w[k_] in u] + (['UNKNOWN'] if 'UNKNOWN' in u else [])
    return 'EMPTY_OR_OTHER' if not cls else cls[0] if len(cls) == 1 else ('MIXED' if 'UNKNOWN' in cls else 'MULTI')
def pcat_r(tid, w):
    if tid in UNKS845:
        return 'UNKNOWN'
    hit = [c for c, k_ in zip(CATN_R, NMK_R) if int(tok(w[k_], add_special_tokens=False).input_ids[0]) == tid or
           int(tok(' ' + w[k_], add_special_tokens=False).input_ids[0]) == tid]
    return hit[0] if len(hit) == 1 else ('AMBIG' if hit else 'OTHER')
def dist_r(xs):
    o_ = {}
    for x in xs:
        o_[str(x)] = o_.get(str(x), 0) + 1
    return o_
def chain_r(st, ids, s):
    if st == 'HOP3':
        return {ids['first'], ids['second'], ids['third']} <= s
    if st == 'BRIDGED':
        return {ids['first_bridged'], ids['bridgecont']} <= s
    return ids['first'] in s and (ids['second'] in s or ids['changed'] in s)
def grounded_r(st, ids, s, a):
    if st == 'HOP3':
        return a == 'END3' and chain_r(st, ids, s)
    if st == 'BRIDGED':
        return a == 'BRIDGE_END' and chain_r(st, ids, s)
    return ids['first'] in s and ((a == 'END' and ids['second'] in s) or (a == 'ALT_END' and ids['changed'] in s))
VPATH_R = {'HOP3': [('MIDDLE',), ('END',), ('END3',)], 'BRIDGED': [('BRIDGE_MID',), ('BRIDGE_END',)],
           'MISSING': [('MIDDLE',), ()], 'LIVE': [('MIDDLE',), ('END', 'ALT_END')], 'FORK': [('MIDDLE',), ('END', 'ALT_END')]}
def src_r(c, w):
    if c not in CONTENT841:
        return None
    cw, k_, v_ = CONTENT841[c]
    return (cw, NODE_R.get(REL841[k_][0]))
def jcase_r(r, wi, w, st):
    ids = w['ids']; S_ = r['steps']; fm = set(r['final_mounted'])
    pc = tcat_r(r['pointer_answer'], w) if r['pointer_answer'] is not None else None
    fc = tcat_r(r['answer_raw'], w)
    ok = r['end'] == 'PATH_COMPLETE' and grounded_r(st, ids, fm, pc)
    fok = grounded_r(st, ids, fm, fc)
    abst = r['end'] == 'ABSTAIN' or pc == 'UNKNOWN'
    term = abst if st == 'MISSING' else ok
    wrongnode, unkev, addr, needless, cur = False, [], [], 0, ['START']
    for s_ in S_:
        k = s_['k']; cur = cur[:k + 1] if len(cur) > k else cur
        node = cur[k] if k < len(cur) else None
        has = any(src_r(c, w) == (wi, node) for c in s_['mem'])
        unkev.append((s_['unk'], has))
        if s_['dec'] == 'SEARCH':
            needless += int(has)
            if k >= 1 and node not in (None, 'START'):
                addr.append(src_r(s_['cand'], w) == (wi, node))
        if s_['dec'] == 'ADVANCE':
            oc = tcat_r(s_['out'], w); vp = VPATH_R[st][k] if k < len(VPATH_R[st]) else ()
            wrongnode = wrongnode or oc not in vp
            cur = cur[:k + 1] + [oc]
        elif s_['dec'] == 'DEAD_END_BACKTRACK':
            cur = cur[:k]
    nsearch = sum(1 for s_ in S_ if s_['dec'] == 'SEARCH')
    pl_ok = r['plan']['N'] == (3 if st == 'HOP3' else 2)
    over = st == 'HOP3' and r['end'] == 'PATH_COMPLETE' and pc == 'END' and len(r['path']) == 2
    return {'world': wi, 'start': st, 'arm': r['arm'], 'end': r['end'], 'pointer_answer': pc, 'frame_answer': fc, 'final_ok': ok,
            'frame_ok': fok, 'terminal_ok': term, 'abstain': abst, 'false_abstain': st in ANSW_R and abst,
            'wrong_entity': (pc not in (None, 'UNKNOWN')) and not ok, 'path_wrong': wrongnode, 'corrected': wrongnode and ok,
            'chain_mounted': any(chain_r(st, ids, set(s_['mem'])) for s_ in S_) or chain_r(st, ids, fm), 'unk_events': unkev,
            'addr': addr, 'needless_search': needless, 'searches': nsearch, 'plan_ok': pl_ok, 'overreach_hop3': over, 'hops': r['hops'],
            'path': '>'.join(tcat_r(x, w) for x in r['path']), 'decs': '>'.join(s_['dec'] for s_ in S_),
            'outs': '>'.join(tcat_r(s_['out'], w) + ('@k%d' % s_['k']) for s_ in S_),
            'mem_final': '+'.join(role_r(c, wi) for c in r['final_mounted'])}
def icase_r(r, wi, w, st):
    ids = w['ids']; S_ = r['steps']; fm = set(r['final_mounted']); valid = {'HOP3': ('END3',), 'BRIDGED': ('BRIDGE_END',)}.get(st, ('END', 'ALT_END'))
    ansc = tcat_r(r['answer_raw'], w) if r['answer_raw'] is not None else None
    ok = ansc is not None and grounded_r(st, ids, fm, ansc)
    prov = [pcat_r(s_['sig']['top'], w) for s_ in S_]
    lean = [t for t, p_ in enumerate(prov) if p_ in CATN_R and p_ not in valid and t < len(S_) - 1]
    stop = r['end'] in ('SIGNAL_STOP',) or ansc == 'UNKNOWN'
    return {'world': wi, 'start': st, 'arm': r['arm'], 'end': r['end'], 'pointer_answer': None, 'frame_answer': ansc, 'final_ok': ok,
            'frame_ok': ok, 'terminal_ok': stop if st == 'MISSING' else ok, 'abstain': stop, 'false_abstain': st in ANSW_R and stop,
            'wrong_entity': ansc not in (None, 'UNKNOWN') and not ok, 'path_wrong': bool(lean), 'corrected': bool(lean) and ok,
            'chain_mounted': any(chain_r(st, ids, set(s_['mem'])) for s_ in S_) or chain_r(st, ids, fm), 'unk_events': [], 'addr': [],
            'needless_search': 0, 'searches': 0, 'plan_ok': None, 'overreach_hop3': st == 'HOP3' and ansc == 'END', 'hops': len(S_),
            'path': '>'.join(prov), 'decs': '>'.join(s_['dec'] for s_ in S_), 'outs': '', 'mem_final': '+'.join(role_r(c, wi) for c in r['final_mounted'])}
BY_R, DG_R, DV_R = {}, {}, {}
for j in JOBS841:
    if j['job'] in REC841:
        k = EVALKEY841[j['job']]; r = REC841[j['job']]
        if j['kind'] == 'DIAG':
            DG_R[k['world']] = r
        elif j['kind'] == 'DIAGV':
            DV_R[k['world']] = r
        else:
            BY_R[(k['world'], k['cond'], k['arm'])] = r
CASES_R = []
for wi, w in enumerate(worlds829):
    for st in STARTS41R:
        for a in ARMS41R:
            if (wi, st, a) in BY_R:
                CASES_R.append((jcase_r if a in JARMS845 else icase_r)(BY_R[(wi, st, a)], wi, w, st))
# ---- designed states: global readout (V, answer token) vs local hop outputs ----
say_r41('SUMMARY', 'DESIGNED STATES: answer-frame V and first token (global readout) | model plan | hop outputs (local) per world')
DT_R = {c: [] for c in DCONDS845}
for wi, w in enumerate(worlds829):
    for d in (DG_R.get(wi) or {'designs': []})['designs']:
        c = DCONDS845[d['i']]; hc = [('UNKNOWN' if x['unk'] else tcat_r(x['out'], w)) for x in d['hops']]
        top3 = [pcat_r(t_, w) for t_ in d['hops'][1]['top1']['ids'][:3]] if len(d['hops']) > 1 else []
        DT_R[c].append({'world': wi, 'V': d['sig']['V'], 'ans1': pcat_r(d['sig']['top'], w), 'plan': d['plan']['N'], 'hops': hc,
                        'hop1_top3': top3})
for c in DCONDS845:
    L_ = DT_R[c]
    if L_:
        say_r41('DESIGNED', c, 'n=%d' % len(L_), 'V_median=%+.2f V>tau=%d' % (float(np.median([x['V'] for x in L_])), sum(x['V'] > TAU841 for x in L_)),
                'ans1=%s' % dist_r([x['ans1'] for x in L_]), 'plan=%s' % dist_r([x['plan'] for x in L_]),
                'hop0=%s' % dist_r([x['hops'][0] if x['hops'] else None for x in L_]),
                'hop1=%s' % dist_r([x['hops'][1] if len(x['hops']) > 1 else 'none' for x in L_]),
                'hop2=%s' % dist_r([x['hops'][2] if len(x['hops']) > 2 else 'none' for x in L_]))
def dh_r(c, k, cat):
    return sum(1 for x in DT_R[c] if len(x['hops']) > k and x['hops'][k] == cat)
VT_R = {}
for wi, w in enumerate(worlds829):
    for x in (DV_R.get(wi) or {'variants': []})['variants']:
        VT_R.setdefault((x['d'], x['variant']), []).append((wi, 'UNKNOWN' if x['unk'] else tcat_r(x['out'], w), x['tok1'], x['p1'], x['top1']))
for (d, vn), L_ in sorted(VT_R.items()):
    say_r41('VARIANT', DCONDS845[d], vn, 'hop1=%s' % dist_r([x[1] for x in L_]))
def shift_r(d, vn):
    own = {x[0]: x for x in VT_R.get((d, 'OWN'), [])}; n_ = 0
    for x in VT_R.get((d, vn), []):
        o = own.get(x[0])
        if o is None:
            continue
        po = dict(zip(x[4]['ids'], x[4]['p'])).get(o[2], 0.0)
        n_ += int(x[1] != o[1] or x[2] != o[2] or abs(o[3] - po) >= 0.5)
    return n_
L1_R = {vn: shift_r(0, vn) for vn in ('OFF', 'ZERO', 'SWAP', 'REVERSE')}
END_V = {vn: sum(1 for x in VT_R.get((0, vn), []) if x[1] == 'END') for vn in ('OWN', 'OFF', 'ZERO', 'SWAP', 'REVERSE')}
LV1 = 'PASS' if all(v >= 10 for v in L1_R.values()) else 'FAIL'
SUFF_R = dh_r('D_SUFF', 1, 'END'); FIRST_R = dh_r('D_FIRST', 1, 'UNKNOWN'); MIRR_R = dh_r('D_MIRROR', 1, 'UNKNOWN')
LV2 = 'PASS' if (SUFF_R >= 10 and FIRST_R >= 10 and MIRR_R >= 9 and all(END_V[v] <= 6 for v in ('OFF', 'ZERO', 'SWAP', 'REVERSE'))) else 'FAIL'
# ---- loops ----
say_r41('SUMMARY', 'CASE CHAINS (roles attached offline)')
for x in CASES_R:
    say_r41('CASE', 'W%02d' % x['world'], x['start'], x['arm'], 'END=%s PTR=%s FRAME=%s ok=%s' % (x['end'], x['pointer_answer'], x['frame_answer'], x['final_ok']),
            'PATH=' + x['path'], 'DEC=' + x['decs'], 'OUT=' + x['outs'], 'FINAL=' + x['mem_final'])
def sel_r(arm=None, st=None):
    return [x for x in CASES_R if (arm is None or x['arm'] == arm) and (st is None or x['start'] in st)]
def n_r(f, arm, st=None):
    return sum(1 for x in sel_r(arm, st) if f(x))
say_r41('SUMMARY', 'TABLE per start x arm')
for st in STARTS41R:
    for a in ARMS41R:
        xs = sel_r(a, (st,))
        if xs:
            say_r41('TABLE', st, a, 'n=%d terminal_ok=%d grounded=%d frame_grounded=%d' % (len(xs), sum(x['terminal_ok'] for x in xs),
                    sum(x['final_ok'] for x in xs), sum(x['frame_ok'] for x in xs)),
                    'corrected=%d path_wrong=%d wrong_entity=%d abstain=%d chain=%d' % (sum(x['corrected'] for x in xs), sum(x['path_wrong'] for x in xs),
                    sum(x['wrong_entity'] for x in xs), sum(x['abstain'] for x in xs), sum(x['chain_mounted'] for x in xs)),
                    'ends=%s' % dist_r([x['end'] for x in xs]), 'hops_mean=%.1f' % float(np.mean([x['hops'] for x in xs])))
GR_R = {a: n_r(lambda x: x['final_ok'], a, ANSW_R) for a in ARMS41R}
FG_R = {a: n_r(lambda x: x['frame_ok'], a, ANSW_R) for a in ARMS41R}
TOT_R = {a: n_r(lambda x: x['terminal_ok'], a) for a in ARMS41R}
COR_R = {a: n_r(lambda x: x['corrected'], a, ANSW_R) for a in ARMS41R}
H3_R = {a: n_r(lambda x: x['final_ok'], a, ('HOP3',)) for a in ARMS41R}
MIS_R = {a: n_r(lambda x: x['terminal_ok'], a, ('MISSING',)) for a in ARMS41R}
WE_R = {a: n_r(lambda x: x['wrong_entity'], a) for a in ARMS41R}
JX_R = sel_r('JUNCTION')
UE_R = [e for x in JX_R for e in x['unk_events']]
UNKP_R = [sum(1 for u, h in UE_R if u and not h), sum(1 for u, h in UE_R if u)]
UNKR_R = [sum(1 for u, h in UE_R if u and not h), sum(1 for u, h in UE_R if not h)]
AD_R = [h for x in JX_R for h in x['addr']]
NS_R = [sum(x['needless_search'] for x in JX_R), sum(x['searches'] for x in JX_R)]
PLAN_R = [sum(1 for x in JX_R if x['plan_ok'] and x['start'] != 'HOP3'), sum(1 for x in JX_R if x['start'] != 'HOP3'),
          sum(1 for x in JX_R if x['plan_ok'] and x['start'] == 'HOP3'), sum(1 for x in JX_R if x['start'] == 'HOP3')]
BESTC_R = max(GR_R[a] for a in ('OFF', 'ZERO', 'SWAP', 'REVERSE'))
NOEFF_R = GR_R['JUNCTION'] - BESTC_R < 3
LV3 = 'PASS' if (GR_R['JUNCTION'] >= GR_R['IMCL'] + 6 and GR_R['JUNCTION'] >= BESTC_R + 6 and MIS_R['JUNCTION'] >= 9 and WE_R['JUNCTION'] <= 6) else 'FAIL'
LV4 = 'PASS' if (H3_R['JUNCTION'] >= 8 and all(H3_R['JUNCTION'] - H3_R[a] >= 3 for a in ARMS41R if a != 'JUNCTION') and
                 PLAN_R[0] >= 10 * PLAN_R[1] / 12.0 and PLAN_R[2] >= 10 * PLAN_R[3] / 12.0 and LV2 == 'PASS') else 'FAIL'
ADDR_R = 'PASS' if (len(AD_R) >= 10 and sum(AD_R) >= 0.75 * len(AD_R)) else 'FAIL'
ERR_R = 'PASS' if (UNKP_R[1] >= 20 and UNKR_R[1] >= 20 and UNKP_R[0] >= 0.85 * UNKP_R[1] and UNKR_R[0] >= 0.75 * UNKR_R[1] and MIRR_R >= 9) else 'FAIL'
NW_J = n_r(lambda x: x['path_wrong'], 'JUNCTION', ANSW_R)
CORR_R = ('NOT_DEMONSTRATED (fewer than 6 JUNCTION loops produced a wrong path node)' if NW_J < 6 else
          'PASS' if (COR_R['JUNCTION'] >= 6 and all(COR_R['JUNCTION'] - COR_R[a] >= 4 for a in ARMS41R if a != 'JUNCTION')) else 'FAIL')
RES_R = 'PASS' if (n_r(lambda x: x['chain_mounted'], 'JUNCTION', ANSW_R) >= 38 and NS_R[0] <= 0.15 * max(1, NS_R[1])) else 'FAIL'
STOP_R = 'PASS' if (MIS_R['JUNCTION'] >= 9 and n_r(lambda x: x['false_abstain'], 'JUNCTION', ANSW_R) <= 6 and
                    n_r(lambda x: x['overreach_hop3'], 'JUNCTION') <= 2) else 'FAIL'
if NOEFF_R:
    CORR_R = RES_R = STOP_R = 'NOT_DEMONSTRATED (changing the control state did not change the outcome)'
    ERR_R = ERR_R if ERR_R == 'FAIL' else 'NOT_DEMONSTRATED (changing the control state did not change the outcome)'
    LV3 = LV3 if LV3 == 'FAIL' else 'NOT_DEMONSTRATED'; LV4 = LV4 if LV4 == 'FAIL' else 'NOT_DEMONSTRATED'
EXT_R = not all(c['pass'] for c in D829['checks'])
VERD_R = {'PHYSICAL_MEMORY_INTEGRITY': 'FAIL' if EXT_R else 'PASS', 'L1_NUMERIC_CAUSALITY': LV1, 'L2_EVIDENCE_SENSITIVITY': LV2,
          'L3_BEHAVIOURAL_CONTROL': LV3, 'L4_AUTONOMOUS_RECURSION': LV4, 'MODEL_DERIVED_ADDRESS': ADDR_R,
          'MODEL_NATIVE_ERROR_DETECTION': ERR_R, 'MODEL_NATIVE_CORRECTION': CORR_R, 'MODEL_NATIVE_RESEARCH_DECISION': RES_R,
          'MODEL_NATIVE_STOP_DECISION': STOP_R, 'AUTONOMOUS_RECURSIVE_REASONING': LV4 + ' [scope: model outputs drive every hop; fixed frames, mechanical budgets]'}
dec845 = ('YETERSİZ KANIT' if BUDGET_STOP841 else 'DEVAM' if (LV2 == 'PASS' and LV3 == 'PASS') else
          'DUR' if (FIRST_R < 6 or MIRR_R < 6 or NOEFF_R) else 'YETERSİZ KANIT')
NUM_R = {'grounded_pointer_answer_48': GR_R, 'grounded_frame_answer_48': FG_R, 'terminal_ok_60': TOT_R, 'path_corrected_48': COR_R,
         'hop3_grounded_12': H3_R, 'missing_abstain_12': MIS_R, 'wrong_entity_60': WE_R,
         'designed_hop1_SUFF_END_FIRST_UNK_MIRROR_UNK': [SUFF_R, FIRST_R, MIRR_R],
         'designed_V_over_tau': {c: sum(x['V'] > TAU841 for x in DT_R[c]) for c in DCONDS845},
         'designed_hop2_D3_PAIR_UNK_D3_FULL_END3': [dh_r('D3_PAIR', 2, 'UNKNOWN'), dh_r('D3_FULL', 2, 'END3')],
         'designed_plan_2hop_3hop': [sum(1 for x in DT_R['D_SUFF'] if x['plan'] == 2), sum(1 for x in DT_R['D3_PAIR'] if x['plan'] == 3)],
         'conflict_hop1_top3_has_both': sum(1 for x in DT_R['D_CONFLICT'] if 'END' in x['hop1_top3'] and 'ALT_END' in x['hop1_top3']),
         'L1_variant_changes_of_12': L1_R, 'L2_SUFF_END_by_state': END_V, 'junction_unknown_precision': UNKP_R,
         'junction_unknown_recall': UNKR_R, 'junction_state_address_next_link': [sum(AD_R), len(AD_R)],
         'junction_needless_searches': NS_R, 'junction_plan_ok_2hop_3hop': PLAN_R, 'junction_wrong_path_loops_48': NW_J,
         'memo': D829.get('memo841R'), 'control_effect_absent': NOEFF_R}
for k_, v_ in NUM_R.items():
    say_r41('MEASURE', k_, json.dumps(v_))
for k_, v_ in VERD_R.items():
    say_r41('VERDICT', k_, v_)
say_r41('DECISION', dec845, HYP841['decision'])
for x in [x for x in JX_R if not x['terminal_ok']]:
    say_r41('FAILED_JUNCTION', 'W%02d' % x['world'], x['start'], 'END=' + x['end'], 'PATH=' + x['path'], 'DEC=' + x['decs'], 'OUT=' + x['outs'])
D829['report845'] = {'cases': CASES_R, 'designed': DT_R, 'variants': {'%d|%s' % k_: [list(y[:4]) for y in v_] for k_, v_ in VT_R.items()},
                     'measures': NUM_R, 'bypass': D829['bypass_verification841'], 'resume': D829['resume841']}
D829['verdict841R'] = {'decision': dec845, 'verdicts': VERD_R, 'measures': NUM_R, 'budget_stop': BUDGET_STOP841, 'reason': HYP841['decision']}
D829['cost841R'] = {'counted': dict(COUNT834), 'predicted_upper': POST841, 'run_seconds': D829['run_seconds841'],
                    'total_seconds_body': round(time.perf_counter() - T0_841, 3), 'peak_gpu_gib': float(_torch829.cuda.max_memory_allocated()) / 2**30}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f845:
    cols845 = sorted({k_ for x in CASES_R for k_ in x})
    wr845 = csv.DictWriter(f845, fieldnames=cols845, extrasaction='ignore')
    wr845.writeheader()
    for x in CASES_R:
        wr845.writerow({k_: (json.dumps(v_) if isinstance(v_, (list, dict)) else v_) for k_, v_ in x.items()})
D829['status'] = 'COMPLETE_TEST845_EVALUATED' if not BUDGET_STOP841 else 'STOPPED_BUDGET_PARTIAL_EVALUATED'
save829()
log829('TEST845_COMPLETED', str(OUT829))
'''

# ---------------- PATCH THE 844 DRIVER (every anchor counted) AND RUN IT ----------------
for a_, b_ in (('"SEED841 = 8415026"', '"SEED841 = 8455026"'),
               ('("PRED_LIMIT_MIN841 = 240.0", "PRED_LIMIT_MIN841 = 420.0")',
                '("PRED_LIMIT_MIN841 = 240.0", "PRED_LIMIT_MIN841 = 900.0"), ("HARD_BUDGET_MIN841 = 300.0", "HARD_BUDGET_MIN841 = 330.0")'),
               ('LRU_N841 = 8\\n"', 'LRU_N841 = 8; NVG841 = 1400; NEG841 = 500; SMAX845 = 3; HMAX845 = 14; CAP845 = 5; NHG845 = 5200; NMG845 = 3200; K845 = 8\\n"'),
               ("IMCL: modelin kendi değer sinyaliyle kapalı döngü (IMCL / STANDART / AÇIK / TERS / BOYUNDURUK), 2 ve 3 halkalı zincir",
                "NATIVE COGNITIVE CONTROL JUNCTION: modelin kendi işaretçi durumu (KAVŞAK / KAPALI / SIFIR / TAKAS / TERS / IMCL / STANDART)"),
               ("D829['test'] = '841R'", "D829['test'] = '845'"),
               ("TEST841-R BİLİMSEL ÖZET", "TEST845 BİLİMSEL ÖZET"), ("(5 başlangıç x 5 kol)", "(tanı + 5 başlangıç x 7 kol)"),
               ("WORLDS841 * 25", "WORLDS841 * 37"), ("print('TEST841-R hücresi:", "print('TEST845 (844 sürücüsü üzerinden):"),
               ("    memx, tmp, ms = mem_for841(list(k_), 'R41_%d' % CNT_R41['mounts'])\n",
                "    if CNT_R41['mounts'] >= NMG845:\n        raise BudgetR41('GLOBAL_MOUNT_CAP')\n    memx, tmp, ms = mem_for841(list(k_), 'R41_%d' % CNT_R41['mounts'])\n")):
    D845 = rp845(D845, a_, b_)
D845 = cut845(D845, "STARTS41R = ('LIVE', 'FORK', 'BRIDGED', 'MISSING', 'HOP3')\n",
              "ALLBANK841 = sorted({c for B in BANKS841", PANEL845)
D845 = cut845(D845, "def cost_upper841(tok_of, p_):", "\n'''\n\n# ---------------- PRE-REGISTERED HYPOTHESES", COST845)
D845 = cut845(D845, "HYP41R = {", "\n\n# ---------------- RUN (replaces", "HYP41R = " + repr(HYP845))
D845 = cut845(D845, "say_r41('PREREG', 'tau=", "'''\n\n# ---------------- OFFLINE EVALUATION", RUN845)
D845 = cut845(D845, "OFF41R = r'''", "'''\nB_ = BODY0_41R", "OFF41R = r'''" + OFF845)
for x_ in ("JUNCTION", "jloop845", "diagv845", "COST845" * 0 + "CAP845 + 1", "PATH_COMPLETE", "TEST845_OFFLINE_START"):
    assert x_ in D845, ('PATCH_MISSING', x_)
assert "'''" not in RUN845 + OFF845 + PANEL845 + COST845, 'TRIPLE_QUOTE'
ast.parse(D845)
print('TEST845 sürücüsü: 844.py blob %s doğrulandı; yamalı 844 sürücüsü %d bayt, SHA-256 %s' %
      (LOCK845[:12], len(D845), hashlib.sha256(D845.encode()).hexdigest()), flush=True)
exec(compile(D845, 'TEST845_DRIVER_844_PATCHED', 'exec'), globals())
