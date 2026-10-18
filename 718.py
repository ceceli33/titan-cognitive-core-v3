# AKBASCORE TEST718 — TEN PHYSICAL CUT3 CARTRIDGES / VANILLA CONTROLS / SEQUENTIAL SYNTHESIS
# Colab A100-80GB, standalone; untested on GPU. TEST709 engine functions and TEST716 forge setup remain unchanged.
# This is sequential physical readout + TEXT-mediated synthesis, NOT simultaneous 10-cartridge native inference.
import os,sys,ast,hashlib,urllib.request,json,time,gc,traceback
from pathlib import Path
import numpy as np
URL716='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/716.py';LOCK716='913fa7a4951f2072df4be2eb49120ea86efa5477'
local=Path('/content/716.py')
if local.is_file():source=local.read_bytes()
else:
 with urllib.request.urlopen(urllib.request.Request(URL716,headers={'User-Agent':'AKBASCORE-TEST718'}),timeout=180) as f:source=f.read(250000)
assert hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest()==LOCK716,'TEST716_SOURCE_DRIFT'
print('PASS TEST716_GIT_BLOB_LOCK',flush=True)
tree=ast.parse(source.decode());setup=next(n for n in tree.body if isinstance(n,ast.Try));stop=next(i for i,n in enumerate(setup.body) if isinstance(n,ast.Delete) and any(isinstance(t,ast.Name) and t.id=='pdf' for t in n.targets))
exec(compile(ast.fix_missing_locations(ast.Module(body=[n for n in tree.body if not isinstance(n,ast.Try)],type_ignores=[])),'716.py:preamble','exec'),globals())
ROOT=Path('/content/AKBASCORE_TEST714');OUT=ROOT/'TEST718_results.json';R718={'test':'718','status':'STARTED','source716_blob':LOCK716,'design':'SHA-locked 709 CUT3 engine; one physical cartridge at a time; vanilla and no-memory controls; text-mediated synthesis','results':[],'limitations':['No 2025-exclusive technical claims without independent 2024 comparison','Question headings are source-derived; not blind questions','Citations in generated answers require manual PDF checking','Ten cartridges are NOT jointly present in native model KV cache','Text-mediated synthesis is not native cross-cartridge relational memory','GPU execution not performed by author']}
def save718():
 OUT.parent.mkdir(parents=True,exist_ok=True);tmp=OUT.with_suffix('.tmp');tmp.write_text(json.dumps(R718,ensure_ascii=False,indent=2,default=str));tmp.replace(OUT)
