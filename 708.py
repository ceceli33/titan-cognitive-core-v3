# AKBASCORE TEST708 — THREE BOOKS / THREE PHYSICAL CUT3 CARTRIDGES / GPU CAPACITY DEMO
# Copyright (c) 2026 Mustafa Akbas
# AKBASCORE RESEARCH SOFTWARE LICENSE: https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/LICENSE
# TEST708: TEST707 engine, append memory-ownership diagnostic and GPU peak reduction.
# No mathematical CUT3 / RoPE / model / tensor dtype change. UNTESTED ON GPU.
# Original: https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/706.py
# Hardware-boundary log: https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/706.log
# Standalone Google Colab A100 80GB. UNTESTED ON GPU. Never reports semantic PASS without ground truth.
# IMPORTANT: 10k-token excerpts per book; NOT the full books or physical printed pages.
import os,sys,subprocess,importlib.util,json,time,hashlib,random,re,gc,traceback,platform,urllib.request,math
from pathlib import Path
from datetime import datetime,timezone
from io import BytesIO
for mod,pkg in [('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50'),('psutil','psutil')]:
 if importlib.util.find_spec(mod) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',pkg])
import torch,transformers,accelerate,bitsandbytes,psutil
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
TEST='708';REV='708-R1';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;DTYPE=torch.bfloat16;DEV=torch.device('cuda:0');EXPECTED=(80,8192,64,8,128)
PAGE_TOKENS=int(os.getenv('AKBASCORE_PAGE_EQUIVALENT_TOKENS','250'))
TOKENS_PER_BOOK=int(os.getenv('AKBASCORE_TOKENS_PER_BOOK','10000'))
CHUNK=int(os.getenv('AKBASCORE_CHUNK_TOKENS','256'))
GPU_RESERVE_GIB=float(os.getenv('AKBASCORE_GPU_RESERVE_GIB','9'))
# Fixed and equal three-book excerpts; no adaptive truncation.
MAX_NEW=int(os.getenv('AKBASCORE_MAX_NEW','48'))
# Texts are public-domain classics, NOT post-2024 or proof of zero pretraining leakage.
BOOKS=[('A','Pride and Prejudice','https://www.gutenberg.org/ebooks/1342.txt.utf-8'),('B','Frankenstein','https://www.gutenberg.org/ebooks/84.txt.utf-8'),('C','The Adventures of Sherlock Holmes','https://www.gutenberg.org/ebooks/1661.txt.utf-8')]
ROOT=Path('/content/AKBASCORE_TEST708');RAW=ROOT/'sources';CART=ROOT/'cartridges';RAW.mkdir(parents=True,exist_ok=True);CART.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'TEST708_results.json';LOG=ROOT/'TEST708.log';LOG.write_text('');START=time.perf_counter();R={'test':TEST,'revision':REV,'status':'STARTED','model':MODEL_ID,'cut':CUT,'page_definition':f'{PAGE_TOKENS} tokenizer tokens = 1 page-equivalent (not a printed page)','books':[],'checks':[],'trials':[],'limits':['Append optimization releases caller-owned upper-KV references; exact SHA-256 guards check all prior KV bytes','Public domain classics: pretraining leakage cannot be excluded','Each book cartridge is an excerpt, not the complete book','Page equivalents are not actual printed page counts','CUT3 persisted cartridge excludes upper layers, but reconstruction requires full live KV','Hot-swap includes SSD read, H2D, upper-cache reconstruction: never assume milliseconds','No demonstrated full-book comprehension or guaranteed cross-book reasoning','Classic-book QA may be answered from model pretraining; semantics are not causally established']}
def log(*a):
 s=' '.join(map(str,a));print(s,flush=True)
 with LOG.open('a') as f:f.write(s+'\n')
def save():
 t=OUT.with_suffix('.tmp');t.write_text(json.dumps(R,indent=2,ensure_ascii=False,default=str));t.replace(OUT)
def ck(name,ok,detail=None):
 R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});log('PASS' if ok else 'FAIL',name,detail or '');save()
 if not ok:raise RuntimeError('CHECK_FAILED_'+name)
