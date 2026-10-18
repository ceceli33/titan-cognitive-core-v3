# AKBASCORE TEST710 | FULL SIEMENS 2025 PDF | SINGLE CUT3 CARTRIDGE
# Runs in ONE Google Colab A100-80GB cell. UNTESTED ON GPU.
# Reuses the exact 709 engine functions; does not change CUT3/RoPE/NF4/BF16.
import os,sys,urllib.request,hashlib,traceback,json,time,re,subprocess,importlib.util
from pathlib import Path
BASE_URL='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/709.py'
PDF_URL='https://cache.industry.siemens.com/dl/files/087/109994087/att_1338962/v1/ONE_universal_op_man_0725_en-US.pdf'
ROOT710=Path('/content/AKBASCORE_TEST710');ROOT710.mkdir(parents=True,exist_ok=True)
def download(url,limit=60*1024*1024):
 req=urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST710/1.0'})
 with urllib.request.urlopen(req,timeout=120) as f:data=f.read(limit+1)
 if len(data)>limit:raise RuntimeError('DOWNLOAD_SIZE_LIMIT')
 return data
def digest(b):return hashlib.sha256(b).hexdigest()
base=download(BASE_URL,2*1024*1024);base_sha=digest(base);base_text=base.decode('utf-8-sig')
anchor="try:\n log('='*105)"
if anchor not in base_text:raise RuntimeError('709_ENGINE_LAYOUT_CHANGED_STOP')
# Keep the upstream engine definitions intact, replace only its experimental driver.
engine=base_text[:base_text.index(anchor)]
engine=engine.replace("ROOT=Path('/content/AKBASCORE_TEST708')","ROOT=Path('/content/AKBASCORE_TEST710')")
engine=engine.replace("OUT=ROOT/'TEST708_results.json';LOG=ROOT/'TEST708.log'","OUT=ROOT/'TEST710_results.json';LOG=ROOT/'TEST710.log'")
engine=engine.replace("TEST='708';REV='708-R2'","TEST='710';REV='710-INITIAL'")
engine=engine.replace("data=f.read(12*1024*1024+1)","data=f.read(60*1024*1024+1)")
engine=engine.replace("if len(data)>12*1024*1024:raise RuntimeError('SOURCE_TOO_LARGE')","if len(data)>60*1024*1024:raise RuntimeError('SOURCE_TOO_LARGE')")
ns={'__name__':'__main__'}
exec(compile(engine,'709_ENGINE_FOR_710','exec'),ns,ns)
# 709 uses these globals. The runtime environment and all engine methods are preserved.
ns['TEST']='710';ns['REV']='710-INITIAL';ns['R']={'test':'710','revision':'710-INITIAL','status':'STARTED','model':ns['MODEL_ID'],'cut':ns['CUT'],'upstream_709_sha256':base_sha,'pdf_url':PDF_URL,'checks':[],'trials':[],'books':[]}
R=ns['R'];log=ns['log'];save=ns['save'];ck=ns['ck'];mem=ns['mem'];sha=ns['sha']
try:
 log('TEST710 FULL PDF / ONE CUT3 CARTRIDGE / FIVE QUESTIONS / NO TRUNCATION')
 ck('CUDA',ns['torch'].cuda.is_available());ck('SINGLE_GPU',ns['torch'].cuda.device_count()==1)
 ck('A100_80GB',ns['torch'].cuda.get_device_properties(0).total_memory>=70*2**30)
 if importlib.util.find_spec('fitz') is None:subprocess.check_call([sys.executable,'-m','pip','install','-q','pymupdf'])
 import fitz
 raw=download(PDF_URL);pdf_sha=digest(raw)
 doc=fitz.open(stream=raw,filetype='pdf');pages=[p.get_text('text',sort=True).strip() for p in doc]
 R['pdf']={'pages':len(pages),'sha256':pdf_sha,'bytes':len(raw),'page_character_counts':[len(p) for p in pages]}
 log('SOURCE_PDF_SHA256',pdf_sha,'PAGES',len(pages),'BYTES',len(raw));save()
 ck('ALL_PAGES_TEXT_EXTRACTED',all(len(x)>40 for x in pages),[i+1 for i,x in enumerate(pages) if len(x)<=40])
 # Five deterministic page anchors chosen without inspecting the model answers.
 idxs=[round((len(pages)-1)*f) for f in (0.1,0.3,0.5,0.7,0.9)]
 def heading(t):
  lines=[re.sub(r'\s+',' ',s).strip() for s in t.splitlines()]
  matches=[s for s in lines if 12<=len(s)<=90 and re.search('[A-Za-z]{3}',s) and not re.match(r'^(SINUMERIK|Siemens AG|Operating Manual|©|Table of contents)',s,re.I)]
  return matches[0] if matches else None
 gold=[heading(pages[i]) for i in idxs]
 ck('FIVE_PAGE_GOLD_ANCHORS',len(set(idxs))==5 and all(gold),list(zip([i+1 for i in idxs],gold)))
 questions=[f'What is the first substantive heading or text line printed on PDF page {i+1} of the Siemens manual? Give the exact wording; if unsure, say UNKNOWN.' for i in idxs]
 R['questions']=[{'pdf_page':i+1,'question':q,'gold':g,'gold_sha256':digest(g.encode())} for i,q,g in zip(idxs,questions,gold)]
 log('FIVE_QUESTIONS_LOCKED',json.dumps(R['questions'],ensure_ascii=False));save()
 text='\n'.join(f'\n[PDF PAGE {i+1} OF {len(pages)}]\n{p}\n' for i,p in enumerate(pages))
 R['pdf']['extracted_text_sha256']=digest(text.encode())
 # Keep PDF for audit until cartridge is sealed. Never put document text in QA prompt.
 ns['RAW'].joinpath('A.pdf').write_bytes(raw)
 tok=ns['AutoTokenizer'].from_pretrained(ns['MODEL_ID'],trust_remote_code=False)
 body=tok(text,add_special_tokens=False,verbose=False).input_ids
 R['pdf']['token_count']=len(body);log('FULL_DOCUMENT_TOKEN_COUNT',len(body));save()
 quant=ns['BitsAndBytesConfig'](load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=ns['DTYPE'],bnb_4bit_use_double_quant=True)
 model=ns['AutoModelForCausalLM'].from_pretrained(ns['MODEL_ID'],quantization_config=quant,dtype=ns['DTYPE'],device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
 for p in model.parameters():p.requires_grad_(False)
 ns['model']=model;cfg=model.config
 NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
 ns.update(NL=NL,H=H,QH=QH,KVH=KVH,HD=HD,tok=tok)
 ck('ARCH',(NL,H,QH,KVH,HD)==ns['EXPECTED'],[NL,H,QH,KVH,HD])
 ck('FROZEN',all(not p.requires_grad for p in model.parameters()))
 prefix='<|im_start|>system\nUse only the available document memory for document-specific questions. If evidence is missing, say UNKNOWN.\n<|im_end|>\n<|im_start|>user\nINFORMATION:\n'
 pids=tok(prefix,add_special_tokens=False).input_ids;ns.update(PIDS=pids,P=len(pids))
 before=ns['sentinel']();R['weights_before']=before
 n=len(body)+len(pids);kvbytes=NL*KVH*HD*2*2;free,_=ns['torch'].cuda.mem_get_info()
 cap=int((free-ns['GPU_RESERVE_GIB']*2**30)//kvbytes)
 R['capacity']={'tokens':n,'kv_only_gib':round(n*kvbytes/2**30,3),'kv_only_limit_tokens':cap,'max_positions':getattr(cfg,'max_position_embeddings',None),'gpu':mem()}
 log('CAPACITY_AUDIT',R['capacity']);save()
 ck('POSITION_LIMIT',n+ns['MAX_NEW']+512<=getattr(cfg,'max_position_embeddings',131072))
 ck('KV_ONLY_FITS',n+ns['MAX_NEW']+512<=cap,R['capacity'])
 # Baseline: same exact five questions, without document and without cartridge.
 ns['trial']('NO_MEMORY',[],questions)
 R['books']=[{'id':'A','title':'Siemens SINUMERIK ONE complete 2025 PDF','url':PDF_URL,'source_sha256':pdf_sha,'requested_tokens':len(body)}]
 cp,secs=ns['forge_stream'](body,'A');cp['source_sha256']=pdf_sha;cp['text_sha256']=R['pdf']['extracted_text_sha256']
 cart=ns['CART']/'A.pt';ns['torch'].save(cp,cart)
 R['books'][0].update(cartridge_sha256=digest(cart.read_bytes()),cartridge_bytes=cart.stat().st_size,forge_seconds=secs)
 log('CARTRIDGE_SHA256',R['books'][0]['cartridge_sha256']);save()
 del cp,body,text,raw,pages,doc
 for p in ns['RAW'].iterdir():p.unlink()
 ck('SOURCE_FILES_REMOVED',not any(ns['RAW'].iterdir()))
 ns['free_gpu']()
 ns['trial']('CUT3_FULL_DOCUMENT',['A'],questions)
 def norm(s):return re.sub(r'[^a-z0-9]+',' ',s.casefold()).strip()
 for trial in R['trials']:
  for j,row in enumerate(trial['qa']):
   row.update(pdf_page=idxs[j]+1,gold=gold[j],exact_match=norm(row['raw'])==norm(gold[j]))
  trial['exact_matches']=sum(row['exact_match'] for row in trial['qa'])
  log('SCORE',trial['label'],trial['exact_matches'],'/5')
 R['weights_after']=ns['sentinel']();ck('WEIGHTS_UNCHANGED',R['weights_before']==R['weights_after'])
 R['status']='COMPLETE_RESULTS_RECORDED'
except Exception as e:
 R['status']='CAPACITY_FAIL' if any(s in str(e) for s in ('GPU_SAFETY_STOP','KV_ONLY_FITS','POSITION_LIMIT','CUDA out of memory')) else 'ERROR'
 R['error']=repr(e);R['traceback']=traceback.format_exc()[-12000:]
 log('TEST710_STOP',R['status'],repr(e));log(R['traceback'])
finally:
 save();log('TEST710_STATUS',R['status']);log('RESULTS',ns['OUT']);log('LOG',ns['LOG'])
