# AKBASCORE SILICON HIPPOCAMPUS — TEST841-R: Native Recursive Cognitive Bypass — Architectural Reconstruction
# Single Colab cell, one A100-80GB, frozen Qwen2.5-72B-Instruct NF4. Engine = the GPU-completed TEST841 cell (841.py git
# blob 135b18e5, fetched and SHA-1 verified at run time). Its locks, gates, CUT3 mount/seal, H3 bypass, M2-soft echo,
# PEAK50 router, store/resume and console layer are reused unchanged; the TEST841 job loop is CUT OUT (nothing of the
# 360-job TEST841 panel is executed). New: fresh sealed panel (+ 3-link chains), IMCL control law, 5 arms, offline audit.
# Recursion junction = the physical memory boundary: every memory state is a fresh CUT3 refusion of SSD cartridges
# (new RoPE positions, no stale KV); deep->input feedback = (1) the model's own answer-frame log-odds V(M) (credit /
# stop signal) and (2) M2-soft vocabulary re-entry (address). No hook, no weight write, no text replay, no training.
# IMCL law (fixed, label-free, class B) over model signals (class A):  V(M) = log p(top non-UNKNOWN) - log p(UNKNOWN)
#   at the first answer token; a_c = V(M) - V(M[c->NULL]); G(c|M) = V(M+c) - V(M+NULL).
#   ANSWER if M and V > ln100 and no a_c < 0 | RETRACT argmin a_c if some a_c < 0 | else PROPOSE (echo of M, or the
#   question cue if M is empty or the last echo candidate was rejected): ACCEPT if G > 0, else exclude; a rejected cue
#   candidate backtracks the newest card, or ends UNKNOWN when M is empty. Excluded cards never return.
# Arms (same panel, start, bank, step budget): IMCL | STANDARD (one answer pass) | OPEN (feedback off: 4 echo reads,
# then answer) | INVERT (sign of G and a reversed) | YOKED (partner world's IMCL decision sequence = matched irrelevant
# feedback). No GPU execution or result is claimed by the code author.
import urllib.request, hashlib, ast
URL41R = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/841.py"
LOCK41R = "135b18e5b1ea113579c607cf9eecf49628cf18c2"   # 841.py git blob (GPU-completed TEST841)
with urllib.request.urlopen(urllib.request.Request(URL41R, headers={"User-Agent": "AKBASCORE-TEST841R"}), timeout=180) as f_:
    raw41r = f_.read(400001)
assert hashlib.sha1(b"blob %d\0" % len(raw41r) + raw41r).hexdigest() == LOCK41R, "STOP_841_SOURCE_CHANGED"
S41R = raw41r.decode("utf-8").replace("TEST841", "TEST841R")
def rp41r(s, a, b, n=1):
    assert s.count(a) == n, ("PATCH_ANCHOR", a[:70], s.count(a))
    return s.replace(a, b)
for a_, b_ in (("SEED841 = 8412026", "SEED841 = 8415026"), ("T_MAX841 = 5 ", "T_MAX841 = 10 "),
               ("PRED_LIMIT_MIN841 = 240.0", "PRED_LIMIT_MIN841 = 420.0"),
               ("latent yeniden giriş (D1 / M2-yumuşak / M2-sert) + TEST840 bypass + GPU PEAK50 + fiziksel CUT3 + model-seçimli eylem döngüsü",
                "IMCL: modelin kendi değer sinyaliyle kapalı döngü (IMCL / STANDART / AÇIK / TERS / BOYUNDURUK), 2 ve 3 halkalı zincir"),
               ("BANK_KINDS841 = ('first', 'second', 'changed', 'mirror', 'decoy', 'fork', 'bridgecont')",
                "BANK_KINDS841 = ('first', 'second', 'changed', 'mirror', 'decoy', 'fork', 'bridgecont', 'third')"),
               ("ACTIONS841 = ('ANSWER', 'SEARCH', 'DROP', 'STOP')\n", "ACTIONS841 = ('ANSWER', 'SEARCH', 'DROP', 'STOP')\n"
                "TAU841 = math.log(100.0); MMAX841 = 4; T_OPEN841 = 4; NVG841 = 2600; NEG841 = 900; NAG841 = 700; LRU_N841 = 8\n"),
               ("'hypotheses': %r, 'body_sha256'", "'q3': Q3TEXT841, 'r_consts': [TAU841, MMAX841, T_OPEN841, NVG841, NEG841, NAG841], "
                "'hypotheses': %r, 'body_sha256'"),
               ("    w['fork_end'] = fresh841(); w['bridge_mid'] = fresh841(); w['bridge_end'] = fresh841()\n",
                "    w['fork_end'] = fresh841(); w['bridge_mid'] = fresh841(); w['bridge_end'] = fresh841(); w['end3'] = fresh841()\n"),
               ("'bridgecont': ('bridge_mid', 'bridge_end'), 'first_bridged': ('start', 'bridge_mid')}",
                "'bridgecont': ('bridge_mid', 'bridge_end'), 'first_bridged': ('start', 'bridge_mid'), 'third': ('end', 'end3')}"),
               ("QTEXT841 = {q['qid']: q['question'] for q in questions829}\n",
                "QTEXT841 = {q['qid']: q['question'] for q in questions829}\nQTEXT841.update(Q3TEXT841)\n"),
               ("    CON841['last'] = (CON841['last'] + [s[:300]])[-6:]\n",
                "    CON841['last'] = (CON841['last'] + [s[:300]])[-6:]\n    if s.startswith('T41R|'):\n"
                "        CON841['n41r'] = CON841.get('n41r', 0) + 1\n        if CON841['n41r'] == 4000:\n"
                "            say841('!! Konsol satırı 4000 oldu: Colab çıktı sınırına yaklaşılıyor; tüm kayıtlar ayrıca dosyada: ' + str(FULL_CONSOLE841))\n"
                "        say841(s[:2400]); return\n")):
    S41R = rp41r(S41R, a_, b_)
T41R = ast.parse(S41R)
def node41r(name, kind=ast.Assign):
    n = [x for x in T41R.body if isinstance(x, kind) and (getattr(x, 'name', None) == name or
         (kind is ast.Assign and getattr(x.targets[0], 'id', None) == name))]
    assert len(n) == 1, ("NODE", name)
    return n[0]
PANEL0_41R = node41r('PANEL_EXT841').value.value
BODY0_41R = node41r('BODY841').value.value

