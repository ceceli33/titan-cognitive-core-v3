# AKBASCORE SILICON HIPPOCAMPUS — TEST735
# TEMPORAL STACKING / ORIGINAL CUT3 PRESERVED / LATENT APPEND CAUSAL CONTROLS
# One Colab cell. Runs SHA-locked TEST730 unchanged. Not GPU-tested by author.
# Hypothesis: appending a prior upper-layer state as a separate temporal segment
# might retain more task information than overwriting the original CUT3 state.
# IMPORTANT: upper-layer outputs are NOT calibrated CUT3 tokens; results are experimental.
import urllib.request,hashlib,ast,json,time,traceback,gc,random
from pathlib import Path
URL='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/730.py'
EXPECTED='c8dfa5bc7735ad2e00bd1b0141c7f0dc6af7cfb7232747e3bbf5b9a26f70dfaf'
raw=urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'AKBASCORE-TEST735'}),timeout=120).read()
sha=hashlib.sha256(raw).hexdigest();assert sha==EXPECTED,('REFERENCE_CHANGED',sha)
required={'DirectCut3','safe_load'}
found={x.name for x in ast.parse(raw.decode()).body if isinstance(x,(ast.ClassDef,ast.FunctionDef))}
assert required.issubset(found)
print('TEST735_REFERENCE_730_SHA256',sha,flush=True)
exec(compile(raw.decode(),'730.py','exec'),globals())
assert R['status']=='DEMO_COMPLETED_UNGRADED'
import torch
import torch.nn.functional as F
ROOT735=Path('/content/AKBASCORE_TEST735' if Path('/content').exists() else '/tmp/AKBASCORE_TEST735');ROOT735.mkdir(parents=True,exist_ok=True)
REPORT735=ROOT735/'TEST735_results.json';LOG735=ROOT735/'TEST735.log';LOG735.write_text('')
def say735(*args):
 s=' '.join(map(str,args));print(s,flush=True)
 with LOG735.open('a') as f:f.write(s+'\n')
def save735(o):
 tmp=REPORT735.with_suffix('.tmp');tmp.write_text(json.dumps(o,indent=2,ensure_ascii=False,default=str));tmp.replace(REPORT735)
def sha735(x):return hashlib.sha256(x.detach().contiguous().cpu().view(torch.uint8).numpy().tobytes()).hexdigest()
# Balanced two-hop cases. All facts are in the prompt: NOT an SSD retrieval benchmark.
# Question wording and gold labels fixed before model execution.
FACTS735=[
 ('Nera owns violet. Violet is stored in north. Varo owns copper. Copper is stored in west.','Where is the object owned by Nera stored?','north','west','A'),
 ('Nera owns violet. Violet is stored in north. Varo owns copper. Copper is stored in west.','Where is the object owned by Varo stored?','north','west','B'),
 ('Miro mentors Sela. Sela works in Cedar. Tavin mentors Ruma. Ruma works in Slate.','Where does the person mentored by Miro work?','Cedar','Slate','A'),
 ('Miro mentors Sela. Sela works in Cedar. Tavin mentors Ruma. Ruma works in Slate.','Where does the person mentored by Tavin work?','Cedar','Slate','B'),
 ('The blue key opens gate 4. Gate 4 leads to Iona. The silver key opens gate 9. Gate 9 leads to Pera.','Who is reached using the silver key?','Iona','Pera','B'),
 ('The blue key opens gate 4. Gate 4 leads to Iona. The silver key opens gate 9. Gate 9 leads to Pera.','Who is reached using the blue key?','Iona','Pera','A'),
 ('RQ-19 is in north archive. North archive is managed by Zeki. LN-28 is in west archive. West archive is managed by Daro.','Who manages the archive containing LN-28?','Zeki','Daro','B'),
 ('RQ-19 is in north archive. North archive is managed by Zeki. LN-28 is in west archive. West archive is managed by Daro.','Who manages the archive containing RQ-19?','Zeki','Daro','A'),
 ('The amber parcel belongs to Kira. Kira lives in Bayport. The green parcel belongs to Sora. Sora lives in Hillford.','Where does the owner of the amber parcel live?','Bayport','Hillford','A'),
 ('The amber parcel belongs to Kira. Kira lives in Bayport. The green parcel belongs to Sora. Sora lives in Hillford.','Where does the owner of the green parcel live?','Bayport','Hillford','B'),
 ('Orin wrote paper Delta. Paper Delta was filed by Leto. Mira wrote paper Gamma. Paper Gamma was filed by Vela.','Who filed the paper written by Mira?','Leto','Vela','B'),
 ('Orin wrote paper Delta. Paper Delta was filed by Leto. Mira wrote paper Gamma. Paper Gamma was filed by Vela.','Who filed the paper written by Orin?','Leto','Vela','A')]
