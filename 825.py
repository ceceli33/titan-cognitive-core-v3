# AKBASCORE SILICON HIPPOCAMPUS — TEST825
# TENSOR-NUMERICAL CONTROL: CUT3 H3 observations -> feedback -> physical cartridge action.
# Built from GPU-completed TEST919 and locked TEST815 engine; no textual action controller.
# Single Colab cell; frozen Qwen2.5-72B NF4; exactly one A100 80GB.
# LOCKED TEST815 engine; no residual hooks, no source replay at read time, no training.
# TEST825: compact leave-one-cartridge-out causal tensor intervention; no new gate or textual controller.
# Numerical controller is EXPERIMENTAL; not the original DRA layer-injection motor.
# Question encoding and final answer readout remain language interfaces; control loop is numeric.
import ast, hashlib, urllib.request, json, csv, gc, time, traceback, random, re, datetime, contextlib, io
from pathlib import Path

T825 = '825'
REPO825 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCK815_825 = '77774f87428c0243c9a86ea6a041364acd9c1b03'
SEED825 = 8252026
WORLDS825 = 3
PARAPHRASES825 = 1
MAX_STEPS825 = 4                 # safety ceiling, NOT evidence of autonomous stopping
MAX_NEW_ANSWER825 = 96
MAX_NEW_CONTROL825 = 0  # no control text generated
MAX_CANDIDATES825 = 5
RUN825 = 'TEST825_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
DIR825 = (Path('/content') if Path('/content').exists() else Path('/tmp')) / RUN825
DIR825.mkdir(parents=True, exist_ok=False)
OUT825 = DIR825 / 'TEST825_results.json'
LOG825 = DIR825 / 'TEST825.log'
REVIEW825 = DIR825 / 'TEST825_blind_review.csv'
OFFLINE825 = DIR825 / 'TEST825_offline_key.json'  # never available to inference/controller

D825 = {'test': T825, 'status': 'STARTED', 'run': RUN825,
        'source815_blob': LOCK815_825, 'controller': 'RETAINED_SIGNED_LEAVE_ONE_OUT', 'checks': [], 'trials': [],
        'limitations': [
            'Control decisions are computed from H3/CUT3 tensors and numerical feedback, without generated action text.',
            'Numerical feedback is an experimental DRA-inspired audit, NOT the original DRA 1.3 layer steering.',
            'TEST825 preserves retained-signed and performs physical leave-one-out CUT3 probes and independent final readouts AFTER selection; no ablation outcome is fed to controller.',
            'Question encoding and final answer readout are boundary interfaces only; no natural-language command or generated text enters the tensor controller.',
            'Offline truth is never given to numeric_rank, free_generate, or controller.',
            'MAX_STEPS is a safety bound, not autonomous stopping.',
            'Native reads and integrity checks are distinct from semantic correctness.',
            'Synthetic two-hop relations test a narrow capability, not general scientific reasoning.',
            'No text-controller self-repair; no oracle or hardcoded answer is used by the numeric controller.',
            'No GPU execution or result is claimed by the code author.', 'Only the previously working retained-signed policy is executed; no validity gate is applied. Two post-selection physical removals per trial are diagnostic, not controller actions.', 'Numerical stability is not equivalent to epistemic sufficiency; safety stops are reported separately.', 'No DRA equivalence is claimed; this is a causal intervention audit, not stopping calibration.']}

