# AKBASCORE SILICON HIPPOCAMPUS — TEST834, single Colab cell (one A100-SXM4-80GB, frozen Qwen2.5-72B-Instruct NF4).
# NATIVE MEMORY ADDRESSING (MAM v1.3.0 PEAK50, rebuilt on 72B H3) + NATIVE ATTENTION RE-ADDRESSING + TEST833 KV RECURRENCE.
# Construction identical to the GPU-completed TEST831/832/833: the SHA-locked TEST829 source (git blob a5a25460...) is
# fetched, verified, patched at fixed unique anchors and executed. The locked TEST815 engine (native CUT3/H3/KV fusion,
# physical SSD cartridges, SHA/tensor/KV/weight gates) is reused unchanged.
#
# ARCHITECTURE (every transition explicit; roles labelled):
#   Q -> frozen model -> layer-3 (CUT3) question rows                                   [NATIVE representation]
#     -> MAM v1.3.0 address: store-mean centring, unit norm, PCA128 candidate stage
#        (exact inner-product search replaces FAISS IVF), top2 log-mean-exp, budget 16, PEAK50 [EXTERNAL fixed retrieval
#        rule transferred as an algorithm; 72B tensors only]
#     -> verified physical cartridge -> native CUT3/KV fusion                           [LOCKED ENGINE]
#     -> question forward over [M ; S(t-1)] (TEST833 recurrence)                        [NATIVE computation]
#     -> attention row of ONE pre-calibrated head (final question token) x stored native rows of the mounted
#        evidence = pointer vector in the same address space                            [NATIVE weights, fixed linear readout]
#     -> same MAM address rule over not-yet-mounted cartridges = next address            [EXTERNAL fixed retrieval rule]
#     -> candidate mounted; accepted iff the same head puts more attention on it than on every mounted card
#                                                                                       [EXTERNAL_UPTAKE_INTERFACE]
#     -> stop when no candidate is taken up (NO_UPTAKE), no address exists, or the safety bound is reached.
# The uptake comparison and the stop are Python comparisons of native numbers: they are an EXTERNAL CONTROLLER INTERFACE,
# never described as model-internal cognition. No evidence count, no answer, no role and no condition label enters it.
# Native declarations of SUFFICIENCY, CONTRADICTION and ABSTENTION do not exist in this architecture: they are reported
# as UNIMPLEMENTED; their native-signal question is tested offline (calibrated on separate worlds, applied to sealed ones).
# No GPU execution or result is claimed by the code author.
import urllib.request, hashlib, ast, json, time, random, math, numpy as np

URL834 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/829.py"
LOCK834 = "a5a25460a3a6bbdf62a0571a9b5ff19e64159cf7"
SEED834 = 8342026
EXPECTED_ARCH834 = (80, 8192, 64, 8, 128)   # (NL, H, QH, KVH, HD) Qwen2.5-72B-Instruct, as locked in 779.py
DEVICE_KIND834 = 'cuda'
WORLDS_EVAL834 = 6            # sealed evaluation worlds (two banks of three worlds)
CAL_WORLDS834 = 12            # separate calibration worlds (four banks of three worlds), used only to lock one head
BLOCK834 = 3                  # worlds per physical bank
CONDS834 = ('FULL', 'OWN_ONLY', 'MISSING_FIRST', 'MISSING_SECOND', 'REPLACE_SECOND_BY_ALT', 'CONFLICT_ALT_ADDED')
SPACES834 = ('H3', 'L2V')     # stored native row spaces: CUT3 hidden rows; layer-2 value rows (TEST524 pointer space)
BETA834 = 8.0                 # MAM locked beta
PEAK_A834 = 0.5               # MAM locked PEAK50 weight (TEST627 lock: ('PEAK50', .5, 0.))
PCA_RANK834 = 128             # MAM PCA128
TOKEN_K834 = 16               # MAM token_k
BUDGET834 = 16                # MAM candidate budget
B_TRY834 = 2                  # address candidates tried per step (search budget; MAM TOP2 convention); safety-type constant
T_ACCEPT_MAX834 = 4           # safety bound on accepted memories (= locked MAX_STEPS829 = 4); reaching it is a SAFETY stop
T_MAX_C834 = 8                # TEST833 recurrence safety bound for condition C
DEEP_LAYERS834 = (40, 79)     # TEST833 legacy readout layers (control only)
MAX_NEW_TEXT834 = 10          # offline answer readout tokens
SEC_FUSION834 = 0.6           # cost model: seconds per short fusion forward (TEST833: 754 forwards in 560.4 s)
SEC_PROBE834 = 0.9            # cost model: seconds per probe forward incl. fp64 readout and per-head transfer
PRED_LIMIT_MIN834 = 240.0     # predicted numeric+offline minutes must not exceed this, else STOP before the model loads
HARD_BUDGET_MIN834 = 300.0    # wall-clock guard on numeric work; exceeding it stops safely (verdict INCONCLUSIVE)

with urllib.request.urlopen(urllib.request.Request(URL834, headers={"User-Agent": "AKBASCORE-TEST834"}), timeout=180) as f834:
    raw834 = f834.read(200001)
blob834 = hashlib.sha1(b"blob " + str(len(raw834)).encode() + b"\0" + raw834).hexdigest()
assert len(raw834) <= 200000 and blob834 == LOCK834, ("STOP_SOURCE_CHANGED", blob834)
src834 = raw834.decode("utf-8")

def patch834(text, old, new):
    assert text.count(old) == 1, ("PATCH_ANCHOR_NOT_UNIQUE", old[:80], text.count(old))
    return text.replace(old, new, 1)

src834 = patch834(src834, "SEED829 = 8292026", "SEED829 = %d" % SEED834)
src834 = patch834(src834, "RUN829 = 'TEST829_'", "RUN829 = 'TEST834_'")
src834 = patch834(src834, "WORLDS829 = 3                    # small pilot (directive); no automatic extension",
                  "WORLDS829 = %d                    # TEST834 sealed evaluation worlds" % WORLDS_EVAL834)
for a834, b834 in (("'TEST829_results.json'", "'TEST834_results.json'"), ("'TEST829.log'", "'TEST834.log'"),
                   ("'TEST829_blind_review.csv'", "'TEST834_run_table.csv'"),
                   ("'TEST829_offline_key.json'", "'TEST829_base_offline_key.json'")):
    src834 = patch834(src834, a834, b834)

