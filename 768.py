# AKBASCORE SILICON HIPPOCAMPUS — TEST768
# Locked GPU-proven TEST767 backbone; same sealed 20-card panel; frozen 72B native CUT3.
# ONE Colab cell. Existing engine definitions are imported VERBATIM by locked Git blobs.
# No training, no source text in QA prompts, no forward hooks, no Gradio.
# TEST768 isolates one-time fusion versus per-query rebuilding.
# It does NOT modify native attention or prove model-internal autonomy.
# Static syntax verified; NOT GPU executed by author.
import os,sys,subprocess,importlib.util,urllib.request,hashlib,json,ast,time,random,re,gc,traceback,types,datetime
from pathlib import Path
from datetime import timezone
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF','expandable_segments:True')
for mod,pkg in [('torch','torch'),('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50'),('numpy','numpy')]:
    if importlib.util.find_spec(mod) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',pkg])
import torch,transformers,bitsandbytes,numpy as np
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
if not torch.cuda.is_available() or torch.cuda.device_count()!=1:raise RuntimeError('ONE_CUDA_GPU_REQUIRED')
GPU_INFO=torch.cuda.get_device_properties(0)
if 'A100' not in GPU_INFO.name or GPU_INFO.total_memory<70*2**30:raise RuntimeError('A100_80GB_REQUIRED')
TEST='768';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
NL,H,QH,KVH,HD=EXPECTED;DTYPE=torch.bfloat16;DEV=torch.device('cuda:0')
CHUNK=128;GPU_RESERVE_GIB=9.0;MAX_NEW=48;MAX_FUSED_TOKENS=3500
NUM_CHAINS=4;SAMPLE_PER_PIECE=512;ROUTE_K=3;MODEL_SEED=7662026
STEPS=('works_at','collaborates_with','archives_in');KINDS=('PERSON','WORK','TEAM','VAULT')
REPO='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCKS={'709.py':'6c9f8cbb1eeed848d45133d73f0d7676b68e9125',
       '730.py':'b1bad9eb3b111b44413f8ef05a3a140ab66a77dd',
       '757.py':'3d88bf8638390995858f23391f1e043faa586835',
       '764.py':'99acb97cde2b11c0c23e14a3ed11cb6f5d7f3902',
       '721.py':'7c6575beddca87f02c344ee1a132f02b191dc00a'}
RUN_ID=datetime.datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
ROOT=Path('/content' if Path('/content').exists() else '/tmp')/('AKBASCORE_TEST768_'+RUN_ID)
ROOT.mkdir(parents=True,exist_ok=False);CART_DIR=ROOT/'physical_cartridges';CART_DIR.mkdir()
LOG=ROOT/'TEST768.log';LOG.write_text('',encoding='utf-8');OUT=ROOT/'TEST768_results.json';MANIFEST=ROOT/'TEST768_manifest.json'
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'locks':LOCKS,'checks':[], 'trials':[],
   'scope':'TEST767 locked physical temporal pairs: once-built GPU-resident fusion vs per-query rebuild; measured latency and correctness',
   'limits':['Pair selection is an oracle diagnostic; NOT autonomous routing',
             'Gold answers are used only after inference for scoring',
             'Unknown and code syntax are not proof of semantic truth',
             'Synthetic labels; results do not establish real-world generalization',
             'No custom attention kernel or neural self-correction is claimed',
             'Wall-clock includes CPU overhead; CUDA events measure GPU stream elapsed time only',
             'Reuses TEST766 synthetic panel; NOT a held-out generalization test',
             'The 0.12 score bias is arbitrary and external; compare to unbiased baseline']}
entries={}
def log(*x):
    s=' '.join(map(str,x));print(s,flush=True)
    with LOG.open('a',encoding='utf-8') as f:f.write(s+'\n')
def save():
    p=Path(str(OUT)+'.tmp');p.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding='utf-8');p.replace(OUT)
def check(name,ok,detail=None):
    R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});save();log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('CHECK_FAILED:'+name)
