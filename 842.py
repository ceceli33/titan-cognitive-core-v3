# ===== TEST842 PARÇA 1/2 — aynı Colab hücresine sırayla yapıştırın =====
# AKBASCORE SILICON HIPPOCAMPUS — TEST842: does the MODEL'S OWN control signal correct a wrong first memory?
# Single Colab cell, one A100-80GB, frozen Qwen2.5-72B-Instruct NF4. Built on the GPU-completed TEST841 cell
# (841.py git blob 135b18e5, fetched and verified at run time); its engine, locks, gates, CUT3 mount, bypass, M2-soft
# re-entry router, store / resume and console layer are reused unchanged. Only the job panel, the run loop, the offline
# evaluation and the console summary are replaced. No GPU execution or result is claimed by the code author.
# Primary hypothesis H842: after a wrong first memory (fork / decoy / the model's own wrong first address), the model's
# memory-dependent control (own action word + own re-entry echo) redirects research to the correct memory and turns a
# wrong provisional inference into a correct final answer; the effect disappears when the echo is computed without
# the current memory (ABLATE) or from another case (SWAP). Same question, start, bank and step budget in all arms.
import urllib.request, hashlib, ast
URL842 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/841.py"
LOCK842 = "135b18e5b1ea113579c607cf9eecf49628cf18c2"   # 841.py git blob (GPU-completed TEST841)
with urllib.request.urlopen(urllib.request.Request(URL842, headers={"User-Agent": "AKBASCORE-TEST842"}), timeout=180) as f_:
    raw842 = f_.read(400001)
assert hashlib.sha1(b"blob %d\0" % len(raw842) + raw842).hexdigest() == LOCK842, "STOP_841_SOURCE_CHANGED"
S842 = raw842.decode("utf-8").replace("TEST841", "TEST842")
def rp842(s, a, b, n=1):
    assert s.count(a) == n, ("PATCH_ANCHOR", a[:70], s.count(a))
    return s.replace(a, b)
for a_, b_ in (("SEED841 = 8412026", "SEED841 = 8422026"), ("T_MAX841 = 5 ", "T_MAX841 = 6 "),
               ("PRED_LIMIT_MIN841 = 240.0", "PRED_LIMIT_MIN841 = 300.0"), ("HARD_BUDGET_MIN841 = 300.0", "HARD_BUDGET_MIN841 = 330.0"),
               ("latent yeniden giriş (D1 / M2-yumuşak / M2-sert) + TEST840 bypass + GPU PEAK50 + fiziksel CUT3 + model-seçimli eylem döngüsü",
                "kapalı döngü hata düzeltme: NORMAL / ABLASYON / NEDENSEL TAKAS (TEST841 motoru, M2-yumuşak)"),
               ("    CON841['last'] = (CON841['last'] + [s[:300]])[-6:]\n",
                "    CON841['last'] = (CON841['last'] + [s[:300]])[-6:]\n    if s.startswith('T842|'):\n"
                "        CON841['n842'] = CON841.get('n842', 0) + 1\n        if CON841['n842'] == 4000:\n"
                "            say841('!! Konsol satırı 4000 oldu: Colab çıktı sınırına yaklaşılıyor; tüm kayıtlar ayrıca dosyada: ' + str(FULL_CONSOLE841))\n"
                "        say841(s[:2400]); return\n")):
    S842 = rp842(S842, a_, b_)
T842 = ast.parse(S842)
def node842(name, kind=ast.Assign):
    n = [x for x in T842.body if isinstance(x, kind) and (getattr(x, 'name', None) == name or
         (kind is ast.Assign and getattr(x.targets[0], 'id', None) == name))]
    assert len(n) == 1, ("NODE", name)
    return n[0]
PANEL0_842 = node842('PANEL_EXT841').value.value
BODY0_842 = node842('BODY841').value.value

