# AKBASCORE SILICON HIPPOCAMPUS — TEST823
# TENSOR-NUMERICAL CONTROL: CUT3 H3 observations -> feedback -> physical cartridge action.
# Built from GPU-completed TEST919 and locked TEST815 engine; no textual action controller.
# Single Colab cell; frozen Qwen2.5-72B NF4; exactly one A100 80GB.
# LOCKED TEST815 engine; no residual hooks, no source replay at read time, no training.
# TEST823: compact blinded validity-gate ablation against retained-signed baseline; no textual control.
# Numerical controller is EXPERIMENTAL; not the original DRA layer-injection motor.
# Question encoding and final answer readout remain language interfaces; control loop is numeric.
import ast, hashlib, urllib.request, json, csv, gc, time, traceback, random, re, datetime, contextlib, io
from pathlib import Path

T823 = '823'
REPO823 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCK815_823 = '77774f87428c0243c9a86ea6a041364acd9c1b03'
SEED823 = 8232026
WORLDS823 = 4
PARAPHRASES823 = 2
MAX_STEPS823 = 4                 # safety ceiling, NOT evidence of autonomous stopping
MAX_NEW_ANSWER823 = 96
MAX_NEW_CONTROL823 = 0  # no control text generated
MAX_CANDIDATES823 = 5
RUN823 = 'TEST823_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
DIR823 = (Path('/content') if Path('/content').exists() else Path('/tmp')) / RUN823
DIR823.mkdir(parents=True, exist_ok=False)
OUT823 = DIR823 / 'TEST823_results.json'
LOG823 = DIR823 / 'TEST823.log'
REVIEW823 = DIR823 / 'TEST823_blind_review.csv'
OFFLINE823 = DIR823 / 'TEST823_offline_key.json'  # never available to inference/controller

D823 = {'test': T823, 'status': 'STARTED', 'run': RUN823,
        'source815_blob': LOCK815_823, 'controller': 'NUMERICAL_VALIDITY_GATE_ABLATION', 'checks': [], 'trials': [],
        'limitations': [
            'Control decisions are computed from H3/CUT3 tensors and numerical feedback, without generated action text.',
            'Numerical feedback is an experimental DRA-inspired audit, NOT the original DRA 1.3 layer steering.',
            'TEST823 compares retained-signed against a predeclared numerical validity gate on identical blinded cases.',
            'Question encoding and final answer readout are boundary interfaces only; no natural-language command or generated text enters the tensor controller.',
            'Offline truth is never given to numeric_rank, free_generate, or controller.',
            'MAX_STEPS is a safety bound, not autonomous stopping.',
            'Native reads and integrity checks are distinct from semantic correctness.',
            'Synthetic two-hop relations test a narrow capability, not general scientific reasoning.',
            'No text-controller self-repair; no oracle or hardcoded answer is used by the numeric controller.',
            'No GPU execution or result is claimed by the code author.', 'Both policies retain all visited cartridges; the validity gate may abstain before fusion.', 'Numerical stability is not equivalent to epistemic sufficiency; safety stops are reported separately.', 'No DRA equivalence is claimed; this test isolates numerical candidate validity, not stopping calibration.']}

