# ======================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST848
# Native self-review, correction and stop feasibility
#
# 3 reused worlds x 3 state arms x 3 evidence conditions = 27 jobs
#
# Arms:
#   MODEL_STATE   : model's own numerical rows
#   ORDER_CONTROL : same rows in reversed order
#   NO_STATE      : no prior numerical rows inserted
#
# Evidence conditions:
#   INTACT        : first + second + changed cards mounted
#   CONFLICT      : intact cards plus existing fork card
#   REMOVED       : first + fork mounted; second/changed unavailable
#
# This tests one model-generated review/control step.
# It does not claim full autonomous recursive reasoning.
# ======================================================================

import urllib.request
import hashlib
import ast
import json
import time
import re
import torch
import numpy as np


# ======================================================================
# 1. LOCKED TEST847 SOURCE
# ======================================================================

URL848 = (
    "https://raw.githubusercontent.com/"
    "ceceli33/titan-cognitive-core-v3/main/847.py"
)
LOCK847_848 = "72ce35daa728f546d92baa26705dd04ed5ad6a11"

request848 = urllib.request.Request(
    URL848,
    headers={"User-Agent": "AKBASCORE-TEST848-SELF-REVIEW"}
)
with urllib.request.urlopen(request848, timeout=180) as response:
    raw848 = response.read(1000001)

blob847_848 = hashlib.sha1(
    b"blob " + str(len(raw848)).encode() + b"\0" + raw848
).hexdigest()

assert blob847_848 == LOCK847_848, (
    "TEST847_SOURCE_LOCK_FAILED",
    blob847_848,
    LOCK847_848
)

SRC848 = raw848.decode("utf-8")
ast.parse(SRC848)


# ======================================================================
# 2. AST-BASED EXACT SOURCE PATCH HELPERS
# ======================================================================

def replace_module_assignment848(source, name, value):
    tree = ast.parse(source)
    matches = [
        node for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == name
            for target in node.targets
        )
    ]

    assert len(matches) == 1, (
        "MODULE_ASSIGNMENT_NOT_UNIQUE",
        name,
        len(matches),
        [node.lineno for node in matches]
    )

    node = matches[0]
    lines = source.splitlines(keepends=True)
    lines[node.lineno - 1:node.end_lineno] = [
        name + " = " + repr(value) + "\n"
    ]
    result = "".join(lines)
    ast.parse(result)
    return result


def replace_exact_once848(source, old, new):
    count = source.count(old)
    assert count == 1, (
        "EXACT_SOURCE_ANCHOR_NOT_UNIQUE",
        old,
        count
    )
    return source.replace(old, new, 1)


# ======================================================================
# 3. PRE-REGISTERED 27-JOB PANEL
# ======================================================================

PANEL_TAIL848 = r'''
PILOT_WORLDS846 = (0, 1, 2)
PILOT_STARTS846 = ('INTACT', 'CONFLICT', 'REMOVED')
PILOT_ARMS846 = (
    'MODEL_STATE',
    'ORDER_CONTROL',
    'NO_STATE'
)
STARTS41R = PILOT_STARTS846
ARMS41R = PILOT_ARMS846
JARMS845 = PILOT_ARMS846
DCONDS845 = ()

for arm in PILOT_ARMS846:
    for wi in PILOT_WORLDS846:
        w = worlds829[wi]
        ids = w['ids']
        B = BANKS841[BLOCKOF841[wi]]

        if len(set((
            ids['first'],
            ids['second'],
            ids['changed'],
            ids['fork']
        ))) != 4:
            raise AssertionError(
                ('PANEL_CARD_ID_COLLISION', wi, ids)
            )

        if intervention_placeholder848 := None:
            raise AssertionError(intervention_placeholder848)

        for condition in PILOT_STARTS846:
            if condition == 'INTACT':
                initial = [
                    ids['first'],
                    ids['second'],
                    ids['changed']
                ]
                drop = ()

            elif condition == 'CONFLICT':
                initial = [
                    ids['first'],
                    ids['second'],
                    ids['changed'],
                    ids['fork']
                ]
                drop = ()

            elif condition == 'REMOVED':
                initial = [
                    ids['first'],
                    ids['fork']
                ]
                drop = (
                    ids['second'],
                    ids['changed']
                )

            else:
                raise ValueError(('UNKNOWN_PANEL_CONDITION', condition))

            initial = list(dict.fromkeys(initial))
            bank = [
                c for c in B['v0']
                if c not in set(initial)
                and c not in set(drop)
            ]

            job41r(
                QID841[wi],
                {
                    'world': wi,
                    'cond': condition,
                    'arm': arm
                },
                bank,
                arm,
                [],
                None
            )

            JOBS841[-1]['intervention'] = condition
            JOBS841[-1]['initial_cards'] = list(initial)

assert len(JOBS841) == 27
assert len({j['job'] for j in JOBS841}) == 27
assert {j['arm'] for j in JOBS841} == set(PILOT_ARMS846)
assert {j['intervention'] for j in JOBS841} == set(PILOT_STARTS846)
assert JOBS841 and JOBS841[0]['bank']

# The inherited TEST841 preflight fixture needs one nonempty start field.
JOBS841[0]['start'] = [JOBS841[0]['bank'][0]]
'''


