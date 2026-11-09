# AKBASCORE SILICON HIPPOCAMPUS — TEST877 — NATIVE DECISION CIRCUIT X-RAY
# One A100-SXM4-80GB Colab cell. Frozen Qwen2.5-72B-Instruct NF4, BF16. Locked engine test870.py (e322ed8).
# QUESTION: through which native pathway (attention output / MLP output / KV-group / query head at the CAR decision
# row) does the difference between two REAL physical outcome cartridges (MISSING vs LIVE, same pre-action state, same
# executed action, same C storage/logical span) reach the native CAR decision, with the TARGET X3 held fixed?
# Timeline per target: canonical H = [M_t2][X2][A][C real](native_append_direct) + [X3 target] -> CAR (car874/reading867).
# Whole-C swap = donor's canonical H (prefix bitwise equal, C rows of the donor) + target X3: no row is re-used out of
# its context. Patches replace ONLY the decision row D (last X3 row) output of attention (post-W_O), of the MLP, or a
# pre-W_O query-head slice, inside an explicit forward that calls the installed Qwen2 submodules in native order (no
# hooks); every later layer, the D row K/V and the teacher-forced CAR continuations are computed natively after it.
# Discovery: World 01 (both directions). Confirmation: World 00 with the pathway frozen before its replay starts.
# Never: weight writes, training, hooks, output_hidden_states/attentions, logit edits, action forcing, new cartridges.
import ast as _a877, hashlib as _h877, json as _j877, urllib.request as _u877
ENGINE_URL877 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB877, MARKER877 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc', 'AKBASCORE SILICON HIPPOCAMPUS — TEST877'

def blob877(raw):
    return _h877.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()

def engine_parts877():
    with _u877.urlopen(_u877.Request(ENGINE_URL877, headers={'User-Agent': 'AKBASCORE-TEST877'}), timeout=240) as r:
        raw = r.read()
    assert blob877(raw) == ENGINE_BLOB877, ('ENGINE_BLOB_MISMATCH', blob877(raw))
    text = raw.decode('utf-8'); _a877.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST877_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST877_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST877_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('877_engine.log', '877_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST877_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '877_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '877_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST877_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old)
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL877, 'git_blob': blob877(raw), 'sha256': _h877.sha256(raw).hexdigest()}

try:
    ENGINE877, ENGINE_INFO877 = engine_parts877()
except BaseException as _exc877:      # console capture starts inside the engine prefix: keep a local record of this failure
    import time as _t877, traceback as _tb877
    _p877 = '/content/TEST877_PRE_ENGINE_ERROR_%s.txt' % _t877.strftime('%Y%m%dT%H%M%SZ', _t877.gmtime())
    try:
        with open(_p877, 'w', encoding='utf-8') as _f877: _f877.write(_tb877.format_exc())
    except OSError: _p877 = 'NOT_WRITTEN'
    print('TEST877 PRE-ENGINE ERROR (before console capture):', type(_exc877).__name__, _exc877, '| traceback:', _p877)
    raise
exec(compile(ENGINE877['prefix'], 'test870.py:prefix', 'exec'), globals())
exec(compile(ENGINE877['body'], 'test870.py:engine', 'exec'), globals())
print('TEST877 ENGINE', _j877.dumps(ENGINE_INFO877, sort_keys=True))

# ============================ pre-registration (fixed before the model is loaded) ============================
# Committed files are locked through the engine's repository archive (load_sources865 / LOCKS864, git blobs).
# The executed-cell blobs printed in the logs are a different object (IPython cell text) and are kept as provenance.
LOCKS864.update({'test870.py': ENGINE_BLOB877, 'Test870.log': 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc',
                 '873.py': '2e44affa5e0dd462155fb265c331270fb8e7b7e1', '873.log': '1c9eb9fca173003eaf45bc7726af13c2817324b7',
                 '874.py': '12172001ba3696ad91087a8b34d7995728259e47', '874.log': '1229e3b70440e3887ccf1bd7e3bad51f900f5313',
                 '875.py': '23fd2ba8b967f447c748ce0e269ba8fc43660761', '875.log': '43488a95a5f68c6de2c06350148854995f121825',
                 '876.py': 'e08c5f57c3c14360d275deb750bb3de33e1d71cc', '876.log': 'dcfaece19f48ba10321f066014b874b9747d39be'})
TEST876_CELL_BLOB877, TEST876_PREREG877 = 'b0083bfe97fee946be41ae3234531c10020b6aca', '441e1be3e67e47d2'
TEST876_PREREG_DEPS877 = ('WORLDS876', 'SIDES876', 'CORRECTIVE876', 'ARMS876', 'SHIFT_MIN876', 'LIVE_TOL876',
                          'WORK_TOKENS876', 'EVAL_TOKENS876', 'PREREG876')
TEST870_MINUTES = TEST865_MINUTES = 110.0
SIDES877 = ('I867_01_MISSING', 'I867_01_LIVE', 'I867_00_MISSING', 'I867_00_LIVE')
SIDES874, _a874, _j874 = SIDES877, _a877, _j877   # module names read by the selected 874.py functions
DISCOVERY877, CONFIRM877 = '01', '00'
ARM877, PRE_STEP877, POST_STEP877 = 'V_X', 2, 3
FUNCS873 = ('kv873', 'length873', 'forward873', 'car873', 'resolve_append873', 'append_card873', 'decide873',
            'probs873', 'same873', 'tv873')
