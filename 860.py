# AKBASCORE SILICON HIPPOCAMPUS — TEST860 NATIVE INFORMATION-GAIN X-RAY
# Locked TEST859 spine; two unchanged original jobs and matched post-hoc replays.
# Information labels are independent offline semantics, never native model inputs.
# Valid panel: NO_NEW, REDUNDANT, NOVEL_USEFUL, IRRELEVANT. CONTRADICTORY is NA:
# the locked REMOVED predecessor has UNKNOWN and no prior endpoint to contradict.
# Diagnostic actions/revisions are never original closed-loop outcomes or STOP claims.
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
import sys
import time
import traceback
import urllib.request
import zipfile

TEST860_KIND = 'NATIVE_INFORMATION_GAIN_XRAY'
CODELOAD860 = 'https://codeload.github.com/ceceli33/titan-cognitive-core-v3/zip/refs/heads/main'
LOCKS860 = {
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
}
STATE_REL_L2_EPS860 = 1e-7
SCORE_ABS_EPS860 = 1e-6
STATE_ORDER860 = ('C', 'E', 'U', 'R', 'Kprev', 'K0', 'J', 'Review')
PREdecision_STAGES860 = ('E', 'U', 'R', 'K0', 'J', 'Review')
CONDITION_PLAN860 = [
    {'condition': 'NO_NEW_INFORMATION', 'added_roles': [],
     'expected': 'NO_NEW_UNIQUE_RELATION_OR_ENDPOINT',
     'execution': 'ORIGINAL_NATIVE', 'control_role': 'REFERENCE'},
    {'condition': 'REDUNDANT_INFORMATION', 'added_roles': ['first'],
     'expected': 'EXISTING_FIRST_RELATION_REPEATED_BY_EXISTING_PHYSICAL_CARTRIDGE',
     'execution': 'DIAGNOSTIC_REPLAY', 'control_role': 'REDUNDANT_NEGATIVE_CONTROL'},
    {'condition': 'NOVEL_USEFUL_INFORMATION', 'added_roles': ['second'],
     'expected': 'NEW_SECOND_RELATION_CREATES_SUPPORTED_TWO_HOP_ENDPOINT',
     'execution': 'DIAGNOSTIC_REPLAY', 'control_role': 'PRIMARY_INFORMATION_CONDITION'},
    {'condition': 'CONTRADICTORY_INFORMATION', 'added_roles': [],
     'expected': 'NOT_APPLICABLE_NO_PRIOR_SUPPORTED_ENDPOINT_IN_LOCKED_REMOVED_BASELINE',
     'execution': 'NOT_APPLICABLE', 'control_role': 'NOT_FABRICATED'},
    {'condition': 'IRRELEVANT_INFORMATION', 'added_roles': ['decoy'],
     'expected': 'NEW_DECOY_RELATION_ADDS_NO_TWO_HOP_ENDPOINT',
     'execution': 'DIAGNOSTIC_REPLAY', 'control_role': 'IRRELEVANT_NEGATIVE_CONTROL'},
]
COMPARISON_PLAN860 = (
    ('NOVEL_VS_REDUNDANT', 'NOVEL_USEFUL_INFORMATION', 'REDUNDANT_INFORMATION'),
    ('NOVEL_VS_IRRELEVANT', 'NOVEL_USEFUL_INFORMATION', 'IRRELEVANT_INFORMATION'),
    ('NOVEL_VS_NO_NEW', 'NOVEL_USEFUL_INFORMATION', 'NO_NEW_INFORMATION'),
    ('REDUNDANT_VS_NO_NEW', 'REDUNDANT_INFORMATION', 'NO_NEW_INFORMATION'),
    ('IRRELEVANT_VS_NO_NEW', 'IRRELEVANT_INFORMATION', 'NO_NEW_INFORMATION'),
)
STAMP860 = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
ROOT860 = pathlib.Path('/content') / ('TEST860_INFORMATION_XRAY_' + STAMP860)
ROOT860.mkdir(parents=True, exist_ok=False)
CONSOLE860 = sys.stdout
ERROR_CONSOLE860 = sys.stderr
LOG_FILE860 = open(ROOT860 / '860.log', 'w', encoding='utf-8')
START860 = time.perf_counter()
REAL_COMPILE860 = builtins.compile
RAW_SOURCES860 = {}
STATE860 = {
    'spine_loaded': False, 'spine_json': {}, 'conditions': copy.deepcopy(CONDITION_PLAN860),
    'native_sequences': {}, 'condition_results': {}, 'comparisons': [],
    'analysis': {}, 'original_record_sha256': None,
}
EXECUTION_ERROR860 = None
PROBE_ERROR860 = None
TRACEBACK860 = ''
ERROR_EVIDENCE860 = {}
TWO_JOB_VERIFICATION860 = {}
ANALYSIS860 = {}
DIAGNOSTIC_STOP860 = None

# TEST859 compatibility bindings. Only selected AST definitions are loaded later;
# its top-level experiment and finalizer are never executed.
ROOT859 = ROOT860
LOG_FILE859 = LOG_FILE860
START859 = START860
CONSOLE859 = CONSOLE860
ERROR_CONSOLE859 = ERROR_CONSOLE860
REAL_COMPILE859 = REAL_COMPILE860
RAW_SOURCES859 = RAW_SOURCES860
STATE859 = {
    'installed': False, 'compiled': False, 'equalities': [], 'observations': [],
    'coverage': [], 'frames': [], 'g': None, 'active': None, 'capture': None,
    'tokenizations': {}, 'hook_audits': [], 'saved_jobs': [], 'invocations': [],
    'contexts': [], 'transitions': {}, 'offline_functions': {},
    'decision_comparison': {}, 'causal_probes': [], 'original_record_sha256': None,
    'environment': {}, 'start': START860,
}
FAILURES859 = []
LAST_CONTEXT859 = None
SPELLINGS859 = (' CONTINUE', ' REVISE', ' STOP', ' SUFFICIENT', ' INSUFFICIENT')


def short860(*args):
    text = ' '.join(str(x) for x in args)
    print(text, file=CONSOLE860, flush=True)
    LOG_FILE860.write(text + '\n')
    LOG_FILE860.flush()


def short859(*args):
    short860(*args)


def json_write860(name, value):
    path = ROOT860 / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
        allow_nan=False), encoding='utf-8')
    return path


def json_write859(name, value):
    # The inherited observer's auxiliary JSON remains in memory. TEST860 writes
    # only its requested reports; no legacy 859_* output files are produced.
    STATE860['spine_json'][name] = copy.deepcopy(value)
    return ROOT860 / name