# ---------------- PANEL (fresh seed; sealed before any model call) ----------------
PANEL41R = PANEL0_41R[:PANEL0_41R.index("JOBS841, EVALKEY841 = [], {}")] + r'''
JOBS841, EVALKEY841 = [], {}
Q3TEXT841 = {w['world'] + '_H3': 'In domain ' + w['world'] + ', starting from ' + w['start'] +
             ', which endpoint is reached after exactly three directed links?' for w in worlds829}
STARTS41R = ('LIVE', 'FORK', 'BRIDGED', 'MISSING', 'HOP3')
ARMS41R = ('IMCL', 'STANDARD', 'OPEN', 'INVERT', 'YOKED')
def job41r(qid, role, bank, arm, start, partner):
    j = 'J41R_' + ''.join(_rng841.choice('0123456789ABCDEF') for _ in range(12))
    JOBS841.append({'job': j, 'kind': 'LOOP', 'qid': qid, 'mount': [], 'bank': list(bank), 'frame': 'A', 'arm': arm,
                    'start': list(start), 'partner': partner})
    EVALKEY841[j] = role
    return j
IMCL41R = {}
for arm in ARMS41R:                                   # IMCL first: YOKED partners must exist
    for wi, w in enumerate(worlds829):
        B = BANKS841[BLOCKOF841[wi]]; ids = w['ids']
        pw = ((BLOCKOF841[wi] + 1) % NBLOCK841) * BLOCK841 + wi % BLOCK841        # partner: other bank, same slot
        for st in STARTS41R:
            start = {'FORK': [ids['fork']], 'BRIDGED': [ids['first_bridged']]}.get(st, [])
            drop = {'MISSING': (ids['second'], ids['changed']), 'BRIDGED': (ids['first'],), 'HOP3': (ids['mirror'],)}.get(st, ())
            jid = job41r(w['world'] + '_H3' if st == 'HOP3' else QID841[wi], {'world': wi, 'cond': st, 'arm': arm},
                         [c for c in B['v0'] if c not in drop], arm, start, IMCL41R.get((st, pw)) if arm == 'YOKED' else None)
            if arm == 'IMCL':
                IMCL41R[(st, wi)] = jid
assert all(j['partner'] for j in JOBS841 if j['arm'] == 'YOKED'), 'YOKED_PARTNER'
JOBS841.sort(key=lambda j: (0 if j['arm'] == 'IMCL' else 1, _rng841.random()))
assert len(JOBS841) == len(EVALKEY841) == len(worlds829) * len(STARTS41R) * len(ARMS41R), 'JOB_COUNT'
ALLBANK841 = sorted({c for B in BANKS841 for v in ('v0', 'v1') for c in B[v]})
def fus_upper841(k, maxb, p_):
    if k <= 0:
        return 0
    c = int(globals().get('CHUNK', 128))
    return (p_ + maxb + c - 1) // c + (k - 1) * ((maxb + c - 1) // c)
def cost_upper841(tok_of, p_):
    mx = max(tok_of.values()); K = K_ECHO841; NJ = len(JOBS841); f5 = fus_upper841(MMAX841 + 1, mx, p_)
    up = {'fusion_forwards': 6 * fus_upper841(2, mx, p_) + (NVG841 + NEG841 + NAG841 + NJ) * f5, 'capture_forwards': 0,
          'probe_forwards': 12 + NVG841 + NEG841 + NAG841, 'rank_forwards': 0, 'bypass_forwards': 8 + NEG841 + 2 * len(worlds829),
          'generation_forwards': 1 + 3 * K + NEG841 * (K - 1) + NJ * MAX_NEW_ANS841}
    sec = MARGIN841 * (up['fusion_forwards'] * SEC_FUSION841 + up['generation_forwards'] * SEC_GEN841 +
                       up['bypass_forwards'] * SEC_BYPASS841 + up['probe_forwards'] * SEC_PROBE841 + 120.0 + len(tok_of) * 2.0)
    return {'numeric_upper': up, 'jobs': NJ, 'physical_cartridges': len(tok_of), 'bank_cartridges': len(ALLBANK841),
            'max_memory_tokens': p_ + (MMAX841 + 1) * mx, 'minutes_upper_excluding_model_load': round(sec / 60.0, 1),
            'cost_model': 'global caps: %d signal / %d echo / %d action probes; fusion %.2f s, token %.2f s, bypass %.2f s, '
                          'probe %.2f s, x%.2f margin' % (NVG841, NEG841, NAG841, SEC_FUSION841, SEC_GEN841, SEC_BYPASS841,
                                                          SEC_PROBE841, MARGIN841)}
'''

# ---------------- PRE-REGISTERED HYPOTHESES AND CRITERIA (fixed before any GPU result) ----------------
HYP41R = {
    'question': ('Can the frozen model\'s own answer-frame log-odds over physically mounted memories, fed back through a fixed '
                 'label-free credit law, detect wrong memories, retract them, redirect research, stop, and complete 2- and '
                 '3-link chains; and does the effect vanish when that feedback is removed (OPEN), reversed (INVERT) or '
                 'replaced by another case\'s decisions (YOKED)?'),
    'audit_basis': ['842/843 (identical): designed V medians NULL -8.5, first -5.25, pair +15.5, order +9.19, fork -5.25, '
                    'fork+decoy +0.31 (7/12 FORK_END), broken -6.31, bridge +16.9; action words never used DROP; corrections 0 '
                    'in every arm; echo from NULL memory = " UNKNOWN": cue from the question rows (840 [A] first 8/12).',
                    'TEST844 failure: 841 teardown runs del MEMNULL841 after its own 360-job loop; TEST841-R cuts the body '
                    'before that loop and checks every engine symbol before the first job.'],
    'law': {'V': 'log p(top non-UNKNOWN first answer token) - log p(UNKNOWN), answer frame of the generation itself',
            'credit': 'a_c = V(M) - V(M with c replaced by the NULL record)', 'gain': 'G = V(M+c) - V(M+NULL)',
            'tau': 'ln 100 (top entity 100x more likely than UNKNOWN; 842 fork+decoy +0.31 lies below, pair +15.5 above)',
            'order': 'ANSWER > RETRACT > CAPACITY_STOP (|M|=4, mechanical) > PROPOSE', 'budget': 'T=10 decisions (OPEN 4 reads)'},
    'arms': {'IMCL': 'law on own signals', 'STANDARD': 'one greedy answer on the start memory',
             'OPEN': 'feedback off: accept every routed card for 4 reads, then answer', 'INVERT': 'law with G and a sign-reversed',
             'YOKED': 'own echo/cue/memory, decisions copied from the partner world IMCL run (other bank, same start)'},
    'starts': {'LIVE': 'empty memory, full bank', 'FORK': 'S->F mounted (wrong first memory)',
               'BRIDGED': 'S->M\' mounted, bank without S->M (evidence change)', 'MISSING': 'empty, bank without M->E and M->E\'',
               'HOP3': '3-link question, bank without the E->M mirror (S->M->E->E3; M->E\' is a dead end)'},
    'criteria': {
        'MODEL_DERIVED_ADDRESS': 'IMCL echo proposals with a chain prefix mounted route to the next valid link in >= 80% of >= 10.',
        'MODEL_NATIVE_ERROR_DETECTION': 'IMCL proposals: good cards G>0 >= 75% and wrong cards G<=0 >= 75% (>= 10 each) AND '
                                        'IMCL entity answers that are not grounded-correct <= 4 of 48 answerable loops.',
        'MODEL_NATIVE_CORRECTION': 'CORRECTED = a provisional wrong entity at an earlier step, then a grounded-correct answer. '
                                   'IMCL >= 6 (48 answerable) AND IMCL - max(YOKED, INVERT) >= 4 AND IMCL - OPEN >= 2; '
                                   'NOT_DEMONSTRATED if fewer than 6 IMCL loops ever leaned wrong.',
        'MODEL_NATIVE_RESEARCH_DECISION': 'IMCL loops that mounted a wrong card and ended grounded-correct >= 50% of >= 8 AND '
                                          'exceed YOKED and INVERT by >= 4 each AND unnecessary search <= 20% of chain loops.',
        'MODEL_NATIVE_STOP_DECISION': 'IMCL MISSING ends by signal stop or UNKNOWN >= 9/12 AND IMCL false UNKNOWN on answerable '
                                      '<= 6/48 AND IMCL chain-mounted loops answer grounded-correct >= 80% (>= 6).',
        'AUTONOMOUS_RECURSIVE_REASONING': 'scope: fixed law over model-native signals. IMCL HOP3 grounded-correct >= 8/12 AND '
                                          'exceeds every other arm on HOP3 by >= 3.',
        'control_effect_rule': 'if IMCL terminal-correct exceeds YOKED by < 3 AND INVERT by < 3 (60 loops each), every '
                               'MODEL_NATIVE verdict and AUTONOMOUS become NOT_DEMONSTRATED.'},
    'decision': 'YETERSİZ KANIT on budget stop. DEVAM if CORRECTION PASS or (RESEARCH PASS and STOP PASS). DUR if IMCL '
                'answerable grounded-correct <= OPEN or the control effect rule fires. Otherwise YETERSİZ KANIT.',
    'classes': {'V, credits, gains, echo, cue rows, answer text': 'A (model computation)',
                'IMCL sign law, PEAK50 argmax, tau': 'B (fixed engineering rule, label-free)',
                'mount / exclusion / capacity / budgets / memo reuse': 'C (mechanical)'},
    'not_measured_deferred': ['non-synthetic memories', 'chains longer than three links', 'a learned or model-written control law',
                              'KORU vs DUZELT on conflicting records']}

