# AKBASCORE SILICON HIPPOCAMPUS — TEST835, single Colab cell (one A100-SXM4-80GB, frozen Qwen2.5-72B-Instruct NF4).
# INTEGRATED EXPERIMENT: NATIVE ATTENTION ADDRESSING OVER THE MOUNTED PHYSICAL BANK + NATIVE KV FEEDBACK + CALIBRATED
# SUFFICIENCY / CONTRADICTION GATES + FIXED EXTERNAL SEARCH SCHEDULE, WITH NEGATIVE CONTROLS AND SHA-VERIFIED RESUME.
#
# Why this design (from the GPU-completed TEST834 run, 834.log git blob d468f3d3, panel SHA 435d97cb reproduced offline):
#   * MAM PEAK50 hop-1 on 72B CUT3 rows: own first link top-1 in 15/30 runs; fork 14, decoy 7 -> direction/endpoint blind.
#   * The pointer readout (one head x stored native rows of the mounted first card) did not address the second link
#     (calibration in-sample 2/12); the uptake interface correctly refused the proposed cards, so B and D ended with
#     a single card in 30/36 runs each. Recurrence had nothing to act on: the missing transition was ADDRESS GENERATION.
# TEST835 therefore tests the closest native alternative: let the frozen model itself attend over the WHOLE mounted
# physical bank and read the address from calibrated attention heads (first head; second head per feedback condition),
# with the TEST833/834 KV state of "having read card c1" fed back natively.
#
# DECISION-MECHANISM CLASSES (reported for every decision):
#   A  = signal produced directly by the frozen model (attention probabilities, KV state, hidden state, next-token law)
#   B  = predeclared numerical gate on an A signal (argmax over cards; one-feature stump fitted on calibration worlds)
#   C  = Python schedule/decision (try at most 2 second candidates, revise the first once, check one extra card for
#        conflict, declare INSUFFICIENT when the schedule is exhausted)
# Physical mounting of the card chosen by an A+B address is EXECUTION, not a decision; the schedule itself is class C.
# No language enters any runtime computation; answer text is generated only after all numerical work (offline).
# No GPU execution or result is claimed by the code author.
import urllib.request, hashlib, ast, json, time, random, math, re, numpy as np

REPO835 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
LOCK829_835 = "a5a25460a3a6bbdf62a0571a9b5ff19e64159cf7"      # locked TEST829 source (wraps the TEST815 engine)
LOCK834_835 = "ab7b2046d7b7e7be18aed8c6ce5a1397e0c991d7"      # GPU-completed TEST834 source (helpers reused verbatim)
LOCK834LOG_835 = "d468f3d3963f7b7d752c0388fe06999d8b7c2fd2"   # TEST834 GPU log (prior evidence, read-only)
SEED835 = 8352026
EXPECTED_ARCH834 = (80, 8192, 64, 8, 128)
DEVICE_KIND835 = 'cuda'
WORLDS_EVAL835 = 6
CAL_WORLDS835 = 12
BLOCK835 = 3
CONDS835 = ('FULL', 'MISSING_FIRST', 'MISSING_SECOND', 'REPLACE_SECOND_BY_ALT', 'CONFLICT_ALT_ADDED', 'MISLEAD_FIRST')
STATES835 = ('OFF', 'FEEDBACK', 'PERTURBED', 'NEG_CONTROL')   # state fed into the second-address forward
R2_835 = 2                    # class C: second-address candidates tried per first candidate
R1_835 = 2                    # class C: first-address candidates (1 = no revision; 2 = one revision)
SPACES834 = ('H3',)           # MAM baseline space (TEST834 helpers)
BETA834, PEAK_A834, PCA_RANK834, TOKEN_K834, BUDGET834 = 8.0, 0.5, 128, 16, 16
MAX_NEW_TEXT835 = 10
SEC_FUSION835, SEC_PROBE835 = 0.6, 0.9
PRED_LIMIT_MIN835 = 240.0
HARD_BUDGET_MIN835 = 300.0
RESUME835 = True              # resume from a SHA-verified checkpoint of an identical earlier TEST835 run, if present

def fetch835(name, lock, limit=400000):
    with urllib.request.urlopen(urllib.request.Request(REPO835 + name, headers={"User-Agent": "AKBASCORE-TEST835"}),
                                timeout=180) as f:
        raw = f.read(limit + 1)
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert len(raw) <= limit and blob == lock, ("STOP_SOURCE_CHANGED", name, blob)
    return raw

raw829_835 = fetch835("829.py", LOCK829_835)
raw834_835 = fetch835("834.py", LOCK834_835)
raw834log_835 = fetch835("834.log", LOCK834LOG_835)
src835 = raw829_835.decode("utf-8")
SOURCE_LINE835 = 'TEST835_SOURCE_LOCKS_VERIFIED %s %s %s' % (LOCK829_835, LOCK834_835, LOCK834LOG_835)

# ---- reuse of GPU-verified TEST834 helpers: extracted by AST from the locked 834.py, never retyped ----
tree834_835 = ast.parse(raw834_835.decode("utf-8"))
body834_835 = [n for n in tree834_835.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'BODY834']
assert len(body834_835) == 1, 'BODY834_NOT_UNIQUE'
BODY834_TEXT835 = body834_835[0].value.value
HELPERS835 = ('unit834', 'fit_store834', 'lse834', 'address834', 'apply_vec834', 'HeadProbe834', 'concat834', 'rprobe834',
              'relocate834', 'rotate834', 'seal834', 'mount834', 'cspans834', 'card_mass834', 'core_span834',
              'question_rows834', 's0_834', 'stump_fit834')
tb834_835 = ast.parse(BODY834_TEXT835)
nodes834_835 = [n for n in tb834_835.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in HELPERS835]
assert sorted(n.name for n in nodes834_835) == sorted(HELPERS835), 'HELPER_SET_MISMATCH'
HELPER_SRC835 = "\n\n".join(ast.get_source_segment(BODY834_TEXT835, n) for n in nodes834_835)
HELPER_SHA835 = hashlib.sha256(HELPER_SRC835.encode()).hexdigest()

def patch835(text, old, new):
    assert text.count(old) == 1, ("PATCH_ANCHOR_NOT_UNIQUE", old[:80], text.count(old))
    return text.replace(old, new, 1)

src835 = patch835(src835, "SEED829 = 8292026", "SEED829 = %d" % SEED835)
src835 = patch835(src835, "RUN829 = 'TEST829_'", "RUN829 = 'TEST835_'")
src835 = patch835(src835, "WORLDS829 = 3                    # small pilot (directive); no automatic extension",
                  "WORLDS829 = %d                    # TEST835 sealed evaluation worlds" % WORLDS_EVAL835)
for a835, b835 in (("'TEST829_results.json'", "'TEST835_results.json'"), ("'TEST829.log'", "'TEST835.log'"),
                   ("'TEST829_blind_review.csv'", "'TEST835_run_table.csv'"),
                   ("'TEST829_offline_key.json'", "'TEST829_base_offline_key.json'")):
    src835 = patch835(src835, a835, b835)

