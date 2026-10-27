# AKBASCORE SILICON HIPPOCAMPUS — TEST792
# DRA-INSPIRED CUT3 HIDDEN-STATE PRESSURE SWEEP / PHYSICAL CUT3
# ONE COLAB CELL | FROZEN Qwen2.5-72B NF4 | ONE A100 80GB
# Proven TEST790 definitions and TEST779 native engine imported VERBATIM by Git blob.
# NO TRAINING, NO GOLD IN INTERVENTION, NO PERSISTENT HOOKS, NO GRADIO.
# This is an EXTERNAL CONTROLLED CAUSAL PROBE, NOT an autonomous closed loop.
import urllib.request,hashlib,ast,json,traceback,gc,math,time
from pathlib import Path

SOURCE792='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/790.py'
BLOB792='d7e4c4b21e9c3c46276845940a9621751b23897f'
def gitblob792(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with urllib.request.urlopen(urllib.request.Request(SOURCE792,headers={'User-Agent':'AKBASCORE-TEST792'}),timeout=180) as response:
    raw792=response.read()
assert gitblob792(raw792)==BLOB792,('FAIL_CLOSED_TEST790_SOURCE_CHANGED',gitblob792(raw792))
tree792=ast.parse(raw792.decode('utf-8'),filename='790.py')
cut792=next((i for i,n in enumerate(tree792.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:4])),None)
assert cut792 is not None and cut792==len(tree792.body)-1,'FAIL_CLOSED_TEST790_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree792.body[:cut792],type_ignores=[])),
             'TEST790_GPU_PROVEN_LOCKED_PRELUDE','exec'),globals())
# The TEST790 prelude runs only imports and definitions, not its GPU experiment.
assert blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')]
assert gitblob785(raw785)==BLOB
TEST='792';OUT=ROOT/'TEST792_results.json';LOG=ROOT/'TEST792.log';MANIFEST=ROOT/'TEST792_manifest.json'
LOG.write_text('',encoding='utf-8')
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'panel_sha256':PANEL_SHA,'locks':LOCKS,
   'source790_git_blob':BLOB792,'source789_git_blob':blob790(raw790),
   'source779_git_blob':gitblob785(raw785),'checks':[],'rows':[],
   'interventions':[{'label':'OFF','gain':0.0},
                    {'label':'PRESS_PLUS_LOW','gain':0.08},
                    {'label':'PRESS_MINUS_LOW','gain':-0.08},
                    {'label':'PRESS_PLUS_HIGH','gain':0.25},
                    {'label':'PRESS_MINUS_HIGH','gain':-0.25}],
   'limits':['TEST779 original Cut3Diagnostic seed/gain is used, not attention-logit bias.',
             'Direction is extracted from the baseline CUT3 state only; never from gold labels.',
             'CUT3 layer state is a causal intervention target, not a truth compass.',
             'Synthetic TEST779 panel is reused, not held-out evidence of generalization.',
             'The first-token logit test measures output influence, not semantic correctness.',
             'Offline scoring is only after all arms; no oracle-guided selection.',
             'No autonomous feedback controller is claimed.']}
def save792():
    tmp=Path(str(OUT)+'.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT)
def gate792(name,ok,detail=None):
    R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});save792()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST792_GATE_'+name)
def emit792(row):
    R['rows'].append(row);save792();log('TEST792_ROW',json.dumps(row,ensure_ascii=False,default=str))

def probe792(mem,q,seed,gain):
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
        gate792('CUT3_STATE_DIM',state.numel()==H and bool(torch.isfinite(state).all().item()),state.numel())
        gate792('LOGITS_FINITE',bool(torch.isfinite(logits).all().item()))
        return {'state':state,'logits':logits,'state_sha256':hashlib.sha256(state.cpu().numpy().tobytes()).hexdigest(),
                'state_norm':float(state.norm().item()),'cut3_delta_l2':actual_delta,'cut3_steps':steps,
                'first_token_id':int(logits.argmax().item())}
    finally:
        del cache
        assert model.model.layers[CUT].forward==old_forward,'CUT3_FORWARD_NOT_RESTORED'

def compare792(base,arm):
    x=base['state'];y=arm['state'];a=base['logits'];b=arm['logits']
    pa=torch.log_softmax(a,dim=-1);pb=torch.log_softmax(b,dim=-1)
    kl=float(torch.sum(pa.exp()*(pa-pb)).item())
    return {'state_l2_delta':float(torch.linalg.vector_norm(y-x).item()),
            'state_cosine':float(torch.nn.functional.cosine_similarity(x[None],y[None]).item()),
            'logit_l2_delta':float(torch.linalg.vector_norm(b-a).item()),
            'first_token_kl':kl,'first_token_changed':base['first_token_id']!=arm['first_token_id']}


