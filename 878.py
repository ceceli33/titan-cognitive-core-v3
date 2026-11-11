# AKBASCORE SILICON HIPPOCAMPUS — TEST878 — PERSISTENT NATIVE EXPERIENCE TRANSFER
# One A100-SXM4-80GB Colab cell. Frozen Qwen2.5-72B-Instruct NF4, BF16. Locked engine test870.py (e322ed8).
# QUESTION: does a physical Experience-CUT3 cartridge written from the REAL [X2][A][C] experience (same pre-action state,
# same executed ACQUIRE, real MISSING vs LIVE outcome cartridge), after the source working state is freed and the file is
# re-loaded from SSD, change the native CAR computation of an INDEPENDENT decision state in an outcome-specific and
# action-information-sensitive way?   write -> free -> reload -> native append -> native CAR.
# Source: exact replay (run_replay870) of World 01 and World 00, canonical H = [M_t2][X2][A] + C by the locked append.
# Cartridge: engine CUT3 format (h = layer-3 output rows, lower = L0-3 K/V rows) of [X2][A][C]; no X3/PRED/EVAL/CAR rows.
# Read: [target memory] + native_append_direct(E) + [target own X] -> decide874 / reading867. Nothing is executed.
# Arms: BASE, FULL-M/L, C-BLIND-M/L (read mask; C is the last segment), A-BLIND-M/L (A hidden from the C rows during the
# L4-79 re-computation and from the reader) against A-REF-M/L (same explicit masked kernel, A readable). The explicit
# layers are used only if, unmasked, they equal the locked append and the native read bitwise; otherwise the A arms are INVALID.
# Never: weight writes, training, hooks, output_hidden_states/attentions, logit edits, action forcing, activation patches.
import ast as _a878, hashlib as _h878, json as _j878, urllib.request as _u878
ENGINE_URL878 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB878, MARKER878 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', 'AKBASCORE SILICON HIPPOCAMPUS — TEST878'

def blob878(raw):
    return _h878.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()

def engine_parts878():
    with _u878.urlopen(_u878.Request(ENGINE_URL878, headers={'User-Agent': 'AKBASCORE-TEST878'}), timeout=240) as r:
        raw = r.read()
    assert blob878(raw) == ENGINE_BLOB878, ('ENGINE_BLOB_MISMATCH', blob878(raw))
    text = raw.decode('utf-8'); _a878.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST878_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST878_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST878_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('878_engine.log', '878_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST878_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '878_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '878_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST878_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old)
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL878, 'git_blob': blob878(raw), 'sha256': _h878.sha256(raw).hexdigest()}

try:
    ENGINE878, ENGINE_INFO878 = engine_parts878()
except BaseException as _exc878:      # console capture starts inside the engine prefix: keep a local record of this failure
    import time as _t878, traceback as _tb878
    _p878 = '/content/TEST878_PRE_ENGINE_ERROR_%s.txt' % _t878.strftime('%Y%m%dT%H%M%SZ', _t878.gmtime())
    try:
        with open(_p878, 'w', encoding='utf-8') as _f878: _f878.write(_tb878.format_exc())
    except OSError: _p878 = 'NOT_WRITTEN'
    print('TEST878 PRE-ENGINE ERROR (before console capture):', type(_exc878).__name__, _exc878, '| traceback:', _p878)
    raise
exec(compile(ENGINE878['prefix'], 'test870.py:prefix', 'exec'), globals())
exec(compile(ENGINE878['body'], 'test870.py:engine', 'exec'), globals())
print('TEST878 ENGINE', _j878.dumps(ENGINE_INFO878, sort_keys=True))

# ============================ pre-registration (fixed before the model is loaded) ============================
LOCKS864.update({'test870.py': ENGINE_BLOB878, 'Test870.log': 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc',
                 '873.py': '2e44affa5e0dd462155fb265c331270fb8e7b7e1', '873.log': '1c9eb9fca173003eaf45bc7726af13c2817324b7',
                 '874.py': '12172001ba3696ad91087a8b34d7995728259e47', '874.log': '1229e3b70440e3887ccf1bd7e3bad51f900f5313',
                 '877.py': 'a6aa7648e0fb765a8dc9b56b8f79b4dcef5fc772', '877.log': 'c4eb58021ed827fb13d5c15fee7c18541f6d4604'})
TEST877_CELL_BLOB878, TEST877_PREREG878 = 'd2f05c2930d3bb46408ce64c06e0e05059726a43', 'adaeb3bdf65ab16e'
TEST877_PREREG_DEPS878 = ('SIDES877', 'DISCOVERY877', 'CONFIRM877', 'ARM877', 'BLOCKS877', 'ROPE_TOL877', 'HARD_MIN877', 'PREREG877')
TEST870_MINUTES = TEST865_MINUTES = 110.0
WORLDS878 = ('01', '00')
SOURCES878 = tuple('I867_%s_%s' % (w, c) for w in WORLDS878 for c in ('MISSING', 'LIVE'))
FORKS878 = tuple('I867_%s_FORK' % w for w in WORLDS878)
SIDES874, _a874, _j874 = SOURCES878, _a878, _j878          # module names read by the selected 874.py functions
_h877, _j877, MOD877 = _h878, _j878, {}                    # module names read by the selected 877.py functions
ARM878, PRE_STEP878, POST_STEP878, FORK_STEP878, ACTION878 = 'V_X', 2, 3, 1, 'ACQUIRE'
FUNCS873 = ('kv873', 'length873', 'forward873', 'car873', 'resolve_append873', 'append_card873', 'decide873',
            'probs873', 'same873', 'tv873')
FUNCS874 = ('load873_874', 'ref873_874', 'keep874', 'forward874', 'car874', 'rows874', 'decide874', 'rel874')
FUNCS877 = ('api877', 'weights_digest877', 'xattn877', 'marg877', 'sub877', 'nrm877')
ROPE_TOL878, REPRO_TOL878, RECON_TOL878, SIG_MIN878 = 1e-2, 6e-4, 0.10, 5e-5
HARD_MIN878, FREE_MIN_GIB878 = 70.0, 8.0
PREREG878 = {
    'question': 'does a physical Experience-CUT3 cartridge of the real [X2,A,C] experience, re-loaded from SSD after the '
                'source working state is freed, change the native CAR computation of an independent decision state in an '
                'outcome-specific and action-information-sensitive way',
    'sources': SOURCES878, 'fork_targets': FORKS878, 'arm': ARM878, 'executed_action': ACTION878,
    'cartridge': 'engine CUT3 format {h, lower, n, p, body_tokens, book_id}: h = layer-3 output rows of [X2][A][C] '
                 '(X2/A: explicit lower forward, bitwise-gated against the native cache; C: the real outcome cartridge body), '
                 'lower = L0-L3 K/V of the same rows (K re-phased to cartridge positions P..), no X3/PRED/EVAL/CAR rows, '
                 'no text, no score, no action label; separate append-only directory; originals untouched',
    'persistence_gate': ['file SHA-256 + every tensor SHA-256 after reload from disk (source gH/h3/card tensors freed first)',
                         'reconstruction [M_t2]+E by native_append_direct: lower K/V rows bitwise equal to the sealed source '
                         'rows (K after the round trip, written-time round-trip rel <= %g)' % ROPE_TOL878,
                         'reconstruction + source X3: same native CAR action and max |dp| <= %g' % RECON_TOL878],
    'recon_tolerance_note': 'the 6e-4 tolerance of TEST873-877 holds for an identical call sequence. The cartridge re-computes '
                            'L4-79 of X2/A in CHUNK-sized calls; 874.log measured this class (NUMERICAL_ORDER_DETERMINISTIC): '
                            'layer-0 rel 0.0025, last-layer rel 0.027, CAR dp up to 0.0297. Bound fixed a priori; whether 6e-4 '
                            'holds is reported separately',
    'targets': {'SAME_GOAL': 'I867_<w>_FORK step 1 pre-action state (same qid, source outcome cards not mounted, state digest '
                             'different from the source t2/t3 states, its recorded CAR reproduced); no substitution',
                'CROSS_WORLD': 'the other world shared t2 pre-action state and its own X2'},
    'read': '[target memory] + native_append_direct(E) + [target own X] -> decide874 / reading867; nothing executed',
    'arms': {'BASE': 'target alone', 'FULL_M/L': 're-loaded real cartridges',
             'C_BLIND_M/L': 'C rows not readable by the target X and CAR continuations (C is the last segment of E: no other '
                            'row was computed from it); gate: C_BLIND_M == C_BLIND_L exactly and pre-C rows bitwise equal',
             'A_BLIND_M/L': 'A rows not readable by the C rows while L4-79 are re-computed, nor by the target X and CAR '
                            'continuations (C lower rows and C h come from the outcome cartridge forged without A). Uses the '
                            'explicit forward; valid only if that forward without a mask equals native_append_direct bitwise, '
                            'otherwise the arm is INVALID (not replaced)',
             'A_REF_M/L': 'path-matched reference of A_BLIND: the same explicit append and explicit read with the same built '
                          'masks in which the A columns are made readable again: A is fully visible, the attention kernel is '
                          'the masked one (masked and unmasked kernels differ numerically in BF16, 874.log). A_REF vs A_BLIND '
                          'is the A-information effect; FULL vs A_REF measures the kernel noise; FULL vs A_BLIND is reported '
                          'only. The explicit read without a mask must equal decide874 exactly, else the A arms are INVALID',
             'SELF_RECONSTRUCTION': 'persistence gate only'},
    'metrics': 'first-token and sequence logp of the 6 CAR words, 15 pairwise margins; action pairs = 5 pairs with %s' % ACTION878,
    'source_signature': 'c = P_A(m(H_M + X3_M) - m(H_L + X3_L)); |c_seq| <= %g -> SOURCE_ACTION_SIGNATURE_ABSENT' % SIG_MIN878,
    'floor': 'per source world: max(%g, max over M/L of |m(reconstruction) - m(source)|) for first and sequence margins' % SIG_MIN878,
    'panel_rule': 'T = m(FULL_M) - m(FULL_L). |T_seq| <= floor -> NO_TRANSFER; else A arms invalid -> TRANSFER_A_BLIND_INVALID; '
                  'A_REF interpretable only if |T_Aref|_seq > floor, <T_full,T_Aref>_seq > 0 and K = |T_full - T_Aref|_seq < '
                  '|T_full|_seq (all finite), else TRANSFER_A_BLIND_INVALID; |T_Aref - T_Ablind|_seq <= max(floor, K) -> '
                  'OUTCOME_TRANSFER_ONLY; else ACTION_INFORMATION_DEPENDENT_TRANSFER; non-finite margins -> TECHNICAL_BLOCK; '
                  'the masked A reference runs only after the unmasked explicit append is bitwise equal to the locked append '
                  '(else UNMASKED_APPEND_PARITY_FAIL)',
    'reported_not_gated': 'direction (cos, rho vs c), norms, action selectivity |T_A|^2/|T|^2, r_A, FULL vs A_BLIND, action and '
                          'probabilities per arm; source X3 and target X are different decision contexts: no vector reproduction '
                          'requirement',
    'verdict': 'same-goal panels of both worlds: equal -> that class, different -> ASYMMETRIC_TRANSFER, any missing -> '
               'NO_INDEPENDENT_TARGET, TRANSFER_A_BLIND_INVALID -> PARTIAL_INCONCLUSIVE. Cross-world class: both panels '
               'transfer (outcome detected) -> CROSS_WORLD_TRANSFER; both NO_TRANSFER -> GOAL_BOUND_TRANSFER; one each -> '
               'ASYMMETRIC_CROSS_WORLD; any missing / no independent target / technical -> CROSS_WORLD_UNRESOLVED. Scope = that '
               'class when the same-goal transfer holds in both worlds; GOAL_BOUND_TRANSFER is never a scope otherwise',
    'guards': 'before every load/append/read group: elapsed > %g min or available VRAM < %g GiB -> PARTIAL_INCONCLUSIVE' % (
        HARD_MIN878, FREE_MIN_GIB878),
    'limits': ['A-blind dependence is not credit assignment', 'no learning, no closed loop, no retrieval: forced mount',
               'two real event pairs: pilot']}
