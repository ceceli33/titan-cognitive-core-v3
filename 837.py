# AKBASCORE SILICON HIPPOCAMPUS — TEST837, single Colab cell (one A100-SXM4-80GB, frozen Qwen2.5-72B-Instruct NF4).
# CAUSAL DECOMPOSITION OF RELATIONAL SEARCH AND CONTEXT LOSS. Three independent experiments, all predeclared:
#   P1  FIRST-CONDITIONED SECOND SEARCH: anchor a (ORACLE = true first, MODEL = largest single-card hidden effect,
#       WRONG = fork) x every other bank card c, isolated physical mounts NULL, [a], [c], [a,c] / [c,a]; TEST831 rho.
#       Python trying all pairs is a CLASS C external search; the score is a native-state measurement.
#   P2  POSITION-PRESERVING PHYSICAL ABLATION: bank rho with cards REMOVED (TEST836), SUBSTITUTED by token-length-
#       matched neutral filler cartridges (positions, KV length, mask and RoPE phases preserved; verified), and
#       SUBSTITUTED with the competing chains of the other worlds also neutralised (NO_COMPETITION); both bank orders.
#   P3  PHYSICAL PAIR vs NATIVE KV STATE: the same bank and question under OFF / TRUE_KV / FORK_KV / IRRELEVANT_KV /
#       ROTATED_KV (+ one further native step from each own state); physical pairs [first, second], [fork, second],
#       [first, mirror]. Second-card top-1, margin, decision change vs measurement change, order sensitivity, offline
#       answer text. KV state and physical co-mounting are DIFFERENT interventions and are compared as information paths.
# Locked parts: TEST829 source (blob a5a25460), TEST834 helpers (834.py blob ab7b2046), bank_forward835 (835.py blob
# 9327cebc), state_after836 (836.py blob ee0038bb), TEST835/836 compact console. No GPU execution or result is claimed
# by the code author.
import urllib.request, hashlib, ast, json, time, random, math, re, numpy as np

REPO837 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
LOCK829_837 = "a5a25460a3a6bbdf62a0571a9b5ff19e64159cf7"
LOCK834_837 = "ab7b2046d7b7e7be18aed8c6ce5a1397e0c991d7"
LOCK835_837 = "9327cebc651f173fd547362825679a1a790fcd6b"
LOCK836_837 = "ee0038bb76cc937e7a0ce41edb8535178f6ba08f"
LOCK836LOG_837 = "cd2761aa3768c2ab065a0631a06e8f4cdc175d5e"   # prior evidence (read-only)
SEED837 = 8372026
EXPECTED_ARCH834 = (80, 8192, 64, 8, 128)
DEVICE_KIND837 = 'cuda'
WORLDS_EVAL837 = 6
BLOCK837 = 3
KINDS837 = ('first', 'second', 'changed', 'mirror', 'decoy', 'fork')      # 6 cards per world -> 18-card banks
SPACES837 = ('h', 'state', 'lp')
P2_MODES837 = ('REMOVE', 'SUBSTITUTE', 'NO_COMPETITION')
P2_ROLES837 = {'REMOVE': ('TRUE', 'FORK', 'MIRROR', 'MISMATCHED_IN_BANK'),
               'SUBSTITUTE': ('TRUE', 'FORK', 'MIRROR', 'MISMATCHED_IN_BANK'),
               'NO_COMPETITION': ('TRUE', 'FORK', 'MIRROR', 'INBOUND')}
MAX_NEW_TEXT837 = 10
SEC_FUSION837, SEC_PROBE837 = 0.6, 0.9
PRED_LIMIT_MIN837 = 240.0
HARD_BUDGET_MIN837 = 300.0
RESUME837 = True

def fetch837(name, lock, limit=400000):
    with urllib.request.urlopen(urllib.request.Request(REPO837 + name, headers={"User-Agent": "AKBASCORE-TEST837"}),
                                timeout=180) as f:
        raw = f.read(limit + 1)
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert len(raw) <= limit and blob == lock, ("STOP_SOURCE_CHANGED", name, blob)
    return raw

raw829_837 = fetch837("829.py", LOCK829_837)
raw834_837 = fetch837("834.py", LOCK834_837)
raw835_837 = fetch837("835.py", LOCK835_837)
raw836_837 = fetch837("836.py", LOCK836_837)
raw836log_837 = fetch837("836.log", LOCK836LOG_837)
src837 = raw829_837.decode("utf-8")

