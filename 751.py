# AKBASCORE SILICON HIPPOCAMPUS — TEST751 / NATIVE EVIDENCE ADAPTATION (SPARSE MASK / NECESSITY / PERMUTATION / FACTORIAL CONTROLS)
# One Colab cell: paste entire file into a cell, or exec(open('...').read()).
# REAL DATA: USGS monthly earthquake feed; numeric fields only, no natural-language reasoning loop.
# Frozen Qwen2.5-72B NF4; exact TEST709/730 CUT3 engine imported by locked Git blobs.
# This test measures selective latent intervention, persistence and causal controls.
# It DOES NOT claim autonomous semantic learning or cross-domain generalization.
import os,sys,subprocess,importlib.util,urllib.request,hashlib,ast,json,time,gc,types,math,traceback,random
from pathlib import Path
from datetime import datetime,timezone
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF','expandable_segments:True')
for mod,pkg in [('torch','torch'),('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50')]:
 if importlib.util.find_spec(mod) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',pkg])
import torch,transformers,bitsandbytes
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
ROOT=Path('/content/AKBASCORE_TEST751' if Path('/content').exists() else '/tmp/AKBASCORE_TEST751')
if ROOT.exists() and (ROOT/'results.json').exists():raise RuntimeError('FAIL_CLOSED: archive previous TEST751 output; never overwrite sealed evidence')
ROOT.mkdir(parents=True,exist_ok=True); CART=ROOT/'cartridges';CART.mkdir(exist_ok=True)
RESULT=ROOT/'results.json'; LOG=ROOT/'TEST751.log';LOG.write_text('')
TEST='751';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
DTYPE=torch.bfloat16;DEV=torch.device('cuda:0');CHUNK=128;GPU_RESERVE_GIB=9.0
MAX_NEW=0 # likelihood and next-token probes only; no free generation
SRC709='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/709.py'
SRC730='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/730.py'
LOCK709='6c9f8cbb1eeed848d45133d73f0d7676b68e9125'
LOCK730='b1bad9eb3b111b44413f8ef05a3a140ab66a77dd'
DATA_URL='https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson'
N_CASES=12; SEED=751; ARMS=('OLD','NEW','ORACLE','BLIND_HKV','H_ONLY','KV_ONLY','RANDOM','SHAM','TOP4')
R={'test':TEST,'status':'STARTED','source':DATA_URL,'model':MODEL_ID,'cut':CUT,'checks':[], 'cases':[], 'arms':list(ARMS),
 'limitations':['Independent structural and output-distribution tests; NOT evidence of semantic self-correction',
 'Numeric fields are serialized as fixed-format ASCII tokens; tokenizer is a frozen language tokenizer',
 'ORACLE uses true changed tokens; BLIND uses paired OLD/NEW H3 differences, not independent error discovery',
 'USGS current monthly feed is time-varying; exact response SHA is sealed at runtime',
 'Fixed labels DEPTH/LAT/MAG are used solely as untrained readout suffixes, not as reasoning loops',
 'Output-distribution shift does not establish factual correctness or causal learning', 'BLIND threshold median+2*MAD fixed in advance; no threshold training', 'Calibration and holdout are descriptive partitions, not independent model fitting', 'Sparse ranking uses paired OLD/NEW H3 and therefore is not independent error detection', 'All probes use a fixed separator and test output distribution, not factual recall', 'RANDOM controls include oracle positions by chance and are not forced to be disjoint', 'Conditional numeric likelihood is not proof of factual recall or autonomous correction', 'Suffix probes were not present during forging and are deliberately out-of-context readouts']}
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
 if not ok:raise RuntimeError('TEST751_'+k)
