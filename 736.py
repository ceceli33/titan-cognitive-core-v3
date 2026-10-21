# AKBASCORE SILICON HIPPOCAMPUS — TEST736
# TEMPORAL STACKING / ORIGINAL CUT3 PRESERVED / LATENT APPEND CAUSAL CONTROLS
# One Colab cell. Runs SHA-locked TEST730 unchanged. Static checks only; not GPU-tested by author.
# Hypothesis: appending a prior upper-layer state as a separate temporal segment
# might retain more task information than overwriting the original CUT3 state.
# IMPORTANT: upper-layer outputs are NOT calibrated CUT3 tokens; results are experimental.
import urllib.request,hashlib,ast,json,time,traceback,gc,random
from pathlib import Path
URL='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/730.py'
EXPECTED='c8dfa5bc7735ad2e00bd1b0141c7f0dc6af7cfb7232747e3bbf5b9a26f70dfaf'
raw=urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'AKBASCORE-TEST736'}),timeout=120).read()
sha=hashlib.sha256(raw).hexdigest();assert sha==EXPECTED,('REFERENCE_CHANGED',sha)
required={'DirectCut3','safe_load'}
found={x.name for x in ast.parse(raw.decode()).body if isinstance(x,(ast.ClassDef,ast.FunctionDef))}
assert required.issubset(found)
print('TEST736_REFERENCE_730_SHA256',sha,flush=True)
exec(compile(raw.decode(),'730.py','exec'),globals())
assert R['status']=='DEMO_COMPLETED_UNGRADED'
import torch
import torch.nn.functional as F
ROOT736=Path('/content/AKBASCORE_TEST736' if Path('/content').exists() else '/tmp/AKBASCORE_TEST736');ROOT736.mkdir(parents=True,exist_ok=True)
REPORT736=ROOT736/'TEST736_results.json';LOG736=ROOT736/'TEST736.log';LOG736.write_text('')
def say736(*args):
 s=' '.join(map(str,args));print(s,flush=True)
 with LOG736.open('a') as f:f.write(s+'\n')
def save736(o):
 tmp=REPORT736.with_suffix('.tmp');tmp.write_text(json.dumps(o,indent=2,ensure_ascii=False,default=str));tmp.replace(REPORT736)
def sha736(x):return hashlib.sha256(x.detach().contiguous().cpu().view(torch.uint8).numpy().tobytes()).hexdigest()
# Locked generative panel: multi-hop chains, distractors, reversal and varied labels.
# The seed, facts and answers are sealed before any model scoring. No answer-based filtering.
# Facts are supplied in the prompt; this tests latent recurrence, not SSD retrieval.
SEED736=7362026
rng736=random.Random(SEED736)
LOC736=['Arden','Boreal','Cobalt','Dorian','Eldrin','Fennel','Garnet','Helios','Indigo','Juniper','Kestrel','Linden','Marble','Nacre','Opal','Pinnacle','Quartz','Raven','Solace','Topaz','Umber','Vesper','Willow','Xenon','Yarrow','Zephyr','Aster','Brindle','Cedar','Dusk','Ember','Flint','Glade','Harbor','Ivory','Jasper','Krypton','Lagoon','Meadow','Nimbus','Orchid','Prairie','Ripple','Saffron','Thistle','Upland','Valley','Warden']
PANEL736=[]
for idx in range(32):
 # Four independent chains. Each has 3 to 6 edges. Distractors are structurally identical.
 hops=3+(idx%4);routes=[];used=set()
 for chain in range(4):
  nodes=[]
  for step in range(hops+1):
   # Generated names unique within the case, avoiding external knowledge.
   token=f'K{idx:02d}{chain}{step}{rng736.randrange(1000,9999)}'
   nodes.append(token)
  routes.append(nodes)
 facts=[]
 for nodes in routes:
  for step in range(hops):
   facts.append(f'{nodes[step]} forwards to {nodes[step+1]}.')
 rng736.shuffle(facts)
 target=(idx*3+1)%4;other=(target+1+idx%2)%4
 correct=routes[target][-1];wrong=routes[other][-1]
 # Balance answer letters exactly.
 gold='A' if idx%2==0 else 'B';a,b=(correct,wrong) if gold=='A' else (wrong,correct)
 PANEL736.append(dict(id=f'Q{idx:02d}',fact=' '.join(facts),
  question=f'Starting at {routes[target][0]}, follow exactly {hops} forwarding steps. What is the final node?',
  a=a,b=b,gold=gold,hops=hops))
