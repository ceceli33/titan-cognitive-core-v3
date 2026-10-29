# AKBASCORE SILICON HIPPOCAMPUS — TEST919
# Autonomous evidence control: KEEP / CORRECT / RESEARCH / STOP
# Single Colab cell; frozen Qwen2.5-72B NF4; exactly one A100 80GB.
# LOCKED TEST815 engine; no residual hooks, no source replay at read time, no training.
# EXPERIMENTAL PROTOCOL, NOT A GPU-VERIFIED RESULT.
# NOTE: controller outputs are model-generated text commands; this does NOT establish
# fully tensor-internal metacognition. Action execution is a bounded external actuator.
import ast, hashlib, urllib.request, json, csv, gc, time, traceback, random, re, datetime
from pathlib import Path

T919 = '919'
REPO919 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCK815_919 = '77774f87428c0243c9a86ea6a041364acd9c1b03'
SEED919 = 9192026
WORLDS919 = 8
PARAPHRASES919 = 3
MAX_STEPS919 = 4                 # safety ceiling, NOT evidence of autonomous stopping
MAX_NEW_ANSWER919 = 96
MAX_NEW_CONTROL919 = 64
MAX_CANDIDATES919 = 5
RUN919 = 'TEST919_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
DIR919 = (Path('/content') if Path('/content').exists() else Path('/tmp')) / RUN919
DIR919.mkdir(parents=True, exist_ok=False)
OUT919 = DIR919 / 'TEST919_results.json'
LOG919 = DIR919 / 'TEST919.log'
REVIEW919 = DIR919 / 'TEST919_blind_review.csv'
OFFLINE919 = DIR919 / 'TEST919_offline_key.json'  # never available to inference/controller

D919 = {'test': T919, 'status': 'STARTED', 'run': RUN919,
        'source815_blob': LOCK815_919, 'checks': [], 'trials': [],
        'limitations': [
            'Model-generated textual controller commands are not tensor-only internal reasoning.',
            'Action parser and physical actuator are external infrastructure; model selects proposed actions.',
            'Offline truth is never given to numeric_rank, free_generate, or controller.',
            'MAX_STEPS is a safety bound, not autonomous stopping.',
            'Native reads and integrity checks are distinct from semantic correctness.',
            'Synthetic two-hop relations test a narrow capability, not general scientific reasoning.',
            'No GPU execution or result is claimed by the code author.']}

