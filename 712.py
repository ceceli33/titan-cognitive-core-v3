# TEST712 — Position-localized recall / existing physical CUT3 Siemens cartridges.
# Runs in ONE Colab A100-80GB cell. Frozen TEST709 engine; no modifications to its CUT3 mathematics.
# Routing in this experiment is a declared page-number oracle, NOT a learned FRAM/FAISS router.
# The original 709 engine is fetched and SHA-pinned, never guessed or text-anchor-spliced.
import ast,hashlib,urllib.request,sys,subprocess,importlib.util,json,time,traceback,gc,re
from pathlib import Path
if importlib.util.find_spec('pymupdf') is None:subprocess.check_call([sys.executable,'-m','pip','install','-q','pymupdf'])
import pymupdf
BASE_URL='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/709.py'
BASE_BLOB_SHA='6c9f8cbb1eeed848d45133d73f0d7676b68e9125' # Git blob SHA; verify via git blob calculation
PDF_URL='https://cache.industry.siemens.com/dl/files/087/109994087/att_1338962/v1/ONE_universal_op_man_0725_en-US.pdf'
PDF_SHA='88c0f8293ce3302135042baf35d704303fb3b5a24915e28b8ca16f3192a7cc1d'
ROOT712=Path('/content/AKBASCORE_TEST712');ROOT712.mkdir(parents=True,exist_ok=True)
MANIFEST=ROOT712/'manifest.json';RESULT=ROOT712/'TEST712_results.json';LOG712=ROOT712/'TEST712.log';LOG712.write_text('')
S={'test':'712','status':'STARTED','engine':'709.py','routing':'PAGE_ORACLE_PLUS_WITHIN_CARTRIDGE_POSITION_CUES_NOT_LEARNED','questions':[],'cartridges':[],'checks':[]}
def emit(*a):
 s=' '.join(map(str,a));print(s,flush=True)
 with LOG712.open('a') as f:f.write(s+'\n')
def persist():RESULT.write_text(json.dumps(S,ensure_ascii=False,indent=2,default=str))
def check(name,condition,details=None):
 S['checks'].append({'name':name,'pass':bool(condition),'details':details});emit('PASS' if condition else 'FAIL',name,details or '');persist()
 if not condition:raise RuntimeError('CHECK_FAILED_'+name)
def get(url,limit):
 req=urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST712-research'})
 with urllib.request.urlopen(req,timeout=180) as f:
  b=f.read(limit+1)
 if len(b)>limit:raise RuntimeError('DOWNLOAD_SIZE_LIMIT')
 return b
