# AKBASCORE PROMETHEUS — TEST727 / Native H3 numeric addressing and SHA lineage
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
ROOT=Path('/content/AKBASCORE_TEST727' if Path('/content').exists() else '/tmp/AKBASCORE_TEST727');ROOT.mkdir(parents=True,exist_ok=True)
LOG=ROOT/'TEST727.log';OUT=ROOT/'TEST727_results.json';LOG.write_text('')
TEST='727';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
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
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST727'}),timeout=120) as f:b=f.read(limit+1)
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
# TEST727 — DOMAIN SYNTHESIS / PHYSICAL RE-ENCODING / ISOLATED RELOAD
# Locked 709 engine, proven 721 direct CUT3, disk SHA ledger, no training or answer-dependent routing.
# The router is deliberately UNCHANGED from TEST721: top2 token-to-native-H3 cosine.
# A scored absent query must not be called UNKNOWN merely because its nearest cartridge is weak.
# ============================================================================================================
import numpy as np
from collections import defaultdict
CART_DIR=ROOT/'physical_cartridges';CART_DIR.mkdir(parents=True,exist_ok=True)
MANIFEST=ROOT/'TEST727_manifest.json'
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
R['method']='Physical native CUT3 source readouts -> model-written domain synthesis -> new native CUT3 synthesis cartridges -> isolated disk reload'
R['limitations']=['Not executed on GPU by code author','S01/S02/S03 and H01/H02 are model-generated textual syntheses re-encoded as native CUT3 H3/KV physical cartridges, NOT a proven tensor-to-tensor merge','RAM spatial graph is a numerical H3 address graph plus explicit lineage edges, NOT trained synapses or a learned manifold','Source cartridges are retained on SSD for lossless detail and causal ablation; domain/hybrid nodes never replace sources','Synthetic engineering values are test fixtures, not real-world equipment specifications','A query is routed by H3 scores with top-k candidates; selecting relevant cartridges does not by itself prove their causal contribution','Multi-node integration here is sequential physical neural readout followed by model synthesis; not simultaneous native multi-cartridge KV composition','No C11 master consolidation in TEST727','No hardcoded model outputs or claimed PASS before GPU run']
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
       'H01':['S01','S02'],'H02':['S02','S03']}
TOPICS={'S01':'electrical','S02':'mechanical','S03':'software','H01':'electrical-mechanical','H02':'mechanical-software'}
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
R['hybrid_results']=[];R['routing_results']=[]

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
 log('='*110);log('AKBASCORE PROMETHEUS — TEST727 — SPATIAL RAM GRAPH + S01/S02/S03 + H01/H02 PHYSICAL NEURAL CARTRIDGES');log('='*110)
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
 # Phase 3: dynamic numerical RAM graph routing and component-level remove-one-node diagnostics.
 # Retrieval still invokes exact sealed native SSD tensors, not synthesized text lookup.
 for hid,parents in [('H01',['S01','S02']),('H02',['S02','S03'])]:
  for question in HYBRID_QUESTIONS[hid]:
   all_nodes=list(entries);route_full=activated(question,banks,all_nodes,seed=hid)
   active=[n for n in route_full['selected'] if n in entries]
   selected_reads=[]
   for node in active:
    raw=physical_read(node,question)
    selected_reads.append({'id':node,'raw':raw})
   ablations={}
   for removed in parents:
    survivors=[n for n in active if n not in (hid,removed) and n not in EDGES.get(removed,[])]
    ablations[removed]={'surviving_nodes':survivors,'removed_nodes':[n for n in active if n not in survivors]}
    # Component-level removal diagnostic; NOT a controlled joint-KV causal ablation.
    ablations[removed]['readouts']=[{'id':n,'raw':physical_read(n,question)} for n in survivors if n in (hid,)+tuple(parents)]
   rec={'target':hid,'routing':route_full,'activated_readouts':selected_reads,'ablation':ablations}
   R['routing_results'].append(rec);save();log('SPATIAL_GRAPH_TRIAL',json.dumps(rec,ensure_ascii=False))
 # Phase 4: ensure all original + synthesized physical nodes persist; validate exact native/ref 80-layer parity.
 for cid in ['S01','S02','S03','H01','H02']:
  check('PHYSICAL_SURVIVES_'+cid,(CART_DIR/(cid+'.pt')).exists())
  cp=safe_load(entries[cid]);gpu_cp=to_gpu(cp)
  ref=initialize(gpu_cp);ref_seals=memory_seals(ref);del ref;release()
  direct=initialize_native(gpu_cp);direct_seals=memory_seals(direct)
  check('80_LAYER_PARITY_'+cid,compare_seals(ref_seals,direct_seals),
        {'matched':sum(a==b for a,b in zip(ref_seals,direct_seals)),'layers':NL})
  del direct,gpu_cp,cp;release()
 check('WEIGHTS_SENTINEL_UNCHANGED',sentinel()==before)
 R['summary']={'source_readout_hits':sum(x['expected_found'] for x in R['source_results']),
   'source_readout_n':len(R['source_results']),'domain_cartridges':len(R['domain_results']),
   'domain_semantic_hits':sum(x['readback_hits'] for x in R['domain_results']),
   'domain_semantic_n':sum(len(x['readback']) for x in R['domain_results']),
   'hybrid_cartridges':len(R['hybrid_results']),
   'hybrid_leaf_hits':sum(x['leaf_hits'] for x in R['hybrid_results']),
   'hybrid_leaf_n':sum(len(x['leaf_probes']) for x in R['hybrid_results']),
   'ram_graph_trials':len(R['routing_results']),
   'ssd_physical_nodes':len(entries),'ssd_sha_verified':True,'weights_unchanged':True}
 R['status']='COMPLETE_SPATIAL_DOMAIN_AND_CROSS_DOMAIN_MEASURED';save()
 log('TEST727_RESULT',R['status']);log('SUMMARY',R['summary']);log('RESULT_JSON',OUT,'MANIFEST',MANIFEST,'LOG',LOG)
except Exception as exc:
 R['status']='ERROR';R['error']=repr(exc);R['traceback']=traceback.format_exc();save();log('TEST727_ERROR',R['traceback']);raise
finally:save()
