# AKBASCORE TEST717 — FULL 80-LAYER NATIVE ACTIVATION XRAY / HELD-OUT ROUTING
# Copyright (c) 2026 Mustafa Akbas. Inherits project license from v3 repository.
# Standalone Colab A100-80GB. GPU execution NOT performed by author.
# Reuses SHA-locked TEST716 setup and TEST709 CUT3 engine, with no changes to model weights or CUT3 functions.
# Full-layer bank is diagnostic; not a replacement for physical CUT3 cartridges.
import os,sys,ast,hashlib,urllib.request,json,time,gc,traceback
from pathlib import Path
import numpy as np
URL716='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/716.py'
LOCK716='913fa7a4951f2072df4be2eb49120ea86efa5477'
LOCAL716=Path('/content/716.py')
if LOCAL716.is_file():src=LOCAL716.read_bytes()
else:
 with urllib.request.urlopen(urllib.request.Request(URL716,headers={'User-Agent':'AKBASCORE-TEST717'}),timeout=180) as f:src=f.read(250000)
assert hashlib.sha1(b'blob '+str(len(src)).encode()+b'\0'+src).hexdigest()==LOCK716,'TEST716_GIT_BLOB_MISMATCH'
print('PASS TEST716_GIT_BLOB_LOCK',flush=True)
tree=ast.parse(src.decode('utf-8'))
# Execute unchanged 716 preamble and source preparation / cartridge creation, stopping before its routing-bank stage.
setup=next(n for n in tree.body if isinstance(n,ast.Try))
stop=next(i for i,n in enumerate(setup.body) if isinstance(n,ast.Delete) and any(isinstance(t,ast.Name) and t.id=='pdf' for t in n.targets))
pre=[n for n in tree.body if not isinstance(n,ast.Try)]
# Last 716 top-level node is its main try; the preamble includes imports, constants, and SHA-locked 709 AST functions.
exec(compile(ast.fix_missing_locations(ast.Module(body=pre,type_ignores=[])),'716.py','exec'),globals())
R={'test':'717','status':'STARTED','source716_blob':LOCK716,'mode':'FULL_LAYER_XRAY','layers':80,'bank_samples_per_cartridge':64,'calibration_heading_per_cartridge':3,'holdout_heading_per_cartridge':3,'limits':['No GPU execution by code author','60 source-derived headings; holdout is disjoint headings, not independent PDF','Question includes heading text; not hidden-fact QA','Layer chosen only on calibration, not holdout','No guarantee of 100% accuracy','Xray pass is separate from existing physical CUT3 forge']}
OUT=Path('/content/AKBASCORE_TEST714/TEST717_results.json');OUT.parent.mkdir(parents=True,exist_ok=True)
def save717():
 tmp=OUT.with_suffix('.tmp');tmp.write_text(json.dumps(R,indent=2,ensure_ascii=False,default=str));tmp.replace(OUT)
