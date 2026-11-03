# TEST849-R2: locked TEST848 backbone, model-directed numerical feedback.
# One Colab cell. 20 jobs. No GPU execution is claimed by the author.
import ast, hashlib, json, urllib.request

URL_R2 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/849.py'
LOCK_R2 = '01a6ac43cbc954cc2f6ceaf8cf0238333ec762b1'
with urllib.request.urlopen(urllib.request.Request(URL_R2,
        headers={'User-Agent': 'AKBASCORE-TEST849-R2'}), timeout=180) as response:
    raw = response.read(1000001)
actual = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
assert actual == LOCK_R2, ('TEST849_PARENT_LOCK_FAILED', actual, LOCK_R2)
source = raw.decode('utf-8')
ast.parse(source)

def replace_block(source, name, value):
    nodes = [n for n in ast.parse(source).body if isinstance(n, ast.Assign)
        and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id == name and isinstance(n.value, ast.Constant)
        and isinstance(n.value.value, str)]
    assert len(nodes) == 1, ('LITERAL_NOT_UNIQUE', name, len(nodes))
    lines = source.splitlines(keepends=True)
    n = nodes[0]
    lines[n.lineno-1:n.end_lineno] = [name+' = '+repr(value)+'\n']
    result = ''.join(lines)
    ast.parse(result)
    return result

