# AKBASCORE TEST704 — THREE INTERNET BOOKS / HOT-SWAPPABLE CUT3 CARTRIDGES
# Copyright (c) 2026 Mustafa Akbas
# Licensed under AKBASCORE RESEARCH SOFTWARE LICENSE
# https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/LICENSE
# Earlier MIT-licensed material remains under its original license.
# Standalone Colab cell; GPU execution NOT performed by author.
import os,sys,subprocess,importlib.util,json,time,hashlib,random,re,gc,traceback,platform,urllib.request,urllib.error
from pathlib import Path
from datetime import datetime,timezone
for m,p in [('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50'),('psutil','psutil'),('pypdf','pypdf')]:
    if importlib.util.find_spec(m) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',p])
import torch,transformers,accelerate,bitsandbytes,psutil
from pypdf import PdfReader
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
from io import BytesIO
TEST='704';REV='704-R1';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
DTYPE=torch.bfloat16;DEVICE=torch.device('cuda:0');SEED=7042026
# Defaults are verifiable public-domain books, NOT 2024+ publications. Replace URLs with licensed 2025+ PDFs/TXT for the publication experiment.
BOOKS=[
 {'id':'A','title':'Pride and Prejudice','url':'https://www.gutenberg.org/ebooks/1342.txt.utf-8','format':'txt','license_note':'Project Gutenberg; inspect local reuse rules'},
 {'id':'B','title':'Frankenstein','url':'https://www.gutenberg.org/ebooks/84.txt.utf-8','format':'txt','license_note':'Project Gutenberg; inspect local reuse rules'},
 {'id':'C','title':'The Adventures of Sherlock Holmes','url':'https://www.gutenberg.org/ebooks/1661.txt.utf-8','format':'txt','license_note':'Project Gutenberg; inspect local reuse rules'},
]
# Conservative initial smoke test: 1024 body tokens per book; increasing to 10k+ requires further memory validation.
MAX_BOOK_TOKENS=int(os.getenv('AKBASCORE_BOOK_TOKENS','1024'))
MAX_DOWNLOAD_BYTES=24*1024*1024;MAX_PDF_PAGES=400;MAX_NEW=40
ROOT=Path('/content/AKBASCORE_TEST704');RAW=ROOT/'sources';CART=ROOT/'cartridges';RAW.mkdir(parents=True,exist_ok=True);CART.mkdir(parents=True,exist_ok=True)
LOG=ROOT/'TEST704.log';OUT=ROOT/'TEST704_results.json';LOG.write_text('',encoding='utf-8')
random.seed(SEED);torch.manual_seed(SEED);torch.set_grad_enabled(False);os.environ['TOKENIZERS_PARALLELISM']='false'
START=time.perf_counter();R={'test':TEST,'revision':REV,'status':'STARTED','model':MODEL_ID,'cut':CUT,'seed':SEED,'timestamp':datetime.now(timezone.utc).isoformat(),'book_limit_tokens':MAX_BOOK_TOKENS,'books':[],'checks':[],'experiments':[],'limitations':['Public-domain default works predate 2024; model may know them from pretraining.','Only initial MAX_BOOK_TOKENS of each book are forged; this is not full-book retention.','Cross-book open-ended answers are exploratory, not scored as proven reasoning.','A+B is append-composition in one live cache; it is not simultaneous independent retrieval routing.']}
def log(*args):
 s=' '.join(map(str,args));print(s,flush=True)
 with LOG.open('a',encoding='utf-8') as f:f.write(s+'\n')
def save():
 p=OUT.with_suffix('.tmp');p.write_text(json.dumps(R,indent=2,ensure_ascii=False,default=str),encoding='utf-8');p.replace(OUT)
def check(name,ok,details=None):
 ok=bool(ok);R['checks'].append({'name':name,'pass':ok,'details':details});log('PASS' if ok else 'FAIL',name,details or '')
 if not ok:raise RuntimeError('CHECK_FAILED_'+name)