# ---------------- PANEL (fresh seed; sealed before any model call) ----------------
PANEL842 = PANEL0_842[:PANEL0_842.index("JOBS841, EVALKEY841 = [], {}")] + r'''
JOBS841, EVALKEY841 = [], {}
DES842 = ('D_NULL', 'D_FIRST', 'D_PAIR', 'D_ORDER', 'D_ID', 'D_FORK', 'D_FORKX', 'D_BROKEN', 'D_BRIDGE', 'D_CONFLICT', 'D_IRREL')
STARTS842 = ('LIVE', 'FORK', 'DECOY', 'BRIDGED', 'MISSING')
ARMS842 = ('NORMAL', 'ABLATE', 'SWAP')
def job842(kind, qid, role, mount=(), bank=(), arm=None, start=(), partner=None):
    j = 'J842_' + ''.join(_rng841.choice('0123456789ABCDEF') for _ in range(12))
    JOBS841.append({'job': j, 'kind': kind, 'qid': qid, 'mount': list(mount), 'bank': list(bank), 'frame': 'A', 'arm': arm,
                    'start': list(start), 'partner': partner})
    EVALKEY841[j] = role
    return j
NORM842 = {}
for arm in ARMS842:
    for wi, w in enumerate(worlds829):
        q = QID841[wi]; B = BANKS841[BLOCKOF841[wi]]; ids = w['ids']
        far = worlds829[((BLOCKOF841[wi] + 1) % NBLOCK841) * BLOCK841 + wi % BLOCK841]['ids']
        if arm == 'NORMAL':
            for cond, m in (('D_NULL', [NULL829]), ('D_FIRST', [ids['first']]), ('D_PAIR', [ids['first'], ids['second']]),
                            ('D_ORDER', [ids['second'], ids['first']]), ('D_ID', [ids['first_v1'], ids['second_v1']]),
                            ('D_FORK', [ids['fork']]), ('D_FORKX', [ids['fork'], ids['decoy']]),
                            ('D_BROKEN', [ids['first_bridged'], ids['second']]), ('D_BRIDGE', [ids['first_bridged'], ids['bridgecont']]),
                            ('D_CONFLICT', [ids['first'], ids['second'], ids['changed']]), ('D_IRREL', [ids['first'], far['second']])):
                job842('DES', q, {'world': wi, 'cond': cond}, mount=m)
        for st in STARTS842:
            start = {'FORK': [ids['fork']], 'DECOY': [ids['decoy']], 'BRIDGED': [ids['first_bridged']]}.get(st, [])
            bank = ([c for c in B['v0'] if c not in (ids['second'], ids['changed'])] if st == 'MISSING' else
                    [c for c in B['v0'] if c != ids['first']] if st == 'BRIDGED' else B['v0'])
            pw = ((BLOCKOF841[wi] + 1) % NBLOCK841) * BLOCK841 + wi % BLOCK841        # partner: other bank, same slot
            jid = job842('LOOP', q, {'world': wi, 'cond': st, 'arm': arm}, bank=bank, arm=arm, start=start,
                         partner=NORM842.get((st, pw)) if arm == 'SWAP' else None)
            if arm == 'NORMAL':
                NORM842[(st, wi)] = jid
assert all(j['partner'] for j in JOBS841 if j['arm'] == 'SWAP'), 'SWAP_PARTNER'
JOBS841.sort(key=lambda j: (0 if j['kind'] == 'DES' else 1 if j['arm'] == 'NORMAL' else 2, _rng841.random()))
assert len(JOBS841) == len(EVALKEY841) == len(worlds829) * (len(DES842) + len(STARTS842) * len(ARMS842)), 'JOB_COUNT'
ALLBANK841 = sorted({c for B in BANKS841 for v in ('v0', 'v1') for c in B[v]})
def fus_upper841(k, maxb, p_):
    if k <= 0:
        return 0
    c = int(globals().get('CHUNK', 128))
    return (p_ + maxb + c - 1) // c + (k - 1) * ((maxb + c - 1) // c)
def cost_upper841(tok_of, p_):
    mx = max(tok_of.values()); nw = len(worlds829); K = K_ECHO841; T = T_MAX841; nl = nw * len(STARTS842) * len(ARMS842)
    nd = nw * len(DES842); fl = sum(fus_upper841(1 + t, mx, p_) for t in range(T))
    up = {'fusion_forwards': 6 * fus_upper841(2, mx, p_) + nd * fus_upper841(3, mx, p_) + nl * 2 * fl, 'capture_forwards': 0,
          'probe_forwards': 12 + nd * 2 + nl * T * 3, 'rank_forwards': 0, 'bypass_forwards': 8 + nl * T,
          'generation_forwards': 1 + 3 * K + nd * (MAX_NEW_ACT841 + MAX_NEW_ANS841) + nl * (T * (MAX_NEW_ACT841 + K - 1) + MAX_NEW_ANS841)}
    sec = MARGIN841 * (up['fusion_forwards'] * SEC_FUSION841 + up['generation_forwards'] * SEC_GEN841 +
                       up['bypass_forwards'] * SEC_BYPASS841 + up['probe_forwards'] * SEC_PROBE841 + 120.0 + len(tok_of) * 2.0)
    return {'numeric_upper': up, 'jobs': len(JOBS841), 'physical_cartridges': len(tok_of), 'bank_cartridges': len(ALLBANK841),
            'max_memory_tokens': p_ + (T + 2) * mx, 'minutes_upper_excluding_model_load': round(sec / 60.0, 1),
            'cost_model': 'fusion %.2f s, token %.2f s, bypass %.2f s, probe %.2f s, x%.2f margin'
                          % (SEC_FUSION841, SEC_GEN841, SEC_BYPASS841, SEC_PROBE841, MARGIN841)}
'''

