# AKBASCORE SILICON HIPPOCAMPUS — TEST793
# DRA-INSPIRED DIRECTIONAL CUT3 PRESSURE / VIEW-CONTRAST CONTROL
# ONE COLAB CELL | FROZEN Qwen2.5-72B NF4 | ONE A100 80GB
# Proven TEST790 definitions and TEST779 native engine imported VERBATIM by Git blob.
# NO TRAINING, NO GOLD IN INTERVENTION, NO PERSISTENT HOOKS, NO GRADIO.
# This is an EXTERNAL CONTROLLED CAUSAL PROBE, NOT an autonomous closed loop.
import urllib.request,hashlib,ast,json,traceback,gc,math,time
from pathlib import Path

SOURCE793='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/790.py'
BLOB793='d7e4c4b21e9c3c46276845940a9621751b23897f'
def gitblob793(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with urllib.request.urlopen(urllib.request.Request(SOURCE793,headers={'User-Agent':'AKBASCORE-TEST793'}),timeout=180) as response:
    raw793=response.read()
assert gitblob793(raw793)==BLOB793,('FAIL_CLOSED_TEST790_SOURCE_CHANGED',gitblob793(raw793))
tree793=ast.parse(raw793.decode('utf-8'),filename='790.py')
cut793=next((i for i,n in enumerate(tree793.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:4])),None)
assert cut793 is not None and cut793==len(tree793.body)-1,'FAIL_CLOSED_TEST790_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree793.body[:cut793],type_ignores=[])),
             'TEST790_GPU_PROVEN_LOCKED_PRELUDE','exec'),globals())
# The TEST790 prelude runs only imports and definitions, not its GPU experiment.
assert blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')]
assert gitblob785(raw785)==BLOB
TEST='793';OUT=ROOT/'TEST793_results.json';LOG=ROOT/'TEST793.log';MANIFEST=ROOT/'TEST793_manifest.json'
LOG.write_text('',encoding='utf-8')
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'panel_sha256':PANEL_SHA,'locks':LOCKS,
   'source790_git_blob':BLOB793,'source789_git_blob':blob790(raw790),
   'source779_git_blob':gitblob785(raw785),'checks':[],'rows':[],
   'interventions':[{'label':'OFF','direction':'NONE','gain':0.0},
                    {'label':'SELF_PLUS','direction':'SELF','gain':0.25},
                    {'label':'SELF_MINUS','direction':'SELF','gain':-0.25},
                    {'label':'CONTRAST_PLUS','direction':'VIEW_CONTRAST','gain':0.25},
                    {'label':'CONTRAST_MINUS','direction':'VIEW_CONTRAST','gain':-0.25}],
   'limits':['TEST779 original Cut3Diagnostic seed/gain is used, not attention-logit bias.',
             'Directions use only baseline CUT3 states from CURRENT and HISTORICAL prompts; no gold labels.',
             'VIEW_CONTRAST direction is a question-view contrast, NOT a source-isolated memory direction.',
             'CUT3 layer state is a causal intervention target, not a truth compass.',
             'Synthetic TEST779 panel is reused, not held-out evidence of generalization.',
             'The first-token logit test measures output influence, not semantic correctness.',
             'Offline scoring is only after all arms; no oracle-guided selection.',
             'No autonomous feedback controller is claimed.']}
def save793():
    tmp=Path(str(OUT)+'.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT)
def gate793(name,ok,detail=None):
    R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});save793()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST793_GATE_'+name)
def emit793(row):
    R['rows'].append(row);save793();log('TEST793_ROW',json.dumps(row,ensure_ascii=False,default=str))