PREREG_SHA878 = sha256_bytes864(_j878.dumps(PREREG878, sort_keys=True).encode())
STATE878 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO878, 'prereg_sha256': PREREG_SHA878, 'source': {}, 'api': {},
            'ref873': {}, 'targets_static': {}, 'sides': {}, 'experience': {}, 'worlds': {}, 'blocks': [], 'verdict': None,
            'error': None}
STATE877 = STATE878                                        # api877 (877.py) writes STATE877['api']
T2_KEEP878, SRC878, TGT878, EXP878 = {}, {}, {}, {}

class Partial878(Exception):
    pass

class Persist878(Exception):
    pass

def line878(*parts): short864('T878', *parts)

def capture_source878():
    try:
        hist = [t for t in get_ipython().history_manager.input_hist_raw if MARKER878 in t and 'def probe878' in t]
        source, how = hist[-1], 'IPYTHON_CELL'
    except (NameError, IndexError):
        source = open(__file__, encoding='utf-8').read() if '__file__' in globals() else None; how = 'FILE_%RUN'
    assert source and MARKER878 in source, 'EXECUTED_878_SOURCE_NOT_CAPTURED'
    tree = _a878.parse(source)
    banned = {'register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook', 'output_hidden_states',
              'output_attentions', 'install_all_output_capturing_hooks', 'backward', 'requires_grad_', 'step', 'zero_grad',
              'execute866', 'mount865', 'free865', 'hop865', 'DirectCut3', 'native_append_direct'}
    for node in tree.body:
        if isinstance(node, _a878.FunctionDef) and node.name.endswith('878') and node.name != 'capture_source878':
            used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in _a878.walk(node) if isinstance(c, _a878.Call)}
            used |= {k.arg for k in _a878.walk(node) if isinstance(k, _a878.keyword)}
            used |= {s.slice.value for s in _a878.walk(node) if isinstance(s, _a878.Subscript) and
                     isinstance(s.slice, _a878.Constant)} & {'native_append_direct', 'DirectCut3'}
            allow = {'native_append_direct'} if node.name == 'append_exp878' else set()
            assert not (used & banned) - allow, ('FIREWALL878', node.name, sorted((used & banned) - allow))
    calls = [n for n in _a878.walk(tree) if isinstance(n, _a878.Call) and getattr(n.func, 'id', None) == 'reproduce_pre859859']
    assert len(calls) == 1, 'MODEL_LOADER_CALL_COUNT_NOT_ONE'
    rs = [n for n in tree.body if isinstance(n, _a878.Assign) and any(getattr(t, 'id', '') == 'xray_point870' for t in n.targets)]
    assert len(rs) == 1 and getattr(rs[0].value, 'id', None) == 'probe878', 'FIREWALL878_REBIND'
    (ROOT864 / 'TEST878.py').write_text(source, encoding='utf-8')
    STATE878['source'] = {'how': how, 'executed_cell_git_blob': git_blob864(source.encode()),
                          'executed_cell_sha256': sha256_bytes864(source.encode()), 'lines': source.count('\n') + 1,
                          'firewall': 'PASS'}

def source_audit878():
    # TEST877: the committed file is locked by git blob; the executed cell is a different object (blob in the log). The
    # committed file must reproduce the pre-registration hash printed by the GPU run, and the log must be that run.
    tree = _a878.parse(RAW_SOURCES864['877.py'].decode(), filename='877.py'); by = {}
    for n in tree.body:
        if isinstance(n, _a878.Assign):
            for t in n.targets:
                for x in _a878.walk(t):
                    if isinstance(x, _a878.Name): by.setdefault(x.id, n)
    nodes = sorted({id(by[k]): by[k] for k in TEST877_PREREG_DEPS878}.values(), key=lambda n: n.lineno)
    ns = {}; exec(compile(_a878.fix_missing_locations(_a878.Module(nodes, [])), '877.py:prereg', 'exec'), ns)
    pre877 = _h878.sha256(_j878.dumps(ns['PREREG877'], sort_keys=True).encode()).hexdigest()
    log = RAW_SOURCES864['877.log'].decode()
    assert pre877.startswith(TEST877_PREREG878) and ('T877 G0 PREREG ' + pre877) in log, ('TEST877_PREREG_MISMATCH', pre877[:16])
    for needle in ('NVIDIA A100-SXM4-80GB', 'cell %s | prereg %s' % (TEST877_CELL_BLOB878, TEST877_PREREG878), 'T877 G1 PREFLIGHT PASS',
                   '"G2_explicit_equals_native_LIVE": true', '"G2_explicit_equals_native_MISSING": true',
                   '"G6_masked_donor_equals_mask_LIVE": true', 'TEST877 VERDICT DISTRIBUTED_PATH', 'status COMPLETE'):
        assert needle in log, ('TEST877_LOG_NOT_THE_EXPECTED_GPU_RUN', needle)
    for name, needles in (('Test870.log', ('XR870 CALIBRATION CALIBRATION_PASS', 'NVIDIA A100')),
                          ('873.log', ('TEST873 OUTCOME', 'status COMPLETE', 'NVIDIA A100')),
                          ('874.log', ('NUMERICAL_ORDER_DETERMINISTIC', 'status COMPLETE', 'NVIDIA A100'))):
        assert all(x in RAW_SOURCES864[name].decode() for x in needles), ('LOCKED_LOG_NOT_A_GPU_RUN', name)
    STATE878['source']['test877'] = {'committed_file_git_blob': LOCKS864['877.py'], 'executed_cell_git_blob_in_log':
        TEST877_CELL_BLOB878, 'prereg_reproduced_from_file': pre877[:16],
        'identity': 'committed file reproduces the run pre-registration; executed-cell bytes are not published',
        'explicit_forward_bitwise_gate_in_log': True}

