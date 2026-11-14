# AKBASCORE SILICON HIPPOCAMPUS — TEST883 / F1 — PHYSICAL EXPERIENCE CARTRIDGE AS THE FEEDBACK CHANNEL (VIS vs C-BLIND)
# One A100-SXM4-80GB Colab cell. Frozen Qwen2.5-72B-Instruct NF4, BF16 activations/KV, SDPA, 80 layers, H=8192.
# No router, no calibration, no thresholds, no STORE, no bank change, no forced action: every executed word is a native CAR
# reading, passed literally to the locked execute866; success is scored only after every live episode, by the locked
# success867 / supported851 evaluator.
# ---------------------------------------------------------------------------------------------------------------------------
# SOURCE MANIFEST — ceceli33/titan-cognitive-core-v3, pinned commit 3d75f289b88271440f4e3e13c2491699e6dc14ca (codeload zip of
# that commit). Git blobs (recomputed from the clone, checked again at G0 before the model is loaded):
#   test870.py de3c8153 (engine: hop865, mount865, execute866, control_step867, feedback867, success867, build_specs869 …)
#   873.py 2e44affa | 874.py 12172001 | 877.py a6aa7648 | 878.py 7842e867 | 881.py 63466135 | 882.py bbd0c53f | 882.log 66479a74
#   869_full_records.json.gz f75a94eb (sha256 daf5a8c4…7f21) | 757.py 3d88bf86 | 841.py 135b18e5 | 851.py 0f01e73b
#   logs 873 1c9eb9fc, 874 1229e3b7, 877 c4eb5802, Test_878_log2 2bfc7adc, 879 c1205bc0, 880 adcc0389, 881 e6e38359
# 882 note: the 882 GPU log names executed cell dc714a11 (2390 lines); the committed 882.py is bbd0c53f (2392 lines). No simple
#   join/strip of the 3 pasted parts reproduces dc714a11: the difference is NOT_CHECKED and nothing here depends on it.
# This cell carries no hash of itself: its blob / SHA-256 are measured at G0 and written before the model is loaded.
# GPU_NOT_RUN_BY_AUTHOR.
import ast as _a883, hashlib as _h883, json as _j883, os as _o883, re as _r883, shutil as _s883, urllib.request as _u883
import math as _m883, gzip as _g883, collections as _c883
import numpy as _np883
_a882, _h882, _j882, _o882, _r882 = _a883, _h883, _j883, _o883, _r883
_a881, _h881, _j881, _o881, _r881, _s881 = _a883, _h883, _j883, _o883, _r883, _s883
ENGINE_URL883 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB883, MARKER883 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', 'AKBASCORE SILICON HIPPOCAMPUS — TEST883 / F1'
HEAD883 = '3d75f289b88271440f4e3e13c2491699e6dc14ca'
FIXTURE_BLOB883, FIXTURE_SHA883 = 'f75a94ebbab8272878050579988cd35cb1deb822', 'daf5a8c4bd36811328a4ab173fe5cd300cc93c812558b883232e60ae42967f21'


def blob883(raw):
    return _h883.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def engine_parts883():
    with _u883.urlopen(_u883.Request(ENGINE_URL883, headers={'User-Agent': 'AKBASCORE-TEST883'}), timeout=240) as r:
        raw = r.read()
    assert blob883(raw) == ENGINE_BLOB883, ('ENGINE_BLOB_MISMATCH', blob883(raw))
    text = raw.decode('utf-8'); _a883.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST883_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST883_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST883_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('883_engine.log', '883_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST883_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '883_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '883_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST883_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old)
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL883, 'git_blob': blob883(raw), 'sha256': _h883.sha256(raw).hexdigest()}


try:
    ENGINE883, ENGINE_INFO883 = engine_parts883()
except BaseException as _exc883:
    import time as _t883, traceback as _tb883
    _p883 = '/content/TEST883_PRE_ENGINE_ERROR_%s.txt' % _t883.strftime('%Y%m%dT%H%M%SZ', _t883.gmtime())
    try:
        with open(_p883, 'w', encoding='utf-8') as _f883: _f883.write(_tb883.format_exc())
    except OSError: _p883 = 'NOT_WRITTEN'
    print('TEST883 PRE-ENGINE ERROR (before console capture):', type(_exc883).__name__, _exc883, '| traceback:', _p883)
    raise
exec(compile(ENGINE883['prefix'], 'test870.py:prefix', 'exec'), globals())
exec(compile(ENGINE883['body'], 'test870.py:engine', 'exec'), globals())
print('TEST883 ENGINE', _j883.dumps(ENGINE_INFO883, sort_keys=True))

# ============================ locks and reused locked code ============================
CODELOAD864 = 'https://codeload.github.com/ceceli33/titan-cognitive-core-v3/zip/' + HEAD883
LOCKS864.update({'test870.py': ENGINE_BLOB883, 'Test870.log': 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc',
                 '873.py': '2e44affa5e0dd462155fb265c331270fb8e7b7e1', '873.log': '1c9eb9fca173003eaf45bc7726af13c2817324b7',
                 '874.py': '12172001ba3696ad91087a8b34d7995728259e47', '874.log': '1229e3b70440e3887ccf1bd7e3bad51f900f5313',
                 '877.py': 'a6aa7648e0fb765a8dc9b56b8f79b4dcef5fc772', '877.log': 'c4eb58021ed827fb13d5c15fee7c18541f6d4604',
                 '878.py': '7842e8675544a0328e3552f059c81b7750068a82', 'Test_878_log2.log': '2bfc7adc2a8f718c012a6d722a9e0a04a72cbedd',
                 '879.py': '92f9eb665173986b6c98b42f07eefb3249c861d4', '879.log': 'c1205bc082fb69c68b9f9f4e290808a0dec71fa8',
                 '880.py': '3e6aab5d79af8f75053b0da873d70779406adb74', '880.log': 'adcc0389b359b1dd254887edb1786fd5edff378a',
                 '881.py': '63466135610cedcdaa7c8c462499f987ef6f08cc', '881.log': 'e6e38359799faef306bb261ca97fcd6ca2a32ef5',
                 '882.py': 'bbd0c53f2bdd5eed7ed51886b852627617ff41d7', '882.log': '66479a74942098de4d2c482693fc28d108ddfe86',
                 '869_full_records.json.gz': FIXTURE_BLOB883})
REQUIRED_LOCKS883 = {'757.py': '3d88bf8638390995858f23391f1e043faa586835', '841.py': '135b18e5b1ea113579c607cf9eecf49628cf18c2',
                     '851.py': '0f01e73b9ad160c988cfe059e8b5ae5e1f35f65b'}
TEST878_PREREG883 = '0555ab01d436c0df7e8e1be21aea3170ac0a50d799a528796212298a48dc4103'
_a878, _h878, _j878 = _a883, _h883, _j883
ENGINE_BLOB878 = ENGINE_BLOB883
CONSTS878 = ('TEST877_CELL_BLOB878', 'TEST877_PREREG_DEPS878', 'TEST870_MINUTES', 'WORLDS878', 'SOURCES878', 'FORKS878',
             'SIDES874', '_h877', 'ARM878', 'FUNCS873', 'FUNCS874', 'FUNCS877', 'ROPE_TOL878', 'HARD_MIN878', 'PREREG878')
FUNCS878 = ('Partial878', 'Persist878', 'line878', 'source_audit878', 'load878', 'guard878', 'xspan878', 'next_kv878',
            'tsha878', 'write_exp878', 'load_exp878', 'append_exp878', 'xappend878', 'xcar878', 'arm878', 'jsafe878',
            'dif878', 'pa878', 'sig878', 'persist878', 'probe878')
CLASSES881 = ('Gate881',)
FUNCS881 = ('peak_update881', 'free_gib881', 'kv_gib881', 'timed881', 'seqlp881', 'cont_tokens881', 'same_reading881',
            'tsha881', 'full_seal881', 'xtrace881', 'zero_slot881', 'selftest_mask881')
BANNED883 = {'register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook', 'output_hidden_states',
             'output_attentions', 'install_all_output_capturing_hooks', 'backward', 'requires_grad_', 'zero_grad',
             'execute866', 'mount865', 'free865', 'hop865', 'DirectCut3', 'native_append_direct', 'route882', 'calibrate882',
             'preC882', 'query880'}
EXEC_ALLOW883 = {'episode883': ('execute866', 'hop865', 'mount865', 'free865')}
ORACLE883 = {'supported851', 'node851', 'world867', 'correct867', 'success867', 'worlds829', 'offline883', 'OFFLINE883',
             'score_fixture883', 'world_index_label', 'FIXTURE_SCORES883'}
RUNTIME883 = ('episode883', 'write_experience883', 'read_with_experience883', 'prepare_experience883', 'reading_view883',
              'guard883', 'cell_admission883')

