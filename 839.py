# AKBASCORE SILICON HIPPOCAMPUS — TEST839, single Colab cell (one A100-SXM4-80GB, frozen Qwen2.5-72B-Instruct NF4).
# MODEL-PRODUCED PHYSICAL ADDRESS TOKENS, APPLIED MECHANICALLY.
#   Every physical cartridge carries a random, content-independent Record ID inside its own body. With an 18-card bank
#   mounted (native CUT3), the frozen model is asked once which records it needs; its greedy output (locked 779
#   free_generate, argmax of its own logits) is decoded to text. The ONLY Python step between that output and the next
#   mount is execute_address839: literal Record-ID strings that exist in the mounted bank's directory are mounted in the
#   order of first emission; any other string is recorded as an invalid address and nothing is guessed or corrected. The
#   model then answers over exactly the cartridges it addressed. Equal-size random selection and the whole bank are
#   counterfactual comparison arms. Answers are scored offline only.
#   Levels reported separately: A = native ID selection while the bank fits in context; B = the applied address
#   causally determines the next model computation; C = finding the address WITHOUT mounting the bank (NOT TESTED).
#   No loop, no re-search, no stop decision is tested. No calibration, no threshold, no ranking, no similarity, no
#   classifier exists in this cell. Locked parts: TEST829 source (blob a5a25460), TEST834 mount/seal helpers (834.py
#   blob ab7b2046), TEST779 generation code (blob fa7017a8, bytecode-verified at runtime). No GPU execution or result
#   is claimed by the code author.
import urllib.request, hashlib, ast, json, time, random, math, re, numpy as np

REPO839 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
LOCK829_839 = "a5a25460a3a6bbdf62a0571a9b5ff19e64159cf7"
LOCK834_839 = "ab7b2046d7b7e7be18aed8c6ce5a1397e0c991d7"
LOCK779_839 = "fa7017a87f25ecef6ed2b2954a850599cb25fcd9"
LOCK838_839 = "99e4e28e06149d22bb33a40e3037f9b93270c1bb"
LOCK838LOG_839 = "469618a7c6e8d09356d6c467de255ce67e5894ba"   # prior evidence (read-only)
SEED839 = 8392026
EXPECTED_ARCH839 = (80, 8192, 64, 8, 128)
DEVICE_KIND839 = 'cuda'
WORLDS839 = 12                # sealed evaluation worlds, 4 banks of 3 worlds x 6 cards = 18 cartridges
BLOCK839 = 3
KINDS839 = ('first', 'second', 'changed', 'mirror', 'decoy', 'fork')
CONDS839 = ('FULL', 'REMOVE_SECOND', 'REMOVE_CONTINUATIONS', 'REMOVE_FIRST')
MAX_NEW_ADDR839 = 40          # ~4 Record IDs; a longer list is truncated by the token budget and recorded as such
MAX_NEW_ANS839 = 10
SEC_FUSION839, SEC_GEN839, MARGIN839 = 0.95, 0.35, 1.25   # TEST837/838 measured; 25 % safety margin
PRED_LIMIT_MIN839 = 240.0
HARD_BUDGET_MIN839 = 300.0
RESUME839 = True
# Predeclared criteria (counts; no fitted quantity anywhere)
A1_NEED839, A1_INVALID_MAX839 = 40, 4          # of 48 FULL episodes
A2_NEED839, A3_NEED839 = 20, 20                # of 24 pairs
A4_NEED839 = 18                                 # of 24 episodes per removal condition
B1_NEED839, B2_GAP839 = 96, 24                  # of 120 episodes; margin over each comparison arm

def fetch839(name, lock, limit=400000):
    with urllib.request.urlopen(urllib.request.Request(REPO839 + name, headers={"User-Agent": "AKBASCORE-TEST839"}),
                                timeout=180) as f:
        raw = f.read(limit + 1)
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert len(raw) <= limit and blob == lock, ("STOP_SOURCE_CHANGED", name, blob)
    return raw

raw829_839 = fetch839("829.py", LOCK829_839)
raw834_839 = fetch839("834.py", LOCK834_839)
raw779_839 = fetch839("779.py", LOCK779_839)
raw838_839 = fetch839("838.py", LOCK838_839)
raw838log_839 = fetch839("838.log", LOCK838LOG_839)
src839 = raw829_839.decode("utf-8")