def load878():
    for name, funcs in (('874.py', FUNCS874), ('877.py', FUNCS877)):
        tree = _a878.parse(RAW_SOURCES864[name].decode(), filename=name)
        nodes = [n for n in tree.body if isinstance(n, _a878.FunctionDef) and n.name in funcs]
        assert {n.name for n in nodes} == set(funcs), ('SELECT', name)
        exec(compile(_a878.fix_missing_locations(_a878.Module(body=nodes, type_ignores=[])), name + ':selected', 'exec'), globals())
    load873_874()

def targets878(refs):
    # Independence of the target states is decided here from the locked 869 records only (no CAR result is read).
    out = {}
    ctl = lambda item: [e for e in refs[(item, ARM878)]['events'] if e['type'] == 'CONTROL']
    src = {}
    for w in WORLDS878:
        cards, shas, t2 = [], [], {}
        for cnd in ('MISSING', 'LIVE'):
            item = 'I867_%s_%s' % (w, cnd); cs = ctl(item)
            assert [x['record']['action'] for x in cs[:2]] == ['ADVANCE', ACTION878], ('T2_PATH', item)
            eff = [e for e in refs[(item, ARM878)]['events'] if e['type'] == 'EFFECT' and e.get('effect') == 'MOUNTED']
            assert eff and eff[0].get('action') == ACTION878, ('OUTCOME_EFFECT', item)
            cards.append(eff[0]['chosen']); shas += [cs[1]['record']['state_sha256'], cs[2]['record']['state_sha256']]
            t2[cnd] = cs[1]
        assert t2['MISSING']['record']['state_sha256'] == t2['LIVE']['record']['state_sha256'], ('T2_STATE_NOT_SHARED', w)
        assert cards[0] != cards[1], ('OUTCOME_CARDS_EQUAL', w)
        src[w] = {'cards': cards, 'shas': shas, 't2_mounted': list(t2['MISSING']['mounted']),
                  'world_index': refs[('I867_%s_MISSING' % w, ARM878)]['world_index']}
    for w in WORLDS878:
        o = [x for x in WORLDS878 if x != w][0]; item = 'I867_%s_FORK' % w; row = {}
        if (item, ARM878) in refs and ctl(item):
            f = ctl(item)[FORK_STEP878 - 1]; why = []
            if set(f['mounted']) & set(src[w]['cards']): why.append('SOURCE_OUTCOME_CARD_MOUNTED')
            if f['record']['state_sha256'] in src[w]['shas']: why.append('STATE_IS_A_SOURCE_STATE')
            if refs[(item, ARM878)]['world_index'] != src[w]['world_index']: why.append('OTHER_WORLD')
            row['SAME_GOAL'] = {'item': item, 'step': FORK_STEP878, 'mounted': list(f['mounted']), 'independent': not why, 'why': why}
        else:
            row['SAME_GOAL'] = {'item': item, 'independent': False, 'why': ['NO_RECORD']}
        why = ['SOURCE_OUTCOME_CARD_MOUNTED'] if set(src[o]['t2_mounted']) & set(src[w]['cards']) else []
        row['CROSS_WORLD'] = {'item': 'I867_%s_MISSING' % o, 'step': PRE_STEP878, 'mounted': src[o]['t2_mounted'],
                              'independent': not why, 'why': why}
        row['source_cards'] = src[w]['cards']; out[w] = row
    return out

def guard878(stage):
    el = (time.perf_counter() - T_START878) / 60.0
    free = (torch.cuda.mem_get_info()[0] + torch.cuda.memory_reserved() - torch.cuda.memory_allocated()) / 2**30
    if el > HARD_MIN878 or free < FREE_MIN_GIB878:
        raise Partial878('%s: elapsed %.1f min (limit %.0f), available VRAM %.2f GiB (min %.0f)' % (stage, el, HARD_MIN878, free, FREE_MIN_GIB878))

# ============================ explicit native layers (no hooks) ============================
def xspan878(env, cache, h, am, lo, hi, lower=(), restore=()):
    # Layers lo..hi-1 of the installed Qwen2 forward on rows h [1, L, H] stored at positions nc.. : the statement order of
    # xforward877 (TEST877: bitwise equal to the native model on the A100). am = 2-D key mask over [cache][h].
    # `lower`: cartridge K/V rows written to the layers below lo first (after the mask is built, as the model would see it).
    # `restore`: ranges hidden in am that are made readable again inside the built 4-D mask (causal rows only): the same
    # masked attention kernel as the blind arm with no information removed (path-matched reference).
    base = env['model'].model; cfg = base.config; L, nc = int(h.shape[1]), int(cache.get_seq_length())
    assert int(am.shape[1]) == nc + L, ('MASK_LENGTH', int(am.shape[1]), nc, L)
    pos = torch.arange(nc, nc + L, device=env['DEV']); pid = pos.unsqueeze(0)
    with torch.no_grad():
        mask = MOD877['mask'](config=cfg, inputs_embeds=h, attention_mask=am, past_key_values=cache, position_ids=pid)
        pe = base.rotary_emb(h, pid)
        for a, b in restore:
            assert mask is not None and mask.ndim == 4 and tuple(mask.shape[-2:]) == (L, nc + L) and a > 0, 'EXPLICIT_MASK_FORMAT'
            mask = mask.clone(); vis = mask[0, 0, L - 1, 0].clone()               # last row reads column 0: the "readable" value of this mask format
            for j in range(a, min(b, nc + L)): mask[:, :, max(j - nc, 0):, j] = vis
        for i, (k, v) in enumerate(lower): cache.update(k, v, i)
        for layer in base.layers[lo:hi]:
            res = h; a = xattn877(layer.self_attn, layer.input_layernorm(h), pe, mask, cache, pid, pos, None, None, None)
            h = res + a
            res = h; h = res + layer.mlp(layer.post_attention_layernorm(h))
    return h

def next_kv878(env, h3, pos0):
    # K/V that layer CUT+1 derives from h3 (Qwen2Attention statements): must equal the native cache rows bitwise
    base = env['model'].model; layer = base.layers[APPEND873['CUT'] + 1]; sa = layer.self_attn
    pid = torch.arange(pos0, pos0 + int(h3.shape[1]), device=env['DEV']).unsqueeze(0)
    with torch.no_grad():
        x = layer.input_layernorm(h3); shape = (*x.shape[:-1], -1, sa.head_dim)
        k = sa.k_proj(x).view(shape).transpose(1, 2); v = sa.v_proj(x).view(shape).transpose(1, 2)
        cos, sin = base.rotary_emb(h3, pid); _, k = MOD877['rope'](k, k, cos, sin)
    return k, v

# ============================ Experience-CUT3: write, reload, append ============================
def tsha878(env, cp):
    return {'h': env['kv_digest'](cp['h']), 'lower': [[env['kv_digest'](k), env['kv_digest'](v)] for k, v in cp['lower']]}

def write_exp878(env, eid, gH, h3, n2, x3s, pre_rows, prov):
    # Physical cartridge in the engine CUT3 format; body rows = [X2][A][C]. K is stored at cartridge positions P.. (the
    # locked append re-phases P+j -> target position). Nothing but native state tensors and provenance is written.
    P, cut, CH, dev, rephase = int(env['P']), APPEND873['CUT'], EXP878['CHUNK'], env['DEV'], APPEND873['rephase']
    path = EXP_DIR878 / (eid + '.pt'); tmp = EXP_DIR878 / (eid + '.pt.tmp')
    assert not path.exists(), ('EXPERIENCE_NAMESPACE_IS_APPEND_ONLY', str(path))
    q = x3s - n2; assert int(h3.shape[1]) == q and int(h3.shape[0]) == 1, ('EXPERIENCE_ROWS', tuple(h3.shape), q)
    lower, seal, rt = [], [], 0.0
    for i in range(cut + 1):
        k, v = gH[i][0][:, :, n2:x3s], gH[i][1][:, :, n2:x3s]; kc, kb = [], []
        for st in range(0, q, CH):
            e = min(q, st + CH); s_pos = torch.arange(n2 + st, n2 + e, device=dev); c_pos = torch.arange(P + st, P + e, device=dev)
            kc.append(rephase(k[:, :, st:e], s_pos, c_pos)); kb.append(rephase(kc[-1], c_pos, s_pos))
        kc, kb = torch.cat(kc, dim=-2), torch.cat(kb, dim=-2)
        rt = max(rt, float(torch.linalg.vector_norm(kb.float() - k.float())) / max(float(torch.linalg.vector_norm(k.float())), 1e-30))
        z = torch.zeros((int(k.shape[0]), int(k.shape[1]), P, int(k.shape[3])), dtype=k.dtype, device=dev)
        lower.append((torch.cat([z, kc], dim=-2).cpu().contiguous(), torch.cat([z, v], dim=-2).cpu().contiguous()))
        seal.append([env['kv_digest'](kb), env['kv_digest'](v)])
    h = torch.cat([torch.zeros((1, P, int(h3.shape[2])), dtype=h3.dtype, device=dev), h3], dim=1).cpu().contiguous()
    cp = {'h': h, 'lower': tuple(lower), 'n': P + q, 'p': P, 'body_tokens': q, 'book_id': eid}
    torch.save(cp, tmp); tmp.replace(path)
    pre = _h878.sha256(_j878.dumps([env['kv_digest'](h[:, P:P + pre_rows])] + [[env['kv_digest'](k[:, :, P:P + pre_rows]),
          env['kv_digest'](v[:, :, P:P + pre_rows])] for k, v in lower]).encode()).hexdigest()
    entry = {'id': eid, 'file': str(path), 'sha256': sha256_file864(path), 'bytes': path.stat().st_size, 'tensor_sha': tsha878(env, cp),
             'body_tokens': q, 'p': P, 'recon_lower_seal': seal, 'roundtrip_K_rel': rt, 'pre_C_seal': pre, 'provenance': prov}
    del cp, h, lower
    return entry