def sha(b):return hashlib.sha256(b).hexdigest()
def sha_file(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def gitblob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def fetch_locked(name):
    req=urllib.request.Request(REPO+name,headers={'User-Agent':'AKBASCORE-TEST768'})
    with urllib.request.urlopen(req,timeout=180) as r:b=r.read(600001)
    check('SOURCE_SIZE_'+name,len(b)<=600000,len(b));check('GIT_LOCK_'+name,gitblob(b)==LOCKS[name],gitblob(b))
    return b
def extract_exact(b,names,label):
    tree=ast.parse(b.decode('utf-8'),filename=label)
    found={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and n.name in names}
    check('SYMBOLS_'+label,set(found)==set(names),sorted(set(names)-set(found)))
    mod=ast.Module(body=[found[n] for n in names],type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod),label,'exec'),globals())
def persist_manifest():
    tmp=Path(str(MANIFEST)+'.tmp')
    tmp.write_text(json.dumps({'test':TEST,'locks':LOCKS,'panel_sha256':R['panel_sha256'],'cartridges':entries},ensure_ascii=False,indent=2,default=str))
    tmp.replace(MANIFEST)
# Seal panel BEFORE model loading or physical cartridge creation.
# New temporal panel, old motor functions imported unchanged.
rng=random.Random(MODEL_SEED);ALPHABET='ABCDEFGHJKLMNPQRSTUVWXYZ'
def opaque(prefix,n=8):return prefix+'-'+''.join(rng.choice(ALPHABET) for _ in range(n))
def synthetic_panel():
    # Four disjoint chains. The middle edge has an old superseded value and a
    # later authoritative replacement; both versions remain on SSD.
    # Each destination has its own independent vault card.
    cases=[];cards={};families=[]
    for i in range(NUM_CHAINS):
        person=opaque('PERSON');work=opaque('WORK')
        oldteam=opaque('TEAM');newteam=opaque('TEAM')
        oldvault=opaque('VAULT');newvault=opaque('VAULT')
        base=f'C{i:02d}'
        card_ids=[base+'_A',base+'_B0',base+'_B1',base+'_C0',base+'_C1']
        cards[card_ids[0]]=f'{person} works_at {work}.'
        cards[card_ids[1]]=(f'Historical record REVISION 0 (superseded): {work} '
                            f'collaborates_with {oldteam}. Valid at revision 0 only.')
        cards[card_ids[2]]=(f'Authoritative CURRENT record REVISION 1: {work} '
                            f'collaborates_with {newteam}. Supersedes revision 0.')
        cards[card_ids[3]]=f'{oldteam} archives_in {oldvault}.'
        cards[card_ids[4]]=f'{newteam} archives_in {newvault}.'
        families.append({'id':base,'old_team':oldteam,'new_team':newteam,
                         'old_vault':oldvault,'new_vault':newvault,'cards':card_ids})
        for view,answer in [('CURRENT',newvault),('HISTORICAL',oldvault)]:
            cases.append({'id':f'Q{i:02d}_{view}', 'person':person,'work':work,
                          'view':view,'answer':answer,'family':base,
                          'question':f'Starting from {person}, follow works_at, '
                          f'then collaborates_with, then archives_in. '
                          f'Use {"only the latest authoritative revision 1" if view=="CURRENT" else "the historical revision 0"} '
                          f'for collaborates_with. What is the final VAULT code? '
                          f'Reply with only the exact VAULT code, or UNKNOWN if evidence is insufficient.'})
    for j in range(2):
        ghost=opaque('PERSON')
        cases.append({'id':f'M{j:02d}','person':ghost,'work':None,
                      'view':'CURRENT','answer':'UNKNOWN','family':None,
                      'question':f'Starting from {ghost}, follow works_at, '
                      'then collaborates_with using the latest authoritative revision, '
                      'then archives_in. Return only the VAULT code or UNKNOWN.'})
    return cases,cards,families
