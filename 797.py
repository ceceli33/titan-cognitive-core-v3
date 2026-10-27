# AKBASCORE SILICON HIPPOCAMPUS — TEST797
# DRA-INSPIRED DISJOINT MATCHED KV CONTROLS / BLIND PRESSURE DOSE AUDIT
# ONE COLAB CELL | FROZEN Qwen2.5-72B NF4 | ONE A100 80GB
# Proven TEST790 definitions and TEST779 native engine imported VERBATIM by Git blob.
# NO TRAINING, NO GOLD IN INTERVENTION, NO PERSISTENT HOOKS, NO GRADIO.
# This is an EXTERNAL CONTROLLED CAUSAL PROBE, NOT an autonomous closed loop.
import urllib.request,hashlib,ast,json,traceback,gc,math,time
from pathlib import Path

SOURCE797='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/790.py'
BLOB797='d7e4c4b21e9c3c46276845940a9621751b23897f'
def gitblob797(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with urllib.request.urlopen(urllib.request.Request(SOURCE797,headers={'User-Agent':'AKBASCORE-TEST797'}),timeout=180) as response:
    raw797=response.read()
assert gitblob797(raw797)==BLOB797,('FAIL_CLOSED_TEST790_SOURCE_CHANGED',gitblob797(raw797))
tree797=ast.parse(raw797.decode('utf-8'),filename='790.py')
cut797=next((i for i,n in enumerate(tree797.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:4])),None)
assert cut797 is not None and cut797==len(tree797.body)-1,'FAIL_CLOSED_TEST790_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree797.body[:cut797],type_ignores=[])),
             'TEST790_GPU_PROVEN_LOCKED_PRELUDE','exec'),globals())
# The TEST790 prelude runs only imports and definitions, not its GPU experiment.
assert blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')]
assert gitblob785(raw785)==BLOB
TEST='797';OUT=ROOT/'TEST797_results.json';LOG=ROOT/'TEST797.log';MANIFEST=ROOT/'TEST797_manifest.json'
LOG.write_text('',encoding='utf-8')
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'panel_sha256':PANEL_SHA,'locks':LOCKS,
   'source790_git_blob':BLOB797,'source789_git_blob':blob790(raw790),
   'source779_git_blob':gitblob785(raw785),'checks':[],'rows':[],
   'interventions':[{'label':'OFF','direction':'NONE','gain':0.0}],
   'limits':['Working TEST796 physical engine, masked/sham controls and SHA locks are unchanged.',
             'Two complementary source-minus-control contrasts are algebraically negatives: rank 1 is expected.',
             'This experiment tests rank and orthogonal residual explicitly; it does not manufacture independence.',
             'A source-specific residual must pass both numerical and independent-control criteria before pressure.',
             'No gold labels, correctness or source identity is used to choose a direction or dose.',
             'All candidate pressure doses are diagnostic probes only; no autonomous controller is claimed.',
             'Zero K/V masks are not actual deletion, and synthetic panel is not held-out generalization.']}

def save797():
    tmp=Path(str(OUT)+'.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT)
def gate797(name,ok,detail=None):
    R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});save797()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST797_GATE_'+name)
def emit797(row):
    R['rows'].append(row);save797();log('TEST797_ROW',json.dumps(row,ensure_ascii=False,default=str))

def probe797(mem,q,seed,gain):
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
        gate797('CUT3_STATE_DIM',state.numel()==H and bool(torch.isfinite(state).all().item()),state.numel())
        gate797('LOGITS_FINITE',bool(torch.isfinite(logits).all().item()))
        return {'state':state,'logits':logits,'state_sha256':hashlib.sha256(state.cpu().numpy().tobytes()).hexdigest(),
                'state_norm':float(state.norm().item()),'cut3_delta_l2':actual_delta,'cut3_steps':steps,
                'first_token_id':int(logits.argmax().item())}
    finally:
        del cache
        assert model.model.layers[CUT].forward==old_forward,'CUT3_FORWARD_NOT_RESTORED'

def compare797(base,arm):
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



def mask797(mem,positions):
    """Length-preserving physical-KV intervention, never mutates original tensor storage.
    Positions are absolute indices in the existing fused prefix. K/V at selected
    positions are set to zero in every layer. This is not true source removal.
    """
    n=int(mem[0][0].shape[-2]);pos=sorted(set(int(p) for p in positions))
    gate797('MASK_POSITIONS_VALID',bool(pos) and min(pos)>=P and max(pos)<n)
    result=[]
    for layer in mem:
        k,v=layer[0],layer[1]
        kc=k.clone();vc=v.clone()
        kc[...,pos,:]=0;vc[...,pos,:]=0
        # preserve any optional metadata without modifying it
        result.append((kc,vc,*layer[2:]))
    gate797('MASK_LENGTH_INVARIANT',len(result)==len(mem) and
            all(result[i][0].shape==mem[i][0].shape and result[i][1].shape==mem[i][1].shape
                for i in range(len(mem))))
    return result

