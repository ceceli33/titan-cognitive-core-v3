# AKBASCORE SILICON HIPPOCAMPUS — TEST766
# Locked TEST765 backbone; temporal conflict panel; frozen 72B native CUT3.
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
TEST='766';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
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
ROOT=Path('/content' if Path('/content').exists() else '/tmp')/('AKBASCORE_TEST766_'+RUN_ID)
ROOT.mkdir(parents=True,exist_ok=False);CART_DIR=ROOT/'physical_cartridges';CART_DIR.mkdir()
LOG=ROOT/'TEST766.log';LOG.write_text('',encoding='utf-8');OUT=ROOT/'TEST766_results.json';MANIFEST=ROOT/'TEST766_manifest.json'
R={'test':TEST,'status':'STARTED','run_id':RUN_ID,'locks':LOCKS,'checks':[], 'trials':[],
   'scope':'temporal contradiction and revision selection on sealed physical CUT3 memory cards',
   'limits':['Controller decisions are external, NOT native neural closed-loop cognition',
             'Gold answers are used only after inference for scoring',
             'Unknown and code syntax are not proof of semantic truth',
             'Synthetic labels; results do not establish real-world generalization',
             'Temporal selection is prompted; native self-correction is NOT demonstrated',
             'A model output may be syntactically valid yet historically wrong']}
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
    req=urllib.request.Request(REPO+name,headers={'User-Agent':'AKBASCORE-TEST766'})
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
    record_cp(cid,cp,'TEST766_TEMPORAL_RELATION',[],{'forge_seconds':seconds,'body_sha256':sha(body.encode())})
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
        if rel=='collaborates_with':
            # User's time-scope is passed into the retrieval question, never
            # an expected entity or a gold card identifier.
            temporal=('latest authoritative revision 1, NOT superseded revision 0'
                      if case['view']=='CURRENT' else
                      'historical revision 0, NOT revision 1')
            question=question.replace('Return ONLY',
                        'Select the '+temporal+'. Return ONLY')
        ranking,scores=numeric_rank(question,bank)
        # Native TEST721 scorer is computed independently from the same query H3
        # when required for auditing; routing remains TEST757's proven scorer.
        if mode in ('FIXED_TOP3','EXPANDED_TOP8'):
            chosen=ranking[:(ROUTE_K if mode=='FIXED_TOP3' else 8)]
            ev=evaluate_step(f'{mode}_{case["id"]}_H{hop}',case['id'],hop,question,chosen,kind)
            attempts=[{'k':len(chosen),'prediction':ev['prediction'],'selected':chosen}]
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
    log('='*108);log('AKBASCORE TEST766 / TEMPORAL CONFLICT / H3 NATIVE CUT3 REVISION SELECTION');log('='*108)
    check('PANEL_SEALED',sha((ROOT/'SEALED_PANEL.json').read_bytes())==PANEL_SHA)
    free,_=torch.cuda.mem_get_info();log('GPU_PREFLIGHT_FREE_GIB',round(free/2**30,2))
    check('FRESH_GPU',free>=40*2**30,'Restart Colab runtime before running if a 72B model remains loaded')
    model_setup();weights_before=sentinel()
    # 4 paired old/current chains + 2 missing controls; no oracle routing.
    for cid,body in sorted(CARD_TEXT.items()):physical_commit(cid,body)
    check('ALL_20_PHYSICAL_CARTRIDGES',len(entries)==20,len(entries))
    bank,bank721=build_bank()
    check('BANK_SHAPE',len(bank)==20 and all(v.shape[0]==H for v in bank.values()))
    for case in CASES:
        for mode in ('FIXED_TOP3','EXPANDED_TOP8'):
            row=traverse(case,mode,bank,bank721)
            R['trials'].append(row);save()
            log('CASE_RESULT',case['id'],mode,'EXACT',row['exact'],'PRED',row['prediction'],'GOLD',row['gold'])
    for mode in ('FIXED_TOP3','EXPANDED_TOP8'):
        selected=[x for x in R['trials'] if x.get('mode')==mode]
        R.setdefault('score',{})[mode]={'exact':sum(x['exact'] for x in selected),'n':len(selected),
            'missing_unknown':sum(x['prediction']=='UNKNOWN' and x['gold']=='UNKNOWN' for x in selected),
            'false_unknown':sum(x['prediction']=='UNKNOWN' and x['gold']!='UNKNOWN' for x in selected),
            'mean_hops':sum(x['hops'] for x in selected)/len(selected),
            'current_correct':sum(x['exact'] for x in selected if x['case_id'].endswith('_CURRENT')),
            'historical_correct':sum(x['exact'] for x in selected if x['case_id'].endswith('_HISTORICAL')),
            'current_total':NUM_CHAINS,'historical_total':NUM_CHAINS}
    check('TRIAL_MATRIX',sum(x.get('mode') in ('FIXED_TOP3','EXPANDED_TOP8') for x in R['trials'])==2*len(CASES))
    check('MODEL_WEIGHTS_UNCHANGED',sentinel()==weights_before)
    check('NO_RESIDUAL_HOOKS',not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
    check('PANEL_UNCHANGED',sha((ROOT/'SEALED_PANEL.json').read_bytes())==PANEL_SHA)
    R['status']='COMPLETE_RESULTS_RECORDED';R['summary']={'model':'frozen Qwen2.5-72B NF4','cards':len(entries),
        'cases':len(CASES),'modes':['FIXED_TOP3','EXPANDED_TOP8'],
        'score':R['score'],'model_internal_closed_loop_proven':False,'contradiction_resolution_proven':False,
        'limitations':'Temporal prompt conditioning and external step controller; independent semantic review required'}
    save();log('TEST766_COMPLETED',json.dumps(R['summary'],ensure_ascii=False))
    log('FILES',OUT,LOG,MANIFEST)
except Exception as e:
    R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc();save()
    log('TEST766_FAILED',repr(e));log(R['traceback']);raise
finally:save()
