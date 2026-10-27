# AKBASCORE SILICON HIPPOCAMPUS — TEST791
# CONTROLLED DRA-INSPIRED ATTENTION DOSE RESPONSE / PHYSICAL CUT3
# ONE COLAB CELL | FROZEN Qwen2.5-72B NF4 | ONE A100 80GB
# Proven TEST790 definitions and TEST779 native engine imported VERBATIM by Git blob.
# NO TRAINING, NO GOLD IN INTERVENTION, NO PERSISTENT HOOKS, NO GRADIO.
# This is an EXTERNAL CONTROLLED CAUSAL PROBE, NOT an autonomous closed loop.
import urllib.request,hashlib,ast,json,traceback,gc,math,time
from pathlib import Path

SOURCE791='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/790.py'
BLOB791='d7e4c4b21e9c3c46276845940a9621751b23897f'
def gitblob791(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with urllib.request.urlopen(urllib.request.Request(SOURCE791,headers={'User-Agent':'AKBASCORE-TEST791'}),timeout=180) as response:
    raw791=response.read()
assert gitblob791(raw791)==BLOB791,('FAIL_CLOSED_TEST790_SOURCE_CHANGED',gitblob791(raw791))
tree791=ast.parse(raw791.decode('utf-8'),filename='790.py')
cut791=next((i for i,n in enumerate(tree791.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:4])),None)
assert cut791 is not None and cut791==len(tree791.body)-1,'FAIL_CLOSED_TEST790_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree791.body[:cut791],type_ignores=[])),
             'TEST790_GPU_PROVEN_LOCKED_PRELUDE','exec'),globals())
# The TEST790 prelude runs only imports and definitions, not its GPU experiment.
assert blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')]
assert gitblob785(raw785)==BLOB
TEST='791';OUT=ROOT/'TEST791_results.json';LOG=ROOT/'TEST791.log';MANIFEST=ROOT/'TEST791_manifest.json'
LOG.write_text('',encoding='utf-8')
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'panel_sha256':PANEL_SHA,'locks':LOCKS,
   'source790_git_blob':BLOB791,'source789_git_blob':blob790(raw790),
   'source779_git_blob':gitblob785(raw785),'checks':[],'rows':[],
   'interventions':[{'label':'OFF','slot':None,'dose':0.0},
                    {'label':'B0_PLUS','slot':'B0','dose':0.7},
                    {'label':'B0_MINUS','slot':'B0','dose':-0.7},
                    {'label':'B1_PLUS','slot':'B1','dose':0.7},
                    {'label':'B1_MINUS','slot':'B1','dose':-0.7}],
   'limits':['This is a controlled attention-logit intervention, NOT a full historical DRA engine.',
             'Synthetic TEST779 panel is reused, not a held-out generalization panel.',
             'Physical slot B0/B1 changes cartridge identity on reversed order.',
             'No oracle, gold, view/scenario or source truth is used for intervention selection.',
             'Attention shifts and state shifts are NOT proofs of semantic correctness.',
             'Temporary SDPA and module.forward instrumentation is restored after every probe.',
             'No autonomous stopping or iterative controller is implemented.']}
def save791():
    tmp=Path(str(OUT)+'.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT)
def gate791(name,ok,detail=None):
    R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});save791()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST791_GATE_'+name)
def emit791(row):
    R['rows'].append(row);save791();log('TEST791_ROW',json.dumps(row,ensure_ascii=False,default=str))

