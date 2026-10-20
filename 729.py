# AKBASCORE PROMETHEUS — TEST729 / Native H3 numeric addressing and SHA lineage
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
ROOT=Path('/content/AKBASCORE_TEST729' if Path('/content').exists() else '/tmp/AKBASCORE_TEST729');ROOT.mkdir(parents=True,exist_ok=True)
LOG=ROOT/'TEST729.log';OUT=ROOT/'TEST729_results.json';LOG.write_text('')
TEST='729';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
DTYPE=torch.bfloat16;DEV=torch.device('cuda:0');CHUNK=128;MAX_NEW=192;GPU_RESERVE_GIB=9.0
SRC709='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/709.py'
SRC716='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/716.py'
LOCK709='6c9f8cbb1eeed848d45133d73f0d7676b68e9125';LOCK716='913fa7a4951f2072df4be2eb49120ea86efa5477'
R={'test':TEST,'status':'STARTED','method':'native CUT3 physical domain synthesis','source_links':[SRC709,SRC716],'checks':[],'measurements':{},'limitations':['Not executed on GPU by code author','This validates CUT3 capture and initialize only; append parity is a separate acceptance gate','Direct layer.forward integration is hook-free but not a compiled C++/CUDA runtime','Greedy answer agreement does not prove semantic correctness']}
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
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST729'}),timeout=120) as f:b=f.read(limit+1)
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
# TEST729 — DOMAIN SYNTHESIS / PHYSICAL RE-ENCODING / ISOLATED RELOAD
# Locked 709 engine, proven 721 direct CUT3, disk SHA ledger, no training or answer-dependent routing.
# The router is deliberately UNCHANGED from TEST721: top2 token-to-native-H3 cosine.
# A scored absent query must not be called UNKNOWN merely because its nearest cartridge is weak.
# ============================================================================================================
import numpy as np
from collections import defaultdict
CART_DIR=ROOT/'physical_cartridges';CART_DIR.mkdir(parents=True,exist_ok=True)
MANIFEST=ROOT/'TEST729_manifest.json'
QUERY_LIMIT=128;MAX_BANK_ROWS=96;TOP_K=5
# Distinct location facts. Two versions of the same asset and nearby misleading records.
# Answers and routing gold never enter model input or routing scores.
# Three topic domains. The hidden target values are not embedded in synthesis prompts.
# These are synthetic engineering records, not certified operating limits.
DOMAIN={
 'S01':('ELECTRICAL',[
  ('C01','The AX-731 drive has a nominal DC bus voltage of 540 volts.','540 volts'),
  ('C02','The AX-731 drive continuous current rating is 18 amperes.','18 amperes'),
  ('C03','The AX-731 drive overcurrent trip threshold is 24 amperes.','24 amperes')]),
 'S02':('MECHANICAL',[
  ('C04','The AX-731 actuator rated output torque is 12 newton meters.','12 newton meters'),
  ('C05','The AX-731 actuator reduction gearbox ratio is 5 to 1.','5 to 1'),
  ('C06','The AX-731 axis maximum mechanical speed is 1200 rpm.','1200 rpm')]),
 'S03':('SOFTWARE',[
  ('C07','The AX-731 PLC samples the drive current every 10 milliseconds.','10 milliseconds'),
  ('C08','The AX-731 PLC raises fault F17 when measured current exceeds 24 amperes.','F17'),
  ('C09','The AX-731 PLC fault F17 requires manual reset after current returns below threshold.','manual reset')])
}
CASES=[];PANEL=[]
for domain,(topic,items) in DOMAIN.items():
 for cid,body,expected in items:
  CASES.append((cid,f'AX-731 {topic} evidence record {cid}. {body}',domain,'SOURCE',expected))
  PANEL.append({'id':cid,'domain':domain,'expected':expected})
