import urllib.request, hashlib, ast, json

URL846 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/845.py"
LOCK846 = "be81a587b3d2b8cd3e9291df6bd9fb481c4c2164"
request846 = urllib.request.Request(URL846, headers={"User-Agent": "AKBASCORE-TEST846-PILOT-V3"})
with urllib.request.urlopen(request846, timeout=180) as response:
    raw846 = response.read(200001)
blob846 = hashlib.sha1(b"blob " + str(len(raw846)).encode() + b"\0" + raw846).hexdigest()
assert blob846 == LOCK846, ("SOURCE_LOCK_FAILED", blob846, LOCK846)
D846 = raw846.decode("utf-8").replace("TEST845", "TEST846P").replace("T845|", "T846P|")

def rp846(source, old, new):
    count = source.count(old)
    assert count == 1, ("PATCH_ANCHOR_FAILED", old[:100], count)
    return source.replace(old, new, 1)

def cut846(source, begin, end, replacement):
    assert source.count(begin) == 1, ("CUT_START_FAILED", begin)
    i = source.index(begin)
    j = source.index(end, i)
    assert j > i
    return source[:i] + replacement + source[j:]

def extract846(source, begin, end):
    assert source.count(begin) == 1, ("EXTRACT_START_FAILED", begin)
    i = source.index(begin) + len(begin)
    j = source.index(end, i)
    return source[i:j]

ORIGINAL_PANEL846 = extract846(D846, "PANEL845 = r'''", "'''\nCOST845 = r'''")
PANEL_FACTORY846 = ORIGINAL_PANEL846.split("DIAG845, JUN845 = {}, {}")[0]
assert "def job41r(" in PANEL_FACTORY846
assert "JOBS841.append(" in PANEL_FACTORY846
PANEL_FACTORY846 = rp846(PANEL_FACTORY846, "    EVALKEY841[j] = role\n", "")
panel_factory_names846 = {
    n.id for n in ast.walk(ast.parse(PANEL_FACTORY846))
    if isinstance(n, ast.Name)
}
assert "EVALKEY841" not in panel_factory_names846, (
    "PANEL_FACTORY_LABEL_ACCESS",
    sorted(panel_factory_names846 & {"EVALKEY841"})
)

PANEL846 = PANEL_FACTORY846 + r'''
PILOT_WORLDS846 = (0, 1, 2)
PILOT_STARTS846 = ('LIVE', 'MISSING', 'HOP3')
PILOT_ARMS846 = ('RSJ', 'RSJ_CUE', 'RSJ_ZERO')
STARTS41R = PILOT_STARTS846
ARMS41R = PILOT_ARMS846
JARMS845 = PILOT_ARMS846
DCONDS845 = ()

for arm in PILOT_ARMS846:
    for wi in PILOT_WORLDS846:
        w = worlds829[wi]
        ids = w['ids']
        B = BANKS841[BLOCKOF841[wi]]

        for st in PILOT_STARTS846:
            drop = {
                'MISSING': (ids['second'], ids['changed']),
                'HOP3': (ids['mirror'],)
            }.get(st, ())

            qid = w['world'] + '_H3' if st == 'HOP3' else QID841[wi]
            bank = [c for c in B['v0'] if c not in drop]

            job41r(
                qid,
                {'world': wi, 'cond': st, 'arm': arm},
                bank,
                arm,
                [],
                None
            )

assert len(JOBS841) == 27
assert len({j['job'] for j in JOBS841}) == 27
assert JOBS841 and JOBS841[0]['bank']
# Legacy TEST841 preflight uses one nonempty start field to select a physical card
# for its bypass equivalence check. The pilot loop below always starts with empty memory.
JOBS841[0]['start'] = [JOBS841[0]['bank'][0]]
'''
PANEL846 = PANEL846.replace("'J845_'", "'J846P_'")
assert "'''" not in PANEL846
panel_names846 = {
    n.id for n in ast.walk(ast.parse(PANEL846))
    if isinstance(n, ast.Name)
}
assert "EVALKEY841" not in panel_names846, (
    "PANEL_LABEL_ACCESS",
    sorted(panel_names846 & {"EVALKEY841"})
)
D846 = cut846(
    D846,
    "PANEL845 = r'''",
    "'''\nCOST845 = r'''",
    "PANEL845 = r'''" + PANEL846
)