def fetch(url,limit=8_000_000):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST751/1.0'}),timeout=120) as f:b=f.read(limit+1)
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
 R['case_ids']=[x['id'] for x in rows];R['panel_sha256']=sha(json.dumps(rows,sort_keys=True).encode());save()
 tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
 # Numeric-only serialized real observations; missing depth encoded as placeholder (not an observation).
 # The prefix is numeric, not an instruction or a chain-of-thought prompt.
 PREFIX='751|';PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
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
 # Independent controls on the same physical OLD/NEW cartridges; no prompt or text feedback.
 import random
 random.seed(SEED)
 def mask_cp(a,b,positions,book_id,mode='HKV'):
  n=a['n'];assert a['n']==b['n'] and a['p']==b['p']
  m=torch.zeros((1,n,1),dtype=torch.bool)
  for j in positions:
   if not (P<=j<n):raise RuntimeError('MASK_OUT_OF_RANGE')
   m[:,j,:]=True
  h=torch.where(m,b['h'],a['h']).contiguous() if mode in ('HKV','H') else a['h'].clone()
  km=m.view(1,1,n,1)
  lower=tuple((torch.where(km,bk,ak).contiguous(),torch.where(km,bv,av).contiguous())
              if mode in ('HKV','KV') else (ak.clone(),av.clone())
              for (ak,av),(bk,bv) in zip(a['lower'],b['lower']))
  return {'h':h,'lower':lower,'n':n,'p':a['p'],'body_tokens':a['body_tokens'],'book_id':book_id}
 def blind_positions(a,b):
  delta=(b['h'].float()-a['h'].float()).square().mean(-1).sqrt()[0]
  vals=delta[P:a['n']]
  med=vals.median();mad=(vals-med).abs().median();threshold=med+2.0*mad
  ranked=sorted(range(P,a['n']),key=lambda j:(-float(delta[j]),j))
  selected=[j for j in ranked if float(delta[j])>float(threshold)]
  return selected,{'median':float(med),'mad':float(mad),'threshold':float(threshold),'budget':len(selected),'ranked':ranked}
 @torch.no_grad()
 def probe(cp):
  # Readout: probability distribution for the SAME one-token numeric separator.
  # This is a mechanistic sensitivity measurement, not a semantic answer.
  gpu=to_gpu(cp);memory=initialize_native(gpu)
  n=cp['n'];qids=tok('|',add_special_tokens=False).input_ids
  check('ONE_TOKEN_PROBE',len(qids)==1,len(qids))
  pos=torch.tensor([[n]],device=DEV,dtype=torch.long)
  cache=cache_build(memory)
  out=model(input_ids=torch.tensor([qids],device=DEV),past_key_values=cache,
   attention_mask=torch.ones((1,n+1),device=DEV,dtype=torch.long),
   position_ids=pos,cache_position=pos.view(-1),use_cache=False,return_dict=True)
  logits=out.logits[0,-1,:].float().cpu()
  del out,cache,memory,gpu;release()
  return logits
 def jsd(x,y):
  px=torch.softmax(x,dim=-1);py=torch.softmax(y,dim=-1);m=(px+py)*0.5
  return float((0.5*(px*(px.clamp_min(1e-30).log()-m.clamp_min(1e-30).log())).sum()+
                0.5*(py*(py.clamp_min(1e-30).log()-m.clamp_min(1e-30).log())).sum()).item())
 @torch.no_grad()
 def candidate_ll(cp,suffix,candidate):
  # Teacher-forced full candidate log likelihood, NOT generated answer.
  suffix_ids=tok(suffix,add_special_tokens=False).input_ids
  candidate_ids=tok(candidate,add_special_tokens=False).input_ids
  if not suffix_ids or not candidate_ids:raise RuntimeError('EMPTY_READOUT_TOKENS')
  gpu=to_gpu(cp);memory=initialize_native(gpu);cache=cache_build(memory)
  n=cp['n'];ids=suffix_ids+candidate_ids
  pos=torch.arange(n,n+len(ids),device=DEV,dtype=torch.long)
  out=model(input_ids=torch.tensor([ids],device=DEV),past_key_values=cache,
    attention_mask=torch.ones((1,n+len(ids)),device=DEV,dtype=torch.long),
    position_ids=pos.view(1,-1),cache_position=pos,use_cache=False,return_dict=True)
  begin=len(suffix_ids)-1
  logits=out.logits[0,begin:begin+len(candidate_ids),:].float()
  targets=torch.tensor(candidate_ids,device=DEV,dtype=torch.long)
  score=float(torch.log_softmax(logits,dim=-1).gather(1,targets[:,None]).sum().item())
  del out,cache,memory,gpu;release()
  return score
 @torch.no_grad()
 def suffix_probe(cp,suffix):
  ids=tok(suffix,add_special_tokens=False).input_ids
  if not ids:raise RuntimeError('EMPTY_SUFFIX')
  gpu=to_gpu(cp);memory=initialize_native(gpu);cache=cache_build(memory)
  n=cp['n'];pos=torch.arange(n,n+len(ids),device=DEV,dtype=torch.long)
  out=model(input_ids=torch.tensor([ids],device=DEV),past_key_values=cache,
    attention_mask=torch.ones((1,n+len(ids)),device=DEV,dtype=torch.long),
    position_ids=pos.view(1,-1),cache_position=pos,use_cache=False,return_dict=True)
  logits=out.logits[0,-1,:].float().cpu()
  del out,cache,memory,gpu;release()
  return logits
 # TEST751: separate hypotheses; all panels sealed before loading cases.
 # P1: structural transfer (9 arms), P2: suffix sensitivity (4 suffixes),
 # P3: depth evidence (truth versus three alternatives),
 # P4: non-target field preservation (LAT/LON/MAG),
 # P5: matched negative controls (OLD/SHAM/RANDOM).
 # A scored preference is a teacher-forced likelihood comparison, NOT a generated factual answer.
 SUFFIXES=('DEPTH=','depth: ','VALUE=','|')
 READ_ARMS=('OLD','NEW','BLIND_HKV','TOP4','RANDOM','SHAM')
 NUM_ARMS=('OLD','NEW','BLIND_HKV','TOP4','SHAM')
 R['protocol']={'suites':['structural','suffix_generalization','depth_three_foils','non_target_preservation','negative_controls'],
   'suffixes':list(SUFFIXES),'read_arms':list(READ_ARMS),'numeric_arms':list(NUM_ARMS),
   'limitations':['No independent error detection: BLIND and TOP4 compare OLD/NEW representations',
    'Teacher-forced numeric preference is not unconstrained recall',
    'Candidate lengths may differ; raw sequence LL is reported with token counts',
    'USGS cases are real but OLD depth=0 is an artificial placeholder',
    'Fixed numeric serialization, no generalization claim outside this format',
    'No layerwise tracing in this test; tracing needs separate hook-validation protocol']}
 save()
 valid=0;rng=random.Random(SEED)
 for i,r in enumerate(rows):
  name=f'CASE{i:02d}';split='CALIBRATION' if i<4 else 'HELD_OUT';log('CASE',name,split,r['id'])
  old=serialize(r,0.0);new=serialize(r,r['depth'])
  oi=tok(old,add_special_tokens=False).input_ids;ni=tok(new,add_special_tokens=False).input_ids
  rec={'case':name,'split':split,'usgs_id':r['id'],'old_sha256':sha(old.encode()),
       'new_sha256':sha(new.encode()),'arms':{},'status':'STARTED'}
  R['cases'].append(rec);save()
  if len(oi)!=len(ni):rec['status']='SKIP_TOKEN_LENGTH';save();continue
  oracle=[P+j for j,(u,v) in enumerate(zip(oi,ni)) if u!=v]
  if not oracle:rec['status']='SKIP_NO_CHANGE';save();continue
  a,_=forge_native(oi,name+'_OLD');b,_=forge_native(ni,name+'_NEW')
  check(name+'_MATCH',a['n']==b['n'] and a['p']==b['p'])
  blind,stats=blind_positions(a,b);ranking=stats.pop('ranked')
  candidates=list(range(P,a['n']))
  random_positions=rng.sample(candidates,len(blind))
  rec.update({'blind_statistics':stats,'oracle_count':len(oracle),'oracle_positions':oracle,
    'blind_positions':blind,'top4_positions':ranking[:4],
    'blind_recall':len(set(blind)&set(oracle))/len(oracle),
    'blind_precision':len(set(blind)&set(oracle))/len(blind) if blind else None})
  cp_map={'OLD':a,'NEW':b,
   'ORACLE':mask_cp(a,b,oracle,name+'_ORACLE'),
   'BLIND_HKV':mask_cp(a,b,blind,name+'_BLIND_HKV'),
   'H_ONLY':mask_cp(a,b,blind,name+'_H_ONLY','H'),
   'KV_ONLY':mask_cp(a,b,blind,name+'_KV_ONLY','KV'),
   'RANDOM':mask_cp(a,b,random_positions,name+'_RANDOM'),
   'SHAM':mask_cp(a,b,[],name+'_SHAM'),
   'TOP4':mask_cp(a,b,ranking[:4],name+'_TOP4')}
  rec['status']='RUNNING';save();log('BLIND_MASK',len(blind),'ORACLE_MASK',len(oracle))
  logits={}
  for arm in ARMS:
   log('ARM',name,arm)
   meta=cp_save(cp_map[arm],name+'_'+arm)
   reloaded=cp_load(meta)
   check(name+'_'+arm+'_RELOAD',len(reloaded['lower'])==CUT+1 and reloaded['n']==a['n'])
   logits[arm]=probe(reloaded)
   rec['arms'][arm]=meta;save();del reloaded;release()
  rec['jsd_to_new']={arm:jsd(logits[arm],logits['NEW']) for arm in ARMS}
  rec['jsd_to_old']={arm:jsd(logits[arm],logits['OLD']) for arm in ARMS}
  rec['blind_beats_random']=rec['jsd_to_new']['BLIND_HKV']<rec['jsd_to_new']['RANDOM']
  del logits;release()
  # P2: fixed readout variants; compare the same arms under each suffix.
  rec['suffix_jsd_to_new']={}
  for suffix in SUFFIXES:
   distros={arm:suffix_probe(cp_map[arm],suffix) for arm in READ_ARMS}
   rec['suffix_jsd_to_new'][suffix]={arm:jsd(distros[arm],distros['NEW']) for arm in READ_ARMS}
   del distros;release()
  # P3 and P4: candidate sets fixed by numeric transformations, no outcome-based tuning.
  # Depth: zero placeholder, neighboring +/- 1 km values (all formatted identically).
  # Other fields: true value versus +1 unit foil. Separate from depth correction.
  fields={
   'DEPTH':('DEPTH=',f"{r['depth']:+09.3f}",
     {'ZERO':f"{0.0:+09.3f}",'PLUS1':f"{r['depth']+1:+09.3f}",'MINUS1':f"{r['depth']-1:+09.3f}"}),
   'LAT':('LAT=',f"{r['lat']:+010.4f}",{'SHIFT1':f"{r['lat']+1:+010.4f}"}),
   'LON':('LON=',f"{r['lon']:+011.4f}",{'SHIFT1':f"{r['lon']+1:+011.4f}"}),
   'MAG':('MAG=',f"{r['mag']:+07.3f}",{'SHIFT1':f"{r['mag']+1:+07.3f}"})}
  rec['numeric_readout']={}
  for field,(suffix,truth,foils) in fields.items():
   rec['numeric_readout'][field]={}
   rec.setdefault('candidate_token_counts',{})[field]={
      'truth':len(tok(truth,add_special_tokens=False).input_ids),
      **{f:len(tok(v,add_special_tokens=False).input_ids) for f,v in foils.items()}}
   for arm in NUM_ARMS:
    truth_ll=candidate_ll(cp_map[arm],suffix,truth)
    foil_lls={key:candidate_ll(cp_map[arm],suffix,value) for key,value in foils.items()}
    rec['numeric_readout'][field][arm]={'truth_ll':truth_ll,
      'foils':{key:{'ll':v,'margin':truth_ll-v,'prefer_truth':truth_ll>v} for key,v in foil_lls.items()},
      'prefer_all':all(truth_ll>v for v in foil_lls.values())}
   save()
  # Explicit no-op consistency check, tolerant to floating-point JSD computation.
  rec['sham_jsd_to_old']=rec['jsd_to_old']['SHAM']
  check(name+'_SHAM_INVARIANT',rec['sham_jsd_to_old']<=1e-9,rec['sham_jsd_to_old'])
  rec['status']='MEASURED';valid+=1;save()
  log('CASE_RESULT',name,'blind_recall',rec['blind_recall'],
      'depth_new_all',rec['numeric_readout']['DEPTH']['NEW']['prefer_all'],
      'depth_new_zero_margin',rec['numeric_readout']['DEPTH']['NEW']['foils']['ZERO']['margin'])
  del cp_map,a,b;release()
 check('VALID_CASES',valid>=8,{'valid':valid,'total':N_CASES})
 measured=[x for x in R['cases'] if x['status']=='MEASURED']
 held=[x for x in measured if x['split']=='HELD_OUT']
 check('HELD_OUT_CASES',len(held)>=6,len(held))
 check('WEIGHTS_UNCHANGED',sentinel()==weight_before)
 def summarize(items):
  n=len(items)
  return {'n':n,'mean_blind_recall':sum(x['blind_recall'] for x in items)/n,
   'blind_beats_random':sum(x['blind_beats_random'] for x in items),
   'mean_jsd_to_new':{arm:sum(x['jsd_to_new'][arm] for x in items)/n for arm in ARMS},
   'suffix_jsd_to_new':{suffix:{arm:sum(x['suffix_jsd_to_new'][suffix][arm] for x in items)/n
     for arm in READ_ARMS} for suffix in SUFFIXES},
   'numeric':{field:{arm:{'prefer_all':sum(x['numeric_readout'][field][arm]['prefer_all'] for x in items),
     'foil_metrics':{foil:{'prefer_truth':sum(x['numeric_readout'][field][arm]['foils'][foil]['prefer_truth'] for x in items),
      'mean_margin':sum(x['numeric_readout'][field][arm]['foils'][foil]['margin'] for x in items)/n}
      for foil in items[0]['numeric_readout'][field][arm]['foils']}}
     for arm in NUM_ARMS} for field in ('DEPTH','LAT','LON','MAG')}}
 R['summary']={'all':summarize(measured),'held_out':summarize(held)}
 R['status']='COMPLETE_MULTI_AXIS_BATCH';R['completed']=stamp();save()
 log('TEST751 COMPLETE',json.dumps(R['summary'],indent=2),RESULT)
except Exception as e:
 R['status']='FAILED';R['error']=repr(e);R['traceback']=traceback.format_exc();save();log('TEST751 FAILED',repr(e));raise
