# AKBASCORE SILICON HIPPOCAMPUS — TEST824
# TENSOR-NUMERICAL CONTROL: CUT3 H3 observations -> feedback -> physical cartridge action.
# Built from GPU-completed TEST919 and locked TEST815 engine; no textual action controller.
# Single Colab cell; frozen Qwen2.5-72B NF4; exactly one A100 80GB.
# LOCKED TEST815 engine; no residual hooks, no source replay at read time, no training.
# TEST824: compact causal diagnosis of retained-signed selection; no new gate, no textual controller.
# Numerical controller is EXPERIMENTAL; not the original DRA layer-injection motor.
# Question encoding and final answer readout remain language interfaces; control loop is numeric.
import ast, hashlib, urllib.request, json, csv, gc, time, traceback, random, re, datetime, contextlib, io
from pathlib import Path

T824 = '824'
REPO824 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCK815_824 = '77774f87428c0243c9a86ea6a041364acd9c1b03'
SEED824 = 8242026
WORLDS824 = 4
PARAPHRASES824 = 1
MAX_STEPS824 = 4                 # safety ceiling, NOT evidence of autonomous stopping
MAX_NEW_ANSWER824 = 96
MAX_NEW_CONTROL824 = 0  # no control text generated
MAX_CANDIDATES824 = 5
RUN824 = 'TEST824_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
DIR824 = (Path('/content') if Path('/content').exists() else Path('/tmp')) / RUN824
DIR824.mkdir(parents=True, exist_ok=False)
OUT824 = DIR824 / 'TEST824_results.json'
LOG824 = DIR824 / 'TEST824.log'
REVIEW824 = DIR824 / 'TEST824_blind_review.csv'
OFFLINE824 = DIR824 / 'TEST824_offline_key.json'  # never available to inference/controller

D824 = {'test': T824, 'status': 'STARTED', 'run': RUN824,
        'source815_blob': LOCK815_824, 'controller': 'RETAINED_SIGNED_CAUSAL_DIAGNOSIS', 'checks': [], 'trials': [],
        'limitations': [
            'Control decisions are computed from H3/CUT3 tensors and numerical feedback, without generated action text.',
            'Numerical feedback is an experimental DRA-inspired audit, NOT the original DRA 1.3 layer steering.',
            'TEST824 preserves retained-signed and records numerical candidate counterfactuals without changing decisions.',
            'Question encoding and final answer readout are boundary interfaces only; no natural-language command or generated text enters the tensor controller.',
            'Offline truth is never given to numeric_rank, free_generate, or controller.',
            'MAX_STEPS is a safety bound, not autonomous stopping.',
            'Native reads and integrity checks are distinct from semantic correctness.',
            'Synthetic two-hop relations test a narrow capability, not general scientific reasoning.',
            'No text-controller self-repair; no oracle or hardcoded answer is used by the numeric controller.',
            'No GPU execution or result is claimed by the code author.', 'Only the previously working retained-signed policy is executed; no validity gate is applied.', 'Numerical stability is not equivalent to epistemic sufficiency; safety stops are reported separately.', 'No DRA equivalence is claimed; this is a diagnostic audit, not stopping calibration.']}

