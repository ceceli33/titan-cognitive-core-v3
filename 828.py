# AKBASCORE SILICON HIPPOCAMPUS — TEST828
# COUNTERFACTUAL OBSERVABILITY OF ONE-HOP TRUNCATION (SHADOW MODE, DIAGNOSTIC ONLY).
# Built on the GPU-completed TEST827 skeleton (827.py, git blob 567822d3...) and the locked TEST815 engine.
# Single Colab cell; frozen Qwen2.5-72B NF4; exactly one A100 80GB.
# LOCKED TEST815 engine; no residual hooks, no source replay at read time, no training, no textual control.
# TEST828 question: can the frozen model's existing full-depth numerical response to physical memory-set
# interventions distinguish sufficient two-hop evidence from incomplete one-hop evidence, without any
# language-mediated control and without access to the answer key?
# The TEST827 RETAINED_SIGNED controller and its stopping rule are executed UNCHANGED; the stopping
# condition is compiled from the exact locked TEST827 source. Every new measurement is shadow-only:
# no TEST828 measurement chooses, rejects, fuses, or stops anything.
# Question encoding and final answer readout remain boundary interfaces; the control loop is numeric.
# No GPU execution or result is claimed by the code author.
import ast, hashlib, urllib.request, json, csv, gc, time, traceback, random, re, datetime, contextlib, io, math, types
from pathlib import Path

T828 = '828'
REPO828 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCK815_828 = '77774f87428c0243c9a86ea6a041364acd9c1b03'
LOCK827_828 = '567822d34781ce966e0d5030a101d950d66156e8'   # GPU-completed TEST827 skeleton
SEED828 = 8282026                # fresh sealed panel (TEST827 used 8272026)
WORLDS828 = 3                    # pilot; six worlds only if the offline pilot verdict justifies it
PARAPHRASES828 = 1
MAX_STEPS828 = 4                 # safety ceiling, NOT evidence of autonomous stopping (unchanged)
MAX_NEW_ANSWER828 = 96
MAX_NEW_CONTROL828 = 0           # no control text generated
MAX_CANDIDATES828 = 5
MAX_NEW_OFFLINE828 = 48          # designed-panel greedy continuation: OFFLINE evaluation only
TOPK_STORE828 = 8                # small offline-inspection summary; distances use the FULL vocabulary
LM_CHUNK828 = 8192               # lm_head rows per float64 chunk (8192 x 8192 x 8 B = 512 MiB transient)
RUN828 = 'TEST828_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
DIR828 = (Path('/content') if Path('/content').exists() else Path('/tmp')) / RUN828
DIR828.mkdir(parents=True, exist_ok=False)
OUT828 = DIR828 / 'TEST828_results.json'
LOG828 = DIR828 / 'TEST828.log'
REVIEW828 = DIR828 / 'TEST828_blind_review.csv'
OFFLINE828 = DIR828 / 'TEST828_offline_key.json'  # never available to inference/controller/shadow

D828 = {'test': T828, 'status': 'STARTED', 'run': RUN828,
        'source815_blob': LOCK815_828, 'source827_blob': LOCK827_828,
        'controller': 'TEST827_RETAINED_SIGNED_UNCHANGED_PLUS_COUNTERFACTUAL_SHADOW',
        'checks': [], 'trials': [], 'designed': [],
        'limitations': [
            'TEST828 is a diagnostic observability experiment, NOT a claim of autonomous stopping.',
            'The TEST827 controller and stopping rule are executed unchanged; the stopping condition is compiled from the locked TEST827 source.',
            'All counterfactual measurements run in shadow mode; none influences ranking, selection, fusion or stopping.',
            'The full-depth readout is the NEXT-TOKEN distribution at the final question position; it is NOT the multi-token answer.',
            'Question encoding (question text only, no instruction) and the final answer readout are boundary interfaces; no generated text enters any runtime decision.',
            'Designed-panel roles (first/second/decoy) exist only in the offline key; runtime uses opaque intervention and cartridge identifiers.',
            'Order-perturbation divergence B(S) is recorded as a diagnostic only and is never used as a threshold.',
            'Low divergence does not prove correctness; a stable distribution does not prove chain completeness; a nonzero leave-one-out effect does not prove logical necessity.',
            'The NULL control cartridge is a physical memory baseline, not an empty memory.',
            'Synthetic two-hop relations test a narrow capability, not general scientific reasoning.',
            'Three-world pilot: any separation is descriptive, not statistically established.',
            'No GPU execution or result is claimed by the code author.']}