# Remove the no-op assignment from the literal panel string while keeping
# the panel source itself exact and AST-parseable.
PANEL_TAIL848 = PANEL_TAIL848.replace(
    """        if intervention_placeholder848 := None:
            raise AssertionError(intervention_placeholder848)

""",
    ""
)


# ======================================================================
# 4. MODEL-NATIVE REVIEW AND FIXED ACTUATOR
#
# The model emits CONTINUE / REVISE / STOP.
# Python only parses this fixed action protocol and applies the action.
# No generated prior answer text is replayed into later prompts.
# ======================================================================

RUN848 = r'''
UPPER_CHECK841 = {}
BUDGET_STOP841 = False
FIRST_STATE848 = {}
FIRST_RECORD848 = {}
REVIEW_FRAME848 = (
    'Question: {q}\n'
    'Use only the mounted physical evidence. The numerical context '
    'inserted after this instruction is your previous one-link calculation '
    'state. Decide whether the prior calculation is supported, must be '
    'revised, or whether the available evidence is insufficient. '
    'Reply with exactly one action word: CONTINUE, REVISE, or STOP.'
)
REVISE_FRAME848 = (
    'Question: {q}\n'
    'Use only mounted physical evidence. The numerical context inserted '
    'after this instruction is your self-review state. Recompute the node '
    'reached by following exactly one directed link from the start node. '
    'If the evidence does not support a node, reply UNKNOWN. '
    'Reply with the node name only.'
)
REVIEW_PRE_SLOT848 = list(
    tok('Previous numerical state:', add_special_tokens=False).input_ids
)
REVIEW_POST_SLOT848 = list(
    tok('Review action:', add_special_tokens=False).input_ids
)
REVISE_PRE_SLOT848 = list(
    tok('Self-review context:', add_special_tokens=False).input_ids
)

t_run841 = time.perf_counter()

assert len(JOBS841) == 27
assert set(j['arm'] for j in JOBS841) == {
    'MODEL_STATE',
    'ORDER_CONTROL',
    'NO_STATE'
}
assert set(j['intervention'] for j in JOBS841) == {
    'INTACT',
    'CONFLICT',
    'REMOVED'
}
assert len({j['qid'] for j in JOBS841}) == 3

QIDS848 = list(dict.fromkeys(j['qid'] for j in JOBS841))
CONDITIONS848 = ('INTACT', 'CONFLICT', 'REMOVED')

# Ensure physical inputs are identical across the three state arms.
for q848 in QIDS848:
    for condition848 in CONDITIONS848:
        paired848 = [
            j for j in JOBS841
            if j['qid'] == q848
            and j['intervention'] == condition848
        ]
        assert len(paired848) == 3
        assert len({tuple(j['initial_cards']) for j in paired848}) == 1
        assert len({tuple(j['bank']) for j in paired848}) == 1

# Capture one shared first-hop model state per question and intervention.
for qi848, q848 in enumerate(QIDS848):
    for ci848, condition848 in enumerate(CONDITIONS848):
        job848 = next(
            j for j in JOBS841
            if j['qid'] == q848
            and j['intervention'] == condition848
        )
        mem848 = list(job848['initial_cards'])

        assert len(mem848) < CAP845, (
            'INITIAL_MEMORY_OVER_CAPACITY',
            q848,
            condition848,
            len(mem848),
            CAP845
        )

        if qi848 == 0 and ci848 == 0:
            with CallCount841() as cc848:
                h0848 = hop845(q848, mem848, 0, None)

            UPPER_CHECK841 = cc848.summary()
            gate829(
                'CUT3_UPPER_LAYER_EXECUTION',
                (
                    UPPER_CHECK841['upper_min'] >= 1
                    and UPPER_CHECK841['lm_head'] >= 1
                ),
                UPPER_CHECK841
            )
        else:
            h0848 = hop845(q848, mem848, 0, None)

        rows848 = h0848['rows'].detach().float().cpu().contiguous()
        assert rows848.ndim == 2
        assert rows848.shape[0] > 0
        assert rows848.shape[1] == H

        key848 = (q848, condition848)
        FIRST_STATE848[key848] = rows848
        FIRST_RECORD848[key848] = {
            'text': h0848['text'],
            'unknown': bool(h0848['unk']),
            'tok1': int(h0848['tok1']),
            'p1': float(h0848['p1']),
            'entropy': float(h0848['H1']),
            'state_sha1': rkey845(rows848),
            'rows': int(rows848.shape[0])
        }

say_r41(
    'TEST848 PRE-REGISTERED HYPOTHESES',
    'H1: With identical mounted evidence, the model-generated review action '
    'can detect an unsupported first-link state and select REVISE or STOP.'
)
say_r41(
    'H2: MODEL_STATE produces more grounded correction events than '
    'ORDER_CONTROL and NO_STATE across the six answerable INTACT/CONFLICT '
    'cases; target difference is at least 2 events against each control.'
)
say_r41(
    'H3: In REMOVED, a model-generated STOP is a candidate native stop '
    'signal; Python only applies the emitted action.'
)
say_r41(
    'TEST848 PANEL',
    '3 reused worlds x 3 state arms x 3 evidence conditions = 27 jobs.'
)
say_r41(
    'TEST848 ACTION SEPARATION',
    'The model emits the review action. Python records and applies that '
    'action; it does not use labels or a correctness rule during execution.'
)

def parse_action848(text848):
    first_line848 = (text848 or '').strip().splitlines()
    if not first_line848:
        return 'INVALID'

    match848 = re.match(
        r'^\s*(CONTINUE|REVISE|STOP)\b',
        first_line848[0].strip().upper()
    )
    if match848 is None:
        return 'INVALID'
    return match848.group(1)


def generate_review848(q848, mem848, rows848):
    memx848 = memx_r41(list(mem848))
    pre848 = (
        list(prompt_ids(REVIEW_FRAME848.format(q=QTEXT841[q848])))
        + REVIEW_PRE_SLOT848
    )
    return gen845(
        memx848,
        pre848,
        rows848,
        REVIEW_POST_SLOT848
    )


def generate_revision848(q848, mem848, review_rows848):
    memx848 = memx_r41(list(mem848))
    pre848 = (
        list(prompt_ids(REVISE_FRAME848.format(q=QTEXT841[q848])))
        + REVISE_PRE_SLOT848
    )
    return gen845(
        memx848,
        pre848,
        review_rows848,
        None
    )


nj848 = len(JOBS841)
log829('TEST848_PROGRESS', 0, '/', nj848)

# Preserve the exact inherited TEST846 source-loop signature.
for ji846, j846 in enumerate(JOBS841):
    if j846['job'] in REC841:
        continue

    elapsed_minutes848 = (time.perf_counter() - T0_841) / 60.0
    if elapsed_minutes848 > HARD_BUDGET_MIN841:
        BUDGET_STOP841 = True
        log829('TEST848_BUDGET_STOP', ji846, nj848)
        break

    q848 = j846['qid']
    arm848 = j846['arm']
    condition848 = j846['intervention']
    mem848 = list(j846['initial_cards'])

    first_key848 = (q848, condition848)
    first_rows848 = FIRST_STATE848[first_key848]
    first_record848 = FIRST_RECORD848[first_key848]

    if arm848 == 'MODEL_STATE':
        review_input848 = first_rows848

    elif arm848 == 'ORDER_CONTROL':
        review_input848 = torch.flip(
            first_rows848,
            dims=[0]
        ).contiguous()

        assert tuple(review_input848.shape) == tuple(first_rows848.shape)

        native_norms848 = torch.linalg.vector_norm(
            first_rows848,
            dim=1
        )
        control_norms848 = torch.linalg.vector_norm(
            review_input848,
            dim=1
        )
        expected_norms848 = torch.flip(native_norms848, dims=[0])

        assert torch.allclose(
            control_norms848,
            expected_norms848,
            atol=1e-6,
            rtol=1e-6
        ), 'ORDER_CONTROL_ROW_NORM_MISMATCH'

        assert torch.equal(
            review_input848,
            torch.flip(first_rows848, dims=[0])
        ), 'ORDER_CONTROL_NOT_EXACT_ROW_REVERSAL'

    elif arm848 == 'NO_STATE':
        review_input848 = None

    else:
        raise ValueError(('UNEXPECTED_ARM', arm848))

    # Model-native review generation. The previous answer text is not
    # replayed; only the selected numerical state is inserted.
    review848 = generate_review848(
        q848,
        mem848,
        review_input848
    )
    decision848 = parse_action848(review848['text'])

    revised848 = None
    final848 = None
    applied848 = None

    # This branch applies the model's explicit action.
    # It does not infer whether that action is correct.
    if decision848 == 'STOP':
        applied848 = 'APPLY_MODEL_STOP'

    elif decision848 == 'REVISE':
        applied848 = 'APPLY_MODEL_REVISE'
        revised848 = generate_revision848(
            q848,
            mem848,
            review848['rows']
        )
        final848 = hop845(
            q848,
            mem848,
            1,
            revised848['rows']
        )

    elif decision848 == 'CONTINUE':
        applied848 = 'APPLY_MODEL_CONTINUE'
        revised848 = {
            'text': first_record848['text'],
            'rows': first_rows848,
            'tok1': first_record848['tok1'],
            'p1': first_record848['p1'],
            'H1': first_record848['entropy'],
            'state_sha1': first_record848['state_sha1']
        }
        final848 = hop845(
            q848,
            mem848,
            1,
            first_rows848
        )

    else:
        # Protocol failure is recorded separately; it is not counted as a
        # model-native STOP decision.
        applied848 = 'PROTOCOL_INVALID_NO_FOLLOWUP'

    review_rows848 = (
        review848['rows'].detach().float().cpu().contiguous()
    )
    if revised848 is not None:
        revised_rows848 = (
            revised848['rows'].detach().float().cpu().contiguous()
        )
    else:
        revised_rows848 = torch.zeros((0, H), dtype=torch.float32)

    if final848 is not None:
        final_rows848 = (
            final848['rows'].detach().float().cpu().contiguous()
        )
        final_text848 = final848['text']
        final_unknown848 = bool(final848['unk'])
        final_tok1848 = int(final848['tok1'])
        final_p1848 = float(final848['p1'])
        final_entropy848 = float(final848['H1'])
    else:
        final_rows848 = torch.zeros((0, H), dtype=torch.float32)
        final_text848 = None
        final_unknown848 = None
        final_tok1848 = None
        final_p1848 = None
        final_entropy848 = None

    rec848 = {
        'job': j846['job'],
        'qid': q848,
        'arm': arm848,
        'condition': condition848,
        'mounted_cards': list(mem848),
        'search_bank_size': len(j846['bank']),

        'first_text': first_record848['text'],
        'first_unknown': first_record848['unknown'],
        'first_tok1': first_record848['tok1'],
        'first_p1': first_record848['p1'],
        'first_entropy': first_record848['entropy'],
        'first_state_sha1': first_record848['state_sha1'],

        'review_text': review848['text'],
        'review_decision': decision848,
        'review_tok1': int(review848['tok1']),
        'review_p1': float(review848['p1']),
        'review_entropy': float(review848['H1']),
        'review_state_sha1': rkey845(review_rows848),

        'python_action': applied848,
        'revision_text': (
            None if revised848 is None else revised848['text']
        ),
        'revision_state_sha1': (
            None if revised848 is None else rkey845(revised_rows848)
        ),

        'final_text': final_text848,
        'final_unknown': final_unknown848,
        'final_tok1': final_tok1848,
        'final_p1': final_p1848,
        'final_entropy': final_entropy848,

        'model_stop_decision': (
            decision848 == 'STOP'
        ),
        'protocol_invalid': decision848 == 'INVALID',
        'grounded_result': 'OFFLINE_PENDING'
    }

    np_rows848 = {
        'first_rows': first_rows848.numpy(),
        'review_input_rows': (
            np.empty((0, H), dtype=np.float32)
            if review_input848 is None
            else review_input848.detach().float().cpu().numpy()
        ),
        'review_output_rows': review_rows848.numpy(),
        'revision_rows': revised_rows848.numpy(),
        'final_rows': final_rows848.numpy()
    }

    REC841[j846['job']] = rec848
    ROWS841[j846['job']] = np_rows848
    save_job841(j846['job'], rec848, np_rows848)

    say_r41(
        'TEST848 CASE',
        'WORLD=%d' % QID841.index(q848),
        'CONDITION=' + condition848,
        'ARM=' + arm848,
        'FIRST=%r' % first_record848['text'][:36],
        'MODEL_SIGNAL=' + decision848,
        'PYTHON_ACTION=' + applied848,
        'REVISION=%r' % (
            None if revised848 is None else revised848['text'][:36]
        ),
        'FINAL=%r' % (
            None if final_text848 is None else final_text848[:36]
        )
    )

    log829(
        'TEST848_PROGRESS',
        ji846 + 1,
        '/',
        nj848,
        arm848,
        condition848
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


# ======================================================================
# 5. OFFLINE EVALUATION
# Ground-truth labels are accessed only after model execution.
# ======================================================================

OFF848 = r'''
log829('TEST846P_OFFLINE_START')
log829('TEST848_OFFLINE_START')

