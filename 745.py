# AKBASCORE SILICON HIPPOCAMPUS — TEST745
# Air Tractor AT-802A OR-2025: AIN preliminary report -> CUT3 synthesis -> sealed blind C11
# -> AIN final report (only AFTER C11 sealed) -> self-audit -> sealed C12.
# Single Colab cell, A100 80GB, frozen Qwen2.5-72B NF4, exact locked 709/730 engine.
# STATIC-VALIDATED ONLY. AIN live document resolution and A100 execution are runtime gates.
import os,sys,subprocess,importlib.util,urllib.request,urllib.parse,hashlib,ast,json,time,gc,re,types,traceback,html,platform
from pathlib import Path
from datetime import datetime,timezone
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF','expandable_segments:True')
for mod,pkg in [('torch','torch'),('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50'),('pymupdf','pymupdf'),('bs4','beautifulsoup4'),('psutil','psutil')]:
    if importlib.util.find_spec(mod) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',pkg])
import torch,transformers,bitsandbytes,pymupdf
from bs4 import BeautifulSoup
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
ROOT=Path('/content/AKBASCORE_TEST745' if Path('/content').exists() else '/tmp/AKBASCORE_TEST745')
RAW=ROOT/'sealed_sources';CART=ROOT/'physical_cartridges';TEXT=ROOT/'generated_text'
for p in (ROOT,RAW,CART,TEXT):p.mkdir(parents=True,exist_ok=True)
LOG=ROOT/'TEST745.log';RESULTS=ROOT/'TEST745_results.json';MANIFEST=ROOT/'TEST745_manifest.json'
if LOG.exists() and LOG.stat().st_size:
    raise RuntimeError('TEST745_EXISTING_LOG: use a fresh experiment directory or archive the prior run')
LOG.write_text('',encoding='utf-8')
MODEL_ID='Qwen/Qwen2.5-72B-Instruct';CUT=3;EXPECTED=(80,8192,64,8,128)
DTYPE=torch.bfloat16;DEV=torch.device('cuda:0');CHUNK=128;GPU_RESERVE_GIB=9.0
MAX_NEW=4096;MAX_FINAL_NEW=8192;MAX_ROUNDS=8;MIN_ROUNDS=2
MAX_SOURCE_TOKENS=6500;MAX_SYNTHESIS_TOKENS=22000;MIN_EXTRACT_CHARS=350
SRC709='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/709.py'
SRC730='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/730.py'
LOCK709='6c9f8cbb1eeed848d45133d73f0d7676b68e9125'
LOCK730_GIT='b1bad9eb3b111b44413f8ef05a3a140ab66a77dd'
CASE_URL='https://ain.hr/en/investigations/accident-of-the-aircraft-air-tractor-802a-or-2025-krivi-put-13-november-2025/'
# The case HTML is used ONLY as a link directory, NEVER as model evidence.
# It already contains the official cause; feeding it to the model would invalidate blindness.
# C01..C03 are chronological portions of ONE preliminary report, not independent reports.
SOURCES=[('C01','PRELIMINARY_SEGMENT_1','PRELIMINARY'),('C02','PRELIMINARY_SEGMENT_2','PRELIMINARY'),('C03','PRELIMINARY_SEGMENT_3','PRELIMINARY')]
GROUPS={'S01':['C01','C02'],'S02':['C02','C03'],'S03':['C01','C03']}
HIERARCHY={'H01':['S01','S02'],'H02':['S02','S03'],'H03':['S01','S03']}
R={'test':'745','status':'STARTED','case':'AIN 343-08/25-02/10 / Air Tractor AT-802A OR-2025','sources':{},'cartridges':{},'generations':[],
   'checks':[],'limitations':['A100 runtime not executed by script author','Text-mediated synthesis; no direct tensor fusion',
   'Single historical accident; no generalization claim','Model self-assessment is not independent expert grading',
   'PDF extraction may omit scanned figures or graphical evidence; fail closed for insufficient text',
   'Pretrained model may know this 2025 accident; a blind document protocol cannot erase pretrained knowledge', 'C01-C03 are partitions of ONE preliminary report, not independent corroborating documents']}
def stamp():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def gitblob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def atomic_json(p,x):
 t=Path(str(p)+'.tmp');t.write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str),encoding='utf-8');t.replace(p)
