# AKBASCORE SILICON HIPPOCAMPUS — TEST866 MODEL-NATIVE RECURSIVE PHYSICAL-EVIDENCE CONTROLLER (FINAL)
# Locked TEST865 physical engine (865.py verbatim below the console-capture block) + one model-native recursive controller (loop866).
# Model: every transition word, every ACQUIRE/REJECT address (own node-name soft rows), every ACCEPT/STOP.
# Python: strict word parse, pointer stack, PEAK50 route, SHA SSD I/O, CUT3 mount; horizon/budget ends (labelled).
# Offline labels: condition construction before execution and scoring after execution only (AST firewall audited).
# GPU EXECUTION NOT VERIFIED BY THE AUTHOR. Static/CPU checks only; results exist only after the team runs it on an A100.
# ===================== CELL CONSOLE CAPTURE — START (I/O only; no effect on the experiment) =====================
# Every character this cell prints (stdout and stderr, including the engine and tracebacks) is ALSO written,
# line-buffered, to /content/TEST866_HUCRE_CIKTISI_<stamp>.txt while it is printed. If Google Drive can be mounted,
# that file and 866.log are copied to MyDrive/TEST866_<stamp>/ every 5 minutes, so a sleeping phone or a lost
# browser connection cannot erase the cell output. The end block (bottom of this cell) downloads everything.
import sys as _cc_sys, os as _cc_os, time as _cc_time, shutil as _cc_shutil, threading as _cc_threading, glob as _cc_glob
CC_DRIVE_BACKUP = True                    # False -> no Google Drive copy (the local file and downloads still work)
CC_STAMP = _cc_time.strftime('%Y%m%dT%H%M%SZ', _cc_time.gmtime())
CC_PATH = '/content/TEST866_HUCRE_CIKTISI_%s.txt' % CC_STAMP
_cc_os.makedirs('/content', exist_ok=True)
CC_FILE = open(CC_PATH, 'w', encoding='utf-8', errors='replace', buffering=1)


class CellConsoleTee:
    def __init__(self, stream):
        self._stream = stream

    def write(self, text):
        result = self._stream.write(text)
        try:
            CC_FILE.write(text if isinstance(text, str) else bytes(text).decode('utf-8', 'replace'))
        except Exception:
            pass
        return result

    def flush(self):
        self._stream.flush()
        try:
            CC_FILE.flush()
        except Exception:
            pass

    def __getattr__(self, name):
        return getattr(self._stream, name)


CC_ORIGINAL = (_cc_sys.stdout, _cc_sys.stderr)
_cc_sys.stdout, _cc_sys.stderr = CellConsoleTee(_cc_sys.stdout), CellConsoleTee(_cc_sys.stderr)
CC_DRIVE_DIR = None
if CC_DRIVE_BACKUP:
    try:
        from google.colab import drive as _cc_drive
        _cc_drive.mount('/content/drive')
        CC_DRIVE_DIR = '/content/drive/MyDrive/TEST866_%s' % CC_STAMP
        _cc_os.makedirs(CC_DRIVE_DIR, exist_ok=True)
    except Exception as _cc_exc:
        print('CELL CONSOLE CAPTURE: Google Drive backup not available (%s: %s); local capture continues.'
              % (type(_cc_exc).__name__, _cc_exc))
        CC_DRIVE_DIR = None
CC_STOP = _cc_threading.Event()


def cc_backup_now():
    if CC_DRIVE_DIR is None:
        return
    try:
        CC_FILE.flush()
        _cc_shutil.copy2(CC_PATH, CC_DRIVE_DIR)
        for folder in sorted(_cc_glob.glob('/content/TEST866_MODEL_NATIVE_CONTROL_*'))[-1:]:
            if _cc_os.path.isfile(folder + '/866.log'):
                _cc_shutil.copy2(folder + '/866.log', CC_DRIVE_DIR + '/866.log')
    except Exception:
        pass


def cc_backup_loop():
    while not CC_STOP.wait(300):
        cc_backup_now()


_cc_threading.Thread(target=cc_backup_loop, daemon=True).start()
print('CELL CONSOLE CAPTURE START', CC_STAMP, '->', CC_PATH, '| Drive backup:', CC_DRIVE_DIR)
# ===================== CELL CONSOLE CAPTURE — the TEST866 experiment follows unchanged =====================
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
    '700.log': 'fcf6c82aed7384a32279e84bfadf102a76f110b2',
    '700_qwen.72b.py': '9862cd80ac27ad28f3daacbb180545cd20df7913',
    '721.log': '45d852b725d34d09711f4d5b5922444098e337cb',
    '721.py': '7c6575beddca87f02c344ee1a132f02b191dc00a',
    '730.py': 'b1bad9eb3b111b44413f8ef05a3a140ab66a77dd',
    '757.log': '8c0899369a01ad5c4fc22dd5124b4ddd41125ddb',
    '757.py': '3d88bf8638390995858f23391f1e043faa586835',
    '759.log': 'c33ec387761dab07563edda3d635038d80867f00',
    '759.py': '273827a86c569a0e06cae88fe3909bf7bb2bea58',
    '779.log': 'a12ece7011b0db2629f18f2eafa8b01c4dd3f3a3',
    '779.py': 'fa7017a87f25ecef6ed2b2954a850599cb25fcd9',
    '785.log': 'd319098c747dbc13a74eb361e43829d34075081e',
    '785.py': 'dfb5f7869efd50bf2c202723286eb7876338af86',
    '834.py': 'ab7b2046d7b7e7be18aed8c6ce5a1397e0c991d7',
    '835.log': 'bfad088c81666674b766c3de95f08e0ab00f4817',
    '835.py': '9327cebc651f173fd547362825679a1a790fcd6b',
    '840.log': 'beaeedccf8dc469ee17e5802e242c7750f91bf2d',
    '840.py': '06bc63ddcda9c11780bd99a7dd58f00f57b80f0e',
    '841.log': '4c22215bde9f169c0566f90a77ac7904d43d1566',
    '841.py': '135b18e5b1ea113579c607cf9eecf49628cf18c2',
    '842.log': 'f6406b0e3525ff2f22cea1464a175c61bf2c2936',
    '842.py': '4653fe9a5dd7bc2dd3a72f25bed00ceebb3936fd',
    '844.log': '83b9e39d5e5062725c7dd74d96640289b22de3f3',
    '844.py': '783dbca9ebab722a0a5826aa708c4f152f8d7ad7',
    '845.log': '09fb3696f44265a57b037669d77e4236eb0fe788',
    '845.py': 'be81a587b3d2b8cd3e9291df6bd9fb481c4c2164',
    '846.log': 'f8123c76f7e37700eaa0cb6349dfee87a72912c4',
    '846.py': '6093896b7e4492f201cece448ad1646b0bd8820a',
    '847.log': '7cb3bf61e76da83211800053e489e2826a1c68de',
    '847.py': '72ce35daa728f546d92baa26705dd04ed5ad6a11',
    '848.log': 'c744910f49f47daed76f49f6d5e35069da30d2e7',
    '848.py': '3876661dca29f282b626eb81068b9c1a21797fe0',
    '849.log': '573ba54e45b648c44c376e362ae69bb2fdc5a788',
    '849.py': '01a6ac43cbc954cc2f6ceaf8cf0238333ec762b1',
    '850.log': 'c070ef432e95f80cd9a1c28318fd2e4a10377296',
    '850.py': '79cc5ab211c01b37324e2d6897a298e84db42101',
    '851.log': 'b38419ef3a069ea4e20d43d15e6d939318083a9a',
    '851.py': '0f01e73b9ad160c988cfe059e8b5ae5e1f35f65b',
    '852.log': 'b434a1e36b22fd99f9590c8b98b8094e927db458',
    '852.py': '4174e9241f773d6a031c51296b6beb11d4637aa5',
    '853.log': '0bfa9104337c44adaf4a07ec0ce6b5e41f457494',
    '853.py': 'a7033caa10fdb86f8f0ee0b8ed1a0ac7514e26be',
    '854.log': '2aa1f85e14d52acbd1ecbad5b5c7df10df0bbcd4',
    '854.py': 'a158d92a61c15a5e71468146d6c1ceeaedce436c',
    '855.log': 'afb58577e700031a4f788940ab4b8e7a69b59999',
    '855.py': '8ab79676aded54cb30316c47feeeae8b89fb4625',
    '856.log': '875a1d5fb3ad5c45700c4ebab17402a3c9b27bb3',
    '856.py': '93d7e9bd7ebc6c692cef0e1e62d05ad96e4086d1',
    '857.log': 'ef3ae882ecf03dd9b9668939bd55ce65eeae8455',
    '857.py': '0891ffe2d638e7a17ff9e851d160c2afeb609a1a',
    '858.log': '6c3ab3e9a5887c2d90cf5f55c9ef55f2d7249209',
    '858.py': 'f78efd24b2fd6dfd2072933f2e99382a50422ceb',
    '859.log': 'b080c81d4fdcc1be0e5a11df500abfb6d7b98707',
    '859.py': '0c7cb37e2dff71e6f1798362a4e3ebee12c71ae9',
    '860.log': '3eac77232332b944960fdf3a40cac2cbfa38c282',
    '860.py': 'd352c7f993f30685ef366e5008eac7c5a45cc9e2',
    '861.log': '2e57ff2f20db600350c41ba7c7b4add3b2b11924',
    '861.py': '4c61c1f021c92b3f701220a10f0927c8b2d89c3b',
    '862.log': '91980c52bc5b98bee3c94cce67756093ace9a6a0',
    '862.py': '40857dd575041ebbee02879da92a98755c7686e4',
    '863.log': '9cb413320c5fb59cb3e06e81570cd62d070f920e',
    '863.py': '9c0bf68f19df1327390d973c3a5e85b2694a439d',
    '864.log': 'd78e170f6c38425e08d525e7f0ee0d44f74395c4',
    '864.py': '42b0b3a42584da67f5b93ede8608d1116ffa249c',
    'v2/560.log': 'b56cb2a16b4a8928705e6a6e24e07983d4849b74',
    'v2/560.py': '35d95a929a4e043a9af346c67fc103da47a792b5',
    'v2/575.log': '55647630d4a0fcf37f35e3f6f3da07a01789d64f',
    'v2/575.py': '569c92c61224ea408cdb6e81dbe45dde06dc05fd',
    'v2/596.log': '192f13722e504167e5c28c1641c5d8a1ece1118c',
    'v2/596.py': '85067b4f1cd0a1a941c0b88752f813360600c6b1',
}
BLIND_SEED864 = 8642026
SHUFFLE_CONTROL_SEED864 = 8642027
TOPK864 = (1, 3, 5)
SEARCH_FRAME864 = 'A'
SEARCH_QUERY_PROTOCOL864 = 'STATE_CONDITIONED_GEN851_SOFT_ROWS_TO_TEST841_H3_PEAK50'
ABSTENTION_PROTOCOL864 = 'NOT_SUPPORTED_LOCKED_ROUTE841_ALWAYS_SELECTS_TOP1'
ADAPTER_REENTRY_EVALUATIONS864 = 1
STAMP864 = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
ROOT864 = pathlib.Path('/content') / ('TEST866_MODEL_NATIVE_CONTROL_' + STAMP864)
ROOT864.mkdir(parents=True, exist_ok=False)
CONSOLE864, ERROR_CONSOLE864 = sys.stdout, sys.stderr
LOG_FILE864 = open(ROOT864 / '866.log', 'w', encoding='utf-8')
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





# ============================ TEST865 UNIFIED CONNECTOR ============================
# The locked TEST864/863 definitions above are loaded, not their experiment tails.
# New code only connects verified native hop, H3/PEAK50, physical mount and review calls.
import csv
import inspect
import math
import os
import shutil



# ======================================================================================================================
# TEST865 — PRE-REGISTRATION (fixed in code before any model call; never edited after looking at data)
# ======================================================================================================================
TEST865_KIND = 'NATIVE_POINTER_PHYSICAL_REENTRY_UNIFIED_MOTOR'
RANDOM_SEED865 = 8652027
SHUFFLE_SEED865 = 8652028
CAUSAL_WORLDS865 = tuple(range(9))            # blocks 0-2; worlds 0/1 were the 849-864 pilot worlds
HELD_OUT_WORLDS865 = (9, 10, 11)              # block 3; never used by 849-864 jobs or by this code's design
ALL_WORLDS865 = CAUSAL_WORLDS865 + HELD_OUT_WORLDS865
PANEL_CONDITIONS865 = ('LIVE', 'REMOVED')     # LIVE=[first]; REMOVED=[first, fork] (864/863 memory, target in pool)
LOOP_CONDITIONS865 = ('LIVE', 'REMOVED', 'HOP3', 'MISSING')
LOOP_ARMS865 = ('NATIVE_P', 'NO_ACQUISITION', 'RANDOM_QUERY')
TRAP_CONTROLS865 = ('REVERSED_EDGE', 'SHARED_NODE', 'DECOY', 'MISSING_TARGET')
S_LIMIT865 = 3                                # TEST845 SMAX845: cards per hop
MAX_HOPS865 = 14                              # TEST845 HMAX845: hop computations per loop
MAX_CARDS865 = 5                              # TEST845 CAP845: mounted cards
MAX_REVIEWS865 = 2                            # identical to locked MAX_REVIEWS851
CALL_ALLOWANCE865 = 8000                      # gen849/gen851/score calls granted to TEST865 stages (mechanical)
TEST865_MINUTES = 180.0                       # wall budget of TEST865 stages; afterwards remaining units = NOT_RUN_BUDGET
ALPHA865 = 0.05
PREREG865 = {
    'unit_of_analysis': 'world x condition item; paired arms share item, memory, pool and pointer',
    'address_target': 'any pool card whose directed relation SOURCE equals the true current node (TEST845 '
                      'MODEL_DERIVED_ADDRESS rule); for LIVE/REMOVED hop>=1 the current node is the world middle node',
    'H1_address_P': {'population': 'causal worlds 0-8 x LIVE,REMOVED (n=18), intention-to-treat: missing/invalid P = miss',
                     'metric': 'hit@1 of P-route in valid source-match set', 'threshold': 0.75},
    'H2_address_over_controls': {'metric': 'hit@1(P) - max(hit@1 CUE_QUESTION_ONLY, RANDOM_NORM_MATCHED, SHUFFLED_KEYS)',
                                 'threshold': 0.40, 'paired_sign_test_two_sided_max_p': ALPHA865},
    'H3_donor_follow': {'population': 'items with valid own and donor P', 'metric': 'donor P routes into donor valid set',
                        'threshold': 0.75, 'min_n': 9},
    'ADDRESS_CAUSAL_EFFECT': 'H1 and H2 and H3',
    'H4_physical_integrity': 'every TEST865 mount: tensor/file SHA, n == P+sum(body), prefix seals, exact restore; 100 percent',
    'H5_candidate_correction': {'population': 'causal items (n=18), ITT', 'metric': 'supported correct re-hop after P mount',
                                'threshold': 0.75, 'minus_random_mount_threshold': 0.40,
                                'paired_sign_test_two_sided_max_p': ALPHA865},
    'H6_closure': {'population': 'NATIVE_P loops, causal worlds x LIVE,REMOVED,HOP3 (n=27), ITT',
                   'metric': 'MODEL_ACCEPT of a supported correct answer', 'threshold': 0.50,
                   'minus_NO_ACQUISITION_threshold': 0.30, 'minus_RANDOM_QUERY_threshold': 0.30,
                   'paired_sign_test_two_sided_max_p': ALPHA865},
    'H7_false_acceptance': 'MISSING loops + trap singletons + missing-target mounts: measured, no pass threshold, '
                           'prior evidence (845/846P/847) predicts high trap acceptance',
    'H8_native_stop': 'literal review STOP after >=1 real acquisition attempt: counted, report only',
    'held_out': 'worlds 9-11 reported separately for every hypothesis; report only (n too small for a threshold)',
    'claim_gating': 'H5/H6/NATIVE_AUTONOMOUS_CLOSURE claimable only if ADDRESS_CAUSAL_EFFECT and H4 pass; '
                    'all stages always execute blind; gates are applied to claims, never to runtime control flow',
    'uncertainty': 'Wilson 95 percent intervals; exact two-sided binomial sign tests on discordant pairs',
    'loop_law': 'TEST845: node -> advance; UNKNOWN -> P addresses a card; UNKNOWN after mount -> unmount; S failed cards '
                '-> dead end -> retract previous hop evidence (attribution by NULL substitution if it was initial) '
                'and backtrack; dead end at root or unretractable -> terminal review on the UNKNOWN candidate',
    'review_law': 'locked BASELINE853 review junction; CONTINUE -> MODEL_ACCEPT; STOP -> MODEL_STOP; REVISE -> new '
                  'P-addressed acquisition for the last hop (NATIVE_P/RANDOM_QUERY) or same-memory native revision '
                  '(NO_ACQUISITION); acquisition exhausted -> mechanical end, never STOP',
    'review_ablation': 'diagnostic {C,E,(K),U} precontrol -> K0-only review at every terminal review; never used for control',
}
PREREG_SHA865 = sha256_bytes864(json.dumps(PREREG865, sort_keys=True).encode('utf-8'))
OFFLINE_NAMES865 = {'worlds829', 'CONTENT841', 'EVALKEY841', 'card_meta829', 'NAMES841', 'REL841', 'cards829',
                    'questions829', 'node851', 'supported851', 'evidence_sufficient862', 'OFFLINE865'}
STATE865 = {'source': {}, 'gates': {}, 'root': [], 'pointer': [], 'addressing': [], 'physical': [], 'traps': [],
            'loops': [], 'hypotheses': {}, 'classes': {}, 'offline': {}, 'budget': {}, 'timings': {},
            'original_native': {}, 'negative': {}, 'inventory': {}}
EVENTS865 = []
ERROR865 = None
TRACEBACK865 = ''
SUCCESS865 = False
T0_865 = None
short865 = short864
table865 = table864
json_write865 = json_write864
sha256_file865 = sha256_file864


def event865(kind, **payload):
    row = {'kind': kind, 't_s': round(time.perf_counter() - START864, 3)}
    if torch.cuda.is_available():
        row['gpu_alloc_gib'] = round(torch.cuda.memory_allocated() / 1024**3, 3)
    row.update(payload)
    EVENTS865.append(row)
    return row


# ======================================================================================================================
# GATE 0 — sources, contracts, dependencies, label firewall
# ======================================================================================================================
def source_text865(name):
    return RAW_SOURCES864[name].decode('utf-8')


def embedded_literal865(source, variable):
    tree = ast.parse(source)
    found = [node.value.value for node in tree.body if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == variable for t in node.targets)
        and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)]
    assert len(found) == 1, ('EMBEDDED_LITERAL_NOT_UNIQUE', variable, len(found))
    return found[0]


def signature865(source, name):
    nodes = [n for n in ast.walk(ast.parse(source)) if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name]
    assert len(nodes) == 1, ('SIGNATURE_NOT_UNIQUE', name, len(nodes))
    node = nodes[0]
    return {'kind': 'class' if isinstance(node, ast.ClassDef) else 'function',
        'signature': 'class' if isinstance(node, ast.ClassDef) else ast.unparse(node.args),
        'ast_sha256': sha256_bytes864(ast.dump(node, include_attributes=False).encode('utf-8'))}


def load_sources865():
    # v3 (engine + logs) and v2 (MAM 7B provenance) are locked by git blob SHA-1. v1 is not executed and not fetched.
    archives = {'v3': CODELOAD864,
                'v2': 'https://codeload.github.com/ceceli33/titan-cognitive-core-v2/zip/refs/heads/main'}
    rows = []
    for tag, url in archives.items():
        request = urllib.request.Request(url, headers={'User-Agent': 'AKBASCORE-TEST865-GATE0'})
        with urllib.request.urlopen(request, timeout=240) as response:
            data = response.read(150000001)
        assert len(data) <= 150000000 and zipfile.is_zipfile(io.BytesIO(data)), ('SOURCE_ARCHIVE_INVALID', tag)
        archive_sha = sha256_bytes864(data)
        with zipfile.ZipFile(io.BytesIO(data)) as zipped:
            names = zipped.namelist()
            for name, expected in LOCKS864.items():
                if (tag == 'v2') != name.startswith('v2/'):
                    continue
                disk_name = name.split('/', 1)[1] if tag == 'v2' else name
                matches = [n for n in names if n.count('/') == 1 and n.endswith('/' + disk_name)]
                assert len(matches) == 1, ('SOURCE_NOT_UNIQUE_OR_404', tag, disk_name, matches)
                raw = zipped.read(matches[0])
                actual = git_blob864(raw)
                assert actual == expected, ('SOURCE_GIT_BLOB_MISMATCH', name, expected, actual)
                if disk_name.endswith('.py'):
                    ast.parse(raw.decode('utf-8'), filename=name)
                RAW_SOURCES864[name] = raw
                rows.append({'repository': tag, 'name': name, 'bytes': len(raw), 'git_blob_sha1': actual,
                    'sha256': sha256_bytes864(raw), 'archive_sha256': archive_sha, 'status': 'PASS'})
    assert len(rows) == len(LOCKS864), ('SOURCE_LOCK_COUNT', len(rows), len(LOCKS864))
    STATE865['source'].update({'locks': rows, 'lock_count': len(rows), 'prereg': PREREG865,
        'prereg_sha256': PREREG_SHA865, 'v1_repository': 'NOT_FETCHED_NOT_EXECUTED'})
    table865('GATE0 SOURCE', integrity='PASS', payload={'locks': len(rows), 'prereg_sha256': PREREG_SHA865})


def capture_cell_source865():
    shell = get_ipython()  # supplied by Colab/IPython
    history = list(shell.history_manager.input_hist_raw)
    marker = 'AKBASCORE SILICON HIPPOCAMPUS — TEST865'
    candidates = [text for text in history if marker in text]
    assert candidates, 'EXECUTED_865_SOURCE_NOT_CAPTURED'
    source = candidates[-1]
    ast.parse(source)
    (ROOT864 / '865.py').write_text(source, encoding='utf-8')
    assert (ROOT864 / '865.py').read_text(encoding='utf-8') == source
    STATE865['source']['executed_cell_sha256'] = sha256_bytes864(source.encode('utf-8'))
    return source


# Expected argument lists, read from the locked sources (841/845/849/851/852/854 bodies, 730/757, 834).
EXPECTED_SIGNATURES865 = {
    'gen849': '(memx, pre, rows, post)', 'gen851': '(memx, pre, segments, post)', 'gen845': '(memx, pre, rows, post)',
    'h3_bypass841': '(mem, ids=None, embeds=None)', 'index_embeds841': '(R)', 'route841': '(h_rows, bank, exclude)',
    'peak50_841': '(Q, K)', 'echo841': '(mem, text, arm)', 'address841': '(memx, qid, frame, arm, bank, exclude)',
    'mem_for841': '(mount, tag)', 'plan845': '(q)', 'end845': '(t_)', 'parse849': '(text)', 'result849': '(h)',
    'stats849': '(rows)', 'relation852': '(C, E)', 'interaction854': '(C, E, K0)', 'qrows841': '(h, qid)',
    'safe_load': '(entry)', 'seal_cp': '(cp)', 'seal834': '(memx)', 'mount834': '(ids, tag)',
    'build_fusion': None, 'native_append_direct': '(memory, cp, strict_sha=True)', 'budget849': '()'}