BODY_R2 = r'''
ARMS849 = ('LEGACY', 'PROTOCOL', 'FROZEN', 'FEEDBACK', 'NO_STATE')
MAX_REVIEWS_R2 = 3
assert len(JOBS841) == 20
assert set(j['arm'] for j in JOBS841) == set(ARMS849)
for q in dict.fromkeys(j['qid'] for j in JOBS841):
    for condition in ('INTACT', 'REMOVED'):
        group = [j for j in JOBS841 if j['qid'] == q and j['intervention'] == condition]
        assert len(group) == 5
        assert len({tuple(j['initial_cards']) for j in group}) == 1
        assert len({tuple(j['bank']) for j in group}) == 1
REVIEW_R2 = (
    'Question: {q}\n'
    'The numerical context is a candidate FINAL answer to this question. '
    'Evaluate that candidate using only mounted physical evidence. '
    'CONTINUE means the candidate completely answers the question and is supported. '
    'REVISE means recompute the final answer from the available evidence. '
    'STOP means the evidence is insufficient to answer the question. '
    'Reply with exactly one word: CONTINUE, REVISE, or STOP.'
)
RECOMPUTE_R2 = (
    'Question: {q}\n'
    'Use only mounted physical evidence. The numerical context contains the '
    'candidate answer and your review state. Recompute the FINAL answer to '
    'the complete question. If the evidence is insufficient, reply UNKNOWN. '
    'Reply with the final node name only.'
)
REVIEW_SUFFIX_R2 = list(tok('\nReview action:', add_special_tokens=False).input_ids)
ANSWER_SUFFIX_R2 = list(tok('\nFinal answer:', add_special_tokens=False).input_ids)
SHARED_R2 = {}
EQ_R2 = False
say_r41('TEST849 RESEARCH HYPOTHESES',
    'FEEDBACK vs FROZEN changes the source of candidate-state rows after REVISE: '
    'latest model output vs initial output. Prompts, evidence and safety limits match. '
    'NO_STATE removes context rows; PROTOCOL is one cycle. LEGACY reproduces TEST848. '
    'A token change alone is not correction. No wrong candidate means no correction opportunity.')
say_r41('TEST849 EXPERIMENTAL PANEL',
    'R2: 2 reused worlds x INTACT/REMOVED x 5 arms = 20 jobs; '
    'at most 3 reviews/job, no extra experimental probes.')

def fingerprint_r2(ids):
    return hashlib.sha256(json.dumps(list(ids)).encode()).hexdigest()

def invoke_r2(memx, pre, rows, post, stage, tensors, traces):
    h = gen849(memx, pre, rows, post)
    stats849(h['rows'])
    tensors[stage+'_input'] = (np.empty((0,H), dtype=np.float32)
        if rows is None else rows.detach().cpu().numpy().copy())
    tensors[stage+'_output'] = h['rows'].numpy().copy()
    traces.append({'stage': stage, 'prompt_sha256': fingerprint_r2(pre),
        'suffix_sha256': fingerprint_r2(post or []), 'result': result849(h)})
    return h

for ji846, j846 in enumerate(JOBS841):
    if j846['job'] in REC841:
        continue
    begun_r2 = time.perf_counter()
    tensors_r2, traces_r2, cycles_r2 = {}, [], []
    q_r2, arm_r2 = j846['qid'], j846['arm']
    condition_r2 = j846['intervention']
    mem_r2 = list(j846['initial_cards'])
    assert len(mem_r2) <= CAP845
    try:
        budget849()
        mx_r2 = memx_r41(mem_r2)
        key_r2 = (q_r2, condition_r2)
        if key_r2 not in SHARED_R2:
            pre_r2 = list(prompt_ids(FR845['hop0'].format(q=QTEXT841[q_r2]))) + SLOT845[3]
            if not EQ_R2:
                with CallCount841() as cc_r2:
                    first_r2 = gen849(mx_r2, pre_r2, None, None)
                UPPER_CHECK841 = cc_r2.summary()
                gate829('CUT3_UPPER_LAYER_EXECUTION',
                    UPPER_CHECK841['upper_min'] >= 1 and UPPER_CHECK841['lm_head'] >= 1,
                    UPPER_CHECK841)
                old_r2 = gen845(mx_r2, pre_r2, None, None)
                equal_r2 = (old_r2['text'] == first_r2['text']
                    and old_r2['toks'] == first_r2['toks']
                    and torch.equal(old_r2['rows'], first_r2['rows']))
                gate829('TEST849_R2_OBSERVATIONAL_GENERATOR_EQUALITY', equal_r2, {})
                assert equal_r2
                EQ_R2 = True
            else:
                first_r2 = gen849(mx_r2, pre_r2, None, None)
            SHARED_R2[key_r2] = {'first': first_r2}
        first_r2 = SHARED_R2[key_r2]['first']
        tensors_r2['first_rows'] = first_r2['rows'].numpy().copy()
        initial_r2 = None
        accepted_r2 = None
        end_r2 = None
        if arm_r2 == 'LEGACY':
            pre_r2 = list(prompt_ids(REVIEW_FRAME848.format(q=QTEXT841[q_r2]))) + REVIEW_PRE_SLOT848
            review_r2 = invoke_r2(mx_r2, pre_r2, first_r2['rows'], REVIEW_POST_SLOT848,
                'legacy_review', tensors_r2, traces_r2)
            scores_r2 = action_scores849(mx_r2, pre_r2, first_r2['rows'], REVIEW_POST_SLOT848)
            legacy_lines_r2 = (review_r2['text'] or '').strip().splitlines()
            legacy_match_r2 = re.match(r'^\s*(CONTINUE|REVISE|STOP)\b',
                legacy_lines_r2[0].strip().upper()) if legacy_lines_r2 else None
            action_r2 = legacy_match_r2.group(1) if legacy_match_r2 else 'INVALID'
            revision_r2 = None
            if action_r2 == 'REVISE':
                revision_r2 = invoke_r2(mx_r2,
                    list(prompt_ids(REVISE_FRAME848.format(q=QTEXT841[q_r2]))) + REVISE_PRE_SLOT848,
                    review_r2['rows'], None, 'legacy_revision', tensors_r2, traces_r2)
                accepted_r2 = invoke_r2(mx_r2,
                    list(prompt_ids(FR845['hop'].format(q=QTEXT841[q_r2]))) + SLOT845[1],
                    revision_r2['rows'], SLOT845[2], 'legacy_final', tensors_r2, traces_r2)
                end_r2 = 'LEGACY_FIXED_COMPLETION'
            elif action_r2 == 'CONTINUE':
                accepted_r2 = invoke_r2(mx_r2,
                    list(prompt_ids(FR845['hop'].format(q=QTEXT841[q_r2]))) + SLOT845[1],
                    first_r2['rows'], SLOT845[2], 'legacy_final', tensors_r2, traces_r2)
                end_r2 = 'LEGACY_FIXED_COMPLETION'
            else:
                end_r2 = 'MODEL_STOP' if action_r2 == 'STOP' else 'PROTOCOL_INVALID'
            cycles_r2.append({'cycle': 0, 'candidate': result849(first_r2),
                'review': result849(review_r2), 'action': action_r2, 'action_scores': scores_r2,
                'revision': None if revision_r2 is None else result849(revision_r2),
                'python_action': 'APPLY_LEGACY_'+action_r2})
        else:
            if 'candidate' not in SHARED_R2[key_r2]:
                SHARED_R2[key_r2]['candidate'] = gen849(mx_r2,
                    list(prompt_ids(FR845['hop'].format(q=QTEXT841[q_r2]))) + SLOT845[1],
                    first_r2['rows'], SLOT845[2])
            initial_r2 = SHARED_R2[key_r2]['candidate']
            current_r2 = initial_r2
            tensors_r2['initial_candidate'] = initial_r2['rows'].numpy().copy()
            limit_r2 = 1 if arm_r2 == 'PROTOCOL' else MAX_REVIEWS_R2
            for cycle_r2 in range(limit_r2):
                candidate_r2 = initial_r2 if arm_r2 == 'FROZEN' else current_r2
                input_r2 = None if arm_r2 == 'NO_STATE' else candidate_r2['rows']
                pre_r2 = list(prompt_ids(REVIEW_R2.format(q=QTEXT841[q_r2]))) + REVIEW_PRE_SLOT848
                review_r2 = invoke_r2(mx_r2, pre_r2, input_r2, REVIEW_SUFFIX_R2,
                    'review_%d'%cycle_r2, tensors_r2, traces_r2)
                scores_r2 = action_scores849(mx_r2, pre_r2, input_r2, REVIEW_SUFFIX_R2)
                action_r2 = parse849(review_r2['text'])
                event_r2 = {'cycle': cycle_r2, 'candidate': result849(candidate_r2),
                    'review': result849(review_r2), 'action': action_r2,
                    'action_scores': scores_r2, 'revision': None,
                    'python_action': 'APPLY_MODEL_'+action_r2,
                    'feedback_from_previous_revision': bool(cycle_r2 and arm_r2 == 'FEEDBACK')}
                if cycle_r2 and arm_r2 == 'FEEDBACK':
                    assert stats849(input_r2)['sha256'] == cycles_r2[-1]['revision']['output']['sha256']
                if action_r2 == 'CONTINUE':
                    accepted_r2, end_r2 = candidate_r2, 'MODEL_ACCEPT'
                elif action_r2 == 'STOP':
                    end_r2 = 'MODEL_STOP'
                elif action_r2 == 'REVISE':
                    state_r2 = (None if arm_r2 == 'NO_STATE' else
                        torch.cat([candidate_r2['rows'], review_r2['rows']], dim=0).contiguous())
                    current_r2 = invoke_r2(mx_r2,
                        list(prompt_ids(RECOMPUTE_R2.format(q=QTEXT841[q_r2]))) + REVISE_PRE_SLOT848,
                        state_r2, ANSWER_SUFFIX_R2, 'revision_%d'%cycle_r2, tensors_r2, traces_r2)
                    event_r2['revision'] = result849(current_r2)
                else:
                    end_r2 = 'PROTOCOL_INVALID'
                    event_r2['python_action'] = 'PROTOCOL_INVALID_NO_FOLLOWUP'
                cycles_r2.append(event_r2)
                say_r41('TEST849 MODEL SIGNAL VS PYTHON ACTION', arm_r2, q_r2, condition_r2,
                    'CYCLE=%d'%cycle_r2, action_r2, 'REVIEW='+repr(review_r2['text']),
                    'REVISION='+repr(None if event_r2['revision'] is None else event_r2['revision']['text']))
                if end_r2 is not None:
                    break
            if end_r2 is None:
                end_r2 = 'MECHANICAL_REVIEW_LIMIT'
        rec_r2 = {'job': j846['job'], 'qid': q_r2, 'arm': arm_r2, 'condition': condition_r2,
            'mounted_cards': mem_r2, 'mounted_count': len(mem_r2), 'first': result849(first_r2),
            'initial': None if initial_r2 is None else result849(initial_r2),
            'cycles': cycles_r2, 'traces': traces_r2, 'end': end_r2,
            'answer': None if accepted_r2 is None else result849(accepted_r2),
            'mechanical_stop_reason': end_r2 if end_r2 in ('MECHANICAL_REVIEW_LIMIT','PROTOCOL_INVALID') else None,
            'seconds': time.perf_counter()-begun_r2,
            'peak_gpu_gib': torch.cuda.max_memory_allocated()/1024**3}
    except BudgetR41 as error_r2:
        BUDGET_STOP841 = True
        rec_r2 = {'job':j846['job'], 'qid':q_r2, 'arm':arm_r2, 'condition':condition_r2,
            'mounted_cards':mem_r2, 'cycles':cycles_r2, 'traces':traces_r2,
            'end':'MECHANICAL_RESOURCE_LIMIT', 'answer':None,
            'mechanical_stop_reason':str(error_r2), 'seconds':time.perf_counter()-begun_r2,
            'peak_gpu_gib':torch.cuda.max_memory_allocated()/1024**3}
    REC841[j846['job']], ROWS841[j846['job']] = rec_r2, tensors_r2
    save_job841(j846['job'], rec_r2, tensors_r2)
    say_r41('TEST849 JOB-BY-JOB RESULTS', q_r2, condition_r2, arm_r2,
        'END='+rec_r2['end'], 'ANSWER='+repr(None if rec_r2['answer'] is None else rec_r2['answer']['text']),
        'SECONDS=%.2f'%rec_r2['seconds'])
    if BUDGET_STOP841:
        break
while LRU_R41:
    evict_r41()
D829['run_seconds841'] = time.perf_counter()-t_run841
D829['memo841R'] = dict(CNT_R41, states=len(SIG_R41), echo_states=len(ECHO_R41),
    hop=CNT845['hop'], hop_hit=CNT845['hop_hit'])
'''

