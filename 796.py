# AKBASCORE SILICON HIPPOCAMPUS — TEST796
# DRA-INSPIRED DISJOINT MATCHED KV CONTROLS / BLIND PRESSURE DOSE AUDIT
# ONE COLAB CELL | FROZEN Qwen2.5-72B NF4 | ONE A100 80GB
# Proven TEST790 definitions and TEST779 native engine imported VERBATIM by Git blob.
# NO TRAINING, NO GOLD IN INTERVENTION, NO PERSISTENT HOOKS, NO GRADIO.
# This is an EXTERNAL CONTROLLED CAUSAL PROBE, NOT an autonomous closed loop.
import urllib.request,hashlib,ast,json,traceback,gc,math,time
from pathlib import Path

SOURCE796='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/790.py'
BLOB796='d7e4c4b21e9c3c46276845940a9621751b23897f'
def gitblob796(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with urllib.request.urlopen(urllib.request.Request(SOURCE796,headers={'User-Agent':'AKBASCORE-TEST796'}),timeout=180) as response:
    raw796=response.read()
assert gitblob796(raw796)==BLOB796,('FAIL_CLOSED_TEST790_SOURCE_CHANGED',gitblob796(raw796))
tree796=ast.parse(raw796.decode('utf-8'),filename='790.py')
cut796=next((i for i,n in enumerate(tree796.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:4])),None)
assert cut796 is not None and cut796==len(tree796.body)-1,'FAIL_CLOSED_TEST790_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree796.body[:cut796],type_ignores=[])),
             'TEST790_GPU_PROVEN_LOCKED_PRELUDE','exec'),globals())
# The TEST790 prelude runs only imports and definitions, not its GPU experiment.
assert blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')]
assert gitblob785(raw785)==BLOB
TEST='796';OUT=ROOT/'TEST796_results.json';LOG=ROOT/'TEST796.log';MANIFEST=ROOT/'TEST796_manifest.json'
LOG.write_text('',encoding='utf-8')
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'panel_sha256':PANEL_SHA,'locks':LOCKS,
   'source790_git_blob':BLOB796,'source789_git_blob':blob790(raw790),
   'source779_git_blob':gitblob785(raw785),'checks':[],'rows':[],
   'interventions':[{'label':'OFF','direction':'NONE','gain':0.0},
                    {'label':'SOURCE0_PLUS','direction':'SOURCE0_MASK','gain':0.5},
                    {'label':'SOURCE0_MINUS','direction':'SOURCE0_MASK','gain':-0.5},
                    {'label':'SOURCE1_PLUS','direction':'SOURCE1_MASK','gain':0.5},
                    {'label':'SOURCE1_MINUS','direction':'SOURCE1_MASK','gain':-0.5}],
   'limits':['TEST779 original Cut3Diagnostic seed/gain is used, not attention-logit bias.',
             'Direction is full-pair CUT3 state minus same-length K/V-masked memory CUT3 state; no gold labels.',
             'Zeroing K and V is a perturbation, not true source deletion: zero keys still occupy attention slots.',
             'Sham and source masks have equal size and are strictly disjoint; use matched partial spans when lengths differ.',
             'Direction is masked-minus-sham CUT3 state, not full-minus-masked; this cancels some generic masking effect, not all positional confounds.',
             'Dose sweep is observation only; neither gold labels nor test correctness selects a dose.',
             'No re-fusion or source-text replay is used for masked controls.',
             'CUT3 layer state is a causal intervention target, not a truth compass.',
             'Synthetic TEST779 panel is reused, not held-out evidence of generalization.',
             'The first-token logit test measures output influence, not semantic correctness.',
             'Offline scoring is only after all arms; no oracle-guided selection.',
             'No autonomous feedback controller is claimed.']}
def save796():
    tmp=Path(str(OUT)+'.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT)
def gate796(name,ok,detail=None):
    R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});save796()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST796_GATE_'+name)
def emit796(row):
    R['rows'].append(row);save796();log('TEST796_ROW',json.dumps(row,ensure_ascii=False,default=str))

