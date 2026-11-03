# AKBASCORE SILICON HIPPOCAMPUS — TEST851
# Model-native candidate/evidence/control coupling on the locked TEST850 chain.
# One Colab cell; one A100-SXM4-80GB; frozen Qwen2.5-72B-Instruct NF4.
# This source does not claim GPU execution. The run itself must establish every GPU result.
import ast, hashlib, json, urllib.request

URL851 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/850.py'
LOCK851 = '79cc5ab211c01b37324e2d6897a298e84db42101'
with urllib.request.urlopen(urllib.request.Request(
        URL851, headers={'User-Agent': 'AKBASCORE-TEST851'}), timeout=180) as response851:
    raw851 = response851.read(1000001)
actual851 = hashlib.sha1(
    b'blob ' + str(len(raw851)).encode() + b'\0' + raw851
).hexdigest()
assert actual851 == LOCK851, ('TEST850_PARENT_LOCK_FAILED', actual851, LOCK851)
source851 = raw851.decode('utf-8')
ast.parse(source851)
print('TEST851 SOURCE VERIFICATION')
print('850.py', actual851, 'PASS; inherited 841–849 locks are checked by the parent chain')


def replace_block851(source, name, value):
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


def once851(source, old, new):
    assert source.count(old) == 1, ('PATCH_NOT_UNIQUE', old[:120], source.count(old))
    return source.replace(old, new, 1)