ENGINE_PREFIX846 = extract846(
    D846,
    "RUN845 = r'''",
    "say_r41('PREREG', 'S=%d HMAX=%d"
)
for required846 in (
    "def gen845(",
    "def hop845(",
    "def addr845(",
    "def plan845(",
    "def jloop845("
):
    assert required846 in ENGINE_PREFIX846, ("ENGINE_SYMBOL_MISSING", required846)
assert "for ji845, j845 in enumerate(JOBS841)" not in ENGINE_PREFIX846

RUN846 = r'''
HMAX846 = 30

FR845['start'] = (
    'Question: {q}\n'
    'Name the start node of the question. '
    'Reply with the node name only.'
)
START_SLOT846 = list(tok('Start node:', add_special_tokens=False).input_ids)
START_CACHE846 = {}

def start846(q):
    if q not in START_CACHE846:
        pre = list(prompt_ids(FR845['start'].format(q=QTEXT841[q]))) + START_SLOT846
        START_CACHE846[q] = gen845(MEMNULL841, pre, None, None)
    return START_CACHE846[q]

def root846(arm, q):
    if arm == 'RSJ_CUE':
        return None
    own = start846(q)['rows']
    if arm == 'RSJ_ZERO':
        return MUE845.float().cpu().reshape(1, H).repeat(max(1, int(own.shape[0])), 1)
    return own

def hopx846(q, mem, k, rows, cue):
    if k == 0 and cue:
        return hop845(q, mem, 0, None)
    return hop845(q, mem, 1, rows)

def attrib846(q, mem, k, path, root, cue):
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
        h = hopx846(q, counterfactual, k, rows, cue)
        if h['unk']:
            return card
        if fallback is None and h['text'].strip() != original:
            fallback = card
    return fallback

MECHENDS846 = (
    'BUDGET_STOP',
    'PLAN_INVALID',
    'NO_NEW_INFORMATION',
    'CAPACITY_STOP',
    'BANK_EXHAUSTED'
)

def jloop846(j):
    q = j['qid']
    arm = j['arm']
    bank = list(j['bank'])
    # The legacy start field is used only by the inherited preflight fixture.
    # Every experimental job begins with empty mounted memory.
    mem = []
    cue = arm == 'RSJ_CUE'
    start_result = start846(q)
    root = root846(arm, q)
    plan = plan845(q)
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

    t0 = time.perf_counter()
    mounts0 = CNT_R41['mounts']

    while end is None:
        k = len(path)

        if k == N:
            end = 'PATH_COMPLETE'
            break

        if hops >= HMAX846:
            end = 'BUDGET_STOP'
            break

        rows = root if k == 0 else path[k-1]['rows']
        state_id = 'ROOT_CUE' if k == 0 and cue else rkey845(rows)
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
        h = hopx846(q, mem, k, rows, cue)
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
                candidate = addr845(
                    q,
                    mem,
                    None if k == 0 and cue else rows,
                    bank,
                    local_exclusions
                )
                if candidate is None:
                    reason = 'NO_CANDIDATE'

            if candidate is not None:
                card = candidate['chosen']
                assert card in bank
                assert card not in mem
                mem.append(card)
                pending = card
                tries[k] = tries.get(k, 0) + 1
                step.update({
                    'dec': 'SEARCH',
                    'cand': card,
                    'try': tries[k],
                    'via': candidate['via']
                })
            else:
                step['why'] = reason
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
                    evidence = previous['evid'] or attrib846(
                        q, mem, k-1, path, root, cue
                    )
                    previous_rows = root if k == 1 else path[k-2]['rows']
                    previous_state = (
                        'ROOT_CUE'
                        if k == 1 and cue
                        else rkey845(previous_rows)
                    )

                    if evidence is not None and evidence in mem:
                        mem.remove(evidence)
                        excluded.append(evidence)
                        excluded_by_state.setdefault(previous_state, []).append(evidence)
                        step['retracted'] = evidence

                    path.pop()
                    tries[k-1] = 0
                    tries[k] = 0
                    step['dec'] = 'DEAD_END_BACKTRACK'

        steps.append(step)
        say_r41(
            'PILOT_HOP',
            j['job'],
            arm,
            'k=%d' % k,
            'OUT=%r' % h['text'][:24],
            'DEC=' + step['dec']
        )

    pointer = (
        path[-1]['text']
        if end == 'PATH_COMPLETE'
        else 'UNKNOWN'
        if end == 'ABSTAIN'
        else None
    )
    frame_answer = answer_r41(q, mem)

    record = {
        'job': j['job'],
        'kind': 'LOOP',
        'qid': q,
        'arm': arm,
        'steps': steps,
        'end': end,
        'pointer_answer': pointer,
        'answer_raw': frame_answer,
        'path': [p['text'] for p in path],
        'plan': plan,
        'start_text': start_result['text'],
        'root_rows': int(root.shape[0]) if root is not None else 0,
        'root_state_sha1': rkey845(root) if root is not None else None,
        'final_mounted': list(mem),
        'excluded': excluded,
        'hops': hops,
        'mounts': CNT_R41['mounts'] - mounts0,
        'seconds': round(time.perf_counter() - t0, 2),
        'mech_dead_ends': mechanical_dead_ends
    }
    return record, {}

assert len(JOBS841) == 27
assert set(j['arm'] for j in JOBS841) == {'RSJ', 'RSJ_CUE', 'RSJ_ZERO'}
assert len({(j['qid'], j['arm']) for j in JOBS841}) >= 18

say_r41(
    'PILOT_PREREG',
    'WORLDS=3',
    'STARTS=3',
    'ARMS=3',
    'JOBS=27',
    'S=3',
    'HMAX=30',
    'CAP=5'
)

UPPER_CHECK841 = {}
t_run841 = time.perf_counter()
nj846 = len(JOBS841)
BUDGET_STOP841 = False
log829('TEST846P_PROGRESS', 0, '/', nj846)

for ji846, j846 in enumerate(JOBS841):
    if j846['job'] not in REC841:
        elapsed_minutes = (time.perf_counter() - T0_841) / 60.0
        if elapsed_minutes > HARD_BUDGET_MIN841:
            BUDGET_STOP841 = True
            log829('TEST846P_BUDGET_STOP', ji846, nj846)
            break
        try:
            if not UPPER_CHECK841:
                with CallCount841() as cc846:
                    rec846, rows846 = jloop846(j846)
                UPPER_CHECK841 = cc846.summary()
                gate829(
                    'CUT3_UPPER_LAYER_EXECUTION',
                    UPPER_CHECK841['upper_min'] >= 1 and UPPER_CHECK841['lm_head'] >= 1,
                    UPPER_CHECK841
                )
            else:
                rec846, rows846 = jloop846(j846)
        except BudgetR41 as err846:
            BUDGET_STOP841 = True
            log829('TEST846P_BUDGET_STOP', str(err846), ji846, nj846)
            break

        REC841[j846['job']] = rec846
        ROWS841[j846['job']] = rows846
        save_job841(j846['job'], rec846, rows846)

    log829('TEST846P_PROGRESS', ji846 + 1, '/', nj846, j846['arm'])

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

FORBIDDEN_RUN_NAMES846 = {
    "EVALKEY841",
    "CONTENT841",
    "worlds829",
    "card_meta829"
}
run_names846 = {
    n.id for n in ast.walk(ast.parse(RUN846))
    if isinstance(n, ast.Name)
}
assert not (run_names846 & FORBIDDEN_RUN_NAMES846), (
    "RUN_LABEL_ISOLATION",
    sorted(run_names846 & FORBIDDEN_RUN_NAMES846)
)

OFF846 = r'''
log829('TEST846P_OFFLINE_START')
PILOT_RESULTS846 = []
PILOT_SUM846 = {}

