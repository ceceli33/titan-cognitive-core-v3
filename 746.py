
# AKBASCORE SILICON HIPPOCAMPUS — TEST746 / NATIVE EVIDENCE ADAPTATION (FIRST MECHANISTIC TEST)
# One Colab cell: paste entire file into a cell, or exec(open('...').read()).
# REAL DATA: USGS monthly earthquake feed; numeric fields only, no natural-language reasoning loop.
# Frozen Qwen2.5-72B NF4; exact TEST709/730 CUT3 engine imported by locked Git blobs.
# This test measures selective latent intervention, persistence and causal controls.
# It DOES NOT claim autonomous semantic learning or cross-domain generalization.
import os,sys,subprocess,importlib.util,urllib.request,hashlib,ast,json,time,gc,types,math,traceback
from pathlib import Path
from datetime import datetime,timezone
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF','expandable_segments:True')
for mod,pkg in [('torch','torch'),('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50')]:
 if importlib.util.find_spec(mod) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',pkg])
import torch,transformers,bitsandbytes
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
ROOT=Path('/content/AKBASCORE_TEST746' if Path('/content').exists() else '/tmp/AKBASCORE_TEST746')
if ROOT.exists() and (ROOT/'results.json').exists():raise RuntimeError('FAIL_CLOSED: archive previous TEST746 output; never overwrite sealed evidence')
ROOT.mkdir(parents=True,exist_ok=True); CART=ROOT/'cartridges';CART.mkdir(exist_ok=True)
RESULT=ROOT/'results.json'; LOG=ROOT/'TEST746.log';LOG.write_text('')
TEST='746';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
DTYPE=torch.bfloat16;DEV=torch.device('cuda:0');CHUNK=128;GPU_RESERVE_GIB=9.0
MAX_NEW=0 # no text generation in this experiment
SRC709='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/709.py'
SRC730='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/730.py'
LOCK709='6c9f8cbb1eeed848d45133d73f0d7676b68e9125'
LOCK730='b1bad9eb3b111b44413f8ef05a3a140ab66a77dd'
DATA_URL='https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson'
N_CASES=6; ALPHA=1.0 # copy changed positions from new evidence; no fitted parameters
R={'test':TEST,'status':'STARTED','source':DATA_URL,'model':MODEL_ID,'cut':CUT,'checks':[], 'cases':[],
 'limitations':['Structural causal adaptation only; NOT evidence of semantic self-correction',
 'Numeric fields are serialized as fixed-format ASCII tokens; tokenizer is a frozen language tokenizer',
 'A changed field is specified by schema, not discovered autonomously',
 'USGS current monthly feed is time-varying; exact response SHA is sealed at runtime',
 'No text reasoning or natural-language prompt is used',
 'The latent intervention may have no useful downstream effect; not yet evaluated here']}
def stamp():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def gitblob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def log(*x):
 s=' '.join(map(str,x));print(s,flush=True)
 with LOG.open('a') as f:f.write(s+'\n')
def save():
 p=RESULT.with_suffix('.tmp');p.write_text(json.dumps(R,indent=2,ensure_ascii=False,default=str));p.replace(RESULT)
def check(k,ok,detail=None):
 R['checks'].append({'name':k,'pass':bool(ok),'detail':detail});save();log('PASS' if ok else 'FAIL',k,detail or '')
 if not ok:raise RuntimeError('TEST746_'+k)
def fetch(url,limit=8_000_000):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST746/1.0'}),timeout=120) as f:b=f.read(limit+1)
 check('DOWNLOAD_LIMIT',len(b)<=limit,len(b));return b
def sha_file(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def release():gc.collect();torch.cuda.empty_cache()
def import_ast(raw,names,filename):
 tree=ast.parse(raw.decode());nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
 check('LOCKED_SYMBOLS_'+filename,{n.name for n in nodes}==set(names))
 exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),filename,'exec'),globals())