def sha(b):return hashlib.sha256(b).hexdigest()
def mem():
 torch.cuda.synchronize();free,total=torch.cuda.mem_get_info()
 return {'gpu_free_gib':round(free/2**30,3),'gpu_allocated_gib':round(torch.cuda.memory_allocated()/2**30,3),'gpu_peak_gib':round(torch.cuda.max_memory_allocated()/2**30,3),'ram_available_gib':round(psutil.virtual_memory().available/2**30,3)}
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-research/1.0 (public reproducibility demo)'})
 with urllib.request.urlopen(req,timeout=90) as resp:
  length=resp.headers.get('Content-Length')
  if length and int(length)>MAX_DOWNLOAD_BYTES:raise ValueError('DOWNLOAD_TOO_LARGE')
  chunks=[];size=0
  while True:
   chunk=resp.read(1024*1024)
   if not chunk:break
   size+=len(chunk)
   if size>MAX_DOWNLOAD_BYTES:raise ValueError('DOWNLOAD_TOO_LARGE')
   chunks.append(chunk)
 return b''.join(chunks)
def clean_text(s):return re.sub(r'\n{4,}','\n\n\n',s.replace('\r\n','\n').replace('\r','\n')).strip()
def extract(b,fmt):
 if fmt=='pdf':
  reader=PdfReader(BytesIO(b));return clean_text('\n'.join((p.extract_text() or '') for p in reader.pages[:MAX_PDF_PAGES]))
 if fmt=='txt':return clean_text(b.decode('utf-8-sig',errors='replace'))
 raise ValueError('SUPPORTED_FORMATS_pdf_txt')
def pairs(c):
 if hasattr(c,'layers'):return tuple((l.keys,l.values) for l in c.layers)
 if hasattr(c,'key_cache'):return tuple(zip(c.key_cache,c.value_cache))
 if isinstance(c,(tuple,list)):return tuple((x[0],x[1]) for x in c)
 raise TypeError('UNSUPPORTED_CACHE_'+type(c).__name__)
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
 dummy=torch.zeros((1,len(pos),H),device=DEVICE,dtype=DTYPE)
 co,si=model.model.rotary_emb(dummy,pos.unsqueeze(0));return co.unsqueeze(1).float(),si.unsqueeze(1).float()
def rephase(k,old,new):
 if torch.equal(old,new):return k
 co,so=rope(old);cn,sn=rope(new);x=k.float();x=x*co-half(x)*so
 return (x*cn+half(x)*sn).to(k.dtype)
def weight_sentinel():
 h=hashlib.sha256()
 for w in [model.model.layers[i].self_attn.o_proj.weight for i in (0,19,39,59,79)]+[model.model.norm.weight,model.lm_head.weight]:
  a=w.detach().reshape(-1);n=a.numel()
  for j in range(16):
   o=j*max(n-256,0)//15;h.update(a[o:o+256].float().cpu().numpy().tobytes())
 return h.hexdigest()