try:
 emit('TEST712 SIEMENS / FROZEN 709 ENGINE / WITHIN-CARTRIDGE POSITION CUE DIAGNOSTIC')
 source=get(BASE_URL,256*1024)
 blob=hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest()
 check('ENGINE_709_BLOB_LOCK',blob==BASE_BLOB_SHA,{'actual':blob,'expected':BASE_BLOB_SHA})
 # Identify the original experiment driver structurally via AST; keep all definitions above it unchanged.
 parsed=ast.parse(source.decode('utf-8-sig'));drivers=[n for n in parsed.body if isinstance(n,ast.Try) and any(isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name) and x.value.func.id=='log' for x in n.body[:4])]
 check('ENGINE_DRIVER_AST_UNIQUE',len(drivers)==1,{'found':len(drivers)})
 driver=drivers[0];engine='\n'.join(source.decode('utf-8-sig').splitlines()[:driver.lineno-1])+'\n'
 # The upstream functions and imports execute exactly as in 709, but its book-demo driver does not.
 exec(compile(engine,'709_ENGINE_UNCHANGED','exec'),globals())
 # Replace ONLY experiment paths/metadata, not CUT3 operations.
 TEST='712';REV='712-POSITION-DIAGNOSTIC';ROOT=ROOT712;RAW=ROOT/'sources';CART=ROOT/'cartridges';RAW.mkdir(exist_ok=True);CART.mkdir(exist_ok=True)
 OUT=RESULT;LOG=LOG712;R=S;R.update({'model':MODEL_ID,'cut':CUT,'limits':['Routing uses known PDF page number; it is an oracle, not learned semantic addressing.','Only five page-heading facts are scored; not full-document comprehension.','All 486 pages are included, but no claim of lossless semantic recall.','NF4 weights are frozen; original 709 CUT3 mechanics are unchanged.']})
 check('CUDA',torch.cuda.is_available());check('SINGLE_GPU',torch.cuda.device_count()==1);check('A100_80GB',torch.cuda.get_device_properties(0).total_memory>=70*2**30)
 pdf=get(PDF_URL,24*1024*1024);actual=hashlib.sha256(pdf).hexdigest();check('PDF_SHA256_LOCK',actual==PDF_SHA,{'sha256':actual,'bytes':len(pdf)})
 doc=pymupdf.open(stream=pdf,filetype='pdf');check('PDF_486_PAGES',len(doc)==486)
 pages=[]
 for i in range(len(doc)):
  content=doc[i].get_text(sort=True)
  check_text=content.strip()
  if not check_text:emit('WARNING EMPTY_PDF_PAGE',i+1)
  pages.append(f'\n[SIEMENS ORIGINAL PDF PAGE {i+1}]\n'+content+'\n[/SIEMENS ORIGINAL PDF PAGE {i+1}]\n')
 check('ALL_PAGES_EXTRACTED',len(pages)==486)
 questions=[(49,'Fundamentals'),(147,'Machining the workpiece'),(243,'Creating a G code program'),(341,'Managing programs'),(437,'Editing the PLC user program')]
 for page,gold in questions:
  check('GOLD_VISIBLE_PAGE_'+str(page),gold.casefold() in pages[page-1].casefold(),{'page':page,'gold':gold})
  S['questions'].append({'pdf_page':page,'gold':gold,'question':f'What is the first substantive section heading printed on PDF page {page} of the Siemens SINUMERIK ONE Universal Operating Manual? Answer with the exact heading only. If uncertain, say UNKNOWN.'})
 persist()
 tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
 token_pages=[tok(x,add_special_tokens=False).input_ids for x in pages]
 total=sum(map(len,token_pages));emit('PDF_EXTRACTED_TOKENS',total)
 # A conservative 18k tokens per cartridge; preserves whole PDF pages; no page omission.
 # Uses smaller than 30k because 709 long-context forging has not been proven at 30k.
 LIMIT=int(os.getenv('AKBASCORE_712_CART_TOKENS','18000'))
 check('CHUNK_LIMIT',1024<=LIMIT<=24000)
 chunks=[];current=[];ids=[];start=1
 for i,pids in enumerate(token_pages,1):
  check('PAGE_WITHIN_CARTRIDGE_'+str(i),len(pids)<=LIMIT,{'tokens':len(pids)}) if len(pids)>LIMIT else None
  if current and len(ids)+len(pids)>LIMIT:
   chunks.append({'first_page':start,'last_page':i-1,'ids':ids});current=[];ids=[];start=i
  current.append(i);ids.extend(pids)
 if current:chunks.append({'first_page':start,'last_page':486,'ids':ids})
 check('NO_TOKEN_LOSS',sum(len(x['ids']) for x in chunks)==total)
 check('ALL_PAGE_RANGES',[(c['first_page'],c['last_page']) for c in chunks][0][0]==1 and chunks[-1]['last_page']==486 and all(a['last_page']+1==b['first_page'] for a,b in zip(chunks,chunks[1:])))
 for i,c in enumerate(chunks,1):
  c['id']=f'C{i:02d}';S['cartridges'].append({'id':c['id'],'pages':[c['first_page'],c['last_page']],'body_tokens':len(c['ids'])})
 emit('CARTRIDGE_PLAN',[(x['id'],x['first_page'],x['last_page'],len(x['ids'])) for x in chunks]);persist()
 quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
 for p in model.parameters():p.requires_grad_(False)
 cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
 check('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,[NL,H,QH,KVH,HD]);check('FROZEN',all(not p.requires_grad for p in model.parameters()))
 check('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
 check('GPU_ONLY',({str(p.device) for p in model.parameters()}|{str(x.device) for x in model.buffers()})=={'cuda:0'})
 before=sentinel();S['weight_sentinel_before']=before
 PREFIX='<|im_start|>system\nUse only the available document memory for document-specific questions. If the evidence is missing, say UNKNOWN.\n<|im_end|>\n<|im_start|>user\nINFORMATION:\n'
 PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
 # Position and physical capacity checks before the expensive forging.
 check('POSITION_LIMIT',max(len(c['ids']) for c in chunks)+P+MAX_NEW+512<=cfg.max_position_embeddings)
 for c in chunks:
  free,_=torch.cuda.mem_get_info();need=(len(c['ids'])+P+1024)*NL*KVH*HD*4+GPU_RESERVE_GIB*2**30
  check('ESTIMATED_GPU_ROOM_'+c['id'],free>=need,{'free_gib':round(free/2**30,2),'need_gib':round(need/2**30,2)})
 # Control before burning. Source is not in model context.
 for q in S['questions']:
  q['baseline_raw']=answer(None,q['question']);emit('BASELINE',q['pdf_page'],repr(q['baseline_raw']));persist()
 # Reuse exactly verified TEST711 physical cartridges when present, avoiding needless GPU forging.
 prior_root=Path('/content/AKBASCORE_TEST711');prior_result=prior_root/'TEST711_results.json';prior=None
 if prior_result.is_file():
  try:
   prior=json.loads(prior_result.read_text());prior_carts=prior.get('cartridges',[])
   valid=(len(prior_carts)==len(chunks) and all(prior_carts[i].get('id')==c['id'] and prior_carts[i].get('pages')==[c['first_page'],c['last_page']] and prior_carts[i].get('body_tokens')==len(c['ids']) and (prior_root/'cartridges'/(c['id']+'.pt')).is_file() for i,c in enumerate(chunks)))
   if not valid:prior=None
  except Exception:prior=None
 # Burn each cartridge with the 709 physical CUT3 function, or reuse SHA-verified TEST711 files.
 for i,c in enumerate(chunks):
  b=S['cartridges'][i];bid=c['id'];path=CART/(bid+'.pt')
  if prior is not None:
   old=prior['cartridges'][i];oldpath=prior_root/'cartridges'/(bid+'.pt')
   raw_hash=hashlib.sha256()
   with oldpath.open('rb') as f:
    for buf in iter(lambda:f.read(8*1024*1024),b''):raw_hash.update(buf)
   check('REUSE_SHA_'+bid,raw_hash.hexdigest()==old.get('cartridge_sha256'))
   b.update({'file_bytes':oldpath.stat().st_size,'cartridge_sha256':old['cartridge_sha256'],'forge_seconds':old.get('forge_seconds'),'book_id':bid,'reused_from_test711':True})
   # The original 709 cart_load looks in CART; point it at the already sealed physical files.
   CART=prior_root/'cartridges';emit('REUSE_TEST711',bid,'SHA256',b['cartridge_sha256']);persist();continue
  emit('FORGE',bid,'PAGES',c['first_page'],c['last_page'],'TOKENS',len(c['ids']))
  cp,seconds=forge_stream(c['ids'],bid)
  cp['source_sha256']=PDF_SHA;cp['pdf_page_range']=(c['first_page'],c['last_page'])
  torch.save(cp,path);b['file_bytes']=path.stat().st_size;b['cartridge_sha256']=sha(path.read_bytes());b['forge_seconds']=seconds
  b['book_id']=bid;check('LOWER_ONLY_'+bid,len(cp['lower'])==CUT+1 and 'upper' not in cp)
  del cp;free_gpu();persist()
 # The 709 cart_load() expects metadata in R['books']; reference existing manifest, no engine changes.
 R['books']=[{'id':b['id'],'cartridge_sha256':b['cartridge_sha256']} for b in S['cartridges']]
 # Exact token offsets are computed from the already sealed page boundaries; never insert gold text into queries.
 # Each target is tested with unchanged original query and three position-only prompts.
 # No text retrieval, gold headings, or source snippets are placed in any prompt.
 for q in S['questions']:
  page=q['pdf_page'];match=[c for c in chunks if c['first_page']<=page<=c['last_page']]
  check('PAGE_ROUTE_UNIQUE_'+str(page),len(match)==1)
  c=match[0];bid=c['id'];q['oracle_cartridge']=bid
  local_start=sum(len(token_pages[j-1]) for j in range(c['first_page'],page))
  local_end=local_start+len(token_pages[page-1]);q['position']={'local_start':local_start,'local_end':local_end,'page_tokens':local_end-local_start,'cartridge_body_tokens':len(c['ids'])}
  # This header exists inside the cartridge; do not inject its content into the question.
  probes=[('ORIGINAL',q['question']),
   ('PAGE_MARKER',f'Locate the literal document marker [SIEMENS ORIGINAL PDF PAGE {page}] in the available memory. Read only the section immediately after that marker. Give its first substantive heading exactly, or UNKNOWN if inaccessible.'),
   ('TOKEN_WINDOW',f'Within the available memory, PDF page {page} begins near body token {local_start} and ends near body token {local_end}. Read that region and return the first substantive heading exactly. If you cannot read that region, answer UNKNOWN.'),
   ('MARKER_AND_OFFSET',f'The requested information is in the memory region bounded by [SIEMENS ORIGINAL PDF PAGE {page}] and [/SIEMENS ORIGINAL PDF PAGE {page}], approximately body-token offsets {local_start}:{local_end}. What is the first substantive section heading in that region? Output only the heading or UNKNOWN.')]
  t=time.perf_counter();cp,times=cart_load(bid);memory=list(initialize(cp));del cp;free_gpu()
  q['mount_timings']=times;q['probes']=[]
  for name,prompt in probes:
   t0=time.perf_counter();raw=answer(memory,prompt);exact=raw.strip().casefold()==q['gold'].casefold()
   q['probes'].append({'name':name,'prompt':prompt,'raw':raw,'exact':exact,'seconds':round(time.perf_counter()-t0,3)})
   emit('QA_PROBE',page,bid,name,'RAW',repr(raw),'EXACT',exact);persist()
  q['mount_and_probes_seconds']=round(time.perf_counter()-t,3)
  del memory;free_gpu();persist()
  # Control: neighboring wrong cartridge with the same marker+offset cue, never the gold text.
  wrong=chunks[(chunks.index(c)+1)%len(chunks)]['id'];cp,times=cart_load(wrong);memory=list(initialize(cp));del cp;free_gpu()
  raw=answer(memory,probes[-1][1]);q['wrong_cartridge']=wrong;q['wrong_cartridge_raw']=raw
  emit('QA_WRONG',page,wrong,repr(raw));del memory;free_gpu();persist()
 check('WEIGHT_SENTINEL_UNCHANGED',sentinel()==before)
 S['score_by_probe']={name:sum(bool(next((r['exact'] for r in q.get('probes',[]) if r['name']==name),False)) for q in S['questions']) for name in ('ORIGINAL','PAGE_MARKER','TOKEN_WINDOW','MARKER_AND_OFFSET')}
 S['status']='COMPLETE_POSITION_DIAGNOSTIC';emit('TEST712_STATUS',S['status'],'SCORES',S['score_by_probe'],'TOTAL_PAGES',len(pages),'TOTAL_TOKENS',total,'CARTS',len(chunks))
except Exception as e:
 S['status']='ERROR';S['error']=repr(e);S['traceback']=traceback.format_exc()[-15000:];emit('TEST712_ERROR',repr(e));emit(S['traceback'])
finally:
 persist();emit('RESULTS',RESULT);emit('LOG',LOG712)
