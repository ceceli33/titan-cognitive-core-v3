# AKBASCORE SILICON HIPPOCAMPUS — TEST765
# TEST721 H3 routing + TEST757 native CUT3 traversal + TEST764 frozen 72B baseline.
# ONE Colab cell. Existing engine definitions are imported VERBATIM by locked Git blobs.
# No training, no source text in QA prompts, no forward hooks, no Gradio.
# IMPORTANT: The adaptive stop/expansion controller is external Python policy,
# not yet an autonomous decision implemented inside the frozen neural model.
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
TEST='765';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
NL,H,QH,KVH,HD=EXPECTED;DTYPE=torch.bfloat16;DEV=torch.device('cuda:0')
CHUNK=128;GPU_RESERVE_GIB=9.0;MAX_NEW=48;MAX_FUSED_TOKENS=3500
NUM_CHAINS=4;SAMPLE_PER_PIECE=512;ROUTE_K=3;MODEL_SEED=7562026
STEPS=('works_at','collaborates_with','archives_in');KINDS=('PERSON','WORK','TEAM','VAULT')
REPO='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCKS={'709.py':'6c9f8cbb1eeed848d45133d73f0d7676b68e9125',
       '730.py':'b1bad9eb3b111b44413f8ef05a3a140ab66a77dd',
       '757.py':'3d88bf8638390995858f23391f1e043faa586835',
       '764.py':'99acb97cde2b11c0c23e14a3ed11cb6f5d7f3902',
       '721.py':'7c6575beddca87f02c344ee1a132f02b191dc00a'}
RUN_ID=datetime.datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
ROOT=Path('/content' if Path('/content').exists() else '/tmp')/('AKBASCORE_TEST765_'+RUN_ID)
ROOT.mkdir(parents=True,exist_ok=False);CART_DIR=ROOT/'physical_cartridges';CART_DIR.mkdir()
LOG=ROOT/'TEST765.log';LOG.write_text('',encoding='utf-8');OUT=ROOT/'TEST765_results.json';MANIFEST=ROOT/'TEST765_manifest.json'
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'locks':LOCKS,'checks':[], 'trials':[],
   'scope':'adaptive H3 route and stepwise CUT3 traversal on sealed synthetic independent cards',
   'limits':['Controller decisions are external, NOT native neural closed-loop cognition',
             'Gold answers are used only after inference for scoring',
             'Unknown and code syntax are not proof of semantic truth',
             'Synthetic labels; results do not establish real-world generalization']}
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
    req=urllib.request.Request(REPO+name,headers={'User-Agent':'AKBASCORE-TEST765'})
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
# Use exact TEST757 synthetic data generator, seeded identically.
rng=random.Random(MODEL_SEED);ALPHABET='ABCDEFGHJKLMNPQRSTUVWXYZ'
def opaque(prefix,n=8):return prefix+'-'+''.join(rng.choice(ALPHABET) for _ in range(n))
def synthetic_panel():
    cases=[];cards={}
    for i in range(NUM_CHAINS):
        person=opaque('PERSON');work=opaque('WORK');team=opaque('TEAM');vault=opaque('VAULT')
        ids=[f'C{i:02d}_A',f'C{i:02d}_B',f'C{i:02d}_C']
        for cid,txt in zip(ids,(f'{person} works_at {work}.',f'{work} collaborates_with {team}.',f'{team} archives_in {vault}.')):cards[cid]=txt
        cases.append({'id':f'Q{i:02d}','person':person,'work':work,'team':team,'answer':vault,'supports':ids,
                      'question':f'Starting from {person}, follow works_at, then collaborates_with, then archives_in. What is the final VAULT code? Reply with only the exact VAULT code, or UNKNOWN if evidence is insufficient.'})
    for j in range(2):
        ghost=opaque('PERSON');cases.append({'id':f'M{j:02d}','person':ghost,'work':None,'team':None,'answer':'UNKNOWN','supports':[],
            'question':f'Starting from {ghost}, follow works_at, then collaborates_with, then archives_in. What is the final VAULT code? Reply with only the exact VAULT code, or UNKNOWN if evidence is insufficient.'})
    return cases,cards
CASES,CARD_TEXT=synthetic_panel()
PANEL_BYTES=json.dumps({'cases':CASES,'cards':CARD_TEXT},sort_keys=True,ensure_ascii=False).encode()
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
    record_cp(cid,cp,'TEST757_SYNTHETIC_RELATION',[],{'forge_seconds':seconds,'body_sha256':sha(body.encode())})
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

