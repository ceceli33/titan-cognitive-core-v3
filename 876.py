# AKBASCORE SILICON HIPPOCAMPUS — TEST876 — NATIVE CAUSAL COUNTERFACTUAL POLICY UPDATE (NKPG)
# One Google Colab cell, one frozen Qwen2.5-72B-Instruct NF4 model, one A100-SXM4-80GB.
# The blob-locked TEST870/875 engine is loaded once. Canonical physical memory uses the unchanged native H append.
# Working branches use native inputs_embeds + DynamicCache + SDPA 4-D boolean masks (True = attend).
# No training, hooks, hidden-state export, external critic, textual memory replay, oracle action, or forced correction.
import ast as _a876, hashlib as _h876, json as _j876, urllib.request as _u876
ENGINE_URL876 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                 'e322ed8ed903f1a438738a3caada6744750cea42/test870.py')
ENGINE_BLOB876 = 'de3c8153266a95fbf9b86ce2e3149f48e16a7bbc'
# 875.py file at commit a07dc3e (pushed 17:32:11Z; the TEST875 A100 run started 17:36:05Z); 875.log at commit 6fc150a.
# 3966df9f... in 875.log is the blob of the Colab cell text captured from IPython history, not of the file: in
# TEST873/874/875 the captured cell blob differs from the file blob every time while the line count is equal.
TEST875_URL876 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                  'a07dc3ef83db46c5ebefe016a793dc39401904cb/875.py')
TEST875_LOG_URL876 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
                      '6fc150a2621d5def8bee25643848a254a17dbba5/875.log')
TEST875_BLOB876 = '23fd2ba8b967f447c748ce0e269ba8fc43660761'          # git blob of the committed 875.py file
TEST875_LOG_BLOB876 = '43488a95a5f68c6de2c06350148854995f121825'      # git blob of the committed 875.log
TEST875_CELL_BLOB876 = '3966df9f865911aa575ee1232055d09f64932bc5'     # executed cell blob, as recorded in 875.log
TEST875_PREREG876 = '308a97d93ce8adfb'                                 # PREREG875 sha256 prefix (file and run)
MARKER876 = 'AKBASCORE SILICON HIPPOCAMPUS — TEST876'

def blob876(raw):
    return _h876.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()

def fetch876(url):
    with _u876.urlopen(_u876.Request(url, headers={'User-Agent': 'AKBASCORE-TEST876'}), timeout=240) as r:
        return r.read()

def engine_parts876():
    raw = fetch876(ENGINE_URL876)
    assert blob876(raw) == ENGINE_BLOB876, ('ENGINE_BLOB_MISMATCH', blob876(raw))
    text = raw.decode('utf-8'); _a876.parse(text)
    a = text.index('# ===================== CELL CONSOLE CAPTURE — START')
    b = text.index('# ===================== CELL CONSOLE CAPTURE — XR870 follows')
    c = text.index('# ============================ SINGLE CELL EXECUTION ============================')
    d = text.index('# ===================== CELL CONSOLE CAPTURE — END')
    parts = {'prefix': text[a:b], 'body': text[b:c], 'suffix': text[d:]}
    renames = [('prefix', "'/content/XR870_HUCRE_CIKTISI_%s.txt'", "'/content/TEST876_HUCRE_CIKTISI_%s.txt'"),
               ('prefix', "'/content/drive/MyDrive/XR870_%s'", "'/content/drive/MyDrive/TEST876_%s'"),
               ('prefix', "'/content/XR870_CALIBRATION_*'", "'/content/TEST876_RUN_*'"),
               ('prefix', "('870.log', '870_events.jsonl')", "('876_engine.log', '876_events.jsonl')"),
               ('body', "('XR870_CALIBRATION_' + STAMP864)", "('TEST876_RUN_' + STAMP864)"),
               ('body', "ROOT864 / '870.log'", "ROOT864 / '876_engine.log'"),
               ('body', "ROOT864 / '870_events.jsonl'", "ROOT864 / '876_events.jsonl'"),
               ('suffix', "'/content/XR870_SONUC_%s.zip'", "'/content/TEST876_SONUC_%s.zip'")]
    for where, old, new in renames:
        assert parts[where].count(old) == 1, ('ENGINE_IO_RENAME', where, old)
        parts[where] = parts[where].replace(old, new)
    return parts, {'url': ENGINE_URL876, 'git_blob': blob876(raw), 'sha256': _h876.sha256(raw).hexdigest()}

try:
    ENGINE876, ENGINE_INFO876 = engine_parts876()
except BaseException as _exc876:      # console capture starts inside the engine prefix: keep a local record of this failure
    import time as _t876, traceback as _tb876
    _p876 = '/content/TEST876_PRE_ENGINE_ERROR_%s.txt' % _t876.strftime('%Y%m%dT%H%M%SZ', _t876.gmtime())
    try:
        with open(_p876, 'w', encoding='utf-8') as _f876: _f876.write(_tb876.format_exc())
    except OSError: _p876 = 'NOT_WRITTEN'
    print('TEST876 PRE-ENGINE ERROR (before console capture):', type(_exc876).__name__, _exc876, '| traceback:', _p876)
    raise
exec(compile(ENGINE876['prefix'], 'test870.py:prefix', 'exec'), globals())
exec(compile(ENGINE876['body'], 'test870.py:engine', 'exec'), globals())
print('TEST876 ENGINE', _j876.dumps(ENGINE_INFO876, sort_keys=True))
LOCKS864.update({'test870.py': ENGINE_BLOB876, 'Test870.log': 'e954d658752a59f66ceaeb1b8c7f52fd86a005dc',
                 '873.py': '2e44affa5e0dd462155fb265c331270fb8e7b7e1',
                 '873.log': '1c9eb9fca173003eaf45bc7726af13c2817324b7',
                 '874.py': '12172001ba3696ad91087a8b34d7995728259e47',
                 '874.log': '1229e3b70440e3887ccf1bd7e3bad51f900f5313',
                 '875.py': TEST875_BLOB876, '875.log': TEST875_LOG_BLOB876})
TEST870_MINUTES = TEST865_MINUTES = 110.0
WORLDS876 = ('01', '00')
SIDES876 = tuple('I867_%s_%s' % (w, c) for w in WORLDS876 for c in ('MISSING', 'LIVE'))
# Namespace aliases required by the unchanged AST-selected TEST874 loader/reference functions.
_a874, _j874, SIDES874 = _a876, _j876, SIDES876
ARM876, PRE_STEP876, POST_STEP876 = 'V_X', 2, 3
FUNCS873 = ('kv873', 'length873', 'forward873', 'car873', 'resolve_append873', 'append_card873', 'decide873',
            'probs873', 'same873', 'tv873')
CORRECTIVE876 = ('STOP', 'REJECT', 'BACKTRACK')
ARMS876 = ('H', 'REAL_Z', 'OUTCOME_ONLY_Z', 'Z_NULL', 'CF_MASK')
ROPE_TOL876, REPRO_TOL876, ROUND_TOL876 = 1e-2, 6e-4, 2e-2
SHIFT_MIN876, LIVE_TOL876, EFFECT_TV876 = .20, .10, .10
WORK_TOKENS876, EVAL_TOKENS876 = 12, 8
PREREG876 = {
    'engine': 'TEST875-H canonical physical state; native CAR six-action sequence logp',
    'sides_priority': SIDES876, 'arms': ARMS876,
    'flow': 'PREDICT -> OBSERVE -> ABDUCE -> RECONSTRUCT -> INTERVENE -> RE-PREDICT -> POLICY UPDATE',
    'prediction': 'sealed at t2 replay tap, before execute866; deterministic native greedy working rollout',
    'working_tokens': WORK_TOKENS876, 'evaluation_tokens': EVAL_TOKENS876,
    'physical_parity': 'working C rows are the canonical native-H C rows, bitwise, all 80 layers (no re-append)',
    'working_graph': '[ROOT_PRE][A][C canonical][PRED sealed at t2, t2 RoPE] then Z/R/CF/EVAL rollouts; logical = storage',
    'correction': {'argmax_required': True, 'corrective': CORRECTIVE876, 'mass_shift_reported': SHIFT_MIN876},
    'live': {'argmax': 'ACCEPT', 'max_probability_drop': LIVE_TOL876},
    'controls': {'OUTCOME_ONLY_Z': 'equal padded-prompt and rollout budget; semantic purity NOT guaranteed',
                 'Z_NULL': 'same REAL_Z graph; Z/R/CF invisible to policy evaluation and CAR',
                 'CF_MASK': 'same REAL_Z graph; CF invisible to policy evaluation and CAR'},
    'continuation': 'only REAL_Z model action; ACCEPT/STOP terminal; ADVANCE/BACKTRACK/ACQUIRE/REJECT use execute866 once',
    'early_stop': 'after world 01 pair on technical failure, no REAL_Z correction, loss of specificity, or LIVE damage',
    'not_evidence': ['corrective mass alone', 'MATCH text', 'Z/reconstruction text alone', 'CAR change alone',
                     'OUTCOME_ONLY_Z semantic purity', 'canonical-only policy equivalence after working-cache deletion']}