R['method']='Locked 728 native CUT3 -> S01/S02/S03 -> H01/H02 -> independently reloadable C11 master cartridge'
R['limitations']=['Not GPU-executed by code author','C11 is generated from model-authored text derived from physically read parent cartridges, then re-encoded to native CUT3 H3/KV; NOT direct tensor-to-tensor fusion','Independent reload is within the same model process after removing source cartridges from the active registry; a fresh-process restart is not proven','H3 graph is numerical address routing with specified lineage edges, not learned synapses','No gold answers inserted into C11 synthesis prompts','Synthetic AX-731 engineering values are fixtures, not equipment safety limits','The model may contain prior knowledge; no-memory baseline is measured','No simultaneous multi-cartridge joint KV inference is claimed']
R['domain_results']=[];R['source_results']=[]
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
# RAM graph: numerical native H3 addresses, explicitly typed lineage edges and dynamic activation.
# SSD remains the sole source of actual H3 + lower-layer K/V payloads.
EDGES={'S01':['C01','C02','C03'],'S02':['C04','C05','C06'],'S03':['C07','C08','C09'],
       'H01':['S01','S02'],'H02':['S02','S03'],'C11':['H01','H02','S01','S02','S03']}
TOPICS={'S01':'electrical','S02':'mechanical','S03':'software','H01':'electrical-mechanical','H02':'mechanical-software','C11':'master electrical-mechanical-software'}
QUERIES={
 'C01':'What is the AX-731 nominal DC bus voltage?',
 'C02':'What is the AX-731 continuous current rating?',
 'C03':'What is the AX-731 overcurrent trip threshold?',
 'C04':'What is the AX-731 actuator rated output torque?',
 'C05':'What is the AX-731 gearbox reduction ratio?',
 'C06':'What is the AX-731 maximum mechanical axis speed?',
 'C07':'How often does the AX-731 PLC sample drive current?',
 'C08':'What fault code is raised when AX-731 drive current exceeds 24 amperes?',
 'C09':'What reset is required after AX-731 fault F17?',
}
HYBRID_QUESTIONS={
 'H01':['How does the AX-731 drive continuous current rating compare to its overcurrent trip threshold?',
        'Which electrical and mechanical specifications describe the AX-731 drive and actuator together?'],
 'H02':['What does the AX-731 PLC do when current exceeds 24 amperes, and what reset is required?',
        'Which mechanical axis speed and PLC current monitoring interval are specified for AX-731?']}
R['graph']={'edges':EDGES,'coordinates':'native H3 sampled BF16 activation rows normalized to float32; exact H3 model boundary','activation':'query H3 top-2 cosine with H3 row bank; typed graph lineage expansion','persisted_payload':'native CUT3 physical cartridges on SSD'}
R['hybrid_results']=[];R['routing_results']=[];R['recovery_results']=[]

def graph_bank(entry):
 cp=safe_load(entry)
 try:return bank_from(cp)
 finally:del cp;release()
def activated(question,banks,available,seed=None):
 q=query_h3(question);ranking,scores=route(q,{k:banks[k] for k in available})
 if seed is None:seed=ranking[0]
 path=[seed];front=[seed]
 while front:
  u=front.pop(0)
  for v in EDGES.get(u,[]):
   if v in available and v not in path:path.append(v);front.append(v)
 return {'question':question,'seed':seed,'selected':path,'top5':ranking[:5],
         'scores':{k:round(float(scores[k]),7) for k in ranking[:5]}}
def physical_read(cid,question):return disk_answer(entries[cid],question)
def synthesis_note(title,reads):
 prompt=('Produce a standalone AX-731 '+title+' engineering synthesis using ONLY the physical neural-memory readouts below. '
 'Keep every numeric value and all technical conditions, and retain the bracketed cartridge identifiers for provenance. '
 'Clearly distinguish documented facts from any deductions. Do not invent missing specifications. '
 'Output only the integrated technical memory.\n'+ '\n'.join('['+x['id']+'] '+x['raw'] for x in reads)+'\nINTEGRATED MEMORY:')
 return answer(None,prompt).strip()
