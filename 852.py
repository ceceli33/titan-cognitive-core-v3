# AKBASCORE SILICON HIPPOCAMPUS — TEST852
# Native coverage/relation control revision on the locked, completed TEST851 chain.
# One Colab cell; one A100-SXM4-80GB; frozen Qwen2.5-72B-Instruct NF4.
# This source does not claim GPU execution. The run itself must establish every GPU result.
import ast, hashlib, json, urllib.request

URL852 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/851.py'
LOCK852 = '0f01e73b9ad160c988cfe059e8b5ae5e1f35f65b'
with urllib.request.urlopen(urllib.request.Request(
        URL852, headers={'User-Agent': 'AKBASCORE-TEST852'}), timeout=180) as response852:
    raw852 = response852.read(1000001)
actual852 = hashlib.sha1(
    b'blob ' + str(len(raw852)).encode() + b'\0' + raw852
).hexdigest()
assert actual852 == LOCK852, ('TEST851_PARENT_LOCK_FAILED', actual852, LOCK852)
source852 = raw852.decode('utf-8')
ast.parse(source852)
print('TEST852 SOURCE VERIFICATION')
print('851.py', actual852, 'PASS; inherited 841–850 locks are checked by the parent chain')


def replace_block852(source, name, value):
    nodes = [n for n in ast.parse(source).body if isinstance(n, ast.Assign)
        and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id == name and isinstance(n.value, ast.Constant)
        and isinstance(n.value.value, str)]
    assert len(nodes) == 1, ('PATCH_LITERAL_NOT_UNIQUE', name, len(nodes))
    lines = source.splitlines(keepends=True)
    node = nodes[0]
    lines[node.lineno-1:node.end_lineno] = [name + ' = ' + repr(value) + '\n']
    result = ''.join(lines)
    ast.parse(result)
    return result


def once852(source, old, new):
    assert source.count(old) == 1, ('PATCH_NOT_UNIQUE', old[:120], source.count(old))
    return source.replace(old, new, 1)


