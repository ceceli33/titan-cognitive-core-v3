import urllib.request, hashlib, ast, json, time

BASE847_URL = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/846.py"
BASE847_BLOB = "6093896b7e4492f201cece448ad1646b0bd8820a"
req847 = urllib.request.Request(BASE847_URL, headers={"User-Agent": "AKBASCORE-TEST847"})
with urllib.request.urlopen(req847, timeout=180) as response:
    raw847 = response.read(1000001)

blob847 = hashlib.sha1(
    b"blob " + str(len(raw847)).encode() + b"\0" + raw847
).hexdigest()
assert blob847 == BASE847_BLOB, ("TEST846_SOURCE_LOCK_FAILED", blob847, BASE847_BLOB)
SRC847 = raw847.decode("utf-8")

def replace_top_assignment847(source, name, expr):
    tree = ast.parse(source)
    candidates = [
        n for n in tree.body
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)
    ]
    if name == "PANEL846":
        candidates = [
            n for n in candidates
            if isinstance(n.value, ast.BinOp)
            and isinstance(n.value.op, ast.Add)
            and isinstance(n.value.left, ast.Name)
            and n.value.left.id == "PANEL_FACTORY846"
        ]
    assert len(candidates) == 1, (
        "ASSIGNMENT_NOT_UNIQUE",
        name,
        len(candidates),
        [(n.lineno, ast.unparse(n.value)[:100]) for n in candidates]
    )
    node = candidates[0]
    lines = source.splitlines(keepends=True)
    lines[node.lineno - 1:node.end_lineno] = [name + " = " + expr + "\n"]
    result = "".join(lines)
    ast.parse(result)
    return result

PANEL_TAIL847 = r'''
PILOT_WORLDS846 = (0, 1, 2)
PILOT_STARTS846 = ('INTACT', 'CONFLICT', 'REMOVED')
PILOT_ARMS846 = ('MODEL_STATE', 'MATCHED_CONTROL', 'CUE_BASELINE')
STARTS41R = PILOT_STARTS846
ARMS41R = PILOT_ARMS846
JARMS845 = PILOT_ARMS846
DCONDS845 = ()

for arm in PILOT_ARMS846:
    for wi in PILOT_WORLDS846:
        w = worlds829[wi]
        ids = w['ids']
        B = BANKS841[BLOCKOF841[wi]]
        for intervention in PILOT_STARTS846:
            initial = []
            drop = ()
            if intervention == 'CONFLICT':
                initial = [ids['fork']]
                drop = (ids['fork'],)
            elif intervention == 'REMOVED':
                drop = (ids['second'], ids['changed'])

            bank = [c for c in B['v0'] if c not in drop]
            qid = QID841[wi]
            job41r(
                qid,
                {'world': wi, 'cond': intervention, 'arm': arm},
                bank,
                arm,
                [],
                None
            )
            JOBS841[-1]['intervention'] = intervention
            JOBS841[-1]['initial_cards'] = list(initial)

assert len(JOBS841) == 27
assert len({j['job'] for j in JOBS841}) == 27
assert JOBS841 and JOBS841[0]['bank']
# Legacy TEST841 preflight fixture selects a physical card from this field.
# The TEST847 experimental loop starts from initial_cards, not this fixture.
JOBS841[0]['start'] = [JOBS841[0]['bank'][0]]
'''