def classify_node848(text848, world848):
    upper848 = str(text848 or '').strip().upper()
    candidates848 = (
        'middle',
        'end',
        'changed_end',
        'fork_end',
        'decoy_end'
    )
    hits848 = [
        key848
        for key848 in candidates848
        if str(world848.get(key848, '')).strip()
        and str(world848[key848]).strip().upper() in upper848
    ]
    if len(hits848) == 1:
        return hits848[0]
    if len(hits848) > 1:
        return 'AMBIGUOUS'
    return 'OTHER'


completed848 = [
    REC841[j['job']]
    for j in JOBS841
    if j['job'] in REC841
]

offline848 = []
paired848 = {}

for r848 in completed848:
    wi848 = QID841.index(r848['qid'])
    world848 = worlds829[wi848]
    ids848 = world848['ids']
    mounted848 = set(r848['mounted_cards'])

    first_class848 = classify_node848(
        r848['first_text'],
        world848
    )
    revision_class848 = (
        classify_node848(r848['revision_text'], world848)
        if r848['revision_text'] is not None
        else None
    )
    final_class848 = (
        classify_node848(r848['final_text'], world848)
        if r848['final_text'] is not None
        else None
    )

    first_correct848 = first_class848 == 'middle'
    first_wrong848 = not first_correct848

    answer_correct848 = final_class848 in ('end', 'changed_end')
    if final_class848 == 'end':
        final_card848 = ids848['second']
    elif final_class848 == 'changed_end':
        final_card848 = ids848['changed']
    else:
        final_card848 = None

    grounded848 = bool(
        answer_correct848
        and ids848['first'] in mounted848
        and final_card848 in mounted848
    )

    correction_event848 = bool(
        first_wrong848
        and r848['review_decision'] == 'REVISE'
        and revision_class848 == 'middle'
        and final_class848 in ('end', 'changed_end')
        and grounded848
    )

    correct_removed_stop848 = bool(
        r848['condition'] == 'REMOVED'
        and r848['review_decision'] == 'STOP'
    )

    false_stop848 = bool(
        r848['condition'] != 'REMOVED'
        and r848['review_decision'] == 'STOP'
    )

    unsupported_removed_answer848 = bool(
        r848['condition'] == 'REMOVED'
        and r848['final_text'] is not None
        and answer_correct848
        and not grounded848
    )

    row848 = {
        'world': wi848,
        'condition': r848['condition'],
        'arm': r848['arm'],
        'first_class': first_class848,
        'first_correct': first_correct848,
        'review_decision': r848['review_decision'],
        'revision_class': revision_class848,
        'final_class': final_class848,
        'answer_correct': answer_correct848,
        'grounded': grounded848,
        'correction_event': correction_event848,
        'correct_removed_stop': correct_removed_stop848,
        'false_stop': false_stop848,
        'unsupported_removed_answer': unsupported_removed_answer848,
        'protocol_invalid': r848['protocol_invalid'],
        'python_action': r848['python_action'],
        'first_text': r848['first_text'],
        'review_text': r848['review_text'],
        'revision_text': r848['revision_text'],
        'final_text': r848['final_text']
    }
    offline848.append(row848)

    paired848.setdefault(
        (wi848, r848['condition']),
        {}
    )[r848['arm']] = row848