def disjoint_pair797(source_start,source_end,other_start,other_end):
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
    log('='*112);log('TEST797 — SOURCE DIRECTION RANK / ORTHOGONAL RESIDUAL / ABSTENTION')
    gate797('TEST790_EXACT_BLOB',gitblob797(raw797)==BLOB797)
    gate797('TEST789_EXACT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate797('TEST779_EXACT_BLOB',gitblob785(raw785)==BLOB)
    gate797('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    gate797('MANIFEST_CONTRACT',R['panel_sha256']==PANEL_SHA and R['locks']==LOCKS)
    persist_manifest()
    gate797('MANIFEST_PREFLIGHT',json.loads(MANIFEST.read_text())['panel_sha256']==PANEL_SHA)
    gate797('PROBE_SYMBOLS',all(callable(globals().get(k)) for k in
       ('Cut3Diagnostic','build_fusion','free_generate','memory_seals','compare_seals','physical_commit')))
    gate797('BASELINE_ONLY',len(R['interventions'])==1 and R['interventions'][0]['gain']==0.0)
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    gate797('GPU_VRAM',free>=40*2**30)
    model_setup();before797=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate797('PHYSICAL_20_CARTRIDGES',len(entries)==20,len(entries))
    families=list(FAMILIES)
    # Same TEST790 conflict panel; no changes to synthetic facts or labels.
    extra797={}
    for ix,fam in enumerate(families):
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        decoy=families[(ix+1)%len(families)]['new_team']
        extra797[fid+'_X1']=(f'Authoritative CURRENT record REVISION 1: {work} '
                                f'collaborates_with {decoy}. Supersedes revision 0.')
        extra797[fid+'_X0']=(f'Historical record REVISION 0 (superseded): {work} '
                                f'collaborates_with {decoy}. Valid at revision 0 only.')
    for cid,body in sorted(extra797.items()):physical_commit(cid,body)
    gate797('PHYSICAL_28_CARTRIDGES',len(entries)==28,len(entries))
    gate797('MANIFEST_AFTER_28',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    # Two families x baseline/conflict x current/historical x forward/reverse = 16 baseline generations.
    # Pressure is diagnostic only; no source-selection claims.
    for fam in families[:2]:
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        for scenario,pair in [('BASELINE',[fid+'_B0',fid+'_B1']),
                              ('SAME_REV_CONFLICT',[fid+'_B1',fid+'_X1'])]:
            original_sha={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in pair}
            for order_name,order in [('FORWARD',pair),('REVERSE',list(reversed(pair)))]:
                mem=None
                try:
                    mem,active,_,_=build_fusion(order,'TEST797_'+fid+'_'+scenario+'_'+order_name,True)
                    gate797('NATIVE_80_'+fid+'_'+scenario+'_'+order_name,len(mem)==80)
                    gate797('PAIR_ORDER_'+fid+'_'+scenario+'_'+order_name,list(active)==order)
                    spans=spans790(order,mem)
                    original_mem_seal=memory_seals(mem)
                    questions={view:CUE[view].format(work=work) for view in VIEWS}
                    baselines={view:probe797(mem,questions[view],None,0.0) for view in VIEWS}
                    # Controlled same-length perturbations of the already fused physical KV.
                    # Each mask is transient, and the untouched full pair is used for every generation.
                    body_start=P;body_end=int(mem[0][0].shape[-2]);isolated={};shams={}
                    source_ranges={0:spans['B0'],1:spans['B1']}
                    for ix in (0,1):
                        start,end=source_ranges[ix]
                        other_start,other_end=source_ranges[1-ix]
                        mask_positions,sham_positions=disjoint_pair797(start,end,other_start,other_end)
                        gate797('EQUAL_MASK_COUNT_'+str(ix),len(mask_positions)==len(sham_positions))
                        gate797('SHAM_DISJOINT_'+str(ix),not(set(mask_positions)&set(sham_positions)))
                        masked=sham=None
                        try:
                            masked=mask797(mem,mask_positions)
                            isolated[ix]={view:probe797(masked,questions[view],None,0.0) for view in VIEWS}
                            del masked;masked=None;gc.collect();release()
                            sham=mask797(mem,sham_positions)
                            shams[ix]={view:probe797(sham,questions[view],None,0.0) for view in VIEWS}
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
                            gate797('SEED_NONZERO_'+key,bool(torch.isfinite(vec).all().item())
                                    and float(vec.norm().item())>1e-6)
                            directions[key]=vec/vec.norm().clamp_min(1e-6)
                            start,end=source_ranges[ix]
                            other_start,other_end=source_ranges[1-ix]
                            source_positions,sham_positions=disjoint_pair797(start,end,other_start,other_end)
                            overlap=len(set(source_positions).intersection(sham_positions))
                            gate797('STRICT_DISJOINT_'+str(ix),overlap==0)
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
                        # The two source contrasts are complementary masks on the SAME two regions.
                        # Verify the algebraic degeneracy rather than calling these independent sources.
                        d0=directions['SOURCE0_MASK'].float()
                        d1=directions['SOURCE1_MASK'].float()
                        cosine=float(torch.dot(d0,d1).item())
                        residual=d1-torch.dot(d1,d0)*d0
                        residual_norm=float(residual.norm().item())
                        raw0=shams[0][view]['state']-isolated[0][view]['state']
                        raw1=shams[1][view]['state']-isolated[1][view]['state']
                        antisymmetry_error=float((raw0+raw1).norm().item())
                        raw_scale=max(float(raw0.norm().item()),float(raw1.norm().item()),1e-9)
                        relative_antisymmetry_error=antisymmetry_error/raw_scale
                        # BF16/FP32 numerical tolerance is an audit threshold, NOT a truth threshold.
                        degenerate=abs(cosine)>0.999 or residual_norm<0.045 or relative_antisymmetry_error<0.01
                        rank=1 if degenerate else 2
                        # Even if a numerical residual appears, the second direction comes from
                        # the exact reversed control and cannot be independently source-validated.
                        independent_control_available=False
                        controller_action='ABSTAIN_NO_INDEPENDENT_SOURCE_DIRECTION'
                        gate797('NO_FALSE_INDEPENDENCE_'+fid+'_'+scenario+'_'+order_name+'_'+view,
                                not independent_control_available)
                        # Diagnostic-only signed pressure scan along the sole observable axis.
                        # It cannot select a source; no answer oracle or dose optimization.
                        dose_scan=[]
                        for gain_scan in (-1.0,-0.5,-0.25,0.25,0.5,1.0):
                            measurement=probe797(mem,q,d0,gain_scan)
                            cm=compare797(baseline,measurement)
                            dose_scan.append({'gain':gain_scan,
                                              'same_pair_margin_delta':cm['same_pair_margin_delta'],
                                              'baseline_margin':cm['baseline_margin'],
                                              'first_token_changed':cm['first_token_changed'],
                                              'first_token_id':measurement['first_token_id'],
                                              'logit_l2_delta':cm['logit_l2_delta']})
                            del measurement
                        output=free_generate(mem,q,seed=None,gain=0.0,
                                             max_new=MAX_TOKENS,spans=spans)
                        prediction=parse789(output['raw'])
                        expected=fam['new_team'] if view=='CURRENT' else fam['old_team']
                        emit797({'family':fid,'scenario_OFFLINE':scenario,'view_OFFLINE':view,
                                 'order':order_name,'cartridges':list(order),
                                 'mask_controls':ablation_stats,
                                 'source_direction_cosine':cosine,
                                 'orthogonal_residual_norm':residual_norm,
                                 'relative_antisymmetry_error':relative_antisymmetry_error,
                                 'measured_direction_rank':rank,
                                 'independent_control_available':independent_control_available,
                                 'controller_action':controller_action,
                                 'blind_dose_scan_single_axis':dose_scan,
                                 'baseline_prediction':prediction,
                                 'expected_OFFLINE':expected,
                                 'baseline_correct_OFFLINE':prediction==expected,
                                 'arms':[{'arm':'OFF','prediction':prediction,
                                          'correct_OFFLINE':prediction==expected,
                                          'first_token_id':baseline['first_token_id']}]})
                    del baselines,isolated,shams
                    gate797('KV_UNCHANGED_'+fid+'_'+scenario+'_'+order_name,
                            compare_seals(original_mem_seal,memory_seals(mem)))
                finally:
                    del mem;gc.collect();release()
            for cid,h in original_sha.items():
                gate797('SSD_SHA_UNCHANGED_'+cid,sha_file(CART_DIR/(cid+'.pt'))==h)
    gate797('TOTAL_CASES',len(R['rows'])==16,len(R['rows']))
    gate797('BASELINE_GENERATIONS',sum(len(row['arms']) for row in R['rows'])==16)
    gate797('ALL_ABSTAIN',all(row['controller_action']=='ABSTAIN_NO_INDEPENDENT_SOURCE_DIRECTION'
                             for row in R['rows']))
    gate797('FROZEN_WEIGHTS',sentinel()==before797)
    gate797('FINAL_MANIFEST',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    gate797('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    R['summary']={'cases':len(R['rows']),'generation_runs':16,
                  'source_direction_cosines':[row['source_direction_cosine'] for row in R['rows']],
                  'direction_rank_counts':{'rank1':sum(row['measured_direction_rank']==1 for row in R['rows']),
                                           'rank2':sum(row['measured_direction_rank']==2 for row in R['rows'])},
                  'abstentions':sum(row['controller_action'].startswith('ABSTAIN') for row in R['rows']),
                  'baseline_correct':sum(row['baseline_correct_OFFLINE'] for row in R['rows']),
                  'interpretation':'Independent source directions are not identifiable from complementary two-mask contrasts; abstention is a safety decision, not autonomous reasoning.'}
    R['status']='COMPLETE_RESULTS_RECORDED';save797()
    log('TEST797_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save797()
    log('TEST797_FAILED',repr(e));log(R['traceback']);raise
finally:save797()