OFF_R2 = r'''
log829('TEST846P_OFFLINE_START')
log829('TEST849_R2_OFFLINE_START')
def node_r2(value, world):
    text = str(value or '').strip().upper().rstrip('.')
    keys = ('middle','end','changed_end','fork_end','decoy_end')
    hits = [k for k in keys if world.get(k) and text == str(world[k]).strip().upper()]
    return hits[0] if len(hits)==1 else 'UNKNOWN' if text=='UNKNOWN' else 'OTHER'

def supported_r2(value, world, mounted):
    c = node_r2(value, world)
    ids = world['ids']
    return bool(ids['first'] in mounted and
        ((c=='end' and ids['second'] in mounted) or
         (c=='changed_end' and ids['changed'] in mounted)))

cases_r2, pairs_r2 = [], []
for j in JOBS841:
    if j['job'] not in REC841:
        continue
    r = REC841[j['job']]
    # TEST846 deliberately removes EVALKEY writes from job41r.
    # Resolve the question/world ONLY in this offline block, as TEST847 does.
    assert QID841.count(j['qid']) == 1, ('OFFLINE_QID_NOT_UNIQUE', j['qid'])
    wi = QID841.index(j['qid'])
    assert wi in PILOT_WORLDS846, ('OFFLINE_WORLD_OUTSIDE_PANEL', wi)
    assert r['job'] == j['job'] and r['qid'] == j['qid'], ('OFFLINE_RECORD_ID_MISMATCH', j['job'])
    assert r['arm'] == j['arm'] and r['condition'] == j['intervention'], ('OFFLINE_RECORD_PANEL_MISMATCH', j['job'])
    assert list(r['mounted_cards']) == list(j['initial_cards']), ('OFFLINE_MOUNT_MISMATCH', j['job'])
    w = worlds829[wi]
    mounted = set(r['mounted_cards'])
    sufficient = w['ids']['first'] in mounted and bool({w['ids']['second'],w['ids']['changed']} & mounted)
    answer = None if r['answer'] is None else r['answer']['text']
    grounded = supported_r2(answer, w, mounted)
    events = []
    for event in r['cycles']:
        candidate = event['candidate']['text']
        cls = node_r2(candidate, w)
        wrong = cls in ('middle','fork_end','decoy_end')
        if r['arm']=='LEGACY':
            wrong = cls in ('end','changed_end','fork_end','decoy_end')
        revision = event['revision']
        events.append({'cycle':event['cycle'], 'candidate_class':cls,
            'candidate_grounded':supported_r2(candidate,w,mounted),
            'confirmed_wrong':wrong, 'action':event['action'],
            'recognized_wrong':wrong and event['action']=='REVISE',
            'revision_grounded':revision is not None and supported_r2(revision['text'],w,mounted),
            'revision_empty':revision is not None and not revision['text'].strip()})
    correction = bool(r['arm']!='LEGACY' and grounded and r['end']=='MODEL_ACCEPT' and
        any(e['confirmed_wrong'] and e['action']=='REVISE' and e['revision_grounded'] for e in events))
    case = {'world':wi,'condition':r['condition'],'arm':r['arm'],'end':r['end'],
        'answer':answer, 'grounded':grounded,'sufficient':sufficient,'correction':correction,
        'correct_stop':r['end']=='MODEL_STOP' and not sufficient,
        'false_stop':r['end']=='MODEL_STOP' and sufficient,
        'unsupported_completion':answer is not None and bool(answer.strip())
            and node_r2(answer,w)!='UNKNOWN' and not grounded,
        'events':events}
    cases_r2.append(case)
summary_r2 = {a:{k:sum(bool(c[k]) for c in cases_r2 if c['arm']==a)
    for k in ('grounded','correction','correct_stop','false_stop','unsupported_completion')} for a in ARMS849}
for wi in PILOT_WORLDS846:
    for cond in PILOT_STARTS846:
        group = {c['arm']:c for c in cases_r2 if c['world']==wi and c['condition']==cond}
        if set(group)==set(ARMS849):
            pairs_r2.append({'world':wi,'condition':cond,
                'feedback_vs_frozen_grounded':int(group['FEEDBACK']['grounded'])-int(group['FROZEN']['grounded']),
                'feedback_vs_frozen_correction':int(group['FEEDBACK']['correction'])-int(group['FROZEN']['correction']),
                'feedback_vs_no_state_grounded':int(group['FEEDBACK']['grounded'])-int(group['NO_STATE']['grounded']),
                'feedback_vs_frozen_stop':int(group['FEEDBACK']['correct_stop'])-int(group['FROZEN']['correct_stop']),
                'feedback_vs_no_state_stop':int(group['FEEDBACK']['correct_stop'])-int(group['NO_STATE']['correct_stop'])})
records_r2 = [REC841[j['job']] for j in JOBS841 if j['job'] in REC841]
checks_r2 = D829.get('checks',[])
physical_r2 = bool(checks_r2) and all(c['pass'] for c in checks_r2)
complete_r2 = len(cases_r2)==20 and len(pairs_r2)==4 and not BUDGET_STOP841
transfers_r2 = [t['result']['trace849']['continuity'] for r in records_r2 for t in r['traces']]
feedback_edges_r2 = sum(e.get('feedback_from_previous_revision',False)
    for r in records_r2 for e in r['cycles'])
wrong_r2 = sum(e['confirmed_wrong'] for c in cases_r2 if c['arm']=='FEEDBACK' for e in c['events'])
precontrast_r2 = []
for q in dict.fromkeys(r['qid'] for r in records_r2):
    for cond in ('INTACT','REMOVED'):
        group = [r for r in records_r2 if r['qid']==q and r['condition']==cond
            and r['arm'] in ('PROTOCOL','FROZEN','FEEDBACK') and r['cycles']]
        if len(group)==3:
            precontrast_r2.append(len({(r['cycles'][0]['review']['text'],
                r['cycles'][0]['review']['output']['sha256']) for r in group})==1)
matched_r2 = len(precontrast_r2)==4 and all(precontrast_r2)
gain_r2 = (matched_r2 and sum(p['feedback_vs_frozen_grounded']+p['feedback_vs_frozen_stop'] for p in pairs_r2)>0
    and sum(p['feedback_vs_no_state_grounded']+p['feedback_vs_no_state_stop'] for p in pairs_r2)>0
    and all(summary_r2['FEEDBACK'][k]<=summary_r2[a][k]
        for a in ('FROZEN','NO_STATE') for k in ('false_stop','unsupported_completion')))
verdict_r2 = ('INCOMPLETE' if not complete_r2 else
    'PRELIMINARY_TASK_RELEVANT_FEEDBACK_SIGNAL' if gain_r2 and physical_r2 and feedback_edges_r2
    else 'NO_CONFIRMED_FEEDBACK_TASK_GAIN')
verdicts_r2 = {
    'SOURCE_INTEGRITY':'PASS', 'PHYSICAL_MEMORY_INTEGRITY':'PASS' if physical_r2 else 'FAIL',
    'NATIVE_BYPASS_INTEGRITY':'PASS' if physical_r2 and UPPER_CHECK841.get('upper_min',0)>=1 else 'INCONCLUSIVE',
    'NUMERICAL_STATE_CONTINUITY':'PASS' if transfers_r2 and all(t['exact_after_bf16'] for t in transfers_r2) else 'INCONCLUSIVE',
    'MATCHED_PREINTERVENTION_REVIEW':'PASS' if matched_r2 else 'INCONCLUSIVE',
    'REVISION_STATE_TRANSFER':'OBSERVED' if feedback_edges_r2 else 'NOT_OBSERVED',
    'STATE_INTERVENTION_EFFECT':verdict_r2,
    'REVIEW_PROTOCOL_DISCRIMINATION':('ACTION_VARIATION_OBSERVED' if len({e['action']
        for r in records_r2 if r['arm']=='FEEDBACK' for e in r['cycles']})>1
        else 'NO_ACTION_VARIATION_OBSERVED'),
    'EVIDENCE_SENSITIVITY':('PRELIMINARY_PAIRED_SIGNAL' if any(
        c['arm']=='FEEDBACK' and c['condition']=='INTACT' and c['grounded']
        and any(d['world']==c['world'] and d['arm']=='FEEDBACK' and d['condition']=='REMOVED'
            and d['correct_stop'] for d in cases_r2) for c in cases_r2) else 'NOT_DEMONSTRATED'),
    'MODEL_NATIVE_ERROR_SIGNAL':'NOT_DEMONSTRATED',
    'MODEL_NATIVE_CORRECTION':('PRELIMINARY_SIGNAL' if summary_r2['FEEDBACK']['correction']
        else 'NOT_EVALUABLE_NO_WRONG_CANDIDATE' if not wrong_r2 else 'NOT_OBSERVED'),
    'MODEL_NATIVE_STOP':('PRELIMINARY_SIGNAL' if summary_r2['FEEDBACK']['correct_stop']
        and not summary_r2['FEEDBACK']['false_stop'] and summary_r2['FEEDBACK']['grounded'] else 'NOT_DEMONSTRATED'),
    'AUTONOMOUS_RECURSIVE_REASONING':'NOT_DEMONSTRATED'}
for title in ('SOURCE VERIFICATION','HARDWARE AND MODEL','PHYSICAL MEMORY INTEGRITY',
    'LOCKED ENGINE VERIFICATION','NUMERICAL STATE CONTINUITY'):
    say_r41('TEST849 '+title, json.dumps(verdicts_r2) if title=='NUMERICAL STATE CONTINUITY'
        else 'See verified inherited preflight; R2 retains physical engine and gates.')
for r in records_r2:
    for e in r['cycles']:
        say_r41('TEST849 REVIEW ACTION DIAGNOSTICS',r['qid'],r['condition'],r['arm'],
            'CYCLE='+str(e['cycle']),e['action'],repr(e['review']['text']))
        say_r41('TEST849 TOKEN AND LOGIT DIAGNOSTICS',
            json.dumps({'tokens':e['review']['trace849']['all_token_ids'],
                'raw':e['review']['trace849']['raw_decode'],
                'action_scores':[[v['spelling'],v['ids'],round(v['sequence_logp'],4)]
                    for v in e['action_scores']]}))
        if e['revision'] is not None:
            t=e['revision']['trace849']
            say_r41('TEST849 REVISION TRANSFER DIAGNOSTICS',
                json.dumps({'input':t['input'],'output':e['revision']['output'],
                    'continuity':t['continuity'],'tokens':t['all_token_ids'],
                    'raw':t['raw_decode'],'empty_reason':t['empty_reason']}))
for c in cases_r2:
    say_r41('TEST849 JOB-BY-JOB RESULTS',json.dumps(c))
say_r41('TEST849 CAUSAL COMPARISON',json.dumps({'summary':summary_r2,'pairs':pairs_r2}))
say_r41('TEST849 MODEL SIGNAL VS PYTHON ACTION',
    'Model emits actions. Python applies them; review/resource caps are mechanical. '
    'FROZEN deliberately reuses initial candidate; NO_STATE removes rows. '
    'LEGACY fixed completion is not model acceptance. No evidence selection or answer override.')
report_r2 = ('TEST849-R2 completed %d/20 jobs. Verified feedback edges: %d. '
    'Verdict: %s. FEEDBACK/FROZEN holds prompts, mounted evidence and maximum reviews fixed; '
    'only the numerical candidate source changes after revision. Actual calls may differ due to model actions. '
    'NO_STATE also changes context length. PROTOCOL uses one cycle. LEGACY comparisons change both protocol '
    'and state handling and cannot isolate one factor. Wrong-candidate opportunities in FEEDBACK: %d. '
    'A universal REVISE action is not error recognition. A mechanical limit is not model STOP. '
    'Fixed evidence cannot demonstrate model-selected evidence retention. Two reused worlds do not establish '
    'generalization or autonomous reasoning. Summary: %s') % (
        len(cases_r2),feedback_edges_r2,verdict_r2,wrong_r2,json.dumps(summary_r2))
say_r41('TEST849 FAILURE ANALYSIS',report_r2)
say_r41('TEST849 NEXT MECHANISM',
    'If no task gain is observed, inspect per-cycle state hashes and action sequence scores; '
    'do not increase loops or force REVISE/STOP to manufacture success.')
say_r41('TEST849 FINAL SCIENTIFIC VERDICT',json.dumps(verdicts_r2))
say_r41('TEST849 SCIENTIFIC REPORT',report_r2)
D829['test849_r2'] = {'cases':cases_r2,'paired':pairs_r2,'summary':summary_r2,
    'feedback_edges':feedback_edges_r2,'matched_first_review':matched_r2,'source_locks':dict(LOCKS849, **{'849.py':'01a6ac43cbc954cc2f6ceaf8cf0238333ec762b1'}),'verdicts':verdicts_r2,'report':report_r2}
D829['verdict841R'] = {'decision':verdict_r2,'verdicts':verdicts_r2,
    'budget_stop':BUDGET_STOP841,'reason':'Pre-registered FEEDBACK/FROZEN and NO_STATE contrasts.'}
D829['cost841R'] = {'counted':dict(COUNT834),'run_seconds':D829['run_seconds841'],
    'peak_gpu_gib':max([r['peak_gpu_gib'] for r in records_r2] or [0.0])}
D829['status'] = 'COMPLETE_TEST849_R2' if complete_r2 else 'PARTIAL_TEST849_R2'
json.dumps(D829,ensure_ascii=False,default=str,allow_nan=False)
save829()
log829('TEST849_R2_COMPLETED',str(OUT829))
'''

