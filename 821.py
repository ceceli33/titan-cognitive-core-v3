# AKBASCORE SILICON HIPPOCAMPUS — TEST821
# TENSOR-NUMERICAL CONTROL: CUT3 H3 observations -> feedback -> physical cartridge action.
# Built from GPU-completed TEST919 and locked TEST815 engine; no textual action controller.
# Single Colab cell; frozen Qwen2.5-72B NF4; exactly one A100 80GB.
# LOCKED TEST815 engine; no residual hooks, no source replay at read time, no training.
# TEST821: numerical evidence competition / interference audit; no textual control.
# Numerical controller is EXPERIMENTAL; not the original DRA layer-injection motor.
# Question encoding and final answer readout remain language interfaces; control loop is numeric.
import ast, hashlib, urllib.request, json, csv, gc, time, traceback, random, re, datetime, contextlib, io
from pathlib import Path

T821 = '821'
REPO821 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCK815_821 = '77774f87428c0243c9a86ea6a041364acd9c1b03'
SEED821 = 8212026
WORLDS821 = 8
PARAPHRASES821 = 3
MAX_STEPS821 = 4                 # safety ceiling, NOT evidence of autonomous stopping
MAX_NEW_ANSWER821 = 96
MAX_NEW_CONTROL821 = 0  # no control text generated
MAX_CANDIDATES821 = 5
RUN821 = 'TEST821_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
DIR821 = (Path('/content') if Path('/content').exists() else Path('/tmp')) / RUN821
DIR821.mkdir(parents=True, exist_ok=False)
OUT821 = DIR821 / 'TEST821_results.json'
LOG821 = DIR821 / 'TEST821.log'
REVIEW821 = DIR821 / 'TEST821_blind_review.csv'
OFFLINE821 = DIR821 / 'TEST821_offline_key.json'  # never available to inference/controller

D821 = {'test': T821, 'status': 'STARTED', 'run': RUN821,
        'source815_blob': LOCK815_821, 'controller': 'NUMERIC_CUT3_H3_CAUSAL_AUDIT', 'checks': [], 'trials': [],
        'limitations': [
            'Control decisions are computed from H3/CUT3 tensors and numerical feedback, without generated action text.',
            'Numerical control is an experimental interface, NOT verified DRA 1.3 layer steering.',
            'TEST821 compares tensor-state-guided selection with H3-rank-only and causal decoy exposure.',
            'Question tokenization and final readout remain linguistic boundary interfaces.',
            'Offline truth is never given to numeric_rank, free_generate, or controller.',
            'MAX_STEPS is a safety bound, not autonomous stopping.',
            'Native reads and integrity checks are distinct from semantic correctness.',
            'Synthetic two-hop relations test a narrow capability, not general scientific reasoning.',
            'No text-controller self-repair; no oracle or hardcoded answer is used by the numeric controller.',
            'No GPU execution or result is claimed by the code author.']}

