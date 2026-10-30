# AKBASCORE SILICON HIPPOCAMPUS — TEST832, single Colab cell (one A100-SXM4-80GB, frozen Qwen2.5-72B-Instruct NF4).
# BLIND CLOSED-LOOP EVIDENCE DISCOVERY, RELATIONAL CLOSURE, ABSTENTION AND STOPPING FROM NUMERICAL STATES.
# Construction identical to the GPU-completed TEST831 (831.py, git blob ca72fb40...): the SHA-locked TEST829 source
# (blob a5a25460...) is fetched, verified, patched at fixed unique anchors and executed. The locked TEST815 engine
# (native CUT3/H3/KV fusion, physical SSD cartridges, SHA/tensor/KV/weight gates) and the observation-only readout
# are reused unchanged. No training, no residual hooks, no RAG, no source replay, no text-mediated control, no regex.
# Runtime receives ONLY: the question (tokenized at the boundary) and an opaque, shuffled list of physical cartridge
# IDs. It is NOT given the first link, the second link, any pair, the hop count or the stopping step. Every
# measurement the controller makes is chosen by the controller from earlier numerical results.
# ARCHITECTURAL STATEMENT: the controller is a fixed, label-free, parameter-free Python policy that reads the frozen
# model's numerical states. Under the absolute rules (frozen weights, no text control, no hooks, no training) the
# model cannot itself emit memory-selection actions; TEST832 therefore tests NUMERICALLY STATE-DRIVEN closed-loop
# control and proves causal dependence on the model states by interventions. It does not claim model-internal agency.
# No GPU execution or result is claimed by the code author.
import urllib.request, hashlib, ast, json, time, random, math, itertools, numpy as np

URL832 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/829.py"
LOCK832 = "a5a25460a3a6bbdf62a0571a9b5ff19e64159cf7"          # 829.py git blob (TEST830/TEST831 lock)
SEED832 = 8322026
SAFETY_ANCHORS832 = 4         # safety bound on anchor attempts per run; reaching it is a SAFETY EXIT, not success
MEAS_CAP832 = 1000            # global safety bound on unique GPU measurements; reaching it is a SAFETY EXIT

with urllib.request.urlopen(urllib.request.Request(URL832, headers={"User-Agent": "AKBASCORE-TEST832"}), timeout=180) as f832:
    raw832 = f832.read(200001)
blob832 = hashlib.sha1(b"blob " + str(len(raw832)).encode() + b"\0" + raw832).hexdigest()
assert len(raw832) <= 200000 and blob832 == LOCK832, ("STOP_SOURCE_CHANGED", blob832)
src832 = raw832.decode("utf-8")

def patch832(text, old, new):
    assert text.count(old) == 1, ("PATCH_ANCHOR_NOT_UNIQUE", old[:80], text.count(old))
    return text.replace(old, new, 1)

src832 = patch832(src832, "SEED829 = 8292026", "SEED829 = %d" % SEED832)
src832 = patch832(src832, "RUN829 = 'TEST829_'", "RUN829 = 'TEST832_'")
for a832, b832 in (("'TEST829_results.json'", "'TEST832_results.json'"), ("'TEST829.log'", "'TEST832.log'"),
                   ("'TEST829_blind_review.csv'", "'TEST832_run_table.csv'"),
                   ("'TEST829_offline_key.json'", "'TEST829_base_offline_key.json'")):
    src832 = patch832(src832, a832, b832)