def load_exp878(env, entry):
    # the checks of the locked safe_load (file SHA, id/p/n, every tensor SHA) on the experience namespace, then locked to_gpu
    path = type(ROOT864)(entry['file'])
    if not (path.exists() and sha256_file864(path) == entry['sha256']): raise Persist878('FILE_SHA ' + entry['id'])
    cp = torch.load(path, map_location='cpu', weights_only=True)
    if not (cp['book_id'] == entry['id'] and int(cp['p']) == int(env['P']) and int(cp['n']) == int(env['P']) + int(cp['body_tokens'])
            and int(cp['body_tokens']) == int(entry['body_tokens'])): raise Persist878('CARTRIDGE_ID ' + entry['id'])
    if tsha878(env, cp) != entry['tensor_sha']: raise Persist878('TENSOR_SHA ' + entry['id'])
    g = env['to_gpu'](cp); del cp
    return g

def append_exp878(env, mem, cp):
    # the locked native append: prior rows sealed, lower rows re-phased, L4-79 re-computed by the model
    n0 = length873(env, mem)
    grown = env['native_append_direct'](list(mem), cp, strict_sha=True)
    assert length873(env, grown) == n0 + int(cp['body_tokens']), ('EXPERIENCE_APPEND_LENGTH', n0, length873(env, grown))
    return grown

def xappend878(env, mem, cp, blind, sham=False):
    # The same append with the explicit layers (CHUNK, positions, re-phase and all-ones mask as native_append_direct),
    # plus `blind`: absolute row ranges no later row may read while L4-79 are re-computed. blind=() must equal the
    # locked append bitwise (checked on every cartridge) before any masked use. sham=True: the blind mask is built and the
    # range is made readable again (reference with the masked kernel path and all information present).
    P, cut, CH, dev, rephase = int(env['P']), APPEND873['CUT'], EXP878['CHUNK'], env['DEV'], APPEND873['rephase']
    n0 = length873(env, mem); q = int(cp['n']) - P; body = cp['h'][:, P:, :]
    cache = env['cache_build'](list(mem))
    for st in range(0, q, CH):
        m = min(CH, q - st); nc = n0 + st
        am = torch.ones((1, nc + m), device=dev, dtype=torch.long)
        for a, b in blind: am[0, a:min(b, nc + m)] = 0
        old, new = torch.arange(P + st, P + st + m, device=dev), torch.arange(nc, nc + m, device=dev)
        lower = [(rephase(k[:, :, P + st:P + st + m, :], old, new), v[:, :, P + st:P + st + m, :]) for k, v in cp['lower']]
        hit = [(a, b) for a, b in blind if a < nc + m]
        xspan878(env, cache, body[:, st:st + m, :], am, cut + 1, int(env['NL']), lower, hit if sham else ())
    grown = kv873(env, cache); del cache
    assert length873(env, grown) == n0 + q, ('EXPLICIT_APPEND_LENGTH', n0, q)
    return grown

def xcar878(env, kv, X, blind, sham):
    # car874 procedure (first token + teacher-forced continuations, each cropped) with the explicit layers, so that the
    # blind arm and its reference run the same masked attention kernel in the read as well. blind=() must equal decide874.
    model = env['model']; cache = env['cache_build'](list(kv)); n0 = int(cache.get_seq_length()); env['budget849']()
    n1 = n0 + int(X.shape[0])
    assert n1 + max(len(ids) for _, ids in ACTION_IDS867) <= int(env['MAX_FUSED_TOKENS']), ('CONTEXT_LIMIT', n1)
    def fwd(Y, last):
        L, nc = int(Y.shape[0]), int(cache.get_seq_length())
        am = torch.ones((1, nc + L), device=env['DEV'], dtype=torch.long)
        for a, b in blind: am[0, a:b] = 0
        h = xspan878(env, cache, Y.reshape(1, L, int(env['H'])), am, 0, int(env['NL']), (), blind if sham else ())
        with torch.no_grad():
            return torch.log_softmax(model.lm_head(model.model.norm(h))[0, -last:].float(), dim=-1)   # all rows, as the model
    first = fwd(X, 1)[0]; scores = []
    for word, ids in ACTION_IDS867:
        token_logps = [float(first[ids[0]])]
        if len(ids) > 1:
            m = len(ids) - 1; lp = fwd(env['embed841'](ids[:-1]), m); cache.crop(-m)
            assert int(cache.get_seq_length()) == n1, 'CAR_CROP_LENGTH_MISMATCH_878'
            token_logps += [float(lp[i, ids[i + 1]]) for i in range(m)]; del lp
        scores.append({'word': word, 'ids': ids, 'token_logps': token_logps, 'sequence_logp': float(sum(token_logps)),
                       'hard_greedy_ids': []})
    top = torch.topk(first, 10); del cache
    return reading867({'scores': scores, 'path': 'CROP', 'fallback_reason': None,
                       'first_top10': {'ids': [int(i) for i in top.indices.tolist()]}, 'X_sha256': None})

# ============================ measures ============================
def arm878(r): return {'action': r['action'], 'p': probs873(r)}

def jsafe878(x):
    # JSON view: a non-finite number is written as the string 'NaN'/'inf' (visible, never silently dropped)
    return json.loads(json.dumps(x, default=str), parse_constant=str)
def dif878(ma, mb): return {k: sub877(ma[k], mb[k]) for k in ('first', 'seq')}

def pa878(action):
    W = [w for w, _ in ACTION_IDS867]; pairs = [(a, b) for i, a in enumerate(W) for b in W[i + 1:]]
    idx = [i for i, p in enumerate(pairs) if action in p]; assert len(idx) == len(W) - 1, ('ACTION_PAIRS', action)
    return idx

def sig878(t, c, idx):
    # direction / norm / action selectivity of a target contrast t against the source contrast c (reported, not gated)
    out = {}
    for k in ('first', 'seq'):
        ta, ca = [t[k][i] for i in idx], [c[k][i] for i in idx]; dot = sum(x * y for x, y in zip(ta, ca))
        na, nc, nall = nrm877(ta), nrm877(ca), nrm877(t[k])
        out[k] = {'norm_all15': nall, 'norm_action5': na, 'norm_other10': max(nall * nall - na * na, 0.0) ** 0.5,
                  'action_selectivity': (na * na) / (nall * nall + 1e-30), 'cos_A': dot / (na * nc + 1e-30),
                  'rho_A': dot / (nc * nc + 1e-30), 'r_A': nrm877(sub877(ca, ta)) / (nc + 1e-30),
                  'cos_all15': sum(x * y for x, y in zip(t[k], c[k])) / (nall * nrm877(c[k]) + 1e-30)}
    return out

# ============================ phase 2: persistence gate and transfer panels ============================
def persist878(env, S):
    guard878('persist_' + S['side']); cut = APPEND873['CUT']; n2 = S['n2']
    cp = load_exp878(env, S['entry'])
    g = append_exp878(env, S['m2'], cp)
    seal_ok = all([env['kv_digest'](g[i][0][:, :, n2:]), env['kv_digest'](g[i][1][:, :, n2:])] == S['entry']['recon_lower_seal'][i]
                  for i in range(cut + 1))
    r, _, _, _ = decide874(env, g, S['X3'].to(env['DEV']), [])
    pr, ps = probs873(r), S['H']['p']; dp = max(abs(pr[w] - ps[w]) for w in ps); mr = marg877(r)
    guard878('persist_unmasked_' + S['side'])
    gx = xappend878(env, S['m2'], cp, ())
    same = all(torch.equal(a[j], b[j]) for a, b in zip(g, gx) for j in (0, 1)); del gx
    a0 = n2 + S['L2']; sham = {'valid': False, 'why': 'UNMASKED_APPEND_PARITY_FAIL'}
    if same:                                           # the masked reference runs only on a bitwise-verified explicit path
        guard878('persist_masked_' + S['side']); sham['why'] = None
        try:                                           # recorded, not hidden: an unusable mask format invalidates the A arms only
            gs = xappend878(env, S['m2'], cp, [(a0, a0 + S['la'])], True)
            sham = {'valid': True, 'why': None, 'upper_K_rel_vs_native_append': max(rel874(
                [tuple(t[:, :, n2:] for t in kv) for kv in g[cut + 1:]], [tuple(t[:, :, n2:] for t in kv) for kv in gs[cut + 1:]]))}
            del gs
        except AssertionError as exc: sham['why'] = str(exc)
    del g, cp
    S['recon'] = {'reloaded_sha_ok': True, 'lower_rows_bitwise': seal_ok, 'roundtrip_K_rel': S['entry']['roundtrip_K_rel'],
                  'action_same': r['action'] == S['H']['action'], 'max_dp': dp, 'within_6e-4': dp <= REPRO_TOL878,
                  'noise': {k: nrm877(sub877(mr[k], S['m'][k])) for k in ('first', 'seq')}, 'arm': arm878(r),
                  'explicit_append_equals_native_bitwise': same, 'A_reference_mask': sham}
    S['recon']['pass'] = bool(seal_ok and S['recon']['action_same'] and dp <= RECON_TOL878 and
                              S['entry']['roundtrip_K_rel'] <= ROPE_TOL878)
    return S['recon']

