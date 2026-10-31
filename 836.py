# AKBASCORE SILICON HIPPOCAMPUS — TEST836, single Colab cell (one A100-SXM4-80GB, frozen Qwen2.5-72B-Instruct NF4).
# TRANSFER AUDIT: WHERE DOES THE MEASURED RELATIONAL SIGNAL (TEST831) GET LOST ON THE WAY TO NATIVE CONTROL?
#
# No controller, no threshold, no calibration: every criterion is a parameter-free ordering of native numbers.
#   P1  POSITIVE CONTROL (TEST831 replication, fresh seed): rho = ||z_ab - z_a - z_b + z_0|| / ||z_b - z_0|| on isolated
#       physical mounts (NULL, A, B, A+B), final-norm hidden / CUT3 / full-vocab log-prob, both cartridge orders.
#   P2  CONTEXT: the same rho with the pair embedded in the full physical bank (z_0 = bank-A-B, z_a = bank-B,
#       z_b = bank-A, z_ab = bank), both bank orders -> does bank widening (TEST832's open bank) erase the signal?
#   P3  TRANSFER: TEST833 native KV state after reading [true first] vs [fork] vs [irrelevant card] vs rotated, fed into
#       a forward over the full bank; the SAME 80x64 heads and the SAME hidden readout for every state (no head selection).
#   P4  TEST832 DECOMPOSITION (offline, from P1/P2 numbers): first-candidate ranking, relevance cut, closure given the
#       true first, mutual-best column check, conflict (two valid closures); each step scored with oracle inputs.
# Locked parts: TEST829 source (blob a5a25460, wraps the TEST815 engine), 10 GPU-verified TEST834 helpers (AST from
# 834.py blob ab7b2046), bank_forward835 (AST from 835.py blob 9327cebc), TEST835 compact console pattern.
# Text never enters the runtime; no answer text is produced by TEST836. No GPU execution or result is claimed by the
# code author.
import urllib.request, hashlib, ast, json, time, random, math, re, numpy as np

REPO836 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
LOCK829_836 = "a5a25460a3a6bbdf62a0571a9b5ff19e64159cf7"
LOCK834_836 = "ab7b2046d7b7e7be18aed8c6ce5a1397e0c991d7"
LOCK835_836 = "9327cebc651f173fd547362825679a1a790fcd6b"
LOCK831LOG_836 = "a24686a075237ff2311c7038b3e81394eead6426"   # prior evidence (read-only)
LOCK835LOG_836 = "bfad088c81666674b766c3de95f08e0ab00f4817"   # prior evidence (read-only)
SEED836 = 8362026
EXPECTED_ARCH834 = (80, 8192, 64, 8, 128)
DEVICE_KIND836 = 'cuda'
WORLDS_EVAL836 = 6
BLOCK836 = 3
KINDS836 = ('first', 'second', 'changed', 'mirror', 'decoy', 'fork')      # 6 cards per world -> 18-card banks
P2_ROLES836 = ('TRUE', 'ALT', 'MIRROR', 'INBOUND', 'FORK', 'MISMATCHED_IN_BANK')
SPACES836 = ('h', 'state', 'lp')
SEC_FUSION836, SEC_PROBE836 = 0.6, 0.9
PRED_LIMIT_MIN836 = 240.0
HARD_BUDGET_MIN836 = 300.0
RESUME836 = True

def fetch836(name, lock, limit=400000):
    with urllib.request.urlopen(urllib.request.Request(REPO836 + name, headers={"User-Agent": "AKBASCORE-TEST836"}),
                                timeout=180) as f:
        raw = f.read(limit + 1)
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert len(raw) <= limit and blob == lock, ("STOP_SOURCE_CHANGED", name, blob)
    return raw

raw829_836 = fetch836("829.py", LOCK829_836)
raw834_836 = fetch836("834.py", LOCK834_836)
raw835_836 = fetch836("835.py", LOCK835_836)
raw831log_836 = fetch836("831.log", LOCK831LOG_836)
raw835log_836 = fetch836("835.log", LOCK835LOG_836)
src836 = raw829_836.decode("utf-8")