RUNTIME_FUNCTIONS865 = ('event865', 'rearm_budget865', 'budget_left865', 'full_h865', 'root_diagnostic865',
    'hop865', 'pointer_query865', 'cue_rows865', 'route_blind865', 'random_matched865', 'norm_matched865',
    'shuffled_route865', 'inventory865', 'prefix_seals865', 'mount865', 'gate2_pointer865', 'gate3_address865',
    'gate45_physical865', 'gate7_traps865', 'terminal_review865', 'loop865', 'acquire865', 'attribute865',
    'run_loops865', 'unmount865', 'review_step865', 'free865')


def audit_contracts865():
    contracts = {}
    b841 = embedded_literal865(source_text865('841.py'), 'BODY841')
    r845 = embedded_literal865(source_text865('845.py'), 'RUN845')
    b851 = embedded_literal865(source_text865('851.py'), 'BODY851')
    h849 = embedded_literal865(source_text865('849.py'), 'HELP849')
    for source, prefix, names in [
            (b841, '841.BODY841', ['index_embeds841', 'h3_bypass841', 'peak50_841', 'route841', 'mem_for841', 'echo841',
                                   'address841', 'qrows841']),
            (r845, '845.RUN845', ['end845', 'gen845', 'hop845', 'addr845', 'plan845', 'jloop845', 'attrib845']),
            (b851, '851.BODY851', ['make_x851', 'gen851']),
            (source_text865('757.py'), '757', ['build_fusion', 'native_append_direct', 'load_verified']),
            (source_text865('730.py'), '730', ['DirectCut3', 'safe_load', 'initialize_native', 'forge_native', 'seal_cp']),
            (h849, '849.HELP849', ['stats849', 'result849', 'parse849', 'continuity849', 'trace849'])]:
        for name in names:
            contracts[prefix + ':' + name] = signature865(source, name)
    # gen849 is assembled by the locked 849 builder: GEN849 = once849(GEN849, 'def gen845(', 'def gen849(').
    assert "GEN849 = once849(GEN849, 'def gen845(', 'def gen849(')" in source_text865('849.py')
    contracts['849.GEN849:gen849'] = {'kind': 'function', 'signature': 'memx, pre, rows, post',
        'origin': 'string patch of 845 gen845 (budget849 + continuity849 + trace849); verified at runtime by inspect'}
    # Cartridge lower K/V hold all n = P + body positions (730 forge_native: kv[:CUT+1] over PIDS+body; 757 slices P+st).
    forge = source_text865('730.py')
    assert "'lower':tuple((k.detach().cpu().contiguous(),v.detach().cpu().contiguous()) for k,v in kv[:CUT+1])" in forge
    assert 'shifted.append(rephase(k[:,:,P+st:P+end,:],oldpos,newpos))' in source_text865('757.py')
    log864 = source_text865('864.log')
    for snippet in ('decision=INVALID', '"raw": ""',
                    '"h_sha256": "aa1087a79ade81db49af76434ce0eecd68df3454ab4597ad40a7c148d9acbbc8"'):
        assert snippet in log864, ('REFERENCE_864_EMPTY_OUTPUT_MISSING', snippet)
    log845 = source_text865('845.log')
    for snippet in ('junction_unknown_precision         [342, 342]', 'junction_state_address_next_link   [46, 199]',
                    'MODEL_DERIVED_ADDRESS            FAIL'):
        assert snippet in log845, ('REFERENCE_845_MISSING', snippet)
    assert 'D1       R1 2/12 FAIL' in source_text865('841.log')
    STATE865['source']['contracts'] = contracts
    STATE865['source']['interpretation'] = {
        '864_common_h_sha256': 'sha256(b"(0, 8192)") = empty (0,8192) output rows, not a common native state',
        '864_tok1': 'not recorded by 864; GATE1 records tok1/top-20/H1/X-SHA',
        '845_address': 'official MODEL_DERIVED_ADDRESS 46/199 FAIL; post-hoc first-try 28/28 is not evidence',
        '841_direct_latent': 'D1 R1 2/12: direct latent re-entry is not used'}
    table865('GATE0 CONTRACTS', integrity='PASS', payload={'n': len(contracts)})


def firewall_audit865(tree):
    # Static proof that runtime decision functions never reference offline labels, offline scorers or the offline key.
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    missing = [name for name in RUNTIME_FUNCTIONS865 if name not in funcs]
    assert not missing, ('FIREWALL_RUNTIME_FUNCTION_MISSING', missing)
    violations = {}
    for name in RUNTIME_FUNCTIONS865:
        bad = set()
        for node in ast.walk(funcs[name]):
            if isinstance(node, ast.Name) and node.id in OFFLINE_NAMES865:
                bad.add(node.id)
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in OFFLINE_NAMES865:
                bad.add(node.value)
            if isinstance(node, ast.Attribute) and node.attr in OFFLINE_NAMES865:
                bad.add(node.attr)
        if bad:
            violations[name] = sorted(bad)
    assert not violations, ('LABEL_FIREWALL_VIOLATION', violations)
    setup = [n for n in ('build_specs865',) if n in funcs]
    STATE865['source']['firewall'] = {'runtime_functions': list(RUNTIME_FUNCTIONS865), 'forbidden': sorted(OFFLINE_NAMES865),
        'violations': {}, 'condition_construction_only': setup, 'offline_scoring_only': ['offline_evaluate865'],
        'status': 'PASS'}
    table865('GATE0 FIREWALL', integrity='PASS', payload=STATE865['source']['firewall'])


def runtime_contracts865(env):
    rows = {}
    for name, expected in EXPECTED_SIGNATURES865.items():
        assert name in env and callable(env[name]), ('RUNTIME_SYMBOL_MISSING', name)
        actual = str(inspect.signature(env[name]))
        ok = expected is None or actual == expected
        rows[name] = {'expected': expected, 'actual': actual, 'match': ok}
        assert ok, ('RUNTIME_SIGNATURE_MISMATCH', name, expected, actual)
    for name in ('KEYS841', 'MU841', 'MEMNULL841', 'QIDS841', 'QTEXT841', 'BANKS841', 'VPAIR841', 'FR845', 'SLOT845',
                 'IDXPRE841', 'IDXPOST841', 'entries', 'CART_DIR', 'NULL829', 'CALLS849', 'CALL_CAP849',
                 'HARD_BUDGET_MIN841', 'T0_841', 'MAX_FUSED_TOKENS', 'SEAL_LAYERS834'):
        assert name in env, ('RUNTIME_GLOBAL_MISSING', name)
    assert env['MAX_REVIEWS851'] == MAX_REVIEWS865 and env['SMAX845'] == S_LIMIT865
    assert env['HMAX845'] == MAX_HOPS865 and env['CAP845'] == MAX_CARDS865
    STATE865['source']['runtime_signatures'] = rows
    table865('GATE0 RUNTIME SIGNATURES', integrity='PASS', payload=rows)


def runtime_preflight865(env, reproduction):
    name = torch.cuda.get_device_name(0)
    total = torch.cuda.get_device_properties(0).total_memory
    assert 'A100' in name and total >= 75 * 1024**3, ('GPU_PREFLIGHT', name, total)
    free, total_now = torch.cuda.mem_get_info()
    disk = shutil.disk_usage(str(ROOT864))
    row = {'gpu': name, 'gpu_bytes': total, 'gpu_free_bytes': free, 'torch': torch.__version__,
        'cuda': torch.version.cuda, 'python': sys.version, 'disk_free_bytes': disk.free,
        'ram_bytes': os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES'),
        'transformers': str(getattr(env.get('transformers'), '__version__', None)),
        'reproduction': reproduction, 'peak_gib_so_far': torch.cuda.max_memory_allocated() / 1024**3,
        'P': int(env['P']), 'CUT': int(env['CUT']), 'NL': int(env['NL']), 'H': int(env['H']),
        'MAX_FUSED_TOKENS': int(env['MAX_FUSED_TOKENS']), 'K845': int(env['K845'])}
    assert row['CUT'] == 3 and row['NL'] == 80 and row['H'] == 8192 and row['P'] == 30
    STATE865['source']['runtime'] = row
    table865('GATE0 RUNTIME', integrity='PASS', payload=row)


def _close865(a, b, eps, path, diffs):
    if isinstance(a, float) or isinstance(b, float):
        if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
            diffs.append((path, 'TYPE'))
            return
        d = abs(float(a) - float(b))
        if d > eps:
            diffs.append((path, d))
        return
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            diffs.append((path, 'KEYS'))
            return
        for k in a:
            _close865(a[k], b[k], eps, path + '/' + str(k), diffs)
        return
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            diffs.append((path, 'LEN'))
            return
        for i, (x, y) in enumerate(zip(a, b)):
            _close865(x, y, eps, path + '/' + str(i), diffs)
        return
    if a != b:
        diffs.append((path, 'VALUE'))


def verify_864_reference865(actual):
    matched = [line for line in source_text865('864.log').splitlines() if line.startswith('TABLE B NATIVE REGRESSION ')]
    assert len(matched) == 1, 'REFERENCE_864_REGRESSION_NOT_UNIQUE'
    reference = json.loads(matched[0][matched[0].index('{'):])
    normalized = json.loads(json.dumps(actual, ensure_ascii=False))
    diffs = []
    _close865(normalized, reference, REGRESSION_ABS_EPS863, '', diffs)
    STATE865['gates']['GATE1_REGRESSION'] = {'status': 'PASS' if not diffs else 'FAIL',
        'tolerance_abs': REGRESSION_ABS_EPS863, 'bitwise_equal': normalized == reference, 'differences': diffs[:50]}
    table865('GATE1 REGRESSION', integrity='PASS' if not diffs else 'FAIL', payload=STATE865['gates']['GATE1_REGRESSION'])
    assert not diffs, ('GATE1_864_NATIVE_REGRESSION_CHANGED', diffs[:10])


def rearm_budget865(env):
    # The locked budget849() caps all gen849/gen851/score calls at CALL_CAP849 (160) and HARD_BUDGET_MIN841 (45 min)
    # since T0_841. TEST865 grants an explicit, logged allowance; MAX_REVIEWS851 and model computation are unchanged.
    before = {'CALLS849': int(env['CALLS849']), 'CALL_CAP849': int(env['CALL_CAP849']),
              'HARD_BUDGET_MIN841': float(env['HARD_BUDGET_MIN841']),
              'elapsed_min_since_T0_841': round((time.perf_counter() - env['T0_841']) / 60.0, 3)}
    env['CALL_CAP849'] = int(env['CALLS849']) + CALL_ALLOWANCE865
    env['HARD_BUDGET_MIN841'] = before['elapsed_min_since_T0_841'] + TEST865_MINUTES + 30.0
    after = {'CALL_CAP849': env['CALL_CAP849'], 'HARD_BUDGET_MIN841': env['HARD_BUDGET_MIN841']}
    STATE865['budget'] = {'before': before, 'after': after, 'allowance_calls': CALL_ALLOWANCE865,
        'test865_minutes': TEST865_MINUTES, 'class': 'MECHANICAL_BUDGET_REARM_LOGGED'}
    table865('M0 BUDGET REARM', payload=STATE865['budget'])


def budget_left865(env, need_calls=60):
    minutes = (time.perf_counter() - T0_865) / 60.0
    calls_left = int(env['CALL_CAP849']) - int(env['CALLS849'])
    return minutes < TEST865_MINUTES and calls_left >= need_calls


# ======================================================================================================================
# Shared runtime helpers (no offline labels)
# ======================================================================================================================
def full_h865(env, h):
    result = env['result849'](h)
    trace = h.get('trace849', {})
    result['X_input_rows_sha256'] = trace.get('input', {}).get('sha256')
    result['termination'] = trace.get('termination')
    result['first_token_is_end845'] = bool(env['end845'](int(h['tok1'])))
    result['tok1_decoded'] = env['tok'].decode([int(h['tok1'])], skip_special_tokens=False)
    result['empty_output'] = not bool(h['text'].strip())
    result['UNKNOWN_explicit'] = h['text'].strip().upper().startswith('UNKNOWN')
    return result


def root_diagnostic865(env):
    # GATE1: TEST864 raw='' x-ray. Diagnostic only; SEARCH/ACTION_TXT841 is never used by the main loop.
    rows = []
    for job in env['JOBS841'][:2]:
        runtime = RUNTIME863[job['job']][0]
        prompt = env['ACTION_TXT841'].format(q=env['QTEXT841'][job['qid']])
        for segment_mode in ('NONE', 'C_E_U_R_K_K0_J'):
            for post_mode in ('EMPTY_864', 'REVIEW_SUFFIX851'):
                segments = search_segments864(env, RUNTIME863[job['job']]) if segment_mode != 'NONE' else []
                post = [] if post_mode == 'EMPTY_864' else list(env['REVIEW_SUFFIX851'])
                h = env['gen851'](runtime['pre']['memx'], env['prompt_ids'](prompt), segments, post)
                check_output_h863(h, 'ROOT864_DIAGNOSTIC_CONTINUITY')
                full = full_h865(env, h)
                record = {'job': job['job'], 'condition': job['intervention'], 'segments': segment_mode,
                    'post': post_mode, 'execution': 'DIAGNOSTIC_ONLY_NOT_USED_BY_MAIN_LOOP', 'raw': h['text'],
                    'parsed_action': env['parse_action841'](h['text']), 'tok1': int(h['tok1']),
                    'tok1_decoded': full['tok1_decoded'], 'tok1_is_end845': full['first_token_is_end845'],
                    'H1': h['H1'], 'top20': h['top1'], 'X_rows_sha256': full['X_input_rows_sha256'],
                    'output_sha256': full['output']['sha256'], 'output_rows': full['output']['shape'][0],
                    'termination': full['termination']}
                rows.append(record)
                event865('ROOT864', **{k: v for k, v in record.items() if k != 'top20'})
                table865('GATE1 ROOT864', job=job['job'], execution=record['execution'],
                    decision=record['parsed_action'], payload={k: v for k, v in record.items() if k != 'top20'})
    STATE865['root'] = rows
    cell = [r for r in rows if r['segments'] != 'NONE' and r['post'] == 'EMPTY_864']
    STATE865['gates']['GATE1_ROOT864'] = {'status': 'EXECUTED_DIAGNOSTIC', 'calls': len(rows),
        '864_cell_first_token_end845': [r['tok1_is_end845'] for r in cell],
        '864_cell_reproduces_empty': all(r['output_rows'] == 0 for r in cell),
        'cue_cell_word_first_token': [not r['tok1_is_end845'] for r in rows if r['post'] == 'REVIEW_SUFFIX851'],
        'main_loop_uses_search_action': False}


def hop865(env, memx, qid, k, pointer):
    if k == 0:
        pre = list(env['prompt_ids'](env['FR845']['hop0'].format(q=env['QTEXT841'][qid]))) + env['SLOT845'][3]
        h = env['gen849'](memx, pre, None, None)
    else:
        assert pointer is not None and pointer.ndim == 2 and pointer.shape[0] > 0, 'EMPTY_POINTER_NOT_ADDRESSABLE'
        pre = list(env['prompt_ids'](env['FR845']['hop'].format(q=env['QTEXT841'][qid]))) + env['SLOT845'][1]
        h = env['gen849'](memx, pre, pointer, env['SLOT845'][2])
    check_output_h863(h, 'HOP865_CONTINUITY')
    text = h['text'].strip()
    # EMPTY is its own class (845 hop845 counted empty text as UNKNOWN; 864 showed empty outputs exist).
    kind = 'EMPTY_OUTPUT' if not text or not h['rows'].shape[0] else (
        'UNKNOWN' if text.upper().startswith('UNKNOWN') else 'NODE')
    return h, kind


def pointer_query865(env, rows):
    # Identical to the locked addr845 query: index_embeds841(P) -> h3_bypass841(MEMNULL841) -> rows of P positions.
    assert rows is not None and rows.ndim == 2 and rows.shape[0] > 0, 'EMPTY_POINTER_NOT_ADDRESSABLE'
    assert rows.dtype == torch.float32 and rows.device.type == 'cpu' and bool(torch.isfinite(rows).all().item())
    h3, bypass_ms = env['h3_bypass841'](env['MEMNULL841'], embeds=env['index_embeds841'](rows.to(env['DEV'])))
    pre_n = len(env['IDXPRE841'])
    post_n = len(env['IDXPOST841'])
    assert tuple(h3.shape) == (pre_n + int(rows.shape[0]) + post_n, env['H']), ('BYPASS_SHAPE', tuple(h3.shape))
    assert bool(torch.isfinite(h3).all().item())
    query = h3[pre_n:pre_n + int(rows.shape[0])].detach().float().cpu()
    del h3
    return query, {'rows_shape': list(rows.shape), 'rows_sha256': env['stats849'](rows)['sha256'],
        'query_shape': list(query.shape), 'query_sha256': env['stats849'](query)['sha256'], 'bypass_ms': bypass_ms,
        'path': 'index_embeds841(rows)->h3_bypass841(MEMNULL841, layers 0..3)->H3 rows'}


CUE865 = {}


def cue_rows865(env, qid):
    # Question-only external baseline: the locked route_r41 'CUE' query (TEST840 question frame over NULL memory).
    if qid not in CUE865:
        h3, ms = env['h3_bypass841'](env['MEMNULL841'], ids=env['QIDS841'][qid])
        CUE865[qid] = (env['qrows841'](h3, qid).detach().float().cpu(), ms)
        del h3
    rows, ms = CUE865[qid]
    return rows, {'query_shape': list(rows.shape), 'query_sha256': env['stats849'](rows)['sha256'], 'bypass_ms': ms,
        'path': 'h3_bypass841(MEMNULL841, QIDS841[q]) -> qrows841 (question only; no mounted memory)'}


def route_blind865(env, query, pool, exclude):
    candidates = sorted(c for c in pool if c not in set(exclude))
    if not candidates or query is None:
        return {'chosen': None, 'scores': {}, 'status': 'BANK_EXHAUSTED' if not candidates else 'NO_QUERY',
                'route_ms': 0.0, 'n_candidates': len(candidates)}
    result = env['route841'](query, candidates, set(exclude))
    assert result['chosen'] in candidates
    values = sorted(result['scores'].values(), reverse=True)
    result.update({'status': 'SELECTED', 'n_candidates': len(candidates),
        'margin': values[0] - values[1] if len(values) > 1 else None})
    return result


def random_matched865(rows, seed):
    if rows is None or not rows.shape[0]:
        return None
    generator = torch.Generator(device='cpu').manual_seed(int(seed))
    values = torch.randn(tuple(rows.shape), generator=generator, dtype=torch.float32)
    values = torch.nn.functional.normalize(values, dim=1, eps=1e-12)
    return values * torch.linalg.vector_norm(rows, dim=1).reshape(-1, 1)


def norm_matched865(rows, reference):
    # Irrelevant model-made rows rescaled so that every row has the mean row norm of the reference pointer.
    if rows is None or reference is None or not rows.shape[0] or not reference.shape[0]:
        return None
    target = float(torch.linalg.vector_norm(reference, dim=1).mean())
    return torch.nn.functional.normalize(rows.float(), dim=1, eps=1e-12) * target


def shuffled_route865(env, query, pool, exclude, seed):
    original = env['KEYS841']
    ids = sorted(original)
    values = [original[cid] for cid in ids]
    random.Random(seed).shuffle(values)
    try:
        env['KEYS841'] = dict(zip(ids, values))
        result = route_blind865(env, query, pool, exclude)
    finally:
        env['KEYS841'] = original
    assert env['KEYS841'] is original, 'KEYS_NOT_RESTORED'
    result['identity_permutation'] = all(a is b for a, b in zip([original[c] for c in ids], values))
    return result


def inventory865(env, cid):
    if cid in STATE865['inventory']:
        return STATE865['inventory'][cid]
    entry = env['entries'][cid]
    path = env['CART_DIR'] / entry['file']
    actual = env['sha_file'](path)
    assert actual == entry['sha256'], ('CARTRIDGE_SHA_MISMATCH', cid)
    cp = env['safe_load'](entry)                       # locked: file SHA, cartridge ID, every tensor SHA
    assert env['seal_cp'](cp) == entry['tensor_sha'], ('CARTRIDGE_TENSOR_PROVENANCE_MISMATCH', cid)
    h3, lower = cp['h'], cp['lower']
    n, p = int(cp['n']), int(cp['p'])
    assert h3.dtype == env['DTYPE'] and tuple(h3.shape) == (1, n, env['H'])
    assert isinstance(lower, (list, tuple)) and len(lower) == env['CUT'] + 1
    assert p == int(env['P']) and n == p + int(cp['body_tokens']) == p + int(entry['body_tokens'])
    for kk, vv in lower:                              # lower K/V cover all n positions (730 forge_native)
        assert tuple(kk.shape) == tuple(vv.shape) == (1, 8, n, 128), ('LOWER_KV_SHAPE', cid, tuple(kk.shape))
    assert bool(torch.isfinite(h3).all().item())
    assert all(bool(torch.isfinite(pair[i]).all().item()) for pair in lower for i in (0, 1))
    row = {'cartridge': cid, 'file': str(path), 'file_sha256': actual, 'tensor_sha_exact': True,
        'H3_shape': list(h3.shape), 'H3_dtype': str(h3.dtype), 'lower_layers': len(lower),
        'lower_shape': list(lower[0][0].shape), 'n': n, 'P': p, 'body_tokens': int(cp['body_tokens']),
        'status': 'VALID'}
    del cp, h3, lower
    STATE865['inventory'][cid] = row
    return row


def prefix_seals865(env, memx, tokens=None):
    rows = []
    for layer in env['SEAL_LAYERS834']:
        key, value = memx[layer]
        if tokens is not None:
            key, value = key[:, :, :tokens, :], value[:, :, :tokens, :]
        rows.append([int(layer), env['kv_digest'](key), env['kv_digest'](value)])
    return rows


SEALS865 = {}


def mount865(env, ids, tag, prior=None):
    # Full native mount through the locked chain mem_for841 -> mount834 -> build_fusion -> native_append_direct.
    ids = list(ids) or [env['NULL829']]               # empty working set = NULL memory (locked key_r41 rule)
    assert len(ids) == len(set(ids)), 'DUPLICATE_MOUNT'
    for cid in ids:
        if cid != env['NULL829']:
            inventory865(env, cid)
    expected = int(env['P']) + sum(int(env['entries'][c]['body_tokens']) for c in ids)
    prior_n = None if prior is None else int(prior[0][0].shape[-2])
    prior_seal = None if prior is None else prefix_seals865(env, prior)
    memx, mounted, ms = env['mem_for841'](ids, tag)
    # mem_for841 returns (MEMNULL841, False) for [NULL829] exactly as the locked memx_r41/attrib845 path expects.
    assert (mounted or ids == [env['NULL829']]) and len(memx) == env['NL'], 'MEMORY_REENTRY_NOT_SUPPORTED'
    n = int(memx[0][0].shape[-2])
    layout = memory_layout864(memx)
    seal = prefix_seals865(env, memx)
    key = tuple(ids)
    restore = None
    if key in SEALS865:
        restore = SEALS865[key] == seal
    else:
        SEALS865[key] = seal
    prefix = None
    if prior is not None and prior_n <= n:
        prefix = prefix_seals865(env, memx, prior_n) == prior_seal
    record = {'tag': tag, 'mount': ids, 'n': n, 'expected_n': expected, 'n_exact': n == expected and layout['tokens'] == n,
        'all_80_layers': layout['all_80_layers'], 'finite': layout['finite'], 'mount_ms': ms,
        'prior_prefix_exact': prefix, 'exact_restore_vs_first_mount': restore,
        'path': 'mem_for841->mount834->build_fusion->native_append_direct (RoPE rephase, strict SHA)'}
    event865('MOUNT', **record)
    return memx, record