try:
 log('='*110);log('AKBASCORE PROMETHEUS — TEST729 — C11 MASTER INDEPENDENT PHYSICAL RELOAD + S01/S02/S03 + H01/H02');log('='*110)
 check('CUDA_AVAILABLE',torch.cuda.is_available(),{'torch':torch.__version__,'cuda':torch.version.cuda})
 check('ONE_GPU',torch.cuda.device_count()==1)
 check('A100_80GB',torch.cuda.get_device_properties(0).total_memory>=70*2**30,torch.cuda.get_device_name(0))
 raw709=download(SRC709);raw716=download(SRC716)
 check('709_GIT_BLOB_LOCK',gitblob(raw709)==LOCK709,gitblob(raw709))
 check('716_GIT_BLOB_LOCK',gitblob(raw716)==LOCK716,gitblob(raw716))
 import_reference(raw709)
 tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
 PREFIX='<|im_start|>system\\nUse only the available document memory for document-specific questions. If the evidence is missing, say UNKNOWN.\\n<|im_end|>\\n<|im_start|>user\\nINFORMATION:\\n'
 PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
 quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
 for parameter in model.parameters():parameter.requires_grad_(False)
 cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
 check('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,[NL,H,QH,KVH,HD])
 check('FROZEN',all(not p.requires_grad for p in model.parameters()))
 check('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
 check('DIRECT_FORWARD_NO_EXISTING_HOOKS',not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
 before=sentinel();R['panel_sha256']=sha(json.dumps(PANEL,sort_keys=True).encode())
 ledger={'test':TEST,'sources':{'709':LOCK709,'716':LOCK716},'model':MODEL_ID,'cut':CUT,'prefix_sha256':sha(PREFIX.encode()),'cartridges':[],'edges':EDGES};entries={};banks={}
 def commit(cid,body,role):
  ids=tok(body,add_special_tokens=False).input_ids
  cp,seconds=forge_native(ids,cid)
  path=CART_DIR/(cid+'.pt');tmp=Path(str(path)+'.tmp');torch.save(cp,tmp);tmp.replace(path)
  entry={'id':cid,'role':role,'file':path.name,'sha256':sha_file(path),'tensor_sha':seal_cp(cp),
         'body_sha256':sha(body.encode()),'body_tokens':len(ids),'forge_s':seconds}
  ledger['cartridges'].append(entry);entries[cid]=entry;atomic_json(MANIFEST,ledger)
  banks[cid]=bank_from(cp)
  del cp;release();log('PHYSICAL_COMMIT',cid,role,entry['sha256'])
 # Phase 1: nine immutable base evidence cartridges on SSD; RAM gets only H3 coordinate banks.
 for cid,body,domain,_,expected in CASES:commit(cid,body,'SOURCE_'+domain)
 check('SOURCE_CARTRIDGES_9',len(entries)==9)
 for domain,(topic,items) in DOMAIN.items():
  evidence=[]
  for cid,body,expected in items:
   question=QUERIES[cid]
   raw=physical_read(cid,question)
   rec={'domain':domain,'id':cid,'question':question,'raw':raw,'expected':expected,
        'expected_found':expected.lower() in raw.lower()}
   evidence.append(rec);R['source_results'].append(rec);save();log('SOURCE_READ',json.dumps(rec,ensure_ascii=False))
  synth=synthesis_note(topic.lower()+' domain',evidence)
  check('NONEMPTY_SYNTHESIS_'+domain,25<len(synth)<6000,len(synth))
  commit(domain,'AX-731 '+topic+' integrated neural memory. '+synth,'DOMAIN_SYNTHESIS')
  tests=[]
  for cid,body,expected in items:
   question=QUERIES[cid];raw=physical_read(domain,question)
   tests.append({'id':cid,'question':question,'expected':expected,'raw':raw,'hit':expected.lower() in raw.lower()})
  missing=physical_read(domain,'What is the official serial number of AX-731? If not documented, answer UNKNOWN.')
  rec={'domain':domain,'synthesis':synth,'synthesis_sha256':sha(synth.encode()),'readback':tests,
       'readback_hits':sum(x['hit'] for x in tests),'missing_raw':missing,'missing_unknown':missing.strip().upper().startswith('UNKNOWN')}
  R['domain_results'].append(rec);save();log('DOMAIN_RESULT',json.dumps(rec,ensure_ascii=False))
 check('DOMAIN_CARTRIDGES_3',all(x in entries for x in DOMAIN))
 # Phase 2: H01/H02 use domain-node physical readouts and original SSD detail nodes.
 # No gold answer is inserted in the model prompts. Original evidence is never destroyed.
 for hid,parents in [('H01',['S01','S02']),('H02',['S02','S03'])]:
  reads=[]
  for parent in parents:
   q='List all AX-731 '+TOPICS[parent]+' technical specifications, numbers and conditions in the available memory.'
   reads.append({'id':parent,'raw':physical_read(parent,q),'question':q,'role':'domain'})
  for parent in parents:
   for cid,body,expected in DOMAIN[parent][1]:
    q=QUERIES[cid];reads.append({'id':cid,'raw':physical_read(cid,q),'question':q,'role':'original evidence'})
  hybrid=synthesis_note('cross-domain '+TOPICS[hid]+' relations',reads)
  check('NONEMPTY_SYNTHESIS_'+hid,25<len(hybrid)<10000,len(hybrid))
  commit(hid,'AX-731 '+TOPICS[hid]+' integrated cross-domain neural memory. '+hybrid,'CROSS_DOMAIN_SYNTHESIS')
  checks=[]
  for q in HYBRID_QUESTIONS[hid]:
   raw=physical_read(hid,q);checks.append({'question':q,'raw':raw,'unknown':raw.strip().upper().startswith('UNKNOWN')})
  # Probe every leaf fact: identify exactly what the hybrid alone retains.
  leaf=[]
  for parent in parents:
   for cid,body,expected in DOMAIN[parent][1]:
    raw=physical_read(hid,QUERIES[cid]);leaf.append({'id':cid,'expected':expected,'raw':raw,'hit':expected.lower() in raw.lower()})
  rec={'hybrid':hid,'parents':parents,'synthesis':hybrid,'readouts':reads,'hybrid_questions':checks,
       'leaf_probes':leaf,'leaf_hits':sum(x['hit'] for x in leaf)}
  R['hybrid_results'].append(rec);save();log('HYBRID_RESULT',json.dumps(rec,ensure_ascii=False))
 check('HYBRID_CARTRIDGES_2',all(x in entries for x in ('H01','H02')))
 # Phase 3: C11 master: independently model-written sections grounded ONLY in native physical cartridge readouts.
 # Parent H01 can lose mechanical details (TEST727), so retain S01/S02/S03 and leaf evidence as sources.
 # Never put expected answers from the gold panel into prompts; read physical cartridges only.
 C11_PARENT_IDS=['H01','H02','S01','S02','S03']
 C11_SOURCE_IDS=[x[0] for x in CASES]
 R['c11_lineage']={'parents':C11_PARENT_IDS,'sources':C11_SOURCE_IDS,
   'parent_file_sha256':{cid:entries[cid]['sha256'] for cid in C11_PARENT_IDS},
   'source_file_sha256':{cid:entries[cid]['sha256'] for cid in C11_SOURCE_IDS}}
 master_sections=[]
 for domain,(topic,items) in DOMAIN.items():
  reads=[]
  parent_q='List the AX-731 '+topic.lower()+' specifications, numbers, and conditions in available memory.'
  reads.append({'id':domain,'raw':physical_read(domain,parent_q)})
  for cid,body,expected in items:
   reads.append({'id':cid,'raw':physical_read(cid,QUERIES[cid])})
  # The LLM, not a code-side answer key, writes the master section.
  prompt=('Write one concise self-contained section for a physical AX-731 master neural-memory cartridge. '
   'Use ONLY the following native neural-cartridge readouts. Include EVERY documented technical value, '
   'its units, its operating condition, and source IDs. No new facts, no external knowledge. '
   'Limit the output to 110 words. Output only the section.\n'
   +'\n'.join('['+r['id']+'] '+r['raw'] for r in reads)+'\nMASTER SECTION:')
  section=answer(None,prompt).strip()
  check('C11_SECTION_NONEMPTY_'+domain,len(section)>30 and len(section)<3000,len(section))
  master_sections.append({'domain':domain,'text':section,'sha256':sha(section.encode()),'sources':[r['id'] for r in reads]})
  log('C11_SECTION',json.dumps(master_sections[-1],ensure_ascii=False))
 # Separate cross-domain bridge readouts ensure the master also includes relationships.
 bridge=[]
 for hid,question in [('H01','Which electrical and mechanical specifications describe the AX-731 drive and actuator together?'),
                       ('H02','Which mechanical axis speed and PLC current monitoring interval are specified for AX-731?')]:
  bridge.append({'id':hid,'raw':physical_read(hid,question)})
 bridge_prompt=('Produce a concise cross-domain master relation note using ONLY these two native neural-memory '
  'readouts. Preserve source labels, do not invent values; mark unknowns explicitly. Limit to 100 words.\n'
  +'\n'.join('['+r['id']+'] '+r['raw'] for r in bridge)+'\nMASTER RELATIONS:')
 bridge_text=answer(None,bridge_prompt).strip()
 check('C11_BRIDGE_NONEMPTY',len(bridge_text)>20,len(bridge_text))
 # Sections are model-authored; concatenation is a storage operation, not hand-written facts.
 master_body=('AX-731 C11 MASTER NEURAL MEMORY. Standalone engineering memory from verified physical '
  'cartridges. Source provenance is indicated by bracketed IDs.\n\n'
  +'\n\n'.join('DOMAIN '+x['domain']+'\n'+x['text'] for x in master_sections)
  +'\n\nCROSS-DOMAIN RELATIONS\n'+bridge_text)
 R['master_sections']=master_sections;R['master_bridge']={'text':bridge_text,'sha256':sha(bridge_text.encode())}
 R['c11_master_body_sha256']=sha(master_body.encode());R['c11_master_body_tokens']=len(tok(master_body,add_special_tokens=False).input_ids)
 check('C11_MASTER_BODY_NONEMPTY',len(master_body)>150 and len(master_body)<12000,len(master_body))
 commit('C11',master_body,'MASTER_PHYSICAL_SYNTHESIS')
 ledger['edges']=EDGES;ledger['c11_lineage']=R['c11_lineage'];ledger['c11_master_body_sha256']=R['c11_master_body_sha256']
 atomic_json(MANIFEST,ledger)
 check('SSD_PHYSICAL_CARTRIDGES_15',len(entries)==15 and all((CART_DIR/(cid+'.pt')).exists() for cid in entries))
 # Phase 4: BEFORE isolation, establish no-memory baseline (same frozen model, no cartridge).
 C11_PANEL=[{'id':cid,'question':QUERIES[cid],'expected':expected,'domain':domain}
            for domain,(_,items) in DOMAIN.items() for cid,body,expected in items]
 CROSS_PANEL=[
  {'id':'X01','question':'For AX-731, give both nominal DC bus voltage and actuator rated output torque.', 'expected':['540 volts','12 newton meters']},
  {'id':'X02','question':'For AX-731, give both continuous current rating and gearbox reduction ratio.', 'expected':['18 amperes','5 to 1']},
  {'id':'X03','question':'For AX-731, give both overcurrent trip threshold and maximum mechanical axis speed.', 'expected':['24 amperes','1200 rpm']},
  {'id':'X04','question':'For AX-731, give both actuator rated output torque and PLC sampling interval.', 'expected':['12 newton meters','10 milliseconds']},
  {'id':'X05','question':'For AX-731, give both gearbox reduction ratio and PLC overcurrent fault code.', 'expected':['5 to 1','F17']},
  {'id':'X06','question':'For AX-731, give both maximum mechanical axis speed and reset procedure for fault F17.', 'expected':['1200 rpm','manual reset']}
 ]
 UNKNOWN_PANEL=['What is the AX-731 factory serial number? If absent, answer UNKNOWN.',
                'What is the AX-731 factory calibration date? If absent, answer UNKNOWN.']
 R['c11_panel_sha256']=sha(json.dumps({'leaf':C11_PANEL,'cross':CROSS_PANEL,'unknown':UNKNOWN_PANEL},sort_keys=True).encode())
 baseline=[]
 for case in C11_PANEL:
  raw=answer(None,case['question']);baseline.append({'id':case['id'],'raw':raw,'hit':case['expected'].lower() in raw.lower()})
 R['no_memory_baseline']=baseline;save();log('C11_NO_MEMORY_BASELINE',json.dumps(baseline,ensure_ascii=False))
 # Remove all 14 non-master cartridge entries and H3 banks from active RAM; SSD files remain immutable.
 saved_entries=dict(entries);saved_banks=dict(banks)
 entries.clear();entries['C11']=saved_entries['C11']
 banks.clear();banks['C11']=saved_banks['C11']
 check('C11_ONLY_ACTIVE_NODE',set(entries)=={'C11'} and set(banks)=={'C11'})
 # Force disk reload each time: no previous memory object or parent cartridge may be consulted.
 R['c11_leaf_readback']=[]
 for case in C11_PANEL:
  raw=physical_read('C11',case['question']);hit=case['expected'].lower() in raw.lower()
  rec={**case,'raw':raw,'hit':hit};R['c11_leaf_readback'].append(rec);save();log('C11_LEAF',json.dumps(rec,ensure_ascii=False))
 R['c11_cross_readback']=[]
 for case in CROSS_PANEL:
  raw=physical_read('C11',case['question']);hits=[v.lower() in raw.lower() for v in case['expected']]
  rec={**case,'raw':raw,'hits':hits,'complete':all(hits)};R['c11_cross_readback'].append(rec);save();log('C11_CROSS',json.dumps(rec,ensure_ascii=False))
 R['c11_unknown_readback']=[]
 for question in UNKNOWN_PANEL:
  raw=physical_read('C11',question);ok=raw.strip().upper().startswith('UNKNOWN')
  rec={'question':question,'raw':raw,'unknown':ok};R['c11_unknown_readback'].append(rec);save();log('C11_UNKNOWN',json.dumps(rec,ensure_ascii=False))
 # Phase 5: exact 80-layer parity and weight sentinel on independently reloaded master.
 cp=safe_load(entries['C11']);cp_gpu=to_gpu(cp)
 ref=initialize(cp_gpu);ref_seals=memory_seals(ref);del ref;release()
 direct=initialize_native(cp_gpu);direct_seals=memory_seals(direct)
 check('C11_80_LAYER_PARITY',compare_seals(ref_seals,direct_seals),
   {'matched':sum(a==b for a,b in zip(ref_seals,direct_seals)),'layers':NL})
 del direct,cp_gpu,cp;release()
 check('WEIGHTS_SENTINEL_UNCHANGED',sentinel()==before)
 # Re-open the complete graph ONLY after isolated master acceptance measurements finish.
 entries.clear();entries.update(saved_entries);banks.clear();banks.update(saved_banks)
 check('SOURCE_AND_SYNTHESIS_SSD_SURVIVE',len(entries)==15 and all((CART_DIR/(cid+'.pt')).exists() for cid in entries))
 summary={'source_readout_hits':sum(x['expected_found'] for x in R['source_results']),
   'domain_semantic_hits':sum(x['readback_hits'] for x in R['domain_results']),
   'domain_semantic_n':sum(len(x['readback']) for x in R['domain_results']),
   'hybrid_leaf_hits':sum(x['leaf_hits'] for x in R['hybrid_results']),
   'hybrid_leaf_n':sum(len(x['leaf_probes']) for x in R['hybrid_results']),
   'ssd_physical_nodes':len(entries),'c11_independent_leaf_hits':sum(x['hit'] for x in R['c11_leaf_readback']),
   'c11_independent_leaf_total':len(C11_PANEL),
   'c11_independent_cross_complete':sum(x['complete'] for x in R['c11_cross_readback']),
   'c11_independent_cross_total':len(CROSS_PANEL),
   'c11_unknown_correct':sum(x['unknown'] for x in R['c11_unknown_readback']),
   'c11_unknown_total':len(UNKNOWN_PANEL),
   'no_memory_baseline_hits':sum(x['hit'] for x in baseline),
   'c11_80_layer_parity':True,'weights_unchanged':True,'ssd_sha_verified':True}
 R['summary']=summary
 # Strict acceptance: all independent master questions and unknown controls must pass.
 # If a gate fails, report MEASURED_NOT_ACCEPTED, do not silently promote to PASS.
 gates={'LEAF_9_9':summary['c11_independent_leaf_hits']==9,
   'CROSS_6_6':summary['c11_independent_cross_complete']==6,
   'UNKNOWN_2_2':summary['c11_unknown_correct']==2,
   'BASELINE_DISTINGUISHABLE':summary['c11_independent_leaf_hits']>summary['no_memory_baseline_hits']}
 R['acceptance_gates']=gates
 for name,ok in gates.items():log('ACCEPT_PASS' if ok else 'ACCEPT_FAIL',name)
 R['status']='PASS_C11_INDEPENDENT_MASTER' if all(gates.values()) else 'MEASURED_C11_NOT_ACCEPTED'
 save();log('TEST729_RESULT',R['status']);log('SUMMARY',summary);log('RESULT_JSON',OUT,'MANIFEST',MANIFEST,'LOG',LOG)
except Exception as exc:
 R['status']='ERROR';R['error']=repr(exc);R['traceback']=traceback.format_exc();save();log('TEST729_ERROR',R['traceback']);raise
finally:save()