correction_by_arm848 = {
    arm848: sum(
        row848['correction_event']
        for row848 in offline848
        if row848['arm'] == arm848
        and row848['condition'] in ('INTACT', 'CONFLICT')
    )
    for arm848 in PILOT_ARMS846
}

conflict_corrections848 = {
    arm848: sum(
        row848['correction_event']
        for row848 in offline848
        if row848['arm'] == arm848
        and row848['condition'] == 'CONFLICT'
    )
    for arm848 in PILOT_ARMS846
}

removed_stops848 = {
    arm848: sum(
        row848['correct_removed_stop']
        for row848 in offline848
        if row848['arm'] == arm848
    )
    for arm848 in PILOT_ARMS846
}

unsupported_removed848 = sum(
    row848['unsupported_removed_answer']
    for row848 in offline848
)

paired_deltas848 = {
    arm848: (
        correction_by_arm848['MODEL_STATE']
        - correction_by_arm848[arm848]
    )
    for arm848 in ('ORDER_CONTROL', 'NO_STATE')
}

primary_pass848 = bool(
    correction_by_arm848['MODEL_STATE']
    >= correction_by_arm848['ORDER_CONTROL'] + 2
    and correction_by_arm848['MODEL_STATE']
    >= correction_by_arm848['NO_STATE'] + 2
    and conflict_corrections848['MODEL_STATE'] >= 2
)