# ---------------- PRE-REGISTERED HYPOTHESES AND CRITERIA (fixed before any GPU result) ----------------
HYP842 = {
    'question': ('After a wrong first memory, does the model\'s own memory-dependent control redirect research and change a '
                 'wrong provisional inference into a correct final answer, and does the effect vanish when that control '
                 'signal is removed (ABLATE) or replaced by another case\'s signal (SWAP)?'),
    'audit_basis': ['841.log only (case files unavailable): M2-soft second address 12/12 conditional on a designed first card; '
                    'live loop 1/12; fork loops 0/12 valid with 9 MODEL_ANSWER; LIVE and MISSING end distributions almost '
                    'identical (STOP 6/6, ANSWER 4/5): termination not driven by evidence availability; designed two-card '
                    'states gave evidence-sensitive actions (pair ANSWER 10/12, broken SEARCH 12/12).',
                    'case-level chains of TEST841 are NOT available; nothing about them is assumed.'],
    'arms': {'NORMAL': 'action word and re-entry echo computed by the model over the CURRENT memory',
             'ABLATE': 'action word over the current memory; echo computed over NULL memory (memory feedback removed)',
             'SWAP': 'action word over the current memory; echo computed over another case\'s memory state at the same step '
                     '(other bank, same start) with that case\'s question'},
    'starts': {'LIVE': 'NULL, full bank (diagnostic replication of the TEST841 live loop with full trace)',
               'FORK': 'S->F mounted (designed wrong first memory)', 'DECOY': 'D->S mounted (designed wrong first memory)',
               'BRIDGED': 'S->M\' mounted, bank without S->M (relation change)', 'MISSING': 'NULL, bank without continuations'},
    'internal_signals': 'per step: action-token probabilities, answer first token, log P(top entity) - log P(UNKNOWN), '
                        'final-layer state change norm and cosine vs the previous step, echo token / probability / entropy, route margin',
    'criteria': {
        'MODEL_DERIVED_ADDRESS': 'NORMAL: after OWN_FIRST is mounted the next routed card is second/changed in >= 90% of '
                                 '>= 6 opportunities AND BRIDGED start first route = M\'-continuation in >= 9/12.',
        'MODEL_NATIVE_ERROR_DETECTION': 'designed: pair -> ANSWER with margin > 0 AND fork+decoy -> not ANSWER with margin < 0 '
                                        'AND broken bridge -> not ANSWER with margin < 0, in >= 10/12 worlds; AND NORMAL '
                                        'FORK+DECOY loops without a premature wrong answer >= 18/24.',
        'MODEL_NATIVE_CORRECTION': 'CORRECTED loop = a step with a wrong card mounted and a wrong-entity provisional answer, '
                                   'then MODEL_ANSWER with a valid endpoint and a valid chain mounted. Over LIVE+FORK+DECOY '
                                   '(36 per arm): NORMAL >= 12 AND NORMAL - ABLATE >= 6 AND NORMAL - SWAP >= 6.',
        'MODEL_NATIVE_RESEARCH_DECISION': 'NORMAL FORK+DECOY loops that route to OWN_FIRST after a wrong card >= 12/24 AND '
                                          'exceed ABLATE and SWAP by >= 4 each AND designed NULL/first -> SEARCH >= 10/12 each.',
        'MODEL_NATIVE_STOP_DECISION': 'NORMAL MISSING ends MODEL_STOP or answer UNKNOWN >= 9/12 AND NORMAL loops that mounted a '
                                      'valid chain end with a valid MODEL_ANSWER in >= 80% of >= 6 such loops (budget stops '
                                      'never count as model stops).',
        'AUTONOMOUS_RECURSIVE_REASONING': 'NOT_DEMONSTRATED by design (two-hop chains, fixed four-word vocabulary, fixed loop).',
        'control_effect_rule': 'if NORMAL and ABLATE trajectories are identical in >= 10/12 worlds for every start, no control '
                               'verdict may be PASS.'},
    'decision': 'DEVAM if MODEL_NATIVE_CORRECTION PASS. DUR if NORMAL corrections <= 2 or <= ABLATE + 1. Otherwise YETERSİZ KANIT.',
    'classes': {'action word, echo, answer, all signals': 'A (model computation, applied literally)',
                'PEAK50 argmax': 'B (fixed engineering router)', 'mount / DROP unmount / exclusion / budget': 'C (mechanical)'},
    'not_measured_deferred': ['chains longer than two links', 'KORU vs DUZELT policy on conflicting records (reported only)',
                              'non-synthetic memories', 'model-generated action vocabulary']}