# ============================ pre-registered design (fixed before the model is loaded) ============================
WORLD_POOL883 = ('03', '06', '07', '09', '10', '11')   # not 00/01 (TEST873-882 development), not 02/04/05/08 (TEST882 G3)
WORLD_SALT883, N_WORLDS883 = 'TEST883|F1|world|', 3   # rank by sha256(salt + world): outcome-free, fixed rule
CONDITIONS883 = ('MISSING', 'FORK')
ARMS883 = ('NOFB', 'CBLIND', 'VIS')                  # NOFB = live 869 NO_FEEDBACK baseline; CBLIND/VIS = F1 arms
HORIZON883 = 6
WALL_MIN883, FREE_MIN_GIB883, SAFETY883 = 75.0, 6.0, 1.25
CART_ROOT883 = '/content/TEST883_EPISODE_CARTRIDGES'  # outside ROOT864: isolated per episode, deleted after the episode
PREREG883 = {
    'test': 'TEST883 / F1 (name given by the user)', 'head': HEAD883,
    'hypotheses': {
        'H1': 'the physical experience E_t=[X2][A][C] of the previous step, read with C visible (VIS), changes the next native '
              'CAR action relative to the same cartridge with only its C span unreadable (C-BLIND)',
        'H2': 'that change is useful: MISSING stopping is not worse than the live NO_FEEDBACK baseline and FORK supported success '
              'improves over C-BLIND in at least two distinct worlds',
        'H0': 'no terminal / action difference, or the difference is not useful'},
    'state_builder': 'locked control_step867 with ctx.arm = NO_FEEDBACK for every F1 arm: FV/FK slots carry the 869 '
                     'NO_FEEDBACK content-free rows (MUE845 repeated, same shape); the experience cartridge replaces their content',
    'decision_memory': {'NOFB': 'B (environment memory) - reading = locked car867 inside control_step867',
                        'CBLIND': '[B][E_{t-1}] - locked xcar878(blind=[C span], sham=False)',
                        'VIS': '[B][E_{t-1}] - locked xcar878(blind=[C span], sham=True): same masked kernel, C made readable',
                        'step_1': 'CBLIND and VIS: xcar878 on B with blind=() (no experience exists yet)'},
    'experience': {'X2': 'the control X of step t (control prompt + action segments + review suffix), native forward on B_t',
                   'A': 'ACTION_IDS867 tokens of the executed native word',
                   'C': 'next model observation = hop and evidence rows produced at step t+1 on the environment memory',
                   'writer': 'locked write_exp878 (CUT3 lower K/V + h3) after bitwise lower / h3 next-layer gates',
                   'mount': 'locked load_exp878 (file + tensor SHA) + append_exp878 on B_{t+1}',
                   'only_latest': 'only E_{t-1} is mounted at decision t (explicit design, not truncation); earlier E stay on SSD '
                                  'unmounted with their SHA in cards_manifest',
                   'isolation': 'one directory per episode outside ROOT; deleted after the episode; never a bank card'},
    'unaffected_by_arm': 'hop865, gen849 evidence, evaluation, legacy rollout and direction866 all run on B (no cartridge): '
                         'the arm changes nothing but the decision reading',
    'worlds': 'first %d of %s ranked by sha256(%r + w)' % (N_WORLDS883, list(WORLD_POOL883), WORLD_SALT883),
    'conditions': CONDITIONS883, 'arms': ARMS883, 'horizon': HORIZON883,
    'endpoint': {'Y': 'success867 after all live work (MISSING: MODEL_STOP; FORK: supported851(accepted, world, mounted))',
                 'primary': 'per world x condition: Y_VIS - Y_CBLIND',
                 'PASS': 'FORK: Y_VIS=1 and Y_CBLIND=0 in >= 2 distinct worlds; no cell with Y_VIS=0 and Y_CBLIND=1; MISSING: '
                         'Y_VIS >= Y_NOFB in every world; all integrity gates PASS',
                 'NEGATIVE': 'everything else, labelled A NO_DIVERGENCE / B SIGNAL_WITHOUT_BENEFIT / E ACTION_EFFECT_WITHOUT_TASK_SUCCESS'
                             ' / DIVERGENCE_NOT_USEFUL', 'TECHNICAL_BLOCK': 'any integrity gate failure'},
    'secondary': ['first divergent step', 'action sequences', 'STOP / ACQUIRE counts', 'steps', 'calls', 'seconds', 'GPU GiB',
                  'cartridges written'],
    'gates': {'G0': 'sources, locks, A100, disk, prereg, CPU selftests, D0 causal-link re-audit',
              'G1': 'model load backbone of TEST882 (bitwise native regression, hook free), API presence',
              'G2': 'probe episode (first world, MISSING, CBLIND, 2 steps, excluded from analysis): write / reload / append parity, '
                    'B seal, zero-C bitwise invariance, trace == locked xcar878',
              'G3': 'live NOFB baselines for every cell; prefix comparison with the 869 NO_FEEDBACK fixture (REPLAY_CONFIRMED or '
                    'DIVERGED; a divergence is recorded, not hidden, and the live baseline is used)',
              'G4': 'CBLIND then VIS for every admitted cell', 'G5': 'sealed offline scoring', 'G6': 'decision matrix and report'},
    'budget': {'wall_min_hard': WALL_MIN883, 'free_vram_min_gib': FREE_MIN_GIB883,
               'cell_admission': 'start a cell (CBLIND + VIS) only if elapsed + 2 x horizon x measured max s/step x %.2f <= wall'
                                 % SAFETY883,
               'never_cut_mid_episode': 'a budget trip inside an episode ends it as BUDGET_STOP, recorded, and stops the experiment',
               'ESTIMATED': 'load ~21 min (882 log: 1245 s); 869 V_X 9.1 s/step; experience write + mount + explicit read not measured'},
    'limits': ['3 worlds x 2 conditions: a pilot; two worlds is a mechanical minimum, not a statistic',
               'MISSING vs LIVE bank sizes (21 vs 23) are not part of this test: within a cell all arms share one bank (SHA checked)',
               'the C of E_t is also present in the current state segments (C/E slots): VIS vs C-BLIND isolates reading C inside '
               'the episode context, as in TEST881']}
PREREG_SHA883 = sha256_bytes864(_j883.dumps(PREREG883, sort_keys=True).encode())
STATE883 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO883, 'prereg_sha256': PREREG_SHA883, 'source': {}, 'gates': {},
            'selftests': {}, 'd0': {}, 'g2': {}, 'baseline': {}, 'cells': {}, 'episodes': [], 'not_run': [], 'offline': None,
            'budget': {'adapter_ffe_lower_bound': 0.0, 'ffe_by_kind': {}, 'arms': {}, 'stages': {}, 'peak_alloc_gib': 0.0,
                       'peak_reserved_gib': 0.0, 'step_seconds': []},
            'result': None, 'error': None}
STATE881 = STATE878 = STATE877 = STATE883
T2_KEEP878, SRC878, TGT878, EXP878 = {}, {}, {}, {}


class Gate883(Exception):
    pass


class Budget883(Exception):
    pass


class Partial878(Exception):
    pass


def line883(*parts): short864('T883', *parts)


def ffe883(tokens, layers=80, kind='adapter'):
    x = float(tokens) * float(layers) / 80.0 / 256.0; b = STATE883['budget']
    b['adapter_ffe_lower_bound'] += x; b['ffe_by_kind'][kind] = b['ffe_by_kind'].get(kind, 0.0) + x
    return x


def gate883(name, status, **info):
    STATE883['gates'][name] = dict(info, status=status, wall_s=round(time.perf_counter() - T_START883, 1),
                                   peak_alloc_gib=round(STATE883['budget']['peak_alloc_gib'], 3))
    json_write864('gate_status.json', STATE883['gates'])
    line883('GATE', name, status, _j883.dumps(info, sort_keys=True, default=str)[:900])
    if status != 'PASS': raise Gate883('%s %s %s' % (name, status, _j883.dumps(info, default=str)[:600]))


# ============================ firewall ============================
def scan883(node, allow=()):
    calls = [c for c in _a883.walk(node) if isinstance(c, _a883.Call)]
    used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in calls}
    used |= {k.arg for k in _a883.walk(node) if isinstance(k, _a883.keyword)}
    used |= {n.id for n in _a883.walk(node) if isinstance(n, _a883.Name)} | {n.attr for n in _a883.walk(node) if isinstance(n, _a883.Attribute)}
    used |= {s.slice.value for s in _a883.walk(node) if isinstance(s, _a883.Subscript) and isinstance(s.slice, _a883.Constant)
             and isinstance(s.slice.value, str)}
    used |= {c.args[1].value for c in calls if getattr(c.func, 'id', None) in ('getattr', 'setattr', 'hasattr') and len(c.args) > 1
             and isinstance(c.args[1], _a883.Constant)}
    bad = (used & BANNED883) - set(allow)
    bad |= {'.step()' for c in calls if isinstance(c.func, _a883.Attribute) and c.func.attr == 'step'}   # optimizer step
    assert not bad, ('FIREWALL883', getattr(node, 'name', '?'), sorted(bad))


def oracle_scan883(node):
    names = {n.id for n in _a883.walk(node) if isinstance(n, _a883.Name)} | \
            {n.attr for n in _a883.walk(node) if isinstance(n, _a883.Attribute)}
    keys = {n.value for n in _a883.walk(node) if isinstance(n, _a883.Constant) and isinstance(n.value, str)}
    bad = (names | keys) & ORACLE883
    assert not bad, ('ORACLE_FIREWALL883', getattr(node, 'name', '?'), sorted(bad))


def capture_source883():
    try:
        source, how = get_ipython().history_manager.input_hist_raw[-1], 'IPYTHON_CURRENT_CELL'
    except NameError:
        source = open(__file__, encoding='utf-8').read() if '__file__' in globals() else None; how = 'FILE_%RUN'
    assert source and MARKER883 in source and 'def episode883' in source and 'def offline883' in source, \
        'EXECUTED_883_SOURCE_NOT_CAPTURED (paste all three parts into ONE cell, in order)'
    tree = _a883.parse(source)
    funcs = {n.name: n for n in tree.body if isinstance(n, _a883.FunctionDef)}
    for name, node in funcs.items():
        if name.endswith('883'): scan883(node, EXEC_ALLOW883.get(name, ()))
    assert set(RUNTIME883) <= set(funcs), ('RUNTIME_FUNCTIONS_MISSING', sorted(set(RUNTIME883) - set(funcs)))
    for name in RUNTIME883: oracle_scan883(funcs[name])
    calls = [n for n in _a883.walk(tree) if isinstance(n, _a883.Call) and getattr(n.func, 'id', None) == 'reproduce_pre859859']
    assert len(calls) == 1, 'MODEL_LOADER_CALL_COUNT_NOT_ONE'
    ex = [n for n in _a883.walk(tree) if isinstance(n, _a883.Call) and getattr(n.func, 'id', None) == 'execute866']
    assert len(ex) == 1, 'EXECUTOR_CALL_COUNT_NOT_ONE'
    (ROOT864 / 'TEST883.py').write_text(source, encoding='utf-8')
    STATE883['source'] = {'how': how, 'executed_cell_git_blob': git_blob864(source.encode()),
                          'executed_cell_sha256': sha256_bytes864(source.encode()), 'lines': source.count('\n') + 1,
                          'firewall': 'PASS', 'oracle_firewall': 'PASS (%d runtime functions)' % len(RUNTIME883),
                          'single_executor_call': True, 'self_hash': 'NONE (measured at runtime only)'}
    json_write864('TEST883_source_manifest.json', dict(STATE883['source'], prereg_sha256=PREREG_SHA883, head=HEAD883,
                                                       engine_blob=ENGINE_BLOB883, locks=dict(LOCKS864),
                                                       required=REQUIRED_LOCKS883, before_model_load=True))