def sha824(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()

def blob824(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def save824():
    p = Path(str(OUT824) + '.tmp')
    p.write_text(json.dumps(D824, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    p.replace(OUT824)

def log824(*args):
    msg = ' '.join(map(str, args))
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        print(msg, flush=True)
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        with LOG824.open('a', encoding='utf-8') as f:
            f.write(msg + '\n')

def gate824(name, ok, detail=None):
    D824['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail})
    save824()
    log824('PASS' if ok else 'FAIL', name, detail if detail is not None else '')
    if not ok:
        raise RuntimeError('TEST824_GATE_' + name)

# PRESEALED panel: opaque names and randomized assignments. All scoring stays offline.
RNG824 = random.Random(SEED824)
ALPH824 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

def code824():
    return ''.join(RNG824.choice(ALPH824) for _ in range(9))

worlds824 = []
seen824 = set()
for wi in range(WORLDS824):
    names = []
    while len(names) < 5:
        n = code824()
        if n not in seen824:
            seen824.add(n); names.append(n)
    worlds824.append({'world': 'DOMAIN_' + code824(), 'start': names[0],
                      'middle': names[1], 'end': names[2],
                      'changed_end': names[3], 'decoy_end': names[4]})

questions824 = []
for w in worlds824:
    for pi, fmt in enumerate((
        'In domain {world}, starting from {start}, which endpoint is reached after exactly two directed links?',
        'For {world}, follow two successive directed edges beginning at {start}. Give the final node.')[:PARAPHRASES824]):
        questions824.append({'qid': w['world'] + '_P' + str(pi), 'world': w['world'],
                             'question': fmt.format(**w), 'expected': w['end'],
                             'changed_expected': w['changed_end']})

# Each domain has two independent source cards and a deliberately irrelevant card.
# Changed source is an independently forged cartridge, never an in-place mutation.
cards824, card_meta824 = {}, {}
for w in worlds824:
    domain = w['world']
    ids = {kind: 'E824_' + code824() for kind in ('first', 'second', 'changed', 'decoy')}
    w['ids'] = ids
    cards824[ids['first']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['start'] + ' -> ' + w['middle'] + '.\n')
    cards824[ids['second']] = ('Evidence record. Domain: ' + domain + '\n' +
                             'Directed relation: ' + w['middle'] + ' -> ' + w['end'] + '.\n')
    cards824[ids['changed']] = ('Evidence record. Domain: ' + domain + '\n' +
                              'Directed relation: ' + w['middle'] + ' -> ' + w['changed_end'] + '.\n')
    cards824[ids['decoy']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['decoy_end'] + ' -> ' + w['start'] + '.\n')
    for kind, cid in ids.items():
        card_meta824[cid] = {'domain': domain, 'kind': kind, 'body_sha256': sha824(cards824[cid])}
NULL824 = 'E824_NULL'
cards824[NULL824] = 'CONTROL MEMORY. No directed relations are available.\n'
card_meta824[NULL824] = {'domain': None, 'kind': 'null', 'body_sha256': sha824(cards824[NULL824])}

# The blind controller sees candidate IDs and its own outputs, never the answer key.
# Baseline and interventions use the SAME code; only physically eligible cartridges differ.
ARMS824 = ('FULL', 'REMOVE_SECOND', 'ADD_IRRELEVANT')
PANEL824 = {'seed': SEED824, 'world_count': WORLDS824, 'paraphrases': PARAPHRASES824,
            'questions': [{'qid': q['qid'], 'question': q['question']} for q in questions824],
            'arms': ARMS824, 'policies': ['RETAINED_SIGNED'], 'limits': [MAX_STEPS824, MAX_NEW_ANSWER824, MAX_NEW_CONTROL824,
                                       MAX_CANDIDATES824], 'card_hashes': card_meta824}
PANEL_SHA824 = sha824(json.dumps(PANEL824, ensure_ascii=False, sort_keys=True))
D824['panel_sha256'] = PANEL_SHA824
D824['panel_public'] = PANEL824
OFFLINE824.write_text(json.dumps({'note': 'OFFLINE ONLY — NEVER IMPORT INTO CONTROLLER',
                                  'questions': questions824, 'worlds': worlds824},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D824['offline_key_sha256'] = sha824(OFFLINE824.read_bytes())
save824()

# The engine is imported from the EXACT locked TEST815 AST prelude, unchanged.
# The original TEST815 experiment is never executed.
try:
    log824('TEST824_START', RUN824, 'PANEL_SHA', PANEL_SHA824)
    req824 = urllib.request.Request(REPO824 + '815.py', headers={'User-Agent': 'AKBASCORE-TEST824'})
    with urllib.request.urlopen(req824, timeout=180) as f:
        raw815_824 = f.read(120001)
    gate824('LOCK815', len(raw815_824) <= 120000 and blob824(raw815_824) == LOCK815_824,
            blob824(raw815_824))
    tree815_824 = ast.parse(raw815_824.decode('utf-8'), filename='815.py')
    idx824 = [i for i, n in enumerate(tree815_824.body) if isinstance(n, ast.Try)]
    gate824('AST_BOUNDARY', len(idx824) == 1 and idx824[0] == len(tree815_824.body) - 1, idx824)
    exec(compile(ast.fix_missing_locations(ast.Module(body=tree815_824.body[:idx824[0]], type_ignores=[])),
                 'LOCKED_TEST815_PRELUDE', 'exec'), globals())
    gate824('LOCKED_ENGINE_SYMBOLS', all(callable(globals().get(x)) for x in
            ('model_setup', 'physical_commit', 'safe_load', 'build_fusion', 'free_generate',
             'memory_seals', 'compare_seals', 'sentinel', 'release', 'numeric_rank')))
    gate824('FRESH_BANK', len(entries) == 0, len(entries))
    import torch as _torch824
    SDPA824 = _torch824.nn.functional.scaled_dot_product_attention

    # Token budget is validated BEFORE loading 72B model weights.
    tok824 = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=False)
    tok_counts824 = {cid: len(tok824.encode(body, add_special_tokens=False)) for cid, body in cards824.items()}
    gate824('TOKEN_BUDGET', all(4 <= n <= 256 for n in tok_counts824.values()),
            {'max_body_tokens': max(tok_counts824.values()), 'stage': 'TOKENIZER_PRE_MODEL'})
    del tok824

    model_setup()
    before824 = sentinel()
    gate824('FROZEN_PREFIX', P == 30, P)
    gate824('FUSION_BUDGET',
            P + MAX_STEPS824 * max(tok_counts824.values()) + 64 <= MAX_FUSED_TOKENS,
            {'max_body_tokens': max(tok_counts824.values()), 'max_fused_tokens': MAX_FUSED_TOKENS})
    for cid, body in cards824.items():
        physical_commit(cid, body)
        gate824('BODY_SHA_' + cid, entries[cid].get('body_sha256') == sha824(body))
    gate824('PHYSICAL_COUNT', len(entries) == len(cards824), len(entries))
    for cid in cards824:
        p = safe_load(entries[cid])
        gate824('RELOAD_' + cid, p['book_id'] == cid and int(p['n']) > P and
                len(p['lower']) == CUT + 1 and tuple(p['h'].shape)[-1] == H)
        del p
    release()

    # Locked numerical H3 bank from TEST815: do not call its fixed 22-card gate.
    # Same H3 tensor sampling/normalization, generalized to this experiment's size.
    bank824 = {}
    for cid in sorted(entries):
        cp = safe_load(entries[cid])
        try:
            x = cp['h'][0, P:, :].float().cpu().numpy()
            gate824('H3_NONEMPTY_' + cid, x.ndim == 2 and x.shape[0] > 8 and x.shape[1] == H)
            ix = np.linspace(0, len(x) - 1, min(96, len(x)), dtype=np.int64)
            bank824[cid] = normalized(x[ix]).T.copy()
        finally:
            del cp
    gate824('H3_BANK', len(bank824) == len(entries), len(bank824))

    def eligible824(world, arm):
        """Experimenter intervention, never inferred from answer or given to controller."""
        pool = []
        for w in worlds824:
            ids = w['ids']
            pool += [ids['first'], ids['second']]
            if arm == 'ADD_IRRELEVANT':
                pool.append(ids['decoy'])
        current = next(w for w in worlds824 if w['world'] == world)
        if arm == 'REMOVE_SECOND':
            pool.remove(current['ids']['second'])
        elif arm == 'REPLACE_SECOND':
            pool.remove(current['ids']['second'])
            pool.append(current['ids']['changed'])
        elif arm == 'NULL':
            return [NULL824]
        return pool

    def _native824_verbose(ids, prompt, tag, max_new):
        t0 = time.perf_counter()
        mem, active, fusion_steps, _ = build_fusion(ids, 'TEST824_' + tag, True)
        try:
            gate824('NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
            n = int(mem[0][0].shape[-2])
            expected = P + sum(int(entries[x]['body_tokens']) for x in ids)
            gate824('NATIVE_LENGTH_' + tag, n == expected, {'n': n, 'expected': expected})
            first = int(entries[ids[0]]['body_tokens'])
            spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                    {'B0': (P, n), 'B1': (n, n)}
            seals = memory_seals(mem)
            out = free_generate(mem, prompt, seed=None, gain=0., max_new=max_new, spans=spans)
            gate824('KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
            gate824('SDPA_RESTORED_' + tag,
                    _torch824.nn.functional.scaled_dot_product_attention is SDPA824)
            return {'raw': out['raw'], 'tokens': int(out['generated_tokens']),
                    'possibly_truncated': int(out['generated_tokens']) >= max_new,
                    'ids': list(ids), 'time_seconds': round(time.perf_counter() - t0, 3),
                    'fusion_steps': fusion_steps,
                    'cartridge_shas': [entries[x]['sha256'] for x in ids]}
        finally:
            del mem
            gc.collect()
            release()

    def native824(ids, prompt, tag, max_new):
        # Suppress repetitive engine PASS / fusion messages on notebook screen.
        # Every failed native call still exposes its captured diagnostic tail.
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                result = _native824_verbose(ids, prompt, tag, max_new)
            return result
        except BaseException:
            log824('NATIVE_FAILURE_DIAGNOSTICS', tag, capture.getvalue()[-12000:])
            raise

    def answer_prompt824(question):
        # Readout boundary only; never used to choose a physical action.
        return ('Use only mounted physical evidence. Follow directed links. '
                'If a link is missing, answer UNKNOWN. Return only the endpoint '
                'or UNKNOWN. Question: ' + question)

    # Model-native state observation: original TEST779/790 native CUT3 probe, unchanged.
    # A question is tokenized at the input boundary; NO language is generated or parsed
    # by the control loop. Only tensors, floats, and opaque cartridge IDs are used.
    gate824('NUMERICAL_PROBE_SYMBOL', callable(globals().get('observe_state')))

    def probe824(ids, question, tag):
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                mem, active, _, _ = build_fusion(ids, 'TEST824_NUM_' + tag, True)
                try:
                    gate824('NUM_NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
                    n = int(mem[0][0].shape[-2])
                    gate824('NUM_NATIVE_LENGTH_' + tag,
                            n == P + sum(int(entries[x]['body_tokens']) for x in ids))
                    first = int(entries[ids[0]]['body_tokens'])
                    spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                            {'B0': (P, n), 'B1': (n, n)}
                    seals = memory_seals(mem)
                    state, att = observe_state(mem, question, spans)
                    gate824('NUM_STATE_' + tag, state.numel() == H and
                            bool(_torch824.isfinite(state).all().item()))
                    gate824('NUM_KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
                    gate824('NUM_SDPA_' + tag,
                            _torch824.nn.functional.scaled_dot_product_attention is SDPA824)
                    vec = state.detach().float().cpu().numpy().copy()
                    return vec, att
                finally:
                    del mem
                    gc.collect()
                    release()
        except BaseException:
            log824('NUMERICAL_PROBE_FAILURE', tag, capture.getvalue()[-6000:])
            raise

    def unit824(x):
        y = np.asarray(x, dtype=np.float64).reshape(-1)
        norm = float(np.linalg.norm(y))
        if not np.isfinite(norm) or norm <= 1e-12:
            raise RuntimeError('NUMERIC_NONFINITE_OR_ZERO_STATE')
        return y / norm

    POLICIES824 = ('RETAINED_SIGNED',)

    def run_trial824(q, arm, policy):
        # Strictly blinded: no source-kind, truth labels or answer text enters the controller.
        # Both policies retain evidence; only the predeclared numerical validity gate differs.
        allowed = eligible824(q['world'], arm)
        ranked, scores = numeric_rank(q['question'], {cid: bank824[cid] for cid in allowed})
        tag = q['qid'] + '_' + arm + '_' + policy
        gate824('RANK_' + tag, len(ranked) == len(allowed) and set(ranked) == set(allowed))
        first = ranked[0]
        selected = [first]
        initial_state, _ = probe824(selected, q['question'], tag + '_INITIAL')
        reference = unit824(initial_state)
        previous = reference.copy()
        vals = np.array([float(scores[c]) for c in ranked], dtype=np.float64)
        gate824('FINITE_RANK_' + tag, bool(np.isfinite(vals).all()))
        spread = max(float(np.std(vals)), 1e-9)
        velocity = np.zeros(H, dtype=np.float64)
        changes, alignment_history, decisions, rejected = [], [], [], []
        trace = [{'step': 0, 'ids': selected[:],
                  'state_sha256': sha824(np.asarray(initial_state, dtype=np.float32).tobytes())}]
        stop_reason = None
        safety_stop = None
        for step in range(1, MAX_STEPS824 + 1):
            candidates = [c for c in ranked if c not in selected]
            if not candidates:
                stop_reason = 'CANDIDATE_EXHAUSTION'
                break
            # Retain all physically read evidence; no sliding-window eviction.
            # Signed alignment distinguishes anti-aligned from aligned H3 vectors.
            utilities = {}
            for cid in candidates:
                matrix = np.asarray(bank824[cid], dtype=np.float64)
                colnorm = np.maximum(np.linalg.norm(matrix, axis=0), 1e-12)
                sims = (previous @ matrix) / colnorm
                signed = float(np.quantile(sims, 0.75))
                rank_z = (float(scores[cid]) - float(np.mean(vals))) / spread
                derivative = float(np.dot(velocity, unit824(np.mean(matrix, axis=1)))) if np.linalg.norm(velocity) > 1e-12 else 0.0
                # Feedback disabled in both arms to isolate validity gating;
                # not presented as a port of the original layerwise DRA motor.
                feedback = 0.0
                utilities[cid] = {'signed_alignment': signed, 'rank_z': rank_z,
                                  'derivative': derivative, 'feedback': feedback,
                                  'priority': rank_z + signed + feedback}
            # Predeclared, source-blind candidate-validity gate. Both inputs are
            # numerical H3/CUT3 observations; no card kind, answer, or source text.
            # Relative cutoffs are recomputed within each trial, never tuned to labels.
            # OBSERVATION ONLY: no thresholds, rejection or new control policy.
            ordered = sorted(candidates, key=lambda c: (-utilities[c]['priority'], ranked.index(c)))
            rejected.append({'step': step, 'candidate_order': ordered,
                             'candidate_metrics': {c: dict(utilities[c]) for c in candidates},
                             'selected_before_step': selected[:],
                             'priority_gap_top2': (float(utilities[ordered[0]]['priority'] -
                                                         utilities[ordered[1]]['priority']) if len(ordered)>1 else None)})
            target = ordered[0]
            # Stability is a diagnostic stop, not an evidence-sufficiency oracle.
            if len(changes) >= 2:
                recent = np.asarray(changes[-2:], dtype=np.float64)
                baseline = max(float(np.median(changes)), 1e-12)
                if float(np.max(recent)) < 0.10 * baseline and float(np.linalg.norm(velocity)) < 0.10 * baseline:
                    stop_reason = 'RELATIVE_TENSOR_STABILITY'
                    break
            next_ids = selected + [target]
            gate824('UNIQUE_ACTIVE_' + tag + '_' + str(step), len(set(next_ids)) == len(next_ids))
            new_state, att = probe824(next_ids, q['question'], tag + '_STEP_' + str(step))
            current = unit824(new_state)
            delta = current - previous
            displacement = float(np.linalg.norm(delta))
            velocity = 0.30 * velocity + 0.70 * delta
            signed_change = float(np.dot(previous, current))
            alignment_history.append(signed_change)
            changes.append(displacement)
            gate824('FINITE_FEEDBACK_' + tag + '_' + str(step),
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
                          'state_sha256': sha824(np.asarray(new_state, dtype=np.float32).tobytes())})
            selected = next_ids
            previous = current
        if stop_reason is None:
            safety_stop = 'MAX_STEPS_SAFETY_BOUND'
        initial = {'raw': '[SKIPPED_DIAGNOSTIC_READOUT]'}
        final = native824(selected, answer_prompt824(q['question']),
                          tag + '_FINAL_READOUT', MAX_NEW_ANSWER824)
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

    for q in questions824:
        for arm in ARMS824:
            for policy in POLICIES824:
                row = run_trial824(q, arm, policy)
                D824['trials'].append(row)
                save824()
                log824('TEST824_TRIAL', row['qid'], arm, policy, 'steps', row['steps_executed'],
                       'stop', row['numeric_stop_reason'] or row['safety_stop'], 'final', repr(row['final'][:80]))

    D824['fixed_baseline'] = []  # omitted to minimize A100 runtime; TEST823 provides baseline.
    gate824('TRIAL_COUNT', len(D824['trials']) == len(questions824) * len(ARMS824) * len(POLICIES824),
            len(D824['trials']))
    gate824('FROZEN_WEIGHT_SENTINEL', before824 == sentinel())
    gate824('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    gate824('PANEL_UNCHANGED', sha824(json.dumps(PANEL824, ensure_ascii=False, sort_keys=True)) == PANEL_SHA824)
    for cid in cards824:
        gate824('FINAL_SHA_' + cid, sha_file(CART_DIR / entries[cid]['file']) == entries[cid]['sha256'])

    # Diagnostic exact-match scoring is performed OFFLINE, after all model calls.
    # The expected answer never enters native824 or run_trial824.
    lookup824 = {q['qid']: q for q in questions824}
    def exact824(ans, expected):
        return ans.strip().strip(' .\n').upper() == expected.upper()
    scored824 = []
    for r in D824['trials']:
        key = lookup824[r['qid']]
        expected = key['changed_expected'] if r['arm'] == 'REPLACE_SECOND' else key['expected']
        should_unknown = r['arm'] in ('REMOVE_SECOND', 'NULL')
        correct = (r['final'].strip().upper() == 'UNKNOWN') if should_unknown else exact824(r['final'], expected)
        scored824.append({'qid': r['qid'], 'arm': r['arm'], 'policy': r['policy'], 'expected': 'UNKNOWN' if should_unknown else expected,
                          'exact_correct': correct, 'model_stop': r['model_stop'],
                          'valid_decisions': r['valid_decisions'],
                          'controller_decisions': r['controller_decisions'],
                          'repair_attempts': r['repair_attempts'],
                          'repair_successes': r['repair_successes'],
                          'initial': r['initial'], 'final': r['final']})
    # OFFLINE ONLY. Truth metadata is never used to choose, reject, fuse, or stop.
    kind_lookup824 = {cid: m['kind'] for cid, m in card_meta824.items()}
    domain_lookup824 = {cid: m['domain'] for cid, m in card_meta824.items()}
    D824['offline_selection_diagnostics'] = []
    for row in D824['trials']:
        w = next(w for w in worlds824 if w['world'] == lookup824[row['qid']]['world'])
        ordered_kinds = [kind_lookup824.get(d['target']) for d in row['model_decisions']]
        chosen_ids = row['trace'][-1]['ids']
        D824['offline_selection_diagnostics'].append({
            'qid': row['qid'], 'arm': row['arm'],
            'initial_kind': kind_lookup824.get(row['initial_selected'][0]),
            'selected_kinds': ordered_kinds,
            'selected_own_domain': [domain_lookup824.get(cid) == w['world'] for cid in chosen_ids],
            'has_first': w['ids']['first'] in chosen_ids,
            'has_second': w['ids']['second'] in chosen_ids,
            'decoy_selected': w['ids']['decoy'] in chosen_ids,
            'final_exact_correct': next(x['exact_correct'] for x in scored824
                                        if x['qid']==row['qid'] and x['arm']==row['arm'] and x['policy']==row['policy']),
            'candidate_audit': row['validity_gate_audit']})
    D824['offline_diagnostic_summary'] = {
        arm: {'cases': sum(x['arm']==arm for x in D824['offline_selection_diagnostics']),
              'both_links_selected': sum(x['arm']==arm and x['has_first'] and x['has_second'] for x in D824['offline_selection_diagnostics']),
              'decoy_selected': sum(x['arm']==arm and x['decoy_selected'] for x in D824['offline_selection_diagnostics'])}
        for arm in ARMS824}
    D824['offline_scores'] = {
        policy: {arm: {
            'cases': sum(x['arm'] == arm and x['policy'] == policy for x in scored824),
            'exact_correct': sum(x['arm'] == arm and x['policy'] == policy and x['exact_correct'] for x in scored824),
            'numerical_stability_stops': sum(r['arm'] == arm and r['policy'] == policy and r['numeric_stop_reason'] == 'RELATIVE_TENSOR_STABILITY' for r in D824['trials']),
            'validity_abstentions': sum(r['arm'] == arm and r['policy'] == policy and r['numeric_stop_reason'] == 'NUMERIC_VALIDITY_ABSTENTION' for r in D824['trials']),
            'safety_bound_stops': sum(r['arm'] == arm and r['policy'] == policy and r['safety_stop'] == 'MAX_STEPS_SAFETY_BOUND' for r in D824['trials']),
            'mean_reads': round(sum(r['steps_executed'] for r in D824['trials'] if r['arm'] == arm and r['policy'] == policy) / len(questions824), 3)
        } for arm in ARMS824} for policy in POLICIES824}
    with REVIEW824.open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['qid', 'arm', 'policy', 'initial', 'final', 'expected', 'exact_correct', 'model_stop',
                'human_reasoning_correct_0_1', 'human_attribution_correct_0_1',
                'human_autonomous_correction_0_1', 'human_notes']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in scored824:
            writer.writerow({k: row.get(k, '') for k in cols})
    D824['review_sha256'] = sha824(REVIEW824.read_bytes())
    D824['status'] = 'COMPLETE_MECHANICAL_OFFLINE_SCORING_HUMAN_REVIEW_PENDING'
    save824()
    log824('TEST824_COMPLETED', json.dumps(D824['offline_scores']), 'SELECTION', json.dumps(D824['offline_diagnostic_summary']), OUT824, REVIEW824)
except BaseException as e:
    D824['status'] = 'ERROR'
    D824['error'] = {'repr': repr(e), 'traceback': traceback.format_exc()}
    save824()
    log824('TEST824_FAILED', repr(e), traceback.format_exc())
    raise
finally:
    gc.collect()
    if 'release' in globals() and callable(globals()['release']):
        try:
            release()
        except Exception:
            pass
    save824()