def sha256_bytes860(data):
    return hashlib.sha256(data).hexdigest()


def git_blob860(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def load_sources860():
    request = urllib.request.Request(CODELOAD860,
        headers={'User-Agent': 'AKBASCORE-TEST860-GATE0'})
    with urllib.request.urlopen(request, timeout=240) as response:
        archive = response.read(100000001)
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        for name, expected in LOCKS860.items():
            matches = [member for member in zipped.namelist()
                if member.endswith('/' + name)]
            assert len(matches) == 1, ('SOURCE_MEMBER_NOT_UNIQUE', name, matches)
            data = zipped.read(matches[0])
            actual = git_blob860(data)
            assert actual == expected, ('SOURCE_LOCK_FAILED', name, actual, expected)
            RAW_SOURCES860[name] = data
            if name.endswith('.py'):
                REAL_COMPILE860(data.decode('utf-8'), name, 'exec')
            short860('GATE0 SOURCE', name, actual, 'PASS')
    assert len(RAW_SOURCES860) == 21


def capture_cell_source860():
    try:
        shell = get_ipython()  # noqa: F821 — supplied by Colab/IPython.
        history = list(shell.history_manager.input_hist_raw)
        marker = 'AKBASCORE SILICON HIPPOCAMPUS — TEST860 NATIVE INFORMATION-GAIN X-RAY'
        candidates = [text for text in history if marker in text]
        if candidates:
            (ROOT860 / '860.py').write_text(candidates[-1], encoding='utf-8')
            return True
    except Exception as exc:
        short860('860.py history capture unavailable:', type(exc).__name__, str(exc))
    return False


def load_spine860():
    assert not STATE860['spine_loaded']
    tree = ast.parse(RAW_SOURCES860['859.py'].decode('utf-8'), filename='859.py')
    names = {
        'current_job859', 'segment_metadata859', 'runtime_context859',
        'hook_audit859', 'assert_hook_free859', 'capture859', 'clone_observer859',
        'install859', 'compile_xray859', 'recover_inherited_error859',
        'reproduce_pre859859', 'records_digest859', 'verify_two_job859',
        'clone_segments859', 'segment_map859', 'native_h_equal859', 'h_summary859',
        'score_actions859', 'score_margins859', 'find_invocation859',
        'state_metrics859', 'paired_metrics859', 'continuity_for_slot859',
        'install_offline_evaluator859', 'evidence_context859', 'original_quality859', 'transport859',
    }
    nodes = [n for n in tree.body if
        (isinstance(n, ast.FunctionDef) and n.name in names) or
        (isinstance(n, ast.ClassDef) and n.name in ('Gate1SmokeComplete859', 'Quiet859'))]
    assert {n.name for n in nodes} == names | {'Gate1SmokeComplete859', 'Quiet859'}
    module = ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[]))
    REAL_COMPILE860(module, 'TEST860_REUSED_TEST859_DEFINITIONS_ONLY', 'exec')
    exec(REAL_COMPILE860(module, 'TEST860_REUSED_TEST859_DEFINITIONS_ONLY', 'exec'), globals())
    STATE860['spine_loaded'] = True
    STATE860['spine_ast_sha256'] = sha256_bytes860(
        ast.dump(module, include_attributes=False).encode())
    short860('TEST859 SPINE: selected definitions only; AST-SHA256',
        STATE860['spine_ast_sha256'], 'top-level exec=0')


def records_digest860(env):
    return records_digest859(env)


def margins860(scores):
    by_name = {s['spelling'].strip(): s for s in scores}
    out = score_margins859(scores)
    out.update({
        'continue_minus_revise_sequence_logp':
            by_name['CONTINUE']['sequence_logp'] - by_name['REVISE']['sequence_logp'],
        'continue_minus_revise_first_token_logit':
            by_name['CONTINUE']['first_token_logit'] - by_name['REVISE']['first_token_logit'],
        'stop_minus_continue_first_token_logit':
            by_name['STOP']['first_token_logit'] - by_name['CONTINUE']['first_token_logit'],
    })
    return out


def relation_roles860(world):
    return {
        'first': (world['start'], world['middle']),
        'second': (world['middle'], world['end']),
        'changed': (world['middle'], world['changed_end']),
        'decoy': (world['decoy_end'], world['start']),
        'fork': (world['start'], world['fork_end']),
    }


def endpoints860(roles, world):
    roles = set(roles)
    answerable = []
    if 'first' in roles and 'second' in roles:
        answerable.append('end')
    if 'first' in roles and 'changed' in roles:
        answerable.append('changed_end')
    return sorted(answerable)


def resolve_conditions860(env):
    jobs = env['JOBS841'][:2]
    assert [j['intervention'] for j in jobs] == ['INTACT', 'REMOVED']
    job = jobs[1]
    record = env['REC841'][job['job']]
    wi = env['QID841'].index(job['qid'])
    world = env['worlds829'][wi]
    ids = world['ids']
    base_roles = ['first', 'fork']
    base_cards = [ids[r] for r in base_roles]
    assert list(record['mounted_cards']) == base_cards, 'LOCKED_REMOVED_MOUNT_CHANGED'
    assert len(record['cycles']) == 2
    relations = relation_roles860(world)
    for role, (a, b) in relations.items():
        cid = ids[role]
        assert cid in env['entries'] and cid in env['cards829']
        expected = ('Evidence record. Domain: ' + world['world'] + '\n' +
            'Directed relation: ' + a + ' -> ' + b + '.\n')
        assert env['cards829'][cid] == expected, ('CARD_SEMANTIC_LOCK_FAILED', role)
    resolved = []
    for planned in CONDITION_PLAN860:
        row = copy.deepcopy(planned)
        row.update({'job': job['job'], 'qid': job['qid'], 'world': world['world']})
        if row['execution'] == 'NOT_APPLICABLE':
            row.update({'validity': 'NOT_APPLICABLE', 'source_cards': [],
                'reason': 'Prior candidate is not a supported endpoint and prior first+fork evidence has no two-hop endpoint; adding changed would be alternative useful evidence, not a matched contradiction.'})
            resolved.append(row)
            continue
        roles = base_roles + row['added_roles']
        cards = [ids[r] for r in roles]
        before_relations = {relations[r] for r in base_roles}
        after_relations = {relations[r] for r in roles}
        before_endpoints = endpoints860(base_roles, world)
        after_endpoints = endpoints860(roles, world)
        new_relations = sorted(after_relations - before_relations)
        new_endpoints = sorted(set(after_endpoints) - set(before_endpoints))
        name = row['condition']
        semantics = {
            'base_roles': base_roles, 'all_role_occurrences': roles,
            'source_cards': cards, 'new_unique_relation_count': len(new_relations),
            'new_endpoints': new_endpoints,
            'prior_endpoints': before_endpoints, 'resulting_endpoints': after_endpoints,
            'new_information': bool(new_relations),
            'task_useful_information': bool(new_endpoints),
            'redundant_information': bool(row['added_roles']) and not new_relations,
            'irrelevant_information': bool(new_relations) and not new_endpoints,
            'contradiction': False,
            'labels_are_offline_only': True,
        }
        valid = {
            'NO_NEW_INFORMATION': not new_relations and not new_endpoints,
            'REDUNDANT_INFORMATION': semantics['redundant_information'],
            'NOVEL_USEFUL_INFORMATION': semantics['new_information'] and semantics['task_useful_information'],
            'IRRELEVANT_INFORMATION': semantics['irrelevant_information'],
        }[name]
        assert valid, ('PREREGISTERED_INFORMATION_SEMANTICS_FAILED', name, semantics)
        assert all(c in env['entries'] for c in cards)
        if name != 'REDUNDANT_INFORMATION':
            assert len(cards) == len(set(cards))
        else:
            assert cards[-1] == cards[0] and len(cards) == len(set(cards)) + 1
        row.update({'validity': 'VALID', 'source_cards': cards,
            'source_cartridge_ids_offline_only': True, 'semantics': semantics,
            'matching': 'Same original cycle0, revision_0 C and review_0 Kprev; only physical mount differs.'})
        resolved.append(row)
    STATE860['conditions'] = resolved
    for row in resolved:
        short860('TABLE A CONDITION', row['condition'], row['execution'], row['validity'],
            row.get('source_cards', []), row.get('control_role'))
    return resolved


