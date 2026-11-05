# AKBASCORE SILICON HIPPOCAMPUS — TEST863 NATIVE STATE REACHABILITY AND CLOSED-LOOP TRANSITION AUDIT
# Locked GPU-verified TEST862/861/860/859 observer spine; unchanged INTACT and REMOVED jobs.
# Native reachability is read only from original executions. Exact restore is diagnostic replay.
# No motor, memory acquisition, candidate architecture, decision rule or review-limit modification.
# GPU execution is not claimed by the author.
import ast
import builtins
import contextlib
import copy
import gc
import hashlib
import io
import json
import pathlib
import re
import symtable
import sys
import time
import traceback
import urllib.request
import zipfile

TEST863_KIND = 'NATIVE_STATE_REACHABILITY_AND_CLOSED_LOOP_TRANSITION_AUDIT'
CODELOAD863 = 'https://codeload.github.com/ceceli33/titan-cognitive-core-v3/zip/refs/heads/main'
LOCKS863 = {
    '849.py': '01a6ac43cbc954cc2f6ceaf8cf0238333ec762b1',
    '850.py': '79cc5ab211c01b37324e2d6897a298e84db42101',
    '851.py': '0f01e73b9ad160c988cfe059e8b5ae5e1f35f65b',
    '852.py': '4174e9241f773d6a031c51296b6beb11d4637aa5',
    '853.py': 'a7033caa10fdb86f8f0ee0b8ed1a0ac7514e26be',
    '854.py': 'a158d92a61c15a5e71468146d6c1ceeaedce436c',
    '850.log': 'c070ef432e95f80cd9a1c28318fd2e4a10377296',
    '851.log': 'b38419ef3a069ea4e20d43d15e6d939318083a9a',
    '852.log': 'b434a1e36b22fd99f9590c8b98b8094e927db458',
    '853.log': '0bfa9104337c44adaf4a07ec0ce6b5e41f457494',
    '854.log': '2aa1f85e14d52acbd1ecbad5b5c7df10df0bbcd4',
    '855.py': '8ab79676aded54cb30316c47feeeae8b89fb4625',
    '856.py': '93d7e9bd7ebc6c692cef0e1e62d05ad96e4086d1',
    '857.py': '0891ffe2d638e7a17ff9e851d160c2afeb609a1a',
    '855.log': 'afb58577e700031a4f788940ab4b8e7a69b59999',
    '856.log': '875a1d5fb3ad5c45700c4ebab17402a3c9b27bb3',
    '857.log': 'ef3ae882ecf03dd9b9668939bd55ce65eeae8455',
    '858.py': 'f78efd24b2fd6dfd2072933f2e99382a50422ceb',
    '858.log': '6c3ab3e9a5887c2d90cf5f55c9ef55f2d7249209',
    '859.py': '0c7cb37e2dff71e6f1798362a4e3ebee12c71ae9',
    '859.log': 'b080c81d4fdcc1be0e5a11df500abfb6d7b98707',
    '860.py': 'd352c7f993f30685ef366e5008eac7c5a45cc9e2',
    '860.log': '3eac77232332b944960fdf3a40cac2cbfa38c282',
    '861.py': '4c61c1f021c92b3f701220a10f0927c8b2d89c3b',
    '861.log': '2e57ff2f20db600350c41ba7c7b4add3b2b11924',
    '862.py': '40857dd575041ebbee02879da92a98755c7686e4',
    '862.log': '91980c52bc5b98bee3c94cce67756093ace9a6a0',
}
STATE_REL_L2_EPS863 = 1e-7
SCORE_ABS_EPS863 = 1e-6
REGRESSION_ABS_EPS863 = 1e-5
STATE_ORDER863 = ('C', 'E', 'U', 'R', 'Kprev', 'K0', 'J', 'Review', 'Revision')
STAMP863 = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
ROOT863 = pathlib.Path('/content') / ('TEST863_NATIVE_REACHABILITY_' + STAMP863)
ROOT863.mkdir(parents=True, exist_ok=False)
CONSOLE863, ERROR_CONSOLE863 = sys.stdout, sys.stderr
LOG_FILE863 = open(ROOT863 / '863.log', 'w', encoding='utf-8')
START863 = time.perf_counter()
REAL_COMPILE863 = builtins.compile
RAW_SOURCES863 = {}
STATE863 = {'spine_loaded': False, 'dependency_audit': {}, 'original_record_sha256': None,
    'memory': {}, 'candidates': {}, 'joint': {}, 'transitions': {}, 'xray': {},
    'restores': [], 'analysis': {}}
RUNTIME863 = {}
EXECUTION_ERROR863 = None
ANALYSIS_ERROR863 = None
TRACEBACK863 = ''
ERROR_EVIDENCE863 = {}
TWO_JOB_VERIFICATION863 = {}
ANALYSIS863 = {}
DIAGNOSTIC_CONTROL_STOP863 = None

# Compatibility namespaces execute selected old definitions, never old experiment bodies.
ROOT862 = ROOT861 = ROOT860 = ROOT859 = ROOT863
LOG_FILE862 = LOG_FILE861 = LOG_FILE860 = LOG_FILE859 = LOG_FILE863
START862 = START861 = START860 = START859 = START863
CONSOLE862 = CONSOLE861 = CONSOLE860 = CONSOLE859 = CONSOLE863
ERROR_CONSOLE862 = ERROR_CONSOLE861 = ERROR_CONSOLE860 = ERROR_CONSOLE859 = ERROR_CONSOLE863
REAL_COMPILE862 = REAL_COMPILE861 = REAL_COMPILE860 = REAL_COMPILE859 = REAL_COMPILE863
RAW_SOURCES862 = RAW_SOURCES861 = RAW_SOURCES860 = RAW_SOURCES859 = RAW_SOURCES863
LOCKS862 = {k: v for k, v in LOCKS863.items() if not k.startswith('862.')}
LOCKS861 = {k: v for k, v in LOCKS862.items() if not k.startswith('861.')}
STATE_REL_L2_EPS862 = STATE_REL_L2_EPS861 = STATE_REL_L2_EPS863
SCORE_ABS_EPS862 = SCORE_ABS_EPS861 = SCORE_ABS_EPS863
REGRESSION_ABS_EPS862 = REGRESSION_ABS_EPS861 = REGRESSION_ABS_EPS863
STATE862 = {'spine_loaded': False, 'dependency_audit': {}}
STATE861 = {'spine_loaded': False, 'spine_json': {}, 'native_sequences': {},
    'arms': {}, 'comparisons': [], 'analysis': {}, 'diagnostic_executions': 0,
    'original_record_sha256': None, 'dependency_audit': {}}
STATE860 = {'spine_loaded': False, 'spine_json': {}, 'conditions': [],
    'native_sequences': {}, 'condition_results': [], 'comparisons': [],
    'analysis': {}, 'original_record_sha256': None}
STATE859 = {'installed': False, 'compiled': False, 'equalities': [],
    'observations': [], 'coverage': [], 'frames': [], 'g': None, 'active': None,
    'capture': None, 'tokenizations': {}, 'hook_audits': [], 'saved_jobs': [],
    'invocations': [], 'contexts': [], 'transitions': {}, 'offline_functions': {},
    'decision_comparison': {}, 'causal_probes': [], 'original_record_sha256': None,
    'environment': {}, 'start': START863}
FAILURES859 = []
LAST_CONTEXT859 = None
SPELLINGS859 = (' CONTINUE', ' REVISE', ' STOP', ' SUFFICIENT', ' INSUFFICIENT')


def short863(*args):
    text = ' '.join(str(x) for x in args)
    print(text, file=CONSOLE863, flush=True)
    LOG_FILE863.write(text + '\n')
    LOG_FILE863.flush()


def json_write863(name, value):
    path = ROOT863 / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
        allow_nan=False), encoding='utf-8')
    return path


def sha256_bytes863(data):
    return hashlib.sha256(data).hexdigest()