complete848 = (
    not BUDGET_STOP841
    and len(completed848) == 27
)

checks848 = D829.get('checks', [])
physical_ok848 = bool(checks848) and all(
    c.get('pass', False) for c in checks848
)

if not complete848:
    verdict848 = 'INCOMPLETE_PILOT'
elif primary_pass848:
    verdict848 = 'PRELIMINARY_NATIVE_CORRECTION_SIGNAL'
else:
    verdict848 = 'PRIMARY_CORRECTION_HYPOTHESIS_NOT_SUPPORTED'

# Per-world and per-condition paired summary.
for key848, arms848 in sorted(paired848.items()):
    wi848, condition848 = key848
    say_r41(
        'TEST848 PAIRED',
        'WORLD=%d' % wi848,
        'CONDITION=' + condition848,
        'MODEL_CORRECT=' + str(
            arms848.get('MODEL_STATE', {}).get('correction_event', False)
        ),
        'ORDER_CORRECT=' + str(
            arms848.get('ORDER_CONTROL', {}).get('correction_event', False)
        ),
        'NO_STATE_CORRECT=' + str(
            arms848.get('NO_STATE', {}).get('correction_event', False)
        )
    )

say_r41('TEST848 SOURCE VERIFICATION')
say_r41(
    'TEST847_GIT_BLOB_SHA1='
    '72ce35daa728f546d92baa26705dd04ed5ad6a11'
)
say_r41(
    'TEST846_GIT_BLOB_SHA1='
    '6093896b7e4492f201cece448ad1646b0bd8820a'
)
say_r41(
    'TEST845_GIT_BLOB_SHA1='
    'be81a587b3d2b8cd3e9291df6bd9fb481c4c2164'
)

