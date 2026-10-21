# AKBASCORE SILICON HIPPOCAMPUS — TEST738
# Hierarchical latent synthesis, physical C01+C02 -> S01, controlled retrieval.
# One Colab cell, A100 80GB, Qwen2.5-72B-Instruct NF4, CUT3.
# Uses SHA-locked working TEST709 and TEST730 function definitions, NOT their demos.
# STATIC VALIDATION ONLY: not executed on A100 by code author.
import os,sys,ast,hashlib,json,time,random,traceback,gc,urllib.request,subprocess,importlib.util,types
from pathlib import Path
from io import BytesIO
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF','expandable_segments:True')
for module,package in [('torch','torch'),('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50')]:
    if importlib.util.find_spec(module) is None:
        subprocess.check_call([sys.executable,'-m','pip','install','-q',package])
import torch,transformers,bitsandbytes
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
ROOT738=Path('/content/AKBASCORE_TEST738' if Path('/content').exists() else '/tmp/AKBASCORE_TEST738')
ROOT738.mkdir(parents=True,exist_ok=True)
CART738=ROOT738/'cartridges';CART738.mkdir(exist_ok=True)
LOG738=ROOT738/'TEST738.log';OUT738=ROOT738/'TEST738_results.json'
LOG738.write_text('',encoding='utf-8')
TEST='738';CUT=3;EXPECTED=(80,8192,64,8,128);MODEL_ID='Qwen/Qwen2.5-72B-Instruct'
DEV=torch.device('cuda:0');DTYPE=torch.bfloat16;CHUNK=128;GPU_RESERVE_GIB=8.0;MAX_NEW=48
URL709='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/709.py'
URL730='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/730.py'
GIT709='6c9f8cbb1eeed848d45133d73f0d7676b68e9125'
SHA730='c8dfa5bc7735ad2e00bd1b0141c7f0dc6af7cfb7232747e3bbf5b9a26f70dfaf'
T738={'test':TEST,'status':'STARTED','model':MODEL_ID,'cut':CUT,'cases':[], 'arms':{},
 'limitations':['Synthetic relational panel, not real forensic documents',
 'S01 uses frozen numeric CUT3/KV cartridges and a fixed focus-input forward pass; no model-generated prose is used to form S01',
 'Concatenated lower-layer caches do not retroactively cross-attend; cross-source interaction occurs in later causal computation and focus tokens',
 'Correct retrieval alone is not proof of novel scientific synthesis',
 'No GPU execution by author; bit-exact parity is a runtime acceptance condition']}
def say(*a):
    s=' '.join(map(str,a));print(s,flush=True)
    with LOG738.open('a',encoding='utf-8') as f:f.write(s+'\n')
def save():
    tmp=OUT738.with_suffix('.tmp');tmp.write_text(json.dumps(T738,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(OUT738)
def ck(name,condition,detail=None):
    say('PASS' if condition else 'FAIL',name,detail if detail is not None else '')
    if not condition:raise RuntimeError('TEST738_'+name)
def sha(b):return hashlib.sha256(b).hexdigest()
def gitblob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST738'}),timeout=120) as r:return r.read(500000)
def release():gc.collect();torch.cuda.empty_cache()
def log(*a):say(*a)
def check(name,ok,detail=None):ck(name,ok,detail)
def atomic_json(path,obj):
    tmp=Path(str(path)+'.tmp');tmp.write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str));tmp.replace(path)
def sha_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
def extract(raw,names,filename):
    tree=ast.parse(raw.decode('utf-8'));found={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names}
    ck('LOCKED_SYMBOLS_'+filename,set(found)==set(names),sorted(set(names)-set(found)))
    mod=ast.Module(body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names],type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod),filename,'exec'),globals())
