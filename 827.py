# AKBASCORE SILICON HIPPOCAMPUS — TEST827
# TENSOR-NUMERICAL CONTROL: CUT3 H3 observations -> feedback -> physical cartridge action.
# Built from GPU-completed TEST826 and locked TEST815 engine; no textual action controller.
# Single Colab cell; frozen Qwen2.5-72B NF4; exactly one A100 80GB.
# LOCKED TEST815 engine; no residual hooks, no source replay at read time, no training.
# TEST827: DRA trajectory and direction audit; no control intervention.
# Numerical controller is EXPERIMENTAL; not the original DRA layer-injection motor.
# Question encoding and final answer readout remain language interfaces; control loop is numeric.
import ast, hashlib, urllib.request, json, csv, gc, time, traceback, random, re, datetime, contextlib, io
from pathlib import Path

T827 = '827'
REPO827 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCK815_827 = '77774f87428c0243c9a86ea6a041364acd9c1b03'
SEED827 = 8272026
WORLDS827 = 3
PARAPHRASES827 = 1
MAX_STEPS827 = 4                 # safety ceiling, NOT evidence of autonomous stopping
MAX_NEW_ANSWER827 = 96
MAX_NEW_CONTROL827 = 0  # no control text generated
MAX_CANDIDATES827 = 5
RUN827 = 'TEST827_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
DIR827 = (Path('/content') if Path('/content').exists() else Path('/tmp')) / RUN827
DIR827.mkdir(parents=True, exist_ok=False)
OUT827 = DIR827 / 'TEST827_results.json'
LOG827 = DIR827 / 'TEST827.log'
REVIEW827 = DIR827 / 'TEST827_blind_review.csv'
OFFLINE827 = DIR827 / 'TEST827_offline_key.json'  # never available to inference/controller

D827 = {'test': T827, 'status': 'STARTED', 'run': RUN827,
        'source815_blob': LOCK815_827, 'controller': 'RETAINED_SIGNED_DRA_TRAJECTORY_SHADOW', 'checks': [], 'trials': [],
        'limitations': [
            'Control decisions are computed from H3/CUT3 tensors and numerical feedback, without generated action text.',
            'Numerical feedback is an experimental DRA-inspired audit, NOT the original DRA 1.3 layer steering.',
            'TEST827 preserves retained-signed and observes DRA velocity, force, direction and energy trajectories; no extra ablation probes and no observation controls stopping.',
            'Question encoding and final answer readout are boundary interfaces only; no natural-language command or generated text enters the tensor controller.',
            'Offline truth is never given to numeric_rank, free_generate, or controller.',
            'MAX_STEPS is a safety bound, not autonomous stopping.',
            'Native reads and integrity checks are distinct from semantic correctness.',
            'Synthetic two-hop relations test a narrow capability, not general scientific reasoning.',
            'No text-controller self-repair; no oracle or hardcoded answer is used by the numeric controller.',
            'No GPU execution or result is claimed by the code author.', 'Only the previously working retained-signed policy is executed; no validity gate is applied. No additional ablation passes; shadow observer uses existing CUT3 probes.', 'Numerical stability is not equivalent to epistemic sufficiency; safety stops are reported separately.', 'This is a DRA-inspired shadow observer, not a port of original hook-based DRA steering.']}