def log717(*args):print(*args,flush=True)
try:
 # Run exact 716 source checks, PDF panel selection, model load and physical CUT3 cartridge forge.
 exec(compile(ast.fix_missing_locations(ast.Module(body=setup.body[:stop+1],type_ignores=[])),'716.py:setup','exec'),globals())
 import torch
 # The 716 setup releases the source; reconstruct identical token bodies from the verified PDF.
 pdf2=fetch(PDF_URL,15000000);assert sha(pdf2)==PDF_SHA
 doc2=fitz.open(stream=pdf2,filetype='pdf')
 P717=64;L717=NL;XDIR=ROOT/'xray717';XDIR.mkdir(exist_ok=True)
 # Memory: 80 layers x 64 positions x 8192 BF16 = 80 MiB per cartridge.
 # Store layerwise sampled activations; do not collect full hidden sequences.
 @torch.no_grad()
 def xray_cartridge(ci):
  bid=f'C{ci+1:02d}';path=XDIR/(bid+'.pt');seal=XDIR/(bid+'.sha256')
  if path.exists() and seal.exists() and sha(path.read_bytes())==seal.read_text().strip():
   z=torch.load(path,map_location='cpu',weights_only=True)
   if z['source_sha']==PDF_SHA and z['layers'].shape==(NL,P717,H) and z['body_tokens']==R['books'][ci]['body_tokens']:
    log717('XRAY_REUSE_SHA',bid);return
  a,b=bounds[ci];s=''.join(f'\n[PDF PAGE {p}]\n'+doc2[p-1].get_text(sort=True) for p in range(a,b+1))
  body=tok(s,add_special_tokens=False).input_ids;ids=PIDS+body;n=len(ids)
  assert len(body)==R['books'][ci]['body_tokens'],'TOKEN_DRIFT_'+bid
  sample=np.linspace(P,n-1,P717,dtype=np.int64);by_layer=[[] for _ in range(NL)];cache=None;hooks=[];offset=[0]
  def make_hook(li):
   def hook(mod,args,out):
    h=out[0] if isinstance(out,(tuple,list)) else out;st=offset[0];mask=(sample>=st)&(sample<st+h.shape[1]);idx=sample[mask]-st
    if len(idx):by_layer[li].append((np.flatnonzero(mask),h[0,torch.as_tensor(idx,device=h.device)].detach().to('cpu',dtype=torch.bfloat16)))
   return hook
  hooks=[model.model.layers[i].register_forward_hook(make_hook(i)) for i in range(NL)]
  try:
   for st in range(0,n,CHUNK):
    piece=ids[st:st+CHUNK];ensure_room(len(piece)+512);offset[0]=st
    pos=torch.arange(st,st+len(piece),device=DEV)
    out=model(input_ids=torch.tensor([piece],device=DEV),past_key_values=cache,attention_mask=torch.ones((1,st+len(piece)),device=DEV,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
    cache=out.past_key_values;del out
    if st==0 or (st//CHUNK+1)%32==0:log717('XRAY_PROGRESS',bid,st+len(piece),'/',n)
  finally:
   for h in hooks:h.remove()
   del cache;free_gpu()
  layers=torch.empty((NL,P717,H),dtype=torch.bfloat16)
  for li,parts in enumerate(by_layer):
   seen=np.zeros(P717,dtype=bool)
   for indexes,v in parts:
    assert not seen[indexes].any(),'SAMPLE_DUPLICATE';layers[li,torch.as_tensor(indexes)]=v;seen[indexes]=True
   assert seen.all(),f'SAMPLE_MISSING_L{li}'
  record={'layers':layers,'source_sha':PDF_SHA,'body_tokens':len(body),'sample_positions':torch.as_tensor(sample),'cartridge':bid,'model':MODEL_ID}
  torch.save(record,path);seal.write_text(sha(path.read_bytes()));log717('XRAY_SAVED',bid,path.stat().st_size)
  del layers,record,body,ids;gc.collect()
 for ci in range(10):xray_cartridge(ci)
 del pdf2,doc2;gc.collect()
 # CPU normalized bank: 10 x 80 x 64 x 8192 float16 (~800MiB). Keep CPU only.
 BANK=[]
 for ci in range(10):
  z=torch.load(XDIR/(f'C{ci+1:02d}.pt'),map_location='cpu',weights_only=True)['layers']
  y=z.float().numpy();y/=np.maximum(np.linalg.norm(y,axis=-1,keepdims=True),1e-8)
  BANK.append(y.astype(np.float16));del z,y
 log717('XRAY_BANK_READY',len(BANK),'layers',NL,'samples',P717)
 # Split by heading identity, not by query variant. First three headings/cartridge are calibration,
 # remaining three are holdout. The split is fixed before any layer score is inspected.
 assert len(panel)==60 and all(sum(x[0]==i for x in panel)==6 for i in range(10)),'PANEL_SPLIT_UNEXPECTED'
 groups={i:[j for j,x in enumerate(panel) if x[0]==i] for i in range(10)}
 cal=set(j for i in range(10) for j in groups[i][:3]);held=set(range(60))-cal
 R['split']={'calibration_headings':sorted(cal),'holdout_headings':sorted(held),'calibration_queries':60,'holdout_queries':60}
 save717()
 @torch.no_grad()
 def query_xray(question):
  s='<|im_start|>user\n'+question+'\n<|im_end|>\n<|im_start|>assistant\n'
  ids=tok(s,add_special_tokens=False).input_ids;buf=[None]*NL
  def mk(li):
   def fn(mod,args,out):
    v=out[0] if isinstance(out,(tuple,list)) else out
    # Same question-token position pooling for every layer; no gold labels.
    buf[li]=v[0].detach().float().cpu().numpy()
   return fn
  hooks=[model.model.layers[i].register_forward_hook(mk(i)) for i in range(NL)]
  try:
   out=model(input_ids=torch.tensor([ids],device=DEV),use_cache=False,return_dict=True);del out
  finally:
   for h in hooks:h.remove()
  return buf
 def score_layer(q,b):
  q=q/np.maximum(np.linalg.norm(q,axis=1,keepdims=True),1e-8)
  sim=q@b.astype(np.float32).T
  return float(np.partition(sim,-2,axis=1)[:,-2:].mean(axis=1).mean())
 # Xray every layer with the TEST715 TOP2 definition; also save last-token-only diagnostic.
 rows=[]
 for j,(question,gold,variant) in enumerate(QUESTIONS):
  qlayers=query_xray(question);all_scores=np.empty((NL,10),dtype=np.float32);last_scores=np.empty((NL,10),dtype=np.float32)
  for li in range(NL):
   q=qlayers[li];qn=q/np.maximum(np.linalg.norm(q,axis=1,keepdims=True),1e-8)
   for ci in range(10):
    b=BANK[ci][li].astype(np.float32);sim=qn@b.T
    all_scores[li,ci]=np.partition(sim,-2,axis=1)[:,-2:].mean(axis=1).mean()
    last_scores[li,ci]=np.partition(sim[-1],-2)[-2:].mean()
  rows.append({'case':j,'heading_index':j//2,'split':'CAL' if j//2 in cal else 'HOLDOUT','variant':variant,'gold':gold,'question':question,'scores':all_scores.tolist(),'last_scores':last_scores.tolist()})
  if j%10==0:log717('XRAY_QUERY_PROGRESS',j+1,'/',len(QUESTIONS))
  R['processed_queries']=j+1;save717()
 def eval_layer(li,subset,key='scores'):
  ranks=[]
  for row in rows:
   if row['split']!=subset:continue
   sc=row[key][li];order=sorted(range(10),key=lambda i:(-sc[i],i));ranks.append(order.index(row['gold'])+1)
  return {'r1':sum(x==1 for x in ranks),'r5':sum(x<=5 for x in ranks),'n':len(ranks),'mrr':round(float(np.mean([1/x for x in ranks])),6)}
 # Selection based on calibration only; holdout metrics not consulted during selection.
 calstats=[eval_layer(i,'CAL') for i in range(NL)]
 chosen=max(range(NL),key=lambda i:(calstats[i]['r1'],calstats[i]['mrr'],-i))
 R['selected_layer']=chosen;R['selection_rule']='max CAL R@1, tie CAL MRR, tie shallowest layer'
 R['layer_calibration']=calstats
 R['locked_baseline_cut3']={'calibration':eval_layer(CUT,'CAL'),'holdout':eval_layer(CUT,'HOLDOUT')}
 R['selected_layer_results']={'calibration':eval_layer(chosen,'CAL'),'holdout':eval_layer(chosen,'HOLDOUT')}
 R['all_layer_holdout_diagnostic']=[eval_layer(i,'HOLDOUT') for i in range(NL)]
 R['last_token_diagnostic']={'selected_layer_holdout':eval_layer(chosen,'HOLDOUT','last_scores'),'cut3_holdout':eval_layer(CUT,'HOLDOUT','last_scores')}
 R['holdout_routes']=[{'case':r['case'],'heading_index':r['heading_index'],'gold':f'C{r["gold"]+1:02d}','selected':f'C{int(np.argmax(r["scores"][chosen]))+1:02d}','gold_rank':sorted(range(10),key=lambda i:(-r['scores'][chosen][i],i)).index(r['gold'])+1} for r in rows if r['split']=='HOLDOUT']
 R['weight_sentinel_after']=sentinel();assert R['weight_sentinel_after']==before,'WEIGHTS_CHANGED'
 R['status']='COMPLETE_XRAY_HELDOUT';save717()
 log717('PASS WEIGHTS_UNCHANGED');log717('TEST717_RESULT',json.dumps({'selected_layer':chosen,'cut3':R['locked_baseline_cut3'],'selected':R['selected_layer_results'],'status':R['status']}))
except Exception as e:
 R['status']='ERROR';R['error']=repr(e);R['traceback']=traceback.format_exc()[-12000:];save717();log717('TEST717_ERROR',R['traceback']);raise
finally:save717()