PREREG_SHA876 = sha256_bytes864(_j876.dumps(PREREG876, sort_keys=True).encode())
STATE876 = {'status': 'NOT_STARTED', 'engine': ENGINE_INFO876, 'prereg_sha256': PREREG_SHA876,
            'source': {}, 'source_audit': {}, 'ref873': {}, 'sides': {}, 'blocks': [], 'early_stop': None,
            'outcome': None, 'error': None}
T2_KEEP876, STASH876, PRED_SEALS876, REF_T2_ACTION876 = {}, {}, {}, {}
NAMES757 = ('P', 'CUT', 'NL', 'H', 'DEV', 'DTYPE', 'CHUNK', 'model', 'DirectCut3', 'ensure_room', 'pairs', 'rephase',
            'kv_digest', 'full_kv_seal', 'cache_build')

PRED_PROMPT876 = '''Native working prediction only. Before any new physical outcome is available, use the visible pre-action memory, task state, and selected action already committed in the cache. Predict the next goal-relevant transition: candidate, evidence, relation, pointer, memory sufficiency, and material uncertainty. Do not choose another action and do not assume an observed outcome.'''
REAL_Z_PROMPT876 = '''Native abduction only. Review the visible actual transition. Infer a compact pre-action latent condition that could explain how the selected action produced the actual outcome. Separate action contribution from independent environment conditions and uncertainty. Do not merely repeat the outcome and do not choose the next action.'''
OUTCOME_Z_PROMPT876 = '''Native outcome-only control. Review the visible actual transition. Describe only the observed outcome and immediately visible state. Do not infer a pre-action latent condition, alternative action, causal contribution, or future decision. Do not choose the next action.'''
RECON_PROMPT876 = '''Native reconstruction only. Using the visible root state, latent working hypothesis, and newly supplied selected action, reconstruct the expected goal-relevant transition. Actual outcome positions are not visible. Report consistency and unresolved uncertainty; do not choose an action.'''
CF_PROMPT876 = '''Native counterfactual prediction only. Using the visible root state and the same latent working hypothesis, apply the newly supplied alternative action and predict its goal-relevant transition. Actual selected-action and actual-outcome positions are not visible. Do not choose the next policy action.'''
EVAL_PROMPT876 = '''Native policy evaluation only. Use every visible working branch and the fresh physical state. Assess whether the actual transition is reconstructible, whether the same-latent alternative changes goal-relevant progress, and whether the evidence supports preservation, revision, or acquiring information. Do not emit or score any declared CAR action word.'''

def line876(*parts): short864('T876', *parts)
def clone876(kv): return [tuple(t.clone() for t in pair) for pair in kv]
def seg876(kv, a, b, layers=None):
    layers = range(len(kv)) if layers is None else layers
    return [(kv[i][0][:, :, a:b].clone(), kv[i][1][:, :, a:b].clone()) for i in layers]
def arm876(reading): return {'action': reading['action'], 'p': probs873(reading), 'reading': reading}
def corr876(p): return sum(float(p[w]) for w in CORRECTIVE876)
def dp876(a, b): return max(abs(float(a['normalized'][w]) - float(b['normalized'][w])) for w in a['normalized'])
def tv876(a, b): return .5 * sum(abs(a['p'][w] - b['p'][w]) for w in a['p'])
def digest876(env, kv, a=0, b=None):
    b = length873(env, kv) if b is None else int(b)
    h = _h876.sha256(); h.update(('ROWS:%d:%d' % (a, b)).encode())
    for i, (k, v) in enumerate(kv):
        kd = g757_876(env)['kv_digest']
        h.update(str(i).encode()); h.update(kd(k[:, :, a:b]).encode()); h.update(kd(v[:, :, a:b]).encode())
    return h.hexdigest()
def state_digest876(env, kv): return digest876(env, kv, 0, length873(env, kv))
def bool876(env, n, value=False): return torch.full((int(n),), bool(value), dtype=torch.bool, device=env['DEV'])
def ones876(env, n, value=True): return torch.full((int(n),), bool(value), dtype=torch.bool, device=env['DEV'])
def spans_visible876(env, n, spans, names):
    v = bool876(env, n)
    for name in names:
        a, b = spans[name]; v[a:b] = True
    return v
def visibility_report876(vis, spans):
    return {name: {'span': [int(a), int(b)], 'visible': int(vis[a:b].sum()), 'length': int(b - a)}
            for name, (a, b) in spans.items() if b <= int(vis.shape[0])}

def g757_876(env):
    fn = env['native_append_direct']; g = getattr(fn, '__wrapped__', fn).__globals__
    missing = [k for k in NAMES757 if k not in g]
    assert not missing and int(g['CUT']) == 3, ('NAMESPACE_757', missing)
    return g

def capture_source876():
    try:
        hist = [t for t in get_ipython().history_manager.input_hist_raw if MARKER876 in t and 'def probe876' in t]
        source, how = hist[-1], 'IPYTHON_CELL'
    except (NameError, IndexError):
        source = open(__file__, encoding='utf-8').read() if '__file__' in globals() else None; how = 'FILE_%RUN'
    assert source and MARKER876 in source, 'EXECUTED_876_SOURCE_NOT_CAPTURED'
    tree = _a876.parse(source)
    banned = {'register_forward_hook', 'register_forward_pre_hook', 'install_all_output_capturing_hooks',
              'output_hidden_states', 'output_attentions', 'backward', 'requires_grad_', 'LoRA', 'peft'}
    used = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for c in _a876.walk(tree) if isinstance(c, _a876.Call)}
    assert not (used & banned), ('FIREWALL876', sorted(used & banned))
    calls = [n for n in _a876.walk(tree) if isinstance(n, _a876.Call) and getattr(n.func, 'id', None) == 'reproduce_pre859859']
    assert len(calls) == 1, 'MODEL_LOADER_CALL_COUNT_NOT_ONE'
    for name, value in (('xray_point870', 'probe876'), ('control_step869', 'stash_control876')):
        rs = [n for n in tree.body if isinstance(n, _a876.Assign) and any(getattr(t, 'id', '') == name for t in n.targets)]
        assert len(rs) == 1 and getattr(rs[0].value, 'id', None) == value, ('FIREWALL876_REBIND', name)
    (ROOT864 / 'TEST876.py').write_text(source, encoding='utf-8')
    STATE876['source'] = {'how': how, 'sha256': sha256_bytes864(source.encode()), 'git_blob': git_blob864(source.encode()),
                          'lines': source.count('\n') + 1, 'firewall': 'PASS'}

