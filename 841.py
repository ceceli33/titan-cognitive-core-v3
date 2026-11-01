# ===== TEST841 PARÇA 1/3 — Colab'da aynı hücreye sırayla yapıştırın =====
# AKBASCORE SILICON HIPPOCAMPUS — TEST841, single Colab cell (one A100-SXM4-80GB, frozen Qwen2.5-72B-Instruct NF4).
# LATENT RE-ENTRY: CAN DEEP RELATIONAL COMPUTATION AFTER THE FIRST PHYSICAL MEMORY BECOME THE NEXT NUMERICAL ADDRESS?
#   Built on the GPU-completed TEST840 backbone (840.py blob 06bc63dd): locked TEST829 source, TEST834 mount/seal,
#   TEST779 generation code (bytecode-verified), TEST730 DirectCut3 (bytecode-verified), TEST840 selective H3 bypass and
#   GPU PEAK50 router (v2 610/626/627 rule). The physical H3 / CUT3 / lower K/V cartridges, SSD files and SHA-256 gates
#   are unchanged and append-only.
#   Engine fact used here (730.py initialize_native + DirectCut3 inject): a vector written at the layer-3 output is
#   invisible to layers 0..3 of every position; the only dynamic input to any layer-3 query is a layer-0 input
#   (embedding-level) vector. Every feedback path is therefore a map psi: deep state -> layer-0 input vector:
#     M2S  vocabulary re-entry, soft : e = softmax(lm_head(norm(h79)))^T E          (probability-weighted embedding)
#     M2H  vocabulary re-entry, hard : e = E[argmax lm_head(norm(h79))]            (greedy token embedding)
#     D1   direct latent feedback    : e = norm(h79) * rms(E) / rms(norm(h79))      (no vocabulary, Coconut-style)
#   Each arm runs K fixed steps from the same probe (lookup frame + fixed assistant prefill) over the mounted memory;
#   the K vectors are placed in a fixed index frame and passed through the TEST840 bypass (layers 0..3 over the NULL
#   memory: the address depends on the mounted card only through the deep computation); the H3 rows of the K
#   positions are routed by the unchanged TEST840 PEAK50 router. Controls: the TEST840 question-row router (D) and a
#   diagnostic mid/upper-layer direct router (M1, layers 16/32/48/64/79, keys forged from the same model).
#   A separate closed loop lets the MODEL choose ANSWER / SEARCH / DROP / STOP (one word, applied literally); Python
#   only mounts, routes the model's own echo, unmounts on DROP and enforces a step budget reported as BUDGET_STOP.
#   Classes: echo, action word, answer = model computation (A); PEAK50 argmax = fixed engineering router (B);
#   mount / unmount / budget = mechanical (C). No GPU execution or result is claimed by the code author.
import urllib.request, hashlib, ast, json, time, random, math, re, contextlib, numpy as np

REPO841 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
REPO2_841 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v2/main/"
LOCK829_841 = "a5a25460a3a6bbdf62a0571a9b5ff19e64159cf7"
LOCK834_841 = "ab7b2046d7b7e7be18aed8c6ce5a1397e0c991d7"
LOCK779_841 = "fa7017a87f25ecef6ed2b2954a850599cb25fcd9"
LOCK730_841 = "b1bad9eb3b111b44413f8ef05a3a140ab66a77dd"
LOCK757_841 = "3d88bf8638390995858f23391f1e043faa586835"
LOCK839_841 = "b76cf9f108f80008670b6fffcf0c2bb94b729cdc"
LOCK840_841 = "06bc63ddcda9c11780bd99a7dd58f00f57b80f0e"   # GPU-completed TEST840 source (backbone lineage)
LOCK610_841 = "a62611a4ffd91c2fcf03796c31da2af11ccd8141345655b562f3a614568af3e7"   # sha256 (as locked by v2 TEST624)
LOCK626_841 = "86ccdbcc3c487675d98bcbe24415b5d10f8e7b0c"
LOCK627_841 = "483477eb375aa632914265ad23b871631ecab84d"
SEED841 = 8412026
EXPECTED_ARCH841 = (80, 8192, 64, 8, 128)
DEVICE_KIND841 = 'cuda'
WORLDS841 = 12                # 4 banks of 3 worlds x 7 cards = 21 physical cartridges per bank (+ new-ID copies)
BLOCK841 = 3
BANK_KINDS841 = ('first', 'second', 'changed', 'mirror', 'decoy', 'fork', 'bridgecont')
BETA841 = 8.0                 # v2 TEST610 locked CFG (3, 0, 8.0); TEST626/627 PEAK50 = (0.5, 0.0)
PEAK_WEIGHT841 = 0.5
MAX_NEW_ANS841 = 10
MAX_NEW_ACT841 = 6
K_ECHO841 = 8                 # fixed number of re-entry steps per arm; rows from the model's own end token on are not indexed
T_MAX841 = 5                  # mechanical step budget of the closed loop (reported as BUDGET_STOP, never as model DUR)
ARMS841 = ('M2S', 'M2H', 'D1')
LENS841 = (8, 16, 24, 32, 40, 48, 56, 64, 72, 79)   # step-0 last-position capture layers (offline logit lens)
MID841 = (16, 32, 48, 64, 79)                      # diagnostic direct mid/upper-layer addressing (M1)
ACTIONS841 = ('ANSWER', 'SEARCH', 'DROP', 'STOP')
# Fixed text frames (identical for every world; no name, answer or cartridge identity inside).
LOOKUP_A841 = ('Use only mounted physical evidence. Follow directed links. Question: {q}\n'
               'Name the single node whose evidence record must be read next to continue. Reply with the node name only.')
LOOKUP_B841 = ('The mounted evidence may be incomplete. Question: {q}\n'
               'Which node should be looked up next? Reply with one node name.')
ACTION_TXT841 = ('Use only mounted physical evidence. Follow directed links. Question: {q}\n'
                 'Decide your next step. Reply with exactly one word:\n'
                 'ANSWER = the mounted evidence is sufficient to answer the question\n'
                 'SEARCH = another evidence record must be read first\n'
                 'DROP = the most recently read record is irrelevant or misleading and should be removed\n'
                 'STOP = the answer cannot be found and further reading will not help')
PREFILL_TXT841 = 'Next node:'         # fixed assistant prefill of the lookup probe
IDXPRE_TXT841 = '\nNext node:'        # fixed index frame around the K re-entry vectors
IDXPOST_TXT841 = '\n'
def lookup_prompt841(q, frame):
    return (LOOKUP_A841 if frame == 'A' else LOOKUP_B841).format(q=q)
def action_prompt841(q):
    return ACTION_TXT841.format(q=q)
# Cost model calibrated on 840.log (278.6 s run: 243 fusion forwards, 368 generated tokens, 122 bypasses), x2 safety.
SEC_FUSION841, SEC_GEN841, SEC_BYPASS841, SEC_PROBE841, MARGIN841 = 0.6, 0.2, 0.1, 0.5, 1.25
PRED_LIMIT_MIN841 = 240.0
HARD_BUDGET_MIN841 = 300.0
RESUME841 = True
# Predeclared criteria (counts of 12 worlds; fixed before any GPU result; no fitted quantity anywhere)
R1_NEED841 = 9          # designed first mounted: top-1 is a card containing the bridge entity (second/changed/mirror)
SHIFT_NEED841 = 9       # bridge changed S->M': top-1 = M'-continuation AND (first mounted) top-1 is an M-card
NULLCTRL_NEED841 = 10   # NULL and irrelevant mounts: top-1 is not an own M-card / M'-card
SPEC_NEED841 = 10       # fork / decoy mounts: top-1 is not an own M-card
ID_NEED841 = 11         # new physical identities: same content selected
FRAME_NEED841 = 9       # lookup frame B: R1 and SHIFT counts (secondary)
I3_NEED841 = 9          # final-layer next-token argmax = first token of the bridge entity (first mounted)
I2_NEED841 = 10         # bridge-entity token rank better with first mounted than with NULL and with irrelevant
L1_NEED841 = 9; L2_NEED841 = 9; L3_NEED841 = 9
A_NULL_NEED841 = 10; A_FIRST_NEED841 = 10; A_COMPLETE_NEED841 = 10; A_BROKEN_NEED841 = 9
H_END_NEED841 = 10; H_ORDER_NEED841 = 10; H_NULL_NEED841 = 10; H_BROKEN_NEED841 = 9
BYPASS_TOL841 = 1e-3          # relative max-abs tolerance for bypass H3 vs full-forward H3 (bitwise reported separately)
ORDER_TOL841 = 1e-5           # absolute score tolerance for key-concatenation order (float32 matmul); same argmax required

def fetch841(base, name, lock, limit=400000, kind='blob'):
    with urllib.request.urlopen(urllib.request.Request(base + name, headers={"User-Agent": "AKBASCORE-TEST841"}),
                                timeout=180) as f:
        raw = f.read(limit + 1)
    if kind == 'blob':
        got = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    else:
        got = hashlib.sha256(raw).hexdigest()
    assert len(raw) <= limit and got == lock, ("STOP_SOURCE_CHANGED", name, got)
    return raw

raw829_841 = fetch841(REPO841, "829.py", LOCK829_841)
raw834_841 = fetch841(REPO841, "834.py", LOCK834_841)
raw779_841 = fetch841(REPO841, "779.py", LOCK779_841)
raw730_841 = fetch841(REPO841, "730.py", LOCK730_841)
raw757_841 = fetch841(REPO841, "757.py", LOCK757_841)
raw839_841 = fetch841(REPO841, "839.py", LOCK839_841)
raw840_841 = fetch841(REPO841, "840.py", LOCK840_841)
raw610_841 = fetch841(REPO2_841, "610.py", LOCK610_841, kind='sha256')
raw626_841 = fetch841(REPO2_841, "626.py", LOCK626_841)
raw627_841 = fetch841(REPO2_841, "627.py", LOCK627_841)
src841 = raw829_841.decode("utf-8")