# ------------------------------------------------------------------------------------------------------------------
# PANEL EXTENSION (module level, executed before any model call; sealed into PANEL829 and its SHA)
# ------------------------------------------------------------------------------------------------------------------
PANEL_EXT834 = r'''
# ---------------- TEST834 PANEL EXTENSION (sealed before any model call) ----------------
for w in worlds829:
    while True:
        fe = code829()
        if fe not in seen829:
            seen829.add(fe); break
    w['fork_end'] = fe
    for kind in ('mirror', 'fork'):
        cid = 'E829_' + code829()
        assert cid not in cards829, 'CARD_ID_COLLISION'
        w['ids'][kind] = cid
    cards829[w['ids']['mirror']] = ('Evidence record. Domain: ' + w['world'] + '\n' +
                                    'Directed relation: ' + w['end'] + ' -> ' + w['middle'] + '.\n')
    cards829[w['ids']['fork']] = ('Evidence record. Domain: ' + w['world'] + '\n' +
                                  'Directed relation: ' + w['start'] + ' -> ' + fe + '.\n')
    for kind in ('mirror', 'fork'):
        card_meta829[w['ids'][kind]] = {'domain': w['world'], 'kind': kind,
                                        'body_sha256': sha829(cards829[w['ids'][kind]])}
for cid in list(card_meta829):
    card_meta829[cid]['split'] = 'null' if cid == NULL829 else 'evaluation'
EVALSTORE834 = sorted(c for c in cards829 if c != NULL829)
# Calibration worlds: separate generator stream, disjoint names and IDs, identical templates. Used ONLY before the
# first evaluation forward, ONLY to lock one attention head (and to fit an offline-only sufficiency stump).
RNGC834 = random.Random(SEED829 + 834001)
def codec834():
    while True:
        c = ''.join(RNGC834.choice(ALPH829) for _ in range(9))
        if c not in seen829:
            seen829.add(c); return c
CALW834 = []
for ci834 in range(CAL_WORLDS834):
    cw = {'world': 'DOMAIN_' + codec834(), 'start': codec834(), 'middle': codec834(), 'end': codec834(),
          'decoy_end': codec834(), 'fork_end': codec834()}
    cw['ids'] = {}
    rel = (('first', cw['start'], cw['middle']), ('second', cw['middle'], cw['end']), ('mirror', cw['end'], cw['middle']),
           ('decoy', cw['decoy_end'], cw['start']), ('fork', cw['start'], cw['fork_end']))
    for kind, a, b in rel:
        cid = 'E829_' + codec834()
        assert cid not in cards829, 'CARD_ID_COLLISION'
        cw['ids'][kind] = cid
        cards829[cid] = 'Evidence record. Domain: ' + cw['world'] + '\n' + 'Directed relation: ' + a + ' -> ' + b + '.\n'
        card_meta829[cid] = {'domain': cw['world'], 'kind': kind, 'body_sha256': sha829(cards829[cid]), 'split': 'calibration'}
    cw['qid'] = cw['world'] + '_P0'
    cw['question'] = ('In domain {world}, starting from {start}, which endpoint is reached after exactly two directed '
                      'links?').format(**cw)
    CALW834.append(cw)
CALSTORE834 = sorted(c for cw in CALW834 for c in cw['ids'].values())
_rngc834 = random.Random(SEED829 + 834002)
CALJOBS834 = []
for bi in range(0, len(CALW834), BLOCK834):
    blk = CALW834[bi:bi + BLOCK834]
    cbank = [cw['ids'][k] for cw in blk for k in ('first', 'second', 'mirror', 'decoy', 'fork')]
    for j, cw in enumerate(blk):
        b_ = list(cbank); _rngc834.shuffle(b_)
        CALJOBS834.append({'qid': cw['qid'], 'question': cw['question'], 'bank': b_, 'first': cw['ids']['first'],
                           'second': cw['ids']['second'], 'mirror': cw['ids']['mirror'],
                           'other': blk[(j + 1) % len(blk)]['ids']['second']})
# Sealed evaluation runs: world x bank condition; opaque IDs; condition labels live only in the offline key.
_rng834 = random.Random(SEED829 + 34)
RUNS834, RUNKEY834 = [], {}
assert len(questions829) == len(worlds829), 'ONE_QUESTION_PER_WORLD'
for bi in range(0, len(worlds829), BLOCK834):
    blk = worlds829[bi:bi + BLOCK834]
    fullbank = [w['ids'][k] for w in blk for k in ('first', 'second', 'mirror', 'decoy', 'fork')]
    for w in blk:
        wi = worlds829.index(w)
        own = [w['ids'][k] for k in ('first', 'second', 'mirror', 'decoy', 'fork')]
        for cond in CONDS834:
            bank = list(own) if cond == 'OWN_ONLY' else list(fullbank)
            if cond == 'MISSING_FIRST':
                bank.remove(w['ids']['first'])
            if cond in ('MISSING_SECOND', 'REPLACE_SECOND_BY_ALT'):
                bank.remove(w['ids']['second'])
            if cond in ('CONFLICT_ALT_ADDED', 'REPLACE_SECOND_BY_ALT'):
                bank.append(w['ids']['changed'])
            _rng834.shuffle(bank)
            tie = list(bank); _rng834.shuffle(tie)
            rid = 'R834_' + ''.join(_rng834.choice('0123456789ABCDEF') for _ in range(12))
            RUNS834.append({'run': rid, 'qid': questions829[wi]['qid'], 'bank': bank, 'tie_order': tie})
            RUNKEY834[rid] = {'world': wi, 'block': bi // BLOCK834, 'condition': cond}
_rng834.shuffle(RUNS834)

def fus_upper834(k, maxb, p_):
    # Upper bound on locked build_fusion forwards for k cartridges (first carries the P-token prefix).
    if k <= 0:
        return 0
    c = int(globals().get('CHUNK', 128))
    return (p_ + maxb + c - 1) // c + (k - 1) * ((maxb + c - 1) // c)

def cost_upper834(tok_of, p_):
    """Upper bounds on every model forward of TEST834 (adaptive loops bounded by the safety constants)."""
    up = {'fusion_forwards': 0, 'probe_forwards': 0, 'capture_forwards': 0, 'rank_forwards': 0, 'generation_forwards': 0}
    maxall = max(tok_of[c] for c in cards829)
    up['fusion_forwards'] += fus_upper834(1, tok_of[NULL829], p_)                       # NULL mount (S_null)
    up['probe_forwards'] += len(questions829) + len(CALJOBS834)                          # S_null per question
    up['fusion_forwards'] += fus_upper834(2, maxall, p_); up['probe_forwards'] += 2      # equivalence gate
    up['fusion_forwards'] += fus_upper834(1, tok_of[NULL829], p_); up['probe_forwards'] += 3; up['generation_forwards'] += 1
    up['capture_forwards'] += len(questions829) + len(CALJOBS834)                        # hop-1 question rows
    up['rank_forwards'] += len(questions829)                                             # 815 numeric_rank control
    for j in CALJOBS834:
        mb = max(tok_of[c] for c in j['bank'])
        up['fusion_forwards'] += fus_upper834(1, mb, p_) + 3 * fus_upper834(2, mb, p_); up['probe_forwards'] += 4
    for r in RUNS834:
        mb = max(tok_of[c] for c in r['bank']); nb = len(r['bank'])
        up['fusion_forwards'] += 2 * fus_upper834(nb, mb, p_); up['probe_forwards'] += 2              # A FWD/REV
        up['fusion_forwards'] += fus_upper834(1, mb, p_); up['probe_forwards'] += 2                   # step 1 + determinism
        up['probe_forwards'] += T_MAX_C834 - 1                                                        # C chain
        for k in range(1, T_ACCEPT_MAX834):                                                           # B, D, E loops
            up['fusion_forwards'] += 3 * B_TRY834 * fus_upper834(k + 1, mb, p_); up['probe_forwards'] += 3 * B_TRY834
        up['fusion_forwards'] += fus_upper834(2, mb, p_); up['probe_forwards'] += 1                   # TOP2 static
        up['fusion_forwards'] += 2 * fus_upper834(T_ACCEPT_MAX834, mb, p_); up['probe_forwards'] += 2 # D final FWD/REV
        up['fusion_forwards'] += T_ACCEPT_MAX834 * fus_upper834(T_ACCEPT_MAX834 - 1, mb, p_)          # LOO
        up['probe_forwards'] += T_ACCEPT_MAX834
    numeric = dict(up)
    off_f = 0; off_g = 0
    for r in RUNS834:
        mb = max(tok_of[c] for c in r['bank'])
        off_f += fus_upper834(len(r['bank']), mb, p_) + 4 * fus_upper834(T_ACCEPT_MAX834, mb, p_)
        off_g += 5 * MAX_NEW_TEXT834
    off_f += len(questions829) * fus_upper834(1, tok_of[NULL829], p_); off_g += len(questions829) * MAX_NEW_TEXT834
    sec = ((numeric['fusion_forwards'] + off_f) * SEC_FUSION834 +
           (numeric['probe_forwards'] + numeric['capture_forwards'] + numeric['rank_forwards']) * SEC_PROBE834 +
           (numeric['generation_forwards'] + off_g) * SEC_FUSION834 + 120.0 + len(cards829) * 2.0)
    maxmem = max(p_ + sum(tok_of[c] for c in r['bank']) for r in RUNS834)
    maxq = max(len(q['question']) for q in questions829)
    per_card = lambda b: (p_ + b) * (int(globals().get('H', 8192)) * 2 + 4 * 2 * 8 * 128 * 2)
    return {'numeric_upper': numeric, 'offline_upper': {'fusion_forwards': off_f, 'generation_forwards': off_g},
            'physical_cartridges': len(cards829),
            'cartridge_disk_mb_estimate': round(sum(per_card(tok_of[c]) for c in cards829) / 2**20, 1),
            'max_memory_tokens': maxmem,
            'kv_bytes_largest_memory_upper': (maxmem + 2 * 64) * 80 * 2 * 8 * 128 * 2,
            'recurrent_steps_upper': {'C_per_run': T_MAX_C834, 'accepted_per_loop': T_ACCEPT_MAX834,
                                      'tries_per_step': B_TRY834},
            'minutes_upper_excluding_model_load': round(sec / 60.0, 1),
            'peak_vram_gib_expected': 'about 39-41 (TEST833 measured 38.92 GiB with a 16-card memory; largest TEST834 memory is similar)',
            'model_weights': 'loaded once (same NF4 path as TEST829-833); download/cache time not estimated',
            'max_question_chars': maxq}
'''
src834 = patch834(src834,
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n",
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n" + PANEL_EXT834)

# Cost estimate printed and budget-gated BEFORE the 72B weights are loaded (tokenizer-only token counts).
PRECOST834 = r'''
    PRE834 = cost_upper834(tok_counts829, 30)
    D829['predicted_cost834_pre_model'] = PRE834
    log829('TEST834_PREDICTED_COST_BEFORE_MODEL_LOAD', json.dumps(PRE834))
    gate829('TEST834_PREDICTED_BUDGET', PRE834['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN834,
            {'minutes_upper': PRE834['minutes_upper_excluding_model_load'], 'limit': PRED_LIMIT_MIN834})
'''
src834 = patch834(src834, "    del tok829\n", "    del tok829\n" + PRECOST834)

HYP834 = {
    'central_hypothesis_H834': (
        'With MAM PEAK50 addressing rebuilt on 72B CUT3 rows and native attention re-addressing, recurrent KV feedback (D) '
        'ends in the correct evidence state (FULL/OWN_ONLY: K supports exactly the true endpoint; REPLACE: exactly the '
        'alternative endpoint; CONFLICT: both endpoints; MISSING_FIRST/MISSING_SECOND: no endpoint) by a non-safety stop, '
        'more often than addressing without recurrence (B), recurrence without re-addressing (C) and static MAM TOP2, '
        'and the advantage is destroyed by norm-preserving value rotation (E).'),
    'evidence_state_definition': ('endpoints(K) = nodes reachable from the question start by exactly two directed relations '
                                  'contained in the final mounted set K (computed OFFLINE from the sealed key).'),
    'criteria': {
        'C1_BLIND_FIRST_DISCOVERY': 'hop-1 PEAK50 top-1 is the own first link in >= 20 of the 30 runs whose bank contains it.',
        'C2_MULTI_MEMORY_SELECTION': 'D final K contains every required link in >= 18 of 24 complete-evidence runs.',
        'C3_CAUSAL_DEPENDENCE': ('in >= 80% of evaluable D runs (all required links in K, |K|>=2; >=6 evaluable) removing each '
                                 'required link moves the final hidden (cosine distance) more than removing any other member '
                                 'and more than reversing the mount order; < 6 evaluable -> INCONCLUSIVE.'),
        'C4_CORRECTION': ('among first-present runs whose hop-1 top-1 is not the own first link (>= 3 needed, else '
                          'INCONCLUSIVE), D ends in a correct evidence state containing the first link in >= 50%.'),
        'C5_ABSTENTION_MISSING': ('in >= 10 of 12 missing-evidence runs D ends with no supported endpoint, by a non-safety stop, '
                                  'having accepted no continuation after the hop-1 card (|K| = 1: nothing that exists continues '
                                  'the chain, so any uptake is a false continuation).'),
        'C6_CONTRADICTION': ('native contradiction declaration: UNIMPLEMENTED (never counted as success). Reported: K supports '
                             'both endpoints in CONFLICT runs (>= 5 of 6 = evidence available).'),
        'C7_ROBUSTNESS': ('(a) D correct in >= 4/6 FULL runs and FULL correct >= OWN_ONLY correct - 1; (b) the head-argmax card '
                          'of the final K forward is identical after mount-order reversal in >= 80% of D runs with |K|>=2 '
                          '(>= 6 evaluable, else INCONCLUSIVE).'),
        'C8_RECURRENCE_IMPROVEMENT': ('D correct >= max(B, C, TOP2) correct + 3; E correct <= D correct - 3; among runs with D '
                                      'correct and B wrong (>= 3 needed) E is wrong in >= 50%.'),
        'C9_STOPPING': ('(a) no SAFETY stop among D-correct runs; (b) in >= 5 of 6 worlds |K_D(FULL)| > |K_D(MISSING_SECOND)|. '
                        'The stop itself is the EXTERNAL_UPTAKE_INTERFACE; a native stop declaration is UNIMPLEMENTED.')},
    'verdict_rule': ('PASS iff C1, C2, C3, C5, C7, C8, C9 PASS and C4 PASS or INCONCLUSIVE. FAIL iff C8 fails or D correct < 12 '
                     'of 36. Otherwise INCONCLUSIVE. A budget stop forces INCONCLUSIVE. UNIMPLEMENTED capabilities are never '
                     'counted as successes.'),
    'sufficiency_signal_test': ('OFFLINE ONLY. Four predeclared native features of a terminal forward (S_null state): '
                                'next-token entropy, locked-head attention mass on evidence cards, locked-head pointer best '
                                'PEAK50 score over unmounted cards, final-hidden cosine distance to the NULL-memory forward. '
                                'A one-feature stump is fitted on CALIBRATION mounts ([first] = incomplete, [first, second] = '
                                'complete), the feature chosen on calibration, then applied unchanged to sealed D terminal '
                                'forwards. Balanced accuracy >= 0.80 (>= 4 per class) = SIGNAL_TRANSFERS (an EXTERNAL '
                                'calibrated readout, not native cognition).'),
    'head_calibration': ('calibration worlds only. For each (space, layer, head): +1 if the pointer from [first] addresses the '
                         'second link first among unmounted cards; +1 if [first, second] puts more mass on second than first; '
                         '+1 if [first, mirror] puts less on mirror; +1 if [first, other-world second] puts less on it. '
                         'argmax total; ties: mean address margin, then space order, layer, head.'),
    'uptake_rule': ('EXTERNAL_UPTAKE_INTERFACE: candidate c appended to K is accepted iff the locked head (final question '
                    'token) puts strictly more attention mass on c than on every card already in K.'),
    'controls': {'A': 'frozen full-bank mount, no addressing, no recurrence (S_null), both mount orders',
                 'TOP2': 'static MAM PEAK50 top-2 mount (count fixed by construction; control only)',
                 'B': 'adaptive addressing loop, S reset to S_null at every forward',
                 'C': 'hop-1 card only, TEST833 recurrence for up to 8 steps, pointer addresses recorded but never executed',
                 'D': 'adaptive addressing loop with TEST833 KV feedback',
                 'E': 'D with every fed-back value rotated by fixed Haar-orthogonal matrices (keys unchanged)',
                 'LEGACY833': 'TEST833 gap-count attention rule on A (the rule the directive forbids as a central claim)',
                 'RANK815': 'locked 815 numeric_rank hop-1 control'}}

CLAIMS834 = {
    'verified_from_prior_research': [
        'MAM addressing source (titan-cognitive-core-v2 610.py blob 4a92e751, 624.py blob ba987d6f, 626.py blob 86ccdbcc, '
        '627.py blob 483477eb): layer-3 residual rows of the fact span after a fixed PREFIX; question_rep = PREFIX + question '
        'at the same local positions; transform_fit(rank=0) = store-mean centring, apply = centre + unit norm; PCA128 = '
        'torch.pca_lowrank of store token rows; FAISS IndexIVFFlat(IP, nlist 128), nprobe 2, token_k 16; touched cartridges '
        'ranked by top2 log-mean-exp; budget 16; final score (1-a)*FRAM + a*peak, beta 8.',
        '626.log: the DIAG-calibrated reranker was PEAK25; PEAK50 scored 24/24 validation and 48/48 alternate wording; '
        '627.py itself states PEAK50 was chosen after inspecting TEST626 validation -> confirmation, not blind generalisation; '
        '627.log: LOCKED_ROUTE 96/96, E2E ORIGINAL 48/48 and ALTERNATE 48/48.',
        'MAM worked because each question shared distinctive tokens with exactly one fact (lexical-geometric overlap in '
        'centred layer-3 space); it never had to encode relation DIRECTION or a second hop.',
        '647.log (blob 7123968b): BLIND_BOTH_SOURCES 12/16, BLIND_BOTH_ANSWERS_CORRECT 7/16, ATOMIC 23/32 -> two-source '
        'retrieval partly works, use of both does not.',
        '648.log (blob 245f3a00): LATENT AB both_ordered 0/16, FUSION_UNIQUE 0/16 -> fusion of two retrieved cartridges did '
        'not yield relational composition. 649: the B-only control answered 12/12, so composite success was not attributable.',
        'v3 locked engine: 815.py blob 77774f87, 827.py blob 567822d3, 829.py blob a5a25460 (CUT3/H3/KV fusion, SHA gates), '
        'GPU-completed in TEST829-833. The v3 router (757/815 numeric_rank: uncentred top-2 cosine of H3 rows) has no '
        'reported measurement exceeding PEAK50; TEST834 measures both on the same sealed panel.',
        '833.log (blob b9eccd8b): A 4/24, B 4/24, C 5/24, verdict FAIL; trajectories differ 24/24; corrections 0; probe '
        'equivalence gates passed; 754 forwards in 560.4 s; peak 38.92 GiB.'],
    'implemented_in_TEST834': [
        'MAM PEAK50 pipeline rebuilt on 72B CUT3 rows (store mean, PCA128 candidate stage with exact inner-product search '
        'in place of FAISS IVF, top2, budget 16, PEAK50).',
        'HeadProbe834: observation-only per-head attention capture of the final question token at all 80 layers (same '
        'technique as the locked AttentionIntervention; outputs computed by the unchanged SDPA).',
        'Pointer re-addressing: locked-head attention weights x stored native rows of mounted evidence, re-addressed with '
        'the same MAM rule over unmounted cartridges.',
        'Head locked on separate calibration worlds before any evaluation forward.',
        'TEST833 KV recurrence preserved (RoPE relocation, Haar value rotation, equivalence and determinism gates).',
        'EXTERNAL_UPTAKE_INTERFACE (labelled external controller).',
        'Offline stage 1-5 evaluation, predeclared criteria, calibrated-stump native-signal test.'],
    'demonstrated_by_TEST834': 'filled only from this run (report834 / verdict834); nothing is claimed before GPU execution'}

BODY834 = r'''
D829['test'] = '834'
D829['controller'] = ('MAM_PEAK50_ADDRESS + NATIVE_ATTENTION_POINTER_READDRESS + TEST833_KV_RECURRENCE; '
                      'EXTERNAL_UPTAKE_INTERFACE (labelled external controller)')
D829['source829_blob'] = LOCK834
D829['hypotheses834'] = PANEL829['test834']['hypotheses']
D829['claims_ledger834'] = CLAIMS834
D829['limitations'] = [
    'Selection, acceptance and stopping are made by a fixed external interface (address rule + uptake comparison) acting on native numbers; they are not model-internal decisions.',
    'Native sufficiency, contradiction and abstention declarations are UNIMPLEMENTED: the frozen model exposes no such output without language.',
    'The pointer is a fixed linear readout (attention weights of one calibrated head x stored native rows), computed in Python.',
    'FAISS IVF is replaced by exact inner-product search in the same PCA128 space (banks of <= 16 cartridges; IVF could only lower recall).',
    'The question tokens are re-entered at every forward (boundary input); no other text enters any runtime computation.',
    'Six synthetic sealed worlds, six bank conditions; one template, one model; twelve separate calibration worlds.',
    'Offline answer readouts use the TEST827 boundary instruction and are produced only after all numerical work and integrity gates.',
    'No GPU execution or result is claimed by the code author.']
gate829('SOURCE829_BLOB', True, LOCK834)
gate829('PANEL_FRESH_SEED', SEED829 == SEED834, SEED829)
gate829('NO_CONTROL_TEXT', MAX_NEW_CONTROL829 == 0)
gate829('RUN_COUNT', len(RUNS834) == len(CONDS834) * len(questions829) and len(questions829) == WORLDS_EVAL834, len(RUNS834))
gate829('CALIBRATION_DISJOINT', not (set(CALSTORE834) & set(EVALSTORE834)) and
        not ({j['qid'] for j in CALJOBS834} & {q['qid'] for q in questions829}))
gate829('MOUNT_CARTRIDGES_PHYSICAL', all(c in entries for r in RUNS834 for c in r['bank']) and
        all(c in entries for c in CALSTORE834))
gate829('MOUNT_EXCLUDES_NULL', all(NULL829 not in r['bank'] for r in RUNS834))
gate829('ENGINE_SYMBOLS834', all(callable(globals().get(x)) for x in
        ('cache_build', 'pairs', 'rephase', 'Cut3Diagnostic', 'AttentionIntervention', 'prompt_ids', 'build_fusion',
         'memory_seals', 'compare_seals', 'free_generate', 'observe_state', 'DirectCut3', 'kv_digest', 'safe_load',
         'numeric_rank', 'cosdist829', 'jsd829', 'full_readout829')))
gate829('ARCH_DIMS', (NL, H, QH, KVH, HD) == EXPECTED_ARCH834 and
        int(model.config.num_attention_heads) == QH and int(model.config.num_key_value_heads) == KVH and
        int(model.config.hidden_size) == H, (NL, H, QH, KVH, HD))
gate829('BF16_COMPUTE', DTYPE == _torch829.bfloat16, str(DTYPE))
gate829('NF4_LINEAR4BIT', any(isinstance(m_, bitsandbytes.nn.Linear4bit) for m_ in model.modules()))
gate829('WEIGHTS_FROZEN', all(not p_.requires_grad for p_ in model.parameters()))
gate829('DEVICE', str(DEV).startswith(DEVICE_KIND834), str(DEV))
gate829('ROPE_MODULE', callable(getattr(model.model, 'rotary_emb', None)))
gate829('SDPA_MODULE', F is _torch829.nn.functional and F.scaled_dot_product_attention is SDPA829)
gate829('PREFIX_P', P == 30, P)
POST834 = cost_upper834({c: int(entries[c]['body_tokens']) for c in cards829}, P)
D829['predicted_cost834'] = POST834
log829('TEST834_PREDICTED_COST', json.dumps(POST834))
gate829('PREDICTED_BUDGET_POST_LOAD', POST834['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN834,
        POST834['minutes_upper_excluding_model_load'])
QTEXT834 = {q['qid']: q['question'] for q in questions829}
QTEXT834.update({j['qid']: j['question'] for j in CALJOBS834})
LQ834 = {qid: list(prompt_ids(t)) for qid, t in QTEXT834.items()}
maxL834 = max(len(v) for v in LQ834.values())
gate829('FUSION_TOKENS_WITH_STATE', POST834['max_memory_tokens'] + 2 * maxL834 + 64 <= MAX_FUSED_TOKENS,
        {'memory': POST834['max_memory_tokens'], 'question': maxL834})
try:
    free834, _ = _torch829.cuda.mem_get_info()
    gate829('VRAM_HEADROOM', free834 / 2**30 >= 8.0, round(free834 / 2**30, 2))
except Exception as e834:
    gate829('VRAM_HEADROOM', False, repr(e834))
D829['noninterference834'] = noninterference829([NULL829], questions829[0]['question'])
for k834, v834 in D829['noninterference834'].items():
    gate829('NONINTERFERENCE_' + k834.upper(), bool(v834), v834)

COUNT834 = {'fusion_forwards': fusion_forwards829([NULL829]), 'probe_forwards': 3, 'capture_forwards': 0,
            'rank_forwards': 0, 'generation_forwards': 1, 'mounts': 1}
T0_834 = time.perf_counter()
HEART834 = DIR829 / 'TEST834_heartbeat.txt'
def beat834(*a):
    msg = ' '.join(map(str, a)) + ' t=' + str(round(time.perf_counter() - T0_834, 1)) + 's'
    print(msg, flush=True)
    with HEART834.open('a', encoding='utf-8') as fh:
        fh.write(msg + '\n')

# ------------------------------------------------------------------------------------------------------------------
# NATIVE ROW STORE (physical cartridges, SHA-verified by the locked safe_load; label-free)
# ------------------------------------------------------------------------------------------------------------------
ROWS834 = {}
for cid834 in EVALSTORE834 + CALSTORE834:
    with contextlib.redirect_stdout(io.StringIO()):
        cp834 = safe_load(entries[cid834])
    b834 = int(entries[cid834]['body_tokens'])
    h3_834 = cp834['h'][0, P:, :].float().numpy().astype(np.float32)
    v2_834 = cp834['lower'][2][1][0].float().numpy().astype(np.float32)          # (KVH, n, HD), values carry no RoPE
    l2v834 = np.ascontiguousarray(np.transpose(v2_834[:, P:, :], (1, 0, 2)).reshape(b834, KVH * HD))
    gate829('MEAS_ROWS_' + cid834, h3_834.shape == (b834, H) and l2v834.shape == (b834, KVH * HD) and
            bool(np.isfinite(h3_834).all()) and bool(np.isfinite(l2v834).all()))
    ROWS834[cid834] = {'H3': h3_834, 'L2V': l2v834}
    del cp834, v2_834

def unit834(x):
    x = np.asarray(x, dtype=np.float32)
    return x / np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-9)

def fit_store834(cids):
    """MAM transform_fit(rank=0) + MAM PCA128 index geometry, fitted on store rows only (no labels, no queries)."""
    st = {}
    for sp in SPACES834:
        X = np.concatenate([ROWS834[c][sp] for c in cids]).astype(np.float64)
        mu = X.mean(0)
        A = {c: unit834(ROWS834[c][sp] - mu) for c in cids}
        T = np.concatenate([A[c] for c in cids]).astype(np.float64)
        center = T.mean(0)
        _, _, vh = np.linalg.svd(T - center, full_matrices=False)
        r = min(PCA_RANK834, vh.shape[0])
        basis = vh[:r].T.astype(np.float32)
        PR = {c: ((A[c] - center) @ basis).astype(np.float32) for c in cids}
        st[sp] = {'mu': mu.astype(np.float32), 'center': center.astype(np.float32), 'basis': basis, 'A': A, 'PR': PR,
                  'rank': r, 'rows': int(T.shape[0])}
    return st
STORE834 = {'eval': fit_store834(EVALSTORE834), 'cal': fit_store834(CALSTORE834)}
D829['address_store834'] = {s: {sp: {'rows': STORE834[s][sp]['rows'], 'pca_rank': STORE834[s][sp]['rank']}
                                for sp in SPACES834} for s in STORE834}

def lse834(x, axis):
    m = np.max(x, axis=axis, keepdims=True)
    return (m + np.log(np.sum(np.exp(x - m), axis=axis, keepdims=True))).squeeze(axis)

def address834(Q, cards, store, sp, tie):
    """MAM v1.3.0 address rule on applied query rows Q (m x dim) over the given cartridges (exact search)."""
    if not cards or Q is None:
        return {'ranked': [], 'score': {}, 'touched': 0, 'candidates': []}
    st = STORE834[store][sp]
    Q = np.asarray(Q, dtype=np.float32).reshape(-1, st['mu'].shape[0])
    qp = (Q - st['center']) @ st['basis']
    owner = np.concatenate([np.full(len(st['PR'][c]), i) for i, c in enumerate(cards)])
    ip = qp @ np.concatenate([st['PR'][c] for c in cards]).T
    k = min(TOKEN_K834, ip.shape[1])
    hits = np.argpartition(-ip, k - 1, axis=1)[:, :k]
    touched = sorted({cards[int(owner[j])] for j in hits.reshape(-1)}, key=lambda c: tie.get(c, 10**6))
    sims = {c: (Q @ st['A'][c].T).astype(np.float64) for c in touched}
    top2 = {}
    for c, s in sims.items():
        v = np.sort(s, axis=1)[:, -min(2, s.shape[1]):]
        top2[c] = float(np.mean((lse834(v * BETA834, 1) - math.log(s.shape[1])) / BETA834))
    cand = sorted(touched, key=lambda c: (-top2[c], tie.get(c, 10**6)))[:BUDGET834]
    score = {}
    for c in cand:
        s = sims[c]
        fram = float(np.mean((lse834(s * BETA834, 1) - math.log(s.shape[1])) / BETA834))
        peak = float(np.mean(s.max(axis=1)))
        score[c] = (1.0 - PEAK_A834) * fram + PEAK_A834 * peak
    ranked = sorted(cand, key=lambda c: (-score[c], tie.get(c, 10**6)))
    return {'ranked': ranked, 'score': score, 'touched': len(touched), 'candidates': cand}

def address_batch834(QS, cards, store, sp):
    """Same rule for many single-row queries at once (calibration of all heads). cards must be in tie order."""
    st = STORE834[store][sp]
    QS = np.asarray(QS, dtype=np.float32)
    qp = (QS - st['center']) @ st['basis']
    owner = np.concatenate([np.full(len(st['PR'][c]), i) for i, c in enumerate(cards)])
    ip = qp @ np.concatenate([st['PR'][c] for c in cards]).T
    k = min(TOKEN_K834, ip.shape[1])
    hits = np.argpartition(-ip, k - 1, axis=1)[:, :k]
    T = np.zeros((QS.shape[0], len(cards)), dtype=bool)
    T[np.arange(QS.shape[0])[:, None], owner[hits]] = True
    TOP2 = np.full(T.shape, -np.inf); SC = np.full(T.shape, -np.inf)
    for i, c in enumerate(cards):
        s = (QS @ st['A'][c].T).astype(np.float64)
        v = np.sort(s, axis=1)[:, -min(2, s.shape[1]):]
        TOP2[:, i] = (lse834(v * BETA834, 1) - math.log(s.shape[1])) / BETA834
        SC[:, i] = (1.0 - PEAK_A834) * ((lse834(s * BETA834, 1) - math.log(s.shape[1])) / BETA834) + PEAK_A834 * s.max(axis=1)
    TOP2 = np.where(T, TOP2, -np.inf)
    order = np.argsort(-TOP2, axis=1, kind='stable')[:, :BUDGET834]
    C = np.zeros(T.shape, dtype=bool)
    C[np.arange(T.shape[0])[:, None], order] = True
    C &= T
    S = np.where(C, SC, -np.inf)
    return S

def apply_vec834(v, store, sp):
    return unit834(np.asarray(v, dtype=np.float32) - STORE834[store][sp]['mu'])

# ------------------------------------------------------------------------------------------------------------------
# OBSERVATION-ONLY PER-HEAD ATTENTION CAPTURE (all layers; outputs by the unchanged SDPA call)
# ------------------------------------------------------------------------------------------------------------------
class HeadProbe834:
    """Temporarily replaces F.scaled_dot_product_attention and every self_attn.forward (instance-method replacement, the
    locked AttentionIntervention technique; never a hook). The SDPA output is computed by the original function with the
    unchanged arguments. Additionally the float32 softmax row of the final query token is copied per head."""
    def __init__(self):
        self.old_sdpa = None; self.old_forwards = {}; self.active = None; self.rows = {}; self.calls = 0
    def __enter__(self):
        self.old_sdpa = F.scaled_dot_product_attention
        ctx = self
        def intercepted(q, k, v, attn_mask=None, dropout_p=0.0, is_causal=False, scale=None, enable_gqa=False):
            layer = ctx.active
            if layer is not None:
                ctx.calls += 1
                if q.ndim != 4 or k.ndim != 4 or v.ndim != 4:
                    raise RuntimeError('UNEXPECTED_SDPA_SHAPE')
                if q.shape[1] != k.shape[1] and not enable_gqa:
                    raise RuntimeError('GQA_UNDECLARED_IN_SDPA')
                if layer in ctx.rows:
                    raise RuntimeError('SDPA_CALLED_TWICE_IN_LAYER')
                with torch.no_grad():
                    nq = q.shape[-2]; nk = k.shape[-2]
                    qq = q[:, :, -1:, :].float(); kk = k.float()
                    if qq.shape[1] != kk.shape[1]:
                        kk = kk.repeat_interleave(qq.shape[1] // kk.shape[1], dim=1)
                    factor = (q.shape[-1] ** -0.5) if scale is None else scale
                    s = torch.matmul(qq, kk.transpose(-2, -1)) * factor
                    if attn_mask is not None:
                        if attn_mask.dtype == torch.bool:
                            s = s.masked_fill(~attn_mask[..., -1:, :], float('-inf'))
                        else:
                            s = s + attn_mask[..., -1:, :].float()
                    if is_causal and nq > 1:
                        allowed = nk - nq + (nq - 1)
                        s[..., allowed + 1:] = float('-inf')
                    pr = torch.softmax(s, dim=-1)
                    ctx.rows[layer] = pr[0, :, 0, :].detach().to('cpu').numpy().astype(np.float32, copy=True)
            return ctx.old_sdpa(q, k, v, attn_mask=attn_mask, dropout_p=dropout_p, is_causal=is_causal, scale=scale,
                                enable_gqa=enable_gqa)
        F.scaled_dot_product_attention = intercepted
        try:
            for i in range(NL):
                module = model.model.layers[i].self_attn
                if module._forward_hooks or module._forward_pre_hooks:
                    raise RuntimeError('ATTENTION_HOOK_PRESENT')
                old = module.forward; self.old_forwards[i] = old
                def wrapped(this, *args, _i=i, _old=old, **kwargs):
                    prior = ctx.active; ctx.active = _i
                    try:
                        return _old(*args, **kwargs)
                    finally:
                        ctx.active = prior
                module.forward = types.MethodType(wrapped, module)
        except BaseException:
            self.__exit__(None, None, None); raise
        return self
    def __exit__(self, *exc):
        for i, old in self.old_forwards.items():
            model.model.layers[i].self_attn.forward = old
        if self.old_sdpa is not None:
            F.scaled_dot_product_attention = self.old_sdpa
        self.active = None
        return False

def concat834(memx, S):
    if S is None:
        return list(memx)
    return [(torch.cat([mk, sk], dim=-2), torch.cat([mv, sv], dim=-2)) for (mk, mv), (sk, sv) in zip(memx, S)]

def rprobe834(memx, S, qids, keep_lp=False):
    """One native forward of the question over cache [M ; S] (TEST833 rprobe833 call, identical positions and mask), with
    the per-head probe, the CUT3 diagnostic and the observation-only lm_head readout."""
    n = int(memx[0][0].shape[-2]); L = len(qids)
    nS = int(S[0][0].shape[-2]) if S is not None else 0
    start = n + nS
    cache = cache_build(concat834(memx, S))
    pos = torch.arange(start, start + L, device=DEV)
    with torch.no_grad():
        with Cut3Diagnostic() as diag, HeadProbe834() as hp, Readout829() as ro:
            out = model(input_ids=torch.tensor([qids], device=DEV), past_key_values=cache,
                        attention_mask=torch.ones((1, start + L), device=DEV, dtype=torch.long),
                        position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
        if diag.last is None or hp.calls != NL or len(hp.rows) != NL or ro.calls != 1:
            raise RuntimeError('TEST834_PROBE_NOT_ACTIVE')
        state = diag.last.float().reshape(-1).cpu().numpy().astype(np.float64)
        lp, lp16, summ = full_readout829(ro.h, ro.z)
        hvec = ro.h.reshape(-1).double().cpu().numpy().copy()
        grown = pairs(out.past_key_values)
        if len(grown) != NL or int(grown[0][0].shape[-2]) != start + L:
            raise RuntimeError('CACHE_GROWTH_UNEXPECTED')
        newS = [(k[:, :, start:start + L, :].clone(), v[:, :, start:start + L, :].clone()) for k, v in grown]
        rows = hp.rows
    if F.scaled_dot_product_attention is not SDPA829 or model.lm_head.__dict__.get('forward') is not HEAD_FWD829:
        raise RuntimeError('TEST834_WRAPPER_NOT_RESTORED')
    if any(rows[l].shape != (QH, start + L) or not np.isfinite(rows[l]).all() for l in range(NL)):
        raise RuntimeError('TEST834_HEAD_ROWS_INVALID')
    del out, cache, grown, lp16
    COUNT834['probe_forwards'] += 1
    res = {'state': state, 'h': hvec, 'summary': summ, 'rows': rows, 'S_raw': newS, 'start': start, 'n': n, 'L': L}
    if keep_lp:
        res['lp'] = lp
    else:
        del lp
    return res

def relocate834(S, old_start, new_start, L):
    if old_start == new_start:
        return [(k, v) for k, v in S]
    old = torch.arange(old_start, old_start + L, device=DEV); new = torch.arange(new_start, new_start + L, device=DEV)
    return [(rephase(k, old, new), v) for k, v in S]

rs834 = np.random.default_rng(SEED834 + 33)
ROT834 = []
for l834 in range(NL):
    mats834 = []
    for j834 in range(KVH):
        qm834, rm834 = np.linalg.qr(rs834.standard_normal((HD, HD)))
        mats834.append(qm834 * np.sign(np.diag(rm834))[None, :])
    ROT834.append(torch.tensor(np.stack(mats834).astype(np.float32), device=DEV))

def rotate834(S):
    return [(k, torch.matmul(v.float(), ROT834[l]).to(v.dtype)) for l, (k, v) in enumerate(S)]

SEAL_LAYERS834 = (0, CUT, NL // 2, NL - 1)
def seal834(memx):
    return [(kv_digest(memx[l][0]), kv_digest(memx[l][1])) for l in SEAL_LAYERS834]

def mount834(ids, tag):
    with contextlib.redirect_stdout(io.StringIO()):
        engine_bindings829('MOUNT_' + tag)
        memx, active, _, _ = build_fusion(list(ids), 'TEST834_' + tag, True)
    n = int(memx[0][0].shape[-2])
    gate829('MEAS_MOUNT_' + tag, len(memx) == NL and list(active) == list(ids) and
            n == P + sum(int(entries[c]['body_tokens']) for c in ids), {'n': n})
    COUNT834['fusion_forwards'] += fusion_forwards829(list(ids)); COUNT834['mounts'] += 1
    return memx, n

def cspans834(mount):
    out = []; pos = P
    for c in mount:
        b = int(entries[c]['body_tokens']); out.append((c, pos, pos + b)); pos += b
    return out

def card_mass834(rows, csp):
    M = np.stack([rows[l] for l in range(NL)]).astype(np.float64)         # (NL, QH, nk)
    return np.stack([M[:, :, a:b].sum(-1) for _, a, b in csp], axis=-1)   # (NL, QH, ncards)

def pointer_rows834(r, csp, sp, store):
    w = np.concatenate([r[a:b] for _, a, b in csp]).astype(np.float64)
    tot = float(w.sum())
    if not np.isfinite(tot) or tot <= 0:
        return None
    X = np.concatenate([ROWS834[c][sp] for c, _, _ in csp]).astype(np.float64)
    return apply_vec834((w / tot) @ X, store, sp)

def gap_count834(vals):
    v = [max(float(x), 1e-300) for x in vals]
    if len(v) < 3:
        return len(v)
    gaps = [math.log(v[j]) - math.log(v[j + 1]) for j in range(len(v) - 1)]
    return 1 + max(range(len(gaps)), key=lambda j: (gaps[j], -j))

def legacy833_834(rows, csp, tie):
    # TEST833 readout (CONTROL ONLY): deep-layer head-mean attention mass per card, largest-log-gap count.
    deep = {c: float(np.mean([rows[l][:, a:b].sum(-1).mean() for l in DEEP_LAYERS834])) for c, a, b in csp}
    ranked = sorted(deep, key=lambda c: (-deep[c], tie.get(c, 10**6)))
    g = gap_count834([deep[c] for c in ranked])
    return {'decision': 'INCOMPLETE' if g == 1 else ('SUFFICIENT' if g == 2 else 'CONFLICT'), 'top': ranked[:g],
            'ranked': ranked[:6], 'deep_mass': [deep[c] for c in ranked[:6]]}

def core_span834(qids):
    head = tok('\nQUESTION:\n', add_special_tokens=False).input_ids
    tail = tok('\n\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n', add_special_tokens=False).input_ids
    a = 0
    while a < min(len(head), len(qids)) and qids[a] == head[a]:
        a += 1
    b = 0
    while b < min(len(tail), len(qids) - a) and qids[-1 - b] == tail[-1 - b]:
        b += 1
    return a, len(qids) - b

def question_rows834(qid):
    """MAM question_rep on 72B: CUT3 rows of the question tokens after the same fixed PREFIX as every cartridge."""
    qids = LQ834[qid]; ids = list(PIDS) + qids; coll = []
    with torch.no_grad():
        with DirectCut3(model.model.layers[CUT], 'capture', collector=coll):
            out = model(input_ids=torch.tensor([ids], device=DEV), use_cache=False, return_dict=True)
        del out
    h = torch.cat(coll, dim=1)[0].float().numpy().astype(np.float32)
    COUNT834['capture_forwards'] += 1
    a, b = core_span834(qids)
    gate829('MEAS_QROWS_' + qid, h.shape == (len(ids), H) and 0 <= a < b <= len(qids), {'span': [a, b]})
    return h[P + a:P + b], {'span': [a, b], 'tokens': len(qids)}

# ------------------------------------------------------------------------------------------------------------------
# S_null(q): question KV over the physical NULL card (TEST833), one NULL mount reused for all questions.
# ------------------------------------------------------------------------------------------------------------------
memN834, nN834 = mount834([NULL829], 'NULL')
sealN834 = seal834(memN834)
SNULL834 = {}
for qid834 in QTEXT834:
    pN = rprobe834(memN834, None, LQ834[qid834])
    SNULL834[qid834] = {'S': [(k.clone(), v.clone()) for k, v in pN['S_raw']], 'pos': pN['start'], 'h': pN['h'],
                        'state': pN['state']}
    del pN
gate829('KV_SEAL_NULL_AFTER_PROBES', seal834(memN834) == sealN834)
del memN834; gc.collect(); release()

def s0_834(qid, n):
    sn = SNULL834[qid]
    return relocate834(sn['S'], sn['pos'], n, len(LQ834[qid]))

# ---- equivalence gate on a CALIBRATION mount: the probe without state reproduces the locked observe_state ----
j0_834 = CALJOBS834[0]
memE834, nE834 = mount834([j0_834['first'], j0_834['second']], 'EQUIV')
b0E834 = int(entries[j0_834['first']]['body_tokens'])
spE834 = {'B0': (P, P + b0E834), 'B1': (P + b0E834, nE834)}
with Readout829() as roE834:
    stE834, attE834 = observe_state(memE834, QTEXT834[j0_834['qid']], spE834)
COUNT834['probe_forwards'] += 1
pE834 = rprobe834(memE834, None, LQ834[j0_834['qid']])
hp_mass834 = {str(l): {'B0': float(pE834['rows'][l][:, spE834['B0'][0]:spE834['B0'][1]].sum(-1).mean()),
                      'B1': float(pE834['rows'][l][:, spE834['B1'][0]:spE834['B1'][1]].sum(-1).mean())}
              for l in (4, 20, 40, 79) if l < NL}
D829['probe_equivalence834'] = {
    'cut3_state_bitwise': bool(np.array_equal(stE834.float().cpu().numpy().astype(np.float64), pE834['state'])),
    'final_hidden_bitwise': bool(np.array_equal(roE834.h.reshape(-1).double().cpu().numpy(), pE834['h'])),
    'headprobe_mass_max_abs_vs_locked_probe': max(abs(hp_mass834[l][s] - float(attE834[l][s + '_mass']))
                                                  for l in hp_mass834 for s in ('B0', 'B1'))}
for k834 in ('cut3_state_bitwise', 'final_hidden_bitwise'):
    gate829('RECURRENT_PROBE_EQUALS_OBSERVE_STATE_' + k834.upper(), D829['probe_equivalence834'][k834])
gate829('HEADPROBE_EQUALS_LOCKED_ATTENTION_PROBE', D829['probe_equivalence834']['headprobe_mass_max_abs_vs_locked_probe'] <= 2e-6,
        D829['probe_equivalence834']['headprobe_mass_max_abs_vs_locked_probe'])
del memE834, pE834, stE834; gc.collect(); release()

# ==================================================================================================================
# CALIBRATION PHASE (separate calibration worlds; their role labels are used ONLY here, before any evaluation forward)
# ==================================================================================================================
beat834('TEST834_CALIBRATION_START', len(CALJOBS834), 'jobs')
NH834 = NL * QH
CALARR834 = {'hit': {sp: [] for sp in SPACES834}, 'margin': {sp: [] for sp in SPACES834},
             'best_after_first': {sp: [] for sp in SPACES834}, 'best_after_pair': {sp: [] for sp in SPACES834},
             'up': [], 'rej_mirror': [], 'rej_other': [], 'cardmass_first': [], 'cardmass_pair': []}
CALSCALAR834 = []
CALHOP1_834 = []
def allhead_pointers834(rows, csp, sp, store):
    Mx = np.stack([rows[l] for l in range(NL)]).reshape(NH834, -1).astype(np.float64)
    idx = np.concatenate([np.arange(a, b) for _, a, b in csp])
    W = Mx[:, idx]; W = (W / np.maximum(W.sum(1, keepdims=True), 1e-300)).astype(np.float32)
    X = np.concatenate([ROWS834[c][sp] for c, _, _ in csp]).astype(np.float32)
    return unit834(W @ X - STORE834[store][sp]['mu'])
for ji834, job in enumerate(CALJOBS834):
    qid = job['qid']; qids = LQ834[qid]; tieC = {c: i for i, c in enumerate(job['bank'])}
    qr, _ = question_rows834(qid)
    h1 = address834(apply_vec834(qr, 'cal', 'H3'), job['bank'], 'cal', 'H3', tieC)
    CALHOP1_834.append({'qid': qid, 'top1_is_first': bool(h1['ranked'] and h1['ranked'][0] == job['first']),
                        'rank_first': (h1['ranked'].index(job['first']) + 1) if job['first'] in h1['ranked'] else None})
    feats = {}
    for tag, mount in (('P1', [job['first']]), ('P2', [job['first'], job['second']]),
                       ('P3', [job['first'], job['mirror']]), ('P4', [job['first'], job['other']])):
        memx, n = mount834(mount, 'CAL_%d_%s' % (ji834, tag))
        seal = seal834(memx)
        p = rprobe834(memx, s0_834(qid, n), qids)
        gate829('MEAS_KV_SEAL_CAL_%d_%s' % (ji834, tag), seal834(memx) == seal)
        csp = cspans834(mount)
        Mc = card_mass834(p['rows'], csp).reshape(NH834, len(mount))
        feats[tag] = {'entropy': p['summary']['entropy_nats'], 'null_dist': cosdist829(p['h'], SNULL834[qid]['h'])}
        if tag in ('P1', 'P2'):
            rest = [c for c in job['bank'] if c not in mount]
            for sp in SPACES834:
                PT = allhead_pointers834(p['rows'], csp, sp, 'cal')
                S = address_batch834(PT, rest, 'cal', sp)
                best = np.max(S, axis=1)
                CALARR834['best_after_first' if tag == 'P1' else 'best_after_pair'][sp].append(best)
                if tag == 'P1':
                    ti = rest.index(job['second'])
                    others = np.delete(S, ti, axis=1)
                    oth = np.max(others, axis=1) if others.shape[1] else np.full(NH834, -np.inf)
                    hit = np.isfinite(S[:, ti]) & (S[:, ti] > oth)
                    CALARR834['hit'][sp].append(hit)
                    CALARR834['margin'][sp].append(np.where(np.isfinite(S[:, ti]) & np.isfinite(oth), S[:, ti] - oth, -1.0))
            CALARR834['cardmass_first' if tag == 'P1' else 'cardmass_pair'].append(Mc.sum(1))
        if tag == 'P2':
            CALARR834['up'].append(Mc[:, 1] > Mc[:, 0])
        if tag == 'P3':
            CALARR834['rej_mirror'].append(Mc[:, 1] < Mc[:, 0])
        if tag == 'P4':
            CALARR834['rej_other'].append(Mc[:, 1] < Mc[:, 0])
        del memx, p; gc.collect(); release()
    CALSCALAR834.append(feats)
    beat834('TEST834_CALIBRATION', ji834 + 1, '/', len(CALJOBS834))
UPT834 = np.sum(CALARR834['up'], axis=0) + np.sum(CALARR834['rej_mirror'], axis=0) + np.sum(CALARR834['rej_other'], axis=0)
cands834 = []
for si834, sp in enumerate(SPACES834):
    tot = np.sum(CALARR834['hit'][sp], axis=0) + UPT834
    mar = np.mean(CALARR834['margin'][sp], axis=0)
    for hi in range(NH834):
        cands834.append((int(tot[hi]), float(mar[hi]), -si834, -(hi // QH), -(hi % QH), sp, hi))
cands834.sort(reverse=True)
best834 = cands834[0]
LOCKSP834 = best834[5]; LOCKL834 = best834[6] // QH; LOCKH834 = best834[6] % QH; LOCKI834 = best834[6]
nj834 = len(CALJOBS834)
D829['lock834'] = {
    'space': LOCKSP834, 'layer': int(LOCKL834), 'head': int(LOCKH834), 'calibration_total': best834[0],
    'calibration_max': 4 * nj834, 'mean_address_margin': best834[1],
    'in_sample_components': {
        'address_second_first': int(np.sum(CALARR834['hit'][LOCKSP834], axis=0)[LOCKI834]),
        'uptake_second': int(np.sum(CALARR834['up'], axis=0)[LOCKI834]),
        'reject_mirror': int(np.sum(CALARR834['rej_mirror'], axis=0)[LOCKI834]),
        'reject_other_world': int(np.sum(CALARR834['rej_other'], axis=0)[LOCKI834]), 'jobs': nj834},
    'top10': [{'total': c[0], 'margin': c[1], 'space': c[5], 'layer': c[6] // QH, 'head': c[6] % QH} for c in cands834[:10]],
    'note': 'IN-SAMPLE calibration counts (selection data); evaluation counts come only from the sealed panel.'}
D829['calibration_hop1_834'] = CALHOP1_834
# Offline-only sufficiency stumps (fitted here on calibration labels, applied only in the OFFLINE PHASE).
FEATS834 = ('entropy', 'lock_card_mass', 'lock_pointer_best', 'null_dist')
calpos834 = {f: [] for f in FEATS834}; calneg834 = {f: [] for f in FEATS834}
for ji834 in range(nj834):
    for f, (tagpos, tagneg) in (('entropy', ('P2', 'P1')), ('null_dist', ('P2', 'P1'))):
        calpos834[f].append(CALSCALAR834[ji834][tagpos][f]); calneg834[f].append(CALSCALAR834[ji834][tagneg][f])
    calpos834['lock_card_mass'].append(float(CALARR834['cardmass_pair'][ji834][LOCKI834]))
    calneg834['lock_card_mass'].append(float(CALARR834['cardmass_first'][ji834][LOCKI834]))
    calpos834['lock_pointer_best'].append(float(CALARR834['best_after_pair'][LOCKSP834][ji834][LOCKI834]))
    calneg834['lock_pointer_best'].append(float(CALARR834['best_after_first'][LOCKSP834][ji834][LOCKI834]))
def stump_fit834(pos, neg):
    vals = sorted(set(float(x) for x in pos + neg if np.isfinite(x)))
    if not vals:
        return {'threshold': None, 'sign': 1, 'cal_balanced_acc': 0.5}
    thr = [vals[0] - 1.0] + [(vals[i] + vals[i + 1]) / 2.0 for i in range(len(vals) - 1)] + [vals[-1] + 1.0]
    best = None
    for t in thr:
        for sgn in (1, -1):
            tp = np.mean([sgn * (x - t) > 0 for x in pos]); tn = np.mean([not (sgn * (x - t) > 0) for x in neg])
            acc = 0.5 * (tp + tn)
            if best is None or acc > best['cal_balanced_acc']:
                best = {'threshold': float(t), 'sign': sgn, 'cal_balanced_acc': float(acc)}
    return best
STUMP834 = {f: stump_fit834(calpos834[f], calneg834[f]) for f in FEATS834}
STUMPSEL834 = max(FEATS834, key=lambda f: (STUMP834[f]['cal_balanced_acc'], -FEATS834.index(f)))
D829['sufficiency_stumps834'] = {'stumps': STUMP834, 'selected_on_calibration': STUMPSEL834,
                                 'calibration_values': {'complete': calpos834, 'incomplete': calneg834}}
del CALARR834, cands834; gc.collect()
gate829('HEAD_LOCKED_BEFORE_EVALUATION', COUNT834['probe_forwards'] > 0 and isinstance(LOCKI834, int) and
        LOCKSP834 in SPACES834, D829['lock834']['space'] + ':' + str(LOCKL834) + ':' + str(LOCKH834))
log829('TEST834_LOCK', json.dumps(D829['lock834']))
COUNT_CAL834 = dict(COUNT834)

# ==================================================================================================================
# EVALUATION RUNTIME (sealed panel). From here until the OFFLINE PHASE no label, role, condition or answer is read.
# ==================================================================================================================
QA834, QSPAN834 = {}, {}
for q834 in sorted(QTEXT834):
    if q834 in {r['qid'] for r in RUNS834}:
        rq, info = question_rows834(q834)
        QA834[q834] = apply_vec834(rq, 'eval', 'H3'); QSPAN834[q834] = info
RANK815_834 = {}
for q834 in sorted(QA834):
    with contextlib.redirect_stdout(io.StringIO()):
        rk834, _ = numeric_rank(QTEXT834[q834], {c: bank829[c] for c in EVALSTORE834})
    RANK815_834[q834] = list(rk834); COUNT834['rank_forwards'] += 1

def lockinfo834(p, mount, excluded, bank, tie):
    r = p['rows'][LOCKL834][LOCKH834]
    csp = cspans834(mount)
    mass = {c: float(r[a:b].sum()) for c, a, b in csp}
    n = csp[-1][2] if csp else P
    rest = [c for c in bank if c not in excluded]
    ptr = pointer_rows834(r, csp, LOCKSP834, 'eval')
    adr = address834(ptr, rest, 'eval', LOCKSP834, tie) if ptr is not None else {'ranked': [], 'score': {}, 'touched': 0}
    arg = max(mass, key=lambda c: (mass[c], -tie.get(c, 10**6))) if mass else None
    return {'mass': mass, 'argmax_card': arg, 'card_mass_total': float(sum(mass.values())),
            'prefix_mass': float(r[:P].sum()), 'state_question_mass': float(r[n:].sum()),
            'addr_ranked': adr['ranked'][:8], 'addr_scores': {c: adr['score'][c] for c in adr['ranked'][:8]},
            'addr_best_score': (adr['score'][adr['ranked'][0]] if adr['ranked'] else None), 'touched': adr['touched'],
            'entropy': p['summary']['entropy_nats'], 'top_ids_offline': p['summary']['top_ids'][:4]}

def stop833_834(steps):
    # TEST833 stop rule (identical), used only for condition C
    for i in range(1, len(steps)):
        t = steps[i]['t']
        if steps[i].get('d_h') == 0.0:
            return t - 1, 'FIXED_POINT'
        if steps[i]['d_h'] <= 2.0 ** -8 * steps[i]['h_norm']:
            return t, 'PRECISION_FIXED_POINT'
        if i >= 2 and steps[i]['d_h'] >= steps[i - 1]['d_h']:
            return t - 1, 'CONTRACTION_ENDED'
    return steps[-1]['t'], 'SAFETY_T_MAX'

def loop834(mode, ctx):
    """B (reset), D (feedback), E (rotated feedback). Same external interface; only the state fed back differs."""
    K = [ctx['c1']]; X = []; L = ctx['L']; qid = ctx['qid']; bank = ctx['bank']; tie = ctx['tie']
    S_acc = {'S': ctx['S1'], 'pos': ctx['n1']}; last = ctx['info1']
    tries = []; stop = None; rot_err = 0.0; keys_same = True
    while stop is None:
        if len(K) >= T_ACCEPT_MAX834:
            stop = 'SAFETY_T_ACCEPT_MAX'; break
        cand = [c for c in last['addr_ranked'] if c not in K and c not in X]
        if not cand:
            stop = 'NO_ADDRESS'; break
        accepted = False
        for c in cand[:B_TRY834]:
            mount = K + [c]
            memx, n = mount834(mount, ctx['run'] + '_' + mode + '_%d_%d' % (len(K), len(tries)))
            seal = seal834(memx)
            if mode == 'B':
                Sin = s0_834(qid, n)
            else:
                Sin = relocate834(S_acc['S'], S_acc['pos'], n, L)
                if mode == 'E':
                    Sr = rotate834(Sin)
                    vn = [float(v.float().norm().item()) for _, v in Sin[::20]]
                    vr = [float(v.float().norm().item()) for _, v in Sr[::20]]
                    rot_err = max(rot_err, max(abs(a - b) / max(a, 1e-30) for a, b in zip(vn, vr)))
                    keys_same = keys_same and all(bool(torch.equal(a[0], b[0])) for a, b in zip(Sin, Sr))
                    Sin = Sr
            p = rprobe834(memx, Sin, ctx['qids'])
            gate829('MEAS_KV_SEAL_' + ctx['run'] + '_' + mode + '_%d' % len(tries), seal834(memx) == seal)
            info = lockinfo834(p, mount, set(mount) | set(X), bank, tie)
            uptake = info['mass'][c] > max(info['mass'][k] for k in K)
            tries.append({'step': len(K) + 1, 'candidate': c, 'uptake': bool(uptake), 'mass_new': info['mass'][c],
                          'mass_max_kept': max(info['mass'][k] for k in K), 'addr_score': last['addr_scores'].get(c),
                          'dist_to_B_same_mount': None, 'h_sha': sha829(np.asarray(p['h'], dtype=np.float32).tobytes()),
                          'h': p['h'] if mode in ('B', 'D') else None, 'info': {k_: info[k_] for k_ in
                          ('argmax_card', 'card_mass_total', 'prefix_mass', 'state_question_mass', 'addr_ranked',
                           'addr_best_score', 'entropy')}})
            if uptake:
                K.append(c); last = info; accepted = True
                if mode != 'B':
                    S_acc = {'S': relocate834(p['S_raw'], p['start'], n, L), 'pos': n}
            else:
                X.append(c)
            del memx, p, Sin
            gc.collect(); release()
            if accepted:
                break
        if not accepted:
            stop = 'NO_UPTAKE'
    return {'K': K, 'rejected': X, 'stop_kind': stop, 'accepted': len(K), 'tries': tries,
            'rotation_value_norm_rel_err': rot_err if mode == 'E' else None,
            'rotation_keys_unchanged': keys_same if mode == 'E' else None}

D829['runs834'] = []
BUDGET_STOP834 = False
t_eval834 = time.perf_counter()
for k_run834, r834 in enumerate(RUNS834):
    if (time.perf_counter() - T0_834) / 60.0 > HARD_BUDGET_MIN834:
        BUDGET_STOP834 = True
        log829('TEST834_BUDGET_STOP', 'completed_runs', k_run834, 'of', len(RUNS834))
        break
    tc = time.perf_counter()
    rid = r834['run']; bank = list(r834['bank']); tie = {c: i for i, c in enumerate(r834['tie_order'])}
    qid = r834['qid']; qids = LQ834[qid]; L = len(qids)
    beat834('TEST834_HEARTBEAT', k_run834 + 1, '/', len(RUNS834), rid, 'bank', len(bank))
    rec = {'run': rid, 'qid': qid, 'bank_size': len(bank)}
    h1 = address834(QA834[qid], bank, 'eval', 'H3', tie)
    rec['hop1'] = {'ranked': h1['ranked'], 'scores': h1['score'], 'touched': h1['touched'], 'candidates': h1['candidates']}
    rec['hop1_815'] = [c for c in RANK815_834[qid] if c in bank]
    # ---- A: frozen full-bank baseline, no addressing, no recurrence, both mount orders ----
    hA = {}
    for order in ('FWD', 'REV'):
        mount = list(bank) if order == 'FWD' else list(reversed(bank))
        memx, n = mount834(mount, rid + '_A_' + order)
        seal = seal834(memx)
        p = rprobe834(memx, s0_834(qid, n), qids)
        gate829('MEAS_KV_SEAL_' + rid + '_A_' + order, seal834(memx) == seal)
        info = lockinfo834(p, mount, set(mount), bank, tie)
        rec['A_' + order] = {'lock': {k_: info[k_] for k_ in ('mass', 'argmax_card', 'card_mass_total', 'entropy')},
                             'legacy833': legacy833_834(p['rows'], cspans834(mount), tie), 'memory_tokens': n}
        hA[order] = p['h']
        del memx, p; gc.collect(); release()
    rec['A_order_hidden_cosdist'] = cosdist829(hA['FWD'], hA['REV'])
    if not h1['ranked']:
        rec['no_hop1_address'] = True
        for mode in ('B', 'D', 'E'):
            rec[mode] = {'K': [], 'rejected': [], 'stop_kind': 'NO_ADDRESS', 'accepted': 0, 'tries': []}
        rec['C'] = {'K': [], 'stop_kind': 'NO_ADDRESS', 'stop_step': 0, 'steps': []}
        rec['TOP2'] = {'K': []}
        rec['D_vs_B_same_mount_hidden_dist'] = []
        rec['D_final'] = {'K': [], 'lock': {'argmax_card': None}, 'features': {f: None for f in FEATS834}}
        D829['runs834'].append(rec); save829(); continue
    c1 = h1['ranked'][0]
    # ---- step 1 (identical input for B, C, D, E) ----
    mem1, n1 = mount834([c1], rid + '_S1')
    seal1 = seal834(mem1)
    S0 = s0_834(qid, n1)
    back = relocate834(S0, n1, SNULL834[qid]['pos'], L)
    rec['rope_roundtrip_max_abs'] = max(float((a[0].float() - b[0].float()).abs().max().item())
                                        for a, b in zip(back, SNULL834[qid]['S']))
    del back
    p1 = rprobe834(mem1, S0, qids); p1b = rprobe834(mem1, S0, qids)
    rec['step1_deterministic'] = bool(np.array_equal(p1['h'], p1b['h']) and np.array_equal(p1['state'], p1b['state']))
    gate829('MEAS_STEP1_DETERMINISTIC_' + rid, rec['step1_deterministic'])
    del p1b
    info1 = lockinfo834(p1, [c1], {c1}, bank, tie)
    S1 = relocate834(p1['S_raw'], p1['start'], n1, L)
    # ---- C: TEST833 recurrence on the fixed hop-1 mount; addresses recorded, never executed ----
    stepsC = [{'t': 1, 'h_norm': float(np.linalg.norm(p1['h'])), 'addr_top': info1['addr_ranked'][:3],
               'argmax_card': info1['argmax_card'], 'entropy': info1['entropy']}]
    Sprev = S1; hprev = p1['h']
    for t in range(2, T_MAX_C834 + 1):
        p = rprobe834(mem1, Sprev, qids)
        inf = lockinfo834(p, [c1], {c1}, bank, tie)
        stepsC.append({'t': t, 'h_norm': float(np.linalg.norm(p['h'])), 'd_h': float(np.linalg.norm(p['h'] - hprev)),
                       'addr_top': inf['addr_ranked'][:3], 'argmax_card': inf['argmax_card'], 'entropy': inf['entropy'],
                       'dist_to_step1': float(np.linalg.norm(p['h'] - p1['h']))})
        Sprev = relocate834(p['S_raw'], p['start'], n1, L); hprev = p['h']
        del p
    gate829('MEAS_KV_SEAL_' + rid + '_STEP1_C', seal834(mem1) == seal1)
    stopC, kindC = stop833_834(stepsC)
    rec['C'] = {'K': [c1], 'stop_kind': kindC, 'stop_step': stopC, 'steps': stepsC}
    del mem1, Sprev; gc.collect(); release()
    rec['step1'] = {'card': c1, 'lock': {k_: info1[k_] for k_ in ('mass', 'card_mass_total', 'addr_ranked', 'addr_scores',
                                                                  'addr_best_score', 'entropy')}}
    ctx = {'run': rid, 'c1': c1, 'L': L, 'qid': qid, 'qids': qids, 'bank': bank, 'tie': tie, 'S1': S1, 'n1': n1,
           'info1': info1}
    for mode in ('B', 'D', 'E'):
        rec[mode] = loop834(mode, ctx)
    # recurrence enters the forward: D vs B hidden distance on identical mounts
    bh = {tuple(rec['B']['K'][:tr['step'] - 1] + [tr['candidate']]): tr['h'] for tr in rec['B']['tries']}
    dd = []
    for tr in rec['D']['tries']:
        key = tuple(rec['D']['K'][:tr['step'] - 1] + [tr['candidate']])
        if key in bh:
            tr['dist_to_B_same_mount'] = float(np.linalg.norm(tr['h'] - bh[key])); dd.append(tr['dist_to_B_same_mount'])
    rec['D_vs_B_same_mount_hidden_dist'] = dd
    for mode in ('B', 'D', 'E'):
        for tr in rec[mode]['tries']:
            tr.pop('h', None)
    del S1, ctx
    # ---- TOP2: static MAM top-2 (count fixed by construction; control only) ----
    k2 = h1['ranked'][:2]
    memx, n = mount834(k2, rid + '_TOP2')
    p = rprobe834(memx, s0_834(qid, n), qids)
    inf = lockinfo834(p, k2, set(k2), bank, tie)
    rec['TOP2'] = {'K': list(k2), 'lock': {k_: inf[k_] for k_ in ('mass', 'argmax_card', 'card_mass_total', 'entropy')}}
    del memx, p; gc.collect(); release()
    # ---- D final evidence set: S_null forwards for stage-2 dependence, order reversal and offline features ----
    KD = list(rec['D']['K'])
    memx, n = mount834(KD, rid + '_DF_FWD')
    seal = seal834(memx)
    fseal = memory_seals(memx)
    pF = rprobe834(memx, s0_834(qid, n), qids, keep_lp=True)
    gate829('MEAS_KV_FULLSEAL_' + rid, compare_seals(fseal, memory_seals(memx)) and seal834(memx) == seal)
    infF = lockinfo834(pF, KD, set(KD), bank, tie)
    rec['D_final'] = {'K': KD, 'lock': {k_: infF[k_] for k_ in ('mass', 'argmax_card', 'card_mass_total', 'addr_ranked',
                                                                 'addr_best_score', 'entropy')},
                      'features': {'entropy': pF['summary']['entropy_nats'], 'lock_card_mass': infF['card_mass_total'],
                                   'lock_pointer_best': infF['addr_best_score'],
                                   'null_dist': cosdist829(pF['h'], SNULL834[qid]['h'])}}
    del memx; gc.collect(); release()
    if len(KD) >= 2:
        memx, n = mount834(list(reversed(KD)), rid + '_DF_REV')
        p = rprobe834(memx, s0_834(qid, n), qids)
        infR = lockinfo834(p, list(reversed(KD)), set(KD), bank, tie)
        rec['D_final']['reversal'] = {'hidden_cosdist': cosdist829(pF['h'], p['h']), 'argmax_card': infR['argmax_card'],
                                      'argmax_same': infR['argmax_card'] == infF['argmax_card']}
        del memx, p; gc.collect(); release()
        loo = []
        for m in KD:
            sub = [c for c in KD if c != m]
            memx, n = mount834(sub, rid + '_LOO_' + m)
            p = rprobe834(memx, s0_834(qid, n), qids, keep_lp=True)
            loo.append({'removed': m, 'hidden_cosdist': cosdist829(pF['h'], p['h']), 'jsd': jsd829(pF['lp'], p['lp']),
                        'top1_same': top1_829(pF['lp']) == top1_829(p['lp'])})
            del memx, p; gc.collect(); release()
        rec['D_final']['loo'] = loo
    del pF; gc.collect(); release()
    rec['seconds'] = round(time.perf_counter() - tc, 3)
    D829['runs834'].append(rec)
    save829()
    log829('TEST834_RUN', rid, 'c1', c1, 'B', len(rec['B']['K']), rec['B']['stop_kind'], 'D', len(rec['D']['K']),
           rec['D']['stop_kind'], 'E', len(rec['E']['K']), rec['E']['stop_kind'], 'C', rec['C']['stop_kind'], 's', rec['seconds'])
D829['numeric_seconds834'] = round(time.perf_counter() - t_eval834, 3)
D829['budget_stop834'] = BUDGET_STOP834

# ---- integrity gates after all numerical work ----
engine_bindings829('FINAL')
gate829('FROZEN_WEIGHT_SENTINEL', before829 == sentinel())
gate829('NO_RESIDUAL_HOOKS', all(not model.model.layers[i]._forward_hooks and not model.model.layers[i]._forward_pre_hooks
                                 for i in range(NL)))
gate829('NO_ATTENTION_HOOKS', all(not model.model.layers[i].self_attn._forward_hooks and
                                  not model.model.layers[i].self_attn._forward_pre_hooks for i in range(NL)))
gate829('SDPA_RESTORED_FINAL', F.scaled_dot_product_attention is SDPA829)
gate829('LM_HEAD_UNWRAPPED', model.lm_head.__dict__.get('forward') is HEAD_FWD829 and
        not model.lm_head._forward_hooks and not model.lm_head._forward_pre_hooks)
gate829('PANEL_UNCHANGED', sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True)) == PANEL_SHA829)
for cid834 in cards829:
    gate829('FINAL_SHA_' + cid834, sha_file(CART_DIR / entries[cid834]['file']) == entries[cid834]['sha256'])
COUNT_NUMERIC834 = dict(COUNT834)
gate829('COUNTED_WITHIN_UPPER_BOUND', all(COUNT_NUMERIC834[k] <= POST834['numeric_upper'][k] for k in POST834['numeric_upper']),
        {'counted': COUNT_NUMERIC834, 'upper': POST834['numeric_upper']})

# ==================================================================================================================
# OFFLINE PHASE: every numerical result is saved; labels and text are used only from here.
# ==================================================================================================================
beat834('TEST834_OFFLINE_READOUTS_START')
TEXT834 = {}
def text834(mount, qid, tag):
    key = (qid, tuple(mount))
    if key in TEXT834:
        return TEXT834[key]
    if mount:
        memx, n = mount834(list(mount), 'TXT_' + tag)
    else:
        memx, n = mount834([NULL829], 'TXT_' + tag)
    o = free_generate(memx, answer_prompt829(QTEXT834[qid]), seed=None, gain=0., max_new=MAX_NEW_TEXT834, spans=None)
    COUNT834['generation_forwards'] += int(o['generated_tokens'])
    TEXT834[key] = {'text': o['raw'].strip(), 'tokens': int(o['generated_tokens'])}
    del memx; gc.collect(); release()
    return TEXT834[key]
for rec in D829['runs834']:
    qid = rec['qid']
    rec['text'] = {'A': text834(next(r['bank'] for r in RUNS834 if r['run'] == rec['run']), qid, rec['run'] + '_A'),
                   'NULL': text834([], qid, qid + '_NULL')}
    for mode in ('TOP2', 'B', 'D', 'E'):
        rec['text'][mode] = text834(rec[mode]['K'], qid, rec['run'] + '_' + mode) if rec[mode]['K'] else None
save829()

KIND834 = {cid: m['kind'] for cid, m in card_meta829.items()}
DOM834 = {cid: m['domain'] for cid, m in card_meta829.items()}
REL834 = {}
for w in worlds829:
    for kind, (a, b) in (('first', ('start', 'middle')), ('second', ('middle', 'end')), ('changed', ('middle', 'changed_end')),
                         ('decoy', ('decoy_end', 'start')), ('mirror', ('end', 'middle')), ('fork', ('start', 'fork_end'))):
        REL834[w['ids'][kind]] = (w[a], w[b])
def role834(cid, w):
    return ('OWN_' if DOM834.get(cid) == w['world'] else 'OTHER_') + str(KIND834.get(cid)).upper()
def endpoints834(K, w):
    mids = {REL834[c][1] for c in K if c in REL834 and REL834[c][0] == w['start']}
    ends = {REL834[c][1] for c in K if c in REL834 and REL834[c][0] in mids}
    name = {w['end']: 'END', w['changed_end']: 'ALT_END', w['middle']: 'MIDDLE', w['fork_end']: 'FORK_END',
            w['decoy_end']: 'DECOY', w['start']: 'START'}
    return sorted(name.get(e, 'OTHER') for e in ends)
def chain_cards834(K, w):
    mids = {REL834[c][1] for c in K if c in REL834 and REL834[c][0] == w['start']}
    ends_from = {c for c in K if c in REL834 and REL834[c][0] in mids}
    starts = {c for c in K if c in REL834 and REL834[c][0] == w['start'] and any(REL834[d][0] == REL834[c][1] for d in ends_from)}
    return starts | ends_from
EXPECT834 = {'FULL': ['END'], 'OWN_ONLY': ['END'], 'REPLACE_SECOND_BY_ALT': ['ALT_END'],
             'CONFLICT_ALT_ADDED': ['ALT_END', 'END'], 'MISSING_SECOND': [], 'MISSING_FIRST': []}
REQUIRED834 = {'FULL': ('first', 'second'), 'OWN_ONLY': ('first', 'second'), 'REPLACE_SECOND_BY_ALT': ('first', 'changed'),
               'CONFLICT_ALT_ADDED': ('first', 'second', 'changed'), 'MISSING_SECOND': (), 'MISSING_FIRST': ()}
COMPLETE834 = ('FULL', 'OWN_ONLY', 'REPLACE_SECOND_BY_ALT', 'CONFLICT_ALT_ADDED')
MISSING834 = ('MISSING_FIRST', 'MISSING_SECOND')
SAFETY834 = ('SAFETY_T_ACCEPT_MAX', 'SAFETY_T_MAX')
def text_class834(t, w):
    u = (t or '').upper()
    return [nm for nm, c in (('END', w['end']), ('MIDDLE', w['middle']), ('ALT_END', w['changed_end']),
                             ('FORK_END', w['fork_end']), ('DECOY', w['decoy_end'])) if c in u] + (['UNKNOWN'] if 'UNKNOWN' in u else [])
def text_correct834(cls, cond):
    names = [x for x in cls if x != 'UNKNOWN']
    if cond in ('FULL', 'OWN_ONLY'):
        return names == ['END'] and 'UNKNOWN' not in cls
    if cond == 'REPLACE_SECOND_BY_ALT':
        return names == ['ALT_END'] and 'UNKNOWN' not in cls
    if cond == 'CONFLICT_ALT_ADDED':
        return ('END' in names and 'ALT_END' in names) or (cls == ['UNKNOWN'])
    return cls == ['UNKNOWN']
EV834 = []
for rec in D829['runs834']:
    key = RUNKEY834[rec['run']]; w = worlds829[key['world']]; cond = key['condition']
    e = {'run': rec['run'], 'world': key['world'], 'block': key['block'], 'condition': cond}
    first = w['ids']['first']
    e['first_in_bank'] = cond != 'MISSING_FIRST'
    e['hop1_top_role'] = role834(rec['hop1']['ranked'][0], w) if rec['hop1']['ranked'] else None
    e['hop1_rank_first'] = (rec['hop1']['ranked'].index(first) + 1) if first in rec['hop1']['ranked'] else None
    e['hop1_roles'] = [role834(c, w) for c in rec['hop1']['ranked'][:5]]
    e['rank815_top_role'] = role834(rec['hop1_815'][0], w) if rec['hop1_815'] else None
    e['rank815_rank_first'] = (rec['hop1_815'].index(first) + 1) if first in rec['hop1_815'] else None
    for mode in ('TOP2', 'B', 'C', 'D', 'E'):
        K = rec[mode]['K']; stop = rec[mode].get('stop_kind', 'STATIC')
        ends = endpoints834(K, w)
        ok = ends == EXPECT834[cond] and stop not in SAFETY834
        req = [w['ids'][k] for k in REQUIRED834[cond]]
        chain = chain_cards834(K, w)
        e[mode] = {'K_roles': [role834(c, w) for c in K], 'endpoints': ends, 'correct': bool(ok), 'stop_kind': stop,
                   'size': len(K), 'required_all_in_K': bool(req) and all(c in K for c in req),
                   'extra_cards': len([c for c in K if c not in chain]),
                   'exact': bool(ok) and all(c in chain for c in K)}
        if mode in ('B', 'D', 'E'):
            e[mode]['tries'] = [{'step': tr['step'], 'role': role834(tr['candidate'], w), 'uptake': tr['uptake']}
                                for tr in rec[mode]['tries']]
            e[mode]['rejected_roles'] = [role834(c, w) for c in rec[mode]['rejected']]
    e['C_addr_roles'] = [[role834(c, w) for c in s['addr_top'][:1]] for s in rec['C']['steps']]
    e['C_addr_changed'] = len({tuple(s['addr_top'][:1]) for s in rec['C']['steps']}) > 1
    e['C_stable_but_incomplete'] = rec['C']['stop_kind'] not in SAFETY834 and cond in COMPLETE834
    e['D_vs_B_hidden_dist'] = rec['D_vs_B_same_mount_hidden_dist']
    e['A_legacy833'] = {o: {'decision': rec['A_' + o]['legacy833']['decision'],
                            'top_roles': [role834(c, w) for c in rec['A_' + o]['legacy833']['top']]} for o in ('FWD', 'REV')}
    e['A_lock_argmax_role'] = {o: role834(rec['A_' + o]['lock']['argmax_card'], w) for o in ('FWD', 'REV')}
    df = rec['D_final']
    e['D_final_argmax_role'] = role834(df['lock']['argmax_card'], w) if df['lock']['argmax_card'] else None
    e['D_final_features'] = df['features']
    if 'reversal' in df:
        e['D_reversal'] = {'hidden_cosdist': df['reversal']['hidden_cosdist'], 'argmax_same': df['reversal']['argmax_same']}
    if 'loo' in df:
        chain = chain_cards834(rec['D']['K'], w)
        e['D_loo'] = [{'role': role834(x['removed'], w), 'on_chain': x['removed'] in chain, 'hidden_cosdist': x['hidden_cosdist'],
                       'jsd': x['jsd'], 'top1_same': x['top1_same']} for x in df['loo']]
    e['text'] = {}
    for mode, tx in rec['text'].items():
        if tx is None:
            e['text'][mode] = None; continue
        cls = text_class834(tx['text'], w)
        e['text'][mode] = {'classes': cls, 'correct': text_correct834(cls, cond)}
    EV834.append(e)
D829['offline_eval834'] = EV834

def cnt834(pred):
    return sum(1 for e in EV834 if pred(e))
def frac_ok834(k, n, need, minimum):
    return 'INCONCLUSIVE' if n < minimum else ('PASS' if k >= need * n - 1e-12 else 'FAIL')
NRUN834 = len(EV834)
corr834 = {m: cnt834(lambda e, m=m: e[m]['correct']) for m in ('TOP2', 'B', 'C', 'D', 'E')}
by_cond834 = {m: {c: [cnt834(lambda e, m=m, c=c: e['condition'] == c and e[m]['correct']),
                      cnt834(lambda e, c=c: e['condition'] == c)] for c in CONDS834} for m in ('TOP2', 'B', 'C', 'D', 'E')}
# C1
fp834 = [e for e in EV834 if e['first_in_bank']]
c1n834 = sum(e['hop1_top_role'] == 'OWN_FIRST' for e in fp834)
C1_834 = 'PASS' if c1n834 >= 20 and len(fp834) == 30 else ('FAIL' if len(fp834) == 30 else 'INCONCLUSIVE')
# C2
cp834 = [e for e in EV834 if e['condition'] in COMPLETE834]
c2n834 = sum(e['D']['required_all_in_K'] for e in cp834)
C2_834 = 'PASS' if c2n834 >= 18 and len(cp834) == 24 else ('FAIL' if len(cp834) == 24 else 'INCONCLUSIVE')
# C3
c3ev834 = [e for e in cp834 if e['D']['required_all_in_K'] and 'D_loo' in e and 'D_reversal' in e]
def c3ok834(e):
    need = [x for x in e['D_loo'] if x['role'].startswith('OWN_') and x['role'][4:].lower() in REQUIRED834[e['condition']]]
    rest = [x['hidden_cosdist'] for x in e['D_loo'] if x not in need]
    ref = max(rest + [e['D_reversal']['hidden_cosdist']])
    return bool(need) and all(x['hidden_cosdist'] > ref for x in need)
c3n834 = sum(c3ok834(e) for e in c3ev834)
C3_834 = frac_ok834(c3n834, len(c3ev834), 0.8, 6)
# C4
c4ev834 = [e for e in fp834 if e['hop1_top_role'] != 'OWN_FIRST']
c4n834 = sum(e['D']['correct'] and 'OWN_FIRST' in e['D']['K_roles'] for e in c4ev834)
C4_834 = frac_ok834(c4n834, len(c4ev834), 0.5, 3)
# C5
ms834 = [e for e in EV834 if e['condition'] in MISSING834]
def abst834(e, m):
    return e[m]['correct'] and e[m]['size'] == 1
c5n834 = sum(abst834(e, 'D') for e in ms834)
C5_834 = 'PASS' if c5n834 >= 10 and len(ms834) == 12 else ('FAIL' if len(ms834) == 12 else 'INCONCLUSIVE')
# C6 (evidence availability only; declaration unimplemented)
cf834 = [e for e in EV834 if e['condition'] == 'CONFLICT_ALT_ADDED']
c6n834 = sum(e['D']['endpoints'] == ['ALT_END', 'END'] for e in cf834)
# C7
fu834 = [e for e in EV834 if e['condition'] == 'FULL']; ow834 = [e for e in EV834 if e['condition'] == 'OWN_ONLY']
c7a834 = sum(e['D']['correct'] for e in fu834) >= 4 and sum(e['D']['correct'] for e in fu834) >= sum(e['D']['correct'] for e in ow834) - 1
c7ev834 = [e for e in EV834 if 'D_reversal' in e]
c7bn834 = sum(e['D_reversal']['argmax_same'] for e in c7ev834)
c7b834 = frac_ok834(c7bn834, len(c7ev834), 0.8, 6)
C7_834 = 'INCONCLUSIVE' if c7b834 == 'INCONCLUSIVE' and c7a834 else ('PASS' if c7a834 and c7b834 == 'PASS' else 'FAIL')
# C8
dbw834 = [e for e in EV834 if e['D']['correct'] and not e['B']['correct']]
c8a834 = corr834['D'] >= max(corr834['B'], corr834['C'], corr834['TOP2']) + 3
c8b834 = corr834['E'] <= corr834['D'] - 3
c8c834 = len(dbw834) >= 3 and sum(not e['E']['correct'] for e in dbw834) >= 0.5 * len(dbw834)
C8_834 = 'PASS' if c8a834 and c8b834 and c8c834 else 'FAIL'
# C9
c9a834 = all(e['D']['stop_kind'] not in SAFETY834 for e in EV834 if e['D']['correct'])
pairs9_834 = []
for wi in range(len(worlds829)):
    fF = [e for e in EV834 if e['world'] == wi and e['condition'] == 'FULL']
    fM = [e for e in EV834 if e['world'] == wi and e['condition'] == 'MISSING_SECOND']
    if fF and fM:
        pairs9_834.append(fF[0]['D']['size'] > fM[0]['D']['size'])
c9b834 = len(pairs9_834) == len(worlds829) and sum(pairs9_834) >= 5
C9_834 = 'PASS' if c9a834 and c9b834 else 'FAIL'
CRIT834 = {'C1_BLIND_FIRST_DISCOVERY': C1_834, 'C2_MULTI_MEMORY_SELECTION': C2_834, 'C3_CAUSAL_DEPENDENCE': C3_834,
           'C4_CORRECTION': C4_834, 'C5_ABSTENTION_MISSING': C5_834, 'C6_CONTRADICTION': 'UNIMPLEMENTED',
           'C7_ROBUSTNESS': C7_834, 'C8_RECURRENCE_IMPROVEMENT': C8_834, 'C9_STOPPING': C9_834}
# Offline native sufficiency signal test (calibrated stump; external readout)
def stump_apply834(f, x):
    s = STUMP834[f]
    return None if (x is None or s['threshold'] is None) else bool(s['sign'] * (x - s['threshold']) > 0)
suf834 = {}
for f in FEATS834:
    pos = [stump_apply834(f, e['D_final_features'][f]) for e in EV834 if e['D']['endpoints']]
    neg = [stump_apply834(f, e['D_final_features'][f]) for e in EV834 if not e['D']['endpoints']]
    pos = [x for x in pos if x is not None]; neg = [x for x in neg if x is not None]
    bal = (0.5 * (np.mean(pos) + np.mean([not x for x in neg]))) if pos and neg else None
    suf834[f] = {'eval_complete_n': len(pos), 'eval_incomplete_n': len(neg), 'eval_balanced_acc': bal,
                 'true_positive': int(sum(pos)), 'true_negative': int(sum(not x for x in neg))}
sel834 = suf834[STUMPSEL834]
SUFF834 = ('INCONCLUSIVE' if sel834['eval_balanced_acc'] is None or min(sel834['eval_complete_n'], sel834['eval_incomplete_n']) < 4
           else ('SIGNAL_TRANSFERS_EXTERNAL_READOUT' if sel834['eval_balanced_acc'] >= 0.8 else 'NO_TRANSFERABLE_SIGNAL'))
central834 = C2_834 == 'PASS' and C5_834 == 'PASS' and C8_834 == 'PASS' and C9_834 == 'PASS'
if BUDGET_STOP834:
    verdict834 = 'INCONCLUSIVE'
elif C8_834 == 'FAIL' or corr834['D'] < 12:
    verdict834 = 'FAIL'
elif central834 and C1_834 == 'PASS' and C3_834 == 'PASS' and C7_834 == 'PASS' and C4_834 in ('PASS', 'INCONCLUSIVE'):
    verdict834 = 'PASS'
else:
    verdict834 = 'INCONCLUSIVE'
def mean834(xs):
    xs = [x for x in xs if x is not None]
    return float(np.mean(xs)) if xs else None
D829['report834'] = {
    'raw_counts': {
        'runs': NRUN834, 'correct_evidence_state': corr834, 'by_condition': by_cond834,
        'C1_hop1_first_top1': [c1n834, len(fp834)],
        'hop1_815_first_top1': [sum(e['rank815_top_role'] == 'OWN_FIRST' for e in fp834), len(fp834)],
        'hop1_top_roles': {r_: sum(e['hop1_top_role'] == r_ for e in EV834) for r_ in sorted({e['hop1_top_role'] for e in EV834 if e['hop1_top_role']})},
        'calibration_hop1_first_top1_separate_worlds': [sum(x['top1_is_first'] for x in CALHOP1_834), len(CALHOP1_834)],
        'C2_required_links_in_K_D': [c2n834, len(cp834)],
        'required_links_in_K': {m: sum(e[m]['required_all_in_K'] for e in cp834) for m in ('TOP2', 'B', 'D', 'E')},
        'C3_dependence': [c3n834, len(c3ev834)], 'C4_correction': [c4n834, len(c4ev834)],
        'C5_missing_abstention_state': {m: sum(abst834(e, m) for e in ms834) for m in ('TOP2', 'B', 'C', 'D', 'E')},
        'missing_no_false_chain_nonsafety': {m: sum(e[m]['correct'] for e in ms834) for m in ('TOP2', 'B', 'C', 'D', 'E')},
        'C6_conflict_both_endpoints_in_K': {m: sum(e[m]['endpoints'] == ['ALT_END', 'END'] for e in cf834) for m in ('TOP2', 'B', 'D', 'E')},
        'C7_full_vs_own_D': [sum(e['D']['correct'] for e in fu834), sum(e['D']['correct'] for e in ow834)],
        'C7_reversal_argmax_same': [c7bn834, len(c7ev834)],
        'C8_D_correct_B_wrong_E_wrong': [sum(not e['E']['correct'] for e in dbw834), len(dbw834)],
        'C9_full_gt_missing_second_size': [int(sum(pairs9_834)), len(pairs9_834)]},
    'stage1_addressing': {
        'hop1_rank_first_mean': mean834([e['hop1_rank_first'] for e in fp834]),
        'second_after_first_D': sum(1 for e in cp834 if 'OWN_FIRST' in e['D']['K_roles'] and any(x in e['D']['K_roles'] for x in ('OWN_SECOND', 'OWN_CHANGED'))),
        'false_uptakes': {m: sum(e[m]['extra_cards'] for e in EV834) for m in ('B', 'D', 'E')},
        'accepted_roles': {m: {r_: sum(1 for e in EV834 for t_ in e[m]['tries'] if t_['uptake'] and t_['role'] == r_)
                               for r_ in sorted({t_['role'] for e in EV834 for t_ in e[m]['tries']})} for m in ('B', 'D', 'E')},
        'rejected_roles': {m: {r_: sum(1 for e in EV834 for t_ in e[m]['tries'] if not t_['uptake'] and t_['role'] == r_)
                               for r_ in sorted({t_['role'] for e in EV834 for t_ in e[m]['tries']})} for m in ('B', 'D', 'E')},
        'A_order_argmax_same': sum(e['A_lock_argmax_role']['FWD'] == e['A_lock_argmax_role']['REV'] for e in EV834)},
    'stage2_native_memory_interaction': {
        'loo_chain_mean_hidden_cosdist': mean834([x['hidden_cosdist'] for e in EV834 for x in e.get('D_loo', []) if x['on_chain']]),
        'loo_offchain_mean_hidden_cosdist': mean834([x['hidden_cosdist'] for e in EV834 for x in e.get('D_loo', []) if not x['on_chain']]),
        'reversal_mean_hidden_cosdist': mean834([e['D_reversal']['hidden_cosdist'] for e in EV834 if 'D_reversal' in e]),
        'D_final_argmax_on_endpoint_card': sum(e['D_final_argmax_role'] in ('OWN_SECOND', 'OWN_CHANGED') for e in cp834),
        'text_correct': {m: sum(1 for e in EV834 if e['text'].get(m) and e['text'][m]['correct']) for m in ('A', 'NULL', 'TOP2', 'B', 'D', 'E')},
        'text_correct_by_condition': {m: {c: sum(1 for e in EV834 if e['condition'] == c and e['text'].get(m) and e['text'][m]['correct'])
                                          for c in CONDS834} for m in ('A', 'TOP2', 'D')}},
    'stage3_recursion': {
        'D_vs_B_same_mount_hidden_dist_positive': [sum(1 for e in EV834 for x in e['D_vs_B_hidden_dist'] if x > 0),
                                                   sum(len(e['D_vs_B_hidden_dist']) for e in EV834)],
        'D_path_differs_from_B': sum(e['D']['K_roles'] != e['B']['K_roles'] for e in EV834),
        'E_path_differs_from_D': sum(e['E']['K_roles'] != e['D']['K_roles'] for e in EV834),
        'C_address_changed_under_recurrence': sum(e['C_addr_changed'] for e in EV834),
        'C_last_address_is_own_second': sum(e['C_addr_roles'][-1][:1] == ['OWN_SECOND'] for e in EV834 if e['C_addr_roles']),
        'C_first_address_is_own_second': sum(e['C_addr_roles'][0][:1] == ['OWN_SECOND'] for e in EV834 if e['C_addr_roles']),
        'C_stop_kinds': {k_: sum(e['C']['stop_kind'] == k_ for e in EV834) for k_ in sorted({e['C']['stop_kind'] for e in EV834})},
        'C_stable_but_incomplete': sum(e['C_stable_but_incomplete'] for e in EV834)},
    'stage4_evidence_control': {m: {
        'sufficient_recognised_complete': sum(e[m]['correct'] for e in cp834),
        'missing_recognised_abstention_state': sum(abst834(e, m) for e in ms834),
        'false_sufficiency_evidence_chain': sum(bool(e[m]['endpoints']) for e in ms834),
        'false_continuation_missing': sum(e[m]['size'] > 1 for e in ms834),
        'false_sufficiency_text': sum(1 for e in ms834 if e['text'].get(m) and any(x in e['text'][m]['classes'] for x in ('END', 'ALT_END'))),
        'false_contradiction': sum(len(e[m]['endpoints']) >= 2 for e in EV834 if e['condition'] != 'CONFLICT_ALT_ADDED'),
        'unnecessary_continuation_extra_cards': sum(e[m]['extra_cards'] for e in EV834),
        'premature_termination': sum((not e[m]['endpoints']) and e[m]['stop_kind'] not in SAFETY834 for e in cp834),
        'correct_abstention_text': sum(1 for e in ms834 if e['text'].get(m) and e['text'][m]['correct'])} for m in ('TOP2', 'B', 'D', 'E')},
    'native_declarations': {'sufficiency': 'UNIMPLEMENTED', 'contradiction': 'UNIMPLEMENTED', 'abstention': 'UNIMPLEMENTED',
                            'stop': 'EXTERNAL_UPTAKE_INTERFACE', 'selection': 'EXTERNAL_FIXED_ADDRESS_RULE_ON_NATIVE_ROWS'},
    'sufficiency_signal_offline': {'per_feature': suf834, 'selected_on_calibration': STUMPSEL834, 'result': SUFF834,
                                   'label': 'EXTERNAL calibrated readout of native numbers; not model-internal'},
    'stage5_stopping': {m: {'stop_kinds': {k_: sum(e[m]['stop_kind'] == k_ for e in EV834) for k_ in sorted({e[m]['stop_kind'] for e in EV834})},
                            'mean_size_complete': mean834([e[m]['size'] for e in cp834]),
                            'mean_size_missing': mean834([e[m]['size'] for e in ms834]),
                            'safety_stops': sum(e[m]['stop_kind'] in SAFETY834 for e in EV834)} for m in ('B', 'D', 'E')},
    'legacy833_on_A': {'decision_correct_like_833': sum(
        (e['A_legacy833']['FWD']['decision'] == ('INCOMPLETE' if e['condition'] in MISSING834 else
                                                 'CONFLICT' if e['condition'] == 'CONFLICT_ALT_ADDED' else 'SUFFICIENT')) for e in EV834),
        'order_consistent': sum(e['A_legacy833']['FWD']['decision'] == e['A_legacy833']['REV']['decision'] for e in EV834)},
    'hypotheses_1_to_8_evidence': {
        'H1_addressing_not_discriminative': {'hop1_first_top1': [c1n834, len(fp834)], 'hop1_top_roles_for_first_present':
            {str(r_): sum(e['hop1_top_role'] == r_ for e in fp834) for r_ in {e['hop1_top_role'] for e in fp834}}},
        'H2_attention_mass_not_evidential': {'A_lock_argmax_roles': {str(r_): sum(e['A_lock_argmax_role']['FWD'] == r_ for e in EV834)
                                                                     for r_ in {e['A_lock_argmax_role']['FWD'] for e in EV834}},
                                             'A_legacy833_top_roles': {str(r_): sum(r_ in e['A_legacy833']['FWD']['top_roles'] for e in EV834)
                                                                       for r_ in {x for e in EV834 for x in e['A_legacy833']['FWD']['top_roles']}}},
        'H3_state_lacks_unresolved_need': 'see stage3: D_path_differs_from_B and C8 counts',
        'H4_repetition_no_new_search': 'see stage3: C_address_changed_under_recurrence',
        'H5_no_uncertainty_to_address': 'see stage1: second_after_first_D, accepted/rejected roles',
        'H6_external_readout': 'structural: selection/acceptance/stop are external interfaces in TEST834 as well',
        'H7_stop_detects_stability': 'see stage3: C_stable_but_incomplete and C_stop_kinds',
        'H8_fusion_loses_roles': 'see C6 counts and D_final_argmax_on_endpoint_card'},
    'integrity': {'probe_equivalence': D829['probe_equivalence834'],
                  'step1_deterministic_all': all(r_.get('step1_deterministic', True) for r_ in D829['runs834']),
                  'rope_roundtrip_max_abs': max([r_.get('rope_roundtrip_max_abs', 0.0) for r_ in D829['runs834']] or [0.0]),
                  'rotation_value_norm_rel_err_max': max([r_['E'].get('rotation_value_norm_rel_err') or 0.0 for r_ in D829['runs834']] or [0.0]),
                  'rotation_keys_unchanged_all': all(r_['E'].get('rotation_keys_unchanged', True) is not False for r_ in D829['runs834'])}}
D829['capabilities834'] = {
    'engineering_integrity': 'PASS (all gates passed; any failure raises before this line)',
    'numerical_causality_recurrence': ('DEMONSTRATED' if D829['report834']['stage3_recursion']['D_vs_B_same_mount_hidden_dist_positive'][0] > 0
                                       else 'NOT_DEMONSTRATED'),
    'blind_memory_discovery': C1_834, 'multi_memory_selection': C2_834, 'causal_dependence': C3_834,
    'autonomous_correction': C4_834, 'evidence_sufficiency_state': C5_834, 'contradiction_recognition': 'UNIMPLEMENTED',
    'robustness': C7_834, 'recurrence_attributable_improvement': C8_834, 'stopping_linked_to_sufficiency': C9_834,
    'native_sufficiency_declaration': 'UNIMPLEMENTED', 'native_abstention_declaration': 'UNIMPLEMENTED',
    'native_stop_declaration': 'UNIMPLEMENTED (stop = EXTERNAL_UPTAKE_INTERFACE)',
    'offline_sufficiency_signal': SUFF834}
D829['verdict834'] = {'verdict': verdict834, 'criteria': CRIT834, 'central_H834': central834, 'budget_stop': BUDGET_STOP834,
                      'correct_evidence_state': corr834, 'runs': NRUN834,
                      'interpretation_guard': ('Trajectory differences, convergence and attention mass never count as success. '
                                               'Selection, acceptance and stopping are an external interface acting on native '
                                               'numbers. UNIMPLEMENTED capabilities are not counted.')}
D829['claims_ledger834'] = dict(CLAIMS834, demonstrated_by_TEST834={
    'source': 'this run only', 'verdict': verdict834, 'criteria': CRIT834, 'capabilities': D829['capabilities834'],
    'correct_evidence_state_counts': corr834, 'runs': NRUN834})
D829['cost834'] = {'counted_numeric': COUNT_NUMERIC834, 'counted_calibration_phase': COUNT_CAL834,
                   'counted_total_including_offline': dict(COUNT834), 'predicted_upper': POST834,
                   'numeric_seconds_eval': D829['numeric_seconds834'], 'total_seconds_body': round(time.perf_counter() - T0_834, 3),
                   'peak_gpu_gib': float(_torch829.cuda.max_memory_allocated()) / 2**30}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f834:
    wr834 = csv.DictWriter(f834, fieldnames=['world', 'condition', 'hop1', 'TOP2', 'B', 'C', 'D', 'E', 'D_stop', 'text_A', 'text_D'])
    wr834.writeheader()
    for e in EV834:
        wr834.writerow({'world': e['world'], 'condition': e['condition'], 'hop1': e['hop1_top_role'],
                        'TOP2': ('OK ' if e['TOP2']['correct'] else 'NO ') + ' '.join(e['TOP2']['K_roles']),
                        'B': ('OK ' if e['B']['correct'] else 'NO ') + ' '.join(e['B']['K_roles']),
                        'C': ('OK ' if e['C']['correct'] else 'NO ') + ' '.join(e['C']['K_roles']),
                        'D': ('OK ' if e['D']['correct'] else 'NO ') + ' '.join(e['D']['K_roles']),
                        'E': ('OK ' if e['E']['correct'] else 'NO ') + ' '.join(e['E']['K_roles']),
                        'D_stop': e['D']['stop_kind'] + '@' + str(e['D']['size']),
                        'text_A': ' '.join(e['text']['A']['classes']) if e['text'].get('A') else '',
                        'text_D': ' '.join(e['text']['D']['classes']) if e['text'].get('D') else ''})
D829['status'] = 'COMPLETE_TEST834_EVALUATED' if not BUDGET_STOP834 else 'STOPPED_BUDGET_PARTIAL_EVALUATED'
save829()
log829('TEST834_EVAL', json.dumps([{'w': e['world'], 'c': e['condition'], 'hop1': e['hop1_top_role'],
                                    **{m: [e[m]['correct'], e[m]['K_roles'], e[m]['stop_kind']] for m in ('TOP2', 'B', 'C', 'D', 'E')}}
                                   for e in EV834]))
log829('TEST834_REPORT', json.dumps(D829['report834'], default=str))
log829('TEST834_CAPABILITIES', json.dumps(D829['capabilities834']))
log829('TEST834_COST', json.dumps(D829['cost834'], default=str))
log829('TEST834_VERDICT', json.dumps(D829['verdict834']))
log829('TEST834_SUMMARY', json.dumps({'verdict': verdict834, 'correct_evidence_state': corr834,
                                       'hop1_first_top1': [c1n834, len(fp834)], 'required_links_in_K_D': [c2n834, len(cp834)],
                                       'abstention_state_D': [c5n834, len(ms834)], 'lock': [LOCKSP834, int(LOCKL834), int(LOCKH834)],
                                       'offline_sufficiency_signal': SUFF834}))
log829('TEST834_COMPLETED', str(OUT829))
'''
BODY_SHA834 = hashlib.sha256(BODY834.encode()).hexdigest()
PANEL_HOOK834 = ("PANEL829['test834'] = {'runs': RUNS834, 'calibration_jobs': CALJOBS834, 'eval_store': EVALSTORE834, "
                 "'cal_store': CALSTORE834, 'hypotheses': %r, 'body_sha256': %r, 'constants': %r, 'seed': SEED829}\n"
                 % (HYP834, BODY_SHA834, {'beta': BETA834, 'peak_a': PEAK_A834, 'pca_rank': PCA_RANK834,
                                          'token_k': TOKEN_K834, 'budget': BUDGET834, 'b_try': B_TRY834,
                                          't_accept_max': T_ACCEPT_MAX834, 't_max_c': T_MAX_C834,
                                          'deep_layers_legacy': list(DEEP_LAYERS834), 'spaces': list(SPACES834),
                                          'max_new_text': MAX_NEW_TEXT834, 'conditions': list(CONDS834)}))
src834 = patch834(src834, "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))",
                  PANEL_HOOK834 + "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))")
OFFLINE_HOOK834 = r'''
OFFLINE834 = DIR829 / 'TEST834_offline_key.json'   # never read by any runtime computation
OFFLINE834.write_text(json.dumps({'note': 'OFFLINE ONLY — run conditions, world roles and card kinds', 'runs': RUNKEY834,
                                  'worlds': worlds829, 'calibration_worlds': CALW834, 'questions': questions829,
                                  'card_meta': card_meta829}, ensure_ascii=False, indent=2), encoding='utf-8')
D829['offline_key834_sha256'] = sha829(OFFLINE834.read_bytes())
'''
src834 = patch834(src834, "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n",
                  "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n" + OFFLINE_HOOK834)
start834 = src834.index("    # RUN ORDER: integrity checks")
start834 = src834.rfind("    # ---", 0, start834)
end834 = src834.index("except BaseException as e:\n    D829['status'] = 'ERROR'", start834)
replacement834 = "\n".join("    " + line if line else "" for line in BODY834.strip("\n").splitlines()) + "\n"
patched834 = src834[:start834] + replacement834 + src834[end834:]
ast.parse(patched834)
print('TEST834_SOURCE_LOCK_VERIFIED', LOCK834)
print('TEST834_BODY_SHA256', BODY_SHA834)
print('TEST834_PATCHED_SOURCE_AST_PASS', len(patched834), hashlib.sha256(patched834.encode()).hexdigest())
exec(compile(patched834, 'TEST834_LOCKED_ENGINE', 'exec'), globals())