def probe796(mem,q,seed,gain):
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
        gate796('CUT3_STATE_DIM',state.numel()==H and bool(torch.isfinite(state).all().item()),state.numel())
        gate796('LOGITS_FINITE',bool(torch.isfinite(logits).all().item()))
        return {'state':state,'logits':logits,'state_sha256':hashlib.sha256(state.cpu().numpy().tobytes()).hexdigest(),
                'state_norm':float(state.norm().item()),'cut3_delta_l2':actual_delta,'cut3_steps':steps,
                'first_token_id':int(logits.argmax().item())}
    finally:
        del cache
        assert model.model.layers[CUT].forward==old_forward,'CUT3_FORWARD_NOT_RESTORED'

def compare796(base,arm):
    x=base['state'];y=arm['state'];a=base['logits'];b=arm['logits']
    pa=torch.log_softmax(a,dim=-1);pb=torch.log_softmax(b,dim=-1)
    kl=float(torch.sum(pa.exp()*(pa-pb)).item())
    top2=torch.topk(a,2)
    first=int(top2.indices[0].item());second=int(top2.indices[1].item())
    margin_before=float((a[first]-a[second]).item())
    margin_after=float((b[first]-b[second]).item())
    top_after=torch.topk(b,2)
    return {'baseline_top1_token':first,'baseline_top2_token':second,
            'baseline_margin':margin_before,
            'same_pair_margin_after':margin_after,
            'same_pair_margin_delta':margin_after-margin_before,
            'actual_top1_margin_after':float((top_after.values[0]-top_after.values[1]).item()),
            'baseline_top1_rank_after':int((b>b[first]).sum().item())+1,
            'state_l2_delta':float(torch.linalg.vector_norm(y-x).item()),
            'state_cosine':float(torch.nn.functional.cosine_similarity(x[None],y[None]).item()),
            'logit_l2_delta':float(torch.linalg.vector_norm(b-a).item()),
            'first_token_kl':kl,'first_token_changed':base['first_token_id']!=arm['first_token_id']}



def mask796(mem,positions):
    """Length-preserving physical-KV intervention, never mutates original tensor storage.
    Positions are absolute indices in the existing fused prefix. K/V at selected
    positions are set to zero in every layer. This is not true source removal.
    """
    n=int(mem[0][0].shape[-2]);pos=sorted(set(int(p) for p in positions))
    gate796('MASK_POSITIONS_VALID',bool(pos) and min(pos)>=P and max(pos)<n)
    result=[]
    for layer in mem:
        k,v=layer[0],layer[1]
        kc=k.clone();vc=v.clone()
        kc[...,pos,:]=0;vc[...,pos,:]=0
        # preserve any optional metadata without modifying it
        result.append((kc,vc,*layer[2:]))
    gate796('MASK_LENGTH_INVARIANT',len(result)==len(mem) and
            all(result[i][0].shape==mem[i][0].shape and result[i][1].shape==mem[i][1].shape
                for i in range(len(mem))))
    return result

def disjoint_pair796(source_start,source_end,other_start,other_end):
    """Equal-cardinality nonoverlapping mask spans. When lengths differ,
    compare matched partial spans; this is not a full-source ablation.
    """
    length=min(source_end-source_start,other_end-other_start)
    if length<=0:raise RuntimeError('EMPTY_DISJOINT_SPAN')
    target=list(range(source_start,source_start+length))
    control=list(range(other_start,other_start+length))
    if len(set(target)&set(control))!=0:raise RuntimeError('MASK_OVERLAP')
    return target,control