say_r41('TEST848 ENGINE INTEGRITY')
say_r41('Inherited TEST847 -> TEST846 -> TEST845 motor and safety gates retained.')
say_r41('No residual hooks, training, LoRA, RAG, text replay, or oracle routing.')
say_r41(
    'Python applies only the model-emitted CONTINUE, REVISE, or STOP action.'
)

say_r41('TEST848 HARDWARE AND MODEL')
say_r41('Hardware/model values are reported by inherited preflight.')
say_r41('GPU execution status is determined by this run, not assumed here.')

say_r41('TEST848 PHYSICAL MEMORY INTEGRITY')
say_r41(
    'PHYSICAL_MEMORY_INTEGRITY='
    + ('PASS' if physical_ok848 else 'FAIL_OR_UNAVAILABLE')
)

say_r41('TEST848 EXPERIMENTAL HYPOTHESIS')
say_r41(
    'MODEL_STATE should produce at least two more grounded correction events '
    'than each state control across the six INTACT/CONFLICT pairs, with at '
    'least two grounded corrections in CONFLICT.'
)

say_r41('TEST848 NATIVE SIGNAL OBSERVATIONS')
for arm848 in PILOT_ARMS846:
    cases848 = [x for x in offline848 if x['arm'] == arm848]
    say_r41(
        'ARM=%s WRONG_FIRST=%d REVISE=%d STOP=%d INVALID=%d'
        % (
            arm848,
            sum(not x['first_correct'] for x in cases848),
            sum(x['review_decision'] == 'REVISE' for x in cases848),
            sum(x['review_decision'] == 'STOP' for x in cases848),
            sum(x['protocol_invalid'] for x in cases848)
        )
    )

say_r41('TEST848 CAUSAL INTERVENTION RESULTS')
say_r41(
    'GROUNDED_CORRECTION MODEL=%d ORDER=%d NO_STATE=%d'
    % (
        correction_by_arm848['MODEL_STATE'],
        correction_by_arm848['ORDER_CONTROL'],
        correction_by_arm848['NO_STATE']
    )
)
say_r41(
    'CONFLICT_CORRECTION MODEL=%d ORDER=%d NO_STATE=%d'
    % (
        conflict_corrections848['MODEL_STATE'],
        conflict_corrections848['ORDER_CONTROL'],
        conflict_corrections848['NO_STATE']
    )
)
say_r41(
    'REMOVED_STOP MODEL=%d ORDER=%d NO_STATE=%d UNSUPPORTED_REMOVED=%d'
    % (
        removed_stops848['MODEL_STATE'],
        removed_stops848['ORDER_CONTROL'],
        removed_stops848['NO_STATE'],
        unsupported_removed848
    )
)

say_r41('TEST848 JOB-BY-JOB EVALUATION')
for row848 in offline848:
    say_r41(
        'WORLD=%d CONDITION=%s ARM=%s FIRST=%s ACTION=%s REVISION=%s '
        'FINAL=%s GROUNDED=%s CORRECTION=%s STOP_OK=%s'
        % (
            row848['world'],
            row848['condition'],
            row848['arm'],
            row848['first_class'],
            row848['review_decision'],
            row848['revision_class'],
            row848['final_class'],
            row848['grounded'],
            row848['correction_event'],
            row848['correct_removed_stop']
        )
    )

say_r41('TEST848 MODEL SIGNAL VS PYTHON ACTION')
say_r41(
    'MODEL_SIGNAL=generated review action and generated numerical review rows.'
)
say_r41(
    'PYTHON_ACTION=literal protocol application: CONTINUE, REVISE, STOP.'
)
say_r41(
    'Invalid action strings are PROTOCOL_INVALID, never counted as model STOP.'
)

say_r41('TEST848 ERROR RECOGNITION')
say_r41(
    'A recognition event requires an offline-confirmed wrong first node '
    'followed by a model-generated REVISE action.'
)

say_r41('TEST848 EVIDENCE PRESERVATION')
say_r41(
    'No card is retracted by Python. Grounded correction requires the '
    'pre-mounted first card and the answer-supporting second/changed card.'
)

say_r41('TEST848 FAILURE ANALYSIS')
say_r41(
    'REMOVED tests evidence insufficiency; unsupported completion is counted '
    'separately. CONTINUE/REVISE/STOP outputs are model signals; Python only '
    'executes their fixed meanings. Correct stopping is not inferred from '
    'Python budgets or UNKNOWN parsing.'
)

say_r41('TEST848 FINAL SCIENTIFIC VERDICT')
say_r41('PRIMARY_VERDICT=' + verdict848)
say_r41(
    'MODEL_NATIVE_STOP_DECISION='
    + (
        'PRELIMINARY_SIGNAL'
        if sum(removed_stops848.values()) > 0
        else 'NOT_OBSERVED'
    )
)
say_r41('AUTONOMOUS_RECURSIVE_REASONING=NOT_DEMONSTRATED')
say_r41(
    'INTERPRETATION: ' +
    'The experiment tests one model-generated review/action/correction '
    'cycle. It does not test open-ended research or autonomous card search.'
)