def source_audit876():
    raw, log = fetch876(TEST875_URL876), fetch876(TEST875_LOG_URL876)
    assert blob876(raw) == TEST875_BLOB876, ('TEST875_BLOB_MISMATCH', blob876(raw))
    assert blob876(log) == TEST875_LOG_BLOB876, ('TEST875_LOG_BLOB_MISMATCH', blob876(log))
    text = raw.decode(); tree = _a876.parse(text)
    # the committed file must carry the same pre-registration that the A100 run printed (fail closed otherwise)
    want = {'WORLDS875', 'SIDES875', 'ARM875', 'CORRECTIVE875', 'ARMS875', 'ROPE_TOL875', 'SHIFT_MIN875', 'PREREG875'}
    nodes = [n for n in tree.body if isinstance(n, _a876.Assign) and any(
        ({t.id} if isinstance(t, _a876.Name) else {e.id for e in getattr(t, 'elts', []) if isinstance(e, _a876.Name)}) & want
        for t in n.targets)]
    ns875 = {}; exec(compile(_a876.fix_missing_locations(_a876.Module(nodes, [])), '875.py:prereg', 'exec'), ns875)
    prereg875 = _h876.sha256(_j876.dumps(ns875['PREREG875'], sort_keys=True).encode()).hexdigest()
    assert prereg875.startswith(TEST875_PREREG876), ('TEST875_PREREG_MISMATCH', prereg875[:16])
    run_line = [x for x in log.decode().splitlines() if x.startswith('TEST875 | GPU NVIDIA A100-SXM4-80GB | source ')]
    assert len(run_line) == 1 and (' source %s ' % TEST875_CELL_BLOB876) in run_line[0] and \
        ('| prereg %s' % TEST875_PREREG876) in run_line[0], ('TEST875_RUN_LINE', run_line)
    funcs = {n.name: n for n in tree.body if isinstance(n, _a876.FunctionDef)}
    assert 'append875' in funcs and 'mask875' in funcs and 'probe875' in funcs and 'step2_875' in funcs
    calls = {getattr(c.func, 'id', getattr(c.func, 'attr', None)) for n in funcs.values() for c in _a876.walk(n)
             if isinstance(c, _a876.Call)}
    assert {'native_append_direct', 'execute866', 'reading867', 'control_step869'} & calls
    logtext = log.decode()
    assert all(x in logtext for x in ('NVIDIA A100-SXM4-80GB', 'TEST875 OUTCOME WRITE_EFFECT_WITHOUT_CORRECTION',
                                      'status COMPLETE', 'BLOCKS []'))
    info = {'875.py': {'url': TEST875_URL876, 'git_blob': blob876(raw), 'sha256': _h876.sha256(raw).hexdigest(),
                       'functions': sorted(funcs), 'executed_cell_blob_in_log': TEST875_CELL_BLOB876,
                       'prereg_sha256_prefix_in_log': TEST875_PREREG876,
                       'file_vs_cell': 'cell bytes not published; equality of executed cell and file is not proven, '
                                       'only commit order, prereg hash and output format are consistent'},
            '875.log': {'url': TEST875_LOG_URL876, 'git_blob': blob876(log), 'sha256': _h876.sha256(log).hexdigest(),
                        'gpu_evidence': 'COMPLETE_WRITE_EFFECT_WITHOUT_CORRECTION'},
            'test870.py': ENGINE_INFO876,
            'preserved_symbols': ['reproduce_pre859859', 'native_append_direct', 'append_card873', 'execute866',
                                  'control_step869', 'car867/car873/car874', 'reading867', 'make_x851', 'mount865'],
            'new_symbols': ['forward_graph876', 'rollout_graph876', 'car_graph876',
                            'build_working876', 'policy_reading876', 'continue876']}
    STATE876['source_audit'] = info
    (ROOT864 / 'TEST876_source_manifest.json').write_text(_j876.dumps(info, indent=2, sort_keys=True), encoding='utf-8')
    (ROOT864 / 'TEST875_published.py').write_bytes(raw); (ROOT864 / 'TEST875_published.log').write_bytes(log)
    line876('GATE0 SOURCE_AUDIT PASS', _j876.dumps({'875_blob': blob876(raw), 'engine': ENGINE_BLOB876}))