PANEL_EXT835 = r'''
# ---------------- TEST835 PANEL EXTENSION (sealed before any model call) ----------------
def fresh835():
    while True:
        c = code829()
        if c not in seen829:
            seen829.add(c); return c
def card835(domain, a, b, extra=''):
    return 'Evidence record. Domain: ' + domain + '\n' + 'Directed relation: ' + a + ' -> ' + b + '.\n' + extra
for w in worlds829:
    w['fork_end'] = fresh835(); w['lure_end'] = fresh835()
    for kind in ('mirror', 'fork', 'lure'):
        cid = 'E829_' + code829()
        assert cid not in cards829, 'CARD_ID_COLLISION'
        w['ids'][kind] = cid
    cards829[w['ids']['mirror']] = card835(w['world'], w['end'], w['middle'])
    cards829[w['ids']['fork']] = card835(w['world'], w['start'], w['fork_end'])
    # lexical lure: an alternative first hop that repeats the start node (unseen during calibration)
    cards829[w['ids']['lure']] = card835(w['world'], w['start'], w['lure_end'], 'Record subject: ' + w['start'] + '.\n')
    for kind in ('mirror', 'fork', 'lure'):
        card_meta829[w['ids'][kind]] = {'domain': w['world'], 'kind': kind, 'body_sha256': sha829(cards829[w['ids'][kind]])}
for cid in list(card_meta829):
    card_meta829[cid]['split'] = 'null' if cid == NULL829 else 'evaluation'
EVALSTORE835 = sorted(c for c in cards829 if c != NULL829)
RNGC835 = random.Random(SEED829 + 835001)
def codec835():
    while True:
        c = ''.join(RNGC835.choice(ALPH829) for _ in range(9))
        if c not in seen829:
            seen829.add(c); return c
CALW835 = []
for ci835 in range(CAL_WORLDS835):
    cw = {'world': 'DOMAIN_' + codec835(), 'start': codec835(), 'middle': codec835(), 'end': codec835(),
          'changed_end': codec835(), 'decoy_end': codec835(), 'fork_end': codec835()}
    cw['ids'] = {}
    for kind, a, b in (('first', 'start', 'middle'), ('second', 'middle', 'end'), ('changed', 'middle', 'changed_end'),
                       ('mirror', 'end', 'middle'), ('decoy', 'decoy_end', 'start'), ('fork', 'start', 'fork_end')):
        cid = 'E829_' + codec835()
        assert cid not in cards829, 'CARD_ID_COLLISION'
        cw['ids'][kind] = cid
        cards829[cid] = card835(cw['world'], cw[a], cw[b])
        card_meta829[cid] = {'domain': cw['world'], 'kind': kind, 'body_sha256': sha829(cards829[cid]), 'split': 'calibration'}
    cw['qid'] = cw['world'] + '_P0'
    cw['question'] = ('In domain {world}, starting from {start}, which endpoint is reached after exactly two directed '
                      'links?').format(**cw)
    CALW835.append(cw)
CALSTORE835 = sorted(c for cw in CALW835 for c in cw['ids'].values())
_rngc835 = random.Random(SEED829 + 835002)
CALBLOCKS835 = []
for bi in range(0, len(CALW835), BLOCK835):
    blk = CALW835[bi:bi + BLOCK835]
    cbank = [cw['ids'][k] for cw in blk for k in ('first', 'second', 'mirror', 'decoy', 'fork')]
    _rngc835.shuffle(cbank)
    nxt = CALW835[(bi + BLOCK835) % len(CALW835):(bi + BLOCK835) % len(CALW835) + BLOCK835]
    jobs = []
    for j, cw in enumerate(blk):
        other = blk[(j + 1) % len(blk)]['ids']['second']
        neg = nxt[j % len(nxt)]['ids']['second']            # card from another calibration bank
        ids = cw['ids']
        jobs.append({'qid': cw['qid'], 'question': cw['question'], 'first': ids['first'], 'second': ids['second'],
                     'neg': neg,
                     'suff_pos': [[ids['first'], ids['second']]],
                     'suff_neg': [[ids['first'], ids['mirror']], [ids['first'], other], [ids['decoy'], ids['first']]],
                     'conf_pos': [[ids['first'], ids['second'], ids['changed']]],
                     'conf_neg': [[ids['first'], ids['second'], other], [ids['first'], ids['second'], ids['mirror']]]})
    CALBLOCKS835.append({'bank': cbank, 'jobs': jobs})
_rng835 = random.Random(SEED829 + 35)
RUNS835, RUNKEY835 = [], {}
assert len(questions829) == len(worlds829), 'ONE_QUESTION_PER_WORLD'
nblk835 = len(worlds829) // BLOCK835
for bi in range(0, len(worlds829), BLOCK835):
    blk = worlds829[bi:bi + BLOCK835]
    fullbank = [w['ids'][k] for w in blk for k in ('first', 'second', 'mirror', 'decoy', 'fork')]
    oblk = worlds829[(bi + BLOCK835) % len(worlds829):(bi + BLOCK835) % len(worlds829) + BLOCK835]
    for w in blk:
        wi = worlds829.index(w)
        neg = _rng835.choice([x['ids'][k] for x in oblk for k in ('first', 'second', 'mirror', 'decoy', 'fork')])
        for cond in CONDS835:
            bank = list(fullbank)
            if cond == 'MISSING_FIRST':
                bank.remove(w['ids']['first'])
            if cond in ('MISSING_SECOND', 'REPLACE_SECOND_BY_ALT'):
                bank.remove(w['ids']['second'])
            if cond in ('CONFLICT_ALT_ADDED', 'REPLACE_SECOND_BY_ALT'):
                bank.append(w['ids']['changed'])
            if cond == 'MISLEAD_FIRST':
                bank.append(w['ids']['lure'])
            _rng835.shuffle(bank)
            tie = list(bank); _rng835.shuffle(tie)
            rid = 'R835_' + ''.join(_rng835.choice('0123456789ABCDEF') for _ in range(12))
            RUNS835.append({'run': rid, 'qid': questions829[wi]['qid'], 'bank': bank, 'tie_order': tie, 'neg': neg})
            RUNKEY835[rid] = {'world': wi, 'block': bi // BLOCK835, 'condition': cond}
_rng835.shuffle(RUNS835)

def fus_upper835(k, maxb, p_):
    if k <= 0:
        return 0
    c = int(globals().get('CHUNK', 128))
    return (p_ + maxb + c - 1) // c + (k - 1) * ((maxb + c - 1) // c)

def cost_upper835(tok_of, p_):
    up = {'fusion_forwards': 0, 'probe_forwards': 0, 'capture_forwards': 0, 'rank_forwards': 0, 'generation_forwards': 0}
    mx = max(tok_of[c] for c in cards829)
    up['fusion_forwards'] += fus_upper835(1, tok_of[NULL829], p_)
    up['probe_forwards'] += len(questions829) + sum(len(b['jobs']) for b in CALBLOCKS835)
    up['fusion_forwards'] += fus_upper835(2, mx, p_); up['probe_forwards'] += 2
    up['fusion_forwards'] += fus_upper835(1, tok_of[NULL829], p_); up['probe_forwards'] += 3; up['generation_forwards'] += 1
    up['capture_forwards'] += len(questions829); up['rank_forwards'] += len(questions829)
    for b in CALBLOCKS835:
        up['fusion_forwards'] += fus_upper835(len(b['bank']), mx, p_)
        for j in b['jobs']:
            up['fusion_forwards'] += 2 * fus_upper835(1, mx, p_) + 4 * fus_upper835(2, mx, p_) + 3 * fus_upper835(3, mx, p_)
            up['probe_forwards'] += 2 + 4 + 7
    for r in RUNS835:
        nb = len(r['bank'])
        up['fusion_forwards'] += 2 * fus_upper835(nb, mx, p_); up['probe_forwards'] += 2       # bank FWD / REV
        up['fusion_forwards'] += (R1_835 + 1) * fus_upper835(1, mx, p_); up['probe_forwards'] += R1_835 + 1
        up['probe_forwards'] += R1_835 * (len(STATES835) - 1)                                 # state forwards on bank
        sets = len(STATES835) * R1_835 * R2_835
        up['fusion_forwards'] += sets * (fus_upper835(2, mx, p_) + fus_upper835(3, mx, p_)); up['probe_forwards'] += 2 * sets
    numeric = dict(up)
    off_f = sum(fus_upper835(len(r['bank']), mx, p_) + len(STATES835) * fus_upper835(3, mx, p_) for r in RUNS835)
    off_f += len(questions829) * fus_upper835(1, tok_of[NULL829], p_)
    off_g = (len(RUNS835) * (1 + len(STATES835)) + len(questions829)) * MAX_NEW_TEXT835
    off_p = len(RUNS835) * 2; off_f += len(RUNS835) * (fus_upper835(len(RUNS835[0]['bank']) + 1, mx, p_) + fus_upper835(1, mx, p_))
    sec = ((numeric['fusion_forwards'] + off_f) * SEC_FUSION835 +
           (numeric['probe_forwards'] + numeric['capture_forwards'] + numeric['rank_forwards'] + off_p) * SEC_PROBE835 +
           (numeric['generation_forwards'] + off_g) * SEC_FUSION835 + 120.0 + len(cards829) * 2.0)
    maxmem = max(p_ + sum(tok_of[c] for c in r['bank']) for r in RUNS835)
    return {'numeric_upper': numeric,
            'offline_upper': {'fusion_forwards': off_f, 'generation_forwards': off_g, 'oracle_probe_forwards': off_p},
            'physical_cartridges': len(cards829),
            'cartridge_disk_mb_estimate': round(sum((p_ + tok_of[c]) * (8192 * 2 + 4 * 2 * 8 * 128 * 2) for c in cards829) / 2**20, 1),
            'max_memory_tokens': maxmem, 'kv_bytes_largest_memory_upper': (maxmem + 2 * 64) * 80 * 2 * 8 * 128 * 2,
            'search_schedule_upper': {'first_candidates': R1_835, 'second_candidates': R2_835, 'state_conditions': len(STATES835)},
            'minutes_upper_excluding_model_load': round(sec / 60.0, 1),
            'peak_vram_gib_expected': 'about 39-42 (TEST834: VRAM headroom 40.05 GiB free after load; 16-card memories)',
            'model_weights': 'loaded once; download/cache time not estimated'}
'''
src835 = patch835(src835,
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n",
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n" + PANEL_EXT835)
PRECOST835 = r'''
    PRE835 = cost_upper835(tok_counts829, 30)
    D829['predicted_cost835_pre_model'] = PRE835
    log829('TEST835_PREDICTED_COST_BEFORE_MODEL_LOAD', json.dumps(PRE835))
    gate829('TEST835_PREDICTED_BUDGET', PRE835['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN835,
            {'minutes_upper': PRE835['minutes_upper_excluding_model_load'], 'limit': PRED_LIMIT_MIN835})
'''
src835 = patch835(src835, "    del tok829\n", "    del tok829\n" + PRECOST835)

HYP835 = {
    'question': ('Can the frozen 72B model, attending over the mounted physical bank, produce the first and the second '
                 'memory address itself, does the native KV state of having read the first memory causally improve the '
                 'second address, and do calibrated gates on native signals recognise sufficiency, missing evidence and '
                 'contradiction well enough for a fixed external schedule to correct, re-search and stop?'),
    'criteria': {
        'K1_FIRST_ADDRESS': 'first-head argmax is the own first link in >= 24 of the 30 first-present runs.',
        'K2_SECOND_ADDRESS': ('with the own first link as c1 (>= 8 evaluable complete runs, else INCONCLUSIVE), the '
                              'FEEDBACK second-head argmax over the other cards is a valid second link (second, or the '
                              'alternative when present) in >= 75%.'),
        'K3_FEEDBACK_CAUSAL': ('on the same evaluable runs FEEDBACK second-address hits >= OFF + 3, >= PERTURBED + 3 and '
                               '>= NEG_CONTROL + 3; otherwise FAIL (INCONCLUSIVE if < 8 evaluable).'),
        'K4_MISSING': ('FEEDBACK schedule ends INSUFFICIENT in >= 10 of 12 missing-evidence runs AND reaches a correct '
                       'non-INSUFFICIENT terminal state in >= 12 of 24 complete-evidence runs (rules out always-UNKNOWN).'),
        'K5_CONTRADICTION': 'CONFLICT terminal state in >= 5 of 6 CONFLICT runs and in <= 2 of the 30 other runs (FEEDBACK).',
        'K6_CORRECTION': ('among complete runs whose first c1 is wrong (>= 3, else INCONCLUSIVE) the FEEDBACK terminal state '
                          'is correct in >= 50%.'),
        'K7_RESEARCH': ('among complete runs with correct c1 but a wrong first second-candidate (>= 3, else INCONCLUSIVE) '
                        'the FEEDBACK terminal state is correct in >= 50%.'),
        'K8_STOPPING': ('FEEDBACK terminal decision correct in >= 24 of 36 runs, with stop types reported separately: '
                        'correct stop, premature stop (SUFFICIENT on a wrong set), unnecessary continuation / budget '
                        'abstention on complete evidence, false conflict.'),
        'K9_NEGATIVE_CONTROLS': ('FEEDBACK terminal correct >= OFF + 3, >= PERTURBED + 3 and >= NEG_CONTROL + 3; '
                                 'otherwise the terminal behaviour is not attributable to native feedback.'),
        'ENGINE': ('Even if every K passes, the loop schedule is class C: the verdict for an autonomous native recursive '
                   'engine is NOT_ESTABLISHED; the strongest possible positive statement is MODEL_SIGNAL_DRIVEN_EXTERNAL_SCHEDULE.')},
    'terminal_correctness': {'FULL': 'SUFFICIENT with exactly {first, second}', 'MISLEAD_FIRST': 'SUFFICIENT with exactly {first, second}',
                             'REPLACE_SECOND_BY_ALT': 'SUFFICIENT with exactly {first, changed}',
                             'CONFLICT_ALT_ADDED': 'CONFLICT with {first, second, changed} all mounted',
                             'MISSING_FIRST': 'INSUFFICIENT', 'MISSING_SECOND': 'INSUFFICIENT'},
    'verdict_rule': ('PASS iff K1-K9 PASS (INCONCLUSIVE allowed only for K6/K7 when not evaluable). FAIL iff K2 or K3 FAIL, '
                     'or K8 FAIL with K9 FAIL. Otherwise INCONCLUSIVE. A budget stop forces INCONCLUSIVE.'),
    'calibration': ('12 separate worlds, 4 banks. First head: argmax hits of the own first link over the full mounted bank '
                    '(S_null state). Second head, separately for each state condition: argmax hits of the own second link '
                    'over the bank minus the first link, the state being S_null (OFF), KV after reading the true first '
                    'card (FEEDBACK), its Haar-rotated values (PERTURBED), or KV after reading a card of another bank '
                    '(NEG_CONTROL). Ties: mean margin, then lower layer, lower head. Stumps: one native feature, chosen on '
                    'calibration; sufficiency [first, second] vs [first, mirror] / [first, other] / [decoy, first]; '
                    'conflict [first, second, changed] vs [first, second, other] / [first, second, mirror].'),
    'schedule_C': ('for c1 in first-head ranking[:R1]: S1 = KV after reading c1; for c2 in second-head(state) ranking over '
                   'bank minus c1 [:R2]: if sufficiency-stump([c1, c2]): take the next second-head candidate c3; if '
                   'conflict-stump([c1, c2, c3]) -> CONFLICT else SUFFICIENT. Exhausted -> INSUFFICIENT.')}

CLAIMS835 = {
    'verified_from_prior_research': [
        'TEST834 GPU log (blob d468f3d3): all integrity gates passed (probe equivalence bitwise, HeadProbe vs locked probe '
        '3.93e-08, noninterference, frozen sentinel, no hooks); 36/36 runs; counted 1810 fusion / 818 probe / 510 mounts; '
        'the log ends at TEST834_OFFLINE_READOUTS_START without a failure record.',
        'TEST834 offline re-analysis (panel regenerated deterministically, panel SHA 435d97cb identical to the log): MAM '
        'hop-1 own first 15/30 (fork 14/36, decoy 7/36 over all runs), identical per world across bank conditions; B and D '
        'ended with one card in 30/36 runs; C contraction stops 35/36.',
        'TEST834 lock: L2V layer 65 head 46; in-sample address of second 2/12, uptake 10/12, reject mirror 12/12, reject '
        'other 12/12 -> refusal worked, address generation did not.',
        'The only .copy() in TEST834 source is ndarray.copy() after .numpy() (rprobe834), executed in every probe of the '
        'completed numeric phase; a Tensor.copy AttributeError therefore cannot come from TEST834 itself.'],
    'implemented_in_TEST835': [
        'Per-head (80 x 64) attention addressing over the full mounted physical bank (HeadProbe834, verbatim).',
        'First/second address heads calibrated on separate worlds; second head per feedback condition.',
        'Native KV feedback of the state after reading c1; Haar-rotated and other-bank negative controls.',
        'Calibrated one-feature sufficiency and conflict gates (class B) and a fixed search schedule (class C).',
        'SHA-chained per-run checkpoint and verified resume; static gate against ambiguous .copy() calls.'],
    'demonstrated_by_TEST835': 'filled only from this run'}

BODY835 = r'''
D829['test'] = '835'
D829['controller'] = 'NATIVE_HEAD_ADDRESS_OVER_MOUNTED_BANK + NATIVE_KV_FEEDBACK; CLASS_B_GATES; CLASS_C_SCHEDULE'
D829['sources835'] = {'829': LOCK829_835, '834': LOCK834_835, '834_log': LOCK834LOG_835, 'helpers_sha256': HELPER_SHA835,
                      'helpers': list(HELPERS835)}
D829['hypotheses835'] = PANEL829['test835']['hypotheses']
D829['limitations'] = [
    'The search schedule (how many candidates, revision, conflict check, when to declare INSUFFICIENT) is a fixed Python policy (class C).',
    'Addresses and gates are class B readouts (argmax, calibrated one-feature stump) of class A native signals.',
    'Mounting a chosen cartridge is execution of a class A+B address, not a model-internal action.',
    'The question tokens are re-entered at every forward (boundary input); no other text enters runtime computation.',
    'Six sealed worlds x six bank conditions; twelve separate calibration worlds; one template; one model.',
    'Answer text is generated offline after all numeric work with the TEST827 boundary instruction.',
    'No GPU execution or result is claimed by the code author.']
gate829('PANEL_FRESH_SEED', SEED829 == SEED835, SEED829)
gate829('NO_CONTROL_TEXT', MAX_NEW_CONTROL829 == 0)
gate829('RUN_COUNT', len(RUNS835) == len(CONDS835) * len(questions829) == len(CONDS835) * WORLDS_EVAL835, len(RUNS835))
gate829('CALIBRATION_DISJOINT', not (set(CALSTORE835) & set(EVALSTORE835)) and
        not ({j['qid'] for b in CALBLOCKS835 for j in b['jobs']} & {q['qid'] for q in questions829}))
gate829('CARTRIDGES_PHYSICAL', all(c in entries for r in RUNS835 for c in r['bank'] + [r['neg']]) and
        all(c in entries for c in CALSTORE835) and all(NULL829 not in r['bank'] for r in RUNS835))
gate829('NEG_CONTROL_OUTSIDE_BANK', all(r['neg'] not in r['bank'] for r in RUNS835))
# static type gate: every .copy() reachable from TEST835 runtime code must be ndarray.copy() after .numpy()
def copy_receivers835(src):
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'copy':
            r = n.func.value
            out.append(isinstance(r, ast.Call) and isinstance(r.func, ast.Attribute) and r.func.attr == 'numpy')
    return out
cr835 = copy_receivers835(HELPER_SRC835) + copy_receivers835(BODY835_TEXT)
gate829('STATIC_COPY_RECEIVERS_ARE_NDARRAY', all(cr835), {'copy_calls': len(cr835)})
exec(compile(HELPER_SRC835, 'TEST834_LOCKED_HELPERS', 'exec'), globals())
gate829('HELPERS834_LOADED', all(callable(globals().get(x)) for x in HELPERS835), HELPER_SHA835)
gate829('ENGINE_SYMBOLS835', all(callable(globals().get(x)) for x in
        ('cache_build', 'pairs', 'rephase', 'Cut3Diagnostic', 'AttentionIntervention', 'prompt_ids', 'build_fusion',
         'memory_seals', 'compare_seals', 'free_generate', 'observe_state', 'DirectCut3', 'kv_digest', 'safe_load',
         'numeric_rank', 'cosdist829', 'jsd829', 'full_readout829')))
gate829('ARCH_DIMS', (NL, H, QH, KVH, HD) == EXPECTED_ARCH834 and int(model.config.num_attention_heads) == QH and
        int(model.config.num_key_value_heads) == KVH and int(model.config.hidden_size) == H, (NL, H, QH, KVH, HD))
gate829('BF16_COMPUTE', DTYPE == _torch829.bfloat16, str(DTYPE))
gate829('NF4_LINEAR4BIT', any(isinstance(m_, bitsandbytes.nn.Linear4bit) for m_ in model.modules()))
gate829('WEIGHTS_FROZEN', all(not p_.requires_grad for p_ in model.parameters()))
gate829('DEVICE', str(DEV).startswith(DEVICE_KIND835), str(DEV))
gate829('ROPE_MODULE', callable(getattr(model.model, 'rotary_emb', None)))
gate829('SDPA_MODULE', F is _torch829.nn.functional and F.scaled_dot_product_attention is SDPA829)
gate829('PREFIX_P', P == 30, P)
gate829('TEST834_LOG_COMPLETE_NUMERIC', raw834log_835.decode('utf-8', 'replace').count('TEST834_RUN ') == 36 and
        'COUNTED_WITHIN_UPPER_BOUND' in raw834log_835.decode('utf-8', 'replace'))
POST835 = cost_upper835({c: int(entries[c]['body_tokens']) for c in cards829}, P)
D829['predicted_cost835'] = POST835
log829('TEST835_PREDICTED_COST', json.dumps(POST835))
gate829('PREDICTED_BUDGET_POST_LOAD', POST835['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN835,
        POST835['minutes_upper_excluding_model_load'])
QTEXT835 = {q['qid']: q['question'] for q in questions829}
for b835 in CALBLOCKS835:
    for j835 in b835['jobs']:
        QTEXT835[j835['qid']] = j835['question']
LQ834 = {qid: list(prompt_ids(t)) for qid, t in QTEXT835.items()}
gate829('FUSION_TOKENS_WITH_STATE', POST835['max_memory_tokens'] + 2 * max(len(v) for v in LQ834.values()) + 64 <= MAX_FUSED_TOKENS,
        POST835['max_memory_tokens'])
try:
    free835, _ = _torch829.cuda.mem_get_info()
    gate829('VRAM_HEADROOM', free835 / 2**30 >= 8.0, round(free835 / 2**30, 2))
except Exception as e835:
    gate829('VRAM_HEADROOM', False, repr(e835))
D829['noninterference835'] = noninterference829([NULL829], questions829[0]['question'])
for k835, v835 in D829['noninterference835'].items():
    gate829('NONINTERFERENCE_' + k835.upper(), bool(v835), v835)
COUNT834 = {'fusion_forwards': fusion_forwards829([NULL829]), 'probe_forwards': 3, 'capture_forwards': 0,
            'rank_forwards': 0, 'generation_forwards': 1, 'mounts': 1}
T0_835 = time.perf_counter()
HEART835 = DIR829 / 'TEST835_heartbeat.txt'
def beat835(*a):
    msg = ' '.join(map(str, a)) + ' t=' + str(round(time.perf_counter() - T0_835, 1)) + 's'
    print(msg, flush=True)
    with HEART835.open('a', encoding='utf-8') as fh:
        fh.write(msg + '\n')
SEAL_LAYERS834 = (0, CUT, NL // 2, NL - 1)
rs835 = np.random.default_rng(SEED835 + 33)
ROT834 = []
for l835 in range(NL):
    mats835 = []
    for j835 in range(KVH):
        qm835, rm835 = np.linalg.qr(rs835.standard_normal((HD, HD)))
        mats835.append(qm835 * np.sign(np.diag(rm835))[None, :])
    ROT834.append(torch.tensor(np.stack(mats835).astype(np.float32), device=DEV))

# ---- MAM baseline store (H3 rows of evaluation cartridges, SHA-verified safe_load) ----
ROWS834 = {}
for cid835 in EVALSTORE835:
    with contextlib.redirect_stdout(io.StringIO()):
        cp835 = safe_load(entries[cid835])
    b835n = int(entries[cid835]['body_tokens'])
    h3_835 = cp835['h'][0, P:, :].float().numpy().astype(np.float32)
    gate829('MEAS_ROWS_' + cid835, h3_835.shape == (b835n, H) and bool(np.isfinite(h3_835).all()))
    ROWS834[cid835] = {'H3': h3_835}
    del cp835
STORE834 = {'eval': fit_store834(EVALSTORE835)}

# ---- S_null per question ----
memN835, nN835 = mount834([NULL829], 'NULL')
sealN835 = seal834(memN835)
SNULL834 = {}
for qid835 in QTEXT835:
    pN = rprobe834(memN835, None, LQ834[qid835])
    SNULL834[qid835] = {'S': [(k.clone(), v.clone()) for k, v in pN['S_raw']], 'pos': pN['start'], 'h': pN['h'],
                        'state': pN['state']}
    del pN
gate829('KV_SEAL_NULL_AFTER_PROBES', seal834(memN835) == sealN835)
del memN835; gc.collect(); release()

# ---- equivalence gate on a calibration mount (as TEST833/834) ----
j0_835 = CALBLOCKS835[0]['jobs'][0]
memE835, nE835 = mount834([j0_835['first'], j0_835['second']], 'EQUIV')
b0E835 = int(entries[j0_835['first']]['body_tokens'])
spE835 = {'B0': (P, P + b0E835), 'B1': (P + b0E835, nE835)}
with Readout829() as roE835:
    stE835, attE835 = observe_state(memE835, QTEXT835[j0_835['qid']], spE835)
COUNT834['probe_forwards'] += 1
pE835 = rprobe834(memE835, None, LQ834[j0_835['qid']])
hpm835 = max(abs(float(pE835['rows'][l][:, spE835[s][0]:spE835[s][1]].sum(-1).mean()) - float(attE835[str(l)][s + '_mass']))
             for l in (4, 20, 40, 79) for s in ('B0', 'B1'))
D829['probe_equivalence835'] = {
    'cut3_state_bitwise': bool(np.array_equal(stE835.float().cpu().numpy().astype(np.float64), pE835['state'])),
    'final_hidden_bitwise': bool(np.array_equal(roE835.h.reshape(-1).double().cpu().numpy(), pE835['h'])),
    'headprobe_mass_max_abs_vs_locked_probe': hpm835}
gate829('PROBE_EQUALS_OBSERVE_STATE_CUT3', D829['probe_equivalence835']['cut3_state_bitwise'])
gate829('PROBE_EQUALS_OBSERVE_STATE_HIDDEN', D829['probe_equivalence835']['final_hidden_bitwise'])
gate829('HEADPROBE_EQUALS_LOCKED_ATTENTION_PROBE', hpm835 <= 2e-6, hpm835)
del memE835, pE835, stE835; gc.collect(); release()

# ---- shared numerical primitives ----
def state_after835(card, qid, n_target, cache):
    """KV rows the frozen model writes for the question after reading physical card `card` (S_null state), relocated
    to canonical positions after a memory of n_target tokens. Cached per (qid, card): deterministic."""
    key = (qid, card)
    if key not in cache:
        memx, n = mount834([card], 'S_' + str(len(cache)) + '_' + card)
        seal = seal834(memx)
        p = rprobe834(memx, s0_834(qid, n), LQ834[qid])
        gate829('MEAS_KV_SEAL_STATE_' + card + '_' + str(len(cache)), seal834(memx) == seal)
        cache[key] = {'S': [(k.clone(), v.clone()) for k, v in p['S_raw']], 'pos': p['start'],
                      'h': p['h'], 'entropy': p['summary']['entropy_nats']}
        del memx, p; gc.collect(); release()
    c = cache[key]
    return relocate834(c['S'], c['pos'], n_target, len(LQ834[qid]))

def entropy835(x):
    x = np.asarray(x, dtype=np.float64); s = float(x.sum())
    if s <= 0:
        return 0.0
    q = x / s
    return float(-(q[q > 0] * np.log(q[q > 0])).sum())

def raw_feats835(K, qid, cache):
    """Native features of the forward over mount K with S_null state (class A). Cached per (qid, K)."""
    key = (qid, tuple(K))
    if key not in cache:
        memx, n = mount834(list(K), 'F_' + str(len(cache)))
        seal = seal834(memx)
        p = rprobe834(memx, s0_834(qid, n), LQ834[qid])
        gate829('MEAS_KV_SEAL_FEAT_' + str(len(cache)), seal834(memx) == seal)
        cm = card_mass834(p['rows'], cspans834(list(K))).astype(np.float32)          # (NL, QH, |K|)
        cache[key] = {'entropy': p['summary']['entropy_nats'], 'top1_prob': float(p['summary']['top_probs'][0]),
                      'null_hidden_dist': cosdist829(p['h'], SNULL834[qid]['h']),
                      'null_cut3_dist': cosdist829(p['state'], SNULL834[qid]['state']), 'cm': cm,
                      'h_sha': sha829(np.asarray(p['h'], dtype=np.float32).tobytes())}
        del memx, p; gc.collect(); release()
    return cache[key]

FEATS835 = ('entropy', 'top1_prob', 'null_hidden_dist', 'null_cut3_dist', 'sh_last_mass', 'sh_card_mass', 'fh_card_entropy')
def feat_vec835(rf, FHd, SHd):
    cmF = rf['cm'][FHd[0], FHd[1], :].astype(np.float64); cmS = rf['cm'][SHd[0], SHd[1], :].astype(np.float64)
    return {'entropy': rf['entropy'], 'top1_prob': rf['top1_prob'], 'null_hidden_dist': rf['null_hidden_dist'],
            'null_cut3_dist': rf['null_cut3_dist'], 'sh_last_mass': float(cmS[-1]), 'sh_card_mass': float(cmS.sum()),
            'fh_card_entropy': entropy835(cmF)}

def rank_cards835(M, lh, cards, idx_of, tie, exclude=()):
    l, h = lh
    sc = {c: float(M[l, h, idx_of[c]]) for c in cards if c not in exclude}
    return sorted(sc, key=lambda c: (-sc[c], tie.get(c, 10**6))), sc

def bank_forward835(memx, n, qid, S, csp):
    p = rprobe834(memx, S, LQ834[qid])
    M = card_mass834(p['rows'], csp).astype(np.float32)
    out = {'M': M, 'h': p['h'], 'entropy': p['summary']['entropy_nats']}
    del p
    return out

# ==================================================================================================================
# CALIBRATION PHASE (separate calibration worlds; their roles are used ONLY here)
# ==================================================================================================================
beat835('TEST835_CALIBRATION_START', sum(len(b['jobs']) for b in CALBLOCKS835), 'jobs')
NH835 = NL * QH
CALHIT835 = {'first': [], 'first_margin': []}
for st in STATES835:
    CALHIT835['second_' + st] = []; CALHIT835['second_margin_' + st] = []
CALFEAT835 = []
SCACHE_CAL835, FCACHE_CAL835 = {}, {}
for bi835, blk in enumerate(CALBLOCKS835):
    bank = list(blk['bank']); idx = {c: i for i, c in enumerate(bank)}
    memB, nB = mount834(bank, 'CALBANK_%d' % bi835)
    sealB = seal834(memB); csp = cspans834(bank)
    for job in blk['jobs']:
        qid = job['qid']; fi = idx[job['first']]; si = idx[job['second']]
        S1 = state_after835(job['first'], qid, nB, SCACHE_CAL835)
        Sn = state_after835(job['neg'], qid, nB, SCACHE_CAL835)
        Sin = {'OFF': s0_834(qid, nB), 'FEEDBACK': S1, 'PERTURBED': rotate834(S1), 'NEG_CONTROL': Sn}
        for st in STATES835:
            M = bank_forward835(memB, nB, qid, Sin[st], csp)['M'].astype(np.float64)
            if st == 'OFF':
                hitF = np.argmax(M, axis=-1) == fi
                othF = np.max(np.delete(M, fi, axis=-1), axis=-1)
                CALHIT835['first'].append(hitF.reshape(-1)); CALHIT835['first_margin'].append((M[..., fi] - othF).reshape(-1))
            Mx = np.array(M, copy=True)
            Mx[..., fi] = -np.inf
            hitS = np.argmax(Mx, axis=-1) == si
            othS = np.max(np.delete(Mx, [fi, si], axis=-1), axis=-1)
            CALHIT835['second_' + st].append(hitS.reshape(-1))
            CALHIT835['second_margin_' + st].append((M[..., si] - othS).reshape(-1))
        del Sin, S1, Sn
        fj = {'suff_pos': [raw_feats835(K, qid, FCACHE_CAL835) for K in job['suff_pos']],
              'suff_neg': [raw_feats835(K, qid, FCACHE_CAL835) for K in job['suff_neg']],
              'conf_pos': [raw_feats835(K, qid, FCACHE_CAL835) for K in job['conf_pos']],
              'conf_neg': [raw_feats835(K, qid, FCACHE_CAL835) for K in job['conf_neg']]}
        CALFEAT835.append(fj)
        beat835('TEST835_CALIBRATION_JOB', qid)
    gate829('MEAS_KV_SEAL_CALBANK_%d' % bi835, seal834(memB) == sealB)
    del memB; gc.collect(); release()

def select_head835(hits, margins):
    tot = np.sum(hits, axis=0); mar = np.mean(margins, axis=0)
    best = max(range(NH835), key=lambda i: (int(tot[i]), float(mar[i]), -(i // QH), -(i % QH)))
    top = sorted(range(NH835), key=lambda i: (-int(tot[i]), -float(mar[i]), i // QH, i % QH))[:8]
    return (best // QH, best % QH), {'hits': int(tot[best]), 'of': len(hits), 'mean_margin': float(mar[best]),
                                      'top8': [{'layer': i // QH, 'head': i % QH, 'hits': int(tot[i]),
                                                'margin': float(mar[i])} for i in top]}
FH835, FHINFO835 = select_head835(CALHIT835['first'], CALHIT835['first_margin'])
SH835, SHINFO835 = {}, {}
for st in STATES835:
    SH835[st], SHINFO835[st] = select_head835(CALHIT835['second_' + st], CALHIT835['second_margin_' + st])
calv835 = {g: {f: [] for f in FEATS835} for g in ('suff_pos', 'suff_neg', 'conf_pos', 'conf_neg')}
for fj in CALFEAT835:
    for g in calv835:
        for rf in fj[g]:
            fv = feat_vec835(rf, FH835, SH835['OFF'])
            for f in FEATS835:
                calv835[g][f].append(fv[f])
def pick_stump835(pos, neg):
    st = {f: stump_fit834(pos[f], neg[f]) for f in FEATS835}
    sel = max(FEATS835, key=lambda f: (st[f]['cal_balanced_acc'], -FEATS835.index(f)))
    return sel, st
SUFFSEL835, SUFFST835 = pick_stump835(calv835['suff_pos'], calv835['suff_neg'])
CONFSEL835, CONFST835 = pick_stump835(calv835['conf_pos'], calv835['conf_neg'])
def gate_apply835(st, f, fv):
    s = st[f]; x = fv[f]
    return False if (x is None or s['threshold'] is None or not np.isfinite(x)) else bool(s['sign'] * (x - s['threshold']) > 0)
LOCK835 = {'first_head': list(FH835), 'second_heads': {st: list(SH835[st]) for st in STATES835},
           'sufficiency_feature': SUFFSEL835, 'sufficiency_stump': SUFFST835[SUFFSEL835],
           'conflict_feature': CONFSEL835, 'conflict_stump': CONFST835[CONFSEL835]}
LOCK_SHA835 = sha829(json.dumps(LOCK835, sort_keys=True))
D829['lock835'] = dict(LOCK835, lock_sha256=LOCK_SHA835, first_head_calibration=FHINFO835,
                       second_head_calibration=SHINFO835,
                       stumps_all={'sufficiency': SUFFST835, 'conflict': CONFST835},
                       note='IN-SAMPLE calibration counts; evaluation counts come only from the sealed panel.')
log829('TEST835_LOCK', json.dumps(D829['lock835'], default=str))
COUNT_CAL835 = dict(COUNT834)
del CALHIT835, FCACHE_CAL835, SCACHE_CAL835; gc.collect(); release()

# ==================================================================================================================
# EVALUATION RUNTIME (sealed panel). Until the OFFLINE PHASE no label, role, condition or answer is read.
# ==================================================================================================================
QA835 = {}
for q835 in sorted(QTEXT835):
    if q835 in {r['qid'] for r in RUNS835}:
        rq835, _ = question_rows834(q835)
        QA835[q835] = apply_vec834(rq835, 'eval', 'H3')
RANK815_835 = {}
for q835 in sorted(QA835):
    with contextlib.redirect_stdout(io.StringIO()):
        rk835, _ = numeric_rank(QTEXT835[q835], {c: bank829[c] for c in EVALSTORE835})
    RANK815_835[q835] = list(rk835); COUNT834['rank_forwards'] += 1

CKPT835 = DIR829 / 'TEST835_checkpoint.jsonl'
HEADER835 = {'panel_sha256': PANEL_SHA829, 'body_sha256': PANEL829['test835']['body_sha256'], 'lock_sha256': LOCK_SHA835,
             'helpers_sha256': HELPER_SHA835}
RESUMED835 = {}
D829['resume835'] = {'enabled': RESUME835, 'source': None, 'reused_runs': 0, 'reason': None}
if RESUME835:
    for cand in sorted(DIR829.parent.glob('TEST835_*/TEST835_checkpoint.jsonl'), reverse=True):
        if cand.parent == DIR829:
            continue
        try:
            lines = cand.read_text(encoding='utf-8').splitlines()
            hdr = json.loads(lines[0])
            if hdr.get('header') != HEADER835:
                D829['resume835']['reason'] = 'header mismatch in ' + str(cand); continue
            prev = sha829(json.dumps(hdr, sort_keys=True)); got = {}
            for ln in lines[1:]:
                o = json.loads(ln)
                ok = o['prev'] == prev and o['sha'] == sha829(json.dumps({'run': o['run'], 'record': o['record'],
                                                                           'prev': o['prev']}, sort_keys=True))
                if not ok:
                    break
                got[o['run']] = o['record']; prev = o['sha']
            RESUMED835 = got
            D829['resume835'].update({'source': str(cand), 'reused_runs': len(got), 'reason': 'header and SHA chain verified'})
            break
        except Exception as e835r:
            D829['resume835']['reason'] = 'unreadable ' + str(cand) + ' ' + repr(e835r)
log829('TEST835_RESUME', json.dumps(D829['resume835']))
with CKPT835.open('w', encoding='utf-8') as fh835:
    fh835.write(json.dumps({'header': HEADER835}, sort_keys=True) + '\n')
PREV835 = [sha829(json.dumps({'header': HEADER835}, sort_keys=True))]
def checkpoint835(rid, rec):
    payload = {'run': rid, 'record': rec, 'prev': PREV835[0]}
    s = sha829(json.dumps(payload, sort_keys=True, default=str))
    with CKPT835.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(dict(payload, sha=s), sort_keys=True, default=str) + '\n')
    PREV835[0] = s

def bankM835(st, c1, ctx):
    """Attention masses over the mounted bank under state condition st (class A). Cached per (st, c1)."""
    if st == 'OFF':
        return ctx['M_off']
    key = (st, None if st == 'NEG_CONTROL' else c1)
    if key not in ctx['bankfw']:
        if st == 'NEG_CONTROL':
            S = state_after835(ctx['neg'], ctx['qid'], ctx['nB'], ctx['scache'])
        else:
            S = state_after835(c1, ctx['qid'], ctx['nB'], ctx['scache'])
            if st == 'PERTURBED':
                S = rotate834(S)
        ctx['bankfw'][key] = bank_forward835(ctx['memB'], ctx['nB'], ctx['qid'], S, ctx['csp'])
        del S
    return ctx['bankfw'][key]['M']

def schedule835(st, ctx):
    """CLASS C schedule over class A signals and class B gates, for one state condition."""
    trace = []; feats_seen = []
    for c1 in ctx['rank1'][:R1_835]:
        M = bankM835(st, c1, ctx)
        rank2, sc2 = rank_cards835(M, SH835[st], ctx['bank'], ctx['idx'], ctx['tie'], exclude={c1})
        for c2 in rank2[:R2_835]:
            fv = feat_vec835(raw_feats835([c1, c2], ctx['qid'], ctx['fcache']), FH835, SH835['OFF'])
            suff = gate_apply835(SUFFST835, SUFFSEL835, fv)
            step = {'c1': c1, 'c2': c2, 'second_score': sc2[c2], 'sufficient_gate': suff,
                    'sufficiency_feature_value': fv[SUFFSEL835]}
            if suff:
                rest = [c for c in rank2 if c != c2]
                if rest:
                    c3 = rest[0]
                    fv3 = feat_vec835(raw_feats835([c1, c2, c3], ctx['qid'], ctx['fcache']), FH835, SH835['OFF'])
                    conf = gate_apply835(CONFST835, CONFSEL835, fv3)
                    step.update({'c3': c3, 'conflict_gate': conf, 'conflict_feature_value': fv3[CONFSEL835]})
                    trace.append(step)
                    if conf:
                        return {'decision': 'CONFLICT', 'K': [c1, c2, c3], 'trace': trace, 'stop': 'STOP_CONFLICT_GATE'}
                    return {'decision': 'SUFFICIENT', 'K': [c1, c2], 'trace': trace, 'stop': 'STOP_SUFFICIENT_GATE'}
                trace.append(step)
                return {'decision': 'SUFFICIENT', 'K': [c1, c2], 'trace': trace, 'stop': 'STOP_SUFFICIENT_GATE'}
            trace.append(step)
    return {'decision': 'INSUFFICIENT', 'K': [], 'trace': trace, 'stop': 'STOP_SCHEDULE_EXHAUSTED_INSUFFICIENT'}

D829['runs835'] = []
BUDGET_STOP835 = False
t_eval835 = time.perf_counter()
for k_run835, r835 in enumerate(RUNS835):
    rid = r835['run']
    if rid in RESUMED835:
        rec = dict(RESUMED835[rid]); rec['resumed_from'] = D829['resume835']['source']
        D829['runs835'].append(rec); checkpoint835(rid, RESUMED835[rid])
        beat835('TEST835_RUN_RESUMED', k_run835 + 1, rid); continue
    if (time.perf_counter() - T0_835) / 60.0 > HARD_BUDGET_MIN835:
        BUDGET_STOP835 = True
        log829('TEST835_BUDGET_STOP', 'completed_runs', k_run835, 'of', len(RUNS835)); break
    tc = time.perf_counter()
    bank = list(r835['bank']); tie = {c: i for i, c in enumerate(r835['tie_order'])}; qid = r835['qid']
    idx = {c: i for i, c in enumerate(bank)}
    beat835('TEST835_HEARTBEAT', k_run835 + 1, '/', len(RUNS835), rid, 'bank', len(bank))
    rec = {'run': rid, 'qid': qid, 'bank_size': len(bank)}
    h1 = address834(QA835[qid], bank, 'eval', 'H3', tie)
    rec['mam_hop1'] = h1['ranked'][:5]; rec['rank815'] = [c for c in RANK815_835[qid] if c in bank][:5]
    # order reversal of the physical bank (OFF state): first-head argmax stability
    rbank = list(reversed(bank)); memR, nR = mount834(rbank, rid + '_REV')
    fR = bank_forward835(memR, nR, qid, s0_834(qid, nR), cspans834(rbank))
    ridx = {c: i for i, c in enumerate(rbank)}
    rec['first_rev'] = rank_cards835(fR['M'], FH835, rbank, ridx, tie)[0][:3]
    del memR, fR; gc.collect(); release()
    memB, nB = mount834(bank, rid + '_BANK')
    sealB = seal834(memB); csp = cspans834(bank)
    fOFF = bank_forward835(memB, nB, qid, s0_834(qid, nB), csp)
    rank1, sc1 = rank_cards835(fOFF['M'], FH835, bank, idx, tie)
    rec['first_rank'] = rank1[:5]; rec['first_scores'] = {c: sc1[c] for c in rank1[:5]}
    rec['first_margin'] = (sc1[rank1[0]] - sc1[rank1[1]]) if len(rank1) > 1 else None
    rec['off_second_masses'] = {st: {c: float(fOFF['M'][SH835[st][0], SH835[st][1], idx[c]]) for c in bank} for st in STATES835}
    ctx = {'rank1': rank1, 'M_off': fOFF['M'], 'bankfw': {}, 'scache': {}, 'fcache': {}, 'memB': memB, 'nB': nB,
           'csp': csp, 'bank': bank, 'idx': idx, 'tie': tie, 'qid': qid, 'neg': r835['neg']}
    rec['schedules'] = {}
    for st in STATES835:
        rec['schedules'][st] = schedule835(st, ctx)
    rec['second_rank_first_c1'] = {}
    for st in STATES835:
        M = bankM835(st, rank1[0], ctx)
        r2, s2 = rank_cards835(M, SH835[st], bank, idx, tie, exclude={rank1[0]})
        rec['second_rank_first_c1'][st] = {'rank': r2[:4], 'margin': (s2[r2[0]] - s2[r2[1]]) if len(r2) > 1 else None}
    rec['feedback_hidden_dist_vs_off'] = {st: float(np.linalg.norm(v['h'] - fOFF['h'])) for (st, c), v in ctx['bankfw'].items()
                                          if c in (rank1[0], None)}
    rec['feature_sets'] = {'|'.join(k[1]): {f: v[f] for f in ('entropy', 'top1_prob', 'null_hidden_dist', 'null_cut3_dist', 'h_sha')}
                           for k, v in ctx['fcache'].items()}
    gate829('MEAS_KV_SEAL_BANK_' + rid, seal834(memB) == sealB)
    del memB, ctx, fOFF; gc.collect(); release()
    rec['seconds'] = round(time.perf_counter() - tc, 3)
    D829['runs835'].append(rec); checkpoint835(rid, rec); save829()
    log829('TEST835_RUN', rid, 'c1', rank1[0], ' '.join(st + ':' + rec['schedules'][st]['decision'] + '/' +
                                                      str(len(rec['schedules'][st]['K'])) for st in STATES835), 's', rec['seconds'])
D829['numeric_seconds835'] = round(time.perf_counter() - t_eval835, 3)
D829['budget_stop835'] = BUDGET_STOP835

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
for cid835 in cards829:
    gate829('FINAL_SHA_' + cid835, sha_file(CART_DIR / entries[cid835]['file']) == entries[cid835]['sha256'])
COUNT_NUMERIC835 = dict(COUNT834)
gate829('COUNTED_WITHIN_UPPER_BOUND', all(COUNT_NUMERIC835[k] <= POST835['numeric_upper'][k] for k in POST835['numeric_upper']),
        {'counted': COUNT_NUMERIC835, 'upper': POST835['numeric_upper']})

# ==================================================================================================================
# OFFLINE PHASE: numerical runtime finished and sealed; labels and text are used only from here.
# ==================================================================================================================
beat835('TEST835_OFFLINE_START')
KIND835 = {cid: m['kind'] for cid, m in card_meta829.items()}
DOM835 = {cid: m['domain'] for cid, m in card_meta829.items()}
def role835(cid, w):
    if cid is None:
        return None
    return ('OWN_' if DOM835.get(cid) == w['world'] else 'OTHER_') + str(KIND835.get(cid)).upper()
# ---- ORACLE DIAGNOSTIC (labelled; never a capability): second-address ceiling given the TRUE first card ----
D829['oracle835'] = []
ORACLE_SC835 = {}
for rec in D829['runs835']:
    key = RUNKEY835[rec['run']]; w = worlds829[key['world']]; first = w['ids']['first']
    r835 = next(r for r in RUNS835 if r['run'] == rec['run'])
    if key['condition'] == 'MISSING_FIRST' or rec['first_rank'][0] == first or rec.get('resumed_from'):
        continue
    bank = list(r835['bank']); tie = {c: i for i, c in enumerate(r835['tie_order'])}; idx = {c: i for i, c in enumerate(bank)}
    memB, nB = mount834(bank, rec['run'] + '_ORACLE')
    csp = cspans834(bank); out = {}
    S1 = state_after835(first, rec['qid'], nB, ORACLE_SC835)
    for st, S in (('FEEDBACK', S1), ('PERTURBED', rotate834(S1))):
        f = bank_forward835(memB, nB, rec['qid'], S, csp)
        out[st] = rank_cards835(f['M'], SH835[st], bank, idx, tie, exclude={first})[0][:3]
    for st in ('OFF', 'NEG_CONTROL'):
        sc = {c: v for c, v in rec['off_second_masses'][st].items() if c != first} if st == 'OFF' else None
        if sc is not None:
            out[st] = sorted(sc, key=lambda c: (-sc[c], tie.get(c, 10**6)))[:3]
    D829['oracle835'].append({'run': rec['run'], 'second_rank_given_true_first': out})
    del memB, S1; gc.collect(); release()
# ---- answer readouts (text, offline only) ----
TEXT835 = {}
def text835(mount, qid, tag):
    key = (qid, tuple(mount))
    if key not in TEXT835:
        memx, n = mount834(list(mount) if mount else [NULL829], 'TXT_' + tag)
        o = free_generate(memx, answer_prompt829(QTEXT835[qid]), seed=None, gain=0., max_new=MAX_NEW_TEXT835, spans=None)
        COUNT834['generation_forwards'] += int(o['generated_tokens'])
        TEXT835[key] = {'text': o['raw'].strip(), 'tokens': int(o['generated_tokens'])}
        del memx; gc.collect(); release()
    return TEXT835[key]
for rec in D829['runs835']:
    r835 = next(r for r in RUNS835 if r['run'] == rec['run'])
    rec['text'] = {'FULL_BANK': text835(r835['bank'], rec['qid'], rec['run'] + '_A'), 'NULL': text835([], rec['qid'], rec['qid'] + '_N')}
    for st in STATES835:
        K = rec['schedules'][st]['K']
        rec['text'][st] = text835(K, rec['qid'], rec['run'] + '_' + st) if K else {'text': 'UNKNOWN', 'tokens': 0,
                                                                                    'note': 'class C INSUFFICIENT -> UNKNOWN'}
save829()

def text_class835(t, w):
    u = (t or '').upper()
    return [nm for nm, c in (('END', w['end']), ('MIDDLE', w['middle']), ('ALT_END', w['changed_end']), ('FORK_END', w['fork_end']),
                             ('DECOY', w['decoy_end']), ('LURE_END', w['lure_end'])) if c in u] + (['UNKNOWN'] if 'UNKNOWN' in u else [])
def text_ok835(cls, cond):
    names = [x for x in cls if x != 'UNKNOWN']
    if cond in ('FULL', 'MISLEAD_FIRST'):
        return names == ['END'] and 'UNKNOWN' not in cls
    if cond == 'REPLACE_SECOND_BY_ALT':
        return names == ['ALT_END'] and 'UNKNOWN' not in cls
    if cond == 'CONFLICT_ALT_ADDED':
        return ('END' in names and 'ALT_END' in names) or cls == ['UNKNOWN']
    return cls == ['UNKNOWN']
COMPLETE835 = ('FULL', 'MISLEAD_FIRST', 'REPLACE_SECOND_BY_ALT', 'CONFLICT_ALT_ADDED')
MISSING835 = ('MISSING_FIRST', 'MISSING_SECOND')
def valid_second835(cid, w, cond):
    k = KIND835.get(cid); own = DOM835.get(cid) == w['world']
    if not own:
        return False
    if cond == 'REPLACE_SECOND_BY_ALT':
        return k == 'changed'
    if cond == 'CONFLICT_ALT_ADDED':
        return k in ('second', 'changed')
    return k == 'second'
def terminal_ok835(sch, w, cond):
    K = set(sch['K']); ids = w['ids']
    if cond in ('FULL', 'MISLEAD_FIRST'):
        return sch['decision'] == 'SUFFICIENT' and K == {ids['first'], ids['second']}
    if cond == 'REPLACE_SECOND_BY_ALT':
        return sch['decision'] == 'SUFFICIENT' and K == {ids['first'], ids['changed']}
    if cond == 'CONFLICT_ALT_ADDED':
        return sch['decision'] == 'CONFLICT' and K == {ids['first'], ids['second'], ids['changed']}
    return sch['decision'] == 'INSUFFICIENT'
EV835 = []
for rec in D829['runs835']:
    key = RUNKEY835[rec['run']]; w = worlds829[key['world']]; cond = key['condition']; first = w['ids']['first']
    e = {'run': rec['run'], 'world': key['world'], 'condition': cond, 'resumed': bool(rec.get('resumed_from'))}
    e['first_present'] = cond != 'MISSING_FIRST'
    e['first_role'] = role835(rec['first_rank'][0], w); e['first_ok'] = rec['first_rank'][0] == first
    e['first_margin'] = rec['first_margin']
    e['first_rev_same'] = rec['first_rev'][:1] == rec['first_rank'][:1]
    e['mam_ok'] = bool(rec['mam_hop1']) and rec['mam_hop1'][0] == first
    e['rank815_ok'] = bool(rec['rank815']) and rec['rank815'][0] == first
    e['second'] = {}
    for st in STATES835:
        r2 = rec['second_rank_first_c1'][st]['rank']
        e['second'][st] = {'role': role835(r2[0], w) if r2 else None, 'ok': bool(r2) and valid_second835(r2[0], w, cond),
                           'margin': rec['second_rank_first_c1'][st]['margin']}
    e['terminal'] = {}
    for st in STATES835:
        sch = rec['schedules'][st]
        tr = sch['trace']
        first_c2_wrong = bool(tr) and tr[0]['c1'] == first and not valid_second835(tr[0]['c2'], w, cond)
        e['terminal'][st] = {'decision': sch['decision'], 'K_roles': [role835(c, w) for c in sch['K']], 'stop': sch['stop'],
                             'ok': terminal_ok835(sch, w, cond), 'steps': len(tr),
                             'revised_first': any(t['c1'] != rec['first_rank'][0] for t in tr),
                             'first_c2_wrong_with_true_first': first_c2_wrong,
                             'premature_sufficient': sch['decision'] == 'SUFFICIENT' and not terminal_ok835(sch, w, cond),
                             'false_conflict': sch['decision'] == 'CONFLICT' and cond != 'CONFLICT_ALT_ADDED',
                             'insufficient_on_complete': sch['decision'] == 'INSUFFICIENT' and cond in COMPLETE835}
        t = rec['text'][st]; cls = text_class835(t['text'], w)
        e['terminal'][st]['text_classes'] = cls; e['terminal'][st]['text_ok'] = text_ok835(cls, cond)
    for nm in ('FULL_BANK', 'NULL'):
        cls = text_class835(rec['text'][nm]['text'], w); e['text_' + nm] = {'classes': cls, 'ok': text_ok835(cls, cond)}
    orc = next((o for o in D829['oracle835'] if o['run'] == rec['run']), None)
    if orc:
        e['oracle_second_ok'] = {st: bool(v) and valid_second835(v[0], w, cond) for st, v in orc['second_rank_given_true_first'].items()}
    EV835.append(e)
D829['offline_eval835'] = EV835

def frac835(k, n, need, minimum):
    return 'INCONCLUSIVE' if n < minimum else ('PASS' if k >= need * n - 1e-12 else 'FAIL')
fp835 = [e for e in EV835 if e['first_present']]
cp835 = [e for e in EV835 if e['condition'] in COMPLETE835]
ms835 = [e for e in EV835 if e['condition'] in MISSING835]
k1n = sum(e['first_ok'] for e in fp835)
K1 = 'PASS' if len(fp835) == 30 and k1n >= 24 else ('FAIL' if len(fp835) == 30 else 'INCONCLUSIVE')
ev2 = [e for e in cp835 if e['first_ok']]
hits2 = {st: sum(e['second'][st]['ok'] for e in ev2) for st in STATES835}
K2 = frac835(hits2['FEEDBACK'], len(ev2), 0.75, 8)
K3 = ('INCONCLUSIVE' if len(ev2) < 8 else
      'PASS' if all(hits2['FEEDBACK'] >= hits2[s] + 3 for s in ('OFF', 'PERTURBED', 'NEG_CONTROL')) else 'FAIL')
term = {st: sum(e['terminal'][st]['ok'] for e in EV835) for st in STATES835}
k4a = sum(e['terminal']['FEEDBACK']['decision'] == 'INSUFFICIENT' for e in ms835)
k4b = sum(e['terminal']['FEEDBACK']['ok'] for e in cp835)
K4 = 'PASS' if len(ms835) == 12 and k4a >= 10 and k4b >= 12 else ('FAIL' if len(ms835) == 12 else 'INCONCLUSIVE')
cf835 = [e for e in EV835 if e['condition'] == 'CONFLICT_ALT_ADDED']
k5a = sum(e['terminal']['FEEDBACK']['decision'] == 'CONFLICT' for e in cf835)
k5b = sum(e['terminal']['FEEDBACK']['false_conflict'] for e in EV835)
K5 = 'PASS' if len(cf835) == 6 and k5a >= 5 and k5b <= 2 else ('FAIL' if len(cf835) == 6 else 'INCONCLUSIVE')
ev6 = [e for e in cp835 if not e['first_ok']]
k6n = sum(e['terminal']['FEEDBACK']['ok'] for e in ev6)
K6 = frac835(k6n, len(ev6), 0.5, 3)
ev7 = [e for e in cp835 if e['terminal']['FEEDBACK']['first_c2_wrong_with_true_first']]
k7n = sum(e['terminal']['FEEDBACK']['ok'] for e in ev7)
K7 = frac835(k7n, len(ev7), 0.5, 3)
K8 = 'PASS' if len(EV835) == 36 and term['FEEDBACK'] >= 24 else ('FAIL' if len(EV835) == 36 else 'INCONCLUSIVE')
K9 = 'PASS' if all(term['FEEDBACK'] >= term[s] + 3 for s in ('OFF', 'PERTURBED', 'NEG_CONTROL')) else 'FAIL'
CRIT835 = {'K1_FIRST_ADDRESS': K1, 'K2_SECOND_ADDRESS': K2, 'K3_FEEDBACK_CAUSAL': K3, 'K4_MISSING': K4,
           'K5_CONTRADICTION': K5, 'K6_CORRECTION': K6, 'K7_RESEARCH': K7, 'K8_STOPPING': K8, 'K9_NEGATIVE_CONTROLS': K9}
if BUDGET_STOP835:
    verdict835 = 'INCONCLUSIVE'
elif K2 == 'FAIL' or K3 == 'FAIL' or (K8 == 'FAIL' and K9 == 'FAIL'):
    verdict835 = 'FAIL'
elif all(v == 'PASS' for k, v in CRIT835.items() if k not in ('K6_CORRECTION', 'K7_RESEARCH')) and \
        all(CRIT835[k] in ('PASS', 'INCONCLUSIVE') for k in ('K6_CORRECTION', 'K7_RESEARCH')):
    verdict835 = 'PASS'
else:
    verdict835 = 'INCONCLUSIVE'
def cnt_roles835(xs):
    out = {}
    for x in xs:
        out[str(x)] = out.get(str(x), 0) + 1
    return out
def mean835(xs):
    xs = [x for x in xs if x is not None]
    return float(np.mean(xs)) if xs else None
REPORT835 = {
    'Q1_first_address_accuracy': {'native_first_head': [k1n, len(fp835)], 'mam_peak50': [sum(e['mam_ok'] for e in fp835), len(fp835)],
                                  'rank815': [sum(e['rank815_ok'] for e in fp835), len(fp835)],
                                  'first_head_roles': cnt_roles835(e['first_role'] for e in EV835),
                                  'first_margin_mean_correct': mean835([e['first_margin'] for e in fp835 if e['first_ok']]),
                                  'first_margin_mean_wrong': mean835([e['first_margin'] for e in fp835 if not e['first_ok']]),
                                  'order_reversal_same_first': [sum(e['first_rev_same'] for e in EV835), len(EV835)]},
    'Q2_second_address_accuracy_given_own_first': {st: [hits2[st], len(ev2)] for st in STATES835},
    'Q2_second_roles': {st: cnt_roles835(e['second'][st]['role'] for e in ev2) for st in STATES835},
    'Q2_oracle_ceiling_runs_with_wrong_c1': {st: [sum(e.get('oracle_second_ok', {}).get(st, False) for e in EV835 if 'oracle_second_ok' in e),
                                                  sum(1 for e in EV835 if 'oracle_second_ok' in e)] for st in STATES835},
    'Q3_feedback_causal': {'second_address': hits2, 'terminal_correct': term,
                           'discordant_FEEDBACK_vs_OFF': [sum(e['second']['FEEDBACK']['ok'] and not e['second']['OFF']['ok'] for e in ev2),
                                                          sum(e['second']['OFF']['ok'] and not e['second']['FEEDBACK']['ok'] for e in ev2)],
                           'hidden_moved_by_state': sum(1 for r in D829['runs835'] if any(v > 0 for v in r['feedback_hidden_dist_vs_off'].values()))},
    'Q4_missing': {st: {'insufficient_on_missing': sum(e['terminal'][st]['decision'] == 'INSUFFICIENT' for e in ms835),
                        'text_unknown_on_missing': sum(e['terminal'][st]['text_ok'] for e in ms835),
                        'insufficient_on_complete': sum(e['terminal'][st]['insufficient_on_complete'] for e in EV835)} for st in STATES835},
    'Q5_contradiction': {st: {'conflict_on_conflict': sum(e['terminal'][st]['decision'] == 'CONFLICT' for e in cf835),
                              'false_conflict': sum(e['terminal'][st]['false_conflict'] for e in EV835)} for st in STATES835},
    'Q6_correction': {st: [sum(e['terminal'][st]['ok'] for e in ev6), len(ev6)] for st in STATES835},
    'Q7_research': {st: [sum(e['terminal'][st]['ok'] for e in ev7), len(ev7)] for st in STATES835},
    'Q8_stopping': {st: {'correct': term[st], 'premature_sufficient': sum(e['terminal'][st]['premature_sufficient'] for e in EV835),
                         'false_conflict': sum(e['terminal'][st]['false_conflict'] for e in EV835),
                         'budget_abstention_on_complete': sum(e['terminal'][st]['insufficient_on_complete'] for e in EV835),
                         'stop_types': cnt_roles835(e['terminal'][st]['stop'] for e in EV835)} for st in STATES835},
    'by_condition_terminal_correct': {st: {c: [sum(e['terminal'][st]['ok'] for e in EV835 if e['condition'] == c),
                                               sum(1 for e in EV835 if e['condition'] == c)] for c in CONDS835} for st in STATES835},
    'text_correct': {'FULL_BANK': sum(e['text_FULL_BANK']['ok'] for e in EV835), 'NULL': sum(e['text_NULL']['ok'] for e in EV835),
                     **{st: sum(e['terminal'][st]['text_ok'] for e in EV835) for st in STATES835}},
    'decision_classes': {'first_address': 'A attention probabilities -> B argmax (calibrated head) -> mount = execution',
                         'second_address': 'A attention under A KV state -> B argmax (calibrated head) -> mount = execution',
                         'sufficiency': 'A native feature -> B calibrated stump', 'conflict': 'A native feature -> B calibrated stump',
                         'continue / revise / re-search / stop / UNKNOWN': 'C fixed schedule',
                         'answer text': 'offline readout only'},
    'resumed_runs': sum(e['resumed'] for e in EV835)}
REPORT835['Q9_which_survive_negative_controls'] = {
    'second_address_feedback_beats_all_controls': K3 == 'PASS', 'terminal_feedback_beats_all_controls': K9 == 'PASS'}
REPORT835['Q10_autonomous_native_recursive_engine'] = (
    'NOT_ESTABLISHED: continuation, revision, re-search and stopping are class C; at best MODEL_SIGNAL_DRIVEN_EXTERNAL_SCHEDULE'
    + (' (all K criteria passed)' if verdict835 == 'PASS' else ''))
D829['report835'] = REPORT835
D829['capabilities835'] = {'first_address': K1, 'second_address': K2, 'feedback_causal': K3, 'missing_recognition': K4,
                           'contradiction_recognition': K5, 'correction': K6, 'research': K7, 'stopping': K8,
                           'negative_controls': K9, 'native_autonomous_engine': 'NOT_ESTABLISHED'}
D829['verdict835'] = {'verdict': verdict835, 'criteria': CRIT835, 'budget_stop': BUDGET_STOP835, 'runs': len(EV835),
                      'interpretation_guard': 'Tensor movement, convergence and attention mass never count as success.'}
D829['claims_ledger835'] = dict(CLAIMS835, demonstrated_by_TEST835={'verdict': verdict835, 'criteria': CRIT835,
                                                                     'terminal_correct': term, 'second_address': hits2})
D829['cost835'] = {'counted_numeric': COUNT_NUMERIC835, 'counted_calibration_phase': COUNT_CAL835,
                   'counted_total_including_offline': dict(COUNT834), 'predicted_upper': POST835,
                   'numeric_seconds_eval': D829['numeric_seconds835'], 'total_seconds_body': round(time.perf_counter() - T0_835, 3),
                   'peak_gpu_gib': float(_torch829.cuda.max_memory_allocated()) / 2**30}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f835:
    wr835 = csv.DictWriter(f835, fieldnames=['world', 'condition', 'first', 'second_FEEDBACK', 'second_OFF'] +
                           ['term_' + st for st in STATES835] + ['text_FEEDBACK'])
    wr835.writeheader()
    for e in EV835:
        row = {'world': e['world'], 'condition': e['condition'], 'first': e['first_role'],
               'second_FEEDBACK': e['second']['FEEDBACK']['role'], 'second_OFF': e['second']['OFF']['role'],
               'text_FEEDBACK': ' '.join(e['terminal']['FEEDBACK']['text_classes'])}
        for st in STATES835:
            t = e['terminal'][st]
            row['term_' + st] = ('OK ' if t['ok'] else 'NO ') + t['decision'] + ':' + ' '.join(x or '' for x in t['K_roles'])
        wr835.writerow(row)
D829['status'] = 'COMPLETE_TEST835_EVALUATED' if not BUDGET_STOP835 else 'STOPPED_BUDGET_PARTIAL_EVALUATED'
save829()
log829('TEST835_REPORT', json.dumps(REPORT835, default=str))
log829('TEST835_CAPABILITIES', json.dumps(D829['capabilities835']))
log829('TEST835_COST', json.dumps(D829['cost835'], default=str))
log829('TEST835_VERDICT', json.dumps(D829['verdict835']))
log829('TEST835_COMPLETED', str(OUT829))
'''
BODY_SHA835 = hashlib.sha256(BODY835.encode()).hexdigest()
PANEL_HOOK835 = ("PANEL829['test835'] = {'runs': RUNS835, 'calibration_blocks': CALBLOCKS835, 'eval_store': EVALSTORE835, "
                 "'cal_store': CALSTORE835, 'hypotheses': %r, 'body_sha256': %r, 'helpers_sha256': %r, 'constants': %r, "
                 "'seed': SEED829}\n" % (HYP835, BODY_SHA835, HELPER_SHA835,
                                         {'R1': R1_835, 'R2': R2_835, 'states': list(STATES835), 'conditions': list(CONDS835),
                                          'max_new_text': MAX_NEW_TEXT835, 'mam': [BETA834, PEAK_A834, PCA_RANK834, TOKEN_K834, BUDGET834]}))
src835 = patch835(src835, "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))",
                  PANEL_HOOK835 + "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))")
OFFLINE_HOOK835 = r'''
OFFLINE835 = DIR829 / 'TEST835_offline_key.json'   # never read by any runtime computation
OFFLINE835.write_text(json.dumps({'note': 'OFFLINE ONLY', 'runs': RUNKEY835, 'worlds': worlds829, 'calibration_worlds': CALW835,
                                  'questions': questions829, 'card_meta': card_meta829}, ensure_ascii=False, indent=2), encoding='utf-8')
D829['offline_key835_sha256'] = sha829(OFFLINE835.read_bytes())
'''
src835 = patch835(src835, "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n",
                  "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n" + OFFLINE_HOOK835)
start835 = src835.index("    # RUN ORDER: integrity checks")
start835 = src835.rfind("    # ---", 0, start835)
end835 = src835.index("except BaseException as e:\n    D829['status'] = 'ERROR'", start835)
BODY835_TEXT = BODY835
replacement835 = "\n".join("    " + line if line else "" for line in BODY835.strip("\n").splitlines()) + "\n"
patched835 = src835[:start835] + replacement835 + src835[end835:]
ast.parse(patched835)
# ==================================================================================================================
# CONSOLE / LOGGING LAYER ONLY. Nothing below changes what is computed: BODY835, the patched engine, the panel, the
# calibration, the controls and the evaluation are executed exactly as above. Every byte that the engine prints is
# written unchanged to a full transcript file; the Colab screen shows only a compact digest, progress, failures,
# and the final scientific summary read from the saved results (D829).
# ==================================================================================================================
import os as _os835, sys as _sys835, io as _io835, traceback as _tb835, datetime as _dt835, shutil as _sh835
from pathlib import Path as _P835
_os835.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')     # download bars only (not data)
for _m835, _f835 in (('huggingface_hub', lambda m: m.utils.disable_progress_bars()),
                     ('transformers', lambda m: m.utils.logging.disable_progress_bar())):
    if _m835 in _sys835.modules:                                    # only if already imported: no new import, no version effect
        try:
            _f835(_sys835.modules[_m835])
        except Exception:
            pass
_ROOT835 = _P835('/content') if _P835('/content').exists() else _P835('/tmp')
FULL_CONSOLE835 = _ROOT835 / ('TEST835_full_console_' + _dt835.datetime.now(_dt835.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.txt')
CON835 = {'phase': 'SOURCE_VERIFICATION', 'runs_done': 0, 'runs_total': None, 'cal_done': 0, 'cal_total': None,
          'last': [], 'fail_lines': [], 't0': time.time(), 'run_dir': None}
_ORIG_OUT835, _ORIG_ERR835 = _sys835.stdout, _sys835.stderr

def say835(*a):
    _ORIG_OUT835.write(' '.join(str(x) for x in a) + '\n'); _ORIG_OUT835.flush()

def _mins835():
    return round((time.time() - CON835['t0']) / 60.0, 1)

def route835(line):
    """Decide what (if anything) of one engine output line is shown on screen. The line itself is already in the file."""
    s = line.strip()
    if not s:
        return
    CON835['last'] = (CON835['last'] + [s[:300]])[-6:]
    if s.startswith('FAIL '):
        CON835['fail_lines'].append(s[:600]); say835('!! ' + s[:600]); return
    if s.startswith('TEST829_FAILED'):
        CON835['fail_lines'].append(s[:300]); return
    if s.startswith('TEST829_START'):
        parts = s.split()
        CON835['run_dir'] = parts[1] if len(parts) > 1 else None
        say835('Çalışma: %s | panel SHA-256: %s' % (parts[1] if len(parts) > 1 else '?', parts[-1]))
        CON835['phase'] = 'ENGINE_PRELUDE_AND_LOCKS'; return
    if s.startswith('TEST815_GPU_PREFLIGHT'):
        say835('GPU: ' + s[len('TEST815_GPU_PREFLIGHT'):].strip()); return
    if s.startswith('TEST815_GPU_FREE_GIB'):
        say835('GPU boş VRAM (yükleme öncesi): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('TEST835_PREDICTED_COST_BEFORE_MODEL_LOAD'):
        try:
            c = json.loads(s.split(' ', 1)[1]); u = c['numeric_upper']
            say835('Maliyet üst sınırı (model yükleme hariç): %s dk | kartuş %s (~%s MB) | fusion<=%s probe<=%s | VRAM %s'
                   % (c['minutes_upper_excluding_model_load'], c['physical_cartridges'], c['cartridge_disk_mb_estimate'],
                      u['fusion_forwards'], u['probe_forwards'], c['peak_vram_gib_expected']))
        except Exception:
            say835(s[:300])
        CON835['phase'] = 'MODEL_LOAD'; say835('Model yükleniyor (Qwen2.5-72B-Instruct, NF4, tek yükleme)...'); return
    if s.startswith('PASS FROZEN_PREFIX'):
        D_ = globals().get('D829', {})
        say835('Model yüklendi (%s s). Fiziksel kartuşlar üretiliyor ve SHA doğrulanıyor...' % D_.get('model_load_seconds', '?'))
        CON835['phase'] = 'PHYSICAL_CARTRIDGE_FORGING'; return
    if s.startswith('PASS PHYSICAL_COUNT'):
        say835('Fiziksel kartuşlar: ' + s.split()[-1] + ' (her biri SHA-256 + tensör SHA ile yeniden yüklendi)')
        CON835['phase'] = 'PREFLIGHT_GATES'; return
    if s.startswith('PASS ARCH_DIMS'):
        say835('Mimari (NL,H,QH,KVH,HD): ' + s[len('PASS ARCH_DIMS'):].strip() + ' | BF16 hesap, NF4, ağırlıklar donmuş'); return
    if s.startswith('PASS VRAM_HEADROOM'):
        say835('Boş VRAM (model sonrası): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('PASS HEADPROBE_EQUALS_LOCKED_ATTENTION_PROBE'):
        say835('Eşdeğerlik kapıları geçti (CUT3/hidden bitwise, HeadProbe farkı ' + s.split()[-1] + ')'); return
    if s.startswith('TEST835_CALIBRATION_START'):
        try:
            CON835['cal_total'] = int(s.split()[1])
        except Exception:
            pass
        CON835['phase'] = 'CALIBRATION'; say835('Kalibrasyon başladı (ayrı dünyalar): %s iş' % CON835['cal_total']); return
    if s.startswith('TEST835_CALIBRATION_JOB'):
        CON835['cal_done'] += 1
        if CON835['cal_total'] and (CON835['cal_done'] % 6 == 0 or CON835['cal_done'] == CON835['cal_total']):
            say835('  kalibrasyon %d/%d (%s dk)' % (CON835['cal_done'], CON835['cal_total'], _mins835()))
        return
    if s.startswith('TEST835_LOCK '):
        try:
            L = json.loads(s.split(' ', 1)[1])
            fh = L['first_head_calibration']; shc = L['second_head_calibration']
            say835('Kilit (kalibrasyon, örnek içi): ilk baş L%s/H%s %s/%s' % (L['first_head'][0], L['first_head'][1], fh['hits'], fh['of']))
            say835('  ikinci baş: ' + ' | '.join('%s L%s/H%s %s/%s' % (st, L['second_heads'][st][0], L['second_heads'][st][1],
                                                                         shc[st]['hits'], shc[st]['of']) for st in L['second_heads']))
            say835('  yeterlilik kapısı: %s (kal. dengeli doğr. %.3f) | çelişki kapısı: %s (%.3f)'
                   % (L['sufficiency_feature'], L['sufficiency_stump']['cal_balanced_acc'], L['conflict_feature'],
                      L['conflict_stump']['cal_balanced_acc']))
        except Exception:
            say835(s[:300])
        CON835['phase'] = 'EVALUATION_RUNTIME'; return
    if s.startswith('TEST835_RESUME '):
        try:
            r = json.loads(s.split(' ', 1)[1])
            say835('Devam mekanizması: yeniden kullanılan koşu %s | %s' % (r.get('reused_runs'), r.get('reason')))
        except Exception:
            say835(s[:300])
        return
    if s.startswith('TEST835_HEARTBEAT '):
        parts = s.split()
        if len(parts) > 3 and parts[2] == '/':
            CON835['phase'] = 'EVALUATION_RUNTIME (koşu %s/%s işleniyor, %s)' % (parts[1], parts[3], parts[4] if len(parts) > 4 else '')
        return
    if s.startswith('TEST835_RUN ') or s.startswith('TEST835_RUN_RESUMED'):
        CON835['runs_done'] += 1; n = CON835['runs_done']; tot = len(globals().get('RUNS835', [])) or 36
        CON835['phase'] = 'EVALUATION_RUNTIME run %d/%d' % (n, tot)
        if n % 6 == 0 or n == tot:
            say835('  koşu %d/%d (%s dk)' % (n, tot, _mins835()))
        return
    if s.startswith('TEST835_BUDGET_STOP'):
        say835('!! ' + s); return
    if s.startswith('TEST835_OFFLINE_START'):
        CON835['phase'] = 'OFFLINE_ORACLE_TEXT_AND_EVALUATION'
        say835('Sayısal çalışma bitti; çevrimdışı oracle tanısı, metin okuması ve değerlendirme (%s dk)' % _mins835()); return
    if s.startswith('TEST835_COMPLETED'):
        CON835['phase'] = 'COMPLETED'; return

class Console835(_io835.TextIOBase):
    """Writes everything to FULL_CONSOLE835 unchanged; routes complete lines to the compact screen digest."""
    def __init__(self, orig, fh):
        self.orig = orig; self.fh = fh; self.buf = ''
    def writable(self):
        return True
    @property
    def encoding(self):
        return 'utf-8'
    def isatty(self):
        return False
    def fileno(self):
        return self.orig.fileno()
    def write(self, x):
        if not isinstance(x, str):
            x = str(x)
        if self.fh.closed:                     # after the cell: late writers (e.g. logging handlers) go to the screen
            return self.orig.write(x)
        self.fh.write(x)
        self.buf += x
        while '\n' in self.buf:
            line, self.buf = self.buf.split('\n', 1)
            try:
                route835(line.split('\r')[-1])
            except Exception as e:
                self.fh.write('\n[console-layer route error ' + repr(e) + ']\n')
        if len(self.buf) > 20000:
            self.buf = self.buf[-2000:]
        return len(x)
    def flush(self):
        try:
            self.fh.flush()
        except Exception:
            pass

def sha_path835(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()

def files835():
    out = []
    d = globals().get('DIR829')
    if d is not None and _P835(d).exists():
        for p in sorted(_P835(d).iterdir()):
            if p.is_file():
                out.append((str(p), p.stat().st_size, sha_path835(p)))
    return out

def fmt835(x):
    if isinstance(x, list) and len(x) == 2 and all(isinstance(v, (int, float)) for v in x):
        return '%s/%s' % (x[0], x[1])
    if isinstance(x, dict):
        return ', '.join('%s=%s' % (k, fmt835(v)) for k, v in x.items())
    if isinstance(x, float):
        return '%.4g' % x
    return str(x)

def final835(D):
    R = D['report835']; V = D['verdict835']; L = D['lock835']; C = D['cost835']; K = V['criteria']
    ST = list(R['Q2_second_address_accuracy_given_own_first'])
    checks = D.get('checks', [])
    say835('=' * 78); say835('TEST835 SONUÇ ÖZETİ'); say835('=' * 78)
    say835('Durum: %s | koşu: %s | devamdan alınan: %s | bütçe durdurması: %s' % (D.get('status'), V['runs'], R['resumed_runs'], V['budget_stop']))
    say835('Bütünlük: %d kapı, %d başarısız | probe eşdeğerliği: %s' % (len(checks), sum(not c['pass'] for c in checks),
                                                                      fmt835(D.get('probe_equivalence835', {}))))
    say835('Donmuş ağırlık / hook yok / SDPA ve lm_head geri yüklendi: %s' % all(
        c['pass'] for c in checks if c['name'] in ('FROZEN_WEIGHT_SENTINEL', 'NO_RESIDUAL_HOOKS', 'NO_ATTENTION_HOOKS',
                                                    'SDPA_RESTORED_FINAL', 'LM_HEAD_UNWRAPPED')))
    fh = L['first_head_calibration']; shc = L['second_head_calibration']
    say835('Kilit (örnek içi kalibrasyon): ilk baş L%d/H%d %d/%d; ikinci baş %s' % (L['first_head'][0], L['first_head'][1], fh['hits'], fh['of'],
           '; '.join('%s L%d/H%d %d/%d' % (st, L['second_heads'][st][0], L['second_heads'][st][1], shc[st]['hits'], shc[st]['of']) for st in ST)))
    say835('Kapılar: yeterlilik=%s (kal. %.3f), çelişki=%s (kal. %.3f)' % (L['sufficiency_feature'], L['sufficiency_stump']['cal_balanced_acc'],
                                                                          L['conflict_feature'], L['conflict_stump']['cal_balanced_acc']))
    q1 = R['Q1_first_address_accuracy']
    say835('-' * 78); say835('[Q1] İLK ADRES')
    say835('  native ilk baş: %s | MAM PEAK50: %s | 815 numeric_rank: %s' % (fmt835(q1['native_first_head']), fmt835(q1['mam_peak50']), fmt835(q1['rank815'])))
    say835('  seçilen roller: ' + fmt835(q1['first_head_roles']))
    say835('  marj (doğru / yanlış seçimde): %s / %s | ters sırada aynı ilk kart: %s' % (fmt835(q1['first_margin_mean_correct']),
                                                                                       fmt835(q1['first_margin_mean_wrong']), fmt835(q1['order_reversal_same_first'])))
    say835('[Q2] İKİNCİ ADRES (ilk kart doğruyken)')
    for st in ST:
        say835('  %-11s %s | roller: %s' % (st, fmt835(R['Q2_second_address_accuracy_given_own_first'][st]), fmt835(R['Q2_second_roles'][st])))
    say835('  oracle tavanı (c1 yanlış koşularda gerçek ilk kartla; yetenek sayılmaz): ' + fmt835(R['Q2_oracle_ceiling_runs_with_wrong_c1']))
    q3 = R['Q3_feedback_causal']
    say835('[Q3] GERİ BESLEME NEDENSELLİĞİ')
    say835('  ikinci adres isabeti: ' + fmt835(q3['second_address']))
    say835('  terminal doğru: ' + fmt835(q3['terminal_correct']))
    say835('  FEEDBACK-OFF uyumsuz çiftler (FB doğru&OFF yanlış / tersi): %s | durumun hidden\'ı değiştirdiği koşu: %s'
           % (fmt835(q3['discordant_FEEDBACK_vs_OFF']), q3['hidden_moved_by_state']))
    say835('[Q4] EKSİK BİLGİ / UNKNOWN')
    for st in ST:
        q = R['Q4_missing'][st]
        say835('  %-11s eksikte INSUFFICIENT %s/12 | eksikte metin UNKNOWN %s/12 | tam kanıtta INSUFFICIENT %s'
               % (st, q['insufficient_on_missing'], q['text_unknown_on_missing'], q['insufficient_on_complete']))
    say835('[Q5] ÇELİŞKİ')
    say835('  ' + ' | '.join('%s: çelişkide CONFLICT %s/6, yanlış CONFLICT %s' % (st, R['Q5_contradiction'][st]['conflict_on_conflict'],
                                                                                R['Q5_contradiction'][st]['false_conflict']) for st in ST))
    say835('[Q6] YANLIŞ İLK ADRESİ DÜZELTME: ' + fmt835(R['Q6_correction']))
    say835('[Q7] YENİDEN ARAMA (ilk ikinci aday yanlışken): ' + fmt835(R['Q7_research']))
    say835('[Q8] DURMA')
    for st in ST:
        q = R['Q8_stopping'][st]
        say835('  %-11s doğru %s/36 | erken SUFFICIENT %s | yanlış CONFLICT %s | tam kanıtta bütçe-UNKNOWN %s | %s'
               % (st, q['correct'], q['premature_sufficient'], q['false_conflict'], q['budget_abstention_on_complete'], fmt835(q['stop_types'])))
    say835('[KOŞUL BAZINDA terminal doğruluk]')
    for st in ST:
        say835('  %-11s %s' % (st, fmt835(R['by_condition_terminal_correct'][st])))
    say835('[METİN CEVAPLARI, çevrimdışı] ' + fmt835(R['text_correct']))
    say835('[KARAR SINIFLARI] A=model sinyali, B=sabit kapı, C=Python planı')
    for k, v in R['decision_classes'].items():
        say835('  %s: %s' % (k, v))
    say835('-' * 78); say835('K1–K9')
    detail = {'K1_FIRST_ADDRESS': fmt835(q1['native_first_head']),
              'K2_SECOND_ADDRESS': fmt835(R['Q2_second_address_accuracy_given_own_first'].get('FEEDBACK')),
              'K3_FEEDBACK_CAUSAL': fmt835(q3['second_address']),
              'K4_MISSING': 'eksikte INSUFFICIENT %s/12, tam kanıtta doğru terminal %s/24' % (
                  R['Q4_missing']['FEEDBACK']['insufficient_on_missing'],
                  sum(R['by_condition_terminal_correct']['FEEDBACK'][c][0] for c in ('FULL', 'MISLEAD_FIRST', 'REPLACE_SECOND_BY_ALT', 'CONFLICT_ALT_ADDED'))),
              'K5_CONTRADICTION': '%s/6, yanlış %s' % (R['Q5_contradiction']['FEEDBACK']['conflict_on_conflict'], R['Q5_contradiction']['FEEDBACK']['false_conflict']),
              'K6_CORRECTION': fmt835(R['Q6_correction'].get('FEEDBACK')), 'K7_RESEARCH': fmt835(R['Q7_research'].get('FEEDBACK')),
              'K8_STOPPING': '%s/36' % R['Q8_stopping']['FEEDBACK']['correct'], 'K9_NEGATIVE_CONTROLS': fmt835(q3['terminal_correct'])}
    for k in K:
        say835('  %-22s %-12s %s' % (k, K[k], detail.get(k, '')))
    say835('Negatif kontroller karşısında: ' + fmt835(R['Q9_which_survive_negative_controls']))
    say835('Otonom native motor: ' + R['Q10_autonomous_native_recursive_engine'])
    # Predeclared presentation mapping of the TEST835 verdict (no new criterion): PASS->DEVAM, FAIL->DUR, else YETERSİZ KANIT.
    dec = {'PASS': 'DEVAM', 'FAIL': 'DUR', 'INCONCLUSIVE': 'YETERSİZ KANIT'}.get(V['verdict'], 'YETERSİZ KANIT')
    say835('=' * 78)
    say835('NİHAİ BİLİMSEL KARAR: %s  (TEST835 verdict = %s)' % (dec, V['verdict']))
    failed = [k for k, v in K.items() if v == 'FAIL']; inc = [k for k, v in K.items() if v == 'INCONCLUSIVE']
    say835('  Başarısız ölçütler: ' + (', '.join(failed) if failed else 'yok'))
    say835('  Belirsiz ölçütler: ' + (', '.join(inc) if inc else 'yok'))
    if dec == 'DUR':
        why = []
        if K.get('K2_SECOND_ADDRESS') == 'FAIL':
            why.append('K2 FAIL: ilk kart doğruyken FEEDBACK ikinci adresi %s (eşik %%75)' % fmt835(R['Q2_second_address_accuracy_given_own_first'].get('FEEDBACK')))
        if K.get('K3_FEEDBACK_CAUSAL') == 'FAIL':
            why.append('K3 FAIL: FEEDBACK ikinci adres isabeti kontrolleri +3 farkla geçemedi (%s)' % fmt835(q3['second_address']))
        if K.get('K8_STOPPING') == 'FAIL' and K.get('K9_NEGATIVE_CONTROLS') == 'FAIL':
            why.append('K8+K9 FAIL: terminal doğru %s/36 ve negatif kontrollerden ayrışmadı (%s)'
                       % (R['Q8_stopping']['FEEDBACK']['correct'], fmt835(q3['terminal_correct'])))
        for w_ in why:
            say835('  Gerekçe: ' + w_)
    elif dec == 'DEVAM':
        say835('  Gerekçe: tüm önceden sabitlenmiş ölçütler geçti; döngü planı yine de C sınıfıdır (otonom native motor kanıtlanmadı).')
    else:
        say835('  Gerekçe: ölçütler ne kesin geçiş ne kesin başarısızlık kuralını sağladı (veya bütçe durdurması).')
    say835('Maliyet: sayılan %s | değerlendirme %s s | toplam gövde %s s | tepe VRAM %.2f GiB'
           % (fmt835(C['counted_total_including_offline']), C['numeric_seconds_eval'], C['total_seconds_body'], C['peak_gpu_gib']))

def files_report835():
    say835('=' * 78); say835('SONUÇ DOSYALARI (SHA-256)')
    for path, size, sh in files835():
        say835('  %s  %d B  %s' % (path, size, sh))

say835('=' * 78)
say835('AKBASCORE TEST835 — model Qwen2.5-72B-Instruct (NF4, donmuş), tek A100-80GB, tek hücre')
say835('Kaynak kilitleri: 829.py %s | 834.py %s | 834.log %s' % (LOCK829_835, LOCK834_835, LOCK834LOG_835))
say835('TEST834 yardımcıları (AST, %d fonksiyon) SHA-256 %s' % (len(HELPERS835), HELPER_SHA835))
say835('BODY835 SHA-256 %s | yamalı kaynak AST geçti (%d bayt, SHA-256 %s)' % (BODY_SHA835, len(patched835), hashlib.sha256(patched835.encode()).hexdigest()))
say835('Kapsam: %d değerlendirme dünyası x %d koşul = %d koşu; %d ayrı kalibrasyon dünyası; durumlar %s'
       % (WORLDS_EVAL835, len(CONDS835), WORLDS_EVAL835 * len(CONDS835), CAL_WORLDS835, '/'.join(STATES835)))
say835('Tam konsol kaydı: ' + str(FULL_CONSOLE835))
say835('=' * 78)
_fh835 = open(FULL_CONSOLE835, 'a', encoding='utf-8', buffering=1)
_fh835.write(SOURCE_LINE835 + '\nTEST835_BODY_SHA256 ' + BODY_SHA835 + '\nTEST835_HELPERS_FROM_TEST834 ' + HELPER_SHA835 + ' ' +
             str(len(HELPERS835)) + '\nTEST835_PATCHED_SOURCE_AST_PASS ' + str(len(patched835)) + ' ' +
             hashlib.sha256(patched835.encode()).hexdigest() + '\n')
import linecache as _lc835                       # source text for tracebacks of exec-compiled code (display only)
for _nm835, _src835 in (('TEST835_LOCKED_ENGINE', patched835), ('TEST834_LOCKED_HELPERS', HELPER_SRC835)):
    _lc835.cache[_nm835] = (len(_src835), None, [x + '\n' for x in _src835.splitlines()], _nm835)
_sys835.stdout = Console835(_ORIG_OUT835, _fh835); _sys835.stderr = Console835(_ORIG_ERR835, _fh835)
TEST835_ERROR = None
try:
    exec(compile(patched835, 'TEST835_LOCKED_ENGINE', 'exec'), globals())
except BaseException as _e835:
    TEST835_ERROR = _e835
    _tbtext835 = _tb835.format_exc()
    _fh835.write('\n[TEST835 OUTER EXCEPTION]\n' + _tbtext835)
finally:
    _sys835.stdout, _sys835.stderr = _ORIG_OUT835, _ORIG_ERR835
    try:
        _fh835.flush(); _fh835.close()
    except Exception:
        pass
    _dir835 = globals().get('DIR829')
    if _dir835 is not None and _P835(_dir835).exists() and FULL_CONSOLE835.exists():
        _dst835 = _P835(_dir835) / FULL_CONSOLE835.name
        _sh835.move(str(FULL_CONSOLE835), str(_dst835)); FULL_CONSOLE835 = _dst835
if TEST835_ERROR is not None:
    D_ = globals().get('D829', {}) if isinstance(globals().get('D829'), dict) else {}
    bad = [c for c in D_.get('checks', []) if not c.get('pass')]
    say835('=' * 78); say835('TEST835 HATA')
    say835('Tür: %s.%s' % (type(TEST835_ERROR).__module__, type(TEST835_ERROR).__name__))
    say835('Mesaj: ' + repr(TEST835_ERROR)[:800])
    say835('Aşama: ' + CON835['phase'] + ' | koşu %s | kalibrasyon %s | geçen %s dk' % (CON835['runs_done'], CON835['cal_done'], _mins835()))
    if bad:
        say835('Başarısız kapı: %s | ayrıntı: %s' % (bad[-1].get('name'), str(bad[-1].get('detail'))[:400]))
    say835('Hata öncesi son motor satırları:')
    for x in CON835['last'][-4:]:
        say835('  ' + x[:240])
    tbl = _tbtext835.rstrip().splitlines()
    say835('Traceback (son %d satır; tamamı dosyada ve results.json içinde):' % min(40, len(tbl)))
    for x in tbl[-40:]:
        say835('  ' + x)
    files_report835()
    say835('Tam konsol kaydı: %s  SHA-256 %s' % (FULL_CONSOLE835, sha_path835(FULL_CONSOLE835) if FULL_CONSOLE835.exists() else '-'))
    raise SystemExit('TEST835_FAILED: ' + type(TEST835_ERROR).__name__)
try:
    final835(D829)
except Exception as _e835s:
    say835('!! Özet basılamadı (veri dosyalarda tam): ' + repr(_e835s))
    say835(_tb835.format_exc()[-1500:])
files_report835()
say835('  (tam konsol kaydı yukarıdaki listede: ' + FULL_CONSOLE835.name + ')')
say835('=' * 78)
