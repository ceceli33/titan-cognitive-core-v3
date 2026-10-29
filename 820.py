# AKBASCORE SILICON HIPPOCAMPUS — TEST920
# TENSOR-NUMERICAL CONTROL: CUT3 H3 observations -> feedback -> physical cartridge action.
# Built from GPU-completed TEST919 and locked TEST815 engine; no textual action controller.
# Single Colab cell; frozen Qwen2.5-72B NF4; exactly one A100 80GB.
# LOCKED TEST815 engine; no residual hooks, no source replay at read time, no training.
# TEST920 REVISION: no natural-language controller, no action parser, no self-repair prompts.
# Numerical controller is EXPERIMENTAL; not the original DRA layer-injection motor.
# Question encoding and final answer readout remain language interfaces; control loop is numeric.
import ast, hashlib, urllib.request, json, csv, gc, time, traceback, random, re, datetime, contextlib, io
from pathlib import Path

T920 = '920'
REPO920 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCK815_920 = '77774f87428c0243c9a86ea6a041364acd9c1b03'
SEED920 = 9202026
WORLDS920 = 8
PARAPHRASES920 = 3
MAX_STEPS920 = 4                 # safety ceiling, NOT evidence of autonomous stopping
MAX_NEW_ANSWER920 = 96
MAX_NEW_CONTROL920 = 0  # no control text generated
MAX_CANDIDATES920 = 5
RUN920 = 'TEST920_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
DIR920 = (Path('/content') if Path('/content').exists() else Path('/tmp')) / RUN920
DIR920.mkdir(parents=True, exist_ok=False)
OUT920 = DIR920 / 'TEST920_results.json'
LOG920 = DIR920 / 'TEST920.log'
REVIEW920 = DIR920 / 'TEST920_blind_review.csv'
OFFLINE920 = DIR920 / 'TEST920_offline_key.json'  # never available to inference/controller

D920 = {'test': T920, 'status': 'STARTED', 'run': RUN920,
        'source815_blob': LOCK815_920, 'controller': 'NUMERIC_CUT3_H3_FEEDBACK', 'checks': [], 'trials': [],
        'limitations': [
            'Control decisions are computed from H3/CUT3 tensors and numerical feedback, without generated action text.',
            'The numerical feedback rule is a new experimental interface, NOT verified DRA 1.3 layer steering.',
            'Question tokenization and final readout remain linguistic boundary interfaces.',
            'Offline truth is never given to numeric_rank, free_generate, or controller.',
            'MAX_STEPS is a safety bound, not autonomous stopping.',
            'Native reads and integrity checks are distinct from semantic correctness.',
            'Synthetic two-hop relations test a narrow capability, not general scientific reasoning.',
            'No text-controller self-repair; no oracle or hardcoded answer is used by the numeric controller.',
            'No GPU execution or result is claimed by the code author.']}