def load876():
    names = ('load873_874', 'ref873_874', 'keep874', 'forward874', 'car874', 'rows874', 'decide874', 'rel874', 'card_range874')
    tree = _a876.parse(RAW_SOURCES864['874.py'].decode(), filename='874.py')
    nodes = [n for n in tree.body if isinstance(n, _a876.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    exec(compile(_a876.fix_missing_locations(_a876.Module(body=nodes, type_ignores=[])), '874.py:selected', 'exec'), globals())
    load873_874()

@torch.no_grad()
def forward_graph876(env, cache, Y, vis, pos0=None, last=1):
    assert Y.ndim == 2 and int(Y.shape[1]) == int(env['H']) and Y.device == env['DEV'] and Y.dtype == env['DTYPE']
    L, n0 = int(Y.shape[0]), int(cache.get_seq_length())
    assert int(vis.shape[0]) == n0 and vis.dtype == torch.bool and vis.device == env['DEV']
    pos0 = n0 if pos0 is None else int(pos0)
    assert n0 + L <= int(env['MAX_FUSED_TOKENS']) and pos0 + L <= int(env['MAX_FUSED_TOKENS'])
    allowed = torch.zeros((1, 1, L, n0 + L), dtype=torch.bool, device=env['DEV'])
    allowed[0, 0, :, :n0] = vis
    allowed[0, 0, :, n0:] = torch.tril(torch.ones((L, L), dtype=torch.bool, device=env['DEV']))
    assert bool(allowed.any(dim=-1).all()), 'FULLY_MASKED_QUERY'
    storage = torch.arange(n0, n0 + L, device=env['DEV'])
    logical = torch.arange(pos0, pos0 + L, device=env['DEV'])
    out = env['model'](inputs_embeds=Y.reshape(1, L, env['H']), past_key_values=cache,
                       attention_mask=allowed, position_ids=logical.unsqueeze(0), cache_position=storage,
                       use_cache=True, return_dict=True)
    logp = torch.log_softmax(out.logits[0, -last:].float(), dim=-1)
    del out, allowed
    assert int(cache.get_seq_length()) == n0 + L, 'GRAPH_CACHE_NOT_EXTENDED'
    return logp

@torch.no_grad()
def rollout_graph876(env, cache, prompt_ids, vis, max_tokens, action_ids=None):
    env['budget849']()
    start = int(cache.get_seq_length())
    prompt_ids = list(env['prompt_ids'](prompt_ids)) if isinstance(prompt_ids, str) else list(prompt_ids)
    pieces = []
    if action_ids is not None: pieces.append(env['embed841'](list(action_ids)))
    pieces.append(env['embed841'](prompt_ids))
    Y = torch.cat(pieces, dim=0); plen = int(Y.shape[0]); action_len = 0 if action_ids is None else len(action_ids)
    logp = forward_graph876(env, cache, Y, vis, last=1)[0]
    vis = torch.cat([vis, ones876(env, plen)]); toks = []
    for _ in range(int(max_tokens)):
        nid = int(torch.argmax(logp).item()); toks.append(nid)
        logp = forward_graph876(env, cache, env['embed841']([nid]), vis, last=1)[0]
        vis = torch.cat([vis, ones876(env, 1)])
    end = int(cache.get_seq_length())
    return {'span': (start, end), 'generated_span': (start + plen, end), 'action_span': (start, start + action_len),
            'prompt_len': len(prompt_ids), 'input_len': plen, 'tokens': toks,
            'text': env['tok'].decode(toks, skip_special_tokens=False), 'vis': vis}

@torch.no_grad()
def car_graph876(env, cache, X, vis):
    # Same ACTION_IDS867, first-token and cropped teacher-forced sequence-logp procedure; only visibility is graphed.
    env['budget849'](); L, n0 = int(X.shape[0]), int(cache.get_seq_length())
    assert int(vis.shape[0]) == n0 and n0 + L + max(len(ids) for _, ids in ACTION_IDS867) <= int(env['MAX_FUSED_TOKENS'])
    first = forward_graph876(env, cache, X, vis, last=1)[0]
    vis1 = torch.cat([vis, ones876(env, L)]); n1 = n0 + L; scores = []
    for word, ids in ACTION_IDS867:
        token_logps = [float(first[ids[0]])]
        if len(ids) > 1:
            m = len(ids) - 1
            lp = forward_graph876(env, cache, env['embed841'](ids[:-1]), vis1, last=m)
            cache.crop(-m); assert int(cache.get_seq_length()) == n1, 'CAR_GRAPH_CROP_LENGTH'
            token_logps += [float(lp[i, ids[i + 1]]) for i in range(m)]
            del lp
        scores.append({'word': word, 'ids': ids, 'token_logps': token_logps,
                       'sequence_logp': float(sum(token_logps)), 'hard_greedy_ids': []})
    top = torch.topk(first, 10)
    return reading867({'scores': scores, 'path': 'GRAPH_4D_CROP', 'fallback_reason': None,
                       'first_top10': {'ids': [int(i) for i in top.indices.tolist()]}, 'X_sha256': None})

def pad_prompts876(env, texts):
    rows = [list(env['prompt_ids'](t)) for t in texts]; width = max(map(len, rows))
    pad = env['tok'].pad_token_id
    if pad is None: pad = env['tok'].eos_token_id
    assert pad is not None and width > 0
    return [[int(pad)] * (width - len(row)) + row for row in rows]

def build_working876(env, z, card, z_prompt, rc_prompts, gH):
    # Working graph = canonical physical state gH [ROOT_PRE][A][C] (locked native H append: C never sees the
    # prediction) + the sealed pre-outcome prediction rows, moved behind C with their t2 RoPE positions kept.
    # Attention reads keys by baked RoPE and visibility, so the actual C is exactly the canonical one (bitwise).
    n_before, n_prea, pkv = int(z['n_before']), int(z['n_prea']), z['prediction_kv']
    pred_end, body = length873(env, pkv), int(env['entries'][card]['body_tokens']); c1 = n_before + body
    NL = len(gH); assert length873(env, gH) == c1 and len(pkv) == NL, 'WORKING_LAYOUT'
    assert all(torch.equal(pkv[i][j][:, :, :n_before], gH[i][j][:, :, :n_before]) for i in range(NL) for j in (0, 1)), \
        'PREDICTION_ROOT_NOT_CANONICAL_ROOT'
    work = [tuple(torch.cat([gH[i][j], pkv[i][j][:, :, n_before:]], dim=-2) for j in (0, 1)) for i in range(NL)]
    p1 = c1 + pred_end - n_before
    spans = {'ROOT_PRE': (0, n_prea), 'A': (n_prea, n_before), 'C': (n_before, c1), 'PRED': (c1, p1)}
    c_exact = all(torch.equal(work[i][j][:, :, n_before:c1], gH[i][j][:, :, n_before:c1]) for i in range(NL) for j in (0, 1))
    pred_exact = all(torch.equal(work[i][j][:, :, c1:p1], pkv[i][j][:, :, n_before:pred_end]) for i in range(NL) for j in (0, 1))
    parity = 0.0 if c_exact else max(rel874(seg876(gH, n_before, c1), seg876(work, n_before, c1)))
    assert c_exact and pred_exact, ('WORKING_PHYSICAL_PARITY', c_exact, pred_exact, parity)
    vis_actual = spans_visible876(env, p1, spans, ('ROOT_PRE', 'A', 'C'))       # Z: actual transition, no prediction
    cache = env['cache_build'](work); del work
    zr = rollout_graph876(env, cache, z_prompt, vis_actual, WORK_TOKENS876)
    spans['Z'] = zr['span']; vis_z = zr['vis']
    # R and CF receive only pre-action root + Z. Actual A/C, prediction, and the other branch are invisible.
    base_r = spans_visible876(env, int(cache.get_seq_length()), spans, ('ROOT_PRE', 'Z'))
    rr = rollout_graph876(env, cache, rc_prompts[0], base_r, WORK_TOKENS876, action_ids=z['a_star_ids'])
    spans['R'] = rr['span']
    base_cf = spans_visible876(env, int(cache.get_seq_length()), spans, ('ROOT_PRE', 'Z'))
    cf = rollout_graph876(env, cache, rc_prompts[1], base_cf, WORK_TOKENS876, action_ids=z['a_alt_ids'])
    spans['CF'] = cf['span']
    assert not bool(base_r[spans['A'][0]:spans['C'][1]].any()), 'RECONSTRUCTION_ACTUAL_LEAK'
    assert not bool(base_r[spans['PRED'][0]:spans['PRED'][1]].any()), 'RECONSTRUCTION_PREDICTION_LEAK'
    assert not bool(base_cf[spans['A'][0]:spans['C'][1]].any()), 'CF_ACTUAL_LEAK'
    assert not bool(base_cf[spans['PRED'][0]:spans['PRED'][1]].any()), 'CF_PREDICTION_LEAK'
    assert not bool(base_cf[spans['R'][0]:spans['R'][1]].any()), 'CF_RECONSTRUCTION_LEAK'
    reports = {'actual': visibility_report876(vis_actual, spans), 'Z': visibility_report876(vis_z, spans),
               'R_base': visibility_report876(base_r, spans), 'CF_base': visibility_report876(base_cf, spans)}
    basekv = kv873(env, cache)
    out = {'kv': basekv, 'spans': spans, 'reports': reports, 'physical_parity_max_rel': parity,
           'physical_lower_exact': c_exact, 'prediction_rows_exact': pred_exact,
           'storage_C': [n_before, c1], 'logical_C': [n_before, c1],
           'storage_PRED': [c1, p1], 'logical_PRED': [n_before, pred_end],
           'Z': {'text': zr['text'], 'tokens': zr['tokens'], 'digest': digest876(env, basekv, *spans['Z']),
                 'prompt_len': zr['prompt_len'], 'generated': len(zr['tokens'])},
           'R': {'text': rr['text'], 'tokens': rr['tokens'], 'digest': digest876(env, basekv, *spans['R'])},
           'CF': {'text': cf['text'], 'tokens': cf['tokens'], 'digest': digest876(env, basekv, *spans['CF'])}}
    del cache
    return out

def policy_reading876(env, base, X3, vis_base):
    cache = env['cache_build'](clone876(base['kv']))
    ev = rollout_graph876(env, cache, EVAL_PROMPT876, vis_base, EVAL_TOKENS876)
    reading = car_graph876(env, cache, X3, ev['vis'])
    out = {'arm': arm876(reading), 'evaluation': {'text': ev['text'], 'tokens': ev['tokens'], 'span': ev['span']},
           'visibility': visibility_report876(vis_base, base['spans'])}
    del cache
    return out

def stash_control876(env, ctx, candidate, pointer, feedback):
    out = _LOCKED_CONTROL_STEP876(env, ctx, candidate, pointer, feedback)
    if ctx['spec']['item'] in SIDES876 and ctx['steps'] + 1 == POST_STEP876:
        STASH876[ctx['spec']['item']] = {'candidate': candidate, 'control': out[0], 'state': out[2]}
    return out

def continue876(env, ctx, side, state, action, gH, X3, seg, m2_cards, card, pre, post):
    st = STASH876.pop(side, None); assert st is not None and st['state'] is state, 'STASH_NOT_T3_STATE'
    ctx2 = dict(ctx, M=list(ctx['M']), path=list(ctx['path']), events=list(ctx['events']),
                mount_records=list(ctx['mount_records']), own_states=list(ctx['own_states']), prev_state=state['own_state'],
                memx=clone876(ctx['memx']))
    effect = execute866(env, ctx2, action, st['candidate'], st['control'], state); row = ctx2['events'][-1]
    res = {'run': True, 'action': action, 'effect': effect, 'chosen': row.get('chosen'),
           'mounted_after': list(ctx2['M']), 'physical_executor': 'execute866'}
    cache = env['cache_build'](clone876(gH)); n0 = int(cache.get_seq_length())
    forward874(env, cache, X3, n0, None, 1)
    n3 = int(cache.get_seq_length()); forward874(env, cache, env['embed841'](dict(ACTION_IDS867)[action]), n3, None, 1)
    kv4 = kv873(env, cache); del cache
    if effect == 'MOUNTED':
        kv4, acquired0 = append_card873(env, kv4, row['chosen']); res['acquired_append'] = {'before': acquired0,
            'after': length873(env, kv4), 'card': row['chosen']}
    drop = [card_range874(env, row['chosen'], m2_cards, card, seg)] if effect == 'UNMOUNTED' else []
    res['read_mask'] = drop
    k = len(ctx2['path']); pointer = None if k == 0 else ctx2['path'][-1]['rows']
    h4, kind = hop865(env, ctx2['memx'], ctx2['spec']['qid'], k, pointer); res['hop4'] = h4['text']
    if kind == 'EMPTY_OUTPUT': res['end'] = 'NATIVE_EMPTY_OUTPUT'
    else:
        feedback, _ = feedback869(env, ctx2)
        control4, record4, state4 = _LOCKED_CONTROL_STEP876(env, ctx2, h4, pointer, feedback)
        if control4 is None: res['end'] = 'NATIVE_EMPTY_STATE'
        else:
            names = slot_names869(env, list(state4['segments']))
            X4, _ = env['make_x851'](pre, [s for s, n in zip(state4['segments'], names) if n not in ('FV', 'FK')], post)
            r4, _, _, _ = decide874(env, kv4, X4, drop)
            res['second_CAR_graph_timeline'] = arm876(r4); res['second_CAR_engine'] = arm876(record4['reading'])
            res['end'] = 'SECOND_NATIVE_CAR_COMPLETE'
            res['second_CAR_scope'] = ('canonical physical timeline [H][X3][A3](+new C)[X4]; working Z/R/CF branches are '
                                       'not carried: recursion depth 1 physical step, not a recursive NKPG policy update')
    del kv4, ctx2['memx']
    return res

def t2_probe876(env, ctx, record, state, out):
    side = ctx['spec']['item']; q = env['QTEXT841'][ctx['spec']['qid']]
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
    ids = dict(ACTION_IDS867); a_star = record['action']
    assert a_star == REF_T2_ACTION876[side], ('T2_ACTION_NOT_THE_LOCKED_RECORD', a_star)   # replay invariant only
    ranked = sorted(record['reading']['scores'], key=lambda s: -float(s['sequence_logp']))
    assert ranked[0]['word'] == a_star and len(ranked) > 1
    a_alt = ranked[1]['word']; assert a_alt != a_star
    segs2 = list(state['segments']); X2, _ = env['make_x851'](pre, segs2, post)
    L2, lp = int(X2.shape[0]), len(pre)
    assert lp + sum(len(x) + (0 if r is None else int(r.shape[0])) for x, r in segs2) + len(post) == L2, 'X2_LAYOUT'
    m2 = clone876(ctx['memx']); n2 = length873(env, m2)
    cache = env['cache_build'](m2); out['checks']['t2_CAR_equals_record'] = same873(car873(env, cache, X2), record['reading'])
    assert int(cache.get_seq_length()) == n2 + L2
    own = env['cache_build'](list(kv873(env, cache))); del cache
    forward873(env, own, env['embed841'](ids[a_star]), n2 + L2)
    own_kv = kv873(env, own); del own
    n_prea, n_before = n2 + L2, length873(env, own_kv)
    work = clone876(own_kv); cache = env['cache_build'](work); vis = ones876(env, n_before)
    pr = rollout_graph876(env, cache, PRED_PROMPT876, vis, WORK_TOKENS876)
    pred_kv = kv873(env, cache); del cache
    pred_span = (n_before, length873(env, pred_kv))
    seal = {'input_state_digest': state_digest876(env, own_kv), 'a_star': a_star, 'a_alt': a_alt,
            'a_star_ids': ids[a_star], 'a_alt_ids': ids[a_alt], 'token_ids': pr['tokens'],
            'working_length': int(pred_span[1] - pred_span[0]), 'storage_span': list(pred_span),
            'logical_span': list(pred_span), 'representation_digest': digest876(env, pred_kv, *pred_span),
            'sequence': 'SEALED_BEFORE_EXECUTE866', 'text': pr['text']}
    world, cond = side.split('_')[1], side.split('_')[2]; other = 'LIVE' if cond == 'MISSING' else 'MISSING'
    peer = PRED_SEALS876.get('I867_%s_%s' % (world, other)); parity = {'checked': False}
    if peer is not None:
        equal_inputs = peer['input_state_digest'] == seal['input_state_digest'] and peer['a_star'] == seal['a_star'] and \
                       peer['a_alt'] == seal['a_alt'] and peer['a_star_ids'] == seal['a_star_ids']
        parity = {'checked': True, 'equal_inputs': equal_inputs,
                  'equal_tokens': peer['token_ids'] == seal['token_ids'],
                  'equal_representation': peer['representation_digest'] == seal['representation_digest']}
        if equal_inputs: assert parity['equal_tokens'] and parity['equal_representation'], ('PAIRED_PREDICTION_MISMATCH', parity)
    PRED_SEALS876[side] = seal
    out['initial_CAR'] = arm876(record['reading']); out['initial_ranking'] = [s['word'] for s in ranked]
    out['A_star'], out['A_alt'], out['prediction_seal'] = a_star, a_alt, seal
    out['paired_prediction'] = parity
    out['lengths'].update({'M_t2': n2, 'X2': L2, 'X2_task_prompt': lp, 'X2_state': L2 - lp,
                           'A': len(ids[a_star]), 'pre_action': n_prea, 'A_committed': n_before,
                           'prediction': pred_span[1]})
    T2_KEEP876[side] = {'own': own_kv, 'prediction_kv': pred_kv, 'n2': n2, 'L2': L2, 'lp': lp,
                        'n_prea': n_prea, 'n_before': n_before, 'm2_cards': list(ctx['M']), 'seal': seal,
                        'a_star': a_star, 'a_alt': a_alt, 'a_star_ids': ids[a_star], 'a_alt_ids': ids[a_alt]}
    assert out['checks']['t2_CAR_equals_record']
    del m2

def probe876(env, ctx, record, state, label):
    side = ctx['spec']['item']; q = env['QTEXT841'][ctx['spec']['qid']]
    pre = list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))); post = env['REVIEW_SUFFIX851']
    out = STATE876['sides'].setdefault(side, {'checks': {}, 'arms': {}, 'lengths': {}, 'branches': {}, 'error': None})
    c, t0 = out['checks'], time.perf_counter()
    try:
        if ctx['steps'] == PRE_STEP876:
            t2_probe876(env, ctx, record, state, out); return
        vram0 = vram_begin870(); z = T2_KEEP876.pop(side); n2, L2, lp = z['n2'], z['L2'], z['lp']
        n_before, n_prea = z['n_before'], z['n_prea']; memx = ctx['memx']
        eff = [e for e in ctx['events'] if e.get('type') == 'EFFECT'][-1]; card = eff.get('chosen')
        body = int(env['entries'][card]['body_tokens']); n3 = int(memx[0][0].shape[-2]); out['card'] = card
        assert digest876(env, z['prediction_kv'], n_before, length873(env, z['prediction_kv'])) == \
               z['seal']['representation_digest'], 'PREDICTION_CHANGED_BEFORE_ACTUAL'
        c['card_mounted'] = eff.get('effect') == 'MOUNTED' and list(ctx['M'])[-1] == card
        names = slot_names869(env, list(state['segments']))
        segs3 = [s for s, n in zip(state['segments'], names) if n not in ('FV', 'FK')]
        X3, _ = env['make_x851'](pre, segs3, post); L3 = int(X3.shape[0])
        assert lp + sum(len(x) + (0 if r is None else int(r.shape[0])) for x, r in segs3) + len(post) == L3, 'X3_LAYOUT'
        seal0 = prefix_seals865(env, memx); hook0 = assert_hook_free859(env, 'T876_before_' + side)
        gH, logical_c0 = append_card873(env, z['own'], card); assert logical_c0 == n_before
        rH, _, _, _ = decide874(env, gH, X3, []); out['arms']['H'] = arm876(rH)
        logical_c1 = n_before + body; x3s = logical_c1
        seg = {'X2_state': [n2 + lp, n2 + L2], 'A': [n_prea, n_before], 'C': [n_before, logical_c1],
               'X3_state': [x3s + lp, x3s + L3]}; out['segments'] = seg
        c['segments'] = n_before == n2 + L2 + len(z['a_star_ids']) and length873(env, gH) == logical_c1
        cut, rephase = APPEND873['CUT'], APPEND873['rephase']
        c['lower_V_bitwise'] = all(torch.equal(gH[i][1][:, :, n_before:], memx[i][1][:, :, n3 - body:]) for i in range(cut + 1))
        rope = max(float(torch.linalg.vector_norm(rephase(gH[i][0][:, :, n_before:], torch.arange(n_before, logical_c1, device=env['DEV']),
            torch.arange(n3 - body, n3, device=env['DEV'])).float() - memx[i][0][:, :, n3 - body:].float())) /
            max(float(torch.linalg.vector_norm(memx[i][0][:, :, n3 - body:].float())), 1e-30) for i in range(cut + 1))
        c['lower_K_rephase'] = rope <= ROPE_TOL876
        ref = STATE876['ref873'][side]['T1']; c['H_reproduces_873'] = rH['action'] == ref['action'] and all(
            abs(out['arms']['H']['p'][w] - ref['p'][w]) <= REPRO_TOL876 for w in ref['p'])
        assert c['card_mounted'] and c['H_reproduces_873'] and c['lower_V_bitwise'] and c['lower_K_rephase'] and c['segments'], c
        zpair = pad_prompts876(env, [REAL_Z_PROMPT876, OUTCOME_Z_PROMPT876])
        rcpair = pad_prompts876(env, [RECON_PROMPT876, CF_PROMPT876])
        bases = {}
        for kind, zp in (('REAL_Z', zpair[0]), ('OUTCOME_ONLY_Z', zpair[1])):
            bases[kind] = build_working876(env, z, card, zp, rcpair, gH)
            out['branches'][kind] = {k: v for k, v in bases[kind].items() if k != 'kv'}
        # Policy evaluation is rerun for each visibility condition, keeping compute and X3 fixed.
        full_real = ones876(env, length873(env, bases['REAL_Z']['kv']))
        full_control = ones876(env, length873(env, bases['OUTCOME_ONLY_Z']['kv']))
        znull = spans_visible876(env, length873(env, bases['REAL_Z']['kv']), bases['REAL_Z']['spans'],
                                 ('ROOT_PRE', 'A', 'PRED', 'C'))
        cfmask = spans_visible876(env, length873(env, bases['REAL_Z']['kv']), bases['REAL_Z']['spans'],
                                  ('ROOT_PRE', 'A', 'PRED', 'C', 'Z', 'R'))
        policies = {'REAL_Z': policy_reading876(env, bases['REAL_Z'], X3, full_real),
                    'OUTCOME_ONLY_Z': policy_reading876(env, bases['OUTCOME_ONLY_Z'], X3, full_control),
                    'Z_NULL': policy_reading876(env, bases['REAL_Z'], X3, znull),
                    'CF_MASK': policy_reading876(env, bases['REAL_Z'], X3, cfmask)}
        for name, value in policies.items(): out['arms'][name] = value['arm']
        out['policy_evaluation'] = {name: value['evaluation'] for name, value in policies.items()}
        out['policy_visibility'] = {name: value['visibility'] for name, value in policies.items()}
        out['control_note'] = 'OUTCOME_ONLY_Z has equal padded prompt/rollout budget; outcome-only semantic purity is not guaranteed.'
        c['branch_masks'] = all(v['reports'][b][span]['visible'] == 0 for v in out['branches'].values()
                                for b in ('R_base', 'CF_base') for span in ('A', 'C', 'PRED'))     # stored under 'reports'
        c['physical_parity'] = all(v['physical_lower_exact'] and v['prediction_rows_exact'] and
                                   v['physical_parity_max_rel'] == 0.0 for v in out['branches'].values())
        c['memory_seal'] = prefix_seals865(env, memx) == seal0
        real = out['arms']['REAL_Z']; miss = side.endswith('MISSING')
        out['corrective_mass'] = {name: corr876(a['p']) for name, a in out['arms'].items()}
        out['corrective_shift_vs_H'] = corr876(real['p']) - corr876(out['arms']['H']['p'])
        out['REAL_corrective'] = real['action'] in CORRECTIVE876
        out['LIVE_ACCEPT_kept'] = True if miss else real['action'] == 'ACCEPT' and \
                                  real['p']['ACCEPT'] >= out['arms']['H']['p']['ACCEPT'] - LIVE_TOL876
        out['control_specificity'] = {'OUTCOME_argmax_differs': out['arms']['OUTCOME_ONLY_Z']['action'] != real['action'],
            'Z_NULL_argmax_differs': out['arms']['Z_NULL']['action'] != real['action'],
            'CF_MASK_argmax_differs': out['arms']['CF_MASK']['action'] != real['action'],
            'OUTCOME_TV': tv876(out['arms']['OUTCOME_ONLY_Z'], real),
            'Z_NULL_TV': tv876(out['arms']['Z_NULL'], real),
            'CF_MASK_TV': tv876(out['arms']['CF_MASK'], real)}
        assert c['branch_masks'] and c['physical_parity'] and c['memory_seal'], ('TECHNICAL_BEFORE_CONTINUATION', c)
        out['step2'] = {'run': False, 'reason': 'No physical continuation for terminal/unchanged policy action'}
        if real['action'] in ('ACCEPT', 'STOP', 'INVALID'):
            out['step2'] = {'run': False, 'reason': 'NATIVE_TERMINAL_' + real['action'], 'terminal': True}
        else:   # PREREG876: ADVANCE/BACKTRACK/ACQUIRE/REJECT -> execute866 once (the model's own word, never forced)
            try:
                out['step2'] = continue876(env, ctx, side, state, real['action'], gH, X3, seg,
                                           z['m2_cards'], card, pre, post)
            except Exception as exc:
                out['step2'] = {'run': True, 'error': '%s: %s' % (type(exc).__name__, str(exc)[:400]),
                                'traceback': traceback.format_exc()}
                (ROOT864 / ('876_%s_continuation_traceback.txt' % side)).write_text(traceback.format_exc(), encoding='utf-8')
        STASH876.pop(side, None); hook1 = assert_hook_free859(env, 'T876_after_' + side)
        c['hook_free'] = not any(x['hook_count'] or x['transformers_output_capturing_installed'] for x in (hook0, hook1))
        assert c['hook_free'], c
        out['vram'] = vram_end870(vram0)
        del bases, policies, gH, z
    except Exception as exc:
        out['error'] = '%s: %s' % (type(exc).__name__, str(exc)[:500]); out['traceback'] = traceback.format_exc()
        (ROOT864 / ('876_%s_t%d_traceback.txt' % (side, ctx['steps']))).write_text(out['traceback'], encoding='utf-8')
        line876('POINT_ERROR', side, 't=%d' % ctx['steps'], out['error'])
    finally:
        gc.collect(); env['release'](); out['seconds_t%d' % ctx['steps']] = round(time.perf_counter() - t0, 3)
    line876('POINT', side, _j876.dumps(c, sort_keys=True, default=str), '' if not out['error'] else out['error'])

