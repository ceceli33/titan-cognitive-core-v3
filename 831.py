# AKBASCORE SILICON HIPPOCAMPUS — TEST831, single Colab cell (one A100 80GB, frozen Qwen2.5-72B-Instruct NF4).
# RELATIONAL-COMPLETION DISCRIMINATION PILOT ON DESIGNED PAIRS (diagnostic only; no selector, no stopping).
# Backbone: the working TEST830 construction — the SHA-locked, GPU-completed TEST829 source is fetched, verified
# by git blob, patched at fixed anchors, and executed. The locked TEST815 engine (native CUT3/H3/KV), physical
# SSD cartridges, SHA/KV/weight gates and the observation-only readout are reused unchanged.
# No training, no residual hooks, no source replay, no RAG, no text-mediated control, no regex relation
# extraction at runtime. Text enters only as (a) the question encoding and (b) offline answer readouts that run
# after every numerical measurement and interaction value has been computed and saved.
# The experimenter designs the intervention pairs (allowed); runtime sees opaque job IDs only. Roles, worlds,
# answer key and orders live in a separate offline key. No GPU execution or result is claimed by the code author.
import urllib.request, hashlib, ast, json, time, random, math, itertools, numpy as np

URL831 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/829.py"
LOCK831 = "a5a25460a3a6bbdf62a0571a9b5ff19e64159cf7"          # 829.py git blob (same lock as TEST830)
SEED831 = 8312026
WORLDS831 = 6                                               # small sealed pilot; independent validation = new seed

with urllib.request.urlopen(urllib.request.Request(URL831, headers={"User-Agent": "AKBASCORE-TEST831"}), timeout=180) as f831:
    raw831 = f831.read(200001)
blob831 = hashlib.sha1(b"blob " + str(len(raw831)).encode() + b"\0" + raw831).hexdigest()
assert len(raw831) <= 200000 and blob831 == LOCK831, ("STOP_SOURCE_CHANGED", blob831)
src831 = raw831.decode("utf-8")

def patch831(text, old, new):
    assert text.count(old) == 1, ("PATCH_ANCHOR_NOT_UNIQUE", old[:80], text.count(old))
    return text.replace(old, new, 1)

# ---- 1. identity of this run (seed, run name, output names, world count) ----
src831 = patch831(src831, "SEED829 = 8292026", "SEED829 = %d" % SEED831)
src831 = patch831(src831, "WORLDS829 = 3 ", "WORLDS829 = %d " % WORLDS831)
src831 = patch831(src831, "RUN829 = 'TEST829_'", "RUN829 = 'TEST831_'")
for a831, b831 in (("'TEST829_results.json'", "'TEST831_results.json'"), ("'TEST829.log'", "'TEST831.log'"),
                   ("'TEST829_blind_review.csv'", "'TEST831_case_table.csv'"),
                   ("'TEST829_offline_key.json'", "'TEST829_base_offline_key.json'")):
    src831 = patch831(src831, a831, b831)

