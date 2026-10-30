# AKBASCORE SILICON HIPPOCAMPUS — TEST826
# TENSOR-NUMERICAL CONTROL: CUT3 H3 observations -> feedback -> physical cartridge action.
# Built from GPU-completed TEST919 and locked TEST815 engine; no textual action controller.
# Single Colab cell; frozen Qwen2.5-72B NF4; exactly one A100 80GB.
# LOCKED TEST815 engine; no residual hooks, no source replay at read time, no training.
# TEST826: DRA-inspired damped oscillator shadow observer; no control intervention.
# Numerical controller is EXPERIMENTAL; not the original DRA layer-injection motor.
# Question encoding and final answer readout remain language interfaces; control loop is numeric.
import ast, hashlib, urllib.request, json, csv, gc, time, traceback, random, re, datetime, contextlib, io
from pathlib import Path

T826 = '826'
REPO826 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCK815_826 = '77774f87428c0243c9a86ea6a041364acd9c1b03'
SEED826 = 8262026
WORLDS826 = 3
PARAPHRASES826 = 1
MAX_STEPS826 = 4                 # safety ceiling, NOT evidence of autonomous stopping
MAX_NEW_ANSWER826 = 96
MAX_NEW_CONTROL826 = 0  # no control text generated
MAX_CANDIDATES826 = 5
RUN826 = 'TEST826_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
DIR826 = (Path('/content') if Path('/content').exists() else Path('/tmp')) / RUN826
DIR826.mkdir(parents=True, exist_ok=False)
OUT826 = DIR826 / 'TEST826_results.json'
LOG826 = DIR826 / 'TEST826.log'
REVIEW826 = DIR826 / 'TEST826_blind_review.csv'
OFFLINE826 = DIR826 / 'TEST826_offline_key.json'  # never available to inference/controller

D826 = {'test': T826, 'status': 'STARTED', 'run': RUN826,
        'source815_blob': LOCK815_826, 'controller': 'RETAINED_SIGNED_DRA_SHADOW', 'checks': [], 'trials': [],
        'limitations': [
            'Control decisions are computed from H3/CUT3 tensors and numerical feedback, without generated action text.',
            'Numerical feedback is an experimental DRA-inspired audit, NOT the original DRA 1.3 layer steering.',
            'TEST826 preserves retained-signed and performs physical leave-one-out CUT3 probes and independent final readouts AFTER selection; no ablation outcome is fed to controller.',
            'Question encoding and final answer readout are boundary interfaces only; no natural-language command or generated text enters the tensor controller.',
            'Offline truth is never given to numeric_rank, free_generate, or controller.',
            'MAX_STEPS is a safety bound, not autonomous stopping.',
            'Native reads and integrity checks are distinct from semantic correctness.',
            'Synthetic two-hop relations test a narrow capability, not general scientific reasoning.',
            'No text-controller self-repair; no oracle or hardcoded answer is used by the numeric controller.',
            'No GPU execution or result is claimed by the code author.', 'Only the previously working retained-signed policy is executed; no validity gate is applied. No additional ablation passes; shadow observer uses existing CUT3 probes.', 'Numerical stability is not equivalent to epistemic sufficiency; safety stops are reported separately.', 'This is a DRA-inspired shadow observer, not a port of original hook-based DRA steering.']}