def panel878(env, M, L, T, idx, c, floor, a_valid):
    n0 = length873(env, T['m']); L2, la, q = M['L2'], M['la'], int(M['entry']['body_tokens'])
    a0, a1, c1 = n0 + L2, n0 + L2 + la, n0 + q
    out = {'target': {k: T[k] for k in ('item', 'step', 'qid', 'mounted', 'X_len')}, 'spans': {'E': [n0, c1], 'A': [a0, a1], 'C': [a1, c1]},
           'reads': 0, 'gates': {}, 'arms': {}}
    seal0 = prefix_seals865(env, T['m']); guard878('panel_base_' + T['item'])
    rd = {'BASE': decide874(env, T['m'], T['X'], [])[0]}; pre = {}
    if a_valid:                                          # the explicit read without a mask must be the native read
        rd['BASE_EXPLICIT'] = xcar878(env, T['m'], T['X'], (), False); a_valid = same873(rd['BASE'], rd['BASE_EXPLICIT'])
    for S in (M, L):
        cnd = S['cond'][0]; guard878('panel_%s_%s' % (T['item'], S['side']))
        cp = load_exp878(env, S['entry']); g = append_exp878(env, T['m'], cp)
        pre[cnd] = [[env['kv_digest'](k[:, :, n0:a1]), env['kv_digest'](v[:, :, n0:a1])] for k, v in g]
        rd['FULL_' + cnd] = decide874(env, g, T['X'], [])[0]
        rd['C_BLIND_' + cnd] = decide874(env, g, T['X'], [(a1, c1)])[0]; del g
        if a_valid:
            guard878('panel_A_%s_%s' % (T['item'], S['side']))
            g = xappend878(env, T['m'], cp, [(a0, a1)]); rd['A_BLIND_' + cnd] = xcar878(env, g, T['X'], [(a0, a1)], False); del g
            g = xappend878(env, T['m'], cp, [(a0, a1)], True); rd['A_REF_' + cnd] = xcar878(env, g, T['X'], [(a0, a1)], True); del g
        del cp
    out['reads'] = len(rd); out['arms'] = {k: arm878(r) for k, r in rd.items()}; m = {k: marg877(r) for k, r in rd.items()}
    out['gates'] = {'pre_C_rows_bitwise_M_eq_L': pre['M'] == pre['L'], 'C_BLIND_M_equals_L': same873(rd['C_BLIND_M'], rd['C_BLIND_L']),
                    'target_memory_unchanged': prefix_seals865(env, T['m']) == seal0,
                    'finite_margins': all(math.isfinite(x) for v_ in m.values() for k in ('first', 'seq') for x in v_[k])}
    out['A_BLIND'] = 'VALID' if a_valid else 'INVALID_EXPLICIT_PATH_NOT_BITWISE_OR_MASK_FORMAT'
    Tf = dif878(m['FULL_M'], m['FULL_L']); out['contrast'] = {'FULL': Tf, 'C_BLIND': dif878(m['C_BLIND_M'], m['C_BLIND_L'])}
    out['signature'] = {'FULL': sig878(Tf, c, idx)}
    out['vs_base'] = {k: {q_: nrm877(sub877(m[k][q_], m['BASE'][q_])) for q_ in ('first', 'seq')} for k in m if k != 'BASE'}
    out['max_dp_FULL_M_vs_L'] = max(abs(out['arms']['FULL_M']['p'][w] - out['arms']['FULL_L']['p'][w]) for w in out['arms']['BASE']['p'])
    out['detect'] = {'outcome_seq': nrm877(Tf['seq']) > floor['seq'], 'outcome_first': nrm877(Tf['first']) > floor['first']}
    if a_valid:
        Ta, Tr = dif878(m['A_BLIND_M'], m['A_BLIND_L']), dif878(m['A_REF_M'], m['A_REF_L']); D, Dt = dif878(Tr, Ta), dif878(Tf, Ta)
        nf, nr, K = nrm877(Tf['seq']), nrm877(Tr['seq']), nrm877(sub877(Tf['seq'], Tr['seq']))
        dot = sum(x * y for x, y in zip(Tf['seq'], Tr['seq'])); nd = nrm877(D['seq']); thr = max(floor['seq'], K)
        fin = all(math.isfinite(x) for x in (nf, nr, K, dot, nd, thr))
        out['A_ref'] = {'norm_T_full_seq': nf, 'norm_T_ref_seq': nr, 'K_full_minus_ref_seq': K, 'dot_full_ref_seq': dot,
                        'norm_ref_minus_blind_seq': nd, 'threshold_max_floor_K': thr, 'finite': fin,
                        'ref_detectable': fin and nr > floor['seq'], 'ref_same_direction': fin and dot > 0.0, 'ref_close': fin and K < nf}
        out['A_ref']['interpretable'] = out['A_ref']['ref_detectable'] and out['A_ref']['ref_same_direction'] and out['A_ref']['ref_close']
        out['contrast'].update({'A_BLIND': Ta, 'A_REF': Tr})
        out['signature'].update({'A_BLIND': sig878(Ta, c, idx), 'A_REF': sig878(Tr, c, idx)})
        out['A_dependence'] = {'path_matched_A_REF_minus_A_BLIND': {'norm_seq': nrm877(D['seq']), 'norm_first': nrm877(D['first']),
                                   'norm_action5_seq': nrm877([D['seq'][i] for i in idx]),
                                   'ratio_to_A_REF_seq': nrm877(D['seq']) / (nrm877(Tr['seq']) + 1e-30),
                                   'r_A_blind_minus_ref_seq': out['signature']['A_BLIND']['seq']['r_A'] - out['signature']['A_REF']['seq']['r_A']},
                               'FULL_minus_A_BLIND_not_path_matched': {'norm_seq': nrm877(Dt['seq']), 'norm_first': nrm877(Dt['first'])},
                               'mask_kernel_noise_FULL_vs_A_REF': {k: max(nrm877(sub877(m['FULL_' + x][k], m['A_REF_' + x][k])) for x in 'ML')
                                                                   for k in ('first', 'seq')}}
        out['detect']['A_dependence_seq'] = fin and nd > thr
    if not all(out['gates'].values()): out['status'] = 'TECHNICAL_BLOCK'
    elif not out['detect']['outcome_seq']: out['status'] = 'NO_TRANSFER'
    elif not a_valid: out['status'] = 'TRANSFER_A_BLIND_INVALID'; out['A_invalid_why'] = 'EXPLICIT_PATH_OR_MASK'
    elif not out['A_ref']['interpretable']: out['status'] = 'TRANSFER_A_BLIND_INVALID'; out['A_invalid_why'] = 'A_REF_NOT_INTERPRETABLE'
    elif not out['detect']['A_dependence_seq']: out['status'] = 'OUTCOME_TRANSFER_ONLY'
    else: out['status'] = 'ACTION_INFORMATION_DEPENDENT_TRANSFER'
    return out