try:
    log('='*112);log('TEST792 — BLIND CUT3 HIDDEN-STATE PRESSURE / NATIVE PHYSICAL MEMORY')
    gate792('TEST790_EXACT_BLOB',gitblob792(raw792)==BLOB792)
    gate792('TEST789_EXACT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate792('TEST779_EXACT_BLOB',gitblob785(raw785)==BLOB)
    gate792('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    gate792('MANIFEST_CONTRACT',R['panel_sha256']==PANEL_SHA and R['locks']==LOCKS)
    persist_manifest()
    gate792('MANIFEST_PREFLIGHT',json.loads(MANIFEST.read_text())['panel_sha256']==PANEL_SHA)
    gate792('PROBE_SYMBOLS',all(callable(globals().get(k)) for k in
       ('Cut3Diagnostic','build_fusion','free_generate','memory_seals','compare_seals','physical_commit')))
    gate792('PRESSURE_SYMMETRY',sorted(x['gain'] for x in R['interventions'])==[-0.25,-0.08,0.0,0.08,0.25])
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    gate792('GPU_VRAM',free>=40*2**30)
    model_setup();before792=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate792('PHYSICAL_20_CARTRIDGES',len(entries)==20,len(entries))
    families=list(FAMILIES)
    # Same TEST790 conflict panel; no changes to synthetic facts or labels.
    extra792={}
    for ix,fam in enumerate(families):
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        decoy=families[(ix+1)%len(families)]['new_team']
        extra792[fid+'_X1']=(f'Authoritative CURRENT record REVISION 1: {work} '
                                f'collaborates_with {decoy}. Supersedes revision 0.')
        extra792[fid+'_X0']=(f'Historical record REVISION 0 (superseded): {work} '
                                f'collaborates_with {decoy}. Valid at revision 0 only.')
    for cid,body in sorted(extra792.items()):physical_commit(cid,body)
    gate792('PHYSICAL_28_CARTRIDGES',len(entries)==28,len(entries))
    gate792('MANIFEST_AFTER_28',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    # Two families x baseline/conflict x current/historical x forward/reverse x five arms = 80 generation runs.
    # All five arms use identical immutable physical memory; only CUT3 hidden-state gain changes.
    for fam in families[:2]:
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        for scenario,pair in [('BASELINE',[fid+'_B0',fid+'_B1']),
                              ('SAME_REV_CONFLICT',[fid+'_B1',fid+'_X1'])]:
            original_sha={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in pair}
            for order_name,order in [('FORWARD',pair),('REVERSE',list(reversed(pair)))]:
                mem=None
                try:
                    mem,active,_,_=build_fusion(order,'TEST792_'+fid+'_'+scenario+'_'+order_name,True)
                    gate792('NATIVE_80_'+fid+'_'+scenario+'_'+order_name,len(mem)==80)
                    gate792('PAIR_ORDER_'+fid+'_'+scenario+'_'+order_name,list(active)==order)
                    spans=spans790(order,mem)
                    original_mem_seal=memory_seals(mem)
                    for view in VIEWS:
                        q=CUE[view].format(work=work)
                        results=[]
                        baseline=probe792(mem,q,None,0.0)
                        # Baseline-only self-direction: zero-mean activation vector.
                        # No labels, answers, expected tokens, or test scenario used.
                        seed=baseline['state']-baseline['state'].mean()
                        gate792('SEED_NONZERO',bool(torch.isfinite(seed).all().item()) and
                                float(seed.norm().item())>1e-6)
                        seed=seed/seed.norm().clamp_min(1e-6)
                        baseline_prediction=None
                        for arm in R['interventions']:
                            gain=float(arm['gain']);label=arm['label']
                            measure=baseline if gain==0 else probe792(mem,q,seed,gain)
                            # EXACT existing TEST779 generation primitive; only CUT3 seed/gain differs.
                            output=free_generate(mem,q,seed=seed if gain else None,gain=gain,
                                                 max_new=MAX_TOKENS,spans=spans)
                            prediction=parse789(output['raw'])
                            row={'arm':label,'gain':gain,'prediction':prediction,'raw':output['raw'],
                                 'generated_tokens':output['generated_tokens'],
                                 'sdpa_calls':output['sdpa_calls'],
                                 'state_norm':measure['state_norm'],
                                 'state_sha256':measure['state_sha256'],
                                 'cut3_delta_l2':measure['cut3_delta_l2'],
                                 'cut3_steps':measure['cut3_steps'],
                                 'first_token_id':measure['first_token_id']}
                            row.update(compare792(baseline,measure))
                            if label=='OFF':baseline_prediction=prediction
                            else:row['prediction_changed']=prediction!=baseline_prediction
                            results.append(row)
                            if gain:del measure
                        gate792('FIVE_ARMS_'+fid+'_'+scenario+'_'+order_name+'_'+view,len(results)==5)
                        expected=fam['new_team'] if view=='CURRENT' else fam['old_team']
                        for row in results:row['correct_OFFLINE']=row['prediction']==expected
                        emit792({'family':fid,'scenario_OFFLINE':scenario,'view_OFFLINE':view,
                                 'order':order_name,'cartridges':list(order),
                                 'baseline_prediction':baseline_prediction,
                                 'expected_OFFLINE':expected,'arms':results})
                        del baseline,seed
                    gate792('KV_UNCHANGED_'+fid+'_'+scenario+'_'+order_name,
                            compare_seals(original_mem_seal,memory_seals(mem)))
                finally:
                    del mem;gc.collect();release()
            for cid,h in original_sha.items():
                gate792('SSD_SHA_UNCHANGED_'+cid,sha_file(CART_DIR/(cid+'.pt'))==h)
    gate792('TOTAL_CASES',len(R['rows'])==16,len(R['rows']))
    gate792('TOTAL_INTERVENTIONS',sum(len(row['arms']) for row in R['rows'])==80)
    gate792('FROZEN_WEIGHTS',sentinel()==before792)
    gate792('FINAL_MANIFEST',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    gate792('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
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
                  'interpretation':'Native CUT3 hidden-state pressure and downstream logit propagation; no autonomous controller.'}
    R['status']='COMPLETE_RESULTS_RECORDED';save792()
    log('TEST792_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save792()
    log('TEST792_FAILED',repr(e));log(R['traceback']);raise
finally:save792()