def native_sequences860(env):
    output = {}
    for job in env['JOBS841'][:2]:
        record = env['REC841'][job['job']]
        quality = original_quality859(env, job, record)
        cycles = []
        for cycle in record['cycles']:
            invocation = find_invocation859(job['job'], 'review_%d' % cycle['cycle'])
            scores = score_actions859(env, invocation['memx'], list(invocation['pre']),
                clone_segments859(invocation['segments']), list(invocation['post']))
            cycles.append({'cycle': cycle['cycle'], 'candidate': cycle['candidate']['text'],
                'action': cycle['action'], 'review_text': cycle['review']['text'],
                'revision': None if cycle.get('revision') is None else cycle['revision']['text'],
                'scores': scores, 'margins': margins860(scores)})
        output[job['job']] = {'condition': job['intervention'], 'execution': 'ORIGINAL_NATIVE',
            'action_provenance': 'ORIGINAL_NATIVE_REVIEW',
            'score_provenance': 'POST_HOC_TEACHER_FORCED_ON_ORIGINAL_INVOCATION_NOT_CALIBRATED_PROBABILITY',
            'initial': record['initial']['text'], 'cycles': cycles,
            'final_answer': None if record.get('answer') is None else record['answer']['text'],
            'end': record['end'], 'model_stop': record['end'] == 'MODEL_STOP',
            'mechanical_limit': record['end'] == 'MECHANICAL_REVIEW_LIMIT',
            'seconds': record.get('seconds'), 'peak_gpu_gib': record.get('peak_gpu_gib'),
            'quality': quality}
        short860('TABLE B NATIVE', job['intervention'], output[job['job']]['initial'],
            [(c['action'], c['revision']) for c in cycles],
            output[job['job']]['final_answer'], record['end'])
    STATE860['native_sequences'] = output
    return output


def decision_quality860(env, job, action, candidate, revision, mounted):
    wi = env['QID841'].index(job['qid'])
    world = env['worlds829'][wi]
    mounted = set(mounted)
    ids = world['ids']
    sufficient = ids['first'] in mounted and bool({ids['second'], ids['changed']} & mounted)
    answer = candidate if action == 'CONTINUE' else None
    grounded = env['supported851'](answer, world, mounted)
    revision_grounded = (None if revision is None else
        env['supported851'](revision, world, mounted))
    unsupported = bool(answer is not None and answer.strip() and
        env['node851'](answer, world) != 'UNKNOWN' and not grounded)
    metrics = {
        'grounded_answer': grounded,
        'unsupported_answer_avoided': not unsupported,
        'task_progress': bool(grounded or revision_grounded),
        'false_stop_avoided': not (action == 'STOP' and sufficient),
    }
    if revision is not None:
        metrics['revision_grounded'] = revision_grounded
    if not sufficient:
        metrics['correct_stop'] = action == 'STOP'
        metrics['unknown_when_insufficient'] = bool(
            (revision and revision.strip().upper() == 'UNKNOWN') or
            (answer and answer.strip().upper() == 'UNKNOWN'))
    return {'action': action, 'candidate': candidate, 'answer': answer,
        'revision': revision, 'sufficient': sufficient, 'grounded': grounded,
        'unsupported_completion': unsupported, 'false_stop': action == 'STOP' and sufficient,
        'diagnostic_stop_action': action == 'STOP', 'native_model_stop': False,
        'quality_metrics': metrics}


def quality_dominance860(reference, value):
    a, b = reference['quality_metrics'], value['quality_metrics']
    common = sorted(k for k in set(a) & set(b) if a[k] is not None and b[k] is not None)
    assert common, 'NO_COMMON_OFFLINE_QUALITY_METRIC'
    better = [k for k in common if bool(a[k]) > bool(b[k])]
    worse = [k for k in common if bool(a[k]) < bool(b[k])]
    return {'common_metrics': common, 'reference_better': better,
        'reference_worse': worse, 'reference_dominates': bool(better) and not worse}


def snapshots860(env):
    job = env['JOBS841'][1]['job']
    return {name: find_invocation859(job, stage) for name, stage in (
        ('pre0', 'precontrol_0'), ('review0', 'review_0'), ('revision0', 'revision_0'),
        ('pre1', 'precontrol_1'), ('review1', 'review_1'), ('revision1', 'revision_1'))}


