# AKBASCORE SILICON HIPPOCAMPUS — TEST829
# AUTONOMOUS NUMERICAL DETECTION OF INCOMPLETE TWO-HOP SUPPORT (SHADOW MODE, SMALL PILOT).
# Built on the GPU-completed TEST828 code (828.py, git blob 45531c87...) which itself preserves the TEST827
# skeleton and the locked TEST815 engine. Single Colab cell; frozen Qwen2.5-72B NF4; exactly one A100 80GB.
# No residual hooks, no source replay at read time, no training, no textual control, no prompt-based decision.
# TEST829 question: WITHOUT being told which cartridges are the correct links, can the system decide from its
# own numerical counterfactual observations whether its current conclusion rests on a single source
# (incomplete two-hop support) or on composite support?
# Runtime sees only: opaque cartridge IDs, the sets the unchanged controller itself selected, and numbers
# produced by the frozen model's single full-depth forward per mounted set. Correct link IDs, the answer key,
# evidence roles/order and the FULL/REMOVE_SECOND/ADD_IRRELEVANT labels never enter the shadow computation.
# The TEST827 controller and its stopping rule run UNCHANGED (rule compiled from locked 827.py); nothing
# computed here chooses, rejects, fuses or stops. All generated text is produced only at the END of the run
# and used only offline. No GPU execution or result is claimed by the code author.
import ast, hashlib, urllib.request, json, csv, gc, time, traceback, random, re, datetime, contextlib, io, math, types
from pathlib import Path

T829 = '829'
SOURCE828_BLOB829 = '45531c87674a9e737a9081d3af41ca3f545431de'   # provenance: GPU-completed TEST828 code
REPO829 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCK815_829 = '77774f87428c0243c9a86ea6a041364acd9c1b03'
LOCK827_829 = '567822d34781ce966e0d5030a101d950d66156e8'   # GPU-completed TEST827 skeleton
SEED829 = 8292026                # fresh sealed panel (TEST828 used 8282026)
WORLDS829 = 3                    # small pilot (directive); no automatic extension
PARAPHRASES829 = 1
MAX_STEPS829 = 4                 # safety ceiling, NOT evidence of autonomous stopping (unchanged)
MAX_NEW_ANSWER829 = 96
MAX_NEW_CONTROL829 = 0           # no control text generated
MAX_CANDIDATES829 = 5
TOPK_STORE829 = 8                # small offline-inspection summary; JSD uses the FULL vocabulary
LM_CHUNK829 = 8192               # lm_head rows per float64 chunk (8192 x 8192 x 8 B = 512 MiB transient)
RUN829 = 'TEST829_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
DIR829 = (Path('/content') if Path('/content').exists() else Path('/tmp')) / RUN829
DIR829.mkdir(parents=True, exist_ok=False)
OUT829 = DIR829 / 'TEST829_results.json'
LOG829 = DIR829 / 'TEST829.log'
REVIEW829 = DIR829 / 'TEST829_blind_review.csv'
OFFLINE829 = DIR829 / 'TEST829_offline_key.json'  # never available to inference/controller/shadow

D829 = {'test': T829, 'status': 'STARTED', 'run': RUN829,
        'source815_blob': LOCK815_829, 'source827_blob': LOCK827_829, 'source828_blob': SOURCE828_BLOB829,
        'controller': 'TEST827_RETAINED_SIGNED_UNCHANGED_PLUS_STEPWISE_COUNTERFACTUAL_SHADOW',
        'checks': [], 'trials': [],
        'limitations': [
            'TEST829 is a small diagnostic pilot, NOT a claim of autonomous stopping; the shadow never acts.',
            'The TEST827 controller and stopping rule are executed unchanged; the stopping condition is compiled from the locked TEST827 source.',
            'Runtime counterfactuals are leave-one-out removals over sets the controller itself selected, identified by opaque IDs only.',
            'The support classification (single-source vs composite) is computed by a parameter-free largest-log-gap rule; no tuned threshold.',
            'Mapping "a two-hop query needs composite support" is a declared structural assumption used ONLY in offline evaluation; the runtime does not parse the question.',
            'Primary readout (predeclared): final-norm hidden state at the final question position. Next-token JSD and CUT3 state are secondary.',
            'TEST828 already showed that the next-token distribution moves almost as much for irrelevant additions as for the second link (margins 1.003-1.008).',
            'Question encoding (question text only) and the end-of-run answer readout are boundary interfaces; no generated text enters any runtime computation.',
            'Leave-one-out effects do not prove logical necessity; a composite dependency structure does not prove a correct chain.',
            'Synthetic two-hop relations test a narrow capability, not general scientific reasoning.',
            'Three-world pilot: any separation is descriptive, not statistically established.',
            'No GPU execution or result is claimed by the code author.']}