try:
    log('='*112);log('TEST796 — STRICT DISJOINT MASK / BLIND DOSE / NATIVE PHYSICAL MEMORY')
    gate796('TEST790_EXACT_BLOB',gitblob796(raw796)==BLOB796)
    gate796('TEST789_EXACT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate796('TEST779_EXACT_BLOB',gitblob785(raw785)==BLOB)
    gate796('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    gate796('MANIFEST_CONTRACT',R['panel_sha256']==PANEL_SHA and R['locks']==LOCKS)
    persist_manifest()
    gate796('MANIFEST_PREFLIGHT',json.loads(MANIFEST.read_text())['panel_sha256']==PANEL_SHA)
    gate796('PROBE_SYMBOLS',all(callable(globals().get(k)) for k in
       ('Cut3Diagnostic','build_fusion','free_generate','memory_seals','compare_seals','physical_commit')))
    gate796('PRESSURE_SYMMETRY',sorted(x['gain'] for x in R['interventions'])==[-0.5,-0.5,0.0,0.5,0.5])
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    gate796('GPU_VRAM',free>=40*2**30)
    model_setup();before796=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate796('PHYSICAL_20_CARTRIDGES',len(entries)==20,len(entries))
    families=list(FAMILIES)
    # Same TEST790 conflict panel; no changes to synthetic facts or labels.
    extra796={}
    for ix,fam in enumerate(families):
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        decoy=families[(ix+1)%len(families)]['new_team']
        extra796[fid+'_X1']=(f'Authoritative CURRENT record REVISION 1: {work} '
                                f'collaborates_with {decoy}. Supersedes revision 0.')
        extra796[fid+'_X0']=(f'Historical record REVISION 0 (superseded): {work} '
                                f'collaborates_with {decoy}. Valid at revision 0 only.')
    for cid,body in sorted(extra796.items()):physical_commit(cid,body)
    gate796('PHYSICAL_28_CARTRIDGES',len(entries)==28,len(entries))
    gate796('MANIFEST_AFTER_28',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
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
                    mem,active,_,_=build_fusion(order,'TEST796_'+fid+'_'+scenario+'_'+order_name,True)
                    gate796('NATIVE_80_'+fid+'_'+scenario+'_'+order_name,len(mem)==80)
                    gate796('PAIR_ORDER_'+fid+'_'+scenario+'_'+order_name,list(active)==order)
                    spans=spans790(order,mem)
                    original_mem_seal=memory_seals(mem)
                    questions={view:CUE[view].format(work=work) for view in VIEWS}
                    baselines={view:probe796(mem,questions[view],None,0.0) for view in VIEWS}
                    # Controlled same-length perturbations of the already fused physical KV.
                    # Each mask is transient, and the untouched full pair is used for every generation.
                    body_start=P;body_end=int(mem[0][0].shape[-2]);isolated={};shams={}
                    source_ranges={0:spans['B0'],1:spans['B1']}
                    for ix in (0,1):
                        start,end=source_ranges[ix]
                        other_start,other_end=source_ranges[1-ix]
                        mask_positions,sham_positions=disjoint_pair796(start,end,other_start,other_end)
                        gate796('EQUAL_MASK_COUNT_'+str(ix),len(mask_positions)==len(sham_positions))
                        gate796('SHAM_DISJOINT_'+str(ix),not(set(mask_positions)&set(sham_positions)))
                        masked=sham=None
                        try:
                            masked=mask796(mem,mask_positions)
                            isolated[ix]={view:probe796(masked,questions[view],None,0.0) for view in VIEWS}
                            del masked;masked=None;gc.collect();release()
                            sham=mask796(mem,sham_positions)
                            shams[ix]={view:probe796(sham,questions[view],None,0.0) for view in VIEWS}
                        finally:
                            del masked,sham;gc.collect();release()
                    for view in VIEWS:
                        q=questions[view];baseline=baselines[view]
                        directions={};ablation_stats={}
                        for ix in (0,1):
                            key='SOURCE'+str(ix)+'_MASK'
                            masked_probe=isolated[ix][view];sham_probe=shams[ix][view]
                            vec=sham_probe['state']-masked_probe['state']
                            sham_vec=baseline['state']-sham_probe['state']
                            gate796('SEED_NONZERO_'+key,bool(torch.isfinite(vec).all().item())
                                    and float(vec.norm().item())>1e-6)
                            directions[key]=vec/vec.norm().clamp_min(1e-6)
                            start,end=source_ranges[ix]
                            other_start,other_end=source_ranges[1-ix]
                            source_positions,sham_positions=disjoint_pair796(start,end,other_start,other_end)
                            overlap=len(set(source_positions).intersection(sham_positions))
                            gate796('STRICT_DISJOINT_'+str(ix),overlap==0)
                            ablation_stats[key]={
                                'masked_physical_source':order[ix],
                                'source_total_tokens':end-start,'mask_tokens':len(source_positions),'sham_tokens':len(sham_positions),
                                'sham_overlap_tokens':overlap,
                                'mask_vs_sham_direction_l2':float(vec.norm().item()),
                                'full_vs_masked_state_l2':float((baseline['state']-masked_probe['state']).norm().item()),
                                'full_vs_sham_state_l2':float(sham_vec.norm().item()),
                                'mask_vs_sham_state_l2':float((masked_probe['state']-sham_probe['state']).norm().item()),
                                'full_vs_masked_logit_l2':float((baseline['logits']-masked_probe['logits']).norm().item()),
                                'full_vs_sham_logit_l2':float((baseline['logits']-sham_probe['logits']).norm().item()),
                                'masked_first_token':masked_probe['first_token_id'],
                                'sham_first_token':sham_probe['first_token_id'],
                                'full_first_token':baseline['first_token_id'],
                                'mask_sham_direction_cosine':float(torch.nn.functional.cosine_similarity(
                                    vec[None],sham_vec[None]).item()) if float(sham_vec.norm().item())>1e-6 else None}
                        dose_scan={}
                        for key,seed in directions.items():
                            doses=[]
                            for gain_scan in (-1.0,-0.5,-0.25,0.25,0.5,1.0):
                                measurement=probe796(mem,q,seed,gain_scan)
                                cm=compare796(baseline,measurement)
                                doses.append({'gain':gain_scan,'baseline_margin':cm['baseline_margin'],
                                              'same_pair_margin_delta':cm['same_pair_margin_delta'],
                                              'first_token_changed':cm['first_token_changed'],
                                              'first_token_id':measurement['first_token_id'],
                                              'logit_l2_delta':cm['logit_l2_delta']})
                                del measurement
                            dose_scan[key]=doses
                        results=[];baseline_prediction=None
                        for arm in R['interventions']:
                            gain=float(arm['gain']);label=arm['label'];direction=arm['direction']
                            seed=None if direction=='NONE' else directions[direction]
                            measure=baseline if gain==0 else probe796(mem,q,seed,gain)
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
                            row.update(compare796(baseline,measure))
                            if label=='OFF':baseline_prediction=prediction
                            else:row['prediction_changed']=prediction!=baseline_prediction
                            results.append(row)
                            if gain:del measure
                        gate796('FIVE_ARMS_'+fid+'_'+scenario+'_'+order_name+'_'+view,len(results)==5)
                        expected=fam['new_team'] if view=='CURRENT' else fam['old_team']
                        for row in results:row['correct_OFFLINE']=row['prediction']==expected
                        emit796({'family':fid,'scenario_OFFLINE':scenario,'view_OFFLINE':view,
                                 'order':order_name,'cartridges':list(order),
                                 'length_matched_mask_probes':ablation_stats,'blind_dose_scan':dose_scan,
                                 'baseline_prediction':baseline_prediction,
                                 'expected_OFFLINE':expected,'arms':results})
                    del baselines,isolated,shams
                    gate796('KV_UNCHANGED_'+fid+'_'+scenario+'_'+order_name,
                            compare_seals(original_mem_seal,memory_seals(mem)))
                finally:
                    del mem;gc.collect();release()
            for cid,h in original_sha.items():
                gate796('SSD_SHA_UNCHANGED_'+cid,sha_file(CART_DIR/(cid+'.pt'))==h)
    gate796('TOTAL_CASES',len(R['rows'])==16,len(R['rows']))
    gate796('TOTAL_INTERVENTIONS',sum(len(row['arms']) for row in R['rows'])==80)
    gate796('FROZEN_WEIGHTS',sentinel()==before796)
    gate796('FINAL_MANIFEST',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    gate796('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
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
                  'interpretation':'Strictly disjoint equal-size partial KV masks; blinded signed dose-vs-margin audit, no correctness oracle, no autonomous controller.'}
    R['status']='COMPLETE_RESULTS_RECORDED';save796()
    log('TEST796_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save796()
    log('TEST796_FAILED',repr(e));log(R['traceback']);raise
finally:save796()
