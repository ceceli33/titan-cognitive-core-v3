# AKBASCORE SILICON HIPPOCAMPUS — TEST731
# Single Colab cell / Python script. Runs exact public TEST730 first, then adds a separate
# experimental latent feedback path without modifying the downloaded reference source.
# NOT GPU-tested by the author. No PASS is asserted in advance.
import urllib.request, hashlib, ast, json, time, traceback, gc
from pathlib import Path
URL='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/730.py'
raw=urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'AKBASCORE-TEST731'}),timeout=120).read()
assert len(raw)>20000 and len(raw)<100000, 'Unexpected reference size'
ref_sha=hashlib.sha256(raw).hexdigest()
ref_ast=ast.parse(raw.decode('utf-8'))
required={'DirectCut3','forge_native','initialize_native','safe_load','to_gpu','memory_seals'}
found={n.name for n in ref_ast.body if isinstance(n,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef))}
assert required.issubset(found), f'Reference API changed: {required-found}'
print('TEST731_REFERENCE_730_SHA256',ref_sha,flush=True)
# Run the unchanged sealed reference. It constructs the physical MASTER and leaves
# model/tokenizer/CUT3 objects in this namespace on successful completion.
exec(compile(raw.decode('utf-8'),'730.py','exec'),globals())
assert R['status']=='DEMO_COMPLETED_UNGRADED','TEST730 did not complete'
import torch
from pathlib import Path
TEST731_DIR=Path('/content/AKBASCORE_TEST731' if Path('/content').exists() else '/tmp/AKBASCORE_TEST731')
TEST731_DIR.mkdir(parents=True,exist_ok=True)
REPORT=TEST731_DIR/'TEST731_results.json'
T={'test':'731','reference_sha256':ref_sha,'reference_status':R['status'],
   'goal':'Native latent feedback CUT3 feasibility; not yet autonomous reasoning',
   'model':MODEL_ID,'cut':CUT,'steps':[], 'status':'STARTED'}
def persist():
 tmp=REPORT.with_suffix('.tmp');tmp.write_text(json.dumps(T,indent=2,default=str));tmp.replace(REPORT)
def tensor_sha(x):
 return hashlib.sha256(x.detach().contiguous().to('cpu').view(torch.uint8).numpy().tobytes()).hexdigest()
def cosine(a,b):
 x=a.float().reshape(-1);y=b.float().reshape(-1)
 return float(torch.nn.functional.cosine_similarity(x[None],y[None]).item())
def metrics(a,b):
 return {'cosine':cosine(a,b),'relative_l2':float((a.float()-b.float()).norm().item()/(a.float().norm().item()+1e-12)),
         'finite':bool(torch.isfinite(b).all().item()),'input_sha256':tensor_sha(a),'output_sha256':tensor_sha(b)}
# Read the actual MASTER physical cartridge; no source document is inserted into prompts.
master_entry=next(e for e in ledger['cartridges'] if e['id']=='MASTER')
cp_cpu=safe_load(master_entry)
# Short tail of the actual H3 cartridge for a bounded feasibility experiment.
N=8
h0=cp_cpu['h'][:,-N:,:].to(DEV,dtype=DTYPE).contiguous()
assert h0.shape==(1,N,H)
# All interventions use a fresh empty cache; positional semantics are explicitly
# experimental and NOT equivalent to original physical MASTER initialization.
# Output hidden state from layer 79 is NOT naturally a CUT3 state; this experiment
# measures this mismatch rather than assuming valid semantic feedback.
@torch.no_grad()
def upper_pass(injected):
 pos=torch.arange(N,device=DEV)
 with DirectCut3(model.model.layers[CUT],'inject',source=injected) as bridge:
  bridge.offset=0
  out=model(inputs_embeds=torch.zeros((1,N,H),device=DEV,dtype=DTYPE),
            attention_mask=torch.ones((1,N),device=DEV,dtype=torch.long),
            position_ids=pos.unsqueeze(0),cache_position=pos,
            use_cache=False,output_hidden_states=True,return_dict=True)
  upper=out.hidden_states[-1].detach().clone()
  logits=out.logits[:,-1,:].detach().float()
 del out
 return upper,logits

def record(arm,iteration,x,y,logits,baseline_logits):
 m=metrics(x,y)
 m.update({'arm':arm,'iteration':iteration,
           'logit_relative_l2':float((logits-baseline_logits).norm().item()/(baseline_logits.norm().item()+1e-12)),
           'top_token_id':int(logits.argmax(dim=-1).item()),
           'top_token':tok.decode([int(logits.argmax(dim=-1).item())]),
           'output_norm':float(y.float().norm().item())})
 T['steps'].append(m);persist();print('TRACE',json.dumps(m,ensure_ascii=False),flush=True)
try:
 t0=time.perf_counter()
 base_upper,base_logits=upper_pass(h0)
 record('BASE',0,h0,base_upper,base_logits,base_logits)
 # Experimental raw recurrence: feed final hidden back into CUT3, with no token generation.
 # This is a feasibility arm, not a claim of a semantically valid bridge.
 raw_upper,raw_logits=upper_pass(base_upper)
 record('RAW_FEEDBACK',1,base_upper,raw_upper,raw_logits,base_logits)
 # Control: re-run same initial state. Must match BASE within numeric tolerance.
 replay_upper,replay_logits=upper_pass(h0)
 record('REPLAY',1,h0,replay_upper,replay_logits,base_logits)
 # Control: remove cross-position correspondence while retaining vector statistics.
 perm=torch.arange(N-1,-1,-1,device=DEV)
 shuffled_upper,shuffled_logits=upper_pass(base_upper[:,perm,:].contiguous())
 record('SHUFFLED_FEEDBACK',1,base_upper[:,perm,:],shuffled_upper,shuffled_logits,base_logits)
 # Control: use zero feedback with same shape/dtype.
 zero=torch.zeros_like(base_upper)
 zero_upper,zero_logits=upper_pass(zero)
 record('ZERO_FEEDBACK',1,zero,zero_upper,zero_logits,base_logits)
 T['checks']={
  'all_finite':all(s['finite'] for s in T['steps']),
  'replay_exact':torch.equal(base_upper,replay_upper) and torch.equal(base_logits,replay_logits),
  'feedback_changes_output':not torch.equal(base_logits,raw_logits),
  'feedback_differs_from_shuffled':not torch.equal(raw_logits,shuffled_logits),
  'feedback_differs_from_zero':not torch.equal(raw_logits,zero_logits),
  'frozen_weights':all(not p.requires_grad for p in model.parameters())}
 T['elapsed_seconds']=round(time.perf_counter()-t0,3)
 T['status']='FEASIBILITY_MEASURED' if T['checks']['all_finite'] else 'NUMERIC_FAILURE'
 T['interpretation']='Changed logits alone do not demonstrate reasoning, autonomous control, semantic preservation or improvement.'
 persist()
 print('TEST731_RESULT',json.dumps({'status':T['status'],'checks':T['checks'],'seconds':T['elapsed_seconds']},ensure_ascii=False),flush=True)
 print('TEST731_JSON',REPORT,flush=True)
except Exception as e:
 T['status']='ERROR';T['error']=repr(e);T['traceback']=traceback.format_exc();persist();raise
finally:
 for key in ['cp_cpu','h0','base_upper','raw_upper','replay_upper','shuffled_upper','zero_upper']:
  if key in globals():globals().pop(key)
 gc.collect();torch.cuda.empty_cache()
