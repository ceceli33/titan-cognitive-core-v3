# AKBASCORE SILICON HIPPOCAMPUS — TEST883 R2 / F1 — PHYSICAL EXPERIENCE CARTRIDGE: INCREMENTAL CARTRIDGE-C CHANNEL (VIS vs C-BLIND)
# R2 = TEST883 (main c084ddaf, blob 24690c56) + fail-closed repairs C1-C8 and estimand wording D. Same engine, same locks,
# same arms, same worlds, same horizon. TEST883.py itself is not modified; this is a separate cell.
# One A100-SXM4-80GB Colab cell. Frozen Qwen2.5-72B-Instruct NF4, BF16 activations/KV, SDPA, 80 layers, H=8192.
# No router, no calibration, no thresholds, no STORE, no bank change, no forced action: every executed word is a native CAR
# reading, passed literally to the locked execute866; success is scored only after every live episode, by the locked
# success867 / supported851 evaluator, in a separate offline environment (oracle keys are removed from the live env).
# Estimand: the INCREMENTAL CARTRIDGE-C CHANNEL (C span of the latest experience readable vs unreadable), not total feedback.
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
ENGINE_BLOB883, MARKER883 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', 'AKBASCORE SILICON HIPPOCAMPUS — TEST883 R2 / F1'
HEAD883 = '3d75f289b88271440f4e3e13c2491699e6dc14ca'
FIXTURE_BLOB883, FIXTURE_SHA883 = 'f75a94ebbab8272878050579988cd35cb1deb822', 'daf5a8c4bd36811328a4ab173fe5cd300cc93c812558b883232e60ae42967f21'


def blob883(raw):
    return _h883.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def engine_parts883():
    with _u883.urlopen(_u883.Request(ENGINE_URL883, headers={'User-Agent': 'AKBASCORE-TEST883R2'}), timeout=240) as r:
        raw = r.read()
    assert blob883(raw) == ENGINE_BLOB883, ('ENGINE_BLOB_MISMATCH', blob883(raw))
    text = raw.decode('utf-8'); _a883.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST883R2_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST883R2_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST883R2_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('883r2_engine.log', '883r2_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST883R2_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '883r2_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '883r2_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST883R2_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old)
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL883, 'git_blob': blob883(raw), 'sha256': _h883.sha256(raw).hexdigest()}


try:
    ENGINE883, ENGINE_INFO883 = engine_parts883()
except BaseException as _exc883:
    import time as _t883, traceback as _tb883
    _p883 = '/content/TEST883R2_PRE_ENGINE_ERROR_%s.txt' % _t883.strftime('%Y%m%dT%H%M%SZ', _t883.gmtime())
    try:
        with open(_p883, 'w', encoding='utf-8') as _f883: _f883.write(_tb883.format_exc())
    except OSError: _p883 = 'NOT_WRITTEN'
    print('TEST883R2 PRE-ENGINE ERROR (before console capture):', type(_exc883).__name__, _exc883, '| traceback:', _p883)
    raise
exec(compile(ENGINE883['prefix'], 'test870.py:prefix', 'exec'), globals())
exec(compile(ENGINE883['body'], 'test870.py:engine', 'exec'), globals())
print('TEST883R2 ENGINE', _j883.dumps(ENGINE_INFO883, sort_keys=True))

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
EXEC_ALLOW883 = {'episode883': ('execute866', 'hop865', 'mount865'), 'cleanup883': ('mount865', 'free865'),
                 'model_contract883': ('output_hidden_states', 'output_attentions')}   # read-only config check (C8)
ORACLE883 = {'supported851', 'node851', 'world867', 'correct867', 'success867', 'worlds829', 'offline883', 'OFFLINE883',
             'score_fixture883', 'world_index_label', 'FIXTURE_SCORES883', 'ORACLE_VAULT883', 'offline_env883', 'OFFLINE867',
             'world_index_truth', 'offline_target', 'install_offline_evaluator859', 'offline_evaluate865', 'offline_evaluate866',
             'offline_evaluate867', 'correct866'}
ORACLE_ENV_KEYS883 = ('worlds829', 'node851', 'supported851')   # removed from the live env after build_specs869 (C6)
DYNAMIC883 = {'getattr', 'setattr', 'hasattr', 'delattr', 'exec', 'eval', 'compile', '__import__', 'globals', 'locals', 'vars',
              'importlib', '__dict__', '__globals__', '__builtins__'}
RUNTIME883 = ('episode883', 'write_experience883', 'read_with_experience883', 'prepare_experience883', 'reading_view883',
              'guard883', 'cell_admission883', 'event_contract883', 'causal_effect883', 'step1_parity883', 'cleanup883')
LIVE_ROOTS883 = ('hop865', 'feedback867', 'control_step867', 'execute866', 'mount865', 'free865', 'prefix_seals865',
                 'budget_left865', 'length873', 'car873', 'forward873', 'kv873', 'cache_kv870')
TERMINAL883 = ('ACCEPT', 'STOP', 'INVALID')                          # a terminal CONTROL has no EFFECT and is the last event
NATURAL_ENDS883 = ('MODEL_STOP', 'MODEL_ACCEPT', 'MODEL_INVALID_ACTION', 'HORIZON_6')
TECH_ENDS883 = ('NATIVE_EMPTY_OUTPUT', 'NATIVE_EMPTY_STATE', 'PHYSICAL_CONTEXT_LIMIT', 'RESOURCE_BUDGET', 'BUDGET_STOP',
                'TECHNICAL_BLOCK', 'EXECUTION_ERROR', 'INTERRUPTED', None)

# ============================ pre-registered design (fixed before the model is loaded) ============================
WORLD_POOL883 = ('03', '06', '07', '09', '10', '11')   # not 00/01 (TEST873-882 development), not 02/04/05/08 (TEST882 G3)
WORLD_SALT883, N_WORLDS883 = 'TEST883|F1|world|', 3   # rank by sha256(salt + world): outcome-free, fixed rule
CONDITIONS883 = ('MISSING', 'FORK')
ARMS883 = ('NOFB', 'CBLIND', 'VIS')                  # NOFB = live 869 NO_FEEDBACK baseline; CBLIND/VIS = F1 arms
HORIZON883 = 6
WALL_MIN883, FREE_MIN_GIB883, SAFETY883 = 75.0, 6.0, 1.25
WALL_S883, OFFLINE_RESERVE_S883 = WALL_MIN883 * 60.0, 180.0
CART_ROOT883 = '/content/TEST883R2_EPISODE_CARTRIDGES'  # outside ROOT864: isolated per episode, deleted after the episode
REQUIRED_WORLDS883 = ('10', '09', '03')              # = select_worlds883() (checked by a CPU selftest before the model)
REQUIRED_CELLS883 = tuple('%s_%s' % (w, c) for w in REQUIRED_WORLDS883 for c in CONDITIONS883)
PREREG883 = {
    'test': 'TEST883 R2 / F1 (name given by the user)', 'head': HEAD883, 'repairs_of': 'TEST883.py main c084ddaf blob 24690c56',
    'estimand': 'INCREMENTAL CARTRIDGE-C CHANNEL: the effect, on the next native CAR action and on the sealed task score, of making '
                'the C span of the latest physical experience cartridge E_{t-1}=[X2][A][C] readable (VIS) instead of unreadable '
                '(CBLIND), with B, X, X2, A, the cartridge tensors and the masked kernel identical. It is NOT the effect of '
                'feedback as a whole.',
    'claims_kept_separate': {
        'physical_influence': 'VIS vs CBLIND action divergence on identical inputs (measured)',
        'content_specificity': 'NOT_TESTED (needs correct vs swapped C: F1-lite plan, not in this cell)',
        'supported_utility': 'FORK supported success (sealed success867 / supported851) and MISSING non-harm (measured)',
        'persistent_learning': 'NOT_TESTED (STORE off, no bank mutation, no cross-episode memory)'},
    'non_equivalences': 'NOFB (content-free FV/FK rows, no cartridge), K_SHAM (869 fixture arm) and CBLIND (cartridge present, C '
                        'span masked) are different controls; none is used as a substitute for another',
    'memory_policy': {'STORE': 'OFF', 'only_latest': True, 'bank_mutation': 'NONE', 'cross_episode_learning': 'NOT_TESTED'},
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
                        'step_1': 'CBLIND and VIS: xcar878 on B with blind=() (no experience exists yet); it must equal the native '
                                  'car873 / control_step867 reading by same_reading881, otherwise TECHNICAL_BLOCK (no forcing)'},
    'experience': {'X2': 'the control X of step t (control prompt + action segments + review suffix), native forward on B_t',
                   'A': 'ACTION_IDS867 tokens of the executed native word',
                   'C': 'next model observation = hop and evidence rows produced at step t+1 on the environment memory',
                   'writer': 'locked write_exp878 (CUT3 lower K/V + h3) after bitwise lower / h3 next-layer gates',
                   'mount': 'locked load_exp878 (file + tensor SHA) + append_exp878 on B_{t+1}',
                   'only_latest': 'only E_{t-1} is mounted at decision t (explicit design, not truncation); earlier E stay on SSD '
                                  'unmounted with their SHA in cards_manifest',
                   'cardinality': 'cartridges per F1 episode == number of nonterminal CONTROL -> next CONTROL transitions '
                                  '(= n_steps - 1 for a natural end)',
                   'isolation': 'one directory per episode outside ROOT; deleted after the episode; never a bank card'},
    'event_contract': 'every nonterminal CONTROL is immediately followed by exactly one EFFECT with the same action; a terminal '
                      'CONTROL (ACCEPT / STOP / INVALID) has no EFFECT and is the last event; stale, duplicate, wrong-action, '
                      'orphan and missing EFFECTs are rejected; an episode without CONTROL is a technical endpoint, never success',
    'unaffected_by_arm': 'hop865, gen849 evidence, evaluation, legacy rollout and direction866 all run on B (no cartridge): '
                         'the arm changes nothing but the decision reading',
    'oracle_separation': 'after build_specs869 the keys %s are moved out of the live env into a sealed offline vault; every live '
                         'episode runs without them; scoring uses a separate offline env after all live work' % list(ORACLE_ENV_KEYS883),
    'worlds': 'first %d of %s ranked by sha256(%r + w)' % (N_WORLDS883, list(WORLD_POOL883), WORLD_SALT883),
    'required_cells': list(REQUIRED_CELLS883), 'conditions': CONDITIONS883, 'arms': ARMS883, 'horizon': HORIZON883,
    'endpoint': {'Y': 'success867 after all live work (MISSING: MODEL_STOP; FORK: supported851(accepted, world, mounted))',
                 'primary': 'per world x condition: Y_VIS - Y_CBLIND',
                 'PASS': 'only with the complete required matrix (6 cells x NOFB/CBLIND/VIS, every Y in {0,1}, natural ends, '
                         'actions, integrity) and no budget stop: FORK: Y_VIS=1 and Y_CBLIND=0 in >= 2 distinct worlds; no cell '
                         'with Y_VIS=0 and Y_CBLIND=1; MISSING: Y_VIS >= Y_NOFB in every world. The PASS label is only '
                         'C_F1_PILOT_POSITIVE',
                 'MISSING_role': 'a MISSING early STOP is only a non-harm check; it is never counted as a gain',
                 'NEGATIVE': 'complete matrix, PASS rule not met: A NO_DIVERGENCE / B SIGNAL_WITHOUT_BENEFIT / E '
                             'ACTION_EFFECT_WITHOUT_TASK_SUCCESS / DIVERGENCE_NOT_USEFUL',
                 'TECHNICAL_BLOCK': 'any integrity gate failure, any missing cell / arm / Y, any technical endpoint, any budget '
                                    'stop (INCOMPLETE_REQUIRED_MATRIX); status COMPLETE is separate from the scientific result'},
    'secondary': ['first divergent step', 'action sequences', 'STOP / ACQUIRE counts', 'steps', 'calls', 'seconds', 'GPU GiB',
                  'cartridges written', 'SSD bytes'],
    'gates': {'G0': 'sources, locks, A100, disk, prereg, CPU selftests (F1-F7 contracts), D0 causal-link re-audit, live-path '
                    'oracle scan of the locked engine',
              'G1': 'model load backbone of TEST882 (bitwise native regression, hook free), API presence, model contract (C8)',
              'G2': 'probe episode (first world, MISSING, CBLIND, 2 steps, excluded from analysis): write / reload / append parity, '
                    'B seal, zero-C bitwise invariance, trace == locked xcar878, step-1 parity',
              'G3': 'live NOFB baselines for every cell; prefix comparison with the 869 NO_FEEDBACK fixture (REPLAY_CONFIRMED or '
                    'DIVERGED; a divergence is recorded, not hidden, and the live baseline is used)',
              'G4': 'CBLIND then VIS for every admitted cell', 'G5': 'sealed offline scoring in a separate env',
              'G6': 'fail-closed decision matrix and report'},
    'budget': {'wall_s_hard': WALL_S883, 'free_vram_min_gib': FREE_MIN_GIB883, 'offline_reserve_s': OFFLINE_RESERVE_S883,
               'admission': 'before G3 and before every cell: elapsed + sum over ALL remaining episodes of (horizon x worst '
                            'measured s/step x %.2f + worst measured episode overhead) + offline reserve <= wall; an empty '
                            'measurement history is never admitted; a refused admission ends the run as INCOMPLETE '
                            '(TECHNICAL_BLOCK), a partial matrix never yields PASS' % SAFETY883,
               'never_cut_mid_episode': 'a budget trip inside an episode ends it as BUDGET_STOP, recorded, and stops the experiment',
               'measured_separately': ['wall s', 'peak alloc / reserved GiB', 'free GiB', 'calls849', 'SSD bytes', 'FFE by kind'],
               'ESTIMATED': 'load ~21 min (882 log: 1245 s); 869 V_X 9.1 s/step; experience write + mount + explicit read not measured'},
    'limits': ['3 worlds x 2 conditions: a pilot; two worlds is a mechanical minimum, not a statistic',
               'MISSING vs LIVE bank sizes (21 vs 23) are not part of this test: within a cell all arms share one bank (SHA checked)',
               'the C of E_t is also present in the current state segments (C/E slots): VIS vs C-BLIND isolates reading C inside '
               'the episode context, as in TEST881',
               'oracle separation covers the env keys and a static scan of the locked live path; closures captured by engine '
               'callables before the keys were removed are NOT_CHECKED']}