# ---------------- RUN (replaces the TEST841 job loop; every engine function above it is unchanged) ----------------
RUN41R = r'''
D829['test'] = '841R'
D829['limitations841R'] = [
    'IMCL law, tau and the PEAK50 router are fixed engineering rules (class B); V, a, G are model computations (class A).',
    'Mount, exclusion, capacity (4 cards), step budget and global compute caps are mechanical (class C); budget and capacity '
    'ends are never reported as model decisions.',
    'Identical (question, ordered memory) states are evaluated once and reused across arms (deterministic frozen model).',
    'Runtime records show opaque cartridge IDs and card text; roles are attached only after the offline marker.',
    'Twelve sealed synthetic worlds, one card template, 2- and 3-link chains. No GPU result is claimed by the code author.']
gate829('ENGINE_SYMBOLS_841R', all(callable(globals().get(x)) for x in (
    'echo841', 'address841', 'h3_bypass841', 'route841', 'qrows841', 'index_embeds841', 'mem_for841', 'gen_answer841',
    'mount834', 'seal834', 'save_job841', 'cache_build', 'prompt_ids', 'answer_prompt829', 'action_prompt841', 'CallCount841'))
    and all(x in globals() for x in ('MEMNULL841', 'SEALNULL841', 'QIDS841', 'QSPAN841', 'REC841', 'KEYS841', 'MU841', 'T0_841')))
gate829('NULL_MEMORY_SEAL_841R_START', seal834(MEMNULL841) == SEALNULL841)
gate829('Q3_QUESTIONS_IN_ENGINE', len(Q3TEXT841) == WORLDS841 and all(q in QTEXT841 and q in QIDS841 for q in Q3TEXT841))
gate829('JOB_STARTS_AND_BANKS_PHYSICAL', all(c in KEYS841 for j in JOBS841 for c in j['bank']) and
        all(c in entries for j in JOBS841 for c in j['start']))
UNK_R41 = int(tok('UNKNOWN', add_special_tokens=False).input_ids[0])
ACT_R41 = {w_: int(tok(w_, add_special_tokens=False).input_ids[0]) for w_ in ACTIONS841}
D829['control_tokens841R'] = {'unknown': UNK_R41, 'actions': ACT_R41, 'tau': TAU841}
log829('TEST841R_CONTROL_TOKENS', json.dumps(D829['control_tokens841R']))
SIG_R41, ACTS_R41, ECHO_R41, CUE_R41, LRU_R41 = {}, {}, {}, {}, []
CNT_R41 = {'sig': 0, 'sig_hit': 0, 'act': 0, 'act_hit': 0, 'echo': 0, 'echo_hit': 0, 'ans': 0, 'mounts': 0, 'evict': 0}
class BudgetR41(Exception):
    pass
def key_r41(m):
    return tuple(m) if m else (NULL829,)
def evict_r41():
    k0, mx0, s0 = LRU_R41.pop(0)
    gate829('MEAS_KV_SEAL_R41_%d' % CNT_R41['evict'], seal834(mx0) == s0)
    CNT_R41['evict'] += 1
    del mx0
    gc.collect(); release()
def memx_r41(m):
    k_ = key_r41(m)
    if k_ == (NULL829,):
        return MEMNULL841
    for e_ in LRU_R41:
        if e_[0] == k_:
            return e_[1]
    memx, tmp, ms = mem_for841(list(k_), 'R41_%d' % CNT_R41['mounts'])
    CNT_R41['mounts'] += 1
    LRU_R41.append((k_, memx, seal834(memx)))
    while len(LRU_R41) > LRU_N841:
        evict_r41()
    return memx
def probe_r41(memx, text):
    ids = list(prompt_ids(text)); n = int(memx[0][0].shape[-2]); cache = cache_build(list(memx))
    pos = torch.arange(n, n + len(ids), device=DEV)
    with torch.no_grad():
        out = model(input_ids=torch.tensor([ids], device=DEV), past_key_values=cache,
                    attention_mask=torch.ones((1, n + len(ids)), device=DEV, dtype=torch.long),
                    position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
        lg = torch.log_softmax(out.logits[0, -1].float(), dim=-1)
        del out
    COUNT834['probe_forwards'] += 1
    del cache
    return lg
def sig_r41(q, m):
    k_ = (q, key_r41(m))
    if k_ in SIG_R41:
        CNT_R41['sig_hit'] += 1
        return SIG_R41[k_]
    if CNT_R41['sig'] >= NVG841:
        raise BudgetR41('GLOBAL_SIGNAL_CAP')
    lq = probe_r41(memx_r41(m), answer_prompt829(QTEXT841[q]))
    top = int(torch.argmax(lq)); l2 = lq.clone(); l2[UNK_R41] = -1e30; nu = int(torch.argmax(l2))
    s = {'V': round(float(lq[nu] - lq[UNK_R41]), 4), 'top': top, 'p_top': round(float(lq[top].exp()), 4), 'nonunk': nu,
         'p_unk': round(float(lq[UNK_R41].exp()), 4)}
    del lq, l2
    SIG_R41[k_] = s; CNT_R41['sig'] += 1
    return s
def act_r41(q, m):
    k_ = (q, key_r41(m))
    if k_ in ACTS_R41:
        CNT_R41['act_hit'] += 1
        return ACTS_R41[k_]
    if CNT_R41['act'] >= NAG841:
        raise BudgetR41('GLOBAL_ACTION_PROBE_CAP')
    la = probe_r41(memx_r41(m), action_prompt841(QTEXT841[q]))
    s = {k2: round(float(la[ACT_R41[w_]].exp()), 4) for k2, w_ in (('pA', 'ANSWER'), ('pS', 'SEARCH'), ('pD', 'DROP'), ('pX', 'STOP'))}
    s['act_top'] = int(torch.argmax(la))
    del la
    ACTS_R41[k_] = s; CNT_R41['act'] += 1
    return s
def route_r41(q, m, src, bank, X):
    ex = set(X) | set(m)
    if not [c for c in bank if c not in ex]:
        return None
    if src == 'CUE':
        if q not in CUE_R41:
            h_, ms_ = h3_bypass841(MEMNULL841, ids=QIDS841[q]); CUE_R41[q] = qrows841(h_, q).float().cpu()
            del h_
        r = route841(CUE_R41[q], bank, ex); info = {'via': 'CUE'}
    else:
        k_ = (q, key_r41(m))
        if k_ in ECHO_R41:
            CNT_R41['echo_hit'] += 1; e_ = ECHO_R41[k_]; r = route841(e_['qr'], bank, ex)
        else:
            if CNT_R41['echo'] >= NEG841:
                raise BudgetR41('GLOBAL_ECHO_CAP')
            r, inf_, last_, R_, qr_ = address841(memx_r41(m), q, 'A', 'M2S', bank, ex)
            e_ = {'qr': qr_.float().cpu(), 'echo': tok.decode([x['top_ids'][0] for x in inf_[:r['indexed_rows']]]),
                  'p0': inf_[0]['top_p'][0], 'H0': round(inf_[0]['entropy'], 4)}
            del last_, R_, qr_
            ECHO_R41[k_] = e_; CNT_R41['echo'] += 1
        info = {'via': 'ECHO', 'echo': e_['echo'], 'p0': e_['p0'], 'H0': e_['H0']}
    sc = sorted(r['scores'].values(), reverse=True)
    info.update({'chosen': r['chosen'], 'margin': round(sc[0] - (sc[1] if len(sc) > 1 else 0.0), 5), 'n_cand': len(sc)})
    return info
def answer_r41(q, m):
    CNT_R41['ans'] += 1
    return gen_answer841(memx_r41(m), q)['raw']
def rel_r41(c):
    t_ = cards829.get(c, '')
    return t_.splitlines()[1].replace('Directed relation: ', '').rstrip('.') if t_.count('\n') >= 2 else c
def mem_r41(m):
    return '[' + '; '.join(rel_r41(c) for c in m) + ']'
def tk_r41(t_):
    return repr(tok.decode([int(t_)]))
def say_r41(*parts):
    log829('T41R|' + DIR829.name + '|' + '|'.join(str(x) for x in parts))
ENDNAME_R41 = {'IMCL': 'SIGNAL_ANSWER', 'INVERT': 'SIGNAL_ANSWER', 'YOKED': 'YOKED_ANSWER', 'STANDARD': 'STANDARD_ANSWER'}
def loop_r41(j):
    q = j['qid']; arm = j['arm']; bank = j['bank']; M = list(j['start']); X = []; ev = []; steps = []; end = None; ans = None
    src = 'ECHO' if M else 'CUE'; sgn = -1.0 if arm == 'INVERT' else 1.0
    par = REC841.get(j['partner']) if arm == 'YOKED' else None
    if arm == 'YOKED' and par is None:
        raise RuntimeError('YOKED_PARTNER_RECORD_MISSING')
    T = 1 if arm == 'STANDARD' else T_OPEN841 if arm == 'OPEN' else T_MAX841
    for t in range(T):
        m0 = list(M); sg = sig_r41(q, M); st = {'t': t, 'mem': m0, 'src': src, 'sig': sg}; idx = None; cr = {}; ex_ = ''
        if arm == 'STANDARD':
            dec = 'ANSWER'
        elif arm in ('IMCL', 'INVERT'):
            st['act'] = act_r41(q, M)
            for i_, c_ in enumerate(M):
                cr[c_] = round(sg['V'] - sig_r41(q, M[:i_] + [NULL829] + M[i_ + 1:])['V'], 4)
            sa = {c_: sgn * v_ for c_, v_ in cr.items()}
            if M and sg['V'] > TAU841 and min(sa.values()) >= 0:
                dec = 'ANSWER'
            elif M and min(sa.values()) < 0:
                dec = 'RETRACT'; idx = min(range(len(M)), key=lambda i_: (sa[M[i_]], i_))
            elif len(M) >= MMAX841:
                dec = 'CAPACITY_STOP'
            else:
                dec = 'PROPOSE'
        elif arm == 'OPEN':
            dec = 'PROPOSE'
        else:
            pe = par['events'][t] if t < len(par['events']) else {'dec': 'PARTNER_ENDED', 'idx': None}
            dec = pe['dec']; idx = pe['idx']
        if dec in ('PROPOSE', 'ACCEPT', 'REJECT', 'REJECT_BACKTRACK'):
            if not M:
                src = 'CUE'
            pi = route_r41(q, M, src, bank, X)
            if pi is None:
                dec = 'NO_CANDIDATES'; end = 'NO_CANDIDATES'; ex_ = 'no candidate left (mechanical end)'
            else:
                c = pi['chosen']; st['cand'] = c; st['route'] = pi; st['cand_src'] = src
                if arm in ('IMCL', 'INVERT'):
                    gp = sig_r41(q, M + [c]); gn = sig_r41(q, M + [NULL829]); G = round(gp['V'] - gn['V'], 4)
                    st['G'] = G; st['cand_top'] = gp['top']
                    dec = 'ACCEPT' if sgn * G > 0 else 'REJECT' if src == 'ECHO' else 'REJECT_BACKTRACK' if M else 'STOP_UNKNOWN'
                elif arm == 'OPEN':
                    dec = 'ACCEPT'
                ex_ = '%s %s (%s) via %s%s margin=%.4f%s' % (dec, c, rel_r41(c), src, (' echo=%r p0=%.3f H0=%.3f' % (
                    pi['echo'][:24], pi['p0'], pi['H0'])) if src == 'ECHO' else '', pi['margin'], (' G=%+.2f' % st['G']) if 'G' in st else '')
                if dec == 'ACCEPT':
                    if len(M) >= (MMAX841 + 1 if arm == 'OPEN' else MMAX841):
                        dec = 'CAPACITY_STOP'; end = 'CAPACITY_STOP'
                    else:
                        M.append(c); src = 'ECHO'
                elif dec == 'REJECT':
                    X.append(c); src = 'CUE'
                elif dec == 'REJECT_BACKTRACK':
                    X.append(c)
                    if M:
                        st['backtracked'] = M.pop(); X.append(st['backtracked']); ex_ += ' | BACKTRACK ' + rel_r41(st['backtracked'])
                    src = 'ECHO' if M else 'CUE'
                else:
                    X.append(c); end = 'SIGNAL_STOP'; ex_ += ' | END UNKNOWN (signal stop)'
        elif dec == 'RETRACT':
            if M:
                st['retracted'] = M.pop(min(idx if idx is not None else len(M) - 1, len(M) - 1)); X.append(st['retracted'])
                ex_ = 'RETRACT ' + rel_r41(st['retracted'])
            src = 'ECHO' if M else 'CUE'
        elif dec == 'ANSWER':
            ans = answer_r41(q, M); end = ENDNAME_R41[arm]; ex_ = 'GENERATE_ANSWER %r' % ans[:60]
        elif dec == 'STOP_UNKNOWN':
            end = 'YOKED_STOP'; ex_ = 'END UNKNOWN (partner decision)'
        else:
            end = 'CAPACITY_STOP' if dec == 'CAPACITY_STOP' else 'NO_CANDIDATES' if dec == 'NO_CANDIDATES' else 'MECH_' + dec
            ex_ = 'mechanical end ' + end
        st['dec'] = dec; st['credit'] = cr; steps.append(st); ev.append({'dec': dec, 'idx': idx})
        sa_ = st.get('act')
        say_r41('STEP', j['job'], arm, 't%d' % t, 'MEM=' + mem_r41(m0), 'SIG V=%+.2f ans1=%s p=%.3f%s' % (
                sg['V'], tk_r41(sg['top']), sg['p_top'], (' | pA=%.2f pS=%.2f pX=%.2f' % (sa_['pA'], sa_['pS'], sa_['pX'])) if sa_ else ''),
                'CREDIT=' + ','.join('%+.2f' % cr[c_] for c_ in m0 if c_ in cr), 'DECISION=' + dec + (' (law on own signal)' if arm in ('IMCL', 'INVERT')
                else ' (partner signal)' if arm == 'YOKED' else ' (fixed)'), 'EXEC=' + ex_, 'NEXT=' + mem_r41(M))
        if end is not None:
            break
    if end is None and arm == 'OPEN':
        ans = answer_r41(q, M); end = 'FIXED_READS'
    if end is None:
        end = 'BUDGET_STOP'
    say_r41('END', j['job'], arm, 'END=' + end + (' (mechanical; NOT a model decision)' if end in ('BUDGET_STOP', 'CAPACITY_STOP',
            'NO_CANDIDATES', 'FIXED_READS') else ''), 'ANSWER=%r' % (ans or '')[:60], 'FINAL=' + mem_r41(M))
    return {'job': j['job'], 'kind': 'LOOP', 'qid': q, 'arm': arm, 'steps': steps, 'events': ev, 'end': end, 'answer_raw': ans,
            'final_mounted': M, 'excluded': X, 'partner': j['partner']}
say_r41('PREREG', 'tau=%.4f MMAX=%d T=%d T_OPEN=%d caps=%d/%d/%d' % (TAU841, MMAX841, T_MAX841, T_OPEN841, NVG841, NEG841, NAG841),
        'LAW=' + HYP841['law']['order'], 'DECISION_RULE=' + HYP841['decision'])
for k_, v_ in HYP841['criteria'].items():
    say_r41('PREREG', k_, v_)
UPPER_CHECK841 = {}
t_run841 = time.perf_counter()
nj41r = len(JOBS841); stp41r = max(1, nj41r // 12)
log829('TEST841R_PROGRESS', 'JOBS', 0, '/', nj41r)
for ji41r, j41r in enumerate(JOBS841):
    if j41r['job'] not in REC841:
        if (time.perf_counter() - T0_841) / 60.0 > HARD_BUDGET_MIN841:
            BUDGET_STOP841 = True; log829('TEST841R_BUDGET_STOP', 'job', ji41r, 'of', nj41r); break
        try:
            if not UPPER_CHECK841:
                with CallCount841() as ccu41r:
                    rec41r = loop_r41(j41r)
                UPPER_CHECK841 = ccu41r.summary()
                gate829('CUT3_MOUNT_AND_ANSWER_RUN_UPPER_LAYERS', UPPER_CHECK841['upper_min'] >= 1 and UPPER_CHECK841['lm_head'] >= 1,
                        UPPER_CHECK841)
            else:
                rec41r = loop_r41(j41r)
        except BudgetR41 as eb41r:
            BUDGET_STOP841 = True; log829('TEST841R_BUDGET_STOP', str(eb41r), 'job', ji41r, 'of', nj41r); break
        REC841[j41r['job']] = rec41r; ROWS841[j41r['job']] = {}; save_job841(j41r['job'], rec41r, {})
    if (ji41r + 1) % stp41r == 0 or ji41r + 1 == nj41r:
        log829('TEST841R_PROGRESS', 'JOBS', ji41r + 1, '/', nj41r)
while LRU_R41:
    evict_r41()
D829['memo841R'] = dict(CNT_R41, states=len(SIG_R41), echo_states=len(ECHO_R41))
log829('TEST841R_MEMO', json.dumps(D829['memo841R']))
'''

