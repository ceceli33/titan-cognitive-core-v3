# AKBASCORE SILICON HIPPOCAMPUS — TEST800
# FIXED-SLOT CONTENT SWAP / POSITION CROSSOVER / KV MASK CONTROLS
# ONE COLAB CELL | FROZEN Qwen2.5-72B NF4 | ONE A100 80GB
# Proven TEST790 definitions and TEST779 native engine imported VERBATIM by Git blob.
# NO TRAINING, NO GOLD IN INTERVENTION, NO PERSISTENT HOOKS, NO GRADIO.
# This is an EXTERNAL CONTROLLED CAUSAL PROBE, NOT an autonomous closed loop.
import urllib.request,hashlib,ast,json,traceback,gc,math,time
from pathlib import Path

SOURCE800='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/790.py'
BLOB800='d7e4c4b21e9c3c46276845940a9621751b23897f'
def gitblob800(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with urllib.request.urlopen(urllib.request.Request(SOURCE800,headers={'User-Agent':'AKBASCORE-TEST800'}),timeout=180) as response:
    raw800=response.read()
assert gitblob800(raw800)==BLOB800,('FAIL_CLOSED_TEST790_SOURCE_CHANGED',gitblob800(raw800))
tree800=ast.parse(raw800.decode('utf-8'),filename='790.py')
cut800=next((i for i,n in enumerate(tree800.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:4])),None)
assert cut800 is not None and cut800==len(tree800.body)-1,'FAIL_CLOSED_TEST790_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree800.body[:cut800],type_ignores=[])),
             'TEST790_GPU_PROVEN_LOCKED_PRELUDE','exec'),globals())
# The TEST790 prelude runs only imports and definitions, not its GPU experiment.
assert blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')]
assert gitblob785(raw785)==BLOB
TEST='800';OUT=ROOT/'TEST800_results.json';LOG=ROOT/'TEST800.log';MANIFEST=ROOT/'TEST800_manifest.json'
LOG.write_text('',encoding='utf-8')
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'panel_sha256':PANEL_SHA,'locks':LOCKS,
   'source790_git_blob':BLOB800,'source789_git_blob':blob790(raw790),
   'source779_git_blob':gitblob785(raw785),'checks':[],'rows':[],
   'interventions':[{'label':'OFF','direction':'NONE','gain':0.0}],
   'limits':['Physical B1/X1 candidate cartridges are crossed with slot 0/1 against fixed B0 anchor.',
             'All comparisons are direct native fused-KV forward passes; no textual source replay.',
             'Same-slot content contrasts are length-matched ONLY when candidate token counts agree.',
             'Unequal-length contrasts are reported separately as confounded; never counted as clean.',
             'Position crossover also changes relative position and context; not fully isolated causal position.',
             'KV zero-mask changes attention behavior and is not equivalent to physical source deletion.',
             'No answer oracle is used for selection; no autonomous controller is claimed.']}


def save800():
    tmp=Path(str(OUT)+'.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT)
def gate800(name,ok,detail=None):
    R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});save800()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST800_GATE_'+name)
def emit800(row):
    R['rows'].append(row);save800();log('TEST800_ROW',json.dumps(row,ensure_ascii=False,default=str))

def probe800(mem,q,seed,gain):
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
        gate800('CUT3_STATE_DIM',state.numel()==H and bool(torch.isfinite(state).all().item()),state.numel())
        gate800('LOGITS_FINITE',bool(torch.isfinite(logits).all().item()))
        return {'state':state,'logits':logits,'state_sha256':hashlib.sha256(state.cpu().numpy().tobytes()).hexdigest(),
                'state_norm':float(state.norm().item()),'cut3_delta_l2':actual_delta,'cut3_steps':steps,
                'first_token_id':int(logits.argmax().item())}
    finally:
        del cache
        assert model.model.layers[CUT].forward==old_forward,'CUT3_FORWARD_NOT_RESTORED'

def compare800(base,arm):
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