def world878(env, w):
    o = [x for x in WORLDS878 if x != w][0]; t0 = time.perf_counter()
    W = STATE878['worlds'].setdefault(w, {}); W.update({'status': 'RUNNING', 'panels': {}, 'reads': 0})
    try:
        M, L = SRC878.get('I867_%s_MISSING' % w), SRC878.get('I867_%s_LIVE' % w)
        if M is None or L is None: W['status'] = 'TECHNICAL_BLOCK'; W['why'] = 'SOURCE_EXPERIENCE_NOT_CAPTURED'; return
        W['gates'] = g = {'same_t2_spans': (M['n2'], M['L2'], M['la']) == (L['n2'], L['L2'], L['la']),
                          'same_action_tokens': M['A_ids'] == L['A_ids'] and M['t2_action'] == L['t2_action'] == ACTION878,
                          'real_cards_differ': M['card'] != L['card'], 'same_C_length': M['body'] == L['body'],
                          'pre_C_cartridge_rows_bitwise': M['entry']['pre_C_seal'] == L['entry']['pre_C_seal'],
                          'same_goal': M['qid'] == L['qid']}
        if not all(g.values()): W['status'] = 'TECHNICAL_BLOCK'; W['why'] = 'SOURCE_PAIR_GATES'; return
        idx = pa878(ACTION878); c = dif878(M['m'], L['m']); ca = {k: [c[k][i] for i in idx] for k in c}
        W['source'] = {'cards': {'MISSING': M['card'], 'LIVE': L['card']}, 'H': {'MISSING': M['H'], 'LIVE': L['H']},
                       'contrast': c, 'norm_all15': {k: nrm877(c[k]) for k in c}, 'norm_action5': {k: nrm877(ca[k]) for k in ca},
                       'action_selectivity_seq': nrm877(ca['seq']) ** 2 / (nrm877(c['seq']) ** 2 + 1e-30), 'action_pairs': idx}
        if nrm877(ca['seq']) <= SIG_MIN878: W['status'] = 'SOURCE_ACTION_SIGNATURE_ABSENT'; return
        W['persistence'] = {S['cond']: persist878(env, S) for S in (M, L)}; W['reads'] += 2
        if not all(r['pass'] for r in W['persistence'].values()): W['status'] = 'PERSISTENCE_FAIL'; return
        a_valid = all(r['explicit_append_equals_native_bitwise'] and r['A_reference_mask']['valid'] for r in W['persistence'].values())
        W['floor'] = floor = {k: max(SIG_MIN878, max(r['noise'][k] for r in W['persistence'].values())) for k in ('first', 'seq')}
        for kind, key in (('SAME_GOAL', ('FORK', w)), ('CROSS_WORLD', ('T2', o))):
            st = STATE878['targets_static'][w][kind]; T = TGT878.get(key); why = list(st['why'])
            if T is None: why.append('TARGET_STATE_NOT_CAPTURED_OR_RECORD_NOT_REPRODUCED')
            elif (kind == 'SAME_GOAL') != (T['qid'] == M['qid']): why.append('GOAL_RELATION')
            elif set(T['mounted']) & {M['card'], L['card']}: why.append('SOURCE_OUTCOME_CARD_MOUNTED')
            if why: W['panels'][kind] = {'status': 'NO_INDEPENDENT_TARGET', 'why': why}; continue
            W['panels'][kind] = panel878(env, M, L, T, idx, c, floor, a_valid); W['reads'] += W['panels'][kind]['reads']
        W['status'] = 'PANELS_DONE'
    except Persist878 as exc:
        W['status'] = 'PERSISTENCE_FAIL'; W['why'] = str(exc); line878('PERSISTENCE_FAIL', w, str(exc))
    except Partial878 as exc:
        W['status'] = 'PARTIAL_INCONCLUSIVE'; W['why'] = str(exc); line878('PARTIAL', w, str(exc))
    finally:
        W['elapsed_s'] = round(time.perf_counter() - t0, 1); W['peak_gib'] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
        json_write864('878_checkpoint_%s.json' % w, jsafe878(W))
        line878('WORLD', w, W['status'], {k: p.get('status') for k, p in W['panels'].items()}, 'reads=%d' % W['reads'],
                'elapsed_s=%s' % W['elapsed_s'], 'peak_gib=%s' % W['peak_gib'])

# ============================ replay tap: real source experience and real target states ============================
def probe878(env, ctx, record, state, label):
    side = ctx['spec']['item']; world, cond = side.split('_')[1], side.split('_')[2]; qid = ctx['spec']['qid']
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=env['QTEXT841'][qid]))); post = env['REVIEW_SUFFIX851']
    out = STATE878['sides'].setdefault(side, {'checks': {}, 'error': None}); c = out['checks']
    try:
        ids = dict(ACTION_IDS867); dev = env['DEV']; cut = APPEND873['CUT']; Hd = int(env['H'])
        if cond == 'FORK':                                   # target only: its own memory and its own X, nothing appended
            X, _ = env['make_x851'](pre, list(state['segments']), post)
            m = [tuple(t.clone() for t in kv) for kv in ctx['memx']]
            cache = env['cache_build'](list(m)); c['t1_CAR_equals_record'] = same873(car873(env, cache, X), record['reading']); del cache
            out.update({'role': 'SAME_GOAL_TARGET', 'mounted': list(ctx['M']), 'qid': qid, 'memory_tokens': length873(env, m)})
            if c['t1_CAR_equals_record']:
                TGT878[('FORK', world)] = {'m': m, 'X': X, 'qid': qid, 'mounted': list(ctx['M']), 'item': side,
                                           'step': ctx['steps'], 'X_len': int(X.shape[0])}
            line878('TARGET', side, _j878.dumps({k: out[k] for k in ('mounted', 'memory_tokens')}), 'record_reproduced=%s' % c['t1_CAR_equals_record'])
            return
        if ctx['steps'] == PRE_STEP878:
            segs2 = list(state['segments']); X2, _ = env['make_x851'](pre, segs2, post); L2 = int(X2.shape[0])
            m2 = [tuple(t.clone() for t in kv) for kv in ctx['memx']]; n2 = length873(env, m2)
            cache = env['cache_build'](list(m2)); c['t2_CAR_equals_record'] = same873(car873(env, cache, X2), record['reading'])
            c['t2_crops'] = int(cache.get_seq_length()) == n2 + L2
            own = env['cache_build'](list(kv873(env, cache))); del cache
            A = ids[record['action']]; la = len(A); EA = env['embed841'](A)
            forward873(env, own, EA, n2 + L2); keep_own = kv873(env, own); del own
            c['commit_length'] = length873(env, keep_own) == n2 + L2 + la
            # h3 of the [X2][A] rows: explicit L0-3 with the same two calls as the native timeline; gated bitwise below
            cl = env['cache_build'](list(m2)); one = lambda n: torch.ones((1, n), device=dev, dtype=torch.long)
            hx = xspan878(env, cl, X2.reshape(1, L2, Hd), one(n2 + L2), 0, cut + 1)
            ha = xspan878(env, cl, EA.reshape(1, la, Hd), one(n2 + L2 + la), 0, cut + 1)
            c['explicit_lower_KV_bitwise'] = all(torch.equal(x, y) for i in range(cut + 1)
                                                 for x, y in zip(cache_kv870(cl, i), keep_own[i]))
            nk = [next_kv878(env, hx, n2), next_kv878(env, ha, n2 + L2)]; ref = keep_own[cut + 1]
            c['h3_next_layer_KV_bitwise'] = all(torch.equal(nk[j][t], ref[t][:, :, a:b]) for j, (a, b) in
                                                enumerate(((n2, n2 + L2), (n2 + L2, n2 + L2 + la))) for t in (0, 1))
            del cl, nk
            assert all(c.values()), ('T2_GATES', c)
            T2_KEEP878[side] = {'own': keep_own, 'A_ids': A, 't2_action': record['action'], 'h3': torch.cat([hx, ha], dim=1),
                                'm2': m2, 'X2': X2, 'L2': L2, 'la': la, 'n2': n2, 'mounted': list(ctx['M'])}
            if cond == 'MISSING':
                TGT878[('T2', world)] = {'m': m2, 'X': X2, 'qid': qid, 'mounted': list(ctx['M']), 'item': side,
                                         'step': ctx['steps'], 'X_len': L2}
            return
        z = T2_KEEP878.pop(side)
        memx = ctx['memx']; eff = [e for e in ctx['events'] if e.get('type') == 'EFFECT'][-1]; card = eff.get('chosen')
        body = int(env['entries'][card]['body_tokens']); n3 = int(memx[0][0].shape[-2]); P = int(env['P'])
        c['card_mounted'] = eff.get('effect') == 'MOUNTED' and list(ctx['M'])[-1] == card
        names = slot_names869(env, list(state['segments']))
        X3, _ = env['make_x851'](pre, [s for s, n in zip(state['segments'], names) if n not in ('FV', 'FK')], post)
        seal0 = prefix_seals865(env, memx); hook0 = assert_hook_free859(env, 'T878_before_' + side)
        gH, n_before = append_card873(env, z['own'], card); del z['own']
        x3s = n_before + body; n2, L2, la = z['n2'], z['L2'], z['la']
        c['timeline'] = n_before == n2 + L2 + la
        rephase = APPEND873['rephase']
        c['lower_V_bitwise'] = all(torch.equal(gH[i][1][:, :, n_before:], memx[i][1][:, :, n3 - body:]) for i in range(cut + 1))
        rope = max(float(torch.linalg.vector_norm(rephase(gH[i][0][:, :, n_before:], torch.arange(n_before, x3s, device=dev),
            torch.arange(n3 - body, n3, device=dev)).float() - memx[i][0][:, :, n3 - body:].float())) /
            max(float(torch.linalg.vector_norm(memx[i][0][:, :, n3 - body:].float())), 1e-30) for i in range(cut + 1))
        c['lower_K_rephase'] = rope <= ROPE_TOL878; out['lower_K_rephase_rel'] = rope
        rH, _, _, _ = decide874(env, gH, X3, [])
        ref = STATE878['ref873'][side]['T1']
        c['H_reproduces_873'] = rH['action'] == ref['action'] and all(abs(probs873(rH)[w] - ref['p'][w]) <= REPRO_TOL878 for w in ref['p'])
        cpc, _ = APPEND873['load'](card)                     # the real outcome cartridge (locked, SHA-verified): its h rows
        c['card_rows'] = int(cpc['n']) - P == body and cpc['book_id'] == card
        h3 = torch.cat([z['h3'], cpc['h'][:, P:, :].to(dev)], dim=1); del cpc
        eid = 'X878_%s_%s' % (world, cond)
        prov = {'world': world, 'item': side, 'arm': ARM878, 'step_pre': PRE_STEP878, 'step_post': POST_STEP878, 'qid': qid,
                'goal_text_sha256': sha256_bytes864(env['QTEXT841'][qid].encode()), 'pre_action_state_sha256': STATIC_T2_SHA878[side],
                'action': z['t2_action'], 'action_token_ids': list(z['A_ids']), 'outcome_cartridge': card,
                'outcome_cartridge_file_sha256': env['entries'][card].get('sha256'), 'mounted_before': z['mounted'],
                'spans_body': {'X2': [0, L2], 'A': [L2, L2 + la], 'C': [L2 + la, L2 + la + body]},
                'source_storage_positions': [n2, x3s], 'cartridge_positions': [P, P + x3s - n2],
                'source_prefix_seal': seal0, 'engine_git_blob': ENGINE_BLOB878, 'cell_git_blob': STATE878['source'].get('executed_cell_git_blob'),
                'weights_digest': WEIGHTS0_878, 'contains': 'native h3 + L0-3 K/V of [X2][A][C] only'}
        entry = write_exp878(env, eid, gH, h3, n2, x3s, L2 + la, prov)
        c['roundtrip_K'] = entry['roundtrip_K_rel'] <= ROPE_TOL878
        c['memory_seal'] = prefix_seals865(env, memx) == seal0
        hook1 = assert_hook_free859(env, 'T878_after_' + side)
        c['hook_free'] = not any(x['hook_count'] or x['transformers_output_capturing_installed'] for x in (hook0, hook1))
        out.update({'role': 'SOURCE', 'card': card, 'H': arm878(rH), 'C': [n_before, x3s], 'E': [n2, x3s], 'X3_len': int(X3.shape[0]),
                    'experience': eid, 'experience_bytes': entry['bytes'], 'roundtrip_K_rel': entry['roundtrip_K_rel']})
        assert all(c.values()), ('SIDE_GATES', c)
        STATE878['experience'][eid] = entry
        SRC878[side] = {'side': side, 'world': world, 'cond': cond, 'm2': z['m2'], 'X3': X3.detach().cpu(), 'H': arm878(rH),
                        'm': marg877(rH), 'entry': entry, 'n2': n2, 'L2': L2, 'la': la, 'body': body, 'qid': qid, 'card': card,
                        'A_ids': list(z['A_ids']), 't2_action': z['t2_action']}
        del gH, h3, z, X3, rH; gc.collect(); torch.cuda.empty_cache()   # source working state is gone: only the SSD file remains
        line878('SOURCE', side, _j878.dumps({k: out[k] for k in ('card', 'E', 'C', 'X3_len', 'H', 'experience', 'experience_bytes')}, sort_keys=True))
    except Exception as exc:
        out['error'] = '%s: %s' % (type(exc).__name__, str(exc)[:400]); out['traceback'] = traceback.format_exc()
        (ROOT864 / ('878_%s_t%d_traceback.txt' % (side, ctx['steps']))).write_text(out['traceback'], encoding='utf-8')
        line878('POINT_ERROR', side, 't=%d' % ctx['steps'], out['error'])

