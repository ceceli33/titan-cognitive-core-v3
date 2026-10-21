# AKBASCORE SILICON HIPPOCAMPUS — TEST741
# Physical parent-free persistence and controlled suffix-truncation.
# One Google Colab cell. Requires NVIDIA A100 80GB.
# Imports the EXACT Git-blob-locked TEST740 code up to (not including) its execution block.
# Reuses locked 709/730 CUT3 engine; no change to attention, RoPE, model, or quantization.
# NOT executed on A100 by code author. Static syntax validation only.
import ast, hashlib, urllib.request, json, time, traceback, gc, shutil
from pathlib import Path
URL740='https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/740.py'
BLOB740='c7a8f7f99f9687ccb69dba34f18259de810f2e72'
def _get741(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AKBASCORE-TEST741'}),timeout=120) as r:
        return r.read(250000)
def _blob741(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
raw740=_get741(URL740)
if _blob741(raw740)!=BLOB740:raise RuntimeError('TEST741_740_GIT_BLOB_LOCK')
source740=raw740.decode('utf-8')
tree740=ast.parse(source740)
# Stop BEFORE TEST740's top-level execution; retain all verified definitions.
entry740=next(n for n in tree740.body if isinstance(n,ast.Try))
pre740='\n'.join(source740.splitlines()[:entry740.lineno-1])+'\n'
# Isolate all generated artifacts. Preserve panel seed, facts, source IDs, engine code.
pre740=pre740.replace("'/content/AKBASCORE_TEST740'", "'/content/AKBASCORE_TEST741'")
pre740=pre740.replace("'/tmp/AKBASCORE_TEST740'", "'/tmp/AKBASCORE_TEST741'")
pre740=pre740.replace("'TEST740.log'", "'TEST741.log'")
pre740=pre740.replace("'TEST740_results.json'", "'TEST741_results.json'")
pre740=pre740.replace("TEST='740'", "TEST='741'")
exec(compile(pre740,'LOCKED_740_PREFIX.py','exec'),globals())
# TEST740 prefix defines T740, ROOT740, CART740, etc. Those names are retained
# intentionally to avoid modifying tested engine functions or data bindings.
T740['test']='741'
T740['parent_source_git_blob']=BLOB740
T740['purpose']='Parent-free H01 reload and suffix-only memory reduction'
T740['limitations']=[
 'The same sealed 12-question synthetic panel is used; this is not a new held-out generalization test.',
 'Deleting parent files tests operational independence, not autonomous semantic consolidation.',
 'Suffix truncation removes existing KV/H3 tokens; it is not learned compression or synthesis.',
 'The base model remains resident on GPU; this is not a process-restart test.',
 'Parent cartridge SHA metadata remains in JSON for provenance; parent files are quarantined.',
 'Original source facts are not provided to read_scores; model pretraining knowledge cannot be fully excluded.',
 'No GPU run performed by code author; runtime checks are authoritative.'
]
T740['arms']={};T740['cartridges']={};save()
import torch, bitsandbytes
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig

def cp_bytes741(cid):
    return (CART740/T740['cartridges'][cid]['file']).stat().st_size

@torch.no_grad()
def suffix_trim741(src,dst,drop):
    cp=load_cp(src)
    ck('TRIM_VALID_'+dst,0<drop<cp['n']-P,(drop,cp['n'],P))
    oldn=cp['n'];newn=oldn-drop
    cp['h']=cp['h'][:,:newn,:].contiguous()
    cp['lower']=tuple((k[...,:newn,:].contiguous(),v[...,:newn,:].contiguous()) for k,v in cp['lower'])
    cp['n']=newn;cp['body_tokens']=newn-P;cp['book_id']=dst
    ck('TRIM_SHAPES_'+dst,cp['h'].shape[1]==newn and all(k.shape[-2]==newn and v.shape[-2]==newn for k,v in cp['lower']))
    save_cp(dst,cp,[src]);del cp
    ck('TRIM_SAVINGS_'+dst,cp_bytes741(dst)<cp_bytes741(src),(cp_bytes741(dst),cp_bytes741(src)))

@torch.no_grad()
def eval741(cid):
    # Every arm is loaded from its SHA-verified physical file, never a live build cache.
    rows=read_scores(cid)
    T740['arms'][cid]={'correct':sum(x['correct'] for x in rows),'total':len(rows),
                        'rows':rows,'mean_gold_margin':sum(x['gold_margin'] for x in rows)/len(rows)}
    save();say('ARM_RESULT',cid,T740['arms'][cid]['correct'],'/',len(rows))

try:
    t0=time.perf_counter()
    ck('740_GIT_BLOB_LOCK',_blob741(raw740)==BLOB740)
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
    a_ids=tok(' A',add_special_tokens=False).input_ids
    b_ids=tok(' B',add_special_tokens=False).input_ids
    ck('LABELS_ONE_TOKEN',len(a_ids)==1 and len(b_ids)==1 and a_ids!=b_ids,(a_ids,b_ids))
    AID740,BID740=a_ids[0],b_ids[0]
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
    model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,
        device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
    for param in model.parameters():param.requires_grad_(False)
    cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads)
    KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
    ck('ARCH',(NL,H,QH,KVH,HD)==EXPECTED,(NL,H,QH,KVH,HD))
    ck('FROZEN',all(not param.requires_grad for param in model.parameters()))
    ck('NF4',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
    before=sentinel()
    # Produce physical parent sources and hierarchical H01 using locked TEST740 methods.
    make_source('C01',source1);make_source('C02',source2);make_source('C03',source3)
    make_joint('S01','C01','C02',focus_mode='semantic')
    make_joint('H01','S01','C03',focus_mode='semantic')
    # Record physical sizes BEFORE removing any parents.
    sizes={cid:cp_bytes741(cid) for cid in ('C01','C02','C03','S01','H01')}
    T740['initial_sizes_bytes']=sizes;save()
    # Verify baseline and ablation prior to physical parent removal.
    eval741('S01');eval741('C03');eval741('H01')
    ck('BASELINE_H01_12_OF_12',T740['arms']['H01']['correct']==12)
    # Last 30 H01 tokens are its terminal semantic focus, as sealed by TEST740.
    focus_len=len(tok(FOCUS740,add_special_tokens=False).input_ids)
    ck('FOCUS_LENGTH_30',focus_len==30,focus_len)
    suffix_trim741('H01','H01_TRIM15',15)
    suffix_trim741('H01','H01_TRIM30',focus_len)
    # Remove all source/first-level physical files from the active cartridge pool.
    # Quarantine rather than irreversibly delete: test is reproducible and reversible.
    quarantine=ROOT740/'quarantined_parents';quarantine.mkdir(exist_ok=True)
    for cid in ('C01','C02','C03','S01'):
        source=CART740/T740['cartridges'][cid]['file']
        ck('PARENT_SHA_BEFORE_QUARANTINE_'+cid,sha_file(source)==T740['cartridges'][cid]['sha256'])
        source.replace(quarantine/source.name)
        ck('PARENT_UNAVAILABLE_'+cid,not source.exists())
    # Remove Python-held source strings; the answer path accesses only H01 descendants.
    source1=source2=source3=source_decoy=None
    del source740,pre740,raw740,raw709,raw730
    release()
    # Parent-free readback. Model remains loaded, but each cartridge is disk reloaded.
    for cid in ('H01','H01_TRIM15','H01_TRIM30'):
        ck('PARENT_FREE_'+cid,all(not (CART740/T740['cartridges'][p]['file']).exists() for p in ('C01','C02','C03','S01')))
        eval741(cid)
    baseline=T740['arms']['H01']['rows']
    for cid in ('H01_TRIM15','H01_TRIM30'):
        rows=T740['arms'][cid]['rows']
        T740['trim_analysis_'+cid]={
            'bytes':cp_bytes741(cid),'bytes_saved':cp_bytes741('H01')-cp_bytes741(cid),
            'saved_fraction':round(1-cp_bytes741(cid)/cp_bytes741('H01'),6),
            'paired_same_predictions':sum(a['pred']==b['pred'] for a,b in zip(baseline,rows)),
            'correct':T740['arms'][cid]['correct'],
            'mean_margin_delta':round(T740['arms'][cid]['mean_gold_margin']-T740['arms']['H01']['mean_gold_margin'],6)
        }
    T740['parent_free_full_retention']=T740['arms']['H01']['correct']==12
    T740['trim30_full_retention']=T740['arms']['H01_TRIM30']['correct']==12
    T740['compression_vs_sources']=round(sizes['H01']/sum(sizes[x] for x in ('C01','C02','C03')),6)
    T740['actual_learned_consolidation_proven']=False
    ck('PANEL_UNCHANGED',sha(json.dumps(PANEL740,sort_keys=True,separators=(',',':')).encode())==PANEL_SHA740)
    for cid in ('H01','H01_TRIM15','H01_TRIM30'):
        ck('FINAL_DISK_'+cid,sha_file(CART740/T740['cartridges'][cid]['file'])==T740['cartridges'][cid]['sha256'])
    ck('WEIGHTS_SENTINEL_UNCHANGED',sentinel()==before)
    T740['status']='COMPLETED_PARENT_FREE_RETENTION' if T740['parent_free_full_retention'] else 'COMPLETED_PARENT_FREE_RETENTION_FAILURE'
    T740['elapsed_seconds']=round(time.perf_counter()-t0,2);save()
    say('TEST741_RESULT',json.dumps({'status':T740['status'],
        'scores':{k:v['correct'] for k,v in T740['arms'].items()},
        'initial_sizes_bytes':sizes,'compression_vs_sources':T740['compression_vs_sources'],
        'trim15':T740['trim_analysis_H01_TRIM15'],'trim30':T740['trim_analysis_H01_TRIM30'],
        'parent_free_full_retention':T740['parent_free_full_retention'],
        'actual_learned_consolidation_proven':False,'elapsed_seconds':T740['elapsed_seconds']},ensure_ascii=False))
    say('TEST741_FILES',OUT740,LOG740)
except Exception:
    T740['status']='ERROR';T740['traceback']=traceback.format_exc();save();say('TEST741_ERROR',T740['traceback']);raise
finally:
    gc.collect()
    if torch.cuda.is_available():torch.cuda.empty_cache()
