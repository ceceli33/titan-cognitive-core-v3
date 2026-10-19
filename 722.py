# AKBASCORE PROMETHEUS — TEST722 / Native H3 numeric addressing and SHA lineage
# Grounded in locked TEST709 engine as imported by TEST716. Google Colab A100 80GB.
# Research test; not GPU-executed by the author. No claim of PASS before running.
import os,sys,subprocess,importlib.util,urllib.request,hashlib,ast,json,time,gc,traceback,platform,types,copy
from pathlib import Path
from datetime import datetime,timezone
from io import BytesIO
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF','expandable_segments:True')
for m,p in [('torch','torch'),('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50'),('psutil','psutil')]:
 if importlib.util.find_spec(m) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',p])
import torch,transformers,bitsandbytes,psutil
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
ROOT=Path('/content/AKBASCORE_TEST722' if Path('/content').exists() else '/tmp/AKBASCORE_TEST722');ROOT.mkdir(parents=True,exist_ok=True)
LOG=ROOT/'TEST722.log';OUT=ROOT/'TEST722_results.json';LOG.write_text('')
TEST='722';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
DTYPE=torch.bfloat16;DEV=torch.device('cuda:0');CHUNK=128;MAX_NEW=48;GPU_RESERVE_GIB=9.0
SRC709='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/709.py'
SRC716='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/716.py'
LOCK709='6c9f8cbb1eeed848d45133d73f0d7676b68e9125';LOCK716='913fa7a4951f2072df4be2eb49120ea86efa5477'
R={'test':TEST,'status':'STARTED','method':'locked TEST709 reference hook versus direct layer.forward replacement','source_links':[SRC709,SRC716],'checks':[],'measurements':{},'limitations':['Not executed on GPU by code author','This validates CUT3 capture and initialize only; append parity is a separate acceptance gate','Direct layer.forward integration is hook-free but not a compiled C++/CUDA runtime','Greedy answer agreement does not prove semantic correctness']}
def log(*xs):
 s=' '.join(map(str,xs));print(s,flush=True)
 with LOG.open('a') as f:f.write(s+'\n')
def save():
 tmp=OUT.with_suffix('.json.tmp');tmp.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str));tmp.replace(OUT)
def check(name,ok,detail=None):
 R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});save();log('PASS' if ok else 'FAIL',name,detail or '')
 if not ok:raise RuntimeError('CHECK_FAILED:'+name)
def gitblob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def download(url,limit=300000):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST722'}),timeout=120) as f:b=f.read(limit+1)
 if len(b)>limit:raise RuntimeError('SOURCE_TOO_LARGE')
 return b
def sha(b):return hashlib.sha256(b).hexdigest()
def sync():torch.cuda.synchronize()
def gpu():
 sync();f,t=torch.cuda.mem_get_info();return {'free_gib':round(f/2**30,3),'allocated_gib':round(torch.cuda.memory_allocated()/2**30,3),'peak_gib':round(torch.cuda.max_memory_allocated()/2**30,3),'total_gib':round(t/2**30,3)}
def release():gc.collect();torch.cuda.empty_cache()
# Native CUT3 interception: temporary direct forward method, NOT a forward hook.
# Only the locked layer-3 boundary is altered; no model weight or other layer is modified.
class DirectCut3:
 def __init__(self,layer,mode,collector=None,source=None):
  self.layer=layer;self.mode=mode;self.collector=collector;self.source=source;self.offset=0;self.old=None
 def __enter__(self):
  if self.layer._forward_hooks or self.layer._forward_pre_hooks:raise RuntimeError('NATIVE_PATH_FORWARD_HOOK_PRESENT')
  self.old=self.layer.forward;ctx=self
  def direct_forward(this,*args,**kwargs):
   out=ctx.old(*args,**kwargs);z=out[0] if isinstance(out,(tuple,list)) else out
   if ctx.mode=='capture':
    ctx.collector.append(z.detach().to('cpu',copy=True).contiguous());return out
   if ctx.mode=='inject':
    st=ctx.offset;target=ctx.source[:,st:st+z.shape[1],:]
    if z.shape!=target.shape:raise RuntimeError(f'NATIVE_INJECTION_SHAPE:{tuple(z.shape)} vs {tuple(target.shape)}')
    return replace(out,target)
   raise RuntimeError('UNKNOWN_NATIVE_MODE')
  self.layer.forward=types.MethodType(direct_forward,self.layer);return self
 def __exit__(self,*exc):
  self.layer.forward=self.old
  return False