def sha(b):return hashlib.sha256(b).hexdigest()
def mem():
 torch.cuda.synchronize();free,total=torch.cuda.mem_get_info()
 return {'free_gib':round(free/2**30,3),'allocated_gib':round(torch.cuda.memory_allocated()/2**30,3),'peak_gib':round(torch.cuda.max_memory_allocated()/2**30,3),'total_gib':round(total/2**30,3)}
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST708-reproducible-research'})
 with urllib.request.urlopen(req,timeout=90) as f:
  data=f.read(12*1024*1024+1)
 if len(data)>12*1024*1024:raise RuntimeError('SOURCE_TOO_LARGE')
 return data

def pairs(c):
 if hasattr(c,'layers'):return tuple((l.keys,l.values) for l in c.layers)
 if hasattr(c,'key_cache'):return tuple(zip(c.key_cache,c.value_cache))
 if isinstance(c,(tuple,list)):return tuple((x[0],x[1]) for x in c)
 raise TypeError('UNKNOWN_CACHE_'+type(c).__name__)
def cache_build(kvs):
 c=DynamicCache()
 for i,(k,v) in enumerate(kvs):c.update(k,v,i)
 return c
def replace(out,h):
 if isinstance(out,tuple):return (h,)+out[1:]
 if isinstance(out,list):return [h]+out[1:]
 return h
def half(x):
 a,b=x.chunk(2,-1);return torch.cat((-b,a),-1)
def rope(pos):
 z=torch.zeros((1,len(pos),H),device=DEV,dtype=DTYPE);co,si=model.model.rotary_emb(z,pos.unsqueeze(0));return co.unsqueeze(1).float(),si.unsqueeze(1).float()
def rephase(k,old,new):
 if torch.equal(old,new):return k
 co,so=rope(old);cn,sn=rope(new);x=k.float();x=x*co-half(x)*so
 return (x*cn+half(x)*sn).to(k.dtype)
def sentinel():
 h=hashlib.sha256()
 for w in [model.model.layers[i].self_attn.o_proj.weight for i in (0,19,39,59,79)]+[model.model.norm.weight,model.lm_head.weight]:
  a=w.detach().reshape(-1);n=a.numel()
  for j in range(16):
   o=j*max(n-256,0)//15;h.update(a[o:o+256].float().cpu().numpy().tobytes())
 return h.hexdigest()

def free_gpu():gc.collect();torch.cuda.empty_cache()
def ensure_room(extra_tokens=0):
 # Full live 80-layer KV grows ~320 KiB/token; reserve must remain before every step.
 f,_=torch.cuda.mem_get_info();need=GPU_RESERVE_GIB*2**30+extra_tokens*NL*KVH*HD*2*2
 if f<need:raise RuntimeError(f'GPU_SAFETY_STOP free={f/2**30:.2f}GiB need={need/2**30:.2f}GiB')

