# AKBASCORE SILICON HIPPOCAMPUS — TEST799
# DRA-INSPIRED SOURCE-IDENTITY / ORDER-EQUIVARIANCE / POSITION CONFOUND AUDIT
# ONE COLAB CELL | FROZEN Qwen2.5-72B NF4 | ONE A100 80GB
# Proven TEST790 definitions and TEST779 native engine imported VERBATIM by Git blob.
# NO TRAINING, NO GOLD IN INTERVENTION, NO PERSISTENT HOOKS, NO GRADIO.
# This is an EXTERNAL CONTROLLED CAUSAL PROBE, NOT an autonomous closed loop.
import urllib.request,hashlib,ast,json,traceback,gc,math,time
from pathlib import Path

SOURCE799='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/790.py'
BLOB799='d7e4c4b21e9c3c46276845940a9621751b23897f'
def gitblob799(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with urllib.request.urlopen(urllib.request.Request(SOURCE799,headers={'User-Agent':'AKBASCORE-TEST799'}),timeout=180) as response:
    raw799=response.read()
assert gitblob799(raw799)==BLOB799,('FAIL_CLOSED_TEST790_SOURCE_CHANGED',gitblob799(raw799))
tree799=ast.parse(raw799.decode('utf-8'),filename='790.py')
cut799=next((i for i,n in enumerate(tree799.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:4])),None)
assert cut799 is not None and cut799==len(tree799.body)-1,'FAIL_CLOSED_TEST790_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree799.body[:cut799],type_ignores=[])),
             'TEST790_GPU_PROVEN_LOCKED_PRELUDE','exec'),globals())
# The TEST790 prelude runs only imports and definitions, not its GPU experiment.
assert blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')]
assert gitblob785(raw785)==BLOB
TEST='799';OUT=ROOT/'TEST799_results.json';LOG=ROOT/'TEST799.log';MANIFEST=ROOT/'TEST799_manifest.json'
LOG.write_text('',encoding='utf-8')
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'panel_sha256':PANEL_SHA,'locks':LOCKS,
   'source790_git_blob':BLOB799,'source789_git_blob':blob790(raw790),
   'source779_git_blob':gitblob785(raw785),'checks':[],'rows':[],
   'interventions':[{'label':'OFF','direction':'NONE','gain':0.0}],
   'limits':['TEST797 engine and sealed physical panel are reused without changing model weights.',
             'Both source effects are computed against the SAME unmasked full-pair baseline.',
             'The source-specific masks are nonoverlapping, but zeroing KV is not actual source deletion.',
             'A jointly masked factorial condition audits nonlinear interaction and common-reference geometry.',
             'A numerically independent direction is not evidence of semantic source identification.',
             'Order swaps compare the same physical cartridge IDs across positions; position and source are not causally separated by this observational comparison.',
             'Source identity transport is compared against positional alignment with matched forward/reverse physical pairs.',
             'No ground-truth labels or expected answers are used to choose directions or pressure.',
             'Pressure is diagnostic only, not autonomous reasoning or a deployed controller.']}


def save799():
    tmp=Path(str(OUT)+'.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT)
def gate799(name,ok,detail=None):
    R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});save799()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST799_GATE_'+name)
def emit799(row):
    R['rows'].append(row);save799();log('TEST799_ROW',json.dumps(row,ensure_ascii=False,default=str))

def probe799(mem,q,seed,gain):
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
        gate799('CUT3_STATE_DIM',state.numel()==H and bool(torch.isfinite(state).all().item()),state.numel())
        gate799('LOGITS_FINITE',bool(torch.isfinite(logits).all().item()))
        return {'state':state,'logits':logits,'state_sha256':hashlib.sha256(state.cpu().numpy().tobytes()).hexdigest(),
                'state_norm':float(state.norm().item()),'cut3_delta_l2':actual_delta,'cut3_steps':steps,
                'first_token_id':int(logits.argmax().item())}
    finally:
        del cache
        assert model.model.layers[CUT].forward==old_forward,'CUT3_FORWARD_NOT_RESTORED'

def compare799(base,arm):
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



def mask799(mem,positions):
    """Length-preserving physical-KV intervention, never mutates original tensor storage.
    Positions are absolute indices in the existing fused prefix. K/V at selected
    positions are set to zero in every layer. This is not true source removal.
    """
    n=int(mem[0][0].shape[-2]);pos=sorted(set(int(p) for p in positions))
    gate799('MASK_POSITIONS_VALID',bool(pos) and min(pos)>=P and max(pos)<n)
    result=[]
    for layer in mem:
        k,v=layer[0],layer[1]
        kc=k.clone();vc=v.clone()
        kc[...,pos,:]=0;vc[...,pos,:]=0
        # preserve any optional metadata without modifying it
        result.append((kc,vc,*layer[2:]))
    gate799('MASK_LENGTH_INVARIANT',len(result)==len(mem) and
            all(result[i][0].shape==mem[i][0].shape and result[i][1].shape==mem[i][1].shape
                for i in range(len(mem))))
    return result