def original_condition860(env, condition, native_sequences):
    job = env['JOBS841'][1]
    record = env['REC841'][job['job']]
    snap = snapshots860(env)
    pm = segment_map859(env, snap['pre1']['segments'])
    dm = segment_map859(env, snap['review1']['segments'])
    cycle = record['cycles'][1]
    scores = native_sequences[job['job']]['cycles'][1]['scores']
    revision = snap['revision1']['h']
    state = {k: state_metrics859(env, rows) for k, rows in (
        ('C', pm['C'][1]), ('E', pm['E'][1]), ('U', pm['U'][1]),
        ('R', pm['R'][1]), ('Kprev', pm['Kprev'][1]),
        ('K0', snap['pre1']['h']['rows']), ('J', dm['J'][1]),
        ('Review', snap['review1']['h']['rows']))}
    return {'condition': condition['condition'], 'execution': 'ORIGINAL_NATIVE',
        'source_cards': list(record['mounted_cards']), 'state': state,
        'evidence_text': cycle['evidence']['text'],
        'coverage_text': cycle['coverage_native']['text'],
        'review': h_summary859(env, snap['review1']['h']),
        'revision': h_summary859(env, revision),
        'greedy_action': cycle['action'], 'scores': scores, 'margins': margins860(scores),
        'quality': decision_quality860(env, job, cycle['action'],
            cycle['candidate']['text'], revision['text'], record['mounted_cards']),
        'diagnostic_stop_action': False, 'native_model_stop': record['end'] == 'MODEL_STOP',
        'seconds': record.get('seconds'), 'peak_gpu_gib': record.get('peak_gpu_gib'),
        'C_source': 'original revision_0.rows', 'Kprev_source': 'original review_0.rows'}


def run_diagnostic860(env, condition, original, restore=False):
    torch = env['torch']
    job = env['JOBS841'][1]
    record = env['REC841'][job['job']]
    snap = snapshots860(env)
    C = snap['revision0']['h']['rows'].clone()
    Kprev = snap['review0']['h']['rows'].clone()
    cards = list(record['mounted_cards']) if restore else list(condition['source_cards'])
    memx, temporary, mount_ms = (snap['pre1']['memx'], False, 0.0) if restore else \
        env['mem_for841'](cards, 'TEST860_' + condition['condition'])
    begun = time.perf_counter()
    torch.cuda.synchronize()
    torch.cuda.reset_peak_memory_stats()
    seal_before = env['seal834'](memx)
    try:
        evidence_pre = list(env['prompt_ids'](env['EVIDENCE851'].format(q=env['QTEXT841'][job['qid']])))
        coverage_pre = list(env['prompt_ids'](env['COVERAGE852'].format(q=env['QTEXT841'][job['qid']])))
        evidence = env['gen849'](memx, evidence_pre, None, env['ANSWER_SUFFIX851'])
        coverage = env['gen849'](memx, coverage_pre, None, env['COVERAGE_SUFFIX852'])
        E, U = evidence['rows'], coverage['rows']
        R = env['relation852'](C, E)
        pre = list(snap['pre1']['pre'])
        post = list(snap['pre1']['post'])
        segments = [(list(env['C_SLOT851']), C), (list(env['E_SLOT851']), E),
            (list(env['K_SLOT851']), Kprev), (list(env['U_SLOT852']), U),
            (list(env['R_SLOT852']), R)]
        K0_h = env['gen851'](memx, pre, segments, post)
        J = env['interaction854'](C, E, K0_h['rows'])
        decision = [(list(env['K_SLOT854']), K0_h['rows']),
                    (list(env['J_SLOT854']), J)]
        review = env['gen851'](memx, list(snap['review1']['pre']), decision,
            list(snap['review1']['post']))
        scores = score_actions859(env, memx, list(snap['review1']['pre']), decision,
            list(snap['review1']['post']))
        action = env['parse849'](review['text'])
        assert action != 'INVALID', 'DIAGNOSTIC_INVALID_IS_NOT_STOP_OR_UNKNOWN'
        revision = None
        if action == 'REVISE':
            recompute = list(env['prompt_ids'](env['RECOMPUTE851'].format(
                q=env['QTEXT841'][job['qid']])))
            revision = env['gen851'](memx, recompute,
                [(list(env['C_SLOT851']), C), (list(env['K_SLOT851']), review['rows']),
                 (list(env['E_SLOT851']), E), (list(env['U_SLOT852']), U),
                 (list(env['R_SLOT852']), R)], list(env['ANSWER_SUFFIX851']))
        for h in (evidence, coverage, K0_h, review) + (() if revision is None else (revision,)):
            assert h['trace849']['continuity']['exact_after_bf16'], 'BF16_CONTINUITY_FAILED'
        assert_hook_free859(env, 'TEST860_' + ('restore' if restore else condition['condition']))
        assert env['seal834'](memx) == seal_before, 'DIAGNOSTIC_MEMORY_CHANGED'
        state_rows = {'C': C, 'E': E, 'U': U, 'R': R, 'Kprev': Kprev,
            'K0': K0_h['rows'], 'J': J, 'Review': review['rows']}
        state = {k: state_metrics859(env, rows) for k, rows in state_rows.items()}
        if not restore:
            # Small CPU FP32 states remain in memory only for matched comparisons.
            DIAGNOSTIC_RUNTIME860[condition['condition']] = state_rows
        revision_text = None if revision is None else revision['text']
        result = {'condition': condition['condition'],
            'execution': 'DIAGNOSTIC_RESTORE' if restore else 'DIAGNOSTIC_REPLAY',
            'source_cards': cards, 'state': state,
            'evidence_text': evidence['text'], 'coverage_text': coverage['text'],
            'review': h_summary859(env, review),
            'revision': None if revision is None else h_summary859(env, revision),
            'greedy_action': action, 'scores': scores, 'margins': margins860(scores),
            'quality': decision_quality860(env, job, action,
                snap['revision0']['h']['text'], revision_text, cards),
            'diagnostic_stop_action': action == 'STOP', 'native_model_stop': False,
            'C_source_sha256': state_metrics859(env, C)['sha256'],
            'Kprev_source_sha256': state_metrics859(env, Kprev)['sha256'],
            'mount_ms': mount_ms}
        if restore:
            original_pre_rows = segment_map859(env, snap['pre1']['segments'])
            assert torch.equal(E, original_pre_rows['E'][1]) and torch.equal(U, original_pre_rows['U'][1])
            assert native_h_equal859(torch, K0_h, snap['pre1']['h']), 'RESTORE_K0_NOT_EXACT'
            assert native_h_equal859(torch, review, snap['review1']['h']), 'RESTORE_REVIEW_NOT_EXACT'
            assert revision is not None and native_h_equal859(torch, revision, snap['revision1']['h']), 'RESTORE_REVISION_NOT_EXACT'
            assert scores == original['scores'], 'RESTORE_ACTION_SCORES_NOT_EXACT'
            result['restore_exact'] = True
        result['seconds'] = time.perf_counter() - begun
        result['peak_gpu_gib'] = torch.cuda.max_memory_allocated() / 1024 ** 3
        short860('TABLE D CONDITION', result['execution'], condition['condition'],
            action, revision_text, result['margins'], 'seconds', result['seconds'],
            'peak_gib', result['peak_gpu_gib'])
        return result
    finally:
        if temporary:
            del memx
            gc.collect()
            env['release']()