def sha821(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()

def blob821(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def save821():
    p = Path(str(OUT821) + '.tmp')
    p.write_text(json.dumps(D821, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    p.replace(OUT821)

def log821(*args):
    msg = ' '.join(map(str, args))
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        print(msg, flush=True)
    if not (msg.startswith('PASS ') and any(k in msg for k in ('FILE_SHA_', 'CARTRIDGE_ID_', 'CARTRIDGE_TENSOR_SHA_', 'NATIVE_INIT_', 'NATIVE_LENGTH_', 'NATIVE80_', 'KV_SEAL_', 'SDPA_RESTORED_', 'RELOAD_', 'H3_NONEMPTY_', 'BODY_SHA_', 'RANK_', 'FINAL_SHA_'))):
        with LOG821.open('a', encoding='utf-8') as f:
            f.write(msg + '\n')

def gate821(name, ok, detail=None):
    D821['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail})
    save821()
    log821('PASS' if ok else 'FAIL', name, detail if detail is not None else '')
    if not ok:
        raise RuntimeError('TEST821_GATE_' + name)

# PRESEALED panel: opaque names and randomized assignments. All scoring stays offline.
RNG821 = random.Random(SEED821)
ALPH821 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

def code821():
    return ''.join(RNG821.choice(ALPH821) for _ in range(9))

worlds821 = []
seen821 = set()
for wi in range(WORLDS821):
    names = []
    while len(names) < 5:
        n = code821()
        if n not in seen821:
            seen821.add(n); names.append(n)
    worlds821.append({'world': 'DOMAIN_' + code821(), 'start': names[0],
                      'middle': names[1], 'end': names[2],
                      'changed_end': names[3], 'decoy_end': names[4]})

questions821 = []
for w in worlds821:
    for pi, fmt in enumerate((
        'In domain {world}, starting from {start}, which endpoint is reached after exactly two directed links?',
        'For {world}, follow two successive directed edges beginning at {start}. Give the final node.',
        'Within {world}, what is the two-step destination of {start}? Do not guess when a link is absent.')):
        questions821.append({'qid': w['world'] + '_P' + str(pi), 'world': w['world'],
                             'question': fmt.format(**w), 'expected': w['end'],
                             'changed_expected': w['changed_end']})

# Each domain has two independent source cards and a deliberately irrelevant card.
# Changed source is an independently forged cartridge, never an in-place mutation.
cards821, card_meta821 = {}, {}
for w in worlds821:
    domain = w['world']
    ids = {kind: 'E821_' + code821() for kind in ('first', 'second', 'changed', 'decoy')}
    w['ids'] = ids
    cards821[ids['first']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['start'] + ' -> ' + w['middle'] + '.\n')
    cards821[ids['second']] = ('Evidence record. Domain: ' + domain + '\n' +
                             'Directed relation: ' + w['middle'] + ' -> ' + w['end'] + '.\n')
    cards821[ids['changed']] = ('Evidence record. Domain: ' + domain + '\n' +
                              'Directed relation: ' + w['middle'] + ' -> ' + w['changed_end'] + '.\n')
    cards821[ids['decoy']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['decoy_end'] + ' -> ' + w['start'] + '.\n')
    for kind, cid in ids.items():
        card_meta821[cid] = {'domain': domain, 'kind': kind, 'body_sha256': sha821(cards821[cid])}
NULL821 = 'E821_NULL'
cards821[NULL821] = 'CONTROL MEMORY. No directed relations are available.\n'
card_meta821[NULL821] = {'domain': None, 'kind': 'null', 'body_sha256': sha821(cards821[NULL821])}

# The blind controller sees candidate IDs and its own outputs, never the answer key.
# Baseline and interventions use the SAME code; only physically eligible cartridges differ.
ARMS821 = ('FULL', 'REMOVE_SECOND', 'REPLACE_SECOND', 'ADD_IRRELEVANT', 'NULL')
PANEL821 = {'seed': SEED821, 'world_count': WORLDS821, 'paraphrases': PARAPHRASES821,
            'questions': [{'qid': q['qid'], 'question': q['question']} for q in questions821],
            'arms': ARMS821, 'limits': [MAX_STEPS821, MAX_NEW_ANSWER821, MAX_NEW_CONTROL821,
                                       MAX_CANDIDATES821], 'card_hashes': card_meta821}
PANEL_SHA821 = sha821(json.dumps(PANEL821, ensure_ascii=False, sort_keys=True))
D821['panel_sha256'] = PANEL_SHA821
D821['panel_public'] = PANEL821
OFFLINE821.write_text(json.dumps({'note': 'OFFLINE ONLY — NEVER IMPORT INTO CONTROLLER',
                                  'questions': questions821, 'worlds': worlds821},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D821['offline_key_sha256'] = sha821(OFFLINE821.read_bytes())
save821()

# The engine is imported from the EXACT locked TEST815 AST prelude, unchanged.
# The original TEST815 experiment is never executed.
try:
    log821('TEST821_START', RUN821, 'PANEL_SHA', PANEL_SHA821)
    req821 = urllib.request.Request(REPO821 + '815.py', headers={'User-Agent': 'AKBASCORE-TEST821'})
    with urllib.request.urlopen(req821, timeout=180) as f:
        raw815_821 = f.read(120001)
    gate821('LOCK815', len(raw815_821) <= 120000 and blob821(raw815_821) == LOCK815_821,
            blob821(raw815_821))
    tree815_821 = ast.parse(raw815_821.decode('utf-8'), filename='815.py')
    idx821 = [i for i, n in enumerate(tree815_821.body) if isinstance(n, ast.Try)]
    gate821('AST_BOUNDARY', len(idx821) == 1 and idx821[0] == len(tree815_821.body) - 1, idx821)
    exec(compile(ast.fix_missing_locations(ast.Module(body=tree815_821.body[:idx821[0]], type_ignores=[])),
                 'LOCKED_TEST815_PRELUDE', 'exec'), globals())
    gate821('LOCKED_ENGINE_SYMBOLS', all(callable(globals().get(x)) for x in
            ('model_setup', 'physical_commit', 'safe_load', 'build_fusion', 'free_generate',
             'memory_seals', 'compare_seals', 'sentinel', 'release', 'numeric_rank')))
    gate821('FRESH_BANK', len(entries) == 0, len(entries))
    import torch as _torch821
    SDPA821 = _torch821.nn.functional.scaled_dot_product_attention

    # Token budget is validated BEFORE loading 72B model weights.
    tok821 = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=False)
    tok_counts821 = {cid: len(tok821.encode(body, add_special_tokens=False)) for cid, body in cards821.items()}
    gate821('TOKEN_BUDGET', all(4 <= n <= 256 for n in tok_counts821.values()),
            {'max_body_tokens': max(tok_counts821.values()), 'stage': 'TOKENIZER_PRE_MODEL'})
    del tok821

    model_setup()
    before821 = sentinel()
    gate821('FROZEN_PREFIX', P == 30, P)
    gate821('FUSION_BUDGET',
            P + 2 * max(tok_counts821.values()) + 64 <= MAX_FUSED_TOKENS,
            {'max_body_tokens': max(tok_counts821.values()), 'max_fused_tokens': MAX_FUSED_TOKENS})
    for cid, body in cards821.items():
        physical_commit(cid, body)
        gate821('BODY_SHA_' + cid, entries[cid].get('body_sha256') == sha821(body))
    gate821('PHYSICAL_COUNT', len(entries) == len(cards821), len(entries))
    for cid in cards821:
        p = safe_load(entries[cid])
        gate821('RELOAD_' + cid, p['book_id'] == cid and int(p['n']) > P and
                len(p['lower']) == CUT + 1 and tuple(p['h'].shape)[-1] == H)
        del p
    release()

    # Locked numerical H3 bank from TEST815: do not call its fixed 22-card gate.
    # Same H3 tensor sampling/normalization, generalized to this experiment's size.
    bank821 = {}
    for cid in sorted(entries):
        cp = safe_load(entries[cid])
        try:
            x = cp['h'][0, P:, :].float().cpu().numpy()
            gate821('H3_NONEMPTY_' + cid, x.ndim == 2 and x.shape[0] > 8 and x.shape[1] == H)
            ix = np.linspace(0, len(x) - 1, min(96, len(x)), dtype=np.int64)
            bank821[cid] = normalized(x[ix]).T.copy()
        finally:
            del cp
    gate821('H3_BANK', len(bank821) == len(entries), len(bank821))

    def eligible821(world, arm):
        """Experimenter intervention, never inferred from answer or given to controller."""
        pool = []
        for w in worlds821:
            ids = w['ids']
            pool += [ids['first'], ids['second']]
            if arm == 'ADD_IRRELEVANT':
                pool.append(ids['decoy'])
        current = next(w for w in worlds821 if w['world'] == world)
        if arm == 'REMOVE_SECOND':
            pool.remove(current['ids']['second'])
        elif arm == 'REPLACE_SECOND':
            pool.remove(current['ids']['second'])
            pool.append(current['ids']['changed'])
        elif arm == 'NULL':
            return [NULL821]
        return pool

    def _native821_verbose(ids, prompt, tag, max_new):
        t0 = time.perf_counter()
        mem, active, fusion_steps, _ = build_fusion(ids, 'TEST821_' + tag, True)
        try:
            gate821('NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
            n = int(mem[0][0].shape[-2])
            expected = P + sum(int(entries[x]['body_tokens']) for x in ids)
            gate821('NATIVE_LENGTH_' + tag, n == expected, {'n': n, 'expected': expected})
            first = int(entries[ids[0]]['body_tokens'])
            spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                    {'B0': (P, n), 'B1': (n, n)}
            seals = memory_seals(mem)
            out = free_generate(mem, prompt, seed=None, gain=0., max_new=max_new, spans=spans)
            gate821('KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
            gate821('SDPA_RESTORED_' + tag,
                    _torch821.nn.functional.scaled_dot_product_attention is SDPA821)
            return {'raw': out['raw'], 'tokens': int(out['generated_tokens']),
                    'possibly_truncated': int(out['generated_tokens']) >= max_new,
                    'ids': list(ids), 'time_seconds': round(time.perf_counter() - t0, 3),
                    'fusion_steps': fusion_steps,
                    'cartridge_shas': [entries[x]['sha256'] for x in ids]}
        finally:
            del mem
            gc.collect()
            release()

    def native821(ids, prompt, tag, max_new):
        # Suppress repetitive engine PASS / fusion messages on notebook screen.
        # Every failed native call still exposes its captured diagnostic tail.
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                result = _native821_verbose(ids, prompt, tag, max_new)
            return result
        except BaseException:
            log821('NATIVE_FAILURE_DIAGNOSTICS', tag, capture.getvalue()[-12000:])
            raise

    def answer_prompt821(question):
        # Readout boundary only; never used to choose a physical action.
        return ('Use only mounted physical evidence. Follow directed links. '
                'If a link is missing, answer UNKNOWN. Return only the endpoint '
                'or UNKNOWN. Question: ' + question)

    # Model-native state observation: original TEST779/790 native CUT3 probe, unchanged.
    # A question is tokenized at the input boundary; NO language is generated or parsed
    # by the control loop. Only tensors, floats, and opaque cartridge IDs are used.
    gate821('NUMERICAL_PROBE_SYMBOL', callable(globals().get('observe_state')))

    def probe821(ids, question, tag):
        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                mem, active, _, _ = build_fusion(ids, 'TEST821_NUM_' + tag, True)
                try:
                    gate821('NUM_NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
                    n = int(mem[0][0].shape[-2])
                    gate821('NUM_NATIVE_LENGTH_' + tag,
                            n == P + sum(int(entries[x]['body_tokens']) for x in ids))
                    first = int(entries[ids[0]]['body_tokens'])
                    spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                            {'B0': (P, n), 'B1': (n, n)}
                    seals = memory_seals(mem)
                    state, att = observe_state(mem, question, spans)
                    gate821('NUM_STATE_' + tag, state.numel() == H and
                            bool(_torch821.isfinite(state).all().item()))
                    gate821('NUM_KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
                    gate821('NUM_SDPA_' + tag,
                            _torch821.nn.functional.scaled_dot_product_attention is SDPA821)
                    vec = state.detach().float().cpu().numpy().copy()
                    return vec, att
                finally:
                    del mem
                    gc.collect()
                    release()
        except BaseException:
            log821('NUMERICAL_PROBE_FAILURE', tag, capture.getvalue()[-6000:])
            raise

    def unit821(x):
        y = np.asarray(x, dtype=np.float64).reshape(-1)
        norm = float(np.linalg.norm(y))
        if not np.isfinite(norm) or norm <= 1e-12:
            raise RuntimeError('NUMERIC_NONFINITE_OR_ZERO_STATE')
        return y / norm

    def run_trial821(q, arm):
        # No generated tokens are ever read to choose a memory or to stop.
        # The probe reads frozen CUT3 activations only. Physical memory cards
        # are unchanged; all interventions are defined by the presealed arm.
        allowed = eligible821(q['world'], arm)
        ranked, scores = numeric_rank(q['question'], {cid: bank821[cid] for cid in allowed})
        gate821('RANK_' + q['qid'] + '_' + arm,
                len(ranked) == len(allowed) and set(ranked) == set(allowed))
        tag = q['qid'] + '_' + arm
        first = ranked[0]
        selected = [first]
        initial_state, _ = probe821(selected, q['question'], tag + '_INITIAL')
        reference = unit821(initial_state)
        previous = reference.copy()
        vals = np.array([float(scores[c]) for c in ranked], dtype=np.float64)
        gate821('FINITE_RANK_' + tag, bool(np.isfinite(vals).all()))
        spread = max(float(np.std(vals)), 1e-9)
        velocity = np.zeros(H, dtype=np.float64)
        changes = []
        decisions = []
        trace = [{'step': 0, 'ids': selected[:],
                  'state_sha256': sha821(np.asarray(initial_state, dtype=np.float32).tobytes())}]
        stop_reason = None
        safety_stop = None
        # Use candidate H3 matrices to compute a tensor-only compatibility
        # against the observed CUT3 state. This is a diagnostic policy, not
        # an oracle: the reference state may itself be wrong or incomplete.
        for step in range(1, MAX_STEPS821 + 1):
            candidates = [c for c in ranked if c not in selected]
            if not candidates:
                stop_reason = 'CANDIDATE_EXHAUSTION'
                break
            utilities = {}
            for cid in candidates:
                matrix = np.asarray(bank821[cid], dtype=np.float64)
                # Columnwise normalized stored H3 vectors; maximum alignment
                # avoids cancellation from averaging opposite-direction tokens.
                colnorm = np.maximum(np.linalg.norm(matrix, axis=0), 1e-12)
                similarities = np.abs((previous @ matrix) / colnorm)
                alignment = float(np.quantile(similarities, 0.75))
                rank_z = (float(scores[cid]) - float(np.mean(vals))) / spread
                # Predeclared balanced diagnostic mixture; no answer labels.
                utilities[cid] = {'alignment': alignment, 'rank_z': rank_z,
                                  'priority': rank_z + alignment}
            target = max(candidates, key=lambda c: (utilities[c]['priority'], -ranked.index(c)))
            # Explicitly record whether a numerical stop is justified.
            # Do not pretend the four-step safety ceiling is autonomous STOP.
            if len(changes) >= 2:
                recent = np.array(changes[-2:], dtype=np.float64)
                # Relative stability: compares observed motion with the
                # trajectory's own historical scale, not a tuned answer rule.
                baseline = max(float(np.median(changes)), 1e-12)
                if float(np.max(recent)) < 0.10 * baseline and float(np.linalg.norm(velocity)) < 0.10 * baseline:
                    stop_reason = 'RELATIVE_TENSOR_STABILITY'
                    break
            next_ids = [selected[-1], target]
            new_state, att = probe821(next_ids, q['question'], tag + '_STEP_' + str(step))
            current = unit821(new_state)
            delta = current - previous
            displacement = float(np.linalg.norm(delta))
            velocity = 0.30 * velocity + 0.70 * delta
            changes.append(displacement)
            # Causal observations: token-normalized attention per mounted slot,
            # and difference from initial tensor state. Never semantic labels.
            span0 = int(entries[next_ids[0]]['body_tokens'])
            span1 = int(entries[next_ids[1]]['body_tokens'])
            slot_density = {}
            for slot, length in [('B0', span0), ('B1', span1)]:
                masses = [float(v[slot + '_mass']) for v in att.values()
                          if isinstance(v, dict) and slot + '_mass' in v]
                slot_density[slot] = float(np.mean(masses) / max(length, 1)) if masses else None
            gate821('FINITE_FEEDBACK_' + tag + '_' + str(step),
                    bool(np.isfinite(displacement) and np.isfinite(velocity).all()))
            decisions.append({'step': step, 'target': target, 'rank_score': float(scores[target]),
                              'priority': utilities[target]['priority'],
                              'h3_alignment': utilities[target]['alignment'],
                              'state_change': displacement,
                              'initial_state_alignment': float(np.dot(reference, current)),
                              'velocity_norm': float(np.linalg.norm(velocity)),
                              'slot_attention_density': slot_density})
            trace.append({'step': step, 'ids': next_ids[:],
                          'state_sha256': sha821(np.asarray(new_state, dtype=np.float32).tobytes())})
            selected = next_ids
            previous = current
        if stop_reason is None:
            safety_stop = 'MAX_STEPS_SAFETY_BOUND'
        # Natural language is allowed only for the experiment's external
        # question/readout, NEVER in the numerical control loop.
        initial = native821([first], answer_prompt821(q['question']),
                            tag + '_INITIAL_READOUT', MAX_NEW_ANSWER821)
        final = native821(selected, answer_prompt821(q['question']),
                          tag + '_FINAL_READOUT', MAX_NEW_ANSWER821)
        return {'qid': q['qid'], 'arm': arm, 'question': q['question'],
                'initial': initial['raw'].strip(), 'final': final['raw'].strip(),
                'initial_selected': [first], 'ranked_ids': ranked,
                'ranked_scores': {cid: float(scores[cid]) for cid in ranked},
                'trace': trace, 'model_decisions': decisions,
                'model_stop': False, 'numerical_stop': stop_reason == 'RELATIVE_TENSOR_STABILITY',
                'numeric_stop_reason': stop_reason, 'safety_stop': safety_stop,
                'steps_executed': len(decisions), 'model_actions': ['NUMERIC_READ'] * len(decisions),
                'valid_decisions': len(decisions), 'first_valid_decisions': len(decisions),
                'repair_attempts': 0, 'repair_successes': 0,
                'controller_decisions': len(decisions)}

    for q in questions821:
        for arm in ARMS821:
            row = run_trial821(q, arm)
            D821['trials'].append(row)
            save821()
            log821('TEST821_TRIAL', row['qid'], arm, 'steps', row['steps_executed'], 'stop', row['numeric_stop_reason'] or row['safety_stop'],
                   'final', repr(row['final'][:80]))

    # Fixed two-read comparison: no model-selected action, same question and H3 bank.
    # It is an experimental control, NOT the proposed autonomous policy.
    D821['fixed_baseline'] = []
    for q in questions821:
        allowed = eligible821(q['world'], 'FULL')
        ranked, _ = numeric_rank(q['question'], {cid: bank821[cid] for cid in allowed})
        ids = ranked[:2]
        baseline = native821(ids, answer_prompt821(q['question']),
                             q['qid'] + '_FIXED_TWO', MAX_NEW_ANSWER821)
        D821['fixed_baseline'].append({'qid': q['qid'], 'ids': ids, 'raw': baseline['raw'],
                                       'possibly_truncated': baseline['possibly_truncated']})
        save821()
    gate821('FIXED_BASELINE_COUNT', len(D821['fixed_baseline']) == len(questions821))

    gate821('TRIAL_COUNT', len(D821['trials']) == len(questions821) * len(ARMS821),
            len(D821['trials']))
    gate821('FROZEN_WEIGHT_SENTINEL', before821 == sentinel())
    gate821('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    gate821('PANEL_UNCHANGED', sha821(json.dumps(PANEL821, ensure_ascii=False, sort_keys=True)) == PANEL_SHA821)
    for cid in cards821:
        gate821('FINAL_SHA_' + cid, sha_file(CART_DIR / entries[cid]['file']) == entries[cid]['sha256'])

    # Diagnostic exact-match scoring is performed OFFLINE, after all model calls.
    # The expected answer never enters native821 or run_trial821.
    lookup821 = {q['qid']: q for q in questions821}
    def exact821(ans, expected):
        return ans.strip().strip(' .\n').upper() == expected.upper()
    scored821 = []
    for r in D821['trials']:
        key = lookup821[r['qid']]
        expected = key['changed_expected'] if r['arm'] == 'REPLACE_SECOND' else key['expected']
        should_unknown = r['arm'] in ('REMOVE_SECOND', 'NULL')
        correct = (r['final'].strip().upper() == 'UNKNOWN') if should_unknown else exact821(r['final'], expected)
        scored821.append({'qid': r['qid'], 'arm': r['arm'], 'expected': 'UNKNOWN' if should_unknown else expected,
                          'exact_correct': correct, 'model_stop': r['model_stop'],
                          'valid_decisions': r['valid_decisions'],
                          'controller_decisions': r['controller_decisions'],
                          'repair_attempts': r['repair_attempts'],
                          'repair_successes': r['repair_successes'],
                          'initial': r['initial'], 'final': r['final']})
    D821['fixed_baseline_offline'] = {'cases': len(D821['fixed_baseline']),
        'exact_correct': sum(exact821(b['raw'], lookup821[b['qid']]['expected'])
                             for b in D821['fixed_baseline'])}
    D821['offline_scores'] = {
        arm: {'cases': sum(x['arm'] == arm for x in scored821),
              'exact_correct': sum(x['arm'] == arm and x['exact_correct'] for x in scored821),
              'model_stops': sum(x['arm'] == arm and x['model_stop'] for x in scored821),
              'numerical_stability_stops': sum(r['arm'] == arm and r['numerical_stop'] for r in D821['trials']),
              'safety_bound_stops': sum(r['arm'] == arm and r['safety_stop'] == 'MAX_STEPS_SAFETY_BOUND' for r in D821['trials']),
              'valid_control_decisions': sum(x['valid_decisions'] for x in scored821 if x['arm'] == arm),
              'total_control_decisions': sum(x['controller_decisions'] for x in scored821 if x['arm'] == arm),
              'repair_attempts': sum(x['repair_attempts'] for x in scored821 if x['arm'] == arm),
              'repair_successes': sum(x['repair_successes'] for x in scored821 if x['arm'] == arm)}
        for arm in ARMS821}
    with REVIEW821.open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['qid', 'arm', 'initial', 'final', 'expected', 'exact_correct', 'model_stop',
                'human_reasoning_correct_0_1', 'human_attribution_correct_0_1',
                'human_autonomous_correction_0_1', 'human_notes']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in scored821:
            writer.writerow({k: row.get(k, '') for k in cols})
    D821['review_sha256'] = sha821(REVIEW821.read_bytes())
    D821['status'] = 'COMPLETE_MECHANICAL_OFFLINE_SCORING_HUMAN_REVIEW_PENDING'
    save821()
    log821('TEST821_COMPLETED', json.dumps(D821['offline_scores']), OUT821, REVIEW821)
except BaseException as e:
    D821['status'] = 'ERROR'
    D821['error'] = {'repr': repr(e), 'traceback': traceback.format_exc()}
    save821()
    log821('TEST821_FAILED', repr(e), traceback.format_exc())
    raise
finally:
    gc.collect()
    if 'release' in globals() and callable(globals()['release']):
        try:
            release()
        except Exception:
            pass
    save821()
