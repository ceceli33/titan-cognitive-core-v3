# AKBASCORE SILICON HIPPOCAMPUS — TEST864 NATIVE EVIDENCE-SEEKING CONTROL AND PHYSICAL MEMORY RE-ENTRY
# Locked TEST863 two-job spine; explicitly experimental state-conditioned search adapter.
# Model produces SEARCH and the soft-row query. Python performs only locked numerical addressing,
# SHA-verified SSD cartridge I/O and native CUT3/H3/KV mount. Offline labels never enter model inputs.
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
import random
import re
import symtable
import sys
import time
import traceback
import torch
import urllib.request
import zipfile

TEST864_KIND = 'NATIVE_EVIDENCE_SEEKING_CONTROL_AND_PHYSICAL_MEMORY_REENTRY'
CODELOAD864 = 'https://codeload.github.com/ceceli33/titan-cognitive-core-v3/zip/refs/heads/main'
LOCKS864 = {
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
    '863.py': '9c0bf68f19df1327390d973c3a5e85b2694a439d',
    '863.log': '9cb413320c5fb59cb3e06e81570cd62d070f920e',
    '721.py': '7c6575beddca87f02c344ee1a132f02b191dc00a',
    '721.log': '45d852b725d34d09711f4d5b5922444098e337cb',
    '757.py': '3d88bf8638390995858f23391f1e043faa586835',
    '757.log': '8c0899369a01ad5c4fc22dd5124b4ddd41125ddb',
    '759.py': '273827a86c569a0e06cae88fe3909bf7bb2bea58',
    '759.log': 'c33ec387761dab07563edda3d635038d80867f00',
    '779.py': 'fa7017a87f25ecef6ed2b2954a850599cb25fcd9',
    '779.log': 'a12ece7011b0db2629f18f2eafa8b01c4dd3f3a3',
    '785.py': 'dfb5f7869efd50bf2c202723286eb7876338af86',
    '785.log': 'd319098c747dbc13a74eb361e43829d34075081e',
    '835.py': '9327cebc651f173fd547362825679a1a790fcd6b',
    '835.log': 'bfad088c81666674b766c3de95f08e0ab00f4817',
    '840.py': '06bc63ddcda9c11780bd99a7dd58f00f57b80f0e',
    '840.log': 'beaeedccf8dc469ee17e5802e242c7750f91bf2d',
    '841.py': '135b18e5b1ea113579c607cf9eecf49628cf18c2',
    '841.log': '4c22215bde9f169c0566f90a77ac7904d43d1566',
    '842.py': '4653fe9a5dd7bc2dd3a72f25bed00ceebb3936fd',
    '842.log': 'f6406b0e3525ff2f22cea1464a175c61bf2c2936',
    '846.py': '6093896b7e4492f201cece448ad1646b0bd8820a',
    '846.log': 'f8123c76f7e37700eaa0cb6349dfee87a72912c4',
}
BLIND_SEED864 = 8642026
SHUFFLE_CONTROL_SEED864 = 8642027
TOPK864 = (1, 3, 5)
SEARCH_FRAME864 = 'A'
SEARCH_QUERY_PROTOCOL864 = 'STATE_CONDITIONED_GEN851_SOFT_ROWS_TO_TEST841_H3_PEAK50'
ABSTENTION_PROTOCOL864 = 'NOT_SUPPORTED_LOCKED_ROUTE841_ALWAYS_SELECTS_TOP1'
ADAPTER_REENTRY_EVALUATIONS864 = 1
STAMP864 = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
ROOT864 = pathlib.Path('/content') / ('TEST864_MEMORY_REENTRY_' + STAMP864)
ROOT864.mkdir(parents=True, exist_ok=False)
CONSOLE864, ERROR_CONSOLE864 = sys.stdout, sys.stderr
LOG_FILE864 = open(ROOT864 / '864.log', 'w', encoding='utf-8')
START864 = time.perf_counter()
REAL_COMPILE864 = builtins.compile
RAW_SOURCES864 = {}
STATE864 = {'source_audit': {}, 'inventory': {}, 'search_signals': {},
    'ranking': {}, 'negative_controls': {}, 'memory_reentry': {},
    'xray': {}, 'interpretation': {}, 'native': {}, 'restores': []}
EXECUTION_ERROR864 = None
TRACEBACK864 = ''
ORIGINAL_CONTROL_TRACE864 = ''
TWO_JOB_VERIFICATION864 = {}
NATIVE_REGRESSION864 = {}
ANALYSIS864 = {}

# TEST863 compatibility namespace: definitions only, never its top-level experiment.
ROOT863 = ROOT862 = ROOT861 = ROOT860 = ROOT859 = ROOT864
LOG_FILE863 = LOG_FILE862 = LOG_FILE861 = LOG_FILE860 = LOG_FILE859 = LOG_FILE864
START863 = START862 = START861 = START860 = START859 = START864
CONSOLE863 = CONSOLE862 = CONSOLE861 = CONSOLE860 = CONSOLE859 = CONSOLE864
ERROR_CONSOLE863 = ERROR_CONSOLE862 = ERROR_CONSOLE861 = ERROR_CONSOLE860 = ERROR_CONSOLE859 = ERROR_CONSOLE864
REAL_COMPILE863 = REAL_COMPILE862 = REAL_COMPILE861 = REAL_COMPILE860 = REAL_COMPILE859 = REAL_COMPILE864
RAW_SOURCES863 = RAW_SOURCES862 = RAW_SOURCES861 = RAW_SOURCES860 = RAW_SOURCES859 = RAW_SOURCES864
LOCKS863 = {k: v for k, v in LOCKS864.items() if k in {
    '849.py','850.py','851.py','852.py','853.py','854.py','850.log','851.log','852.log',
    '853.log','854.log','855.py','856.py','857.py','855.log','856.log','857.log','858.py',
    '858.log','859.py','859.log','860.py','860.log','861.py','861.log','862.py','862.log'}}
LOCKS862 = {k: v for k, v in LOCKS863.items() if not k.startswith('862.')}
LOCKS861 = {k: v for k, v in LOCKS862.items() if not k.startswith('861.')}
STATE_REL_L2_EPS863 = STATE_REL_L2_EPS862 = STATE_REL_L2_EPS861 = 1e-7
SCORE_ABS_EPS863 = SCORE_ABS_EPS862 = SCORE_ABS_EPS861 = 1e-6
REGRESSION_ABS_EPS863 = REGRESSION_ABS_EPS862 = REGRESSION_ABS_EPS861 = 1e-5
STATE_ORDER863 = ('C', 'E', 'U', 'R', 'Kprev', 'K0', 'J', 'Review', 'Revision')
STATE863 = {'spine_loaded': False, 'dependency_audit': {}, 'original_record_sha256': None,
    'memory': {}, 'candidates': {}, 'joint': {}, 'transitions': {}, 'xray': {},
    'restores': [], 'analysis': {}}
RUNTIME863 = {}
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
    'environment': {}, 'start': START864}
FAILURES859 = []
LAST_CONTEXT859 = None
SPELLINGS859 = (' CONTINUE', ' REVISE', ' STOP', ' SUFFICIENT', ' INSUFFICIENT')


def sha256_bytes864(data):
    return hashlib.sha256(data).hexdigest()


def git_blob864(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def sha256_file864(path):
    h = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def json_write864(name, value):
    path = ROOT864 / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
        allow_nan=False), encoding='utf-8')
    return path


def short864(*args):
    text = ' '.join(str(x) for x in args)
    print(text, file=CONSOLE864, flush=True)
    LOG_FILE864.write(text + '\n')
    LOG_FILE864.flush()


def table864(label, job='GLOBAL', cycle='NA', execution='SOURCE_AUDIT',
        cartridge='NA', decision='NA', integrity='PASS', payload=None):
    short864('TABLE ' + label, 'job=' + str(job), 'cycle=' + str(cycle),
        'execution=' + execution, 'cartridge=' + str(cartridge),
        'decision=' + str(decision), 'integrity=' + integrity,
        '' if payload is None else json.dumps(payload, ensure_ascii=False))