FUNCS874 = ('load873_874', 'ref873_874', 'keep874', 'forward874', 'car874', 'rows874', 'decide874', 'rel874')
BLOCKS877 = ((0, 20), (20, 40), (40, 60), (60, 80))
ROPE_TOL877, REPRO_TOL877, NUM_FLOOR877, DETECT_X877, RHO_MIN877 = 1e-2, 6e-4, 1e-5, 5.0, 0.5
HARD_MIN877, VRAM_ABORT_GIB877 = 100.0, 60.0
PREREG877 = {
    'question': 'native pathway carrying the REAL C-content difference to the CAR decision, target X3 fixed',
    'sides': SIDES877, 'discovery_world': DISCOVERY877, 'confirmation_world': CONFIRM877, 'arm': ARM877,
    'arms_per_target': {'NATIVE': 'decide874 on canonical H (TEST874-876 GPU path)',
                        'BASE': 'explicit forward, no patch: must equal NATIVE bitwise (readings and X3 K/V rows)',
                        'SWAP': 'DIAGNOSTIC_REAL_CONTENT_SWAP: donor canonical H (prefix bitwise equal) + target X3',
                        'MASK': 'target C not readable (2-D key mask) by X3 and every CAR continuation',
                        'MASKED_DONOR': 'donor C masked + target X3: must equal MASK bitwise',
                        'SELF_PATCH': 'own attention / MLP / pre-W_O outputs patched back at D, all layers: must equal BASE',
                        'PATCH': 'DIAGNOSTIC_ACTIVATION_PATCH: SWAP-run D-row outputs on the pathway, into BASE',
                        'ABLATE_SHAM': 'DIAGNOSTIC_SHAM: MASK-run D-row outputs on the pathway, into BASE',
                        'RESCUE': 'SWAP-run pathway into MASK (frozen pathway only, reported)'},
    'metrics': 'first-token and full-sequence logp of the 6 CAR words, 15 pairwise margins each; reading867 unchanged',
    'effects': 'tau = m(SWAP)-m(BASE); nu = m(BASE)-m(MASK); P = m(PATCH)-m(BASE); A = m(ABLATE_SHAM)-m(BASE)',
    'rho_r': 'rho = <P,tau>/|tau|^2; r = |tau-P|/|tau|; r_sham = |tau-A|/|tau| (sequence margins primary)',
    'num_floor': 'tau_num = max(%g, max no-op |dm|); detectable: |tau| > %g * tau_num' % (NUM_FLOOR877, DETECT_X877),
    'pass_rule': 'both directions: rho_seq >= %g and r_seq < r_sham_seq' % RHO_MIN877,
    'levels': ['8 blocks: {attn, mlp} x %s' % (BLOCKS877,), 'if exactly one: its 20 single layers (same pathway)',
               'if exactly one attn layer: 8 KV groups (pre-W_O slice 1024g:1024(g+1) = query heads 8g..8g+7)',
               'if exactly one group: its 8 query heads (128q:128(q+1))',
               'freeze the finest level with exactly one passing candidate; 0 or >1 at block level -> stop'],
    'distributed_vs_none': 'no block passes: full-depth attn or mlp passes -> DISTRIBUTED_PATH else NO_LOCALIZED_PATH; '
                           '>1 block passes -> DISTRIBUTED_PATH',
    'confirmation': 'World 00 replayed only with a frozen manifest; same gates; frozen pathway must pass the same rule',
    'stops': ['G3 mismatch -> NO_DATA', 'tau not detectable: nu detectable -> NONSPECIFIC_CONTEXT_EFFECT else NO_EFFECT',
              'first-token tau not detectable but sequence tau detectable -> CAR_CONTINUATION_ONLY',
              'hard stop %g min or %g GiB -> PARTIAL_INCONCLUSIVE' % (HARD_MIN877, VRAM_ABORT_GIB877)],
    'limits': ['VALUE_NOT_IDENTIFIED', 'WRITABLE_LEARNING_NOT_TESTED', 'two event pairs: pilot, no population claim']}
PREREG_SHA877 = sha256_bytes864(_j877.dumps(PREREG877, sort_keys=True).encode())
STATE877 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO877, 'prereg_sha256': PREREG_SHA877, 'source': {}, 'api': {},
            'ref873': {}, 'sides': {}, 'worlds': {}, 'frozen': None, 'blocks': [], 'verdict': None, 'error': None}
T2_KEEP877, PAIR877, MOD877 = {}, {}, {}

class Partial877(Exception):
    pass

def line877(*parts): short864('T877', *parts)

def capture_source877():
    try:
        hist = [t for t in get_ipython().history_manager.input_hist_raw if MARKER877 in t and 'def probe877' in t]
        source, how = hist[-1], 'IPYTHON_CELL'
    except (NameError, IndexError):
        source = open(__file__, encoding='utf-8').read() if '__file__' in globals() else None; how = 'FILE_%RUN'
    assert source and MARKER877 in source, 'EXECUTED_877_SOURCE_NOT_CAPTURED'
    tree = _a877.parse(source)
    banned = {'register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook', 'output_hidden_states',
              'output_attentions', 'install_all_output_capturing_hooks', 'backward', 'requires_grad_', 'step', 'zero_grad',
              'execute866', 'mount865', 'free865', 'hop865', 'native_append_direct'}
    for node in tree.body:
        if isinstance(node, _a877.FunctionDef) and node.name.endswith('877') and node.name != 'capture_source877':
            used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in _a877.walk(node) if isinstance(c, _a877.Call)}
            used |= {k.arg for k in _a877.walk(node) if isinstance(k, _a877.keyword)}
            assert not used & banned, ('FIREWALL877', node.name, sorted(used & banned))
    calls = [n for n in _a877.walk(tree) if isinstance(n, _a877.Call) and getattr(n.func, 'id', None) == 'reproduce_pre859859']
    assert len(calls) == 1, 'MODEL_LOADER_CALL_COUNT_NOT_ONE'
    rs = [n for n in tree.body if isinstance(n, _a877.Assign) and any(getattr(t, 'id', '') == 'xray_point870' for t in n.targets)]
    assert len(rs) == 1 and getattr(rs[0].value, 'id', None) == 'probe877', 'FIREWALL877_REBIND'
    (ROOT864 / 'TEST877.py').write_text(source, encoding='utf-8')
    STATE877['source'] = {'how': how, 'executed_cell_git_blob': git_blob864(source.encode()),
                          'executed_cell_sha256': sha256_bytes864(source.encode()), 'lines': source.count('\n') + 1,
                          'firewall': 'PASS'}

def source_audit877():
    # TEST876: committed file (archive lock) vs executed cell (log). Byte equality of the cell is NOT provable from the
    # published artefacts; the committed file must reproduce the run's printed pre-registration hash (fail closed).
    tree = _a877.parse(RAW_SOURCES864['876.py'].decode(), filename='876.py')
    by = {}
    for n in tree.body:
        if isinstance(n, _a877.Assign):
            for t in n.targets:
                for x in _a877.walk(t):
                    if isinstance(x, _a877.Name): by.setdefault(x.id, n)
    nodes = sorted({id(by[k]): by[k] for k in TEST876_PREREG_DEPS877}.values(), key=lambda n: n.lineno)
    ns = {}; exec(compile(_a877.fix_missing_locations(_a877.Module(nodes, [])), '876.py:prereg', 'exec'), ns)
    pre876 = _h877.sha256(_j877.dumps(ns['PREREG876'], sort_keys=True).encode()).hexdigest()
    log = RAW_SOURCES864['876.log'].decode()
    run = [x for x in log.splitlines() if x.startswith('TEST876 | GPU NVIDIA A100-SXM4-80GB | source ')]
    assert pre876.startswith(TEST876_PREREG877), ('TEST876_PREREG_MISMATCH', pre876[:16])
    assert len(run) == 1 and (' source %s ' % TEST876_CELL_BLOB877) in run[0] and ('| prereg %s' % TEST876_PREREG877) in run[0], \
        ('TEST876_RUN_LINE', run)
    for name, needles in (('Test870.log', ('XR870 CALIBRATION CALIBRATION_PASS', 'NVIDIA A100')),
                          ('873.log', ('TEST873 OUTCOME', 'status COMPLETE', 'NVIDIA A100')),
                          ('876.log', ('TEST876 OUTCOME', 'NVIDIA A100', 'peak GPU'))):
        assert all(x in RAW_SOURCES864[name].decode() for x in needles), ('LOCKED_LOG_NOT_A_GPU_RUN', name)
    STATE877['source']['test876'] = {'committed_file_git_blob': LOCKS864['876.py'], 'executed_cell_git_blob_in_log':
        TEST876_CELL_BLOB877, 'prereg_reproduced_from_file': pre876[:16],
        'identity': 'committed file reproduces the run pre-registration; executed-cell bytes are not published'}