def sha827(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()

def blob827(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def save827():
    p = Path(str(OUT827) + '.tmp')
    p.write_text(json.dumps(D827, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    p.replace(OUT827)

def log827(*args):
    msg = ' '.join(map(str, args))
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        print(msg, flush=True)
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        with LOG827.open('a', encoding='utf-8') as f:
            f.write(msg + '\n')

def gate827(name, ok, detail=None):
    D827['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail})
    save827()
    log827('PASS' if ok else 'FAIL', name, detail if detail is not None else '')
    if not ok:
        raise RuntimeError('TEST827_GATE_' + name)

# PRESEALED panel: opaque names and randomized assignments. All scoring stays offline.
RNG827 = random.Random(SEED827)
ALPH827 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

def code827():
    return ''.join(RNG827.choice(ALPH827) for _ in range(9))

worlds827 = []
seen827 = set()
for wi in range(WORLDS827):
    names = []
    while len(names) < 5:
        n = code827()
        if n not in seen827:
            seen827.add(n); names.append(n)
    worlds827.append({'world': 'DOMAIN_' + code827(), 'start': names[0],
                      'middle': names[1], 'end': names[2],
                      'changed_end': names[3], 'decoy_end': names[4]})

questions827 = []
for w in worlds827:
    for pi, fmt in enumerate((
        'In domain {world}, starting from {start}, which endpoint is reached after exactly two directed links?',
        'For {world}, follow two successive directed edges beginning at {start}. Give the final node.')[:PARAPHRASES827]):
        questions827.append({'qid': w['world'] + '_P' + str(pi), 'world': w['world'],
                             'question': fmt.format(**w), 'expected': w['end'],
                             'changed_expected': w['changed_end']})

# Each domain has two independent source cards and a deliberately irrelevant card.
# Changed source is an independently forged cartridge, never an in-place mutation.
cards827, card_meta827 = {}, {}
for w in worlds827:
    domain = w['world']
    ids = {kind: 'E827_' + code827() for kind in ('first', 'second', 'changed', 'decoy')}
    w['ids'] = ids
    cards827[ids['first']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['start'] + ' -> ' + w['middle'] + '.\n')
    cards827[ids['second']] = ('Evidence record. Domain: ' + domain + '\n' +
                             'Directed relation: ' + w['middle'] + ' -> ' + w['end'] + '.\n')
    cards827[ids['changed']] = ('Evidence record. Domain: ' + domain + '\n' +
                              'Directed relation: ' + w['middle'] + ' -> ' + w['changed_end'] + '.\n')
    cards827[ids['decoy']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['decoy_end'] + ' -> ' + w['start'] + '.\n')
    for kind, cid in ids.items():
        card_meta827[cid] = {'domain': domain, 'kind': kind, 'body_sha256': sha827(cards827[cid])}
NULL827 = 'E827_NULL'
cards827[NULL827] = 'CONTROL MEMORY. No directed relations are available.\n'
card_meta827[NULL827] = {'domain': None, 'kind': 'null', 'body_sha256': sha827(cards827[NULL827])}

# The blind controller sees candidate IDs and its own outputs, never the answer key.
# Baseline and interventions use the SAME code; only physically eligible cartridges differ.
ARMS827 = ('FULL', 'REMOVE_SECOND', 'ADD_IRRELEVANT')
PANEL827 = {'seed': SEED827, 'world_count': WORLDS827, 'paraphrases': PARAPHRASES827,
            'questions': [{'qid': q['qid'], 'question': q['question']} for q in questions827],
            'arms': ARMS827, 'policies': ['RETAINED_SIGNED'], 'limits': [MAX_STEPS827, MAX_NEW_ANSWER827, MAX_NEW_CONTROL827,
                                       MAX_CANDIDATES827], 'card_hashes': card_meta827}
PANEL_SHA827 = sha827(json.dumps(PANEL827, ensure_ascii=False, sort_keys=True))
D827['panel_sha256'] = PANEL_SHA827
D827['panel_public'] = PANEL827
OFFLINE827.write_text(json.dumps({'note': 'OFFLINE ONLY — NEVER IMPORT INTO CONTROLLER',
                                  'questions': questions827, 'worlds': worlds827},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D827['offline_key_sha256'] = sha827(OFFLINE827.read_bytes())
save827()

# The engine is imported from the EXACT locked TEST815 AST prelude, unchanged.
# The original TEST815 experiment is never executed.
try:
    log827('TEST827_START', RUN827, 'PANEL_SHA', PANEL_SHA827)
    req827 = urllib.request.Request(REPO827 + '815.py', headers={'User-Agent': 'AKBASCORE-TEST827'})
    with urllib.request.urlopen(req827, timeout=180) as f:
        raw815_827 = f.read(120001)
    gate827('LOCK815', len(raw815_827) <= 120000 and blob827(raw815_827) == LOCK815_827,
            blob827(raw815_827))
    tree815_827 = ast.parse(raw815_827.decode('utf-8'), filename='815.py')
    idx827 = [i for i, n in enumerate(tree815_827.body) if isinstance(n, ast.Try)]
    gate827('AST_BOUNDARY', len(idx827) == 1 and idx827[0] == len(tree815_827.body) - 1, idx827)
    exec(compile(ast.fix_missing_locations(ast.Module(body=tree815_827.body[:idx827[0]], type_ignores=[])),
                 'LOCKED_TEST815_PRELUDE', 'exec'), globals())
    gate827('LOCKED_ENGINE_SYMBOLS', all(callable(globals().get(x)) for x in
            ('model_setup', 'physical_commit', 'safe_load', 'build_fusion', 'free_generate',
             'memory_seals', 'compare_seals', 'sentinel', 'release', 'numeric_rank')))
    gate827('FRESH_BANK', len(entries) == 0, len(entries))
    import torch as _torch827
    SDPA827 = _torch827.nn.functional.scaled_dot_product_attention

    # Token budget is validated BEFORE loading 72B model weights.
    tok827 = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=False)
    tok_counts827 = {cid: len(tok827.encode(body, add_special_tokens=False)) for cid, body in cards827.items()}
    gate827('TOKEN_BUDGET', all(4 <= n <= 256 for n in tok_counts827.values()),
            {'max_body_tokens': max(tok_counts827.values()), 'stage': 'TOKENIZER_PRE_MODEL'})
    del tok827

    model_setup()
    before827 = sentinel()
    gate827('FROZEN_PREFIX', P == 30, P)
    gate827('FUSION_BUDGET',
            P + MAX_STEPS827 * max(tok_counts827.values()) + 64 <= MAX_FUSED_TOKENS,
            {'max_body_tokens': max(tok_counts827.values()), 'max_fused_tokens': MAX_FUSED_TOKENS})
    for cid, body in cards827.items():
        physical_commit(cid, body)
        gate827('BODY_SHA_' + cid, entries[cid].get('body_sha256') == sha827(body))
    gate827('PHYSICAL_COUNT', len(entries) == len(cards827), len(entries))
    for cid in cards827:
        p = safe_load(entries[cid])
        gate827('RELOAD_' + cid, p['book_id'] == cid and int(p['n']) > P and
                len(p['lower']) == CUT + 1 and tuple(p['h'].shape)[-1] == H)
        del p
    release()

    # Locked numerical H3 bank from TEST815: do not call its fixed 22-card gate.
    # Same H3 tensor sampling/normalization, generalized to this experiment's size.
    bank827 = {}
    for cid in sorted(entries):
        cp = safe_load(entries[cid])
        try:
            x = cp['h'][0, P:, :].float().cpu().numpy()
            gate827('H3_NONEMPTY_' + cid, x.ndim == 2 and x.shape[0] > 8 and x.shape[1] == H)
            ix = np.linspace(0, len(x) - 1, min(96, len(x)), dtype=np.int64)
            bank827[cid] = normalized(x[ix]).T.copy()
        finally:
            del cp
    gate827('H3_BANK', len(bank827) == len(entries), len(bank827))

    def eligible827(world, arm):
        """Experimenter intervention, never inferred from answer or given to controller."""
        pool = []
        for w in worlds827:
            ids = w['ids']
            pool += [ids['first'], ids['second']]
            if arm == 'ADD_IRRELEVANT':
                pool.append(ids['decoy'])
        current = next(w for w in worlds827 if w['world'] == world)
        if arm == 'REMOVE_SECOND':
            pool.remove(current['ids']['second'])
        elif arm == 'REPLACE_SECOND':
            pool.remove(current['ids']['second'])
            pool.append(current['ids']['changed'])
        elif arm == 'NULL':
            return [NULL827]
        return pool

    def _native827_verbose(ids, prompt, tag, max_new):
        t0 = time.perf_counter()
        mem, active, fusion_steps, _ = build_fusion(ids, 'TEST827_' + tag, True)
        try:
            gate827('NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
            n = int(mem[0][0].shape[-2])
            expected = P + sum(int(entries[x]['body_tokens']) for x in ids)
            gate827('NATIVE_LENGTH_' + tag, n == expected, {'n': n, 'expected': expected})
            first = int(entries[ids[0]]['body_tokens'])
            spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                    {'B0': (P, n), 'B1': (n, n)}
            seals = memory_seals(mem)
            out = free_generate(mem, prompt, seed=None, gain=0., max_new=max_new, spans=spans)
            gate827('KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
            gate827('SDPA_RESTORED_' + tag,
                    _torch827.nn.functional.scaled_dot_product_attention is SDPA827)
            return {'raw': out['raw'], 'tokens': int(out['generated_tokens']),
                    'possibly_truncated': int(out['generated_tokens']) >= max_new,
                    'ids': list(ids), 'time_seconds': round(time.perf_counter() - t0, 3),
                    'fusion_steps': fusion_steps,
                    'cartridge_shas': [entries[x]['sha256'] for x in ids]}
        finally:
            del mem
            gc.collect()
            release()

    def native827(ids, prompt, tag, max_new):
        # Suppress repetitive engine PASS / fusion messages on notebook screen.
        # Every failed native call still exposes its captured diagnostic tail.
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                result = _native827_verbose(ids, prompt, tag, max_new)
            return result
        except BaseException:
            log827('NATIVE_FAILURE_DIAGNOSTICS', tag, capture.getvalue()[-12000:])
            raise

    def answer_prompt827(question):
        # Readout boundary only; never used to choose a physical action.
        return ('Use only mounted physical evidence. Follow directed links. '
                'If a link is missing, answer UNKNOWN. Return only the endpoint '
                'or UNKNOWN. Question: ' + question)

    # Model-native state observation: original TEST779/790 native CUT3 probe, unchanged.
    # A question is tokenized at the input boundary; NO language is generated or parsed
    # by the control loop. Only tensors, floats, and opaque cartridge IDs are used.
    gate827('NUMERICAL_PROBE_SYMBOL', callable(globals().get('observe_state')))

    def probe827(ids, question, tag):
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                mem, active, _, _ = build_fusion(ids, 'TEST827_NUM_' + tag, True)
                try:
                    gate827('NUM_NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
                    n = int(mem[0][0].shape[-2])
                    gate827('NUM_NATIVE_LENGTH_' + tag,
                            n == P + sum(int(entries[x]['body_tokens']) for x in ids))
                    first = int(entries[ids[0]]['body_tokens'])
                    spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                            {'B0': (P, n), 'B1': (n, n)}
                    seals = memory_seals(mem)
                    state, att = observe_state(mem, question, spans)
                    gate827('NUM_STATE_' + tag, state.numel() == H and
                            bool(_torch827.isfinite(state).all().item()))
                    gate827('NUM_KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
                    gate827('NUM_SDPA_' + tag,
                            _torch827.nn.functional.scaled_dot_product_attention is SDPA827)
                    vec = state.detach().float().cpu().numpy().copy()
                    return vec, att
                finally:
                    del mem
                    gc.collect()
                    release()
        except BaseException:
            log827('NUMERICAL_PROBE_FAILURE', tag, capture.getvalue()[-6000:])
            raise

    def unit827(x):
        y = np.asarray(x, dtype=np.float64).reshape(-1)
        norm = float(np.linalg.norm(y))
        if not np.isfinite(norm) or norm <= 1e-12:
            raise RuntimeError('NUMERIC_NONFINITE_OR_ZERO_STATE')
        return y / norm

    POLICIES827 = ('RETAINED_SIGNED',)

    def run_trial827(q, arm, policy):
        # Strictly blinded: no source-kind, truth labels or answer text enters the controller.
        # Both policies retain evidence; only the predeclared numerical validity gate differs.
        allowed = eligible827(q['world'], arm)
        ranked, scores = numeric_rank(q['question'], {cid: bank827[cid] for cid in allowed})
        tag = q['qid'] + '_' + arm + '_' + policy
        gate827('RANK_' + tag, len(ranked) == len(allowed) and set(ranked) == set(allowed))
        first = ranked[0]
        selected = [first]
        initial_state, _ = probe827(selected, q['question'], tag + '_INITIAL')
        reference = unit827(initial_state)
        previous = reference.copy()
        vals = np.array([float(scores[c]) for c in ranked], dtype=np.float64)
        gate827('FINITE_RANK_' + tag, bool(np.isfinite(vals).all()))
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
                  'state_sha256': sha827(np.asarray(initial_state, dtype=np.float32).tobytes())}]
        stop_reason = None
        safety_stop = None
        for step in range(1, MAX_STEPS827 + 1):
            candidates = [c for c in ranked if c not in selected]
            if not candidates:
                stop_reason = 'CANDIDATE_EXHAUSTION'
                break
            # Retain all physically read evidence; no sliding-window eviction.
            # Signed alignment distinguishes anti-aligned from aligned H3 vectors.
            utilities = {}
            for cid in candidates:
                matrix = np.asarray(bank827[cid], dtype=np.float64)
                colnorm = np.maximum(np.linalg.norm(matrix, axis=0), 1e-12)
                sims = (previous @ matrix) / colnorm
                signed = float(np.quantile(sims, 0.75))
                rank_z = (float(scores[cid]) - float(np.mean(vals))) / spread
                derivative = float(np.dot(velocity, unit827(np.mean(matrix, axis=1)))) if np.linalg.norm(velocity) > 1e-12 else 0.0
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
            gate827('UNIQUE_ACTIVE_' + tag + '_' + str(step), len(set(next_ids)) == len(next_ids))
            new_state, att = probe827(next_ids, q['question'], tag + '_STEP_' + str(step))
            current = unit827(new_state)
            # DRA-inspired second-order shadow; never affects model, rank or stopping.
            osc_force = osc_drive * (current - previous) - osc_stiffness * (osc_x - current)
            osc_v = (1.0 - osc_gamma) * osc_v + osc_force
            # Angular reversal and force/velocity work: direction-aware, not just norm.
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
            gate827('DRA_SHADOW_FINITE_' + tag + '_' + str(step),
                    bool(np.isfinite(osc_energy) and np.isfinite(osc_speed) and np.isfinite(osc_error)))
            delta = current - previous
            displacement = float(np.linalg.norm(delta))
            velocity = 0.30 * velocity + 0.70 * delta
            signed_change = float(np.dot(previous, current))
            alignment_history.append(signed_change)
            changes.append(displacement)
            gate827('FINITE_FEEDBACK_' + tag + '_' + str(step),
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
                          'state_sha256': sha827(np.asarray(new_state, dtype=np.float32).tobytes())})
            selected = next_ids
            previous = current
        if stop_reason is None:
            safety_stop = 'MAX_STEPS_SAFETY_BOUND'
        initial = {'raw': '[SKIPPED_DIAGNOSTIC_READOUT]'}
        final = native827(selected, answer_prompt827(q['question']),
                          tag + '_FINAL_READOUT', MAX_NEW_ANSWER827)
        ablations = []  # Omitted: no extra GPU forward passes.
        return {'qid': q['qid'], 'arm': arm, 'policy': policy, 'question': q['question'],
                'initial': initial['raw'].strip(), 'final': final['raw'].strip(),
                'initial_selected': [first], 'ranked_ids': ranked,
                'ranked_scores': {cid: float(scores[cid]) for cid in ranked},
                'trace': trace, 'model_decisions': decisions, 'validity_gate_audit': rejected, 'causal_ablations': ablations, 'dra_shadow': osc_history,
                'model_stop': False, 'numerical_stop': stop_reason in ('RELATIVE_TENSOR_STABILITY', 'NUMERIC_VALIDITY_ABSTENTION'),
                'numeric_stop_reason': stop_reason, 'safety_stop': safety_stop,
                'steps_executed': len(decisions), 'model_actions': ['NUMERIC_READ'] * len(decisions),
                'valid_decisions': len(decisions), 'first_valid_decisions': len(decisions),
                'repair_attempts': 0, 'repair_successes': 0,
                'controller_decisions': len(decisions)}

    for q in questions827:
        for arm in ARMS827:
            for policy in POLICIES827:
                row = run_trial827(q, arm, policy)
                D827['trials'].append(row)
                save827()
                log827('TEST827_TRIAL', row['qid'], arm, policy, 'steps', row['steps_executed'],
                       'stop', row['numeric_stop_reason'] or row['safety_stop'], 'final', repr(row['final'][:80]))

    D827['fixed_baseline'] = []  # omitted to minimize A100 runtime; TEST823 provides baseline.
    gate827('TRIAL_COUNT', len(D827['trials']) == len(questions827) * len(ARMS827) * len(POLICIES827),
            len(D827['trials']))
    gate827('FROZEN_WEIGHT_SENTINEL', before827 == sentinel())
    gate827('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    gate827('PANEL_UNCHANGED', sha827(json.dumps(PANEL827, ensure_ascii=False, sort_keys=True)) == PANEL_SHA827)
    for cid in cards827:
        gate827('FINAL_SHA_' + cid, sha_file(CART_DIR / entries[cid]['file']) == entries[cid]['sha256'])

    # Diagnostic exact-match scoring is performed OFFLINE, after all model calls.
    # The expected answer never enters native827 or run_trial827.
    lookup827 = {q['qid']: q for q in questions827}
    def exact827(ans, expected):
        return ans.strip().strip(' .\n').upper() == expected.upper()
    scored827 = []
    for r in D827['trials']:
        key = lookup827[r['qid']]
        expected = key['changed_expected'] if r['arm'] == 'REPLACE_SECOND' else key['expected']
        should_unknown = r['arm'] in ('REMOVE_SECOND', 'NULL')
        correct = (r['final'].strip().upper() == 'UNKNOWN') if should_unknown else exact827(r['final'], expected)
        scored827.append({'qid': r['qid'], 'arm': r['arm'], 'policy': r['policy'], 'expected': 'UNKNOWN' if should_unknown else expected,
                          'exact_correct': correct, 'model_stop': r['model_stop'],
                          'valid_decisions': r['valid_decisions'],
                          'controller_decisions': r['controller_decisions'],
                          'repair_attempts': r['repair_attempts'],
                          'repair_successes': r['repair_successes'],
                          'initial': r['initial'], 'final': r['final']})
    # OFFLINE ONLY. Truth metadata is never used to choose, reject, fuse, or stop.
    kind_lookup827 = {cid: m['kind'] for cid, m in card_meta827.items()}
    domain_lookup827 = {cid: m['domain'] for cid, m in card_meta827.items()}
    D827['offline_selection_diagnostics'] = []
    for row in D827['trials']:
        w = next(w for w in worlds827 if w['world'] == lookup827[row['qid']]['world'])
        ordered_kinds = [kind_lookup827.get(d['target']) for d in row['model_decisions']]
        chosen_ids = row['trace'][-1]['ids']
        D827['offline_selection_diagnostics'].append({
            'qid': row['qid'], 'arm': row['arm'],
            'initial_kind': kind_lookup827.get(row['initial_selected'][0]),
            'selected_kinds': ordered_kinds,
            'selected_own_domain': [domain_lookup827.get(cid) == w['world'] for cid in chosen_ids],
            'has_first': w['ids']['first'] in chosen_ids,
            'has_second': w['ids']['second'] in chosen_ids,
            'decoy_selected': w['ids']['decoy'] in chosen_ids,
            'final_exact_correct': next(x['exact_correct'] for x in scored827
                                        if x['qid']==row['qid'] and x['arm']==row['arm'] and x['policy']==row['policy']),
            'candidate_audit': row['validity_gate_audit']})
    # Offline diagnostic only; labels are not passed into oscillator.
    D827['offline_dra_summary'] = {}
    for arm in ARMS827:
        rr = [r for r in D827['trials'] if r['arm'] == arm]
        final = [r['dra_shadow'][-1] for r in rr if r['dra_shadow']]
        D827['offline_dra_summary'][arm] = {
            'cases': len(rr),
            'mean_final_energy': round(float(np.mean([x['energy'] for x in final])), 8),
            'mean_final_speed': round(float(np.mean([x['velocity_norm'] for x in final])), 8),
            'mean_final_tracking_error': round(float(np.mean([x['tracking_error'] for x in final])), 8),
            'energy_declined_last_step': sum(len(r['dra_shadow']) >= 2 and
                r['dra_shadow'][-1]['energy'] < r['dra_shadow'][-2]['energy'] for r in rr),
            'mean_step_energy': [round(float(np.mean([r['dra_shadow'][i]['energy'] for r in rr])), 8)
                                 for i in range(MAX_STEPS827)],
            'mean_step_speed': [round(float(np.mean([r['dra_shadow'][i]['velocity_norm'] for r in rr])), 8)
                                for i in range(MAX_STEPS827)],
            'mean_step_drive': [round(float(np.mean([r['dra_shadow'][i]['drive_norm'] for r in rr])), 8)
                                for i in range(MAX_STEPS827)],
            'mean_final_force_work': round(float(np.mean([x['force_work'] for x in final])), 8),
            'mean_final_turn_cosine': round(float(np.mean([x['velocity_turn_cosine'] for x in final])), 8),
            'last_two_energy_decreasing': sum(len(r['dra_shadow']) >= 3 and
                r['dra_shadow'][-1]['energy'] < r['dra_shadow'][-2]['energy'] < r['dra_shadow'][-3]['energy']
                for r in rr)}
    D827['offline_paired_trajectory'] = []
    for q in questions827:
        byarm = {r['arm']: r for r in D827['trials'] if r['qid'] == q['qid']}
        if len(byarm) != len(ARMS827):
            continue
        def trajectory(r):
            return [float(x['energy']) for x in r['dra_shadow']]
        full = trajectory(byarm['FULL'])
        missing = trajectory(byarm['REMOVE_SECOND'])
        decoy = trajectory(byarm['ADD_IRRELEVANT'])
        D827['offline_paired_trajectory'].append({
            'qid': q['qid'], 'full_energy': full, 'missing_energy': missing,
            'decoy_energy': decoy,
            'missing_minus_full_last': missing[-1]-full[-1],
            'decoy_minus_full_last': decoy[-1]-full[-1],
            'missing_minus_full_auc': float(np.sum(np.asarray(missing)-np.asarray(full))),
            'decoy_minus_full_auc': float(np.sum(np.asarray(decoy)-np.asarray(full)))})
    D827['offline_causal_diagnostics'] = []
    D827['offline_causal_summary'] = {'status': 'NOT_RUN'}
    D827['offline_diagnostic_summary'] = {
        arm: {'cases': sum(x['arm']==arm for x in D827['offline_selection_diagnostics']),
              'both_links_selected': sum(x['arm']==arm and x['has_first'] and x['has_second'] for x in D827['offline_selection_diagnostics']),
              'decoy_selected': sum(x['arm']==arm and x['decoy_selected'] for x in D827['offline_selection_diagnostics'])}
        for arm in ARMS827}
    D827['offline_scores'] = {
        policy: {arm: {
            'cases': sum(x['arm'] == arm and x['policy'] == policy for x in scored827),
            'exact_correct': sum(x['arm'] == arm and x['policy'] == policy and x['exact_correct'] for x in scored827),
            'numerical_stability_stops': sum(r['arm'] == arm and r['policy'] == policy and r['numeric_stop_reason'] == 'RELATIVE_TENSOR_STABILITY' for r in D827['trials']),
            'validity_abstentions': sum(r['arm'] == arm and r['policy'] == policy and r['numeric_stop_reason'] == 'NUMERIC_VALIDITY_ABSTENTION' for r in D827['trials']),
            'safety_bound_stops': sum(r['arm'] == arm and r['policy'] == policy and r['safety_stop'] == 'MAX_STEPS_SAFETY_BOUND' for r in D827['trials']),
            'mean_reads': round(sum(r['steps_executed'] for r in D827['trials'] if r['arm'] == arm and r['policy'] == policy) / len(questions827), 3)
        } for arm in ARMS827} for policy in POLICIES827}
    with REVIEW827.open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['qid', 'arm', 'policy', 'initial', 'final', 'expected', 'exact_correct', 'model_stop',
                'human_reasoning_correct_0_1', 'human_attribution_correct_0_1',
                'human_autonomous_correction_0_1', 'human_notes']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in scored827:
            writer.writerow({k: row.get(k, '') for k in cols})
    D827['review_sha256'] = sha827(REVIEW827.read_bytes())
    D827['status'] = 'COMPLETE_MECHANICAL_OFFLINE_SCORING_HUMAN_REVIEW_PENDING'
    save827()
    log827('TEST827_COMPLETED', json.dumps(D827['offline_scores']), 'SELECTION', json.dumps(D827['offline_diagnostic_summary']), 'DRA_SHADOW', json.dumps(D827['offline_dra_summary']), 'PAIRED_TRAJECTORY', json.dumps(D827['offline_paired_trajectory']), OUT827, REVIEW827)
except BaseException as e:
    D827['status'] = 'ERROR'
    D827['error'] = {'repr': repr(e), 'traceback': traceback.format_exc()}
    save827()
    log827('TEST827_FAILED', repr(e), traceback.format_exc())
    raise
finally:
    gc.collect()
    if 'release' in globals() and callable(globals()['release']):
        try:
            release()
        except Exception:
            pass
    save827()