# Aliases used by the selected locked definitions.
short863 = short862 = short861 = short864
json_write863 = json_write862 = json_write861 = json_write864
sha256_bytes863 = sha256_bytes862 = sha256_bytes861 = sha256_bytes864
git_blob863 = git_blob862 = git_blob864
sha256_bytes859 = sha256_bytes864
git_blob859 = git_blob864


def capture_cell_source864():
    try:
        shell = get_ipython()  # supplied by Colab/IPython
        history = list(shell.history_manager.input_hist_raw)
        marker = 'AKBASCORE SILICON HIPPOCAMPUS — TEST864 NATIVE EVIDENCE-SEEKING CONTROL AND PHYSICAL MEMORY RE-ENTRY'
        candidates = [text for text in history if marker in text]
        if candidates:
            source_text = candidates[-1]
            (ROOT864 / '864.py').write_text(source_text, encoding='utf-8')
            RAW_SOURCES864['864.py'] = source_text.encode('utf-8')
            return True
    except Exception as exc:
        table864('A SOURCE CAPTURE', execution='NOT_SUPPORTED', integrity='FAIL',
            payload={'error': type(exc).__name__ + ': ' + str(exc)})
    return False


def load_sources864():
    request = urllib.request.Request(CODELOAD864,
        headers={'User-Agent': 'AKBASCORE-TEST864-GATE0'})
    with urllib.request.urlopen(request, timeout=240) as response:
        archive = response.read(100000001)
    rows = []
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        for name, expected in LOCKS864.items():
            matches = [n for n in zipped.namelist() if n.endswith('/' + name)]
            assert len(matches) == 1, ('SOURCE_NOT_UNIQUE', name, matches)
            data = zipped.read(matches[0])
            actual = git_blob864(data)
            assert actual == expected, ('SOURCE_GIT_BLOB_MISMATCH', name, expected, actual)
            if name.endswith('.py'):
                ast.parse(data.decode('utf-8'), filename=name)
            RAW_SOURCES864[name] = data
            rows.append({'file': name, 'bytes': len(data), 'git_blob_sha1': actual,
                'sha256': sha256_bytes864(data), 'status': 'PASS'})
            table864('A SOURCE', cartridge=name, payload={'git_blob_sha1': actual})
    assert len(rows) == len(LOCKS864) == 49
    STATE864['source_audit']['locks'] = rows
    return rows


def feasibility_audit864():
    sources = {name: RAW_SOURCES864[name].decode('utf-8') for name in LOCKS864
        if name.endswith('.py')}
    required = {
        '841.py': ('def address841(', 'def route841(', 'def peak50_841(',
            'def h3_bypass841(', 'def mem_for841(', 'def parse_action841(',
            'def index_embeds841('),
        '851.py': ('def gen851(', 'def shared851('),
        '757.py': ('def native_append_direct(', 'def build_fusion(',
            'def load_verified(', 'shifted.append(rephase('),
        '721.py': ('def safe_load_cartridge(', 'torch.load(path,map_location=\'cpu\',weights_only=True)'),
        '863.py': ('def audit_job863(', 'def exact_restore863(', 'def physical_seal863(')}
    for name, snippets in required.items():
        for snippet in snippets:
            assert snippet in sources[name], ('FEASIBILITY_SNIPPET_MISSING', name, snippet)
    log841 = RAW_SOURCES864['841.log'].decode('utf-8')
    assert 'M2S      R1 12/12 PASS' in log841
    assert 'MODEL_CHOSEN_ACTIONS_IN_FIXED_LOOP ACT=PASS' in log841
    log863 = RAW_SOURCES864['863.log'].decode('utf-8')
    for item in ('TEST863 TECHNICAL TECHNICAL_NATIVE_REACHABILITY_PASS',
            'GATE4_NATIVE_STATE_AND_REACHABILITY_AUDIT PASS',
            'GATE5_EXACT_RESTORE PASS', 'TEST863 AUTONOMOUS CORRECTION CLOSURE NOT_OBSERVED'):
        assert item in log863, ('REFERENCE_863_GATE_MISSING', item)
    protocol = {'blind_seed': BLIND_SEED864, 'shuffle_control_seed': SHUFFLE_CONTROL_SEED864,
        'topk': TOPK864, 'frame': SEARCH_FRAME864, 'query_protocol': SEARCH_QUERY_PROTOCOL864,
        'abstention': ABSTENTION_PROTOCOL864,
        'reentry_evaluations': ADAPTER_REENTRY_EVALUATIONS864,
        'query_states': ['C', 'E', 'U', 'R', 'K0', 'J', 'Review'],
        'query_state_slot_map': {'C': 'C_SLOT851', 'E': 'E_SLOT851', 'U': 'U_SLOT852',
            'R': 'R_SLOT852', 'K0': 'K_SLOT854', 'J': 'J_SLOT854', 'Review': 'K_SLOT851'},
        'main_adapter_job': 'REMOVED cycle1 only',
        'no_target_or_answer_in_model_or_router_inputs': True,
        'no_threshold_fit_or_card_substitution': True,
        'scope': 'PILOT_ONLY_ONE_WORLD_TWO_ORIGINAL_JOBS'}
    protocol_sha = sha256_bytes864(json.dumps(protocol, sort_keys=True).encode('utf-8'))
    feasibility = {
        'native_query_origin': 'Original REMOVED cycle1 C/E/U/R/K0/J/Review -> locked gen851 soft rows; no random tensor.',
        'search_decision_origin': 'Same original states -> locked ACTION_TXT841 -> gen851 text -> parse_action841.',
        'addressing': 'Locked index_embeds841 -> h3_bypass841 over MEMNULL841 -> route841 PEAK50.',
        'physical_format': 'CPU .pt cartridge with H3 plus CUT3 lower K/V; safe_load verifies file and tensor SHA.',
        'reentry': 'Locked mem_for841/mount834/build_fusion; native_append_direct rephases appended RoPE keys.',
        'adapter_supported_conditionally': True,
        'native_vs_adapter': 'Original jobs are LEVEL_A; query/address are LEVEL_B; remount/evaluation are LEVEL_C.',
        'protocol': protocol, 'protocol_sha256': protocol_sha,
        'status': 'PASS_BEFORE_MODEL_LOAD'}
    STATE864['source_audit'].update({'feasibility': feasibility, 'protocol': protocol,
        'protocol_sha256': protocol_sha})
    table864('A FEASIBILITY', payload=feasibility)
    return feasibility