def select_locked883():
    for name, b in REQUIRED_LOCKS883.items():
        assert LOCKS864.get(name) == b and git_blob864(RAW_SOURCES864[name]) == b, ('REQUIRED_LOCK', name)
    for name in ('878.py', '881.py', '882.py', '882.log', '869_full_records.json.gz'):
        assert git_blob864(RAW_SOURCES864[name]) == LOCKS864[name], ('LOCK', name)
    assert sha256_bytes864(RAW_SOURCES864['869_full_records.json.gz']) == FIXTURE_SHA883, 'FIXTURE_SHA256'
    t8 = _a883.parse(RAW_SOURCES864['878.py'].decode())
    c8 = [n for n in t8.body if isinstance(n, _a883.Assign) and
          {x.id for t in n.targets for x in _a883.walk(t) if isinstance(x, _a883.Name)} & set(CONSTS878)]
    f8 = [n for n in t8.body if isinstance(n, (_a883.FunctionDef, _a883.ClassDef)) and n.name in FUNCS878]
    assert {n.name for n in f8} == set(FUNCS878), 'SELECT_878'
    for n in f8:
        if isinstance(n, _a883.FunctionDef): scan883(n, ('native_append_direct',) if n.name == 'append_exp878' else ())
    exec(compile(_a883.fix_missing_locations(_a883.Module(c8, [])), '878.py:constants', 'exec'), globals())
    assert sha256_bytes864(_j883.dumps(PREREG878, sort_keys=True).encode()) == TEST878_PREREG883, 'TEST878_PREREG_MISMATCH'
    exec(compile(_a883.fix_missing_locations(_a883.Module(f8, [])), '878.py:selected', 'exec'), globals())
    t1 = _a883.parse(RAW_SOURCES864['881.py'].decode())
    f1 = [n for n in t1.body if isinstance(n, (_a883.FunctionDef, _a883.ClassDef)) and n.name in set(FUNCS881) | set(CLASSES881)]
    assert {n.name for n in f1} == set(FUNCS881) | set(CLASSES881), 'SELECT_881'
    for n in f1:
        if isinstance(n, _a883.FunctionDef): scan883(n)
    exec(compile(_a883.fix_missing_locations(_a883.Module(f1, [])), '881.py:selected', 'exec'), globals())
    log881, log882 = RAW_SOURCES864['881.log'].decode(), RAW_SOURCES864['882.log'].decode()
    prov = {'881': all(x in log881 for x in ('NVIDIA A100-SXM4-80GB', 'TEST881 VERDICT MASKED_PATH_C_SPECIFIC_SIGNAL', 'status COMPLETE')),
            '882': all(x in log882 for x in ('T882 G2 {"C_blind_provenance_dup_Z_equal": true', 'TEST882 VERDICT REVISE_ADDRESS_DOMAIN',
                                             'cell dc714a1190965cc8ac5098a79d66d8780a1abadb'))}
    assert all(prov.values()), ('LOCKED_LOG_PROVENANCE', prov)
    STATE883['source']['reused'] = {'878.py': LOCKS864['878.py'], 'functions878': sorted(FUNCS878), '881.py': LOCKS864['881.py'],
                                    'functions881': sorted(FUNCS881), 'not_reused_from_882': 'router / calibration / address encoder '
                                    '/ store: none of route882, calibrate882, preC882, query880, RealStore882 exists in this cell',
                                    'log_provenance': prov}


def guard883(stage):
    peak_update881(); el = (time.perf_counter() - T_START883) / 60.0; free = free_gib881()
    STATE883['budget']['stages'][stage] = {'wall_min': round(el, 2), 'free_gib': round(free, 2)}
    why = [x for x, bad in (('WALL %.1f>%.0f min' % (el, WALL_MIN883), el > WALL_MIN883),
                            ('VRAM_FREE %.2f<%.1f GiB' % (free, FREE_MIN_GIB883), free < FREE_MIN_GIB883)) if bad]
    if why: raise Budget883('%s: %s' % (stage, '; '.join(why)))


ffe881, guard881, line881 = ffe883, (lambda stage, need_gib=0.0: guard883(stage)), line883

# ============================ pure core (CPU-testable; no model, no labels) ============================
def select_worlds883():
    return sorted(WORLD_POOL883, key=lambda w: _h883.sha256((WORLD_SALT883 + w).encode()).hexdigest())[:N_WORLDS883]


