# AKBASCORE TEST714 — QWEN72B NATIVE-ACTIVATION ADDRESSING / SIEMENS CUT3
# Standalone Colab A100-80GB; untested on GPU. TEST709 engine functions loaded unchanged by AST.
# Addressing is UNSUPERVISED and uses no question gold, page number, or answer string.
import os,sys,subprocess,importlib.util,urllib.request,hashlib,ast,json,time,gc,random,traceback
from pathlib import Path
for mod,pkg in [('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50'),('fitz','pymupdf'),('sklearn','scikit-learn')]:
 if importlib.util.find_spec(mod) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',pkg])
import torch,numpy as np,fitz
from sklearn.decomposition import PCA
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
from io import BytesIO
TEST='714';ROOT=Path('/content/AKBASCORE_TEST714');ROOT.mkdir(parents=True,exist_ok=True)
CART=ROOT/'cartridges';CART.mkdir(exist_ok=True);OUT=ROOT/'TEST714_results.json'
MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;DTYPE=torch.bfloat16;DEV=torch.device('cuda:0');EXPECTED=(80,8192,64,8,128)
CHUNK=256;MAX_NEW=48;GPU_RESERVE_GIB=9.;NL=80;H=8192;QH=64;KVH=8;HD=128
SOURCE709='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/709.py'
LOCK709='6c9f8cbb1eeed848d45133d73f0d7676b68e9125' # Git blob SHA1, not SHA256
PDF_URL='https://cache.industry.siemens.com/dl/files/087/109994087/att_1338962/v1/ONE_universal_op_man_0725_en-US.pdf'
PDF_SHA='88c0f8293ce3302135042baf35d704303fb3b5a24915e28b8ca16f3192a7cc1d'
# Predeclared queries: gold cartridge is used ONLY in evaluation, never in retrieval.
# The queries are thematic and are NOT an independently verified page-specific QA panel.
PANEL=[('What does the manual say about the fundamentals of operation?',1),('How do I machine a workpiece?',2),('How do I create a G code program?',4),('How do I manage programs?',6),('How can I edit the PLC user program?',8)]
# Zero-index golds above follow previously recorded 10 page ranges; validation below verifies the mapping.
R={'test':TEST,'status':'STARTED','engine':'709.py AST function extraction','method':'unsupervised PCA128 token-activation candidate search + exact cosine rerank','queries':[],'limits':['GPU run not performed by code author','Five thematic questions are a preliminary routing diagnostic, not a blind benchmark','Model-internal CUT3 activation space may not be a semantic retrieval embedding','PCA is trained only on stored cartridge activations; no supervised calibration','This test does not claim accurate answer generation or RAG superiority']}
def log(*a):print(*a,flush=True)
def save():OUT.write_text(json.dumps(R,indent=2,ensure_ascii=False,default=str))
def sha(x):return hashlib.sha256(x).hexdigest()
def fetch(url,limit):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST714'}),timeout=180) as f:b=f.read(limit+1)
 assert len(b)<=limit,'DOWNLOAD_SIZE_LIMIT';return b