def sha823(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()

def blob823(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def save823():
    p = Path(str(OUT823) + '.tmp')
    p.write_text(json.dumps(D823, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    p.replace(OUT823)

def log823(*args):
    msg = ' '.join(map(str, args))
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        print(msg, flush=True)
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        with LOG823.open('a', encoding='utf-8') as f:
            f.write(msg + '\n')

def gate823(name, ok, detail=None):
    D823['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail})
    save823()
    log823('PASS' if ok else 'FAIL', name, detail if detail is not None else '')
    if not ok:
        raise RuntimeError('TEST823_GATE_' + name)

# PRESEALED panel: opaque names and randomized assignments. All scoring stays offline.
RNG823 = random.Random(SEED823)
ALPH823 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

def code823():
    return ''.join(RNG823.choice(ALPH823) for _ in range(9))

worlds823 = []
seen823 = set()
for wi in range(WORLDS823):
    names = []
    while len(names) < 5:
        n = code823()
        if n not in seen823:
            seen823.add(n); names.append(n)
    worlds823.append({'world': 'DOMAIN_' + code823(), 'start': names[0],
                      'middle': names[1], 'end': names[2],
                      'changed_end': names[3], 'decoy_end': names[4]})

questions823 = []
for w in worlds823:
    for pi, fmt in enumerate((
        'In domain {world}, starting from {start}, which endpoint is reached after exactly two directed links?',
        'For {world}, follow two successive directed edges beginning at {start}. Give the final node.')):
        questions823.append({'qid': w['world'] + '_P' + str(pi), 'world': w['world'],
                             'question': fmt.format(**w), 'expected': w['end'],
                             'changed_expected': w['changed_end']})

# Each domain has two independent source cards and a deliberately irrelevant card.
# Changed source is an independently forged cartridge, never an in-place mutation.
cards823, card_meta823 = {}, {}
for w in worlds823:
    domain = w['world']
    ids = {kind: 'E823_' + code823() for kind in ('first', 'second', 'changed', 'decoy')}
    w['ids'] = ids
    cards823[ids['first']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['start'] + ' -> ' + w['middle'] + '.\n')
    cards823[ids['second']] = ('Evidence record. Domain: ' + domain + '\n' +
                             'Directed relation: ' + w['middle'] + ' -> ' + w['end'] + '.\n')
    cards823[ids['changed']] = ('Evidence record. Domain: ' + domain + '\n' +
                              'Directed relation: ' + w['middle'] + ' -> ' + w['changed_end'] + '.\n')
    cards823[ids['decoy']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['decoy_end'] + ' -> ' + w['start'] + '.\n')
    for kind, cid in ids.items():
        card_meta823[cid] = {'domain': domain, 'kind': kind, 'body_sha256': sha823(cards823[cid])}
NULL823 = 'E823_NULL'
cards823[NULL823] = 'CONTROL MEMORY. No directed relations are available.\n'
card_meta823[NULL823] = {'domain': None, 'kind': 'null', 'body_sha256': sha823(cards823[NULL823])}

# The blind controller sees candidate IDs and its own outputs, never the answer key.
# Baseline and interventions use the SAME code; only physically eligible cartridges differ.
ARMS823 = ('FULL', 'REMOVE_SECOND', 'REPLACE_SECOND', 'ADD_IRRELEVANT', 'NULL')
PANEL823 = {'seed': SEED823, 'world_count': WORLDS823, 'paraphrases': PARAPHRASES823,
            'questions': [{'qid': q['qid'], 'question': q['question']} for q in questions823],
            'arms': ARMS823, 'policies': ['RETAINED_SIGNED', 'VALIDITY_GATED'], 'limits': [MAX_STEPS823, MAX_NEW_ANSWER823, MAX_NEW_CONTROL823,
                                       MAX_CANDIDATES823], 'card_hashes': card_meta823}
PANEL_SHA823 = sha823(json.dumps(PANEL823, ensure_ascii=False, sort_keys=True))
D823['panel_sha256'] = PANEL_SHA823
D823['panel_public'] = PANEL823
OFFLINE823.write_text(json.dumps({'note': 'OFFLINE ONLY — NEVER IMPORT INTO CONTROLLER',
                                  'questions': questions823, 'worlds': worlds823},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D823['offline_key_sha256'] = sha823(OFFLINE823.read_bytes())
save823()

# The engine is imported from the EXACT locked TEST815 AST prelude, unchanged.
# The original TEST815 experiment is never executed.
try:
    log823('TEST823_START', RUN823, 'PANEL_SHA', PANEL_SHA823)
    req823 = urllib.request.Request(REPO823 + '815.py', headers={'User-Agent': 'AKBASCORE-TEST823'})
    with urllib.request.urlopen(req823, timeout=180) as f:
        raw815_823 = f.read(120001)
    gate823('LOCK815', len(raw815_823) <= 120000 and blob823(raw815_823) == LOCK815_823,
            blob823(raw815_823))
    tree815_823 = ast.parse(raw815_823.decode('utf-8'), filename='815.py')
    idx823 = [i for i, n in enumerate(tree815_823.body) if isinstance(n, ast.Try)]
    gate823('AST_BOUNDARY', len(idx823) == 1 and idx823[0] == len(tree815_823.body) - 1, idx823)
    exec(compile(ast.fix_missing_locations(ast.Module(body=tree815_823.body[:idx823[0]], type_ignores=[])),
                 'LOCKED_TEST815_PRELUDE', 'exec'), globals())
    gate823('LOCKED_ENGINE_SYMBOLS', all(callable(globals().get(x)) for x in
            ('model_setup', 'physical_commit', 'safe_load', 'build_fusion', 'free_generate',
             'memory_seals', 'compare_seals', 'sentinel', 'release', 'numeric_rank')))
    gate823('FRESH_BANK', len(entries) == 0, len(entries))
    import torch as _torch823
    SDPA823 = _torch823.nn.functional.scaled_dot_product_attention

    # Token budget is validated BEFORE loading 72B model weights.
    tok823 = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=False)
    tok_counts823 = {cid: len(tok823.encode(body, add_special_tokens=False)) for cid, body in cards823.items()}
    gate823('TOKEN_BUDGET', all(4 <= n <= 256 for n in tok_counts823.values()),
            {'max_body_tokens': max(tok_counts823.values()), 'stage': 'TOKENIZER_PRE_MODEL'})
    del tok823

    model_setup()
    before823 = sentinel()
    gate823('FROZEN_PREFIX', P == 30, P)
    gate823('FUSION_BUDGET',
            P + MAX_STEPS823 * max(tok_counts823.values()) + 64 <= MAX_FUSED_TOKENS,
            {'max_body_tokens': max(tok_counts823.values()), 'max_fused_tokens': MAX_FUSED_TOKENS})
    for cid, body in cards823.items():
        physical_commit(cid, body)
        gate823('BODY_SHA_' + cid, entries[cid].get('body_sha256') == sha823(body))
    gate823('PHYSICAL_COUNT', len(entries) == len(cards823), len(entries))
    for cid in cards823:
        p = safe_load(entries[cid])
        gate823('RELOAD_' + cid, p['book_id'] == cid and int(p['n']) > P and
                len(p['lower']) == CUT + 1 and tuple(p['h'].shape)[-1] == H)
        del p
    release()

    # Locked numerical H3 bank from TEST815: do not call its fixed 22-card gate.
    # Same H3 tensor sampling/normalization, generalized to this experiment's size.
    bank823 = {}
    for cid in sorted(entries):
        cp = safe_load(entries[cid])
        try:
            x = cp['h'][0, P:, :].float().cpu().numpy()
            gate823('H3_NONEMPTY_' + cid, x.ndim == 2 and x.shape[0] > 8 and x.shape[1] == H)
            ix = np.linspace(0, len(x) - 1, min(96, len(x)), dtype=np.int64)
            bank823[cid] = normalized(x[ix]).T.copy()
        finally:
            del cp
    gate823('H3_BANK', len(bank823) == len(entries), len(bank823))

    def eligible823(world, arm):
        """Experimenter intervention, never inferred from answer or given to controller."""
        pool = []
        for w in worlds823:
            ids = w['ids']
            pool += [ids['first'], ids['second']]
            if arm == 'ADD_IRRELEVANT':
                pool.append(ids['decoy'])
        current = next(w for w in worlds823 if w['world'] == world)
        if arm == 'REMOVE_SECOND':
            pool.remove(current['ids']['second'])
        elif arm == 'REPLACE_SECOND':
            pool.remove(current['ids']['second'])
            pool.append(current['ids']['changed'])
        elif arm == 'NULL':
            return [NULL823]
        return pool

    def _native823_verbose(ids, prompt, tag, max_new):
        t0 = time.perf_counter()
        mem, active, fusion_steps, _ = build_fusion(ids, 'TEST823_' + tag, True)
        try:
            gate823('NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
            n = int(mem[0][0].shape[-2])
            expected = P + sum(int(entries[x]['body_tokens']) for x in ids)
            gate823('NATIVE_LENGTH_' + tag, n == expected, {'n': n, 'expected': expected})
            first = int(entries[ids[0]]['body_tokens'])
            spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                    {'B0': (P, n), 'B1': (n, n)}
            seals = memory_seals(mem)
            out = free_generate(mem, prompt, seed=None, gain=0., max_new=max_new, spans=spans)
            gate823('KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
            gate823('SDPA_RESTORED_' + tag,
                    _torch823.nn.functional.scaled_dot_product_attention is SDPA823)
            return {'raw': out['raw'], 'tokens': int(out['generated_tokens']),
                    'possibly_truncated': int(out['generated_tokens']) >= max_new,
                    'ids': list(ids), 'time_seconds': round(time.perf_counter() - t0, 3),
                    'fusion_steps': fusion_steps,
                    'cartridge_shas': [entries[x]['sha256'] for x in ids]}
        finally:
            del mem
            gc.collect()
            release()

    def native823(ids, prompt, tag, max_new):
        # Suppress repetitive engine PASS / fusion messages on notebook screen.
        # Every failed native call still exposes its captured diagnostic tail.
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                result = _native823_verbose(ids, prompt, tag, max_new)
            return result
        except BaseException:
            log823('NATIVE_FAILURE_DIAGNOSTICS', tag, capture.getvalue()[-12000:])
            raise

    def answer_prompt823(question):
        # Readout boundary only; never used to choose a physical action.
        return ('Use only mounted physical evidence. Follow directed links. '
                'If a link is missing, answer UNKNOWN. Return only the endpoint '
                'or UNKNOWN. Question: ' + question)

    # Model-native state observation: original TEST779/790 native CUT3 probe, unchanged.
    # A question is tokenized at the input boundary; NO language is generated or parsed
    # by the control loop. Only tensors, floats, and opaque cartridge IDs are used.
    gate823('NUMERICAL_PROBE_SYMBOL', callable(globals().get('observe_state')))

    def probe823(ids, question, tag):
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                mem, active, _, _ = build_fusion(ids, 'TEST823_NUM_' + tag, True)
                try:
                    gate823('NUM_NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
                    n = int(mem[0][0].shape[-2])
                    gate823('NUM_NATIVE_LENGTH_' + tag,
                            n == P + sum(int(entries[x]['body_tokens']) for x in ids))
                    first = int(entries[ids[0]]['body_tokens'])
                    spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                            {'B0': (P, n), 'B1': (n, n)}
                    seals = memory_seals(mem)
                    state, att = observe_state(mem, question, spans)
                    gate823('NUM_STATE_' + tag, state.numel() == H and
                            bool(_torch823.isfinite(state).all().item()))
                    gate823('NUM_KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
                    gate823('NUM_SDPA_' + tag,
                            _torch823.nn.functional.scaled_dot_product_attention is SDPA823)
                    vec = state.detach().float().cpu().numpy().copy()
                    return vec, att
                finally:
                    del mem
                    gc.collect()
                    release()
        except BaseException:
            log823('NUMERICAL_PROBE_FAILURE', tag, capture.getvalue()[-6000:])
            raise

    def unit823(x):
        y = np.asarray(x, dtype=np.float64).reshape(-1)
        norm = float(np.linalg.norm(y))
        if not np.isfinite(norm) or norm <= 1e-12:
            raise RuntimeError('NUMERIC_NONFINITE_OR_ZERO_STATE')
        return y / norm

    POLICIES823 = ('RETAINED_SIGNED', 'VALIDITY_GATED')

    def run_trial823(q, arm, policy):
        # Strictly blinded: no source-kind, truth labels or answer text enters the controller.
        # Both policies retain evidence; only the predeclared numerical validity gate differs.
        allowed = eligible823(q['world'], arm)
        ranked, scores = numeric_rank(q['question'], {cid: bank823[cid] for cid in allowed})
        tag = q['qid'] + '_' + arm + '_' + policy
        gate823('RANK_' + tag, len(ranked) == len(allowed) and set(ranked) == set(allowed))
        first = ranked[0]
        selected = [first]
        initial_state, _ = probe823(selected, q['question'], tag + '_INITIAL')
        reference = unit823(initial_state)
        previous = reference.copy()
        vals = np.array([float(scores[c]) for c in ranked], dtype=np.float64)
        gate823('FINITE_RANK_' + tag, bool(np.isfinite(vals).all()))
        spread = max(float(np.std(vals)), 1e-9)
        velocity = np.zeros(H, dtype=np.float64)
        changes, alignment_history, decisions, rejected = [], [], [], []
        trace = [{'step': 0, 'ids': selected[:],
                  'state_sha256': sha823(np.asarray(initial_state, dtype=np.float32).tobytes())}]
        stop_reason = None
        safety_stop = None
        for step in range(1, MAX_STEPS823 + 1):
            candidates = [c for c in ranked if c not in selected]
            if not candidates:
                stop_reason = 'CANDIDATE_EXHAUSTION'
                break
            # Retain all physically read evidence; no sliding-window eviction.
            # Signed alignment distinguishes anti-aligned from aligned H3 vectors.
            utilities = {}
            for cid in candidates:
                matrix = np.asarray(bank823[cid], dtype=np.float64)
                colnorm = np.maximum(np.linalg.norm(matrix, axis=0), 1e-12)
                sims = (previous @ matrix) / colnorm
                signed = float(np.quantile(sims, 0.75))
                rank_z = (float(scores[cid]) - float(np.mean(vals))) / spread
                derivative = float(np.dot(velocity, unit823(np.mean(matrix, axis=1)))) if np.linalg.norm(velocity) > 1e-12 else 0.0
                # Feedback disabled in both arms to isolate validity gating;
                # not presented as a port of the original layerwise DRA motor.
                feedback = 0.0
                utilities[cid] = {'signed_alignment': signed, 'rank_z': rank_z,
                                  'derivative': derivative, 'feedback': feedback,
                                  'priority': rank_z + signed + feedback}
            # Predeclared, source-blind candidate-validity gate. Both inputs are
            # numerical H3/CUT3 observations; no card kind, answer, or source text.
            # Relative cutoffs are recomputed within each trial, never tuned to labels.
            if policy == 'VALIDITY_GATED':
                priorities = np.array([utilities[c]['priority'] for c in candidates], dtype=np.float64)
                signed_values = np.array([utilities[c]['signed_alignment'] for c in candidates], dtype=np.float64)
                priority_floor = float(np.median(priorities))
                signed_floor = float(np.median(signed_values))
                valid = [c for c in candidates if utilities[c]['priority'] >= priority_floor and
                         utilities[c]['signed_alignment'] >= signed_floor]
                rejected.append({'step': step, 'candidates': len(candidates), 'valid': len(valid),
                                 'priority_floor': priority_floor, 'signed_floor': signed_floor,
                                 'rejected_ids': [c for c in candidates if c not in valid]})
                if not valid:
                    stop_reason = 'NUMERIC_VALIDITY_ABSTENTION'
                    break
                target = max(valid, key=lambda c: (utilities[c]['priority'], -ranked.index(c)))
            else:
                target = max(candidates, key=lambda c: (utilities[c]['priority'], -ranked.index(c)))
            # Stability is a diagnostic stop, not an evidence-sufficiency oracle.
            if len(changes) >= 2:
                recent = np.asarray(changes[-2:], dtype=np.float64)
                baseline = max(float(np.median(changes)), 1e-12)
                if float(np.max(recent)) < 0.10 * baseline and float(np.linalg.norm(velocity)) < 0.10 * baseline:
                    stop_reason = 'RELATIVE_TENSOR_STABILITY'
                    break
            next_ids = selected + [target]
            gate823('UNIQUE_ACTIVE_' + tag + '_' + str(step), len(set(next_ids)) == len(next_ids))
            new_state, att = probe823(next_ids, q['question'], tag + '_STEP_' + str(step))
            current = unit823(new_state)
            delta = current - previous
            displacement = float(np.linalg.norm(delta))
            velocity = 0.30 * velocity + 0.70 * delta
            signed_change = float(np.dot(previous, current))
            alignment_history.append(signed_change)
            changes.append(displacement)
            gate823('FINITE_FEEDBACK_' + tag + '_' + str(step),
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
                          'state_sha256': sha823(np.asarray(new_state, dtype=np.float32).tobytes())})
            selected = next_ids
            previous = current
        if stop_reason is None:
            safety_stop = 'MAX_STEPS_SAFETY_BOUND'
        initial = native823([first], answer_prompt823(q['question']),
                            tag + '_INITIAL_READOUT', MAX_NEW_ANSWER823)
        final = native823(selected, answer_prompt823(q['question']),
                          tag + '_FINAL_READOUT', MAX_NEW_ANSWER823)
        return {'qid': q['qid'], 'arm': arm, 'policy': policy, 'question': q['question'],
                'initial': initial['raw'].strip(), 'final': final['raw'].strip(),
                'initial_selected': [first], 'ranked_ids': ranked,
                'ranked_scores': {cid: float(scores[cid]) for cid in ranked},
                'trace': trace, 'model_decisions': decisions, 'validity_gate_audit': rejected,
                'model_stop': False, 'numerical_stop': stop_reason in ('RELATIVE_TENSOR_STABILITY', 'NUMERIC_VALIDITY_ABSTENTION'),
                'numeric_stop_reason': stop_reason, 'safety_stop': safety_stop,
                'steps_executed': len(decisions), 'model_actions': ['NUMERIC_READ'] * len(decisions),
                'valid_decisions': len(decisions), 'first_valid_decisions': len(decisions),
                'repair_attempts': 0, 'repair_successes': 0,
                'controller_decisions': len(decisions)}

    for q in questions823:
        for arm in ARMS823:
            for policy in POLICIES823:
                row = run_trial823(q, arm, policy)
                D823['trials'].append(row)
                save823()
                log823('TEST823_TRIAL', row['qid'], arm, policy, 'steps', row['steps_executed'],
                       'stop', row['numeric_stop_reason'] or row['safety_stop'], 'final', repr(row['final'][:80]))

    # Fixed two-read comparison: no model-selected action, same question and H3 bank.
    # It is an experimental control, NOT the proposed autonomous policy.
    D823['fixed_baseline'] = []
    for q in questions823:
        allowed = eligible823(q['world'], 'FULL')
        ranked, _ = numeric_rank(q['question'], {cid: bank823[cid] for cid in allowed})
        ids = ranked[:2]
        baseline = native823(ids, answer_prompt823(q['question']),
                             q['qid'] + '_FIXED_TWO', MAX_NEW_ANSWER823)
        D823['fixed_baseline'].append({'qid': q['qid'], 'ids': ids, 'raw': baseline['raw'],
                                       'possibly_truncated': baseline['possibly_truncated']})
        save823()
    gate823('FIXED_BASELINE_COUNT', len(D823['fixed_baseline']) == len(questions823))

    gate823('TRIAL_COUNT', len(D823['trials']) == len(questions823) * len(ARMS823) * len(POLICIES823),
            len(D823['trials']))
    gate823('FROZEN_WEIGHT_SENTINEL', before823 == sentinel())
    gate823('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    gate823('PANEL_UNCHANGED', sha823(json.dumps(PANEL823, ensure_ascii=False, sort_keys=True)) == PANEL_SHA823)
    for cid in cards823:
        gate823('FINAL_SHA_' + cid, sha_file(CART_DIR / entries[cid]['file']) == entries[cid]['sha256'])

    # Diagnostic exact-match scoring is performed OFFLINE, after all model calls.
    # The expected answer never enters native823 or run_trial823.
    lookup823 = {q['qid']: q for q in questions823}
    def exact823(ans, expected):
        return ans.strip().strip(' .\n').upper() == expected.upper()
    scored823 = []
    for r in D823['trials']:
        key = lookup823[r['qid']]
        expected = key['changed_expected'] if r['arm'] == 'REPLACE_SECOND' else key['expected']
        should_unknown = r['arm'] in ('REMOVE_SECOND', 'NULL')
        correct = (r['final'].strip().upper() == 'UNKNOWN') if should_unknown else exact823(r['final'], expected)
        scored823.append({'qid': r['qid'], 'arm': r['arm'], 'policy': r['policy'], 'expected': 'UNKNOWN' if should_unknown else expected,
                          'exact_correct': correct, 'model_stop': r['model_stop'],
                          'valid_decisions': r['valid_decisions'],
                          'controller_decisions': r['controller_decisions'],
                          'repair_attempts': r['repair_attempts'],
                          'repair_successes': r['repair_successes'],
                          'initial': r['initial'], 'final': r['final']})
    D823['fixed_baseline_offline'] = {'cases': len(D823['fixed_baseline']),
        'exact_correct': sum(exact823(b['raw'], lookup823[b['qid']]['expected'])
                             for b in D823['fixed_baseline'])}
    D823['offline_scores'] = {
        policy: {arm: {
            'cases': sum(x['arm'] == arm and x['policy'] == policy for x in scored823),
            'exact_correct': sum(x['arm'] == arm and x['policy'] == policy and x['exact_correct'] for x in scored823),
            'numerical_stability_stops': sum(r['arm'] == arm and r['policy'] == policy and r['numeric_stop_reason'] == 'RELATIVE_TENSOR_STABILITY' for r in D823['trials']),
            'validity_abstentions': sum(r['arm'] == arm and r['policy'] == policy and r['numeric_stop_reason'] == 'NUMERIC_VALIDITY_ABSTENTION' for r in D823['trials']),
            'safety_bound_stops': sum(r['arm'] == arm and r['policy'] == policy and r['safety_stop'] == 'MAX_STEPS_SAFETY_BOUND' for r in D823['trials']),
            'mean_reads': round(sum(r['steps_executed'] for r in D823['trials'] if r['arm'] == arm and r['policy'] == policy) / len(questions823), 3)
        } for arm in ARMS823} for policy in POLICIES823}
    with REVIEW823.open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['qid', 'arm', 'policy', 'initial', 'final', 'expected', 'exact_correct', 'model_stop',
                'human_reasoning_correct_0_1', 'human_attribution_correct_0_1',
                'human_autonomous_correction_0_1', 'human_notes']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in scored823:
            writer.writerow({k: row.get(k, '') for k in cols})
    D823['review_sha256'] = sha823(REVIEW823.read_bytes())
    D823['status'] = 'COMPLETE_MECHANICAL_OFFLINE_SCORING_HUMAN_REVIEW_PENDING'
    save823()
    log823('TEST823_COMPLETED', json.dumps(D823['offline_scores']), OUT823, REVIEW823)
except BaseException as e:
    D823['status'] = 'ERROR'
    D823['error'] = {'repr': repr(e), 'traceback': traceback.format_exc()}
    save823()
    log823('TEST823_FAILED', repr(e), traceback.format_exc())
    raise
finally:
    gc.collect()
    if 'release' in globals() and callable(globals()['release']):
        try:
            release()
        except Exception:
            pass
    save823()