xray_point870 = probe878

def verdict878():
    blocks = list(STATE878['blocks']); reps = {r.get('item'): r for r in STATE870['replays']}
    for side, s in STATE878['sides'].items():
        if s.get('error'): blocks.append('POINT_ERROR:' + side)
        if reps.get(side, {}).get('ok') is not True: blocks.append('REPLAY_NOT_EXACT:' + side)
    Ws = [STATE878['worlds'].get(w, {}) for w in WORLDS878]; st = [W.get('status') for W in Ws]
    sg = [W.get('panels', {}).get('SAME_GOAL', {}).get('status') for W in Ws]
    cw = [W.get('panels', {}).get('CROSS_WORLD', {}).get('status') for W in Ws]
    moved = ('OUTCOME_TRANSFER_ONLY', 'ACTION_INFORMATION_DEPENDENT_TRANSFER', 'TRANSFER_A_BLIND_INVALID')
    scope = None
    if blocks or 'TECHNICAL_BLOCK' in st or 'TECHNICAL_BLOCK' in sg + cw or None in st: v = 'TECHNICAL_BLOCK'
    elif 'PARTIAL_INCONCLUSIVE' in st: v = 'PARTIAL_INCONCLUSIVE'
    elif 'PERSISTENCE_FAIL' in st: v = 'PERSISTENCE_FAIL'
    elif 'SOURCE_ACTION_SIGNATURE_ABSENT' in st: v = 'SOURCE_ACTION_SIGNATURE_ABSENT'
    elif 'NO_INDEPENDENT_TARGET' in sg or None in sg: v = 'NO_INDEPENDENT_TARGET'
    elif 'TRANSFER_A_BLIND_INVALID' in sg: v = 'PARTIAL_INCONCLUSIVE'
    elif sg[0] != sg[1]: v = 'ASYMMETRIC_TRANSFER'
    else: v = sg[0]
    if all(x in moved for x in cw): cwc = 'CROSS_WORLD_TRANSFER'
    elif all(x in moved + ('NO_TRANSFER',) for x in cw):
        cwc = 'GOAL_BOUND_TRANSFER' if all(x == 'NO_TRANSFER' for x in cw) else 'ASYMMETRIC_CROSS_WORLD'
    else: cwc = 'CROSS_WORLD_UNRESOLVED'          # missing, not run, no independent target, technical or partial
    if v in moved: scope = cwc                     # a scope only when the same-goal transfer holds in both worlds; cwc is always reported
    STATE878['verdict'] = {'verdict': v, 'scope': scope, 'blocks': blocks, 'worlds': dict(zip(WORLDS878, st)),
                           'same_goal': dict(zip(WORLDS878, sg)), 'cross_world': dict(zip(WORLDS878, cw)), 'cross_world_class': cwc,
                           'credit': 'ACTION_CREDIT_NOT_ESTABLISHED: A-blind dependence is not credit assignment',
                           'limits': ['no learning / closed loop / retrieval tested: forced mount', 'two real event pairs: pilot']}
    return STATE878['verdict']

