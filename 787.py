# AKBASCORE SILICON HIPPOCAMPUS — TEST787
# ONE COLAB CELL | A100 80GB | FROZEN Qwen2.5-72B | NO HOOKS / NO TRAINING
# Exact TEST785 working prelude -> exact TEST779 physical CUT3 engine.
# TEST787: counterfactual physical memory perturbations + source-blind DrA probe.
import urllib.request, hashlib, ast, json, traceback, gc, math, time

URL787='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/785.py'
BLOB785_SHA256='a4e2ea480764d68cc73be9bfcf926dca5765fffadcad6dc99e3c0ef7b0642ec1'
src787=urllib.request.urlopen(urllib.request.Request(URL787,headers={'User-Agent':'AKBASCORE-TEST787'}),timeout=180).read()
assert hashlib.sha256(src787).hexdigest()==BLOB785_SHA256,'FAIL_CLOSED_TEST785_SOURCE_CHANGED'
tree787=ast.parse(src787.decode('utf-8'),filename='785.py')
cut787=next((i for i,n in enumerate(tree787.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:3])),None)
assert cut787 is not None and cut787==len(tree787.body)-1,'FAIL_CLOSED_TEST785_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree787.body[:cut787],type_ignores=[])),
             'TEST785_LOCKED_PRELUDE','exec'),globals())
assert gitblob785(raw785)==BLOB,'FAIL_CLOSED_TEST779_SOURCE_CHANGED'

TEST='787'; OUT=ROOT/'TEST787_results.json'; LOG=ROOT/'TEST787.log'; MANIFEST=ROOT/'TEST787_manifest.json'
LOG.write_text('',encoding='utf-8')
MAX_TOKENS=20
# Precommitted, fixed thresholds. NOT optimized on panel gold labels.
MIN_PAIR_ADVANTAGE=0.15
MIN_CONTRADICTION=0.15
R={'test':'787','status':'STARTED','run_id':RUN_ID,
   'source785_sha256':BLOB785_SHA256,'source779_git_blob':BLOB,
   'panel_sha256':PANEL_SHA,'locks':LOCKS,'rows':[],'checks':[],
   'thresholds':{'pair_advantage':MIN_PAIR_ADVANTAGE,'contradiction':MIN_CONTRADICTION},
   'limitations':[
       'Synthetic TEST779 panel reused; results not held-out generalization',
       'Swapped and cross-family cache combinations are perturbation probes, not guaranteed wrong-PAIR examples',
       'Model may confidently produce incorrect answers; candidate likelihood is not truth',
       'Controller receives no gold answer, temporal view, cartridge text, or source correctness',
       'This is a one-step intervention probe, not autonomous learning or STORE',
       'Cross-family source mismatch is known to the experimenter but hidden from controller',
       'Score comparisons are conditional on the frozen model, not calibrated probabilities of correctness']}
def save787(): OUT.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
def emit787(row):
    R['rows'].append(row);save787();log('TEST787_ROW',json.dumps(row,ensure_ascii=False,default=str))
def clean787(s): return s.strip() if isinstance(s,str) else ''
def read787(mem,q):
    return free_generate(mem,q,max_new=MAX_TOKENS,spans={'B0':(0,0),'B1':(0,0)})
def score787(mem,q,candidate):
    return float(norm785(mem,q,candidate)) if candidate else float('-inf')
