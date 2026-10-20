# AKBASCORE PROMETHEUS — TEST730 / Native H3 numeric addressing and SHA lineage
# Grounded in locked TEST709 engine as imported by TEST716. Google Colab A100 80GB.
# Research test; not GPU-executed by the author. No claim of PASS before running.
import os,sys,subprocess,importlib.util,urllib.request,hashlib,ast,json,time,gc,traceback,platform,types,copy
from pathlib import Path
from datetime import datetime,timezone
from io import BytesIO
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF','expandable_segments:True')
for m,p in [('torch','torch'),('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50'),('psutil','psutil'),('bs4','beautifulsoup4')]:
 if importlib.util.find_spec(m) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',p])
import torch,transformers,bitsandbytes,psutil
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
ROOT=Path('/content/AKBASCORE_TEST730' if Path('/content').exists() else '/tmp/AKBASCORE_TEST730');ROOT.mkdir(parents=True,exist_ok=True)
LOG=ROOT/'TEST730.log';OUT=ROOT/'TEST730_results.json';LOG.write_text('')
TEST='730';MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
DTYPE=torch.bfloat16;DEV=torch.device('cuda:0');CHUNK=128;MAX_NEW=768;GPU_RESERVE_GIB=9.0
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
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST730'}),timeout=120) as f:b=f.read(limit+1)
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

# TEST730: real 2026 publications; source capture -> immutable physical CUT3 -> free model synthesis -> physical master -> six sealed questions.
# IMPORTANT: This is an orchestrated reading/synthesis pipeline, NOT self-directed unsupervised learning.
# No reference answers, preferred conclusions, or hard-coded evidence relationships are supplied to the model.
import re,html,random
from urllib.parse import urlparse
from html.parser import HTMLParser
CART_DIR=ROOT/'physical_cartridges';CART_DIR.mkdir(parents=True,exist_ok=True)
MANIFEST=ROOT/'TEST730_manifest.json';EVIDENCE_DIR=ROOT/'sealed_sources';EVIDENCE_DIR.mkdir(parents=True,exist_ok=True)
# Real sources, each 2026; license and year are validated from page metadata before use.
# If an article is inaccessible or does not explicitly permit reuse, fail closed; do not substitute invented text.
SOURCES=[
 {'id':'P01','url':'https://www.nature.com/articles/s41599-026-07019-z','role':'learning outcomes'},
 {'id':'P02','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC13521781/','role':'critical thinking and dependency'},
 {'id':'P03','url':'https://doi.org/10.1016/j.caeai.2026.100571','role':'conditional effects'}]
# Presealed questions, NEVER used during reading, synthesis, or cartridge generation.
HUMAN=[
 'What are the main conclusions of the three publications, and where do they disagree?',
 'Which claims are supported by empirical evidence, and what are the main limitations?',
 'After comparing all three publications, what is your own conclusion? Explain uncertainties and cite source IDs.' ]
ADVANCED=[
 'Develop a new causal model that could reconcile apparently conflicting results across the three publications. Separate evidence, assumptions and predictions; cite sources.',
 'Design a preregistered randomized experiment that could falsify your proposed causal model. Specify interventions, measures, confounders and discriminating outcomes.',
 'Identify the most consequential unresolved contradiction, formulate two rival explanations, and propose the smallest decisive test. Explain what each possible result would imply.' ]