# ---------------------------------------------------------------------------------------------------------------
# Panel extension (module level, sealed with the panel SHA BEFORE any model call). New cards use the SAME 'E829_'
# opaque prefix as the base cards, so no ID string distinguishes card kinds.
# Conditions are physical bank interventions by the experimenter (what memory exists), never hints.
# ---------------------------------------------------------------------------------------------------------------
PANEL_EXT832 = r'''
# ---------------- TEST832 PANEL EXTENSION ----------------
NULLB832 = 'E832_NULLB'
cards829[NULLB832] = 'CONTROL MEMORY. This record contains no relation entries.\n'
card_meta829[NULLB832] = {'domain': None, 'kind': 'null_b', 'body_sha256': sha829(cards829[NULLB832])}
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
_rng832 = random.Random(SEED829 + 32)
FULLBANK832 = [w['ids'][k] for w in worlds829 for k in ('first', 'second', 'mirror', 'decoy', 'fork')]
RUNS832, RUNKEY832 = [], {}
for wi, w in enumerate(worlds829):
    for cond in ('FULL', 'MISSING_SECOND', 'CONFLICT_ALT_ADDED', 'REPLACE_SECOND_BY_ALT'):
        bank = list(FULLBANK832)
        if cond in ('MISSING_SECOND', 'REPLACE_SECOND_BY_ALT'):
            bank.remove(w['ids']['second'])
        if cond in ('CONFLICT_ALT_ADDED', 'REPLACE_SECOND_BY_ALT'):
            bank.append(w['ids']['changed'])
        _rng832.shuffle(bank)
        tie = list(bank); _rng832.shuffle(tie)
        rid = 'R832_' + ''.join(_rng832.choice('0123456789ABCDEF') for _ in range(12))
        RUNS832.append({'run': rid, 'qid': questions829[wi]['qid'], 'bank': bank, 'tie_order': tie})
        RUNKEY832[rid] = {'world': wi, 'condition': cond}
_rng832.shuffle(RUNS832)
'''
src832 = patch832(src832,
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n",
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n" + PANEL_EXT832)

HYP832 = {
    'primary_hypothesis_H832': (
        'A fixed, label-free, parameter-free closed-loop policy that reads only final-norm hidden states (one native '
        'forward per mounted set) reaches the correct terminal decision in every sealed run by its OWN closure rule '
        '(not by a safety bound): FULL -> SUFFICIENT with the true first and second links; MISSING_SECOND -> ABSTAIN; '
        'CONFLICT_ALT_ADDED -> CONFLICT naming the two continuations; REPLACE_SECOND_BY_ALT -> SUFFICIENT with the '
        'first link and the alternative link.'),
    'policy': ('1) singles s(c)=||z(c)-z(NULL)|| for every bank card; 2) question-relevant anchors = cards above the '
               'largest log-gap of sorted s (parameter-free); 3) for each anchor a in descending s: rho(a,b) for every b; '
               '4) the row-best b1 is accepted only if a is also the best predecessor of b1 over every other bank card '
               '(mutual-best closure, column null); 5) if b1 closes and the row-runner-up b2 also closes -> CONFLICT; if '
               'only b1 closes -> SUFFICIENT; if b1 does not close -> switch to the next anchor (self-correction); '
               '6) no relevant anchor left -> ABSTAIN. rho(a,b)=||z_ab-z_a-z_b+z_0||/||z_b-z_0||.'),
    'failure_condition': ('H832 is falsified by any wrong terminal decision, any wrong pair, any SUFFICIENT/CONFLICT in a '
                          'MISSING_SECOND run (wrongful stop), or any run ended by a safety bound.'),
    'a_priori_risk': ('TEST831 data: the lexical mirror C->B reached rho 2.21 while TRUE ranged 2.16-2.69. If the mirror '
                      'is mutual-best when B->C is absent, MISSING runs will stop wrongly; that would falsify '
                      '"interaction specificity = relational completion".'),
    'causal_controls': ['bank interventions (4 conditions)', 'same FULL bank, different question (3 worlds)',
                        'CPU replay with relabelled IDs and new listing/tie order (must be invariant)',
                        'CPU replay with the measured states of the selected card and the runner-up swapped (decision must follow the states)'],
    'readout': 'final-norm hidden state (lm_head input) at the last question token; baseline physical NULL card'}

BODY832 = r'''
D829['test'] = '832'
D829['controller'] = 'LABEL_FREE_PARAMETER_FREE_MUTUAL_BEST_CLOSURE_POLICY_ON_FINAL_HIDDEN_STATES'
D829['source829_blob'] = LOCK832_ID
D829['hypotheses832'] = PANEL829['test832']['hypotheses']
D829['limitations'] = [
    'The controller is an external fixed Python policy reading model states; this is state-driven control, not model-internal agency.',
    'Physical NULL is a neutral one-card memory, not an empty cache (locked engine requires >=1 card with >4 body tokens).',
    'Bank conditions are experimenter interventions on which memories physically exist; they are not hints.',
    'Three synthetic worlds, one question template, one model: a pilot, not a generalization test.',
    'The closure rule is pairwise; chains longer than two hops are not tested.',
    'Offline answer readouts use the TEST827 boundary instruction and are produced only after all decisions are saved.',
    'No GPU execution or result is claimed by the code author.']
gate829('SOURCE829_BLOB', True, LOCK832_ID)
gate829('PANEL_FRESH_SEED', SEED829 == SEED832_ID, SEED829)
gate829('NO_CONTROL_TEXT', MAX_NEW_CONTROL829 == 0)
gate829('RUN_COUNT', len(RUNS832) == 4 * len(questions829), len(RUNS832))
gate829('BANK_CARTRIDGES_PHYSICAL', all(c in entries for r in RUNS832 for c in r['bank']))
gate829('BANK_EXCLUDES_NULL', all(NULL829 not in r['bank'] and NULLB832 not in r['bank'] for r in RUNS832))
chunks832 = {c: (int(entries[c]['body_tokens']) + P + CHUNK829 - 1) // CHUNK829 for c in entries}
gate829('ONE_CHUNK_PER_CARD', all(v == 1 for v in chunks832.values()), max(chunks832.values()))
gate829('FUSION_TOKENS_PAIR', P + 2 * max(int(entries[c]['body_tokens']) for c in entries) + 64 <= MAX_FUSED_TOKENS)
try:
    free832, _ = _torch829.cuda.mem_get_info()
    gate829('VRAM_HEADROOM', free832 / 2**30 >= 8.0, round(free832 / 2**30, 2))
except Exception as e832:
    gate829('VRAM_HEADROOM', False, repr(e832))
# Budget: worst case WITHOUT reuse = every run uses every safety anchor with full row and two columns.
K832 = max(len(r['bank']) for r in RUNS832)
ub832 = len(RUNS832) * (1 + K832 + SAFETY_ANCHORS832 * ((K832 - 1) + 2 * (K832 - 2))) + 2
per_run_min832 = 1 + K832 + (K832 - 1) + (K832 - 2)                 # one anchor, row + one column
gate829('MEASUREMENT_CAP_TIME_BUDGET', MEAS_CAP832 * 1.9 / 60.0 <= 45.0, {'cap': MEAS_CAP832, 'minutes_at_1.9s': round(MEAS_CAP832 * 1.9 / 60, 1)})
D829['budget832'] = {'bank_size_max': K832, 'worst_case_measurements_without_reuse': ub832,
                     'one_anchor_run_measurements_without_reuse': per_run_min832, 'cap': MEAS_CAP832,
                     'safety_anchors': SAFETY_ANCHORS832,
                     'note': 'Reaching the cap ends the remaining runs as SAFETY_EXIT (reported as failure, not success).'}
log829('TEST832_BUDGET', json.dumps(D829['budget832']))

D829['noninterference832'] = noninterference829([NULL829], questions829[0]['question'])
for k832, v832 in D829['noninterference832'].items():
    gate829('NONINTERFERENCE_' + k832.upper(), bool(v832), v832)

qtext832 = {q['qid']: q['question'] for q in questions829}      # boundary input only
CACHE832, LEDGER832 = {}, []
STATS832 = {'measured': 0, 'reused': 0}
REUSE832 = {'on': False}

class BudgetExit832(Exception):
    pass

def gpu_measure832(ids, qid, tag):
    if STATS832['measured'] >= MEAS_CAP832:
        raise BudgetExit832()
    m = measure829(list(ids), qtext832[qid], tag, 'TEST832_MEASUREMENT')
    v = {'h': np.asarray(m['h'], dtype=np.float64).copy(), 'summary': m['summary']}
    m['lp'] = None; m['lp16'] = None
    STATS832['measured'] += 1
    LEDGER832.append({'n': STATS832['measured'], 'ids': list(ids), 'qid': qid, 'tag': tag})
    return v

# Determinism check BEFORE any reuse: identical (ids, question) twice must be bitwise identical.
det_a832 = gpu_measure832([RUNS832[0]['bank'][0], RUNS832[0]['bank'][1]], RUNS832[0]['qid'], 'J832_DET_A')
det_b832 = gpu_measure832([RUNS832[0]['bank'][0], RUNS832[0]['bank'][1]], RUNS832[0]['qid'], 'J832_DET_B')
D829['determinism832'] = {k: det_a832['summary'][k] == det_b832['summary'][k]
                          for k in ('logits_bf16_sha256', 'final_hidden_sha256', 'state_sha256')}
REUSE832['on'] = all(D829['determinism832'].values())
if REUSE832['on']:
    CACHE832[(tuple([RUNS832[0]['bank'][0], RUNS832[0]['bank'][1]]), RUNS832[0]['qid'])] = det_a832
log829('TEST832_DETERMINISM', json.dumps(dict(D829['determinism832'], reuse_enabled=REUSE832['on'])))
del det_a832, det_b832

def live_measure832(ids, qid):
    key = (tuple(ids), qid)
    if REUSE832['on'] and key in CACHE832:
        STATS832['reused'] += 1
        return CACHE832[key]
    v = gpu_measure832(ids, qid, 'J832_%05d' % (STATS832['measured'] + 1))
    if REUSE832['on']:
        CACHE832[key] = v
    return v

def gap_count832(values):
    # Parameter-free natural break: cut at the largest log-ratio gap of the descending values (ties -> smaller set).
    v = [max(float(x), 1e-300) for x in values]
    if len(v) < 3:
        return len(v)
    gaps = [math.log(v[j]) - math.log(v[j + 1]) for j in range(len(v) - 1)]
    return 1 + max(range(len(gaps)), key=lambda j: (gaps[j], -j))

def policy832(run, meas):
    """Label-free closed loop. Inputs: question id, opaque bank IDs, a sealed tie order, and a measurement function.
    Every next measurement is chosen from earlier numbers. Returns decision + full numerical trace."""
    qid = run['qid']; bank = list(run['bank']); tie = {c: i for i, c in enumerate(run['tie_order'])}
    trace = []
    def h(ids):
        return meas(ids, qid)['h']
    def rho(a, b, z0):
        za = h([a]); zb = h([b]); zab = h([a, b])
        g = float(np.linalg.norm(zab - za - zb + z0)); nb = float(np.linalg.norm(zb - z0))
        return g / max(nb, 1e-300)
    def done(decision, selected, anchors_tried, stop_kind):
        return {'decision': decision, 'selected': selected, 'anchors_tried': anchors_tried, 'stop_kind': stop_kind,
                'trace': trace}
    tried = []
    try:
        z0 = h([NULL829])
        s = {c: float(np.linalg.norm(h([c]) - z0)) for c in bank}
        order = sorted(bank, key=lambda c: (-s[c], tie[c]))
        m_rel = gap_count832([s[c] for c in order])
        relevant = order[:m_rel]
        trace.append({'event': 'SINGLE_EFFECTS', 'order': order, 'single_effect': [s[c] for c in order],
                      'relevant_anchor_count': m_rel})
        for a in order:
            if a not in relevant:
                trace.append({'event': 'NO_RELEVANT_ANCHOR_LEFT'})
                return done('ABSTAIN', [], tried, 'AUTONOMOUS')
            if len(tried) >= SAFETY_ANCHORS832:
                trace.append({'event': 'SAFETY_ANCHOR_BOUND'})
                return done('SAFETY_EXIT', [], tried, 'SAFETY_ANCHOR_BOUND')
            tried.append(a)
            row = {b: rho(a, b, z0) for b in bank if b != a}
            ranked = sorted(row, key=lambda b: (-row[b], tie[b]))
            b1 = ranked[0]; b2 = ranked[1] if len(ranked) > 1 else None
            col1 = {c: rho(c, b1, z0) for c in bank if c not in (a, b1)}
            best1 = max(col1, key=lambda c: (col1[c], -tie[c])) if col1 else None
            close1 = best1 is None or row[b1] > col1[best1]
            step = {'event': 'ANCHOR_ATTEMPT', 'anchor': a, 'anchor_single_effect': s[a],
                    'row_top5': [(b, row[b]) for b in ranked[:5]], 'b1': b1, 'b1_rho': row[b1],
                    'b1_best_other_predecessor': best1, 'b1_best_other_rho': col1.get(best1), 'b1_closes': close1}
            if close1 and b2 is not None:
                col2 = {c: rho(c, b2, z0) for c in bank if c not in (a, b2)}
                best2 = max(col2, key=lambda c: (col2[c], -tie[c])) if col2 else None
                close2 = best2 is None or row[b2] > col2[best2]
                step.update({'b2': b2, 'b2_rho': row[b2], 'b2_best_other_predecessor': best2,
                             'b2_best_other_rho': col2.get(best2), 'b2_closes': close2})
                trace.append(step)
                if close2:
                    return done('CONFLICT', [a, b1, b2], tried, 'AUTONOMOUS')
                return done('SUFFICIENT', [a, b1], tried, 'AUTONOMOUS')
            if close1:
                trace.append(step)
                return done('SUFFICIENT', [a, b1], tried, 'AUTONOMOUS')
            step['next'] = 'SWITCH_ANCHOR'
            trace.append(step)
        trace.append({'event': 'ALL_ANCHORS_TRIED'})
        return done('ABSTAIN', [], tried, 'AUTONOMOUS')
    except BudgetExit832:
        trace.append({'event': 'SAFETY_MEASUREMENT_BUDGET'})
        return done('SAFETY_EXIT', [], tried, 'SAFETY_MEASUREMENT_BUDGET')

t832 = time.perf_counter()
D829['runs832'] = []
for r832 in RUNS832:                              # sealed shuffled order
    m_before = STATS832['measured']; u_before = STATS832['reused']; t0 = time.perf_counter()
    out832 = policy832(r832, live_measure832)
    out832.update({'run': r832['run'], 'qid': r832['qid'], 'bank_size': len(r832['bank']),
                   'new_measurements': STATS832['measured'] - m_before, 'reused_measurements': STATS832['reused'] - u_before,
                   'seconds': round(time.perf_counter() - t0, 3)})
    D829['runs832'].append(out832)
    save829()
    log829('TEST832_RUN', r832['run'], out832['decision'], out832['stop_kind'], 'anchors', len(out832['anchors_tried']),
           'new', out832['new_measurements'], 'reused', out832['reused_measurements'], 's', out832['seconds'])
D829['policy_seconds832'] = round(time.perf_counter() - t832, 3)

# H3 routing diagnostic (TEST815 locked numeric_rank): computed AFTER all decisions; never used by the policy.
D829['h3_diagnostic832'] = {}
for r832 in RUNS832:
    tr832 = time.perf_counter()
    ranked832, scores832 = numeric_rank(qtext832[r832['qid']], {c: bank829[c] for c in r832['bank']})
    cost829('H3_DIAGNOSTIC', time.perf_counter() - tr832, rank=1)
    D829['h3_diagnostic832'][r832['run']] = ranked832

# ---- integrity gates after all numerical decisions ----
engine_bindings829('FINAL')
gate829('FROZEN_WEIGHT_SENTINEL', before829 == sentinel())
gate829('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
gate829('LM_HEAD_UNWRAPPED', model.lm_head.__dict__.get('forward') is HEAD_FWD829 and
        not model.lm_head._forward_hooks and not model.lm_head._forward_pre_hooks)
gate829('PANEL_UNCHANGED', sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True)) == PANEL_SHA829)
for cid832 in cards829:
    gate829('FINAL_SHA_' + cid832, sha_file(CART_DIR / entries[cid832]['file']) == entries[cid832]['sha256'])
cm832 = COST829.get('TEST832_MEASUREMENT', {})
gate829('COUNTED_EQUALS_LEDGER', cm832.get('measurements') == len(LEDGER832) == STATS832['measured'],
        {'counted': cm832.get('measurements'), 'ledger': len(LEDGER832)})

# ---- CPU-only causal replays over the measured states (no GPU, no new measurement) ----
class MissingReplay832(Exception):
    pass

def cached_measure832(mapping):
    def f(ids, qid):
        key = (tuple(mapping.get(c, c) for c in ids), qid)
        if key not in CACHE832:
            raise MissingReplay832(str(key))
        return CACHE832[key]
    return f

D829['replays832'] = []
rng_rep832 = random.Random(SEED832 + 7)
for r832, o832 in zip(RUNS832, D829['runs832']):
    rec = {'run': r832['run']}
    if not REUSE832['on']:
        rec['status'] = 'SKIPPED_NO_DETERMINISTIC_CACHE'; D829['replays832'].append(rec); continue
    # (1) relabel + new listing + new tie order: decision must be invariant (mapped back).
    lab = {c: 'OPAQUE_%03d' % i for i, c in enumerate(rng_rep832.sample(r832['bank'], len(r832['bank'])))}
    inv = {v: k for k, v in lab.items()}
    bank2 = [lab[c] for c in r832['bank']]; rng_rep832.shuffle(bank2)
    tie2 = list(bank2); rng_rep832.shuffle(tie2)
    try:
        o2 = policy832({'qid': r832['qid'], 'bank': bank2, 'tie_order': tie2}, cached_measure832(inv))
        rec['relabel_decision'] = o2['decision']
        rec['relabel_selected_mapped_back'] = [inv[c] for c in o2['selected']]
        rec['relabel_invariant'] = (o2['decision'] == o832['decision'] and
                                    rec['relabel_selected_mapped_back'] == o832['selected'])
    except MissingReplay832 as e:
        rec['relabel_invariant'] = None; rec['relabel_missing'] = str(e)
    # (2) state swap: the selected continuation and the row runner-up exchange ALL their measured states.
    last = [t for t in o832['trace'] if t.get('event') == 'ANCHOR_ATTEMPT']
    if o832['decision'] in ('SUFFICIENT', 'CONFLICT') and last and last[-1].get('b2'):
        b1, b2 = last[-1]['b1'], last[-1]['b2']
        try:
            o3 = policy832(r832, cached_measure832({b1: b2, b2: b1}))
            rec['swap_pair'] = [b1, b2]
            rec['swap_decision'] = o3['decision']; rec['swap_selected'] = o3['selected']
            rec['swap_follows_states'] = (o832['decision'] == 'SUFFICIENT' and o3['decision'] == 'SUFFICIENT' and
                                          o3['selected'][1:] == [b2]) or (o832['decision'] == 'CONFLICT' and o3['decision'] == 'CONFLICT')
        except MissingReplay832 as e:
            rec['swap_follows_states'] = None; rec['swap_missing'] = str(e)
    D829['replays832'].append(rec)

# ==========================================================================================================
# OFFLINE PHASE: all decisions, traces and replays are saved; labels and text are used only from here on.
# ==========================================================================================================
D829['offline_readouts832'] = []
for r832, o832 in zip(RUNS832, D829['runs832']):
    if o832['selected']:
        q832 = qtext832[r832['qid']]
        ro832 = native829(list(o832['selected']), answer_prompt829(q832), 'T832_RD_' + r832['run'], 24)
        D829['offline_readouts832'].append({'run': r832['run'], 'text': ro832['raw'].strip(), 'tokens': ro832['tokens']})
save829()

KIND832 = {cid: m['kind'] for cid, m in card_meta829.items()}
DOM832 = {cid: m['domain'] for cid, m in card_meta829.items()}
def role832(cid, w):
    return ('OWN_' if DOM832.get(cid) == w['world'] else 'OTHER_') + str(KIND832.get(cid)).upper()
EXPECT832 = {'FULL': ('SUFFICIENT', ['OWN_FIRST', 'OWN_SECOND']), 'MISSING_SECOND': ('ABSTAIN', []),
             'CONFLICT_ALT_ADDED': ('CONFLICT', ['OWN_FIRST', 'OWN_SECOND', 'OWN_CHANGED']),
             'REPLACE_SECOND_BY_ALT': ('SUFFICIENT', ['OWN_FIRST', 'OWN_CHANGED'])}
eval832 = []
for r832, o832 in zip(RUNS832, D829['runs832']):
    key = RUNKEY832[r832['run']]; w = worlds829[key['world']]
    exp_dec, exp_roles = EXPECT832[key['condition']]
    sel_roles = [role832(c, w) for c in o832['selected']]
    tried_roles = [role832(c, w) for c in o832['anchors_tried']]
    ok_pair = (sel_roles[:1] == exp_roles[:1] and sorted(sel_roles[1:]) == sorted(exp_roles[1:])) if exp_roles else sel_roles == []
    att = [t for t in o832['trace'] if t.get('event') == 'ANCHOR_ATTEMPT']
    h3 = D829['h3_diagnostic832'][r832['run']]
    rec = {'run': r832['run'], 'world': key['world'], 'condition': key['condition'], 'expected': exp_dec,
           'decision': o832['decision'], 'stop_kind': o832['stop_kind'], 'selected_roles': sel_roles,
           'anchors_tried_roles': tried_roles, 'decision_correct': o832['decision'] == exp_dec,
           'pair_correct': ok_pair, 'correct': o832['decision'] == exp_dec and ok_pair,
           'first_evidence_found_independently': 'OWN_FIRST' in sel_roles[:1],
           'first_anchor_tried_was_own_first': tried_roles[:1] == ['OWN_FIRST'],
           'second_evidence_found_independently': any(x in sel_roles[1:] for x in ('OWN_SECOND', 'OWN_CHANGED')),
           'self_correction': len(tried_roles) > 1 and o832['decision'] == exp_dec and ok_pair,
           'anchor_switches': max(len(tried_roles) - 1, 0),
           'wrongful_stop': key['condition'] == 'MISSING_SECOND' and o832['decision'] in ('SUFFICIENT', 'CONFLICT'),
           'false_conflict': key['condition'] != 'CONFLICT_ALT_ADDED' and o832['decision'] == 'CONFLICT',
           'row_top5_roles_per_attempt': [[(role832(b, w), round(v, 4)) for b, v in t['row_top5']] for t in att],
           'closure_competitor_roles': [(role832(t['b1'], w), t['b1_closes'], role832(t['b1_best_other_predecessor'], w)
                                         if t.get('b1_best_other_predecessor') else None) for t in att],
           'h3_rank_own_first': next((i + 1 for i, c in enumerate(h3) if role832(c, w) == 'OWN_FIRST'), None),
           'h3_rank_own_second': next((i + 1 for i, c in enumerate(h3) if role832(c, w) == 'OWN_SECOND'), None),
           'new_measurements': o832['new_measurements'], 'reused_measurements': o832['reused_measurements']}
    rd = next((x for x in D829['offline_readouts832'] if x['run'] == r832['run']), None)
    if rd:
        u = rd['text'].upper()
        rec['readout_text'] = rd['text']
        rec['readout_mentions'] = [n for n, c in (('END', w['end']), ('MIDDLE', w['middle']), ('ALT_END', w['changed_end']),
                                                  ('FORK_END', w['fork_end'])) if c in u] + (['UNKNOWN'] if 'UNKNOWN' in u else [])
    eval832.append(rec)
D829['offline_eval832'] = eval832

def frac832(xs):
    return [sum(1 for x in xs if x), len(xs)]
by_cond = {c: [e for e in eval832 if e['condition'] == c] for c in EXPECT832}
reps = D829['replays832']
D829['report832'] = {
    'first_evidence_independent_discovery': frac832([e['first_evidence_found_independently'] for e in eval832
                                                     if e['condition'] != 'MISSING_SECOND']),
    'second_evidence_independent_discovery': frac832([e['second_evidence_found_independently'] for e in eval832
                                                      if e['condition'] != 'MISSING_SECOND']),
    'relational_integrity_correct_pairs': frac832([e['pair_correct'] for e in eval832 if e['condition'] != 'MISSING_SECOND']),
    'incomplete_evidence_recognised_abstain': frac832([e['decision'] == 'ABSTAIN' for e in by_cond['MISSING_SECOND']]),
    'conflict_recognised': frac832([e['decision'] == 'CONFLICT' for e in by_cond['CONFLICT_ALT_ADDED']]),
    'alternative_chain_accepted': frac832([e['correct'] for e in by_cond['REPLACE_SECOND_BY_ALT']]),
    'self_correction_after_wrong_first_anchor': frac832([e['self_correction'] for e in eval832 if e['anchor_switches'] > 0]),
    'recursive_steps_numerically_driven': {'runs_with_anchor_switch': sum(e['anchor_switches'] > 0 for e in eval832),
                                           'total_anchor_attempts': sum(len(e['anchors_tried_roles']) for e in eval832)},
    'autonomous_stops': sum(e['stop_kind'] == 'AUTONOMOUS' for e in eval832),
    'safety_exits': sum(e['stop_kind'] != 'AUTONOMOUS' for e in eval832),
    'false_positives': {'wrongful_stops_on_missing': sum(e['wrongful_stop'] for e in eval832),
                        'false_conflicts': sum(e['false_conflict'] for e in eval832),
                        'sufficient_with_wrong_pair': sum(e['decision'] == 'SUFFICIENT' and not e['pair_correct'] for e in eval832)},
    'interventions': {
        'bank_condition_changes_decision_per_world': {w: sorted(set(e['decision'] for e in eval832 if e['world'] == w))
                                                      for w in range(len(worlds829))},
        'same_full_bank_different_question_selects_own_world': frac832([e['correct'] for e in by_cond['FULL']]),
        'relabel_listing_invariant': frac832([x.get('relabel_invariant') is True for x in reps]),
        'state_swap_decision_follows_states': frac832([x.get('swap_follows_states') is True for x in reps if 'swap_pair' in x])},
    'integrity': {'determinism_bitwise': all(D829['determinism832'].values()), 'gates': 'all passed (run reached evaluation)'},
    'h3_routing_diagnostic_own_first_in_top2': frac832([(e['h3_rank_own_first'] or 99) <= 2 for e in eval832])}
H832 = all(e['correct'] and e['stop_kind'] == 'AUTONOMOUS' for e in eval832)
D829['verdict832'] = {
    'question': ('Can numerical states of a frozen model, produced from physical memory cartridges, govern the '
                 "system's own evidence search and stopping without an answer key or textual control?"),
    'H832': 'SUPPORTED_IN_PILOT' if H832 else 'FALSIFIED_IN_PILOT',
    'correct_runs': frac832([e['correct'] for e in eval832]),
    'failed_runs': [{k: e[k] for k in ('world', 'condition', 'expected', 'decision', 'stop_kind', 'selected_roles',
                                       'anchors_tried_roles', 'closure_competitor_roles')} for e in eval832 if not e['correct']],
    'mechanism_statement': ('Decisions are produced by a fixed external policy; their content is caused by the model '
                            'states (see state-swap and bank/question interventions). This is not model-internal agency.')}
D829['cost832'] = {'unique_gpu_measurements': STATS832['measured'], 'reused_measurements': STATS832['reused'],
                   'upper_bound': ub832, 'policy_seconds': D829['policy_seconds832'],
                   'measurement': {k: cm832.get(k) for k in ('measurements', 'fusion_forwards', 'probe_forwards', 'seconds', 'peak_gpu_gib')},
                   'h3_diagnostic': COST829.get('H3_DIAGNOSTIC'), 'offline_readouts': COST829.get('END_OF_RUN_FINAL_READOUT'),
                   'noninterference': COST829.get('NONINTERFERENCE_CHECK')}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f832:
    wr832 = csv.DictWriter(f832, fieldnames=['world', 'condition', 'expected', 'decision', 'stop_kind', 'selected_roles',
                                             'anchors_tried_roles', 'correct', 'readout_text'])
    wr832.writeheader()
    for e in eval832:
        wr832.writerow({k: (' '.join(e[k]) if isinstance(e.get(k), list) else e.get(k, '')) for k in
                        ('world', 'condition', 'expected', 'decision', 'stop_kind', 'selected_roles',
                         'anchors_tried_roles', 'correct', 'readout_text')})
D829['status'] = 'COMPLETE_CLOSED_LOOP_PILOT_EVALUATED'
save829()
log829('TEST832_EVAL', json.dumps([{k: e[k] for k in ('world', 'condition', 'decision', 'stop_kind', 'selected_roles',
                                                       'anchors_tried_roles', 'correct')} for e in eval832]))
log829('TEST832_TRACE_ROLES', json.dumps([{'w': e['world'], 'c': e['condition'], 'rows': e['row_top5_roles_per_attempt'],
                                           'closure': e['closure_competitor_roles']} for e in eval832]))
log829('TEST832_REPORT', json.dumps(D829['report832']))
log829('TEST832_REPLAYS', json.dumps(D829['replays832']))
log829('TEST832_COST', json.dumps(D829['cost832']))
log829('TEST832_VERDICT', json.dumps(D829['verdict832']))
log829('TEST832_COMPLETED', str(OUT829))
'''
BODY_SHA832 = hashlib.sha256(BODY832.encode()).hexdigest()
PANEL_HOOK832 = ("PANEL829['test832'] = {'runs': RUNS832, 'hypotheses': %r, 'policy_body_sha256': %r, "
                 "'safety_anchors': %d, 'measurement_cap': %d, 'seed': SEED829}\n"
                 % (HYP832, BODY_SHA832, SAFETY_ANCHORS832, MEAS_CAP832))
src832 = patch832(src832, "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))",
                  PANEL_HOOK832 + "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))")
OFFLINE_HOOK832 = r'''
OFFLINE832 = DIR829 / 'TEST832_offline_key.json'   # never read by any runtime computation
OFFLINE832.write_text(json.dumps({'note': 'OFFLINE ONLY — run conditions and card kinds', 'runs': RUNKEY832,
                                  'worlds': worlds829, 'questions': questions829, 'card_meta': card_meta829},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D829['offline_key832_sha256'] = sha829(OFFLINE832.read_bytes())
'''
src832 = patch832(src832, "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n",
                  "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n" + OFFLINE_HOOK832)
start832 = src832.index("    # RUN ORDER: integrity checks")
start832 = src832.rfind("    # ---", 0, start832)
end832 = src832.index("except BaseException as e:\n    D829['status'] = 'ERROR'", start832)
body832 = BODY832.replace("LOCK832_ID", repr(LOCK832)).replace("SEED832_ID", str(SEED832))
replacement832 = "\n".join("    " + line if line else "" for line in body832.strip("\n").splitlines()) + "\n"
patched832 = src832[:start832] + replacement832 + src832[end832:]
ast.parse(patched832)
print('TEST832_SOURCE_LOCK_VERIFIED', LOCK832)
print('TEST832_POLICY_BODY_SHA256', BODY_SHA832)
print('TEST832_PATCHED_SOURCE_AST_PASS', len(patched832), hashlib.sha256(patched832.encode()).hexdigest())
exec(compile(patched832, 'TEST832_LOCKED_ENGINE', 'exec'), globals())