def sha826(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()

def blob826(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def save826():
    p = Path(str(OUT826) + '.tmp')
    p.write_text(json.dumps(D826, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    p.replace(OUT826)

def log826(*args):
    msg = ' '.join(map(str, args))
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        print(msg, flush=True)
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        with LOG826.open('a', encoding='utf-8') as f:
            f.write(msg + '\n')

def gate826(name, ok, detail=None):
    D826['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail})
    save826()
    log826('PASS' if ok else 'FAIL', name, detail if detail is not None else '')
    if not ok:
        raise RuntimeError('TEST826_GATE_' + name)

# PRESEALED panel: opaque names and randomized assignments. All scoring stays offline.
RNG826 = random.Random(SEED826)
ALPH826 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

def code826():
    return ''.join(RNG826.choice(ALPH826) for _ in range(9))

worlds826 = []
seen826 = set()
for wi in range(WORLDS826):
    names = []
    while len(names) < 5:
        n = code826()
        if n not in seen826:
            seen826.add(n); names.append(n)
    worlds826.append({'world': 'DOMAIN_' + code826(), 'start': names[0],
                      'middle': names[1], 'end': names[2],
                      'changed_end': names[3], 'decoy_end': names[4]})

questions826 = []
for w in worlds826:
    for pi, fmt in enumerate((
        'In domain {world}, starting from {start}, which endpoint is reached after exactly two directed links?',
        'For {world}, follow two successive directed edges beginning at {start}. Give the final node.')[:PARAPHRASES826]):
        questions826.append({'qid': w['world'] + '_P' + str(pi), 'world': w['world'],
                             'question': fmt.format(**w), 'expected': w['end'],
                             'changed_expected': w['changed_end']})

# Each domain has two independent source cards and a deliberately irrelevant card.
# Changed source is an independently forged cartridge, never an in-place mutation.
cards826, card_meta826 = {}, {}
for w in worlds826:
    domain = w['world']
    ids = {kind: 'E826_' + code826() for kind in ('first', 'second', 'changed', 'decoy')}
    w['ids'] = ids
    cards826[ids['first']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['start'] + ' -> ' + w['middle'] + '.\n')
    cards826[ids['second']] = ('Evidence record. Domain: ' + domain + '\n' +
                             'Directed relation: ' + w['middle'] + ' -> ' + w['end'] + '.\n')
    cards826[ids['changed']] = ('Evidence record. Domain: ' + domain + '\n' +
                              'Directed relation: ' + w['middle'] + ' -> ' + w['changed_end'] + '.\n')
    cards826[ids['decoy']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['decoy_end'] + ' -> ' + w['start'] + '.\n')
    for kind, cid in ids.items():
        card_meta826[cid] = {'domain': domain, 'kind': kind, 'body_sha256': sha826(cards826[cid])}
NULL826 = 'E826_NULL'
cards826[NULL826] = 'CONTROL MEMORY. No directed relations are available.\n'
card_meta826[NULL826] = {'domain': None, 'kind': 'null', 'body_sha256': sha826(cards826[NULL826])}

# The blind controller sees candidate IDs and its own outputs, never the answer key.
# Baseline and interventions use the SAME code; only physically eligible cartridges differ.
ARMS826 = ('FULL', 'REMOVE_SECOND', 'ADD_IRRELEVANT')
PANEL826 = {'seed': SEED826, 'world_count': WORLDS826, 'paraphrases': PARAPHRASES826,
            'questions': [{'qid': q['qid'], 'question': q['question']} for q in questions826],
            'arms': ARMS826, 'policies': ['RETAINED_SIGNED'], 'limits': [MAX_STEPS826, MAX_NEW_ANSWER826, MAX_NEW_CONTROL826,
                                       MAX_CANDIDATES826], 'card_hashes': card_meta826}
PANEL_SHA826 = sha826(json.dumps(PANEL826, ensure_ascii=False, sort_keys=True))
D826['panel_sha256'] = PANEL_SHA826
D826['panel_public'] = PANEL826
OFFLINE826.write_text(json.dumps({'note': 'OFFLINE ONLY — NEVER IMPORT INTO CONTROLLER',
                                  'questions': questions826, 'worlds': worlds826},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D826['offline_key_sha256'] = sha826(OFFLINE826.read_bytes())
save826()

# The engine is imported from the EXACT locked TEST815 AST prelude, unchanged.
# The original TEST815 experiment is never executed.
try:
    log826('TEST826_START', RUN826, 'PANEL_SHA', PANEL_SHA826)
    req826 = urllib.request.Request(REPO826 + '815.py', headers={'User-Agent': 'AKBASCORE-TEST826'})
    with urllib.request.urlopen(req826, timeout=180) as f:
        raw815_826 = f.read(120001)
    gate826('LOCK815', len(raw815_826) <= 120000 and blob826(raw815_826) == LOCK815_826,
            blob826(raw815_826))
    tree815_826 = ast.parse(raw815_826.decode('utf-8'), filename='815.py')
    idx826 = [i for i, n in enumerate(tree815_826.body) if isinstance(n, ast.Try)]
    gate826('AST_BOUNDARY', len(idx826) == 1 and idx826[0] == len(tree815_826.body) - 1, idx826)
    exec(compile(ast.fix_missing_locations(ast.Module(body=tree815_826.body[:idx826[0]], type_ignores=[])),
                 'LOCKED_TEST815_PRELUDE', 'exec'), globals())
    gate826('LOCKED_ENGINE_SYMBOLS', all(callable(globals().get(x)) for x in
            ('model_setup', 'physical_commit', 'safe_load', 'build_fusion', 'free_generate',
             'memory_seals', 'compare_seals', 'sentinel', 'release', 'numeric_rank')))
    gate826('FRESH_BANK', len(entries) == 0, len(entries))
    import torch as _torch826
    SDPA826 = _torch826.nn.functional.scaled_dot_product_attention

    # Token budget is validated BEFORE loading 72B model weights.
    tok826 = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=False)
    tok_counts826 = {cid: len(tok826.encode(body, add_special_tokens=False)) for cid, body in cards826.items()}
    gate826('TOKEN_BUDGET', all(4 <= n <= 256 for n in tok_counts826.values()),
            {'max_body_tokens': max(tok_counts826.values()), 'stage': 'TOKENIZER_PRE_MODEL'})
    del tok826

    model_setup()
    before826 = sentinel()
    gate826('FROZEN_PREFIX', P == 30, P)
    gate826('FUSION_BUDGET',
            P + MAX_STEPS826 * max(tok_counts826.values()) + 64 <= MAX_FUSED_TOKENS,
            {'max_body_tokens': max(tok_counts826.values()), 'max_fused_tokens': MAX_FUSED_TOKENS})
    for cid, body in cards826.items():
        physical_commit(cid, body)
        gate826('BODY_SHA_' + cid, entries[cid].get('body_sha256') == sha826(body))
    gate826('PHYSICAL_COUNT', len(entries) == len(cards826), len(entries))
    for cid in cards826:
        p = safe_load(entries[cid])
        gate826('RELOAD_' + cid, p['book_id'] == cid and int(p['n']) > P and
                len(p['lower']) == CUT + 1 and tuple(p['h'].shape)[-1] == H)
        del p
    release()

    # Locked numerical H3 bank from TEST815: do not call its fixed 22-card gate.
    # Same H3 tensor sampling/normalization, generalized to this experiment's size.
    bank826 = {}
    for cid in sorted(entries):
        cp = safe_load(entries[cid])
        try:
            x = cp['h'][0, P:, :].float().cpu().numpy()
            gate826('H3_NONEMPTY_' + cid, x.ndim == 2 and x.shape[0] > 8 and x.shape[1] == H)
            ix = np.linspace(0, len(x) - 1, min(96, len(x)), dtype=np.int64)
            bank826[cid] = normalized(x[ix]).T.copy()
        finally:
            del cp
    gate826('H3_BANK', len(bank826) == len(entries), len(bank826))

    def eligible826(world, arm):
        """Experimenter intervention, never inferred from answer or given to controller."""
        pool = []
        for w in worlds826:
            ids = w['ids']
            pool += [ids['first'], ids['second']]
            if arm == 'ADD_IRRELEVANT':
                pool.append(ids['decoy'])
        current = next(w for w in worlds826 if w['world'] == world)
        if arm == 'REMOVE_SECOND':
            pool.remove(current['ids']['second'])
        elif arm == 'REPLACE_SECOND':
            pool.remove(current['ids']['second'])
            pool.append(current['ids']['changed'])
        elif arm == 'NULL':
            return [NULL826]
        return pool

    def _native826_verbose(ids, prompt, tag, max_new):
        t0 = time.perf_counter()
        mem, active, fusion_steps, _ = build_fusion(ids, 'TEST826_' + tag, True)
        try:
            gate826('NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
            n = int(mem[0][0].shape[-2])
            expected = P + sum(int(entries[x]['body_tokens']) for x in ids)
            gate826('NATIVE_LENGTH_' + tag, n == expected, {'n': n, 'expected': expected})
            first = int(entries[ids[0]]['body_tokens'])
            spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                    {'B0': (P, n), 'B1': (n, n)}
            seals = memory_seals(mem)
            out = free_generate(mem, prompt, seed=None, gain=0., max_new=max_new, spans=spans)
            gate826('KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
            gate826('SDPA_RESTORED_' + tag,
                    _torch826.nn.functional.scaled_dot_product_attention is SDPA826)
            return {'raw': out['raw'], 'tokens': int(out['generated_tokens']),
                    'possibly_truncated': int(out['generated_tokens']) >= max_new,
                    'ids': list(ids), 'time_seconds': round(time.perf_counter() - t0, 3),
                    'fusion_steps': fusion_steps,
                    'cartridge_shas': [entries[x]['sha256'] for x in ids]}
        finally:
            del mem
            gc.collect()
            release()

    def native826(ids, prompt, tag, max_new):
        # Suppress repetitive engine PASS / fusion messages on notebook screen.
        # Every failed native call still exposes its captured diagnostic tail.
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                result = _native826_verbose(ids, prompt, tag, max_new)
            return result
        except BaseException:
            log826('NATIVE_FAILURE_DIAGNOSTICS', tag, capture.getvalue()[-12000:])
            raise

    def answer_prompt826(question):
        # Readout boundary only; never used to choose a physical action.
        return ('Use only mounted physical evidence. Follow directed links. '
                'If a link is missing, answer UNKNOWN. Return only the endpoint '
                'or UNKNOWN. Question: ' + question)

    # Model-native state observation: original TEST779/790 native CUT3 probe, unchanged.
    # A question is tokenized at the input boundary; NO language is generated or parsed
    # by the control loop. Only tensors, floats, and opaque cartridge IDs are used.
    gate826('NUMERICAL_PROBE_SYMBOL', callable(globals().get('observe_state')))

    def probe826(ids, question, tag):
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                mem, active, _, _ = build_fusion(ids, 'TEST826_NUM_' + tag, True)
                try:
                    gate826('NUM_NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
                    n = int(mem[0][0].shape[-2])
                    gate826('NUM_NATIVE_LENGTH_' + tag,
                            n == P + sum(int(entries[x]['body_tokens']) for x in ids))
                    first = int(entries[ids[0]]['body_tokens'])
                    spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                            {'B0': (P, n), 'B1': (n, n)}
                    seals = memory_seals(mem)
                    state, att = observe_state(mem, question, spans)
                    gate826('NUM_STATE_' + tag, state.numel() == H and
                            bool(_torch826.isfinite(state).all().item()))
                    gate826('NUM_KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
                    gate826('NUM_SDPA_' + tag,
                            _torch826.nn.functional.scaled_dot_product_attention is SDPA826)
                    vec = state.detach().float().cpu().numpy().copy()
                    return vec, att
                finally:
                    del mem
                    gc.collect()
                    release()
        except BaseException:
            log826('NUMERICAL_PROBE_FAILURE', tag, capture.getvalue()[-6000:])
            raise

    def unit826(x):
        y = np.asarray(x, dtype=np.float64).reshape(-1)
        norm = float(np.linalg.norm(y))
        if not np.isfinite(norm) or norm <= 1e-12:
            raise RuntimeError('NUMERIC_NONFINITE_OR_ZERO_STATE')
        return y / norm

    POLICIES826 = ('RETAINED_SIGNED',)

    def run_trial826(q, arm, policy):
        # Strictly blinded: no source-kind, truth labels or answer text enters the controller.
        # Both policies retain evidence; only the predeclared numerical validity gate differs.
        allowed = eligible826(q['world'], arm)
        ranked, scores = numeric_rank(q['question'], {cid: bank826[cid] for cid in allowed})
        tag = q['qid'] + '_' + arm + '_' + policy
        gate826('RANK_' + tag, len(ranked) == len(allowed) and set(ranked) == set(allowed))
        first = ranked[0]
        selected = [first]
        initial_state, _ = probe826(selected, q['question'], tag + '_INITIAL')
        reference = unit826(initial_state)
        previous = reference.copy()
        vals = np.array([float(scores[c]) for c in ranked], dtype=np.float64)
        gate826('FINITE_RANK_' + tag, bool(np.isfinite(vals).all()))
        spread = max(float(np.std(vals)), 1e-9)
        velocity = np.zeros(H, dtype=np.float64)
        osc_x = reference.copy()
        osc_v = np.zeros(H, dtype=np.float64)
        osc_history = []
        osc_gamma, osc_stiffness, osc_drive = 0.30, 0.12, 0.30
        changes, alignment_history, decisions, rejected = [], [], [], []
        trace = [{'step': 0, 'ids': selected[:],
                  'state_sha256': sha826(np.asarray(initial_state, dtype=np.float32).tobytes())}]
        stop_reason = None
        safety_stop = None
        for step in range(1, MAX_STEPS826 + 1):
            candidates = [c for c in ranked if c not in selected]
            if not candidates:
                stop_reason = 'CANDIDATE_EXHAUSTION'
                break
            # Retain all physically read evidence; no sliding-window eviction.
            # Signed alignment distinguishes anti-aligned from aligned H3 vectors.
            utilities = {}
            for cid in candidates:
                matrix = np.asarray(bank826[cid], dtype=np.float64)
                colnorm = np.maximum(np.linalg.norm(matrix, axis=0), 1e-12)
                sims = (previous @ matrix) / colnorm
                signed = float(np.quantile(sims, 0.75))
                rank_z = (float(scores[cid]) - float(np.mean(vals))) / spread
                derivative = float(np.dot(velocity, unit826(np.mean(matrix, axis=1)))) if np.linalg.norm(velocity) > 1e-12 else 0.0
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
            gate826('UNIQUE_ACTIVE_' + tag + '_' + str(step), len(set(next_ids)) == len(next_ids))
            new_state, att = probe826(next_ids, q['question'], tag + '_STEP_' + str(step))
            current = unit826(new_state)
            # DRA-inspired second-order shadow; never affects model, rank or stopping.
            osc_force = osc_drive * (current - previous) - osc_stiffness * (osc_x - current)
            osc_v = (1.0 - osc_gamma) * osc_v + osc_force
            osc_x = osc_x + osc_v
            osc_error = float(np.linalg.norm(osc_x - current))
            osc_speed = float(np.linalg.norm(osc_v))
            osc_energy = float(0.5 * osc_speed**2 + 0.5 * osc_stiffness * osc_error**2)
            osc_history.append({'step': step, 'velocity_norm': osc_speed,
                                'tracking_error': osc_error,
                                'drive_norm': float(np.linalg.norm(current - previous)),
                                'energy': osc_energy,
                                'energy_delta': osc_energy - osc_history[-1]['energy'] if osc_history else None})
            gate826('DRA_SHADOW_FINITE_' + tag + '_' + str(step),
                    bool(np.isfinite(osc_energy) and np.isfinite(osc_speed) and np.isfinite(osc_error)))
            delta = current - previous
            displacement = float(np.linalg.norm(delta))
            velocity = 0.30 * velocity + 0.70 * delta
            signed_change = float(np.dot(previous, current))
            alignment_history.append(signed_change)
            changes.append(displacement)
            gate826('FINITE_FEEDBACK_' + tag + '_' + str(step),
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
                          'state_sha256': sha826(np.asarray(new_state, dtype=np.float32).tobytes())})
            selected = next_ids
            previous = current
        if stop_reason is None:
            safety_stop = 'MAX_STEPS_SAFETY_BOUND'
        initial = {'raw': '[SKIPPED_DIAGNOSTIC_READOUT]'}
        final = native826(selected, answer_prompt826(q['question']),
                          tag + '_FINAL_READOUT', MAX_NEW_ANSWER826)
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

    for q in questions826:
        for arm in ARMS826:
            for policy in POLICIES826:
                row = run_trial826(q, arm, policy)
                D826['trials'].append(row)
                save826()
                log826('TEST826_TRIAL', row['qid'], arm, policy, 'steps', row['steps_executed'],
                       'stop', row['numeric_stop_reason'] or row['safety_stop'], 'final', repr(row['final'][:80]))

    D826['fixed_baseline'] = []  # omitted to minimize A100 runtime; TEST823 provides baseline.
    gate826('TRIAL_COUNT', len(D826['trials']) == len(questions826) * len(ARMS826) * len(POLICIES826),
            len(D826['trials']))
    gate826('FROZEN_WEIGHT_SENTINEL', before826 == sentinel())
    gate826('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    gate826('PANEL_UNCHANGED', sha826(json.dumps(PANEL826, ensure_ascii=False, sort_keys=True)) == PANEL_SHA826)
    for cid in cards826:
        gate826('FINAL_SHA_' + cid, sha_file(CART_DIR / entries[cid]['file']) == entries[cid]['sha256'])

    # Diagnostic exact-match scoring is performed OFFLINE, after all model calls.
    # The expected answer never enters native826 or run_trial826.
    lookup826 = {q['qid']: q for q in questions826}
    def exact826(ans, expected):
        return ans.strip().strip(' .\n').upper() == expected.upper()
    scored826 = []
    for r in D826['trials']:
        key = lookup826[r['qid']]
        expected = key['changed_expected'] if r['arm'] == 'REPLACE_SECOND' else key['expected']
        should_unknown = r['arm'] in ('REMOVE_SECOND', 'NULL')
        correct = (r['final'].strip().upper() == 'UNKNOWN') if should_unknown else exact826(r['final'], expected)
        scored826.append({'qid': r['qid'], 'arm': r['arm'], 'policy': r['policy'], 'expected': 'UNKNOWN' if should_unknown else expected,
                          'exact_correct': correct, 'model_stop': r['model_stop'],
                          'valid_decisions': r['valid_decisions'],
                          'controller_decisions': r['controller_decisions'],
                          'repair_attempts': r['repair_attempts'],
                          'repair_successes': r['repair_successes'],
                          'initial': r['initial'], 'final': r['final']})
    # OFFLINE ONLY. Truth metadata is never used to choose, reject, fuse, or stop.
    kind_lookup826 = {cid: m['kind'] for cid, m in card_meta826.items()}
    domain_lookup826 = {cid: m['domain'] for cid, m in card_meta826.items()}
    D826['offline_selection_diagnostics'] = []
    for row in D826['trials']:
        w = next(w for w in worlds826 if w['world'] == lookup826[row['qid']]['world'])
        ordered_kinds = [kind_lookup826.get(d['target']) for d in row['model_decisions']]
        chosen_ids = row['trace'][-1]['ids']
        D826['offline_selection_diagnostics'].append({
            'qid': row['qid'], 'arm': row['arm'],
            'initial_kind': kind_lookup826.get(row['initial_selected'][0]),
            'selected_kinds': ordered_kinds,
            'selected_own_domain': [domain_lookup826.get(cid) == w['world'] for cid in chosen_ids],
            'has_first': w['ids']['first'] in chosen_ids,
            'has_second': w['ids']['second'] in chosen_ids,
            'decoy_selected': w['ids']['decoy'] in chosen_ids,
            'final_exact_correct': next(x['exact_correct'] for x in scored826
                                        if x['qid']==row['qid'] and x['arm']==row['arm'] and x['policy']==row['policy']),
            'candidate_audit': row['validity_gate_audit']})
    # Offline diagnostic only; labels are not passed into oscillator.
    D826['offline_dra_summary'] = {}
    for arm in ARMS826:
        rr = [r for r in D826['trials'] if r['arm'] == arm]
        final = [r['dra_shadow'][-1] for r in rr if r['dra_shadow']]
        D826['offline_dra_summary'][arm] = {
            'cases': len(rr),
            'mean_final_energy': round(float(np.mean([x['energy'] for x in final])), 8),
            'mean_final_speed': round(float(np.mean([x['velocity_norm'] for x in final])), 8),
            'mean_final_tracking_error': round(float(np.mean([x['tracking_error'] for x in final])), 8),
            'energy_declined_last_step': sum(len(r['dra_shadow']) >= 2 and
                r['dra_shadow'][-1]['energy'] < r['dra_shadow'][-2]['energy'] for r in rr)}
    D826['offline_causal_diagnostics'] = []
    D826['offline_causal_summary'] = {'status': 'NOT_RUN'}
    D826['offline_diagnostic_summary'] = {
        arm: {'cases': sum(x['arm']==arm for x in D826['offline_selection_diagnostics']),
              'both_links_selected': sum(x['arm']==arm and x['has_first'] and x['has_second'] for x in D826['offline_selection_diagnostics']),
              'decoy_selected': sum(x['arm']==arm and x['decoy_selected'] for x in D826['offline_selection_diagnostics'])}
        for arm in ARMS826}
    D826['offline_scores'] = {
        policy: {arm: {
            'cases': sum(x['arm'] == arm and x['policy'] == policy for x in scored826),
            'exact_correct': sum(x['arm'] == arm and x['policy'] == policy and x['exact_correct'] for x in scored826),
            'numerical_stability_stops': sum(r['arm'] == arm and r['policy'] == policy and r['numeric_stop_reason'] == 'RELATIVE_TENSOR_STABILITY' for r in D826['trials']),
            'validity_abstentions': sum(r['arm'] == arm and r['policy'] == policy and r['numeric_stop_reason'] == 'NUMERIC_VALIDITY_ABSTENTION' for r in D826['trials']),
            'safety_bound_stops': sum(r['arm'] == arm and r['policy'] == policy and r['safety_stop'] == 'MAX_STEPS_SAFETY_BOUND' for r in D826['trials']),
            'mean_reads': round(sum(r['steps_executed'] for r in D826['trials'] if r['arm'] == arm and r['policy'] == policy) / len(questions826), 3)
        } for arm in ARMS826} for policy in POLICIES826}
    with REVIEW826.open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['qid', 'arm', 'policy', 'initial', 'final', 'expected', 'exact_correct', 'model_stop',
                'human_reasoning_correct_0_1', 'human_attribution_correct_0_1',
                'human_autonomous_correction_0_1', 'human_notes']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in scored826:
            writer.writerow({k: row.get(k, '') for k in cols})
    D826['review_sha256'] = sha826(REVIEW826.read_bytes())
    D826['status'] = 'COMPLETE_MECHANICAL_OFFLINE_SCORING_HUMAN_REVIEW_PENDING'
    save826()
    log826('TEST826_COMPLETED', json.dumps(D826['offline_scores']), 'SELECTION', json.dumps(D826['offline_diagnostic_summary']), 'DRA_SHADOW', json.dumps(D826['offline_dra_summary']), OUT826, REVIEW826)
except BaseException as e:
    D826['status'] = 'ERROR'
    D826['error'] = {'repr': repr(e), 'traceback': traceback.format_exc()}
    save826()
    log826('TEST826_FAILED', repr(e), traceback.format_exc())
    raise
finally:
    gc.collect()
    if 'release' in globals() and callable(globals()['release']):
        try:
            release()
        except Exception:
            pass
    save826()