BODY851 = r'''
ARMS851 = ('BASELINE851', 'NATIVE852', 'MATCHED_CONTROL852')
MAX_REVIEWS851 = 2
CALL_CAP849 = min(CALL_CAP849, 160)
HARD_BUDGET_MIN841 = min(HARD_BUDGET_MIN841, 45.0)
assert len(JOBS841) == 12
assert set(j['arm'] for j in JOBS841) == set(ARMS851)
QORDER851 = list(dict.fromkeys(j['qid'] for j in JOBS841))
assert len(QORDER851) == 2
# The counterfactual starting state is the model's own hop0 output. Python
# writes neither an answer nor an error label. JOBS841 remains read-only.
MODE851 = {q: ('NATURAL' if i == 0 else 'COUNTERFACTUAL')
    for i, q in enumerate(QORDER851)}
for q in QORDER851:
    for condition in ('INTACT', 'REMOVED'):
        group = [j for j in JOBS841 if j['qid'] == q and j['intervention'] == condition]
        assert len(group) == 3
        assert len({tuple(j['initial_cards']) for j in group}) == 1
        assert len({tuple(j['bank']) for j in group}) == 1
        assert all(MODE851[j['qid']] == MODE851[q] for j in group)
PANEL_LOCK851 = {
    'test': 'TEST852', 'jobs': 12, 'arms': list(ARMS851),
    'worlds': list(QORDER851), 'conditions': ['INTACT', 'REMOVED'],
    'initial_modes': MODE851, 'max_reviews_per_job': MAX_REVIEWS851,
    'max_output_tokens_inherited_K845': K845,
    'native_call_cap': CALL_CAP849, 'hard_minutes': HARD_BUDGET_MIN841,
    'counterfactual': 'initial candidate = model hop0 output rows; no answer-key access',
    'native852': 'C/E/Kprev plus native coverage U and relation R=[mean(C)-mean(E),mean(C)+mean(E)]',
    'matched_control852': 'same U and R tensors with their semantic slots swapped',
    'job_specs': [{**{k: j[k] for k in (
        'job', 'qid', 'arm', 'intervention', 'initial_cards', 'bank'
    )}, 'initial_mode': MODE851[j['qid']]} for j in JOBS841]
}
PANEL_SHA851 = hashlib.sha256(json.dumps(
    PANEL_LOCK851, sort_keys=True, ensure_ascii=False
).encode()).hexdigest()

# The parent BODY_R2 literal is replaced, so materialize its fixed interface here.
REVIEW851 = (
    'Question: {q}\n'
    'The numerical context is a candidate FINAL answer to this question. '
    'Evaluate that candidate using only mounted physical evidence. '
    'CONTINUE means the candidate completely answers the question and is supported. '
    'REVISE means recompute the final answer from the available evidence. '
    'STOP means the evidence is insufficient to answer the question. '
    'Reply with exactly one word: CONTINUE, REVISE, or STOP.'
)
RECOMPUTE851 = (
    'Question: {q}\n'
    'Use only mounted physical evidence. The numerical context contains the '
    'candidate answer and your review state. Recompute the FINAL answer to '
    'the complete question. If the evidence is insufficient, reply UNKNOWN. '
    'Reply with the final node name only.'
)
EVIDENCE851 = (
    'Question: {q}\n'
    'Use only mounted physical evidence. Independently compute the FINAL answer '
    'from the available records. If the evidence is insufficient, reply UNKNOWN. '
    'Reply with the final node name only.'
)
REVIEW_SUFFIX851 = list(tok('\nReview action:', add_special_tokens=False).input_ids)
ANSWER_SUFFIX851 = list(tok('\nFinal answer:', add_special_tokens=False).input_ids)
C_SLOT851 = list(tok('Candidate numerical state:', add_special_tokens=False).input_ids)
E_SLOT851 = list(tok('Independent evidence numerical state:', add_special_tokens=False).input_ids)
K_SLOT851 = list(tok('Previous control numerical state:', add_special_tokens=False).input_ids)
U_SLOT852 = list(tok('Native evidence coverage state:', add_special_tokens=False).input_ids)
R_SLOT852 = list(tok('Candidate evidence relation state:', add_special_tokens=False).input_ids)
COVERAGE852 = (
    'Question: {q}\n'
    'Audit only the mounted physical evidence, independently of any candidate answer. '
    'Determine whether those records contain sufficient information to compute the complete '
    'final answer. Reply with exactly one word: SUFFICIENT or INSUFFICIENT.'
)
COVERAGE_SUFFIX852 = list(tok('\nEvidence coverage:', add_special_tokens=False).input_ids)
SHARED851 = {}
COVERAGE_SHARED852 = {}
EQ851 = False

say_r41('TEST852 RESEARCH HYPOTHESES',
    'Preserve TEST852 correction and preservation while adding native evidence-coverage U '
    'and candidate-evidence relation R to the control junction. STOP is never Python-generated.')
say_r41('TEST852 ENGINE MODIFICATION',
    'Only the control/revision junction changes. Physical CUT3/H3/KV, NF4 loading, cache construction, '
    'RoPE accounting, BF16 execution, frozen weights and generation stopping remain inherited.')
say_r41('TEST852 NATIVE CONTROL MECHANISM',
    'BASELINE851 uses TEST852 C/E/Kprev. NATIVE852 uses C/E/Kprev plus native coverage U and '
    'relation R. MATCHED_CONTROL852 receives the identical U/R tensors with their slots swapped.')
say_r41('TEST852 MATHEMATICAL DESIGN',
    'U=Psi(T_theta(P_coverage;M)); R=[mean(C)-mean(E),mean(C)+mean(E)]. '
    'K=F_native(C,E,Kprev,U,R,Q), A=G_native(K), C_next=H_native(C,E,K,U,R). '
    'U is an additional same-model native computation; R is fixed tensor arithmetic, not a decision.')
say_r41('TEST852 EXPERIMENTAL PANEL',
    '12 jobs = 2 worlds x 2 evidence conditions x 3 arms; world 1 NATURAL, world 2 COUNTERFACTUAL; '
    'maximum 2 reviews/job; no teacher-forced diagnostic forwards. PANEL_SHA256='+PANEL_SHA851)


def fingerprint851(ids):
    return hashlib.sha256(json.dumps(list(ids)).encode()).hexdigest()


def joined851(segments):
    rows = [r for _, r in segments if r is not None and len(r)]
    return (torch.cat(rows, dim=0).float().cpu().contiguous() if rows
        else torch.zeros((0, H), dtype=torch.float32))


def make_x851(pre, segments, post):
    parts = [embed841(pre)]
    checks = []
    for slot, rows in segments:
        if slot:
            parts.append(embed841(slot))
        if rows is not None and len(rows):
            assert rows.ndim == 2 and rows.shape[1] == H
            assert rows.device.type == 'cpu' and rows.dtype == torch.float32
            assert torch.isfinite(rows).all().item()
            start = sum(int(p.shape[0]) for p in parts)
            parts.append(rows.to(device=DEV, dtype=DTYPE))
            checks.append((start, rows))
    if post:
        parts.append(embed841(post))
    X = torch.cat(parts, dim=0)
    assert X.dtype == DTYPE and X.device.type == 'cuda' and X.shape[1] == H
    return X, checks


@torch.no_grad()
def gen851(memx, pre, segments, post):
    budget849()
    X, checks = make_x851(pre, segments, post)
    L = int(X.shape[0])
    n = int(memx[0][0].shape[-2])
    assert n + L + K845 <= MAX_FUSED_TOKENS, ('CONTEXT_LIMIT', n, L)
    transfers = []
    for start, rows in checks:
        transfers.append(continuity849(rows, X, start))
    transfer = {'segments': transfers,
        'exact_after_bf16': all(t['exact_after_bf16'] for t in transfers)}
    cache = cache_build(list(memx))
    pos = torch.arange(n, n + L, device=DEV)
    out = model(inputs_embeds=X.reshape(1, L, H), past_key_values=cache,
        attention_mask=torch.ones((1, n + L), device=DEV, dtype=torch.long),
        position_ids=pos.unsqueeze(0), cache_position=pos,
        use_cache=True, return_dict=True)
    # CausalLMOutputWithPast supplies logits. The decision state K is the
    # native soft-row rollout; no optional hidden-state output or hook is used.
    logits = out.logits[0, -1].float()
    del out
    COUNT834['probe_forwards'] += 1
    R, toks, info = [], [], []
    for t in range(K845):
        p = torch.softmax(logits, dim=-1)
        top = torch.topk(p, 20)
        info.append({'ids': [int(x) for x in top.indices.tolist()],
            'p': [round(float(x), 7) for x in top.values.tolist()],
            'H': round(float(-(p * p.clamp_min(1e-30).log()).sum()), 5)})
        toks.append(info[-1]['ids'][0])
        if end845(toks[-1]):
            break
        v = (p.to(E841.dtype).reshape(1, -1) @ E841).reshape(-1)
        R.append(v.to(DTYPE))
        if t + 1 < K845:
            x = n + L + t
            out = model(inputs_embeds=v.to(DTYPE).reshape(1, 1, H),
                past_key_values=cache,
                attention_mask=torch.ones((1, x + 1), device=DEV, dtype=torch.long),
                position_ids=torch.tensor([[x]], device=DEV),
                cache_position=torch.tensor([x], device=DEV),
                use_cache=True, return_dict=True)
            logits = out.logits[0, -1].float()
            del out
            COUNT834['generation_forwards'] += 1
    del cache
    kend = len(R)
    text = tok.decode([t_ for t_ in toks if not end845(t_)])
    rows = torch.stack(R).float().cpu() if R else torch.zeros((0, H))
    return {'rows': rows, 'text': text, 'toks': toks[:kend],
        'tok1': toks[0], 'p1': info[0]['p'][0], 'H1': info[0]['H'],
        'top1': info[0], 'kend': kend,
        'control_hidden': None,
        'trace849': trace849(toks, info, joined851(segments), transfer)}


def invoke851(memx, pre, segments, post, stage, tensors, traces, baseline=False):
    rows = None if baseline else joined851(segments)
    if baseline:
        assert len(segments) == 1
        rows = segments[0][1]
        h = gen849(memx, pre, rows, post)
    else:
        h = gen851(memx, pre, segments, post)
    stats849(h['rows'])
    tensors[stage+'_input'] = (np.empty((0, H), dtype=np.float32)
        if rows is None else rows.detach().cpu().numpy().copy())
    tensors[stage+'_output'] = h['rows'].numpy().copy()
    traces.append({'stage': stage, 'prompt_sha256': fingerprint851(pre),
        'suffix_sha256': fingerprint851(post or []),
        'segments': [{'slot_sha256': fingerprint851(slot or []),
            'state': stats849(rows)} for slot, rows in segments],
        'result': result849(h)})
    return h


def intervened851(arm, C, E):
    # Retain the locked TEST852 C/E interface without the former row-order arms.
    assert arm in ARMS851
    return C.contiguous(), E.contiguous()


def pooled852(rows):
    assert rows.ndim == 2 and rows.shape[1] == H
    assert rows.device.type == 'cpu' and rows.dtype == torch.float32
    if not len(rows):
        return torch.zeros((H,), dtype=torch.float32)
    return rows.mean(dim=0)


def relation852(C, E):
    # Fixed, oracle-free numerical interaction. Both rows are derived solely
    # from native model states; no correctness or sufficiency label is computed.
    c, e = pooled852(C), pooled852(E)
    R = torch.stack((c-e, c+e), dim=0).contiguous()
    assert R.shape == (2, H) and R.dtype == torch.float32
    assert torch.isfinite(R).all().item()
    return R


def route852(arm, U, R):
    # Matched control preserves tensors, total rows, dtype and global norm;
    # only the semantic U/R slot routing is causally disrupted.
    if arm == 'NATIVE852':
        return U, R
    assert arm == 'MATCHED_CONTROL852'
    return R, U


@torch.no_grad()
def coverage_state852(q, condition, mode, memx):
    key = (q, condition, mode)
    if key not in COVERAGE_SHARED852:
        COVERAGE_SHARED852[key] = gen849(memx,
            list(prompt_ids(COVERAGE852.format(q=QTEXT841[q]))),
            None, COVERAGE_SUFFIX852)
    return COVERAGE_SHARED852[key]


def shared851(q, condition, mode, memx):
    global EQ851, UPPER_CHECK841
    key = (q, condition, mode)
    if key in SHARED851:
        return SHARED851[key]
    pre = list(prompt_ids(FR845['hop0'].format(q=QTEXT841[q]))) + SLOT845[3]
    if not EQ851:
        with CallCount841() as cc:
            first = gen849(memx, pre, None, None)
        UPPER_CHECK841 = cc.summary()
        gate829('CUT3_UPPER_LAYER_EXECUTION',
            UPPER_CHECK841['upper_min'] >= 1 and UPPER_CHECK841['lm_head'] >= 1,
            UPPER_CHECK841)
        old = gen845(memx, pre, None, None)
        equal = (old['text'] == first['text'] and old['toks'] == first['toks']
            and torch.equal(old['rows'], first['rows']))
        gate829('TEST852_OBSERVATIONAL_GENERATOR_EQUALITY', equal, {})
        assert equal
        EQ851 = True
    else:
        first = gen849(memx, pre, None, None)
    candidate = None
    if mode == 'NATURAL':
        candidate = gen849(memx,
            list(prompt_ids(FR845['hop'].format(q=QTEXT841[q]))) + SLOT845[1],
            first['rows'], SLOT845[2])
    evidence = gen849(memx,
        list(prompt_ids(EVIDENCE851.format(q=QTEXT841[q]))),
        None, ANSWER_SUFFIX851)
    initial = first if mode == 'COUNTERFACTUAL' else candidate
    assert initial is not None and initial['rows'].shape[1] == H
    SHARED851[key] = {'first': first, 'natural_candidate': candidate,
        'evidence': evidence, 'initial': initial}
    return SHARED851[key]


for ji846, j846 in enumerate(JOBS841):
    j851 = j846
    if j851['job'] in REC841:
        continue
    begun851 = time.perf_counter()
    tensors851, traces851, cycles851 = {}, [], []
    q851, arm851 = j851['qid'], j851['arm']
    condition851, mode851 = j851['intervention'], MODE851[q851]
    mem851 = list(j851['initial_cards'])
    assert len(mem851) <= CAP845
    accepted851, end851 = None, None
    current851 = None
    transitions851 = 0
    try:
        budget849()
        mx851 = memx_r41(mem851)
        shared = shared851(q851, condition851, mode851, mx851)
        first851 = shared['first']
        initial851 = shared['initial']
        evidence851 = shared['evidence']
        coverage_h852 = None
        if arm851 != 'BASELINE851':
            coverage_h852 = coverage_state852(q851, condition851, mode851, mx851)
        current851 = initial851
        tensors851['first_rows'] = first851['rows'].numpy().copy()
        tensors851['initial_candidate'] = initial851['rows'].numpy().copy()
        tensors851['evidence_rows'] = evidence851['rows'].numpy().copy()
        if coverage_h852 is not None:
            tensors851['coverage_rows'] = coverage_h852['rows'].numpy().copy()
        previous_control851 = None
        for cycle851 in range(MAX_REVIEWS851):
            candidate851 = current851
            C851, E851 = intervened851(arm851, candidate851['rows'], evidence851['rows'])
            relation_rows852, routed_u852, routed_r852 = None, None, None
            if arm851 == 'BASELINE851':
                pre851 = list(prompt_ids(REVIEW851.format(q=QTEXT841[q851])))
                segments851 = [(C_SLOT851, C851), (E_SLOT851, E851)]
                if previous_control851 is not None:
                    segments851.append((K_SLOT851, previous_control851['rows']))
                review851 = invoke851(mx851, pre851, segments851, REVIEW_SUFFIX851,
                    'review_%d'%cycle851, tensors851, traces851)
            else:
                relation_rows852 = relation852(C851, E851)
                routed_u852, routed_r852 = route852(
                    arm851, coverage_h852['rows'], relation_rows852)
                pre851 = list(prompt_ids(REVIEW851.format(q=QTEXT841[q851])))
                segments851 = [(C_SLOT851, C851), (E_SLOT851, E851)]
                if previous_control851 is not None:
                    segments851.append((K_SLOT851, previous_control851['rows']))
                segments851.extend([(U_SLOT852, routed_u852), (R_SLOT852, routed_r852)])
                review851 = invoke851(mx851, pre851, segments851, REVIEW_SUFFIX851,
                    'review_%d'%cycle851, tensors851, traces851)
            action851 = parse849(review851['text'])
            repetition851 = bool(cycles851 and
                cycles851[-1]['action'] == action851 and
                cycles851[-1]['candidate']['output']['sha256'] == result849(candidate851)['output']['sha256'])
            event851 = {
                'cycle': cycle851, 'candidate': result849(candidate851),
                'candidate_intervened': stats849(C851),
                'evidence': result849(evidence851),
                'evidence_intervened': stats849(E851),
                'coverage_native': None if coverage_h852 is None else result849(coverage_h852),
                'relation_state': None if relation_rows852 is None else stats849(relation_rows852),
                'routed_coverage_state': None if routed_u852 is None else stats849(routed_u852),
                'routed_relation_state': None if routed_r852 is None else stats849(routed_r852),
                'previous_control': None if previous_control851 is None else result849(previous_control851),
                'review': result849(review851), 'action': action851,
                'control_token_ids': review851['trace849']['all_token_ids'],
                'control_token_scores': review851['trace849']['token_top20'],
                'revision': None, 'python_action': 'APPLY_MODEL_'+action851,
                'model_native_action': action851,
                'loop_repetition': repetition851,
                'recurrent_previous_control': previous_control851 is not None
            }
            if previous_control851 is not None:
                recurrent_segments851 = [rows for slot, rows in segments851 if slot == K_SLOT851]
                assert len(recurrent_segments851) == 1
                assert recurrent_segments851[0].shape == previous_control851['rows'].shape
                assert stats849(recurrent_segments851[0])['sha256'] == cycles851[-1]['review']['output']['sha256']
            if action851 == 'CONTINUE':
                accepted851, end851 = candidate851, 'MODEL_ACCEPT'
            elif action851 == 'STOP':
                end851 = 'MODEL_STOP'
            elif action851 == 'REVISE':
                transitions851 += 1
                recompute_pre851 = list(prompt_ids(RECOMPUTE851.format(q=QTEXT841[q851])))
                if arm851 == 'BASELINE851':
                    current851 = invoke851(mx851, recompute_pre851,
                        [(C_SLOT851, C851), (K_SLOT851, review851['rows']),
                         (E_SLOT851, E851)], ANSWER_SUFFIX851,
                        'revision_%d'%cycle851, tensors851, traces851)
                else:
                    current851 = invoke851(mx851, recompute_pre851,
                        [(C_SLOT851, C851), (K_SLOT851, review851['rows']),
                         (E_SLOT851, E851), (U_SLOT852, routed_u852),
                         (R_SLOT852, routed_r852)], ANSWER_SUFFIX851,
                        'revision_%d'%cycle851, tensors851, traces851)
                event851['revision'] = result849(current851)
            else:
                end851 = 'PROTOCOL_INVALID'
                event851['python_action'] = 'PROTOCOL_INVALID_NO_FOLLOWUP'
            cycles851.append(event851)
            say_r41('TEST852 CANDIDATE STATE', q851, condition851, mode851, arm851,
                'CYCLE='+str(cycle851), json.dumps(event851['candidate_intervened']))
            say_r41('TEST852 EVIDENCE STATE', q851, condition851, arm851,
                json.dumps({'E':event851['evidence_intervened'],
                    'U':event851['routed_coverage_state'], 'R':event851['routed_relation_state']}))
            say_r41('TEST852 CONTROL STATE', q851, condition851, arm851,
                'CYCLE='+str(cycle851), json.dumps({'soft_rows':event851['review']['output'],
                    'coverage_text':None if coverage_h852 is None else coverage_h852['text'],
                    'final_hidden':event851['review'].get('control_hidden')}))
            say_r41('TEST852 MODEL DECISION', q851, condition851, mode851, arm851,
                'CYCLE='+str(cycle851), action851, 'TOKENS='+str(event851['control_token_ids']),
                'REVIEW='+repr(review851['text']))
            say_r41('TEST852 NUMERICAL FEEDBACK', q851, arm851, 'CYCLE='+str(cycle851),
                'REVISION='+repr(None if event851['revision'] is None else event851['revision']['text']))
            say_r41('TEST852 RECURRENT FEEDBACK', q851, arm851, 'CYCLE='+str(cycle851),
                'KPREV='+str(event851['recurrent_previous_control']),
                json.dumps(review851['trace849']['continuity']))
            say_r41('TEST852 LOOP COLLAPSE DIAGNOSTICS', q851, arm851,
                'CYCLE='+str(cycle851), 'REPETITION='+str(repetition851))
            say_r41('TEST852 MODEL SIGNAL VS PYTHON ACTION', q851, arm851,
                action851, event851['python_action'])
            if end851 is not None:
                break
            previous_control851 = review851
        if end851 is None:
            end851 = 'MECHANICAL_REVIEW_LIMIT'
        rec851 = {
            'job': j851['job'], 'world_id': q851, 'qid': q851, 'arm': arm851,
            'condition': condition851, 'initial_mode': mode851,
            'mounted_cards': mem851, 'mounted_count': len(mem851),
            'first': result849(first851), 'initial': result849(initial851),
            'evidence_native': result849(evidence851), 'cycles': cycles851,
            'traces': traces851, 'end': end851,
            'answer': None if accepted851 is None else result849(accepted851),
            'final_candidate': result849(current851),
            'feedback_transition_count': transitions851,
            'model_stop': end851 == 'MODEL_STOP',
            'mechanical_stop_reason': end851 if end851 in (
                'MECHANICAL_REVIEW_LIMIT', 'PROTOCOL_INVALID') else None,
            'wrong_candidate_opportunity': 'OFFLINE_ONLY',
            'evidence_groundedness': 'OFFLINE_ONLY',
            'seconds': time.perf_counter()-begun851,
            'peak_gpu_gib': torch.cuda.max_memory_allocated()/1024**3
        }
    except BudgetR41 as error851:
        BUDGET_STOP841 = True
        rec851 = {'job':j851['job'], 'world_id':q851, 'qid':q851, 'arm':arm851,
            'condition':condition851, 'initial_mode':mode851,
            'mounted_cards':mem851, 'cycles':cycles851, 'traces':traces851,
            'end':'MECHANICAL_RESOURCE_LIMIT', 'answer':None,
            'final_candidate':None if current851 is None else result849(current851),
            'feedback_transition_count':transitions851, 'model_stop':False,
            'mechanical_stop_reason':str(error851),
            'seconds':time.perf_counter()-begun851,
            'peak_gpu_gib':torch.cuda.max_memory_allocated()/1024**3}
    REC841[j851['job']], ROWS841[j851['job']] = rec851, tensors851
    save_job841(j851['job'], rec851, tensors851)
    say_r41('TEST852 JOB-BY-JOB RESULTS', q851, condition851, mode851, arm851,
        'END='+rec851['end'],
        'ANSWER='+repr(None if rec851['answer'] is None else rec851['answer']['text']),
        'SECONDS=%.2f'%rec851['seconds'],
        'PEAK_GIB=%.3f'%rec851['peak_gpu_gib'])
    if BUDGET_STOP841:
        break
while LRU_R41:
    evict_r41()
# Diagnose, never suppress or clear, any residual layer hook before the
# inherited final integrity gate. Hook registration remains prohibited.
residual_hooks851 = []
for layer_index851 in range(NL):
    layer851 = model.model.layers[layer_index851]
    for hook_kind851 in ('_forward_pre_hooks', '_forward_hooks'):
        for hook_handle851, hook851 in getattr(layer851, hook_kind851).items():
            residual_hooks851.append({'layer':layer_index851,
                'kind':hook_kind851, 'handle':str(hook_handle851),
                'hook_type':type(hook851).__name__})
D829['test852_residual_hook_audit'] = residual_hooks851
log829('TEST852_RESIDUAL_HOOK_AUDIT', json.dumps(residual_hooks851))
gate829('TEST852_NO_RESIDUAL_HOOKS_BEFORE_FINAL', not residual_hooks851,
    residual_hooks851)
D829['run_seconds841'] = time.perf_counter()-t_run841
D829['memo851'] = dict(CNT_R41, states=len(SIG_R41), echo_states=len(ECHO_R41),
    hop=CNT845['hop'], hop_hit=CNT845['hop_hit'])
D829['panel852_sha256'] = PANEL_SHA851
'''