BODY851 = r'''
ARMS851 = (
    'BASELINE', 'COUPLED_NATIVE', 'MATCHED_CONTROL',
    'CANDIDATE_ABLATION', 'EVIDENCE_ABLATION'
)
MAX_REVIEWS851 = 2
CALL_CAP849 = min(CALL_CAP849, 240)
HARD_BUDGET_MIN841 = min(HARD_BUDGET_MIN841, 60.0)
assert len(JOBS841) == 20
assert set(j['arm'] for j in JOBS841) == set(ARMS851)
QORDER851 = list(dict.fromkeys(j['qid'] for j in JOBS841))
assert len(QORDER851) == 2
# Pre-registered counterfactual: for the second world only, the model's actual
# one-link output state is used as the initial FINAL candidate. No answer text,
# answer key, target token, correctness label or externally written state enters.
MODE851 = {q: ('NATURAL' if i == 0 else 'COUNTERFACTUAL')
    for i, q in enumerate(QORDER851)}
# JOBS841 is referenced by PANEL829. Never mutate those shared dictionaries:
# initial_mode is derived from this immutable-by-convention TEST851 mapping.
for q in QORDER851:
    for condition in ('INTACT', 'REMOVED'):
        group = [j for j in JOBS841 if j['qid'] == q and j['intervention'] == condition]
        assert len(group) == 5
        assert len({tuple(j['initial_cards']) for j in group}) == 1
        assert len({tuple(j['bank']) for j in group}) == 1
        assert all(MODE851[j['qid']] == MODE851[q] for j in group)
PANEL_LOCK851 = {
    'test': 'TEST851', 'jobs': 20, 'arms': list(ARMS851),
    'worlds': list(QORDER851), 'conditions': ['INTACT', 'REMOVED'],
    'initial_modes': MODE851, 'max_reviews_per_job': MAX_REVIEWS851,
    'max_output_tokens_inherited_K845': K845,
    'native_call_cap': CALL_CAP849, 'hard_minutes': HARD_BUDGET_MIN841,
    'counterfactual': 'initial candidate = model hop0 output rows; no answer-key access',
    'ablations': {
        'CANDIDATE_ABLATION': 'reverse C row order only',
        'EVIDENCE_ABLATION': 'reverse E row order only',
        'MATCHED_CONTROL': 'reverse both C and E row order'
    },
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
SHARED851 = {}
EQ851 = False

say_r41('TEST851 RESEARCH HYPOTHESES',
    'H1: joint native C/E/Kprev computation changes control decisions under matched row-order ablations. '
    'H2: sufficient evidence permits preservation; insufficient evidence permits STOP; a verified wrong '
    'one-link candidate can be recomputed into a grounded final candidate. None is assumed true.')
say_r41('TEST851 ENGINE MODIFICATION',
    'Only the control junction changes. Physical CUT3/H3/KV, NF4 loading, cache construction, '
    'RoPE accounting, BF16 execution and generation stopping remain inherited. No hooks or training.')
say_r41('TEST851 NATIVE CANDIDATE-CONTROL COUPLING',
    'X=[P;slot_C;C;slot_E;E;(slot_K;Kprev);slot_action]. All state rows are BF16 layer-0 inputs, '
    '8192 wide, at consecutive post-memory RoPE positions. Revision uses [C;K;E].')
say_r41('TEST851 CAUSAL INTERVENTIONS',
    'COUPLED=(C,E); CANDIDATE=(reverse(C),E); EVIDENCE=(C,reverse(E)); '
    'MATCHED=(reverse(C),reverse(E)). Shapes, dtypes, norms, mounted cards and native probes match.')
say_r41('TEST851 EXPERIMENTAL PANEL',
    '20 jobs = 2 worlds x 2 evidence conditions x 5 arms; world 1 NATURAL, world 2 COUNTERFACTUAL; '
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
    cr = arm in ('CANDIDATE_ABLATION', 'MATCHED_CONTROL')
    er = arm in ('EVIDENCE_ABLATION', 'MATCHED_CONTROL')
    return (C.flip(0).contiguous() if cr else C,
        E.flip(0).contiguous() if er else E)


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
        gate829('TEST851_OBSERVATIONAL_GENERATOR_EQUALITY', equal, {})
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
        current851 = initial851
        tensors851['first_rows'] = first851['rows'].numpy().copy()
        tensors851['initial_candidate'] = initial851['rows'].numpy().copy()
        tensors851['evidence_rows'] = evidence851['rows'].numpy().copy()
        previous_control851 = None
        for cycle851 in range(MAX_REVIEWS851):
            candidate851 = current851
            C851, E851 = intervened851(arm851, candidate851['rows'], evidence851['rows'])
            if arm851 == 'BASELINE':
                pre851 = (list(prompt_ids(REVIEW851.format(q=QTEXT841[q851])))
                    + REVIEW_PRE_SLOT848)
                segments851 = [(None, C851)]
                review851 = invoke851(mx851, pre851, segments851, REVIEW_SUFFIX851,
                    'review_%d'%cycle851, tensors851, traces851, baseline=True)
            else:
                pre851 = list(prompt_ids(REVIEW851.format(q=QTEXT841[q851])))
                segments851 = [(C_SLOT851, C851), (E_SLOT851, E851)]
                if previous_control851 is not None:
                    segments851.append((K_SLOT851, previous_control851['rows']))
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
                'previous_control': None if previous_control851 is None else result849(previous_control851),
                'review': result849(review851), 'action': action851,
                'control_token_ids': review851['trace849']['all_token_ids'],
                'control_token_scores': review851['trace849']['token_top20'],
                'revision': None, 'python_action': 'APPLY_MODEL_'+action851,
                'model_native_action': action851,
                'loop_repetition': repetition851,
                'recurrent_previous_control': previous_control851 is not None
            }
            if previous_control851 is not None and arm851 != 'BASELINE':
                assert segments851[-1][1].shape == previous_control851['rows'].shape
                assert stats849(segments851[-1][1])['sha256'] == cycles851[-1]['review']['output']['sha256']
            if action851 == 'CONTINUE':
                accepted851, end851 = candidate851, 'MODEL_ACCEPT'
            elif action851 == 'STOP':
                end851 = 'MODEL_STOP'
            elif action851 == 'REVISE':
                transitions851 += 1
                recompute_pre851 = list(prompt_ids(RECOMPUTE851.format(q=QTEXT841[q851])))
                if arm851 == 'BASELINE':
                    state851 = torch.cat([C851, review851['rows']], dim=0).contiguous()
                    recompute_pre851 += REVISE_PRE_SLOT848
                    current851 = invoke851(mx851, recompute_pre851,
                        [(None, state851)], ANSWER_SUFFIX851,
                        'revision_%d'%cycle851, tensors851, traces851, baseline=True)
                else:
                    current851 = invoke851(mx851, recompute_pre851,
                        [(C_SLOT851, C851), (K_SLOT851, review851['rows']),
                         (E_SLOT851, E851)], ANSWER_SUFFIX851,
                        'revision_%d'%cycle851, tensors851, traces851)
                event851['revision'] = result849(current851)
            else:
                end851 = 'PROTOCOL_INVALID'
                event851['python_action'] = 'PROTOCOL_INVALID_NO_FOLLOWUP'
            cycles851.append(event851)
            say_r41('TEST851 CANDIDATE STATE', q851, condition851, mode851, arm851,
                'CYCLE='+str(cycle851), json.dumps(event851['candidate_intervened']))
            say_r41('TEST851 EVIDENCE STATE', q851, condition851, arm851,
                json.dumps(event851['evidence_intervened']))
            say_r41('TEST851 CONTROL STATE', q851, condition851, arm851,
                'CYCLE='+str(cycle851), json.dumps({'soft_rows':event851['review']['output'],
                    'final_hidden':event851['review'].get('control_hidden')}))
            say_r41('TEST851 MODEL DECISION', q851, condition851, mode851, arm851,
                'CYCLE='+str(cycle851), action851, 'TOKENS='+str(event851['control_token_ids']),
                'REVIEW='+repr(review851['text']))
            say_r41('TEST851 NUMERICAL FEEDBACK', q851, arm851, 'CYCLE='+str(cycle851),
                'REVISION='+repr(None if event851['revision'] is None else event851['revision']['text']))
            say_r41('TEST851 RECURRENT STATE TRANSFER', q851, arm851, 'CYCLE='+str(cycle851),
                'KPREV='+str(event851['recurrent_previous_control']),
                json.dumps(review851['trace849']['continuity']))
            say_r41('TEST851 LOOP COLLAPSE DIAGNOSTICS', q851, arm851,
                'CYCLE='+str(cycle851), 'REPETITION='+str(repetition851))
            say_r41('TEST851 MODEL SIGNAL VS PYTHON ACTION', q851, arm851,
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
    say_r41('TEST851 JOB-BY-JOB RESULTS', q851, condition851, mode851, arm851,
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
D829['test851_residual_hook_audit'] = residual_hooks851
log829('TEST851_RESIDUAL_HOOK_AUDIT', json.dumps(residual_hooks851))
gate829('TEST851_NO_RESIDUAL_HOOKS_BEFORE_FINAL', not residual_hooks851,
    residual_hooks851)
D829['run_seconds841'] = time.perf_counter()-t_run841
D829['memo851'] = dict(CNT_R41, states=len(SIG_R41), echo_states=len(ECHO_R41),
    hop=CNT845['hop'], hop_hit=CNT845['hop_hit'])
D829['panel851_sha256'] = PANEL_SHA851
'''

