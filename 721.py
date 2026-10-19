# AKBASCORE PROMETHEUS — TEST721 / Native H3 numeric addressing and SHA lineage
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
ROOT=Path('/content/AKBASCORE_TEST721' if Path('/content').exists() else '/tmp/AKBASCORE_TEST721');ROOT.mkdir(parents=True,exist_ok=True)
LOG=ROOT/'TEST721.log';OUT=ROOT/'TEST721_results.json';LOG.write_text('')
TEST='721';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
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
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST721'}),timeout=120) as f:b=f.read(limit+1)
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
# TEST721 — NUMERICAL H3 ADDRESS BANK + EXACT SOURCE PROVENANCE + PHYSICAL CUT3 RELOAD
# Preserve locked TEST709 forge/initialize and TEST720 direct-forward integration.
# Corpus is synthetic and fixed BEFORE questions; gold labels are evaluation-only.
# Native retrieval is not allowed to read the answer key or provenance page label.
# ============================================================================================================
import numpy as np
CART_DIR=ROOT/'physical_cartridges';CART_DIR.mkdir(parents=True,exist_ok=True)
MANIFEST=ROOT/'TEST721_manifest.json'
MAX_BANK_ROWS=96;QUERY_LIMIT=96;TOP_K=3
CASES=[
 ("C01","The Alderfall coolant regulator uses the code AX-731. The regulator is stored in the north archive.","Where is the AX-731 coolant regulator stored?","north archive"),
 ("C02","The Brindle torque controller uses the code BT-962. The controller is stored in the slate pavilion.","Where is the BT-962 torque controller stored?","slate pavilion"),
 ("C03","The Cedarpoint servo monitor uses the code DN-348. The monitor is stored in the willow chamber.","Where is the DN-348 servo monitor stored?","willow chamber"),
 ("C04","The Dunewell pressure sensor uses the code EV-415. The sensor is stored in the amber vault.","Where is the EV-415 pressure sensor stored?","amber vault"),
 ("C05","The Eastmere spindle driver uses the code FK-276. The driver is stored in the copper annex.","Where is the FK-276 spindle driver stored?","copper annex"),
 ("C06","The Fernridge motor coupler uses the code GL-583. The coupler is stored in the river gallery.","Where is the GL-583 motor coupler stored?","river gallery"),
 ("C07","The Grayhaven encoder uses the code HM-824. The encoder is stored in the quartz station.","Where is the HM-824 encoder stored?","quartz station"),
 ("C08","The Hollowcrest feed controller uses the code JP-139. The controller is stored in the cedar bay.","Where is the JP-139 feed controller stored?","cedar bay"),
 ("C09","The Ironmere relay module uses the code KR-657. The module is stored in the silver depot.","Where is the KR-657 relay module stored?","silver depot"),
 ("C10","The Juniperfield axis converter uses the code LS-902. The converter is stored in the moss chamber.","Where is the LS-902 axis converter stored?","moss chamber")
]
UNKNOWN_QUESTIONS=[
 "Where is the ZZ-000 optical transceiver stored?",
 "Which vault holds the nonexistent PX-000 calibration cube?"
]
R['method']='TEST720 direct CUT3 + TEST716 native H3 addressing + exact rerank + SHA-256 physical cartridge lineage'
R['limitations']=['Frozen 72B; no fine-tuning','Numerical routing scores are not truth scores','SHA verifies cartridge bytes, not factual veracity','Synthetic labels may be memorized only from this run, but model pretraining cannot be fully ruled out','TEST721 does not establish autonomous reasoning or APPEND parity','Top-k is a candidate ranking; UNKNOWN requires separate evidence checks']
R['routing']=[]
R['physical_reloads']=[]
R['negative_controls']=[]
R['measurements']={}
def sha_file(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def atomic_json(path,obj):
 tmp=Path(str(path)+'.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=str),encoding='utf-8');tmp.replace(path)
def safe_load_cartridge(entry):
 path=CART_DIR/entry['file']
 check('FILE_SHA_'+entry['id'],path.exists() and sha_file(path)==entry['file_sha256'])
 cp=torch.load(path,map_location='cpu',weights_only=True)
 check('CART_SHAPE_'+entry['id'],cp['book_id']==entry['id'] and cp['p']==P and cp['n']==P+cp['body_tokens'] and cp['h'].shape==(1,cp['n'],H) and len(cp['lower'])==CUT+1)
 check('CART_TENSOR_SHA_'+entry['id'],json.dumps(seal_cp(cp),sort_keys=True)==json.dumps(entry['tensor_sha256'],sort_keys=True))
 return cp
def normalize(x):
 x=np.asarray(x,dtype=np.float32)
 return x/np.maximum(np.linalg.norm(x,axis=-1,keepdims=True),1e-8)
def make_bank(cp):
 # Keep exact 8192D native H3 rows. Prefix is excluded.
 x=cp['h'][0,P:,:].float()
 check('NONEMPTY_H3_'+cp['book_id'],x.shape[0]>0)
 idx=np.linspace(0,len(x)-1,min(MAX_BANK_ROWS,len(x)),dtype=np.int64)
 return normalize(x[torch.from_numpy(idx)].numpy())
@torch.no_grad()
def query_h3(question):
 # Only the question reaches the model. No source text, gold labels, or page indices.
 s='<|im_start|>user\n'+question+'\n<|im_end|>\n<|im_start|>assistant\n'
 ids=tok(s,add_special_tokens=False).input_ids
 check('QUERY_LIMIT_'+str(len(R['routing'])+len(R['negative_controls'])),len(ids)<=QUERY_LIMIT,len(ids))
 captured=[]
 with DirectCut3(model.model.layers[CUT],'capture',collector=captured):
  out=model(input_ids=torch.tensor([ids],device=DEV),use_cache=False,return_dict=True)
  del out
 check('QUERY_CAPTURE',len(captured)==1)
 return normalize(captured[0][0].float().numpy())
def native_score(q,bank):
 # TEST716 TOP2-inspired native score, no PCA fitting and no gold supervision.
 # For each query token, take its two strongest bank positions.
 sim=q@bank.T
 n=min(2,sim.shape[1])
 peaks=np.partition(sim,-n,axis=1)[:,-n:]
 return float(peaks.mean(axis=1).mean())
def route(q,banks):
 scores={key:native_score(q,bank) for key,bank in banks.items()}
 ordered=sorted(scores,key=lambda key:(-scores[key],key))
 return ordered,{key:round(scores[key],8) for key in ordered}
def physical_answer(entry,question):
 cp=safe_load_cartridge(entry)
 gpu_cp=to_gpu(cp)
 del cp
 memory=initialize_native(gpu_cp)
 check('RELOAD_80_LAYERS_'+entry['id'],len(memory)==NL)
 raw=answer(memory,question)
 del memory,gpu_cp
 release()
 return raw
def no_memory_answer(question):
 # Locked TEST709 answer(None, question) as a pretraining/no-cartridge control.
 raw=answer(None,question)
 release()
 return raw
try:
 log('='*108);log('AKBASCORE PROMETHEUS — TEST721 — H3 NUMERICAL ADDRESSING / SHA LEDGER / PHYSICAL RELOAD');log('='*108)
 check('CUDA_AVAILABLE',torch.cuda.is_available(),{'torch':torch.__version__,'cuda':torch.version.cuda})
 check('ONE_GPU',torch.cuda.device_count()==1)
 check('A100_80GB',torch.cuda.get_device_properties(0).total_memory>=70*2**30,torch.cuda.get_device_name(0))
 check('RESERVE',GPU_RESERVE_GIB>=9 and 32<=CHUNK<=512)
 raw709=download(SRC709);raw716=download(SRC716)
 check('709_GIT_BLOB_LOCK',gitblob(raw709)==LOCK709,gitblob(raw709))
 check('716_GIT_BLOB_LOCK',gitblob(raw716)==LOCK716,gitblob(raw716))
 import_reference(raw709)
 R['environment']={'python':platform.python_version(),'torch':torch.__version__,'transformers':transformers.__version__,'bitsandbytes':bitsandbytes.__version__,'gpu':torch.cuda.get_device_name(0)}
 tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
 PREFIX='<|im_start|>system\nUse only the available document memory for document-specific questions. If the evidence is missing, say UNKNOWN.\n<|im_end|>\n<|im_start|>user\nINFORMATION:\n'
 PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
 quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
 log('LOAD_FROZEN_72B_NF4')
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
 for param in model.parameters():param.requires_grad_(False)
 cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
 check('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,[NL,H,QH,KVH,HD])
 check('FROZEN',all(not p.requires_grad for p in model.parameters()))
 check('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
 check('DIRECT_FORWARD_NO_EXISTING_HOOKS',not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
 before=sentinel();R['weight_sentinel_before']=before
 log('MODEL_READY',gpu())
 # The answer key is sealed separately and never passed to routing or the model.
 panel=[{'id':cid,'question':q,'expected':expected} for cid,body,q,expected in CASES]
 panel_sha=sha(json.dumps(panel,sort_keys=True,ensure_ascii=False).encode())
 R['sealed_panel_sha256']=panel_sha
 manifest={'test':TEST,'model':MODEL_ID,'cut':CUT,'prefix_sha256':sha(PREFIX.encode()),'sources':{'709':LOCK709,'716':LOCK716},'cartridges':[]}
 banks={}
 # Each cartridge is a physically saved CPU H3 + L0-L3 K/V file; immutable after commit.
 for cid,body,question,expected in CASES:
  log('FORGE_NATIVE',cid)
  ids=tok(body,add_special_tokens=False).input_ids
  cp,seconds=forge_native(ids,cid)
  check('BODY_TOKENS_'+cid,cp['body_tokens']==len(ids))
  filename=cid+'.pt';path=CART_DIR/filename
  # Write to temporary file and rename atomically.
  temp=path.with_suffix('.pt.tmp')
  torch.save(cp,temp)
  temp.replace(path)
  entry={'id':cid,'file':filename,'file_sha256':sha_file(path),'tensor_sha256':seal_cp(cp),'body_sha256':sha(body.encode()),'body_tokens':len(ids),'n':cp['n'],'prefix_tokens':P,'forge_seconds':seconds}
  banks[cid]=make_bank(cp)
  manifest['cartridges'].append(entry)
  atomic_json(MANIFEST,manifest)
  log('PHYSICAL_COMMIT',cid,entry['file_sha256'],'tokens',cp['n'],'forge_s',seconds)
  del cp
  release()
 check('TEN_PHYSICAL_CARTRIDGES',len(manifest['cartridges'])==10)
 check('TEN_UNIQUE_SHA256',len({e['file_sha256'] for e in manifest['cartridges']})==10)
 # Re-read committed manifest from disk, not the live object.
 ledger=json.loads(MANIFEST.read_text(encoding='utf-8'))
 check('MANIFEST_RELOAD',len(ledger['cartridges'])==10 and ledger['prefix_sha256']==sha(PREFIX.encode()))
 for e in ledger['cartridges']:
  cp=safe_load_cartridge(e)
  # Verify that bank recomputation from disk matches the original RAM bank.
  rebuilt=make_bank(cp)
  check('BANK_DISK_PARITY_'+e['id'],np.array_equal(rebuilt,banks[e['id']]))
  del cp,rebuilt
 # Router reads ONLY question H3 + memory H3 banks; never the gold answer.
 for row in panel:
  question=row['question'];q=query_h3(question);ordered,scores=route(q,banks)
  selected=ordered[0]
  record={'question':question,'selected':selected,'top3':ordered[:TOP_K],'scores':scores,'gold_cartridge':row['id'],'hit1':selected==row['id'],'hit3':row['id'] in ordered[:TOP_K]}
  R['routing'].append(record);save()
  log('ROUTE',json.dumps(record,ensure_ascii=False))
 R['routing_summary']={'r1':sum(r['hit1'] for r in R['routing']),'r3':sum(r['hit3'] for r in R['routing']),'n':len(R['routing'])}
 log('ROUTING_SUMMARY',R['routing_summary'])
 # Evidence is physically loaded only after numerical routing; evaluate TOP1 and GOLD separately.
 by_id={e['id']:e for e in ledger['cartridges']}
 for row,route_record in zip(panel,R['routing']):
  q=row['question'];chosen=route_record['selected']
  raw=physical_answer(by_id[chosen],q)
  # Independent expected string check is evaluation only; it cannot affect routing or generation.
  correct=row['expected'].casefold() in raw.casefold()
  result={'question':q,'selected':chosen,'gold':row['id'],'raw':raw,'expected':row['expected'],'contains_expected':correct,'routing_correct':chosen==row['id']}
  R['physical_reloads'].append(result);save()
  log('PHYSICAL_RELOAD_QA',json.dumps(result,ensure_ascii=False))
 # Controls: same query without physical memory, and absent-key queries.
 for question in UNKNOWN_QUESTIONS:
  q=query_h3(question);ordered,scores=route(q,banks)
  # Ranking always returns something; do not mislabel this as detection of missing evidence.
  raw=physical_answer(by_id[ordered[0]],question)
  row={'question':question,'selected':ordered[0],'raw':raw,'expected_behavior':'UNKNOWN','explicit_unknown':raw.strip().upper().startswith('UNKNOWN'),'scores':scores}
  R['negative_controls'].append(row);save()
  log('UNKNOWN_CONTROL',json.dumps(row,ensure_ascii=False))
 # Causal comparison for the first query: selected physical memory versus no memory.
 q0=panel[0]['question']
 R['no_memory_control']={'question':q0,'raw':no_memory_answer(q0)}
 log('NO_MEMORY_CONTROL',R['no_memory_control'])
 # Reference TEST709 vs native initialize on disk-restored C01, exact all 80 layers.
 cp=safe_load_cartridge(by_id['C01']);gpu_cp=to_gpu(cp)
 log('REFERENCE_INIT_C01')
 ref=initialize(gpu_cp);seals_ref=memory_seals(ref)
 del ref
 release()
 log('NATIVE_INIT_C01')
 nat=initialize_native(gpu_cp);seals_nat=memory_seals(nat)
 check('REFERENCE_NATIVE_80_LAYER_EXACT',compare_seals(seals_ref,seals_nat),{'matched':sum(a==b for a,b in zip(seals_ref,seals_nat)),'layers':NL})
 del nat,gpu_cp,cp
 release()
 check('WEIGHTS_SENTINEL_UNCHANGED',sentinel()==before)
 R['semantic_summary']={'correct_selected':sum(r['contains_expected'] for r in R['physical_reloads']),'n':len(R['physical_reloads']),'unknown_explicit':sum(r['explicit_unknown'] for r in R['negative_controls']),'unknown_n':len(R['negative_controls'])}
 R['status']='COMPLETE_ADDRESSING_AND_PROVENANCE_MEASURED'
 save()
 log('TEST721_RESULT',R['status'])
 log('ROUTING',R['routing_summary'],'SEMANTIC',R['semantic_summary'])
 log('RESULT_JSON',OUT,'MANIFEST',MANIFEST,'LOG',LOG)
except Exception as exc:
 R['status']='ERROR';R['error']=repr(exc);R['traceback']=traceback.format_exc();save();log('TEST721_ERROR',R['traceback']);raise
finally:
 save()