def probe793(mem,q,seed,gain):
    """Use the EXACT TEST779 Cut3Diagnostic pressure primitive on the true forward path.
    Return CUT3 output and first next-token logits from the same forward pass.
    No attention intervention; all output-layer effects are native downstream propagation.
    """
    qids=prompt_ids(q);n=int(mem[0][0].shape[-2]);cache=cache_build(mem)
    pos=torch.arange(n,n+len(qids),device=DEV)
    old_forward=model.model.layers[CUT].forward
    try:
        with torch.no_grad(),Cut3Diagnostic(seed=seed,gain=gain) as diag:
            output=model(input_ids=torch.tensor([qids],device=DEV),past_key_values=cache,
                attention_mask=torch.ones((1,n+len(qids)),device=DEV,dtype=torch.long),
                position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
            state=diag.last.float().detach().reshape(-1).contiguous().clone()
            logits=output.logits[0,-1].float().detach().clone()
            actual_delta=float(diag.delta_l2)
            steps=int(diag.steps)
            del output
        gate793('CUT3_STATE_DIM',state.numel()==H and bool(torch.isfinite(state).all().item()),state.numel())
        gate793('LOGITS_FINITE',bool(torch.isfinite(logits).all().item()))
        return {'state':state,'logits':logits,'state_sha256':hashlib.sha256(state.cpu().numpy().tobytes()).hexdigest(),
                'state_norm':float(state.norm().item()),'cut3_delta_l2':actual_delta,'cut3_steps':steps,
                'first_token_id':int(logits.argmax().item())}
    finally:
        del cache
        assert model.model.layers[CUT].forward==old_forward,'CUT3_FORWARD_NOT_RESTORED'

def compare793(base,arm):
    x=base['state'];y=arm['state'];a=base['logits'];b=arm['logits']
    pa=torch.log_softmax(a,dim=-1);pb=torch.log_softmax(b,dim=-1)
    kl=float(torch.sum(pa.exp()*(pa-pb)).item())
    return {'state_l2_delta':float(torch.linalg.vector_norm(y-x).item()),
            'state_cosine':float(torch.nn.functional.cosine_similarity(x[None],y[None]).item()),
            'logit_l2_delta':float(torch.linalg.vector_norm(b-a).item()),
            'first_token_kl':kl,'first_token_changed':base['first_token_id']!=arm['first_token_id']}


try:
    log('='*112);log('TEST793 — BLIND CUT3 HIDDEN-STATE PRESSURE / NATIVE PHYSICAL MEMORY')
    gate793('TEST790_EXACT_BLOB',gitblob793(raw793)==BLOB793)
    gate793('TEST789_EXACT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate793('TEST779_EXACT_BLOB',gitblob785(raw785)==BLOB)
    gate793('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    gate793('MANIFEST_CONTRACT',R['panel_sha256']==PANEL_SHA and R['locks']==LOCKS)
    persist_manifest()
    gate793('MANIFEST_PREFLIGHT',json.loads(MANIFEST.read_text())['panel_sha256']==PANEL_SHA)
    gate793('PROBE_SYMBOLS',all(callable(globals().get(k)) for k in
       ('Cut3Diagnostic','build_fusion','free_generate','memory_seals','compare_seals','physical_commit')))
    gate793('PRESSURE_SYMMETRY',sorted(x['gain'] for x in R['interventions'])==[-0.25,-0.25,0.0,0.25,0.25])
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    gate793('GPU_VRAM',free>=40*2**30)
    model_setup();before793=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate793('PHYSICAL_20_CARTRIDGES',len(entries)==20,len(entries))
    families=list(FAMILIES)
    # Same TEST790 conflict panel; no changes to synthetic facts or labels.
    extra793={}
    for ix,fam in enumerate(families):
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        decoy=families[(ix+1)%len(families)]['new_team']
        extra793[fid+'_X1']=(f'Authoritative CURRENT record REVISION 1: {work} '
                                f'collaborates_with {decoy}. Supersedes revision 0.')
        extra793[fid+'_X0']=(f'Historical record REVISION 0 (superseded): {work} '
                                f'collaborates_with {decoy}. Valid at revision 0 only.')
    for cid,body in sorted(extra793.items()):physical_commit(cid,body)
    gate793('PHYSICAL_28_CARTRIDGES',len(entries)==28,len(entries))
    gate793('MANIFEST_AFTER_28',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    # Two families x baseline/conflict x current/historical x forward/reverse x five arms = 80 generation runs.
    # All five arms use identical immutable physical memory; only direction/gain change.
    for fam in families[:2]:
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        for scenario,pair in [('BASELINE',[fid+'_B0',fid+'_B1']),
                              ('SAME_REV_CONFLICT',[fid+'_B1',fid+'_X1'])]:
            original_sha={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in pair}
            for order_name,order in [('FORWARD',pair),('REVERSE',list(reversed(pair)))]:
                mem=None
                try:
                    mem,active,_,_=build_fusion(order,'TEST793_'+fid+'_'+scenario+'_'+order_name,True)
                    gate793('NATIVE_80_'+fid+'_'+scenario+'_'+order_name,len(mem)==80)
                    gate793('PAIR_ORDER_'+fid+'_'+scenario+'_'+order_name,list(active)==order)
                    spans=spans790(order,mem)
                    original_mem_seal=memory_seals(mem)
                    # Both view baselines are measured BEFORE any intervention. The
                    # contrast is question-view dependent, not gold/source supervised.
                    questions={view:CUE[view].format(work=work) for view in VIEWS}
                    baselines={view:probe793(mem,questions[view],None,0.0) for view in VIEWS}
                    gate793('TWO_BASELINES',len(baselines)==2)
                    for view in VIEWS:
                        q=questions[view];baseline=baselines[view]
                        opposite=next(v for v in VIEWS if v!=view)
                        self_seed=baseline['state']-baseline['state'].mean()
                        contrast_seed=baseline['state']-baselines[opposite]['state']
                        directions={'SELF':self_seed,'VIEW_CONTRAST':contrast_seed}
                        for key,vec in directions.items():
                            gate793('SEED_NONZERO_'+key,bool(torch.isfinite(vec).all().item()) and
                                    float(vec.norm().item())>1e-6)
                            directions[key]=vec/vec.norm().clamp_min(1e-6)
                        results=[];baseline_prediction=None
                        for arm in R['interventions']:
                            gain=float(arm['gain']);label=arm['label']
                            direction=arm['direction']
                            seed=None if direction=='NONE' else directions[direction]
                            measure=baseline if gain==0 else probe793(mem,q,seed,gain)
                            output=free_generate(mem,q,seed=seed,gain=gain,
                                                 max_new=MAX_TOKENS,spans=spans)
                            prediction=parse789(output['raw'])
                            row={'arm':label,'direction':direction,'gain':gain,
                                 'prediction':prediction,'raw':output['raw'],
                                 'generated_tokens':output['generated_tokens'],
                                 'sdpa_calls':output['sdpa_calls'],
                                 'state_norm':measure['state_norm'],
                                 'state_sha256':measure['state_sha256'],
                                 'cut3_delta_l2':measure['cut3_delta_l2'],
                                 'cut3_steps':measure['cut3_steps'],
                                 'first_token_id':measure['first_token_id']}
                            row.update(compare793(baseline,measure))
                            if label=='OFF':baseline_prediction=prediction
                            else:row['prediction_changed']=prediction!=baseline_prediction
                            results.append(row)
                            if gain:del measure
                        gate793('FIVE_ARMS_'+fid+'_'+scenario+'_'+order_name+'_'+view,len(results)==5)
                        expected=fam['new_team'] if view=='CURRENT' else fam['old_team']
                        for row in results:row['correct_OFFLINE']=row['prediction']==expected
                        emit793({'family':fid,'scenario_OFFLINE':scenario,'view_OFFLINE':view,
                                 'order':order_name,'cartridges':list(order),
                                 'baseline_prediction':baseline_prediction,
                                 'expected_OFFLINE':expected,'arms':results})
                    del baselines
                    gate793('KV_UNCHANGED_'+fid+'_'+scenario+'_'+order_name,
                            compare_seals(original_mem_seal,memory_seals(mem)))
                finally:
                    del mem;gc.collect();release()
            for cid,h in original_sha.items():
                gate793('SSD_SHA_UNCHANGED_'+cid,sha_file(CART_DIR/(cid+'.pt'))==h)
    gate793('TOTAL_CASES',len(R['rows'])==16,len(R['rows']))
    gate793('TOTAL_INTERVENTIONS',sum(len(row['arms']) for row in R['rows'])==80)
    gate793('FROZEN_WEIGHTS',sentinel()==before793)
    gate793('FINAL_MANIFEST',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    gate793('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    changed=sum(a.get('prediction_changed',False) for row in R['rows'] for a in row['arms'])
    improved=sum(a['correct_OFFLINE'] and not row['arms'][0]['correct_OFFLINE']
                 for row in R['rows'] for a in row['arms'][1:])
    damaged=sum(not a['correct_OFFLINE'] and row['arms'][0]['correct_OFFLINE']
                for row in R['rows'] for a in row['arms'][1:])
    nonzero=sum(a['state_l2_delta']>1e-5 for row in R['rows'] for a in row['arms'][1:])
    logit_effects=sum(a['logit_l2_delta']>1e-5 for row in R['rows'] for a in row['arms'][1:])
    first_changes=sum(a['first_token_changed'] for row in R['rows'] for a in row['arms'][1:])
    R['summary']={'cases':len(R['rows']),'generation_runs':80,'changed_outputs':changed,
                  'nonzero_cut3_state_effects':nonzero,'nonzero_logit_effects':logit_effects,
                  'first_token_argmax_changes':first_changes,
                  'offline_improvements':improved,'offline_damages':damaged,
                  'baseline_correct':sum(row['arms'][0]['correct_OFFLINE'] for row in R['rows']),
                  'interpretation':'Compare baseline-self versus question-view contrast directions on native CUT3; no autonomous controller or source-isolated direction.'}
    R['status']='COMPLETE_RESULTS_RECORDED';save793()
    log('TEST793_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save793()
    log('TEST793_FAILED',repr(e));log(R['traceback']);raise
finally:save793()