PANEL735=[dict(id=f'Q{i:02d}',fact=f,question=q,a=a,b=b,gold=g) for i,(f,q,a,b,g) in enumerate(FACTS735)]
panel_bytes=json.dumps(PANEL735,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode();panel_sha=hashlib.sha256(panel_bytes).hexdigest()
(ROOT735/'sealed_panel.json').write_bytes(panel_bytes)
T735={'test':'735','reference_sha256':sha,'panel_sha256':panel_sha,'status':'STARTED','cases':[],
 'interpretation_limits':['Raw upper states are not native CUT3 states','Appending numerical vectors does not prove temporal reasoning','All facts supplied in prompt; no physical memory retrieval','12 cases are exploratory, not statistically decisive','Original question preserved; appended positions are experimental pseudo-tokens']}
save735(T735)
AID=tok(' A',add_special_tokens=False).input_ids;BID=tok(' B',add_special_tokens=False).input_ids
assert len(AID)==len(BID)==1 and AID!=BID
AID,BID=AID[0],BID[0]
say735('TEST735_PANEL_SHA256',panel_sha,'CASES',len(PANEL735),'LABEL_IDS',AID,BID)
@torch.no_grad()
def capture735(ids):
 n=ids.shape[1];pos=torch.arange(n,device=DEV);collector=[]
 with DirectCut3(model.model.layers[CUT],'capture',collector=collector):
  out=model.model(input_ids=ids,attention_mask=torch.ones_like(ids),position_ids=pos[None],cache_position=pos,use_cache=False,return_dict=True)
 h=torch.cat(collector,dim=1).to(DEV,dtype=DTYPE).contiguous()
 logits=model.lm_head(out.last_hidden_state[:,-1:,:]).detach().float()[:,-1,:]
 del out
 assert h.shape==(1,n,H)
 return h,logits
@torch.no_grad()
def upper735(state):
 n=state.shape[1];pos=torch.arange(n,device=DEV)
 with DirectCut3(model.model.layers[CUT],'inject',source=state) as bridge:
  bridge.offset=0
  out=model.model(inputs_embeds=torch.zeros((1,n,H),device=DEV,dtype=DTYPE),
   attention_mask=torch.ones((1,n),device=DEV,dtype=torch.long),position_ids=pos[None],cache_position=pos,
   use_cache=False,return_dict=True)
 y=out.last_hidden_state.detach().clone()
 logits=model.lm_head(y[:,-1:,:]).detach().float()[:,-1,:]
 del out
 return y,logits

def score735(logits,gold):
 assert logits.ndim==2 and logits.shape==(1,model.config.vocab_size),('BAD_LOGITS',tuple(logits.shape))
 ab=logits[0].index_select(0,torch.tensor([AID,BID],device=logits.device))
 m=float((ab[0]-ab[1]).item());pred='A' if m>0 else 'B' if m<0 else 'TIE'
 return dict(pred=pred,correct=pred==gold,gold_margin=m if gold=='A' else -m,
  p_gold=float(F.softmax(ab.float(),dim=0)[0 if gold=='A' else 1].item()),
  top_token_id=int(logits[0].argmax().item()))

def summarize735(arm):
 xs=[c['arms'][arm] for c in T735['cases']]
 return dict(correct=sum(int(x['correct']) for x in xs),total=len(xs),
  accuracy=sum(int(x['correct']) for x in xs)/len(xs),
  mean_gold_margin=sum(x['gold_margin'] for x in xs)/len(xs))
try:
 t0=time.perf_counter();before=sentinel();torch.manual_seed(735);random.seed(735)
 master=next(e for e in ledger['cartridges'] if e['id']=='MASTER');cp=safe_load(master);del cp
 T735['master_sha256']=master['sha256']
 for item in PANEL735:
  prompt=('Read the facts. Solve the question. Respond with only A or B.\nFacts: '+item['fact']+
          '\nQuestion: '+item['question']+'\nA: '+item['a']+'\nB: '+item['b']+'\nAnswer:')
  ids=torch.tensor([tok(prompt,add_special_tokens=False).input_ids],device=DEV)
  h,native=capture735(ids);first,base=upper735(h)
  parity=float((native-base).abs().max().item())
  assert torch.allclose(native,base,rtol=2e-3,atol=0.05),('PARITY',item['id'],parity)
  # F0 stays byte-for-byte unchanged in every stacked arm.
  # F1 is an appended, short, numerically scaled pseudo-token segment.
  # Scaling matches H3 RMS, but does NOT calibrate the representation semantics.
  K=8;tail=first[:,-K:,:].contiguous();orig_tail=h[:,-K:,:].contiguous()
  rms_h=h.float().square().mean().sqrt();rms_y=tail.float().square().mean().sqrt()
  scale=(rms_h/(rms_y+1e-12)).clamp(max=100).to(DTYPE)
  raw_tail=(tail*scale).contiguous()
  # Separate arms keep F0 identical and append equal numbers of pseudo-tokens.
  # Native-H3 self-tail is a positive structural reference, not a reasoning control.
  append={'TEMPORAL_RAW':raw_tail,
          'TEMPORAL_SHUFFLED':raw_tail.flip(1).contiguous(),
          'TEMPORAL_ZERO':torch.zeros_like(raw_tail),
          'TEMPORAL_NATIVE_H3':orig_tail}
  arms={'BASE':score735(base,item['gold'])};appended_sha={}
  for name,extra in append.items():
   stacked=torch.cat([h,extra],dim=1)
   assert torch.equal(stacked[:,:h.shape[1],:],h),('F0_CHANGED',name,item['id'])
   _,lg=upper735(stacked)
   arms[name]=score735(lg,item['gold']);appended_sha[name]=sha735(extra)
   del stacked,lg
  # The 734 overwrite baseline is measured without modifying F0/other arms.
  _,overwrite=upper735(first)
  arms['RAW_OVERWRITE']=score735(overwrite,item['gold'])
  rec={'id':item['id'],'gold':item['gold'],'tokens':int(ids.shape[1]),'parity_max_abs':parity,
       'f0_sha256':sha735(h),'append_sha256':appended_sha,'scale':float(scale.item()),
       'h3_rms':float(rms_h.item()),'upper_rms':float(rms_y.item()),'arms':arms}
  T735['cases'].append(rec);save735(T735);say735('CASE735',json.dumps(rec,ensure_ascii=False))
  del ids,h,native,first,base,tail,orig_tail,raw_tail,overwrite,append
  if len(T735['cases'])%4==0:gc.collect();torch.cuda.empty_cache()
 assert hashlib.sha256((ROOT735/'sealed_panel.json').read_bytes()).hexdigest()==panel_sha
 names=['BASE','RAW_OVERWRITE','TEMPORAL_RAW','TEMPORAL_SHUFFLED','TEMPORAL_ZERO','TEMPORAL_NATIVE_H3']
 T735['summary']={name:summarize735(name) for name in names}
 s=T735['summary'];T735['checks']={'reference_complete':R['status']=='DEMO_COMPLETED_UNGRADED',
  'sealed_panel_unchanged':True,'master_integrity_verified':True,
  'f0_preserved':True,'native_replay_parity':True,'weights_frozen':all(not p.requires_grad for p in model.parameters()),
  'weight_sentinel_unchanged':sentinel()==before,
  'temporal_improves_over_base':s['TEMPORAL_RAW']['correct']>s['BASE']['correct'],
  'temporal_exceeds_both_controls':s['TEMPORAL_RAW']['correct']>max(s['TEMPORAL_SHUFFLED']['correct'],s['TEMPORAL_ZERO']['correct'])}
 T735['status']='EXPLORATORY_GAIN_OBSERVED' if T735['checks']['temporal_improves_over_base'] and T735['checks']['temporal_exceeds_both_controls'] else 'NO_DEMONSTRATED_SEMANTIC_GAIN'
 T735['elapsed_seconds']=round(time.perf_counter()-t0,3);save735(T735)
 say735('TEST735_SUMMARY',json.dumps(T735['summary'],ensure_ascii=False))
 say735('TEST735_RESULT',json.dumps({'status':T735['status'],'checks':T735['checks'],'seconds':T735['elapsed_seconds']},ensure_ascii=False))
 say735('TEST735_JSON',REPORT735,'LOG',LOG735)
except Exception:
 T735['status']='ERROR';T735['traceback']=traceback.format_exc();save735(T735)
 say735('TEST735_ERROR',T735['traceback']);raise
finally:
 gc.collect()
 try:torch.cuda.synchronize();torch.cuda.empty_cache()
 except Exception as e:print('TEST735_CUDA_CLEANUP_SKIPPED',repr(e),flush=True)
