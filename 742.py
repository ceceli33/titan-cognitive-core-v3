# AKBASCORE SILICON HIPPOCAMPUS — TEST742
# Cross-source relational transfer: hierarchical numeric cartridges vs directly
# forged full-source context, missing-edge and counterfactual decoy controls.
# One Google Colab cell; A100 80GB; frozen Qwen2.5-72B NF4 CUT3.
# Static-validated only: no A100 execution by code author.
import ast,hashlib,urllib.request,json,time,traceback,gc,random
from pathlib import Path
URL740='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/740.py'
BLOB740='c7a8f7f99f9687ccb69dba34f18259de810f2e72'
def _fetch742(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST742'}),timeout=120) as r:return r.read(250000)
def _blob742(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
raw740=_fetch742(URL740)
if _blob742(raw740)!=BLOB740:raise RuntimeError('TEST742_740_GIT_BLOB_LOCK')
src740=raw740.decode('utf-8');tree740=ast.parse(src740)
entry740=next(n for n in tree740.body if isinstance(n,ast.Try))
prefix740='\n'.join(src740.splitlines()[:entry740.lineno-1])+'\n'
prefix740=prefix740.replace("'/content/AKBASCORE_TEST740'","'/content/AKBASCORE_TEST742'")
prefix740=prefix740.replace("'/tmp/AKBASCORE_TEST740'","'/tmp/AKBASCORE_TEST742'")
prefix740=prefix740.replace("'TEST740.log'","'TEST742.log'")
prefix740=prefix740.replace("'TEST740_results.json'","'TEST742_results.json'")
prefix740=prefix740.replace("TEST='740'","TEST='742'")
exec(compile(prefix740,'LOCKED_740_PREFIX.py','exec'),globals())
T740.update({'test':'742','parent_source_git_blob':BLOB740,
 'purpose':'Evaluate cross-source transfer on presealed novel question templates with physical hierarchy and direct full-text controls',
 'limitations':[
  'Synthetic relational facts; no real-world or scientific discovery is demonstrated.',
  'Questions are new templates but facts are the same 12 records; this is not independent data holdout.',
  'Hierarchical CUT3 joint caches carry source information; no learned compression is asserted.',
  'Direct text baseline is freshly forged from source text and may have different token count and computation.',
  'The no-focus hierarchy has fewer tokens than focused hierarchy; neutral focus is length-matched.',
  'Two-choice accuracy can be inflated by chance; paired correctness and margins are reported.',
  'Decoy tests counterfactual sensitivity, not a failure if the model follows the changed source.',
  'No A100 execution by author; runtime checks determine validity.'],
 'arms':{},'cartridges':{}})
# Construct an independent question panel before loading the model or seeing outputs.
# No correct answer is copied into any question stem; both candidates are shown.
PANEL742=[]
def add742(kind,i,question,correct,wrong):
    gold='A' if (i+{'person_to_place':0,'place_to_person':1,'instrument_to_place':0}[kind])%2==0 else 'B'
    a,b=(correct,wrong) if gold=='A' else (wrong,correct)
    PANEL742.append({'id':f'{kind}_{i:02d}','kind':kind,'question':question,'A':a,'B':b,'gold':gold})
for i,p in enumerate(people):
    location=places[perm[i]]
    add742('person_to_place',i,f'Which location contains the system assigned to the instrument owned by {p}?',location,places[perm[(i+5)%12]])
    add742('place_to_person',i,f'Who owns the instrument assigned to the system located in {location}?',p,people[(i+5)%12])
    add742('instrument_to_place',i,f'At which location is the system that uses the {objects[i]} instrument?',location,places[perm[(i+7)%12]])
assert len(PANEL742)==36 and len({x['id'] for x in PANEL742})==36
PANEL740=PANEL742
PANEL_SHA740=sha(json.dumps(PANEL740,sort_keys=True,separators=(',',':')).encode())
(ROOT740/'sealed_panel.json').write_text(json.dumps(PANEL740,ensure_ascii=False,indent=2),encoding='utf-8')
T740['panel_sha256']=PANEL_SHA740
T740['panel_kind_counts']={k:sum(x['kind']==k for x in PANEL740) for k in ('person_to_place','place_to_person','instrument_to_place')}
save()
import torch,bitsandbytes
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
@torch.no_grad()
def evaluate742(cid):
    rows=read_scores(cid)
    assert len(rows)==len(PANEL740)
    for r,p in zip(rows,PANEL740):r['kind']=p['kind']
    bykind={k:sum(r['correct'] for r in rows if r['kind']==k) for k in T740['panel_kind_counts']}
    T740['arms'][cid]={'correct':sum(r['correct'] for r in rows),'total':len(rows),'by_kind':bykind,
        'rows':rows,'mean_gold_margin':sum(r['gold_margin'] for r in rows)/len(rows)}
    save();say('ARM_RESULT',cid,T740['arms'][cid]['correct'],'/',len(rows),bykind)
try:
    t0=time.perf_counter()
    ck('740_GIT_BLOB_LOCK',_blob742(raw740)==BLOB740)
    ck('CUDA',torch.cuda.is_available())
    ck('ONE_GPU',torch.cuda.device_count()==1)
    gpu_name=torch.cuda.get_device_name(0);gpu_total=torch.cuda.get_device_properties(0).total_memory
    ck('A100_80GB',('A100' in gpu_name) and gpu_total>=70*2**30,gpu_name)
    raw709=fetch(URL709);raw730=fetch(URL730)
    ck('709_GIT_BLOB_LOCK',gitblob(raw709)==GIT709)
    ck('730_SHA256_LOCK',sha(raw730)==SHA730)
    extract(raw709,NAMES709,'709.py');extract(raw730,NAMES730,'730.py')
    tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
    PIDS=tok('<|im_start|>system\nUse only the available document memory for document-specific questions. If the evidence is missing, say UNKNOWN.\n<|im_end|>\n<|im_start|>user\nINFORMATION:\n',add_special_tokens=False).input_ids
    P=len(PIDS)
    a_ids=tok(' A',add_special_tokens=False).input_ids;b_ids=tok(' B',add_special_tokens=False).input_ids
    ck('LABELS_ONE_TOKEN',len(a_ids)==1 and len(b_ids)==1 and a_ids!=b_ids,(a_ids,b_ids))
    AID740,BID740=a_ids[0],b_ids[0]
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
    model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,
        device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
    for par in model.parameters():par.requires_grad_(False)
    cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads)
    KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
    ck('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,(NL,H,QH,KVH,HD))
    ck('FROZEN',all(not par.requires_grad for par in model.parameters()))
    ck('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
    before=sentinel()
    make_source('C01',source1);make_source('C02',source2);make_source('C03',source3)
    make_source('C03_DECOY',source_decoy)
    make_joint('S01','C01','C02',focus_mode='semantic')
    make_joint('S01_NOFOCUS','C01','C02',focus_mode='none')
    make_joint('S01_NEUTRAL','C01','C02',focus_mode='neutral')
    make_joint('H01','S01','C03',focus_mode='semantic')
    make_joint('H01_NOFOCUS','S01_NOFOCUS','C03',focus_mode='none')
    make_joint('H01_NEUTRAL','S01_NEUTRAL','C03',focus_mode='neutral')
    make_joint('MISSING_C02','C01','C03',focus_mode='none')
    make_joint('H01_DECOY','S01','C03_DECOY',focus_mode='semantic')
    # Genuine directly forged full-text comparator, not another hierarchy.
    # Uses locked forge_native and identical frozen weights/tokenizer.
    flat_body=source1+'\n'+source2+'\n'+source3
    make_source('FLAT_TEXT',flat_body)
    ck('FLAT_SOURCES_SHA',sha(flat_body.encode())==sha((source1+'\n'+source2+'\n'+source3).encode()))
    T740['physical_bytes']={k:(CART740/v['file']).stat().st_size for k,v in T740['cartridges'].items()}
    T740['physical_tokens']={k:v['n'] for k,v in T740['cartridges'].items()}
    save()
    for arm in ('H01','H01_NOFOCUS','H01_NEUTRAL','FLAT_TEXT','S01','C03','MISSING_C02','H01_DECOY'):
        evaluate742(arm)
    arms=T740['arms'];base=arms['H01']['rows']
    T740['paired']={k:{'hier_only_correct':sum(a['correct'] and not b['correct'] for a,b in zip(base,arms[k]['rows'])),
                        'control_only_correct':sum(b['correct'] and not a['correct'] for a,b in zip(base,arms[k]['rows'])),
                        'same_prediction':sum(a['pred']==b['pred'] for a,b in zip(base,arms[k]['rows']))}
                    for k in arms if k!='H01'}
    T740['margin_deltas']={k:round(arms['H01']['mean_gold_margin']-v['mean_gold_margin'],5) for k,v in arms.items() if k!='H01'}
    T740['hierarchy_exceeds_flat_text_accuracy']=arms['H01']['correct']>arms['FLAT_TEXT']['correct']
    T740['hierarchy_exceeds_equal_information_controls']=arms['H01']['correct']>max(arms[k]['correct'] for k in ('H01_NOFOCUS','H01_NEUTRAL'))
    ck('PANEL_UNCHANGED',sha(json.dumps(PANEL740,sort_keys=True,separators=(',',':')).encode())==PANEL_SHA740)
    for cid,meta in T740['cartridges'].items():ck('FINAL_DISK_'+cid,sha_file(CART740/meta['file'])==meta['sha256'])
    ck('WEIGHTS_SENTINEL_UNCHANGED',sentinel()==before)
    T740['status']='COMPLETED_CROSS_SOURCE_EVALUATION'
    T740['novel_scientific_synthesis_proven']=False
    T740['elapsed_seconds']=round(time.perf_counter()-t0,2);save()
    say('TEST742_RESULT',json.dumps({'status':T740['status'],
        'scores':{k:v['correct'] for k,v in arms.items()},
        'by_kind':{k:v['by_kind'] for k,v in arms.items()},
        'hierarchy_exceeds_flat_text_accuracy':T740['hierarchy_exceeds_flat_text_accuracy'],
        'hierarchy_exceeds_equal_information_controls':T740['hierarchy_exceeds_equal_information_controls'],
        'margin_deltas':T740['margin_deltas'],'paired':T740['paired'],
        'physical_tokens':T740['physical_tokens'],
        'novel_scientific_synthesis_proven':False,
        'elapsed_seconds':T740['elapsed_seconds']},ensure_ascii=False))
    say('TEST742_FILES',OUT740,LOG740)
except Exception:
    T740['status']='ERROR';T740['traceback']=traceback.format_exc();save();say('TEST742_ERROR',T740['traceback']);raise
finally:
    gc.collect()
    if torch.cuda.is_available():torch.cuda.empty_cache()
