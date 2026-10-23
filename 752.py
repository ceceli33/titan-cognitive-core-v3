# AKBASCORE SILICON HIPPOCAMPUS — TEST752 / COGNITIVE OS: RELATIONAL READ, VERIFICATION, MEMORY CONSOLIDATION
# Standalone single Colab cell. Frozen Qwen2.5-72B NF4 / A100 80GB / locked 709+730 CUT3 engine.
# No modifications to native motor. No claims of autonomous learning or success before execution.
# Corrected: DirectCut3 requires the 'types' module in imported-function globals.
import os,sys,subprocess,importlib.util,urllib.request,hashlib,ast,json,time,gc,random,traceback,re,types
from pathlib import Path
from datetime import datetime,timezone
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF','expandable_segments:True')
for mod,pkg in [('torch','torch'),('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50')]:
 if importlib.util.find_spec(mod) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',pkg])
import torch,transformers,bitsandbytes
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
ROOT=Path('/content/AKBASCORE_TEST752' if Path('/content').exists() else '/tmp/AKBASCORE_TEST752')
if (ROOT/'results.json').exists():raise RuntimeError('FAIL_CLOSED: existing TEST752 results; archive or rename the failed run folder before rerunning')
ROOT.mkdir(parents=True,exist_ok=True);CART=ROOT/'cartridges';CART.mkdir(exist_ok=True)
LOG=ROOT/'TEST752.log';LOG.write_text('');OUT=ROOT/'results.json'
MODEL_ID='Qwen/Qwen2.5-72B-Instruct';DTYPE=torch.bfloat16;DEV=torch.device('cuda:0');CUT=3;CHUNK=128;GPU_RESERVE_GIB=9.0
SRC709='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/709.py';SRC730='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/730.py'
LOCK709='6c9f8cbb1eeed848d45133d73f0d7676b68e9125';LOCK730='b1bad9eb3b111b44413f8ef05a3a140ab66a77dd'
SEED=752;N_CASES=8;MAX_NEW=12
R={'test':'752','status':'STARTED','model':MODEL_ID,'seed':SEED,'cases':[],'checks':[],
   'protocol':{'single_model_load':True,'native_engine':'unchanged 709+730 CUT3','case_count':N_CASES,
   'readout':'greedy native cache continuation, answer digits or UNKNOWN',
   'memory_scope':'Each multi-fact cartridge is forged from a combined source. Independent cartridge fusion is NOT claimed.',
   'independence':'Presealed test cases; no feedback injected into prompts; no gold answers given in test questions.',
   'limitations':['Synthetic relational data; not proof of real-world generalization',
   'No autonomous memory search, model-driven writing, or self-improvement',
   'Decision verification uses external ground truth and is not autonomous self-verification',
   'A wrong result must remain wrong; no answer-specific repair']}}
def log(*x):
 s=' '.join(map(str,x));print(s,flush=True)
 with LOG.open('a') as f:f.write(s+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def gitblob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def sha_file(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def save():
 tmp=OUT.with_suffix('.tmp');tmp.write_text(json.dumps(R,indent=2,ensure_ascii=False,default=str));tmp.replace(OUT)
def check(name,ok,detail=None):
 R['checks'].append({'name':name,'pass':bool(ok),'detail':detail});save();log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
 if not ok:raise RuntimeError('TEST752_'+name)
def fetch(url,limit):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST752/1.0'}),timeout=120) as f:b=f.read(limit+1)
 check('DOWNLOAD_LIMIT',len(b)<=limit,len(b));return b
def import_ast(raw,names,filename):
 tree=ast.parse(raw.decode());nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
 check('SYMBOLS_'+filename,{n.name for n in nodes}==set(names))
 exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),filename,'exec'),globals())