OFF851 = r'''
# Inherited TEST848 builder requires this exact offline marker.
log829('TEST846P_OFFLINE_START')
log829('TEST852_OFFLINE_START')

def node851(value, world):
    text = str(value or '').strip().upper().rstrip('.')
    keys = ('start', 'middle', 'end', 'changed_end', 'fork_end', 'decoy_end',
        'bridge_mid', 'bridge_end', 'end3')
    hits = [k for k in keys if world.get(k) and text == str(world[k]).strip().upper()]
    return hits[0] if len(hits) == 1 else 'UNKNOWN' if text == 'UNKNOWN' else 'OTHER'


def supported851(value, world, mounted):
    c = node851(value, world)
    ids = world['ids']
    return bool(ids['first'] in mounted and
        ((c == 'end' and ids['second'] in mounted) or
         (c == 'changed_end' and ids['changed'] in mounted)))


def revise_indicator851(record):
    return int(bool(record['cycles']) and record['cycles'][0]['action'] == 'REVISE')


cases851, groups851 = [], []
for j in JOBS841:
    if j['job'] not in REC841:
        continue
    r = REC841[j['job']]
    assert QID841.count(j['qid']) == 1, ('OFFLINE_QID_NOT_UNIQUE', j['qid'])
    wi = QID841.index(j['qid'])
    assert wi in PILOT_WORLDS846
    assert r['job'] == j['job'] and r['qid'] == j['qid']
    assert r['arm'] == j['arm'] and r['condition'] == j['intervention']
    assert r['initial_mode'] == MODE851[j['qid']]
    assert list(r['mounted_cards']) == list(j['initial_cards'])
    w = worlds829[wi]
    mounted = set(r['mounted_cards'])
    sufficient = w['ids']['first'] in mounted and bool(
        {w['ids']['second'], w['ids']['changed']} & mounted)
    answer = None if r.get('answer') is None else r['answer']['text']
    initial = None if r.get('initial') is None else r['initial']['text']
    initial_grounded = supported851(initial, w, mounted)
    initial_wrong = node851(initial, w) in (
        'start', 'middle', 'fork_end', 'decoy_end', 'bridge_mid', 'bridge_end', 'end3')
    grounded = supported851(answer, w, mounted)
    events = []
    for e in r['cycles']:
        candidate = e['candidate']['text']
        revision = e['revision']
        revision_grounded = revision is not None and supported851(revision['text'], w, mounted)
        events.append({'cycle':e['cycle'], 'candidate_class':node851(candidate,w),
            'candidate_grounded':supported851(candidate,w,mounted),
            'candidate_wrong':node851(candidate,w) in (
                'start','middle','fork_end','decoy_end','bridge_mid','bridge_end','end3'),
            'action':e['action'], 'revision_grounded':revision_grounded,
            'loop_repetition':e['loop_repetition'],
            'coverage_text':None if e.get('coverage_native') is None else e['coverage_native']['text'],
            'relation':e.get('relation_state')})
    correction = bool(initial_wrong and grounded and r['end'] == 'MODEL_ACCEPT' and
        any(e['candidate_wrong'] and e['action'] == 'REVISE' and e['revision_grounded']
            for e in events))
    error_signal = bool(initial_wrong and r['cycles'] and
        r['cycles'][0]['action'] == 'REVISE')
    preservation = bool(r['initial_mode'] == 'NATURAL' and sufficient and
        initial_grounded and grounded and r['end'] == 'MODEL_ACCEPT' and
        not any(e['action'] == 'REVISE' for e in r['cycles']))
    unnecessary_revision = bool(initial_grounded and
        any(e['action'] == 'REVISE' for e in r['cycles']))
    case = {'world':wi, 'world_id':r['world_id'], 'condition':r['condition'],
        'mode':r['initial_mode'], 'arm':r['arm'], 'end':r['end'],
        'initial':initial, 'initial_class':node851(initial,w),
        'initial_grounded':initial_grounded, 'wrong_candidate_opportunity':initial_wrong,
        'answer':answer, 'grounded':grounded, 'sufficient':sufficient,
        'error_signal':error_signal, 'correction':correction,
        'correct_preservation':preservation, 'unnecessary_revision':unnecessary_revision,
        'correct_stop':r['end'] == 'MODEL_STOP' and not sufficient,
        'false_stop':r['end'] == 'MODEL_STOP' and sufficient,
        'unsupported_completion':answer is not None and bool(answer.strip())
            and node851(answer,w) != 'UNKNOWN' and not grounded,
        'model_stop':r.get('model_stop',False),
        'mechanical_stop':r.get('mechanical_stop_reason') is not None,
        'feedback_transition_count':r.get('feedback_transition_count',0),
        'loop_repetition':any(e['loop_repetition'] for e in events),
        'events':events}
    cases851.append(case)

records851 = [REC841[j['job']] for j in JOBS841 if j['job'] in REC841]
for q in QORDER851:
    for condition in ('INTACT', 'REMOVED'):
        group = {r['arm']:r for r in records851
            if r['qid'] == q and r['condition'] == condition}
        if set(group) != set(ARMS851) or not all(group[a]['cycles'] for a in ARMS851):
            continue
        baseline = group['BASELINE851']
        native = group['NATIVE852']
        matched = group['MATCHED_CONTROL852']
        n0, m0 = native['cycles'][0], matched['cycles'][0]
        state_change = (n0['review']['output']['sha256'] != m0['review']['output']['sha256'])
        decision_change = (n0['action'] != m0['action'] or
            n0['control_token_ids'] != m0['control_token_ids'])
        score_change = abs(n0['review']['p1'] - m0['review']['p1']) > 1e-7
        # Verify that the matched arm received the same U/R values, cross-routed.
        assert n0['routed_coverage_state']['sha256'] == m0['routed_relation_state']['sha256']
        assert n0['routed_relation_state']['sha256'] == m0['routed_coverage_state']['sha256']
        assert n0['coverage_native']['output']['sha256'] == m0['coverage_native']['output']['sha256']
        groups851.append({'qid':q, 'condition':condition, 'mode':native['initial_mode'],
            'state_change':state_change, 'decision_change':decision_change,
            'score_change':score_change,
            'causal_observation':state_change and (decision_change or score_change),
            'actions':{a:group[a]['cycles'][0]['action'] for a in ARMS851},
            'native_vs_baseline_action_changed':n0['action'] != baseline['cycles'][0]['action'],
            'native_correction':any(c['correction'] for c in cases851
                if c['world_id']==q and c['condition']==condition and c['arm']=='NATIVE852'),
            'native_preservation':any(c['correct_preservation'] for c in cases851
                if c['world_id']==q and c['condition']==condition and c['arm']=='NATIVE852'),
            'native_correct_stop':any(c['correct_stop'] for c in cases851
                if c['world_id']==q and c['condition']==condition and c['arm']=='NATIVE852')})

summary851 = {a:{k:sum(bool(c[k]) for c in cases851 if c['arm'] == a)
    for k in ('grounded','wrong_candidate_opportunity','error_signal','correction',
        'correct_preservation','unnecessary_revision','correct_stop','false_stop',
        'unsupported_completion','model_stop','mechanical_stop','loop_repetition')}
    for a in ARMS851}
complete851 = len(cases851) == 12 and len(groups851) == 4 and not BUDGET_STOP841
protocol_invalid852 = any(r['end'] == 'PROTOCOL_INVALID' for r in records851)
checks851 = D829.get('checks',[])
physical851 = bool(checks851) and all(c['pass'] for c in checks851)
transfers851 = [t['result']['trace849']['continuity']
    for r in records851 for t in r['traces']]
transfer_pass851 = bool(transfers851) and all(
    t.get('exact_after_bf16',False) for t in transfers851)
recurrent_edges851 = sum(e['recurrent_previous_control']
    for r in records851 if r['arm'] == 'NATIVE852' for e in r['cycles'])
wrong_native852 = summary851['NATIVE852']['wrong_candidate_opportunity']
causal852 = any(g['causal_observation'] for g in groups851)
decision_causal852 = any(g['decision_change'] for g in groups851)
action_variation851 = len({e['action'] for r in records851
    if r['arm'] == 'NATIVE852' for e in r['cycles']}) > 1
metrics852 = ('correction','correct_preservation','correct_stop')
control_specific852 = (
    all(summary851['NATIVE852'][k] >= summary851['MATCHED_CONTROL852'][k] for k in metrics852)
    and any(summary851['NATIVE852'][k] > summary851['MATCHED_CONTROL852'][k] for k in metrics852))
baseline_benefit852 = any(summary851['NATIVE852'][k] > summary851['BASELINE851'][k]
    for k in metrics852)
retained852 = (summary851['NATIVE852']['correction'] >= summary851['BASELINE851']['correction']
    and summary851['NATIVE852']['correct_preservation'] >= summary851['BASELINE851']['correct_preservation']
    and summary851['NATIVE852']['unnecessary_revision'] <= summary851['BASELINE851']['unnecessary_revision'])
correction_pass851 = summary851['NATIVE852']['correction'] > 0
preservation_pass851 = (summary851['NATIVE852']['correct_preservation'] > 0
    and summary851['NATIVE852']['unnecessary_revision'] == 0)
stop_pass851 = (summary851['NATIVE852']['correct_stop'] > 0
    and summary851['NATIVE852']['false_stop'] == 0)
discrimination851 = action_variation851 and baseline_benefit852 and control_specific852
verdicts851 = {
    'SOURCE_INTEGRITY':'PASS',
    'PHYSICAL_MEMORY_INTEGRITY':'PASS' if physical851 else 'FAIL',
    'NATIVE_BYPASS_INTEGRITY':'PASS' if physical851 and UPPER_CHECK841.get('upper_min',0) >= 1 else 'INCONCLUSIVE',
    'NUMERICAL_STATE_CONTINUITY':'PASS' if transfer_pass851 else 'INCONCLUSIVE',
    'NATIVE_CONTROL_COUPLING':'PASS' if transfer_pass851 and any(
        r['arm'] == 'NATIVE852' and len(r['traces']) for r in records851) else 'INCONCLUSIVE',
    'TASK_RELEVANT_DECISION_DISCRIMINATION':'PRELIMINARY_PILOT_SIGNAL' if discrimination851 else 'NOT_DEMONSTRATED',
    'MODEL_NATIVE_PRESERVATION':'PRELIMINARY_OBSERVED' if preservation_pass851 else 'NOT_DEMONSTRATED',
    'MODEL_NATIVE_ERROR_SIGNAL':'PRELIMINARY_OBSERVED' if summary851['NATIVE852']['error_signal'] else
        ('NOT_EVALUABLE_NO_WRONG_CANDIDATE' if not wrong_native852 else 'NOT_OBSERVED'),
    'MODEL_NATIVE_CORRECTION':'PRELIMINARY_OBSERVED' if correction_pass851 else
        ('NOT_EVALUABLE_NO_WRONG_CANDIDATE' if not wrong_native852 else 'NOT_OBSERVED'),
    'MODEL_NATIVE_STOP':'PRELIMINARY_OBSERVED' if stop_pass851 else 'NOT_DEMONSTRATED',
    'MODEL_NATIVE_RESEARCH_REQUEST':'NOT_IMPLEMENTED_PROTOCOL_UNCHANGED',
    'NATIVE_RECURRENT_FEEDBACK':'PASS' if recurrent_edges851 and transfer_pass851 else 'NOT_DEMONSTRATED',
    'AUTONOMOUS_RECURSIVE_REASONING':('PRELIMINARY_SINGLE_PANEL_SIGNAL'
        if all((discrimination851,recurrent_edges851,correction_pass851,preservation_pass851,stop_pass851,retained852))
        else 'NOT_DEMONSTRATED')
}
if not complete851:
    final_verdict851 = 'INCOMPLETE'
elif protocol_invalid852:
    final_verdict851 = 'PROTOCOL_INVALID'
elif not retained852:
    final_verdict851 = 'TEST852_GAINS_REGRESSED'
elif all((stop_pass851,correction_pass851,preservation_pass851,control_specific852,decision_causal852)):
    final_verdict851 = 'PRELIMINARY_NATIVE_STOP_CORRECTION_PRESERVATION_SIGNAL'
elif correction_pass851 and preservation_pass851:
    final_verdict851 = 'PRELIMINARY_COUPLING_RETAINED_STOP_NOT_DEMONSTRATED'
else:
    final_verdict851 = 'NO_CONFIRMED_TASK_RELEVANT_CONTROL_REVISION'

for c in cases851:
    if c['arm'] == 'NATIVE852':
        say_r41('TEST852 WRONG CANDIDATE OPPORTUNITY', json.dumps({
            'world':c['world_id'], 'condition':c['condition'], 'mode':c['mode'],
            'initial_class':c['initial_class'], 'wrong':c['wrong_candidate_opportunity']}))
        say_r41('TEST852 CORRECTION RESULT', json.dumps({
            'world':c['world_id'], 'condition':c['condition'],
            'error_signal':c['error_signal'], 'correction':c['correction'], 'events':c['events']}))
        say_r41('TEST852 PRESERVATION RESULT', json.dumps({
            'world':c['world_id'], 'condition':c['condition'],
            'preservation':c['correct_preservation'], 'unnecessary_revision':c['unnecessary_revision']}))
        say_r41('TEST852 MODEL STOP RESULT', json.dumps({
            'world':c['world_id'], 'condition':c['condition'], 'sufficient':c['sufficient'],
            'correct_stop':c['correct_stop'], 'false_stop':c['false_stop'],
            'unsupported_completion':c['unsupported_completion']}))
        say_r41('TEST852 MECHANICAL STOP RESULT', json.dumps({
            'world':c['world_id'], 'condition':c['condition'], 'end':c['end'],
            'mechanical_stop':c['mechanical_stop']}))
for g in groups851:
    say_r41('TEST852 MATCHED CONTROL COMPARISON', json.dumps(g))
    say_r41('TEST852 CAUSAL EFFECT', json.dumps({k:g[k] for k in (
        'qid','condition','state_change','decision_change','score_change','causal_observation')}))
say_r41('TEST852 HARDWARE PREFLIGHT',
    'PASS' if physical851 else 'FAIL',
    'Inherited one-CUDA A100, Qwen2.5-72B NF4, 80 layers, H=8192, BF16 and frozen-weight gates.')
say_r41('TEST852 PHYSICAL MEMORY INTEGRITY',
    'PASS' if physical851 else 'FAIL', 'Mounted cards are identical within every matched three-arm group.')
say_r41('TEST852 FAILURE ANALYSIS',
    'U/R state or score changes alone are not STOP or task success. Mechanical limits are not model STOP. '
    'Slot swapping preserves values and total rows but does not prove generalization. '
    'TEST852 non-regression and this 12-job pilot do not establish population superiority. '
    'Summary='+json.dumps(summary851))
next851 = ('If STOP remains absent while correction/preservation are retained, inspect whether U changes '
    'the native decision rather than adding loops. If matched routing has no decision effect, reject this '
    'U/R junction. Research request remains unimplemented; do not claim it.')
say_r41('TEST852 NEXT ENGINEERING STEP', next851)
say_r41('TEST852 FINAL SCIENTIFIC VERDICT', final_verdict851, json.dumps(verdicts851))
report851 = ('TEST852 completed %d/12 jobs; %d matched groups; NATIVE852 wrong opportunities=%d; '
    'recurrent Kprev edges=%d; U/R causal observations=%s; decision changes=%s; verdict=%s. '
    'GPU results are established only by this executed run.') % (
        len(cases851),len(groups851),wrong_native852,recurrent_edges851,
        causal852,decision_causal852,final_verdict851)
D829['test852'] = {'cases':cases851, 'matched_groups':groups851, 'summary':summary851,
    'panel_sha256':PANEL_SHA851, 'source_locks':dict(LOCKS849,
        **{'849.py':'01a6ac43cbc954cc2f6ceaf8cf0238333ec762b1',
           '850.py':'79cc5ab211c01b37324e2d6897a298e84db42101',
           '851.py':'0f01e73b9ad160c988cfe059e8b5ae5e1f35f65b'}),
    'verdicts':verdicts851, 'final_verdict':final_verdict851, 'report':report851,
    'protocol_invalid':protocol_invalid852, 'native_calls':CALLS849}
D829['verdict841R'] = {'decision':final_verdict851, 'verdicts':verdicts851,
    'budget_stop':BUDGET_STOP841, 'reason':'Pre-registered 12-job TEST852 U/R control panel.'}
D829['cost841R'] = {'counted':dict(COUNT834), 'native_calls':CALLS849,
    'run_seconds':D829['run_seconds841'],
    'peak_gpu_gib':max([r['peak_gpu_gib'] for r in records851] or [0.0])}
D829['status'] = 'COMPLETE_TEST852' if complete851 else 'PARTIAL_TEST852'
json.dumps(D829, ensure_ascii=False, default=str, allow_nan=False)
save829()
import os
artifact851 = str(OUT829)
artifact_sha851 = (hashlib.sha256(open(artifact851,'rb').read()).hexdigest()
    if os.path.isfile(artifact851) else None)
say_r41('TEST852 ARTIFACT SHA256', artifact851, artifact_sha851,
    'PANEL_SHA256='+PANEL_SHA851)
log829('TEST852_COMPLETED', str(OUT829), final_verdict851)
'''