panel_bytes=json.dumps(PANEL736,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode();panel_sha=hashlib.sha256(panel_bytes).hexdigest()
(ROOT736/'sealed_panel.json').write_bytes(panel_bytes)
T736={'test':'736','reference_sha256':sha,'panel_sha256':panel_sha,'status':'STARTED','cases':[],
 'panel_generation_seed':SEED736,'interpretation_limits':['Raw upper states are not native CUT3 states','Appending numerical vectors does not prove temporal reasoning','All facts supplied in prompt; no physical memory retrieval','32 generated cases are exploratory, not statistically decisive','Original question preserved; appended positions are experimental pseudo-tokens']}
save736(T736)
AID=tok(' A',add_special_tokens=False).input_ids;BID=tok(' B',add_special_tokens=False).input_ids
assert len(AID)==len(BID)==1 and AID!=BID,('LABEL_TOKENIZATION',AID,BID)
AID,BID=AID[0],BID[0]
assert 0<=AID<model.config.vocab_size and 0<=BID<model.config.vocab_size,('LABEL_ID_OUT_OF_RANGE',AID,BID)
say736('TEST736_PANEL_SHA256',panel_sha,'CASES',len(PANEL736),'LABEL_IDS',AID,BID)
@torch.no_grad()
def capture736(ids):
 n=ids.shape[1];pos=torch.arange(n,device=DEV);collector=[]
 with DirectCut3(model.model.layers[CUT],'capture',collector=collector):
  out=model.model(input_ids=ids,attention_mask=torch.ones_like(ids),position_ids=pos[None],cache_position=pos,use_cache=False,return_dict=True)
 h=torch.cat(collector,dim=1).to(DEV,dtype=DTYPE).contiguous()
 logits=model.lm_head(out.last_hidden_state[:,-1:,:]).detach().float()[:,-1,:]
 del out
 assert h.shape==(1,n,H),('CAPTURE_SHAPE',tuple(h.shape),(1,n,H))
 assert logits.shape==(1,model.config.vocab_size),('CAPTURE_LOGITS',tuple(logits.shape))
 return h,logits
@torch.no_grad()
def upper736(state):
 n=state.shape[1];pos=torch.arange(n,device=DEV)
 with DirectCut3(model.model.layers[CUT],'inject',source=state) as bridge:
  bridge.offset=0
  out=model.model(inputs_embeds=torch.zeros((1,n,H),device=DEV,dtype=DTYPE),
   attention_mask=torch.ones((1,n),device=DEV,dtype=torch.long),position_ids=pos[None],cache_position=pos,
   use_cache=False,return_dict=True)
 y=out.last_hidden_state.detach().clone()
 assert y.shape==(1,n,H),('UPPER_SHAPE',tuple(y.shape),(1,n,H))
 logits=model.lm_head(y[:,-1:,:]).detach().float()[:,-1,:]
 del out
 assert logits.shape==(1,model.config.vocab_size),('UPPER_LOGITS',tuple(logits.shape))
 return y,logits

def score736(logits,gold):
 assert logits.ndim==2 and logits.shape==(1,model.config.vocab_size),('BAD_LOGITS',tuple(logits.shape))
 ab=logits[0].index_select(0,torch.tensor([AID,BID],device=logits.device))
 m=float((ab[0]-ab[1]).item());pred='A' if m>0 else 'B' if m<0 else 'TIE'
 return dict(pred=pred,correct=pred==gold,gold_margin=m if gold=='A' else -m,
  p_gold=float(F.softmax(ab.float(),dim=0)[0 if gold=='A' else 1].item()),
  top_token_id=int(logits[0].argmax().item()))

def summarize736(arm):
 xs=[c['arms'][arm] for c in T736['cases']]
 return dict(correct=sum(int(x['correct']) for x in xs),total=len(xs),
  accuracy=sum(int(x['correct']) for x in xs)/len(xs),
  mean_gold_margin=sum(x['gold_margin'] for x in xs)/len(xs))
try:
 t0=time.perf_counter();before=sentinel();torch.manual_seed(736);random.seed(736)
 master=next(e for e in ledger['cartridges'] if e['id']=='MASTER');cp=safe_load(master);del cp
 T736['master_sha256']=master['sha256']
 for item in PANEL736:
  prompt=('Read the facts. Solve the question. Respond with only A or B.\nFacts: '+item['fact']+
          '\nQuestion: '+item['question']+'\nA: '+item['a']+'\nB: '+item['b']+'\nAnswer:')
  ids=torch.tensor([tok(prompt,add_special_tokens=False).input_ids],device=DEV)
  h,native=capture736(ids);first,base=upper736(h)
  parity=float((native-base).abs().max().item())
  assert torch.allclose(native,base,rtol=2e-3,atol=0.05),('PARITY',item['id'],parity)
  # F0 stays byte-for-byte unchanged in every stacked arm.
  # F1 is an appended, short, numerically scaled pseudo-token segment.
  # Scaling matches H3 RMS, but does NOT calibrate the representation semantics.
  K=8
  assert h.shape[1]>=K and first.shape==h.shape,('TEMPORAL_INPUT_SHAPE',tuple(h.shape),tuple(first.shape))
  tail=first[:,-K:,:].contiguous();orig_tail=h[:,-K:,:].contiguous()
  rms_h=h.float().square().mean().sqrt();rms_y=tail.float().square().mean().sqrt()
  scale=(rms_h/(rms_y+1e-12)).clamp(max=100).to(DTYPE)
  raw_tail=(tail*scale).contiguous()
  assert bool(torch.isfinite(raw_tail).all().item()),('NONFINITE_TEMPORAL_FRAME',item['id'])
  # Separate arms keep F0 identical and append equal numbers of pseudo-tokens.
  # Native-H3 self-tail is a positive structural reference, not a reasoning control.
  append={'TEMPORAL_RAW':raw_tail,
          'TEMPORAL_SHUFFLED':raw_tail.flip(1).contiguous(),
          'TEMPORAL_ZERO':torch.zeros_like(raw_tail),
          'TEMPORAL_NATIVE_H3':orig_tail}
  arms={'BASE':score736(base,item['gold'])};appended_sha={}
  for name,extra in append.items():
   assert extra.shape==(1,K,H),('APPEND_SHAPE',name,tuple(extra.shape))
   stacked=torch.cat([h,extra],dim=1)
   assert torch.equal(stacked[:,:h.shape[1],:],h),('F0_CHANGED',name,item['id'])
   _,lg=upper736(stacked)
   arms[name]=score736(lg,item['gold']);appended_sha[name]=sha736(extra)
   del stacked,lg
  # The 734 overwrite baseline is measured without modifying F0/other arms.
  _,overwrite=upper736(first)
  arms['RAW_OVERWRITE']=score736(overwrite,item['gold'])
  rec={'id':item['id'],'gold':item['gold'],'tokens':int(ids.shape[1]),'parity_max_abs':parity,
       'f0_sha256':sha736(h),'append_sha256':appended_sha,'scale':float(scale.item()),
       'h3_rms':float(rms_h.item()),'upper_rms':float(rms_y.item()),'arms':arms}
  T736['cases'].append(rec);save736(T736);say736('CASE736',json.dumps(rec,ensure_ascii=False))
  del ids,h,native,first,base,tail,orig_tail,raw_tail,overwrite,append
  if len(T736['cases'])%4==0:
   gc.collect()
   torch.cuda.empty_cache()
 assert hashlib.sha256((ROOT736/'sealed_panel.json').read_bytes()).hexdigest()==panel_sha
 names=['BASE','RAW_OVERWRITE','TEMPORAL_RAW','TEMPORAL_SHUFFLED','TEMPORAL_ZERO','TEMPORAL_NATIVE_H3']
 T736['summary']={name:summarize736(name) for name in names}
 s=T736['summary'];T736['checks']={'reference_complete':R['status']=='DEMO_COMPLETED_UNGRADED',
  'sealed_panel_unchanged':True,'master_integrity_verified':True,
  'f0_preserved':True,'native_replay_parity':True,'weights_frozen':all(not p.requires_grad for p in model.parameters()),
  'weight_sentinel_unchanged':sentinel()==before,
  'temporal_improves_over_base':s['TEMPORAL_RAW']['correct']>s['BASE']['correct'],
  'temporal_exceeds_both_controls':s['TEMPORAL_RAW']['correct']>max(s['TEMPORAL_SHUFFLED']['correct'],s['TEMPORAL_ZERO']['correct'])}
 # Paired transitions quantify correction AND regression; no post-hoc choice of a favorable subset.
 base_wrong=[c for c in T736['cases'] if not c['arms']['BASE']['correct']]
 base_right=[c for c in T736['cases'] if c['arms']['BASE']['correct']]
 T736['paired']={name:{'base_wrong_total':len(base_wrong),
  'wrong_to_right':sum(c['arms'][name]['correct'] for c in base_wrong),
  'right_to_wrong':sum(not c['arms'][name]['correct'] for c in base_right),
  'net_correct_change':s[name]['correct']-s['BASE']['correct']}
  for name in names if name!='BASE'}
 T736['checks']['raw_corrects_at_least_one_base_error']=T736['paired']['TEMPORAL_RAW']['wrong_to_right']>0
 T736['checks']['raw_net_improves']=T736['paired']['TEMPORAL_RAW']['net_correct_change']>0
 T736['checks']['raw_corrections_exceed_controls']=T736['paired']['TEMPORAL_RAW']['wrong_to_right']>max(T736['paired']['TEMPORAL_SHUFFLED']['wrong_to_right'],T736['paired']['TEMPORAL_ZERO']['wrong_to_right'])
 T736['status']='EXPLORATORY_CORRECTION_SIGNAL' if all(T736['checks'][k] for k in ('raw_corrects_at_least_one_base_error','raw_net_improves','raw_corrections_exceed_controls')) else 'NO_DEMONSTRATED_CORRECTION_GAIN'
 say736('TEST736_PAIRED',json.dumps(T736['paired'],ensure_ascii=False))
 T736['elapsed_seconds']=round(time.perf_counter()-t0,3);save736(T736)
 say736('TEST736_SUMMARY',json.dumps(T736['summary'],ensure_ascii=False))
 say736('TEST736_RESULT',json.dumps({'status':T736['status'],'checks':T736['checks'],'seconds':T736['elapsed_seconds']},ensure_ascii=False))
 say736('TEST736_JSON',REPORT736,'LOG',LOG736)
except Exception:
 T736['status']='ERROR';T736['traceback']=traceback.format_exc();save736(T736)
 say736('TEST736_ERROR',T736['traceback']);raise
finally:
 gc.collect()
 try:torch.cuda.synchronize();torch.cuda.empty_cache()
 except Exception as e:print('TEST736_CUDA_CLEANUP_SKIPPED',repr(e),flush=True)