def extract841(raw, body_name, names):
    tree = ast.parse(raw.decode("utf-8"))
    bodies = [n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == body_name]
    assert len(bodies) == 1, ('BODY_NOT_UNIQUE', body_name)
    text = bodies[0].value.value
    nodes = [n for n in ast.parse(text).body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert sorted(n.name for n in nodes) == sorted(names), ('HELPER_SET_MISMATCH', body_name)
    return "\n\n".join(ast.get_source_segment(text, n) for n in nodes)
HELPERS841 = ('mount834', 'seal834')
HELPER_SRC841 = extract841(raw834_841, 'BODY834', HELPERS841)
HELPER_SHA841 = hashlib.sha256(HELPER_SRC841.encode()).hexdigest()

# ---- v2 addressing mathematics, read from the cited sources (asserted, then re-implemented on GPU tensors) ----
def v2_source_facts841():
    s610 = raw610_841.decode('utf-8'); s626 = raw626_841.decode('utf-8'); s627 = raw627_841.decode('utf-8')
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
V2FACTS841 = v2_source_facts841()
assert all(v for k, v in V2FACTS841.items() if k not in ('v2_query_capture_used_forward_hooks', 'v2_candidate_stage_pca_faiss')), V2FACTS841

# ---- locked 779 reference code objects (same compile pipeline as the locked TEST785 loader; compiled, never run) ----
FG779_NODE841 = [n for n in ast.parse(raw779_841.decode('utf-8')).body if isinstance(n, ast.FunctionDef) and n.name == 'free_generate']
assert len(FG779_NODE841) == 1, 'LOCKED_779_SYMBOLS'
FG_DEFAULTS841 = tuple(ast.literal_eval(d) for d in FG779_NODE841[0].args.defaults)
def ref779_841(raw):
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
REF779_841 = ref779_841(raw779_841)
# DirectCut3 (730) and build_fusion / native_append_direct (757) as locked sources: AST text for identity gates
def fn_src841(raw, name):
    s = raw.decode('utf-8'); t = ast.parse(s)
    n = [x for x in t.body if isinstance(x, (ast.FunctionDef, ast.ClassDef)) and x.name == name]
    assert len(n) == 1, ('LOCKED_SYMBOL', name)
    return ast.dump(n[0])
DC3_DUMP841 = fn_src841(raw730_841, 'DirectCut3')
BF_DUMP841 = fn_src841(raw757_841, 'build_fusion')
NAD_DUMP841 = fn_src841(raw757_841, 'native_append_direct')

def patch841(text, old, new):
    assert text.count(old) == 1, ("PATCH_ANCHOR_NOT_UNIQUE", old[:80], text.count(old))
    return text.replace(old, new, 1)

src841 = patch841(src841, "SEED829 = 8292026", "SEED829 = %d" % SEED841)
src841 = patch841(src841, "RUN829 = 'TEST829_'", "RUN829 = 'TEST841_'")
src841 = patch841(src841, "WORLDS829 = 3                    # small pilot (directive); no automatic extension",
                  "WORLDS829 = %d                   # TEST841 sealed evaluation worlds" % WORLDS841)
for a841, b841 in (("'TEST829_results.json'", "'TEST841_results.json'"), ("'TEST829.log'", "'TEST841.log'"),
                   ("'TEST829_blind_review.csv'", "'TEST841_case_table.csv'"),
                   ("'TEST829_offline_key.json'", "'TEST829_base_offline_key.json'")):
    src841 = patch841(src841, a841, b841)

PANEL_EXT841 = r'''
# ---------------- TEST841 PANEL EXTENSION (sealed before any model call; fresh seed: unseen entities) ----------------
def fresh841():
    while True:
        c = code829()
        if c not in seen829:
            seen829.add(c); return c
for w in worlds829:                       # base TEST829 cards are replaced by the TEST841 card set
    for cid in list(w['ids'].values()):
        cards829.pop(cid); card_meta829.pop(cid)
    w['ids'] = {}
    w['fork_end'] = fresh841(); w['bridge_mid'] = fresh841(); w['bridge_end'] = fresh841()
REL841 = {'first': ('start', 'middle'), 'second': ('middle', 'end'), 'changed': ('middle', 'changed_end'),
          'decoy': ('decoy_end', 'start'), 'mirror': ('end', 'middle'), 'fork': ('start', 'fork_end'),
          'bridgecont': ('bridge_mid', 'bridge_end'), 'first_bridged': ('start', 'bridge_mid')}
def body841(w, kind):
    a, b = REL841[kind]
    return 'Evidence record. Domain: ' + w['world'] + '\n' + 'Directed relation: ' + w[a] + ' -> ' + w[b] + '.\n'
_rng841 = random.Random(SEED829 + 41)
CONTENT841 = {}           # cartridge -> (world index, kind, id_version)      OFFLINE ONLY
BANKS841 = []             # per block: {'v0': [cartridges], 'v1': [cartridges]} same content order
def newcard841(wi, kind, ver):
    cid = 'E841_' + code829()
    assert cid not in cards829, 'CARD_ID_COLLISION'
    cards829[cid] = body841(worlds829[wi], kind)
    card_meta829[cid] = {'domain': worlds829[wi]['world'], 'kind': kind, 'id_version': ver, 'body_sha256': sha829(cards829[cid])}
    CONTENT841[cid] = (wi, kind, ver)
    return cid
for bi in range(0, len(worlds829), BLOCK841):
    contents = [(wi, k) for wi in range(bi, bi + BLOCK841) for k in BANK_KINDS841]
    _rng841.shuffle(contents)
    v = {}
    for ver in (0, 1):                     # v1: the same contents under new physical cartridge identities
        v[ver] = [newcard841(wi, k, ver) for wi, k in contents]
    for (wi, k), c0 in zip(contents, v[0]):
        worlds829[wi]['ids'][k] = c0
    for (wi, k), c1 in zip(contents, v[1]):
        worlds829[wi]['ids'][k + '_v1'] = c1
    BANKS841.append({'v0': v[0], 'v1': v[1], 'worlds': list(range(bi, bi + BLOCK841))})
for wi in range(len(worlds829)):           # designed bridge-change card: not in any bank
    worlds829[wi]['ids']['first_bridged'] = newcard841(wi, 'first_bridged', 0)
NAMES841 = {w[k] for w in worlds829 for k in ('world', 'start', 'middle', 'end', 'changed_end', 'decoy_end', 'fork_end',
                                                'bridge_mid', 'bridge_end')}
assert len(NAMES841) == 9 * len(worlds829), 'NAME_COLLISION'
assert not any(nm in t_ for nm in NAMES841 for t_ in (LOOKUP_A841, LOOKUP_B841, ACTION_TXT841, PREFILL_TXT841,
                                                 IDXPRE_TXT841, IDXPOST_TXT841)), 'FRAME_CONTAINS_PANEL_NAME'
QID841 = [questions829[i]['qid'] for i in range(len(worlds829))]
assert len(questions829) == len(worlds829), 'ONE_QUESTION_PER_WORLD'
BLOCKOF841 = {wi: wi // BLOCK841 for wi in range(len(worlds829))}
NBLOCK841 = len(BANKS841)
# Jobs. Runtime sees only opaque job IDs, mounts, banks, frame and arm; roles live in EVALKEY841 (offline key).
JOBS841, EVALKEY841 = [], {}
def job841(kind, qid, role, mount=(), bank=(), frame='A', arm=None, start=()):
    j = 'J841_' + ''.join(_rng841.choice('0123456789ABCDEF') for _ in range(12))
    JOBS841.append({'job': j, 'kind': kind, 'qid': qid, 'mount': list(mount), 'bank': list(bank), 'frame': frame,
                    'arm': arm, 'start': list(start)})
    EVALKEY841[j] = role
for wi, w in enumerate(worlds829):
    q = QID841[wi]; B = BANKS841[BLOCKOF841[wi]]; ids = w['ids']
    other = worlds829[BLOCKOF841[wi] * BLOCK841 + (wi + 1) % BLOCK841]['ids']              # same bank, other world
    far = worlds829[((BLOCKOF841[wi] + 1) % NBLOCK841) * BLOCK841 + wi % BLOCK841]['ids']  # other bank: unrelated names
    no_first = [c for c in B['v0'] if c != ids['first']]
    missing = [c for c in B['v0'] if c not in (ids['second'], ids['changed'])]
    for cond, m, bank, fr in (('S_NULL', [NULL829], B['v0'], 'A'), ('S_FIRST', [ids['first']], B['v0'], 'A'),
                              ('S_BRIDGED', [ids['first_bridged']], no_first, 'A'), ('S_FORK', [ids['fork']], B['v0'], 'A'),
                              ('S_DECOY', [ids['decoy']], B['v0'], 'A'), ('S_IRREL', [far['first']], B['v0'], 'A'),
                              ('S_FIRST_V1', [ids['first_v1']], B['v1'], 'A'), ('S_NULL_FB', [NULL829], B['v0'], 'B'),
                              ('S_FIRST_FB', [ids['first']], B['v0'], 'B'), ('S_BRIDGED_FB', [ids['first_bridged']], no_first, 'B')):
        job841('STATE', q, {'world': wi, 'cond': cond}, mount=m, bank=bank, frame=fr)
    for cond, m in (('ANSWER_FIRST_SECOND', [ids['first'], ids['second']]), ('ANSWER_SECOND_FIRST', [ids['second'], ids['first']]),
                    ('ANSWER_FIRST_IRRELEVANT', [ids['first'], other['second']]),
                    ('ANSWER_BRIDGED_SECOND', [ids['first_bridged'], ids['second']]),
                    ('ANSWER_BRIDGED_BRIDGECONT', [ids['first_bridged'], ids['bridgecont']]), ('ANSWER_NULL', [NULL829])):
        job841('ANSWER', q, {'world': wi, 'cond': cond}, mount=m)
    for cond, m in (('ACT_NULL', [NULL829]), ('ACT_FIRST', [ids['first']]), ('ACT_COMPLETE', [ids['first'], ids['second']]),
                    ('ACT_BROKEN', [ids['first_bridged'], ids['second']]), ('ACT_FORK', [ids['fork']])):
        job841('ACTION', q, {'world': wi, 'cond': cond}, mount=m)
    for arm in ARMS841:
        for cond, st, bank in (('LOOP_LIVE', [], B['v0']), ('LOOP_MISSING', [], missing), ('LOOP_FORK', [ids['fork']], B['v0'])):
            job841('LOOP', q, {'world': wi, 'cond': cond, 'arm': arm}, bank=bank, arm=arm, start=st)
_rng841.shuffle(JOBS841)
assert len(JOBS841) == len(EVALKEY841) == len(worlds829) * 30, 'JOB_COUNT'
ALLBANK841 = sorted({c for B in BANKS841 for v in ('v0', 'v1') for c in B[v]})

def fus_upper841(k, maxb, p_):
    if k <= 0:
        return 0
    c = int(globals().get('CHUNK', 128))
    return (p_ + maxb + c - 1) // c + (k - 1) * ((maxb + c - 1) // c)

def cost_upper841(tok_of, p_):
    mx = max(tok_of.values()); nw = len(worlds829); K = K_ECHO841; T = T_MAX841; na = len(ARMS841)
    up = {'fusion_forwards': 0, 'probe_forwards': 12, 'capture_forwards': 0, 'rank_forwards': 0,
          'generation_forwards': 1 + 3 * K, 'bypass_forwards': 0}
    up['fusion_forwards'] += 6 * fus_upper841(2, mx, p_)                         # NULL mount, equivalence checks
    up['fusion_forwards'] += nw * 10 * fus_upper841(1, mx, p_)                   # STATE jobs
    up['fusion_forwards'] += nw * 6 * fus_upper841(2, mx, p_)                    # ANSWER jobs
    up['fusion_forwards'] += nw * 5 * fus_upper841(2, mx, p_)                    # ACTION jobs
    up['fusion_forwards'] += nw * 3 * na * T * fus_upper841(T + 1, mx, p_)       # LOOP jobs (one mount per step)
    up['probe_forwards'] += len(ALLBANK841)                                      # mid-layer key forge
    up['probe_forwards'] += nw * 10 * na + nw * 3 * na * T                       # lookup probes (step 0 of every echo)
    up['generation_forwards'] += nw * 10 * na * (K - 1) + nw * 3 * na * T * (K - 1)   # echo steps 1..K-1
    up['generation_forwards'] += nw * 6 * MAX_NEW_ANS841 + nw * 5 * MAX_NEW_ACT841
    up['generation_forwards'] += nw * 3 * na * (T * MAX_NEW_ACT841 + MAX_NEW_ANS841) + 4 * MAX_NEW_ANS841
    up['bypass_forwards'] += nw * 10 * (1 + na) + nw * 3 * na * T + 8
    sec = MARGIN841 * (up['fusion_forwards'] * SEC_FUSION841 + up['generation_forwards'] * SEC_GEN841 +
                       up['bypass_forwards'] * SEC_BYPASS841 + up['probe_forwards'] * SEC_PROBE841 + 120.0 + len(tok_of) * 2.0)
    return {'numeric_upper': up, 'jobs': len(JOBS841), 'physical_cartridges': len(tok_of), 'bank_cartridges': len(ALLBANK841),
            'max_memory_tokens': p_ + (T + 1) * mx, 'minutes_upper_excluding_model_load': round(sec / 60.0, 1),
            'cost_model': 'fusion %.2f s, generated/echo token %.2f s, bypass pass %.2f s, full probe %.2f s, x%.2f margin'
                          % (SEC_FUSION841, SEC_GEN841, SEC_BYPASS841, SEC_PROBE841, MARGIN841)}
'''
src841 = patch841(src841,
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n",
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n" + PANEL_EXT841)
PRECOST841 = r'''
    PRE841 = cost_upper841(tok_counts829, 30)
    D829['predicted_cost841_pre_model'] = PRE841
    log829('TEST841_PREDICTED_COST_BEFORE_MODEL_LOAD', json.dumps(PRE841))
    gate829('TEST841_PREDICTED_BUDGET', PRE841['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN841,
            {'minutes_upper': PRE841['minutes_upper_excluding_model_load'], 'limit': PRED_LIMIT_MIN841})
'''
# Source-level verification BEFORE the model is loaded (fails closed in seconds, not after the 13-minute load).
SRCVER841 = r'''
# ---------------- SOURCE-LEVEL VERIFICATION (pre-model) ----------------
def copy_receivers841(src):
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'copy':
            r = n.func.value
            out.append(isinstance(r, ast.Call) and isinstance(r.func, ast.Attribute) and r.func.attr == 'numpy')
    return out
cr841 = copy_receivers841(HELPER_SRC841) + copy_receivers841(BODY841_TEXT) + copy_receivers841(SRCVER841_TEXT)
gate829('STATIC_COPY_RECEIVERS_ARE_NDARRAY', all(cr841), {'copy_calls': len(cr841)})
MARK841 = '# ====== OFFLINE' + ' PHASE MARKER ======'
gate829('OFFLINE_MARKER_UNIQUE', BODY841_TEXT.count(MARK841) == 1)
pre841 = ast.parse(BODY841_TEXT.split(MARK841)[0])
hook841 = ast.parse(SRCVER841_TEXT)
body841t = ast.parse(BODY841_TEXT)
LABELS841 = {'EVALKEY841', 'CONTENT841', 'worlds829', 'card_meta829', 'NAMES841', 'BLOCKOF841'}
used841 = {n.id for t_ in (pre841, hook841) for n in ast.walk(t_) if isinstance(n, ast.Name)}
gate829('STATIC_NO_LABELS_BEFORE_OFFLINE', not (used841 & LABELS841), sorted(used841 & LABELS841))
hookcalls841 = sorted({n.attr for t_ in (body841t, hook841) for n in ast.walk(t_) if isinstance(n, ast.Attribute) and
                       n.attr in ('register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook')})
gate829('STATIC_NO_HOOK_REGISTRATION', not hookcalls841, hookcalls841)
# the ONLY assignments to model.model.layers are the truncation and its restoration inside h3_bypass841
lay841 = [n for n in ast.walk(body841t) if isinstance(n, ast.Assign) and any(ast.unparse(t) == 'model.model.layers' for t in n.targets)]
byp841 = [n for n in body841t.body if isinstance(n, ast.FunctionDef) and n.name == 'h3_bypass841']
inside841 = {id(x) for x in ast.walk(byp841[0])} if byp841 else set()
gate829('STATIC_LAYER_TRUNCATION_ONLY_IN_BYPASS', len(byp841) == 1 and len(lay841) == 2 and all(id(n) in inside841 for n in lay841),
        len(lay841))
fin841 = [n for n in ast.walk(byp841[0]) if isinstance(n, ast.Try)] if byp841 else []
gate829('STATIC_TRUNCATION_RESTORED_IN_FINALLY', len(fin841) == 1 and
        any(ast.unparse(s) == 'model.model.layers = full' for s in fin841[0].finalbody))
# no assignment to any weight / parameter / embedding / norm attribute anywhere in the body
wr841 = sorted({ast.unparse(t) for n in ast.walk(body841t) if isinstance(n, (ast.Assign, ast.AugAssign))
                for t in (n.targets if isinstance(n, ast.Assign) else [n.target])
                if isinstance(t, (ast.Attribute, ast.Subscript)) and any(k in ast.unparse(t) for k in
                ('weight', 'embed_tokens', 'lm_head', '.norm', 'requires_grad'))})
gate829('STATIC_NO_WEIGHT_WRITES', not wr841, wr841)
# generation = locked TEST779 code (code objects compiled through the identical locked pipeline)
def code_sig841(co):
    return (co.co_code, co.co_names, co.co_varnames, co.co_argcount, co.co_kwonlyargcount, co.co_flags,
            tuple(code_sig841(c) if hasattr(c, 'co_code') else repr(c) for c in co.co_consts))
import inspect as _insp841
def cmp841(live, ref):
    return {'bytecode_and_constants': code_sig841(live) == code_sig841(ref), 'filename': live.co_filename == ref.co_filename,
            'first_line': live.co_firstlineno == ref.co_firstlineno, 'name': live.co_name == ref.co_name,
            'live_filename': live.co_filename}
fgu841 = _insp841.unwrap(free_generate)
LB841 = {'free_generate': cmp841(fgu841.__code__, REF779_841['free_generate'])}
LB841['free_generate']['defaults'] = fgu841.__defaults__ == FG_DEFAULTS841
for m_ in ('__init__', '__enter__', '__exit__'):
    LB841['AttentionIntervention.' + m_] = cmp841(getattr(AttentionIntervention, m_).__code__, REF779_841['AttentionIntervention.' + m_])
CUT3INFO841 = {m_: cmp841(getattr(Cut3Diagnostic, m_).__code__, REF779_841['Cut3Diagnostic.' + m_]) for m_ in ('__init__', '__enter__', '__exit__')}
D829['locked_bytecode841'] = {'gated': LB841, 'informational_Cut3Diagnostic': CUT3INFO841}
gate829('LOCKED_FREE_GENERATE_BYTECODE', all(v for k, v in LB841['free_generate'].items() if k != 'live_filename'), LB841['free_generate'])
gate829('LOCKED_ATTENTION_INTERVENTION_BYTECODE',
        all(all(v for k, v in LB841['AttentionIntervention.' + m_].items() if k != 'live_filename') for m_ in ('__init__', '__enter__', '__exit__')),
        {k: v for k, v in LB841.items() if k.startswith('Att')})
log829('TEST841_CUT3_BYTECODE_INFO', json.dumps({m_: v['bytecode_and_constants'] for m_, v in CUT3INFO841.items()}))
# exactly two free_generate call sites: the TEST827 answer frame and the fixed action frame, both of the question only;
# seed=None, gain=0., spans=None (greedy, no intervention)
calls841 = [n for n in ast.walk(body841t) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'free_generate']
def call_kind841(n):
    kw = {k.arg: k.value for k in n.keywords}
    base = (len(n.args) == 2 and isinstance(kw.get('seed'), ast.Constant) and kw['seed'].value is None and
            isinstance(kw.get('gain'), ast.Constant) and kw['gain'].value == 0 and
            isinstance(kw.get('spans'), ast.Constant) and kw['spans'].value is None and
            isinstance(n.args[1], ast.Call) and isinstance(n.args[1].func, ast.Name) and len(n.args[1].args) == 1 and
            ast.unparse(n.args[1].args[0]).startswith('QTEXT841['))
    return n.args[1].func.id if base else None
gate829('STATIC_GENERATION_CALLS_UNMODIFIED', len(calls841) == 2 and
        sorted(call_kind841(n) or '' for n in calls841) == ['action_prompt841', 'answer_prompt829'], len(calls841))
# the router consumes only tensors, the candidate list and the exclusion set (AST whitelist of free names)
def names841(fnames):
    fs = [n for n in body841t.body if isinstance(n, ast.FunctionDef) and n.name in fnames]
    return len(fs), {n.id for f_ in fs for n in ast.walk(f_) if isinstance(n, ast.Name)}
nr841, rnames841 = names841(('route841', 'peak50_841', 'unit841', 'route_mid841'))
gate829('STATIC_ROUTER_INPUTS', nr841 == 4 and rnames841 <= {
    'h_rows', 'bank', 'exclude', 'Q', 'K', 'S', 'fram', 'peak', 'cand', 'sc', 'idx', 'chosen', 't0', 'c', 'x', 'torch', 'math',
    'DEV', 'MU841', 'KEYS841', 'BETA841', 'PEAK_WEIGHT841', 'unit841', 'peak50_841', 'sorted', 'float', 'int', 'time', 'round',
    'len', 'zip', 'v', 'q_row', 'layer', 'MIDMU841', 'MIDKEYS841', 'route841', 'keys', 'mu', 'dict'}, sorted(rnames841))
# the re-entry echo sees only the mounted memory, the frame text and the model's own tensors (no label, no card list)
ne841, enames841 = names841(('echo841', 'direct841', 'index_embeds841', 'embed841'))
gate829('STATIC_ECHO_INPUTS', ne841 == 4 and enames841 <= {
    'mem', 'text', 'arm', 'h', 'z', 'ids', 'n', 'cache', 'caps', 'l', 'st', 'out', 'logits', 'last', 'rows', 'info', 't', 'p',
    'top', 'v', 'h79', 'cap79', 'pos', 'R', 't0', 'torch', 'model', 'DEV', 'DTYPE', 'H', 'NL', 'E841', 'RMS_E841', 'LENS841',
    'K_ECHO841', 'PREFILL841', 'IDXPRE841', 'IDXPOST841', 'prompt_ids', 'cache_build', 'DirectCut3', 'contextlib', 'direct841',
    'tok', 'kend', 'next', 'max',
    'embed841', 'COUNT834', 'list', 'len', 'int', 'float', 'round', 'time', 'dict', 'range', 'zip', 'RuntimeError', 'x', 'k',
    'lid', '_torch829'}, sorted(enames841))
DC3CMP841 = {m_: cmp841(getattr(DirectCut3, m_).__code__, REF_DC3_841[m_]) for m_ in ('__init__', '__enter__', '__exit__')}
gate829('LOCKED_DIRECTCUT3_BYTECODE', all(all(v for k, v in d.items() if k != 'live_filename') for d in DC3CMP841.values()), DC3CMP841)
gate829('V2_ADDRESSING_SOURCE_FACTS', all(v for k, v in V2FACTS841.items()
                                          if k not in ('v2_query_capture_used_forward_hooks', 'v2_candidate_stage_pca_faiss')), V2FACTS841)
D829['source_verification841'] = True
log829('TEST841_SOURCE_VERIFIED_BEFORE_MODEL_LOAD')
'''
SRCVER841_TEXT = SRCVER841
src841 = patch841(src841, "    del tok829\n", "\n".join("    " + l if l else "" for l in SRCVER841.strip("\n").splitlines()) +
                  "\n    del tok829\n" + PRECOST841)

HYP841 = {
    'question': ('After the first physical memory is read, can the relational information computed in the deep layers be '
                 'turned into the numerical address of the next physical memory without any external semantic decision '
                 'or oracle guidance?'),
    'engine_fact': ('730 initialize_native injects H3 at the layer-3 output and keeps the stored lower K/V: a layer-3 '
                    'injection never reaches layers 0..3 of any position. The only dynamic input of a layer-3 query is a '
                    'layer-0 input vector, so every feedback path is a map psi(deep state) -> layer-0 input.'),
    'arms': {'M2S': 'soft vocabulary re-entry: e = p^T E, p = softmax(logits) (no token emitted)',
             'M2H': 'hard vocabulary re-entry: e = E[argmax p] (equivalent to greedy tokens)',
             'D1': 'direct latent feedback: e = norm(h79) scaled to the mean embedding RMS (no vocabulary)',
             'CTRL840': 'control: TEST840 router on the question rows of the mounted state (unchanged)',
             'M1_Lx': 'diagnostic: last probe position at layer x vs card rows at layer x (keys forged from the same model)'},
    'pipeline': ('lookup frame (fixed) + assistant prefill "Next node:" over the mounted memory -> K=8 re-entry steps -> '
                 'the vectors before the model\'s own end token (same stop rule as free_generate) in the fixed index frame -> TEST840 bypass (layers 0..3 over NULL memory) -> H3 rows of the K '
                 'positions -> PEAK50 argmax over the bank minus mounted cartridges -> SHA-verified CUT3 mount.'),
    'sub_goals': {
        'IV1_STATE_CHANGE': 'final-layer state change by the first card (reported, offline).',
        'IV2_CONTENT_SPECIFIC': 'bridge-token rank (final layer) better with first than with NULL and with an irrelevant card.',
        'IV3_BRIDGE_SALIENCE': 'final-layer argmax after the prefill = first token of the bridge entity (first mounted).',
        'IV4_ADDRESS': 'R1: top-1 is an own card containing the bridge entity (second / changed / mirror).',
        'IV5_CAUSAL_SHIFT': 'SHIFT: with S->M\' the top-1 is the M\'-continuation, and with S->M an M-card.',
        'IV6_NEGATIVE': 'NULL / irrelevant / fork / decoy mounts do not produce an own M-card address.',
        'IV7_IDENTITY': 'new physical identities: same content selected.',
        'IV8_SOFT_VS_HARD': 'agreement, cosine and entropy of soft vs hard re-entry (reported).',
        'IV9_WRONG_FIRST': 'closed loop started from the fork: the model reaches a valid endpoint (L3).',
        'IV10_SUFFICIENCY': 'model action on designed states and closed loops with / without the continuation (L1, L2, ACT_*).'},
    'criteria': {
        'R1': 'designed first mounted: top-1 own second / changed / mirror in >= 9 of 12 (per arm). R1V (second / changed only) reported.',
        'SHIFT': 'top-1 own M\'-continuation with S->M\' mounted AND R1 hit with S->M mounted, in >= 9 of 12.',
        'NULLCTRL': 'NULL mount and unrelated-bank mount: top-1 is not an own M-card (nor the M\'-card) in >= 10 of 12 each.',
        'SPEC': 'fork mount and decoy mount: top-1 is not an own M-card in >= 10 of 12 each.',
        'ID': 'first mounted with new physical identities: same content as top-1 in >= 11 of 12.',
        'CONVERSION': 'R1 and SHIFT and NULLCTRL and SPEC PASS (per arm).',
        'FRAME_B': 'secondary: R1 and SHIFT counts with lookup frame B >= 9 of 12.',
        'I3': 'final-layer next-token argmax is the first token of the bridge entity with first mounted in >= 9 of 12.',
        'I2': 'bridge-token rank better with first than with NULL and than with the unrelated card in >= 10 of 12.',
        'L1_LIVE': 'closed loop, full bank, start NULL: model ANSWERs a valid endpoint with first + a continuation mounted, >= 9 of 12.',
        'L2_MISSING': 'closed loop, continuations absent: model ends with STOP or ANSWER = UNKNOWN (no entity), >= 9 of 12.',
        'L3_FORK': 'closed loop started from the fork: model ANSWERs a valid endpoint, >= 9 of 12.',
        'ACT': 'action word on designed states: NULL->SEARCH >= 10, first->SEARCH >= 10, first+second->ANSWER >= 10, '
               'S->M\'+second -> not ANSWER >= 9.',
        'H': 'answers: first+second END >= 10, second+first END >= 10, NULL UNKNOWN >= 10, S->M\'+second UNKNOWN >= 9.',
        'F': 'engineering: key-order max abs score diff <= 1e-5 with identical argmax; new identities keep content (ID).'},
    'decision': ('DEVAM if at least one main arm (M2S, M2H, D1) has CONVERSION PASS. DUR if every main arm FAILs both R1 '
                 'and SHIFT. Otherwise YETERSİZ KANIT. A budget stop forces YETERSİZ KANIT. Closed-loop results are '
                 'reported as separate verdicts and never upgrade an addressing result to cognition.'),
    'verdicts': {'LATENT_ADDRESS_CONVERSION': 'per arm from CONVERSION',
                 'MODEL_CHOSEN_ACTIONS_IN_FIXED_LOOP': 'L1 / L2 / L3 / ACT (model word applied literally; fixed vocabulary)',
                 'MODEL_NATIVE_COGNITIVE_CONTROL': ('at most PARTIAL: the action vocabulary, the loop, the router and the '
                                                    'budget are fixed by the experimenter; KORU vs DUZELT on conflicting '
                                                    'evidence is not measured'),
                 'AUTONOMOUS_RECURSIVE_REASONING': 'NOT_DEMONSTRATED (two-hop synthetic chains only)'},
    'classes': {'echo vectors, action word, answer text': 'A (model computation; applied literally)',
                'PEAK50 scores and argmax on GPU (H3, mid-layer diagnostic)': 'B (fixed engineering router, v2 rule, not tuned)',
                'mount / DROP unmount / exclusion of mounted cards / step budget / index frame': 'C (mechanical, fixed before run)'},
    'not_measured_deferred': ['KORU vs DUZELT when two mounted records conflict (both continuations present)',
                              'chains longer than two links; variable chain length', 'non-synthetic memories',
                              'model-generated action vocabulary (the four words are fixed by the experimenter)',
                              'model-native stopping without a fixed vocabulary']}

CLAIMS841 = {
    'verified_from_prior_research': [
        '840.log: bypass bitwise; designed first card -> second address 0/12 (top-1 always a remaining start-entity card); '
        'bridge shift 0/12; first+second answer END 12/12; NULL UNKNOWN 12/12; S->M\'+second UNKNOWN 8/12; live chain answers '
        'MIDDLE 6/12 (the model computes the bridge entity from the first card).',
        '836.log P1: isolated-pair relational interaction separates in the final-norm hidden 11/12, CUT3 0/12.',
        '838.log: final-hidden projection 0.94 vs CUT3 projection 0.43-0.46 (Python reader, class B); pair scan is class C.',
        '833.log: native KV recurrence B 4/24 vs reset A 4/24 vs rotated C 5/24 (FAIL).',
        '835.log: calibrated attention-head addressing with KV feedback 7/11 vs negative control 7 (FAIL).',
        '839.log: model-written Record-ID addresses FULL chain 11/48; selections dominated by start-entity cards.',
        'v2 656 (7B): Python-composed first-card + question H3 query found the second card 14/16 (external composition).'],
    'implemented_in_TEST841': ['three psi maps (M2S, M2H, D1) from the same probe; TEST840 router unchanged',
                               'diagnostic mid/upper-layer direct router with keys forged by the same model',
                               'model-chosen ANSWER / SEARCH / DROP / STOP closed loop with mechanical execution',
                               'offline logit lens of the bridge entity at 10 depths'],
    'demonstrated_by_TEST841': 'filled only from this run'}

# DirectCut3 reference: compiled exactly as the locked 779 extract_exact compiles the 730 symbols (never executed)
def ref_class_methods841(raw, label, names, cls):
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
REF_DC3_841 = ref_class_methods841(raw730_841, '730.py', ['DirectCut3', 'forge_native', 'initialize_native', 'to_gpu', 'seal_cp',
                                                         'memory_seals', 'compare_seals', 'safe_load', 'release'], 'DirectCut3')
assert set(REF_DC3_841) >= {'__init__', '__enter__', '__exit__'}, 'REF_DC3'

# ===== TEST841 PARÇA 2/3 — Colab'da aynı hücreye sırayla yapıştırın =====
BODY841 = r'''
D829['test'] = '841'
D829['controller'] = ('ENGINEERING ROUTER (fixed GPU PEAK50 argmax) over H3 rows of model-produced re-entry vectors; '
                      'model-chosen one-word actions applied literally in a fixed loop; mechanical mount / unmount / budget')
D829['sources841'] = {'829': LOCK829_841, '834': LOCK834_841, '779': LOCK779_841, '730': LOCK730_841, '757': LOCK757_841,
                      '839': LOCK839_841, '840': LOCK840_841, 'v2_610_sha256': LOCK610_841, 'v2_626': LOCK626_841,
                      'v2_627': LOCK627_841, 'helpers_sha256': HELPER_SHA841, 'v2_source_facts': V2FACTS841}
D829['hypotheses841'] = PANEL829['test841']['hypotheses']
D829['limitations'] = [
    'The router is a fixed GPU tensor argmax (v2 PEAK50); it is an engineering component, not model-native cognition.',
    'The lookup frame, the assistant prefill "Next node:", the index frame, K=8, the end-token row rule (the same stop rule '
    'as free_generate) and the four action words are fixed by the experimenter; they carry no name, answer or cartridge '
    'identity, but they are engineering priors.',
    'M2H is computationally greedy token decoding of the lookup reply; M2S differs from it only where the model\'s '
    'next-token distribution is not peaked; D1 has no trained interface to layer 0 (frozen weights, no training).',
    'Mounted cartridges are excluded from routing; DROP unmounts the last cartridge from the working set only (the SSD '
    'bank is append-only and unchanged); the step budget is mechanical and reported as BUDGET_STOP.',
    'Twelve sealed worlds, one card template, one question template, two lookup frames, one model, two-hop chains only.',
    'Answer text is produced with the TEST827 boundary instruction; answers are scored offline only.',
    'No GPU execution or result is claimed by the code author.']
gate829('SOURCE_VERIFICATION_DONE_BEFORE_MODEL_LOAD', bool(D829.get('source_verification841')))
gate829('PANEL_FRESH_SEED', SEED829 == SEED841, SEED829)
gate829('ENGINE829_CONTROLLER_TEXT_DISABLED', MAX_NEW_CONTROL829 == 0)
gate829('WORLD_COUNT', len(questions829) == WORLDS841 and len(QID841) == WORLDS841)
gate829('JOBS_UNIQUE', len({j['job'] for j in JOBS841}) == len(JOBS841), len(JOBS841))
gate829('CARTRIDGES_PHYSICAL', all(c in entries for j in JOBS841 for c in j['mount'] + j['bank'] + j['start']) and NULL829 in entries)
exec(compile(HELPER_SRC841, 'TEST841_LOCKED_HELPERS', 'exec'), globals())
gate829('HELPERS_LOADED', all(callable(globals().get(x)) for x in HELPERS841), HELPER_SHA841)
gate829('ENGINE_SYMBOLS841', all(callable(globals().get(x)) for x in
        ('build_fusion', 'kv_digest', 'safe_load', 'free_generate', 'answer_prompt829', 'DirectCut3', 'cache_build', 'prompt_ids')))
gate829('ARCH_DIMS', (NL, H, QH, KVH, HD) == EXPECTED_ARCH841 and int(model.config.num_attention_heads) == QH and
        int(model.config.num_key_value_heads) == KVH and int(model.config.hidden_size) == H and
        int(model.config.num_hidden_layers) == NL and len(model.model.layers) == NL, (NL, H, QH, KVH, HD))
gate829('BF16_COMPUTE', DTYPE == _torch829.bfloat16, str(DTYPE))
gate829('NF4_LINEAR4BIT', any(isinstance(m_, bitsandbytes.nn.Linear4bit) for m_ in model.modules()))
gate829('WEIGHTS_FROZEN', all(not p_.requires_grad for p_ in model.parameters()))
gate829('DEVICE', str(DEV).startswith(DEVICE_KIND841), str(DEV))
gate829('SDPA_MODULE', F is _torch829.nn.functional and F.scaled_dot_product_attention is SDPA829)
gate829('NO_RESIDUAL_HOOKS_START', all(not model.model.layers[i]._forward_hooks and not model.model.layers[i]._forward_pre_hooks
                                       for i in range(NL)))
gate829('PREFIX_P', P == 30, P)
POST841 = cost_upper841({c: int(entries[c]['body_tokens']) for c in cards829}, P)
D829['predicted_cost841'] = POST841
log829('TEST841_PREDICTED_COST', json.dumps(POST841))
gate829('PREDICTED_BUDGET_POST_LOAD', POST841['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN841,
        POST841['minutes_upper_excluding_model_load'])
QTEXT841 = {q['qid']: q['question'] for q in questions829}
# TEST840 router query frame (control arm), unchanged
QPRE841 = list(tok('\nQUESTION:\n', add_special_tokens=False).input_ids)
QPOST841 = list(tok('\n', add_special_tokens=False).input_ids)
QIDS841, QSPAN841 = {}, {}
for qid841, t841 in QTEXT841.items():
    body_ = list(tok(t841, add_special_tokens=False).input_ids)
    QIDS841[qid841] = QPRE841 + body_ + QPOST841
    QSPAN841[qid841] = (len(QPRE841), len(QPRE841) + len(body_))
PREFILL841 = list(tok(PREFILL_TXT841, add_special_tokens=False).input_ids)
IDXPRE841 = list(tok(IDXPRE_TXT841, add_special_tokens=False).input_ids)
IDXPOST841 = list(tok(IDXPOST_TXT841, add_special_tokens=False).input_ids)
LONGEST841 = max(len(prompt_ids(lookup_prompt841(t_, f_))) for t_ in QTEXT841.values() for f_ in ('A', 'B')) + len(PREFILL841) + K_ECHO841
gate829('FUSION_TOKENS', POST841['max_memory_tokens'] + max(LONGEST841, max(len(prompt_ids(action_prompt841(t_))) for t_ in QTEXT841.values())
                                                             + MAX_NEW_ANS841) + 128 <= MAX_FUSED_TOKENS,
        {'memory': POST841['max_memory_tokens'], 'longest_probe': LONGEST841})
try:
    free841, _ = _torch829.cuda.mem_get_info()
    gate829('VRAM_HEADROOM', free841 / 2**30 >= 8.0, round(free841 / 2**30, 2))
except Exception as e841:
    gate829('VRAM_HEADROOM', False, repr(e841))
D829['noninterference841'] = noninterference829([NULL829], questions829[0]['question'])
for k841, v841 in D829['noninterference841'].items():
    gate829('NONINTERFERENCE_' + k841.upper(), bool(v841), v841)
COUNT834 = {'fusion_forwards': fusion_forwards829([NULL829]), 'probe_forwards': 3, 'capture_forwards': 0,
            'rank_forwards': 0, 'generation_forwards': 1, 'mounts': 1, 'bypass_forwards': 0}
T0_841 = time.perf_counter()
SEAL_LAYERS834 = (0, CUT, NL // 2, NL - 1)

# ==================================================================================================================
# THE MODEL'S OWN INPUT / OUTPUT MATRICES (read only; never written: STATIC_NO_WEIGHT_WRITES)
# ==================================================================================================================
E841 = model.model.embed_tokens.weight
def ptr841(t_):
    return t_.data_ptr() if hasattr(t_, 'data_ptr') else id(t_)
VOCAB841 = int(model.config.vocab_size)
gate829('EMBEDDING_MATRIX', tuple(E841.shape) == (VOCAB841, H), {'shape': list(E841.shape), 'dtype': str(E841.dtype)})
acc841 = 0.0
for s0_841 in range(0, int(E841.shape[0]), 8192):
    blk841 = E841[s0_841:s0_841 + 8192].float()
    acc841 += float((blk841 * blk841).mean(dim=1).sqrt().sum())
    del blk841
RMS_E841 = acc841 / float(E841.shape[0])          # mean row RMS of the embedding matrix (label-free, weights only)
D829['io_matrices841'] = {'embedding_shape': list(E841.shape), 'embedding_dtype': str(E841.dtype),
                          'lm_head_weight_dtype': str(getattr(model.lm_head.weight, 'dtype', None)),
                          'tied_input_output': ptr841(model.lm_head.weight) == ptr841(E841),
                          'mean_embedding_row_rms': RMS_E841}
log829('TEST841_IO_MATRICES', json.dumps(D829['io_matrices841']))
gate829('EMBEDDING_RMS_FINITE', math.isfinite(RMS_E841) and RMS_E841 > 0, RMS_E841)
def embed841(ids):
    return model.model.embed_tokens(torch.tensor(list(ids), device=DEV))
def direct841(h):
    z = model.model.norm(h.to(DEV).to(DTYPE).reshape(1, 1, H)).reshape(-1).float()
    return (z * (RMS_E841 / (z * z).mean().sqrt().clamp_min(1e-9))).to(DTYPE)
def index_embeds841(R):
    return torch.cat([embed841(IDXPRE841), R.to(DTYPE), embed841(IDXPOST841)], dim=0)

# ==================================================================================================================
# SELECTIVE BYPASS (TEST840): the model's own embedding / rotary / mask / decoder layers 0..3 over the mounted lower K/V.
# Input either token ids or layer-0 input vectors (inputs_embeds); layers 4..79 and lm_head are not executed.
# ==================================================================================================================
ORIG_LAYERS841 = model.model.layers
ORIG_LAYER_IDS841 = [id(x) for x in ORIG_LAYERS841]
FWDREF841 = [ORIG_LAYERS841[i].forward for i in range(NL)] + [model.lm_head.forward]   # identity reference
class CallCount841:
    """Observation-only instance-method replacement on every decoder layer and lm_head (never a hook); counts calls."""
    def __init__(self):
        self.n = {}; self.saved = []
    def __enter__(self):
        mods = [('L%d' % i, ORIG_LAYERS841[i]) for i in range(NL)] + [('HEAD', model.lm_head)]
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
def h3_bypass841(mem, ids=None, embeds=None):
    n = int(mem[0][0].shape[-2])
    cache = cache_build(list(mem[:CUT + 1]))
    L = len(ids) if embeds is None else int(embeds.shape[0])
    pos = torch.arange(n, n + L, device=DEV)
    inp = ({'input_ids': torch.tensor([ids], device=DEV)} if embeds is None else
           {'inputs_embeds': embeds.to(DTYPE).reshape(1, L, H)})
    cap = []
    t0 = time.perf_counter()
    full = model.model.layers
    if full is not ORIG_LAYERS841 or len(full) != NL:
        raise RuntimeError('LAYERS_NOT_ORIGINAL')
    try:
        model.model.layers = torch.nn.ModuleList(list(full)[:CUT + 1])
        with torch.no_grad():
            with DirectCut3(full[CUT], 'capture', collector=cap):
                out = model.model(past_key_values=cache, attention_mask=torch.ones((1, n + L), device=DEV, dtype=torch.long),
                                  position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True, **inp)
                del out
    finally:
        model.model.layers = full
    if model.model.layers is not ORIG_LAYERS841 or [id(x) for x in model.model.layers] != ORIG_LAYER_IDS841:
        raise RuntimeError('LAYERS_NOT_RESTORED')
    _torch829.cuda.synchronize()
    COUNT834['bypass_forwards'] += 1
    if len(cap) != 1:
        raise RuntimeError('BYPASS_CAPTURE_COUNT')
    h = cap[0][0]
    del cache, cap
    return h, round((time.perf_counter() - t0) * 1000.0, 3)
def h3_full841(mem, ids):
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

# ==================================================================================================================
# LATENT RE-ENTRY ECHO. One probe forward of the full model over the mounted memory (fixed lookup frame + fixed
# assistant prefill), then K-1 single-position forwards whose layer-0 input is psi(previous step):
#   M2S: softmax(logits)^T E      M2H: E[argmax logits]      D1: norm(h79) rescaled to the mean embedding RMS.
# Returns the K vectors, the per-step next-token summary, and the step-0 last-position states of LENS841 layers.
# ==================================================================================================================
def echo841(mem, text, arm):
    ids = list(prompt_ids(text)) + list(PREFILL841)
    n = int(mem[0][0].shape[-2])
    cache = cache_build(list(mem))
    caps = {l: [] for l in LENS841}
    t0 = time.perf_counter()
    pos = torch.arange(n, n + len(ids), device=DEV)
    with torch.no_grad():
        with contextlib.ExitStack() as st:
            for l in LENS841:
                st.enter_context(DirectCut3(model.model.layers[l], 'capture', collector=caps[l]))
            out = model(input_ids=torch.tensor([ids], device=DEV), past_key_values=cache,
                        attention_mask=torch.ones((1, n + len(ids)), device=DEV, dtype=torch.long),
                        position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
            logits = out.logits[0, -1].float()
            del out
    COUNT834['probe_forwards'] += 1
    last = {l: caps[l][0][0, -1, :].float() for l in LENS841}
    h79 = last[NL - 1].to(DEV)
    rows, info = [], []
    for t in range(K_ECHO841):
        p = torch.softmax(logits, dim=-1)
        top = torch.topk(p, 5)
        info.append({'top_ids': [int(x) for x in top.indices.tolist()], 'top_p': [round(float(x), 6) for x in top.values.tolist()],
                     'entropy': float(-(p * p.clamp_min(1e-30).log()).sum())})
        if arm == 'M2S':
            v = (p.to(E841.dtype).reshape(1, -1) @ E841).reshape(-1)
        elif arm == 'M2H':
            v = E841[int(torch.argmax(p))]
        elif arm == 'D1':
            v = direct841(h79)
        else:
            raise RuntimeError('UNKNOWN_ARM')
        rows.append(v.to(DTYPE))
        if t + 1 < K_ECHO841:
            cap79 = []
            x = n + len(ids) + t
            with torch.no_grad():
                with DirectCut3(model.model.layers[NL - 1], 'capture', collector=cap79):
                    out = model(inputs_embeds=v.to(DTYPE).reshape(1, 1, H), past_key_values=cache,
                                attention_mask=torch.ones((1, x + 1), device=DEV, dtype=torch.long),
                                position_ids=torch.tensor([[x]], device=DEV), cache_position=torch.tensor([x], device=DEV),
                                use_cache=True, return_dict=True)
                    logits = out.logits[0, -1].float()
                    del out
            COUNT834['generation_forwards'] += 1
            h79 = cap79[0][0, -1, :].float().to(DEV)
    R = torch.stack(rows)
    # rows from the first step whose argmax is the model's own end token are not indexed (free_generate's stop rule)
    kend = max(1, next((t for t in range(len(info)) if info[t]['top_ids'][0] == int(tok.eos_token_id)), K_ECHO841))
    del cache, caps
    _torch829.cuda.synchronize()
    return R, info, last, round((time.perf_counter() - t0) * 1000.0, 3), kend

# ---- physical H3 key bank (SHA-verified cartridges; v2 rank-0 store fit: centering + unit norm) ----
KEYROWS841 = {}
t_keys841 = time.perf_counter()
for cid841 in ALLBANK841:
    cp841 = safe_load(entries[cid841])                     # locked: file SHA, cartridge ID and every tensor SHA verified
    KEYROWS841[cid841] = cp841['h'][0, P:, :].to(DEV).float()
    del cp841
gate829('KEY_ROWS_SHAPE', all(v.ndim == 2 and v.shape[1] == H and v.shape[0] >= 4 for v in KEYROWS841.values()), len(KEYROWS841))
MU841 = torch.cat([KEYROWS841[c] for c in ALLBANK841], dim=0).mean(dim=0)   # label-free store mean (v2 transform_fit rank 0)
def unit841(x):
    return x / x.norm(dim=-1, keepdim=True).clamp_min(1e-9)
KEYS841 = {c: unit841(v - MU841) for c, v in KEYROWS841.items()}
VPAIR841 = [(B['v0'][i], B['v1'][i]) for B in BANKS841 for i in range(len(B['v0']))]   # same content, new identity
D829['key_bank841'] = {'cartridges': len(KEYS841), 'rows': int(sum(v.shape[0] for v in KEYS841.values())),
                       'load_seconds': round(time.perf_counter() - t_keys841, 3),
                       'v1_keys_bitwise_identical_to_v0': [sum(1 for a_, b_ in VPAIR841 if torch.equal(KEYROWS841[a_], KEYROWS841[b_])),
                                                           len(VPAIR841)]}
# ---- diagnostic mid/upper-layer key bank: the same model run once over each card exactly as the forge did ----
KEYLAYERS841 = sorted(set(MID841) | {CUT})
def keyforge841(cid):
    ids = list(PIDS) + list(tok(cards829[cid], add_special_tokens=False).input_ids)
    caps = {l: [] for l in KEYLAYERS841}
    pos = torch.arange(0, len(ids), device=DEV)
    with torch.no_grad():
        with contextlib.ExitStack() as st:
            for l in KEYLAYERS841:
                st.enter_context(DirectCut3(model.model.layers[l], 'capture', collector=caps[l]))
            out = model.model(input_ids=torch.tensor([ids], device=DEV), attention_mask=torch.ones((1, len(ids)), device=DEV, dtype=torch.long),
                              position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
            del out
    COUNT834['probe_forwards'] += 1
    return {l: caps[l][0][0, P:, :] for l in KEYLAYERS841}, len(ids) - P
MIDROWS841 = {l: {} for l in MID841}
KF841 = {'h3_bitwise': 0, 'h3_max_rel': 0.0, 'n': 0}
t_mid841 = time.perf_counter()
for cid841 in ALLBANK841:
    rr841, nb841 = keyforge841(cid841)
    gate829('MEAS_KEYFORGE_TOKENS_' + cid841, nb841 == int(entries[cid841]['body_tokens']), nb841)
    ref841 = KEYROWS841[cid841].float().cpu()
    KF841['h3_bitwise'] += int(torch.equal(rr841[CUT].float(), ref841))
    KF841['h3_max_rel'] = max(KF841['h3_max_rel'], float((rr841[CUT].float() - ref841).abs().max()) /
                              max(float(ref841.abs().max()), 1e-9))
    KF841['n'] += 1
    for l841 in MID841:
        MIDROWS841[l841][cid841] = rr841[l841].to(DEV).float()
    del rr841, ref841
MIDMU841 = {l: torch.cat([MIDROWS841[l][c] for c in ALLBANK841], dim=0).mean(dim=0) for l in MID841}
MIDKEYS841 = {l: {c: unit841(MIDROWS841[l][c] - MIDMU841[l]) for c in ALLBANK841} for l in MID841}
del MIDROWS841
KF841['seconds'] = round(time.perf_counter() - t_mid841, 3)
KF841['context_matches_forge'] = KF841['h3_max_rel'] <= 1e-2     # diagnostic validity of M1 (non-fatal by design)
D829['mid_key_bank841'] = KF841
log829('TEST841_MID_KEY_BANK', json.dumps(KF841))
def peak50_841(Q, K):
    S = (Q @ K.T).double()
    fram = ((torch.logsumexp(S * BETA841, dim=1) - math.log(S.shape[1])) / BETA841).mean()
    peak = S.max(dim=1).values.mean()
    return (1.0 - PEAK_WEIGHT841) * fram + PEAK_WEIGHT841 * peak
def route841(h_rows, bank, exclude):
    t0 = time.perf_counter()
    Q = unit841(h_rows.to(DEV).float() - MU841)
    cand = sorted(c for c in bank if c not in exclude)       # mechanical: never re-address a mounted cartridge
    sc = torch.stack([peak50_841(Q, KEYS841[c]) for c in cand])
    idx = int(torch.argmax(sc).item())                        # first maximum = smallest cartridge ID (v2 tie rule)
    chosen = cand[idx]
    return {'chosen': chosen, 'scores': {c: float(v) for c, v in zip(cand, sc.tolist())},
            'route_ms': round((time.perf_counter() - t0) * 1000.0, 3)}
def route_mid841(q_row, layer, bank, exclude):
    t0 = time.perf_counter()
    Q = unit841(q_row.to(DEV).float().reshape(1, -1) - MIDMU841[layer])
    cand = sorted(c for c in bank if c not in exclude)
    sc = torch.stack([peak50_841(Q, MIDKEYS841[layer][c]) for c in cand])
    idx = int(torch.argmax(sc).item())
    chosen = cand[idx]
    return {'chosen': chosen, 'scores': {c: float(v) for c, v in zip(cand, sc.tolist())},
            'route_ms': round((time.perf_counter() - t0) * 1000.0, 3)}
def qrows841(h, qid):
    a, b = QSPAN841[qid]
    return h[a:b, :]

# ---- NULL memory (no relation), mounted once and kept ----
MEMNULL841, NNULL841 = mount834([NULL829], 'NULL')
SEALNULL841 = seal834(MEMNULL841)

# ---- VERIFICATION: bypass = full forward (ids and embeddings paths); call counts; echo runs the full model ----
qv841 = QID841[0]
with CallCount841() as cc841:
    hb841, msb841 = h3_bypass841(MEMNULL841, ids=QIDS841[qv841])
CC_BYPASS841 = cc841.summary()
with CallCount841() as cc841:
    hf841, msf841 = h3_full841(MEMNULL841, QIDS841[qv841])
CC_FULL841 = cc841.summary()
with CallCount841() as cc841:
    he841, mse841 = h3_bypass841(MEMNULL841, embeds=embed841(QIDS841[qv841]))
CC_EMB841 = cc841.summary()
d841 = float((hb841.float() - hf841.float()).abs().max().item()); s841 = float(hf841.float().abs().max().item())
de841 = float((he841.float() - hb841.float()).abs().max().item())
JB841 = next(j for j in JOBS841 if j['kind'] == 'STATE' and j['mount'] != [NULL829])
mem2_841, n2_841 = mount834([JB841['mount'][0]], 'EQUIV_CARD')
hb2_841, msb2_841 = h3_bypass841(mem2_841, ids=QIDS841[qv841]); hf2_841, msf2_841 = h3_full841(mem2_841, QIDS841[qv841])
d2_841 = float((hb2_841.float() - hf2_841.float()).abs().max().item())
del mem2_841; gc.collect(); release()
with CallCount841() as cc841:
    Rv841, iv841, lv841, msv841, kv841 = echo841(MEMNULL841, lookup_prompt841(QTEXT841[qv841], 'A'), 'M2H')
CC_ECHO841 = cc841.summary()
Rv2_841, iv2_841, _, _, _ = echo841(MEMNULL841, lookup_prompt841(QTEXT841[qv841], 'A'), 'M2H')
D829['bypass_verification841'] = {
    'null_memory': {'bitwise': bool(torch.equal(hb841, hf841)), 'max_abs': d841, 'scale': s841,
                    'bypass_ms': msb841, 'full_forward_ms': msf841},
    'one_card_memory': {'bitwise': bool(torch.equal(hb2_841, hf2_841)), 'max_abs': d2_841,
                        'bypass_ms': msb2_841, 'full_forward_ms': msf2_841},
    'embeds_path': {'bitwise_vs_ids_path': bool(torch.equal(he841, hb841)), 'max_abs': de841, 'bypass_ms': mse841},
    'calls_bypass': CC_BYPASS841, 'calls_full': CC_FULL841, 'calls_embeds_bypass': CC_EMB841, 'calls_echo': CC_ECHO841,
    'echo_deterministic_hard': bool(torch.equal(Rv841, Rv2_841)) and iv841 == iv2_841, 'echo_ms': msv841,
    'h3_dtype': str(hb841.dtype), 'h3_shape': list(hb841.shape)}
log829('TEST841_BYPASS_VERIFICATION', json.dumps(D829['bypass_verification841']))
gate829('BYPASS_H3_EQUALS_FULL_FORWARD_H3', d841 <= BYPASS_TOL841 * max(s841, 1e-9) and d2_841 <= BYPASS_TOL841 * max(s841, 1e-9),
        D829['bypass_verification841'])
gate829('BYPASS_EMBEDS_PATH_EQUALS_IDS_PATH', de841 <= BYPASS_TOL841 * max(s841, 1e-9), de841)
gate829('BYPASS_SKIPS_UPPER_LAYERS_AND_LM_HEAD', all(c_['lower_calls'] == [1] * (CUT + 1) and c_['upper_max'] == 0 and
                                                     c_['lm_head'] == 0 for c_ in (CC_BYPASS841, CC_EMB841)),
        [CC_BYPASS841, CC_EMB841])
gate829('FULL_FORWARD_RUNS_ALL_LAYERS', CC_FULL841['lower_calls'] == [1] * (CUT + 1) and CC_FULL841['upper_min'] == 1 and
        CC_FULL841['upper_max'] == 1 and CC_FULL841['lm_head'] == 1, CC_FULL841)
gate829('ECHO_RUNS_FULL_MODEL_EACH_STEP', CC_ECHO841['lower_calls'] == [K_ECHO841] * (CUT + 1) and
        CC_ECHO841['upper_min'] == K_ECHO841 and CC_ECHO841['upper_max'] == K_ECHO841 and CC_ECHO841['lm_head'] == K_ECHO841,
        CC_ECHO841)
gate829('ECHO_SHAPE', tuple(Rv841.shape) == (K_ECHO841, H) and len(iv841) == K_ECHO841, list(Rv841.shape))
gate829('LAYERS_RESTORED', model.model.layers is ORIG_LAYERS841 and len(model.model.layers) == NL)
gate829('NULL_MEMORY_UNCHANGED', seal834(MEMNULL841) == SEALNULL841)

# ---- ENGINEERING INVARIANCE (F): key concatenation order ----
def batched_scores841(Q, bank):
    K = torch.cat([KEYS841[c] for c in bank], dim=0)
    S = (Q @ K.T).double(); out = {}; s0 = 0
    for c in bank:
        m = KEYS841[c].shape[0]; Sc = S[:, s0:s0 + m]; s0 += m
        out[c] = float((1.0 - PEAK_WEIGHT841) * ((torch.logsumexp(Sc * BETA841, dim=1) - math.log(m)) / BETA841).mean() +
                       PEAK_WEIGHT841 * Sc.max(dim=1).values.mean())
    return out
Qv841 = unit841(qrows841(hb841, qv841).to(DEV).float() - MU841)
fw841 = batched_scores841(Qv841, JB841['bank']); bw841 = batched_scores841(Qv841, list(reversed(JB841['bank'])))
lp841 = route841(qrows841(hb841, qv841), JB841['bank'], set())['scores']
F_ORDER841 = max(max(abs(fw841[c] - bw841[c]) for c in fw841), max(abs(fw841[c] - lp841[c]) for c in fw841))
amx841 = lambda d_: sorted(d_, key=lambda c: (-d_[c], c))[0]
F_ARGMAX841 = amx841(fw841) == amx841(bw841) == amx841(lp841)
D829['invariance841'] = {'order_max_abs_score_diff': F_ORDER841, 'same_argmax': F_ARGMAX841}
del hb841, hf841, he841, hb2_841, hf2_841, Rv841, Rv2_841

# ---- per-job record store (SHA-256 manifest; job-level resume) ----
EDIR841 = DIR829 / 'TEST841_jobs'
EDIR841.mkdir(exist_ok=True)
MAN841 = DIR829 / 'TEST841_job_manifest.jsonl'
HEADER841 = {'panel_sha256': PANEL_SHA829, 'body_sha256': PANEL829['test841']['body_sha256'], 'helpers_sha256': HELPER_SHA841}
REC841, ROWS841 = {}, {}
D829['resume841'] = {'enabled': RESUME841, 'source': None, 'reused_jobs': 0, 'reason': None}
if RESUME841:
    for cand in sorted(DIR829.parent.glob('TEST841_*/TEST841_job_manifest.jsonl'), reverse=True):
        if cand.parent == DIR829:
            continue
        try:
            lines = cand.read_text(encoding='utf-8').splitlines()
            if not lines or json.loads(lines[0]).get('header') != HEADER841:
                D829['resume841']['reason'] = 'header mismatch in ' + str(cand); continue
            got, gotr = {}, {}
            for ln in lines[1:]:
                o = json.loads(ln); fj = cand.parent / 'TEST841_jobs' / o['json']; fn = cand.parent / 'TEST841_jobs' / o['npz']
                if fj.exists() and fn.exists() and sha_file(fj) == o['json_sha256'] and sha_file(fn) == o['npz_sha256']:
                    got[o['key']] = json.loads(fj.read_text(encoding='utf-8'))
                    with np.load(fn, allow_pickle=False) as z:
                        gotr[o['key']] = {k: np.array(z[k], copy=True) for k in z.files}
            REC841.update(got); ROWS841.update(gotr)
            D829['resume841'].update({'source': str(cand), 'reused_jobs': len(got), 'reason': 'header and per-file SHA-256 verified'})
            break
        except Exception as e841r:
            D829['resume841']['reason'] = 'unreadable ' + str(cand) + ' ' + repr(e841r)
log829('TEST841_RESUME', json.dumps(D829['resume841']))
with MAN841.open('w', encoding='utf-8') as fh841:
    fh841.write(json.dumps({'header': HEADER841}, sort_keys=True) + '\n')
def save_job841(key, rec, rows):
    fj = EDIR841 / (key + '.json'); fn = EDIR841 / (key + '.npz')
    fj.write_text(json.dumps(rec, sort_keys=True), encoding='utf-8')
    np.savez(fn, **rows)
    with MAN841.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps({'key': key, 'json': fj.name, 'npz': fn.name, 'json_sha256': sha_file(fj),
                             'npz_sha256': sha_file(fn)}, sort_keys=True) + '\n')
for k841 in list(REC841):
    save_job841(k841, REC841[k841], ROWS841.get(k841, {}))

# ==================================================================================================================
# RUNTIME. Jobs are opaque. The router sees only H3 rows, a candidate list and the mounted (excluded) cartridges; the
# echo sees only the mounted memory and a fixed frame; actions are the model's own first word, applied literally.
# ==================================================================================================================
BUDGET_STOP841 = False
def mem_for841(mount, tag):
    if list(mount) == [NULL829]:
        return MEMNULL841, False, 0.0
    t0 = time.perf_counter()
    memx, n = mount834(list(mount), tag)
    return memx, True, round((time.perf_counter() - t0) * 1000.0, 3)
def gen_answer841(memx, qid):
    o = free_generate(memx, answer_prompt829(QTEXT841[qid]), seed=None, gain=0., max_new=MAX_NEW_ANS841, spans=None)
    COUNT834['generation_forwards'] += int(o['generated_tokens'])
    return o
def gen_action841(memx, qid):
    o = free_generate(memx, action_prompt841(QTEXT841[qid]), seed=None, gain=0., max_new=MAX_NEW_ACT841, spans=None)
    COUNT834['generation_forwards'] += int(o['generated_tokens'])
    return o
def parse_action841(raw):
    m = re.match(r'\s*([A-Za-z]+)', raw or '')
    w = m.group(1).upper() if m else ''
    return w if w in ACTIONS841 else 'INVALID'                # literal: no synonym, no repair, no second guess
def address841(memx, qid, frame, arm, bank, exclude):
    R, info, last, ms, kend = echo841(memx, lookup_prompt841(QTEXT841[qid], frame), arm)
    hi, msi = h3_bypass841(MEMNULL841, embeds=index_embeds841(R[:kend]))     # address depends on memory only via the echo
    qr = hi[len(IDXPRE841):len(IDXPRE841) + kend]
    r = route841(qr, bank, exclude)
    r.update({'echo_ms': ms, 'index_ms': msi, 'indexed_rows': kend})
    return r, info, last, R, qr
def answer841(cards, qid, tag):
    t0 = time.perf_counter()
    memx, tmp, mount_ms = mem_for841(cards, tag)
    t1 = time.perf_counter()
    seal = seal834(memx)
    o = gen_answer841(memx, qid)
    gate829('MEAS_KV_SEAL_' + tag, seal834(memx) == seal)
    del memx
    if tmp:
        gc.collect(); release()
    return {'raw': o['raw'], 'generated_tokens': int(o['generated_tokens']), 'mount_ms': mount_ms,
            'answer_ms': round((time.perf_counter() - t1) * 1000.0, 3), 'mount': list(cards)}
def state_job841(j, tag):
    mount = list(j['mount']); q = j['qid']; bank = j['bank']; ex = set(mount)
    memx, tmp, mount_ms = mem_for841(mount, tag)
    seal = seal834(memx)
    hq, msq = h3_bypass841(memx, ids=QIDS841[q])
    rec = {'job': j['job'], 'kind': 'STATE', 'frame': j['frame'], 'mount_ms': mount_ms, 'arms': {}, 'step0_equal': []}
    rec['arms']['CTRL840'] = dict(route841(qrows841(hq, q), bank, ex), bypass_ms=msq)
    rows = {}
    last0 = None
    for arm in ARMS841:
        r, info, last, R, qr = address841(memx, q, j['frame'], arm, bank, ex)
        rec['arms'][arm] = dict(r, echo=info)
        if arm == 'D1':
            rec['arms']['D1_1'] = route841(qr[:1], bank, ex)
        rows[arm + '_vec'] = R.float().cpu().numpy().astype(np.float32)
        rows[arm + '_h3q'] = qr.float().cpu().numpy().astype(np.float32)
        if last0 is None:
            last0 = last; rec['step0_top'] = info[0]
        else:
            rec['step0_equal'].append(info[0]['top_ids'] == rec['step0_top']['top_ids'] and info[0]['top_p'] == rec['step0_top']['top_p'])
    for l in MID841:
        rec['arms']['M1_L%d' % l] = route_mid841(last0[l], l, bank, ex)
    rows['lens_last'] = torch.stack([last0[l] for l in LENS841]).numpy().astype(np.float32)
    gate829('MEAS_KV_SEAL_' + tag, seal834(memx) == seal)
    del memx
    if tmp:
        gc.collect(); release()
    return rec, rows
def action_job841(j, tag):
    memx, tmp, mount_ms = mem_for841(j['mount'], tag)
    seal = seal834(memx)
    o = gen_action841(memx, j['qid'])
    gate829('MEAS_KV_SEAL_' + tag, seal834(memx) == seal)
    del memx
    if tmp:
        gc.collect(); release()
    return {'job': j['job'], 'kind': 'ACTION', 'raw': o['raw'], 'action': parse_action841(o['raw']),
            'generated_tokens': int(o['generated_tokens']), 'mount_ms': mount_ms}
def loop_job841(j, tag):
    q = j['qid']; arm = j['arm']; bank = j['bank']
    work = list(j['start']); dropped = []; steps = []; end = None; ans = None
    for t in range(T_MAX841):
        mount = list(work) if work else [NULL829]
        memx, tmp, mount_ms = mem_for841(mount, tag + '_%d' % t)
        seal = seal834(memx)
        o = gen_action841(memx, q)
        act = parse_action841(o['raw'])
        st = {'t': t, 'mounted': mount, 'action_raw': o['raw'], 'action': act, 'mount_ms': mount_ms}
        if act == 'ANSWER':
            a = gen_answer841(memx, q); ans = a['raw']; end = 'MODEL_ANSWER'
        elif act == 'STOP':
            end = 'MODEL_STOP'
        elif act == 'DROP':
            st['dropped'] = work.pop() if work else None          # working set only; the SSD bank is append-only
            if st['dropped'] is not None:
                dropped.append(st['dropped'])
        elif act == 'SEARCH':
            ex = set(work) | set(dropped)
            if not [c for c in bank if c not in ex]:
                end = 'NO_CANDIDATES'
            else:
                r, info, last, R, qr = address841(memx, q, 'A', arm, bank, ex)
                st['route'] = r; st['echo'] = info
                work.append(r['chosen'])                               # mechanical application of the routed address
        else:
            end = 'INVALID_ACTION'
        gate829('MEAS_KV_SEAL_' + tag + '_%d' % t, seal834(memx) == seal)
        del memx
        if tmp:
            gc.collect(); release()
        steps.append(st)
        if end is not None:
            break
    if end is None:
        end = 'BUDGET_STOP'                                            # mechanical; never reported as a model decision
    return {'job': j['job'], 'kind': 'LOOP', 'arm': arm, 'steps': steps, 'end': end, 'answer_raw': ans,
            'final_mounted': work, 'dropped': dropped}
UPPER_CHECK841 = {}
t_run841 = time.perf_counter()
nj841 = len(JOBS841); step841 = max(1, nj841 // 8)
log829('TEST841_PROGRESS', 'JOBS', 0, '/', nj841)
for ji841, j841 in enumerate(JOBS841):
    jj = j841['job']
    if jj not in REC841:
        if (time.perf_counter() - T0_841) / 60.0 > HARD_BUDGET_MIN841:
            BUDGET_STOP841 = True; log829('TEST841_BUDGET_STOP', 'job', ji841, 'of', nj841); break
        if j841['kind'] == 'STATE':
            rec, rows = state_job841(j841, 'S_' + jj)
        elif j841['kind'] == 'ANSWER':
            if not UPPER_CHECK841:
                with CallCount841() as ccu:
                    a = answer841(j841['mount'], j841['qid'], 'A_' + jj)
                UPPER_CHECK841 = ccu.summary()
                gate829('CUT3_MOUNT_AND_ANSWER_RUN_UPPER_LAYERS', UPPER_CHECK841['upper_min'] >= 1 and UPPER_CHECK841['lm_head'] >= 1,
                        UPPER_CHECK841)
            else:
                a = answer841(j841['mount'], j841['qid'], 'A_' + jj)
            rec, rows = {'job': jj, 'kind': 'ANSWER', 'answer': a}, {}
        elif j841['kind'] == 'ACTION':
            rec, rows = action_job841(j841, 'C_' + jj), {}
        else:
            rec, rows = loop_job841(j841, 'L_' + jj), {}
        REC841[jj] = rec; ROWS841[jj] = rows; save_job841(jj, rec, rows)
    if (ji841 + 1) % step841 == 0 or ji841 + 1 == nj841:
        log829('TEST841_PROGRESS', 'JOBS', ji841 + 1, '/', nj841)
D829['run_seconds841'] = round(time.perf_counter() - t_run841, 3)
D829['upper_layer_check841'] = UPPER_CHECK841
D829['budget_stop841'] = BUDGET_STOP841
gate829('NULL_MEMORY_UNCHANGED_FINAL', seal834(MEMNULL841) == SEALNULL841)
del MEMNULL841; gc.collect(); release()

engine_bindings829('FINAL')
gate829('FROZEN_WEIGHT_SENTINEL', before829 == sentinel())
gate829('LAYERS_RESTORED_FINAL', model.model.layers is ORIG_LAYERS841 and [id(x) for x in model.model.layers] == ORIG_LAYER_IDS841)
gate829('NO_RESIDUAL_HOOKS', all(not model.model.layers[i]._forward_hooks and not model.model.layers[i]._forward_pre_hooks
                                 for i in range(NL)))
gate829('NO_ATTENTION_HOOKS', all(not model.model.layers[i].self_attn._forward_hooks and
                                  not model.model.layers[i].self_attn._forward_pre_hooks for i in range(NL)))
gate829('LAYER_FORWARDS_RESTORED', all(model.model.layers[i].forward == FWDREF841[i] for i in range(NL)) and
        model.lm_head.forward == FWDREF841[NL])
gate829('SDPA_RESTORED_FINAL', F.scaled_dot_product_attention is SDPA829)
gate829('LM_HEAD_UNWRAPPED', model.lm_head.__dict__.get('forward') is HEAD_FWD829 and
        not model.lm_head._forward_hooks and not model.lm_head._forward_pre_hooks)
gate829('EMBEDDING_UNCHANGED_OBJECT', model.model.embed_tokens.weight is E841)
gate829('PANEL_UNCHANGED', sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True)) == PANEL_SHA829)
for cid841 in cards829:
    gate829('FINAL_SHA_' + cid841, sha_file(CART_DIR / entries[cid841]['file']) == entries[cid841]['sha256'])
COUNT_NUMERIC841 = dict(COUNT834)
gate829('COUNTED_WITHIN_UPPER_BOUND', all(COUNT_NUMERIC841.get(k, 0) <= POST841['numeric_upper'][k] for k in POST841['numeric_upper']),
        {'counted': COUNT_NUMERIC841, 'upper': POST841['numeric_upper']})

# ====== OFFLINE PHASE MARKER ======
# OFFLINE PHASE: every routing pass, echo, action and answer is finished and saved; roles are read only from here.
log829('TEST841_OFFLINE_START')
def ok841(k, n, need, full):
    return 'INCONCLUSIVE' if n < full else ('PASS' if k >= need else 'FAIL')
def role841(cid, wi):
    if cid == NULL829:
        return 'NULL'
    if cid not in CONTENT841:
        return 'OTHER'
    cw, k, ver = CONTENT841[cid]
    return ('OWN_' if cw == wi else 'OTHER_') + k.upper()
MCARD841 = ('OWN_SECOND', 'OWN_CHANGED', 'OWN_MIRROR')
VALID841 = ('OWN_SECOND', 'OWN_CHANGED')
def rank841(scores, cids):
    order = sorted(scores, key=lambda c: (-scores[c], c))
    rs = [order.index(c) + 1 for c in cids if c in scores]
    return min(rs) if rs else None
def tcls841(t, w):
    u = (t or '').upper()
    names = [nm for nm, c in (('END', w['end']), ('ALT_END', w['changed_end']), ('MIDDLE', w['middle']), ('START', w['start']),
                              ('FORK_END', w['fork_end']), ('DECOY', w['decoy_end']), ('BRIDGE_MID', w['bridge_mid']),
                              ('BRIDGE_END', w['bridge_end'])) if c in u]
    return names + (['UNKNOWN'] if 'UNKNOWN' in u else [])
def tcat841(cls):
    if not cls:
        return 'EMPTY_OR_OTHER'
    if cls == ['UNKNOWN']:
        return 'UNKNOWN'
    if 'UNKNOWN' in cls:
        return 'MIXED'
    return cls[0] if len(cls) == 1 else 'MULTI:' + '+'.join(cls)
def tid841(name):
    return int(tok(' ' + name, add_special_tokens=False).input_ids[0])
def dist841(xs):
    out = {}
    for x in xs:
        out[str(x)] = out.get(str(x), 0) + 1
    return out
BYW841 = {}
for j in JOBS841:
    if j['job'] in REC841:
        k = EVALKEY841[j['job']]
        key = k['cond'] + ('_' + k['arm'] if 'arm' in k else '')
        BYW841.setdefault(k['world'], {})[key] = (j, REC841[j['job']])
NW841 = len(worlds829)
ARMLIST841 = ['CTRL840', 'M2S', 'M2H', 'D1', 'D1_1'] + ['M1_L%d' % l for l in MID841]
STATES841 = ('S_NULL', 'S_FIRST', 'S_BRIDGED', 'S_FORK', 'S_DECOY', 'S_IRREL', 'S_FIRST_V1', 'S_NULL_FB', 'S_FIRST_FB', 'S_BRIDGED_FB')
CELLS841 = {}
for wi, w in enumerate(worlds829):
    d = BYW841.get(wi, {}); ids = w['ids']; x = {'world': wi}
    for cond in STATES841:
        if cond not in d:
            continue
        _, r = d[cond]
        for arm in ARMLIST841:
            ra = r['arms'].get(arm)
            if ra is None:
                continue
            x[arm + '|' + cond] = role841(ra['chosen'], wi)
            if cond in ('S_FIRST', 'S_FIRST_V1'):
                x[arm + '|' + cond + '|content'] = list(CONTENT841[ra['chosen']][:2]) if ra['chosen'] in CONTENT841 else None
            if cond == 'S_FIRST':
                x[arm + '|first_indexed_rows'] = ra.get('indexed_rows')
                mc = [ids[k] for k in ('second', 'changed', 'mirror')]
                x[arm + '|first_mcard_rank'] = rank841(ra['scores'], mc)
            if cond == 'S_BRIDGED':
                x[arm + '|bridged_bridgecont_rank'] = rank841(ra['scores'], [ids['bridgecont']])
        if 'step0_top' in r:
            x['step0_top1|' + cond] = r['step0_top']['top_ids'][0]
            x['step0_p1|' + cond] = r['step0_top']['top_p'][0]
            x['step0_equal_across_arms|' + cond] = all(r['step0_equal'])
            x['hard_echo_text|' + cond] = tok.decode([s_['top_ids'][0] for s_ in r['arms']['M2H']['echo']], skip_special_tokens=False)
            x['soft_entropy_mean|' + cond] = float(np.mean([s_['entropy'] for s_ in r['arms']['M2S']['echo']]))
    for cond in ('ANSWER_FIRST_SECOND', 'ANSWER_SECOND_FIRST', 'ANSWER_FIRST_IRRELEVANT', 'ANSWER_BRIDGED_SECOND',
                 'ANSWER_BRIDGED_BRIDGECONT', 'ANSWER_NULL'):
        if cond in d:
            x[cond] = tcat841(tcls841(d[cond][1]['answer']['raw'], w))
    for cond in ('ACT_NULL', 'ACT_FIRST', 'ACT_COMPLETE', 'ACT_BROKEN', 'ACT_FORK'):
        if cond in d:
            x[cond] = d[cond][1]['action']
    for arm in ARMS841:
        for cond in ('LOOP_LIVE', 'LOOP_MISSING', 'LOOP_FORK'):
            key = cond + '_' + arm
            if key not in d:
                continue
            _, r = d[key]
            fm = set(r['final_mounted'])
            x[key + '|end'] = r['end']
            x[key + '|answer'] = tcat841(tcls841(r['answer_raw'], w)) if r['answer_raw'] is not None else None
            x[key + '|actions'] = '>'.join(s_['action'] for s_ in r['steps'])
            x[key + '|routed_roles'] = '>'.join(role841(s_['route']['chosen'], wi) for s_ in r['steps'] if 'route' in s_)
            x[key + '|has_chain'] = ids['first'] in fm and bool(fm & {ids['second'], ids['changed']})
            x[key + '|dropped_roles'] = '>'.join(role841(c, wi) for c in r['dropped'])
            x[key + '|steps'] = len(r['steps'])
    CELLS841[wi] = x
WL841 = list(CELLS841.values())
def cnt841(f):
    xs = [f(x) for x in WL841]
    xs = [v for v in xs if v is not None]
    return [sum(1 for v in xs if v), len(xs)]
def has841(x, *keys):
    return all(k in x for k in keys)
ARMRES841 = {}
for arm in ARMLIST841:
    r1 = cnt841(lambda x: (x[arm + '|S_FIRST'] in MCARD841) if has841(x, arm + '|S_FIRST') else None)
    r1v = cnt841(lambda x: (x[arm + '|S_FIRST'] in VALID841) if has841(x, arm + '|S_FIRST') else None)
    shift = cnt841(lambda x: (x[arm + '|S_BRIDGED'] == 'OWN_BRIDGECONT' and x[arm + '|S_FIRST'] in MCARD841)
                   if has841(x, arm + '|S_BRIDGED', arm + '|S_FIRST') else None)
    nul = cnt841(lambda x: (x[arm + '|S_NULL'] not in MCARD841 + ('OWN_BRIDGECONT',)) if has841(x, arm + '|S_NULL') else None)
    irr = cnt841(lambda x: (x[arm + '|S_IRREL'] not in MCARD841 + ('OWN_BRIDGECONT',)) if has841(x, arm + '|S_IRREL') else None)
    frk = cnt841(lambda x: (x[arm + '|S_FORK'] not in MCARD841) if has841(x, arm + '|S_FORK') else None)
    dec = cnt841(lambda x: (x[arm + '|S_DECOY'] not in MCARD841) if has841(x, arm + '|S_DECOY') else None)
    idc = cnt841(lambda x: (x[arm + '|S_FIRST_V1|content'] == x[arm + '|S_FIRST|content'])
                 if has841(x, arm + '|S_FIRST_V1|content', arm + '|S_FIRST|content') else None)
    fb1 = cnt841(lambda x: (x[arm + '|S_FIRST_FB'] in MCARD841) if has841(x, arm + '|S_FIRST_FB') else None)
    fbs = cnt841(lambda x: (x[arm + '|S_BRIDGED_FB'] == 'OWN_BRIDGECONT' and x[arm + '|S_FIRST_FB'] in MCARD841)
                 if has841(x, arm + '|S_BRIDGED_FB', arm + '|S_FIRST_FB') else None)
    R1 = ok841(r1[0], r1[1], R1_NEED841, NW841); SHIFT = ok841(shift[0], shift[1], SHIFT_NEED841, NW841)
    NULLC = ('INCONCLUSIVE' if min(nul[1], irr[1]) < NW841 else
             'PASS' if (nul[0] >= NULLCTRL_NEED841 and irr[0] >= NULLCTRL_NEED841) else 'FAIL')
    SPEC = ('INCONCLUSIVE' if min(frk[1], dec[1]) < NW841 else
            'PASS' if (frk[0] >= SPEC_NEED841 and dec[0] >= SPEC_NEED841) else 'FAIL')
    IDC = ok841(idc[0], idc[1], ID_NEED841, NW841)
    FRB = ('INCONCLUSIVE' if min(fb1[1], fbs[1]) < NW841 else
           'PASS' if (fb1[0] >= FRAME_NEED841 and fbs[0] >= FRAME_NEED841) else 'FAIL')
    CONV = ('PASS' if all(v == 'PASS' for v in (R1, SHIFT, NULLC, SPEC)) else
            'INCONCLUSIVE' if 'INCONCLUSIVE' in (R1, SHIFT, NULLC, SPEC) else 'FAIL')
    roles = {c: dist841([x.get(arm + '|' + c) for x in WL841 if arm + '|' + c in x]) for c in STATES841}
    ARMRES841[arm] = {'R1': R1, 'R1_count': r1, 'R1V_count': r1v, 'SHIFT': SHIFT, 'SHIFT_count': shift, 'NULLCTRL': NULLC,
                      'null_count': nul, 'irrelevant_count': irr, 'SPEC': SPEC, 'fork_count': frk, 'decoy_count': dec,
                      'ID': IDC, 'ID_count': idc, 'FRAME_B': FRB, 'frame_b_r1': fb1, 'frame_b_shift': fbs,
                      'CONVERSION': CONV, 'top1_roles': roles,
                      'first_mcard_rank': [x.get(arm + '|first_mcard_rank') for x in WL841],
                      'indexed_rows_first': [x.get(arm + '|first_indexed_rows') for x in WL841],
                      'bridged_bridgecont_rank': [x.get(arm + '|bridged_bridgecont_rank') for x in WL841]}
# ---- intermediate measurements (IV.1-IV.3, IV.8): offline logit lens with the model's own final norm and lm_head ----
def lens_ranks841(vec, tids):
    with torch.no_grad():
        lg = model.lm_head(model.model.norm(torch.tensor(vec, device=DEV).to(DTYPE).reshape(1, 1, H)))[0, 0].float()
    return [int((lg > lg[t_]).sum().item()) + 1 for t_ in tids]
LENS_RES841 = {}
INTER841 = {'I3_first_top1_is_bridge': [], 'bridged_top1_is_new_bridge': [], 'I2_rank_better': [], 'state_change_ratio': [],
            'earliest_rank1_layer_first': [], 'hard_echo_contains_bridge': [], 'soft_hard_cos_mean': [],
            'soft_entropy_first': [], 'cos_row1_with_bridge_embedding': {'M2S': [], 'M2H': [], 'D1': []},
            'cos_row1_with_start_embedding': {'M2S': [], 'M2H': [], 'D1': []}}
Ef841 = lambda t_: E841[t_].float().to(DEV)
def tt841(a):
    return torch.tensor(np.asarray(a, dtype=np.float32), device=DEV).reshape(-1) if isinstance(a, np.ndarray) else a.float().reshape(-1)
def cos841(a, b):
    a = tt841(a); b = tt841(b)
    return float((a * b).sum() / (a.norm() * b.norm()).clamp_min(1e-9))
for wi, w in enumerate(worlds829):
    d = BYW841.get(wi, {}); ids = w['ids']
    tM, tMb, tS = tid841(w['middle']), tid841(w['bridge_mid']), tid841(w['start'])
    lr = {}
    for cond in ('S_NULL', 'S_FIRST', 'S_BRIDGED', 'S_FORK', 'S_IRREL'):
        if cond in d and d[cond][0]['job'] in ROWS841 and 'lens_last' in ROWS841[d[cond][0]['job']]:
            L_ = ROWS841[d[cond][0]['job']]['lens_last']
            lr[cond] = [lens_ranks841(L_[i], [tM, tMb, tS]) for i in range(len(LENS841))]
    LENS_RES841[wi] = lr
    if 'S_FIRST' in d:
        r = d['S_FIRST'][1]
        INTER841['I3_first_top1_is_bridge'].append(r['step0_top']['top_ids'][0] == tM)
        INTER841['hard_echo_contains_bridge'].append(w['middle'].upper() in
                                                       tok.decode([s_['top_ids'][0] for s_ in r['arms']['M2H']['echo']]).replace(' ', '').upper())
        INTER841['soft_entropy_first'].append(float(np.mean([s_['entropy'] for s_ in r['arms']['M2S']['echo']])))
        rw = ROWS841.get(d['S_FIRST'][0]['job'], {})
        if 'M2S_vec' in rw and 'M2H_vec' in rw:
            INTER841['soft_hard_cos_mean'].append(float(np.mean([cos841(rw['M2S_vec'][t_], rw['M2H_vec'][t_])
                                                                 for t_ in range(K_ECHO841)])))
            for arm in ARMS841:
                INTER841['cos_row1_with_bridge_embedding'][arm].append(cos841(rw[arm + '_vec'][0], Ef841(tM)))
                INTER841['cos_row1_with_start_embedding'][arm].append(cos841(rw[arm + '_vec'][0], Ef841(tS)))
    if 'S_BRIDGED' in d:
        INTER841['bridged_top1_is_new_bridge'].append(d['S_BRIDGED'][1]['step0_top']['top_ids'][0] == tMb)
    if all(c in lr for c in ('S_FIRST', 'S_NULL', 'S_IRREL')):
        INTER841['I2_rank_better'].append(lr['S_FIRST'][-1][0] < lr['S_NULL'][-1][0] and lr['S_FIRST'][-1][0] < lr['S_IRREL'][-1][0])
        e1 = [LENS841[i] for i in range(len(LENS841)) if lr['S_FIRST'][i][0] == 1]
        INTER841['earliest_rank1_layer_first'].append(e1[0] if e1 else None)
    if all(c in d for c in ('S_FIRST', 'S_NULL', 'S_IRREL')):
        h0 = ROWS841[d['S_NULL'][0]['job']]['lens_last'][-1]; h1 = ROWS841[d['S_FIRST'][0]['job']]['lens_last'][-1]
        h2 = ROWS841[d['S_IRREL'][0]['job']]['lens_last'][-1]
        INTER841['state_change_ratio'].append(float(np.linalg.norm(h1 - h0) / max(np.linalg.norm(h2 - h0), 1e-9)))
i3 = [sum(INTER841['I3_first_top1_is_bridge']), len(INTER841['I3_first_top1_is_bridge'])]
i2 = [sum(INTER841['I2_rank_better']), len(INTER841['I2_rank_better'])]
I3 = ok841(i3[0], i3[1], I3_NEED841, NW841); I2 = ok841(i2[0], i2[1], I2_NEED841, NW841)
LENS_MEDIAN841 = {}
for cond in ('S_NULL', 'S_FIRST', 'S_BRIDGED', 'S_FORK', 'S_IRREL'):
    for ti, tn in enumerate(('bridge', 'new_bridge', 'start')):
        vals = [[LENS_RES841[wi][cond][i][ti] for wi in LENS_RES841 if cond in LENS_RES841[wi]] for i in range(len(LENS841))]
        LENS_MEDIAN841[cond + '|' + tn] = [float(np.median(v)) if v else None for v in vals]
# ---- actions on designed states, closed loops ----
a_null = cnt841(lambda x: (x['ACT_NULL'] == 'SEARCH') if 'ACT_NULL' in x else None)
a_first = cnt841(lambda x: (x['ACT_FIRST'] == 'SEARCH') if 'ACT_FIRST' in x else None)
a_comp = cnt841(lambda x: (x['ACT_COMPLETE'] == 'ANSWER') if 'ACT_COMPLETE' in x else None)
a_brok = cnt841(lambda x: (x['ACT_BROKEN'] != 'ANSWER') if 'ACT_BROKEN' in x else None)
ACT841 = ('INCONCLUSIVE' if min(a_null[1], a_first[1], a_comp[1], a_brok[1]) < NW841 else
          'PASS' if (a_null[0] >= A_NULL_NEED841 and a_first[0] >= A_FIRST_NEED841 and a_comp[0] >= A_COMPLETE_NEED841 and
                     a_brok[0] >= A_BROKEN_NEED841) else 'FAIL')
ACTDIST841 = {c: dist841([x.get(c) for x in WL841 if c in x]) for c in ('ACT_NULL', 'ACT_FIRST', 'ACT_COMPLETE', 'ACT_BROKEN', 'ACT_FORK')}
LOOPRES841 = {}
for arm in ARMS841:
    k1, k2, k3 = 'LOOP_LIVE_' + arm, 'LOOP_MISSING_' + arm, 'LOOP_FORK_' + arm
    l1 = cnt841(lambda x: (x[k1 + '|end'] == 'MODEL_ANSWER' and x[k1 + '|answer'] in ('END', 'ALT_END') and x[k1 + '|has_chain'])
                if k1 + '|end' in x else None)
    l2 = cnt841(lambda x: (x[k2 + '|end'] == 'MODEL_STOP' or (x[k2 + '|end'] == 'MODEL_ANSWER' and x[k2 + '|answer'] == 'UNKNOWN'))
                if k2 + '|end' in x else None)
    l3 = cnt841(lambda x: (x[k3 + '|end'] == 'MODEL_ANSWER' and x[k3 + '|answer'] in ('END', 'ALT_END')) if k3 + '|end' in x else None)
    LOOPRES841[arm] = {'L1_LIVE': ok841(l1[0], l1[1], L1_NEED841, NW841), 'L1_count': l1,
                       'L2_MISSING': ok841(l2[0], l2[1], L2_NEED841, NW841), 'L2_count': l2,
                       'L3_FORK': ok841(l3[0], l3[1], L3_NEED841, NW841), 'L3_count': l3}
    for k_, nm in ((k1, 'live'), (k2, 'missing'), (k3, 'fork')):
        LOOPRES841[arm][nm] = {'ends': dist841([x.get(k_ + '|end') for x in WL841 if k_ + '|end' in x]),
                               'answers': dist841([x.get(k_ + '|answer') for x in WL841 if k_ + '|end' in x]),
                               'actions': dist841([x.get(k_ + '|actions') for x in WL841 if k_ + '|end' in x]),
                               'routed': dist841([x.get(k_ + '|routed_roles') for x in WL841 if k_ + '|end' in x]),
                               'dropped': dist841([x.get(k_ + '|dropped_roles') for x in WL841 if k_ + '|end' in x]),
                               'budget_stops': sum(1 for x in WL841 if x.get(k_ + '|end') == 'BUDGET_STOP'),
                               'chain_mounted': sum(1 for x in WL841 if x.get(k_ + '|has_chain'))}
# ---- answers on designed mounts ----
h_end = cnt841(lambda x: (x['ANSWER_FIRST_SECOND'] == 'END') if 'ANSWER_FIRST_SECOND' in x else None)
h_ord = cnt841(lambda x: (x['ANSWER_SECOND_FIRST'] == 'END') if 'ANSWER_SECOND_FIRST' in x else None)
h_null = cnt841(lambda x: (x['ANSWER_NULL'] == 'UNKNOWN') if 'ANSWER_NULL' in x else None)
h_brk = cnt841(lambda x: (x['ANSWER_BRIDGED_SECOND'] == 'UNKNOWN') if 'ANSWER_BRIDGED_SECOND' in x else None)
h_bc = cnt841(lambda x: (x['ANSWER_BRIDGED_BRIDGECONT'] == 'BRIDGE_END') if 'ANSWER_BRIDGED_BRIDGECONT' in x else None)
h_irr = cnt841(lambda x: (x['ANSWER_FIRST_IRRELEVANT'] == 'UNKNOWN') if 'ANSWER_FIRST_IRRELEVANT' in x else None)
HABL841 = ('INCONCLUSIVE' if min(h_end[1], h_ord[1], h_null[1], h_brk[1]) < NW841 else
           'PASS' if (h_end[0] >= H_END_NEED841 and h_ord[0] >= H_ORDER_NEED841 and h_null[0] >= H_NULL_NEED841 and
                      h_brk[0] >= H_BROKEN_NEED841) else 'FAIL')
F841 = 'PASS' if (F_ORDER841 <= ORDER_TOL841 and F_ARGMAX841) else 'FAIL'
# ---- decision ----
MAIN841 = ('M2S', 'M2H', 'D1')
EXTCTRL841 = not all(c['pass'] for c in D829['checks'] if c['name'].startswith(('STATIC_', 'LOCKED_', 'BYPASS_', 'LAYERS_', 'ECHO_')))
if BUDGET_STOP841:
    decision841 = 'YETERSİZ KANIT'
elif any(ARMRES841[a]['CONVERSION'] == 'PASS' for a in MAIN841):
    decision841 = 'DEVAM'
elif all(ARMRES841[a]['R1'] == 'FAIL' and ARMRES841[a]['SHIFT'] == 'FAIL' for a in MAIN841):
    decision841 = 'DUR'
else:
    decision841 = 'YETERSİZ KANIT'
loop_pass841 = [a for a in MAIN841 if all(LOOPRES841[a][k] == 'PASS' for k in ('L1_LIVE', 'L2_MISSING', 'L3_FORK'))]
VERDICTS841 = {
    'LATENT_ADDRESS_CONVERSION': {a: ARMRES841[a]['CONVERSION'] for a in ARMLIST841},
    'MODEL_CHOSEN_ACTIONS_IN_FIXED_LOOP': {'ACT': ACT841, **{a: {k: LOOPRES841[a][k] for k in ('L1_LIVE', 'L2_MISSING', 'L3_FORK')}
                                                              for a in MAIN841}},
    'MODEL_NATIVE_COGNITIVE_CONTROL': ('FAIL' if EXTCTRL841 else
                                       ('PARTIAL: model-chosen actions in a fixed four-word vocabulary and a fixed loop (arms '
                                        + ', '.join(loop_pass841) + '); KORU vs DUZELT on conflicting evidence not measured')
                                       if (loop_pass841 and ACT841 == 'PASS') else 'NOT_DEMONSTRATED'),
    'AUTONOMOUS_RECURSIVE_REASONING': 'NOT_DEMONSTRATED (two-hop synthetic chains, fixed vocabulary, fixed loop)',
    'external_cognitive_control_detected': EXTCTRL841}
CRIT841 = {'ARMS': {a: {k: ARMRES841[a][k] for k in ('R1', 'SHIFT', 'NULLCTRL', 'SPEC', 'ID', 'FRAME_B', 'CONVERSION')}
                    for a in ARMLIST841},
           'I3_BRIDGE_SALIENCE': I3, 'I2_CONTENT_SPECIFIC': I2, 'ACT_DESIGNED_STATES': ACT841,
           'LOOPS': {a: {k: LOOPRES841[a][k] for k in ('L1_LIVE', 'L2_MISSING', 'L3_FORK')} for a in MAIN841},
           'H_ANSWERS': HABL841, 'F_ORDER': F841}
TIM841 = {}
def med841(vals):
    vals = [v for v in vals if v is not None]
    return float(np.median(vals)) if vals else None
SREC841 = [REC841[j['job']] for j in JOBS841 if j['job'] in REC841 and REC841[j['job']]['kind'] == 'STATE']
for arm in ARMS841:
    TIM841['echo_ms_median_' + arm] = med841([r['arms'][arm]['echo_ms'] for r in SREC841])
    TIM841['index_bypass_ms_median_' + arm] = med841([r['arms'][arm]['index_ms'] for r in SREC841])
TIM841['route_ms_median'] = med841([r['arms']['M2S']['route_ms'] for r in SREC841])
TIM841['ctrl_bypass_ms_median'] = med841([r['arms']['CTRL840']['bypass_ms'] for r in SREC841])
TIM841['mount_ms_median'] = med841([r['mount_ms'] for r in SREC841 if r['mount_ms']])
TIM841['answer_ms_median'] = med841([REC841[j['job']]['answer']['answer_ms'] for j in JOBS841
                                     if j['job'] in REC841 and REC841[j['job']]['kind'] == 'ANSWER'])
TIM841['bypass_vs_full_ms_null'] = [D829['bypass_verification841']['null_memory']['bypass_ms'],
                                    D829['bypass_verification841']['null_memory']['full_forward_ms']]
TIM841['key_bank_load_seconds'] = D829['key_bank841']['load_seconds']
TIM841['mid_key_forge_seconds'] = D829['mid_key_bank841']['seconds']
REPORT841 = {
    'bypass': D829['bypass_verification841'], 'upper_layer_check': UPPER_CHECK841, 'io_matrices': D829['io_matrices841'],
    'mid_key_bank': D829['mid_key_bank841'], 'arms': ARMRES841,
    'intermediate': {'I3': I3, 'I3_count': i3, 'I2': I2, 'I2_count': i2,
                     'bridged_top1_is_new_bridge': [sum(INTER841['bridged_top1_is_new_bridge']), len(INTER841['bridged_top1_is_new_bridge'])],
                     'hard_echo_contains_bridge': [sum(INTER841['hard_echo_contains_bridge']), len(INTER841['hard_echo_contains_bridge'])],
                     'state_change_ratio_first_over_irrelevant': INTER841['state_change_ratio'],
                     'earliest_rank1_layer_first': INTER841['earliest_rank1_layer_first'],
                     'soft_hard_cos_mean': INTER841['soft_hard_cos_mean'], 'soft_entropy_first': INTER841['soft_entropy_first'],
                     'cos_row1_with_bridge_embedding': {a: med841(v) for a, v in INTER841['cos_row1_with_bridge_embedding'].items()},
                     'cos_row1_with_start_embedding': {a: med841(v) for a, v in INTER841['cos_row1_with_start_embedding'].items()},
                     'lens_median_rank': LENS_MEDIAN841, 'lens_layers': list(LENS841)},
    'actions': {'ACT': ACT841, 'null_search': a_null, 'first_search': a_first, 'complete_answer': a_comp,
                'broken_not_answer': a_brok, 'distributions': ACTDIST841},
    'loops': LOOPRES841,
    'answers': {'H': HABL841, 'first_second_end': h_end, 'second_first_end': h_ord, 'null_unknown': h_null,
                'bridged_second_unknown': h_brk, 'bridged_bridgecont_bridge_end': h_bc, 'first_irrelevant_unknown': h_irr},
    'F': {'F': F841, 'order_max_abs_score_diff': F_ORDER841, 'same_argmax': F_ARGMAX841,
          'v1_keys_bitwise_identical': D829['key_bank841']['v1_keys_bitwise_identical_to_v0']},
    'timing': TIM841, 'verdicts': VERDICTS841, 'classes': HYP841['classes'], 'not_measured': HYP841['not_measured_deferred'],
    'resume': D829['resume841']}
D829['cells841'] = CELLS841
D829['lens841'] = LENS_RES841
D829['report841'] = REPORT841
D829['verdict841'] = {'decision': decision841, 'criteria': CRIT841, 'verdicts': VERDICTS841, 'budget_stop': BUDGET_STOP841,
                      'interpretation_guard': ('The GPU router is an engineering component. CONVERSION PASS would show that '
                                               'the model\'s own deep computation over mounted memory, fed back through psi, '
                                               'carries the next address numerically; it is not cognitive control. Loop '
                                               'results are model-chosen words in a fixed vocabulary, applied literally.')}
D829['claims_ledger841'] = dict(CLAIMS841, demonstrated_by_TEST841={'decision': decision841, 'criteria': CRIT841, 'verdicts': VERDICTS841})
D829['cost841'] = {'counted': dict(COUNT834), 'predicted_upper': POST841, 'run_seconds': D829['run_seconds841'],
                   'total_seconds_body': round(time.perf_counter() - T0_841, 3),
                   'peak_gpu_gib': float(_torch829.cuda.max_memory_allocated()) / 2**30}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f841:
    cols841 = sorted({k for x in WL841 for k in x})
    wr841 = csv.DictWriter(f841, fieldnames=cols841)
    wr841.writeheader()
    for x in WL841:
        wr841.writerow({k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in x.items()})
D829['status'] = 'COMPLETE_TEST841_EVALUATED' if not BUDGET_STOP841 else 'STOPPED_BUDGET_PARTIAL_EVALUATED'
save829()
log829('TEST841_REPORT', json.dumps(REPORT841, default=str))
log829('TEST841_VERDICT', json.dumps(D829['verdict841'], default=str))
log829('TEST841_COMPLETED', str(OUT829))
'''

# ===== TEST841 PARÇA 3/3 — Colab'da aynı hücreye sırayla yapıştırın =====
BODY_SHA841 = hashlib.sha256(BODY841.encode()).hexdigest()
PANEL_HOOK841 = ("PANEL829['test841'] = {'jobs': JOBS841, 'banks': BANKS841, 'beta': BETA841, 'peak_weight': PEAK_WEIGHT841, "
                 "'k_echo': K_ECHO841, 't_max': T_MAX841, 'arms': ARMS841, 'lens': LENS841, 'mid': MID841, 'actions': ACTIONS841, "
                 "'frames': [LOOKUP_A841, LOOKUP_B841, ACTION_TXT841, PREFILL_TXT841, IDXPRE_TXT841, IDXPOST_TXT841], "
                 "'thresholds': {'R1': R1_NEED841, 'SHIFT': SHIFT_NEED841, 'NULLCTRL': NULLCTRL_NEED841, 'SPEC': SPEC_NEED841, "
                 "'ID': ID_NEED841, 'FRAME_B': FRAME_NEED841, 'I3': I3_NEED841, 'I2': I2_NEED841, 'L': [L1_NEED841, L2_NEED841, L3_NEED841], "
                 "'ACT': [A_NULL_NEED841, A_FIRST_NEED841, A_COMPLETE_NEED841, A_BROKEN_NEED841], "
                 "'H': [H_END_NEED841, H_ORDER_NEED841, H_NULL_NEED841, H_BROKEN_NEED841], 'bypass_tol': BYPASS_TOL841, "
                 "'order_tol': ORDER_TOL841}, "
                 "'hypotheses': %r, 'body_sha256': %r, 'helpers_sha256': %r, 'seed': SEED829}\n"
                 % (HYP841, BODY_SHA841, HELPER_SHA841))
src841 = patch841(src841, "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))",
                  PANEL_HOOK841 + "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))")
OFFLINE_HOOK841 = r'''
OFFLINE841 = DIR829 / 'TEST841_offline_key.json'   # never read by any runtime computation
OFFLINE841.write_text(json.dumps({'note': 'OFFLINE ONLY', 'jobs': EVALKEY841,
                                  'cartridge_contents': {c: list(v) for c, v in CONTENT841.items()},
                                  'worlds': worlds829, 'questions': questions829, 'card_meta': card_meta829},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D829['offline_key841_sha256'] = sha829(OFFLINE841.read_bytes())
'''
src841 = patch841(src841, "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n",
                  "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n" + OFFLINE_HOOK841)
start841 = src841.index("    # RUN ORDER: integrity checks")
start841 = src841.rfind("    # ---", 0, start841)
end841 = src841.index("except BaseException as e:\n    D829['status'] = 'ERROR'", start841)
BODY841_TEXT = BODY841
replacement841 = "\n".join("    " + line if line else "" for line in BODY841.strip("\n").splitlines()) + "\n"
patched841 = src841[:start841] + replacement841 + src841[end841:]
ast.parse(patched841)
# ==================================================================================================================
# CONSOLE / LOGGING LAYER (TEST835 pattern). Nothing below changes what is computed. Every byte the engine prints is
# written unchanged to a full transcript file; the screen shows a compact digest, progress, failures and the summary.
# ==================================================================================================================
import os as _os841, sys as _sys841, io as _io841, traceback as _tb841, datetime as _dt841, shutil as _sh841
from pathlib import Path as _P841
_os841.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')     # download bars only (not data)
for _m841, _f841 in (('huggingface_hub', lambda m: m.utils.disable_progress_bars()),
                     ('transformers', lambda m: m.utils.logging.disable_progress_bar())):
    if _m841 in _sys841.modules:                                    # only if already imported: no new import
        try:
            _f841(_sys841.modules[_m841])
        except Exception:
            pass
_ROOT841 = _P841('/content') if _P841('/content').exists() else _P841('/tmp')
FULL_CONSOLE841 = _ROOT841 / ('TEST841_full_console_' + _dt841.datetime.now(_dt841.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.txt')
CON841 = {'phase': 'SOURCE_VERIFICATION', 'last': [], 'fail_lines': [], 't0': time.time(), 'measure': '0/0', 'p3': 0}
_ORIG_OUT841, _ORIG_ERR841 = _sys841.stdout, _sys841.stderr

def say841(*a):
    _ORIG_OUT841.write(' '.join(str(x) for x in a) + '\n'); _ORIG_OUT841.flush()

def _mins841():
    return round((time.time() - CON841['t0']) / 60.0, 1)

def conroute841(line):
    s = line.strip()
    if not s:
        return
    CON841['last'] = (CON841['last'] + [s[:300]])[-6:]
    if s.startswith('FAIL '):
        CON841['fail_lines'].append(s[:600]); say841('!! ' + s[:600]); return
    if s.startswith('TEST829_FAILED'):
        CON841['fail_lines'].append(s[:300]); return
    if s.startswith('TEST829_START'):
        parts = s.split()
        say841('Çalışma: %s | panel SHA-256: %s' % (parts[1] if len(parts) > 1 else '?', parts[-1]))
        CON841['phase'] = 'ENGINE_PRELUDE_AND_LOCKS'; return
    if s.startswith('TEST815_GPU_PREFLIGHT'):
        say841('GPU: ' + s[len('TEST815_GPU_PREFLIGHT'):].strip()); return
    if s.startswith('TEST815_GPU_FREE_GIB'):
        say841('GPU boş VRAM (yükleme öncesi): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('TEST841_PREDICTED_COST_BEFORE_MODEL_LOAD'):
        try:
            c = json.loads(s.split(' ', 1)[1]); u = c['numeric_upper']
            say841('Maliyet üst sınırı (model yükleme hariç, %%25 pay dahil): %s dk | iş %s | kartuş %s (banka %s) | fusion<=%s '
                   'bypass<=%s üretim<=%s' % (c['minutes_upper_excluding_model_load'], c['jobs'], c['physical_cartridges'],
                   c['bank_cartridges'], u['fusion_forwards'], u['bypass_forwards'], u['generation_forwards']))
        except Exception:
            say841(s[:300])
        CON841['phase'] = 'MODEL_LOAD'; say841('Model yükleniyor (Qwen2.5-72B-Instruct, NF4, tek yükleme)...'); return
    if s.startswith('PASS FROZEN_PREFIX'):
        D_ = globals().get('D829', {})
        say841('Model yüklendi (%s s). Fiziksel kartuşlar üretiliyor ve SHA doğrulanıyor...' % D_.get('model_load_seconds', '?'))
        CON841['phase'] = 'PHYSICAL_CARTRIDGE_FORGING'; return
    if s.startswith('PASS PHYSICAL_COUNT'):
        say841('Fiziksel kartuşlar: ' + s.split()[-1] + ' (her biri SHA-256 + tensör SHA ile yeniden yüklendi)')
        CON841['phase'] = 'PREFLIGHT_GATES'; return
    if s.startswith('PASS ARCH_DIMS'):
        say841('Mimari (NL,H,QH,KVH,HD): ' + s[len('PASS ARCH_DIMS'):].strip() + ' | BF16 hesap, NF4, ağırlıklar donmuş'); return
    if s.startswith('PASS VRAM_HEADROOM'):
        say841('Boş VRAM (model sonrası): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('PASS STATIC_NO_LABELS_BEFORE_OFFLINE'):
        say841('Sızıntı kapısı: çevrimdışı işaretinden önce hiçbir etiket nesnesi kullanılmıyor (AST)'); return
    if s.startswith('PASS LOCKED_FREE_GENERATE_BYTECODE'):
        say841('Kaynak doğrulama: free_generate bytecode = kilitli 779 derlemesi (aynı boru hattı); greedy argmax, örnekleme yok'); return
    if s.startswith('PASS LOCKED_ATTENTION_INTERVENTION_BYTECODE'):
        say841('Kaynak doğrulama: AttentionIntervention bytecode = kilitli 779 (bias=0: maske değişmez)'); return
    if s.startswith('TEST841_CUT3_BYTECODE_INFO'):
        say841('Bilgi: Cut3Diagnostic kilitli 779 bytecode eşitliği ' + s.split(' ', 1)[1][:160] + ' (seed=None: enjeksiyon dalı çalışmaz)'); return
    if s.startswith('TEST841_SOURCE_VERIFIED_BEFORE_MODEL_LOAD'):
        say841('Kaynak doğrulama tamam (model yüklenmeden önce)'); return
    if s.startswith('PASS STATIC_GENERATION_CALLS_UNMODIFIED'):
        say841('Kaynak doğrulama: iki üretim çağrısı (cevap çerçevesi, eylem çerçevesi): seed=None, gain=0, spans=None, greedy'); return
    if s.startswith('PASS STATIC_ECHO_INPUTS'):
        say841('Kaynak doğrulama: yankı yalnızca takılı belleği, sabit çerçeveyi ve modelin kendi tensörlerini görüyor'); return
    if s.startswith('PASS STATIC_NO_WEIGHT_WRITES'):
        say841('Kaynak doğrulama: ağırlık / embedding / norm / lm_head yazımı yok (AST)'); return
    if s.startswith('PASS STATIC_LAYER_TRUNCATION_ONLY_IN_BYPASS'):
        say841('Kaynak doğrulama: katman listesi yalnızca bypass fonksiyonunda kısaltılıyor ve finally ile geri yükleniyor'); return
    if s.startswith('PASS STATIC_ROUTER_INPUTS'):
        say841('Kaynak doğrulama: yönlendirici yalnızca H3 satırları, aday listesi ve takılı kartları görüyor (etiket yok)'); return
    if s.startswith('PASS LOCKED_DIRECTCUT3_BYTECODE'):
        say841('Kaynak doğrulama: DirectCut3 bytecode = kilitli 730 derlemesi'); return
    if s.startswith('PASS V2_ADDRESSING_SOURCE_FACTS'):
        say841('Kaynak doğrulama: v2 610/626/627 adresleme formülleri kaynakta doğrulandı (L3, rank-0, beta 8, PEAK50)'); return
    if s.startswith('TEST841_BYPASS_VERIFICATION'):
        try:
            r = json.loads(s.split(' ', 1)[1])
            say841('Bypass doğrulama: H3 bitwise (NULL %s, kart %s, embeds yolu %s) | bypass çağrıları alt %s üst %s lm_head %s | %s ms vs tam %s ms'
                   % (r['null_memory']['bitwise'], r['one_card_memory']['bitwise'], r['embeds_path']['bitwise_vs_ids_path'],
                      r['calls_bypass']['lower_calls'], r['calls_bypass']['upper_max'], r['calls_bypass']['lm_head'],
                      r['null_memory']['bypass_ms'], r['null_memory']['full_forward_ms']))
            say841('Yankı doğrulama: her adımda 80 katman + lm_head %s | sert yankı deterministik %s | %s ms'
                   % (r['calls_echo'], r['echo_deterministic_hard'], r['echo_ms']))
        except Exception:
            say841(s[:300])
        return
    if s.startswith('TEST841_IO_MATRICES'):
        try:
            r = json.loads(s.split(' ', 1)[1])
            say841('Giriş/çıkış matrisleri: embed %s %s | lm_head %s | bağlı (tied) %s | ortalama embedding satır RMS %.4g'
                   % (r['embedding_shape'], r['embedding_dtype'], r['lm_head_weight_dtype'], r['tied_input_output'],
                      r['mean_embedding_row_rms']))
        except Exception:
            say841(s[:300])
        return
    if s.startswith('TEST841_MID_KEY_BANK'):
        try:
            r = json.loads(s.split(' ', 1)[1])
            say841('Orta katman anahtar bankası (tanı): %s kart, katman-3 kartuşla bitwise %s/%s, maks göreli fark %.3g, bağlam eşleşmesi %s, %s s'
                   % (r['n'], r['h3_bitwise'], r['n'], r['h3_max_rel'], r['context_matches_forge'], r['seconds']))
        except Exception:
            say841(s[:300])
        return
    if s.startswith('PASS CUT3_MOUNT_AND_ANSWER_RUN_UPPER_LAYERS'):
        say841('Üst katman yeniden hesaplama doğrulandı (CUT3 mount + cevap): ' + s[len('PASS CUT3_MOUNT_AND_ANSWER_RUN_UPPER_LAYERS'):].strip()[:160]); return
    if s.startswith('TEST841_RESUME '):
        try:
            r = json.loads(s.split(' ', 1)[1])
            say841('Devam mekanizması: yeniden kullanılan iş %s | %s' % (r.get('reused_jobs'), r.get('reason')))
            CON841['phase'] = 'RUNTIME'
        except Exception:
            say841(s[:300])
        return
    if s.startswith('TEST841_PROGRESS'):
        p = s.split()
        if len(p) >= 5:
            CON841['phase'] = 'MEASUREMENT %s (%s/%s)' % (p[1], p[2], p[4])
            if p[2] != '0':
                say841('  %-11s %s/%s (%s dk)' % (p[1], p[2], p[4], _mins841()))
        return
    if s.startswith('TEST841_BUDGET_STOP'):
        say841('!! ' + s); return
    if s.startswith('TEST841_OFFLINE_START'):
        CON841['phase'] = 'OFFLINE_EVALUATION'
        say841('Ölçüm bitti; çevrimdışı değerlendirme (%s dk)' % _mins841()); return
    if s.startswith('TEST841_COMPLETED'):
        CON841['phase'] = 'COMPLETED'; return

class Console841(_io841.TextIOBase):
    """Writes everything to FULL_CONSOLE841 unchanged; routes complete lines to the compact screen digest."""
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
                conroute841(line.split('\r')[-1])
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

def sha_path841(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()

def fmt841(x):
    if isinstance(x, list) and len(x) == 2 and all(isinstance(v, (int, float)) for v in x):
        return '%s/%s' % (x[0], x[1])
    if isinstance(x, dict):
        return ', '.join('%s=%s' % (k, fmt841(v)) for k, v in x.items())
    if isinstance(x, float):
        return '%.4g' % x
    if isinstance(x, list):
        return '[' + ', '.join(fmt841(v) for v in x) + ']'
    return str(x)

def files_report841():
    say841('=' * 78); say841('SONUÇ DOSYALARI (SHA-256)')
    d = globals().get('DIR829')
    if d is None or not _P841(d).exists():
        say841('  (çalışma klasörü yok)'); return
    for p in sorted(_P841(d).iterdir()):
        if p.is_file():
            say841('  %s  %d B  %s' % (p, p.stat().st_size, sha_path841(p)))
    vd = _P841(d) / 'TEST841_jobs'
    if vd.exists():
        fs = sorted(x for x in vd.iterdir() if x.is_file())
        say841('  %s/  %d iş kaydı, %.1f MB (her dosyanın SHA-256 değeri TEST841_job_manifest.jsonl içinde)'
               % (vd, len(fs), sum(x.stat().st_size for x in fs) / 2**20))

def final841(D):
    R = D['report841']; V = D['verdict841']; K = V['criteria']; C = D['cost841']; VD = V['verdicts']
    checks = D.get('checks', [])
    BV = R['bypass']; T = R['timing']; I = R['intermediate']; A = R['arms']
    say841('=' * 78); say841('TEST841 SONUÇ ÖZETİ (latent yeniden giriş; yönlendirici = MÜHENDİSLİK; eylem kelimesi = modelin çıktısı)'); say841('=' * 78)
    say841('Durum: %s | bütçe durdurması: %s | devam: yeniden kullanılan iş %s' % (D.get('status'), V['budget_stop'],
           R['resume'].get('reused_jobs')))
    say841('Bütünlük: %d kapı, %d başarısız | dış bilişsel kontrol tespit edildi: %s' % (len(checks), sum(not c['pass'] for c in checks),
           VD['external_cognitive_control_detected']))
    say841('-' * 78)
    say841('[BYPASS] H3 %s %s | NULL bitwise %s, kart bitwise %s, embeds yolu bitwise %s | yankı her adımda tam model %s'
           % (BV['h3_shape'], BV['h3_dtype'], BV['null_memory']['bitwise'], BV['one_card_memory']['bitwise'],
              BV['embeds_path']['bitwise_vs_ids_path'], BV['calls_echo']))
    iom = R['io_matrices']; mk = R['mid_key_bank']
    say841('  embed %s %s, lm_head %s, bağlı %s | orta katman anahtarları bağlam eşleşmesi %s (maks göreli fark %.3g)'
           % (iom['embedding_shape'], iom['embedding_dtype'], iom['lm_head_weight_dtype'], iom['tied_input_output'],
              mk['context_matches_forge'], mk['h3_max_rel']))
    say841('  Süre medyan: yankı M2S %s / M2H %s / D1 %s ms | indeks bypass %s ms | yönlendirici %s ms | mount %s ms | cevap %s ms'
           % (fmt841(T['echo_ms_median_M2S']), fmt841(T['echo_ms_median_M2H']), fmt841(T['echo_ms_median_D1']),
              fmt841(T['index_bypass_ms_median_M2S']), fmt841(T['route_ms_median']), fmt841(T['mount_ms_median']),
              fmt841(T['answer_ms_median'])))
    say841('-' * 78); say841('ARA ÖLÇÜMLER (çevrimdışı; modelin kendi son normu + lm_head ile logit lens)')
    say841('  [IV.3] ilk kart takılıyken sonraki token argmax = köprü varlığının ilk tokeni %s (%s) | S->M\' takılıyken yeni köprü %s'
           % (fmt841(I['I3_count']), I['I3'], fmt841(I['bridged_top1_is_new_bridge'])))
    say841('  [IV.2] köprü tokeni sırası ilk kartla NULL ve ilgisiz karttan iyi %s (%s) | sert yankı köprü adını içeriyor %s'
           % (fmt841(I['I2_count']), I['I2'], fmt841(I['hard_echo_contains_bridge'])))
    lm = I['lens_median_rank']
    say841('  [lens] köprü tokeni medyan sıra, katman %s:' % fmt841(I['lens_layers']))
    for cond in ('S_NULL', 'S_FIRST', 'S_IRREL'):
        say841('     %-9s %s' % (cond, fmt841(lm.get(cond + '|bridge'))))
    say841('     S_BRIDGED (yeni köprü) %s' % fmt841(lm.get('S_BRIDGED|new_bridge')))
    say841('  [IV.1] son katman durum değişimi ilk/ilgisiz oranı %s' % fmt841([round(x, 2) for x in I['state_change_ratio_first_over_irrelevant']]))
    say841('  [IV.8] yumuşak-sert kosinüs %s | yumuşak entropi %s | 1. vektörün köprü embedding kosinüsü %s | başlangıç %s'
           % (fmt841([round(x, 3) for x in I['soft_hard_cos_mean']]), fmt841([round(x, 3) for x in I['soft_entropy_first']]),
              fmt841(I['cos_row1_with_bridge_embedding']), fmt841(I['cos_row1_with_start_embedding'])))
    say841('-' * 78); say841('ADRESLEME KOLLARI (R1 köprü kartı | R1V geçerli yön | SHIFT köprü değişimi | NULL/ilgisiz | fork/decoy | ID | çerçeve B)')
    for arm in ('CTRL840', 'M2S', 'M2H', 'D1', 'D1_1', 'M1_L16', 'M1_L32', 'M1_L48', 'M1_L64', 'M1_L79'):
        a = A.get(arm)
        if not a:
            continue
        say841('  %-8s R1 %s %-4s | R1V %s | SHIFT %s %-4s | %s/%s %-4s | %s/%s %-4s | ID %s | B %s/%s | DÖNÜŞÜM %s'
               % (arm, fmt841(a['R1_count']), a['R1'], fmt841(a['R1V_count']), fmt841(a['SHIFT_count']), a['SHIFT'],
                  fmt841(a['null_count']), fmt841(a['irrelevant_count']), a['NULLCTRL'], fmt841(a['fork_count']),
                  fmt841(a['decoy_count']), a['SPEC'], fmt841(a['ID_count']), fmt841(a['frame_b_r1']), fmt841(a['frame_b_shift']),
                  a['CONVERSION']))
    for arm in ('M2S', 'M2H', 'D1'):
        say841('    %s ilk kart sonrası top-1 rolleri: %s' % (arm, fmt841(A[arm]['top1_roles']['S_FIRST'])))
    say841('-' * 78); say841('KAPALI DÖNGÜ (modelin kendi eylem kelimesi harfiyen uygulandı; bütçe durdurması modelin kararı değildir)')
    ac = R['actions']
    say841('  Tasarlanmış durumlar: NULL->SEARCH %s | ilk->SEARCH %s | ilk+ikinci->ANSWER %s | bozuk köprü->ANSWER değil %s | %s'
           % (fmt841(ac['null_search']), fmt841(ac['first_search']), fmt841(ac['complete_answer']), fmt841(ac['broken_not_answer']),
              ac['ACT']))
    say841('    dağılımlar: %s' % fmt841(ac['distributions']))
    for arm in ('M2S', 'M2H', 'D1'):
        L = R['loops'][arm]
        say841('  %-4s L1 canlı %s %-4s | L2 eksik %s %-4s | L3 fork %s %-4s | bütçe durdurması %s/%s/%s'
               % (arm, fmt841(L['L1_count']), L['L1_LIVE'], fmt841(L['L2_count']), L['L2_MISSING'], fmt841(L['L3_count']),
                  L['L3_FORK'], L['live']['budget_stops'], L['missing']['budget_stops'], L['fork']['budget_stops']))
        say841('       canlı bitişler %s | eksik bitişler %s | fork bitişler %s'
               % (fmt841(L['live']['ends']), fmt841(L['missing']['ends']), fmt841(L['fork']['ends'])))
    h = R['answers']
    say841('[H] Cevaplar: ilk+ikinci uç %s | ikinci+ilk uç %s | NULL UNKNOWN %s | bozuk köprü UNKNOWN %s | köprü+köprü-devam %s | ilgisiz UNKNOWN %s | %s'
           % (fmt841(h['first_second_end']), fmt841(h['second_first_end']), fmt841(h['null_unknown']), fmt841(h['bridged_second_unknown']),
              fmt841(h['bridged_bridgecont_bridge_end']), fmt841(h['first_irrelevant_unknown']), h['H']))
    f = R['F']
    say841('[F] Anahtar sırası maks fark %s, aynı argmax %s | yeni kimlikli anahtarlar bitwise aynı %s | %s'
           % (fmt841(f['order_max_abs_score_diff']), f['same_argmax'], fmt841(f['v1_keys_bitwise_identical']), f['F']))
    say841('-' * 78); say841('HÜKÜMLER:')
    say841('  LATENT_ADDRESS_CONVERSION          %s' % fmt841(VD['LATENT_ADDRESS_CONVERSION']))
    say841('  MODEL_CHOSEN_ACTIONS_IN_FIXED_LOOP %s' % fmt841(VD['MODEL_CHOSEN_ACTIONS_IN_FIXED_LOOP']))
    say841('  MODEL_NATIVE_COGNITIVE_CONTROL     %s' % VD['MODEL_NATIVE_COGNITIVE_CONTROL'])
    say841('  AUTONOMOUS_RECURSIVE_REASONING     %s' % VD['AUTONOMOUS_RECURSIVE_REASONING'])
    say841('  Ölçülmedi / ertelendi: %s' % '; '.join(R['not_measured']))
    say841('=' * 78)
    say841('NİHAİ BİLİMSEL KARAR: %s' % V['decision'])
    if V['decision'] == 'DEVAM':
        ok = [a for a in ('M2S', 'M2H', 'D1') if A[a]['CONVERSION'] == 'PASS']
        say841('  Gerekçe: %s kolunda R1, SHIFT, NULL/ilgisiz ve fork/decoy kontrolleri PASS — derin hesaplama sabit '
               'yönlendiriciyle bir sonraki fiziksel adrese dönüştü. Yönlendirici mühendisliktir.' % ', '.join(ok))
    elif V['decision'] == 'DUR':
        say841('  Gerekçe: üç ana kolun hiçbirinde R1 ve SHIFT geçmedi — derin bilgi bu yollarla adrese dönüşmedi.')
    else:
        say841('  Gerekçe: ' + ('bütçe durdurması' if V['budget_stop'] else
                               'ne DEVAM ne DUR kuralı sağlandı (bkz. kol satırları)'))
    say841('Maliyet: sayılan %s | çalışma %s s | toplam gövde %s s | tepe VRAM %.2f GiB'
           % (fmt841(C['counted']), C['run_seconds'], C['total_seconds_body'], C['peak_gpu_gib']))

say841('=' * 78)
say841('AKBASCORE TEST841 — latent yeniden giriş (D1 / M2-yumuşak / M2-sert) + TEST840 bypass + GPU PEAK50 + fiziksel CUT3 + model-seçimli eylem döngüsü; Qwen2.5-72B (NF4, donmuş)')
say841('Kaynak kilitleri: 829 %s | 834 %s | 779 %s | 730 %s | 757 %s | 839 %s | 840 %s | v2 610(sha256) %s | v2 626 %s | v2 627 %s'
       % (LOCK829_841[:12], LOCK834_841[:12], LOCK779_841[:12], LOCK730_841[:12], LOCK757_841[:12], LOCK839_841[:12],
          LOCK840_841[:12], LOCK610_841[:12], LOCK626_841[:12], LOCK627_841[:12]))
say841('Kilitli yardımcılar (AST, %d fonksiyon) SHA-256 %s' % (len(HELPERS841), HELPER_SHA841))
say841('BODY841 SHA-256 %s | yamalı kaynak AST geçti (%d bayt, SHA-256 %s)' % (BODY_SHA841, len(patched841), hashlib.sha256(patched841.encode()).hexdigest()))
say841('Kapsam: %d görülmemiş dünya, 21 kartuşluk 4 banka (+ yeni kimlikli kopyalar), %d iş (120 durum, 72 cevap, 60 eylem, 108 döngü) | '
       'K=%d yankı vektörü, döngü bütçesi %d adım' % (WORLDS841, WORLDS841 * 30, K_ECHO841, T_MAX841))
say841('Tam konsol kaydı: ' + str(FULL_CONSOLE841))
say841('=' * 78)
_fh841 = open(FULL_CONSOLE841, 'a', encoding='utf-8', buffering=1)
_fh841.write('TEST841_SOURCE_LOCKS ' + ' '.join((LOCK829_841, LOCK834_841, LOCK779_841, LOCK730_841, LOCK757_841, LOCK839_841, LOCK840_841, LOCK610_841, LOCK626_841, LOCK627_841)) +
             '\nTEST841_BODY_SHA256 ' + BODY_SHA841 + '\nTEST841_HELPERS ' + HELPER_SHA841 +
             '\nTEST841_PATCHED_SOURCE_AST_PASS ' + str(len(patched841)) + ' ' + hashlib.sha256(patched841.encode()).hexdigest() + '\n')
import linecache as _lc841
for _nm841, _src841 in (('TEST841_LOCKED_ENGINE', patched841), ('TEST841_LOCKED_HELPERS', HELPER_SRC841)):
    _lc841.cache[_nm841] = (len(_src841), None, [x + '\n' for x in _src841.splitlines()], _nm841)
_sys841.stdout = Console841(_ORIG_OUT841, _fh841); _sys841.stderr = Console841(_ORIG_ERR841, _fh841)
TEST841_ERROR = None
try:
    exec(compile(patched841, 'TEST841_LOCKED_ENGINE', 'exec'), globals())
except BaseException as _e841:
    TEST841_ERROR = _e841
    _tbtext841 = _tb841.format_exc()
    _fh841.write('\n[TEST841 OUTER EXCEPTION]\n' + _tbtext841)
finally:
    _sys841.stdout, _sys841.stderr = _ORIG_OUT841, _ORIG_ERR841
    try:
        _fh841.flush(); _fh841.close()
    except Exception:
        pass
    _dir841 = globals().get('DIR829')
    if _dir841 is not None and _P841(_dir841).exists() and FULL_CONSOLE841.exists():
        _dst841 = _P841(_dir841) / FULL_CONSOLE841.name
        _sh841.move(str(FULL_CONSOLE841), str(_dst841)); FULL_CONSOLE841 = _dst841
if TEST841_ERROR is not None:
    D_ = globals().get('D829', {}) if isinstance(globals().get('D829'), dict) else {}
    bad = [c for c in D_.get('checks', []) if not c.get('pass')]
    say841('=' * 78); say841('TEST841 HATA')
    say841('Tür: %s.%s' % (type(TEST841_ERROR).__module__, type(TEST841_ERROR).__name__))
    say841('Mesaj: ' + repr(TEST841_ERROR)[:800])
    say841('Aşama: ' + CON841['phase'] + ' | geçen %s dk' % _mins841())
    if bad:
        say841('Başarısız kapı: %s | ayrıntı: %s' % (bad[-1].get('name'), str(bad[-1].get('detail'))[:400]))
    say841('Hata öncesi son motor satırları:')
    for x in CON841['last'][-4:]:
        say841('  ' + x[:240])
    tbl = _tbtext841.rstrip().splitlines()
    say841('Traceback (son %d satır; tamamı dosyada ve results.json içinde):' % min(40, len(tbl)))
    for x in tbl[-40:]:
        say841('  ' + x)
    files_report841()
    say841('Tam konsol kaydı: %s  SHA-256 %s' % (FULL_CONSOLE841, sha_path841(FULL_CONSOLE841) if FULL_CONSOLE841.exists() else '-'))
    say841('Not: tamamlanan ölçümler vektör dosyalarında; hücre yeniden çalıştırılırsa SHA doğrulanıp yeniden kullanılır.')
    raise SystemExit('TEST841_FAILED: ' + type(TEST841_ERROR).__name__)
try:
    final841(D829)
except Exception as _e841s:
    say841('!! Özet basılamadı (veri dosyalarda tam): ' + repr(_e841s))
    say841(_tb841.format_exc()[-1500:])
files_report841()
say841('=' * 78)