def mask800(mem,positions):
    """Length-preserving physical-KV intervention, never mutates original tensor storage.
    Positions are absolute indices in the existing fused prefix. K/V at selected
    positions are set to zero in every layer. This is not true source removal.
    """
    n=int(mem[0][0].shape[-2]);pos=sorted(set(int(p) for p in positions))
    gate800('MASK_POSITIONS_VALID',bool(pos) and min(pos)>=P and max(pos)<n)
    result=[]
    for layer in mem:
        k,v=layer[0],layer[1]
        kc=k.clone();vc=v.clone()
        kc[...,pos,:]=0;vc[...,pos,:]=0
        # preserve any optional metadata without modifying it
        result.append((kc,vc,*layer[2:]))
    gate800('MASK_LENGTH_INVARIANT',len(result)==len(mem) and
            all(result[i][0].shape==mem[i][0].shape and result[i][1].shape==mem[i][1].shape
                for i in range(len(mem))))
    return result

def disjoint_pair800(source_start,source_end,other_start,other_end):
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
    log('='*112);log('TEST800 — FIXED-SLOT CONTENT SWAP / POSITION CROSSOVER / KV MASK CONTROL')
    gate800('TEST790_EXACT_BLOB',gitblob800(raw800)==BLOB800)
    gate800('TEST789_EXACT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate800('TEST779_EXACT_BLOB',gitblob785(raw785)==BLOB)
    gate800('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    gate800('MANIFEST_CONTRACT',R['panel_sha256']==PANEL_SHA and R['locks']==LOCKS)
    persist_manifest()
    gate800('MANIFEST_PREFLIGHT',json.loads(MANIFEST.read_text())['panel_sha256']==PANEL_SHA)
    gate800('PROBE_SYMBOLS',all(callable(globals().get(k)) for k in
       ('Cut3Diagnostic','build_fusion','free_generate','memory_seals','compare_seals','physical_commit')))
    gate800('BASELINE_ONLY',len(R['interventions'])==1 and R['interventions'][0]['gain']==0.0)
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    gate800('GPU_VRAM',free>=40*2**30)
    model_setup();before800=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate800('PHYSICAL_20_CARTRIDGES',len(entries)==20,len(entries))
    families=list(FAMILIES)
    extra800={}
    for ix,fam in enumerate(families):
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        decoy=families[(ix+1)%len(families)]['new_team']
        extra800[fid+'_X1']=(f'Authoritative CURRENT record REVISION 1: {work} '
                                f'collaborates_with {decoy}. Supersedes revision 0.')
        extra800[fid+'_X0']=(f'Historical record REVISION 0 (superseded): {work} '
                                f'collaborates_with {decoy}. Valid at revision 0 only.')
    for cid,body in sorted(extra800.items()):physical_commit(cid,body)
    gate800('PHYSICAL_28_CARTRIDGES',len(entries)==28,len(entries))
    gate800('MANIFEST_AFTER_28',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    # 2 families x 2 candidate contents x 2 candidate slots x 2 question views = 16 baselines.
    # Each condition uses its own native fused physical-KV pair; no fabricated KV replacement.
    paired={}; comparisons=[]
    for fam in families[:2]:
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        anchor=fid+'_B0';candidates=[fid+'_B1',fid+'_X1']
        original_sha={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in [anchor]+candidates}
        for candidate in candidates:
            for slot in (0,1):
                order=[candidate,anchor] if slot==0 else [anchor,candidate]
                mem=None
                try:
                    mem,active,_,_=build_fusion(order,'TEST800_'+fid+'_'+candidate+'_'+str(slot),True)
                    gate800('NATIVE_80_'+fid+'_'+candidate+'_'+str(slot),len(mem)==80)
                    gate800('PAIR_ORDER_'+fid+'_'+candidate+'_'+str(slot),list(active)==order)
                    spans=spans790(order,mem)
                    source_ranges={0:spans['B0'],1:spans['B1']}
                    candidate_positions=list(range(*source_ranges[slot]))
                    anchor_positions=list(range(*source_ranges[1-slot]))
                    gate800('DISJOINT_SOURCE_SPANS',not(set(candidate_positions)&set(anchor_positions)))
                    seal=memory_seals(mem)
                    for view in VIEWS:
                        q=CUE[view].format(work=work)
                        full=probe800(mem,q,None,0.0)
                        # Identical-length zero-mask controls within this SAME fused memory.
                        masked_candidate=mask800(mem,candidate_positions)
                        try: mc=probe800(masked_candidate,q,None,0.0)
                        finally: del masked_candidate;gc.collect();release()
                        masked_anchor=mask800(mem,anchor_positions)
                        try: ma=probe800(masked_anchor,q,None,0.0)
                        finally: del masked_anchor;gc.collect();release()
                        # A full generation is retained only for the untouched OFF baseline.
                        output=free_generate(mem,q,seed=None,gain=0.0,max_new=MAX_TOKENS,spans=spans)
                        prediction=parse789(output['raw'])
                        expected=fam['new_team'] if view=='CURRENT' else fam['old_team']
                        key=(fid,candidate,slot,view)
                        paired[key]={'state':full['state'].detach().cpu().clone(),
                                     'logits':full['logits'].detach().cpu().clone(),
                                     'candidate_effect':(full['state']-mc['state']).detach().cpu().clone(),
                                     'anchor_effect':(full['state']-ma['state']).detach().cpu().clone(),
                                     'candidate_tokens':len(candidate_positions),
                                     'anchor_tokens':len(anchor_positions),
                                     'first_token_id':full['first_token_id']}
                        emit800({'family':fid,'candidate_id':candidate,'anchor_id':anchor,
                                 'candidate_slot':slot,'order':list(order),'view_OFFLINE':view,
                                 'candidate_tokens':len(candidate_positions),'anchor_tokens':len(anchor_positions),
                                 'candidate_mask_state_l2':float((full['state']-mc['state']).norm().item()),
                                 'anchor_mask_state_l2':float((full['state']-ma['state']).norm().item()),
                                 'candidate_mask_logit_l2':float((full['logits']-mc['logits']).norm().item()),
                                 'anchor_mask_logit_l2':float((full['logits']-ma['logits']).norm().item()),
                                 'candidate_mask_first_token_changed':full['first_token_id']!=mc['first_token_id'],
                                 'anchor_mask_first_token_changed':full['first_token_id']!=ma['first_token_id'],
                                 'baseline_prediction':prediction,'expected_OFFLINE':expected,
                                 'baseline_correct_OFFLINE':prediction==expected,
                                 'controller_action':'ABSTAIN_NO_VALIDATED_CAUSAL_SELECTOR',
                                 'arms':[{'arm':'OFF','prediction':prediction,
                                          'correct_OFFLINE':prediction==expected}]})
                    gate800('KV_UNCHANGED_'+fid+'_'+candidate+'_'+str(slot),
                            compare_seals(seal,memory_seals(mem)))
                finally:
                    del mem;gc.collect();release()
        # Crossed 2x2 contrasts; content at same slot versus slot at same content.
        def dist800(a,b):return float((a.float()-b.float()).norm().item())
        def cos800(a,b):
            a=a.float();b=b.float();return float(torch.dot(a,b).item()/max(float(a.norm().item())*float(b.norm().item()),1e-12))
        for view in VIEWS:
            a,b=candidates
            x={(cand,slot):paired[(fid,cand,slot,view)] for cand in candidates for slot in (0,1)}
            clean=(x[(a,0)]['candidate_tokens']==x[(b,0)]['candidate_tokens'] and
                   x[(a,1)]['candidate_tokens']==x[(b,1)]['candidate_tokens'])
            # Signed content contrasts in same slot; position contrasts for same candidate.
            c0=x[(b,0)]['state']-x[(a,0)]['state']
            c1=x[(b,1)]['state']-x[(a,1)]['state']
            p_a=x[(a,1)]['state']-x[(a,0)]['state']
            p_b=x[(b,1)]['state']-x[(b,0)]['state']
            interaction=c1-c0
            # Candidate-specific masking effects within each exact native fused pair.
            e0=x[(b,0)]['candidate_effect']-x[(a,0)]['candidate_effect']
            e1=x[(b,1)]['candidate_effect']-x[(a,1)]['candidate_effect']
            row={'family':fid,'view':view,'candidate_ids':candidates,
                 'candidate_token_counts':{cand:[x[(cand,s)]['candidate_tokens'] for s in (0,1)] for cand in candidates},
                 'length_matched_content_contrast':clean,
                 'content_at_slot0_l2':dist800(x[(b,0)]['state'],x[(a,0)]['state']),
                 'content_at_slot1_l2':dist800(x[(b,1)]['state'],x[(a,1)]['state']),
                 'position_for_B1_l2':dist800(x[(a,0)]['state'],x[(a,1)]['state']),
                 'position_for_X1_l2':dist800(x[(b,0)]['state'],x[(b,1)]['state']),
                 'content_direction_cosine_across_slots':cos800(c0,c1),
                 'content_position_interaction_l2':float(interaction.norm().item()),
                 'candidate_mask_effect_content_delta_slot0_l2':float(e0.norm().item()),
                 'candidate_mask_effect_content_delta_slot1_l2':float(e1.norm().item()),
                 'content_first_token_changes':[x[(a,s)]['first_token_id']!=x[(b,s)]['first_token_id'] for s in (0,1)],
                 'position_first_token_changes':[x[(cand,0)]['first_token_id']!=x[(cand,1)]['first_token_id'] for cand in candidates],
                 'causal_scope':'LENGTH_MATCHED_FIXED_SLOT_CONTENT_COMPARISON' if clean else 'LENGTH_CONFOUNDED_DIAGNOSTIC_ONLY',
                 'interpretation_limit':'Native KV content swap via cartridge substitution; source position and context are not independently held fixed across slot swaps.'}
            comparisons.append(row);log('TEST800_FACTORIAL',json.dumps(row,ensure_ascii=False))
        for cid,h in original_sha.items():
            gate800('SSD_SHA_UNCHANGED_'+cid,sha_file(CART_DIR/(cid+'.pt'))==h)
    gate800('TOTAL_CASES',len(R['rows'])==16,len(R['rows']))
    gate800('FACTORIAL_COMPARISONS',len(comparisons)==4,len(comparisons))
    gate800('CLEAN_LENGTH_MATCHED_AVAILABLE',sum(t['length_matched_content_contrast'] for t in comparisons)>=1)
    gate800('BASELINE_GENERATIONS',sum(len(row['arms']) for row in R['rows'])==16)
    gate800('ALL_ABSTAIN',all(row['controller_action'].startswith('ABSTAIN') for row in R['rows']))
    gate800('FROZEN_WEIGHTS',sentinel()==before800)
    gate800('FINAL_MANIFEST',len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    gate800('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    R['factorial_audit']=comparisons
    R['summary']={'cases':len(R['rows']),'generation_runs':16,'factorial_comparisons':len(comparisons),
                  'clean_length_matched_comparisons':sum(t['length_matched_content_contrast'] for t in comparisons),
                  'confounded_length_comparisons':sum(not t['length_matched_content_contrast'] for t in comparisons),
                  'baseline_correct':sum(row['baseline_correct_OFFLINE'] for row in R['rows']),
                  'abstentions':sum(row['controller_action'].startswith('ABSTAIN') for row in R['rows']),
                  'interpretation':'2x2 physical cartridge content-by-slot crossover, with native-KV mask controls. Clean fixed-slot contrasts are only those with equal token lengths. Position/order/context remain entangled; no autonomous selector.'}
    R['status']='COMPLETE_RESULTS_RECORDED';save800()
    log('TEST800_COMPLETED',json.dumps(R['summary'],ensure_ascii=False));log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save800()
    log('TEST800_FAILED',repr(e));log(R['traceback']);raise
finally:save800()