RUN847 = r'''
HMAX847 = 30
FR845['start'] = (
    'Question: {q}\n'
    'Name the start node of the question. Reply with the node name only.'
)
START_SLOT847 = list(tok('Start node:', add_special_tokens=False).input_ids)
ROOT_CACHE847 = {}
ROOT_STATE847 = {}
MATCHED_STATE847 = {}
PLAN_CACHE847 = {}

def start_state847(q):
    if q not in ROOT_CACHE847:
        pre = list(prompt_ids(FR845['start'].format(q=QTEXT841[q]))) + START_SLOT847
        ROOT_CACHE847[q] = gen845(MEMNULL841, pre, None, None)
    return ROOT_CACHE847[q]

def match_rows847(target, donor):
    target = target.detach().float().cpu()
    donor = donor.detach().float().cpu()
    assert target.ndim == 2 and target.shape[1] == H
    assert target.shape[0] > 0, ("EMPTY_MODEL_STATE", tuple(target.shape))

    n = int(target.shape[0])
    if donor.ndim != 2 or donor.shape[1] != H or donor.shape[0] == 0:
        donor = MUE845.float().cpu().reshape(1, H)

    indices = torch.arange(n) % int(donor.shape[0])
    rows = donor.index_select(0, indices).clone()
    target_norm = torch.linalg.vector_norm(target, dim=1, keepdim=True)
    donor_norm = torch.linalg.vector_norm(rows, dim=1, keepdim=True)

    fallback = MUE845.float().cpu().reshape(1, H).expand(n, -1).clone()
    fallback_norm = torch.linalg.vector_norm(fallback, dim=1, keepdim=True)
    assert bool(torch.all(fallback_norm > 1e-12)), "MATCHED_CONTROL_FALLBACK_ZERO"
    fallback = fallback / fallback_norm.clamp_min(1e-12)

    rows = rows / donor_norm.clamp_min(1e-12)
    rows = torch.where(donor_norm > 1e-12, rows, fallback)
    matched = (rows * target_norm).contiguous()

    out_norm = torch.linalg.vector_norm(matched, dim=1)
    assert tuple(matched.shape) == tuple(target.shape), (
        "MATCHED_CONTROL_SHAPE", tuple(matched.shape), tuple(target.shape)
    )
    assert bool(torch.allclose(
        out_norm, target_norm.reshape(-1), atol=1e-5, rtol=1e-5
    )), (
        "MATCHED_CONTROL_NORM_MISMATCH",
        float((out_norm - target_norm.reshape(-1)).abs().max())
    )
    return matched

def state_for847(arm, q):
    if arm == 'CUE_BASELINE':
        return None
    if arm == 'MODEL_STATE':
        return ROOT_STATE847[q]
    if arm == 'MATCHED_CONTROL':
        return MATCHED_STATE847[q]
    raise ValueError(("UNKNOWN_ARM", arm))

def hop847(q, mem, k, rows, arm):
    if k == 0 and arm == 'CUE_BASELINE':
        return hop845(q, mem, 0, None)
    return hop845(q, mem, 1, rows)

def attribute847(q, mem, k, path, root, arm):
    used = {p['evid'] for p in path if p['evid'] is not None}
    rows = root if k == 0 else path[k-1]['rows']
    original = path[k]['text'].strip()
    original_mem = list(path[k]['mem'])
    fallback = None

    for i, card in enumerate(original_mem):
        if card in used or card not in mem:
            continue
        counterfactual = list(original_mem)
        counterfactual[i] = NULL829
        h = hop847(q, counterfactual, k, rows, arm)
        if h['unk']:
            return card, 'COUNTERFACTUAL_UNKNOWN'
        if fallback is None and h['text'].strip() != original:
            fallback = card

    if fallback is not None:
        return fallback, 'COUNTERFACTUAL_OUTPUT_CHANGE'
    return None, 'NO_COUNTERFACTUAL_ATTRIBUTION'

def plan847(q):
    if q not in PLAN_CACHE847:
        PLAN_CACHE847[q] = plan845(q)
    return PLAN_CACHE847[q]

def loop847(j):
    q = j['qid']
    arm = j['arm']
    intervention = j['intervention']
    bank = list(j['bank'])
    mem = list(j['initial_cards'])
    assert len(mem) < CAP845, ("INITIAL_CAPACITY", j['job'], len(mem), CAP845)

    root = state_for847(arm, q)
    plan = plan847(q)
    N = plan['N']

    path = []
    steps = []
    excluded = []
    excluded_by_state = {}
    tries = {}
    seen = set()
    pending = None
    hops = 0
    mechanical_dead_ends = 0
    end = 'PLAN_INVALID' if N is None else None
    mounts0 = CNT_R41['mounts']
    t0 = time.perf_counter()

    while end is None:
        k = len(path)
        if k == N:
            end = 'PATH_COMPLETE'
            break
        if hops >= HMAX847:
            end = 'BUDGET_STOP'
            break

        rows = root if k == 0 else path[k-1]['rows']
        state_id = (
            'ROOT_CUE'
            if k == 0 and arm == 'CUE_BASELINE'
            else rkey845(rows)
        )
        local_exclusions = excluded_by_state.setdefault(state_id, [])
        control_key = (
            k,
            key_r41(mem),
            state_id,
            tuple(sorted(local_exclusions)),
            tries.get(k, 0)
        )
        if control_key in seen:
            end = 'NO_NEW_INFORMATION'
            break
        seen.add(control_key)

        before = list(mem)
        h = hop847(q, mem, k, rows, arm)
        hops += 1
        step = {
            'k': k,
            'mem': before,
            'out': h['text'],
            'unk': h['unk'],
            'dec': None,
            'state': str(state_id)
        }

        if not h['unk']:
            path.append({
                'rows': h['rows'],
                'text': h['text'],
                'evid': pending,
                'mem': before
            })
            pending = None
            tries[k+1] = 0
            step['dec'] = 'ADVANCE'
        else:
            if pending is not None:
                if pending in mem:
                    mem.remove(pending)
                excluded.append(pending)
                local_exclusions.append(pending)
                step['unmounted'] = pending
                pending = None

            candidate = None
            reason = None
            if tries.get(k, 0) >= SMAX845:
                reason = 'S_EXHAUSTED'
            elif len(mem) >= CAP845:
                reason = 'CAPACITY'
            else:
                address_rows = None if k == 0 and arm == 'CUE_BASELINE' else rows
                candidate = addr845(q, mem, address_rows, bank, local_exclusions)
                if candidate is None:
                    reason = 'NO_CANDIDATE'

            if candidate is not None:
                card = candidate['chosen']
                assert card in bank and card not in mem, ("BAD_MOUNT", j['job'], card)
                mem.append(card)
                pending = card
                tries[k] = tries.get(k, 0) + 1
                step.update({
                    'dec': 'SEARCH',
                    'cand': card,
                    'try': tries[k],
                    'via': candidate.get('via'),
                    'margin': candidate.get('margin'),
                    'n_cand': candidate.get('n_cand')
                })
            else:
                step['why'] = reason
                step['python_stop_trigger'] = reason
                if reason != 'S_EXHAUSTED':
                    mechanical_dead_ends += 1

                if k == 0:
                    end = {
                        'S_EXHAUSTED': 'ABSTAIN',
                        'CAPACITY': 'CAPACITY_STOP',
                        'NO_CANDIDATE': 'BANK_EXHAUSTED'
                    }[reason]
                    step['dec'] = 'ABSTAIN' if end == 'ABSTAIN' else 'MECH_STOP'
                else:
                    previous = path[k-1]
                    if previous['evid'] is not None:
                        evidence = previous['evid']
                        basis = 'PREVIOUSLY_MOUNTED_CARD'
                    else:
                        evidence, basis = attribute847(q, mem, k-1, path, root, arm)

                    previous_rows = root if k == 1 else path[k-2]['rows']
                    previous_state = (
                        'ROOT_CUE'
                        if k == 1 and arm == 'CUE_BASELINE'
                        else rkey845(previous_rows)
                    )
                    if evidence is not None and evidence in mem:
                        mem.remove(evidence)
                        excluded.append(evidence)
                        excluded_by_state.setdefault(previous_state, []).append(evidence)
                        step['retracted'] = evidence
                        step['retraction_basis'] = basis

                    path.pop()
                    tries[k-1] = 0
                    tries[k] = 0
                    step['dec'] = 'DEAD_END_BACKTRACK'

        steps.append(step)
        say_r41(
            'TEST847_HOP',
            j['job'],
            arm,
            intervention,
            'k=%d' % k,
            'OUT=%r' % h['text'][:24],
            'DEC=' + str(step['dec'])
        )

    pointer = (
        path[-1]['text']
        if end == 'PATH_COMPLETE'
        else 'UNKNOWN'
        if end == 'ABSTAIN'
        else None
    )
    frame_answer = answer_r41(q, mem)
    path_trace = [
        {'text': p['text'], 'evid': p['evid'], 'mem': list(p['mem'])}
        for p in path
    ]
    first_selected = (
        j['initial_cards'][0]
        if j['initial_cards']
        else next((s['cand'] for s in steps if 'cand' in s), None)
    )

    record = {
        'job': j['job'],
        'qid': q,
        'arm': arm,
        'intervention': intervention,
        'steps': steps,
        'path_trace': path_trace,
        'end': end,
        'pointer_answer': pointer,
        'answer_raw': frame_answer,
        'plan': plan,
        'first_selected_card': first_selected,
        'initial_cards': list(j['initial_cards']),
        'final_mounted': list(mem),
        'excluded': excluded,
        'hops': hops,
        'mounts': CNT_R41['mounts'] - mounts0,
        'seconds': round(time.perf_counter() - t0, 2),
        'mechanical_dead_ends': mechanical_dead_ends,
        'root_rows': int(root.shape[0]) if root is not None else 0,
        'root_state_sha1': rkey845(root) if root is not None else None
    }
    return record, {}

assert len(JOBS841) == 27
assert set(j['arm'] for j in JOBS841) == set(PILOT_ARMS846)
assert set(j['intervention'] for j in JOBS841) == set(PILOT_STARTS846)

QIDS847 = list(dict.fromkeys(j['qid'] for j in JOBS841))
assert len(QIDS847) == 3, ("EXPECTED_THREE_FIXED_QIDS", QIDS847)

for q in QIDS847:
    rows = start_state847(q)['rows'].detach().float().cpu()
    assert rows.ndim == 2 and rows.shape[0] > 0 and rows.shape[1] == H, (
        "ROOT_STATE_PREFLIGHT_FAILED", q, tuple(rows.shape)
    )
    ROOT_STATE847[q] = rows.contiguous()

DONOR_QID847 = {
    q: QIDS847[(i + 1) % len(QIDS847)]
    for i, q in enumerate(QIDS847)
}
for q in QIDS847:
    MATCHED_STATE847[q] = match_rows847(
        ROOT_STATE847[q],
        ROOT_STATE847[DONOR_QID847[q]]
    )
    assert tuple(MATCHED_STATE847[q].shape) == tuple(ROOT_STATE847[q].shape)
    norm_error = float((
        torch.linalg.vector_norm(MATCHED_STATE847[q], dim=1)
        - torch.linalg.vector_norm(ROOT_STATE847[q], dim=1)
    ).abs().max())
    say_r41(
        'TEST847_ROOT_STATE',
        q,
        'MODEL_ROWS=%s' % (tuple(ROOT_STATE847[q].shape),),
        'DONOR_QID=%s' % DONOR_QID847[q],
        'MATCHED_NORM_MAXERR=%.8g' % norm_error
    )

gate829(
    'TEST847_ROOT_STATES_NONEMPTY_AND_MATCHED',
    len(ROOT_STATE847) == 3
    and all(ROOT_STATE847[q].shape[0] > 0 for q in QIDS847)
    and all(MATCHED_STATE847[q].shape == ROOT_STATE847[q].shape for q in QIDS847),
    {q: list(ROOT_STATE847[q].shape) for q in QIDS847}
)

say_r41('TEST847 PRE-REGISTERED HYPOTHESES')
say_r41(
    'H1_PRIMARY',
    'Across six INTACT/CONFLICT pairs, MODEL_STATE must exceed MATCHED_CONTROL '
    'by at least 2 grounded correct outcomes.'
)
say_r41(
    'H1_CORRECTION',
    'A correction event requires a wrong intermediate, counterfactual evidence re-evaluation, '
    'retraction, then a physically grounded correct two-link answer.'
)
say_r41(
    'H1_REMOVED',
    'REMOVED has no searchable second/changed evidence. An ABSTAIN after S_EXHAUSTED '
    'is a mechanical stop, not a model-native stop.'
)
say_r41(
    'TEST847 EXPERIMENTAL PANEL',
    '3 fixed existing worlds x 3 arms x 3 interventions = 27 jobs; S=%d HMAX=%d CAP=%d'
    % (SMAX845, HMAX847, CAP845)
)
say_r41('CONTROL_DONOR_MAP', json.dumps(DONOR_QID847, sort_keys=True))

UPPER_CHECK841 = {}
t_run841 = time.perf_counter()
nj846 = len(JOBS841)
BUDGET_STOP841 = False
log829('TEST847_PROGRESS', 0, '/', nj846)

for ji846, j846 in enumerate(JOBS841):
    if j846['job'] not in REC841:
        elapsed_minutes = (time.perf_counter() - T0_841) / 60.0
        if elapsed_minutes > HARD_BUDGET_MIN841:
            BUDGET_STOP841 = True
            log829('TEST847_BUDGET_STOP', ji846, nj846)
            break
        try:
            if not UPPER_CHECK841:
                with CallCount841() as cc847:
                    rec847, rows847 = loop847(j846)
                UPPER_CHECK841 = cc847.summary()
                gate829(
                    'CUT3_UPPER_LAYER_EXECUTION',
                    UPPER_CHECK841['upper_min'] >= 1 and UPPER_CHECK841['lm_head'] >= 1,
                    UPPER_CHECK841
                )
            else:
                rec847, rows847 = loop847(j846)
        except BudgetR41 as err847:
            BUDGET_STOP841 = True
            log829('TEST847_BUDGET_STOP', str(err847), ji846, nj846)
            break

        REC841[j846['job']] = rec847
        ROWS841[j846['job']] = rows847
        save_job841(j846['job'], rec847, rows847)

    log829(
        'TEST847_PROGRESS',
        ji846 + 1,
        '/',
        nj846,
        j846['arm'],
        j846['intervention']
    )

while LRU_R41:
    evict_r41()

D829['run_seconds841'] = round(time.perf_counter() - t_run841, 3)
D829['memo841R'] = dict(
    CNT_R41,
    states=len(SIG_R41),
    echo_states=len(ECHO_R41),
    hop=CNT845['hop'],
    hop_hit=CNT845['hop_hit']
)
'''

