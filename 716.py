# AKBASCORE TEST716 — QWEN72B NATIVE-ACTIVATION ADDRESSING / SIEMENS CUT3
# Standalone Colab A100-80GB; untested on GPU. TEST709 engine functions loaded unchanged by AST.
# Addressing is UNSUPERVISED and uses no question gold, page number, or answer string.
import os,sys,subprocess,importlib.util,urllib.request,hashlib,ast,json,time,gc,random,traceback,re
from pathlib import Path
for mod,pkg in [('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50'),('pymupdf','pymupdf'),('sklearn','scikit-learn')]:
 if importlib.util.find_spec(mod) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',pkg])
import torch,numpy as np,pymupdf as fitz
from sklearn.decomposition import PCA
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
from io import BytesIO
TEST='716';ROOT=Path('/content/AKBASCORE_TEST714');ROOT.mkdir(parents=True,exist_ok=True)
CART=ROOT/'cartridges';CART.mkdir(exist_ok=True);OUT=ROOT/'TEST716_results.json'
MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;DTYPE=torch.bfloat16;DEV=torch.device('cuda:0');EXPECTED=(80,8192,64,8,128)
CHUNK=256;MAX_NEW=48;GPU_RESERVE_GIB=9.;NL=80;H=8192;QH=64;KVH=8;HD=128
SOURCE709='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/709.py'
LOCK709='6c9f8cbb1eeed848d45133d73f0d7676b68e9125' # Git blob SHA1, not SHA256
PDF_URL='https://cache.industry.siemens.com/dl/files/087/109994087/att_1338962/v1/ONE_universal_op_man_0725_en-US.pdf'
PDF_SHA='88c0f8293ce3302135042baf35d704303fb3b5a24915e28b8ca16f3192a7cc1d'
# TEST716 uses deterministic document-derived unique section headings, not the TEST715 thematic panel.
# Section-title wording is visible in the query: this is a routing test, NOT hidden-fact QA or semantic understanding proof.
PANEL=[]
# Zero-index golds above follow previously recorded 10 page ranges; validation below verifies the mapping.
R={'test':TEST,'status':'STARTED','engine':'709.py AST function extraction','method':'Locked TOP2 primary versus PCA128/MAXMEAN/PEAK50; unique PDF heading panel; no training or labels in ranking','queries':[],'limits':['GPU run not performed by code author','New document-derived heading panel; unique normalized headings only; lexical cues exist; NOT independent hidden-fact QA','Model-internal CUT3 activation space may not be a semantic retrieval embedding','No gold labels used in scoring; no fitted supervised parameters','This test does not claim accurate answer generation or RAG superiority']}
def log(*a):print(*a,flush=True)
def save():OUT.write_text(json.dumps(R,indent=2,ensure_ascii=False,default=str))
def sha(x):return hashlib.sha256(x).hexdigest()
def fetch(url,limit):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST715'}),timeout=180) as f:b=f.read(limit+1)
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
 # Build a deterministic, source-grounded panel from actual PDF headings BEFORE routing.
 # Extract lines starting with numbered section identifiers; require occurrence in exactly one cartridge.
 # Do not consult embeddings, model responses, or rankings when choosing the panel.
 import collections
 heading_re=re.compile(r'^\s*((?:[1-9]\d?)(?:\.[1-9]\d?){1,3})\s+([A-Za-z][A-Za-z0-9 /,()\-–:]+?)\s*$')
 candidates=[]
 for ci,(a,b) in enumerate(bounds):
  for pg in range(a,b+1):
   for line in doc[pg-1].get_text(sort=True).splitlines():
    m=heading_re.match(line.strip())
    if not m:continue
    label=' '.join(m.group(2).split()).strip(' .:-')
    if not (15<=len(label)<=90 and len(label.split())>=3 and not re.search(r'\.{3,}|\d{3,}',label)):continue
    normkey=re.sub(r'[^a-z0-9]+',' ',label.lower()).strip()
    candidates.append((ci,pg,m.group(1),label,normkey))
 bykey=collections.defaultdict(set)
 for ci,pg,num,label,key in candidates:bykey[key].add(ci)
 unique=[x for x in candidates if len(bykey[x[4]])==1]
 panel=[];seen=set()
 for ci in range(10):
  group=[]
  for x in unique:
   if x[0]!=ci or x[4] in seen:continue
   seen.add(x[4]);group.append(x)
  group.sort(key=lambda x:hashlib.sha256((str(x[1])+'|'+x[4]).encode()).hexdigest())
  panel.extend(group[:6])
 R['panel_source']={'heading_candidates':len(candidates),'unique_cartridge_heading_candidates':len(unique),'selected':len(panel),'per_cartridge':dict(collections.Counter(x[0]+1 for x in panel)),'selection':'SHA256 sort, up to 6 unique headings per cartridge, before scoring'}
 ck('PANEL_MIN_30',len(panel)>=30)
 R['panel']=[{'cartridge':f'C{x[0]+1:02d}','pdf_page':x[1],'section_number':x[2],'heading':x[3]} for x in panel]
 # Two query phrasings per unique heading; gold is used only in evaluation.
 QUESTIONS=[]
 for ci,pg,num,label,key in panel:
  QUESTIONS.append((f'Which part of the Siemens SINUMERIK ONE manual covers {label}?',ci,0))
  QUESTIONS.append((f'Find the manual section about {label}.',ci,1))
 R['query_design']={'unique_headings':len(panel),'queries':len(QUESTIONS),'paraphrases_per_heading':2,'new_topics_not_TEST715':True,'lexical_heading_in_query':True,'gold_from_unique_pdf_heading':True,'not_blind_qa':True}
 log('PANEL_READY',json.dumps(R['panel_source']));save()
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
  if path.exists() and (CART/(bid+'.sha256')).exists() and sha(path.read_bytes())==(CART/(bid+'.sha256')).read_text().strip() and torch.load(path,map_location='cpu',weights_only=True).get('body_tokens')==len(body):
   log('REUSE_SHA_VERIFIED',bid)
  else:
   log('FORGE',bid,'TOKENS',len(body));cp,secs=forge_stream(body,bid);torch.save(cp,path);(CART/(bid+'.sha256')).write_text(sha(path.read_bytes()));del cp;free_gpu()
  R['books'][i].update({'cartridge_sha256':sha(path.read_bytes()),'body_tokens':len(body),'page_range':bounds[i]});save()
 del pdf,doc,bodies;gc.collect()
 # Physical CUT3 H3 native activations: evenly sampled positions, never page labels or gold.
 # Preserve TEST714's PCA128 baseline exactly; add native scoring from original 8192D vectors.
 rng=np.random.default_rng(714);BANK=[];OWN=[];PER=512
 for i in range(10):
  cp=torch.load(CART/(f'C{i+1:02d}.pt'),map_location='cpu',weights_only=True)
  x=cp['h'][0,P:,:].float();inds=np.linspace(0,len(x)-1,min(PER,len(x)),dtype=np.int64)
  BANK.append(x[torch.from_numpy(inds)].numpy());OWN.extend([i]*len(inds));del cp,x
 X=np.concatenate(BANK).astype(np.float32);OWN=np.array(OWN,dtype=np.int32)
 pca=PCA(n_components=128,svd_solver='randomized',random_state=714)
 Z=pca.fit_transform(X);Z/=np.maximum(np.linalg.norm(Z,axis=1,keepdims=True),1e-8)
 # Native H3 vectors are normalized once; never compressed for exact reranking.
 X/=np.maximum(np.linalg.norm(X,axis=1,keepdims=True),1e-8)
 XB=[np.ascontiguousarray(X[OWN==i].T) for i in range(10)]
 ZB=[np.ascontiguousarray(Z[OWN==i].T) for i in range(10)]
 @torch.no_grad()
 def query_activation(question):
  s='<|im_start|>user\n'+question+'\n<|im_end|>\n<|im_start|>assistant\n'
  ids=tok(s,add_special_tokens=False).input_ids;outbuf=[]
  def cap(mod,args,out):outbuf.append((out[0] if isinstance(out,(tuple,list)) else out).detach().float().cpu())
  hook=model.model.layers[CUT].register_forward_hook(cap)
  try:
   out=model(input_ids=torch.tensor([ids],device=DEV),use_cache=False,return_dict=True);del out
  finally:hook.remove()
  return outbuf[0][0].numpy().astype(np.float32)
 def norm(x):return x/np.maximum(np.linalg.norm(x,axis=1,keepdims=True),1e-8)
 def rank(scores):return sorted(range(10),key=lambda i:(-scores[i],i))
 def metrics(q,bank):
  # Compare each question position with ALL 512 sampled positions in one cartridge.
  sim=q@bank;peaks=np.partition(sim,-2,axis=1)[:,-2:]
  return float(peaks.max(axis=1).mean()),float(peaks.mean(axis=1).mean()),float(np.quantile(peaks.max(axis=1),0.5))
 # Locked primary method: native H3 TOP2 selected from TEST715, no tuning on this panel.
 R['primary_method']='NATIVE8192_TOP2'
 R['routing_methods']=['PCA128_MAXMEAN','NATIVE8192_MAXMEAN','NATIVE8192_TOP2','NATIVE8192_PEAK50']
 for j,(question,gold,variant) in enumerate(QUESTIONS):
  q=query_activation(question);qn=norm(q);qz=norm(pca.transform(q))
  pca_scores=[metrics(qz,b)[0] for b in ZB]
  nm=[metrics(qn,b) for b in XB]
  scores={'PCA128_MAXMEAN':pca_scores,'NATIVE8192_MAXMEAN':[a for a,b,c in nm],
          'NATIVE8192_TOP2':[b for a,b,c in nm],'NATIVE8192_PEAK50':[c for a,b,c in nm]}
  results={}
  for method,sc in scores.items():
   ordered=rank(sc)
   results[method]={'selected':f'C{ordered[0]+1:02d}','top5':[f'C{i+1:02d}' for i in ordered[:5]],'hit1':ordered[0]==gold,'hit5':gold in ordered[:5],
                    'gold_rank':ordered.index(gold)+1,'scores':[round(float(v),6) for v in sc]}
  row={'case':j,'variant':variant,'question':question,'gold_cartridge':f'C{gold+1:02d}','methods':results}
  R['queries'].append(row);log('ROUTE',json.dumps(row,ensure_ascii=False));save()
 R['summary']={method:{'r1':sum(row['methods'][method]['hit1'] for row in R['queries']),
                        'r5':sum(row['methods'][method]['hit5'] for row in R['queries']),
                        'n':len(R['queries']),
                        'first_phrasing_r1':sum(row['methods'][method]['hit1'] for row in R['queries'] if row['variant']==0)}
               for method in R['routing_methods']}
 log('ROUTING_SUMMARY',json.dumps(R['summary']))
 ck('WEIGHTS_UNCHANGED',sentinel()==before)
 R['status']='COMPLETE_ROUTING_COMPARISON';save();log('TEST716_RESULT',R['status'],json.dumps(R['summary']))
except Exception as e:
 R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc()[-10000:];save();log('TEST716_ERROR',R['traceback']);raise
finally:save()
