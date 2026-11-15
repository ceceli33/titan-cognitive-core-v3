# AKBASCORE SILICON HIPPOCAMPUS — TEST866 / M6-S01 — ONE CELL, ONE RUN: CPU preflight -> model -> G0/G1 -> S0A-S0G -> automatic
#   Stage 1 (content-specific native readability of a physical CUT3/H3/KV experience bank) when, and only when, Stage 0 and
#   the Stage-1 readiness / preseal gates pass. Base: 886.py (commit 289f4260, blob 638cf623) = M6S0 + the repairs B01-B17
#   of the 886 review. Locked native backbone unchanged (car867 / reading867 / control_step867 / execute866 / hop865 /
#   mount865 / free865 / 873 / 877 / 878). TEST866 is the experiment name; execute866 is the locked executor.
#   GPU EXECUTION NOT VERIFIED BY THE AUTHOR.
import ast as _a883, hashlib as _h883, json as _j883, os as _o883, re as _r883, shutil as _s883, urllib.request as _u883
import math as _m883, gzip as _g883, collections as _c883, marshal as _ms885, copy as _cp885
import numpy as _np883
_a882, _h882, _j882, _o882, _r882 = _a883, _h883, _j883, _o883, _r883
_a881, _h881, _j881, _o881, _r881, _s881 = _a883, _h883, _j883, _o883, _r883, _s883
ENGINE_URL883 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB883, MARKER883 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', 'AKBASCORE SILICON HIPPOCAMPUS — TEST866 / M6-S01'
HEAD883 = '3d75f289b88271440f4e3e13c2491699e6dc14ca'
FIXTURE_BLOB883, FIXTURE_SHA883 = 'f75a94ebbab8272878050579988cd35cb1deb822', 'daf5a8c4bd36811328a4ab173fe5cd300cc93c812558b883232e60ae42967f21'


def blob883(raw):
    return _h883.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def engine_parts883():
    with _u883.urlopen(_u883.Request(ENGINE_URL883, headers={'User-Agent': 'AKBASCORE-TEST866'}), timeout=240) as r:
        raw = r.read()
    assert blob883(raw) == ENGINE_BLOB883, ('ENGINE_BLOB_MISMATCH', blob883(raw))
    text = raw.decode('utf-8'); _a883.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST866_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST866_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST866_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('TEST866_engine.log', 'TEST866_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST866_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / 'TEST866_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / 'TEST866_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST866_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old)
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL883, 'git_blob': blob883(raw), 'sha256': _h883.sha256(raw).hexdigest()}


try:
    ENGINE883, ENGINE_INFO883 = engine_parts883()
except BaseException as _exc883:
    import time as _t883, traceback as _tb883
    _p883 = '/content/TEST866_PRE_ENGINE_ERROR_%s.txt' % _t883.strftime('%Y%m%dT%H%M%SZ', _t883.gmtime())
    try:
        with open(_p883, 'w', encoding='utf-8') as _f883: _f883.write(_tb883.format_exc())
    except OSError: _p883 = 'NOT_WRITTEN'
    print('TEST866 PRE-ENGINE ERROR (before console capture):', type(_exc883).__name__, _exc883, '| traceback:', _p883)
    raise
exec(compile(ENGINE883['prefix'], 'test870.py:prefix', 'exec'), globals())
exec(compile(ENGINE883['body'], 'test870.py:engine', 'exec'), globals())
print('TEST866 ENGINE', _j883.dumps(ENGINE_INFO883, sort_keys=True))

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
                 'model_contract883': ('output_hidden_states', 'output_attentions'),   # read-only config check (C8)
                 'snapshot_m6': ('hop865', 'mount865', 'free865'),
                 'st_m6': ('free865',)}                              # CPU sandbox test of the locked free865 body                     # M6 step-1 snapshot (no action executed)
ORACLE883 = {'supported851', 'node851', 'world867', 'correct867', 'success867', 'worlds829', 'offline883', 'OFFLINE883',
             'score_fixture883', 'world_index_label', 'FIXTURE_SCORES883', 'ORACLE_VAULT883', 'offline_env883', 'OFFLINE867',
             'world_index_truth', 'offline_target', 'install_offline_evaluator859', 'offline_evaluate865', 'offline_evaluate866',
             'offline_evaluate867', 'correct866', 'evaluator_env885', 'episode_scores885', 'fixture_scores885',
             'vault_fingerprint885', 'OFFLINE_DIGEST_G1_885', 'VAULT_FP885', 'locked_evaluator_sandbox885'}
ORACLE_ENV_KEYS883 = ('worlds829', 'node851', 'supported851')   # removed from the live env after build_specs869 (C6)
DYNAMIC883 = {'getattr', 'setattr', 'hasattr', 'delattr', 'exec', 'eval', 'compile', '__import__', 'globals', 'locals', 'vars',
              'importlib', '__dict__', '__globals__', '__builtins__'}
RUNTIME883 = ('episode883', 'write_experience883', 'read_with_experience883', 'prepare_experience883', 'reading_view883',
              'guard883', 'cell_admission883', 'event_contract883', 'causal_effect883', 'step1_parity883', 'cleanup883',
              'mount_ok883', 'read_contract883', 'exp_op883',
              'snapshot_m6', 'm6_xspan', 'm6_car', 'm6_mask_bias', 'cut3_rows_m6', 'gate_block_gpu_m6')
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
CART_ROOT883 = '/content/TEST866_EPISODE_CARTRIDGES'  # outside ROOT864: isolated per episode, deleted after the episode
REQUIRED_WORLDS883 = ('10', '09', '03')              # = select_worlds883() (checked by a CPU selftest before the model)
REQUIRED_CELLS883 = tuple('%s_%s' % (w, c) for w in REQUIRED_WORLDS883 for c in CONDITIONS883)
PREREG883 = {
    'test': 'TEST866 / M6-S01 (name given by the user)', 'head': HEAD883, 'repairs_of': '883_R3.py commit aff38957 blob 782f3f1c sha256 ae3c7352 (R3 G2 TECHNICAL_BLOCK: T0_865 None, F1 NOT_TESTED)',
    'clock': 'T_START883 is the single experiment clock (never reset). Right before the first G2 probe: T0_865 = now, '
             'remaining_total_s = WALL_S883 - (now - T_START883) (<= 0 -> BUDGET_STOP), TEST865_MINUTES = (remaining_total_s - '
             '1e-6 s) / 60 (the phase deadline is never looser than the total deadline), ONE rearm_budget865 (CALL_ALLOWANCE865 '
             '= 3000 kept), the first budget_left865 must return True. T0_841 and CALLS849 are not reset. The +30 min that the '
             'locked rearm adds to HARD_BUDGET_MIN841 is the locked engine margin, not a replacement of the 75 min deadline, '
             'which guard883 and admission enforce unchanged',
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
    'mount_contract': 'every mount865 record: n_exact, all_80_layers, finite, prior_prefix_exact is not False and '
                      'exact_restore_vs_first_mount is not False (None = first mount of that set, accepted); the episode-end '
                      'restore test of cleanup883 is kept separately',
    'read_contract': 'every experience read, before the model reads: provenance present and well formed, id == X883_ + sha256 '
                     '(provenance)[:16], entry sha256 / tensor_sha / id equal to the manifest record of the latest cartridge, '
                     'step_written == decision step - 1, file inside the episode directory, spans X2 / A / C contiguous with '
                     'C end == body_tokens; load_exp878 itself checks file SHA-256, book id, P, n, body_tokens and tensor SHA '
                     '(not repeated); after append: n_exact, C span inside the appended range, B prefix first / last layer bitwise. '
                     'Heavy zero-C / trace parity stays on the first CBLIND read only',
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
               'measured_separately': ['wall s', 'peak alloc / reserved GiB', 'free GiB', 'calls849', 'SSD bytes', 'FFE by kind',
                                       'per experience op: write s, load+append+read s, body_tokens, free GiB after'],
               'long_cartridge': 'mechanical: the first cartridge of the run whose body_tokens exceed the maximum body_tokens written '
                                 'by the G2 probe; its natural write / load+append+read seconds and free GiB are recorded; every '
                                 'admission after it uses it; until it is observed every admission record says '
                                 'LONG_CARTRIDGE_NOT_YET_MEASURED (projection basis = probe + measured steps, not a guarantee); '
                                 'an experience op leaving < free_vram_min_gib refuses further admission (BUDGET_STOP). No extra '
                                 'forward and no artificial action is produced for measurement. OOM prevention is not claimed',
               'readmission': 'before G3, before every cell and after every live episode of G3 / G4',
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
                       'ssd_bytes': 0, 'admissions': [], 'exp_ops': [],
                       'long_cartridge': {'threshold_body_tokens': None, 'first_long': None, 'measured': False}},
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


# locked offline-evaluator AST digest: sha256(ast.dump(Module([node851, supported851]))) of BODY851 in 851.py (blob 0f01e73b);
# reproduced on CPU from the locked bytes and equal to the G1 value printed by install_offline_evaluator859 in 884.log
EVAL_DIGEST885 = '269ad030168813e9b945c095d4b37d1744394903c9eb459d016c72783276df99'


def g2_budget_plan883(now, t_start, wall_s, eps_s=1e-6):
    # fix 1: phase clock of the locked budget_left865 from the unchanged experiment clock; None = no time left (no probe)
    elapsed = float(now) - float(t_start); remaining = float(wall_s) - elapsed
    if not remaining > eps_s: return None
    return {'T0_865': float(now), 'elapsed_total_s': round(elapsed, 3), 'remaining_total_s': round(remaining, 3),
            'TEST865_MINUTES': (remaining - eps_s) / 60.0, 'eps_s': eps_s}


def budget_clocks883(env, stage):
    # fix 2: separately labelled clocks; none of them is a model-load time
    now = time.perf_counter()
    try: cap = round(now - START864, 3)
    except NameError: cap = 'NA'
    c = {'stage': stage, 'cell_or_engine_capture_wall_s': cap, 'experiment_total_wall_s': round(now - T_START883, 3),
         'g2_phase_wall_s': None if T0_865 is None else round(now - T0_865, 3),
         'native_engine_wall_s': round(now - float(env['T0_841']), 3) if 'T0_841' in env else 'NA',
         'remaining_total_s': round(WALL_S883 - (now - T_START883), 3), 'TEST865_MINUTES': TEST865_MINUTES,
         'HARD_BUDGET_MIN841': float(env['HARD_BUDGET_MIN841']) if 'HARD_BUDGET_MIN841' in env else 'NA',
         'CALL_CAP849': int(env['CALL_CAP849']) if 'CALL_CAP849' in env else 'NA',
         'CALLS849': int(env['CALLS849']) if 'CALLS849' in env else 'NA', 'CALL_ALLOWANCE865': CALL_ALLOWANCE865,
         'note': '+30 min in HARD_BUDGET_MIN841 is the locked engine margin; the 75 min total deadline is guard883 / admission'}
    c['calls_left'] = c['CALL_CAP849'] - c['CALLS849'] if isinstance(c['CALL_CAP849'], int) and isinstance(c['CALLS849'], int) else 'NA'
    return c


def gate_fail_record883(stage, error):
    # fix 3: the same fields as gate883 for an exception path
    try: peak = round(STATE883['budget']['peak_alloc_gib'], 3)
    except Exception: peak = 'NA'
    return {'status': 'FAIL', 'wall_s': round(time.perf_counter() - T_START883, 1), 'peak_alloc_gib': peak, 'error': str(error)[:600]}


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


def suffix_last883(source):
    sfx = 'exec(compile(ENGINE' + "883['suffix']"
    nonempty = [l for l in source.splitlines() if l.strip()]
    i = source.rfind(sfx)
    after = source[i:].split('\n', 1)[1] if i >= 0 and '\n' in source[i:] else ''
    return bool(nonempty) and nonempty[-1].startswith(sfx) and i >= 0 and not after.strip()


def source_contract883(source):
    # F7: one complete cell, all parts, in order, no multi-cell / %run / shell escape; line count by splitlines
    lines = source.splitlines()
    bad = [i + 1 for i, l in enumerate(lines) if _r883.match(r'\s*(%%|%run|%load|!|# %%|#%%|In \[\d*\]:)', l)]
    once = lambda *frag: source.count(''.join(frag)) == 1       # patterns joined so this function never matches itself
    out = {'lines': len(lines), 'marker_once': once('MARKER', "883 = '") and source.count(MARKER883) >= 1,
           'magic_or_cell_separator_lines': bad[:10], 'episode_def_once': once('def ', 'episode883('),
           'offline_def_once': once('def ', 'offline883('), 'verdict_def_once': once('def ', 'verdict883('),
           # B01: the last NON-EMPTY line must be the engine suffix; trailing whitespace is tolerated, any code after it is not
           'ends_with_engine_suffix': suffix_last883(source),
           't866_marker': 'TEST866 / M6-S01' in source}
    out['ok'] = bool(out['marker_once'] and not bad and out['episode_def_once'] and out['offline_def_once'] and
                     out['verdict_def_once'] and out['ends_with_engine_suffix'] and out['t866_marker'])
    return out


def write_probe883(root):
    # G0 preflight: results directory writable, JSON + ZIP round trip, then removed (no experiment data)
    import zipfile as _z883
    p = _o883.path.join(str(root), '_t866_write_probe.json'); zp = p + '.zip'
    payload = _j883.dumps({'probe': 'TEST866', 't': time.time()}).encode()
    with open(p, 'wb') as f: f.write(payload)
    with _z883.ZipFile(zp, 'w', _z883.ZIP_DEFLATED) as z: z.write(p, 'probe.json')
    with _z883.ZipFile(zp) as z: ok = z.read('probe.json') == payload and z.testzip() is None
    _o883.remove(p); _o883.remove(zp)
    return {'json_zip_roundtrip': ok, 'removed': not _o883.path.exists(p) and not _o883.path.exists(zp)}


def clock_order883(tree):
    # fix 1 source contract: exactly one rearm_budget865 call in the cell, at main-block level, after the module-level
    # assignments of T0_865 and TEST865_MINUTES and before the first episode883 call (the G2 probe)
    calls = [n for n in _a883.walk(tree) if isinstance(n, _a883.Call) and getattr(n.func, 'id', None) == 'rearm_budget865']
    main = next((n for n in tree.body if isinstance(n, _a883.Try) and 'capture_source883()' in _a883.unparse(n)), None)
    out = {'rearm_calls': len(calls), 'main_found': main is not None}
    if main is None or len(calls) != 1: return dict(out, ok=False)
    line = lambda pred: next((st.lineno for st in main.body if pred(st)), None)
    tgt = lambda st, name: isinstance(st, _a883.Assign) and any(isinstance(t, _a883.Name) and t.id == name for t in st.targets)
    out['T0_865_line'] = line(lambda st: tgt(st, 'T0_865'))
    out['TEST865_MINUTES_line'] = line(lambda st: tgt(st, 'TEST865_MINUTES') or (isinstance(st, _a883.Assign) and any(
        isinstance(t, _a883.Tuple) and any(getattr(e, 'id', None) == 'TEST865_MINUTES' for e in t.elts) for t in st.targets)))
    out['rearm_line'] = calls[0].lineno
    out['rearm_at_main_level'] = any(isinstance(st, _a883.Expr) and st.value is calls[0] for st in main.body)
    out['first_episode_line'] = min((n.lineno for st in main.body for n in _a883.walk(st) if isinstance(n, _a883.Call) and
                                     getattr(n.func, 'id', None) == 'episode883'), default=None)
    out['ok'] = bool(out['rearm_at_main_level'] and out['T0_865_line'] and out['TEST865_MINUTES_line'] and out['first_episode_line'] and
                     max(out['T0_865_line'], out['TEST865_MINUTES_line']) < out['rearm_line'] < out['first_episode_line'])
    return out


EPISODE_OBSERVER883 = None   # B04: post-commit observer (None = OFF: no observation is constructed)
REC_SINK883 = None           # Stage 1: persistent-bank sink for REC-arm experience cartridges (None outside Stage 1)