def free865(env, *memories):
    for memx in memories:
        if memx is not None and memx is not env['MEMNULL841']:
            del memx
    env['release']()
    gc.collect()


# ======================================================================================================================
# Condition construction (OFFLINE SETUP before execution: initial memory, pools, singleton traps). Produces opaque IDs.
# ======================================================================================================================
def build_specs865(env):
    worlds = env['worlds829']
    assert len(worlds) == 12 and env['BLOCK841'] == 3 and len(env['BANKS841']) == 4
    vpair = dict(env['VPAIR841'])
    items, loops = [], []
    for wi in ALL_WORLDS865:
        ids = worlds[wi]['ids']
        block = wi // env['BLOCK841']
        bank = list(env['BANKS841'][block]['v0'])
        v1_bank = list(env['BANKS841'][block]['v1'])
        donor = block * 3 + (wi % 3 + 1) % 3
        irrelevant = ((block + 1) % len(env['BANKS841'])) * 3 + wi % 3
        for condition in PANEL_CONDITIONS865 + ('HOP3', 'MISSING'):
            initial = [ids['first'], ids['fork']] if condition == 'REMOVED' else [ids['first']]
            qid = worlds[wi]['world'] + '_H3' if condition == 'HOP3' else env['QID841'][wi]
            pool = [c for c in bank if c not in initial]
            if condition == 'MISSING':
                pool = [c for c in pool if c not in (ids['second'], ids['changed'])]
            spec = {'item': 'I865_%02d_%s' % (wi, condition), 'world_index': wi, 'condition': condition, 'qid': qid,
                    'initial': initial, 'pool': pool,
                    'pool_missing': [c for c in pool if c not in (ids['second'], ids['changed'])],
                    'v1_pool': v1_bank, 'v1_exclude': [vpair[c] for c in initial],
                    'donor_item': 'I865_%02d_%s' % (donor, condition),
                    'irrelevant_item': 'I865_%02d_%s' % (irrelevant, condition),
                    'traps': {'REVERSED_EDGE': [ids['mirror']], 'SHARED_NODE': [ids['fork']], 'DECOY': [ids['decoy']]},
                    'held_out': wi in HELD_OUT_WORLDS865}
            assert spec['qid'] in env['QTEXT841'] and spec['qid'] in env['QIDS841']
            assert set(pool) <= set(bank) and not set(initial) & set(pool)
            if condition in PANEL_CONDITIONS865:
                items.append(spec)
            loops.append(spec)
    STATE865['specs'] = {'items': items, 'loops': loops,
        'sha256': sha256_bytes864(json.dumps([items, loops], sort_keys=True).encode('utf-8'))}
    table865('M0 SPECS', payload={'items': len(items), 'loop_specs': len(loops), 'sha256': STATE865['specs']['sha256']})
    return items, loops


# ======================================================================================================================
# GATE 2 — native pointer states; GATE 3 — causal addressing arms on the same blind pool
# ======================================================================================================================
POINTERS865 = {}


def gate2_pointer865(env, items):
    for spec in items:
        memx = None
        record = {'item': spec['item'], 'condition': spec['condition'], 'held_out': spec['held_out'],
                  'execution': 'NATIVE_HOP_OVER_PHYSICAL_MEMORY', 'status': 'NOT_RUN'}
        try:
            memx, mount = mount865(env, spec['initial'], '865_G2_' + spec['item'])
            hop0, kind0 = hop865(env, memx, spec['qid'], 0, None)
            valid = kind0 == 'NODE'
            P = hop0['rows'] if valid else None
            hop1, kind1 = (hop865(env, memx, spec['qid'], 1, P) if valid else (None, 'NO_POINTER'))
            echo, info, last, R, qr = env['address841'](memx, spec['qid'], 'A', 'M2S', spec['pool'], set(spec['initial']))
            del last, R, qr
            values = sorted(echo['scores'].values(), reverse=True)
            echo.update({'status': 'SELECTED', 'n_candidates': len(echo['scores']),
                         'margin': values[0] - values[1] if len(values) > 1 else None})
            POINTERS865[spec['item']] = {'P': P, 'C': None if hop1 is None else hop1['rows'],
                                         'base_seal': prefix_seals865(env, memx), 'ECHO': echo}
            record.update({'status': 'EXECUTED', 'mount': mount, 'hop0': full_h865(env, hop0), 'hop0_kind': kind0,
                'hop1': None if hop1 is None else full_h865(env, hop1), 'hop1_kind': kind1,
                'P_sha256': None if P is None else env['stats849'](P)['sha256'],
                'P_rows': None if P is None else int(P.shape[0])})
        except Exception as exc:
            record.update({'status': 'EXECUTION_ERROR', 'error': type(exc).__name__ + ': ' + str(exc),
                           'traceback': traceback.format_exc()})
        finally:
            free865(env, memx)
        STATE865['pointer'].append(record)
        table865('GATE2 POINTER', job=spec['item'], execution=record['execution'],
            decision=str(record.get('hop0_kind')) + '/' + str(record.get('hop1_kind')),
            integrity='PASS' if record['status'] == 'EXECUTED' else 'FAIL',
            payload={'hop0': record.get('hop0', {}).get('text'), 'hop1': (record.get('hop1') or {}).get('text'),
                     'status': record['status']})


def gate3_address865(env, items):
    for spec in items:
        own = POINTERS865.get(spec['item'], {})
        donor = POINTERS865.get(spec['donor_item'], {})
        far = POINTERS865.get(spec['irrelevant_item'], {})
        P = own.get('P')
        seed = RANDOM_SEED865 + 97 * ALL_WORLDS865.index(spec['world_index']) + PANEL_CONDITIONS865.index(spec['condition'])
        sources = {'P': P, 'C': own.get('C'), 'RANDOM_NORM_MATCHED': random_matched865(P, seed),
                   'CROSS_WORLD_DONOR': donor.get('P'), 'IRRELEVANT_NORM_MATCHED': norm_matched865(far.get('P'), P)}
        arms = {}
        for arm, rows in sources.items():
            if rows is None or not rows.shape[0]:
                arms[arm] = {'status': 'POINTER_UNAVAILABLE', 'chosen': None, 'scores': {}}
                continue
            query, provenance = pointer_query865(env, rows)
            arms[arm] = route_blind865(env, query, spec['pool'], spec['initial']) | {'provenance': provenance}
            if arm == 'P':
                arms['SHUFFLED_KEYS'] = shuffled_route865(env, query, spec['pool'], spec['initial'],
                                                          SHUFFLE_SEED865 + seed) | {'provenance': provenance}
                arms['MISSING_TARGET_RANKING'] = route_blind865(env, query, spec['pool_missing'], spec['initial']) | {
                    'provenance': provenance, 'abstention_supported': False}
                arms['V1_IDENTITY_REMAP'] = route_blind865(env, query, spec['v1_pool'], spec['v1_exclude']) | {
                    'provenance': provenance}
            del query
        for arm in ('SHUFFLED_KEYS', 'MISSING_TARGET_RANKING', 'V1_IDENTITY_REMAP'):
            arms.setdefault(arm, {'status': 'POINTER_UNAVAILABLE', 'chosen': None, 'scores': {}})
        cue, provenance = cue_rows865(env, spec['qid'])
        arms['CUE_QUESTION_ONLY'] = route_blind865(env, cue, spec['pool'], spec['initial']) | {'provenance': provenance}
        arms['ECHO841_M2S'] = own.get('ECHO') or {'status': 'POINTER_UNAVAILABLE', 'chosen': None, 'scores': {}}
        row = {'item': spec['item'], 'condition': spec['condition'], 'held_out': spec['held_out'], 'arms': arms,
               'pool_size': len(spec['pool']), 'execution': 'MODEL_DERIVED_QUERY_PLUS_MECHANICAL_RETRIEVAL',
               'offline_labels_used_by_router': False}
        STATE865['addressing'].append(row)
        event865('ADDRESS', item=spec['item'], chosen={a: v.get('chosen') for a, v in arms.items()})
        table865('GATE3 ADDRESS', job=spec['item'], execution=row['execution'], decision=str(arms['P'].get('chosen')),
            payload={a: {'chosen': v.get('chosen'), 'status': v.get('status'), 'margin': v.get('margin')}
                     for a, v in arms.items()})


# ======================================================================================================================
# GATE 4/5 — physical SSD load + CUT3 re-entry, re-hop under the same P, paired counterfactuals, exact restore
# ======================================================================================================================
def gate45_physical865(env, items):
    by_item = {row['item']: row for row in STATE865['addressing']}
    for spec in items:
        own = POINTERS865.get(spec['item'], {})
        P = own.get('P')
        arms = by_item[spec['item']]['arms']
        row = {'item': spec['item'], 'condition': spec['condition'], 'held_out': spec['held_out'],
               'execution': 'PHYSICAL_REENTRY_SAME_POINTER', 'mounts': {}}
        for arm in ('P', 'RANDOM_NORM_MATCHED'):
            chosen = arms[arm].get('chosen')
            result = {'chosen': chosen, 'status': 'NOT_RUN'}
            memx = None
            try:
                if P is None:
                    result['status'] = 'POINTER_UNAVAILABLE'
                elif chosen is None:
                    result['status'] = 'NO_SELECTION'
                else:
                    memx, mount = mount865(env, spec['initial'] + [chosen], '865_G4_%s_%s' % (arm, spec['item']))
                    result['prefix_vs_initial_exact'] = prefix_seals865(env, memx, int(env['P']) + sum(
                        int(env['entries'][c]['body_tokens']) for c in spec['initial'])) == own['base_seal']
                    h, kind = hop865(env, memx, spec['qid'], 1, P)
                    result.update({'status': 'REHOP_EVALUATED', 'mount': mount, 'rehop': full_h865(env, h),
                                   'rehop_kind': kind})
            except Exception as exc:
                result.update({'status': 'EXECUTION_ERROR', 'error': type(exc).__name__ + ': ' + str(exc),
                               'traceback': traceback.format_exc()})
            finally:
                free865(env, memx)
            row['mounts'][arm] = result
        restore = None
        try:
            memx, mount = mount865(env, spec['initial'], '865_G4_RESTORE_' + spec['item'])
            restore = prefix_seals865(env, memx) == own.get('base_seal')
            free865(env, memx)
        except Exception as exc:
            row['restore_error'] = type(exc).__name__ + ': ' + str(exc)
        row['exact_restore'] = restore
        STATE865['physical'].append(row)
        table865('GATE4 REENTRY', job=spec['item'], execution=row['execution'],
            cartridge=str(row['mounts']['P'].get('chosen')), decision=str(row['mounts']['P'].get('rehop_kind')),
            integrity='PASS' if row['mounts']['P'].get('status') == 'REHOP_EVALUATED' and restore else 'FAIL',
            payload={'P_rehop': row['mounts']['P'].get('rehop', {}).get('text'),
                     'RANDOM_rehop': row['mounts']['RANDOM_NORM_MATCHED'].get('rehop', {}).get('text'),
                     'exact_restore': restore})


def gate7_traps865(env, items):
    # Forced singleton mounts are DIAGNOSTIC_REPLAY_ONLY: the experimenter, not the router, chooses the trap card.
    for spec in [s for s in items if s['condition'] == 'LIVE']:
        P = POINTERS865.get(spec['item'], {}).get('P')
        for control in TRAP_CONTROLS865:
            result = {'item': spec['item'], 'control': control, 'held_out': spec['held_out'],
                      'execution': 'DIAGNOSTIC_REPLAY_ONLY' if control != 'MISSING_TARGET' else
                      'MODEL_DERIVED_QUERY_MECHANICAL_RETRIEVAL_TARGET_ABSENT', 'status': 'NOT_RUN'}
            memx = None
            try:
                if P is None:
                    result['status'] = 'POINTER_UNAVAILABLE'
                else:
                    if control == 'MISSING_TARGET':
                        query, provenance = pointer_query865(env, P)
                        route = route_blind865(env, query, spec['pool_missing'], spec['initial'])
                        chosen = route['chosen']
                        result['route'] = {k: v for k, v in route.items() if k != 'scores'}
                        del query
                    else:
                        chosen = spec['traps'][control][0]
                    if chosen is None:
                        result['status'] = 'BANK_EXHAUSTED'
                    else:
                        memx, mount = mount865(env, spec['initial'] + [chosen], '865_G7_%s_%s' % (control, spec['item']))
                        h, kind = hop865(env, memx, spec['qid'], 1, P)
                        result.update({'status': 'REHOP_EVALUATED', 'chosen': chosen, 'mount': mount,
                                       'rehop': full_h865(env, h), 'rehop_kind': kind,
                                       'local_acceptance': kind == 'NODE'})
            except Exception as exc:
                result.update({'status': 'EXECUTION_ERROR', 'error': type(exc).__name__ + ': ' + str(exc),
                               'traceback': traceback.format_exc()})
            finally:
                free865(env, memx)
            STATE865['traps'].append(result)
            table865('GATE7 TRAP', job=spec['item'], execution=result['execution'], cartridge=str(result.get('chosen')),
                decision=str(result.get('rehop_kind', result['status'])),
                integrity='PASS' if result['status'] == 'REHOP_EVALUATED' else 'FAIL',
                payload={'control': control, 'text': result.get('rehop', {}).get('text')})


# ======================================================================================================================
# Terminal native review (locked BASELINE853 junction) + diagnostic {C,E,U} ablation
# ======================================================================================================================
def terminal_review865(env, memx, qid, candidate, previous_review):
    q = env['QTEXT841'][qid]
    c_state = candidate['rows'].detach().float().cpu()
    evidence = env['gen849'](memx, list(env['prompt_ids'](env['EVIDENCE851'].format(q=q))), None, env['ANSWER_SUFFIX851'])
    coverage = env['gen849'](memx, list(env['prompt_ids'](env['COVERAGE852'].format(q=q))), None, env['COVERAGE_SUFFIX852'])
    check_output_h863(evidence, 'REVIEW865_EVIDENCE')
    check_output_h863(coverage, 'REVIEW865_COVERAGE')
    e_state = evidence['rows'].detach().float().cpu()
    u_state = coverage['rows'].detach().float().cpu()
    empty = [name for name, value in (('C', c_state), ('E', e_state), ('U', u_state)) if not value.shape[0]]
    if empty:                                         # an empty native state cannot be transferred; mechanical end
        return {'status': 'EMPTY_NATIVE_REVIEW_INPUT', 'empty': empty, 'evidence': full_h865(env, evidence),
                'coverage': full_h865(env, coverage)}, None, None
    r_state = env['relation852'](c_state, e_state)
    review_pre = list(env['prompt_ids'](env['REVIEW851'].format(q=q)))
    pre_segments = [(env['C_SLOT851'], c_state), (env['E_SLOT851'], e_state)]
    if previous_review is not None:
        pre_segments.append((env['K_SLOT851'], previous_review['rows']))
    pre_segments.extend([(env['U_SLOT852'], u_state), (env['R_SLOT852'], r_state)])
    pre_h = env['gen851'](memx, review_pre, pre_segments, env['REVIEW_SUFFIX851'])
    check_output_h863(pre_h, 'REVIEW865_PRECONTROL')
    k0 = pre_h['rows']
    if not k0.shape[0]:
        return {'status': 'EMPTY_NATIVE_REVIEW_INPUT', 'empty': ['K0'], 'precontrol': full_h865(env, pre_h)}, None, None
    j_state = env['interaction854'](c_state, e_state, k0)
    review_segments = [(env['K_SLOT854'], k0), (env['J_SLOT854'], j_state)]
    review = env['gen851'](memx, review_pre, review_segments, env['REVIEW_SUFFIX851'])
    check_output_h863(review, 'REVIEW865_REVIEW')
    action = env['parse849'](review['text'])
    score_rows = score_actions859(env, memx, review_pre, review_segments, env['REVIEW_SUFFIX851'])
    assert [r['spelling'].strip() for r in score_rows] == ['CONTINUE', 'REVISE', 'STOP']
    scores = {r['spelling'].strip(): r['sequence_logp'] for r in score_rows}
    revision = None
    revision_segments = None
    if action == 'REVISE':
        revision_segments = [(env['C_SLOT851'], c_state), (env['K_SLOT851'], review['rows']),
            (env['E_SLOT851'], e_state), (env['U_SLOT852'], u_state), (env['R_SLOT852'], r_state)]
        revision = env['gen851'](memx, list(env['prompt_ids'](env['RECOMPUTE851'].format(q=q))), revision_segments,
                                 env['ANSWER_SUFFIX851'])
        check_output_h863(revision, 'REVIEW865_REVISION')
    pre_inv = {'segments': pre_segments, 'h': pre_h}
    review_inv = {'segments': review_segments, 'h': review}
    transfers = [
        transfer864(env, 'C', '865_PRECONTROL', c_state, env['C_SLOT851'], pre_inv, source_stage='native_hop'),
        transfer864(env, 'E', '865_PRECONTROL', e_state, env['E_SLOT851'], pre_inv, source_stage='native_evidence'),
        transfer864(env, 'U', '865_PRECONTROL', u_state, env['U_SLOT852'], pre_inv, source_stage='native_coverage'),
        transfer864(env, 'R', '865_PRECONTROL', r_state, env['R_SLOT852'], pre_inv,
            recompute=lambda: env['relation852'](c_state, e_state), source_stage='native_relation'),
        transfer864(env, 'K0', '865_REVIEW', k0, env['K_SLOT854'], review_inv, source_stage='native_precontrol'),
        transfer864(env, 'J', '865_REVIEW', j_state, env['J_SLOT854'], review_inv,
            recompute=lambda: env['interaction854'](c_state, e_state, k0), source_stage='native_interaction')]
    if previous_review is not None:
        transfers.append(transfer864(env, 'Kprev', '865_PRECONTROL', previous_review['rows'], env['K_SLOT851'],
                                     pre_inv, source_stage='previous_native_review'))
    # Diagnostic ablation (never used for control): {C,E,(K),U} precontrol without R, K0-only review without J.
    ab_pre = [s for s in pre_segments if s[0] != env['R_SLOT852']]
    ab_k0 = env['gen851'](memx, review_pre, ab_pre, env['REVIEW_SUFFIX851'])
    check_output_h863(ab_k0, 'REVIEW865_ABLATION_PRE')
    ablation = {'status': 'EMPTY_K0'}
    if ab_k0['rows'].shape[0]:
        ab_segments = [(env['K_SLOT854'], ab_k0['rows'])]
        ab_review = env['gen851'](memx, review_pre, ab_segments, env['REVIEW_SUFFIX851'])
        check_output_h863(ab_review, 'REVIEW865_ABLATION_REVIEW')
        ab_scores = score_actions859(env, memx, review_pre, ab_segments, env['REVIEW_SUFFIX851'])
        ablation = {'status': 'EXECUTED', 'action': env['parse849'](ab_review['text']), 'text': ab_review['text'],
                    'scores': {r['spelling'].strip(): r['sequence_logp'] for r in ab_scores},
                    'agrees_with_full_review': env['parse849'](ab_review['text']) == action,
                    'execution': 'DIAGNOSTIC_ABLATION_NOT_USED_FOR_CONTROL'}
    record = {'candidate': full_h865(env, candidate), 'evidence': full_h865(env, evidence),
        'coverage': full_h865(env, coverage), 'precontrol': full_h865(env, pre_h), 'review': full_h865(env, review),
        'action': action, 'scores': scores,
        'margin_continue_minus_best_other': scores['CONTINUE'] - max(scores['REVISE'], scores['STOP']),
        'margin_stop_minus_revise': scores['STOP'] - scores['REVISE'],
        'revision_same_memory': None if revision is None else full_h865(env, revision),
        'states': {name: state863(env, value) for name, value in
                   (('C', c_state), ('E', e_state), ('U', u_state), ('R', r_state), ('K0', k0), ('J', j_state))},
        'transfers_exact': all(t['passed'] for t in transfers), 'ablation_CEU_K0': ablation,
        'memory_tokens': int(memx[0][0].shape[-2])}
    assert record['transfers_exact'], 'REVIEW865_STATE_TRANSFER_FAILED'
    return record, review, revision


# ======================================================================================================================
# Closed loop (TEST845 law + terminal review). Arms differ only in the acquisition query / acquisition availability.
# ======================================================================================================================
def acquire865(env, ctx, k, pointer, reason):
    # One acquisition attempt for hop k: P (or a norm-matched random query) -> fixed router -> SHA load -> CUT3 mount.
    key = (k, 'ROOT' if k == 0 else ctx['path'][k - 1]['text'].strip().upper())
    excluded = ctx['XN'].setdefault(key, set())
    if ctx['tries'].get(key, 0) >= S_LIMIT865:
        return None, 'S_LIMIT'
    if len(ctx['M']) >= MAX_CARDS865:
        return None, 'CAPACITY_STOP'
    if ctx['arm'] == 'RANDOM_QUERY':
        rows = random_matched865(pointer, RANDOM_SEED865 + 1009 * ctx['acquisitions'] +
                                 int(sha256_bytes864(ctx['spec']['item'].encode())[:8], 16) % 1000003)
    else:
        rows = pointer
    query, provenance = pointer_query865(env, rows)
    route = route_blind865(env, query, ctx['spec']['pool'], set(ctx['M']) | excluded)
    del query
    ctx['tries'][key] = ctx['tries'].get(key, 0) + 1
    ctx['acquisitions'] += 1
    if route['chosen'] is None:
        return None, 'BANK_EXHAUSTED'
    chosen = route['chosen']
    excluded.add(chosen)
    old = ctx['memx']
    ctx['memx'], mount = mount865(env, ctx['M'] + [chosen], '865_L_%s_%s_%d' % (ctx['arm'], ctx['spec']['item'],
                                                                             ctx['acquisitions']), prior=old)
    free865(env, old)
    ctx['M'].append(chosen)
    ctx['mount_records'].append(mount)
    ctx['events'].append({'type': 'ACQUIRE', 'k': k, 'reason': reason, 'chosen': chosen, 'try': ctx['tries'][key],
        'route': {x: y for x, y in route.items() if x != 'scores'}, 'scores': route['scores'],
        'provenance': provenance, 'mount': mount,
        'query_origin': 'MODEL_POINTER' if ctx['arm'] == 'NATIVE_P' else 'NORM_MATCHED_RANDOM_CONTROL'})
    return chosen, 'MOUNTED'


def unmount865(env, ctx, card, why):
    ctx['M'].remove(card)
    old = ctx['memx']
    ctx['memx'], mount = mount865(env, ctx['M'], '865_U_%s_%s_%d' % (ctx['arm'], ctx['spec']['item'], len(ctx['events'])))
    free865(env, old)
    ctx['mount_records'].append(mount)
    ctx['events'].append({'type': 'UNMOUNT', 'card': card, 'why': why, 'mount': mount})
    ctx['flags']['unmount'] += 1