def report878():
    words = ('ACQUIRE', 'BACKTRACK', 'REJECT', 'STOP', 'ACCEPT', 'ADVANCE'); f3 = lambda xs: ' '.join('%.3f' % x for x in xs)
    print('=' * 110)
    print('TEST878 PERSISTENT NATIVE EXPERIENCE TRANSFER | GPU %s | cell %s | prereg %s | api %s' % (CC_GPU.get('name'),
          STATE878['source'].get('executed_cell_git_blob'), PREREG_SHA878[:16], _j878.dumps(STATE878['api'].get('transformers'))))
    print('experience namespace: %s' % (EXP_DIR878 if 'EXP_DIR878' in globals() else None))
    for side in SOURCES878 + FORKS878:
        s = STATE878['sides'].get(side)
        print('  %s %s' % (side, 'NOT_REACHED' if not s else _j878.dumps({k: s.get(k) for k in (
            'role', 'card', 'E', 'C', 'X3_len', 'H', 'experience', 'roundtrip_K_rel', 'mounted', 'checks', 'error')}, default=str)))
    for w in WORLDS878:
        W = STATE878['worlds'].get(w)
        if not W: print('WORLD %s NOT_RUN' % w); continue
        print('WORLD %s status %s %s | reads %s elapsed_s %s peak_gib %s | static targets %s' % (w, W.get('status'), W.get('why', ''),
              W.get('reads'), W.get('elapsed_s'), W.get('peak_gib'), _j878.dumps(STATE878['targets_static'].get(w), sort_keys=True)))
        if W.get('gates'): print('  source pair gates %s' % _j878.dumps(W['gates'], sort_keys=True))
        S = W.get('source')
        if S:
            print('  SOURCE contrast M-L seq(15) %s' % f3(S['contrast']['seq']))
            print('  SOURCE |c| all15 first=%.4f seq=%.4f | action5 first=%.4f seq=%.4f | action selectivity seq=%.3f | pairs %s' % (
                S['norm_all15']['first'], S['norm_all15']['seq'], S['norm_action5']['first'], S['norm_action5']['seq'],
                S['action_selectivity_seq'], S['action_pairs']))
        for cnd, r in (W.get('persistence') or {}).items():
            print('  PERSIST %-7s pass=%s sha=%s lower_rows_bitwise=%s K_roundtrip_rel=%.5f action_same=%s max_dp=%.5f within_6e-4=%s '
                  'noise first=%.4f seq=%.4f explicit_append_bitwise=%s A_reference_mask=%s' % (cnd, r['pass'], r['reloaded_sha_ok'],
                  r['lower_rows_bitwise'], r['roundtrip_K_rel'], r['action_same'], r['max_dp'], r['within_6e-4'], r['noise']['first'],
                  r['noise']['seq'], r['explicit_append_equals_native_bitwise'], _j878.dumps(r['A_reference_mask'])))
        if W.get('floor'): print('  floor first=%.5f seq=%.5f' % (W['floor']['first'], W['floor']['seq']))
        for kind, p in (W.get('panels') or {}).items():
            print('  PANEL %-11s status %s %s' % (kind, p.get('status'), p.get('why', '')))
            if 'arms' not in p: continue
            print('    target %s spans %s gates %s A_BLIND %s' % (_j878.dumps(p['target']), _j878.dumps(p['spans']),
                  _j878.dumps(p['gates'], sort_keys=True), p['A_BLIND']))
            for arm, a in p['arms'].items():
                print('    %-10s %-9s ' % (arm, a['action']) + ' '.join('%s=%.4f' % (x, a['p'][x]) for x in words) +
                      ('' if arm == 'BASE' else ' | |m-BASE| seq=%.3f' % p['vs_base'][arm]['seq']))
            for arm, t in p['contrast'].items(): print('    contrast %-8s M-L seq(15) %s' % (arm, f3(t['seq'])))
            for arm, s in p['signature'].items():
                for k in ('first', 'seq'):
                    e = s[k]; print('    signature %-8s %-5s |T|15=%.4f |T|A5=%.4f |T|other10=%.4f selectivity=%.3f cos_A=%.3f rho_A=%.3f '
                                    'r_A=%.3f cos_all=%.3f' % (arm, k, e['norm_all15'], e['norm_action5'], e['norm_other10'],
                                    e['action_selectivity'], e['cos_A'], e['rho_A'], e['r_A'], e['cos_all15']))
            print('    detect %s | max dp FULL M vs L %.4f | A dependence %s' % (_j878.dumps(p['detect'], sort_keys=True),
                  p['max_dp_FULL_M_vs_L'], _j878.dumps(p.get('A_dependence'), sort_keys=True)))
            print('    A_REF gate %s | invalid_why %s' % (_j878.dumps(p.get('A_ref'), sort_keys=True), p.get('A_invalid_why')))
    v = STATE878['verdict'] or {}
    print('TEST878 VERDICT %s | scope %s | same-goal %s | cross-world %s (%s) | worlds %s | blocks %s | %s' % (v.get('verdict'),
          v.get('scope'), v.get('same_goal'), v.get('cross_world'), v.get('cross_world_class'), v.get('worlds'), v.get('blocks'),
          v.get('credit')))
    print('LIMITS: A-blind dependence is not credit assignment; forced mount, no retrieval, no closed loop, no learning claim; '
          'two real event pairs (pilot); labels are detectability classes above the reconstruction floor - read the sizes.')
    print('status %s | wall %.0f s | peak GPU %.2f GiB | GPU_EXECUTION_NOT_VERIFIED_BY_AUTHOR' % (STATE878['status'],
          time.perf_counter() - T_START878, torch.cuda.max_memory_allocated() / 2**30 if torch.cuda.is_available() else 0.0))
    print('=' * 110)

T_START878 = time.perf_counter()
try:
    STATE878['status'] = 'G0_SOURCE'; capture_source878()
    json_write864('878_prereg.json', {'prereg': PREREG878, 'sha256': PREREG_SHA878, 'before_model_load': True})
    line878('G0 PREREG', PREREG_SHA878)
    load_sources865(); source_audit878(); load878(); STATE878['ref873'] = ref873_874(RAW_SOURCES864['873.log'].decode())
    feasibility_audit864(); audit_contracts865(); load_spine864(); REFS878 = load_records870()
    STATE878['targets_static'] = targets878(REFS878)
    STATIC_T2_SHA878 = {s: [e['record'] for e in REFS878[(s, ARM878)]['events'] if e['type'] == 'CONTROL'][PRE_STEP878 - 1]['state_sha256']
                        for s in SOURCES878}
    line878('G0 SOURCE PASS', _j878.dumps(STATE878['source'], sort_keys=True))
    line878('G0 TARGETS', _j878.dumps(STATE878['targets_static'], sort_keys=True))
    STATE878['status'] = 'G1_PREFLIGHT'; assert CC_GPU_OK, ('GPU_PRECHECK', CC_GPU)
    env878, original_error878, original_trace878, reproduction878 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace878; TWO_JOB_VERIFICATION864 = verify_two_job859(env878, original_trace878)
    assert_hook_free859(env878, 'T878_before_native'); install_offline_evaluator859(env878)
    native878 = native_sequences860(env878); NATIVE_REGRESSION864 = native_regression864(env878, native878)
    verify_864_reference865(NATIVE_REGRESSION864); ANALYSIS864 = run_analysis863(env878, native878)
    assert len(STATE863['restores']) == 3 and all(r['exact'] for r in STATE863['restores'])
    digest878 = records_digest861(env878); null_seal878 = physical_seal863(env878, env878['MEMNULL841'])
    runtime_contracts865(env878); runtime_preflight865(env878, reproduction878); rearm_budget865(env878); make_slots866(env878)
    SLOTS867['PREV_EVALUATION'] = list(env878['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env878); resolve_append873(env878); api877(env878); WEIGHTS0_878 = weights_digest877(env878)
    chunk878 = [ns['CHUNK'] for ns in (env878['build_fusion'].__globals__, env878) if 'CHUNK' in ns]
    assert chunk878 and int(chunk878[0]) > 0 and all(k in env878 for k in ('P', 'to_gpu', 'kv_digest', 'entries')), 'EXPERIENCE_NAMESPACE'
    EXP878['CHUNK'] = int(chunk878[0])
    EXP_DIR878 = ROOT864.parent / ('TEST878_EXPERIENCE_CUT3_' + STAMP864); EXP_DIR878.mkdir(parents=True, exist_ok=False)
    assert_hook_free859(env878, 'T878_before_points')
    line878('G1 PREFLIGHT PASS', _j878.dumps(STATE878['api'], sort_keys=True), 'CHUNK=%d P=%d' % (EXP878['CHUNK'], int(env878['P'])),
            'model_load_s=%.0f' % (time.perf_counter() - T_START878))
    STATE878['status'] = 'RUNNING'; T0_865 = time.perf_counter(); by_key878 = build_specs869(env878)
    plan878 = [(s, {PRE_STEP878: 'T2_EXPERIENCE', POST_STEP878: 'T3_EXPERIENCE'}) for s in SOURCES878] + \
              [(s, {FORK_STEP878: 'T1_TARGET'}) for s in FORKS878 if STATE878['targets_static'][s.split('_')[1]]['SAME_GOAL']['independent']]
    for side, tg in plan878:
        guard878('replay_' + side)
        rep = run_replay870(env878, {'id': side, 'item': side, 'arm': ARM878, 'targets': tg}, by_key878, REFS878)
        T2_KEEP878.pop(side, None)
        if not rep['ok']: STATE878['blocks'].append('REPLAY_NOT_EXACT:' + side)
    json_write864('878_experience_manifest.json', jsafe878(STATE878['experience']))
    STATE878['status'] = 'TRANSFER'
    for w in WORLDS878: world878(env878, w)
    hook = hook_audit859(env878, 'T878_final')
    if records_digest861(env878) != digest878 or physical_seal863(env878, env878['MEMNULL841']) != null_seal878 or \
            hook['hook_count'] or hook['transformers_output_capturing_installed'] or weights_digest877(env878) != WEIGHTS0_878:
        STATE878['blocks'].append('POST_RUN_INTEGRITY')
    STATE878['status'] = 'COMPLETE'; verdict878()
except Partial878 as exc:
    STATE878['error'] = str(exc); STATE878['status'] = 'PARTIAL_AT_' + str(STATE878['status'])
    STATE878['verdict'] = {'verdict': 'PARTIAL_INCONCLUSIVE', 'blocks': [], 'why': str(exc)}
except BaseException as exc:
    STATE878['error'] = '%s: %s' % (type(exc).__name__, exc); STATE878['traceback'] = traceback.format_exc()
    STATE878['status'] = 'FAILED_AT_' + str(STATE878['status'])
    STATE878['verdict'] = {'verdict': 'TECHNICAL_BLOCK', 'blocks': ['EXCEPTION: ' + STATE878['error'][:300]]}
    (ROOT864 / '878_traceback.txt').write_text(STATE878['traceback'], encoding='utf-8')
    print('TEST878 ERROR', STATE878['error'][:300], '| full traceback:', ROOT864 / '878_traceback.txt', file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        json_write864('878_result.json', jsafe878(dict(STATE878, replays=STATE870['replays'])))
    except Exception as exc: print('RESULT_WRITE_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    try: report878()
    except Exception as exc: print('REPORT_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE878['suffix'], 'test870.py:suffix', 'exec'), globals())
