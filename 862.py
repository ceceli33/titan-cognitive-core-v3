# AKBASCORE SILICON HIPPOCAMPUS — TEST862 NATIVE CANDIDATE-EVIDENCE CAUSAL SEPARATION
# Locked GPU-verified TEST861/860/859 spine; two unchanged original jobs.
# Fixed-Kprev 2x2 post-revision diagnostic panel; no native third cycle is claimed.
# Candidate and evidence states are model/cartridge outputs, never Python-written answers.
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

TEST862_KIND = 'NATIVE_CANDIDATE_EVIDENCE_CAUSAL_SEPARATION'
CODELOAD862 = 'https://codeload.github.com/ceceli33/titan-cognitive-core-v3/zip/refs/heads/main'
LOCKS862 = {
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
}
STATE_REL_L2_EPS862 = 1e-7
SCORE_ABS_EPS862 = 1e-6
REGRESSION_ABS_EPS862 = 1e-5
STATE_ORDER862 = ('C', 'E', 'U', 'R', 'Kprev', 'K0', 'J', 'Review')
FACTOR_ARMS862 = ('C0E0', 'C1E0', 'C0E1', 'C1E1')
NEGATIVE_ARMS862 = ('C0EIRR', 'C1EIRR')
SCORE_FIELDS862 = ('sequence_logp', 'mean_token_logp', 'first_token_logit',
    'first_token_logp', 'first_token_softmax_probability')
STAMP862 = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
ROOT862 = pathlib.Path('/content') / ('TEST862_CANDIDATE_EVIDENCE_' + STAMP862)
ROOT862.mkdir(parents=True, exist_ok=False)
CONSOLE862, ERROR_CONSOLE862 = sys.stdout, sys.stderr
LOG_FILE862 = open(ROOT862 / '862.log', 'w', encoding='utf-8')
START862 = time.perf_counter()
REAL_COMPILE862 = builtins.compile
RAW_SOURCES862 = {}
STATE862 = {'spine_loaded': False, 'dependency_audit': {},
    'original_record_sha256': None, 'diagnostic_assessments': 0,
    'diagnostic_candidate_generations': 0, 'conditions': {}, 'effects': {},
    'controls': {}, 'analysis': {}}
CANDIDATES862, EVIDENCE862 = {}, {}
PANEL_ROWS862, PANEL_HS862 = {}, {}
EXECUTION_ERROR862 = None
PROBE_ERROR862 = None
TRACEBACK862 = ''
ERROR_EVIDENCE862 = {}
TWO_JOB_VERIFICATION862 = {}
ANALYSIS862 = {}
DIAGNOSTIC_CONTROL_STOP862 = None

# Compatibility namespaces: only selected definitions are executed, never old experiments.
ROOT861 = ROOT860 = ROOT859 = ROOT862
LOG_FILE861 = LOG_FILE860 = LOG_FILE859 = LOG_FILE862
START861 = START860 = START859 = START862
CONSOLE861 = CONSOLE860 = CONSOLE859 = CONSOLE862
ERROR_CONSOLE861 = ERROR_CONSOLE860 = ERROR_CONSOLE859 = ERROR_CONSOLE862
REAL_COMPILE861 = REAL_COMPILE860 = REAL_COMPILE859 = REAL_COMPILE862
RAW_SOURCES861 = RAW_SOURCES860 = RAW_SOURCES859 = RAW_SOURCES862
LOCKS861 = {k: v for k, v in LOCKS862.items() if not k.startswith('861.')}
STATE_REL_L2_EPS861 = STATE_REL_L2_EPS862
SCORE_ABS_EPS861 = SCORE_ABS_EPS862
REGRESSION_ABS_EPS861 = REGRESSION_ABS_EPS862
STATE861 = {'spine_loaded': False, 'spine_json': {}, 'native_sequences': {},
    'arms': {}, 'comparisons': [], 'analysis': {}, 'diagnostic_executions': 0,
    'original_record_sha256': None, 'dependency_audit': {}}
STATE860 = {'spine_loaded': False, 'spine_json': {}, 'conditions': [],
    'native_sequences': {}, 'condition_results': {}, 'comparisons': [],
    'analysis': {}, 'original_record_sha256': None}
STATE859 = {'installed': False, 'compiled': False, 'equalities': [],
    'observations': [], 'coverage': [], 'frames': [], 'g': None, 'active': None,
    'capture': None, 'tokenizations': {}, 'hook_audits': [], 'saved_jobs': [],
    'invocations': [], 'contexts': [], 'transitions': {}, 'offline_functions': {},
    'decision_comparison': {}, 'causal_probes': [], 'original_record_sha256': None,
    'environment': {}, 'start': START862}
FAILURES859 = []
LAST_CONTEXT859 = None
SPELLINGS859 = (' CONTINUE', ' REVISE', ' STOP', ' SUFFICIENT', ' INSUFFICIENT')


def short862(*args):
    text = ' '.join(str(x) for x in args)
    print(text, file=CONSOLE862, flush=True)
    LOG_FILE862.write(text + '\n')
    LOG_FILE862.flush()


def json_write862(name, value):
    path = ROOT862 / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
        allow_nan=False), encoding='utf-8')
    return path


def sha256_bytes862(data):
    return hashlib.sha256(data).hexdigest()