# ---------------- RUN LOOP (replaces the TEST841 job loop; engine functions above it are unchanged) ----------------
RUN842 = r'''
D829['test'] = '842'
D829['limitations842'] = ['Only M2-soft re-entry is used (TEST841 CONVERSION PASS); D1 and M2-hard were not carried over.',
                          'Runtime records show opaque cartridge IDs and card text; roles are attached only after the offline marker.',
                          'TEST841 case files were not available; the TEST842 hypothesis rests on 841.log aggregates and code.']
ACT_TID842 = {w_: int(tok(w_, add_special_tokens=False).input_ids[0]) for w_ in ACTIONS841}
UNK_TID842 = int(tok('UNKNOWN', add_special_tokens=False).input_ids[0])
D829['control_tokens842'] = {'actions': ACT_TID842, 'unknown': UNK_TID842,
                             'action_first_tokens_distinct': len(set(ACT_TID842.values())) == len(ACT_TID842)}
log829('TEST842_CONTROL_TOKENS', json.dumps(D829['control_tokens842']))
def probe842(memx, text):
    ids = list(prompt_ids(text)); n = int(memx[0][0].shape[-2]); cache = cache_build(list(memx)); cap = []
    pos = torch.arange(n, n + len(ids), device=DEV)
    with torch.no_grad():
        with DirectCut3(model.model.layers[NL - 1], 'capture', collector=cap):
            out = model(input_ids=torch.tensor([ids], device=DEV), past_key_values=cache,
                        attention_mask=torch.ones((1, n + len(ids)), device=DEV, dtype=torch.long),
                        position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
            lg = torch.log_softmax(out.logits[0, -1].float(), dim=-1)
            del out
    COUNT834['probe_forwards'] += 1
    del cache
    return lg, cap[0][0, -1, :].float()
def sig842(memx, qid):
    la, _ = probe842(memx, action_prompt841(QTEXT841[qid]))
    lq, h = probe842(memx, answer_prompt829(QTEXT841[qid]))
    top = int(torch.argmax(lq)); lq2 = lq.clone(); lq2[UNK_TID842] = -1e30; nu = int(torch.argmax(lq2))
    s = {k_: round(float(la[ACT_TID842[w_]].exp()), 4) for k_, w_ in (('pA', 'ANSWER'), ('pS', 'SEARCH'), ('pD', 'DROP'), ('pX', 'STOP'))}
    s.update({'act_top': int(torch.argmax(la)), 'ans_top': top, 'ans_top_p': round(float(lq[top].exp()), 4), 'ans_nonunk': nu,
              'margin': round(float(lq[nu] - lq[UNK_TID842]), 4)})
    return s, h
def rel842(c):
    t_ = cards829.get(c, '')
    return 'NULL' if c == NULL829 else (t_.splitlines()[1].replace('Directed relation: ', '').rstrip('.') if t_.count('\n') >= 2 else c)
def mem842(m):
    return '[' + '; '.join(rel842(c) for c in m) + ']'
def tk842(t_):
    return repr(tok.decode([int(t_)]))
def say842(*parts):
    log829('T842|' + DIR829.name + '|' + '|'.join(str(x) for x in parts))
def sigs842(s):
    return ('pA=%.3f pS=%.3f pD=%.3f pX=%.3f act1=%s | ans1=%s p=%.3f m=%+.2f%s' % (s['pA'], s['pS'], s['pD'], s['pX'],
            tk842(s['act_top']), tk842(s['ans_top']), s['ans_top_p'], s['margin'],
            (' | dh=%.4g cos=%.4f' % (s['dh'], s['cos_prev'])) if 'dh' in s else ''))
def des842(j):
    memx, tmp, mms = mem_for841(j['mount'], 'D_' + j['job']); seal = seal834(memx)
    s, h = sig842(memx, j['qid'])
    oa = gen_action841(memx, j['qid']); ob = gen_answer841(memx, j['qid'])
    gate829('MEAS_KV_SEAL_D_' + j['job'], seal834(memx) == seal)
    del memx
    if tmp:
        gc.collect(); release()
    rec = {'job': j['job'], 'kind': 'DES', 'qid': j['qid'], 'mount': j['mount'], 'sig': s, 'action_raw': oa['raw'],
           'action': parse_action841(oa['raw']), 'answer_raw': ob['raw']}
    say842('DES', j['job'], 'MEM=' + mem842(j['mount']), 'SIG ' + sigs842(s), 'DECISION raw=%r -> %s' % (oa['raw'][:40], rec['action']),
           'ANSWER_TEXT=%r' % ob['raw'][:60])
    return rec
def loop842(j):
    q = j['qid']; arm = j['arm']; bank = j['bank']; work = list(j['start']); dropped = []; steps = []; end = None; ans = None; hp = None
    par = REC841.get(j['partner']) if arm == 'SWAP' else None
    if arm == 'SWAP' and par is None:
        raise RuntimeError('SWAP_PARTNER_RECORD_MISSING')
    say842('LOOP_START', j['job'], 'ARM=' + arm, 'START=' + mem842(work or [NULL829]), 'BANK=%d' % len(bank),
           'PARTNER=' + (j['partner'] if par else '-'))
    for t in range(T_MAX841):
        mount = list(work) if work else [NULL829]
        memx, tmp, mms = mem_for841(mount, 'L%s_%d' % (j['job'], t)); seal = seal834(memx)
        s, h = sig842(memx, q)
        if hp is not None:
            s['dh'] = float((h - hp).norm()); s['cos_prev'] = float((h * hp).sum() / (h.norm() * hp.norm()).clamp_min(1e-9))
        hp = h
        o = gen_action841(memx, q); act = parse_action841(o['raw'])
        st = {'t': t, 'mounted': mount, 'sig': s, 'action_raw': o['raw'], 'action': act}
        if act == 'ANSWER':
            ans = gen_answer841(memx, q)['raw']; end = 'MODEL_ANSWER'; ex_ = 'GENERATE_ANSWER %r' % ans[:60]
        elif act == 'STOP':
            end = 'MODEL_STOP'; ex_ = 'END_BY_MODEL_STOP'
        elif act == 'DROP':
            st['dropped'] = work.pop() if work else None
            if st['dropped'] is not None:
                dropped.append(st['dropped'])
            ex_ = 'UNMOUNT ' + (rel842(st['dropped']) if st['dropped'] else 'nothing (working set empty)')
        elif act == 'SEARCH':
            ex = set(work) | set(dropped)
            if not [c for c in bank if c not in ex]:
                end = 'NO_CANDIDATES'; ex_ = 'NO_CANDIDATES'
            else:
                if arm == 'NORMAL':
                    cm, cq, ctmp, src = memx, q, False, 'own memory'
                elif arm == 'ABLATE':
                    cm, cq, ctmp, src = MEMNULL841, q, False, 'NULL memory'
                else:
                    pst = par['steps'][min(t, len(par['steps']) - 1)]['mounted'] if par['steps'] else [NULL829]
                    cm, ctmp, _ = mem_for841(pst, 'P%s_%d' % (j['job'], t)); cq = par['qid']; src = 'partner ' + mem842(pst)
                r, info, last, R, qr = address841(cm, cq, 'A', 'M2S', bank, ex)
                if ctmp:
                    del cm; gc.collect(); release()
                top3 = sorted(r['scores'].items(), key=lambda kv: (-kv[1], kv[0]))[:3]
                ec = [(e_['top_ids'][0], e_['top_p'][0], round(e_['entropy'], 4)) for e_ in info[:r['indexed_rows']]]
                st['route'] = {'chosen': r['chosen'], 'top3': top3, 'indexed_rows': r['indexed_rows'], 'echo_src': src, 'echo': ec}
                work.append(r['chosen'])
                ex_ = 'MOUNT %s (%s) | echo=%r p0=%.3f H0=%.3f src=%s | route_margin=%.4f' % (
                    r['chosen'], rel842(r['chosen']), tok.decode([e_[0] for e_ in ec]), ec[0][1], ec[0][2], src,
                    top3[0][1] - (top3[1][1] if len(top3) > 1 else 0.0))
        else:
            end = 'INVALID_ACTION'; ex_ = 'END_INVALID_ACTION (model word not in the fixed vocabulary)'
        gate829('MEAS_KV_SEAL_L%s_%d' % (j['job'], t), seal834(memx) == seal)
        del memx
        if tmp:
            gc.collect(); release()
        steps.append(st)
        say842('STEP', j['job'], arm, 't%d' % t, 'MEMORY=' + mem842(mount), 'SIGNAL ' + sigs842(s),
               'DECISION raw=%r -> %s' % (o['raw'][:30], act), 'EXECUTED ' + ex_, 'NEXT_MEMORY=' + mem842(work or [NULL829]))
        if end is not None:
            break
    if end is None:
        end = 'BUDGET_STOP'
    say842('LOOP_END', j['job'], arm, 'END=' + end + (' (mechanical budget; NOT a model decision)' if end == 'BUDGET_STOP' else ''),
           'ANSWER=%r' % (ans or '')[:60], 'FINAL_MEMORY=' + mem842(work or [NULL829]))
    return {'job': j['job'], 'kind': 'LOOP', 'qid': q, 'arm': arm, 'steps': steps, 'end': end, 'answer_raw': ans,
            'final_mounted': work, 'dropped': dropped}
UPPER_CHECK841 = {}
t_run841 = time.perf_counter()
nj842 = len(JOBS841); stp842 = max(1, nj842 // 12)
log829('TEST842_PROGRESS', 'JOBS', 0, '/', nj842)
for ji842, j842 in enumerate(JOBS841):
    if j842['job'] not in REC841:
        if (time.perf_counter() - T0_841) / 60.0 > HARD_BUDGET_MIN841:
            BUDGET_STOP841 = True; log829('TEST842_BUDGET_STOP', 'job', ji842, 'of', nj842); break
        if j842['kind'] == 'DES' and not UPPER_CHECK841:
            with CallCount841() as ccu842:
                rec842 = des842(j842)
            UPPER_CHECK841 = ccu842.summary()
            gate829('CUT3_MOUNT_AND_ANSWER_RUN_UPPER_LAYERS', UPPER_CHECK841['upper_min'] >= 1 and UPPER_CHECK841['lm_head'] >= 1,
                    UPPER_CHECK841)
        else:
            rec842 = des842(j842) if j842['kind'] == 'DES' else loop842(j842)
        REC841[j842['job']] = rec842; ROWS841[j842['job']] = {}; save_job841(j842['job'], rec842, {})
    if (ji842 + 1) % stp842 == 0 or ji842 + 1 == nj842:
        log829('TEST842_PROGRESS', 'JOBS', ji842 + 1, '/', nj842)
'''