OFF851 = r'''
# Inherited TEST848 builder requires this exact offline marker.
log829('TEST846P_OFFLINE_START')
log829('TEST851_OFFLINE_START')

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
            'loop_repetition':e['loop_repetition']})
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
        if set(group) != set(ARMS851):
            continue
        coupled = group['COUPLED_NATIVE']
        candidate_ablated = group['CANDIDATE_ABLATION']
        evidence_ablated = group['EVIDENCE_ABLATION']
        matched = group['MATCHED_CONTROL']
        assert all(group[a]['cycles'] for a in ARMS851)
        c0 = coupled['cycles'][0]
        ca = candidate_ablated['cycles'][0]
        ea = evidence_ablated['cycles'][0]
        mc = matched['cycles'][0]
        def changed851(a, b):
            state_change = (a['review']['output']['sha256'] != b['review']['output']['sha256']
                or (a['review'].get('control_hidden') or {}).get('sha256') !=
                   (b['review'].get('control_hidden') or {}).get('sha256'))
            decision_change = (a['action'] != b['action'] or
                a['control_token_ids'] != b['control_token_ids'])
            score_change = abs(a['review']['p1'] - b['review']['p1']) > 1e-7
            return {'state_change':state_change, 'decision_change':decision_change,
                'score_change':score_change,
                'causal_observation':state_change and (decision_change or score_change)}
        y00, y10 = revise_indicator851(coupled), revise_indicator851(candidate_ablated)
        y01, y11 = revise_indicator851(evidence_ablated), revise_indicator851(matched)
        groups851.append({'qid':q, 'condition':condition,
            'mode':coupled['initial_mode'],
            'candidate_effect':changed851(c0,ca),
            'evidence_effect':changed851(c0,ea),
            'double_effect':changed851(c0,mc),
            'revise_interaction_y00_y10_y01_y11':y00-y10-y01+y11,
            'actions':{a:group[a]['cycles'][0]['action'] for a in ARMS851},
            'baseline_vs_coupled_action_changed':
                group['BASELINE']['cycles'][0]['action'] != c0['action']})

summary851 = {a:{k:sum(bool(c[k]) for c in cases851 if c['arm'] == a)
    for k in ('grounded','wrong_candidate_opportunity','error_signal','correction',
        'correct_preservation','unnecessary_revision','correct_stop','false_stop',
        'unsupported_completion','model_stop','mechanical_stop','loop_repetition')}
    for a in ARMS851}
complete851 = len(cases851) == 20 and len(groups851) == 4 and not BUDGET_STOP841
checks851 = D829.get('checks',[])
physical851 = bool(checks851) and all(c['pass'] for c in checks851)
transfers851 = [t['result']['trace849']['continuity']
    for r in records851 for t in r['traces']]
transfer_pass851 = bool(transfers851) and all(
    t.get('exact_after_bf16',False) for t in transfers851)
recurrent_edges851 = sum(e['recurrent_previous_control']
    for r in records851 if r['arm'] != 'BASELINE' for e in r['cycles'])
wrong_coupled851 = summary851['COUPLED_NATIVE']['wrong_candidate_opportunity']
candidate_causal851 = any(g['candidate_effect']['causal_observation'] for g in groups851)
evidence_causal851 = any(g['evidence_effect']['causal_observation'] for g in groups851)
interaction851 = any(g['revise_interaction_y00_y10_y01_y11'] != 0 for g in groups851)
action_variation851 = len({e['action'] for r in records851
    if r['arm'] == 'COUPLED_NATIVE' for e in r['cycles']}) > 1
# A small paired pilot can establish observed events, not population superiority.
task_benefit851 = (
    summary851['COUPLED_NATIVE']['correction'] > summary851['BASELINE']['correction']
    or summary851['COUPLED_NATIVE']['correct_preservation'] > summary851['BASELINE']['correct_preservation']
    or summary851['COUPLED_NATIVE']['correct_stop'] > summary851['BASELINE']['correct_stop'])
control_metrics851 = ('correction', 'correct_preservation', 'correct_stop')
control_specific851 = (
    all(summary851['COUPLED_NATIVE'][k] >= summary851['MATCHED_CONTROL'][k]
        for k in control_metrics851)
    and any(summary851['COUPLED_NATIVE'][k] > summary851['MATCHED_CONTROL'][k]
        for k in control_metrics851))
discrimination851 = action_variation851 and task_benefit851 and control_specific851
correction_pass851 = summary851['COUPLED_NATIVE']['correction'] > 0
preservation_pass851 = (summary851['COUPLED_NATIVE']['correct_preservation'] > 0
    and summary851['COUPLED_NATIVE']['unnecessary_revision'] == 0)
stop_pass851 = (summary851['COUPLED_NATIVE']['correct_stop'] > 0
    and summary851['COUPLED_NATIVE']['false_stop'] == 0)
verdicts851 = {
    'SOURCE_INTEGRITY':'PASS',
    'PHYSICAL_MEMORY_INTEGRITY':'PASS' if physical851 else 'FAIL',
    'NATIVE_BYPASS_INTEGRITY':'PASS' if physical851 and UPPER_CHECK841.get('upper_min',0) >= 1 else 'INCONCLUSIVE',
    'CANDIDATE_STATE_TRANSFER':'PASS' if transfer_pass851 else 'INCONCLUSIVE',
    'EVIDENCE_STATE_TRANSFER':'PASS' if transfer_pass851 else 'INCONCLUSIVE',
    'CONTROL_STATE_COUPLING':'PASS' if transfer_pass851 and any(
        r['arm'] == 'COUPLED_NATIVE' and len(r['traces']) for r in records851) else 'INCONCLUSIVE',
    'CANDIDATE_CAUSAL_EFFECT':'PRELIMINARY_OBSERVED' if candidate_causal851 else 'NOT_DEMONSTRATED',
    'EVIDENCE_CAUSAL_EFFECT':'PRELIMINARY_OBSERVED' if evidence_causal851 else 'NOT_DEMONSTRATED',
    'CANDIDATE_EVIDENCE_INTERACTION':'DESCRIPTIVE_NONZERO' if interaction851 else 'NOT_OBSERVED',
    'TASK_RELEVANT_CONTROL_DISCRIMINATION':'PRELIMINARY_PILOT_SIGNAL' if discrimination851 else 'NOT_DEMONSTRATED',
    'NATIVE_RECURRENT_FEEDBACK':'PASS' if recurrent_edges851 and transfer_pass851 else 'NOT_DEMONSTRATED',
    'MODEL_NATIVE_ERROR_SIGNAL':'PRELIMINARY_OBSERVED' if summary851['COUPLED_NATIVE']['error_signal'] else
        ('NOT_EVALUABLE_NO_WRONG_CANDIDATE' if not wrong_coupled851 else 'NOT_OBSERVED'),
    'MODEL_NATIVE_CORRECTION':'PRELIMINARY_OBSERVED' if correction_pass851 else
        ('NOT_EVALUABLE_NO_WRONG_CANDIDATE' if not wrong_coupled851 else 'NOT_OBSERVED'),
    'MODEL_NATIVE_PRESERVATION':'PRELIMINARY_OBSERVED' if preservation_pass851 else 'NOT_DEMONSTRATED',
    'MODEL_NATIVE_STOP':'PRELIMINARY_OBSERVED' if stop_pass851 else 'NOT_DEMONSTRATED',
    'AUTONOMOUS_RECURSIVE_REASONING':('PRELIMINARY_SINGLE_PANEL_SIGNAL'
        if all((discrimination851,recurrent_edges851,correction_pass851,preservation_pass851,stop_pass851))
        else 'NOT_DEMONSTRATED')
}
final_verdict851 = ('INCOMPLETE' if not complete851 else
    'PRELIMINARY_NATIVE_COUPLING_SIGNAL' if discrimination851 and candidate_causal851 and evidence_causal851
    else 'NO_CONFIRMED_TASK_RELEVANT_COUPLING_GAIN')

for c in cases851:
    if c['arm'] == 'COUPLED_NATIVE':
        say_r41('TEST851 WRONG INITIAL CANDIDATES', json.dumps({
            'world':c['world_id'], 'condition':c['condition'], 'mode':c['mode'],
            'initial_class':c['initial_class'], 'wrong':c['wrong_candidate_opportunity']}))
        say_r41('TEST851 CORRECTION RESULTS', json.dumps({
            'world':c['world_id'], 'condition':c['condition'],
            'error_signal':c['error_signal'], 'correction':c['correction'],
            'preservation':c['correct_preservation'], 'events':c['events']}))
        say_r41('TEST851 EVIDENCE SUFFICIENCY', json.dumps({
            'world':c['world_id'], 'condition':c['condition'], 'sufficient':c['sufficient'],
            'grounded':c['grounded'], 'correct_stop':c['correct_stop'],
            'false_stop':c['false_stop'], 'unsupported_completion':c['unsupported_completion']}))
for g in groups851:
    say_r41('TEST851 MATCHED CONTROL COMPARISON', json.dumps(g))
say_r41('TEST851 HARDWARE AND MODEL',
    'Inherited gates: one CUDA A100, Qwen2.5-72B NF4, 80 layers, H=8192, BF16, frozen weights.')
say_r41('TEST851 LOCKED ENGINE VERIFICATION',
    'Parent 850 and transitive 841–849 Git blob locks, AST patches, upper-layer execution and no-hook gates retained.')
say_r41('TEST851 PHYSICAL MEMORY INTEGRITY',
    'PASS' if physical851 else 'FAIL', 'Mounted cards were identical within every matched five-arm group.')
say_r41('TEST851 FAILURE ANALYSIS',
    'Tensor transfer is not decision control. Token change is not correction. Mechanical limits are not model STOP. '
    'Row-order ablations test dependence on the explicit C/E pathways; they do not remove physical KV evidence. '
    'One NATURAL and one COUNTERFACTUAL world cannot establish generalization or statistical superiority. '
    'Summary='+json.dumps(summary851))
next851 = ('Replicate the coupled junction on fresh worlds only if paired causal and task-relevant signals both occur. '
    'If only state/logit changes occur, keep the backbone and revise the native readout rather than increasing loops. '
    'If no C/E causal effect occurs, this junction is rejected. If wrong candidates do not materialize, correction remains unevaluable.')
say_r41('TEST851 NEXT ENGINEERING IMPLICATION', next851)
say_r41('TEST851 FINAL SCIENTIFIC VERDICT', final_verdict851, json.dumps(verdicts851))
report851 = ('TEST851 completed %d/20 jobs; %d matched groups; wrong initial opportunities in COUPLED=%d; '
    'recurrent Kprev edges=%d; candidate causal observations=%s; evidence causal observations=%s; '
    'verdict=%s. GPU results are established only by this executed run.') % (
        len(cases851),len(groups851),wrong_coupled851,recurrent_edges851,
        candidate_causal851,evidence_causal851,final_verdict851)
D829['test851'] = {'cases':cases851, 'matched_groups':groups851, 'summary':summary851,
    'panel_sha256':PANEL_SHA851, 'source_locks':dict(LOCKS849,
        **{'849.py':'01a6ac43cbc954cc2f6ceaf8cf0238333ec762b1',
           '850.py':'79cc5ab211c01b37324e2d6897a298e84db42101'}),
    'verdicts':verdicts851, 'final_verdict':final_verdict851, 'report':report851,
    'native_calls':CALLS849}
D829['verdict841R'] = {'decision':final_verdict851, 'verdicts':verdicts851,
    'budget_stop':BUDGET_STOP841, 'reason':'Pre-registered small paired TEST851 coupling panel.'}
D829['cost841R'] = {'counted':dict(COUNT834), 'native_calls':CALLS849,
    'run_seconds':D829['run_seconds841'],
    'peak_gpu_gib':max([r['peak_gpu_gib'] for r in records851] or [0.0])}
D829['status'] = 'COMPLETE_TEST851' if complete851 else 'PARTIAL_TEST851'
json.dumps(D829, ensure_ascii=False, default=str, allow_nan=False)
save829()
import os
artifact851 = str(OUT829)
artifact_sha851 = (hashlib.sha256(open(artifact851,'rb').read()).hexdigest()
    if os.path.isfile(artifact851) else None)
say_r41('TEST851 ARTIFACT PATHS AND SHA256', artifact851, artifact_sha851,
    'PANEL_SHA256='+PANEL_SHA851)
log829('TEST851_COMPLETED', str(OUT829), final_verdict851)
'''