# Use only the existing tested engine functions; no rewritten transformer execution path.
try:
 check('CUDA',torch.cuda.is_available());check('ONE_GPU',torch.cuda.device_count()==1)
 check('A100_80GB','A100' in torch.cuda.get_device_name(0) and torch.cuda.get_device_properties(0).total_memory>=70*2**30)
 raw709=fetch(SRC709,500_000);raw730=fetch(SRC730,500_000)
 check('709_LOCK',gitblob(raw709)==LOCK709);check('730_LOCK',gitblob(raw730)==LOCK730)
 import_ast(raw709,{'pairs','cache_build','replace','half','rope','rephase','sentinel','free_gpu','ensure_room','kv_digest','full_kv_seal'},'709.py')
 import_ast(raw730,{'DirectCut3','forge_native','initialize_native','to_gpu','seal_cp'},'730.py')
 data=fetch(DATA_URL);(ROOT/'usgs_source.geojson').write_bytes(data)
 R['source_sha256']=sha(data);R['retrieved']=stamp()
 feed=json.loads(data);rows=[]
 for x in feed.get('features',[]):
  p=x.get('properties') or {};g=x.get('geometry') or {};c=g.get('coordinates') or []
  if len(c)<3 or not all(isinstance(v,(int,float)) and math.isfinite(v) for v in c[:3]):continue
  if not isinstance(p.get('mag'),(int,float)) or not math.isfinite(p['mag']):continue
  if not x.get('id'):continue
  lon,lat,depth=c[:3]
  if not (-180<=lon<=180 and -90<=lat<=90 and -10<=depth<=900):continue
  rows.append({'id':str(x['id']),'lon':float(lon),'lat':float(lat),'depth':float(depth),'mag':float(p['mag']),'time':p.get('time')})
 rows.sort(key=lambda x:x['id']);check('REAL_CASES',len(rows)>=N_CASES,len(rows));rows=rows[:N_CASES]
 R['case_ids']=[x['id'] for x in rows];save()
 tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
 # Same fixed-width record schema in old and new; only depth evidence is updated.
 # The prefix is numeric, not an instruction or a chain-of-thought prompt.
 PREFIX='746|';PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
 quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
 for p in model.parameters():p.requires_grad_(False)
 cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
 check('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,(NL,H,QH,KVH,HD));check('FROZEN',all(not p.requires_grad for p in model.parameters()))
 check('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
 weight_before=sentinel()
 def serialize(r,depth):
  # Numeric-only, stable fields, exact same schema in all arms.
  return f"{r['lat']:+010.4f}|{r['lon']:+011.4f}|{depth:+09.3f}|{r['mag']:+07.3f}|"
 def cp_save(cp,name):
  path=CART/(name+'.pt');tmp=path.with_suffix('.tmp');torch.save(cp,tmp);tmp.replace(path)
  return {'file':path.name,'sha256':sha_file(path),'tensor_sha':seal_cp(cp)}
 def cp_load(meta):
  path=CART/meta['file'];check('FILE_SHA_'+path.stem,sha_file(path)==meta['sha256'])
  cp=torch.load(path,map_location='cpu',weights_only=True)
  check('TENSOR_SHA_'+path.stem,seal_cp(cp)==meta['tensor_sha']);return cp
 def dist(a,b):
  x=a.float();y=b.float();return float((x-y).square().mean().sqrt().item())
 for i,r in enumerate(rows):
  name=f'CASE{i:02d}';log('CASE',name,'USGS_ID',r['id'])
  # Initial record has no depth measurement; updated record has the observed depth.
  # Zero is a placeholder only, never represented as a true observation.
  old=serialize(r,0.0);new=serialize(r,r['depth'])
  old_ids=tok(old,add_special_tokens=False).input_ids;new_ids=tok(new,add_special_tokens=False).input_ids
  # Fail closed if numeric tokenization changes positions; no hidden alignment heuristic.
  if len(old_ids)!=len(new_ids):
   R['cases'].append({'case':name,'id':r['id'],'status':'TOKEN_ALIGNMENT_UNSUPPORTED','old_tokens':len(old_ids),'new_tokens':len(new_ids)});save();continue
  changed=[j for j,(a,b) in enumerate(zip(old_ids,new_ids)) if a!=b]
  if not changed:
   R['cases'].append({'case':name,'id':r['id'],'status':'NO_TOKEN_DELTA'});save();continue
  a,_=forge_native(old_ids,name+'_OLD');b,_=forge_native(new_ids,name+'_NEW')
  check(name+'_SHAPE',a['n']==b['n'] and a['p']==b['p'] and a['h'].shape==b['h'].shape)
  # The exact token-delta mask is a controlled first experiment, NOT autonomous discovery.
  mask=torch.zeros((1,a['n'],1),dtype=torch.float32)
  for j in changed:mask[:,P+j,:]=1.0
  # Causal propagation can change later activations too; measure, don't conceal it.
  z=a['h'].float();v=b['h'].float();m=mask
  h=(z*(1-m)+v*m).to(a['h'].dtype).contiguous()
  lower=[]
  for (ak,av),(bk,bv) in zip(a['lower'],b['lower']):
   km=m.view(1,1,a['n'],1)
   lower.append(((ak.float()*(1-km)+bk.float()*km).to(ak.dtype).contiguous(),
                 (av.float()*(1-km)+bv.float()*km).to(av.dtype).contiguous()))
  f={'h':h,'lower':tuple(lower),'n':a['n'],'p':a['p'],'body_tokens':a['body_tokens'],'book_id':name+'_F01'}
  # Preservation and intervention are measured against both controls.
  unchanged=(1-mask).bool().expand_as(h);altered=mask.bool().expand_as(h)
  check(name+'_PRESERVE_H',torch.equal(f['h'][unchanged],a['h'][unchanged]))
  check(name+'_ADAPT_H',torch.equal(f['h'][altered],b['h'][altered]))
  old_meta=cp_save(a,name+'_OLD');new_meta=cp_save(b,name+'_NEW');f_meta=cp_save(f,name+'_F01')
  del a,b,f;release()
  loaded=cp_load(f_meta)
  # Native full 80-layer reload from TEST730, not a new engine.
  gpu=to_gpu(loaded);memory=initialize_native(gpu)
  check(name+'_RELOAD_80',len(memory)==NL)
  rec={'case':name,'usgs_id':r['id'],'status':'STRUCTURAL_PASS','old_record_sha256':sha(old.encode()),
       'new_record_sha256':sha(new.encode()),'changed_token_positions':changed,
       'old':old_meta,'new':new_meta,'F01':f_meta,'parent_shas':[old_meta['sha256'],new_meta['sha256']],
       'h_rms_from_old':dist(loaded['h'],cp_load(old_meta)['h']),
       'h_rms_from_new':dist(loaded['h'],cp_load(new_meta)['h']),
       'measurement':'structural only; semantic learning NOT tested'}
  R['cases'].append(rec);save();del loaded,gpu,memory;release()
 check('AT_LEAST_ONE_VALID_CASE',any(x['status']=='STRUCTURAL_PASS' for x in R['cases']))
 check('WEIGHTS_UNCHANGED',sentinel()==weight_before)
 R['status']='STRUCTURAL_STAGE_COMPLETE';R['completed']=stamp();save()
 log('TEST746 STRUCTURAL STAGE COMPLETE — no autonomous-learning claim',RESULT)
except Exception as e:
 R['status']='FAILED';R['error']=repr(e);R['traceback']=traceback.format_exc();save();log('TEST746 FAILED',repr(e));raise