def sha829(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()

def blob829(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def save829():
    p = Path(str(OUT829) + '.tmp')
    p.write_text(json.dumps(D829, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    p.replace(OUT829)

QUIET829 = ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_',
            'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_',
            'NUM_', 'MEAS_', 'ENGINE_BINDINGS_', 'UNIQUE_ACTIVE_', 'DRA_SHADOW_FINITE_', 'FINITE_FEEDBACK_', 'FINITE_RANK_')

def log829(*args):
    msg = ' '.join(map(str, args))
    if not (msg.startswith('PASS ') and any(k in msg for k in QUIET829)):
        print(msg, flush=True)
        with LOG829.open('a', encoding='utf-8') as f:
            f.write(msg + '\n')

def gate829(name, ok, detail=None):
    D829['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail})
    if not (ok and any(k in name for k in QUIET829)):
        save829()
    log829('PASS' if ok else 'FAIL', name, detail if detail is not None else '')
    if not ok:
        save829()
        raise RuntimeError('TEST829_GATE_' + name)

# PRESEALED panel: opaque names and randomized assignments. All scoring stays offline.
# Same generator and card templates as TEST827; only the seed (fresh panel) and prefixes differ.
RNG829 = random.Random(SEED829)
ALPH829 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

def code829():
    return ''.join(RNG829.choice(ALPH829) for _ in range(9))

worlds829 = []
seen829 = set()
for wi in range(WORLDS829):
    names = []
    while len(names) < 5:
        n = code829()
        if n not in seen829:
            seen829.add(n); names.append(n)
    worlds829.append({'world': 'DOMAIN_' + code829(), 'start': names[0],
                      'middle': names[1], 'end': names[2],
                      'changed_end': names[3], 'decoy_end': names[4]})

questions829 = []
for w in worlds829:
    for pi, fmt in enumerate((
        'In domain {world}, starting from {start}, which endpoint is reached after exactly two directed links?',
        'For {world}, follow two successive directed edges beginning at {start}. Give the final node.')[:PARAPHRASES829]):
        questions829.append({'qid': w['world'] + '_P' + str(pi), 'world': w['world'],
                             'question': fmt.format(**w), 'expected': w['end'],
                             'changed_expected': w['changed_end']})

cards829, card_meta829 = {}, {}
for w in worlds829:
    domain = w['world']
    ids = {kind: 'E829_' + code829() for kind in ('first', 'second', 'changed', 'decoy')}
    w['ids'] = ids
    cards829[ids['first']] = ('Evidence record. Domain: ' + domain + '\n' +
                              'Directed relation: ' + w['start'] + ' -> ' + w['middle'] + '.\n')
    cards829[ids['second']] = ('Evidence record. Domain: ' + domain + '\n' +
                               'Directed relation: ' + w['middle'] + ' -> ' + w['end'] + '.\n')
    cards829[ids['changed']] = ('Evidence record. Domain: ' + domain + '\n' +
                                'Directed relation: ' + w['middle'] + ' -> ' + w['changed_end'] + '.\n')
    cards829[ids['decoy']] = ('Evidence record. Domain: ' + domain + '\n' +
                              'Directed relation: ' + w['decoy_end'] + ' -> ' + w['start'] + '.\n')
    for kind, cid in ids.items():
        card_meta829[cid] = {'domain': domain, 'kind': kind, 'body_sha256': sha829(cards829[cid])}
NULL829 = 'E829_NULL'
cards829[NULL829] = 'CONTROL MEMORY. No directed relations are available.\n'
card_meta829[NULL829] = {'domain': None, 'kind': 'null', 'body_sha256': sha829(cards829[NULL829])}
# Public panel hashes carry no kind/domain labels (those live only in the offline key).
card_hashes_public829 = {cid: m['body_sha256'] for cid, m in card_meta829.items()}

ARMS829 = ('FULL', 'REMOVE_SECOND', 'ADD_IRRELEVANT')
PANEL829 = {'seed': SEED829, 'world_count': WORLDS829, 'paraphrases': PARAPHRASES829,
            'questions': [{'qid': q['qid'], 'question': q['question']} for q in questions829],
            'arms': ARMS829, 'policies': ['RETAINED_SIGNED'],
            'limits': [MAX_STEPS829, MAX_NEW_ANSWER829, MAX_NEW_CONTROL829, MAX_CANDIDATES829,
                       TOPK_STORE829],
            'card_hashes': card_hashes_public829,
            'shadow_protocol': ['STEPWISE_LEAVE_ONE_OUT_ON_CONTROLLER_SETS_SIZE_GE_3',
                                'REUSE_PREVIOUS_STEP_AS_LOO_OF_LAST_ADDED_IF_DETERMINISTIC',
                                'ONE_DETERMINISM_CHECK', 'ONE_NONINTERFERENCE_CHECK',
                                'FINAL_ANSWER_READOUTS_AT_END_OF_RUN_OFFLINE_ONLY'],
            'support_rule': 'LARGEST_LOG_GAP_DEPENDENCY_COUNT_PARAMETER_FREE',
            'primary_readout': 'FINAL_NORM_HIDDEN_STATE_AT_FINAL_QUESTION_POSITION_COSINE_DISTANCE',
            'secondary_readouts': ['FULL_VOCAB_NEXT_TOKEN_JSD_FP64', 'CUT3_BLOCK3_STATE_COSINE_DISTANCE']}
PANEL_SHA829 = sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True))
D829['panel_sha256'] = PANEL_SHA829
D829['panel_public'] = PANEL829
OFFLINE829.write_text(json.dumps({'note': 'OFFLINE ONLY — NEVER IMPORT INTO CONTROLLER OR SHADOW',
                                  'questions': questions829, 'worlds': worlds829,
                                  'card_meta': card_meta829},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D829['offline_key_sha256'] = sha829(OFFLINE829.read_bytes())
save829()

def fetch_locked829(name, lock, limit=120000):
    req = urllib.request.Request(REPO829 + name, headers={'User-Agent': 'AKBASCORE-TEST829'})
    with urllib.request.urlopen(req, timeout=180) as f:
        raw = f.read(limit + 1)
    gate829('LOCK_' + name, len(raw) <= limit and blob829(raw) == lock, blob829(raw))
    return raw

# The engine is imported from the EXACT locked TEST815 AST prelude, unchanged.
# The original TEST815 experiment is never executed.
try:
    log829('TEST829_START', RUN829, 'PANEL_SHA', PANEL_SHA829)
    T0_829 = time.perf_counter()
    raw815_829 = fetch_locked829('815.py', LOCK815_829)
    tree815_829 = ast.parse(raw815_829.decode('utf-8'), filename='815.py')
    idx829 = [i for i, n in enumerate(tree815_829.body) if isinstance(n, ast.Try)]
    gate829('AST_BOUNDARY', len(idx829) == 1 and idx829[0] == len(tree815_829.body) - 1, idx829)
    exec(compile(ast.fix_missing_locations(ast.Module(body=tree815_829.body[:idx829[0]], type_ignores=[])),
                 'LOCKED_TEST815_PRELUDE', 'exec'), globals())
    gate829('LOCKED_ENGINE_SYMBOLS', all(callable(globals().get(x)) for x in
            ('model_setup', 'physical_commit', 'safe_load', 'build_fusion', 'free_generate',
             'memory_seals', 'compare_seals', 'sentinel', 'release', 'numeric_rank', 'observe_state',
             'prompt_ids', 'normalized', 'sha_file')))
    gate829('FRESH_BANK', len(entries) == 0, len(entries))
    # ENGINE BINDING PREFLIGHT. The locked engine resolves these names through this cell's globals at
    # call time; a TEST829 global with the same name would silently replace them (TEST829 run 1 failed
    # because a cell-level dict `pairs` replaced 709.py pairs()). Capture the locked objects now and
    # require object identity before every physical fusion and at the end.
    ENGINE_NAMES829 = ('pairs', 'cache_build', 'replace', 'half', 'rope', 'rephase', 'sentinel', 'free_gpu',
                       'ensure_room', 'kv_digest', 'full_kv_seal', 'answer', 'DirectCut3', 'forge_native',
                       'initialize_native', 'to_gpu', 'seal_cp', 'memory_seals', 'compare_seals', 'safe_load',
                       'release', 'native_append_direct', 'load_verified', 'build_fusion', 'normalized',
                       'query_native', 'numeric_rank', 'read_exact', 'model_setup', 'record_cp', 'physical_commit',
                       'observe_state', 'free_generate', 'prompt_ids', 'cache_build', 'Cut3Diagnostic',
                       'AttentionIntervention', 'aggregate_attention', 'sha_file', 'check', 'log')
    ENGINE_LOCKED829 = {k: globals().get(k) for k in ENGINE_NAMES829}
    _pairs829 = ENGINE_LOCKED829['pairs']
    gate829('ENGINE_BINDING_PREFLIGHT_PAIRS',
            callable(_pairs829) and getattr(_pairs829, '__name__', None) == 'pairs' and
            getattr(getattr(_pairs829, '__code__', None), 'co_filename', None) == '709.py',
            {'type': type(_pairs829).__name__, 'name': getattr(_pairs829, '__name__', None),
             'file': getattr(getattr(_pairs829, '__code__', None), 'co_filename', None)})
    gate829('ENGINE_BINDING_PREFLIGHT_ALL_CALLABLE',
            all(callable(v) for v in ENGINE_LOCKED829.values()),
            sorted(k for k, v in ENGINE_LOCKED829.items() if not callable(v)))
    D829['engine_bindings'] = {k: {'type': type(v).__name__,
                                   'file': getattr(getattr(v, '__code__', None), 'co_filename', None)}
                               for k, v in ENGINE_LOCKED829.items()}

    def engine_bindings829(tag):
        bad = sorted(k for k, v in ENGINE_LOCKED829.items() if globals().get(k) is not v)
        gate829('ENGINE_BINDINGS_' + tag, not bad, bad or None)

    import torch as _torch829
    SDPA829 = _torch829.nn.functional.scaled_dot_product_attention

    # ------------------------------------------------------------------------------------------
    # 1. STOPPING-RULE VERIFICATION AGAINST THE EXACT EXECUTABLE TEST827 CODE.
    # The condition is extracted from locked 827.py (run_trial827) and compiled VERBATIM into a
    # predicate. TEST829 calls this predicate at exactly the same place in the loop as TEST827.
    # ------------------------------------------------------------------------------------------
    raw827_829 = fetch_locked829('827.py', LOCK827_829)
    src827_829 = raw827_829.decode('utf-8')
    tree827_829 = ast.parse(src827_829, filename='827.py')
    fn827 = [n for n in ast.walk(tree827_829) if isinstance(n, ast.FunctionDef) and n.name == 'run_trial827']
    gate829('STOP827_FUNCTION', len(fn827) == 1, len(fn827))
    stop_nodes829 = [m for m in ast.walk(fn827[0]) if isinstance(m, ast.If) and
                     ast.unparse(m.test) == 'len(changes) >= 2']
    gate829('STOP827_NODE_UNIQUE', len(stop_nodes829) == 1, len(stop_nodes829))
    sn829 = stop_nodes829[0]
    inner829 = sn829.body[2] if len(sn829.body) == 3 else None
    gate829('STOP827_STRUCTURE',
            [type(b).__name__ for b in sn829.body] == ['Assign', 'Assign', 'If'] and
            [ast.unparse(t) for t in sn829.body[0].targets] == ['recent'] and
            [ast.unparse(t) for t in sn829.body[1].targets] == ['baseline'] and
            [type(b).__name__ for b in inner829.body] == ['Assign', 'Break'] and
            ast.unparse(inner829.body[0].value) == "'RELATIVE_TENSOR_STABILITY'",
            ast.get_source_segment(src827_829, sn829))
    # Predicate shell parsed from a template; its test expressions and assignments are the
    # locked TEST827 AST nodes themselves (only `break` becomes `return True`).
    _pred829 = ast.parse('def locked_stop827(changes, velocity):\n    if OUTER:\n        pass\n    return False\n').body[0]
    _pred829.body[0].test = sn829.test
    _pred829.body[0].body = [sn829.body[0], sn829.body[1],
                             ast.If(test=inner829.test, body=[ast.Return(value=ast.Constant(value=True))], orelse=[])]
    exec(compile(ast.fix_missing_locations(ast.Module(body=[_pred829], type_ignores=[])),
                 'LOCKED_TEST827_STOP_CONDITION', 'exec'), globals())

    def stop_audit829(changes, velocity):
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

    rng_stop829 = np.random.default_rng(SEED829)
    fires829 = {}
    for n_ in (2, 3):
        cnt = 0
        for _ in range(50000):
            ch = list(10.0 ** rng_stop829.uniform(-12.0, 2.0, size=n_))
            cnt += bool(locked_stop827(ch, np.zeros(4)))
        for _ in range(50000):
            ch = list(np.exp(rng_stop829.normal(0.0, 6.0, size=n_)))
            cnt += bool(locked_stop827(ch, np.zeros(4)))
        fires829[n_] = cnt
    checked_lengths829 = [s - 1 for s in range(1, MAX_STEPS829 + 1) if s - 1 >= 2]
    D829['stop_rule_verification'] = {
        'source': '827.py run_trial827, git blob ' + LOCK827_829,
        'condition_source': ast.get_source_segment(src827_829, sn829),
        'checked_len_changes_with_MAX_STEPS_4': checked_lengths829,
        'random_positive_trials_per_n': 100000, 'velocity_used': 'zero (most permissive)',
        'fires_n2': fires829[2], 'fires_n3': fires829[3],
        'degenerate_zero_displacements_n2_fires': bool(locked_stop827([0.0, 0.0], np.zeros(4))),
        'n4_counterexample_[1,1,0.01,0.01]_fires': bool(locked_stop827([1.0, 1.0, 0.01, 0.01], np.zeros(4))),
        'analytic': ('For n in {2,3}, max(changes[-2:]) >= median(changes) (n=2: max >= mean; n=3: any two of '
                     'three values include one >= the median). If median >= 1e-12 the condition requires '
                     'max(recent) < 0.1*median <= 0.1*max(recent), impossible. If median < 1e-12 it requires '
                     'max(recent) < 1e-13 and ||velocity|| < 1e-13, i.e. numerically identical unit states. With '
                     'MAX_STEPS=4 the rule is evaluated only at len(changes) in {2,3}; it is therefore unreachable '
                     'for non-degenerate trajectories. For n >= 4 it is reachable (e.g. [1,1,0.01,0.01]).'),
        'modified_in_TEST829': False}
    gate829('STOP_RULE_IMPOSSIBILITY_VERIFIED',
            fires829[2] == 0 and fires829[3] == 0 and checked_lengths829 == [2, 3] and
            D829['stop_rule_verification']['degenerate_zero_displacements_n2_fires'] and
            D829['stop_rule_verification']['n4_counterexample_[1,1,0.01,0.01]_fires'],
            {k: D829['stop_rule_verification'][k] for k in ('fires_n2', 'fires_n3', 'checked_len_changes_with_MAX_STEPS_4')})

    # Token budget is validated BEFORE loading 72B model weights.
    tok829 = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=False)
    tok_counts829 = {cid: len(tok829.encode(body, add_special_tokens=False)) for cid, body in cards829.items()}
    gate829('TOKEN_BUDGET', all(4 <= n <= 256 for n in tok_counts829.values()),
            {'max_body_tokens': max(tok_counts829.values()), 'stage': 'TOKENIZER_PRE_MODEL'})
    del tok829

    t_load829 = time.perf_counter()
    model_setup()
    D829['model_load_seconds'] = round(time.perf_counter() - t_load829, 3)
    before829 = sentinel()
    gate829('FROZEN_PREFIX', P == 30, P)
    gate829('FUSION_BUDGET',
            P + MAX_STEPS829 * max(tok_counts829.values()) + 64 <= MAX_FUSED_TOKENS,
            {'max_body_tokens': max(tok_counts829.values()), 'max_fused_tokens': MAX_FUSED_TOKENS})
    gate829('FUSION_BUDGET_FINAL_SET',
            P + (MAX_STEPS829 + 1) * max(tok_counts829.values()) + 64 <= MAX_FUSED_TOKENS,
            {'cartridges': MAX_STEPS829 + 1})
    engine_bindings829('BEFORE_PHYSICAL_COMMIT')
    for cid, body in cards829.items():
        physical_commit(cid, body)
        gate829('BODY_SHA_' + cid, entries[cid].get('body_sha256') == sha829(body))
    gate829('PHYSICAL_COUNT', len(entries) == len(cards829), len(entries))
    for cid in cards829:
        p = safe_load(entries[cid])
        gate829('RELOAD_' + cid, p['book_id'] == cid and int(p['n']) > P and
                len(p['lower']) == CUT + 1 and tuple(p['h'].shape)[-1] == H)
        del p
    release()

    # Locked numerical H3 bank (identical to TEST827).
    bank829 = {}
    for cid in sorted(entries):
        cp = safe_load(entries[cid])
        try:
            x = cp['h'][0, P:, :].float().cpu().numpy()
            gate829('H3_NONEMPTY_' + cid, x.ndim == 2 and x.shape[0] > 8 and x.shape[1] == H)
            ix = np.linspace(0, len(x) - 1, min(96, len(x)), dtype=np.int64)
            bank829[cid] = normalized(x[ix]).T.copy()
        finally:
            del cp
    gate829('H3_BANK', len(bank829) == len(entries), len(bank829))

    def eligible829(world, arm):
        """Experimenter intervention, never inferred from answer or given to controller (TEST827 verbatim)."""
        pool = []
        for w in worlds829:
            ids = w['ids']
            pool += [ids['first'], ids['second']]
            if arm == 'ADD_IRRELEVANT':
                pool.append(ids['decoy'])
        current = next(w for w in worlds829 if w['world'] == world)
        if arm == 'REMOVE_SECOND':
            pool.remove(current['ids']['second'])
        elif arm == 'REPLACE_SECOND':
            pool.remove(current['ids']['second'])
            pool.append(current['ids']['changed'])
        elif arm == 'NULL':
            return [NULL829]
        return pool

    # ------------------------------------------------------------------------------------------
    # COMPUTE ACCOUNTING. Full-model forward passes are counted at their call sites:
    # fusion (initialize_native/native_append_direct: one forward per CHUNK of a mounted cartridge),
    # probe (observe_state: one forward), generation (free_generate: one forward per generated token),
    # rank (numeric_rank -> query_native: one forward).
    # ------------------------------------------------------------------------------------------
    CHUNK829 = int(globals().get('CHUNK', 128))
    COST829 = {}

    def cost829(cat, seconds=0.0, fusion=0, probe=0, generation=0, rank=0, mounts=0, measures=0):
        c = COST829.setdefault(cat, {'seconds': 0.0, 'fusion_forwards': 0, 'probe_forwards': 0,
                                     'generation_forwards': 0, 'rank_forwards': 0,
                                     'cartridge_mounts': 0, 'measurements': 0, 'peak_gpu_gib': 0.0})
        c['seconds'] += float(seconds); c['fusion_forwards'] += int(fusion); c['probe_forwards'] += int(probe)
        c['generation_forwards'] += int(generation); c['rank_forwards'] += int(rank)
        c['cartridge_mounts'] += int(mounts); c['measurements'] += int(measures)
        try:
            c['peak_gpu_gib'] = max(c['peak_gpu_gib'], float(_torch829.cuda.max_memory_allocated()) / 2**30)
        except Exception:
            pass

    def fusion_forwards829(ids):
        n = 0
        for k, cid in enumerate(ids):
            tokens = int(entries[cid]['body_tokens']) + (P if k == 0 else 0)
            n += (tokens + CHUNK829 - 1) // CHUNK829
        return n

    def reset_peak829():
        try:
            _torch829.cuda.reset_peak_memory_stats()
        except Exception:
            pass

    def _native829_verbose(ids, prompt, tag, max_new):
        t0 = time.perf_counter()
        engine_bindings829(tag)
        mem, active, fusion_steps, _ = build_fusion(ids, 'TEST829_' + tag, True)
        try:
            gate829('NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
            n = int(mem[0][0].shape[-2])
            expected = P + sum(int(entries[x]['body_tokens']) for x in ids)
            gate829('NATIVE_LENGTH_' + tag, n == expected, {'n': n, 'expected': expected})
            first = int(entries[ids[0]]['body_tokens'])
            spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                    {'B0': (P, n), 'B1': (n, n)}
            seals = memory_seals(mem)
            out = free_generate(mem, prompt, seed=None, gain=0., max_new=max_new, spans=spans)
            gate829('KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
            gate829('SDPA_RESTORED_' + tag,
                    _torch829.nn.functional.scaled_dot_product_attention is SDPA829)
            return {'raw': out['raw'], 'tokens': int(out['generated_tokens']),
                    'possibly_truncated': int(out['generated_tokens']) >= max_new,
                    'ids': list(ids), 'time_seconds': round(time.perf_counter() - t0, 3),
                    'fusion_steps': fusion_steps,
                    'cartridge_shas': [entries[x]['sha256'] for x in ids]}
        finally:
            del mem
            gc.collect()
            release()

    def native829(ids, prompt, tag, max_new):
        capture = io.StringIO()
        reset_peak829(); t0 = time.perf_counter()
        try:
            with contextlib.redirect_stdout(capture):
                result = _native829_verbose(ids, prompt, tag, max_new)
            cost829('END_OF_RUN_FINAL_READOUT', time.perf_counter() - t0, fusion=fusion_forwards829(ids),
                    generation=result['tokens'], mounts=len(ids))
            return result
        except BaseException:
            log829('NATIVE_FAILURE_DIAGNOSTICS', tag, capture.getvalue()[-12000:])
            raise

    def answer_prompt829(question):
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
    gate829('NUMERICAL_PROBE_SYMBOL', callable(globals().get('observe_state')))
    head829 = model.lm_head
    import inspect as _inspect829
    try:
        _fwd_src829 = _inspect829.getsource(type(model).forward)
    except Exception as _e:
        _fwd_src829 = ''
    try:
        _sig829 = str(_inspect829.signature(type(model).forward))
    except Exception:
        _sig829 = ''
    W829 = getattr(head829, 'weight', None)
    is4bit829 = False
    try:
        is4bit829 = isinstance(head829, bitsandbytes.nn.Linear4bit)
    except Exception:
        pass
    FP64_MODE829 = (W829 is not None and not is4bit829 and
                    str(W829.dtype) in ('torch.bfloat16', 'torch.float16', 'torch.float32') and
                    tuple(W829.shape) == (int(model.config.vocab_size), H))
    VOCAB829 = int(model.config.vocab_size)
    NTOK829 = int(len(tok))
    D829['readout_semantics'] = {
        'transformers_version': getattr(globals().get('transformers'), '__version__', None),
        'torch_version': getattr(_torch829, '__version__', None),
        'model_class': type(model).__name__, 'lm_head_class': type(head829).__name__,
        'lm_head_weight_dtype': str(getattr(W829, 'dtype', None)),
        'lm_head_weight_shape': list(getattr(W829, 'shape', [])),
        'lm_head_has_bias': getattr(head829, 'bias', None) is not None,
        'lm_head_is_linear4bit': is4bit829,
        'config_vocab_size': VOCAB829, 'tokenizer_length': NTOK829,
        'padded_vocab_rows': VOCAB829 - NTOK829,
        'tie_word_embeddings': bool(getattr(model.config, 'tie_word_embeddings', False)),
        'final_logit_softcapping': getattr(model.config, 'final_logit_softcapping', None),
        'forward_signature': _sig829,
        'forward_source_has_logits_to_keep': 'logits_to_keep' in _fwd_src829,
        'forward_source_calls_lm_head': 'lm_head(' in _fwd_src829,
        'forward_source_contains_float_call': '.float()' in _fwd_src829,
        'precision_mode': 'FP64_RECOMPUTED_FROM_CAPTURED_FINAL_HIDDEN' if FP64_MODE829 else 'RETURNED_BF16_LOGITS_ONLY',
        'generation_interface': ('free_generate takes argmax of out.logits[0,-1] of the SAME forward; no '
                                 'temperature, top-k/top-p, repetition penalty or logits processor is applied'),
        'question_encoding': 'prompt_ids(question): question text only, no instruction (same as observe_state)'}
    HEAD_FWD829 = head829.__dict__.get('forward')   # original instance-level forward, if any
    gate829('READOUT_HEAD_NO_HOOKS', not head829._forward_hooks and not head829._forward_pre_hooks)
    gate829('READOUT_HEAD_SHAPE', W829 is not None and tuple(W829.shape)[-1] == H, list(getattr(W829, 'shape', [])))
    log829('TEST829_READOUT_SEMANTICS', json.dumps(D829['readout_semantics']))

    class Readout829:
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

    LN2_829 = math.log(2.0)

    def jsd829(lp, lq):
        # Exact Jensen-Shannon divergence (nats) over the FULL vocabulary, float64, log-space mixture.
        m = _torch829.logaddexp(lp, lq) - LN2_829
        p = _torch829.exp(lp); q = _torch829.exp(lq)
        zero = _torch829.zeros_like(p)
        a = _torch829.where(p > 0, p * (lp - m), zero).sum()
        b = _torch829.where(q > 0, q * (lq - m), zero).sum()
        v = float((0.5 * (a + b)).item())
        return min(max(v, 0.0), LN2_829)

    def tv829(lp, lq):
        return float((0.5 * (_torch829.exp(lp) - _torch829.exp(lq)).abs().sum()).item())

    def top1_829(lp):
        return int(lp.argmax().item())

    def full_readout829(h, z):
        zb = z.reshape(-1)
        lp16 = _torch829.log_softmax(zb.double(), dim=-1)
        summary = {}
        if FP64_MODE829:
            h64 = h.reshape(-1).double()
            parts = []
            for i in range(0, VOCAB829, LM_CHUNK829):
                parts.append(_torch829.matmul(W829[i:i + LM_CHUNK829].double(), h64))
            logits64 = _torch829.cat(parts)
            if getattr(head829, 'bias', None) is not None:
                logits64 = logits64 + head829.bias.double()
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
            lp64 = _torch829.log_softmax(logits64, dim=-1)
            del logits64, diff, a, b, zd
        else:
            lp64 = lp16
        top = _torch829.topk(lp64, TOPK_STORE829)
        summary.update({
            'entropy_nats': float((-(_torch829.exp(lp64) * lp64)).sum().item()),
            'top_ids': [int(x) for x in top.indices.cpu().tolist()],
            'top_probs': [float(math.exp(x)) for x in top.values.cpu().tolist()],
            'argmax_bf16': int(zb.argmax().item()), 'argmax_fp64': top1_829(lp64),
            'padded_vocab_mass': (float(_torch829.exp(lp64[NTOK829:]).sum().item()) if VOCAB829 > NTOK829 else 0.0),
            'precision_jsd_fp64_vs_returned_bf16': jsd829(lp64, lp16),
            'logits_bf16_sha256': sha829(zb.float().cpu().numpy().tobytes()),
            'final_hidden_sha256': sha829(h.reshape(-1).float().cpu().numpy().tobytes())})
        return lp64, lp16, summary

    def measure829(ids, question, tag, category, gen_max=0):
        """Mount ids natively, run the locked observe_state once (wrapped readout), optionally run an
        offline-only greedy continuation in the SAME mounted memory. Returns numbers; text is offline-only."""
        capture = io.StringIO()
        reset_peak829(); t0 = time.perf_counter()
        try:
            with contextlib.redirect_stdout(capture):
                engine_bindings829(tag)
                mem, active, _, _ = build_fusion(ids, 'TEST829_MEAS_' + tag, True)
                try:
                    gate829('MEAS_NATIVE80_' + tag, len(mem) == NL and list(active) == list(ids))
                    n = int(mem[0][0].shape[-2])
                    gate829('MEAS_NATIVE_LENGTH_' + tag,
                            n == P + sum(int(entries[x]['body_tokens']) for x in ids))
                    first = int(entries[ids[0]]['body_tokens'])
                    spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                            {'B0': (P, n), 'B1': (n, n)}
                    seals = memory_seals(mem)
                    nq = len(prompt_ids(question))
                    with Readout829() as ro:
                        state, att = observe_state(mem, question, spans)
                    gate829('MEAS_HEAD_RESTORED_' + tag, model.lm_head.__dict__.get('forward') is HEAD_FWD829)
                    gate829('MEAS_READOUT_SEMANTICS_' + tag,
                            ro.calls == 1 and ro.out_shape is not None and ro.out_shape[0] == 1 and
                            ro.out_shape[-1] == VOCAB829 and ro.in_shape[-1] == H and
                            ro.out_shape[1] in (1, nq) and ro.in_shape[1] == ro.out_shape[1],
                            {'calls': ro.calls, 'in': ro.in_shape, 'out': ro.out_shape, 'nq': nq})
                    gate829('MEAS_STATE_' + tag, state.numel() == H and
                            bool(_torch829.isfinite(state).all().item()))
                    gate829('MEAS_FINITE_LOGITS_' + tag, bool(_torch829.isfinite(ro.z).all().item()))
                    lp64, lp16, summary = full_readout829(ro.h, ro.z)
                    if FP64_MODE829:
                        gate829('MEAS_LOGIT_RECONSTRUCTION_' + tag, summary['reconstruction_correlation'] >= 0.9999,
                                {k: summary[k] for k in summary if k.startswith('reconstruction')})
                    summary.update({'logits_rows_returned': ro.out_shape[1], 'question_tokens': nq,
                                    'logits_dtype': ro.out_dtype, 'ids': list(ids), 'memory_tokens': n})
                    gen = None
                    if gen_max:
                        out = free_generate(mem, question, seed=None, gain=0., max_new=gen_max, spans=spans)
                        gen = {'raw': out['raw'], 'tokens': int(out['generated_tokens']),
                               'possibly_truncated': int(out['generated_tokens']) >= gen_max}
                    gate829('MEAS_KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
                    gate829('MEAS_SDPA_' + tag,
                            _torch829.nn.functional.scaled_dot_product_attention is SDPA829)
                    vec = state.detach().float().cpu().numpy().copy()
                    hvec = ro.h.reshape(-1).double().cpu().numpy().copy()
                    summary['state_sha256'] = sha829(np.asarray(vec, dtype=np.float32).tobytes())
                    summary['state_norm'] = float(np.linalg.norm(vec))
                finally:
                    del mem
                    gc.collect()
                    release()
            elapsed = time.perf_counter() - t0
            cost829(category, elapsed, fusion=fusion_forwards829(ids), probe=1, mounts=len(ids), measures=1)
            summary['seconds'] = round(elapsed, 3)
            return {'state': vec, 'h': hvec, 'att': att, 'lp': lp64, 'lp16': lp16, 'summary': summary,
                    'offline_generation': gen}
        except BaseException:
            log829('MEASUREMENT_FAILURE', tag, capture.getvalue()[-6000:])
            raise

    def unit829(x):
        y = np.asarray(x, dtype=np.float64).reshape(-1)
        norm = float(np.linalg.norm(y))
        if not np.isfinite(norm) or norm <= 1e-12:
            raise RuntimeError('NUMERIC_NONFINITE_OR_ZERO_STATE')
        return y / norm

    def cosdist829(a, b):
        return float(1.0 - np.dot(unit829(a), unit829(b)))

    def pair829(a, b):
        # Label-free numerical distances between two measurements of the SAME question, three readouts.
        return {'hidden': cosdist829(a['h'], b['h']),                 # PRIMARY (predeclared)
                'jsd': jsd829(a['lp'], b['lp']),                     # secondary: full-vocabulary next token
                'cut3': cosdist829(a['state'], b['state']),          # secondary: block-3 state
                'top1_same': top1_829(a['lp']) == top1_829(b['lp'])}

    READOUTS829 = ('hidden', 'jsd', 'cut3')

    def support_rule829(effects):
        """Parameter-free dependency count: sort leave-one-out effects descending and cut at the largest
        log-ratio gap between consecutive values. Ties -> smaller count (conservative). Needs n >= 3."""
        n = len(effects)
        if n < 3:
            return {'n': n, 'class': 'UNDETERMINED_LT3', 'dependency_count': None}
        v = sorted((max(float(e), 1e-300) for e in effects), reverse=True)
        gaps = [math.log(v[j]) - math.log(v[j + 1]) for j in range(n - 1)]
        m = 1 + max(range(n - 1), key=lambda j: (gaps[j], -j))
        return {'n': n, 'class': 'COMPOSITE' if m >= 2 else 'SINGLE_SOURCE', 'dependency_count': m,
                'sorted_effects': v, 'log_gaps': gaps,
                'r2_second_over_first': v[1] / v[0] if v[0] > 0 else None}

    # ------------------------------------------------------------------------------------------
    # NON-INTERFERENCE CHECK (once, label-free): the wrapped readout must leave the CUT3 state and
    # attention measurements bit-identical, and the captured argmax must equal the first greedy
    # token produced by the unchanged free_generate on the same mounted memory.
    # ------------------------------------------------------------------------------------------
    def noninterference829(ids, question):
        capture = io.StringIO(); reset_peak829(); t0 = time.perf_counter()
        with contextlib.redirect_stdout(capture):
            engine_bindings829('NONINTERFERENCE')
            mem, active, _, _ = build_fusion(ids, 'TEST829_NONINTERFERENCE', True)
            try:
                n = int(mem[0][0].shape[-2]); first = int(entries[ids[0]]['body_tokens'])
                spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else {'B0': (P, n), 'B1': (n, n)}
                seals = memory_seals(mem)
                s_plain, a_plain = observe_state(mem, question, spans)
                with Readout829() as ro:
                    s_wrapped, a_wrapped = observe_state(mem, question, spans)
                s_again, a_again = observe_state(mem, question, spans)
                g1 = free_generate(mem, question, seed=None, gain=0., max_new=1, spans=spans)
                tok_dec = tok.decode([int(ro.z.argmax().item())], skip_special_tokens=True).strip()
                res = {'state_bitwise_plain_vs_wrapped': bool(_torch829.equal(s_plain, s_wrapped)),
                       'state_bitwise_plain_vs_after': bool(_torch829.equal(s_plain, s_again)),
                       'attention_equal_plain_vs_wrapped': a_plain == a_wrapped,
                       'attention_equal_plain_vs_after': a_plain == a_again,
                       'first_greedy_token_equals_captured_argmax': g1['raw'] == tok_dec,
                       'head_restored': model.lm_head.__dict__.get('forward') is HEAD_FWD829,
                       'kv_sealed': compare_seals(seals, memory_seals(mem)),
                       'sdpa_restored': _torch829.nn.functional.scaled_dot_product_attention is SDPA829}
            finally:
                del mem; gc.collect(); release()
        cost829('NONINTERFERENCE_CHECK', time.perf_counter() - t0, fusion=fusion_forwards829(ids), probe=3,
                generation=1, mounts=len(ids))
        return res

    POLICIES829 = ('RETAINED_SIGNED',)
    REUSE829 = {'enabled': False}

    def shadow829(step_sets, step_meas, q, tag):
        """Step-wise leave-one-out over the controller's OWN sets (opaque IDs). For a set S_t (size >= 3) every
        member is removed once, order otherwise preserved. Removing the last-added member gives exactly the
        previous step set S_(t-1), already measured by the trajectory; it is reused only when bitwise
        determinism was verified at run start. Returns numbers only; never influences anything."""
        out = []
        for t, (S, mS) in enumerate(zip(step_sets, step_meas)):
            row = {'step': t, 'S': list(S), 'n': len(S)}
            if len(S) >= 3:
                loo = []
                for k_, cid in enumerate(S):
                    rest = [c for c in S if c != cid]
                    reused = (REUSE829['enabled'] and k_ == len(S) - 1 and t >= 1 and rest == list(step_sets[t - 1]))
                    if reused:
                        mr = step_meas[t - 1]
                    else:
                        mr = measure829(rest, q['question'], tag + '_SH_S' + str(t) + '_LOO' + str(k_),
                                        'SHADOW_STEPWISE_LOO')
                    loo.append(dict(pair829(mS, mr), removed=cid, position=k_, reused_previous_step=reused))
                    if not reused:
                        mr['lp'] = None; mr['lp16'] = None
                row['leave_one_out'] = loo
                row['support'] = {r_: support_rule829([x[r_] for x in loo]) for r_ in READOUTS829}
            else:
                row['support'] = {r_: support_rule829([]) for r_ in READOUTS829}
            out.append(row)
        return out

    def run_trial829(q, arm, policy):
        # TEST827 RETAINED_SIGNED controller, unchanged (as in TEST828). Strictly blinded: no source-kind, truth
        # labels or answer text enters the controller. Additions are read-only: per-step measurements are kept
        # for the shadow, the stop rule is audited, and the shadow runs only after the trajectory has ended.
        allowed = eligible829(q['world'], arm)
        t_rank = time.perf_counter()
        ranked, scores = numeric_rank(q['question'], {cid: bank829[cid] for cid in allowed})
        cost829('BASELINE_TRAJECTORY', time.perf_counter() - t_rank, rank=1)
        tag = q['qid'] + '_' + arm + '_' + policy
        gate829('RANK_' + tag, len(ranked) == len(allowed) and set(ranked) == set(allowed))
        first = ranked[0]
        selected = [first]
        m0 = measure829(selected, q['question'], tag + '_INITIAL', 'BASELINE_TRAJECTORY')
        initial_state = m0['state']
        reference = unit829(initial_state)
        previous = reference.copy()
        vals = np.array([float(scores[c]) for c in ranked], dtype=np.float64)
        gate829('FINITE_RANK_' + tag, bool(np.isfinite(vals).all()))
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
                  'state_sha256': sha829(np.asarray(initial_state, dtype=np.float32).tobytes())}]
        step_sets, step_meas = [selected[:]], [m0]      # shadow-only record of the controller's own sets
        readout_traj = [{'step': 0, 'ids_count': 1, 'jsd_to_previous': None, 'hidden_dist_to_previous': None,
                         'entropy_nats': m0['summary']['entropy_nats'],
                         'top_ids': m0['summary']['top_ids'], 'top_probs': m0['summary']['top_probs']}]
        m_prev = m0
        stop_audit = []
        stop_reason = None
        safety_stop = None
        for step in range(1, MAX_STEPS829 + 1):
            candidates = [c for c in ranked if c not in selected]
            if not candidates:
                stop_reason = 'CANDIDATE_EXHAUSTION'
                break
            utilities = {}
            for cid in candidates:
                matrix = np.asarray(bank829[cid], dtype=np.float64)
                colnorm = np.maximum(np.linalg.norm(matrix, axis=0), 1e-12)
                sims = (previous @ matrix) / colnorm
                signed = float(np.quantile(sims, 0.75))
                rank_z = (float(scores[cid]) - float(np.mean(vals))) / spread
                derivative = float(np.dot(velocity, unit829(np.mean(matrix, axis=1)))) if np.linalg.norm(velocity) > 1e-12 else 0.0
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
            stop_audit.append(dict(stop_audit829(changes, velocity), step=step))
            if locked_stop827(changes, velocity):
                stop_reason = 'RELATIVE_TENSOR_STABILITY'
                break
            next_ids = selected + [target]
            gate829('UNIQUE_ACTIVE_' + tag + '_' + str(step), len(set(next_ids)) == len(next_ids))
            m_new = measure829(next_ids, q['question'], tag + '_STEP_' + str(step), 'BASELINE_TRAJECTORY')
            new_state, att = m_new['state'], m_new['att']
            current = unit829(new_state)
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
            gate829('DRA_SHADOW_FINITE_' + tag + '_' + str(step),
                    bool(np.isfinite(osc_energy) and np.isfinite(osc_speed) and np.isfinite(osc_error)))
            delta = current - previous
            displacement = float(np.linalg.norm(delta))
            velocity = 0.30 * velocity + 0.70 * delta
            signed_change = float(np.dot(previous, current))
            alignment_history.append(signed_change)
            changes.append(displacement)
            gate829('FINITE_FEEDBACK_' + tag + '_' + str(step),
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
                          'state_sha256': sha829(np.asarray(new_state, dtype=np.float32).tobytes())})
            # Read-only full-depth readout trajectory (same forward as the CUT3 probe; zero extra passes).
            readout_traj.append({'step': step, 'ids_count': len(next_ids),
                                 'jsd_to_previous': jsd829(m_prev['lp'], m_new['lp']),
                                 'hidden_dist_to_previous': cosdist829(m_prev['h'], m_new['h']),
                                 'tv_to_previous': tv829(m_prev['lp'], m_new['lp']),
                                 'top1_changed': top1_829(m_prev['lp']) != top1_829(m_new['lp']),
                                 'entropy_nats': m_new['summary']['entropy_nats'],
                                 'top_ids': m_new['summary']['top_ids'], 'top_probs': m_new['summary']['top_probs'],
                                 'cut3_state_change': displacement})
            m_prev = m_new
            step_sets.append(next_ids[:]); step_meas.append(m_new)
            selected = next_ids
            previous = current
        if stop_reason is None:
            safety_stop = 'MAX_STEPS_SAFETY_BOUND'
        initial = {'raw': '[SKIPPED_DIAGNOSTIC_READOUT]'}
        # SHADOW: step-wise counterfactual support analysis; runs after all control actions are complete.
        shadow = shadow829(step_sets, step_meas, q, tag)
        for mm in step_meas:
            mm['lp'] = None; mm['lp16'] = None
        return {'qid': q['qid'], 'arm': arm, 'policy': policy, 'question': q['question'],
                'initial': initial['raw'].strip(), 'final': None, 'final_tokens': None,
                'final_possibly_truncated': None, 'final_selected': selected[:],
                'initial_selected': [first], 'ranked_ids': ranked,
                'ranked_scores': {cid: float(scores[cid]) for cid in ranked},
                'trace': trace, 'model_decisions': decisions, 'validity_gate_audit': rejected,
                'causal_ablations': [], 'dra_shadow': osc_history,
                'stop_rule_audit': stop_audit, 'shadow_readout_trajectory': readout_traj,
                'stepwise_support_shadow': shadow,
                'model_stop': False, 'numerical_stop': stop_reason in ('RELATIVE_TENSOR_STABILITY', 'NUMERIC_VALIDITY_ABSTENTION'),
                'numeric_stop_reason': stop_reason, 'safety_stop': safety_stop,
                'steps_executed': len(decisions), 'model_actions': ['NUMERIC_READ'] * len(decisions),
                'valid_decisions': len(decisions), 'first_valid_decisions': len(decisions),
                'repair_attempts': 0, 'repair_successes': 0,
                'controller_decisions': len(decisions)}

    # ------------------------------------------------------------------------------------------
    # RUN ORDER: integrity checks -> unchanged controller trajectories with step-wise shadow -> end-of-run
    # answer readouts (offline-only text) -> integrity gates -> offline evaluation.
    # ------------------------------------------------------------------------------------------
    qlookup829 = {q['qid']: q for q in questions829}   # qid -> question text (boundary input)
    D829['noninterference'] = noninterference829([NULL829], questions829[0]['question'])
    for k_, v_ in D829['noninterference'].items():
        gate829('NONINTERFERENCE_' + k_.upper(), bool(v_), v_)
    # One determinism check (TEST828 found 12/12 bitwise replays). Label-free set: first three opaque IDs.
    det_ids829 = [c for c in sorted(entries) if c != NULL829][:3]
    _da = measure829(det_ids829, questions829[0]['question'], 'DETERMINISM_A', 'DETERMINISM_CHECK')
    _db = measure829(det_ids829, questions829[0]['question'], 'DETERMINISM_B', 'DETERMINISM_CHECK')
    D829['determinism'] = {
        'ids_count': len(det_ids829),
        'logits_bitwise': _da['summary']['logits_bf16_sha256'] == _db['summary']['logits_bf16_sha256'],
        'final_hidden_bitwise': _da['summary']['final_hidden_sha256'] == _db['summary']['final_hidden_sha256'],
        'cut3_state_bitwise': _da['summary']['state_sha256'] == _db['summary']['state_sha256'],
        'distances': pair829(_da, _db)}
    REUSE829['enabled'] = bool(D829['determinism']['logits_bitwise'] and D829['determinism']['final_hidden_bitwise']
                               and D829['determinism']['cut3_state_bitwise'])
    D829['determinism']['reuse_previous_step_enabled'] = REUSE829['enabled']
    log829('TEST829_DETERMINISM', json.dumps(D829['determinism']))
    del _da, _db

    for q in questions829:
        for arm in ARMS829:
            for policy in POLICIES829:
                row = run_trial829(q, arm, policy)
                D829['trials'].append(row)
                save829()
                log829('TEST829_TRIAL', row['qid'], arm, policy, 'steps', row['steps_executed'],
                       'stop', row['numeric_stop_reason'] or row['safety_stop'],
                       'support_primary', [x['support']['hidden']['class'] for x in row['stepwise_support_shadow']],
                       'm', [x['support']['hidden']['dependency_count'] for x in row['stepwise_support_shadow']])

    # END-OF-RUN answer readouts: identical TEST827 boundary readout of each final set. Text is stored for
    # offline evaluation only; nothing after this point feeds any runtime computation.
    for row in D829['trials']:
        q = qlookup829[row['qid']]
        final = native829(row['final_selected'], answer_prompt829(q['question']),
                          row['qid'] + '_' + row['arm'] + '_' + row['policy'] + '_FINAL_READOUT', MAX_NEW_ANSWER829)
        row['final'] = final['raw'].strip(); row['final_tokens'] = final['tokens']
        row['final_possibly_truncated'] = final['possibly_truncated']
        log829('TEST829_FINAL_READOUT', row['qid'], row['arm'], repr(row['final'][:80]))
    save829()

    D829['fixed_baseline'] = []
    gate829('TRIAL_COUNT', len(D829['trials']) == len(questions829) * len(ARMS829) * len(POLICIES829),
            len(D829['trials']))
    engine_bindings829('FINAL')
    gate829('FROZEN_WEIGHT_SENTINEL', before829 == sentinel())
    gate829('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    gate829('LM_HEAD_UNWRAPPED', model.lm_head.__dict__.get('forward') is HEAD_FWD829 and
            not model.lm_head._forward_hooks and not model.lm_head._forward_pre_hooks)
    gate829('PANEL_UNCHANGED', sha829(json.dumps(PANEL829, ensure_ascii=False, sort_keys=True)) == PANEL_SHA829)
    for cid in cards829:
        gate829('FINAL_SHA_' + cid, sha_file(CART_DIR / entries[cid]['file']) == entries[cid]['sha256'])
    D829['runtime_seconds_total'] = round(time.perf_counter() - T0_829, 3)

    # ==========================================================================================
    # OFFLINE EVALUATION. Everything below runs after all model calls; labels are used here only.
    # ==========================================================================================
    lookup829 = {q['qid']: q for q in questions829}
    world_of829 = {w['world']: w for w in worlds829}
    kind829 = {cid: m['kind'] for cid, m in card_meta829.items()}
    dom829 = {cid: m['domain'] for cid, m in card_meta829.items()}

    def role_of829(cid, w):
        if cid == NULL829:
            return 'NULL'
        if dom829.get(cid) == w['world']:
            return 'OWN_' + kind829[cid].upper()
        return 'OTHER_' + kind829[cid].upper()

    def classify829(text, w):
        t = (text or '').strip(); u = t.upper()
        clean = u.strip(' .\n*`"\'')
        own = {'END': w['end'], 'MIDDLE': w['middle'], 'START': w['start'],
               'CHANGED_END': w['changed_end'], 'DECOY_END': w['decoy_end']}
        others = {c: 'OTHER_WORLD' for ow in worlds829 if ow is not w
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

    def status829(S, w):
        roles = [role_of829(x, w) for x in S]
        if 'OWN_FIRST' in roles and 'OWN_SECOND' in roles:
            return 'COMPLETE', roles
        if 'OWN_FIRST' in roles:
            return 'TRUNCATED', roles
        return 'NO_START_LINK', roles

    def auc829(pos, neg):
        # P(stat_complete > stat_insufficient), ties count 1/2; descriptive only.
        if not pos or not neg:
            return None
        return sum((a > b) + 0.5 * (a == b) for a in pos for b in neg) / (len(pos) * len(neg))

    # ---- per-step offline labelling (labels used ONLY here) ----
    D829['offline_steps'] = []
    for r in D829['trials']:
        w = world_of829[lookup829[r['qid']]['world']]
        for x in r['stepwise_support_shadow']:
            st, roles = status829(x['S'], w)
            rec = {'qid': r['qid'], 'arm': r['arm'], 'step': x['step'], 'n': x['n'], 'status': st, 'roles': roles,
                   'is_final_set': x['step'] == len(r['stepwise_support_shadow']) - 1}
            for r_ in READOUTS829:
                sup = x['support'][r_]
                rec[r_ + '_class'] = sup['class']; rec[r_ + '_m'] = sup['dependency_count']
                rec[r_ + '_r2'] = sup.get('r2_second_over_first')
                if x.get('leave_one_out'):
                    order = sorted(range(len(x['leave_one_out'])), key=lambda k: (-x['leave_one_out'][k][r_], k))
                    rec[r_ + '_loo_roles_by_magnitude'] = [role_of829(x['leave_one_out'][k]['removed'], w) for k in order]
                    rec[r_ + '_loo_by_role'] = {role_of829(y['removed'], w) + '@' + str(y['position']): y[r_]
                                                for y in x['leave_one_out']}
            D829['offline_steps'].append(rec)

    # ---- final answers (end-of-run text), prefix-aware scoring ----
    scored829 = []
    for r in D829['trials']:
        key = lookup829[r['qid']]; w = world_of829[key['world']]
        c = classify829(r['final'], w)
        should_unknown = r['arm'] in ('REMOVE_SECOND', 'NULL')
        prefix_ok = (c['class'] == 'UNKNOWN_PREFIX') if should_unknown else c['class'] in ('OWN_END_EXACT', 'OWN_END_LAST_MENTIONED')
        fin = [x for x in D829['offline_steps'] if x['qid'] == r['qid'] and x['arm'] == r['arm'] and x['is_final_set']][0]
        scored829.append({'qid': r['qid'], 'arm': r['arm'], 'policy': r['policy'],
                          'expected': 'UNKNOWN' if should_unknown else key['expected'],
                          'prefix_aware_correct': prefix_ok, 'final_class': c['class'], 'final': r['final'],
                          'final_set_status': fin['status'],
                          'final_set_support_primary': fin['hidden_class']})

    # ---- predeclared evaluation (written before any result exists) ----
    # Primary readout: 'hidden'. Evaluated steps: n >= 3. Insufficient = TRUNCATED or NO_START_LINK.
    # SAFETY      : no insufficient step is classified COMPOSITE (a composite-support stop would be wrongful).
    # SENSITIVITY : every COMPLETE step is classified COMPOSITE (otherwise the signal cannot license a stop).
    # NON-VACUITY : at least one COMPLETE and one TRUNCATED evaluated step.
    # Structural assumption, offline only: a two-hop query requires composite support.
    def evaluate829(r_):
        ev = [x for x in D829['offline_steps'] if x['n'] >= 3]
        insuff = [x for x in ev if x['status'] != 'COMPLETE']
        trunc = [x for x in ev if x['status'] == 'TRUNCATED']
        comp = [x for x in ev if x['status'] == 'COMPLETE']
        false_comp = [x for x in insuff if x[r_ + '_class'] == 'COMPOSITE']
        hit = [x for x in comp if x[r_ + '_class'] == 'COMPOSITE']
        pair_found = [x for x in hit if sorted(x[r_ + '_loo_roles_by_magnitude'][:2]) == ['OWN_FIRST', 'OWN_SECOND']]
        if not comp or not trunc:
            verdict = 'INCONCLUSIVE_VACUOUS_PILOT'
        elif false_comp:
            verdict = 'FAILURE_WRONGFUL_STOP_NOT_PREVENTED'
        elif len(hit) < len(comp):
            verdict = 'FAILURE_COMPOSITE_SUPPORT_NOT_DETECTED'
        else:
            verdict = 'SIGNAL_SUPPORTED_IN_PILOT'
        r2c = [x[r_ + '_r2'] for x in comp if x[r_ + '_r2'] is not None]
        r2i = [x[r_ + '_r2'] for x in insuff if x[r_ + '_r2'] is not None]
        return {'verdict': verdict, 'evaluated_steps': len(ev), 'complete_steps': len(comp),
                'truncated_steps': len(trunc), 'no_start_steps': len(insuff) - len(trunc),
                'false_composite_on_insufficient': len(false_comp),
                'false_composite_cases': [(x['qid'], x['arm'], x['step']) for x in false_comp],
                'composite_detected_on_complete': len(hit),
                'missed_complete_cases': [(x['qid'], x['arm'], x['step']) for x in comp if x not in hit],
                'top2_dependencies_equal_true_pair': len(pair_found),
                'r2_complete': r2c, 'r2_insufficient': r2i, 'r2_auc_complete_gt_insufficient': auc829(r2c, r2i),
                'dependency_count_complete': [x[r_ + '_m'] for x in comp],
                'dependency_count_insufficient': [x[r_ + '_m'] for x in insuff]}

    ev829 = {r_: evaluate829(r_) for r_ in READOUTS829}
    prim = ev829['hidden']
    trunc_final = [x for x in scored829 if x['final_set_status'] == 'TRUNCATED']
    comp_final = [x for x in scored829 if x['final_set_status'] == 'COMPLETE']
    D829['offline_verdict'] = {
        'question': ('Without the correct link IDs, can the system distinguish incomplete two-hop support from '
                     'complete support using only its own numerical counterfactual observations?'),
        'primary_readout': 'hidden', 'primary': prim, 'secondary': {k: ev829[k] for k in ('jsd', 'cut3')},
        'answer': prim['verdict'],
        'shadow_counterfactual_on_final_sets': {
            'truncated_final_sets': len(trunc_final),
            'truncated_final_wrong_answers': sum(not x['prefix_aware_correct'] for x in trunc_final),
            'truncated_final_wrong_answers_flagged_single_source': sum(
                (not x['prefix_aware_correct']) and x['final_set_support_primary'] != 'COMPOSITE' for x in trunc_final),
            'complete_final_sets': len(comp_final),
            'complete_final_correct_answers': sum(x['prefix_aware_correct'] for x in comp_final),
            'complete_final_correct_answers_licensed_composite': sum(
                x['prefix_aware_correct'] and x['final_set_support_primary'] == 'COMPOSITE' for x in comp_final)},
        'stopping': {'rule_modified': False,
                     'numerical_stability_stops': sum(r['numeric_stop_reason'] == 'RELATIVE_TENSOR_STABILITY' for r in D829['trials']),
                     'safety_bound_stops': sum(r['safety_stop'] == 'MAX_STEPS_SAFETY_BOUND' for r in D829['trials']),
                     'claim': 'NO_AUTONOMOUS_STOPPING_CLAIM_SHADOW_ONLY'},
        'caveats': ['The support rule is parameter-free; the requirement "two-hop needs composite support" is a declared assumption used offline only.',
                    'Steps within a trial are correlated (nested sets); counts are descriptive, not independent samples.',
                    'Secondary readouts are reported for transparency; the verdict uses only the predeclared primary readout.',
                    'A composite dependency structure does not prove a correct chain; single-source does not prove absence of evidence.',
                    'Three-world pilot; generalization beyond synthetic two-hop relations is not tested.']}

    # ---- compute cost (and the TEST828 -> TEST829 reduction plan) ----
    base_keys = ('BASELINE_TRAJECTORY', 'END_OF_RUN_FINAL_READOUT')
    add_keys = ('SHADOW_STEPWISE_LOO', 'DETERMINISM_CHECK', 'NONINTERFERENCE_CHECK')
    def total829(keys, field):
        return sum(COST829.get(k, {}).get(field, 0) for k in keys)
    fwd_fields = ('fusion_forwards', 'probe_forwards', 'generation_forwards', 'rank_forwards')
    base_fwd = sum(total829(base_keys, f) for f in fwd_fields)
    add_fwd = sum(total829(add_keys, f) for f in fwd_fields)
    predicted_shadow = 0
    for r in D829['trials']:
        for x in r['stepwise_support_shadow']:
            if x['n'] >= 3:
                fresh = [y for y in x['leave_one_out'] if not y['reused_previous_step']]
                predicted_shadow += len(fresh) * x['n']        # (n-1) fusion + 1 probe per fresh LOO set
    D829['compute_cost'] = {
        'by_category': {k: dict(v, seconds=round(v['seconds'], 3), peak_gpu_gib=round(v['peak_gpu_gib'], 3))
                        for k, v in COST829.items()},
        'baseline_forward_passes': base_fwd, 'added_forward_passes': add_fwd,
        'added_over_baseline_forward_ratio': add_fwd / max(base_fwd, 1),
        'shadow_forward_passes_counted': sum(total829(('SHADOW_STEPWISE_LOO',), f) for f in fwd_fields),
        'shadow_forward_passes_predicted_from_set_sizes': predicted_shadow,
        'baseline_seconds': round(total829(base_keys, 'seconds'), 3),
        'added_seconds': round(total829(add_keys, 'seconds'), 3),
        'model_load_seconds': D829.get('model_load_seconds'),
        'runtime_seconds_total': D829.get('runtime_seconds_total'),
        'model_loads': 1, 'full_vocabulary_vectors_stored_on_disk': 0,
        'peak_gpu_gib_overall': round(max([v['peak_gpu_gib'] for v in COST829.values()] or [0.0]), 3),
        'gpu': (_torch829.cuda.get_device_name(0) if _torch829.cuda.is_available() else None),
        'test828_added_forwards_reference': 1782,
        'test828_removed_components': {
            'designed_panel_probe_and_fusion': 81, 'designed_panel_offline_generation_approx': 1221,
            'order_reverse_rotate': 108, 'replay_x9': 54, 'null_references': 6,
            'keep_top1_keep_top2_drop_top2': 81, 'final_set_loo_replaced_by_stepwise_loo_with_reuse': 225}}

    engine_bindings829('AFTER_OFFLINE')
    D829['offline_scores'] = {arm: {
        'cases': sum(x['arm'] == arm for x in scored829),
        'prefix_aware_correct': sum(x['arm'] == arm and x['prefix_aware_correct'] for x in scored829),
        'final_classes': sorted(x['final_class'] for x in scored829 if x['arm'] == arm),
        'final_set_status': sorted(x['final_set_status'] for x in scored829 if x['arm'] == arm),
        'mean_reads': round(sum(r['steps_executed'] for r in D829['trials'] if r['arm'] == arm) / len(questions829), 3)}
        for arm in ARMS829}

    with REVIEW829.open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['source', 'qid', 'arm', 'step', 'text_or_roles', 'mechanical_class', 'expected_or_status',
                'support_primary', 'human_reasoning_correct_0_1', 'human_truncation_0_1', 'human_notes']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in scored829:
            writer.writerow({'source': 'END_OF_RUN_FINAL_READOUT', 'qid': row['qid'], 'arm': row['arm'], 'step': 'final',
                             'text_or_roles': row['final'], 'mechanical_class': row['final_class'],
                             'expected_or_status': row['expected'], 'support_primary': row['final_set_support_primary']})
        for x in D829['offline_steps']:
            writer.writerow({'source': 'STEP_SET', 'qid': x['qid'], 'arm': x['arm'], 'step': x['step'],
                             'text_or_roles': ' '.join(x['roles']), 'mechanical_class': '',
                             'expected_or_status': x['status'], 'support_primary': x['hidden_class']})
    D829['review_sha256'] = sha829(REVIEW829.read_bytes())
    D829['status'] = 'COMPLETE_DIAGNOSTIC_SHADOW_ONLY_HUMAN_REVIEW_PENDING'
    save829()
    log829('TEST829_VERDICT', json.dumps({'answer': D829['offline_verdict']['answer'],
           'primary': {k: prim[k] for k in prim if k not in ('r2_complete', 'r2_insufficient')},
           'secondary_verdicts': {k: ev829[k]['verdict'] for k in ('jsd', 'cut3')}}))
    log829('TEST829_FINAL_SETS', json.dumps(D829['offline_verdict']['shadow_counterfactual_on_final_sets']))
    log829('TEST829_SCORES', json.dumps(D829['offline_scores']))
    log829('TEST829_STOP_RULE', json.dumps({k: D829['stop_rule_verification'][k] for k in
           ('fires_n2', 'fires_n3', 'checked_len_changes_with_MAX_STEPS_4', 'modified_in_TEST829')}))
    log829('TEST829_COST', json.dumps({k: D829['compute_cost'][k] for k in
           ('baseline_forward_passes', 'added_forward_passes', 'added_over_baseline_forward_ratio',
            'shadow_forward_passes_counted', 'shadow_forward_passes_predicted_from_set_sizes',
            'baseline_seconds', 'added_seconds', 'peak_gpu_gib_overall', 'runtime_seconds_total')}))
    log829('TEST829_COMPLETED', OUT829, OFFLINE829, REVIEW829)
except BaseException as e:
    D829['status'] = 'ERROR'
    D829['error'] = {'repr': repr(e), 'traceback': traceback.format_exc()}
    save829()
    log829('TEST829_FAILED', repr(e), traceback.format_exc())
    raise
finally:
    gc.collect()
    if 'release' in globals() and callable(globals()['release']):
        try:
            release()
        except Exception:
            pass
    save829()