def first_divergence883(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y: return i + 1
    return None if len(a) == len(b) else min(len(a), len(b)) + 1


def causal_effect883(events, ci):
    # the EFFECT caused by the CONTROL at events[ci]: the first EFFECT after it and before the next CONTROL, same action
    for e in events[ci + 1:]:
        if e['type'] == 'CONTROL': return None
        if e['type'] == 'EFFECT': return e if e.get('action') == events[ci].get('action') else None
    return None


def d0_causal883(records):
    # D0 re-audit with the causal link: the step-2 ACQUIRE effect must be caused by the step-2 CONTROL of the same record
    cj = lambda d: _j883.dumps(d, sort_keys=True)
    P = {(r['arm'], r['world_index'], r['condition']): r for r in records if r['phase'] in ('PANEL', 'GATE4')}
    out = {}
    for (arm, w, c), L in sorted(P.items()):
        if c != 'LIVE' or (arm, w, 'MISSING') not in P: continue
        M = P[(arm, w, 'MISSING')]; row = {'arm': arm, 'world_index': w}
        for tag, r in (('M', M), ('L', L)):
            cis = [i for i, e in enumerate(r['events']) if e['type'] == 'CONTROL']
            ci = next((i for i in cis if r['events'][i].get('step') == 2), None)
            eff = None if ci is None else causal_effect883(r['events'], ci)
            row[tag] = {'control_step2_index': ci, 'action': None if ci is None else r['events'][ci]['action'],
                        'state': None if ci is None else cj(r['events'][ci]['record']['state_sha256']),
                        'mounted_before': None if ci is None else r['events'][ci]['mounted'],
                        'effect': None if eff is None else eff.get('effect'),
                        'query': None if eff is None else (eff.get('provenance') or {}).get('query_sha256'),
                        'chosen': None if eff is None else eff.get('chosen'),
                        'bank_size': None if eff is None else (eff.get('route') or {}).get('n_candidates')}
        m, l = row['M'], row['L']
        row['eligible'] = bool(m['action'] == l['action'] == 'ACQUIRE' and m['state'] == l['state'] and m['state'] is not None
                               and m['effect'] == l['effect'] == 'MOUNTED' and m['query'] == l['query'] and m['query']
                               and m['mounted_before'] == l['mounted_before'] and m['chosen'] != l['chosen'])
        row['bank_sizes'] = [m['bank_size'], l['bank_size']]
        for tag in ('M', 'L'): row[tag].pop('state')
        out['%s|%02d' % (arm, w)] = row
    summary = _c883.Counter((v['arm'], v['eligible']) for v in out.values())
    return out, {a: {'eligible': summary[(a, True)], 'not_eligible': summary[(a, False)]} for a in sorted({v['arm'] for v in out.values()})}


def verdict883(cells, integrity_ok, blocks=()):
    # cells: {key: {world, cond, Y: {arm: 0 | 1 | None}, actions: {arm: list}, acq: {arm: int}, end: {arm: str}, accepted: {arm: str}}}
    if not integrity_ok or blocks: return {'result': 'TECHNICAL_BLOCK', 'labels': list(blocks) or ['INTEGRITY'], 'reason': 'integrity'}
    done = {k: c for k, c in cells.items() if c['Y'].get('VIS') is not None and c['Y'].get('CBLIND') is not None}
    if not done: return {'result': 'TECHNICAL_BLOCK', 'labels': ['NO_COMPLETED_CELL'], 'reason': 'no cell with both F1 arms scored'}
    harms = sorted(k for k, c in done.items() if c['Y']['VIS'] == 0 and c['Y']['CBLIND'] == 1)
    fork_gain = sorted({c['world'] for c in done.values() if c['cond'] == 'FORK' and c['Y']['VIS'] == 1 and c['Y']['CBLIND'] == 0})
    miss = [c for c in done.values() if c['cond'] == 'MISSING']
    missing_ok = bool(miss) and all(c['Y'].get('NOFB') is not None and c['Y']['VIS'] >= c['Y']['NOFB'] for c in miss)
    diverged = sorted(k for k, c in done.items() if c['actions']['VIS'] != c['actions']['CBLIND'])
    labels = []
    if not diverged: labels.append('A_NO_DIVERGENCE')
    if diverged and (not missing_ok or any(c['acq']['VIS'] > c['acq'].get('NOFB', c['acq']['VIS']) for c in miss)):
        labels.append('B_SIGNAL_WITHOUT_BENEFIT')
    if any(c['end']['VIS'] != c['end']['CBLIND'] and c['Y']['VIS'] == c['Y']['CBLIND'] for c in done.values()):
        labels.append('E_ACTION_EFFECT_WITHOUT_TASK_SUCCESS')
    ok = len(fork_gain) >= 2 and not harms and missing_ok
    if ok: return {'result': 'PASS', 'labels': ['C_F1_PILOT_POSITIVE'] + labels, 'fork_gain_worlds': fork_gain, 'harms': harms,
                   'diverged_cells': diverged, 'reason': 'FORK gain in %s, no harm, MISSING not worse than NOFB' % fork_gain}
    if not labels: labels.append('DIVERGENCE_NOT_USEFUL')
    return {'result': 'NEGATIVE', 'labels': labels, 'fork_gain_worlds': fork_gain, 'harms': harms, 'diverged_cells': diverged,
            'missing_not_worse_than_nofb': missing_ok,
            'reason': 'fork_gain_worlds=%s (need >= 2), harms=%s, missing_ok=%s' % (fork_gain, harms, missing_ok)}


def cell_admission883(elapsed_s, step_seconds):
    s = max(step_seconds) if step_seconds else None
    if s is None: return True, None
    projected = elapsed_s + 2 * HORIZON883 * s * SAFETY883
    return projected <= WALL_MIN883 * 60.0, projected


# ============================ CPU selftests (before the model is loaded) ============================
def st_worlds883():
    w = select_worlds883()
    return {'three_worlds': len(w) == 3, 'rule_is_deterministic': w == select_worlds883(),
            'disjoint_from_882_calibration_and_development': not set(w) & {'00', '01', '02', '04', '05', '08'},
            'expected_from_prereg_rule': w == ['10', '09', '03']}


def st_divergence883():
    ev = [{'type': 'CONTROL', 'action': 'ACQUIRE', 'step': 2}, {'type': 'CONTROL', 'action': 'ACQUIRE', 'step': 3},
          {'type': 'EFFECT', 'action': 'ACQUIRE', 'effect': 'MOUNTED'}]
    ev2 = [{'type': 'CONTROL', 'action': 'ACQUIRE', 'step': 2}, {'type': 'EFFECT', 'action': 'ADVANCE', 'effect': 'POINTER_ADVANCED'}]
    ev3 = [{'type': 'CONTROL', 'action': 'ACQUIRE', 'step': 2}, {'type': 'HOP'}, {'type': 'EFFECT', 'action': 'ACQUIRE', 'effect': 'MOUNTED'}]
    return {'causal_link_rejects_effect_of_a_later_control': causal_effect883(ev, 0) is None,
            'causal_link_rejects_other_action': causal_effect883(ev2, 0) is None,
            'causal_link_accepts_own_effect': (causal_effect883(ev3, 0) or {}).get('effect') == 'MOUNTED',
            'none_when_equal': first_divergence883(['ADVANCE', 'STOP'], ['ADVANCE', 'STOP']) is None,
            'first_index_1_based': first_divergence883(['ADVANCE', 'ACQUIRE'], ['ADVANCE', 'STOP']) == 2,
            'length_difference': first_divergence883(['ADVANCE'], ['ADVANCE', 'STOP']) == 2,
            'step_one': first_divergence883(['STOP'], ['ACQUIRE']) == 1}


def st_verdict883():
    def cell(w, c, yv, yc, yn, av, ac, acq=(0, 0, 0), ev='MODEL_STOP', ec='MODEL_STOP'):
        return {'world': w, 'cond': c, 'Y': {'VIS': yv, 'CBLIND': yc, 'NOFB': yn}, 'actions': {'VIS': av, 'CBLIND': ac},
                'acq': {'VIS': acq[0], 'CBLIND': acq[1], 'NOFB': acq[2]}, 'end': {'VIS': ev, 'CBLIND': ec}}
    same = ['ADVANCE', 'STOP']
    base = {'10M': cell('10', 'MISSING', 1, 1, 1, same, same), '09M': cell('09', 'MISSING', 1, 1, 1, same, same),
            '10F': cell('10', 'FORK', 1, 0, 0, ['ACCEPT'], ['ACQUIRE'], ev='MODEL_ACCEPT', ec='OBSERVATION_HORIZON'),
            '09F': cell('09', 'FORK', 1, 0, 0, ['ACCEPT'], ['ACQUIRE'], ev='MODEL_ACCEPT', ec='OBSERVATION_HORIZON')}
    p = verdict883(base, True)
    one = dict(base); one['09F'] = cell('09', 'FORK', 0, 0, 0, same, same)
    harm = dict(base); harm['03F'] = cell('03', 'FORK', 0, 1, 0, ['ACQUIRE'], ['ACCEPT'], ev='OBSERVATION_HORIZON', ec='MODEL_ACCEPT')
    miss = dict(base); miss['10M'] = cell('10', 'MISSING', 0, 1, 1, ['ACQUIRE'] * 6, same, acq=(6, 0, 0), ev='OBSERVATION_HORIZON')
    nodiv = {k: cell(v['world'], v['cond'], 0, 0, 0, same, same) for k, v in base.items()}
    eff = {'10F': cell('10', 'FORK', 0, 0, 0, ['ACCEPT'], ['ACQUIRE'], ev='MODEL_ACCEPT', ec='OBSERVATION_HORIZON'),
           '10M': cell('10', 'MISSING', 1, 1, 1, same, same)}
    miss2 = dict(base); miss2['10M'] = cell('10', 'MISSING', 0, 0, 1, ['ACQUIRE'] * 6, ['ACQUIRE'] * 6, acq=(6, 6, 0), ev='HORIZON_6',
                                           ec='HORIZON_6')
    return {'pass_case': p['result'] == 'PASS' and p['fork_gain_worlds'] == ['09', '10'],
            'missing_below_nofb_blocks_pass_even_without_harm': verdict883(miss2, True)['result'] == 'NEGATIVE',
            'one_fork_gain_is_negative': verdict883(one, True)['result'] == 'NEGATIVE',
            'any_harm_is_negative': verdict883(harm, True)['result'] == 'NEGATIVE',
            'missing_worse_than_nofb_is_B': 'B_SIGNAL_WITHOUT_BENEFIT' in verdict883(miss, True)['labels'],
            'no_divergence_is_A': verdict883(nodiv, True)['labels'] == ['A_NO_DIVERGENCE'],
            'accept_without_support_is_E': 'E_ACTION_EFFECT_WITHOUT_TASK_SUCCESS' in verdict883(eff, True)['labels'],
            'integrity_failure_blocks': verdict883(base, False)['result'] == 'TECHNICAL_BLOCK',
            'unscored_cells_block': verdict883({'x': cell('10', 'FORK', None, 0, 0, same, same)}, True)['result'] == 'TECHNICAL_BLOCK'}


def st_firewall883():
    res = {}
    cases = {'executor_outside_episode': ('def f883(env):\n    execute866(env, 1, 2, 3, 4, 5)\n', BANNED883),
             'hook': ('def f883(m):\n    m.register_forward_hook(1)\n', BANNED883),
             'hidden_states_kw': ('def f883(m):\n    m(output_hidden_states=True)\n', BANNED883),
             'router_882': ('def f883(a):\n    return route882(a)\n', BANNED883),
             'optimizer_step': ('def f883(o):\n    o.step()\n', BANNED883)}
    for k, (src, _) in cases.items():
        try: scan883(_a883.parse(src).body[0]); res[k + '_refused'] = False
        except AssertionError: res[k + '_refused'] = True
    for k, src in {'oracle_success': 'def f883(env, r, s):\n    return success867(env, r, s)\n',
                   'oracle_worlds': "def f883(env):\n    return env['worlds829']\n"}.items():
        try: oracle_scan883(_a883.parse(src).body[0]); res[k + '_refused'] = False
        except AssertionError: res[k + '_refused'] = True
    try: scan883(_a883.parse('def f883(x):\n    step = x + 1\n    return step\n').body[0]); res['data_name_step_allowed'] = True
    except AssertionError: res['data_name_step_allowed'] = False
    return res


def st_prereg883():
    a = sha256_bytes864(_j883.dumps(PREREG883, sort_keys=True).encode())
    b = sha256_bytes864(_j883.dumps(dict(PREREG883, horizon=HORIZON883 + 1), sort_keys=True).encode())
    return {'prereg_sha_reproduces': a == PREREG_SHA883, 'prereg_sha_sensitive': a != b,
            'arms_exact': tuple(PREREG883['arms']) == ('NOFB', 'CBLIND', 'VIS')}


def st_rope883():
    rng = _np883.random.default_rng(883); d = 16; inv = 1.0 / (1e6 ** (_np883.arange(0, d, 2) / d))
    def rot(x, pos, sign=1.0):
        ang = sign * _np883.outer(pos, inv); c, s = _np883.cos(ang), _np883.sin(ang); x1, x2 = x[:, :d // 2], x[:, d // 2:]
        return _np883.concatenate([x1 * c - x2 * s, x1 * s + x2 * c], axis=1)
    reph = lambda x, a, b: rot(rot(x, a, -1.0), b)
    k = rng.standard_normal((64, d)); pa, pb = _np883.arange(30, 94), _np883.arange(412, 476)
    back = reph(reph(k, pa, pb), pb, pa); wrong = reph(reph(k, pa, pb), pb + 1, pa)
    return {'roundtrip': float(_np883.linalg.norm(back - k) / _np883.linalg.norm(k)) < 1e-10,
            'wrong_position_detected': float(_np883.linalg.norm(wrong - k) / _np883.linalg.norm(k)) > 1e-2}


def st_d0_883():
    recs = _j883.loads(_g883.decompress(RAW_SOURCES864['869_full_records.json.gz']))
    units = _c883.Counter((r['item'], r['arm'], r['phase']) for r in recs)
    rows, summ = d0_causal883(recs)
    STATE883['d0'] = {'pairs': rows, 'summary': summ, 'records': len(recs),
                      'note': 'bank sizes differ (MISSING 21 vs LIVE 23): the pair contrast is card + bank, not one card'}
    json_write864('TEST883_d0_causal.json', STATE883['d0'])
    nofb = summ.get('NO_FEEDBACK', {})
    return {'records_295': len(recs) == 295, 'unit_item_arm_phase_unique': max(units.values()) == 1,
            'causal_link_checked_for_every_pair': all(v['M']['control_step2_index'] is not None for v in rows.values()),
            'no_feedback_pairs_counted': nofb.get('eligible', 0) + nofb.get('not_eligible', 0) == 12,
            'bank_sizes_recorded': all(v['bank_sizes'][0] is not None for v in rows.values() if v['eligible'])}


def run_selftests883():
    tests = {'worlds': st_worlds883, 'divergence': st_divergence883, 'verdict': st_verdict883, 'firewall': st_firewall883,
             'prereg': st_prereg883, 'rope': st_rope883, 'd0_causal': st_d0_883}
    out, bad = {}, []
    for k, fn in tests.items():
        try:
            r = fn(); out[k] = r
            if not all(v is True for v in r.values()): bad.append(k)
        except BaseException as exc:
            out[k] = {'error': '%s: %s' % (type(exc).__name__, exc)}; bad.append(k)
    try:
        out['mask_locked_881'] = {k: v for k, v in selftest_mask881().items() if k != 'scope'}
        STATE883['selftests'].pop('mask', None)
    except BaseException as exc:
        out['mask_locked_881'] = {'error': '%s: %s' % (type(exc).__name__, exc)}; bad.append('mask_locked_881')
    STATE883['selftests'].update(out)
    json_write864('TEST883_cpu_selftest.json', {'results': out, 'failed': bad, 'prereg_sha256': PREREG_SHA883})
    if bad: raise Gate883('G0_CPU_SELFTEST_FAIL %s' % bad)
    return out

# ============================ runtime: one F1 episode (native decisions, literal executor, physical experience) ============================
def reading_view883(r):
    return {'action': r['action'], 'argmax_word': r.get('argmax_word'), 'abstain': r.get('abstain'), 'mass': r.get('mass'),
            'normalized': r.get('normalized'), 'margin_logp': r.get('margin_logp'),
            'scores': [{'word': s['word'], 'token_logps': s['token_logps'], 'sequence_logp': s['sequence_logp']} for s in r['scores']]}


def prepare_experience883(env, cache, B, X, action):
    # [B][X] is already in `cache` (left there by the locked car873); add A natively, then the explicit L0-3 rows of X and A
    cut, dev, Hd = APPEND873['CUT'], env['DEV'], int(env['H']); n2, L2 = length873(env, B), int(X.shape[0])
    own = env['cache_build'](list(kv873(env, cache)))
    A = list(dict(ACTION_IDS867)[action]); la = len(A); EA = env['embed841'](A)
    forward873(env, own, EA, n2 + L2); keep = kv873(env, own); del own
    one = lambda n: torch.ones((1, n), device=dev, dtype=torch.long)
    cl = env['cache_build'](list(B))
    hx = xspan878(env, cl, X.reshape(1, L2, Hd), one(n2 + L2), 0, cut + 1)
    ha = xspan878(env, cl, EA.reshape(1, la, Hd), one(n2 + L2 + la), 0, cut + 1)
    ck = {'X2A_explicit_lower_KV_bitwise': all(torch.equal(x, y) for i in range(cut + 1) for x, y in zip(cache_kv870(cl, i), keep[i]))}
    nk = [next_kv878(env, hx, n2), next_kv878(env, ha, n2 + L2)]; ref = keep[cut + 1]
    ck['X2A_h3_next_layer_KV_bitwise'] = all(torch.equal(nk[j][t], ref[t][:, :, a:b]) for j, (a, b) in
                                             enumerate(((n2, n2 + L2), (n2 + L2, n2 + L2 + la))) for t in (0, 1))
    del nk
    ffe883(la, 80, 'experience_action'); ffe883(L2 + la, cut + 1, 'experience_lower')
    return {'keep': keep, 'cl': cl, 'hx': hx, 'ha': ha, 'n2': n2, 'L2': L2, 'la': la, 'A': A, 'action': action,
            'X_sha256': tsha881(X), 'checks': ck}


def write_experience883(env, E, c_rows, e_rows, cdir, meta):
    # C = the next model observation (hop + evidence rows of the following step); written by the locked write_exp878
    global EXP_DIR878
    cut, dev, Hd = APPEND873['CUT'], env['DEV'], int(env['H']); n1 = E['n2'] + E['L2'] + E['la']
    one = lambda n: torch.ones((1, n), device=dev, dtype=torch.long)
    Y, _ = env['make_x851'](env['C_SLOT851'], [([], c_rows), (env['E_SLOT851'], e_rows)], []); body = int(Y.shape[0])
    own2 = env['cache_build'](list(E['keep'])); forward873(env, own2, Y, n1); gH = kv873(env, own2); del own2
    h3c = xspan878(env, E['cl'], Y.reshape(1, body, Hd), one(n1 + body), 0, cut + 1)
    ck = dict(E['checks'])
    ck['C_explicit_lower_KV_bitwise'] = all(torch.equal(a[:, :, n1:], b[:, :, n1:n1 + body]) for i in range(cut + 1)
                                            for a, b in zip(cache_kv870(E['cl'], i), gH[i]))
    ck['C_h3_next_layer_KV_bitwise'] = all(torch.equal(a, b[:, :, n1:n1 + body]) for a, b in zip(next_kv878(env, h3c, n1), gH[cut + 1]))
    ffe883(body, 80 + cut + 1, 'experience_C')
    if not all(ck.values()): raise Gate883('EXPERIENCE_WRITE_GATES %s' % sorted(k for k, v in ck.items() if not v))
    prov = dict(meta, test='TEST883', namespace='EPISODE_ONLY_NOT_A_BANK_CARD', requires_parent=False, action=E['action'],
                action_token_ids=E['A'], X_sha256=E['X_sha256'], source_prefix_tokens=E['n2'],
                spans_body={'X2': [0, E['L2']], 'A': [E['L2'], E['L2'] + E['la']], 'C': [E['L2'] + E['la'], E['L2'] + E['la'] + body]},
                C_kind='NEXT_MODEL_OBSERVATION (hop + evidence of the following step)', C_rows_sha256=env['stats849'](c_rows)['sha256'],
                E_rows_sha256=env['stats849'](e_rows)['sha256'], weights_digest=WEIGHTS0_878, engine_git_blob=ENGINE_BLOB883,
                head=HEAD883, cell_git_blob=STATE883['source'].get('executed_cell_git_blob'))
    eid = 'X883_' + sha256_bytes864(_j883.dumps(prov, sort_keys=True, default=str).encode())[:16]
    old, EXP_DIR878 = EXP_DIR878, type(ROOT864)(cdir)
    try:
        entry = write_exp878(env, eid, gH, torch.cat([E['hx'], E['ha'], h3c], dim=1), E['n2'], n1 + body, E['L2'] + E['la'], prov)
    finally:
        EXP_DIR878 = old
    if entry['roundtrip_K_rel'] > ROPE_TOL878: raise Gate883('EXPERIENCE_ROUNDTRIP %.3e' % entry['roundtrip_K_rel'])
    rec = {k: entry[k] for k in ('id', 'sha256', 'bytes', 'body_tokens', 'roundtrip_K_rel', 'pre_C_seal')}
    rec.update({'tensor_sha': entry.get('tensor_sha'), 'C_span_body': prov['spans_body']['C'], 'checks': ck,
                'episode_prev_cartridge': meta.get('episode_prev_cartridge')})
    with open(ROOT864 / 'cards_manifest.jsonl', 'a', encoding='utf-8') as f:
        f.write(_j883.dumps(dict(rec, **{k: meta[k] for k in ('episode_id', 'world_index', 'condition', 'arm', 'step_written')}),
                            sort_keys=True, default=str) + '\n')
    del gH, h3c, Y
    return entry, rec


def read_with_experience883(env, B, entry, X, arm, first):
    # decision reading on [B][E]: CBLIND hides only the C span; VIS reads it through the same masked kernel (TEST881 contract)
    seal0 = full_seal881(B)['all'] if first else None
    cp = load_exp878(env, entry); q = int(cp['body_tokens']); n0 = length873(env, B)
    g = append_exp878(env, B, cp); ffe883(q, 80, 'experience_mount')
    sp = entry['provenance']['spans_body']; C = [n0 + sp['C'][0], n0 + sp['C'][1]]
    rec = {'cartridge': entry['id'], 'positions': [n0, n0 + q], 'C_span': C, 'n_exact': length873(env, g) == n0 + q,
           'prefix_rows_bitwise_first_last_layer': bool(torch.equal(g[0][0][:, :, :n0], B[0][0]) and torch.equal(g[-1][1][:, :, :n0], B[-1][1]))}
    if first:
        gx = xappend878(env, B, cp, ()); ffe883(q, 80, 'experience_mount_parity')
        rec['explicit_equals_native_append_bitwise'] = all(torch.equal(a[t], b[t]) for a, b in zip(g, gx) for t in (0, 1)); del gx
        rec['B_full_seal_unchanged'] = full_seal881(B)['all'] == seal0
    if arm == 'CBLIND' and first:
        rd, tr = xtrace881(env, g, X, [C]); gz = zero_slot881(env, g, C[0], C[1]); rz, tz = xtrace881(env, gz, X, [C]); del gz
        rec['zero_C'] = {'reading_invariant': same_reading881(rd, rz), 'X_KV_80_layers_bitwise': tr['X']['kv'] == tz['X']['kv'],
                         'X_final_hidden_bitwise': tr['X']['hidden'] == tz['X']['hidden'],
                         'continuations_bitwise': tr['continuations'] == tz['continuations'],
                         'mask_and_positions_equal': tr['X']['mask_sha256'] == tz['X']['mask_sha256'] and tr['X']['positions'] == tz['X']['positions']}
    reading = xcar878(env, g, X, [C], arm == 'VIS'); ffe883(int(X.shape[0]) + cont_tokens881(), 80, 'decision_read')
    if arm == 'CBLIND' and first: rec['trace_equals_locked_xcar878'] = same_reading881(rd, reading)
    del g, cp
    flat = [v for k, v in rec.items() if isinstance(v, bool)] + [v for v in (rec.get('zero_C') or {}).values()]
    if not all(flat): raise Gate883('EXPERIENCE_READ_GATES %s' % _j883.dumps(rec, default=str)[:700])
    return reading, rec


def episode883(env, spec, arm, ep_id, horizon):
    key = {'world_index': int(spec['world_index']), 'condition': spec['condition'], 'arm': arm, 'episode_id': ep_id}
    ctx = {'spec': spec, 'arm': 'NO_FEEDBACK', 'M': list(spec['initial']), 'memx': None, 'path': [], 'prev_state': None,
           'own_states': [], 'events': [], 'mount_records': [], 'acquisitions': 0, 'rejections': 0, 'addresses': 0,
           'steps': 0, 'hops': 0, 'donor_item': None}
    cdir = _o883.path.join(CART_ROOT883, ep_id); _o883.makedirs(cdir, exist_ok=False)
    q = env['QTEXT841'][spec['qid']]; pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
    out = dict(key, item=spec['item'], steps=[], end=None, accepted=None, error=None, cartridges=[], first_read_done=False)
    E, last_entry, prev_hop, t0, calls0 = None, None, None, time.perf_counter(), int(env['CALLS849'])
    ctx['memx'], mount = mount865(env, ctx['M'], '883_L0_%s_%s' % (arm, spec['item'])); ctx['mount_records'].append(mount)
    initial_seal = prefix_seals865(env, ctx['memx'])
    out['start'] = {'bank_sha256': sha256_bytes864(_j883.dumps(sorted((c, env['entries'][c]['sha256']) for c in spec['pool'])).encode()),
                    'bank_size': len(spec['pool']), 'initial': list(spec['initial']), 'initial_seal': initial_seal,
                    'memory_tokens': length873(env, ctx['memx']), 'cartridge_dir_empty': not _o883.listdir(cdir)}
    pending = None
    try:
        while out['end'] is None:
            if ctx['steps'] >= horizon: out['end'] = 'HORIZON_%d' % horizon; break
            if not budget_left865(env, STEP_CALLS867): out['end'] = 'RESOURCE_BUDGET'; break
            guard883('%s_t%d' % (ep_id, ctx['steps'] + 1)); ts = time.perf_counter()
            k = len(ctx['path']); pointer = None if k == 0 else ctx['path'][-1]['rows']
            h, kind = hop865(env, ctx['memx'], spec['qid'], k, pointer); ctx['hops'] += 1
            ctx['events'].append({'type': 'HOP', 'k': k, 'kind_logged_only': kind, 'raw': h['text'], 'mounted': list(ctx['M']),
                                  'decision_source': 'MODEL'})
            if kind == 'EMPTY_OUTPUT': out['end'] = 'NATIVE_EMPTY_OUTPUT'; break
            feedback, fb_info = feedback867(env, ctx)
            control, record, state = control_step867(env, ctx, h, pointer, feedback)
            if control is None: out['end'] = 'NATIVE_EMPTY_STATE'; break
            ctx['steps'] += 1; B = ctx['memx']; X, _ = env['make_x851'](pre, state['segments'], post)
            st = dict(key, step=ctx['steps'], k=k, hop=h['text'], hop_changed=None if prev_hop is None else h['text'] != prev_hop,
                      state_sha256=record['state_sha256'], X_sha256=tsha881(X), B_tokens=length873(env, B), mounted_before=list(ctx['M']),
                      feedback=fb_info['source'], nofb_reading=reading_view883(record['reading']), legacy=record['legacy_action'])
            prev_hop = h['text']
            if arm == 'NOFB':
                reading, st['decision'] = record['reading'], {'memory': 'B', 'path': 'locked car867 inside control_step867'}
                cache = None
            else:
                cache = env['cache_build'](list(B)); nat = car873(env, cache, X); ffe883(int(X.shape[0]) + cont_tokens881(), 80, 'native_read')
                st['car873_equals_car867'] = same_reading881(nat, record['reading'])
                if not st['car873_equals_car867']: raise Gate883('X_PARITY car873 != control_step867 reading at %s t%d' % (ep_id, ctx['steps']))
                if pending is not None:
                    c_rows, e_rows = state['segments'][0][1], state['segments'][1][1]
                    last_entry, wrec = write_experience883(env, pending, c_rows, e_rows, cdir, dict(
                        key, step_written=ctx['steps'] - 1, episode_prev_cartridge=None if not out['cartridges'] else out['cartridges'][-1]['id']))
                    out['cartridges'].append(wrec); st['experience_written'] = wrec['id']; del pending; pending = None
                if last_entry is None:
                    reading = xcar878(env, B, X, (), False); ffe883(int(X.shape[0]) + cont_tokens881(), 80, 'decision_read')
                    st['decision'] = {'memory': 'B (no experience yet)', 'path': 'xcar878 blind=()',
                                      'explicit_equals_native': same_reading881(reading, record['reading'])}
                else:
                    reading, rrec = read_with_experience883(env, B, last_entry, X, arm, not out['first_read_done'])
                    out['first_read_done'] = True
                    st['decision'] = dict(rrec, memory='[B][E_t-1]', path='xcar878 blind=[C] sham=%s' % (arm == 'VIS'))
            action = reading['action']
            st.update({'reading': reading_view883(reading), 'action': action, 'decision_source': 'MODEL_CAR_READING_ON_ARM_MEMORY',
                       'differs_from_nofb_reading': action != record['action']})
            ctx['events'].append({'type': 'CONTROL', 'k': k, 'step': ctx['steps'], 'action': action, 'decision_source': 'MODEL',
                                  'mounted': list(ctx['M']), 'state_sha256': record['state_sha256'], 'f1_arm': arm})
            terminal = action in ('INVALID', 'ACCEPT', 'STOP')
            if arm != 'NOFB' and not terminal: pending = prepare_experience883(env, cache, B, X, action)
            del cache
            if action == 'INVALID': out['end'] = 'MODEL_INVALID_ACTION'
            elif action == 'ACCEPT': out['end'], out['accepted'] = 'MODEL_ACCEPT', h['text'].strip()
            elif action == 'STOP': out['end'] = 'MODEL_STOP'
            else:
                ctx['prev_state'] = state['own_state']
                execute866(env, ctx, action, h, control, state)
                eff = ctx['events'][-1]
                st['effect'] = {x: eff.get(x) for x in ('action', 'effect', 'chosen', 'mounted_before', 'mounted_after', 'path_after',
                                                       'direction_text', 'address_origin')}
                st['effect']['route'] = eff.get('route'); st['effect']['query_sha256'] = (eff.get('provenance') or {}).get('query_sha256')
                if eff.get('mount'): st['effect']['n_exact'] = eff['mount'].get('n_exact')
                st['effect']['executed_equals_reading'] = eff.get('action') == action
            st['seconds'] = round(time.perf_counter() - ts, 3); st['calls'] = int(env['CALLS849']) - calls0
            out['steps'].append(st)
            with open(ROOT864 / 'decisions.jsonl', 'a', encoding='utf-8') as f: f.write(_j883.dumps(jsafe878(st), sort_keys=True) + '\n')
            top3 = sorted(reading['normalized'].items(), key=lambda kv: -kv[1])[:3]
            line883('STEP', ep_id, 't=%d' % ctx['steps'], 'hop=%r' % h['text'], 'CAR=' + '|'.join('%s:%.3f' % (w, p) for w, p in top3),
                    'exec=%s' % action, 'nofb=%s' % record['action'], 'effect=%s' % (st.get('effect') or {}).get('effect'),
                    's=%.1f' % st['seconds'])
            if arm != 'NOFB': STATE883['budget']['step_seconds'].append(st['seconds'])
    except AssertionError as exc:
        if exc.args and isinstance(exc.args[0], tuple) and exc.args[0] and exc.args[0][0] == 'CONTEXT_LIMIT':
            out['end'] = 'PHYSICAL_CONTEXT_LIMIT'; out['error'] = str(exc)
        else:
            out['end'], out['error'], out['traceback'] = 'EXECUTION_ERROR', '%s: %s' % (type(exc).__name__, exc), traceback.format_exc()
    except Budget883 as exc:
        out['end'], out['error'] = 'BUDGET_STOP', str(exc)
    except Gate883 as exc:
        out['end'], out['error'], out['traceback'] = 'TECHNICAL_BLOCK', str(exc), traceback.format_exc()
    except Exception as exc:
        out['end'], out['error'], out['traceback'] = 'EXECUTION_ERROR', '%s: %s' % (type(exc).__name__, exc), traceback.format_exc()
    pending = None; gc.collect(); torch.cuda.empty_cache()
    effects = [e for e in ctx['events'] if e['type'] == 'EFFECT']; controls = [e for e in ctx['events'] if e['type'] == 'CONTROL']
    out.update({'final_mounted': list(ctx['M']), 'path': [p['text'] for p in ctx['path']], 'n_steps': ctx['steps'],
                'actions': [c['action'] for c in controls], 'effects': [e['effect'] for e in effects], 'acquisitions': ctx['acquisitions'],
                'executed_equals_reading': all(e['action'] == c['action'] for c, e in zip(controls, effects)),
                'mount_integrity': bool(ctx['mount_records']) and all(m['n_exact'] and m['all_80_layers'] and m['finite'] and
                                                                      m['prior_prefix_exact'] is not False for m in ctx['mount_records'])})
    try:
        free865(env, ctx['memx']); ctx['memx'] = None
        rm, _ = mount865(env, spec['initial'], '883_LR_%s_%s' % (arm, spec['item']))
        out['exact_restore'] = prefix_seals865(env, rm) == initial_seal; free865(env, rm)
    except Exception as exc:
        out['exact_restore'] = False; out['restore_error'] = '%s: %s' % (type(exc).__name__, exc)
    out['cartridges_deleted'] = sorted(_o883.listdir(cdir)); _s883.rmtree(cdir, ignore_errors=True)
    out['isolated_after_episode'] = not _o883.path.exists(cdir)
    out['seconds'] = round(time.perf_counter() - t0, 1); out['calls'] = int(env['CALLS849']) - calls0
    line883('EPISODE', ep_id, 'end=%s' % out['end'], 'actions=%s' % '>'.join(out['actions']), 'accepted=%r' % out['accepted'],
            'cards=%d' % len(out['cartridges']), 'restore=%s' % out['exact_restore'], 's=%.0f' % out['seconds'],
            '' if not out['error'] else 'ERROR=' + str(out['error'])[:300])
    if out.get('traceback'): short864(out['traceback'])
    rec = {k: v for k, v in out.items() if k != 'steps'}
    with open(ROOT864 / 'episodes.jsonl', 'a', encoding='utf-8') as f: f.write(_j883.dumps(jsafe878(rec), sort_keys=True) + '\n')
    STATE883['episodes'].append(out)
    if out['end'] in ('BUDGET_STOP',): raise Budget883(out['error'])
    if out['end'] in ('TECHNICAL_BLOCK', 'EXECUTION_ERROR') or not out['exact_restore'] or not out['mount_integrity'] or \
            not out['executed_equals_reading'] or not out['isolated_after_episode']:
        raise Gate883('EPISODE_INTEGRITY %s end=%s restore=%s mount=%s exec=%s err=%s' % (
            ep_id, out['end'], out['exact_restore'], out['mount_integrity'], out['executed_equals_reading'], str(out['error'])[:300]))
    return out

# ============================ G3 baseline comparison, cell assembly, sealed offline scoring ============================
def compare_fixture883(ep, ref):
    cj = lambda d: _j883.dumps(d, sort_keys=True)
    rc = [e for e in ref['events'] if e['type'] == 'CONTROL']; rf = [e for e in ref['events'] if e['type'] == 'EFFECT']
    n = len(ep['steps']); out = {'fixture_actions': [c['action'] for c in rc], 'live_actions': ep['actions'],
                                 'fixture_end': ref['end'], 'live_end': ep['end'], 'steps_compared': n}
    out['actions_prefix_equal'] = ep['actions'] == out['fixture_actions'][:n]
    out['state_sha_prefix_equal'] = all(cj(s['state_sha256']) == cj(c['record']['state_sha256']) for s, c in zip(ep['steps'], rc))
    out['effects_prefix_equal'] = ep['effects'] == [e['effect'] for e in rf][:len(ep['effects'])]
    out['first_divergent_step'] = first_divergence883(ep['actions'], out['fixture_actions'][:max(n, 1)])
    fixture_within = len(rc) <= HORIZON883
    out['end_consistent'] = (ep['end'] == ref['end']) if fixture_within else ep['end'] == 'HORIZON_%d' % HORIZON883
    out['label'] = 'REPLAY_CONFIRMED' if (out['actions_prefix_equal'] and out['state_sha_prefix_equal'] and
                                          out['effects_prefix_equal'] and out['end_consistent']) else 'DIVERGED_LIVE_BASELINE_USED'
    return out


def assemble_cell883(w, c, eps):
    nb, cb, vi = eps['NOFB'], eps['CBLIND'], eps['VIS']
    d = first_divergence883(cb['actions'], vi['actions'])
    upto = (d - 1) if d else min(len(cb['steps']), len(vi['steps']))
    pre = all(a['state_sha256'] == b['state_sha256'] and a['X_sha256'] == b['X_sha256'] and a['B_tokens'] == b['B_tokens']
              for a, b in zip(cb['steps'][:upto], vi['steps'][:upto]))
    cards = all(x.get('tensor_sha') == y.get('tensor_sha') and x['pre_C_seal'] == y['pre_C_seal']
                for x, y in zip(cb['cartridges'][:max(upto - 1, 0)], vi['cartridges'][:max(upto - 1, 0)]))
    same_start = len({_j883.dumps(e['start'], sort_keys=True) for e in (nb, cb, vi)}) == 1
    step1 = bool(nb['steps'] and cb['steps'] and vi['steps']) and nb['steps'][0]['state_sha256'] == cb['steps'][0]['state_sha256'] == \
        vi['steps'][0]['state_sha256']
    return {'world': w, 'cond': c, 'first_divergent_step_VIS_vs_CBLIND': d,
            'first_divergent_step_VIS_vs_NOFB': first_divergence883(nb['actions'], vi['actions']),
            'actions': {a: eps[a]['actions'] for a in ARMS883}, 'end': {a: eps[a]['end'] for a in ARMS883},
            'accepted': {a: eps[a]['accepted'] for a in ARMS883}, 'acq': {a: eps[a]['acquisitions'] for a in ARMS883},
            'steps': {a: eps[a]['n_steps'] for a in ARMS883}, 'seconds': {a: eps[a]['seconds'] for a in ARMS883},
            'cartridges': {a: len(eps[a]['cartridges']) for a in ARMS883},
            'integrity': {'pre_divergence_steps_bitwise': pre, 'pre_divergence_cartridges_bitwise': cards,
                          'same_start_bank_and_seal_all_arms': same_start, 'step1_state_equal_all_arms': step1},
            'Y': {a: None for a in ARMS883}}


def offline883(env, by_key, refs):
    # G5, after every live episode: the locked sealed evaluator. Nothing here is read by a runtime function.
    scores, fixture = {}, _c883.defaultdict(lambda: {'n': 0, 'success': 0, 'model_accept': 0, 'supported_accept': 0})
    for ep in STATE883['episodes']:
        spec = by_key[(ep['world_index'], ep['condition'])]
        row = {'end': ep['end'], 'accepted_candidate': ep['accepted'], 'final_mounted': ep['final_mounted']}
        scores[ep['episode_id']] = {'Y': int(bool(success867(env, row, spec))), 'end': ep['end'], 'accepted': ep['accepted']}
    for r in _j883.loads(_g883.decompress(RAW_SOURCES864['869_full_records.json.gz'])):   # all arms incl. K_SHAM (phase GATE4)
        if r.get('phase') not in ('PANEL', 'GATE4'): continue
        spec = by_key[(int(r['world_index']), r['condition'])]; s = fixture['%s|%s' % (r['arm'], r['condition'])]
        s['n'] += 1; s['success'] += int(bool(success867(env, r, spec))); s['model_accept'] += int(r['end'] == 'MODEL_ACCEPT')
        s['supported_accept'] += int(r['end'] == 'MODEL_ACCEPT' and bool(correct867(env, r, spec)))
    for key, cell in STATE883['cells'].items():
        for a in ARMS883:
            sc = scores.get('%s_%s_%s' % (a, cell['world'], cell['cond']))
            cell['Y'][a] = None if sc is None else sc['Y']
    out = {'episodes': scores, 'fixture_869_success_by_arm_condition': dict(fixture),
           'evaluator': 'locked success867 (MISSING: MODEL_STOP; else correct867 -> supported851)', 'after_all_live_work': True}
    STATE883['offline'] = out; json_write864('offline_scores.json', out)
    return out


def report883():
    print('=' * 112)
    print('TEST883 | GPU %s | head %s | cell %s | prereg %s' % (CC_GPU.get('name'), HEAD883[:12], STATE883['source'].get(
        'executed_cell_git_blob'), PREREG_SHA883[:16]))
    for g, v in STATE883['gates'].items(): print('GATE %-3s %-6s wall=%ss' % (g, v['status'], v['wall_s']))
    for k, b in STATE883['baseline'].items():
        print('G3 BASELINE %-12s %-28s live=%s fixture=%s end live/fixture=%s/%s' % (k, b['label'], '>'.join(b['live_actions']),
              '>'.join(b['fixture_actions'][:HORIZON883]), b['live_end'], b['fixture_end']))
    print('%-12s %-6s | %-34s | %-34s | %-34s | Y nofb/cb/vis | div' % ('cell', '', 'NOFB', 'CBLIND', 'VIS'))
    for k, c in STATE883['cells'].items():
        print('%-12s %-6s | %-34s | %-34s | %-34s | %s/%s/%s | %s' % (k, c['cond'][:6], '>'.join(x[:3] for x in c['actions']['NOFB'])[:34],
              '>'.join(x[:3] for x in c['actions']['CBLIND'])[:34], '>'.join(x[:3] for x in c['actions']['VIS'])[:34],
              c['Y']['NOFB'], c['Y']['CBLIND'], c['Y']['VIS'], c['first_divergent_step_VIS_vs_CBLIND']))
    off = STATE883.get('offline') or {}
    for k, v in sorted((off.get('fixture_869_success_by_arm_condition') or {}).items()):
        print('869 FIXTURE %-24s n=%2d success=%2d model_accept=%2d supported_accept=%2d' % (k, v['n'], v['success'], v['model_accept'],
                                                                                         v['supported_accept']))
    b = STATE883['budget']; ss = b['step_seconds']
    print('BUDGET adapter_ffe_lower_bound=%.1f %s TOTAL_GPU_WORK_NOT_FULLY_ACCOUNTED calls849=%s peak_alloc=%.2f GiB peak_reserved=%.2f '
          'GiB arm_s_per_step mean=%s max=%s' % (b['adapter_ffe_lower_bound'], _j883.dumps({k: round(v, 2) for k, v in b['ffe_by_kind'].items()}),
          env883['CALLS849'] if 'env883' in globals() else None, b['peak_alloc_gib'], b['peak_reserved_gib'],
          round(sum(ss) / len(ss), 1) if ss else None, max(ss) if ss else None))
    if STATE883['not_run']: print('NOT_RUN', STATE883['not_run'])
    r = STATE883['result'] or {'result': 'TECHNICAL_BLOCK', 'reason': 'no result'}
    print('TEST883 RESULT %s | %s | labels %s' % (r['result'], r.get('reason'), r.get('labels')))
    print('status %s | wall %.0f s | GPU_RUN_THIS_TEST if this console is from a Colab run; GPU_NOT_RUN_BY_AUTHOR (cell author)' % (
        STATE883['status'], time.perf_counter() - T_START883))
    print('=' * 112)


# ============================ single cell execution ============================
T_START878 = T_START883 = time.perf_counter()
try:
    STATE883['status'] = 'G0'; capture_source883()
    json_write864('TEST883_prereg.json', {'prereg': PREREG883, 'sha256': PREREG_SHA883, 'written_before_model_load': True})
    (ROOT864 / 'TEST883_prereg.json.sha256').write_text(sha256_bytes864((ROOT864 / 'TEST883_prereg.json').read_bytes()) +
                                                        '  TEST883_prereg.json\n', encoding='utf-8')
    load_sources865(); select_locked883(); run_selftests883()
    du = _s883.disk_usage(str(ROOT864))
    if du.free / 2**30 < 5.0: raise Gate883('DISK_FREE %.1f GiB' % (du.free / 2**30))
    source_audit878(); load878(); feasibility_audit864(); audit_contracts865(); load_spine864(); REFS883 = load_records870()
    WORLDS883 = select_worlds883()
    assert CC_GPU_OK and 'A100' in str(CC_GPU.get('name')) and CC_GPU.get('total_gib', 0) >= 78.0, ('A100_80GB_REQUIRED', CC_GPU)
    gate883('G0', 'PASS', worlds=WORLDS883, selftests=sorted(STATE883['selftests']), d0=STATE883['d0']['summary'],
            source={k: v for k, v in STATE883['source'].items() if k != 'reused'}, disk_free_gib=round(du.free / 2**30, 1))
    STATE883['status'] = 'G1'
    env883, original_error883, original_trace883, reproduction883 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace883; TWO_JOB_VERIFICATION864 = verify_two_job859(env883, original_trace883)
    assert_hook_free859(env883, 'T883_before_native'); install_offline_evaluator859(env883)
    native883 = native_sequences860(env883); NATIVE_REGRESSION864 = native_regression864(env883, native883)
    verify_864_reference865(NATIVE_REGRESSION864); ANALYSIS864 = run_analysis863(env883, native883)
    assert len(STATE863['restores']) == 3 and all(r_['exact'] for r_ in STATE863['restores'])
    digest883 = records_digest861(env883); null_seal883 = physical_seal863(env883, env883['MEMNULL841'])
    runtime_contracts865(env883); runtime_preflight865(env883, reproduction883); rearm_budget865(env883); make_slots866(env883)
    SLOTS867['PREV_EVALUATION'] = list(env883['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env883); resolve_append873(env883); api877(env883); WEIGHTS0_878 = weights_digest877(env883)
    chunk883 = [ns['CHUNK'] for ns in (env883['build_fusion'].__globals__, env883) if 'CHUNK' in ns]
    assert chunk883 and int(chunk883[0]) > 0 and all(k in env883 for k in (
        'P', 'to_gpu', 'entries', 'make_x851', 'gen851', 'gen849', 'C_SLOT851', 'E_SLOT851', 'REVIEW_SUFFIX851', 'stats849',
        'MUE845', 'MEMNULL841', 'relation852', 'R_SLOT852', 'QTEXT841', 'worlds829', 'node851', 'supported851')), 'ENGINE_NAMESPACE'
    EXP878['CHUNK'] = int(chunk883[0])
    vocab883 = sorted(w_ for w_, _ in ACTION_IDS867)
    assert vocab883 == ['ACCEPT', 'ACQUIRE', 'ADVANCE', 'BACKTRACK', 'REJECT', 'STOP'], ('NATIVE_VOCABULARY', vocab883)
    assert not any(p_.requires_grad for p_ in env883['model'].parameters()), 'NOT_FROZEN'
    hook883 = assert_hook_free859(env883, 'T883_before_points')
    if _o883.path.exists(CART_ROOT883): _s883.rmtree(CART_ROOT883)
    _o883.makedirs(CART_ROOT883); EXP_DIR878 = type(ROOT864)(CART_ROOT883)
    gate883('G1', 'PASS', api=STATE883.get('api'), vocabulary=vocab883, chunk=EXP878['CHUNK'], P=int(env883['P']),
            model_load_s=round(time.perf_counter() - T_START883), hook_free=True)
    by_key883 = build_specs869(env883)
    CELLS883 = [(w_, c_) for w_ in WORLDS883 for c_ in CONDITIONS883]
    STATE883['status'] = 'G2'; probe883 = None
    for w_, c_ in CELLS883:
        p_ = episode883(env883, by_key883[(int(w_), c_)], 'CBLIND', 'G2_PROBE_%s_%s' % (w_, c_), 2)
        if p_['n_steps'] == 2 and p_['first_read_done']: probe883 = p_; break
    if probe883 is None: gate883('G2', 'BLOCK', why='NO_CELL_REACHED_A_SECOND_DECISION_WITH_AN_EXPERIENCE (probe cannot test the read)')
    rd883 = probe883['steps'][1]['decision']
    gate883('G2', 'PASS', probe=probe883['episode_id'], cartridge=probe883['cartridges'][0], read=rd883,
            restore=probe883['exact_restore'], isolated=probe883['isolated_after_episode'], seconds=probe883['seconds'])
    STATE883['status'] = 'G3'
    for w_, c_ in CELLS883:
        spec_ = by_key883[(int(w_), c_)]
        ep_ = episode883(env883, spec_, 'NOFB', 'NOFB_%s_%s' % (w_, c_), HORIZON883)
        STATE883['baseline']['%s_%s' % (w_, c_)] = compare_fixture883(ep_, REFS883[(spec_['item'], 'NO_FEEDBACK')])
    gate883('G3', 'PASS', labels={k: v['label'] for k, v in STATE883['baseline'].items()},
            note='a DIVERGED label is recorded, not a block: the live NOFB baseline is used (pre-registered)')
    STATE883['status'] = 'G4'
    for i_, (w_, c_) in enumerate(CELLS883):
        ok_, proj_ = cell_admission883(time.perf_counter() - T_START883, STATE883['budget']['step_seconds'])
        if not ok_:
            STATE883['not_run'] += ['CELL_%s_%s: admission projected %.0f s > %.0f s' % (w2, c2, proj_, WALL_MIN883 * 60)
                                    for w2, c2 in CELLS883[i_:]]
            break
        eps_ = {'NOFB': next(e for e in STATE883['episodes'] if e['episode_id'] == 'NOFB_%s_%s' % (w_, c_))}
        for a_ in ('CBLIND', 'VIS'):
            eps_[a_] = episode883(env883, by_key883[(int(w_), c_)], a_, '%s_%s_%s' % (a_, w_, c_), HORIZON883)
        cell_ = assemble_cell883(w_, c_, eps_); STATE883['cells']['%s_%s' % (w_, c_)] = cell_
        if not all(cell_['integrity'].values()): raise Gate883('G4_CELL_INTEGRITY %s %s' % ((w_, c_), cell_['integrity']))
    gate883('G4', 'PASS', cells=sorted(STATE883['cells']), not_run=STATE883['not_run'])
    STATE883['status'] = 'G5'; offline883(env883, by_key883, REFS883)
    gate883('G5', 'PASS', episodes=len(STATE883['offline']['episodes']))
    if records_digest861(env883) != digest883 or physical_seal863(env883, env883['MEMNULL841']) != null_seal883 or \
            weights_digest877(env883) != WEIGHTS0_878 or hook_audit859(env883, 'T883_final')['hook_count']:
        raise Gate883('POST_RUN_INTEGRITY')
    STATE883['status'] = 'G6'
    STATE883['result'] = verdict883({k: v for k, v in STATE883['cells'].items()}, True)
    gate883('G6', 'PASS', result=STATE883['result']['result'])
    STATE883['status'] = 'COMPLETE'
except Budget883 as exc:
    STATE883['error'] = str(exc); STATE883['not_run'].append('BUDGET_STOP at %s: %s' % (STATE883['status'], exc))
    try:
        if 'by_key883' in globals() and STATE883['cells']:
            offline883(env883, by_key883, REFS883)
            STATE883['result'] = verdict883(STATE883['cells'], True)
            STATE883['result']['labels'].append('PARTIAL_BUDGET_STOP')
        else:
            STATE883['result'] = {'result': 'TECHNICAL_BLOCK', 'labels': ['BUDGET_STOP_BEFORE_ANY_CELL'], 'reason': str(exc)}
    except Exception as exc2:
        STATE883['result'] = {'result': 'TECHNICAL_BLOCK', 'labels': ['OFFLINE_AFTER_BUDGET_STOP_FAILED'], 'reason': str(exc2)}
    STATE883['status'] = 'BUDGET_STOP_AT_' + str(STATE883['status'])
except BaseException as exc:
    STATE883['error'] = '%s: %s' % (type(exc).__name__, exc); STATE883['traceback'] = traceback.format_exc()
    STATE883['result'] = {'result': 'TECHNICAL_BLOCK', 'labels': ['FAILED_AT_' + str(STATE883['status'])], 'reason': STATE883['error'][:400]}
    STATE883['gates'].setdefault(str(STATE883['status']), {'status': 'FAIL', 'error': STATE883['error'][:600]})
    STATE883['status'] = 'FAILED_AT_' + str(STATE883['status'])
    (ROOT864 / '883_traceback.txt').write_text(STATE883['traceback'], encoding='utf-8')
    print('TEST883 ERROR', STATE883['error'][:300], '| full traceback:', ROOT864 / '883_traceback.txt', file=ERROR_CONSOLE864, flush=True)
    print(STATE883['traceback'], file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        json_write864('gate_status.json', STATE883['gates'])
        json_write864('final_report.json', jsafe878({k: v for k, v in STATE883.items() if k != 'episodes'}) if 'jsafe878' in globals()
                      else _j883.loads(_j883.dumps({k: v for k, v in STATE883.items() if k != 'episodes'}, default=str)))
    except Exception as exc: print('RESULT_WRITE_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    try: report883()
    except Exception as exc: print('REPORT_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE883['suffix'], 'test870.py:suffix', 'exec'), globals())
