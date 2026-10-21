# AKBASCORE SILICON HIPPOCAMPUS — TEST743
# Conflict / revision / missing-evidence causal controls; frozen Qwen2.5-72B NF4 CUT3.
# ONE COLAB CELL. A100 80GB REQUIRED. STATIC VALIDATION ONLY; not executed on GPU by author.
# Reuses unchanged, SHA-locked TEST740 physical cartridge engine (709/730).
import ast,hashlib,urllib.request,json,time,traceback,gc,random
from pathlib import Path
URL740='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/740.py'
BLOB740='c7a8f7f99f9687ccb69dba34f18259de810f2e72'
def fetch743(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST743'}),timeout=120) as r:return r.read(250000)
def blob743(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
raw740=fetch743(URL740)
if blob743(raw740)!=BLOB740:raise RuntimeError('TEST743_740_GIT_BLOB_LOCK')
src=raw740.decode();tree=ast.parse(src)
entry=next(n for n in tree.body if isinstance(n,ast.Try))
prefix='\n'.join(src.splitlines()[:entry.lineno-1])+'\n'
for a,b in [('AKBASCORE_TEST740','AKBASCORE_TEST743'),('TEST740.log','TEST743.log'),('TEST740_results.json','TEST743_results.json'),("TEST='740'","TEST='743'")]:prefix=prefix.replace(a,b)
exec(compile(prefix,'LOCKED_740_PREFIX.py','exec'),globals())
# Dependency bootstrap is inherited from locked TEST740/TEST742 prefix.
import torch,bitsandbytes
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
# Synthetic facts deliberately constructed BEFORE model loading and independently sealed.
# Date precedence is specified explicitly. Incomplete/ambiguous records must yield UNKNOWN.
people=['Nera','Varo','Miro','Sela','Tavin','Ruma','Kira','Sora','Orin','Mira','Leto','Vela']
objects=['violet','copper','cedar','slate','amber','silver','indigo','quartz','onyx','coral','ivory','bronze']
systems=['Axion','Bexor','Cylar','Davor','Evrin','Fayen','Gorix','Havor','Ixion','Jovar','Kavin','Luron']
places=['Arden','Boreal','Cobalt','Dorian','Eldrin','Fennel','Garnet','Helios','Indigo','Juniper','Kestrel','Linden']
perm=list(range(12));random.Random(7402026).shuffle(perm)
# C01: owner -> instrument; C02: instrument -> system; C03: system -> location.
source1='\n'.join(f'{p} owns the {o} instrument.' for p,o in zip(people,objects))
source2='\n'.join(f'The {o} instrument is assigned to the {systems[i]} system.' for i,o in enumerate(objects))
source3='\n'.join(f'The {systems[i]} system is located in {places[perm[i]]}.' for i in range(12))
# New dated updates. Four systems change location, four have ambiguous same-date
# conflicting location claims, and four are unmodified. Unknown entities have no record.
changed=(0,1,2,3);conflicted=(4,5,6,7);unchanged=(8,9,10,11)
newplaces={i:places[perm[(i+5)%12]] for i in changed}
conflictplaces={i:places[perm[(i+6)%12]] for i in conflicted}
update_lines=['RECORD POLICY: For a system, a later dated location replaces earlier dated locations. If two different locations have the same latest date and neither has priority, its location is UNKNOWN. If no record exists, answer UNKNOWN.']
for i in range(12):
    update_lines.append(f'On 2026-01-01 the {systems[i]} system location was recorded as {places[perm[i]]}.')
for i in changed:update_lines.append(f'On 2026-08-01 the {systems[i]} system location was updated to {newplaces[i]}.')
for i in conflicted:
    update_lines.append(f'On 2026-08-01 the {systems[i]} system location was recorded as {places[perm[i]]}.')
    update_lines.append(f'On 2026-08-01 the {systems[i]} system location was recorded as {conflictplaces[i]}.')
source4='\n'.join(update_lines)
# Equal-information baseline: one direct, newly forged context cartridge.
flat_body=source1+'\n'+source2+'\n'+source3+'\n'+source4
# Counterfactual control: remove the update source entirely.
# Causal comparison is evaluated only on changed and conflicted cases.
PANEL743=[]
def add_case(kind,i,question,correct,wrong):
    gold='A' if len(PANEL743)%2==0 else 'B'
    a,b=(correct,wrong) if gold=='A' else (wrong,correct)
    PANEL743.append({'id':f'{kind}_{i:02d}','kind':kind,'question':question,
                     'A':a,'B':b,'gold':gold,'correct_text':correct})
for i,p in enumerate(people):
    q=f'Using the latest valid dated record, where is the system assigned to the instrument owned by {p} located? If the record is ambiguous or missing, choose UNKNOWN.'
    if i in changed:add_case('revised',i,q,newplaces[i],places[perm[i]])
    elif i in conflicted:add_case('conflict',i,q,'UNKNOWN',places[perm[i]])
    else:add_case('unchanged',i,q,places[perm[i]],places[perm[(i+3)%12]])
for i in range(8):
    q=f'Using only recorded facts, where is the system assigned to the instrument owned by UnknownPerson{i} located? If absent, choose UNKNOWN.'
    add_case('missing',i,q,'UNKNOWN',places[perm[i]])
# Include direct system queries to separate chain retrieval from conflict handling.
for i in changed+conflicted:
    q=f'What is the latest unambiguous location for the {systems[i]} system? If the latest records conflict, choose UNKNOWN.'
    correct=newplaces[i] if i in changed else 'UNKNOWN'
    add_case('direct_revised' if i in changed else 'direct_conflict',i,q,correct,places[perm[i]])
assert len(PANEL743)==28
PANEL740=PANEL743
PANEL_SHA740=sha(json.dumps(PANEL740,sort_keys=True,separators=(',',':')).encode())
(ROOT740/'sealed_panel.json').write_text(json.dumps(PANEL740,indent=2),encoding='utf-8')
T740.update({'test':'743','status':'STARTED','parent_source_git_blob':BLOB740,
 'panel_sha256':PANEL_SHA740,'arms':{},'cartridges':{},
 'source_sha256':{k:sha(v.encode()) for k,v in {'C01':source1,'C02':source2,'C03':source3,'C04':source4}.items()},
 'limitations':['Synthetic 28-question fixed panel; no independent generalization claim.',
 'UNKNOWN is one of two displayed answer options, so chance baseline is 50%.',
 'The policy text is explicitly supplied, not autonomously discovered.',
 'Dated updates are appended as a physical cartridge; earlier KV is immutable.',
 'Hierarchy and flat text may have different token counts and computation.',
 'A correct UNKNOWN choice does not by itself demonstrate calibrated uncertainty.',
 'A100 80GB is required, matching the successful TEST742 runtime; no 40GB fallback.',
 'The original 740 engine is reused with exact SHA locks; not GPU-tested by author.']})
save()
@torch.no_grad()
def evaluate743(cid):
    cp=to_gpu(load_cp(cid));memory=initialize_native(cp);rows=[]
    for item in PANEL740:
        suffix=('\nQUESTION:\n'+item['question']+'\nA: '+item['A']+'\nB: '+item['B']+
                '\nChoose only A or B.\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n')
        ids=tok(suffix,add_special_tokens=False).input_ids
        n=cp['n'];ensure_room(len(ids)+256)
        cache=cache_build(memory);pos=torch.arange(n,n+len(ids),device=DEV)
        out=model(input_ids=torch.tensor([ids],device=DEV),past_key_values=cache,
            attention_mask=torch.ones((1,n+len(ids)),device=DEV,dtype=torch.long),
            position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
        logits=out.logits[0,-1,:].float();la=float(logits[AID740]);lb=float(logits[BID740])
        pred='A' if la>lb else 'B' if lb>la else 'TIE'
        rows.append({'id':item['id'],'kind':item['kind'],'pred':pred,'gold':item['gold'],
                     'correct':pred==item['gold'],'gold_margin':la-lb if item['gold']=='A' else lb-la})
        del out,cache,logits
    del memory,cp;release()
    kinds=sorted(set(r['kind'] for r in rows))
    T740['arms'][cid]={'correct':sum(r['correct'] for r in rows),'total':len(rows),
        'by_kind':{k:sum(r['correct'] for r in rows if r['kind']==k) for k in kinds},
        'rows':rows,'mean_gold_margin':sum(r['gold_margin'] for r in rows)/len(rows)}
    save();say('ARM_RESULT',cid,T740['arms'][cid]['correct'],'/',len(rows),T740['arms'][cid]['by_kind'])
try:
    t0=time.perf_counter();ck('740_GIT_BLOB_LOCK',blob743(raw740)==BLOB740)
    ck('CUDA',torch.cuda.is_available());ck('ONE_GPU',torch.cuda.device_count()==1)
    gpu_name=torch.cuda.get_device_name(0);gpu_total=torch.cuda.get_device_properties(0).total_memory
    ck('A100_80GB','A100' in gpu_name and gpu_total>=70*2**30,gpu_name)
    say('GPU_MEMORY_GIB',round(gpu_total/2**30,2),'STRICT_80GB_ENGINE')
    raw709=fetch(URL709);raw730=fetch(URL730)
    ck('709_GIT_BLOB_LOCK',gitblob(raw709)==GIT709);ck('730_SHA256_LOCK',sha(raw730)==SHA730)
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
    for p in model.parameters():p.requires_grad_(False)
    cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads)
    KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
    ck('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,(NL,H,QH,KVH,HD))
    ck('FROZEN',all(not p.requires_grad for p in model.parameters()))
    ck('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
    ck('MODEL_GPU_FREE_HEADROOM',torch.cuda.mem_get_info()[0]>=GPU_RESERVE_GIB*2**30+512*NL*KVH*HD*4)
    before=sentinel()
    make_source('C01',source1);make_source('C02',source2);make_source('C03',source3);make_source('C04',source4)
    make_joint('S01','C01','C02',focus_mode='semantic')
    make_joint('H01_OLD','S01','C03',focus_mode='semantic')
    make_joint('H02_UPDATED','H01_OLD','C04',focus_mode='semantic')
    make_source('FLAT_UPDATED',flat_body)
    for arm in ('H02_UPDATED','FLAT_UPDATED','H01_OLD','C04'):
        evaluate743(arm)
    arms=T740['arms'];updated=arms['H02_UPDATED']['rows']
    T740['paired']={k:{'updated_only_correct':sum(a['correct'] and not b['correct'] for a,b in zip(updated,v['rows'])),
                         'control_only_correct':sum(b['correct'] and not a['correct'] for a,b in zip(updated,v['rows']))}
                    for k,v in arms.items() if k!='H02_UPDATED'}
    ck('PANEL_UNCHANGED',sha(json.dumps(PANEL740,sort_keys=True,separators=(',',':')).encode())==PANEL_SHA740)
    for cid,meta in T740['cartridges'].items():
        ck('FINAL_DISK_'+cid,sha_file(CART740/meta['file'])==meta['sha256'])
    ck('WEIGHTS_SENTINEL_UNCHANGED',sentinel()==before)
    T740['status']='COMPLETED_CONFLICT_REVISION_EVALUATION'
    T740['hierarchy_exceeds_flat_text_accuracy']=arms['H02_UPDATED']['correct']>arms['FLAT_UPDATED']['correct']
    T740['elapsed_seconds']=round(time.perf_counter()-t0,2);save()
    say('TEST743_RESULT',json.dumps({'status':T740['status'],
        'scores':{k:v['correct'] for k,v in arms.items()},
        'by_kind':{k:v['by_kind'] for k,v in arms.items()},
        'paired':T740['paired'],
        'hierarchy_exceeds_flat_text_accuracy':T740['hierarchy_exceeds_flat_text_accuracy'],
        'elapsed_seconds':T740['elapsed_seconds']},ensure_ascii=False))
    say('TEST743_FILES',OUT740,LOG740)
except Exception:
    T740['status']='ERROR';T740['traceback']=traceback.format_exc();save();say('TEST743_ERROR',T740['traceback']);raise
finally:
    gc.collect()
    if torch.cuda.is_available():torch.cuda.empty_cache()