# ---- 2. panel extension: new physical cards, opaque jobs and cases; sealed BEFORE model loading ----
PANEL_EXT831 = r'''
# ---------------- TEST831 PANEL EXTENSION (module level, before any model call) ----------------
NULLB831 = 'E831_NULLB'
cards829[NULLB831] = 'CONTROL MEMORY. This record contains no relation entries.\n'
card_meta829[NULLB831] = {'domain': None, 'kind': 'null_b', 'body_sha256': sha829(cards829[NULLB831])}
for w in worlds829:
    while True:
        fe = code829()
        if fe not in seen829:
            seen829.add(fe); break
    w['fork_end'] = fe
    w['ids']['mirror'] = 'E831_' + code829()
    w['ids']['fork'] = 'E831_' + code829()
    cards829[w['ids']['mirror']] = ('Evidence record. Domain: ' + w['world'] + '\n' +
                                    'Directed relation: ' + w['end'] + ' -> ' + w['middle'] + '.\n')
    cards829[w['ids']['fork']] = ('Evidence record. Domain: ' + w['world'] + '\n' +
                                  'Directed relation: ' + w['start'] + ' -> ' + fe + '.\n')
    for kind in ('mirror', 'fork'):
        card_meta829[w['ids'][kind]] = {'domain': w['world'], 'kind': kind,
                                        'body_sha256': sha829(cards829[w['ids'][kind]])}
JOBS831, JOBKEY831, CASES831, CASEKEY831 = [], {}, [], {}
_rng831 = random.Random(SEED829 + 31)
def _jid831():
    return 'J831_' + ''.join(_rng831.choice('0123456789ABCDEF') for _ in range(12))
_job_by_key831 = {}
def _job831(ids, qid, role):
    k = (tuple(ids), qid)
    if k not in _job_by_key831:
        j = _jid831()
        _job_by_key831[k] = j
        JOBS831.append({'job': j, 'ids': list(ids), 'qid': qid})
        JOBKEY831[j] = role
    return _job_by_key831[k]
for wa, wrow in enumerate(worlds829):
    qid831x = questions829[wa]['qid']
    jn = {'A': _job831([NULL829], qid831x, {'row': wa, 'kind': 'NULL_A'}),
          'B': _job831([NULLB831], qid831x, {'row': wa, 'kind': 'NULL_B'})}
    a = wrow['ids']['first']
    ja = _job831([a], qid831x, {'row': wa, 'kind': 'ANCHOR_FIRST_LINK_ONLY'})
    blist = [('TRUE' if wb == wa else 'MISMATCHED_SECOND', wb, worlds829[wb]['ids']['second'])
             for wb in range(len(worlds829))]
    blist += [('MIRROR', wa, wrow['ids']['mirror']), ('INBOUND', wa, wrow['ids']['decoy']),
              ('FORK', wa, wrow['ids']['fork']), ('ALT', wa, wrow['ids']['changed'])]
    for role, wb, b in blist:
        jb = _job831([b], qid831x, {'row': wa, 'kind': 'SINGLE', 'b_role': role, 'b_world': wb})
        for order, ids in (('FORWARD', [a, b]), ('REVERSE', [b, a])):
            jab = _job831(ids, qid831x, {'row': wa, 'kind': 'PAIR', 'b_role': role, 'b_world': wb, 'order': order})
            for nv in ('A', 'B'):
                c = 'C831_' + ''.join(_rng831.choice('0123456789ABCDEF') for _ in range(12))
                CASES831.append({'case': c, 'null': jn[nv], 'a': ja, 'b': jb, 'ab': jab})
                CASEKEY831[c] = {'row': wa, 'b_role': role, 'b_world': wb, 'order': order, 'null_variant': nv}
_rng831.shuffle(JOBS831)
_rng831.shuffle(CASES831)
'''
src831 = patch831(src831,
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n",
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n" + PANEL_EXT831)

HYP831 = {
    'primary_hypothesis_H1': (
        'In the final-norm hidden state at the final question position, the true continuation b=B->C of the '
        'anchor a=A->B produces the largest relative second-order interaction rho = ||Gamma|| / ||z_b - z_0||, '
        'Gamma = z_ab - z_a - z_b + z_0, among all matched non-composing alternatives: every mismatched second '
        'link in the same row (same anchor and question), the same true b paired with every other anchor (same '
        'column), the lexical mirror C->B, the inbound card X->A and the fork A->E; in every world and in both '
        'cartridge orders, with the physical NULL_A baseline.'),
    'failure_condition': 'H1 is falsified if, for any world and any order, any listed control has rho >= rho_TRUE.',
    'statistic_provenance': ('rho was suggested by TEST830 data (TRUE/ALT ~2.1-2.3 vs decoy ~1.2-1.6); TEST831 is '
                             'its first confirmatory use, on a fresh seed with new controls. Raw ||Gamma|| (TEST830) '
                             'is reported as secondary.'),
    'not_claimed': ['autonomous selection', 'autonomous stopping', 'general reasoning',
                    'that a large interaction is evidence sufficiency'],
    'secondary_predeclared': ['raw ||Gamma|| dominance', 'NULL_B robustness', 'ALT valid-chain consistency',
                              'CUT3 and log-prob interaction features', 'exact column-permutation p-value',
                              'placement robustness (margin vs TRUE order effect)', 'single-effect correlation (H0a)'],
    'readout': 'final-norm hidden state (lm_head input) at the last question token; one forward per mounted set'}
PANEL_HOOK831 = ("PANEL829['test831'] = {'jobs': JOBS831, 'cases': CASES831, 'hypotheses': %r, "
                 "'worlds': WORLDS829, 'seed': SEED829}\n" % (HYP831,))
src831 = patch831(src831, "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))",
                  PANEL_HOOK831 + "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))")
OFFLINE_HOOK831 = r'''
OFFLINE831 = DIR829 / 'TEST831_offline_key.json'   # never read by any runtime computation
OFFLINE831.write_text(json.dumps({'note': 'OFFLINE ONLY — job/case roles', 'jobs': JOBKEY831, 'cases': CASEKEY831,
                                  'worlds': worlds829, 'questions': questions829, 'card_meta': card_meta829},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D829['offline_key831_sha256'] = sha829(OFFLINE831.read_bytes())
'''
src831 = patch831(src831, "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n",
                  "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n" + OFFLINE_HOOK831)

# ---- 3. replace the TEST829 run section by the TEST831 measurement body (inside the original try) ----
start831 = src831.index("    # RUN ORDER: integrity checks")
start831 = src831.rfind("    # ---", 0, start831)
end831 = src831.index("except BaseException as e:\n    D829['status'] = 'ERROR'", start831)
BODY831 = r'''
D829['test'] = '831'
D829['controller'] = 'NONE_DIAGNOSTIC_DESIGNED_PAIRS_NO_SELECTOR_NO_STOPPING'
D829['source829_blob'] = LOCK831_ID
D829['hypotheses831'] = PANEL829['test831']['hypotheses']
D829['limitations'] = [
    'Designed experimenter pairs: a positive result is NOT blind autonomous selection and licenses no stopping.',
    'Physical NULL is a neutral one-card memory, not an empty cache: the locked engine requires >4 body tokens per card and >=1 card per memory; NULL_B robustness is reported.',
    'rho was motivated by TEST830 data; TEST831 is its first confirmatory use (fresh seed, new controls).',
    'Mismatched second links come from other domains; same-domain negatives (mirror, inbound, fork) control the domain-name overlap.',
    'Six worlds x two orders is a small pilot; independent validation requires a new sealed seed.',
    'Final-norm hidden state at one position is a single readout; it is not the multi-token answer.',
    'Offline answer readouts use the TEST827 boundary instruction and are evaluated only after all measurements.',
    'No GPU execution or result is claimed by the code author.']
gate829('SOURCE829_BLOB', True, LOCK831_ID)
gate829('PANEL_FRESH_SEED', SEED829 == SEED831_ID, SEED829)
gate829('NO_CONTROL_TEXT', MAX_NEW_CONTROL829 == 0)
gate829('JOB_COUNT', len(JOBS831) == 33 * WORLDS829, len(JOBS831))
gate829('CASE_COUNT', len(CASES831) == 40 * WORLDS829, len(CASES831))
gate829('JOBS_UNIQUE', len({(tuple(j['ids']), j['qid']) for j in JOBS831}) == len(JOBS831))
gate829('JOB_CARTRIDGES_PHYSICAL', all(c in entries for j in JOBS831 for c in j['ids']))
gate829('PAIRS_TWO_CARDS', all(len(j['ids']) in (1, 2) for j in JOBS831))
# Budgets checked before any measurement.
chunks831 = {c: (int(entries[c]['body_tokens']) + P + CHUNK829 - 1) // CHUNK829 for c in entries}
gate829('ONE_CHUNK_PER_CARD', all(v == 1 for v in chunks831.values()), max(chunks831.values()))
gate829('FUSION_TOKENS_PAIR', max(P + sum(int(entries[c]['body_tokens']) for c in j['ids']) for j in JOBS831) + 64
        <= MAX_FUSED_TOKENS)
try:
    free831, total831 = _torch829.cuda.mem_get_info()
    gate829('VRAM_HEADROOM', free831 / 2**30 >= 8.0, round(free831 / 2**30, 2))
except Exception as e831:
    gate829('VRAM_HEADROOM', False, repr(e831))
predicted831 = {'measurements': len(JOBS831) + 1,
                'fusion_forwards': sum(fusion_forwards829(j['ids']) for j in JOBS831) + fusion_forwards829(JOBS831[0]['ids']),
                'probe_forwards': len(JOBS831) + 1}
D829['predicted_cost831'] = predicted831
log829('TEST831_PREDICTED_COST', json.dumps(predicted831))

D829['noninterference831'] = noninterference829([NULL829], questions829[0]['question'])
for k831, v831 in D829['noninterference831'].items():
    gate829('NONINTERFERENCE_' + k831.upper(), bool(v831), v831)

qtext831 = {q['qid']: q['question'] for q in questions829}      # question text: boundary input only
VEC831 = {}
t831 = time.perf_counter()

def compact831(m):
    lp = m['lp'].detach().to(device='cpu', dtype=_torch829.float64).numpy().copy()
    out = {'h': np.asarray(m['h'], dtype=np.float64).copy(), 'state': np.asarray(m['state'], dtype=np.float64).copy(),
           'lp': lp, 'summary': m['summary'], 'att': m['att']}
    m['lp'] = None; m['lp16'] = None
    return out

for k831, j831 in enumerate(JOBS831):       # sealed shuffled order; opaque IDs only
    VEC831[j831['job']] = compact831(measure829(j831['ids'], qtext831[j831['qid']], j831['job'], 'TEST831_MEASUREMENT'))
    if (k831 + 1) % 33 == 0:
        log829('TEST831_PROGRESS', k831 + 1, '/', len(JOBS831), round(time.perf_counter() - t831, 1), 's')
rep831 = compact831(measure829(JOBS831[0]['ids'], qtext831[JOBS831[0]['qid']], JOBS831[0]['job'] + '_REPLAY',
                               'TEST831_MEASUREMENT'))
D829['determinism831'] = {k: VEC831[JOBS831[0]['job']]['summary'][k] == rep831['summary'][k]
                          for k in ('logits_bf16_sha256', 'final_hidden_sha256', 'state_sha256')}
log829('TEST831_DETERMINISM', json.dumps(D829['determinism831']))
del rep831

def feats831(case, space):
    z0, za, zb, zab = (VEC831[case[k]][space] for k in ('null', 'a', 'b', 'ab'))
    gam = zab - za - zb + z0
    db0 = zb - z0; dba = zab - za; da0 = za - z0
    nb0 = float(np.linalg.norm(db0)); nba = float(np.linalg.norm(dba)); ng = float(np.linalg.norm(gam))
    return {'gamma': ng, 'rho': ng / max(nb0, 1e-300), 'delta_b_given_a': nba, 'delta_b_alone': nb0,
            'delta_a_alone': float(np.linalg.norm(da0)), 'joint': float(np.linalg.norm(zab - z0)),
            'cos_db_given_a_vs_db_alone': float(np.dot(dba, db0) / max(nba * nb0, 1e-300))}

D829['cases831'] = {}
for c831 in CASES831:                       # label-free arithmetic over opaque case structure
    D829['cases831'][c831['case']] = {sp: feats831(c831, sp) for sp in ('h', 'state', 'lp')}
D829['measurement_seconds831'] = round(time.perf_counter() - t831, 3)
save829()

# ---- integrity gates after all numerical measurements ----
engine_bindings829('FINAL')
gate829('FROZEN_WEIGHT_SENTINEL', before829 == sentinel())
gate829('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
gate829('LM_HEAD_UNWRAPPED', model.lm_head.__dict__.get('forward') is HEAD_FWD829 and
        not model.lm_head._forward_hooks and not model.lm_head._forward_pre_hooks)
gate829('PANEL_UNCHANGED', sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True)) == PANEL_SHA829)
for cid831 in cards829:
    gate829('FINAL_SHA_' + cid831, sha_file(CART_DIR / entries[cid831]['file']) == entries[cid831]['sha256'])
cm831 = COST829.get('TEST831_MEASUREMENT', {})
gate829('COUNTED_EQUALS_PREDICTED',
        cm831.get('measurements') == predicted831['measurements'] and
        cm831.get('fusion_forwards') == predicted831['fusion_forwards'] and
        cm831.get('probe_forwards') == predicted831['probe_forwards'],
        {'counted': {k: cm831.get(k) for k in ('measurements', 'fusion_forwards', 'probe_forwards')}})

# ==========================================================================================================
# OFFLINE PHASE BEGINS: every numerical measurement and interaction value above is saved; labels and text
# are used only from here on (answer readouts, then evaluation).
# ==========================================================================================================
# ---- offline answer readouts (text) ----
READOUT_ROLES831 = ('TRUE', 'ALT', 'MIRROR', 'INBOUND', 'FORK')
D829['offline_readouts831'] = []
for wa831, w831 in enumerate(worlds829):
    q831 = questions829[wa831]['question']
    sets831 = [('ANCHOR_ONLY', [w831['ids']['first']])]
    sets831 += [(r, [w831['ids']['first'], w831['ids'][{'TRUE': 'second', 'ALT': 'changed', 'MIRROR': 'mirror',
                                                        'INBOUND': 'decoy', 'FORK': 'fork'}[r]]])
                for r in READOUT_ROLES831]
    for role831, ids831 in sets831:
        o831 = native829(ids831, answer_prompt829(q831), 'T831_RD_' + str(wa831) + '_' + role831, 24)
        D829['offline_readouts831'].append({'row': wa831, 'role': role831, 'text': o831['raw'].strip(),
                                            'tokens': o831['tokens']})
save829()

# ==========================================================================================================
# OFFLINE EVALUATION (labels used only here, after all model calls)
# ==========================================================================================================
def lookup831(row, role, order, nv, b_world=None, space='h'):
    out = []
    for c, k in CASEKEY831.items():
        if k['row'] == row and k['b_role'] == role and k['order'] == order and k['null_variant'] == nv and \
                (b_world is None or k['b_world'] == b_world):
            out.append(D829['cases831'][c][space])
    return out

def column831(true_world, order, nv, space='h'):
    # The SAME true second card of `true_world`, paired with every OTHER anchor/question.
    return [D829['cases831'][c][space] for c, k in CASEKEY831.items()
            if k['b_role'] == 'MISMATCHED_SECOND' and k['b_world'] == true_world and k['order'] == order and
            k['null_variant'] == nv]

def evaluate831(stat, nv, space='h', include_alt=False):
    rows = []
    for wa in range(WORLDS829):
        for order in ('FORWARD', 'REVERSE'):
            t = lookup831(wa, 'TRUE', order, nv, space=space)[0][stat]
            ctrl = {}
            for x in lookup831(wa, 'MISMATCHED_SECOND', order, nv, space=space):
                ctrl.setdefault('ROW_MISMATCHED_SECOND', []).append(x[stat])
            ctrl['COLUMN_SAME_B_OTHER_ANCHOR'] = [x[stat] for x in column831(wa, order, nv, space)]
            for r in ('MIRROR', 'INBOUND', 'FORK') + (('ALT',) if include_alt else ()):
                ctrl[r] = [x[stat] for x in lookup831(wa, r, order, nv, space=space)]
            mx = {k: max(v) for k, v in ctrl.items()}
            beaten = sorted(k for k, v in mx.items() if v >= t)
            rows.append({'row': wa, 'order': order, 'true': t, 'max_control': max(mx.values()),
                         'max_by_control': mx, 'margin': t - max(mx.values()), 'controls_ge_true': beaten,
                         'pass': not beaten})
    return {'all_pass': all(r['pass'] for r in rows), 'passes': sum(r['pass'] for r in rows), 'cases': len(rows),
            'rows': rows}

primary831 = evaluate831('rho', 'A', 'h')
secondary831 = {
    'raw_gamma_hidden_nullA': evaluate831('gamma', 'A', 'h'),
    'rho_hidden_nullB': evaluate831('rho', 'B', 'h'),
    'rho_cut3_nullA': evaluate831('rho', 'A', 'state'),
    'rho_logprob_nullA': evaluate831('rho', 'A', 'lp'),
    'raw_gamma_cut3_nullA': evaluate831('gamma', 'A', 'state'),
    'raw_gamma_logprob_nullA': evaluate831('gamma', 'A', 'lp')}

# ALT valid-chain consistency: ALT must also beat every NEGATIVE control (TRUE excluded).
alt_rows831 = []
for wa in range(WORLDS829):
    for order in ('FORWARD', 'REVERSE'):
        alt = lookup831(wa, 'ALT', order, 'A')[0]['rho']
        negs = ([x['rho'] for x in lookup831(wa, 'MISMATCHED_SECOND', order, 'A')] +
                [x['rho'] for r in ('MIRROR', 'INBOUND', 'FORK') for x in lookup831(wa, r, order, 'A')])
        alt_rows831.append({'row': wa, 'order': order, 'alt': alt, 'max_negative': max(negs), 'pass': alt > max(negs)})
secondary831['alt_consistency_rho'] = {'all_pass': all(r['pass'] for r in alt_rows831),
                                       'passes': sum(r['pass'] for r in alt_rows831), 'rows': alt_rows831}

# Exact column-permutation test on the WxW cross-world matrix (SEASC TEST160-style matched vs shuffled mapping).
perm831 = {}
for stat in ('rho', 'gamma'):
    for order in ('FORWARD', 'REVERSE'):
        M = np.zeros((WORLDS829, WORLDS829))
        for c, k in CASEKEY831.items():
            if k['null_variant'] == 'A' and k['order'] == order and k['b_role'] in ('TRUE', 'MISMATCHED_SECOND'):
                M[k['row'], k['b_world']] = D829['cases831'][c]['h'][stat]
        obs = float(np.trace(M))
        null = [float(sum(M[i, p[i]] for i in range(WORLDS829))) for p in itertools.permutations(range(WORLDS829))]
        perm831[stat + '_' + order] = {'observed_diagonal_sum': obs, 'permutations': len(null),
                                      'p_value_ge': sum(v >= obs for v in null) / len(null),
                                      'matrix_rows_anchor_cols_b': M.round(6).tolist()}
secondary831['column_permutation'] = perm831

# Placement robustness: does the separation exceed the TRUE pair's own order effect?
place831 = []
for wa in range(WORLDS829):
    tf = lookup831(wa, 'TRUE', 'FORWARD', 'A')[0]['rho']; tr = lookup831(wa, 'TRUE', 'REVERSE', 'A')[0]['rho']
    mg = min(r['margin'] for r in primary831['rows'] if r['row'] == wa)
    place831.append({'row': wa, 'min_margin': mg, 'true_order_effect': abs(tf - tr), 'margin_exceeds_order_effect': mg > abs(tf - tr)})
secondary831['placement_robustness'] = place831

# H0a: does raw Gamma simply track the single-effect magnitude of b?
def spearman831(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1]) if len(x) > 2 else None
allA831 = [D829['cases831'][c]['h'] for c, k in CASEKEY831.items() if k['null_variant'] == 'A']
secondary831['H0a_spearman_gamma_vs_single_b'] = spearman831([x['gamma'] for x in allA831], [x['delta_b_alone'] for x in allA831])
secondary831['H0a_spearman_rho_vs_single_b'] = spearman831([x['rho'] for x in allA831], [x['delta_b_alone'] for x in allA831])

# Mechanism summary by role (hidden, NULL_A).
mech831 = {}
for role in ('TRUE', 'ALT', 'MISMATCHED_SECOND', 'MIRROR', 'INBOUND', 'FORK'):
    xs = [D829['cases831'][c]['h'] for c, k in CASEKEY831.items() if k['null_variant'] == 'A' and k['b_role'] == role]
    mech831[role] = {f: [round(float(np.min([x[f] for x in xs])), 4), round(float(np.median([x[f] for x in xs])), 4),
                         round(float(np.max([x[f] for x in xs])), 4)]
                     for f in ('rho', 'gamma', 'delta_b_given_a', 'delta_b_alone', 'cos_db_given_a_vs_db_alone')}
secondary831['mechanism_min_median_max_by_role'] = mech831

# Confound table: token counts and node overlap (computed offline from card texts).
NODES831 = {}                                   # node sets from the sealed panel design (no text parsing)
for w in worlds829:
    for kind, pair in (('first', ('start', 'middle')), ('second', ('middle', 'end')), ('changed', ('middle', 'changed_end')),
                       ('decoy', ('decoy_end', 'start')), ('mirror', ('end', 'middle')), ('fork', ('start', 'fork_end'))):
        NODES831[w['ids'][kind]] = {w[pair[0]], w[pair[1]]}
def nodes831(cid):
    return NODES831.get(cid, set())
conf831 = []
for wa, w in enumerate(worlds829):
    a = w['ids']['first']; qnodes = {w['start']}
    for role, cid in [('TRUE', w['ids']['second']), ('ALT', w['ids']['changed']), ('MIRROR', w['ids']['mirror']),
                      ('INBOUND', w['ids']['decoy']), ('FORK', w['ids']['fork'])] + \
                     [('MISMATCHED_SECOND_w' + str(wb), worlds829[wb]['ids']['second']) for wb in range(WORLDS829) if wb != wa]:
        conf831.append({'row': wa, 'role': role, 'body_tokens': int(entries[cid]['body_tokens']),
                        'anchor_body_tokens': int(entries[a]['body_tokens']),
                        'nodes_shared_with_anchor': len(nodes831(cid) & nodes831(a)),
                        'nodes_shared_with_question': len(nodes831(cid) & qnodes),
                        'same_domain_as_question': card_meta829[cid]['domain'] == w['world']})
secondary831['confound_table'] = conf831
secondary831['token_lengths'] = {'question_tokens': {q['qid']: len(prompt_ids(q['question'])) for q in questions829},
                                 'null_a_tokens': int(entries[NULL829]['body_tokens']),
                                 'null_b_tokens': int(entries[NULLB831]['body_tokens'])}

def classify831(text, w):
    u = (text or '').strip().upper()
    if u.startswith('UNKNOWN'):
        return 'UNKNOWN_PREFIX'
    hits = [(u.rfind(c), r) for r, c in (('END', w['end']), ('MIDDLE', w['middle']), ('ALT_END', w['changed_end']),
                                        ('FORK_END', w['fork_end']), ('START', w['start']), ('DECOY_END', w['decoy_end']))
            if c in u]
    return 'LAST_' + max(hits)[1] if hits else 'NO_CODE'
for r in D829['offline_readouts831']:
    r['class'] = classify831(r['text'], worlds829[r['row']])

verdict831 = 'H1_SUPPORTED_IN_DESIGNED_PILOT' if primary831['all_pass'] else 'H1_FALSIFIED_IN_PILOT'
D829['verdict831'] = {
    'final_question': ('Can two physical memories be distinguished, without the answer key and only from the '
                       'model numerical states, because they complete the relational structure the question '
                       'requires rather than merely changing the output?'),
    'answer': verdict831, 'primary': {k: primary831[k] for k in ('all_pass', 'passes', 'cases')},
    'primary_failures': [r for r in primary831['rows'] if not r['pass']],
    'nullB_consistent': secondary831['rho_hidden_nullB']['all_pass'] == primary831['all_pass'],
    'alt_consistent': secondary831['alt_consistency_rho']['all_pass'],
    'raw_gamma_all_pass': secondary831['raw_gamma_hidden_nullA']['all_pass'],
    'permutation_p': {k: v['p_value_ge'] for k, v in perm831.items()},
    'placement_robust_rows': sum(x['margin_exceeds_order_effect'] for x in place831),
    'determinism_bitwise': all(D829['determinism831'].values()),
    'separate_assessments': {
        'scientific_measurement': 'complete' if all(D829['determinism831'].values()) else 'determinism not bitwise',
        'methodological_integrity': 'gates passed (see checks)',
        'relational_discrimination': verdict831,
        'generalization': 'NOT_ESTABLISHED (six synthetic worlds, one template, one model)',
        'autonomous_control': 'NOT_TESTED (designed pairs; no selector; no stopping)'}}
D829['secondary831'] = secondary831
D829['primary831'] = primary831
D829['cost831'] = {'measured': {k: COST829.get('TEST831_MEASUREMENT', {}).get(k) for k in
                                ('measurements', 'fusion_forwards', 'probe_forwards', 'seconds', 'peak_gpu_gib')},
                   'predicted': predicted831,
                   'offline_readouts': {k: COST829.get('END_OF_RUN_FINAL_READOUT', {}).get(k) for k in
                                        ('fusion_forwards', 'generation_forwards', 'seconds')},
                   'measurement_seconds': D829['measurement_seconds831']}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f831:
    wr831 = csv.DictWriter(f831, fieldnames=['row', 'order', 'stat', 'true', 'max_control', 'margin', 'controls_ge_true', 'pass'])
    wr831.writeheader()
    for stat831, ev831 in (('rho_hidden_nullA_PRIMARY', primary831), ('gamma_hidden_nullA', secondary831['raw_gamma_hidden_nullA']),
                           ('rho_hidden_nullB', secondary831['rho_hidden_nullB'])):
        for r in ev831['rows']:
            wr831.writerow({'row': r['row'], 'order': r['order'], 'stat': stat831, 'true': r['true'],
                           'max_control': r['max_control'], 'margin': r['margin'],
                           'controls_ge_true': ' '.join(r['controls_ge_true']), 'pass': r['pass']})
D829['status'] = 'COMPLETE_DIAGNOSTIC_DESIGNED_PAIRS_NOT_AUTONOMOUS'
save829()
log829('TEST831_PRIMARY', json.dumps({'answer': verdict831, 'passes': primary831['passes'], 'cases': primary831['cases'],
       'rows': [{k: r[k] for k in ('row', 'order', 'true', 'max_control', 'controls_ge_true')} for r in primary831['rows']]}))
log829('TEST831_SECONDARY', json.dumps({k: (v['passes'], v['cases']) for k, v in secondary831.items()
                                        if isinstance(v, dict) and 'passes' in v and 'cases' in v}))
log829('TEST831_ALT', json.dumps({'passes': secondary831['alt_consistency_rho']['passes']}))
log829('TEST831_PERMUTATION', json.dumps({k: v['p_value_ge'] for k, v in perm831.items()}))
log829('TEST831_MECHANISM', json.dumps(mech831))
log829('TEST831_PLACEMENT', json.dumps(place831))
log829('TEST831_H0A', json.dumps({k: secondary831[k] for k in ('H0a_spearman_gamma_vs_single_b', 'H0a_spearman_rho_vs_single_b')}))
log829('TEST831_READOUTS', json.dumps([{k: r[k] for k in ('row', 'role', 'class')} for r in D829['offline_readouts831']]))
log829('TEST831_COST', json.dumps(D829['cost831']))
log829('TEST831_VERDICT', json.dumps({k: v for k, v in D829['verdict831'].items() if k != 'primary_failures'}))
log829('TEST831_COMPLETED', str(OUT829))
'''
BODY831 = BODY831.replace("LOCK831_ID", repr(LOCK831)).replace("SEED831_ID", str(SEED831))
replacement831 = "\n".join("    " + line if line else "" for line in BODY831.strip("\n").splitlines()) + "\n"
patched831 = src831[:start831] + replacement831 + src831[end831:]
ast.parse(patched831)
print('TEST831_SOURCE_LOCK_VERIFIED', LOCK831)
print('TEST831_PATCHED_SOURCE_AST_PASS', len(patched831), hashlib.sha256(patched831.encode()).hexdigest())
exec(compile(patched831, 'TEST831_LOCKED_ENGINE', 'exec'), globals())
