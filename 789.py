# AKBASCORE SILICON HIPPOCAMPUS — TEST789
# ONE COLAB CELL | A100 80GB | FROZEN Qwen2.5-72B | PHYSICAL CUT3
# Exact GPU-completed TEST788 working prelude and native TEST779 engine.
# Test: blind counterfactual order-stability gate; no gold/source text in controller.
# This is a deterministic safety baseline, NOT autonomous truth identification.
import urllib.request,hashlib,ast,json,traceback,gc,re

SOURCE_URL_789='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/788.py'
SOURCE_GIT_BLOB_789='51e9e8428a45f075cde4f6ce72c9bdaca396163b'
# Explicit Git blob lock (GitHub's published 788.py); no imported helper required.
src789=urllib.request.urlopen(urllib.request.Request(SOURCE_URL_789,headers={'User-Agent':'AKBASCORE-TEST789'}),timeout=180).read()
actual789=hashlib.sha1(b'blob '+str(len(src789)).encode()+b'\0'+src789).hexdigest()
# Set by release build; fail closed if source changes.
assert actual789==SOURCE_GIT_BLOB_789,('FAIL_CLOSED_TEST788_CHANGED',actual789)
tree789=ast.parse(src789.decode('utf-8'),filename='788.py')
cut789=next((i for i,n in enumerate(tree789.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:3])),None)
assert cut789 is not None and cut789==len(tree789.body)-1,'FAIL_CLOSED_TEST788_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree789.body[:cut789],type_ignores=[])),
             'TEST788_LOCKED_PRELUDE','exec'),globals())
assert gitblob785(raw785)==BLOB,'FAIL_CLOSED_TEST779_SOURCE_CHANGED'

TEST='789';OUT=ROOT/'TEST789_results.json';LOG=ROOT/'TEST789.log';MANIFEST=ROOT/'TEST789_manifest.json'
LOG.write_text('',encoding='utf-8')
MAX_TOKENS=20
R={'test':'789','status':'STARTED','run_id':RUN_ID,
   'source788_git_blob':SOURCE_GIT_BLOB_789,'source779_git_blob':BLOB,
   'panel_sha256':PANEL_SHA,'locks':LOCKS,'rows':[],'checks':[],
   'design':'Order-reversal counterfactual on identical physical cartridge pair; blind abstention gate',
   'limitations':['Deterministic order-consistency controller, not autonomous truth detection',
                  'Synthetic TEST779 panel reused; not held-out generalization',
                  'Two agreeing wrong orders can still produce an incorrect answer',
                  'Order reversal is a perturbation, not independent evidence of truth',
                  'Controller sees only parsed native readouts, not gold, view, scenario, source text or source IDs',
                  'No online learning, source reliability inference or model weight update']}
def save789():OUT.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
def emit789(row):
    R['rows'].append(row);save789();log('TEST789_ROW',json.dumps(row,ensure_ascii=False,default=str))

def parse789(raw):
    # Use model's existing exact TEAM-code parser, not raw-string equality.
    # In particular, "UNKNOWN\n\nExplanation" must be counted as abstention.
    p=read_exact(raw,'TEAM')
    if not isinstance(p,str):return 'UNKNOWN'
    p=p.strip()
    return p if re.fullmatch(r'TEAM-[A-Z]+',p) else 'UNKNOWN'

def decide789(forward,reverse):
    # No source identity, order metadata, gold or scenario is provided to this function.
    if forward=='UNKNOWN' or reverse=='UNKNOWN':
        return {'action':'ABSTAIN','reason':'MISSING_CONSENSUS'}
    if forward!=reverse:
        return {'action':'ABSTAIN','reason':'ORDER_SENSITIVE_CONFLICT'}
    return {'action':'KEEP_PAIR','reason':'ORDER_STABLE_AGREEMENT','candidate':forward}