xray_point870 = probe876
_LOCKED_CONTROL_STEP876 = control_step869
control_step869 = stash_control876

def side_behavior876(side):
    s = STATE876['sides'].get(side)
    if not s or s.get('error') or 'REAL_Z' not in s.get('arms', {}): return {'technical_ok': False, 'corrective': False}
    real, h = s['arms']['REAL_Z'], s['arms']['H']
    technical = all(s['checks'].get(k) for k in ('card_mounted', 'segments', 'lower_V_bitwise', 'lower_K_rephase',
                    'H_reproduces_873', 'branch_masks', 'physical_parity', 'memory_seal', 'hook_free'))
    missing = side.endswith('MISSING')
    corrective = real['action'] in CORRECTIVE876 if missing else False
    live = True if missing else real['action'] == 'ACCEPT' and real['p']['ACCEPT'] >= h['p']['ACCEPT'] - LIVE_TOL876
    specificity = (s['arms']['OUTCOME_ONLY_Z']['action'] != real['action'] or
                   tv876(s['arms']['OUTCOME_ONLY_Z'], real) >= EFFECT_TV876) and \
                  (s['arms']['Z_NULL']['action'] != real['action'] or
                   tv876(s['arms']['Z_NULL'], real) >= EFFECT_TV876) and \
                  (s['arms']['CF_MASK']['action'] != real['action'] or tv876(s['arms']['CF_MASK'], real) >= EFFECT_TV876)
    continuation = s.get('step2', {})
    recursion_ok = True
    if corrective and real['action'] != 'STOP':
        recursion_ok = continuation.get('run') is True and continuation.get('end') == 'SECOND_NATIVE_CAR_COMPLETE' and \
                       not continuation.get('error')
    return {'technical_ok': technical, 'corrective': corrective, 'live_preserved': live, 'specific': specificity,
            'recursive_ok': recursion_ok, 'real_action': real['action'], 'mass_shift': s.get('corrective_shift_vs_H')}