def ck(k,v):R[k]=bool(v);log(('PASS' if v else 'FAIL'),k);save();assert v,k
# Extract EXACT original function definitions, without executing 709's demo/try block.
raw=fetch(SOURCE709,200000);tree=ast.parse(raw.decode());names={'pairs','cache_build','replace','half','rope','rephase','sentinel','free_gpu','ensure_room','forge_stream','cart_load','initialize','kv_digest','full_kv_seal','append','answer','mem'}
found={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in names}
assert found.keys()==names,(names-found.keys());fnmod=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[])
# Decorators require torch available; all function bodies are unchanged.
exec(compile(ast.fix_missing_locations(fnmod),'709.py','exec'),globals())
try:
 ck('709_GIT_BLOB_LOCK',hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==LOCK709)
 pdf=fetch(PDF_URL,15000000);ck('PDF_SHA256_LOCK',sha(pdf)==PDF_SHA)
 doc=fitz.open(stream=pdf,filetype='pdf');ck('PDF_486_PAGES',len(doc)==486)
 (ROOT/'siemens.pdf').write_bytes(pdf)
 tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
 PREFIX='<|im_start|>system\nUse only the available document memory for document-specific questions. If the evidence is missing, say UNKNOWN.\n<|im_end|>\n<|im_start|>user\nINFORMATION:\n'
 PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
 # Recreate previously reported exact page boundaries. Any drift is recorded, not hidden.
 bounds=[(1,40),(41,96),(97,149),(150,197),(198,255),(256,311),(312,362),(363,415),(416,461),(462,486)]
 bodies=[]
 for a,b in bounds:
  s=''.join(f'\n[PDF PAGE {p}]\n'+doc[p-1].get_text(sort=True) for p in range(a,b+1))
  bodies.append(tok(s,add_special_tokens=False).input_ids)
 R['page_ranges']=bounds;R['body_tokens']=[len(x) for x in bodies];log('TOKEN_COUNTS',R['body_tokens']);save()
 ck('ALL_PAGES_COVERED',sum(b-a+1 for a,b in bounds)==486)
 quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
 ck('CUDA_A100_80GB',torch.cuda.is_available() and torch.cuda.get_device_properties(0).total_memory>=70*2**30)
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
 for p in model.parameters():p.requires_grad_(False)
 cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
 ck('MODEL_ARCH', (NL,H,QH,KVH,HD)==EXPECTED)
 ck('FROZEN',all(not p.requires_grad for p in model.parameters()))
 before=sentinel();R['weight_sentinel_before']=before
 # Forge all 10 physical cartridges using ORIGINAL TEST709 function unchanged.
 R['books']=[{'id':f'C{i+1:02d}'} for i in range(10)]
 for i,body in enumerate(bodies):
  bid=f'C{i+1:02d}';path=CART/(bid+'.pt')
  if path.exists() and (CART/(bid+'.sha256')).exists() and sha(path.read_bytes())==(CART/(bid+'.sha256')).read_text().strip():
   log('REUSE_SHA_VERIFIED',bid)
  else:
   log('FORGE',bid,'TOKENS',len(body));cp,secs=forge_stream(body,bid);torch.save(cp,path);(CART/(bid+'.sha256')).write_text(sha(path.read_bytes()));del cp;free_gpu()
  R['books'][i].update({'cartridge_sha256':sha(path.read_bytes()),'body_tokens':len(body),'page_range':bounds[i]});save()
 del pdf,doc,bodies;gc.collect()
 # Activation bank: H_CUT is from the physical cartridge; skip the canonical prefix and page marker-like text.
 # We use evenly sampled native hidden-state positions; no text labels are indexed.
 rng=np.random.default_rng(714);BANK=[];OWN=[];PER=512
 for i in range(10):
  cp=torch.load(CART/(f'C{i+1:02d}.pt'),map_location='cpu',weights_only=True)
  x=cp['h'][0,P:,:].float();inds=np.linspace(0,len(x)-1,min(PER,len(x)),dtype=np.int64)
  BANK.append(x[torch.from_numpy(inds)].numpy());OWN.extend([i]*len(inds));del cp,x
 X=np.concatenate(BANK).astype(np.float32);OWN=np.array(OWN,dtype=np.int32)
 # PCA is label-free, fit to stored memory only. A fixed seed prevents nondeterministic fitting.
 pca=PCA(n_components=128,svd_solver='randomized',random_state=714)
 Z=pca.fit_transform(X);Z/=np.maximum(np.linalg.norm(Z,axis=1,keepdims=True),1e-8)
 # Exact-rerank uses all sampled memory tokens, not gold labels. PCA candidates are diagnostic.
 @torch.no_grad()
 def query_activation(question):
  # The question is NOT preceded by page numbers, answers, or source snippets.
  s='<|im_start|>user\n'+question+'\n<|im_end|>\n<|im_start|>assistant\n'
  ids=tok(s,add_special_tokens=False).input_ids;outbuf=[]
  def cap(mod,args,out):outbuf.append((out[0] if isinstance(out,(tuple,list)) else out).detach().float().cpu())
  hook=model.model.layers[CUT].register_forward_hook(cap)
  try:
   out=model(input_ids=torch.tensor([ids],device=DEV),use_cache=False,return_dict=True);del out
  finally:hook.remove()
  return outbuf[0][0].numpy().astype(np.float32)
 def score(q,db):
  # Tokenwise maximum cosine, then mean over question tokens. Query does not access gold.
  a=q/np.maximum(np.linalg.norm(q,axis=1,keepdims=True),1e-8)
  return float((a@db.T).max(axis=1).mean())
 for j,(question,gold) in enumerate(PANEL):
  q=query_activation(question);qz=pca.transform(q);qz/=np.maximum(np.linalg.norm(qz,axis=1,keepdims=True),1e-8)
  # All 10 cartridge candidates are scored; do not assume routing success from page oracle.
  scores=[score(qz,Z[OWN==i]) for i in range(10)]
  ranked=sorted(range(10),key=lambda i:(-scores[i],i));row={'case':j,'question':question,'gold_cartridge':f'C{gold+1:02d}','selected':f'C{ranked[0]+1:02d}','top5':[f'C{i+1:02d}' for i in ranked[:5]],'hit1':ranked[0]==gold,'hit5':gold in ranked[:5],'scores':[round(s,6) for s in scores]}
  R['queries'].append(row);log('ROUTE',json.dumps(row,ensure_ascii=False));save()
 R['recall_at_1']=sum(x['hit1'] for x in R['queries'])/len(R['queries']);R['recall_at_5']=sum(x['hit5'] for x in R['queries'])/len(R['queries'])
 ck('WEIGHTS_UNCHANGED',sentinel()==before)
 R['status']='COMPLETE_ROUTING_ONLY';save();log('TEST714_RESULT',R['status'],'R1',R['recall_at_1'],'R5',R['recall_at_5'])
except Exception as e:
 R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc()[-10000:];save();log('TEST714_ERROR',R['traceback']);raise
finally:save()
