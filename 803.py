# AKBASCORE SILICON HIPPOCAMPUS — TEST803
# BOUNDED EVIDENCE-DIRECTED CLOSED LOOP / PHYSICAL CUT3 CARTRIDGES
# ONE COLAB CELL | FROZEN Qwen2.5-72B NF4 | ONE A100 80GB
# Proven TEST790 definitions and TEST779 native engine imported VERBATIM by Git blob.
# NO TRAINING, NO GOLD IN INTERVENTION, NO PERSISTENT HOOKS, NO GRADIO.
# First bounded adaptive controller; general autonomous reasoning remains unproven.
import urllib.request,hashlib,ast,json,traceback,gc,math,time
from pathlib import Path

# Fail fast BEFORE downloading locked source trees or 72B model weights.
# Do not weaken the TEST779 hardware contract.
def preflight_gpu803():
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError('TEST803_REQUIRES_TORCH_AND_A100_80GB_RUNTIME') from exc
    if not torch.cuda.is_available():
        raise RuntimeError('TEST803_NO_CUDA_GPU: Select a Colab A100 80GB runtime.')
    count=torch.cuda.device_count()
    if count!=1:
        raise RuntimeError(f'TEST803_EXPECTS_ONE_GPU: detected={count}')
    info=torch.cuda.get_device_properties(0)
    name=info.name; gib=info.total_memory/(1024**3)
    print('TEST803_GPU_PREFLIGHT',{'name':name,'vram_gib':round(gib,2),'gpu_count':count},flush=True)
    if 'A100' not in name or info.total_memory < 70*2**30:
        raise RuntimeError(
            f'TEST803_A100_80GB_REQUIRED: detected {name}, {gib:.2f} GiB. '
            'In Colab choose Runtime > Change runtime type > A100 GPU; '
            'restart the runtime and execute this cell again. '
            'The locked TEST779 safety gate is intentionally unchanged.')
    free,total=torch.cuda.mem_get_info(0)
    print('TEST803_GPU_FREE_GIB',round(free/2**30,2),flush=True)
    if free < 40*2**30:
        raise RuntimeError(
            f'TEST803_INSUFFICIENT_FREE_VRAM: {free/2**30:.2f} GiB free; '
            'restart the runtime to clear old models.')
preflight_gpu803()

SOURCE803='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/790.py'
BLOB803='d7e4c4b21e9c3c46276845940a9621751b23897f'
def gitblob803(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with urllib.request.urlopen(urllib.request.Request(SOURCE803,headers={'User-Agent':'AKBASCORE-TEST803'}),timeout=180) as response:
    raw803=response.read()
assert gitblob803(raw803)==BLOB803,('FAIL_CLOSED_TEST790_SOURCE_CHANGED',gitblob803(raw803))
tree803=ast.parse(raw803.decode('utf-8'),filename='790.py')
cut803=next((i for i,n in enumerate(tree803.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:4])),None)
assert cut803 is not None and cut803==len(tree803.body)-1,'FAIL_CLOSED_TEST790_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree803.body[:cut803],type_ignores=[])),
             'TEST790_GPU_PROVEN_LOCKED_PRELUDE','exec'),globals())
# The TEST790 prelude runs only imports and definitions, not its GPU experiment.
assert blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')]
assert gitblob785(raw785)==BLOB
assert torch.cuda.is_available() and torch.cuda.device_count()==1
assert 'A100' in torch.cuda.get_device_properties(0).name
TEST='803';OUT=ROOT/'TEST803_results.json';LOG=ROOT/'TEST803.log';MANIFEST=ROOT/'TEST803_manifest.json'
LOG.write_text('',encoding='utf-8')
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'panel_sha256':PANEL_SHA,
   'locks':LOCKS,'source790_git_blob':BLOB803,'checks':[],'rows':[],
   'objective':'First evidence-directed bounded closed-loop controller on physical native CUT3 cartridges',
   'limits':['The view and source-role policy are supplied by experiment metadata; autonomous source discovery is NOT tested.',
             'No oracle answer enters the controller; all truth labels are scored after decisions.',
             'Source singleton changes prefix length and RoPE context; it is not isolated source deletion.',
             'Concordance is not correctness; output consensus is not proof of general reasoning.',
             'Bounded retry is a first closed-loop prototype, not a demonstrated general autonomous reasoning engine.']}

def save803():
    tmp=Path(str(OUT)+'.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT)
def gate803(name,ok,detail=None):
    R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});save803()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST803_GATE_'+name)
def emit803(row):
    R['rows'].append(row);save803();log('TEST803_ROW',json.dumps(row,ensure_ascii=False,default=str))

# Sealed experimental truth panel is created before loading the model; the controller
# never reads this object. It is used only in offline grading after all actions.
def expected803(fam, candidate, view, decoy_map):
    if view=='HISTORICAL':return fam['old_team']
    if candidate.endswith('_X1'):return decoy_map[fam['id']]
    return fam['new_team']