def extract836(raw, body_name, names):
    tree = ast.parse(raw.decode("utf-8"))
    bodies = [n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == body_name]
    assert len(bodies) == 1, ('BODY_NOT_UNIQUE', body_name)
    text = bodies[0].value.value
    nodes = [n for n in ast.parse(text).body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert sorted(n.name for n in nodes) == sorted(names), ('HELPER_SET_MISMATCH', body_name)
    return "\n\n".join(ast.get_source_segment(text, n) for n in nodes)
HELPERS834_836 = ('HeadProbe834', 'concat834', 'rprobe834', 'relocate834', 'rotate834', 'seal834', 'mount834', 'cspans834',
                  'card_mass834', 's0_834')
HELPERS835_836 = ('bank_forward835',)
HELPER_SRC836 = extract836(raw834_836, 'BODY834', HELPERS834_836) + "\n\n" + extract836(raw835_836, 'BODY835', HELPERS835_836)
HELPER_SHA836 = hashlib.sha256(HELPER_SRC836.encode()).hexdigest()
HELPERS836 = HELPERS834_836 + HELPERS835_836

def patch836(text, old, new):
    assert text.count(old) == 1, ("PATCH_ANCHOR_NOT_UNIQUE", old[:80], text.count(old))
    return text.replace(old, new, 1)

src836 = patch836(src836, "SEED829 = 8292026", "SEED829 = %d" % SEED836)
src836 = patch836(src836, "RUN829 = 'TEST829_'", "RUN829 = 'TEST836_'")
src836 = patch836(src836, "WORLDS829 = 3                    # small pilot (directive); no automatic extension",
                  "WORLDS829 = %d                    # TEST836 sealed worlds" % WORLDS_EVAL836)
for a836, b836 in (("'TEST829_results.json'", "'TEST836_results.json'"), ("'TEST829.log'", "'TEST836.log'"),
                   ("'TEST829_blind_review.csv'", "'TEST836_case_table.csv'"),
                   ("'TEST829_offline_key.json'", "'TEST829_base_offline_key.json'")):
    src836 = patch836(src836, a836, b836)

PANEL_EXT836 = r'''
# ---------------- TEST836 PANEL EXTENSION (sealed before any model call) ----------------
def fresh836():
    while True:
        c = code829()
        if c not in seen829:
            seen829.add(c); return c
for w in worlds829:
    w['fork_end'] = fresh836()
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
_rng836 = random.Random(SEED829 + 36)
QID836 = [questions829[i]['qid'] for i in range(len(worlds829))]
assert len(questions829) == len(worlds829), 'ONE_QUESTION_PER_WORLD'
BANKS836 = []
for bi in range(0, len(worlds829), BLOCK836):
    b_ = [worlds829[i]['ids'][k] for i in range(bi, bi + BLOCK836) for k in KINDS836]
    _rng836.shuffle(b_)
    BANKS836.append(b_)
def block836(wi):
    return wi // BLOCK836
JOBS836, JOBKEY836, CASES836, CASEKEY836 = [], {}, [], {}
_jobidx836 = {}
def job836(ids, qid, phase, role):
    k = (tuple(ids), qid)
    if k not in _jobidx836:
        j = 'J836_' + ''.join(_rng836.choice('0123456789ABCDEF') for _ in range(12))
        _jobidx836[k] = j
        JOBS836.append({'job': j, 'mount': list(ids), 'qid': qid, 'phase': phase})
        JOBKEY836[j] = role
    return _jobidx836[k]
def case836(phase, null, a, b, ab, key):
    c = 'C836_' + ''.join(_rng836.choice('0123456789ABCDEF') for _ in range(12))
    CASES836.append({'case': c, 'phase': phase, 'null': null, 'a': a, 'b': b, 'ab': ab})
    CASEKEY836[c] = key
for wa, w in enumerate(worlds829):
    q = QID836[wa]; a = w['ids']['first']
    jn = job836([NULL829], q, 'P1', {'world': wa, 'kind': 'NULL'})
    ja = job836([a], q, 'P1', {'world': wa, 'kind': 'SINGLE', 'card': a})
    blist = [('TRUE', wa, w['ids']['second']), ('ALT', wa, w['ids']['changed']), ('MIRROR', wa, w['ids']['mirror']),
             ('INBOUND', wa, w['ids']['decoy']), ('FORK', wa, w['ids']['fork'])]
    blist += [('MISMATCHED', wb, worlds829[wb]['ids']['second']) for wb in range(len(worlds829)) if wb != wa]
    for role, wb, b in blist:
        jb = job836([b], q, 'P1', {'world': wa, 'kind': 'SINGLE', 'card': b})
        for order, ids in (('FORWARD', [a, b]), ('REVERSE', [b, a])):
            jab = job836(ids, q, 'P1', {'world': wa, 'kind': 'PAIR', 'b_role': role, 'b_world': wb, 'order': order})
            case836('P1', jn, ja, jb, jab, {'world': wa, 'b_role': role, 'b_world': wb, 'order': order})
    for c in BANKS836[block836(wa)]:                                    # singles for the TEST832 first-candidate step
        job836([c], q, 'P1', {'world': wa, 'kind': 'SINGLE', 'card': c})
    nxt = worlds829[block836(wa) * BLOCK836 + (wa + 1) % BLOCK836]['ids']['second']
    p2 = [('TRUE', w['ids']['second']), ('ALT', w['ids']['changed']), ('MIRROR', w['ids']['mirror']),
          ('INBOUND', w['ids']['decoy']), ('FORK', w['ids']['fork']), ('MISMATCHED_IN_BANK', nxt)]
    for order in ('FORWARD', 'REVERSE'):
        base = list(BANKS836[block836(wa)]) if order == 'FORWARD' else list(reversed(BANKS836[block836(wa)]))
        jab = job836(base, q, 'P2', {'world': wa, 'kind': 'BANK_FULL', 'order': order})
        jb = job836([c for c in base if c != a], q, 'P2', {'world': wa, 'kind': 'BANK_MINUS_A', 'order': order})
        for role, b in p2:
            ja2 = job836([c for c in base if c != b], q, 'P2', {'world': wa, 'kind': 'BANK_MINUS_B', 'b_role': role, 'order': order})
            j0 = job836([c for c in base if c not in (a, b)], q, 'P2', {'world': wa, 'kind': 'BANK_MINUS_AB', 'b_role': role, 'order': order})
            # roles in the TEST831 formula: a = anchor (first) present, b = candidate present
            case836('P2', j0, ja2, jb, jab, {'world': wa, 'b_role': role, 'order': order})
# P3: native KV state after reading a designed card set, fed into a forward over the full bank (FORWARD order).
P3ITEMS836, P3KEY836 = [], {}
for wa, w in enumerate(worlds829):
    irr = worlds829[(wa + BLOCK836) % len(worlds829)]['ids']['second']          # card of the other bank
    specs = [('FIRST', [w['ids']['first']], False), ('FIRST_ROTATED', [w['ids']['first']], True),
             ('FORK_FIRST', [w['ids']['fork']], False), ('IRRELEVANT', [irr], False),
             ('COMPLETE_PAIR', [w['ids']['first'], w['ids']['second']], False)]
    states = []
    for role, cards, rot in specs:
        sid = 'S836_' + ''.join(_rng836.choice('0123456789ABCDEF') for _ in range(12))
        states.append({'sid': sid, 'cards': cards, 'rotate': rot}); P3KEY836[sid] = role
    _rng836.shuffle(states)
    P3ITEMS836.append({'qid': QID836[wa], 'bank': list(BANKS836[block836(wa)]), 'states': states})
_rng836.shuffle(JOBS836); _rng836.shuffle(CASES836)
GROUPS836, GROUP_ORDER836 = {}, []
for j in JOBS836:                                   # mount groups in the sealed shuffled order of first appearance
    m = tuple(j['mount'])
    if m not in GROUPS836:
        GROUPS836[m] = []; GROUP_ORDER836.append(m)
    GROUPS836[m].append(j['job'])
JOBREC836 = {j['job']: j for j in JOBS836}

def fus_upper836(k, maxb, p_):
    if k <= 0:
        return 0
    c = int(globals().get('CHUNK', 128))
    return (p_ + maxb + c - 1) // c + (k - 1) * ((maxb + c - 1) // c)

def cost_upper836(tok_of, p_):
    mx = max(tok_of[c] for c in cards829)
    up = {'fusion_forwards': 0, 'probe_forwards': 0, 'capture_forwards': 0, 'rank_forwards': 0, 'generation_forwards': 0}
    up['fusion_forwards'] += fus_upper836(1, tok_of[NULL829], p_) + fus_upper836(2, mx, p_) + fus_upper836(1, tok_of[NULL829], p_)
    up['probe_forwards'] += len(QID836) + 2 + 3 + 1; up['generation_forwards'] += 1           # S_null, equivalence, nonint., replay
    up['fusion_forwards'] += fus_upper836(len(JOBS836[0]['mount']), mx, p_)                     # determinism replay
    for m, js in GROUPS836.items():
        up['fusion_forwards'] += fus_upper836(len(m), mx, p_); up['probe_forwards'] += len(js)
    for it in P3ITEMS836:
        up['fusion_forwards'] += fus_upper836(len(it['bank']), mx, p_)
        for s in it['states']:
            up['fusion_forwards'] += fus_upper836(len(s['cards']), mx, p_); up['probe_forwards'] += 2
        up['probe_forwards'] += 1
    sec = up['fusion_forwards'] * SEC_FUSION836 + up['probe_forwards'] * SEC_PROBE836 + 120.0 + len(cards829) * 2.0
    maxmem = max(p_ + sum(tok_of[c] for c in m) for m in GROUPS836)
    return {'numeric_upper': up, 'jobs': len(JOBS836), 'mount_groups': len(GROUPS836), 'cases': len(CASES836),
            'p3_items': len(P3ITEMS836), 'physical_cartridges': len(cards829),
            'cartridge_disk_mb_estimate': round(sum((p_ + tok_of[c]) * (8192 * 2 + 4 * 2 * 8 * 128 * 2) for c in cards829) / 2**20, 1),
            'vector_disk_mb_estimate': round(len(JOBS836) * (8192 * 8 * 2 + 152064 * 8) / 2**20, 1),
            'max_memory_tokens': maxmem, 'minutes_upper_excluding_model_load': round(sec / 60.0, 1),
            'peak_vram_gib_expected': 'about 39-41 (TEST835 measured 39.86 GiB peak)',
            'model_weights': 'loaded once; download/cache time not estimated'}
'''
src836 = patch836(src836,
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n",
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n" + PANEL_EXT836)
PRECOST836 = r'''
    PRE836 = cost_upper836(tok_counts829, 30)
    D829['predicted_cost836_pre_model'] = PRE836
    log829('TEST836_PREDICTED_COST_BEFORE_MODEL_LOAD', json.dumps(PRE836))
    gate829('TEST836_PREDICTED_BUDGET', PRE836['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN836,
            {'minutes_upper': PRE836['minutes_upper_excluding_model_load'], 'limit': PRED_LIMIT_MIN836})
'''
src836 = patch836(src836, "    del tok829\n", "    del tok829\n" + PRECOST836)

HYP836 = {
    'question': ('Where is the TEST831 relational-completion signal lost on the way to native control: is it not '
                 'reproducible, erased by the open bank, or not carried by the native KV state into the next computation?'),
    'rho': 'rho = ||z_ab - z_a - z_b + z_0|| / ||z_b - z_0|| (TEST831 feats831, unchanged).',
    'criteria': {
        'T1_POSITIVE_CONTROL': ('isolated mounts, final-norm hidden: rho_TRUE exceeds every row control (5 mismatched second '
                                'links, mirror, inbound, fork) and every column control (the same true b with the other 5 '
                                'anchors) in >= 10 of 12 (world, order) cells. CUT3 and log-prob are reported, not required.'),
        'T2_BANK_CONTEXT': ('pair embedded in the full 18-card bank, final-norm hidden: rho_TRUE exceeds mirror, inbound, fork '
                            'and the in-bank mismatched second link in >= 10 of 12 (world, order) cells.'),
        'T3_ORDER': 'both orders pass in >= 5 of 6 worlds, isolated (T1 cells) and in the bank (T2 cells).',
        'T4_ALT_VALID_CHAIN': ('rho_ALT (valid alternative continuation) exceeds the same row controls in >= 10 of 12 cells '
                               '(isolated): precondition for recognising two closures = conflict.'),
        'T5_NATIVE_TRANSFER': ('over the full bank, the number of heads (of 80 x 64) whose attention gain on the true second '
                               'card (vs the S_null forward) is positive and larger than on every non-chain card is larger '
                               'after reading [true first] than after reading the rotated state, [fork] and [irrelevant card], '
                               'in >= 5 of 6 worlds. Same heads, same readout for every state.')},
    'decision': ('DUR if T1 fails (signal not reproducible). DEVAM if T1, T2 and T5 pass. Otherwise YETERSİZ KANIT with the '
                 'loss locus: CONTEXT (T2 fails), TRANSFER (T5 fails), or both. A budget stop forces YETERSİZ KANIT.'),
    'p4_decomposition': ('offline, oracle inputs per step: (1) first candidate = largest single-card hidden distance to NULL '
                         'over the bank; (2) largest-log-gap relevance cut contains the first link; (3) closure: argmax_b '
                         'rho(first, b) is the second or alternative (isolated row, and bank context); (4) mutual best: '
                         'first is the argmax anchor for that b (column); (5) conflict: both TRUE and ALT exceed all '
                         'non-composing controls. The first step below 10/12 (or 5/6) is the loss step.'),
    'not_claimed': ['autonomous selection', 'autonomous stopping', 'that rho is evidence sufficiency',
                    'that a Python threshold on rho is model-native control']}

CLAIMS836 = {
    'verified_from_prior_research': [
        '831.log (blob a24686a0): TEST831_PRIMARY H1_SUPPORTED_IN_DESIGNED_PILOT 12/12 on final-norm hidden; CUT3 and '
        'log-prob rho did not separate (retrospective audit: 0/12 each).',
        '832: the same rho inside an external selection policy reached 4/12 correct terminal states.',
        '833.log: native 80-layer KV recurrence works (trajectories differ 24/24) but terminal 4/24 vs 4/24.',
        '835.log (blob bfad088c): all gates passed; K1-K9 FAIL; first head 14/30, order reversal same first 10/36; '
        'FEEDBACK and NEG_CONTROL shared head L62/H49 and gave identical totals; OFF used another head (confound); '
        'oracle NEG_CONTROL was not computed and is NOT a 0/16 measurement.'],
    'implemented_in_TEST836': [
        'TEST831 rho on a fresh seed with an 18-card bank design (P1), the same rho inside the bank (P2).',
        'Head-agnostic transfer measurement of the TEST833 KV state over all 80 x 64 heads (P3), with rotated, fork and '
        'irrelevant-state controls; no head is selected.',
        'Offline decomposition of the TEST832 policy steps (P4).',
        'Per-job SHA-256-verified vector files and job-level resume; TEST835 compact console.'],
    'demonstrated_by_TEST836': 'filled only from this run'}

BODY836 = r'''
D829['test'] = '836'
D829['controller'] = 'NONE_TRANSFER_AUDIT_PARAMETER_FREE_ORDERINGS'
D829['sources836'] = {'829': LOCK829_836, '834': LOCK834_836, '835': LOCK835_836, '831_log': LOCK831LOG_836,
                      '835_log': LOCK835LOG_836, 'helpers_sha256': HELPER_SHA836, 'helpers': list(HELPERS836)}
D829['hypotheses836'] = PANEL829['test836']['hypotheses']
D829['limitations'] = [
    'Designed pairs and designed states: a positive result is not autonomous selection, stopping or control.',
    'rho is computed in Python from native states; it is a measurement, not a model decision.',
    'Six sealed worlds, one template, one model; 12 (world, order) cells are not 12 independent worlds.',
    'Bank-context rho uses physical removal (bank minus cards), not masking; positions of the remaining cards shift.',
    'P3 states are designed (true first, fork, irrelevant, rotated); the bank always contains the true first and second.',
    'No answer text is produced; the question tokens are the only boundary input.',
    'No GPU execution or result is claimed by the code author.']
gate829('PANEL_FRESH_SEED', SEED829 == SEED836, SEED829)
gate829('NO_CONTROL_TEXT', MAX_NEW_CONTROL829 == 0)
gate829('WORLD_COUNT', len(worlds829) == WORLDS_EVAL836 and len(QID836) == WORLDS_EVAL836)
gate829('JOBS_UNIQUE', len({(tuple(j['mount']), j['qid']) for j in JOBS836}) == len(JOBS836), len(JOBS836))
gate829('CASE_COUNT', len(CASES836) == WORLDS_EVAL836 * (10 * 2 + len(P2_ROLES836) * 2), len(CASES836))
gate829('CARTRIDGES_PHYSICAL', all(c in entries for j in JOBS836 for c in j['mount']) and
        all(c in entries for it in P3ITEMS836 for s in it['states'] for c in s['cards'] + it['bank']))
def copy_receivers836(src):
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'copy':
            r = n.func.value
            out.append(isinstance(r, ast.Call) and isinstance(r.func, ast.Attribute) and r.func.attr == 'numpy')
    return out
cr836 = copy_receivers836(HELPER_SRC836) + copy_receivers836(BODY836_TEXT)
gate829('STATIC_COPY_RECEIVERS_ARE_NDARRAY', all(cr836), {'copy_calls': len(cr836)})
exec(compile(HELPER_SRC836, 'TEST836_LOCKED_HELPERS', 'exec'), globals())
gate829('HELPERS_LOADED', all(callable(globals().get(x)) for x in HELPERS836), HELPER_SHA836)
gate829('ENGINE_SYMBOLS836', all(callable(globals().get(x)) for x in
        ('cache_build', 'pairs', 'rephase', 'Cut3Diagnostic', 'AttentionIntervention', 'prompt_ids', 'build_fusion',
         'memory_seals', 'compare_seals', 'observe_state', 'kv_digest', 'safe_load', 'cosdist829', 'full_readout829')))
gate829('ARCH_DIMS', (NL, H, QH, KVH, HD) == EXPECTED_ARCH834 and int(model.config.num_attention_heads) == QH and
        int(model.config.num_key_value_heads) == KVH and int(model.config.hidden_size) == H, (NL, H, QH, KVH, HD))
gate829('BF16_COMPUTE', DTYPE == _torch829.bfloat16, str(DTYPE))
gate829('NF4_LINEAR4BIT', any(isinstance(m_, bitsandbytes.nn.Linear4bit) for m_ in model.modules()))
gate829('WEIGHTS_FROZEN', all(not p_.requires_grad for p_ in model.parameters()))
gate829('DEVICE', str(DEV).startswith(DEVICE_KIND836), str(DEV))
gate829('ROPE_MODULE', callable(getattr(model.model, 'rotary_emb', None)))
gate829('SDPA_MODULE', F is _torch829.nn.functional and F.scaled_dot_product_attention is SDPA829)
gate829('PREFIX_P', P == 30, P)
gate829('PRIOR_LOGS_PRESENT', b'TEST831_PRIMARY' in raw831log_836 and 'K1_FIRST_ADDRESS'.encode() in raw835log_836)
POST836 = cost_upper836({c: int(entries[c]['body_tokens']) for c in cards829}, P)
D829['predicted_cost836'] = POST836
log829('TEST836_PREDICTED_COST', json.dumps(POST836))
gate829('PREDICTED_BUDGET_POST_LOAD', POST836['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN836,
        POST836['minutes_upper_excluding_model_load'])
QTEXT836 = {q['qid']: q['question'] for q in questions829}
LQ834 = {qid: list(prompt_ids(t)) for qid, t in QTEXT836.items()}
gate829('FUSION_TOKENS_WITH_STATE', POST836['max_memory_tokens'] + 2 * max(len(v) for v in LQ834.values()) + 64 <= MAX_FUSED_TOKENS,
        POST836['max_memory_tokens'])
try:
    free836, _ = _torch829.cuda.mem_get_info()
    gate829('VRAM_HEADROOM', free836 / 2**30 >= 8.0, round(free836 / 2**30, 2))
except Exception as e836:
    gate829('VRAM_HEADROOM', False, repr(e836))
D829['noninterference836'] = noninterference829([NULL829], questions829[0]['question'])
for k836, v836 in D829['noninterference836'].items():
    gate829('NONINTERFERENCE_' + k836.upper(), bool(v836), v836)
COUNT834 = {'fusion_forwards': fusion_forwards829([NULL829]), 'probe_forwards': 3, 'capture_forwards': 0,
            'rank_forwards': 0, 'generation_forwards': 1, 'mounts': 1}
T0_836 = time.perf_counter()
SEAL_LAYERS834 = (0, CUT, NL // 2, NL - 1)
rs836 = np.random.default_rng(SEED836 + 33)
ROT834 = []
for l836 in range(NL):
    mats836 = []
    for j836 in range(KVH):
        qm836, rm836 = np.linalg.qr(rs836.standard_normal((HD, HD)))
        mats836.append(qm836 * np.sign(np.diag(rm836))[None, :])
    ROT834.append(torch.tensor(np.stack(mats836).astype(np.float32), device=DEV))

# ---- S_null per question (TEST833 state, needed by P3) ----
memN836, nN836 = mount834([NULL829], 'NULL')
sealN836 = seal834(memN836)
SNULL834 = {}
for qid836 in QTEXT836:
    pN = rprobe834(memN836, None, LQ834[qid836])
    SNULL834[qid836] = {'S': [(k.clone(), v.clone()) for k, v in pN['S_raw']], 'pos': pN['start'], 'h': pN['h'],
                        'state': pN['state']}
    del pN
gate829('KV_SEAL_NULL_AFTER_PROBES', seal834(memN836) == sealN836)
del memN836; gc.collect(); release()

# ---- equivalence: rprobe834 without state == locked observe_state (the TEST831 measure829 path) ----
jE836 = next(j for j in JOBS836 if len(j['mount']) == 2)
memE836, nE836 = mount834(jE836['mount'], 'EQUIV')
b0E836 = int(entries[jE836['mount'][0]]['body_tokens'])
spE836 = {'B0': (P, P + b0E836), 'B1': (P + b0E836, nE836)}
with Readout829() as roE836:
    stE836, attE836 = observe_state(memE836, QTEXT836[jE836['qid']], spE836)
COUNT834['probe_forwards'] += 1
pE836 = rprobe834(memE836, None, LQ834[jE836['qid']])
hpm836 = max(abs(float(pE836['rows'][l][:, spE836[s][0]:spE836[s][1]].sum(-1).mean()) - float(attE836[str(l)][s + '_mass']))
             for l in (4, 20, 40, 79) for s in ('B0', 'B1'))
D829['probe_equivalence836'] = {
    'cut3_state_bitwise': bool(np.array_equal(stE836.float().cpu().numpy().astype(np.float64), pE836['state'])),
    'final_hidden_bitwise': bool(np.array_equal(roE836.h.reshape(-1).double().cpu().numpy(), pE836['h'])),
    'headprobe_mass_max_abs_vs_locked_probe': hpm836}
gate829('PROBE_EQUALS_OBSERVE_STATE_CUT3', D829['probe_equivalence836']['cut3_state_bitwise'])
gate829('PROBE_EQUALS_OBSERVE_STATE_HIDDEN', D829['probe_equivalence836']['final_hidden_bitwise'])
gate829('HEADPROBE_EQUALS_LOCKED_ATTENTION_PROBE', hpm836 <= 2e-6, hpm836)
del memE836, pE836, stE836; gc.collect(); release()

# ---- per-job vector store on disk (SHA-256 manifest; job-level resume) ----
VDIR836 = DIR829 / 'TEST836_vectors'
VDIR836.mkdir(exist_ok=True)
MAN836 = DIR829 / 'TEST836_vector_manifest.jsonl'
HEADER836 = {'panel_sha256': PANEL_SHA829, 'body_sha256': PANEL829['test836']['body_sha256'], 'helpers_sha256': HELPER_SHA836}
VEC836 = {}
D829['resume836'] = {'enabled': RESUME836, 'source': None, 'reused_jobs': 0, 'reused_p3': 0, 'reason': None}
def load_npz836(path):
    with np.load(path, allow_pickle=False) as z:
        return {k: np.array(z[k], copy=True) for k in z.files}
RESUMED_P3_836 = {}
if RESUME836:
    for cand in sorted(DIR829.parent.glob('TEST836_*/TEST836_vector_manifest.jsonl'), reverse=True):
        if cand.parent == DIR829:
            continue
        try:
            lines = cand.read_text(encoding='utf-8').splitlines()
            if not lines or json.loads(lines[0]).get('header') != HEADER836:
                D829['resume836']['reason'] = 'header mismatch in ' + str(cand); continue
            got, got3 = {}, {}
            for ln in lines[1:]:
                o = json.loads(ln); f = cand.parent / 'TEST836_vectors' / o['file']
                if not f.exists() or sha_file(f) != o['sha256']:
                    continue
                if o['kind'] == 'job':
                    got[o['key']] = load_npz836(f)
                else:
                    got3[o['key']] = load_npz836(f)
            VEC836.update(got); RESUMED_P3_836.update(got3)
            D829['resume836'].update({'source': str(cand), 'reused_jobs': len(got), 'reused_p3': len(got3),
                                      'reason': 'header and per-file SHA-256 verified'})
            break
        except Exception as e836r:
            D829['resume836']['reason'] = 'unreadable ' + str(cand) + ' ' + repr(e836r)
log829('TEST836_RESUME', json.dumps(D829['resume836']))
with MAN836.open('w', encoding='utf-8') as fh836:
    fh836.write(json.dumps({'header': HEADER836}, sort_keys=True) + '\n')
def save_vec836(kind, key, arrays):
    f = VDIR836 / (key + '.npz')
    np.savez(f, **arrays)
    with MAN836.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps({'kind': kind, 'key': key, 'file': f.name, 'sha256': sha_file(f)}, sort_keys=True) + '\n')
for k836 in list(VEC836):                     # carry verified resumed vectors into this run's manifest
    save_vec836('job', k836, VEC836[k836])
for k836 in list(RESUMED_P3_836):
    save_vec836('p3', k836, RESUMED_P3_836[k836])

# ==================================================================================================================
# MEASUREMENT RUNTIME (sealed panel; opaque job IDs only). Until the OFFLINE PHASE no role or label is read.
# ==================================================================================================================
BUDGET_STOP836 = False
t_meas836 = time.perf_counter()
NG836 = len(GROUP_ORDER836); done836 = 0
for gi836, m836 in enumerate(GROUP_ORDER836):
    todo = [jj for jj in GROUPS836[m836] if jj not in VEC836]
    done836 += 1
    if todo:
        if (time.perf_counter() - T0_836) / 60.0 > HARD_BUDGET_MIN836:
            BUDGET_STOP836 = True
            log829('TEST836_BUDGET_STOP', 'mount_groups_done', gi836, 'of', NG836); break
        memx, n = mount834(list(m836), 'G%d' % gi836)
        seal = seal834(memx)
        for jj in todo:
            jrec = JOBREC836[jj]
            p = rprobe834(memx, None, LQ834[jrec['qid']], keep_lp=True)
            lp = p['lp'].detach().to(device='cpu', dtype=_torch829.float64).numpy()
            arr = {'h': np.asarray(p['h'], dtype=np.float64), 'state': np.asarray(p['state'], dtype=np.float64),
                   'lp': np.asarray(lp, dtype=np.float64), 'entropy': np.asarray([p['summary']['entropy_nats']])}
            VEC836[jj] = arr; save_vec836('job', jj, arr)
            del p, lp
        gate829('MEAS_KV_SEAL_G%d' % gi836, seal834(memx) == seal)
        del memx; gc.collect(); release()
    if done836 % max(1, NG836 // 8) == 0 or done836 == NG836:
        log829('TEST836_MEASURE_PROGRESS', done836, '/', NG836, 'jobs', len(VEC836), '/', len(JOBS836))
D829['measure_seconds836'] = round(time.perf_counter() - t_meas836, 3)
# determinism replay of the first job (bitwise)
jR836 = JOBS836[0]
memR836, nR836 = mount834(jR836['mount'], 'REPLAY')
pR836 = rprobe834(memR836, None, LQ834[jR836['qid']])
D829['determinism836'] = {'hidden_bitwise': bool(np.array_equal(pR836['h'], VEC836[jR836['job']]['h'])) if jR836['job'] in VEC836 else None,
                          'cut3_bitwise': bool(np.array_equal(pR836['state'], VEC836[jR836['job']]['state'])) if jR836['job'] in VEC836 else None}
gate829('DETERMINISM_REPLAY', BUDGET_STOP836 or (D829['determinism836']['hidden_bitwise'] and D829['determinism836']['cut3_bitwise']),
        D829['determinism836'])
del memR836, pR836; gc.collect(); release()

# ---- P3: native state transfer over the full bank (all heads, all states, identical readout) ----
def state_after836(cards, qid, n_target, cache):
    """KV rows the frozen model writes for the question after reading physical `cards` (S_null state; TEST835
    state_after835 generalised to a card list), relocated to canonical positions after n_target memory tokens."""
    key = (qid, tuple(cards))
    if key not in cache:
        memx, n = mount834(list(cards), 'S_' + str(len(cache)))
        seal = seal834(memx)
        p = rprobe834(memx, s0_834(qid, n), LQ834[qid])
        gate829('MEAS_KV_SEAL_STATE_' + str(len(cache)), seal834(memx) == seal)
        cache[key] = {'S': [(k.clone(), v.clone()) for k, v in p['S_raw']], 'pos': p['start'], 'h': p['h']}
        del memx, p; gc.collect(); release()
    c = cache[key]
    return relocate834(c['S'], c['pos'], n_target, len(LQ834[qid]))
P3RES836 = dict(RESUMED_P3_836)
for ii836, it in enumerate(P3ITEMS836):
    key0 = 'P3_%d_OFF' % ii836
    need = [key0] + ['P3_%d_%s' % (ii836, s['sid']) for s in it['states']]
    if all(k in P3RES836 for k in need) or BUDGET_STOP836:
        continue
    if (time.perf_counter() - T0_836) / 60.0 > HARD_BUDGET_MIN836:
        BUDGET_STOP836 = True; log829('TEST836_BUDGET_STOP', 'p3_items_done', ii836); break
    bank = list(it['bank']); qid = it['qid']; scache = {}
    memB, nB = mount834(bank, 'P3BANK_%d' % ii836)
    sealB = seal834(memB); csp = cspans834(bank)
    f0 = bank_forward835(memB, nB, qid, s0_834(qid, nB), csp)
    P3RES836[key0] = {'M': f0['M'], 'h': np.asarray(f0['h'], dtype=np.float64)}; save_vec836('p3', key0, P3RES836[key0])
    for s in it['states']:
        S = state_after836(s['cards'], qid, nB, scache)
        if s['rotate']:
            S = rotate834(S)
        f = bank_forward835(memB, nB, qid, S, csp)
        k = 'P3_%d_%s' % (ii836, s['sid'])
        P3RES836[k] = {'M': f['M'], 'h': np.asarray(f['h'], dtype=np.float64)}; save_vec836('p3', k, P3RES836[k])
        del S, f
    gate829('MEAS_KV_SEAL_P3BANK_%d' % ii836, seal834(memB) == sealB)
    del memB, scache; gc.collect(); release()
    log829('TEST836_P3_PROGRESS', ii836 + 1, '/', len(P3ITEMS836))
D829['budget_stop836'] = BUDGET_STOP836

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
for cid836 in cards829:
    gate829('FINAL_SHA_' + cid836, sha_file(CART_DIR / entries[cid836]['file']) == entries[cid836]['sha256'])
gate829('COUNTED_WITHIN_UPPER_BOUND', all(COUNT834[k] <= POST836['numeric_upper'][k] for k in POST836['numeric_upper']),
        {'counted': dict(COUNT834), 'upper': POST836['numeric_upper']})

# ==================================================================================================================
# OFFLINE PHASE: all measurements saved; roles are read only from here.
# ==================================================================================================================
log829('TEST836_OFFLINE_START')
KIND836 = {cid: m['kind'] for cid, m in card_meta829.items()}
def feats836(case, space):
    z0, za, zb, zab = (VEC836[case[k]][space] for k in ('null', 'a', 'b', 'ab'))
    gam = zab - za - zb + z0; db0 = zb - z0
    ng = float(np.linalg.norm(gam)); nb0 = float(np.linalg.norm(db0))
    return {'rho': ng / max(nb0, 1e-300), 'gamma': ng, 'delta_b_alone': nb0}
avail836 = lambda c: all(c[k] in VEC836 for k in ('null', 'a', 'b', 'ab'))
RHO836 = {}
for c in CASES836:
    if avail836(c):
        k = CASEKEY836[c['case']]
        RHO836[(c['phase'], k['world'], k['b_role'], k.get('b_world', k['world']), k['order'])] = {sp: feats836(c, sp) for sp in SPACES836}
def p1cells836(space):
    cells = []
    for wa in range(len(worlds829)):
        for order in ('FORWARD', 'REVERSE'):
            t = RHO836.get(('P1', wa, 'TRUE', wa, order))
            if t is None:
                continue
            row = [RHO836[x][space]['rho'] for x in RHO836 if x[0] == 'P1' and x[1] == wa and x[4] == order and x[2] in
                   ('MISMATCHED', 'MIRROR', 'INBOUND', 'FORK')]
            col = [RHO836[x][space]['rho'] for x in RHO836 if x[0] == 'P1' and x[2] == 'MISMATCHED' and x[3] == wa and x[4] == order]
            alt = RHO836.get(('P1', wa, 'ALT', wa, order))
            tr = t[space]['rho']
            cells.append({'world': wa, 'order': order, 'true': tr, 'max_row': max(row) if row else None,
                          'max_col': max(col) if col else None,
                          'pass': bool(row) and bool(col) and tr > max(row) and tr > max(col),
                          'alt': alt[space]['rho'] if alt else None,
                          'alt_pass': bool(alt) and bool(row) and alt[space]['rho'] > max(row)})
    return cells
P1CELLS836 = {sp: p1cells836(sp) for sp in SPACES836}
def p2cells836(space):
    cells = []
    for wa in range(len(worlds829)):
        for order in ('FORWARD', 'REVERSE'):
            t = RHO836.get(('P2', wa, 'TRUE', wa, order))
            if t is None:
                continue
            ctl = {r: RHO836[('P2', wa, r, wa, order)][space]['rho'] for r in ('MIRROR', 'INBOUND', 'FORK', 'MISMATCHED_IN_BANK')
                   if ('P2', wa, r, wa, order) in RHO836}
            alt = RHO836.get(('P2', wa, 'ALT', wa, order))
            tr = t[space]['rho']
            allr = dict(ctl); allr['TRUE'] = tr
            if alt:
                allr['ALT'] = alt[space]['rho']
            cells.append({'world': wa, 'order': order, 'true': tr, 'controls': ctl,
                          'pass': len(ctl) == 4 and all(tr > v for v in ctl.values()),
                          'alt': alt[space]['rho'] if alt else None,
                          'argmax_role': max(allr, key=lambda r: allr[r])})
    return cells
P2CELLS836 = {sp: p2cells836(sp) for sp in SPACES836}
def cnt836(cells, key='pass'):
    return [sum(1 for c in cells if c[key]), len(cells)]
def order_worlds836(cells):
    ok = 0; tot = 0
    for wa in range(len(worlds829)):
        cs = [c for c in cells if c['world'] == wa]
        if len(cs) == 2:
            tot += 1; ok += all(c['pass'] for c in cs)
    return [ok, tot]
# ---- P3 analysis ----
P3EV836 = []
for ii836, it in enumerate(P3ITEMS836):
    if 'P3_%d_OFF' % ii836 not in P3RES836:
        continue
    wa = QID836.index(it['qid']); w = worlds829[wa]; bank = it['bank']; idx = {c: i for i, c in enumerate(bank)}
    fi = idx[w['ids']['first']]; si = idx[w['ids']['second']]
    nonchain = [i for i, c in enumerate(bank) if c not in (w['ids']['first'], w['ids']['second'])]
    M0 = P3RES836['P3_%d_OFF' % ii836]['M'].astype(np.float64); h0 = P3RES836['P3_%d_OFF' % ii836]['h']
    dcomp = None
    jfirst = next((j['job'] for j in JOBS836 if j['qid'] == it['qid'] and j['mount'] == [w['ids']['first']]), None)
    jpair = next((j['job'] for j in JOBS836 if j['qid'] == it['qid'] and j['mount'] == [w['ids']['first'], w['ids']['second']]), None)
    if jfirst in VEC836 and jpair in VEC836:
        dcomp = VEC836[jpair]['h'] - VEC836[jfirst]['h']
    def argmax_second(M):
        Mx = np.array(M, copy=True); Mx[..., fi] = -np.inf
        return int((np.argmax(Mx, axis=-1) == si).sum())
    rec = {'world': wa, 'argmax_second_heads_OFF': argmax_second(M0)}
    for s in it['states']:
        k = 'P3_%d_%s' % (ii836, s['sid'])
        if k not in P3RES836:
            continue
        role = P3KEY836[s['sid']]
        M = P3RES836[k]['M'].astype(np.float64); D_ = M - M0
        spec = (D_[..., si] > 0) & (D_[..., si] > np.max(D_[..., nonchain], axis=-1))
        dh = P3RES836[k]['h'] - h0
        rec[role] = {'spec_heads': int(spec.sum()), 'argmax_second_heads': argmax_second(M),
                     'mean_gain_second': float(D_[..., si].mean()), 'mean_gain_first': float(D_[..., fi].mean()),
                     'mean_gain_nonchain': float(D_[..., nonchain].mean()),
                     'hidden_shift_norm': float(np.linalg.norm(dh)),
                     'hidden_shift_cos_completion': (float(np.dot(dh, dcomp) / max(np.linalg.norm(dh) * np.linalg.norm(dcomp), 1e-300))
                                                     if dcomp is not None else None)}
    ctrls = [rec.get(r, {}).get('spec_heads') for r in ('FIRST_ROTATED', 'FORK_FIRST', 'IRRELEVANT')]
    rec['first_beats_all_controls'] = ('FIRST' in rec and all(x is not None for x in ctrls) and
                                       rec['FIRST']['spec_heads'] > max(ctrls))
    P3EV836.append(rec)
# ---- P4: TEST832 policy decomposition (oracle inputs per step) ----
P4_836 = []
def single836(c, qid):
    j = next((x['job'] for x in JOBS836 if x['qid'] == qid and x['mount'] == [c]), None)
    return VEC836.get(j) if j else None
for wa, w in enumerate(worlds829):
    q = QID836[wa]; bank = BANKS836[wa // BLOCK836]
    jn = next(x['job'] for x in JOBS836 if x['qid'] == q and x['mount'] == [NULL829])
    if jn not in VEC836:
        continue
    eff = {c: cosdist829(single836(c, q)['h'], VEC836[jn]['h']) for c in bank if single836(c, q) is not None}
    if len(eff) < 3:
        continue
    rk = sorted(eff, key=lambda c: -eff[c])
    v = [max(eff[c], 1e-300) for c in rk]
    gaps = [math.log(v[i]) - math.log(v[i + 1]) for i in range(len(v) - 1)]
    g = 1 + max(range(len(gaps)), key=lambda i: (gaps[i], -i))
    rec = {'world': wa, 'first_rank_by_single_effect': rk.index(w['ids']['first']) + 1, 'relevance_cut_size': g,
           'cut_contains_first': w['ids']['first'] in rk[:g], 'cut_contains_second': w['ids']['second'] in rk[:g],
           'top_single_role': KIND836.get(rk[0])}
    for order in ('FORWARD', 'REVERSE'):
        row = {x[2] + ('' if x[2] != 'MISMATCHED' else '_' + str(x[3])): RHO836[x]['h']['rho'] for x in RHO836
               if x[0] == 'P1' and x[1] == wa and x[4] == order}
        if row:
            best = max(row, key=lambda r: row[r])
            rec['closure_isolated_' + order] = best
            col = {x[1]: RHO836[x]['h']['rho'] for x in RHO836 if x[0] == 'P1' and x[2] == 'MISMATCHED' and x[3] == wa and x[4] == order}
            col[wa] = row.get('TRUE', -1)
            rec['mutual_best_' + order] = max(col, key=lambda a: col[a]) == wa
            neg = [row[r] for r in row if r.startswith('MISMATCHED') or r in ('MIRROR', 'INBOUND', 'FORK')]
            rec['conflict_detectable_' + order] = bool(neg) and row.get('TRUE', -1) > max(neg) and row.get('ALT', -1) > max(neg)
        c2 = next((c for c in P2CELLS836['h'] if c['world'] == wa and c['order'] == order), None)
        if c2:
            rec['closure_bank_' + order] = c2['argmax_role']
    P4_836.append(rec)
def frac_ok836(k, n, need):
    return 'INCONCLUSIVE' if n == 0 else ('PASS' if k >= need else 'FAIL')
t1 = cnt836(P1CELLS836['h']); t2 = cnt836(P2CELLS836['h'])
T1 = frac_ok836(t1[0], t1[1], 10) if t1[1] == 12 else 'INCONCLUSIVE'
T2 = frac_ok836(t2[0], t2[1], 10) if t2[1] == 12 else 'INCONCLUSIVE'
o1 = order_worlds836(P1CELLS836['h']); o2 = order_worlds836(P2CELLS836['h'])
T3 = 'INCONCLUSIVE' if o1[1] < 6 or o2[1] < 6 else ('PASS' if o1[0] >= 5 and o2[0] >= 5 else 'FAIL')
t4 = cnt836(P1CELLS836['h'], 'alt_pass')
T4 = frac_ok836(t4[0], t4[1], 10) if t4[1] == 12 else 'INCONCLUSIVE'
t5 = [sum(r['first_beats_all_controls'] for r in P3EV836), len(P3EV836)]
T5 = frac_ok836(t5[0], t5[1], 5) if t5[1] == 6 else 'INCONCLUSIVE'
CRIT836 = {'T1_POSITIVE_CONTROL': T1, 'T2_BANK_CONTEXT': T2, 'T3_ORDER': T3, 'T4_ALT_VALID_CHAIN': T4, 'T5_NATIVE_TRANSFER': T5}
locus = [nm for nm, t in (('CONTEXT', T2), ('TRANSFER', T5)) if t != 'PASS']
if BUDGET_STOP836:
    decision836 = 'YETERSİZ KANIT'
elif T1 == 'FAIL':
    decision836 = 'DUR'
elif T1 == 'PASS' and T2 == 'PASS' and T5 == 'PASS':
    decision836 = 'DEVAM'
else:
    decision836 = 'YETERSİZ KANIT'
def p4count836(key, ok):
    xs = [r.get(key) for r in P4_836 if key in r]
    return [sum(1 for x in xs if ok(x)), len(xs)]
P4SUM836 = {'1_first_top1_by_single_effect': p4count836('first_rank_by_single_effect', lambda x: x == 1),
            '2_cut_contains_first': p4count836('cut_contains_first', bool),
            '2_cut_contains_second': p4count836('cut_contains_second', bool),
            '3_closure_isolated_valid': [sum(1 for r in P4_836 for o in ('FORWARD', 'REVERSE') if r.get('closure_isolated_' + o) in ('TRUE', 'ALT')),
                                         sum(1 for r in P4_836 for o in ('FORWARD', 'REVERSE') if 'closure_isolated_' + o in r)],
            '3_closure_bank_valid': [sum(1 for r in P4_836 for o in ('FORWARD', 'REVERSE') if r.get('closure_bank_' + o) in ('TRUE', 'ALT')),
                                     sum(1 for r in P4_836 for o in ('FORWARD', 'REVERSE') if 'closure_bank_' + o in r)],
            '4_mutual_best': [sum(1 for r in P4_836 for o in ('FORWARD', 'REVERSE') if r.get('mutual_best_' + o)),
                              sum(1 for r in P4_836 for o in ('FORWARD', 'REVERSE') if 'mutual_best_' + o in r)],
            '5_conflict_detectable': [sum(1 for r in P4_836 for o in ('FORWARD', 'REVERSE') if r.get('conflict_detectable_' + o)),
                                      sum(1 for r in P4_836 for o in ('FORWARD', 'REVERSE') if 'conflict_detectable_' + o in r)]}
def loss_step836():
    for k, (a, n) in P4SUM836.items():
        if n and a < (5 if n <= 6 else 10):
            return k
    return 'NONE'
P3SUM836 = {}
for role in ('FIRST', 'FIRST_ROTATED', 'FORK_FIRST', 'IRRELEVANT', 'COMPLETE_PAIR'):
    xs = [r[role] for r in P3EV836 if role in r]
    if xs:
        P3SUM836[role] = {'spec_heads_per_world': [x['spec_heads'] for x in xs],
                          'argmax_second_heads_per_world': [x['argmax_second_heads'] for x in xs],
                          'mean_gain_second': float(np.mean([x['mean_gain_second'] for x in xs])),
                          'mean_gain_nonchain': float(np.mean([x['mean_gain_nonchain'] for x in xs])),
                          'hidden_shift_cos_completion_mean': (float(np.mean([x['hidden_shift_cos_completion'] for x in xs]))
                                                               if all(x['hidden_shift_cos_completion'] is not None for x in xs) else None)}
P3SUM836['argmax_second_heads_OFF_per_world'] = [r['argmax_second_heads_OFF'] for r in P3EV836]
REPORT836 = {
    'P1_isolated_rho': {sp: {'pass': cnt836(P1CELLS836[sp]), 'alt_pass': cnt836(P1CELLS836[sp], 'alt_pass'),
                             'both_orders_worlds': order_worlds836(P1CELLS836[sp]),
                             'mean_true': float(np.mean([c['true'] for c in P1CELLS836[sp]])) if P1CELLS836[sp] else None,
                             'mean_max_row': float(np.mean([c['max_row'] for c in P1CELLS836[sp]])) if P1CELLS836[sp] else None}
                        for sp in SPACES836},
    'P2_bank_rho': {sp: {'pass': cnt836(P2CELLS836[sp]), 'both_orders_worlds': order_worlds836(P2CELLS836[sp]),
                         'argmax_roles': {r: sum(1 for c in P2CELLS836[sp] if c['argmax_role'] == r) for r in ('TRUE',) + tuple(P2_ROLES836[1:])},
                         'mean_true': float(np.mean([c['true'] for c in P2CELLS836[sp]])) if P2CELLS836[sp] else None}
                    for sp in SPACES836},
    'P3_transfer': P3SUM836, 'P3_first_beats_controls_worlds': t5,
    'P4_decomposition': P4SUM836, 'P4_loss_step': loss_step836(),
    'resume': D829['resume836'], 'determinism': D829['determinism836']}
D829['cells836'] = {'P1': P1CELLS836, 'P2': P2CELLS836, 'P3': P3EV836, 'P4': P4_836}
D829['report836'] = REPORT836
D829['verdict836'] = {'decision': decision836, 'criteria': CRIT836, 'loss_locus': locus, 'budget_stop': BUDGET_STOP836,
                      'interpretation_guard': 'rho and head counts are measurements; no Python threshold is reported as model-native control.'}
D829['claims_ledger836'] = dict(CLAIMS836, demonstrated_by_TEST836={'decision': decision836, 'criteria': CRIT836})
D829['cost836'] = {'counted': dict(COUNT834), 'predicted_upper': POST836, 'measure_seconds': D829['measure_seconds836'],
                   'total_seconds_body': round(time.perf_counter() - T0_836, 3),
                   'peak_gpu_gib': float(_torch829.cuda.max_memory_allocated()) / 2**30}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f836:
    wr836 = csv.DictWriter(f836, fieldnames=['phase', 'world', 'order', 'space', 'true', 'max_row_or_controls', 'pass', 'alt'])
    wr836.writeheader()
    for ph, cells in (('P1', P1CELLS836), ('P2', P2CELLS836)):
        for sp in SPACES836:
            for c in cells[sp]:
                wr836.writerow({'phase': ph, 'world': c['world'], 'order': c['order'], 'space': sp, 'true': c['true'],
                                'max_row_or_controls': c.get('max_row', json.dumps(c.get('controls'))), 'pass': c['pass'], 'alt': c['alt']})
D829['status'] = 'COMPLETE_TEST836_EVALUATED' if not BUDGET_STOP836 else 'STOPPED_BUDGET_PARTIAL_EVALUATED'
save829()
log829('TEST836_REPORT', json.dumps(REPORT836, default=str))
log829('TEST836_VERDICT', json.dumps(D829['verdict836'], default=str))
log829('TEST836_COMPLETED', str(OUT829))
'''
BODY_SHA836 = hashlib.sha256(BODY836.encode()).hexdigest()
PANEL_HOOK836 = ("PANEL829['test836'] = {'jobs': JOBS836, 'cases': CASES836, 'p3_items': P3ITEMS836, 'banks': BANKS836, "
                 "'hypotheses': %r, 'body_sha256': %r, 'helpers_sha256': %r, 'seed': SEED829}\n"
                 % (HYP836, BODY_SHA836, HELPER_SHA836))
src836 = patch836(src836, "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))",
                  PANEL_HOOK836 + "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))")
OFFLINE_HOOK836 = r'''
OFFLINE836 = DIR829 / 'TEST836_offline_key.json'   # never read by any runtime computation
OFFLINE836.write_text(json.dumps({'note': 'OFFLINE ONLY', 'jobs': JOBKEY836, 'cases': CASEKEY836, 'p3_states': P3KEY836,
                                  'worlds': worlds829, 'questions': questions829, 'card_meta': card_meta829},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D829['offline_key836_sha256'] = sha829(OFFLINE836.read_bytes())
'''
src836 = patch836(src836, "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n",
                  "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n" + OFFLINE_HOOK836)
start836 = src836.index("    # RUN ORDER: integrity checks")
start836 = src836.rfind("    # ---", 0, start836)
end836 = src836.index("except BaseException as e:\n    D829['status'] = 'ERROR'", start836)
BODY836_TEXT = BODY836
replacement836 = "\n".join("    " + line if line else "" for line in BODY836.strip("\n").splitlines()) + "\n"
patched836 = src836[:start836] + replacement836 + src836[end836:]
ast.parse(patched836)

# ==================================================================================================================
# CONSOLE / LOGGING LAYER (TEST835 pattern). Nothing below changes what is computed. Every byte the engine prints is
# written unchanged to a full transcript file; the screen shows a compact digest, progress, failures and the summary.
# ==================================================================================================================
import os as _os836, sys as _sys836, io as _io836, traceback as _tb836, datetime as _dt836, shutil as _sh836
from pathlib import Path as _P836
_os836.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')     # download bars only (not data)
for _m836, _f836 in (('huggingface_hub', lambda m: m.utils.disable_progress_bars()),
                     ('transformers', lambda m: m.utils.logging.disable_progress_bar())):
    if _m836 in _sys836.modules:                                    # only if already imported: no new import
        try:
            _f836(_sys836.modules[_m836])
        except Exception:
            pass
_ROOT836 = _P836('/content') if _P836('/content').exists() else _P836('/tmp')
FULL_CONSOLE836 = _ROOT836 / ('TEST836_full_console_' + _dt836.datetime.now(_dt836.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.txt')
CON836 = {'phase': 'SOURCE_VERIFICATION', 'last': [], 'fail_lines': [], 't0': time.time(), 'measure': '0/0', 'p3': 0}
_ORIG_OUT836, _ORIG_ERR836 = _sys836.stdout, _sys836.stderr

def say836(*a):
    _ORIG_OUT836.write(' '.join(str(x) for x in a) + '\n'); _ORIG_OUT836.flush()

def _mins836():
    return round((time.time() - CON836['t0']) / 60.0, 1)

def route836(line):
    s = line.strip()
    if not s:
        return
    CON836['last'] = (CON836['last'] + [s[:300]])[-6:]
    if s.startswith('FAIL '):
        CON836['fail_lines'].append(s[:600]); say836('!! ' + s[:600]); return
    if s.startswith('TEST829_FAILED'):
        CON836['fail_lines'].append(s[:300]); return
    if s.startswith('TEST829_START'):
        parts = s.split()
        say836('Çalışma: %s | panel SHA-256: %s' % (parts[1] if len(parts) > 1 else '?', parts[-1]))
        CON836['phase'] = 'ENGINE_PRELUDE_AND_LOCKS'; return
    if s.startswith('TEST815_GPU_PREFLIGHT'):
        say836('GPU: ' + s[len('TEST815_GPU_PREFLIGHT'):].strip()); return
    if s.startswith('TEST815_GPU_FREE_GIB'):
        say836('GPU boş VRAM (yükleme öncesi): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('TEST836_PREDICTED_COST_BEFORE_MODEL_LOAD'):
        try:
            c = json.loads(s.split(' ', 1)[1]); u = c['numeric_upper']
            say836('Maliyet üst sınırı (model yükleme hariç): %s dk | iş %s, mount grubu %s, durum %s | kartuş %s (~%s MB), '
                   'vektör dosyaları ~%s MB | fusion<=%s probe<=%s' % (c['minutes_upper_excluding_model_load'], c['jobs'],
                   c['mount_groups'], c['p3_items'], c['physical_cartridges'], c['cartridge_disk_mb_estimate'],
                   c['vector_disk_mb_estimate'], u['fusion_forwards'], u['probe_forwards']))
        except Exception:
            say836(s[:300])
        CON836['phase'] = 'MODEL_LOAD'; say836('Model yükleniyor (Qwen2.5-72B-Instruct, NF4, tek yükleme)...'); return
    if s.startswith('PASS FROZEN_PREFIX'):
        D_ = globals().get('D829', {})
        say836('Model yüklendi (%s s). Fiziksel kartuşlar üretiliyor ve SHA doğrulanıyor...' % D_.get('model_load_seconds', '?'))
        CON836['phase'] = 'PHYSICAL_CARTRIDGE_FORGING'; return
    if s.startswith('PASS PHYSICAL_COUNT'):
        say836('Fiziksel kartuşlar: ' + s.split()[-1] + ' (her biri SHA-256 + tensör SHA ile yeniden yüklendi)')
        CON836['phase'] = 'PREFLIGHT_GATES'; return
    if s.startswith('PASS ARCH_DIMS'):
        say836('Mimari (NL,H,QH,KVH,HD): ' + s[len('PASS ARCH_DIMS'):].strip() + ' | BF16 hesap, NF4, ağırlıklar donmuş'); return
    if s.startswith('PASS VRAM_HEADROOM'):
        say836('Boş VRAM (model sonrası): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('PASS HEADPROBE_EQUALS_LOCKED_ATTENTION_PROBE'):
        say836('Eşdeğerlik kapıları geçti (CUT3/hidden bitwise, HeadProbe farkı ' + s.split()[-1] + ')')
        CON836['phase'] = 'MEASUREMENT_P1_P2'; return
    if s.startswith('TEST836_RESUME '):
        try:
            r = json.loads(s.split(' ', 1)[1])
            say836('Devam mekanizması: yeniden kullanılan iş %s, P3 %s | %s' % (r.get('reused_jobs'), r.get('reused_p3'), r.get('reason')))
        except Exception:
            say836(s[:300])
        return
    if s.startswith('TEST836_MEASURE_PROGRESS'):
        p = s.split()
        CON836['measure'] = p[1] + '/' + p[3] if len(p) > 3 else '?'
        CON836['phase'] = 'MEASUREMENT_P1_P2 (mount grubu %s)' % CON836['measure']
        say836('  ölçüm (P1+P2) mount grubu %s | iş %s (%s dk)' % (CON836['measure'], ' '.join(p[5:8]) if len(p) > 7 else '?', _mins836()))
        return
    if s.startswith('TEST836_P3_PROGRESS'):
        p = s.split(); CON836['p3'] = p[1]
        CON836['phase'] = 'P3_TRANSFER (%s)' % ' '.join(p[1:4])
        if p[1] == p[3] or int(p[1]) % 3 == 0:
            say836('  aktarım (P3) %s/%s (%s dk)' % (p[1], p[3], _mins836()))
        return
    if s.startswith('TEST836_BUDGET_STOP'):
        say836('!! ' + s); return
    if s.startswith('TEST836_OFFLINE_START'):
        CON836['phase'] = 'OFFLINE_EVALUATION'
        say836('Ölçüm bitti; çevrimdışı değerlendirme (%s dk)' % _mins836()); return
    if s.startswith('TEST836_COMPLETED'):
        CON836['phase'] = 'COMPLETED'; return

class Console836(_io836.TextIOBase):
    """Writes everything to FULL_CONSOLE836 unchanged; routes complete lines to the compact screen digest."""
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
                route836(line.split('\r')[-1])
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

def sha_path836(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()

def fmt836(x):
    if isinstance(x, list) and len(x) == 2 and all(isinstance(v, (int, float)) for v in x):
        return '%s/%s' % (x[0], x[1])
    if isinstance(x, dict):
        return ', '.join('%s=%s' % (k, fmt836(v)) for k, v in x.items())
    if isinstance(x, float):
        return '%.4g' % x
    if isinstance(x, list):
        return '[' + ', '.join(fmt836(v) for v in x) + ']'
    return str(x)

def files_report836():
    say836('=' * 78); say836('SONUÇ DOSYALARI (SHA-256)')
    d = globals().get('DIR829')
    if d is None or not _P836(d).exists():
        say836('  (çalışma klasörü yok)'); return
    for p in sorted(_P836(d).iterdir()):
        if p.is_file():
            say836('  %s  %d B  %s' % (p, p.stat().st_size, sha_path836(p)))
    vd = _P836(d) / 'TEST836_vectors'
    if vd.exists():
        fs = sorted(x for x in vd.iterdir() if x.is_file())
        say836('  %s/  %d vektör dosyası, %.1f MB (her dosyanın SHA-256 değeri TEST836_vector_manifest.jsonl içinde)'
               % (vd, len(fs), sum(x.stat().st_size for x in fs) / 2**20))

def final836(D):
    R = D['report836']; V = D['verdict836']; K = V['criteria']; C = D['cost836']
    checks = D.get('checks', [])
    say836('=' * 78); say836('TEST836 SONUÇ ÖZETİ (aktarım denetimi; kontrolcü yok)'); say836('=' * 78)
    say836('Durum: %s | bütçe durdurması: %s | devam: iş %s, P3 %s' % (D.get('status'), V['budget_stop'],
           R['resume'].get('reused_jobs'), R['resume'].get('reused_p3')))
    say836('Bütünlük: %d kapı, %d başarısız | eşdeğerlik: %s | determinizm: %s' % (len(checks), sum(not c['pass'] for c in checks),
           fmt836(D.get('probe_equivalence836', {})), fmt836(R.get('determinism', {}))))
    say836('-' * 78); say836('[P1] POZİTİF KONTROL — izole çiftler, TEST831 rho (satır+sütun üstünlüğü, 12 hücre)')
    for sp, nm in (('h', 'son-norm hidden'), ('state', 'CUT3'), ('lp', 'log-olasılık')):
        r = R['P1_isolated_rho'][sp]
        say836('  %-16s geçen %s | ALT geçerli zincir %s | iki sırada geçen dünya %s | ort. TRUE %s, ort. en büyük satır %s'
               % (nm, fmt836(r['pass']), fmt836(r['alt_pass']), fmt836(r['both_orders_worlds']), fmt836(r['mean_true']), fmt836(r['mean_max_row'])))
    say836('[P2] BANKA BAĞLAMI — çift 18 kartlık bankanın içinde (TRUE > mirror/inbound/fork/banka-içi yanlış ikinci)')
    for sp, nm in (('h', 'son-norm hidden'), ('state', 'CUT3'), ('lp', 'log-olasılık')):
        r = R['P2_bank_rho'][sp]
        say836('  %-16s geçen %s | iki sırada geçen dünya %s | en büyük rho rolü: %s'
               % (nm, fmt836(r['pass']), fmt836(r['both_orders_worlds']), fmt836(r['argmax_roles'])))
    say836('[P3] NATIVE AKTARIM — aynı 5120 baş, aynı okuma; ikinci karta özgü kazanç gösteren baş sayısı (dünya başına)')
    P3 = R['P3_transfer']
    for role in ('FIRST', 'FIRST_ROTATED', 'FORK_FIRST', 'IRRELEVANT', 'COMPLETE_PAIR'):
        if role in P3:
            x = P3[role]
            say836('  %-14s özgü baş %s | ikinci argmax baş %s | ort. kazanç ikinci %s / zincir dışı %s | hidden-tamamlanma cos %s'
                   % (role, x['spec_heads_per_world'], x['argmax_second_heads_per_world'], fmt836(x['mean_gain_second']),
                      fmt836(x['mean_gain_nonchain']), fmt836(x['hidden_shift_cos_completion_mean'])))
    say836('  OFF ikinci argmax baş: %s | FIRST tüm kontrolleri geçen dünya: %s' % (P3.get('argmax_second_heads_OFF_per_world'),
                                                                                fmt836(R['P3_first_beats_controls_worlds'])))
    say836('[P4] TEST832 ADIM AYRIŞTIRMASI (her adım önceki adımlar doğru verilerek)')
    for k, v in R['P4_decomposition'].items():
        say836('  %-34s %s' % (k, fmt836(v)))
    say836('  kayıp adımı: ' + str(R['P4_loss_step']))
    say836('-' * 78); say836('T1–T5')
    det = {'T1_POSITIVE_CONTROL': fmt836(R['P1_isolated_rho']['h']['pass']), 'T2_BANK_CONTEXT': fmt836(R['P2_bank_rho']['h']['pass']),
           'T3_ORDER': 'izole %s, banka %s' % (fmt836(R['P1_isolated_rho']['h']['both_orders_worlds']), fmt836(R['P2_bank_rho']['h']['both_orders_worlds'])),
           'T4_ALT_VALID_CHAIN': fmt836(R['P1_isolated_rho']['h']['alt_pass']), 'T5_NATIVE_TRANSFER': fmt836(R['P3_first_beats_controls_worlds'])}
    for k in K:
        say836('  %-22s %-12s %s' % (k, K[k], det.get(k, '')))
    say836('=' * 78)
    say836('NİHAİ BİLİMSEL KARAR: %s' % V['decision'])
    if V['decision'] == 'DUR':
        say836('  Gerekçe: T1 FAIL — TEST831 ilişkisel sinyali yeni seed ile yeniden üretilemedi.')
    elif V['decision'] == 'DEVAM':
        say836('  Gerekçe: sinyal yeniden üretildi (T1), bankada korundu (T2) ve native KV durumu onu ikinci karta özgü '
               'dikkat kazancına taşıdı (T5). Bu bir ölçümdür; kapalı döngü kontrol henüz kurulmadı.')
    else:
        say836('  Gerekçe: ' + ('bütçe durdurması' if V['budget_stop'] else 'kayıp yeri = ' + (', '.join(V['loss_locus']) or 'belirsiz')
                                + ' (CONTEXT: banka bağlamında kayboluyor; TRANSFER: native durum onu sonraki hesaplamaya taşımıyor)'))
    say836('  Not: rho ve baş sayıları Python ile hesaplanan ölçümlerdir; model-native kontrol olarak sunulmaz.')
    say836('Maliyet: sayılan %s | ölçüm %s s | toplam gövde %s s | tepe VRAM %.2f GiB'
           % (fmt836(C['counted']), C['measure_seconds'], C['total_seconds_body'], C['peak_gpu_gib']))

say836('=' * 78)
say836('AKBASCORE TEST836 — aktarım denetimi; Qwen2.5-72B-Instruct (NF4, donmuş), tek A100-80GB, tek hücre')
say836('Kaynak kilitleri: 829.py %s | 834.py %s | 835.py %s | 831.log %s | 835.log %s'
       % (LOCK829_836, LOCK834_836, LOCK835_836, LOCK831LOG_836, LOCK835LOG_836))
say836('Kilitli yardımcılar (AST, %d fonksiyon) SHA-256 %s' % (len(HELPERS836), HELPER_SHA836))
say836('BODY836 SHA-256 %s | yamalı kaynak AST geçti (%d bayt, SHA-256 %s)' % (BODY_SHA836, len(patched836), hashlib.sha256(patched836.encode()).hexdigest()))
say836('Kapsam: %d dünya, 18 kartlık 2 banka | P1 izole rho, P2 banka rho, P3 native aktarım (5 durum), P4 TEST832 ayrıştırması'
       % WORLDS_EVAL836)
say836('Tam konsol kaydı: ' + str(FULL_CONSOLE836))
say836('=' * 78)
_fh836 = open(FULL_CONSOLE836, 'a', encoding='utf-8', buffering=1)
_fh836.write('TEST836_SOURCE_LOCKS ' + ' '.join((LOCK829_836, LOCK834_836, LOCK835_836, LOCK831LOG_836, LOCK835LOG_836)) +
             '\nTEST836_BODY_SHA256 ' + BODY_SHA836 + '\nTEST836_HELPERS ' + HELPER_SHA836 +
             '\nTEST836_PATCHED_SOURCE_AST_PASS ' + str(len(patched836)) + ' ' + hashlib.sha256(patched836.encode()).hexdigest() + '\n')
import linecache as _lc836
for _nm836, _src836 in (('TEST836_LOCKED_ENGINE', patched836), ('TEST836_LOCKED_HELPERS', HELPER_SRC836)):
    _lc836.cache[_nm836] = (len(_src836), None, [x + '\n' for x in _src836.splitlines()], _nm836)
_sys836.stdout = Console836(_ORIG_OUT836, _fh836); _sys836.stderr = Console836(_ORIG_ERR836, _fh836)
TEST836_ERROR = None
try:
    exec(compile(patched836, 'TEST836_LOCKED_ENGINE', 'exec'), globals())
except BaseException as _e836:
    TEST836_ERROR = _e836
    _tbtext836 = _tb836.format_exc()
    _fh836.write('\n[TEST836 OUTER EXCEPTION]\n' + _tbtext836)
finally:
    _sys836.stdout, _sys836.stderr = _ORIG_OUT836, _ORIG_ERR836
    try:
        _fh836.flush(); _fh836.close()
    except Exception:
        pass
    _dir836 = globals().get('DIR829')
    if _dir836 is not None and _P836(_dir836).exists() and FULL_CONSOLE836.exists():
        _dst836 = _P836(_dir836) / FULL_CONSOLE836.name
        _sh836.move(str(FULL_CONSOLE836), str(_dst836)); FULL_CONSOLE836 = _dst836
if TEST836_ERROR is not None:
    D_ = globals().get('D829', {}) if isinstance(globals().get('D829'), dict) else {}
    bad = [c for c in D_.get('checks', []) if not c.get('pass')]
    say836('=' * 78); say836('TEST836 HATA')
    say836('Tür: %s.%s' % (type(TEST836_ERROR).__module__, type(TEST836_ERROR).__name__))
    say836('Mesaj: ' + repr(TEST836_ERROR)[:800])
    say836('Aşama: ' + CON836['phase'] + ' | geçen %s dk' % _mins836())
    if bad:
        say836('Başarısız kapı: %s | ayrıntı: %s' % (bad[-1].get('name'), str(bad[-1].get('detail'))[:400]))
    say836('Hata öncesi son motor satırları:')
    for x in CON836['last'][-4:]:
        say836('  ' + x[:240])
    tbl = _tbtext836.rstrip().splitlines()
    say836('Traceback (son %d satır; tamamı dosyada ve results.json içinde):' % min(40, len(tbl)))
    for x in tbl[-40:]:
        say836('  ' + x)
    files_report836()
    say836('Tam konsol kaydı: %s  SHA-256 %s' % (FULL_CONSOLE836, sha_path836(FULL_CONSOLE836) if FULL_CONSOLE836.exists() else '-'))
    say836('Not: tamamlanan ölçümler vektör dosyalarında; hücre yeniden çalıştırılırsa SHA doğrulanıp yeniden kullanılır.')
    raise SystemExit('TEST836_FAILED: ' + type(TEST836_ERROR).__name__)
try:
    final836(D829)
except Exception as _e836s:
    say836('!! Özet basılamadı (veri dosyalarda tam): ' + repr(_e836s))
    say836(_tb836.format_exc()[-1500:])
files_report836()
say836('=' * 78)