def capture_source883():
    try:
        source, how = get_ipython().history_manager.input_hist_raw[-1], 'IPYTHON_CURRENT_CELL'
    except NameError:
        source = open(__file__, encoding='utf-8').read() if '__file__' in globals() else None; how = 'FILE_%RUN'
    assert source and MARKER883 in source and 'def episode883' in source and 'def offline883' in source, \
        'EXECUTED_TEST866_SOURCE_NOT_CAPTURED (paste all three parts into ONE cell, in order)'
    sc = source_contract883(source)
    assert sc['ok'], ('SOURCE_CONTRACT883', sc)
    tree = _a883.parse(source)
    co = clock_order883(tree)
    assert co['ok'], ('CLOCK_ORDER884', co)
    funcs = {n.name: n for n in tree.body if isinstance(n, _a883.FunctionDef)}
    for name, node in funcs.items():
        if name.endswith(('883', '884', '885', '_m6')) or name.startswith('m6_'): scan883(node, EXEC_ALLOW883.get(name, ()))
    assert set(RUNTIME883) <= set(funcs), ('RUNTIME_FUNCTIONS_MISSING', sorted(set(RUNTIME883) - set(funcs)))
    for name in RUNTIME883: oracle_scan883(funcs[name])
    calls = [n for n in _a883.walk(tree) if isinstance(n, _a883.Call) and getattr(n.func, 'id', None) == 'reproduce_pre859859']
    assert len(calls) == 1, 'MODEL_LOADER_CALL_COUNT_NOT_ONE'
    ex = [n for n in _a883.walk(tree) if isinstance(n, _a883.Call) and getattr(n.func, 'id', None) == 'execute866']
    assert len(ex) == 1, 'EXECUTOR_CALL_COUNT_NOT_ONE'
    (ROOT864 / 'TEST866.py').write_text(source, encoding='utf-8')
    STATE883['source'] = {'how': how, 'executed_cell_git_blob': git_blob864(source.encode()),
                          'executed_cell_sha256': sha256_bytes864(source.encode()), 'lines_splitlines': sc['lines'],
                          'source_contract': sc, 'clock_order': co, 'firewall': 'PASS',
                          'oracle_firewall': 'PASS (%d runtime functions, dynamic escapes refused)' % len(RUNTIME883),
                          'single_executor_call': True, 'self_hash': 'NONE (measured at runtime only)'}
    line883('SOURCE', 'executed_cell_git_blob=%s' % STATE883['source']['executed_cell_git_blob'],
            'sha256=%s' % STATE883['source']['executed_cell_sha256'], 'lines=%d' % sc['lines'], 'base=883_R3.py blob 782f3f1c')
    json_write864('TEST866_source_manifest.json', dict(STATE883['source'], prereg_sha256=PREREG_SHA883, head=HEAD883,
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
    # index alignment (R3-02): cartridges[i] is E_{i+1}, written from step i+1 and read by decision i+2
    out['cards_index_aligned'] = all((x.get('provenance_core') or {}).get('step_written') == i + 1
                                     for ep in (cb, vi) for i, x in enumerate(ep['cartridges'][:k]))
    out['cards_ok'] = out['cards_index_aligned'] and all(cartridge_core883(x) == cartridge_core883(y) and x.get('tensor_sha') is not None
                                                         for x, y in zip(cb['cartridges'][:k], vi['cartridges'][:k]))
    return out


def cell_admission883(elapsed_s, step_seconds, overhead_s, remaining_episodes, horizon=None, reserve_s=None, wall_s=None,
                      min_free_after_exp_gib=None, long_measured=None):
    # C7 / R3-04 conservative: empty history is never admitted; every remaining episode (NOFB and F1) is projected at the worst
    # measured (heaviest) step; an experience op that left < FREE_MIN_GIB883 free refuses admission. long_measured is recorded
    # by the caller as the projection basis; it never makes the projection look exact.
    horizon = HORIZON883 if horizon is None else horizon
    reserve_s = OFFLINE_RESERVE_S883 if reserve_s is None else reserve_s
    wall_s = WALL_S883 if wall_s is None else wall_s
    if not step_seconds: return False, None
    if min_free_after_exp_gib is not None and min_free_after_exp_gib < FREE_MIN_GIB883: return False, None
    worst = max(step_seconds); over = max(overhead_s) if overhead_s else worst
    projected = elapsed_s + remaining_episodes * (horizon * worst * SAFETY883 + over) + reserve_s
    return projected <= wall_s, round(projected, 1)


def long_update883(lc, op):
    # R3-04 mechanical long-cartridge rule: first op with body_tokens > threshold (max body_tokens of the G2 probe)
    if lc['threshold_body_tokens'] is None or lc['first_long'] is not None: return False
    if int(op.get('body_tokens') or 0) > int(lc['threshold_body_tokens']) and op.get('read_s') is not None:
        lc['first_long'] = dict(op); lc['measured'] = True
        return True
    return False


def mount_ok883(records):
    # R3-01: locked mount865 record schema (test870.py mount865): exact_restore_vs_first_mount is None on the first mount of a
    # card set, True / False afterwards. Only an explicit False is refused; an absent field is refused (no silent proof)
    return bool(records) and all(m.get('n_exact') is True and m.get('all_80_layers') is True and m.get('finite') is True and
                                 'prior_prefix_exact' in m and m['prior_prefix_exact'] is not False and
                                 'exact_restore_vs_first_mount' in m and m['exact_restore_vs_first_mount'] is not False
                                 for m in records)


def read_contract883(entry, card, step, ep_id, cdir):
    # R3-03 light per-read contract, checked before the model reads; independent of any model output
    why = []
    prov = entry.get('provenance') if isinstance(entry, dict) else None
    if not isinstance(prov, dict): return ['PROVENANCE_MISSING']
    for k in ('test', 'namespace', 'action', 'spans_body', 'step_written', 'episode_id', 'X_sha256', 'C_rows_sha256'):
        if k not in prov: why.append('PROVENANCE_FIELD_MISSING:' + k)
    if why: return why
    if prov['test'] != 'TEST883' or prov['namespace'] != 'EPISODE_ONLY_NOT_A_BANK_CARD': why.append('PROVENANCE_NAMESPACE')
    if prov['action'] in TERMINAL883: why.append('PROVENANCE_TERMINAL_ACTION')
    if prov['episode_id'] != ep_id: why.append('PROVENANCE_EPISODE')
    if prov['step_written'] != step - 1: why.append('STEP_WRITTEN %s != %s' % (prov['step_written'], step - 1))
    eid = 'X883_' + _h883.sha256(_j883.dumps(prov, sort_keys=True, default=str).encode()).hexdigest()[:16]
    if entry.get('id') != eid: why.append('ID_NOT_PROVENANCE_HASH')
    for k in ('id', 'sha256', 'tensor_sha', 'body_tokens', 'pre_C_seal'):
        if card.get(k) != entry.get(k): why.append('MANIFEST_MISMATCH:' + k)
    if not str(entry.get('file', '')).startswith(str(cdir) + _o883.sep): why.append('FILE_OUTSIDE_EPISODE_DIR')
    sp = prov['spans_body']; q = entry.get('body_tokens')
    try:
        x2, a_, c_ = [list(map(int, sp[k])) for k in ('X2', 'A', 'C')]
        if not (x2[0] == 0 and x2[1] == a_[0] and a_[1] == c_[0] and 0 < x2[1] < a_[1] < c_[1] and c_[1] == int(q)):
            why.append('SPANS_NOT_CONTIGUOUS_OR_C_END_NE_BODY_TOKENS')
        if list(card.get('C_span_body') or []) != c_: why.append('C_SPAN_MANIFEST_MISMATCH')
    except (KeyError, TypeError, ValueError):
        why.append('SPANS_MALFORMED')
    return why


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
            'probe_horizon_2_natural': expected_cartridges883(2, 'HORIZON_2', 2) == 1 and not natural_end883('HORIZON_2'),
            'step2_same_card_accepted_index_aligned': a2.get('cards_index_aligned') is True,
            'misaligned_index_refused': compare_prefix883(ep(['ACQUIRE', 'STOP'], [card('T1', step=2)]),
                                                          ep(['ACQUIRE', 'ACCEPT'], [card('T1', step=2)]))['cards_ok'] is False,
            'extra_cartridge_fails_cardinality': expected_cartridges883(2, 'MODEL_STOP') != 2,
            'missing_cartridge_fails_cardinality': expected_cartridges883(3, 'MODEL_STOP') != 1}


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


def vault_fingerprint885(vault):
    # identity + content of every vault object: functions by code bytes and globals identity, data by canonical JSON
    fp = {}
    for k in sorted(vault):
        v = vault[k]
        if hasattr(v, '__code__'):
            fp[k] = {'id': id(v), 'globals_id': id(v.__globals__), 'code_sha256': _h883.sha256(_ms885.dumps(v.__code__)).hexdigest()}
        else:
            fp[k] = {'id': id(v), 'sha256': _h883.sha256(_j883.dumps(v, sort_keys=True, default=str).encode()).hexdigest()}
    return fp


def evaluator_env885(env, vault, g1_digest, vault_fp, installer=None):
    # THE single G5 evaluator path (normal G5 and budget-stop fallback): a new offline env, then the SAME locked
    # install_offline_evaluator859 run on it, so node851 / supported851 get __globals__ = oenv. Nothing is put back in the live env.
    installer = install_offline_evaluator859 if installer is None else installer
    if set(ORACLE_ENV_KEYS883) & set(env): raise Gate883('G5_LIVE_ENV_HAS_ORACLE_KEYS %s' % sorted(set(ORACLE_ENV_KEYS883) & set(env)))
    if vault_fingerprint885(vault) != vault_fp: raise Gate883('G5_VAULT_CHANGED_BEFORE_REINSTALL')
    oenv = offline_env883(env, vault)
    digest = installer(oenv)
    checks = {'oenv_is_new_dict': oenv is not env, 'node851_globals_is_oenv': oenv['node851'].__globals__ is oenv,
              'supported851_globals_is_oenv': oenv['supported851'].__globals__ is oenv,
              'digest_equals_g1': digest == g1_digest, 'digest_equals_locked_851': digest == EVAL_DIGEST885,
              'live_env_oracle_free': not set(ORACLE_ENV_KEYS883) & set(env),
              'vault_unchanged': vault_fingerprint885(vault) == vault_fp,
              'worlds829_is_vault_object': oenv['worlds829'] is vault['worlds829'],
              'reinstalled_are_new_objects': oenv['node851'] is not vault['node851'] and oenv['supported851'] is not vault['supported851']}
    rec = dict(checks, digest=digest, g1_digest=g1_digest, oenv_keys=len(oenv))
    if not all(checks.values()): raise Gate883('G5_EVALUATOR_NAMESPACE %s' % sorted(k for k, v in checks.items() if not v))
    return oenv, rec


def episode_scores885(oenv, by_key, episodes):
    scores = {}
    for ep in episodes:
        if ep['episode_id'].startswith('G2_PROBE'): continue
        spec = by_key[(ep['world_index'], ep['condition'])]                                  # KeyError = technical block
        row = {'end': ep['end'], 'accepted_candidate': ep['accepted'], 'final_mounted': ep['final_mounted']}
        y = int(bool(success867(oenv, row, spec))) if natural_end883(ep['end']) else None   # technical end: never success
        scores[ep['episode_id']] = {'Y': y, 'end': ep['end'], 'accepted': ep['accepted']}
    return scores


def fixture_scores885(oenv, by_key, records):
    fixture = _c883.defaultdict(lambda: {'n': 0, 'success': 0, 'model_accept': 0, 'supported_accept': 0})
    for r in records:                                             # all arms incl. K_SHAM (phase GATE4)
        if r.get('phase') not in ('PANEL', 'GATE4'): continue
        spec = by_key[(int(r['world_index']), r['condition'])]; s = fixture['%s|%s' % (r['arm'], r['condition'])]
        s['n'] += 1; s['success'] += int(bool(success867(oenv, r, spec))); s['model_accept'] += int(r['end'] == 'MODEL_ACCEPT')
        s['supported_accept'] += int(r['end'] == 'MODEL_ACCEPT' and bool(correct867(oenv, r, spec)))
    return dict(fixture)


def g5_complete885(scores, fixture):
    # G5 PASS only with all 18 analysis episodes scored (Y in {0,1}) and the full 869 fixture summary (288 rows, 24 groups)
    want = {'%s_%s' % (a, k) for k in REQUIRED_CELLS883 for a in ARMS883}
    c = {'analysis_episodes_18': set(scores) == want, 'every_Y_binary': all(scores.get(k, {}).get('Y') in (0, 1) for k in want),
         'fixture_rows_288': sum(v['n'] for v in fixture.values()) == 288, 'fixture_groups_24': len(fixture) == 24}
    return dict(c, ok=all(c.values()), missing=sorted(want - set(scores)),
                non_binary=sorted(k for k in want if scores.get(k, {}).get('Y') not in (0, 1)))


def locked_evaluator_sandbox885():
    # CPU preflight material from the LOCKED bytes only: node851 / supported851 AST of BODY851 (851.py) and the
    # install_offline_evaluator859 AST of 859.py, executed in a sandbox with its own STATE859 (no global is touched)
    lit = [n.value for n in _a883.walk(_a883.parse(RAW_SOURCES864['851.py'].decode()))
           if isinstance(n, _a883.Constant) and isinstance(n.value, str) and 'def supported851(' in n.value]
    assert len(lit) == 1, ('BODY851_LITERAL', len(lit))
    fns = {n.name: n for n in _a883.parse(lit[0]).body if isinstance(n, _a883.FunctionDef) and n.name in ('node851', 'supported851')}
    t859 = _a883.parse(RAW_SOURCES864['859.py'].decode())
    inst = [n for n in t859.body if isinstance(n, _a883.FunctionDef) and n.name in ('install_offline_evaluator859', 'sha256_bytes859')]
    sb = {'STATE859': {'offline_functions': {k: _cp885.deepcopy(v) for k, v in fns.items()}}, 'REAL_COMPILE859': compile,
          'short859': lambda *a: None, 'ast': _a883, 'copy': _cp885, 'hashlib': _h883}
    exec(compile(_a883.Module(inst, []), '859.py:install_offline_evaluator859', 'exec'), sb)
    dump0 = {k: _a883.dump(v, include_attributes=False) for k, v in sb['STATE859']['offline_functions'].items()}
    return sb, dump0


def world_t885(i):
    w = {k: '%s%02d' % (k.upper(), i) for k in ('start', 'middle', 'end', 'changed_end', 'fork_end', 'decoy_end', 'bridge_mid',
                                                'bridge_end', 'end3')}
    w['ids'] = {k: 'E_%s_%02d' % (k, i) for k in ('first', 'second', 'third', 'changed')}
    return w


def st_evaluator885():
    # G5 namespace repair, with the real locked installer + evaluator ASTs, the real seal / offline_env / success867 /
    # correct867 and a SYNTHETIC oracle (worlds). Scores here are SYNTHETIC_CPU_SMOKE_NOT_SCIENTIFIC_RESULT.
    res = {}
    sb, dump0 = locked_evaluator_sandbox885()
    inst = sb['install_offline_evaluator859']
    worlds = [world_t885(i) for i in range(12)]
    live = {'worlds829': worlds, 'P': 30}
    g1 = inst(live)                                                          # G1 equivalent
    res['1_g1_globals_are_live_env'] = live['node851'].__globals__ is live and live['supported851'].__globals__ is live
    res['1_g1_digest_equals_locked'] = g1 == EVAL_DIGEST885
    vault = seal_oracle883(live)
    res['2_seal_removes_three_keys'] = not set(ORACLE_ENV_KEYS883) & set(live) and set(vault) == set(ORACLE_ENV_KEYS883)
    fp = vault_fingerprint885(vault)
    w0 = worlds[0]; good = (w0['end'], w0, {w0['ids']['first'], w0['ids']['second']})
    copy_ = offline_env883(live, vault)
    try: copy_['supported851'](*good); res['3_dict_copy_reproduces_NameError'] = False
    except NameError as exc: res['3_dict_copy_reproduces_NameError'] = "'node851'" in str(exc)
    only = dict(live); only['node851'] = vault['node851']; only['supported851'] = vault['supported851']
    try: only['supported851'](*good); res['4_only_node851_in_copy_still_fails'] = False
    except NameError: res['4_only_node851_in_copy_still_fails'] = True
    oenv, rec = evaluator_env885(live, vault, g1, fp, installer=inst)
    res['5_reinstall_fixes'] = oenv['supported851'](*good) is True and oenv['node851'](w0['end'], w0) == 'end'
    res['5_digest_and_globals'] = rec['digest_equals_g1'] and rec['node851_globals_is_oenv'] and rec['supported851_globals_is_oenv']
    res['6_live_env_still_oracle_free'] = not set(ORACLE_ENV_KEYS883) & set(live) and 'node851' not in live
    res['6_vault_and_locked_asts_unchanged'] = vault_fingerprint885(vault) == fp and \
        {k: _a883.dump(v, include_attributes=False) for k, v in sb['STATE859']['offline_functions'].items()} == dump0
    res['6_vault_original_globals_still_live'] = vault['supported851'].__globals__ is live
    try: evaluator_env885(dict(live, node851=1), vault, g1, fp, installer=inst); res['6_leak_into_live_refused'] = False
    except Gate883: res['6_leak_into_live_refused'] = True
    try: evaluator_env885(live, dict(vault, worlds829=list(worlds)), g1, fp, installer=inst); res['6_vault_swap_refused'] = False
    except Gate883: res['6_vault_swap_refused'] = True
    try: evaluator_env885(live, vault, 'f' * 64, fp, installer=inst); res['6_digest_mismatch_refused'] = False
    except Gate883: res['6_digest_mismatch_refused'] = True
    sp = lambda c, w=0: {'condition': c, 'panel': 'OLD', 'world_index': w}
    S = lambda row, c: success867(oenv, row, sp(c))
    res['7_missing_stop_true'] = S({'end': 'MODEL_STOP'}, 'MISSING') is True
    res['7_missing_accept_false'] = S({'end': 'MODEL_ACCEPT', 'accepted_candidate': w0['end'], 'final_mounted': list(good[2])}, 'MISSING') is False
    res['7_fork_supported_true'] = S({'end': 'MODEL_ACCEPT', 'accepted_candidate': w0['end'], 'final_mounted': list(good[2])}, 'FORK') is True
    res['7_fork_unsupported_false'] = S({'end': 'MODEL_ACCEPT', 'accepted_candidate': w0['end'], 'final_mounted': [w0['ids']['first']]}, 'FORK') is False
    res['7_fork_wrong_answer_false'] = S({'end': 'MODEL_ACCEPT', 'accepted_candidate': w0['fork_end'], 'final_mounted': list(good[2])}, 'FORK') is False
    res['7_fork_horizon_false'] = S({'end': 'HORIZON_6', 'accepted_candidate': None, 'final_mounted': list(good[2])}, 'FORK') is False
    recs = _j883.loads(_g883.decompress(RAW_SOURCES864['869_full_records.json.gz']))
    by_key = {(w, c): sp(c, w) for w in range(12) for c in ('FORK', 'LIVE', 'MISSING', 'SUFFICIENT')}
    f1 = fixture_scores885(oenv, by_key, recs); f2 = fixture_scores885(oenv, by_key, recs)
    res['8_fixture_288_rows_24_groups'] = sum(v['n'] for v in f1.values()) == 288 and len(f1) == 24
    res['8_scores_labelled_SYNTHETIC_CPU_SMOKE_NOT_SCIENTIFIC_RESULT'] = True   # synthetic worlds: never a TEST884/885 result
    res['9_second_loop_identical'] = f1 == f2
    pos = [{'phase': 'PANEL', 'arm': 'V_X', 'condition': 'FORK', 'world_index': 0, 'end': 'MODEL_ACCEPT',
            'accepted_candidate': w0['end'], 'final_mounted': list(good[2])}]
    neg = [dict(pos[0], final_mounted=[w0['ids']['first']])]
    res['7_supported_accept_positive_branch'] = fixture_scores885(oenv, by_key, pos)['V_X|FORK']['supported_accept'] == 1
    res['7_supported_accept_negative_branch'] = fixture_scores885(oenv, by_key, neg)['V_X|FORK']['supported_accept'] == 0
    try: fixture_scores885(oenv, {k: v for k, v in by_key.items() if k != (0, 'FORK')}, pos); res['9_missing_spec_raises'] = False
    except KeyError: res['9_missing_spec_raises'] = True
    try: success867(dict(oenv, worlds829=worlds[:1]), pos[0], sp('FORK', 5)); res['9_missing_world_raises'] = False
    except IndexError: res['9_missing_world_raises'] = True
    eps = [{'episode_id': '%s_%s' % (a, k), 'world_index': int(k[:2]), 'condition': k[3:], 'end': 'MODEL_STOP', 'accepted': None,
            'final_mounted': []} for k in REQUIRED_CELLS883 for a in ARMS883] + [{'episode_id': 'G2_PROBE_10_MISSING'}]
    sc = episode_scores885(oenv, by_key, eps)
    res['10_g5_complete_on_full_set'] = g5_complete885(sc, f1)['ok'] and 'G2_PROBE_10_MISSING' not in sc
    sc_none = dict(sc); sc_none['VIS_03_FORK'] = dict(sc['VIS_03_FORK'], Y=None)
    res['10_g5_incomplete_on_None_Y'] = not g5_complete885(sc_none, f1)['ok']
    res['10_g5_incomplete_on_missing_episode'] = not g5_complete885({k: v for k, v in sc.items() if k != 'NOFB_10_FORK'}, f1)['ok']
    res['10_g5_incomplete_on_fixture_gap'] = not g5_complete885(sc, {k: v for k, v in f1.items() if k != 'V_X|FORK'})['ok']
    rt = _j883.loads(_j883.dumps({'episodes': sc, 'fixture': f1, 'evaluator_g5': rec}, default=str))
    res['10_json_roundtrip'] = rt['episodes'] == sc and rt['fixture'] == {k: v for k, v in f1.items()}
    return res


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
            'old_883_marker_refused': not c(ok_src.replace('TEST866 / M6-S01', 'TEST883 / F1'))['ok']}


def st_r3_mount883():
    # R3-01 (a): None / True accepted, explicit False refused even with every other field true; absent field refused
    good = {'n_exact': True, 'all_80_layers': True, 'finite': True, 'prior_prefix_exact': None, 'exact_restore_vs_first_mount': None}
    m = lambda **kw: dict(good, **kw)
    absent = {k: v for k, v in good.items() if k != 'exact_restore_vs_first_mount'}
    return {'first_mount_none_accepted': mount_ok883([good]), 'restore_true_accepted': mount_ok883([good, m(exact_restore_vs_first_mount=True)]),
            'restore_false_refused': not mount_ok883([good, m(exact_restore_vs_first_mount=False)]),
            'restore_false_refused_all_else_true': not mount_ok883([m(exact_restore_vs_first_mount=False, prior_prefix_exact=True)]),
            'prior_prefix_false_refused': not mount_ok883([m(prior_prefix_exact=False)]),
            'absent_restore_field_refused': not mount_ok883([absent]), 'no_records_refused': not mount_ok883([]),
            'n_exact_false_refused': not mount_ok883([m(n_exact=False)]), 'truthy_non_bool_refused': not mount_ok883([m(finite=1)])}


def r3_entry883(step=2, ep='E1', cdir='/c/E1', **over):
    prov = {'test': 'TEST883', 'namespace': 'EPISODE_ONLY_NOT_A_BANK_CARD', 'action': 'ACQUIRE', 'episode_id': ep,
            'step_written': step - 1, 'X_sha256': 'x', 'C_rows_sha256': 'c', 'spans_body': {'X2': [0, 40], 'A': [40, 43], 'C': [43, 60]}}
    prov.update(over.pop('prov', {}))
    eid = 'X883_' + _h883.sha256(_j883.dumps(prov, sort_keys=True, default=str).encode()).hexdigest()[:16]
    entry = {'id': eid, 'file': cdir + _o883.sep + eid + '.pt', 'sha256': 'F', 'tensor_sha': {'h': 'T'}, 'body_tokens': 60,
             'pre_C_seal': 'P', 'provenance': prov}
    card = {k: entry[k] for k in ('id', 'sha256', 'tensor_sha', 'body_tokens', 'pre_C_seal')}; card['C_span_body'] = [43, 60]
    entry.update(over.pop('entry', {})); card.update(over.pop('card', {}))
    return entry, card


def st_r3_read883():
    # R3-03 (c): light per-read contract
    R = lambda e, c, step=2, ep='E1', cdir='/c/E1': read_contract883(e, c, step, ep, cdir)
    e, c = r3_entry883()
    bad_span, cs = r3_entry883(prov={'spans_body': {'X2': [0, 40], 'A': [41, 43], 'C': [43, 60]}})
    c_end, cc = r3_entry883(prov={'spans_body': {'X2': [0, 40], 'A': [40, 43], 'C': [43, 59]}})
    no_prov = dict(e); no_prov.pop('provenance')
    miss_field, cm = r3_entry883(); miss_field['provenance'] = {k: v for k, v in miss_field['provenance'].items() if k != 'step_written'}
    bt, cb = r3_entry883(entry={'body_tokens': 61})
    sha, csh = r3_entry883(card={'sha256': 'G'})
    tsh, ct = r3_entry883(card={'tensor_sha': {'h': 'U'}})
    forged = dict(e, provenance=dict(e['provenance'], action='ADVANCE'))
    term, ctm = r3_entry883(prov={'action': 'STOP'})
    return {'valid_cartridge_passes': R(e, c) == [], 'broken_span_refused': bool(R(bad_span, cs)),
            'C_end_ne_body_tokens_refused': bool(R(c_end, cc)), 'missing_provenance_refused': R(no_prov, c) == ['PROVENANCE_MISSING'],
            'missing_provenance_field_refused': bool(R(miss_field, cm)), 'body_token_mismatch_refused': bool(R(bt, cb)),
            'manifest_sha_mismatch_refused': bool(R(sha, csh)), 'tensor_sha_mismatch_refused': bool(R(tsh, ct)),
            'provenance_edit_breaks_id_hash': 'ID_NOT_PROVENANCE_HASH' in R(forged, c),
            'wrong_step_refused': bool(R(e, c, step=3)), 'wrong_episode_refused': bool(R(e, c, ep='E2')),
            'file_outside_episode_dir_refused': bool(R(e, c, cdir='/c/OTHER')), 'terminal_action_refused': bool(R(term, ctm)),
            'C_span_manifest_mismatch_refused': bool(R(e, dict(c, C_span_body=[43, 59])))}


def st_r3_budget883():
    # R3-04 (d): empty history, short probe, long cartridge measured / not measured, VRAM after experience op
    A = cell_admission883
    lc = {'threshold_body_tokens': None, 'first_long': None, 'measured': False}
    before_threshold = long_update883(lc, {'body_tokens': 900, 'read_s': 3.0})
    lc['threshold_body_tokens'] = 120
    short = long_update883(lc, {'body_tokens': 120, 'read_s': 1.0})
    unmeasured = long_update883(lc, {'body_tokens': 400, 'read_s': None})
    first = long_update883(lc, {'body_tokens': 400, 'read_s': 5.0})
    second = long_update883(lc, {'body_tokens': 800, 'read_s': 9.0})
    return {'empty_history_refused': A(0.0, [], [], 18)[0] is False,
            'short_probe_projection_admits_when_it_fits': A(1500.0, [12.0, 13.0], [20.0], 18)[0] is True,
            'heavy_long_step_refuses_remaining': A(1500.0, [12.0, 40.0], [20.0], 18)[0] is False,
            'no_threshold_no_long': before_threshold is False and lc['first_long']['body_tokens'] == 400,
            'equal_to_probe_not_long': short is False, 'unmeasured_op_not_counted': unmeasured is False,
            'first_long_recorded_once': first is True and second is False and lc['measured'] is True,
            'low_free_vram_after_experience_refused': A(1500.0, [12.0], [20.0], 2, min_free_after_exp_gib=5.9)[0] is False,
            'enough_free_vram_admitted': A(1500.0, [12.0], [20.0], 2, min_free_after_exp_gib=6.0)[0] is True,
            'partial_matrix_never_pass': verdict883({}, REQUIRED_CELLS883, True, True)['result'] == 'TECHNICAL_BLOCK'}


def locked_budget_left884(t0, minutes):
    # sandbox copy of the LOCKED budget_left865 (taken from the engine body by AST, unmodified) with its own T0 / minutes
    node = next(n for n in _a883.parse(ENGINE883['body']).body if isinstance(n, _a883.FunctionDef) and n.name == 'budget_left865')
    clock = {'now': 0.0}
    sb = {'time': type('Clock', (), {'perf_counter': staticmethod(lambda: clock['now'])}), 'T0_865': t0, 'TEST865_MINUTES': minutes,
          'int': int}
    exec(compile(_a883.Module([node], []), 'test870.py:budget_left865', 'exec'), sb)
    return sb['budget_left865'], clock


def st_clock884():
    # fix 1 (CPU): R3 TypeError reproduced on T0_865=None; explicit init gives a real bool at the total deadline
    res = {}
    f, clk = locked_budget_left884(None, 110.0); clk['now'] = 5.0
    try: f({'CALL_CAP849': 3048, 'CALLS849': 48}, 1); res['r3_typeerror_reproduced'] = False
    except TypeError as exc: res['r3_typeerror_reproduced'] = "'float' and 'NoneType'" in str(exc)
    plan = g2_budget_plan883(1215.0, 0.0, 4500.0)
    res['remaining_3285_s'] = plan['remaining_total_s'] == 3285.0
    res['minutes_54_75'] = abs(plan['TEST865_MINUTES'] - 54.75) < 1e-7 and plan['TEST865_MINUTES'] < 54.75
    f, clk = locked_budget_left884(plan['T0_865'], plan['TEST865_MINUTES'])
    env = {'CALL_CAP849': 10, 'CALLS849': 9}
    clk['now'] = 4499.99; res['total_4499_99_true'] = f(env, 1) is True
    clk['now'] = 4500.00; res['total_4500_00_false'] = f(env, 1) is False
    clk['now'] = 1300.0; res['returns_bool'] = type(f(env, 1)) is bool
    res['calls_cap10_used9_need1_true'] = f({'CALL_CAP849': 10, 'CALLS849': 9}, 1) is True
    res['calls_exhausted_false'] = f({'CALL_CAP849': 10, 'CALLS849': 10}, 1) is False
    res['no_time_left_none'] = g2_budget_plan883(4500.0, 0.0, 4500.0) is None and g2_budget_plan883(4600.0, 0.0, 4500.0) is None
    res['phase_never_looser_than_total'] = all(
        plan_['T0_865'] + plan_['TEST865_MINUTES'] * 60.0 <= 0.0 + 4500.0 for plan_ in
        [g2_budget_plan883(t, 0.0, 4500.0) for t in (0.5, 1215.0, 1215.123456789, 4499.0, 4499.999)])
    one = "try:\n    capture_source883()\n    T0_865 = 1\n    TEST865_MINUTES = 2\n    rearm_budget865(e)\n    episode883(e)\nexcept Exception:\n    pass\n"
    two = one.replace("    rearm_budget865(e)\n", "    rearm_budget865(e)\n    rearm_budget865(e)\n")
    early = one.replace("    T0_865 = 1\n    TEST865_MINUTES = 2\n    rearm_budget865(e)\n", "    rearm_budget865(e)\n    T0_865 = 1\n    TEST865_MINUTES = 2\n")
    after = one.replace("    rearm_budget865(e)\n    episode883(e)\n", "    episode883(e)\n    rearm_budget865(e)\n")
    co = lambda src: clock_order883(_a883.parse(src))['ok']
    res['clock_order_ok'] = co(one); res['two_rearms_refused'] = not co(two)
    res['rearm_before_T0_refused'] = not co(early); res['rearm_after_probe_refused'] = not co(after)
    r = gate_fail_record883('G2', 'TypeError: x')
    res['fail_record_fields'] = set(r) == {'status', 'wall_s', 'peak_alloc_gib', 'error'} and r['status'] == 'FAIL'
    return res


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
    json_write864('TEST866_d0_causal.json', STATE883['d0'])
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
             'T884_clock': st_clock884, 'T885_evaluator': st_evaluator885, 'M6_math_bank_hdo': st_m6, 'R3_01_mount': st_r3_mount883, 'R3_03_read': st_r3_read883, 'R3_04_budget': st_r3_budget883,
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
    json_write864('TEST866_cpu_selftest.json', {'results': out, 'failed': bad, 'prereg_sha256': PREREG_SHA883})
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