def sha828(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()

def blob828(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def save828():
    p = Path(str(OUT828) + '.tmp')
    p.write_text(json.dumps(D828, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    p.replace(OUT828)

QUIET828 = ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_',
            'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_',
            'NUM_', 'MEAS_', 'ENGINE_BINDINGS_', 'UNIQUE_ACTIVE_', 'DRA_SHADOW_FINITE_', 'FINITE_FEEDBACK_', 'FINITE_RANK_')

def log828(*args):
    msg = ' '.join(map(str, args))
    if not (msg.startswith('PASS ') and any(k in msg for k in QUIET828)):
        print(msg, flush=True)
        with LOG828.open('a', encoding='utf-8') as f:
            f.write(msg + '\n')

def gate828(name, ok, detail=None):
    D828['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail})
    if not (ok and any(k in name for k in QUIET828)):
        save828()
    log828('PASS' if ok else 'FAIL', name, detail if detail is not None else '')
    if not ok:
        save828()
        raise RuntimeError('TEST828_GATE_' + name)

# PRESEALED panel: opaque names and randomized assignments. All scoring stays offline.
# Same generator and card templates as TEST827; only the seed (fresh panel) and prefixes differ.
RNG828 = random.Random(SEED828)
ALPH828 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

def code828():
    return ''.join(RNG828.choice(ALPH828) for _ in range(9))

worlds828 = []
seen828 = set()
for wi in range(WORLDS828):
    names = []
    while len(names) < 5:
        n = code828()
        if n not in seen828:
            seen828.add(n); names.append(n)
    worlds828.append({'world': 'DOMAIN_' + code828(), 'start': names[0],
                      'middle': names[1], 'end': names[2],
                      'changed_end': names[3], 'decoy_end': names[4]})

questions828 = []
for w in worlds828:
    for pi, fmt in enumerate((
        'In domain {world}, starting from {start}, which endpoint is reached after exactly two directed links?',
        'For {world}, follow two successive directed edges beginning at {start}. Give the final node.')[:PARAPHRASES828]):
        questions828.append({'qid': w['world'] + '_P' + str(pi), 'world': w['world'],
                             'question': fmt.format(**w), 'expected': w['end'],
                             'changed_expected': w['changed_end']})

cards828, card_meta828 = {}, {}
for w in worlds828:
    domain = w['world']
    ids = {kind: 'E828_' + code828() for kind in ('first', 'second', 'changed', 'decoy')}
    w['ids'] = ids
    cards828[ids['first']] = ('Evidence record. Domain: ' + domain + '\n' +
                              'Directed relation: ' + w['start'] + ' -> ' + w['middle'] + '.\n')
    cards828[ids['second']] = ('Evidence record. Domain: ' + domain + '\n' +
                               'Directed relation: ' + w['middle'] + ' -> ' + w['end'] + '.\n')
    cards828[ids['changed']] = ('Evidence record. Domain: ' + domain + '\n' +
                                'Directed relation: ' + w['middle'] + ' -> ' + w['changed_end'] + '.\n')
    cards828[ids['decoy']] = ('Evidence record. Domain: ' + domain + '\n' +
                              'Directed relation: ' + w['decoy_end'] + ' -> ' + w['start'] + '.\n')
    for kind, cid in ids.items():
        card_meta828[cid] = {'domain': domain, 'kind': kind, 'body_sha256': sha828(cards828[cid])}
NULL828 = 'E828_NULL'
cards828[NULL828] = 'CONTROL MEMORY. No directed relations are available.\n'
card_meta828[NULL828] = {'domain': None, 'kind': 'null', 'body_sha256': sha828(cards828[NULL828])}
# Public panel hashes carry no kind/domain labels (those live only in the offline key).
card_hashes_public828 = {cid: m['body_sha256'] for cid, m in card_meta828.items()}

# DESIGNED ONE-HOP TRUNCATION PANEL (experimenter intervention, sealed before model loading).
# Roles are written ONLY to the offline key. Runtime receives opaque intervention IDs and cartridge lists,
# executed in a seeded shuffled order so execution position carries no role information.
DESIGN_ROLES828 = ('NULL', 'FIRST', 'SECOND', 'DECOY', 'BOTH', 'BOTH_REV', 'FIRST_DECOY',
                   'FIRST_OTHER', 'BOTH_DECOY', 'BOTH_REPLAY')
design_public828, design_key828 = [], {}
_order828 = random.Random(SEED828 + 1)
for wi, w in enumerate(worlds828):
    i = w['ids']
    other_second = worlds828[(wi + 1) % WORLDS828]['ids']['second']
    role_ids = {'NULL': [NULL828], 'FIRST': [i['first']], 'SECOND': [i['second']], 'DECOY': [i['decoy']],
                'BOTH': [i['first'], i['second']], 'BOTH_REV': [i['second'], i['first']],
                'FIRST_DECOY': [i['first'], i['decoy']], 'FIRST_OTHER': [i['first'], other_second],
                'BOTH_DECOY': [i['first'], i['second'], i['decoy']], 'BOTH_REPLAY': [i['first'], i['second']]}
    qid = next(q['qid'] for q in questions828 if q['world'] == w['world'])
    rows = []
    for role in DESIGN_ROLES828:
        xid = 'X828_' + code828()
        design_key828[xid] = {'role': role, 'world': w['world']}
        rows.append({'xid': xid, 'qid': qid, 'ids': role_ids[role],
                     'offline_generation': role != 'BOTH_REPLAY'})
    _order828.shuffle(rows)
    design_public828 += rows

ARMS828 = ('FULL', 'REMOVE_SECOND', 'ADD_IRRELEVANT')
PANEL828 = {'seed': SEED828, 'world_count': WORLDS828, 'paraphrases': PARAPHRASES828,
            'questions': [{'qid': q['qid'], 'question': q['question']} for q in questions828],
            'arms': ARMS828, 'policies': ['RETAINED_SIGNED'],
            'limits': [MAX_STEPS828, MAX_NEW_ANSWER828, MAX_NEW_CONTROL828, MAX_CANDIDATES828,
                       MAX_NEW_OFFLINE828, TOPK_STORE828],
            'card_hashes': card_hashes_public828, 'designed_interventions': design_public828,
            'shadow_protocol': ['REPLAY', 'REVERSE', 'ROTATE', 'LEAVE_ONE_OUT', 'KEEP_TOP1_LOO',
                                'KEEP_TOP2_LOO', 'DROP_TOP2_LOO', 'NULL_REFERENCE'],
            'readout': 'FULL_VOCABULARY_NEXT_TOKEN_DISTRIBUTION_AT_FINAL_QUESTION_POSITION'}
PANEL_SHA828 = sha828(json.dumps(PANEL828, ensure_ascii=False, sort_keys=True))
D828['panel_sha256'] = PANEL_SHA828
D828['panel_public'] = PANEL828
OFFLINE828.write_text(json.dumps({'note': 'OFFLINE ONLY — NEVER IMPORT INTO CONTROLLER OR SHADOW',
                                  'questions': questions828, 'worlds': worlds828,
                                  'card_meta': card_meta828, 'designed_roles': design_key828},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D828['offline_key_sha256'] = sha828(OFFLINE828.read_bytes())
save828()

def fetch_locked828(name, lock, limit=120000):
    req = urllib.request.Request(REPO828 + name, headers={'User-Agent': 'AKBASCORE-TEST828'})
    with urllib.request.urlopen(req, timeout=180) as f:
        raw = f.read(limit + 1)
    gate828('LOCK_' + name, len(raw) <= limit and blob828(raw) == lock, blob828(raw))
    return raw

# The engine is imported from the EXACT locked TEST815 AST prelude, unchanged.
# The original TEST815 experiment is never executed.
try:
    log828('TEST828_START', RUN828, 'PANEL_SHA', PANEL_SHA828)
    T0_828 = time.perf_counter()
    raw815_828 = fetch_locked828('815.py', LOCK815_828)
    tree815_828 = ast.parse(raw815_828.decode('utf-8'), filename='815.py')
    idx828 = [i for i, n in enumerate(tree815_828.body) if isinstance(n, ast.Try)]
    gate828('AST_BOUNDARY', len(idx828) == 1 and idx828[0] == len(tree815_828.body) - 1, idx828)
    exec(compile(ast.fix_missing_locations(ast.Module(body=tree815_828.body[:idx828[0]], type_ignores=[])),
                 'LOCKED_TEST815_PRELUDE', 'exec'), globals())
    gate828('LOCKED_ENGINE_SYMBOLS', all(callable(globals().get(x)) for x in
            ('model_setup', 'physical_commit', 'safe_load', 'build_fusion', 'free_generate',
             'memory_seals', 'compare_seals', 'sentinel', 'release', 'numeric_rank', 'observe_state',
             'prompt_ids', 'normalized', 'sha_file')))
    gate828('FRESH_BANK', len(entries) == 0, len(entries))
    # ENGINE BINDING PREFLIGHT. The locked engine resolves these names through this cell's globals at
    # call time; a TEST828 global with the same name would silently replace them (TEST828 run 1 failed
    # because a cell-level dict `pairs` replaced 709.py pairs()). Capture the locked objects now and
    # require object identity before every physical fusion and at the end.
    ENGINE_NAMES828 = ('pairs', 'cache_build', 'replace', 'half', 'rope', 'rephase', 'sentinel', 'free_gpu',
                       'ensure_room', 'kv_digest', 'full_kv_seal', 'answer', 'DirectCut3', 'forge_native',
                       'initialize_native', 'to_gpu', 'seal_cp', 'memory_seals', 'compare_seals', 'safe_load',
                       'release', 'native_append_direct', 'load_verified', 'build_fusion', 'normalized',
                       'query_native', 'numeric_rank', 'read_exact', 'model_setup', 'record_cp', 'physical_commit',
                       'observe_state', 'free_generate', 'prompt_ids', 'cache_build', 'Cut3Diagnostic',
                       'AttentionIntervention', 'aggregate_attention', 'sha_file', 'check', 'log')
    ENGINE_LOCKED828 = {k: globals().get(k) for k in ENGINE_NAMES828}
    _pairs828 = ENGINE_LOCKED828['pairs']
    gate828('ENGINE_BINDING_PREFLIGHT_PAIRS',
            callable(_pairs828) and getattr(_pairs828, '__name__', None) == 'pairs' and
            getattr(getattr(_pairs828, '__code__', None), 'co_filename', None) == '709.py',
            {'type': type(_pairs828).__name__, 'name': getattr(_pairs828, '__name__', None),
             'file': getattr(getattr(_pairs828, '__code__', None), 'co_filename', None)})
    gate828('ENGINE_BINDING_PREFLIGHT_ALL_CALLABLE',
            all(callable(v) for v in ENGINE_LOCKED828.values()),
            sorted(k for k, v in ENGINE_LOCKED828.items() if not callable(v)))
    D828['engine_bindings'] = {k: {'type': type(v).__name__,
                                   'file': getattr(getattr(v, '__code__', None), 'co_filename', None)}
                               for k, v in ENGINE_LOCKED828.items()}

    def engine_bindings828(tag):
        bad = sorted(k for k, v in ENGINE_LOCKED828.items() if globals().get(k) is not v)
        gate828('ENGINE_BINDINGS_' + tag, not bad, bad or None)

    import torch as _torch828
    SDPA828 = _torch828.nn.functional.scaled_dot_product_attention

    # ------------------------------------------------------------------------------------------
    # 1. STOPPING-RULE VERIFICATION AGAINST THE EXACT EXECUTABLE TEST827 CODE.
    # The condition is extracted from locked 827.py (run_trial827) and compiled VERBATIM into a
    # predicate. TEST828 calls this predicate at exactly the same place in the loop as TEST827.
    # ------------------------------------------------------------------------------------------
    raw827_828 = fetch_locked828('827.py', LOCK827_828)
    src827_828 = raw827_828.decode('utf-8')
    tree827_828 = ast.parse(src827_828, filename='827.py')
    fn827 = [n for n in ast.walk(tree827_828) if isinstance(n, ast.FunctionDef) and n.name == 'run_trial827']
    gate828('STOP827_FUNCTION', len(fn827) == 1, len(fn827))
    stop_nodes828 = [m for m in ast.walk(fn827[0]) if isinstance(m, ast.If) and
                     ast.unparse(m.test) == 'len(changes) >= 2']
    gate828('STOP827_NODE_UNIQUE', len(stop_nodes828) == 1, len(stop_nodes828))
    sn828 = stop_nodes828[0]
    inner828 = sn828.body[2] if len(sn828.body) == 3 else None
    gate828('STOP827_STRUCTURE',
            [type(b).__name__ for b in sn828.body] == ['Assign', 'Assign', 'If'] and
            [ast.unparse(t) for t in sn828.body[0].targets] == ['recent'] and
            [ast.unparse(t) for t in sn828.body[1].targets] == ['baseline'] and
            [type(b).__name__ for b in inner828.body] == ['Assign', 'Break'] and
            ast.unparse(inner828.body[0].value) == "'RELATIVE_TENSOR_STABILITY'",
            ast.get_source_segment(src827_828, sn828))
    # Predicate shell parsed from a template; its test expressions and assignments are the
    # locked TEST827 AST nodes themselves (only `break` becomes `return True`).
    _pred828 = ast.parse('def locked_stop827(changes, velocity):\n    if OUTER:\n        pass\n    return False\n').body[0]
    _pred828.body[0].test = sn828.test
    _pred828.body[0].body = [sn828.body[0], sn828.body[1],
                             ast.If(test=inner828.test, body=[ast.Return(value=ast.Constant(value=True))], orelse=[])]
    exec(compile(ast.fix_missing_locations(ast.Module(body=[_pred828], type_ignores=[])),
                 'LOCKED_TEST827_STOP_CONDITION', 'exec'), globals())

    def stop_audit828(changes, velocity):
        # Read-only audit of the locked condition; never used for control.
        n = len(changes)
        if n < 2:
            return {'n': n, 'evaluated': False, 'fired': False}
        recent = np.asarray(changes[-2:], dtype=np.float64)
        med = float(np.median(changes)); baseline = max(med, 1e-12)
        return {'n': n, 'evaluated': True, 'max_recent': float(np.max(recent)), 'median': med,
                'baseline': baseline, 'recent_ratio': float(np.max(recent)) / baseline,
                'velocity_ratio': float(np.linalg.norm(velocity)) / baseline,
                'required_ratio_below': 0.10,
                'max_recent_ge_median': bool(float(np.max(recent)) >= med),
                'fired': bool(locked_stop827(changes, velocity))}

    rng_stop828 = np.random.default_rng(SEED828)
    fires828 = {}
    for n_ in (2, 3):
        cnt = 0
        for _ in range(50000):
            ch = list(10.0 ** rng_stop828.uniform(-12.0, 2.0, size=n_))
            cnt += bool(locked_stop827(ch, np.zeros(4)))
        for _ in range(50000):
            ch = list(np.exp(rng_stop828.normal(0.0, 6.0, size=n_)))
            cnt += bool(locked_stop827(ch, np.zeros(4)))
        fires828[n_] = cnt
    checked_lengths828 = [s - 1 for s in range(1, MAX_STEPS828 + 1) if s - 1 >= 2]
    D828['stop_rule_verification'] = {
        'source': '827.py run_trial827, git blob ' + LOCK827_828,
        'condition_source': ast.get_source_segment(src827_828, sn828),
        'checked_len_changes_with_MAX_STEPS_4': checked_lengths828,
        'random_positive_trials_per_n': 100000, 'velocity_used': 'zero (most permissive)',
        'fires_n2': fires828[2], 'fires_n3': fires828[3],
        'degenerate_zero_displacements_n2_fires': bool(locked_stop827([0.0, 0.0], np.zeros(4))),
        'n4_counterexample_[1,1,0.01,0.01]_fires': bool(locked_stop827([1.0, 1.0, 0.01, 0.01], np.zeros(4))),
        'analytic': ('For n in {2,3}, max(changes[-2:]) >= median(changes) (n=2: max >= mean; n=3: any two of '
                     'three values include one >= the median). If median >= 1e-12 the condition requires '
                     'max(recent) < 0.1*median <= 0.1*max(recent), impossible. If median < 1e-12 it requires '
                     'max(recent) < 1e-13 and ||velocity|| < 1e-13, i.e. numerically identical unit states. With '
                     'MAX_STEPS=4 the rule is evaluated only at len(changes) in {2,3}; it is therefore unreachable '
                     'for non-degenerate trajectories. For n >= 4 it is reachable (e.g. [1,1,0.01,0.01]).'),
        'modified_in_TEST828': False}
    gate828('STOP_RULE_IMPOSSIBILITY_VERIFIED',
            fires828[2] == 0 and fires828[3] == 0 and checked_lengths828 == [2, 3] and
            D828['stop_rule_verification']['degenerate_zero_displacements_n2_fires'] and
            D828['stop_rule_verification']['n4_counterexample_[1,1,0.01,0.01]_fires'],
            {k: D828['stop_rule_verification'][k] for k in ('fires_n2', 'fires_n3', 'checked_len_changes_with_MAX_STEPS_4')})

    # Token budget is validated BEFORE loading 72B model weights.
    tok828 = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=False)
    tok_counts828 = {cid: len(tok828.encode(body, add_special_tokens=False)) for cid, body in cards828.items()}
    gate828('TOKEN_BUDGET', all(4 <= n <= 256 for n in tok_counts828.values()),
            {'max_body_tokens': max(tok_counts828.values()), 'stage': 'TOKENIZER_PRE_MODEL'})
    del tok828

    t_load828 = time.perf_counter()
    model_setup()
    D828['model_load_seconds'] = round(time.perf_counter() - t_load828, 3)
    before828 = sentinel()
    gate828('FROZEN_PREFIX', P == 30, P)
    gate828('FUSION_BUDGET',
            P + MAX_STEPS828 * max(tok_counts828.values()) + 64 <= MAX_FUSED_TOKENS,
            {'max_body_tokens': max(tok_counts828.values()), 'max_fused_tokens': MAX_FUSED_TOKENS})
    gate828('FUSION_BUDGET_FINAL_SET',
            P + (MAX_STEPS828 + 1) * max(tok_counts828.values()) + 64 <= MAX_FUSED_TOKENS,
            {'cartridges': MAX_STEPS828 + 1})
    engine_bindings828('BEFORE_PHYSICAL_COMMIT')
    for cid, body in cards828.items():
        physical_commit(cid, body)
        gate828('BODY_SHA_' + cid, entries[cid].get('body_sha256') == sha828(body))
    gate828('PHYSICAL_COUNT', len(entries) == len(cards828), len(entries))
    for cid in cards828:
        p = safe_load(entries[cid])
        gate828('RELOAD_' + cid, p['book_id'] == cid and int(p['n']) > P and
                len(p['lower']) == CUT + 1 and tuple(p['h'].shape)[-1] == H)
        del p
    release()

    # Locked numerical H3 bank (identical to TEST827).
    bank828 = {}
    for cid in sorted(entries):
        cp = safe_load(entries[cid])
        try:
            x = cp['h'][0, P:, :].float().cpu().numpy()
            gate828('H3_NONEMPTY_' + cid, x.ndim == 2 and x.shape[0] > 8 and x.shape[1] == H)
            ix = np.linspace(0, len(x) - 1, min(96, len(x)), dtype=np.int64)
            bank828[cid] = normalized(x[ix]).T.copy()
        finally:
            del cp
    gate828('H3_BANK', len(bank828) == len(entries), len(bank828))

    def eligible828(world, arm):
        """Experimenter intervention, never inferred from answer or given to controller (TEST827 verbatim)."""
        pool = []
        for w in worlds828:
            ids = w['ids']
            pool += [ids['first'], ids['second']]
            if arm == 'ADD_IRRELEVANT':
                pool.append(ids['decoy'])
        current = next(w for w in worlds828 if w['world'] == world)
        if arm == 'REMOVE_SECOND':
            pool.remove(current['ids']['second'])
        elif arm == 'REPLACE_SECOND':
            pool.remove(current['ids']['second'])
            pool.append(current['ids']['changed'])
        elif arm == 'NULL':
            return [NULL828]
        return pool

    # ------------------------------------------------------------------------------------------
    # COMPUTE ACCOUNTING. Full-model forward passes are counted at their call sites:
    # fusion (initialize_native/native_append_direct: one forward per CHUNK of a mounted cartridge),
    # probe (observe_state: one forward), generation (free_generate: one forward per generated token),
    # rank (numeric_rank -> query_native: one forward).
    # ------------------------------------------------------------------------------------------
    CHUNK828 = int(globals().get('CHUNK', 128))
    COST828 = {}

    def cost828(cat, seconds=0.0, fusion=0, probe=0, generation=0, rank=0, mounts=0, measures=0):
        c = COST828.setdefault(cat, {'seconds': 0.0, 'fusion_forwards': 0, 'probe_forwards': 0,
                                     'generation_forwards': 0, 'rank_forwards': 0,
                                     'cartridge_mounts': 0, 'measurements': 0, 'peak_gpu_gib': 0.0})
        c['seconds'] += float(seconds); c['fusion_forwards'] += int(fusion); c['probe_forwards'] += int(probe)
        c['generation_forwards'] += int(generation); c['rank_forwards'] += int(rank)
        c['cartridge_mounts'] += int(mounts); c['measurements'] += int(measures)
        try:
            c['peak_gpu_gib'] = max(c['peak_gpu_gib'], float(_torch828.cuda.max_memory_allocated()) / 2**30)
        except Exception:
            pass

    def fusion_forwards828(ids):
        n = 0
        for k, cid in enumerate(ids):
            tokens = int(entries[cid]['body_tokens']) + (P if k == 0 else 0)
            n += (tokens + CHUNK828 - 1) // CHUNK828
        return n

    def reset_peak828():
        try:
            _torch828.cuda.reset_peak_memory_stats()
        except Exception:
            pass

    def _native828_verbose(ids, prompt, tag, max_new):
        t0 = time.perf_counter()
        engine_bindings828(tag)
        mem, active, fusion_steps, _ = build_fusion(ids, 'TEST828_' + tag, True)
        try:
            gate828('NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
            n = int(mem[0][0].shape[-2])
            expected = P + sum(int(entries[x]['body_tokens']) for x in ids)
            gate828('NATIVE_LENGTH_' + tag, n == expected, {'n': n, 'expected': expected})
            first = int(entries[ids[0]]['body_tokens'])
            spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                    {'B0': (P, n), 'B1': (n, n)}
            seals = memory_seals(mem)
            out = free_generate(mem, prompt, seed=None, gain=0., max_new=max_new, spans=spans)
            gate828('KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
            gate828('SDPA_RESTORED_' + tag,
                    _torch828.nn.functional.scaled_dot_product_attention is SDPA828)
            return {'raw': out['raw'], 'tokens': int(out['generated_tokens']),
                    'possibly_truncated': int(out['generated_tokens']) >= max_new,
                    'ids': list(ids), 'time_seconds': round(time.perf_counter() - t0, 3),
                    'fusion_steps': fusion_steps,
                    'cartridge_shas': [entries[x]['sha256'] for x in ids]}
        finally:
            del mem
            gc.collect()
            release()

    def native828(ids, prompt, tag, max_new):
        capture = io.StringIO()
        reset_peak828(); t0 = time.perf_counter()
        try:
            with contextlib.redirect_stdout(capture):
                result = _native828_verbose(ids, prompt, tag, max_new)
            cost828('BASELINE_FINAL_READOUT', time.perf_counter() - t0, fusion=fusion_forwards828(ids),
                    generation=result['tokens'], mounts=len(ids))
            return result
        except BaseException:
            log828('NATIVE_FAILURE_DIAGNOSTICS', tag, capture.getvalue()[-12000:])
            raise

    def answer_prompt828(question):
        # Readout boundary only; never used to choose a physical action (TEST827 verbatim text).
        return ('Use only mounted physical evidence. Follow directed links. '
                'If a link is missing, answer UNKNOWN. Return only the endpoint '
                'or UNKNOWN. Question: ' + question)

    # ------------------------------------------------------------------------------------------
    # 2. FULL-DEPTH READOUT: semantics inspection and observation-only capture.
    # The model's own forward is executed by the locked observe_state() unchanged. During that
    # single forward, model.lm_head.forward is temporarily replaced (same technique as the locked
    # Cut3Diagnostic: an instance-method replacement, never a hook) by a wrapper that calls the
    # original and returns its output object untouched, keeping copies of (a) the lm_head input at
    # the final position (= final-norm hidden state of block 80) and (b) the returned logits row.
    # ------------------------------------------------------------------------------------------
    gate828('NUMERICAL_PROBE_SYMBOL', callable(globals().get('observe_state')))
    head828 = model.lm_head
    import inspect as _inspect828
    try:
        _fwd_src828 = _inspect828.getsource(type(model).forward)
    except Exception as _e:
        _fwd_src828 = ''
    try:
        _sig828 = str(_inspect828.signature(type(model).forward))
    except Exception:
        _sig828 = ''
    W828 = getattr(head828, 'weight', None)
    is4bit828 = False
    try:
        is4bit828 = isinstance(head828, bitsandbytes.nn.Linear4bit)
    except Exception:
        pass
    FP64_MODE828 = (W828 is not None and not is4bit828 and
                    str(W828.dtype) in ('torch.bfloat16', 'torch.float16', 'torch.float32') and
                    tuple(W828.shape) == (int(model.config.vocab_size), H))
    VOCAB828 = int(model.config.vocab_size)
    NTOK828 = int(len(tok))
    D828['readout_semantics'] = {
        'transformers_version': getattr(globals().get('transformers'), '__version__', None),
        'torch_version': getattr(_torch828, '__version__', None),
        'model_class': type(model).__name__, 'lm_head_class': type(head828).__name__,
        'lm_head_weight_dtype': str(getattr(W828, 'dtype', None)),
        'lm_head_weight_shape': list(getattr(W828, 'shape', [])),
        'lm_head_has_bias': getattr(head828, 'bias', None) is not None,
        'lm_head_is_linear4bit': is4bit828,
        'config_vocab_size': VOCAB828, 'tokenizer_length': NTOK828,
        'padded_vocab_rows': VOCAB828 - NTOK828,
        'tie_word_embeddings': bool(getattr(model.config, 'tie_word_embeddings', False)),
        'final_logit_softcapping': getattr(model.config, 'final_logit_softcapping', None),
        'forward_signature': _sig828,
        'forward_source_has_logits_to_keep': 'logits_to_keep' in _fwd_src828,
        'forward_source_calls_lm_head': 'lm_head(' in _fwd_src828,
        'forward_source_contains_float_call': '.float()' in _fwd_src828,
        'precision_mode': 'FP64_RECOMPUTED_FROM_CAPTURED_FINAL_HIDDEN' if FP64_MODE828 else 'RETURNED_BF16_LOGITS_ONLY',
        'generation_interface': ('free_generate takes argmax of out.logits[0,-1] of the SAME forward; no '
                                 'temperature, top-k/top-p, repetition penalty or logits processor is applied'),
        'question_encoding': 'prompt_ids(question): question text only, no instruction (same as observe_state)'}
    HEAD_FWD828 = head828.__dict__.get('forward')   # original instance-level forward, if any
    gate828('READOUT_HEAD_NO_HOOKS', not head828._forward_hooks and not head828._forward_pre_hooks)
    gate828('READOUT_HEAD_SHAPE', W828 is not None and tuple(W828.shape)[-1] == H, list(getattr(W828, 'shape', [])))
    log828('TEST828_READOUT_SEMANTICS', json.dumps(D828['readout_semantics']))

    class Readout828:
        """Observation-only temporary replacement of lm_head.forward; restored on exit."""
        def __init__(self):
            self.old = None; self.had_instance = False; self.calls = 0
            self.h = None; self.z = None; self.in_shape = None; self.out_shape = None; self.out_dtype = None
        def __enter__(self):
            head = model.lm_head
            if head._forward_hooks or head._forward_pre_hooks:
                raise RuntimeError('LM_HEAD_HOOK_PRESENT')
            self.had_instance = 'forward' in head.__dict__
            self.old = head.forward; ctx = self
            def wrapped(this, *args, **kwargs):
                out = ctx.old(*args, **kwargs)
                x = args[0] if args else next(iter(kwargs.values()))
                ctx.calls += 1
                ctx.in_shape = tuple(x.shape); ctx.out_shape = tuple(out.shape); ctx.out_dtype = str(out.dtype)
                ctx.h = x[0, -1, :].detach().clone()
                ctx.z = out[0, -1, :].detach().clone()
                return out
            head.forward = types.MethodType(wrapped, head)
            return self
        def __exit__(self, *exc):
            head = model.lm_head
            if self.had_instance:
                head.forward = self.old
            else:
                head.__dict__.pop('forward', None)
            return False

    LN2_828 = math.log(2.0)

    def jsd828(lp, lq):
        # Exact Jensen-Shannon divergence (nats) over the FULL vocabulary, float64, log-space mixture.
        m = _torch828.logaddexp(lp, lq) - LN2_828
        p = _torch828.exp(lp); q = _torch828.exp(lq)
        zero = _torch828.zeros_like(p)
        a = _torch828.where(p > 0, p * (lp - m), zero).sum()
        b = _torch828.where(q > 0, q * (lq - m), zero).sum()
        v = float((0.5 * (a + b)).item())
        return min(max(v, 0.0), LN2_828)

    def tv828(lp, lq):
        return float((0.5 * (_torch828.exp(lp) - _torch828.exp(lq)).abs().sum()).item())

    def top1_828(lp):
        return int(lp.argmax().item())

    def full_readout828(h, z):
        zb = z.reshape(-1)
        lp16 = _torch828.log_softmax(zb.double(), dim=-1)
        summary = {}
        if FP64_MODE828:
            h64 = h.reshape(-1).double()
            parts = []
            for i in range(0, VOCAB828, LM_CHUNK828):
                parts.append(_torch828.matmul(W828[i:i + LM_CHUNK828].double(), h64))
            logits64 = _torch828.cat(parts)
            if getattr(head828, 'bias', None) is not None:
                logits64 = logits64 + head828.bias.double()
            del parts
            zd = zb.double()
            diff = (logits64 - zd).abs()
            mx = float(zd.abs().max().item())
            ulp = 2.0 ** (math.floor(math.log2(max(mx, 1e-30))) - 7)
            a = logits64 - logits64.mean(); b = zd - zd.mean()
            corr = float(((a * b).sum() / (a.norm() * b.norm()).clamp_min(1e-300)).item())
            summary.update({'reconstruction_max_abs': float(diff.max().item()),
                            'reconstruction_max_abs_in_bf16_ulp_at_max': float(diff.max().item()) / ulp,
                            'reconstruction_bf16_round_exact_fraction':
                                float((logits64.to(DTYPE) == zb).double().mean().item()),
                            'reconstruction_correlation': corr,
                            'argmax_fp64_equals_bf16': int(logits64.argmax().item()) == int(zb.argmax().item())})
            lp64 = _torch828.log_softmax(logits64, dim=-1)
            del logits64, diff, a, b, zd
        else:
            lp64 = lp16
        top = _torch828.topk(lp64, TOPK_STORE828)
        summary.update({
            'entropy_nats': float((-(_torch828.exp(lp64) * lp64)).sum().item()),
            'top_ids': [int(x) for x in top.indices.cpu().tolist()],
            'top_probs': [float(math.exp(x)) for x in top.values.cpu().tolist()],
            'argmax_bf16': int(zb.argmax().item()), 'argmax_fp64': top1_828(lp64),
            'padded_vocab_mass': (float(_torch828.exp(lp64[NTOK828:]).sum().item()) if VOCAB828 > NTOK828 else 0.0),
            'precision_jsd_fp64_vs_returned_bf16': jsd828(lp64, lp16),
            'logits_bf16_sha256': sha828(zb.float().cpu().numpy().tobytes()),
            'final_hidden_sha256': sha828(h.reshape(-1).float().cpu().numpy().tobytes())})
        return lp64, lp16, summary

    def measure828(ids, question, tag, category, gen_max=0):
        """Mount ids natively, run the locked observe_state once (wrapped readout), optionally run an
        offline-only greedy continuation in the SAME mounted memory. Returns numbers; text is offline-only."""
        capture = io.StringIO()
        reset_peak828(); t0 = time.perf_counter()
        try:
            with contextlib.redirect_stdout(capture):
                engine_bindings828(tag)
                mem, active, _, _ = build_fusion(ids, 'TEST828_MEAS_' + tag, True)
                try:
                    gate828('MEAS_NATIVE80_' + tag, len(mem) == NL and list(active) == list(ids))
                    n = int(mem[0][0].shape[-2])
                    gate828('MEAS_NATIVE_LENGTH_' + tag,
                            n == P + sum(int(entries[x]['body_tokens']) for x in ids))
                    first = int(entries[ids[0]]['body_tokens'])
                    spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                            {'B0': (P, n), 'B1': (n, n)}
                    seals = memory_seals(mem)
                    nq = len(prompt_ids(question))
                    with Readout828() as ro:
                        state, att = observe_state(mem, question, spans)
                    gate828('MEAS_HEAD_RESTORED_' + tag, model.lm_head.__dict__.get('forward') is HEAD_FWD828)
                    gate828('MEAS_READOUT_SEMANTICS_' + tag,
                            ro.calls == 1 and ro.out_shape is not None and ro.out_shape[0] == 1 and
                            ro.out_shape[-1] == VOCAB828 and ro.in_shape[-1] == H and
                            ro.out_shape[1] in (1, nq) and ro.in_shape[1] == ro.out_shape[1],
                            {'calls': ro.calls, 'in': ro.in_shape, 'out': ro.out_shape, 'nq': nq})
                    gate828('MEAS_STATE_' + tag, state.numel() == H and
                            bool(_torch828.isfinite(state).all().item()))
                    gate828('MEAS_FINITE_LOGITS_' + tag, bool(_torch828.isfinite(ro.z).all().item()))
                    lp64, lp16, summary = full_readout828(ro.h, ro.z)
                    if FP64_MODE828:
                        gate828('MEAS_LOGIT_RECONSTRUCTION_' + tag, summary['reconstruction_correlation'] >= 0.9999,
                                {k: summary[k] for k in summary if k.startswith('reconstruction')})
                    summary.update({'logits_rows_returned': ro.out_shape[1], 'question_tokens': nq,
                                    'logits_dtype': ro.out_dtype, 'ids': list(ids), 'memory_tokens': n})
                    gen = None
                    if gen_max:
                        out = free_generate(mem, question, seed=None, gain=0., max_new=gen_max, spans=spans)
                        gen = {'raw': out['raw'], 'tokens': int(out['generated_tokens']),
                               'possibly_truncated': int(out['generated_tokens']) >= gen_max}
                    gate828('MEAS_KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
                    gate828('MEAS_SDPA_' + tag,
                            _torch828.nn.functional.scaled_dot_product_attention is SDPA828)
                    vec = state.detach().float().cpu().numpy().copy()
                    summary['state_sha256'] = sha828(np.asarray(vec, dtype=np.float32).tobytes())
                    summary['state_norm'] = float(np.linalg.norm(vec))
                finally:
                    del mem
                    gc.collect()
                    release()
            elapsed = time.perf_counter() - t0
            cost828(category, elapsed, fusion=fusion_forwards828(ids), probe=1, mounts=len(ids), measures=1)
            if gen is not None:
                cost828('DESIGNED_OFFLINE_GENERATION', 0.0, generation=gen['tokens'])
            summary['seconds'] = round(elapsed, 3)
            return {'state': vec, 'att': att, 'lp': lp64, 'lp16': lp16, 'summary': summary,
                    'offline_generation': gen}
        except BaseException:
            log828('MEASUREMENT_FAILURE', tag, capture.getvalue()[-6000:])
            raise

    def unit828(x):
        y = np.asarray(x, dtype=np.float64).reshape(-1)
        norm = float(np.linalg.norm(y))
        if not np.isfinite(norm) or norm <= 1e-12:
            raise RuntimeError('NUMERIC_NONFINITE_OR_ZERO_STATE')
        return y / norm

    def pair828(a, b):
        # Label-free numerical comparison of two measurements.
        return {'jsd': jsd828(a['lp'], b['lp']), 'jsd_returned_bf16': jsd828(a['lp16'], b['lp16']),
                'tv': tv828(a['lp'], b['lp']), 'top1_same': top1_828(a['lp']) == top1_828(b['lp']),
                'cut3_state_cosine': float(np.dot(unit828(a['state']), unit828(b['state']))),
                'cut3_state_change': float(np.linalg.norm(unit828(a['state']) - unit828(b['state'])))}

    def additive828(lx, ly, lbase):
        # Additive (non-interacting) log-linear prediction: l_x + l_y - l_base, renormalised.
        return _torch828.log_softmax(lx + ly - lbase, dim=-1)

    # ------------------------------------------------------------------------------------------
    # NON-INTERFERENCE CHECK (once, label-free): the wrapped readout must leave the CUT3 state and
    # attention measurements bit-identical, and the captured argmax must equal the first greedy
    # token produced by the unchanged free_generate on the same mounted memory.
    # ------------------------------------------------------------------------------------------
    def noninterference828(ids, question):
        capture = io.StringIO(); reset_peak828(); t0 = time.perf_counter()
        with contextlib.redirect_stdout(capture):
            engine_bindings828('NONINTERFERENCE')
            mem, active, _, _ = build_fusion(ids, 'TEST828_NONINTERFERENCE', True)
            try:
                n = int(mem[0][0].shape[-2]); first = int(entries[ids[0]]['body_tokens'])
                spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else {'B0': (P, n), 'B1': (n, n)}
                seals = memory_seals(mem)
                s_plain, a_plain = observe_state(mem, question, spans)
                with Readout828() as ro:
                    s_wrapped, a_wrapped = observe_state(mem, question, spans)
                s_again, a_again = observe_state(mem, question, spans)
                g1 = free_generate(mem, question, seed=None, gain=0., max_new=1, spans=spans)
                tok_dec = tok.decode([int(ro.z.argmax().item())], skip_special_tokens=True).strip()
                res = {'state_bitwise_plain_vs_wrapped': bool(_torch828.equal(s_plain, s_wrapped)),
                       'state_bitwise_plain_vs_after': bool(_torch828.equal(s_plain, s_again)),
                       'attention_equal_plain_vs_wrapped': a_plain == a_wrapped,
                       'attention_equal_plain_vs_after': a_plain == a_again,
                       'first_greedy_token_equals_captured_argmax': g1['raw'] == tok_dec,
                       'head_restored': model.lm_head.__dict__.get('forward') is HEAD_FWD828,
                       'kv_sealed': compare_seals(seals, memory_seals(mem)),
                       'sdpa_restored': _torch828.nn.functional.scaled_dot_product_attention is SDPA828}
            finally:
                del mem; gc.collect(); release()
        cost828('NONINTERFERENCE_CHECK', time.perf_counter() - t0, fusion=fusion_forwards828(ids), probe=3,
                generation=1, mounts=len(ids))
        return res

    POLICIES828 = ('RETAINED_SIGNED',)
    SHADOW_NULL828 = {}

    def shadow_null828(q):
        # Physical NULL control under the same question: a runtime-known control cartridge,
        # not an answer label. Cached per question; used only by shadow measurements.
        if q['qid'] not in SHADOW_NULL828:
            SHADOW_NULL828[q['qid']] = measure828([NULL828], q['question'], q['qid'] + '_SHADOW_NULL', 'SHADOW_COUNTERFACTUAL')
        return SHADOW_NULL828[q['qid']]

    def shadow828(S, mS, q, tag):
        """Counterfactual shadow over the FINAL selected set S (opaque IDs only). Returns numbers only.
        Never influences the trajectory, the final readout, or stopping."""
        mN = shadow_null828(q)
        out = {'S': list(S), 'S_readout': mS['summary'], 'null_readout_sha': mN['summary']['logits_bf16_sha256'],
               'pi_S_vs_null': pair828(mS, mN)}
        rep = measure828(list(S), q['question'], tag + '_SH_REPLAY', 'SHADOW_COUNTERFACTUAL')
        out['replay'] = dict(pair828(mS, rep),
                             logits_bitwise=rep['summary']['logits_bf16_sha256'] == mS['summary']['logits_bf16_sha256'],
                             state_bitwise=rep['summary']['state_sha256'] == mS['summary']['state_sha256'])
        del rep
        out['order'] = {}
        if len(S) > 1:
            for name, perm in (('REVERSE', list(S)[::-1]), ('ROTATE', list(S)[1:] + list(S)[:1])):
                mp = measure828(perm, q['question'], tag + '_SH_' + name, 'SHADOW_COUNTERFACTUAL')
                out['order'][name] = dict(pair828(mS, mp), ids=perm, readout=mp['summary'])
                del mp
        loo, loo_m = [], {}
        if len(S) > 1:
            for k, cid in enumerate(S):
                rest = [c for c in S if c != cid]
                mr = measure828(rest, q['question'], tag + '_SH_LOO' + str(k), 'SHADOW_COUNTERFACTUAL')
                row = dict(pair828(mS, mr), removed=cid, position=k, pi_vs_null=jsd828(mr['lp'], mN['lp']),
                           readout=mr['summary'])
                loo.append(row); loo_m[cid] = mr
        out['leave_one_out'] = loo
        if loo:
            order = sorted(range(len(loo)), key=lambda k: (-loo[k]['jsd'], k))
            vals = [loo[k]['jsd'] for k in order]
            out['loo_sorted_jsd'] = vals
            out['loo_r2_second_over_first'] = (vals[1] / vals[0]) if len(vals) > 1 and vals[0] > 0 else None
            out['loo_profile_over_replay_floor'] = ([v / out['replay']['jsd'] for v in vals]
                                                    if out['replay']['jsd'] > 0 else None)
            a = S[order[0]]
            mk1 = measure828([a], q['question'], tag + '_SH_KEEP1', 'SHADOW_COUNTERFACTUAL')
            out['keep_top1'] = dict(pair828(mS, mk1), ids=[a], pi_vs_null=jsd828(mk1['lp'], mN['lp']),
                                    readout=mk1['summary'])
            del mk1
            if len(loo) > 1:
                b = S[order[1]]
                core = [c for c in S if c in (a, b)]
                mk2 = measure828(core, q['question'], tag + '_SH_KEEP2', 'SHADOW_COUNTERFACTUAL')
                out['keep_top2'] = dict(pair828(mS, mk2), ids=core, pi_vs_null=jsd828(mk2['lp'], mN['lp']),
                                        readout=mk2['summary'])
                del mk2
                if len(S) > 2:
                    dropped = [c for c in S if c not in (a, b)]
                    md = measure828(dropped, q['question'], tag + '_SH_DROP2', 'SHADOW_COUNTERFACTUAL')
                    lp_add = additive828(loo_m[a]['lp'], loo_m[b]['lp'], mS['lp'])
                    out['drop_top2'] = dict(pair828(mS, md), ids=dropped, pi_vs_null=jsd828(md['lp'], mN['lp']),
                                            readout=md['summary'])
                    out['pair_interaction_top2'] = {
                        'pair': [a, b], 'joint_removal_jsd': jsd828(mS['lp'], md['lp']),
                        'sum_individual_removal_jsd': loo[order[0]]['jsd'] + loo[order[1]]['jsd'],
                        'nonadditivity_jsd_vs_additive_prediction': jsd828(md['lp'], lp_add)}
                    del md, lp_add
        for v in loo_m.values():
            v['lp'] = None; v['lp16'] = None
        del loo_m
        return out

    def run_trial828(q, arm, policy):
        # TEST827 RETAINED_SIGNED controller, unchanged. Strictly blinded: no source-kind, truth labels or
        # answer text enters the controller. The only additions are read-only records (readout trajectory,
        # stop-rule audit) and the shadow counterfactuals AFTER the final readout.
        allowed = eligible828(q['world'], arm)
        t_rank = time.perf_counter()
        ranked, scores = numeric_rank(q['question'], {cid: bank828[cid] for cid in allowed})
        cost828('BASELINE_TRAJECTORY', time.perf_counter() - t_rank, rank=1)
        tag = q['qid'] + '_' + arm + '_' + policy
        gate828('RANK_' + tag, len(ranked) == len(allowed) and set(ranked) == set(allowed))
        mN = shadow_null828(q)   # independent shadow reference; does not touch controller variables
        first = ranked[0]
        selected = [first]
        m0 = measure828(selected, q['question'], tag + '_INITIAL', 'BASELINE_TRAJECTORY')
        initial_state = m0['state']
        reference = unit828(initial_state)
        previous = reference.copy()
        vals = np.array([float(scores[c]) for c in ranked], dtype=np.float64)
        gate828('FINITE_RANK_' + tag, bool(np.isfinite(vals).all()))
        spread = max(float(np.std(vals)), 1e-9)
        velocity = np.zeros(H, dtype=np.float64)
        osc_x = reference.copy()
        osc_v = np.zeros(H, dtype=np.float64)
        osc_history = []
        osc_prev_v = None
        osc_prev_force = None
        osc_gamma, osc_stiffness, osc_drive = 0.30, 0.12, 0.30
        changes, alignment_history, decisions, rejected = [], [], [], []
        trace = [{'step': 0, 'ids': selected[:],
                  'state_sha256': sha828(np.asarray(initial_state, dtype=np.float32).tobytes())}]
        readout_traj = [{'step': 0, 'ids_count': 1, 'jsd_to_previous': None,
                         'jsd_to_null': jsd828(m0['lp'], mN['lp']), 'entropy_nats': m0['summary']['entropy_nats'],
                         'top_ids': m0['summary']['top_ids'], 'top_probs': m0['summary']['top_probs']}]
        m_prev = m0
        stop_audit = []
        stop_reason = None
        safety_stop = None
        for step in range(1, MAX_STEPS828 + 1):
            candidates = [c for c in ranked if c not in selected]
            if not candidates:
                stop_reason = 'CANDIDATE_EXHAUSTION'
                break
            utilities = {}
            for cid in candidates:
                matrix = np.asarray(bank828[cid], dtype=np.float64)
                colnorm = np.maximum(np.linalg.norm(matrix, axis=0), 1e-12)
                sims = (previous @ matrix) / colnorm
                signed = float(np.quantile(sims, 0.75))
                rank_z = (float(scores[cid]) - float(np.mean(vals))) / spread
                derivative = float(np.dot(velocity, unit828(np.mean(matrix, axis=1)))) if np.linalg.norm(velocity) > 1e-12 else 0.0
                feedback = 0.0
                utilities[cid] = {'signed_alignment': signed, 'rank_z': rank_z,
                                  'derivative': derivative, 'feedback': feedback,
                                  'priority': rank_z + signed + feedback}
            ordered = sorted(candidates, key=lambda c: (-utilities[c]['priority'], ranked.index(c)))
            rejected.append({'step': step, 'candidate_order': ordered,
                             'candidate_metrics': {c: dict(utilities[c]) for c in candidates},
                             'selected_before_step': selected[:],
                             'priority_gap_top2': (float(utilities[ordered[0]]['priority'] -
                                                         utilities[ordered[1]]['priority']) if len(ordered)>1 else None)})
            target = ordered[0]
            # Stability stop: the EXACT locked TEST827 condition (compiled from 827.py), audited read-only.
            stop_audit.append(dict(stop_audit828(changes, velocity), step=step))
            if locked_stop827(changes, velocity):
                stop_reason = 'RELATIVE_TENSOR_STABILITY'
                break
            next_ids = selected + [target]
            gate828('UNIQUE_ACTIVE_' + tag + '_' + str(step), len(set(next_ids)) == len(next_ids))
            m_new = measure828(next_ids, q['question'], tag + '_STEP_' + str(step), 'BASELINE_TRAJECTORY')
            new_state, att = m_new['state'], m_new['att']
            current = unit828(new_state)
            osc_force = osc_drive * (current - previous) - osc_stiffness * (osc_x - current)
            osc_v = (1.0 - osc_gamma) * osc_v + osc_force
            speed_before = float(np.linalg.norm(osc_v))
            force_norm = float(np.linalg.norm(osc_force))
            force_work = float(np.dot(osc_force, osc_v))
            turn_cos = (float(np.dot(osc_prev_v, osc_v) /
                              max(np.linalg.norm(osc_prev_v) * speed_before, 1e-12))
                        if osc_prev_v is not None else None)
            force_turn_cos = (float(np.dot(osc_prev_force, osc_force) /
                                    max(np.linalg.norm(osc_prev_force) * force_norm, 1e-12))
                              if osc_prev_force is not None else None)
            osc_prev_v = osc_v.copy()
            osc_prev_force = osc_force.copy()
            osc_x = osc_x + osc_v
            osc_error = float(np.linalg.norm(osc_x - current))
            osc_speed = float(np.linalg.norm(osc_v))
            osc_energy = float(0.5 * osc_speed**2 + 0.5 * osc_stiffness * osc_error**2)
            osc_history.append({'step': step, 'velocity_norm': osc_speed,
                                'tracking_error': osc_error,
                                'drive_norm': float(np.linalg.norm(current - previous)),
                                'energy': osc_energy,
                                'energy_delta': osc_energy - osc_history[-1]['energy'] if osc_history else None,
                                'force_norm': force_norm, 'force_work': force_work,
                                'velocity_turn_cosine': turn_cos, 'force_turn_cosine': force_turn_cos,
                                'energy_ratio': (osc_energy / max(osc_history[-1]['energy'], 1e-12)
                                                 if osc_history else None)})
            gate828('DRA_SHADOW_FINITE_' + tag + '_' + str(step),
                    bool(np.isfinite(osc_energy) and np.isfinite(osc_speed) and np.isfinite(osc_error)))
            delta = current - previous
            displacement = float(np.linalg.norm(delta))
            velocity = 0.30 * velocity + 0.70 * delta
            signed_change = float(np.dot(previous, current))
            alignment_history.append(signed_change)
            changes.append(displacement)
            gate828('FINITE_FEEDBACK_' + tag + '_' + str(step),
                    bool(np.isfinite(displacement) and np.isfinite(velocity).all() and
                         np.isfinite(utilities[target]['priority'])))
            decisions.append({'step': step, 'target': target, 'rank_score': float(scores[target]),
                              'priority': utilities[target]['priority'],
                              'signed_alignment': utilities[target]['signed_alignment'],
                              'derivative': utilities[target]['derivative'],
                              'feedback': utilities[target]['feedback'],
                              'state_change': displacement, 'state_cosine': signed_change,
                              'alignment_delta': signed_change - (alignment_history[-2] if len(alignment_history)>1 else 1.0),
                              'velocity_norm': float(np.linalg.norm(velocity)),
                              'active_count': len(next_ids)})
            trace.append({'step': step, 'ids': next_ids[:],
                          'state_sha256': sha828(np.asarray(new_state, dtype=np.float32).tobytes())})
            # Read-only full-depth readout trajectory (same forward as the CUT3 probe; zero extra passes).
            readout_traj.append({'step': step, 'ids_count': len(next_ids),
                                 'jsd_to_previous': jsd828(m_prev['lp'], m_new['lp']),
                                 'jsd_to_null': jsd828(m_new['lp'], mN['lp']),
                                 'tv_to_previous': tv828(m_prev['lp'], m_new['lp']),
                                 'top1_changed': top1_828(m_prev['lp']) != top1_828(m_new['lp']),
                                 'entropy_nats': m_new['summary']['entropy_nats'],
                                 'top_ids': m_new['summary']['top_ids'], 'top_probs': m_new['summary']['top_probs'],
                                 'cut3_state_change': displacement})
            m_prev = m_new
            selected = next_ids
            previous = current
        if stop_reason is None:
            safety_stop = 'MAX_STEPS_SAFETY_BOUND'
        initial = {'raw': '[SKIPPED_DIAGNOSTIC_READOUT]'}
        final = native828(selected, answer_prompt828(q['question']),
                          tag + '_FINAL_READOUT', MAX_NEW_ANSWER828)
        # SHADOW: counterfactual observability on the final set; after all control actions are complete.
        shadow = shadow828(selected, m_prev, q, tag)
        m0['lp'] = None; m_prev['lp'] = None
        return {'qid': q['qid'], 'arm': arm, 'policy': policy, 'question': q['question'],
                'initial': initial['raw'].strip(), 'final': final['raw'].strip(),
                'final_tokens': final['tokens'], 'final_possibly_truncated': final['possibly_truncated'],
                'initial_selected': [first], 'ranked_ids': ranked,
                'ranked_scores': {cid: float(scores[cid]) for cid in ranked},
                'trace': trace, 'model_decisions': decisions, 'validity_gate_audit': rejected,
                'causal_ablations': [], 'dra_shadow': osc_history,
                'stop_rule_audit': stop_audit, 'shadow_readout_trajectory': readout_traj,
                'counterfactual_shadow': shadow,
                'model_stop': False, 'numerical_stop': stop_reason in ('RELATIVE_TENSOR_STABILITY', 'NUMERIC_VALIDITY_ABSTENTION'),
                'numeric_stop_reason': stop_reason, 'safety_stop': safety_stop,
                'steps_executed': len(decisions), 'model_actions': ['NUMERIC_READ'] * len(decisions),
                'valid_decisions': len(decisions), 'first_valid_decisions': len(decisions),
                'repair_attempts': 0, 'repair_successes': 0,
                'controller_decisions': len(decisions)}

    # ------------------------------------------------------------------------------------------
    # 5./6. DESIGNED ONE-HOP TRUNCATION PANEL (highest priority; executed first).
    # Runtime iterates opaque intervention IDs only. All pairwise distances and all set-algebra
    # interaction tests are computed generically (label-free) from the cartridge lists.
    # ------------------------------------------------------------------------------------------
    qlookup828 = {q['qid']: q for q in questions828}   # qid -> question text (boundary input)
    D828['noninterference'] = noninterference828(design_public828[0]['ids'],
                                                 qlookup828[design_public828[0]['qid']]['question'])
    for k_, v_ in D828['noninterference'].items():
        gate828('NONINTERFERENCE_' + k_.upper(), bool(v_), v_)

    for qid in [q['qid'] for q in questions828]:
        rows = [r for r in design_public828 if r['qid'] == qid]
        question = qlookup828[qid]['question']
        meas = {}
        for r in rows:
            m = measure828(r['ids'], question, r['xid'], 'DESIGNED_PANEL',
                           gen_max=MAX_NEW_OFFLINE828 if r['offline_generation'] else 0)
            meas[r['xid']] = m
            log828('TEST828_DESIGNED_MEASURE', qid, r['xid'], 'k', len(r['ids']),
                   'H', round(m['summary']['entropy_nats'], 4), 'p1', round(m['summary']['top_probs'][0], 4))
        xids = [r['xid'] for r in rows]
        pairs828 = {}
        for a_i in range(len(xids)):
            for b_i in range(a_i + 1, len(xids)):
                pairs828[xids[a_i] + '|' + xids[b_i]] = pair828(meas[xids[a_i]], meas[xids[b_i]])
        idsets = {x: tuple(next(r['ids'] for r in rows if r['xid'] == x)) for x in xids}
        null_x = [x for x in xids if idsets[x] == (NULL828,)]
        interactions = []
        if len(null_x) == 1:
            nx = null_x[0]
            for z in xids:
                for xa in xids:
                    for xb in xids:
                        A, B, Z = set(idsets[xa]), set(idsets[xb]), set(idsets[z])
                        if (xa < xb and xa != z and xb != z and NULL828 not in A | B | Z and
                                not (A & B) and (A | B) == Z):
                            lp_add = additive828(meas[xa]['lp'], meas[xb]['lp'], meas[nx]['lp'])
                            interactions.append({
                                'z': z, 'x': xa, 'y': xb, 'null': nx,
                                'nonadditivity_jsd': jsd828(meas[z]['lp'], lp_add),
                                'effect_z_vs_null': jsd828(meas[z]['lp'], meas[nx]['lp']),
                                'effect_x_vs_null': jsd828(meas[xa]['lp'], meas[nx]['lp']),
                                'effect_y_vs_null': jsd828(meas[xb]['lp'], meas[nx]['lp']),
                                'z_vs_x': jsd828(meas[z]['lp'], meas[xa]['lp']),
                                'z_vs_y': jsd828(meas[z]['lp'], meas[xb]['lp'])})
                            del lp_add
        D828['designed'].append({'qid': qid, 'execution_order': xids,
                                 'measurements': {x: {'ids': list(idsets[x]), 'readout': meas[x]['summary']}
                                                  for x in xids},
                                 'pairwise': pairs828, 'set_interactions': interactions})
        # Offline-only text kept apart; no runtime function reads this field.
        D828.setdefault('offline_only_designed_generation', {})[qid] = {
            x: meas[x]['offline_generation'] for x in xids}
        for x in xids:
            meas[x]['lp'] = None; meas[x]['lp16'] = None
        del meas
        gc.collect(); release()
        save828()

    for q in questions828:
        for arm in ARMS828:
            for policy in POLICIES828:
                row = run_trial828(q, arm, policy)
                D828['trials'].append(row)
                save828()
                sh = row['counterfactual_shadow']
                log828('TEST828_TRIAL', row['qid'], arm, policy, 'steps', row['steps_executed'],
                       'stop', row['numeric_stop_reason'] or row['safety_stop'],
                       'LOO_r2', None if sh.get('loo_r2_second_over_first') is None else round(sh['loo_r2_second_over_first'], 4),
                       'final', repr(row['final'][:80]))
    for v in SHADOW_NULL828.values():
        v['lp'] = None; v['lp16'] = None

    D828['fixed_baseline'] = []
    gate828('TRIAL_COUNT', len(D828['trials']) == len(questions828) * len(ARMS828) * len(POLICIES828),
            len(D828['trials']))
    gate828('DESIGNED_COUNT', sum(len(d['measurements']) for d in D828['designed']) == len(design_public828))
    engine_bindings828('FINAL')
    gate828('FROZEN_WEIGHT_SENTINEL', before828 == sentinel())
    gate828('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    gate828('LM_HEAD_UNWRAPPED', model.lm_head.__dict__.get('forward') is HEAD_FWD828 and
            not model.lm_head._forward_hooks and not model.lm_head._forward_pre_hooks)
    gate828('PANEL_UNCHANGED', sha828(json.dumps(PANEL828, ensure_ascii=False, sort_keys=True)) == PANEL_SHA828)
    for cid in cards828:
        gate828('FINAL_SHA_' + cid, sha_file(CART_DIR / entries[cid]['file']) == entries[cid]['sha256'])
    D828['runtime_seconds_total'] = round(time.perf_counter() - T0_828, 3)

    # ==========================================================================================
    # OFFLINE EVALUATION. Everything below runs after all model calls; labels are used here only.
    # ==========================================================================================
    lookup828 = {q['qid']: q for q in questions828}
    world_of828 = {w['world']: w for w in worlds828}
    kind828 = {cid: m['kind'] for cid, m in card_meta828.items()}
    dom828 = {cid: m['domain'] for cid, m in card_meta828.items()}

    def role_of828(cid, w):
        if cid == NULL828:
            return 'NULL'
        if dom828.get(cid) == w['world']:
            return 'OWN_' + kind828[cid].upper()
        return 'OTHER_' + kind828[cid].upper()

    def classify828(text, w):
        t = (text or '').strip(); u = t.upper()
        clean = u.strip(' .\n*`"\'')
        own = {'END': w['end'], 'MIDDLE': w['middle'], 'START': w['start'],
               'CHANGED_END': w['changed_end'], 'DECOY_END': w['decoy_end']}
        others = {c: 'OTHER_WORLD' for ow in worlds828 if ow is not w
                  for c in (ow['start'], ow['middle'], ow['end'], ow['decoy_end'])}
        pos = []
        for role, c in own.items():
            for mt in re.finditer(re.escape(c), u):
                pos.append((mt.start(), role))
        for c, role in others.items():
            for mt in re.finditer(re.escape(c), u):
                pos.append((mt.start(), role))
        pos.sort()
        last = pos[-1][1] if pos else None
        if u.startswith('UNKNOWN'):
            cls = 'UNKNOWN_PREFIX'
        elif clean == w['end']:
            cls = 'OWN_END_EXACT'
        elif clean == w['middle']:
            cls = 'OWN_MIDDLE_EXACT_TRUNCATION'
        elif last == 'END':
            cls = 'OWN_END_LAST_MENTIONED'
        elif last == 'MIDDLE':
            cls = 'OWN_MIDDLE_LAST_MENTIONED_TRUNCATION'
        elif 'UNKNOWN' in u:
            cls = 'UNKNOWN_CONTAINED'
        elif last is not None:
            cls = 'OTHER_CODE_' + last
        else:
            cls = 'NO_CODE'
        return {'class': cls, 'mentions': [r for _, r in pos], 'legacy_827_exact_end': u.strip(' .\n') == w['end'],
                'legacy_827_exact_unknown': u == 'UNKNOWN'}

    def first_ids828(code):
        out = set()
        for variant in (code, ' ' + code):
            ids_ = tok(variant, add_special_tokens=False).input_ids
            ids_ = [t_ for t_ in ids_ if tok.decode([t_], skip_special_tokens=True).strip()]   # skip pure-whitespace pieces
            if ids_:
                out.add(ids_[0])
        return sorted(out)

    unknown_first828 = first_ids828('UNKNOWN')

    def top_presence828(readout, ids_):
        out = []
        for t_ in ids_:
            if t_ in readout['top_ids']:
                out.append({'token': t_, 'rank': readout['top_ids'].index(t_) + 1,
                            'prob': readout['top_probs'][readout['top_ids'].index(t_)]})
        return out

    # ---- designed panel ----
    D828['offline_designed'] = []
    CONTROL_PAIRS828 = (('FIRST', 'FIRST_DECOY'), ('FIRST', 'FIRST_OTHER'), ('BOTH', 'BOTH_DECOY'),
                        ('BOTH', 'BOTH_REV'), ('BOTH', 'BOTH_REPLAY'))
    for d in D828['designed']:
        w = world_of828[lookup828[d['qid']]['world']]
        x_of = {design_key828[x]['role']: x for x in d['execution_order']}

        def dist(r1, r2, key='jsd'):
            a, b = x_of[r1], x_of[r2]
            p = d['pairwise'].get(a + '|' + b) or d['pairwise'].get(b + '|' + a)
            return p[key]
        gens = D828['offline_only_designed_generation'][d['qid']]
        cls = {}
        for role, x in x_of.items():
            g_ = gens.get(x)
            rd = d['measurements'][x]['readout']
            first_tok = tok.decode([rd['argmax_bf16']], skip_special_tokens=True).strip()
            cls[role] = {'greedy_question_only': None if g_ is None else g_['raw'],
                         'greedy_class': None if g_ is None else classify828(g_['raw'], w)['class'],
                         'greedy_tokens': None if g_ is None else g_['tokens'],
                         'readout_top1_token_text': first_tok,
                         'first_token_consistent_with_greedy': (None if g_ is None else
                                                                (g_['raw'] or '').startswith(first_tok)),
                         'entropy_nats': rd['entropy_nats'], 'top1_prob': rd['top_probs'][0],
                         'own_end_first_token_in_top8': top_presence828(rd, first_ids828(w['end'])),
                         'own_middle_first_token_in_top8': top_presence828(rd, first_ids828(w['middle'])),
                         'unknown_first_token_in_top8': top_presence828(rd, unknown_first828),
                         'precision_jsd': rd['precision_jsd_fp64_vs_returned_bf16']}
        evidence = dist('FIRST', 'BOTH'); evidence16 = dist('FIRST', 'BOTH', 'jsd_returned_bf16')
        controls = {a + '~' + b: dist(a, b) for a, b in CONTROL_PAIRS828}
        controls16 = {a + '~' + b: dist(a, b, 'jsd_returned_bf16') for a, b in CONTROL_PAIRS828}
        cmax = max(controls.values()); cmax16 = max(controls16.values())
        inter = {}
        for it in d['set_interactions']:
            key = design_key828[it['x']]['role'] + '+' + design_key828[it['y']]['role'] + '->' + design_key828[it['z']]['role']
            inter[key] = {k: v for k, v in it.items() if k not in ('x', 'y', 'z', 'null')}
        ef, es = first_ids828(w['end']), first_ids828(w['middle'])
        D828['offline_designed'].append({
            'qid': d['qid'], 'world': w['world'],
            'evidence_effect_FIRST_vs_BOTH_jsd': evidence,
            'matched_controls_jsd': controls, 'max_control_jsd': cmax,
            'separation_margin': evidence / max(cmax, 1e-300),
            'separated_beyond_all_controls': evidence > cmax,
            'separation_margin_returned_bf16': evidence16 / max(cmax16, 1e-300),
            'separated_beyond_all_controls_returned_bf16': evidence16 > cmax16,
            'prior_NULL_vs_FIRST_jsd': dist('NULL', 'FIRST'), 'prior_NULL_vs_BOTH_jsd': dist('NULL', 'BOTH'),
            'SECOND_alone_vs_NULL_jsd': dist('NULL', 'SECOND'),
            'top1_same_FIRST_BOTH': dist('FIRST', 'BOTH', 'top1_same'),
            'cut3_state_change_FIRST_BOTH': dist('FIRST', 'BOTH', 'cut3_state_change'),
            'cut3_state_change_FIRST_FIRST_DECOY': dist('FIRST', 'FIRST_DECOY', 'cut3_state_change'),
            'replay_jsd_BOTH': dist('BOTH', 'BOTH_REPLAY'),
            'replay_bitwise_BOTH': (d['measurements'][x_of['BOTH']]['readout']['logits_bf16_sha256'] ==
                                    d['measurements'][x_of['BOTH_REPLAY']]['readout']['logits_bf16_sha256']),
            'order_jsd_BOTH_vs_BOTH_REV': dist('BOTH', 'BOTH_REV'),
            'set_interactions_by_role': inter,
            'end_and_middle_share_first_token': bool(set(ef) & set(es)),
            'roles': cls,
            'answer_level_truncation_FIRST_middle_BOTH_end': (
                (cls['FIRST']['greedy_class'] or '').startswith('OWN_MIDDLE') and
                (cls['BOTH']['greedy_class'] or '').startswith('OWN_END'))})

    # ---- trials: legacy and prefix-aware scoring; shadow by role ----
    scored828 = []
    D828['offline_trials'] = []
    for r in D828['trials']:
        key = lookup828[r['qid']]; w = world_of828[key['world']]
        c = classify828(r['final'], w)
        should_unknown = r['arm'] in ('REMOVE_SECOND', 'NULL')
        legacy = c['legacy_827_exact_unknown'] if should_unknown else c['legacy_827_exact_end']
        prefix_ok = (c['class'] == 'UNKNOWN_PREFIX') if should_unknown else c['class'] in ('OWN_END_EXACT', 'OWN_END_LAST_MENTIONED')
        scored828.append({'qid': r['qid'], 'arm': r['arm'], 'policy': r['policy'],
                          'expected': 'UNKNOWN' if should_unknown else key['expected'],
                          'exact_correct': legacy, 'prefix_aware_correct': prefix_ok,
                          'final_class': c['class'], 'model_stop': r['model_stop'],
                          'initial': r['initial'], 'final': r['final']})
        sh = r['counterfactual_shadow']
        S = sh['S']; roles = [role_of828(x, w) for x in S]
        loo = sh.get('leave_one_out', [])
        top_roles = [role_of828(loo[k]['removed'], w) for k in
                     sorted(range(len(loo)), key=lambda k: (-loo[k]['jsd'], k))]
        D828['offline_trials'].append({
            'qid': r['qid'], 'arm': r['arm'], 'final_set_roles': roles,
            'has_own_first': 'OWN_FIRST' in roles, 'has_own_second': 'OWN_SECOND' in roles,
            'evidence_status': ('COMPLETE' if 'OWN_FIRST' in roles and 'OWN_SECOND' in roles else
                                'TRUNCATED' if 'OWN_FIRST' in roles else 'NO_START_LINK'),
            'final_class': c['class'],
            'loo_by_role': {role_of828(x['removed'], w) + '@' + str(x['position']): x['jsd'] for x in loo},
            'loo_roles_by_magnitude': top_roles,
            'loo_r2_second_over_first': sh.get('loo_r2_second_over_first'),
            'replay_jsd': sh['replay']['jsd'], 'replay_logits_bitwise': sh['replay']['logits_bitwise'],
            'order_reverse_jsd': sh['order'].get('REVERSE', {}).get('jsd'),
            'order_rotate_jsd': sh['order'].get('ROTATE', {}).get('jsd'),
            'min_loo_jsd': min([x['jsd'] for x in loo]) if loo else None,
            'keep_top1_role': role_of828(sh['keep_top1']['ids'][0], w) if 'keep_top1' in sh else None,
            'keep_top1_vs_S_jsd': sh.get('keep_top1', {}).get('jsd'),
            'keep_top1_top1_same': sh.get('keep_top1', {}).get('top1_same'),
            'keep_top2_roles': [role_of828(x, w) for x in sh.get('keep_top2', {}).get('ids', [])],
            'keep_top2_vs_S_jsd': sh.get('keep_top2', {}).get('jsd'),
            'pair_interaction_top2': sh.get('pair_interaction_top2'),
            'pi_S_vs_null': sh['pi_S_vs_null']['jsd'],
            'stop_rule_audit': r['stop_rule_audit']})

    # ---- predeclared offline verdict rules (written before any result exists) ----
    # H1 (designed observability): in a world, D(FIRST,BOTH) exceeds EVERY matched control
    #     (adding an irrelevant same-domain or cross-domain card to FIRST; adding an irrelevant card,
    #     reversing order, or replaying BOTH). Required in all pilot worlds.
    # H2 (label-free runtime separation): the leave-one-out ratio r2 = L(2)/L(1) on the final set is
    #     larger for every COMPLETE final set than for every TRUNCATED final set.
    # Order diagnostic: B(S) > replay floor => deterministic representational change, not numerical noise.
    odes = D828['offline_designed']
    h1_worlds = sum(x['separated_beyond_all_controls'] for x in odes)
    h1 = h1_worlds == len(odes) and len(odes) > 0
    h1_bf16 = all(x['separated_beyond_all_controls_returned_bf16'] for x in odes) and len(odes) > 0
    comp = [x['loo_r2_second_over_first'] for x in D828['offline_trials']
            if x['evidence_status'] == 'COMPLETE' and x['loo_r2_second_over_first'] is not None]
    trunc = [x['loo_r2_second_over_first'] for x in D828['offline_trials']
             if x['evidence_status'] == 'TRUNCATED' and x['loo_r2_second_over_first'] is not None]
    h2 = bool(comp and trunc and min(comp) > max(trunc))
    replay_all = [x['replay_jsd'] for x in D828['offline_trials']] + [x['replay_jsd_BOTH'] for x in odes]
    replay_bitwise_all = (all(x['replay_logits_bitwise'] for x in D828['offline_trials']) and
                          all(x['replay_bitwise_BOTH'] for x in odes))
    order_all = [v for x in D828['offline_trials'] for v in (x['order_reverse_jsd'], x['order_rotate_jsd'])
                 if v is not None] + [x['order_jsd_BOTH_vs_BOTH_REV'] for x in odes]
    replay_floor = max(replay_all) if replay_all else 0.0
    order_class = ('NO_ORDER_MEASUREMENTS' if not order_all else
                   'REPRESENTATIONAL_CHANGE' if min(order_all) > replay_floor else
                   'NOT_SEPARABLE_FROM_NUMERICAL_REPLAY_VARIATION')
    rev_answer_changed = [x['roles']['BOTH']['greedy_class'] != x['roles']['BOTH_REV']['greedy_class'] for x in odes]
    truncated_trials = [x for x in D828['offline_trials'] if x['evidence_status'] == 'TRUNCATED']
    max_prec = max([m['readout']['precision_jsd_fp64_vs_returned_bf16'] for d in D828['designed']
                    for m in d['measurements'].values()] or [0.0])
    if h1 and h2:
        answer828 = 'YES_IN_THIS_THREE_WORLD_PILOT_WITH_LIMITATIONS'
        barrier828 = None
    elif h1:
        answer828 = 'PARTIAL_OBSERVABLE_ONLY_WITH_EXPERIMENTER_SUPPLIED_ONE_LINK_REFERENCE'
        barrier828 = ('The full-depth readout separates FIRST from BOTH beyond matched controls, but the label-free '
                   'leave-one-out profile of the final selected set did not separate complete from truncated sets: '
                   'the runtime lacks the one-link reference that makes the difference visible.')
    elif h2:
        answer828 = 'INCONCLUSIVE_RUNTIME_SEPARATION_WITHOUT_DESIGNED_SEPARATION'
        barrier828 = 'Runtime r2 separated, but the designed FIRST-vs-BOTH effect did not exceed every matched control.'
    else:
        answer828 = 'NO_OBSERVABILITY_BARRIER'
        barrier828 = ('Adding the second relevant link does not change the full-depth next-token readout more than '
                   'matched irrelevant-addition, order or replay controls, and the label-free leave-one-out profile '
                   'does not separate complete from truncated final sets.')
    D828['offline_verdict'] = {
        'acceptance_question': ("Can the frozen model's existing full-depth numerical response to physical memory-set "
                                "interventions distinguish sufficient two-hop evidence from incomplete one-hop evidence "
                                "without any language-mediated control or access to the answer key?"),
        'answer': answer828, 'observability_barrier': barrier828,
        'H1_designed_worlds_separated': h1_worlds, 'H1_worlds_total': len(odes), 'H1': h1,
        'H1_holds_with_returned_bf16_logits': h1_bf16,
        'separation_margins': [x['separation_margin'] for x in odes],
        'evidence_effects_jsd': [x['evidence_effect_FIRST_vs_BOTH_jsd'] for x in odes],
        'max_control_jsd': [x['max_control_jsd'] for x in odes],
        'H2_runtime_r2_complete': comp, 'H2_runtime_r2_truncated': trunc, 'H2': h2,
        'answer_level_truncation_reproduced_worlds': sum(x['answer_level_truncation_FIRST_middle_BOTH_end'] for x in odes),
        'truncated_final_sets_keep_top1_is_own_first': sum(x['keep_top1_role'] == 'OWN_FIRST' for x in truncated_trials),
        'truncated_final_sets_count': len(truncated_trials),
        'order_noise_classification': order_class,
        'order_jsd_values': order_all, 'replay_floor_jsd': replay_floor, 'replay_bitwise_all': replay_bitwise_all,
        'reverse_order_changed_greedy_answer_worlds': sum(rev_answer_changed),
        'B_S_admissible_as_stopping_threshold': False,
        'B_S_reason': ('Recorded as a diagnostic only (directive 4). Order perturbations classified as ' + order_class +
                       '; native CUT3 fusion is order-dependent, so B(S) is not a noise floor for evidence relevance.'),
        'max_precision_jsd_fp64_vs_bf16_designed': max_prec,
        'stopping': {'rule_modified': False, 'numerical_stability_stops': sum(r['numeric_stop_reason'] == 'RELATIVE_TENSOR_STABILITY' for r in D828['trials']),
                     'safety_bound_stops': sum(r['safety_stop'] == 'MAX_STEPS_SAFETY_BOUND' for r in D828['trials']),
                     'claim': 'NO_AUTONOMOUS_STOPPING_CLAIM'},
        'six_world_extension': ('JUSTIFIED_TO_TEST_STABILITY_OF_PILOT_SEPARATION' if h1 else
                                'NOT_JUSTIFIED_PILOT_SHOWED_NO_MEANINGFUL_SEPARATION'),
        'caveats': ['Next-token full-depth distributions are not multi-token answers; see first-token consistency and greedy classes.',
                    'Low divergence does not prove correctness; nonzero leave-one-out does not prove logical necessity.',
                    'H2 uses role labels only offline to group final sets; the r2 statistic itself is label-free.',
                    'Three worlds and three trials per arm: descriptive pilot only.']}

    # ---- compute cost ----
    base_keys = ('BASELINE_TRAJECTORY', 'BASELINE_FINAL_READOUT')
    add_keys = ('SHADOW_COUNTERFACTUAL', 'DESIGNED_PANEL', 'DESIGNED_OFFLINE_GENERATION', 'NONINTERFERENCE_CHECK')
    def total828(keys, field):
        return sum(COST828.get(k, {}).get(field, 0) for k in keys)
    fwd_fields = ('fusion_forwards', 'probe_forwards', 'generation_forwards', 'rank_forwards')
    base_fwd = sum(total828(base_keys, f) for f in fwd_fields)
    add_fwd = sum(total828(add_keys, f) for f in fwd_fields)
    D828['compute_cost'] = {
        'by_category': {k: dict(v, seconds=round(v['seconds'], 3), peak_gpu_gib=round(v['peak_gpu_gib'], 3))
                        for k, v in COST828.items()},
        'baseline_forward_passes': base_fwd, 'added_forward_passes': add_fwd,
        'added_over_baseline_forward_ratio': add_fwd / max(base_fwd, 1),
        'baseline_seconds': round(total828(base_keys, 'seconds'), 3),
        'added_seconds': round(total828(add_keys, 'seconds'), 3),
        'model_load_seconds': D828.get('model_load_seconds'),
        'runtime_seconds_total': D828.get('runtime_seconds_total'),
        'model_loads': 1, 'full_vocabulary_vectors_stored_on_disk': 0,
        'peak_gpu_gib_overall': round(max([v['peak_gpu_gib'] for v in COST828.values()] or [0.0]), 3),
        'gpu': (_torch828.cuda.get_device_name(0) if _torch828.cuda.is_available() else None)}

    engine_bindings828('AFTER_OFFLINE')
    D828['offline_scores'] = {
        policy: {arm: {
            'cases': sum(x['arm'] == arm and x['policy'] == policy for x in scored828),
            'exact_correct_legacy_827': sum(x['arm'] == arm and x['policy'] == policy and x['exact_correct'] for x in scored828),
            'prefix_aware_correct': sum(x['arm'] == arm and x['policy'] == policy and x['prefix_aware_correct'] for x in scored828),
            'final_classes': sorted(x['final_class'] for x in scored828 if x['arm'] == arm and x['policy'] == policy),
            'numerical_stability_stops': sum(r['arm'] == arm and r['policy'] == policy and r['numeric_stop_reason'] == 'RELATIVE_TENSOR_STABILITY' for r in D828['trials']),
            'safety_bound_stops': sum(r['arm'] == arm and r['policy'] == policy and r['safety_stop'] == 'MAX_STEPS_SAFETY_BOUND' for r in D828['trials']),
            'mean_reads': round(sum(r['steps_executed'] for r in D828['trials'] if r['arm'] == arm and r['policy'] == policy) / len(questions828), 3)
        } for arm in ARMS828} for policy in POLICIES828}

    with REVIEW828.open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['source', 'qid', 'arm_or_role', 'text', 'mechanical_class', 'expected',
                'human_reasoning_correct_0_1', 'human_truncation_0_1', 'human_notes']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in scored828:
            writer.writerow({'source': 'TRIAL_FINAL_READOUT', 'qid': row['qid'], 'arm_or_role': row['arm'],
                             'text': row['final'], 'mechanical_class': row['final_class'], 'expected': row['expected']})
        for x in D828['offline_designed']:
            for role, c in x['roles'].items():
                if c['greedy_question_only'] is not None:
                    writer.writerow({'source': 'DESIGNED_QUESTION_ONLY_GREEDY', 'qid': x['qid'], 'arm_or_role': role,
                                     'text': c['greedy_question_only'], 'mechanical_class': c['greedy_class'],
                                     'expected': ''})
    D828['review_sha256'] = sha828(REVIEW828.read_bytes())
    D828['status'] = 'COMPLETE_DIAGNOSTIC_SHADOW_ONLY_HUMAN_REVIEW_PENDING'
    save828()
    log828('TEST828_VERDICT', json.dumps({k: D828['offline_verdict'][k] for k in
           ('answer', 'H1_designed_worlds_separated', 'H1_worlds_total', 'H1_holds_with_returned_bf16_logits',
            'separation_margins', 'H2', 'H2_runtime_r2_complete', 'H2_runtime_r2_truncated',
            'answer_level_truncation_reproduced_worlds', 'order_noise_classification', 'replay_bitwise_all',
            'six_world_extension')}))
    log828('TEST828_DESIGNED_OFFLINE', json.dumps([{k: x[k] for k in ('qid', 'evidence_effect_FIRST_vs_BOTH_jsd', 'max_control_jsd',
            'separation_margin', 'answer_level_truncation_FIRST_middle_BOTH_end', 'end_and_middle_share_first_token')}
            for x in D828['offline_designed']]))
    log828('TEST828_SCORES', json.dumps(D828['offline_scores']))
    log828('TEST828_STOP_RULE', json.dumps({k: D828['stop_rule_verification'][k] for k in
           ('fires_n2', 'fires_n3', 'checked_len_changes_with_MAX_STEPS_4', 'modified_in_TEST828')}))
    log828('TEST828_COST', json.dumps({k: D828['compute_cost'][k] for k in
           ('baseline_forward_passes', 'added_forward_passes', 'added_over_baseline_forward_ratio',
            'baseline_seconds', 'added_seconds', 'peak_gpu_gib_overall', 'runtime_seconds_total')}))
    log828('TEST828_COMPLETED', OUT828, OFFLINE828, REVIEW828)
except BaseException as e:
    D828['status'] = 'ERROR'
    D828['error'] = {'repr': repr(e), 'traceback': traceback.format_exc()}
    save828()
    log828('TEST828_FAILED', repr(e), traceback.format_exc())
    raise
finally:
    gc.collect()
    if 'release' in globals() and callable(globals()['release']):
        try:
            release()
        except Exception:
            pass
    save828()