# Exact TEST709 engine extraction, never execute demo code.
def import_reference(raw):
 names={'pairs','cache_build','replace','half','rope','rephase','sentinel','free_gpu','ensure_room','forge_stream','cart_load','initialize','kv_digest','full_kv_seal','append','answer','mem'}
 tree=ast.parse(raw.decode('utf-8'));found={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names}
 check('ALL_LOCKED_FUNCTIONS_PRESENT',set(found)==names,sorted(names-set(found)))
 mod=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[])
 exec(compile(ast.fix_missing_locations(mod),'709.py','exec'),globals())
# New forge uses same streaming input, positions and physical format as TEST709.
@torch.no_grad()
def forge_native(body_ids,book_id):
 ids=PIDS+body_ids;n=len(ids);cache=None;h_chunks=[];t=time.perf_counter()
 with DirectCut3(model.model.layers[CUT],'capture',collector=h_chunks):
  for st in range(0,n,CHUNK):
   piece=ids[st:st+CHUNK];ensure_room(len(piece)+512);pos=torch.arange(st,st+len(piece),device=DEV)
   out=model(input_ids=torch.tensor([piece],device=DEV),past_key_values=cache,
    attention_mask=torch.ones((1,st+len(piece)),device=DEV,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
   cache=out.past_key_values;del out
 kv=pairs(cache)
 cp={'h':torch.cat(h_chunks,dim=1),'lower':tuple((k.detach().cpu().contiguous(),v.detach().cpu().contiguous()) for k,v in kv[:CUT+1]),'n':n,'p':P,'body_tokens':len(body_ids),'book_id':book_id}
 check('NATIVE_FORGE_SHAPE',cp['h'].shape==(1,n,H) and len(cp['lower'])==CUT+1)
 del cache,kv;release();return cp,round(time.perf_counter()-t,3)
@torch.no_grad()
def initialize_native(cp):
 n=cp['n'];h=cp['h'];ensure_room(n+512);upper=None
 with DirectCut3(model.model.layers[CUT],'inject',source=h) as bridge:
  for st in range(0,n,CHUNK):
   q=min(CHUNK,n-st);ensure_room(q+512);bridge.offset=st;pos=torch.arange(st,st+q,device=DEV)
   out=model(inputs_embeds=torch.zeros((1,q,H),device=DEV,dtype=DTYPE),past_key_values=upper,
    attention_mask=torch.ones((1,st+q),device=DEV,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
   upper=out.past_key_values;del out
 kv=pairs(upper);result=cp['lower']+tuple((k.detach().clone(),v.detach().clone()) for k,v in kv[CUT+1:]);check('NATIVE_INIT_80_LAYERS',len(result)==NL)
 del upper,kv;return result

def to_gpu(cp):
 return {'h':cp['h'].to(DEV),'lower':tuple((k.to(DEV),v.to(DEV)) for k,v in cp['lower']),'n':cp['n'],'p':cp['p'],'body_tokens':cp['body_tokens'],'book_id':cp['book_id']}
def seal_cp(cp):
 return {'h':sha(cp['h'].contiguous().view(torch.uint8).numpy().tobytes()),'lower':[(sha(k.contiguous().view(torch.uint8).numpy().tobytes()),sha(v.contiguous().view(torch.uint8).numpy().tobytes())) for k,v in cp['lower']]}
def memory_seals(mem):return [(kv_digest(k),kv_digest(v)) for k,v in mem]
def compare_seals(a,b):return len(a)==len(b) and all(x==y for x,y in zip(a,b))

# ============================================================================================================
# TEST722 — HARD NEGATIVES / VERSION COLLISIONS / OPEN-SET H3 ROUTING
# Locked 709 engine, proven 721 direct CUT3, disk SHA ledger, no training or answer-dependent routing.
# The router is deliberately UNCHANGED from TEST721: top2 token-to-native-H3 cosine.
# A scored absent query must not be called UNKNOWN merely because its nearest cartridge is weak.
# ============================================================================================================
import numpy as np
from collections import defaultdict
CART_DIR=ROOT/'physical_cartridges';CART_DIR.mkdir(parents=True,exist_ok=True)
MANIFEST=ROOT/'TEST722_manifest.json'
QUERY_LIMIT=128;MAX_BANK_ROWS=96;TOP_K=5
# Distinct location facts. Two versions of the same asset and nearby misleading records.
# Answers and routing gold never enter model input or routing scores.
FAMILIES=[
 ('AX-731','coolant regulator','north archive','south annex','copper vault'),
 ('BT-962','torque controller','slate pavilion','glass depot','amber bay'),
 ('DN-348','servo monitor','willow chamber','cedar room','granite station'),
 ('EV-415','pressure sensor','amber vault','river gallery','moss annex'),
 ('FK-276','spindle driver','copper annex','silver hangar','quartz store'),
 ('GL-583','motor coupler','river gallery','north bunker','blue pavilion'),
 ('HM-824','encoder','quartz station','slate room','willow depot'),
 ('JP-139','feed controller','cedar bay','copper tower','amber warehouse'),
 ('KR-657','relay module','silver depot','moss gallery','glass chamber'),
 ('LS-902','axis converter','moss chamber','quartz annex','south pavilion')
]
# Each record is an independent cartridge. Three records share code/type but differ in revision.
# Explicit revision information in the question disambiguates the target without metadata oracle.
CASES=[];PANEL=[]
for idx,(code,device,loc_a,loc_b,loc_c) in enumerate(FAMILIES,1):
 for revision,location in [('R1',loc_a),('R2',loc_b),('R3',loc_c)]:
  cid=f'C{idx:02d}_{revision}'
  text=(f'Equipment registry entry. Asset code: {code}. Equipment type: {device}. '
        f'Revision: {revision}. For asset {code} revision {revision}, '
        f'the official storage location is {location}. '
        f'This location applies only to revision {revision} of {code}.')
  CASES.append((cid,text,code,revision,location))
  PANEL.append({'id':cid,'question':f'Where is the {code} {device}, revision {revision}, stored?',
                'expected':location,'code':code,'revision':revision})
UNKNOWN=[
 {'question':'Where is the ZZ-000 optical transceiver, revision R1, stored?','reason':'absent_code'},
 {'question':'Where is the AX-731 coolant regulator, revision R9, stored?','reason':'absent_revision'},
 {'question':'Where is the BT-962 torque controller, revision R4, stored?','reason':'absent_revision'},
 {'question':'Where is the PX-000 calibration cube, revision R3, stored?','reason':'absent_code'},
 {'question':'Where is the DN-348 servo monitor, revision R0, stored?','reason':'absent_revision'},
 {'question':'Where is the FK-276 spindle driver, revision R8, stored?','reason':'absent_revision'}
]
R['method']='TEST721 fixed native H3 top2 routing on 30 version-confusable physical CUT3 cartridges'
R['limitations']=['GPU run not performed by code author','Router always selects nearest neighbor; no automatic abstention','No learned threshold is calibrated on this panel','Physical answer is scored separately from retrieval','Semantic correctness uses strict location inclusion and excludes other same-code revisions','This is controlled synthetic evidence, not proof of general reasoning','APPEND/RoPE parity is outside TEST722']
R['routing']=[];R['qa']=[];R['unknown']=[];R['controls']=[]
def sha_file(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def atomic_json(path,obj):
 tmp=Path(str(path)+'.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=str));tmp.replace(path)
def safe_load(entry):
 path=CART_DIR/entry['file']
 check('FILE_SHA_'+entry['id'],path.exists() and sha_file(path)==entry['sha256'])
 cp=torch.load(path,map_location='cpu',weights_only=True)
 check('CARTRIDGE_ID_'+entry['id'],cp['book_id']==entry['id'] and cp['p']==P and cp['n']==P+cp['body_tokens'])
 check('CARTRIDGE_SHA_'+entry['id'],json.dumps(seal_cp(cp),sort_keys=True)==json.dumps(entry['tensor_sha'],sort_keys=True))
 return cp
def normalize(a):
 a=np.asarray(a,dtype=np.float32)
 return a/np.maximum(np.linalg.norm(a,axis=-1,keepdims=True),1e-8)
def bank_from(cp):
 x=cp['h'][0,P:,:].float()
 if x.shape[0]<1:raise RuntimeError('EMPTY_BANK')
 idx=np.linspace(0,len(x)-1,min(MAX_BANK_ROWS,len(x)),dtype=np.int64)
 return normalize(x[torch.from_numpy(idx)].numpy())
@torch.no_grad()
def query_h3(question):
 prompt='<|im_start|>user\n'+question+'\n<|im_end|>\n<|im_start|>assistant\n'
 ids=tok(prompt,add_special_tokens=False).input_ids
 if len(ids)>QUERY_LIMIT:raise RuntimeError('QUERY_TOO_LONG')
 captures=[]
 with DirectCut3(model.model.layers[CUT],'capture',collector=captures):
  output=model(input_ids=torch.tensor([ids],device=DEV),use_cache=False,return_dict=True)
  del output
 if len(captures)!=1:raise RuntimeError('QUERY_H3_CAPTURE_COUNT')
 return normalize(captures[0][0].float().numpy())
def native_score(q,bank):
 sim=q@bank.T
 n=min(2,sim.shape[1])
 return float(np.partition(sim,-n,axis=1)[:,-n:].mean(axis=1).mean())
def route(q,banks):
 scores={cid:native_score(q,b) for cid,b in banks.items()}
 ordered=sorted(scores,key=lambda cid:(-scores[cid],cid))
 return ordered,scores
@torch.no_grad()
def disk_answer(entry,question):
 cp=safe_load(entry)
 cp_gpu=to_gpu(cp)
 del cp
 memory=initialize_native(cp_gpu)
 if len(memory)!=NL:raise RuntimeError('RELOAD_LAYER_COUNT')
 raw=answer(memory,question)
 del memory,cp_gpu
 release()
 return raw
try:
 log('='*110);log('AKBASCORE PROMETHEUS — TEST722 — HARD NEGATIVES / VERSION COLLISIONS / OPEN-SET');log('='*110)
 check('CUDA_AVAILABLE',torch.cuda.is_available(),{'torch':torch.__version__,'cuda':torch.version.cuda})
 check('ONE_GPU',torch.cuda.device_count()==1)
 check('A100_80GB',torch.cuda.get_device_properties(0).total_memory>=70*2**30,torch.cuda.get_device_name(0))
 check('RESERVE',GPU_RESERVE_GIB>=9 and 32<=CHUNK<=512)
 raw709=download(SRC709);raw716=download(SRC716)
 check('709_GIT_BLOB_LOCK',gitblob(raw709)==LOCK709,gitblob(raw709))
 check('716_GIT_BLOB_LOCK',gitblob(raw716)==LOCK716,gitblob(raw716))
 import_reference(raw709)
 tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
 PREFIX='<|im_start|>system\nUse only the available document memory for document-specific questions. If the evidence is missing, say UNKNOWN.\n<|im_end|>\n<|im_start|>user\nINFORMATION:\n'
 PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
 quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
 log('LOAD_FROZEN_72B_NF4')
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
 for parameter in model.parameters():parameter.requires_grad_(False)
 cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
 check('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,[NL,H,QH,KVH,HD])
 check('FROZEN',all(not p.requires_grad for p in model.parameters()))
 check('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
 check('DIRECT_FORWARD_NO_EXISTING_HOOKS',not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
 before=sentinel();R['weight_sentinel_before']=before
 R['panel_sha256']=sha(json.dumps(PANEL,sort_keys=True,ensure_ascii=False).encode())
 R['environment']={'torch':torch.__version__,'transformers':transformers.__version__,'gpu':torch.cuda.get_device_name(0)}
 log('MODEL_READY',gpu())
 ledger={'test':TEST,'sources':{'709':LOCK709,'716':LOCK716},'model':MODEL_ID,'cut':CUT,'prefix_sha256':sha(PREFIX.encode()),'cartridges':[]}
 banks={}
 # FORGE and physical commits: immutable source body, SHA256, H3 address bank.
 for cid,body,code,revision,location in CASES:
  ids=tok(body,add_special_tokens=False).input_ids
  log('FORGE_NATIVE',cid,'body_tokens',len(ids))
  cp,seconds=forge_native(ids,cid)
  filename=cid+'.pt';path=CART_DIR/filename;tmp=Path(str(path)+'.tmp')
  torch.save(cp,tmp);tmp.replace(path)
  entry={'id':cid,'file':filename,'sha256':sha_file(path),'tensor_sha':seal_cp(cp),
         'body_sha256':sha(body.encode()),'body_tokens':len(ids),'forge_s':seconds}
  banks[cid]=bank_from(cp);ledger['cartridges'].append(entry)
  atomic_json(MANIFEST,ledger)
  log('COMMIT',cid,entry['sha256'],'forge_s',seconds)
  del cp
  release()
 check('CARTRIDGES_30',len(ledger['cartridges'])==30)
 check('UNIQUE_CARTRIDGES',len({e['sha256'] for e in ledger['cartridges']})==30)
 persisted=json.loads(MANIFEST.read_text(encoding='utf-8'))
 check('MANIFEST_REOPEN',len(persisted['cartridges'])==30 and persisted['prefix_sha256']==sha(PREFIX.encode()))
 entries={e['id']:e for e in persisted['cartridges']}
 for cid,entry in entries.items():
  cp=safe_load(entry);rebuild=bank_from(cp)
  check('BANK_DISK_EXACT_'+cid,np.array_equal(rebuild,banks[cid]))
  del cp,rebuild
 # No answers/gold labels enter route() or native_score().
 for row in PANEL:
  q=query_h3(row['question']);ordered,scores=route(q,banks)
  top1=ordered[0];margin=scores[top1]-scores[ordered[1]]
  rec={'id':row['id'],'question':row['question'],'selected':top1,'top5':ordered[:TOP_K],
       'gold':row['id'],'hit1':top1==row['id'],'hit5':row['id'] in ordered[:TOP_K],
       'top1_score':round(scores[top1],8),'margin':round(margin,8),
       'gold_score':round(scores[row['id']],8)}
  R['routing'].append(rec);save();log('ROUTE',json.dumps(rec,ensure_ascii=False))
 R['routing_summary']={'r1':sum(r['hit1'] for r in R['routing']),'r5':sum(r['hit5'] for r in R['routing']),'n':len(PANEL)}
 log('ROUTING_SUMMARY',R['routing_summary'])
 # Actual selected cartridge, NOT the oracle gold. Score correct revision/location only.
 for row,route_row in zip(PANEL,R['routing']):
  raw=disk_answer(entries[route_row['selected']],row['question'])
  wrong_locations=[loc for code,device,*locs in FAMILIES if code==row['code'] for loc in locs if loc!=row['expected']]
  valid=(row['expected'].casefold() in raw.casefold()) and not any(loc.casefold() in raw.casefold() for loc in wrong_locations)
  rec={'id':row['id'],'selected':route_row['selected'],'expected':row['expected'],'raw':raw,'strict_correct':valid,'routing_correct':route_row['hit1']}
  R['qa'].append(rec);save();log('PHYSICAL_QA',json.dumps(rec,ensure_ascii=False))
 # Open-set: no special threshold, do not pretend routing knows missing evidence.
 for row in UNKNOWN:
  q=query_h3(row['question']);ordered,scores=route(q,banks)
  raw=disk_answer(entries[ordered[0]],row['question'])
  rec={'question':row['question'],'reason':row['reason'],'selected':ordered[0],
       'top1_score':round(scores[ordered[0]],8),'margin':round(scores[ordered[0]]-scores[ordered[1]],8),
       'raw':raw,'explicit_unknown':raw.strip().upper().startswith('UNKNOWN')}
  R['unknown'].append(rec);save();log('UNKNOWN_CONTROL',json.dumps(rec,ensure_ascii=False))
 # Causal controls: same question with no cartridge and wrong-revision cartridge.
 control=PANEL[0];q0=control['question']
 baseline=answer(None,q0)
 wrong_id='C01_R2'
 wrong=disk_answer(entries[wrong_id],q0)
 correct=disk_answer(entries[control['id']],q0)
 R['controls']=[{'type':'NO_MEMORY','question':q0,'raw':baseline},
                {'type':'WRONG_REVISION','cartridge':wrong_id,'question':q0,'raw':wrong},
                {'type':'CORRECT_REVISION','cartridge':control['id'],'question':q0,'raw':correct}]
 for item in R['controls']:log('CAUSAL_CONTROL',json.dumps(item,ensure_ascii=False))
 # Locked reference vs direct CUT3 80-layer K/V parity on disk-loaded C01_R1.
 cp=safe_load(entries['C01_R1']);gpu_cp=to_gpu(cp)
 log('REFERENCE_INIT_C01_R1')
 ref=initialize(gpu_cp);ref_seals=memory_seals(ref)
 del ref;release()
 log('DIRECT_INIT_C01_R1')
 direct=initialize_native(gpu_cp);direct_seals=memory_seals(direct)
 check('REFERENCE_DIRECT_80_LAYER_EXACT',compare_seals(ref_seals,direct_seals),{'matched':sum(a==b for a,b in zip(ref_seals,direct_seals)),'layers':NL})
 del direct,gpu_cp,cp;release()
 check('WEIGHTS_SENTINEL_UNCHANGED',sentinel()==before)
 R['summary']={'routing':R['routing_summary'],'qa_strict':sum(x['strict_correct'] for x in R['qa']),
               'qa_n':len(R['qa']),'unknown_explicit':sum(x['explicit_unknown'] for x in R['unknown']),
               'unknown_n':len(R['unknown'])}
 R['status']='COMPLETE_HARD_NEGATIVES_MEASURED';save()
 log('TEST722_RESULT',R['status']);log('SUMMARY',R['summary']);log('RESULT_JSON',OUT,'MANIFEST',MANIFEST,'LOG',LOG)
except Exception as exc:
 R['status']='ERROR';R['error']=repr(exc);R['traceback']=traceback.format_exc();save();log('TEST722_ERROR',R['traceback']);raise
finally:save()