def outcome876():
    blocks = list(STATE876['blocks']); rows = {side: side_behavior876(side) for side in SIDES876 if side in STATE876['sides']}
    reps = {r.get('item'): r for r in STATE870['replays']}
    for side, s in STATE876['sides'].items():
        if reps.get(side, {}).get('ok') is not True: blocks.append('REPLAY_NOT_EXACT:' + side)
        if s.get('error'): blocks.append('POINT_ERROR:' + side)
    technical = any(not r['technical_ok'] for r in rows.values()) or bool(blocks)
    if technical: outcome = 'TECHNICAL_BLOCK'
    elif not rows: outcome = 'TECHNICAL_BLOCK'
    else:
        missing = [r for side, r in rows.items() if side.endswith('MISSING')]
        live = [r for side, r in rows.items() if side.endswith('LIVE')]
        if not all(r['corrective'] for r in missing): outcome = 'NO_NKPG_CORRECTION'
        elif not all(r['live_preserved'] for r in live): outcome = 'LIVE_PRESERVATION_FAILURE'
        elif not all(r['specific'] for r in missing): outcome = 'NONSPECIFIC_WORKING_STATE_EFFECT'
        elif not all(r['recursive_ok'] for r in missing): outcome = 'CORRECTION_WITHOUT_COMPLETE_PHYSICAL_RECURSION'
        elif STATE876['early_stop']: outcome = 'NKPG_CANDIDATE_EARLY_STOP'
        else: outcome = 'NKPG_CAUSAL_CORRECTION_CANDIDATE'
    res = {'outcome': outcome, 'blocks': blocks, 'sides': rows, 'early_stop': STATE876['early_stop'],
           'claim_limit': 'Candidate only: native counterfactual specificity on executed panels; not general self-attribution.'}
    STATE876['outcome'] = res; return res