def attribute865(env, ctx, kk):
    # TEST845 attrib845: which mounted card produced hop kk? NULL829 substitution, first change wins (mechanical).
    used = {p['evid'] for p in ctx['path'] if p['evid']}
    pointer = None if kk == 0 else ctx['path'][kk - 1]['rows']
    for i, card in enumerate(list(ctx['M'])):
        if card in used:
            continue
        trial = ctx['M'][:i] + [env['NULL829']] + ctx['M'][i + 1:]
        memx, mount = mount865(env, trial, '865_A_%s_%s_%d' % (ctx['arm'], ctx['spec']['item'], len(ctx['events'])))
        try:
            h, kind = hop865(env, memx, ctx['spec']['qid'], kk, pointer)
            ctx['hops'] += 1
        finally:
            free865(env, memx)
        ctx['events'].append({'type': 'ATTRIBUTION_HOP', 'k': kk, 'substituted': card, 'text': h['text'], 'kind': kind})
        if h['text'].strip() != ctx['path'][kk]['text'].strip():
            return card
    return None


def review_step865(env, ctx, candidate, kf):
    record, review, revision = terminal_review865(env, ctx['memx'], ctx['spec']['qid'], candidate, ctx['previous_review'])
    if review is None:
        ctx['events'].append({'type': 'REVIEW_NOT_POSSIBLE', 'k': kf, 'record': record})
        record['action'] = 'EMPTY_NATIVE_REVIEW_INPUT'
        return record, None
    ctx['previous_review'] = review
    ctx['reviews'].append(record)
    ctx['events'].append({'type': 'REVIEW', 'k': kf, 'action': record['action'], 'candidate': record['candidate']['text'],
                          'scores': record['scores'], 'mounted': list(ctx['M']),
                          'acquisitions_before_review': ctx['acquisitions']})
    table865('GATE6 REVIEW', job=ctx['spec']['item'], cycle=len(ctx['reviews']), execution='NATIVE_REVIEW_' + ctx['arm'],
             decision=record['action'], payload={'candidate': record['candidate']['text'], 'scores': record['scores'],
                                                 'ablation': record['ablation_CEU_K0'].get('action')})
    return record, revision


def loop865(env, spec, arm):
    ctx = {'spec': spec, 'arm': arm, 'M': list(spec['initial']), 'memx': None, 'path': [], 'XN': {}, 'tries': {},
           'events': [], 'reviews': [], 'previous_review': None, 'acquisitions': 0, 'hops': 0, 'mount_records': [],
           'flags': {'unknown_trigger': 0, 'unmount': 0, 'backtrack': 0, 'attribution': 0, 'revise_acquisition': 0,
                     'first_try_accepts': 0, 'later_try_accepts': 0}}
    end, accepted = None, None
    t0 = time.perf_counter()
    plan = env['plan845'](spec['qid'])
    N = plan['N']
    pend = None
    try:
        ctx['memx'], mount = mount865(env, ctx['M'], '865_L0_%s_%s' % (arm, spec['item']))
        ctx['mount_records'].append(mount)
        initial_seal = prefix_seals865(env, ctx['memx'])
        if N is None:
            end = 'PLAN_INVALID'
        while end is None:
            if ctx['hops'] >= MAX_HOPS865:
                end = 'BUDGET_STOP'
                break
            k = len(ctx['path'])
            candidate, kf = None, None
            if k == N:
                candidate, kf = ctx['path'][-1]['h'], k - 1
            else:
                pointer = None if k == 0 else ctx['path'][k - 1]['rows']
                h, kind = hop865(env, ctx['memx'], spec['qid'], k, pointer)
                ctx['hops'] += 1
                ctx['events'].append({'type': 'HOP', 'k': k, 'kind': kind, 'h': full_h865(env, h), 'mounted': list(ctx['M']),
                                      'pending_card': pend})
                table865('GATE6 HOP', job=spec['item'], cycle=ctx['hops'], execution='NATIVE_HOP_' + arm, decision=kind,
                         payload={'k': k, 'text': h['text'], 'mounted': list(ctx['M'])})
                if kind == 'EMPTY_OUTPUT':
                    end = 'EMPTY_OUTPUT'
                    break
                if kind == 'NODE':
                    if pend is not None:
                        key = (k, 'ROOT' if k == 0 else ctx['path'][k - 1]['text'].strip().upper())
                        ctx['flags']['first_try_accepts' if ctx['tries'].get(key) == 1 else 'later_try_accepts'] += 1
                    ctx['path'].append({'h': h, 'rows': h['rows'], 'text': h['text'].strip(), 'evid': pend})
                    pend = None
                    continue
                ctx['flags']['unknown_trigger'] += 1
                if pend is not None:                      # UNKNOWN after mount -> unmount (TEST845 law)
                    unmount865(env, ctx, pend, 'UNKNOWN_AFTER_MOUNT')
                    pend = None
                if arm != 'NO_ACQUISITION' and k > 0:
                    chosen, status = acquire865(env, ctx, k, pointer, 'MODEL_UNKNOWN')
                    if chosen is not None:
                        pend = chosen
                        continue
                    if k >= 1:                            # dead end: retract previous hop evidence and backtrack
                        evid = ctx['path'][k - 1]['evid']
                        if evid is None:
                            evid = attribute865(env, ctx, k - 1)
                            ctx['flags']['attribution'] += 1
                        if evid is not None and evid in ctx['M'] and ctx['flags']['backtrack'] < 2:
                            unmount865(env, ctx, evid, 'DEAD_END_RETRACT')
                            key = (k - 1, 'ROOT' if k - 1 == 0 else ctx['path'][k - 2]['text'].strip().upper())
                            ctx['XN'].setdefault(key, set()).add(evid)
                            ctx['path'].pop()
                            ctx['tries'] = {x: y for x, y in ctx['tries'].items() if x[0] < k - 1 or x == key}
                            ctx['flags']['backtrack'] += 1
                            continue
                candidate, kf = h, k                      # unaddressable UNKNOWN -> native terminal review
            if len(ctx['reviews']) >= MAX_REVIEWS865:
                end = 'MECHANICAL_REVIEW_LIMIT'
                break
            if not budget_left865(env, 40):
                end = 'NOT_RUN_BUDGET'
                break
            record, revision = review_step865(env, ctx, candidate, kf)
            if record['action'] == 'CONTINUE':
                end, accepted = 'MODEL_ACCEPT', record['candidate']['text'].strip()
                break
            if record['action'] == 'STOP':
                end = 'MODEL_STOP'
                break
            if record['action'] == 'EMPTY_NATIVE_REVIEW_INPUT':
                end = 'EMPTY_OUTPUT'
                break
            if record['action'] != 'REVISE':
                end = 'PROTOCOL_INVALID'
                break
            if len(ctx['reviews']) >= MAX_REVIEWS865:
                end = 'MECHANICAL_REVIEW_LIMIT'
                break
            if arm == 'NO_ACQUISITION':                   # locked 849-864 semantics: same-memory native revision
                if revision is None or not revision['text'].strip() or not revision['rows'].shape[0]:
                    end = 'EMPTY_OUTPUT'
                    break
                record2, revision2 = review_step865(env, ctx, revision, kf)
                if record2['action'] == 'EMPTY_NATIVE_REVIEW_INPUT':
                    end = 'EMPTY_OUTPUT'
                elif record2['action'] == 'CONTINUE':
                    end, accepted = 'MODEL_ACCEPT', record2['candidate']['text'].strip()
                elif record2['action'] == 'STOP':
                    end = 'MODEL_STOP'
                else:
                    end = 'MECHANICAL_REVIEW_LIMIT' if record2['action'] == 'REVISE' else 'PROTOCOL_INVALID'
                break
            # REVISE -> new P-addressed acquisition for the last hop kf (requires a pointer: kf >= 1)
            if kf < 1:
                end = 'REVISE_NO_POINTER_MECHANICAL'
                break
            if kf < len(ctx['path']):                     # candidate was a path node: re-derive hop kf
                ctx['path'] = ctx['path'][:kf]
            pointer = ctx['path'][kf - 1]['rows']
            ctx['flags']['revise_acquisition'] += 1
            chosen, status = acquire865(env, ctx, kf, pointer, 'MODEL_REVISE')
            if chosen is None:
                end = 'ACQUISITION_EXHAUSTED_' + status
                break
            pend = chosen
        result = {'item': spec['item'], 'arm': arm, 'condition': spec['condition'], 'held_out': spec['held_out'],
            'plan': {'text': plan['text'], 'N': N}, 'end': end, 'accepted_candidate': accepted,
            'path': [p['text'] for p in ctx['path']], 'path_evidence': [p['evid'] for p in ctx['path']],
            'final_mounted': list(ctx['M']), 'hops': ctx['hops'], 'acquisitions': ctx['acquisitions'],
            'reviews': ctx['reviews'], 'events': ctx['events'], 'flags': ctx['flags'],
            'mount_integrity': all(m['n_exact'] and m['all_80_layers'] and m['finite'] and m['prior_prefix_exact'] is not False
                                   and m['exact_restore_vs_first_mount'] is not False for m in ctx['mount_records']),
            'model_stop': end == 'MODEL_STOP', 'model_accept': end == 'MODEL_ACCEPT',
            'mechanical_end': end not in ('MODEL_STOP', 'MODEL_ACCEPT'), 'seconds': round(time.perf_counter() - t0, 3)}
        free865(env, ctx['memx'])
        ctx['memx'] = None
        restore_memx, restore = mount865(env, spec['initial'], '865_LR_%s_%s' % (arm, spec['item']))
        result['exact_restore'] = prefix_seals865(env, restore_memx) == initial_seal
        free865(env, restore_memx)
    except Exception as exc:
        result = {'item': spec['item'], 'arm': arm, 'condition': spec['condition'], 'held_out': spec['held_out'],
            'end': 'EXECUTION_ERROR', 'error': type(exc).__name__ + ': ' + str(exc), 'traceback': traceback.format_exc(),
            'events': ctx['events'], 'reviews': ctx['reviews'], 'flags': ctx['flags'], 'final_mounted': list(ctx['M']),
            'path': [p['text'] for p in ctx['path']], 'model_stop': False, 'model_accept': False, 'mechanical_end': True,
            'mount_integrity': False, 'exact_restore': None, 'accepted_candidate': None}
        free865(env, ctx['memx'])
        table865('GATE6 LOOP', job=spec['item'], integrity='FAIL', payload={'error': result['error']})
    STATE865['loops'].append(result)
    table865('GATE6 END', job=spec['item'], execution='LOOP_' + arm, decision=result['end'],
        integrity='PASS' if result['end'] != 'EXECUTION_ERROR' else 'FAIL',
        payload={'path': result.get('path'), 'mounted': result.get('final_mounted'), 'flags': result.get('flags'),
                 'accepted': result.get('accepted_candidate'), 'exact_restore': result.get('exact_restore')})
    return result


def run_loops865(env, loop_specs):
    for spec in loop_specs:
        arms = ('NATIVE_P',) if spec['condition'] == 'MISSING' else LOOP_ARMS865
        for arm in arms:
            if not budget_left865(env, 80):
                STATE865['loops'].append({'item': spec['item'], 'arm': arm, 'condition': spec['condition'],
                    'held_out': spec['held_out'], 'end': 'NOT_RUN_BUDGET', 'mechanical_end': True,
                    'model_stop': False, 'model_accept': False, 'events': [], 'reviews': [], 'flags': {},
                    'final_mounted': [], 'path': [], 'accepted_candidate': None, 'mount_integrity': None,
                    'exact_restore': None})
                continue
            loop865(env, spec, arm)


# ======================================================================================================================
# OFFLINE EVALUATION (after all execution). The only place that reads worlds829 / CONTENT841 / supported851.
# ======================================================================================================================
def wilson865(k, n, z=1.959963984540054):
    if not n:
        return [None, None]
    p = k / n
    den = 1 + z * z / n
    center = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [max(0.0, center - half), min(1.0, center + half)]


def sign_test865(a, b):
    # exact two-sided binomial test on discordant pairs (a True & b False vs a False & b True)
    up = sum(1 for x, y in zip(a, b) if x and not y)
    down = sum(1 for x, y in zip(a, b) if y and not x)
    n = up + down
    if not n:
        return {'up': 0, 'down': 0, 'p_two_sided': 1.0}
    tail = sum(math.comb(n, i) for i in range(max(up, down), n + 1)) / 2 ** n
    return {'up': up, 'down': down, 'p_two_sided': min(1.0, 2 * tail)}


def rate865(flags):
    k, n = sum(bool(x) for x in flags), len(flags)
    return {'k': k, 'n': n, 'rate': k / n if n else None, 'wilson95': wilson865(k, n)}


def offline_evaluate865(env):
    W = env['worlds829']
    CONTENT = env['CONTENT841']
    REL = env['REL841']
    def rel(cid):
        if cid is None or cid not in CONTENT:
            return None
        wi, kind, ver = CONTENT[cid]
        a, b = REL[kind]
        return {'world': wi, 'kind': kind, 'source': W[wi][a], 'target': W[wi][b], 'version': ver}
    def valid_for(node_name, pool):
        return {c for c in pool if rel(c) is not None and rel(c)['source'] == node_name}
    def cls(cid, node_name, wi):
        r = rel(cid)
        if r is None:
            return 'NONE' if cid is None else 'NON_BANK'
        if r['world'] != wi:
            return 'OTHER_WORLD'
        if r['source'] == node_name:
            return 'SOURCE_MATCH_' + r['kind'].upper()
        if r['target'] == node_name:
            return 'REVERSED_EDGE_' + r['kind'].upper()
        if W[wi]['start'] in (r['source'], r['target']):
            return 'SHARED_START_NODE_' + r['kind'].upper()
        return 'SAME_WORLD_OTHER_' + r['kind'].upper()
    specs = {s['item']: s for s in STATE865['specs']['loops']}
    # ---------------- GATE 3 addressing ----------------
    rows = []
    for item in STATE865['addressing']:
        spec = specs[item['item']]
        wi = spec['world_index']
        middle = W[wi]['middle']
        valid = valid_for(middle, spec['pool'])
        donor_wi = specs[spec['donor_item']]['world_index']
        out = {}
        for arm, route in item['arms'].items():
            chosen = route.get('chosen')
            if arm == 'CROSS_WORLD_DONOR':
                target_set = valid_for(W[donor_wi]['middle'], spec['pool'])
                cls_wi, node = donor_wi, W[donor_wi]['middle']
            elif arm == 'V1_IDENTITY_REMAP':
                vpair = {b: a for a, b in env['VPAIR841']}
                target_set = {c for c in spec['v1_pool'] if vpair.get(c) in valid}
                chosen_v0 = vpair.get(chosen)
                out[arm] = {'chosen': chosen, 'hit1': chosen in target_set, 'class': cls(chosen_v0, middle, wi),
                            'same_content_as_P_choice': chosen_v0 == item['arms']['P'].get('chosen')}
                continue
            elif arm == 'MISSING_TARGET_RANKING':
                target_set = valid_for(middle, spec['pool_missing'])
                cls_wi, node = wi, middle
            else:
                target_set, cls_wi, node = valid, wi, middle
            order = sorted(route.get('scores', {}), key=lambda c: (-route['scores'][c], c))
            ranks = [order.index(c) + 1 for c in target_set if c in order]
            best = min(ranks) if ranks else None
            out[arm] = {'chosen': chosen, 'hit1': chosen in target_set, 'hit3': best is not None and best <= 3,
                        'hit5': best is not None and best <= 5, 'best_valid_rank': best, 'margin': route.get('margin'),
                        'class': cls(chosen, node, cls_wi), 'valid_set_size': len(target_set),
                        'status': route.get('status')}
        pointer_row = next(p for p in STATE865['pointer'] if p['item'] == item['item'])
        p_text = (pointer_row.get('hop0') or {}).get('text', '')
        p_node = env['node851'](p_text, W[wi])
        out['_pointer'] = {'hop0_text': p_text, 'hop0_class': p_node, 'P_names_middle': p_node == 'middle',
                           'hop1_class': env['node851']((pointer_row.get('hop1') or {}).get('text', ''), W[wi]),
                           'chance_hit1': len(valid) / max(1, len(spec['pool']))}
        item['offline'] = out
        rows.append({'item': item['item'], 'condition': item['condition'], 'held_out': item['held_out'], **{
            a: v for a, v in out.items()}})
    def pick(held, arm, key='hit1', cond=None):
        return [r[arm][key] for r in rows if r['held_out'] == held and arm in r and (cond is None or cond(r))]
    H = {}
    causal = [r for r in rows if not r['held_out']]
    h1 = rate865(pick(False, 'P'))
    H['H1'] = dict(h1, threshold=0.75, chance=sum(r['_pointer']['chance_hit1'] for r in causal) / max(1, len(causal)),
                   conditional_on_P_names_middle=rate865(pick(False, 'P', cond=lambda r: r['_pointer']['P_names_middle'])),
                   status='PASS' if h1['n'] == 18 and h1['rate'] is not None and h1['rate'] >= 0.75 else 'FAIL')
    controls = {a: rate865(pick(False, a)) for a in ('CUE_QUESTION_ONLY', 'RANDOM_NORM_MATCHED', 'SHUFFLED_KEYS', 'C',
                                                     'IRRELEVANT_NORM_MATCHED', 'ECHO841_M2S')}
    best_arm = max(('CUE_QUESTION_ONLY', 'RANDOM_NORM_MATCHED', 'SHUFFLED_KEYS'), key=lambda a: controls[a]['rate'] or 0.0)
    gap = (h1['rate'] or 0.0) - (controls[best_arm]['rate'] or 0.0)
    test = sign_test865(pick(False, 'P'), pick(False, best_arm))
    H['H2'] = {'controls': controls, 'best_preregistered_control': best_arm, 'gap': gap, 'threshold': 0.40,
               'sign_test_vs_best': test, 'status': 'PASS' if gap >= 0.40 and test['p_two_sided'] <= ALPHA865 else 'FAIL'}
    donor_rows = [r for r in causal if r['P']['status'] != 'POINTER_UNAVAILABLE' and
                  r['CROSS_WORLD_DONOR']['status'] != 'POINTER_UNAVAILABLE']
    h3 = rate865([r['CROSS_WORLD_DONOR']['hit1'] for r in donor_rows])
    H['H3'] = dict(h3, threshold=0.75, status='PASS' if h3['n'] >= 9 and (h3['rate'] or 0) >= 0.75 else 'FAIL')
    address_ok = H['H1']['status'] == H['H2']['status'] == H['H3']['status'] == 'PASS'
    # ---------------- GATE 4/5 physical ----------------
    mounts = [m for m in (e for e in EVENTS865 if e['kind'] == 'MOUNT')]
    integrity = all(m['n_exact'] and m['all_80_layers'] and m['finite'] and m['prior_prefix_exact'] is not False and
                    m['exact_restore_vs_first_mount'] is not False for m in mounts)
    restores = [r.get('exact_restore') for r in STATE865['physical']] + [r.get('exact_restore') for r in STATE865['loops']
                                                                          if r['end'] not in ('NOT_RUN_BUDGET',)]
    H['H4'] = {'mounts': len(mounts), 'all_mount_checks_exact': integrity,
               'exact_restores': rate865([x is True for x in restores]),
               'status': 'PASS' if integrity and restores and all(x is True for x in restores) else 'FAIL'}
    phys = []
    for row in STATE865['physical']:
        spec = specs[row['item']]
        w = W[spec['world_index']]
        def correct(m):
            if m.get('status') != 'REHOP_EVALUATED':
                return False
            return bool(env['supported851'](m['rehop']['text'].strip(), w, set(m['mount']['mount'])))
        baseline = next(p for p in STATE865['pointer'] if p['item'] == row['item'])
        b_text = (baseline.get('hop1') or {}).get('text', '')
        phys.append({'item': row['item'], 'held_out': row['held_out'], 'P_correct': correct(row['mounts']['P']),
                     'RANDOM_correct': correct(row['mounts']['RANDOM_NORM_MATCHED']),
                     'no_mount_correct': bool(env['supported851'](b_text.strip(), w, set(spec['initial']))),
                     'P_rehop_class': env['node851'](row['mounts']['P'].get('rehop', {}).get('text', ''), w),
                     'changed_by_new_evidence': row['mounts']['P'].get('rehop', {}).get('text') != b_text})
        row['offline'] = phys[-1]
    pc = [x for x in phys if not x['held_out']]
    h5 = rate865([x['P_correct'] for x in pc])
    h5r = rate865([x['RANDOM_correct'] for x in pc])
    t5 = sign_test865([x['P_correct'] for x in pc], [x['RANDOM_correct'] for x in pc])
    H['H5'] = dict(h5, random_mount=h5r, no_mount=rate865([x['no_mount_correct'] for x in pc]), sign_test=t5,
                   threshold=0.75, minus_random_threshold=0.40,
                   status='PASS' if h5['n'] == 18 and (h5['rate'] or 0) >= 0.75 and
                   (h5['rate'] or 0) - (h5r['rate'] or 0) >= 0.40 and t5['p_two_sided'] <= ALPHA865 else 'FAIL')
    # ---------------- GATE 6 loops ----------------
    def loop_correct(r):
        spec = specs[r['item']]
        w = W[spec['world_index']]
        a = r.get('accepted_candidate')
        if r.get('end') != 'MODEL_ACCEPT' or not a:
            return False
        if spec['condition'] == 'HOP3':
            ids = w['ids']
            return env['node851'](a, w) == 'end3' and {ids['first'], ids['second'], ids['third']} <= set(r['final_mounted'])
        return bool(env['supported851'](a, w, set(r['final_mounted'])))
    for r in STATE865['loops']:
        r['offline'] = {'correct_accept': loop_correct(r),
                        'false_accept': r.get('end') == 'MODEL_ACCEPT' and not loop_correct(r),
                        'accepted_class': env['node851'](r.get('accepted_candidate') or '', W[specs[r['item']]['world_index']])}
        fl = r.get('flags', {})
        strict = (r['arm'] == 'NATIVE_P' and r['offline']['correct_accept'] and r.get('acquisitions', 0) >= 1 and
                  fl.get('unmount', 0) == 0 and fl.get('backtrack', 0) == 0 and fl.get('attribution', 0) == 0 and
                  fl.get('later_try_accepts', 0) == 0 and fl.get('first_try_accepts', 0) >= 1)
        r['offline']['strict_native_chain'] = strict
        r['offline']['adapter_assisted_completion'] = r['offline']['correct_accept'] and not strict and r['arm'] == 'NATIVE_P'
    def L(arm, held, conds=('LIVE', 'REMOVED', 'HOP3')):
        out = {}
        for r in STATE865['loops']:
            if r['arm'] == arm and r['held_out'] == held and r['condition'] in conds:
                out[r['item']] = r
        return out
    nat, noa, rnd = L('NATIVE_P', False), L('NO_ACQUISITION', False), L('RANDOM_QUERY', False)
    keys = sorted(nat)
    a6 = [nat[k]['offline']['correct_accept'] for k in keys]
    b6 = [noa[k]['offline']['correct_accept'] if k in noa else False for k in keys]
    c6 = [rnd[k]['offline']['correct_accept'] if k in rnd else False for k in keys]
    h6 = rate865(a6)
    t6a, t6b = sign_test865(a6, b6), sign_test865(a6, c6)
    g_noa = (h6['rate'] or 0) - (rate865(b6)['rate'] or 0)
    g_rnd = (h6['rate'] or 0) - (rate865(c6)['rate'] or 0)
    H['H6'] = dict(h6, NO_ACQUISITION=rate865(b6), RANDOM_QUERY=rate865(c6), gap_vs_no_acquisition=g_noa,
                   gap_vs_random_query=g_rnd, sign_test_vs_no_acquisition=t6a, sign_test_vs_random_query=t6b,
                   strict_native_chain=rate865([nat[k]['offline']['strict_native_chain'] for k in keys]),
                   not_run_budget=sum(1 for k in keys for d in (nat, noa, rnd) if k in d and d[k]['end'] == 'NOT_RUN_BUDGET'),
                   threshold=0.50, status='PASS' if h6['n'] == 27 and (h6['rate'] or 0) >= 0.50 and g_noa >= 0.30 and
                   g_rnd >= 0.30 and t6a['p_two_sided'] <= ALPHA865 and t6b['p_two_sided'] <= ALPHA865 else 'FAIL')
    if H['H6']['status'] == 'FAIL' and H['H6']['not_run_budget']:
        H['H6']['status'] = 'INCOMPLETE_BUDGET'
    # ---------------- GATE 7 false acceptance / traps ----------------
    trap_rows = []
    for t in STATE865['traps']:
        spec = specs[t['item']]
        w = W[spec['world_index']]
        if t.get('status') != 'REHOP_EVALUATED':
            trap_rows.append({'control': t['control'], 'held_out': t['held_out'], 'evaluated': False})
            continue
        supported = bool(env['supported851'](t['rehop']['text'].strip(), w, set(t['mount']['mount'])))
        t['offline'] = {'local_acceptance': t['local_acceptance'], 'trap_accept': t['local_acceptance'] and not supported,
                        'node_class': env['node851'](t['rehop']['text'], w), 'card_class': cls(t.get('chosen'), w['middle'],
                                                                                                spec['world_index'])}
        trap_rows.append({'control': t['control'], 'held_out': t['held_out'], 'evaluated': True, **t['offline']})
    missing = [r for r in STATE865['loops'] if r['condition'] == 'MISSING']
    H['H7'] = {'per_control': {c: rate865([x['trap_accept'] for x in trap_rows if x['control'] == c and x['evaluated']])
                               for c in TRAP_CONTROLS865},
               'missing_loops_false_accept': rate865([r['offline']['false_accept'] for r in missing]),
               'missing_loops_model_stop': rate865([r.get('end') == 'MODEL_STOP' for r in missing]),
               'missing_loops_ends': {e: sum(1 for r in missing if r.get('end') == e) for e in sorted({r.get('end') for r in missing})},
               'status': 'MEASURED'}
    stops = [r for r in STATE865['loops'] if r.get('end') == 'MODEL_STOP']
    stops_after = [r for r in stops if any(e['type'] == 'ACQUIRE' for e in r.get('events', []))]
    H['H8'] = {'model_stop_total': len(stops), 'model_stop_after_real_acquisition': len(stops_after),
               'items': [(r['item'], r['arm']) for r in stops], 'status': 'OBSERVED' if stops_after else 'NOT_OBSERVED'}
    held = {}
    for arm in ('P', 'CUE_QUESTION_ONLY', 'RANDOM_NORM_MATCHED', 'SHUFFLED_KEYS', 'V1_IDENTITY_REMAP'):
        held['address_' + arm] = rate865(pick(True, arm))
    held['v1_identity_causal'] = rate865(pick(False, 'V1_IDENTITY_REMAP'))
    held['physical_P_correct'] = rate865([x['P_correct'] for x in phys if x['held_out']])
    for arm in LOOP_ARMS865:
        held['loop_' + arm] = rate865([r['offline']['correct_accept'] for r in L(arm, True).values()])
    held['loop_NATIVE_P_strict'] = rate865([r['offline']['strict_native_chain'] for r in L('NATIVE_P', True).values()])
    H['HELD_OUT'] = dict(held, status='REPORT_ONLY')
    ablation = [rv['ablation_CEU_K0'] for r in STATE865['loops'] for rv in r.get('reviews', [])
                if (rv.get('ablation_CEU_K0') or {}).get('status') == 'EXECUTED']
    H['REVIEW_ABLATION'] = {'n': len(ablation), 'agreement': rate865([a['agrees_with_full_review'] for a in ablation]),
                            'status': 'DIAGNOSTIC'}
    STATE865['hypotheses'] = H
    claim = address_ok and H['H4']['status'] == 'PASS'
    loops_all = [r for r in STATE865['loops'] if r['end'] != 'NOT_RUN_BUDGET']
    def C(status, claimable=True, **kw):
        return dict(kw, status=status if claimable else 'NOT_CLAIMABLE', raw_status=status)
    STATE865['classes'] = {
        'SOURCE_INTEGRITY_PASS': C('PASS' if STATE865['gates'].get('GATE0_SOURCE', {}).get('status') == 'PASS' and
                                   STATE865['gates'].get('GATE1_REGRESSION', {}).get('status') == 'PASS' else 'FAIL'),
        'ADDRESS_CAUSAL_EFFECT': C('PASS' if address_ok else 'FAIL', H1=H['H1']['status'], H2=H['H2']['status'],
                                   H3=H['H3']['status'], meaning='model-derived query + mechanical retrieval'),
        'PHYSICAL_REENTRY_PASS': C(H['H4']['status']),
        'CANDIDATE_CORRECTION': C(H['H5']['status'], claim),
        'MODEL_NATIVE_ACCEPT': C('OBSERVED' if any(r.get('end') == 'MODEL_ACCEPT' for r in loops_all) else 'NOT_OBSERVED',
                                 count=sum(r.get('end') == 'MODEL_ACCEPT' for r in loops_all),
                                 false_accepts=sum(r['offline']['false_accept'] for r in loops_all)),
        'MODEL_NATIVE_STOP': C(H['H8']['status'], count_after_acquisition=H['H8']['model_stop_after_real_acquisition']),
        'ADAPTER_ASSISTED_COMPLETION': C('OBSERVED' if any(r['offline']['adapter_assisted_completion'] for r in loops_all)
                                         else 'NOT_OBSERVED', claim,
                                         count=sum(r['offline']['adapter_assisted_completion'] for r in loops_all)),
        'MECHANICAL_BUDGET_STOP': C('OBSERVED' if any(r.get('mechanical_end') for r in STATE865['loops']) else 'NOT_OBSERVED',
                                    ends={e: sum(1 for r in STATE865['loops'] if r.get('end') == e and r.get('mechanical_end'))
                                          for e in sorted({r.get('end') for r in STATE865['loops'] if r.get('mechanical_end')})}),
        'DIAGNOSTIC_REPLAY_ONLY': C('EXECUTED', items=['GATE7 singleton traps', 'GATE1 root 2x2', 'review ablation']),
        'NATIVE_AUTONOMOUS_CLOSURE': C('OBSERVED' if H['H6']['status'] == 'PASS' and H['H6']['strict_native_chain']['k'] > 0
                                       else 'NOT_OBSERVED', claim and H['H5']['status'] == 'PASS',
                                       strict_count=H['H6']['strict_native_chain']['k'],
                                       composition='MODEL_UNKNOWN_OR_REVISE_TRIGGER + MODEL_POINTER_QUERY + MECHANICAL_LABEL_FREE_RETRIEVAL'
                                                   ' + MODEL_REHOP_ACCEPTANCE + MODEL_CONTINUE; first-try, no retry/backtrack'),
        'NOT_CLAIMABLE': {'status': 'APPLIED' if not claim else 'NOT_APPLIED',
                          'reason': None if claim else 'ADDRESS_CAUSAL_EFFECT or PHYSICAL_REENTRY failed'}}
    STATE865['gates'].update({
        'GATE2_POINTER': {'status': 'EXECUTED', 'valid_P': sum(p.get('hop0_kind') == 'NODE' for p in STATE865['pointer']),
                          'n': len(STATE865['pointer'])},
        'GATE3_ADDRESS': {'status': 'PASS' if address_ok else 'FAIL'},
        'GATE4_PHYSICAL': {'status': H['H4']['status']},
        'GATE5_CANDIDATE': {'status': H['H5']['status'] if claim else 'NOT_CLAIMABLE'},
        'GATE6_CLOSURE': {'status': H['H6']['status'] if claim and H['H5']['status'] == 'PASS' else 'NOT_CLAIMABLE'},
        'GATE7_TRAPS': {'status': 'MEASURED'},
        'GATE8_HELD_OUT': {'status': 'REPORT_ONLY'}})
    STATE865['offline'] = {'addressing_rows': rows, 'physical_rows': phys, 'trap_rows': trap_rows}
    with (ROOT864 / '865_addressing.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['item', 'condition', 'held_out', 'arm', 'chosen', 'hit1', 'hit3', 'hit5', 'best_valid_rank',
                         'class', 'margin', 'valid_set_size'])
        for r in rows:
            for arm, v in r.items():
                if isinstance(v, dict) and 'chosen' in v:
                    writer.writerow([r['item'], r['condition'], r['held_out'], arm, v.get('chosen'), v.get('hit1'),
                                     v.get('hit3'), v.get('hit5'), v.get('best_valid_rank'), v.get('class'),
                                     v.get('margin'), v.get('valid_set_size')])
    with (ROOT864 / '865_loops.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['item', 'condition', 'held_out', 'arm', 'end', 'accepted', 'correct_accept', 'false_accept',
                         'strict_native_chain', 'acquisitions', 'hops', 'reviews', 'actions', 'final_mounted'])
        for r in STATE865['loops']:
            writer.writerow([r['item'], r['condition'], r['held_out'], r['arm'], r.get('end'), r.get('accepted_candidate'),
                             r.get('offline', {}).get('correct_accept'), r.get('offline', {}).get('false_accept'),
                             r.get('offline', {}).get('strict_native_chain'), r.get('acquisitions'), r.get('hops'),
                             len(r.get('reviews', [])), '>'.join(x['action'] for x in r.get('reviews', [])),
                             '|'.join(r.get('final_mounted', []))])
    return H