def sha919(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()

def blob919(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def save919():
    p = Path(str(OUT919) + '.tmp')
    p.write_text(json.dumps(D919, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    p.replace(OUT919)

def log919(*args):
    msg = ' '.join(map(str, args))
    print(msg, flush=True)
    with LOG919.open('a', encoding='utf-8') as f:
        f.write(msg + '\n')

def gate919(name, ok, detail=None):
    D919['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail})
    save919()
    log919('PASS' if ok else 'FAIL', name, detail if detail is not None else '')
    if not ok:
        raise RuntimeError('TEST919_GATE_' + name)

# PRESEALED panel: opaque names and randomized assignments. All scoring stays offline.
RNG919 = random.Random(SEED919)
ALPH919 = 'ABCDEFGHJKLMNPQRSTUVWXYZ'

def code919():
    return ''.join(RNG919.choice(ALPH919) for _ in range(9))

worlds919 = []
seen919 = set()
for wi in range(WORLDS919):
    names = []
    while len(names) < 5:
        n = code919()
        if n not in seen919:
            seen919.add(n); names.append(n)
    worlds919.append({'world': 'DOMAIN_' + code919(), 'start': names[0],
                      'middle': names[1], 'end': names[2],
                      'changed_end': names[3], 'decoy_end': names[4]})

questions919 = []
for w in worlds919:
    for pi, fmt in enumerate((
        'In domain {world}, starting from {start}, which endpoint is reached after exactly two directed links?',
        'For {world}, follow two successive directed edges beginning at {start}. Give the final node.',
        'Within {world}, what is the two-step destination of {start}? Do not guess when a link is absent.')):
        questions919.append({'qid': w['world'] + '_P' + str(pi), 'world': w['world'],
                             'question': fmt.format(**w), 'expected': w['end'],
                             'changed_expected': w['changed_end']})

# Each domain has two independent source cards and a deliberately irrelevant card.
# Changed source is an independently forged cartridge, never an in-place mutation.
cards919, card_meta919 = {}, {}
for w in worlds919:
    domain = w['world']
    ids = {kind: 'E919_' + code919() for kind in ('first', 'second', 'changed', 'decoy')}
    w['ids'] = ids
    cards919[ids['first']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['start'] + ' -> ' + w['middle'] + '.\n')
    cards919[ids['second']] = ('Evidence record. Domain: ' + domain + '\n' +
                             'Directed relation: ' + w['middle'] + ' -> ' + w['end'] + '.\n')
    cards919[ids['changed']] = ('Evidence record. Domain: ' + domain + '\n' +
                              'Directed relation: ' + w['middle'] + ' -> ' + w['changed_end'] + '.\n')
    cards919[ids['decoy']] = ('Evidence record. Domain: ' + domain + '\n' +
                            'Directed relation: ' + w['decoy_end'] + ' -> ' + w['start'] + '.\n')
    for kind, cid in ids.items():
        card_meta919[cid] = {'domain': domain, 'kind': kind, 'body_sha256': sha919(cards919[cid])}
NULL919 = 'E919_NULL'
cards919[NULL919] = 'CONTROL MEMORY. No directed relations are available.\n'
card_meta919[NULL919] = {'domain': None, 'kind': 'null', 'body_sha256': sha919(cards919[NULL919])}

# The blind controller sees candidate IDs and its own outputs, never the answer key.
# Baseline and interventions use the SAME code; only physically eligible cartridges differ.
ARMS919 = ('FULL', 'REMOVE_SECOND', 'REPLACE_SECOND', 'ADD_IRRELEVANT', 'NULL')
PANEL919 = {'seed': SEED919, 'world_count': WORLDS919, 'paraphrases': PARAPHRASES919,
            'questions': [{'qid': q['qid'], 'question': q['question']} for q in questions919],
            'arms': ARMS919, 'limits': [MAX_STEPS919, MAX_NEW_ANSWER919, MAX_NEW_CONTROL919,
                                       MAX_CANDIDATES919], 'card_hashes': card_meta919}
PANEL_SHA919 = sha919(json.dumps(PANEL919, ensure_ascii=False, sort_keys=True))
D919['panel_sha256'] = PANEL_SHA919
D919['panel_public'] = PANEL919
OFFLINE919.write_text(json.dumps({'note': 'OFFLINE ONLY — NEVER IMPORT INTO CONTROLLER',
                                  'questions': questions919, 'worlds': worlds919},
                                 ensure_ascii=False, indent=2), encoding='utf-8')
D919['offline_key_sha256'] = sha919(OFFLINE919.read_bytes())
save919()

# The engine is imported from the EXACT locked TEST815 AST prelude, unchanged.
# The original TEST815 experiment is never executed.
try:
    log919('TEST919_START', RUN919, 'PANEL_SHA', PANEL_SHA919)
    req919 = urllib.request.Request(REPO919 + '815.py', headers={'User-Agent': 'AKBASCORE-TEST919'})
    with urllib.request.urlopen(req919, timeout=180) as f:
        raw815_919 = f.read(120001)
    gate919('LOCK815', len(raw815_919) <= 120000 and blob919(raw815_919) == LOCK815_919,
            blob919(raw815_919))
    tree815_919 = ast.parse(raw815_919.decode('utf-8'), filename='815.py')
    idx919 = [i for i, n in enumerate(tree815_919.body) if isinstance(n, ast.Try)]
    gate919('AST_BOUNDARY', len(idx919) == 1 and idx919[0] == len(tree815_919.body) - 1, idx919)
    exec(compile(ast.fix_missing_locations(ast.Module(body=tree815_919.body[:idx919[0]], type_ignores=[])),
                 'LOCKED_TEST815_PRELUDE', 'exec'), globals())
    gate919('LOCKED_ENGINE_SYMBOLS', all(callable(globals().get(x)) for x in
            ('model_setup', 'physical_commit', 'safe_load', 'build_fusion', 'free_generate',
             'memory_seals', 'compare_seals', 'sentinel', 'release', 'numeric_rank')))
    gate919('FRESH_BANK', len(entries) == 0, len(entries))
    import torch as _torch919
    SDPA919 = _torch919.nn.functional.scaled_dot_product_attention

    # Token budget is validated BEFORE loading 72B model weights.
    tok919 = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=False)
    tok_counts919 = {cid: len(tok919.encode(body, add_special_tokens=False)) for cid, body in cards919.items()}
    gate919('TOKEN_BUDGET', all(4 <= n <= 256 for n in tok_counts919.values()),
            {'max_body_tokens': max(tok_counts919.values()), 'stage': 'TOKENIZER_PRE_MODEL'})
    del tok919

    model_setup()
    before919 = sentinel()
    gate919('FROZEN_PREFIX', P == 30, P)
    gate919('FUSION_BUDGET',
            P + 2 * max(tok_counts919.values()) + 64 <= MAX_FUSED_TOKENS,
            {'max_body_tokens': max(tok_counts919.values()), 'max_fused_tokens': MAX_FUSED_TOKENS})
    for cid, body in cards919.items():
        physical_commit(cid, body)
        gate919('BODY_SHA_' + cid, entries[cid].get('body_sha256') == sha919(body))
    gate919('PHYSICAL_COUNT', len(entries) == len(cards919), len(entries))
    for cid in cards919:
        p = safe_load(entries[cid])
        gate919('RELOAD_' + cid, p['book_id'] == cid and int(p['n']) > P and
                len(p['lower']) == CUT + 1 and tuple(p['h'].shape)[-1] == H)
        del p
    release()

    # Locked numerical H3 bank from TEST815: do not call its fixed 22-card gate.
    # Same H3 tensor sampling/normalization, generalized to this experiment's size.
    bank919 = {}
    for cid in sorted(entries):
        cp = safe_load(entries[cid])
        try:
            x = cp['h'][0, P:, :].float().cpu().numpy()
            gate919('H3_NONEMPTY_' + cid, x.ndim == 2 and x.shape[0] > 8 and x.shape[1] == H)
            ix = np.linspace(0, len(x) - 1, min(96, len(x)), dtype=np.int64)
            bank919[cid] = normalized(x[ix]).T.copy()
        finally:
            del cp
    gate919('H3_BANK', len(bank919) == len(entries), len(bank919))

    def eligible919(world, arm):
        """Experimenter intervention, never inferred from answer or given to controller."""
        pool = []
        for w in worlds919:
            ids = w['ids']
            pool += [ids['first'], ids['second']]
            if arm == 'ADD_IRRELEVANT':
                pool.append(ids['decoy'])
        current = next(w for w in worlds919 if w['world'] == world)
        if arm == 'REMOVE_SECOND':
            pool.remove(current['ids']['second'])
        elif arm == 'REPLACE_SECOND':
            pool.remove(current['ids']['second'])
            pool.append(current['ids']['changed'])
        elif arm == 'NULL':
            return [NULL919]
        return pool

    def native919(ids, prompt, tag, max_new):
        t0 = time.perf_counter()
        mem, active, fusion_steps, _ = build_fusion(ids, 'TEST919_' + tag, True)
        try:
            gate919('NATIVE80_' + tag, len(mem) == NL and list(active) == ids)
            n = int(mem[0][0].shape[-2])
            expected = P + sum(int(entries[x]['body_tokens']) for x in ids)
            gate919('NATIVE_LENGTH_' + tag, n == expected, {'n': n, 'expected': expected})
            first = int(entries[ids[0]]['body_tokens'])
            spans = {'B0': (P, P + first), 'B1': (P + first, n)} if len(ids) == 2 else \
                    {'B0': (P, n), 'B1': (n, n)}
            seals = memory_seals(mem)
            out = free_generate(mem, prompt, seed=None, gain=0., max_new=max_new, spans=spans)
            gate919('KV_SEAL_' + tag, compare_seals(seals, memory_seals(mem)))
            gate919('SDPA_RESTORED_' + tag,
                    _torch919.nn.functional.scaled_dot_product_attention is SDPA919)
            return {'raw': out['raw'], 'tokens': int(out['generated_tokens']),
                    'possibly_truncated': int(out['generated_tokens']) >= max_new,
                    'ids': list(ids), 'time_seconds': round(time.perf_counter() - t0, 3),
                    'fusion_steps': fusion_steps,
                    'cartridge_shas': [entries[x]['sha256'] for x in ids]}
        finally:
            del mem
            gc.collect()
            release()

    def parse_control919(raw, candidate_ids):
        # Strict syntax: no guessed fallback action. Invalid control => safety stop,
        # reported as failure to produce a valid autonomous decision.
        m = re.search(r'(?im)^\s*ACTION\s*:\s*(KEEP|CORRECT|RESEARCH|STOP)\s*$', raw)
        n = re.search(r'(?im)^\s*NEXT\s*:\s*([A-Za-z0-9_\-]+|NONE)\s*$', raw)
        if not m or not n:
            return {'valid': False, 'reason': 'FORMAT', 'raw': raw}
        action, target = m.group(1).upper(), n.group(1)
        if action == 'STOP' and target != 'NONE':
            return {'valid': False, 'reason': 'STOP_WITH_TARGET', 'raw': raw}
        if action != 'STOP' and target not in candidate_ids:
            return {'valid': False, 'reason': 'TARGET_NOT_OFFERED', 'raw': raw}
        return {'valid': True, 'action': action, 'target': target}

    def control_prompt919(question, hypothesis, candidates, visited):
        # Previous model output is an intermediate hypothesis, NOT replayed source text.
        # Only opaque cartridge IDs, not source content or truth labels, are shown.
        return ('You are controlling your own next evidence operation. The mounted physical memory '
                'is your current evidence. Previous hypothesis is your own output, not a ground truth. '
                'Decide without external correction. KEEP means preserve hypothesis and inspect NEXT '
                'to verify; CORRECT means evidence suggests revision and inspect NEXT; RESEARCH means '
                'insufficient evidence and inspect NEXT; STOP means enough evidence or no useful next '
                'step. Do not claim certainty without evidence. Reply EXACTLY two lines:\n'
                'ACTION: KEEP|CORRECT|RESEARCH|STOP\nNEXT: <candidate_id>|NONE\n'
                'Question: ' + question + '\nPrevious hypothesis: ' + hypothesis + '\n'
                'Previously inspected cartridge IDs: ' + ', '.join(visited) + '\n'
                'Available next cartridge IDs: ' + ', '.join(candidates) + '\n')

    def answer_prompt919(question, previous=None):
        s = ('Use only the mounted physical evidence. Follow directed links precisely. '
             'If a required link is missing, answer UNKNOWN. Give only the final endpoint '
             'or UNKNOWN. Question: ' + question)
        if previous is not None:
            s += '\nPrevious tentative hypothesis (not a fact): ' + previous
        return s

    def run_trial919(q, arm):
        allowed = eligible919(q['world'], arm)
        # Blind numerical rank over eligible physical cartridges; no gold source IDs.
        ranked, scores = numeric_rank(q['question'], {cid: bank919[cid] for cid in allowed})
        gate919('RANK_' + q['qid'] + '_' + arm,
                len(ranked) == len(allowed) and set(ranked) == set(allowed))
        tag = q['qid'] + '_' + arm
        selected = [ranked[0]]
        initial = native919(selected, answer_prompt919(q['question']), tag + '_INITIAL', MAX_NEW_ANSWER919)
        hypothesis = initial['raw'].strip()
        trace = [{'step': 0, 'operation': 'INITIAL', 'ids': selected[:], 'answer': initial,
                  'hypothesis': hypothesis}]
        stopped_by_model = False
        safety_stop = None
        model_decisions = []
        for step in range(1, MAX_STEPS919 + 1):
            # Candidate IDs are drawn from blind numeric ranking, not oracle labels.
            candidates = [cid for cid in ranked if cid not in selected][:MAX_CANDIDATES919]
            # The controller sees mounted evidence and its own hypothesis, not the gold.
            audit = native919(selected,
                              control_prompt919(q['question'], hypothesis, candidates, selected),
                              tag + '_CONTROL_' + str(step), MAX_NEW_CONTROL919)
            decision = parse_control919(audit['raw'], candidates)
            model_decisions.append({'step': step, 'control_read': audit, 'decision': decision,
                                    'candidate_ids': candidates})
            if not decision['valid']:
                safety_stop = 'INVALID_CONTROLLER_OUTPUT'
                break
            if decision['action'] == 'STOP':
                stopped_by_model = True
                break
            target = decision['target']
            # The controller's proposed action actually changes the next native read.
            # Keep a maximum of two physical sources in a native fusion; don't silently
            # drop a third source. Re-read chosen evidence independently if >2 needed.
            if target in selected:
                safety_stop = 'REPEATED_TARGET'
                break
            selected = ([selected[-1], target] if len(selected) >= 2 else selected + [target])
            nxt = native919(selected, answer_prompt919(q['question'], hypothesis),
                            tag + '_ACTION_' + str(step), MAX_NEW_ANSWER919)
            new_hypothesis = nxt['raw'].strip()
            trace.append({'step': step, 'operation': decision['action'], 'target': target,
                          'ids': selected[:], 'answer': nxt, 'before': hypothesis,
                          'after': new_hypothesis, 'changed': new_hypothesis != hypothesis})
            hypothesis = new_hypothesis
        if not stopped_by_model and safety_stop is None:
            safety_stop = 'MAX_STEPS_SAFETY_BOUND'
        return {'qid': q['qid'], 'arm': arm, 'question': q['question'],
                'initial': initial['raw'].strip(), 'final': hypothesis,
                'initial_selected': [ranked[0]], 'ranked_ids': ranked,
                'ranked_scores': {cid: float(scores[cid]) for cid in ranked},
                'trace': trace, 'model_decisions': model_decisions,
                'model_stop': stopped_by_model, 'safety_stop': safety_stop,
                'steps_executed': len(model_decisions),
                'model_actions': [d['decision'].get('action', 'INVALID') for d in model_decisions],
                'valid_decisions': sum(bool(d['decision']['valid']) for d in model_decisions),
                'controller_decisions': len(model_decisions)}

    for q in questions919:
        for arm in ARMS919:
            row = run_trial919(q, arm)
            D919['trials'].append(row)
            save919()
            log919('TEST919_TRIAL', row['qid'], arm, 'initial', repr(row['initial']),
                   'final', repr(row['final']), 'actions', row['model_actions'],
                   'model_stop', row['model_stop'], 'safety_stop', row['safety_stop'])

    # Fixed two-read comparison: no model-selected action, same question and H3 bank.
    # It is an experimental control, NOT the proposed autonomous policy.
    D919['fixed_baseline'] = []
    for q in questions919:
        allowed = eligible919(q['world'], 'FULL')
        ranked, _ = numeric_rank(q['question'], {cid: bank919[cid] for cid in allowed})
        ids = ranked[:2]
        baseline = native919(ids, answer_prompt919(q['question']),
                             q['qid'] + '_FIXED_TWO', MAX_NEW_ANSWER919)
        D919['fixed_baseline'].append({'qid': q['qid'], 'ids': ids, 'raw': baseline['raw'],
                                       'possibly_truncated': baseline['possibly_truncated']})
        save919()
    gate919('FIXED_BASELINE_COUNT', len(D919['fixed_baseline']) == len(questions919))

    gate919('TRIAL_COUNT', len(D919['trials']) == len(questions919) * len(ARMS919),
            len(D919['trials']))
    gate919('FROZEN_WEIGHT_SENTINEL', before919 == sentinel())
    gate919('NO_RESIDUAL_HOOKS', not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    gate919('PANEL_UNCHANGED', sha919(json.dumps(PANEL919, ensure_ascii=False, sort_keys=True)) == PANEL_SHA919)
    for cid in cards919:
        gate919('FINAL_SHA_' + cid, sha_file(CART_DIR / entries[cid]['file']) == entries[cid]['sha256'])

    # Diagnostic exact-match scoring is performed OFFLINE, after all model calls.
    # The expected answer never enters native919 or run_trial919.
    lookup919 = {q['qid']: q for q in questions919}
    def exact919(ans, expected):
        return ans.strip().strip(' .\n').upper() == expected.upper()
    scored919 = []
    for r in D919['trials']:
        key = lookup919[r['qid']]
        expected = key['changed_expected'] if r['arm'] == 'REPLACE_SECOND' else key['expected']
        should_unknown = r['arm'] in ('REMOVE_SECOND', 'NULL')
        correct = (r['final'].strip().upper() == 'UNKNOWN') if should_unknown else exact919(r['final'], expected)
        scored919.append({'qid': r['qid'], 'arm': r['arm'], 'expected': 'UNKNOWN' if should_unknown else expected,
                          'exact_correct': correct, 'model_stop': r['model_stop'],
                          'valid_decisions': r['valid_decisions'],
                          'controller_decisions': r['controller_decisions'],
                          'initial': r['initial'], 'final': r['final']})
    D919['fixed_baseline_offline'] = {'cases': len(D919['fixed_baseline']),
        'exact_correct': sum(exact919(b['raw'], lookup919[b['qid']]['expected'])
                             for b in D919['fixed_baseline'])}
    D919['offline_scores'] = {
        arm: {'cases': sum(x['arm'] == arm for x in scored919),
              'exact_correct': sum(x['arm'] == arm and x['exact_correct'] for x in scored919),
              'model_stops': sum(x['arm'] == arm and x['model_stop'] for x in scored919),
              'valid_control_decisions': sum(x['valid_decisions'] for x in scored919 if x['arm'] == arm),
              'total_control_decisions': sum(x['controller_decisions'] for x in scored919 if x['arm'] == arm)}
        for arm in ARMS919}
    with REVIEW919.open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['qid', 'arm', 'initial', 'final', 'expected', 'exact_correct', 'model_stop',
                'human_reasoning_correct_0_1', 'human_attribution_correct_0_1',
                'human_autonomous_correction_0_1', 'human_notes']
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in scored919:
            writer.writerow({k: row.get(k, '') for k in cols})
    D919['review_sha256'] = sha919(REVIEW919.read_bytes())
    D919['status'] = 'COMPLETE_MECHANICAL_OFFLINE_SCORING_HUMAN_REVIEW_PENDING'
    save919()
    log919('TEST919_COMPLETED', json.dumps(D919['offline_scores']), OUT919, REVIEW919)
except BaseException as e:
    D919['status'] = 'ERROR'
    D919['error'] = {'repr': repr(e), 'traceback': traceback.format_exc()}
    save919()
    log919('TEST919_FAILED', repr(e), traceback.format_exc())
    raise
finally:
    gc.collect()
    if 'release' in globals() and callable(globals()['release']):
        try:
            release()
        except Exception:
            pass
    save919()