# Relabel only TEST851 display/gate strings; variable names and locked interfaces remain.
source852 = source852.replace('TEST851', 'TEST852')
source852 = replace_block852(source852, 'BODY851', BODY851)
source852 = replace_block852(source852, 'OFF851', OFF851)
source852 = once852(source852,
    (chr(92)*3) + '"(' + "'BASELINE', 'COUPLED_NATIVE', 'MATCHED_CONTROL', 'CANDIDATE_ABLATION', 'EVIDENCE_ABLATION'" + ')' + (chr(92)*3) + '"',
    (chr(92)*3) + '"(' + "'BASELINE851', 'NATIVE852', 'MATCHED_CONTROL852'" + ')' + (chr(92)*3) + '"')
source852 = once852(source852,
    "a.value='PANEL: TEST849-R2; 20 jobs | BASELINE / COUPLED_NATIVE / MATCHED_CONTROL / CANDIDATE_ABLATION / EVIDENCE_ABLATION'",
    "a.value='PANEL: TEST849-R2; 12 jobs | BASELINE851 / NATIVE852 / MATCHED_CONTROL852'")
source852 = source852.replace('PANEL: 20 jobs; 2 cycles maximum; no extra teacher-forced probes',
    'PANEL: 12 jobs; 2 cycles maximum; no extra teacher-forced probes')