PREREG_SHA883 = sha256_bytes864(_j883.dumps(PREREG883, sort_keys=True).encode())
STATE883 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO883, 'prereg_sha256': PREREG_SHA883, 'source': {}, 'gates': {},
            'selftests': {}, 'd0': {}, 'g2': {}, 'baseline': {}, 'cells': {}, 'episodes': [], 'not_run': [], 'offline': None,
            'budget': {'adapter_ffe_lower_bound': 0.0, 'ffe_by_kind': {}, 'arms': {}, 'stages': {}, 'peak_alloc_gib': 0.0,
                       'peak_reserved_gib': 0.0, 'step_seconds': [], 'nofb_step_seconds': [], 'episode_overhead_s': [],
                       'ssd_bytes': 0, 'admissions': []},
            'model_contract': {}, 'oracle_separation': {}, 'live_scan': {}, 'cleanup_errors': [], 'result': None, 'error': None}
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
    # runtime functions: no oracle name / key, no dynamic attribute / code / namespace access, env / spec keys literal only (C6)
    names = {n.id for n in _a883.walk(node) if isinstance(n, _a883.Name)} | \
            {n.attr for n in _a883.walk(node) if isinstance(n, _a883.Attribute)}
    keys = {n.value for n in _a883.walk(node) if isinstance(n, _a883.Constant) and isinstance(n.value, str)}
    bad = sorted((names | keys) & ORACLE883)
    bad += sorted('DYNAMIC:' + x for x in names & DYNAMIC883)
    for s_ in _a883.walk(node):
        if isinstance(s_, _a883.Subscript) and isinstance(s_.value, _a883.Name) and s_.value.id in ('env', 'spec', 'env883') and \
                not (isinstance(s_.slice, _a883.Constant) and isinstance(s_.slice.value, str)):
            bad.append('DYNAMIC_KEY:%s[%s]' % (s_.value.id, _a883.unparse(s_.slice)[:40]))
        if isinstance(s_, _a883.keyword) and s_.arg is None and isinstance(s_.value, _a883.Name) and \
                s_.value.id in ('env', 'spec', 'env883'):
            bad.append('DYNAMIC_UNPACK:**%s' % s_.value.id)
    assert not bad, ('ORACLE_FIREWALL883', getattr(node, 'name', '?'), bad)


def live_path_scan883(sources):
    # static scan of the locked functions reached from the live roots (engine body + 873 + selected 878 / 881): no oracle key
    # or oracle function name. Calls made through env callables (gen849, make_x851 and the like) are not traced: NOT_CHECKED.
    funcs = {}
    for src in sources:
        for n in _a883.walk(_a883.parse(src)):
            if isinstance(n, _a883.FunctionDef): funcs.setdefault(n.name, n)
    seen, stack = set(), [r for r in LIVE_ROOTS883 + tuple(FUNCS878) + tuple(FUNCS881) if r in funcs]
    while stack:
        f = stack.pop()
        if f in seen or f not in funcs: continue
        seen.add(f)
        stack += [c.func.id for c in _a883.walk(funcs[f]) if isinstance(c, _a883.Call) and isinstance(c.func, _a883.Name)]
    hits = {}
    for f in sorted(seen):
        ns_ = {n.id for n in _a883.walk(funcs[f]) if isinstance(n, _a883.Name)} | \
              {n.value for n in _a883.walk(funcs[f]) if isinstance(n, _a883.Constant) and isinstance(n.value, str)}
        h = sorted(ns_ & (ORACLE883 | set(ORACLE_ENV_KEYS883)))
        if h: hits[f] = h
    missing = sorted(set(LIVE_ROOTS883) - seen)
    return {'functions_scanned': len(seen), 'oracle_hits': hits, 'roots_missing': missing,
            'not_traced': 'env callables (gen849, gen851, make_x851, embed841, cache_build and others)', 'ok': not hits and not missing}


def source_contract883(source):
    # F7: one complete cell, all parts, in order, no multi-cell / %run / shell escape; line count by splitlines
    lines = source.splitlines()
    bad = [i + 1 for i, l in enumerate(lines) if _r883.match(r'\s*(%%|%run|%load|!|# %%|#%%|In \[\d*\]:)', l)]
    once = lambda *frag: source.count(''.join(frag)) == 1       # patterns joined so this function never matches itself
    out = {'lines': len(lines), 'marker_once': once('MARKER', "883 = '") and source.count(MARKER883) >= 1,
           'magic_or_cell_separator_lines': bad[:10], 'episode_def_once': once('def ', 'episode883('),
           'offline_def_once': once('def ', 'offline883('), 'verdict_def_once': once('def ', 'verdict883('),
           'ends_with_engine_suffix': lines[-1].startswith('exec(compile(ENGINE' + "883['suffix']") if lines else False,
           'r2_marker': 'TEST883 R2 / F1' in source}
    out['ok'] = bool(out['marker_once'] and not bad and out['episode_def_once'] and out['offline_def_once'] and
                     out['verdict_def_once'] and out['ends_with_engine_suffix'] and out['r2_marker'])
    return out


