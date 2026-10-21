# AKBASCORE SILICON HIPPOCAMPUS — TEST734
# TEST734 repairs 2D [1,vocab] score indexing from TEST733; no change to panel or CUT3.
# Sealed binary-answer semantic probe for native CUT3 recurrence, based on locked TEST730/TEST732.
# One Colab cell; no GPU execution claimed by author. TEST730 source and engine unchanged.
import urllib.request, hashlib, ast, json, time, traceback, gc, random
from pathlib import Path
URL='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/730.py'
raw=urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'AKBASCORE-TEST734'}),timeout=120).read()
ref_sha=hashlib.sha256(raw).hexdigest()
EXPECTED_SHA='c8dfa5bc7735ad2e00bd1b0141c7f0dc6af7cfb7232747e3bbf5b9a26f70dfaf'
assert ref_sha==EXPECTED_SHA, f'TEST730 changed: {ref_sha}'
required={'DirectCut3','forge_native','initialize_native','safe_load','to_gpu'}
found={n.name for n in ast.parse(raw.decode()).body if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
assert required.issubset(found),f'Missing reference API: {required-found}'
print('TEST734_REFERENCE_730_SHA256',ref_sha,flush=True)
# Identical working reference. Builds and verifies MASTER and loads frozen 72B model.
exec(compile(raw.decode(),'730.py','exec'),globals())
assert R['status']=='DEMO_COMPLETED_UNGRADED'
import torch
import torch.nn.functional as F
ROOT733=Path('/content/AKBASCORE_TEST734' if Path('/content').exists() else '/tmp/AKBASCORE_TEST734')
ROOT733.mkdir(parents=True,exist_ok=True)
REPORT733=ROOT733/'TEST734_results.json'
LOG733=ROOT733/'TEST734.log'
LOG733.write_text('')
def say733(*args):
 s=' '.join(map(str,args));print(s,flush=True)
 with LOG733.open('a') as f:f.write(s+'\n')
def atomic733(obj):
 p=REPORT733.with_suffix('.tmp');p.write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str));p.replace(REPORT733)