def extract839(raw, body_name, names):
    tree = ast.parse(raw.decode("utf-8"))
    bodies = [n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == body_name]
    assert len(bodies) == 1, ('BODY_NOT_UNIQUE', body_name)
    text = bodies[0].value.value
    nodes = [n for n in ast.parse(text).body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert sorted(n.name for n in nodes) == sorted(names), ('HELPER_SET_MISMATCH', body_name)
    return "\n\n".join(ast.get_source_segment(text, n) for n in nodes)
HELPERS839 = ('mount834', 'seal834')
HELPER_SRC839 = extract839(raw834_839, 'BODY834', HELPERS839)
HELPER_SHA839 = hashlib.sha256(HELPER_SRC839.encode()).hexdigest()
# The locked generation function as it exists in 779.py (used for the runtime bytecode identity gate).
FG779_NODE839 = [n for n in ast.parse(raw779_839.decode('utf-8')).body
                 if isinstance(n, ast.FunctionDef) and n.name == 'free_generate']
AI779_NODE839 = [n for n in ast.parse(raw779_839.decode('utf-8')).body
                 if isinstance(n, ast.ClassDef) and n.name == 'AttentionIntervention']
assert len(FG779_NODE839) == 1 and len(AI779_NODE839) == 1, 'LOCKED_779_SYMBOLS'
FG_DEFAULTS839 = tuple(ast.literal_eval(d) for d in FG779_NODE839[0].args.defaults)
# Reference code objects: the blob-verified 779 prelude compiled EXACTLY as the locked TEST785 loader compiles it
# (same AST cut, same filename label). Compiled only, never executed. Bytecode depends on the module context (e.g. an
# imported module name compiles attribute calls differently), so only an identical pipeline is a valid reference.
def ref779_839(raw):
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
REF779_839 = ref779_839(raw779_839)

def patch839(text, old, new):
    assert text.count(old) == 1, ("PATCH_ANCHOR_NOT_UNIQUE", old[:80], text.count(old))
    return text.replace(old, new, 1)

src839 = patch839(src839, "SEED829 = 8292026", "SEED829 = %d" % SEED839)
src839 = patch839(src839, "RUN829 = 'TEST829_'", "RUN829 = 'TEST839_'")
src839 = patch839(src839, "WORLDS829 = 3                    # small pilot (directive); no automatic extension",
                  "WORLDS829 = %d                   # TEST839 sealed evaluation worlds" % WORLDS839)
for a839, b839 in (("'TEST829_results.json'", "'TEST839_results.json'"), ("'TEST829.log'", "'TEST839.log'"),
                   ("'TEST829_blind_review.csv'", "'TEST839_case_table.csv'"),
                   ("'TEST829_offline_key.json'", "'TEST829_base_offline_key.json'")):
    src839 = patch839(src839, a839, b839)

PANEL_EXT839 = r'''
# ---------------- TEST839 PANEL EXTENSION (sealed before any model call) ----------------
def fresh839():
    while True:
        c = code829()
        if c not in seen829:
            seen829.add(c); return c
# The base TEST829 cards carry no Record ID; they are removed and replaced by ID-bearing cartridges.
for w in worlds829:
    for cid in list(w['ids'].values()):
        cards829.pop(cid); card_meta829.pop(cid)
    w['fork_end'] = fresh839()
REL839 = {'first': ('start', 'middle'), 'second': ('middle', 'end'), 'changed': ('middle', 'changed_end'),
          'decoy': ('decoy_end', 'start'), 'mirror': ('end', 'middle'), 'fork': ('start', 'fork_end')}
RNGID839 = random.Random(SEED829 + 839001)        # Record IDs: independent stream, never derived from content
IDSEEN839 = set()
def rid839():
    while True:
        s = 'R' + ''.join(RNGID839.choice('0123456789') for _ in range(5))
        if s not in IDSEEN839:
            IDSEEN839.add(s); return s
def body839(rid, w, kind):
    a, b = REL839[kind]
    return ('Record ID: ' + rid + '\n' + 'Evidence record. Domain: ' + w['world'] + '\n' +
            'Directed relation: ' + w[a] + ' -> ' + w[b] + '.\n')
_rng839 = random.Random(SEED829 + 39)
CONTENT839 = {}          # cartridge -> (world index, kind)       OFFLINE ONLY
BLOCKS839 = []           # per bank: content order, cartridges per ID version
for bi in range(0, len(worlds829), BLOCK839):
    contents = [(wi, k) for wi in range(bi, bi + BLOCK839) for k in KINDS839]
    r0 = [rid839() for _ in contents]
    while True:                                   # v1: a derangement of the v0 IDs over the same contents
        r1 = list(r0); _rng839.shuffle(r1)
        if all(a != b for a, b in zip(r0, r1)):
            break
    ver = {}
    for vi, rids in enumerate((r0, r1)):
        ver[vi] = {}
        for (wi, k), rid in zip(contents, rids):
            cid = 'E839_' + code829()
            assert cid not in cards829, 'CARD_ID_COLLISION'
            cards829[cid] = body839(rid, worlds829[wi], k)
            card_meta829[cid] = {'domain': worlds829[wi]['world'], 'kind': k, 'record_id': rid, 'id_version': vi,
                                 'body_sha256': sha829(cards829[cid])}
            CONTENT839[cid] = (wi, k)
            ver[vi][(wi, k)] = (cid, rid)
    order = list(contents); _rng839.shuffle(order)
    BLOCKS839.append({'contents': contents, 'order': order, 'ver': ver, 'worlds': list(range(bi, bi + BLOCK839))})
for b_ in BLOCKS839:
    for (wi, k), (cid, rid) in b_['ver'][0].items():
        worlds829[wi]['ids'][k] = cid           # v0 cartridges (offline key convenience)
NAMES839 = {w[k] for w in worlds829 for k in ('world', 'start', 'middle', 'end', 'changed_end', 'decoy_end', 'fork_end')}
assert len(NAMES839) == 7 * len(worlds829), 'NAME_COLLISION'
assert len(IDSEEN839) == 6 * len(worlds829), 'RECORD_ID_COLLISION'
QID839 = [questions829[i]['qid'] for i in range(len(worlds829))]
assert len(questions829) == len(worlds829), 'ONE_QUESTION_PER_WORLD'
REMOVE839 = {'FULL': (), 'REMOVE_SECOND': ('second',), 'REMOVE_CONTINUATIONS': ('second', 'changed'), 'REMOVE_FIRST': ('first',)}
EPIS839, EVALKEY839 = [], {}          # EVALKEY: offline key only
def episode839(bank, directory, qid, role):
    e = 'P839_' + ''.join(_rng839.choice('0123456789ABCDEF') for _ in range(12))
    EPIS839.append({'ep': e, 'bank': list(bank), 'directory': dict(directory), 'qid': qid})
    EVALKEY839[e] = role
for bi, b_ in enumerate(BLOCKS839):
    for order in ('FORWARD', 'REVERSE'):
        seq = b_['order'] if order == 'FORWARD' else list(reversed(b_['order']))
        for vi in (0, 1):                                      # FULL: one bank mount serves the bank's 3 questions
            bank = [b_['ver'][vi][c][0] for c in seq]
            directory = {b_['ver'][vi][c][1]: b_['ver'][vi][c][0] for c in seq}
            for wi in b_['worlds']:
                episode839(bank, directory, QID839[wi], {'world': wi, 'cond': 'FULL', 'order': order, 'id_version': vi, 'block': bi})
        for wi in b_['worlds']:
            for cond in CONDS839[1:]:
                keep = [c for c in seq if not (c[0] == wi and c[1] in REMOVE839[cond])]
                bank = [b_['ver'][0][c][0] for c in keep]
                directory = {b_['ver'][0][c][1]: b_['ver'][0][c][0] for c in keep}
                episode839(bank, directory, QID839[wi], {'world': wi, 'cond': cond, 'order': order, 'id_version': 0, 'block': bi})
_rng839.shuffle(EPIS839)
assert len(EVALKEY839) == len(EPIS839) == 4 * 3 * 2 * 2 + 4 * 3 * 3 * 2, 'EPISODE_COUNT'
assert all(cards829[c].startswith('Record ID: ' + r + '\n') for e_ in EPIS839 for r, c in e_['directory'].items()), 'RECORD_ID_IN_BODY'
GROUPS839, GORDER839 = {}, []
for e_ in EPIS839:
    m = tuple(e_['bank'])
    if m not in GROUPS839:
        GROUPS839[m] = []; GORDER839.append(m)
    GROUPS839[m].append(e_['ep'])

def fus_upper839(k, maxb, p_):
    if k <= 0:
        return 0
    c = int(globals().get('CHUNK', 128))
    return (p_ + maxb + c - 1) // c + (k - 1) * ((maxb + c - 1) // c)

def cost_upper839(tok_of, p_):
    mx = max(tok_of.values())
    up = {'fusion_forwards': 0, 'probe_forwards': 3, 'capture_forwards': 0, 'rank_forwards': 0, 'generation_forwards': 1}
    up['fusion_forwards'] += 2 * fus_upper839(max(len(m) for m in GROUPS839), mx, p_) + 2   # noninterference, replay
    for m, eps in GROUPS839.items():
        up['fusion_forwards'] += fus_upper839(len(m), mx, p_)                 # bank mount
        up['fusion_forwards'] += len(eps) * 2 * fus_upper839(len(m), mx, p_)  # self + random mounts (worst case)
        up['generation_forwards'] += len(eps) * (MAX_NEW_ADDR839 + 3 * MAX_NEW_ANS839)
    up['generation_forwards'] += MAX_NEW_ADDR839                               # determinism replay
    sec = MARGIN839 * (up['fusion_forwards'] * SEC_FUSION839 + up['generation_forwards'] * SEC_GEN839 +
                       120.0 + len(tok_of) * 2.0)
    return {'numeric_upper': up, 'episodes': len(EPIS839), 'bank_mounts': len(GROUPS839),
            'physical_cartridges': len(tok_of), 'max_bank_tokens': max(p_ + sum(tok_of[c] for c in m) for m in GROUPS839),
            'minutes_upper_excluding_model_load': round(sec / 60.0, 1),
            'cost_model': 'fusion %.2f s, generated token %.2f s, x%.2f margin, worst-case self/random mounts = bank size'
                          % (SEC_FUSION839, SEC_GEN839, MARGIN839)}
'''
src839 = patch839(src839,
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n",
    "card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}\n" + PANEL_EXT839)
PRECOST839 = r'''
    PRE839 = cost_upper839(tok_counts829, 30)
    D829['predicted_cost839_pre_model'] = PRE839
    log829('TEST839_PREDICTED_COST_BEFORE_MODEL_LOAD', json.dumps(PRE839))
    gate829('TEST839_PREDICTED_BUDGET', PRE839['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN839,
            {'minutes_upper': PRE839['minutes_upper_excluding_model_load'], 'limit': PRED_LIMIT_MIN839})
'''
# Source-level verification BEFORE the model is loaded (fails closed in seconds, not after the 13-minute load).
SRCVER839 = r'''
# ---------------- SOURCE-LEVEL VERIFICATION: the address is the model's own computation ----------------
def copy_receivers839(src):
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'copy':
            r = n.func.value
            out.append(isinstance(r, ast.Call) and isinstance(r.func, ast.Attribute) and r.func.attr == 'numpy')
    return out
cr839 = copy_receivers839(HELPER_SRC839) + copy_receivers839(BODY839_TEXT) + copy_receivers839(SRCVER839_TEXT)
gate829('STATIC_COPY_RECEIVERS_ARE_NDARRAY', all(cr839), {'copy_calls': len(cr839)})
MARK839 = '# ====== OFFLINE' + ' PHASE MARKER ======'
gate829('OFFLINE_MARKER_UNIQUE', BODY839_TEXT.count(MARK839) == 1)
pre839 = ast.parse(BODY839_TEXT.split(MARK839)[0])
hook839 = ast.parse(SRCVER839_TEXT)
LABELS839 = {'EVALKEY839', 'CONTENT839', 'worlds829', 'card_meta829', 'NAMES839', 'BLOCKS839', 'REMOVE839'}
used839 = {n.id for t_ in (pre839, hook839) for n in ast.walk(t_) if isinstance(n, ast.Name)}
gate829('STATIC_NO_LABELS_BEFORE_OFFLINE', not (used839 & LABELS839), sorted(used839 & LABELS839))
# (1) generation = locked TEST779 code: the engine's functions are compared with the code objects obtained by compiling
#     the SAME blob-verified 779 prelude the SAME way the locked TEST785 loader does (no execution of that compile).
def code_sig839(co):
    return (co.co_code, co.co_names, co.co_varnames, co.co_argcount, co.co_kwonlyargcount, co.co_flags,
            tuple(code_sig839(c) if hasattr(c, 'co_code') else repr(c) for c in co.co_consts))
import inspect as _insp839
def cmp839(live, ref):
    return {'bytecode_and_constants': code_sig839(live) == code_sig839(ref), 'filename': live.co_filename == ref.co_filename,
            'first_line': live.co_firstlineno == ref.co_firstlineno, 'name': live.co_name == ref.co_name,
            'live_filename': live.co_filename}
fg_unwrapped839 = _insp839.unwrap(free_generate)
LB839 = {'free_generate': cmp839(fg_unwrapped839.__code__, REF779_839['free_generate'])}
LB839['free_generate']['defaults'] = fg_unwrapped839.__defaults__ == FG_DEFAULTS839
LB839['free_generate']['decorator'] = [ast.unparse(d) for d in FG779_NODE839[0].decorator_list] == ['torch.no_grad()']
for m_ in ('__init__', '__enter__', '__exit__'):
    LB839['AttentionIntervention.' + m_] = cmp839(getattr(AttentionIntervention, m_).__code__, REF779_839['AttentionIntervention.' + m_])
CUT3INFO839 = {m_: cmp839(getattr(Cut3Diagnostic, m_).__code__, REF779_839['Cut3Diagnostic.' + m_])
               for m_ in ('__init__', '__enter__', '__exit__')}                   # informational (stubbed in the CPU sim)
D829['locked_bytecode839'] = {'gated': LB839, 'informational_Cut3Diagnostic': CUT3INFO839}
gate829('LOCKED_FREE_GENERATE_BYTECODE', all(v for k, v in LB839['free_generate'].items() if k != 'live_filename'),
        LB839['free_generate'])
gate829('LOCKED_ATTENTION_INTERVENTION_BYTECODE',
        all(all(v for k, v in LB839['AttentionIntervention.' + m_].items() if k != 'live_filename')
            for m_ in ('__init__', '__enter__', '__exit__')), {k: v for k, v in LB839.items() if k.startswith('Att')})
log829('TEST839_CUT3_BYTECODE_INFO', json.dumps({m_: v['bytecode_and_constants'] for m_, v in CUT3INFO839.items()}))
fgsrc839 = ast.unparse(FG779_NODE839[0])
gate829('FREE_GENERATE_IS_GREEDY_ARGMAX', 'next_id = int(out.logits[0, -1].argmax().item())' in fgsrc839 and
        fgsrc839.count('argmax') == 1 and not any(t in fgsrc839 for t in ('multinomial', 'sample', 'topk', 'softmax')),
        fgsrc839.count('argmax'))
# (2) every free_generate call: seed=None, gain=0., spans=None (=> Cut3Diagnostic and AttentionIntervention are
#     observation-only: no seed injection, no attention bias), prompt built only from a sealed frame + question text
calls839 = [n for n in ast.walk(ast.parse(BODY839_TEXT)) if isinstance(n, ast.Call) and
            isinstance(n.func, ast.Name) and n.func.id == 'free_generate']
def call_ok839(n):
    kw = {k.arg: k.value for k in n.keywords}
    return (len(n.args) == 2 and isinstance(kw.get('seed'), ast.Constant) and kw['seed'].value is None and
            isinstance(kw.get('gain'), ast.Constant) and kw['gain'].value == 0 and
            isinstance(kw.get('spans'), ast.Constant) and kw['spans'].value is None and
            isinstance(n.args[1], ast.Call) and isinstance(n.args[1].func, ast.Name) and
            n.args[1].func.id in ('address_prompt839', 'answer_prompt829') and len(n.args[1].args) == 1 and
            ast.unparse(n.args[1].args[0]).startswith('QTEXT839['))
gate829('STATIC_GENERATION_CALLS_UNMODIFIED', len(calls839) == 2 and all(call_ok839(n) for n in calls839), len(calls839))
# (3) the address frame is a sealed constant; the answer frame never receives address text (no replay)
def address_prompt839(question):
    return ADDRESS_FRAME839 + question
apn839 = [n for n in hook839.body if isinstance(n, ast.FunctionDef) and n.name == 'address_prompt839'][0]
gate829('STATIC_ADDRESS_FRAME_CONSTANT', ast.unparse(apn839.body[0]) == 'return ADDRESS_FRAME839 + question' and
        len(apn839.body) == 1 and isinstance(ADDRESS_FRAME839, str))
# (4) the mechanical executor: literal lookup only (AST whitelist)
ID_RE839 = re.compile(ID_PATTERN839)
def execute_address839(raw, directory):
    found = ID_RE839.findall(raw)
    mount = []
    invalid = []
    for s in found:
        if s in directory:
            if directory[s] not in mount:
                mount.append(directory[s])
        else:
            invalid.append(s)
    return {'found': found, 'mount': mount, 'invalid': invalid}
exn839 = [n for n in hook839.body if isinstance(n, ast.FunctionDef) and n.name == 'execute_address839'][0]
names839 = {n.id for n in ast.walk(exn839) if isinstance(n, ast.Name)}
attrs839 = {n.func.attr for n in ast.walk(exn839) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
fcalls839 = [n for n in ast.walk(exn839) if isinstance(n, ast.Call) and not isinstance(n.func, ast.Attribute)]
nodes839 = {type(n).__name__ for n in ast.walk(exn839)}
gate829('STATIC_EXECUTOR_LITERAL_LOOKUP_ONLY',
        names839 <= {'ID_RE839', 'raw', 'directory', 'found', 'mount', 'invalid', 's'} and attrs839 <= {'findall', 'append'}
        and not fcalls839 and not (nodes839 & {'Lambda', 'Compare_sorted', 'ListComp', 'GeneratorExp', 'While', 'Try',
                                               'BinOp', 'Global', 'Import', 'ImportFrom'}),
        {'names': sorted(names839), 'calls': sorted(attrs839), 'nodes': sorted(nodes839)})
gate829('EXECUTOR_PATTERN', ID_RE839.findall('R12345 xR12345 R123456 R1234 R54321.') == ['R12345', 'R54321'])
gate829('EXECUTOR_NO_CORRECTION', execute_address839('R00001 R00002 R00001', {'R00002': 'X'}) ==
        {'found': ['R00001', 'R00002', 'R00001'], 'mount': ['X'], 'invalid': ['R00001', 'R00001']})
D829['source_verification839'] = True
log829('TEST839_SOURCE_VERIFIED_BEFORE_MODEL_LOAD')
'''
SRCVER839_TEXT = SRCVER839
src839 = patch839(src839, "    del tok829\n", "\n".join("    " + l if l else "" for l in SRCVER839.strip("\n").splitlines()) +
                  "\n    del tok829\n" + PRECOST839)

# ---- the only two interfaces between the model and the physical memory (sealed, verified by AST gates) ----
ADDRESS_FRAME839 = ('Each mounted evidence record begins with its Record ID (the letter R followed by five digits). '
                    'List the Record IDs of exactly the records needed to answer the question, in the order in which '
                    'they are used, separated by single spaces. If the mounted records cannot answer the question, '
                    'reply NONE. Reply only with Record IDs or NONE. Question: ')
ID_PATTERN839 = r'(?<![A-Za-z0-9])R[0-9]{5}(?![A-Za-z0-9])'

HYP839 = {
    'question': ('Does the frozen model, from its own computation over mounted physical memory, produce a content-'
                 'dependent physical address (Record ID) that, applied mechanically, causally determines its next '
                 'computation?'),
    'levels': {'A': 'native Record-ID selection while the whole bank is mounted (fits in context)',
               'B': 'the mechanically applied address determines the next model computation (answer over the addressed mount)',
               'C': 'finding the address without mounting the bank: NOT TESTED; large-scale autonomous addressing is NOT claimed'},
    'mechanical_executor': ('execute_address839: regex finds literal strings R + 5 digits in the decoded greedy output; '
                            'a string that is a key of the mounted bank directory is mounted once, in first-emission '
                            'order; every other string is an invalid address (recorded, never corrected); no valid '
                            'address -> the NULL control memory is mounted.'),
    'controls': ['random content-independent Record IDs (separate RNG stream)',
                 'ID swap: the same contents re-forged with a derangement of the IDs (v1)',
                 'bank order FORWARD / REVERSE',
                 'removal of the needed cartridge(s): REMOVE_SECOND (alternative continuation remains), '
                 'REMOVE_CONTINUATIONS (no continuation), REMOVE_FIRST (only the fork starts at the question start)',
                 'fork, mirror, inbound decoy and two other worlds\' complete chains present in every bank',
                 'invalid addresses: no correction; empty address: NULL memory',
                 'equal-size random selection from the same bank and the whole bank as comparison arms',
                 'answers scored offline only'],
    'criteria': {
        'A1_FULL_ADDRESS': ('FULL (48 episodes = 12 questions x 2 orders x 2 ID versions): the addressed set contains the '
                            'own first link and a valid continuation (second or changed) and no other cartridge in >= 40; '
                            'episodes with any invalid address <= 4.'),
        'A2_CONTENT_FOLLOWING': 'ID swap: same addressed contents for v0 and v1 in >= 20 of 24 (question, order) pairs.',
        'A3_ORDER_INVARIANCE': ('FORWARD and REVERSE give the same addressed contents, or both give a clean own chain '
                                '(either valid continuation), in >= 20 of 24 (question, version) pairs; strict content '
                                'identity is reported separately.'),
        'A4_REMOVAL': ('REMOVE_SECOND: first + changed and nothing else in >= 18 of 24. REMOVE_CONTINUATIONS and '
                       'REMOVE_FIRST: addressed set contains no cartridge outside the own chain and no invalid address '
                       'in >= 18 of 24 each.'),
        'B1_SELF_ANSWER': ('answer over the self-addressed mount correct in >= 96 of 120 episodes (FULL: end or '
                           'alternative end only; REMOVE_SECOND: alternative end only; REMOVE_CONTINUATIONS / '
                           'REMOVE_FIRST: UNKNOWN only).'),
        'B2_CAUSAL': ('self-addressed correct >= whole-bank correct + 24 and >= equal-size random correct + 24 '
                      '(of 120).'),
        'C_WITHOUT_BANK': 'NOT_TESTED'},
    'decision': ('DEVAM if A1..A4 and B1, B2 PASS. DUR if A1 FAIL. Otherwise YETERSİZ KANIT. A budget stop forces '
                 'YETERSİZ KANIT. MODEL-NATIVE OTONOMİ is not demonstrated by this test (no loop, no stop, level C '
                 'not tested); it is FAIL if any external cognitive control is detected.'),
    'classes': {'Record-ID tokens, answers': 'A (model computation: attention over mounted CUT3 memory + greedy argmax)',
                'execute_address839': 'mechanical literal lookup (no ranking, no similarity, no threshold, no correction)',
                'fixed two-phase protocol (address once, answer once)': 'experiment infrastructure, identical for all episodes',
                'random arm': 'counterfactual control only, never feeds a decision'}}

CLAIMS839 = {
    'verified_from_prior_research': [
        '838.log (blob 469618a7): with the true pair mounted the model answers the end 12/12; wrong pairs UNKNOWN '
        '(FORK+SECOND 12/12, IRRELEVANT 12/12, FIRST+MIRROR 9/12, DECOY+FIRST only 4/12); relational information is '
        'linearly readable from one forward, but only by a Python reader (class B) and a class C pair scan.',
        '837.log: with an 18-card bank mounted the model answers correctly 1/6 (context loss).',
        'TEST919: model-written control commands over opaque IDs without content binding: half invalid, no model stop.'],
    'implemented_in_TEST839': ['Record IDs inside the cartridges; one address generation; literal mechanical execution; '
                               'answer over the addressed mount; random / whole-bank counterfactuals; ID swap, order and '
                               'removal controls.'],
    'demonstrated_by_TEST839': 'filled only from this run'}

BODY839 = r'''
D829['test'] = '839'
D829['controller'] = 'NONE. Address = model greedy output; executor = literal Record-ID lookup (mechanical); no loop.'
D829['sources839'] = {'829': LOCK829_839, '834': LOCK834_839, '779': LOCK779_839, '838': LOCK838_839,
                      '838_log': LOCK838LOG_839, 'helpers_sha256': HELPER_SHA839, 'helpers': list(HELPERS839)}
D829['hypotheses839'] = PANEL829['test839']['hypotheses']
D829['limitations'] = [
    'The whole 18-card bank is mounted while the model writes the address (level A). Addressing without mounting the '
    'bank (level C) is not tested; no large-scale or million-cartridge addressing is claimed.',
    'Address and answer are two fixed phases identical for every episode; no re-search, revision or stop decision is tested.',
    'The address channel is text (Record-ID tokens) by explicit user decision; it is not accepted as the final architecture.',
    'The address frame and the TEST827 answer frame are boundary instructions; the answer frame names UNKNOWN.',
    'Twelve sealed worlds, one card template, one question template, one model.',
    'No GPU execution or result is claimed by the code author.']
gate829('PANEL_FRESH_SEED', SEED829 == SEED839, SEED829)
gate829('NO_CONTROL_TEXT', MAX_NEW_CONTROL829 == 0)
gate829('WORLD_COUNT', len(questions829) == WORLDS839 and len(QID839) == WORLDS839)
gate829('EPISODES_UNIQUE', len({e['ep'] for e in EPIS839}) == len(EPIS839), len(EPIS839))
gate829('DIRECTORY_IS_BANK', all(sorted(e['directory'].values()) == sorted(e['bank']) and
                                 len(e['directory']) == len(e['bank']) for e in EPIS839))
gate829('CARTRIDGES_PHYSICAL', all(c in entries for e in EPIS839 for c in e['bank']) and NULL829 in entries)
gate829('SOURCE_VERIFICATION_DONE_BEFORE_MODEL_LOAD', bool(D829.get('source_verification839')))
# ---------------- engine / model gates ----------------
exec(compile(HELPER_SRC839, 'TEST839_LOCKED_HELPERS', 'exec'), globals())
gate829('HELPERS_LOADED', all(callable(globals().get(x)) for x in HELPERS839), HELPER_SHA839)
gate829('ENGINE_SYMBOLS839', all(callable(globals().get(x)) for x in
        ('build_fusion', 'kv_digest', 'safe_load', 'free_generate', 'answer_prompt829', 'Cut3Diagnostic',
         'AttentionIntervention', 'cache_build', 'prompt_ids')))
gate829('ARCH_DIMS', (NL, H, QH, KVH, HD) == EXPECTED_ARCH839 and int(model.config.num_attention_heads) == QH and
        int(model.config.num_key_value_heads) == KVH and int(model.config.hidden_size) == H, (NL, H, QH, KVH, HD))
gate829('BF16_COMPUTE', DTYPE == _torch829.bfloat16, str(DTYPE))
gate829('NF4_LINEAR4BIT', any(isinstance(m_, bitsandbytes.nn.Linear4bit) for m_ in model.modules()))
gate829('WEIGHTS_FROZEN', all(not p_.requires_grad for p_ in model.parameters()))
gate829('DEVICE', str(DEV).startswith(DEVICE_KIND839), str(DEV))
gate829('SDPA_MODULE', F is _torch829.nn.functional and F.scaled_dot_product_attention is SDPA829)
gate829('NO_RESIDUAL_HOOKS_START', all(not model.model.layers[i]._forward_hooks and not model.model.layers[i]._forward_pre_hooks
                                       for i in range(NL)))
gate829('PREFIX_P', P == 30, P)

gate829('PRIOR_LOG_PRESENT', b'TEST838' in raw838log_839 and b'NOT_DEMONSTRATED' in raw838log_839)
POST839 = cost_upper839({c: int(entries[c]['body_tokens']) for c in cards829}, P)
D829['predicted_cost839'] = POST839
log829('TEST839_PREDICTED_COST', json.dumps(POST839))
gate829('PREDICTED_BUDGET_POST_LOAD', POST839['minutes_upper_excluding_model_load'] <= PRED_LIMIT_MIN839,
        POST839['minutes_upper_excluding_model_load'])
QTEXT839 = {q['qid']: q['question'] for q in questions829}
LPMAX839 = max(max(len(prompt_ids(address_prompt839(t))), len(prompt_ids(answer_prompt829(t)))) for t in QTEXT839.values())
gate829('FUSION_TOKENS_WITH_PROMPT', POST839['max_bank_tokens'] + LPMAX839 + MAX_NEW_ADDR839 + 16 <= MAX_FUSED_TOKENS,
        {'bank': POST839['max_bank_tokens'], 'prompt': LPMAX839, 'limit': MAX_FUSED_TOKENS})
try:
    free839, _ = _torch829.cuda.mem_get_info()
    gate829('VRAM_HEADROOM', free839 / 2**30 >= 8.0, round(free839 / 2**30, 2))
except Exception as e839:
    gate829('VRAM_HEADROOM', False, repr(e839))
D829['noninterference839'] = noninterference829([NULL829], questions829[0]['question'])
for k839, v839 in D829['noninterference839'].items():
    gate829('NONINTERFERENCE_' + k839.upper(), bool(v839), v839)
COUNT834 = {'fusion_forwards': fusion_forwards829([NULL829]), 'probe_forwards': 3, 'capture_forwards': 0,
            'rank_forwards': 0, 'generation_forwards': 1, 'mounts': 1}
T0_839 = time.perf_counter()
SEAL_LAYERS834 = (0, CUT, NL // 2, NL - 1)

# ---- per-episode record store (SHA-256 manifest; episode-level resume) ----
EDIR839 = DIR829 / 'TEST839_episodes'
EDIR839.mkdir(exist_ok=True)
MAN839 = DIR829 / 'TEST839_episode_manifest.jsonl'
HEADER839 = {'panel_sha256': PANEL_SHA829, 'body_sha256': PANEL829['test839']['body_sha256'], 'helpers_sha256': HELPER_SHA839}
REC839 = {}
D829['resume839'] = {'enabled': RESUME839, 'source': None, 'reused_episodes': 0, 'reason': None}
if RESUME839:
    for cand in sorted(DIR829.parent.glob('TEST839_*/TEST839_episode_manifest.jsonl'), reverse=True):
        if cand.parent == DIR829:
            continue
        try:
            lines = cand.read_text(encoding='utf-8').splitlines()
            if not lines or json.loads(lines[0]).get('header') != HEADER839:
                D829['resume839']['reason'] = 'header mismatch in ' + str(cand); continue
            got = {}
            for ln in lines[1:]:
                o = json.loads(ln); f = cand.parent / 'TEST839_episodes' / o['file']
                if f.exists() and sha_file(f) == o['sha256']:
                    got[o['key']] = json.loads(f.read_text(encoding='utf-8'))
            REC839.update({k: v for k, v in got.items() if v.get('complete')})
            D829['resume839'].update({'source': str(cand), 'reused_episodes': len(REC839),
                                      'reason': 'header and per-file SHA-256 verified'})
            break
        except Exception as e839r:
            D829['resume839']['reason'] = 'unreadable ' + str(cand) + ' ' + repr(e839r)
log829('TEST839_RESUME', json.dumps(D829['resume839']))
with MAN839.open('w', encoding='utf-8') as fh839:
    fh839.write(json.dumps({'header': HEADER839}, sort_keys=True) + '\n')
def save_rec839(key, rec):
    f = EDIR839 / (key + '.json')
    f.write_text(json.dumps(rec, sort_keys=True), encoding='utf-8')
    with MAN839.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps({'key': key, 'file': f.name, 'sha256': sha_file(f)}, sort_keys=True) + '\n')
for k839 in list(REC839):
    save_rec839(k839, REC839[k839])

# ==================================================================================================================
# RUNTIME. Episodes are opaque IDs. The runtime never reads which cartridge is which. The model writes the address;
# execute_address839 applies it literally; the model answers over what it addressed.
# ==================================================================================================================
BUDGET_STOP839 = False
EPMAP839 = {e['ep']: e for e in EPIS839}
def gen839(memx, qid, frame, max_new):
    if frame == 'ADDRESS':
        o = free_generate(memx, address_prompt839(QTEXT839[qid]), seed=None, gain=0., max_new=max_new, spans=None)
    else:
        o = free_generate(memx, answer_prompt829(QTEXT839[qid]), seed=None, gain=0., max_new=max_new, spans=None)
    COUNT834['generation_forwards'] += int(o['generated_tokens'])
    return {'raw': o['raw'], 'generated_tokens': int(o['generated_tokens']), 'budget_exhausted': int(o['generated_tokens']) >= max_new}
def answer_over839(cards, qid, tag):
    memx, n = mount834(list(cards), tag)
    seal = seal834(memx)
    a = gen839(memx, qid, 'ANSWER', MAX_NEW_ANS839)
    gate829('MEAS_KV_SEAL_' + tag, seal834(memx) == seal)
    del memx; gc.collect(); release()
    return a
t_run839 = time.perf_counter()
ng839 = len(GORDER839); step839 = max(1, ng839 // 4)
log829('TEST839_PROGRESS', 'BANKS', 0, '/', ng839)
for gi839, m839 in enumerate(GORDER839):
    todo = [x for x in GROUPS839[m839] if x not in REC839]
    if todo:
        if (time.perf_counter() - T0_839) / 60.0 > HARD_BUDGET_MIN839:
            BUDGET_STOP839 = True; log829('TEST839_BUDGET_STOP', 'bank', gi839, 'of', ng839); break
        memB, nB = mount834(list(m839), 'BANK_G%d' % gi839)
        sealB = seal834(memB)
        part = {}
        for ep in todo:
            e = EPMAP839[ep]
            part[ep] = {'address': gen839(memB, e['qid'], 'ADDRESS', MAX_NEW_ADDR839),
                        'whole_bank_answer': gen839(memB, e['qid'], 'ANSWER', MAX_NEW_ANS839)}
        gate829('MEAS_KV_SEAL_BANK_G%d' % gi839, seal834(memB) == sealB)
        del memB; gc.collect(); release()
        for ep in todo:
            e = EPMAP839[ep]
            ex = execute_address839(part[ep]['address']['raw'], e['directory'])     # the only Python step
            self_mount = ex['mount'] if ex['mount'] else [NULL829]
            gate829('APPLIED_EXACTLY_' + ep, self_mount == (ex['mount'] or [NULL829]) and
                    all(c in e['bank'] for c in ex['mount']))
            sa = answer_over839(self_mount, e['qid'], 'SELF_' + ep)
            k = len(ex['mount'])
            rr = random.Random(int(hashlib.sha256(('RANDOM_ARM|' + ep).encode()).hexdigest()[:12], 16))
            rmount = rr.sample(list(e['bank']), k) if k else [NULL829]                  # counterfactual control only
            ra = answer_over839(rmount, e['qid'], 'RAND_' + ep)
            rec = {'ep': ep, 'qid': e['qid'], 'bank_size': len(e['bank']), 'address': part[ep]['address'],
                   'executor': ex, 'self_mount': self_mount, 'self_mount_sha256': [entries[c]['sha256'] for c in self_mount],
                   'self_answer': sa, 'random_mount': rmount, 'random_answer': ra,
                   'whole_bank_answer': part[ep]['whole_bank_answer'], 'complete': True}
            REC839[ep] = rec; save_rec839(ep, rec)
    if (gi839 + 1) % step839 == 0 or gi839 + 1 == ng839:
        log829('TEST839_PROGRESS', 'BANKS', gi839 + 1, '/', ng839)
D829['run_seconds839'] = round(time.perf_counter() - t_run839, 3)
# determinism: one address generation replayed on a fresh mount of the same bank
epR839 = EPIS839[0]
if epR839['ep'] in REC839 and not BUDGET_STOP839:
    memR, nR = mount834(list(epR839['bank']), 'REPLAY')
    rp = gen839(memR, epR839['qid'], 'ADDRESS', MAX_NEW_ADDR839)
    D829['determinism839'] = {'address_text_identical': rp['raw'] == REC839[epR839['ep']]['address']['raw'],
                              'original': REC839[epR839['ep']]['address']['raw'], 'replay': rp['raw']}
    log829('TEST839_DETERMINISM', json.dumps(D829['determinism839']))       # recorded; a mismatch forces YETERSİZ KANIT
    del memR; gc.collect(); release()
else:
    D829['determinism839'] = {'address_text_identical': None}
D829['budget_stop839'] = BUDGET_STOP839

engine_bindings829('FINAL')
gate829('FROZEN_WEIGHT_SENTINEL', before829 == sentinel())
gate829('NO_RESIDUAL_HOOKS', all(not model.model.layers[i]._forward_hooks and not model.model.layers[i]._forward_pre_hooks
                                 for i in range(NL)))
gate829('NO_ATTENTION_HOOKS', all(not model.model.layers[i].self_attn._forward_hooks and
                                  not model.model.layers[i].self_attn._forward_pre_hooks for i in range(NL)))
gate829('SDPA_RESTORED_FINAL', F.scaled_dot_product_attention is SDPA829)
gate829('LM_HEAD_UNWRAPPED', model.lm_head.__dict__.get('forward') is HEAD_FWD829 and
        not model.lm_head._forward_hooks and not model.lm_head._forward_pre_hooks)
gate829('PANEL_UNCHANGED', sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True)) == PANEL_SHA829)
for cid839 in cards829:
    gate829('FINAL_SHA_' + cid839, sha_file(CART_DIR / entries[cid839]['file']) == entries[cid839]['sha256'])
COUNT_NUMERIC839 = dict(COUNT834)
gate829('COUNTED_WITHIN_UPPER_BOUND', all(COUNT_NUMERIC839[k] <= POST839['numeric_upper'][k] for k in POST839['numeric_upper']),
        {'counted': COUNT_NUMERIC839, 'upper': POST839['numeric_upper']})

# ====== OFFLINE PHASE MARKER ======
# OFFLINE PHASE: every generation is finished and saved; labels are read only from here.
log829('TEST839_OFFLINE_START')
def frac839(xs):
    return [sum(1 for x in xs if x), len(xs)]
def ok839(k, n, need, full):
    return 'INCONCLUSIVE' if n < full else ('PASS' if k >= need else 'FAIL')
def role839(cid, wi):
    if cid == NULL829:
        return 'NULL'
    cw, k = CONTENT839[cid]
    return ('OWN_' if cw == wi else 'OTHER_') + k.upper()
def tcls839(t, w):
    u = (t or '').upper()
    names = [nm for nm, c in (('END', w['end']), ('ALT_END', w['changed_end']), ('MIDDLE', w['middle']), ('START', w['start']),
                              ('FORK_END', w['fork_end']), ('DECOY', w['decoy_end'])) if c in u]
    others = sorted({nm for nm in NAMES839 if nm in u and nm not in (w['end'], w['changed_end'], w['middle'], w['start'],
                                                                         w['fork_end'], w['decoy_end'], w['world'])})
    return names + (['OTHER_WORLD_NAME'] if others else []) + (['UNKNOWN'] if 'UNKNOWN' in u else [])
def tcat839(cls):
    if not cls:
        return 'EMPTY_OR_OTHER'
    if cls == ['UNKNOWN']:
        return 'UNKNOWN'
    if 'UNKNOWN' in cls:
        return 'MIXED'
    return {('END',): 'END', ('ALT_END',): 'ALT_END'}.get(tuple(cls), 'OTHER:' + '+'.join(cls))
EXPECT839 = {'FULL': ('END', 'ALT_END'), 'REMOVE_SECOND': ('ALT_END',), 'REMOVE_CONTINUATIONS': ('UNKNOWN',),
             'REMOVE_FIRST': ('UNKNOWN',)}
def aclass839(roles):
    s = set(roles)
    chain = {'OWN_FIRST', 'OWN_SECOND', 'OWN_CHANGED'}
    if not s or s == {'NULL'}:
        return 'EMPTY'
    if 'OWN_FIRST' in s and s & {'OWN_SECOND', 'OWN_CHANGED'}:
        return 'CHAIN' if s <= chain else 'CHAIN_WITH_EXTRA'
    return 'PARTIAL_OWN' if s <= chain else 'DISTRACTED'
EV839 = []
for e in EPIS839:
    r = REC839.get(e['ep'])
    if r is None:
        continue
    k = EVALKEY839[e['ep']]; wi = k['world']; w = worlds829[wi]
    roles = [role839(c, wi) for c in r['executor']['mount']]
    content = sorted(CONTENT839[c] for c in r['executor']['mount'])
    cats = {arm: tcat839(tcls839(r[arm]['raw'], w)) for arm in ('self_answer', 'random_answer', 'whole_bank_answer')}
    atext = r['address']['raw'].upper()
    EV839.append({'ep': e['ep'], 'world': wi, 'cond': k['cond'], 'order': k['order'], 'id_version': k['id_version'],
                  'roles': roles, 'content': content, 'aclass': aclass839(roles), 'n_found': len(r['executor']['found']),
                  'n_valid': len(r['executor']['mount']), 'n_invalid': len(r['executor']['invalid']),
                  'n_malformed_id_like': len([t for t in re.findall(r'(?<![A-Za-z0-9])R[0-9]+(?![A-Za-z0-9])', r['address']['raw'])
                                              if len(t) != 6]),
                  'empty': not r['executor']['mount'], 'says_none': 'NONE' in atext,
                  'address_mentions_entity_names': any(nm in atext for nm in NAMES839),
                  'address_budget_exhausted': r['address']['budget_exhausted'],
                  'categories': cats, 'correct': {arm: cats[arm] in EXPECT839[k['cond']] for arm in cats},
                  'random_roles': [role839(c, wi) for c in r['random_mount']], 'address_raw': r['address']['raw'],
                  'answers_raw': {arm: r[arm]['raw'] for arm in cats}})
def sel839(cond, **kw):
    return [x for x in EV839 if x['cond'] == cond and all(x[a] == b for a, b in kw.items())]
FULL839 = sel839('FULL')
a1 = frac839([x['aclass'] == 'CHAIN' for x in FULL839]); a1_inv = sum(1 for x in FULL839 if x['n_invalid'])
A1 = ('INCONCLUSIVE' if a1[1] < 48 else 'PASS' if (a1[0] >= A1_NEED839 and a1_inv <= A1_INVALID_MAX839) else 'FAIL')
def pairs839(keyf, a, b):
    idx = {}
    for x in FULL839:
        idx.setdefault(keyf(x), {})[x['id_version'] if a == 'v' else x['order']] = x
    vals = (0, 1) if a == 'v' else ('FORWARD', 'REVERSE')
    return [(d[vals[0]], d[vals[1]]) for d in idx.values() if vals[0] in d and vals[1] in d]
p2 = pairs839(lambda x: (x['world'], x['order']), 'v', None)
a2 = frac839([u['content'] == v['content'] for u, v in p2])
a2_chain = frac839([u['content'] == v['content'] and u['aclass'] == 'CHAIN' for u, v in p2])
# ID-following diagnostic: v1 address reuses the literal v0 ID strings (which in v1 belong to other contents)
a2_idfollow = 0
for u, v in p2:
    ru = REC839[u['ep']]['executor']['found']; rv = REC839[v['ep']]['executor']['found']
    a2_idfollow += bool(ru) and ru == rv
A2 = ok839(a2[0], a2[1], A2_NEED839, 24)
p3 = pairs839(lambda x: (x['world'], x['id_version']), 'o', None)
a3 = frac839([u['content'] == v['content'] or (u['aclass'] == 'CHAIN' and v['aclass'] == 'CHAIN') for u, v in p3])
a3_strict = frac839([u['content'] == v['content'] for u, v in p3])
A3 = ok839(a3[0], a3[1], A3_NEED839, 24)
rs = sel839('REMOVE_SECOND'); rc = sel839('REMOVE_CONTINUATIONS'); rf = sel839('REMOVE_FIRST')
a4 = {'REMOVE_SECOND': frac839([set(x['roles']) == {'OWN_FIRST', 'OWN_CHANGED'} for x in rs]),
      'REMOVE_CONTINUATIONS': frac839([x['aclass'] in ('PARTIAL_OWN', 'EMPTY') and not x['n_invalid'] for x in rc]),
      'REMOVE_FIRST': frac839([x['aclass'] in ('PARTIAL_OWN', 'EMPTY') and not x['n_invalid'] for x in rf])}
A4 = ('INCONCLUSIVE' if min(v[1] for v in a4.values()) < 24 else
      'PASS' if all(v[0] >= A4_NEED839 for v in a4.values()) else 'FAIL')
b = {arm: frac839([x['correct'][arm] for x in EV839]) for arm in ('self_answer', 'random_answer', 'whole_bank_answer')}
B1 = ok839(b['self_answer'][0], b['self_answer'][1], B1_NEED839, 120)
B2 = ('INCONCLUSIVE' if b['self_answer'][1] < 120 else
      'PASS' if (b['self_answer'][0] >= b['whole_bank_answer'][0] + B2_GAP839 and
                 b['self_answer'][0] >= b['random_answer'][0] + B2_GAP839) else 'FAIL')
bycond = {c: {arm: frac839([x['correct'][arm] for x in sel839(c)]) for arm in ('self_answer', 'random_answer', 'whole_bank_answer')}
          for c in CONDS839}
byclass = {}
for x in EV839:
    byclass.setdefault(x['aclass'], []).append(x['correct']['self_answer'])
byclass = {k: frac839(v) for k, v in byclass.items()}
roletab = {}
for x in EV839:
    for rr_ in x['roles']:
        roletab.setdefault(x['cond'], {}); roletab[x['cond']][rr_] = roletab[x['cond']].get(rr_, 0) + 1
classtab = {c: {} for c in CONDS839}
for x in EV839:
    classtab[x['cond']][x['aclass']] = classtab[x['cond']].get(x['aclass'], 0) + 1
anstab = {c: {} for c in CONDS839}
for x in EV839:
    kk = x['categories']['self_answer']; anstab[x['cond']][kk] = anstab[x['cond']].get(kk, 0) + 1
noaddr = {'empty_address_episodes': frac839([x['empty'] for x in EV839]),
          'says_none': frac839([x['says_none'] for x in EV839]),
          'any_invalid_address': frac839([x['n_invalid'] > 0 for x in EV839]),
          'invalid_strings_total': sum(x['n_invalid'] for x in EV839),
          'malformed_id_like_strings_total (never applied)': sum(x['n_malformed_id_like'] for x in EV839),
          'address_mentions_entity_names': frac839([x['address_mentions_entity_names'] for x in EV839]),
          'address_token_budget_exhausted': frac839([x['address_budget_exhausted'] for x in EV839]),
          'empty_by_condition': {c: frac839([x['empty'] for x in sel839(c)]) for c in CONDS839},
          'mean_valid_ids': (float(np.mean([x['n_valid'] for x in EV839])) if EV839 else None)}
if BUDGET_STOP839 or D829['determinism839'].get('address_text_identical') is False:
    decision839 = 'YETERSİZ KANIT'
elif all(v == 'PASS' for v in (A1, A2, A3, A4, B1, B2)):
    decision839 = 'DEVAM'
elif A1 == 'FAIL':
    decision839 = 'DUR'
else:
    decision839 = 'YETERSİZ KANIT'
LEVEL_A = 'PASS' if all(v == 'PASS' for v in (A1, A2, A3, A4)) else ('INCONCLUSIVE' if 'INCONCLUSIVE' in (A1, A2, A3, A4) else 'FAIL')
LEVEL_B = 'PASS' if (B1 == 'PASS' and B2 == 'PASS') else ('INCONCLUSIVE' if 'INCONCLUSIVE' in (B1, B2) else 'FAIL')
EXTCTRL839 = not all(c['pass'] for c in D829['checks'] if c['name'].startswith(('STATIC_', 'LOCKED_', 'APPLIED_EXACTLY_', 'EXECUTOR_')))
CRIT839 = {'A1_FULL_ADDRESS': A1, 'A2_CONTENT_FOLLOWING': A2, 'A3_ORDER_INVARIANCE': A3, 'A4_REMOVAL': A4,
           'B1_SELF_ANSWER': B1, 'B2_CAUSAL': B2, 'C_WITHOUT_BANK': 'NOT_TESTED'}
LEVELS839 = {'A_in_context_native_id_selection': LEVEL_A, 'B_applied_address_drives_next_computation': LEVEL_B,
             'C_addressing_without_mounting_the_bank': 'NOT_TESTED (not solved; no large-scale claim)',
             'external_cognitive_control_detected': EXTCTRL839,
             'MODEL_NATIVE_AUTONOMY': ('FAIL' if EXTCTRL839 else
                                       'NOT_DEMONSTRATED (single fixed address phase, no loop / stop, level C not tested)')}
REPORT839 = {
    'A_address': {'full_chain': a1, 'full_any_invalid': a1_inv, 'class_table': classtab, 'role_table': roletab,
                  'id_swap_same_content': a2, 'id_swap_same_content_and_chain': a2_chain,
                  'id_swap_literal_v0_strings_repeated_in_v1': [a2_idfollow, len(p2)],
                  'order_invariant': a3, 'order_same_content_strict': a3_strict, 'removal': a4, 'no_address': noaddr},
    'B_next_computation': {'correct_all': b, 'correct_by_condition': bycond, 'self_answer_by_address_class': byclass,
                           'self_answer_categories': anstab},
    'levels': LEVELS839, 'classes': HYP839['classes'], 'resume': D829['resume839'], 'determinism': D829['determinism839']}
D829['cells839'] = EV839
D829['report839'] = REPORT839
D829['verdict839'] = {'decision': decision839, 'criteria': CRIT839, 'levels': LEVELS839, 'budget_stop': BUDGET_STOP839,
                      'interpretation_guard': ('The whole bank is mounted while the address is written (level A). Level '
                                               'C is not tested; no million-cartridge addressing is claimed. No loop, '
                                               're-search or stop decision is tested.')}
D829['claims_ledger839'] = dict(CLAIMS839, demonstrated_by_TEST839={'decision': decision839, 'criteria': CRIT839, 'levels': LEVELS839})
D829['cost839'] = {'counted': dict(COUNT834), 'predicted_upper': POST839, 'run_seconds': D829['run_seconds839'],
                   'total_seconds_body': round(time.perf_counter() - T0_839, 3),
                   'peak_gpu_gib': float(_torch829.cuda.max_memory_allocated()) / 2**30}
with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f839:
    wr839 = csv.DictWriter(f839, fieldnames=['episode', 'world', 'condition', 'order', 'id_version', 'address_raw', 'address_roles',
                                             'address_class', 'invalid', 'self_answer', 'self_category', 'random_answer',
                                             'random_category', 'whole_bank_answer', 'whole_bank_category'])
    wr839.writeheader()
    for x in EV839:
        wr839.writerow({'episode': x['ep'], 'world': x['world'], 'condition': x['cond'], 'order': x['order'],
                        'id_version': x['id_version'], 'address_raw': x['address_raw'], 'address_roles': ' '.join(x['roles']),
                        'address_class': x['aclass'], 'invalid': x['n_invalid'],
                        'self_answer': x['answers_raw']['self_answer'], 'self_category': x['categories']['self_answer'],
                        'random_answer': x['answers_raw']['random_answer'], 'random_category': x['categories']['random_answer'],
                        'whole_bank_answer': x['answers_raw']['whole_bank_answer'],
                        'whole_bank_category': x['categories']['whole_bank_answer']})
D829['status'] = 'COMPLETE_TEST839_EVALUATED' if not BUDGET_STOP839 else 'STOPPED_BUDGET_PARTIAL_EVALUATED'
save829()
log829('TEST839_REPORT', json.dumps(REPORT839, default=str))
log829('TEST839_VERDICT', json.dumps(D829['verdict839'], default=str))
log829('TEST839_COMPLETED', str(OUT829))
'''
BODY_SHA839 = hashlib.sha256(BODY839.encode()).hexdigest()
PANEL_HOOK839 = ("PANEL829['test839'] = {'episodes': [{'ep': e['ep'], 'qid': e['qid'], 'bank': e['bank'], 'directory': e['directory']} "
                 "for e in EPIS839], 'address_frame': ADDRESS_FRAME839, 'id_pattern': ID_PATTERN839, "
                 "'thresholds': {'A1': [A1_NEED839, A1_INVALID_MAX839], 'A2': A2_NEED839, 'A3': A3_NEED839, 'A4': A4_NEED839, "
                 "'B1': B1_NEED839, 'B2': B2_GAP839}, 'max_new': [MAX_NEW_ADDR839, MAX_NEW_ANS839], "
                 "'hypotheses': %r, 'body_sha256': %r, 'helpers_sha256': %r, 'seed': SEED829}\n"
                 % (HYP839, BODY_SHA839, HELPER_SHA839))
src839 = patch839(src839, "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))",
                  PANEL_HOOK839 + "PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))")
OFFLINE_HOOK839 = r'''
OFFLINE839 = DIR829 / 'TEST839_offline_key.json'   # never read by any runtime computation
OFFLINE839.write_text(json.dumps({'note': 'OFFLINE ONLY', 'episodes': EVALKEY839,
                                  'cartridge_contents': {c: list(v) for c, v in CONTENT839.items()},
                                  'worlds': worlds829, 'questions': questions829, 'card_meta': card_meta829},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D829['offline_key839_sha256'] = sha829(OFFLINE839.read_bytes())
'''
src839 = patch839(src839, "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n",
                  "D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())\n" + OFFLINE_HOOK839)
start839 = src839.index("    # RUN ORDER: integrity checks")
start839 = src839.rfind("    # ---", 0, start839)
end839 = src839.index("except BaseException as e:\n    D829['status'] = 'ERROR'", start839)
BODY839_TEXT = BODY839
replacement839 = "\n".join("    " + line if line else "" for line in BODY839.strip("\n").splitlines()) + "\n"
patched839 = src839[:start839] + replacement839 + src839[end839:]
ast.parse(patched839)
# ==================================================================================================================
# CONSOLE / LOGGING LAYER (TEST835 pattern). Nothing below changes what is computed. Every byte the engine prints is
# written unchanged to a full transcript file; the screen shows a compact digest, progress, failures and the summary.
# ==================================================================================================================
import os as _os839, sys as _sys839, io as _io839, traceback as _tb839, datetime as _dt839, shutil as _sh839
from pathlib import Path as _P839
_os839.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')     # download bars only (not data)
for _m839, _f839 in (('huggingface_hub', lambda m: m.utils.disable_progress_bars()),
                     ('transformers', lambda m: m.utils.logging.disable_progress_bar())):
    if _m839 in _sys839.modules:                                    # only if already imported: no new import
        try:
            _f839(_sys839.modules[_m839])
        except Exception:
            pass
_ROOT839 = _P839('/content') if _P839('/content').exists() else _P839('/tmp')
FULL_CONSOLE839 = _ROOT839 / ('TEST839_full_console_' + _dt839.datetime.now(_dt839.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.txt')
CON839 = {'phase': 'SOURCE_VERIFICATION', 'last': [], 'fail_lines': [], 't0': time.time(), 'measure': '0/0', 'p3': 0}
_ORIG_OUT839, _ORIG_ERR839 = _sys839.stdout, _sys839.stderr

def say839(*a):
    _ORIG_OUT839.write(' '.join(str(x) for x in a) + '\n'); _ORIG_OUT839.flush()

def _mins839():
    return round((time.time() - CON839['t0']) / 60.0, 1)

def route839(line):
    s = line.strip()
    if not s:
        return
    CON839['last'] = (CON839['last'] + [s[:300]])[-6:]
    if s.startswith('FAIL '):
        CON839['fail_lines'].append(s[:600]); say839('!! ' + s[:600]); return
    if s.startswith('TEST829_FAILED'):
        CON839['fail_lines'].append(s[:300]); return
    if s.startswith('TEST829_START'):
        parts = s.split()
        say839('Çalışma: %s | panel SHA-256: %s' % (parts[1] if len(parts) > 1 else '?', parts[-1]))
        CON839['phase'] = 'ENGINE_PRELUDE_AND_LOCKS'; return
    if s.startswith('TEST815_GPU_PREFLIGHT'):
        say839('GPU: ' + s[len('TEST815_GPU_PREFLIGHT'):].strip()); return
    if s.startswith('TEST815_GPU_FREE_GIB'):
        say839('GPU boş VRAM (yükleme öncesi): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('TEST839_PREDICTED_COST_BEFORE_MODEL_LOAD'):
        try:
            c = json.loads(s.split(' ', 1)[1]); u = c['numeric_upper']
            say839('Maliyet üst sınırı (model yükleme hariç, %%25 pay dahil): %s dk | bölüm %s, banka mount %s | kartuş %s | '
                   'fusion<=%s üretim<=%s' % (c['minutes_upper_excluding_model_load'], c['episodes'], c['bank_mounts'],
                   c['physical_cartridges'], u['fusion_forwards'], u['generation_forwards']))
        except Exception:
            say839(s[:300])
        CON839['phase'] = 'MODEL_LOAD'; say839('Model yükleniyor (Qwen2.5-72B-Instruct, NF4, tek yükleme)...'); return
    if s.startswith('PASS FROZEN_PREFIX'):
        D_ = globals().get('D829', {})
        say839('Model yüklendi (%s s). Fiziksel kartuşlar üretiliyor ve SHA doğrulanıyor...' % D_.get('model_load_seconds', '?'))
        CON839['phase'] = 'PHYSICAL_CARTRIDGE_FORGING'; return
    if s.startswith('PASS PHYSICAL_COUNT'):
        say839('Fiziksel kartuşlar: ' + s.split()[-1] + ' (her biri SHA-256 + tensör SHA ile yeniden yüklendi)')
        CON839['phase'] = 'PREFLIGHT_GATES'; return
    if s.startswith('PASS ARCH_DIMS'):
        say839('Mimari (NL,H,QH,KVH,HD): ' + s[len('PASS ARCH_DIMS'):].strip() + ' | BF16 hesap, NF4, ağırlıklar donmuş'); return
    if s.startswith('PASS VRAM_HEADROOM'):
        say839('Boş VRAM (model sonrası): ' + s.split()[-1] + ' GiB'); return
    if s.startswith('PASS STATIC_NO_LABELS_BEFORE_OFFLINE'):
        say839('Sızıntı kapısı: çevrimdışı işaretinden önce hiçbir etiket nesnesi kullanılmıyor (AST)'); return
    if s.startswith('PASS LOCKED_FREE_GENERATE_BYTECODE'):
        say839('Kaynak doğrulama: free_generate bytecode = kilitli 779 derlemesi (aynı boru hattı); greedy argmax, örnekleme yok'); return
    if s.startswith('PASS LOCKED_ATTENTION_INTERVENTION_BYTECODE'):
        say839('Kaynak doğrulama: AttentionIntervention bytecode = kilitli 779 (bias=0: maske değişmez)'); return
    if s.startswith('TEST839_CUT3_BYTECODE_INFO'):
        say839('Bilgi: Cut3Diagnostic kilitli 779 bytecode eşitliği ' + s.split(' ', 1)[1][:160] + ' (seed=None: enjeksiyon dalı çalışmaz)'); return
    if s.startswith('TEST839_SOURCE_VERIFIED_BEFORE_MODEL_LOAD'):
        say839('Kaynak doğrulama tamam (model yüklenmeden önce)'); return
    if s.startswith('TEST839_DETERMINISM'):
        try:
            r = json.loads(s.split(' ', 1)[1]); say839('Determinizm (adres metni yeniden üretimi): %s' % r.get('address_text_identical'))
        except Exception:
            say839(s[:200])
        return
    if s.startswith('PASS STATIC_EXECUTOR_LITERAL_LOOKUP_ONLY'):
        say839('Kaynak doğrulama: yürütücü yalnızca birebir Record-ID eşlemesi (benzerlik/sıralama/düzeltme yok)'); return
    if s.startswith('PASS STATIC_GENERATION_CALLS_UNMODIFIED'):
        say839('Kaynak doğrulama: tüm üretim çağrıları seed=None, gain=0, spans=None; cevap çerçevesine adres metni girmiyor'); return
    if s.startswith('TEST839_RESUME '):
        try:
            r = json.loads(s.split(' ', 1)[1])
            say839('Devam mekanizması: yeniden kullanılan bölüm %s | %s' % (r.get('reused_episodes'), r.get('reason')))
            CON839['phase'] = 'RUNTIME'
        except Exception:
            say839(s[:300])
        return
    if s.startswith('TEST839_PROGRESS'):
        p = s.split()
        if len(p) >= 5:
            CON839['phase'] = 'MEASUREMENT %s (%s/%s)' % (p[1], p[2], p[4])
            if p[2] != '0':
                say839('  %-11s %s/%s (%s dk)' % (p[1], p[2], p[4], _mins839()))
        return
    if s.startswith('TEST839_BUDGET_STOP'):
        say839('!! ' + s); return
    if s.startswith('TEST839_OFFLINE_START'):
        CON839['phase'] = 'OFFLINE_EVALUATION'
        say839('Ölçüm bitti; çevrimdışı değerlendirme (%s dk)' % _mins839()); return
    if s.startswith('TEST839_COMPLETED'):
        CON839['phase'] = 'COMPLETED'; return

class Console839(_io839.TextIOBase):
    """Writes everything to FULL_CONSOLE839 unchanged; routes complete lines to the compact screen digest."""
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
                route839(line.split('\r')[-1])
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

def sha_path839(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()

def fmt839(x):
    if isinstance(x, list) and len(x) == 2 and all(isinstance(v, (int, float)) for v in x):
        return '%s/%s' % (x[0], x[1])
    if isinstance(x, dict):
        return ', '.join('%s=%s' % (k, fmt839(v)) for k, v in x.items())
    if isinstance(x, float):
        return '%.4g' % x
    if isinstance(x, list):
        return '[' + ', '.join(fmt839(v) for v in x) + ']'
    return str(x)

def files_report839():
    say839('=' * 78); say839('SONUÇ DOSYALARI (SHA-256)')
    d = globals().get('DIR829')
    if d is None or not _P839(d).exists():
        say839('  (çalışma klasörü yok)'); return
    for p in sorted(_P839(d).iterdir()):
        if p.is_file():
            say839('  %s  %d B  %s' % (p, p.stat().st_size, sha_path839(p)))
    vd = _P839(d) / 'TEST839_episodes'
    if vd.exists():
        fs = sorted(x for x in vd.iterdir() if x.is_file())
        say839('  %s/  %d bölüm kaydı, %.1f MB (her dosyanın SHA-256 değeri TEST839_episode_manifest.jsonl içinde)'
               % (vd, len(fs), sum(x.stat().st_size for x in fs) / 2**20))

def final839(D):
    R = D['report839']; V = D['verdict839']; K = V['criteria']; C = D['cost839']; L = V['levels']
    checks = D.get('checks', [])
    A = R['A_address']; B = R['B_next_computation']; N = A['no_address']
    say839('=' * 78); say839('TEST839 SONUÇ ÖZETİ (adres = modelin greedy çıktısı; yürütücü = birebir Record-ID eşlemesi)'); say839('=' * 78)
    say839('Durum: %s | bütçe durdurması: %s | devam: yeniden kullanılan bölüm %s | determinizm: %s'
           % (D.get('status'), V['budget_stop'], R['resume'].get('reused_episodes'), fmt839(R.get('determinism', {}))))
    say839('Bütünlük: %d kapı, %d başarısız | kaynak doğrulama: free_generate/AttentionIntervention bytecode = kilitli 779, '
           'greedy argmax, seed=None/gain=0/bias=0, yürütücü AST beyaz liste, çevrimdışı öncesi etiket yok'
           % (len(checks), sum(not c['pass'] for c in checks)))
    say839('-' * 78); say839('[A] BANKA BAĞLAMDAYKEN MODEL-NATIVE ID SEÇİMİ (18 kartuş takılı; tam banka modele görünür)')
    say839('  FULL: kendi zinciri (ilk + geçerli devam, fazlası yok) %s | geçersiz adres içeren bölüm %s/48'
           % (fmt839(A['full_chain']), A['full_any_invalid']))
    for c, t in A['class_table'].items():
        say839('  %-21s adres sınıfları: %s' % (c, ', '.join('%s=%s' % kv for kv in sorted(t.items()))))
    for c, t in A['role_table'].items():
        say839('  %-21s seçilen roller : %s' % (c, ', '.join('%s=%s' % kv for kv in sorted(t.items()))))
    say839('  ID değişimi (v0 -> v1, aynı içerik): aynı içerik %s | aynı içerik ve zincir %s | v0 ID dizgileri v1\'de aynen tekrar %s'
           % (fmt839(A['id_swap_same_content']), fmt839(A['id_swap_same_content_and_chain']),
              fmt839(A['id_swap_literal_v0_strings_repeated_in_v1'])))
    say839('  Sıra değişimi (FORWARD/REVERSE): aynı içerik ya da ikisi de temiz zincir %s | birebir aynı içerik %s'
           % (fmt839(A['order_invariant']), fmt839(A['order_same_content_strict'])))
    say839('  Çıkarma kontrolleri: ' + fmt839(A['removal']))
    say839('  Adres üretilemeyen bölüm %s (NONE yazan %s) | geçersiz adres içeren %s (toplam %s dizgi) | adres metninde varlık adı %s | '
           'token bütçesi doldu %s | ort. geçerli ID %s | biçimi bozuk ID benzeri dizgi %s (uygulanmadı)' % (
           fmt839(N['empty_address_episodes']), fmt839(N['says_none']),
           fmt839(N['any_invalid_address']), N['invalid_strings_total'], fmt839(N['address_mentions_entity_names']),
           fmt839(N['address_token_budget_exhausted']), fmt839(N['mean_valid_ids']),
           N['malformed_id_like_strings_total (never applied)']))
    say839('  Koşullara göre boş adres: ' + fmt839(N['empty_by_condition']))
    say839('[B] UYGULANAN ADRES SONRAKİ HESAPLAMAYI BELİRLİYOR MU (cevap yalnız modelin adreslediği mount üzerinde)')
    say839('  Doğru cevap (120): kendi adresi %s | eşit boyutlu rastgele seçim %s | tüm banka %s'
           % (fmt839(B['correct_all']['self_answer']), fmt839(B['correct_all']['random_answer']),
              fmt839(B['correct_all']['whole_bank_answer'])))
    for c, t in B['correct_by_condition'].items():
        say839('  %-21s kendi %s | rastgele %s | tüm banka %s | kendi cevap kategorileri %s'
               % (c, fmt839(t['self_answer']), fmt839(t['random_answer']), fmt839(t['whole_bank_answer']),
                  ', '.join('%s=%s' % kv for kv in sorted(B['self_answer_categories'].get(c, {}).items()))))
    say839('  Adres sınıfına göre kendi cevabı doğru: ' + fmt839(B['self_answer_by_address_class']))
    say839('[C] BANKA TAKILMADAN ADRES BULMA: TEST EDİLMEDİ — çözülmedi; milyon kartuşluk adresleme iddiası yok')
    say839('-' * 78); say839('ÖLÇÜTLER')
    for k in K:
        say839('  %-24s %s' % (k, K[k]))
    say839('DÜZEYLER:')
    for k, v in L.items():
        say839('  %-46s %s' % (k, v))
    say839('=' * 78)
    say839('NİHAİ BİLİMSEL KARAR: %s' % V['decision'])
    if V['decision'] == 'DEVAM':
        say839('  Gerekçe: A1-A4 ve B1-B2 PASS — banka bağlamdayken model içerik bağımlı adres üretti ve uygulanan adres '
               'sonraki hesaplamayı belirledi. C test edilmedi; döngü/durma test edilmedi; otonomi iddiası yok.')
    elif V['decision'] == 'DUR':
        say839('  Gerekçe: A1 FAIL — banka bağlamdayken bile model önceden sabit ölçütte doğru adresi üretemedi.')
    else:
        say839('  Gerekçe: ' + ('bütçe durdurması' if V['budget_stop'] else
                               'ölçütler ne DEVAM ne DUR kuralını sağladı (bkz. A1-A4 / B1-B2 satırları)'))
    say839('Maliyet: sayılan %s | çalışma %s s | toplam gövde %s s | tepe VRAM %.2f GiB'
           % (fmt839(C['counted']), C['run_seconds'], C['total_seconds_body'], C['peak_gpu_gib']))

say839('=' * 78)
say839('AKBASCORE TEST839 — modelin ürettiği fiziksel adres tokenlerinin mekanik uygulanması; Qwen2.5-72B-Instruct (NF4, donmuş), tek A100-80GB')
say839('Kaynak kilitleri: 829.py %s | 834.py %s | 779.py %s | 838.py %s | 838.log %s'
       % (LOCK829_839, LOCK834_839, LOCK779_839, LOCK838_839, LOCK838LOG_839))
say839('Kilitli yardımcılar (AST, %d fonksiyon) SHA-256 %s' % (len(HELPERS839), HELPER_SHA839))
say839('BODY839 SHA-256 %s | yamalı kaynak AST geçti (%d bayt, SHA-256 %s)' % (BODY_SHA839, len(patched839), hashlib.sha256(patched839.encode()).hexdigest()))
say839('Kapsam: %d görülmemiş dünya, 18 kartuşluk 4 banka, %d bölüm (FULL x 2 ID sürümü x 2 sıra + 3 çıkarma koşulu x 2 sıra) | '
       'düzey C (banka takılmadan adresleme) TEST EDİLMİYOR' % (WORLDS839, WORLDS839 * (2 * 2 + 3 * 2)))
say839('Tam konsol kaydı: ' + str(FULL_CONSOLE839))
say839('=' * 78)
_fh839 = open(FULL_CONSOLE839, 'a', encoding='utf-8', buffering=1)
_fh839.write('TEST839_SOURCE_LOCKS ' + ' '.join((LOCK829_839, LOCK834_839, LOCK779_839, LOCK838_839, LOCK838LOG_839)) +
             '\nTEST839_BODY_SHA256 ' + BODY_SHA839 + '\nTEST839_HELPERS ' + HELPER_SHA839 +
             '\nTEST839_PATCHED_SOURCE_AST_PASS ' + str(len(patched839)) + ' ' + hashlib.sha256(patched839.encode()).hexdigest() + '\n')
import linecache as _lc839
for _nm839, _src839 in (('TEST839_LOCKED_ENGINE', patched839), ('TEST839_LOCKED_HELPERS', HELPER_SRC839)):
    _lc839.cache[_nm839] = (len(_src839), None, [x + '\n' for x in _src839.splitlines()], _nm839)
_sys839.stdout = Console839(_ORIG_OUT839, _fh839); _sys839.stderr = Console839(_ORIG_ERR839, _fh839)
TEST839_ERROR = None
try:
    exec(compile(patched839, 'TEST839_LOCKED_ENGINE', 'exec'), globals())
except BaseException as _e839:
    TEST839_ERROR = _e839
    _tbtext839 = _tb839.format_exc()
    _fh839.write('\n[TEST839 OUTER EXCEPTION]\n' + _tbtext839)
finally:
    _sys839.stdout, _sys839.stderr = _ORIG_OUT839, _ORIG_ERR839
    try:
        _fh839.flush(); _fh839.close()
    except Exception:
        pass
    _dir839 = globals().get('DIR829')
    if _dir839 is not None and _P839(_dir839).exists() and FULL_CONSOLE839.exists():
        _dst839 = _P839(_dir839) / FULL_CONSOLE839.name
        _sh839.move(str(FULL_CONSOLE839), str(_dst839)); FULL_CONSOLE839 = _dst839
if TEST839_ERROR is not None:
    D_ = globals().get('D829', {}) if isinstance(globals().get('D829'), dict) else {}
    bad = [c for c in D_.get('checks', []) if not c.get('pass')]
    say839('=' * 78); say839('TEST839 HATA')
    say839('Tür: %s.%s' % (type(TEST839_ERROR).__module__, type(TEST839_ERROR).__name__))
    say839('Mesaj: ' + repr(TEST839_ERROR)[:800])
    say839('Aşama: ' + CON839['phase'] + ' | geçen %s dk' % _mins839())
    if bad:
        say839('Başarısız kapı: %s | ayrıntı: %s' % (bad[-1].get('name'), str(bad[-1].get('detail'))[:400]))
    say839('Hata öncesi son motor satırları:')
    for x in CON839['last'][-4:]:
        say839('  ' + x[:240])
    tbl = _tbtext839.rstrip().splitlines()
    say839('Traceback (son %d satır; tamamı dosyada ve results.json içinde):' % min(40, len(tbl)))
    for x in tbl[-40:]:
        say839('  ' + x)
    files_report839()
    say839('Tam konsol kaydı: %s  SHA-256 %s' % (FULL_CONSOLE839, sha_path839(FULL_CONSOLE839) if FULL_CONSOLE839.exists() else '-'))
    say839('Not: tamamlanan ölçümler vektör dosyalarında; hücre yeniden çalıştırılırsa SHA doğrulanıp yeniden kullanılır.')
    raise SystemExit('TEST839_FAILED: ' + type(TEST839_ERROR).__name__)
try:
    final839(D829)
except Exception as _e839s:
    say839('!! Özet basılamadı (veri dosyalarda tam): ' + repr(_e839s))
    say839(_tb839.format_exc()[-1500:])
files_report839()
say839('=' * 78)