def architecture_audit876(env):
    cfg = env['model'].config
    vals = {'layers': int(cfg.num_hidden_layers), 'hidden': int(cfg.hidden_size),
            'query_heads': int(cfg.num_attention_heads), 'kv_heads': int(cfg.num_key_value_heads)}
    assert vals == {'layers': 80, 'hidden': 8192, 'query_heads': 64, 'kv_heads': 8}, vals
    assert vals['hidden'] // vals['query_heads'] == 128 and env['DTYPE'] == torch.bfloat16
    kv_dtypes = {t.dtype for pair in env['MEMNULL841'] for t in pair}
    assert kv_dtypes == {torch.bfloat16}, ('KV_NOT_BF16', sorted(map(str, kv_dtypes)))
    qc = getattr(cfg, 'quantization_config', None) or getattr(env['model'], 'quantization_config', None)
    assert qc is not None
    get = lambda k, default=None: qc.get(k, default) if isinstance(qc, dict) else getattr(qc, k, default)
    assert get('load_in_4bit', True) and get('bnb_4bit_quant_type') == 'nf4', ('NF4_CONFIG', qc)
    assert not any(p.requires_grad for p in env['model'].parameters())
    STATE876['architecture'] = dict(vals, head_dim=128, activation=str(env['DTYPE']), kv_dtype=str(torch.bfloat16),
                                    nf4=True, attn=getattr(cfg, '_attn_implementation', None))
    line876('MODEL ARCHITECTURE NF4/BF16 PASS', STATE876['architecture'])

def report876():
    words = ('ACQUIRE', 'BACKTRACK', 'REJECT', 'STOP', 'ACCEPT', 'ADVANCE')
    print('=' * 110); print('TEST876 | GPU', CC_GPU.get('name'), '| source', STATE876['source'].get('git_blob'),
                            '| prereg', PREREG_SHA876[:16], '| early_stop', STATE876['early_stop'])
    for side in SIDES876:
        s = STATE876['sides'].get(side)
        if not s: print(side, 'NOT_REACHED'); continue
        print('\nWORLD/CONDITION', side, 'card', s.get('card'), 'root/prediction', (s.get('prediction_seal') or {}).get('input_state_digest'))
        print('  lengths', _j876.dumps(s.get('lengths')), 'A_star', s.get('A_star'), 'A_alt', s.get('A_alt'))
        print('  initial', _j876.dumps((s.get('initial_CAR') or {}).get('p'), sort_keys=True), 'ranking', s.get('initial_ranking'))
        print('  prediction', _j876.dumps(s.get('prediction_seal'), default=str)[:1800])
        print('  paired_prediction', _j876.dumps(s.get('paired_prediction'), sort_keys=True))
        for name in ARMS876:
            if name in s['arms']:
                a = s['arms'][name]
                print('  %-15s %-9s' % (name, a['action']), ' '.join('%s=%.4f' % (w, a['p'][w]) for w in words),
                      'corr=%.4f' % corr876(a['p']))
        for kind, b in s.get('branches', {}).items():
            print('  BRANCH', kind, 'physical_parity', b.get('physical_parity_max_rel'), 'lower_exact', b.get('physical_lower_exact'),
                  'storage_C', b.get('storage_C'), 'logical_C', b.get('logical_C'))
            print('    Z', _j876.dumps(b.get('Z'), default=str)[:1200])
            print('    R', _j876.dumps(b.get('R'), default=str)[:900])
            print('    CF', _j876.dumps(b.get('CF'), default=str)[:900])
            print('    masks', _j876.dumps(b.get('reports'), default=str)[:1800])
        print('  policy_eval', _j876.dumps(s.get('policy_evaluation'), default=str)[:1600])
        print('  corrective_shift', s.get('corrective_shift_vs_H'), 'REAL_corrective', s.get('REAL_corrective'),
              'LIVE_ACCEPT_kept', s.get('LIVE_ACCEPT_kept'), 'specificity', _j876.dumps(s.get('control_specificity')))
        print('  continuation', _j876.dumps(s.get('step2'), default=str)[:2200])
        print('  checks', _j876.dumps(s.get('checks'), sort_keys=True), 'seconds', s.get('seconds_t3'),
              'peak_GiB', (s.get('vram') or {}).get('peak_allocated_gib'), 'ERROR', s.get('error'))
    o = STATE876['outcome'] or {}; print('\nTEST876 OUTCOME', _j876.dumps(o, sort_keys=True, default=str))
    print('CONTROL LIMIT: OUTCOME_ONLY_Z semantic purity is not guaranteed; corrective mass and native text alone are not causal evidence.')
    print('GPU_EXECUTION_NOT_VERIFIED_BY_AUTHOR (K3.1 Pro; Claude review). Static source/CPU checks are not A100 validation.')
    print('status', STATE876['status'], '| wall %.0fs' % (time.perf_counter() - T_START876),
          '| peak GPU %.2f GiB' % (max(STATE870['costs'].get('session_peak_allocated_bytes', 0),
          torch.cuda.max_memory_allocated() if torch.cuda.is_available() else 0) / 2**30))