CASES,CARD_TEXT,FAMILIES=synthetic_panel()
PANEL_BYTES=json.dumps({'cases':CASES,'cards':CARD_TEXT,'families':FAMILIES},sort_keys=True,ensure_ascii=False).encode()
PANEL_SHA=sha(PANEL_BYTES);(ROOT/'SEALED_PANEL.json').write_bytes(PANEL_BYTES)
R['panel_sha256']=PANEL_SHA;save()
# Exact locked engine functions. TEST721 routing is recovered via its native score and H3 capture,
# TEST757 provides proven 3-hop traversal, physical append and score-compatible formatting.
raw709=fetch_locked('709.py');raw730=fetch_locked('730.py');raw757=fetch_locked('757.py')
raw721=fetch_locked('721.py');raw764=fetch_locked('764.py')
extract_exact(raw709,['pairs','cache_build','replace','half','rope','rephase','sentinel','free_gpu','ensure_room',
                      'kv_digest','full_kv_seal','answer','mem'],'709.py')
extract_exact(raw730,['DirectCut3','forge_native','initialize_native','to_gpu','seal_cp',
                      'memory_seals','compare_seals','safe_load','release'],'730.py')
extract_exact(raw757,['native_append_direct','load_verified','build_fusion','answer_fused','run_arm',
                      'normalized','exact_value','query_native','numeric_rank','step_question','read_exact','model_setup'],'757.py')
# Import the TEST721 exact routing scorer as a provenance control (same TOP2 rule).
extract_exact(raw721,['native_score','route'],'721.py')
# Import only the TEST764 working disk commit and manifest helpers, not its AIN experiment.
extract_exact(raw764,['record_cp'],'764.py')
check('ENGINE_DEPENDENCIES',all(callable(globals().get(k)) for k in
      ('forge_native','initialize_native','native_append_direct','build_fusion','run_arm','query_native','numeric_rank','route','model_setup','record_cp')))

def physical_commit(cid,body):
    ids=tok(body,add_special_tokens=False).input_ids
    check('CARD_NONEMPTY_'+cid,len(ids)>4,len(ids))
    cp,seconds=forge_native(ids,cid)
    record_cp(cid,cp,'TEST768_TEMPORAL_RELATION',[],{'forge_seconds':seconds,'body_sha256':sha(body.encode())})
    del cp;release()

def build_bank():
    bank={};bank721={}
    for cid in sorted(entries):
        cp=safe_load(entries[cid]);x=cp['h'][0,P:,:].float().cpu().numpy()
        ix=np.linspace(0,len(x)-1,min(SAMPLE_PER_PIECE,len(x)),dtype=np.int64)
        bank[cid]=normalized(x[ix]).T.copy();bank721[cid]=normalized(x[ix])
        del cp
    return bank,bank721

def evaluate_step(label,cid,hop,question,ids,kind):
    if not ids:return {'raw':'UNKNOWN','prediction':'UNKNOWN','selected':[]}
    trial=run_arm(label,ids,[{'id':cid+'_'+str(hop),'question':question}],strict_sha=True)
    raw=trial['answers'][0]['raw'];return {'raw':raw,'prediction':read_exact(raw,kind),'selected':list(ids)}

# TEST768: SAME SEALED B0/B1 PAIR, SAME FUSION ORDER, only query cue changes.
# Direct-pair tests are diagnostic upper bounds, NOT evidence of successful autonomous routing.
# Routing tests separately report unmodified H3 and metadata-biased candidate ranking.
# No gold labels, answer values or support IDs are used by the H3 ranking or bias.
# The family identifier is used only to select a controlled pair for the causal diagnostic.
CUE={
 'NEUTRAL':'Using the available document memory, for {work} find collaborates_with. Return ONLY its exact TEAM code or UNKNOWN.',
 'CURRENT':'Using the available document memory, for {work} find collaborates_with in the latest authoritative revision 1. Ignore superseded revision 0. Return ONLY its exact TEAM code or UNKNOWN.',
 'HISTORICAL':'Using the available document memory, for {work} find collaborates_with in historical revision 0, not revision 1. Return ONLY its exact TEAM code or UNKNOWN.'}
def read_pair(label,ids,q):
    row=run_arm(label,ids,[{'id':label,'question':q}],strict_sha=True)
    raw=row['answers'][0]['raw']
    return {'raw':raw,'prediction':read_exact(raw,'TEAM'),'selected':list(ids)}