QUESTION_SET=[{'id':f'H{i+1}','level':'HUMAN','question':q} for i,q in enumerate(HUMAN)]+[{'id':f'A{i+1}','level':'ADVANCED','question':q} for i,q in enumerate(ADVANCED)]
R['method']='2026 internet documents -> native CUT3 physical source cartridges -> open-ended synthesis -> master CUT3 -> 6 blind questions'
R['limitations']=['No GPU run by code author','Reading and synthesis are orchestrated by general prompts; not autonomous choice of memory operations','Text-mediated synthesis re-encoded to physical H3/KV, not direct tensor fusion','Three sources can differ without being logically contradictory','No human-superiority claim without an independently evaluated human baseline','In-process disk reload; fresh-process reload not established','Licensing and source date must be verified on retrieved pages','No answer key or desired conclusion enters synthesis prompts']
# Robust source acquisition: metadata and article text are separated; licensing is verified from
# explicit CC URL in HTML/XML or Europe PMC full-text XML, never from open-access status alone.
# If an originally proposed URL fails verification, a *disclosed* Europe PMC replacement is
# selected from the same topical category. Selection and immutable source hashes are logged.
from urllib.parse import urlencode,quote
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import date
SOURCE_MAX_CHARS=10500
MIN_SOURCE_CHARS=1400
MAX_SOURCE_TOKENS=3800
TOPIC_QUERIES={
 'P01':'(TITLE_ABS:("generative AI" OR ChatGPT) AND TITLE_ABS:(learning OR achievement OR performance)) AND FIRST_PDATE:[2026-01-01 TO 2026-12-31] AND OPEN_ACCESS:y',
 'P02':'(TITLE_ABS:("generative AI" OR ChatGPT) AND TITLE_ABS:("critical thinking" OR dependence OR cognitive)) AND FIRST_PDATE:[2026-01-01 TO 2026-12-31] AND OPEN_ACCESS:y',
 'P03':'(TITLE_ABS:("generative AI" OR ChatGPT) AND TITLE_ABS:(education OR metacognition OR creativity)) AND FIRST_PDATE:[2026-01-01 TO 2026-12-31] AND OPEN_ACCESS:y'}