OFF847 = r'''
log829('TEST847_OFFLINE_START')

def node_class847(text, w):
    u = (text or '').upper()
    keys = (
        'start', 'middle', 'end', 'changed_end', 'end3',
        'fork_end', 'decoy_end', 'bridge_mid', 'bridge_end'
    )
    hits = [
        k for k in keys
        if str(w.get(k, '')).upper() and str(w[k]).upper() in u
    ]
    return hits[0] if len(hits) == 1 else ('AMBIGUOUS' if len(hits) > 1 else 'OTHER')

def card_source847(cid, wi, w):
    if cid not in CONTENT841:
        return None
    cw, kind, _version = CONTENT841[cid]
    if cw != wi or kind not in REL841:
        return None
    return w.get(REL841[kind][0])

PILOT_RESULTS847 = []
SUMMARY847 = {}

for j in JOBS841:
    if j['job'] not in REC841:
        continue

    r = REC841[j['job']]
    wi = QID841.index(j['qid'])
    w = worlds829[wi]
    ids = w['ids']
    intervention = j['intervention']
    arm = j['arm']
    trace = r['path_trace']
    answer_cat = node_class847(r['pointer_answer'], w) if r['pointer_answer'] else None
    grounded = False

    if intervention in ('INTACT', 'CONFLICT') and len(trace) >= 2:
        first_node = node_class847(trace[0]['text'], w)
        second_node = node_class847(trace[1]['text'], w)
        first_ok = (
            first_node == 'middle'
            and trace[0]['evid'] == ids['first']
            and ids['first'] in trace[0]['mem']
        )
        second_card = (
            ids['second'] if second_node == 'end'
            else ids['changed'] if second_node == 'changed_end'
            else None
        )
        second_ok = (
            second_card is not None
            and trace[1]['evid'] == second_card
            and second_card in trace[1]['mem']
        )
        grounded = bool(
            r['end'] == 'PATH_COMPLETE'
            and first_ok
            and second_ok
            and answer_cat in ('end', 'changed_end')
        )

    wrong_steps = []
    unknown_no_edge = 0
    unknown_with_edge = 0
    unnecessary_search = 0
    wrong_candidate = 0
    stack = []

    for si, step in enumerate(r['steps']):
        k = step['k']
        stack = stack[:k]
        if k == 0:
            current_cat = 'start'
        elif len(stack) >= k:
            current_cat = node_class847(stack[k-1]['text'], w)
        else:
            current_cat = 'OTHER'

        current_value = w.get(current_cat) if current_cat in w else None
        mounted_edge = False
        if current_value is not None:
            mounted_edge = any(
                card_source847(cid, wi, w) == current_value
                for cid in step['mem']
            )

        out_cat = node_class847(step['out'], w)
        expected = (
            {'middle'} if current_cat == 'start'
            else {'end', 'changed_end'} if current_cat == 'middle'
            else set()
        )
        if not step['unk'] and out_cat not in expected:
            wrong_steps.append({
                'step_index': si,
                'k': k,
                'output': step['out'],
                'output_class': out_cat,
                'current_class': current_cat
            })

        if step['unk']:
            if mounted_edge:
                unknown_with_edge += 1
            else:
                unknown_no_edge += 1

        if step.get('dec') == 'SEARCH' and mounted_edge:
            unnecessary_search += 1

        if 'cand' in step and current_cat in ('start', 'middle'):
            valid_cards = (
                {ids['first']}
                if current_cat == 'start'
                else {ids['second'], ids['changed']}
            )
            if step['cand'] not in valid_cards:
                wrong_candidate += 1

        if step.get('dec') == 'ADVANCE':
            stack.append({'text': step['out']})
        elif step.get('dec') == 'DEAD_END_BACKTRACK' and stack:
            stack.pop()

    backtracks = [
        (i, s) for i, s in enumerate(r['steps'])
        if s.get('dec') == 'DEAD_END_BACKTRACK'
    ]
    retractions = [
        (i, s) for i, s in enumerate(r['steps'])
        if s.get('retracted') is not None
    ]
    wrong_root_indices = [
        x['step_index'] for x in wrong_steps if x['k'] == 0
    ]
    counterfactual_after_wrong = any(
        s.get('retraction_basis') in (
            'COUNTERFACTUAL_UNKNOWN',
            'COUNTERFACTUAL_OUTPUT_CHANGE'
        )
        and any(wi_ < i for wi_ in wrong_root_indices)
        for i, s in retractions
    )
    retraction_after_wrong = any(
        any(wi_ < i for wi_ in wrong_root_indices)
        for i, _s in backtracks
    )
    corrected_after_wrong = bool(
        intervention == 'CONFLICT'
        and wrong_root_indices
        and counterfactual_after_wrong
        and retraction_after_wrong
        and grounded
    )

    stop_reason = (
        'MODEL_PATH_COMPLETE'
        if r['end'] == 'PATH_COMPLETE'
        else 'MECHANICAL_S_LIMIT'
        if any(s.get('why') == 'S_EXHAUSTED' for s in r['steps'])
        else 'MECHANICAL_CAPACITY'
        if any(s.get('why') == 'CAPACITY' for s in r['steps'])
        else 'MECHANICAL_BANK_EXHAUSTED'
        if any(s.get('why') == 'NO_CANDIDATE' for s in r['steps'])
        else 'MECHANICAL_HOP_BUDGET'
        if r['end'] == 'BUDGET_STOP'
        else 'NO_NEW_INFORMATION'
        if r['end'] == 'NO_NEW_INFORMATION'
        else 'PLAN_INVALID'
        if r['end'] == 'PLAN_INVALID'
        else 'OTHER'
    )
    removed_answer = intervention == 'REMOVED' and answer_cat is not None
    first_card = r['first_selected_card']
    first_source = card_source847(first_card, wi, w) if first_card is not None else None

    row = {
        'job': j['job'],
        'world_index': wi,
        'intervention': intervention,
        'arm': arm,
        'root_rows': r['root_rows'],
        'root_state_sha1': r['root_state_sha1'],
        'first_selected_card': first_card,
        'first_card_source': first_source,
        'steps': r['steps'],
        'path_trace': trace,
        'wrong_intermediates': wrong_steps,
        'unknown_no_mounted_edge': unknown_no_edge,
        'unknown_with_mounted_edge': unknown_with_edge,
        'python_backtracks': len(backtracks),
        'physical_card_retractions': [s.get('retracted') for _, s in retractions],
        'counterfactual_retractions': sum(
            s.get('retraction_basis') in (
                'COUNTERFACTUAL_UNKNOWN',
                'COUNTERFACTUAL_OUTPUT_CHANGE'
            )
            for _, s in retractions
        ),
        'corrected_after_wrong_grounded': corrected_after_wrong,
        'end': r['end'],
        'answer': r['pointer_answer'],
        'answer_class': answer_cat,
        'grounded_correct': grounded,
        'unsupported_removed_answer': removed_answer,
        'stop_reason': stop_reason,
        'hops': r['hops'],
        'searches': sum(s.get('dec') == 'SEARCH' for s in r['steps']),
        'wrong_candidate_count': wrong_candidate,
        'unnecessary_search_count': unnecessary_search,
        'mounts': r['mounts'],
        'seconds': r['seconds'],
        'final_mounted': r['final_mounted'],
        'excluded': r['excluded']
    }
    PILOT_RESULTS847.append(row)
    SUMMARY847.setdefault((wi, intervention, arm), []).append(row)

say_r41('TEST847 JOB-BY-JOB RESULTS')
for row in PILOT_RESULTS847:
    say_r41(
        'TEST847_CASE',
        'W=%d' % row['world_index'],
        row['intervention'],
        row['arm'],
        'ROOT_ROWS=%d' % row['root_rows'],
        'FIRST=%s/SOURCE=%s' % (row['first_selected_card'], row['first_card_source']),
        'PATH=' + json.dumps(
            [(p['text'], p['evid']) for p in row['path_trace']],
            ensure_ascii=False
        ),
        'WRONG=%d' % len(row['wrong_intermediates']),
        'BACKTRACK=%d' % row['python_backtracks'],
        'RETRACT=' + json.dumps(row['physical_card_retractions']),
        'END=%s' % row['end'],
        'ANSWER=%s' % row['answer_class'],
        'GROUNDED=%s' % row['grounded_correct'],
        'STOP=%s' % row['stop_reason']
    )

say_r41('TEST847 CAUSAL COMPARISON')
paired = []
for wi in PILOT_WORLDS846:
    for intervention in PILOT_STARTS846:
        model_rows = SUMMARY847.get((wi, intervention, 'MODEL_STATE'), [])
        matched_rows = SUMMARY847.get((wi, intervention, 'MATCHED_CONTROL'), [])
        cue_rows = SUMMARY847.get((wi, intervention, 'CUE_BASELINE'), [])
        if len(model_rows) == len(matched_rows) == len(cue_rows) == 1:
            m, c, b = model_rows[0], matched_rows[0], cue_rows[0]
            paired.append({
                'world': wi,
                'intervention': intervention,
                'model_grounded': m['grounded_correct'],
                'matched_grounded': c['grounded_correct'],
                'cue_grounded': b['grounded_correct'],
                'delta_model_matched': int(m['grounded_correct']) - int(c['grounded_correct'])
            })
            say_r41(
                'TEST847_PAIR',
                'W=%d' % wi,
                intervention,
                'MODEL=%s' % m['grounded_correct'],
                'MATCHED=%s' % c['grounded_correct'],
                'CUE=%s' % b['grounded_correct'],
                'DELTA=%+d' % (
                    int(m['grounded_correct']) - int(c['grounded_correct'])
                )
            )

answerable_pairs = [
    p for p in paired if p['intervention'] in ('INTACT', 'CONFLICT')
]
primary_delta = sum(p['delta_model_matched'] for p in answerable_pairs)
model_rescues = sum(
    r['corrected_after_wrong_grounded']
    for r in PILOT_RESULTS847
    if r['arm'] == 'MODEL_STATE' and r['intervention'] == 'CONFLICT'
)
matched_rescues = sum(
    r['corrected_after_wrong_grounded']
    for r in PILOT_RESULTS847
    if r['arm'] == 'MATCHED_CONTROL' and r['intervention'] == 'CONFLICT'
)
cue_rescues = sum(
    r['corrected_after_wrong_grounded']
    for r in PILOT_RESULTS847
    if r['arm'] == 'CUE_BASELINE' and r['intervention'] == 'CONFLICT'
)

complete847 = (
    not BUDGET_STOP841
    and len(PILOT_RESULTS847) == 27
    and len(paired) == 9
)
if not complete847:
    primary_verdict = 'INCONCLUSIVE_INCOMPLETE_PANEL'
elif primary_delta >= 2 and model_rescues >= 2 and model_rescues > matched_rescues:
    primary_verdict = 'PRELIMINARY_MODEL_STATE_CONTRIBUTION_SIGNAL'
elif primary_delta <= 0 and model_rescues <= matched_rescues:
    primary_verdict = 'PRIMARY_HYPOTHESIS_NOT_SUPPORTED'
else:
    primary_verdict = 'INCONCLUSIVE_MIXED_SMALL_PANEL'

removed = [r for r in PILOT_RESULTS847 if r['intervention'] == 'REMOVED']
unsupported_removed = sum(r['unsupported_removed_answer'] for r in removed)
mechanical_stops = sum(
    r['stop_reason'].startswith('MECHANICAL')
    for r in PILOT_RESULTS847
)
all_backtracks = sum(r['python_backtracks'] for r in PILOT_RESULTS847)
all_unknown_no_edge = sum(r['unknown_no_mounted_edge'] for r in PILOT_RESULTS847)
all_unknown_with_edge = sum(r['unknown_with_mounted_edge'] for r in PILOT_RESULTS847)
all_wrong_candidates = sum(r['wrong_candidate_count'] for r in PILOT_RESULTS847)
all_unnecessary_search = sum(r['unnecessary_search_count'] for r in PILOT_RESULTS847)

say_r41('TEST847 ERROR DETECTION AND CORRECTION')
say_r41(
    'UNKNOWN_NO_EDGE=%d UNKNOWN_WITH_EDGE=%d PYTHON_BACKTRACKS=%d '
    'COUNTERFACTUAL_RETRACTIONS=%d MODEL_STATE_RESCUES=%d MATCHED_RESCUES=%d CUE_RESCUES=%d'
    % (
        all_unknown_no_edge,
        all_unknown_with_edge,
        all_backtracks,
        sum(r['counterfactual_retractions'] for r in PILOT_RESULTS847),
        model_rescues,
        matched_rescues,
        cue_rescues
    )
)
say_r41(
    'WRONG_CANDIDATES=%d UNNECESSARY_SEARCHES=%d REMOVED_UNSUPPORTED_ANSWERS=%d '
    'MECHANICAL_STOPS=%d'
    % (
        all_wrong_candidates,
        all_unnecessary_search,
        unsupported_removed,
        mechanical_stops
    )
)

say_r41('TEST847 FAILURE ANALYSIS')
for arm in PILOT_ARMS846:
    for intervention in PILOT_STARTS846:
        rs = [
            r for r in PILOT_RESULTS847
            if r['arm'] == arm and r['intervention'] == intervention
        ]
        say_r41(
            'FAILURE_CELL',
            arm,
            intervention,
            'N=%d' % len(rs),
            'GROUNDED=%d' % sum(r['grounded_correct'] for r in rs),
            'WRONG_INTERMEDIATE=%d' % sum(bool(r['wrong_intermediates']) for r in rs),
            'BACKTRACK=%d' % sum(r['python_backtracks'] for r in rs),
            'UNSUPPORTED=%d' % sum(r['unsupported_removed_answer'] for r in rs)
        )

physical_ok847 = all(c['pass'] for c in D829['checks'])
say_r41('TEST847 FINAL SCIENTIFIC VERDICT')
say_r41('PRIMARY_HYPOTHESIS:', primary_verdict)
say_r41('PAIRED_DELTA_MODEL_MINUS_MATCHED:', primary_delta)
say_r41(
    'GROUNDED_CONFLICT_RESCUES_MODEL_MATCHED_CUE:',
    model_rescues,
    matched_rescues,
    cue_rescues
)
say_r41('PHYSICAL_MEMORY_INTEGRITY:', 'PASS' if physical_ok847 else 'FAIL')
say_r41('MODEL_NATIVE_AUTONOMOUS_REASONING:', 'NOT_DEMONSTRATED')
say_r41('MODEL_NATIVE_STOP:', 'NOT_DEMONSTRATED')
say_r41(
    'INTERPRETATION:',
    'UNKNOWN model çıktısıdır; arama, kanıt çıkarma, geri dönüş ve S/HMAX duruşları '
    'Python kontrolüdür. Bu pilot yalnızca eşleştirilmiş durumların kanıtla destekli '
    'sonuçlar üzerindeki farkını sınar.'
)

if primary_verdict == 'PRELIMINARY_MODEL_STATE_CONTRIBUTION_SIGNAL':
    mechanism_next = (
        'Yanlış ilk ara düğüm ile sonraki UNKNOWN arasındaki durum sürekliliğini ve '
        'karşıolgusal kanıt attribution adımını ayrı ayrı sınamak gerekir.'
    )
elif primary_verdict == 'PRIMARY_HYPOTHESIS_NOT_SUPPORTED':
    mechanism_next = (
        'Model durumunun eşlenmiş kontrol üstünde katkısı bu küçük panelde görülmedi; '
        'önce kök durumun hedef düğüm bilgisini taşıyıp taşımadığı incelenmelidir.'
    )
else:
    mechanism_next = (
        'Sonuç küçük veya karışık kaldı; vaka kayıtları incelenerek önceden kilitli '
        'bir doğrulama paneli tasarlanmalıdır.'
    )

say_r41('NEXT_MECHANISM:', mechanism_next)

report_lines847 = [
    'TEST847 27 önceden tanımlanmış işi değerlendirdi: üç sabit mevcut dünya, üç kol ve üç kanıt müdahalesi.',
    'Birincil nedensel karşılaştırma, aynı satır şekli ve satır normlarına sahip MODEL_STATE ile MATCHED_CONTROL arasındadır.',
    'INTACT özgün bankayı korur; CONFLICT mevcut fork kartuşunu başlangıç belleğine takar; REMOVED second/changed kartuşlarını o işin aranabilir bankasından çıkarır.',
    'Grounded sonuç için kayıtlı yolun fiziksel first kartuşunu ve geçerli second/changed kartuşunu kullanması gerekir.',
    'Model UNKNOWN çıktıları; Python arama, çıkarma, geri dönüş ve mekanik durdurma kararlarından ayrı sayılır.',
    'Birincil hüküm: ' + primary_verdict + '. MODEL_STATE eksi MATCHED_CONTROL eşlenmiş grounded cevap farkı: ' + str(primary_delta) + '.',
    'CONFLICT grounded düzeltme sayıları (MODEL_STATE / MATCHED_CONTROL / CUE_BASELINE): '
    + str(model_rescues) + ' / ' + str(matched_rescues) + ' / ' + str(cue_rescues) + '.',
    'REMOVED desteksiz cevap: ' + str(unsupported_removed)
    + '; Python backtrack: ' + str(all_backtracks)
    + '; mekanik durma: ' + str(mechanical_stops) + '.',
    'Otonom rekürsif akıl yürütme ve model-native durma NOT_DEMONSTRATED olarak kalır; arama, geri alma ve bütçeler Python kontrolündedir.',
    'Sonraki mekanizma: ' + mechanism_next
]

say_r41('TEST847 SCIENTIFIC REPORT')
for line in report_lines847:
    say_r41('REPORT', line)

D829['test847'] = {
    'status': 'COMPLETE' if complete847 else 'INCOMPLETE',
    'source_base_846_blob_sha1': '6093896b7e4492f201cece448ad1646b0bd8820a',
    'jobs_expected': 27,
    'jobs_completed': len(PILOT_RESULTS847),
    'primary_verdict': primary_verdict,
    'primary_delta_model_vs_matched_answerable': primary_delta,
    'conflict_grounded_rescues': {
        'MODEL_STATE': model_rescues,
        'MATCHED_CONTROL': matched_rescues,
        'CUE_BASELINE': cue_rescues
    },
    'error_detection_and_correction': {
        'unknown_no_mounted_edge': all_unknown_no_edge,
        'unknown_with_mounted_edge': all_unknown_with_edge,
        'python_backtracks': all_backtracks,
        'wrong_candidates': all_wrong_candidates,
        'unnecessary_searches': all_unnecessary_search,
        'unsupported_removed_answers': unsupported_removed,
        'mechanical_stops': mechanical_stops
    },
    'physical_memory_integrity': 'PASS' if physical_ok847 else 'FAIL',
    'autonomous_recursive_reasoning': 'NOT_DEMONSTRATED',
    'model_native_stop': 'NOT_DEMONSTRATED',
    'paired_cases': paired,
    'cases': PILOT_RESULTS847,
    'report': report_lines847,
    'limitations': [
        'Three existing worlds only; exploratory panel, no generalization claim.',
        'World indices 0, 1, 2 fixed before model execution, not selected from TEST846 outcomes.',
        'CONFLICT is an existing competing fork route, not a newly invented fact.',
        'REMOVED excludes second/changed from the query bank; append-only files are not deleted.',
        'CUE_BASELINE differs in root frame by definition; primary state comparison is MODEL_STATE vs MATCHED_CONTROL.',
        'Python implements search, retraction, backtracking, and mechanical budgets.',
        'No autonomous reasoning PASS is inferred.'
    ]
}
D829['verdict841R'] = {
    'decision': primary_verdict,
    'verdicts': {
        'PHYSICAL_MEMORY_INTEGRITY': 'PASS' if physical_ok847 else 'FAIL',
        'MODEL_NATIVE_STOP_DECISION': 'NOT_DEMONSTRATED',
        'AUTONOMOUS_RECURSIVE_REASONING': 'NOT_DEMONSTRATED',
        'C1_TO_C7_FULL_PANEL': 'NOT_EVALUATED'
    },
    'budget_stop': BUDGET_STOP841,
    'measures': {
        'primary_delta': primary_delta,
        'model_rescues': model_rescues,
        'matched_rescues': matched_rescues,
        'cue_rescues': cue_rescues
    }
}
D829['status'] = 'COMPLETE_TEST847' if complete847 else 'PARTIAL_TEST847'
save829()
log829('TEST847_COMPLETED', str(OUT829))
'''