def effective_state_difference860(diff):
    if diff['exact']:
        return False
    if diff['status'] == 'NOT_COMPARABLE_SHAPE':
        return True
    value = diff.get('relative_l2')
    return value is not None and value > STATE_REL_L2_EPS860


def compare_runtime860(env, name, reference, control, runtime_states):
    states = {}
    for stage in STATE_ORDER860:
        diff = paired_metrics859(env, runtime_states[reference['condition']][stage],
            runtime_states[control['condition']][stage])
        diff['significant'] = effective_state_difference860(diff)
        diff['reference_norm'] = reference['state'][stage]['norm']
        diff['control_norm'] = control['state'][stage]['norm']
        diff['norm_delta_reference_minus_control'] = (
            None if diff['reference_norm'] is None or diff['control_norm'] is None else
            diff['reference_norm'] - diff['control_norm'])
        states[stage] = diff
    score_delta = score_deltas860(reference['scores'], control['scores'])
    score_effect = any(abs(x['sequence_logp_delta']) > SCORE_ABS_EPS860
        for x in score_delta.values())
    numerical = any(x['significant'] for x in states.values()) or score_effect
    action_changed = reference['greedy_action'] != control['greedy_action']
    ref_revision = None if reference.get('revision') is None else reference['revision']['text']
    ctl_revision = None if control.get('revision') is None else control['revision']['text']
    revision_changed = ref_revision != ctl_revision
    dominance = quality_dominance860(reference['quality'], control['quality'])
    evidence_aligned = (action_changed or revision_changed) and dominance['reference_dominates']
    decision_sensitive = score_effect or action_changed or revision_changed
    dimensions = {
        'A_NO_DETECTABLE_NUMERICAL_DIFFERENCE': not numerical,
        'B_NUMERICAL_DIFFERENCE_ONLY': numerical and not decision_sensitive,
        'C_INFORMATION_CONDITION_DISCRIMINATION': False,
        'D_DECISION_SENSITIVITY': decision_sensitive,
        'E_EVIDENCE_ALIGNED_DECISION_EFFECT': evidence_aligned,
        'score_effect': score_effect, 'greedy_action_changed': action_changed,
        'revision_text_changed': revision_changed,
    }
    label = ('E_EVIDENCE_ALIGNED_DECISION_EFFECT' if evidence_aligned else
        'D_DECISION_SENSITIVITY' if dimensions['D_DECISION_SENSITIVITY'] else
        'B_NUMERICAL_DIFFERENCE_ONLY' if numerical else 'A_NO_DETECTABLE_NUMERICAL_DIFFERENCE')
    row = {'comparison': name, 'reference': reference['condition'],
        'control': control['condition'],
        'execution': 'MATCHED_POST_HOC_COMPARISON',
        'causal_scope': 'Diagnostic physical-mount intervention only; not an original closed-loop outcome.',
        'states': states, 'score_deltas': score_delta,
        'reference_action': reference['greedy_action'], 'control_action': control['greedy_action'],
        'reference_revision': ref_revision, 'control_revision': ctl_revision,
        'quality_dominance': dominance, 'dimensions': dimensions, 'class': label,
        'significant_stages': [s for s in STATE_ORDER860 if states[s]['significant']]}
    short860('TABLE F COMPARISON', name, label, row['significant_stages'],
        'score_effect', score_effect, 'greedy_changed', action_changed,
        'revision_changed', revision_changed, 'evidence_aligned', evidence_aligned)
    return row


def score_deltas860(reference, value):
    ref = {x['spelling'].strip(): x for x in reference}
    val = {x['spelling'].strip(): x for x in value}
    return {name: {
        'sequence_logp_delta': val[name]['sequence_logp'] - ref[name]['sequence_logp'],
        'mean_token_logp_delta': val[name]['mean_token_logp'] - ref[name]['mean_token_logp'],
        'first_token_logit_delta': val[name]['first_token_logit'] - ref[name]['first_token_logit']}
        for name in ('CONTINUE', 'REVISE', 'STOP')}


def information_discrimination860(comparisons):
    primary = [r for r in comparisons if r['comparison'] in
        ('NOVEL_VS_REDUNDANT', 'NOVEL_VS_IRRELEVANT')]
    assert len(primary) == 2
    common = set(PREdecision_STAGES860)
    for row in primary:
        common &= {s for s, d in row['states'].items() if d['significant']}
    signature = []
    for stage in sorted(common, key=PREdecision_STAGES860.index):
        signs = []
        for row in primary:
            delta = row['states'][stage]['norm_delta_reference_minus_control']
            signs.append(0 if delta is None or abs(delta) <= 1e-12 else (1 if delta > 0 else -1))
        if signs[0] != 0 and signs[0] == signs[1]:
            signature.append(stage)
    found = bool(signature)
    for row in primary:
        row['dimensions']['C_INFORMATION_CONDITION_DISCRIMINATION'] = found
        if found and row['class'] == 'B_NUMERICAL_DIFFERENCE_ONLY':
            row['class'] = 'C_INFORMATION_CONDITION_DISCRIMINATION'
    return {'criterion': 'At least one common significant predecision stage in both novel-vs-control contrasts with the same nonzero novel-minus-control norm-delta sign; thresholds fixed before native diagnostics.',
        'signature_stages': signature, 'observed': found,
        'scope': 'One world; descriptive discrimination, not population generalization.'}