def load877():
    tree = _a877.parse(RAW_SOURCES864['874.py'].decode(), filename='874.py')
    nodes = [n for n in tree.body if isinstance(n, _a877.FunctionDef) and n.name in FUNCS874]
    assert {n.name for n in nodes} == set(FUNCS874), 'SELECT_874'
    exec(compile(_a877.fix_missing_locations(_a877.Module(body=nodes, type_ignores=[])), '874.py:selected', 'exec'), globals())
    load873_874()

def api877(env):
    # The explicit forward below re-states the installed Qwen2 forward order. Verify the installed sources first.
    import sys, inspect, transformers
    m = env['model']; base = m.model; cfg = base.config; sa = base.layers[0].self_attn
    src = {k: inspect.getsource(f) for k, f in (('attn', type(sa).forward), ('layer', type(base.layers[0]).forward),
                                                ('model', type(base).forward), ('lm', type(m).forward))}
    need = {'attn': ['query_states = self.q_proj(hidden_states).view(hidden_shape).transpose(1, 2)',
                     'key_states = self.k_proj(hidden_states).view(hidden_shape).transpose(1, 2)',
                     'value_states = self.v_proj(hidden_states).view(hidden_shape).transpose(1, 2)',
                     'query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin)',
                     'key_states, value_states = past_key_values.update(key_states, value_states, self.layer_idx)',
                     'ALL_ATTENTION_FUNCTIONS.get_interface(', 'scaling=self.scaling', 'sliding_window=self.sliding_window',
                     'attn_output = attn_output.reshape(*input_shape, -1).contiguous()', 'attn_output = self.o_proj(attn_output)'],
            'layer': ['hidden_states = self.input_layernorm(hidden_states)', 'hidden_states = self.post_attention_layernorm(hidden_states)',
                      'hidden_states = self.mlp(hidden_states)'],
            'model': ['"full_attention": create_causal_mask(**mask_kwargs)', 'hidden_states = inputs_embeds',
                      'position_embeddings = self.rotary_emb(hidden_states, position_ids)', 'hidden_states = self.norm(hidden_states)'],
            'lm': ['hidden_states = slice_logits_to_keep(hidden_states, logits_to_keep)', 'logits = self.lm_head(hidden_states)']}
    miss = {k: [s for s in v if s not in src[k]] for k, v in need.items()}
    assert not any(miss.values()), ('INSTALLED_QWEN2_SOURCE_DIFFERS', miss)
    assert src['layer'].count('hidden_states = residual + hidden_states') == 2, 'DECODER_RESIDUALS'
    assert (int(cfg.num_hidden_layers), int(cfg.hidden_size), int(cfg.num_attention_heads), int(cfg.num_key_value_heads),
            int(sa.head_dim)) == (80, 8192, 64, 8, 128), 'QWEN2_72B_SHAPE'
    assert cfg._attn_implementation == 'sdpa' and not getattr(base, 'has_sliding_layers', False) and \
        set(cfg.layer_types) == {'full_attention'}, 'ATTENTION_IMPLEMENTATION'
    assert not any(p.requires_grad for p in m.parameters()) and not m.training, 'NOT_FROZEN_EVAL'
    lm_mod, at_mod = sys.modules[type(base).__module__], sys.modules[type(sa).__module__]
    MOD877.update({'mask': lm_mod.create_causal_mask, 'rope': at_mod.apply_rotary_pos_emb, 'attn_mod': at_mod,
                   'NL': int(cfg.num_hidden_layers), 'NH': int(cfg.num_attention_heads), 'NKV': int(cfg.num_key_value_heads),
                   'HD': int(sa.head_dim)})
    STATE877['api'] = {'transformers': transformers.__version__, 'torch': torch.__version__,
                       'source_sha256': {k: _h877.sha256(v.encode()).hexdigest()[:16] for k, v in src.items()},
                       'shape': [80, 8192, 64, 8, 128], 'attn': 'sdpa'}

def weights_digest877(env):
    m = env['model']; h = _h877.sha256()
    for t in (m.model.embed_tokens.weight[:64], m.model.norm.weight, m.lm_head.weight[:64],
              m.model.layers[0].input_layernorm.weight, m.model.layers[79].post_attention_layernorm.weight):
        h.update(t.detach().float().cpu().numpy().tobytes())
    return h.hexdigest()

# ============================ explicit native forward (no hooks) ============================
def xattn877(sa, x, pe, mask, cache, pid, cpos, pre_patch, rec, mass):
    # Qwen2Attention.forward of the installed transformers, statement by statement (checked by api877 + parity).
    input_shape = x.shape[:-1]; hidden_shape = (*input_shape, -1, sa.head_dim)
    q = sa.q_proj(x).view(hidden_shape).transpose(1, 2)
    k = sa.k_proj(x).view(hidden_shape).transpose(1, 2)
    v = sa.v_proj(x).view(hidden_shape).transpose(1, 2)
    cos, sin = pe
    q, k = MOD877['rope'](q, k, cos, sin)
    k, v = cache.update(k, v, sa.layer_idx)
    iface = MOD877['attn_mod'].ALL_ATTENTION_FUNCTIONS.get_interface(sa.config._attn_implementation,
                                                                     MOD877['attn_mod'].eager_attention_forward)
    o, _ = iface(sa, q, k, v, mask, dropout=0.0 if not sa.training else sa.attention_dropout, scaling=sa.scaling,
                 sliding_window=sa.sliding_window, position_ids=pid, use_cache=True, cache_position=cpos)
    o = o.reshape(*input_shape, -1).contiguous()
    for s, e, val in pre_patch or ():
        o[:, -1, s:e] = val                       # pre-W_O query-head slice of the decision row only
    if rec is not None: rec.append(o[0, -1].clone())
    if mass is not None:                          # descriptive: D-row attention mass on C per query head (GQA: q//8)
        qd, kk = q[0, :, -1, :].float(), k[0].float()
        grp = torch.arange(qd.shape[0], device=qd.device) // (qd.shape[0] // kk.shape[0])
        w = torch.softmax(torch.einsum('hd,hnd->hn', qd, kk[grp]) * sa.scaling, dim=-1)
        mass['C'] = [round(float(x), 6) for x in w[:, mass['c0']:mass['c1']].sum(-1)]
        del qd, kk, w
    return sa.o_proj(o)