def read_with_experience883(env, B, entry, X, arm, first, card, step, ep_id, cdir, b_tokens):
    # decision reading on [B][E]: CBLIND hides only the C span; VIS reads it through the same masked kernel (TEST881 contract)
    # R3-03: light contract on EVERY read before the model reads (heavy zero-C / trace parity stays first-CBLIND-only)
    why = read_contract883(entry, card, step, ep_id, cdir)
    if why: raise Gate883('READ_CONTRACT %s step %d: %s' % (ep_id, step, why))
    seal0 = full_seal881(B)['all'] if first else None
    n0 = length873(env, B)
    if n0 != b_tokens: raise Gate883('READ_CONTRACT %s step %d: B length %d != %d' % (ep_id, step, n0, b_tokens))
    try:
        cp = load_exp878(env, entry)        # locked: file SHA-256, book id, P, n, body_tokens, tensor SHA (not repeated here)
    except Persist878 as exc:
        raise Gate883('READ_CONTRACT %s step %d: load_exp878 %s' % (ep_id, step, exc))
    q = int(cp['body_tokens'])
    if q != int(entry['body_tokens']): raise Gate883('READ_CONTRACT body_tokens %d != %s' % (q, entry['body_tokens']))
    g = append_exp878(env, B, cp); ffe883(q, 80, 'experience_mount')
    sp = entry['provenance']['spans_body']; C = [n0 + sp['C'][0], n0 + sp['C'][1]]
    rec = {'cartridge': entry['id'], 'positions': [n0, n0 + q], 'C_span': C, 'n_exact': length873(env, g) == n0 + q,
           'C_span_inside_appended_range': n0 <= C[0] < C[1] == n0 + q, 'read_contract': 'PASS',
           'load_exp878_contract': 'file sha256 + book id + P + n + body_tokens + tensor_sha (locked, verified on load)',
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


def exp_op883(ep_id, step, arm, body_tokens, write_s, read_s):
    # R3-04: natural experience work only (no extra forward, no artificial action); body_tokens is the cartridge length
    try: free = round(free_gib881(), 2)
    except Exception: free = None
    op = {'episode_id': ep_id, 'step': step, 'arm': arm, 'body_tokens': body_tokens, 'write_s': write_s, 'read_s': read_s,
          'free_gib_after': free, 'peak_alloc_gib': round(STATE883['budget']['peak_alloc_gib'], 3)}
    STATE883['budget']['exp_ops'].append(op)
    if long_update883(STATE883['budget']['long_cartridge'], op): line883('LONG_CARTRIDGE_FIRST_MEASURED', _j883.dumps(op))
    return op


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
            rm, _ = mount865(env, spec['initial'], 'TEST866_LR_%s_%s' % (arm, spec['item']))
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
            ctx['memx'], mount = mount865(env, ctx['M'], 'TEST866_L0_%s_%s' % (arm, spec['item'])); ctx['mount_records'].append(mount)
            initial_seal = prefix_seals865(env, ctx['memx'])
            out['start'] = {'bank_sha256': sha256_bytes864(_j883.dumps(sorted((c, env['entries'][c]['sha256']) for c in spec['pool'])).encode()),
                            'bank_size': len(spec['pool']), 'initial': list(spec['initial']), 'initial_seal': initial_seal,
                            'memory_tokens': length873(env, ctx['memx']), 'cartridge_dir_empty': not _o883.listdir(cdir)}
            while out['end'] is None:
                if ctx['steps'] >= horizon: out['end'] = 'HORIZON_%d' % horizon; break
                if not budget_left865(env, STEP_CALLS867): out['end'] = 'RESOURCE_BUDGET'; break
                guard883('%s_t%d' % (ep_id, ctx['steps'] + 1)); ts = time.perf_counter(); step_calls0 = int(env['CALLS849'])
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
                    w_s = None
                    if pending is not None:
                        c_rows, e_rows = state['segments'][0][1], state['segments'][1][1]; tw = time.perf_counter()
                        last_entry, wrec = write_experience883(env, pending, c_rows, e_rows, cdir, dict(
                            key, step_written=ctx['steps'] - 1, episode_prev_cartridge=None if not out['cartridges'] else out['cartridges'][-1]['id']))
                        out['cartridges'].append(wrec); st['experience_written'] = wrec['id']; pending = None
                        w_s = round(time.perf_counter() - tw, 3)
                        if arm == 'REC':                     # Stage 1 history: commit the recorded experience to the bank
                            if REC_SINK883 is None: raise Gate883('REC_WITHOUT_BANK_SINK')
                            st['bank_commit'] = REC_SINK883(last_entry, wrec, out['steps'][-1], key)
                    if arm == 'REC':
                        # REC = natural NOFB decision (locked car867 inside control_step867); the experience is recorded, never read
                        reading = record['reading']
                        if out['step1_parity'] is None: out['step1_parity'] = st['car873_equals_car867']
                        st['decision'] = {'memory': 'B', 'path': 'locked car867 inside control_step867 (REC: recorded, not read)'}
                    elif last_entry is None:
                        reading = xcar878(env, B, X, (), False); ffe883(int(X.shape[0]) + cont_tokens881(), 80, 'decision_read')
                        out['step1_parity'] = step1_parity883(reading, record['reading'])   # Gate883 on any difference (C2)
                        st['decision'] = {'memory': 'B (no experience yet)', 'path': 'xcar878 blind=()', 'step1_parity': True}
                    else:
                        tr = time.perf_counter()
                        reading, rrec = read_with_experience883(env, B, last_entry, X, arm, not out['first_read_done'],
                                                                out['cartridges'][-1], ctx['steps'], ep_id, cdir, st['B_tokens'])
                        out['first_read_done'] = True
                        st['exp_op'] = exp_op883(ep_id, ctx['steps'], arm, int(last_entry['body_tokens']), w_s,
                                                 round(time.perf_counter() - tr, 3))
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
                st['seconds'] = round(time.perf_counter() - ts, 3); st['calls'] = int(env['CALLS849']) - step_calls0; step_sum += st['seconds']
                out['steps'].append(st)
                if EPISODE_OBSERVER883 is not None:          # B04: post-commit observer; OFF = None = no observation at all
                    try: EPISODE_OBSERVER883(ep_id, _j883.loads(_j883.dumps(jsafe878(st), sort_keys=True, default=str)))
                    except Exception as exc_obs: out.setdefault('observer_errors', []).append('%s: %s' % (type(exc_obs).__name__, exc_obs))
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
                'cartridges_expected': exp_cards,
                # R3-02: also from the real CONTROL sequence: nonterminal CONTROL i followed by a CONTROL i+1
                'control_transitions': sum(1 for i, c_ in enumerate(controls[:-1]) if c_['action'] not in TERMINAL883),
                'cartridge_cardinality_ok': exp_cards is not None and len(out['cartridges']) == exp_cards and (
                    arm == 'NOFB' or exp_cards == sum(1 for i, c_ in enumerate(controls[:-1]) if c_['action'] not in TERMINAL883)),
                'mount_integrity': mount_ok883(ctx['mount_records'])})   # R3-01: includes exact_restore_vs_first_mount is not False
    out['seconds'] = round(time.perf_counter() - t0, 1); out['calls'] = int(env['CALLS849']) - calls0   # episode total
    out['step_calls_sum'] = sum(s_['calls'] for s_ in out['steps']); out['primary_failure'] = None if natural_end883(out['end'], horizon) \
        else {'end': out['end'], 'error': out['error']}
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
        if bad['end']:   # fix 3: one primary failure; the other flags follow from it and are not independent findings
            raise Gate883('EPISODE_INTEGRITY %s PRIMARY=%s: %s | consequential_flags=%s' % (
                ep_id, out['end'], str(out['error'])[:300], sorted(k for k, v in bad.items() if v and k != 'end')))
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


def offline883(env, vault, by_key):
    # G5, after every live work. Entry = the single evaluator path evaluator_env885 (also used by the budget-stop fallback):
    # isolated oenv + the same locked installer re-run on it. No runtime function reads oenv.
    oenv, ev = evaluator_env885(env, vault, OFFLINE_DIGEST_G1_885, VAULT_FP885)
    STATE883['evaluator_g5'] = ev
    line883('G5_EVALUATOR', _j883.dumps(ev, default=str))
    scores = episode_scores885(oenv, by_key, STATE883['episodes'])
    fixture = fixture_scores885(oenv, by_key, _j883.loads(_g883.decompress(RAW_SOURCES864['869_full_records.json.gz'])))
    for key, cell in STATE883['cells'].items():
        for a in ARMS883:
            sc = scores.get('%s_%s_%s' % (a, cell['world'], cell['cond']))
            cell['Y'][a] = None if sc is None else sc['Y']
    out = {'episodes': scores, 'fixture_869_success_by_arm_condition': fixture, 'completeness': g5_complete885(scores, fixture),
           'evaluator': 'locked success867 (MISSING: MODEL_STOP; else correct867 -> supported851), separate offline env with '
                        'the locked evaluator re-installed on it (globals = oenv)', 'evaluator_g5': ev,
           'after_all_live_work': True, 'live_env_has_oracle_keys': bool(set(ORACLE_ENV_KEYS883) & set(env))}
    STATE883['offline'] = out; json_write864('offline_scores.json', out)
    return out


def admit883(stage, remaining_episodes):
    b = STATE883['budget']; lc = b['long_cartridge']; steps = b['step_seconds'] + b['nofb_step_seconds']
    frees = [o['free_gib_after'] for o in b['exp_ops'] if o.get('free_gib_after') is not None]
    ok, proj = cell_admission883(time.perf_counter() - T_START883, steps, b['episode_overhead_s'], remaining_episodes,
                                 min_free_after_exp_gib=min(frees) if frees else None, long_measured=lc['measured'])
    basis = 'LONG_CARTRIDGE_MEASURED' if lc['measured'] else 'LONG_CARTRIDGE_NOT_YET_MEASURED (probe + measured steps; not exact)'
    b['admissions'].append({'stage': stage, 'remaining_episodes': remaining_episodes, 'projected_s': proj, 'admitted': ok,
                            'worst_step_s': max(steps) if steps else None, 'min_free_after_exp_gib': min(frees) if frees else None,
                            'basis': basis, 'long_threshold_body_tokens': lc['threshold_body_tokens']})
    if not ok:
        raise Budget883('ADMISSION_REFUSED %s: projected %s s for %d remaining episodes (wall %.0f s), min free after experience '
                        '%s GiB (min %.1f), history %d steps, %s' % (stage, proj, remaining_episodes, WALL_S883,
                                                                    min(frees) if frees else None, FREE_MIN_GIB883, len(steps), basis))


def report883():
    print('=' * 112)
    print('TEST866 | GPU %s | head %s | cell %s | prereg %s' % (CC_GPU.get('name'), HEAD883[:12], STATE883['source'].get(
        'executed_cell_git_blob'), PREREG_SHA883[:16]))
    for g, v in STATE883['gates'].items():
        print('GATE %-3s %-6s wall=%ss peak=%s %s' % (g, v.get('status', 'NA'), v.get('wall_s', 'NA'), v.get('peak_alloc_gib', 'NA'),
                                                    '' if not v.get('error') else 'error=' + str(v['error'])[:200]))
    for k in ('g2_budget_init', 'clocks_final'):
        if STATE883.get(k): print(k.upper(), _j883.dumps(STATE883[k], default=str)[:900])
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
    print('LONG_CARTRIDGE', _j883.dumps(b['long_cartridge'], default=str)[:500], '| experience ops', len(b['exp_ops']),
          '| max read_s', max([o['read_s'] for o in b['exp_ops'] if o.get('read_s') is not None] or [0.0]))
    if STATE883['model_contract']: print('MODEL_CONTRACT', _j883.dumps(STATE883['model_contract'], default=str)[:700])
    if STATE883['not_run']: print('NOT_RUN', STATE883['not_run'])
    r = STATE883['result'] or {'result': 'TECHNICAL_BLOCK', 'reason': 'no result'}
    if r.get('incomplete'): print('INCOMPLETE_CELLS', _j883.dumps(r['incomplete'])[:900])
    print('ESTIMAND incremental cartridge-C channel (VIS vs CBLIND) | content specificity NOT_TESTED | persistent learning NOT_TESTED')
    print('TEST866 RESULT %s | %s | labels %s' % (r['result'], r.get('reason'), r.get('labels')))
    print('status %s (run status, separate from the scientific result) | wall %.0f s | GPU_RUN_THIS_TEST if this console is from a '
          'Colab run; GPU_NOT_RUN_BY_AUTHOR (cell author)' % (STATE883['status'], time.perf_counter() - T_START883))
    print('=' * 112)


# =====================================================================================================================
# TEST866 / M6-S01 — Stage 0 (mechanical gates S0A-S0G) and, automatically in the same run when Stage 0 and the Stage-1
# readiness / preseal gates pass, Stage 1 (content-specific native readability). HDO stdout + immutable disk log.
# No training, no gradients, no registered hooks, no output_hidden_states, no oracle routing, no forced action: every live
# decision is the locked car867 reading inside control_step867, executed by the locked execute866 (via episode883).
# Diagnostic readings run on pre-action snapshots, never execute an action (OUTCOME=NOT_EXECUTED) and never write the bank.
# =====================================================================================================================
import os as _o6, json as _j6, hashlib as _h6, time as _t6, math as _mt6, random as _rd6, zipfile as _zf6

M6_MARK = 'TEST866 / M6-S01'
HDO_MODE_M6 = 'FULL'                     # locked before the run: SUMMARY | FULL | RAW
HDO_CAP_M6 = {'SUMMARY': 600, 'FULL': 4000, 'RAW': None}
ACTIONS_M6 = ('ADVANCE', 'ACQUIRE', 'REJECT', 'BACKTRACK', 'ACCEPT', 'STOP')
SLOTS_M6 = 8                              # CUT3 slots (8 x 32768 B raw) for the S0 probe and for every Stage-1 slot set
ROW_BYTES_M6 = 8192 * 2 + 4 * 2 * 8 * 128 * 2   # H3 BF16[8192] + layers 0-3 K,V BF16[8,128] = 32768
GATE_TOL_CAP_M6 = 0.05                    # sealed cap (nats): explicit-mask vs implicit-mask kernel difference
ROPE_REL_CAP_M6 = 1e-2                    # sealed cap: K canonical round-trip relative error (bf16)
BLOCK_REL_TOL_M6 = 1e-4                   # float32 exact block identity tolerance
EPS_FLOOR_M6 = 0.02                       # sealed floor (nats) of epsilon_num
EPS_MULT_M6 = 3.0                         # epsilon_num = max(floor, 3 x worst Stage-0 numerical delta)
ADMIT_H3_RANGE_M6 = (0.25, 4.0)           # slot H3 norm / median source-row H3 norm
ADMIT_LOGIT_PAD_M6 = 2.0                  # nats added to the Stage-0 probe excess (slot max logit - native q99)
ADMIT_RATIO_MULT_M6, ADMIT_RATIO_MIN_M6 = 4.0, 0.25
RAM_MIN_GIB_M6, DISK_NEED_GIB_M6 = 8.0, 3.0
EXPECTED_ENV_M6 = {   # canonical strings: EXPECTED_SIGNATURES865 (locked engine) where present, else the 886 A100 run (HDO/01)
    'make_x851': '(pre, segments, post)', 'gen851': '(memx, pre, segments, post)', 'cache_build': '(kvs)',
    'native_append_direct': '(memory, cp, strict_sha=True)', 'embed841': '(ids)', 'to_gpu': '(cp)'}
STATE_M6 = {'gates': {}, 'measure': {}, 'verdict': None, 'stage1': 'NOT_RUN', 'anomalies': [], 'cleanup_errors': [],
            'hdo_s': 0.0}


# ----------------------------------------------------------------------------------------------------- HDO (stdout)
def hdo_canon_m6(payload):
    return _j6.dumps(payload, sort_keys=True, default=str, separators=(',', ':'))


class HDO_M6:
    # each record: monotone HDO_SEQ, section, event/episode/step, PRE_SHA (payload), POST_SHA (chain), PARENT_SEAL
    def __init__(self, mode, path, enabled=True):
        assert mode in HDO_CAP_M6, ('HDO_MODE', mode)
        self.mode, self.path, self.enabled = mode, str(path), enabled
        self.seq, self.parent, self.lines, self.closed = 0, '0' * 64, 0, False
        self.f = open(self.path, 'a', encoding='utf-8')

    def emit(self, section, name, payload, event='-', episode='-', step='-'):
        t0 = _t6.perf_counter()
        body = hdo_canon_m6(payload)
        pre = _h6.sha256(body.encode()).hexdigest()
        self.seq += 1
        post = _h6.sha256(('%s|%d|%s|%s|%s' % (self.parent, self.seq, section, name, pre)).encode()).hexdigest()
        head = 'HDO/%s %s SEQ=%d EVENT=%s EP=%s STEP=%s PRE_SHA=%s POST_SHA=%s PARENT_SEAL=%s' % (
            section, name, self.seq, event, episode, step, pre[:16], post[:16], self.parent[:16])
        self.f.write(head + ' ' + body + '\n'); self.lines += 1
        cap = HDO_CAP_M6[self.mode]
        if self.enabled:
            if cap is None or len(body) <= cap: print(head, body, flush=True)
            else:
                parts = [body[i:i + cap] for i in range(0, len(body), cap)]
                print(head, 'BLOCKS=%d' % len(parts), flush=True)
                for i, p in enumerate(parts): print('HDO/%s %s SEQ=%d BLOCK=%d/%d %s' % (section, name, self.seq, i + 1, len(parts), p), flush=True)
        self.parent = post
        STATE_M6['hdo_s'] += _t6.perf_counter() - t0
        return post

    def close(self):
        self.f.flush(); _o6.fsync(self.f.fileno()); self.f.close(); self.closed = True
        data = open(self.path, 'rb').read()
        return {'path': self.path, 'bytes': len(data), 'sha256': _h6.sha256(data).hexdigest(), 'last_seq': self.seq, 'lines': self.lines}


def hdo_verify_chain_m6(path):
    # recompute every POST_SHA from the disk log; malformed / truncated lines are a structured failure, never an exception
    parent, seq, ok, bad = '0' * 64, 0, True, []
    for ln, line in enumerate(open(path, encoding='utf-8'), 1):
        try:
            if ' {' not in line or not line.endswith('\n'): raise ValueError('NO_PAYLOAD_OR_TRUNCATED')
            head, body = line.rstrip('\n').split(' {', 1); body = '{' + body
            _j6.loads(body)
            f = head.split(' '); section, name = f[0][4:], f[1]
            kv = dict(x.split('=', 1) for x in f[2:])
            pre = _h6.sha256(body.encode()).hexdigest(); seq += 1
            post = _h6.sha256(('%s|%d|%s|%s|%s' % (parent, seq, section, name, pre)).encode()).hexdigest()
            good = int(kv['SEQ']) == seq and kv['PRE_SHA'] == pre[:16] and kv['POST_SHA'] == post[:16] and kv['PARENT_SEAL'] == parent[:16]
            if not good: bad.append(ln)
            ok = ok and good; parent = post
        except (ValueError, KeyError, IndexError) as exc:
            ok = False; bad.append('%d:%s' % (ln, type(exc).__name__))
    return {'ok': ok and seq > 0, 'records': seq, 'bad_lines': bad[:20]}


# ------------------------------------------------------------------------------------- append-only bank (SSD, atomic)
class Bank_M6:
    # payload -> temp -> flush/fsync -> SHA verify -> atomic rename -> dir fsync -> manifest (parent SHA, fsync) -> readback.
    # A file not bound to the manifest is never a member. cleanup_orphans removes only *.tmp; a non-member final file (crash
    # after rename, before manifest) is QUARANTINE: reported, never deleted. Nothing committed is deleted.
    def __init__(self, root):
        self.root = str(root); _o6.makedirs(self.root, exist_ok=True)
        self.manifest = _o6.path.join(self.root, 'manifest.jsonl')
        if not _o6.path.exists(self.manifest): open(self.manifest, 'a').close()

    def parse(self):
        ents, bad = [], []
        raw = open(self.manifest, 'rb').read()
        if raw and not raw.endswith(b'\n'): bad.append('TRUNCATED_LAST_LINE')
        for i, l in enumerate(raw.splitlines()):
            if not l.strip(): continue
            try:
                e = _j6.loads(l.decode())
                if not all(k in e for k in ('name', 'sha256', 'bytes', 'parent_manifest_sha256', 'seq', 'meta')): raise KeyError('FIELDS')
                ents.append(e)
            except (ValueError, KeyError, UnicodeDecodeError) as exc:
                bad.append('LINE_%d_%s' % (i + 1, type(exc).__name__))
        return ents, bad

    def entries(self):
        ents, bad = self.parse()
        if bad: raise Gate883('BANK_MANIFEST_MALFORMED %s' % bad)
        return ents

    def head_sha(self):
        return _h6.sha256(open(self.manifest, 'rb').read()).hexdigest()

    def commit(self, name, data, meta):
        assert '/' not in name and not name.endswith('.tmp') and name != 'manifest.jsonl', ('BANK_NAME', name)
        ents = self.entries()
        final = _o6.path.join(self.root, name); tmp = final + '.tmp'
        assert not _o6.path.exists(final) and name not in {e['name'] for e in ents}, ('BANK_APPEND_ONLY_DUPLICATE_NAME', name)
        eid = (meta or {}).get('event_id')
        assert eid is None or eid not in {e['meta'].get('event_id') for e in ents}, ('BANK_DUPLICATE_EVENT_ID', eid)
        sha = _h6.sha256(data).hexdigest()
        with open(tmp, 'wb') as f:
            f.write(data); f.flush(); _o6.fsync(f.fileno())
        if _h6.sha256(open(tmp, 'rb').read()).hexdigest() != sha: raise Gate883('BANK_TEMP_SHA ' + name)
        _o6.replace(tmp, final)
        dfd = _o6.open(self.root, _o6.O_RDONLY)
        try: _o6.fsync(dfd)
        finally: _o6.close(dfd)
        rec = {'name': name, 'sha256': sha, 'bytes': len(data), 'parent_manifest_sha256': self.head_sha(), 'meta': meta,
               'seq': len(ents) + 1}
        with open(self.manifest, 'a', encoding='utf-8') as f:
            f.write(_j6.dumps(rec, sort_keys=True, default=str) + '\n'); f.flush(); _o6.fsync(f.fileno())
        back = open(final, 'rb').read()
        if _h6.sha256(back).hexdigest() != sha or self.entries()[-1]['sha256'] != sha: raise Gate883('BANK_READBACK ' + name)
        return rec

    def verify(self):
        ents, bad = self.parse()
        raw = open(self.manifest, 'rb').read().splitlines(keepends=True)
        parent_ok, files_ok = not bad, not bad
        for i, e in enumerate(ents):
            parent_ok = parent_ok and e['parent_manifest_sha256'] == _h6.sha256(b''.join(raw[:i])).hexdigest() and e['seq'] == i + 1
            p = _o6.path.join(self.root, e['name'])
            files_ok = files_ok and _o6.path.exists(p) and _h6.sha256(open(p, 'rb').read()).hexdigest() == e['sha256']
        members = {e['name'] for e in ents}
        names = [e['name'] for e in ents]
        others = sorted(n for n in _o6.listdir(self.root) if n != 'manifest.jsonl' and n not in members)
        tmp_orphans = [n for n in others if n.endswith('.tmp')]
        quarantine = [n for n in others if not n.endswith('.tmp')]
        out = {'entries': len(ents), 'parent_chain_ok': parent_ok, 'files_ok': files_ok, 'malformed': bad,
               'duplicate_names': len(names) != len(set(names)), 'tmp_orphans': tmp_orphans, 'quarantine': quarantine,
               'manifest_sha256': self.head_sha()}
        out['ok'] = bool(parent_ok and files_ok and not bad and not out['duplicate_names'] and not tmp_orphans and not quarantine)
        return out

    def cleanup_orphans(self):
        ents, bad = self.parse()
        if bad: return []                                        # malformed manifest: touch nothing
        members = {e['name'] for e in ents}
        gone = []
        for n in sorted(_o6.listdir(self.root)):
            if n.endswith('.tmp') and n[:-4] not in members:
                _o6.remove(_o6.path.join(self.root, n)); gone.append(n)
        return gone


# ------------------------------------------------------------------------------------ pure math (CPU self-tests)
def count_update_m6(N, gamma):
    assert gamma in (0, 1), ('ELIGIBILITY', gamma)
    return N + gamma                                             # never minus


def log_posterior_update_m6(logw, logp_obs, gamma):
    a = [lw + gamma * lp for lw, lp in zip(logw, logp_obs)]      # never minus
    m = max(a); z = m + _mt6.log(sum(_mt6.exp(x - m) for x in a))
    return [x - z for x in a]