def mechanism_summary860(comparisons):
    primary = {r['comparison']: r for r in comparisons
        if r['comparison'] in ('NOVEL_VS_REDUNDANT', 'NOVEL_VS_IRRELEVANT')}
    propagation = {}
    for name, row in primary.items():
        stages = row['significant_stages']
        first = next((s for s in STATE_ORDER860 if s in stages), None)
        after = STATE_ORDER860[STATE_ORDER860.index(first) + 1:] if first else []
        attenuated = next((s for s in after if s not in stages), 'NOT_OBSERVED_WITHIN_MEASURED_CHAIN')
        propagation[name] = {'first_detectable_stage': first or 'NONE_ABOVE_PRECISION',
            'first_later_nondetectable_stage': attenuated,
            'reaches_review': 'Review' in stages,
            'reaches_decision_scores': row['dimensions']['score_effect'],
            'changes_greedy_action': row['dimensions']['greedy_action_changed'],
            'changes_revision_text': row['dimensions']['revision_text_changed']}
        short860('TABLE C XRAY', name, row['states'])
        short860('TABLE E DISCRIMINATION', name, row['significant_stages'])
    early = [any(primary[n]['states'][s]['significant'] for s in ('E', 'U', 'R')) for n in primary]
    late = [any(primary[n]['states'][s]['significant'] for s in ('K0', 'J', 'Review')) for n in primary]
    decision = [primary[n]['dimensions']['D_DECISION_SENSITIVITY'] for n in primary]
    if not any(early) and not any(late) and not any(decision):
        candidate = 'REPRESENTATION_ISSUE_CANDIDATE_LIMITED_TO_MEASURED_STATES'
    elif all(early) and not any(late):
        candidate = 'TRANSMISSION_ISSUE_CANDIDATE_EARLY_ONLY'
    elif all(late) and not any(decision):
        candidate = 'DECISION_MAPPING_ISSUE_CANDIDATE_PREDECISION_ONLY'
    else:
        candidate = 'UNRESOLVED_MIXED_OR_DECISION_SENSITIVE_PATTERN'
    return {'propagation': propagation, 'explanation_candidate': candidate,
        'not_a_definitive_diagnosis': True, 'world_count': 1,
        'unresolved': 'Single-world matched replays cannot identify a unique internal cause or generalize across tasks.'}


def required_answers860(conditions, comparisons, discrimination, mechanism, transport):
    by_name = {r['comparison']: r for r in comparisons}
    novel_redundant = by_name['NOVEL_VS_REDUNDANT']
    novel_irrelevant = by_name['NOVEL_VS_IRRELEVANT']
    novel_new = by_name['NOVEL_VS_NO_NEW']
    no_new = conditions['NO_NEW_INFORMATION']
    return {
        '1_new_vs_repeated': {'discrimination_observed': discrimination['observed'],
            'signature_stages': discrimination['signature_stages'],
            'contrast': novel_redundant['class']},
        '2_novel_vs_irrelevant': {'significant_stages': novel_irrelevant['significant_stages'],
            'score_effect': novel_irrelevant['dimensions']['score_effect'],
            'greedy_action_changed': novel_irrelevant['dimensions']['greedy_action_changed']},
        '3_contradictory_information': 'NOT_APPLICABLE: no valid matched contradictory condition was fabricated.',
        '4_Kprev_and_C_transport': transport,
        '5_J_and_review_preservation': {name: {
            'J': by_name[name]['states']['J'],
            'Review': by_name[name]['states']['Review']}
            for name in ('NOVEL_VS_REDUNDANT', 'NOVEL_VS_IRRELEVANT')},
        '6_native_decision_score_sensitivity': {name: {
            'score_effect': row['dimensions']['score_effect'],
            'greedy_action_changed': row['dimensions']['greedy_action_changed']}
            for name, row in by_name.items()},
        '7_revise_without_new_information': {
            'observed_action': no_new['greedy_action'],
            'observed_revision': None if no_new.get('revision') is None else no_new['revision']['text'],
            'margins': no_new['margins'],
            'interpretation': 'REVISE and UNKNOWN coexist with the measured scores; the reason REVISE remains preferred is UNRESOLVED, not inferred from UNKNOWN.'},
        '8_action_tendency_with_novel_information': {
            'novel_action': conditions['NOVEL_USEFUL_INFORMATION']['greedy_action'],
            'novel_revision': conditions['NOVEL_USEFUL_INFORMATION'].get('revision'),
            'changes_vs_no_new': novel_new['dimensions']['greedy_action_changed'] or novel_new['dimensions']['revision_text_changed'],
            'score_effect_vs_no_new': novel_new['dimensions']['score_effect']},
        '9_representation_transmission_decision_evidence': mechanism,
        '10_still_unexplained_before_motor_revision': mechanism['unresolved'],
    }