def xforward877(env, cache, Y, keep, last, patch=None, rec=None, mass=None):
    # Same call as forward874 (2-D mask from `keep`, RoPE = storage positions) but layer by layer.
    model = env['model']; base = model.model; cfg = base.config; P = patch or {}
    L, nc = int(Y.shape[0]), int(cache.get_seq_length())
    assert int(keep.shape[0]) == nc, ('KEEP_LENGTH', int(keep.shape[0]), nc)
    am = torch.ones((1, nc + L), device=env['DEV'], dtype=torch.long); am[0, :nc] = keep
    pos, cpos = torch.arange(nc, nc + L, device=env['DEV']), torch.arange(nc, nc + L, device=env['DEV'])
    pid = pos.unsqueeze(0)
    with torch.no_grad():
        h = Y.reshape(1, L, env['H'])
        mask = MOD877['mask'](config=cfg, inputs_embeds=h, attention_mask=am, past_key_values=cache, position_ids=pid)
        pe = base.rotary_emb(h, pid)
        for i, layer in enumerate(base.layers[:cfg.num_hidden_layers]):
            if rec is not None: rec['resid'].append(h[0, -1].clone())
            res = h; x = layer.input_layernorm(h)
            a = xattn877(layer.self_attn, x, pe, mask, cache, pid, cpos, P.get('pre', {}).get(i),
                         None if rec is None else rec['pre'], mass if (mass is not None and mass['layer'] == i) else None)
            if i in P.get('attn', {}): a[:, -1, :] = P['attn'][i]
            if rec is not None: rec['attn'].append(a[0, -1].clone())
            h = res + a
            res = h; x = layer.post_attention_layernorm(h); mo = layer.mlp(x)
            if i in P.get('mlp', {}): mo[:, -1, :] = P['mlp'][i]
            if rec is not None: rec['mlp'].append(mo[0, -1].clone())
            h = res + mo
        h = base.norm(h)
        logits = model.lm_head(h)                 # all rows, as Qwen2ForCausalLM with logits_to_keep=0 (same GEMM shape)
        logp = torch.log_softmax(logits[0, -last:].float(), dim=-1)
        del logits, h
    assert int(cache.get_seq_length()) == nc + L, 'TIMELINE_NOT_EXTENDED_877'
    return logp

def rec877(): return {'resid': [], 'attn': [], 'mlp': [], 'pre': []}

def xcar877(env, kv, X, ranges=(), patch=None, rec=None, mass=None, rows=False):
    # car874 procedure; the X3 forward is explicit (patch/record at D), continuations are forward874 (native) and cropped.
    cache = env['cache_build'](list(kv)); n0 = int(cache.get_seq_length())
    keep = keep874(env, n0, list(ranges)); env['budget849']()
    L = int(X.shape[0]); n1, p1 = n0 + L, n0 + L
    assert p1 + max(len(ids) for _, ids in ACTION_IDS867) <= int(env['MAX_FUSED_TOKENS']), ('CONTEXT_LIMIT', p1)
    first = xforward877(env, cache, X, keep, 1, patch, rec, mass)[0]
    keep1 = torch.cat([keep, torch.ones(L, dtype=keep.dtype, device=keep.device)])
    scores = []
    for word, ids in ACTION_IDS867:
        token_logps = [float(first[ids[0]])]
        if len(ids) > 1:
            m = len(ids) - 1
            lp = forward874(env, cache, env['embed841'](ids[:-1]), p1, keep1, m)
            cache.crop(-m)
            assert int(cache.get_seq_length()) == n1, 'CAR_CROP_LENGTH_MISMATCH_877'
            token_logps += [float(lp[i, ids[i + 1]]) for i in range(m)]
            del lp
        scores.append({'word': word, 'ids': ids, 'token_logps': token_logps, 'sequence_logp': float(sum(token_logps)),
                       'hard_greedy_ids': []})
    top = torch.topk(first, 10)
    reading = reading867({'scores': scores, 'path': 'CROP', 'fallback_reason': None,
                          'first_top10': {'ids': [int(i) for i in top.indices.tolist()]}, 'X_sha256': None})
    got = rows874(env, cache, L) if rows else None
    del cache, first
    return reading, got

# ============================ margins and effects ============================
def marg877(r):
    W = [w for w, _ in ACTION_IDS867]; pairs = [(a, b) for i, a in enumerate(W) for b in W[i + 1:]]
    f = {s['word']: s['token_logps'][0] for s in r['scores']}; q = {s['word']: s['sequence_logp'] for s in r['scores']}
    return {'first': [f[a] - f[b] for a, b in pairs], 'seq': [q[a] - q[b] for a, b in pairs]}

def sub877(a, b): return [x - y for x, y in zip(a, b)]
def nrm877(a): return sum(x * x for x in a) ** 0.5
def dif877(ma, mb): return {k: sub877(ma[k], mb[k]) for k in ('first', 'seq')}
def maxabs877(d): return max(abs(x) for k in ('first', 'seq') for x in d[k])

def effect877(tau, P, A):
    out = {}
    for k in ('first', 'seq'):
        tt, nt = sum(x * x for x in tau[k]), nrm877(tau[k])
        out[k] = {'rho': sum(x * y for x, y in zip(P[k], tau[k])) / (tt + 1e-12),
                  'r': nrm877(sub877(tau[k], P[k])) / (nt + 1e-12), 'r_sham': nrm877(sub877(tau[k], A[k])) / (nt + 1e-12),
                  'norm_P': nrm877(P[k]), 'norm_A': nrm877(A[k])}
    out['pass'] = out['seq']['rho'] >= RHO_MIN877 and out['seq']['r'] < out['seq']['r_sham']
    return out

def arm877(r): return {'action': r['action'], 'p': probs873(r)}

def guard877(stage):
    el = (time.perf_counter() - T_START877) / 60.0; peak = torch.cuda.max_memory_allocated() / 2**30
    if el > HARD_MIN877 or peak > VRAM_ABORT_GIB877:
        raise Partial877('%s: elapsed %.1f min, peak %.2f GiB' % (stage, el, peak))