def capture_source883():
    try:
        source, how = get_ipython().history_manager.input_hist_raw[-1], 'IPYTHON_CURRENT_CELL'
    except NameError:
        source = open(__file__, encoding='utf-8').read() if '__file__' in globals() else None; how = 'FILE_%RUN'
    assert source and MARKER883 in source and 'def episode883' in source and 'def offline883' in source, \
        'EXECUTED_883R2_SOURCE_NOT_CAPTURED (paste all three parts into ONE cell, in order)'
    sc = source_contract883(source)
    assert sc['ok'], ('SOURCE_CONTRACT883', sc)
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
    (ROOT864 / 'TEST883_R2.py').write_text(source, encoding='utf-8')
    STATE883['source'] = {'how': how, 'executed_cell_git_blob': git_blob864(source.encode()),
                          'executed_cell_sha256': sha256_bytes864(source.encode()), 'lines_splitlines': sc['lines'],
                          'source_contract': sc, 'firewall': 'PASS',
                          'oracle_firewall': 'PASS (%d runtime functions, dynamic escapes refused)' % len(RUNTIME883),
                          'single_executor_call': True, 'self_hash': 'NONE (measured at runtime only)'}
    json_write864('TEST883R2_source_manifest.json', dict(STATE883['source'], prereg_sha256=PREREG_SHA883, head=HEAD883,
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


def model_contract883(env, gpu):
    # C8: recorded and gated after the model load; no hook is installed, nothing is changed
    m = env['model']; cfg = m.config; mods = list(m.modules())
    lin4 = [x for x in mods if type(x).__name__ == 'Linear4bit']
    qc = getattr(cfg, 'quantization_config', None)
    qtype = (qc.get('bnb_4bit_quant_type') if isinstance(qc, dict) else getattr(qc, 'bnb_4bit_quant_type', None))
    if qtype is None and lin4:
        qs = getattr(lin4[0].weight, 'quant_state', None); qtype = getattr(qs, 'quant_type', None)
    kv = env['MEMNULL841'][0][0]
    hooks = sum(len(getattr(x, '_forward_hooks', {})) + len(getattr(x, '_forward_pre_hooks', {})) for x in mods)
    c = {'gpu_A100_80GB': 'A100' in str(gpu.get('name')) and float(gpu.get('total_gib', 0)) >= 78.0,
         'requires_grad_all_false': not any(p_.requires_grad for p_ in m.parameters()),
         'layers_80': int(getattr(cfg, 'num_hidden_layers', -1)) == 80, 'hidden_8192': int(getattr(cfg, 'hidden_size', -1)) == 8192,
         'linear4bit_present': len(lin4) > 0, 'nf4': str(qtype).lower() == 'nf4',
         'kv_bf16': str(getattr(kv, 'dtype', None)) == 'torch.bfloat16',
         'attn_sdpa': getattr(cfg, '_attn_implementation', None) == 'sdpa',
         'output_hidden_states_off': not bool(getattr(cfg, 'output_hidden_states', False)),
         'output_attentions_off': not bool(getattr(cfg, 'output_attentions', False)), 'no_forward_hooks': hooks == 0}
    info = {'gpu': gpu.get('name'), 'total_gib': gpu.get('total_gib'), 'linear4bit_modules': len(lin4), 'quant_type': qtype,
            'kv_dtype': str(getattr(kv, 'dtype', None)), 'attn_implementation': getattr(cfg, '_attn_implementation', None),
            'forward_hooks': hooks}
    return {'checks': c, 'info': info, 'ok': all(c.values())}


ffe881, guard881, line881 = ffe883, (lambda stage, need_gib=0.0: guard883(stage)), line883

# ============================ pure core (CPU-testable; no model, no labels) ============================
def select_worlds883():
    return sorted(WORLD_POOL883, key=lambda w: _h883.sha256((WORLD_SALT883 + w).encode()).hexdigest())[:N_WORLDS883]


def first_divergence883(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y: return i + 1
    return None if len(a) == len(b) else min(len(a), len(b)) + 1


def event_contract883(events):
    # C4 strict contract. pairs[ci] = index of the EFFECT caused by the CONTROL at ci (None for a terminal CONTROL)
    probs, pairs, last_control = [], {}, None
    for i, e in enumerate(events):
        t = e.get('type')
        if t == 'CONTROL':
            if last_control is not None and events[last_control].get('action') in TERMINAL883:
                probs.append(('CONTROL_AFTER_TERMINAL', i))
            last_control = i
            nxt = events[i + 1] if i + 1 < len(events) else None
            if e.get('action') in TERMINAL883:
                pairs[i] = None
                if nxt is not None: probs.append(('EVENT_AFTER_TERMINAL_CONTROL', i, nxt.get('type')))
            elif nxt is None or nxt.get('type') != 'EFFECT': probs.append(('MISSING_EFFECT', i))
            elif nxt.get('action') != e.get('action'): probs.append(('WRONG_ACTION_EFFECT', i, nxt.get('action')))
            else: pairs[i] = i + 1
        elif t == 'EFFECT':
            prev = events[i - 1] if i > 0 else None
            if prev is None or prev.get('type') != 'CONTROL': probs.append(('STALE_OR_DUPLICATE_EFFECT', i))
            elif prev.get('action') in TERMINAL883: probs.append(('EFFECT_AFTER_TERMINAL', i))
    n_control = sum(1 for e in events if e.get('type') == 'CONTROL')
    if n_control == 0: probs.append(('NO_CONTROL_NATIVE_EMPTY',))
    return {'ok': not probs, 'problems': probs, 'pairs': pairs, 'controls': n_control,
            'effects': sum(1 for e in events if e.get('type') == 'EFFECT')}


def causal_effect883(events, ci):
    # the EFFECT caused by the CONTROL at events[ci], under the strict contract of the whole record; None otherwise
    c = event_contract883(events)
    if not c['ok'] or events[ci].get('type') != 'CONTROL': return None
    j = c['pairs'].get(ci)
    return None if j is None else events[j]


def d0_causal883(records):
    # D0 re-audit with the strict causal link: the step-2 ACQUIRE effect must be caused by the step-2 CONTROL of the same record
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
                        'event_contract_ok': event_contract883(r['events'])['ok'],
                        'state': None if ci is None else cj(r['events'][ci]['record']['state_sha256']),
                        'mounted_before': None if ci is None else r['events'][ci]['mounted'],
                        'effect': None if eff is None else eff.get('effect'),
                        'query': None if eff is None else (eff.get('provenance') or {}).get('query_sha256'),
                        'chosen': None if eff is None else eff.get('chosen'),
                        'bank_size': None if eff is None else (eff.get('route') or {}).get('n_candidates')}
        m, l = row['M'], row['L']
        row['eligible'] = bool(m['event_contract_ok'] and l['event_contract_ok'] and
                               m['action'] == l['action'] == 'ACQUIRE' and m['state'] == l['state'] and m['state'] is not None
                               and m['effect'] == l['effect'] == 'MOUNTED' and m['query'] == l['query'] and m['query']
                               and m['mounted_before'] == l['mounted_before'] and m['chosen'] != l['chosen'])
        row['bank_sizes'] = [m['bank_size'], l['bank_size']]
        for tag in ('M', 'L'): row[tag].pop('state')
        out['%s|%02d' % (arm, w)] = row
    summary = _c883.Counter((v['arm'], v['eligible']) for v in out.values())
    return out, {a: {'eligible': summary[(a, True)], 'not_eligible': summary[(a, False)]} for a in sorted({v['arm'] for v in out.values()})}


def step1_parity883(reading, native):
    # C2: with no experience, the explicit xcar878(B, X, (), False) reading must equal the native reading; no forcing
    ok = bool(same_reading881(reading, native))
    if not ok: raise Gate883('STEP1_PARITY explicit=%s native=%s' % (reading.get('action'), native.get('action')))
    return ok


def cell_status883(cell):
    # one cell of the required matrix: every arm present, natural end, Y in {0, 1}, actions list, integrity all True
    why = []
    for a in ARMS883:
        y = (cell.get('Y') or {}).get(a, 'ABSENT'); end = (cell.get('end') or {}).get(a, 'ABSENT')
        if y not in (0, 1): why.append('Y_%s=%s' % (a, y))
        if end not in NATURAL_ENDS883: why.append('END_%s=%s' % (a, end))
        if not isinstance((cell.get('actions') or {}).get(a), list): why.append('ACTIONS_%s_ABSENT' % a)
        if (cell.get('contract') or {}).get(a) is not True: why.append('EVENT_CONTRACT_%s' % a)
    integ = cell.get('integrity')
    if not isinstance(integ, dict) or not integ or not all(v is True for v in integ.values()):
        why.append('INTEGRITY %s' % sorted(k for k, v in (integ or {}).items() if v is not True))
    return why


def verdict883(cells, required, integrity_ok, allow_pass, blocks=()):
    # C1 fail-closed: PASS / NEGATIVE only on the complete required matrix with allow_pass; everything else TECHNICAL_BLOCK
    incomplete = {k: ['CELL_ABSENT'] for k in required if k not in cells}
    incomplete.update({k: w for k, w in ((k, cell_status883(cells[k])) for k in required if k in cells) if w})
    extra = sorted(set(cells) - set(required))
    base = {'required_cells': list(required), 'incomplete': incomplete, 'unexpected_cells': extra}
    if not integrity_ok or blocks:
        return dict(base, result='TECHNICAL_BLOCK', labels=list(blocks) or ['INTEGRITY'], reason='integrity')
    if incomplete or extra or not required:
        return dict(base, result='TECHNICAL_BLOCK', labels=['INCOMPLETE_REQUIRED_MATRIX'],
                    reason='%d of %d required cells incomplete' % (len(incomplete), len(required)))
    if not allow_pass:
        return dict(base, result='TECHNICAL_BLOCK', labels=['INCOMPLETE_REQUIRED_MATRIX', 'PASS_NOT_ALLOWED'],
                    reason='allow_pass=False (budget stop or interrupted run)')
    done = {k: cells[k] for k in required}
    harms = sorted(k for k, c in done.items() if c['Y']['VIS'] == 0 and c['Y']['CBLIND'] == 1)
    fork_gain = sorted({c['world'] for c in done.values() if c['cond'] == 'FORK' and c['Y']['VIS'] == 1 and c['Y']['CBLIND'] == 0})
    miss = [c for c in done.values() if c['cond'] == 'MISSING']
    missing_ok = bool(miss) and all(c['Y']['VIS'] >= c['Y']['NOFB'] for c in miss)   # MISSING: non-harm only, never a gain
    diverged = sorted(k for k, c in done.items() if c['actions']['VIS'] != c['actions']['CBLIND'])
    labels = []
    if not diverged: labels.append('A_NO_DIVERGENCE')
    if diverged and (not missing_ok or any(c['acq']['VIS'] > c['acq']['NOFB'] for c in miss)):
        labels.append('B_SIGNAL_WITHOUT_BENEFIT')
    if any(c['end']['VIS'] != c['end']['CBLIND'] and c['Y']['VIS'] == c['Y']['CBLIND'] for c in done.values()):
        labels.append('E_ACTION_EFFECT_WITHOUT_TASK_SUCCESS')
    sci = {'fork_gain_worlds': fork_gain, 'harms': harms, 'diverged_cells': diverged, 'missing_not_worse_than_nofb': missing_ok}
    if len(fork_gain) >= 2 and not harms and missing_ok:
        return dict(base, **sci, result='PASS', labels=['C_F1_PILOT_POSITIVE'] + labels,
                    reason='FORK gain in %s, no harm, MISSING not worse than NOFB (incremental cartridge-C channel)' % fork_gain)
    if not labels: labels.append('DIVERGENCE_NOT_USEFUL')
    return dict(base, **sci, result='NEGATIVE', labels=labels,
                reason='fork_gain_worlds=%s (need >= 2), harms=%s, missing_ok=%s' % (fork_gain, harms, missing_ok))


def natural_end883(end, horizon=None):
    return end in NATURAL_ENDS883 or (isinstance(end, str) and end == 'HORIZON_%d' % (HORIZON883 if horizon is None else horizon))


def expected_cartridges883(n_steps, end, horizon=None):
    # C3 cardinality: one cartridge per nonterminal CONTROL followed by a next CONTROL. Steps 1..n-1 are nonterminal by
    # construction (a terminal ends the episode), so a natural end gives n_steps - 1; a native empty hop / state at step n+1
    # discards the pending experience of step n (no next CONTROL), also n_steps - 1. Any other end: undefined (None)
    ok = natural_end883(end, horizon) or end in ('NATIVE_EMPTY_OUTPUT', 'NATIVE_EMPTY_STATE')
    return max(int(n_steps) - 1, 0) if ok else None


def cartridge_core883(rec):
    keys = ('tensor_sha', 'pre_C_seal', 'body_tokens', 'C_span_body')
    return dict({k: rec.get(k) for k in keys}, **{'prov_' + k: (rec.get('provenance_core') or {}).get(k) for k in PROV_CORE883})


PROV_CORE883 = ('action', 'action_token_ids', 'X_sha256', 'source_prefix_tokens', 'C_rows_sha256', 'E_rows_sha256', 'step_written',
                'spans_body')


def compare_prefix883(cb, vi):
    # C3: d = first divergent step (1-based) of the executed actions, or None. Decision inputs of steps 1..u must be identical,
    # u = d if d else the common length (equal when no divergence); the decision at step t >= 2 reads E_{t-1} = cartridges[t-2],
    # so cartridges[0 .. u-2] (u-1 of them) must be identical. No zip truncation: a shorter list is a failure.
    d = first_divergence883(cb['actions'], vi['actions'])
    u = d if d else len(cb['actions'])
    if not d and len(cb['actions']) != len(vi['actions']): u = None
    out = {'d': d, 'inputs_upto': u, 'cards_upto': None if u is None else max(u - 1, 0)}
    if u is None: return dict(out, steps_ok=False, cards_ok=False, why='LENGTH_MISMATCH_WITHOUT_DIVERGENCE')
    if len(cb['steps']) < u or len(vi['steps']) < u: return dict(out, steps_ok=False, cards_ok=False, why='STEPS_SHORTER_THAN_PREFIX')
    fields = ('state_sha256', 'X_sha256', 'B_tokens', 'mounted_before', 'hop')
    out['steps_ok'] = all(_j883.dumps([a.get(f) for f in fields], sort_keys=True, default=str) ==
                          _j883.dumps([b.get(f) for f in fields], sort_keys=True, default=str)
                          for a, b in zip(cb['steps'][:u], vi['steps'][:u]))
    k = out['cards_upto']
    if len(cb['cartridges']) < k or len(vi['cartridges']) < k: return dict(out, cards_ok=False, why='CARTRIDGES_SHORTER_THAN_PREFIX')
    out['cards_compared'] = k
    out['cards_ok'] = all(cartridge_core883(x) == cartridge_core883(y) and x.get('tensor_sha') is not None
                          for x, y in zip(cb['cartridges'][:k], vi['cartridges'][:k]))
    return out


def cell_admission883(elapsed_s, step_seconds, overhead_s, remaining_episodes, horizon=None, reserve_s=None, wall_s=None):
    # C7 conservative: empty history is never admitted; every remaining episode is projected at the worst measured step
    horizon = HORIZON883 if horizon is None else horizon
    reserve_s = OFFLINE_RESERVE_S883 if reserve_s is None else reserve_s
    wall_s = WALL_S883 if wall_s is None else wall_s
    if not step_seconds: return False, None
    worst = max(step_seconds); over = max(overhead_s) if overhead_s else worst
    projected = elapsed_s + remaining_episodes * (horizon * worst * SAFETY883 + over) + reserve_s
    return projected <= wall_s, round(projected, 1)


# ============================ CPU selftests (before the model is loaded) ============================
def st_worlds883():
    w = select_worlds883()
    return {'three_worlds': len(w) == 3, 'rule_is_deterministic': w == select_worlds883(),
            'disjoint_from_882_calibration_and_development': not set(w) & {'00', '01', '02', '04', '05', '08'},
            'expected_from_prereg_rule': w == ['10', '09', '03'], 'required_worlds_equal_rule': list(REQUIRED_WORLDS883) == w,
            'required_cells_6': len(REQUIRED_CELLS883) == 6 and len(set(REQUIRED_CELLS883)) == 6}


def ev883(*spec):
    # tiny event builder for tests: 'H', 'C:ACQUIRE', 'E:ACQUIRE'
    out = []
    for x in spec:
        if x == 'H': out.append({'type': 'HOP'})
        else:
            t, a = x.split(':'); out.append({'type': 'CONTROL' if t == 'C' else 'EFFECT', 'action': a, 'effect': 'X_' + a})
    return out


def st_events883():
    # F2: strict event contract
    ok = lambda *x: event_contract883(ev883(*x))['ok']
    good = ok('H', 'C:ACQUIRE', 'E:ACQUIRE', 'H', 'C:ADVANCE', 'E:ADVANCE', 'H', 'C:STOP')
    return {'good_sequence_ok': good, 'horizon_end_without_terminal_ok': ok('H', 'C:ACQUIRE', 'E:ACQUIRE'),
            'missing_effect_refused': not ok('H', 'C:ACQUIRE', 'H', 'C:STOP'),
            'stale_effect_refused': not ok('H', 'C:ACQUIRE', 'E:ACQUIRE', 'H', 'E:ACQUIRE', 'C:STOP'),
            'duplicate_effect_refused': not ok('H', 'C:ACQUIRE', 'E:ACQUIRE', 'E:ACQUIRE'),
            'wrong_action_refused': not ok('H', 'C:ACQUIRE', 'E:ADVANCE'),
            'terminal_extra_effect_refused': not ok('H', 'C:STOP', 'E:STOP'),
            'event_after_terminal_refused': not ok('H', 'C:ACCEPT', 'H'),
            'control_after_terminal_refused': not ok('H', 'C:ACCEPT', 'C:ADVANCE', 'E:ADVANCE'),
            'effect_not_immediate_refused': not ok('H', 'C:ACQUIRE', 'H', 'E:ACQUIRE'),
            'empty_is_not_ok': not ok() and not ok('H'),
            'causal_effect_own': (causal_effect883(ev883('H', 'C:ACQUIRE', 'E:ACQUIRE'), 1) or {}).get('effect') == 'X_ACQUIRE',
            'causal_effect_none_when_record_broken': causal_effect883(ev883('H', 'C:ACQUIRE', 'E:ACQUIRE', 'E:ACQUIRE'), 1) is None,
            'causal_effect_terminal_none': causal_effect883(ev883('H', 'C:STOP'), 1) is None,
            'none_when_equal': first_divergence883(['ADVANCE', 'STOP'], ['ADVANCE', 'STOP']) is None,
            'first_index_1_based': first_divergence883(['ADVANCE', 'ACQUIRE'], ['ADVANCE', 'STOP']) == 2,
            'length_difference': first_divergence883(['ADVANCE'], ['ADVANCE', 'STOP']) == 2,
            'step_one': first_divergence883(['STOP'], ['ACQUIRE']) == 1}


def cell_t883(w, c, yv, yc, yn, av, ac, acq=(0, 0, 0), ev='MODEL_STOP', ec='MODEL_STOP', en='MODEL_STOP'):
    return {'world': w, 'cond': c, 'Y': {'VIS': yv, 'CBLIND': yc, 'NOFB': yn}, 'actions': {'VIS': av, 'CBLIND': ac, 'NOFB': ['STOP']},
            'acq': {'VIS': acq[0], 'CBLIND': acq[1], 'NOFB': acq[2]}, 'end': {'VIS': ev, 'CBLIND': ec, 'NOFB': en},
            'contract': {a: True for a in ARMS883}, 'integrity': {'x': True}}


def st_verdict883():
    # F1: fail-closed verdict over the 6 required cells
    same = ['ADVANCE', 'STOP']; R = REQUIRED_CELLS883
    base = {}
    for w in REQUIRED_WORLDS883:
        base[w + '_MISSING'] = cell_t883(w, 'MISSING', 1, 1, 1, same, same)
        base[w + '_FORK'] = cell_t883(w, 'FORK', 0, 0, 0, same, same)
    base['10_FORK'] = cell_t883('10', 'FORK', 1, 0, 0, ['ACCEPT'], ['ACQUIRE'], ev='MODEL_ACCEPT', ec='HORIZON_6')
    base['09_FORK'] = cell_t883('09', 'FORK', 1, 0, 0, ['ACCEPT'], ['ACQUIRE'], ev='MODEL_ACCEPT', ec='HORIZON_6')
    V = lambda cells, ok=True, ap=True: verdict883(cells, R, ok, ap)
    p = V(base)
    mod = lambda k, **kw: dict(base, **{k: dict(base[k], **kw)})
    no_cell = {k: v for k, v in base.items() if k != '03_MISSING'}
    no_arm = mod('03_FORK', Y={'VIS': 0, 'CBLIND': 0})
    none_y = mod('03_FORK', Y={'VIS': 0, 'CBLIND': None, 'NOFB': 0})
    tech = mod('03_FORK', end={'VIS': 'NATIVE_EMPTY_OUTPUT', 'CBLIND': 'MODEL_STOP', 'NOFB': 'MODEL_STOP'})
    budget_end = mod('03_FORK', end={'VIS': 'BUDGET_STOP', 'CBLIND': 'MODEL_STOP', 'NOFB': 'MODEL_STOP'})
    bad_int = mod('03_FORK', integrity={'x': False})
    bad_contract = mod('03_FORK', contract={'VIS': True, 'CBLIND': False, 'NOFB': True})
    harm = mod('03_FORK', Y={'VIS': 0, 'CBLIND': 1, 'NOFB': 0}, actions={'VIS': ['ACQUIRE'], 'CBLIND': ['ACCEPT'], 'NOFB': ['STOP']})
    one = mod('09_FORK', Y={'VIS': 0, 'CBLIND': 0, 'NOFB': 0}, actions={'VIS': same, 'CBLIND': same, 'NOFB': ['STOP']})
    miss = mod('10_MISSING', Y={'VIS': 0, 'CBLIND': 0, 'NOFB': 1}, actions={'VIS': ['ACQUIRE'] * 6, 'CBLIND': same, 'NOFB': ['STOP']},
               acq={'VIS': 6, 'CBLIND': 0, 'NOFB': 0}, end={'VIS': 'HORIZON_6', 'CBLIND': 'MODEL_STOP', 'NOFB': 'MODEL_STOP'})
    nodiv = {k: dict(v, Y={'VIS': 0, 'CBLIND': 0, 'NOFB': 0}, actions={'VIS': same, 'CBLIND': same, 'NOFB': same},
                     end={'VIS': 'MODEL_STOP', 'CBLIND': 'MODEL_STOP', 'NOFB': 'MODEL_STOP'}) for k, v in base.items()}
    extra = dict(base, **{'11_FORK': base['10_FORK']})
    tb = lambda r: r['result'] == 'TECHNICAL_BLOCK' and 'INCOMPLETE_REQUIRED_MATRIX' in r['labels']
    return {'pass_case': p['result'] == 'PASS' and p['fork_gain_worlds'] == ['09', '10'] and p['labels'][0] == 'C_F1_PILOT_POSITIVE',
            'missing_cell_blocks': tb(V(no_cell)), 'missing_arm_blocks': tb(V(no_arm)), 'none_Y_blocks': tb(V(none_y)),
            'technical_end_blocks': tb(V(tech)), 'budget_end_blocks': tb(V(budget_end)), 'cell_integrity_blocks': tb(V(bad_int)),
            'event_contract_blocks': tb(V(bad_contract)), 'unexpected_cell_blocks': tb(V(extra)),
            'allow_pass_false_blocks_even_complete_pass': tb(V(base, ap=False)) and V(base, ap=False)['result'] != 'PASS',
            'empty_matrix_blocks': tb(V({})), 'integrity_flag_blocks': V(base, ok=False)['result'] == 'TECHNICAL_BLOCK',
            'harm_is_negative': V(harm)['result'] == 'NEGATIVE', 'one_fork_gain_is_negative': V(one)['result'] == 'NEGATIVE',
            'missing_below_nofb_is_negative_B': V(miss)['result'] == 'NEGATIVE' and 'B_SIGNAL_WITHOUT_BENEFIT' in V(miss)['labels'],
            'no_divergence_is_A': V(nodiv)['labels'] == ['A_NO_DIVERGENCE'] and V(nodiv)['result'] == 'NEGATIVE',
            'missing_stop_never_a_gain': V(dict(nodiv, **{k: dict(nodiv[k], Y={'VIS': 1, 'CBLIND': 0, 'NOFB': 1})
                                                         for k in nodiv if k.endswith('MISSING')}))['result'] == 'NEGATIVE'}


def st_cartridge883():
    # F3: prefix definition, first-E comparison on a step-2 divergence, cardinality, no zip truncation
    card = lambda t, seal='s', step=1: {'tensor_sha': t, 'pre_C_seal': seal, 'body_tokens': 9, 'C_span_body': [4, 9],
                                         'provenance_core': {'action': 'ACQUIRE', 'step_written': step, 'X_sha256': 'x%d' % step}}
    stp = lambda i, s='S': {'state_sha256': s + str(i), 'X_sha256': 'X' + str(i), 'B_tokens': 100 + i, 'mounted_before': [], 'hop': 'h'}
    ep = lambda acts, cards, steps=None: {'actions': acts, 'cartridges': cards, 'steps': steps or [stp(i) for i in range(len(acts))]}
    a2 = compare_prefix883(ep(['ACQUIRE', 'STOP'], [card('T1')]), ep(['ACQUIRE', 'ACCEPT'], [card('T1')]))
    a2bad = compare_prefix883(ep(['ACQUIRE', 'STOP'], [card('T1')]), ep(['ACQUIRE', 'ACCEPT'], [card('T2')]))
    a2seal = compare_prefix883(ep(['ACQUIRE', 'STOP'], [card('T1')]), ep(['ACQUIRE', 'ACCEPT'], [card('T1', 'z')]))
    a2prov = compare_prefix883(ep(['ACQUIRE', 'STOP'], [card('T1')]), ep(['ACQUIRE', 'ACCEPT'], [card('T1', step=7)]))
    a2short = compare_prefix883(ep(['ACQUIRE', 'STOP'], [card('T1')]), ep(['ACQUIRE', 'ACCEPT'], []))
    d1 = compare_prefix883(ep(['STOP'], []), ep(['ACQUIRE', 'STOP'], [card('T1')]))
    d1state = compare_prefix883(ep(['STOP'], []), ep(['ACQUIRE', 'STOP'], [card('T1')], [stp(0, 'Q'), stp(1)]))
    nd = compare_prefix883(ep(['ACQUIRE', 'ADVANCE', 'STOP'], [card('T1'), card('T2', step=2)]),
                           ep(['ACQUIRE', 'ADVANCE', 'STOP'], [card('T1'), card('T2', step=2)]))
    nd_last = compare_prefix883(ep(['ACQUIRE', 'ADVANCE', 'STOP'], [card('T1'), card('T2', step=2)]),
                                ep(['ACQUIRE', 'ADVANCE', 'STOP'], [card('T1'), card('T3', step=2)]))
    stepshort = compare_prefix883(ep(['ACQUIRE', 'STOP'], [card('T1')], [stp(0)]), ep(['ACQUIRE', 'ACCEPT'], [card('T1')]))
    return {'step2_divergence_compares_first_E': a2['d'] == 2 and a2['cards_upto'] == 1 and a2['cards_ok'] and a2['steps_ok'],
            'step2_divergence_tensor_mismatch_fails': a2bad['cards_ok'] is False,
            'pre_C_seal_mismatch_fails': a2seal['cards_ok'] is False, 'provenance_mismatch_fails': a2prov['cards_ok'] is False,
            'missing_cartridge_fails_no_zip_truncation': a2short['cards_ok'] is False,
            'step1_divergence_empty_card_set_ok': d1['d'] == 1 and d1['cards_upto'] == 0 and d1['cards_ok'] and d1['steps_ok'],
            'step1_divergence_still_checks_step1_inputs': d1state['steps_ok'] is False,
            'no_divergence_compares_all_cards': nd['d'] is None and nd['cards_upto'] == 2 and nd['cards_ok'],
            'no_divergence_last_card_mismatch_fails': nd_last['cards_ok'] is False,
            'steps_shorter_than_prefix_fails': stepshort['steps_ok'] is False,
            'cardinality_natural': expected_cartridges883(3, 'MODEL_STOP') == 2 and expected_cartridges883(1, 'MODEL_ACCEPT') == 0
                                   and expected_cartridges883(6, 'HORIZON_6') == 5,
            'cardinality_native_empty_mid_episode': expected_cartridges883(3, 'NATIVE_EMPTY_OUTPUT') == 2,
            'cardinality_error_none': expected_cartridges883(2, 'EXECUTION_ERROR') is None,
            'probe_horizon_2_natural': expected_cartridges883(2, 'HORIZON_2', 2) == 1 and not natural_end883('HORIZON_2')}


def st_step1883():
    # F4: step-1 parity gate (uses the locked same_reading881 / same873 contract)
    r = {'action': 'ACQUIRE', 'argmax_word': 'ACQUIRE', 'abstain': False, 'mass': 0.9,
         'scores': [{'word': 'ACQUIRE', 'token_logps': [-0.1]}, {'word': 'STOP', 'token_logps': [-2.0]}]}
    other = dict(r, scores=[{'word': 'ACQUIRE', 'token_logps': [-0.1000001]}, {'word': 'STOP', 'token_logps': [-2.0]}])
    act = dict(r, action='STOP')
    def raises(a, b):
        try: step1_parity883(a, b); return False
        except Gate883: return True
    return {'equal_passes': step1_parity883(r, dict(r)) is True, 'logp_bit_difference_blocks': raises(other, r),
            'action_difference_blocks': raises(act, r), 'natural_terminal_step1_not_forced': step1_parity883(act, dict(act)) is True}


def st_firewall883():
    # F5: hook / executor / router / optimizer bans and the oracle + dynamic-escape firewall of runtime functions
    res = {}
    cases = {'executor_outside_episode': 'def f883(env):\n    execute866(env, 1, 2, 3, 4, 5)\n',
             'hook': 'def f883(m):\n    m.register_forward_hook(1)\n',
             'hidden_states_kw': 'def f883(m):\n    m(output_hidden_states=True)\n',
             'router_882': 'def f883(a):\n    return route882(a)\n', 'optimizer_step': 'def f883(o):\n    o.step()\n'}
    for k, src in cases.items():
        try: scan883(_a883.parse(src).body[0]); res[k + '_refused'] = False
        except AssertionError: res[k + '_refused'] = True
    oc = {'oracle_success': 'def f883(env, r, s):\n    return success867(env, r, s)\n',
          'oracle_supported': "def f883(env, a, w, m):\n    return env['supported851'](a, w, m)\n",
          'oracle_worlds': "def f883(env):\n    return env['worlds829']\n",
          'oracle_vault': 'def f883():\n    return ORACLE_VAULT883\n',
          'dynamic_getattr': "def f883(m, k):\n    return getattr(m, k)\n",
          'dynamic_exec': "def f883(s):\n    exec(s)\n", 'dynamic_eval': "def f883(s):\n    return eval(s)\n",
          'dynamic_import': "def f883(s):\n    return __import__(s)\n", 'dynamic_globals': "def f883():\n    return globals()['x']\n",
          'dynamic_locals': "def f883():\n    return locals()\n", 'dynamic_vars': "def f883(o):\n    return vars(o)\n",
          'dynamic_env_key': "def f883(env, k):\n    return env[k]\n", 'dynamic_spec_key': "def f883(spec, k):\n    return spec[k]\n",
          'dynamic_env_key_concat': "def f883(env):\n    return env['worlds' + '829']\n",
          'env_unpack': "def f883(env):\n    return dict(**env)\n",
          'dunder_globals': "def f883(f):\n    return f.__globals__\n"}
    for k, src in oc.items():
        try: oracle_scan883(_a883.parse(src).body[0]); res[k + '_refused'] = False
        except AssertionError: res[k + '_refused'] = True
    try:
        oracle_scan883(_a883.parse("def f883(env, spec, ctx, k):\n    return env['QTEXT841'][spec['qid']], ctx[k]\n").body[0])
        res['literal_keys_and_ctx_allowed'] = True
    except AssertionError: res['literal_keys_and_ctx_allowed'] = False
    try: scan883(_a883.parse('def f883(x):\n    step = x + 1\n    return step\n').body[0]); res['data_name_step_allowed'] = True
    except AssertionError: res['data_name_step_allowed'] = False
    v = {'worlds829': 1, 'node851': 2, 'supported851': 3, 'P': 4}
    vault = seal_oracle883(v)
    res['seal_removes_keys'] = not set(ORACLE_ENV_KEYS883) & set(v) and v == {'P': 4}
    res['offline_env_restores_keys'] = offline_env883(v, vault)['supported851'] == 3 and 'supported851' not in v
    try: seal_oracle883({'P': 4}); res['seal_requires_all_keys'] = False
    except Gate883: res['seal_requires_all_keys'] = True
    return res


def seal_oracle883(env):
    # C6: move the oracle keys out of the live env into a sealed vault (only offline883 ever sees them again)
    missing = [k for k in ORACLE_ENV_KEYS883 if k not in env]
    if missing: raise Gate883('ORACLE_KEYS_ABSENT %s' % missing)
    vault = {k: env.pop(k) for k in ORACLE_ENV_KEYS883}
    if set(ORACLE_ENV_KEYS883) & set(env): raise Gate883('ORACLE_KEYS_STILL_IN_LIVE_ENV')
    return vault


def offline_env883(env, vault):
    # separate offline env: a new dict (shallow), the live env stays without the oracle keys
    oenv = dict(env); oenv.update(vault)
    return oenv


def st_source883():
    # F7: source contract on synthetic sources (fragments are joined so this function's own text never matches the contract)
    m_, d_, x_ = 'MARKER' + "883 = ", 'def ' + 'episode883(', "exec(compile(ENGINE" + "883['suffix'], 'a', 'exec'))"
    ok_src = "%s'x', %r\n%s): pass\ndef %s(): pass\ndef %s(): pass\n%s" % (m_, MARKER883, d_, 'offline' + '883', 'verdict' + '883', x_)
    two = ok_src + "\n# " + "%%\n" + m_ + "'y'"
    run = "%" + "run other.py\n" + ok_src
    trunc = ok_src.rsplit('\n', 1)[0]
    dup = ok_src.replace('\n' + x_, '\n' + d_ + '): pass\n' + x_)
    shell = "!" + "pip install x\n" + ok_src
    c = source_contract883
    return {'complete_ok': c(ok_src)['ok'] and c(ok_src)['lines'] == len(ok_src.splitlines()),
            'multi_cell_refused': not c(two)['ok'], 'percent_run_refused': not c(run)['ok'], 'truncated_refused': not c(trunc)['ok'],
            'duplicate_def_refused': not c(dup)['ok'], 'shell_escape_refused': not c(shell)['ok'],
            'old_883_marker_refused': not c(ok_src.replace('TEST883 R2 / F1', 'TEST883 / F1'))['ok']}


def st_budget883():
    # C7 admission
    A = cell_admission883
    return {'empty_history_refused': A(0.0, [], [], 12)[0] is False,
            'fits': A(1000.0, [10.0], [20.0], 2, reserve_s=100.0, wall_s=4500.0)[0] is True,
            'all_remaining_projected': A(1000.0, [10.0], [20.0], 40, reserve_s=100.0, wall_s=4500.0)[0] is False,
            'worst_step_used': A(1000.0, [1.0, 60.0], [0.0], 8, reserve_s=0.0, wall_s=4500.0)[1] == 1000.0 + 8 * (6 * 60.0 * SAFETY883 + 0.0),
            'reserve_counted': A(4400.0, [1.0], [0.0], 0, reserve_s=180.0, wall_s=4500.0)[0] is False,
            'wall_is_4500': WALL_S883 == 4500.0}


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
    json_write864('TEST883R2_d0_causal.json', STATE883['d0'])
    nofb = summ.get('NO_FEEDBACK', {})
    pg = [r for r in recs if r['phase'] in ('PANEL', 'GATE4')]
    expect = {'NO_FEEDBACK': 10, 'V_X': 12, 'K_X': 12, 'KV_X': 12, 'NATIVE_FEEDBACK': 12, 'K_SHAM': 9}
    return {'records_295': len(recs) == 295, 'panel_gate4_288': len(pg) == 288,
            'unit_item_arm_phase_unique': max(units.values()) == 1,
            'strict_event_contract_all_295': all(event_contract883(r['events'])['ok'] for r in recs),
            'causal_link_checked_for_every_pair': all(v['M']['control_step2_index'] is not None for v in rows.values()),
            'no_feedback_pairs_counted': nofb.get('eligible', 0) + nofb.get('not_eligible', 0) == 12,
            'd0_eligible_counts_unchanged': {a: summ.get(a, {}).get('eligible') for a in expect} == expect,
            'bank_sizes_recorded': all(v['bank_sizes'][0] is not None for v in rows.values() if v['eligible'])}


def run_selftests883():
    tests = {'F1_verdict': st_verdict883, 'F2_events': st_events883, 'F3_cartridge': st_cartridge883, 'F4_step1': st_step1883,
             'F5_firewall': st_firewall883, 'F7_source': st_source883, 'worlds': st_worlds883, 'budget': st_budget883,
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
    json_write864('TEST883R2_cpu_selftest.json', {'results': out, 'failed': bad, 'prereg_sha256': PREREG_SHA883})
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
                'episode_prev_cartridge': meta.get('episode_prev_cartridge'),
                'provenance_core': {k: prov.get(k) for k in PROV_CORE883}})
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


def cleanup883(env, ctx, out, spec, arm, cdir, initial_seal, interrupted):
    # C5: always runs (also on KeyboardInterrupt / SystemExit); every failure is recorded, nothing is swallowed silently
    errs = []
    try:
        if ctx.get('memx') is not None: free865(env, ctx['memx'])
        ctx['memx'] = None
    except BaseException as exc: errs.append('FREE %s: %s' % (type(exc).__name__, exc))
    out['exact_restore_vs_first_mount'] = None
    if initial_seal is not None and not interrupted:
        rm = None
        try:
            rm, _ = mount865(env, spec['initial'], '883R2_LR_%s_%s' % (arm, spec['item']))
            out['exact_restore_vs_first_mount'] = prefix_seals865(env, rm) == initial_seal
        except BaseException as exc:
            out['exact_restore_vs_first_mount'] = False; errs.append('RESTORE %s: %s' % (type(exc).__name__, exc))
        finally:
            try:
                if rm is not None: free865(env, rm)
            except BaseException as exc: errs.append('FREE_RESTORE %s: %s' % (type(exc).__name__, exc))
    try:
        out['cartridges_deleted'] = sorted(_o883.listdir(cdir)) if _o883.path.isdir(cdir) else []
        if _o883.path.exists(cdir): _s883.rmtree(cdir)
    except BaseException as exc: errs.append('RMTREE %s: %s' % (type(exc).__name__, exc))
    out['isolated_after_episode'] = not _o883.path.exists(cdir)
    try: gc.collect(); torch.cuda.empty_cache()
    except BaseException as exc: errs.append('EMPTY_CACHE %s: %s' % (type(exc).__name__, exc))
    out['cleanup_errors'] = errs
    if errs: STATE883['cleanup_errors'].append({'episode_id': out.get('episode_id'), 'errors': errs})
    return errs


def episode883(env, spec, arm, ep_id, horizon):
    key = {'world_index': int(spec['world_index']), 'condition': spec['condition'], 'arm': arm, 'episode_id': ep_id}
    ctx = {'spec': spec, 'arm': 'NO_FEEDBACK', 'M': list(spec['initial']), 'memx': None, 'path': [], 'prev_state': None,
           'own_states': [], 'events': [], 'mount_records': [], 'acquisitions': 0, 'rejections': 0, 'addresses': 0,
           'steps': 0, 'hops': 0, 'donor_item': None}
    cdir = _o883.path.join(CART_ROOT883, ep_id)
    out = dict(key, item=spec['item'], steps=[], end=None, accepted=None, error=None, cartridges=[], first_read_done=False,
               step1_parity=None)
    E, last_entry, prev_hop, t0, calls0 = None, None, None, time.perf_counter(), int(env['CALLS849'])
    ffe0, initial_seal, interrupted, pending, step_sum = STATE883['budget']['adapter_ffe_lower_bound'], None, None, None, 0.0
    try:
        try:
            _o883.makedirs(cdir, exist_ok=False)
            q = env['QTEXT841'][spec['qid']]; pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
            ctx['memx'], mount = mount865(env, ctx['M'], '883R2_L0_%s_%s' % (arm, spec['item'])); ctx['mount_records'].append(mount)
            initial_seal = prefix_seals865(env, ctx['memx'])
            out['start'] = {'bank_sha256': sha256_bytes864(_j883.dumps(sorted((c, env['entries'][c]['sha256']) for c in spec['pool'])).encode()),
                            'bank_size': len(spec['pool']), 'initial': list(spec['initial']), 'initial_seal': initial_seal,
                            'memory_tokens': length873(env, ctx['memx']), 'cartridge_dir_empty': not _o883.listdir(cdir)}
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
                          state_sha256=record['state_sha256'], X_sha256=tsha881(X), B_tokens=length873(env, B),
                          mounted_before=list(ctx['M']), feedback=fb_info['source'], nofb_reading=reading_view883(record['reading']),
                          legacy=record['legacy_action'])
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
                        out['cartridges'].append(wrec); st['experience_written'] = wrec['id']; pending = None
                    if last_entry is None:
                        reading = xcar878(env, B, X, (), False); ffe883(int(X.shape[0]) + cont_tokens881(), 80, 'decision_read')
                        out['step1_parity'] = step1_parity883(reading, record['reading'])   # Gate883 on any difference (C2)
                        st['decision'] = {'memory': 'B (no experience yet)', 'path': 'xcar878 blind=()', 'step1_parity': True}
                    else:
                        reading, rrec = read_with_experience883(env, B, last_entry, X, arm, not out['first_read_done'])
                        out['first_read_done'] = True
                        st['decision'] = dict(rrec, memory='[B][E_t-1]', path='xcar878 blind=[C] sham=%s' % (arm == 'VIS'))
                action = reading['action']
                st.update({'reading': reading_view883(reading), 'action': action, 'decision_source': 'MODEL_CAR_READING_ON_ARM_MEMORY',
                           'differs_from_nofb_reading': action != record['action']})
                ctx['events'].append({'type': 'CONTROL', 'k': k, 'step': ctx['steps'], 'action': action, 'decision_source': 'MODEL',
                                      'mounted': list(ctx['M']), 'state_sha256': record['state_sha256'], 'f1_arm': arm})
                terminal = action in TERMINAL883
                if arm != 'NOFB' and not terminal: pending = prepare_experience883(env, cache, B, X, action)
                del cache
                if action == 'INVALID': out['end'] = 'MODEL_INVALID_ACTION'
                elif action == 'ACCEPT': out['end'], out['accepted'] = 'MODEL_ACCEPT', h['text'].strip()
                elif action == 'STOP': out['end'] = 'MODEL_STOP'
                else:
                    ctx['prev_state'] = state['own_state']; n_ev = len(ctx['events'])
                    execute866(env, ctx, action, h, control, state)
                    eff = ctx['events'][-1]
                    st['effect'] = {x: eff.get(x) for x in ('action', 'effect', 'chosen', 'mounted_before', 'mounted_after', 'path_after',
                                                           'direction_text', 'address_origin')}
                    st['effect']['route'] = eff.get('route'); st['effect']['query_sha256'] = (eff.get('provenance') or {}).get('query_sha256')
                    if eff.get('mount'): st['effect']['n_exact'] = eff['mount'].get('n_exact')
                    st['effect']['one_event_appended'] = len(ctx['events']) == n_ev + 1
                    st['effect']['executed_equals_reading'] = bool(eff.get('type') == 'EFFECT' and eff.get('action') == action and
                                                                   st['effect']['one_event_appended'])
                    if not st['effect']['executed_equals_reading']: raise Gate883('EFFECT_CONTRACT at %s t%d' % (ep_id, ctx['steps']))
                st['seconds'] = round(time.perf_counter() - ts, 3); st['calls'] = int(env['CALLS849']) - calls0; step_sum += st['seconds']
                out['steps'].append(st)
                with open(ROOT864 / 'decisions.jsonl', 'a', encoding='utf-8') as f: f.write(_j883.dumps(jsafe878(st), sort_keys=True) + '\n')
                top3 = sorted(reading['normalized'].items(), key=lambda kv: -kv[1])[:3]
                line883('STEP', ep_id, 't=%d' % ctx['steps'], 'hop=%r' % h['text'], 'CAR=' + '|'.join('%s:%.3f' % (w, p) for w, p in top3),
                        'exec=%s' % action, 'nofb=%s' % record['action'], 'effect=%s' % (st.get('effect') or {}).get('effect'),
                        's=%.1f' % st['seconds'])
                STATE883['budget']['nofb_step_seconds' if arm == 'NOFB' else 'step_seconds'].append(st['seconds'])
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
        except BaseException as exc:   # KeyboardInterrupt / SystemExit: clean up, record, re-raise (never a PASS)
            out['end'], out['error'], interrupted = 'INTERRUPTED', '%s: %s' % (type(exc).__name__, exc), exc
    finally:
        pending = None
        cleanup883(env, ctx, out, spec, arm, cdir, initial_seal, interrupted is not None)
    contract = event_contract883(ctx['events'])
    effects = [e for e in ctx['events'] if e['type'] == 'EFFECT']; controls = [e for e in ctx['events'] if e['type'] == 'CONTROL']
    exp_cards = expected_cartridges883(ctx['steps'], out['end'], horizon) if arm != 'NOFB' else 0
    out.update({'final_mounted': list(ctx['M']), 'path': [p['text'] for p in ctx['path']], 'n_steps': ctx['steps'],
                'actions': [c['action'] for c in controls], 'effects': [e['effect'] for e in effects], 'acquisitions': ctx['acquisitions'],
                'event_contract': {k: contract[k] for k in ('ok', 'problems', 'controls', 'effects')},
                'executed_equals_reading': bool(contract['ok'] and [c['action'] for c in controls] == [s_['action'] for s_ in out['steps']]),
                'technical_endpoint': not natural_end883(out['end'], horizon),
                'cartridges_expected': exp_cards, 'cartridge_cardinality_ok': exp_cards is not None and len(out['cartridges']) == exp_cards,
                'mount_integrity': bool(ctx['mount_records']) and all(m['n_exact'] and m['all_80_layers'] and m['finite'] and
                                                                      m['prior_prefix_exact'] is not False for m in ctx['mount_records'])})
    out['seconds'] = round(time.perf_counter() - t0, 1); out['calls'] = int(env['CALLS849']) - calls0
    out['overhead_s'] = round(out['seconds'] - step_sum, 1); out['ssd_bytes'] = sum(int(c.get('bytes') or 0) for c in out['cartridges'])
    out['ffe'] = round(STATE883['budget']['adapter_ffe_lower_bound'] - ffe0, 2)
    try: out['free_gib_after'] = round(free_gib881(), 2)
    except BaseException as exc: out['free_gib_after'] = None; out['cleanup_errors'].append('FREE_GIB %s' % type(exc).__name__)
    STATE883['budget']['episode_overhead_s'].append(out['overhead_s']); STATE883['budget']['ssd_bytes'] += out['ssd_bytes']
    line883('EPISODE', ep_id, 'end=%s' % out['end'], 'actions=%s' % '>'.join(out['actions']), 'accepted=%r' % out['accepted'],
            'cards=%d/%s' % (len(out['cartridges']), exp_cards), 'restore=%s' % out['exact_restore_vs_first_mount'],
            'contract=%s' % contract['ok'], 's=%.0f' % out['seconds'], '' if not out['error'] else 'ERROR=' + str(out['error'])[:300])
    if out.get('traceback'): short864(out['traceback'])
    rec = {k: v for k, v in out.items() if k != 'steps'}
    with open(ROOT864 / 'episodes.jsonl', 'a', encoding='utf-8') as f: f.write(_j883.dumps(jsafe878(rec), sort_keys=True) + '\n')
    STATE883['episodes'].append(out)
    if interrupted is not None: raise interrupted
    if out['end'] in ('BUDGET_STOP', 'RESOURCE_BUDGET'): raise Budget883(out['error'] or out['end'])
    natural_empty = out['end'] in ('NATIVE_EMPTY_OUTPUT', 'NATIVE_EMPTY_STATE') and not controls
    bad = {'end': out['end'] in ('TECHNICAL_BLOCK', 'EXECUTION_ERROR', 'PHYSICAL_CONTEXT_LIMIT'),
           'restore': out['exact_restore_vs_first_mount'] is not True, 'mount': not out['mount_integrity'],
           'contract': not (out['executed_equals_reading'] or natural_empty), 'isolated': not out['isolated_after_episode'],
           'cleanup': bool(out['cleanup_errors']), 'cardinality': not (out['cartridge_cardinality_ok'] or natural_empty),
           'step1_parity': arm != 'NOFB' and out['n_steps'] > 0 and out['step1_parity'] is not True}
    if any(bad.values()):
        raise Gate883('EPISODE_INTEGRITY %s %s err=%s' % (ep_id, sorted(k for k, v in bad.items() if v), str(out['error'])[:300]))
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
    cmp_ = compare_prefix883(cb, vi)
    same_start = all('start' in e for e in (nb, cb, vi)) and len({_j883.dumps(e['start'], sort_keys=True) for e in (nb, cb, vi)}) == 1
    step1 = bool(nb['steps'] and cb['steps'] and vi['steps']) and nb['steps'][0]['state_sha256'] == cb['steps'][0]['state_sha256'] == \
        vi['steps'][0]['state_sha256'] and nb['steps'][0]['X_sha256'] == cb['steps'][0]['X_sha256'] == vi['steps'][0]['X_sha256']
    technical = any(eps[a]['technical_endpoint'] for a in ARMS883)
    return {'world': w, 'cond': c, 'first_divergent_step_VIS_vs_CBLIND': cmp_['d'],
            'first_divergent_step_VIS_vs_NOFB': first_divergence883(nb['actions'], vi['actions']), 'prefix': cmp_,
            'actions': {a: eps[a]['actions'] for a in ARMS883}, 'end': {a: eps[a]['end'] for a in ARMS883},
            'accepted': {a: eps[a]['accepted'] for a in ARMS883}, 'acq': {a: eps[a]['acquisitions'] for a in ARMS883},
            'steps': {a: eps[a]['n_steps'] for a in ARMS883}, 'seconds': {a: eps[a]['seconds'] for a in ARMS883},
            'cartridges': {a: len(eps[a]['cartridges']) for a in ARMS883},
            'contract': {a: eps[a]['event_contract']['ok'] for a in ARMS883}, 'technical_endpoint': technical,
            'integrity': {'pre_divergence_steps_bitwise': cmp_['steps_ok'] is True, 'pre_divergence_cartridges_bitwise': cmp_['cards_ok'] is True,
                          'same_start_bank_and_seal_all_arms': same_start, 'step1_state_and_X_equal_all_arms': step1,
                          'cartridge_cardinality_all_arms': all(eps[a]['cartridge_cardinality_ok'] for a in ARMS883),
                          'step1_parity_F1_arms': all(eps[a]['step1_parity'] is True for a in ('CBLIND', 'VIS')),
                          'executed_equals_reading_all_arms': all(eps[a]['executed_equals_reading'] for a in ARMS883),
                          'exact_restore_all_arms': all(eps[a]['exact_restore_vs_first_mount'] is True for a in ARMS883)},
            'Y': {a: None for a in ARMS883}}