# Replace only TEST850's experiment body and offline evaluator. The physical
# engine, model loader, cache builder and all transitive source gates are inherited.
source851 = replace_block851(source851, 'BODY_R2', BODY851)
source851 = replace_block851(source851, 'OFF_R2', OFF851)
source851 = once851(source851,
    "\\\"('LEGACY', 'PROTOCOL', 'FROZEN', 'FEEDBACK', 'NO_STATE')\\\"",
    "\\\"('BASELINE', 'COUPLED_NATIVE', 'MATCHED_CONTROL', 'CANDIDATE_ABLATION', 'EVIDENCE_ABLATION')\\\"")
source851 = once851(source851,
    "a.value='PANEL: TEST849-R2; 20 jobs | LEGACY / PROTOCOL / FROZEN / FEEDBACK / NO_STATE'",
    "a.value='PANEL: TEST849-R2; 20 jobs | BASELINE / COUPLED_NATIVE / MATCHED_CONTROL / CANDIDATE_ABLATION / EVIDENCE_ABLATION'")
source851 = source851.replace('TEST849-R2', 'TEST851')

# Static verification before any inherited model-loading code is executed.
for block851 in (BODY851, OFF851):
    ast.parse(block851)
    compile(block851, '<TEST851_EMBEDDED>', 'exec')
