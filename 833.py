# AKBASCORE SILICON HIPPOCAMPUS — TEST833, single Colab cell (one A100-SXM4-80GB, frozen Qwen2.5-72B-Instruct NF4).
# NATIVE RECURSIVE TENSOR DYNAMICS: S(t+1) = F_theta(S(t), M, Q) IN THE MODEL'S OWN KV SPACE. A/B/C IN ONE RUN.
# Construction identical to the GPU-completed TEST831/TEST832: the SHA-locked TEST829 source (git blob a5a25460...)
# is fetched, verified, patched at fixed unique anchors and executed. The locked TEST815 engine (native CUT3/H3/KV
# fusion, physical SSD cartridges, SHA/tensor/KV/weight gates) is reused unchanged; the whole physical bank is fused
# natively into one memory M.
# Recurrent state S(t): the 80-layer key/value rows that the frozen model itself writes for the question tokens while
# attending to [M ; S(t-1)]. Keys are RoPE-rephased (locked 709.py rephase) to fixed canonical positions so that every
# step has identical length, positions and mask. S(t-1) enters the next forward ONLY as native attention cache rows:
# no hook, no injection into the residual stream, no text, no generated answer, no regex.
#   A  RESET     : S(t-1) := S_null (question KV computed over the physical NULL card) at every step.
#   B  FEEDBACK  : S(t-1) := F(S(t-2), M, Q), the model's own previous state.
#   C  CAUSAL    : as B, but the fed-back values are rotated by a fixed per-layer/per-head Haar orthogonal matrix:
#                  every value-row norm and every within-head inner product is preserved, keys (attention pattern onto
#                  the state) are untouched, directional information is destroyed.
# Readouts (fixed, identical for A/B/C, label-free): deep attention mass of the final question token on each cartridge
# span, final-norm hidden state, CUT3 state. Stop rule (identical for A/B/C): exact fixed point or end of contraction.
# ARCHITECTURAL STATEMENT: mapping numbers to a terminal decision is still a fixed external readout; TEST833 isolates
# whether the MODEL DYNAMICS (B vs A vs C, same readout) cause better discovery, abstention and stopping.
# No GPU execution or result is claimed by the code author.
import urllib.request, hashlib, ast, json, time, random, math, numpy as np

URL833 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/829.py"
LOCK833 = "a5a25460a3a6bbdf62a0571a9b5ff19e64159cf7"
SEED833 = 8332026
T_MAX833 = 8                  # safety bound on recurrent steps; reaching it without a stop is a SAFETY STOP
DEEP_LAYERS833 = (40, 79)     # predeclared deep layers for the attention readout (subset of the locked probe layers)

with urllib.request.urlopen(urllib.request.Request(URL833, headers={"User-Agent": "AKBASCORE-TEST833"}), timeout=180) as f833:
    raw833 = f833.read(200001)
blob833 = hashlib.sha1(b"blob " + str(len(raw833)).encode() + b"\0" + raw833).hexdigest()
assert len(raw833) <= 200000 and blob833 == LOCK833, ("STOP_SOURCE_CHANGED", blob833)
src833 = raw833.decode("utf-8")

def patch833(text, old, new):
    assert text.count(old) == 1, ("PATCH_ANCHOR_NOT_UNIQUE", old[:80], text.count(old))
    return text.replace(old, new, 1)

src833 = patch833(src833, "SEED829 = 8292026", "SEED829 = %d" % SEED833)
src833 = patch833(src833, "RUN829 = 'TEST829_'", "RUN829 = 'TEST833_'")
for a833, b833 in (("'TEST829_results.json'", "'TEST833_results.json'"), ("'TEST829.log'", "'TEST833.log'"),
                   ("'TEST829_blind_review.csv'", "'TEST833_config_table.csv'"),
                   ("'TEST829_offline_key.json'", "'TEST829_base_offline_key.json'")):
    src833 = patch833(src833, a833, b833)