def l718(*a):print(*a,flush=True)
try:
 # Execute original source checks, PDF parsing, model load, and cartridge forge/reuse without changing functions.
 exec(compile(ast.fix_missing_locations(ast.Module(body=setup.body[:stop+1],type_ignores=[])),'716.py:setup','exec'),globals())
 import torch
 # Guard: ten full caches would exceed practical 80GB GPU capacity. Use strictly one physical cartridge at a time.
 R718['pdf_sha256']=PDF_SHA;R718['model']=MODEL_ID;R718['cartridges']=[{'id':b['id'],'pages':b['page_range'],'body_tokens':b['body_tokens'],'sha256':b['cartridge_sha256']} for b in R['books']]
 R718['weight_sentinel_before']=before;R718['panel']=[{'cartridge':f'C{x[0]+1:02d}','pdf_page':x[1],'heading':x[3]} for x in panel];save718()
 # Deterministic source-grounded question per cartridge: first selected heading; no outcome-based cherry-picking.
 chosen={i:next(x for x in panel if x[0]==i) for i in range(10)}
 def question(x):
  return ('According to the July 2025 Siemens SINUMERIK ONE Universal Operating Manual (V6.25 SP1), explain the specific operating procedure, controls, or constraints described in the section titled "'+x[3]+'". Identify the section and PDF page if verifiable. Do not guess; if evidence is unavailable say UNKNOWN. Do not invent a citation.')
 def run_answer(memory,q,max_new=144):
  global MAX_NEW
  prev=MAX_NEW;MAX_NEW=max_new
  try:
   with torch.no_grad():return answer(memory,q)
  finally:MAX_NEW=prev;free_gpu()
 # Genuine vanilla answers: same weights, same question, no PDF, no cartridge, no external retrieval.
 for ci in range(10):
  x=chosen[ci];bid=f'C{ci+1:02d}';q=question(x)
  row={'id':bid,'pdf_page':x[1],'section_number':x[2],'heading':x[3],'question':q}
  row['vanilla']=run_answer(None,q);R718['results'].append(row);l718('VANILLA',bid,json.dumps(row['vanilla'],ensure_ascii=False));save718()
 # Physically reload each SHA-verified cartridge, rebuild upper KV with unchanged 709 initialize, answer, then fully release.
 for ci in range(10):
  bid=f'C{ci+1:02d}';row=R718['results'][ci];memory=None;cp=None
  try:
   cp,times=cart_load(bid);memory=list(initialize(cp));del cp;cp=None;free_gpu()
   row['physical_readout']=run_answer(memory,row['question']);row['timing']=times;row['cache_tokens']=int(memory[0][0].shape[-2]);l718('PHYSICAL',bid,json.dumps(row['physical_readout'],ensure_ascii=False));save718()
  finally:
   if cp is not None:del cp
   if memory is not None:del memory
   free_gpu()
 # No-cartridge ablation repeated AFTER physical trials to check memory isolation.
 for ci in (0,4,9):
  row=R718['results'][ci];row['post_release_no_memory']=run_answer(None,row['question']);l718('ABLATION',row['id'],json.dumps(row['post_release_no_memory'],ensure_ascii=False));save718()
 # Document the physical cartridge geometry without labels or model-generated interpretations.
 # This is a descriptive cosine map of mean sampled native H3 vectors, NOT a proof of semantic relationships.
 vectors=[]
 for ci in range(10):
  z=torch.load(CART/(f'C{ci+1:02d}.pt'),map_location='cpu',weights_only=True)
  h=z['h'][0,P:,:];ix=np.linspace(0,len(h)-1,min(64,len(h)),dtype=np.int64)
  v=h[torch.as_tensor(ix)].float().mean(0).numpy();v/=max(np.linalg.norm(v),1e-8);vectors.append(v);del z,h;gc.collect()
 mat=np.stack(vectors).astype(np.float32);sim=mat@mat.T
 R718['map']={'metric':'cosine of mean 64 evenly sampled H3 activations per cartridge','cartridges':[f'C{i+1:02d}' for i in range(10)],'similarity':sim.round(6).tolist(),'interpretation_limit':'not causal or validated semantic linkage'}
 np.savetxt(ROOT/'TEST718_cosine_map.csv',sim,delimiter=',',fmt='%.6f')
 try:
  import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
  fig,ax=plt.subplots(figsize=(8,7));im=ax.imshow(sim,vmin=-1,vmax=1,cmap='coolwarm');ax.set_xticks(range(10),[f'C{i+1:02d}' for i in range(10)]);ax.set_yticks(range(10),[f'C{i+1:02d}' for i in range(10)])
  ax.set_title('TEST718 — Physical CUT3 H3 cartridge similarity (descriptive)');fig.colorbar(im,ax=ax,label='Cosine similarity');fig.tight_layout();fig.savefig(ROOT/'TEST718_memory_map.png',dpi=180);plt.close(fig)
 except Exception as e:R718['map_render_error']=repr(e)
 save718()
 # Text-mediated synthesis: each piece of evidence is generated by physical cartridge readout.
 # The synthesis step has NO cartridge attached; explicitly report the intermediate text to prevent misleading claims.
 evidence='\n\n'.join(f'[{r["id"]}, PDF page {r["pdf_page"]}, heading {r["heading"]}]\n{r["physical_readout"]}' for r in R718['results'])
 synth=('The following are ten separately generated outputs from ten physical memory cartridges of the July 2025 Siemens SINUMERIK ONE Universal manual. They may contain errors. Synthesize ONLY what is supported by these excerpts. Compare operating workflows, dependencies, and differences across sections. Cite the cartridge IDs for each statement. Distinguish observed evidence from inference. Do not invent connections. If there is not enough evidence, say so.\n\n'+evidence+'\n\nProvide a concise technical synthesis with cross-cartridge links and uncertainty notes.')
 R718['synthesis_input']=synth;R718['synthesis_mode']='VANILLA_TEXT_ONLY_OVER_PRIOR_PHYSICAL_READOUTS';save718()
 R718['synthesis_output']=run_answer(None,synth,max_new=480);l718('SYNTHESIS',json.dumps(R718['synthesis_output'],ensure_ascii=False));save718()
 R718['weight_sentinel_after']=sentinel();assert R718['weight_sentinel_after']==before,'WEIGHTS_CHANGED'
 R718['status']='COMPLETE_SEQUENTIAL_PHYSICAL_READOUT_AND_TEXT_SYNTHESIS';save718()
 l718('PASS WEIGHTS_UNCHANGED');l718('TEST718_RESULT',json.dumps({'status':R718['status'],'physical_readouts':len(R718['results']),'synthesis_mode':R718['synthesis_mode'],'map_png':str(ROOT/'TEST718_memory_map.png'),'results_json':str(OUT)}))
except Exception as e:
 R718['status']='ERROR';R718['error']=repr(e);R718['traceback']=traceback.format_exc()[-12000:];save718();l718('TEST718_ERROR',R718['traceback']);raise
finally:save718()