# ============================ world panel (gates + total effect) ============================
def total877(env, w, M, L):
    out = {'world': w, 'gates': {}, 'targets': {}, 'reads': 0}
    nb, c1 = M['n_before'], M['x3s']
    g = out['gates']
    g['G3_same_C_span'] = (M['n_before'], M['x3s'], M['body']) == (L['n_before'], L['x3s'], L['body'])
    g['G3_same_action'] = M['t2_action'] == L['t2_action'] == 'ACQUIRE' and M['A_ids'] == L['A_ids']
    g['G3_real_cards_differ'] = M['card'] != L['card']
    g['G3_prefix_bitwise'] = g['G3_same_C_span'] and all(torch.equal(M['gH'][i][j][:, :, :nb], L['gH'][i][j][:, :, :nb])
                                                        for i in range(len(M['gH'])) for j in (0, 1))
    if g['G3_same_C_span'] and not g['G3_prefix_bitwise']:
        out['prefix_max_rel'] = max(rel874(*[[tuple(t[:, :, :nb] for t in kv) for kv in x['gH']] for x in (M, L)]))
    out['C'] = [nb, c1]; out['cards'] = {'MISSING': M['card'], 'LIVE': L['card']}
    out['X3_len'] = {'MISSING': int(M['X3'].shape[0]), 'LIVE': int(L['X3'].shape[0])}
    if not all(v for k, v in g.items() if k.startswith('G3')):
        out['status'] = 'NO_DATA'; return out
    noop = []
    for t, d in ((M, L), (L, M)):
        guard877('total_%s_%s' % (w, t['cond']))
        T = {}
        nat, rows_n, _, _ = decide874(env, t['gH'], t['X3'], [], rows=True)
        T['recB'] = rec877(); base, rows_x = xcar877(env, t['gH'], t['X3'], (), rec=T['recB'], rows=True)
        T['recS'] = rec877(); swap, _ = xcar877(env, d['gH'], t['X3'], (), rec=T['recS'])
        T['recM'] = rec877(); mask, _ = xcar877(env, t['gH'], t['X3'], [(nb, c1)], rec=T['recM'])
        mdon, _ = xcar877(env, d['gH'], t['X3'], [(nb, c1)])
        NL, width = MOD877['NL'], MOD877['NH'] * MOD877['HD']
        sp = {'attn': {i: T['recB']['attn'][i] for i in range(NL)}}
        sm = {'mlp': {i: T['recB']['mlp'][i] for i in range(NL)}}
        sh = {'pre': {i: [(0, width, T['recB']['pre'][i])] for i in range(NL)}}
        selfs = [xcar877(env, t['gH'], t['X3'], (), patch=p)[0] for p in (sp, sm, sh)]
        out['reads'] += 8
        mB, mS, mM, mMD = (marg877(x) for x in (base, swap, mask, mdon))
        mN = marg877(nat)
        T['gates'] = {'G2_explicit_equals_native': same873(nat, base) and all(
                          torch.equal(x, y) for p, q in zip(rows_n, rows_x) for x, y in zip(p, q)),
                      'G6_self_patch_noop': all(same873(base, s) for s in selfs),
                      'G6_masked_donor_equals_mask': same873(mask, mdon)}
        noop += [maxabs877(dif877(mN, mB)), maxabs877(dif877(mMD, mM))] + [maxabs877(dif877(marg877(s), mB)) for s in selfs]
        T['m'] = {'BASE': mB, 'SWAP': mS, 'MASK': mM}
        T['arms'] = {'NATIVE': arm877(nat), 'BASE': arm877(base), 'SWAP': arm877(swap), 'MASK': arm877(mask),
                     'MASKED_DONOR': arm877(mdon)}
        T['tau'], T['nu'] = dif877(mS, mB), dif877(mB, mM)
        T['did'] = dif877(T['tau'], dif877(mMD, mM))
        T['obs'] = {k: [round(float(torch.linalg.vector_norm(T['recS'][k][i].float() - T['recB'][k][i].float())), 4)
                        for i in range(MOD877['NL'])] for k in ('resid', 'attn', 'mlp')}
        del rows_n, rows_x
        out['targets'][t['cond']] = T
    out['tau_num'] = max([NUM_FLOOR877] + noop)
    for cond, T in out['targets'].items():
        for k in ('G2_explicit_equals_native', 'G6_self_patch_noop', 'G6_masked_donor_equals_mask'):
            g['%s_%s' % (k, cond)] = T['gates'][k]
        T['detect'] = {k: nrm877(T['tau'][k]) > DETECT_X877 * out['tau_num'] for k in ('first', 'seq')}
        T['detect']['nu'] = nrm877(T['nu']['seq']) > DETECT_X877 * out['tau_num']
        T['norms'] = {'tau_first': nrm877(T['tau']['first']), 'tau_seq': nrm877(T['tau']['seq']),
                      'nu_seq': nrm877(T['nu']['seq']), 'did_minus_tau': maxabs877(dif877(T['did'], T['tau']))}
    if not all(g[k] for k in g if k.startswith(('G2', 'G6_self'))): out['status'] = 'CACHE_PARITY_FAIL'; return out
    if not all(g[k] for k in g if k.startswith('G6_masked')): out['status'] = 'MASK_PARITY_FAIL'; return out
    Ts = list(out['targets'].values())
    if not all(T['detect']['seq'] for T in Ts):
        out['status'] = 'NONSPECIFIC_CONTEXT_EFFECT' if any(T['detect']['nu'] for T in Ts) else 'NO_EFFECT'
    elif not any(T['detect']['first'] for T in Ts):
        out['status'] = 'CAR_CONTINUATION_ONLY'
    else:
        out['status'] = 'TOTAL_EFFECT'
    return out

def build877(path, rec):
    kind, layers = path['kind'], path['layers']
    if kind == 'pre':
        s, e = path['slice']; return {'pre': {i: [(s, e, rec['pre'][i][s:e])] for i in layers}}
    return {kind: {i: rec[kind][i] for i in layers}}

def test877(env, tot, M, L, path):
    # one pathway, both directions: PATCH (SWAP-run D outputs) and ABLATE_SHAM (MASK-run D outputs) into BASE
    res = {'path': path, 'dirs': {}}
    for t in (M, L):
        T = tot['targets'][t['cond']]
        rp, _ = xcar877(env, t['gH'], t['X3'], (), patch=build877(path, T['recS']))
        ra, _ = xcar877(env, t['gH'], t['X3'], (), patch=build877(path, T['recM']))
        e = effect877(T['tau'], dif877(marg877(rp), T['m']['BASE']), dif877(marg877(ra), T['m']['BASE']))
        e['PATCH'], e['ABLATE_SHAM'] = arm877(rp), arm877(ra)
        res['dirs'][t['cond'] + '<-donor'] = e
    tot['reads'] += 4
    res['pass'] = all(e['pass'] for e in res['dirs'].values())
    return res

def scan877(env, tot, M, L):
    # discovery only: pre-registered hierarchy; freeze the finest level with exactly one passing candidate
    sc = {'levels': [], 'frozen': None}
    def level(name, paths):
        guard877('scan_' + name)
        rows = [test877(env, tot, M, L, p) for p in paths]
        sc['levels'].append({'level': name, 'rows': rows, 'passing': [r['path'] for r in rows if r['pass']]})
        return [r['path'] for r in rows if r['pass']]
    blocks = level('block', [{'kind': k, 'layers': list(range(a, b)), 'label': '%s_L%d-%d' % (k, a, b - 1)}
                             for k in ('attn', 'mlp') for a, b in BLOCKS877])
    if len(blocks) != 1:
        if not blocks:
            full = level('full_depth', [{'kind': k, 'layers': list(range(MOD877['NL'])), 'label': '%s_all_layers' % k}
                                        for k in ('attn', 'mlp')])
            sc['status'] = 'DISTRIBUTED_PATH' if full else 'NO_LOCALIZED_PATH'
        else:
            sc['status'] = 'DISTRIBUTED_PATH'
        return sc
    sel = blocks[0]; sc['frozen'] = dict(sel, granularity='block')
    layers = level('layer', [{'kind': sel['kind'], 'layers': [i], 'label': '%s_L%d' % (sel['kind'], i)} for i in sel['layers']])
    if len(layers) == 1:
        sc['frozen'] = dict(layers[0], granularity='layer')
        if sel['kind'] == 'attn':
            li, hd, gs = layers[0]['layers'][0], MOD877['HD'], MOD877['NH'] // MOD877['NKV']    # GQA: query head q -> KV q//gs
            groups = level('kv_group', [{'kind': 'pre', 'layers': [li], 'slice': (hd * gs * g, hd * gs * (g + 1)), 'kv_group': g,
                                         'label': 'L%d_kvgroup%d_heads%d-%d' % (li, g, gs * g, gs * g + gs - 1)}
                                        for g in range(MOD877['NKV'])])
            if len(groups) == 1:
                sc['frozen'] = dict(groups[0], granularity='kv_group')
                g0 = groups[0]['kv_group']
                heads = level('head', [{'kind': 'pre', 'layers': [li], 'slice': (hd * q, hd * (q + 1)), 'query_head': q, 'kv_group': g0,
                                        'label': 'L%d_head%d_kv%d' % (li, q, g0)} for q in range(gs * g0, gs * g0 + gs)])
                if len(heads) == 1:
                    sc['frozen'] = dict(heads[0], granularity='head')
    sc['status'] = 'LOCALIZED_CIRCUIT_CANDIDATE'
    return sc

