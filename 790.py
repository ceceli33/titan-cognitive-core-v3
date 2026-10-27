# AKBASCORE SILICON HIPPOCAMPUS — TEST790 / DRA INTEGRATION AUDIT
# ONE COLAB CELL | A100 80GB | FROZEN Qwen2.5-72B | NO NEW ENGINE
# First component: TEST779 native CUT3 state/attention observation (TEST784 lineage).
# The GPU-proven TEST789 prelude and physical engine are imported unchanged.
# This is an observational interface audit, NOT a closed-loop controller.
# PATCH: preserve TEST779 manifest contract R['panel_sha256'] and R['locks'] when replacing R.
import urllib.request,hashlib,ast,json,traceback,gc,inspect,math,re

SOURCES790={
 ('titan-cognitive-core','AkbasCore_1.3_DRA_Motoru_Damped_Resonance_Alignment_Akbas_2026_DRA.py'):'fe8294e7d572a7f79b3643612b39c44c64560515',
 ('titan-cognitive-core','AkbasCore_2.0_DRA-MANIFOLD.py'):'173b81fdbba94572d1276ee9ff6e61655487b31e',
 ('titan-cognitive-core-v2','664.py'):'8757f8056dff817703eccb9630a5850c3371666d',
 ('titan-cognitive-core-v3','784_DrA_start.py'):'27a24dd6668dfa1a4804fd24e78cea9416822076',
 ('titan-cognitive-core-v3','789.py'):'56daecf29d54286b82e3f4b03387229a0f9547fb',
}
def blob790(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def fetch790(repo,path,expected):
    url='https://raw.githubusercontent.com/ceceli33/'+repo+'/main/'+path
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST790'}),timeout=180) as f: raw=f.read()
    got=blob790(raw)
    if got!=expected:raise RuntimeError('FAIL_CLOSED_SOURCE_CHANGED '+repo+'/'+path+' '+got)
    return raw
# Import EXACT TEST789 definitions; never execute its test loop.
raw790=fetch790('titan-cognitive-core-v3','789.py',SOURCES790[('titan-cognitive-core-v3','789.py')])
tree790=ast.parse(raw790.decode('utf-8'),filename='789.py')
cut790=next((i for i,n in enumerate(tree790.body) if isinstance(n,ast.Try) and any(
    isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name)
    and x.value.func.id=='log' for x in n.body[:3])),None)
assert cut790 is not None and cut790==len(tree790.body)-1,'FAIL_CLOSED_789_AST_BOUNDARY'
exec(compile(ast.fix_missing_locations(ast.Module(body=tree790.body[:cut790],type_ignores=[])),
             'TEST789_LOCKED_PRELUDE','exec'),globals())
assert gitblob785(raw785)==BLOB,'FAIL_CLOSED_TEST779_SOURCE_CHANGED'
TEST='790';OUT=ROOT/'TEST790_results.json';LOG=ROOT/'TEST790.log';MANIFEST=ROOT/'TEST790_manifest.json'
LOG.write_text('',encoding='utf-8')
R={'test':'790','status':'STARTED','run_id':RUN_ID,
   'panel_sha256':PANEL_SHA,'locks':LOCKS,
   'source_locks':{},'inventory':{},'rows':[],
   'checks':[],'scope':'OBSERVATION-ONLY; no DRA injection, no loop, no autonomous truth claims',
   'limits':['Synthetic previously used panel, not held-out','DrA 1.3/2.0 and v2 664 audited statically only',
             'TEST779 state/attention probe is instrumented observation, not hook-free runtime',
             'No controller uses gold, scenario, view or source-body labels',
             'No inference from attention magnitude to source truth']}
def save790():OUT.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
def emit790(row):R['rows'].append(row);save790();log('TEST790_ROW',json.dumps(row,ensure_ascii=False,default=str))
def gate790(name,ok,detail=None):
    R['checks'].append({'name':name,'ok':bool(ok),'detail':detail});save790()
    log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('TEST790_GATE_'+name)