# ======================================================================================================================
# Report / manifest
# ======================================================================================================================
def partial_report865():
    return {'test': 865, 'kind': TEST865_KIND, 'status': 'INCOMPLETE', 'gpu_execution_claimed_by_author': False,
        'preregistered': PREREG865, 'preregistered_sha256': PREREG_SHA865, 'source': STATE865['source'],
        'budget': STATE865['budget'], 'gates': STATE865['gates'], 'classes': STATE865['classes'],
        'hypotheses': STATE865['hypotheses'], 'original_native': STATE865['original_native'],
        'root864': STATE865['root'], 'pointer': STATE865['pointer'], 'addressing': STATE865['addressing'],
        'physical': STATE865['physical'], 'traps': STATE865['traps'], 'loops': STATE865['loops'],
        'inventory': STATE865['inventory'], 'negative': STATE865['negative'], 'timings': STATE865['timings'],
        'error': ERROR865, 'traceback': TRACEBACK865,
        'interpretation_rules': ['UNKNOWN->acquisition is a fixed adapter protocol executing a model output',
            'retrieval is a fixed label-free GPU PEAK50 argmax over physical H3 rows (engineering, not cognition)',
            'retries, unmounts, attribution and backtracking are mechanical (ADAPTER_ASSISTED)',
            'integrity PASS or a correct answer alone is never evidence of native autonomous closure']}


def finalize865(success):
    report = partial_report865()
    peak = torch.cuda.max_memory_allocated() / 1024**3 if torch.cuda.is_available() else None
    report['peak_gpu_gib'] = peak
    report['wall_seconds'] = round(time.perf_counter() - START864, 3)
    technical = {'source_locks': STATE865['source'].get('lock_count') == len(LOCKS864),
        'firewall': STATE865['source'].get('firewall', {}).get('status') == 'PASS',
        'regression': STATE865['gates'].get('GATE1_REGRESSION', {}).get('status') == 'PASS',
        'executed_source_saved': (ROOT864 / '865.py').is_file(), 'experiment_completed': bool(success),
        'no_loop_execution_error': all(r.get('end') != 'EXECUTION_ERROR' for r in STATE865['loops'])}
    report['technical_gates'] = technical
    report['status'] = 'TEST865_TECHNICAL_EXECUTION_COMPLETE' if success and all(technical.values()) else 'UNRESOLVED'
    json_write865('865_report.json', report)
    with (ROOT864 / '865_events.jsonl').open('w', encoding='utf-8') as handle:
        for row in EVENTS865:
            handle.write(json.dumps(row, ensure_ascii=False, default=str) + '\n')
    names = ['865.py', '865.log', '865_report.json', '865_events.jsonl', '865_addressing.csv', '865_loops.csv']
    manifest = {}
    LOG_FILE864.flush()
    for name in names:
        path = ROOT864 / name
        manifest[name] = ({'bytes': path.stat().st_size, 'sha256': sha256_file865(path)} if path.is_file()
                          else {'status': 'NOT_AVAILABLE'})
    json_write865('865_manifest.json', manifest)
    short865('TEST865 STATUS', report['status'], json.dumps(technical))
    short865('TEST865 CLASSES', json.dumps({k: v.get('status') for k, v in STATE865['classes'].items()}))
    short865('TEST865 HYPOTHESES', json.dumps({k: v.get('status') for k, v in STATE865['hypotheses'].items()}))
    short865('TEST865 PEAK_GPU_GIB', peak, 'WALL_S', report['wall_seconds'], 'FILES', str(ROOT864))
    short865('GPU EXECUTION NOT VERIFIED BY THE CODE AUTHOR; this run is the first execution.')
    return report, manifest




# ============================ TEST866 MODEL-NATIVE RECURSIVE CONTROLLER ============================
# Everything above this line is the locked TEST865 cell (865.py, git blob 9a0ba587...), byte-identical except the header,
# ROOT and log name. It supplies the physical engine (sources, SHA locks, CUT3 mount, H3/PEAK50 router, native hop) and the
# PY865_REFERENCE comparison arm (loop865 with its Python rules, run unchanged and labelled as a Python-rule reference).
# TEST866 adds ONE controller for all model arms: loop866. In loop866 Python never chooses a cognitive transition:
#   * every transition (advance, acquire, reject, backtrack, accept, stop) is the literal word the model generated;
#   * the physical address of an ACQUIRE or REJECT is the soft-row state of a node name the model generated;
#   * Python only executes that word (pointer push/pop, PEAK50 route, SHA load, CUT3 mount/unmount) and records it.
# Removed from model control (present only in the PY865_REFERENCE arm): S=3 retries, UNKNOWN->automatic acquisition,
# UNKNOWN-after-mount->automatic unmount, NULL-substitution attribution, dead-end retract/backtrack, MAX_CARDS=5,
# MAX_HOPS=14, MAX_REVIEWS=2, REVISE->automatic acquisition, Python veto of ADVANCE/BACKTRACK, 'pending card' bookkeeping.
# Mechanical ends that remain (never counted as model STOP, always counted as failure for the model):
#   OBSERVATION_HORIZON (20 control steps, identical for every model arm), RESOURCE_BUDGET (wall clock / call allowance),
#   NATIVE_EMPTY_OUTPUT / NATIVE_EMPTY_STATE (the model emitted no rows, nothing can be transferred),
#   MODEL_INVALID_ACTION (strict one-word parser, the same law as locked parse849), PHYSICAL_CONTEXT_LIMIT, EXECUTION_ERROR.
import gzip
TEST866_KIND = 'MODEL_NATIVE_RECURSIVE_CONTROL_WITH_PHYSICAL_EVIDENCE'
LOCKS864.update({'865.py': '9a0ba587d36466638d9391621f29540bfed5a539',
                 '865.log': 'b6415d65efceb542df12f5597da5a6bd0aa86b9d'})
CAUSAL_WORLDS866 = tuple(range(9))
EVALUATION_WORLDS866 = (9, 10, 11)
ALL_WORLDS866 = CAUSAL_WORLDS866 + EVALUATION_WORLDS866
CONDITIONS866 = ('LIVE', 'FORK', 'HOP3', 'MISSING', 'SUFFICIENT')
PRIMARY_CONDITIONS866 = ('LIVE', 'FORK', 'HOP3')
MODEL_ARMS866 = ('MODEL_CONTROL', 'NO_ACQUISITION', 'RANDOM_ADDRESS', 'SHUFFLED_STATE')
REFERENCE_ARM866 = 'PY865_REFERENCE'
ARM_MATRIX866 = {
    ('CAUSAL', 'LIVE'): ('MODEL_CONTROL', 'NO_ACQUISITION', 'RANDOM_ADDRESS', 'SHUFFLED_STATE', 'PY865_REFERENCE'),
    ('CAUSAL', 'FORK'): ('MODEL_CONTROL', 'NO_ACQUISITION', 'RANDOM_ADDRESS', 'SHUFFLED_STATE', 'PY865_REFERENCE'),
    ('CAUSAL', 'HOP3'): ('MODEL_CONTROL', 'NO_ACQUISITION', 'RANDOM_ADDRESS', 'SHUFFLED_STATE', 'PY865_REFERENCE'),
    ('CAUSAL', 'MISSING'): ('MODEL_CONTROL', 'SHUFFLED_STATE', 'PY865_REFERENCE'),
    ('CAUSAL', 'SUFFICIENT'): ('MODEL_CONTROL', 'PY865_REFERENCE'),
    ('EVALUATION', 'LIVE'): ('MODEL_CONTROL', 'RANDOM_ADDRESS', 'PY865_REFERENCE'),
    ('EVALUATION', 'FORK'): ('MODEL_CONTROL', 'RANDOM_ADDRESS', 'PY865_REFERENCE'),
    ('EVALUATION', 'HOP3'): ('MODEL_CONTROL', 'RANDOM_ADDRESS', 'PY865_REFERENCE'),
    ('EVALUATION', 'MISSING'): ('MODEL_CONTROL', 'PY865_REFERENCE'),
    ('EVALUATION', 'SUFFICIENT'): ('MODEL_CONTROL', 'PY865_REFERENCE')}
TRAP_CONTROLS866 = ('REVERSED_EDGE', 'SHARED_NODE', 'DECOY')
TRAP_ARMS866 = ('MODEL_CONTROL', 'SHUFFLED_STATE')
ACTIONS866 = ('ADVANCE', 'ACQUIRE', 'REJECT', 'BACKTRACK', 'ACCEPT', 'STOP')
HORIZON866 = 20                         # observation horizon in model control steps; identical for every model arm
TEST866_MINUTES = 330.0
TEST865_MINUTES = TEST866_MINUTES       # shared wall-clock accounting read by the locked budget_left865/rearm_budget865
CALL_ALLOWANCE865 = 26000               # shared generator-call allowance read by the locked rearm_budget865
STEP_CALLS866 = 8                       # calls reserved before one model step (hop, evidence, evaluation, action, direction)
ALPHA866 = 0.05
RANDOM_SEED866 = 8662027
END_CLASSES866 = {
    'MODEL_ACCEPT': 'MODEL', 'MODEL_STOP': 'MODEL',
    'MODEL_INVALID_ACTION': 'MECHANICAL_PROTOCOL_PARSE', 'NATIVE_EMPTY_OUTPUT': 'MECHANICAL_NO_NATIVE_ROWS',
    'NATIVE_EMPTY_STATE': 'MECHANICAL_NO_NATIVE_ROWS', 'OBSERVATION_HORIZON': 'MECHANICAL_OBSERVATION_LIMIT',
    'RESOURCE_BUDGET': 'MECHANICAL_RESOURCE', 'PHYSICAL_CONTEXT_LIMIT': 'MECHANICAL_RESOURCE',
    'EXECUTION_ERROR': 'MECHANICAL_ERROR'}
EFFECTS866 = ('POINTER_ADVANCED', 'POINTER_RETRACTED', 'NO_EFFECT_AT_ROOT', 'MOUNTED', 'UNMOUNTED',
              'NO_EFFECT_ACQUISITION_DISABLED_BY_ARM', 'NO_EFFECT_EMPTY_DIRECTION', 'NO_EFFECT_BANK_EXHAUSTED',
              'NO_EFFECT_EMPTY_MEMORY')
MODEL_LOOP_FUNCTIONS866 = ('loop866', 'control_step866', 'direction866', 'address866', 'execute866', 'segments866',
                           'parse866')
FORBIDDEN_CONTROL866 = {'S_LIMIT865', 'MAX_CARDS865', 'MAX_HOPS865', 'MAX_REVIEWS865', 'acquire865', 'unmount865',
                        'attribute865', 'review_step865', 'terminal_review865', 'loop865', 'plan845', 'attrib845',
                        'parse849', 'UNKNOWN', 'NODE', 'UNKNOWN_explicit', 'empty_output', 'tries', 'XN', 'pending',
                        'first_try_accepts', 'later_try_accepts'}
EVALUATION_PROMPT866 = '''Question: {q}
The numerical context contains the latest candidate produced from the current reasoning node, an independently computed answer from the mounted physical evidence, their relation, the current reasoning node when reasoning has advanced, and your previous control state when one exists. Evaluate in a few words whether the latest candidate is a supported step toward answering the question and what is missing. Use only mounted physical evidence and do not invent evidence.'''
CONTROL_PROMPT866 = '''Question: {q}
The numerical context contains the latest candidate produced from the current reasoning node, an independently computed answer from the mounted physical evidence, their relation, the current reasoning node when reasoning has advanced, your previous control state when one exists, and your own evaluation. Decide the next reasoning action.
ADVANCE means the latest candidate is a valid intermediate node; reasoning continues from it.
ACQUIRE means the mounted physical evidence is insufficient; one more physical record will be retrieved, and you will name the node whose outgoing record is needed.
REJECT means a mounted physical record is misleading or invalid; you will name the node that record leads to, and it will be removed.
BACKTRACK means the current reasoning node was a wrong step; reasoning returns to the previous node.
ACCEPT means the latest candidate completely answers the question and is returned as the final answer.
STOP means the question cannot be answered from the available physical evidence; reasoning ends without an answer.
Reply with exactly one word: ADVANCE, ACQUIRE, REJECT, BACKTRACK, ACCEPT, or STOP.'''
DIRECTION_PROMPT866 = {
    'ACQUIRE': '''Question: {q}
You decided ACQUIRE. The numerical context contains the latest candidate, the independent answer, their relation, the current reasoning node when reasoning has advanced, your evaluation and your decision. Name the single node whose outgoing directed relation record must be retrieved next from physical memory. Reply with the node name only.''',
    'REJECT': '''Question: {q}
You decided REJECT. The numerical context contains the latest candidate, the independent answer, their relation, the current reasoning node when reasoning has advanced, your evaluation and your decision. Name the node that the misleading mounted directed relation record leads to (its target node); that record will be removed. Reply with the node name only.'''}
SLOT_TEXT866 = {'POINTER': 'Current reasoning node numerical state:', 'EVALUATION': 'Own evaluation numerical state:',
                'ACTION': 'Current control decision numerical state:', 'EVALUATION_SUFFIX': '\nEvaluation:',
                'DIRECTION_SUFFIX': '\nNode name:'}