@torch.no_grad()
def forge_stream(body_ids,book_id):
 # Real streaming prefill of one contiguous context. Retains live full KV during forging;
 # persists ONLY H_CUT and L0..CUT KV to CPU. No truncation of requested body.
 ids=PIDS+body_ids;n=len(ids);cache=None;h_chunks=[];t=time.perf_counter()
 def capture(mod,args,out):h_chunks.append((out[0] if isinstance(out,(tuple,list)) else out).detach().to('cpu',copy=True).contiguous())
 hook=model.model.layers[CUT].register_forward_hook(capture)
 try:
  for st in range(0,n,CHUNK):
   piece=ids[st:st+CHUNK];ensure_room(len(piece)+512)
   pos=torch.arange(st,st+len(piece),device=DEV)
   out=model(input_ids=torch.tensor([piece],device=DEV),past_key_values=cache,
    attention_mask=torch.ones((1,st+len(piece)),device=DEV,dtype=torch.long),
    position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
   cache=out.past_key_values;del out
   if st==0 or (st//CHUNK+1)%32==0:log('FORGE_PROGRESS',book_id,st+len(piece),'/',n,'GPU',mem());save()
  kv=pairs(cache)
  cp={'h':torch.cat(h_chunks,dim=1),'lower':tuple((k.detach().cpu().contiguous(),v.detach().cpu().contiguous()) for k,v in kv[:CUT+1]),'n':n,'p':P,'body_tokens':len(body_ids),'book_id':book_id}
  if cp['h'].shape!=(1,n,H) or len(cp['lower'])!=CUT+1:raise RuntimeError('FORGE_SHAPE')
  return cp,round(time.perf_counter()-t,3)
 finally:
  hook.remove();del cache;free_gpu()

def cart_load(bid):
 b=next(x for x in R['books'] if x['id']==bid);p=CART/(bid+'.pt');t=time.perf_counter();raw=p.read_bytes()
 if sha(raw)!=b['cartridge_sha256']:raise RuntimeError('SHA_MISMATCH_'+bid)
 cp=torch.load(BytesIO(raw),map_location='cpu',weights_only=True)
 if cp['book_id']!=bid or len(cp['lower'])!=CUT+1 or cp['h'].shape!=(1,cp['n'],H):raise RuntimeError('CARTRIDGE_INVALID_'+bid)
 disk_s=time.perf_counter()-t;t=time.perf_counter()
 cp['h']=cp['h'].to(DEV);cp['lower']=tuple((k.to(DEV),v.to(DEV)) for k,v in cp['lower'])
 torch.cuda.synchronize();return cp,{'ssd_load_ms':round(disk_s*1000,3),'h2d_ms':round((time.perf_counter()-t)*1000,3)}

@torch.no_grad()
def initialize(cp):
 n=cp['n'];h=cp['h'];ensure_room(n+512)
 def inject(mod,args,out):
  z=out[0] if isinstance(out,(tuple,list)) else out
  if z.shape!=h.shape:raise RuntimeError('INIT_H_SHAPE')
  return replace(out,h)
 # Chunked upper-cache rebuild; injection at CUT layer is sliced per chunk.
 # Single-pass n-token forward is too memory-heavy for long books.
 upper=None;hook=None;offset=[0]
 def inject_chunk(mod,args,out):
  z=out[0] if isinstance(out,(tuple,list)) else out
  st=offset[0];target=h[:,st:st+z.shape[1],:]
  if z.shape!=target.shape:raise RuntimeError('INIT_CHUNK_SHAPE')
  return replace(out,target)
 hook=model.model.layers[CUT].register_forward_hook(inject_chunk)
 try:
  for st in range(0,n,CHUNK):
   q=min(CHUNK,n-st);ensure_room(q+512);offset[0]=st
   pos=torch.arange(st,st+q,device=DEV)
   out=model(inputs_embeds=torch.zeros((1,q,H),device=DEV,dtype=DTYPE),past_key_values=upper,
    attention_mask=torch.ones((1,st+q),device=DEV,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
   upper=out.past_key_values;del out
  kv=pairs(upper)
  result=cp['lower']+tuple((k.detach().clone(),v.detach().clone()) for k,v in kv[CUT+1:])
  if len(result)!=NL:raise RuntimeError('INIT_LAYERS')
  return result
 finally:
  hook.remove();del upper

def kv_digest(t,block=1048576):
 # Exact SHA-256 of every BF16 tensor byte; chunked CPU transfer, no full-size CPU duplicate.
 h=hashlib.sha256();v=t.detach().contiguous().view(-1)
 for st in range(0,v.numel(),block):h.update(v[st:st+block].cpu().numpy().tobytes())
 return h.hexdigest()

def full_kv_seal(kvs):
 return tuple((kv_digest(k),kv_digest(v)) for k,v in kvs)

@torch.no_grad()
def append(memory,cp):
 # Ownership repair: memory MUST be a mutable list and MUST be exclusively owned by trial().
 # Previous TEST707 kept all old upper-layer tensors alive while DynamicCache concatenated
 # the growing KV, doubling peak live memory. Transfer ownership to DynamicCache, then
 # drop old upper-layer references before any forward. Retain only four lower-layer pairs.
 if not isinstance(memory,list) or len(memory)!=NL or any(x is None for x in memory):raise RuntimeError('APPEND_REQUIRES_OWNED_LIST')
 oldn=memory[0][0].shape[-2];q=cp['n']-P;body=cp['h'][:,P:,:]
 log('APPEND_DIAG_BEFORE_SEAL',{'old_tokens':oldn,'new_tokens':q,'gpu':mem()})
 seals=full_kv_seal(memory)
 log('APPEND_PRIOR_SHA256_SEALED',{'layers':len(seals),'gpu':mem()})
 old_lower=tuple(memory[:CUT+1]);upper=cache_build(memory)
 for i in range(NL):memory[i]=None
 free_gpu();log('APPEND_DIAG_AFTER_RELEASE',mem());offset=[0]
 def inject(mod,args,out):
  z=out[0] if isinstance(out,(tuple,list)) else out
  st=offset[0];target=body[:,st:st+z.shape[1],:]
  if z.shape!=target.shape:raise RuntimeError('APPEND_H_SHAPE')
  return replace(out,target)
 hook=model.model.layers[CUT].register_forward_hook(inject)
 try:
  for st in range(0,q,CHUNK):
   m=min(CHUNK,q-st);ensure_room(m+512);offset[0]=st
   pos=torch.arange(oldn+st,oldn+st+m,device=DEV)
   out=model(inputs_embeds=torch.zeros((1,m,H),device=DEV,dtype=DTYPE),past_key_values=upper,
    attention_mask=torch.ones((1,oldn+st+m),device=DEV,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
   upper=out.past_key_values;del out
   if st==0 or (st//CHUNK+1)%8==0:log('APPEND_PROGRESS',st+m,'/',q,'GPU',mem())
  grown=list(pairs(upper))
  for i in range(CUT+1):
   ok,ov=old_lower[i];k,v=cp['lower'][i];nk=[]
   for st in range(0,q,CHUNK):
    end=min(q,st+CHUNK);old=torch.arange(P+st,P+end,device=DEV);new=torch.arange(oldn+st,oldn+end,device=DEV)
    nk.append(rephase(k[:,:,P+st:P+end,:],old,new))
   grown[i]=(torch.cat([ok]+nk,dim=-2),torch.cat((ov,v[:,:,P:,:]),dim=-2))
  result=grown
  # Verify EVERY original K/V byte for all 80 layers, not sampled rows.
  for i,((nk,nv),(kh,vh)) in enumerate(zip(result,seals)):
   if kv_digest(nk[:,:,:oldn,:])!=kh or kv_digest(nv[:,:,:oldn,:])!=vh:raise RuntimeError('APPEND_PRIOR_SHA256_CHANGED_LAYER_'+str(i))
  log('PASS APPEND_ALL_80_LAYERS_EXACT_SHA256',{'old_tokens':oldn,'new_tokens':oldn+q})
  return result
 finally:
  hook.remove();del upper

@torch.no_grad()
def answer(memory,question):
 suffix='\nQUESTION:\n'+question+'\n\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n'
 ids=tok(suffix,add_special_tokens=False).input_ids;n=0 if memory is None else memory[0][0].shape[-2]
 cache=None if memory is None else cache_build(memory)
 pos=torch.arange(n,n+len(ids),device=DEV)
 out=model(input_ids=torch.tensor([ids],device=DEV),past_key_values=cache,
  attention_mask=torch.ones((1,n+len(ids)),device=DEV,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
 cache=out.past_key_values;next_id=out.logits[:,-1,:].argmax(-1,keepdim=True);gen=[]
 stop={tok.eos_token_id,tok.convert_tokens_to_ids('<|im_end|>')}
 for _ in range(MAX_NEW):
  v=int(next_id.item())
  if v in stop:break
  gen.append(v);n=cache.get_seq_length();pos=torch.tensor([n],device=DEV)
  out=model(input_ids=next_id,past_key_values=cache,attention_mask=torch.ones((1,n+1),device=DEV,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
  cache=out.past_key_values;next_id=out.logits[:,-1,:].argmax(-1,keepdim=True)
 return tok.decode(gen,skip_special_tokens=True).strip()

def trial(label,bids,questions):
 t=time.perf_counter();memory=None;stages=[]
 try:
  for bid in bids:
   cp,times=cart_load(bid);t0=time.perf_counter()
   new=list(initialize(cp)) if memory is None else append(memory,cp)
   del memory;memory=new;del new,cp;free_gpu();torch.cuda.synchronize()
   times['rebuild_ms']=round((time.perf_counter()-t0)*1000,3);times['end_to_end_ms']=round(times['ssd_load_ms']+times['h2d_ms']+times['rebuild_ms'],3)
   times['book']=bid;times['cache_tokens']=memory[0][0].shape[-2];times['gpu']=mem();stages.append(times);log('HOT_SWAP_TIMING',label,bid,times);save()
  rows=[]
  for q in questions:
   ensure_room(512);raw=answer(memory,q);log('QA',label,repr(q),'->',repr(raw));rows.append({'question':q,'raw':raw})
  result={'label':label,'active':bids,'stages':stages,'qa':rows,'cache_tokens':0 if memory is None else memory[0][0].shape[-2],'seconds':round(time.perf_counter()-t,3),'gpu':mem(),'semantics':'UNSCORED'}
  R['trials'].append(result);save();return result
 finally:
  del memory;free_gpu()

try:
 log('='*105);log('AKBASCORE TEST708 — THREE BOOKS / 3 x 10000 TOKEN PHYSICAL CUT3 / TIMED HOT SWAP');log('='*105)
 ck('CUDA',torch.cuda.is_available());ck('SINGLE_GPU',torch.cuda.device_count()==1);ck('A100_80GB',torch.cuda.get_device_properties(0).total_memory>=70*2**30)
 ck('CONFIG',PAGE_TOKENS>=100 and 32<=CHUNK<=1024 and GPU_RESERVE_GIB>=4 and TOKENS_PER_BOOK>=1024)
 R['env']={'gpu':torch.cuda.get_device_name(0),'torch':torch.__version__,'transformers':transformers.__version__,'bitsandbytes':bitsandbytes.__version__,'python':platform.python_version(),'chunk_tokens':CHUNK,'reserve_gib':GPU_RESERVE_GIB}
 source={}
 for bid,title,url in BOOKS:
  data=fetch(url);(RAW/(bid+'.txt')).write_bytes(data);source[bid]=data.decode('utf-8-sig',errors='replace')
  R['books'].append({'id':bid,'title':title,'url':url,'source_sha256':sha(data),'source_bytes':len(data)})
  log('SOURCE',bid,'BYTES',len(data),'SHA256',sha(data));save()
 tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
 # tokenize with truncation=False intentionally; warn about token limit only for full source, not model inputs.
 bodies={bid:tok(text,add_special_tokens=False,verbose=False).input_ids for bid,text in source.items()}
 for b in R['books']:b['total_source_tokens']=len(bodies[b['id']])
 ck('THREE_BOOKS_HAVE_REQUIRED_TOKENS',all(len(bodies[x])>=TOKENS_PER_BOOK for x in ('A','B','C')),{x:len(bodies[x]) for x in ('A','B','C')})
 quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
 log('LOADING_72B_NF4_GPU_ONLY');t=time.perf_counter()
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
 for p in model.parameters():p.requires_grad_(False)
 R['model_load_s']=round(time.perf_counter()-t,2);cfg=model.config
 NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
 ck('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,[NL,H,QH,KVH,HD]);ck('FROZEN',all(not p.requires_grad for p in model.parameters()))
 ck('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
 ck('GPU_ONLY',({str(p.device) for p in model.parameters()}|{str(x.device) for x in model.buffers()})=={'cuda:0'})
 R['model_revision']=getattr(cfg,'_commit_hash',None);before=sentinel();R['weight_sentinel_before']=before
 PREFIX='<|im_start|>system\nUse only the available document memory for document-specific questions. If the evidence is missing, say UNKNOWN.\n<|im_end|>\n<|im_start|>user\nINFORMATION:\n'
 PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
 target={x:TOKENS_PER_BOOK for x in ('A','B','C')}
 kv_bytes=NL*KVH*HD*2*2;free,_=torch.cuda.mem_get_info()
 # Theoretical KV-only estimate, NOT a measured peak or a guarantee of fit.
 max_live=int((free-GPU_RESERVE_GIB*2**30)//kv_bytes)
 R['budget']={'tokens_per_book':TOKENS_PER_BOOK,'total_body_tokens':3*TOKENS_PER_BOOK,'max_live_cache_tokens_estimate':max_live,'full_kv_bytes_per_token':kv_bytes,'reserve_gib':GPU_RESERVE_GIB,'model_gpu':mem()}
 log('CAPACITY_BUDGET',R['budget']);save()
 ck('KV_ONLY_ESTIMATE_FITS',max_live>=3*(TOKENS_PER_BOOK+P)+MAX_NEW+256,R['budget'])
 for b in R['books']:
  bid=b['id'];count=target[bid];b['requested_tokens']=count;b['page_equivalents']=count/PAGE_TOKENS
  log('FORGING',bid,'TOKENS',count,'PAGE_EQUIVALENTS',count/PAGE_TOKENS)
  cp,secs=forge_stream(bodies[bid][:count],bid)
  cp['source_sha256']=b['source_sha256'];path=CART/(bid+'.pt');torch.save(cp,path)
  b['cartridge_file_bytes']=path.stat().st_size;b['cartridge_sha256']=sha(path.read_bytes());b['forge_seconds']=secs
  b['tensor_bytes']=cp['h'].numel()*cp['h'].element_size()+sum(k.numel()*k.element_size()+v.numel()*v.element_size() for k,v in cp['lower'])
  ck('CARTRIDGE_LOWER_ONLY_'+bid,len(cp['lower'])==CUT+1 and 'upper' not in cp)
  log('SAVED',bid,'FILE_BYTES',b['cartridge_file_bytes'],'SHA256',b['cartridge_sha256']);del cp;free_gpu();save()
 del source,bodies
 for p in RAW.iterdir():p.unlink()
 ck('SOURCE_FILES_REMOVED',not any(RAW.iterdir()))
 # Freshly reconstruct A and verify that full context can be read; this may be slower than milliseconds.
 trial('NO_CARTRIDGE',[],['What document is currently loaded? Answer UNKNOWN if no document is available.'])
 trial('A_ONLY',['A'],['Who is Elizabeth Bennet?', 'What is the relationship between Elizabeth Bennet and Jane Bennet?'])
 trial('B_ONLY',['B'],['Who is Robert Walton?', 'What expedition is Robert Walton undertaking?'])
 trial('C_ONLY',['C'],['Who is Dr. Watson?', 'What is the name of the detective associated with Dr. Watson?'])
 trial('A_PLUS_B',['A','B'],['Identify one person from Pride and Prejudice and one person from Frankenstein.'])
 trial('B_PLUS_A',['B','A'],['Name the narrator of the opening letters in Frankenstein and a Bennet sister from Pride and Prejudice.'])
 trial('A_PLUS_C',['A','C'],['Name a Bennet sister and the detective in the other document.'])
 trial('B_PLUS_C',['B','C'],['Name the Arctic explorer from Frankenstein and the detective from the other document.'])
 trial('A_PLUS_B_PLUS_C',['A','B','C'],['Identify Elizabeth Bennet, Robert Walton and Sherlock Holmes and associate each with its own document.'])
 trial('C_PLUS_B_PLUS_A',['C','B','A'],['Name a character from each of the three different documents and say which document contains each.'])
 trial('A_RESTORED',['A'],['Who is Elizabeth Bennet?'])
 ck('THREE_CARTRIDGES_ON_DISK',all((CART/(x+'.pt')).is_file() for x in ('A','B','C')))
 ck('THREE_WAY_RECONSTRUCTION',any(x['label']=='A_PLUS_B_PLUS_C' and x['cache_tokens']>=3*TOKENS_PER_BOOK for x in R['trials']) and any(x['label']=='C_PLUS_B_PLUS_A' and x['cache_tokens']>=3*TOKENS_PER_BOOK for x in R['trials']))
 after=sentinel();R['weight_sentinel_after']=after;ck('WEIGHT_SENTINEL_UNCHANGED',before==after)
 R['status']='PASS_PHYSICAL_UNSCORED_SEMANTICS'
except Exception as e:
 R['status']='ERROR';R['error_type']=type(e).__name__;R['error']=str(e);R['traceback']=traceback.format_exc()[-15000:];log('ERROR',type(e).__name__,str(e));log(R['traceback'])
finally:
 R['elapsed_s']=round(time.perf_counter()-START,2)
 try:R['gpu_final']=mem()
 except Exception:pass
 save();log('='*105);log('TEST708_STATUS',R['status']);log('RESULT_JSON',OUT);log('RESULT_LOG',LOG);log('='*105)