def offline883(oenv, by_key):
    # G5, after every live work, in the separate offline env (oracle keys restored only there). No runtime function reads it.
    scores, fixture = {}, _c883.defaultdict(lambda: {'n': 0, 'success': 0, 'model_accept': 0, 'supported_accept': 0})
    for ep in STATE883['episodes']:
        if ep['episode_id'].startswith('G2_PROBE'): continue
        spec = by_key[(ep['world_index'], ep['condition'])]
        row = {'end': ep['end'], 'accepted_candidate': ep['accepted'], 'final_mounted': ep['final_mounted']}
        y = int(bool(success867(oenv, row, spec))) if natural_end883(ep['end']) else None   # technical end: never success
        scores[ep['episode_id']] = {'Y': y, 'end': ep['end'], 'accepted': ep['accepted']}
    for r in _j883.loads(_g883.decompress(RAW_SOURCES864['869_full_records.json.gz'])):   # all arms incl. K_SHAM (phase GATE4)
        if r.get('phase') not in ('PANEL', 'GATE4'): continue
        spec = by_key[(int(r['world_index']), r['condition'])]; s = fixture['%s|%s' % (r['arm'], r['condition'])]
        s['n'] += 1; s['success'] += int(bool(success867(oenv, r, spec))); s['model_accept'] += int(r['end'] == 'MODEL_ACCEPT')
        s['supported_accept'] += int(r['end'] == 'MODEL_ACCEPT' and bool(correct867(oenv, r, spec)))
    for key, cell in STATE883['cells'].items():
        for a in ARMS883:
            sc = scores.get('%s_%s_%s' % (a, cell['world'], cell['cond']))
            cell['Y'][a] = None if sc is None else sc['Y']
    out = {'episodes': scores, 'fixture_869_success_by_arm_condition': dict(fixture),
           'evaluator': 'locked success867 (MISSING: MODEL_STOP; else correct867 -> supported851), separate offline env',
           'after_all_live_work': True, 'live_env_has_oracle_keys': bool(set(ORACLE_ENV_KEYS883) & set(env883))}
    STATE883['offline'] = out; json_write864('offline_scores.json', out)
    return out