SLOTS866 = {}
PREREG866 = {
    'mechanism': 'Per step: native hop (locked hop865) -> native evidence E (locked EVIDENCE851) -> R=relation852(C,E) -> '
                 'native evaluation V over [C,E,R,P,Kprev] -> native action over [C,E,R,P,Kprev,V] -> for ACQUIRE/REJECT a '
                 'native node-name generation whose soft rows are the physical address (index_embeds841 -> h3_bypass841 -> '
                 'PEAK50 route841). Kprev is the previous action state (recursion).',
    'python_role': 'Executes the literal model word only: ADVANCE push pointer; BACKTRACK pop pointer; ACQUIRE route the '
                   'model-named current node over pool minus mounted and mount; REJECT route the model-named target node '
                   'over mounted cards and unmount; ACCEPT/STOP end. No retry counts, card caps, attribution, automatic mount/unmount or vetoes.',
    'mechanical_ends': END_CLASSES866, 'effects': list(EFFECTS866), 'horizon_steps': HORIZON866,
    'source_separation': {'A_model': 'hop, evidence, evaluation, action and direction text plus soft rows',
                          'B_python_io': 'strict word parse, pointer stack, PEAK50, SHA I/O, CUT3 mount, resource limits',
                          'C_offline': 'condition construction before execution and locked scoring after execution'},
    'conditions': {'LIVE': '[first]; second needed from pool', 'FORK': '[first, fork] (865 REMOVED memory); a dead-end branch '
                   'exists from start; second needed', 'HOP3': '[first]; three links, second and third needed',
                   'MISSING': '[first]; second and changed removed from pool; no supported answer exists',
                   'SUFFICIENT': '[first, second]; complete chain already mounted'},
    'dropped_draft_condition': 'CONTRADICT=[first, changed] was dropped: locked supported851 counts changed_end as a '
                               'supported answer when changed is mounted, so a wrong-candidate label has no evidence signal.',
    'arms': {'MODEL_CONTROL': 'full model control', 'NO_ACQUISITION': 'ACQUIRE executes no mount (sham); all else identical',
             'RANDOM_ADDRESS': 'model words kept; ACQUIRE/REJECT address rows replaced by norm-matched random rows',
             'SHUFFLED_STATE': 'C,E,R slot contents permuted (C<-E, E<-R, R<-C) in evaluation, action and direction',
             'PY865_REFERENCE': 'locked loop865 NATIVE_P with its Python rules; comparison only, never mixed into model arms'},
    'arm_matrix': {a + '/' + b: list(v) for (a, b), v in ARM_MATRIX866.items()},
    'unit': 'world x condition item; arms paired on the same initial memory, question and blind pool; intention-to-treat',
    'scoring': 'correct = MODEL_ACCEPT of supported851 answer given final mounted cards; HOP3 = end3 with first, second, third',
    'H1_closure': {'population': 'causal LIVE+FORK+HOP3 (n=27) MODEL_CONTROL', 'min_rate': 0.50,
                   'min_gap_vs_NO_ACQUISITION': 0.30, 'sign_p_max': ALPHA866},
    'H2_model_address': {'population': 'same 27 items, MODEL_CONTROL vs RANDOM_ADDRESS',
                         'min_correct_accept_gap': 0.30, 'min_loop_valid_acquisition_gap': 0.20, 'sign_p_max': ALPHA866},
    'H3_state_reading': {'population': 'same 27 items, MODEL_CONTROL vs SHUFFLED_STATE', 'min_correct_accept_gap': 0.20,
                         'sign_p_max': ALPHA866},
    'H4_provenance': 'static purity audit PASS and 100 percent of model-arm transitions caused by a literal model word',
    'H5_false_acceptance': {'MISSING_MODEL_CONTROL_accept_max': 0.10, 'trap_ACCEPT_max': 0.25},
    'H6_trap_validity': {'population': 'causal LIVE forced trap probes (9 x 3) per arm', 'metric': 'REJECT or BACKTRACK',
                         'min_rate': 0.40, 'min_gap_vs_SHUFFLED_STATE': 0.20},
    'H7_dead_end': 'FORK: model BACKTRACK/REJECT usage and closure, report only',
    'H8_stopping': 'MISSING literal STOP, SUFFICIENT acceptance without acquisition, report only',
    'H9_python_reference': 'paired MODEL_CONTROL vs PY865_REFERENCE per condition, report only, no threshold',
    'H10_evaluation_worlds': 'worlds 9-11 report only; they appear in the inspected 865 log, so they are not new-to-design',
    'claim_rule': 'MODEL_CONTROLLED_CLOSURE claimable only if H1, H2, H3, H4 and physical integrity pass. A correct answer '
                  'or a valid mount alone is not autonomous reasoning. Mechanical ends are never model STOP.',
    'uncertainty': 'Wilson 95 percent intervals and exact two-sided sign tests on discordant pairs',
    'budgets': {'wall_minutes': TEST866_MINUTES, 'generator_allowance': CALL_ALLOWANCE865, 'horizon_steps': HORIZON866}}
PREREG_SHA866 = sha256_bytes864(json.dumps(PREREG866, sort_keys=True).encode('utf-8'))
STATE866 = {'source': {}, 'gates': {}, 'specs': {}, 'loops': [], 'traps': [], 'hypotheses': {},
            'offline': {}, 'original_native': {}, 'negative': {}, 'timings': {}}
EVENTS866 = []
EVENTS865 = EVENTS866                    # locked mount events and TEST866 events share one chronological stream
EVENTS_FILE866 = open(ROOT864 / '866_events.jsonl', 'w', encoding='utf-8')
ERROR866 = None
TRACEBACK866 = ''
T0_866 = None
short866 = short864
table866 = table864
json_write866 = json_write864
sha256_file866 = sha256_file864


def event866(kind, source, **payload):
    row = {'kind': kind, 'source': source, 't_s': round(time.perf_counter() - START864, 3)}
    if torch.cuda.is_available():
        row['gpu_alloc_gib'] = round(torch.cuda.memory_allocated() / 1024**3, 3)
    row.update(payload)
    EVENTS866.append(row)
    EVENTS_FILE866.write(json.dumps(row, ensure_ascii=False, default=str) + '\n')
    EVENTS_FILE866.flush()
    return row


# ============================ GATE 0: source, locked-865 identity, firewall, control purity ============================
def capture_cell_source866():
    shell = get_ipython()
    history = list(shell.history_manager.input_hist_raw)
    marker = 'AKBASCORE SILICON HIPPOCAMPUS — TEST866'
    candidates = [text for text in history if marker in text]
    assert candidates, 'EXECUTED_866_SOURCE_NOT_CAPTURED'
    source = candidates[-1]
    ast.parse(source)
    (ROOT864 / '866.py').write_text(source, encoding='utf-8')
    assert (ROOT864 / '866.py').read_text(encoding='utf-8') == source
    STATE866['source']['executed_cell_sha256'] = sha256_bytes864(source.encode('utf-8'))
    return source


def verify_locked865_866(executed_source):
    source865 = source_text865('865.py')
    log865 = source_text865('865.log')
    assert git_blob864(source865.encode()) == LOCKS864['865.py']
    assert git_blob864(log865.encode()) == LOCKS864['865.log']
    for snippet in ('NVIDIA A100-SXM4-80GB', 'TEST865 STATUS TEST865_TECHNICAL_EXECUTION_COMPLETE',
                    '"PHYSICAL_REENTRY_PASS": "PASS"', '"H1": "PASS"', '"H2": "PASS"'):
        assert snippet in log865, ('LOCKED865_GPU_LOG_EVIDENCE_MISSING', snippet)
    match = re.search(r'TEST865 PEAK_GPU_GIB ([0-9.]+) WALL_S ([0-9.]+)', log865)
    assert match, 'LOCKED865_GPU_RESOURCES_NOT_PARSEABLE'
    remote = ast.parse(source865)
    local = ast.parse(executed_source)
    remote_funcs = [n.name for n in remote.body if isinstance(n, ast.FunctionDef)]
    comparisons = {}
    for name in remote_funcs:                       # every 865 function must be byte-identical in AST
        r = [n for n in remote.body if isinstance(n, ast.FunctionDef) and n.name == name]
        l = [n for n in local.body if isinstance(n, ast.FunctionDef) and n.name == name]
        assert len(r) == len(l) == 1, ('REUSED_865_FUNCTION_NOT_UNIQUE', name)
        equal = ast.dump(r[0], include_attributes=False) == ast.dump(l[0], include_attributes=False)
        assert equal, ('REUSED_865_FUNCTION_CHANGED', name)
        comparisons[name] = sha256_bytes864(ast.dump(r[0], include_attributes=False).encode())
    STATE866['source']['locked865'] = {
        'source_git_blob': LOCKS864['865.py'], 'log_git_blob': LOCKS864['865.log'],
        'gpu_log_evidence': 'REAL_A100_EXECUTION_IN_LOCKED_865_LOG_NOT_IN_CURRENT_TEST866',
        'peak_gpu_gib_865': float(match.group(1)), 'wall_seconds_865': float(match.group(2)),
        'functions_ast_identical': len(comparisons), 'function_ast_sha256': comparisons,
        'reused_physical_engine': ['hop865', 'pointer_query865', 'route_blind865', 'random_matched865', 'mount865',
                                   'free865', 'prefix_seals865', 'inventory865', 'full_h865', 'budget_left865'],
        'python_rules_only_in_PY865_REFERENCE': ['S_LIMIT865 retries', 'UNKNOWN->acquire865', 'UNKNOWN after mount->unmount865',
                                                 'attribute865', 'dead-end backtrack', 'MAX_CARDS865', 'MAX_HOPS865',
                                                 'MAX_REVIEWS865', 'REVISE->acquire865']}
    table866('GATE0 LOCKED865', integrity='PASS', payload={k: v for k, v in STATE866['source']['locked865'].items()
                                                           if k != 'function_ast_sha256'})


def firewall_audit866(tree):
    setup = ('build_specs866',)
    offline = ('offline_evaluate866', 'valid_for866', 'card_class866', 'correct866', 'write_csv866')
    audits = ('firewall_audit866', 'purity_audit866')
    forbidden = set(OFFLINE_NAMES865) | {'correct866', 'valid_for866', 'card_class866', 'offline_evaluate866'}
    violations = {}
    online = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or not node.name.endswith('866'):
            continue
        if node.name in setup + offline + audits:
            continue
        online.append(node.name)
        names = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
        names |= {n.attr for n in ast.walk(node) if isinstance(n, ast.Attribute)}
        names |= {n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
        used = sorted(names & forbidden)
        if used:
            violations[node.name] = used
    assert not violations, ('OFFLINE_LABEL_FIREWALL', violations)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in ('backward', 'step', 'register_forward_hook',
                                          'register_forward_pre_hook', 'load_state_dict'), node.func.attr
    STATE866['source']['firewall'] = {'status': 'PASS', 'online_functions': online,
        'condition_construction_only': list(setup), 'offline_only': list(offline),
        'forbidden_names': sorted(forbidden), 'violations': violations}
    table866('GATE0 FIREWALL866', integrity='PASS', payload=STATE866['source']['firewall'])


def purity_audit866(tree):
    # Static proof of what Python can do inside model control. Every branch condition is published verbatim.
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    missing = [n for n in MODEL_LOOP_FUNCTIONS866 if n not in funcs]
    assert not missing, ('MODEL_LOOP_FUNCTION_MISSING', missing)
    violations, branches = {}, {}
    for name in MODEL_LOOP_FUNCTIONS866:
        node = funcs[name]
        names = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
        names |= {n.attr for n in ast.walk(node) if isinstance(n, ast.Attribute)}
        names |= {n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
        bad = sorted(names & FORBIDDEN_CONTROL866)
        if bad:
            violations[name] = bad
        branches[name] = [ast.unparse(n.test) for n in ast.walk(node) if isinstance(n, (ast.If, ast.While, ast.IfExp))]
    assert not violations, ('PYTHON_COGNITIVE_RULE_IN_MODEL_CONTROL', violations)

    def constants(value):
        if isinstance(value, ast.Constant):
            return {value.value} - {None}
        if isinstance(value, ast.IfExp):
            return constants(value.body) | constants(value.orelse)
        assert False, ('NON_LITERAL_ASSIGNMENT', ast.unparse(value))

    def assigned(node, target):
        out = set()
        for n in ast.walk(node):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name) and t.id == target:
                        out |= constants(n.value)
                    if isinstance(t, ast.Tuple) and isinstance(n.value, ast.Tuple):
                        for a, b in zip(t.elts, n.value.elts):
                            if isinstance(a, ast.Name) and a.id == target:
                                out |= constants(b)
        return out
    ends = assigned(funcs['loop866'], 'end')
    effects = assigned(funcs['execute866'], 'effect')
    assert ends == set(END_CLASSES866), ('UNDECLARED_LOOP_END', sorted(ends ^ set(END_CLASSES866)))
    assert effects <= set(EFFECTS866), ('UNDECLARED_EFFECT', sorted(effects - set(EFFECTS866)))
    model_ends = sorted(e for e, c in END_CLASSES866.items() if c == 'MODEL')
    STATE866['source']['purity'] = {'status': 'PASS', 'functions': list(MODEL_LOOP_FUNCTIONS866),
        'forbidden_python_rules': sorted(FORBIDDEN_CONTROL866), 'violations': violations,
        'loop_ends': {e: END_CLASSES866[e] for e in sorted(ends)}, 'model_ends': model_ends,
        'effects': sorted(effects), 'python_branch_inventory': branches,
        'statement': 'Python branches only on: the literal model word, the arm label, empty native rows, an empty '
                     'candidate set, the observation horizon and the resource budget; the remaining branches only '
                     'restore memory or format logs.'}
    table866('GATE0 PURITY866', integrity='PASS', payload=STATE866['source']['purity'])


def make_slots866(env):
    for name, text in SLOT_TEXT866.items():
        SLOTS866[name] = list(env['tok'](text, add_special_tokens=False).input_ids)
        assert SLOTS866[name], ('EMPTY_SLOT_TOKENS', name)
    STATE866['source']['slots'] = {k: {'text': SLOT_TEXT866[k], 'n_tokens': len(v)} for k, v in SLOTS866.items()}


# ============================ CONDITION CONSTRUCTION (setup only; labels never reach the loop) ============================
def build_specs866(env):
    worlds = env['worlds829']
    assert len(worlds) == 12 and env['BLOCK841'] == 3 and len(env['BANKS841']) == 4
    specs = []
    for block in ('CAUSAL', 'EVALUATION'):
        for wi in (CAUSAL_WORLDS866 if block == 'CAUSAL' else EVALUATION_WORLDS866):
            ids = worlds[wi]['ids']
            bank = list(env['BANKS841'][wi // env['BLOCK841']]['v0'])
            for condition in CONDITIONS866:
                initial = {'FORK': [ids['first'], ids['fork']],
                           'SUFFICIENT': [ids['first'], ids['second']]}.get(condition, [ids['first']])
                qid = worlds[wi]['world'] + '_H3' if condition == 'HOP3' else env['QID841'][wi]
                pool = [c for c in bank if c not in initial]
                if condition == 'MISSING':
                    pool = [c for c in pool if c not in (ids['second'], ids['changed'])]
                spec = {'item': 'I866_%02d_%s' % (wi, condition), 'world_index': wi, 'condition': condition,
                        'qid': qid, 'initial': initial, 'pool': pool, 'block': block,
                        'held_out': block == 'EVALUATION', 'arms': list(ARM_MATRIX866[(block, condition)]),
                        'traps': {'REVERSED_EDGE': ids['mirror'], 'SHARED_NODE': ids['fork'], 'DECOY': ids['decoy']}}
                assert qid in env['QTEXT841'] and qid in env['QIDS841']
                assert set(pool) <= set(bank) and not set(initial) & set(pool)
                specs.append(spec)
    STATE866['specs'] = {'rows': specs, 'sha256': sha256_bytes864(json.dumps(specs, sort_keys=True).encode('utf-8'))}
    planned = sum(len(s['arms']) for s in specs)
    STATE866['specs']['planned_loops'] = planned
    table866('M0 SPECS866', payload={'items': len(specs), 'planned_loops': planned, 'sha256': STATE866['specs']['sha256']})
    return specs


# ============================ A: MODEL OUTPUT -> B: NEUTRAL EXECUTION (model control) ============================
def parse866(text):
    value = str(text).strip().upper()          # identical law to locked parse849: exact word or INVALID
    return value if value in ACTIONS866 else 'INVALID'


def segments866(env, arm, c_state, e_state, r_state, pointer, kprev):
    values = [c_state, e_state, r_state]
    if arm == 'SHUFFLED_STATE':
        values = [e_state, r_state, c_state]  # fixed matched slot ablation; no labels involved
    segments = [(env['C_SLOT851'], values[0]), (env['E_SLOT851'], values[1]), (env['R_SLOT852'], values[2])]
    if pointer is not None:
        segments.append((SLOTS866['POINTER'], pointer))
    if kprev is not None:
        segments.append((env['K_SLOT851'], kprev))
    return segments


def control_step866(env, memx, qid, arm, candidate, pointer, previous_control):
    q = env['QTEXT841'][qid]
    c_state = candidate['rows'].detach().float().cpu()
    evidence = env['gen849'](memx, list(env['prompt_ids'](env['EVIDENCE851'].format(q=q))), None, env['ANSWER_SUFFIX851'])
    check_output_h863(evidence, 'CONTROL866_EVIDENCE')
    e_state = evidence['rows'].detach().float().cpu()
    if not c_state.shape[0] or not e_state.shape[0]:
        return None, {'status': 'NATIVE_EMPTY_STATE', 'action': None, 'candidate': full_h865(env, candidate),
                      'evidence': full_h865(env, evidence), 'decision_source': 'MECHANICAL_NO_NATIVE_ROWS'}, None
    r_state = env['relation852'](c_state, e_state)
    kprev = None if previous_control is None else previous_control['rows']
    segments = segments866(env, arm, c_state, e_state, r_state, pointer, kprev)
    evaluation = env['gen851'](memx, list(env['prompt_ids'](EVALUATION_PROMPT866.format(q=q))), segments,
                               SLOTS866['EVALUATION_SUFFIX'])
    check_output_h863(evaluation, 'CONTROL866_EVALUATION')
    v_state = evaluation['rows'].detach().float().cpu()
    action_segments = list(segments) + [(SLOTS866['EVALUATION'], v_state)]
    control = env['gen851'](memx, list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))), action_segments,
                            env['REVIEW_SUFFIX851'])
    check_output_h863(control, 'CONTROL866_ACTION')
    action = parse866(control['text'])
    record = {'status': 'EXECUTED', 'action': action, 'raw': control['text'], 'valid_action': action != 'INVALID',
              'decision_source': 'MODEL', 'candidate': full_h865(env, candidate), 'evidence': full_h865(env, evidence),
              'evaluation': full_h865(env, evaluation), 'control': full_h865(env, control),
              'evaluation_text': evaluation['text'], 'evaluation_rows': int(v_state.shape[0]),
              'control_rows': int(control['rows'].shape[0]), 'top20': control.get('top1'), 'H1': control.get('H1'),
              'state_sha256': {'C': env['stats849'](c_state)['sha256'], 'E': env['stats849'](e_state)['sha256'],
                               'R': env['stats849'](r_state)['sha256'], 'V': env['stats849'](v_state)['sha256'],
                               'P': None if pointer is None else env['stats849'](pointer)['sha256'],
                               'Kprev': None if kprev is None else env['stats849'](kprev)['sha256']},
              'slot_ablation': 'C<-E,E<-R,R<-C' if arm == 'SHUFFLED_STATE' else 'IDENTITY',
              'memory_tokens': int(memx[0][0].shape[-2])}
    return control, record, {'segments': action_segments}


def direction866(env, memx, qid, purpose, state, control):
    q = env['QTEXT841'][qid]
    segments = list(state['segments']) + [(SLOTS866['ACTION'], control['rows'].detach().float().cpu())]
    direction = env['gen851'](memx, list(env['prompt_ids'](DIRECTION_PROMPT866[purpose].format(q=q))), segments,
                              SLOTS866['DIRECTION_SUFFIX'])
    check_output_h863(direction, 'CONTROL866_DIRECTION_' + purpose)
    return direction


def address866(env, ctx, rows, candidates, exclude):
    origin = 'MODEL_NAMED_NODE_SOFT_ROWS'
    if ctx['arm'] == 'RANDOM_ADDRESS' and rows is not None and rows.shape[0]:
        seed = RANDOM_SEED866 + 7919 * ctx['addresses'] + int(sha256_bytes864(
            (ctx['spec']['item'] + ctx['arm']).encode())[:8], 16) % 1000003
        rows = random_matched865(rows, seed)
        origin = 'NORM_MATCHED_RANDOM_ROWS'
    ctx['addresses'] += 1
    if rows is None or not rows.shape[0]:
        return None, None, origin
    query, provenance = pointer_query865(env, rows.detach().float().cpu())
    route = route_blind865(env, query, candidates, exclude)
    del query
    provenance['origin'] = origin
    return route, provenance, origin


def execute866(env, ctx, action, candidate, control, state):
    # Executes the literal model word. No Python condition on candidate content, hop class or card identity.
    spec = ctx['spec']
    k = len(ctx['path'])
    node_text = 'ROOT' if k == 0 else ctx['path'][-1]['text']
    row = {'type': 'EFFECT', 'action': action, 'k': k, 'node_text': node_text, 'decision_source': 'MODEL',
           'mounted_before': list(ctx['M'])}
    effect = None
    if action == 'ADVANCE':
        ctx['path'].append({'rows': candidate['rows'].detach().float().cpu(), 'text': candidate['text'].strip()})
        effect = 'POINTER_ADVANCED'
    if action == 'BACKTRACK':
        if ctx['path']:
            removed = ctx['path'].pop()
            row['removed_node'] = removed['text']
            effect = 'POINTER_RETRACTED'
        else:
            effect = 'NO_EFFECT_AT_ROOT'
    if action in ('ACQUIRE', 'REJECT'):
        direction = direction866(env, ctx['memx'], spec['qid'], action, state, control)
        row['direction'] = full_h865(env, direction)
        row['direction_text'] = direction['text'].strip()
        if action == 'ACQUIRE':
            candidates, exclude = list(spec['pool']), set(ctx['M'])
        else:
            candidates, exclude = [c for c in ctx['M'] if c != env['NULL829']], set()
        if action == 'ACQUIRE' and ctx['arm'] == 'NO_ACQUISITION':
            effect = 'NO_EFFECT_ACQUISITION_DISABLED_BY_ARM'
        elif not candidates:
            effect = 'NO_EFFECT_EMPTY_MEMORY' if action == 'REJECT' else 'NO_EFFECT_BANK_EXHAUSTED'
        else:
            route, provenance, origin = address866(env, ctx, direction['rows'], candidates, exclude)
            row.update({'route': None if route is None else {x: y for x, y in route.items() if x != 'scores'},
                        'scores': None if route is None else route.get('scores'), 'provenance': provenance,
                        'address_origin': origin})
            if route is None:
                effect = 'NO_EFFECT_EMPTY_DIRECTION'
            elif route['chosen'] is None:
                effect = 'NO_EFFECT_BANK_EXHAUSTED'
            else:
                chosen = route['chosen']
                old = ctx['memx']
                if action == 'ACQUIRE':
                    # prefix seal applies only when the old card list is a physical prefix (NULL memory is not)
                    ctx['memx'], mount = mount865(env, ctx['M'] + [chosen], '866_A_%s_%s_%d' % (
                        ctx['arm'], spec['item'], ctx['steps']), prior=old if ctx['M'] else None)
                    ctx['M'].append(chosen)
                    ctx['acquisitions'] += 1
                    effect = 'MOUNTED'
                else:
                    remaining = [c for c in ctx['M'] if c != chosen]
                    ctx['memx'], mount = mount865(env, remaining, '866_R_%s_%s_%d' % (
                        ctx['arm'], spec['item'], ctx['steps']))
                    ctx['M'] = remaining
                    ctx['rejections'] += 1
                    effect = 'UNMOUNTED'
                free865(env, old)
                ctx['mount_records'].append(mount)
                row.update({'chosen': chosen, 'mount': mount})
    row.update({'effect': effect, 'mounted_after': list(ctx['M']), 'path_after': [p['text'] for p in ctx['path']]})
    ctx['events'].append(row)
    event866('MODEL_EFFECT', 'MODEL_WORD_PLUS_PYTHON_IO', item=spec['item'], arm=ctx['arm'], action=action, effect=effect,
             chosen=row.get('chosen'), direction=row.get('direction_text'), mounted=list(ctx['M']))
    table866('GATE5 EFFECT866', job=spec['item'], cycle=ctx['steps'], execution='EXECUTE_MODEL_WORD_' + ctx['arm'],
             cartridge=str(row.get('chosen')), decision=action,
             payload={'effect': effect, 'direction': row.get('direction_text'), 'mounted': list(ctx['M']),
                      'path': [p['text'] for p in ctx['path']], 'margin': (row.get('route') or {}).get('margin')})
    return effect