def sha825(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()

def blob825(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def save825():
    p = Path(str(OUT825) + '.tmp')
    p.write_text(json.dumps(D825, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    p.replace(OUT825)

def log825(*args):
    msg = ' '.join(map(str, args))
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        print(msg, flush=True)
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        with LOG825.open('a', encoding='utf-8') as f:
            f.write(msg + '\n')

def gate825(name, ok, detail=None):
    D825['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail})
    save825()
    log825('PASS' if ok else 'FAIL', name, detail if detail is not None else '')
    if not ok:
        raise RuntimeError('TEST825_GATE_' + name)

# PRESEALED panel: opaque names and randomized assignments. All scoring stays offline.
RNG825 = random.Random(SEED825)
ALPH825 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

def code825():
    return ''.join(RNG825.choice(ALPH825) for _ in range(9))

worlds825 = []
seen825 = set()
for wi in range(WORLDS825):
    names = []
    while len(names) < 5:
        n = code825()
        if n not in seen825:
            seen825.add(n); names.append(n)
    worlds825.append({'world': 'DOMAIN_' + code825(), 'start': names[0],
                      'middle': names[1], 'end': names[2],
                      'changed_end': names[3], 'decoy_end': names[4]})

questions825 = []
for w in worlds825:
    for pi, fmt in enumerate((
        'In domain {world}, starting from {start}, which endpoint is reached after exactly two directed links?',
        'For {world}, follow two successive directed edges beginning at {start}. Give the final node.')[:PARAPHRASES825]):
        questions825.append({'qid': w['world'] + '_P' + str(pi), 'world': w['world'],
                             'question': fmt.format(**w), 'expected': w['end'],
                             'changed_expected': w['changed_end']})

# Each domain has two independent source cards and a deliberately irrelevant card.
# Changed source is an independently forged cartridge, never an in-place mutation.
cards825, card_meta825 = {}, {}
for w in worlds825:
    domain = w['world']
    ids = {kind: 'E825_' + code825() for kind in ('first', 'second', 'changed', 'decoy')}
    w['ids'] = ids
    cards825[ids['first']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['start'] + ' -> ' + w['middle'] + '.\n')
    cards825[ids['second']] = ('Evidence record. Domain: ' + domain + '\n' +
                             'Directed relation: ' + w['middle'] + ' -> ' + w['end'] + '.\n')
    cards825[ids['changed']] = ('Evidence record. Domain: ' + domain + '\n' +
                              'Directed relation: ' + w['middle'] + ' -> ' + w['changed_end'] + '.\n')
    cards825[ids['decoy']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['decoy_end'] + ' -> ' + w['start'] + '.\n')
    for kind, cid in ids.items():
        card_meta825[cid] = {'domain': domain, 'kind': kind, 'body_sha256': sha825(cards825[cid])}
NULL825 = 'E825_NULL'
cards825[NULL825] = 'CONTROL MEMORY. No directed relations are available.\n'
card_meta825[NULL825] = {'domain': None, 'kind': 'null', 'body_sha256': sha825(cards825[NULL825])}

# The blind controller sees candidate IDs and its own outputs, never the answer key.
# Baseline and interventions use the SAME code; only physically eligible cartridges differ.
ARMS825 = ('FULL', 'REMOVE_SECOND', 'ADD_IRRELEVANT')
PANEL825 = {'seed': SEED825, 'world_count': WORLDS825, 'paraphrases': PARAPHRASES825,
            'questions': [{'qid': q['qid'], 'question': q['question']} for q in questions825],
            'arms': ARMS825, 'policies': ['RETAINED_SIGNED'], 'limits': [MAX_STEPS825, MAX_NEW_ANSWER825, MAX_NEW_CONTROL825,
                                       MAX_CANDIDATES825], 'card_hashes': card_meta825}
PANEL_SHA825 = sha825(json.dumps(PANEL825, ensure_ascii=False, sort_keys=True))
D825['panel_sha256'] = PANEL_SHA825
D825['panel_public'] = PANEL825
OFFLINE825.write_text(json.dumps({'note': 'OFFLINE ONLY — NEVER IMPORT INTO CONTROLLER',
                                  'questions': questions825, 'worlds': worlds825},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D825['offline_key_sha256'] = sha825(OFFLINE825.read_bytes())
save825()

# The engine is imported from the EXACT locked TEST815 AST prelude, unchanged.
# The original TEST815 experiment is never executed.
try:
    log825('TEST825_START', RUN825, 'PANEL_SHA', PANEL_SHA825)
    req825 = urllib.request.Request(REPO825 + '815.py', headers={'User-Agent': 'AKBASCORE-TEST825'})
    with urllib.request.urlopen(req825, timeout=180) as f:
        raw815_825 = f.read(120001)
    gate825('LOCK815', len(raw815_825) <= 120000 and blob825(raw815_825) == LOCK815_825,
            blob825(raw815_825))
    tree815_825 = ast.parse(raw815_825.decode('utf-8'), filename='815.py')
    idx825 = [i for i, n in enumerate(tree815_825.body) if isinstance(n, ast.Try)]
    gate825('AST_BOUNDARY', len(idx825) == 1 and idx825[0] == len(tree815_825.body) - 1, idx825)
    exec(compile(ast.fix_missing_locations(ast.Module(body=tree815_825.body[:idx825[0]], type_ignores=[])),
                 'LOCKED_TEST815_PRELUDE', 'exec'), globals())
    gate825('LOCKED_ENGINE_SYMBOLS', all(callable(globals().get(x)) for x in
            ('model_setup', 'physical_commit', 'safe_load', 'build_fusion', 'free_generate',
             'memory_seals', 'compare_seals', 'sentinel', 'release', 'numeric_rank')))
    gate825('FRESH_BANK', len(entries) == 0, len(entries))
    import torch as _torch825
    SDPA825 = _torch825.nn.functional.scaled_dot_product_attention

    # Token budget is validated BEFORE loading 72B model weights.
    tok825 = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=False)
    tok_counts825 = {cid: len(tok825.encode(body, add_special_tokens=False)) for cid, body in cards825.items()}
    gate825('TOKEN_BUDGET', all(4 <= n <= 256 for n in tok_counts825.values()),
            {'max_body_tokens': max(tok_counts825.values()), 'stage': 'TOKENIZER_PRE_MODEL'})
    del tok825

    model_setup()
    before825 = sentinel()
    gate825('FROZEN_PREFIX', P == 30, P)
    gate825('FUSION_BUDGET',
            P + MAX_STEPS825 * max(tok_counts825.values()) + 64 <= MAX_FUSED_TOKENS,
            {'max_body_tokens': max(tok_counts825.values()), 'max_fused_tokens': MAX_FUSED_TOKENS})
    for cid, body in cards825.items():
        physical_commit(cid, body)
        gate825('BODY_SHA_' + cid, entries[cid].get('body_sha256') == sha825(body))
    gate825('PHYSICAL_COUNT', len(entries) == len(cards825), len(entries))
    for cid in cards825:
        p = safe_load(entries[cid])
        gate825('RELOAD_' + cid, p['book_id'] == cid and int(p['n']) > P and
                len(p['lower']) == CUT + 1 and tuple(p['h'].shape)[-1] == H)
        del p
    release()

    # Locked numerical H3 bank from TEST815: do not call its fixed 22-card gate.
    # Same H3 tensor sampling/normalization, generalized to this experiment's size.
    bank825 = {}
    for cid in sorted(entries):
        cp = safe_load(entries[cid])
        try:
            x = cp['h'][0, P:, :].float().cpu().numpy()
            gate825('H3_NONEMPTY_' + cid, x.ndim == 2 and x.shape[0] > 8 and x.shape[1] == H)
            ix = np.linspace(0, len(x) - 1, min(96, len(x)), dtype=np.int64)
            bank825[cid] = normalized(x[ix]).T.copy()
        finally:
            del cp
    gate825('H3_BANK', len(bank825) == len(entries), len(bank825))

    def eligible825(world, arm):
        """Experimenter intervention, never inferred from answer or given to controller."""
        pool = []
        for w in worlds825:
            ids = w['ids']
            pool += [ids['first'], ids['second']]
            if arm == 'ADD_IRRELEVANT':
                pool.append(ids['decoy'])
        current = next(w for w in worlds825 if w['world'] == world)
        if arm == 'REMOVE_SECOND':
            pool.remove(current['ids']['second'])
        elif arm == 'REPLACE_SECOND':
            pool.remove(current['ids']['second'])
            pool.append(current['ids']['changed'])
        elif arm == 'NULL':
            return [NULL825]
        return pool

    def _native825_verbose(ids, prompt, tag, max_new):
        t0 = time.perf_counter()
        mem, active, fusion_steps, _ = build_fusion(ids, 'TEST825_' + tag, True)
        try:
            gate825('NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
            n = int(mem[0][0].shape[-2])
            expected = P + sum(int(entries[x]['body_tokens']) for x in ids)
            gate825('NATIVE_LENGTH_' + tag, n == expected, {'n': n, 'expected': expected})
            first = int(entries[ids[0]]['body_tokens'])
            spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                    {'B0': (P, n), 'B1': (n, n)}
            seals = memory_seals(mem)
            out = free_generate(mem, prompt, seed=None, gain=0., max_new=max_new, spans=spans)
            gate825('KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
            gate825('SDPA_RESTORED_' + tag,
                    _torch825.nn.functional.scaled_dot_product_attention is SDPA825)
            return {'raw': out['raw'], 'tokens': int(out['generated_tokens']),
                    'possibly_truncated': int(out['generated_tokens']) >= max_new,
                    'ids': list(ids), 'time_seconds': round(time.perf_counter() - t0, 3),
                    'fusion_steps': fusion_steps,
                    'cartridge_shas': [entries[x]['sha256'] for x in ids]}
        finally:
            del mem
            gc.collect()
            release()

    def native825(ids, prompt, tag, max_new):
        # Suppress repetitive engine PASS / fusion messages on notebook screen.
        # Every failed native call still exposes its captured diagnostic tail.
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                result = _native825_verbose(ids, prompt, tag, max_new)
            return result
        except BaseException:
            log825('NATIVE_FAILURE_DIAGNOSTICS', tag, capture.getvalue()[-12000:])
            raise

    def answer_prompt825(question):
        # Readout boundary only; never used to choose a physical action.
        return ('Use only mounted physical evidence. Follow directed links. '
                'If a link is missing, answer UNKNOWN. Return only the endpoint '
                'or UNKNOWN. Question: ' + question)

    # Model-native state observation: original TEST779/790 native CUT3 probe, unchanged.
    # A question is tokenized at the input boundary; NO language is generated or parsed
    # by the control loop. Only tensors, floats, and opaque cartridge IDs are used.
    gate825('NUMERICAL_PROBE_SYMBOL', callable(globals().get('observe_state')))

    def probe825(ids, question, tag):
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                mem, active, _, _ = build_fusion(ids, 'TEST825_NUM_' + tag, True)
                try:
                    gate825('NUM_NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
                    n = int(mem[0][0].shape[-2])
                    gate825('NUM_NATIVE_LENGTH_' + tag,
                            n == P + sum(int(entries[x]['body_tokens']) for x in ids))
                    first = int(entries[ids[0]]['body_tokens'])
                    spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                            {'B0': (P, n), 'B1': (n, n)}
                    seals = memory_seals(mem)
                    state, att = observe_state(mem, question, spans)
                    gate825('NUM_STATE_' + tag, state.numel() == H and
                            bool(_torch825.isfinite(state).all().item()))
                    gate825('NUM_KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
                    gate825('NUM_SDPA_' + tag,
                            _torch825.nn.functional.scaled_dot_product_attention is SDPA825)
                    vec = state.detach().float().cpu().numpy().copy()
                    return vec, att
                finally:
                    del mem
                    gc.collect()
                    release()
        except BaseException:
            log825('NUMERICAL_PROBE_FAILURE', tag, capture.getvalue()[-6000:])
            raise

    def unit825(x):
        y = np.asarray(x, dtype=np.float64).reshape(-1)
        norm = float(np.linalg.norm(y))
        if not np.isfinite(norm) or norm <= 1e-12:
            raise RuntimeError('NUMERIC_NONFINITE_OR_ZERO_STATE')
        return y / norm

    POLICIES825 = ('RETAINED_SIGNED',)

    def run_trial825(q, arm, policy):
        # Strictly blinded: no source-kind, truth labels or answer text enters the controller.
        # Both policies retain evidence; only the predeclared numerical validity gate differs.
        allowed = eligible825(q['world'], arm)
        ranked, scores = numeric_rank(q['question'], {cid: bank825[cid] for cid in allowed})
        tag = q['qid'] + '_' + arm + '_' + policy
        gate825('RANK_' + tag, len(ranked) == len(allowed) and set(ranked) == set(allowed))
        first = ranked[0]
        selected = [first]
        initial_state, _ = probe825(selected, q['question'], tag + '_INITIAL')
        reference = unit825(initial_state)
        previous = reference.copy()
        vals = np.array([float(scores[c]) for c in ranked], dtype=np.float64)
        gate825('FINITE_RANK_' + tag, bool(np.isfinite(vals).all()))
        spread = max(float(np.std(vals)), 1e-9)
        velocity = np.zeros(H, dtype=np.float64)
        changes, alignment_history, decisions, rejected = [], [], [], []
        trace = [{'step': 0, 'ids': selected[:],
                  'state_sha256': sha825(np.asarray(initial_state, dtype=np.float32).tobytes())}]
        stop_reason = None
        safety_stop = None
        for step in range(1, MAX_STEPS825 + 1):
            candidates = [c for c in ranked if c not in selected]
            if not candidates:
                stop_reason = 'CANDIDATE_EXHAUSTION'
                break
            # Retain all physically read evidence; no sliding-window eviction.
            # Signed alignment distinguishes anti-aligned from aligned H3 vectors.
            utilities = {}
            for cid in candidates:
                matrix = np.asarray(bank825[cid], dtype=np.float64)
                colnorm = np.maximum(np.linalg.norm(matrix, axis=0), 1e-12)
                sims = (previous @ matrix) / colnorm
                signed = float(np.quantile(sims, 0.75))
                rank_z = (float(scores[cid]) - float(np.mean(vals))) / spread
                derivative = float(np.dot(velocity, unit825(np.mean(matrix, axis=1)))) if np.linalg.norm(velocity) > 1e-12 else 0.0
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
            gate825('UNIQUE_ACTIVE_' + tag + '_' + str(step), len(set(next_ids)) == len(next_ids))
            new_state, att = probe825(next_ids, q['question'], tag + '_STEP_' + str(step))
            current = unit825(new_state)
            delta = current - previous
            displacement = float(np.linalg.norm(delta))
            velocity = 0.30 * velocity + 0.70 * delta
            signed_change = float(np.dot(previous, current))
            alignment_history.append(signed_change)
            changes.append(displacement)
            gate825('FINITE_FEEDBACK_' + tag + '_' + str(step),
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
                          'state_sha256': sha825(np.asarray(new_state, dtype=np.float32).tobytes())})
            selected = next_ids
            previous = current
        if stop_reason is None:
            safety_stop = 'MAX_STEPS_SAFETY_BOUND'
        initial = {'raw': '[SKIPPED_DIAGNOSTIC_READOUT]'}
        final = native825(selected, answer_prompt825(q['question']),
                          tag + '_FINAL_READOUT', MAX_NEW_ANSWER825)
        # POST-SELECTION CAUSAL ABLATIONS: remove each of the first two mounted
        # physical cartridges. Identical question, frozen model, native CUT3.
        # These outputs NEVER change selection, controller state, or stop decisions.
        # IDs are opaque; no card kind, expected answer, or text is consulted.
        ablations = []
        for ab_index in range(min(2, len(selected))):
            removed = selected[ab_index]
            kept = [x for j, x in enumerate(selected) if j != ab_index]
            if not kept:
                continue
            abtag = tag + '_LOO_' + str(ab_index)
            ab_state, _ = probe825(kept, q['question'], abtag + '_STATE')
            ab_unit = unit825(ab_state)
            ab_out = native825(kept, answer_prompt825(q['question']),
                               abtag + '_READOUT', MAX_NEW_ANSWER825)
            ablations.append({'removed_id': removed, 'removed_position': ab_index,
                              'remaining_ids': kept,
                              'tensor_cosine_to_full': float(np.dot(previous, ab_unit)),
                              'tensor_l2_unit_delta': float(np.linalg.norm(previous - ab_unit)),
                              'full_final': final['raw'].strip(),
                              'ablated_final': ab_out['raw'].strip(),
                              'readout_changed': final['raw'].strip() != ab_out['raw'].strip(),
                              'readout_tokens': ab_out['tokens']})
        return {'qid': q['qid'], 'arm': arm, 'policy': policy, 'question': q['question'],
                'initial': initial['raw'].strip(), 'final': final['raw'].strip(),
                'initial_selected': [first], 'ranked_ids': ranked,
                'ranked_scores': {cid: float(scores[cid]) for cid in ranked},
                'trace': trace, 'model_decisions': decisions, 'validity_gate_audit': rejected, 'causal_ablations': ablations,
                'model_stop': False, 'numerical_stop': stop_reason in ('RELATIVE_TENSOR_STABILITY', 'NUMERIC_VALIDITY_ABSTENTION'),
                'numeric_stop_reason': stop_reason, 'safety_stop': safety_stop,
                'steps_executed': len(decisions), 'model_actions': ['NUMERIC_READ'] * len(decisions),
                'valid_decisions': len(decisions), 'first_valid_decisions': len(decisions),
                'repair_attempts': 0, 'repair_successes': 0,
                'controller_decisions': len(decisions)}

    for q in questions825:
        for arm in ARMS825:
            for policy in POLICIES825:
                row = run_trial825(q, arm, policy)
                D825['trials'].append(row)
                save825()
                log825('TEST825_TRIAL', row['qid'], arm, policy, 'steps', row['steps_executed'],
                       'stop', row['numeric_stop_reason'] or row['safety_stop'], 'final', repr(row['final'][:80]))

    D825['fixed_baseline'] = []  # omitted to minimize A100 runtime; TEST823 provides baseline.
    gate825('TRIAL_COUNT', len(D825['trials']) == len(questions825) * len(ARMS825) * len(POLICIES825),
            len(D825['trials']))
    gate825('FROZEN_WEIGHT_SENTINEL', before825 == sentinel())
    gate825('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    gate825('PANEL_UNCHANGED', sha825(json.dumps(PANEL825, ensure_ascii=False, sort_keys=True)) == PANEL_SHA825)
    for cid in cards825:
        gate825('FINAL_SHA_' + cid, sha_file(CART_DIR / entries[cid]['file']) == entries[cid]['sha256'])

    # Diagnostic exact-match scoring is performed OFFLINE, after all model calls.
    # The expected answer never enters native825 or run_trial825.
    lookup825 = {q['qid']: q for q in questions825}
    def exact825(ans, expected):
        return ans.strip().strip(' .\n').upper() == expected.upper()
    scored825 = []
    for r in D825['trials']:
        key = lookup825[r['qid']]
        expected = key['changed_expected'] if r['arm'] == 'REPLACE_SECOND' else key['expected']
        should_unknown = r['arm'] in ('REMOVE_SECOND', 'NULL')
        correct = (r['final'].strip().upper() == 'UNKNOWN') if should_unknown else exact825(r['final'], expected)
        scored825.append({'qid': r['qid'], 'arm': r['arm'], 'policy': r['policy'], 'expected': 'UNKNOWN' if should_unknown else expected,
                          'exact_correct': correct, 'model_stop': r['model_stop'],
                          'valid_decisions': r['valid_decisions'],
                          'controller_decisions': r['controller_decisions'],
                          'repair_attempts': r['repair_attempts'],
                          'repair_successes': r['repair_successes'],
                          'initial': r['initial'], 'final': r['final']})
    # OFFLINE ONLY. Truth metadata is never used to choose, reject, fuse, or stop.
    kind_lookup825 = {cid: m['kind'] for cid, m in card_meta825.items()}
    domain_lookup825 = {cid: m['domain'] for cid, m in card_meta825.items()}
    D825['offline_selection_diagnostics'] = []
    for row in D825['trials']:
        w = next(w for w in worlds825 if w['world'] == lookup825[row['qid']]['world'])
        ordered_kinds = [kind_lookup825.get(d['target']) for d in row['model_decisions']]
        chosen_ids = row['trace'][-1]['ids']
        D825['offline_selection_diagnostics'].append({
            'qid': row['qid'], 'arm': row['arm'],
            'initial_kind': kind_lookup825.get(row['initial_selected'][0]),
            'selected_kinds': ordered_kinds,
            'selected_own_domain': [domain_lookup825.get(cid) == w['world'] for cid in chosen_ids],
            'has_first': w['ids']['first'] in chosen_ids,
            'has_second': w['ids']['second'] in chosen_ids,
            'decoy_selected': w['ids']['decoy'] in chosen_ids,
            'final_exact_correct': next(x['exact_correct'] for x in scored825
                                        if x['qid']==row['qid'] and x['arm']==row['arm'] and x['policy']==row['policy']),
            'candidate_audit': row['validity_gate_audit']})
    # Source labels are added only after every physical intervention and readout.
    # No offline label is passed into the controller or the ablation routine.
    D825['offline_causal_diagnostics'] = []
    for row in D825['trials']:
        world = lookup825[row['qid']]['world']
        for ab in row['causal_ablations']:
            kind = kind_lookup825.get(ab['removed_id'])
            D825['offline_causal_diagnostics'].append({
                'qid': row['qid'], 'arm': row['arm'],
                'removed_kind': kind,
                'removed_own_domain': domain_lookup825.get(ab['removed_id']) == world,
                'tensor_cosine_to_full': ab['tensor_cosine_to_full'],
                'tensor_l2_unit_delta': ab['tensor_l2_unit_delta'],
                'readout_changed': ab['readout_changed'],
                'full_final': ab['full_final'], 'ablated_final': ab['ablated_final']})
    D825['offline_causal_summary'] = {
        arm: {'ablations': sum(x['arm']==arm for x in D825['offline_causal_diagnostics']),
              'readout_changed': sum(x['arm']==arm and x['readout_changed'] for x in D825['offline_causal_diagnostics']),
              'mean_tensor_l2_unit_delta': round(float(np.mean([x['tensor_l2_unit_delta']
                  for x in D825['offline_causal_diagnostics'] if x['arm']==arm])), 6)}
        for arm in ARMS825}
    D825['offline_diagnostic_summary'] = {
        arm: {'cases': sum(x['arm']==arm for x in D825['offline_selection_diagnostics']),
              'both_links_selected': sum(x['arm']==arm and x['has_first'] and x['has_second'] for x in D825['offline_selection_diagnostics']),
              'decoy_selected': sum(x['arm']==arm and x['decoy_selected'] for x in D825['offline_selection_diagnostics'])}
        for arm in ARMS825}
    D825['offline_scores'] = {
        policy: {arm: {
            'cases': sum(x['arm'] == arm and x['policy'] == policy for x in scored825),
            'exact_correct': sum(x['arm'] == arm and x['policy'] == policy and x['exact_correct'] for x in scored825),
            'numerical_stability_stops': sum(r['arm'] == arm and r['policy'] == policy and r['numeric_stop_reason'] == 'RELATIVE_TENSOR_STABILITY' for r in D825['trials']),
            'validity_abstentions': sum(r['arm'] == arm and r['policy'] == policy and r['numeric_stop_reason'] == 'NUMERIC_VALIDITY_ABSTENTION' for r in D825['trials']),
            'safety_bound_stops': sum(r['arm'] == arm and r['policy'] == policy and r['safety_stop'] == 'MAX_STEPS_SAFETY_BOUND' for r in D825['trials']),
            'mean_reads': round(sum(r['steps_executed'] for r in D825['trials'] if r['arm'] == arm and r['policy'] == policy) / len(questions825), 3)
        } for arm in ARMS825} for policy in POLICIES825}
    with REVIEW825.open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['qid', 'arm', 'policy', 'initial', 'final', 'expected', 'exact_correct', 'model_stop',
                'human_reasoning_correct_0_1', 'human_attribution_correct_0_1',
                'human_autonomous_correction_0_1', 'human_notes']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in scored825:
            writer.writerow({k: row.get(k, '') for k in cols})
    D825['review_sha256'] = sha825(REVIEW825.read_bytes())
    D825['status'] = 'COMPLETE_MECHANICAL_OFFLINE_SCORING_HUMAN_REVIEW_PENDING'
    save825()
    log825('TEST825_COMPLETED', json.dumps(D825['offline_scores']), 'SELECTION', json.dumps(D825['offline_diagnostic_summary']), 'CAUSAL', json.dumps(D825['offline_causal_summary']), OUT825, REVIEW825)
except BaseException as e:
    D825['status'] = 'ERROR'
    D825['error'] = {'repr': repr(e), 'traceback': traceback.format_exc()}
    save825()
    log825('TEST825_FAILED', repr(e), traceback.format_exc())
    raise
finally:
    gc.collect()
    if 'release' in globals() and callable(globals()['release']):
        try:
            release()
        except Exception:
            pass
    save825()