# TEST768: unchanged native build_fusion / answer_fused engines, but KEEP fused KV
# GPU-resident while changing only the query. Rebuild baseline uses identical
# pair and exact question, with fresh native fusion per trial.
# No routing, metadata score modification, custom CUDA kernel or model training.
# CUDA event time is NOT interpreted as isolated attention kernel time.
REPEATS=3
VIEWS=('CURRENT','HISTORICAL','NEUTRAL')
R['observations']=[]
R['timing']={}
save()

def synchronized_measure(fn):
    torch.cuda.synchronize()
    start=torch.cuda.Event(enable_timing=True);end=torch.cuda.Event(enable_timing=True)
    wall0=time.perf_counter();start.record()
    result=fn()
    end.record();torch.cuda.synchronize()
    return result,{'wall_ms':round((time.perf_counter()-wall0)*1000,3),
                   'cuda_stream_ms':round(start.elapsed_time(end),3)}

def answer_once(mem,question):
    raw,t=synchronized_measure(lambda:answer_fused(mem,question))
    return {'raw':raw,'prediction':read_exact(raw,'TEAM'),**t}

def record(fid,view,arm,iteration,ids,question,gold,answer_row,build_t=None):
    row={'family':fid,'view':view,'arm':arm,'iteration':iteration,
         'selected':list(ids),'question_sha256':sha(question.encode()),
         'prediction':answer_row['prediction'],'raw':answer_row['raw'],
         'gold':gold,'correct':None if gold is None else answer_row['prediction']==gold,
         'answer_wall_ms':answer_row['wall_ms'],
         'answer_cuda_stream_ms':answer_row['cuda_stream_ms']}
    if build_t is not None:row.update({'build_wall_ms':build_t['wall_ms'],
                                      'build_cuda_stream_ms':build_t['cuda_stream_ms'],
                                      'total_wall_ms':round(build_t['wall_ms']+answer_row['wall_ms'],3)})
    R['observations'].append(row);save()
    log('OBS',fid,view,arm,'ITER',iteration,'PRED',row['prediction'],
        'GOLD',gold,'ANSWER_WALL_MS',row['answer_wall_ms'],
        'BUILD_WALL_MS',row.get('build_wall_ms','REUSED'))
    return row

def run_family(fam):
    fid=fam['id'];pair=[fid+'_B0',fid+'_B1']
    case=next(c for c in CASES if c['family']==fid)
    questions={view:CUE[view].format(work=case['work']) for view in VIEWS}
    golds={'CURRENT':fam['new_team'],'HISTORICAL':fam['old_team'],'NEUTRAL':None}
    sha_before={cid:sha_file(CART_DIR/(cid+'.pt')) for cid in pair}
    # Baseline: SAME exact pair, fresh fusion for each question, no cached state.
    for view in VIEWS:
        label='REBUILD_'+fid+'_'+view
        pack,build_t=synchronized_measure(lambda:build_fusion(pair,label,True))
        mem,active,steps,build_s=pack
        try:
            check('REBUILD_ACTIVE_'+fid+'_'+view,list(active)==pair,list(active))
            before=memory_seals(mem)
            ans=answer_once(mem,questions[view])
            check('REBUILD_MEM_IMMUTABLE_'+fid+'_'+view,
                  compare_seals(before,memory_seals(mem)))
            record(fid,view,'REBUILD',0,pair,questions[view],golds[view],ans,build_t)
        finally:
            del mem,pack;release()
    # Once-built fused memory, same order, no changes between temporal queries.
    label='RESIDENT_'+fid
    pack,build_t=synchronized_measure(lambda:build_fusion(pair,label,True))
    mem,active,steps,build_s=pack
    try:
        check('RESIDENT_ACTIVE_'+fid,list(active)==pair,list(active))
        sealed=memory_seals(mem)
        R['timing'][fid]={'resident_build_wall_ms':build_t['wall_ms'],
                          'resident_build_cuda_stream_ms':build_t['cuda_stream_ms'],
                          'resident_memory_tokens':int(mem[0][0].shape[-2]) if isinstance(mem,(tuple,list)) else None}
        save()
        # All 3 time views interleaved, repeated on unchanged physical GPU memory.
        # Repetition also checks state leakage across distinct queries.
        for iteration in range(REPEATS):
            for view in VIEWS:
                ans=answer_once(mem,questions[view])
                record(fid,view,'RESIDENT',iteration,pair,questions[view],golds[view],ans)
        check('RESIDENT_MEM_IMMUTABLE_'+fid,compare_seals(sealed,memory_seals(mem)))
    finally:
        del mem,pack;release()
    for cid in pair:
        check('PAIR_SHA_UNCHANGED_'+fid+'_'+cid,
              sha_file(CART_DIR/(cid+'.pt'))==sha_before[cid]==entries[cid]['sha256'])

