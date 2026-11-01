# AKBASCORE SILICON HIPPOCAMPUS — TEST840, single Colab cell (one A100-SXM4-80GB, frozen Qwen2.5-72B-Instruct NF4).
# NATIVE H3 LATENT ROUTER: SELECTIVE TRANSFORMER BYPASS -> GPU NUMERICAL ADDRESS -> PHYSICAL CUT3 MOUNT -> NEW H3 STATE.
#   Addressing pass: the model's OWN modules run (embedding, rotary, causal mask, decoder layers 0..3) over the lower
#   K/V (layers 0..3) of the currently mounted physical memory; decoder layers 4..79 and lm_head are NOT executed
#   (temporary ModuleList truncation of model.model.layers, restored in finally; no hook). The question-token H3 rows
#   (bf16, 8192) are matched on the GPU against H3 key rows of the SHA-verified physical cartridges with the v2 TEST610/
#   624/626/627 rule (L3, rank-0 store centering + unit norm, beta 8, PEAK50 = 0.5 FRAM + 0.5 PEAK). The argmax index is
#   mapped mechanically to its cartridge file, SHA-verified and mounted with the locked native CUT3 engine (upper layers
#   4..79 recomputed). The second addressing pass is computed from the NEW state: the same question attends, in layers
#   0..3, to the lower K/V of the cartridge that was just mounted.
#   Classes: numerical candidate finding = ENGINEERING ROUTER (fixed GPU argmax, not cognition); physical execution =
#   mechanical; cognitive control (when to read, what next, when to stop) = NOT implemented, reported NOT_DEMONSTRATED.
#   Locked parts: TEST829 source (blob a5a25460), TEST834 mount/seal (834.py blob ab7b2046), TEST779 generation code
#   (blob fa7017a8, bytecode-verified), TEST757 build_fusion / TEST730 DirectCut3 via the locked engine chain, v2 610.py
#   transform_fit / apply and 626.py features626 / rerank626 (PEAK50) re-implemented on GPU from the cited source.
#   No GPU execution or result is claimed by the code author.
import urllib.request, hashlib, ast, json, time, random, math, re, numpy as np

REPO840 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
REPO2_840 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v2/main/"
LOCK829_840 = "a5a25460a3a6bbdf62a0571a9b5ff19e64159cf7"
LOCK834_840 = "ab7b2046d7b7e7be18aed8c6ce5a1397e0c991d7"
LOCK779_840 = "fa7017a87f25ecef6ed2b2954a850599cb25fcd9"
LOCK730_840 = "b1bad9eb3b111b44413f8ef05a3a140ab66a77dd"
LOCK757_840 = "3d88bf8638390995858f23391f1e043faa586835"
LOCK839_840 = "b76cf9f108f80008670b6fffcf0c2bb94b729cdc"
LOCK610_840 = "a62611a4ffd91c2fcf03796c31da2af11ccd8141345655b562f3a614568af3e7"   # sha256 (as locked by v2 TEST624)
LOCK626_840 = "86ccdbcc3c487675d98bcbe24415b5d10f8e7b0c"
LOCK627_840 = "483477eb375aa632914265ad23b871631ecab84d"
SEED840 = 8402026
EXPECTED_ARCH840 = (80, 8192, 64, 8, 128)
DEVICE_KIND840 = 'cuda'
WORLDS840 = 12                # 4 banks of 3 worlds x 7 cards = 21 physical cartridges per bank
BLOCK840 = 3
BANK_KINDS840 = ('first', 'second', 'changed', 'mirror', 'decoy', 'fork', 'bridgecont')
BETA840 = 8.0                 # v2 TEST610 locked CFG (3, 0, 8.0); TEST626/627 PEAK50 = (0.5, 0.0)
PEAK_WEIGHT840 = 0.5
MAX_NEW_ANS840 = 10
SEC_FUSION840, SEC_GEN840, SEC_BYPASS840, SEC_PROBE840, MARGIN840 = 0.95, 0.35, 0.4, 1.2, 1.25
PRED_LIMIT_MIN840 = 240.0
HARD_BUDGET_MIN840 = 300.0
RESUME840 = True
# Predeclared criteria (counts of 12 worlds; no fitted quantity anywhere)
A1_NEED840 = 9; B1_NEED840 = 9; B2_NEED840 = 9; C1_NEED840 = 10; D1_NEED840 = 10; E1_NEED840 = 9
H_END_NEED840 = 10; H_NULL_NEED840 = 10; H_BROKEN_NEED840 = 9
BYPASS_TOL840 = 1e-3          # relative max-abs tolerance for bypass H3 vs full-forward H3 (bitwise reported separately)

def fetch840(base, name, lock, limit=400000, kind='blob'):
    with urllib.request.urlopen(urllib.request.Request(base + name, headers={"User-Agent": "AKBASCORE-TEST840"}),
                                timeout=180) as f:
        raw = f.read(limit + 1)
    if kind == 'blob':
        got = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    else:
        got = hashlib.sha256(raw).hexdigest()
    assert len(raw) <= limit and got == lock, ("STOP_SOURCE_CHANGED", name, got)
    return raw

raw829_840 = fetch840(REPO840, "829.py", LOCK829_840)
raw834_840 = fetch840(REPO840, "834.py", LOCK834_840)
raw779_840 = fetch840(REPO840, "779.py", LOCK779_840)
raw730_840 = fetch840(REPO840, "730.py", LOCK730_840)
raw757_840 = fetch840(REPO840, "757.py", LOCK757_840)
raw839_840 = fetch840(REPO840, "839.py", LOCK839_840)
raw610_840 = fetch840(REPO2_840, "610.py", LOCK610_840, kind='sha256')
raw626_840 = fetch840(REPO2_840, "626.py", LOCK626_840)
raw627_840 = fetch840(REPO2_840, "627.py", LOCK627_840)
src840 = raw829_840.decode("utf-8")