def decide787(preds,scores):
    # Inputs: opaque candidate outputs and log probabilities ONLY.
    # Baseline PAIR answer; use independent physical single-cache alternatives as a challenge.
    p=clean787(preds['PAIR'])
    if not p or p=='UNKNOWN':
        proposals=list(dict.fromkeys(x for x in (clean787(preds['B0']),clean787(preds['B1']))
                                        if x and x!='UNKNOWN'))
        if len(proposals)!=1:
            return {'action':'ABSTAIN','reason':'PAIR_MISSING_AND_NONUNIQUE'}
        c=proposals[0]
        if scores['PAIR'].get(c,float('-inf'))-scores['PAIR'].get('UNKNOWN',float('-inf')) < MIN_PAIR_ADVANTAGE:
            return {'action':'ABSTAIN','reason':'PAIR_DOES_NOT_SUPPORT_RECOVERY'}
        owners=[s for s in ('B0','B1') if clean787(preds[s])==c]
        if len(owners)!=1:return {'action':'ABSTAIN','reason':'RECOVERY_SOURCE_NOT_UNIQUE'}
        return {'action':'SWITCH_'+owners[0],'reason':'PAIR_ABSTAIN_RECOVERED','candidate':c}
    # When PAIR has a concrete answer, quantify disagreement rather than blindly trusting it.
    alternatives=list(dict.fromkeys(x for x in (clean787(preds['B0']),clean787(preds['B1']))
                                      if x and x!='UNKNOWN' and x!=p))
    if not alternatives:return {'action':'KEEP_PAIR','reason':'NO_CONCRETE_CHALLENGER'}
    # PAIR must itself prefer a competing candidate over its own answer, and the
    # candidate must have unique isolated support. Otherwise avoid damaging PAIR.
    ranked=sorted(((c,scores['PAIR'].get(c,float('-inf'))-scores['PAIR'].get(p,float('-inf')))
                   for c in alternatives),key=lambda x:x[1],reverse=True)
    challenger,gap=ranked[0]
    if gap < MIN_CONTRADICTION:
        return {'action':'KEEP_PAIR','reason':'PAIR_SUPPORTS_OWN_ANSWER',
                'strongest_challenge':challenger,'gap':gap}
    owners=[s for s in ('B0','B1') if clean787(preds[s])==challenger]
    if len(owners)!=1:return {'action':'ABSTAIN','reason':'CHALLENGER_SOURCE_AMBIGUOUS','gap':gap}
    return {'action':'SWITCH_'+owners[0],'reason':'PAIR_SELF_CONTRADICTION',
            'candidate':challenger,'gap':gap}

def controller_unit787():
    tests=[({'PAIR':'TEAM-X','B0':'UNKNOWN','B1':'TEAM-X'},
            {'PAIR':{'TEAM-X':-0.1,'UNKNOWN':-8}},'KEEP_PAIR'),
           ({'PAIR':'UNKNOWN','B0':'UNKNOWN','B1':'UNKNOWN'},
            {'PAIR':{'UNKNOWN':-0.1}},'ABSTAIN'),
           ({'PAIR':'TEAM-X','B0':'TEAM-Y','B1':'TEAM-X'},
            {'PAIR':{'TEAM-X':-5,'TEAM-Y':-0.1}},'SWITCH_B0')]
    for i,(p,s,want) in enumerate(tests):
        got=decide787(p,s)
        check('CONTROLLER_UNIT_'+str(i),got['action']==want,got)