# ---------------- OFFLINE EVALUATION (labels are read only after the marker) ----------------

# ===== TEST842 PARÇA 2/2 — aynı Colab hücresine sırayla yapıştırın =====
OFF842 = r'''
log829('TEST842_OFFLINE_START')
CATN842 = ('END', 'ALT_END', 'MIDDLE', 'START', 'FORK_END', 'DECOY', 'BRIDGE_MID', 'BRIDGE_END')
NMK842 = ('end', 'changed_end', 'middle', 'start', 'fork_end', 'decoy_end', 'bridge_mid', 'bridge_end')
def role842(c, wi):
    if c == NULL829:
        return 'NULL'
    if c not in CONTENT841:
        return 'UNK'
    cw, k_, v_ = CONTENT841[c]
    return ('OWN_' if cw == wi else 'OTHER_') + k_.upper()
def tcat842(t_, w):
    u = (t_ or '').upper(); cls = [c for c, k_ in zip(CATN842, NMK842) if w[k_] in u] + (['UNKNOWN'] if 'UNKNOWN' in u else [])
    return 'EMPTY_OR_OTHER' if not cls else cls[0] if len(cls) == 1 else ('MIXED' if 'UNKNOWN' in cls else 'MULTI')
def pcat842(tid, w):
    if tid == UNK_TID842:
        return 'UNKNOWN'
    hit = [c for c, k_ in zip(CATN842, NMK842) if int(tok(w[k_], add_special_tokens=False).input_ids[0]) == tid]
    return hit[0] if len(hit) == 1 else ('AMBIG' if hit else 'OTHER')
def dist842(xs):
    o_ = {}
    for x in xs:
        o_[str(x)] = o_.get(str(x), 0) + 1
    return o_
BY842 = {}
for j in JOBS841:
    if j['job'] in REC841:
        k = EVALKEY841[j['job']]
        BY842.setdefault(k['world'], {})[k['cond'] + ('|' + j['arm'] if j['kind'] == 'LOOP' else '')] = REC841[j['job']]
NW842 = len(worlds829)
# ---- designed states ----
DT842 = {c: [] for c in DES842}
ERRD842 = []
for wi, w in enumerate(worlds829):
    d = BY842.get(wi, {})
    for c in DES842:
        if c in d:
            r = d[c]; valid = ('BRIDGE_END',) if c == 'D_BRIDGE' else ('END', 'ALT_END')
            DT842[c].append({'world': wi, 'action': r['action'], 'margin': r['sig']['margin'], 'pA': r['sig']['pA'], 'pS': r['sig']['pS'],
                             'pD': r['sig']['pD'], 'pX': r['sig']['pX'], 'prov': pcat842(r['sig']['ans_top'], w),
                             'answer': tcat842(r['answer_raw'], w)})
    if all(c in d for c in ('D_PAIR', 'D_FORKX', 'D_BROKEN')):
        ERRD842.append(d['D_PAIR']['action'] == 'ANSWER' and d['D_PAIR']['sig']['margin'] > 0 and
                       all(d[c]['action'] != 'ANSWER' and d[c]['sig']['margin'] < 0 for c in ('D_FORKX', 'D_BROKEN')))
say842('SUMMARY', 'DESIGNED STATES (action word / median margin logP(entity)-logP(UNKNOWN) / mean action probabilities / provisional first token / answer)')
for c in DES842:
    L_ = DT842[c]
    if L_:
        say842('DESIGNED', c, 'n=%d' % len(L_), 'action=%s' % dist842([x['action'] for x in L_]),
               'margin_median=%+.2f' % float(np.median([x['margin'] for x in L_])),
               'pA=%.3f pS=%.3f pD=%.3f pX=%.3f' % tuple(float(np.mean([x[k_] for x in L_])) for k_ in ('pA', 'pS', 'pD', 'pX')),
               'prov=%s' % dist842([x['prov'] for x in L_]), 'answer=%s' % dist842([x['answer'] for x in L_]))
# ---- loops: role-annotated case chains ----
GOOD842 = {'NULL', 'OWN_FIRST', 'OWN_SECOND', 'OWN_CHANGED'}
def case842(r, wi, w, st):
    ids = w['ids']; good = {'NULL', 'OWN_FIRST_BRIDGED', 'OWN_BRIDGECONT'} if st == 'BRIDGED' else GOOD842
    valid = ('BRIDGE_END',) if st == 'BRIDGED' else ('END', 'ALT_END')
    roles = [[role842(c, wi) for c in s_['mounted']] for s_ in r['steps']]
    prov = [pcat842(s_['sig']['ans_top'], w) for s_ in r['steps']]
    fm = set(r['final_mounted'])
    chain = ((ids['first_bridged'] in fm and ids['bridgecont'] in fm) if st == 'BRIDGED' else
             (ids['first'] in fm and bool(fm & {ids['second'], ids['changed']})))
    ansc = tcat842(r['answer_raw'], w) if r['answer_raw'] is not None else None
    ok = r['end'] == 'MODEL_ANSWER' and ansc in valid and chain
    wrong = [t for t, ro in enumerate(roles) if any(x not in good for x in ro) and prov[t] not in valid + ('UNKNOWN',)]
    seen = False; redirect = False; routed = []
    for s_, ro in zip(r['steps'], roles):
        seen = seen or any(x not in good for x in ro)
        if 'route' in s_:
            routed.append(role842(s_['route']['chosen'], wi))
            redirect = redirect or (seen and s_['route']['chosen'] == ids['first'])
    sec = []
    for s_, ro in zip(r['steps'], roles):
        if 'route' in s_ and ('OWN_FIRST' in ro):
            sec.append(role842(s_['route']['chosen'], wi) in ('OWN_SECOND', 'OWN_CHANGED'))
    term_ok = (r['end'] == 'MODEL_STOP' or (r['end'] == 'MODEL_ANSWER' and ansc == 'UNKNOWN')) if st == 'MISSING' else ok
    typ = ('CORRECTED' if (wrong and ok) else 'CORRECT_WITHOUT_ERROR' if ok else
           ('CORRECT_STOP' if term_ok else 'PREMATURE_WRONG_ANSWER') if r['end'] == 'MODEL_ANSWER' else
           ('CORRECT_STOP' if term_ok else r['end']))
    return {'world': wi, 'start': st, 'arm': r['arm'], 'type': typ, 'end': r['end'], 'answer': ansc, 'final_ok': ok, 'terminal_ok': term_ok,
            'corrected': bool(wrong and ok), 'first_wrong_step': wrong[0] if wrong else None, 'redirect_to_first': redirect,
            'premature_wrong_answer': r['end'] == 'MODEL_ANSWER' and not term_ok, 'chain_mounted': chain,
            'first_route': routed[0] if routed else None, 'second_hits': sec, 'drops': sum(1 for s_ in r['steps'] if s_['action'] == 'DROP'),
            'actions': '>'.join(s_['action'] for s_ in r['steps']), 'prov': '>'.join(prov), 'routed': '>'.join(routed),
            'mem_roles': ' | '.join('+'.join(ro) for ro in roles),
            'traj': [(s_['action'], list(CONTENT841.get(s_.get('route', {}).get('chosen'), (None, None, None))[:2])) for s_ in r['steps']]}
CASES842 = []
for wi, w in enumerate(worlds829):
    for st in STARTS842:
        for arm in ARMS842:
            r = BY842.get(wi, {}).get(st + '|' + arm)
            if r:
                CASES842.append(case842(r, wi, w, st))
say842('SUMMARY', 'CASE CHAINS (roles attached offline): memory roles per step | actions | provisional first token | routed roles | outcome')
for x in CASES842:
    say842('CASE', 'W%02d' % x['world'], x['start'], x['arm'], 'TYPE=' + x['type'], 'END=%s ANSWER=%s' % (x['end'], x['answer']),
           'MEM=' + x['mem_roles'], 'ACT=' + x['actions'], 'PROV=' + x['prov'], 'ROUTED=' + x['routed'],
           'first_wrong_step=%s redirect_to_first=%s drops=%d' % (x['first_wrong_step'], x['redirect_to_first'], x['drops']))
def cnt842(f, st=None, arm=None):
    xs = [x for x in CASES842 if (st is None or x['start'] in st) and (arm is None or x['arm'] == arm)]
    return sum(1 for x in xs if f(x)), len(xs)
say842('SUMMARY', 'LOOP TABLE per start x arm')
for st in STARTS842:
    for arm in ARMS842:
        xs = [x for x in CASES842 if x['start'] == st and x['arm'] == arm]
        if xs:
            say842('TABLE', st, arm, 'n=%d' % len(xs), 'terminal_ok=%d' % sum(x['terminal_ok'] for x in xs),
                   'corrected=%d' % sum(x['corrected'] for x in xs), 'redirect_to_first=%d' % sum(x['redirect_to_first'] for x in xs),
                   'premature_wrong=%d' % sum(x['premature_wrong_answer'] for x in xs), 'types=%s' % dist842([x['type'] for x in xs]),
                   'ends=%s' % dist842([x['end'] for x in xs]), 'drops=%d' % sum(x['drops'] for x in xs),
                   'first_route=%s' % dist842([x['first_route'] for x in xs]))
IDENT842 = {}
for st in STARTS842:
    tr = {(x['world'], x['arm']): x['traj'] for x in CASES842 if x['start'] == st}
    IDENT842[st] = sum(1 for wi in range(NW842) if (wi, 'NORMAL') in tr and tr.get((wi, 'NORMAL')) == tr.get((wi, 'ABLATE')))
say842('CONTROL_EFFECT', 'worlds where NORMAL and ABLATE trajectories are identical (action + routed content): %s' % IDENT842)
NOEFFECT842 = all(v >= 10 for v in IDENT842.values())
# ---- verdicts (pre-registered) ----
sh = [h_ for x in CASES842 if x['arm'] == 'NORMAL' for h_ in x['second_hits']]
br = cnt842(lambda x: x['first_route'] == 'OWN_BRIDGECONT', ('BRIDGED',), 'NORMAL')
ADDR842 = 'PASS' if (len(sh) >= 6 and sum(sh) >= 0.9 * len(sh) and br[0] >= 9) else 'FAIL'
pre842 = cnt842(lambda x: not x['premature_wrong_answer'], ('FORK', 'DECOY'), 'NORMAL')
ERR842 = 'PASS' if (sum(ERRD842) >= 10 and pre842[0] >= 18) else 'FAIL'
cor = {a: cnt842(lambda x: x['corrected'], ('LIVE', 'FORK', 'DECOY'), a)[0] for a in ARMS842}
red = {a: cnt842(lambda x: x['redirect_to_first'], ('FORK', 'DECOY'), a)[0] for a in ARMS842}
dsr = [sum(1 for x in DT842[c] if x['action'] == 'SEARCH') for c in ('D_NULL', 'D_FIRST')]
CORR842 = 'PASS' if (cor['NORMAL'] >= 12 and cor['NORMAL'] - cor['ABLATE'] >= 6 and cor['NORMAL'] - cor['SWAP'] >= 6) else 'FAIL'
RES842 = 'PASS' if (red['NORMAL'] >= 12 and red['NORMAL'] - red['ABLATE'] >= 4 and red['NORMAL'] - red['SWAP'] >= 4 and min(dsr) >= 10) else 'FAIL'
mis = cnt842(lambda x: x['terminal_ok'], ('MISSING',), 'NORMAL')
chl = [x for x in CASES842 if x['arm'] == 'NORMAL' and x['chain_mounted'] and x['start'] != 'MISSING']
STOP842 = ('NOT_DEMONSTRATED (fewer than 6 NORMAL loops mounted a valid chain)' if len(chl) < 6 else
           'PASS' if (mis[0] >= 9 and sum(x['final_ok'] for x in chl) >= 0.8 * len(chl)) else 'FAIL')
if NOEFFECT842:
    CORR842 = RES842 = 'NOT_DEMONSTRATED (control signal change did not change the trajectory)'
    ERR842 = ERR842 if ERR842 == 'FAIL' else 'NOT_DEMONSTRATED (control signal change did not change the trajectory)'
EXT842 = not all(c['pass'] for c in D829['checks'])
VERD842 = {'PHYSICAL_MEMORY_INTEGRITY': 'PASS' if not EXT842 else 'FAIL', 'MODEL_DERIVED_ADDRESS': ADDR842,
           'MODEL_NATIVE_ERROR_DETECTION': ERR842, 'MODEL_NATIVE_CORRECTION': CORR842, 'MODEL_NATIVE_RESEARCH_DECISION': RES842,
           'MODEL_NATIVE_STOP_DECISION': STOP842,
           'AUTONOMOUS_RECURSIVE_REASONING': 'NOT_DEMONSTRATED (two-hop chains, fixed vocabulary and loop)'}
dec842 = ('YETERSİZ KANIT' if BUDGET_STOP841 else 'DEVAM' if CORR842 == 'PASS' else
          'DUR' if (cor['NORMAL'] <= 2 or cor['NORMAL'] <= cor['ABLATE'] + 1) else 'YETERSİZ KANIT')
NUM842 = {'second_address_hits': [sum(sh), len(sh)], 'bridged_first_route_bridgecont': list(br), 'designed_error_discrimination': [sum(ERRD842), len(ERRD842)],
          'no_premature_wrong_fork_decoy_normal': list(pre842), 'corrected_by_arm': cor, 'redirect_by_arm': red,
          'designed_search_null_first': dsr, 'missing_terminal_ok_normal': list(mis),
          'chain_loops_final_ok_normal': [sum(x['final_ok'] for x in chl), len(chl)], 'normal_ablate_identical': IDENT842}
for k_, v_ in NUM842.items():
    say842('MEASURE', k_, json.dumps(v_))
for k_, v_ in VERD842.items():
    say842('VERDICT', k_, v_)
say842('DECISION', dec842, HYP842['decision'])
FAILED842 = [x for x in CASES842 if x['arm'] == 'NORMAL' and not x['terminal_ok']]
say842('SUMMARY', 'FAILED NORMAL CASES: %d (each listed above as CASE ... NORMAL with its first wrong step)' % len(FAILED842))
for x in FAILED842:
    say842('FAILED', 'W%02d' % x['world'], x['start'], 'TYPE=' + x['type'], 'first_wrong_step=%s' % x['first_wrong_step'],
           'ACT=' + x['actions'], 'PROV=' + x['prov'], 'ROUTED=' + x['routed'])
D829['report842'] = {'designed': DT842, 'cases': CASES842, 'measures': NUM842, 'control_tokens': D829['control_tokens842'],
                     'bypass': D829['bypass_verification841'], 'resume': D829['resume841'], 'not_measured': HYP841['not_measured_deferred']}
D829['verdict842'] = {'decision': dec842, 'verdicts': VERD842, 'measures': NUM842, 'budget_stop': BUDGET_STOP841,
                      'reason': HYP841['decision']}
D829['cost842'] = {'counted': dict(COUNT834), 'predicted_upper': POST841, 'run_seconds': D829['run_seconds841'],
                   'total_seconds_body': round(time.perf_counter() - T0_841, 3), 'peak_gpu_gib': float(_torch829.cuda.max_memory_allocated()) / 2**30}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f842:
    cols842 = sorted({k_ for x in CASES842 for k_ in x if k_ != 'traj'})
    wr842 = csv.DictWriter(f842, fieldnames=cols842, extrasaction='ignore')
    wr842.writeheader()
    for x in CASES842:
        wr842.writerow({k_: (json.dumps(v_) if isinstance(v_, (list, dict)) else v_) for k_, v_ in x.items() if k_ != 'traj'})
D829['status'] = 'COMPLETE_TEST842_EVALUATED' if not BUDGET_STOP841 else 'STOPPED_BUDGET_PARTIAL_EVALUATED'
save829()
log829('TEST842_COMPLETED', str(OUT829))
'''
B_ = BODY0_842.replace("D829['test'] = '841'", "")
B_ = rp842(B_, "JB841 = next(j for j in JOBS841 if j['kind'] == 'STATE' and j['mount'] != [NULL829])",
           "JB841 = next(j for j in JOBS841 if j['kind'] == 'DES' and j['mount'] != [NULL829])\n"
           "JBANK842 = next(j['bank'] for j in JOBS841 if j['bank'])")