# ---------------- OFFLINE EVALUATION (labels are read only after the marker) ----------------
OFF41R = r'''
log829('TEST841R_OFFLINE_START')
CATN_R = ('END', 'ALT_END', 'END3', 'MIDDLE', 'START', 'FORK_END', 'DECOY', 'BRIDGE_MID', 'BRIDGE_END')
NMK_R = ('end', 'changed_end', 'end3', 'middle', 'start', 'fork_end', 'decoy_end', 'bridge_mid', 'bridge_end')
ANSW_R = ('LIVE', 'FORK', 'BRIDGED', 'HOP3')
GOOD_R = {'HOP3': {'OWN_FIRST', 'OWN_SECOND', 'OWN_THIRD'}, 'BRIDGED': {'OWN_FIRST_BRIDGED', 'OWN_BRIDGECONT'}}
VALID_R = {'HOP3': ('END3',), 'BRIDGED': ('BRIDGE_END',)}
def role_r(c, wi):
    if c not in CONTENT841:
        return 'NULL' if c == NULL829 else 'UNK'
    cw, k_, v_ = CONTENT841[c]
    return ('OWN_' if cw == wi else 'OTHER_') + k_.upper()
def tcat_r(t_, w):
    u = (t_ or '').upper(); cls = [c for c, k_ in zip(CATN_R, NMK_R) if w[k_] in u] + (['UNKNOWN'] if 'UNKNOWN' in u else [])
    return 'EMPTY_OR_OTHER' if not cls else cls[0] if len(cls) == 1 else ('MIXED' if 'UNKNOWN' in cls else 'MULTI')
def pcat_r(tid, w):
    if tid == UNK_R41:
        return 'UNKNOWN'
    hit = [c for c, k_ in zip(CATN_R, NMK_R) if int(tok(w[k_], add_special_tokens=False).input_ids[0]) == tid]
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
NXT_R = {'OWN_FIRST': ('OWN_SECOND', 'OWN_CHANGED'), 'OWN_FIRST_BRIDGED': ('OWN_BRIDGECONT',), 'OWN_SECOND': ('OWN_THIRD',)}
def case_r(r, wi, w, st):
    ids = w['ids']; good = GOOD_R.get(st, {'OWN_FIRST', 'OWN_SECOND', 'OWN_CHANGED'}); valid = VALID_R.get(st, ('END', 'ALT_END'))
    S_ = r['steps']; roles = [[role_r(c, wi) for c in s_['mem']] for s_ in S_]; prov = [pcat_r(s_['sig']['top'], w) for s_ in S_]
    fm = set(r['final_mounted']); ansc = tcat_r(r['answer_raw'], w) if r['answer_raw'] is not None else None
    ok = ansc is not None and grounded_r(st, ids, fm, ansc)
    lean = [t for t, p_ in enumerate(prov) if p_ in CATN_R and p_ not in valid and t < len(S_) - 1]
    wrongmem = [t for t, ro in enumerate(roles) if any(x not in good for x in ro)]
    answered = r['end'] in ('SIGNAL_ANSWER', 'YOKED_ANSWER', 'STANDARD_ANSWER', 'FIXED_READS')
    stoplike = r['end'] in ('SIGNAL_STOP', 'YOKED_STOP') or (answered and ansc == 'UNKNOWN')
    term = stoplike if st == 'MISSING' else ok
    props = [(role_r(s_['cand'], wi) in good, s_.get('G'), s_['dec']) for s_ in S_ if 'cand' in s_]
    chs = [t for t, s_ in enumerate(S_) if chain_r(st, ids, set(s_['mem']))]
    unnec = any(S_[t]['dec'] in ('ACCEPT', 'REJECT', 'REJECT_BACKTRACK') for t in chs)
    addr = []
    for s_, ro in zip(S_, roles):
        if s_.get('cand_src') == 'ECHO' and st != 'MISSING':
            nx = [y for x in ro for y in NXT_R.get(x, ()) if not (set(NXT_R.get(x, ())) & set(ro))]
            if nx:
                addr.append(role_r(s_['cand'], wi) in nx)
    ret = [role_r(s_[k2], wi) for s_ in S_ for k2 in ('retracted', 'backtracked') if k2 in s_]
    rej = [role_r(s_['cand'], wi) for s_ in S_ if 'cand' in s_ and s_['dec'] in ('REJECT', 'REJECT_BACKTRACK', 'STOP_UNKNOWN')]
    acc = [role_r(s_['cand'], wi) for s_ in S_ if 'cand' in s_ and s_['dec'] == 'ACCEPT']
    typ = ('CORRECTED' if (lean and ok) else 'RECOVERED' if (wrongmem and ok) else 'CORRECT_DIRECT' if ok else
           'CORRECT_STOP' if (st == 'MISSING' and term) else 'WRONG_ANSWER' if (answered and ansc != 'UNKNOWN') else
           'FALSE_UNKNOWN' if stoplike else r['end'])
    return {'world': wi, 'start': st, 'arm': r['arm'], 'type': typ, 'end': r['end'], 'answer': ansc, 'final_ok': ok,
            'terminal_ok': term, 'corrected': bool(lean and ok), 'recovered': bool(wrongmem and ok), 'leaned_wrong': bool(lean),
            'wrong_mounted': bool(wrongmem), 'premature_wrong': answered and ansc not in (None, 'UNKNOWN') and not ok,
            'false_unknown': st in ANSW_R and stoplike, 'chain_seen': bool(chs), 'unnecessary_search': unnec, 'addr': addr,
            'props': props, 'junk_accept': sum(x not in good for x in acc), 'good_rejected': sum(x in good for x in rej + ret),
            'retract_wrong': [sum(x not in good for x in ret), len(ret)], 'steps_n': len(S_),
            'dead_end_recovered': st == 'HOP3' and 'OWN_CHANGED' in acc and ok,
            'decs': '>'.join(s_['dec'] for s_ in S_), 'prov': '>'.join(prov), 'mem_roles': ' | '.join('+'.join(ro) or '-' for ro in roles),
            'cands': '>'.join(role_r(s_['cand'], wi) + '@' + s_['cand_src'] for s_ in S_ if 'cand' in s_),
            'V': [s_['sig']['V'] for s_ in S_], 'G': [s_.get('G') for s_ in S_ if 'cand' in s_]}
BY_R = {}
for j in JOBS841:
    if j['job'] in REC841:
        k = EVALKEY841[j['job']]; BY_R[(k['world'], k['cond'], k['arm'])] = REC841[j['job']]
CASES_R = [case_r(BY_R[(wi, st, a)], wi, w, st) for wi, w in enumerate(worlds829) for st in STARTS41R for a in ARMS41R
           if (wi, st, a) in BY_R]
say_r41('SUMMARY', 'CASE CHAINS (roles attached offline): memory roles per step | decisions | provisional first token | candidates | outcome')
for x in CASES_R:
    say_r41('CASE', 'W%02d' % x['world'], x['start'], x['arm'], 'TYPE=' + x['type'], 'END=%s ANSWER=%s' % (x['end'], x['answer']),
            'MEM=' + x['mem_roles'], 'DEC=' + x['decs'], 'PROV=' + x['prov'], 'CAND=' + x['cands'],
            'V=' + ','.join('%+.1f' % v for v in x['V']), 'G=' + ','.join('%+.1f' % g for g in x['G'] if g is not None))
def sel_r(arm=None, st=None):
    return [x for x in CASES_R if (arm is None or x['arm'] == arm) and (st is None or x['start'] in st)]
def n_r(f, arm, st=None):
    return sum(1 for x in sel_r(arm, st) if f(x))
say_r41('SUMMARY', 'TABLE per start x arm')
for st in STARTS41R:
    for a in ARMS41R:
        xs = sel_r(a, (st,))
        if xs:
            say_r41('TABLE', st, a, 'n=%d' % len(xs), 'terminal_ok=%d' % sum(x['terminal_ok'] for x in xs),
                    'corrected=%d recovered=%d leaned=%d' % (sum(x['corrected'] for x in xs), sum(x['recovered'] for x in xs),
                                                             sum(x['leaned_wrong'] for x in xs)),
                    'wrong_ans=%d false_unk=%d junk_acc=%d good_rej=%d' % (sum(x['premature_wrong'] for x in xs),
                    sum(x['false_unknown'] for x in xs), sum(x['junk_accept'] for x in xs), sum(x['good_rejected'] for x in xs)),
                    'ends=%s' % dist_r([x['end'] for x in xs]), 'types=%s' % dist_r([x['type'] for x in xs]),
                    'steps_mean=%.1f' % float(np.mean([x['steps_n'] for x in xs])))
PR_R = [p for x in sel_r('IMCL') for p in x['props'] if p[1] is not None]
GOODP_R = [p for p in PR_R if p[0]]; BADP_R = [p for p in PR_R if not p[0]]
ADR_R = [h for x in sel_r('IMCL') for h in x['addr']]
EVS_R = sum(1 for wi in range(len(worlds829)) if all(any(x['world'] == wi and x['start'] == s2 and x['terminal_ok'] for x in sel_r('IMCL'))
                                                   for s2 in ('LIVE', 'MISSING', 'BRIDGED')))
VA_R = [(s_['dec'], tok.decode([s_['act']['act_top']]).strip().upper()[:3]) for j in JOBS841 if j['arm'] == 'IMCL' and j['job'] in REC841
        for s_ in REC841[j['job']]['steps'] if 'act' in s_]
TOT_R = {a: n_r(lambda x: x['terminal_ok'], a) for a in ARMS41R}
ANS_R = {a: n_r(lambda x: x['final_ok'], a, ANSW_R) for a in ARMS41R}
COR_R = {a: n_r(lambda x: x['corrected'], a, ANSW_R) for a in ARMS41R}
REC_R = {a: n_r(lambda x: x['recovered'], a, ANSW_R) for a in ARMS41R}
H3_R = {a: n_r(lambda x: x['final_ok'], a, ('HOP3',)) for a in ARMS41R}
MIS_R = {a: n_r(lambda x: x['terminal_ok'], a, ('MISSING',)) for a in ARMS41R}
LEAN_I = n_r(lambda x: x['leaned_wrong'], 'IMCL', ANSW_R); WM_I = n_r(lambda x: x['wrong_mounted'], 'IMCL', ANSW_R)
CH_I = [x for x in sel_r('IMCL', ANSW_R) if x['chain_seen']]
NOEFF_R = (TOT_R['IMCL'] - TOT_R['YOKED'] < 3) and (TOT_R['IMCL'] - TOT_R['INVERT'] < 3)
ADDR_R = 'PASS' if (len(ADR_R) >= 10 and sum(ADR_R) >= 0.8 * len(ADR_R)) else 'FAIL'
ERR_R = ('PASS' if (len(GOODP_R) >= 10 and len(BADP_R) >= 10 and sum(p[1] > 0 for p in GOODP_R) >= 0.75 * len(GOODP_R) and
                    sum(p[1] <= 0 for p in BADP_R) >= 0.75 * len(BADP_R) and n_r(lambda x: x['premature_wrong'], 'IMCL', ANSW_R) <= 4)
         else 'FAIL')
CORR_R = ('NOT_DEMONSTRATED (fewer than 6 IMCL loops leaned wrong)' if LEAN_I < 6 else
          'PASS' if (COR_R['IMCL'] >= 6 and COR_R['IMCL'] - max(COR_R['YOKED'], COR_R['INVERT']) >= 4 and
                     COR_R['IMCL'] - COR_R['OPEN'] >= 2) else 'FAIL')
RES_R = ('NOT_DEMONSTRATED (fewer than 8 IMCL loops mounted a wrong card)' if WM_I < 8 else
         'PASS' if (REC_R['IMCL'] >= 0.5 * WM_I and REC_R['IMCL'] - REC_R['YOKED'] >= 4 and REC_R['IMCL'] - REC_R['INVERT'] >= 4 and
                    sum(x['unnecessary_search'] for x in CH_I) <= 0.2 * max(1, len(CH_I))) else 'FAIL')
STOP_R = ('NOT_DEMONSTRATED (fewer than 6 IMCL loops mounted a valid chain)' if len(CH_I) < 6 else
          'PASS' if (MIS_R['IMCL'] >= 9 and n_r(lambda x: x['false_unknown'], 'IMCL', ANSW_R) <= 6 and
                     sum(x['final_ok'] for x in CH_I) >= 0.8 * len(CH_I)) else 'FAIL')
AUT_R = 'PASS' if (H3_R['IMCL'] >= 8 and all(H3_R['IMCL'] - H3_R[a] >= 3 for a in ARMS41R if a != 'IMCL')) else 'FAIL'
if NOEFF_R:
    CORR_R = RES_R = STOP_R = AUT_R = 'NOT_DEMONSTRATED (changing the control signal did not change behaviour)'
    ERR_R = ERR_R if ERR_R == 'FAIL' else 'NOT_DEMONSTRATED (changing the control signal did not change behaviour)'
EXT_R = not all(c['pass'] for c in D829['checks'])
VERD_R = {'PHYSICAL_MEMORY_INTEGRITY': 'FAIL' if EXT_R else 'PASS', 'MODEL_DERIVED_ADDRESS': ADDR_R,
          'MODEL_NATIVE_ERROR_DETECTION': ERR_R, 'MODEL_NATIVE_CORRECTION': CORR_R, 'MODEL_NATIVE_RESEARCH_DECISION': RES_R,
          'MODEL_NATIVE_STOP_DECISION': STOP_R, 'AUTONOMOUS_RECURSIVE_REASONING': AUT_R + ' [scope: fixed law over model-native signals]'}
dec41r = ('YETERSİZ KANIT' if BUDGET_STOP841 else 'DEVAM' if (CORR_R == 'PASS' or (RES_R == 'PASS' and STOP_R == 'PASS')) else
          'DUR' if (ANS_R['IMCL'] <= ANS_R['OPEN'] or NOEFF_R) else 'YETERSİZ KANIT')
NUM_R = {'terminal_ok_by_arm_60': TOT_R, 'grounded_correct_answerable_48': ANS_R, 'corrected_48': COR_R, 'recovered_48': REC_R,
         'hop3_grounded_12': H3_R, 'missing_stop_or_unknown_12': MIS_R, 'imcl_leaned_wrong_loops': LEAN_I,
         'imcl_wrong_mounted_loops': WM_I, 'imcl_good_proposals_G_pos': [sum(p[1] > 0 for p in GOODP_R), len(GOODP_R)],
         'imcl_wrong_proposals_G_nonpos': [sum(p[1] <= 0 for p in BADP_R), len(BADP_R)],
         'imcl_G_median_good_wrong': [float(np.median([p[1] for p in GOODP_R])) if GOODP_R else None,
                                      float(np.median([p[1] for p in BADP_R])) if BADP_R else None],
         'imcl_echo_next_link': [sum(ADR_R), len(ADR_R)], 'imcl_wrong_answers_48': n_r(lambda x: x['premature_wrong'], 'IMCL', ANSW_R),
         'imcl_false_unknown_48': n_r(lambda x: x['false_unknown'], 'IMCL', ANSW_R),
         'imcl_chain_loops_correct': [sum(x['final_ok'] for x in CH_I), len(CH_I)],
         'imcl_unnecessary_search': [sum(x['unnecessary_search'] for x in CH_I), len(CH_I)],
         'imcl_retractions_wrong_total': [sum(x['retract_wrong'][0] for x in sel_r('IMCL')), sum(x['retract_wrong'][1] for x in sel_r('IMCL'))],
         'imcl_junk_accepts': sum(x['junk_accept'] for x in sel_r('IMCL')), 'imcl_good_rejected': sum(x['good_rejected'] for x in sel_r('IMCL')),
         'hop3_dead_end_recovered_imcl': n_r(lambda x: x['dead_end_recovered'], 'IMCL'),
         'evidence_sensitive_worlds_imcl': EVS_R, 'verbal_action_vs_law': dist_r(['%s/%s' % v for v in VA_R]),
         'memo': D829.get('memo841R'), 'control_effect_absent': NOEFF_R}
for k_, v_ in NUM_R.items():
    say_r41('MEASURE', k_, json.dumps(v_))
for k_, v_ in VERD_R.items():
    say_r41('VERDICT', k_, v_)
say_r41('DECISION', dec41r, HYP841['decision'])
for x in [x for x in sel_r('IMCL') if not x['terminal_ok']]:
    say_r41('FAILED_IMCL', 'W%02d' % x['world'], x['start'], 'TYPE=' + x['type'], 'DEC=' + x['decs'], 'PROV=' + x['prov'], 'CAND=' + x['cands'])
D829['report841R'] = {'cases': CASES_R, 'measures': NUM_R, 'control_tokens': D829['control_tokens841R'],
                      'bypass': D829['bypass_verification841'], 'resume': D829['resume841'], 'not_measured': HYP841['not_measured_deferred']}
D829['verdict841R'] = {'decision': dec41r, 'verdicts': VERD_R, 'measures': NUM_R, 'budget_stop': BUDGET_STOP841, 'reason': HYP841['decision']}
D829['cost841R'] = {'counted': dict(COUNT834), 'predicted_upper': POST841, 'run_seconds': D829['run_seconds841'],
                    'total_seconds_body': round(time.perf_counter() - T0_841, 3), 'peak_gpu_gib': float(_torch829.cuda.max_memory_allocated()) / 2**30}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f41r:
    cols41r = sorted({k_ for x in CASES_R for k_ in x})
    wr41r = csv.DictWriter(f41r, fieldnames=cols41r, extrasaction='ignore')
    wr41r.writeheader()
    for x in CASES_R:
        wr41r.writerow({k_: (json.dumps(v_) if isinstance(v_, (list, dict)) else v_) for k_, v_ in x.items()})
D829['status'] = 'COMPLETE_TEST841R_EVALUATED' if not BUDGET_STOP841 else 'STOPPED_BUDGET_PARTIAL_EVALUATED'
save829()
log829('TEST841R_COMPLETED', str(OUT829))
'''
B_ = BODY0_41R.replace("D829['test'] = '841'", "")
B_ = rp41r(B_, "JB841 = next(j for j in JOBS841 if j['kind'] == 'STATE' and j['mount'] != [NULL829])",
           "JB841 = {'mount': next(j['start'] for j in JOBS841 if j['start'])}\nJBANK41R = next(j['bank'] for j in JOBS841 if j['bank'])")