def frozen_extras877(env, tot, M, L, path):
    # reported only: RESCUE (SWAP-run pathway into MASK) and descriptive D-row attention mass on C
    out = {}
    nb, c1 = tot['C']
    for t in (M, L):
        T = tot['targets'][t['cond']]
        rr, _ = xcar877(env, t['gH'], t['X3'], [(nb, c1)], patch=build877(path, T['recS']))
        ref = dif877(T['m']['SWAP'], T['m']['MASK']); R = dif877(marg877(rr), T['m']['MASK'])
        ent = {'RESCUE': arm877(rr), 'rho_rescue_seq': sum(x * y for x, y in zip(R['seq'], ref['seq'])) / (sum(x * x for x in ref['seq']) + 1e-12)}
        if path['kind'] in ('attn', 'pre') and len(path['layers']) == 1:
            mass = {'layer': path['layers'][0], 'c0': nb, 'c1': c1}
            xcar877(env, t['gH'], t['X3'], (), mass=mass); ent['C_attention_mass_by_query_head'] = mass['C']
        out[t['cond']] = ent
    tot['reads'] += 4
    return out

# ============================ replay tap ============================
def probe877(env, ctx, record, state, label):
    side = ctx['spec']['item']; world, cond = side.split('_')[1], side.split('_')[2]
    q = env['QTEXT841'][ctx['spec']['qid']]
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
    out = STATE877['sides'].setdefault(side, {'checks': {}, 'error': None}); c = out['checks']; t0 = time.perf_counter()
    try:
        ids = dict(ACTION_IDS867)
        if ctx['steps'] == PRE_STEP877:
            out['t2_action'] = record['action']
            segs2 = list(state['segments']); X2, _ = env['make_x851'](pre, segs2, post); L2 = int(X2.shape[0])
            m2 = [tuple(t.clone() for t in kv) for kv in ctx['memx']]; n2 = length873(env, m2)
            cache = env['cache_build'](list(m2)); c['t2_CAR_equals_record'] = same873(car873(env, cache, X2), record['reading'])
            c['t2_crops'] = int(cache.get_seq_length()) == n2 + L2
            own = env['cache_build'](list(kv873(env, cache))); del cache
            forward873(env, own, env['embed841'](ids[record['action']]), n2 + L2); keep_own = kv873(env, own); del own, m2
            c['commit_length'] = length873(env, keep_own) == n2 + L2 + len(ids[record['action']])
            T2_KEEP877[side] = {'own': keep_own, 'A_ids': ids[record['action']], 't2_action': record['action']}
            assert c['t2_CAR_equals_record'] and c['t2_crops'] and c['commit_length'], c
            return
        z = T2_KEEP877.pop(side)
        memx = ctx['memx']; eff = [e for e in ctx['events'] if e.get('type') == 'EFFECT'][-1]; card = eff.get('chosen')
        body = int(env['entries'][card]['body_tokens']); n3 = int(memx[0][0].shape[-2]); out['card'] = card
        c['card_mounted'] = eff.get('effect') == 'MOUNTED' and list(ctx['M'])[-1] == card
        names = slot_names869(env, list(state['segments']))
        X3, _ = env['make_x851'](pre, [s for s, n in zip(state['segments'], names) if n not in ('FV', 'FK')], post)
        seal0 = prefix_seals865(env, memx); hook0 = assert_hook_free859(env, 'T877_before_' + side)
        gH, n_before = append_card873(env, z['own'], card); del z['own']
        x3s = n_before + body
        cut, rephase = APPEND873['CUT'], APPEND873['rephase']
        c['lower_V_bitwise'] = all(torch.equal(gH[i][1][:, :, n_before:], memx[i][1][:, :, n3 - body:]) for i in range(cut + 1))
        rope = max(float(torch.linalg.vector_norm(rephase(gH[i][0][:, :, n_before:], torch.arange(n_before, x3s, device=env['DEV']),
            torch.arange(n3 - body, n3, device=env['DEV'])).float() - memx[i][0][:, :, n3 - body:].float())) /
            max(float(torch.linalg.vector_norm(memx[i][0][:, :, n3 - body:].float())), 1e-30) for i in range(cut + 1))
        c['lower_K_rephase'] = rope <= ROPE_TOL877; out['lower_K_rephase_rel'] = rope
        rH, _, _, _ = decide874(env, gH, X3, [])
        ref = STATE877['ref873'][side]['T1']
        c['H_reproduces_873'] = rH['action'] == ref['action'] and all(abs(probs873(rH)[w] - ref['p'][w]) <= REPRO_TOL877 for w in ref['p'])
        out.update({'H': arm877(rH), 'C': [n_before, x3s], 'X3_len': int(X3.shape[0]), 'n_before': n_before})
        c['memory_seal'] = prefix_seals865(env, memx) == seal0
        hook1 = assert_hook_free859(env, 'T877_after_' + side)
        c['hook_free'] = not any(x['hook_count'] or x['transformers_output_capturing_installed'] for x in (hook0, hook1))
        if not c['lower_K_rephase']: out['status'] = 'ROPE_PARITY_FAIL'
        assert all(c.values()), ('SIDE_GATES', c)
        PAIR877.setdefault(world, {})[cond] = {'cond': cond, 'gH': gH, 'X3': X3, 'card': card, 'n_before': n_before, 'x3s': x3s,
                                               'body': body, 'A_ids': z['A_ids'], 't2_action': z['t2_action']}
        line877('SIDE', side, _j877.dumps({'card': card, 'C': [n_before, x3s], 'X3': int(X3.shape[0]), 'H': out['H']}, sort_keys=True))
        if cond == 'LIVE':
            run_world877(env, world)
    except Partial877 as exc:
        out['partial'] = str(exc); STATE877['worlds'].setdefault(world, {})['status'] = 'PARTIAL_INCONCLUSIVE'
        line877('PARTIAL', side, str(exc))
    except Exception as exc:
        out['error'] = '%s: %s' % (type(exc).__name__, str(exc)[:400]); out['traceback'] = traceback.format_exc()
        (ROOT864 / ('877_%s_t%d_traceback.txt' % (side, ctx['steps']))).write_text(out['traceback'], encoding='utf-8')
        line877('POINT_ERROR', side, 't=%d' % ctx['steps'], out['error'])
    finally:
        if ctx['steps'] == POST_STEP877 and side.endswith('LIVE'): PAIR877.pop(world, None)
        gc.collect(); env['release'](); out['seconds_t%d' % ctx['steps']] = round(time.perf_counter() - t0, 3)