def gated_block_m6(sB, vB, sC, vC, g):
    # exact block form o = (N_B + g N_C) / (Z_B + g Z_C). B12: empty base, non-finite inputs, negative g and a zero
    # denominator are explicit failures (ValueError), never a silent NaN
    if not sB: raise ValueError('EMPTY_BASE_BLOCK')
    if not (g >= 0 and _mt6.isfinite(g)): raise ValueError('GATE_NOT_FINITE_NONNEGATIVE')
    if not all(_mt6.isfinite(x) for x in list(sB) + list(sC)): raise ValueError('NONFINITE_SCORE')
    m = max(list(sB) + list(sC))
    zb = sum(_mt6.exp(s - m) for s in sB); zc = sum(_mt6.exp(s - m) for s in sC)
    den = zb + g * zc
    if not den > 0: raise ValueError('ZERO_DENOMINATOR')
    nb = [sum(_mt6.exp(s - m) * v[d] for s, v in zip(sB, vB)) for d in range(len(vB[0]))]
    nc = [sum(_mt6.exp(s - m) * v[d] for s, v in zip(sC, vC)) for d in range(len(vB[0]))] if sC else [0.0] * len(vB[0])
    o = [(a + g * b) / den for a, b in zip(nb, nc)]
    if not all(_mt6.isfinite(x) for x in o): raise ValueError('NONFINITE_OUTPUT')
    return o, (g * zc) / den


def biased_softmax_m6(sB, vB, sC, vC, g):
    s = list(sB) + ([x + _mt6.log(g) for x in sC] if g > 0 else [])
    v = list(vB) + (list(vC) if g > 0 else [])
    m = max(s); w = [_mt6.exp(x - m) for x in s]; z = sum(w)
    return [sum(wi * vi[d] for wi, vi in zip(w, v)) / z for d in range(len(vB[0]))]