source852 = once852(source852,
    '# Static verification before any inherited model-loading code is executed.',
    '\n# TEST852 changes only inherited panel cardinality; every source patch is unique.\nsource851 = once851(source851, \'lines[last_panel.end_lineno:last_panel.end_lineno] = [\\n    "PANEL849 = once849(PANEL849, \\\\"(\\\'LEGACY\\\', \\\'BOUNDARY\\\', \\\'CONTINUITY\\\', \\\'ORDER_CONTROL\\\', \\\'NO_STATE\\\')\\\\", "\\n    "\\\\"(\\\'BASELINE851\\\', \\\'NATIVE852\\\', \\\'MATCHED_CONTROL852\\\')\\\\")\\\\n"]\', \'lines[last_panel.end_lineno:last_panel.end_lineno] = [\\n    "PANEL849 = once849(PANEL849, \\\\"(\\\'LEGACY\\\', \\\'BOUNDARY\\\', \\\'CONTINUITY\\\', \\\'ORDER_CONTROL\\\', \\\'NO_STATE\\\')\\\\", "\\n    "\\\\"(\\\'BASELINE851\\\', \\\'NATIVE852\\\', \\\'MATCHED_CONTROL852\\\')\\\\")\\\\n",\\n    "PANEL849 = once849(PANEL849, \\\'assert len(JOBS841) == 20\\\', \\\'assert len(JOBS841) == 12\\\')\\\\n",\\n    "PANEL849 = once849(PANEL849, \\\\"assert len({j[\\\'job\\\'] for j in JOBS841}) == 20\\\\", "\\n    "\\\\"assert len({j[\\\'job\\\'] for j in JOBS841}) == 12\\\\")\\\\n"]\')\nsource851 = once851(source851, "source = replace_block(source, \'BODY849\', BODY_R2)", \'assert source.count("assert \\\'assert len(JOBS841) == 20\\\' in panel_text848") == 1\\nsource = source.replace("assert \\\'assert len(JOBS841) == 20\\\' in panel_text848",\\n    "assert \\\'assert len(JOBS841) == 12\\\' in panel_text848", 1)\\nsource = replace_block(source, \\\'BODY849\\\', BODY_R2)\')\n\n' + '# Static verification before any inherited model-loading code is executed.')

