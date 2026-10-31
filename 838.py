# AKBASCORE SILICON HIPPOCAMPUS — TEST838, single Colab cell (one A100-SXM4-80GB, frozen Qwen2.5-72B-Instruct NF4).
# IS THE RELATIONAL-COMPLETION INFORMATION THAT RHO EXTRACTS FROM FOUR COUNTERFACTUAL MOUNTS PRESENT IN ONE NATIVE FORWARD?
#   P1  Information dependence of the physical pair: NULL, FIRST_ONLY, SECOND_ONLY, TRUE_PAIR, ALT_PAIR, FORK_PLUS_SECOND,
#       FIRST_PLUS_MIRROR, DECOY_PLUS_FIRST, IRRELEVANT_PAIR (another world's complete chain); both pair orders. Endpoint
#       and UNKNOWN are separate success categories (offline answer text); first-answer-token distribution and hidden
#       states are recorded.
#   P2  Single-forward candidate signals (predeclared list), each from ONE forward of ONE mount; one-feature stumps and
#       difference-of-means directions are fitted on CALIBRATION worlds only and applied unchanged to sealed EVALUATION
#       worlds (3 with the calibration card template, 3 with an unseen template and new names). rho (4 mounts) is
#       computed only as an offline reference and never enters any decision.
#   P3  First-memory addressing: (B1) single-card signals, first vs fork vs decoy vs other-world first; (B2) an
#       ordered-pair scan of the whole bank with the selected single-forward signal (CLASS C external search),
#       executed only if the calibration accuracy of the selected signal reaches a predeclared gate.
# Classes: A = native numbers (hidden, CUT3, attention, next-token law); B = calibrated direction / stump / argmax;
# C = Python trying pairs and mounting. Native control of the next computation is NOT tested here and is reported as
# NOT_DEMONSTRATED. Locked parts: TEST829 source (blob a5a25460), TEST834 helpers (834.py blob ab7b2046), TEST837
# skeleton and console (837.py blob 2049a98b). No GPU execution or result is claimed by the code author.
import urllib.request, hashlib, ast, json, time, random, math, re, numpy as np

REPO838 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
LOCK829_838 = "a5a25460a3a6bbdf62a0571a9b5ff19e64159cf7"
LOCK834_838 = "ab7b2046d7b7e7be18aed8c6ce5a1397e0c991d7"
LOCK837_838 = "2049a98b19ddfc0517cf23e8cec2d20061f0ee84"
LOCK837LOG_838 = "d64c63eeb0e57441f71e0e19a7adae07b4bc8f3d"   # prior evidence (read-only)
SEED838 = 8382026
EXPECTED_ARCH834 = (80, 8192, 64, 8, 128)
DEVICE_KIND838 = 'cuda'
CAL_WORLDS838 = 8
EVAL_WORLDS838 = 6            # first 3: calibration template; last 3: unseen template + new names
BLOCK838 = 3
# Predeclared single-forward candidate signals (order = tie order). Every value is read from ONE forward of ONE mount;
# *_PROJ = unit final-norm hidden (or CUT3 state) projected on a CONSTANT direction fitted on calibration worlds only.
GROUP838 = {'Q_HIDDEN_PROJ': 'REPRESENTATIONAL', 'Q_HIDDEN_PROJ_ORTH_UNK': 'REPRESENTATIONAL',
            'Q_CUT3_PROJ': 'REPRESENTATIONAL', 'Q_ATTN_BALANCE': 'REPRESENTATIONAL',
            'A_HIDDEN_PROJ': 'BEHAVIOURAL', 'A_HIDDEN_PROJ_ORTH_UNK': 'BEHAVIOURAL', 'A_ENTROPY': 'BEHAVIOURAL',
            'A_TOP1_PROB': 'BEHAVIOURAL', 'A_LOGP_UNKNOWN': 'UNKNOWN_WORD', 'A_UNK_GAP': 'UNKNOWN_WORD',
            'Q_LOGP_UNKNOWN': 'UNKNOWN_WORD'}
SIGNALS838 = tuple(GROUP838)
REPRESENTATIONAL838 = tuple(s for s in SIGNALS838 if GROUP838[s] == 'REPRESENTATIONAL')   # question frame, no instruction
CONTROLS838 = ('CTRL_ATTN_CARD_MASS', 'CTRL_MOUNT_TOKENS')     # confound controls in the D2 criterion, never selected
DESCRIPTIVE838 = ('DESC_HIDDEN_NORM',)   # native magnitude, reported only (it may carry the same information; not a veto)
FRAME_OF838 = {s: s[0] for s in SIGNALS838}                                                  # 'Q' or 'A'
D2_BAL838, D2_FP838, D2_SUB838, D2_CTRL_GAP838, D2_P838 = 0.85, 0.25, 0.75, 0.10, 0.01
D1_PAIR838, D1_SINGLE838, B2_NEED838 = 10, 5, 5
NPERM838 = 10000
B2_GATE838 = 0.80             # calibration balanced accuracy needed to run the B2 pair scan (decided on calibration)
MAX_NEW_TEXT838 = 10
SEC_FUSION838, SEC_PROBE838, MARGIN838 = 0.95, 1.2, 1.25    # TEST837 measured ~0.92 s/forward; 25 % safety margin
PRED_LIMIT_MIN838 = 240.0
HARD_BUDGET_MIN838 = 300.0
RESUME838 = True

def fetch838(name, lock, limit=400000):
    with urllib.request.urlopen(urllib.request.Request(REPO838 + name, headers={"User-Agent": "AKBASCORE-TEST838"}),
                                timeout=180) as f:
        raw = f.read(limit + 1)
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert len(raw) <= limit and blob == lock, ("STOP_SOURCE_CHANGED", name, blob)
    return raw

raw829_838 = fetch838("829.py", LOCK829_838)
raw834_838 = fetch838("834.py", LOCK834_838)
raw837_838 = fetch838("837.py", LOCK837_838)
raw837log_838 = fetch838("837.log", LOCK837LOG_838)
src838 = raw829_838.decode("utf-8")