def finite_nonneg_m6(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and _mt6.isfinite(x) and x >= 0


def admission_m6(elapsed_s, remaining_units, worst_live_s, worst_diag_s, worst_compile_s, reserve_s, wall_s):
    # B05/B07: every term must be a measured finite non-negative number; all terms are added, never subtracted
    for x in (elapsed_s, remaining_units, worst_live_s, worst_diag_s, worst_compile_s, reserve_s, wall_s):
        if not finite_nonneg_m6(x): raise ValueError('ADMISSION_TERM_INVALID %r' % (x,))
    projected = elapsed_s + remaining_units * (worst_live_s + worst_diag_s + worst_compile_s) + reserve_s   # all terms plus
    return projected <= wall_s, round(projected, 1)


def memory_projection_m6(measured, transient, rebuild, slot, log_overhead, limit):
    for x in (measured, transient, rebuild, slot, log_overhead, limit):
        if not finite_nonneg_m6(x): raise ValueError('MEMORY_TERM_INVALID %r' % (x,))
    total = measured + transient + rebuild + slot + log_overhead
    return total <= limit, round(total, 3)


def stage1_projection_m6(elapsed_s, M, plan, reserve_s, wall_s):
    # per-unit workload of the sealed Stage-1 plan x the worst measured Stage-0 cost of that unit kind; missing -> ValueError
    need = {'live_step': plan['live_steps'], 'compile': plan['compiles'] + plan['live_steps'], 'diag_read': plan['reads'],
            'admissibility': plan['admissibility'], 'snapshot': plan['snapshots']}
    total = float(elapsed_s)
    for k, n in need.items():
        vals = M.get(k)
        if not vals or not all(finite_nonneg_m6(v) for v in vals): raise ValueError('MEASUREMENT_MISSING_%s' % k)
        total += n * max(vals)
    if not finite_nonneg_m6(M.get('hdo_s_total', -1)): raise ValueError('MEASUREMENT_MISSING_hdo')
    total += 2.0 * M['hdo_s_total'] + reserve_s                  # Stage-1 HDO volume bounded by 2 x Stage 0 (sealed)
    return total <= wall_s, round(total, 1)


def six_view_m6(reading):
    sc = {s['word']: float(s['sequence_logp']) for s in reading['scores']}
    assert sorted(sc) == sorted(ACTIONS_M6), ('SIX_ACTIONS', sorted(sc))
    order = sorted(ACTIONS_M6, key=lambda w: (-sc[w], ACTIONS_M6.index(w)))
    return {'logp': {w: sc[w] for w in ACTIONS_M6}, 'full_rank': order, 'mass': reading.get('mass'),
            'margin': reading.get('margin_logp'), 'selected': reading.get('action'),
            'normalized': {w: (reading.get('normalized') or {}).get(w) for w in ACTIONS_M6}}


def directional_d_m6(lp, lp_no, a_plus, a_zero):
    return (lp[a_plus] - lp_no[a_plus]) - (lp[a_zero] - lp_no[a_zero])


def stage1_history_verdict_m6(D, eps, admissible, inert_ok):
    # sealed decision rule for one history j (D: condition -> directional D_j; admissible: condition -> bool)
    if not inert_ok: return 'INCONCLUSIVE', 'inert recompute outside epsilon_num'
    if not admissible.get('TRUE', False): return 'NATIVE_MANIFOLD_REJECT', 'TRUE slot set not admissible'
    if not all(admissible.get(c, False) for c in ('WRONG_OUTCOME', 'SHUFFLED_HISTORY', 'MATCHED_GEOMETRY', 'MEDOID_UNION')):
        return 'INCONCLUSIVE', 'a control slot set is not admissible'
    t, m = D['TRUE'] > eps, D['MEDOID_UNION'] > eps
    if not t and m: return 'SYNTHETIC_G_REJECTED', 'medoid union reads, synthetic barycenter does not'
    if not t and not m: return 'NATIVE_STRUCTURAL_READING_NOT_SUPPORTED', 'neither TRUE nor medoid union exceeds epsilon_num'
    if any(D[c] >= D['TRUE'] - eps for c in ('WRONG_OUTCOME', 'SHUFFLED_HISTORY', 'MATCHED_GEOMETRY')):
        return 'GEOMETRY_OR_NONSPECIFIC_EFFECT', 'a control is within epsilon_num of TRUE'
    if D['ECHO_MASKED'] <= eps: return 'CURRENT_ECHO_EXPLAINS_EFFECT', 'masking the context slots removes the effect'
    return 'SUPPORTED', 'TRUE > eps, controls below TRUE - eps, echo-masked > eps'


def stage1_combine_m6(labels):
    if labels and all(l == 'SUPPORTED' for l in labels): return 'STAGE1_CONTENT_SPECIFIC_NATIVE_READING_SUPPORTED'
    if len(set(labels)) == 1: return labels[0]
    return 'INCONCLUSIVE'


def chunks_m6(a, b, k):
    n = b - a
    if n < k or k < 1: raise ValueError('ROLE_ROWS_FEWER_THAN_SLOTS %d < %d' % (n, k))
    edges = [a + (n * i) // k for i in range(k + 1)]
    return [(edges[i], edges[i + 1]) for i in range(k)]


def medoid_index_m6(dist_rows):
    # dist_rows: square list of distances; the row minimising the sum (ties -> lowest index)
    sums = [sum(r) for r in dist_rows]
    return min(range(len(sums)), key=lambda i: (sums[i], i))


# ------------------------------------------------------------------------- canonical signatures and provenance (B02/B03/B15)
def ast_default_m6(node):
    try: return ('LIT', repr(_a883.literal_eval(node)))
    except (ValueError, TypeError, SyntaxError): return ('EXPR', _a883.unparse(node))


def canon_sig_ast_m6(fnode):
    a, out = fnode.args, []
    pos = list(a.posonlyargs) + list(a.args); nd = len(a.defaults)
    for i, p in enumerate(pos):
        kind = 'POSITIONAL_ONLY' if i < len(a.posonlyargs) else 'POSITIONAL_OR_KEYWORD'
        d = a.defaults[i - (len(pos) - nd)] if i >= len(pos) - nd else None
        out.append((p.arg, kind) + (ast_default_m6(d) if d is not None else ('NO_DEFAULT', None)))
    if a.vararg: out.append((a.vararg.arg, 'VAR_POSITIONAL', 'NO_DEFAULT', None))
    for p, d in zip(a.kwonlyargs, a.kw_defaults):
        out.append((p.arg, 'KEYWORD_ONLY') + (ast_default_m6(d) if d is not None else ('NO_DEFAULT', None)))
    if a.kwarg: out.append((a.kwarg.arg, 'VAR_KEYWORD', 'NO_DEFAULT', None))
    return out


def canon_sig_live_m6(fn):
    import inspect as _in6
    if _in6.ismethod(fn): return 'BOUND_METHOD'
    out = []
    for p in _in6.signature(fn).parameters.values():
        if p.default is _in6.Parameter.empty: d = ('NO_DEFAULT', None)
        else:
            try: d = ('LIT', repr(_a883.literal_eval(repr(p.default))))
            except (ValueError, SyntaxError, TypeError): d = ('EXPR_RUNTIME', type(p.default).__name__)
        out.append((p.name, p.kind.name) + d)
    return out


def sig_str_m6(canon):
    if not isinstance(canon, list): return str(canon)
    parts, star = [], False
    for name, kind, dk, dv in canon:
        if kind == 'KEYWORD_ONLY' and not star: parts.append('*'); star = True
        if kind == 'VAR_POSITIONAL': parts.append('*' + name); star = True; continue
        if kind == 'VAR_KEYWORD': parts.append('**' + name); continue
        parts.append(name + ('' if dk == 'NO_DEFAULT' else '=' + (dv if dk == 'LIT' else '<%s>' % dv)))
    return '(' + ', '.join(parts) + ')'


def code_names_m6(code):
    names = set(code.co_names) | set(code.co_varnames)
    for c in code.co_consts:
        if hasattr(c, 'co_names'): names |= code_names_m6(c)
    return names


def provenance_m6(fn):
    # B15: binding provenance of a live callable, and oracle reachability through its code, globals and closure cells
    import inspect as _in6
    oracle = set(ORACLE883) | set(ORACLE_ENV_KEYS883)
    fn = _in6.unwrap(fn)                                     # decorated callables (e.g. torch.no_grad) -> the real function
    code = fn.__code__; g = fn.__globals__
    cells = []
    for c in (fn.__closure__ or ()):
        try: v = c.cell_contents
        except ValueError: v = None
        cells.append(v)
    closure_hits = []
    for v in cells:
        if isinstance(v, dict) and set(v) & set(ORACLE_ENV_KEYS883): closure_hits.append('DICT_WITH_ORACLE_KEYS')
        if callable(v) and getattr(v, '__name__', '') in oracle: closure_hits.append('ORACLE_CALLABLE:' + v.__name__)
    return {'co_name': code.co_name, 'co_filename': code.co_filename, 'firstlineno': code.co_firstlineno,
            'code_sha256': _h6.sha256(_ms885.dumps(code)).hexdigest(), 'globals_id': id(g), 'closure_cells': len(cells),
            'oracle_names_in_code': sorted(code_names_m6(code) & oracle), 'oracle_keys_in_globals': sorted(set(g) & set(ORACLE_ENV_KEYS883)),
            'oracle_in_closure': closure_hits}


def locked_defs_m6(names, sources):
    # every FunctionDef in `names` found in the locked source texts, top level or inside embedded string bodies (one parse per file)
    hits = {n: [] for n in names}
    for fname, text in sources:
        if not any(('def %s(' % n) in text for n in names): continue
        try: tree = _a883.parse(text)
        except SyntaxError: continue
        for node in _a883.walk(tree):
            if isinstance(node, _a883.FunctionDef) and node.name in hits: hits[node.name].append((fname, node))
            elif isinstance(node, _a883.Constant) and isinstance(node.value, str) and any(('def %s(' % n) in node.value for n in names):
                try:
                    for m in _a883.walk(_a883.parse(node.value)):
                        if isinstance(m, _a883.FunctionDef) and m.name in hits: hits[m.name].append((fname + ':literal', m))
                except SyntaxError: pass
    return hits


# ------------------------------------------------------------------------- GPU: explicit, hook-free, gate-capable path
def m6_mask_bias(mask, L, nc, cols, logg, dtype, dev):
    # additive score bias on the C block columns: s' = s + log(g) (g > 0) or -> finfo.min (g = 0). mask None = implicit
    # causal SDPA; it is materialised here only when a bias is requested (kernel path then differs: measured, not hidden)
    neg = torch.finfo(dtype).min
    if mask is not None and mask.dtype == torch.bool:     # boolean SDPA mask (True = attend) -> additive form
        mask = torch.where(mask, torch.zeros((), dtype=dtype, device=dev), torch.full((), neg, dtype=dtype, device=dev))
    if mask is None:
        i = torch.arange(L, device=dev).unsqueeze(1); j = torch.arange(nc + L, device=dev).unsqueeze(0)
        mask = torch.where(j <= nc + i, torch.zeros((), dtype=dtype, device=dev), torch.full((), neg, dtype=dtype, device=dev))
        mask = mask.reshape(1, 1, L, nc + L)
    else:
        mask = mask.clone()
    for a, b in cols:
        if logg is None: continue
        if logg == float('-inf'): mask[:, :, :, a:b] = neg
        else: mask[:, :, :, a:b] = mask[:, :, :, a:b] + torch.tensor(logg, dtype=dtype, device=dev)
    return mask


def m6_xspan(env, cache, h, am, lo, hi, cols=(), logg=None):
    # = locked xspan878 (no lower / restore), plus the optional additive C-block bias; with logg None the code path is the
    # locked one statement for statement
    base = env['model'].model
    cfg = base.config
    L, nc = (int(h.shape[1]), int(cache.get_seq_length()))
    assert int(am.shape[1]) == nc + L, ('MASK_LENGTH', int(am.shape[1]), nc, L)
    pos = torch.arange(nc, nc + L, device=env['DEV'])
    pid = pos.unsqueeze(0)
    with torch.no_grad():
        mask = MOD877['mask'](config=cfg, inputs_embeds=h, attention_mask=am, past_key_values=cache, position_ids=pid)
        pe = base.rotary_emb(h, pid)
        if logg is not None and cols:
            mask = m6_mask_bias(mask, L, nc, cols, logg, h.dtype, env['DEV'])
        for layer in base.layers[lo:hi]:
            res = h
            a = xattn877(layer.self_attn, layer.input_layernorm(h), pe, mask, cache, pid, pos, None, None, None)
            h = res + a
            res = h
            h = res + layer.mlp(layer.post_attention_layernorm(h))
    return h


def m6_car(env, kv, X, cols=(), logg=None):
    # = locked xcar878 with blind=(), sham=False, reading through m6_xspan (optional C-block gate). Decision rule unchanged:
    # the locked reading867 of the six native action words
    model = env['model']
    cache = env['cache_build'](list(kv))
    n0 = int(cache.get_seq_length())
    env['budget849']()
    n1 = n0 + int(X.shape[0])
    assert n1 + max((len(ids) for _, ids in ACTION_IDS867)) <= int(env['MAX_FUSED_TOKENS']), ('CONTEXT_LIMIT', n1)

    def fwd(Y, last):
        L, nc = (int(Y.shape[0]), int(cache.get_seq_length()))
        am = torch.ones((1, nc + L), device=env['DEV'], dtype=torch.long)
        h = m6_xspan(env, cache, Y.reshape(1, L, int(env['H'])), am, 0, int(env['NL']), cols, logg)
        with torch.no_grad():
            return torch.log_softmax(model.lm_head(model.model.norm(h))[0, -last:].float(), dim=-1)
    first = fwd(X, 1)[0]
    scores = []
    for word, ids in ACTION_IDS867:
        token_logps = [float(first[ids[0]])]
        if len(ids) > 1:
            m = len(ids) - 1
            lp = fwd(env['embed841'](ids[:-1]), m)
            cache.crop(-m)
            assert int(cache.get_seq_length()) == n1, 'CAR_CROP_LENGTH_MISMATCH_M6'
            token_logps += [float(lp[i, ids[i + 1]]) for i in range(m)]
            del lp
        scores.append({'word': word, 'ids': ids, 'token_logps': token_logps, 'sequence_logp': float(sum(token_logps)), 'hard_greedy_ids': []})
    top = torch.topk(first, 10)
    del cache
    return reading867({'scores': scores, 'path': 'CROP', 'fallback_reason': None, 'first_top10': {'ids': [int(i) for i in top.indices.tolist()]}, 'X_sha256': None})


def snapshot_m6(env, spec, tag):
    # pre-action step-1 snapshot built by the same locked calls as episode883 step 1 (mount865, hop865, feedback867,
    # control_step867, make_x851). No action is executed. Returns B (owned), X, the locked native reading and seals.
    ctx = {'spec': spec, 'arm': 'NO_FEEDBACK', 'M': list(spec['initial']), 'memx': None, 'path': [], 'prev_state': None,
           'own_states': [], 'events': [], 'mount_records': [], 'acquisitions': 0, 'rejections': 0, 'addresses': 0,
           'steps': 0, 'hops': 0, 'donor_item': None}
    q = env['QTEXT841'][spec['qid']]; pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
    c0 = int(env['CALLS849'])
    ctx['memx'], mount = mount865(env, ctx['M'], 'T866_%s' % tag)
    try:
        h, kind = hop865(env, ctx['memx'], spec['qid'], 0, None)
        if kind == 'EMPTY_OUTPUT': raise Gate883('SNAPSHOT_EMPTY_HOP')
        feedback, _ = feedback867(env, ctx)
        control, record, state = control_step867(env, ctx, h, None, feedback)
        if control is None: raise Gate883('SNAPSHOT_EMPTY_STATE')
        X, _ = env['make_x851'](pre, state['segments'], post)
        B = list(kv873(env, env['cache_build'](list(ctx['memx']))))
        snap = {'B': B, 'X': X, 'record': record, 'hop': h['text'], 'mount': mount, 'state_sha256': record['state_sha256'],
                'X_sha256': tsha881(X), 'B_tokens': length873(env, B), 'B_seal': full_seal881(B)['all'],
                'c_rows_sha256': env['stats849'](state['segments'][0][1])['sha256'], 'calls': int(env['CALLS849']) - c0}
    finally:
        free865(env, ctx['memx']); ctx['memx'] = None
    return snap


def cut3_rows_m6(env, snap, r):
    # CUT3 rows of the first r rows of X over [B]: layers 0-3 K/V (native forward) + H3 (explicit layers 0-3)
    cut, Hd, dev = APPEND873['CUT'], int(env['H']), env['DEV']
    B, X = snap['B'], snap['X']; n2 = length873(env, B); Xr = X[:r]
    own = env['cache_build'](list(B)); forward873(env, own, Xr, n2); gH = kv873(env, own); del own
    cl = env['cache_build'](list(B))
    h3 = m6_xspan(env, cl, Xr.reshape(1, r, Hd), torch.ones((1, n2 + r), device=dev, dtype=torch.long), 0, cut + 1)
    ck = {'lower_explicit_equals_native': all(torch.equal(a[:, :, n2:], b[:, :, n2:n2 + r]) for i in range(cut + 1)
                                              for a, b in zip(cache_kv870(cl, i), gH[i])),
          'h3_next_layer_equals_native': all(torch.equal(a, b[:, :, n2:n2 + r]) for a, b in zip(next_kv878(env, h3, n2), gH[cut + 1]))}
    del cl
    return gH, h3, n2, ck


def gate_block_gpu_m6(env, G, X, c0, c1, gs=(0.0, 0.5, 1.0, 2.0)):
    # layer-0 exact attention check on real model tensors (float32): q from the module projections (no hook), keys/values
    # from [G] + X; the SAME bias builder as the CAR path; block identity, slot-mass monotonicity, admissibility statistics.
    # B12: empty base / empty C / non-finite scores / zero normaliser are explicit structured failures
    base = env['model'].model; sa = base.layers[0].self_attn; dev = env['DEV']
    if not (0 < c0 < c1): return {'block_identity_ok': False, 'mass_monotone_and_g0_zero': False, 'reason': 'EMPTY_BASE_OR_EMPTY_C'}
    cache = env['cache_build'](list(G))
    try:
        nc = int(cache.get_seq_length()); L = int(X.shape[0])
        with torch.no_grad():
            h = X.reshape(1, L, int(env['H']))
            pid = torch.arange(nc, nc + L, device=dev).unsqueeze(0)
            x = base.layers[0].input_layernorm(h); shp = (1, L, -1, sa.head_dim)
            q = sa.q_proj(x).view(shp).transpose(1, 2); k = sa.k_proj(x).view(shp).transpose(1, 2); v = sa.v_proj(x).view(shp).transpose(1, 2)
            cos, sin = base.rotary_emb(h, pid); q, k = MOD877['rope'](q, k, cos, sin)
            K0, V0 = cache_kv870(cache, 0)
            K = torch.cat([K0, k], dim=2)[0].float(); V = torch.cat([V0, v], dim=2)[0].float(); qd = q[0, :, -1, :].float()
            grp = torch.arange(qd.shape[0], device=dev) // (qd.shape[0] // K.shape[0])
            s = torch.einsum('hd,hnd->hn', qd, K[grp]) * float(sa.scaling)
            Vg = V[grp]
            if not bool(torch.isfinite(s).all()):
                return {'block_identity_ok': False, 'mass_monotone_and_g0_zero': False, 'reason': 'NONFINITE_SCORES'}
            cmask = torch.zeros(s.shape[-1], dtype=torch.bool, device=dev); cmask[c0:c1] = True
            m = s.max(dim=-1, keepdim=True).values
            e = torch.exp(s - m); zb = e[:, ~cmask].sum(-1); zc = e[:, cmask].sum(-1)
            if not bool((zb > 0).all()):
                return {'block_identity_ok': False, 'mass_monotone_and_g0_zero': False, 'reason': 'ZERO_BASE_NORMALISER'}
            nb = torch.einsum('hn,hnd->hd', e[:, ~cmask], Vg[:, ~cmask]); ncc = torch.einsum('hn,hnd->hd', e[:, cmask], Vg[:, cmask])
            out = {'g': {}}; prev_mass = -1.0; mono = True; worst = 0.0
            for g in gs:
                blk = (nb + g * ncc) / (zb + g * zc).unsqueeze(-1)
                row = m6_mask_bias(None, L, nc, [(c0, c1)], _mt6.log(g) if g > 0 else float('-inf'), torch.float32, dev)[0, 0, -1]
                w = torch.softmax(s + row.unsqueeze(0), dim=-1)
                ref = torch.einsum('hn,hnd->hd', w, Vg)
                rel = float((blk - ref).norm() / ref.norm().clamp_min(1e-30))
                mass = float(((g * zc) / (zb + g * zc)).mean())
                if not (_mt6.isfinite(rel) and _mt6.isfinite(mass)): rel = float('inf')
                mono = (mono and mass > prev_mass) if g > 0 else (mono and mass == 0.0)
                prev_mass = mass; worst = max(worst, rel)
                out['g'][str(g)] = {'block_vs_biased_softmax_rel': rel, 'slot_mass_mean': mass}
            sl = s[:, cmask].flatten(); nat = s[:, :c0].flatten()
            qs = torch.quantile(nat, torch.tensor([0.01, 0.5, 0.99], device=dev))
            out.update({'block_identity_ok': worst <= BLOCK_REL_TOL_M6, 'mass_monotone_and_g0_zero': mono,
                        'stats': {'slot_logit_max': float(sl.max()), 'slot_logit_min': float(sl.min()),
                                  'native_q01_q50_q99': [float(x) for x in qs], 'ratio_Zc_over_Zb_mean': float((zc / zb).mean())}})
        return out
    finally:
        del cache


def m6_reading_delta(a, b):
    sa, sb = six_view_m6(a)['logp'], six_view_m6(b)['logp']
    return max(abs(sa[w] - sb[w]) for w in ACTIONS_M6)


# ------------------------------------------------------------------------------------ Stage 1: slot compiler (G)
ROLE_SLOTS_M6 = (('X2', 5), ('A', 1), ('C', 2))          # sealed fixed role-slot counts: CTX / action / outcome = 8 slots


def cp_rows_m6(cp, P, r):
    # one recorded CUT3 row (body index r): H3 (1,H), lower [(K (1,8,1,128) at canonical position P+r, V)] x 4
    return cp['h'][:, P + r:P + r + 1], [(k[:, :, P + r:P + r + 1], v[:, :, P + r:P + r + 1]) for k, v in cp['lower']]


def bary_slot_m6(env, cp, P, a, b):
    # barycenter of recorded rows a..b-1: H3 / V mean; K unrotated to position 0 (RoPE canonicalisation), mean, kept at 0
    rep, dev = APPEND873['rephase'], env['DEV']
    h = cp['h'][:, P + a:P + b].float().mean(dim=1, keepdim=True).to(cp['h'].dtype)
    low = []
    for k, v in cp['lower']:
        kk = rep(k[:, :, P + a:P + b], torch.arange(P + a, P + b, device=dev), torch.zeros(b - a, dtype=torch.long, device=dev))
        low.append((kk.float().mean(dim=2, keepdim=True).to(k.dtype), v[:, :, P + a:P + b].float().mean(dim=2, keepdim=True).to(v.dtype)))
    return {'h': h, 'lower': low, 'pos': 0}


def medoid_slot_m6(env, cp, P, a, b):
    # exact recorded row of a..b-1 minimising the summed H3 L2 distance (ties -> lowest index); K stays at its own position
    hh = cp['h'][0, P + a:P + b].float()
    d = torch.cdist(hh.unsqueeze(0), hh.unsqueeze(0))[0]
    j = medoid_index_m6(d.tolist())
    h, low = cp_rows_m6(cp, P, a + j)
    return {'h': h, 'lower': low, 'pos': P + a + j}


def role_slots_m6(env, cp_ctx, cp_out, P, kind):
    # sealed slot list [X2 x5, A x1, C x2]; X2 and A from cp_ctx, C from cp_out (TRUE: same event; WRONG: other event)
    out = []
    for role, k in ROLE_SLOTS_M6:
        cp = cp_out if role == 'C' else cp_ctx
        a0, b0 = cp['spans_body'][role]
        for a, b in chunks_m6(a0, b0, k):
            out.append((bary_slot_m6 if kind == 'BARY' else medoid_slot_m6)(env, cp, P, a, b))
    return out


def geometry_slots_m6(env, cp_src, P, ref_slots):
    # MATCHED-GEOMETRY: 8 barycenters of the CONTEXT rows of another event, each tensor rescaled to the norm of the
    # corresponding TRUE slot tensor (same count / positions / norms; no action, no outcome content)
    a0, b0 = cp_src['spans_body']['X2']
    out = []
    for (a, b), ref in zip(chunks_m6(a0, b0, SLOTS_M6), ref_slots):
        s = bary_slot_m6(env, cp_src, P, a, b)
        sc = lambda x, y: (x.float() * (y.float().norm() / x.float().norm().clamp_min(1e-30))).to(x.dtype)
        out.append({'h': sc(s['h'], ref['h']), 'lower': [(sc(k, rk), sc(v, rv)) for (k, v), (rk, rv) in zip(s['lower'], ref['lower'])],
                    'pos': 0})
    return out


def assemble_cp_m6(env, slots):
    # 873-format cartridge of len(slots) rows at canonical positions P..P+q-1 (K rotated there from each slot's position)
    P, rep, dev = int(env['P']), APPEND873['rephase'], env['DEV']; q = len(slots)
    hz = torch.zeros((1, P, int(env['H'])), dtype=slots[0]['h'].dtype, device=dev)
    h = torch.cat([hz] + [s['h'] for s in slots], dim=1)
    lower = []
    for li in range(len(slots[0]['lower'])):
        ks = [rep(s['lower'][li][0], torch.tensor([s['pos']], device=dev), torch.tensor([P + i], device=dev)) for i, s in enumerate(slots)]
        vs = [s['lower'][li][1] for s in slots]
        k0 = ks[0]
        z = torch.zeros((int(k0.shape[0]), int(k0.shape[1]), P, int(k0.shape[3])), dtype=k0.dtype, device=dev)
        lower.append((torch.cat([z] + ks, dim=2), torch.cat([z] + vs, dim=2)))
    return {'h': h, 'lower': tuple(lower), 'n': P + q, 'p': P, 'body_tokens': q}


def cp_digest_m6(cp):
    P = int(cp['p'])
    parts = [cp['h'][:, P:]] + [t[:, :, P:] for kv in cp['lower'] for t in kv]
    return _h6.sha256(b''.join(tsha881(t).encode() for t in parts)).hexdigest()


def admissible_m6(env, G, X, nB, cp, src_cp, cal):
    # sealed query-manifold admissibility of a mounted slot set (pre-reading, independent of the CAR result)
    P = int(cp['p'])
    hn = cp['h'][0, P:].float().norm(dim=-1)
    a0, b0 = src_cp['spans_body']['X2'][0], src_cp['spans_body']['C'][1]
    med = float(src_cp['h'][0, P + a0:P + b0].float().norm(dim=-1).median())
    blk = gate_block_gpu_m6(env, G, X, nB, nB + int(cp['body_tokens']), gs=(1.0,))
    st = blk.get('stats') or {}
    c = {'h3_norm_ratio_in_range': bool(((hn / med) >= ADMIT_H3_RANGE_M6[0]).all() and ((hn / med) <= ADMIT_H3_RANGE_M6[1]).all()),
         'slot_logit_max_le_native_q99_plus_margin': bool(st) and st['slot_logit_max'] <= st['native_q01_q50_q99'][2] + cal['logit_margin'],
         'normaliser_ratio_le_cap': bool(st) and st['ratio_Zc_over_Zb_mean'] <= cal['ratio_cap'],
         'block_identity': blk['block_identity_ok'], 'finite': bool(torch.isfinite(cp['h']).all())}
    return all(c.values()), dict(c, stats=st, h3_ratio_min=float((hn / med).min()), h3_ratio_max=float((hn / med).max()))


def mount_slots_m6(env, B, cp):
    return xappend878(env, B, cp, ())


def emit_episode_m6(hdo, out, label):
    ep = out['episode_id']
    hdo.emit('03', 'EPISODE_BEGIN', {'label': label, 'world_index': out['world_index'], 'condition': out['condition'], 'arm': out['arm'],
                                     'start': {k: out['start'][k] for k in ('bank_sha256', 'bank_size', 'initial_seal', 'memory_tokens')}
                                     if out.get('start') else None}, event='E', episode=ep)
    for st in out['steps']:
        t = st['step']
        hdo.emit('04', 'STEP_PRE_ACTION', {'k': st['k'], 'hop': st['hop'], 'mounted_before': st['mounted_before'], 'state_sha256': st['state_sha256'],
                                           'X_sha256': st['X_sha256'], 'B_tokens': st['B_tokens'], 'snapshot': st['state_sha256'],
                                           'structural_predictions': 'NOT_AVAILABLE (F is not a decision maker in Stage 0-1)'}, event='S', episode=ep, step=t)
        six = six_view_m6(st['reading'])
        hdo.emit('05', 'SIX_ACTION_NATIVE_CAR', dict(six, decision_source=st['decision_source'], path='locked car867 in control_step867'),
                 event='S', episode=ep, step=t)
        eff = st.get('effect') or {}
        mb, ma = eff.get('mounted_before'), eff.get('mounted_after')
        hdo.emit('06', 'EXECUTED_OUTCOME', {'executed_action': st['action'], 'effect': eff.get('effect'), 'chosen': eff.get('chosen'),
                                            'delta_mounted': None if mb is None or ma is None else len(ma) - len(mb),
                                            'path_after': eff.get('path_after'), 'executed_equals_reading': eff.get('executed_equals_reading'),
                                            'terminalclass': st['action'] if st['action'] in TERMINAL883 else None,
                                            'bank_commit': st.get('bank_commit'), 'calls': st['calls'], 'seconds': st['seconds']},
                 event='S', episode=ep, step=t)
        hdo.emit('07', 'PREDICTION_AUDIT', {'sealed_prediction': 'NOT_AVAILABLE', 'residual': 'NOT_AVAILABLE',
                                            'eligibility': 'NOT_AVAILABLE', 'reason': 'F is not run in Stage 0-1'},
                 event='S', episode=ep, step=t)
    hdo.emit('10', 'EPISODE_TIMELINE', {'actions': out['actions'], 'effects': out['effects'], 'end': out['end'], 'seconds': out['seconds'],
                                        'calls': out['calls'], 'restore': out.get('exact_restore_vs_first_mount'),
                                        'contract': out['event_contract']['ok'], 'observer_errors': out.get('observer_errors', [])},
             event='E', episode=ep)


def outcome_m6(st):
    # structural outcome of an EXECUTED step from the locked executor fields only (post-action; never in a pre-action prefix)
    eff = st.get('effect') or {}
    mb, ma = eff.get('mounted_before'), eff.get('mounted_after')
    e = eff.get('effect')
    dm = None if mb is None or ma is None else len(ma) - len(mb)
    return {'action': st['action'], 'effect': e, 'delta_mounted': dm, 'path_after': eff.get('path_after'),
            'nochange': None if e is None else str(e).startswith('NO_EFFECT'),
            'terminalclass': st['action'] if st['action'] in TERMINAL883 else None}


# ------------------------------------------------------------------------------------ CPU self-tests (pure)
def st_m6():
    res = {}
    res['count_plus_gamma'] = count_update_m6(3, 1) == 4 and count_update_m6(3, 0) == 3
    try: count_update_m6(3, -1); res['negative_gamma_refused'] = False
    except AssertionError: res['negative_gamma_refused'] = True
    lw = [_mt6.log(0.5), _mt6.log(0.5)]
    post = log_posterior_update_m6(lw, [_mt6.log(0.9), _mt6.log(0.1)], 1)
    res['posterior_raises_high_p'] = post[0] > lw[0] and post[1] < lw[1] and abs(sum(_mt6.exp(x) for x in post) - 1) < 1e-12
    res['posterior_gamma0_unchanged'] = all(abs(a - b) < 1e-15 for a, b in zip(log_posterior_update_m6(lw, [-5.0, -1.0], 0), lw))
    sB, vB = [0.3, -0.2, 1.1], [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]]
    sC, vC = [0.7, 0.1], [[2.0, -1.0], [-1.0, 3.0]]
    o1, m1 = gated_block_m6(sB, vB, sC, vC, 1.0); o2, m2 = gated_block_m6(sB, vB, sC, vC, 2.0)
    o0, m0 = gated_block_m6(sB, vB, sC, vC, 0.0)
    res['gate_block_equals_biased_softmax'] = all(abs(a - b) < 1e-12 for g in (0.5, 1.0, 2.0, 7.0)
                                                  for a, b in zip(gated_block_m6(sB, vB, sC, vC, g)[0], biased_softmax_m6(sB, vB, sC, vC, g)))
    res['gate_g_gt_1_increases_block_mass'] = m2 > m1 > m0 == 0.0
    res['gate_g0_removes_block'] = all(abs(a - b) < 1e-12 for a, b in zip(o0, biased_softmax_m6(sB, vB, [], [], 1.0)))
    res['gate_R0_parity'] = all(abs(a - b) < 1e-12 for a, b in zip(gated_block_m6(sB, vB, [], [], 3.0)[0], biased_softmax_m6(sB, vB, [], [], 1.0)))
    res['gate_empty_C_exact_base'] = gated_block_m6(sB, vB, [], [], 1.0)[1] == 0.0
    for name, args in (('empty_base', ([], [], sC, vC, 1.0)), ('nan_score', ([float('nan')], [[1.0, 0.0]], [], [], 1.0)),
                       ('negative_g', (sB, vB, sC, vC, -1.0)), ('inf_g', (sB, vB, sC, vC, float('inf')))):
        try: gated_block_m6(*args); res['gate_%s_refused' % name] = False
        except ValueError: res['gate_%s_refused' % name] = True
    try: gated_block_m6([-800.0], [[1.0, 0.0]], [800.0], [[0.0, 1.0]], 0.0); res['gate_zero_denominator_refused'] = False
    except ValueError: res['gate_zero_denominator_refused'] = True
    res['admission_all_plus'] = admission_m6(100, 2, 10, 5, 1, 50, 200) == (True, 182.0) and admission_m6(100, 4, 10, 5, 1, 50, 200) == (False, 214.0)
    for bad in (-1.0, float('nan'), float('inf'), None):
        try: admission_m6(100, 2, bad, 5, 1, 50, 200); res['admission_refuses_%r' % (bad,)] = False
        except ValueError: res['admission_refuses_%r' % (bad,)] = True
    res['memory_all_plus'] = memory_projection_m6(40.0, 2.0, 1.0, 0.25, 0.01, 74.0)[0] is True and \
        memory_projection_m6(70.0, 2.0, 1.5, 0.25, 0.5, 74.0)[0] is False
    try: memory_projection_m6(40.0, float('nan'), 1.0, 0.25, 0.01, 74.0); res['memory_nan_refused'] = False
    except ValueError: res['memory_nan_refused'] = True
    plan = {'live_steps': 12, 'compiles': 14, 'reads': 16, 'admissibility': 14, 'snapshots': 2}
    Mt = {'live_step': [5.0, 9.0], 'compile': [1.0], 'diag_read': [3.0], 'admissibility': [0.5], 'snapshot': [8.0], 'hdo_s_total': 2.0}
    ok_, proj_ = stage1_projection_m6(1000.0, Mt, plan, 180.0, 4500.0)
    res['stage1_projection_sum'] = ok_ and proj_ == 1000.0 + 12 * 9.0 + 26 * 1.0 + 16 * 3.0 + 14 * 0.5 + 2 * 8.0 + 4.0 + 180.0
    try: stage1_projection_m6(1000.0, dict(Mt, diag_read=[]), plan, 180.0, 4500.0); res['stage1_projection_missing_refused'] = False
    except ValueError: res['stage1_projection_missing_refused'] = True
    res['row_bytes_32768'] = ROW_BYTES_M6 == 32768 and SLOTS_M6 * ROW_BYTES_M6 == 262144
    res['role_slots_8'] = sum(k for _, k in ROLE_SLOTS_M6) == SLOTS_M6
    res['chunks_cover'] = chunks_m6(10, 21, 5) == [(10, 12), (12, 14), (14, 16), (16, 18), (18, 21)]
    try: chunks_m6(0, 1, 2); res['chunks_too_few_refused'] = False
    except ValueError: res['chunks_too_few_refused'] = True
    res['medoid_index'] = medoid_index_m6([[0, 1, 4], [1, 0, 1], [4, 1, 0]]) == 1
    lp_no = {w: -2.0 for w in ACTIONS_M6}; lp_t = dict(lp_no, ACQUIRE=-1.0, ADVANCE=-2.5)
    res['directional_d_sign'] = directional_d_m6(lp_t, lp_no, 'ACQUIRE', 'ADVANCE') == 1.5
    adm = {c: True for c in ('TRUE', 'WRONG_OUTCOME', 'SHUFFLED_HISTORY', 'MATCHED_GEOMETRY', 'MEDOID_UNION', 'ECHO_MASKED')}
    D = {'TRUE': 1.0, 'WRONG_OUTCOME': 0.1, 'SHUFFLED_HISTORY': 0.2, 'MATCHED_GEOMETRY': 0.0, 'MEDOID_UNION': 0.9, 'ECHO_MASKED': 0.8}
    V = lambda d, a=adm, i=True: stage1_history_verdict_m6(d, 0.05, a, i)[0]
    res['verdict_supported'] = V(D) == 'SUPPORTED'
    res['verdict_nonspecific'] = V(dict(D, WRONG_OUTCOME=0.97)) == 'GEOMETRY_OR_NONSPECIFIC_EFFECT'
    res['verdict_echo'] = V(dict(D, ECHO_MASKED=0.01)) == 'CURRENT_ECHO_EXPLAINS_EFFECT'
    res['verdict_synthetic_rejected'] = V(dict(D, TRUE=0.0)) == 'SYNTHETIC_G_REJECTED'
    res['verdict_not_supported'] = V(dict(D, TRUE=0.0, MEDOID_UNION=0.0)) == 'NATIVE_STRUCTURAL_READING_NOT_SUPPORTED'
    res['verdict_manifold'] = V(D, dict(adm, TRUE=False)) == 'NATIVE_MANIFOLD_REJECT'
    res['verdict_inert'] = V(D, adm, False) == 'INCONCLUSIVE'
    res['combine'] = stage1_combine_m6(['SUPPORTED', 'SUPPORTED']) == 'STAGE1_CONTENT_SPECIFIC_NATIVE_READING_SUPPORTED' and \
        stage1_combine_m6(['SUPPORTED', 'CURRENT_ECHO_EXPLAINS_EFFECT']) == 'INCONCLUSIVE' and stage1_combine_m6([]) == 'INCONCLUSIVE'
    # canonical signature comparator (B02 / B03): free865 and negative mutations
    src = ("def free865(env, *memories):\n    pass\n"
           "def car867(env, memx, pre, segments, post, path='CROP'):\n    pass\n"
           "def nad(memory, cp, strict_sha=True):\n    pass\n"
           "def kwo(a, *, b=1, **kw):\n    pass\n")
    ns_ = {}; exec(compile(src, 'sigtest', 'exec'), ns_)
    tr = {n.name: n for n in _a883.parse(src).body}
    eq = lambda name, fn: canon_sig_ast_m6(tr[name]) == canon_sig_live_m6(fn)
    res['sig_free865_variadic_equal'] = eq('free865', ns_['free865']) and sig_str_m6(canon_sig_ast_m6(tr['free865'])) == '(env, *memories)'
    res['sig_default_equal'] = eq('car867', ns_['car867']) and eq('nad', ns_['nad']) and sig_str_m6(canon_sig_live_m6(ns_['nad'])) == '(memory, cp, strict_sha=True)'
    res['sig_kwonly_varkw_equal'] = eq('kwo', ns_['kwo']) and sig_str_m6(canon_sig_live_m6(ns_['kwo'])) == '(a, *, b=1, **kw)'
    mut = {'drop_vararg': "def free865(env):\n    pass\n", 'drop_default': "def car867(env, memx, pre, segments, post, path):\n    pass\n",
           'change_default': "def car867(env, memx, pre, segments, post, path='FULL'):\n    pass\n",
           'kwonly_to_pos': "def kwo(a, b=1, **kw):\n    pass\n", 'drop_varkw': "def kwo(a, *, b=1):\n    pass\n",
           'rename': "def nad(memory, cp, strict=True):\n    pass\n", 'reorder': "def nad(cp, memory, strict_sha=True):\n    pass\n",
           'strict_default_false': "def nad(memory, cp, strict_sha=False):\n    pass\n"}
    for k, s in mut.items():
        m_ = {}; exec(compile(s, 'mut', 'exec'), m_); fn = next(v for v in m_.values() if callable(v))
        res['sig_mutation_%s_detected' % k] = canon_sig_ast_m6(tr[fn.__name__]) != canon_sig_live_m6(fn)

    class Obj:
        def meth(self, x): return x
    res['sig_bound_method_flagged'] = canon_sig_live_m6(Obj().meth) == 'BOUND_METHOD'
    # locked free865 body in a sandbox: zero / one / two memories, None, MEMNULL, release / gc counts, implicit None
    fnode = next(n for n in _a883.parse(ENGINE883['body']).body if isinstance(n, _a883.FunctionDef) and n.name == 'free865') \
        if isinstance(ENGINE883, dict) and ENGINE883.get('body') else None
    if fnode is not None:
        cnt = {'release': 0, 'gc': 0}
        sb = {'gc': type('G', (), {'collect': staticmethod(lambda: cnt.__setitem__('gc', cnt['gc'] + 1))})}
        exec(compile(_a883.Module([fnode], []), 'test870.py:free865', 'exec'), sb)
        nul = object(); envm = {'MEMNULL841': nul, 'release': lambda: cnt.__setitem__('release', cnt['release'] + 1)}
        rets = [sb['free865'](envm), sb['free865'](envm, [1]), sb['free865'](envm, [1], [2]), sb['free865'](envm, None, nul)]
        res['free865_locked_calls'] = rets == [None] * 4 and cnt == {'release': 4, 'gc': 4} and \
            canon_sig_ast_m6(fnode) == [('env', 'POSITIONAL_OR_KEYWORD', 'NO_DEFAULT', None), ('memories', 'VAR_POSITIONAL', 'NO_DEFAULT', None)]
        try: sb['free865'](envm, memx=[1]); res['free865_wrong_keyword_typeerror'] = False
        except TypeError: res['free865_wrong_keyword_typeerror'] = True
    else:
        res['free865_locked_calls'] = res['free865_wrong_keyword_typeerror'] = False
    # bank: happy path, append-only, duplicate event id, interrupted temp, crash after rename (quarantine), corruption,
    # manifest tamper, truncated / malformed manifest, bank-copy readback
    import tempfile as _tf6
    d = _tf6.mkdtemp(prefix='t866bank_')
    b = Bank_M6(d); b.commit('a.bin', b'x' * 10, {'event_id': 'e1'}); b.commit('b.bin', b'y' * 7, {'event_id': 'e2'})
    v = b.verify()
    res['bank_happy_chain'] = v['ok'] and v['entries'] == 2
    try: b.commit('a.bin', b'z', {}); res['bank_duplicate_name_refused'] = False
    except AssertionError: res['bank_duplicate_name_refused'] = True
    try: b.commit('c.bin', b'z', {'event_id': 'e1'}); res['bank_duplicate_event_refused'] = False
    except AssertionError: res['bank_duplicate_event_refused'] = True
    open(_o6.path.join(d, 'c.bin.tmp'), 'wb').write(b'interrupted')
    res['bank_interrupted_temp_detected_then_cleaned'] = b.verify()['tmp_orphans'] == ['c.bin.tmp'] and not b.verify()['ok'] and \
        b.cleanup_orphans() == ['c.bin.tmp'] and b.verify()['ok']
    open(_o6.path.join(d, 'd.bin'), 'wb').write(b'renamed-before-manifest')
    res['bank_crash_after_rename_quarantined_not_deleted'] = b.verify()['quarantine'] == ['d.bin'] and not b.verify()['ok'] and \
        b.cleanup_orphans() == [] and _o6.path.exists(_o6.path.join(d, 'd.bin'))
    _o6.remove(_o6.path.join(d, 'd.bin'))
    res['bank_copy_readback'] = open(_o6.path.join(d, 'a.bin'), 'rb').read() == b'x' * 10 and b.verify()['ok']
    raw_a = open(_o6.path.join(d, 'a.bin'), 'rb').read(); open(_o6.path.join(d, 'a.bin'), 'wb').write(b'X' + raw_a[1:])
    res['bank_file_corruption_detected'] = b.verify()['files_ok'] is False
    open(_o6.path.join(d, 'a.bin'), 'wb').write(raw_a)
    mraw = open(b.manifest, 'rb').read()
    open(b.manifest, 'wb').write(mraw.replace(b'"event_id": "e1"', b'"event_id": "e9"'))
    res['bank_manifest_tamper_detected'] = b.verify()['parent_chain_ok'] is False
    open(b.manifest, 'wb').write(mraw[:-5])
    vt = b.verify()
    res['bank_truncated_manifest_structured'] = vt['ok'] is False and bool(vt['malformed'])
    open(b.manifest, 'wb').write(mraw + b'{not json\n')
    vm = b.verify()
    res['bank_malformed_manifest_structured'] = vm['ok'] is False and bool(vm['malformed']) and b.cleanup_orphans() == []
    try: b.commit('e.bin', b'q', {}); res['bank_commit_on_malformed_refused'] = False
    except Gate883: res['bank_commit_on_malformed_refused'] = True
    open(b.manifest, 'wb').write(mraw)
    # HDO chain: sequence, payload tamper, parent tamper, truncated line, malformed json
    h = HDO_M6('FULL', _o6.path.join(d, 'hdo.log'), enabled=False)
    h.emit('00', 'RUN_LOCK', {'a': 1}); h.emit('05', 'SIX', {'b': [1, 2]}, event='e', episode='x', step=1); h.emit('13', 'V', {'c': 3})
    info = h.close(); good = open(info['path'], encoding='utf-8').read()
    res['hdo_sequence_chain'] = hdo_verify_chain_m6(info['path'])['ok'] and hdo_verify_chain_m6(info['path'])['records'] == 3
    for name, txt in (('payload', good.replace('"b":[1,2]', '"b":[1,3]')), ('parent', good.replace('PARENT_SEAL=', 'PARENT_SEAL=f', 1)),
                      ('truncated', good[:-7]), ('malformed', good.replace('{"c":3}', '{"c":3')), ('gap', '\n'.join(good.split('\n')[::2]))):
        open(info['path'], 'w', encoding='utf-8').write(txt)
        res['hdo_%s_detected' % name] = hdo_verify_chain_m6(info['path'])['ok'] is False
    open(info['path'], 'w', encoding='utf-8').write('')
    res['hdo_empty_log_not_ok'] = hdo_verify_chain_m6(info['path'])['ok'] is False
    fake = {'action': 'ACQUIRE', 'mass': 0.9, 'margin_logp': 1.2, 'normalized': {w: 1 / 6 for w in ACTIONS_M6},
            'scores': [{'word': w, 'sequence_logp': -float(i)} for i, w in enumerate(ACTIONS_M6)]}
    sv = six_view_m6(fake)
    res['six_view_rank'] = sv['full_rank'][0] == 'ADVANCE' and len(sv['logp']) == 6
    res['outcome_terminal_has_no_effect'] = outcome_m6({'action': 'STOP', 'effect': None})['terminalclass'] == 'STOP' and \
        outcome_m6({'action': 'STOP', 'effect': None})['nochange'] is None
    res['outcome_no_effect_is_nochange'] = outcome_m6({'action': 'BACKTRACK', 'effect': {'effect': 'NO_EFFECT_AT_ROOT',
                                                       'mounted_before': ['a'], 'mounted_after': ['a']}})['nochange'] is True
    # provenance / oracle firewall on env callables (B15): a callable whose code, globals or closure reaches an oracle key
    envx = {'worlds829': [1]}
    exec(compile("def leaky(x):\n    return worlds829\n", 'leak', 'exec'), envx)
    res['provenance_flags_oracle_name_and_globals'] = bool(provenance_m6(envx['leaky'])['oracle_names_in_code']) and \
        bool(provenance_m6(envx['leaky'])['oracle_keys_in_globals'])
    def mk(dd):
        def inner(): return dd
        return inner
    res['provenance_flags_oracle_closure'] = bool(provenance_m6(mk({'node851': 1}))['oracle_in_closure'])
    res['provenance_clean_function'] = not any(provenance_m6(count_update_m6)[k] for k in ('oracle_names_in_code', 'oracle_keys_in_globals', 'oracle_in_closure'))
    return res
class Readiness866(Exception):
    # Stage-1 readiness / preseal failure: Stage 1 is not run; this is not a scientific result
    pass


NATIVES_M6 = {'car867': 'test870.py', 'reading867': 'test870.py', 'control_step867': 'test870.py', 'execute866': 'test870.py',
              'hop865': 'test870.py', 'direction866': 'test870.py', 'address866': 'test870.py', 'mount865': 'test870.py',
              'free865': 'test870.py', 'forward873': '873.py', 'kv873': '873.py', 'length873': '873.py', 'car873': '873.py',
              'xspan878': '878.py', 'next_kv878': '878.py', 'write_exp878': '878.py', 'load_exp878': '878.py',
              'append_exp878': '878.py', 'xcar878': '878.py', 'xappend878': '878.py', 'xattn877': '877.py'}
S1_CONDITIONS_M6 = ('NO_MEMORY', 'TRUE', 'WRONG_OUTCOME', 'SHUFFLED_HISTORY', 'MATCHED_GEOMETRY', 'INERT_RECOMPUTE',
                    'ECHO_MASKED', 'MEDOID_UNION')
S1_PLAN_M6 = {
    'histories': [{'id': 'H1', 'history': [10, 'FORK'], 'test': [10, 'MISSING']},
                  {'id': 'H2', 'history': [9, 'FORK'], 'test': [9, 'MISSING']}],
    'history_arm': 'REC = natural NOFB decision (locked car867), experience of every nonterminal step recorded as a CUT3 '
                   'cartridge [X2 = pre-action control X][A = executed action tokens][C = next observation] and committed to '
                   'the persistent bank; never read during the history',
    'history_horizon': HORIZON883,
    'a_plus': 'ACQUIRE', 'a_zero': 'ADVANCE', 'expected_sign': '+',
    'e_plus_rule': 'first executed REC event with effect MOUNTED (action ACQUIRE) that has a committed cartridge',
    'e_zero_rule': 'first executed REC event with effect POINTER_ADVANCED (action ADVANCE) that has a committed cartridge',
    'test_context': 'fresh step-1 pre-action snapshot of the test spec (nothing executed); slots appended after its B',
    'D_j': '[logp_C(a+) - logp_NO(a+)] - [logp_C(a0) - logp_NO(a0)] for each condition C; hypothesis D_TRUE > epsilon_num',
    'role_slots': [list(x) for x in ROLE_SLOTS_M6],
    'conditions': {
        'NO_MEMORY': 'B_T only',
        'TRUE': 'barycentric slots of e+ : X2 x5, A x1, C x2',
        'WRONG_OUTCOME': 'X2 x5 and A x1 of e+, C x2 of e0 (same slot count / positions)',
        'SHUFFLED_HISTORY': 'the TRUE slots in reversed order (C, A, X2): outcome before action, K re-phased to the new positions',
        'MATCHED_GEOMETRY': '8 barycenters of the X2 rows of e0, each tensor rescaled to the norm of the matching TRUE slot tensor',
        'INERT_RECOMPUTE': 'TRUE recompiled from an independent reload of the bank copy of e+ (digest must equal TRUE)',
        'ECHO_MASKED': 'TRUE slots mounted, the 5 X2 (context) slot columns gated g=0 (explicit mask)',
        'MEDOID_UNION': 'exact recorded rows: per chunk the H3 medoid row of e+ (no averaging)'},
    'verdict': 'stage1_history_verdict_m6 per history, stage1_combine_m6 over both (sealed in source)',
    'workload': {'live_steps': 2 * HORIZON883, 'compiles': 12, 'reads': 16, 'admissibility': 12, 'snapshots': 2},
    'never': ['no TRUE / control CAR value is computed before the preseal JSON is written',
              'no counterfactual outcome is executed or written to the bank',
              'no action is forced; the history decisions are the natural locked car867 readings']}
PREREG_M6 = {
    'test': 'TEST866 / M6-S01: Stage 0 (S0A-S0G) then automatic Stage 1 (content-specific native readability)',
    'base': '886.py commit 289f4260 blob 638cf623 (repairs B01-B17 of the 886 review)', 'head': HEAD883, 'hdo_mode': HDO_MODE_M6,
    'stage0': {
        'S0A': 'structured canonical signatures (name / kind / order / default) of 21 natives vs their locked source AST, '
               'live co_code == compiled locked AST; 6 env callables vs EXPECTED_ENV_M6; binding provenance; oracle '
               'firewall over code / globals / closure; grad free; no registered hook; model contract',
        'S0C': 'same-B / same-X no-slot parity: car873 == m6_car(R=0) == native car867 (bitwise), 80-layer KV, determinism',
        'S0B': 'CUT3 write -> SHA -> reload bitwise; bank commit / readback; negative: file corruption, tensor-SHA mismatch, '
               'scratch-bank crash / quarantine (the live bank is never mutated by a diagnostic)',
        'S0E': 'append_exp878 == xappend878; B prefix 80-layer unchanged; layer-4 slot KV == next_kv878(H3); H3 perturbation '
               'changes layers 4-79 K and V, never 0-3',
        'S0D': 'g=1 explicit vs implicit, g=0 vs no slot (cap %.3g); layer-0 block identity g in {0,0.5,1,2}; mass monotone; '
               'canonical restore of H3 + all lower K / V and of the reading; GQA 64/8/128; finite' % GATE_TOL_CAP_M6,
        'S0F': 'post-commit observer OFF (None) vs ON, same physical start and Python / NumPy / Torch CPU / CUDA RNG: six '
               'logps / rank / action / effect / chosen / path / mounts / end / calls / RNG / bank identical',
        'S0G': 'measured time / VRAM / RAM / disk / calls admission of the sealed Stage-1 workload; missing or non-finite -> BLOCK'},
    'stage1_plan': S1_PLAN_M6,
    'calibration': {'epsilon_num': 'max(%.3g, %.1f x max(Stage-0 explicit-mask delta, g0 delta, determinism delta))' % (EPS_FLOOR_M6, EPS_MULT_M6),
                    'admissibility': 'H3 norm ratio in %s; slot max logit <= native q99 + max(0, S0 probe excess) + %.1f; '
                                     'Zc/Zb <= max(%.1f x S0 probe ratio, %.2f)' % (list(ADMIT_H3_RANGE_M6), ADMIT_LOGIT_PAD_M6,
                                                                                  ADMIT_RATIO_MULT_M6, ADMIT_RATIO_MIN_M6)},
    'labels_allowed': ['TECHNICAL_BLOCK', 'INCOMPLETE_BUDGET', 'NATIVE_MANIFOLD_REJECT', 'NO_DIRECTIONAL_NATIVE_USE',
                       'GEOMETRY_OR_NONSPECIFIC_EFFECT', 'CURRENT_ECHO_EXPLAINS_EFFECT', 'SYNTHETIC_G_REJECTED',
                       'NATIVE_STRUCTURAL_READING_NOT_SUPPORTED', 'STAGE1_CONTENT_SPECIFIC_NATIVE_READING_SUPPORTED', 'INCONCLUSIVE'],
    'never_claimed': ['PERSISTENT_LEARNING', 'TASK_SUCCESS', 'TRANSFER', 'STAGE2-4', 'AUTONOMOUS_REASONING'],
    'gpu_execution': 'NOT VERIFIED by the author'}
PREREG_M6_SHA = _h6.sha256(hdo_canon_m6(PREREG_M6).encode()).hexdigest()


def signatures_m6(env):
    # S0A / B02 / B03 / B15: structured comparison of the LAST ACTIVE bindings (after G1) with the locked source ASTs
    g = globals(); out, ok = {}, True
    trees = {}
    for f in set(NATIVES_M6.values()):
        trees[f] = {n.name: n for n in _a883.walk(_a883.parse(ENGINE883['body'] if f == 'test870.py' else RAW_SOURCES864[f].decode()))
                    if isinstance(n, _a883.FunctionDef)}
    for name, f in sorted(NATIVES_M6.items()):
        node, fn = trees[f].get(name), g.get(name)
        exp = None if node is None else canon_sig_ast_m6(node)
        act = None if fn is None else canon_sig_live_m6(fn)
        code_eq = None
        if node is not None and fn is not None and hasattr(fn, '__code__'):
            mod = compile(_a883.Module([node], []), f, 'exec')
            cc = next((c for c in mod.co_consts if hasattr(c, 'co_name') and c.co_name == name), None)
            code_eq = cc is not None and cc.co_code == fn.__code__.co_code
        pv = provenance_m6(fn) if fn is not None and hasattr(fn, '__code__') else None
        clean = pv is not None and not pv['oracle_keys_in_globals'] and not pv['oracle_in_closure']
        out[name] = {'source': f, 'expected': sig_str_m6(exp) if exp else None, 'actual': sig_str_m6(act) if act else None,
                     'match': exp is not None and exp == act, 'co_code_equals_locked': code_eq, 'provenance': pv, 'oracle_clean': clean}
        ok = ok and out[name]['match'] and code_eq is True and clean
    envs = {}
    idx = locked_defs_m6(sorted(EXPECTED_ENV_M6), [(n, RAW_SOURCES864[n].decode(errors='replace')) for n in sorted(RAW_SOURCES864) if n.endswith('.py')])
    for k, want in sorted(EXPECTED_ENV_M6.items()):
        fn = env.get(k)
        if fn is None: envs[k] = {'present': False}; ok = False; continue
        act = canon_sig_live_m6(fn)
        pv = provenance_m6(fn) if hasattr(fn, '__code__') else None
        cands = idx[k]
        cand_match = [fname for fname, nd in cands if canon_sig_ast_m6(nd) == act]
        clean = pv is not None and not pv['oracle_names_in_code'] and not pv['oracle_keys_in_globals'] and not pv['oracle_in_closure']
        envs[k] = {'present': True, 'expected': want, 'actual': sig_str_m6(act), 'match': sig_str_m6(act) == want and act != 'BOUND_METHOD',
                   'locked_source_candidates': [c[0] for c in cands], 'locked_source_signature_match': cand_match or 'NO_LOCKED_SOURCE_IN_CELL',
                   'provenance': pv, 'oracle_clean': clean}
        ok = ok and envs[k]['match'] and clean and (not cands or bool(cand_match))
    return {'globals': out, 'env_callables': envs, 'ok': ok}


def rng_snapshot_m6():
    return {'py': _rd6.getstate(), 'np': _np883.random.get_state(), 'torch': torch.get_rng_state().clone(),
            'cuda': torch.cuda.get_rng_state().clone()}


def rng_restore_m6(s):
    _rd6.setstate(s['py']); _np883.random.set_state(s['np']); torch.set_rng_state(s['torch']); torch.cuda.set_rng_state(s['cuda'])


def rng_sha_m6():
    parts = [repr(_rd6.getstate()).encode(), repr(_np883.random.get_state()[1].tolist()).encode(),
             torch.get_rng_state().numpy().tobytes(), torch.cuda.get_rng_state().cpu().numpy().tobytes()]
    return _h6.sha256(b''.join(parts)).hexdigest()


def proc_ram_gib_m6():
    try:
        mi = dict((l.split(':')[0], int(l.split()[1])) for l in open('/proc/meminfo') if l.split()[1:2])
        return {'total_gib': round(mi['MemTotal'] / 2**20, 2), 'available_gib': round(mi['MemAvailable'] / 2**20, 2)}
    except (OSError, KeyError, ValueError, IndexError) as exc:
        return {'error': '%s: %s' % (type(exc).__name__, exc)}


def alloc_gib_m6():
    return torch.cuda.memory_allocated() / 2**30


def run_m6(stage, key, fn, *a, **kw):
    # B06: the 75-min total deadline and the VRAM guard before AND after every expensive diagnostic; measured duration and
    # allocation increase; never cut inside a locked call
    guard883(stage + '_pre')
    m0, t = alloc_gib_m6(), time.perf_counter()
    r = fn(*a, **kw)
    dt = round(time.perf_counter() - t, 3)
    STATE_M6['measure'].setdefault(key, []).append(dt)
    STATE_M6['measure'].setdefault('transient_gib', []).append(round(max(alloc_gib_m6() - m0, 0.0), 4))
    guard883(stage + '_post')
    return r


def drop_m6(*names):
    # B17: release diagnostic tensors / caches; a cleanup failure is recorded and never hides the original exception
    g = globals()
    for n in names:
        try: g.pop(n, None)
        except Exception as exc: STATE_M6['cleanup_errors'].append('%s: %s: %s' % (n, type(exc).__name__, exc))
    try: gc.collect(); torch.cuda.empty_cache()
    except Exception as exc: STATE_M6['cleanup_errors'].append('EMPTY_CACHE %s: %s' % (type(exc).__name__, exc))


def rec_sink_m6(bank, hdo, events):
    # Stage-1 history sink: the locked-written cartridge of a REC step is committed to the persistent bank (append-only)
    def sink(entry, wrec, prev_step, key):
        data = open(entry['file'], 'rb').read()
        if _h6.sha256(data).hexdigest() != entry['sha256']: raise Gate883('REC_SINK_FILE_SHA ' + entry['id'])
        y = outcome_m6(prev_step)
        ev = {'event_id': '%s_t%d' % (key['episode_id'], prev_step['step']), 'episode_id': key['episode_id'],
              'world_index': key['world_index'], 'condition': key['condition'], 'step': prev_step['step'], 'outcome': y,
              'cartridge_id': entry['id'], 'tensor_sha': entry['tensor_sha'], 'body_tokens': entry['body_tokens'],
              'spans_body': entry['provenance']['spans_body'], 'C_rows_sha256': entry['provenance']['C_rows_sha256'],
              'X_sha256': entry['provenance']['X_sha256'], 'source_sha256': entry['sha256']}
        rec = bank.commit(entry['id'] + '.pt', data, ev)
        bentry = dict(entry, file=_o6.path.join(bank.root, entry['id'] + '.pt'))
        events.append(dict(ev, bank_entry=bentry, bank_seq=rec['seq']))
        hdo.emit('08', 'PHYSICAL_WRITE_REVISION', {'event': {k: v for k, v in ev.items()}, 'bank_seq': rec['seq'], 'bytes': rec['bytes'],
                                                   'sha256': rec['sha256'], 'parent_manifest_sha256': rec['parent_manifest_sha256']},
                 event='REC', episode=key['episode_id'], step=prev_step['step'])
        return {'bank_seq': rec['seq'], 'sha256': rec['sha256'], 'event_id': ev['event_id']}
    return sink


def load_event_cp_m6(env, ev):
    cp = load_exp878(env, ev['bank_entry'])               # locked: file SHA, id / p / n / body_tokens, every tensor SHA
    cp['spans_body'] = {k: list(v) for k, v in ev['spans_body'].items()}
    return cp


def shuffled_slots_m6(slots):
    return list(reversed(slots))


def write_json_sha_m6(name, obj):
    json_write864(name, obj)
    p = ROOT864 / name
    return {'path': str(p), 'sha256': sha256_bytes864(p.read_bytes()), 'bytes': p.stat().st_size}


# ============================ single cell execution (TEST866: Stage 0 -> automatic Stage 1) ============================
T_START878 = T_START883 = time.perf_counter()
ORACLE_VAULT883 = None; OFFLINE_DIGEST_G1_885 = None; VAULT_FP885 = None; HDO6 = None; BANK6 = None
ARTIFACTS_M6 = {}; S1_RESULTS_M6 = {'status': 'NOT_RUN'}; S1_PRESEAL_M6 = {'status': 'NOT_RUN'}; S0_RESULTS_M6 = {}
try:
    STATE883['status'] = 'G0'; capture_source883()
    json_write864('TEST866_prereg.json', {'prereg': PREREG_M6, 'sha256': PREREG_M6_SHA, 'f1_prereg_sha256': PREREG_SHA883,
                                          'written_before_model_load': True})
    load_sources865(); select_locked883()
    du = _s883.disk_usage(str(ROOT864))
    if du.free / 2**30 < 5.0: raise Gate883('DISK_FREE %.1f GiB' % (du.free / 2**30))
    STATE883['write_probe'] = write_probe883(ROOT864)
    if not all(STATE883['write_probe'].values()): raise Gate883('WRITE_PROBE %s' % STATE883['write_probe'])
    source_audit878(); load878(); run_selftests883()          # every CPU self-test must PASS before the model is loaded
    STATE883['live_scan'] = live_path_scan883([ENGINE883['body']] + [RAW_SOURCES864[n].decode() for n in ('873.py', '878.py', '881.py')])
    if not STATE883['live_scan']['ok']: raise Gate883('LIVE_PATH_ORACLE_SCAN %s' % STATE883['live_scan'])
    feasibility_audit864(); audit_contracts865(); load_spine864(); REFS883 = load_records870()
    WORLDS883 = select_worlds883()
    assert WORLDS883 == list(REQUIRED_WORLDS883), ('WORLDS_RULE', WORLDS883)
    assert CC_GPU_OK and 'A100' in str(CC_GPU.get('name')) and CC_GPU.get('total_gib', 0) >= 78.0, ('A100_80GB_REQUIRED', CC_GPU)
    pre_ram = proc_ram_gib_m6()
    if not (pre_ram.get('available_gib', 0) >= RAM_MIN_GIB_M6 and du.free / 2**30 >= DISK_NEED_GIB_M6 + 5.0):
        raise Budget883('RESOURCE_PREADMISSION ram=%s disk_free_gib=%.1f' % (pre_ram, du.free / 2**30))
    gate883('G0', 'PASS', selftests=sorted(STATE883['selftests']), d0=STATE883['d0']['summary'], ram=pre_ram,
            source={k: v for k, v in STATE883['source'].items() if k != 'reused'}, disk_free_gib=round(du.free / 2**30, 1))
    HDO6 = HDO_M6(HDO_MODE_M6, ROOT864 / 'TEST866_hdo.log')
    HDO6.emit('00', 'RUN_LOCK', {'mark': M6_MARK, 'mode': HDO_MODE_M6, 'prereg_sha256': PREREG_M6_SHA, 'head': HEAD883,
                                 'engine_blob': ENGINE_BLOB883, 'executed_cell_git_blob': STATE883['source']['executed_cell_git_blob'],
                                 'executed_cell_sha256': STATE883['source']['executed_cell_sha256'],
                                 'executed_cell_lines': STATE883['source']['lines_splitlines'],
                                 'cpu_selftests': {k: all(v_ is True for v_ in r_.values()) if 'error' not in r_ else r_['error']
                                                   for k, r_ in STATE883['selftests'].items()},
                                 'HDO_VIEW_TRUNCATION': 'UNKNOWN (stdout completeness is not observable; the disk chain is authoritative)'})
    STATE883['status'] = 'G1'
    env883, original_error883, original_trace883, reproduction883 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace883; TWO_JOB_VERIFICATION864 = verify_two_job859(env883, original_trace883)
    assert_hook_free859(env883, 'T866_before_native'); OFFLINE_DIGEST_G1_885 = install_offline_evaluator859(env883)
    if OFFLINE_DIGEST_G1_885 != EVAL_DIGEST885: raise Gate883('EVALUATOR_DIGEST_G1 %s != locked %s' % (OFFLINE_DIGEST_G1_885, EVAL_DIGEST885))
    native883 = native_sequences860(env883); NATIVE_REGRESSION864 = native_regression864(env883, native883)
    verify_864_reference865(NATIVE_REGRESSION864); ANALYSIS864 = run_analysis863(env883, native883)
    assert len(STATE863['restores']) == 3 and all(r_['exact'] for r_ in STATE863['restores'])
    digest883 = records_digest861(env883); null_seal883 = physical_seal863(env883, env883['MEMNULL841'])
    runtime_contracts865(env883); runtime_preflight865(env883, reproduction883); make_slots866(env883)
    SLOTS867['PREV_EVALUATION'] = list(env883['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env883); resolve_append873(env883); api877(env883); WEIGHTS0_878 = weights_digest877(env883)
    chunk883 = [ns['CHUNK'] for ns in (env883['build_fusion'].__globals__, env883) if 'CHUNK' in ns]
    assert chunk883 and int(chunk883[0]) > 0 and all(k in env883 for k in (
        'P', 'to_gpu', 'entries', 'make_x851', 'gen851', 'gen849', 'C_SLOT851', 'E_SLOT851', 'REVIEW_SUFFIX851', 'stats849',
        'MUE845', 'MEMNULL841', 'relation852', 'R_SLOT852', 'QTEXT841', 'native_append_direct', 'cache_build') + ORACLE_ENV_KEYS883), 'ENGINE_NAMESPACE'
    EXP878['CHUNK'] = int(chunk883[0])
    vocab883 = sorted(w_ for w_, _ in ACTION_IDS867)
    assert vocab883 == sorted(ACTIONS_M6), ('NATIVE_VOCABULARY', vocab883)
    assert not any(p_.requires_grad for p_ in env883['model'].parameters()), 'NOT_FROZEN'
    hook883 = assert_hook_free859(env883, 'T866_before_points')
    STATE883['model_contract'] = model_contract883(env883, CC_GPU); STATE883['model_contract']['physical_seal_MEMNULL'] = null_seal883
    if not STATE883['model_contract']['ok']: gate883('G1', 'BLOCK', model_contract=STATE883['model_contract'])
    if _o883.path.exists(CART_ROOT883): _s883.rmtree(CART_ROOT883)
    _o883.makedirs(CART_ROOT883); EXP_DIR878 = type(ROOT864)(CART_ROOT883)
    gate883('G1', 'PASS', api=STATE883.get('api'), vocabulary=vocab883, chunk=EXP878['CHUNK'], P=int(env883['P']),
            g0_g1_wall_s=round(time.perf_counter() - T_START883, 1), hook_free=True, model_contract=STATE883['model_contract']['checks'])
    by_key883 = build_specs869(env883)
    ORACLE_VAULT883 = seal_oracle883(env883); VAULT_FP885 = vault_fingerprint885(ORACLE_VAULT883)
    SPEC_M6 = by_key883[(10, 'MISSING')]                       # sealed: the first required cell of the 883-886 design
    # ---- one phase clock + one rearm from the unchanged T_START883 before the first live generation ----
    STATE883['status'] = 'S0A'
    assert CALL_ALLOWANCE865 == 3000, ('CALL_ALLOWANCE865', CALL_ALLOWANCE865)
    now_ = time.perf_counter(); plan_ = g2_budget_plan883(now_, T_START883, WALL_S883)
    if plan_ is None: raise Budget883('NO_TIME_LEFT_BEFORE_STAGE0: elapsed %.1f s of %.0f s' % (now_ - T_START883, WALL_S883))
    T0_865 = plan_['T0_865']; TEST865_MINUTES = plan_['TEST865_MINUTES']
    rearm_budget865(env883)
    bl_ = budget_left865(env883, STEP_CALLS867)
    if bl_ is not True: raise Budget883('RESOURCE_BUDGET_AT_STAGE0_START budget_left865=%r' % (bl_,))
    BANK6 = Bank_M6(ROOT864 / 'm6_bank')                     # persistent: never deleted by any cleanup of this cell
    HDO6.emit('01', 'SOURCE_AND_MODEL_CONTRACT', {'model_contract': STATE883['model_contract'], 'api': STATE883.get('api'),
                                                  'weights_digest': WEIGHTS0_878, 'hook_audit': hook883, 'oracle_keys_in_live_env':
                                                  sorted(set(ORACLE_ENV_KEYS883) & set(env883)), 'gpu': CC_GPU})
    HDO6.emit('02', 'SEALED_PLAN_AND_BUDGET', {'prereg': PREREG_M6, 'budget_init': dict(budget_clocks883(env883, 'S0_INIT'), plan=plan_),
                                               'spec': {k: SPEC_M6[k] for k in ('item', 'world_index', 'condition')}})
    # ---------------- S0A ----------------
    sig6 = signatures_m6(env883)
    fp6 = {'executed_cell_git_blob': STATE883['source']['executed_cell_git_blob'], 'head': HEAD883, 'engine_blob': ENGINE_BLOB883,
           'weights_digest': WEIGHTS0_878, 'torch': str(torch.__version__), 'model_contract_ok': STATE883['model_contract']['ok'],
           'grad_free': not any(p_.requires_grad for p_ in env883['model'].parameters()),
           'hooks': assert_hook_free859(env883, 'T866_S0A')['hook_count'], 'signatures_ok': sig6['ok'],
           'oracle_keys_in_live_env': sorted(set(ORACLE_ENV_KEYS883) & set(env883))}
    HDO6.emit('01', 'NATIVE_SIGNATURES', sig6, event='S0A')
    S0_RESULTS_M6['S0A'] = {'fingerprint': fp6, 'signatures': sig6}
    if not (sig6['ok'] and fp6['grad_free'] and fp6['hooks'] == 0 and fp6['model_contract_ok'] and not fp6['oracle_keys_in_live_env']):
        gate883('S0A', 'BLOCK', fingerprint=fp6, bad=sorted([k for k, v in sig6['globals'].items() if not (v['match'] and v['co_code_equals_locked'] and v['oracle_clean'])] +
                                                      [k for k, v in sig6['env_callables'].items() if not (v.get('match') and v.get('oracle_clean'))]))
    gate883('S0A', 'PASS', fingerprint=fp6)
    # ---------------- S0C (snapshot, no-slot parity) ----------------
    STATE883['status'] = 'S0C'
    try:
        SNAP6 = run_m6('S0C_snapshot', 'snapshot', snapshot_m6, env883, SPEC_M6, 'S0')
        native_r = SNAP6['record']['reading']; B6, X6 = SNAP6['B'], SNAP6['X']; nB6 = SNAP6['B_tokens']
        r_car873 = run_m6('S0C_car873', 'diag_read', car873, env883, env883['cache_build'](list(B6)), X6)
        r_m6 = run_m6('S0C_m6car', 'diag_read', m6_car, env883, B6, X6); r_m6b = run_m6('S0C_m6car2', 'diag_read', m6_car, env883, B6, X6)
        own_ = env883['cache_build'](list(B6)); forward873(env883, own_, X6, nB6); kv_nat = kv873(env883, own_); del own_
        cl_ = env883['cache_build'](list(B6))
        m6_xspan(env883, cl_, X6.reshape(1, int(X6.shape[0]), int(env883['H'])), torch.ones((1, nB6 + int(X6.shape[0])), device=env883['DEV'], dtype=torch.long), 0, int(env883['NL']))
        kv_exp = kv873(env883, cl_); del cl_
        c0 = {'native_path_is_CROP': (SNAP6['record']['reading'].get('path') or 'CROP') == 'CROP',
              'car873_equals_native_car867': same_reading881(r_car873, native_r), 'm6_car_R0_equals_native': same_reading881(r_m6, native_r),
              'm6_car_deterministic': same_reading881(r_m6, r_m6b),
              'explicit_80_layer_KV_equals_native_forward873': all(torch.equal(a, b) for i in range(int(env883['NL'])) for a, b in zip(kv_exp[i], kv_nat[i])),
              'B_seal_unchanged': full_seal881(B6)['all'] == SNAP6['B_seal']}
    finally:
        drop_m6('kv_exp', 'kv_nat', 'own_', 'cl_')
    HDO6.emit('05', 'SIX_ACTION_NATIVE_CAR', dict(six_view_m6(native_r), snapshot=SNAP6['state_sha256'], X_sha256=SNAP6['X_sha256'],
                                                  path='locked car867 (snapshot step 1, nothing executed)'), event='S0C', episode='SNAP_S0', step=1)
    S0_RESULTS_M6['S0C'] = c0
    if not all(c0.values()): gate883('S0C', 'BLOCK', checks=c0)
    gate883('S0C', 'PASS', checks=c0)
    # ---------------- S0B (CUT3 write / reload / bank, negatives) ----------------
    STATE883['status'] = 'S0B'
    gH6, h36, n26, ck6 = run_m6('S0B_cut3', 'compile', cut3_rows_m6, env883, SNAP6, SLOTS_M6)
    prov6 = {'test': 'TEST866', 'namespace': 'STAGE0_MECHANICAL_PROBE_NOT_A_MEMORY', 'source': 'first %d X rows of snapshot S0' % SLOTS_M6,
             'X_sha256': SNAP6['X_sha256'], 'state_sha256': SNAP6['state_sha256'], 'B_tokens': nB6, 'weights_digest': WEIGHTS0_878,
             'cell_git_blob': STATE883['source']['executed_cell_git_blob']}
    eid6 = 'T866S0_' + _h6.sha256(hdo_canon_m6(prov6).encode()).hexdigest()[:16]
    entry6 = run_m6('S0B_write', 'compile', write_exp878, env883, eid6, gH6, h36, n26, n26 + SLOTS_M6, SLOTS_M6, prov6)
    cp6 = run_m6('S0B_load', 'compile', load_exp878, env883, entry6)
    P6 = int(env883['P']); CUT6, NL6 = APPEND873['CUT'], int(env883['NL'])
    b0 = dict(ck6, file_sha_and_tensor_sha_on_reload=True,
              h3_reload_bitwise=torch.equal(cp6['h'][:, P6:], h36),
              v_reload_bitwise=all(torch.equal(cp6['lower'][i][1][:, :, P6:], gH6[i][1][:, :, n26:n26 + SLOTS_M6]) for i in range(CUT6 + 1)),
              k_roundtrip_ok=entry6['roundtrip_K_rel'] <= ROPE_REL_CAP_M6,
              device_dtype_ok=all(t.is_cuda and t.dtype == torch.bfloat16 for t in [cp6['h']] + [x for kv in cp6['lower'] for x in kv]))
    drop_m6('gH6')
    bank_head0 = BANK6.head_sha()
    scratch6 = ROOT864 / 'S0B_scratch'; _o6.makedirs(scratch6, exist_ok=True)
    sb6 = Bank_M6(scratch6 / 'bank')                           # diagnostic bank: the live bank is never touched here
    raw6 = open(entry6['file'], 'rb').read()
    srec6 = sb6.commit(eid6 + '.pt', raw6, {'stage': 'S0B', 'event_id': 'S0B_probe'})
    cpb6 = load_exp878(env883, dict(entry6, file=_o6.path.join(sb6.root, eid6 + '.pt')))
    b0['bank_copy_reload_bitwise'] = torch.equal(cpb6['h'], cp6['h']) and all(torch.equal(a, b) for x, y in zip(cpb6['lower'], cp6['lower']) for a, b in zip(x, y))
    drop_m6('cpb6')
    bad_file = scratch6 / 'corrupt.pt'; bad_file.write_bytes(raw6[:-1] + bytes([raw6[-1] ^ 1]))
    try: load_exp878(env883, dict(entry6, file=str(bad_file))); b0['file_corruption_refused'] = False
    except Persist878 as exc: b0['file_corruption_refused'] = 'FILE_SHA' in str(exc)
    cpt = torch.load(entry6['file'], map_location='cpu', weights_only=True)
    cpt['h'] = cpt['h'].clone(); cpt['h'][0, -1, 0] = cpt['h'][0, -1, 0] + 1
    tfile = scratch6 / 'tensor_mismatch.pt'; torch.save(cpt, tfile); del cpt
    try: load_exp878(env883, dict(entry6, file=str(tfile), sha256=sha256_file864(tfile))); b0['tensor_sha_mismatch_refused'] = False
    except Persist878 as exc: b0['tensor_sha_mismatch_refused'] = 'TENSOR_SHA' in str(exc)
    try: sb6.commit(eid6 + '.pt', raw6, {}); b0['duplicate_refused'] = False
    except AssertionError: b0['duplicate_refused'] = True
    open(_o6.path.join(sb6.root, 'interrupted.pt.tmp'), 'wb').write(b'partial')
    open(_o6.path.join(sb6.root, 'after_rename_before_manifest.pt'), 'wb').write(raw6)
    vs6 = sb6.verify(); gone6 = sb6.cleanup_orphans(); vs7 = sb6.verify()
    b0['scratch_orphan_temp_removed'] = vs6['tmp_orphans'] == ['interrupted.pt.tmp'] and gone6 == ['interrupted.pt.tmp']
    b0['scratch_final_orphan_quarantined_not_deleted'] = vs7['quarantine'] == ['after_rename_before_manifest.pt'] and \
        _o6.path.exists(_o6.path.join(sb6.root, 'after_rename_before_manifest.pt')) and vs7['ok'] is False
    open(sb6.manifest, 'ab').write(b'{"truncated":')
    b0['scratch_malformed_manifest_structured'] = sb6.verify()['ok'] is False and bool(sb6.verify()['malformed'])
    b0['live_bank_unchanged_by_diagnostics'] = BANK6.head_sha() == bank_head0 and BANK6.verify()['entries'] == 0
    S0_RESULTS_M6['S0B'] = dict(b0, cartridge={k: entry6[k] for k in ('id', 'file', 'sha256', 'bytes', 'body_tokens', 'roundtrip_K_rel')},
                                scratch_commit=srec6)
    HDO6.emit('08', 'PHYSICAL_WRITE_REVISION', S0_RESULTS_M6['S0B'], event='S0B')
    if not all(v for v in b0.values()): gate883('S0B', 'BLOCK', checks=b0)
    gate883('S0B', 'PASS', checks=b0)
    # ---------------- S0E (lower boundary / upper rebuild) ----------------
    STATE883['status'] = 'S0E'
    try:
        m_before = alloc_gib_m6()
        G_nat = run_m6('S0E_native_append', 'compile', append_exp878, env883, B6, cp6)
        G_x = run_m6('S0E_explicit_append', 'compile', xappend878, env883, B6, cp6, ())
        STATE_M6['measure']['rebuild_gib'] = [round(max(alloc_gib_m6() - m_before, 0.0) / 2, 4)]
        cp6p = dict(cp6); cp6p['h'] = (cp6['h'].float() * (1.0 + 2.0 ** -6)).to(cp6['h'].dtype)
        G_p = run_m6('S0E_perturbed', 'compile', xappend878, env883, B6, cp6p, ())
        sl6 = slice(nB6, nB6 + SLOTS_M6)
        nk6 = next_kv878(env883, cp6['h'][:, P6:], nB6)
        e0 = {'native_append_equals_explicit_append': all(torch.equal(a, b) for i in range(NL6) for a, b in zip(G_nat[i], G_x[i])),
              'B_prefix_all_80_layers_unchanged': all(torch.equal(G_x[i][t][:, :, :nB6], B6[i][t]) for i in range(NL6) for t in (0, 1)),
              'layer4_slot_KV_equals_next_kv878_of_H3': all(torch.equal(nk6[t], G_x[CUT6 + 1][t][:, :, sl6]) for t in (0, 1)),
              'perturbed_H3_changes_every_upper_layer_K_and_V': all(not torch.equal(G_p[i][t][:, :, sl6], G_x[i][t][:, :, sl6])
                                                                    for i in range(CUT6 + 1, NL6) for t in (0, 1)),
              'perturbed_H3_leaves_lower_layers_K_and_V': all(torch.equal(G_p[i][t][:, :, sl6], G_x[i][t][:, :, sl6]) for i in range(CUT6 + 1) for t in (0, 1)),
              'shape_dtype_device': all(G_x[i][t].dtype == torch.bfloat16 and G_x[i][t].is_cuda and int(G_x[i][t].shape[2]) == nB6 + SLOTS_M6
                                        for i in range(NL6) for t in (0, 1)),
              'finite': all(bool(torch.isfinite(G_x[i][t]).all()) for i in range(NL6) for t in (0, 1))}
    finally:
        drop_m6('G_p', 'G_nat', 'nk6', 'cp6p')
    S0_RESULTS_M6['S0E'] = dict(e0, native_append_semantics='native_append_direct injects H3 by temporarily substituting layer %d forward '
                                                            '(DirectCut3 "inject"); not a registered hook; the explicit xappend878 path '
                                                            'has no substitution and is used for every Stage-1 slot mount' % CUT6)
    HDO6.emit('08', 'UPPER_REBUILD', S0_RESULTS_M6['S0E'], event='S0E')
    if not all(e0.values()): gate883('S0E', 'BLOCK', checks=e0)
    gate883('S0E', 'PASS', checks=e0)
    # ---------------- S0D (R=0, g, mask, RoPE, GQA, permutation, finite) ----------------
    STATE883['status'] = 'S0D'
    try:
        cols6 = [(nB6, nB6 + SLOTS_M6)]
        rG1 = run_m6('S0D_g1', 'diag_read', m6_car, env883, G_x, X6)
        rG1e = run_m6('S0D_g1e', 'diag_read', m6_car, env883, G_x, X6, cols6, 0.0)
        rG0 = run_m6('S0D_g0', 'diag_read', m6_car, env883, G_x, X6, cols6, float('-inf'))
        rG2 = run_m6('S0D_g2', 'diag_read', m6_car, env883, G_x, X6, cols6, _mt6.log(2.0))
        blk6 = run_m6('S0D_block', 'admissibility', gate_block_gpu_m6, env883, G_x, X6, nB6, nB6 + SLOTS_M6)
        perm6 = list(range(SLOTS_M6))[::-1]
        pick = lambda t, idx, dim: torch.cat([t.narrow(dim, 0, P6), t.narrow(dim, P6, SLOTS_M6).index_select(dim, torch.tensor(idx, device=t.device))], dim=dim)
        cpr = {'h': pick(cp6['h'], perm6, 1), 'n': cp6['n'], 'p': cp6['p'], 'body_tokens': cp6['body_tokens'],
               'lower': tuple((pick(k, perm6, 2), pick(v, perm6, 2)) for k, v in cp6['lower'])}
        canon = sorted(range(SLOTS_M6), key=lambda j: perm6[j])        # canonical storage order = source row order
        cpc = {'h': pick(cpr['h'], canon, 1), 'n': cp6['n'], 'p': cp6['p'], 'body_tokens': cp6['body_tokens'],
               'lower': tuple((pick(k, canon, 2), pick(v, canon, 2)) for k, v in cpr['lower'])}
        canon_tensors_ok = torch.equal(cpc['h'], cp6['h']) and all(torch.equal(a, b) for x, y in zip(cpc['lower'], cp6['lower']) for a, b in zip(x, y))
        G_c = xappend878(env883, B6, cpc, ()); rC = run_m6('S0D_canon', 'diag_read', m6_car, env883, G_c, X6); drop_m6('G_c')
        G_raw = xappend878(env883, B6, cpr, ()); rRaw = run_m6('S0D_raw', 'diag_read', m6_car, env883, G_raw, X6); drop_m6('G_raw')
        fin = lambda r: all(_mt6.isfinite(s['sequence_logp']) for s in r['scores'])
        d0 = {'R0_parity_bitwise': c0['m6_car_R0_equals_native'],
              'explicit_mask_g1_within_cap': m6_reading_delta(rG1, rG1e) <= GATE_TOL_CAP_M6,
              'g0_within_cap': m6_reading_delta(rG0, r_m6) <= GATE_TOL_CAP_M6,
              'g2_finite': fin(rG2), 'all_finite': all(fin(r) for r in (rG1, rG1e, rG0, rG2, rRaw, rC)),
              'layer0_block_identity_g_0_05_1_2': blk6['block_identity_ok'], 'layer0_slot_mass_monotone_g0_zero': blk6['mass_monotone_and_g0_zero'],
              'rope_canonical_roundtrip_ok': entry6['roundtrip_K_rel'] <= ROPE_REL_CAP_M6,
              'canonical_restore_H3_and_all_lower_KV_bitwise': canon_tensors_ok,
              'canonical_restore_reading_bitwise': same_reading881(rC, rG1),
              'gqa_64q_8kv_128': int(G_x[0][0].shape[1]) == 8 and int(G_x[0][0].shape[-1]) == 128 and STATE883.get('api', {}).get('shape', [0, 0, 0, 0, 0])[2:5] == [64, 8, 128]}
        meas_d0 = {'explicit_mask_g1_vs_implicit_delta_nats': m6_reading_delta(rG1, rG1e), 'g0_vs_no_slot_delta_nats': m6_reading_delta(rG0, r_m6),
                   'determinism_delta_nats': m6_reading_delta(r_m6, r_m6b), 'raw_permutation_delta_nats': m6_reading_delta(rRaw, rG1),
                   'layer0': blk6}
        rows6 = []
        for name, r in (('NO_SLOT', r_m6), ('SLOT_G1_IMPLICIT', rG1), ('SLOT_G1_EXPLICIT', rG1e), ('SLOT_G0', rG0), ('SLOT_G2', rG2),
                        ('SLOT_RAW_PERMUTED', rRaw), ('SLOT_CANONICAL_RESTORED', rC)):
            v = six_view_m6(r); base_ = six_view_m6(r_m6)
            rows6.append({'condition': name, 'logp': v['logp'], 'rank': v['full_rank'], 'delta_from_NO': {w: v['logp'][w] - base_['logp'][w] for w in ACTIONS_M6},
                          'delta_from_TRUE': 'NOT_APPLICABLE (no TRUE cartridge in Stage 0)', 'LIVE_BANK_MUTATED': False, 'OUTCOME': 'NOT_EXECUTED'})
            if v['full_rank'] != base_['full_rank']:
                STATE_M6['anomalies'].append({'kind': 'FULL_RANK_CHANGE', 'stage': 'S0D', 'condition': name, 'from': base_['full_rank'], 'to': v['full_rank']})
    finally:
        drop_m6('cpr', 'cpc', 'G_x', 'G_c', 'G_raw')
    S0_RESULTS_M6['S0D'] = dict(d0, measured=meas_d0)
    HDO6.emit('09', 'ISOLATED_COUNTERFACTUALS', {'snapshot': SNAP6['state_sha256'], 'rows': rows6, 'measured': meas_d0,
                                                 'slots': 'mechanical probe rows (first %d X rows), not memory content; g>0 is an attention intervention' % SLOTS_M6},
               event='S0D')
    if not all(d0.values()): gate883('S0D', 'BLOCK', checks=d0)
    gate883('S0D', 'PASS', checks=d0)
    drop_m6('cp6', 'h36', 'B6', 'X6')
    SNAP6.pop('B', None); SNAP6.pop('X', None)
    # ---------------- S0F (post-commit observer OFF / ON parity) ----------------
    STATE883['status'] = 'S0F'
    guard883('S0F_pre')
    bankF0 = BANK6.head_sha(); rngS = rng_snapshot_m6(); rng0 = rng_sha_m6()
    OBS_M6 = []
    EPISODE_OBSERVER883 = None
    epA = episode883(env883, SPEC_M6, 'NOFB', 'T866_S0F_OFF', 2)
    rngA = rng_sha_m6(); obs_after_off = len(OBS_M6)
    rng_restore_m6(rngS)
    rng_restored_ok = rng_sha_m6() == rng0
    EPISODE_OBSERVER883 = lambda ep_, st_: OBS_M6.append((ep_, st_))
    try:
        epB = episode883(env883, SPEC_M6, 'NOFB', 'T866_S0F_ON', 2)
    finally:
        EPISODE_OBSERVER883 = None
    rngB = rng_sha_m6()
    guard883('S0F_post')
    emit_episode_m6(HDO6, epB, 'OBSERVER_ON')
    six_ = lambda ep: [[(s_['word'], s_['token_logps'], s_['sequence_logp']) for s_ in st_['reading']['scores']] for st_ in ep['steps']]
    rank_ = lambda ep: [six_view_m6(st_['reading'])['full_rank'] for st_ in ep['steps']]
    effk = ('effect', 'chosen', 'mounted_before', 'mounted_after', 'path_after', 'address_origin', 'executed_equals_reading')
    eff_ = lambda ep: [{k: (st_.get('effect') or {}).get(k) for k in effk} for st_ in ep['steps']]
    f0 = {'rng_restored_before_ON': rng_restored_ok, 'OFF_built_no_observation': obs_after_off == 0,
          'ON_observed_every_step': len(OBS_M6) == len(epB['steps']) and not epB.get('observer_errors'),
          'actions_equal': epA['actions'] == epB['actions'], 'six_token_and_sequence_logps_bitwise': six_(epA) == six_(epB),
          'ranks_equal': rank_(epA) == rank_(epB), 'effects_chosen_path_mounts_equal': eff_(epA) == eff_(epB),
          'end_equal': epA['end'] == epB['end'] and epA['final_mounted'] == epB['final_mounted'] and epA['path'] == epB['path'],
          'native_call_counts_equal': epA['calls'] == epB['calls'] and [s_['calls'] for s_ in epA['steps']] == [s_['calls'] for s_ in epB['steps']],
          'rng_final_equal': rngA == rngB, 'start_seal_equal': epA['start']['initial_seal'] == epB['start']['initial_seal'],
          'restore_both': epA['exact_restore_vs_first_mount'] is True and epB['exact_restore_vs_first_mount'] is True,
          'bank_manifest_unchanged': BANK6.head_sha() == bankF0, 'both_natural_end': natural_end883(epA['end'], 2) and natural_end883(epB['end'], 2),
          'event_contract_both': epA['event_contract']['ok'] and epB['event_contract']['ok']}
    STATE_M6['measure']['live_step'] = [s_['seconds'] for e_ in (epA, epB) for s_ in e_['steps']]
    STATE_M6['measure']['live_step_calls'] = [s_['calls'] for e_ in (epA, epB) for s_ in e_['steps']]
    S0_RESULTS_M6['S0F'] = f0
    HDO6.emit('10', 'EPISODE_TIMELINE', {'label': 'OBSERVER_OFF_RUN (reported after both runs)', 'actions': epA['actions'],
                                         'effects': epA['effects'], 'end': epA['end'], 'parity': f0}, event='S0F', episode=epA['episode_id'])
    if not all(f0.values()): gate883('S0F', 'BLOCK', checks=f0)
    gate883('S0F', 'PASS', checks=f0)
    # ---------------- S0G (measured resources; sealed Stage-1 workload admission) ----------------
    STATE883['status'] = 'S0G'
    peak_update881()
    M6m = STATE_M6['measure']; M6m['hdo_s_total'] = round(STATE_M6['hdo_s'], 3)
    elapsed6 = time.perf_counter() - T_START883
    clocks6 = budget_clocks883(env883, 'S0G')
    g0 = {'elapsed_s': round(elapsed6, 1), 'measure': {k: v for k, v in M6m.items()}, 'clocks': clocks6,
          'peak_alloc_gib': STATE883['budget']['peak_alloc_gib'], 'peak_reserved_gib': STATE883['budget']['peak_reserved_gib'],
          'free_gib': round(free_gib881(), 2), 'ram': proc_ram_gib_m6(), 'disk_free_gib': round(_s883.disk_usage(str(ROOT864)).free / 2**30, 2)}
    adm = {}
    try:
        adm['time'] = stage1_projection_m6(elapsed6, M6m, S1_PLAN_M6['workload'], OFFLINE_RESERVE_S883, WALL_S883)
        slot_gib = SLOTS_M6 * 80 * 4096 * 2 / 2**30
        adm['vram'] = memory_projection_m6(float(STATE883['budget']['peak_reserved_gib']), max(M6m['transient_gib']),
                                           max(M6m['rebuild_gib']), slot_gib, 0.01, float(CC_GPU['total_gib']) - FREE_MIN_GIB883)
        calls_need = S1_PLAN_M6['workload']['live_steps'] * max(M6m['live_step_calls']) + \
            S1_PLAN_M6['workload']['snapshots'] * max(1, int(SNAP6['calls'])) + S1_PLAN_M6['workload']['reads'] + 50
        adm['calls'] = (finite_nonneg_m6(clocks6['calls_left']) and clocks6['calls_left'] >= calls_need, calls_need)
        adm['ram'] = (g0['ram'].get('available_gib', -1) >= RAM_MIN_GIB_M6, g0['ram'].get('available_gib'))
        adm['disk'] = (g0['disk_free_gib'] >= DISK_NEED_GIB_M6, g0['disk_free_gib'])
        adm['all_measured'] = (all(finite_nonneg_m6(x) for k in ('live_step', 'compile', 'diag_read', 'admissibility', 'snapshot',
                                                                 'transient_gib', 'rebuild_gib') for x in M6m.get(k, [None])), None)
    except (ValueError, KeyError, TypeError) as exc:
        adm['error'] = (False, '%s: %s' % (type(exc).__name__, exc))
    g0['admission'] = {k: {'admitted': v[0], 'value': v[1]} for k, v in adm.items()}
    S0_RESULTS_M6['S0G'] = g0
    HDO6.emit('02', 'MEASURED_BUDGET', g0, event='S0G')
    if not adm or not all(v[0] is True for v in adm.values()): gate883('S0G', 'BLOCK', admission=g0['admission'])
    gate883('S0G', 'PASS', admission=g0['admission'])
    ARTIFACTS_M6['stage0'] = write_json_sha_m6('TEST866_stage0.json', {'status': 'STAGE0_PASS', 'results': S0_RESULTS_M6})
    STATE883['result'] = {'result': 'INCONCLUSIVE', 'labels': ['STAGE0_PASS', 'STAGE1_PENDING'], 'reason': 'Stage 0 passed'}
    # ======================= STAGE 1 (automatic) =======================
    STATE883['status'] = 'S1R'
    eps6 = max(EPS_FLOOR_M6, EPS_MULT_M6 * max(meas_d0['explicit_mask_g1_vs_implicit_delta_nats'], meas_d0['g0_vs_no_slot_delta_nats'],
                                               meas_d0['determinism_delta_nats']))
    st0 = blk6.get('stats') or {}
    if not st0: raise Readiness866('S1-B3 NO_ADMISSIBILITY_CALIBRATION')
    cal6 = {'epsilon_num': eps6, 'logit_margin': max(0.0, st0['slot_logit_max'] - st0['native_q01_q50_q99'][2]) + ADMIT_LOGIT_PAD_M6,
            'ratio_cap': max(ADMIT_RATIO_MULT_M6 * st0['ratio_Zc_over_Zb_mean'], ADMIT_RATIO_MIN_M6), 'source': 'Stage-0 S0D measurements only'}
    if not all(finite_nonneg_m6(v) for k, v in cal6.items() if k != 'source'): raise Readiness866('S1-B3 CALIBRATION_NOT_FINITE %s' % cal6)
    S1_PRESEAL_M6 = {'status': 'PRESEAL_A', 'plan': S1_PLAN_M6, 'calibration': cal6, 'stage0_admission': g0['admission'],
                     'written_before_any_stage1_reading': True, 'prereg_sha256': PREREG_M6_SHA}
    ARTIFACTS_M6['preseal'] = write_json_sha_m6('TEST866_stage1_preseal.json', S1_PRESEAL_M6)
    HDO6.emit('02', 'STAGE1_PRESEAL_A', {'calibration': cal6, 'plan_sha256': _h6.sha256(hdo_canon_m6(S1_PLAN_M6).encode()).hexdigest(),
                                         'preseal_file': ARTIFACTS_M6['preseal']}, event='S1R')
    # ---- histories: two natural REC episodes, experience committed to the persistent bank ----
    STATE883['status'] = 'S1H'
    EVENTS_M6 = {}
    for hj in S1_PLAN_M6['histories']:
        ok_, proj_ = cell_admission883(time.perf_counter() - T_START883, STATE_M6['measure']['live_step'], STATE883['budget']['episode_overhead_s'] or [0.0],
                                       len(S1_PLAN_M6['histories']))
        if not ok_: raise Budget883('S1_HISTORY_ADMISSION %s projected %s' % (hj['id'], proj_))
        EVENTS_M6[hj['id']] = []
        REC_SINK883 = rec_sink_m6(BANK6, HDO6, EVENTS_M6[hj['id']])
        try:
            epH = episode883(env883, by_key883[tuple(hj['history'])], 'REC', 'T866_%s_REC' % hj['id'], S1_PLAN_M6['history_horizon'])
        finally:
            REC_SINK883 = None
        STATE_M6['measure']['live_step'] += [s_['seconds'] for s_ in epH['steps']]
        emit_episode_m6(HDO6, epH, 'STAGE1_HISTORY_' + hj['id'])
        if not natural_end883(epH['end'], S1_PLAN_M6['history_horizon']): raise Readiness866('S1-B1 HISTORY_NOT_NATURAL %s %s' % (hj['id'], epH['end']))
    bank_v = BANK6.verify()
    if not bank_v['ok']: raise Gate883('S1_BANK_VERIFY %s' % bank_v)
    # ---- preseal B: events, test snapshots, compiled slot sets, admissibility; NO Stage-1 CAR value yet ----
    STATE883['status'] = 'S1P'
    S1W = {}
    for hj in S1_PLAN_M6['histories']:
        hid = hj['id']; evs = EVENTS_M6[hid]
        ep_ = next((e for e in evs if e['outcome']['effect'] == 'MOUNTED' and e['outcome']['action'] == S1_PLAN_M6['a_plus']), None)
        e0_ = next((e for e in evs if e['outcome']['effect'] == 'POINTER_ADVANCED' and e['outcome']['action'] == S1_PLAN_M6['a_zero']), None)
        if ep_ is None or e0_ is None:
            raise Readiness866('S1-B1 EVENT_PAIR_ABSENT %s (events %s)' % (hid, [(e['outcome']['action'], e['outcome']['effect']) for e in evs]))
        snapT = run_m6('S1_snapshot_' + hid, 'snapshot', snapshot_m6, env883, by_key883[tuple(hj['test'])], 'S1_' + hid)
        if ep_['C_rows_sha256'] == snapT['c_rows_sha256'] or ep_['X_sha256'] == snapT['X_sha256']:
            raise Readiness866('S1-B1 EXACT_ECHO %s (history rows identical to the test context rows)' % hid)
        cpP = load_event_cp_m6(env883, ep_); cp0 = load_event_cp_m6(env883, e0_)
        Pn = int(env883['P'])
        try:
            slots_true = role_slots_m6(env883, cpP, cpP, Pn, 'BARY')
            sets = {'TRUE': slots_true, 'WRONG_OUTCOME': role_slots_m6(env883, cpP, cp0, Pn, 'BARY'),
                    'SHUFFLED_HISTORY': shuffled_slots_m6(slots_true), 'MATCHED_GEOMETRY': geometry_slots_m6(env883, cp0, Pn, slots_true),
                    'MEDOID_UNION': role_slots_m6(env883, cpP, cpP, Pn, 'MEDOID')}
            cpI = load_event_cp_m6(env883, ep_)                  # independent reload of the bank copy
            sets['INERT_RECOMPUTE'] = role_slots_m6(env883, cpI, cpI, Pn, 'BARY'); del cpI
        except ValueError as exc:
            raise Readiness866('S1-B2 SLOT_COMPILE %s %s' % (hid, exc))
        cps = {k: run_m6('S1_compile_%s_%s' % (hid, k), 'compile', assemble_cp_m6, env883, v) for k, v in sets.items()}
        dig = {k: cp_digest_m6(v) for k, v in cps.items()}
        nBT = snapT['B_tokens']; adm_ = {}
        for k, cpk in cps.items():
            Gk = xappend878(env883, snapT['B'], cpk, ())
            adm_[k] = run_m6('S1_admit_%s_%s' % (hid, k), 'admissibility', admissible_m6, env883, Gk, snapT['X'], nBT, cpk, cpP, cal6)
            del Gk; gc.collect(); torch.cuda.empty_cache()
        adm_['ECHO_MASKED'] = adm_['TRUE']
        S1W[hid] = {'e_plus': ep_, 'e_zero': e0_, 'snap': snapT, 'cps': cps, 'digests': dig, 'admissible': {k: v[0] for k, v in adm_.items()},
                    'admissibility': {k: v[1] for k, v in adm_.items()}}
        del cpP, cp0, sets, slots_true
    pre_b = {hid: {'e_plus': {k: w['e_plus'][k] for k in ('event_id', 'outcome', 'cartridge_id', 'source_sha256', 'bank_seq')},
                   'e_zero': {k: w['e_zero'][k] for k in ('event_id', 'outcome', 'cartridge_id', 'source_sha256', 'bank_seq')},
                   'test_snapshot': {k: w['snap'][k] for k in ('state_sha256', 'X_sha256', 'B_tokens', 'B_seal', 'c_rows_sha256')},
                   'slot_digests': w['digests'], 'admissible': w['admissible'], 'admissibility': w['admissibility'],
                   'inert_digest_equals_true': w['digests']['INERT_RECOMPUTE'] == w['digests']['TRUE']} for hid, w in S1W.items()}
    S1_PRESEAL_M6 = dict(S1_PRESEAL_M6, status='PRESEAL_B_SEALED', histories=pre_b, bank_manifest_sha256=BANK6.head_sha(),
                         sealed_at_s=round(time.perf_counter() - T_START883, 1))
    ARTIFACTS_M6['preseal'] = write_json_sha_m6('TEST866_stage1_preseal.json', S1_PRESEAL_M6)
    HDO6.emit('02', 'STAGE1_PRESEAL_B', {'histories': pre_b, 'preseal_file': ARTIFACTS_M6['preseal']}, event='S1P')
    ok_, proj_ = admission_m6(time.perf_counter() - T_START883, 2, max(STATE_M6['measure']['diag_read']) * 8,
                              max(STATE_M6['measure']['diag_read']) * 0, max(STATE_M6['measure']['compile']) * 7, OFFLINE_RESERVE_S883, WALL_S883)
    if not ok_: raise Budget883('S1_READ_ADMISSION projected %s' % proj_)
    # ---- Stage-1 readings (isolated; nothing executed; the bank is not written) ----
    STATE883['status'] = 'S1X'
    bank_before_reads = BANK6.head_sha()
    a_p, a_0 = S1_PLAN_M6['a_plus'], S1_PLAN_M6['a_zero']
    S1_RESULTS_M6 = {'status': 'RUNNING', 'histories': {}}
    labels6 = []
    for hj in S1_PLAN_M6['histories']:
        hid = hj['id']; w = S1W[hid]; snapT = w['snap']; nBT = snapT['B_tokens']
        guard883('S1X_%s_pre' % hid)
        R = {'NO_MEMORY': run_m6('S1_read_%s_NO' % hid, 'diag_read', m6_car, env883, snapT['B'], snapT['X'])}
        for k in ('TRUE', 'WRONG_OUTCOME', 'SHUFFLED_HISTORY', 'MATCHED_GEOMETRY', 'INERT_RECOMPUTE', 'MEDOID_UNION'):
            Gk = xappend878(env883, snapT['B'], w['cps'][k], ())
            R[k] = run_m6('S1_read_%s_%s' % (hid, k), 'diag_read', m6_car, env883, Gk, snapT['X'])
            if k == 'TRUE':
                R['ECHO_MASKED'] = run_m6('S1_read_%s_ECHO' % hid, 'diag_read', m6_car, env883, Gk, snapT['X'], [(nBT, nBT + 5)], float('-inf'))
            del Gk; gc.collect(); torch.cuda.empty_cache()
        lp = {k: six_view_m6(v)['logp'] for k, v in R.items()}
        D = {k: directional_d_m6(lp[k], lp['NO_MEMORY'], a_p, a_0) for k in R if k != 'NO_MEMORY'}
        inert_ok = pre_b[hid]['inert_digest_equals_true'] and abs(D['INERT_RECOMPUTE'] - D['TRUE']) <= eps6
        lab, why = stage1_history_verdict_m6(D, eps6, w['admissible'], inert_ok)
        labels6.append(lab)
        rows = []
        for k in S1_CONDITIONS_M6:
            v = six_view_m6(R[k]); b_ = six_view_m6(R['NO_MEMORY']); t_ = six_view_m6(R['TRUE'])
            rows.append({'condition': k, 'logp': v['logp'], 'rank': v['full_rank'], 'selected': v['selected'],
                         'delta_from_NO': {a: v['logp'][a] - b_['logp'][a] for a in ACTIONS_M6},
                         'delta_from_TRUE': {a: v['logp'][a] - t_['logp'][a] for a in ACTIONS_M6},
                         'D': D.get(k), 'admissible': w['admissible'].get(k, True), 'LIVE_BANK_MUTATED': False, 'OUTCOME': 'NOT_EXECUTED'})
            if v['full_rank'] != b_['full_rank']:
                STATE_M6['anomalies'].append({'kind': 'FULL_RANK_CHANGE', 'stage': 'S1', 'history': hid, 'condition': k, 'from': b_['full_rank'], 'to': v['full_rank']})
            if (v['margin'] or 0) * (b_['margin'] or 0) < 0:
                STATE_M6['anomalies'].append({'kind': 'MARGIN_SIGN_FLIP', 'stage': 'S1', 'history': hid, 'condition': k})
        S1_RESULTS_M6['histories'][hid] = {'D': D, 'epsilon_num': eps6, 'inert_ok': inert_ok, 'label': lab, 'reason': why, 'rows': rows}
        HDO6.emit('09', 'ISOLATED_COUNTERFACTUALS', {'history': hid, 'a_plus': a_p, 'a_zero': a_0, 'epsilon_num': eps6, 'rows': rows,
                                                     'label': lab, 'reason': why}, event='S1X', episode=hid)
    if BANK6.head_sha() != bank_before_reads: raise Gate883('S1_READS_MUTATED_BANK')
    STATE883['status'] = 'S1A'
    s1_label = stage1_combine_m6(labels6)
    S1_RESULTS_M6.update({'status': 'COMPLETE', 'label': s1_label, 'history_labels': labels6, 'bank_unchanged_by_reads': True})
    ARTIFACTS_M6['stage1'] = write_json_sha_m6('TEST866_stage1_results.json', S1_RESULTS_M6)
    HDO6.emit('11', 'TRANSFER_AND_REVISION', {'status': 'NOT_RUN', 'reason': 'Stage 2-4 are not part of TEST866'})
    HDO6.emit('12', 'ANOMALY_CANDIDATES', {'candidates': STATE_M6['anomalies'], 'note': 'ANOMALY_CANDIDATE only, never a PASS'})
    STATE_M6['verdict'] = {'stage0': 'PASS', 'stage1': s1_label, 'label': s1_label, 'history_labels': labels6,
                           'not_claimed': PREREG_M6['never_claimed']}
    HDO6.emit('13', 'STAGE_VERDICT', STATE_M6['verdict'])
    STATE883['result'] = {'result': s1_label, 'labels': ['STAGE0_PASS', 'STAGE1_COMPLETE', s1_label], 'reason': 'sealed Stage-1 rule'}
    STATE883['status'] = 'COMPLETE'
except Readiness866 as exc:
    STATE883['error'] = 'Readiness866: %s' % exc; STATE883['traceback'] = traceback.format_exc()
    STATE883['result'] = {'result': 'INCONCLUSIVE', 'labels': ['STAGE0_PASS', 'STAGE1_READINESS_BLOCK', 'STAGE1_NOT_RUN'], 'reason': str(exc)[:400],
                          'PARTIAL_PASS': False}
    S1_RESULTS_M6 = {'status': 'NOT_RUN', 'reason': str(exc)}
    STATE883['status'] = 'READINESS_BLOCK_AT_' + str(STATE883['status'])
except Budget883 as exc:
    STATE883['error'] = str(exc); STATE883['traceback'] = traceback.format_exc()
    STATE883['result'] = {'result': 'INCOMPLETE_BUDGET', 'labels': ['TECHNICAL_BLOCK', 'STAGE1_NOT_RUN' if S1_RESULTS_M6.get('status') != 'RUNNING' else 'STAGE1_INCOMPLETE'],
                          'reason': str(exc)[:400], 'PARTIAL_PASS': False}
    STATE883['gates'].setdefault(str(STATE883['status']), gate_fail_record883(STATE883['status'], STATE883['error']))
    STATE883['status'] = 'BUDGET_STOP_AT_' + str(STATE883['status'])
except BaseException as exc:
    STATE883['error'] = '%s: %s' % (type(exc).__name__, exc); STATE883['traceback'] = traceback.format_exc()
    STATE883['result'] = {'result': 'TECHNICAL_BLOCK', 'labels': ['FAILED_AT_' + str(STATE883['status']), 'STAGE1_NOT_RUN'],
                          'reason': STATE883['error'][:400], 'PARTIAL_PASS': False}
    STATE883['gates'].setdefault(str(STATE883['status']), gate_fail_record883(STATE883['status'], STATE883['error']))
    STATE883['status'] = 'FAILED_AT_' + str(STATE883['status'])
    print('TEST866 ERROR', STATE883['error'][:300], file=ERROR_CONSOLE864, flush=True)
    print(STATE883['traceback'], file=ERROR_CONSOLE864, flush=True)
finally:
    EPISODE_OBSERVER883 = None; REC_SINK883 = None
    FINAL_M6 = {'checks': {}, 'errors': []}
    try:
        (ROOT864 / 'TEST866_traceback.txt').write_text(STATE883.get('traceback') or 'NO_EXCEPTION\n', encoding='utf-8')
    except Exception as exc: FINAL_M6['errors'].append('TRACEBACK_WRITE %s: %s' % (type(exc).__name__, exc))
    try:
        if _o883.path.exists(CART_ROOT883): _s883.rmtree(CART_ROOT883)     # episode cartridges only; m6_bank is kept
    except Exception as exc: FINAL_M6['errors'].append('CART_ROOT %s: %s' % (type(exc).__name__, exc))
    try:
        bv_ = BANK6.verify() if BANK6 is not None else {'ok': True, 'entries': 0, 'note': 'bank not created'}
        FINAL_M6['checks']['bank_verify'] = bv_['ok']; FINAL_M6['bank'] = bv_
    except Exception as exc: FINAL_M6['checks']['bank_verify'] = False; FINAL_M6['errors'].append('BANK_VERIFY %s: %s' % (type(exc).__name__, exc))
    if HDO6 is not None:
        try:
            if STATE883['status'] != 'COMPLETE':
                HDO6.emit('15', 'SAFE_STOP', {'exception': STATE883.get('error'), 'traceback': STATE883.get('traceback'),
                                              'last_safe_seal': HDO6.parent, 'partial_bank_manifest_sha256': BANK6.head_sha() if BANK6 else None,
                                              'result': STATE883['result'], 'PARTIAL_PASS': False,
                                              'not_run': 'every gate after %s' % STATE883['status']})
            HDO6.emit('14', 'FINAL_RESEARCHER_VIEW', {'status': STATE883['status'], 'result': STATE883['result'],
                                                      'gates': {k: v.get('status') for k, v in STATE883['gates'].items()},
                                                      'stage1': {k: v for k, v in S1_RESULTS_M6.items() if k != 'histories'},
                                                      'bank': FINAL_M6.get('bank'), 'cleanup_errors': STATE883['cleanup_errors'] + STATE_M6['cleanup_errors'],
                                                      'GPU_EXECUTION_NOT_VERIFIED_BY_AUTHOR': True, 'HDO_VIEW_TRUNCATION': 'UNKNOWN'})
            info6 = HDO6.close(); chain6 = hdo_verify_chain_m6(info6['path'])
            FINAL_M6['hdo'] = dict(info6, chain=chain6); FINAL_M6['checks']['hdo_closed'] = True; FINAL_M6['checks']['hdo_chain'] = chain6['ok']
        except Exception as exc:
            FINAL_M6['checks']['hdo_closed'] = False; FINAL_M6['errors'].append('HDO %s: %s' % (type(exc).__name__, exc))
            FINAL_M6['hdo_traceback'] = traceback.format_exc()
    else:
        FINAL_M6['checks']['hdo_closed'] = STATE883['status'].startswith(('FAILED_AT_G0', 'BUDGET_STOP_AT_G0'))
    try:
        json_write864('TEST866_gate_status.json', STATE883['gates']); json_write864('gate_status.json', STATE883['gates'])
        if 'stage0' not in ARTIFACTS_M6: ARTIFACTS_M6['stage0'] = write_json_sha_m6('TEST866_stage0.json', {'status': STATE883['status'], 'results': S0_RESULTS_M6})
        if 'stage1' not in ARTIFACTS_M6: ARTIFACTS_M6['stage1'] = write_json_sha_m6('TEST866_stage1_results.json', S1_RESULTS_M6)
        if 'preseal' not in ARTIFACTS_M6: ARTIFACTS_M6['preseal'] = write_json_sha_m6('TEST866_stage1_preseal.json', S1_PRESEAL_M6)
        FINAL_M6['checks']['artifacts_written'] = True
    except Exception as exc:
        FINAL_M6['checks']['artifacts_written'] = False; FINAL_M6['errors'].append('ARTIFACTS %s: %s' % (type(exc).__name__, exc))
    def final_report_m6():
        return _j883.loads(_j883.dumps({'state883': {k: v for k, v in STATE883.items() if k != 'episodes'}, 'm6': STATE_M6,
                                        'final': FINAL_M6, 'artifacts': ARTIFACTS_M6}, default=str))
    try:
        json_write864('TEST866_final_report.json', final_report_m6())
        req_ = ['TEST866.py', 'TEST866_source_manifest.json', 'TEST866_cpu_selftest.json', 'TEST866_gate_status.json', 'TEST866_hdo.log',
                'TEST866_stage0.json', 'TEST866_stage1_preseal.json', 'TEST866_stage1_results.json', 'TEST866_traceback.txt',
                'TEST866_final_report.json']
        present_ = [n for n in req_ if (ROOT864 / n).exists()]
        zp_ = ROOT864 / 'TEST866_results.zip'
        with _zf6.ZipFile(zp_, 'w', _zf6.ZIP_DEFLATED) as z_:
            for p_ in sorted(ROOT864.rglob('*')):
                if p_.is_file() and p_.name != 'TEST866_results.zip': z_.write(p_, str(p_.relative_to(ROOT864)))
        with _zf6.ZipFile(zp_) as z_:
            names_ = set(z_.namelist()); bad_ = z_.testzip()
        FINAL_M6['zip'] = {'path': str(zp_), 'sha256': sha256_bytes864(zp_.read_bytes()), 'entries': len(names_), 'testzip': bad_,
                           'required_present': present_, 'required_missing': sorted(set(req_) - set(present_))}
        FINAL_M6['checks']['zip_ok'] = bad_ is None and all(n in names_ for n in present_) and not FINAL_M6['zip']['required_missing']
        drv_ = '/content/drive/MyDrive'
        if _o6.path.isdir(drv_):
            try:
                dst_ = _o6.path.join(drv_, 'TEST866_' + STAMP864); _o6.makedirs(dst_, exist_ok=True)
                _s883.copy2(str(zp_), dst_)
                FINAL_M6['drive'] = {'copied': sha256_bytes864(open(_o6.path.join(dst_, zp_.name), 'rb').read()) == FINAL_M6['zip']['sha256'], 'path': dst_}
            except Exception as exc: FINAL_M6['drive'] = {'copied': False, 'error': '%s: %s' % (type(exc).__name__, exc)}
        else:
            FINAL_M6['drive'] = {'copied': False, 'reason': 'Drive not mounted; local artifacts only'}
    except Exception as exc:
        FINAL_M6['checks']['zip_ok'] = False; FINAL_M6['errors'].append('ZIP %s: %s' % (type(exc).__name__, exc))
    # B08: any finalisation failure revokes the previous labels (fail-closed)
    fin_ok_ = all(v is True for v in FINAL_M6['checks'].values()) and not FINAL_M6['errors'] and not STATE_M6['cleanup_errors']
    if not fin_ok_ and (STATE883['result'] or {}).get('result') != 'TECHNICAL_BLOCK':
        STATE883['result'] = {'result': 'TECHNICAL_BLOCK', 'labels': ['FINALIZATION_FAILED'], 'revoked': STATE883['result'],
                              'reason': 'finalisation checks %s errors %s' % (FINAL_M6['checks'], FINAL_M6['errors'][:3]), 'PARTIAL_PASS': False}
        STATE883['status'] = 'FINALIZATION_FAILED_AFTER_' + str(STATE883['status'])
    FINAL_M6['final_ok'] = fin_ok_
    try: json_write864('TEST866_final_report.json', final_report_m6())       # outside the ZIP when finalisation changed it
    except Exception as exc: print('FINAL_REPORT_REWRITE_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    if FINAL_M6.get('hdo'):
        print('HDO_DISK_LOG path=%s bytes=%d sha256=%s last_seq=%d chain_ok=%s HDO_VIEW_TRUNCATION=UNKNOWN' % (
            FINAL_M6['hdo']['path'], FINAL_M6['hdo']['bytes'], FINAL_M6['hdo']['sha256'], FINAL_M6['hdo']['last_seq'], FINAL_M6['hdo']['chain']['ok']), flush=True)
    print('TEST866 ZIP %s | DRIVE %s' % (FINAL_M6.get('zip'), FINAL_M6.get('drive')), flush=True)
    print('TEST866 RESULT %s | status %s | labels %s | final_ok %s | GPU_EXECUTION_NOT_VERIFIED_BY_AUTHOR (cell author)' % (
        (STATE883['result'] or {}).get('result'), STATE883['status'], (STATE883['result'] or {}).get('labels'), fin_ok_), flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE883['suffix'], 'test870.py:suffix', 'exec'), globals())