B_ = rp41r(B_, "JB841['bank']", "JBANK41R", 3)
k0_ = B_.index("KEYLAYERS841 = sorted(set(MID841) | {CUT})"); k1_ = B_.index("log829('TEST841R_MID_KEY_BANK', json.dumps(KF841))\n")
B_ = B_[:k0_] + B_[k1_ + len("log829('TEST841R_MID_KEY_BANK', json.dumps(KF841))\n"):]   # unused M1 key forge removed
MK41R = "# ====== OFFLINE" + " PHASE MARKER ======"
NEWBODY41R = (B_[:B_.index("UPPER_CHECK841 = {}\nt_run841")] + RUN41R +
              B_[B_.index("D829['run_seconds841'] = round("):B_.index(MK41R)] + MK41R + "\n" + OFF41R)
FINAL41R = r'''
def final841(D):
    V = D.get('verdict841R', {}); C = D.get('cost841R', {})
    say841('=' * 78); say841('TEST841-R BİLİMSEL ÖZET (vaka zincirleri yukarıda "T41R|" satırlarında; tam kayıt dosyada)'); say841('=' * 78)
    say841('Durum: %s | kapı: %d, başarısız %d | devam: yeniden kullanılan iş %s' % (D.get('status'), len(D.get('checks', [])),
           sum(not c['pass'] for c in D.get('checks', [])), D.get('resume841', {}).get('reused_jobs')))
    for k_, v_ in V.get('measures', {}).items():
        say841('  %-34s %s' % (k_, json.dumps(v_)))
    say841('-' * 78)
    for k_, v_ in V.get('verdicts', {}).items():
        say841('  %-32s %s' % (k_, v_))
    say841('=' * 78); say841('NİHAİ BİLİMSEL KARAR: %s' % V.get('decision')); say841('  Kural: ' + str(V.get('reason')))
    say841('Maliyet: %s | çalışma %s s | tepe VRAM %.2f GiB' % (C.get('counted'), C.get('run_seconds'), C.get('peak_gpu_gib', 0.0)))
'''
KAP41R = [x for x in T41R.body if isinstance(x, ast.Expr) and "'Kapsam:" in ast.unparse(x)]
assert len(KAP41R) == 1, 'KAPSAM'
REPL41R = sorted([(node41r('PANEL_EXT841'), "PANEL_EXT841 = " + repr(PANEL41R)), (node41r('HYP841'), "HYP841 = " + repr(HYP41R)),
                  (node41r('BODY841'), "BODY841 = " + repr(NEWBODY41R)), (node41r('final841', ast.FunctionDef), FINAL41R.strip("\n")),
                  (KAP41R[0], "say841('Kapsam: %d görülmemiş dünya, %d iş (5 başlangıç x 5 kol), 24 kartuşluk 4 banka + 3 halkalı soru | "
                              "K=%d yankı, IMCL bütçesi %d karar, tau=ln100' % (WORLDS841, WORLDS841 * 25, K_ECHO841, T_MAX841))")],
                 key=lambda p: -p[0].lineno)
L41R = S41R.splitlines(keepends=True)
for n_, txt_ in REPL41R:
    L41R[n_.lineno - 1:n_.end_lineno] = [txt_ + "\n"]
S41R = "".join(L41R)
ast.parse(S41R)
print('TEST841-R hücresi: TEST841 kaynağı blob %s doğrulandı; yamalı kaynak %d bayt, SHA-256 %s' %
      (LOCK41R[:12], len(S41R), hashlib.sha256(S41R.encode()).hexdigest()), flush=True)
exec(compile(S41R, 'TEST841R_CELL', 'exec'), globals())