report848 = (
    'TEST848 completed %d of 27 jobs across three previously used worlds, '
    'three state conditions and three evidence conditions. Grounded '
    'correction events were MODEL_STATE=%d, ORDER_CONTROL=%d and NO_STATE=%d; '
    'CONFLICT corrections were %d, %d and %d. Correct model-emitted STOP '
    'actions in REMOVED were %d, %d and %d; unsupported REMOVED answers=%d. '
    'The primary criterion was %s. These results can support only a '
    'preliminary one-cycle native review/correction signal. They do not '
    'establish autonomous evidence search, card-level retention decisions, '
    'open-ended recursion, or general reasoning.'
    % (
        len(completed848),
        correction_by_arm848['MODEL_STATE'],
        correction_by_arm848['ORDER_CONTROL'],
        correction_by_arm848['NO_STATE'],
        conflict_corrections848['MODEL_STATE'],
        conflict_corrections848['ORDER_CONTROL'],
        conflict_corrections848['NO_STATE'],
        removed_stops848['MODEL_STATE'],
        removed_stops848['ORDER_CONTROL'],
        removed_stops848['NO_STATE'],
        unsupported_removed848,
        verdict848
    )
)
say_r41('TEST848 SCIENTIFIC REPORT')
say_r41(report848)

D829['test848'] = {
    'status': 'COMPLETE' if complete848 else 'INCOMPLETE',
    'jobs_expected': 27,
    'jobs_completed': len(completed848),
    'primary_verdict': verdict848,
    'correction_by_arm': correction_by_arm848,
    'conflict_corrections_by_arm': conflict_corrections848,
    'removed_stops_by_arm': removed_stops848,
    'unsupported_removed_answers': unsupported_removed848,
    'physical_memory_integrity': (
        'PASS' if physical_ok848 else 'FAIL_OR_UNAVAILABLE'
    ),
    'autonomous_recursive_reasoning': 'NOT_DEMONSTRATED',
    'cases': offline848,
    'paired': [
        {
            'world': pair_key848[0],
            'condition': pair_key848[1],
            'arms': pair_value848
        }
        for pair_key848, pair_value848 in sorted(
            paired848.items(),
            key=lambda item: (item[0][0], item[0][1])
        )
    ],
    'report': report848
}

D829['verdict841R'] = {
    'decision': verdict848,
    'verdicts': {
        'PHYSICAL_MEMORY_INTEGRITY': (
            'PASS' if physical_ok848 else 'FAIL_OR_UNAVAILABLE'
        ),
        'MODEL_NATIVE_ERROR_SIGNAL': (
            'PRELIMINARY_SIGNAL'
            if any(
                (not x['first_correct'])
                and x['review_decision'] == 'REVISE'
                for x in offline848
            )
            else 'NOT_OBSERVED'
        ),
        'MODEL_NATIVE_CORRECTION': (
            'PRELIMINARY_SIGNAL'
            if sum(correction_by_arm848.values()) > 0
            else 'NOT_OBSERVED'
        ),
        'MODEL_NATIVE_STOP_DECISION': (
            'PRELIMINARY_SIGNAL'
            if sum(removed_stops848.values()) > 0
            else 'NOT_OBSERVED'
        ),
        'AUTONOMOUS_RECURSIVE_REASONING': 'NOT_DEMONSTRATED'
    },
    'budget_stop': BUDGET_STOP841
}