def loop866(env, spec, arm):
    assert arm in MODEL_ARMS866
    ctx = {'spec': spec, 'arm': arm, 'M': list(spec['initial']), 'memx': None, 'path': [], 'previous_control': None,
           'events': [], 'mount_records': [], 'acquisitions': 0, 'rejections': 0, 'addresses': 0, 'steps': 0, 'hops': 0}
    end, accepted, error, trace = None, None, None, None
    t0 = time.perf_counter()
    initial_seal = None
    try:
        ctx['memx'], mount = mount865(env, ctx['M'], '866_L0_%s_%s' % (arm, spec['item']))
        ctx['mount_records'].append(mount)
        initial_seal = prefix_seals865(env, ctx['memx'])
        table866('GATE5 BEGIN866', job=spec['item'], execution='MODEL_CONTROL_LOOP_' + arm, cartridge=str(ctx['M']),
                 payload={'arm': arm, 'condition': spec['condition'], 'pool_size': len(spec['pool'])})
        while end is None:
            if ctx['steps'] >= HORIZON866:
                end = 'OBSERVATION_HORIZON'
                break
            if not budget_left865(env, STEP_CALLS866):
                end = 'RESOURCE_BUDGET'
                break
            k = len(ctx['path'])
            pointer = None if k == 0 else ctx['path'][-1]['rows']
            h, kind = hop865(env, ctx['memx'], spec['qid'], k, pointer)
            ctx['hops'] += 1
            ctx['events'].append({'type': 'HOP', 'k': k, 'kind_logged_only': kind, 'h': full_h865(env, h),
                                  'mounted': list(ctx['M']), 'decision_source': 'MODEL'})
            table866('GATE5 HOP866', job=spec['item'], cycle=ctx['steps'], execution='NATIVE_HOP_' + arm,
                     decision=kind, payload={'k': k, 'raw': h['text'], 'mounted': list(ctx['M'])})
            if kind == 'EMPTY_OUTPUT':
                end = 'NATIVE_EMPTY_OUTPUT'
                break
            control, record, state = control_step866(env, ctx['memx'], spec['qid'], arm, h, pointer,
                                                     ctx['previous_control'])
            if control is None:
                ctx['events'].append({'type': 'CONTROL_NOT_POSSIBLE', 'k': k, 'record': record,
                                      'decision_source': 'MECHANICAL_NO_NATIVE_ROWS'})
                end = 'NATIVE_EMPTY_STATE'
                break
            ctx['steps'] += 1
            action = record['action']
            ctx['events'].append({'type': 'CONTROL', 'k': k, 'step': ctx['steps'], 'action': action,
                                  'raw': record['raw'], 'record': record, 'decision_source': 'MODEL',
                                  'mounted': list(ctx['M'])})
            event866('MODEL_CONTROL', 'MODEL', item=spec['item'], arm=arm, k=k, step=ctx['steps'], action=action,
                     raw=record['raw'], candidate=h['text'], evidence=record['evidence']['text'],
                     evaluation=record['evaluation_text'], mounted=list(ctx['M']))
            table866('GATE5 CONTROL866', job=spec['item'], cycle=ctx['steps'], execution='MODEL_WORD_' + arm,
                     decision=action, payload={'k': k, 'candidate': h['text'], 'evidence': record['evidence']['text'],
                                               'evaluation': record['evaluation_text'], 'raw': record['raw'],
                                               'p1': record['control'].get('p1'), 'H1': record['H1']})
            if action == 'INVALID':
                end = 'MODEL_INVALID_ACTION'
                break
            if action == 'ACCEPT':
                end, accepted = 'MODEL_ACCEPT', h['text'].strip()
                break
            if action == 'STOP':
                end = 'MODEL_STOP'
                break
            ctx['previous_control'] = control
            execute866(env, ctx, action, h, control, state)
    except Exception as exc:
        error, trace = type(exc).__name__ + ': ' + str(exc), traceback.format_exc()
        context_limit = isinstance(exc, AssertionError) and bool(exc.args) and isinstance(exc.args[0], tuple) and \
            bool(exc.args[0]) and exc.args[0][0] == 'CONTEXT_LIMIT'
        end = 'PHYSICAL_CONTEXT_LIMIT' if context_limit else 'EXECUTION_ERROR'
    actions = [e['action'] for e in ctx['events'] if e['type'] == 'CONTROL']
    effects = [e['effect'] for e in ctx['events'] if e['type'] == 'EFFECT']
    result = {'item': spec['item'], 'arm': arm, 'experiment_arm': arm, 'condition': spec['condition'],
              'block': spec['block'], 'held_out': spec['held_out'], 'end': end, 'end_class': END_CLASSES866[end],
              'accepted_candidate': accepted, 'path': [p['text'] for p in ctx['path']], 'final_mounted': list(ctx['M']),
              'hops': ctx['hops'], 'steps': ctx['steps'], 'acquisitions': ctx['acquisitions'],
              'rejections': ctx['rejections'], 'actions': actions, 'effects': effects, 'events': ctx['events'],
              'model_stop': end == 'MODEL_STOP', 'model_accept': end == 'MODEL_ACCEPT',
              'mechanical_end': END_CLASSES866[end] != 'MODEL',
              'transitions_from_literal_model_word': all(e.get('decision_source') == 'MODEL' for e in ctx['events']
                                                         if e['type'] in ('CONTROL', 'EFFECT')),
              'mount_integrity': bool(ctx['mount_records']) and all(
                  m['n_exact'] and m['all_80_layers'] and m['finite'] and m['prior_prefix_exact'] is not False and
                  m['exact_restore_vs_first_mount'] is not False for m in ctx['mount_records']),
              'error': error, 'traceback': trace, 'exact_restore': None, 'seconds': None}
    try:
        free865(env, ctx['memx'])
        ctx['memx'] = None
        if initial_seal is not None:
            restore_memx, restore = mount865(env, spec['initial'], '866_LR_%s_%s' % (arm, spec['item']))
            result['exact_restore'] = prefix_seals865(env, restore_memx) == initial_seal
            free865(env, restore_memx)
    except Exception as exc:
        result['restore_error'] = type(exc).__name__ + ': ' + str(exc)
        result['exact_restore'] = False
    result['seconds'] = round(time.perf_counter() - t0, 3)
    event866('LOOP_END', 'PYTHON_IO', item=spec['item'], arm=arm, end=end, accepted=accepted, actions=actions,
             effects=effects, mounted=list(ctx['M']))
    table866('GATE5 END866', job=spec['item'], execution='MODEL_CONTROL_LOOP_' + arm, decision=end,
             integrity='FAIL' if end == 'EXECUTION_ERROR' else 'PASS',
             payload={'accepted': accepted, 'actions': actions, 'effects': effects, 'path': result['path'],
                      'mounted': list(ctx['M']), 'exact_restore': result['exact_restore'], 'error': error})
    return result


def not_run866(spec, arm):
    return {'item': spec['item'], 'arm': arm, 'experiment_arm': arm, 'condition': spec['condition'],
            'block': spec['block'], 'held_out': spec['held_out'], 'end': 'NOT_RUN_BUDGET',
            'end_class': 'MECHANICAL_RESOURCE', 'accepted_candidate': None, 'path': [], 'final_mounted': [],
            'hops': 0, 'steps': 0, 'acquisitions': 0, 'rejections': 0, 'actions': [], 'effects': [], 'events': [],
            'model_stop': False, 'model_accept': False, 'mechanical_end': True,
            'transitions_from_literal_model_word': None, 'mount_integrity': None, 'exact_restore': None}


def run_panel866(env, specs):
    for spec in specs:
        for arm in spec['arms']:
            if not budget_left865(env, 6 * STEP_CALLS866):
                STATE866['loops'].append(not_run866(spec, arm))
                event866('LOOP_NOT_RUN', 'MECHANICAL_RESOURCE', item=spec['item'], arm=arm)
                continue
            if arm == REFERENCE_ARM866:
                row = loop865(env, spec, 'NATIVE_P')      # locked Python-rule reference, unchanged
                row = dict(row, experiment_arm=REFERENCE_ARM866, block=spec['block'],
                           end_class='MODEL' if row['end'] in ('MODEL_ACCEPT', 'MODEL_STOP') else 'PY865_MECHANICAL',
                           actions=[e.get('action') for e in row.get('events', []) if e.get('type') == 'REVIEW'],
                           steps=len(row.get('reviews', [])))
                STATE866['loops'].append(row)
            else:
                STATE866['loops'].append(loop866(env, spec, arm))


def trap_probe866(env, spec, control_name, arm):
    # Forced diagnostic memory [first, trap]: only the following evaluation/action word is model sourced.
    result = {'item': spec['item'], 'control': control_name, 'arm': arm, 'status': 'NOT_RUN',
              'execution': 'FORCED_DIAGNOSTIC_EVIDENCE_NOT_MODEL_SELECTED'}
    memx = None
    try:
        chosen = spec['traps'][control_name]
        memx, mount = mount865(env, spec['initial'] + [chosen], '866_T_%s_%s_%s' % (control_name, arm, spec['item']))
        h0, kind0 = hop865(env, memx, spec['qid'], 0, None)
        result.update({'chosen': chosen, 'mount': mount, 'hop0': full_h865(env, h0), 'hop0_kind': kind0})
        if kind0 == 'EMPTY_OUTPUT':
            result['status'] = 'NATIVE_EMPTY_OUTPUT'
        else:
            pointer = h0['rows'].detach().float().cpu()
            h1, kind1 = hop865(env, memx, spec['qid'], 1, pointer)
            result.update({'hop1': full_h865(env, h1), 'hop1_kind': kind1})
            if kind1 == 'EMPTY_OUTPUT':
                result['status'] = 'NATIVE_EMPTY_OUTPUT'
            else:
                control, record, state = control_step866(env, memx, spec['qid'], arm, h1, pointer, None)
                result.update({'controller': record, 'action': record.get('action'),
                               'status': 'EXECUTED' if control is not None else 'NATIVE_EMPTY_STATE'})
    except Exception as exc:
        result.update({'status': 'EXECUTION_ERROR', 'error': type(exc).__name__ + ': ' + str(exc),
                       'traceback': traceback.format_exc()})
    finally:
        free865(env, memx)
    STATE866['traps'].append(result)
    event866('TRAP_PROBE', 'MODEL_WORD_AFTER_FORCED_SETUP', item=spec['item'], arm=arm, control=control_name,
             action=result.get('action'), status=result['status'])
    table866('GATE6 TRAP866', job=spec['item'], execution=result['execution'], cartridge=str(result.get('chosen')),
             decision=str(result.get('action')), integrity='FAIL' if result['status'] == 'EXECUTION_ERROR' else 'PASS',
             payload={'control': control_name, 'arm': arm, 'hop0': (result.get('hop0') or {}).get('text'),
                      'hop1': (result.get('hop1') or {}).get('text'),
                      'evaluation': (result.get('controller') or {}).get('evaluation_text'),
                      'raw_action': (result.get('controller') or {}).get('raw'), 'status': result['status']})
    return result


def run_traps866(env, specs):
    for spec in specs:
        if spec['block'] != 'CAUSAL' or spec['condition'] != 'LIVE':
            continue
        for control_name in TRAP_CONTROLS866:
            for arm in TRAP_ARMS866:
                if budget_left865(env, STEP_CALLS866):
                    trap_probe866(env, spec, control_name, arm)
                else:
                    STATE866['traps'].append({'item': spec['item'], 'control': control_name, 'arm': arm,
                                              'status': 'NOT_RUN_BUDGET', 'execution': 'MECHANICAL_RESOURCE'})


# ============================ C: OFFLINE LABELS, STATISTICS, ARTIFACTS (after all execution) ============================
def card_class866(env, cid, node_name, wi):
    if cid is None:
        return 'NONE'
    if cid not in env['CONTENT841']:
        return 'NON_BANK'
    cwi, kind, ver = env['CONTENT841'][cid]
    source_key, target_key = env['REL841'][kind]
    source = env['worlds829'][cwi][source_key]
    target = env['worlds829'][cwi][target_key]
    if cwi != wi:
        return 'OTHER_WORLD'
    if source == node_name:
        return 'SOURCE_MATCH_' + kind.upper()
    if target == node_name:
        return 'REVERSED_EDGE_' + kind.upper()
    if env['worlds829'][wi]['start'] in (source, target):
        return 'SHARED_START_NODE_' + kind.upper()
    return 'SAME_WORLD_OTHER_' + kind.upper()


def valid_for866(env, node_name, pool, wi):
    valid = set()
    for cid in pool:
        if cid in env['CONTENT841']:
            cwi, kind, ver = env['CONTENT841'][cid]
            source, target = env['REL841'][kind]
            if cwi == wi and env['worlds829'][wi][source] == node_name:
                valid.add(cid)
    return valid


def correct866(env, row, spec):
    # 865 loop_correct law: supported851 for two-link questions; end3 with first, second, third for HOP3.
    if row.get('end') != 'MODEL_ACCEPT' or not row.get('accepted_candidate'):
        return False
    w = env['worlds829'][spec['world_index']]
    answer = row['accepted_candidate']
    if spec['condition'] == 'HOP3':
        ids = w['ids']
        return (env['node851'](answer, w) == 'end3' and
                {ids['first'], ids['second'], ids['third']} <= set(row.get('final_mounted', [])))
    return bool(env['supported851'](answer, w, set(row.get('final_mounted', []))))


def offline_evaluate866(env):
    specs = {s['item']: s for s in STATE866['specs']['rows']}
    rows = STATE866['loops']
    acquisitions, rejections = [], []
    for row in rows:
        spec = specs[row['item']]
        wi = spec['world_index']
        w = env['worlds829'][wi]
        correct = correct866(env, row, spec)
        needed = {w['ids']['first'], w['ids']['second']} | ({w['ids']['third']} if spec['condition'] == 'HOP3' else set())
        row['offline'] = {'correct_accept': correct, 'false_accept': row.get('end') == 'MODEL_ACCEPT' and not correct,
                          'accepted_class': env['node851'](row.get('accepted_candidate') or '', w),
                          'correct_stop_missing': spec['condition'] == 'MISSING' and row.get('end') == 'MODEL_STOP',
                          'accept_without_acquisition': row.get('end') == 'MODEL_ACCEPT' and row.get('acquisitions', 0) == 0}
        if row['experiment_arm'] not in MODEL_ARMS866:
            continue
        for e in row.get('events', []):
            if e.get('type') != 'EFFECT' or e.get('action') not in ('ACQUIRE', 'REJECT'):
                continue
            text = e.get('node_text', 'ROOT')
            node_class = 'start' if text == 'ROOT' else env['node851'](text, w)
            node_name = w.get(node_class, text.strip())
            direction_class = env['node851'](e.get('direction_text') or '', w)
            chosen = e.get('chosen')
            if e['action'] == 'ACQUIRE':
                valid = valid_for866(env, node_name, spec['pool'], wi)
                e['offline'] = {'node_class': node_class, 'direction_class': direction_class,
                                'direction_names_current_node': direction_class == node_class,
                                'valid_set_size': len(valid), 'valid_acquisition': chosen in valid,
                                'card_class': card_class866(env, chosen, node_name, wi)}
                acquisitions.append({'item': row['item'], 'condition': row['condition'], 'block': row['block'],
                                     'arm': row['experiment_arm'], 'k': e.get('k'), 'node_text': text,
                                     'node_class': node_class, 'direction_text': e.get('direction_text'),
                                     'direction_class': direction_class, 'effect': e.get('effect'), 'chosen': chosen,
                                     'valid': chosen in valid, 'class': e['offline']['card_class'],
                                     'valid_set_size': len(valid), 'origin': e.get('address_origin'),
                                     'margin': (e.get('route') or {}).get('margin')})
            else:
                e['offline'] = {'removed_needed_card': chosen in needed, 'direction_class': direction_class,
                                'card_class': card_class866(env, chosen, node_name, wi)}
                rejections.append({'item': row['item'], 'condition': row['condition'], 'block': row['block'],
                                   'arm': row['experiment_arm'], 'effect': e.get('effect'), 'chosen': chosen,
                                   'removed_needed_card': chosen in needed, 'class': e['offline']['card_class'],
                                   'direction_text': e.get('direction_text')})
    for trap in STATE866['traps']:
        spec = specs[trap['item']]
        w = env['worlds829'][spec['world_index']]
        action = trap.get('action')
        trap['offline'] = {'action': action, 'reject_or_backtrack': action in ('REJECT', 'BACKTRACK'),
                           'accept': action == 'ACCEPT', 'advance': action == 'ADVANCE',
                           'hop1_class': env['node851']((trap.get('hop1') or {}).get('text', ''), w),
                           'card_class': card_class866(env, trap.get('chosen'), w['middle'], spec['world_index'])}

    def planned(arm, block='CAUSAL', conditions=PRIMARY_CONDITIONS866):
        return sorted(s['item'] for s in specs.values() if s['block'] == block and s['condition'] in conditions
                      and arm in s['arms'])

    def by(arm):
        return {r['item']: r for r in rows if r['experiment_arm'] == arm}

    def vec(arm, items, key):
        got = by(arm)
        return [bool((got.get(i) or {}).get('offline', {}).get(key, False)) for i in items]

    def paired(a, b, key, conditions=PRIMARY_CONDITIONS866):
        items = sorted(set(planned(a, conditions=conditions)) & set(planned(b, conditions=conditions)))
        va, vb = vec(a, items, key), vec(b, items, key)
        return items, va, vb, rate865(va), rate865(vb), sign_test865(va, vb)

    H = {}
    items1, mc1, na1, r_mc, r_na, s1 = paired('MODEL_CONTROL', 'NO_ACQUISITION', 'correct_accept')
    gap1 = (r_mc['rate'] or 0.0) - (r_na['rate'] or 0.0)
    H['H1'] = {'items': len(items1), 'MODEL_CONTROL': r_mc, 'NO_ACQUISITION': r_na, 'gap': gap1, 'sign': s1,
               'status': 'PASS' if len(items1) == 27 and (r_mc['rate'] or 0.0) >= 0.50 and gap1 >= 0.30 and
               s1['p_two_sided'] <= ALPHA866 else 'FAIL'}
    items2, mc2, ra2, r_mc2, r_ra2, s2 = paired('MODEL_CONTROL', 'RANDOM_ADDRESS', 'correct_accept')
    loopvalid = {}
    for arm in ('MODEL_CONTROL', 'RANDOM_ADDRESS'):
        loopvalid[arm] = [any(a['valid'] for a in acquisitions if a['item'] == i and a['arm'] == arm and
                              a['effect'] == 'MOUNTED') for i in items2]
    lv_m, lv_r = rate865(loopvalid['MODEL_CONTROL']), rate865(loopvalid['RANDOM_ADDRESS'])
    s2v = sign_test865(loopvalid['MODEL_CONTROL'], loopvalid['RANDOM_ADDRESS'])
    gap2, gap2v = (r_mc2['rate'] or 0.0) - (r_ra2['rate'] or 0.0), (lv_m['rate'] or 0.0) - (lv_r['rate'] or 0.0)
    ev = {arm: rate865([a['valid'] for a in acquisitions if a['arm'] == arm and a['block'] == 'CAUSAL' and
                        a['effect'] == 'MOUNTED']) for arm in ('MODEL_CONTROL', 'RANDOM_ADDRESS', 'SHUFFLED_STATE')}
    named = rate865([a['direction_class'] == a['node_class'] for a in acquisitions
                     if a['arm'] == 'MODEL_CONTROL' and a['block'] == 'CAUSAL'])
    H['H2'] = {'items': len(items2), 'correct_accept_MODEL_CONTROL': r_mc2, 'correct_accept_RANDOM_ADDRESS': r_ra2,
               'correct_accept_gap': gap2, 'sign_correct_accept': s2, 'loop_valid_acquisition_MODEL_CONTROL': lv_m,
               'loop_valid_acquisition_RANDOM_ADDRESS': lv_r, 'loop_valid_gap': gap2v, 'sign_loop_valid': s2v,
               'event_valid_acquisition': ev, 'MODEL_CONTROL_direction_names_current_node': named,
               'status': 'PASS' if len(items2) == 27 and gap2 >= 0.30 and gap2v >= 0.20 and
               max(s2['p_two_sided'], s2v['p_two_sided']) <= ALPHA866 else 'FAIL'}
    items3, mc3, sh3, r_mc3, r_sh3, s3 = paired('MODEL_CONTROL', 'SHUFFLED_STATE', 'correct_accept')
    gap3 = (r_mc3['rate'] or 0.0) - (r_sh3['rate'] or 0.0)
    H['H3'] = {'items': len(items3), 'MODEL_CONTROL': r_mc3, 'SHUFFLED_STATE': r_sh3, 'gap': gap3, 'sign': s3,
               'status': 'PASS' if len(items3) == 27 and gap3 >= 0.20 and s3['p_two_sided'] <= ALPHA866 else 'FAIL'}
    model_rows = [r for r in rows if r['experiment_arm'] in MODEL_ARMS866]
    executed_model = [r for r in model_rows if r['end'] != 'NOT_RUN_BUDGET']
    literal = [r.get('transitions_from_literal_model_word') is True for r in executed_model]
    H['H4'] = {'static_purity': STATE866['source'].get('purity', {}).get('status'),
               'loops_all_transitions_literal_model_word': rate865(literal),
               'model_control_transitions': sum(len(r.get('actions', [])) for r in executed_model),
               'model_arm_loops_not_run_budget': len(model_rows) - len(executed_model),
               'status': 'PASS' if STATE866['source'].get('purity', {}).get('status') == 'PASS' and literal and
               all(literal) and len(model_rows) == len(executed_model) else 'FAIL'}
    missing = vec('MODEL_CONTROL', planned('MODEL_CONTROL', conditions=('MISSING',)), 'false_accept')
    trap_m = [t for t in STATE866['traps'] if t['arm'] == 'MODEL_CONTROL']
    trap_s = [t for t in STATE866['traps'] if t['arm'] == 'SHUFFLED_STATE']
    tm_acc = rate865([t.get('offline', {}).get('accept', False) for t in trap_m])
    H['H5'] = {'MISSING_false_accept': rate865(missing), 'trap_ACCEPT_MODEL_CONTROL': tm_acc,
               'trap_ADVANCE_MODEL_CONTROL': rate865([t.get('offline', {}).get('advance', False) for t in trap_m]),
               'status': 'PASS' if len(missing) == 9 and len(trap_m) == 27 and
               all(t['status'] == 'EXECUTED' for t in trap_m) and (rate865(missing)['rate'] or 0.0) <= 0.10 and
               (tm_acc['rate'] or 0.0) <= 0.25 else 'FAIL'}
    tm_rb = rate865([t.get('offline', {}).get('reject_or_backtrack', False) for t in trap_m])
    ts_rb = rate865([t.get('offline', {}).get('reject_or_backtrack', False) for t in trap_s])
    gap6 = (tm_rb['rate'] or 0.0) - (ts_rb['rate'] or 0.0)
    by_kind = {}
    for t in trap_m + trap_s:
        key = t['arm'] + '/' + t['control'] + '/' + str(t.get('offline', {}).get('hop1_class'))
        by_kind.setdefault(key, {})
        a = str(t.get('action'))
        by_kind[key][a] = by_kind[key].get(a, 0) + 1
    H['H6'] = {'MODEL_CONTROL_reject_or_backtrack': tm_rb, 'SHUFFLED_STATE_reject_or_backtrack': ts_rb, 'gap': gap6,
               'actions_by_arm_trap_hop1class': by_kind,
               'status': 'PASS' if len(trap_m) == len(trap_s) == 27 and
               all(t['status'] == 'EXECUTED' for t in trap_m + trap_s) and (tm_rb['rate'] or 0.0) >= 0.40 and
               gap6 >= 0.20 else 'FAIL'}

    def describe(arm, block, conditions):
        group = [r for r in rows if r['experiment_arm'] == arm and r['block'] == block and r['condition'] in conditions]
        actions = {}
        for r in group:
            for a in r.get('actions', []):
                actions[str(a)] = actions.get(str(a), 0) + 1
        return {'n': len(group), 'correct_accept': rate865([r['offline']['correct_accept'] for r in group]),
                'false_accept': rate865([r['offline']['false_accept'] for r in group]),
                'literal_STOP': rate865([r['end'] == 'MODEL_STOP' for r in group]),
                'accept_without_acquisition': rate865([r['offline']['accept_without_acquisition'] for r in group]),
                'ends': {e: sum(r['end'] == e for r in group) for e in sorted({r['end'] for r in group})},
                'action_counts': actions,
                'mean_steps': (sum(r.get('steps', 0) for r in group) / len(group)) if group else None}
    H['H7'] = {'FORK': {arm: describe(arm, 'CAUSAL', ('FORK',)) for arm in
                        ('MODEL_CONTROL', 'NO_ACQUISITION', 'RANDOM_ADDRESS', 'SHUFFLED_STATE', REFERENCE_ARM866)},
               'model_backtracks_FORK': sum(r.get('effects', []).count('POINTER_RETRACTED') for r in rows
                                            if r['experiment_arm'] == 'MODEL_CONTROL' and r['condition'] == 'FORK'),
               'model_rejections_FORK': [x for x in rejections if x['arm'] == 'MODEL_CONTROL' and x['condition'] == 'FORK'],
               'status': 'REPORT_ONLY'}
    H['H8'] = {'MISSING': {arm: describe(arm, 'CAUSAL', ('MISSING',)) for arm in
                           ('MODEL_CONTROL', 'SHUFFLED_STATE', REFERENCE_ARM866)},
               'SUFFICIENT': {arm: describe(arm, 'CAUSAL', ('SUFFICIENT',)) for arm in ('MODEL_CONTROL', REFERENCE_ARM866)},
               'status': 'REPORT_ONLY'}
    H['H9'] = {'status': 'REPORT_ONLY', 'conditions': {}}
    for condition in CONDITIONS866:
        items, a, b, ra, rb, s = paired('MODEL_CONTROL', REFERENCE_ARM866, 'correct_accept', (condition,))
        H['H9']['conditions'][condition] = {'items': len(items), 'MODEL_CONTROL': ra, REFERENCE_ARM866: rb, 'sign': s}
    H['H10'] = {'status': 'REPORT_ONLY', 'disclosure': PREREG866['H10_evaluation_worlds'],
                'arms': {arm: describe(arm, 'EVALUATION', CONDITIONS866) for arm in
                         ('MODEL_CONTROL', 'RANDOM_ADDRESS', REFERENCE_ARM866)}}
    mounts = [e for e in EVENTS866 if e.get('kind') == 'MOUNT']
    mount_ok = bool(mounts) and all(e.get('n_exact') and e.get('all_80_layers') and e.get('finite') and
        e.get('prior_prefix_exact') is not False and e.get('exact_restore_vs_first_mount') is not False for e in mounts)
    executed = [r for r in rows if r['end'] not in ('NOT_RUN_BUDGET',)]
    restores = [r.get('exact_restore') is True for r in executed]
    physical = {'mounts': len(mounts), 'all_mount_checks_exact': mount_ok, 'exact_restores': rate865(restores),
                'status': 'PASS' if mount_ok and restores and all(restores) else 'FAIL'}
    claim = all(H[h]['status'] == 'PASS' for h in ('H1', 'H2', 'H3', 'H4')) and physical['status'] == 'PASS'
    H['CLAIM'] = {'MODEL_CONTROLLED_CLOSURE': 'CLAIMABLE' if claim else 'NOT_CLAIMABLE',
                  'rule': PREREG866['claim_rule'], 'status': 'PASS' if claim else 'FAIL'}
    STATE866['hypotheses'] = H
    ends = {}
    for r in rows:
        ends.setdefault(r['experiment_arm'], {}).setdefault(r['end'], 0)
        ends[r['experiment_arm']][r['end']] += 1
    STATE866['offline'] = {'loop_count': len(rows), 'planned_loops': STATE866['specs']['planned_loops'],
        'ends_by_arm': ends, 'acquisitions': acquisitions, 'rejections': rejections, 'physical': physical,
        'not_run_budget': sum(r['end'] == 'NOT_RUN_BUDGET' for r in rows),
        'execution_errors': sum(r['end'] == 'EXECUTION_ERROR' for r in rows)}
    STATE866['gates'].update({'GATE3_PANEL': {'status': 'EXECUTED', 'planned': STATE866['offline']['planned_loops'],
            'observed': len(rows), 'not_run_budget': STATE866['offline']['not_run_budget']},
        'GATE4_PHYSICAL': {'status': physical['status']}, 'GATE5_PROVENANCE': {'status': H['H4']['status']},
        'GATE6_TRAPS': {'status': H['H6']['status'], 'false_acceptance': H['H5']['status']},
        'GATE7_EVALUATION': {'status': 'REPORT_ONLY'}})
    write_csv866(rows, acquisitions, rejections)
    return H