# Static verification before any inherited model-loading code is executed.
for block852 in (BODY851, OFF851):
    ast.parse(block852)
    compile(block852, '<TEST852_EMBEDDED>', 'exec')
body_tree852 = ast.parse(BODY851)
function852 = {n.name:n for n in body_tree852.body if isinstance(n, ast.FunctionDef)}
assert set(('gen851','invoke851','shared851','intervened851','relation852','route852','coverage_state852')) <= set(function852)
assert [a.arg for a in function852['gen851'].args.args] == ['memx','pre','segments','post']
assert [a.arg for a in function852['intervened851'].args.args] == ['arm','C','E']
assert [a.arg for a in function852['relation852'].args.args] == ['C','E']
assert [a.arg for a in function852['route852'].args.args] == ['arm','U','R']
assert 'out.last_hidden_state' not in BODY851
assert 'output_hidden_states' not in BODY851
assert 'out.hidden_states' not in BODY851
assert "'control_hidden': None" in BODY851
assert 'TEST852_NO_RESIDUAL_HOOKS_BEFORE_FINAL' in BODY851
names852 = {n.id for n in ast.walk(body_tree852) if isinstance(n, ast.Name)}
assert not names852 & {'EVALKEY841','CONTENT841','worlds829','card_meta829'}
assert BODY851.count('for ji846, j846 in enumerate(JOBS841)') == 1
assert "j['initial_mode']" not in BODY851 + OFF851
assert "j851['initial_mode']" not in BODY851 + OFF851
assert 'TEST846P_OFFLINE_START' in OFF851
assert 'register_forward_hook' not in BODY851
assert 'register_forward_pre_hook' not in BODY851
assert '.backward(' not in BODY851 and 'optimizer' not in BODY851.lower()
assert 'action_scores849(' not in BODY851
assert 'MAX_REVIEWS851 = 2' in BODY851
assert 'assert len(JOBS841) == 12' in BODY851
assert "ARMS851 = ('BASELINE851', 'NATIVE852', 'MATCHED_CONTROL852')" in BODY851
assert "'MODEL_NATIVE_RESEARCH_REQUEST':'NOT_IMPLEMENTED_PROTOCOL_UNCHANGED'" in OFF851
final_tree852 = ast.parse(source852)
compile(final_tree852, 'TEST852_LOCKED_BUILDER', 'exec')
print('TEST852 LOCKED ENGINE VERIFICATION')
print('WRAPPER AST: PASS | EMBEDDED COMPILE: PASS | PATCH UNIQUENESS: PASS')
print('FUNCTION SIGNATURES: PASS | RUNTIME ANSWER-KEY ISOLATION: PASS')
print('PANEL: 12 jobs; 2 cycles maximum; matched U/R slot-routing control')
print('BUILDER SHA256:', hashlib.sha256(source852.encode()).hexdigest())
print('GPU EXECUTION: NOT VERIFIED BY AUTHOR; only this Colab run can establish it', flush=True)
exec(compile(final_tree852, 'TEST852_LOCKED_BUILDER', 'exec'), globals())