def extract840(raw, body_name, names):
    tree = ast.parse(raw.decode("utf-8"))
    bodies = [n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == body_name]
    assert len(bodies) == 1, ('BODY_NOT_UNIQUE', body_name)
    text = bodies[0].value.value
    nodes = [n for n in ast.parse(text).body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert sorted(n.name for n in nodes) == sorted(names), ('HELPER_SET_MISMATCH', body_name)
    return "\n\n".join(ast.get_source_segment(text, n) for n in nodes)
HELPERS840 = ('mount834', 'seal834')
HELPER_SRC840 = extract840(raw834_840, 'BODY834', HELPERS840)
HELPER_SHA840 = hashlib.sha256(HELPER_SRC840.encode()).hexdigest()

# ---- v2 addressing mathematics, read from the cited sources (asserted, then re-implemented on GPU tensors) ----
def v2_source_facts840():
    s610 = raw610_840.decode('utf-8'); s626 = raw626_840.decode('utf-8'); s627 = raw627_840.decode('utf-8')
    t610 = ast.parse(s610)
    fns = {n.name: ast.get_source_segment(s610, n) for n in t610.body if isinstance(n, ast.FunctionDef)}
    facts = {
        'transform_fit_rank0_is_centering': "if rank==0:return mu,None" in fns.get('transform_fit', ''),
        'apply_is_center_then_unit_norm': ('Y=X-mu' in fns.get('apply', '') and 'unit_norm(Y)' in fns.get('apply', '')),
        'locked_cfg_layer3_rank0_beta8': "check('FRAM_LOCK_BEFORE_CUT3',CFG==(3,0,8.0)" in s610,
        'fram_formula': 'torch.logsumexp(s*BETA626,dim=1)-math.log(s.shape[1])).mean().item()/BETA626' in s626,
        'peak_formula': 'peak_scores={ci:float(s.max(dim=1).values.mean().item())' in s626,
        'rerank_mix': 'scores={ci:(1-a)*n[ci]+a*p[ci]+b*c[ci] for ci in ids}' in s626,
        'peak50_cfg': "('PEAK50',.5,0.)" in s626,
        'peak50_locked_in_627': "assert LOCKED627==('PEAK50',.5,0.),'RERANK_LOCK_MISMATCH'" in s627,
        'tie_break_by_id': 'sorted(ids,key=lambda ci:(-scores[ci],ci))' in s626,
        'v2_query_capture_used_forward_hooks': 'register_forward_hook' in fns.get('capture_residual', ''),
        'v2_candidate_stage_pca_faiss': 'INDEX.search' in s626}
    return facts
V2FACTS840 = v2_source_facts840()
assert all(v for k, v in V2FACTS840.items() if k not in ('v2_query_capture_used_forward_hooks', 'v2_candidate_stage_pca_faiss')), V2FACTS840

# ---- locked 779 reference code objects (same compile pipeline as the locked TEST785 loader; compiled, never run) ----
FG779_NODE840 = [n for n in ast.parse(raw779_840.decode('utf-8')).body if isinstance(n, ast.FunctionDef) and n.name == 'free_generate']
assert len(FG779_NODE840) == 1, 'LOCKED_779_SYMBOLS'
FG_DEFAULTS840 = tuple(ast.literal_eval(d) for d in FG779_NODE840[0].args.defaults)
def ref779_840(raw):
    tree = ast.parse(raw.decode('utf-8'), filename='779.py')
    idx = next((i for i, node in enumerate(tree.body) if isinstance(node, ast.Try)
                and any(isinstance(x, ast.Expr) and isinstance(x.value, ast.Call)
                        and isinstance(x.value.func, ast.Name) and x.value.func.id == 'log' for x in node.body[:3])), None)
    assert idx is not None and idx == len(tree.body) - 1, 'REF779_AST_BOUNDARY'
    mod = compile(ast.fix_missing_locations(ast.Module(body=tree.body[:idx], type_ignores=[])), 'TEST779_LOCKED_PRELUDE', 'exec')
    out = {}
    for c in mod.co_consts:
        if hasattr(c, 'co_code') and c.co_name == 'free_generate':
            out['free_generate'] = c
        if hasattr(c, 'co_code') and c.co_name in ('AttentionIntervention', 'Cut3Diagnostic'):
            for m in c.co_consts:
                if hasattr(m, 'co_code') and m.co_name in ('__init__', '__enter__', '__exit__'):
                    out[c.co_name + '.' + m.co_name] = m
    assert len(out) == 7, ('REF779_SYMBOLS', sorted(out))
    return out
REF779_840 = ref779_840(raw779_840)
# DirectCut3 (730) and build_fusion / native_append_direct (757) as locked sources: AST text for identity gates
def fn_src840(raw, name):
    s = raw.decode('utf-8'); t = ast.parse(s)
    n = [x for x in t.body if isinstance(x, (ast.FunctionDef, ast.ClassDef)) and x.name == name]
    assert len(n) == 1, ('LOCKED_SYMBOL', name)
    return ast.dump(n[0])
DC3_DUMP840 = fn_src840(raw730_840, 'DirectCut3')
BF_DUMP840 = fn_src840(raw757_840, 'build_fusion')
NAD_DUMP840 = fn_src840(raw757_840, 'native_append_direct')

def patch840(text, old, new):
    assert text.count(old) == 1, ("PATCH_ANCHOR_NOT_UNIQUE", old[:80], text.count(old))
    return text.replace(old, new, 1)

src840 = patch840(src840, "SEED829 = 8292026", "SEED829 = %d" % SEED840)
src840 = patch840(src840, "RUN829 = 'TEST829_'", "RUN829 = 'TEST840_'")
src840 = patch840(src840, "WORLDS829 = 3                    # small pilot (directive); no automatic extension",
                  "WORLDS829 = %d                   # TEST840 sealed evaluation worlds" % WORLDS840)
for a840, b840 in (("'TEST829_results.json'", "'TEST840_results.json'"), ("'TEST829.log'", "'TEST840.log'"),
                   ("'TEST829_blind_review.csv'", "'TEST840_case_table.csv'"),
                   ("'TEST829_offline_key.json'", "'TEST829_base_offline_key.json'")):
    src840 = patch840(src840, a840, b840)

PANEL_EXT840 = r'''
# ---------------- TEST840 PANEL EXTENSION (sealed before any model call) ----------------
def fresh840():
    while True:
        c = code829()
        if c not in seen829:
            seen829.add(c); return c
for w in worlds829:                       # base TEST829 cards are replaced by the TEST840 card set
    for cid in list(w['ids'].values()):
        cards829.pop(cid); card_meta829.pop(cid)
    w['ids'] = {}
    w['fork_end'] = fresh840(); w['bridge_mid'] = fresh840(); w['bridge_end'] = fresh840()
REL840 = {'first': ('start', 'middle'), 'second': ('middle', 'end'), 'changed': ('middle', 'changed_end'),
          'decoy': ('decoy_end', 'start'), 'mirror': ('end', 'middle'), 'fork': ('start', 'fork_end'),
          'bridgecont': ('bridge_mid', 'bridge_end'), 'first_bridged': ('start', 'bridge_mid')}
def body840(w, kind):
    a, b = REL840[kind]
    return 'Evidence record. Domain: ' + w['world'] + '\n' + 'Directed relation: ' + w[a] + ' -> ' + w[b] + '.\n'
_rng840 = random.Random(SEED829 + 40)
CONTENT840 = {}           # cartridge -> (world index, kind, id_version)      OFFLINE ONLY
BANKS840 = []             # per block: {'v0': [cartridges], 'v1': [cartridges]} same content order
def newcard840(wi, kind, ver):
    cid = 'E840_' + code829()
    assert cid not in cards829, 'CARD_ID_COLLISION'
    cards829[cid] = body840(worlds829[wi], kind)
    card_meta829[cid] = {'domain': worlds829[wi]['world'], 'kind': kind, 'id_version': ver, 'body_sha256': sha829(cards829[cid])}
    CONTENT840[cid] = (wi, kind, ver)
    return cid
for bi in range(0, len(worlds829), BLOCK840):
    contents = [(wi, k) for wi in range(bi, bi + BLOCK840) for k in BANK_KINDS840]
    _rng840.shuffle(contents)
    v = {}
    for ver in (0, 1):                     # v1: the same contents under new physical cartridge identities
        v[ver] = [newcard840(wi, k, ver) for wi, k in contents]
    for (wi, k), c0 in zip(contents, v[0]):
        worlds829[wi]['ids'][k] = c0
    for (wi, k), c1 in zip(contents, v[1]):
        worlds829[wi]['ids'][k + '_v1'] = c1
    BANKS840.append({'v0': v[0], 'v1': v[1], 'worlds': list(range(bi, bi + BLOCK840))})
for wi in range(len(worlds829)):           # designed bridge-change card: not in any bank
    worlds829[wi]['ids']['first_bridged'] = newcard840(wi, 'first_bridged', 0)
NAMES840 = {w[k] for w in worlds829 for k in ('world', 'start', 'middle', 'end', 'changed_end', 'decoy_end', 'fork_end',
                                                'bridge_mid', 'bridge_end')}
assert len(NAMES840) == 9 * len(worlds829), 'NAME_COLLISION'
QID840 = [questions829[i]['qid'] for i in range(len(worlds829))]
assert len(questions829) == len(worlds829), 'ONE_QUESTION_PER_WORLD'
BLOCKOF840 = {wi: wi // BLOCK840 for wi in range(len(worlds829))}
# Jobs. Runtime sees only opaque job IDs, mounts and banks; roles live in EVALKEY840 (offline key).
JOBS840, EVALKEY840 = [], {}
def job840(kind, qid, mount, bank, role):
    j = 'J840_' + ''.join(_rng840.choice('0123456789ABCDEF') for _ in range(12))
    JOBS840.append({'job': j, 'kind': kind, 'qid': qid, 'mount': list(mount), 'bank': list(bank)})
    EVALKEY840[j] = role
for wi, w in enumerate(worlds829):
    q = QID840[wi]; B = BANKS840[BLOCKOF840[wi]]; ids = w['ids']
    other = worlds829[BLOCKOF840[wi] * BLOCK840 + (wi + 1) % BLOCK840]['ids']
    job840('LIVE', q, [], B['v0'], {'world': wi, 'cond': 'LIVE'})
    reduced = [c for c in B['v0'] if c not in (ids['second'], ids['changed'])]
    job840('LIVE', q, [], reduced, {'world': wi, 'cond': 'LIVE_MISSING_CONTINUATION'})
    for cond, m, bank in (('ROUTE_AFTER_FIRST', [ids['first']], B['v0']),
                          ('ROUTE_AFTER_FIRST_BRIDGED', [ids['first_bridged']], [c for c in B['v0'] if c != ids['first']]),
                          ('ROUTE_AFTER_FORK', [ids['fork']], B['v0']),
                          ('ROUTE_AFTER_DECOY', [ids['decoy']], B['v0']),
                          ('ROUTE_AFTER_FIRST_V1', [ids['first_v1']], B['v1']),
                          ('ROUTE_AFTER_NULL_V1', [NULL829], B['v1'])):
        job840('ROUTE', q, m, bank, {'world': wi, 'cond': cond})
    for cond, m in (('ANSWER_FIRST_SECOND', [ids['first'], ids['second']]),
                    ('ANSWER_FIRST_IRRELEVANT', [ids['first'], other['second']]),
                    ('ANSWER_BRIDGED_SECOND', [ids['first_bridged'], ids['second']]),
                    ('ANSWER_BRIDGED_BRIDGECONT', [ids['first_bridged'], ids['bridgecont']]),
                    ('ANSWER_NULL', [NULL829])):
        job840('ANSWER', q, m, [], {'world': wi, 'cond': cond})
_rng840.shuffle(JOBS840)
assert len(JOBS840) == len(EVALKEY840) == len(worlds829) * 13, 'JOB_COUNT'
ALLBANK840 = sorted({c for B in BANKS840 for v in ('v0', 'v1') for c in B[v]})

def fus_upper840(k, maxb, p_):
    if k <= 0:
        return 0
    c = int(globals().get('CHUNK', 128))
    return (p_ + maxb + c - 1) // c + (k - 1) * ((maxb + c - 1) // c)

def cost_upper840(tok_of, p_):
    mx = max(tok_of.values()); nw = len(worlds829)
    up = {'fusion_forwards': 0, 'probe_forwards': 3 + 3, 'capture_forwards': 0, 'rank_forwards': 0,
          'generation_forwards': 1, 'bypass_forwards': 0}
    up['fusion_forwards'] += 6 * fus_upper840(2, mx, p_)                  # NULL mount, equivalence / recompute checks
    up['fusion_forwards'] += nw * 2 * (fus_upper840(1, mx, p_) + fus_upper840(2, mx, p_))   # LIVE + LIVE_MISSING
    up['fusion_forwards'] += nw * 6 * fus_upper840(1, mx, p_)               # ROUTE jobs
    up['fusion_forwards'] += nw * 5 * fus_upper840(2, mx, p_)               # ANSWER jobs
    up['bypass_forwards'] += nw * 2 * 2 + nw * 6 + 4
    up['generation_forwards'] += nw * (2 + 5) * MAX_NEW_ANS840 + 4 * MAX_NEW_ANS840
    sec = MARGIN840 * (up['fusion_forwards'] * SEC_FUSION840 + up['generation_forwards'] * SEC_GEN840 +
                       up['bypass_forwards'] * SEC_BYPASS840 + up['probe_forwards'] * SEC_PROBE840 + 120.0 + len(tok_of) * 2.0)
    return {'numeric_upper': up, 'jobs': len(JOBS840), 'physical_cartridges': len(tok_of), 'bank_cartridges': len(ALLBANK840),
            'max_memory_tokens': p_ + 2 * mx, 'minutes_upper_excluding_model_load': round(sec / 60.0, 1),
            'cost_model': 'fusion %.2f s, generated token %.2f s, bypass pass %.2f s, full probe %.2f s, x%.2f margin'
                          % (SEC_FUSION840, SEC_GEN840, SEC_BYPASS840, SEC_PROBE840, MARGIN840)}
'''
src840 = patch840(src840,
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n",
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n" + PANEL_EXT840)
PRECOST840 = r'''
    PRE840 = cost_upper840(tok_counts829, 30)
    D829['predicted_cost840_pre_model'] = PRE840
    log829('TEST840_PREDICTED_COST_BEFORE_MODEL_LOAD', json.dumps(PRE840))
    gate829('TEST840_PREDICTED_BUDGET', PRE840['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN840,
            {'minutes_upper': PRE840['minutes_upper_excluding_model_load'], 'limit': PRED_LIMIT_MIN840})
'''
# Source-level verification BEFORE the model is loaded (fails closed in seconds, not after the 13-minute load).
SRCVER840 = r'''
# ---------------- SOURCE-LEVEL VERIFICATION (pre-model) ----------------
def copy_receivers840(src):
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'copy':
            r = n.func.value
            out.append(isinstance(r, ast.Call) and isinstance(r.func, ast.Attribute) and r.func.attr == 'numpy')
    return out
cr840 = copy_receivers840(HELPER_SRC840) + copy_receivers840(BODY840_TEXT) + copy_receivers840(SRCVER840_TEXT)
gate829('STATIC_COPY_RECEIVERS_ARE_NDARRAY', all(cr840), {'copy_calls': len(cr840)})
MARK840 = '# ====== OFFLINE' + ' PHASE MARKER ======'
gate829('OFFLINE_MARKER_UNIQUE', BODY840_TEXT.count(MARK840) == 1)
pre840 = ast.parse(BODY840_TEXT.split(MARK840)[0])
hook840 = ast.parse(SRCVER840_TEXT)
body840t = ast.parse(BODY840_TEXT)
LABELS840 = {'EVALKEY840', 'CONTENT840', 'worlds829', 'card_meta829', 'NAMES840', 'BLOCKOF840'}
used840 = {n.id for t_ in (pre840, hook840) for n in ast.walk(t_) if isinstance(n, ast.Name)}
gate829('STATIC_NO_LABELS_BEFORE_OFFLINE', not (used840 & LABELS840), sorted(used840 & LABELS840))
hookcalls840 = sorted({n.attr for t_ in (body840t, hook840) for n in ast.walk(t_) if isinstance(n, ast.Attribute) and
                       n.attr in ('register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook')})
gate829('STATIC_NO_HOOK_REGISTRATION', not hookcalls840, hookcalls840)
# the ONLY assignments to model.model.layers are the truncation and its restoration inside h3_bypass840
lay840 = [n for n in ast.walk(body840t) if isinstance(n, ast.Assign) and any(ast.unparse(t) == 'model.model.layers' for t in n.targets)]
byp840 = [n for n in body840t.body if isinstance(n, ast.FunctionDef) and n.name == 'h3_bypass840']
inside840 = {id(x) for x in ast.walk(byp840[0])} if byp840 else set()
gate829('STATIC_LAYER_TRUNCATION_ONLY_IN_BYPASS', len(byp840) == 1 and len(lay840) == 2 and all(id(n) in inside840 for n in lay840),
        len(lay840))
fin840 = [n for n in ast.walk(byp840[0]) if isinstance(n, ast.Try)] if byp840 else []
gate829('STATIC_TRUNCATION_RESTORED_IN_FINALLY', len(fin840) == 1 and
        any(ast.unparse(s) == 'model.model.layers = full' for s in fin840[0].finalbody))
# generation = locked TEST779 code (code objects compiled through the identical locked pipeline)
def code_sig840(co):
    return (co.co_code, co.co_names, co.co_varnames, co.co_argcount, co.co_kwonlyargcount, co.co_flags,
            tuple(code_sig840(c) if hasattr(c, 'co_code') else repr(c) for c in co.co_consts))
import inspect as _insp840
def cmp840(live, ref):
    return {'bytecode_and_constants': code_sig840(live) == code_sig840(ref), 'filename': live.co_filename == ref.co_filename,
            'first_line': live.co_firstlineno == ref.co_firstlineno, 'name': live.co_name == ref.co_name,
            'live_filename': live.co_filename}
fgu840 = _insp840.unwrap(free_generate)
LB840 = {'free_generate': cmp840(fgu840.__code__, REF779_840['free_generate'])}
LB840['free_generate']['defaults'] = fgu840.__defaults__ == FG_DEFAULTS840
for m_ in ('__init__', '__enter__', '__exit__'):
    LB840['AttentionIntervention.' + m_] = cmp840(getattr(AttentionIntervention, m_).__code__, REF779_840['AttentionIntervention.' + m_])
CUT3INFO840 = {m_: cmp840(getattr(Cut3Diagnostic, m_).__code__, REF779_840['Cut3Diagnostic.' + m_]) for m_ in ('__init__', '__enter__', '__exit__')}
D829['locked_bytecode840'] = {'gated': LB840, 'informational_Cut3Diagnostic': CUT3INFO840}
gate829('LOCKED_FREE_GENERATE_BYTECODE', all(v for k, v in LB840['free_generate'].items() if k != 'live_filename'), LB840['free_generate'])
gate829('LOCKED_ATTENTION_INTERVENTION_BYTECODE',
        all(all(v for k, v in LB840['AttentionIntervention.' + m_].items() if k != 'live_filename') for m_ in ('__init__', '__enter__', '__exit__')),
        {k: v for k, v in LB840.items() if k.startswith('Att')})
log829('TEST840_CUT3_BYTECODE_INFO', json.dumps({m_: v['bytecode_and_constants'] for m_, v in CUT3INFO840.items()}))
# every free_generate call: seed=None, gain=0., spans=None; prompt = TEST827 answer frame of the question only
calls840 = [n for n in ast.walk(body840t) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'free_generate']
def call_ok840(n):
    kw = {k.arg: k.value for k in n.keywords}
    return (len(n.args) == 2 and isinstance(kw.get('seed'), ast.Constant) and kw['seed'].value is None and
            isinstance(kw.get('gain'), ast.Constant) and kw['gain'].value == 0 and
            isinstance(kw.get('spans'), ast.Constant) and kw['spans'].value is None and
            isinstance(n.args[1], ast.Call) and isinstance(n.args[1].func, ast.Name) and n.args[1].func.id == 'answer_prompt829'
            and ast.unparse(n.args[1].args[0]).startswith('QTEXT840['))
gate829('STATIC_GENERATION_CALLS_UNMODIFIED', len(calls840) == 1 and all(call_ok840(n) for n in calls840), len(calls840))
# the router consumes only tensors, the candidate list and the exclusion set (AST whitelist of free names)
rt840 = [n for n in body840t.body if isinstance(n, ast.FunctionDef) and n.name in ('route840', 'peak50_840', 'unit840')]
rnames840 = {n.id for f_ in rt840 for n in ast.walk(f_) if isinstance(n, ast.Name)}
gate829('STATIC_ROUTER_INPUTS', len(rt840) == 3 and rnames840 <= {
    'h_rows', 'bank', 'exclude', 'Q', 'K', 'S', 'fram', 'peak', 'cand', 'sc', 'idx', 'chosen', 't0', 'c', 'x', 'torch', 'math',
    'DEV', 'MU840', 'KEYS840', 'BETA840', 'PEAK_WEIGHT840', 'unit840', 'peak50_840', 'sorted', 'float', 'int', 'time', 'round',
    'len', 'zip', 'v', 'COUNT834'}, sorted(rnames840))
DC3CMP840 = {m_: cmp840(getattr(DirectCut3, m_).__code__, REF_DC3_840[m_]) for m_ in ('__init__', '__enter__', '__exit__')}
gate829('LOCKED_DIRECTCUT3_BYTECODE', all(all(v for k, v in d.items() if k != 'live_filename') for d in DC3CMP840.values()), DC3CMP840)
gate829('V2_ADDRESSING_SOURCE_FACTS', all(v for k, v in V2FACTS840.items()
                                          if k not in ('v2_query_capture_used_forward_hooks', 'v2_candidate_stage_pca_faiss')), V2FACTS840)
D829['source_verification840'] = True
log829('TEST840_SOURCE_VERIFIED_BEFORE_MODEL_LOAD')
'''
SRCVER840_TEXT = SRCVER840
src840 = patch840(src840, "    del tok829\n", "\n".join("    " + l if l else "" for l in SRCVER840.strip("\n").splitlines()) +
                  "\n    del tok829\n" + PRECOST840)

HYP840 = {
    'question': ('Can the frozen model\'s own lower-layer computation over mounted physical memory produce a new H3 query '
                 'state from which a fixed GPU numerical router reaches the relationally correct next cartridge?'),
    'functions': {'1_numerical_candidate_finding': 'GPU PEAK50 over H3 rows (engineering router; fixed argmax; NOT cognition)',
                  '2_physical_execution': 'index -> cartridge file, SHA-256 verified load, locked native CUT3 mount (mechanical)',
                  '3_cognitive_control': 'when to read / what next / when to stop: NOT implemented (fixed two-pass protocol)'},
    'bypass': ('addressing pass runs embedding, rotary, causal mask and decoder layers 0..3 of the model itself over the '
               'lower K/V of the mounted memory; layers 4..79 and lm_head are skipped (call counts gated); the final norm '
               'of the base model runs on H3 and its output is discarded.'),
    'second_query': ('the question-token H3 rows recomputed by layers 0..3 with the just-mounted cartridge\'s lower K/V in '
                     'the cache; never the previous H3 reused. A difference query (state with card minus NULL state) is '
                     'reported as a secondary, offline analysis only.'),
    'criteria': {
        'A1_FIRST_ADDRESS': 'live first pass selects the own first link in >= 9 of 12 worlds.',
        'B1_SECOND_AFTER_FIRST': 'with the own first link mounted, top-1 is a valid continuation (second / changed) in >= 9 of 12.',
        'B2_LIVE_CHAIN': 'live chain = own first then a valid continuation in >= 9 of 12.',
        'C1_MEMORY_DEPENDENCE': ('best valid continuation rank is better with the first link mounted than with NULL mounted '
                                 '(first excluded in both) in >= 10 of 12.'),
        'D1_BRIDGE_SENSITIVITY': ('with S->M\' mounted instead of S->M, the M\'-continuation rank improves AND the best '
                                  'M-continuation rank worsens, in >= 10 of 12.'),
        'E1_FORK_DECOY': 'with the own first link mounted, top-1 is not the fork or the inbound decoy in >= 9 of 12.',
        'F_INVARIANCE': ('engineering invariances: scores independent of key concatenation order (max abs <= 1e-9) and '
                         'identical contents selected under new physical cartridge identities (12 of 12).'),
        'G_MISSING': 'reported only: what the router selects without any continuation; no abstention is claimed.',
        'H_ABLATION': ('answers over designed mounts: first+second gives the end >= 10 of 12; NULL gives UNKNOWN >= 10 of 12; '
                       'bridged-first+second gives UNKNOWN >= 9 of 12 (memory affects the next computation).')},
    'verdicts': {'NATIVE_TENSOR_ROUTING': 'bypass + GPU router implemented (gates) and its relational result (B1, C1, D1)',
                 'MODEL_NATIVE_COGNITIVE_CONTROL': 'NOT_DEMONSTRATED by construction (fixed router, fixed pass count)',
                 'AUTONOMOUS_RECURSIVE_REASONING': 'NOT_DEMONSTRATED'},
    'decision': ('DEVAM if B1, C1 and D1 PASS. DUR if C1 FAIL and D1 FAIL. Otherwise YETERSİZ KANIT. A budget stop forces '
                 'YETERSİZ KANIT.'),
    'classes': {'H3 rows of the question (layers 0..3 over mounted lower K/V)': 'A (model computation)',
                'PEAK50 scores and argmax on GPU': 'B (fixed engineering router, v2 rule, not tuned here)',
                'index -> file, SHA, CUT3 mount, fixed two passes': 'C (mechanical execution / fixed protocol)'}}

CLAIMS840 = {
    'verified_from_prior_research': [
        'v2 TEST624-627 (Qwen 7B): L3 query + PCA128/FAISS candidates + TOP2 + PEAK50 selected the correct single fact '
        'cartridge in 96/96 on previously exposed facts; ranking was done by Python/FAISS; query capture used forward hooks.',
        'v2 TEST655/656: question-only H3 cosine for the second link 5/16 (random 6/16); Python sum of first-card and '
        'question H3 14/16 (external composition).',
        'v3 TEST834: PEAK50 on 72B H3, own first 15/30 vs fork 14/30 (single-card symmetry).',
        '839.log: text Record-ID addresses failed (FULL chain 11/48); selections dominated by start-entity cards and position.'],
    'implemented_in_TEST840': ['selective bypass of layers 4..79 and lm_head for addressing (no hooks)',
                               'GPU PEAK50 router on 72B H3 keys built from the same model', 'second pass from the new state',
                               'memory-removal, bridge-change, fork/decoy, physical-identity and order controls'],
    'demonstrated_by_TEST840': 'filled only from this run'}

# DirectCut3 reference: compiled exactly as the locked 779 extract_exact compiles the 730 symbols (never executed)
def ref_class_methods840(raw, label, names, cls):
    tree = ast.parse(raw.decode('utf-8'), filename=label)
    found = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name in names}
    assert set(found) == set(names), ('REF_SYMBOLS', label)
    mod = compile(ast.fix_missing_locations(ast.Module(body=[found[n] for n in names], type_ignores=[])), label, 'exec')
    out = {}
    for c in mod.co_consts:
        if hasattr(c, 'co_code') and c.co_name == cls:
            for m in c.co_consts:
                if hasattr(m, 'co_code'):
                    out[m.co_name] = m
    return out
REF_DC3_840 = ref_class_methods840(raw730_840, '730.py', ['DirectCut3', 'forge_native', 'initialize_native', 'to_gpu', 'seal_cp',
                                                         'memory_seals', 'compare_seals', 'safe_load', 'release'], 'DirectCut3')
assert set(REF_DC3_840) >= {'__init__', '__enter__', '__exit__'}, 'REF_DC3'

BODY840 = r'''
D829['test'] = '840'
D829['controller'] = ('ENGINEERING ROUTER (fixed GPU PEAK50 argmax over model H3 rows); fixed two-pass protocol; '
                      'no model-native cognitive control')
D829['sources840'] = {'829': LOCK829_840, '834': LOCK834_840, '779': LOCK779_840, '730': LOCK730_840, '757': LOCK757_840,
                      '839': LOCK839_840, 'v2_610_sha256': LOCK610_840, 'v2_626': LOCK626_840, 'v2_627': LOCK627_840,
                      'helpers_sha256': HELPER_SHA840, 'v2_source_facts': V2FACTS840}
D829['hypotheses840'] = PANEL829['test840']['hypotheses']
D829['limitations'] = [
    'The router is a fixed GPU tensor argmax (v2 PEAK50); it is an engineering component, not model-native cognition.',
    'The number of addressing passes (two) and the answer phase are a fixed protocol; no need / next / stop decision is made by the model.',
    'The addressing query is built from layers 0..3 only; upper-layer computation cannot influence a layer-3 state of '
    'the same tokens in a decoder-only transformer except through emitted tokens, which are not used for addressing.',
    'Twelve sealed worlds, one card template, one question template, one model. 21-cartridge banks (exact search, '
    'no PCA / FAISS approximation: the v2 candidate stage was an acceleration for 1,453 cartridges).',
    'Answer text is produced with the TEST827 boundary instruction; answers are scored offline only.',
    'No GPU execution or result is claimed by the code author.']
gate829('SOURCE_VERIFICATION_DONE_BEFORE_MODEL_LOAD', bool(D829.get('source_verification840')))
gate829('PANEL_FRESH_SEED', SEED829 == SEED840, SEED829)
gate829('NO_CONTROL_TEXT', MAX_NEW_CONTROL829 == 0)
gate829('WORLD_COUNT', len(questions829) == WORLDS840 and len(QID840) == WORLDS840)
gate829('JOBS_UNIQUE', len({j['job'] for j in JOBS840}) == len(JOBS840), len(JOBS840))
gate829('CARTRIDGES_PHYSICAL', all(c in entries for j in JOBS840 for c in j['mount'] + j['bank']) and NULL829 in entries)
exec(compile(HELPER_SRC840, 'TEST840_LOCKED_HELPERS', 'exec'), globals())
gate829('HELPERS_LOADED', all(callable(globals().get(x)) for x in HELPERS840), HELPER_SHA840)
gate829('ENGINE_SYMBOLS840', all(callable(globals().get(x)) for x in
        ('build_fusion', 'kv_digest', 'safe_load', 'free_generate', 'answer_prompt829', 'DirectCut3', 'cache_build')))
gate829('ARCH_DIMS', (NL, H, QH, KVH, HD) == EXPECTED_ARCH840 and int(model.config.num_attention_heads) == QH and
        int(model.config.num_key_value_heads) == KVH and int(model.config.hidden_size) == H and
        int(model.config.num_hidden_layers) == NL and len(model.model.layers) == NL, (NL, H, QH, KVH, HD))
gate829('BF16_COMPUTE', DTYPE == _torch829.bfloat16, str(DTYPE))
gate829('NF4_LINEAR4BIT', any(isinstance(m_, bitsandbytes.nn.Linear4bit) for m_ in model.modules()))
gate829('WEIGHTS_FROZEN', all(not p_.requires_grad for p_ in model.parameters()))
gate829('DEVICE', str(DEV).startswith(DEVICE_KIND840), str(DEV))
gate829('SDPA_MODULE', F is _torch829.nn.functional and F.scaled_dot_product_attention is SDPA829)
gate829('NO_RESIDUAL_HOOKS_START', all(not model.model.layers[i]._forward_hooks and not model.model.layers[i]._forward_pre_hooks
                                       for i in range(NL)))
gate829('PREFIX_P', P == 30, P)
POST840 = cost_upper840({c: int(entries[c]['body_tokens']) for c in cards829}, P)
D829['predicted_cost840'] = POST840
log829('TEST840_PREDICTED_COST', json.dumps(POST840))
gate829('PREDICTED_BUDGET_POST_LOAD', POST840['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN840,
        POST840['minutes_upper_excluding_model_load'])
QTEXT840 = {q['qid']: q['question'] for q in questions829}
# Router query frame (fixed for every question): '\nQUESTION:\n' + question + '\n' as concatenated token lists; the
# query rows are exactly the question-text tokens (v2 610 question_rep used the question span the same way).
QPRE840 = list(tok('\nQUESTION:\n', add_special_tokens=False).input_ids)
QPOST840 = list(tok('\n', add_special_tokens=False).input_ids)
QIDS840, QSPAN840 = {}, {}
for qid840, t840 in QTEXT840.items():
    body_ = list(tok(t840, add_special_tokens=False).input_ids)
    QIDS840[qid840] = QPRE840 + body_ + QPOST840
    QSPAN840[qid840] = (len(QPRE840), len(QPRE840) + len(body_))
gate829('FUSION_TOKENS', POST840['max_memory_tokens'] + max(len(v) for v in QIDS840.values()) + 128 <= MAX_FUSED_TOKENS,
        POST840['max_memory_tokens'])
try:
    free840, _ = _torch829.cuda.mem_get_info()
    gate829('VRAM_HEADROOM', free840 / 2**30 >= 8.0, round(free840 / 2**30, 2))
except Exception as e840:
    gate829('VRAM_HEADROOM', False, repr(e840))
D829['noninterference840'] = noninterference829([NULL829], questions829[0]['question'])
for k840, v840 in D829['noninterference840'].items():
    gate829('NONINTERFERENCE_' + k840.upper(), bool(v840), v840)
COUNT834 = {'fusion_forwards': fusion_forwards829([NULL829]), 'probe_forwards': 3, 'capture_forwards': 0,
            'rank_forwards': 0, 'generation_forwards': 1, 'mounts': 1, 'bypass_forwards': 0}
T0_840 = time.perf_counter()
SEAL_LAYERS834 = (0, CUT, NL // 2, NL - 1)

# ==================================================================================================================
# SELECTIVE BYPASS: the model's own embedding / rotary / mask / decoder layers 0..3 over the mounted lower K/V.
# ==================================================================================================================
ORIG_LAYERS840 = model.model.layers
ORIG_LAYER_IDS840 = [id(x) for x in ORIG_LAYERS840]
class CallCount840:
    """Observation-only instance-method replacement on every decoder layer and lm_head (never a hook); counts calls."""
    def __init__(self):
        self.n = {}; self.saved = []
    def __enter__(self):
        mods = [('L%d' % i, ORIG_LAYERS840[i]) for i in range(NL)] + [('HEAD', model.lm_head)]
        ctx = self
        for name, mod in mods:
            if mod._forward_hooks or mod._forward_pre_hooks:
                raise RuntimeError('HOOK_PRESENT_' + name)
            had = 'forward' in mod.__dict__; old = mod.forward; self.n[name] = 0
            def wrapped(this, *a, _name=name, _old=old, **k):
                ctx.n[_name] += 1
                return _old(*a, **k)
            mod.forward = types.MethodType(wrapped, mod)
            self.saved.append((mod, had, old))
        return self
    def __exit__(self, *exc):
        for mod, had, old in reversed(self.saved):
            if had:
                mod.forward = old
            else:
                mod.__dict__.pop('forward', None)
        self.saved = []
        return False
    def summary(self):
        lower = [self.n['L%d' % i] for i in range(CUT + 1)]
        upper = [self.n['L%d' % i] for i in range(CUT + 1, NL)]
        return {'lower_calls': lower, 'upper_min': min(upper), 'upper_max': max(upper), 'lm_head': self.n['HEAD']}
def h3_bypass840(mem, ids):
    n = int(mem[0][0].shape[-2])
    cache = cache_build(list(mem[:CUT + 1]))
    pos = torch.arange(n, n + len(ids), device=DEV)
    cap = []
    t0 = time.perf_counter()
    full = model.model.layers
    if full is not ORIG_LAYERS840 or len(full) != NL:
        raise RuntimeError('LAYERS_NOT_ORIGINAL')
    try:
        model.model.layers = torch.nn.ModuleList(list(full)[:CUT + 1])
        with torch.no_grad():
            with DirectCut3(full[CUT], 'capture', collector=cap):
                out = model.model(input_ids=torch.tensor([ids], device=DEV), past_key_values=cache,
                                  attention_mask=torch.ones((1, n + len(ids)), device=DEV, dtype=torch.long),
                                  position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
                del out
    finally:
        model.model.layers = full
    if model.model.layers is not ORIG_LAYERS840 or [id(x) for x in model.model.layers] != ORIG_LAYER_IDS840:
        raise RuntimeError('LAYERS_NOT_RESTORED')
    _torch829.cuda.synchronize()
    COUNT834['bypass_forwards'] += 1
    if len(cap) != 1:
        raise RuntimeError('BYPASS_CAPTURE_COUNT')
    h = cap[0][0]
    del cache, cap
    return h, round((time.perf_counter() - t0) * 1000.0, 3)
def h3_full840(mem, ids):
    n = int(mem[0][0].shape[-2])
    cache = cache_build(list(mem))
    pos = torch.arange(n, n + len(ids), device=DEV)
    cap = []
    t0 = time.perf_counter()
    with torch.no_grad():
        with DirectCut3(model.model.layers[CUT], 'capture', collector=cap):
            out = model(input_ids=torch.tensor([ids], device=DEV), past_key_values=cache,
                        attention_mask=torch.ones((1, n + len(ids)), device=DEV, dtype=torch.long),
                        position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
            del out
    _torch829.cuda.synchronize()
    COUNT834['probe_forwards'] += 1
    h = cap[0][0]
    del cache, cap
    return h, round((time.perf_counter() - t0) * 1000.0, 3)

# ---- physical H3 key bank (SHA-verified cartridges of the same 72B model; v2 rank-0 store fit: centering + unit norm) ----
KEYROWS840 = {}
t_keys840 = time.perf_counter()
for cid840 in ALLBANK840:
    cp840 = safe_load(entries[cid840])                     # locked: file SHA, cartridge ID and every tensor SHA verified
    KEYROWS840[cid840] = cp840['h'][0, P:, :].to(DEV).float()
    del cp840
gate829('KEY_ROWS_SHAPE', all(v.ndim == 2 and v.shape[1] == H and v.shape[0] >= 4 for v in KEYROWS840.values()), len(KEYROWS840))
MU840 = torch.cat([KEYROWS840[c] for c in ALLBANK840], dim=0).mean(dim=0)   # label-free store mean (v2 transform_fit rank 0)
def unit840(x):
    return x / x.norm(dim=-1, keepdim=True).clamp_min(1e-9)
KEYS840 = {c: unit840(v - MU840) for c, v in KEYROWS840.items()}
VPAIR840 = [(B['v0'][i], B['v1'][i]) for B in BANKS840 for i in range(len(B['v0']))]   # same content, new identity
D829['key_bank840'] = {'cartridges': len(KEYS840), 'rows': int(sum(v.shape[0] for v in KEYS840.values())),
                       'load_seconds': round(time.perf_counter() - t_keys840, 3),
                       'v1_keys_bitwise_identical_to_v0': [sum(1 for a_, b_ in VPAIR840 if torch.equal(KEYROWS840[a_], KEYROWS840[b_])),
                                                           len(VPAIR840)]}
def peak50_840(Q, K):
    S = (Q @ K.T).double()
    fram = ((torch.logsumexp(S * BETA840, dim=1) - math.log(S.shape[1])) / BETA840).mean()
    peak = S.max(dim=1).values.mean()
    return (1.0 - PEAK_WEIGHT840) * fram + PEAK_WEIGHT840 * peak
def route840(h_rows, bank, exclude):
    t0 = time.perf_counter()
    Q = unit840(h_rows.to(DEV).float() - MU840)
    cand = sorted(c for c in bank if c not in exclude)       # mechanical: never re-address a mounted cartridge
    sc = torch.stack([peak50_840(Q, KEYS840[c]) for c in cand])
    idx = int(torch.argmax(sc).item())                        # first maximum = smallest cartridge ID (v2 tie rule)
    chosen = cand[idx]
    return {'chosen': chosen, 'scores': {c: float(v) for c, v in zip(cand, sc.tolist())},
            'route_ms': round((time.perf_counter() - t0) * 1000.0, 3)}
def qrows840(h, qid):
    a, b = QSPAN840[qid]
    return h[a:b, :]

# ---- NULL memory (no relation), mounted once and kept ----
MEMNULL840, NNULL840 = mount834([NULL829], 'NULL')
SEALNULL840 = seal834(MEMNULL840)

# ---- BYPASS VERIFICATION: equivalence with the full model forward; call counts; restoration ----
qv840 = QID840[0]
with CallCount840() as cc840:
    hb840, msb840 = h3_bypass840(MEMNULL840, QIDS840[qv840])
CC_BYPASS840 = cc840.summary()
with CallCount840() as cc840:
    hf840, msf840 = h3_full840(MEMNULL840, QIDS840[qv840])
CC_FULL840 = cc840.summary()
d840 = float((hb840.float() - hf840.float()).abs().max().item()); s840 = float(hf840.float().abs().max().item())
JB840 = next(j for j in JOBS840 if j['bank'])
mem2_840, n2_840 = mount834([JB840['bank'][0]], 'EQUIV_CARD')
hb2_840, msb2_840 = h3_bypass840(mem2_840, QIDS840[qv840]); hf2_840, msf2_840 = h3_full840(mem2_840, QIDS840[qv840])
d2_840 = float((hb2_840.float() - hf2_840.float()).abs().max().item())
del mem2_840; gc.collect(); release()
D829['bypass_verification840'] = {
    'null_memory': {'bitwise': bool(torch.equal(hb840, hf840)), 'max_abs': d840, 'scale': s840,
                    'bypass_ms': msb840, 'full_forward_ms': msf840},
    'one_card_memory': {'bitwise': bool(torch.equal(hb2_840, hf2_840)), 'max_abs': d2_840,
                        'bypass_ms': msb2_840, 'full_forward_ms': msf2_840},
    'calls_bypass': CC_BYPASS840, 'calls_full': CC_FULL840, 'h3_dtype': str(hb840.dtype), 'h3_shape': list(hb840.shape)}
log829('TEST840_BYPASS_VERIFICATION', json.dumps(D829['bypass_verification840']))
gate829('BYPASS_H3_EQUALS_FULL_FORWARD_H3', d840 <= BYPASS_TOL840 * max(s840, 1e-9) and d2_840 <= BYPASS_TOL840 * max(s840, 1e-9),
        D829['bypass_verification840'])
gate829('BYPASS_SKIPS_UPPER_LAYERS_AND_LM_HEAD', CC_BYPASS840['lower_calls'] == [1] * (CUT + 1) and
        CC_BYPASS840['upper_max'] == 0 and CC_BYPASS840['lm_head'] == 0, CC_BYPASS840)
gate829('FULL_FORWARD_RUNS_ALL_LAYERS', CC_FULL840['lower_calls'] == [1] * (CUT + 1) and CC_FULL840['upper_min'] == 1 and
        CC_FULL840['upper_max'] == 1 and CC_FULL840['lm_head'] == 1, CC_FULL840)
gate829('LAYERS_RESTORED', model.model.layers is ORIG_LAYERS840 and len(model.model.layers) == NL)
gate829('NULL_MEMORY_UNCHANGED', seal834(MEMNULL840) == SEALNULL840)

# ---- ENGINEERING INVARIANCES (F): key concatenation order; physical identity of cartridges ----
def batched_scores840(Q, bank):
    K = torch.cat([KEYS840[c] for c in bank], dim=0)
    S = (Q @ K.T).double(); out = {}; s0 = 0
    for c in bank:
        m = KEYS840[c].shape[0]; Sc = S[:, s0:s0 + m]; s0 += m
        out[c] = float((1.0 - PEAK_WEIGHT840) * ((torch.logsumexp(Sc * BETA840, dim=1) - math.log(m)) / BETA840).mean() +
                       PEAK_WEIGHT840 * Sc.max(dim=1).values.mean())
    return out
Qv840 = unit840(qrows840(hb840, qv840).to(DEV).float() - MU840)
fw840 = batched_scores840(Qv840, JB840['bank']); bw840 = batched_scores840(Qv840, list(reversed(JB840['bank'])))
lp840 = route840(qrows840(hb840, qv840), JB840['bank'], set())['scores']
F_ORDER840 = max(max(abs(fw840[c] - bw840[c]) for c in fw840), max(abs(fw840[c] - lp840[c]) for c in fw840))
D829['invariance840'] = {'order_max_abs_score_diff': F_ORDER840}
del hb840, hf840, hb2_840, hf2_840

# ---- per-job record store (SHA-256 manifest; job-level resume) ----
EDIR840 = DIR829 / 'TEST840_jobs'
EDIR840.mkdir(exist_ok=True)
MAN840 = DIR829 / 'TEST840_job_manifest.jsonl'
HEADER840 = {'panel_sha256': PANEL_SHA829, 'body_sha256': PANEL829['test840']['body_sha256'], 'helpers_sha256': HELPER_SHA840}
REC840, ROWS840 = {}, {}
D829['resume840'] = {'enabled': RESUME840, 'source': None, 'reused_jobs': 0, 'reason': None}
if RESUME840:
    for cand in sorted(DIR829.parent.glob('TEST840_*/TEST840_job_manifest.jsonl'), reverse=True):
        if cand.parent == DIR829:
            continue
        try:
            lines = cand.read_text(encoding='utf-8').splitlines()
            if not lines or json.loads(lines[0]).get('header') != HEADER840:
                D829['resume840']['reason'] = 'header mismatch in ' + str(cand); continue
            got, gotr = {}, {}
            for ln in lines[1:]:
                o = json.loads(ln); fj = cand.parent / 'TEST840_jobs' / o['json']; fn = cand.parent / 'TEST840_jobs' / o['npz']
                if fj.exists() and fn.exists() and sha_file(fj) == o['json_sha256'] and sha_file(fn) == o['npz_sha256']:
                    got[o['key']] = json.loads(fj.read_text(encoding='utf-8'))
                    with np.load(fn, allow_pickle=False) as z:
                        gotr[o['key']] = {k: np.array(z[k], copy=True) for k in z.files}
            REC840.update(got); ROWS840.update(gotr)
            D829['resume840'].update({'source': str(cand), 'reused_jobs': len(got), 'reason': 'header and per-file SHA-256 verified'})
            break
        except Exception as e840r:
            D829['resume840']['reason'] = 'unreadable ' + str(cand) + ' ' + repr(e840r)
log829('TEST840_RESUME', json.dumps(D829['resume840']))
with MAN840.open('w', encoding='utf-8') as fh840:
    fh840.write(json.dumps({'header': HEADER840}, sort_keys=True) + '\n')
def save_job840(key, rec, rows):
    fj = EDIR840 / (key + '.json'); fn = EDIR840 / (key + '.npz')
    fj.write_text(json.dumps(rec, sort_keys=True), encoding='utf-8')
    np.savez(fn, **rows)
    with MAN840.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps({'key': key, 'json': fj.name, 'npz': fn.name, 'json_sha256': sha_file(fj),
                             'npz_sha256': sha_file(fn)}, sort_keys=True) + '\n')
for k840 in list(REC840):
    save_job840(k840, REC840[k840], ROWS840.get(k840, {}))

# ==================================================================================================================
# RUNTIME. Jobs are opaque; the router sees only H3 rows, a candidate list and the mounted (excluded) cartridges.
# ==================================================================================================================
BUDGET_STOP840 = False
def answer840(cards, qid, tag, counter=None):
    t0 = time.perf_counter()
    memx, n = mount834(list(cards), tag)
    t1 = time.perf_counter()
    seal = seal834(memx)
    o = free_generate(memx, answer_prompt829(QTEXT840[qid]), seed=None, gain=0., max_new=MAX_NEW_ANS840, spans=None)
    COUNT834['generation_forwards'] += int(o['generated_tokens'])
    gate829('MEAS_KV_SEAL_' + tag, seal834(memx) == seal)
    del memx; gc.collect(); release()
    return {'raw': o['raw'], 'generated_tokens': int(o['generated_tokens']), 'mount_ms': round((t1 - t0) * 1000.0, 3),
            'answer_ms': round((time.perf_counter() - t1) * 1000.0, 3), 'mount': list(cards)}
def state_route840(mount, qid, bank, tag):
    t0 = time.perf_counter()
    if mount == [NULL829]:
        h, ms = h3_bypass840(MEMNULL840, QIDS840[qid]); mount_ms = 0.0
    else:
        memx, n = mount834(list(mount), tag)
        mount_ms = round((time.perf_counter() - t0) * 1000.0, 3)
        seal = seal834(memx)
        h, ms = h3_bypass840(memx, QIDS840[qid])
        gate829('MEAS_KV_SEAL_' + tag, seal834(memx) == seal)
        del memx; gc.collect(); release()
    hr = qrows840(h, qid)
    r = route840(hr, bank, set(mount))
    r.update({'bypass_ms': ms, 'mount_ms': mount_ms})
    return r, hr.float().cpu().numpy().astype(np.float32)
UPPER_CHECK840 = {}
t_run840 = time.perf_counter()
nj840 = len(JOBS840); step840 = max(1, nj840 // 6)
log829('TEST840_PROGRESS', 'JOBS', 0, '/', nj840)
for ji840, j840 in enumerate(JOBS840):
    jj = j840['job']
    if jj not in REC840:
        if (time.perf_counter() - T0_840) / 60.0 > HARD_BUDGET_MIN840:
            BUDGET_STOP840 = True; log829('TEST840_BUDGET_STOP', 'job', ji840, 'of', nj840); break
        q = j840['qid']
        if j840['kind'] == 'LIVE':
            r1, h1 = state_route840([NULL829], q, j840['bank'], 'L1_' + jj)       # pass 1: baseline state
            c1 = r1['chosen']                                                    # router output, applied mechanically
            r2, h2 = state_route840([c1], q, j840['bank'], 'L2_' + jj)          # pass 2: NEW state (c1 mounted)
            c2 = r2['chosen']
            if not UPPER_CHECK840:
                with CallCount840() as ccu:
                    a = answer840([c1, c2], q, 'LA_' + jj)
                UPPER_CHECK840 = ccu.summary()
                gate829('CUT3_MOUNT_AND_ANSWER_RUN_UPPER_LAYERS', UPPER_CHECK840['upper_min'] >= 1 and UPPER_CHECK840['lm_head'] >= 1,
                        UPPER_CHECK840)
            else:
                a = answer840([c1, c2], q, 'LA_' + jj)
            rec = {'job': jj, 'kind': 'LIVE', 'pass1': r1, 'pass2': r2, 'answer': a}
            rows = {'h1': h1, 'h2': h2}
        elif j840['kind'] == 'ROUTE':
            r, h = state_route840(j840['mount'], q, j840['bank'], 'R_' + jj)
            rec = {'job': jj, 'kind': 'ROUTE', 'route': r}
            rows = {'h': h}
        else:
            rec = {'job': jj, 'kind': 'ANSWER', 'answer': answer840(j840['mount'], q, 'A_' + jj)}
            rows = {}
        REC840[jj] = rec; ROWS840[jj] = rows; save_job840(jj, rec, rows)
    if (ji840 + 1) % step840 == 0 or ji840 + 1 == nj840:
        log829('TEST840_PROGRESS', 'JOBS', ji840 + 1, '/', nj840)
D829['run_seconds840'] = round(time.perf_counter() - t_run840, 3)
D829['upper_layer_check840'] = UPPER_CHECK840
D829['budget_stop840'] = BUDGET_STOP840
gate829('NULL_MEMORY_UNCHANGED_FINAL', seal834(MEMNULL840) == SEALNULL840)
del MEMNULL840; gc.collect(); release()

engine_bindings829('FINAL')
gate829('FROZEN_WEIGHT_SENTINEL', before829 == sentinel())
gate829('LAYERS_RESTORED_FINAL', model.model.layers is ORIG_LAYERS840 and [id(x) for x in model.model.layers] == ORIG_LAYER_IDS840)
gate829('NO_RESIDUAL_HOOKS', all(not model.model.layers[i]._forward_hooks and not model.model.layers[i]._forward_pre_hooks
                                 for i in range(NL)))
gate829('NO_ATTENTION_HOOKS', all(not model.model.layers[i].self_attn._forward_hooks and
                                  not model.model.layers[i].self_attn._forward_pre_hooks for i in range(NL)))
gate829('SDPA_RESTORED_FINAL', F.scaled_dot_product_attention is SDPA829)
gate829('LM_HEAD_UNWRAPPED', model.lm_head.__dict__.get('forward') is HEAD_FWD829 and
        not model.lm_head._forward_hooks and not model.lm_head._forward_pre_hooks)
gate829('PANEL_UNCHANGED', sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True)) == PANEL_SHA829)
for cid840 in cards829:
    gate829('FINAL_SHA_' + cid840, sha_file(CART_DIR / entries[cid840]['file']) == entries[cid840]['sha256'])
COUNT_NUMERIC840 = dict(COUNT834)
gate829('COUNTED_WITHIN_UPPER_BOUND', all(COUNT_NUMERIC840.get(k, 0) <= POST840['numeric_upper'][k] for k in POST840['numeric_upper']),
        {'counted': COUNT_NUMERIC840, 'upper': POST840['numeric_upper']})

# ====== OFFLINE PHASE MARKER ======
# OFFLINE PHASE: every router pass and answer is finished and saved; roles are read only from here.
log829('TEST840_OFFLINE_START')
def frac840(xs):
    return [sum(1 for x in xs if x), len(xs)]
def ok840(k, n, need, full):
    return 'INCONCLUSIVE' if n < full else ('PASS' if k >= need else 'FAIL')
def role840(cid, wi):
    if cid == NULL829:
        return 'NULL'
    cw, k, ver = CONTENT840[cid]
    return ('OWN_' if cw == wi else 'OTHER_') + k.upper()
def rank840(scores, cids):
    order = sorted(scores, key=lambda c: (-scores[c], c))
    rs = [order.index(c) + 1 for c in cids if c in scores]
    return min(rs) if rs else None
def tcls840(t, w):
    u = (t or '').upper()
    names = [nm for nm, c in (('END', w['end']), ('ALT_END', w['changed_end']), ('MIDDLE', w['middle']), ('START', w['start']),
                              ('FORK_END', w['fork_end']), ('DECOY', w['decoy_end']), ('BRIDGE_MID', w['bridge_mid']),
                              ('BRIDGE_END', w['bridge_end'])) if c in u]
    return names + (['UNKNOWN'] if 'UNKNOWN' in u else [])
def tcat840(cls):
    if not cls:
        return 'EMPTY_OR_OTHER'
    if cls == ['UNKNOWN']:
        return 'UNKNOWN'
    if 'UNKNOWN' in cls:
        return 'MIXED'
    return cls[0] if len(cls) == 1 else 'MULTI:' + '+'.join(cls)
BYW840 = {}
for j in JOBS840:
    if j['job'] in REC840:
        k = EVALKEY840[j['job']]; BYW840.setdefault(k['world'], {})[k['cond']] = (j, REC840[j['job']])
W840 = {}
for wi, w in enumerate(worlds829):
    d = BYW840.get(wi, {}); ids = w['ids']; x = {'world': wi}
    valid = [ids['second'], ids['changed']]
    if 'LIVE' in d:
        _, r = d['LIVE']
        x['pass1_role'] = role840(r['pass1']['chosen'], wi); x['pass2_role'] = role840(r['pass2']['chosen'], wi)
        x['pass1_first_rank'] = rank840(r['pass1']['scores'], [ids['first']])
        x['pass1_margin'] = sorted(r['pass1']['scores'].values())[-1] - sorted(r['pass1']['scores'].values())[-2]
        x['live_chain'] = x['pass1_role'] == 'OWN_FIRST' and x['pass2_role'] in ('OWN_SECOND', 'OWN_CHANGED')
        x['live_answer'] = tcat840(tcls840(r['answer']['raw'], w))
        # C: NULL-state ranking with the first link excluded (same candidate set as the first-mounted pass)
        s0 = {c: v for c, v in r['pass1']['scores'].items() if c != ids['first']}
        x['null_valid_rank'] = rank840(s0, valid); x['null_bridgecont_rank'] = rank840(s0, [ids['bridgecont']])
        x['pass1_roles_top3'] = [role840(c, wi) for c in sorted(r['pass1']['scores'], key=lambda c: (-r['pass1']['scores'][c], c))[:3]]
    if 'LIVE_MISSING_CONTINUATION' in d:
        _, r = d['LIVE_MISSING_CONTINUATION']
        x['missing_pass1_role'] = role840(r['pass1']['chosen'], wi); x['missing_pass2_role'] = role840(r['pass2']['chosen'], wi)
        sc = sorted(r['pass2']['scores'].values())
        x['missing_pass2_margin'] = sc[-1] - sc[-2]; x['missing_answer'] = tcat840(tcls840(r['answer']['raw'], w))
    for cond, key in (('ROUTE_AFTER_FIRST', 'first'), ('ROUTE_AFTER_FIRST_BRIDGED', 'bridged'), ('ROUTE_AFTER_FORK', 'fork'),
                      ('ROUTE_AFTER_DECOY', 'decoy'), ('ROUTE_AFTER_FIRST_V1', 'first_v1'), ('ROUTE_AFTER_NULL_V1', 'null_v1')):
        if cond in d:
            _, r = d[cond]; s = r['route']['scores']
            vids = [ids[k + '_v1'] for k in ('second', 'changed')] if key in ('first_v1', 'null_v1') else valid
            bid = ids['bridgecont_v1'] if key in ('first_v1', 'null_v1') else ids['bridgecont']
            x[key + '_top1_role'] = role840(r['route']['chosen'], wi)
            x[key + '_valid_rank'] = rank840(s, vids); x[key + '_bridgecont_rank'] = rank840(s, [bid])
            x[key + '_top1_content'] = list(CONTENT840[r['route']['chosen']][:2])
    for cond in ('ANSWER_FIRST_SECOND', 'ANSWER_FIRST_IRRELEVANT', 'ANSWER_BRIDGED_SECOND', 'ANSWER_BRIDGED_BRIDGECONT', 'ANSWER_NULL'):
        if cond in d:
            x[cond] = tcat840(tcls840(d[cond][1]['answer']['raw'], w))
    W840[wi] = x
WL840 = list(W840.values())
def cnt840(f):
    xs = [f(x) for x in WL840]
    xs = [v for v in xs if v is not None]
    return [sum(1 for v in xs if v), len(xs)]
a1 = cnt840(lambda x: x.get('pass1_role') == 'OWN_FIRST' if 'pass1_role' in x else None)
b1 = cnt840(lambda x: x.get('first_top1_role') in ('OWN_SECOND', 'OWN_CHANGED') if 'first_top1_role' in x else None)
b2 = cnt840(lambda x: x.get('live_chain') if 'live_chain' in x else None)
c1 = cnt840(lambda x: (x['first_valid_rank'] < x['null_valid_rank'])
            if x.get('first_valid_rank') is not None and x.get('null_valid_rank') is not None else None)
d1 = cnt840(lambda x: (x['bridged_bridgecont_rank'] < x['first_bridgecont_rank'] and x['first_valid_rank'] < x['bridged_valid_rank'])
            if all(x.get(k) is not None for k in ('bridged_bridgecont_rank', 'first_bridgecont_rank', 'first_valid_rank',
                                                  'bridged_valid_rank')) else None)
e1 = cnt840(lambda x: x.get('first_top1_role') not in ('OWN_FORK', 'OWN_DECOY') if 'first_top1_role' in x else None)
f_id = cnt840(lambda x: (x['first_v1_top1_content'] == x['first_top1_content'])
              if 'first_v1_top1_content' in x and 'first_top1_content' in x else None)
f_id_null = cnt840(lambda x: (x['null_v1_top1_role'] == x['pass1_role']) if 'null_v1_top1_role' in x and 'pass1_role' in x else None)
h_end = cnt840(lambda x: x.get('ANSWER_FIRST_SECOND') == 'END' if 'ANSWER_FIRST_SECOND' in x else None)
h_null = cnt840(lambda x: x.get('ANSWER_NULL') == 'UNKNOWN' if 'ANSWER_NULL' in x else None)
h_broken = cnt840(lambda x: x.get('ANSWER_BRIDGED_SECOND') == 'UNKNOWN' if 'ANSWER_BRIDGED_SECOND' in x else None)
h_bridge = cnt840(lambda x: x.get('ANSWER_BRIDGED_BRIDGECONT') == 'BRIDGE_END' if 'ANSWER_BRIDGED_BRIDGECONT' in x else None)
h_irr = cnt840(lambda x: x.get('ANSWER_FIRST_IRRELEVANT') == 'UNKNOWN' if 'ANSWER_FIRST_IRRELEVANT' in x else None)
live_ans = cnt840(lambda x: x.get('live_answer') in ('END', 'ALT_END') if 'live_answer' in x else None)
def dist840(key):
    out = {}
    for x in WL840:
        if key in x:
            out[x[key]] = out.get(x[key], 0) + 1
    return out
NW840 = len(worlds829)
A1 = ok840(a1[0], a1[1], A1_NEED840, NW840); B1 = ok840(b1[0], b1[1], B1_NEED840, NW840)
B2 = ok840(b2[0], b2[1], B2_NEED840, NW840); C1 = ok840(c1[0], c1[1], C1_NEED840, NW840)
D1 = ok840(d1[0], d1[1], D1_NEED840, NW840); E1 = ok840(e1[0], e1[1], E1_NEED840, NW840)
F1 = ('PASS' if (F_ORDER840 <= 1e-9 and f_id[0] == NW840 and f_id_null[0] == NW840) else
      ('INCONCLUSIVE' if f_id[1] < NW840 else 'FAIL'))
H1 = ('INCONCLUSIVE' if min(h_end[1], h_null[1], h_broken[1]) < NW840 else
      'PASS' if (h_end[0] >= H_END_NEED840 and h_null[0] >= H_NULL_NEED840 and h_broken[0] >= H_BROKEN_NEED840) else 'FAIL')
# secondary, offline only: difference query (state with card minus NULL state) for the first and bridged mounts
DELTA840 = {'first_valid_rank': [], 'bridged_bridgecont_rank': [], 'first_bridgecont_rank': [], 'bridged_valid_rank': []}
for wi, w in enumerate(worlds829):
    d = BYW840.get(wi, {}); ids = w['ids']
    if not all(c in d for c in ('LIVE', 'ROUTE_AFTER_FIRST', 'ROUTE_AFTER_FIRST_BRIDGED')):
        continue
    h0 = torch.tensor(ROWS840[d['LIVE'][0]['job']]['h1'], device=DEV)
    for key, cond in (('first', 'ROUTE_AFTER_FIRST'), ('bridged', 'ROUTE_AFTER_FIRST_BRIDGED')):
        j, r = d[cond]
        hx = torch.tensor(ROWS840[j['job']]['h'], device=DEV)
        Qd = unit840(hx - h0)
        cand = sorted(c for c in j['bank'] if c not in j['mount'])
        s = {c: float(peak50_840(Qd, KEYS840[c])) for c in cand}
        DELTA840[key + '_valid_rank'].append(rank840(s, [ids['second'], ids['changed']]))
        DELTA840[key + '_bridgecont_rank'].append(rank840(s, [ids['bridgecont']]))
TIM840 = {}
for kind, path in (('bypass_ms', ('route', 'bypass_ms')), ('route_ms', ('route', 'route_ms')), ('mount_ms', ('route', 'mount_ms'))):
    vals = [REC840[j['job']][path[0]][path[1]] for j in JOBS840 if j['job'] in REC840 and REC840[j['job']]['kind'] == 'ROUTE']
    TIM840[kind + '_median'] = float(np.median(vals)) if vals else None
ans_ms = [REC840[j['job']]['answer']['answer_ms'] for j in JOBS840 if j['job'] in REC840 and REC840[j['job']]['kind'] == 'ANSWER']
TIM840['answer_ms_median'] = float(np.median(ans_ms)) if ans_ms else None
TIM840.update({'bypass_vs_full_ms_null': [D829['bypass_verification840']['null_memory']['bypass_ms'],
                                          D829['bypass_verification840']['null_memory']['full_forward_ms']],
               'key_bank_load_seconds': D829['key_bank840']['load_seconds']})
EXTCTRL840 = not all(c['pass'] for c in D829['checks'] if c['name'].startswith(('STATIC_', 'LOCKED_', 'BYPASS_', 'LAYERS_')))
ROUTING_IMPL840 = ('IMPLEMENTED_ENGINEERING_ROUTER' if all(c['pass'] for c in D829['checks'] if c['name'].startswith('BYPASS_'))
                   else 'NOT_IMPLEMENTED')
REL840 = 'PASS' if (B1 == 'PASS' and C1 == 'PASS' and D1 == 'PASS') else ('INCONCLUSIVE' if 'INCONCLUSIVE' in (B1, C1, D1) else 'FAIL')
if BUDGET_STOP840:
    decision840 = 'YETERSİZ KANIT'
elif REL840 == 'PASS':
    decision840 = 'DEVAM'
elif C1 == 'FAIL' and D1 == 'FAIL':
    decision840 = 'DUR'
else:
    decision840 = 'YETERSİZ KANIT'
CRIT840 = {'A1_FIRST_ADDRESS': A1, 'B1_SECOND_AFTER_FIRST': B1, 'B2_LIVE_CHAIN': B2, 'C1_MEMORY_DEPENDENCE': C1,
           'D1_BRIDGE_SENSITIVITY': D1, 'E1_FORK_DECOY': E1, 'F_INVARIANCE': F1, 'G_MISSING': 'REPORTED_ONLY',
           'H_ABLATION': H1}
VERDICTS840 = {'NATIVE_TENSOR_ROUTING': {'implementation': ROUTING_IMPL840, 'relational_second_pass': REL840},
               'MODEL_NATIVE_COGNITIVE_CONTROL': 'FAIL' if EXTCTRL840 else 'NOT_DEMONSTRATED (fixed router and fixed pass count)',
               'AUTONOMOUS_RECURSIVE_REASONING': 'NOT_DEMONSTRATED',
               'external_cognitive_control_detected': EXTCTRL840}
REPORT840 = {
    'bypass': D829['bypass_verification840'], 'upper_layer_check': UPPER_CHECK840,
    'A_first_address': {'own_first': a1, 'pass1_roles': dist840('pass1_role'), 'first_rank_median':
                        (float(np.median([x['pass1_first_rank'] for x in WL840 if x.get('pass1_first_rank')])) if WL840 else None)},
    'B_second_address': {'after_designed_first': b1, 'after_first_roles': dist840('first_top1_role'), 'live_chain': b2,
                         'live_pass2_roles': dist840('pass2_role'), 'live_answer_correct': live_ans},
    'C_memory_dependence': {'valid_rank_better_with_first_than_null': c1,
                            'ranks': [(x.get('null_valid_rank'), x.get('first_valid_rank')) for x in WL840]},
    'D_bridge': {'both_shifts': d1, 'ranks': [{k: x.get(k) for k in ('first_valid_rank', 'bridged_valid_rank', 'first_bridgecont_rank',
                                                                     'bridged_bridgecont_rank')} for x in WL840],
                 'bridged_top1_roles': dist840('bridged_top1_role')},
    'E_fork_decoy': {'after_first_not_fork_decoy': e1, 'after_fork_roles': dist840('fork_top1_role'),
                     'after_decoy_roles': dist840('decoy_top1_role')},
    'F_invariance': {'order_max_abs_score_diff': F_ORDER840, 'v1_keys_bitwise_identical': D829['key_bank840']['v1_keys_bitwise_identical_to_v0'],
                     'new_physical_ids_same_content_after_first': f_id,
                     'new_physical_ids_same_first_pass': f_id_null},
    'G_missing': {'pass2_roles': dist840('missing_pass2_role'), 'answers': dist840('missing_answer'),
                  'pass2_margins': [x.get('missing_pass2_margin') for x in WL840]},
    'H_ablation': {'first_second_end': h_end, 'null_unknown': h_null, 'bridged_second_unknown': h_broken,
                   'bridged_bridgecont_bridge_end': h_bridge, 'first_irrelevant_unknown': h_irr,
                   'answers': {c: dist840(c) for c in ('ANSWER_FIRST_SECOND', 'ANSWER_FIRST_IRRELEVANT', 'ANSWER_BRIDGED_SECOND',
                                                       'ANSWER_BRIDGED_BRIDGECONT', 'ANSWER_NULL')}, 'live_answers': dist840('live_answer')},
    'secondary_delta_query': DELTA840, 'timing': TIM840, 'verdicts': VERDICTS840, 'classes': HYP840['classes'],
    'resume': D829['resume840']}
D829['cells840'] = W840
D829['report840'] = REPORT840
D829['verdict840'] = {'decision': decision840, 'criteria': CRIT840, 'verdicts': VERDICTS840, 'budget_stop': BUDGET_STOP840,
                      'interpretation_guard': ('The GPU router is an engineering component. Passing B1/C1/D1 would show '
                                               'that the model\'s lower-layer state over mounted memory carries the next '
                                               'address numerically, not that the model controls its memory access.')}
D829['claims_ledger840'] = dict(CLAIMS840, demonstrated_by_TEST840={'decision': decision840, 'criteria': CRIT840, 'verdicts': VERDICTS840})
D829['cost840'] = {'counted': dict(COUNT834), 'predicted_upper': POST840, 'run_seconds': D829['run_seconds840'],
                   'total_seconds_body': round(time.perf_counter() - T0_840, 3),
                   'peak_gpu_gib': float(_torch829.cuda.max_memory_allocated()) / 2**30}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f840:
    cols840 = sorted({k for x in WL840 for k in x})
    wr840 = csv.DictWriter(f840, fieldnames=cols840)
    wr840.writeheader()
    for x in WL840:
        wr840.writerow({k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in x.items()})
D829['status'] = 'COMPLETE_TEST840_EVALUATED' if not BUDGET_STOP840 else 'STOPPED_BUDGET_PARTIAL_EVALUATED'
save829()
log829('TEST840_REPORT', json.dumps(REPORT840, default=str))
log829('TEST840_VERDICT', json.dumps(D829['verdict840'], default=str))
log829('TEST840_COMPLETED', str(OUT829))
'''
BODY_SHA840 = hashlib.sha256(BODY840.encode()).hexdigest()
PANEL_HOOK840 = ("PANEL829['test840'] = {'jobs': JOBS840, 'banks': BANKS840, 'beta': BETA840, 'peak_weight': PEAK_WEIGHT840, "
                 "'thresholds': {'A1': A1_NEED840, 'B1': B1_NEED840, 'B2': B2_NEED840, 'C1': C1_NEED840, 'D1': D1_NEED840, "
                 "'E1': E1_NEED840, 'H': [H_END_NEED840, H_NULL_NEED840, H_BROKEN_NEED840], 'bypass_tol': BYPASS_TOL840}, "
                 "'hypotheses': %r, 'body_sha256': %r, 'helpers_sha256': %r, 'seed': SEED829}\n"
                 % (HYP840, BODY_SHA840, HELPER_SHA840))
src840 = patch840(src840, "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))",
                  PANEL_HOOK840 + "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))")
OFFLINE_HOOK840 = r'''
OFFLINE840 = DIR829 / 'TEST840_offline_key.json'   # never read by any runtime computation
OFFLINE840.write_text(json.dumps({'note': 'OFFLINE ONLY', 'jobs': EVALKEY840,
                                  'cartridge_contents': {c: list(v) for c, v in CONTENT840.items()},
                                  'worlds': worlds829, 'questions': questions829, 'card_meta': card_meta829},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D829['offline_key840_sha256'] = sha829(OFFLINE840.read_bytes())
'''
src840 = patch840(src840, "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n",
                  "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n" + OFFLINE_HOOK840)
start840 = src840.index("    # RUN ORDER: integrity checks")
start840 = src840.rfind("    # ---", 0, start840)
end840 = src840.index("except BaseException as e:\n    D829['status'] = 'ERROR'", start840)
BODY840_TEXT = BODY840
replacement840 = "\n".join("    " + line if line else "" for line in BODY840.strip("\n").splitlines()) + "\n"
patched840 = src840[:start840] + replacement840 + src840[end840:]
ast.parse(patched840)
# ==================================================================================================================
# CONSOLE / LOGGING LAYER (TEST835 pattern). Nothing below changes what is computed. Every byte the engine prints is
# written unchanged to a full transcript file; the screen shows a compact digest, progress, failures and the summary.
# ==================================================================================================================
import os as _os840, sys as _sys840, io as _io840, traceback as _tb840, datetime as _dt840, shutil as _sh840
from pathlib import Path as _P840
_os840.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')     # download bars only (not data)
for _m840, _f840 in (('huggingface_hub', lambda m: m.utils.disable_progress_bars()),
                     ('transformers', lambda m: m.utils.logging.disable_progress_bar())):
    if _m840 in _sys840.modules:                                    # only if already imported: no new import
        try:
            _f840(_sys840.modules[_m840])
        except Exception:
            pass
_ROOT840 = _P840('/content') if _P840('/content').exists() else _P840('/tmp')
FULL_CONSOLE840 = _ROOT840 / ('TEST840_full_console_' + _dt840.datetime.now(_dt840.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.txt')
CON840 = {'phase': 'SOURCE_VERIFICATION', 'last': [], 'fail_lines': [], 't0': time.time(), 'measure': '0/0', 'p3': 0}
_ORIG_OUT840, _ORIG_ERR840 = _sys840.stdout, _sys840.stderr

def say840(*a):
    _ORIG_OUT840.write(' '.join(str(x) for x in a) + '\n'); _ORIG_OUT840.flush()

def _mins840():
    return round((time.time() - CON840['t0']) / 60.0, 1)

def route840(line):
    s = line.strip()
    if not s:
        return
    CON840['last'] = (CON840['last'] + [s[:300]])[-6:]
    if s.startswith('FAIL '):
        CON840['fail_lines'].append(s[:600]); say840('!! ' + s[:600]); return
    if s.startswith('TEST829_FAILED'):
        CON840['fail_lines'].append(s[:300]); return
    if s.startswith('TEST829_START'):
        parts = s.split()
        say840('Çalışma: %s | panel SHA-256: %s' % (parts[1] if len(parts) > 1 else '?', parts[-1]))
        CON840['phase'] = 'ENGINE_PRELUDE_AND_LOCKS'; return
    if s.startswith('TEST815_GPU_PREFLIGHT'):
        say840('GPU: ' + s[len('TEST815_GPU_PREFLIGHT'):].strip()); return
    if s.startswith('TEST815_GPU_FREE_GIB'):
        say840('GPU boş VRAM (yükleme öncesi): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('TEST840_PREDICTED_COST_BEFORE_MODEL_LOAD'):
        try:
            c = json.loads(s.split(' ', 1)[1]); u = c['numeric_upper']
            say840('Maliyet üst sınırı (model yükleme hariç, %%25 pay dahil): %s dk | iş %s | kartuş %s (banka %s) | fusion<=%s '
                   'bypass<=%s üretim<=%s' % (c['minutes_upper_excluding_model_load'], c['jobs'], c['physical_cartridges'],
                   c['bank_cartridges'], u['fusion_forwards'], u['bypass_forwards'], u['generation_forwards']))
        except Exception:
            say840(s[:300])
        CON840['phase'] = 'MODEL_LOAD'; say840('Model yükleniyor (Qwen2.5-72B-Instruct, NF4, tek yükleme)...'); return
    if s.startswith('PASS FROZEN_PREFIX'):
        D_ = globals().get('D829', {})
        say840('Model yüklendi (%s s). Fiziksel kartuşlar üretiliyor ve SHA doğrulanıyor...' % D_.get('model_load_seconds', '?'))
        CON840['phase'] = 'PHYSICAL_CARTRIDGE_FORGING'; return
    if s.startswith('PASS PHYSICAL_COUNT'):
        say840('Fiziksel kartuşlar: ' + s.split()[-1] + ' (her biri SHA-256 + tensör SHA ile yeniden yüklendi)')
        CON840['phase'] = 'PREFLIGHT_GATES'; return
    if s.startswith('PASS ARCH_DIMS'):
        say840('Mimari (NL,H,QH,KVH,HD): ' + s[len('PASS ARCH_DIMS'):].strip() + ' | BF16 hesap, NF4, ağırlıklar donmuş'); return
    if s.startswith('PASS VRAM_HEADROOM'):
        say840('Boş VRAM (model sonrası): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('PASS STATIC_NO_LABELS_BEFORE_OFFLINE'):
        say840('Sızıntı kapısı: çevrimdışı işaretinden önce hiçbir etiket nesnesi kullanılmıyor (AST)'); return
    if s.startswith('PASS LOCKED_FREE_GENERATE_BYTECODE'):
        say840('Kaynak doğrulama: free_generate bytecode = kilitli 779 derlemesi (aynı boru hattı); greedy argmax, örnekleme yok'); return
    if s.startswith('PASS LOCKED_ATTENTION_INTERVENTION_BYTECODE'):
        say840('Kaynak doğrulama: AttentionIntervention bytecode = kilitli 779 (bias=0: maske değişmez)'); return
    if s.startswith('TEST840_CUT3_BYTECODE_INFO'):
        say840('Bilgi: Cut3Diagnostic kilitli 779 bytecode eşitliği ' + s.split(' ', 1)[1][:160] + ' (seed=None: enjeksiyon dalı çalışmaz)'); return
    if s.startswith('TEST840_SOURCE_VERIFIED_BEFORE_MODEL_LOAD'):
        say840('Kaynak doğrulama tamam (model yüklenmeden önce)'); return
    if s.startswith('PASS STATIC_GENERATION_CALLS_UNMODIFIED'):
        say840('Kaynak doğrulama: cevap üretimi seed=None, gain=0, spans=None; adresleme dil üretimi kullanmıyor'); return
    if s.startswith('PASS STATIC_LAYER_TRUNCATION_ONLY_IN_BYPASS'):
        say840('Kaynak doğrulama: katman listesi yalnızca bypass fonksiyonunda kısaltılıyor ve finally ile geri yükleniyor'); return
    if s.startswith('PASS STATIC_ROUTER_INPUTS'):
        say840('Kaynak doğrulama: yönlendirici yalnızca H3 satırları, aday listesi ve takılı kartları görüyor (etiket yok)'); return
    if s.startswith('PASS LOCKED_DIRECTCUT3_BYTECODE'):
        say840('Kaynak doğrulama: DirectCut3 bytecode = kilitli 730 derlemesi'); return
    if s.startswith('PASS V2_ADDRESSING_SOURCE_FACTS'):
        say840('Kaynak doğrulama: v2 610/626/627 adresleme formülleri kaynakta doğrulandı (L3, rank-0, beta 8, PEAK50)'); return
    if s.startswith('TEST840_BYPASS_VERIFICATION'):
        try:
            r = json.loads(s.split(' ', 1)[1])
            say840('Bypass doğrulama: H3 bitwise (NULL %s, kart %s) | bypass çağrıları alt %s üst %s lm_head %s | %s ms vs tam %s ms'
                   % (r['null_memory']['bitwise'], r['one_card_memory']['bitwise'], r['calls_bypass']['lower_calls'],
                      r['calls_bypass']['upper_max'], r['calls_bypass']['lm_head'], r['null_memory']['bypass_ms'],
                      r['null_memory']['full_forward_ms']))
        except Exception:
            say840(s[:300])
        return
    if s.startswith('PASS CUT3_MOUNT_AND_ANSWER_RUN_UPPER_LAYERS'):
        say840('Üst katman yeniden hesaplama doğrulandı (CUT3 mount + cevap): ' + s[len('PASS CUT3_MOUNT_AND_ANSWER_RUN_UPPER_LAYERS'):].strip()[:160]); return
    if s.startswith('TEST840_RESUME '):
        try:
            r = json.loads(s.split(' ', 1)[1])
            say840('Devam mekanizması: yeniden kullanılan iş %s | %s' % (r.get('reused_jobs'), r.get('reason')))
            CON840['phase'] = 'RUNTIME'
        except Exception:
            say840(s[:300])
        return
    if s.startswith('TEST840_PROGRESS'):
        p = s.split()
        if len(p) >= 5:
            CON840['phase'] = 'MEASUREMENT %s (%s/%s)' % (p[1], p[2], p[4])
            if p[2] != '0':
                say840('  %-11s %s/%s (%s dk)' % (p[1], p[2], p[4], _mins840()))
        return
    if s.startswith('TEST840_BUDGET_STOP'):
        say840('!! ' + s); return
    if s.startswith('TEST840_OFFLINE_START'):
        CON840['phase'] = 'OFFLINE_EVALUATION'
        say840('Ölçüm bitti; çevrimdışı değerlendirme (%s dk)' % _mins840()); return
    if s.startswith('TEST840_COMPLETED'):
        CON840['phase'] = 'COMPLETED'; return

class Console840(_io840.TextIOBase):
    """Writes everything to FULL_CONSOLE840 unchanged; routes complete lines to the compact screen digest."""
    def __init__(self, orig, fh):
        self.orig = orig; self.fh = fh; self.buf = ''
    def writable(self):
        return True
    @property
    def encoding(self):
        return 'utf-8'
    def isatty(self):
        return False
    def fileno(self):
        return self.orig.fileno()
    def write(self, x):
        if not isinstance(x, str):
            x = str(x)
        if self.fh.closed:
            return self.orig.write(x)
        self.fh.write(x)
        self.buf += x
        while '\n' in self.buf:
            line, self.buf = self.buf.split('\n', 1)
            try:
                route840(line.split('\r')[-1])
            except Exception as e:
                self.fh.write('\n[console-layer route error ' + repr(e) + ']\n')
        if len(self.buf) > 20000:
            self.buf = self.buf[-2000:]
        return len(x)
    def flush(self):
        try:
            self.fh.flush()
        except Exception:
            pass

def sha_path840(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()

def fmt840(x):
    if isinstance(x, list) and len(x) == 2 and all(isinstance(v, (int, float)) for v in x):
        return '%s/%s' % (x[0], x[1])
    if isinstance(x, dict):
        return ', '.join('%s=%s' % (k, fmt840(v)) for k, v in x.items())
    if isinstance(x, float):
        return '%.4g' % x
    if isinstance(x, list):
        return '[' + ', '.join(fmt840(v) for v in x) + ']'
    return str(x)

def files_report840():
    say840('=' * 78); say840('SONUÇ DOSYALARI (SHA-256)')
    d = globals().get('DIR829')
    if d is None or not _P840(d).exists():
        say840('  (çalışma klasörü yok)'); return
    for p in sorted(_P840(d).iterdir()):
        if p.is_file():
            say840('  %s  %d B  %s' % (p, p.stat().st_size, sha_path840(p)))
    vd = _P840(d) / 'TEST840_jobs'
    if vd.exists():
        fs = sorted(x for x in vd.iterdir() if x.is_file())
        say840('  %s/  %d iş kaydı, %.1f MB (her dosyanın SHA-256 değeri TEST840_job_manifest.jsonl içinde)'
               % (vd, len(fs), sum(x.stat().st_size for x in fs) / 2**20))

def final840(D):
    R = D['report840']; V = D['verdict840']; K = V['criteria']; C = D['cost840']; VD = V['verdicts']
    checks = D.get('checks', [])
    BV = R['bypass']; U = R['upper_layer_check']; T = R['timing']
    say840('=' * 78); say840('TEST840 SONUÇ ÖZETİ (H3 bypass + GPU PEAK50 yönlendirici = MÜHENDİSLİK; bilişsel kontrol yok)'); say840('=' * 78)
    say840('Durum: %s | bütçe durdurması: %s | devam: yeniden kullanılan iş %s' % (D.get('status'), V['budget_stop'],
           R['resume'].get('reused_jobs')))
    say840('Bütünlük: %d kapı, %d başarısız | dış bilişsel kontrol tespit edildi: %s' % (len(checks), sum(not c['pass'] for c in checks),
           VD['external_cognitive_control_detected']))
    say840('-' * 78); say840('[BYPASS] adresleme geçişi: gömme + rotary + maske + katman 0-3 (modelin kendi modülleri), 4-79 ve lm_head yok')
    say840('  H3 %s %s | NULL bellek: bitwise %s, maks fark %s | tek kartlık bellek: bitwise %s, maks fark %s'
           % (BV['h3_shape'], BV['h3_dtype'], BV['null_memory']['bitwise'], fmt840(BV['null_memory']['max_abs']),
              BV['one_card_memory']['bitwise'], fmt840(BV['one_card_memory']['max_abs'])))
    say840('  Çağrı sayıları — bypass: alt %s, üst maks %s, lm_head %s | tam forward: üst min %s, lm_head %s'
           % (BV['calls_bypass']['lower_calls'], BV['calls_bypass']['upper_max'], BV['calls_bypass']['lm_head'],
              BV['calls_full']['upper_min'], BV['calls_full']['lm_head']))
    say840('  Süre: bypass %s ms / tam forward %s ms (NULL bellek) | medyan: bypass %s ms, yönlendirici %s ms, mount %s ms, cevap %s ms'
           % (T['bypass_vs_full_ms_null'][0], T['bypass_vs_full_ms_null'][1], fmt840(T['bypass_ms_median']),
              fmt840(T['route_ms_median']), fmt840(T['mount_ms_median']), fmt840(T['answer_ms_median'])))
    say840('  CUT3 mount + cevap sırasında üst katmanlar çalıştı: üst min %s, lm_head %s | anahtar bankası yükleme %s s'
           % (U.get('upper_min'), U.get('lm_head'), T['key_bank_load_seconds']))
    a = R['A_first_address']; b = R['B_second_address']; c = R['C_memory_dependence']; d = R['D_bridge']
    e = R['E_fork_decoy']; f = R['F_invariance']; g = R['G_missing']; h = R['H_ablation']
    say840('[A] İlk adres (NULL durum): kendi ilk kart %s | roller %s | ilk kart sırası medyanı %s'
           % (fmt840(a['own_first']), fmt840(a['pass1_roles']), fmt840(a['first_rank_median'])))
    say840('[B] İkinci adres — tasarlanmış ilk kart takılıyken top-1 geçerli devam %s | roller %s'
           % (fmt840(b['after_designed_first']), fmt840(b['after_first_roles'])))
    say840('    canlı zincir (yönlendiricinin kendi c1 -> c2) %s | ikinci geçiş rolleri %s | canlı cevap doğru %s'
           % (fmt840(b['live_chain']), fmt840(b['live_pass2_roles']), fmt840(b['live_answer_correct'])))
    say840('[C] Bellek bağımlılığı: geçerli devam sırası ilk kart takılıyken NULL\'dan iyi %s | (NULL, İLK) sıraları %s'
           % (fmt840(c['valid_rank_better_with_first_than_null']), fmt840(c['ranks'])))
    say840('[D] Köprü değişimi (S->M\' takılı): iki yönlü kayma %s | köprü-sonrası top-1 rolleri %s'
           % (fmt840(d['both_shifts']), fmt840(d['bridged_top1_roles'])))
    say840('[E] Fork/decoy: ilk kart takılıyken top-1 fork/decoy değil %s | fork takılıyken %s | decoy takılıyken %s'
           % (fmt840(e['after_first_not_fork_decoy']), fmt840(e['after_fork_roles']), fmt840(e['after_decoy_roles'])))
    say840('[F] Değişmezlik (mühendislik): anahtar sırası maks fark %s | yeni kimlikli anahtarlar bitwise aynı %s | aynı içerik (ilk kart sonrası) %s, (ilk geçiş) %s'
           % (fmt840(f['order_max_abs_score_diff']), fmt840(f['v1_keys_bitwise_identical']), fmt840(f['new_physical_ids_same_content_after_first']),
              fmt840(f['new_physical_ids_same_first_pass'])))
    say840('[G] Devam kartı yokken: ikinci geçiş rolleri %s | cevaplar %s (çekimserlik iddiası yok)'
           % (fmt840(g['pass2_roles']), fmt840(g['answers'])))
    say840('[H] Ablasyon cevapları: ilk+ikinci uç %s | NULL UNKNOWN %s | köprüsü bozuk+ikinci UNKNOWN %s | köprü+köprü-devam %s | ilk+ilgisiz UNKNOWN %s'
           % (fmt840(h['first_second_end']), fmt840(h['null_unknown']), fmt840(h['bridged_second_unknown']),
              fmt840(h['bridged_bridgecont_bridge_end']), fmt840(h['first_irrelevant_unknown'])))
    say840('    canlı zincir cevap kategorileri %s' % fmt840(h['live_answers']))
    dq = R['secondary_delta_query']
    say840('[İkincil, çevrimdışı] fark sorgusu (kart - NULL): ilk kart sonrası geçerli sıra %s | köprü sonrası köprü-devam sırası %s'
           % (dq['first_valid_rank'], dq['bridged_bridgecont_rank']))
    say840('-' * 78); say840('ÖLÇÜTLER')
    for k in K:
        say840('  %-24s %s' % (k, K[k]))
    say840('ÜÇ AYRI HÜKÜM:')
    say840('  NATIVE_TENSOR_ROUTING           uygulama: %s | ilişkisel ikinci geçiş: %s'
           % (VD['NATIVE_TENSOR_ROUTING']['implementation'], VD['NATIVE_TENSOR_ROUTING']['relational_second_pass']))
    say840('  MODEL_NATIVE_COGNITIVE_CONTROL  %s' % VD['MODEL_NATIVE_COGNITIVE_CONTROL'])
    say840('  AUTONOMOUS_RECURSIVE_REASONING  %s' % VD['AUTONOMOUS_RECURSIVE_REASONING'])
    say840('=' * 78)
    say840('NİHAİ BİLİMSEL KARAR: %s' % V['decision'])
    if V['decision'] == 'DEVAM':
        say840('  Gerekçe: B1, C1, D1 PASS — takılı belleğe bağlı yeni H3 durumu sabit sayısal yönlendiriciyle ilişkisel doğru '
               'devam kartını buldu. Yönlendirici mühendisliktir; bilişsel kontrol gösterilmedi.')
    elif V['decision'] == 'DUR':
        say840('  Gerekçe: C1 FAIL ve D1 FAIL — katman 0-3 durumu takılı belleğe ilişkisel olarak bağlanmadı.')
    else:
        say840('  Gerekçe: ' + ('bütçe durdurması' if V['budget_stop'] else
                               'ölçütler ne DEVAM ne DUR kuralını sağladı (bkz. B1 / C1 / D1 satırları)'))
    say840('Maliyet: sayılan %s | çalışma %s s | toplam gövde %s s | tepe VRAM %.2f GiB'
           % (fmt840(C['counted']), C['run_seconds'], C['total_seconds_body'], C['peak_gpu_gib']))

say840('=' * 78)
say840('AKBASCORE TEST840 — native H3 latent router: seçici Transformer bypass + GPU sayısal adres + fiziksel CUT3; Qwen2.5-72B (NF4, donmuş)')
say840('Kaynak kilitleri: 829 %s | 834 %s | 779 %s | 730 %s | 757 %s | 839 %s | v2 610(sha256) %s | v2 626 %s | v2 627 %s'
       % (LOCK829_840[:12], LOCK834_840[:12], LOCK779_840[:12], LOCK730_840[:12], LOCK757_840[:12], LOCK839_840[:12],
          LOCK610_840[:12], LOCK626_840[:12], LOCK627_840[:12]))
say840('Kilitli yardımcılar (AST, %d fonksiyon) SHA-256 %s' % (len(HELPERS840), HELPER_SHA840))
say840('BODY840 SHA-256 %s | yamalı kaynak AST geçti (%d bayt, SHA-256 %s)' % (BODY_SHA840, len(patched840), hashlib.sha256(patched840.encode()).hexdigest()))
say840('Kapsam: %d görülmemiş dünya, 21 kartuşluk 4 banka (+ yeni fiziksel kimlikli kopyalar), %d iş | yönlendirici = mühendislik, '
       'bilişsel kontrol test edilmiyor' % (WORLDS840, WORLDS840 * 13))
say840('Tam konsol kaydı: ' + str(FULL_CONSOLE840))
say840('=' * 78)
_fh840 = open(FULL_CONSOLE840, 'a', encoding='utf-8', buffering=1)
_fh840.write('TEST840_SOURCE_LOCKS ' + ' '.join((LOCK829_840, LOCK834_840, LOCK779_840, LOCK730_840, LOCK757_840, LOCK839_840, LOCK610_840, LOCK626_840, LOCK627_840)) +
             '\nTEST840_BODY_SHA256 ' + BODY_SHA840 + '\nTEST840_HELPERS ' + HELPER_SHA840 +
             '\nTEST840_PATCHED_SOURCE_AST_PASS ' + str(len(patched840)) + ' ' + hashlib.sha256(patched840.encode()).hexdigest() + '\n')
import linecache as _lc840
for _nm840, _src840 in (('TEST840_LOCKED_ENGINE', patched840), ('TEST840_LOCKED_HELPERS', HELPER_SRC840)):
    _lc840.cache[_nm840] = (len(_src840), None, [x + '\n' for x in _src840.splitlines()], _nm840)
_sys840.stdout = Console840(_ORIG_OUT840, _fh840); _sys840.stderr = Console840(_ORIG_ERR840, _fh840)
TEST840_ERROR = None
try:
    exec(compile(patched840, 'TEST840_LOCKED_ENGINE', 'exec'), globals())
except BaseException as _e840:
    TEST840_ERROR = _e840
    _tbtext840 = _tb840.format_exc()
    _fh840.write('\n[TEST840 OUTER EXCEPTION]\n' + _tbtext840)
finally:
    _sys840.stdout, _sys840.stderr = _ORIG_OUT840, _ORIG_ERR840
    try:
        _fh840.flush(); _fh840.close()
    except Exception:
        pass
    _dir840 = globals().get('DIR829')
    if _dir840 is not None and _P840(_dir840).exists() and FULL_CONSOLE840.exists():
        _dst840 = _P840(_dir840) / FULL_CONSOLE840.name
        _sh840.move(str(FULL_CONSOLE840), str(_dst840)); FULL_CONSOLE840 = _dst840
if TEST840_ERROR is not None:
    D_ = globals().get('D829', {}) if isinstance(globals().get('D829'), dict) else {}
    bad = [c for c in D_.get('checks', []) if not c.get('pass')]
    say840('=' * 78); say840('TEST840 HATA')
    say840('Tür: %s.%s' % (type(TEST840_ERROR).__module__, type(TEST840_ERROR).__name__))
    say840('Mesaj: ' + repr(TEST840_ERROR)[:800])
    say840('Aşama: ' + CON840['phase'] + ' | geçen %s dk' % _mins840())
    if bad:
        say840('Başarısız kapı: %s | ayrıntı: %s' % (bad[-1].get('name'), str(bad[-1].get('detail'))[:400]))
    say840('Hata öncesi son motor satırları:')
    for x in CON840['last'][-4:]:
        say840('  ' + x[:240])
    tbl = _tbtext840.rstrip().splitlines()
    say840('Traceback (son %d satır; tamamı dosyada ve results.json içinde):' % min(40, len(tbl)))
    for x in tbl[-40:]:
        say840('  ' + x)
    files_report840()
    say840('Tam konsol kaydı: %s  SHA-256 %s' % (FULL_CONSOLE840, sha_path840(FULL_CONSOLE840) if FULL_CONSOLE840.exists() else '-'))
    say840('Not: tamamlanan ölçümler vektör dosyalarında; hücre yeniden çalıştırılırsa SHA doğrulanıp yeniden kullanılır.')
    raise SystemExit('TEST840_FAILED: ' + type(TEST840_ERROR).__name__)
try:
    final840(D829)
except Exception as _e840s:
    say840('!! Özet basılamadı (veri dosyalarda tam): ' + repr(_e840s))
    say840(_tb840.format_exc()[-1500:])
files_report840()
say840('=' * 78)