for j in JOBS841:
    if j['job'] not in REC841:
        continue

    r = REC841[j['job']]
    qid = j['qid']

    if qid.endswith('_H3'):
        wi = next(
            i for i, w_ in enumerate(worlds829)
            if qid == w_['world'] + '_H3'
        )
        st = 'HOP3'
    else:
        wi = QID841.index(qid)
        ids = worlds829[wi]['ids']
        bank_set = set(j['bank'])
        st = (
            'MISSING'
            if ids['second'] not in bank_set
            and ids['changed'] not in bank_set
            else 'LIVE'
        )

    arm = j['arm']
    w = worlds829[wi]
    ids = w['ids']
    final_mem = set(r['final_mounted'])
    answer = r['pointer_answer'].strip() if r['pointer_answer'] is not None else None

    if st == 'MISSING':
        correct = r['end'] == 'ABSTAIN' and r.get('mech_dead_ends', 0) == 0
        grounded = False
    elif st == 'HOP3':
        grounded = (
            r['end'] == 'PATH_COMPLETE'
            and answer == w['end3']
            and {ids['first'], ids['second'], ids['third']} <= final_mem
        )
        correct = grounded
    else:
        grounded = (
            r['end'] == 'PATH_COMPLETE'
            and ids['first'] in final_mem
            and (
                (answer == w['end'] and ids['second'] in final_mem)
                or (answer == w['changed_end'] and ids['changed'] in final_mem)
            )
        )
        correct = grounded

    row = {
        'world': wi,
        'start': st,
        'arm': arm,
        'end': r['end'],
        'answer': answer,
        'correct': bool(correct),
        'grounded': bool(grounded),
        'hops': r['hops'],
        'mounts': r['mounts'],
        'seconds': r['seconds'],
        'mechanical_dead_ends': r['mech_dead_ends'],
        'path': r['path'],
        'final_mounted': r['final_mounted'],
        'start_text': r['start_text'],
        'root_rows': r.get('root_rows', 0),
        'root_state_sha1': r.get('root_state_sha1')
    }
    PILOT_RESULTS846.append(row)
    PILOT_SUM846.setdefault((arm, st), []).append(row)

