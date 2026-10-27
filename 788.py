# AKBASCORE TEST788 — PHYSICAL SAME-ENTITY CONTRADICTION / FROZEN 72B
# ONE COLAB CELL; GPU-PROVEN TEST787 DEFINITIONS, UNCHANGED TEST779 ENGINE.
# Research probe: conflicting revision-1 sources and causal physical ablation.
# No gold, revision view, source body, or scenario label enters controller.
import urllib.request,hashlib,ast,json,traceback,gc,math
URL788='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/787.py'
# SHA of 787.py is precommitted below; change requires manual review.
EXPECTED_787_GIT_BLOB='fcc939d2d04fc81d754246922bc40d7be13dcb5c'
src788=urllib.request.urlopen(urllib.request.Request(URL788,headers={'User-Agent':'AKBASCORE-TEST788'}),timeout=180).read()
assert hashlib.sha1(b'blob '+str(len(src788)).encode()+b'\0'+src788).hexdigest()==EXPECTED_787_GIT_BLOB,'FAIL_CLOSED_TEST787_SOURCE_CHANGED'
tree788=ast.parse(src788.decode('utf-8'),filename='787.py')
cut788=next((i for i,n in enumerate(tree788.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:3])),None)
assert cut788 is not None and cut788==len(tree788.body)-1,'FAIL_CLOSED_TEST787_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree788.body[:cut788],type_ignores=[])),
             'TEST787_LOCKED_PRELUDE','exec'),globals())
assert gitblob785(raw785)==BLOB,'FAIL_CLOSED_TEST779_SOURCE_CHANGED'
TEST='788';OUT=ROOT/'TEST788_results.json';LOG=ROOT/'TEST788.log';MANIFEST=ROOT/'TEST788_manifest.json'
LOG.write_text('',encoding='utf-8')
MAX_TOKENS=20
R={'test':'788','status':'STARTED','run_id':RUN_ID,'source787_git_blob':EXPECTED_787_GIT_BLOB,
   'source779_git_blob':BLOB,'panel_sha256':PANEL_SHA,'locks':LOCKS,
   'rows':[],'checks':[],
   'design':'Same-work, same-revision conflicting physical source cartridges',
   'limits':['Original synthetic TEST779 work identifiers reused; not held-out generalization',
             'Conflicting authoritative claims have no intrinsically knowable ground truth',
             'No gold answers, source bodies, scenario or temporal view supplied to controller',
             'No claim of autonomous semantic conflict resolution or learning',
             'Observed physical ablation is causal on outputs, not a proof of truth',
             'Controller is an observational baseline: does not force a correct answer']}
def save788():OUT.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
def emit788(row):
    R['rows'].append(row);save788();log('TEST788_ROW',json.dumps(row,ensure_ascii=False,default=str))
def clean788(s):return s.strip() if isinstance(s,str) else ''
def read788(mem,q):return free_generate(mem,q,max_new=MAX_TOKENS,spans={'B0':(0,0),'B1':(0,0)})
def score788(mem,q,c):return float(norm785(mem,q,c)) if c else float('-inf')
def decision788(preds,scores):
    # Identical to the TEST787 decision baseline; scenario-blind, no oracle.
    return decide787(preds,scores)
def negative_unit788():
    controller_unit787()
    # A PAIR with two concrete challengers cannot be labeled 'wrong' without truth.
    check('CONFLICT_NO_GOLD_IN_CONTROLLER',
          'expected' not in decision788.__code__.co_names and
          'view' not in decision788.__code__.co_names)