def write_csv866(rows, acquisitions, rejections):
    with (ROOT864 / '866_loops.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['item', 'block', 'condition', 'arm', 'end', 'end_class', 'accepted', 'correct_accept',
                         'false_accept', 'acquisitions', 'rejections', 'steps', 'hops', 'actions', 'effects',
                         'final_mounted', 'mount_integrity', 'exact_restore', 'seconds'])
        for r in rows:
            writer.writerow([r['item'], r.get('block'), r['condition'], r['experiment_arm'], r['end'], r.get('end_class'),
                             r.get('accepted_candidate'), r['offline']['correct_accept'], r['offline']['false_accept'],
                             r.get('acquisitions', 0), r.get('rejections', 0), r.get('steps', 0), r.get('hops', 0),
                             '>'.join(str(a) for a in r.get('actions', [])),
                             '>'.join(str(a) for a in r.get('effects', [])), '|'.join(r.get('final_mounted', [])),
                             r.get('mount_integrity'), r.get('exact_restore'), r.get('seconds')])
    with (ROOT864 / '866_controls.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['item', 'condition', 'arm', 'step', 'k', 'candidate', 'evidence', 'evaluation', 'action_raw',
                         'action', 'mounted', 'control_rows_sha256'])
        for r in rows:
            if r['experiment_arm'] not in MODEL_ARMS866:
                continue
            for e in r.get('events', []):
                if e.get('type') == 'CONTROL':
                    rec = e.get('record') or {}
                    writer.writerow([r['item'], r['condition'], r['experiment_arm'], e.get('step'), e.get('k'),
                                     (rec.get('candidate') or {}).get('text'), (rec.get('evidence') or {}).get('text'),
                                     rec.get('evaluation_text'), e.get('raw'), e.get('action'),
                                     '|'.join(e.get('mounted', [])),
                                     ((rec.get('control') or {}).get('output') or {}).get('sha256')])
    with (ROOT864 / '866_acquisitions.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        keys = ['item', 'block', 'condition', 'arm', 'k', 'node_text', 'node_class', 'direction_text', 'direction_class',
                'effect', 'chosen', 'valid', 'class', 'valid_set_size', 'origin', 'margin']
        writer.writerow(keys)
        for a in acquisitions:
            writer.writerow([a.get(k) for k in keys])
    with (ROOT864 / '866_rejections.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        keys = ['item', 'block', 'condition', 'arm', 'effect', 'chosen', 'removed_needed_card', 'class', 'direction_text']
        writer.writerow(keys)
        for a in rejections:
            writer.writerow([a.get(k) for k in keys])
    with (ROOT864 / '866_traps.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['item', 'control', 'arm', 'status', 'chosen', 'hop0', 'hop1', 'hop1_class', 'evaluation',
                         'action', 'reject_or_backtrack', 'accept', 'card_class'])
        for t in STATE866['traps']:
            off = t.get('offline', {})
            writer.writerow([t['item'], t['control'], t['arm'], t['status'], t.get('chosen'),
                             (t.get('hop0') or {}).get('text'), (t.get('hop1') or {}).get('text'), off.get('hop1_class'),
                             (t.get('controller') or {}).get('evaluation_text'), t.get('action'),
                             off.get('reject_or_backtrack'), off.get('accept'), off.get('card_class')])


def partial_report866():
    return {'test': 866, 'kind': TEST866_KIND, 'status': 'INCOMPLETE', 'root866': str(ROOT864),
        'gpu_execution_claimed_by_author': False, 'preregistered': PREREG866, 'preregistered_sha256': PREREG_SHA866,
        'source': STATE866['source'], 'locked865_runtime': {'budget': STATE865['budget'], 'gates': STATE865['gates'],
                                                             'root_xray': STATE865['root']},
        'gates': STATE866['gates'], 'hypotheses': STATE866['hypotheses'],
        'original_native': STATE866['original_native'], 'specifications': STATE866['specs'],
        'loops': [{k: v for k, v in r.items() if k not in ('events', 'reviews')} for r in STATE866['loops']],
        'loops_note': 'compact rows; every event, review, token top-20 and trace is in 866_full_records.json.gz',
        'traps': [{k: v for k, v in t.items() if k not in ('controller', 'hop0', 'hop1', 'mount')} | {
            'hop0_text': (t.get('hop0') or {}).get('text'), 'hop1_text': (t.get('hop1') or {}).get('text'),
            'evaluation_text': (t.get('controller') or {}).get('evaluation_text'),
            'raw_action': (t.get('controller') or {}).get('raw')} for t in STATE866['traps']],
        'offline': STATE866['offline'],
        'negative': STATE866['negative'], 'timings': STATE866['timings'], 'error': ERROR866, 'traceback': TRACEBACK866,
        'interpretation_rules': [
            'A: model words and soft rows; B: Python executes the word (pointer, PEAK50, SHA I/O, CUT3); C: offline labels.',
            'In model arms Python never selects a transition; the only Python ends are listed in END_CLASSES866.',
            'Mechanical ends (horizon, budget, empty rows, invalid word, context, error) count as failure, never as STOP.',
            'PY865_REFERENCE is the locked Python-rule loop, reported only as a comparison.',
            'Forced trap cartridges diagnose validity judgement; they are not model-selected acquisitions.',
            'A physically valid mount or a correct answer alone does not establish autonomous recursive reasoning.',
            'Worlds 9-11 are report-only and are not represented as new-to-design.']}


def finalize866(success):
    report = partial_report866()
    report['peak_gpu_gib'] = torch.cuda.max_memory_allocated() / 1024**3 if torch.cuda.is_available() else None
    report['wall_seconds'] = round(time.perf_counter() - START864, 3)
    rows = STATE866['loops']
    planned = STATE866.get('specs', {}).get('planned_loops') or 0
    technical = {
        'source_locks': STATE865['source'].get('lock_count') == len(LOCKS864),
        'locked865_ast_identity': 'locked865' in STATE866['source'],
        'firewall': STATE866['source'].get('firewall', {}).get('status') == 'PASS',
        'control_purity': STATE866['source'].get('purity', {}).get('status') == 'PASS',
        'regression': STATE865['gates'].get('GATE1_REGRESSION', {}).get('status') == 'PASS',
        'executed_source_saved': (ROOT864 / '866.py').is_file(),
        'experiment_completed': bool(success),
        'panel_complete': planned > 0 and len(rows) == planned and all(r.get('end') != 'NOT_RUN_BUDGET' for r in rows),
        'no_loop_execution_error': all(r.get('end') != 'EXECUTION_ERROR' for r in rows),
        'physical_fail_closed': STATE866.get('offline', {}).get('physical', {}).get('status') == 'PASS'}
    report['technical_gates'] = technical
    report['status'] = 'TEST866_TECHNICAL_EXECUTION_COMPLETE' if all(technical.values()) else 'UNRESOLVED'
    json_write866('866_report.json', report)
    with gzip.open(ROOT864 / '866_full_records.json.gz', 'wt', encoding='utf-8') as handle:
        json.dump({'loops': STATE866['loops'], 'traps': STATE866['traps'], 'root_xray': STATE865['root']}, handle,
                  ensure_ascii=False, default=str)
    if not EVENTS_FILE866.closed:
        EVENTS_FILE866.flush()
        EVENTS_FILE866.close()
    with (ROOT864 / '866_events.jsonl').open('w', encoding='utf-8') as handle:
        for row in EVENTS866:
            handle.write(json.dumps(row, ensure_ascii=False, default=str) + '\n')
    names = ['866.py', '866.log', '866_report.json', '866_events.jsonl', '866_loops.csv', '866_controls.csv',
             '866_acquisitions.csv', '866_rejections.csv', '866_traps.csv', '866_full_records.json.gz']
    required = {name: (ROOT864 / name).is_file() and (ROOT864 / name).stat().st_size > 0 for name in names}
    report['technical_gates']['required_artifacts_present'] = all(required.values())
    report['required_artifacts'] = required
    if not all(report['technical_gates'].values()):
        report['status'] = 'UNRESOLVED'
    short866('TEST866 STATUS', report['status'])
    short866('TEST866 TECHNICAL', json.dumps(report['technical_gates'], sort_keys=True))
    short866('TEST866 HYPOTHESES', json.dumps({k: v.get('status') for k, v in STATE866['hypotheses'].items()},
                                              sort_keys=True))
    short866('TEST866 ENDS_BY_ARM', json.dumps(STATE866.get('offline', {}).get('ends_by_arm', {}), sort_keys=True))
    short866('TEST866 PEAK_GPU_GIB', report['peak_gpu_gib'], 'WALL_S', report['wall_seconds'], 'FILES', str(ROOT864))
    short866('GPU EXECUTION NOT VERIFIED BY THE CODE AUTHOR; this run is the first execution.')
    json_write866('866_report.json', report)
    LOG_FILE864.flush()
    manifest = {'test': 866, 'status': report['status'], 'required_artifacts': required, 'files': {}}
    for name in names:
        path = ROOT864 / name
        manifest['files'][name] = ({'bytes': path.stat().st_size, 'sha256': sha256_file866(path),
            'git_blob_sha1': git_blob864(path.read_bytes())} if path.is_file() else {'status': 'MISSING'})
    json_write866('866_manifest.json', manifest)
    return report, manifest


# ============================ SINGLE CELL EXECUTION ============================
SUCCESS866 = False
try:
    table866('M0 BEGIN866', payload={'test': 866, 'root': str(ROOT864), 'prereg_sha256': PREREG_SHA866})
    load_sources865()
    feasibility_audit864()
    EXECUTED_SOURCE866 = capture_cell_source866()
    audit_contracts865()
    load_spine864()
    tree866 = ast.parse(EXECUTED_SOURCE866, filename='866.py')
    nodes865 = [copy.deepcopy(n) for n in tree866.body if isinstance(n, ast.FunctionDef) and n.name.endswith('865')]
    _dependency_audit861(nodes865)
    STATE865['source']['dependency_audit'] = copy.deepcopy(STATE861['dependency_audit'])
    firewall_audit865(tree866)
    verify_locked865_866(EXECUTED_SOURCE866)
    nodes866 = [copy.deepcopy(n) for n in tree866.body if isinstance(n, ast.FunctionDef) and n.name.endswith('866')]
    _dependency_audit861(nodes866)
    STATE866['source']['dependency_audit'] = copy.deepcopy(STATE861['dependency_audit'])
    firewall_audit866(tree866)
    purity_audit866(tree866)
    STATE865['gates']['GATE0_SOURCE'] = {'status': 'PASS', 'locks': len(LOCKS864)}
    STATE866['gates']['GATE0_SOURCE'] = {'status': 'PASS', 'locks': len(LOCKS864)}
    env866, original_error866, original_trace866, reproduction866 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace866
    jobs866 = verify_two_job859(env866, original_trace866)
    TWO_JOB_VERIFICATION864 = jobs866
    assert_hook_free859(env866, 'TEST866_before_native_regression')
    install_offline_evaluator859(env866)
    native866 = native_sequences860(env866)
    NATIVE_REGRESSION864 = native_regression864(env866, native866)
    verify_864_reference865(NATIVE_REGRESSION864)
    ANALYSIS864 = run_analysis863(env866, native866)
    assert len(STATE863['restores']) == 3 and all(r['exact'] for r in STATE863['restores']), 'ORIGINAL_EXACT_RESTORE'
    STATE866['original_native'] = {'records': env866['REC841'], 'sequences': native866,
        'analysis': ANALYSIS864, 'two_job_verification': jobs866, 'restores': STATE863['restores']}
    original_digest866 = records_digest861(env866)
    null_seal866 = physical_seal863(env866, env866['MEMNULL841'])
    keys_identity866 = id(env866['KEYS841'])
    runtime_contracts865(env866)
    runtime_preflight865(env866, reproduction866)
    rearm_budget865(env866)
    make_slots866(env866)
    T0_866 = time.perf_counter()
    T0_865 = T0_866
    root_diagnostic865(env866)
    STATE866['timings']['gate1_s'] = round(time.perf_counter() - T0_866, 3)
    specs866 = build_specs866(env866)
    STATE866['gates']['GATE2_SPECS'] = {'status': 'PASS', 'n': len(specs866), 'sha256': STATE866['specs']['sha256'],
                                        'planned_loops': STATE866['specs']['planned_loops']}
    run_traps866(env866, specs866)
    STATE866['timings']['traps_s'] = round(time.perf_counter() - T0_866, 3)
    run_panel866(env866, specs866)
    STATE866['timings']['panel_s'] = round(time.perf_counter() - T0_866, 3)
    # ====== OFFLINE PHASE MARKER 866: labels become accessible only below ======
    STATE866['negative'] = {
        'ORIGINAL_RECORD_UNCHANGED': records_digest861(env866) == original_digest866,
        'MEMNULL841_UNCHANGED': physical_seal863(env866, env866['MEMNULL841']) == null_seal866,
        'KEYS841_OBJECT_UNCHANGED': id(env866['KEYS841']) == keys_identity866,
        'ORIGINAL_REVIEW_LIMIT_UNCHANGED': env866['MAX_REVIEWS851'] == 2,
        'PYTHON_RULES_IN_MODEL_ARMS': 'NONE (static purity audit)'}
    assert all(v is True for k, v in STATE866['negative'].items() if k != 'PYTHON_RULES_IN_MODEL_ARMS'), \
        ('NEGATIVE_CONTROL_FAILED', STATE866['negative'])
    offline_evaluate866(env866)
    SUCCESS866 = True
    finalize866(True)
except BaseException as exc:
    ERROR866 = type(exc).__name__ + ': ' + str(exc)
    TRACEBACK866 = traceback.format_exc()
    print(TRACEBACK866, file=ERROR_CONSOLE864, flush=True)
    short866('TEST866 FULL TRACEBACK', TRACEBACK866)
    short866('TEST866 INCOMPLETE', ERROR866)
    try:
        finalize866(False)
    except BaseException as final_exc:
        print('FINALIZE_FAILED', type(final_exc).__name__, final_exc, file=ERROR_CONSOLE864, flush=True)
        traceback.print_exc()
finally:
    if not EVENTS_FILE866.closed:
        EVENTS_FILE866.close()
    LOG_FILE864.close()

# ===================== CELL CONSOLE CAPTURE — END: package and download (I/O only; TEST866 is finished) =====================
import hashlib as _cc_hashlib, pathlib as _cc_pathlib, zipfile as _cc_zipfile
try:
    print('CELL CONSOLE CAPTURE END', _cc_time.strftime('%Y-%m-%dT%H:%M:%SZ', _cc_time.gmtime()))
    _cc_sys.stdout.flush()
    _cc_sys.stderr.flush()
finally:
    CC_STOP.set()
    _cc_sys.stdout, _cc_sys.stderr = CC_ORIGINAL
    CC_FILE.close()
CC_ROOT = _cc_pathlib.Path(str(ROOT864))
CC_ZIP = _cc_pathlib.Path('/content/TEST866_SONUC_%s.zip' % CC_STAMP)
with _cc_zipfile.ZipFile(CC_ZIP, 'w', compression=_cc_zipfile.ZIP_DEFLATED, compresslevel=9) as _cc_z:
    _cc_sums = []
    for _cc_p in sorted(CC_ROOT.rglob('*')):
        if _cc_p.is_file():
            _cc_z.write(_cc_p, arcname=CC_ROOT.name + '/' + str(_cc_p.relative_to(CC_ROOT)))
            _cc_sums.append('%s  %s' % (_cc_hashlib.sha256(_cc_p.read_bytes()).hexdigest(), _cc_p.relative_to(CC_ROOT)))
    _cc_z.write(CC_PATH, arcname=CC_ROOT.name + '/' + _cc_os.path.basename(CC_PATH))
    _cc_sums.append('%s  %s' % (_cc_hashlib.sha256(open(CC_PATH, 'rb').read()).hexdigest(), _cc_os.path.basename(CC_PATH)))
    _cc_z.writestr(CC_ROOT.name + '/SHA256SUMS.txt', '\n'.join(_cc_sums) + '\n')
assert _cc_zipfile.ZipFile(CC_ZIP).testzip() is None, 'ZIP_CORRUPT'
CC_SIZE = _cc_os.path.getsize(CC_PATH)
print('CELL OUTPUT FILE :', CC_PATH, '%.2f MB' % (CC_SIZE / 1e6), 'sha256',
      _cc_hashlib.sha256(open(CC_PATH, 'rb').read()).hexdigest())
print('RESULT ZIP       :', CC_ZIP, '%.2f MB' % (CC_ZIP.stat().st_size / 1e6), 'sha256',
      _cc_hashlib.sha256(CC_ZIP.read_bytes()).hexdigest())
if CC_DRIVE_DIR is not None:
    try:
        _cc_shutil.copy2(CC_PATH, CC_DRIVE_DIR)
        _cc_shutil.copy2(CC_ZIP, CC_DRIVE_DIR)
        print('DRIVE COPY       :', CC_DRIVE_DIR)
    except Exception as _cc_exc:
        print('DRIVE COPY FAILED:', type(_cc_exc).__name__, _cc_exc)
try:
    from google.colab import files as _cc_files
    _cc_files.download(CC_PATH)
    _cc_files.download(str(CC_ZIP))
    print('Downloads started. If the phone did not receive them, run in a new cell:')
    print("from google.colab import files; files.download(%r); files.download(%r)" % (CC_PATH, str(CC_ZIP)))
except Exception as _cc_exc:
    print('Automatic download not available (%s); the files are in /content.' % type(_cc_exc).__name__)