def pub877(W):
    # JSON view of a world: recorded D-row tensors are working data, never written
    t = dict(W.get('total') or {}); t['targets'] = {c: {k: v for k, v in T.items() if k not in ('recB', 'recS', 'recM')}
                                                   for c, T in (t.get('targets') or {}).items()}
    return json.loads(json.dumps(dict(W, total=t), default=str))

def run_world877(env, world):
    M, L = PAIR877[world]['MISSING'], PAIR877[world]['LIVE']; t0 = time.perf_counter()
    seal = [prefix_seals865(env, x['gH']) for x in (M, L)]; wd = weights_digest877(env)
    W = STATE877['worlds'].setdefault(world, {}); W['role'] = 'discovery' if world == DISCOVERY877 else 'confirmation'
    W['cache_digest'] = {'MISSING_gH': seal[0], 'LIVE_gH': seal[1], 'weights': wd}
    try:
        tot = total877(env, world, M, L); W['total'] = tot; W['status'] = tot['status']
        json_write864('877_checkpoint_%s_total.json' % world, pub877(W))
        if tot['status'] == 'TOTAL_EFFECT':
            if world == DISCOVERY877:
                sc = scan877(env, tot, M, L); W['scan'] = sc; W['status'] = sc['status']
                if sc['frozen'] is not None and sc['status'] == 'LOCALIZED_CIRCUIT_CANDIDATE':
                    W['frozen_extras'] = frozen_extras877(env, tot, M, L, sc['frozen'])
                    manifest = {'pathway': sc['frozen'], 'rule': PREREG877['pass_rule'], 'prereg_sha256': PREREG_SHA877,
                                'executed_cell_git_blob': STATE877['source'].get('executed_cell_git_blob'),
                                'discovery_reads': tot['reads']}
                    manifest['sha256'] = sha256_bytes864(_j877.dumps(manifest, sort_keys=True, default=str).encode())
                    STATE877['frozen'] = manifest; json_write864('877_frozen_manifest.json', manifest)
                    line877('FROZEN', _j877.dumps(manifest, sort_keys=True, default=str))
            elif STATE877['frozen'] is not None:
                path = STATE877['frozen']['pathway']
                W['confirmation'] = test877(env, tot, M, L, path)
                W['frozen_extras'] = frozen_extras877(env, tot, M, L, path)
                W['status'] = 'CONFIRMED' if W['confirmation']['pass'] else 'NOT_CONFIRMED'
        W['canonical_unchanged'] = [prefix_seals865(env, x['gH']) for x in (M, L)] == seal and weights_digest877(env) == wd
        if not W['canonical_unchanged']: STATE877['blocks'].append('CANONICAL_STATE_CHANGED:' + world)
    finally:
        for T in (W.get('total') or {}).get('targets', {}).values():
            for k in ('recB', 'recS', 'recM'): T.pop(k, None)
        W['elapsed_s'] = round(time.perf_counter() - t0, 1); W['peak_gib'] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
        json_write864('877_checkpoint_%s.json' % world, pub877(W))
    line877('WORLD', world, W['status'], 'reads=%d' % W['total']['reads'], 'elapsed_s=%s' % W['elapsed_s'], 'peak_gib=%s' % W['peak_gib'])

xray_point870 = probe877

def verdict877():
    blocks = list(STATE877['blocks']); reps = {r.get('item'): r for r in STATE870['replays']}
    for side, s in STATE877['sides'].items():
        if s.get('error'): blocks.append('POINT_ERROR:' + side)
        if reps.get(side, {}).get('ok') is not True: blocks.append('REPLAY_NOT_EXACT:' + side)
    D, C = STATE877['worlds'].get(DISCOVERY877, {}), STATE877['worlds'].get(CONFIRM877, {})
    rope = any(s.get('status') == 'ROPE_PARITY_FAIL' for s in STATE877['sides'].values())
    if blocks: v = 'ROPE_PARITY_FAIL' if rope else 'TECHNICAL_BLOCK'
    elif D.get('status') in (None, 'PARTIAL_INCONCLUSIVE') or C.get('status') == 'PARTIAL_INCONCLUSIVE': v = 'PARTIAL_INCONCLUSIVE'
    elif D['status'] != 'LOCALIZED_CIRCUIT_CANDIDATE': v = D['status']
    elif C.get('status') == 'CONFIRMED': v = 'CONFIRMED_OUTCOME_TO_CAR_CIRCUIT_PILOT'
    else: v = 'LOCALIZED_CIRCUIT_CANDIDATE'
    STATE877['verdict'] = {'verdict': v, 'blocks': blocks, 'discovery': D.get('status'), 'confirmation': C.get('status', 'NOT_RUN'),
                           'limits': ['VALUE_NOT_IDENTIFIED', 'WRITABLE_LEARNING_NOT_TESTED', 'two real event pairs: pilot']}
    return STATE877['verdict']

def report877():
    words = ('ACQUIRE', 'BACKTRACK', 'REJECT', 'STOP', 'ACCEPT', 'ADVANCE')
    print('=' * 110)
    print('TEST877 NATIVE DECISION CIRCUIT X-RAY | GPU %s | cell %s | prereg %s | api %s' % (
        CC_GPU.get('name'), STATE877['source'].get('executed_cell_git_blob'), PREREG_SHA877[:16], _j877.dumps(STATE877['api'].get('transformers'))))
    for side in SIDES877:
        s = STATE877['sides'].get(side)
        print('  %s %s' % (side, 'NOT_REACHED' if not s else _j877.dumps({k: s.get(k) for k in ('card', 'C', 'X3_len', 'H', 'error', 'partial')}, default=str)))
    for w in (DISCOVERY877, CONFIRM877):
        W = STATE877['worlds'].get(w)
        if not W: print('WORLD %s NOT_RUN' % w); continue
        tot = W.get('total', {})
        print('WORLD %s (%s) status %s | C %s cards %s X3 %s tau_num %s reads %s' % (w, W.get('role'), W.get('status'), tot.get('C'),
              tot.get('cards'), tot.get('X3_len'), tot.get('tau_num'), tot.get('reads')))
        print('  gates %s | prefix_max_rel %s | elapsed_s %s peak_gib %s' % (_j877.dumps(tot.get('gates'), sort_keys=True),
              tot.get('prefix_max_rel', 0.0), W.get('elapsed_s'), W.get('peak_gib')))
        print('  cache digest %s' % _j877.dumps(W.get('cache_digest'), sort_keys=True, default=str)[:400])
        for cond, T in tot.get('targets', {}).items():
            for arm in ('NATIVE', 'BASE', 'SWAP', 'MASK', 'MASKED_DONOR'):
                a = T['arms'][arm]; print('  %-7s %-12s %-9s' % (cond, arm, a['action']) + ' '.join('%s=%.4f' % (x, a['p'][x]) for x in words))
            print('  %-7s |tau|first=%.4f seq=%.4f |nu|seq=%.4f detect=%s' % (cond, T['norms']['tau_first'], T['norms']['tau_seq'],
                  T['norms']['nu_seq'], T['detect']))
            for arm in ('BASE', 'SWAP', 'MASK'):
                print('  %-7s %-5s seq margins %s' % (cond, arm, ' '.join('%.3f' % x for x in T['m'][arm]['seq'])))
            print('  %-7s obs |swap-base| attn by block %s mlp by block %s' % (cond,
                  [round(sum(T['obs']['attn'][a:b]), 2) for a, b in BLOCKS877], [round(sum(T['obs']['mlp'][a:b]), 2) for a, b in BLOCKS877]))
        for lv in (W.get('scan') or {}).get('levels', []):
            for r in lv['rows']:
                print('  SCAN %-9s %-28s pass=%-5s %s' % (lv['level'], r['path']['label'], r['pass'], ' | '.join(
                    '%s rho=%.3f r=%.3f r_sham=%.3f rho_first=%.3f' % (k, e['seq']['rho'], e['seq']['r'], e['seq']['r_sham'], e['first']['rho'])
                    for k, e in r['dirs'].items())))
        if W.get('confirmation'):
            r = W['confirmation']; print('  CONFIRM %-28s pass=%s %s' % (r['path']['label'], r['pass'], ' | '.join(
                '%s rho=%.3f r=%.3f r_sham=%.3f' % (k, e['seq']['rho'], e['seq']['r'], e['seq']['r_sham']) for k, e in r['dirs'].items())))
        if W.get('frozen_extras'): print('  frozen extras %s' % _j877.dumps(W['frozen_extras'], sort_keys=True))
    if STATE877['frozen']: print('FROZEN MANIFEST', _j877.dumps(STATE877['frozen'], sort_keys=True, default=str))
    v = STATE877['verdict'] or {}
    print('TEST877 VERDICT %s | discovery %s | confirmation %s | blocks %s' % (v.get('verdict'), v.get('discovery'), v.get('confirmation'), v.get('blocks')))
    print('LIMITS: VALUE_NOT_IDENTIFIED; WRITABLE_LEARNING_NOT_TESTED; two real event pairs (pilot); patches are diagnostic, nothing written.')
    print('status %s | wall %.0f s | peak GPU %.2f GiB | GPU_EXECUTION_NOT_VERIFIED_BY_AUTHOR' % (STATE877['status'],
          time.perf_counter() - T_START877, torch.cuda.max_memory_allocated() / 2**30 if torch.cuda.is_available() else 0.0))
    print('=' * 110)