def disjoint_pair799(source_start,source_end,other_start,other_end):
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
    log('='*112);log('TEST799 — SOURCE-IDENTITY / ORDER-EQUIVARIANCE / POSITION CONFOUND AUDIT')
    gate799('TEST790_EXACT_BLOB',gitblob799(raw799)==BLOB799)
    gate799('TEST789_EXACT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate799('TEST779_EXACT_BLOB',gitblob785(raw785)==BLOB)
    gate799('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    gate799('MANIFEST_CONTRACT',R['panel_sha256']==PANEL_SHA and R['locks']==LOCKS)
    persist_manifest()
    gate799('MANIFEST_PREFLIGHT',json.loads(MANIFEST.read_text())['panel_sha256']==PANEL_SHA)
    gate799('PROBE_SYMBOLS',all(callable(globals().get(k)) for k in
       ('Cut3Diagnostic','build_fusion','free_generate','memory_seals','compare_seals','physical_commit')))
    gate799('BASELINE_ONLY',len(R['interventions'])==1 and R['interventions'][0]['gain']==0.0)
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    gate799('GPU_VRAM',free>=40*2**30)
    model_setup();before799=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate799('PHYSICAL_20_CARTRIDGES',len(entries)==20,len(entries))
    families=list(FAMILIES)
    # Same TEST790 conflict panel; no changes to synthetic facts or labels.
    extra799={}
    for ix,fam in enumerate(families):
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        decoy=families[(ix+1)%len(families)]['new_team']
        extra799[fid+'_X1']=(f'Authoritative CURRENT record REVISION 1: {work} '
                                f'collaborates_with {decoy}. Supersedes revision 0.')
        extra799[fid+'_X0']=(f'Historical record REVISION 0 (superseded): {work} '
                                f'collaborates_with {decoy}. Valid at revision 0 only.')
    for cid,body in sorted(extra799.items()):physical_commit(cid,body)
    gate799('PHYSICAL_28_CARTRIDGES',len(entries)==28,len(entries))
    gate799('MANIFEST_AFTER_28',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    # Two families x baseline/conflict x current/historical x forward/reverse = 16 baseline generations.
    # Pressure is diagnostic only; no source-selection claims.
    transport799=[]
    for fam in families[:2]:
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        for scenario,pair in [('BASELINE',[fid+'_B0',fid+'_B1']),
                              ('SAME_REV_CONFLICT',[fid+'_B1',fid+'_X1'])]:
            original_sha={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in pair}
            by_order799={}
            for order_name,order in [('FORWARD',pair),('REVERSE',list(reversed(pair)))]:
                mem=None
                try:
                    mem,active,_,_=build_fusion(order,'TEST799_'+fid+'_'+scenario+'_'+order_name,True)
                    gate799('NATIVE_80_'+fid+'_'+scenario+'_'+order_name,len(mem)==80)
                    gate799('PAIR_ORDER_'+fid+'_'+scenario+'_'+order_name,list(active)==order)
                    spans=spans790(order,mem)
                    original_mem_seal=memory_seals(mem)
                    questions={view:CUE[view].format(work=work) for view in VIEWS}
                    baselines={view:probe799(mem,questions[view],None,0.0) for view in VIEWS}
                    # Common reference: the SAME untouched full fused pair for both effects.
                    # This avoids TEST797's algebraic complement subtraction.
                    isolated={}; joint={}
                    source_ranges={0:spans['B0'],1:spans['B1']}
                    source_positions={ix:list(range(*source_ranges[ix])) for ix in (0,1)}
                    gate799('SOURCE_SPANS_DISJOINT',not(set(source_positions[0]) & set(source_positions[1])))
                    for ix in (0,1):
                        masked=None
                        try:
                            masked=mask799(mem,source_positions[ix])
                            isolated[ix]={view:probe799(masked,questions[view],None,0.0) for view in VIEWS}
                        finally:
                            del masked;gc.collect();release()
                    joint_mem=None
                    try:
                        joint_mem=mask799(mem,source_positions[0]+source_positions[1])
                        joint={view:probe799(joint_mem,questions[view],None,0.0) for view in VIEWS}
                    finally:
                        del joint_mem;gc.collect();release()
                    by_order799[order_name]={}
                    for view in VIEWS:
                        q=questions[view];baseline=baselines[view]
                        full_state=baseline['state']
                        # Two separate source-vs-full vectors: not forced to be negatives.
                        raw=[full_state-isolated[ix][view]['state'] for ix in (0,1)]
                        norms=[float(x.norm().item()) for x in raw]
                        gate799('FINITE_NONZERO_EFFECTS_'+fid+'_'+scenario+'_'+order_name+'_'+view,
                                all(bool(torch.isfinite(x).all().item()) for x in raw) and min(norms)>1e-6)
                        d0=raw[0]/raw[0].norm().clamp_min(1e-6)
                        d1=raw[1]/raw[1].norm().clamp_min(1e-6)
                        cosine=float(torch.dot(d0,d1).item())
                        residual=d1-torch.dot(d1,d0)*d0
                        residual_norm=float(residual.norm().item())
                        # Preserve raw, common-reference effects for cross-order physical-ID alignment.
                        by_order799[order_name][view]={'physical':{order[ix]:raw[ix].detach().cpu().clone() for ix in (0,1)},
                                                       'position':{ix:raw[ix].detach().cpu().clone() for ix in (0,1)},
                                                       'baseline':full_state.detach().cpu().clone()}
                        # Factorial interaction: full - mask0 - mask1 + mask_both.
                        interaction=full_state-isolated[0][view]['state']-isolated[1][view]['state']+joint[view]['state']
                        interaction_norm=float(interaction.norm().item())
                        relative_interaction=interaction_norm/max(norms[0],norms[1],1e-9)
                        rank=2 if abs(cosine)<0.995 and residual_norm>0.10 else 1
                        # Independent geometrical directions are diagnostic, not a validated source selector.
                        action='ABSTAIN_NO_GEOMETRIC_INDEPENDENCE' if rank==1 else 'ABSTAIN_NO_VALIDATED_SOURCE_SELECTOR'
                        # Test one direction and the orthogonal residual (only if measurable).
                        scan={}
                        for label,axis in [('SOURCE0_FULL',d0),('SOURCE1_ORTHOGONAL',
                                           residual/residual.norm().clamp_min(1e-6) if rank==2 else None)]:
                            if axis is None:
                                scan[label]=[];continue
                            measurements=[]
                            for gain_scan in (-1.0,-0.5,-0.25,0.25,0.5,1.0):
                                measurement=probe799(mem,q,axis,gain_scan)
                                cm=compare799(baseline,measurement)
                                measurements.append({'gain':gain_scan,
                                    'same_pair_margin_delta':cm['same_pair_margin_delta'],
                                    'baseline_margin':cm['baseline_margin'],
                                    'first_token_changed':cm['first_token_changed'],
                                    'first_token_id':measurement['first_token_id'],
                                    'logit_l2_delta':cm['logit_l2_delta']})
                                del measurement
                            scan[label]=measurements
                        output=free_generate(mem,q,seed=None,gain=0.0,
                                             max_new=MAX_TOKENS,spans=spans)
                        prediction=parse789(output['raw'])
                        expected=fam['new_team'] if view=='CURRENT' else fam['old_team']
                        emit799({'family':fid,'scenario_OFFLINE':scenario,'view_OFFLINE':view,
                                 'order':order_name,'cartridges':list(order),
                                 'reference':'FULL_UNMASKED_FUSED_PAIR',
                                 'source_mask_tokens':[len(source_positions[0]),len(source_positions[1])],
                                 'source_effect_l2':norms,
                                 'source_direction_cosine':cosine,
                                 'orthogonal_residual_norm':residual_norm,
                                 'measured_direction_rank':rank,
                                 'factorial_interaction_l2':interaction_norm,
                                 'relative_factorial_interaction':relative_interaction,
                                 'full_vs_mask0_logit_l2':float((baseline['logits']-isolated[0][view]['logits']).norm().item()),
                                 'full_vs_mask1_logit_l2':float((baseline['logits']-isolated[1][view]['logits']).norm().item()),
                                 'full_vs_maskboth_logit_l2':float((baseline['logits']-joint[view]['logits']).norm().item()),
                                 'controller_action':action,
                                 'blind_dose_scans':scan,
                                 'baseline_prediction':prediction,
                                 'expected_OFFLINE':expected,
                                 'baseline_correct_OFFLINE':prediction==expected,
                                 'arms':[{'arm':'OFF','prediction':prediction,
                                          'correct_OFFLINE':prediction==expected,
                                          'first_token_id':baseline['first_token_id']}]})
                    del baselines,isolated,joint
                    gate799('KV_UNCHANGED_'+fid+'_'+scenario+'_'+order_name,
                            compare_seals(original_mem_seal,memory_seals(mem)))
                finally:
                    del mem;gc.collect();release()
            # Cross-order audit: identity-aligned effects versus position-aligned effects.
            # All comparisons use the same sealed physical cartridges; no expected answer enters this analysis.
            for view in VIEWS:
                forward=by_order799['FORWARD'][view];reverse=by_order799['REVERSE'][view]
                def cos799(a,b):
                    a=a.float();b=b.float()
                    return float(torch.dot(a,b).item()/(max(float(a.norm().item())*float(b.norm().item()),1e-12)))
                def dist799(a,b):return float((a.float()-b.float()).norm().item())
                identity_cos={cid:cos799(forward['physical'][cid],reverse['physical'][cid]) for cid in pair}
                identity_dist={cid:dist799(forward['physical'][cid],reverse['physical'][cid]) for cid in pair}
                position_cos={str(ix):cos799(forward['position'][ix],reverse['position'][ix]) for ix in (0,1)}
                position_dist={str(ix):dist799(forward['position'][ix],reverse['position'][ix]) for ix in (0,1)}
                # Compare two possible correspondences, using the same two forward and reverse vectors.
                same_id_score=sum(identity_cos.values())/2.0
                same_pos_score=sum(position_cos.values())/2.0
                # Counterfactual swap is not available; this is an observational order-transport test.
                transport799.append({'family':fid,'scenario':scenario,'view':view,
                    'physical_ids':list(pair),'same_id_cosines':identity_cos,
                    'same_position_cosines':position_cos,
                    'same_id_l2':identity_dist,'same_position_l2':position_dist,
                    'same_id_mean_cosine':same_id_score,'same_position_mean_cosine':same_pos_score,
                    'identity_minus_position_cosine':same_id_score-same_pos_score,
                    'forward_reverse_baseline_state_l2':dist799(forward['baseline'],reverse['baseline']),
                    'interpretation_limit':'Observational swap: position, order, and context are entangled.'})
                log('TEST799_TRANSPORT',json.dumps(transport799[-1],ensure_ascii=False))
            del by_order799
            for cid,h in original_sha.items():
                gate799('SSD_SHA_UNCHANGED_'+cid,sha_file(CART_DIR/(cid+'.pt'))==h)
    gate799('TOTAL_CASES',len(R['rows'])==16,len(R['rows']))
    gate799('TRANSPORT_PAIRS',len(transport799)==8,len(transport799))
    gate799('TRANSPORT_FINITE',all(math.isfinite(t['identity_minus_position_cosine']) for t in transport799))
    gate799('BASELINE_GENERATIONS',sum(len(row['arms']) for row in R['rows'])==16)
    gate799('ALL_ABSTAIN',all(row['controller_action'].startswith('ABSTAIN') for row in R['rows']))
    gate799('FROZEN_WEIGHTS',sentinel()==before799)
    gate799('FINAL_MANIFEST',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    gate799('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    R['transport_audit']=transport799
    R['summary']={'cases':len(R['rows']),'generation_runs':16,
                  'transport_pairs':len(transport799),
                  'mean_identity_minus_position_cosine':sum(t['identity_minus_position_cosine'] for t in transport799)/len(transport799),
                  'identity_preferred_pairs':sum(t['identity_minus_position_cosine']>0 for t in transport799),
                  'source_direction_cosines':[row['source_direction_cosine'] for row in R['rows']],
                  'direction_rank_counts':{'rank1':sum(row['measured_direction_rank']==1 for row in R['rows']),
                                           'rank2':sum(row['measured_direction_rank']==2 for row in R['rows'])},
                  'abstentions':sum(row['controller_action'].startswith('ABSTAIN') for row in R['rows']),
                  'mean_factorial_interaction_l2':sum(row['factorial_interaction_l2'] for row in R['rows'])/len(R['rows']),
                  'baseline_correct':sum(row['baseline_correct_OFFLINE'] for row in R['rows']),
                  'interpretation':'Matched physical cartridge source effects are compared across forward/reverse order, against positional alignment. This is an observational confound audit, not proof of semantic source tracking or autonomous reasoning.'}
    R['status']='COMPLETE_RESULTS_RECORDED';save799()
    log('TEST799_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save799()
    log('TEST799_FAILED',repr(e));log(R['traceback']);raise
finally:save799()