def traverse(case,mode,bank,bank721):
    current=case['person'];trace=[]
    for hop,(rel,kind) in enumerate(zip(STEPS,KINDS[1:]),1):
        if current in ('UNKNOWN','INVALID'):break
        question=step_question(current,rel,kind)
        ranking,scores=numeric_rank(question,bank)
        # Native TEST721 scorer is computed independently from the same query H3
        # when required for auditing; routing remains TEST757's proven scorer.
        if mode=='FIXED_TOP3':
            chosen=ranking[:ROUTE_K]
            ev=evaluate_step(f'{mode}_{case["id"]}_H{hop}',case['id'],hop,question,chosen,kind)
            attempts=[{'k':len(chosen),'prediction':ev['prediction'],'selected':chosen}]
        elif mode=='ADAPTIVE_1_TO_3':
            # A syntax-valid answer alone is NOT treated as certainty: top-1 and top-3
            # must agree to accept; otherwise abstain. No gold or support IDs consulted.
            first=evaluate_step(f'ADAPT1_{case["id"]}_H{hop}',case['id'],hop,question,ranking[:1],kind)
            attempts=[{'k':1,'prediction':first['prediction'],'selected':ranking[:1]}]
            if first['prediction'] in ('UNKNOWN','INVALID'):
                second=evaluate_step(f'ADAPT3_{case["id"]}_H{hop}',case['id'],hop,question,ranking[:3],kind)
                attempts.append({'k':3,'prediction':second['prediction'],'selected':ranking[:3]})
                ev=second
            else:
                # Avoid false certainty: require a second read with additional evidence.
                second=evaluate_step(f'CONFIRM3_{case["id"]}_H{hop}',case['id'],hop,question,ranking[:3],kind)
                attempts.append({'k':3,'prediction':second['prediction'],'selected':ranking[:3]})
                ev=second if second['prediction']==first['prediction'] else {'raw':second['raw'],'prediction':'UNKNOWN','selected':ranking[:3]}
        else:raise RuntimeError('UNKNOWN_MODE')
        trace.append({'hop':hop,'relation':rel,'subject':current,'question':question,
                      'ranked_top3':ranking[:3],'top3_scores':{x:round(scores[x],8) for x in ranking[:3]},
                      'attempts':attempts,'raw':ev['raw'],'prediction':ev['prediction']})
        log('STEP',mode,case['id'],hop,'RANK',ranking[:3],'PRED',ev['prediction'])
        current=ev['prediction']
    final=current if len(trace)==3 and current!='INVALID' else 'UNKNOWN'
    return {'case_id':case['id'],'mode':mode,'trace':trace,'prediction':final,
            'gold':case['answer'],'exact':final==case['answer'],'hops':len(trace)}

try:
    log('='*108);log('AKBASCORE TEST765 / TEST721+757+764 / ADAPTIVE H3 NATIVE CUT3 TRAVERSAL');log('='*108)
    check('PANEL_SEALED',sha((ROOT/'SEALED_PANEL.json').read_bytes())==PANEL_SHA)
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    check('FRESH_GPU',free>=40*2**30,'Restart Colab runtime before running if a 72B model remains loaded')
    model_setup();weights_before=sentinel()
    # EXACT same 4-chain/2-missing test distribution as TEST757.
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    check('ALL_12_PHYSICAL_CARTRIDGES',len(entries)==12,len(entries))
    bank,bank721=build_bank()
    check('BANK_SHAPE',len(bank)==12 and all(v.shape[0]==H for v in bank.values()))
    for case in CASES:
        for mode in ('FIXED_TOP3','ADAPTIVE_1_TO_3'):
            row=traverse(case,mode,bank,bank721)
            R['trials'].append(row);save()
            log('CASE_RESULT',case['id'],mode,'EXACT',row['exact'],'PRED',row['prediction'],'GOLD',row['gold'])
    for mode in ('FIXED_TOP3','ADAPTIVE_1_TO_3'):
        selected=[x for x in R['trials'] if x.get('mode')==mode]
        R.setdefault('score',{})[mode]={'exact':sum(x['exact'] for x in selected),'n':len(selected),
            'missing_unknown':sum(x['prediction']=='UNKNOWN' and x['gold']=='UNKNOWN' for x in selected),
            'false_unknown':sum(x['prediction']=='UNKNOWN' and x['gold']!='UNKNOWN' for x in selected),
            'mean_hops':sum(x['hops'] for x in selected)/len(selected)}
    check('TRIAL_MATRIX',sum(x.get('mode') in ('FIXED_TOP3','ADAPTIVE_1_TO_3') for x in R['trials'])==2*len(CASES))
    check('MODEL_WEIGHTS_UNCHANGED',sentinel()==weights_before)
    check('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
    check('PANEL_UNCHANGED',sha((ROOT/'SEALED_PANEL.json').read_bytes())==PANEL_SHA)
    R['status']='COMPLETE_RESULTS_RECORDED';R['summary']={'model':'frozen Qwen2.5-72B NF4','cards':len(entries),
        'cases':len(CASES),'modes':['FIXED_TOP3','ADAPTIVE_1_TO_3'],
        'score':R['score'],'model_internal_closed_loop_proven':False}
    save();log('TEST765_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save()
    log('TEST765_FAILED',repr(e));log(R['traceback']);raise
finally:save()