PANEL_EXT833 = r'''
# ---------------- TEST833 PANEL EXTENSION (sealed before any model call) ----------------
for w in worlds829:
    while True:
        fe = code829()
        if fe not in seen829:
            seen829.add(fe); break
    w['fork_end'] = fe
    w['ids']['mirror'] = 'E829_' + code829()
    w['ids']['fork'] = 'E829_' + code829()
    cards829[w['ids']['mirror']] = ('Evidence record. Domain: ' + w['world'] + '\n' +
                                    'Directed relation: ' + w['end'] + ' -> ' + w['middle'] + '.\n')
    cards829[w['ids']['fork']] = ('Evidence record. Domain: ' + w['world'] + '\n' +
                                  'Directed relation: ' + w['start'] + ' -> ' + fe + '.\n')
    for kind in ('mirror', 'fork'):
        card_meta829[w['ids'][kind]] = {'domain': w['world'], 'kind': kind,
                                        'body_sha256': sha829(cards829[w['ids'][kind]])}
_rng833 = random.Random(SEED829 + 33)
FULLBANK833 = [w['ids'][k] for w in worlds829 for k in ('first', 'second', 'mirror', 'decoy', 'fork')]
RUNS833, RUNKEY833 = [], {}
for wi, w in enumerate(worlds829):
    for cond in ('FULL', 'MISSING_SECOND', 'CONFLICT_ALT_ADDED', 'REPLACE_SECOND_BY_ALT'):
        bank = list(FULLBANK833)
        if cond in ('MISSING_SECOND', 'REPLACE_SECOND_BY_ALT'):
            bank.remove(w['ids']['second'])
        if cond in ('CONFLICT_ALT_ADDED', 'REPLACE_SECOND_BY_ALT'):
            bank.append(w['ids']['changed'])
        _rng833.shuffle(bank)
        tie = list(bank); _rng833.shuffle(tie)
        for order in ('FORWARD', 'REVERSED'):
            mount = list(bank) if order == 'FORWARD' else list(reversed(bank))
            rid = 'R833_' + ''.join(_rng833.choice('0123456789ABCDEF') for _ in range(12))
            RUNS833.append({'run': rid, 'qid': questions829[wi]['qid'], 'mount': mount, 'tie_order': tie})
            RUNKEY833[rid] = {'world': wi, 'condition': cond, 'order': order}
_rng833.shuffle(RUNS833)
'''
src833 = patch833(src833,
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n",
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n" + PANEL_EXT833)

HYP833 = {
    'primary_hypothesis_H833': (
        'Native KV feedback (B) causally improves the fixed label-free readout relative to reset (A) and to '
        'norm-preserving information-destroying feedback (C): B reaches the correct terminal readout (FULL -> SUFFICIENT '
        'with the true first and second links; MISSING_SECOND -> INCOMPLETE; CONFLICT_ALT_ADDED -> CONFLICT including both '
        'continuations; REPLACE_SECOND_BY_ALT -> SUFFICIENT with first link and alternative) in every configuration and both '
        'mount orders by its own stop rule, and every configuration that B gets right but A gets wrong is also wrong under C.'),
    'partial_criterion': 'B correct count strictly greater than both A and C correct counts.',
    'failure_condition': 'Neither criterion holds. A/B/C trajectory differences or stability alone never count as success.',
    'readout': ('deep attention mass (mean of layers 40 and 79, final question token, head-mean) per cartridge span; '
                'largest-log-gap count g over sorted masses: g=1 INCOMPLETE, g=2 SUFFICIENT(top-2), g>=3 CONFLICT(top-g). '
                'The g->decision map encodes the two-hop structure and is identical for A/B/C.'),
    'stop_rule': ('stop at step t if h(t) equals h(t-1) bitwise (FIXED_POINT); or ||h(t)-h(t-1)|| <= 2^-8 ||h(t)|| '
                  '(PRECISION_FIXED_POINT: change below bf16 storage precision, a number-format constant, not a task '
                  'constant); or, for t>=3, ||h(t)-h(t-1)|| >= ||h(t-1)-h(t-2)|| (CONTRACTION_ENDED); otherwise continue to '
                  'T_MAX (SAFETY_T_MAX, reported as a safety stop, not success).'),
    'intervention_C': ('V_l,j <- V_l,j R_l,j with R_l,j Haar-orthogonal (fixed seed) for every layer l and KV head j; '
                       'keys unchanged; ||v R|| = ||v|| and <v_a R, v_b R> = <v_a, v_b> exactly.')}

BODY833 = r'''
D829['test'] = '833'
D829['controller'] = 'NATIVE_KV_RECURRENCE_A_RESET_B_FEEDBACK_C_ROTATED_FEEDBACK_FIXED_READOUT'
D829['source829_blob'] = LOCK833_ID
D829['hypotheses833'] = PANEL829['test833']['hypotheses']
D829['limitations'] = [
    'The terminal decision is a fixed external readout of model numbers (same for A/B/C); the test isolates the contribution of the model dynamics, it does not make the readout model-internal.',
    'The question tokens are re-entered at every step in A, B and C alike (boundary input); no other text enters.',
    'Physical NULL is a neutral one-card memory, not an empty cache.',
    'Three synthetic worlds, four bank conditions, two mount orders; one template, one model.',
    'The g->decision map encodes the two-hop task structure; it is predeclared and condition-independent.',
    'Offline answer readouts use the TEST827 boundary instruction and are produced only after every numerical step is saved.',
    'No GPU execution or result is claimed by the code author.']
gate829('SOURCE829_BLOB', True, LOCK833_ID)
gate829('PANEL_FRESH_SEED', SEED829 == SEED833_ID, SEED829)
gate829('NO_CONTROL_TEXT', MAX_NEW_CONTROL829 == 0)
gate829('RUN_COUNT', len(RUNS833) == 8 * len(questions829), len(RUNS833))
gate829('MOUNT_CARTRIDGES_PHYSICAL', all(c in entries for r in RUNS833 for c in r['mount']))
gate829('MOUNT_EXCLUDES_NULL', all(NULL829 not in r['mount'] for r in RUNS833))
gate829('ENGINE_RECURRENCE_SYMBOLS', all(callable(globals().get(x)) for x in
        ('cache_build', 'pairs', 'rephase', 'Cut3Diagnostic', 'AttentionIntervention', 'prompt_ids', 'build_fusion',
         'memory_seals', 'compare_seals', 'free_generate', 'observe_state')))
gate829('PROBE_LAYERS_INCLUDE_DEEP', all(l in (4, 20, 40, 79) for l in DEEP_LAYERS833_ID))
L833 = {q['qid']: list(prompt_ids(q['question'])) for q in questions829}     # boundary token ids, fixed
maxmem833 = max(P + sum(int(entries[c]['body_tokens']) for c in r['mount']) for r in RUNS833)
maxL833 = max(len(v) for v in L833.values())
gate829('FUSION_TOKENS_WITH_STATE', maxmem833 + 2 * maxL833 + 64 <= MAX_FUSED_TOKENS,
        {'memory': maxmem833, 'question': maxL833, 'max_fused': MAX_FUSED_TOKENS})
try:
    free833, _ = _torch829.cuda.mem_get_info()
    gate829('VRAM_HEADROOM', free833 / 2**30 >= 8.0, round(free833 / 2**30, 2))
except Exception as e833:
    gate829('VRAM_HEADROOM', False, repr(e833))
pred833 = {'configs': len(RUNS833),
           'fusion_forwards_numeric': sum(fusion_forwards829(r['mount']) for r in RUNS833) + len(questions829) * fusion_forwards829([NULL829])
                                      + fusion_forwards829(list(RUNS833[0]['mount'][:2])),
           'fusion_forwards_offline_rebuilds': sum(fusion_forwards829(r['mount']) for r in RUNS833) // 2,
           'probe_forwards_numeric': len(RUNS833) * (2 + 2 * (T_MAX833 - 1)) + len(questions829) + 2,
           'probe_forwards_offline_upper': (len(RUNS833) // 2) * T_MAX833,
           'offline_generation_upper': (len(RUNS833) // 2) * 2 * 16,
           'minutes_estimate': round(((len(RUNS833) * 1.5) * 10 + len(RUNS833) * (2 + 2 * (T_MAX833 - 1)) * 0.5
                                      + (len(RUNS833) // 2) * (10 + 2 * 16 * 0.15)) / 60.0, 1),
           'kv_bytes_per_memory_upper': (maxmem833 + 2 * maxL833) * NL * 2 * KVH * HD * 2}
D829['predicted_cost833'] = pred833
log829('TEST833_PREDICTED_COST', json.dumps(pred833))

D829['noninterference833'] = noninterference829([NULL829], questions829[0]['question'])
for k833, v833 in D829['noninterference833'].items():
    gate829('NONINTERFERENCE_' + k833.upper(), bool(v833), v833)

COUNT833 = {'probe_forwards': 0, 'fusion_forwards': 0, 'mounts': 0}

def spans833(mount, n_state):
    pos = P; sp = {'PREFIX': (0, P)}
    for k, c in enumerate(mount):
        b = int(entries[c]['body_tokens'])
        sp['C%02d' % k] = (pos, pos + b); pos += b
    if n_state:
        sp['STATE'] = (pos, pos + n_state)
    return sp, pos

def concat833(mem, S):
    if S is None:
        return list(mem)
    return [(torch.cat([mk, sk], dim=-2), torch.cat([mv, sv], dim=-2)) for (mk, mv), (sk, sv) in zip(mem, S)]

def rprobe833(mem, S, qids, spans):
    """One native forward of the question over cache [M ; S]. Same call as the locked observe_state (same wrappers,
    positions continue after the cache, all-ones mask), plus: per-span attention records of the final question token,
    the final-norm hidden (observation-only lm_head wrapper) and the model-written KV rows of the question tokens."""
    n = int(mem[0][0].shape[-2]); L = len(qids)
    nS = int(S[0][0].shape[-2]) if S is not None else 0
    start = n + nS
    cache = cache_build(concat833(mem, S))
    pos = torch.arange(start, start + L, device=DEV)
    with torch.no_grad():
        with Cut3Diagnostic() as diag, AttentionIntervention(spans) as probe, Readout829() as ro:
            out = model(input_ids=torch.tensor([qids], device=DEV), past_key_values=cache,
                        attention_mask=torch.ones((1, start + L), device=DEV, dtype=torch.long),
                        position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
        if diag.last is None or probe.calls < 4 or ro.calls != 1:
            raise RuntimeError('RECURRENT_PROBE_NOT_ACTIVE')
        state = diag.last.float().reshape(-1).cpu().numpy().astype(np.float64)
        lp, lp16, summ = full_readout829(ro.h, ro.z)
        hvec = ro.h.reshape(-1).double().cpu().numpy().copy()
        recs = [{'layer': r['layer'], 'masses': dict(r['masses'])} for r in probe.records]
        grown = pairs(out.past_key_values)              # same object the locked initialize_native reads
        if len(grown) != NL or int(grown[0][0].shape[-2]) != start + L:
            raise RuntimeError('CACHE_GROWTH_UNEXPECTED')
        newS = [(k[:, :, start:start + L, :].clone(), v[:, :, start:start + L, :].clone()) for k, v in grown]
    del out, cache, grown, lp, lp16
    COUNT833['probe_forwards'] += 1
    return {'state': state, 'h': hvec, 'summary': summ, 'records': recs, 'S_raw': newS, 'start': start, 'n': n, 'L': L}

def canon833(S_raw, start, n, L):
    # RoPE-consistent relocation of the model-written keys to canonical positions n..n+L-1 (values are position-free).
    old = torch.arange(start, start + L, device=DEV); new = torch.arange(n, n + L, device=DEV)
    return [(rephase(k, old, new), v) for k, v in S_raw]

def sdist833(S1, S2):
    num = 0.0; den = 0.0
    for (k1, v1), (k2, v2) in zip(S1, S2):
        dk = k1.float() - k2.float(); dv = v1.float() - v2.float()
        num += float((dk * dk).sum().item()) + float((dv * dv).sum().item())
        den += float((k2.float() * k2.float()).sum().item()) + float((v2.float() * v2.float()).sum().item())
    return math.sqrt(num / max(den, 1e-300))

# Fixed Haar-orthogonal rotations for C (seeded, predeclared).
rs833 = np.random.default_rng(SEED833_ID + 33)
ROT833 = []
for l833 in range(NL):
    mats = []
    for j833 in range(KVH):
        qm, rm = np.linalg.qr(rs833.standard_normal((HD, HD)))
        mats.append(qm * np.sign(np.diag(rm))[None, :])
    ROT833.append(torch.tensor(np.stack(mats).astype(np.float32), device=DEV))

def rotate833(S):
    out = []
    for l, (k, v) in enumerate(S):
        out.append((k, torch.matmul(v.float(), ROT833[l]).to(v.dtype)))
    return out

def gap_count833(vals):
    v = [max(float(x), 1e-300) for x in vals]
    if len(v) < 3:
        return len(v)
    gaps = [math.log(v[j]) - math.log(v[j + 1]) for j in range(len(v) - 1)]
    return 1 + max(range(len(gaps)), key=lambda j: (gaps[j], -j))

def readout833(recs, mount, tie):
    deep = {}
    for c_idx, c in enumerate(mount):
        key = 'C%02d' % c_idx
        ms = [r['masses'][key] for r in recs if r['layer'] in DEEP_LAYERS833_ID]
        deep[c] = float(np.mean(ms)) if ms else 0.0
    ranked = sorted(mount, key=lambda c: (-deep[c], tie[c]))
    g = gap_count833([deep[c] for c in ranked])
    decision = 'INCOMPLETE' if g == 1 else ('SUFFICIENT' if g == 2 else 'CONFLICT')
    tot = sum(deep.values())
    pnorm = [deep[c] / tot for c in ranked] if tot > 0 else []
    ent = -sum(p * math.log(p) for p in pnorm if p > 0)
    def span_mass(name):
        ms = [r['masses'].get(name, 0.0) for r in recs if r['layer'] in DEEP_LAYERS833_ID]
        return float(np.mean(ms)) if ms else 0.0
    return {'decision': decision, 'gap_count': g, 'top': ranked[:g], 'ranked': ranked[:6],
            'deep_mass': [deep[c] for c in ranked[:6]], 'cartridge_mass_total': tot,
            'state_mass': span_mass('STATE'), 'prefix_mass': span_mass('PREFIX'), 'cartridge_entropy': ent}

# ---- initial states S_null(q): question KV over the physical NULL card (one per question) ----
SNULL833 = {}
for q833 in questions829:
    with contextlib.redirect_stdout(io.StringIO()):
        engine_bindings829('SNULL_' + q833['qid'])
        memN, activeN, _, _ = build_fusion([NULL829], 'TEST833_SNULL_' + q833['qid'], True)
    COUNT833['fusion_forwards'] += fusion_forwards829([NULL829]); COUNT833['mounts'] += 1
    spN, nN = spans833([NULL829], 0)
    pN = rprobe833(memN, None, L833[q833['qid']], spN)
    SNULL833[q833['qid']] = {'S_raw': [(k.clone(), v.clone()) for k, v in pN['S_raw']], 'start': pN['start'], 'L': pN['L']}
    del memN, pN; gc.collect(); release()

# ---- equivalence gate: the recurrent probe without state reproduces the locked observe_state bitwise ----
r0_833 = RUNS833[0]
with contextlib.redirect_stdout(io.StringIO()):
    memE, _, _, _ = build_fusion(list(r0_833['mount'][:2]), 'TEST833_EQUIV', True)
nE = int(memE[0][0].shape[-2]); b0E = int(entries[r0_833['mount'][0]]['body_tokens'])
spE = {'B0': (P, P + b0E), 'B1': (P + b0E, nE)}
with Readout829() as roE:
    stE, _ = observe_state(memE, qtext833_ID[r0_833['qid']], spE)
pE = rprobe833(memE, None, L833[r0_833['qid']], spE)
D829['probe_equivalence833'] = {
    'cut3_state_bitwise': bool(np.array_equal(stE.float().cpu().numpy().astype(np.float64), pE['state'])),
    'final_hidden_bitwise': bool(np.array_equal(roE.h.reshape(-1).double().cpu().numpy(), pE['h']))}
for k833, v833 in D829['probe_equivalence833'].items():
    gate829('RECURRENT_PROBE_EQUALS_OBSERVE_STATE_' + k833.upper(), v833, v833)
COUNT833['fusion_forwards'] += fusion_forwards829(list(r0_833['mount'][:2])); COUNT833['probe_forwards'] += 1
del memE, pE, stE; gc.collect(); release()

# ---- main A/B/C loop over sealed configurations ----
D829['configs833'] = []
t833 = time.perf_counter()
for r833 in RUNS833:
    tc = time.perf_counter()
    mount = list(r833['mount']); tie = {c: i for i, c in enumerate(r833['tie_order'])}; qids = L833[r833['qid']]
    with contextlib.redirect_stdout(io.StringIO()):
        engine_bindings829('MOUNT_' + r833['run'])
        memX833, active, _, _ = build_fusion(mount, 'TEST833_' + r833['run'], True)
    gate829('MEAS_MOUNT_NATIVE_' + r833['run'], len(memX833) == NL and list(active) == mount)
    COUNT833['fusion_forwards'] += fusion_forwards829(mount); COUNT833['mounts'] += 1
    n = int(memX833[0][0].shape[-2]); L = len(qids)
    gate829('MEAS_MOUNT_LENGTH_' + r833['run'], n == P + sum(int(entries[c]['body_tokens']) for c in mount))
    seals = memory_seals(memX833)
    spans, _ = spans833(mount, L)
    sn = SNULL833[r833['qid']]
    S0 = canon833(sn['S_raw'], sn['start'], n, L)          # same initial state for A, B and C
    # round-trip RoPE check on the relocated keys
    back = canon833(S0, n, sn['start'], L)
    rt_err = max(float((a[0].float() - b[0].float()).abs().max().item()) for a, b in zip(back, sn['S_raw']))
    traj = {'A': [], 'B': [], 'C': []}
    # A: reset — every step is the same computation; computed twice to verify bitwise determinism, then reused.
    pA = rprobe833(memX833, S0, qids, spans); pA2 = rprobe833(memX833, S0, qids, spans)
    detA = bool(np.array_equal(pA['h'], pA2['h']) and np.array_equal(pA['state'], pA2['state']))
    gate829('MEAS_A_DETERMINISTIC_' + r833['run'], detA)
    del pA2
    # B and C
    def run_chain(rotate):
        steps = []
        S_prev = S0; S_prev_raw = S0; p_prev = None
        first = pA                                          # step 1 input S0 is identical for all conditions
        for t in range(1, T_MAX833 + 1):
            p = first if t == 1 else rprobe833(memX833, S_prev, qids, spans)
            S_new = canon833(p['S_raw'], p['start'], n, L)
            gate829('MEAS_STATE_SHAPE_' + r833['run'] + '_' + str(t), len(S_new) == NL and
                    tuple(S_new[0][0].shape)[-2] == L and bool(torch.isfinite(S_new[-1][1].float()).all().item()))
            fed = rotate833(S_new) if rotate else S_new
            if rotate:
                vn = [float(v.float().norm().item()) for _, v in S_new[::20]]
                vr = [float(v.float().norm().item()) for _, v in fed[::20]]
                knorm_same = all(bool(torch.equal(a[0], b[0])) for a, b in zip(S_new, fed))
            ro = readout833(p['records'], mount, tie)
            step = {'t': t, 'h_norm': float(np.linalg.norm(p['h'])), 'readout': ro,
                    'entropy_next_token': p['summary']['entropy_nats'], 'top_ids_offline': p['summary']['top_ids'],
                    'd_state_rel': sdist833(S_new, S_prev_raw) if t > 1 else None}
            if rotate:
                step['rotation_value_norm_rel_err'] = max(abs(a - b) / max(a, 1e-30) for a, b in zip(vn, vr))
                step['rotation_keys_unchanged'] = knorm_same
            if p_prev is not None:
                step['d_h'] = float(np.linalg.norm(p['h'] - p_prev['h']))
                step['d_cut3'] = float(np.linalg.norm(p['state'] - p_prev['state']))
            step['dist_to_A_h'] = float(np.linalg.norm(p['h'] - pA['h']))
            steps.append(step)
            if p_prev is not None and p_prev is not first:
                del p_prev['S_raw']
            p_prev = p; S_prev = fed; S_prev_raw = S_new
        return steps, S_prev, p_prev['h']
    stepsB, S_B_last, hB_last = run_chain(False)
    stepsC, S_C_last, hC_last = run_chain(True)
    gate829('KV_SEAL_AFTER_RECURRENCE_' + r833['run'], compare_seals(seals, memory_seals(memX833)))
    def stop_of(steps):
        for i in range(1, len(steps)):
            t = steps[i]['t']
            if steps[i].get('d_h') == 0.0:
                return t - 1, 'FIXED_POINT'
            if steps[i]['d_h'] <= 2.0 ** -8 * steps[i]['h_norm']:
                return t, 'PRECISION_FIXED_POINT'
            if i >= 2 and steps[i]['d_h'] >= steps[i - 1]['d_h']:
                return t - 1, 'CONTRACTION_ENDED'
        return steps[-1]['t'], 'SAFETY_T_MAX'
    rA = readout833(pA['records'], mount, tie)
    stopB, kindB = stop_of(stepsB); stopC, kindC = stop_of(stepsC)
    cfg = {'run': r833['run'], 'qid': r833['qid'], 'mount_size': len(mount), 'memory_tokens': n, 'question_tokens': L,
           'rope_roundtrip_max_abs': rt_err, 'A_deterministic': detA,
           'A': {'stop_step': 1, 'stop_kind': 'RESET_FIXED_BY_CONSTRUCTION', 'readout': rA,
                 'h_norm': float(np.linalg.norm(pA['h']))},
           'B': {'stop_step': stopB, 'stop_kind': kindB, 'readout': stepsB[stopB - 1]['readout'], 'steps': stepsB},
           'C': {'stop_step': stopC, 'stop_kind': kindC, 'readout': stepsC[stopC - 1]['readout'], 'steps': stepsC},
           'B_vs_C_final_hidden_distance': float(np.linalg.norm(hB_last - hC_last)),
           'B_final_vs_A_hidden_distance': float(np.linalg.norm(hB_last - pA['h'])),
           'seconds': None}
    cfg['seconds'] = round(time.perf_counter() - tc, 3)
    D829['configs833'].append(cfg)
    save829()
    log829('TEST833_CONFIG', r833['run'], 'A', rA['decision'], 'B', cfg['B']['readout']['decision'], kindB, stopB,
           'C', cfg['C']['readout']['decision'], kindC, stopC, 's', cfg['seconds'])
    del memX833, pA, stepsB, stepsC, S_B_last, S_C_last, S0, back, hB_last, hC_last
    gc.collect(); release()
D829['numeric_seconds833'] = round(time.perf_counter() - t833, 3)

# ---- integrity gates after all numerical work ----
engine_bindings829('FINAL')
gate829('FROZEN_WEIGHT_SENTINEL', before829 == sentinel())
gate829('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
gate829('LM_HEAD_UNWRAPPED', model.lm_head.__dict__.get('forward') is HEAD_FWD829 and
        not model.lm_head._forward_hooks and not model.lm_head._forward_pre_hooks)
gate829('PANEL_UNCHANGED', sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True)) == PANEL_SHA829)
for cid833 in cards829:
    gate829('FINAL_SHA_' + cid833, sha_file(CART_DIR / entries[cid833]['file']) == entries[cid833]['sha256'])
COUNT_NUMERIC833 = dict(COUNT833)
gate829('COUNTED_NUMERIC_EQUALS_PREDICTED',
        COUNT_NUMERIC833['fusion_forwards'] == pred833['fusion_forwards_numeric'] and
        COUNT_NUMERIC833['probe_forwards'] == pred833['probe_forwards_numeric'],
        {'counted': COUNT_NUMERIC833, 'predicted': {k: pred833[k] for k in ('fusion_forwards_numeric', 'probe_forwards_numeric')}})

# ==========================================================================================================
# OFFLINE PHASE: all numerical trajectories and readouts are saved; labels and text are used only from here.
# ==========================================================================================================
D829['offline_readouts833'] = []
for r833, cfg in zip(RUNS833, D829['configs833']):
    if RUNKEY833[r833['run']]['order'] != 'FORWARD':
        continue                                             # text check on one order only (cost)
    mount = list(r833['mount']); qids = L833[r833['qid']]
    with contextlib.redirect_stdout(io.StringIO()):
        memX833, _, _, _ = build_fusion(mount, 'TEST833_RD_' + r833['run'], True)
    n = int(memX833[0][0].shape[-2]); L = len(qids)
    sn = SNULL833[r833['qid']]; S0 = canon833(sn['S_raw'], sn['start'], n, L)
    # regenerate B's stop state numerically (deterministic) — no text enters this recomputation
    S = S0; p = None
    for t in range(1, cfg['B']['stop_step'] + 1):
        p = rprobe833(memX833, S, qids, spans833(mount, L)[0]); S = canon833(p['S_raw'], p['start'], n, L)
    for cond, state in (('A', S0), ('B', S)):
        o = free_generate(concat833(memX833, state), answer_prompt829(qtext833_ID[r833['qid']]), seed=None, gain=0.,
                          max_new=16, spans=None)
        D829['offline_readouts833'].append({'run': r833['run'], 'condition': cond, 'text': o['raw'].strip(),
                                            'tokens': int(o['generated_tokens'])})
    del memX833, S, S0, p; gc.collect(); release()
save829()

KIND833 = {cid: m['kind'] for cid, m in card_meta829.items()}
DOM833 = {cid: m['domain'] for cid, m in card_meta829.items()}
def role833(cid, w):
    return ('OWN_' if DOM833.get(cid) == w['world'] else 'OTHER_') + str(KIND833.get(cid)).upper()
EXPECT833 = {'FULL': ('SUFFICIENT', ['OWN_FIRST', 'OWN_SECOND']), 'MISSING_SECOND': ('INCOMPLETE', []),
             'CONFLICT_ALT_ADDED': ('CONFLICT', ['OWN_FIRST', 'OWN_SECOND', 'OWN_CHANGED']),
             'REPLACE_SECOND_BY_ALT': ('SUFFICIENT', ['OWN_FIRST', 'OWN_CHANGED'])}
def correct833(ro, cond, w):
    dec, need = EXPECT833[cond]
    roles = [role833(c, w) for c in ro['top']]
    if ro['decision'] != dec:
        return False, roles
    if dec == 'INCOMPLETE':
        return True, roles
    if dec == 'CONFLICT':
        return all(x in roles for x in need), roles
    return sorted(roles) == sorted(need), roles
eval833 = []
for r833, cfg in zip(RUNS833, D829['configs833']):
    key = RUNKEY833[r833['run']]; w = worlds829[key['world']]
    rec = {'run': r833['run'], 'world': key['world'], 'condition': key['condition'], 'order': key['order']}
    for cond in ('A', 'B', 'C'):
        ok, roles = correct833(cfg[cond]['readout'], key['condition'], w)
        rec[cond] = {'decision': cfg[cond]['readout']['decision'], 'top_roles': roles, 'correct': ok,
                     'stop_kind': cfg[cond]['stop_kind'], 'stop_step': cfg[cond]['stop_step'],
                     'ranked_roles': [role833(c, w) for c in cfg[cond]['readout']['ranked']]}
    st = cfg['B']['steps']
    rec['B_step1_top_roles'] = [role833(c, w) for c in st[0]['readout']['top']]
    rec['B_correction'] = (not correct833(st[0]['readout'], key['condition'], w)[0]) and rec['B']['correct']
    rec['B_differs_from_A'] = any((s.get('dist_to_A_h') or 0) > 0 for s in st[1:])
    dh = [s.get('d_h') for s in st if s.get('d_h') is not None]
    ratios = [dh[i] / dh[i - 1] for i in range(1, len(dh)) if dh[i - 1] > 0]
    rec['B_dynamics'] = ('FIXED_POINT' if dh and dh[-1] == 0 else
                         'CONTRACTING' if ratios and all(x < 1 for x in ratios[-2:]) else
                         'EXPANDING' if ratios and all(x > 1 for x in ratios[-2:]) else 'NON_MONOTONE_OR_PERIODIC')
    rec['B_d_h'] = dh; rec['B_contraction_ratios'] = ratios
    rec['C_d_h'] = [s.get('d_h') for s in cfg['C']['steps'] if s.get('d_h') is not None]
    rec['stable_but_wrong_B'] = rec['B_dynamics'] in ('FIXED_POINT', 'CONTRACTING') and not rec['B']['correct']
    rec['state_mass_B_final'] = st[-1]['readout']['state_mass']; rec['state_mass_A'] = cfg['A']['readout']['state_mass']
    for x in D829['offline_readouts833']:
        if x['run'] == r833['run']:
            u = x['text'].upper()
            rec['text_' + x['condition']] = [nm for nm, c in (('END', w['end']), ('MIDDLE', w['middle']), ('ALT_END', w['changed_end']),
                                                              ('FORK_END', w['fork_end'])) if c in u] + (['UNKNOWN'] if 'UNKNOWN' in u else [])
    eval833.append(rec)
D829['offline_eval833'] = eval833

def count833(cond, pred=lambda e, c: e[c]['correct']):
    return sum(1 for e in eval833 if pred(e, cond))
nA, nB, nC = count833('A'), count833('B'), count833('C')
info_causal = all(not e['C']['correct'] for e in eval833 if e['B']['correct'] and not e['A']['correct'])
auto_B = all(e['B']['stop_kind'] in ('FIXED_POINT', 'PRECISION_FIXED_POINT', 'CONTRACTION_ENDED') for e in eval833)
full833 = nB == len(eval833) and auto_B and info_causal
partial833 = nB > nA and nB > nC
order_consistent = {c: sum(1 for w in range(len(worlds829)) for cond in EXPECT833
                           if len({e[c]['decision'] for e in eval833 if e['world'] == w and e['condition'] == cond}) == 1)
                    for c in ('A', 'B', 'C')}
def auc833(pos, neg):
    if not pos or not neg:
        return None
    return sum((a > b) + 0.5 * (a == b) for a in pos for b in neg) / (len(pos) * len(neg))
sep833 = {}
for cond in ('A', 'B'):
    comp = [e for e, cfg in zip(eval833, D829['configs833']) if e['condition'] in ('FULL', 'REPLACE_SECOND_BY_ALT')]
    miss = [e for e in eval833 if e['condition'] == 'MISSING_SECOND']
    def feat(e, f):
        cfg = next(c for c in D829['configs833'] if c['run'] == e['run'])
        ro = cfg[cond]['readout']
        return {'top2_mass_share': (sum(ro['deep_mass'][:2]) / max(ro['cartridge_mass_total'], 1e-300)),
                'gap_count': ro['gap_count'], 'cartridge_entropy': ro['cartridge_entropy']}[f]
    sep833[cond] = {f: auc833([feat(e, f) for e in comp], [feat(e, f) for e in miss])
                    for f in ('top2_mass_share', 'gap_count', 'cartridge_entropy')}
D829['report833'] = {
    'correct_terminal_readouts': {'A': [nA, len(eval833)], 'B': [nB, len(eval833)], 'C': [nC, len(eval833)]},
    'first_link_in_top_B': sum('OWN_FIRST' in e['B']['top_roles'] for e in eval833),
    'first_link_in_top_A': sum('OWN_FIRST' in e['A']['top_roles'] for e in eval833),
    'second_or_alt_in_top_B': sum(any(x in e['B']['top_roles'] for x in ('OWN_SECOND', 'OWN_CHANGED')) for e in eval833),
    'second_or_alt_in_top_A': sum(any(x in e['A']['top_roles'] for x in ('OWN_SECOND', 'OWN_CHANGED')) for e in eval833),
    'B_trajectory_differs_from_A': sum(e['B_differs_from_A'] for e in eval833),
    'B_corrections_after_wrong_step1': sum(e['B_correction'] for e in eval833),
    'incomplete_recognised': {c: sum(e[c]['decision'] == 'INCOMPLETE' for e in eval833 if e['condition'] == 'MISSING_SECOND')
                              for c in ('A', 'B', 'C')},
    'misleading_completion_rejected': {c: sum(not any(x in e[c]['top_roles'] for x in ('OWN_MIRROR', 'OWN_FORK', 'OWN_DECOY'))
                                              for e in eval833 if e['condition'] == 'MISSING_SECOND') for c in ('A', 'B', 'C')},
    'conflict_recognised': {c: sum(e[c]['correct'] for e in eval833 if e['condition'] == 'CONFLICT_ALT_ADDED') for c in ('A', 'B', 'C')},
    'false_positives': {c: {'sufficient_or_conflict_on_missing': sum(e[c]['decision'] != 'INCOMPLETE' for e in eval833
                                                                     if e['condition'] == 'MISSING_SECOND'),
                            'wrong_pair_when_sufficient': sum(e[c]['decision'] == 'SUFFICIENT' and not e[c]['correct'] for e in eval833)}
                        for c in ('A', 'B', 'C')},
    'B_dynamics_classes': {k: sum(e['B_dynamics'] == k for e in eval833) for k in ('FIXED_POINT', 'CONTRACTING', 'EXPANDING', 'NON_MONOTONE_OR_PERIODIC')},
    'stable_but_wrong_B': sum(e['stable_but_wrong_B'] for e in eval833),
    'stop_kinds': {c: {k: sum(e[c]['stop_kind'] == k for e in eval833) for k in
                       ('FIXED_POINT', 'PRECISION_FIXED_POINT', 'CONTRACTION_ENDED', 'SAFETY_T_MAX', 'RESET_FIXED_BY_CONSTRUCTION')} for c in ('A', 'B', 'C')},
    'stop_depends_on_sufficiency_B': {'mean_stop_step_complete': float(np.mean([e['B']['stop_step'] for e in eval833 if e['condition'] in ('FULL', 'REPLACE_SECOND_BY_ALT')])),
                                      'mean_stop_step_missing': float(np.mean([e['B']['stop_step'] for e in eval833 if e['condition'] == 'MISSING_SECOND']))},
    'order_consistent_world_conditions': order_consistent,
    'B_information_causal_vs_C': info_causal,
    'offline_separability_auc_complete_vs_missing': sep833,
    'feedback_integrity': {'rope_roundtrip_max_abs': max(c['rope_roundtrip_max_abs'] for c in D829['configs833']),
                           'A_deterministic_all': all(c['A_deterministic'] for c in D829['configs833']),
                           'probe_equivalence': D829['probe_equivalence833'],
                           'rotation_value_norm_rel_err_max': max(s.get('rotation_value_norm_rel_err', 0.0) for c in D829['configs833'] for s in c['C']['steps']),
                           'rotation_keys_unchanged_all': all(s.get('rotation_keys_unchanged', True) for c in D829['configs833'] for s in c['C']['steps'])}}
verdict833 = ('FULL_PASS' if full833 else 'PARTIAL_PASS_B_BETTER_THAN_A_AND_C' if partial833 else 'FAIL')
D829['verdict833'] = {
    'question': 'Does a native recursive numerical state of the frozen model causally improve discovery, abstention and stopping?',
    'verdict': verdict833, 'B_correct': nB, 'A_correct': nA, 'C_correct': nC, 'configs': len(eval833),
    'B_autonomous_stops_all': auto_B, 'information_causal': info_causal,
    'interpretation_guard': ('A/B/C trajectory differences and stability are reported separately and never count as '
                             'success; decisions come from a fixed external readout identical across conditions.')}
D829['cost833'] = {'counted_numeric': COUNT_NUMERIC833, 'counted_total_including_offline': dict(COUNT833),
                   'predicted': pred833, 'numeric_seconds': D829['numeric_seconds833'],
                   'offline_generated_tokens': sum(x['tokens'] for x in D829['offline_readouts833']),
                   'peak_gpu_gib': max([v.get('peak_gpu_gib', 0.0) for v in COST829.values()] or [0.0])}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f833:
    wr833 = csv.DictWriter(f833, fieldnames=['world', 'condition', 'order', 'A', 'B', 'C', 'B_dynamics', 'B_stop', 'text_A', 'text_B'])
    wr833.writeheader()
    for e in eval833:
        wr833.writerow({'world': e['world'], 'condition': e['condition'], 'order': e['order'],
                        'A': e['A']['decision'] + ':' + ' '.join(e['A']['top_roles']),
                        'B': e['B']['decision'] + ':' + ' '.join(e['B']['top_roles']),
                        'C': e['C']['decision'] + ':' + ' '.join(e['C']['top_roles']),
                        'B_dynamics': e['B_dynamics'], 'B_stop': e['B']['stop_kind'] + '@' + str(e['B']['stop_step']),
                        'text_A': ' '.join(e.get('text_A', [])), 'text_B': ' '.join(e.get('text_B', []))})
D829['status'] = 'COMPLETE_A_B_C_RECURRENCE_EVALUATED'
save829()
log829('TEST833_EVAL', json.dumps([{k: (e[k] if k in ('world', 'condition', 'order', 'B_dynamics') else
                                        {kk: e[k][kk] for kk in ('decision', 'top_roles', 'correct', 'stop_kind', 'stop_step')})
                                    for k in ('world', 'condition', 'order', 'A', 'B', 'C', 'B_dynamics')} for e in eval833]))
log829('TEST833_DYNAMICS', json.dumps([{'w': e['world'], 'c': e['condition'], 'o': e['order'], 'B_d_h': e['B_d_h'],
                                        'C_d_h': e['C_d_h'], 'B_step1_top': e['B_step1_top_roles'],
                                        'state_mass_A': e['state_mass_A'], 'state_mass_B': e['state_mass_B_final']} for e in eval833]))
log829('TEST833_REPORT', json.dumps(D829['report833']))
log829('TEST833_COST', json.dumps(D829['cost833']))
log829('TEST833_VERDICT', json.dumps(D829['verdict833']))
log829('TEST833_COMPLETED', str(OUT829))
'''
BODY_SHA833 = hashlib.sha256(BODY833.encode()).hexdigest()
PANEL_HOOK833 = ("PANEL829['test833'] = {'runs': RUNS833, 'hypotheses': %r, 'body_sha256': %r, 't_max': %d, "
                 "'deep_layers': %r, 'seed': SEED829}\n" % (HYP833, BODY_SHA833, T_MAX833, list(DEEP_LAYERS833)))
src833 = patch833(src833, "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))",
                  PANEL_HOOK833 + "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))")
OFFLINE_HOOK833 = r'''
OFFLINE833 = DIR829 / 'TEST833_offline_key.json'   # never read by any runtime computation
OFFLINE833.write_text(json.dumps({'note': 'OFFLINE ONLY — configuration conditions and card kinds', 'runs': RUNKEY833,
                                  'worlds': worlds829, 'questions': questions829, 'card_meta': card_meta829},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D829['offline_key833_sha256'] = sha829(OFFLINE833.read_bytes())
'''
src833 = patch833(src833, "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n",
                  "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n" + OFFLINE_HOOK833)
start833 = src833.index("    # RUN ORDER: integrity checks")
start833 = src833.rfind("    # ---", 0, start833)
end833 = src833.index("except BaseException as e:\n    D829['status'] = 'ERROR'", start833)
body833 = (BODY833.replace("LOCK833_ID", repr(LOCK833)).replace("SEED833_ID", str(SEED833))
           .replace("DEEP_LAYERS833_ID", repr(tuple(DEEP_LAYERS833)))
           .replace("qtext833_ID", "{q['qid']: q['question'] for q in questions829}"))
replacement833 = "\n".join("    " + line if line else "" for line in body833.strip("\n").splitlines()) + "\n"
patched833 = src833[:start833] + replacement833 + src833[end833:]
ast.parse(patched833)
print('TEST833_SOURCE_LOCK_VERIFIED', LOCK833)
print('TEST833_BODY_SHA256', BODY_SHA833)
print('TEST833_PATCHED_SOURCE_AST_PASS', len(patched833), hashlib.sha256(patched833.encode()).hexdigest())
exec(compile(patched833, 'TEST833_LOCKED_ENGINE', 'exec'), globals())