source = replace_block(source, 'BODY849', BODY_R2)
source = replace_block(source, 'OFF849', OFF_R2)
# Change only the panel's final literal assignment, by its AST target.
tree = ast.parse(source)
panel_nodes = [n for n in tree.body if isinstance(n,ast.Assign)
    and any(isinstance(t,ast.Name) and t.id=='PANEL849' for t in n.targets)]
assert panel_nodes
last_panel = panel_nodes[-1]
lines = source.splitlines(keepends=True)
lines[last_panel.end_lineno:last_panel.end_lineno] = [
    "PANEL849 = once849(PANEL849, \"('LEGACY', 'BOUNDARY', 'CONTINUITY', 'ORDER_CONTROL', 'NO_STATE')\", "
    "\"('LEGACY', 'PROTOCOL', 'FROZEN', 'FEEDBACK', 'NO_STATE')\")\n"]
source = ''.join(lines)
# Replace stale direct display text only; computational literals are untouched.
tree = ast.parse(source)
for n in tree.body:
    if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call):
        c=n.value
        if isinstance(c.func,ast.Name) and c.func.id=='print':
            for a in c.args:
                if isinstance(a,ast.Constant) and isinstance(a.value,str) and a.value.startswith('PANEL:'):
                    a.value='PANEL: TEST849-R2; 20 jobs | LEGACY / PROTOCOL / FROZEN / FEEDBACK / NO_STATE'
ast.fix_missing_locations(tree)
for block in (BODY_R2,OFF_R2):
    ast.parse(block)
names = {n.id for n in ast.walk(ast.parse(BODY_R2)) if isinstance(n,ast.Name)}
assert not names & {'EVALKEY841','CONTENT841','worlds829','card_meta829'}
assert BODY_R2.count('for ji846, j846 in enumerate(JOBS841)')==1
print('TEST849-R2 PARENT SOURCE SHA1:',actual)
print('TEST849-R2 WRAPPER AST: PASS; full inherited engine checks follow.')
print('GPU EXECUTION: NOT VERIFIED BY AUTHOR',flush=True)
exec(compile(tree,'TEST849_R2_LOCKED_BUILDER','exec'),globals())