def save():atomic_json(RESULTS,R)
def log(*a):
 s=' '.join(map(str,a));print(s,flush=True)
 with LOG.open('a',encoding='utf-8') as f:f.write(s+'\n')
def check(name,ok,detail=None):
 R['checks'].append({'name':name,'ok':bool(ok),'detail':detail});save();log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
 if not ok:raise RuntimeError('TEST745_'+name)
def sha_file(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def fetch(url,limit=45_000_000):
 req=urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST745-research/1.0','Accept':'application/pdf,text/html,*/*'})
 with urllib.request.urlopen(req,timeout=180) as response:
  data=response.read(limit+1);final=response.geturl()
 check('DOWNLOAD_WITHIN_LIMIT',len(data)<=limit,{'url':url,'bytes':len(data)})
 return data,final
def release():gc.collect();torch.cuda.empty_cache()
def replace_from_ast(raw,names,filename):
 tree=ast.parse(raw.decode('utf-8'));nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
 check('LOCKED_SYMBOLS_'+filename,{n.name for n in nodes}==set(names),sorted(set(names)-{n.name for n in nodes}))
 exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),filename,'exec'),globals())
def pdf_text(data):
 doc=pymupdf.open(stream=data,filetype='pdf');pages=[]
 for i,page in enumerate(doc):
  t=page.get_text('text',sort=True)
  if t.strip():pages.append(f'[PDF PAGE {i+1}]\n'+t)
 return '\n\n'.join(pages),len(doc)
def safe_excerpt(text,cid):
 # Fixed document-order selection; never keyword-select for a desired accident cause.
 text=re.sub(r'\n{4,}','\n\n',text).strip()
 check('EXTRACTABLE_TEXT_'+cid,len(text)>=MIN_EXTRACT_CHARS,{'characters':len(text)})
 ids=tok(text,add_special_tokens=False).input_ids
 excerpt=tok.decode(ids[:MAX_SOURCE_TOKENS],skip_special_tokens=False) if len(ids)>MAX_SOURCE_TOKENS else text
 kept=len(tok(excerpt,add_special_tokens=False).input_ids)
 check('NO_SOURCE_TRUNCATION_'+cid,kept==len(ids),{'original_tokens':len(ids),'kept_tokens':kept})
 return excerpt,len(ids),kept
def resolve_ain_reports(html_bytes):
 # Only link labels and hrefs are inspected. NEVER save or pass the HTML body to the model.
 soup=BeautifulSoup(html_bytes,'html.parser');found={'preliminary':[],'final':[]}
 for a in soup.find_all('a',href=True):
  label=' '.join(a.stripped_strings).strip().lower()
  href=urllib.parse.urljoin(CASE_URL,html.unescape(a['href']))
  if not href.startswith('https://ain.hr/') and not href.startswith('https://www.ain.hr/'):
   continue
  if ('preliminary report' in label or 'preliminarno izvješće' in label):found['preliminary'].append((label,href))
  elif ('final report' in label or 'završno izvješće' in label):found['final'].append((label,href))
 return found

def partition_preliminary(extracted):
 # Document-order, not answer-conditioned. Three slices are parts of a single original.
 ids=tok(extracted,add_special_tokens=False).input_ids
 check('PRELIMINARY_ENOUGH_TOKENS',len(ids)>=450,{'tokens':len(ids)})
 bounds=[round(len(ids)*i/3) for i in range(4)]
 return {f'C{i+1:02d}':tok.decode(ids[bounds[i]:bounds[i+1]],skip_special_tokens=False) for i in range(3)}

def leakage_guard(text):
 # A preliminary report may discuss "probable cause" or "final report" in
 # generic disclaimers. A keyword alone is NOT evidence of leaked findings.
 # Audit each occurrence in context; reject explicit causal findings and
 # any document claiming to BE the final report. No text is silently removed.
 norm=re.sub(r'\\s+',' ',text)
 generic=[r'\\bprobable cause\\b',r'\\bfinal report\\b',
          r'\\bfinal conclusions?\\b',r'\\bcontributing factors?\\b']
 contexts=[]
 for pat in generic:
  for match in re.finditer(pat,norm,re.I):
   contexts.append({'term':match.group(0),'context':norm[max(0,match.start()-190):min(len(norm),match.end()+230)]})
 R['preliminary_leakage_review']={'mentions':contexts,'review_method':'contextual; conservative strong-claim rejection'}
 save()
 # Only statements asserting a determination (rather than explaining that
 # the investigation is ongoing) are treated as an automatic leakage gate.
 strong=[
  r'\\b(?:the )?(?:probable|root|primary) cause (?:of (?:the|this) (?:accident|crash) )?(?:was|is|has been determined|has been established)\\b',
  r'\\b(?:investigation|investigators|agency) (?:has |have )?(?:concluded|determined|established) that\\b',
  r'\\b(?:the )?final report (?:concludes|determines|establishes|found)\\b',
  r'\\b(?:the )?cause of (?:the|this) (?:accident|crash) (?:was|is)\\b',
  r'\\buzrok (?:ove )?nesreće (?:je|bio)\\b']
 hits=[pat for pat in strong if re.search(pat,norm,re.I)]
 check('PRELIMINARY_OUTCOME_LEAKAGE_GUARD',not hits,{'strong_claim_patterns':hits,'generic_mentions':len(contexts)})
 check('PRELIMINARY_NOT_FINAL_REPORT',
       not re.search(r'\\bfinal investigation report\\b|\\bfinal accident investigation report\\b',norm[:350],re.I),
       'Inspect document title and first page')
# Preserve unchanged engine definitions; no code patching to force desired conclusions.
try:
 t0=time.perf_counter();save();log('AKBASCORE TEST745 / BLIND AIN CAUSAL SYNTHESIS',stamp())
 check('CUDA',torch.cuda.is_available());check('ONE_GPU',torch.cuda.device_count()==1)
 gpu_name=torch.cuda.get_device_name(0);total=torch.cuda.get_device_properties(0).total_memory
 check('A100_80GB','A100' in gpu_name and total>=70*2**30,gpu_name)
 raw709,_=fetch(SRC709,500_000);raw730,_=fetch(SRC730,500_000)
 check('709_GIT_BLOB_LOCK',gitblob(raw709)==LOCK709,gitblob(raw709))
 check('730_GIT_BLOB_LOCK',gitblob(raw730)==LOCK730_GIT,gitblob(raw730))
 replace_from_ast(raw709,{'pairs','cache_build','replace','half','rope','rephase','sentinel','free_gpu','ensure_room','kv_digest','full_kv_seal','append','answer','mem'},'709.py')
 replace_from_ast(raw730,{'DirectCut3','forge_native','initialize_native','to_gpu','seal_cp'},'730.py')
 # PRE-GPU evidence stage: resolve official links, download ONLY the preliminary PDF.
 # The official AIN case page contains the cause: its bytes must NEVER enter model prompts.
 page,case_resolved=fetch(CASE_URL,5_000_000)
 links=resolve_ain_reports(page)
 check('PRELIMINARY_LINK_FOUND',len(links['preliminary'])>=1,links)
 check('FINAL_LINK_FOUND',len(links['final'])>=1,links)
 # Prefer the English-labeled document; fail closed on ambiguous duplicate English links.
 prelim=[x for x in links['preliminary'] if x[0]=='preliminary report'] or links['preliminary']
 final=[x for x in links['final'] if x[0]=='final report'] or links['final']
 check('PRELIMINARY_LINK_UNAMBIGUOUS',len(set(u for _,u in prelim))==1,prelim)
 check('FINAL_LINK_UNAMBIGUOUS',len(set(u for _,u in final))==1,final)
 preliminary_url=prelim[0][1];FINAL_URL=final[0][1]
 R['ain_links']={'case_url':CASE_URL,'preliminary_url':preliminary_url,'final_url_sealed_not_fetched':FINAL_URL,'case_page_sha256_quarantined':sha(page)};save()
 # Never store the case page in source_text or TEXT. It is not admissible evidence.
 raw,prelim_resolved=fetch(preliminary_url,40_000_000)
 check('PRELIMINARY_PDF_SIGNATURE',raw[:5]==b'%PDF-',{'url':prelim_resolved,'head':raw[:10].hex()})
 (RAW/'AIN_PRELIMINARY.pdf').write_bytes(raw)
 extracted,npages=pdf_text(raw)
 check('PRELIMINARY_EXTRACTED',len(extracted)>=1400,{'pages':npages,'chars':len(extracted)})
 leakage_guard(extracted)
 (RAW/'AIN_PRELIMINARY_EXTRACT.txt').write_text(extracted,encoding='utf-8')
 R['preliminary']={'url':prelim_resolved,'pdf_sha256':sha(raw),'extracted_sha256':sha(extracted.encode()),'pages':npages,'retrieved':stamp()};save()
 # Tokenized splitting happens after tokenizer initialization; no factual fabrication.
 source_text={}
 # The outcome is inaccessible to this program until C11 has been committed and verified.
 check('FRESH_RUN_NO_OLD_SEALS',not any((CART/x).exists() for x in ('C11.pt','C12.pt')) and not (ROOT/'C11_BLIND_SEAL.json').exists(),
       'Use a fresh output directory for every new trial')
 check('FINAL_REPORT_NOT_DOWNLOADED_BEFORE_C11',not (RAW/'AIN_FINAL.pdf').exists())
 tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
 PREFIX='<|im_start|>system\nUse available evidence critically. Separate observations, hypotheses and uncertainties. Never invent document-specific facts.\n<|im_end|>\n<|im_start|>user\nINFORMATION:\n'
 PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
 source_text=partition_preliminary(extracted)
 for cid,_,category in SOURCES:
  segment=source_text[cid];R['sources'][cid]={'title':'AIN preliminary report / '+cid,'category':category,'url':prelim_resolved,'parent_pdf_sha256':sha(raw),'segment_sha256':sha(segment.encode()),'segments_are_independent':False};save()
 quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
 for par in model.parameters():par.requires_grad_(False)
 cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
 check('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,(NL,H,QH,KVH,HD))
 check('FROZEN',all(not p.requires_grad for p in model.parameters()))
 check('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
 weights_before=sentinel();entries={}
 @torch.no_grad()
 def commit(cid,body,role,parents):
  ids=tok(body,add_special_tokens=False).input_ids
  check('NONEMPTY_'+cid,len(ids)>=30 and len(ids)<=9000,len(ids))
  cp,seconds=forge_native(ids,cid);path=CART/(cid+'.pt');tmp=Path(str(path)+'.tmp');torch.save(cp,tmp);tmp.replace(path)
  check('CP_ON_DISK_'+cid,path.exists())
  meta={'id':cid,'role':role,'parents':[{'id':p,'sha256':entries[p]['sha256']} for p in parents],
    'file':path.name,'sha256':sha_file(path),'tensor_sha':seal_cp(cp),'body_sha256':sha(body.encode()),
    'body_tokens':len(ids),'forge_seconds':seconds,'created':stamp()}
  entries[cid]=meta;R['cartridges'][cid]=meta;atomic_json(MANIFEST,{'test':'745','cartridges':entries,'source_manifest':R['sources']});save()
  log('PHYSICAL_SEALED',cid,meta['sha256'],'PARENTS',parents);del cp;release();return meta
 @torch.no_grad()
 def load_cp(cid):
  meta=entries[cid];path=CART/meta['file'];check('FILE_SHA_'+cid,sha_file(path)==meta['sha256'])
  cp=torch.load(path,map_location='cpu',weights_only=True)
  check('TENSOR_SHA_'+cid,seal_cp(cp)==meta['tensor_sha'])
  check('CARTRIDGE_ID_'+cid,cp['book_id']==cid)
  return cp
 @torch.no_grad()
 def physical_answer(cid,question,limit=MAX_NEW):
  global MAX_NEW
  old_limit=MAX_NEW;MAX_NEW=limit
  try:
   cpu=load_cp(cid);gpu=to_gpu(cpu);del cpu
   memory=initialize_native(gpu);check('FULL_80_LAYER_MEMORY_'+cid,len(memory)==80)
   before=full_kv_seal(memory) if False else None
   result=answer(memory,question)
   del memory,gpu;release()
   tokens=len(tok(result,add_special_tokens=False).input_ids)
   rec={'cid':cid,'question_sha256':sha(question.encode()),'answer_sha256':sha(result.encode()),
    'tokens':tokens,'limit':limit,'possible_truncation':tokens>=limit-8,'created':stamp()}
   R['generations'].append(rec);save()
   (TEXT/(cid+'_'+str(len(R['generations']))+'.txt')).write_text(result,encoding='utf-8')
   log('GENERATION',cid,'TOKENS',tokens,'LIMIT',limit,'POSSIBLE_TRUNCATION',rec['possible_truncation'])
   check('GENERATION_NONEMPTY_'+cid,bool(result.strip()))
   check('GENERATION_NOT_TRUNCATED_'+cid,not rec['possible_truncation'])
   return result
  finally:MAX_NEW=old_limit
 # Stage A: source CUT3 cartridges; only first token-ordered excerpt of each factual PDF.
 for cid,needle,category in SOURCES:
  body,total_tokens,kept=safe_excerpt(source_text[cid],cid)
  excerpt_path=RAW/(cid+'_FORGED.txt');excerpt_path.write_text(body,encoding='utf-8')
  R['sources'][cid].update({'full_tokens':total_tokens,'forged_tokens':kept,'forged_text_sha256':sha(body.encode()),
   'excerpt_is_partial':kept<total_tokens});save()
  commit(cid,body,'AIN_PRELIMINARY_SEGMENT',[])
 # Stage B: independent reflection from each physical cartridge, not the original text.
 reflections={}
 for cid,needle,category in SOURCES:
  q=('Analyze this factual investigative record independently. Separate direct observations, uncertainties, '
     'alternative interpretations, and what additional evidence would distinguish explanations. '
     'Use the source identifier '+cid+'. Do not assume that the cause is known or that any one record proves it.')
  reflections[cid]=physical_answer(cid,q)
 # Stage C: three overlapping document-part syntheses from model-generated readouts.
 def synthesize_text(cid,parts,task,limit=MAX_NEW):
  # Synthesis is explicitly TEXT-mediated, as in proven TEST730; never claim tensor fusion.
  prompt=('You are conducting an independent, evidence-limited investigation. '
          'Synthesize the following separately recovered investigative perspectives. '
          'Distinguish observation from inference, consider rival hypotheses, and cite IDs. '
          'Do not use knowledge of a published final investigation outcome.\n\n'+task+'\n\n'+
          '\n\n'.join('['+k+'] '+v for k,v in parts.items())+'\n\nSYNTHESIS:')
  # Model prompt must not be silently truncated. Limit source reflections by explicit failure, not cherry-picking.
  n=len(tok(prompt,add_special_tokens=False).input_ids)
  check('SYNTHESIS_CONTEXT_FITS_'+cid,n<=MAX_SYNTHESIS_TOKENS,{'tokens':n,'max':MAX_SYNTHESIS_TOKENS})
  global MAX_NEW
  old=MAX_NEW;MAX_NEW=limit
  try:res=answer(None,prompt)
  finally:MAX_NEW=old
  rec={'cid':cid,'prompt_sha256':sha(prompt.encode()),'answer_sha256':sha(res.encode()),'tokens':len(tok(res,add_special_tokens=False).input_ids),'limit':limit}
  R['generations'].append(rec);save()
  check('SYNTHESIS_NONEMPTY_'+cid,len(res)>150)
  check('SYNTHESIS_NOT_TRUNCATED_'+cid,rec['tokens']<limit-8)
  (TEXT/(cid+'_synthesis.txt')).write_text(res,encoding='utf-8');return res
 stext={}
 for sid,parents in GROUPS.items():
  stext[sid]=synthesize_text(sid,{p:reflections[p] for p in parents},'Develop a subsystem causal explanation and list contradictions.')
  commit(sid,stext[sid],'SUBSYSTEM_SYNTHESIS',parents)
 htext={}
 for hid,parents in HIERARCHY.items():
  # Cross-system analysis reads physical S cartridges, not the raw original documents.
  retrieved={p:physical_answer(p,'Explain the principal subsystem findings, evidence links, and uncertainties.') for p in parents}
  htext[hid]=synthesize_text(hid,retrieved,'Identify interactions between subsystems, rival explanations, and decisive missing evidence.')
  commit(hid,htext[hid],'CROSS_SYSTEM_SYNTHESIS',parents)
 # Stage D: bounded closed-loop self-critique, no answer-specific rules and no confidence-based forced conclusion.
 initial=synthesize_text('INITIAL',{k:physical_answer(k,'State your cross-system hypothesis, evidence, and remaining uncertainties.') for k in HIERARCHY},
   'Form a preliminary accident explanation with competing hypotheses, confidence estimates and disconfirming evidence.')
 history=[initial];R['blind_rounds']=[];save()
 for round_id in range(1,MAX_ROUNDS+1):
  latest=history[-1]
  prompt=('Review your previous investigation hypothesis without access to any official accident conclusion. '
    'Search for internal contradictions, alternative causal pathways, unsupported assumptions and decisive tests. '
    'Revise only if warranted by the evidence. End with a complete updated hypothesis, alternatives, '
    'confidence assessment, and a section headed OPEN_UNCERTAINTIES.\n\nPREVIOUS ANALYSIS:\n'+latest)
  check('LOOP_PROMPT_FITS_'+str(round_id),len(tok(prompt,add_special_tokens=False).input_ids)<=MAX_SYNTHESIS_TOKENS)
  old=MAX_NEW;MAX_NEW=4096
  try:new=answer(None,prompt)
  finally:MAX_NEW=old
  nt=len(tok(new,add_special_tokens=False).input_ids)
  check('LOOP_NOT_TRUNCATED_'+str(round_id),nt<4096-8)
  check('LOOP_NONEMPTY_'+str(round_id),len(new)>150)
  (TEXT/f'blind_round_{round_id:02d}.txt').write_text(new,encoding='utf-8')
  history.append(new);R['blind_rounds'].append({'round':round_id,'sha256':sha(new.encode()),'tokens':nt});save()
  # Deterministic hard cap; no semantic quick fix, no manufactured confidence score.
 # Stage E: seal first hypothesis and the physical C11 BEFORE outcome download.
 blind_final=history[-1]
 blind_questions=[
  'Give your best-supported causal account of the accident. Distinguish initiating event, crew response, contributing factors and uncertainties.',
  'Give two plausible competing explanations and the evidence that would distinguish them.',
  'Which conclusions remain unsupported or unknowable from the available factual records?']
 blind_body=('SEALED BLIND INVESTIGATION — NO OFFICIAL OUTCOME AVAILABLE AT FORGE TIME\n'
  +'HIERARCHICAL PARENT HASHES: '+json.dumps({k:entries[k]['sha256'] for k in HIERARCHY},sort_keys=True)
  +'\n[FINAL BLIND ANALYSIS]\n'+blind_final)
 check('C11_BODY_CONTEXT_FITS',len(tok(blind_body,add_special_tokens=False).input_ids)<=9000)
 commit('C11',blind_body,'BLIND_MASTER',['H01','H02','H03'])
 blind_answers=[physical_answer('C11',q,MAX_FINAL_NEW) for q in blind_questions]
 R['blind_answers']=[{'question':q,'answer':a,'sha256':sha(a.encode())} for q,a in zip(blind_questions,blind_answers)]
 R['C11_seal']={'sha256':entries['C11']['sha256'],'blind_answers_sha256':sha(json.dumps(R['blind_answers'],sort_keys=True).encode()),'sealed_at':stamp()}
 atomic_json(ROOT/'C11_BLIND_SEAL.json',R['C11_seal']);save()
 check('C11_LOCKED_BEFORE_FINAL',sha_file(CART/'C11.pt')==R['C11_seal']['sha256'])
 # HARD EMBARGO BOUNDARY: final AIN report is fetched only after the blind seal is on disk.
 R['phase']='OFFICIAL_OUTCOME_UNLOCKED';save();log('OFFICIAL_OUTCOME_UNLOCK',stamp())
 final_pdf,final_resolved=fetch(FINAL_URL,30_000_000)
 check('FINAL_PDF_SIGNATURE',final_pdf[:5]==b'%PDF-')
 (RAW/'AIN_FINAL.pdf').write_bytes(final_pdf)
 final_text,pages=pdf_text(final_pdf)
 check('FINAL_EXTRACTABLE',len(final_text)>12000,{'pages':pages,'chars':len(final_text)})
 (RAW/'AIN_FINAL_EXTRACT.txt').write_text(final_text,encoding='utf-8')
 R['official_outcome']={'url':final_resolved,'pdf_sha256':sha(final_pdf),'text_sha256':sha(final_text.encode()),
   'pages':pages,'retrieved':stamp()};save()
 # The evaluation sees the official report, but never alters C11.
 # Fixed, transparent extraction of AIN findings sections; record full report for audit.
 final_ids=tok(final_text,add_special_tokens=False).input_ids
 # Evaluation excerpt combines introductory factual record and later official findings.
 # No final-report text is accessed before the C11 seal.
 lower=final_text.lower();matches=list(re.finditer(r'probable cause|conclusions|findings',lower))
 candidate=[m.start() for m in matches if m.start()>len(final_text)*0.18]
 key_pos=candidate[-1] if candidate else int(len(final_text)*0.65)
 official_excerpt=final_text[:7000]+'\n\n[OFFICIAL FINDINGS EXCERPT]\n'+final_text[max(0,key_pos-1800):key_pos+21000]
 official_excerpt=tok.decode(tok(official_excerpt,add_special_tokens=False).input_ids[:6500],skip_special_tokens=False)
 (RAW/'AIN_FINAL_EVALUATION_EXCERPT.txt').write_text(official_excerpt,encoding='utf-8')
 R['official_outcome']['evaluation_excerpt_sha256']=sha(official_excerpt.encode());save()
 audit_prompt=('OFFICIAL AIN FINAL REPORT EXCERPT (new evidence, unavailable during the blind phase):\n'+official_excerpt+
   '\n\nPRESEALED BLIND PREDICTIONS:\n'+'\n\n'.join('[Q'+str(i+1)+'] '+x['answer'] for i,x in enumerate(R['blind_answers']))+
   '\n\nCompare the sealed predictions with the official findings. Explicitly identify agreements, disagreements, '
   'unsupported assertions, missed causal mechanisms and unresolved ambiguity. Quote or cite relevant report sections. '
   'Do not rewrite or retrospectively improve the original predictions. Assess your own success and uncertainty.')
 check('AUDIT_CONTEXT_FITS',len(tok(audit_prompt,add_special_tokens=False).input_ids)<=14000)
 old=MAX_NEW;MAX_NEW=MAX_FINAL_NEW
 try:audit=answer(None,audit_prompt)
 finally:MAX_NEW=old
 check('AUDIT_NOT_TRUNCATED',len(tok(audit,add_special_tokens=False).input_ids)<MAX_FINAL_NEW-8)
 (TEXT/'POST_OUTCOME_SELF_AUDIT.txt').write_text(audit,encoding='utf-8')
 R['self_audit']={'sha256':sha(audit.encode()),'text':audit};save()
 # Separate auditable baseline: the self-audit is a model claim, NOT an expert score.
 human_review=('HUMAN REVIEW STATUS: NOT PROVIDED. Official AIN findings are not a substitute for '
               'an independent human grading of the model predictions. Human corrections may be appended '
               'later as a separately sealed child; none are fabricated in TEST745.')
 c12body=('HUMAN–AI MASTER (HUMAN REVIEW PENDING)\nPARENT C11 FILE SHA256: '+entries['C11']['sha256']+
   '\nOFFICIAL AIN FINAL REPORT SHA256: '+R['official_outcome']['pdf_sha256']+
   '\n\n[SEALED ORIGINAL BLIND PREDICTIONS HASH]\n'+R['C11_seal']['blind_answers_sha256']+
   '\n\n[MODEL SELF AUDIT AFTER OFFICIAL OUTCOME]\n'+audit+'\n\n[HUMAN REVIEW]\n'+human_review)
 check('C12_BODY_FITS',len(tok(c12body,add_special_tokens=False).input_ids)<=9000)
 commit('C12',c12body,'HUMAN_AI_MASTER_HUMAN_REVIEW_PENDING',['C11'])
 check('C11_IMMUTABLE',sha_file(CART/'C11.pt')==R['C11_seal']['sha256'])
 check('C12_PARENT_SHA',entries['C12']['parents'][0]['sha256']==entries['C11']['sha256'])
 check('FROZEN_SENTINEL_UNCHANGED',sentinel()==weights_before)
 R['status']='COMPLETED';R['elapsed_seconds']=round(time.perf_counter()-t0,2);save()
 log('TEST745_COMPLETED','C11',entries['C11']['sha256'],'C12',entries['C12']['sha256'],'SECONDS',R['elapsed_seconds'])
except Exception as exc:
 R['status']='FAILED_CLOSED';R['error']=repr(exc);R['traceback']=traceback.format_exc();save()
 log('TEST745_FAILED_CLOSED',repr(exc));traceback.print_exc();raise
finally:
 log('OUTPUT_DIR',ROOT)