def unit789():
    for i,(a,b,action) in enumerate([
        ('TEAM-ABC','TEAM-ABC','KEEP_PAIR'),
        ('TEAM-ABC','TEAM-XYZ','ABSTAIN'),
        ('UNKNOWN','TEAM-ABC','ABSTAIN'),
        ('TEAM-ABC','UNKNOWN','ABSTAIN'),
        ('UNKNOWN','UNKNOWN','ABSTAIN')]):
        check('DECISION_UNIT_'+str(i),decide789(a,b)['action']==action)
    check('PARSE_UNKNOWN_EXPLANATION',parse789('UNKNOWN\n\nRevision 2 is latest.')=='UNKNOWN')

try:
    log('='*110)
    log('AKBASCORE TEST789 — PHYSICAL ORDER-REVERSAL / BLIND CONSISTENCY GATE')
    check('EXACT_788_GIT_BLOB',actual789==SOURCE_GIT_BLOB_789)
    check('EXACT_779_GIT_BLOB',gitblob785(raw785)==BLOB)
    check('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    unit789()
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    check('GPU_VRAM',free>=40*2**30,'Fresh A100 runtime required')
    model_setup();weights_before=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    check('PHYSICAL_20_CARTRIDGES',len(entries)==20,len(entries))
    families=list(FAMILIES)
    check('FOUR_FAMILIES',len(families)==4,len(families))
    # Exactly the TEST788 contradictory cartridge texts, unchanged.
    new_cards={}
    for i,fam in enumerate(families):
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        decoy=families[(i+1)%len(families)]['new_team']
        assert decoy not in (fam['new_team'],fam['old_team'])
        new_cards[fid+'_X1']=(f'Authoritative CURRENT record REVISION 1: {work} '
                              f'collaborates_with {decoy}. Supersedes revision 0.')
        new_cards[fid+'_X0']=(f'Historical record REVISION 0 (superseded): {work} '
                              f'collaborates_with {decoy}. Valid at revision 0 only.')
        new_cards[fid+'_X2']=(f'Authoritative CURRENT record REVISION 2: {work} '
                              f'collaborates_with {decoy}. Supersedes revision 1.')
    for cid,body in sorted(new_cards.items()):physical_commit(cid,body)
    check('PHYSICAL_32_CARTRIDGES',len(entries)==32,len(entries))
    for ix,fam in enumerate(families):
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        b0=fid+'_B0';b1=fid+'_B1';x1=fid+'_X1';x0=fid+'_X0';x2=fid+'_X2'
        scenarios=[('BASELINE',[b0,b1]),('SAME_REV_CONFLICT',[b1,x1]),
                   ('SAME_REV_REVERSED',[x1,b1]),('OLDER_DECOY',[b1,x0]),
                   ('NEWER_DECOY',[b1,x2]),('DECOY_ONLY',[x1,x2])]
        original_sha={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in (b0,b1,x0,x1,x2)}
        for scenario,pair in scenarios:
            mems={}
            try:
                # Both physical installations use the same unchanged 80-layer fusion.
                for arm,order in (('FORWARD',pair),('REVERSE',list(reversed(pair)))):
                    mems[arm],active,_,_=build_fusion(order,'TEST789_'+fid+'_'+scenario+'_'+arm,True)
                    check('NATIVE_80_'+fid+'_'+scenario+'_'+arm,len(mems[arm])==80)
                    check('PAIR_ORDER_'+fid+'_'+scenario+'_'+arm,list(active)==order)
                seals={arm:memory_seals(mem) for arm,mem in mems.items()}
                for view in VIEWS:
                    q=CUE[view].format(work=work)
                    generated={arm:read788(mems[arm],q) for arm in ('FORWARD','REVERSE')}
                    parsed={arm:parse789(generated[arm]['raw']) for arm in generated}
                    decision=decide789(parsed['FORWARD'],parsed['REVERSE'])
                    final=parsed['FORWARD'] if decision['action']=='KEEP_PAIR' else 'UNKNOWN'
                    # Offline-only evaluation AFTER the decision. No gold in controller.
                    baseline=fam['new_team'] if view=='CURRENT' else fam['old_team']
                    decoy=families[(ix+1)%len(families)]['new_team']
                    row={'family':fid,'scenario_OFFLINE':scenario,'view_OFFLINE':view,
                         'cartridges_OFFLINE':pair,'generated':generated,'parsed':parsed,
                         'decision':decision,'final':final,
                         'baseline_expected_OFFLINE':baseline,'decoy_OFFLINE':decoy,
                         'forward_baseline_OFFLINE':parsed['FORWARD']==baseline,
                         'forward_decoy_OFFLINE':parsed['FORWARD']==decoy,
                         'reverse_baseline_OFFLINE':parsed['REVERSE']==baseline,
                         'reverse_decoy_OFFLINE':parsed['REVERSE']==decoy,
                         'order_sensitive_OFFLINE':parsed['FORWARD']!=parsed['REVERSE'],
                         'final_baseline_OFFLINE':final==baseline,
                         'final_decoy_OFFLINE':final==decoy,
                         'final_unknown_OFFLINE':final=='UNKNOWN',
                         'wrong_forward_suppressed_OFFLINE':parsed['FORWARD']==decoy and final=='UNKNOWN',
                         'correct_forward_damaged_OFFLINE':parsed['FORWARD']==baseline and final!=baseline}
                    emit789(row)
                for arm,mem in mems.items():
                    check('KV_UNCHANGED_'+fid+'_'+scenario+'_'+arm,
                          compare_seals(seals[arm],memory_seals(mem)))
            finally:
                mems.clear();gc.collect();release()
        for cid,h in original_sha.items():
            check('SSD_SHA_UNCHANGED_'+cid,sha_file(CART_DIR/(cid+'.pt'))==h)
    check('TOTAL_CASES',len(R['rows'])==len(families)*6*len(VIEWS),len(R['rows']))
    check('FROZEN_WEIGHTS',sentinel()==weights_before)
    check('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
          not model.model.layers[CUT]._forward_pre_hooks)
    R['summary']={'n':len(R['rows']),
       'order_sensitive':sum(r['order_sensitive_OFFLINE'] for r in R['rows']),
       'forward_baseline':sum(r['forward_baseline_OFFLINE'] for r in R['rows']),
       'forward_decoy':sum(r['forward_decoy_OFFLINE'] for r in R['rows']),
       'final_baseline':sum(r['final_baseline_OFFLINE'] for r in R['rows']),
       'final_decoy':sum(r['final_decoy_OFFLINE'] for r in R['rows']),
       'final_unknown':sum(r['final_unknown_OFFLINE'] for r in R['rows']),
       'wrong_forward_suppressed':sum(r['wrong_forward_suppressed_OFFLINE'] for r in R['rows']),
       'correct_forward_damaged':sum(r['correct_forward_damaged_OFFLINE'] for r in R['rows']),
       'actions':{a:sum(r['decision']['action']==a for r in R['rows']) for a in ('KEEP_PAIR','ABSTAIN')},
       'scenarios':{sc:{'n':sum(r['scenario_OFFLINE']==sc for r in R['rows']),
                         'order_sensitive':sum(r['scenario_OFFLINE']==sc and r['order_sensitive_OFFLINE'] for r in R['rows']),
                         'final_decoy':sum(r['scenario_OFFLINE']==sc and r['final_decoy_OFFLINE'] for r in R['rows'])}
                    for sc in ('BASELINE','SAME_REV_CONFLICT','SAME_REV_REVERSED','OLDER_DECOY','NEWER_DECOY','DECOY_ONLY')},
       'interpretation':'Order consistency can trigger abstention; agreement is not proof of truth.'}
    R['status']='COMPLETE_RESULTS_RECORDED';save789()
    log('TEST789_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc()
    save789();log('TEST789_FAILED',repr(e));log(R['traceback']);raise
finally:save789()