def run_analysis860(env):
    digest = records_digest860(env)
    STATE860['original_record_sha256'] = digest
    conditions_list = resolve_conditions860(env)
    conditions = {r['condition']: r for r in conditions_list}
    job = env['JOBS841'][1]
    transfers = transport859(env, job)
    native_sequences = native_sequences860(env)
    original = original_condition860(env, conditions['NO_NEW_INFORMATION'], native_sequences)
    results = {'NO_NEW_INFORMATION': original}
    runtime_states = {'NO_NEW_INFORMATION': {}}
    snap = snapshots860(env)
    pm = segment_map859(env, snap['pre1']['segments'])
    dm = segment_map859(env, snap['review1']['segments'])
    runtime_states['NO_NEW_INFORMATION'] = {
        'C': pm['C'][1], 'E': pm['E'][1], 'U': pm['U'][1], 'R': pm['R'][1],
        'Kprev': pm['Kprev'][1], 'K0': snap['pre1']['h']['rows'], 'J': dm['J'][1],
        'Review': snap['review1']['h']['rows']}
    for name in ('REDUNDANT_INFORMATION', 'NOVEL_USEFUL_INFORMATION', 'IRRELEVANT_INFORMATION'):
        result = run_diagnostic860(env, conditions[name], original)
        results[name] = result
        runtime_states[name] = DIAGNOSTIC_RUNTIME860[name]
    restore = run_diagnostic860(env, conditions['NO_NEW_INFORMATION'], original, True)
    assert restore['restore_exact']
    comparisons = []
    for name, a, b in COMPARISON_PLAN860:
        comparisons.append(compare_runtime860(env, name, results[a], results[b], runtime_states))
    discrimination = information_discrimination860(comparisons)
    mechanism = mechanism_summary860(comparisons)
    assert records_digest860(env) == digest, 'DIAGNOSTICS_CHANGED_ORIGINAL_RECORDS'
    assert_hook_free859(env, 'post_TEST860_information_xray')
    assert not any(p.requires_grad for p in env['model'].parameters())
    STATE860['condition_results'] = results
    STATE860['comparisons'] = comparisons
    answers = required_answers860(results, comparisons, discrimination, mechanism, transfers)
    class_counts = {letter: sum(r['class'].startswith(letter + '_') for r in comparisons)
        for letter in 'ABCDE'}
    analysis = {
        'status': 'TECHNICAL_XRAY_COMPLETE_RESULTS_NOT_PRESET',
        'original_records_unchanged': True, 'restore_full_path_exact': True,
        'valid_conditions': [r['condition'] for r in conditions_list if r['validity'] == 'VALID'],
        'not_applicable_conditions': [r['condition'] for r in conditions_list if r['validity'] == 'NOT_APPLICABLE'],
        'class_counts': class_counts, 'information_discrimination': discrimination,
        'native_decision_sensitivity_observed': False,
        'native_decision_sensitivity_scope': 'UNRESOLVED_ONLY_NO_NEW_INFORMATION_IS_ORIGINAL_NATIVE',
        'diagnostic_decision_sensitivity_observed': any(r['dimensions']['D_DECISION_SENSITIVITY'] for r in comparisons),
        'diagnostic_greedy_action_effect_observed': any(r['dimensions']['greedy_action_changed'] for r in comparisons),
        'evidence_aligned_decision_effect_observed': any(r['dimensions']['E_EVIDENCE_ALIGNED_DECISION_EFFECT'] for r in comparisons),
        'native_model_stop_observed': any(v['model_stop'] for v in native_sequences.values()),
        'diagnostic_stop_observed': any(r['diagnostic_stop_action'] for r in results.values()),
        'mechanism': mechanism, 'required_answers': answers,
        'scope': 'Two original jobs, one information world, three matched diagnostic mount changes; no statistical generalization.'}
    information_artifact = {'preregistered_plan': CONDITION_PLAN860,
        'thresholds': {'state_relative_l2': STATE_REL_L2_EPS860, 'score_abs_sequence_logp': SCORE_ABS_EPS860},
        'feasibility': {
            'original_mid_loop_evidence_mount': 'NOT_SUPPORTED_INITIAL_CARDS_FIXED_FOR_EACH_JOB',
            'native_new_information_conditions_added_to_original_loop': 0,
            'physical_data_preparation': 'Existing CUT3/H3/KV cartridges only; REDUNDANT remounts the same first cartridge; no new cartridge or architecture.',
            'diagnostic_scope': 'Post-hoc only; C and Kprev originate from the same original cycle0 outputs.',
            'contradiction': 'NOT_APPLICABLE_NO_MATCHED_PRIOR_ENDPOINT'},
        'conditions': conditions_list, 'transfers': transfers,
        'matching_proof': {name: {
            'C_source_sha256': state_metrics859(env, runtime_states[name]['C'])['sha256'],
            'Kprev_source_sha256': state_metrics859(env, runtime_states[name]['Kprev'])['sha256']}
            for name in results},
        'original_record_sha256': digest}
    state_artifact = {'conditions': {name: {'execution': r['execution'],
            'source_cards': r['source_cards'], 'states': r['state']} for name, r in results.items()},
        'comparisons': comparisons, 'mechanism': mechanism,
        'restore': {'execution': restore['execution'], 'exact': True,
            'scores': restore['scores'], 'margins': restore['margins']}}
    decision_artifact = {'native_sequences': native_sequences,
        'condition_decisions': results, 'comparisons': comparisons,
        'teacher_forced_scores_are_not_calibrated_probabilities': True,
        'diagnostic_actions_are_not_original_actions': True,
        'required_answers': answers}
    json_write860('860_information_conditions.json', information_artifact)
    json_write860('860_state_xray.json', state_artifact)
    json_write860('860_decision_effects.json', decision_artifact)
    short860('TABLE G MECHANISM', json.dumps(mechanism, ensure_ascii=False))
    short860('TABLE G REQUIRED ANSWERS', json.dumps(answers, ensure_ascii=False))
    STATE860['analysis'] = analysis
    return analysis


# CPU runtime states are populated inside run_diagnostic860 without serializing tensors.
DIAGNOSTIC_RUNTIME860 = {}


def write_partial860():
    if not (ROOT860 / '860_information_conditions.json').exists():
        json_write860('860_information_conditions.json', {
            'preregistered_plan': CONDITION_PLAN860, 'conditions': STATE860['conditions'],
            'status': 'PARTIAL_OR_NOT_STARTED'})
    if not (ROOT860 / '860_state_xray.json').exists():
        json_write860('860_state_xray.json', {'status': 'PARTIAL_OR_NOT_STARTED',
            'comparisons': STATE860['comparisons']})
    if not (ROOT860 / '860_decision_effects.json').exists():
        json_write860('860_decision_effects.json', {'status': 'PARTIAL_OR_NOT_STARTED',
            'native_sequences': STATE860['native_sequences'],
            'condition_decisions': STATE860['condition_results']})


def finalize860(gates, execution):
    write_partial860()
    capture_cell_source860()
    source_present = (ROOT860 / '860.py').is_file() and (ROOT860 / '860.py').stat().st_size > 0
    gates['GATE8_ARTIFACT_INTEGRITY'] = 'PASS' if source_present else 'FAIL'
    required = ('GATE0_SOURCE_INTEGRITY', 'GATE1_HOOKFREE_ORIGINAL_TWO_JOBS',
        'GATE2_OBSERVER_EQUIVALENCE', 'GATE3_INFORMATION_CONDITION_VALIDITY',
        'GATE4_MATCHED_NATIVE_XRAY_AND_RESTORE', 'GATE8_ARTIFACT_INTEGRITY')
    technical = all(gates.get(k) == 'PASS' for k in required)
    report = {'test': TEST860_KIND, 'execution': execution, 'gates': gates,
        'technical_result': 'TECHNICAL_XRAY_PASS' if technical else 'TECHNICAL_XRAY_NOT_PASSED',
        'scientific_result': 'DIAGNOSTIC_INFORMATION_CONDITION_DISCRIMINATION_OBSERVED' if ANALYSIS860.get(
            'information_discrimination', {}).get('observed') else 'DIAGNOSTIC_INFORMATION_CONDITION_DISCRIMINATION_NOT_DEMONSTRATED',
        'behavioral_result': 'DIAGNOSTIC_DECISION_SENSITIVITY_OBSERVED' if ANALYSIS860.get(
            'diagnostic_decision_sensitivity_observed') else 'DIAGNOSTIC_DECISION_SENSITIVITY_NOT_DEMONSTRATED',
        'native_decision_result': 'UNRESOLVED_NO_NATIVE_INFORMATION_INTERVENTION',
        'evidence_aligned_result': 'DIAGNOSTIC_EVIDENCE_ALIGNED_EFFECT_OBSERVED' if ANALYSIS860.get(
            'evidence_aligned_decision_effect_observed') else 'EVIDENCE_ALIGNED_DECISION_EFFECT_NOT_DEMONSTRATED',
        'original_error': EXECUTION_ERROR860, 'analysis_error': PROBE_ERROR860,
        'diagnostic_stop': DIAGNOSTIC_STOP860, 'diagnostic_stop_is_model_stop': False,
        'technical_verification': TWO_JOB_VERIFICATION860, 'analysis': ANALYSIS860,
        'source_lock_count': len(RAW_SOURCES860), 'environment': STATE859['environment'],
        'observer_equalities': STATE859['equalities'],
        'coverage_observer_equalities': [c['observer_equality'] for c in STATE859['coverage']],
        'seconds': time.perf_counter() - START860,
        'limitations': [
            'One information world; no independent generalization claim.',
            'Only NO_NEW_INFORMATION is an original native closed-loop condition.',
            'REDUNDANT, NOVEL_USEFUL and IRRELEVANT are post-hoc DIAGNOSTIC_REPLAY conditions.',
            'CONTRADICTORY is NOT_APPLICABLE for the locked matched predecessor.',
            'Teacher-forced scores are not calibrated action probabilities.',
            'Diagnostic STOP is not original MODEL_STOP; mechanical limit is not MODEL_STOP.',
            'Tensor differences alone do not establish semantic encoding or decision improvement.'],
        'TEST860_NEW_ENGINE': False, 'TEST860_MOTOR_REVISION': False}
    json_write860('860_report.json', report)
    short860('TEST860 TECHNICAL', report['technical_result'])
    short860('TEST860 SCIENTIFIC', report['scientific_result'])
    short860('TEST860 BEHAVIORAL', report['behavioral_result'])
    for name, status in gates.items():
        short860(name, status)
    short860('ARTIFACTS', ROOT860)
    LOG_FILE860.flush()
    manifest = {}
    for path in sorted(ROOT860.rglob('*')):
        if path.is_file() and path.name != '860_sha256_manifest.json':
            manifest[str(path.relative_to(ROOT860))] = {
                'bytes': path.stat().st_size, 'sha256': sha256_bytes860(path.read_bytes())}
    json_write860('860_sha256_manifest.json', manifest)