def readout803(mem, question, spans=None):
    out=free_generate(mem,question,seed=None,gain=0.0,max_new=MAX_TOKENS,spans=spans)
    pred=parse789(out['raw'])
    return {'prediction':pred,'raw':out['raw'][:250],
            'generated_tokens':out['generated_tokens'],'sdpa_calls':out['sdpa_calls']}

def decide803(question, order, source_mem, ledger):
    # Four possible native physical reads. The next read depends on previous results.
    # Metadata routing is visible and fixed; answer values are NEVER used as targets.
    view=ledger['view']
    assert len(order)==2 and len(set(order))==2, 'INVALID_SOURCE_PAIR'
    relevant_candidates=[cid for cid in order if cid.endswith(('_B1','_X1'))]
    anchor_candidates=[cid for cid in order if cid.endswith('_B0')]
    assert len(relevant_candidates)==1 and len(anchor_candidates)==1, 'SOURCE_ROLE_AMBIGUITY'
    assert view in ('CURRENT','HISTORICAL'), 'INVALID_VIEW'
    relevant=(relevant_candidates[0] if view=='CURRENT' else anchor_candidates[0])
    irrelevant=next(x for x in order if x!=relevant)
    steps=[];cache={}
    def read(key,ids):
        if key not in cache:
            mem,active,_,_=build_fusion(ids,'TEST803_'+ledger['case_id']+'_'+key,True)
            try:
                gate803('NATIVE80_'+ledger['case_id']+'_'+key,len(mem)==80 and list(active)==ids)
                if len(ids)==2:
                    spans=spans790(ids,mem)
                else:
                    single_n=int(entries[ids[0]]['body_tokens'])
                    total_n=int(mem[0][0].shape[-2])
                    gate803('SINGLETON_SPAN_'+ledger['case_id']+'_'+key,
                            total_n==P+single_n,{'actual':total_n,'expected':P+single_n})
                    # AttentionIntervention requires two named slots; an empty
                    # unused slot does not introduce any synthetic memory tokens.
                    spans={'B0':(P,total_n),'B1':(total_n,total_n)}
                seal=memory_seals(mem)
                result=readout803(mem,question,spans)
                gate803('KV_SEAL_'+ledger['case_id']+'_'+key,compare_seals(seal,memory_seals(mem)))
                cache[key]=result
            finally:
                del mem;gc.collect();release()
        steps.append({'step':len(steps)+1,'operation':key,'cartridges':ids,
                      'prediction':cache[key]['prediction']})
        return cache[key]['prediction']
    # First thought: native fused memory.
    first=read('PAIR',order)
    # Reflect: inspect relevant evidence alone. If it disagrees, test competing
    # evidence BEFORE making any decision.
    relevant_pred=read('RELEVANT_SINGLE',[relevant])
    conflicting=(first!=relevant_pred or first=='UNKNOWN')
    if conflicting:
        alternative=read('OTHER_SINGLE',[irrelevant])
    else:
        alternative=None
    # Retry using physically reversed native fusion, not a fabricated KV permutation.
    reverse=read('REVERSE_PAIR',list(reversed(order)))
    if first!='UNKNOWN' and first==relevant_pred==reverse:
        action='ANSWER';final=first;reason='PAIR_RELEVANT_SINGLE_REVERSE_CONSENSUS'
    else:
        action='ABSTAIN';final='UNKNOWN'
        reason='SOURCE_DISAGREEMENT_OR_ORDER_INSTABILITY'
    return {'action':action,'answer':final,'reason':reason,'steps':steps,
            'conflict_detected':conflicting,'retries':int(conflicting),
            'initial_prediction':first,'relevant_prediction':relevant_pred,
            'alternative_prediction':alternative,'reverse_prediction':reverse,
            'relevant_source':relevant,'irrelevant_source':irrelevant}