def extract837(raw, body_name, names):
    tree = ast.parse(raw.decode("utf-8"))
    bodies = [n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == body_name]
    assert len(bodies) == 1, ('BODY_NOT_UNIQUE', body_name)
    text = bodies[0].value.value
    nodes = [n for n in ast.parse(text).body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert sorted(n.name for n in nodes) == sorted(names), ('HELPER_SET_MISMATCH', body_name)
    return "\n\n".join(ast.get_source_segment(text, n) for n in nodes)
HELPERS834_837 = ('HeadProbe834', 'concat834', 'rprobe834', 'relocate834', 'rotate834', 'seal834', 'mount834', 'cspans834',
                  'card_mass834', 's0_834')
HELPERS835_837 = ('bank_forward835',)
HELPERS836_837 = ('state_after836',)
HELPER_SRC837 = (extract837(raw834_837, 'BODY834', HELPERS834_837) + "\n\n" + extract837(raw835_837, 'BODY835', HELPERS835_837)
                 + "\n\n" + extract837(raw836_837, 'BODY836', HELPERS836_837))
HELPER_SHA837 = hashlib.sha256(HELPER_SRC837.encode()).hexdigest()
HELPERS837 = HELPERS834_837 + HELPERS835_837 + HELPERS836_837

def patch837(text, old, new):
    assert text.count(old) == 1, ("PATCH_ANCHOR_NOT_UNIQUE", old[:80], text.count(old))
    return text.replace(old, new, 1)

src837 = patch837(src837, "SEED829 = 8292026", "SEED829 = %d" % SEED837)
src837 = patch837(src837, "RUN829 = 'TEST829_'", "RUN829 = 'TEST837_'")
src837 = patch837(src837, "WORLDS829 = 3                    # small pilot (directive); no automatic extension",
                  "WORLDS829 = %d                    # TEST837 sealed worlds" % WORLDS_EVAL837)
for a837, b837 in (("'TEST829_results.json'", "'TEST837_results.json'"), ("'TEST829.log'", "'TEST837.log'"),
                   ("'TEST829_blind_review.csv'", "'TEST837_case_table.csv'"),
                   ("'TEST829_offline_key.json'", "'TEST829_base_offline_key.json'")):
    src837 = patch837(src837, a837, b837)

PANEL_EXT837 = r'''
# ---------------- TEST837 PANEL EXTENSION (sealed before any model call) ----------------
def fresh837():
    while True:
        c = code829()
        if c not in seen829:
            seen829.add(c); return c
for w in worlds829:
    w['fork_end'] = fresh837()
    for kind in ('mirror', 'fork'):
        cid = 'E829_' + code829()
        assert cid not in cards829, 'CARD_ID_COLLISION'
        w['ids'][kind] = cid
    cards829[w['ids']['mirror']] = ('Evidence record. Domain: ' + w['world'] + '\n' + 'Directed relation: ' + w['end'] +
                                    ' -> ' + w['middle'] + '.\n')
    cards829[w['ids']['fork']] = ('Evidence record. Domain: ' + w['world'] + '\n' + 'Directed relation: ' + w['start'] +
                                  ' -> ' + w['fork_end'] + '.\n')
    for kind in ('mirror', 'fork'):
        card_meta829[w['ids'][kind]] = {'domain': w['world'], 'kind': kind, 'body_sha256': sha829(cards829[w['ids'][kind]])}
_rng837 = random.Random(SEED829 + 37)
QID837 = [questions829[i]['qid'] for i in range(len(worlds829))]
assert len(questions829) == len(worlds829), 'ONE_QUESTION_PER_WORLD'
BANKS837 = []
for bi in range(0, len(worlds829), BLOCK837):
    b_ = [worlds829[i]['ids'][k] for i in range(bi, bi + BLOCK837) for k in KINDS837]
    _rng837.shuffle(b_)
    BANKS837.append(b_)
# One neutral filler cartridge per bank card. Its text (no relation, token length equal to the card it replaces) is
# produced by a fixed procedure from the tokenizer BEFORE the model is loaded; IDs and roles are sealed here.
FILL837 = {}
for b_ in BANKS837:
    for c in b_:
        fid = 'E829_' + code829()
        assert fid not in cards829, 'CARD_ID_COLLISION'
        FILL837[c] = fid
        card_meta829[fid] = {'domain': None, 'kind': 'filler', 'filler_of': c, 'body_sha256': None}
def block837(wi):
    return wi // BLOCK837
def bank837(wi, order):
    b_ = list(BANKS837[block837(wi)])
    return b_ if order == 'FORWARD' else list(reversed(b_))
def sub837(base, repl):
    return [FILL837[c] if c in repl else c for c in base]
def p2_base837(wi, order, mode):
    base = bank837(wi, order)
    if mode != 'NO_COMPETITION':
        return base
    others = [worlds829[j] for j in range(block837(wi) * BLOCK837, block837(wi) * BLOCK837 + BLOCK837) if j != wi]
    comp = {x['ids'][k] for x in others for k in ('second', 'changed')}         # break the competing chains
    return sub837(base, comp)
def p2_mounts837(wi, order, mode, a, b):
    base = p2_base837(wi, order, mode)
    if mode == 'REMOVE':
        return {'ab': base, 'b': [c for c in base if c != a], 'a': [c for c in base if c != b],
                'null': [c for c in base if c not in (a, b)]}
    return {'ab': base, 'b': sub837(base, {a}), 'a': sub837(base, {b}), 'null': sub837(base, {a, b})}
def p2_target837(wi, role):
    w = worlds829[wi]
    if role == 'MISMATCHED_IN_BANK':
        return worlds829[block837(wi) * BLOCK837 + (wi + 1) % BLOCK837]['ids']['second']
    return w['ids'][{'TRUE': 'second', 'FORK': 'fork', 'MIRROR': 'mirror', 'INBOUND': 'decoy'}[role]]
JOBS837, JOBKEY837 = [], {}
JOBMAP837 = {}
def job837(ids, qid, phase, role):
    k = (tuple(ids), qid)
    if k not in JOBMAP837:
        j = 'J837_' + ''.join(_rng837.choice('0123456789ABCDEF') for _ in range(12))
        JOBMAP837[k] = j
        JOBS837.append({'job': j, 'mount': list(ids), 'qid': qid, 'phase': phase})
        JOBKEY837[j] = role
    return JOBMAP837[k]
for wa, w in enumerate(worlds829):
    q = QID837[wa]; bank = BANKS837[block837(wa)]
    job837([NULL829], q, 'P1', {'world': wa, 'kind': 'NULL'})
    for c in bank + [FILL837[w['ids']['second']]]:
        job837([c], q, 'P1', {'world': wa, 'kind': 'SINGLE', 'card': c})
    for atype, a in (('ORACLE', w['ids']['first']), ('WRONG', w['ids']['fork'])):
        cands = [c for c in bank if c != a] + ([FILL837[w['ids']['second']]] if atype == 'ORACLE' else [])
        for c in cands:
            job837([a, c], q, 'P1', {'world': wa, 'kind': 'PAIR', 'anchor': atype, 'card': c, 'order': 'FORWARD'})
            job837([c, a], q, 'P1', {'world': wa, 'kind': 'PAIR', 'anchor': atype, 'card': c, 'order': 'REVERSE'})
    for order in ('FORWARD', 'REVERSE'):
        for mode in P2_MODES837:
            for role in P2_ROLES837[mode]:
                ms = p2_mounts837(wa, order, mode, w['ids']['first'], p2_target837(wa, role))
                for slot, m in ms.items():
                    job837(m, q, 'P2', {'world': wa, 'kind': 'P2', 'mode': mode, 'role': role, 'order': order, 'slot': slot})
P3ITEMS837, P3KEY837 = [], {}
for wa, w in enumerate(worlds829):
    irr = worlds829[(wa + BLOCK837) % len(worlds829)]['ids']['second']
    for order in ('FORWARD', 'REVERSE'):
        specs = [('TRUE_KV', [w['ids']['first']], False, True), ('ROTATED_KV', [w['ids']['first']], True, False),
                 ('FORK_KV', [w['ids']['fork']], False, True), ('IRRELEVANT_KV', [irr], False, True)]
        states = []
        for role, cards, rot, step2 in specs:
            sid = 'S837_' + ''.join(_rng837.choice('0123456789ABCDEF') for _ in range(12))
            states.append({'sid': sid, 'cards': cards, 'rotate': rot, 'step2': step2}); P3KEY837[sid] = role
        _rng837.shuffle(states)
        P3ITEMS837.append({'qid': QID837[wa], 'order': order, 'bank': bank837(wa, order), 'states': states})
PHYS837 = []                                                        # physical pairs for offline answer readout
for wa, w in enumerate(worlds829):
    for role, m in (('PHYSICAL_PAIR', [w['ids']['first'], w['ids']['second']]),
                    ('PHYSICAL_WRONG_FIRST', [w['ids']['fork'], w['ids']['second']]),
                    ('PHYSICAL_WRONG_SECOND', [w['ids']['first'], w['ids']['mirror']])):
        PHYS837.append({'qid': QID837[wa], 'mount': m, 'role': role, 'world': wa})
_rng837.shuffle(JOBS837)
GROUPS837, GROUP_ORDER837 = {}, []
for j in JOBS837:
    m = tuple(j['mount'])
    if m not in GROUPS837:
        GROUPS837[m] = []; GROUP_ORDER837.append(m)
    GROUPS837[m].append(j['job'])

def fus_upper837(k, maxb, p_):
    if k <= 0:
        return 0
    c = int(globals().get('CHUNK', 128))
    return (p_ + maxb + c - 1) // c + (k - 1) * ((maxb + c - 1) // c)

def cost_upper837(tok_of, p_):
    mx = max(tok_of[c] for c in tok_of)
    up = {'fusion_forwards': 0, 'probe_forwards': 0, 'capture_forwards': 0, 'rank_forwards': 0, 'generation_forwards': 0}
    up['fusion_forwards'] += fus_upper837(1, mx, p_) + fus_upper837(2, mx, p_) + fus_upper837(1, mx, p_)
    up['probe_forwards'] += len(QID837) + 2 + 3 + 1; up['generation_forwards'] += 1
    up['fusion_forwards'] += fus_upper837(len(JOBS837[0]['mount']), mx, p_)
    for m, js in GROUPS837.items():
        up['fusion_forwards'] += fus_upper837(len(m), mx, p_); up['probe_forwards'] += len(js)
    nb = len(BANKS837[0])
    up['fusion_forwards'] += len(QID837) * 2 * (nb - 1) * fus_upper837(2, mx, p_)        # MODEL-anchor pairs (worst case)
    up['probe_forwards'] += len(QID837) * 2 * (nb - 1)
    for it in P3ITEMS837:
        up['fusion_forwards'] += fus_upper837(len(it['bank']), mx, p_)
        for s in it['states']:
            up['fusion_forwards'] += fus_upper837(len(s['cards']), mx, p_); up['probe_forwards'] += 3
        up['probe_forwards'] += 1
    off_f = (len(P3ITEMS837) // 2) * fus_upper837(nb, mx, p_) + len(PHYS837) * fus_upper837(2, mx, p_) + len(QID837) * 4
    off_g = (len(P3ITEMS837) // 2 * 5 + len(PHYS837)) * MAX_NEW_TEXT837
    up['fusion_forwards'] += 4 * fus_upper837(nb, mx, p_)                                   # position-equivalence mounts
    sec = ((up['fusion_forwards'] + off_f) * SEC_FUSION837 + up['probe_forwards'] * SEC_PROBE837 +
           (off_g + len(QID837) * 4) * SEC_FUSION837 + 120.0 + len(tok_of) * 2.0)
    maxmem = max(p_ + sum(tok_of.get(c, mx) for c in m) for m in GROUPS837)
    return {'numeric_upper': up, 'offline_upper': {'fusion_forwards': off_f, 'generation_forwards': off_g},
            'jobs_panel': len(JOBS837), 'mount_groups': len(GROUPS837), 'p3_items': len(P3ITEMS837),
            'physical_cartridges': len(tok_of), 'fillers': len(FILL837),
            'vector_disk_mb_estimate': round((len(JOBS837) + len(QID837) * 2 * (nb - 1)) * (8192 * 16 + 152064 * 8) / 2**20, 1),
            'max_memory_tokens': maxmem, 'minutes_upper_excluding_model_load': round(sec / 60.0, 1),
            'peak_vram_gib_expected': 'about 39-41 (TEST836 measured 39.54 GiB peak)',
            'scaling_note': 'P1 search cost per anchor = 2 x (N - 1) pair mounts + N singles: linear in bank size N'}
'''
src837 = patch837(src837,
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n",
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n" + PANEL_EXT837)

# Filler texts are generated with the tokenizer only (before the model is loaded), then committed as physical cartridges.
FILLER_HOOK837 = r'''
    def filler_text837(target, tokr):
        base = 'Neutral record. Domain: NONE\nNo directed relation is stated'
        for pad in (' here', ' now', ' only', ' x'):
            for r in range(0, 120):
                for tail in ('.\n', ' .\n', '!\n'):
                    t = base + pad * r + tail
                    if len(tokr.encode(t, add_special_tokens=False)) == target:
                        return t
        return None
    FILLTXT837 = {}
    for c837, f837 in FILL837.items():
        t837 = filler_text837(tok_counts829[c837], tok829)
        gate829('FILLER_TEXT_' + c837, t837 is not None and '->' not in t837, tok_counts829[c837])
        FILLTXT837[f837] = t837
        cards829[f837] = t837
        card_meta829[f837]['body_sha256'] = sha829(t837)
        tok_counts829[f837] = len(tok829.encode(t837, add_special_tokens=False))
    gate829('FILLER_LENGTHS_EQUAL', all(tok_counts829[FILL837[c]] == tok_counts829[c] for c in FILL837), len(FILL837))
    D829['fillers837'] = {f: {'replaces': c, 'tokens': tok_counts829[f], 'body_sha256': sha829(FILLTXT837[f])}
                          for c, f in FILL837.items()}
    D829['fillers837_sha256'] = sha829(json.dumps(D829['fillers837'], sort_keys=True))
'''
PRECOST837 = r'''
    PRE837 = cost_upper837(tok_counts829, 30)
    D829['predicted_cost837_pre_model'] = PRE837
    log829('TEST837_PREDICTED_COST_BEFORE_MODEL_LOAD', json.dumps(PRE837))
    gate829('TEST837_PREDICTED_BUDGET', PRE837['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN837,
            {'minutes_upper': PRE837['minutes_upper_excluding_model_load'], 'limit': PRED_LIMIT_MIN837})
'''
src837 = patch837(src837, "    del tok829\n", FILLER_HOOK837 + "    del tok829\n" + PRECOST837)

HYP837 = {
    'question': ('Can the second memory be found by a first-conditioned relational computation; is the bank-context loss '
                 'caused by position shifts, by competing chains, or by both; does the native KV state of the first '
                 'memory change the next selection; and how does physical co-mounting compare with KV transfer?'),
    'rho': 'rho = ||z_ab - z_a - z_b + z_0|| / ||z_b - z_0||, final-norm hidden (TEST831 feats831).',
    'valid_second': 'the own second link or the own alternative continuation (changed); both are valid closures.',
    'criteria': {
        'A1_ORACLE_CONDITIONAL_SEARCH': ('true first as anchor: top-1 of rho over the 17 other bank cards (+ filler) is a '
                                         'valid second in >= 10 of 12 (world, order) cells.'),
        'A2_END_TO_END': ('anchor = largest single-card hidden effect vs NULL (class B argmax), then the same search: valid '
                          'second top-1 in >= 10 of 12 cells (counted wrong whenever the anchor is not the true first).'),
        'A3_WRONG_FIRST': 'with the fork as anchor the best rho is lower than the best rho with the true first in >= 10 of 12 cells.',
        'A4_ORDER': 'A1 holds in both orders in >= 5 of 6 worlds.',
        'B_FILLER_NEUTRAL': ('filler of the second: rho(first, filler) < rho(first, second) in >= 11 of 12 cells and the '
                             'filler is never top-1; position equivalence of substituted mounts verified bitwise.'),
        'B_CONTEXT_CAUSE': ('per mode, a cell passes when rho_TRUE exceeds every control of that mode. With r, s, c the '
                            'REMOVE, SUBSTITUTE, NO_COMPETITION passes (of 12): NO_LOSS if r >= 10; POSITION if s >= 10; '
                            'COMPETITION if c >= 10; POSITION_PARTIAL if s >= r + 3; COMPETITION_PARTIAL if c >= s + 3; '
                            'else OTHER. Evaluated in this order.'),
        'C1_KV_TRANSFER': ('over the bank, decision = top-1 non-first card by mean attention gain over all 5120 heads vs '
                           'OFF. TRUE_KV valid-second top-1 count (12 cells) >= max(FORK_KV, IRRELEVANT_KV, ROTATED_KV) + 3.'),
        'C2_PHYSICAL_VS_KV': 'PHYSICAL path (A1 count) vs KV path (C1 TRUE_KV count): PHYSICAL_SUPERIOR if A1 - C1 >= 3.',
        'C3_PERSISTENCE': 'one further native step: TRUE_KV2 count >= max(FORK_KV2, IRRELEVANT_KV2) + 3.'},
    'decision': ('DEVAM (TEST838 justified) if (A1 and A2 and A3 PASS) or C1 PASS. DUR if A1 FAIL and C1 FAIL. Otherwise '
                 'YETERSİZ KANIT. A budget stop forces YETERSİZ KANIT.'),
    'classes': {'rho values, attention masses, KV states, hidden states': 'A (native)',
                'argmax, rho ranking, decision top-1': 'B (fixed numerical gate)',
                'trying every pair, choosing anchors, mounting': 'C (external search / execution)'}}

CLAIMS837 = {
    'verified_from_prior_research': [
        '836.log (blob cd2761aa): isolated hidden rho 11/12, ALT 10/12; bank rho 5/12 (both orders 1/6); P3 head counts '
        'after [first] ~ [fork] ~ [irrelevant] (e.g. 119/115/114 heads) -> no content-specific KV transfer; TEST832 '
        'decomposition: single-effect first 5/6, relevance cut never contains the second (0/6), isolated closure 11/12, '
        'mutual best 12/12, conflict detectable 10/12; predeclared decision YETERSİZ KANIT (CONTEXT, TRANSFER).',
        'The 836 removal ablation shifts the positions of every later card; it cannot separate position from competition.'],
    'implemented_in_TEST837': [
        'First-conditioned pair search over the whole bank with ORACLE, MODEL and WRONG anchors (class C search).',
        'Token-length-matched neutral filler cartridges and position-equivalence gates for substitution ablations.',
        'NO_COMPETITION banks (other worlds second/changed neutralised, positions preserved).',
        'KV-state vs physical-pair comparison with top-1, margins, decision change, one further native step, answer text.'],
    'demonstrated_by_TEST837': 'filled only from this run'}

BODY837 = r'''
D829['test'] = '837'
D829['controller'] = 'NONE_DECOMPOSITION; P1 SEARCH = CLASS C EXTERNAL; ARGMAX = CLASS B'
D829['sources837'] = {'829': LOCK829_837, '834': LOCK834_837, '835': LOCK835_837, '836': LOCK836_837,
                      '836_log': LOCK836LOG_837, 'helpers_sha256': HELPER_SHA837, 'helpers': list(HELPERS837)}
D829['hypotheses837'] = PANEL829['test837']['hypotheses']
D829['limitations'] = [
    'P1 tries every pair in Python (class C). A successful search is not model-native addressing.',
    'Fillers preserve token count (hence positions, KV length, mask, RoPE phases) but not token identity.',
    'Six sealed worlds, one template, one model; 12 (world, order) cells are not 12 independent worlds.',
    'KV-state transfer and physical co-mounting are different interventions; they are compared as information paths only.',
    'Answer text is produced offline after all numeric work, with the TEST827 boundary instruction.',
    'No GPU execution or result is claimed by the code author.']
gate829('PANEL_FRESH_SEED', SEED829 == SEED837, SEED829)
gate829('NO_CONTROL_TEXT', MAX_NEW_CONTROL829 == 0)
gate829('WORLD_COUNT', len(worlds829) == WORLDS_EVAL837 and len(QID837) == WORLDS_EVAL837)
gate829('JOBS_UNIQUE', len({(tuple(j['mount']), j['qid']) for j in JOBS837}) == len(JOBS837), len(JOBS837))
gate829('CARTRIDGES_PHYSICAL', all(c in entries for j in JOBS837 for c in j['mount']) and
        all(c in entries for it in P3ITEMS837 for s in it['states'] for c in s['cards'] + it['bank']))
gate829('FILLERS_COMMITTED_EQUAL_LENGTH', all(int(entries[FILL837[c]]['body_tokens']) == int(entries[c]['body_tokens'])
                                              for c in FILL837), len(FILL837))
def copy_receivers837(src):
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'copy':
            r = n.func.value
            out.append(isinstance(r, ast.Call) and isinstance(r.func, ast.Attribute) and r.func.attr == 'numpy')
    return out
cr837 = copy_receivers837(HELPER_SRC837) + copy_receivers837(BODY837_TEXT)
gate829('STATIC_COPY_RECEIVERS_ARE_NDARRAY', all(cr837), {'copy_calls': len(cr837)})
exec(compile(HELPER_SRC837, 'TEST837_LOCKED_HELPERS', 'exec'), globals())
gate829('HELPERS_LOADED', all(callable(globals().get(x)) for x in HELPERS837), HELPER_SHA837)
gate829('ENGINE_SYMBOLS837', all(callable(globals().get(x)) for x in
        ('cache_build', 'pairs', 'rephase', 'Cut3Diagnostic', 'AttentionIntervention', 'prompt_ids', 'build_fusion',
         'memory_seals', 'compare_seals', 'observe_state', 'kv_digest', 'safe_load', 'cosdist829', 'full_readout829',
         'free_generate', 'answer_prompt829')))
gate829('ARCH_DIMS', (NL, H, QH, KVH, HD) == EXPECTED_ARCH834 and int(model.config.num_attention_heads) == QH and
        int(model.config.num_key_value_heads) == KVH and int(model.config.hidden_size) == H, (NL, H, QH, KVH, HD))
gate829('BF16_COMPUTE', DTYPE == _torch829.bfloat16, str(DTYPE))
gate829('NF4_LINEAR4BIT', any(isinstance(m_, bitsandbytes.nn.Linear4bit) for m_ in model.modules()))
gate829('WEIGHTS_FROZEN', all(not p_.requires_grad for p_ in model.parameters()))
gate829('DEVICE', str(DEV).startswith(DEVICE_KIND837), str(DEV))
gate829('ROPE_MODULE', callable(getattr(model.model, 'rotary_emb', None)))
gate829('SDPA_MODULE', F is _torch829.nn.functional and F.scaled_dot_product_attention is SDPA829)
gate829('PREFIX_P', P == 30, P)
gate829('PRIOR_LOG_PRESENT', b'T2_BANK_CONTEXT' in raw836log_837)
POST837 = cost_upper837({c: int(entries[c]['body_tokens']) for c in cards829}, P)
D829['predicted_cost837'] = POST837
log829('TEST837_PREDICTED_COST', json.dumps(POST837))
gate829('PREDICTED_BUDGET_POST_LOAD', POST837['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN837,
        POST837['minutes_upper_excluding_model_load'])
QTEXT837 = {q['qid']: q['question'] for q in questions829}
LQ834 = {qid: list(prompt_ids(t)) for qid, t in QTEXT837.items()}
gate829('FUSION_TOKENS_WITH_STATE', POST837['max_memory_tokens'] + 2 * max(len(v) for v in LQ834.values()) + 64 <= MAX_FUSED_TOKENS,
        POST837['max_memory_tokens'])
try:
    free837, _ = _torch829.cuda.mem_get_info()
    gate829('VRAM_HEADROOM', free837 / 2**30 >= 8.0, round(free837 / 2**30, 2))
except Exception as e837:
    gate829('VRAM_HEADROOM', False, repr(e837))
D829['noninterference837'] = noninterference829([NULL829], questions829[0]['question'])
for k837, v837 in D829['noninterference837'].items():
    gate829('NONINTERFERENCE_' + k837.upper(), bool(v837), v837)
COUNT834 = {'fusion_forwards': fusion_forwards829([NULL829]), 'probe_forwards': 3, 'capture_forwards': 0,
            'rank_forwards': 0, 'generation_forwards': 1, 'mounts': 1}
T0_837 = time.perf_counter()
SEAL_LAYERS834 = (0, CUT, NL // 2, NL - 1)
rs837 = np.random.default_rng(SEED837 + 33)
ROT834 = []
for l837 in range(NL):
    mats837 = []
    for j837 in range(KVH):
        qm837, rm837 = np.linalg.qr(rs837.standard_normal((HD, HD)))
        mats837.append(qm837 * np.sign(np.diag(rm837))[None, :])
    ROT834.append(torch.tensor(np.stack(mats837).astype(np.float32), device=DEV))

memN837, nN837 = mount834([NULL829], 'NULL')
sealN837 = seal834(memN837)
SNULL834 = {}
for qid837 in QTEXT837:
    pN = rprobe834(memN837, None, LQ834[qid837])
    SNULL834[qid837] = {'S': [(k.clone(), v.clone()) for k, v in pN['S_raw']], 'pos': pN['start'], 'h': pN['h'],
                        'state': pN['state']}
    del pN
gate829('KV_SEAL_NULL_AFTER_PROBES', seal834(memN837) == sealN837)
del memN837; gc.collect(); release()

jE837 = next(j for j in JOBS837 if len(j['mount']) == 2)
memE837, nE837 = mount834(jE837['mount'], 'EQUIV')
b0E837 = int(entries[jE837['mount'][0]]['body_tokens'])
spE837 = {'B0': (P, P + b0E837), 'B1': (P + b0E837, nE837)}
with Readout829() as roE837:
    stE837, attE837 = observe_state(memE837, QTEXT837[jE837['qid']], spE837)
COUNT834['probe_forwards'] += 1
pE837 = rprobe834(memE837, None, LQ834[jE837['qid']])
hpm837 = max(abs(float(pE837['rows'][l][:, spE837[s][0]:spE837[s][1]].sum(-1).mean()) - float(attE837[str(l)][s + '_mass']))
             for l in (4, 20, 40, 79) for s in ('B0', 'B1'))
D829['probe_equivalence837'] = {
    'cut3_state_bitwise': bool(np.array_equal(stE837.float().cpu().numpy().astype(np.float64), pE837['state'])),
    'final_hidden_bitwise': bool(np.array_equal(roE837.h.reshape(-1).double().cpu().numpy(), pE837['h'])),
    'headprobe_mass_max_abs_vs_locked_probe': hpm837}
gate829('PROBE_EQUALS_OBSERVE_STATE_CUT3', D829['probe_equivalence837']['cut3_state_bitwise'])
gate829('PROBE_EQUALS_OBSERVE_STATE_HIDDEN', D829['probe_equivalence837']['final_hidden_bitwise'])
gate829('HEADPROBE_EQUALS_LOCKED_ATTENTION_PROBE', hpm837 <= 2e-6, hpm837)
del memE837, pE837, stE837; gc.collect(); release()

# ---- position equivalence of substitution: n, spans and lower-layer key rows of untouched cards identical ----
def pos_equiv837(full, subst, changed):
    m1, n1 = mount834(full, 'PEQ_A'); m2, n2 = mount834(subst, 'PEQ_B')
    s1 = cspans834(full); s2 = cspans834(subst)
    same_spans = n1 == n2 and [(a, b) for _, a, b in s1] == [(a, b) for _, a, b in s2]
    rows = []
    for (c1, a, b), (c2, _, _) in zip(s1, s2):
        if c1 == c2 and c1 not in changed:
            rows.extend(range(a, b))
    eq = {}
    for l in range(CUT + 1):
        k1 = m1[l][0][:, :, rows, :]; k2 = m2[l][0][:, :, rows, :]
        v1 = m1[l][1][:, :, rows, :]; v2 = m2[l][1][:, :, rows, :]
        eq[l] = bool(torch.equal(k1, k2)) and bool(torch.equal(v1, v2))
    pref = bool(torch.equal(m1[0][0][:, :, :P, :], m2[0][0][:, :, :P, :]))      # informational (prefix forged per card)
    del m1, m2; gc.collect(); release()
    return {'n_equal': n1 == n2, 'spans_equal': same_spans, 'lower_layers_untouched_rows_bitwise': eq, 'prefix_bitwise': pref,
            'untouched_rows': len(rows)}
peqcard837 = BANKS837[0][len(BANKS837[0]) // 2]          # label-free choice: middle card of the first bank
PEQ837 = {}
for order837 in ('FORWARD', 'REVERSE'):
    full837 = list(BANKS837[0]) if order837 == 'FORWARD' else list(reversed(BANKS837[0]))
    PEQ837[order837] = pos_equiv837(full837, sub837(full837, {peqcard837}), {peqcard837})
D829['position_equivalence837'] = PEQ837
gate829('POSITION_EQUIVALENCE_SUBSTITUTION', all(v['n_equal'] and v['spans_equal'] and
                                                 all(v['lower_layers_untouched_rows_bitwise'].values()) for v in PEQ837.values()),
        PEQ837)

# ---- per-job vector store (SHA-256 manifest; job-level resume) ----
VDIR837 = DIR829 / 'TEST837_vectors'
VDIR837.mkdir(exist_ok=True)
MAN837 = DIR829 / 'TEST837_vector_manifest.jsonl'
HEADER837 = {'panel_sha256': PANEL_SHA829, 'body_sha256': PANEL829['test837']['body_sha256'], 'helpers_sha256': HELPER_SHA837,
             'fillers_sha256': D829['fillers837_sha256']}
VEC837 = {}
P3RES837 = {}
D829['resume837'] = {'enabled': RESUME837, 'source': None, 'reused_jobs': 0, 'reused_p3': 0, 'reason': None}
def load_npz837(path):
    with np.load(path, allow_pickle=False) as z:
        return {k: np.array(z[k], copy=True) for k in z.files}
if RESUME837:
    for cand in sorted(DIR829.parent.glob('TEST837_*/TEST837_vector_manifest.jsonl'), reverse=True):
        if cand.parent == DIR829:
            continue
        try:
            lines = cand.read_text(encoding='utf-8').splitlines()
            if not lines or json.loads(lines[0]).get('header') != HEADER837:
                D829['resume837']['reason'] = 'header mismatch in ' + str(cand); continue
            got, got3 = {}, {}
            for ln in lines[1:]:
                o = json.loads(ln); f = cand.parent / 'TEST837_vectors' / o['file']
                if not f.exists() or sha_file(f) != o['sha256']:
                    continue
                (got if o['kind'] == 'job' else got3)[o['key']] = load_npz837(f)
            VEC837.update(got); P3RES837.update(got3)
            D829['resume837'].update({'source': str(cand), 'reused_jobs': len(got), 'reused_p3': len(got3),
                                      'reason': 'header and per-file SHA-256 verified'})
            break
        except Exception as e837r:
            D829['resume837']['reason'] = 'unreadable ' + str(cand) + ' ' + repr(e837r)
log829('TEST837_RESUME', json.dumps(D829['resume837']))
with MAN837.open('w', encoding='utf-8') as fh837:
    fh837.write(json.dumps({'header': HEADER837}, sort_keys=True) + '\n')
def save_vec837(kind, key, arrays):
    f = VDIR837 / (key + '.npz')
    np.savez(f, **arrays)
    with MAN837.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps({'kind': kind, 'key': key, 'file': f.name, 'sha256': sha_file(f)}, sort_keys=True) + '\n')
for k837 in list(VEC837):
    save_vec837('job', k837, VEC837[k837])
for k837 in list(P3RES837):
    save_vec837('p3', k837, P3RES837[k837])

# ==================================================================================================================
# MEASUREMENT RUNTIME (sealed panel; opaque job IDs only). Until the OFFLINE PHASE no role or label is read.
# ==================================================================================================================
BUDGET_STOP837 = False
ALLJOBS837 = {j['job']: j for j in JOBS837}
KEY2JOB837 = {(tuple(j['mount']), j['qid']): j['job'] for j in JOBS837}
def measure_jobs837(job_ids, tag):
    global BUDGET_STOP837
    groups, order = {}, []
    for jj in job_ids:
        m = tuple(ALLJOBS837[jj]['mount'])
        if m not in groups:
            groups[m] = []; order.append(m)
        groups[m].append(jj)
    ng = len(order); step = max(1, ng // 3)
    log829('TEST837_PROGRESS', tag, 0, '/', ng)
    for gi, m in enumerate(order):
        todo = [jj for jj in groups[m] if jj not in VEC837]
        if todo:
            if (time.perf_counter() - T0_837) / 60.0 > HARD_BUDGET_MIN837:
                BUDGET_STOP837 = True
                log829('TEST837_BUDGET_STOP', tag, 'mount_groups_done', gi, 'of', ng); return
            memx, n = mount834(list(m), tag + '_G%d' % gi)
            seal = seal834(memx)
            for jj in todo:
                p = rprobe834(memx, None, LQ834[ALLJOBS837[jj]['qid']], keep_lp=True)
                lp = p['lp'].detach().to(device='cpu', dtype=_torch829.float64).numpy()
                arr = {'h': np.asarray(p['h'], dtype=np.float64), 'state': np.asarray(p['state'], dtype=np.float64),
                       'lp': np.asarray(lp, dtype=np.float64), 'entropy': np.asarray([p['summary']['entropy_nats']])}
                VEC837[jj] = arr; save_vec837('job', jj, arr)
                del p, lp
            gate829('MEAS_KV_SEAL_' + tag + '_G%d' % gi, seal834(memx) == seal)
            del memx; gc.collect(); release()
        if (gi + 1) % step == 0 or gi + 1 == ng:
            log829('TEST837_PROGRESS', tag, gi + 1, '/', ng)
t_meas837 = time.perf_counter()
# P1a: NULL and single-card forwards; P1b: designed pairs (ORACLE / WRONG anchors, opaque)
measure_jobs837([j['job'] for j in JOBS837 if j['phase'] == 'P1' and len(j['mount']) == 1], 'P1_SINGLES')
# MODEL anchor: largest single-card hidden effect vs NULL over the bank (class B argmax on native distances)
MODEL_ANCHOR837 = {}
RTJOBS837 = []
if not BUDGET_STOP837:
    for wa837 in range(len(QID837)):
        q = QID837[wa837]; bank = BANKS837[wa837 // BLOCK837]
        hn = VEC837[KEY2JOB837[((NULL829,), q)]]['h']
        eff = {c: cosdist829(VEC837[KEY2JOB837[((c,), q)]]['h'], hn) for c in bank}
        anc = max(bank, key=lambda c: (eff[c], -bank.index(c)))
        MODEL_ANCHOR837[q] = {'anchor': anc, 'effects': eff}
        for c in bank:
            if c == anc:
                continue
            for m in ([anc, c], [c, anc]):
                k = (tuple(m), q)
                if k not in KEY2JOB837:
                    jj = 'J837M_' + sha829(json.dumps([q] + m))[:12]
                    rec = {'job': jj, 'mount': list(m), 'qid': q, 'phase': 'P1_MODEL'}
                    ALLJOBS837[jj] = rec; KEY2JOB837[k] = jj; RTJOBS837.append(rec)
    D829['model_anchor837'] = MODEL_ANCHOR837
    D829['runtime_jobs837'] = RTJOBS837
pairs837 = [j['job'] for j in JOBS837 if j['phase'] == 'P1' and len(j['mount']) == 2] + [j['job'] for j in RTJOBS837]
if not BUDGET_STOP837:
    measure_jobs837(pairs837, 'P1_PAIRS')
if not BUDGET_STOP837:
    measure_jobs837([j['job'] for j in JOBS837 if j['phase'] == 'P2'], 'P2_BANK')
D829['measure_seconds837'] = round(time.perf_counter() - t_meas837, 3)
jR837 = JOBS837[0]
if jR837['job'] in VEC837:
    memR837, nR837 = mount834(jR837['mount'], 'REPLAY')
    pR837 = rprobe834(memR837, None, LQ834[jR837['qid']])
    D829['determinism837'] = {'hidden_bitwise': bool(np.array_equal(pR837['h'], VEC837[jR837['job']]['h'])),
                              'cut3_bitwise': bool(np.array_equal(pR837['state'], VEC837[jR837['job']]['state']))}
    gate829('DETERMINISM_REPLAY', D829['determinism837']['hidden_bitwise'] and D829['determinism837']['cut3_bitwise'],
            D829['determinism837'])
    del memR837, pR837; gc.collect(); release()
else:
    D829['determinism837'] = {'hidden_bitwise': None, 'cut3_bitwise': None}

# ---- P3: same bank, same question; KV states vs OFF; one further native step from own states ----
def bank_forward837(memx, n, qid, S, csp):
    p = rprobe834(memx, S, LQ834[qid])
    out = {'M': card_mass834(p['rows'], csp).astype(np.float32), 'h': np.asarray(p['h'], dtype=np.float64),
           'S': relocate834(p['S_raw'], p['start'], n, len(LQ834[qid]))}
    del p
    return out
for ii837, it in enumerate(P3ITEMS837):
    keys = ['P3_%d_OFF' % ii837] + ['P3_%d_%s' % (ii837, s['sid']) for s in it['states']] + \
           ['P3_%d_%s_STEP2' % (ii837, s['sid']) for s in it['states'] if s['step2']]
    if all(k in P3RES837 for k in keys) or BUDGET_STOP837:
        continue
    if (time.perf_counter() - T0_837) / 60.0 > HARD_BUDGET_MIN837:
        BUDGET_STOP837 = True; log829('TEST837_BUDGET_STOP', 'P3', ii837); break
    bank = list(it['bank']); qid = it['qid']; scache = {}
    memB, nB = mount834(bank, 'P3BANK_%d' % ii837)
    sealB = seal834(memB); csp = cspans834(bank)
    f0 = bank_forward837(memB, nB, qid, s0_834(qid, nB), csp)
    P3RES837[keys[0]] = {'M': f0['M'], 'h': f0['h']}; save_vec837('p3', keys[0], P3RES837[keys[0]])
    del f0
    for s in it['states']:
        S = state_after836(s['cards'], qid, nB, scache)
        if s['rotate']:
            S = rotate834(S)
        f = bank_forward837(memB, nB, qid, S, csp)
        k = 'P3_%d_%s' % (ii837, s['sid'])
        P3RES837[k] = {'M': f['M'], 'h': f['h']}; save_vec837('p3', k, P3RES837[k])
        if s['step2']:
            f2 = bank_forward837(memB, nB, qid, f['S'], csp)
            P3RES837[k + '_STEP2'] = {'M': f2['M'], 'h': f2['h']}; save_vec837('p3', k + '_STEP2', P3RES837[k + '_STEP2'])
            del f2
        del S, f
    gate829('MEAS_KV_SEAL_P3BANK_%d' % ii837, seal834(memB) == sealB)
    del memB, scache; gc.collect(); release()
    log829('TEST837_PROGRESS', 'P3', ii837 + 1, '/', len(P3ITEMS837))
D829['budget_stop837'] = BUDGET_STOP837

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
for cid837 in cards829:
    gate829('FINAL_SHA_' + cid837, sha_file(CART_DIR / entries[cid837]['file']) == entries[cid837]['sha256'])
COUNT_NUMERIC837 = dict(COUNT834)
gate829('COUNTED_WITHIN_UPPER_BOUND', all(COUNT_NUMERIC837[k] <= POST837['numeric_upper'][k] for k in POST837['numeric_upper']),
        {'counted': COUNT_NUMERIC837, 'upper': POST837['numeric_upper']})

# ==================================================================================================================
# OFFLINE PHASE: all measurements saved; roles are read only from here. Answer text is produced only here.
# ==================================================================================================================
log829('TEST837_OFFLINE_START')
TEXT837 = {}
if not BUDGET_STOP837:
    for wa837, w837 in enumerate(worlds829):                    # P3 text: bank (FORWARD) + state
        it = next(x for x in P3ITEMS837 if x['qid'] == QID837[wa837] and x['order'] == 'FORWARD')
        memB, nB = mount834(it['bank'], 'TXTBANK_%d' % wa837); scache = {}
        conds = [('OFF', None)] + [(P3KEY837[s['sid']], s) for s in it['states']]
        for role, s in conds:
            S = s0_834(it['qid'], nB) if s is None else state_after836(s['cards'], it['qid'], nB, scache)
            if s is not None and s['rotate']:
                S = rotate834(S)
            o = free_generate(concat834(memB, S), answer_prompt829(QTEXT837[it['qid']]), seed=None, gain=0.,
                              max_new=MAX_NEW_TEXT837, spans=None)
            COUNT834['generation_forwards'] += int(o['generated_tokens'])
            TEXT837[(wa837, role)] = o['raw'].strip()
            del S
        del memB, scache; gc.collect(); release()
    for ph in PHYS837:
        memx, n = mount834(ph['mount'], 'TXTPHYS')
        o = free_generate(memx, answer_prompt829(QTEXT837[ph['qid']]), seed=None, gain=0., max_new=MAX_NEW_TEXT837, spans=None)
        COUNT834['generation_forwards'] += int(o['generated_tokens'])
        TEXT837[(ph['world'], ph['role'])] = o['raw'].strip()
        del memx; gc.collect(); release()
KIND837 = {cid: m['kind'] for cid, m in card_meta829.items()}
DOM837 = {cid: m['domain'] for cid, m in card_meta829.items()}
def role837(cid, w):
    if cid is None:
        return None
    if KIND837.get(cid) == 'filler':
        return 'FILLER'
    return ('OWN_' if DOM837.get(cid) == w['world'] else 'OTHER_') + str(KIND837.get(cid)).upper()
def valid837(cid, w):
    return cid in (w['ids']['second'], w['ids']['changed'])
def rho837(mounts, q, space='h'):
    ks = {s: KEY2JOB837.get((tuple(m), q)) for s, m in mounts.items()}
    if any(k is None or k not in VEC837 for k in ks.values()):
        return None
    z0, za, zb, zab = (VEC837[ks[s]][space] for s in ('null', 'a', 'b', 'ab'))
    return float(np.linalg.norm(zab - za - zb + z0) / max(np.linalg.norm(zb - z0), 1e-300))
def pair_mounts837(a, c, order):
    return {'null': [NULL829], 'a': [a], 'b': [c], 'ab': [a, c] if order == 'FORWARD' else [c, a]}
# ---- P1 ----
P1EV837 = []
for wa, w in enumerate(worlds829):
    q = QID837[wa]; bank = BANKS837[wa // BLOCK837]
    anchors = {'ORACLE': w['ids']['first'], 'WRONG': w['ids']['fork'],
               'MODEL': MODEL_ANCHOR837.get(q, {}).get('anchor')}
    for atype, a in anchors.items():
        if a is None:
            continue
        cands = [c for c in bank if c != a] + ([FILL837[w['ids']['second']]] if atype == 'ORACLE' else [])
        for order in ('FORWARD', 'REVERSE'):
            sc = {c: rho837(pair_mounts837(a, c, order), q) for c in cands}
            sc = {c: v for c, v in sc.items() if v is not None}
            if len(sc) < len(cands):
                continue
            rk = sorted(sc, key=lambda c: (-sc[c], bank.index(c) if c in bank else 99))
            vrank = next((i + 1 for i, c in enumerate(rk) if valid837(c, w)), None)
            best_valid = max([sc[c] for c in rk if valid837(c, w)] or [None]) if any(valid837(c, w) for c in rk) else None
            best_invalid = max([sc[c] for c in rk if not valid837(c, w)] or [float('nan')])
            rec = {'world': wa, 'anchor': atype, 'anchor_role': role837(a, w), 'order': order,
                   'top1_role': role837(rk[0], w), 'top1_valid': valid837(rk[0], w), 'valid_rank': vrank,
                   'top3_valid': vrank is not None and vrank <= 3, 'both_valid_top2': all(valid837(c, w) for c in rk[:2]),
                   'best_rho': sc[rk[0]], 'margin_valid_vs_invalid': (best_valid - best_invalid) if best_valid is not None else None,
                   'top5_roles': [role837(c, w) for c in rk[:5]]}
            for cls, fn in (('FORK', lambda c: c == w['ids']['fork']), ('MIRROR', lambda c: c == w['ids']['mirror']),
                            ('INBOUND', lambda c: c == w['ids']['decoy']),
                            ('OTHER_WORLD', lambda c: DOM837.get(c) not in (w['world'], None))):
                xs = [sc[c] for c in sc if fn(c)]
                rec['margin_vs_' + cls] = (best_valid - max(xs)) if (xs and best_valid is not None) else None
            if atype == 'ORACLE':
                f = FILL837[w['ids']['second']]
                rec['filler_rho'] = sc.get(f); rec['second_rho'] = sc.get(w['ids']['second'])
                rec['filler_top1'] = rk[0] == f
            P1EV837.append(rec)
def p1count837(atype, key):
    xs = [r for r in P1EV837 if r['anchor'] == atype]
    return [sum(1 for r in xs if r[key]), len(xs)]
a1 = p1count837('ORACLE', 'top1_valid'); a2 = p1count837('MODEL', 'top1_valid')
mod_ok = {r['world'] for r in P1EV837 if r['anchor'] == 'MODEL' and r['anchor_role'] == 'OWN_FIRST'}
a2_strict = [sum(1 for r in P1EV837 if r['anchor'] == 'MODEL' and r['top1_valid'] and r['world'] in mod_ok),
             sum(1 for r in P1EV837 if r['anchor'] == 'MODEL')]
a3 = [0, 0]
for wa in range(len(worlds829)):
    for order in ('FORWARD', 'REVERSE'):
        o = next((r for r in P1EV837 if r['anchor'] == 'ORACLE' and r['world'] == wa and r['order'] == order), None)
        g = next((r for r in P1EV837 if r['anchor'] == 'WRONG' and r['world'] == wa and r['order'] == order), None)
        if o and g:
            a3[1] += 1; a3[0] += g['best_rho'] < o['best_rho']
a4 = [0, 0]
for wa in range(len(worlds829)):
    xs = [r for r in P1EV837 if r['anchor'] == 'ORACLE' and r['world'] == wa]
    if len(xs) == 2:
        a4[1] += 1; a4[0] += all(r['top1_valid'] for r in xs)
fl = [r for r in P1EV837 if r['anchor'] == 'ORACLE' and r.get('filler_rho') is not None and r.get('second_rho') is not None]
bfill = [sum(1 for r in fl if r['filler_rho'] < r['second_rho']), len(fl)]
bfill_top = sum(1 for r in fl if r['filler_top1'])
def ok837(k, n, need):
    return 'INCONCLUSIVE' if n == 0 else ('PASS' if k >= need else 'FAIL')
A1 = ok837(a1[0], a1[1], 10) if a1[1] == 12 else 'INCONCLUSIVE'
A2 = ok837(a2_strict[0], a2_strict[1], 10) if a2_strict[1] == 12 else 'INCONCLUSIVE'
A3 = ok837(a3[0], a3[1], 10) if a3[1] == 12 else 'INCONCLUSIVE'
A4 = ok837(a4[0], a4[1], 5) if a4[1] == 6 else 'INCONCLUSIVE'
BF = ('PASS' if bfill[1] == 12 and bfill[0] >= 11 and bfill_top == 0 else
      ('INCONCLUSIVE' if bfill[1] < 12 else 'FAIL'))
# ---- P2 ----
P2EV837 = []
for wa, w in enumerate(worlds829):
    q = QID837[wa]
    for order in ('FORWARD', 'REVERSE'):
        for mode in P2_MODES837:
            vals = {}
            for role in P2_ROLES837[mode]:
                for sp in SPACES837:
                    vals.setdefault(sp, {})[role] = rho837(p2_mounts837(wa, order, mode, w['ids']['first'], p2_target837(wa, role)), q, sp)
            rec = {'world': wa, 'order': order, 'mode': mode, 'rho_h': vals['h'], 'rho_state': vals['state'], 'rho_lp': vals['lp']}
            for sp in SPACES837:
                v = vals[sp]
                rec['pass_' + sp] = (all(x is not None for x in v.values()) and
                                     all(v['TRUE'] > v[r] for r in P2_ROLES837[mode] if r != 'TRUE'))
                rec['common_pass_' + sp] = (all(v.get(r) is not None for r in ('TRUE', 'FORK', 'MIRROR')) and
                                            v['TRUE'] > v['FORK'] and v['TRUE'] > v['MIRROR'])
            P2EV837.append(rec)
def p2count837(mode, key='pass_h'):
    xs = [r for r in P2EV837 if r['mode'] == mode]
    return [sum(1 for r in xs if r[key]), len(xs)]
def p2orders837(mode):
    ok = tot = 0
    for wa in range(len(worlds829)):
        xs = [r for r in P2EV837 if r['mode'] == mode and r['world'] == wa]
        if len(xs) == 2:
            tot += 1; ok += all(r['pass_h'] for r in xs)
    return [ok, tot]
r_, s_, c_ = (p2count837(m)[0] for m in P2_MODES837)
n2 = min(p2count837(m)[1] for m in P2_MODES837)
if n2 < 12:
    CAUSE837 = 'INCONCLUSIVE'
elif r_ >= 10:
    CAUSE837 = 'NO_LOSS'
elif s_ >= 10:
    CAUSE837 = 'POSITION'
elif c_ >= 10:
    CAUSE837 = 'COMPETITION'
elif s_ >= r_ + 3:
    CAUSE837 = 'POSITION_PARTIAL'
elif c_ >= s_ + 3:
    CAUSE837 = 'COMPETITION_PARTIAL'
else:
    CAUSE837 = 'OTHER'
# ---- P3 ----
P3EV837 = []
for ii837, it in enumerate(P3ITEMS837):
    if 'P3_%d_OFF' % ii837 not in P3RES837:
        continue
    wa = QID837.index(it['qid']); w = worlds829[wa]; bank = it['bank']; idx = {c: i for i, c in enumerate(bank)}
    fi = idx[w['ids']['first']]; vi = [idx[w['ids']['second']], idx[w['ids']['changed']]]
    nonfirst = [i for i in range(len(bank)) if i != fi]
    M0 = P3RES837['P3_%d_OFF' % ii837]['M'].astype(np.float64); h0 = P3RES837['P3_%d_OFF' % ii837]['h']
    def decide(M, base):
        agg = M.mean(axis=(0, 1)); gain = (M - base).mean(axis=(0, 1)) if base is not None else agg
        tg = max(nonfirst, key=lambda i: gain[i]); ta = max(nonfirst, key=lambda i: agg[i])
        rival = max([gain[i] for i in nonfirst if i not in vi])
        return {'top1_gain': role837(bank[tg], w), 'top1_gain_valid': tg in vi, 'top1_mass': role837(bank[ta], w),
                'top1_mass_valid': ta in vi, 'gain_margin_valid_vs_rival': float(max(gain[i] for i in vi) - rival),
                'valid_rank_by_gain': 1 + sorted(nonfirst, key=lambda i: -gain[i]).index(max(vi, key=lambda i: gain[i]))}
    rec = {'world': wa, 'order': it['order'], 'OFF': decide(M0, None)}
    for s in it['states']:
        role = P3KEY837[s['sid']]
        for suffix in ('', '_STEP2'):
            k = 'P3_%d_%s%s' % (ii837, s['sid'], suffix)
            if k not in P3RES837:
                continue
            M = P3RES837[k]['M'].astype(np.float64)
            d = decide(M, M0)
            d['hidden_shift_norm'] = float(np.linalg.norm(P3RES837[k]['h'] - h0))
            d['mass_top1_changed_vs_OFF'] = d['top1_mass'] != rec['OFF']['top1_mass']
            rec[role + ('2' if suffix else '')] = d
    P3EV837.append(rec)
def p3count837(role, key='top1_gain_valid'):
    xs = [r[role] for r in P3EV837 if role in r]
    return [sum(1 for x in xs if x[key]), len(xs)]
c1 = {r: p3count837(r) for r in ('TRUE_KV', 'FORK_KV', 'IRRELEVANT_KV', 'ROTATED_KV', 'TRUE_KV2', 'FORK_KV2', 'IRRELEVANT_KV2')}
C1 = ('INCONCLUSIVE' if c1['TRUE_KV'][1] < 12 else
      'PASS' if c1['TRUE_KV'][0] >= max(c1['FORK_KV'][0], c1['IRRELEVANT_KV'][0], c1['ROTATED_KV'][0]) + 3 else 'FAIL')
C3 = ('INCONCLUSIVE' if c1['TRUE_KV2'][1] < 12 else
      'PASS' if c1['TRUE_KV2'][0] >= max(c1['FORK_KV2'][0], c1['IRRELEVANT_KV2'][0]) + 3 else 'FAIL')
C2 = ('INCONCLUSIVE' if a1[1] < 12 or c1['TRUE_KV'][1] < 12 else
      'PHYSICAL_SUPERIOR' if a1[0] - c1['TRUE_KV'][0] >= 3 else
      'KV_SUPERIOR' if c1['TRUE_KV'][0] - a1[0] >= 3 else 'NO_CLEAR_DIFFERENCE')
order_p3 = [0, 0]
for wa in range(len(worlds829)):
    xs = [r for r in P3EV837 if r['world'] == wa and 'TRUE_KV' in r]
    if len(xs) == 2:
        order_p3[1] += 1; order_p3[0] += xs[0]['TRUE_KV']['top1_gain'] == xs[1]['TRUE_KV']['top1_gain']
# ---- text ----
def tcls837(t, w):
    u = (t or '').upper()
    return [nm for nm, c in (('END', w['end']), ('MIDDLE', w['middle']), ('ALT_END', w['changed_end']), ('FORK_END', w['fork_end']),
                             ('DECOY', w['decoy_end'])) if c in u] + (['UNKNOWN'] if 'UNKNOWN' in u else [])
TXT837 = {}
for (wa, role), t in TEXT837.items():
    cls = tcls837(t, worlds829[wa])
    if role == 'PHYSICAL_PAIR':
        ok = [x for x in cls if x != 'UNKNOWN'] == ['END'] and 'UNKNOWN' not in cls
    elif role.startswith('PHYSICAL_WRONG'):
        ok = cls == ['UNKNOWN']
    else:                                    # bank contains both continuations: END and/or ALT_END, nothing else
        names = [x for x in cls if x != 'UNKNOWN']
        ok = bool(names) and set(names) <= {'END', 'ALT_END'}
    TXT837.setdefault(role, []).append({'world': wa, 'classes': cls, 'ok': ok, 'text': t})
TXTSUM837 = {r: [sum(1 for x in v if x['ok']), len(v)] for r, v in TXT837.items()}
if BUDGET_STOP837:
    decision837 = 'YETERSİZ KANIT'
elif (A1 == 'PASS' and A2 == 'PASS' and A3 == 'PASS') or C1 == 'PASS':
    decision837 = 'DEVAM'
elif A1 == 'FAIL' and C1 == 'FAIL':
    decision837 = 'DUR'
else:
    decision837 = 'YETERSİZ KANIT'
CRIT837 = {'A1_ORACLE_CONDITIONAL_SEARCH': A1, 'A2_END_TO_END': A2, 'A3_WRONG_FIRST': A3, 'A4_ORDER': A4,
           'B_FILLER_NEUTRAL': BF, 'B_CONTEXT_CAUSE': CAUSE837, 'C1_KV_TRANSFER': C1, 'C2_PHYSICAL_VS_KV': C2,
           'C3_PERSISTENCE': C3}
REPORT837 = {
    'Q1_conditional_search': {'ORACLE_top1_valid': a1, 'ORACLE_top3_valid': p1count837('ORACLE', 'top3_valid'),
                              'ORACLE_both_valid_top2': p1count837('ORACLE', 'both_valid_top2'),
                              'MODEL_top1_valid': a2, 'MODEL_top1_valid_with_true_anchor': a2_strict,
                              'MODEL_anchor_roles': {str(r['anchor_role']): sum(1 for x in P1EV837 if x['anchor'] == 'MODEL' and
                                                                                 x['anchor_role'] == r['anchor_role'])
                                                     for r in P1EV837 if r['anchor'] == 'MODEL'},
                              'WRONG_top1_roles': {str(r['top1_role']): sum(1 for x in P1EV837 if x['anchor'] == 'WRONG' and
                                                                             x['top1_role'] == r['top1_role'])
                                                   for r in P1EV837 if r['anchor'] == 'WRONG'},
                              'WRONG_best_rho_below_ORACLE': a3, 'ORACLE_both_orders_worlds': a4,
                              'ORACLE_top1_roles': {str(r['top1_role']): sum(1 for x in P1EV837 if x['anchor'] == 'ORACLE' and
                                                                              x['top1_role'] == r['top1_role'])
                                                    for r in P1EV837 if r['anchor'] == 'ORACLE'},
                              'ORACLE_mean_margins': {k: (float(np.mean([r[k] for r in P1EV837 if r['anchor'] == 'ORACLE' and r[k] is not None]))
                                                          if any(r[k] is not None for r in P1EV837 if r['anchor'] == 'ORACLE') else None)
                                                      for k in ('margin_valid_vs_invalid', 'margin_vs_FORK', 'margin_vs_MIRROR',
                                                                'margin_vs_INBOUND', 'margin_vs_OTHER_WORLD')},
                              'filler_below_second': bfill, 'filler_top1': bfill_top,
                              'cost_pairs_per_anchor': 2 * (len(BANKS837[0]) - 1),
                              'scaling_pairs_per_anchor': {n: 2 * (n - 1) for n in (18, 100, 1000)}},
    'Q2_context_cause': {'cause': CAUSE837, **{m: {'pass_h': p2count837(m), 'common_pass_h': p2count837(m, 'common_pass_h'),
                                                   'pass_state': p2count837(m, 'pass_state'), 'pass_lp': p2count837(m, 'pass_lp'),
                                                   'both_orders_worlds': p2orders837(m)} for m in P2_MODES837},
                         'position_equivalence': D829['position_equivalence837']},
    'Q3_kv_transfer': {'top1_gain_valid': c1, 'top1_mass_valid': {r: p3count837(r, 'top1_mass_valid') for r in c1},
                       'mass_decision_changed_vs_OFF': {r: p3count837(r, 'mass_top1_changed_vs_OFF') for r in c1},
                       'OFF_top1_mass_valid': [sum(1 for r in P3EV837 if r['OFF']['top1_mass_valid']), len(P3EV837)],
                       'mean_gain_margin': {r: (float(np.mean([x[r]['gain_margin_valid_vs_rival'] for x in P3EV837 if r in x]))
                                                if any(r in x for x in P3EV837) else None) for r in c1},
                       'mean_hidden_shift': {r: (float(np.mean([x[r]['hidden_shift_norm'] for x in P3EV837 if r in x]))
                                                 if any(r in x for x in P3EV837) else None) for r in c1},
                       'TRUE_KV_order_same_top1_worlds': order_p3},
    'Q4_physical_vs_kv': {'physical_path_A1': a1, 'kv_path_TRUE_KV': c1['TRUE_KV'], 'verdict': C2, 'answers': TXTSUM837},
    'Q5_attribution': HYP837['classes'],
    'resume': D829['resume837'], 'determinism': D829['determinism837']}
D829['cells837'] = {'P1': P1EV837, 'P2': P2EV837, 'P3': P3EV837, 'text': TXT837}
D829['report837'] = REPORT837
D829['verdict837'] = {'decision': decision837, 'criteria': CRIT837, 'budget_stop': BUDGET_STOP837,
                      'interpretation_guard': ('P1 is a class C external pair search over native measurements; a pass is '
                                               'not model-native addressing. KV and physical pairs are different interventions.')}
D829['claims_ledger837'] = dict(CLAIMS837, demonstrated_by_TEST837={'decision': decision837, 'criteria': CRIT837})
D829['cost837'] = {'counted': dict(COUNT834), 'predicted_upper': POST837, 'measure_seconds': D829['measure_seconds837'],
                   'total_seconds_body': round(time.perf_counter() - T0_837, 3), 'runtime_model_jobs': len(RTJOBS837),
                   'peak_gpu_gib': float(_torch829.cuda.max_memory_allocated()) / 2**30}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f837:
    wr837 = csv.DictWriter(f837, fieldnames=['part', 'world', 'order', 'condition', 'top1', 'valid', 'detail'])
    wr837.writeheader()
    for r in P1EV837:
        wr837.writerow({'part': 'P1', 'world': r['world'], 'order': r['order'], 'condition': r['anchor'] + ':' + str(r['anchor_role']),
                        'top1': r['top1_role'], 'valid': r['top1_valid'], 'detail': json.dumps(r['top5_roles'])})
    for r in P2EV837:
        wr837.writerow({'part': 'P2', 'world': r['world'], 'order': r['order'], 'condition': r['mode'], 'top1': '',
                        'valid': r['pass_h'], 'detail': json.dumps(r['rho_h'])})
    for r in P3EV837:
        for k, v in r.items():
            if isinstance(v, dict):
                wr837.writerow({'part': 'P3', 'world': r['world'], 'order': r['order'], 'condition': k,
                                'top1': v['top1_gain'] if 'top1_gain' in v else '', 'valid': v.get('top1_gain_valid'),
                                'detail': json.dumps({kk: vv for kk, vv in v.items() if kk not in ('top1_gain',)}, default=str)})
D829['status'] = 'COMPLETE_TEST837_EVALUATED' if not BUDGET_STOP837 else 'STOPPED_BUDGET_PARTIAL_EVALUATED'
save829()
log829('TEST837_REPORT', json.dumps(REPORT837, default=str))
log829('TEST837_VERDICT', json.dumps(D829['verdict837'], default=str))
log829('TEST837_COMPLETED', str(OUT829))
'''
BODY_SHA837 = hashlib.sha256(BODY837.encode()).hexdigest()
PANEL_HOOK837 = ("PANEL829['test837'] = {'jobs': JOBS837, 'p3_items': P3ITEMS837, 'physical_pairs': PHYS837, 'banks': BANKS837, "
                 "'fillers': FILL837, 'hypotheses': %r, 'body_sha256': %r, 'helpers_sha256': %r, 'seed': SEED829}\n"
                 % (HYP837, BODY_SHA837, HELPER_SHA837))
src837 = patch837(src837, "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))",
                  PANEL_HOOK837 + "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))")
OFFLINE_HOOK837 = r'''
OFFLINE837 = DIR829 / 'TEST837_offline_key.json'   # never read by any runtime computation
OFFLINE837.write_text(json.dumps({'note': 'OFFLINE ONLY', 'jobs': JOBKEY837, 'p3_states': P3KEY837, 'worlds': worlds829,
                                  'questions': questions829, 'card_meta': card_meta829}, ensure_ascii=False, indent=2), encoding='utf-8')
D829['offline_key837_sha256'] = sha829(OFFLINE837.read_bytes())
'''
src837 = patch837(src837, "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n",
                  "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n" + OFFLINE_HOOK837)
start837 = src837.index("    # RUN ORDER: integrity checks")
start837 = src837.rfind("    # ---", 0, start837)
end837 = src837.index("except BaseException as e:\n    D829['status'] = 'ERROR'", start837)
BODY837_TEXT = BODY837
replacement837 = "\n".join("    " + line if line else "" for line in BODY837.strip("\n").splitlines()) + "\n"
patched837 = src837[:start837] + replacement837 + src837[end837:]
ast.parse(patched837)

# ==================================================================================================================
# CONSOLE / LOGGING LAYER (TEST835 pattern). Nothing below changes what is computed. Every byte the engine prints is
# written unchanged to a full transcript file; the screen shows a compact digest, progress, failures and the summary.
# ==================================================================================================================
import os as _os837, sys as _sys837, io as _io837, traceback as _tb837, datetime as _dt837, shutil as _sh837
from pathlib import Path as _P837
_os837.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')     # download bars only (not data)
for _m837, _f837 in (('huggingface_hub', lambda m: m.utils.disable_progress_bars()),
                     ('transformers', lambda m: m.utils.logging.disable_progress_bar())):
    if _m837 in _sys837.modules:                                    # only if already imported: no new import
        try:
            _f837(_sys837.modules[_m837])
        except Exception:
            pass
_ROOT837 = _P837('/content') if _P837('/content').exists() else _P837('/tmp')
FULL_CONSOLE837 = _ROOT837 / ('TEST837_full_console_' + _dt837.datetime.now(_dt837.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.txt')
CON837 = {'phase': 'SOURCE_VERIFICATION', 'last': [], 'fail_lines': [], 't0': time.time(), 'measure': '0/0', 'p3': 0}
_ORIG_OUT837, _ORIG_ERR837 = _sys837.stdout, _sys837.stderr

def say837(*a):
    _ORIG_OUT837.write(' '.join(str(x) for x in a) + '\n'); _ORIG_OUT837.flush()

def _mins837():
    return round((time.time() - CON837['t0']) / 60.0, 1)

def route837(line):
    s = line.strip()
    if not s:
        return
    CON837['last'] = (CON837['last'] + [s[:300]])[-6:]
    if s.startswith('FAIL '):
        CON837['fail_lines'].append(s[:600]); say837('!! ' + s[:600]); return
    if s.startswith('TEST829_FAILED'):
        CON837['fail_lines'].append(s[:300]); return
    if s.startswith('TEST829_START'):
        parts = s.split()
        say837('Çalışma: %s | panel SHA-256: %s' % (parts[1] if len(parts) > 1 else '?', parts[-1]))
        CON837['phase'] = 'ENGINE_PRELUDE_AND_LOCKS'; return
    if s.startswith('TEST815_GPU_PREFLIGHT'):
        say837('GPU: ' + s[len('TEST815_GPU_PREFLIGHT'):].strip()); return
    if s.startswith('TEST815_GPU_FREE_GIB'):
        say837('GPU boş VRAM (yükleme öncesi): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('TEST837_PREDICTED_COST_BEFORE_MODEL_LOAD'):
        try:
            c = json.loads(s.split(' ', 1)[1]); u = c['numeric_upper']
            say837('Maliyet üst sınırı (model yükleme hariç): %s dk | panel işi %s, mount grubu %s, P3 %s | kartuş %s (dolgu %s) | '
                   'vektör ~%s MB | fusion<=%s probe<=%s' % (c['minutes_upper_excluding_model_load'], c['jobs_panel'], c['mount_groups'],
                   c['p3_items'], c['physical_cartridges'], c['fillers'], c['vector_disk_mb_estimate'], u['fusion_forwards'],
                   u['probe_forwards']))
        except Exception:
            say837(s[:300])
        CON837['phase'] = 'MODEL_LOAD'; say837('Model yükleniyor (Qwen2.5-72B-Instruct, NF4, tek yükleme)...'); return
    if s.startswith('PASS FROZEN_PREFIX'):
        D_ = globals().get('D829', {})
        say837('Model yüklendi (%s s). Fiziksel kartuşlar üretiliyor ve SHA doğrulanıyor...' % D_.get('model_load_seconds', '?'))
        CON837['phase'] = 'PHYSICAL_CARTRIDGE_FORGING'; return
    if s.startswith('PASS PHYSICAL_COUNT'):
        say837('Fiziksel kartuşlar: ' + s.split()[-1] + ' (her biri SHA-256 + tensör SHA ile yeniden yüklendi)')
        CON837['phase'] = 'PREFLIGHT_GATES'; return
    if s.startswith('PASS ARCH_DIMS'):
        say837('Mimari (NL,H,QH,KVH,HD): ' + s[len('PASS ARCH_DIMS'):].strip() + ' | BF16 hesap, NF4, ağırlıklar donmuş'); return
    if s.startswith('PASS VRAM_HEADROOM'):
        say837('Boş VRAM (model sonrası): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('PASS HEADPROBE_EQUALS_LOCKED_ATTENTION_PROBE'):
        say837('Eşdeğerlik kapıları geçti (CUT3/hidden bitwise, HeadProbe farkı ' + s.split()[-1] + ')'); return
    if s.startswith('PASS FILLER_LENGTHS_EQUAL'):
        say837('Nötr dolgu kartları: ' + s.split()[-1] + ' adet, token uzunlukları eşit (model yüklenmeden önce)'); return
    if s.startswith('PASS POSITION_EQUIVALENCE_SUBSTITUTION'):
        say837('Konum eşdeğerliği geçti: dolgu ile n, kart aralıkları ve alt katman K/V satırları bitwise aynı')
        CON837['phase'] = 'MEASUREMENT'; return
    if s.startswith('TEST837_RESUME '):
        try:
            r = json.loads(s.split(' ', 1)[1])
            say837('Devam mekanizması: yeniden kullanılan iş %s, P3 %s | %s' % (r.get('reused_jobs'), r.get('reused_p3'), r.get('reason')))
        except Exception:
            say837(s[:300])
        return
    if s.startswith('TEST837_PROGRESS'):
        p = s.split()
        if len(p) >= 5:
            CON837['phase'] = 'MEASUREMENT %s (%s/%s)' % (p[1], p[2], p[4])
            if p[2] != '0' and (p[1] != 'P3' or p[2] == p[4] or int(p[2]) % 4 == 0):
                say837('  %-11s %s/%s (%s dk)' % (p[1], p[2], p[4], _mins837()))
        return
    if s.startswith('TEST837_BUDGET_STOP'):
        say837('!! ' + s); return
    if s.startswith('TEST837_OFFLINE_START'):
        CON837['phase'] = 'OFFLINE_EVALUATION'
        say837('Ölçüm bitti; çevrimdışı değerlendirme (%s dk)' % _mins837()); return
    if s.startswith('TEST837_COMPLETED'):
        CON837['phase'] = 'COMPLETED'; return

class Console837(_io837.TextIOBase):
    """Writes everything to FULL_CONSOLE837 unchanged; routes complete lines to the compact screen digest."""
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
                route837(line.split('\r')[-1])
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

def sha_path837(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()

def fmt837(x):
    if isinstance(x, list) and len(x) == 2 and all(isinstance(v, (int, float)) for v in x):
        return '%s/%s' % (x[0], x[1])
    if isinstance(x, dict):
        return ', '.join('%s=%s' % (k, fmt837(v)) for k, v in x.items())
    if isinstance(x, float):
        return '%.4g' % x
    if isinstance(x, list):
        return '[' + ', '.join(fmt837(v) for v in x) + ']'
    return str(x)

def files_report837():
    say837('=' * 78); say837('SONUÇ DOSYALARI (SHA-256)')
    d = globals().get('DIR829')
    if d is None or not _P837(d).exists():
        say837('  (çalışma klasörü yok)'); return
    for p in sorted(_P837(d).iterdir()):
        if p.is_file():
            say837('  %s  %d B  %s' % (p, p.stat().st_size, sha_path837(p)))
    vd = _P837(d) / 'TEST837_vectors'
    if vd.exists():
        fs = sorted(x for x in vd.iterdir() if x.is_file())
        say837('  %s/  %d vektör dosyası, %.1f MB (her dosyanın SHA-256 değeri TEST837_vector_manifest.jsonl içinde)'
               % (vd, len(fs), sum(x.stat().st_size for x in fs) / 2**20))

def final837(D):
    R = D['report837']; V = D['verdict837']; K = V['criteria']; C = D['cost837']
    checks = D.get('checks', [])
    q1 = R['Q1_conditional_search']; q2 = R['Q2_context_cause']; q3 = R['Q3_kv_transfer']; q4 = R['Q4_physical_vs_kv']
    say837('=' * 78); say837('TEST837 SONUÇ ÖZETİ (ayrıştırma; P1 araması C sınıfı harici aramadır)'); say837('=' * 78)
    say837('Durum: %s | bütçe durdurması: %s | devam: iş %s, P3 %s' % (D.get('status'), V['budget_stop'],
           R['resume'].get('reused_jobs'), R['resume'].get('reused_p3')))
    say837('Bütünlük: %d kapı, %d başarısız | eşdeğerlik: %s | determinizm: %s' % (len(checks), sum(not c['pass'] for c in checks),
           fmt837(D.get('probe_equivalence837', {})), fmt837(R.get('determinism', {}))))
    say837('-' * 78); say837('[P1] İLK KARTA KOŞULLU İKİNCİ KART ARAMASI (17 aday, TEST831 rho, 12 hücre = 6 dünya x 2 sıra)')
    say837('  ORACLE (gerçek ilk kart): top-1 geçerli %s | top-3 %s | iki geçerli top-2 (çelişki) %s | iki sırada %s'
           % (fmt837(q1['ORACLE_top1_valid']), fmt837(q1['ORACLE_top3_valid']), fmt837(q1['ORACLE_both_valid_top2']),
              fmt837(q1['ORACLE_both_orders_worlds'])))
    say837('    top-1 rolleri: ' + fmt837(q1['ORACLE_top1_roles']))
    say837('    ort. marjlar: ' + fmt837(q1['ORACLE_mean_margins']))
    say837('  MODEL (tek kart etkisiyle seçilen ilk kart): top-1 geçerli %s | gerçek ilk kartla %s | çapa rolleri %s'
           % (fmt837(q1['MODEL_top1_valid']), fmt837(q1['MODEL_top1_valid_with_true_anchor']), fmt837(q1['MODEL_anchor_roles'])))
    say837('  WRONG (fork çapa): en iyi rho ORACLE altında %s | top-1 rolleri %s'
           % (fmt837(q1['WRONG_best_rho_below_ORACLE']), fmt837(q1['WRONG_top1_roles'])))
    say837('  Dolgu kontrolü: rho(ilk, dolgu) < rho(ilk, ikinci) %s | dolgu top-1 %s' % (fmt837(q1['filler_below_second']), q1['filler_top1']))
    say837('  Maliyet: çapa başına %s çift mount; N=18/100/1000 için %s (doğrusal)' % (q1['cost_pairs_per_anchor'],
                                                                                     fmt837(q1['scaling_pairs_per_anchor'])))
    say837('[P2] BAĞLAM KAYBI NEDENİ (bankada rho_TRUE > tüm kontroller; hidden / CUT3 / log-olasılık; iki sıra)')
    for m in ('REMOVE', 'SUBSTITUTE', 'NO_COMPETITION'):
        x = q2[m]
        say837('  %-15s hidden %s (ortak kontrollerle %s) | CUT3 %s | logp %s | iki sırada %s'
               % (m, fmt837(x['pass_h']), fmt837(x['common_pass_h']), fmt837(x['pass_state']), fmt837(x['pass_lp']),
                  fmt837(x['both_orders_worlds'])))
    say837('  Neden (önceden sabit kural): ' + str(q2['cause']))
    say837('[P3] NATIVE KV DURUMU — aynı banka/soru; karar = OFF\'a göre ortalama dikkat kazancında ilk-olmayan top-1')
    for r in ('TRUE_KV', 'FORK_KV', 'IRRELEVANT_KV', 'ROTATED_KV', 'TRUE_KV2', 'FORK_KV2', 'IRRELEVANT_KV2'):
        if r in q3['top1_gain_valid']:
            say837('  %-14s kazanç-top1 geçerli %s | kütle-top1 geçerli %s | kütle kararı OFF\'tan değişti %s | ort. marj %s | hidden kayması %s'
                   % (r, fmt837(q3['top1_gain_valid'][r]), fmt837(q3['top1_mass_valid'][r]), fmt837(q3['mass_decision_changed_vs_OFF'][r]),
                      fmt837(q3['mean_gain_margin'][r]), fmt837(q3['mean_hidden_shift'][r])))
    say837('  OFF kütle-top1 geçerli %s | TRUE_KV iki sırada aynı top-1 %s' % (fmt837(q3['OFF_top1_mass_valid']),
                                                                         fmt837(q3['TRUE_KV_order_same_top1_worlds'])))
    say837('[P3] FİZİKSEL ÇİFT vs KV: fiziksel yol (P1 ORACLE) %s | KV yolu (TRUE_KV) %s | %s'
           % (fmt837(q4['physical_path_A1']), fmt837(q4['kv_path_TRUE_KV']), q4['verdict']))
    say837('  Cevap metni (çevrimdışı) doğru: ' + fmt837(q4['answers']))
    say837('-' * 78); say837('ÖLÇÜTLER')
    for k in K:
        say837('  %-30s %s' % (k, K[k]))
    say837('[Sınıflar] ' + fmt837(R['Q5_attribution']))
    say837('=' * 78)
    say837('NİHAİ BİLİMSEL KARAR: %s' % V['decision'])
    if V['decision'] == 'DEVAM':
        say837('  Gerekçe: koşullu ilişkisel arama (A1+A2+A3) veya native KV aktarımı (C1) önceden sabit ölçütü geçti; TEST838 gerekçelendi. '
               'P1 araması C sınıfıdır, model-native adresleme sayılmaz.')
    elif V['decision'] == 'DUR':
        say837('  Gerekçe: A1 FAIL ve C1 FAIL — ne ilk karta koşullu ilişkisel arama ne native KV aktarımı ikinci kartı güvenilir bulmadı.')
    else:
        say837('  Gerekçe: ' + ('bütçe durdurması' if V['budget_stop'] else
                               'ölçütler ne DEVAM ne DUR kuralını sağladı (bkz. A1/A2/A3/C1 satırları)'))
    say837('Maliyet: sayılan %s | ölçüm %s s | toplam gövde %s s | çalışma zamanı MODEL işi %s | tepe VRAM %.2f GiB'
           % (fmt837(C['counted']), C['measure_seconds'], C['total_seconds_body'], C['runtime_model_jobs'], C['peak_gpu_gib']))

say837('=' * 78)
say837('AKBASCORE TEST837 — ilişkisel arama / bağlam kaybı / aktarım ayrıştırması; Qwen2.5-72B-Instruct (NF4, donmuş), tek A100-80GB')
say837('Kaynak kilitleri: 829.py %s | 834.py %s | 835.py %s | 836.py %s | 836.log %s'
       % (LOCK829_837, LOCK834_837, LOCK835_837, LOCK836_837, LOCK836LOG_837))
say837('Kilitli yardımcılar (AST, %d fonksiyon) SHA-256 %s' % (len(HELPERS837), HELPER_SHA837))
say837('BODY837 SHA-256 %s | yamalı kaynak AST geçti (%d bayt, SHA-256 %s)' % (BODY_SHA837, len(patched837), hashlib.sha256(patched837.encode()).hexdigest()))
say837('Kapsam: %d dünya, 18 kartlık 2 banka | P1 ilk karta koşullu arama (ORACLE/MODEL/WRONG), P2 REMOVE/SUBSTITUTE/NO_COMPETITION, '
       'P3 KV durumu vs fiziksel çift' % WORLDS_EVAL837)
say837('Tam konsol kaydı: ' + str(FULL_CONSOLE837))
say837('=' * 78)
_fh837 = open(FULL_CONSOLE837, 'a', encoding='utf-8', buffering=1)
_fh837.write('TEST837_SOURCE_LOCKS ' + ' '.join((LOCK829_837, LOCK834_837, LOCK835_837, LOCK836_837, LOCK836LOG_837)) +
             '\nTEST837_BODY_SHA256 ' + BODY_SHA837 + '\nTEST837_HELPERS ' + HELPER_SHA837 +
             '\nTEST837_PATCHED_SOURCE_AST_PASS ' + str(len(patched837)) + ' ' + hashlib.sha256(patched837.encode()).hexdigest() + '\n')
import linecache as _lc837
for _nm837, _src837 in (('TEST837_LOCKED_ENGINE', patched837), ('TEST837_LOCKED_HELPERS', HELPER_SRC837)):
    _lc837.cache[_nm837] = (len(_src837), None, [x + '\n' for x in _src837.splitlines()], _nm837)
_sys837.stdout = Console837(_ORIG_OUT837, _fh837); _sys837.stderr = Console837(_ORIG_ERR837, _fh837)
TEST837_ERROR = None
try:
    exec(compile(patched837, 'TEST837_LOCKED_ENGINE', 'exec'), globals())
except BaseException as _e837:
    TEST837_ERROR = _e837
    _tbtext837 = _tb837.format_exc()
    _fh837.write('\n[TEST837 OUTER EXCEPTION]\n' + _tbtext837)
finally:
    _sys837.stdout, _sys837.stderr = _ORIG_OUT837, _ORIG_ERR837
    try:
        _fh837.flush(); _fh837.close()
    except Exception:
        pass
    _dir837 = globals().get('DIR829')
    if _dir837 is not None and _P837(_dir837).exists() and FULL_CONSOLE837.exists():
        _dst837 = _P837(_dir837) / FULL_CONSOLE837.name
        _sh837.move(str(FULL_CONSOLE837), str(_dst837)); FULL_CONSOLE837 = _dst837
if TEST837_ERROR is not None:
    D_ = globals().get('D829', {}) if isinstance(globals().get('D829'), dict) else {}
    bad = [c for c in D_.get('checks', []) if not c.get('pass')]
    say837('=' * 78); say837('TEST837 HATA')
    say837('Tür: %s.%s' % (type(TEST837_ERROR).__module__, type(TEST837_ERROR).__name__))
    say837('Mesaj: ' + repr(TEST837_ERROR)[:800])
    say837('Aşama: ' + CON837['phase'] + ' | geçen %s dk' % _mins837())
    if bad:
        say837('Başarısız kapı: %s | ayrıntı: %s' % (bad[-1].get('name'), str(bad[-1].get('detail'))[:400]))
    say837('Hata öncesi son motor satırları:')
    for x in CON837['last'][-4:]:
        say837('  ' + x[:240])
    tbl = _tbtext837.rstrip().splitlines()
    say837('Traceback (son %d satır; tamamı dosyada ve results.json içinde):' % min(40, len(tbl)))
    for x in tbl[-40:]:
        say837('  ' + x)
    files_report837()
    say837('Tam konsol kaydı: %s  SHA-256 %s' % (FULL_CONSOLE837, sha_path837(FULL_CONSOLE837) if FULL_CONSOLE837.exists() else '-'))
    say837('Not: tamamlanan ölçümler vektör dosyalarında; hücre yeniden çalıştırılırsa SHA doğrulanıp yeniden kullanılır.')
    raise SystemExit('TEST837_FAILED: ' + type(TEST837_ERROR).__name__)
try:
    final837(D829)
except Exception as _e837s:
    say837('!! Özet basılamadı (veri dosyalarda tam): ' + repr(_e837s))
    say837(_tb837.format_exc()[-1500:])
files_report837()
say837('=' * 78)