def release():gc.collect();torch.cuda.empty_cache()
try:
 check('CUDA',torch.cuda.is_available());check('ONE_GPU',torch.cuda.device_count()==1)
 check('A100_80GB','A100' in torch.cuda.get_device_name(0) and torch.cuda.get_device_properties(0).total_memory>=70*2**30)
 a=fetch(SRC709,500000);b=fetch(SRC730,500000)
 check('709_LOCK',gitblob(a)==LOCK709);check('730_LOCK',gitblob(b)==LOCK730)
 check('ENGINE_TYPES_DEPENDENCY',hasattr(types,'MethodType'))
 import_ast(a,{'pairs','cache_build','replace','half','rope','rephase','sentinel','free_gpu','ensure_room','kv_digest','full_kv_seal'},'709.py')
 import_ast(b,{'DirectCut3','forge_native','initialize_native','to_gpu','seal_cp'},'730.py')
 rng=random.Random(SEED);panel=[]
 # Explicitly synthetic, non-memorized relational facts; no gold answers in query.
 for i in range(N_CASES):
  a1=rng.randrange(11,48);b1=rng.randrange(4,19);c1=rng.randrange(3,14)
  tag=f'K{i:02d}X{rng.randrange(10000,99999)}'
  # Unique code labels, no model pretraining answer; two-hop arithmetic and contradictory updates.
  panel.append({'id':tag,'base':a1,'increment':b1,'discount':c1,'result':a1+b1-c1,
                'revision':a1+b1-c1+7,'source_texts':[
                  f'Record {tag}: starting units = {a1}.',
                  f'Record {tag}: added units = {b1}.',
                  f'Record {tag}: removed units = {c1}.']})
 R['panel_sha256']=sha(json.dumps(panel,sort_keys=True).encode());R['panel']=panel;save()
 tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
 PREFIX='<|im_start|>system\nYou are reading stored numerical records. Use only the stored records. Calculate the final units as starting plus added minus removed. If a required field is missing or contradictory values appear for the same field without an explicit authoritative correction, answer UNKNOWN. Reply with only one integer or UNKNOWN.\n<|im_end|>\n<|im_start|>user\nSTORED RECORDS:\n'
 PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
 quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
 model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
 for p in model.parameters():p.requires_grad_(False)
 cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
 check('ARCH',(NL,H,QH,KVH,HD)==(80,8192,64,8,128),(NL,H,QH,KVH,HD))
 check('FROZEN',all(not p.requires_grad for p in model.parameters()))
 check('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
 weight_before=sentinel()
 def save_cp(cp,name):
  path=CART/(name+'.pt');tmp=path.with_suffix('.tmp');torch.save(cp,tmp);tmp.replace(path)
  return {'file':path.name,'sha256':sha_file(path),'tensor_sha':seal_cp(cp)}
 def load_cp(meta):
  path=CART/meta['file'];check('FILE_SHA_'+path.stem,sha_file(path)==meta['sha256'])
  cp=torch.load(path,map_location='cpu',weights_only=True)
  check('TENSOR_SHA_'+path.stem,seal_cp(cp)==meta['tensor_sha']);return cp
 @torch.no_grad()
 def answer_native(cp,question):
  gpu=to_gpu(cp);mem=initialize_native(gpu);cache=cache_build(mem);n=cp['n']
  # Continue the existing frozen full-layer cache with an ordinary question; never put facts in the question.
  suffix=f'\nQUESTION: For record {question}, what are the final units?\nANSWER:'
  ids=tok(suffix,add_special_tokens=False).input_ids
  pos=torch.arange(n,n+len(ids),device=DEV)
  out=model(input_ids=torch.tensor([ids],device=DEV),past_key_values=cache,
   attention_mask=torch.ones((1,n+len(ids)),device=DEV,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
  cache=out.past_key_values;generated=[];logits=out.logits[:,-1,:]
  for step in range(MAX_NEW):
   nxt=int(logits.argmax(-1).item());generated.append(nxt)
   if nxt==tok.eos_token_id or nxt==tok.convert_tokens_to_ids('<|im_end|>'):break
   if step==MAX_NEW-1:break
   cp_pos=torch.tensor([n+len(ids)+step],device=DEV)
   out=model(input_ids=torch.tensor([[nxt]],device=DEV),past_key_values=cache,
    attention_mask=torch.ones((1,n+len(ids)+step+1),device=DEV,dtype=torch.long),
    position_ids=cp_pos.view(1,1),cache_position=cp_pos,use_cache=True,return_dict=True)
   cache=out.past_key_values;logits=out.logits[:,-1,:]
  result=tok.decode(generated,skip_special_tokens=True).strip()
  del out,cache,mem,gpu,logits;release();return result
 def normalize_answer(s):
  # Strict: do not award success for explanatory text containing a lucky number.
  s=s.strip();return s if re.fullmatch(r'-?\d+|UNKNOWN',s) else 'INVALID'
 arms=('COMPLETE','MISSING','CONFLICT','REVISED','SINGLE_FACT','NO_RECORD')
 for i,case in enumerate(panel):
  rec={'id':case['id'],'split':'CALIBRATION' if i<2 else 'HELD_OUT','arms':{},'status':'RUNNING'};R['cases'].append(rec);save()
  records=case['source_texts'];tag=case['id']
  variants={
   'COMPLETE':'\n'.join(records),
   'MISSING':'\n'.join(records[:2]),
   'CONFLICT':'\n'.join(records+[f'Record {tag}: removed units = {case["discount"]+7}.']),
   'REVISED':'\n'.join(records[:2]+[f'Record {tag}: removed units = {case["discount"]-7}.']),
   'SINGLE_FACT':records[0],
   'NO_RECORD':f'No records are available for {tag}.'}
  # CONFLICT has no stipulated authority. Correct response under test protocol is UNKNOWN.
  expected={'COMPLETE':str(case['result']),'MISSING':'UNKNOWN','CONFLICT':'UNKNOWN',
            'REVISED':str(case['revision']),'SINGLE_FACT':'UNKNOWN','NO_RECORD':'UNKNOWN'}
  for arm in arms:
   body=variants[arm]+'\n<|im_end|>\n<|im_start|>user\n'
   ids=tok(body,add_special_tokens=False).input_ids
   cp,forge_seconds=forge_native(ids,tag+'_'+arm)
   meta=save_cp(cp,tag+'_'+arm);del cp;release()
   reloaded=load_cp(meta);raw=answer_native(reloaded,tag);prediction=normalize_answer(raw)
   rec['arms'][arm]={'expected':expected[arm],'raw':raw,'prediction':prediction,'correct':prediction==expected[arm],
                     'cartridge':meta,'forge_seconds':forge_seconds,'body_sha256':sha(body.encode())}
   log('CASE_ARM',tag,arm,'EXPECTED',expected[arm],'PRED',repr(prediction),'CORRECT',prediction==expected[arm]);save()
   del reloaded;release()
  rec['status']='MEASURED';save()
 check('VALID_CASES',sum(x['status']=='MEASURED' for x in R['cases'])==N_CASES)
 check('HELD_OUT_CASES',sum(x['status']=='MEASURED' and x['split']=='HELD_OUT' for x in R['cases'])==N_CASES-2)
 check('WEIGHTS_UNCHANGED',sentinel()==weight_before)
 def summary(items):
  return {'n':len(items),'accuracy_by_arm':{arm:sum(x['arms'][arm]['correct'] for x in items)/len(items) for arm in arms},
          'complete_and_missing_both_correct':sum(x['arms']['COMPLETE']['correct'] and x['arms']['MISSING']['correct'] for x in items),
          'complete_and_revised_both_correct':sum(x['arms']['COMPLETE']['correct'] and x['arms']['REVISED']['correct'] for x in items)}
 R['summary']={'all':summary(R['cases']),'held_out':summary([x for x in R['cases'] if x['split']=='HELD_OUT'])}
 R['status']='COMPLETE_MEASURED';R['completed_utc']=datetime.now(timezone.utc).isoformat();save();log('TEST752 COMPLETE',json.dumps(R['summary'],indent=2),str(OUT))
except Exception as e:
 R['status']='FAILED';R['error']=repr(e);R['traceback']=traceback.format_exc();save();log('TEST752 FAILED',repr(e));raise