T_START876 = time.perf_counter()
try:
    STATE876['status'] = 'GATE0'; capture_source876(); source_audit876()
    json_write864('TEST876_prereg.json', {'prereg': PREREG876, 'sha256': PREREG_SHA876, 'before_model_load': True})
    load_sources865(); load876(); STATE876['ref873'] = ref873_874(RAW_SOURCES864['873.log'].decode())
    for name, needles in (('Test870.log', ('XR870 CALIBRATION CALIBRATION_PASS', 'NVIDIA A100')),
                          ('873.log', ('TEST873 OUTCOME', 'status COMPLETE', 'NVIDIA A100')),
                          ('874.log', ('TEST874 OUTCOME', 'status COMPLETE', 'NVIDIA A100', 'NUMERICAL_ORDER_DETERMINISTIC'))):
        assert all(x in RAW_SOURCES864[name].decode() for x in needles), ('LOCKED_LOG_NOT_COMPLETE', name)
    feasibility_audit864(); audit_contracts865(); load_spine864(); REFS876 = load_records870()
    for w in WORLDS876:
        sha = {}
        for cnd in ('MISSING', 'LIVE'):
            ctl = [e['record'] for e in REFS876[('I867_%s_%s' % (w, cnd), ARM876)]['events'] if e['type'] == 'CONTROL']
            assert [x['action'] for x in ctl[:2]] == ['ADVANCE', 'ACQUIRE']; sha[cnd] = ctl[PRE_STEP876 - 1]['state_sha256']
            REF_T2_ACTION876['I867_%s_%s' % (w, cnd)] = ctl[PRE_STEP876 - 1]['action']
        if sha['MISSING'] != sha['LIVE']: line876('PAIRED_INPUT_DIFFERENCE', w, sha)
    STATE876['status'] = 'GATE1'; assert CC_GPU_OK, ('GPU_PRECHECK', CC_GPU)
    env876, original_error876, original_trace876, reproduction876 = reproduce_pre859859()
    architecture_audit876(env876)
    ORIGINAL_CONTROL_TRACE864 = original_trace876; TWO_JOB_VERIFICATION864 = verify_two_job859(env876, original_trace876)
    assert_hook_free859(env876, 'T876_before_native'); install_offline_evaluator859(env876)
    native876 = native_sequences860(env876); NATIVE_REGRESSION864 = native_regression864(env876, native876)
    verify_864_reference865(NATIVE_REGRESSION864); ANALYSIS864 = run_analysis863(env876, native876)
    assert len(STATE863['restores']) == 3 and all(r['exact'] for r in STATE863['restores'])
    digest876_records = records_digest861(env876); null_seal876 = physical_seal863(env876, env876['MEMNULL841'])
    runtime_contracts865(env876); runtime_preflight865(env876, reproduction876); rearm_budget865(env876); make_slots866(env876)
    SLOTS867['PREV_EVALUATION'] = list(env876['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)
    action_ids867(env876); resolve_append873(env876); g757_876(env876)
    assert getattr(env876['model'].config, '_attn_implementation', None) == 'sdpa'
    assert_hook_free859(env876, 'T876_before_points'); STATE876['status'] = 'RUNNING'; T0_865 = time.perf_counter()
    by_key876 = build_specs869(env876)
    for world in WORLDS876:
        for cnd in ('MISSING', 'LIVE'):
            side = 'I867_%s_%s' % (world, cnd)
            rep = run_replay870(env876, {'id': side, 'item': side, 'arm': ARM876,
                'targets': {PRE_STEP876: 'T2_PREDICTION_SEAL', POST_STEP876: 'T3_NKPG'}}, by_key876, REFS876)
            T2_KEEP876.pop(side, None); STASH876.pop(side, None)
            if not rep['ok']: STATE876['blocks'].append('REPLAY_NOT_EXACT:' + side)
            if STATE876['sides'].get(side, {}).get('error'):
                STATE876['early_stop'] = 'TECHNICAL_POINT_ERROR:' + side; break
        behavior = {side: side_behavior876(side) for side in SIDES876 if side.startswith('I867_%s_' % world)}
        m = behavior.get('I867_%s_MISSING' % world, {}); l = behavior.get('I867_%s_LIVE' % world, {})
        if STATE876['early_stop'] is None:
            if not m.get('technical_ok') or not l.get('technical_ok'): STATE876['early_stop'] = 'TECHNICAL_GATE:' + world
            elif not m.get('corrective'): STATE876['early_stop'] = 'NO_REAL_Z_CORRECTION:' + world
            elif not m.get('specific'): STATE876['early_stop'] = 'NONSPECIFIC_CONTROL:' + world
            elif not l.get('live_preserved'): STATE876['early_stop'] = 'LIVE_PRESERVATION:' + world
            elif not m.get('recursive_ok'): STATE876['early_stop'] = 'PHYSICAL_RECURSION:' + world
        if STATE876['early_stop'] is not None: break
    hook = hook_audit859(env876, 'T876_final')
    if digest876_records != records_digest861(env876) or null_seal876 != physical_seal863(env876, env876['MEMNULL841']) or \
       hook['hook_count'] or hook['transformers_output_capturing_installed']:
        STATE876['blocks'].append('POST_RUN_INTEGRITY')
    STATE876['status'] = 'EARLY_STOP' if STATE876['early_stop'] else 'COMPLETE'; outcome876()
except BaseException as exc:
    STATE876['error'] = '%s: %s' % (type(exc).__name__, exc); STATE876['traceback'] = traceback.format_exc()
    STATE876['status'] = 'FAILED_AT_' + str(STATE876['status'])
    STATE876['outcome'] = {'outcome': 'TECHNICAL_BLOCK', 'blocks': ['EXCEPTION: ' + STATE876['error'][:400]]}
    (ROOT864 / 'TEST876_traceback.txt').write_text(STATE876['traceback'], encoding='utf-8')
    print('TEST876 ERROR', STATE876['error'][:400], '| full traceback:', ROOT864 / 'TEST876_traceback.txt',
          file=ERROR_CONSOLE864, flush=True)
finally:
    try:
        result = dict(STATE876, replays=STATE870['replays'])
        clean = json.loads(json.dumps(result, default=str, allow_nan=False))
        json_write864('TEST876_results.json', clean)
        (ROOT864 / 'TEST876_summary.txt').write_text(_j876.dumps(STATE876.get('outcome'), indent=2, sort_keys=True, default=str),
                                                       encoding='utf-8')
        manifest = {}
        for p in sorted(ROOT864.glob('TEST876*')):
            if p.is_file(): manifest[p.name] = _h876.sha256(p.read_bytes()).hexdigest()
        (ROOT864 / 'TEST876_SHA_manifest.json').write_text(_j876.dumps(manifest, indent=2, sort_keys=True), encoding='utf-8')
    except Exception as exc: print('RESULT_WRITE_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    try: report876()
    except Exception as exc: print('REPORT_FAILED', type(exc).__name__, exc, file=ERROR_CONSOLE864, flush=True)
    if 'EVENTS_FILE866' in globals() and not EVENTS_FILE866.closed: EVENTS_FILE866.close()
    if 'LOG_FILE864' in globals() and not LOG_FILE864.closed: LOG_FILE864.close()
exec(compile(ENGINE876['suffix'], 'test870.py:suffix', 'exec'), globals())