try:
    log('='*112);log('TEST803 — EVIDENCE-DIRECTED BOUNDED RECURSIVE CONTROL / NATIVE CUT3')
    gate803('TEST790_EXACT_BLOB',gitblob803(raw803)==BLOB803)
    gate803('TEST789_EXACT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate803('TEST779_EXACT_BLOB',gitblob785(raw785)==BLOB)
    gate803('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    persist_manifest()
    gate803('MANIFEST_PREFLIGHT',json.loads(MANIFEST.read_text())['panel_sha256']==PANEL_SHA)
    gate803('PROVEN_NATIVE_SYMBOLS',all(callable(globals().get(k)) for k in
        ('build_fusion','free_generate','memory_seals','compare_seals','physical_commit','parse789')))
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    gate803('GPU_VRAM',free>=40*2**30)
    # Build the fixed, independent truth ledger BEFORE loading the model.
    families=list(FAMILIES)
    decoy_map={fam['id']:families[(ix+1)%len(families)]['new_team'] for ix,fam in enumerate(families)}
    truth803={}
    for fam in families:
        for candidate in (fam['id']+'_B1',fam['id']+'_X1'):
            for view in VIEWS:
                key=fam['id']+'|'+candidate+'|'+view
                truth803[key]=expected803(fam,candidate,view,decoy_map)
    truth_digest=hashlib.sha256(json.dumps(truth803,sort_keys=True).encode()).hexdigest()
    R['sealed_truth_sha256']=truth_digest
    gate803('SEALED_TRUTH_PANEL',len(truth803)==16,truth_digest)
    model_setup();before803=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate803('PHYSICAL_20_CARTRIDGES',len(entries)==20,len(entries))
    extras={}
    for fam in families:
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        extras[fid+'_X1']=(f'Authoritative CURRENT record REVISION 1: {work} '
                            f'collaborates_with {decoy_map[fid]}. Supersedes revision 0.')
        extras[fid+'_X0']=(f'Historical record REVISION 0 (superseded): {work} '
                            f'collaborates_with {decoy_map[fid]}. Valid at revision 0 only.')
    for cid,body in sorted(extras.items()):physical_commit(cid,body)
    gate803('PHYSICAL_28_CARTRIDGES',len(entries)==28,len(entries))
    for fam in families:
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        anchor=fid+'_B0'
        for candidate in (fid+'_B1',fid+'_X1'):
            # Different orders deliberately vary by candidate; reverse is audited in-loop.
            order=[candidate,anchor] if candidate.endswith('_B1') else [anchor,candidate]
            for view in VIEWS:
                case_id=fid+'_'+candidate+'_'+view
                q=CUE[view].format(work=work)
                decision=decide803(q,order,entries,{'view':view,'case_id':case_id})
                # Gold appears ONLY after the controller has finished and committed.
                expected=truth803[fid+'|'+candidate+'|'+view]
                row={'case_id':case_id,'family':fid,'candidate':candidate,'view':view,
                     'expected_OFFLINE':expected,'controller':decision,
                     'correct_OFFLINE':decision['action']=='ANSWER' and decision['answer']==expected,
                     'initial_correct_OFFLINE':decision['initial_prediction']==expected}
                R['rows'].append(row);save803()
                log('TEST803_ROW',json.dumps(row,ensure_ascii=False))
    gate803('TOTAL_CASES',len(R['rows'])==16,len(R['rows']))
    gate803('CLOSED_LOOP_STEPS',all(3<=len(r['controller']['steps'])<=4 for r in R['rows']))
    gate803('NATIVE_READS_UNIQUE_PER_CASE',all(
        len({tuple(x['cartridges']) for x in r['controller']['steps']})==len(r['controller']['steps'])
        for r in R['rows']))
    gate803('CONTROLLER_ACTION_VALID',all(
        r['controller']['action'] in ('ANSWER','ABSTAIN') and
        (r['controller']['answer']=='UNKNOWN' if r['controller']['action']=='ABSTAIN'
         else r['controller']['answer']!='UNKNOWN') for r in R['rows']))
    gate803('RETRY_CONDITIONAL',all((len(r['controller']['steps'])==4)==r['controller']['conflict_detected'] for r in R['rows']))
    gate803('NO_GOLD_IN_CONTROLLER',all('expected' not in str(r['controller']) for r in R['rows']))
    gate803('SEALED_TRUTH_UNCHANGED',hashlib.sha256(json.dumps(truth803,sort_keys=True).encode()).hexdigest()==truth_digest)
    gate803('FROZEN_WEIGHTS',sentinel()==before803)
    gate803('FINAL_MANIFEST',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    gate803('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    answers=[r for r in R['rows'] if r['controller']['action']=='ANSWER']
    R['summary']={'cases':len(R['rows']),'native_generation_runs':sum(len(r['controller']['steps']) for r in R['rows']),
       'conditional_retry_cases':sum(r['controller']['conflict_detected'] for r in R['rows']),
       'answers':len(answers),'abstentions':16-len(answers),
       'answered_correct':sum(r['correct_OFFLINE'] for r in R['rows']),
       'initial_correct':sum(r['initial_correct_OFFLINE'] for r in R['rows']),
       'answer_precision':sum(r['correct_OFFLINE'] for r in R['rows'])/len(answers) if answers else None,
       'autonomous_general_reasoning_proven':False,
       'interpretation':'Bounded metadata-guided closed-loop with physical native evidence checks and conditional retry; not proof of general autonomous reasoning.'}
    R['status']='COMPLETE_RESULTS_RECORDED';save803()
    log('TEST803_COMPLETED',json.dumps(R['summary'],ensure_ascii=False));log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save803()
    log('TEST803_FAILED',repr(e));log(R['traceback']);raise
finally:
    gc.collect()
    if 'release' in globals() and callable(release):release()
    save803()