def git_blob863(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


short862 = short861 = short863
json_write862 = json_write861 = json_write863
sha256_bytes862 = sha256_bytes861 = sha256_bytes863
git_blob862 = git_blob861 = git_blob863


def capture_cell_source863():
    try:
        shell = get_ipython()  # noqa: F821 — supplied by Colab/IPython.
        history = list(shell.history_manager.input_hist_raw)
        marker = 'AKBASCORE SILICON HIPPOCAMPUS — TEST863 NATIVE STATE REACHABILITY AND CLOSED-LOOP TRANSITION AUDIT'
        candidates = [text for text in history if marker in text]
        if candidates:
            (ROOT863 / '863.py').write_text(candidates[-1], encoding='utf-8')
            return True
    except Exception as exc:
        short863('TABLE A SOURCE_CAPTURE job=GLOBAL cycle=NA execution=NATIVE_OBSERVATION_ONLY',
            type(exc).__name__, str(exc))
    return False


def load_sources863():
    request = urllib.request.Request(CODELOAD863,
        headers={'User-Agent': 'AKBASCORE-TEST863-GATE0'})
    with urllib.request.urlopen(request, timeout=240) as response:
        archive = response.read(100000001)
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        for name, expected in LOCKS863.items():
            matches = [n for n in zipped.namelist() if n.endswith('/' + name)]
            assert len(matches) == 1, ('SOURCE_NOT_UNIQUE', name, matches)
            data = zipped.read(matches[0])
            actual = git_blob863(data)
            assert actual == expected, ('SOURCE_GIT_BLOB_MISMATCH', name, expected, actual)
            RAW_SOURCES863[name] = data
            short863('TABLE A SOURCE', name, actual,
                'job=GLOBAL cycle=NA execution=NATIVE_OBSERVATION_ONLY PASS')
    assert len(RAW_SOURCES863) == 27
    return RAW_SOURCES863


def _selected862_nodes863():
    tree = ast.parse(RAW_SOURCES863['862.py'].decode('utf-8'), filename='862.py')
    names = {'_selected861_nodes862', 'load_spine862', 'native_closure862',
        'evidence_sufficient862'}
    nodes = [copy.deepcopy(n) for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == names
    return tree, nodes


def load_spine863():
    assert not STATE863['spine_loaded']
    tree862, nodes862 = _selected862_nodes863()
    exec(REAL_COMPILE863(ast.fix_missing_locations(ast.Module(
        body=nodes862, type_ignores=[])),
        'TEST863_REUSED_862_DEFINITIONS_ONLY', 'exec'), globals())
    load_spine862()
    tree861, nodes861 = _selected861_nodes862()
    tree860, nodes860 = _selected860_nodes861()
    nodes859 = _selected859_nodes861(tree860)
    _dependency_audit861(nodes862 + nodes861 + nodes860 + nodes859)
    STATE863['dependency_audit'] = copy.deepcopy(STATE861['dependency_audit'])
    STATE863['spine_loaded'] = True
    short863('TABLE A SPINE job=GLOBAL cycle=NA execution=NATIVE_OBSERVATION_ONLY',
        '862+861+860+859 selected definitions only; top-level experiment exec=0; missing=0')


def parse_reference862():
    text = RAW_SOURCES863['862.log'].decode('utf-8')
    required = (
        'TEST862 TECHNICAL TECHNICAL_FACTORIAL_XRAY_PASS',
        'TEST862 NATIVE CLOSURE NATIVE_AUTONOMOUS_CLOSURE_NOT_OBSERVED',
        'GATE0_SOURCE_INTEGRITY PASS',
        'GATE1_HOOKFREE_ORIGINAL_TWO_JOBS PASS',
        'GATE2_OBSERVER_EQUIVALENCE PASS',
        'GATE3_NATIVE_861_REGRESSION_AND_C1_GENERATION PASS',
        'GATE4_FACTORIAL_CONDITION_VALIDITY PASS',
        'GATE5_RESTORE_AND_SAME_STATE_REPLAY PASS',
        'GATE9_ARTIFACT_INTEGRITY PASS')
    for item in required:
        assert item in text, ('REFERENCE_862_GATE_MISSING', item)
    match = re.search(r'^TABLE K GREEDY TRANSITIONS (\{.*\})$', text, re.MULTILINE)
    assert match, 'REFERENCE_862_FACTORIAL_ACTIONS_MISSING'
    actions = json.loads(match.group(1))
    expected = {'C0E0': 'REVISE', 'C1E0': 'REVISE',
        'C0E1': 'REVISE', 'C1E1': 'CONTINUE'}
    assert all(actions[k] == v for k, v in expected.items()), actions
    native_rows = []
    pattern = re.compile(
        r'^TABLE B ORIGINAL NATIVE (\S+) (\S+) (\[.*?\]) native model stop= (True|False)$',
        re.MULTILINE)
    for job, end, action_text, model_stop in pattern.findall(text):
        native_rows.append({'reference_job': job, 'end': end,
            'actions': ast.literal_eval(action_text), 'model_stop': model_stop == 'True'})
    assert len(native_rows) == 2, ('REFERENCE_862_NATIVE_JOB_COUNT', len(native_rows))
    native = dict(zip(('INTACT', 'REMOVED'), native_rows))
    return {'factorial_actions': actions, 'native': native,
        'diagnostic_results_are_not_native_reachability': True}


def native_regression863(env, native, reference862):
    reference860 = parse_reference860()
    regression = native_regression861(env, native, reference860)
    comparisons = {}
    for job in env['JOBS841'][:2]:
        jid = job['job']
        condition = job['intervention']
        assert condition in reference862['native'], ('REFERENCE_862_CONDITION_MISSING', condition)
        actual = {'end': env['REC841'][jid]['end'],
            'actions': [c['action'] for c in env['REC841'][jid]['cycles']],
            'model_stop': env['REC841'][jid]['model_stop']}
        expected_full = reference862['native'][condition]
        expected = {k: expected_full[k] for k in ('end', 'actions', 'model_stop')}
        assert actual == expected, ('NATIVE_862_REGRESSION', jid, actual, expected)
        comparisons[jid] = {'condition': condition, 'actual': actual,
            'reference862': expected_full, 'exact': True}
    regression['native_862_comparisons'] = comparisons
    regression['reference862_factorial_scope'] = 'DIAGNOSTIC_ONLY_NOT_USED_AS_NATIVE_EVIDENCE'
    short863('TABLE B REGRESSION job=BOTH cycle=ALL execution=ORIGINAL_NATIVE',
        json.dumps(regression, ensure_ascii=False))
    return regression


def state863(env, rows):
    if rows is None:
        return {'status': 'NOT_PRESENT_NATIVE_INITIAL_CYCLE_OR_NO_REVISION',
            'shape': None, 'dtype': None, 'device': None, 'norm': None,
            'mean': None, 'std': None, 'finite': None, 'sha256': None}
    return state_summary861(env, rows)


def comparison863(env, source, destination):
    if source is None or destination is None:
        return {'status': 'NOT_APPLICABLE_STATE_ABSENT', 'exact': None,
            'relative_l2': None, 'cosine': None}
    return paired_metrics859(env, source, destination)


def transfer863(env, source, destination, invocation, slot, path,
        source_stage, destination_stage, source_role, destination_role):
    torch = env['torch']
    source_state, destination_state = state863(env, source), state863(env, destination)
    difference = comparison863(env, source, destination)
    bf16 = continuity_for_slot859(env, invocation, slot)
    exact = source.shape == destination.shape and torch.equal(source, destination)
    assert exact, ('NATIVE_TRANSFER_SOURCE_MISMATCH', path, difference)
    assert bf16.get('status') == 'CHECKED' and bf16.get('exact_after_bf16'), (
        'NATIVE_TRANSFER_BF16_OR_POSITION_FAILURE', path, bf16)
    return {'path': path, 'execution': 'NATIVE_OBSERVATION_ONLY',
        'source_execution': 'ORIGINAL_NATIVE', 'source_stage': source_stage,
        'destination_stage': destination_stage, 'source_role': source_role,
        'destination_role': destination_role, 'source': source_state,
        'destination': destination_state, 'source_sha256': source_state['sha256'],
        'destination_sha256': destination_state['sha256'], 'exact': exact,
        'difference': difference, 'bf16': bf16, 'slot_ids': list(slot),
        'position_and_rope_path': 'Original invoke851/gen851/make_x851 path; no positional injection.'}


def check_output_h863(h, label):
    continuity = h['trace849']['continuity']
    assert continuity.get('exact_after_bf16'), (label + '_BF16_CONTINUITY_FAILED', continuity)
    assert h['rows'].dtype.is_floating_point and h['rows'].device.type == 'cpu'
    return continuity


def shared_native863(env, job, record):
    key = (job['qid'], job['intervention'], record['initial_mode'])
    assert key in env['SHARED851'] and key in env['COVERAGE_SHARED852'], (
        'NATIVE_SHARED_STATE_MISSING', key)
    shared = env['SHARED851'][key]
    coverage = env['COVERAGE_SHARED852'][key]
    assert shared['initial']['text'] == record['initial']['text']
    assert shared['evidence']['text'] == record['evidence_native']['text']
    return shared, coverage


def cartridge_detail863(env, world, card_id):
    roles = [role for role, cid in world['ids'].items() if cid == card_id]
    relations = relation_roles860(world)
    relation_rows = [{'role': role, 'from': relations[role][0], 'to': relations[role][1]}
        for role in roles if role in relations]
    text = env['cards829'][card_id]
    entry = env['entries'][card_id]
    return {'card_id': card_id, 'roles': roles, 'relations': relation_rows,
        'card_text_sha256': sha256_bytes863(text.encode('utf-8')),
        'cartridge_file_sha256': entry.get('sha256'),
        'sha256_source': 'Locked cards829 text and entries metadata; offline observation only.'}


def physical_seal863(env, memx):
    # Locked seal834 returns four (K_digest, V_digest) pairs, not one string.
    # Hash its canonical JSON losslessly for compact cross-stage equality audits.
    seal = env['seal834'](memx)
    assert isinstance(seal, (list, tuple)) and len(seal) == 4, (
        'PHYSICAL_MEMORY_SEAL_SCHEMA_MISMATCH', type(seal).__name__,
        None if not isinstance(seal, (list, tuple)) else len(seal))
    normalized = []
    for pair in seal:
        assert isinstance(pair, (list, tuple)) and len(pair) == 2, (
            'PHYSICAL_MEMORY_KV_PAIR_SCHEMA_MISMATCH', pair)
        assert all(isinstance(digest, str) and
            re.fullmatch(r'[0-9a-f]{64}', digest) for digest in pair), (
            'PHYSICAL_MEMORY_KV_DIGEST_INVALID', pair)
        normalized.append(list(pair))
    canonical = json.dumps(normalized, ensure_ascii='ascii', separators=(',', ':'))
    return sha256_bytes863(canonical.encode('ascii'))


def _score_margin_deltas863(before, after):
    return {name: after[name] - before[name] for name in sorted(before)}


def audit_job863(env, job, native):
    torch = env['torch']
    jid = job['job']
    record = env['REC841'][jid]
    world = env['worlds829'][env['QID841'].index(job['qid'])]
    shared, coverage = shared_native863(env, job, record)
    initial_cards = list(record['mounted_cards'])
    sufficient = evidence_sufficient862(env, job, initial_cards)
    card_details = [cartridge_detail863(env, world, cid) for cid in initial_cards]
    missing = []
    if not sufficient:
        missing.append({'role': 'second', 'card_id': world['ids']['second'],
            'from': world['middle'], 'to': world['end'],
            'reason': 'The expected two-hop path first+second is interrupted; second is not mounted.'})
    memory_cycles, candidate_cycles, joint_cycles, xray_cycles = [], [], [], []
    transition_rows = []
    RUNTIME863[jid] = {}
    base_memx = find_invocation859(jid, 'precontrol_0')['memx']
    arm_audit = job['intervention'] + '_STATE_AUDIT'
    for cycle in record['cycles']:
        index = int(cycle['cycle'])
        pre = find_invocation859(jid, 'precontrol_%d' % index)
        review = find_invocation859(jid, 'review_%d' % index)
        revision = find_invocation859(jid, 'revision_%d' % index) if cycle.get('revision') else None
        pm, dm = segment_map859(env, pre['segments']), segment_map859(env, review['segments'])
        assert all(name in pm for name in ('C', 'E', 'U', 'R'))
        assert all(name in dm for name in ('K0', 'J'))
        assert ('Kprev' in pm) == (index > 0)
        if index == 0:
            candidate_source = shared['initial']
            candidate_stage = 'initial'
        else:
            candidate_source = find_invocation859(jid, 'revision_%d' % (index - 1))['h']
            candidate_stage = 'revision_%d' % (index - 1)
        assert candidate_source['text'] == cycle['candidate']['text']
        C, E, U, R = (pm[name][1] for name in ('C', 'E', 'U', 'R'))
        Kprev = pm['Kprev'][1] if index > 0 else None
        K0, J, Review = pre['h']['rows'], dm['J'][1], review['h']['rows']
        previous_review = find_invocation859(jid, 'review_%d' % (index - 1))['h'] if index > 0 else None
        transfers = {
            'C': transfer863(env, candidate_source['rows'], C, pre, env['C_SLOT851'],
                candidate_stage + '.rows -> current851 -> cycle.C', candidate_stage,
                'precontrol_%d' % index, 'candidate_output', 'C'),
            'E': transfer863(env, shared['evidence']['rows'], E, pre, env['E_SLOT851'],
                'shared851.evidence.rows -> cycle.E', 'shared851.evidence',
                'precontrol_%d' % index, 'native_evidence', 'E'),
            'U': transfer863(env, coverage['rows'], U, pre, env['U_SLOT852'],
                'coverage_state852.rows -> cycle.U', 'coverage_state852',
                'precontrol_%d' % index, 'native_coverage', 'U'),
            'R': transfer863(env, env['relation852'](C, E), R, pre, env['R_SLOT852'],
                'relation852(C,E) -> cycle.R', 'relation852', 'precontrol_%d' % index,
                'relation_recompute_observation', 'R'),
            'K0': transfer863(env, K0, dm['K0'][1], review, env['K_SLOT854'],
                'precontrol.rows -> route854 -> review.K0', 'precontrol_%d' % index,
                'review_%d' % index, 'K0', 'K0'),
            'J': transfer863(env, env['interaction854'](C, E, K0), J, review,
                env['J_SLOT854'], 'interaction854(C,E,K0) -> route854 -> review.J',
                'interaction854', 'review_%d' % index, 'J_recompute_observation', 'J')}
        if index > 0:
            transfers['Kprev'] = transfer863(env, previous_review['rows'], Kprev, pre,
                env['K_SLOT851'], 'review_%d.rows -> previous_control851 -> cycle.Kprev' % (index - 1),
                'review_%d' % (index - 1), 'precontrol_%d' % index, 'Review', 'Kprev')
        else:
            transfers['Kprev'] = {'execution': 'NATIVE_OBSERVATION_ONLY',
                'status': 'NOT_PRESENT_IN_NATIVE_CYCLE0', 'exact': None,
                'relative_l2': None, 'cosine': None}
        check_output_h863(pre['h'], jid + '_K0_' + str(index))
        check_output_h863(review['h'], jid + '_REVIEW_' + str(index))
        revision_inputs, revision_quality = {}, None
        Revision = None
        if revision is not None:
            Revision = revision['h']['rows']
            check_output_h863(revision['h'], jid + '_REVISION_' + str(index))
            rm = segment_map859(env, revision['segments'])
            assert all(name in rm for name in ('C', 'E', 'Kprev', 'U', 'R'))
            revision_inputs = {
                'C': transfer863(env, C, rm['C'][1], revision, env['C_SLOT851'],
                    'cycle.C -> RECOMPUTE851.C', 'precontrol_%d' % index,
                    'revision_%d' % index, 'C', 'C'),
                'E': transfer863(env, E, rm['E'][1], revision, env['E_SLOT851'],
                    'cycle.E -> RECOMPUTE851.E', 'precontrol_%d' % index,
                    'revision_%d' % index, 'E', 'E'),
                'U': transfer863(env, U, rm['U'][1], revision, env['U_SLOT852'],
                    'cycle.U -> RECOMPUTE851.U', 'coverage_state852',
                    'revision_%d' % index, 'U', 'U'),
                'R': transfer863(env, R, rm['R'][1], revision, env['R_SLOT852'],
                    'cycle.R -> RECOMPUTE851.R', 'relation852',
                    'revision_%d' % index, 'R', 'R'),
                'Kprev': transfer863(env, Review, rm['Kprev'][1], revision, env['K_SLOT851'],
                    'current Review.rows -> RECOMPUTE851.K', 'review_%d' % index,
                    'revision_%d' % index, 'Review', 'revision_K')}
            revision_quality = offline_revision_quality861(env, job, revision['h']['text'],
                initial_cards, cycle['candidate']['text'])
        states = {name: state863(env, value) for name, value in (
            ('C', C), ('E', E), ('U', U), ('R', R), ('Kprev', Kprev),
            ('K0', K0), ('J', J), ('Review', Review), ('Revision', Revision))}
        assert all(x['finite'] for x in states.values() if x['finite'] is not None)
        RUNTIME863[jid][index] = {'C': C, 'E': E, 'U': U, 'R': R, 'Kprev': Kprev,
            'K0': K0, 'J': J, 'Review': Review, 'Revision': Revision,
            'pre': pre, 'review': review, 'revision': revision,
            'candidate_source': candidate_source}
        seals = {'precontrol': physical_seal863(env, pre['memx']),
            'review': physical_seal863(env, review['memx'])}
        if revision is not None:
            seals['revision'] = physical_seal863(env, revision['memx'])
        assert len(set(seals.values())) == 1, ('NATIVE_PHYSICAL_MEMORY_SEAL_CHANGED', jid, index, seals)
        stage_memories = [pre['memx'], review['memx']] + ([] if revision is None else [revision['memx']])
        same_memory_object = all(memx is base_memx for memx in stage_memories)
        assert same_memory_object, ('NATIVE_MEMORY_OBJECT_CHANGED', jid, index)
        current_cards = list(record['mounted_cards'])
        previous_cards = initial_cards if index == 0 else memory_cycles[index - 1]['accessible_cards']
        added = [cid for cid in current_cards if cid not in previous_cards]
        removed = [cid for cid in previous_cards if cid not in current_cards]
        memory_row = {'arm': arm_audit, 'job': jid, 'qid': job['qid'],
            'condition': job['intervention'], 'cycle': index,
            'execution': 'NATIVE_OBSERVATION_ONLY', 'source_execution': 'ORIGINAL_NATIVE',
            'initial_card_count': len(initial_cards), 'accessible_card_count': len(current_cards),
            'accessible_cards': current_cards, 'card_details': card_details,
            'physical_memory_sha256': seals['precontrol'], 'stage_physical_seals': seals,
            'physical_memory_seal_encoding': 'SHA256(canonical JSON of locked seal834 four K/V digest pairs)',
            'same_physical_memory_object_as_cycle0': same_memory_object,
            'memory_tokens': int(pre['memx'][0][0].shape[-2]),
            'added_cards': added, 'removed_cards': removed,
            'memory_set_changed': bool(added or removed),
            'new_evidence_discovered': bool(added),
            'model_selected_new_cartridge': None if added else False,
            'selection_path_observed': False,
            'mem851_lifetime': 'Created once from initial_cards before cycle0; same memx in all native stages.'}
        memory_cycles.append(memory_row)
        correct = env['node851'](cycle['candidate']['text'], world) == 'end'
        grounded = bool(env['supported851'](cycle['candidate']['text'], world, set(initial_cards)))
        previous_candidate = record['cycles'][index - 1]['candidate']['text'] if index > 0 else None
        previous_rows = RUNTIME863[jid][index - 1]['candidate_source']['rows'] if index > 0 else None
        candidate_row = {'arm': arm_audit, 'job': jid, 'cycle': index,
            'condition': job['intervention'], 'execution': 'NATIVE_OBSERVATION_ONLY',
            'source_execution': 'ORIGINAL_NATIVE', 'candidate_stage': candidate_stage,
            'candidate_text_offline_only': cycle['candidate']['text'],
            'candidate_state': states['C'], 'candidate_correct_offline': correct,
            'candidate_grounded_offline': grounded,
            'previous_candidate_text_offline_only': previous_candidate,
            'candidate_text_changed_from_previous': (None if index == 0 else
                previous_candidate != cycle['candidate']['text']),
            'candidate_state_difference_from_previous': comparison863(env, previous_rows, C),
            'revision_text_offline_only': None if revision is None else revision['h']['text'],
            'revision_state': states['Revision'], 'revision_quality_offline_only': revision_quality,
            'labels_entered_native_inputs': False}
        candidate_cycles.append(candidate_row)
        native_cycle = native[jid]['cycles'][index]
        action = cycle['action']
        assert action == native_cycle['action'] == env['parse849'](review['h']['text'])
        joint = 'C%dE%d' % (int(correct), int(sufficient))
        decision_quality = decision_quality860(env, job, action, cycle['candidate']['text'],
            None if revision is None else revision['h']['text'], initial_cards)
        joint_row = {'arm': arm_audit, 'job': jid, 'cycle': index,
            'condition': job['intervention'], 'execution': 'NATIVE_OBSERVATION_ONLY',
            'source_execution': 'ORIGINAL_NATIVE', 'joint_state_offline_only': joint,
            'C1_correct_candidate': correct, 'E1_sufficient_evidence': sufficient,
            'candidate_grounded': grounded, 'native_greedy_action': action,
            'native_action_is_greedy_review': True, 'native_end_after_cycle': record['end'] if (
                index == len(record['cycles']) - 1) else 'CONTINUES_TO_NEXT_NATIVE_CYCLE',
            'decision_quality_offline_only': decision_quality,
            'native_model_accept': bool(index == len(record['cycles']) - 1 and record['end'] == 'MODEL_ACCEPT'),
            'native_model_stop': bool(index == len(record['cycles']) - 1 and record['end'] == 'MODEL_STOP'),
            'mechanical_limit_is_model_stop': False, 'labels_entered_native_inputs': False}
        joint_cycles.append(joint_row)
        xray_row = {'arm': arm_audit, 'job': jid, 'cycle': index,
            'condition': job['intervention'], 'execution': 'NATIVE_OBSERVATION_ONLY',
            'source_execution': 'ORIGINAL_NATIVE', 'states': states,
            'source_destination_transfers': transfers, 'revision_inputs': revision_inputs,
            'precontrol_output': h_summary859(env, pre['h']),
            'review_output': h_summary859(env, review['h']),
            'revision_output': None if revision is None else h_summary859(env, revision['h']),
            'scores': native_cycle['scores'], 'margins': native_cycle['margins'],
            'score_provenance': native[jid]['score_provenance']}
        xray_cycles.append(xray_row)
        short863('TABLE C MEMORY ACCESS', jid, 'cycle=%d' % index,
            'execution=NATIVE_OBSERVATION_ONLY', 'cards=' + json.dumps(current_cards),
            'physical_sha256=' + seals['precontrol'],
            'added=' + str(len(added)), 'removed=' + str(len(removed)))
        short863('TABLE D EVIDENCE REACHABILITY', jid, 'cycle=%d' % index,
            'execution=NATIVE_OBSERVATION_ONLY', 'sufficient=' + str(sufficient),
            'missing=' + json.dumps(missing, ensure_ascii=False))
        short863('TABLE E CANDIDATE REACHABILITY', jid, 'cycle=%d' % index,
            'execution=NATIVE_OBSERVATION_ONLY', 'stage=' + candidate_stage,
            'correct=' + str(correct), 'grounded=' + str(grounded),
            'revision=' + repr(candidate_row['revision_text_offline_only']))
        short863('TABLE F NATIVE JOINT STATE', jid, 'cycle=%d' % index,
            'execution=NATIVE_OBSERVATION_ONLY', joint, 'native_action=' + action)
        short863('TABLE H STATE XRAY', jid, 'cycle=%d' % index,
            'execution=NATIVE_OBSERVATION_ONLY', json.dumps(states))
        short863('TABLE I NATIVE ACTION SCORES', jid, 'cycle=%d' % index,
            'execution=NATIVE_OBSERVATION_ONLY', 'native_greedy=' + action,
            json.dumps(native_cycle['scores']), 'margins=' + json.dumps(native_cycle['margins']))
        if revision is not None:
            has_next = index + 1 < len(record['cycles'])
            carried = None
            if has_next:
                next_pre = find_invocation859(jid, 'precontrol_%d' % (index + 1))
                next_C = segment_map859(env, next_pre['segments'])['C'][1]
                carried = torch.equal(Revision, next_C)
            review_delta = comparison863(env,
                None if previous_review is None else previous_review['rows'], Review)
            score_delta = None if index == 0 else score_deltas860(
                native[jid]['cycles'][index - 1]['scores'], native_cycle['scores'])
            margin_delta = None if index == 0 else _score_margin_deltas863(
                native[jid]['cycles'][index - 1]['margins'], native_cycle['margins'])
            transition = {'arm': arm_audit, 'job': jid, 'cycle': index,
                'condition': job['intervention'], 'execution': 'NATIVE_OBSERVATION_ONLY',
                'source_execution': 'ORIGINAL_NATIVE', 'native_action': 'REVISE',
                'new_evidence': memory_row['new_evidence_discovered'],
                'new_card_ids': list(added),
                'new_candidate_generated': True,
                'candidate_text_changed': cycle['candidate']['text'] != revision['h']['text'],
                'candidate_state_change': comparison863(env, C, Revision),
                'candidate_correct_before': correct,
                'candidate_correct_after': revision_quality['candidate_correct_for_task'],
                'candidate_correctness_changed': correct != revision_quality['candidate_correct_for_task'],
                'revision_grounded': revision_quality['revision_grounded_by_mounted_evidence'],
                'Kprev_for_revision_is_current_review_exact': revision_inputs['Kprev']['exact'],
                'Kprev_change_from_previous_review': review_delta,
                'review_state_change_from_previous': review_delta,
                'action_score_change_from_previous': score_delta,
                'action_margin_change_from_previous': margin_delta,
                'revision_uses_only_existing_E_U': bool(
                    revision_inputs['E']['exact'] and revision_inputs['U']['exact']),
                'revision_carried_to_next_C': carried,
                'carry_status': ('EXACT_NEXT_NATIVE_C' if carried else
                    'NEXT_NATIVE_C_MISMATCH' if carried is False else
                    'NOT_OBSERVED_NO_NEXT_NATIVE_EVALUATION'),
                'new_task_endpoint_reached_offline': bool(
                    not correct and revision_quality['candidate_correct_for_task']),
                'semantic_new_information_claimed': False}
            transition_rows.append(transition)
            short863('TABLE G REVISE TRANSITION', jid, 'cycle=%d' % index,
                'execution=NATIVE_OBSERVATION_ONLY', json.dumps(transition, ensure_ascii=False))
    memory_summary = {'arm': arm_audit, 'job': jid, 'qid': job['qid'],
        'condition': job['intervention'], 'execution': 'NATIVE_OBSERVATION_ONLY',
        'source_execution': 'ORIGINAL_NATIVE', 'initial_card_count': len(initial_cards),
        'initial_cards': initial_cards, 'card_details': card_details,
        'initial_physical_memory_sha256': memory_cycles[0]['physical_memory_sha256'],
        'initial_evidence_sufficient_offline': sufficient,
        'missing_relations_offline_only': missing, 'cycles': memory_cycles,
        'memory_set_changed_any_cycle': any(x['memory_set_changed'] for x in memory_cycles),
        'new_card_added_any_cycle': any(bool(x['added_cards']) for x in memory_cycles),
        'card_removed_any_cycle': any(bool(x['removed_cards']) for x in memory_cycles),
        'new_evidence_discovered_any_cycle': any(x['new_evidence_discovered'] for x in memory_cycles),
        'model_new_cartridge_selection_observed': False,
        'native_evidence_acquisition_status': 'NATIVE_EVIDENCE_ACQUISITION_NOT_IMPLEMENTED',
        'labels_entered_native_inputs': False}
    correct_stages = []
    for row in candidate_cycles:
        if row['candidate_correct_offline']:
            correct_stages.append(row['candidate_stage'])
        if row['revision_quality_offline_only'] and row['revision_quality_offline_only']['candidate_correct_for_task']:
            correct_stages.append('revision_%d' % row['cycle'])
    correct_stages = list(dict.fromkeys(correct_stages))
    candidate_summary = {'arm': arm_audit, 'job': jid, 'condition': job['intervention'],
        'execution': 'NATIVE_OBSERVATION_ONLY', 'source_execution': 'ORIGINAL_NATIVE',
        'cycles': candidate_cycles, 'correct_candidate_stages': correct_stages,
        'first_correct_candidate_stage': correct_stages[0] if correct_stages else None,
        'native_correct_candidate_reached': bool(correct_stages),
        'status': ('NATIVE_CORRECT_CANDIDATE_REACHED' if correct_stages else
            'NATIVE_CORRECT_CANDIDATE_NOT_REACHED'),
        'candidate_truth_and_grounding_are_offline_only': True}
    joint_summary = {'arm': arm_audit, 'job': jid, 'condition': job['intervention'],
        'execution': 'NATIVE_OBSERVATION_ONLY', 'source_execution': 'ORIGINAL_NATIVE',
        'cycles': joint_cycles,
        'native_C1E1_cycles': [x['cycle'] for x in joint_cycles if x['joint_state_offline_only'] == 'C1E1'],
        'native_C1E1_reached': any(x['joint_state_offline_only'] == 'C1E1' for x in joint_cycles),
        'status': ('NATIVE_C1E1_REACHED' if any(x['joint_state_offline_only'] == 'C1E1' for x in joint_cycles)
            else 'NATIVE_C1E1_NOT_REACHED'),
        'native_C1E1_actions': [{'cycle': x['cycle'], 'action': x['native_greedy_action'],
            'end': x['native_end_after_cycle']} for x in joint_cycles
            if x['joint_state_offline_only'] == 'C1E1']}
    STATE863['memory'][jid] = memory_summary
    STATE863['candidates'][jid] = candidate_summary
    STATE863['joint'][jid] = joint_summary
    STATE863['transitions'][jid] = transition_rows
    STATE863['xray'][jid] = xray_cycles
    return {'memory': memory_summary, 'candidates': candidate_summary,
        'joint': joint_summary, 'transitions': transition_rows, 'xray': xray_cycles}


def exact_restore863(env, native):
    torch = env['torch']
    restores = []
    with torch.no_grad():
        for job in env['JOBS841'][:2]:
            jid = job['job']
            for cycle in env['REC841'][jid]['cycles']:
                index = int(cycle['cycle'])
                runtime = RUNTIME863[jid][index]
                pre, review = runtime['pre'], runtime['review']
                K0 = env['gen851'](pre['memx'], list(pre['pre']),
                    clone_segments859(pre['segments']), list(pre['post']))
                J = env['interaction854'](runtime['C'], runtime['E'], K0['rows'])
                review_replay = env['gen851'](review['memx'], list(review['pre']),
                    clone_segments859(review['segments']), list(review['post']))
                scores = score_actions859(env, review['memx'], list(review['pre']),
                    clone_segments859(review['segments']), list(review['post']))
                check_output_h863(K0, 'RESTORE_K0')
                check_output_h863(review_replay, 'RESTORE_REVIEW')
                K0_exact = native_h_equal859(torch, pre['h'], K0)
                J_exact = torch.equal(runtime['J'], J)
                review_exact = native_h_equal859(torch, review['h'], review_replay)
                scores_exact = scores == native[jid]['cycles'][index]['scores']
                action_exact = env['parse849'](review_replay['text']) == cycle['action']
                R_exact = torch.equal(runtime['R'], env['relation852'](runtime['C'], runtime['E']))
                revision_exact, revision_summary = None, None
                if runtime['revision'] is not None:
                    original_revision = runtime['revision']
                    revision_replay = env['gen851'](original_revision['memx'],
                        list(original_revision['pre']), clone_segments859(original_revision['segments']),
                        list(original_revision['post']))
                    check_output_h863(revision_replay, 'RESTORE_REVISION')
                    revision_exact = native_h_equal859(torch, original_revision['h'], revision_replay)
                    revision_summary = h_summary859(env, revision_replay)
                exact = all(x for x in (K0_exact, J_exact, review_exact, scores_exact,
                    action_exact, R_exact) if x is not None) and revision_exact is not False
                row = {'arm': 'EXACT_RESTORE', 'job': jid, 'cycle': index,
                    'condition': job['intervention'], 'execution': 'DIAGNOSTIC_REPLAY',
                    'source_execution': 'ORIGINAL_NATIVE', 'exact': exact,
                    'K0_exact': K0_exact, 'J_exact': J_exact, 'R_exact': R_exact,
                    'Review_exact': review_exact, 'Revision_exact': revision_exact,
                    'scores_exact': scores_exact, 'native_action_reproduced': action_exact,
                    'K0': h_summary859(env, K0), 'Review': h_summary859(env, review_replay),
                    'Revision': revision_summary, 'scores': scores,
                    'native_reachability_credit': False,
                    'not_a_native_third_cycle': True,
                    'teacher_forced_scores_are_not_calibrated_probabilities': True}
                restores.append(row)
                short863('TABLE K EXACT_RESTORE', jid, 'cycle=%d' % index,
                    'execution=DIAGNOSTIC_REPLAY', 'EXACT' if exact else 'FAILED',
                    json.dumps({k: row[k] for k in ('K0_exact', 'J_exact', 'R_exact',
                        'Review_exact', 'Revision_exact', 'scores_exact', 'native_action_reproduced')}))
    STATE863['restores'] = restores
    return restores


def _first_missing863(memory, candidates, joint):
    if joint['native_C1E1_reached']:
        return 'NOT_APPLICABLE_NATIVE_C1E1_REACHED'
    if not memory['initial_evidence_sufficient_offline'] and not memory['new_evidence_discovered_any_cycle']:
        return 'EVIDENCE_ACCESS_BEFORE_CANDIDATE_FORMATION'
    if not candidates['native_correct_candidate_reached']:
        return 'CANDIDATE_FORMATION_WITH_ACCESSIBLE_EVIDENCE'
    return 'JOINT_STATE_TRANSITION_OR_CARRY'


def final_reachability863(env, motor_map):
    jobs = env['JOBS841'][:2]
    intact, removed = jobs[0]['job'], jobs[1]['job']
    memory, candidates, joint = STATE863['memory'], STATE863['candidates'], STATE863['joint']
    closures = native_closure862(env)
    correct_scopes = {jid: candidates[jid]['correct_candidate_stages'] for jid in candidates}
    c1e1_scopes = {jid: joint[jid]['native_C1E1_cycles'] for jid in joint}
    aligned = []
    for jid, summary in joint.items():
        for row in summary['cycles']:
            if (row['joint_state_offline_only'] == 'C1E1' and
                    row['native_greedy_action'] == 'CONTINUE' and row['candidate_grounded'] and
                    not row['decision_quality_offline_only']['unsupported_completion']):
                aligned.append({'job': jid, 'cycle': row['cycle'],
                    'action': row['native_greedy_action'], 'end': row['native_end_after_cycle']})
    acquisition_absent = all(not memory[job['job']]['new_card_added_any_cycle'] and
        not memory[job['job']]['model_new_cartridge_selection_observed'] for job in jobs)
    acquisition_absent = acquisition_absent and 'no mid-loop native evidence remount' in motor_map['memory_lifetime']
    dimensions = {
        'A_NATIVE_EVIDENCE_REACHABLE': any(memory[job['job']]['initial_evidence_sufficient_offline'] for job in jobs),
        'B_NATIVE_CORRECT_CANDIDATE_REACHABLE': any(candidates[job['job']]['native_correct_candidate_reached'] for job in jobs),
        'C_NATIVE_C1E1_REACHABLE': any(joint[job['job']]['native_C1E1_reached'] for job in jobs),
        'D_NATIVE_EVIDENCE_ACQUISITION_NOT_IMPLEMENTED': acquisition_absent,
        'E_NATIVE_CORRECT_CANDIDATE_NOT_REACHED': not candidates[removed]['native_correct_candidate_reached'],
        'F_NATIVE_C1E1_NOT_REACHED': not joint[removed]['native_C1E1_reached'],
        'G_NATIVE_EVIDENCE_ALIGNED_ACTION_OBSERVED': bool(aligned),
        'H_NATIVE_AUTONOMOUS_CORRECTION_AND_CLOSURE_OBSERVED': any(
            x['native_autonomous_correction_closure'] for x in closures)}
    scopes = {
        'A': [job['job'] for job in jobs if memory[job['job']]['initial_evidence_sufficient_offline']],
        'B': correct_scopes, 'C': c1e1_scopes,
        'D': [job['job'] for job in jobs] if acquisition_absent else [],
        'E': [removed] if dimensions['E_NATIVE_CORRECT_CANDIDATE_NOT_REACHED'] else [],
        'F': [removed] if dimensions['F_NATIVE_C1E1_NOT_REACHED'] else [],
        'G': aligned,
        'H': [x['job'] for x in closures if x['native_autonomous_correction_closure']]}
    classes = [name for name, value in dimensions.items() if value]
    if not classes:
        classes = ['UNRESOLVED']
    first_missing = {job['job']: _first_missing863(memory[job['job']],
        candidates[job['job']], joint[job['job']]) for job in jobs}
    removed_transitions = STATE863['transitions'][removed]
    sufficient_carry = []
    for job in jobs:
        jid = job['job']
        for index in range(len(joint[jid]['cycles']) - 1):
            current, nxt = joint[jid]['cycles'][index], joint[jid]['cycles'][index + 1]
            if current['E1_sufficient_evidence']:
                sufficient_carry.append({'job': jid, 'from_cycle': index, 'to_cycle': index + 1,
                    'E_exact': STATE863['xray'][jid][index + 1]['source_destination_transfers']['E']['exact'],
                    'sufficient_at_next': nxt['E1_sufficient_evidence']})
    possibility_a = bool(not memory[removed]['initial_evidence_sufficient_offline'] and
        not memory[removed]['new_evidence_discovered_any_cycle'])
    possibility_b_by_job = {}
    possibility_c_by_job = {}
    for job in jobs:
        jid = job['job']
        sufficient_wrong = [x['cycle'] for x in joint[jid]['cycles']
            if x['E1_sufficient_evidence'] and not x['C1_correct_candidate']]
        if sufficient_wrong:
            b_status = 'SUPPORTED_FOR_OBSERVED_CYCLES'
        elif not memory[jid]['initial_evidence_sufficient_offline']:
            b_status = 'UNRESOLVED_NO_NATIVE_SUFFICIENT_EVIDENCE_STATE'
        else:
            b_status = 'NOT_OBSERVED'
        produced_correct = candidates[jid]['native_correct_candidate_reached']
        had_sufficient = memory[jid]['initial_evidence_sufficient_offline']
        if produced_correct and had_sufficient and not joint[jid]['native_C1E1_reached']:
            c_status = 'SUPPORTED_FOR_THIS_JOB'
        elif not produced_correct or not had_sufficient:
            c_status = 'NOT_ISOLATED_UPSTREAM_PREREQUISITE_MISSING'
        else:
            c_status = 'NOT_OBSERVED'
        possibility_b_by_job[jid] = {'status': b_status, 'sufficient_but_wrong_cycles': sufficient_wrong}
        possibility_c_by_job[jid] = {'status': c_status}
    possibilities = {
        'A_EVIDENCE_ACCESS_LIMIT': {'status': 'SUPPORTED_FOR_REMOVED' if possibility_a else 'NOT_DEMONSTRATED',
            'scope': removed, 'first_missing_transition': first_missing[removed]},
        'B_CANDIDATE_FORMATION_LIMIT': {'by_job': possibility_b_by_job,
            'status': 'UNRESOLVED_FOR_REMOVED' if possibility_b_by_job[removed]['status'].startswith('UNRESOLVED')
                else possibility_b_by_job[removed]['status']},
        'C_STATE_TRANSITION_LIMIT': {'by_job': possibility_c_by_job,
            'status': possibility_c_by_job[removed]['status']}}
    answers = {
        '1_INTACT_native_C1E1': {'reached': joint[intact]['native_C1E1_reached'],
            'cycles': joint[intact]['native_C1E1_cycles']},
        '2_REMOVED_native_C1E1': {'reached': joint[removed]['native_C1E1_reached'],
            'cycles': joint[removed]['native_C1E1_cycles']},
        '3_REMOVED_missing_relation': memory[removed]['missing_relations_offline_only'],
        '4_REVISE_creates_new_evidence': any(x['new_evidence'] for rows in STATE863['transitions'].values() for x in rows),
        '5_REVISE_reprocesses_existing_evidence': {'by_job': {jid: [
            {'cycle': x['cycle'], 'existing_E_U_exact': x['revision_uses_only_existing_E_U'],
             'candidate_state_changed': not x['candidate_state_change']['exact']}
            for x in rows] for jid, rows in STATE863['transitions'].items()},
            'scope': 'Evidence-only yes where exact; candidate and Kprev may also change.'},
        '6_native_memory_set_changes': {jid: memory[jid]['memory_set_changed_any_cycle'] for jid in memory},
        '7_model_selects_new_cartridge': {jid: memory[jid]['model_new_cartridge_selection_observed'] for jid in memory},
        '8_correct_candidate_native_stage': {jid: candidates[jid]['first_correct_candidate_stage'] for jid in candidates},
        '9_correct_candidate_carried_to_next_cycle': {jid: [
            {'cycle': x['cycle'], 'correct_after': x['candidate_correct_after'],
             'carried': x['revision_carried_to_next_C'], 'status': x['carry_status']}
            for x in STATE863['transitions'][jid] if x['candidate_correct_after']] for jid in candidates},
        '10_sufficient_evidence_preserved_into_next_native_evaluation': (
            sufficient_carry if sufficient_carry else 'NOT_APPLICABLE_NO_NATIVE_SUFFICIENT_TO_NEXT_EVALUATION'),
        '11_native_C1E1_actions': {jid: joint[jid]['native_C1E1_actions'] for jid in joint},
        '12_first_missing_transition_when_no_C1E1': first_missing,
        '13_missing_stage_classification': first_missing,
        '14_natural_reachability_limit': {
            'memory': motor_map['memory_lifetime'], 'MAX_REVIEWS851': motor_map['MAX_REVIEWS851'],
            'removed_limit': first_missing[removed],
            'mechanical_limit_is_MODEL_STOP': False},
        '15_TEST862_diagnostic_transfer_to_native': {
            'native_positive_control': aligned,
            'condition': 'Only an actually occurring native C1E1 evaluation can support native action transfer.',
            'INTACT_initial_Kprev': 'ABSENT_NATIVE_CYCLE0',
            'REMOVED_post_revision_Kprev': 'PRESENT_FROM_PREVIOUS_REVIEW',
            'conditions_are_not_fully_equivalent': True,
            'removed_post_revision_transfer_observed': False,
            'diagnostic_C1E1_is_native_C1E1': False}}
    result = {'execution': 'NATIVE_OBSERVATION_ONLY', 'dimensions': dimensions,
        'dimension_scopes': scopes, 'reported_classes': classes,
        'possibilities': possibilities, 'required_answers': answers,
        'first_missing_transition': first_missing,
        'native_evidence_aligned_actions': aligned,
        'native_closure_evidence': closures,
        'intact_success_is_removed_correction_success': False,
        'diagnostic_continue_is_MODEL_ACCEPT': False,
        'diagnostic_stop_is_MODEL_STOP': False,
        'mechanical_limit_EOS_UNKNOWN_are_MODEL_STOP': False,
        'single_world_no_population_generalization': True}
    short863('TABLE J INTACT VS REMOVED', 'job=%s|%s' % (intact, removed),
        'cycle=ALL execution=NATIVE_OBSERVATION_ONLY',
        json.dumps({'INTACT': {'candidate': candidates[intact]['status'], 'joint': joint[intact]['status']},
            'REMOVED': {'candidate': candidates[removed]['status'], 'joint': joint[removed]['status']},
            'first_missing': first_missing}, ensure_ascii=False))
    short863('TABLE L FINAL REACHABILITY', 'job=BOTH cycle=ALL execution=NATIVE_OBSERVATION_ONLY',
        json.dumps(result, ensure_ascii=False))
    return result


def run_analysis863(env, native):
    digest = records_digest861(env)
    STATE863['original_record_sha256'] = digest
    motor_map = motor_map861()
    for job in env['JOBS841'][:2]:
        record = env['REC841'][job['job']]
        short863('TABLE B ORIGINAL NATIVE', job['job'], 'cycle=ALL execution=ORIGINAL_NATIVE',
            job['intervention'], record['end'], [c['action'] for c in record['cycles']],
            'model_stop=' + str(record['model_stop']))
    short863('TABLE A GPU ENVIRONMENT job=GLOBAL cycle=NA execution=NATIVE_OBSERVATION_ONLY',
        json.dumps(STATE859['environment']))
    audits = {job['job']: audit_job863(env, job, native) for job in env['JOBS841'][:2]}
    restores = exact_restore863(env, native)
    conclusion = final_reachability863(env, motor_map)
    assert records_digest861(env) == digest, 'OBSERVATION_CHANGED_ORIGINAL_NATIVE_RECORDS'
    assert_hook_free859(env, 'post_TEST863_native_reachability_audit')
    assert not any(p.requires_grad for p in env['model'].parameters())
    assert env['MAX_REVIEWS851'] == 2
    memory_artifact = {'jobs': STATE863['memory'], 'motor_map': motor_map,
        'execution': 'NATIVE_OBSERVATION_ONLY'}
    candidate_artifact = {'jobs': STATE863['candidates'], 'execution': 'NATIVE_OBSERVATION_ONLY'}
    joint_artifact = {'jobs': STATE863['joint'], 'conclusion': conclusion,
        'execution': 'NATIVE_OBSERVATION_ONLY'}
    transition_artifact = {'jobs': STATE863['transitions'], 'restores': restores,
        'execution': 'NATIVE_OBSERVATION_ONLY_AND_DIAGNOSTIC_REPLAY_SEPARATED'}
    xray_artifact = {'jobs': STATE863['xray'], 'restores': restores,
        'state_order': STATE_ORDER863,
        'teacher_forced_scores_are_not_calibrated_probabilities': True}
    json_write863('863_native_memory_access.json', memory_artifact)
    json_write863('863_candidate_reachability.json', candidate_artifact)
    json_write863('863_joint_state_reachability.json', joint_artifact)
    json_write863('863_transition_audit.json', transition_artifact)
    json_write863('863_state_xray.json', xray_artifact)
    analysis = {'status': 'NATIVE_REACHABILITY_AUDIT_COMPLETE',
        'native_jobs': 2, 'native_evaluations': sum(len(x['cycles']) for x in STATE863['joint'].values()),
        'diagnostic_restores': len(restores), 'new_native_jobs_created': 0,
        'new_native_cycles_created': 0, 'controls_exact': all(x['exact'] for x in restores),
        'original_records_unchanged': True, 'conclusion': conclusion,
        'motor_map': motor_map, 'native_sequences': native}
    STATE863['analysis'] = analysis
    return analysis


def write_partial863():
    artifacts = {
        '863_native_memory_access.json': {'status': 'PARTIAL_OR_NOT_STARTED', 'jobs': STATE863['memory']},
        '863_candidate_reachability.json': {'status': 'PARTIAL_OR_NOT_STARTED', 'jobs': STATE863['candidates']},
        '863_joint_state_reachability.json': {'status': 'PARTIAL_OR_NOT_STARTED', 'jobs': STATE863['joint']},
        '863_transition_audit.json': {'status': 'PARTIAL_OR_NOT_STARTED',
            'jobs': STATE863['transitions'], 'restores': STATE863['restores']},
        '863_state_xray.json': {'status': 'PARTIAL_OR_NOT_STARTED',
            'jobs': STATE863['xray'], 'restores': STATE863['restores']}}
    for name, value in artifacts.items():
        if not (ROOT863 / name).exists():
            json_write863(name, value)


def finalize863(gates, execution):
    write_partial863()
    capture_cell_source863()
    source_path = ROOT863 / '863.py'
    source_present = source_path.is_file() and source_path.stat().st_size > 0
    source_sha = sha256_bytes863(source_path.read_bytes()) if source_present else None
    gates['GATE7_ARTIFACT_INTEGRITY'] = 'PASS' if source_present else 'FAIL'
    required = ('GATE0_SOURCE_INTEGRITY', 'GATE1_GPU_PREFLIGHT_NATIVE_TWO_JOBS',
        'GATE2_HOOKFREE_OBSERVER_EQUIVALENCE', 'GATE3_862_NATIVE_REGRESSION',
        'GATE4_NATIVE_STATE_AND_REACHABILITY_AUDIT', 'GATE5_EXACT_RESTORE',
        'GATE6_REQUIRED_ARTIFACT_CONTENT', 'GATE7_ARTIFACT_INTEGRITY')
    technical = all(gates.get(k) == 'PASS' for k in required)
    conclusion = ANALYSIS863.get('conclusion', {})
    dimensions = conclusion.get('dimensions', {})
    classes = conclusion.get('reported_classes', ['UNRESOLVED'])
    report = {'test': TEST863_KIND, 'execution': execution, 'gates': gates,
        'technical_result': 'TECHNICAL_NATIVE_REACHABILITY_PASS' if technical else
            'TECHNICAL_NATIVE_REACHABILITY_NOT_PASSED',
        'scientific_result': classes if dimensions else 'UNRESOLVED',
        'native_autonomous_correction_and_closure': (
            'OBSERVED' if dimensions.get('H_NATIVE_AUTONOMOUS_CORRECTION_AND_CLOSURE_OBSERVED')
            else 'NOT_OBSERVED'),
        'native_evidence_aligned_action': 'OBSERVED' if dimensions.get(
            'G_NATIVE_EVIDENCE_ALIGNED_ACTION_OBSERVED') else 'NOT_OBSERVED',
        'original_error': EXECUTION_ERROR863, 'analysis_error': ANALYSIS_ERROR863,
        'diagnostic_control_stop': DIAGNOSTIC_CONTROL_STOP863,
        'diagnostic_control_stop_is_model_stop': False,
        'technical_verification': TWO_JOB_VERIFICATION863,
        'analysis': ANALYSIS863, 'source_lock_count': len(RAW_SOURCES863),
        'dependency_audit': STATE863['dependency_audit'],
        'environment': STATE859['environment'], 'observer_equalities': STATE859['equalities'],
        'coverage_observer_equalities': [c['observer_equality'] for c in STATE859['coverage']],
        'source_capture': {'file': '863.py', 'present': source_present, 'sha256': source_sha},
        'seconds': time.perf_counter() - START863,
        'limitations': [
            'One task world and the original two jobs; no population generalization.',
            'INTACT native C1E1 is an initial-state positive control, not REMOVED autonomous correction.',
            'Native cycle0 has no Kprev; INTACT and REMOVED post-revision states are not fully equivalent.',
            'Exact restore is diagnostic replay and earns no native reachability credit.',
            'Teacher-forced scores are not calibrated action probabilities.',
            'Mechanical review limit, EOS and UNKNOWN are not MODEL_STOP.',
            'No evidence acquisition, motor revision, new decision rule or extra native cycle is introduced.'],
        'TEST863_NEW_ENGINE': False, 'TEST863_MOTOR_REVISION': False,
        'TEST863_ANSWER_FIXED_BY_PYTHON': False, 'TEST863_MAX_REVIEWS_CHANGED': False,
        'TEST863_ORACLE_LABELS_ENTERED_NATIVE_INPUTS': False}
    json_write863('863_report.json', report)
    if TRACEBACK863:
        (ROOT863 / '863_traceback.txt').write_text(TRACEBACK863, encoding='utf-8')
    short863('TEST863 TECHNICAL', report['technical_result'])
    short863('TEST863 SCIENTIFIC', json.dumps(report['scientific_result'], ensure_ascii=False))
    short863('TEST863 NATIVE ALIGNED ACTION', report['native_evidence_aligned_action'])
    short863('TEST863 AUTONOMOUS CORRECTION CLOSURE', report['native_autonomous_correction_and_closure'])
    for name, status in gates.items():
        short863(name, status)
    short863('ARTIFACTS', ROOT863)
    LOG_FILE863.flush()
    manifest = {}
    for path in sorted(ROOT863.rglob('*')):
        if path.is_file() and path.name != '863_sha256_manifest.json':
            manifest[str(path.relative_to(ROOT863))] = {'bytes': path.stat().st_size,
                'sha256': sha256_bytes863(path.read_bytes())}
    json_write863('863_sha256_manifest.json', manifest)


try:
    short863('TEST863: native evidence, candidate and joint-state reachability audit.')
    short863('GPU EXECUTION: NOT VERIFIED BY AUTHOR; restart Colab before this cell.')
    load_sources863()
    load_spine863()
    reference862 = parse_reference862()
    gate0 = 'PASS'
    env863, error863, trace863, evidence863 = reproduce_pre859859()
    EXECUTION_ERROR863, TRACEBACK863, ERROR_EVIDENCE863 = error863, trace863, evidence863
    if trace863:
        short863(trace863[-12000:])
    if 'GATE1_TWO_JOB_OBSERVATION_COMPLETE' in trace863:
        DIAGNOSTIC_CONTROL_STOP863 = 'GATE1_TWO_JOB_OBSERVATION_COMPLETE'
    try:
        TWO_JOB_VERIFICATION863 = verify_two_job859(env863, trace863)
        EXECUTION_ERROR863 = None
        gate1 = gate2 = 'PASS'
    except Exception as exc:
        EXECUTION_ERROR863 = type(exc).__name__ + ': ' + str(exc)
        gate1 = gate2 = 'BLOCKED'
        short863(traceback.format_exc())
    if gate1 == 'PASS':
        try:
            install_offline_evaluator859(env863)
            native863 = native_sequences860(env863)
            regression863 = native_regression863(env863, native863, reference862)
            gate3 = 'PASS'
        except BaseException as exc:
            ANALYSIS_ERROR863 = type(exc).__name__ + ': ' + str(exc)
            TRACEBACK863 += '\n===== TEST863 NATIVE REGRESSION FAILURE =====\n' + traceback.format_exc()
            short863(traceback.format_exc())
            gate3 = 'BLOCKED'
            native863 = None
        if gate3 == 'PASS':
            try:
                ANALYSIS863 = run_analysis863(env863, native863)
                gate4 = 'PASS'
                gate5 = 'PASS' if ANALYSIS863['controls_exact'] else 'FAIL'
                gate6 = 'PASS'
                execution = 'NATIVE_REACHABILITY_AUDIT_COMPLETE'
            except BaseException as exc:
                ANALYSIS_ERROR863 = type(exc).__name__ + ': ' + str(exc)
                TRACEBACK863 += '\n===== TEST863 ANALYSIS FAILURE =====\n' + traceback.format_exc()
                short863(traceback.format_exc())
                gate4 = gate5 = gate6 = 'BLOCKED'
                execution = 'ANALYSIS_INCOMPLETE_FULL_TRACEBACK_IN_LOG'
        else:
            gate4 = gate5 = gate6 = 'BLOCKED'
            execution = 'NATIVE_REGRESSION_FAILED_REACHABILITY_NOT_RUN'
    else:
        gate3 = gate4 = gate5 = gate6 = 'BLOCKED'
        execution = 'TWO_JOB_TECHNICAL_VERIFICATION_FAILED'
    gates = {'GATE0_SOURCE_INTEGRITY': gate0,
        'GATE1_GPU_PREFLIGHT_NATIVE_TWO_JOBS': gate1,
        'GATE2_HOOKFREE_OBSERVER_EQUIVALENCE': gate2,
        'GATE3_862_NATIVE_REGRESSION': gate3,
        'GATE4_NATIVE_STATE_AND_REACHABILITY_AUDIT': gate4,
        'GATE5_EXACT_RESTORE': gate5,
        'GATE6_REQUIRED_ARTIFACT_CONTENT': gate6,
        'GATE7_ARTIFACT_INTEGRITY': 'PASS'}
    finalize863(gates, execution)
except BaseException as exc:
    EXECUTION_ERROR863 = type(exc).__name__ + ': ' + str(exc)
    TRACEBACK863 += '\n===== TEST863 OUTER FAILURE =====\n' + traceback.format_exc()
    sys.stdout, sys.stderr = CONSOLE863, ERROR_CONSOLE863
    short863(traceback.format_exc())
    gates = {'GATE0_SOURCE_INTEGRITY': 'PASS' if len(RAW_SOURCES863) == 27 else 'FAIL',
        'GATE1_GPU_PREFLIGHT_NATIVE_TWO_JOBS': 'BLOCKED',
        'GATE2_HOOKFREE_OBSERVER_EQUIVALENCE': 'BLOCKED',
        'GATE3_862_NATIVE_REGRESSION': 'BLOCKED',
        'GATE4_NATIVE_STATE_AND_REACHABILITY_AUDIT': 'BLOCKED',
        'GATE5_EXACT_RESTORE': 'BLOCKED', 'GATE6_REQUIRED_ARTIFACT_CONTENT': 'BLOCKED',
        'GATE7_ARTIFACT_INTEGRITY': 'PASS'}
    finalize863(gates, 'TEST863_FAILURE_FULL_TRACEBACK_IN_LOG')
finally:
    LOG_FILE863.close()