comparison846 = {}
for arm in PILOT_ARMS846:
    for st in PILOT_STARTS846:
        rows = PILOT_SUM846.get((arm, st), [])
        comparison846[arm + '|' + st] = {
            'correct': sum(x['correct'] for x in rows),
            'grounded': sum(x['grounded'] for x in rows),
            'total': len(rows),
            'ends': [x['end'] for x in rows],
            'root_rows': [x['root_rows'] for x in rows]
        }
        log829(
            'TEST846P_RESULT',
            arm,
            st,
            'CORRECT=%d/%d' % (comparison846[arm + '|' + st]['correct'], len(rows)),
            'GROUNDED=%d' % comparison846[arm + '|' + st]['grounded'],
            'ENDS=' + json.dumps(comparison846[arm + '|' + st]['ends']),
            'ROOT_ROWS=' + json.dumps(comparison846[arm + '|' + st]['root_rows'])
        )

complete846 = (
    not BUDGET_STOP841
    and len(PILOT_RESULTS846) == 27
    and all(
        len(PILOT_SUM846.get((arm, st), [])) == 3
        for arm in PILOT_ARMS846
        for st in PILOT_STARTS846
    )
)
physical_ok846 = all(c['pass'] for c in D829['checks'])

D829['pilot846'] = {
    'status': 'COMPLETE_PILOT' if complete846 else 'INCOMPLETE_PILOT',
    'jobs_expected': 27,
    'jobs_completed': len(PILOT_RESULTS846),
    'comparison': comparison846,
    'cases': PILOT_RESULTS846,
    'limitations': [
        'Exploratory pilot, three worlds only.',
        'Original TEST845 worlds reused.',
        'Not a held-out generalization test.',
        'No full C1-C7 evaluation.',
        'ABSTAIN follows mechanical search limits.',
        'RSJ_CUE changes both root frame and state.',
        'Path completion uses model plan and Python counting.',
        'No autonomous reasoning PASS inferred.'
    ]
}