def admit883(stage, remaining_episodes):
    b = STATE883['budget']
    ok, proj = cell_admission883(time.perf_counter() - T_START883, b['step_seconds'] + b['nofb_step_seconds'], b['episode_overhead_s'],
                                 remaining_episodes)
    b['admissions'].append({'stage': stage, 'remaining_episodes': remaining_episodes, 'projected_s': proj, 'admitted': ok,
                            'worst_step_s': max(b['step_seconds'] + b['nofb_step_seconds']) if b['step_seconds'] else None})
    if not ok:
        raise Budget883('ADMISSION_REFUSED %s: projected %s s for %d remaining episodes > %.0f s (history %d steps)' % (
            stage, proj, remaining_episodes, WALL_S883, len(b['step_seconds'])))


def report883():
    print('=' * 112)
    print('TEST883R2 | GPU %s | head %s | cell %s | prereg %s' % (CC_GPU.get('name'), HEAD883[:12], STATE883['source'].get(
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
    print('BUDGET ssd_bytes=%s admissions=%s cleanup_errors=%s' % (b['ssd_bytes'], _j883.dumps(b['admissions'])[:600],
                                                                   len(STATE883['cleanup_errors'])))
    if STATE883['model_contract']: print('MODEL_CONTRACT', _j883.dumps(STATE883['model_contract'], default=str)[:700])
    if STATE883['not_run']: print('NOT_RUN', STATE883['not_run'])
    r = STATE883['result'] or {'result': 'TECHNICAL_BLOCK', 'reason': 'no result'}
    if r.get('incomplete'): print('INCOMPLETE_CELLS', _j883.dumps(r['incomplete'])[:900])
    print('ESTIMAND incremental cartridge-C channel (VIS vs CBLIND) | content specificity NOT_TESTED | persistent learning NOT_TESTED')
    print('TEST883R2 RESULT %s | %s | labels %s' % (r['result'], r.get('reason'), r.get('labels')))
    print('status %s (run status, separate from the scientific result) | wall %.0f s | GPU_RUN_THIS_TEST if this console is from a '
          'Colab run; GPU_NOT_RUN_BY_AUTHOR (cell author)' % (STATE883['status'], time.perf_counter() - T_START883))
    print('=' * 112)


# ============================ single cell execution ============================
T_START878 = T_START883 = time.perf_counter()
ORACLE_VAULT883 = None
try:
    STATE883['status'] = 'G0'; capture_source883()
    json_write864('TEST883R2_prereg.json', {'prereg': PREREG883, 'sha256': PREREG_SHA883, 'written_before_model_load': True})
    (ROOT864 / 'TEST883R2_prereg.json.sha256').write_text(sha256_bytes864((ROOT864 / 'TEST883R2_prereg.json').read_bytes()) +
                                                          '  TEST883R2_prereg.json\n', encoding='utf-8')
    load_sources865(); select_locked883()
    du = _s883.disk_usage(str(ROOT864))
    if du.free / 2**30 < 5.0: raise Gate883('DISK_FREE %.1f GiB' % (du.free / 2**30))
    source_audit878(); load878(); run_selftests883()
    STATE883['live_scan'] = live_path_scan883([ENGINE883['body']] + [RAW_SOURCES864[n].decode() for n in ('873.py', '878.py', '881.py')])
    if not STATE883['live_scan']['ok']: raise Gate883('LIVE_PATH_ORACLE_SCAN %s' % STATE883['live_scan'])
    feasibility_audit864(); audit_contracts865(); load_spine864(); REFS883 = load_records870()
    WORLDS883 = select_worlds883()
    assert WORLDS883 == list(REQUIRED_WORLDS883), ('WORLDS_RULE', WORLDS883)
    assert CC_GPU_OK and 'A100' in str(CC_GPU.get('name')) and CC_GPU.get('total_gib', 0) >= 78.0, ('A100_80GB_REQUIRED', CC_GPU)
    gate883('G0', 'PASS', worlds=WORLDS883, selftests=sorted(STATE883['selftests']), d0=STATE883['d0']['summary'],
            live_scan={k: v for k, v in STATE883['live_scan'].items() if k != 'not_traced'},
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
        'MUE845', 'MEMNULL841', 'relation852', 'R_SLOT852', 'QTEXT841') + ORACLE_ENV_KEYS883), 'ENGINE_NAMESPACE'
    EXP878['CHUNK'] = int(chunk883[0])
    vocab883 = sorted(w_ for w_, _ in ACTION_IDS867)
    assert vocab883 == ['ACCEPT', 'ACQUIRE', 'ADVANCE', 'BACKTRACK', 'REJECT', 'STOP'], ('NATIVE_VOCABULARY', vocab883)
    assert not any(p_.requires_grad for p_ in env883['model'].parameters()), 'NOT_FROZEN'
    hook883 = assert_hook_free859(env883, 'T883_before_points')
    STATE883['model_contract'] = model_contract883(env883, CC_GPU); STATE883['model_contract']['physical_seal_MEMNULL'] = null_seal883
    if not STATE883['model_contract']['ok']: gate883('G1', 'BLOCK', model_contract=STATE883['model_contract'])
    if _o883.path.exists(CART_ROOT883): _s883.rmtree(CART_ROOT883)
    _o883.makedirs(CART_ROOT883); EXP_DIR878 = type(ROOT864)(CART_ROOT883)
    gate883('G1', 'PASS', api=STATE883.get('api'), vocabulary=vocab883, chunk=EXP878['CHUNK'], P=int(env883['P']),
            model_load_s=round(time.perf_counter() - T_START883), hook_free=True, model_contract=STATE883['model_contract']['checks'])
    by_key883 = build_specs869(env883)
    CELLS883 = [(w_, c_) for w_ in WORLDS883 for c_ in CONDITIONS883]
    assert ['%s_%s' % x for x in CELLS883] == list(REQUIRED_CELLS883), 'REQUIRED_CELLS'
    ORACLE_VAULT883 = seal_oracle883(env883)                      # C6: live work from here on runs without the oracle keys
    STATE883['oracle_separation'] = {'removed_keys': sorted(ORACLE_VAULT883), 'live_env_has_none': not set(ORACLE_ENV_KEYS883) & set(env883),
                                     'after': 'build_specs869', 'restored_only_in': 'offline_env883 (G5)'}
    STATE883['status'] = 'G2'; probe883 = None
    for w_, c_ in CELLS883:
        p_ = episode883(env883, by_key883[(int(w_), c_)], 'CBLIND', 'G2_PROBE_%s_%s' % (w_, c_), 2)
        if p_['n_steps'] == 2 and p_['first_read_done']: probe883 = p_; break
    if probe883 is None: gate883('G2', 'BLOCK', why='NO_CELL_REACHED_A_SECOND_DECISION_WITH_AN_EXPERIENCE (probe cannot test the read)')
    rd883 = probe883['steps'][1]['decision']
    gate883('G2', 'PASS', probe=probe883['episode_id'], cartridge=probe883['cartridges'][0], read=rd883, step1_parity=probe883['step1_parity'],
            restore=probe883['exact_restore_vs_first_mount'], isolated=probe883['isolated_after_episode'], seconds=probe883['seconds'])
    STATE883['status'] = 'G3'
    admit883('G3', len(CELLS883) * len(ARMS883))
    for w_, c_ in CELLS883:
        spec_ = by_key883[(int(w_), c_)]
        ep_ = episode883(env883, spec_, 'NOFB', 'NOFB_%s_%s' % (w_, c_), HORIZON883)
        STATE883['baseline']['%s_%s' % (w_, c_)] = compare_fixture883(ep_, REFS883[(spec_['item'], 'NO_FEEDBACK')])
    gate883('G3', 'PASS', labels={k: v['label'] for k, v in STATE883['baseline'].items()},
            note='a DIVERGED label is recorded, not a block: the live NOFB baseline is used (pre-registered)')
    STATE883['status'] = 'G4'
    for i_, (w_, c_) in enumerate(CELLS883):
        admit883('G4_%s_%s' % (w_, c_), 2 * (len(CELLS883) - i_))
        eps_ = {'NOFB': next(e for e in STATE883['episodes'] if e['episode_id'] == 'NOFB_%s_%s' % (w_, c_))}
        for a_ in ('CBLIND', 'VIS'):
            eps_[a_] = episode883(env883, by_key883[(int(w_), c_)], a_, '%s_%s_%s' % (a_, w_, c_), HORIZON883)
        cell_ = assemble_cell883(w_, c_, eps_); STATE883['cells']['%s_%s' % (w_, c_)] = cell_
        if not cell_['technical_endpoint'] and not all(cell_['integrity'].values()):
            raise Gate883('G4_CELL_INTEGRITY %s %s' % ((w_, c_), cell_['integrity']))
    gate883('G4', 'PASS', cells=sorted(STATE883['cells']), not_run=STATE883['not_run'],
            technical_endpoint_cells=sorted(k for k, v in STATE883['cells'].items() if v['technical_endpoint']))
    STATE883['status'] = 'G5'
    if records_digest861(env883) != digest883 or physical_seal863(env883, env883['MEMNULL841']) != null_seal883 or \
            weights_digest877(env883) != WEIGHTS0_878 or hook_audit859(env883, 'T883_final')['hook_count']:
        raise Gate883('POST_RUN_INTEGRITY')
    mc2_ = model_contract883(env883, CC_GPU)
    if not mc2_['ok']: raise Gate883('POST_RUN_MODEL_CONTRACT %s' % mc2_['checks'])
    offline883(offline_env883(env883, ORACLE_VAULT883), by_key883)
    gate883('G5', 'PASS', episodes=len(STATE883['offline']['episodes']), live_env_oracle_free=not STATE883['offline']['live_env_has_oracle_keys'])
    STATE883['status'] = 'G6'
    integrity_ok883 = not STATE883['cleanup_errors'] and not STATE883['offline']['live_env_has_oracle_keys']
    STATE883['result'] = verdict883(STATE883['cells'], REQUIRED_CELLS883, integrity_ok883, True)
    gate883('G6', 'PASS', result=STATE883['result']['result'], labels=STATE883['result']['labels'])
    STATE883['status'] = 'COMPLETE'
except Budget883 as exc:
    STATE883['error'] = str(exc); STATE883['not_run'].append('BUDGET_STOP at %s: %s' % (STATE883['status'], exc))
    try:
        if 'by_key883' in globals() and ORACLE_VAULT883 is not None and STATE883['cells']:
            offline883(offline_env883(env883, ORACLE_VAULT883), by_key883)
        STATE883['result'] = verdict883(STATE883['cells'], REQUIRED_CELLS883, True, False)   # allow_pass=False: never PASS
        STATE883['result']['labels'].append('BUDGET_STOP')
    except Exception as exc2:
        STATE883['result'] = {'result': 'TECHNICAL_BLOCK', 'labels': ['OFFLINE_AFTER_BUDGET_STOP_FAILED', 'BUDGET_STOP'], 'reason': str(exc2)}
    STATE883['status'] = 'BUDGET_STOP_AT_' + str(STATE883['status'])
except BaseException as exc:
    STATE883['error'] = '%s: %s' % (type(exc).__name__, exc); STATE883['traceback'] = traceback.format_exc()
    STATE883['result'] = {'result': 'TECHNICAL_BLOCK', 'labels': ['FAILED_AT_' + str(STATE883['status'])], 'reason': STATE883['error'][:400]}
    STATE883['gates'].setdefault(str(STATE883['status']), {'status': 'FAIL', 'error': STATE883['error'][:600]})
    STATE883['status'] = 'FAILED_AT_' + str(STATE883['status'])
    (ROOT864 / '883r2_traceback.txt').write_text(STATE883['traceback'], encoding='utf-8')
    print('TEST883R2 ERROR', STATE883['error'][:300], '| full traceback:', ROOT864 / '883r2_traceback.txt', file=ERROR_CONSOLE864, flush=True)
    print(STATE883['traceback'], file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        if _o883.path.exists(CART_ROOT883):
            left_ = sorted(_o883.listdir(CART_ROOT883)); _s883.rmtree(CART_ROOT883)
            if left_: STATE883['cleanup_errors'].append({'episode_id': 'CART_ROOT', 'errors': ['LEFTOVER %s' % left_[:20]]})
    except BaseException as exc: STATE883['cleanup_errors'].append({'episode_id': 'CART_ROOT', 'errors': ['%s: %s' % (type(exc).__name__, exc)]})
    if STATE883['cleanup_errors'] and (STATE883['result'] or {}).get('result') != 'TECHNICAL_BLOCK':
        STATE883['result'] = dict(STATE883['result'] or {}, result='TECHNICAL_BLOCK', labels=['CLEANUP_FAILED'], reason='cleanup errors')
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