T_START877 = time.perf_counter()
try:
    STATE877['status'] = 'G0_SOURCE'; capture_source877()
    json_write864('877_prereg.json', {'prereg': PREREG877, 'sha256': PREREG_SHA877, 'before_model_load': True})
    line877('G0 PREREG', PREREG_SHA877)
    load_sources865(); source_audit877(); load877(); STATE877['ref873'] = ref873_874(RAW_SOURCES864['873.log'].decode())
    feasibility_audit864(); audit_contracts865(); load_spine864(); REFS877 = load_records870()
    for w in ('00', '01'):
        sha = {}
        for cnd in ('MISSING', 'LIVE'):
            ctl = [e['record'] for e in REFS877[('I867_%s_%s' % (w, cnd), ARM877)]['events'] if e['type'] == 'CONTROL']
            assert [x['action'] for x in ctl[:2]] == ['ADVANCE', 'ACQUIRE'], ('T2_PATH', w, cnd)
            sha[cnd] = ctl[PRE_STEP877 - 1]['state_sha256']
        assert sha['MISSING'] == sha['LIVE'], ('T2_STATE_NOT_SHARED', w)
    line877('G0 SOURCE PASS', _j877.dumps(STATE877['source'], sort_keys=True))
    STATE877['status'] = 'G1_PREFLIGHT'; assert CC_GPU_OK, ('GPU_PRECHECK', CC_GPU)
    env877, original_error877, original_trace877, reproduction877 = reproduce_pre859859()
    ORIGINAL_CONTROL_TRACE864 = original_trace877; TWO_JOB_VERIFICATION864 = verify_two_job859(env877, original_trace877)
    assert_hook_free859(env877, 'T877_before_native'); install_offline_evaluator859(env877)
    native877 = native_sequences860(env877); NATIVE_REGRESSION864 = native_regression864(env877, native877)
    verify_864_reference865(NATIVE_REGRESSION864); ANALYSIS864 = run_analysis863(env877, native877)
    assert len(STATE863['restores']) == 3 and all(r['exact'] for r in STATE863['restores'])
    digest877 = records_digest861(env877); null_seal877 = physical_seal863(env877, env877['MEMNULL841'])
    runtime_contracts865(env877); runtime_preflight865(env877, reproduction877); rearm_budget865(env877); make_slots866(env877)
    SLOTS867['PREV_EVALUATION'] = list(env877['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env877); resolve_append873(env877); api877(env877); WEIGHTS0_877 = weights_digest877(env877)
    assert_hook_free859(env877, 'T877_before_points')
    line877('G1 PREFLIGHT PASS', _j877.dumps(STATE877['api'], sort_keys=True), 'model_load_s=%.0f' % (time.perf_counter() - T_START877))
    STATE877['status'] = 'RUNNING'; T0_865 = time.perf_counter(); by_key877 = build_specs869(env877)
    for side in SIDES877:
        if side.startswith('I867_%s' % CONFIRM877) and STATE877['frozen'] is None:
            line877('SKIP', side, 'no frozen pathway from discovery: confirmation not run'); continue
        if STATE877['worlds'].get(DISCOVERY877, {}).get('status') == 'PARTIAL_INCONCLUSIVE': break
        rep = run_replay870(env877, {'id': side, 'item': side, 'arm': ARM877,
                                     'targets': {PRE_STEP877: 'T2_TIMELINE', POST_STEP877: 'T3_XRAY'}}, by_key877, REFS877)
        T2_KEEP877.pop(side, None)
        if not rep['ok']: STATE877['blocks'].append('REPLAY_NOT_EXACT:' + side)
    hook = hook_audit859(env877, 'T877_final')
    if records_digest861(env877) != digest877 or physical_seal863(env877, env877['MEMNULL841']) != null_seal877 or \
            hook['hook_count'] or hook['transformers_output_capturing_installed'] or weights_digest877(env877) != WEIGHTS0_877:
        STATE877['blocks'].append('POST_RUN_INTEGRITY')
    STATE877['status'] = 'COMPLETE'; verdict877()
except BaseException as exc:
    STATE877['error'] = '%s: %s' % (type(exc).__name__, exc); STATE877['traceback'] = traceback.format_exc()
    STATE877['status'] = 'FAILED_AT_' + str(STATE877['status'])
    STATE877['verdict'] = {'verdict': 'TECHNICAL_BLOCK', 'blocks': ['EXCEPTION: ' + STATE877['error'][:300]]}
    (ROOT864 / '877_traceback.txt').write_text(STATE877['traceback'], encoding='utf-8')
    print('TEST877 ERROR', STATE877['error'][:300], '| full traceback:', ROOT864 / '877_traceback.txt', file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        json_write864('877_result.json', json.loads(json.dumps(dict(STATE877, replays=STATE870['replays']), default=str, allow_nan=False)))
    except Exception as exc: print('RESULT_WRITE_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    try: report877()
    except Exception as exc: print('REPORT_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE877['suffix'], 'test870.py:suffix', 'exec'), globals())