D829['verdict841R'] = {
    'decision': 'PILOT_COMPLETE_REVIEW_RESULTS' if complete846 else 'PILOT_INCOMPLETE',
    'verdicts': {
        'PHYSICAL_MEMORY_INTEGRITY': 'PASS' if physical_ok846 else 'FAIL',
        'MODEL_NATIVE_STOP_DECISION': 'NOT_DEMONSTRATED',
        'AUTONOMOUS_RECURSIVE_REASONING': 'NOT_DEMONSTRATED',
        'C1_TO_C7_FULL_PANEL': 'NOT_EVALUATED'
    },
    'budget_stop': BUDGET_STOP841
}
D829['status'] = 'COMPLETE_TEST846_PILOT' if complete846 else 'PARTIAL_TEST846_PILOT'
log829('TEST846P_FINAL', D829['pilot846']['status'], json.dumps(comparison846))
save829()
log829('TEST846P_COMPLETED', str(OUT829))
'''

D846 = rp846(
    D846,
    "HARD_BUDGET_MIN841 = 330.0",
    "HARD_BUDGET_MIN841 = 600.0"
)
D846 = cut846(
    D846,
    "RUN845 = r'''",
    "'''\n\n# ---------------- OFFLINE EVALUATION",
    "RUN845 = r'''" + ENGINE_PREFIX846 + RUN846
)
D846 = cut846(
    D846,
    "OFF845 = r'''",
    "'''\n\n# ---------------- PATCH THE 844 DRIVER",
    "OFF845 = r'''" + OFF846
)

assert "TEST846P_OFFLINE_START" in D846
assert "'''" not in PANEL846 + RUN846 + OFF846
assert "for ji846, j846 in enumerate(JOBS841)" in RUN846
assert "for ji845, j845 in enumerate(JOBS841)" not in RUN846
assert "J846P_" in PANEL846
assert "PILOT_WORLDS846 = (0, 1, 2)" in PANEL846
ast.parse(D846)

parsed846 = ast.parse(D846)
blocks846 = {}
for node in parsed846.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1:
        target = node.targets[0]
        if isinstance(target, ast.Name) and target.id in ("PANEL845", "RUN845", "OFF845"):
            blocks846[target.id] = node.value.value

assert set(blocks846) == {"PANEL845", "RUN845", "OFF845"}
for block_name846 in ("PANEL845", "RUN845", "OFF845"):
    ast.parse(blocks846[block_name846])

run_names846 = {
    n.id for n in ast.walk(ast.parse(blocks846["RUN845"]))
    if isinstance(n, ast.Name)
}
assert not (run_names846 & FORBIDDEN_RUN_NAMES846), (
    "LABEL_LEAK_IN_RUN",
    sorted(run_names846 & FORBIDDEN_RUN_NAMES846)
)
assert blocks846["RUN845"].count("for ji846, j846 in enumerate(JOBS841)") == 1
assert "for ji845, j845 in enumerate(JOBS841)" not in blocks846["RUN845"]

print("=" * 78)
print("AKBASCORE SILICON HIPPOCAMPUS — TEST846 PILOT v3")
print("=" * 78)
print("SOURCE GIT BLOB:", LOCK846)
print("PATCHED DRIVER SHA256:", hashlib.sha256(D846.encode()).hexdigest())
print("WORLDS: 3 | START CONDITIONS: 3 | ARMS: 3 | EXPERIMENTAL JOBS: 27")
print("SOURCE AST: PASS | PANEL AST: PASS | RUN AST: PASS | OFFLINE AST: PASS")
print("RUN LABEL ISOLATION: PASS | SINGLE PILOT LOOP: PASS | SOURCE LOCK: PASS")
print("GPU EXECUTION: NOT YET VERIFIED")
print("=" * 78, flush=True)

exec(compile(D846, "TEST846_PILOT_DRIVER", "exec"), globals())