try:
    log('='*112);log('AKBASCORE TEST788 / PHYSICAL CONTRADICTORY SAME-ENTITY REVISION-1 RECORDS')
    check('EXACT_787_GIT_BLOB',gitblob785(src788)==EXPECTED_787_GIT_BLOB)
    check('EXACT_779_GIT_BLOB',gitblob785(raw785)==BLOB)
    check('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    negative_unit788()
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    check('GPU_VRAM',free>=40*2**30,'Fresh A100 runtime required')
    model_setup();weights_before=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    check('PHYSICAL_20_CARTRIDGES',len(entries)==20,len(entries))
    families=list(FAMILIES)
    check('FOUR_FAMILIES',len(families)==4,len(families))
    # New cartridges contain SAME work identifier and incompatible claims.
    # Decoy team is taken from another independent family, never the true team.
    # Gold remains offline and cannot be used by the decision function.
    new_cards={}
    for i,fam in enumerate(families):
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        other=families[(i+1)%len(families)]
        decoy=other['new_team']
        assert decoy not in (fam['new_team'],fam['old_team'])
        new_cards[fid+'_X1']=(f'Authoritative CURRENT record REVISION 1: {work} '
                              f'collaborates_with {decoy}. Supersedes revision 0.')
        new_cards[fid+'_X0']=(f'Historical record REVISION 0 (superseded): {work} '
                              f'collaborates_with {decoy}. Valid at revision 0 only.')
        # Contradictory claim with explicit higher revision, a distinct scenario.
        new_cards[fid+'_X2']=(f'Authoritative CURRENT record REVISION 2: {work} '
                              f'collaborates_with {decoy}. Supersedes revision 1.')
    for cid,body in sorted(new_cards.items()):physical_commit(cid,body)
    check('PHYSICAL_32_CARTRIDGES',len(entries)==32,len(entries))
    for fam in families:
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        b0=fid+'_B0';b1=fid+'_B1';x1=fid+'_X1';x0=fid+'_X0';x2=fid+'_X2'
        # All arms built with the same unchanged 80-layer native fusion.
        scenarios=[('BASELINE',[b0,b1]),
                   ('SAME_REV_CONFLICT',[b1,x1]),
                   ('SAME_REV_REVERSED',[x1,b1]),
                   ('OLDER_DECOY',[b1,x0]),
                   ('NEWER_DECOY',[b1,x2]),
                   ('DECOY_ONLY',[x1,x2])]
        original_sha={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in (b0,b1,x0,x1,x2)}
        for scenario,pair in scenarios:
            mems={}
            try:
                for key,cid in zip(('B0','B1'),pair):
                    mems[key]=build_source_cache(cid,fid+'_'+scenario)
                    check('NATIVE_80_'+fid+'_'+scenario+'_'+key,len(mems[key])==80)
                mems['PAIR'],active,_,_=build_fusion(pair,'TEST788_'+fid+'_'+scenario,True)
                check('NATIVE_PAIR_80_'+fid+'_'+scenario,len(mems['PAIR'])==80)
                check('PAIR_ORDER_'+fid+'_'+scenario,list(active)==pair)
                seals={s:memory_seals(m) for s,m in mems.items()}
                for view in VIEWS:
                    q=CUE[view].format(work=work)
                    generated={s:read788(mems[s],q) for s in ('B0','B1','PAIR')}
                    preds={s:clean788(generated[s]['raw']) for s in generated}
                    candidates=list(dict.fromkeys(x for x in list(preds.values())+['UNKNOWN'] if x))
                    scores={s:{c:round(score788(mems[s],q,c),6) for c in candidates}
                            for s in ('B0','B1','PAIR')}
                    decision=decision788(preds,scores)
                    action=decision['action']
                    selected=('PAIR' if action=='KEEP_PAIR' else
                              'B0' if action=='SWITCH_B0' else
                              'B1' if action=='SWITCH_B1' else None)
                    readout=read788(mems[selected],q) if selected else None
                    final=clean788(readout['raw']) if readout else 'UNKNOWN'
                    # Offline reference labels are applied only after physical action.
                    baseline_expected=fam['new_team'] if view=='CURRENT' else fam['old_team']
                    decoy=families[(families.index(fam)+1)%len(families)]['new_team']
                    row={'family':fid,'scenario_OFFLINE':scenario,'view_OFFLINE':view,
                         'cartridges_OFFLINE':pair,'generated':generated,'scores':scores,
                         'decision':decision,'selected':selected,'readout':readout,'final':final,
                         'baseline_expected_OFFLINE':baseline_expected,'decoy_OFFLINE':decoy,
                         'pair_is_baseline_OFFLINE':preds['PAIR']==baseline_expected,
                         'pair_is_decoy_OFFLINE':preds['PAIR']==decoy,
                         'final_is_baseline_OFFLINE':final==baseline_expected,
                         'final_is_decoy_OFFLINE':final==decoy,
                         'pair_unknown_OFFLINE':preds['PAIR']=='UNKNOWN',
                         'final_unknown_OFFLINE':final=='UNKNOWN',
                         'changed_pair_OFFLINE':final!=preds['PAIR']}
                    emit788(row)
                for s,m in mems.items():
                    check('KV_UNCHANGED_'+fid+'_'+scenario+'_'+s,
                          compare_seals(seals[s],memory_seals(m)))
            finally:
                mems.clear();gc.collect();release()
        for cid,h in original_sha.items():
            check('SSD_SHA_UNCHANGED_'+cid,sha_file(CART_DIR/(cid+'.pt'))==h)
    check('TOTAL_CASES',len(R['rows'])==len(families)*6*len(VIEWS),len(R['rows']))
    check('FROZEN_WEIGHTS',sentinel()==weights_before)
    check('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
          not model.model.layers[CUT]._forward_pre_hooks)
    R['summary']={'n':len(R['rows']),
       'pair_baseline':sum(r['pair_is_baseline_OFFLINE'] for r in R['rows']),
       'pair_decoy':sum(r['pair_is_decoy_OFFLINE'] for r in R['rows']),
       'pair_unknown':sum(r['pair_unknown_OFFLINE'] for r in R['rows']),
       'final_baseline':sum(r['final_is_baseline_OFFLINE'] for r in R['rows']),
       'final_decoy':sum(r['final_is_decoy_OFFLINE'] for r in R['rows']),
       'final_unknown':sum(r['final_unknown_OFFLINE'] for r in R['rows']),
       'changed_pair':sum(r['changed_pair_OFFLINE'] for r in R['rows']),
       'actions':{a:sum(r['decision']['action']==a for r in R['rows'])
                  for a in ('SWITCH_B0','SWITCH_B1','KEEP_PAIR','ABSTAIN')},
       'scenarios':{sc:{'n':sum(r['scenario_OFFLINE']==sc for r in R['rows']),
                        'pair_baseline':sum(r['scenario_OFFLINE']==sc and r['pair_is_baseline_OFFLINE'] for r in R['rows']),
                        'pair_decoy':sum(r['scenario_OFFLINE']==sc and r['pair_is_decoy_OFFLINE'] for r in R['rows']),
                        'pair_unknown':sum(r['scenario_OFFLINE']==sc and r['pair_unknown_OFFLINE'] for r in R['rows'])}
                    for sc in ('BASELINE','SAME_REV_CONFLICT','SAME_REV_REVERSED','OLDER_DECOY','NEWER_DECOY','DECOY_ONLY')},
       'interpretation':'Contradiction sensitivity, not an autonomous truth detector.'}
    R['status']='COMPLETE_RESULTS_RECORDED';save788()
    log('TEST788_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc()
    save788();log('TEST788_FAILED',repr(e));log(R['traceback']);raise
finally:save788()