D829['status'] = (
    'COMPLETE_TEST848' if complete848 else 'PARTIAL_TEST848'
)
log829('TEST848_FINAL', verdict848)
save829()
log829('TEST848_COMPLETED', str(OUT829))
'''


# ======================================================================
# 6. PATCH LOCKED TEST847 DRIVER
# ======================================================================

SRC848 = replace_module_assignment848(
    SRC848, "PANEL_TAIL847", PANEL_TAIL848
)
SRC848 = replace_module_assignment848(
    SRC848, "RUN847", RUN848
)
SRC848 = replace_module_assignment848(
    SRC848, "OFF847", OFF848
)

SRC848 = SRC848.replace("TEST847", "TEST848")

# Replace inherited TEST847 claims with this test's registered panel.
SRC848 = replace_exact_once848(
    SRC848,
    'print("MODEL_STATE vs MATCHED_CONTROL: +2 grounded outcomes across six INTACT/CONFLICT pairs,")',
    'print("Primary comparison: MODEL_STATE vs ORDER_CONTROL vs NO_STATE.")'
)
SRC848 = replace_exact_once848(
    SRC848,
    'print("and at least two grounded conflict rescues, exceeding MATCHED_CONTROL.")',
    'print("Correction requires a wrong first node, REVISE, corrected node, and grounded final answer.")'
)
SRC848 = replace_exact_once848(
    SRC848,
    'print("Python-triggered backtracking and mechanical stops are not model-native correction.")',
    'print("Python applies only explicit model actions; invalid output is not a model stop.")'
)
SRC848 = replace_exact_once848(
    SRC848,
    'print("Arms: MODEL_STATE, MATCHED_CONTROL, CUE_BASELINE")',
    'print("Arms: MODEL_STATE, ORDER_CONTROL, NO_STATE")'
)
SRC848 = replace_exact_once848(
    SRC848,
    'print("Interventions: INTACT, CONFLICT, REMOVED")',
    'print("Conditions: INTACT, CONFLICT, REMOVED")'
)

ast.parse(SRC848)


# ======================================================================
# 7. STATIC SECURITY AND INHERITED SOURCE-GATE CHECKS
# ======================================================================

tree848 = ast.parse(SRC848)
assign848 = {}

for node848 in tree848.body:
    if isinstance(node848, ast.Assign) and len(node848.targets) == 1:
        target848 = node848.targets[0]
        if isinstance(target848, ast.Name):
            assign848[target848.id] = node848.value

for name848 in ("PANEL_TAIL847", "RUN847", "OFF847"):
    assert name848 in assign848, (
        'EMBEDDED_ASSIGNMENT_MISSING',
        name848
    )
    assert isinstance(assign848[name848], ast.Constant)
    assert isinstance(assign848[name848].value, str)
    ast.parse(assign848[name848].value)

panel_text848 = assign848['PANEL_TAIL847'].value
run_text848 = assign848['RUN847'].value
off_text848 = assign848['OFF847'].value

run_ast848 = ast.parse(run_text848)
run_names848 = {
    node848.id
    for node848 in ast.walk(run_ast848)
    if isinstance(node848, ast.Name)
}

for forbidden848 in (
    'EVALKEY841',
    'CONTENT841',
    'worlds829',
    'card_meta829'
):
    assert forbidden848 not in run_names848, (
        'LABEL_OR_GROUND_TRUTH_ACCESS_IN_RUN',
        forbidden848
    )

# The locked TEST846 source requires this exact loop string.
assert 'for ji846, j846 in enumerate(JOBS841)' in run_text848
assert 'for ji845, j845 in enumerate(JOBS841)' not in run_text848

job_loops848 = []
for node848 in ast.walk(run_ast848):
    if not isinstance(node848, ast.For):
        continue
    target_names848 = {
        item848.id
        for item848 in ast.walk(node848.target)
        if isinstance(item848, ast.Name)
    }
    if 'j846' in target_names848:
        job_loops848.append(node848)

assert len(job_loops848) == 1, (
    'EXPERIMENTAL_JOB_LOOP_COUNT',
    len(job_loops848)
)

job_loop848 = job_loops848[0]
assert isinstance(job_loop848.target, ast.Tuple)
assert isinstance(job_loop848.iter, ast.Call)
assert isinstance(job_loop848.iter.func, ast.Name)
assert job_loop848.iter.func.id == 'enumerate'
assert len(job_loop848.iter.args) == 1
assert isinstance(job_loop848.iter.args[0], ast.Name)
assert job_loop848.iter.args[0].id == 'JOBS841'

assert 'PILOT_WORLDS846 = (0, 1, 2)' in panel_text848
assert 'assert len(JOBS841) == 27' in panel_text848
assert 'TEST846P_OFFLINE_START' in off_text848

for forbidden_text848 in (
    'addr845(',
    'DEAD_END_BACKTRACK',
    'SMAX845',
    'EVALKEY841',
    'CONTENT841'
):
    assert forbidden_text848 not in run_text848, (
        'FORBIDDEN_RUN_TEXT',
        forbidden_text848
    )

ast.parse(SRC848)
ast.parse(panel_text848)
ast.parse(run_text848)
ast.parse(off_text848)


# ======================================================================
# 8. PREFLIGHT OUTPUT AND EXECUTION
# ======================================================================

print("=" * 78)
print("AKBASCORE SILICON HIPPOCAMPUS — TEST848")
print("TEST848 SOURCE VERIFICATION")
print("TEST847 Git blob SHA1:", LOCK847_848)
print("TEST846 Git blob SHA1:", "6093896b7e4492f201cece448ad1646b0bd8820a")
print("TEST845 Git blob SHA1:", "be81a587b3d2b8cd3e9291df6bd9fb481c4c2164")
print("SOURCE AST: PASS")
print("PANEL/RUN/OFF AST: PASS")
print("RUN LABEL ISOLATION AST: PASS")
print("EXPERIMENTAL JOB LOOP: PASS")
print("=" * 78)
print("TEST848 EXPERIMENTAL PANEL")
print("3 existing worlds x 3 actions arms x 3 evidence conditions = 27 jobs")
print("MODEL_STATE | ORDER_CONTROL | NO_STATE")
print("INTACT | CONFLICT | REMOVED")
print("GPU EXECUTION: NOT VERIFIED HERE")
print("=" * 78, flush=True)

exec(
    compile(
        SRC848,
        "TEST848_LOCKED_TEST847_BASE",
        "exec"
    ),
    globals()
)