def extract838(raw, body_name, names):
    tree = ast.parse(raw.decode("utf-8"))
    bodies = [n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == body_name]
    assert len(bodies) == 1, ('BODY_NOT_UNIQUE', body_name)
    text = bodies[0].value.value
    nodes = [n for n in ast.parse(text).body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert sorted(n.name for n in nodes) == sorted(names), ('HELPER_SET_MISMATCH', body_name)
    return "\n\n".join(ast.get_source_segment(text, n) for n in nodes)
HELPERS834_838 = ('HeadProbe834', 'concat834', 'rprobe834', 'seal834', 'mount834', 'cspans834', 'card_mass834', 'stump_fit834')
HELPERS837_838 = ('load_npz837',)
HELPER_SRC838 = extract838(raw834_838, 'BODY834', HELPERS834_838) + "\n\n" + extract838(raw837_838, 'BODY837', HELPERS837_838)
HELPER_SHA838 = hashlib.sha256(HELPER_SRC838.encode()).hexdigest()
HELPERS838 = HELPERS834_838 + HELPERS837_838

def patch838(text, old, new):
    assert text.count(old) == 1, ("PATCH_ANCHOR_NOT_UNIQUE", old[:80], text.count(old))
    return text.replace(old, new, 1)

src838 = patch838(src838, "SEED829 = 8292026", "SEED829 = %d" % SEED838)
src838 = patch838(src838, "RUN829 = 'TEST829_'", "RUN829 = 'TEST838_'")
src838 = patch838(src838, "WORLDS829 = 3                    # small pilot (directive); no automatic extension",
                  "WORLDS829 = %d                    # TEST838 sealed evaluation worlds" % EVAL_WORLDS838)
for a838, b838 in (("'TEST829_results.json'", "'TEST838_results.json'"), ("'TEST829.log'", "'TEST838.log'"),
                   ("'TEST829_blind_review.csv'", "'TEST838_case_table.csv'"),
                   ("'TEST829_offline_key.json'", "'TEST829_base_offline_key.json'")):
    src838 = patch838(src838, a838, b838)

PANEL_EXT838 = r'''
# ---------------- TEST838 PANEL EXTENSION (sealed before any model call) ----------------
TEMPLATES838 = {'STANDARD': lambda d, a, b: 'Evidence record. Domain: ' + d + '\n' + 'Directed relation: ' + a + ' -> ' + b + '.\n',
                'UNSEEN': lambda d, a, b: 'Evidence record. Domain: ' + d + '\n' + 'Link: ' + a + ' leads to ' + b + '.\n'}
def fresh838():
    while True:
        c = code829()
        if c not in seen829:
            seen829.add(c); return c
# Evaluation worlds (base TEST829 generator: first/second/changed/decoy) + mirror/fork; worlds 3-5 use the unseen template.
for wi, w in enumerate(worlds829):
    w['template'] = 'STANDARD' if wi < BLOCK838 else 'UNSEEN'
    w['fork_end'] = fresh838()
    for kind in ('mirror', 'fork'):
        cid = 'E829_' + code829()
        assert cid not in cards829, 'CARD_ID_COLLISION'
        w['ids'][kind] = cid
    T = TEMPLATES838[w['template']]
    rel = {'first': (w['start'], w['middle']), 'second': (w['middle'], w['end']), 'changed': (w['middle'], w['changed_end']),
           'decoy': (w['decoy_end'], w['start']), 'mirror': (w['end'], w['middle']), 'fork': (w['start'], w['fork_end'])}
    for kind, (a, b) in rel.items():
        cards829[w['ids'][kind]] = T(w['world'], a, b)
        card_meta829[w['ids'][kind]] = {'domain': w['world'], 'kind': kind, 'body_sha256': sha829(cards829[w['ids'][kind]]),
                                        'split': 'evaluation', 'template': w['template']}
EVALSTORE838 = sorted(c for c in cards829 if c != NULL829)
# Calibration worlds: separate generator stream, calibration template only.
RNGC838 = random.Random(SEED829 + 838001)
def codec838():
    while True:
        c = ''.join(RNGC838.choice(ALPH829) for _ in range(9))
        if c not in seen829:
            seen829.add(c); return c
CALW838 = []
for ci in range(CAL_WORLDS838):
    cw = {'world': 'DOMAIN_' + codec838(), 'start': codec838(), 'middle': codec838(), 'end': codec838(),
          'changed_end': codec838(), 'decoy_end': codec838(), 'fork_end': codec838(), 'template': 'STANDARD', 'ids': {}}
    rel = {'first': ('start', 'middle'), 'second': ('middle', 'end'), 'changed': ('middle', 'changed_end'),
           'decoy': ('decoy_end', 'start'), 'mirror': ('end', 'middle'), 'fork': ('start', 'fork_end')}
    for kind, (a, b) in rel.items():
        cid = 'E829_' + codec838()
        assert cid not in cards829, 'CARD_ID_COLLISION'
        cw['ids'][kind] = cid
        cards829[cid] = TEMPLATES838['STANDARD'](cw['world'], cw[a], cw[b])
        card_meta829[cid] = {'domain': cw['world'], 'kind': kind, 'body_sha256': sha829(cards829[cid]),
                             'split': 'calibration', 'template': 'STANDARD'}
    cw['qid'] = cw['world'] + '_P0'
    assert cw['qid'] not in [q['qid'] for q in questions829], 'QID_COLLISION'
    cw['question'] = ('In domain {world}, starting from {start}, which endpoint is reached after exactly two directed '
                      'links?').format(**cw)
    CALW838.append(cw)
CALSTORE838 = sorted(c for cw in CALW838 for c in cw['ids'].values())
NAMES_E838 = {w[k] for w in worlds829 for k in ('world', 'start', 'middle', 'end', 'changed_end', 'decoy_end', 'fork_end')}
NAMES_C838 = {w[k] for w in CALW838 for k in ('world', 'start', 'middle', 'end', 'changed_end', 'decoy_end', 'fork_end')}
assert not (NAMES_E838 & NAMES_C838) and not (set(EVALSTORE838) & set(CALSTORE838)), 'SPLIT_LEAK'
assert len(NAMES_E838) == 7 * len(worlds829) and len(NAMES_C838) == 7 * len(CALW838), 'NAME_COLLISION'
FRAMES838 = ('Q', 'A')            # Q = question-only frame (prompt_ids(question)); A = TEST827 answer boundary frame
COND838 = ('NULL', 'FIRST_ONLY', 'SECOND_ONLY', 'FORK_ONLY', 'MIRROR_ONLY', 'DECOY_ONLY', 'CHANGED_ONLY',
           'TRUE_PAIR', 'ALT_PAIR', 'FORK_PLUS_SECOND', 'FIRST_PLUS_MIRROR', 'DECOY_PLUS_FIRST', 'IRRELEVANT_PAIR')
POSITIVE838 = ('TRUE_PAIR', 'ALT_PAIR')
NEGATIVE838 = ('FORK_PLUS_SECOND', 'FIRST_PLUS_MIRROR', 'DECOY_PLUS_FIRST', 'IRRELEVANT_PAIR')
def cond_mounts838(w, other):
    i = w['ids']; o = other['ids']
    singles = {'NULL': [NULL829], 'FIRST_ONLY': [i['first']], 'SECOND_ONLY': [i['second']], 'FORK_ONLY': [i['fork']],
               'MIRROR_ONLY': [i['mirror']], 'DECOY_ONLY': [i['decoy']], 'CHANGED_ONLY': [i['changed']],
               'OTHER_FIRST_ONLY': [o['first']], 'OTHER_SECOND_ONLY': [o['second']]}
    pairs = {'TRUE_PAIR': (i['first'], i['second']), 'ALT_PAIR': (i['first'], i['changed']),
             'FORK_PLUS_SECOND': (i['fork'], i['second']), 'FIRST_PLUS_MIRROR': (i['first'], i['mirror']),
             'DECOY_PLUS_FIRST': (i['decoy'], i['first']), 'IRRELEVANT_PAIR': (o['first'], o['second'])}
    out = {k: v for k, v in singles.items()}
    for k, (a, b) in pairs.items():
        out[k + '|FORWARD'] = [a, b]; out[k + '|REVERSE'] = [b, a]
    return out
_rng838 = random.Random(SEED829 + 38)
JOBS838, JOBMAP838 = [], {}
CALKEY838, EVALKEY838 = {}, {}      # CALKEY: calibration labels (usable for fitting); EVALKEY: offline key only
def job838(ids, qid, phase, role):
    k = (tuple(ids), qid)
    assert k not in JOBMAP838, 'DUPLICATE_JOB'
    j = 'J838_' + ''.join(_rng838.choice('0123456789ABCDEF') for _ in range(12))
    JOBMAP838[k] = j
    JOBS838.append({'job': j, 'mount': list(ids), 'qid': qid, 'phase': phase})
    (CALKEY838 if phase == 'CAL' else EVALKEY838)[j] = role
    return j
QID838 = {'CAL': [cw['qid'] for cw in CALW838], 'EVAL': [questions829[i]['qid'] for i in range(len(worlds829))]}
assert len(questions829) == len(worlds829), 'ONE_QUESTION_PER_WORLD'
for split, ws in (('CAL', CALW838), ('EVAL', worlds829)):
    for k, w in enumerate(ws):
        if split == 'EVAL':                                   # irrelevant chain from a world with the same template
            blk = k // BLOCK838
            other = ws[blk * BLOCK838 + (k + 1) % BLOCK838]
        else:
            other = ws[(k + 1) % len(ws)]
        q = QID838[split][k]
        for cond, m in cond_mounts838(w, other).items():
            job838(m, q, split, {'split': split, 'world': k, 'cond': cond})
# B2 banks (evaluation only): 18 cards = 3 worlds x 6 kinds, per template block; ordered pairs scanned if gated in.
BANKS838, BANKQ838 = [], []
for bi in range(0, len(worlds829), BLOCK838):
    b_ = [worlds829[i]['ids'][k] for i in range(bi, bi + BLOCK838) for k in ('first', 'second', 'changed', 'mirror', 'decoy', 'fork')]
    _rng838.shuffle(b_)
    BANKS838.append(b_)
    BANKQ838.append([QID838['EVAL'][i] for i in range(bi, bi + BLOCK838)])
_rng838.shuffle(JOBS838)
CALJOBS838 = [j for j in JOBS838 if j['phase'] == 'CAL']
EVALJOBS838 = [j for j in JOBS838 if j['phase'] == 'EVAL']
assert set(EVALKEY838) == {j['job'] for j in EVALJOBS838} and not (set(CALKEY838) & set(EVALKEY838)), 'KEY_PARTITION'

def fus_upper838(k, maxb, p_):
    if k <= 0:
        return 0
    c = int(globals().get('CHUNK', 128))
    return (p_ + maxb + c - 1) // c + (k - 1) * ((maxb + c - 1) // c)

def cost_upper838(tok_of, p_):
    mx = max(tok_of.values())
    up = {'fusion_forwards': 0, 'probe_forwards': 0, 'capture_forwards': 0, 'rank_forwards': 0, 'generation_forwards': 0}
    up['fusion_forwards'] += 3 * fus_upper838(2, mx, p_); up['probe_forwards'] += 2 + 3 + 1; up['generation_forwards'] += 1
    mounts = {tuple(j['mount']) for j in JOBS838}
    up['fusion_forwards'] += sum(fus_upper838(len(m), mx, p_) for m in mounts)
    up['probe_forwards'] += 2 * len(JOBS838)
    nb = len(BANKS838[0]); pairs = nb * (nb - 1)
    up['fusion_forwards'] += len(BANKS838) * pairs * fus_upper838(2, mx, p_)
    up['probe_forwards'] += len(BANKS838) * pairs * BLOCK838 * len(FRAMES838)        # worst case: both frames gated in
    off_f = sum(fus_upper838(len(m), mx, p_) for m in {tuple(j['mount']) for j in EVALJOBS838})
    off_g = len(EVALJOBS838) * MAX_NEW_TEXT838
    sec = MARGIN838 * ((up['fusion_forwards'] + off_f + off_g + up['generation_forwards']) * SEC_FUSION838 +
                       up['probe_forwards'] * SEC_PROBE838 + 120.0 + len(tok_of) * 2.0)
    return {'numeric_upper': up, 'offline_upper': {'fusion_forwards': off_f, 'generation_forwards': off_g},
            'jobs': len(JOBS838), 'cal_jobs': len(CALJOBS838), 'eval_jobs': len(EVALJOBS838), 'mounts': len(mounts),
            'b2_pair_mounts': len(BANKS838) * pairs, 'physical_cartridges': len(tok_of),
            'max_memory_tokens': max(p_ + sum(tok_of[c] for c in m) for m in mounts | {tuple(BANKS838[0][:2])}),
            'minutes_upper_excluding_model_load': round(sec / 60.0, 1),
            'cost_model': 'fusion %.2f s, probe %.2f s per forward (TEST837 measured ~0.92 s), x%.2f margin' % (SEC_FUSION838, SEC_PROBE838, MARGIN838),
            'scaling': scaling838()}

def scaling838():
    # ordered-pair scan without knowing the first card: N(N-1) pair mounts (one probe each per question); rho needs in
    # addition N single mounts and NULL. Seconds use the TEST837 measurement (~1.9 s per pair mount + one probe).
    out = {}
    for n in (18, 100, 1000, 1000000):
        pr = n * (n - 1)
        out[str(n)] = {'pair_mounts': pr, 'single_forward_scan_probes': pr, 'rho_mounts': pr + n + 1,
                       'seconds_at_1p9s': round(pr * 1.9, 1), 'years_at_1p9s': round(pr * 1.9 / 3.15576e7, 4),
                       'known_first_scan_pair_mounts': 2 * (n - 1)}
    return out
'''
src838 = patch838(src838,
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n",
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n" + PANEL_EXT838)
PRECOST838 = r'''
    PRE838 = cost_upper838(tok_counts829, 30)
    D829['predicted_cost838_pre_model'] = PRE838
    log829('TEST838_PREDICTED_COST_BEFORE_MODEL_LOAD', json.dumps(PRE838))
    gate829('TEST838_PREDICTED_BUDGET', PRE838['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN838,
            {'minutes_upper': PRE838['minutes_upper_excluding_model_load'], 'limit': PRED_LIMIT_MIN838})
'''
src838 = patch838(src838, "    del tok829\n", "    del tok829\n" + PRECOST838)

HYP838 = {
    'question': ('Is the relational-completion information that rho extracts from four counterfactual mounts readable '
                 'from ONE native forward of ONE physical mount, and does it generalise to unseen worlds, names and an '
                 'unseen card template?'),
    'labels': ('Structural, model-independent: a two-card mount is POSITIVE when it contains a complete two-link chain '
               'from the question start (TRUE_PAIR = first+second, ALT_PAIR = first+changed); NEGATIVE classes are '
               'FORK_PLUS_SECOND, FIRST_PLUS_MIRROR (same names as TRUE_PAIR), DECOY_PLUS_FIRST (complete chain that does '
               'not start at the question start) and IRRELEVANT_PAIR (complete chain of another world). Both card orders.'),
    'design_audit': [
        'First vs fork cannot be distinguished from a single card: "S -> M" and "S -> F" are symmetric until the card '
        'that continues M is present. Addressing without knowing the first card therefore needs a second card (pair) '
        'or the bank; B1 measures this predicted limitation, B2 is a class C ordered-pair scan.',
        'The answer frame (TEST827 boundary instruction) itself contains the word UNKNOWN; answer-frame signals are '
        'BEHAVIOURAL. Representational signals use the question-only frame (no instruction).',
        'Endpoint names are never used at runtime (that would leak the answer); UNKNOWN probability uses only the '
        'token ids of the word UNKNOWN, identical for every mount. Endpoint-token probabilities are computed offline only.',
        'Signals that are the UNKNOWN word probability (or its gap) are labelled UNKNOWN_WORD and cannot answer the '
        'question of general relational understanding. *_ORTH_UNK directions have the lm_head rows of the UNKNOWN '
        'tokens projected out, so they cannot act through the direct UNKNOWN logit.',
        'Positives and negatives are all two-card mounts of the same template (card count and format matched). '
        'FIRST_PLUS_MIRROR has the same entity names as TRUE_PAIR (token-identity control); both orders (position '
        'control); confound controls: total attention mass on the cards and mount token count (hidden-state norm '
        'is reported descriptively: it is itself a native carrier and cannot serve as a confound veto).',
        'Directions and stumps are fitted on calibration worlds only; selection and the B2 gate use leave-one-world-out '
        'cross-validation inside calibration; nothing is changed after evaluation measurements start.',
        'A signal computed by subtracting two forwards is not single-forward; projections use constant calibration '
        'vectors only. rho (four mounts) is computed offline as a class C reference only.'],
    'criteria': {
        'D1_PHYSICAL_DEPENDENCE': ('evaluation answer text: TRUE_PAIR gives the end and no other name and no UNKNOWN in '
                                   '>= 10 of 12 (world, order); FIRST_ONLY, SECOND_ONLY and NULL give UNKNOWN only in '
                                   '>= 5 of 6 worlds each.'),
        'D2_SINGLE_FORWARD_SIGNAL': ('the signal selected on calibration (best leave-one-world-out balanced accuracy, '
                                     'predeclared tie order) on the 72 evaluation pair mounts: balanced accuracy >= 0.85; '
                                     'false-positive rate <= 0.25 in every negative class; >= 0.75 on the unseen-template '
                                     'subset and in each order; >= best confound control + 0.10; label-permutation '
                                     'p <= 0.01.'),
        'D2R_REPRESENTATIONAL': 'the same criterion for the best question-frame REPRESENTATIONAL signal.',
        'D3_B1_SINGLE_CARD_ADDRESSING': ('reported only: calibrated first-vs-fork single-card classifiers evaluated blind '
                                         '(predicted chance by symmetry) and top-1 of the first card among 8 singles.'),
        'D3_B2_PAIR_SCAN': ('only for a signal whose calibration cross-validated balanced accuracy >= 0.80: for each '
                            'evaluation question, the top-scoring ordered pair of its 18-card bank (306 pairs) is '
                            '{own first, own second or changed} in >= 5 of 6 questions (CLASS C search).'),
        'D4_NATIVE_CONTROL': 'NOT_DEMONSTRATED by construction: a Python reader evaluates the signal and Python mounts.'},
    'decision': ('DEVAM if D1 PASS and D2R PASS. DUR if D2 FAIL and D2R FAIL. Otherwise YETERSİZ KANIT. A budget stop '
                 'forces YETERSİZ KANIT. D3/D4 are reported separately and never raise the decision.'),
    'rho_reference': 'rho on evaluation pair mounts (offline only), stump fitted on calibration rho, Spearman with signals.',
    'classes': {'hidden / CUT3 / attention / next-token law of one forward': 'A (native numbers)',
                'calibrated direction, stump, argmax over pairs': 'B (fixed numerical reader, Python)',
                'trying all pairs, mounting, choosing what to mount': 'C (external search / execution)'}}

CLAIMS838 = {
    'verified_from_prior_research': [
        '837.log (blob d64c63ee): ORACLE first-conditioned rho search 12/12 (both orders 6/6); MODEL anchor (single-card '
        'effect) chose the fork in 8/12 -> 4/12 end-to-end; fork anchor below true first 11/12; KV states TRUE/FORK/'
        'IRRELEVANT all 7/12 (no content selectivity); answers: [first, second] end 6/6, [fork, second] UNKNOWN 6/6, '
        '[first, mirror] UNKNOWN 3/6; bank answers OFF 1/6; decision YETERSİZ KANIT.',
        'rho is a class C counterfactual measurement (four physical mounts); it is not a single-forward native signal.'],
    'implemented_in_TEST838': [
        'Physical information-dependence panel with separate endpoint / UNKNOWN categories.',
        'Eight predeclared single-forward signals, calibrated on separate worlds, evaluated blind incl. unseen template.',
        'Single-card and pair-scan addressing analyses with explicit class labels and cost scaling.'],
    'demonstrated_by_TEST838': 'filled only from this run'}

BODY838 = r'''
D829['test'] = '838'
D829['controller'] = 'NONE; SIGNAL READER = PYTHON (CLASS B); PAIR SCAN = CLASS C EXTERNAL SEARCH'
D829['sources838'] = {'829': LOCK829_838, '834': LOCK834_838, '837': LOCK837_838, '837_log': LOCK837LOG_838,
                      'helpers_sha256': HELPER_SHA838, 'helpers': list(HELPERS838)}
D829['hypotheses838'] = PANEL829['test838']['hypotheses']
D829['limitations'] = [
    'Every candidate signal is read by a Python reader (calibrated direction + one-feature stump, class B). Even a '
    'perfect signal is not model-native control of the next computation (D4 = NOT_DEMONSTRATED).',
    'B2 tries every ordered pair in Python (class C). A successful scan is not model-native addressing.',
    'Eight calibration and six evaluation worlds, one model, one question template; 12 (world, order) cells per class '
    'are not 12 independent worlds.',
    'Answer-frame signals see the TEST827 boundary instruction that names UNKNOWN; they are reported as behavioural.',
    'Answer text is produced offline after all numeric work, with the TEST827 boundary instruction.',
    'No GPU execution or result is claimed by the code author.']
gate829('PANEL_FRESH_SEED', SEED829 == SEED838, SEED829)
gate829('NO_CONTROL_TEXT', MAX_NEW_CONTROL829 == 0)
gate829('WORLD_COUNT', len(questions829) == EVAL_WORLDS838 and len(CALW838) == CAL_WORLDS838 and
        len(QID838['EVAL']) == EVAL_WORLDS838 and len(QID838['CAL']) == CAL_WORLDS838)
gate829('JOBS_UNIQUE', len({(tuple(j['mount']), j['qid']) for j in JOBS838}) == len(JOBS838), len(JOBS838))
gate829('JOB_KEYS_PARTITION', set(CALKEY838) == {j['job'] for j in CALJOBS838} and
        not (set(CALKEY838) & {j['job'] for j in EVALJOBS838}) and len(CALJOBS838) + len(EVALJOBS838) == len(JOBS838))
gate829('SPLIT_CARDS_DISJOINT', all(c in set(CALSTORE838) | {NULL829} for j in CALJOBS838 for c in j['mount']) and
        all(c in set(EVALSTORE838) | {NULL829} for j in EVALJOBS838 for c in j['mount']) and
        all(c in set(EVALSTORE838) for b in BANKS838 for c in b))
gate829('CARTRIDGES_PHYSICAL', all(c in entries for j in JOBS838 for c in j['mount']) and
        all(c in entries for b in BANKS838 for c in b))
def copy_receivers838(src):
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'copy':
            r = n.func.value
            out.append(isinstance(r, ast.Call) and isinstance(r.func, ast.Attribute) and r.func.attr == 'numpy')
    return out
cr838 = copy_receivers838(HELPER_SRC838) + copy_receivers838(BODY838_TEXT)
gate829('STATIC_COPY_RECEIVERS_ARE_NDARRAY', all(cr838), {'copy_calls': len(cr838)})
# Static leak gate: before the OFFLINE marker the runtime never names the evaluation key or any labelled panel object.
MARK838 = '# ====== OFFLINE' + ' PHASE MARKER ======'
gate829('OFFLINE_MARKER_UNIQUE', BODY838_TEXT.count(MARK838) == 1)
pre838 = ast.parse(BODY838_TEXT.split(MARK838)[0])
used838 = {n.id for n in ast.walk(pre838) if isinstance(n, ast.Name)}
gate829('STATIC_NO_EVAL_LABELS_BEFORE_OFFLINE', not (used838 & {'EVALKEY838', 'worlds829', 'card_meta829', 'NAMES_E838'}),
        sorted(used838 & {'EVALKEY838', 'worlds829', 'card_meta829', 'NAMES_E838'}))
exec(compile(HELPER_SRC838, 'TEST838_LOCKED_HELPERS', 'exec'), globals())
gate829('HELPERS_LOADED', all(callable(globals().get(x)) for x in HELPERS838), HELPER_SHA838)
gate829('ENGINE_SYMBOLS838', all(callable(globals().get(x)) for x in
        ('cache_build', 'pairs', 'Cut3Diagnostic', 'prompt_ids', 'build_fusion', 'observe_state', 'kv_digest',
         'safe_load', 'cosdist829', 'full_readout829', 'free_generate', 'answer_prompt829')))
gate829('ARCH_DIMS', (NL, H, QH, KVH, HD) == EXPECTED_ARCH834 and int(model.config.num_attention_heads) == QH and
        int(model.config.num_key_value_heads) == KVH and int(model.config.hidden_size) == H, (NL, H, QH, KVH, HD))
gate829('BF16_COMPUTE', DTYPE == _torch829.bfloat16, str(DTYPE))
gate829('NF4_LINEAR4BIT', any(isinstance(m_, bitsandbytes.nn.Linear4bit) for m_ in model.modules()))
gate829('WEIGHTS_FROZEN', all(not p_.requires_grad for p_ in model.parameters()))
gate829('DEVICE', str(DEV).startswith(DEVICE_KIND838), str(DEV))
gate829('SDPA_MODULE', F is _torch829.nn.functional and F.scaled_dot_product_attention is SDPA829)
gate829('PREFIX_P', P == 30, P)
gate829('PRIOR_LOG_PRESENT', b'PHYSICAL_SUPERIOR' in raw837log_838 and b'TEST837' in raw837log_838)
POST838 = cost_upper838({c: int(entries[c]['body_tokens']) for c in cards829}, P)
D829['predicted_cost838'] = POST838
log829('TEST838_PREDICTED_COST', json.dumps(POST838))
gate829('PREDICTED_BUDGET_POST_LOAD', POST838['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN838,
        POST838['minutes_upper_excluding_model_load'])
QTEXT838 = {q['qid']: q['question'] for q in questions829}
QTEXT838.update({cw['qid']: cw['question'] for cw in CALW838})
FIDS838 = {}
for qid838, t838 in QTEXT838.items():
    FIDS838[(qid838, 'Q')] = list(prompt_ids(t838))                       # question-only frame
    FIDS838[(qid838, 'A')] = list(prompt_ids(answer_prompt829(t838)))     # TEST827 answer boundary frame (= free_generate)
gate829('FUSION_TOKENS_WITH_FRAME', POST838['max_memory_tokens'] + max(len(v) for v in FIDS838.values()) + 64 <= MAX_FUSED_TOKENS,
        POST838['max_memory_tokens'])
# UNKNOWN token ids (identical for every mount; no entity name is ever used at runtime)
UNK_IDS838 = sorted({int(tok.encode(x, add_special_tokens=False)[0]) for x in ('UNKNOWN', ' UNKNOWN')})
D829['unknown_tokens838'] = {'first_token_ids': UNK_IDS838, 'pieces': [tok.decode([u]) for u in UNK_IDS838],
                             'full_encodings': {x: [int(i) for i in tok.encode(x, add_special_tokens=False)]
                                                for x in ('UNKNOWN', ' UNKNOWN')}}
gate829('UNKNOWN_TOKENS', 1 <= len(UNK_IDS838) <= 2, D829['unknown_tokens838'])
gate829('LM_HEAD_ROWS_FOR_ORTH', W829 is not None and bool(FP64_MODE829), str(getattr(W829, 'dtype', None)))
WUNK838 = np.stack([W829[u].double().cpu().numpy() for u in UNK_IDS838]).astype(np.float64)
QUNK838 = np.linalg.qr(WUNK838.T)[0].T                                  # orthonormal basis of the UNKNOWN lm_head rows
gate829('UNKNOWN_BASIS', QUNK838.shape == (len(UNK_IDS838), H) and np.isfinite(QUNK838).all(), list(QUNK838.shape))
try:
    free838, _ = _torch829.cuda.mem_get_info()
    gate829('VRAM_HEADROOM', free838 / 2**30 >= 8.0, round(free838 / 2**30, 2))
except Exception as e838:
    gate829('VRAM_HEADROOM', False, repr(e838))
D829['noninterference838'] = noninterference829([NULL829], questions829[0]['question'])
for k838, v838 in D829['noninterference838'].items():
    gate829('NONINTERFERENCE_' + k838.upper(), bool(v838), v838)
COUNT834 = {'fusion_forwards': fusion_forwards829([NULL829]), 'probe_forwards': 3, 'capture_forwards': 0,
            'rank_forwards': 0, 'generation_forwards': 1, 'mounts': 1}
T0_838 = time.perf_counter()
SEAL_LAYERS834 = (0, CUT, NL // 2, NL - 1)

# ---- equivalence of the probe with the locked observe_state (question frame) ----
jE838 = next(j for j in CALJOBS838 if len(j['mount']) == 2)
memE838, nE838 = mount834(jE838['mount'], 'EQUIV')
b0E838 = int(entries[jE838['mount'][0]]['body_tokens'])
spE838 = {'B0': (P, P + b0E838), 'B1': (P + b0E838, nE838)}
with Readout829() as roE838:
    stE838, attE838 = observe_state(memE838, QTEXT838[jE838['qid']], spE838)
COUNT834['probe_forwards'] += 1
pE838 = rprobe834(memE838, None, FIDS838[(jE838['qid'], 'Q')])
hpm838 = max(abs(float(pE838['rows'][l][:, spE838[s][0]:spE838[s][1]].sum(-1).mean()) - float(attE838[str(l)][s + '_mass']))
             for l in (4, 20, 40, 79) for s in ('B0', 'B1'))
D829['probe_equivalence838'] = {
    'cut3_state_bitwise': bool(np.array_equal(stE838.float().cpu().numpy().astype(np.float64), pE838['state'])),
    'final_hidden_bitwise': bool(np.array_equal(roE838.h.reshape(-1).double().cpu().numpy(), pE838['h'])),
    'headprobe_mass_max_abs_vs_locked_probe': hpm838}
gate829('PROBE_EQUALS_OBSERVE_STATE_CUT3', D829['probe_equivalence838']['cut3_state_bitwise'])
gate829('PROBE_EQUALS_OBSERVE_STATE_HIDDEN', D829['probe_equivalence838']['final_hidden_bitwise'])
gate829('HEADPROBE_EQUALS_LOCKED_ATTENTION_PROBE', hpm838 <= 2e-6, hpm838)
del memE838, pE838, stE838; gc.collect(); release()

# ---- per-job vector store (SHA-256 manifest; job-level resume) ----
VDIR838 = DIR829 / 'TEST838_vectors'
VDIR838.mkdir(exist_ok=True)
MAN838 = DIR829 / 'TEST838_vector_manifest.jsonl'
HEADER838 = {'panel_sha256': PANEL_SHA829, 'body_sha256': PANEL829['test838']['body_sha256'], 'helpers_sha256': HELPER_SHA838}
VEC838 = {}
D829['resume838'] = {'enabled': RESUME838, 'source': None, 'reused_jobs': 0, 'reason': None}
if RESUME838:
    for cand in sorted(DIR829.parent.glob('TEST838_*/TEST838_vector_manifest.jsonl'), reverse=True):
        if cand.parent == DIR829:
            continue
        try:
            lines = cand.read_text(encoding='utf-8').splitlines()
            if not lines or json.loads(lines[0]).get('header') != HEADER838:
                D829['resume838']['reason'] = 'header mismatch in ' + str(cand); continue
            got = {}
            for ln in lines[1:]:
                o = json.loads(ln); f = cand.parent / 'TEST838_vectors' / o['file']
                if not f.exists() or sha_file(f) != o['sha256']:
                    continue
                got[o['key']] = load_npz837(f)
            VEC838.update(got)
            D829['resume838'].update({'source': str(cand), 'reused_jobs': len(got), 'reason': 'header and per-file SHA-256 verified'})
            break
        except Exception as e838r:
            D829['resume838']['reason'] = 'unreadable ' + str(cand) + ' ' + repr(e838r)
log829('TEST838_RESUME', json.dumps(D829['resume838']))
with MAN838.open('w', encoding='utf-8') as fh838:
    fh838.write(json.dumps({'header': HEADER838}, sort_keys=True) + '\n')
def save_vec838(key, arrays):
    f = VDIR838 / (key + '.npz')
    np.savez(f, **arrays)
    with MAN838.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps({'kind': 'job', 'key': key, 'file': f.name, 'sha256': sha_file(f)}, sort_keys=True) + '\n')
for k838 in list(VEC838):
    save_vec838(k838, VEC838[k838])

# ==================================================================================================================
# MEASUREMENT RUNTIME. Evaluation jobs are opaque IDs; only calibration labels (CALKEY838) are read before the offline
# phase, and only by the calibration fit.
# ==================================================================================================================
BUDGET_STOP838 = False
ALLJOBS838 = {j['job']: j for j in JOBS838}
KEY2JOB838 = {(tuple(j['mount']), j['qid']): j['job'] for j in JOBS838}
def scal838(lp, summ):
    lu = float(np.logaddexp.reduce(lp[UNK_IDS838]))
    rest = np.array(lp, dtype=np.float64)
    rest[UNK_IDS838] = -np.inf
    return np.asarray([lu, lu - float(rest.max()), float(summ['entropy_nats']), float(np.exp(lp.max())),
                       float(summ['argmax_bf16']), float(summ['argmax_fp64'])], dtype=np.float64)
def measure_jobs838(job_ids, tag, frames, store_lp):
    global BUDGET_STOP838
    groups, order = {}, []
    for jj in job_ids:
        m = tuple(ALLJOBS838[jj]['mount'])
        if m not in groups:
            groups[m] = []; order.append(m)
        groups[m].append(jj)
    ng = len(order); step = max(1, ng // 3)
    log829('TEST838_PROGRESS', tag, 0, '/', ng)
    for gi, m in enumerate(order):
        todo = [jj for jj in groups[m] if jj not in VEC838 or any(F_ + '_h' not in VEC838[jj] for F_ in frames)]
        if todo:
            if (time.perf_counter() - T0_838) / 60.0 > HARD_BUDGET_MIN838:
                BUDGET_STOP838 = True
                log829('TEST838_BUDGET_STOP', tag, 'mount_groups_done', gi, 'of', ng); return
            memx, n = mount834(list(m), tag + '_G%d' % gi)
            seal = seal834(memx); csp = cspans834(list(m))
            for jj in todo:
                arr = dict(VEC838.get(jj, {}))
                arr['n'] = np.asarray([n], dtype=np.float64)
                for F_ in frames:
                    if F_ + '_h' in arr:
                        continue
                    p = rprobe834(memx, None, FIDS838[(ALLJOBS838[jj]['qid'], F_)], keep_lp=True)
                    lp = p['lp'].detach().to(device='cpu', dtype=_torch829.float64).numpy()
                    arr[F_ + '_h'] = np.asarray(p['h'], dtype=np.float64)
                    arr[F_ + '_state'] = np.asarray(p['state'], dtype=np.float64)
                    arr[F_ + '_M'] = card_mass834(p['rows'], csp).astype(np.float32)
                    arr[F_ + '_scal'] = scal838(lp, p['summary'])
                    if store_lp:
                        arr[F_ + '_lp'] = np.asarray(lp, dtype=np.float32)
                    del p, lp
                VEC838[jj] = arr; save_vec838(jj, arr)
            gate829('MEAS_KV_SEAL_' + tag + '_G%d' % gi, seal834(memx) == seal)
            del memx; gc.collect(); release()
        if (gi + 1) % step == 0 or gi + 1 == ng:
            log829('TEST838_PROGRESS', tag, gi + 1, '/', ng)

# ---- signal computation from one stored forward (same code for calibration, evaluation and B2) ----
def unit838(v):
    v = np.asarray(v, dtype=np.float64)
    return v / max(float(np.linalg.norm(v)), 1e-300)
def feats838(arr, dirs):
    f = {}
    if 'Q_h' in arr:
        hq = unit838(arr['Q_h']); Mq = arr['Q_M'].astype(np.float64)
        f['Q_HIDDEN_PROJ'] = float(hq @ dirs['Q_h']); f['Q_HIDDEN_PROJ_ORTH_UNK'] = float(hq @ dirs['Q_h_orth'])
        f['Q_CUT3_PROJ'] = float(unit838(arr['Q_state']) @ dirs['Q_state'])
        tot = Mq.sum(-1)
        f['Q_ATTN_BALANCE'] = (float(np.mean(np.minimum(Mq[..., 0], Mq[..., 1]) / np.maximum(tot, 1e-12)))
                               if Mq.shape[-1] == 2 else float('nan'))
        f['Q_LOGP_UNKNOWN'] = float(arr['Q_scal'][0])
        f['CTRL_ATTN_CARD_MASS'] = float(tot.mean()); f['DESC_HIDDEN_NORM'] = float(np.linalg.norm(arr['Q_h']))
    if 'A_h' in arr:
        ha = unit838(arr['A_h'])
        f['A_HIDDEN_PROJ'] = float(ha @ dirs['A_h']); f['A_HIDDEN_PROJ_ORTH_UNK'] = float(ha @ dirs['A_h_orth'])
        f['A_LOGP_UNKNOWN'], f['A_UNK_GAP'], f['A_ENTROPY'], f['A_TOP1_PROB'] = (float(x) for x in arr['A_scal'][:4])
    f['CTRL_MOUNT_TOKENS'] = float(arr['n'][0])
    return f
def dirs838(pos, neg):
    d = {}
    for key, src in (('Q_h', 'Q_h'), ('Q_state', 'Q_state'), ('A_h', 'A_h')):
        mp = np.mean([unit838(a[src]) for a in pos], axis=0); mn = np.mean([unit838(a[src]) for a in neg], axis=0)
        d[key] = unit838(mp - mn)
    for key in ('Q_h', 'A_h'):
        v = d[key] - QUNK838.T @ (QUNK838 @ d[key])
        d[key + '_orth'] = unit838(v)
    return d
ALLSIG838 = tuple(SIGNALS838) + tuple(CONTROLS838) + tuple(DESCRIPTIVE838)
def fit838(items):
    pos = [a for a, y in items if y]; neg = [a for a, y in items if not y]
    dirs = dirs838(pos, neg)
    fs = [(feats838(a, dirs), y) for a, y in items]
    st = {s: stump_fit834([f[s] for f, y in fs if y], [f[s] for f, y in fs if not y]) for s in ALLSIG838}
    return {'dirs': dirs, 'stumps': st}
def sscore838(st, x):
    if st['threshold'] is None or not np.isfinite(x):
        return float('nan')
    return float(st['sign'] * (x - st['threshold']))
def balacc838(pred, lab):
    pred = [bool(p) for p in pred]; lab = [bool(y) for y in lab]
    tp = [p for p, y in zip(pred, lab) if y]; tn = [not p for p, y in zip(pred, lab) if not y]
    if not tp or not tn:
        return None
    return 0.5 * (float(np.mean(tp)) + float(np.mean(tn)))

t_meas838 = time.perf_counter()
measure_jobs838([j['job'] for j in CALJOBS838], 'CAL', FRAMES838, True)

# ---- CALIBRATION FIT (calibration worlds only; leave-one-world-out CV for selection and the B2 gate) ----
CALFIT838, B1FIT838, CV838 = None, None, {}
SELECTED838 = REP838 = None
B2RUN838 = []
if not BUDGET_STOP838:
    calp = [(j['job'], CALKEY838[j['job']]) for j in CALJOBS838 if '|' in CALKEY838[j['job']]['cond']]
    gate829('CALFIT_USES_CALIBRATION_ONLY', all(jj in CALKEY838 and ALLJOBS838[jj]['phase'] == 'CAL' for jj, _ in calp) and
            len(calp) == CAL_WORLDS838 * 12, len(calp))
    def lab838(r):
        return r['cond'].split('|')[0] in POSITIVE838
    cvp = {s: [] for s in ALLSIG838}; cvy = []; cvw = []
    for k in range(CAL_WORLDS838):
        tr = [(VEC838[jj], lab838(r)) for jj, r in calp if r['world'] != k]
        te = [(VEC838[jj], lab838(r)) for jj, r in calp if r['world'] == k]
        fk = fit838(tr)
        for a, y in te:
            fv = feats838(a, fk['dirs'])
            for s in ALLSIG838:
                cvp[s].append(sscore838(fk['stumps'][s], fv[s]) > 0)
            cvy.append(y); cvw.append(k)
    for s in ALLSIG838:
        per = [balacc838([p for p, w in zip(cvp[s], cvw) if w == k], [y for y, w in zip(cvy, cvw) if w == k])
               for k in range(CAL_WORLDS838)]
        CV838[s] = {'cv_balanced_acc': balacc838(cvp[s], cvy), 'per_world': per,
                    'worst_world': min(x for x in per if x is not None)}
    CALFIT838 = fit838([(VEC838[jj], lab838(r)) for jj, r in calp])
    for s in ALLSIG838:
        CV838[s]['in_sample_balanced_acc'] = CALFIT838['stumps'][s]['cal_balanced_acc']
    SELECTED838 = max(SIGNALS838, key=lambda s: (CV838[s]['cv_balanced_acc'] or 0.0, -SIGNALS838.index(s)))
    REP838 = max(REPRESENTATIONAL838, key=lambda s: (CV838[s]['cv_balanced_acc'] or 0.0, -SIGNALS838.index(s)))
    B2RUN838 = [s for s in dict.fromkeys([SELECTED838, REP838]) if (CV838[s]['cv_balanced_acc'] or 0.0) >= B2_GATE838]
    # B1: first vs fork from single-card calibration mounts (reported only)
    cals = [(j['job'], CALKEY838[j['job']]) for j in CALJOBS838 if CALKEY838[j['job']]['cond'] in ('FIRST_ONLY', 'FORK_ONLY')]
    B1FIT838 = fit838([(VEC838[jj], r['cond'] == 'FIRST_ONLY') for jj, r in cals])
    dsha = {k: sha829(np.ascontiguousarray(v).tobytes()) for k, v in CALFIT838['dirs'].items()}
    D829['calibration838'] = {'cv': CV838, 'selected': SELECTED838, 'representational_selected': REP838,
                              'b2_signals': B2RUN838, 'b2_gate': B2_GATE838, 'stumps': CALFIT838['stumps'],
                              'direction_sha256': dsha, 'b1_stumps': B1FIT838['stumps'],
                              'b1_direction_sha256': {k: sha829(np.ascontiguousarray(v).tobytes()) for k, v in B1FIT838['dirs'].items()},
                              'n_items': len(calp)}
    D829['calibration838_sha256'] = sha829(json.dumps(D829['calibration838'], sort_keys=True, default=str))
    np.savez(DIR829 / 'TEST838_calibration_directions.npz', **{'pair_' + k: v for k, v in CALFIT838['dirs'].items()},
             **{'b1_' + k: v for k, v in B1FIT838['dirs'].items()})
    save829()
    log829('TEST838_CALFIT', json.dumps({'selected': SELECTED838, 'selected_cv': CV838[SELECTED838]['cv_balanced_acc'],
                                         'rep': REP838, 'rep_cv': CV838[REP838]['cv_balanced_acc'], 'b2': B2RUN838,
                                         'cv': {s: CV838[s]['cv_balanced_acc'] for s in ALLSIG838},
                                         'sha256': D829['calibration838_sha256']}))
    gate829('CALIBRATION_SEALED_BEFORE_EVALUATION', D829['calibration838_sha256'] is not None, D829['calibration838_sha256'])

# ---- EVALUATION MEASUREMENT (sealed fit; nothing below changes CALFIT838) ----
if not BUDGET_STOP838:
    measure_jobs838([j['job'] for j in EVALJOBS838], 'EVAL', FRAMES838, True)

# ---- B2: ordered-pair scan of each 18-card evaluation bank (CLASS C), only if gated in on calibration ----
B2JOBS838 = []
if B2RUN838 and not BUDGET_STOP838:
    b2frames = tuple(sorted({FRAME_OF838[s] for s in B2RUN838}))
    for bi, bank in enumerate(BANKS838):
        for x in bank:
            for y in bank:
                if x == y:
                    continue
                for q in BANKQ838[bi]:
                    k = ((x, y), q)
                    if k not in KEY2JOB838:
                        jj = 'J838B_' + sha829(json.dumps([q, x, y]))[:12]
                        rec = {'job': jj, 'mount': [x, y], 'qid': q, 'phase': 'B2'}
                        ALLJOBS838[jj] = rec; KEY2JOB838[k] = jj
                    B2JOBS838.append({'bank': bi, 'mount': [x, y], 'qid': q, 'job': KEY2JOB838[k]})
    measure_jobs838([b['job'] for b in B2JOBS838], 'B2', b2frames, False)
D829['b2_jobs838'] = B2JOBS838
D829['measure_seconds838'] = round(time.perf_counter() - t_meas838, 3)
jR838 = CALJOBS838[0]
if jR838['job'] in VEC838:
    memR838, nR838 = mount834(jR838['mount'], 'REPLAY')
    pR838 = rprobe834(memR838, None, FIDS838[(jR838['qid'], 'Q')])
    D829['determinism838'] = {'hidden_bitwise': bool(np.array_equal(pR838['h'], VEC838[jR838['job']]['Q_h'])),
                              'cut3_bitwise': bool(np.array_equal(pR838['state'], VEC838[jR838['job']]['Q_state']))}
    gate829('DETERMINISM_REPLAY', D829['determinism838']['hidden_bitwise'] and D829['determinism838']['cut3_bitwise'],
            D829['determinism838'])
    del memR838, pR838; gc.collect(); release()
else:
    D829['determinism838'] = {'hidden_bitwise': None, 'cut3_bitwise': None}
D829['budget_stop838'] = BUDGET_STOP838

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
for cid838 in cards829:
    gate829('FINAL_SHA_' + cid838, sha_file(CART_DIR / entries[cid838]['file']) == entries[cid838]['sha256'])
COUNT_NUMERIC838 = dict(COUNT834)
gate829('COUNTED_WITHIN_UPPER_BOUND', all(COUNT_NUMERIC838[k] <= POST838['numeric_upper'][k] for k in POST838['numeric_upper']),
        {'counted': COUNT_NUMERIC838, 'upper': POST838['numeric_upper']})

# ====== OFFLINE PHASE MARKER ======
# OFFLINE PHASE: all numeric measurements are saved; evaluation roles are read only from here. Answer text only here.
log829('TEST838_OFFLINE_START')
TEXT838 = {}
if not BUDGET_STOP838:
    egroups = {}
    for j in EVALJOBS838:
        egroups.setdefault(tuple(j['mount']), []).append(j)
    for gi, (m, js) in enumerate(egroups.items()):
        memx, n = mount834(list(m), 'TXT_G%d' % gi)
        for j in js:
            o = free_generate(memx, answer_prompt829(QTEXT838[j['qid']]), seed=None, gain=0., max_new=MAX_NEW_TEXT838, spans=None)
            COUNT834['generation_forwards'] += int(o['generated_tokens'])
            TEXT838[j['job']] = {'raw': o['raw'].strip(), 'generated_tokens': int(o['generated_tokens'])}
        del memx; gc.collect(); release()
        if (gi + 1) % 42 == 0 or gi + 1 == len(egroups):
            log829('TEST838_PROGRESS', 'TEXT', gi + 1, '/', len(egroups))
W838 = {q: (worlds829[i], i) for i, q in enumerate(QID838['EVAL'])}
def ok838(k, n, need, full):
    return 'INCONCLUSIVE' if n < full else ('PASS' if k >= need else 'FAIL')
def frac838(xs):
    return [sum(1 for x in xs if x), len(xs)]
# ---- D1: physical information dependence (answer text, separate END / UNKNOWN categories) ----
def tcls838(t, w):
    u = (t or '').upper()
    names = [nm for nm, c in (('END', w['end']), ('MIDDLE', w['middle']), ('START', w['start']), ('ALT_END', w['changed_end']),
                              ('FORK_END', w['fork_end']), ('DECOY', w['decoy_end'])) if c in u]
    return names + (['UNKNOWN'] if 'UNKNOWN' in u else [])
def tcat838(cls):
    names = [x for x in cls if x != 'UNKNOWN']
    if not cls:
        return 'EMPTY_OR_OTHER'
    if cls == ['UNKNOWN']:
        return 'UNKNOWN'
    if 'UNKNOWN' in cls:
        return 'MIXED'
    if names == ['END']:
        return 'END'
    if names == ['ALT_END']:
        return 'ALT_END'
    return 'OTHER_NAME:' + '+'.join(names)
TXTEV838 = []
for j in EVALJOBS838:
    if j['job'] not in TEXT838:
        continue
    r = EVALKEY838[j['job']]; w, wi = W838[j['qid']]
    cls = tcls838(TEXT838[j['job']]['raw'], w)
    TXTEV838.append({'world': wi, 'cond': r['cond'], 'classes': cls, 'category': tcat838(cls),
                     'text': TEXT838[j['job']]['raw'], 'generated_tokens': TEXT838[j['job']]['generated_tokens']})
def tcount838(cond_prefix, cat):
    xs = [x for x in TXTEV838 if x['cond'].split('|')[0] == cond_prefix]
    return [sum(1 for x in xs if x['category'] == cat), len(xs)]
TXTTAB838 = {}
for x in TXTEV838:
    c = x['cond'].split('|')[0]
    TXTTAB838.setdefault(c, {}); TXTTAB838[c][x['category']] = TXTTAB838[c].get(x['category'], 0) + 1
d1 = {'TRUE_PAIR_END': tcount838('TRUE_PAIR', 'END'), 'FIRST_ONLY_UNKNOWN': tcount838('FIRST_ONLY', 'UNKNOWN'),
      'SECOND_ONLY_UNKNOWN': tcount838('SECOND_ONLY', 'UNKNOWN'), 'NULL_UNKNOWN': tcount838('NULL', 'UNKNOWN'),
      'SECOND_ONLY_END': tcount838('SECOND_ONLY', 'END'), 'ALT_PAIR_ALT_END': tcount838('ALT_PAIR', 'ALT_END'),
      'FORK_PLUS_SECOND_UNKNOWN': tcount838('FORK_PLUS_SECOND', 'UNKNOWN'),
      'FIRST_PLUS_MIRROR_UNKNOWN': tcount838('FIRST_PLUS_MIRROR', 'UNKNOWN'),
      'DECOY_PLUS_FIRST_UNKNOWN': tcount838('DECOY_PLUS_FIRST', 'UNKNOWN'),
      'IRRELEVANT_PAIR_UNKNOWN': tcount838('IRRELEVANT_PAIR', 'UNKNOWN')}
D1 = ('INCONCLUSIVE' if d1['TRUE_PAIR_END'][1] < 12 or min(d1[k][1] for k in ('FIRST_ONLY_UNKNOWN', 'SECOND_ONLY_UNKNOWN', 'NULL_UNKNOWN')) < 6
      else 'PASS' if (d1['TRUE_PAIR_END'][0] >= D1_PAIR838 and all(d1[k][0] >= D1_SINGLE838 for k in
                                                                 ('FIRST_ONLY_UNKNOWN', 'SECOND_ONLY_UNKNOWN', 'NULL_UNKNOWN')))
      else 'FAIL')
# ---- first-answer-token law (offline; endpoint tokens use labels and never enter a decision) ----
def ftok838(name):
    return sorted({int(tok.encode(x, add_special_tokens=False)[0]) for x in (name, ' ' + name)})
FT838 = []
for j in EVALJOBS838:
    a = VEC838.get(j['job'])
    if a is None or 'A_lp' not in a:
        continue
    r = EVALKEY838[j['job']]; w, wi = W838[j['qid']]
    lp = a['A_lp'].astype(np.float64)
    lu = float(np.logaddexp.reduce(lp[UNK_IDS838]))
    le = float(np.logaddexp.reduce(lp[ftok838(w['end'])])); lc = float(np.logaddexp.reduce(lp[ftok838(w['changed_end'])]))
    FT838.append({'world': wi, 'cond': r['cond'], 'logp_unknown': lu, 'logp_end_first_token': le, 'logp_alt_first_token': lc,
                  'end_minus_unknown': le - lu, 'argmax_is_unknown_token': int(a['A_scal'][4]) in UNK_IDS838,
                  'entropy': float(a['A_scal'][2])})
FTSUM838 = {}
for c in sorted({x['cond'].split('|')[0] for x in FT838}):
    xs = [x for x in FT838 if x['cond'].split('|')[0] == c]
    FTSUM838[c] = {'n': len(xs), 'mean_logp_unknown': float(np.mean([x['logp_unknown'] for x in xs])),
                   'mean_end_minus_unknown': float(np.mean([x['end_minus_unknown'] for x in xs])),
                   'argmax_unknown': frac838([x['argmax_is_unknown_token'] for x in xs]),
                   'mean_entropy': float(np.mean([x['entropy'] for x in xs]))}
TOKCTRL838 = {'unknown_tokens': D829['unknown_tokens838'],
              'entity_names_sharing_unknown_first_token': sum(1 for nm in NAMES_E838 if set(ftok838(nm)) & set(UNK_IDS838)),
              'mean_tokens_end_name': float(np.mean([len(tok.encode(w['end'], add_special_tokens=False)) for w in worlds829])),
              'tokens_unknown': len(tok.encode('UNKNOWN', add_special_tokens=False)),
              'mean_generated_tokens_by_category': {c: float(np.mean([x['generated_tokens'] for x in TXTEV838 if x['category'] == c]))
                                                    for c in sorted({x['category'] for x in TXTEV838})}}
# ---- D2: blind evaluation of the sealed single-forward readers ----
EVP838 = [(j['job'], EVALKEY838[j['job']]) for j in EVALJOBS838 if '|' in EVALKEY838[j['job']]['cond'] and j['job'] in VEC838]
def evrow838(jj, r):
    w, wi = W838[ALLJOBS838[jj]['qid']]
    c, order = r['cond'].split('|')
    return {'job': jj, 'world': wi, 'cond': c, 'order': order, 'label': c in POSITIVE838,
            'template': 'UNSEEN' if wi >= BLOCK838 else 'STANDARD'}
EVROWS838 = [evrow838(jj, r) for jj, r in EVP838]
SC838 = {}
if CALFIT838 is not None:
    for row in EVROWS838:
        fv = feats838(VEC838[row['job']], CALFIT838['dirs'])
        row['raw'] = fv
        row['score'] = {s: sscore838(CALFIT838['stumps'][s], fv[s]) for s in ALLSIG838}
rngp838 = np.random.default_rng(SEED838 + 77)
def perm_p838(pred, lab):
    pred = np.asarray(pred, bool); lab = np.asarray(lab, bool)
    obs = balacc838(pred, lab)
    if obs is None:
        return None
    cnt = 0
    for _ in range(NPERM838):
        y = rngp838.permutation(lab)
        tp = pred[y].mean(); tn = (~pred[~y]).mean()
        cnt += (0.5 * (tp + tn) >= obs - 1e-12)
    return (cnt + 1) / (NPERM838 + 1)
def eval_signal838(s):
    rows = [r for r in EVROWS838 if 'score' in r]
    if not rows:
        return {'n': 0}
    pr = [r['score'][s] > 0 for r in rows]; lb = [r['label'] for r in rows]
    out = {'n': len(rows), 'balanced_acc': balacc838(pr, lb)}
    out['fp_rate'] = {c: (float(np.mean([p for p, r in zip(pr, rows) if r['cond'] == c])) if any(r['cond'] == c for r in rows) else None)
                      for c in NEGATIVE838}
    out['tp_rate'] = {c: (float(np.mean([p for p, r in zip(pr, rows) if r['cond'] == c])) if any(r['cond'] == c for r in rows) else None)
                      for c in POSITIVE838}
    out['unseen_template'] = balacc838([p for p, r in zip(pr, rows) if r['template'] == 'UNSEEN'],
                                       [r['label'] for r in rows if r['template'] == 'UNSEEN'])
    out['standard_template'] = balacc838([p for p, r in zip(pr, rows) if r['template'] == 'STANDARD'],
                                         [r['label'] for r in rows if r['template'] == 'STANDARD'])
    out['order'] = {o: balacc838([p for p, r in zip(pr, rows) if r['order'] == o], [r['label'] for r in rows if r['order'] == o])
                    for o in ('FORWARD', 'REVERSE')}
    out['per_world'] = [balacc838([p for p, r in zip(pr, rows) if r['world'] == k], [r['label'] for r in rows if r['world'] == k])
                        for k in range(EVAL_WORLDS838)]
    sc = [r['score'][s] for r in rows]
    pos = [x for x, r in zip(sc, rows) if r['label'] and np.isfinite(x)]; neg = [x for x, r in zip(sc, rows) if not r['label'] and np.isfinite(x)]
    out['mean_margin_pos_minus_neg'] = (float(np.mean(pos) - np.mean(neg)) if pos and neg else None)
    sep = 0
    for k in range(EVAL_WORLDS838):
        pk = [x for x, r in zip(sc, rows) if r['world'] == k and r['label']]; nk = [x for x, r in zip(sc, rows) if r['world'] == k and not r['label']]
        sep += bool(pk and nk and min(pk) > max(nk))
    out['worlds_perfectly_separated'] = [sep, EVAL_WORLDS838]
    out['perm_p'] = perm_p838(pr, lb)
    return out
EV838 = {s: eval_signal838(s) for s in ALLSIG838} if CALFIT838 is not None else {}
CTRLBEST838 = max([EV838[c]['balanced_acc'] or 0.0 for c in CONTROLS838]) if EV838 else None
def d2crit838(s):
    if s is None or s not in EV838 or EV838[s].get('n', 0) < 72:
        return 'INCONCLUSIVE', {}
    e = EV838[s]
    parts = {'balanced_acc': (e['balanced_acc'] or 0) >= D2_BAL838,
             'fp_each_negative_class': all(v is not None and v <= D2_FP838 for v in e['fp_rate'].values()),
             'unseen_template': (e['unseen_template'] or 0) >= D2_SUB838,
             'each_order': all((v or 0) >= D2_SUB838 for v in e['order'].values()),
             'beats_confound_controls': (e['balanced_acc'] or 0) >= CTRLBEST838 + D2_CTRL_GAP838,
             'permutation': e['perm_p'] is not None and e['perm_p'] <= D2_P838}
    return ('PASS' if all(parts.values()) else 'FAIL'), parts
D2, D2PARTS838 = d2crit838(SELECTED838)
D2R, D2RPARTS838 = d2crit838(REP838)
# per-condition table on ALL evaluation mounts (pairs and single-card controls) for the selected readers
CONDTAB838 = {}
if CALFIT838 is not None:
    for j in EVALJOBS838:
        if j['job'] not in VEC838:
            continue
        r = EVALKEY838[j['job']]; c = r['cond'].split('|')[0]
        fv = feats838(VEC838[j['job']], CALFIT838['dirs'])
        for s in dict.fromkeys([SELECTED838, REP838]):
            x = sscore838(CALFIT838['stumps'][s], fv[s])
            CONDTAB838.setdefault(s, {}).setdefault(c, []).append(x)
    CONDTAB838 = {s: {c: {'n': len(v), 'positive_rate': float(np.mean([x > 0 for x in v])),
                          'mean_signed_score': (float(np.nanmean(v)) if np.isfinite(v).any() else None)}
                      for c, v in t.items()} for s, t in CONDTAB838.items()}
# ---- rho reference (CLASS C, four mounts; offline only) ----
def rho838(mount, q):
    ks = [KEY2JOB838.get(((NULL829,), q)), KEY2JOB838.get(((mount[0],), q)), KEY2JOB838.get(((mount[1],), q)),
          KEY2JOB838.get((tuple(mount), q))]
    if any(k is None or k not in VEC838 for k in ks):
        return None
    z0, za, zb, zab = (VEC838[k]['Q_h'] for k in ks)
    return float(np.linalg.norm(zab - za - zb + z0) / max(np.linalg.norm(zb - z0), 1e-300))
RHO838 = {}
calrho = [(rho838(ALLJOBS838[j['job']]['mount'], j['qid']), CALKEY838[j['job']]['cond'].split('|')[0] in POSITIVE838)
          for j in CALJOBS838 if '|' in CALKEY838[j['job']]['cond']]
calrho = [(x, y) for x, y in calrho if x is not None]
if calrho and EVROWS838:
    strho = stump_fit834([x for x, y in calrho if y], [x for x, y in calrho if not y])
    ev = [(rho838(ALLJOBS838[r['job']]['mount'], ALLJOBS838[r['job']]['qid']), r) for r in EVROWS838]
    ev = [(x, r) for x, r in ev if x is not None]
    RHO838 = {'stump': strho, 'n': len(ev),
              'balanced_acc': balacc838([sscore838(strho, x) > 0 for x, _ in ev], [r['label'] for _, r in ev]),
              'fp_rate': {c: float(np.mean([sscore838(strho, x) > 0 for x, r in ev if r['cond'] == c])) for c in NEGATIVE838},
              'unseen_template': balacc838([sscore838(strho, x) > 0 for x, r in ev if r['template'] == 'UNSEEN'],
                                           [r['label'] for x, r in ev if r['template'] == 'UNSEEN'])}
    def spear838(a, b):
        a = np.asarray(a, float); b = np.asarray(b, float); ok = np.isfinite(a) & np.isfinite(b)
        if ok.sum() < 3:
            return None
        ra = np.argsort(np.argsort(a[ok])); rb = np.argsort(np.argsort(b[ok]))
        return float(np.corrcoef(ra, rb)[0, 1])
    RHO838['spearman_with'] = {s: spear838([x for x, _ in ev], [r['raw'][s] for _, r in ev]) for s in
                               dict.fromkeys([SELECTED838, REP838]) if s is not None and all('raw' in r for _, r in ev)}
# ---- D3-B1: single-card addressing (first vs fork; top-1 of the first among 8 singles) ----
B1_838 = {}
SINGLES838 = ('FIRST_ONLY', 'SECOND_ONLY', 'FORK_ONLY', 'MIRROR_ONLY', 'DECOY_ONLY', 'CHANGED_ONLY', 'OTHER_FIRST_ONLY', 'OTHER_SECOND_ONLY')
if B1FIT838 is not None:
    per = {}
    for j in EVALJOBS838:
        r = EVALKEY838[j['job']]
        if r['cond'] in SINGLES838 and j['job'] in VEC838:
            per.setdefault(r['world'], {})[r['cond']] = feats838(VEC838[j['job']], B1FIT838['dirs'])
    for s in ALLSIG838:
        if s == 'Q_ATTN_BALANCE':
            continue
        st = B1FIT838['stumps'][s]
        fp = [(sscore838(st, per[k]['FIRST_ONLY'][s]), sscore838(st, per[k]['FORK_ONLY'][s])) for k in per
              if 'FIRST_ONLY' in per[k] and 'FORK_ONLY' in per[k]]
        top1 = [max(per[k], key=lambda c: (np.nan_to_num(sscore838(st, per[k][c][s]), nan=-np.inf), -SINGLES838.index(c))) == 'FIRST_ONLY'
                for k in per if len(per[k]) == len(SINGLES838)]
        B1_838[s] = {'first_vs_fork_balanced_acc': balacc838([a > 0 for a, b in fp] + [b > 0 for a, b in fp],
                                                             [True] * len(fp) + [False] * len(fp)),
                     'first_above_fork_worlds': frac838([a > b for a, b in fp]), 'first_top1_among_8_singles': frac838(top1),
                     'calibration_in_sample_acc': st['cal_balanced_acc']}
B1BEST838 = max(B1_838, key=lambda s: (B1_838[s]['first_vs_fork_balanced_acc'] or 0.0)) if B1_838 else None
# ---- D3-B2: ordered-pair scan results (CLASS C) ----
B2RES838 = {}
for s in B2RUN838:
    recs = []
    for bi, bank in enumerate(BANKS838):
        for q in BANKQ838[bi]:
            w, wi = W838[q]; own_first = w['ids']['first']; valid2 = {w['ids']['second'], w['ids']['changed']}
            sc = []
            for b in B2JOBS838:
                if b['bank'] == bi and b['qid'] == q and b['job'] in VEC838 and FRAME_OF838[s] + '_h' in VEC838[b['job']]:
                    fv = feats838(VEC838[b['job']], CALFIT838['dirs'])
                    sc.append((sscore838(CALFIT838['stumps'][s], fv[s]), fv[s], tuple(b['mount'])))
            if len(sc) < len(bank) * (len(bank) - 1):
                continue
            sc.sort(key=lambda t: (-np.nan_to_num(t[0], nan=-np.inf), t[2]))
            def isvalid(m):
                return own_first in m and bool(set(m) & valid2)
            def isother(m):
                return any(set(m) == {ow['ids']['first'], ow['ids'][k2]} for ow in worlds829 if ow is not w for k2 in ('second', 'changed'))
            vr = next((i + 1 for i, t in enumerate(sc) if isvalid(t[2])), None)
            top = sc[0][2]
            recs.append({'world': wi, 'top1_valid': isvalid(top), 'top1_contains_own_first': own_first in top,
                         'best_valid_rank': vr, 'top10_valid': sum(1 for t in sc[:10] if isvalid(t[2])),
                         'top10_other_world_complete_chain': sum(1 for t in sc[:10] if isother(t[2])),
                         'positive_predictions': sum(1 for t in sc if t[0] > 0), 'pairs': len(sc)})
    B2RES838[s] = {'cells': recs, 'top1_valid': frac838([r['top1_valid'] for r in recs]),
                   'top1_contains_own_first': frac838([r['top1_contains_own_first'] for r in recs]),
                   'median_best_valid_rank': (float(np.median([r['best_valid_rank'] for r in recs])) if recs else None),
                   'status': ok838(sum(1 for r in recs if r['top1_valid']), len(recs), B2_NEED838, EVAL_WORLDS838)}
def b2status838(s):
    if s is None:
        return 'NOT_RUN'
    if s not in B2RUN838:
        return 'NOT_RUN_GATE'
    return B2RES838.get(s, {}).get('status', 'INCONCLUSIVE')
B2SEL838, B2REP838 = b2status838(SELECTED838), b2status838(REP838)
# ---- decision ----
if BUDGET_STOP838:
    decision838 = 'YETERSİZ KANIT'
elif D1 == 'PASS' and D2R == 'PASS':
    decision838 = 'DEVAM'
elif D2 == 'FAIL' and D2R == 'FAIL':
    decision838 = 'DUR'
else:
    decision838 = 'YETERSİZ KANIT'
SELGROUP838 = GROUP838.get(SELECTED838)
Q2_838 = ('YES_REPRESENTATIONAL' if D2R == 'PASS' else
          ('ONLY_' + str(SELGROUP838) if D2 == 'PASS' else ('INCONCLUSIVE' if 'INCONCLUSIVE' in (D2, D2R) else 'NO')))
Q3_838 = ('YES_CLASS_C_PAIR_SCAN' if 'PASS' in (B2SEL838, B2REP838) else
          ('NOT_RUN_GATE' if not B2RUN838 else 'NO'))
CRIT838 = {'D1_PHYSICAL_DEPENDENCE': D1, 'D2_SINGLE_FORWARD_SIGNAL': D2, 'D2R_REPRESENTATIONAL': D2R,
           'D3_B1_SINGLE_CARD_ADDRESSING': 'REPORTED_ONLY', 'D3_B2_PAIR_SCAN_SELECTED': B2SEL838,
           'D3_B2_PAIR_SCAN_REPRESENTATIONAL': B2REP838, 'D4_NATIVE_CONTROL': 'NOT_DEMONSTRATED'}
FINALQ838 = {'1_physical_pair_dependence': D1, '2_generalisable_single_forward_relational_signal': Q2_838,
             '3_first_memory_addressing_without_known_first': Q3_838 + ' (single-card B1 reported separately)',
             '4_model_native_control_without_python_search': 'NOT_DEMONSTRATED'}
REPORT838 = {
    'P1_physical_dependence': {'criteria_counts': d1, 'category_table': TXTTAB838, 'first_token_law': FTSUM838,
                               'token_controls': TOKCTRL838},
    'P2_single_forward': {'selected': SELECTED838, 'selected_group': SELGROUP838, 'representational_selected': REP838,
                          'calibration_cv': {s: CV838.get(s, {}).get('cv_balanced_acc') for s in ALLSIG838},
                          'calibration_worst_world': {s: CV838.get(s, {}).get('worst_world') for s in ALLSIG838},
                          'evaluation': EV838, 'best_control_balanced_acc': CTRLBEST838,
                          'd2_parts': D2PARTS838, 'd2r_parts': D2RPARTS838, 'condition_table': CONDTAB838,
                          'rho_reference_class_C': RHO838},
    'P3_addressing': {'A_pair_validity_single_forward': {'selected': D2, 'representational': D2R},
                      'B1_single_card': B1_838, 'B1_best_signal': B1BEST838,
                      'B2_pair_scan_class_C': {s: {k: v for k, v in r.items() if k != 'cells'} for s, r in B2RES838.items()},
                      'B2_signals_gated_in': B2RUN838, 'B2_gate': B2_GATE838,
                      'scaling': POST838['scaling']},
    'final_questions': FINALQ838, 'classes': HYP838['classes'],
    'resume': D829['resume838'], 'determinism': D829['determinism838']}
D829['cells838'] = {'text': TXTEV838, 'first_token': FT838, 'eval_rows': [{k: v for k, v in r.items()} for r in EVROWS838],
                    'b2': {s: r['cells'] for s, r in B2RES838.items()}}
D829['report838'] = REPORT838
D829['verdict838'] = {'decision': decision838, 'criteria': CRIT838, 'budget_stop': BUDGET_STOP838,
                      'interpretation_guard': ('Single-forward signals are read by a calibrated Python reader (class B); '
                                               'B2 is a class C external search; D4 is never inferred from D1/D2/D3.')}
D829['claims_ledger838'] = dict(CLAIMS838, demonstrated_by_TEST838={'decision': decision838, 'criteria': CRIT838,
                                                                     'final_questions': FINALQ838})
D829['cost838'] = {'counted': dict(COUNT834), 'predicted_upper': POST838, 'measure_seconds': D829['measure_seconds838'],
                   'total_seconds_body': round(time.perf_counter() - T0_838, 3), 'b2_jobs': len(B2JOBS838),
                   'peak_gpu_gib': float(_torch829.cuda.max_memory_allocated()) / 2**30}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f838:
    wr838 = csv.DictWriter(f838, fieldnames=['part', 'world', 'condition', 'order', 'label', 'signal', 'value', 'detail'])
    wr838.writeheader()
    for x in TXTEV838:
        wr838.writerow({'part': 'P1_TEXT', 'world': x['world'], 'condition': x['cond'], 'order': '', 'label': x['category'],
                        'signal': 'answer_text', 'value': x['text'], 'detail': json.dumps(x['classes'])})
    for r in EVROWS838:
        for s in ALLSIG838:
            if 'raw' in r:
                wr838.writerow({'part': 'P2_EVAL', 'world': r['world'], 'condition': r['cond'], 'order': r['order'],
                                'label': r['label'], 'signal': s, 'value': r['raw'][s], 'detail': r['score'][s]})
    for s, rr in B2RES838.items():
        for x in rr['cells']:
            wr838.writerow({'part': 'B2', 'world': x['world'], 'condition': '', 'order': '', 'label': x['top1_valid'],
                            'signal': s, 'value': x['best_valid_rank'], 'detail': json.dumps(x)})
D829['status'] = 'COMPLETE_TEST838_EVALUATED' if not BUDGET_STOP838 else 'STOPPED_BUDGET_PARTIAL_EVALUATED'
save829()
log829('TEST838_REPORT', json.dumps(REPORT838, default=str))
log829('TEST838_VERDICT', json.dumps(D829['verdict838'], default=str))
log829('TEST838_COMPLETED', str(OUT829))
'''
BODY_SHA838 = hashlib.sha256(BODY838.encode()).hexdigest()
PANEL_HOOK838 = ("PANEL829['test838'] = {'jobs': JOBS838, 'banks': BANKS838, 'bank_questions': BANKQ838, "
                 "'calibration_questions': [{'qid': cw['qid'], 'question': cw['question']} for cw in CALW838], "
                 "'calibration_labels': CALKEY838, 'signals': GROUP838, 'controls': CONTROLS838, 'descriptive': DESCRIPTIVE838, "
                 "'thresholds': {'D2_BAL': D2_BAL838, 'D2_FP': D2_FP838, 'D2_SUB': D2_SUB838, 'D2_CTRL_GAP': D2_CTRL_GAP838, "
                 "'D2_P': D2_P838, 'D1_PAIR': D1_PAIR838, 'D1_SINGLE': D1_SINGLE838, 'B2_NEED': B2_NEED838, 'B2_GATE': B2_GATE838, "
                 "'NPERM': NPERM838}, "
                 "'hypotheses': %r, 'body_sha256': %r, 'helpers_sha256': %r, 'seed': SEED829}\n"
                 % (HYP838, BODY_SHA838, HELPER_SHA838))
src838 = patch838(src838, "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))",
                  PANEL_HOOK838 + "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))")
OFFLINE_HOOK838 = r'''
OFFLINE838 = DIR829 / 'TEST838_offline_key.json'   # never read by any runtime computation
OFFLINE838.write_text(json.dumps({'note': 'OFFLINE ONLY', 'evaluation_jobs': EVALKEY838, 'calibration_jobs': CALKEY838,
                                  'worlds': worlds829, 'calibration_worlds': CALW838, 'questions': questions829,
                                  'card_meta': card_meta829}, ensure_ascii=False, indent=2), encoding='utf-8')
D829['offline_key838_sha256'] = sha829(OFFLINE838.read_bytes())
'''
src838 = patch838(src838, "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n",
                  "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n" + OFFLINE_HOOK838)
start838 = src838.index("    # RUN ORDER: integrity checks")
start838 = src838.rfind("    # ---", 0, start838)
end838 = src838.index("except BaseException as e:\n    D829['status'] = 'ERROR'", start838)
BODY838_TEXT = BODY838
replacement838 = "\n".join("    " + line if line else "" for line in BODY838.strip("\n").splitlines()) + "\n"
patched838 = src838[:start838] + replacement838 + src838[end838:]
ast.parse(patched838)
# ==================================================================================================================
# CONSOLE / LOGGING LAYER (TEST835 pattern). Nothing below changes what is computed. Every byte the engine prints is
# written unchanged to a full transcript file; the screen shows a compact digest, progress, failures and the summary.
# ==================================================================================================================
import os as _os838, sys as _sys838, io as _io838, traceback as _tb838, datetime as _dt838, shutil as _sh838
from pathlib import Path as _P838
_os838.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')     # download bars only (not data)
for _m838, _f838 in (('huggingface_hub', lambda m: m.utils.disable_progress_bars()),
                     ('transformers', lambda m: m.utils.logging.disable_progress_bar())):
    if _m838 in _sys838.modules:                                    # only if already imported: no new import
        try:
            _f838(_sys838.modules[_m838])
        except Exception:
            pass
_ROOT838 = _P838('/content') if _P838('/content').exists() else _P838('/tmp')
FULL_CONSOLE838 = _ROOT838 / ('TEST838_full_console_' + _dt838.datetime.now(_dt838.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.txt')
CON838 = {'phase': 'SOURCE_VERIFICATION', 'last': [], 'fail_lines': [], 't0': time.time(), 'measure': '0/0', 'p3': 0}
_ORIG_OUT838, _ORIG_ERR838 = _sys838.stdout, _sys838.stderr

def say838(*a):
    _ORIG_OUT838.write(' '.join(str(x) for x in a) + '\n'); _ORIG_OUT838.flush()

def _mins838():
    return round((time.time() - CON838['t0']) / 60.0, 1)

def route838(line):
    s = line.strip()
    if not s:
        return
    CON838['last'] = (CON838['last'] + [s[:300]])[-6:]
    if s.startswith('FAIL '):
        CON838['fail_lines'].append(s[:600]); say838('!! ' + s[:600]); return
    if s.startswith('TEST829_FAILED'):
        CON838['fail_lines'].append(s[:300]); return
    if s.startswith('TEST829_START'):
        parts = s.split()
        say838('Çalışma: %s | panel SHA-256: %s' % (parts[1] if len(parts) > 1 else '?', parts[-1]))
        CON838['phase'] = 'ENGINE_PRELUDE_AND_LOCKS'; return
    if s.startswith('TEST815_GPU_PREFLIGHT'):
        say838('GPU: ' + s[len('TEST815_GPU_PREFLIGHT'):].strip()); return
    if s.startswith('TEST815_GPU_FREE_GIB'):
        say838('GPU boş VRAM (yükleme öncesi): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('TEST838_PREDICTED_COST_BEFORE_MODEL_LOAD'):
        try:
            c = json.loads(s.split(' ', 1)[1]); u = c['numeric_upper']
            say838('Maliyet üst sınırı (model yükleme hariç, %%25 pay dahil): %s dk | iş %s (kalibrasyon %s, değerlendirme %s), mount %s | '
                   'B2 en kötü durum %s çift mount | kartuş %s | fusion<=%s probe<=%s' % (c['minutes_upper_excluding_model_load'], c['jobs'],
                   c['cal_jobs'], c['eval_jobs'], c['mounts'], c['b2_pair_mounts'], c['physical_cartridges'], u['fusion_forwards'],
                   u['probe_forwards']))
        except Exception:
            say838(s[:300])
        CON838['phase'] = 'MODEL_LOAD'; say838('Model yükleniyor (Qwen2.5-72B-Instruct, NF4, tek yükleme)...'); return
    if s.startswith('PASS FROZEN_PREFIX'):
        D_ = globals().get('D829', {})
        say838('Model yüklendi (%s s). Fiziksel kartuşlar üretiliyor ve SHA doğrulanıyor...' % D_.get('model_load_seconds', '?'))
        CON838['phase'] = 'PHYSICAL_CARTRIDGE_FORGING'; return
    if s.startswith('PASS PHYSICAL_COUNT'):
        say838('Fiziksel kartuşlar: ' + s.split()[-1] + ' (her biri SHA-256 + tensör SHA ile yeniden yüklendi)')
        CON838['phase'] = 'PREFLIGHT_GATES'; return
    if s.startswith('PASS ARCH_DIMS'):
        say838('Mimari (NL,H,QH,KVH,HD): ' + s[len('PASS ARCH_DIMS'):].strip() + ' | BF16 hesap, NF4, ağırlıklar donmuş'); return
    if s.startswith('PASS VRAM_HEADROOM'):
        say838('Boş VRAM (model sonrası): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('PASS HEADPROBE_EQUALS_LOCKED_ATTENTION_PROBE'):
        say838('Eşdeğerlik kapıları geçti (CUT3/hidden bitwise, HeadProbe farkı ' + s.split()[-1] + ')'); return
    if s.startswith('PASS UNKNOWN_TOKENS'):
        say838('UNKNOWN ilk-token kimlikleri (tüm mount\'larda aynı): ' + s[len('PASS UNKNOWN_TOKENS'):].strip()[:200]); return
    if s.startswith('PASS STATIC_NO_EVAL_LABELS_BEFORE_OFFLINE'):
        say838('Sızıntı kapısı: çevrimdışı işaretinden önce değerlendirme etiketi kullanılmıyor (AST)'); return
    if s.startswith('TEST838_CALFIT'):
        try:
            r = json.loads(s.split(' ', 1)[1])
            say838('Kalibrasyon mühürlendi (LOWO-CV): seçilen %s CV=%.3f | temsil %s CV=%.3f | B2 çalışacak: %s | SHA %s'
                   % (r['selected'], r['selected_cv'] or 0, r['rep'], r['rep_cv'] or 0, r['b2'] or 'HAYIR (kapı)', r['sha256'][:16]))
        except Exception:
            say838(s[:300])
        CON838['phase'] = 'MEASUREMENT EVAL'; return
    if s.startswith('TEST838_RESUME '):
        try:
            r = json.loads(s.split(' ', 1)[1])
            say838('Devam mekanizması: yeniden kullanılan iş %s | %s' % (r.get('reused_jobs'), r.get('reason')))
            CON838['phase'] = 'MEASUREMENT CAL'
        except Exception:
            say838(s[:300])
        return
    if s.startswith('TEST838_PROGRESS'):
        p = s.split()
        if len(p) >= 5:
            CON838['phase'] = 'MEASUREMENT %s (%s/%s)' % (p[1], p[2], p[4])
            if p[2] != '0':
                say838('  %-11s %s/%s (%s dk)' % (p[1], p[2], p[4], _mins838()))
        return
    if s.startswith('TEST838_BUDGET_STOP'):
        say838('!! ' + s); return
    if s.startswith('TEST838_OFFLINE_START'):
        CON838['phase'] = 'OFFLINE_EVALUATION'
        say838('Ölçüm bitti; çevrimdışı değerlendirme (%s dk)' % _mins838()); return
    if s.startswith('TEST838_COMPLETED'):
        CON838['phase'] = 'COMPLETED'; return

class Console838(_io838.TextIOBase):
    """Writes everything to FULL_CONSOLE838 unchanged; routes complete lines to the compact screen digest."""
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
        if self.fh.closed:
            return self.orig.write(x)
        self.fh.write(x)
        self.buf += x
        while '\n' in self.buf:
            line, self.buf = self.buf.split('\n', 1)
            try:
                route838(line.split('\r')[-1])
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

def sha_path838(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()

def fmt838(x):
    if isinstance(x, list) and len(x) == 2 and all(isinstance(v, (int, float)) for v in x):
        return '%s/%s' % (x[0], x[1])
    if isinstance(x, dict):
        return ', '.join('%s=%s' % (k, fmt838(v)) for k, v in x.items())
    if isinstance(x, float):
        return '%.4g' % x
    if isinstance(x, list):
        return '[' + ', '.join(fmt838(v) for v in x) + ']'
    return str(x)

def files_report838():
    say838('=' * 78); say838('SONUÇ DOSYALARI (SHA-256)')
    d = globals().get('DIR829')
    if d is None or not _P838(d).exists():
        say838('  (çalışma klasörü yok)'); return
    for p in sorted(_P838(d).iterdir()):
        if p.is_file():
            say838('  %s  %d B  %s' % (p, p.stat().st_size, sha_path838(p)))
    vd = _P838(d) / 'TEST838_vectors'
    if vd.exists():
        fs = sorted(x for x in vd.iterdir() if x.is_file())
        say838('  %s/  %d vektör dosyası, %.1f MB (her dosyanın SHA-256 değeri TEST838_vector_manifest.jsonl içinde)'
               % (vd, len(fs), sum(x.stat().st_size for x in fs) / 2**20))

def final838(D):
    R = D['report838']; V = D['verdict838']; K = V['criteria']; C = D['cost838']
    checks = D.get('checks', [])
    p1 = R['P1_physical_dependence']; p2 = R['P2_single_forward']; p3 = R['P3_addressing']; FQ = R['final_questions']
    say838('=' * 78); say838('TEST838 SONUÇ ÖZETİ (sinyal okuyucu B sınıfı Python; B2 çift taraması C sınıfı dış arama)'); say838('=' * 78)
    say838('Durum: %s | bütçe durdurması: %s | devam: yeniden kullanılan iş %s' % (D.get('status'), V['budget_stop'],
           R['resume'].get('reused_jobs')))
    say838('Bütünlük: %d kapı, %d başarısız | eşdeğerlik: %s | determinizm: %s' % (len(checks), sum(not c['pass'] for c in checks),
           fmt838(D.get('probe_equivalence838', {})), fmt838(R.get('determinism', {}))))
    say838('-' * 78); say838('[P1] FİZİKSEL ÇİFTİN BİLGİ BAĞIMLILIĞI (kör değerlendirme, cevap metni; uç nokta ve UNKNOWN ayrı kategoriler)')
    c = p1['criteria_counts']
    say838('  TRUE_PAIR uç nokta %s | FIRST_ONLY UNKNOWN %s | SECOND_ONLY UNKNOWN %s (SECOND_ONLY uç nokta %s) | NULL UNKNOWN %s'
           % (fmt838(c['TRUE_PAIR_END']), fmt838(c['FIRST_ONLY_UNKNOWN']), fmt838(c['SECOND_ONLY_UNKNOWN']),
              fmt838(c['SECOND_ONLY_END']), fmt838(c['NULL_UNKNOWN'])))
    say838('  Doğru UNKNOWN (olumlu kontrol): FORK+SECOND %s | FIRST+MIRROR %s | DECOY+FIRST %s | IRRELEVANT %s | ALT_PAIR alternatif uç %s'
           % (fmt838(c['FORK_PLUS_SECOND_UNKNOWN']), fmt838(c['FIRST_PLUS_MIRROR_UNKNOWN']), fmt838(c['DECOY_PLUS_FIRST_UNKNOWN']),
              fmt838(c['IRRELEVANT_PAIR_UNKNOWN']), fmt838(c['ALT_PAIR_ALT_END'])))
    say838('  İlk cevap tokeni (çevrimdışı; ort. log P(uç) - log P(UNKNOWN), argmax=UNKNOWN):')
    for k in ('NULL', 'FIRST_ONLY', 'SECOND_ONLY', 'TRUE_PAIR', 'ALT_PAIR', 'FORK_PLUS_SECOND', 'FIRST_PLUS_MIRROR',
              'DECOY_PLUS_FIRST', 'IRRELEVANT_PAIR'):
        x = p1['first_token_law'].get(k)
        if x:
            say838('    %-18s fark %+.2f | argmax UNKNOWN %s | entropi %.2f' % (k, x['mean_end_minus_unknown'],
                                                                         fmt838(x['argmax_unknown']), x['mean_entropy']))
    t = p1['token_controls']
    say838('  Token kontrolü: UNKNOWN ilk tokenini paylaşan varlık adı %s | UNKNOWN %s token, uç adı ort. %.1f token'
           % (t['entity_names_sharing_unknown_first_token'], t['tokens_unknown'], t['mean_tokens_end_name']))
    say838('[P2] TEK FORWARD SİNYALLERİ (kalibrasyonda LOWO-CV ile seçildi, değerlendirmede değiştirilmedi; 72 çift mount)')
    say838('  %-24s %-16s %6s | %6s %6s %6s | %s' % ('sinyal', 'grup', 'CV', 'kör', 'yeni-ş', 'p', 'yanlış pozitif (FORK/MIRROR/DECOY/IRR)'))
    ev = p2['evaluation']
    for s in list(D['report838']['P2_single_forward']['calibration_cv']):
        e = ev.get(s, {}); cv = p2['calibration_cv'].get(s)
        if not e or not e.get('n'):
            continue
        fp = e['fp_rate']
        mark = ' <SEÇİLEN' if s == p2['selected'] else (' <TEMSİL' if s == p2['representational_selected'] else '')
        say838('  %-24s %-16s %6s | %6s %6s %6s | %s/%s/%s/%s%s' % (s, GROUP838.get(s, 'CONTROL' if s in CONTROLS838 else 'DESCRIPTIVE'),
               fmt838(cv), fmt838(e['balanced_acc']), fmt838(e['unseen_template']), fmt838(e['perm_p']),
               fmt838(fp['FORK_PLUS_SECOND']), fmt838(fp['FIRST_PLUS_MIRROR']), fmt838(fp['DECOY_PLUS_FIRST']),
               fmt838(fp['IRRELEVANT_PAIR']), mark))
    for tag, s in (('seçilen', p2['selected']), ('temsil', p2['representational_selected'])):
        e = ev.get(s, {})
        if e.get('n'):
            say838('  %s %s: sıralar %s | marj %s | dünya içi tam ayrım %s | dünya başına %s' % (tag, s, fmt838(e['order']),
                   fmt838(e['mean_margin_pos_minus_neg']), fmt838(e['worlds_perfectly_separated']), fmt838(e['per_world'])))
    say838('  En iyi karıştırıcı kontrol (dikkat kütlesi / token sayısı): %s | D2 parçaları %s | D2R parçaları %s'
           % (fmt838(p2['best_control_balanced_acc']), fmt838(p2['d2_parts']), fmt838(p2['d2r_parts'])))
    for s, tab in p2['condition_table'].items():
        say838('  %s pozitif oranı (tek kart dahil): %s' % (s, ', '.join('%s=%s' % (k, fmt838(v['positive_rate'])) for k, v in tab.items())))
    rr = p2['rho_reference_class_C']
    if rr:
        say838('  rho referansı (4 mount, C sınıfı): kör %s | yeni-ş %s | Spearman %s' % (fmt838(rr.get('balanced_acc')),
               fmt838(rr.get('unseen_template')), fmt838(rr.get('spearman_with', {}))))
    say838('[P3] İLK ANININ ADRESLENMESİ — A ve B ayrı sayılır')
    say838('  A (çift takılıyken tek forward geçerlilik): seçilen %s | temsil %s' % (p3['A_pair_validity_single_forward']['selected'],
           p3['A_pair_validity_single_forward']['representational']))
    b1 = p3['B1_single_card']; bb = p3['B1_best_signal']
    if bb:
        x = b1[bb]
        say838('  B1 (tek kart, ilk vs fork; simetri nedeniyle şans bekleniyor): en iyi %s kör %s | ilk>fork %s | 8 tek kart içinde ilk top-1 %s'
               % (bb, fmt838(x['first_vs_fork_balanced_acc']), fmt838(x['first_above_fork_worlds']), fmt838(x['first_top1_among_8_singles'])))
    if p3['B2_pair_scan_class_C']:
        for s, r in p3['B2_pair_scan_class_C'].items():
            say838('  B2 (C sınıfı, 306 sıralı çift/soru) %s: top-1 geçerli %s | top-1 kendi ilk kartı içeriyor %s | en iyi geçerli sıra medyanı %s | %s'
                   % (s, fmt838(r['top1_valid']), fmt838(r['top1_contains_own_first']), fmt838(r['median_best_valid_rank']), r['status']))
    else:
        say838('  B2 çalıştırılmadı: hiçbir seçilen sinyal kalibrasyon kapısını (CV >= %s) geçmedi' % p3['B2_gate'])
    sc = p3['scaling']
    say838('  Ölçek (ilk kart bilinmeden sıralı çift taraması, ~1.9 s/çift): ' + ' | '.join(
        'N=%s: %s çift ~%s' % (n, v['pair_mounts'], ('%.1f saat' % (v['seconds_at_1p9s'] / 3600.0)) if v['years_at_1p9s'] < 1
                               else ('%.0f yıl' % v['years_at_1p9s'])) for n, v in sc.items()))
    say838('-' * 78); say838('ÖLÇÜTLER')
    for k in K:
        say838('  %-34s %s' % (k, K[k]))
    say838('NİHAİ AYRIM:')
    for k, v in FQ.items():
        say838('  %-52s %s' % (k, v))
    say838('=' * 78)
    say838('NİHAİ BİLİMSEL KARAR: %s' % V['decision'])
    if V['decision'] == 'DEVAM':
        say838('  Gerekçe: D1 PASS ve D2R PASS — fiziksel çift bağımlılığı ve görülmemiş dünyalara genellenen tek-forward temsil sinyali. '
               'Okuyucu Python (B), B2 C sınıfı; model-native kontrol (madde 4) gösterilmedi.')
    elif V['decision'] == 'DUR':
        say838('  Gerekçe: D2 FAIL ve D2R FAIL — önceden sabit ölçütleri geçen tek-forward sinyal bulunamadı.')
    else:
        say838('  Gerekçe: ' + ('bütçe durdurması' if V['budget_stop'] else
                               'ölçütler ne DEVAM ne DUR kuralını sağladı (bkz. D1 / D2 / D2R satırları)'))
    say838('Maliyet: sayılan %s | ölçüm %s s | toplam gövde %s s | B2 işi %s | tepe VRAM %.2f GiB'
           % (fmt838(C['counted']), C['measure_seconds'], C['total_seconds_body'], C['b2_jobs'], C['peak_gpu_gib']))

say838('=' * 78)
say838('AKBASCORE TEST838 — tek native forward ilişkisel sinyal testi; Qwen2.5-72B-Instruct (NF4, donmuş), tek A100-80GB')
say838('Kaynak kilitleri: 829.py %s | 834.py %s | 837.py %s | 837.log %s' % (LOCK829_838, LOCK834_838, LOCK837_838, LOCK837LOG_838))
say838('Kilitli yardımcılar (AST, %d fonksiyon) SHA-256 %s' % (len(HELPERS838), HELPER_SHA838))
say838('BODY838 SHA-256 %s | yamalı kaynak AST geçti (%d bayt, SHA-256 %s)' % (BODY_SHA838, len(patched838), hashlib.sha256(patched838.encode()).hexdigest()))
say838('Kapsam: kalibrasyon %d dünya / kör değerlendirme %d dünya (%d görülmemiş şablon) | %d aday sinyal + %d karıştırıcı kontrol + 1 betimsel | '
       'B2 çift taraması kalibrasyon kapısına bağlı' % (CAL_WORLDS838, EVAL_WORLDS838, EVAL_WORLDS838 - BLOCK838, len(SIGNALS838), len(CONTROLS838)))
say838('Tam konsol kaydı: ' + str(FULL_CONSOLE838))
say838('=' * 78)
_fh838 = open(FULL_CONSOLE838, 'a', encoding='utf-8', buffering=1)
_fh838.write('TEST838_SOURCE_LOCKS ' + ' '.join((LOCK829_838, LOCK834_838, LOCK837_838, LOCK837LOG_838)) +
             '\nTEST838_BODY_SHA256 ' + BODY_SHA838 + '\nTEST838_HELPERS ' + HELPER_SHA838 +
             '\nTEST838_PATCHED_SOURCE_AST_PASS ' + str(len(patched838)) + ' ' + hashlib.sha256(patched838.encode()).hexdigest() + '\n')
import linecache as _lc838
for _nm838, _src838 in (('TEST838_LOCKED_ENGINE', patched838), ('TEST838_LOCKED_HELPERS', HELPER_SRC838)):
    _lc838.cache[_nm838] = (len(_src838), None, [x + '\n' for x in _src838.splitlines()], _nm838)
_sys838.stdout = Console838(_ORIG_OUT838, _fh838); _sys838.stderr = Console838(_ORIG_ERR838, _fh838)
TEST838_ERROR = None
try:
    exec(compile(patched838, 'TEST838_LOCKED_ENGINE', 'exec'), globals())
except BaseException as _e838:
    TEST838_ERROR = _e838
    _tbtext838 = _tb838.format_exc()
    _fh838.write('\n[TEST838 OUTER EXCEPTION]\n' + _tbtext838)
finally:
    _sys838.stdout, _sys838.stderr = _ORIG_OUT838, _ORIG_ERR838
    try:
        _fh838.flush(); _fh838.close()
    except Exception:
        pass
    _dir838 = globals().get('DIR829')
    if _dir838 is not None and _P838(_dir838).exists() and FULL_CONSOLE838.exists():
        _dst838 = _P838(_dir838) / FULL_CONSOLE838.name
        _sh838.move(str(FULL_CONSOLE838), str(_dst838)); FULL_CONSOLE838 = _dst838
if TEST838_ERROR is not None:
    D_ = globals().get('D829', {}) if isinstance(globals().get('D829'), dict) else {}
    bad = [c for c in D_.get('checks', []) if not c.get('pass')]
    say838('=' * 78); say838('TEST838 HATA')
    say838('Tür: %s.%s' % (type(TEST838_ERROR).__module__, type(TEST838_ERROR).__name__))
    say838('Mesaj: ' + repr(TEST838_ERROR)[:800])
    say838('Aşama: ' + CON838['phase'] + ' | geçen %s dk' % _mins838())
    if bad:
        say838('Başarısız kapı: %s | ayrıntı: %s' % (bad[-1].get('name'), str(bad[-1].get('detail'))[:400]))
    say838('Hata öncesi son motor satırları:')
    for x in CON838['last'][-4:]:
        say838('  ' + x[:240])
    tbl = _tbtext838.rstrip().splitlines()
    say838('Traceback (son %d satır; tamamı dosyada ve results.json içinde):' % min(40, len(tbl)))
    for x in tbl[-40:]:
        say838('  ' + x)
    files_report838()
    say838('Tam konsol kaydı: %s  SHA-256 %s' % (FULL_CONSOLE838, sha_path838(FULL_CONSOLE838) if FULL_CONSOLE838.exists() else '-'))
    say838('Not: tamamlanan ölçümler vektör dosyalarında; hücre yeniden çalıştırılırsa SHA doğrulanıp yeniden kullanılır.')
    raise SystemExit('TEST838_FAILED: ' + type(TEST838_ERROR).__name__)
try:
    final838(D829)
except Exception as _e838s:
    say838('!! Özet basılamadı (veri dosyalarda tam): ' + repr(_e838s))
    say838(_tb838.format_exc()[-1500:])
files_report838()
say838('=' * 78)