try:
    log('='*110)
    log('AKBASCORE TEST787 — PHYSICAL COUNTERFACTUAL MEMORY / PAIR CONTRADICTION PROBE')
    check('EXACT_785_SHA256',hashlib.sha256(src787).hexdigest()==BLOB785_SHA256)
    check('EXACT_779_GIT_BLOB',gitblob785(raw785)==BLOB)
    check('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    controller_unit787()
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    check('GPU_VRAM',free>=40*2**30,'Fresh A100 runtime required')
    model_setup();weights_before=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    check('PHYSICAL_20_CARTRIDGES',len(entries)==20,len(entries))
    families=list(FAMILIES)
    check('FAMILIES_AT_LEAST_4',len(families)>=4,len(families))
    for ix,fam in enumerate(families):
        fid=fam['id'];other=families[(ix+1)%len(families)]['id']
        b0=fid+'_B0';b1=fid+'_B1';d0=other+'_B0';d1=other+'_B1'
        # No modification of any cartridge. Only native installation order/selection changes.
        cids=[b0,b1,d0,d1]
        sha_before={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in cids}
        scenarios=[
            ('ORIGINAL',[b0,b1]),
            ('REVERSED',[b1,b0]),
            ('CROSS_B0',[b0,d1]),
            ('CROSS_B1',[d0,b1]),
            ('UNRELATED',[d0,d1])]
        work=next(c['work'] for c in CASES if c['family']==fid)
        for scen,pair in scenarios:
            mems={}
            try:
                # Native physical readout: isolated caches and fused PAIR.
                for key,cid in zip(('B0','B1'),pair):
                    mems[key]=build_source_cache(cid,fid+'_'+scen)
                    check('NATIVE_80_'+fid+'_'+scen+'_'+key,len(mems[key])==80)
                mems['PAIR'],active,_,_=build_fusion(pair,'TEST787_'+fid+'_'+scen,True)
                check('NATIVE_PAIR_80_'+fid+'_'+scen,len(mems['PAIR'])==80)
                check('PAIR_ORDER_'+fid+'_'+scen,list(active)==pair)
                seals={s:memory_seals(m) for s,m in mems.items()}
                for view in VIEWS:
                    q=CUE[view].format(work=work)
                    gen={s:read787(mems[s],q) for s in ('B0','B1','PAIR')}
                    preds={s:clean787(gen[s]['raw']) for s in gen}
                    candidates=list(dict.fromkeys(x for x in list(preds.values())+['UNKNOWN'] if x))
                    scores={s:{c:round(score787(mems[s],q,c),6) for c in candidates}
                            for s in ('B0','B1','PAIR')}
                    decision=decide787(preds,scores)
                    action=decision['action']
                    selected='PAIR' if action=='KEEP_PAIR' else (
                        'B0' if action=='SWITCH_B0' else ('B1' if action=='SWITCH_B1' else None))
                    readout=read787(mems[selected],q) if selected else None
                    final=clean787(readout['raw']) if readout else 'UNKNOWN'
                    # Gold is strictly offline: evaluated AFTER action/readout.
                    expected=fam['new_team'] if view=='CURRENT' else fam['old_team']
                    row={'family':fid,'scenario':scen,'view_OFFLINE':view,
                         'cartridges_OFFLINE':pair,'generated':gen,'scores':scores,
                         'decision':decision,'selected':selected,'readout':readout,
                         'final':final,'expected_OFFLINE':expected,
                         'correct_OFFLINE':final==expected,
                         'pair_correct_OFFLINE':preds['PAIR']==expected,
                         'pair_nonunknown_wrong_OFFLINE':preds['PAIR'] not in ('','UNKNOWN',expected),
                         'correct_pair_damaged_OFFLINE':preds['PAIR']==expected and final!=expected,
                         'wrong_pair_corrected_OFFLINE':preds['PAIR'] not in ('','UNKNOWN',expected) and final==expected,
                         'unjustified_answer_OFFLINE':scen=='UNRELATED' and final!='UNKNOWN'}
                    emit787(row)
                for s,m in mems.items():
                    check('KV_UNCHANGED_'+fid+'_'+scen+'_'+s,
                          compare_seals(seals[s],memory_seals(m)))
            finally:
                mems.clear();gc.collect();release()
        for cid in cids:
            check('SSD_SHA_UNCHANGED_'+cid,sha_file(CART_DIR/(cid+'.pt'))==sha_before[cid])
    check('TOTAL_CASES',len(R['rows'])==len(families)*5*len(VIEWS),len(R['rows']))
    check('FROZEN_WEIGHTS',sentinel()==weights_before)
    check('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks
          and not model.model.layers[CUT]._forward_pre_hooks)
    R['summary']={
        'n':len(R['rows']),
        'correct':sum(x['correct_OFFLINE'] for x in R['rows']),
        'pair_correct':sum(x['pair_correct_OFFLINE'] for x in R['rows']),
        'wrong_pair_cases':sum(x['pair_nonunknown_wrong_OFFLINE'] for x in R['rows']),
        'wrong_pair_corrected':sum(x['wrong_pair_corrected_OFFLINE'] for x in R['rows']),
        'correct_pair_damaged':sum(x['correct_pair_damaged_OFFLINE'] for x in R['rows']),
        'unrelated_nonunknown':sum(x['unjustified_answer_OFFLINE'] for x in R['rows']),
        'actions':{a:sum(x['decision']['action']==a for x in R['rows'])
                   for a in ('SWITCH_B0','SWITCH_B1','KEEP_PAIR','ABSTAIN')},
        'scenarios':{sc:{'n':sum(x['scenario']==sc for x in R['rows']),
                         'correct':sum(x['scenario']==sc and x['correct_OFFLINE'] for x in R['rows']),
                         'pair_correct':sum(x['scenario']==sc and x['pair_correct_OFFLINE'] for x in R['rows'])}
                     for sc in ('ORIGINAL','REVERSED','CROSS_B0','CROSS_B1','UNRELATED')},
        'note':'No correction success unless incorrect PAIR cases actually occur and are corrected.'}
    R['status']='COMPLETE_RESULTS_RECORDED';save787()
    log('TEST787_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc()
    save787();log('TEST787_FAILED',repr(e));log(R['traceback']);raise
finally:
    save787()