def sha920(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()

def blob920(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def save920():
    p = Path(str(OUT920) + '.tmp')
    p.write_text(json.dumps(D920, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    p.replace(OUT920)

def log920(*args):
    msg = ' '.join(map(str, args))
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        print(msg, flush=True)
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        with LOG920.open('a', encoding='utf-8') as f:
            f.write(msg + '\n')

def gate920(name, ok, detail=None):
    D920['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail})
    save920()
    log920('PASS' if ok else 'FAIL', name, detail if detail is not None else '')
    if not ok:
        raise RuntimeError('TEST920_GATE_' + name)

# PRESEALED panel: opaque names and randomized assignments. All scoring stays offline.
RNG920 = random.Random(SEED920)
ALPH920 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

def code920():
    return ''.join(RNG920.choice(ALPH920) for _ in range(9))

worlds920 = []
seen920 = set()
for wi in range(WORLDS920):
    names = []
    while len(names) < 5:
        n = code920()
        if n not in seen920:
            seen920.add(n); names.append(n)
    worlds920.append({'world': 'DOMAIN_' + code920(), 'start': names[0],
                      'middle': names[1], 'end': names[2],
                      'changed_end': names[3], 'decoy_end': names[4]})

questions920 = []
for w in worlds920:
    for pi, fmt in enumerate((
        'In domain {world}, starting from {start}, which endpoint is reached after exactly two directed links?',
        'For {world}, follow two successive directed edges beginning at {start}. Give the final node.',
        'Within {world}, what is the two-step destination of {start}? Do not guess when a link is absent.')):
        questions920.append({'qid': w['world'] + '_P' + str(pi), 'world': w['world'],
                             'question': fmt.format(**w), 'expected': w['end'],
                             'changed_expected': w['changed_end']})

# Each domain has two independent source cards and a deliberately irrelevant card.
# Changed source is an independently forged cartridge, never an in-place mutation.
cards920, card_meta920 = {}, {}
for w in worlds920:
    domain = w['world']
    ids = {kind: 'E920_' + code920() for kind in ('first', 'second', 'changed', 'decoy')}
    w['ids'] = ids
    cards920[ids['first']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['start'] + ' -> ' + w['middle'] + '.\n')
    cards920[ids['second']] = ('Evidence record. Domain: ' + domain + '\n' +
                             'Directed relation: ' + w['middle'] + ' -> ' + w['end'] + '.\n')
    cards920[ids['changed']] = ('Evidence record. Domain: ' + domain + '\n' +
                              'Directed relation: ' + w['middle'] + ' -> ' + w['changed_end'] + '.\n')
    cards920[ids['decoy']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['decoy_end'] + ' -> ' + w['start'] + '.\n')
    for kind, cid in ids.items():
        card_meta920[cid] = {'domain': domain, 'kind': kind, 'body_sha256': sha920(cards920[cid])}
NULL920 = 'E920_NULL'
cards920[NULL920] = 'CONTROL MEMORY. No directed relations are available.\n'
card_meta920[NULL920] = {'domain': None, 'kind': 'null', 'body_sha256': sha920(cards920[NULL920])}

# The blind controller sees candidate IDs and its own outputs, never the answer key.
# Baseline and interventions use the SAME code; only physically eligible cartridges differ.
ARMS920 = ('FULL', 'REMOVE_SECOND', 'REPLACE_SECOND', 'ADD_IRRELEVANT', 'NULL')
PANEL920 = {'seed': SEED920, 'world_count': WORLDS920, 'paraphrases': PARAPHRASES920,
            'questions': [{'qid': q['qid'], 'question': q['question']} for q in questions920],
            'arms': ARMS920, 'limits': [MAX_STEPS920, MAX_NEW_ANSWER920, MAX_NEW_CONTROL920,
                                       MAX_CANDIDATES920], 'card_hashes': card_meta920}
PANEL_SHA920 = sha920(json.dumps(PANEL920, ensure_ascii=False, sort_keys=True))
D920['panel_sha256'] = PANEL_SHA920
D920['panel_public'] = PANEL920
OFFLINE920.write_text(json.dumps({'note': 'OFFLINE ONLY — NEVER IMPORT INTO CONTROLLER',
                                  'questions': questions920, 'worlds': worlds920},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D920['offline_key_sha256'] = sha920(OFFLINE920.read_bytes())
save920()

# The engine is imported from the EXACT locked TEST815 AST prelude, unchanged.
# The original TEST815 experiment is never executed.
try:
    log920('TEST920_START', RUN920, 'PANEL_SHA', PANEL_SHA920)
    req920 = urllib.request.Request(REPO920 + '815.py', headers={'User-Agent': 'AKBASCORE-TEST920'})
    with urllib.request.urlopen(req920, timeout=180) as f:
        raw815_920 = f.read(120001)
    gate920('LOCK815', len(raw815_920) <= 120000 and blob920(raw815_920) == LOCK815_920,
            blob920(raw815_920))
    tree815_920 = ast.parse(raw815_920.decode('utf-8'), filename='815.py')
    idx920 = [i for i, n in enumerate(tree815_920.body) if isinstance(n, ast.Try)]
    gate920('AST_BOUNDARY', len(idx920) == 1 and idx920[0] == len(tree815_920.body) - 1, idx920)
    exec(compile(ast.fix_missing_locations(ast.Module(body=tree815_920.body[:idx920[0]], type_ignores=[])),
                 'LOCKED_TEST815_PRELUDE', 'exec'), globals())
    gate920('LOCKED_ENGINE_SYMBOLS', all(callable(globals().get(x)) for x in
            ('model_setup', 'physical_commit', 'safe_load', 'build_fusion', 'free_generate',
             'memory_seals', 'compare_seals', 'sentinel', 'release', 'numeric_rank')))
    gate920('FRESH_BANK', len(entries) == 0, len(entries))
    import torch as _torch920
    SDPA920 = _torch920.nn.functional.scaled_dot_product_attention

    # Token budget is validated BEFORE loading 72B model weights.
    tok920 = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=False)
    tok_counts920 = {cid: len(tok920.encode(body, add_special_tokens=False)) for cid, body in cards920.items()}
    gate920('TOKEN_BUDGET', all(4 <= n <= 256 for n in tok_counts920.values()),
            {'max_body_tokens': max(tok_counts920.values()), 'stage': 'TOKENIZER_PRE_MODEL'})
    del tok920

    model_setup()
    before920 = sentinel()
    gate920('FROZEN_PREFIX', P == 30, P)
    gate920('FUSION_BUDGET',
            P + 2 * max(tok_counts920.values()) + 64 <= MAX_FUSED_TOKENS,
            {'max_body_tokens': max(tok_counts920.values()), 'max_fused_tokens': MAX_FUSED_TOKENS})
    for cid, body in cards920.items():
        physical_commit(cid, body)
        gate920('BODY_SHA_' + cid, entries[cid].get('body_sha256') == sha920(body))
    gate920('PHYSICAL_COUNT', len(entries) == len(cards920), len(entries))
    for cid in cards920:
        p = safe_load(entries[cid])
        gate920('RELOAD_' + cid, p['book_id'] == cid and int(p['n']) > P and
                len(p['lower']) == CUT + 1 and tuple(p['h'].shape)[-1] == H)
        del p
    release()

    # Locked numerical H3 bank from TEST815: do not call its fixed 22-card gate.
    # Same H3 tensor sampling/normalization, generalized to this experiment's size.
    bank920 = {}
    for cid in sorted(entries):
        cp = safe_load(entries[cid])
        try:
            x = cp['h'][0, P:, :].float().cpu().numpy()
            gate920('H3_NONEMPTY_' + cid, x.ndim == 2 and x.shape[0] > 8 and x.shape[1] == H)
            ix = np.linspace(0, len(x) - 1, min(96, len(x)), dtype=np.int64)
            bank920[cid] = normalized(x[ix]).T.copy()
        finally:
            del cp
    gate920('H3_BANK', len(bank920) == len(entries), len(bank920))

    def eligible920(world, arm):
        """Experimenter intervention, never inferred from answer or given to controller."""
        pool = []
        for w in worlds920:
            ids = w['ids']
            pool += [ids['first'], ids['second']]
            if arm == 'ADD_IRRELEVANT':
                pool.append(ids['decoy'])
        current = next(w for w in worlds920 if w['world'] == world)
        if arm == 'REMOVE_SECOND':
            pool.remove(current['ids']['second'])
        elif arm == 'REPLACE_SECOND':
            pool.remove(current['ids']['second'])
            pool.append(current['ids']['changed'])
        elif arm == 'NULL':
            return [NULL920]
        return pool

    def _native920_verbose(ids, prompt, tag, max_new):
        t0 = time.perf_counter()
        mem, active, fusion_steps, _ = build_fusion(ids, 'TEST920_' + tag, True)
        try:
            gate920('NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
            n = int(mem[0][0].shape[-2])
            expected = P + sum(int(entries[x]['body_tokens']) for x in ids)
            gate920('NATIVE_LENGTH_' + tag, n == expected, {'n': n, 'expected': expected})
            first = int(entries[ids[0]]['body_tokens'])
            spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                    {'B0': (P, n), 'B1': (n, n)}
            seals = memory_seals(mem)
            out = free_generate(mem, prompt, seed=None, gain=0., max_new=max_new, spans=spans)
            gate920('KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
            gate920('SDPA_RESTORED_' + tag,
                    _torch920.nn.functional.scaled_dot_product_attention is SDPA920)
            return {'raw': out['raw'], 'tokens': int(out['generated_tokens']),
                    'possibly_truncated': int(out['generated_tokens']) >= max_new,
                    'ids': list(ids), 'time_seconds': round(time.perf_counter() - t0, 3),
                    'fusion_steps': fusion_steps,
                    'cartridge_shas': [entries[x]['sha256'] for x in ids]}
        finally:
            del mem
            gc.collect()
            release()

    def native920(ids, prompt, tag, max_new):
        # Suppress repetitive engine PASS / fusion messages on notebook screen.
        # Every failed native call still exposes its captured diagnostic tail.
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                result = _native920_verbose(ids, prompt, tag, max_new)
            return result
        except BaseException:
            log920('NATIVE_FAILURE_DIAGNOSTICS', tag, capture.getvalue()[-12000:])
            raise

    def answer_prompt920(question):
        # Readout boundary only; never used to choose a physical action.
        return ('Use only mounted physical evidence. Follow directed links. '
                'If a link is missing, answer UNKNOWN. Return only the endpoint '
                'or UNKNOWN. Question: ' + question)

    # Model-native state observation: original TEST779/790 native CUT3 probe, unchanged.
    # A question is tokenized at the input boundary; NO language is generated or parsed
    # by the control loop. Only tensors, floats, and opaque cartridge IDs are used.
    gate920('NUMERICAL_PROBE_SYMBOL', callable(globals().get('observe_state')))

    def probe920(ids, question, tag):
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                mem, active, _, _ = build_fusion(ids, 'TEST920_NUM_' + tag, True)
                try:
                    gate920('NUM_NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
                    n = int(mem[0][0].shape[-2])
                    gate920('NUM_NATIVE_LENGTH_' + tag,
                            n == P + sum(int(entries[x]['body_tokens']) for x in ids))
                    first = int(entries[ids[0]]['body_tokens'])
                    spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                            {'B0': (P, n), 'B1': (n, n)}
                    seals = memory_seals(mem)
                    state, att = observe_state(mem, question, spans)
                    gate920('NUM_STATE_' + tag, state.numel() == H and
                            bool(_torch920.isfinite(state).all().item()))
                    gate920('NUM_KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
                    gate920('NUM_SDPA_' + tag,
                            _torch920.nn.functional.scaled_dot_product_attention is SDPA920)
                    vec = state.detach().float().cpu().numpy().copy()
                    return vec, att
                finally:
                    del mem
                    gc.collect()
                    release()
        except BaseException:
            log920('NUMERICAL_PROBE_FAILURE', tag, capture.getvalue()[-6000:])
            raise

    def unit920(x):
        y = np.asarray(x, dtype=np.float64).reshape(-1)
        norm = float(np.linalg.norm(y))
        if not np.isfinite(norm) or norm <= 1e-12:
            raise RuntimeError('NUMERIC_NONFINITE_OR_ZERO_STATE')
        return y / norm

    def run_trial920(q, arm):
        allowed = eligible920(q['world'], arm)
        ranked, scores = numeric_rank(q['question'], {cid: bank920[cid] for cid in allowed})
        gate920('RANK_' + q['qid'] + '_' + arm,
                len(ranked) == len(allowed) and set(ranked) == set(allowed))
        tag = q['qid'] + '_' + arm
        selected = [ranked[0]]
        state, _ = probe920(selected, q['question'], tag + '_INITIAL')
        previous = unit920(state)
        # Normalized question-to-H3 ranking supplies the first candidate priority.
        # Controller observes actual CUT3 state after every physical read.
        vals = np.array([float(scores[c]) for c in ranked], dtype=np.float64)
        gate920('FINITE_RANK_' + tag, bool(np.isfinite(vals).all()))
        # Dimensionless dynamic variables: no fitted per-case answers or oracle labels.
        velocity = np.zeros(H, dtype=np.float64)
        energy = 1.0
        trace = [{'step': 0, 'ids': selected[:], 'state_norm': float(np.linalg.norm(state)),
                  'state_sha256': sha920(np.asarray(state, dtype=np.float32).tobytes())}]
        decisions = []
        stop_reason = None
        safety_stop = None
        # Numerical state feedback, not a textual KEEP/CORRECT/RESEARCH/STOP parser.
        # Damping is a time-step recurrence; it must not be misrepresented as the
        # original DRA depth envelope or a proven differential-equation controller.
        for step in range(1, MAX_STEPS920 + 1):
            candidates = [c for c in ranked if c not in selected]
            if not candidates:
                stop_reason = 'CANDIDATE_EXHAUSTION'
                break
            # Score from H3 cartridge tensors; no generated words or labels.
            # Novelty relative to the current native CUT3 state is an observable
            # geometric feature, not a correctness oracle.
            utilities = {}
            for cid in candidates:
                bank = np.asarray(bank920[cid], dtype=np.float64)
                centroid = unit920(bank.mean(axis=1))
                novelty = 1.0 - abs(float(np.dot(previous, centroid)))
                base = float(scores[cid])
                utilities[cid] = (base, novelty)
            base_arr = np.array([utilities[c][0] for c in candidates], dtype=np.float64)
            spread = float(np.std(vals)) + 1e-9
            priority = {c: (utilities[c][0] - float(np.mean(vals))) / spread +
                        0.25 * utilities[c][1] for c in candidates}
            target = max(candidates, key=lambda c: (priority[c], -ranked.index(c)))
            # A measured, numerical stopping gate: after at least one physical
            # comparison, stop only when state change and velocity are both small.
            if step > 1 and energy < 0.025 and float(np.linalg.norm(velocity)) < 0.025:
                stop_reason = 'NUMERICAL_STABILITY'
                break
            next_ids = selected + [target] if len(selected) == 1 else [selected[-1], target]
            new_state, _ = probe920(next_ids, q['question'], tag + '_STEP_' + str(step))
            current = unit920(new_state)
            displacement = current - previous
            # Critically bounded damped feedback state, measured after actual fusion.
            velocity = 0.30 * velocity + 0.70 * displacement
            energy = float(np.linalg.norm(displacement) / np.sqrt(2.0))
            gate920('FINITE_FEEDBACK_' + tag + '_' + str(step),
                    bool(np.isfinite(energy) and np.isfinite(velocity).all()))
            decisions.append({'step': step, 'target': target, 'rank_score': float(scores[target]),
                              'priority': float(priority[target]), 'state_change': energy,
                              'velocity_norm': float(np.linalg.norm(velocity)),
                              'controller': 'NUMERIC_CUT3_H3_FEEDBACK'})
            trace.append({'step': step, 'ids': next_ids[:], 'state_change': energy,
                          'state_sha256': sha920(np.asarray(new_state, dtype=np.float32).tobytes())})
            selected = next_ids
            previous = current
        if stop_reason is None:
            safety_stop = 'MAX_STEPS_SAFETY_BOUND'
        # Language is permitted only at the readout boundary, never to control
        # which memory is mounted, when to stop, or how the feedback is updated.
        initial = native920([ranked[0]], answer_prompt920(q['question']),
                            tag + '_INITIAL_READOUT', MAX_NEW_ANSWER920)
        final = native920(selected, answer_prompt920(q['question']),
                          tag + '_FINAL_READOUT', MAX_NEW_ANSWER920)
        return {'qid': q['qid'], 'arm': arm, 'question': q['question'],
                'initial': initial['raw'].strip(), 'final': final['raw'].strip(),
                'initial_selected': [ranked[0]], 'ranked_ids': ranked,
                'ranked_scores': {cid: float(scores[cid]) for cid in ranked},
                'trace': trace, 'model_decisions': decisions,
                'model_stop': stop_reason == 'NUMERICAL_STABILITY',
                'numeric_stop_reason': stop_reason, 'safety_stop': safety_stop,
                'steps_executed': len(decisions),
                'model_actions': ['NUMERIC_READ'] * len(decisions),
                'valid_decisions': len(decisions), 'first_valid_decisions': len(decisions),
                'repair_attempts': 0, 'repair_successes': 0,
                'controller_decisions': len(decisions)}

    for q in questions920:
        for arm in ARMS920:
            row = run_trial920(q, arm)
            D920['trials'].append(row)
            save920()
            log920('TEST920_TRIAL', row['qid'], arm, 'initial', repr(row['initial']),
                   'final', repr(row['final']), 'actions', row['model_actions'], 'numerical_stop', row['numeric_stop_reason'],
                   'model_stop', row['model_stop'], 'safety_stop', row['safety_stop'])

    # Fixed two-read comparison: no model-selected action, same question and H3 bank.
    # It is an experimental control, NOT the proposed autonomous policy.
    D920['fixed_baseline'] = []
    for q in questions920:
        allowed = eligible920(q['world'], 'FULL')
        ranked, _ = numeric_rank(q['question'], {cid: bank920[cid] for cid in allowed})
        ids = ranked[:2]
        baseline = native920(ids, answer_prompt920(q['question']),
                             q['qid'] + '_FIXED_TWO', MAX_NEW_ANSWER920)
        D920['fixed_baseline'].append({'qid': q['qid'], 'ids': ids, 'raw': baseline['raw'],
                                       'possibly_truncated': baseline['possibly_truncated']})
        save920()
    gate920('FIXED_BASELINE_COUNT', len(D920['fixed_baseline']) == len(questions920))

    gate920('TRIAL_COUNT', len(D920['trials']) == len(questions920) * len(ARMS920),
            len(D920['trials']))
    gate920('FROZEN_WEIGHT_SENTINEL', before920 == sentinel())
    gate920('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    gate920('PANEL_UNCHANGED', sha920(json.dumps(PANEL920, ensure_ascii=False, sort_keys=True)) == PANEL_SHA920)
    for cid in cards920:
        gate920('FINAL_SHA_' + cid, sha_file(CART_DIR / entries[cid]['file']) == entries[cid]['sha256'])

    # Diagnostic exact-match scoring is performed OFFLINE, after all model calls.
    # The expected answer never enters native920 or run_trial920.
    lookup920 = {q['qid']: q for q in questions920}
    def exact920(ans, expected):
        return ans.strip().strip(' .\n').upper() == expected.upper()
    scored920 = []
    for r in D920['trials']:
        key = lookup920[r['qid']]
        expected = key['changed_expected'] if r['arm'] == 'REPLACE_SECOND' else key['expected']
        should_unknown = r['arm'] in ('REMOVE_SECOND', 'NULL')
        correct = (r['final'].strip().upper() == 'UNKNOWN') if should_unknown else exact920(r['final'], expected)
        scored920.append({'qid': r['qid'], 'arm': r['arm'], 'expected': 'UNKNOWN' if should_unknown else expected,
                          'exact_correct': correct, 'model_stop': r['model_stop'],
                          'valid_decisions': r['valid_decisions'],
                          'controller_decisions': r['controller_decisions'],
                          'repair_attempts': r['repair_attempts'],
                          'repair_successes': r['repair_successes'],
                          'initial': r['initial'], 'final': r['final']})
    D920['fixed_baseline_offline'] = {'cases': len(D920['fixed_baseline']),
        'exact_correct': sum(exact920(b['raw'], lookup920[b['qid']]['expected'])
                             for b in D920['fixed_baseline'])}
    D920['offline_scores'] = {
        arm: {'cases': sum(x['arm'] == arm for x in scored920),
              'exact_correct': sum(x['arm'] == arm and x['exact_correct'] for x in scored920),
              'model_stops': sum(x['arm'] == arm and x['model_stop'] for x in scored920),
              'valid_control_decisions': sum(x['valid_decisions'] for x in scored920 if x['arm'] == arm),
              'total_control_decisions': sum(x['controller_decisions'] for x in scored920 if x['arm'] == arm),
              'repair_attempts': sum(x['repair_attempts'] for x in scored920 if x['arm'] == arm),
              'repair_successes': sum(x['repair_successes'] for x in scored920 if x['arm'] == arm)}
        for arm in ARMS920}
    with REVIEW920.open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['qid', 'arm', 'initial', 'final', 'expected', 'exact_correct', 'model_stop',
                'human_reasoning_correct_0_1', 'human_attribution_correct_0_1',
                'human_autonomous_correction_0_1', 'human_notes']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in scored920:
            writer.writerow({k: row.get(k, '') for k in cols})
    D920['review_sha256'] = sha920(REVIEW920.read_bytes())
    D920['status'] = 'COMPLETE_MECHANICAL_OFFLINE_SCORING_HUMAN_REVIEW_PENDING'
    save920()
    log920('TEST920_COMPLETED', json.dumps(D920['offline_scores']), OUT920, REVIEW920)
except BaseException as e:
    D920['status'] = 'ERROR'
    D920['error'] = {'repr': repr(e), 'traceback': traceback.format_exc()}
    save920()
    log920('TEST920_FAILED', repr(e), traceback.format_exc())
    raise
finally:
    gc.collect()
    if 'release' in globals() and callable(globals()['release']):
        try:
            release()
        except Exception:
            pass
    save920()