@torch.no_grad()
def forge(ids):
 state={};n=len(ids)
 def capture(module,args,out):state['h']=(out[0] if isinstance(out,(tuple,list)) else out).detach().clone()
 hook=model.model.layers[CUT].register_forward_hook(capture)
 try:
  pos=torch.arange(n,device=DEVICE)
  out=model(input_ids=torch.tensor([ids],device=DEVICE),attention_mask=torch.ones((1,n),device=DEVICE,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
  kv=pairs(out.past_key_values)
  if len(kv)!=NL or state['h'].shape!=(1,n,H):raise RuntimeError('FORGE_GEOMETRY')
  # PERSIST ONLY H_CUT AND LOWER LAYERS, NOT THE FULL 80-LAYER CACHE.
  cp={'h':state['h'].cpu().contiguous(),'lower':tuple((k.cpu().contiguous(),v.cpu().contiguous()) for k,v in kv[:CUT+1]),'n':n,'p':P}
  del out,kv
  return cp
 finally:hook.remove()
def cartridge_bytes(cp):
 ts=[cp['h']]+[t for pair in cp['lower'] for t in pair]
 return sum(t.numel()*t.element_size() for t in ts)
def load_cartridge(book_id):
 path=CART/(book_id+'.pt');b=path.read_bytes();expect=next(x['cartridge_sha256'] for x in R['books'] if x['id']==book_id)
 if sha(b)!=expect:raise RuntimeError('CARTRIDGE_SHA_MISMATCH_'+book_id)
 # weights_only=True prevents arbitrary pickle execution in normal torch loading.
 cp=torch.load(BytesIO(b),map_location='cpu',weights_only=True)
 if len(cp['lower'])!=CUT+1 or cp['h'].shape!=(1,cp['n'],H) or cp['p']!=P:raise RuntimeError('INVALID_CARTRIDGE_'+book_id)
 return {'h':cp['h'].to(DEVICE),'lower':tuple((k.to(DEVICE),v.to(DEVICE)) for k,v in cp['lower']),'n':cp['n'],'p':cp['p']}
@torch.no_grad()
def initialize(cp):
 n=cp['n'];h=cp['h']
 def inject(module,args,out):
  cur=out[0] if isinstance(out,(tuple,list)) else out
  if cur.shape!=h.shape:raise RuntimeError('INIT_SHAPE')
  return replace(out,h)
 hook=model.model.layers[CUT].register_forward_hook(inject)
 try:
  pos=torch.arange(n,device=DEVICE)
  out=model(inputs_embeds=torch.zeros((1,n,H),device=DEVICE,dtype=DTYPE),attention_mask=torch.ones((1,n),device=DEVICE,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
  upper=pairs(out.past_key_values)
  result=cp['lower']+tuple((k.detach().clone(),v.detach().clone()) for k,v in upper[CUT+1:])
  if len(result)!=NL:raise RuntimeError('INIT_LAYER_COUNT')
  for i in range(CUT+1):
   if not torch.equal(result[i][0],cp['lower'][i][0]) or not torch.equal(result[i][1],cp['lower'][i][1]):raise RuntimeError('INIT_LOWER_NOT_EXACT')
  return result
 finally:hook.remove()
@torch.no_grad()
def append(memory,cp):
 oldn=int(memory[0][0].shape[-2]);q=cp['n']-P
 if q<=0:raise RuntimeError('EMPTY_BODY')
 pos=torch.arange(oldn,oldn+q,device=DEVICE);body=cp['h'][:,P:,:]
 def inject(module,args,out):
  cur=out[0] if isinstance(out,(tuple,list)) else out
  if cur.shape!=body.shape:raise RuntimeError('APPEND_SHAPE')
  return replace(out,body)
 hook=model.model.layers[CUT].register_forward_hook(inject)
 try:
  out=model(inputs_embeds=torch.zeros((1,q,H),device=DEVICE,dtype=DTYPE),past_key_values=cache_build(memory),attention_mask=torch.ones((1,oldn+q),device=DEVICE,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
  grown=list(pairs(out.past_key_values))
  for i in range(CUT+1):
   ok,ov=memory[i];k,v=cp['lower'][i]
   nk=rephase(k[:,:,P:,:],torch.arange(P,cp['n'],device=DEVICE),pos)
   grown[i]=(torch.cat((ok,nk),-2),torch.cat((ov,v[:,:,P:,:]),-2))
  result=tuple(grown)
  for i,((ok,ov),(nk,nv)) in enumerate(zip(memory,result)):
   if nk.shape[-2]!=oldn+q or nv.shape[-2]!=oldn+q:raise RuntimeError('LENGTH_LAYER_'+str(i))
   if not torch.equal(ok,nk[:,:,:oldn,:]) or not torch.equal(ov,nv[:,:,:oldn,:]):raise RuntimeError('BITWISE_APPEND_LAYER_'+str(i))
  return result
 finally:hook.remove()
@torch.no_grad()
def answer(memory,question,max_new=MAX_NEW):
 suffix='\nQUESTION:\n'+question+'\n\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n'
 ids=tok(suffix,add_special_tokens=False).input_ids
 if memory is None:
  n=0;cache=None
 else:
  n=int(memory[0][0].shape[-2]);cache=cache_build(memory)
 pos=torch.arange(n,n+len(ids),device=DEVICE)
 out=model(input_ids=torch.tensor([ids],device=DEVICE),past_key_values=cache,attention_mask=torch.ones((1,n+len(ids)),device=DEVICE,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
 cache=out.past_key_values;next_id=out.logits[:,-1,:].argmax(-1,keepdim=True);gen=[]
 stop={tok.eos_token_id,tok.convert_tokens_to_ids('<|im_end|>')}
 for _ in range(max_new):
  t=int(next_id.item())
  if t in stop:break
  gen.append(t);n=cache.get_seq_length();pos=torch.tensor([n],device=DEVICE)
  out=model(input_ids=next_id,past_key_values=cache,attention_mask=torch.ones((1,n+1),device=DEVICE,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
  cache=out.past_key_values;next_id=out.logits[:,-1,:].argmax(-1,keepdim=True)
 return tok.decode(gen,skip_special_tokens=True).strip()
def trial(label,book_ids,questions):
 t=time.perf_counter();memory=None
 for bid in book_ids:
  cp=load_cartridge(bid)
  memory=initialize(cp) if memory is None else append(memory,cp)
  del cp
 rows=[]
 for question in questions:
  raw=answer(memory,question)
  rows.append({'question':question,'raw':raw});log('QA',label,repr(question),'->',repr(raw))
 row={'label':label,'active_cartridges':book_ids,'queries':rows,'seconds':round(time.perf_counter()-t,2),'gpu':mem(),'cache_tokens':int(memory[0][0].shape[-2]) if memory is not None else 0}
 R['experiments'].append(row);save();del memory;gc.collect();torch.cuda.empty_cache()
 return row
try:
 log('='*110);log('AKBASCORE TEST704 — THREE INTERNET BOOKS / DISK CARTRIDGES / HOT SWAP');log('='*110)
 check('CUDA',torch.cuda.is_available());check('SINGLE_GPU',torch.cuda.device_count()==1);check('A100_80GB_CLASS',torch.cuda.get_device_properties(0).total_memory>=70*2**30)
 R['environment']={'gpu':torch.cuda.get_device_name(0),'torch':torch.__version__,'transformers':transformers.__version__,'accelerate':accelerate.__version__,'bitsandbytes':bitsandbytes.__version__,'python':platform.python_version()}
 check('BOOK_COUNT',len(BOOKS)==3 and len({x['id'] for x in BOOKS})==3)
 check('TOKEN_LIMIT',64<=MAX_BOOK_TOKENS<=16384,MAX_BOOK_TOKENS)
 # Fetch all source documents before loading the model; SHA and byte counts are independently recorded.
 source_texts={}
 for b in BOOKS:
  log('DOWNLOADING',b['id'],b['url']);data=fetch(b['url']);(RAW/(b['id']+'.'+b['format'])).write_bytes(data)
  extracted=extract(data,b['format'])
  if len(extracted)<1500:raise RuntimeError('SOURCE_TOO_SHORT_'+b['id'])
  source_texts[b['id']]=extracted
  item={**b,'source_bytes':len(data),'source_sha256':sha(data),'extracted_chars':len(extracted)};R['books'].append(item)
  log('SOURCE',b['id'],'BYTES',len(data),'SHA256',item['source_sha256'],'CHARS',len(extracted));save()
 tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
 quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
 log('LOADING_MODEL_NF4_GPU_ONLY');t=time.perf_counter()
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
 for p in model.parameters():p.requires_grad_(False)
 R['model_load_seconds']=round(time.perf_counter()-t,2);cfg=model.config
 NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
 check('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,[NL,H,QH,KVH,HD]);check('FROZEN',all(not p.requires_grad for p in model.parameters()))
 check('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
 devices={str(p.device) for p in model.parameters()}|{str(b.device) for b in model.buffers()};check('GPU_ONLY',devices=={'cuda:0'},sorted(devices))
 R['model_revision']=getattr(cfg,'_commit_hash',None);R['model_loaded_gpu']=mem();before=weight_sentinel();R['weight_sentinel_before']=before
 PREFIX='<|im_start|>system\nUse only the available document memory when answering questions about the documents. If evidence is missing, say UNKNOWN.\n<|im_end|>\n<|im_start|>user\nINFORMATION:\n'
 PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS);R['canonical_prefix_tokens']=P
 for b in R['books']:
  # No injected artificial facts or answers. Text is verbatim extracted source (up to token limit).
  source=source_texts[b['id']]
  body_ids=tok(source,add_special_tokens=False).input_ids[:MAX_BOOK_TOKENS]
  # Use body IDs as-is, no string concatenation retokenization ambiguity.
  ids=PIDS+body_ids;b['source_total_tokens']=len(tok(source,add_special_tokens=False).input_ids);b['forged_body_tokens']=len(body_ids)
  log('FORGING',b['id'],'BODY_TOKENS',len(body_ids),'FULL_SOURCE_TOKENS',b['source_total_tokens']);t=time.perf_counter()
  cp=forge(ids);cp['source_sha256']=b['source_sha256'];cp['book_id']=b['id'];cp['body_token_count']=len(body_ids)
  path=CART/(b['id']+'.pt');torch.save(cp,path);data=path.read_bytes()
  b['cartridge_file']=str(path);b['cartridge_sha256']=sha(data);b['cartridge_file_bytes']=len(data);b['cartridge_tensor_bytes']=cartridge_bytes(cp);b['forge_seconds']=round(time.perf_counter()-t,2)
  check('CARTRIDGE_ONLY_LOWER_'+b['id'],len(cp['lower'])==CUT+1 and 'kv' not in cp)
  log('SAVED_CARTRIDGE',b['id'],'BYTES',len(data),'SHA256',b['cartridge_sha256']);del cp;torch.cuda.empty_cache();save()
 # Source content is no longer used by any subsequent evaluation. Remove local source files too.
 source_texts.clear();del source_texts
 for p in RAW.iterdir():p.unlink()
 check('SOURCE_FILES_REMOVED',not any(RAW.iterdir()))
 gc.collect();torch.cuda.empty_cache();log('SOURCE_TEXT_REMOVED; STARTING SAME-MODEL HOT-SWAP TRIALS')
 # These are deliberately open-ended, NOT scored as validated semantic retrieval or reasoning.
 QA={
  'A':['Which characters are introduced in the available Pride and Prejudice excerpt?','What event is described in the available document excerpt?'],
  'B':['Which characters are introduced in the available Frankenstein excerpt?','What event is described in the available document excerpt?'],
  'C':['Which characters are introduced in the available Sherlock Holmes excerpt?','What event is described in the available document excerpt?'],
 }
 # A-only, B-only, A+B, B+A, C-only, A-only again: no model reload, new cache rebuilt from SSD each time.
 trial('NO_CARTRIDGE',[],['What does the loaded document excerpt say about its opening scene?'])
 trial('A_ONLY',['A'],QA['A']+['According to the available document, what is the opening scene of Frankenstein?'])
 trial('B_ONLY',['B'],QA['B']+['According to the available document, what is the opening scene of Pride and Prejudice?'])
 trial('A_PLUS_B',['A','B'],['Compare the opening situations in the available Pride and Prejudice and Frankenstein excerpts. Cite details from each excerpt.','Which excerpt discusses a family gathering, and which discusses scientific discovery? Answer only if supported by the available excerpts.'])
 trial('B_PLUS_A',['B','A'],['Compare the opening situations in the available Pride and Prejudice and Frankenstein excerpts. Cite details from each excerpt.'])
 trial('C_ONLY',['C'],QA['C']+['According to the available document, what is the opening scene of Frankenstein?'])
 trial('A_RESTORED',['A'],QA['A'])
 after=weight_sentinel();R['weight_sentinel_after']=after;check('WEIGHT_SENTINEL_UNCHANGED',before==after)
 R['status']='PASS_MECHANICS_UNSCORED_SEMANTICS'
except Exception as e:
 R['status']='ERROR';R['error_type']=type(e).__name__;R['error']=str(e);R['traceback']=traceback.format_exc()[-12000:];log('ERROR',type(e).__name__,str(e))
finally:
 R['elapsed_seconds']=round(time.perf_counter()-START,2)
 try:R['final_gpu']=mem()
 except Exception:pass
 save();log('='*110);log('TEST704_STATUS',R['status']);log('RESULT_JSON',OUT);log('RESULT_LOG',LOG);log('='*110)