def tsha733(t):return hashlib.sha256(t.detach().contiguous().cpu().view(torch.uint8).numpy().tobytes()).hexdigest()
# A sealed panel: new invented facts; all evidence supplied in each prompt. No external answer lookup.
# Reversing labels prevents constant-A or constant-B strategies from passing.
FACTS733=[
 ('The violet lantern belongs to Nera. The copper lantern belongs to Varo.','Who owns the violet lantern?','Nera','Varo','A'),
 ('The violet lantern belongs to Nera. The copper lantern belongs to Varo.','Who owns the copper lantern?','Nera','Varo','B'),
 ('Miro filed the blue report. Sela filed the amber report.','Who filed the amber report?','Miro','Sela','B'),
 ('Miro filed the blue report. Sela filed the amber report.','Who filed the blue report?','Miro','Sela','A'),
 ('Tavin works at Cedar Lab. Ruma works at Slate Lab.','Where does Tavin work?','Cedar Lab','Slate Lab','A'),
 ('Tavin works at Cedar Lab. Ruma works at Slate Lab.','Where does Ruma work?','Cedar Lab','Slate Lab','B'),
 ('The orchid key opens Gate 4. The silver key opens Gate 9.','Which gate does the silver key open?','Gate 4','Gate 9','B'),
 ('The orchid key opens Gate 4. The silver key opens Gate 9.','Which gate does the orchid key open?','Gate 4','Gate 9','A'),
 ('Iona mentors Pera. Pera mentors Zeki.','Who mentors Zeki?','Iona','Pera','B'),
 ('Iona mentors Pera. Pera mentors Zeki.','Who mentors Pera?','Iona','Pera','A'),
 ('The north archive stores token RQ-19. The west archive stores token LN-28.','Where is token RQ-19 stored?','north archive','west archive','A'),
 ('The north archive stores token RQ-19. The west archive stores token LN-28.','Where is token LN-28 stored?','north archive','west archive','B'),
]
PANEL733=[{'id':f'Q{i:02d}','fact':f,'question':q,'option_a':a,'option_b':b,'gold':g} for i,(f,q,a,b,g) in enumerate(FACTS733)]
PANEL_BYTES=json.dumps(PANEL733,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
PANEL_SHA733=hashlib.sha256(PANEL_BYTES).hexdigest()
(ROOT733/'sealed_panel.json').write_bytes(PANEL_BYTES)
T733={'test':'734','reference_730_sha256':ref_sha,'panel_sha256':PANEL_SHA733,'status':'STARTED',
 'hypothesis':'Does raw native latent recurrence improve binary fact selection relative to no-feedback and matched controls?',
 'method':'Prompt H3 capture; replay parity; 1/2/3 raw recurrences; position shuffle and zero controls; teacher-forced A/B next-token scoring',
 'limitations':['Prompt facts are explicitly visible; this is NOT a MASTER memory-retrieval test',
 'The last normalized hidden state is not a calibrated CUT3 representation',
 'No learned bridge or autonomous stopping controller',
 'Improvement requires accuracy/margin gains over controls, not mere logit changes'],
 'cases':[], 'checks':{}}
atomic733(T733)
# A/B token scoring must be unambiguous; choose tokenizer-specific single tokens for suffixes.
a_ids=tok(' A',add_special_tokens=False).input_ids
b_ids=tok(' B',add_special_tokens=False).input_ids
assert len(a_ids)==len(b_ids)==1 and a_ids[0]!=b_ids[0],('BAD_LABEL_TOKENIZATION',a_ids,b_ids)
AID,BID=a_ids[0],b_ids[0]
say733('TEST734_PANEL_SHA256',PANEL_SHA733,'CASES',len(PANEL733),'LABEL_IDS',AID,BID)
# Keep the full question at the same positions in each arm. No extra tokens/compute for controls.
# Capture H3 from the actual model forward, then compare against a native H3 replay.
@torch.no_grad()
def capture733(ids):
 collector=[];n=ids.shape[1];pos=torch.arange(n,device=DEV)
 with DirectCut3(model.model.layers[CUT],'capture',collector=collector):
  out=model.model(input_ids=ids,attention_mask=torch.ones_like(ids),position_ids=pos.unsqueeze(0),
                  cache_position=pos,use_cache=False,return_dict=True)
 h3=torch.cat(collector,dim=1).to(DEV,dtype=DTYPE)
 logits=model.lm_head(out.last_hidden_state[:,-1:,:]).detach().float()[:,-1,:]
 del out
 return h3,logits
@torch.no_grad()
def upper733(h3):
 n=h3.shape[1];pos=torch.arange(n,device=DEV)
 with DirectCut3(model.model.layers[CUT],'inject',source=h3) as bridge:
  bridge.offset=0
  out=model.model(inputs_embeds=torch.zeros((1,n,H),device=DEV,dtype=DTYPE),
      attention_mask=torch.ones((1,n),device=DEV,dtype=torch.long),
      position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=False,return_dict=True)
 upper=out.last_hidden_state.detach().clone()
 logits=model.lm_head(upper[:,-1:,:]).detach().float()[:,-1,:]
 del out
 return upper,logits

def score733(logits,gold):
 assert logits.ndim==2 and logits.shape[0]==1 and logits.shape[1]==model.config.vocab_size, ('LOGIT_SHAPE',tuple(logits.shape))
 ab=logits[0].index_select(0,torch.tensor([AID,BID],device=logits.device,dtype=torch.long))
 margin=float((ab[0]-ab[1]).item())
 pred='A' if margin>0 else 'B'
 return {'pred':pred,'correct':pred==gold,'margin_a_minus_b':margin,
         'gold_margin':margin if gold=='A' else -margin,
         'ab_probability':float(F.softmax(ab.float(),dim=0)[0].item()),
         'top_token_id':int(logits[0].argmax().item())}

def summary733(cases,arm):
 xs=[c['arms'][arm] for c in cases]
 return {'correct':sum(x['correct'] for x in xs),'total':len(xs),
         'accuracy':sum(x['correct'] for x in xs)/len(xs),
         'mean_gold_margin':sum(x['gold_margin'] for x in xs)/len(xs)}

try:
 t0=time.perf_counter();random.seed(733);torch.manual_seed(733)
 before733=sentinel()
 # Assert MASTER remains a real, sealed physical cartridge, even though panel facts are separate.
 master733=next(e for e in ledger['cartridges'] if e['id']=='MASTER')
 cp733=safe_load(master733)
 T733['master_cartridge_sha256']=master733['sha256'];del cp733
 for item in PANEL733:
  # Trailing space ensures the next token is A or B, with one-token label IDs.
  prompt=('Read the facts and answer using only A or B.\nFacts: '+item['fact']+'\nQuestion: '+item['question']+
          '\nA: '+item['option_a']+'\nB: '+item['option_b']+'\nAnswer:')
  # Because label tokens include leading spaces, prompt ends at colon.
  ids=torch.tensor([tok(prompt,add_special_tokens=False).input_ids],device=DEV)
  h3,native_logits=capture733(ids)
  base_upper,base_logits=upper733(h3)
  # BF16 native replay must agree with actual forward to within tolerance; fail closed.
  parity=float((native_logits-base_logits).abs().max().item())
  assert torch.allclose(native_logits,base_logits,rtol=2e-3,atol=0.05),('H3_REPLAY_PARITY',item['id'],parity)
  replay_upper,replay_logits=upper733(h3)
  assert torch.equal(base_logits,replay_logits),('NONDETERMINISTIC_REPLAY',item['id'])
  raw1,log1=upper733(base_upper)
  raw2,log2=upper733(raw1)
  raw3,log3=upper733(raw2)
  shuffled,shuf_logits=upper733(base_upper.flip(1).contiguous())
  zero,zero_logits=upper733(torch.zeros_like(base_upper))
  arms={'BASE':base_logits,'RAW1':log1,'RAW2':log2,'RAW3':log3,
        'SHUFFLED':shuf_logits,'ZERO':zero_logits}
  rec={'id':item['id'],'gold':item['gold'],'tokens':int(ids.shape[1]),
       'h3_sha256':tsha733(h3),'parity_max_abs':parity,
       'arms':{k:score733(v,item['gold']) for k,v in arms.items()},
       'state_cosine':float(F.cosine_similarity(h3.float().flatten()[None],base_upper.float().flatten()[None]).item())}
  T733['cases'].append(rec);atomic733(T733)
  say733('CASE733',json.dumps(rec,ensure_ascii=False))
  del ids,h3,native_logits,base_upper,base_logits,replay_upper,replay_logits,raw1,raw2,raw3,shuffled,zero
  if len(T733['cases'])%4==0:gc.collect();torch.cuda.empty_cache()
 assert hashlib.sha256((ROOT733/'sealed_panel.json').read_bytes()).hexdigest()==PANEL_SHA733
 T733['summary']={k:summary733(T733['cases'],k) for k in ('BASE','RAW1','RAW2','RAW3','SHUFFLED','ZERO')}
 s=T733['summary'];baseline=s['BASE']['correct'];best=max(s[k]['correct'] for k in ('RAW1','RAW2','RAW3'))
 controls=max(s[k]['correct'] for k in ('SHUFFLED','ZERO'))
 T733['checks']={'reference_complete':R['status']=='DEMO_COMPLETED_UNGRADED',
                 'sealed_panel_unchanged':True,
                 'master_integrity_verified':True,
                 'native_replay_parity':True,
                 'weights_frozen':all(not p.requires_grad for p in model.parameters()),
                 'weight_sentinel_unchanged':sentinel()==before733,
                 'raw_improves_over_base':best>baseline,
                 'raw_exceeds_controls':best>controls}
 T733['status']='SEMANTIC_GAIN_OBSERVED' if all(T733['checks'].values()) else 'NO_DEMONSTRATED_SEMANTIC_GAIN'
 T733['elapsed_seconds']=round(time.perf_counter()-t0,3)
 atomic733(T733)
 say733('TEST734_SUMMARY',json.dumps(T733['summary'],ensure_ascii=False))
 say733('TEST734_RESULT',json.dumps({'status':T733['status'],'checks':T733['checks'],'seconds':T733['elapsed_seconds']},ensure_ascii=False))
 say733('TEST734_JSON',REPORT733,'LOG',LOG733)
except Exception as e:
 T733['status']='ERROR';T733['error']=repr(e);T733['traceback']=traceback.format_exc();atomic733(T733)
 say733('TEST734_ERROR',traceback.format_exc());raise
finally:
 gc.collect()
 try:
  torch.cuda.synchronize()
  torch.cuda.empty_cache()
 except Exception as cleanup_error:
  print('TEST734_CUDA_CLEANUP_SKIPPED',repr(cleanup_error),flush=True)