def stats(values):
    if not values:return None
    v=sorted(float(x) for x in values)
    return {'n':len(v),'min_ms':round(v[0],3),
            'median_ms':round(float(np.median(v)),3),
            'p95_ms':round(float(np.percentile(v,95)),3),
            'max_ms':round(v[-1],3)}

def summarize():
    out={}
    for arm in ('REBUILD','RESIDENT'):
        rows=[x for x in R['observations'] if x['arm']==arm]
        scored=[x for x in rows if x['gold'] is not None]
        out[arm]={'correct':sum(x['correct'] for x in scored),'n':len(scored),
                  'current_correct':sum(x['correct'] for x in scored if x['view']=='CURRENT'),
                  'historical_correct':sum(x['correct'] for x in scored if x['view']=='HISTORICAL'),
                  'answer_wall_ms':stats(x['answer_wall_ms'] for x in rows),
                  'answer_cuda_stream_ms':stats(x['answer_cuda_stream_ms'] for x in rows)}
        if arm=='REBUILD':
            out[arm]['build_wall_ms']=stats(x['build_wall_ms'] for x in rows)
            out[arm]['total_wall_ms']=stats(x['total_wall_ms'] for x in rows)
    out['RESIDENT']['one_time_build_wall_ms']=stats(x['resident_build_wall_ms'] for x in R['timing'].values())
    return out

try:
    log('='*108)
    log('AKBASCORE TEST768 / ONCE-BUILT GPU-RESIDENT CUT3 / QUERY SWITCH / CUDA TIMING')
    log('='*108)
    check('PANEL_SEALED',sha((ROOT/'SEALED_PANEL.json').read_bytes())==PANEL_SHA)
    free,_=torch.cuda.mem_get_info()
    log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    check('FRESH_GPU',free>=40*2**30,'Restart Colab runtime if 72B already loaded')
    model_setup();weights_before=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    check('ALL_20_PHYSICAL_CARTRIDGES',len(entries)==20,len(entries))
    for fam in FAMILIES:run_family(fam)
    expected=NUM_CHAINS*len(VIEWS)*(1+REPEATS)
    check('OBSERVATION_MATRIX',len(R['observations'])==expected,len(R['observations']))
    check('MODEL_WEIGHTS_UNCHANGED',sentinel()==weights_before)
    check('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and
          not model.model.layers[CUT]._forward_pre_hooks)
    check('PANEL_UNCHANGED',sha((ROOT/'SEALED_PANEL.json').read_bytes())==PANEL_SHA)
    score=summarize();R['score']=score
    R['status']='COMPLETE_RESULTS_RECORDED'
    R['summary']={'model':'frozen Qwen2.5-72B NF4',
                  'cards':len(entries),'pairs':NUM_CHAINS,'resident_repeats':REPEATS,
                  'score':score,'model_internal_closed_loop_proven':False,
                  'native_new_kernel_proven':False,
                  'interpretation':'Native proven CUT3 fusion reused on GPU; oracle pair diagnostic. '
                                   'CUDA events cover scheduled GPU stream work, not pure attention. '
                                   'No inference that arbitrary retrieval or true autonomy is solved.'}
    save();log('TEST768_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save()
    log('TEST768_FAILED',repr(e));log(R['traceback']);raise
finally:save()