# Fixed, sealed question panel BEFORE model load; no favorable case selection.
rng=random.Random(7382026)
people=['Nera','Varo','Miro','Sela','Tavin','Ruma','Kira','Sora','Orin','Mira','Leto','Vela']
objects=['violet','copper','cedar','slate','amber','silver','indigo','quartz','onyx','coral','ivory','bronze']
places=['Arden','Boreal','Cobalt','Dorian','Eldrin','Fennel','Garnet','Helios','Indigo','Juniper','Kestrel','Linden']
perm=list(range(12));rng.shuffle(perm)
# C01: person->object, C02: object->place. Both required to answer person->place.
source1='\n'.join(f'{p} owns the {o} instrument.' for p,o in zip(people,objects))
source2='\n'.join(f'The {o} instrument is stored in {places[perm[i]]}.' for i,o in enumerate(objects))
# Decoy has the same form and length class but assigns different places.
source_decoy='\n'.join(f'The {o} instrument is stored in {places[perm[(i+1)%12]]}.' for i,o in enumerate(objects))
# One uninformative question-free focus input; it is NOT a generated synthesis text.
FOCUS738='\nSYNTHESIS FOCUS: Integrate the available relations. Preserve source-specific links, distinguish unsupported connections, and prepare to answer later questions.\n'
PANEL738=[]
for i,p in enumerate(people):
    correct=places[perm[i]];other=places[perm[(i+3)%12]]
    # Counterbalance labels. Both answer choices appear in the query, not the source.
    gold='A' if i%2==0 else 'B'
    a,b=(correct,other) if gold=='A' else (other,correct)
    PANEL738.append({'id':f'Q{i:02d}','question':f'Where is the instrument owned by {p} stored?', 'A':a,'B':b,'gold':gold})
PANEL_SHA738=sha(json.dumps(PANEL738,sort_keys=True,separators=(',',':')).encode())
(ROOT738/'sealed_panel.json').write_text(json.dumps(PANEL738,indent=2),encoding='utf-8')
T738['panel_sha256']=PANEL_SHA738;T738['source_sha256']={'C01':sha(source1.encode()),'C02':sha(source2.encode()),'DECOY':sha(source_decoy.encode())}
save()
# Locked TEST709 functions (including tested append/rephase/cache semantics).
NAMES709={'pairs','cache_build','replace','half','rope','rephase','sentinel','free_gpu','ensure_room','kv_digest','full_kv_seal','append','mem'}
# TEST730 functions, without executing its 80GB demo/source downloads.
NAMES730={'DirectCut3','forge_native','initialize_native','to_gpu','seal_cp'}
@torch.no_grad()
def save_cp(cid,cp,parents):
    ck('CP_SHAPE_'+cid,cp['h'].shape==(1,cp['n'],H) and len(cp['lower'])==CUT+1)
    path=CART738/(cid+'.pt');tmp=Path(str(path)+'.tmp');torch.save(cp,tmp);tmp.replace(path)
    meta={'id':cid,'file':path.name,'sha256':sha_file(path),'tensor_sha':seal_cp(cp),'parents':parents,'n':cp['n']}
    T738['cartridges'][cid]=meta;save();say('SEALED_CARTRIDGE',cid,meta['sha256'],'tokens',cp['n'])
    return meta
@torch.no_grad()
def load_cp(cid):
    e=T738['cartridges'][cid];path=CART738/e['file']
    ck('DISK_SHA_'+cid,sha_file(path)==e['sha256'])
    cp=torch.load(path,map_location='cpu',weights_only=True)
    ck('TENSOR_SHA_'+cid,seal_cp(cp)==e['tensor_sha'])
    return cp
@torch.no_grad()
def make_source(cid,body):
    ids=tok(body,add_special_tokens=False).input_ids
    cp,seconds=forge_native(ids,cid)
    save_cp(cid,cp,[]);del cp;release();say('SOURCE_FORGED',cid,'seconds',seconds)