def measure791(mem,q,spans,slot,dose):
    """TEST779 exact Cut3Diagnostic + AttentionIntervention primitives; dose applied to real KV rows."""
    qids=prompt_ids(q);n=int(mem[0][0].shape[-2]);cache=cache_build(mem)
    pos=torch.arange(n,n+len(qids),device=DEV)
    old_sdpa=F.scaled_dot_product_attention
    old_forwards={i:model.model.layers[i].self_attn.forward for i in (4,20,40,79)}
    try:
        with torch.no_grad():
            with Cut3Diagnostic() as diag,AttentionIntervention(spans,bias_span=slot,bias=dose) as probe:
                output=model(input_ids=torch.tensor([qids],device=DEV),past_key_values=cache,
                    attention_mask=torch.ones((1,n+len(qids)),device=DEV,dtype=torch.long),
                    position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
                gate791('ACTIVE_STATE_PROBE',diag.last is not None and probe.calls>=4,probe.calls)
                state=diag.last.float().detach().reshape(-1).contiguous().clone()
                gate791('STATE_DIM_FINITE',state.numel()==H and bool(torch.isfinite(state).all().item()),state.numel())
                att=aggregate_attention(probe.records)
                del output
        norm=float(torch.linalg.vector_norm(state).item())
        digest=hashlib.sha256(state.cpu().numpy().tobytes()).hexdigest()
        density=source_signal(att,spans)[2]
        return {'state':state,'norm':norm,'state_sha256':digest,'attention':att,'density':density,
                'probe_calls':probe.calls}
    finally:
        del cache
        # Fail closed on leaked runtime instrumentation.
        assert F.scaled_dot_product_attention is old_sdpa,'SDPA_NOT_RESTORED'
        assert all(model.model.layers[i].self_attn.forward==old_forwards[i] for i in old_forwards),'FORWARD_NOT_RESTORED'

def compare791(base,arm):
    x=base['state'];y=arm['state'];delta=y-x
    return {'state_l2_delta':float(torch.linalg.vector_norm(delta).item()),
            'state_cosine':float(torch.nn.functional.cosine_similarity(x[None],y[None]).item()),
            'B0_density_delta':float(arm['density']['B0']-base['density']['B0']),
            'B1_density_delta':float(arm['density']['B1']-base['density']['B1'])}

try:
    log('='*112);log('TEST791 — BLIND BIDIRECTIONAL ATTENTION DOSE RESPONSE / NATIVE PHYSICAL CUT3')
    gate791('TEST790_EXACT_BLOB',gitblob791(raw791)==BLOB791)
    gate791('TEST789_EXACT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate791('TEST779_EXACT_BLOB',gitblob785(raw785)==BLOB)
    gate791('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    gate791('MANIFEST_CONTRACT',R['panel_sha256']==PANEL_SHA and R['locks']==LOCKS)
    persist_manifest()
    gate791('MANIFEST_PREFLIGHT',json.loads(MANIFEST.read_text())['panel_sha256']==PANEL_SHA)
    gate791('PROBE_SYMBOLS',all(callable(globals().get(k)) for k in
       ('observe_state','source_signal','build_fusion','free_generate','memory_seals','compare_seals','physical_commit')))
    gate791('DOSE_SYMMETRY',sorted(x['dose'] for x in R['interventions'])==[-0.7,-0.7,0.0,0.7,0.7])
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    gate791('GPU_VRAM',free>=40*2**30)
    model_setup();before791=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate791('PHYSICAL_20_CARTRIDGES',len(entries)==20,len(entries))
    families=list(FAMILIES)
    # Same TEST790 conflict panel; no changes to synthetic facts or labels.
    extra791={}
    for ix,fam in enumerate(families):
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        decoy=families[(ix+1)%len(families)]['new_team']
        extra791[fid+'_X1']=(f'Authoritative CURRENT record REVISION 1: {work} '
                                f'collaborates_with {decoy}. Supersedes revision 0.')
        extra791[fid+'_X0']=(f'Historical record REVISION 0 (superseded): {work} '
                                f'collaborates_with {decoy}. Valid at revision 0 only.')
    for cid,body in sorted(extra791.items()):physical_commit(cid,body)
    gate791('PHYSICAL_28_CARTRIDGES',len(entries)==28,len(entries))
    gate791('MANIFEST_AFTER_28',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    # Two families x baseline/conflict x current/historical x forward/reverse x five arms = 80 generation runs.
    # All five arms run on the same immutable physical cache; only attention bias changes.
    for fam in families[:2]:
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        for scenario,pair in [('BASELINE',[fid+'_B0',fid+'_B1']),
                              ('SAME_REV_CONFLICT',[fid+'_B1',fid+'_X1'])]:
            original_sha={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in pair}
            for order_name,order in [('FORWARD',pair),('REVERSE',list(reversed(pair)))]:
                mem=None
                try:
                    mem,active,_,_=build_fusion(order,'TEST791_'+fid+'_'+scenario+'_'+order_name,True)
                    gate791('NATIVE_80_'+fid+'_'+scenario+'_'+order_name,len(mem)==80)
                    gate791('PAIR_ORDER_'+fid+'_'+scenario+'_'+order_name,list(active)==order)
                    spans=spans790(order,mem)
                    original_mem_seal=memory_seals(mem)
                    for view in VIEWS:
                        q=CUE[view].format(work=work)
                        results=[];base_state=None;baseline_prediction=None
                        for arm in R['interventions']:
                            slot=arm['slot'];dose=arm['dose'];label=arm['label']
                            measure=measure791(mem,q,spans,slot,dose)
                            output=free_generate(mem,q,max_new=MAX_TOKENS,spans=spans,
                                                 bias_span=slot,bias=dose)
                            prediction=parse789(output['raw'])
                            row={'arm':label,'physical_slot':slot,'dose':dose,
                                 'physical_cartridge':order[0] if slot=='B0' else order[1] if slot=='B1' else None,
                                 'prediction':prediction,'raw':output['raw'],
                                 'generated_tokens':output['generated_tokens'],
                                 'sdpa_calls':output['sdpa_calls'],
                                 'state_norm':measure['norm'],'state_sha256':measure['state_sha256'],
                                 'attention':measure['attention'],'density':measure['density']}
                            if label=='OFF':
                                base_state=measure;baseline_prediction=prediction
                                row['state_l2_delta']=0.0;row['state_cosine']=1.0
                                row['B0_density_delta']=0.0;row['B1_density_delta']=0.0
                            else:
                                row.update(compare791(base_state,measure))
                                row['prediction_changed']=prediction!=baseline_prediction
                            results.append(row)
                            del measure
                        gate791('FIVE_ARMS_'+fid+'_'+scenario+'_'+order_name+'_'+view,len(results)==5)
                        # Offline scoring ONLY after all interventions have finished.
                        expected=fam['new_team'] if view=='CURRENT' else fam['old_team']
                        for row in results:row['correct_OFFLINE']=row['prediction']==expected
                        emit791({'family':fid,'scenario_OFFLINE':scenario,'view_OFFLINE':view,
                                 'order':order_name,'cartridges':list(order),
                                 'baseline_prediction':baseline_prediction,
                                 'expected_OFFLINE':expected,'arms':results})
                    gate791('KV_UNCHANGED_'+fid+'_'+scenario+'_'+order_name,
                            compare_seals(original_mem_seal,memory_seals(mem)))
                finally:
                    del mem;gc.collect();release()
            for cid,h in original_sha.items():
                gate791('SSD_SHA_UNCHANGED_'+cid,sha_file(CART_DIR/(cid+'.pt'))==h)
    gate791('TOTAL_CASES',len(R['rows'])==16,len(R['rows']))
    gate791('TOTAL_INTERVENTIONS',sum(len(row['arms']) for row in R['rows'])==80)
    gate791('FROZEN_WEIGHTS',sentinel()==before791)
    gate791('FINAL_MANIFEST',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    gate791('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    changed=sum(a.get('prediction_changed',False) for row in R['rows'] for a in row['arms'])
    improved=sum(a['correct_OFFLINE'] and not row['arms'][0]['correct_OFFLINE']
                 for row in R['rows'] for a in row['arms'][1:])
    damaged=sum(not a['correct_OFFLINE'] and row['arms'][0]['correct_OFFLINE']
                for row in R['rows'] for a in row['arms'][1:])
    nonzero=sum(a['state_l2_delta']>1e-5 for row in R['rows'] for a in row['arms'][1:])
    R['summary']={'cases':len(R['rows']),'generation_runs':80,'changed_outputs':changed,
                  'nonzero_state_effects':nonzero,'offline_improvements':improved,
                  'offline_damages':damaged,'baseline_correct':sum(row['arms'][0]['correct_OFFLINE'] for row in R['rows']),
                  'interpretation':'Causal dose-response audit only; no autonomous controller or correctness oracle.'}
    R['status']='COMPLETE_RESULTS_RECORDED';save791()
    log('TEST791_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save791()
    log('TEST791_FAILED',repr(e));log(R['traceback']);raise
finally:save791()