try:
    short860('TEST860: native information conditions, numerical propagation and decision X-ray.')
    short860('GPU EXECUTION: NOT VERIFIED BY AUTHOR; restart Colab before this cell.')
    load_sources860()
    load_spine860()
    gate0 = 'PASS'
    env860, error860, trace860, evidence860 = reproduce_pre859859()
    EXECUTION_ERROR860, TRACEBACK860, ERROR_EVIDENCE860 = error860, trace860, evidence860
    if trace860:
        short860(trace860[-12000:])
    if 'GATE1_TWO_JOB_OBSERVATION_COMPLETE' in trace860:
        DIAGNOSTIC_STOP860 = 'GATE1_TWO_JOB_OBSERVATION_COMPLETE'
    try:
        TWO_JOB_VERIFICATION860 = verify_two_job859(env860, trace860)
        EXECUTION_ERROR860 = None
        gate1 = gate2 = 'PASS'
    except Exception as exc:
        EXECUTION_ERROR860 = type(exc).__name__ + ': ' + str(exc)
        gate1 = gate2 = 'BLOCKED'
        short860(traceback.format_exc())
    if gate1 == 'PASS':
        try:
            install_offline_evaluator859(env860)
            ANALYSIS860 = run_analysis860(env860)
            gate3 = gate4 = 'PASS'
            execution = 'INFORMATION_XRAY_COMPLETE'
        except BaseException as exc:
            PROBE_ERROR860 = type(exc).__name__ + ': ' + str(exc)
            TRACEBACK860 += '\n===== TEST860 ANALYSIS FAILURE =====\n' + traceback.format_exc()
            short860(traceback.format_exc())
            gate3 = gate4 = 'BLOCKED'
            execution = 'ANALYSIS_INCOMPLETE_FULL_TRACEBACK_IN_LOG'
    else:
        gate3 = gate4 = 'BLOCKED'
        execution = 'TWO_JOB_TECHNICAL_VERIFICATION_FAILED'
    gates = {
        'GATE0_SOURCE_INTEGRITY': gate0,
        'GATE1_HOOKFREE_ORIGINAL_TWO_JOBS': gate1,
        'GATE2_OBSERVER_EQUIVALENCE': gate2,
        'GATE3_INFORMATION_CONDITION_VALIDITY': gate3,
        'GATE4_MATCHED_NATIVE_XRAY_AND_RESTORE': gate4,
        'GATE5_INFORMATION_DISCRIMINATION': 'OBSERVED_DIAGNOSTIC_ONLY' if ANALYSIS860.get(
            'information_discrimination', {}).get('observed') else 'NOT_DEMONSTRATED',
        'GATE6_DIAGNOSTIC_DECISION_SENSITIVITY': 'OBSERVED_DIAGNOSTIC_ONLY' if ANALYSIS860.get(
            'diagnostic_decision_sensitivity_observed') else 'NOT_DEMONSTRATED',
        'GATE7_EVIDENCE_ALIGNED_DECISION_EFFECT': 'OBSERVED_DIAGNOSTIC_ONLY' if ANALYSIS860.get(
            'evidence_aligned_decision_effect_observed') else 'NOT_DEMONSTRATED',
        'GATE8_ARTIFACT_INTEGRITY': 'PASS'}
    finalize860(gates, execution)
except BaseException as exc:
    EXECUTION_ERROR860 = type(exc).__name__ + ': ' + str(exc)
    sys.stdout, sys.stderr = CONSOLE860, ERROR_CONSOLE860
    short860(traceback.format_exc())
    gates = {
        'GATE0_SOURCE_INTEGRITY': 'PASS' if len(RAW_SOURCES860) == 21 else 'FAIL',
        'GATE1_HOOKFREE_ORIGINAL_TWO_JOBS': 'BLOCKED',
        'GATE2_OBSERVER_EQUIVALENCE': 'BLOCKED',
        'GATE3_INFORMATION_CONDITION_VALIDITY': 'BLOCKED',
        'GATE4_MATCHED_NATIVE_XRAY_AND_RESTORE': 'BLOCKED',
        'GATE5_INFORMATION_DISCRIMINATION': 'BLOCKED',
        'GATE6_DIAGNOSTIC_DECISION_SENSITIVITY': 'BLOCKED',
        'GATE7_EVIDENCE_ALIGNED_DECISION_EFFECT': 'BLOCKED',
        'GATE8_ARTIFACT_INTEGRITY': 'PASS'}
    finalize860(gates, 'TEST860_FAILURE_FULL_TRACEBACK_IN_LOG')
finally:
    LOG_FILE860.close()