CC_RE=re.compile(r'https?://(?:www\.)?creativecommons\.org/licenses/(by(?:-sa|-nc|-nd|-nc-sa|-nc-nd)?)/([34]\.0)(?:/|[\s\"\'<])',re.I)
def http_get(url,limit=6_000_000):
 req=urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-PROMETHEUS/TEST730 (academic research)','Accept':'application/xml,text/xml,text/html,application/xhtml+xml;q=0.9,*/*;q=0.7'})
 with urllib.request.urlopen(req,timeout=90) as resp:
  data=resp.read(limit+1);final=resp.geturl();typ=resp.headers.get('Content-Type','')
 if len(data)>limit:raise RuntimeError('HTTP_BODY_TOO_LARGE:'+url)
 return data,final,typ
def license_match(*parts):
 for part in parts:
  m=CC_RE.search(part or '')
  if m:return m.group(0)
 return None
def normalize_text(s):return re.sub(r'\s+',' ',html.unescape(s)).strip()
def html_article(src):
 data,final,typ=http_get(src['url'])
 if 'html' not in typ.lower() and not data[:200].lstrip().lower().startswith(b'<!doctype html'):raise RuntimeError('SOURCE_NOT_HTML:'+src['id'])
 soup=BeautifulSoup(data,'html.parser')
 metas={}
 for m in soup.find_all('meta'):
  k=(m.get('name') or m.get('property') or '').lower();v=m.get('content','')
  if k and v:metas.setdefault(k,[]).append(v)
 pub=' '.join(v for k in ('citation_publication_date','citation_date','article:published_time','dc.date','dc.date.issued','prism.publicationdate') for v in metas.get(k,[]))
 # License links often live in the HTML head or footer, which must not be included as article text.
 lic=license_match(data.decode('utf-8','replace'),*(m.get('href','') for m in soup.select('a[href]')))
 if not lic:raise RuntimeError('LICENSE_NOT_VERIFIED:'+src['id'])
 if not re.search(r'(?<!\d)2026(?!\d)',pub):raise RuntimeError('PUBLICATION_YEAR_NOT_VERIFIED:'+src['id']+':'+repr(pub[:100]))
 container=soup.select_one('article') or soup.select_one('main')
 if container is None:raise RuntimeError('ARTICLE_BODY_NOT_FOUND:'+src['id'])
 for bad in container.select('script,style,nav,footer,header,aside,form,figure,table,.references,.ref-list,.related-content,.article-metrics,.c-article-footer'):bad.decompose()
 # Use substantive article paragraphs rather than first 11k characters of navigation/boilerplate.
 paragraphs=[normalize_text(el.get_text(' ',strip=True)) for el in container.select('h2,h3,p')]
 paragraphs=[x for x in paragraphs if len(x)>45 and not re.match(r'^(references|acknowledg|funding|conflict of interest|data availability)',x,re.I)]
 body='\n\n'.join(paragraphs)
 if len(body)<MIN_SOURCE_CHARS:raise RuntimeError('INSUFFICIENT_ARTICLE_TEXT:'+src['id'])
 body=body[:SOURCE_MAX_CHARS]
 title=normalize_text((soup.find('h1') or soup.find('title')).get_text(' ',strip=True))
 return {'id':src['id'],'url':src['url'],'resolved_url':final,'title':title,'license':lic,'published':pub[:160],
  'body':body,'full_html_sha256':sha(data),'excerpt_sha256':sha(body.encode()),'excerpt_chars':len(body),'source_method':'ARTICLE_HTML'}
def europe_pmc_search(query):
 api='https://www.ebi.ac.uk/europepmc/webservices/rest/search?'+urlencode({'query':query,'format':'json','pageSize':30,'resultType':'core'})
 data,_,_=http_get(api,1_500_000)
 return json.loads(data)['resultList']['result']
def europe_pmc_fulltext(pmcid,src):
 url='https://www.ebi.ac.uk/europepmc/webservices/rest/'+quote(pmcid,safe='')+'/fullTextXML'
 data,final,_=http_get(url,6_000_000)
 root=ET.fromstring(data)
 # Verify actual published date and license on the full-text article, not on the search page.
 dates=[]
 for d in root.findall('.//front/article-meta/pub-date'):
  y=d.findtext('year');dates.append(y or '')
 if '2026' not in dates:raise RuntimeError('XML_YEAR_NOT_2026:'+pmcid+':'+str(dates))
 licenses=root.findall('.//front/article-meta/permissions/license')
 lic=license_match(*[ET.tostring(x,encoding='unicode') for x in licenses])
 if not lic:raise RuntimeError('XML_LICENSE_NOT_CC:'+pmcid)
 title=normalize_text(' '.join(root.find('.//front/article-meta/title-group/article-title').itertext()))
 body_el=root.find('./body')
 if body_el is None:raise RuntimeError('XML_BODY_MISSING:'+pmcid)
 blocks=[]
 for section in body_el.findall('.//sec'):
  heading=section.find('./title')
  if heading is not None:blocks.append(normalize_text(' '.join(heading.itertext())))
  for para in section.findall('./p'):
   text=normalize_text(' '.join(para.itertext()))
   if len(text)>45:blocks.append(text)
 if not blocks:
  blocks=[normalize_text(' '.join(x.itertext())) for x in body_el.findall('.//p') if len(normalize_text(' '.join(x.itertext())))>45]
 body='\n\n'.join(blocks)[:SOURCE_MAX_CHARS]
 if len(body)<MIN_SOURCE_CHARS:raise RuntimeError('XML_BODY_TOO_SHORT:'+pmcid)
 return {'id':src['id'],'url':src['url'],'resolved_url':final,'title':title,'license':lic,'published':'2026 (article XML)',
  'body':body,'full_html_sha256':sha(data),'excerpt_sha256':sha(body.encode()),'excerpt_chars':len(body),'source_method':'EUROPE_PMC_FULLTEXT','pmcid':pmcid}
def retrieve_publication(src,used_pmcs):
 try:
  if 'pmc.ncbi.nlm.nih.gov/articles/' in src['url']:
   pmc=re.search(r'PMC\d+',src['url'],re.I)
   if not pmc:raise RuntimeError('PMC_ID_MISSING')
   result=europe_pmc_fulltext(pmc.group(0).upper(),src)
   if result['pmcid'] in used_pmcs:raise RuntimeError('DUPLICATE_SOURCE')
   used_pmcs.add(result['pmcid']);return result
  return html_article(src)
 except Exception as primary:
  log('SOURCE_PRIMARY_REJECTED',src['id'],repr(primary))
  R.setdefault('source_rejections',[]).append({'id':src['id'],'url':src['url'],'reason':repr(primary)})
  # Replacements are NEVER silent: record the original URL, chosen PMCID and the reason.
  results=europe_pmc_search(TOPIC_QUERIES[src['id']])
  for rec in results:
   pmcid=rec.get('pmcid')
   if not pmcid or pmcid in used_pmcs:continue
   try:
    p=europe_pmc_fulltext(pmcid,src);p['original_url_rejected']=src['url'];p['replacement_reason']=repr(primary)
    used_pmcs.add(pmcid);log('SOURCE_EXPLICIT_REPLACEMENT',src['id'],pmcid,p['title'],p['license']);return p
   except Exception as err:log('SOURCE_CANDIDATE_REJECTED',src['id'],pmcid,str(err)[:180])
  raise RuntimeError('NO_VERIFIABLE_2026_CC_FULLTEXT:'+src['id']+'; original='+repr(primary))
def sha_file(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def atomic_json(path,obj):
 tmp=Path(str(path)+'.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=str));tmp.replace(path)
def safe_load(entry):
 path=CART_DIR/entry['file'];check('FILE_SHA_'+entry['id'],path.exists() and sha_file(path)==entry['sha256'])
 cp=torch.load(path,map_location='cpu',weights_only=True)
 check('CARTRIDGE_ID_'+entry['id'],cp['book_id']==entry['id'] and cp['p']==P and cp['n']==P+cp['body_tokens'])
 check('CARTRIDGE_TENSOR_SHA_'+entry['id'],seal_cp(cp)==entry['tensor_sha'])
 return cp
def physical_read(entry,question):
 cp=safe_load(entry);gpu_cp=to_gpu(cp);del cp
 memory=initialize_native(gpu_cp);result=answer(memory,question)
 del memory,gpu_cp;release();return result
@torch.no_grad()
def commit(cid,body,role,parents):
 ids=tok(body,add_special_tokens=False).input_ids
 check('NONEMPTY_BODY_'+cid,100<=len(ids)<=9000,{'tokens':len(ids)})
 cp,seconds=forge_native(ids,cid);path=CART_DIR/(cid+'.pt');tmp=Path(str(path)+'.tmp');torch.save(cp,tmp);tmp.replace(path)
 e={'id':cid,'role':role,'parents':parents,'file':path.name,'sha256':sha_file(path),'tensor_sha':seal_cp(cp),
    'body_sha256':sha(body.encode()),'body_tokens':len(ids),'forge_seconds':seconds}
 entries[cid]=e;ledger['cartridges'].append(e);atomic_json(MANIFEST,ledger);del cp;release()
 log('PHYSICAL_COMMIT',cid,role,e['sha256']);return e
try:
 log('='*110);log('AKBASCORE PROMETHEUS — TEST730 — THREE REAL SOURCES / AUTONOMOUS-STYLE SYNTHESIS / SEALED MASTER');log('='*110)
 # Freeze the six questions BEFORE accessing source documents or model.
 panel_file=ROOT/'SEALED_QUESTIONS.json';atomic_json(panel_file,QUESTION_SET)
 panel_sha=sha(panel_file.read_bytes());R['sealed_question_sha256']=panel_sha;log('QUESTION_PANEL_PRESEALED_SHA256',panel_sha)
 check('CUDA_AVAILABLE',torch.cuda.is_available(),{'torch':torch.__version__,'cuda':torch.version.cuda})
 check('ONE_GPU',torch.cuda.device_count()==1)
 check('A100_80GB',torch.cuda.get_device_properties(0).total_memory>=70*2**30,torch.cuda.get_device_name(0))
 raw709=download(SRC709);raw716=download(SRC716)
 check('709_GIT_BLOB_LOCK',gitblob(raw709)==LOCK709,gitblob(raw709));check('716_GIT_BLOB_LOCK',gitblob(raw716)==LOCK716,gitblob(raw716))
 import_reference(raw709)
 # Download and validate all three sources before expensive model load.
 publications=[];used_pmcs=set()
 for source in SOURCES:
  p=retrieve_publication(source,used_pmcs);publications.append(p)
  sealed=EVIDENCE_DIR/(p['id']+'.txt');sealed.write_text(p['body'],encoding='utf-8')
  check('SOURCE_TEXT_SHA_'+p['id'],sha(sealed.read_bytes())==p['excerpt_sha256'])
  log('SOURCE_LOCK',json.dumps({k:v for k,v in p.items() if k!='body'},ensure_ascii=False))
 R['publications']=[{k:v for k,v in p.items() if k!='body'} for p in publications];save()
 check('THREE_DISTINCT_SOURCES',len({p['resolved_url'] for p in publications})==3)
 check('SOURCE_REUSE_LICENSES_VERIFIED',all(p['license'] and 'creativecommons.org/licenses/' in p['license'] for p in publications))
 tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
 PREFIX='<|im_start|>system\nUse only the available document memory for document-specific questions. If the evidence is missing, say UNKNOWN.\n<|im_end|>\n<|im_start|>user\nINFORMATION:\n'
 PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
 quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
 for parameter in model.parameters():parameter.requires_grad_(False)
 cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
 check('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,[NL,H,QH,KVH,HD]);check('FROZEN',all(not p.requires_grad for p in model.parameters()))
 check('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
 check('DIRECT_FORWARD_NO_EXISTING_HOOKS',not model.model.layers[CUT]._forward_hooks and not model.model.layers[CUT]._forward_pre_hooks)
 before=sentinel();entries={};ledger={'test':TEST,'engine':{'709':LOCK709,'716':LOCK716},'model':MODEL_ID,'cut':CUT,'question_sha256':panel_sha,
  'sources':R['publications'],'cartridges':[],'edges':{'MASTER':['P01','P02','P03']}}
 # PHASE 1: feed source texts without question-specific instructions. Each source is a physically persisted neural cartridge.
 for p in publications:
  encoded=tok(p['body'],add_special_tokens=False).input_ids
  if len(encoded)>MAX_SOURCE_TOKENS:
   clipped=tok.decode(encoded[:MAX_SOURCE_TOKENS],skip_special_tokens=False)
   p['body']=clipped;p['excerpt_sha256']=sha(clipped.encode());p['excerpt_chars']=len(clipped);p['token_truncated']=True
   (EVIDENCE_DIR/(p['id']+'.txt')).write_text(clipped,encoding='utf-8')
   R['publications']=[{k:v for k,v in x.items() if k!='body'} for x in publications];ledger['sources']=R['publications'];save()
  check('SOURCE_TEXT_FINAL_SHA_'+p['id'],sha((EVIDENCE_DIR/(p['id']+'.txt')).read_bytes())==p['excerpt_sha256'])
  commit(p['id'],p['body'],'REAL_SOURCE',[])
 check('THREE_PHYSICAL_SOURCES',len(entries)==3)
 # PHASE 2: physically read each source. A general open-ended reflection prompt is identical for all three.
 # No questions from SEALED_QUESTIONS and no preferred answer are used.
 reflections=[]
 for p in publications:
  question='What do you understand from this document? Describe its central claims, evidence, uncertainties and implications in your own words. Do not assume it is correct.'
  reflection=physical_read(entries[p['id']],question)
  check('SOURCE_REFLECTION_NONEMPTY_'+p['id'],len(reflection.strip())>70)
  reflections.append({'id':p['id'],'reflection':reflection,'reflection_sha256':sha(reflection.encode())})
  log('READING_REFLECTION',p['id'],reflection)
 # PHASE 3: unconstrained conclusion. No imposed agreement, disagreement, decision, or answer key.
 # Source reflections are model-generated from neural cartridge readout; this is text-mediated synthesis.
 synthesis_prompt=('Read these three independently remembered perspectives. Think critically, identify what genuinely conflicts and what does not, '
  'weigh the strength of evidence, form your own best synthesis, and explain what would change your mind. '
  'You may agree with one, none or parts of each. State uncertainties and source identifiers. '
  'Do not invent facts or claim to have performed experiments.\n\n'
  +'\n\n'.join('['+r['id']+'] '+r['reflection'] for r in reflections)+'\n\nYOUR INDEPENDENT SYNTHESIS:')
 conclusion=answer(None,synthesis_prompt).strip()
 check('SYNTHESIS_NONEMPTY',len(conclusion)>120,len(conclusion))
 R['model_synthesis']={'text':conclusion,'sha256':sha(conclusion.encode()),'parents':[p['id'] for p in publications]};save();log('MODEL_SYNTHESIS',conclusion)
 # MASTER contains the three source-derived reflections plus the model's own synthesis, never the sealed test questions.
 master_body=('PROMETHEUS REAL-WORLD MASTER MEMORY. Source IDs and independently read perspectives:\n\n'
  +'\n\n'.join('['+r['id']+'] '+r['reflection'] for r in reflections)
  +'\n\nMODEL SYNTHESIS (NOT AN ESTABLISHED FACT):\n'+conclusion)
 commit('MASTER',master_body,'MASTER_SYNTHESIS',['P01','P02','P03'])
 check('FOUR_PHYSICAL_CARTRIDGES',len(entries)==4 and all((CART_DIR/(cid+'.pt')).exists() for cid in entries))
 # PHASE 4: no source text, reflections or parent cartridge is available to answer queries; master only.
 original=dict(entries);entries.clear();entries['MASTER']=original['MASTER']
 check('MASTER_ONLY_ACTIVE',set(entries)=={'MASTER'})
 check('SEALED_QUESTIONS_UNCHANGED',sha(panel_file.read_bytes())==panel_sha)
 results=[]
 for q in QUESTION_SET:
  raw=physical_read(entries['MASTER'],q['question'])
  rec={**q,'answer':raw,'answer_sha256':sha(raw.encode()),'nonempty':bool(raw.strip())}
  results.append(rec);R['questions']=results;save();log('DEMO_QUESTION',q['id'],q['question']);log('DEMO_ANSWER',q['id'],raw)
 # A baseline provides contrast, not an automatic correctness grade.
 baseline=[]
 for q in QUESTION_SET:
  raw=answer(None,q['question']);baseline.append({'id':q['id'],'answer':raw})
 R['no_memory_baseline']=baseline;save()
 cp=safe_load(entries['MASTER']);gpu_cp=to_gpu(cp)
 ref=initialize(gpu_cp);ref_seals=memory_seals(ref);del ref;release()
 direct=initialize_native(gpu_cp);direct_seals=memory_seals(direct)
 check('MASTER_80_LAYER_PARITY',compare_seals(ref_seals,direct_seals),{'matched':sum(a==b for a,b in zip(ref_seals,direct_seals)),'layers':NL})
 del direct,gpu_cp,cp;release()
 check('WEIGHTS_SENTINEL_UNCHANGED',sentinel()==before)
 entries.clear();entries.update(original)
 check('ALL_PHYSICAL_SOURCES_PRESERVED',len(entries)==4 and all((CART_DIR/(cid+'.pt')).exists() for cid in entries))
 summary={'sources':3,'master':1,'question_count':len(results),'human_questions':3,'advanced_questions':3,
  'answered_nonempty':sum(x['nonempty'] for x in results),'ssd_sha_verified':True,'master_80_layer_parity':True,
  'weights_unchanged':True,'independent_correctness_not_yet_graded':True}
 R['summary']=summary;R['status']='DEMO_COMPLETED_UNGRADED' if all(x['nonempty'] for x in results) else 'DEMO_INCOMPLETE';save()
 log('TEST730_RESULT',R['status']);log('SUMMARY',summary);log('RESULT_JSON',OUT,'MANIFEST',MANIFEST,'LOG',LOG)
except Exception as exc:
 R['status']='ERROR';R['error']=repr(exc);R['traceback']=traceback.format_exc();save();log('TEST730_ERROR',R['traceback']);raise
finally:save()