# Patch only the structurally identified base panel assignment.
SRC847 = replace_top_assignment847(
    SRC847,
    "PANEL846",
    "PANEL_FACTORY846 + " + repr(PANEL_TAIL847)
)
SRC847 = replace_top_assignment847(SRC847, "RUN846", repr(RUN847))
SRC847 = replace_top_assignment847(SRC847, "OFF846", repr(OFF847))
SRC847 = SRC847.replace("TEST846P", "TEST847")
SRC847 = SRC847.replace("TEST846 PILOT v3", "TEST847 CAUSAL PILOT")

# Final artifact hashes are emitted after the inherited engine has closed its writers.
SRC847 += r'''

print("=" * 78)
print("TEST847 ARTIFACT PATHS AND SHA256")
if globals().get("DIR829") is not None:
    for p847 in sorted(_P841(DIR829).rglob("*")):
        if p847.is_file():
            print(
                str(p847),
                "BYTES=" + str(p847.stat().st_size),
                "SHA256=" + sha_path841(p847)
            )
print("=" * 78)
'''

ast.parse(SRC847)

print("=" * 78)
print("TEST847 SOURCE VERIFICATION")
print("TEST846.py Git blob SHA1:", BASE847_BLOB)
print("Locked parent chain: TEST845.py -> TEST844.py -> TEST841.py")
print("TEST846P_results.json: unavailable in repository; case-level claims are not inferred")
print("=" * 78)
print("TEST847 HARDWARE AND MODEL")
print("Single NVIDIA A100-SXM4-80GB | Qwen2.5-72B-Instruct NF4 | frozen weights")
print("=" * 78)
print("TEST847 PHYSICAL MEMORY INTEGRITY")
print("Inherited SHA, CUT3, H3/KV and no-hook gates remain enabled")
print("=" * 78)
print("TEST847 PRE-REGISTERED HYPOTHESES")
print("MODEL_STATE vs MATCHED_CONTROL: +2 grounded outcomes across six INTACT/CONFLICT pairs,")
print("and at least two grounded conflict rescues, exceeding MATCHED_CONTROL.")
print("Python-triggered backtracking and mechanical stops are not model-native correction.")
print("=" * 78)
print("TEST847 EXPERIMENTAL PANEL")
print("3 fixed existing worlds x 3 arms x 3 interventions = 27 jobs; maximum 30")
print("Arms: MODEL_STATE, MATCHED_CONTROL, CUE_BASELINE")
print("Interventions: INTACT, CONFLICT, REMOVED")
print("GPU EXECUTION: NOT VERIFIED HERE")
print("=" * 78, flush=True)

exec(compile(SRC847, "TEST847_LOCKED_TEST846_BASE", "exec"), globals())