def _selected863_nodes864():
    tree = ast.parse(RAW_SOURCES864['863.py'].decode('utf-8'), filename='863.py')
    names = {'_selected862_nodes863', 'load_spine863', 'parse_reference862',
        'native_regression863', 'state863', 'comparison863', 'transfer863',
        'check_output_h863', 'shared_native863', 'cartridge_detail863',
        'physical_seal863', '_score_margin_deltas863', 'audit_job863',
        'exact_restore863', '_first_missing863', 'final_reachability863',
        'run_analysis863', 'native_closure862'}
    # native_closure862 is loaded from 862.py by the 863 spine, not duplicated here.
    names.remove('native_closure862')
    nodes = [copy.deepcopy(n) for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == names
    return tree, nodes


def load_spine864():
    assert not STATE863['spine_loaded']
    tree863, nodes863 = _selected863_nodes864()
    exec(REAL_COMPILE864(ast.fix_missing_locations(ast.Module(
        body=nodes863, type_ignores=[])),
        'TEST864_REUSED_863_DEFINITIONS_ONLY', 'exec'), globals())
    load_spine863()
    _dependency_audit861(nodes863)
    STATE864['source_audit']['dependency_audit'] = copy.deepcopy(STATE861['dependency_audit'])
    STATE864['source_audit']['spine_ast_sha256'] = sha256_bytes864(ast.dump(ast.Module(
        body=nodes863, type_ignores=[]), include_attributes=False).encode('utf-8'))
    table864('A DEPENDENCIES', payload=STATE864['source_audit']['dependency_audit'])
    assert '864.py' in RAW_SOURCES864, 'EXECUTED_864_SOURCE_NOT_CAPTURED'
    tree864 = ast.parse(RAW_SOURCES864['864.py'].decode('utf-8'), filename='864.py')
    adapter_nodes = [copy.deepcopy(n) for n in tree864.body if isinstance(n, ast.FunctionDef)
        and n.name not in {'capture_cell_source864', 'load_spine864'}]
    _dependency_audit861(adapter_nodes)
    STATE864['source_audit']['adapter_dependency_audit'] = copy.deepcopy(STATE861['dependency_audit'])
    STATE864['source_audit']['adapter_ast_sha256'] = sha256_bytes864(ast.dump(ast.Module(
        body=adapter_nodes, type_ignores=[]), include_attributes=False).encode('utf-8'))
    table864('A ADAPTER DEPENDENCIES', payload=STATE864['source_audit']['adapter_dependency_audit'])


def parse_reference863():
    text = RAW_SOURCES864['863.log'].decode('utf-8')
    pattern = re.compile(
        r'^TABLE B ORIGINAL NATIVE (\S+) cycle=ALL execution=ORIGINAL_NATIVE (INTACT|REMOVED) (\S+) (\[.*?\]) model_stop=(True|False)$',
        re.MULTILINE)
    rows = []
    for job, condition, end, actions, model_stop in pattern.findall(text):
        rows.append({'reference_job': job, 'condition': condition, 'end': end,
            'actions': ast.literal_eval(actions), 'model_stop': model_stop == 'True'})
    assert len(rows) == 2, ('REFERENCE_863_NATIVE_JOB_COUNT', len(rows))
    return {row['condition']: row for row in rows}


def native_regression864(env, native):
    reference862 = parse_reference862()
    regression = native_regression863(env, native, reference862)
    reference863 = parse_reference863()
    comparisons = {}
    for job in env['JOBS841'][:2]:
        jid, condition = job['job'], job['intervention']
        actual = {'end': env['REC841'][jid]['end'],
            'actions': [c['action'] for c in env['REC841'][jid]['cycles']],
            'model_stop': env['REC841'][jid]['model_stop']}
        expected = {k: reference863[condition][k] for k in ('end', 'actions', 'model_stop')}
        assert actual == expected, ('NATIVE_863_REGRESSION', jid, actual, expected)
        assert jid == reference863[condition]['reference_job'], ('NATIVE_JOB_ID_REGRESSION', jid)
        comparisons[jid] = {'condition': condition, 'actual': actual,
            'reference863': reference863[condition], 'exact': True}
        table864('B ORIGINAL NATIVE', job=jid, cycle='ALL', execution='ORIGINAL_NATIVE',
            decision=actual['actions'], payload=actual)
    regression['native_863_comparisons'] = comparisons
    regression['adapter_not_run_yet'] = True
    return regression


def native_motor_map864(env):
    body = STATE859['g']['BODY841']
    required = ('def gen849(', 'def gen851(', 'def invoke851(', 'def relation852(',
        'def interaction854(', 'def shared851(', 'def coverage_state852(',
        'def mem_for841(', 'mem851 = list(j851[\'initial_cards\'])',
        'MAX_REVIEWS851 = 2', "end851 = 'MECHANICAL_REVIEW_LIMIT'")
    for snippet in required:
        assert snippet in body, ('NATIVE_MOTOR_MAP_MISSING', snippet)
    result = {'level': 'LEVEL_A_LOCKED_ORIGINAL_MOTOR',
        'memory': 'Initial cartridge list mounted once; original REVISE cannot add a cartridge.',
        'candidate': 'shared851 native hop0/hop generation.',
        'review': 'C/E/U/R/Kprev -> precontrol K0 -> J -> native Review.',
        'review_limit': 2, 'mechanical_limit_is_model_stop': False,
        'adapter_is_not_original_native': True}
    STATE864['source_audit']['native_motor_map'] = result
    return result


def tensor_summary864(env, rows):
    return state_metrics859(env, rows.detach().float().cpu().contiguous())


def transfer864(env, name, stage, rows, dest, expected, recompute=None,
        source_stage='experimental', source_execution='LEVEL_C_EXPERIMENTAL_MEMORY_ADAPTER'):
    observed = tensor_summary864(env, rows)
    record = {'name': name, 'source_stage': source_stage, 'destination_stage': stage,
        'source_execution': source_execution, 'destination_slot': dest,
        'continuity': 'CPU_NUMERICAL_STATE_ROWS', 'observed': observed,
        'identity_or_recompute': 'RECOMPUTE_EQUALITY' if recompute is not None else 'OBJECT_IDENTITY',
        'passed': False}
    matched = [value for slot, value in expected['segments'] if slot == dest]
    assert len(matched) == 1, ('DESTINATION_SLOT_NOT_UNIQUE', name, stage, len(matched))
    destination = tensor_summary864(env, matched[0])
    record['destination'] = destination
    record['comparison'] = comparison863(env, rows, matched[0])
    record['bf16'] = continuity_for_slot859(env, expected, dest)
    assert record['bf16'].get('status') == 'CHECKED' and record['bf16'].get('exact_after_bf16'), (
        'STATE_TRANSFER_BF16_864', name, stage, record['bf16'])
    record['passed'] = bool(record['comparison']['exact'])
    if recompute is not None:
        recomputed_rows = recompute()
        second = tensor_summary864(env, recomputed_rows)
        record['recomputed'] = second
        record['recompute_comparison'] = comparison863(env, rows, recomputed_rows)
        record['passed'] = record['passed'] and bool(record['recompute_comparison']['exact'])
    assert record['passed'], ('STATE_TRANSFER_864', name, stage, record)
    return record


def inventory_cartridge864(env, cid, expected_control=False):
    entry = env['entries'][cid]
    path = env['CART_DIR'] / entry['file']
    record = {'cartridge': cid, 'file': str(path), 'offline_label_known_to_model': False,
        'control_only': expected_control}
    try:
        actual_sha = env['sha_file'](path)
        assert actual_sha == entry['sha256'], ('CARTRIDGE_SHA_MISMATCH', cid)
        cp = env['safe_load'](entry)
        h3 = cp['h']
        kv = cp['lower']
        assert h3.dtype == env['DTYPE'] and h3.ndim == 3
        assert isinstance(kv, (list, tuple)) and len(kv) == env['CUT'] + 1
        finite_h3 = bool(torch.isfinite(h3).all().item())
        finite_kv = all(bool(torch.isfinite(pair[kind]).all().item())
            for pair in kv for kind in (0, 1))
        record.update({'status': 'VALID', 'file_sha256': actual_sha,
            'file_bytes': path.stat().st_size, 'H3_shape': list(h3.shape),
            'H3_dtype': str(h3.dtype), 'H3_finite': finite_h3,
            'stored_lower_KV_layers': list(range(len(kv))),
            'stored_lower_KV_layer_count': len(kv),
            'runtime_80_layer_cache_not_stored': True,
            'expected_prefix_tokens': int(cp['p']),
            'lower_prefix_tokens': int(kv[0][0].shape[-2]),
            'H3_total_tokens': int(h3.shape[1]),
            'H3_body_tokens': int(cp['body_tokens']),
            'lower_KV_shapes': {str(layer): [list(pair[0].shape), list(pair[1].shape)]
                for layer, pair in enumerate(kv)}, 'lower_KV_finite': finite_kv})
    except Exception as exc:
        record.update({'status': 'CARTRIDGE_FORMAT_INCOMPATIBLE',
            'error': type(exc).__name__ + ': ' + str(exc), 'traceback': traceback.format_exc()})
        table864('C CARTRIDGE FORMAT', cartridge=cid, execution='LEVEL_B_PHYSICAL_INVENTORY',
            integrity='FAIL', payload=record)
    STATE864['inventory'][cid] = record
    return record


def adapter_pool864(env):
    job = env['JOBS841'][1]
    assert job['intervention'] == 'REMOVED'
    wi = env['QID841'].index(job['qid'])
    world = env['worlds829'][wi]
    base = list(job['initial_cards'])
    block = env['BLOCKOF841'][wi]
    bank = list(env['BANKS841'][block]['v0'])
    candidates = [cid for cid in bank if cid not in base]
    blinded = list(candidates)
    random.Random(BLIND_SEED864).shuffle(blinded)
    # Offline-only role labels: never supplied to model_search864 or route841.
    offline_target = world['ids']['second']
    other_wi = ((block + 1) % env['NBLOCK841']) * env['BLOCK841'] + wi % env['BLOCK841']
    irrelevant = env['worlds829'][other_wi]['ids']['first']
    assert offline_target in candidates and irrelevant not in base and irrelevant not in candidates
    ids = list(dict.fromkeys(base + candidates + [irrelevant]))
    inventory = [inventory_cartridge864(env, cid, cid == irrelevant) for cid in ids]
    assert all(row['status'] == 'VALID' for row in inventory), 'INVENTORY_FORMAT_FAILURE'
    result = {'job': job['job'], 'condition': job['intervention'], 'world': wi,
        'block': block, 'base_mount': base, 'bank': bank, 'blinded_candidates': blinded,
        'exclude': base, 'blind_seed': BLIND_SEED864,
        'blinded_pool_sha256': sha256_bytes864(json.dumps(blinded).encode()),
        'offline_target': offline_target, 'irrelevant_control': irrelevant,
        'pool_roles_disclosed_to_model_or_router': False,
        'pool_size': len(blinded), 'inventory_count': len(inventory)}
    table864('C BLIND POOL', job=job['job'], execution='LEVEL_B_EXPERIMENTAL_ADAPTER',
        integrity='PASS', payload=result)
    return result


def search_segments864(env, runtime):
    base = runtime[0]
    review_rows = base['review']['h']['rows']
    return [(env['C_SLOT851'], base['C']), (env['E_SLOT851'], base['E']),
        (env['U_SLOT852'], base['U']), (env['R_SLOT852'], base['R']),
        (env['K_SLOT851'], review_rows), (env['K_SLOT854'], base['K0']),
        (env['J_SLOT854'], base['J'])]


def search_decision864(env, runtime, job):
    base = runtime[0]
    previous_review = base['review']['h']
    action_prompt = env['ACTION_TXT841'].format(q=env['QTEXT841'][job['qid']])
    h = env['gen851'](base['pre']['memx'],
        env['prompt_ids'](action_prompt),
        search_segments864(env, runtime), [])
    check_output_h863(h, 'SEARCH_DECISION_CONTINUITY_INVALID')
    assert bool(torch.isfinite(h['rows']).all().item()), 'SEARCH_DECISION_NONFINITE'
    raw = h['text'].strip()
    action = env['parse_action841'](raw)
    record = {'job': job['job'], 'condition': job['intervention'],
        'execution': 'LEVEL_B_EXPERIMENTAL_SEARCH_ADAPTER', 'raw': raw, 'action': action,
        'is_search': action == 'SEARCH', 'source_cycle': 1,
        'source_states': ['C', 'E', 'U', 'R', 'K0', 'J', 'Review'],
        'previous_review_present': previous_review is not None,
        'h_sha256': h_summary859(env, h)['output']['sha256'], 'prompt': action_prompt,
        'target_or_answer_supplied': False,
        'REVISE_is_not_SEARCH': True}
    table864('E NATIVE SEARCH ACTION', job=job['job'], cycle=1,
        execution='LEVEL_B_EXPERIMENTAL_SEARCH_ADAPTER', decision=action,
        payload={k: v for k, v in record.items() if k != 'prompt'})
    return action, record


def model_search864(env, runtime, job):
    action, decision = search_decision864(env, runtime, job)
    result = {'decision': decision, 'status': 'SEARCH_SIGNAL_NOT_REQUESTED'}
    STATE864['search_signals'][job['job']] = result
    if action != 'SEARCH':
        table864('D SEARCH SIGNAL', job=job['job'], cycle=1,
            execution='LEVEL_B_EXPERIMENTAL_SEARCH_ADAPTER', decision=action,
            integrity='NOT_REQUESTED', payload={'query_generated': False})
        return None, None, result
    base = runtime[0]
    previous_review = base['review']['h']
    prompt = env['lookup_prompt841'](env['QTEXT841'][job['qid']], SEARCH_FRAME864)
    h = env['gen851'](base['pre']['memx'], env['prompt_ids'](prompt) + list(env['PREFILL841']),
        search_segments864(env, runtime), [])
    check_output_h863(h, 'SEARCH_QUERY_CONTINUITY_INVALID')
    rows = h['rows']
    assert rows is not None and rows.ndim == 2 and rows.shape[0] > 0, 'EMPTY_SEARCH_QUERY'
    assert bool(torch.isfinite(rows.float()).all().item()), 'NONFINITE_SEARCH_QUERY'
    h3, bypass_ms = env['h3_bypass841'](env['MEMNULL841'],
        embeds=env['index_embeds841'](rows.to(env['DEV'])))
    index_pre_n = len(env['embed841'](env['IDXPRE841']))
    index_post_n = len(env['embed841'](env['IDXPOST841']))
    expected_h3_rows = index_pre_n + int(rows.shape[0]) + index_post_n
    assert h3.shape == (expected_h3_rows, env['H']), ('SEARCH_H3_SHAPE', list(h3.shape))
    assert bool(torch.isfinite(h3).all().item()), 'NONFINITE_SEARCH_H3'
    qr = h3[index_pre_n:index_pre_n + int(rows.shape[0])].to('cpu', torch.float32)
    assert qr.shape == rows.shape
    query = {'status': 'MODEL_NATIVE_SEARCH_SIGNAL',
        'execution': 'LEVEL_B_EXPERIMENTAL_SEARCH_ADAPTER', 'job': job['job'],
        'condition': job['intervention'], 'source_cycle': 1,
        'source_states': ['C', 'E', 'U', 'R', 'K0', 'J', 'Review'],
        'soft_rows_shape': list(rows.shape), 'soft_rows_finite': True,
        'h3_shape': list(h3.shape), 'bypass_ms': bypass_ms,
        'query_summary': tensor_summary864(env, qr), 'h_sha256': h_summary859(env, h)['output']['sha256'],
        'prompt': prompt, 'target_or_answer_supplied': False,
        'provenance': 'gen851(model, original REMOVED cycle1 numerical states)'}
    result = {'decision': decision, 'query': query, 'status': 'SEARCH_SIGNAL_OBSERVED'}
    STATE864['search_signals'][job['job']] = result
    table864('D MODEL SEARCH SIGNAL', job=job['job'], cycle=1,
        execution='LEVEL_B_EXPERIMENTAL_SEARCH_ADAPTER', decision=action,
        payload=query)
    return h, qr, result


def ranked_from_scores864(scores, target):
    ordered = sorted(scores, key=lambda cid: (-scores[cid], cid))
    top = {}
    for k in TOPK864:
        top[str(k)] = (target in ordered[:k] if len(ordered) >= k else None) if target in scores else None
    return {'order': ordered, 'topk_hit': top,
        'target_rank': ordered.index(target) + 1 if target in ordered else None,
        'target_score': scores.get(target), 'scores': scores}


def route_and_rank864(env, qr, pool):
    chosen_route = env['route841'](qr, pool['blinded_candidates'], pool['exclude'])
    chosen = chosen_route['chosen']
    scores = chosen_route['scores']
    assert chosen in pool['blinded_candidates'] and chosen not in pool['exclude']
    ranked = ranked_from_scores864(scores, pool['offline_target'])
    top_score = scores[ranked['order'][0]]
    second_score = scores[ranked['order'][1]] if len(ranked['order']) > 1 else None
    main = {'job': pool['job'], 'condition': pool['condition'],
        'execution': 'LEVEL_B_EXPERIMENTAL_MEMORY_ADAPTER', 'chosen': chosen,
        'offline_target': pool['offline_target'], 'top1_correct': chosen == pool['offline_target'],
        'pool_size': pool['pool_size'], 'blinded_pool_sha256': pool['blinded_pool_sha256'],
        'route_ms': chosen_route['route_ms'], 'ranking': ranked,
        'top1_margin': top_score - second_score if second_score is not None else None,
        'abstention': ABSTENTION_PROTOCOL864, 'abstained': False,
        'oracle_free': True, 'selected_card_not_substituted': True}
    STATE864['ranking']['MAIN'] = main
    table864('F ADDRESS RANKING', job=pool['job'], execution=main['execution'],
        cartridge=chosen, decision='SELECTED', payload=main)
    ids = sorted(scores)
    values = [scores[cid] for cid in ids]
    random.Random(SHUFFLE_CONTROL_SEED864).shuffle(values)
    shuffled_scores = dict(zip(ids, values))
    identity_permutation = all(shuffled_scores[cid] == scores[cid] for cid in ids)
    shuffled_ranked = ranked_from_scores864(shuffled_scores, pool['offline_target'])
    shuffled = {'control': 'SHUFFLED_ADDRESSING', 'execution': 'DIAGNOSTIC_RANKING_ONLY',
        'seed': SHUFFLE_CONTROL_SEED864, 'identity_permutation': identity_permutation,
        'chosen': shuffled_ranked['order'][0],
        'offline_target': pool['offline_target'],
        'top1_correct': shuffled_ranked['order'][0] == pool['offline_target'],
        'ranking': shuffled_ranked, 'physical_mount_performed': False,
        'native_success_claim': False}
    missing_bank = [cid for cid in pool['blinded_candidates'] if cid != pool['offline_target']]
    missing_route = env['route841'](qr, missing_bank, pool['exclude'])
    missing_ranked = ranked_from_scores864(missing_route['scores'], pool['offline_target'])
    missing = {'control': 'MISSING_TARGET', 'execution': 'DIAGNOSTIC_RANKING_ONLY',
        'chosen': missing_route['chosen'], 'offline_target': pool['offline_target'],
        'false_positive_selection': True, 'router_abstained': False,
        'abstention': ABSTENTION_PROTOCOL864, 'route_ms': missing_route['route_ms'],
        'ranking': missing_ranked, 'physical_mount_performed': False,
        'native_success_claim': False}
    STATE864['ranking'].update({'SHUFFLED_ADDRESSING': shuffled, 'MISSING_TARGET': missing})
    table864('F SHUFFLED ADDRESS CONTROL', job=pool['job'], execution='DIAGNOSTIC_RANKING_ONLY',
        cartridge=shuffled['chosen'], payload=shuffled)
    table864('F MISSING TARGET CONTROL', job=pool['job'], execution='DIAGNOSTIC_RANKING_ONLY',
        cartridge=missing['chosen'], payload=missing)
    return chosen_route, main


def generate_candidate_evidence864(env, job, memx):
    q = job['qid']
    hop0 = env['gen849'](memx,
        list(env['prompt_ids'](env['FR845']['hop0'].format(q=env['QTEXT841'][q]))) + env['SLOT845'][3],
        None, None)
    check_output_h863(hop0, 'REENTRY_HOP0_INVALID')
    assert bool(torch.isfinite(hop0['rows']).all().item()), 'REENTRY_HOP0_NONFINITE'
    candidate = env['gen849'](memx,
        list(env['prompt_ids'](env['FR845']['hop'].format(q=env['QTEXT841'][q]))) + env['SLOT845'][1],
        hop0['rows'], env['SLOT845'][2])
    evidence = env['gen849'](memx,
        list(env['prompt_ids'](env['EVIDENCE851'].format(q=env['QTEXT841'][q]))),
        None, env['ANSWER_SUFFIX851'])
    coverage = env['gen849'](memx,
        list(env['prompt_ids'](env['COVERAGE852'].format(q=env['QTEXT841'][q]))),
        None, env['COVERAGE_SUFFIX852'])
    for item, name in ((candidate, 'C'), (evidence, 'E'), (coverage, 'U')):
        check_output_h863(item, 'REENTRY_CONTINUITY_' + name)
        assert bool(torch.isfinite(item['rows']).all().item()), ('REENTRY_OUTPUT_NONFINITE', name)
    return hop0, candidate, evidence, coverage


def memory_layout864(memx):
    rows = []
    finite = True
    tokens = None
    for layer, (key, value) in enumerate(memx):
        shape = list(key.shape)
        assert tuple(key.shape) == tuple(value.shape), ('RUNTIME_KV_SHAPE', layer)
        assert key.dtype == torch.bfloat16 and value.dtype == torch.bfloat16
        assert key.is_cuda and value.is_cuda
        layer_finite = bool(torch.isfinite(key).all().item() and torch.isfinite(value).all().item())
        finite = finite and layer_finite
        if tokens is None:
            tokens = int(key.shape[-2])
        assert int(key.shape[-2]) == tokens
        rows.append({'layer': layer, 'K_shape': shape, 'V_shape': list(value.shape),
            'dtype': str(key.dtype), 'device': str(key.device), 'finite': layer_finite})
    assert len(memx) == 80 and finite and tokens is not None, 'MEMORY_LAYOUT_INVALID'
    return {'layers': len(memx), 'all_80_layers': True, 'tokens': tokens,
        'dtype': 'torch.bfloat16', 'device': 'cuda', 'finite': finite, 'per_layer': rows}


def reentry864(env, job, original_runtime, selected, control_name='MAIN'):
    selected_inventory = STATE864['inventory'][selected]
    if selected_inventory['status'] != 'VALID':
        return {'control': control_name, 'selected': selected,
            'status': 'CARTRIDGE_FORMAT_INCOMPATIBLE', 'mounted': False,
            'execution': 'LEVEL_C_EXPERIMENTAL_MEMORY_REENTRY'}
    assert job['intervention'] == 'REMOVED'
    assert 0 in original_runtime
    original = original_runtime[0]
    previous_review = original['review']['h']
    base_cards = list(job['initial_cards'])
    assert selected not in base_cards
    mount = base_cards + [selected]
    base_tokens = int(env['P']) + sum(int(env['entries'][cid]['body_tokens']) for cid in base_cards)
    expected_tokens = base_tokens + int(env['entries'][selected]['body_tokens'])
    result = {'control': control_name, 'selected': selected, 'mount': mount,
        'base_mount': base_cards, 'execution': 'LEVEL_C_EXPERIMENTAL_MEMORY_REENTRY',
        'selected_card_substituted': False, 'oracle_routing': False,
        'expected_tokens': expected_tokens, 'base_tokens': base_tokens,
        'status': 'NOT_RUN', 'mounted': False, 'numeric_reentry': False}
    memx = None
    try:
        memx, mounted, mount_ms = env['mem_for841'](mount, 'TEST864_REENTRY_' + control_name)
        assert mounted and len(memx) == 80, 'MEMORY_REENTRY_NOT_SUPPORTED'
        layout = memory_layout864(memx)
        assert layout['tokens'] == expected_tokens, ('REENTRY_TOKEN_COUNT', layout['tokens'], expected_tokens)
        before_seal = physical_seal863(env, memx)
        after_seal = physical_seal863(env, memx)
        assert before_seal == after_seal
        result.update({'status': 'MOUNTED', 'mounted': True, 'mount_ms': mount_ms,
            'memory_layout': layout, 'physical_seal_sha256': before_seal,
            'physical_seal_stable': True,
            'cartridge_inventory': selected_inventory,
            'fusion_path': 'mount834/build_fusion/native_initialize_direct/native_append_direct with rephase'})
        hop0, candidate, evidence, coverage = generate_candidate_evidence864(env, job, memx)
        c_state = candidate['rows'].detach().float().cpu()
        e_state = evidence['rows'].detach().float().cpu()
        u_state = coverage['rows'].detach().float().cpu()
        r_state = env['relation852'](c_state, e_state)
        review_pre = list(env['prompt_ids'](env['REVIEW851'].format(q=env['QTEXT841'][job['qid']])))
        pre_segments = [(env['C_SLOT851'], c_state), (env['E_SLOT851'], e_state),
            (env['K_SLOT851'], previous_review['rows']), (env['U_SLOT852'], u_state),
            (env['R_SLOT852'], r_state)]
        pre_h = env['gen851'](memx, review_pre, pre_segments, env['REVIEW_SUFFIX851'])
        check_output_h863(pre_h, 'REENTRY_PRECONTROL_INVALID')
        k0 = pre_h['rows']
        j_state = env['interaction854'](c_state, e_state, k0)
        recompute_pre = list(env['prompt_ids'](env['RECOMPUTE851'].format(q=env['QTEXT841'][job['qid']])))
        assert job['arm'] == 'BASELINE853', ('UNEXPECTED_ORIGINAL_REVIEW_ARM', job['arm'])
        review_segments = [(env['K_SLOT854'], k0), (env['J_SLOT854'], j_state)]
        review = env['gen851'](memx, review_pre, review_segments, env['REVIEW_SUFFIX851'])
        check_output_h863(review, 'REENTRY_REVIEW_INVALID')
        action = env['parse849'](review['text'])
        assert action in ('CONTINUE', 'REVISE', 'STOP'), ('REENTRY_ACTION_INVALID', action)
        score_rows = score_actions859(env, memx, review_pre, review_segments, env['REVIEW_SUFFIX851'])
        assert [row['spelling'].strip() for row in score_rows] == ['CONTINUE', 'REVISE', 'STOP']
        scores = {row['spelling'].strip(): row for row in score_rows}
        revision = None
        if action == 'REVISE':
            revision_segments = [(env['C_SLOT851'], c_state), (env['K_SLOT851'], review['rows']),
                (env['E_SLOT851'], e_state), (env['U_SLOT852'], u_state), (env['R_SLOT852'], r_state)]
            revision = env['gen851'](memx, recompute_pre, revision_segments, env['ANSWER_SUFFIX851'])
            check_output_h863(revision, 'REENTRY_REVISION_INVALID')
        assert physical_seal863(env, memx) == before_seal, 'MEMORY_SEAL_CHANGED_DURING_REENTRY'
        states = {'C': c_state, 'E': e_state, 'U': u_state, 'R': r_state,
            'K0': k0, 'J': j_state, 'Kprev': previous_review['rows'],
            'Review': review['rows'], 'Revision': None if revision is None else revision['rows']}
        pre_inv = {'segments': pre_segments, 'h': pre_h}
        review_inv = {'segments': review_segments, 'h': review}
        transfers = [
            transfer864(env, 'C', 'REENTRY_PRECONTROL', c_state, env['C_SLOT851'], pre_inv,
                source_stage='experimental_candidate'),
            transfer864(env, 'E', 'REENTRY_PRECONTROL', e_state, env['E_SLOT851'], pre_inv,
                source_stage='experimental_evidence'),
            transfer864(env, 'U', 'REENTRY_PRECONTROL', u_state, env['U_SLOT852'], pre_inv,
                source_stage='experimental_coverage'),
            transfer864(env, 'R', 'REENTRY_PRECONTROL', r_state, env['R_SLOT852'], pre_inv,
                recompute=lambda: env['relation852'](c_state, e_state), source_stage='experimental_candidate_evidence'),
            transfer864(env, 'Kprev', 'REENTRY_PRECONTROL', previous_review['rows'], env['K_SLOT851'], pre_inv,
                source_stage='original_cycle1_review', source_execution='ORIGINAL_NATIVE'),
            transfer864(env, 'K0', 'REENTRY_REVIEW', k0, env['K_SLOT854'], review_inv,
                source_stage='experimental_precontrol'),
            transfer864(env, 'J', 'REENTRY_REVIEW', j_state, env['J_SLOT854'], review_inv,
                recompute=lambda: env['interaction854'](c_state, e_state, k0), source_stage='experimental_precontrol')]
        if revision is not None:
            revision_inv = {'segments': revision_segments, 'h': revision}
            for name, slot in (('C', env['C_SLOT851']), ('E', env['E_SLOT851']),
                    ('U', env['U_SLOT852']), ('R', env['R_SLOT852'])):
                transfers.append(transfer864(env, name, 'REENTRY_REVISION', states[name],
                    slot, revision_inv, source_stage='experimental_review'))
            transfers.append(transfer864(env, 'Review', 'REENTRY_REVISION', review['rows'],
                env['K_SLOT851'], revision_inv, source_stage='experimental_review'))
        qrow = env['worlds829'][env['QID841'].index(job['qid'])]
        sufficient = bool(evidence_sufficient862(env, job, mount))
        reason = 'SUFFICIENT' if sufficient else 'MISSING_REQUIRED_RELATION'
        correct = bool(env['node851'](candidate['text'].strip(), qrow) == 'end')
        supported = bool(env['supported851'](candidate['text'].strip(), qrow, set(mount)))
        grounded = correct and sufficient and supported
        aligned = bool(action == 'CONTINUE' and grounded)
        completion = {'classification': 'EXPERIMENTAL_ADAPTER_ASSISTED_COMPLETION',
            'observed': aligned, 'native_autonomous': False}
        quality = {'candidate_correct_for_task': correct, 'supported_final_answer': supported,
            'sufficient_evidence': sufficient}
        score_margin = scores['CONTINUE']['sequence_logp'] - max(
            scores['REVISE']['sequence_logp'], scores['STOP']['sequence_logp'])
        result.update({'status': 'REENTRY_EVALUATED', 'numeric_reentry': True,
            'hop0': env['result849'](hop0), 'candidate': env['result849'](candidate),
            'evidence': env['result849'](evidence), 'coverage': env['result849'](coverage),
            'resolution': None,
            'states': {name: state863(env, value) for name, value in states.items()},
            'review': env['result849'](review), 'review_scores': score_rows, 'score_margin': score_margin,
            'action': action, 'revision': None if revision is None else env['result849'](revision),
            'transfers': transfers, 'offline': {'candidate_correct': correct,
                'supported_answer': supported, 'evidence_sufficient': sufficient,
                'evidence_reason': reason, 'grounded_answer': grounded,
                'C1E1': correct and sufficient, 'aligned_continue': aligned,
                'quality_metrics': quality},
            'completion': completion,
            'adapter_assisted_not_native_autonomous': True,
            'one_adapter_evaluation_only': True})
        STATE864['memory_reentry'][control_name] = result
        STATE864['xray'][control_name] = {'control': control_name,
            'execution': result['execution'], 'states': result['states'],
            'transfers': transfers, 'scores': score_rows, 'action': action,
            'offline': result['offline'], 'completion': completion}
        table864('H PHYSICAL REENTRY', job=job['job'], cycle='ADAPTER1',
            execution=result['execution'], cartridge=selected, decision=action,
            payload={'mounted': True, 'tokens': layout['tokens'], 'candidate': candidate['text'].strip(),
                'offline': result['offline'], 'completion': completion})
        table864('I CANDIDATE DECISION XRAY', job=job['job'], cycle='ADAPTER1',
            execution=result['execution'], cartridge=selected, decision=action,
            payload=STATE864['xray'][control_name])
        return result
    except Exception as exc:
        result.update({'status': 'MEMORY_REENTRY_NOT_SUPPORTED' if not result['mounted'] else 'REENTRY_FAILED',
            'error': type(exc).__name__ + ': ' + str(exc), 'traceback': traceback.format_exc(),
            'numeric_reentry': False})
        STATE864['memory_reentry'][control_name] = result
        table864('H PHYSICAL REENTRY', job=job['job'], cycle='ADAPTER1',
            execution=result['execution'], cartridge=selected, integrity='FAIL', payload=result)
        return result
    finally:
        if memx is not None:
            del memx
            env['release']()
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


def interpretation864(env, native, pool, search, ranking, reentry, intact_search):
    main_search = search.get('REMOVED', {})
    decision = main_search.get('decision', {})
    query = main_search.get('query', {})
    ranking_main = ranking.get('MAIN', {})
    main_reentry = reentry.get('MAIN', {})
    offline = main_reentry.get('offline', {})
    completion = main_reentry.get('completion', {})
    native_closure = native_closure862(env)
    native_autonomous = any(x['native_autonomous_correction_closure'] for x in native_closure)
    native_conclusion = native.get('analysis', {}).get('conclusion', {})
    removed_jid = next(job['job'] for job in env['JOBS841'][:2] if job['intervention'] == 'REMOVED')
    classes = []
    if query.get('status') == 'MODEL_NATIVE_SEARCH_SIGNAL': classes.append('MODEL_NATIVE_SEARCH_SIGNAL')
    if decision.get('action') == 'SEARCH': classes.append('MODEL_NATIVE_SEARCH_DECISION')
    if ranking_main: classes.append('ORACLE_FREE_MEMORY_ADDRESSING')
    if main_reentry.get('mounted'): classes.append('PHYSICAL_MEMORY_LOAD')
    if main_reentry.get('numeric_reentry'): classes.append('NUMERICAL_MEMORY_REENTRY')
    if offline.get('candidate_correct'): classes.append('NEW_CORRECT_CANDIDATE')
    if offline.get('aligned_continue'): classes.append('EVIDENCE_ALIGNED_ADAPTER_DECISION')
    if completion.get('observed'): classes.append('EXPERIMENTAL_ADAPTER_ASSISTED_COMPLETION')
    if native_autonomous: classes.append('NATIVE_AUTONOMOUS_CLOSED_LOOP_COMPLETION')
    if decision.get('action') == 'SEARCH' and not query: classes.append('SEARCH_SIGNAL_UNRESOLVED')
    if main_reentry.get('status') == 'CARTRIDGE_FORMAT_INCOMPATIBLE': classes.append('CARTRIDGE_FORMAT_INCOMPATIBLE')
    if main_reentry.get('status') == 'MEMORY_REENTRY_NOT_SUPPORTED': classes.append('MEMORY_REENTRY_NOT_SUPPORTED')
    if not classes: classes.append('UNRESOLVED')
    gates = {
        'A_MODEL_SEARCH_SIGNAL': bool(query),
        'B_REAL_SEARCH_DECISION': decision.get('action') == 'SEARCH',
        'C_ORACLE_FREE_ADDRESSING': bool(ranking_main),
        'D_PHYSICAL_CARTRIDGE_LOAD': bool(main_reentry.get('mounted')),
        'E_NUMERICAL_REENTRY': bool(main_reentry.get('numeric_reentry')),
        'F_NEW_CORRECT_CANDIDATE': bool(offline.get('candidate_correct')),
        'G_EVIDENCE_ALIGNED_DECISION': bool(offline.get('aligned_continue')),
        'H_ORIGINAL_NATIVE_AUTONOMOUS_CLOSURE': native_autonomous}
    hypotheses = {
        'H1_SEARCH_SIGNAL_NATIVE': {'observed': gates['A_MODEL_SEARCH_SIGNAL'], 'evidence': query.get('provenance')},
        'H2_SEARCH_DECISION_NATIVE': {'observed': gates['B_REAL_SEARCH_DECISION'], 'action': decision.get('action')},
        'H3_ADDRESSING_ORACLE_FREE': {'observed': gates['C_ORACLE_FREE_ADDRESSING'], 'top1_correct': ranking_main.get('top1_correct')},
        'H4_PHYSICAL_LOAD': {'observed': gates['D_PHYSICAL_CARTRIDGE_LOAD'], 'selected': main_reentry.get('selected')},
        'H5_NUMERICAL_REENTRY': {'observed': gates['E_NUMERICAL_REENTRY'], 'layout': main_reentry.get('memory_layout', {})},
        'H6_CORRECT_CANDIDATE': {'observed': gates['F_NEW_CORRECT_CANDIDATE'], 'offline': offline},
        'H7_NATIVE_AUTONOMOUS_CLOSURE': {'observed': gates['H_ORIGINAL_NATIVE_AUTONOMOUS_CLOSURE'],
            'adapter_completion_cannot_count': True, 'native_closure862': native_closure}}
    answers = {
        '1_FIRST_MISSING_NATIVE_STAGE': native_conclusion.get('first_missing_transition', {}).get(removed_jid),
        '2_ORIGINAL_REMOVED_ACQUIRES_EVIDENCE': STATE863['memory'][removed_jid]['new_evidence_discovered_any_cycle'],
        '3_ORIGINAL_REMOVED_NEW_CORRECT_CANDIDATE': STATE863['candidates'][removed_jid]['native_correct_candidate_reached'],
        '4_NATIVE_QUERY_SOURCE': query.get('provenance', 'UNRESOLVED'),
        '5_REAL_SEARCH': decision.get('action') == 'SEARCH',
        '6_ADDRESSING': 'ORACLE_FREE_MEMORY_ADDRESSING' if ranking_main else 'UNRESOLVED',
        '7_CARTRIDGE_PHYSICAL': main_reentry.get('status', 'NOT_RUN'),
        '8_NUMERICAL_REENTRY': main_reentry.get('status', 'NOT_RUN'),
        '9_NEW_CORRECT_CANDIDATE': offline.get('candidate_correct', False),
        '10_ALIGNED_DECISION': offline.get('aligned_continue', False),
        '11_ADAPTER_COMPLETION': completion,
        '12_NATIVE_AUTONOMOUS_CLOSURE': native_closure,
        '13_NO_SEARCH_CONTROL': native.get('records', {}).get('REMOVED', {}).get('cycles', []),
        '14_FINAL_CLASSIFICATION': classes}
    result = {'scope': 'PILOT_ONLY_ONE_WORLD_TWO_ORIGINAL_JOBS', 'classes': classes,
        'gates': gates, 'hypotheses': hypotheses, 'answers': answers,
        'original_native': {'INTACT_search_probe': intact_search,
            'REMOVED_cycles': native.get('records', {}).get('REMOVED', {}).get('cycles', []),
            'native_closure862': native_closure},
        'adapter_levels': {'search_and_address': 'LEVEL_B_EXPERIMENTAL_MEMORY_ACCESS_ADAPTER',
            'mount_and_reentry': 'LEVEL_C_EXPERIMENTAL_CLOSED_LOOP_REENTRY'},
        'native_autonomous_claim': False,
        'adapter_assisted_claim': bool(completion.get('observed')),
        'model_roles': ['SEARCH/ANSWER/DROP/STOP literal decision', 'soft-row address query',
            'new candidate', 'evidence/coverage', 'Review/Revision'],
        'python_roles': ['locked H3/PEAK50 addressing', 'SHA verification', 'SSD read',
            'numeric mount', 'offline evaluation'],
        'prohibitions': {'oracle_routing': False, 'answer_override': False,
            'forced_STOP': False, 'forced_CONTINUE': False, 'forced_REVISE': False,
            'card_substitution': False, 'text_replay': False, 'training': False}}
    STATE864['interpretation'] = result
    return result


def run_experiment864(env, native, analysis):
    original_record_sha = records_digest861(env)
    records = env['REC841']
    assert len(records) == 2
    jobs = {job['intervention']: job for job in env['JOBS841'][:2]}
    restores = STATE863['restores']
    assert len(restores) == 3 and all(row['exact'] for row in restores), 'EXACT_RESTORE_864_FAILED'
    STATE864['restores'] = restores
    STATE864['negative_controls']['EXACT_RESTORE'] = restores
    removed_record = records[jobs['REMOVED']['job']]
    STATE864['negative_controls']['NO_SEARCH_ORIGINAL'] = {
        'execution': 'ORIGINAL_NATIVE', 'record': removed_record,
        'native_evidence_acquired': False, 'adapter_completion': False}
    native_motor_map864(env)
    pool = adapter_pool864(env)
    intact_job, removed_job = jobs['INTACT'], jobs['REMOVED']
    intact_action, intact_search = search_decision864(env, RUNTIME863[intact_job['job']], intact_job)
    STATE864['search_signals']['INTACT'] = {'decision': intact_search,
        'status': 'CONTROL_ACTION_ONLY_NO_QUERY_NO_MOUNT'}
    removed_query_h, qr, removed_search = model_search864(env, RUNTIME863[removed_job['job']], removed_job)
    STATE864['search_signals']['REMOVED'] = removed_search
    reentry = {}
    if removed_search['decision']['action'] == 'SEARCH':
        assert qr is not None
        chosen_route, main_ranking = route_and_rank864(env, qr, pool)
        reentry['MAIN'] = reentry864(env, removed_job, RUNTIME863[removed_job['job']],
            chosen_route['chosen'], 'MAIN')
    else:
        STATE864['ranking']['MAIN'] = {'status': 'NOT_RUN_NO_MODEL_SEARCH',
            'execution': 'LEVEL_B_EXPERIMENTAL_MEMORY_ADAPTER'}
    reentry['IRRELEVANT_CARTRIDGE'] = reentry864(env, removed_job, RUNTIME863[removed_job['job']],
        pool['irrelevant_control'], 'IRRELEVANT_CARTRIDGE')
    STATE864['negative_controls']['IRRELEVANT_CARTRIDGE'] = reentry['IRRELEVANT_CARTRIDGE']
    STATE864['negative_controls']['SHUFFLED_ADDRESSING'] = STATE864['ranking'].get('SHUFFLED_ADDRESSING',
        {'status': 'NOT_RUN_NO_MODEL_SEARCH'})
    STATE864['negative_controls']['MISSING_TARGET'] = STATE864['ranking'].get('MISSING_TARGET',
        {'status': 'NOT_RUN_NO_MODEL_SEARCH'})
    native_package = {'records': {'INTACT': records[intact_job['job']], 'REMOVED': removed_record},
        'sequences': native, 'analysis': analysis}
    STATE864['native'] = native_package
    result = interpretation864(env, native_package, pool, STATE864['search_signals'], STATE864['ranking'],
        reentry, intact_search)
    assert records_digest861(env) == original_record_sha, 'ORIGINAL_NATIVE_RECORD_CHANGED'
    assert env['MAX_REVIEWS851'] == 2, 'REVIEW_LIMIT_CHANGED'
    return result


def partial_report864():
    return {'test': 864, 'kind': TEST864_KIND, 'status': 'INCOMPLETE',
        'execution_scope': 'ORIGINAL_NATIVE_PLUS_EXPERIMENTAL_ADAPTER',
        'source_audit': STATE864['source_audit'], 'native': STATE864['native'],
        'two_job_verification': TWO_JOB_VERIFICATION864,
        'native_regression': NATIVE_REGRESSION864,
        'search_signals': STATE864['search_signals'], 'ranking': STATE864['ranking'],
        'negative_controls': STATE864['negative_controls'],
        'memory_reentry': STATE864['memory_reentry'],
        'candidate_decision_xray': STATE864['xray'],
        'interpretation': STATE864['interpretation'], 'error': EXECUTION_ERROR864,
        'traceback': TRACEBACK864}


def finalize864(success=False):
    global EXECUTION_ERROR864
    report = partial_report864()
    source_present = (ROOT864 / '864.py').is_file()
    technical = {'gate0_49_source_locks': len(STATE864['source_audit'].get('locks', [])) == 49,
        'gate1_original_spine': STATE863.get('spine_loaded', False),
        'gate2_original_native_two_jobs': len(STATE864['native'].get('records', {})) == 2,
        'gate3_exact_restore': bool(STATE864['restores']) and all(x['exact'] for x in STATE864['restores']),
        'gate4_experiment_completed': success,
        'gate5_source_present': source_present}
    report['technical_gates'] = technical
    report['status'] = 'TEST864_TECHNICAL_EXECUTION_COMPLETE' if success and all(technical.values()) else 'UNRESOLVED'
    report['scientific_scope'] = 'PILOT_ONLY; adapter-assisted completion is not native autonomous closure.'
    report['adapter_is_native_autonomous'] = False
    report['analysis'] = ANALYSIS864
    report['error'] = EXECUTION_ERROR864
    report['traceback'] = TRACEBACK864
    json_write864('864_report.json', report)
    json_write864('864_source_audit.json', STATE864['source_audit'])
    json_write864('864_cartridge_inventory.json', STATE864['inventory'])
    json_write864('864_search_signals.json', STATE864['search_signals'])
    json_write864('864_address_ranking.json', STATE864['ranking'])
    json_write864('864_negative_controls.json', STATE864['negative_controls'])
    json_write864('864_memory_reentry.json', STATE864['memory_reentry'])
    json_write864('864_candidate_decision_xray.json', STATE864['xray'])
    names = ['864.py', '864.log', '864_report.json', '864_source_audit.json',
        '864_cartridge_inventory.json', '864_search_signals.json', '864_address_ranking.json',
        '864_negative_controls.json', '864_memory_reentry.json', '864_candidate_decision_xray.json']
    manifest = {}
    LOG_FILE864.flush()
    for name in names:
        path = ROOT864 / name
        if path.is_file():
            manifest[name] = {'bytes': path.stat().st_size, 'sha256': sha256_file864(path)}
        else:
            manifest[name] = {'status': 'NOT_AVAILABLE'}
    json_write864('864_sha256_manifest.json', manifest)
    return report, manifest


try:
    table864('A BEGIN', payload={'test': 864, 'root': str(ROOT864)})
    load_sources864()
    feasibility_audit864()
    source_ok = capture_cell_source864()
    table864('A SOURCE CAPTURE', integrity='PASS' if source_ok else 'FAIL', payload={'saved': source_ok})
    load_spine864()
    env864, original_error864, original_trace864, reproduction_evidence864 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace864
    table864('B ENVIRONMENT', payload=reproduction_evidence864)
    jobs864 = verify_two_job859(env864, original_trace864)
    TWO_JOB_VERIFICATION864 = jobs864
    table864('B PANEL', payload=jobs864)
    assert_hook_free859(env864, 'TEST864_before_native_regression')
    install_offline_evaluator859(env864)
    native864 = native_sequences860(env864)
    NATIVE_REGRESSION864 = native_regression864(env864, native864)
    table864('B NATIVE REGRESSION', payload=NATIVE_REGRESSION864)
    ANALYSIS864 = run_analysis863(env864, native864)
    STATE864['analysis'] = ANALYSIS864
    table864('J FIRST MISSING STAGE', payload=ANALYSIS864['conclusion']['first_missing_transition'])
    result864 = run_experiment864(env864, native864, ANALYSIS864)
    table864('K NEGATIVE CONTROLS', execution='DIAGNOSTIC_ONLY',
        payload={k: {'status': v.get('status', 'RECORDED') if isinstance(v, dict) else 'RECORDED'}
            for k, v in STATE864['negative_controls'].items()})
    table864('L EXECUTION SCOPE', payload={'original': 'LEVEL_A_LOCKED_ORIGINAL_MOTOR',
        'adapter': 'LEVEL_B_AND_C_EXPERIMENTAL', 'native_autonomous': False})
    table864('M FINAL CLASSIFICATION', payload=result864)
    table864('N NEXT MISSING STAGE', payload={'next': result864['answers']['1_FIRST_MISSING_NATIVE_STAGE'],
        'adapter_completion_not_native_closure': True})
    success864 = True
    short864('TEST864 TECHNICAL EXECUTION_COMPLETE')
    short864('TEST864 SCIENTIFIC PILOT_ONLY', json.dumps(result864, ensure_ascii=False))
    finalize864(True)
except Exception as exc:
    EXECUTION_ERROR864 = type(exc).__name__ + ': ' + str(exc)
    TRACEBACK864 = traceback.format_exc()
    print(TRACEBACK864, file=ERROR_CONSOLE864, flush=True)
    short864('TEST864 FULL TRACEBACK', TRACEBACK864)
    short864('TEST864 INCOMPLETE', EXECUTION_ERROR864)
    finalize864(False)
finally:
    LOG_FILE864.close()