body_tree851 = ast.parse(BODY851)
function851 = {n.name:n for n in body_tree851.body if isinstance(n, ast.FunctionDef)}
assert set(('gen851','invoke851','shared851','intervened851')) <= set(function851)
assert [a.arg for a in function851['gen851'].args.args] == ['memx','pre','segments','post']
assert [a.arg for a in function851['intervened851'].args.args] == ['arm','C','E']
assert 'out.last_hidden_state' not in BODY851
assert 'output_hidden_states' not in BODY851
assert 'out.hidden_states' not in BODY851
assert "'control_hidden': None" in BODY851
assert 'TEST851_NO_RESIDUAL_HOOKS_BEFORE_FINAL' in BODY851
names851 = {n.id for n in ast.walk(body_tree851) if isinstance(n, ast.Name)}
assert not names851 & {'EVALKEY841','CONTENT841','worlds829','card_meta829'}
assert BODY851.count('for ji846, j846 in enumerate(JOBS841)') == 1
# Shared parent-panel jobs must remain read-only; the offline evaluator derives
# initial_mode from MODE851 as well, so no hidden JOBS841 schema is required.
assert "j['initial_mode']" not in BODY851 + OFF851
assert "j851['initial_mode']" not in BODY851 + OFF851
assert 'TEST846P_OFFLINE_START' in OFF851
assert 'for ji845, j845 in enumerate(JOBS841)' not in BODY851
assert 'register_forward_hook' not in BODY851
assert 'register_forward_pre_hook' not in BODY851
assert '.backward(' not in BODY851 and 'optimizer' not in BODY851.lower()
assert 'action_scores849(' not in BODY851
assert 'MAX_REVIEWS851 = 2' in BODY851
assert "MAX_REVIEWS_R2 = 3" not in BODY851
assert 'LEGACY / PROTOCOL / FROZEN / FEEDBACK / NO_STATE' not in source851
final_tree851 = ast.parse(source851)
compile(final_tree851, 'TEST851_LOCKED_BUILDER', 'exec')
print('TEST851 LOCKED ENGINE VERIFICATION')
print('WRAPPER AST: PASS | EMBEDDED COMPILE: PASS | PATCH UNIQUENESS: PASS')
print('FUNCTION SIGNATURES: PASS | RUNTIME ANSWER-KEY ISOLATION: PASS')
print('PANEL: 20 jobs; 2 cycles maximum; no extra teacher-forced probes')
print('BUILDER SHA256:', hashlib.sha256(source851.encode()).hexdigest())
print('GPU EXECUTION: NOT VERIFIED BY AUTHOR; only this Colab run can establish it', flush=True)
exec(compile(final_tree851, 'TEST851_LOCKED_BUILDER', 'exec'), globals())