@torch.no_grad()
def make_joint(cid,first,second,focus=True):
    # Load ONLY existing physical cartridges; no source text or model-produced summary.
    cpu1=load_cp(first);cpu2=load_cp(second)
    a=to_gpu(cpu1);b=to_gpu(cpu2);del cpu1,cpu2
    h=torch.cat((a['h'],b['h'][:,P:,:]),dim=1).contiguous()
    n=a['n']+b['n']-P
    memory=list(initialize_native(a))
    # 709.append() repairs RoPE of lower K and performs a genuine upper-layer forward.
    memory=append(memory,b)
    ck('JOINT_LENGTH_'+cid,len(memory)==NL and memory[0][0].shape[-2]==n)
    del a,b;release()
    if focus:
        ids=tok(FOCUS738,add_special_tokens=False).input_ids
        ck('FOCUS_NONEMPTY',len(ids)>0)
        capture=[];cache=cache_build(memory)
        with DirectCut3(model.model.layers[CUT],'capture',collector=capture):
            for st in range(0,len(ids),CHUNK):
                piece=ids[st:st+CHUNK];q=len(piece);ensure_room(q+512)
                pos=torch.arange(n+st,n+st+q,device=DEV)
                out=model(input_ids=torch.tensor([piece],device=DEV),past_key_values=cache,
                    attention_mask=torch.ones((1,n+st+q),device=DEV,dtype=torch.long),
                    position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
                cache=out.past_key_values;del out
        h=torch.cat([h]+[x.to(DEV) for x in capture],dim=1)
        n+=len(ids)
        del capture
        # Keep one owner of live KV; source 'memory' must be released before CPU export.
        del memory
        memory=list(pairs(cache));del cache
    cp={'h':h.detach().cpu().contiguous(),
        'lower':tuple((k.detach().cpu().contiguous(),v.detach().cpu().contiguous()) for k,v in memory[:CUT+1]),
        'n':n,'p':P,'body_tokens':n-P,'book_id':cid}
    ck('JOINT_H3_LENGTH_'+cid,cp['h'].shape==(1,n,H))
    save_cp(cid,cp,[first,second]);del cp,memory,h;release()
@torch.no_grad()
def read_scores(cid):
    cp=to_gpu(load_cp(cid));memory=initialize_native(cp)
    # Two single-token choices, prevalidated for this tokenizer.
    results=[]
    for row in PANEL738:
        suffix=('\nQUESTION:\n'+row['question']+'\nA: '+row['A']+'\nB: '+row['B']+
                '\nRespond with only A or B.\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n')
        ids=tok(suffix,add_special_tokens=False).input_ids
        oldn=cp['n'];ensure_room(len(ids)+256)
        cache=cache_build(memory)
        pos=torch.arange(oldn,oldn+len(ids),device=DEV)
        out=model(input_ids=torch.tensor([ids],device=DEV),past_key_values=cache,
            attention_mask=torch.ones((1,oldn+len(ids)),device=DEV,dtype=torch.long),
            position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
        logits=out.logits[0,-1,:].float()
        la=float(logits[AID738].item());lb=float(logits[BID738].item())
        pred='A' if la>lb else 'B' if lb>la else 'TIE'
        results.append({'id':row['id'],'pred':pred,'gold':row['gold'],'correct':pred==row['gold'],
                        'gold_margin':(la-lb) if row['gold']=='A' else (lb-la)})
        del out,cache,logits
    # Recheck lower/upper cache after read; answer() should not mutate memory in place.
    del memory,cp;release()
    return results
try:
    t0=time.perf_counter()
    ck('CUDA',torch.cuda.is_available())
    ck('ONE_GPU',torch.cuda.device_count()==1)
    gpu_name=torch.cuda.get_device_name(0);gpu_total=torch.cuda.get_device_properties(0).total_memory
    ck('A100_80GB',('A100' in gpu_name) and gpu_total>=70*2**30,gpu_name)
    raw709=fetch(URL709);raw730=fetch(URL730)
    ck('709_GIT_BLOB_LOCK',gitblob(raw709)==GIT709)
    ck('730_SHA256_LOCK',sha(raw730)==SHA730)
    extract(raw709,NAMES709,'709.py');extract(raw730,NAMES730,'730.py')
    tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
    PIDS=tok('<|im_start|>system\nUse only the available document memory for document-specific questions. If the evidence is missing, say UNKNOWN.\n<|im_end|>\n<|im_start|>user\nINFORMATION:\n',add_special_tokens=False).input_ids
    P=len(PIDS)
    a_ids=tok(' A',add_special_tokens=False).input_ids;b_ids=tok(' B',add_special_tokens=False).input_ids
    ck('LABELS_ONE_TOKEN',len(a_ids)==1 and len(b_ids)==1 and a_ids!=b_ids,(a_ids,b_ids))
    AID738,BID738=a_ids[0],b_ids[0]
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
    model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,
        device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
    for p in model.parameters():p.requires_grad_(False)
    cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads)
    KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
    ck('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,(NL,H,QH,KVH,HD))
    ck('FROZEN',all(not p.requires_grad for p in model.parameters()))
    ck('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
    before=sentinel();T738['cartridges']={};save()
    make_source('C01',source1);make_source('C02',source2);make_source('C03_DECOY',source_decoy)
    # S01 is formed from actual physical C01+C02, not re-forging combined text.
    make_joint('S01','C01','C02')
    make_joint('S01_REVERSE','C02','C01')
    make_joint('S01_DECOY','C01','C03_DECOY')
    for arm in ('S01','C01','C02','S01_REVERSE','S01_DECOY'):
        rows=read_scores(arm);correct=sum(x['correct'] for x in rows)
        T738['arms'][arm]={'correct':correct,'total':len(rows),'rows':rows,
                           'mean_gold_margin':sum(x['gold_margin'] for x in rows)/len(rows)}
        save();say('ARM_RESULT',arm,correct,'/',len(rows))
    ck('PANEL_UNCHANGED',sha(json.dumps(PANEL738,sort_keys=True,separators=(',',':')).encode())==PANEL_SHA738)
    for cid in T738['cartridges']:ck('FINAL_DISK_'+cid,sha_file(CART738/T738['cartridges'][cid]['file'])==T738['cartridges'][cid]['sha256'])
    ck('WEIGHTS_SENTINEL_UNCHANGED',sentinel()==before)
    s=T738['arms'];T738['paired']={arm:{'wrong_to_right':sum((not x['correct']) and y['correct'] for x,y in zip(s[arm]['rows'],s['S01']['rows'])),
        'right_to_wrong':sum(x['correct'] and (not y['correct']) for x,y in zip(s[arm]['rows'],s['S01']['rows']))}
        for arm in ('C01','C02','S01_REVERSE','S01_DECOY')}
    T738['s01_exceeds_ablation_controls']=s['S01']['correct']>max(s[k]['correct'] for k in ('C01','C02','S01_DECOY'))
    T738['order_sensitivity']=s['S01']['correct']-s['S01_REVERSE']['correct']
    T738['status']='COMPLETED_UNGRADED_SYNTHESIS' if T738['s01_exceeds_ablation_controls'] else 'COMPLETED_NO_UNIQUE_SYNTHESIS_ADVANTAGE'
    T738['elapsed_seconds']=round(time.perf_counter()-t0,2);save()
    say('TEST738_RESULT',json.dumps({'status':T738['status'],'scores':{k:v['correct'] for k,v in s.items()},
        's01_exceeds_ablation_controls':T738['s01_exceeds_ablation_controls'],'elapsed_seconds':T738['elapsed_seconds']},ensure_ascii=False))
    say('TEST738_FILES',OUT738,LOG738)
except Exception:
    T738['status']='ERROR';T738['traceback']=traceback.format_exc();save();say('TEST738_ERROR',T738['traceback']);raise
finally:
    gc.collect()
    if torch.cuda.is_available():torch.cuda.empty_cache()