B_ = rp842(B_, "JB841['bank']", "JBANK842", 3)
k0_ = B_.index("KEYLAYERS841 = sorted(set(MID841) | {CUT})"); k1_ = B_.index("log829('TEST842_MID_KEY_BANK', json.dumps(KF841))\n")
B_ = B_[:k0_] + B_[k1_ + len("log829('TEST842_MID_KEY_BANK', json.dumps(KF841))\n"):]   # unused M1 key forge removed
MK842 = "# ====== OFFLINE" + " PHASE MARKER ======"
NEWBODY842 = (B_[:B_.index("UPPER_CHECK841 = {}\nt_run841")] + RUN842 +
              B_[B_.index("D829['run_seconds841'] = round("):B_.index(MK842)] + MK842 + "\n" + OFF842)
FINAL842 = r'''
def final841(D):
    V = D.get('verdict842', {}); C = D.get('cost842', {})
    say841('=' * 78); say841('TEST842 BİLİMSEL ÖZET (vaka zincirleri yukarıda "T842|" satırlarında; tam kayıt dosyada)'); say841('=' * 78)
    say841('Durum: %s | kapı: %d, başarısız %d | devam: yeniden kullanılan iş %s' % (D.get('status'), len(D.get('checks', [])),
           sum(not c['pass'] for c in D.get('checks', [])), D.get('resume841', {}).get('reused_jobs')))
    for k_, v_ in V.get('measures', {}).items():
        say841('  %-38s %s' % (k_, json.dumps(v_)))
    say841('-' * 78)
    for k_, v_ in V.get('verdicts', {}).items():
        say841('  %-32s %s' % (k_, v_))
    say841('=' * 78); say841('NİHAİ BİLİMSEL KARAR: %s' % V.get('decision')); say841('  Kural: ' + str(V.get('reason')))
    say841('Maliyet: %s | çalışma %s s | tepe VRAM %.2f GiB' % (C.get('counted'), C.get('run_seconds'), C.get('peak_gpu_gib', 0.0)))
'''
KAP842 = [x for x in T842.body if isinstance(x, ast.Expr) and "'Kapsam:" in ast.unparse(x)]
assert len(KAP842) == 1, 'KAPSAM'
REPL842 = sorted([(node842('PANEL_EXT841'), "PANEL_EXT841 = " + repr(PANEL842)), (node842('HYP841'), "HYP841 = " + repr(HYP842)),
                  (node842('BODY841'), "BODY841 = " + repr(NEWBODY842)), (node842('final841', ast.FunctionDef), FINAL842.strip("\n")),
                  (KAP842[0], "say841('Kapsam: %d görülmemiş dünya, %d iş (%d tasarlanmış durum + %d kapalı döngü: 5 başlangıç x 3 kol) | "
                              "K=%d yankı, döngü bütçesi %d adım' % (WORLDS841, WORLDS841 * 26, WORLDS841 * 11, WORLDS841 * 15, K_ECHO841, T_MAX841))")],
                 key=lambda p: -p[0].lineno)
L842 = S842.splitlines(keepends=True)
for n_, txt_ in REPL842:
    L842[n_.lineno - 1:n_.end_lineno] = [txt_ + "\n"]
S842 = "".join(L842)
ast.parse(S842)
print('TEST842 hücresi: TEST841 kaynağı blob %s doğrulandı; yamalı kaynak %d bayt, SHA-256 %s' %
      (LOCK842[:12], len(S842), hashlib.sha256(S842.encode()).hexdigest()), flush=True)
exec(compile(S842, 'TEST842_CELL', 'exec'), globals())