def audit790():
    for (repo,path),expected in SOURCES790.items():
        raw=raw790 if path=='789.py' and repo=='titan-cognitive-core-v3' else fetch790(repo,path,expected)
        src=raw.decode('utf-8');tree=ast.parse(src,filename=path)
        funcs=[n.name for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
        classes=[n.name for n in ast.walk(tree) if isinstance(n,ast.ClassDef)]
        tokens={k:len(re.findall(re.escape(k),src,re.I)) for k in ('steer','resonan','feedback','observe','stop','abstain','CUT3','attention','hook')}
        key=repo+'/'+path
        R['source_locks'][key]={'git_blob':expected,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
        R['inventory'][key]={'functions':funcs,'classes':classes,'term_counts_NOT_CAPABILITIES':tokens}
        gate790('LOCKED_'+path,blob790(raw)==expected)
    gate790('NATIVE_OBSERVATION_SYMBOLS',all(callable(globals().get(n)) for n in
        ('observe_state','source_signal','build_fusion','free_generate','memory_seals','compare_seals','physical_commit')))
    gate790('DRA784_SOURCE_VERIFIED',any(k.endswith('784_DrA_start.py') for k in R['inventory']))
    save790()

def spans790(order,mem):
    # Same physical positions as TEST779 source_spans, but respects arbitrary order.
    a,b=order;n0=int(entries[a]['body_tokens']);n1=int(entries[b]['body_tokens'])
    n=int(mem[0][0].shape[-2]);gate790('SPAN_TOTAL_'+a+'_'+b,n==P+n0+n1,{'actual':n,'expected':P+n0+n1})
    return {'B0':(P,P+n0),'B1':(P+n0,P+n0+n1)}

try:
    log('='*112);log('TEST790 — THREE-REPOSITORY DRA/CUT3 INTEGRATION AUDIT — OBSERVATION FIRST')
    audit790()
    gate790('EXACT_789_GIT_BLOB',blob790(raw790)==SOURCES790[('titan-cognitive-core-v3','789.py')])
    gate790('EXACT_779_GIT_BLOB',gitblob785(raw785)==BLOB)
    gate790('SEALED_PANEL',hashlib.sha256((ROOT/'SEALED_PANEL.json').read_bytes()).hexdigest()==PANEL_SHA)
    gate790('MANIFEST_PANEL_KEY',R.get('panel_sha256')==PANEL_SHA)
    gate790('MANIFEST_LOCKS_KEY',R.get('locks')==LOCKS)
    # Run the unchanged TEST779 manifest writer BEFORE expensive 72B model loading.
    persist_manifest()
    manifest_pre790=json.loads(MANIFEST.read_text(encoding='utf-8'))
    gate790('MANIFEST_PREFLIGHT',manifest_pre790.get('panel_sha256')==PANEL_SHA and
            manifest_pre790.get('locks')==LOCKS and manifest_pre790.get('cartridges')=={})
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    gate790('GPU_VRAM',free>=40*2**30,'Fresh A100 80GB runtime required')
    model_setup();before790=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    gate790('PHYSICAL_20_CARTRIDGES',len(entries)==20,len(entries))
    gate790('MANIFEST_AFTER_20',MANIFEST.exists() and json.loads(MANIFEST.read_text())['panel_sha256']==PANEL_SHA)
    families=list(FAMILIES);gate790('FOUR_FAMILIES',len(families)==4,len(families))
    # Exact same contradictory source template used by TEST789; no new synthetic facts.
    cards790={}
    for ix,fam in enumerate(families):
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        decoy=families[(ix+1)%len(families)]['new_team']
        cards790[fid+'_X1']=(f'Authoritative CURRENT record REVISION 1: {work} '
                              f'collaborates_with {decoy}. Supersedes revision 0.')
        cards790[fid+'_X0']=(f'Historical record REVISION 0 (superseded): {work} '
                              f'collaborates_with {decoy}. Valid at revision 0 only.')
    for cid,body in sorted(cards790.items()):physical_commit(cid,body)
    gate790('PHYSICAL_28_CARTRIDGES',len(entries)==28,len(entries))
    gate790('MANIFEST_AFTER_28',MANIFEST.exists() and len(json.loads(MANIFEST.read_text())['cartridges'])==28)
    # Small paired audit, NOT a re-run of all 48 TEST789 cases.
    # Two families x two scenarios x two views = 8 observation pairs.
    for fam in families[:2]:
        fid=fam['id'];work=next(c['work'] for c in CASES if c['family']==fid)
        for scenario,pair in [('BASELINE',[fid+'_B0',fid+'_B1']),
                              ('SAME_REV_CONFLICT',[fid+'_B1',fid+'_X1'])]:
            hashes={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in pair}
            mems={}
            try:
                for arm,order in [('FORWARD',pair),('REVERSE',list(reversed(pair)))]:
                    mem,active,_,_=build_fusion(order,'TEST790_'+fid+'_'+scenario+'_'+arm,True)
                    gate790('NATIVE_80_'+fid+'_'+scenario+'_'+arm,len(mem)==80)
                    gate790('PAIR_ORDER_'+fid+'_'+scenario+'_'+arm,list(active)==order)
                    mems[arm]={'mem':mem,'spans':spans790(order,mem),'seal':memory_seals(mem)}
                for view in VIEWS:
                    q=CUE[view].format(work=work)
                    observations={}
                    for arm in ('FORWARD','REVERSE'):
                        m=mems[arm];state,att=observe_state(m['mem'],q,m['spans'])
                        chosen,confidence,density=source_signal(att,m['spans'])
                        gate790('STATE_FINITE_'+fid+'_'+scenario+'_'+arm+'_'+view,
                                state.numel()==H and bool(torch.isfinite(state).all().item()))
                        out=free_generate(m['mem'],q,max_new=MAX_TOKENS,spans={'B0':(0,0),'B1':(0,0)})
                        observations[arm]={'raw':out['raw'],'parsed':parse789(out['raw']),
                            'state_norm':float(torch.linalg.vector_norm(state).item()),
                            'state_sha256':hashlib.sha256(state.detach().cpu().numpy().tobytes()).hexdigest(),
                            'attention':att,'density':density,'dominant_physical_slot':chosen,
                            'relative_density_gap':confidence}
                        del state
                    f=observations['FORWARD']['parsed'];r=observations['REVERSE']['parsed']
                    decision=decide789(f,r)  # baseline only; audit does NOT modify decision.
                    # Gold is evaluated strictly AFTER both observations and decision.
                    expected=fam['new_team'] if view=='CURRENT' else fam['old_team']
                    emit790({'family':fid,'scenario_OFFLINE':scenario,'view_OFFLINE':view,
                        'cartridges_OFFLINE':pair,'observations':observations,'decision789':decision,
                        'order_sensitive_OFFLINE':f!=r,'forward_correct_OFFLINE':f==expected,
                        'reverse_correct_OFFLINE':r==expected,'expected_OFFLINE':expected})
                for arm,m in mems.items():
                    gate790('KV_UNCHANGED_'+fid+'_'+scenario+'_'+arm,
                            compare_seals(m['seal'],memory_seals(m['mem'])))
            finally:
                mems.clear();gc.collect();release()
            for cid,h in hashes.items():gate790('SSD_SHA_UNCHANGED_'+cid,sha_file(CART_DIR/(cid+'.pt'))==h)
    gate790('TOTAL_CASES',len(R['rows'])==8,len(R['rows']))
    gate790('FROZEN_WEIGHTS',sentinel()==before790)
    gate790('FINAL_MANIFEST',MANIFEST.exists() and json.loads(MANIFEST.read_text()).get('panel_sha256')==PANEL_SHA)
    gate790('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
            not model.model.layers[CUT]._forward_pre_hooks)
    R['summary']={'n':len(R['rows']),
       'order_sensitive':sum(x['order_sensitive_OFFLINE'] for x in R['rows']),
       'forward_correct':sum(x['forward_correct_OFFLINE'] for x in R['rows']),
       'reverse_correct':sum(x['reverse_correct_OFFLINE'] for x in R['rows']),
       'scope':'TEST779/784 observation interface audited against native 72B CUT3; no closed-loop proof',
       'next_gate':'Correlate blind observation changes with held-out correction under controlled interventions'}
    R['status']='COMPLETE_RESULTS_RECORDED';save790()
    log('TEST790_COMPLETED',json.dumps(R['summary'],ensure_ascii=False));log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save790()
    log('TEST790_FAILED',repr(e));log(R['traceback']);raise
finally:save790()