def git_blob862(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


short861 = short862
json_write861 = json_write862
sha256_bytes861 = sha256_bytes862
git_blob861 = git_blob862


def capture_cell_source862():
    try:
        shell = get_ipython()  # noqa: F821 — supplied by Colab/IPython.
        history = list(shell.history_manager.input_hist_raw)
        marker = 'AKBASCORE SILICON HIPPOCAMPUS — TEST862 NATIVE CANDIDATE-EVIDENCE CAUSAL SEPARATION'
        candidates = [text for text in history if marker in text]
        if candidates:
            (ROOT862 / '862.py').write_text(candidates[-1], encoding='utf-8')
            return True
    except Exception as exc:
        short862('862.py history capture unavailable:', type(exc).__name__, str(exc))
    return False


def load_sources862():
    request = urllib.request.Request(CODELOAD862,
        headers={'User-Agent': 'AKBASCORE-TEST862-GATE0'})
    with urllib.request.urlopen(request, timeout=240) as response:
        archive = response.read(100000001)
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        for name, expected in LOCKS862.items():
            matches = [n for n in zipped.namelist() if n.endswith('/' + name)]
            assert len(matches) == 1, ('SOURCE_NOT_UNIQUE', name, matches)
            data = zipped.read(matches[0])
            actual = git_blob862(data)
            assert actual == expected, ('SOURCE_GIT_BLOB_MISMATCH', name, expected, actual)
            RAW_SOURCES862[name] = data
            short862('TABLE A SOURCE', name, actual, 'PASS')
    assert len(RAW_SOURCES862) == 25
    return RAW_SOURCES862


def _selected861_nodes862():
    tree = ast.parse(RAW_SOURCES862['861.py'].decode('utf-8'), filename='861.py')
    names = {'short861', 'json_write861', 'sha256_bytes861', 'git_blob861',
        '_selected860_nodes861', '_selected859_nodes861', '_dependency_audit861',
        'load_spine861', 'records_digest861', 'motor_map861', 'parse_reference860',
        'margins_close861', 'native_regression861', 'offline_revision_quality861',
        'state_summary861'}
    nodes = [copy.deepcopy(n) for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == names
    return tree, nodes


def load_spine862():
    assert not STATE862['spine_loaded']
    tree861, nodes861 = _selected861_nodes862()
    exec(REAL_COMPILE862(ast.fix_missing_locations(ast.Module(
        body=nodes861, type_ignores=[])), 'TEST862_REUSED_861_DEFINITIONS_ONLY', 'exec'), globals())
    load_spine861()
    tree860, nodes860 = _selected860_nodes861()
    nodes859 = _selected859_nodes861(tree860)
    _dependency_audit861(nodes861 + nodes860 + nodes859)
    STATE862['dependency_audit'] = copy.deepcopy(STATE861['dependency_audit'])
    STATE862['spine_loaded'] = True
    short862('TABLE A SPINE', '861+860+859 selected definitions only',
        'top-level experiment exec=0', 'static global missing=0')


def parse_reference861():
    text = RAW_SOURCES862['861.log'].decode('utf-8')
    required = ('TEST861 TECHNICAL TECHNICAL_XRAY_PASS',
        'GATE3_860_REGRESSION_AND_CORRECT_REVISION PASS',
        'GATE4_MATCHED_CARRY_XRAY_AND_RESTORE PASS',
        'GATE5_CORRECT_REVISION_REPRODUCTION OBSERVED_DIAGNOSTIC_ONLY',
        'GATE7_GREEDY_ACTION_EFFECT OBSERVED_DIAGNOSTIC_ONLY',
        'TEST861 NATIVE CLOSURE EVIDENCE_ALIGNED_NATIVE_CLOSURE_NOT_OBSERVED')
    for item in required:
        assert item in text, ('REFERENCE_861_GATE_MISSING', item)
    pattern = re.compile(
        r'^TABLE C REVISION GENERATION NOVEL_CORRECT_REVISION (\S+) (.+?) offline .* margins (\{.*\})$',
        re.MULTILINE)
    match = pattern.search(text)
    assert match, 'REFERENCE_861_NOVEL_GENERATION_MISSING'
    action, revision, margins = match.groups()
    post = re.search(r'^TABLE H NATIVE VS DIAGNOSTIC NOVEL_CORRECT_REVISION post action (\S+)',
        text, re.MULTILINE)
    assert post, 'REFERENCE_861_POST_ACTION_MISSING'
    return {'generation_action': action, 'revision_text': ast.literal_eval(revision),
        'generation_margins': ast.literal_eval(margins),
        'post_action_with_natural_kprev': post.group(1),
        'native_autonomous_closure_observed': False}


def native_closure862(env):
    evidence = []
    for job in env['JOBS841'][:2]:
        record = env['REC841'][job['job']]
        wi = env['QID841'].index(job['qid'])
        world = env['worlds829'][wi]
        mounted = set(record['mounted_cards'])
        grounded_revisions = []
        for cycle in record['cycles']:
            revision = cycle.get('revision')
            if revision is not None:
                grounded_revisions.append(bool(env['supported851'](
                    revision['text'], world, mounted)))
        answer = record.get('answer')
        answer_text = answer.get('text') if isinstance(answer, dict) else answer
        grounded_answer = bool(answer_text and env['supported851'](answer_text, world, mounted))
        closure = bool(any(grounded_revisions) and grounded_answer and
            any(c['action'] == 'REVISE' for c in record['cycles']) and
            record['end'] in ('MODEL_ACCEPT', 'MODEL_STOP'))
        evidence.append({'job': job['job'], 'end': record['end'],
            'grounded_revisions': grounded_revisions, 'grounded_answer': grounded_answer,
            'native_autonomous_correction_closure': closure})
    return evidence


def _gpu_begin862(env):
    torch = env['torch']
    torch.cuda.synchronize()
    torch.cuda.reset_peak_memory_stats()
    return time.perf_counter()


def _gpu_end862(env, started):
    torch = env['torch']
    torch.cuda.synchronize()
    return {'seconds': time.perf_counter() - started,
        'peak_gpu_gib': torch.cuda.max_memory_allocated() / 1024 ** 3,
        'reserved_gpu_gib': torch.cuda.memory_reserved() / 1024 ** 3}


def _check_h862(h, label):
    continuity = h['trace849']['continuity']
    assert continuity.get('exact_after_bf16'), (label + '_BF16_CONTINUITY_FAILED', continuity)
    assert h['rows'].dtype.is_floating_point and h['rows'].device.type == 'cpu'
    return continuity


def _slot_continuity862(env, invocation, slot, label):
    row = continuity_for_slot859(env, invocation, slot)
    assert row.get('status') == 'CHECKED' and row.get('exact_after_bf16'), (
        label + '_SLOT_BF16_OR_POSITION_CONTINUITY_FAILED', row)
    return row


def evidence_sufficient862(env, job, cards):
    world = env['worlds829'][env['QID841'].index(job['qid'])]
    ids = world['ids']
    mounted = set(cards)
    return ids['first'] in mounted and bool({ids['second'], ids['changed']} & mounted)


def public_candidate862(row):
    return {k: copy.deepcopy(v) for k, v in row.items() if k not in ('rows', 'h')}


def public_evidence862(row):
    return {k: copy.deepcopy(v) for k, v in row.items()
        if k not in ('memx', 'E', 'U', 'evidence_h', 'coverage_h')}


def prepare_e0_862(env, job, snap):
    record = env['REC841'][job['job']]
    pm = segment_map859(env, snap['pre1']['segments'])
    cycle = record['cycles'][1]
    row = {'label': 'E0', 'factor_level': 0, 'execution': 'ORIGINAL_NATIVE',
        'source_cards': list(record['mounted_cards']),
        'source_stages': ['precontrol_1'], 'memx': snap['pre1']['memx'],
        'E': pm['E'][1], 'U': pm['U'][1],
        'evidence_text': cycle['evidence']['text'],
        'coverage_text': cycle['coverage_native']['text'],
        'E_summary': state_summary861(env, pm['E'][1]),
        'U_summary': state_summary861(env, pm['U'][1]),
        'evidence_sufficient_offline': evidence_sufficient862(env, job, record['mounted_cards']),
        'physical_memory_source': 'Original REMOVED cycle1 memx and native precontrol_1 E/U slots.',
        'labels_entered_native_inputs': False}
    assert not row['evidence_sufficient_offline']
    row['seal_before'] = env['seal834'](row['memx'])
    EVIDENCE862['E0'] = row
    return row


def prepare_evidence862(env, job, condition, label):
    assert label in ('E1', 'EIRR')
    started = _gpu_begin862(env)
    memx, temporary, mount_ms = env['mem_for841'](
        list(condition['source_cards']), 'TEST862_' + label)
    evidence_pre = list(env['prompt_ids'](env['EVIDENCE851'].format(q=env['QTEXT841'][job['qid']])))
    coverage_pre = list(env['prompt_ids'](env['COVERAGE852'].format(q=env['QTEXT841'][job['qid']])))
    evidence = env['gen849'](memx, evidence_pre, None, env['ANSWER_SUFFIX851'])
    coverage = env['gen849'](memx, coverage_pre, None, env['COVERAGE_SUFFIX852'])
    _check_h862(evidence, label + '_EVIDENCE')
    _check_h862(coverage, label + '_COVERAGE')
    row = {'label': label, 'factor_level': 1 if label == 'E1' else None,
        'execution': 'DIAGNOSTIC_REPLAY', 'condition': condition['condition'],
        'source_cards': list(condition['source_cards']),
        'source_stages': ['native gen849 evidence', 'native gen849 coverage'],
        'memx': memx, 'E': evidence['rows'], 'U': coverage['rows'],
        'evidence_h': evidence, 'coverage_h': coverage,
        'evidence_text': evidence['text'], 'coverage_text': coverage['text'],
        'E_summary': state_summary861(env, evidence['rows']),
        'U_summary': state_summary861(env, coverage['rows']),
        'evidence_sufficient_offline': evidence_sufficient862(env, job, condition['source_cards']),
        'physical_memory_source': 'Locked mem_for841 physical cartridge mount; no semantic text injection into slots.',
        'semantics_offline_only': condition['semantics'], 'mount_ms': mount_ms,
        'labels_entered_native_inputs': False}
    row.update(_gpu_end862(env, started))
    expected = label == 'E1'
    assert row['evidence_sufficient_offline'] == expected, (label + '_OFFLINE_SUFFICIENCY_MISMATCH')
    row['seal_before'] = env['seal834'](memx)
    EVIDENCE862[label] = row
    return row


def source_c0_862(env, job, snap):
    h = snap['revision1']['h']
    _check_h862(h, 'C0_SOURCE')
    quality = offline_revision_quality861(env, job, h['text'],
        EVIDENCE862['E0']['source_cards'], snap['revision0']['h']['text'])
    assert not quality['candidate_correct_for_task'], 'C0_IS_NOT_UNKNOWN_OR_INCORRECT'
    row = {'label': 'C0', 'factor_level': 0, 'execution': 'ORIGINAL_NATIVE',
        'rows': h['rows'], 'h': h, 'text': h['text'], 'source_stage': 'revision_1',
        'source_job': job['job'], 'state': state_summary861(env, h['rows']),
        'source_runtime_continuity': h['trace849']['continuity'],
        'offline_quality': quality,
        'provenance': 'Original REMOVED native cycle1 revision_1.rows; no text written by Python.',
        'labels_entered_native_inputs': False}
    CANDIDATES862['C0'] = row
    return row


def generate_c1_862(env, job, snap, reference):
    torch = env['torch']
    e1 = EVIDENCE862['E1']
    STATE862['diagnostic_candidate_generations'] += 1
    assert STATE862['diagnostic_candidate_generations'] == 1
    started = _gpu_begin862(env)
    C = snap['revision0']['h']['rows']
    Kprev_seed = snap['review0']['h']['rows']
    E, U = e1['E'], e1['U']
    R = env['relation852'](C, E)
    segments = [(list(env['C_SLOT851']), C), (list(env['E_SLOT851']), E),
        (list(env['K_SLOT851']), Kprev_seed), (list(env['U_SLOT852']), U),
        (list(env['R_SLOT852']), R)]
    K0 = env['gen851'](e1['memx'], list(snap['pre1']['pre']), segments,
        list(snap['pre1']['post']))
    pre_inv = {'pre': list(snap['pre1']['pre']), 'segments': segments,
        'post': list(snap['pre1']['post']), 'h': K0}
    J = env['interaction854'](C, E, K0['rows'])
    decision = [(list(env['K_SLOT854']), K0['rows']), (list(env['J_SLOT854']), J)]
    review = env['gen851'](e1['memx'], list(snap['review1']['pre']), decision,
        list(snap['review1']['post']))
    review_inv = {'pre': list(snap['review1']['pre']), 'segments': decision,
        'post': list(snap['review1']['post']), 'h': review}
    scores = score_actions859(env, e1['memx'], list(snap['review1']['pre']),
        decision, list(snap['review1']['post']))
    action = env['parse849'](review['text'])
    assert action != 'INVALID', 'C1_GENERATION_INVALID_IS_NOT_STOP'
    for slot in (env['C_SLOT851'], env['E_SLOT851'], env['K_SLOT851'],
        env['U_SLOT852'], env['R_SLOT852']):
        _slot_continuity862(env, pre_inv, slot, 'C1_GENERATION_PRE')
    for slot in (env['K_SLOT854'], env['J_SLOT854']):
        _slot_continuity862(env, review_inv, slot, 'C1_GENERATION_REVIEW')
    _check_h862(K0, 'C1_GENERATION_K0')
    _check_h862(review, 'C1_GENERATION_REVIEW')
    margins = margins860(scores)
    regression = margins_close861(margins, reference['generation_margins'])
    assert action == reference['generation_action'] and regression['within_preregistered_tolerance'], (
        'TEST861_C1_GENERATION_REGRESSION_FAILED', action, regression)
    assert action == 'REVISE', 'NO_REVISION_PATH_TO_OBTAIN_C1'
    recompute = list(env['prompt_ids'](env['RECOMPUTE851'].format(q=env['QTEXT841'][job['qid']])))
    revision = env['gen851'](e1['memx'], recompute,
        [(list(env['C_SLOT851']), C), (list(env['K_SLOT851']), review['rows']),
         (list(env['E_SLOT851']), E), (list(env['U_SLOT852']), U),
         (list(env['R_SLOT852']), R)], list(env['ANSWER_SUFFIX851']))
    _check_h862(revision, 'C1_REVISION')
    assert revision['text'] == reference['revision_text'], (
        'TEST861_CORRECT_REVISION_TEXT_REGRESSION_FAILED', revision['text'])
    quality = offline_revision_quality861(env, job, revision['text'],
        e1['source_cards'], snap['revision0']['h']['text'])
    assert quality['candidate_correct_for_task'] and quality['revision_grounded_by_mounted_evidence'], (
        'C1_OFFLINE_CORRECTNESS_OR_GROUNDING_FAILED', quality)
    row = {'label': 'C1', 'factor_level': 1, 'execution': 'DIAGNOSTIC_REPLAY',
        'rows': revision['rows'], 'h': revision, 'text': revision['text'],
        'source_stage': 'TEST861-matched NOVEL_CORRECT_REVISION native gen851 output',
        'source_job': job['job'], 'state': state_summary861(env, revision['rows']),
        'source_runtime_continuity': revision['trace849']['continuity'],
        'offline_quality': quality,
        'provenance': 'Model-generated revision.rows under E1; no Python answer text or fixed embedding.',
        'natural_kprev_state_not_used_in_fixed_panel': state_summary861(env, review['rows']),
        'labels_entered_native_inputs': False}
    CANDIDATES862['C1'] = row
    result = {'execution': 'DIAGNOSTIC_REPLAY', 'phase': 'TEST861_MATCHED_CYCLE1_REVISION_GENERATION',
        'action': action, 'revision_text': revision['text'], 'scores': scores,
        'margins': margins, 'regression_to_861': regression,
        'review': h_summary859(env, review), 'revision': h_summary859(env, revision),
        'offline_quality': quality, 'natural_kprev_used_by_861_post': True,
        'fixed_panel_kprev_is_different_control': True}
    result.update(_gpu_end862(env, started))
    short862('TABLE D CANDIDATE C1 REGENERATION', action, repr(revision['text']),
        '861 generation regression PASS', 'offline correct+grounded PASS')
    return result


def _protocol862(env, snap):
    payload = {'precontrol_pre': list(snap['pre1']['pre']),
        'precontrol_post': list(snap['pre1']['post']),
        'review_pre': list(snap['review1']['pre']),
        'review_post': list(snap['review1']['post'])}
    return {k + '_sha256': sha256_bytes862(json.dumps(v).encode()) for k, v in payload.items()}


def run_condition862(env, arm, candidate_label, evidence_label, fixed_kprev, snap,
        execution='DIAGNOSTIC_FACTORIAL_INTERVENTION'):
    torch = env['torch']
    job = env['JOBS841'][1]
    candidate = CANDIDATES862[candidate_label]
    evidence = EVIDENCE862[evidence_label]
    STATE862['diagnostic_assessments'] += 1
    started = _gpu_begin862(env)
    C, E, U = candidate['rows'], evidence['E'], evidence['U']
    Kprev = fixed_kprev
    # Soft-row counts may natively differ; role/width/continuity, not shape alone, govern validity.
    assert C.ndim == E.ndim == U.ndim == Kprev.ndim == 2
    assert C.shape[1] == E.shape[1] == U.shape[1] == Kprev.shape[1] == env['H']
    assert C.dtype == E.dtype == U.dtype == Kprev.dtype == torch.float32
    assert C.device.type == E.device.type == U.device.type == Kprev.device.type == 'cpu'
    R = env['relation852'](C, E)
    segments = [(list(env['C_SLOT851']), C), (list(env['E_SLOT851']), E),
        (list(env['K_SLOT851']), Kprev), (list(env['U_SLOT852']), U),
        (list(env['R_SLOT852']), R)]
    K0 = env['gen851'](evidence['memx'], list(snap['pre1']['pre']), segments,
        list(snap['pre1']['post']))
    pre_inv = {'pre': list(snap['pre1']['pre']), 'segments': segments,
        'post': list(snap['pre1']['post']), 'h': K0}
    J = env['interaction854'](C, E, K0['rows'])
    decision = [(list(env['K_SLOT854']), K0['rows']), (list(env['J_SLOT854']), J)]
    review = env['gen851'](evidence['memx'], list(snap['review1']['pre']), decision,
        list(snap['review1']['post']))
    review_inv = {'pre': list(snap['review1']['pre']), 'segments': decision,
        'post': list(snap['review1']['post']), 'h': review}
    scores = score_actions859(env, evidence['memx'], list(snap['review1']['pre']),
        decision, list(snap['review1']['post']))
    action = env['parse849'](review['text'])
    invalid_negative = action == 'INVALID' and arm in NEGATIVE_ARMS862
    assert action != 'INVALID' or invalid_negative, (arm + '_INVALID_IS_NOT_STOP_OR_UNKNOWN')
    # A malformed optional negative-control review is N/A, never STOP and never a main-panel failure.
    _check_h862(K0, arm + '_K0')
    _check_h862(review, arm + '_REVIEW')
    slot_continuity = {}
    for name, slot in (('C', env['C_SLOT851']), ('E', env['E_SLOT851']),
        ('Kprev', env['K_SLOT851']), ('U', env['U_SLOT852']), ('R', env['R_SLOT852'])):
        slot_continuity[name] = _slot_continuity862(env, pre_inv, slot, arm + '_' + name)
    for name, slot in (('K0', env['K_SLOT854']), ('J', env['J_SLOT854'])):
        slot_continuity[name] = _slot_continuity862(env, review_inv, slot, arm + '_' + name)
    rows = {'C': C, 'E': E, 'U': U, 'R': R, 'Kprev': Kprev,
        'K0': K0['rows'], 'J': J, 'Review': review['rows']}
    states = {name: state_summary861(env, value) for name, value in rows.items()}
    assert all(x['finite'] for x in states.values())
    assert env['seal834'](evidence['memx']) == evidence['seal_before'], (
        arm + '_PHYSICAL_CARTRIDGE_MUTATED')
    quality = offline_revision_quality861(env, job, candidate['text'],
        evidence['source_cards'], snap['revision0']['h']['text'])
    previous_correct = env['node851'](snap['revision0']['h']['text'],
        env['worlds829'][env['QID841'].index(job['qid'])]) == 'end'
    quality['previous_candidate_correct_offline'] = previous_correct
    quality['previous_candidate_error_corrected_offline'] = bool(
        not previous_correct and quality['candidate_correct_for_task'])
    decision_quality = decision_quality860(env, job, action, candidate['text'],
        None, evidence['source_cards'])
    source_destination = {}
    for name, source, slot in (
        ('C', candidate['rows'], env['C_SLOT851']),
        ('E', evidence['E'], env['E_SLOT851']),
        ('U', evidence['U'], env['U_SLOT852']),
        ('Kprev', fixed_kprev, env['K_SLOT851'])):
        source_summary = state_summary861(env, source)
        destination_summary = states[name]
        assert source_summary['sha256'] == destination_summary['sha256']
        assert torch.equal(source, rows[name])
        source_destination[name] = {'source': source_summary,
            'destination': destination_summary, 'exact': True,
            'source_role': name, 'destination_role': name,
            'slot_ids': list(slot), 'bf16': slot_continuity[name],
            'position_and_rope_path': 'Locked gen851/make_x851 slot positions; no manual positional state injection.'}
    result = {'arm': arm, 'candidate_factor': candidate_label,
        'evidence_factor': evidence_label, 'execution': execution,
        'status': 'NOT_APPLICABLE' if invalid_negative else 'COMPLETE',
        'invalid_reason': 'Native greedy review text did not parse as CONTINUE/REVISE/STOP; optional negative control only.' if invalid_negative else None,
        'phase': 'POST_REVISION_REASSESSMENT_NOT_NATIVE_CYCLE',
        'job': job['job'], 'qid': job['qid'],
        'candidate_text_offline_only': candidate['text'],
        'source_cards': list(evidence['source_cards']),
        'evidence_text': evidence['evidence_text'], 'coverage_text': evidence['coverage_text'],
        'greedy_action': action,
        'score_argmax_action': max(scores, key=lambda x: x['sequence_logp'])['spelling'].strip(),
        'scores': scores, 'margins': margins860(scores), 'state': states,
        'source_destination_integrity': source_destination,
        'slot_continuity': slot_continuity,
        'review': h_summary859(env, review), 'offline_quality': quality,
        'decision_quality_offline_only': decision_quality,
        'diagnostic_stop_action': action == 'STOP', 'native_model_stop': False,
        'native_model_accept': False, 'new_revision_generated': False,
        'fixed_kprev_control': True, 'protocol': _protocol862(env, snap),
        'labels_entered_native_inputs': False}
    result.update(_gpu_end862(env, started))
    PANEL_ROWS862[arm] = rows
    PANEL_HS862[arm] = {'K0': K0, 'Review': review}
    STATE862['conditions'][arm] = result
    short862('TABLE G SCORES', arm, execution, action, json.dumps(scores),
        'margins', json.dumps(result['margins']))
    short862('TABLE F XRAY', arm, json.dumps(states))
    if invalid_negative:
        short862('TABLE C NEGATIVE CONTROL', arm, 'NOT_APPLICABLE',
            'INVALID is not STOP; raw Review and scores retained.')
    return result


def state_difference862(env, before, after):
    out = {}
    for name in STATE_ORDER862:
        row = paired_metrics859(env, PANEL_ROWS862[before][name], PANEL_ROWS862[after][name])
        row['before_sha256'] = STATE862['conditions'][before]['state'][name]['sha256']
        row['after_sha256'] = STATE862['conditions'][after]['state'][name]['sha256']
        row['significant'] = bool(not row['exact'] and (
            row['status'] == 'NOT_COMPARABLE_SHAPE' or
            (row.get('relative_l2') is not None and row['relative_l2'] > STATE_REL_L2_EPS862)))
        out[name] = row
    return out


def flat_decision_metrics862(result):
    flat = {}
    for score in result['scores']:
        name = score['spelling'].strip()
        for field in SCORE_FIELDS862:
            flat[name + '__' + field] = float(score[field])
    for name, value in result['margins'].items():
        flat['MARGIN__' + name] = float(value)
    return flat


def effect862(env, before, after, label, family):
    a = flat_decision_metrics862(STATE862['conditions'][before])
    b = flat_decision_metrics862(STATE862['conditions'][after])
    assert set(a) == set(b)
    deltas = {name: b[name] - a[name] for name in sorted(a)}
    xray = state_difference862(env, before, after)
    return {'comparison': label, 'family': family, 'formula': after + ' - ' + before,
        'before': before, 'after': after, 'execution': 'MATCHED_POST_HOC_COMPARISON',
        'valid': True, 'score_deltas': deltas,
        'significant_metrics': [name for name, value in deltas.items()
            if abs(value) > SCORE_ABS_EPS862],
        'state_xray': xray,
        'first_changed_state': next((name for name in STATE_ORDER862
            if xray[name]['significant']), None),
        'greedy_transition': {'before': STATE862['conditions'][before]['greedy_action'],
            'after': STATE862['conditions'][after]['greedy_action'],
            'changed': STATE862['conditions'][before]['greedy_action'] !=
                STATE862['conditions'][after]['greedy_action']},
        'teacher_forced_scores_are_not_calibrated_probabilities': True}


def panel_validity862(env, fixed_kprev):
    torch = env['torch']
    checks = {}
    def exact_rows(a, b, state):
        return torch.equal(PANEL_ROWS862[a][state], PANEL_ROWS862[b][state])
    checks['C0_exact_across_E'] = exact_rows('C0E0', 'C0E1', 'C')
    checks['C1_exact_across_E'] = exact_rows('C1E0', 'C1E1', 'C')
    checks['E0_exact_across_C'] = exact_rows('C0E0', 'C1E0', 'E')
    checks['E1_exact_across_C'] = exact_rows('C0E1', 'C1E1', 'E')
    checks['U0_exact_across_C'] = exact_rows('C0E0', 'C1E0', 'U')
    checks['U1_exact_across_C'] = exact_rows('C0E1', 'C1E1', 'U')
    checks['Kprev_exact_all_four'] = all(torch.equal(PANEL_ROWS862[x]['Kprev'], fixed_kprev)
        for x in FACTOR_ARMS862)
    protocols = [STATE862['conditions'][x]['protocol'] for x in FACTOR_ARMS862]
    checks['same_prompt_protocol'] = all(x == protocols[0] for x in protocols)
    checks['same_question_job_model_stage'] = all(
        STATE862['conditions'][x]['qid'] == env['JOBS841'][1]['qid'] and
        STATE862['conditions'][x]['phase'] == 'POST_REVISION_REASSESSMENT_NOT_NATIVE_CYCLE'
        for x in FACTOR_ARMS862)
    checks['same_action_spellings'] = all(
        [s['spelling'] for s in STATE862['conditions'][x]['scores']] ==
        [' CONTINUE', ' REVISE', ' STOP'] for x in FACTOR_ARMS862)
    checks['candidate_factor_offline_valid'] = bool(
        not CANDIDATES862['C0']['offline_quality']['candidate_correct_for_task'] and
        CANDIDATES862['C1']['offline_quality']['candidate_correct_for_task'])
    checks['evidence_factor_offline_valid'] = bool(
        not EVIDENCE862['E0']['evidence_sufficient_offline'] and
        EVIDENCE862['E1']['evidence_sufficient_offline'])
    checks['frozen_model'] = not any(p.requires_grad for p in env['model'].parameters())
    checks['cartridges_unchanged'] = all(env['seal834'](EVIDENCE862[x]['memx']) ==
        EVIDENCE862[x]['seal_before'] for x in EVIDENCE862)
    checks['bf16_and_role_integrity'] = all(
        all(v['bf16'].get('exact_after_bf16') for v in
            STATE862['conditions'][x]['source_destination_integrity'].values())
        for x in FACTOR_ARMS862)
    valid = all(checks.values())
    for arm in FACTOR_ARMS862:
        STATE862['conditions'][arm]['factorial_condition_valid'] = valid
        short862('TABLE C CONDITION VALIDITY', arm, 'VALID' if valid else 'INVALID',
            STATE862['conditions'][arm]['execution'], 'fixed Kprev; native third cycle=False')
    return {'valid': valid, 'checks': checks,
        'fixed_kprev_state': state_summary861(env, fixed_kprev),
        'fixed_kprev_source': 'Original REMOVED review_1.rows, identical in C0E0/C1E0/C0E1/C1E1.',
        'natural_kprev_panel_execution': 'NOT_RUN_SEPARATE_COMPARISON_UNRESOLVED',
        'candidate_dependents_recomputed': ['R', 'K0', 'J', 'Review'],
        'evidence_dependents_recomputed': ['R', 'K0', 'J', 'Review'],
        'U_recomputed_once_per_evidence_mount_and_reused_exact': True,
        'labels_entered_native_inputs': False}


def compare_control862(env, reference_arm, replay_arm, label):
    torch = env['torch']
    reference = STATE862['conditions'][reference_arm]
    replay = STATE862['conditions'][replay_arm]
    states = {}
    for name in STATE_ORDER862:
        states[name] = paired_metrics859(env, PANEL_ROWS862[reference_arm][name],
            PANEL_ROWS862[replay_arm][name])
    exact_states = all(x['exact'] for x in states.values())
    exact_h = all(native_h_equal859(torch, PANEL_HS862[reference_arm][stage],
        PANEL_HS862[replay_arm][stage]) for stage in ('K0', 'Review'))
    exact_scores = reference['scores'] == replay['scores']
    exact_action = reference['greedy_action'] == replay['greedy_action']
    exact = exact_states and exact_h and exact_scores and exact_action
    result = {'control': label, 'reference': reference_arm, 'replay': replay_arm,
        'execution': 'DIAGNOSTIC_REPLAY', 'exact': exact,
        'exact_states': exact_states, 'exact_native_outputs': exact_h,
        'exact_scores': exact_scores, 'exact_greedy_action': exact_action,
        'states': states,
        'reference_action': reference['greedy_action'], 'replay_action': replay['greedy_action'],
        'reference_scores': reference['scores'], 'replay_scores': replay['scores'],
        'difference_diagnosis': 'EXACT' if exact else
            'UNRESOLVED_NUMERICAL_INSTABILITY_OR_UNCONTROLLED_EXECUTION_STATE',
        'original_native_post_revision_baseline_exists': False,
        'labels_entered_native_inputs': False}
    STATE862['controls'][label] = result
    short862('TABLE L CONTROL', label, 'EXACT' if exact else 'FAILED',
        reference_arm, replay_arm, result['difference_diagnosis'])
    return result


def compute_effects862(env, panel_valid):
    if not panel_valid:
        return {'status': 'NOT_COMPUTED_FACTORIAL_PANEL_NOT_VALID',
            'candidate_main': {}, 'evidence_main': {}, 'interaction': {},
            'negative_controls': {}}
    candidate = {
        'CANDIDATE_AT_E0': effect862(env, 'C0E0', 'C1E0',
            'CANDIDATE_AT_E0', 'CANDIDATE_MAIN_EFFECT'),
        'CANDIDATE_AT_E1': effect862(env, 'C0E1', 'C1E1',
            'CANDIDATE_AT_E1', 'CANDIDATE_MAIN_EFFECT')}
    evidence = {
        'EVIDENCE_AT_C0': effect862(env, 'C0E0', 'C0E1',
            'EVIDENCE_AT_C0', 'EVIDENCE_MAIN_EFFECT'),
        'EVIDENCE_AT_C1': effect862(env, 'C1E0', 'C1E1',
            'EVIDENCE_AT_C1', 'EVIDENCE_MAIN_EFFECT')}
    all_metrics = flat_decision_metrics862(STATE862['conditions']['C0E0'])
    interaction_deltas = {}
    for name in sorted(all_metrics):
        a = flat_decision_metrics862(STATE862['conditions']['C0E0'])[name]
        b = flat_decision_metrics862(STATE862['conditions']['C1E0'])[name]
        c = flat_decision_metrics862(STATE862['conditions']['C0E1'])[name]
        d = flat_decision_metrics862(STATE862['conditions']['C1E1'])[name]
        interaction_deltas[name] = (d - b) - (c - a)
    interaction = {'formula': '(C1E1 - C1E0) - (C0E1 - C0E0)',
        'execution': 'MATCHED_POST_HOC_COMPARISON', 'valid': True,
        'score_deltas': interaction_deltas,
        'significant_metrics': [name for name, value in interaction_deltas.items()
            if abs(value) > SCORE_ABS_EPS862],
        'greedy_action_arithmetic_applied': False,
        'interpretation': 'Factorial output interaction only; not consciousness, understanding or autonomous reasoning.'}
    for group in (candidate, evidence):
        names = sorted(all_metrics)
        consistency = {}
        rows = list(group.values())
        for name in names:
            x, y = rows[0]['score_deltas'][name], rows[1]['score_deltas'][name]
            consistency[name] = {
                'both_nonzero': abs(x) > SCORE_ABS_EPS862 and abs(y) > SCORE_ABS_EPS862,
                'same_direction': (x > SCORE_ABS_EPS862 and y > SCORE_ABS_EPS862) or
                    (x < -SCORE_ABS_EPS862 and y < -SCORE_ABS_EPS862),
                'delta_1': x, 'delta_2': y}
        for row in rows:
            row['cross_level_metric_consistency'] = consistency
    negative_specs = (
        ('CANDIDATE_AT_IRRELEVANT', 'C0EIRR', 'C1EIRR'),
        ('IRRELEVANT_AT_C0_VS_E0', 'C0E0', 'C0EIRR'),
        ('IRRELEVANT_AT_C1_VS_E0', 'C1E0', 'C1EIRR'),
        ('IRRELEVANT_AT_C0_VS_E1', 'C0E1', 'C0EIRR'),
        ('IRRELEVANT_AT_C1_VS_E1', 'C1E1', 'C1EIRR'))
    negative = {}
    for name, before, after in negative_specs:
        if any(STATE862['conditions'][x].get('status') == 'NOT_APPLICABLE'
                for x in (before, after)):
            negative[name] = {'comparison': name, 'family': 'NEGATIVE_CONTROL',
                'status': 'NOT_APPLICABLE', 'valid': False, 'before': before, 'after': after,
                'reason': 'At least one optional irrelevant-control greedy review is INVALID; no effect arithmetic is fabricated.',
                'part_of_2x2_causal_estimand': False}
        else:
            negative[name] = effect862(env, before, after, name, 'NEGATIVE_CONTROL')
            negative[name]['part_of_2x2_causal_estimand'] = False
    combined = effect862(env, 'C0E0', 'C1E1',
        'COMBINED_CANDIDATE_AND_EVIDENCE', 'COMBINED_DIAGONAL_STATE_XRAY')
    result = {'status': 'MEASURED', 'candidate_main': candidate,
        'evidence_main': evidence, 'interaction': interaction,
        'combined_diagonal': combined,
        'negative_controls': negative, 'score_abs_epsilon': SCORE_ABS_EPS862,
        'state_relative_l2_epsilon': STATE_REL_L2_EPS862,
        'single_world_deterministic_contrasts_not_population_statistics': True}
    STATE862['effects'] = result
    for name, row in candidate.items():
        short862('TABLE H CANDIDATE MAIN EFFECT', name,
            json.dumps(row['score_deltas']), 'greedy', row['greedy_transition'])
    for name, row in evidence.items():
        short862('TABLE I EVIDENCE MAIN EFFECT', name,
            json.dumps(row['score_deltas']), 'greedy', row['greedy_transition'])
    short862('TABLE J CANDIDATE_X_EVIDENCE INTERACTION',
        json.dumps(interaction_deltas), 'significant', interaction['significant_metrics'])
    short862('TABLE K GREEDY TRANSITIONS', json.dumps({x: STATE862['conditions'][x]['greedy_action']
        for x in FACTOR_ARMS862 + NEGATIVE_ARMS862}))
    return result


def _has_effect_at_both_levels862(group):
    if len(group) != 2:
        return False
    rows = list(group.values())
    # A main-effect class requires a shared metric at both levels, not unrelated one-level changes.
    return bool(set(rows[0]['significant_metrics']) & set(rows[1]['significant_metrics']))


def _condition_public862(row):
    return {'arm': row['arm'], 'execution': row['execution'], 'phase': row['phase'],
        'status': row.get('status', 'COMPLETE'), 'invalid_reason': row.get('invalid_reason'),
        'candidate_factor': row['candidate_factor'], 'evidence_factor': row['evidence_factor'],
        'greedy_action': row['greedy_action'], 'score_argmax_action': row['score_argmax_action'],
        'scores': row['scores'], 'margins': row['margins'], 'state': row['state'],
        'offline_quality': row['offline_quality'],
        'decision_quality_offline_only': row['decision_quality_offline_only'],
        'fixed_kprev_control': row['fixed_kprev_control'],
        'native_model_stop': False, 'native_model_accept': False,
        'new_revision_generated': False}


def final_interpretation862(env, native, validity, effects):
    controls_exact = bool(STATE862['controls'].get('EXACT_RESTORE', {}).get('exact') and
        STATE862['controls'].get('SAME_STATE_REPLAY', {}).get('exact'))
    causal_valid = validity['valid'] and controls_exact
    candidate_effect = causal_valid and _has_effect_at_both_levels862(
        effects.get('candidate_main', {}))
    evidence_effect = causal_valid and _has_effect_at_both_levels862(
        effects.get('evidence_main', {}))
    interaction_effect = bool(causal_valid and effects.get('interaction', {}).get('significant_metrics'))
    actions = {x: STATE862['conditions'][x]['greedy_action'] for x in FACTOR_ARMS862}
    greedy_effect = causal_valid and len(set(actions.values())) > 1
    aligned = []
    for arm in FACTOR_ARMS862:
        row = STATE862['conditions'][arm]
        dq = row['decision_quality_offline_only']
        quality_metrics = dq['quality_metrics']
        if (row['greedy_action'] == 'CONTINUE' and
                quality_metrics['grounded_answer'] and not dq['unsupported_completion']):
            aligned.append(arm)
    diagnostic_aligned = causal_valid and bool(aligned)
    native_evidence = native_closure862(env)
    native_closure = any(x['native_autonomous_correction_closure'] for x in native_evidence)
    dimensions = {
        'A_FACTORIAL_PANEL_NOT_VALID': not validity['valid'],
        'B_CANDIDATE_MAIN_EFFECT_OBSERVED': candidate_effect,
        'C_EVIDENCE_MAIN_EFFECT_OBSERVED': evidence_effect,
        'D_CANDIDATE_EVIDENCE_INTERACTION_OBSERVED': interaction_effect,
        'E_GREEDY_ACTION_EFFECT_OBSERVED': greedy_effect,
        'F_EVIDENCE_ALIGNED_DIAGNOSTIC_DECISION_OBSERVED': diagnostic_aligned,
        'G_NATIVE_AUTONOMOUS_CLOSURE_OBSERVED': native_closure}
    scopes = {'A': 'FACTORIAL_VALIDITY', 'B': 'DIAGNOSTIC_FACTORIAL_INTERVENTION',
        'C': 'DIAGNOSTIC_FACTORIAL_INTERVENTION', 'D': 'DIAGNOSTIC_FACTORIAL_INTERVENTION',
        'E': 'DIAGNOSTIC_GREEDY_ONLY', 'F': 'DIAGNOSTIC_OFFLINE_EVALUATION',
        'G': 'ORIGINAL_NATIVE_ONLY'}
    classes = [name for name, value in dimensions.items() if value]
    if not classes:
        classes = ['UNRESOLVED']
    hypotheses = {
        'H1_CANDIDATE_MAIN_EFFECT': {'status': 'SUPPORTED_DIAGNOSTIC' if candidate_effect else
            'NOT_DEMONSTRATED' if causal_valid else 'UNRESOLVED',
            'evidence': ['CANDIDATE_AT_E0', 'CANDIDATE_AT_E1']},
        'H2_EVIDENCE_MAIN_EFFECT': {'status': 'SUPPORTED_DIAGNOSTIC' if evidence_effect else
            'NOT_DEMONSTRATED' if causal_valid else 'UNRESOLVED',
            'evidence': ['EVIDENCE_AT_C0', 'EVIDENCE_AT_C1']},
        'H3_CANDIDATE_EVIDENCE_INTERACTION': {'status': 'SUPPORTED_DIAGNOSTIC' if interaction_effect else
            'NOT_DEMONSTRATED' if causal_valid else 'UNRESOLVED',
            'evidence': ['(C1E1-C1E0)-(C0E1-C0E0)']}}
    possibilities = {
        'CANDIDATE_DOMINANT': {'status': 'SUPPORTED_COMPONENT' if candidate_effect else 'NOT_ESTABLISHED',
            'limit': 'No exclusive dominance claim; main effects and interaction may coexist.'},
        'EVIDENCE_DOMINANT': {'status': 'SUPPORTED_COMPONENT' if evidence_effect else 'NOT_ESTABLISHED',
            'limit': 'No exclusive dominance claim; teacher-forced scores are not calibrated probabilities.'},
        'COMBINED_EFFECT': {'status': 'SUPPORTED_COMPONENT' if interaction_effect else 'NOT_ESTABLISHED',
            'limit': 'Output interaction does not identify a unique semantic mechanism.'}}
    def brief(row):
        if not row:
            return {'status': 'NOT_MEASURED'}
        return {'score_deltas': row['score_deltas'],
            'significant_metrics': row['significant_metrics'],
            'greedy_transition': row['greedy_transition']}
    candidate_rows = effects.get('candidate_main', {})
    evidence_rows = effects.get('evidence_main', {})
    continue_metrics = {name: row.get('score_deltas', {}) for name, row in
        list(candidate_rows.items()) + list(evidence_rows.items())}
    answers = {
        '1_correct_candidate_alone_changes_scores': brief(candidate_rows.get('CANDIDATE_AT_E0')),
        '2_sufficient_evidence_alone_changes_scores': brief(evidence_rows.get('EVIDENCE_AT_C0')),
        '3_candidate_evidence_interaction': effects.get('interaction', {'status': 'NOT_MEASURED'}),
        '4_which_factor_changes_CONTINUE_tendency': continue_metrics,
        '5_which_factor_preserves_REVISE_tendency': {'actions': actions,
            'candidate_contrasts': brief(candidate_rows.get('CANDIDATE_AT_E0')),
            'evidence_contrasts': brief(evidence_rows.get('EVIDENCE_AT_C0'))},
        '6_STOP_score_changes': {name: {k: v for k, v in row.get('score_deltas', {}).items()
            if k.startswith('STOP__') or k.startswith('MARGIN__stop_')}
            for name, row in list(candidate_rows.items()) + list(evidence_rows.items())},
        '7_greedy_action_conditions': actions,
        '8_candidate_effect_on_J_and_Review': {name: {state: row['state_xray'][state]
            for state in ('J', 'Review')} for name, row in candidate_rows.items()},
        '9_evidence_effect_on_J_and_Review': {name: {state: row['state_xray'][state]
            for state in ('J', 'Review')} for name, row in evidence_rows.items()},
        '10_fixed_Kprev_results': {'fixed_exact': validity['checks'].get('Kprev_exact_all_four'),
            'fixed_panel_actions': actions, 'natural_Kprev_contrast': 'NOT_MEASURED',
            'change_relative_to_natural_Kprev': 'UNRESOLVED'},
        '11_correct_candidate_with_insufficient_evidence': _condition_public862(STATE862['conditions']['C1E0']),
        '12_UNKNOWN_candidate_with_sufficient_evidence': _condition_public862(STATE862['conditions']['C0E1']),
        '13_correct_candidate_with_sufficient_evidence': _condition_public862(STATE862['conditions']['C1E1']),
        '14_transfer_to_native_closed_loop': 'DIAGNOSTIC_ONLY; no native third cycle, MODEL_ACCEPT or MODEL_STOP is inferred.',
        '15_remaining_uncertainties_before_motor_revision': [
            'One task world; no population or statistical generalization.',
            'Fixed-Kprev panel does not estimate natural-Kprev effects.',
            'Teacher-forced scores are not calibrated action probabilities.',
            'State interaction does not localize a unique transformer circuit or semantic computation.',
            'Diagnostic factor sensitivity does not establish autonomous native correction or closure.']}
    result = {'dimensions': dimensions, 'dimension_scopes': scopes,
        'reported_classes': classes, 'causal_contrasts_valid': causal_valid,
        'factorial_conditions_valid': validity['valid'], 'controls_exact': controls_exact,
        'hypotheses': hypotheses, 'possibilities': possibilities,
        'required_answers': answers, 'native_closure_evidence': native_evidence,
        'diagnostic_aligned_conditions': aligned,
        'native_vs_diagnostic_separation': True,
        'candidate_vs_evidence_causality': 'SEPARATED_AT_MEASURED_OUTPUT_LEVEL' if causal_valid else
            'UNRESOLVED_INVALID_PANEL_OR_CONTROL_FAILURE',
        'not_a_definitive_semantic_or_circuit_diagnosis': True,
        'teacher_forced_scores_are_not_calibrated_probabilities': True,
        'diagnostic_continue_is_MODEL_ACCEPT': False, 'diagnostic_stop_is_MODEL_STOP': False,
        'mechanical_limit_EOS_UNKNOWN_are_MODEL_STOP': False}
    short862('TABLE M FINAL CAUSAL INTERPRETATION', json.dumps(result, ensure_ascii=False))
    return result


def run_analysis862(env):
    global ENV862
    ENV862 = env
    digest = records_digest861(env)
    STATE862['original_record_sha256'] = digest
    job = env['JOBS841'][1]
    snap = snapshots860(env)
    motor_map = motor_map861()
    reference860 = parse_reference860()
    reference861 = parse_reference861()
    native = native_sequences860(env)
    regression = native_regression861(env, native, reference860)
    native_evidence = native_closure862(env)
    # Unexpected native outcomes are recorded, never forced back to the TEST861 class.
    for record_job in env['JOBS841'][:2]:
        record = env['REC841'][record_job['job']]
        short862('TABLE B ORIGINAL NATIVE', record_job['job'], record['end'],
            [c['action'] for c in record['cycles']], 'native model stop=', record['model_stop'])
    short862('TABLE A GPU ENVIRONMENT', json.dumps(STATE859['environment']))
    conditions_list = resolve_conditions860(env)
    conditions = {row['condition']: row for row in conditions_list}
    prepare_e0_862(env, job, snap)
    prepare_evidence862(env, job, conditions['NOVEL_USEFUL_INFORMATION'], 'E1')
    prepare_evidence862(env, job, conditions['IRRELEVANT_INFORMATION'], 'EIRR')
    source_c0_862(env, job, snap)
    c1_generation = generate_c1_862(env, job, snap, reference861)
    for label, row in CANDIDATES862.items():
        short862('TABLE D CANDIDATE PROVENANCE', label, json.dumps(public_candidate862(row), ensure_ascii=False))
    for label, row in EVIDENCE862.items():
        short862('TABLE E EVIDENCE PROVENANCE', label, json.dumps(public_evidence862(row), ensure_ascii=False))
    fixed_kprev = snap['review1']['h']['rows']
    for arm, candidate, evidence in (
        ('C0E0', 'C0', 'E0'), ('C1E0', 'C1', 'E0'),
        ('C0E1', 'C0', 'E1'), ('C1E1', 'C1', 'E1')):
        run_condition862(env, arm, candidate, evidence, fixed_kprev, snap)
    for arm, candidate in (('C0EIRR', 'C0'), ('C1EIRR', 'C1')):
        run_condition862(env, arm, candidate, 'EIRR', fixed_kprev, snap)
    validity = panel_validity862(env, fixed_kprev)
    run_condition862(env, 'EXACT_RESTORE', 'C0', 'E0', fixed_kprev, snap,
        execution='DIAGNOSTIC_REPLAY')
    compare_control862(env, 'C0E0', 'EXACT_RESTORE', 'EXACT_RESTORE')
    run_condition862(env, 'SAME_STATE_REPLAY', 'C1', 'E1', fixed_kprev, snap,
        execution='DIAGNOSTIC_REPLAY')
    compare_control862(env, 'C1E1', 'SAME_STATE_REPLAY', 'SAME_STATE_REPLAY')
    effects = compute_effects862(env, validity['valid'])
    mechanism = final_interpretation862(env, native, validity, effects)
    assert records_digest861(env) == digest, 'DIAGNOSTICS_CHANGED_ORIGINAL_NATIVE_RECORDS'
    assert_hook_free859(env, 'post_TEST862_factorial_xray')
    assert not any(p.requires_grad for p in env['model'].parameters())
    condition_artifact = {'reference861': reference861, 'native_regression860': regression,
        'motor_map': motor_map, 'validity': validity,
        'conditions': {name: _condition_public862(STATE862['conditions'][name])
            for name in FACTOR_ARMS862 + NEGATIVE_ARMS862},
        'controls': STATE862['controls'],
        'native_original_jobs': native,
        'native_post_cycle1_reassessment': {'execution': 'NOT_SUPPORTED',
            'reason': 'Original REMOVED ends at MECHANICAL_REVIEW_LIMIT; no native post-cycle1 review exists.'},
        'native_autonomous_closure_observed': mechanism['dimensions']['G_NATIVE_AUTONOMOUS_CLOSURE_OBSERVED']}
    state_artifact = {'candidates': {k: public_candidate862(v) for k, v in CANDIDATES862.items()},
        'evidence': {k: public_evidence862(v) for k, v in EVIDENCE862.items()},
        'c1_generation': c1_generation,
        'panel_states': {name: STATE862['conditions'][name]['state'] for name in FACTOR_ARMS862},
        'source_destination_integrity': {name: STATE862['conditions'][name]['source_destination_integrity']
            for name in FACTOR_ARMS862 + NEGATIVE_ARMS862},
        'fixed_kprev': validity['fixed_kprev_state'],
        'E0_E1_difference_offline_only': {
            'E0_cards': EVIDENCE862['E0']['source_cards'],
            'E1_cards': EVIDENCE862['E1']['source_cards'],
            'added_cards': [x for x in EVIDENCE862['E1']['source_cards']
                if x not in EVIDENCE862['E0']['source_cards']],
            'E0_sufficient': EVIDENCE862['E0']['evidence_sufficient_offline'],
            'E1_sufficient': EVIDENCE862['E1']['evidence_sufficient_offline'],
            'E1_relation_semantics': EVIDENCE862['E1']['semantics_offline_only'],
            'E0_state': EVIDENCE862['E0']['E_summary'], 'E1_state': EVIDENCE862['E1']['E_summary'],
            'labels_entered_native_inputs': False},
        'large_tensors_written_to_disk': False}
    xray_artifact = {'conditions': {name: _condition_public862(STATE862['conditions'][name])
            for name in FACTOR_ARMS862 + NEGATIVE_ARMS862},
        'effects': effects, 'controls': STATE862['controls'], 'mechanism': mechanism,
        'diagnostic_assessments': STATE862['diagnostic_assessments'],
        'diagnostic_candidate_generations': STATE862['diagnostic_candidate_generations'],
        'native_jobs': 2, 'original_records_unchanged': True,
        'no_revision_after_factorial_review': True}
    json_write862('862_factorial_conditions.json', condition_artifact)
    json_write862('862_candidate_evidence_states.json', state_artifact)
    json_write862('862_factorial_effects.json', effects)
    json_write862('862_decision_xray.json', xray_artifact)
    analysis = {'status': 'TECHNICAL_XRAY_COMPLETE_RESULTS_NOT_PRESET',
        'native_jobs': 2, 'diagnostic_assessments': STATE862['diagnostic_assessments'],
        'diagnostic_candidate_generations': 1, 'validity': validity,
        'effects': effects, 'controls': STATE862['controls'], 'mechanism': mechanism,
        'native_regression860': regression, 'c1_generation_regression861': c1_generation['regression_to_861'],
        'original_records_unchanged': True,
        'native_autonomous_closure_observed': mechanism['dimensions']['G_NATIVE_AUTONOMOUS_CLOSURE_OBSERVED'],
        'scope': 'One world, fixed original review_1 Kprev, four diagnostic factorial conditions plus two irrelevant controls.'}
    STATE862['analysis'] = analysis
    return analysis


def write_partial862():
    if not (ROOT862 / '862_factorial_conditions.json').exists():
        json_write862('862_factorial_conditions.json', {'status': 'PARTIAL_OR_NOT_STARTED',
            'conditions': {k: _condition_public862(v) for k, v in STATE862['conditions'].items()}})
    if not (ROOT862 / '862_candidate_evidence_states.json').exists():
        json_write862('862_candidate_evidence_states.json', {'status': 'PARTIAL_OR_NOT_STARTED',
            'candidates': {k: public_candidate862(v) for k, v in CANDIDATES862.items()},
            'evidence': {k: public_evidence862(v) for k, v in EVIDENCE862.items()}})
    if not (ROOT862 / '862_factorial_effects.json').exists():
        json_write862('862_factorial_effects.json', STATE862['effects'] or
            {'status': 'PARTIAL_OR_NOT_STARTED'})
    if not (ROOT862 / '862_decision_xray.json').exists():
        json_write862('862_decision_xray.json', {'status': 'PARTIAL_OR_NOT_STARTED',
            'conditions': {k: _condition_public862(v) for k, v in STATE862['conditions'].items()},
            'controls': STATE862['controls']})


def finalize862(gates, execution):
    write_partial862()
    capture_cell_source862()
    source_path = ROOT862 / '862.py'
    source_present = source_path.is_file() and source_path.stat().st_size > 0
    source_sha = sha256_bytes862(source_path.read_bytes()) if source_present else None
    gates['GATE9_ARTIFACT_INTEGRITY'] = 'PASS' if source_present else 'FAIL'
    required = ('GATE0_SOURCE_INTEGRITY', 'GATE1_HOOKFREE_ORIGINAL_TWO_JOBS',
        'GATE2_OBSERVER_EQUIVALENCE', 'GATE3_NATIVE_861_REGRESSION_AND_C1_GENERATION',
        'GATE4_FACTORIAL_CONDITION_VALIDITY', 'GATE5_RESTORE_AND_SAME_STATE_REPLAY',
        'GATE9_ARTIFACT_INTEGRITY')
    technical = all(gates.get(k) == 'PASS' for k in required)
    mechanism = ANALYSIS862.get('mechanism', {})
    dimensions = mechanism.get('dimensions', {})
    classes = mechanism.get('reported_classes', ['UNRESOLVED'])
    report = {'test': TEST862_KIND, 'execution': execution, 'gates': gates,
        'technical_result': 'TECHNICAL_FACTORIAL_XRAY_PASS' if technical else
            'TECHNICAL_FACTORIAL_XRAY_NOT_PASSED',
        'scientific_result': classes if dimensions else 'UNRESOLVED',
        'behavioral_result': 'DIAGNOSTIC_GREEDY_ACTION_EFFECT_OBSERVED' if dimensions.get(
            'E_GREEDY_ACTION_EFFECT_OBSERVED') else 'DIAGNOSTIC_GREEDY_ACTION_EFFECT_NOT_DEMONSTRATED',
        'native_autonomous_closure_result': 'NATIVE_AUTONOMOUS_CLOSURE_OBSERVED' if dimensions.get(
            'G_NATIVE_AUTONOMOUS_CLOSURE_OBSERVED') else 'NATIVE_AUTONOMOUS_CLOSURE_NOT_OBSERVED',
        'candidate_main_effect': 'OBSERVED_DIAGNOSTIC_ONLY' if dimensions.get(
            'B_CANDIDATE_MAIN_EFFECT_OBSERVED') else 'NOT_DEMONSTRATED',
        'evidence_main_effect': 'OBSERVED_DIAGNOSTIC_ONLY' if dimensions.get(
            'C_EVIDENCE_MAIN_EFFECT_OBSERVED') else 'NOT_DEMONSTRATED',
        'candidate_evidence_interaction': 'OBSERVED_DIAGNOSTIC_ONLY' if dimensions.get(
            'D_CANDIDATE_EVIDENCE_INTERACTION_OBSERVED') else 'NOT_DEMONSTRATED',
        'negative_control_status': {arm: STATE862['conditions'].get(arm, {}).get('status', 'NOT_RUN')
            for arm in NEGATIVE_ARMS862},
        'partial_failures_not_hidden': [arm for arm in NEGATIVE_ARMS862
            if STATE862['conditions'].get(arm, {}).get('status') == 'NOT_APPLICABLE'],
        'original_error': EXECUTION_ERROR862, 'analysis_error': PROBE_ERROR862,
        'diagnostic_control_stop': DIAGNOSTIC_CONTROL_STOP862,
        'diagnostic_control_stop_is_model_stop': False,
        'technical_verification': TWO_JOB_VERIFICATION862, 'analysis': ANALYSIS862,
        'source_lock_count': len(RAW_SOURCES862),
        'dependency_audit': STATE862['dependency_audit'],
        'environment': STATE859['environment'], 'observer_equalities': STATE859['equalities'],
        'coverage_observer_equalities': [c['observer_equality'] for c in STATE859['coverage']],
        'source_capture': {'file': '862.py', 'present': source_present, 'sha256': source_sha},
        'seconds': time.perf_counter() - START862,
        'limitations': ['One world and deterministic contrasts; no population generalization.',
            'All four post-revision factorial conditions are diagnostic, not a native third cycle.',
            'Kprev is fixed to original review_1.rows; natural-Kprev contrast is not measured.',
            'C0E0 exact restore references the diagnostic C0E0 panel, not a nonexistent native post-cycle1 review.',
            'Teacher-forced scores are not calibrated action probabilities.',
            'Diagnostic CONTINUE/STOP are not MODEL_ACCEPT/MODEL_STOP.',
            'Mechanical review limit, EOS and UNKNOWN are not MODEL_STOP.',
            'Nonzero interaction is only an output-level factorial effect, not a unique semantic or circuit diagnosis.',
            'No motor revision, decision rule, memory architecture or autonomous closure is introduced.'],
        'TEST862_NEW_ENGINE': False, 'TEST862_MOTOR_REVISION': False,
        'TEST862_ANSWER_FIXED_BY_PYTHON': False, 'TEST862_MAX_REVIEWS_CHANGED': False,
        'TEST862_ORACLE_LABELS_ENTERED_NATIVE_INPUTS': False}
    json_write862('862_report.json', report)
    if TRACEBACK862:
        (ROOT862 / '862_traceback.txt').write_text(TRACEBACK862, encoding='utf-8')
    short862('TEST862 TECHNICAL', report['technical_result'])
    short862('TEST862 SCIENTIFIC', json.dumps(report['scientific_result'], ensure_ascii=False))
    short862('TEST862 BEHAVIORAL', report['behavioral_result'])
    short862('TEST862 NATIVE CLOSURE', report['native_autonomous_closure_result'])
    for name, status in gates.items():
        short862(name, status)
    short862('ARTIFACTS', ROOT862)
    LOG_FILE862.flush()
    manifest = {}
    for path in sorted(ROOT862.rglob('*')):
        if path.is_file() and path.name != '862_sha256_manifest.json':
            manifest[str(path.relative_to(ROOT862))] = {'bytes': path.stat().st_size,
                'sha256': sha256_bytes862(path.read_bytes())}
    json_write862('862_sha256_manifest.json', manifest)


try:
    short862('TEST862: candidate, evidence and interaction X-ray with fixed Kprev.')
    short862('GPU EXECUTION: NOT VERIFIED BY AUTHOR; restart Colab before this cell.')
    load_sources862()
    load_spine862()
    parse_reference861()
    gate0 = 'PASS'
    env862, error862, trace862, evidence862 = reproduce_pre859859()
    EXECUTION_ERROR862, TRACEBACK862, ERROR_EVIDENCE862 = error862, trace862, evidence862
    if trace862:
        short862(trace862[-12000:])
    if 'GATE1_TWO_JOB_OBSERVATION_COMPLETE' in trace862:
        DIAGNOSTIC_CONTROL_STOP862 = 'GATE1_TWO_JOB_OBSERVATION_COMPLETE'
    try:
        TWO_JOB_VERIFICATION862 = verify_two_job859(env862, trace862)
        EXECUTION_ERROR862 = None
        gate1 = gate2 = 'PASS'
    except Exception as exc:
        EXECUTION_ERROR862 = type(exc).__name__ + ': ' + str(exc)
        gate1 = gate2 = 'BLOCKED'
        short862(traceback.format_exc())
    if gate1 == 'PASS':
        try:
            install_offline_evaluator859(env862)
            ANALYSIS862 = run_analysis862(env862)
            dims = ANALYSIS862['mechanism']['dimensions']
            gate3 = 'PASS'
            gate4 = 'PASS' if ANALYSIS862['validity']['valid'] else 'FAIL'
            gate5 = 'PASS' if ANALYSIS862['mechanism']['controls_exact'] else 'FAIL'
            execution = 'CANDIDATE_EVIDENCE_FACTORIAL_XRAY_COMPLETE'
        except BaseException as exc:
            PROBE_ERROR862 = type(exc).__name__ + ': ' + str(exc)
            TRACEBACK862 += '\n===== TEST862 ANALYSIS FAILURE =====\n' + traceback.format_exc()
            short862(traceback.format_exc())
            gate3 = gate4 = gate5 = 'BLOCKED'
            dims = {}
            execution = 'ANALYSIS_INCOMPLETE_FULL_TRACEBACK_IN_LOG'
    else:
        gate3 = gate4 = gate5 = 'BLOCKED'
        dims = {}
        execution = 'TWO_JOB_TECHNICAL_VERIFICATION_FAILED'
    gates = {'GATE0_SOURCE_INTEGRITY': gate0,
        'GATE1_HOOKFREE_ORIGINAL_TWO_JOBS': gate1,
        'GATE2_OBSERVER_EQUIVALENCE': gate2,
        'GATE3_NATIVE_861_REGRESSION_AND_C1_GENERATION': gate3,
        'GATE4_FACTORIAL_CONDITION_VALIDITY': gate4,
        'GATE5_RESTORE_AND_SAME_STATE_REPLAY': gate5,
        'GATE6_CANDIDATE_MAIN_EFFECT': 'OBSERVED_DIAGNOSTIC_ONLY' if dims.get(
            'B_CANDIDATE_MAIN_EFFECT_OBSERVED') else 'NOT_DEMONSTRATED',
        'GATE7_EVIDENCE_MAIN_EFFECT': 'OBSERVED_DIAGNOSTIC_ONLY' if dims.get(
            'C_EVIDENCE_MAIN_EFFECT_OBSERVED') else 'NOT_DEMONSTRATED',
        'GATE8_CANDIDATE_EVIDENCE_INTERACTION': 'OBSERVED_DIAGNOSTIC_ONLY' if dims.get(
            'D_CANDIDATE_EVIDENCE_INTERACTION_OBSERVED') else 'NOT_DEMONSTRATED',
        'GATE9_ARTIFACT_INTEGRITY': 'PASS'}
    finalize862(gates, execution)
except BaseException as exc:
    EXECUTION_ERROR862 = type(exc).__name__ + ': ' + str(exc)
    TRACEBACK862 += '\n===== TEST862 OUTER FAILURE =====\n' + traceback.format_exc()
    sys.stdout, sys.stderr = CONSOLE862, ERROR_CONSOLE862
    short862(traceback.format_exc())
    gates = {'GATE0_SOURCE_INTEGRITY': 'PASS' if len(RAW_SOURCES862) == 25 else 'FAIL',
        'GATE1_HOOKFREE_ORIGINAL_TWO_JOBS': 'BLOCKED', 'GATE2_OBSERVER_EQUIVALENCE': 'BLOCKED',
        'GATE3_NATIVE_861_REGRESSION_AND_C1_GENERATION': 'BLOCKED',
        'GATE4_FACTORIAL_CONDITION_VALIDITY': 'BLOCKED',
        'GATE5_RESTORE_AND_SAME_STATE_REPLAY': 'BLOCKED',
        'GATE6_CANDIDATE_MAIN_EFFECT': 'BLOCKED', 'GATE7_EVIDENCE_MAIN_EFFECT': 'BLOCKED',
        'GATE8_CANDIDATE_EVIDENCE_INTERACTION': 'BLOCKED', 'GATE9_ARTIFACT_INTEGRITY': 'PASS'}
    finalize862(gates, 'TEST862_FAILURE_FULL_TRACEBACK_IN_LOG')
finally:
    LOG_FILE862.close()
