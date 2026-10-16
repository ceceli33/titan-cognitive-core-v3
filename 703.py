# AKBASCORE TEST703 — QWEN2.5-72B NF4 / INCREMENTAL CARTRIDGE CAPACITY
# Standalone Colab cell. TEST702-R2 native checkpoint/init/append/answer backbone.
# CUT1/3/6; stages 2/8/32/128; append-only checks; raw QA; absence controls.
import os,sys,time,json,hashlib,traceback,gc,subprocess,importlib.util,random,platform,inspect
from pathlib import Path
from datetime import datetime,timezone
for m,p in [('transformers','transformers>=5.18,<6'),('accelerate','accelerate>=1.15'),('bitsandbytes','bitsandbytes>=0.50'),('psutil','psutil')]:
    if importlib.util.find_spec(m) is None:subprocess.check_call([sys.executable,'-m','pip','install','-q',p])
import torch,transformers,accelerate,bitsandbytes,psutil
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
TEST='703';REVISION='703-R1';SEED=7032026;MODEL_ID='Qwen/Qwen2.5-72B-Instruct'
EXPECTED=(80,8192,64,8,128);CUTS=(1,3,6);STAGES=(2,8,32,128);DTYPE=torch.bfloat16;DEVICE=torch.device('cuda:0')
ROOT=Path('/content/AKBASCORE_TEST703');ROOT.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'TEST703_results.json';LOG=ROOT/'TEST703.log';LOG.write_text('',encoding='utf-8')
random.seed(SEED);torch.manual_seed(SEED)
if torch.cuda.is_available():torch.cuda.manual_seed_all(SEED)
torch.set_grad_enabled(False);os.environ['TOKENIZERS_PARALLELISM']='false';START=time.perf_counter()
RESULT={'test':TEST,'revision':REVISION,'model':MODEL_ID,'status':'STARTED','timestamp':datetime.now(timezone.utc).isoformat(),'seed':SEED,'cuts':list(CUTS),'stages':list(STAGES),'checks':[],'runs':[]}
def log(*a):
    s=' '.join(map(str,a));print(s,flush=True)
    with LOG.open('a',encoding='utf-8') as f:f.write(s+'\n')
def save():
    t=OUT.with_suffix('.tmp');t.write_text(json.dumps(RESULT,indent=2,ensure_ascii=False,default=str),encoding='utf-8');t.replace(OUT)
def check(name,ok,detail=None):
    ok=bool(ok);RESULT['checks'].append({'name':name,'pass':ok,'detail':detail});log('PASS' if ok else 'FAIL',name,detail if detail is not None else '')
    if not ok:raise RuntimeError('CHECK_FAILED_'+name)
def gib(n):return round(float(n)/2**30,5)
def mem():
    torch.cuda.synchronize();free,total=torch.cuda.mem_get_info()
    return {'gpu_free_gib':gib(free),'gpu_total_gib':gib(total),'gpu_allocated_gib':gib(torch.cuda.memory_allocated()),'gpu_reserved_gib':gib(torch.cuda.memory_reserved()),'gpu_peak_allocated_gib':gib(torch.cuda.max_memory_allocated()),'ram_available_gib':gib(psutil.virtual_memory().available)}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def pairs(c):
    if hasattr(c,'layers'):return tuple((l.keys,l.values) for l in c.layers)
    if hasattr(c,'key_cache'):return tuple(zip(c.key_cache,c.value_cache))
    if isinstance(c,(tuple,list)):return tuple((x[0],x[1]) for x in c)
    raise TypeError('UNSUPPORTED_CACHE_'+type(c).__name__)
def clone(c):return tuple((k.detach().clone(),v.detach().clone()) for k,v in pairs(c))
def cache_build(kvs):
    c=DynamicCache()
    for i,(k,v) in enumerate(kvs):c.update(k,v,i)
    return c
def replace(out,h):
    if isinstance(out,tuple):return (h,)+out[1:]
    if isinstance(out,list):return [h]+out[1:]
    return h
def half(x):
    a,b=x.chunk(2,-1);return torch.cat((-b,a),-1)
def rope(pos):
    d=torch.zeros((1,len(pos),H),device=DEVICE,dtype=DTYPE);co,si=model.model.rotary_emb(d,pos.unsqueeze(0));return co.unsqueeze(1).float(),si.unsqueeze(1).float()
def rephase(k,old,new):
    if torch.equal(old,new):return k
    co,so=rope(old);cn,sn=rope(new);x=k.float();x=x*co-half(x)*so;return (x*cn+half(x)*sn).to(k.dtype)
def weight_sentinel():
    h=hashlib.sha256();p=[model.model.layers[i].self_attn.o_proj.weight for i in (0,19,39,59,79)]+[model.model.norm.weight,model.lm_head.weight]
    for w in p:
        a=w.detach().reshape(-1);n=a.numel()
        for j in range(16):
            o=j*max(n-256,0)//15;h.update(a[o:o+256].float().cpu().numpy().tobytes())
    return h.hexdigest()
def forward_ids(ids):
    n=len(ids);pos=torch.arange(n,device=DEVICE)
    return model(input_ids=torch.tensor([ids],device=DEVICE),attention_mask=torch.ones((1,n),device=DEVICE,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
@torch.no_grad()
def checkpoint(ci,cut):
    ids=PIDS+CAR[ci]['body'];n=len(ids);state={}
    def capture(module,args,out):state['h']=(out[0] if isinstance(out,(tuple,list)) else out).detach().clone()
    hook=model.model.layers[cut].register_forward_hook(capture)
    try:
        out=forward_ids(ids);kv=clone(out.past_key_values)
        if 'h' not in state or state['h'].shape!=(1,n,H) or len(kv)!=NL:raise RuntimeError('FORGE_GEOMETRY')
        return {'h':state['h'],'kv':kv,'pos':torch.arange(n,device=DEVICE),'body':n-P}
    finally:hook.remove()
@torch.no_grad()
def init_from_checkpoint(cp,cut):
    n=cp['h'].shape[1]
    def inject(module,args,out):
        cur=out[0] if isinstance(out,(tuple,list)) else out
        if cur.shape!=cp['h'].shape:raise RuntimeError('INIT_INJECTION_SHAPE')
        return replace(out,cp['h'])
    hook=model.model.layers[cut].register_forward_hook(inject)
    try:
        pos=torch.arange(n,device=DEVICE)
        out=model(inputs_embeds=torch.zeros((1,n,H),device=DEVICE,dtype=DTYPE),attention_mask=torch.ones((1,n),device=DEVICE,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
        upper=clone(out.past_key_values)
        if len(upper)!=NL:raise RuntimeError('INIT_UPPER_COUNT')
        return cp['kv'][:cut+1]+upper[cut+1:]
    finally:hook.remove()
@torch.no_grad()
def append_from_checkpoint(memory,cp,cut):
    oldn=int(memory[0][0].shape[-2]);q=cp['body'];pos=torch.arange(oldn,oldn+q,device=DEVICE);body=cp['h'][:,P:,:]
    if body.shape!=(1,q,H):raise RuntimeError('BODY_SHAPE')
    def inject(module,args,out):
        cur=out[0] if isinstance(out,(tuple,list)) else out
        if cur.shape!=body.shape:raise RuntimeError('APPEND_INJECTION_SHAPE')
        return replace(out,body)
    hook=model.model.layers[cut].register_forward_hook(inject)
    try:
        out=model(inputs_embeds=torch.zeros((1,q,H),device=DEVICE,dtype=DTYPE),past_key_values=cache_build(memory),attention_mask=torch.ones((1,oldn+q),device=DEVICE,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
        grown=list(clone(out.past_key_values))
        for i in range(cut+1):
            ok,ov=memory[i];k,v=cp['kv'][i];k=rephase(k[:,:,P:,:],cp['pos'][P:],pos);v=v[:,:,P:,:]
            grown[i]=(torch.cat((ok,k),-2),torch.cat((ov,v),-2))
        result=tuple(grown)
        if len(result)!=NL:raise RuntimeError('APPEND_LAYER_COUNT')
        for i,((ok,ov),(nk,nv)) in enumerate(zip(memory,result)):
            if nk.shape[-2]!=oldn+q or nv.shape[-2]!=oldn+q:raise RuntimeError('CACHE_LENGTH_LAYER_'+str(i))
            if not torch.equal(ok,nk[:,:,:oldn,:]) or not torch.equal(ov,nv[:,:,:oldn,:]):raise RuntimeError('APPEND_BITWISE_LAYER_'+str(i))
        return result
    finally:hook.remove()
def kv_profile(m):
    size=sum(k.numel()*k.element_size()+v.numel()*v.element_size() for k,v in m)
    return {'layers':len(m),'tokens':int(m[0][0].shape[-2]),'kv_bytes':int(size),'kv_gib':gib(size),'shape':list(m[0][0].shape)}
@torch.no_grad()
def answer(memory,question,max_new=20):
    suffix='\nQUESTION:\n'+question+'\n\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n'
    ids=tok(suffix,add_special_tokens=False).input_ids;n=int(memory[0][0].shape[-2]);pos=torch.arange(n,n+len(ids),device=DEVICE)
    cache=cache_build(memory)
    out=model(input_ids=torch.tensor([ids],device=DEVICE),past_key_values=cache,attention_mask=torch.ones((1,n+len(ids)),device=DEVICE,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
    cache=out.past_key_values;next_id=out.logits[:,-1,:].argmax(-1,keepdim=True);gen=[]
    stop={tok.eos_token_id,tok.convert_tokens_to_ids('<|im_end|>')}
    for _ in range(max_new):
        t=int(next_id.item())
        if t in stop:break
        gen.append(t);n=cache.get_seq_length();pos=torch.tensor([n],device=DEVICE)
        out=model(input_ids=next_id,past_key_values=cache,attention_mask=torch.ones((1,n+1),device=DEVICE,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
        cache=out.past_key_values;next_id=out.logits[:,-1,:].argmax(-1,keepdim=True)
    return tok.decode(gen,skip_special_tokens=True).strip()
def factual_score(raw,target,all_targets):
    import re
    hits=[v for v in all_targets if re.search(r'(?<!\w)'+re.escape(v)+r'(?!\w)',raw,re.IGNORECASE)]
    return {'exact':raw.strip().casefold()==target.casefold(),'target_present':target in hits,'other_targets_present':[x for x in hits if x!=target],'unambiguous':target in hits and len(hits)==1}
def query_index(n):
    # Fixed preregistered coverage: first, middle, last plus 3 seeded positions.
    indices={0,n//2,n-1};rng=random.Random(SEED+n)
    while len(indices)<min(n,6):indices.add(rng.randrange(n))
    return sorted(indices)
def run_cut(cut):
    run={'cut':cut,'status':'STARTED','stages':[]};RESULT['runs'].append(run);save()
    memory=None;last_stage=0
    try:
        gc.collect();torch.cuda.empty_cache();torch.cuda.reset_peak_memory_stats()
        for stage in STAGES:
            row={'count':stage,'status':'STARTED','start_memory':mem(),'checks':[],'queries':[]};run['stages'].append(row);save();t0=time.perf_counter()
            for ci in range(last_stage,stage):
                cp=checkpoint(ci,cut)
                if memory is None:
                    memory=init_from_checkpoint(cp,cut)
                    if not all(torch.equal(memory[i][0],cp['kv'][i][0]) and torch.equal(memory[i][1],cp['kv'][i][1]) for i in range(cut+1)):raise RuntimeError('INIT_LOWER_NOT_EXACT')
                else:
                    oldn=memory[0][0].shape[-2];new=append_from_checkpoint(memory,cp,cut)
                    # Validate new lower-layer cartridge rows against independently forged rows.
                    pos=torch.arange(oldn,oldn+cp['body'],device=DEVICE)
                    for li in range(cut+1):
                        ek=rephase(cp['kv'][li][0][:,:,P:,:],cp['pos'][P:],pos);ev=cp['kv'][li][1][:,:,P:,:]
                        if not torch.equal(new[li][0][:,:,oldn:,:],ek) or not torch.equal(new[li][1][:,:,oldn:,:],ev):raise RuntimeError('LOWER_REPHASE_LAYER_'+str(li))
                    memory=new
                    del new
                del cp
                if (ci+1)%16==0:log('CUT',cut,'APPENDED',ci+1,'/',stage)
            last_stage=stage
            row['build_seconds']=round(time.perf_counter()-t0,3)
            row['profile']=kv_profile(memory);row['memory_after_build']=mem()
            expected=P+sum(len(CAR[i]['body']) for i in range(stage))
            if row['profile']['tokens']!=expected or row['profile']['layers']!=NL:raise RuntimeError('STAGE_CACHE_GEOMETRY')
            row['checks'].append({'name':'CACHE_LENGTH','pass':True})
            row['checks'].append({'name':'ALL_APPEND_BITWISE','pass':True})
            for idx in query_index(stage):
                raw=answer(memory,CAR[idx]['question']);score=factual_score(raw,CAR[idx]['target'],TARGETS)
                item={'index':idx,'question':CAR[idx]['question'],'expected':CAR[idx]['target'],'raw':raw,**score}
                row['queries'].append(item);log('CUT',cut,'N',stage,'Q',idx,'RAW',repr(raw),'UNAMBIGUOUS',score['unambiguous'])
            if stage==2:
                # Omission control: cartridge 1 absent; compare same question against full 2-cartridge memory.
                cp_control=checkpoint(0,cut);control_memory=init_from_checkpoint(cp_control,cut)
                absent_raw=answer(control_memory,CAR[1]['question']);full_raw=next((x['raw'] for x in row['queries'] if x['index']==1),None)
                row['omission_control']={'excluded_index':1,'question':CAR[1]['question'],'expected':CAR[1]['target'],'without_raw':absent_raw,'with_raw':full_raw,'without_score':factual_score(absent_raw,CAR[1]['target'],TARGETS),'with_score':factual_score(full_raw,CAR[1]['target'],TARGETS) if full_raw is not None else None}
                log('CUT',cut,'OMISSION_CONTROL',repr(absent_raw),'FULL',repr(full_raw))
                del cp_control,control_memory
            row['accuracy']={'tested':len(row['queries']),'exact':sum(x['exact'] for x in row['queries']),'target_present':sum(x['target_present'] for x in row['queries']),'unambiguous':sum(x['unambiguous'] for x in row['queries'])}
            row['memory_after_queries']=mem();row['status']='PASS_PHYSICAL'
            log('STAGE',stage,'CUT',cut,'PASS_PHYSICAL','TOKENS',expected,'UNAMBIGUOUS',row['accuracy']['unambiguous'],'/',row['accuracy']['tested'])
            save()
        run['status']='PASS_PHYSICAL'
    except Exception as e:
        run['status']='OOM' if isinstance(e,torch.cuda.OutOfMemoryError) else 'ERROR'
        run['error_type']=type(e).__name__;run['error']=str(e);run['traceback']=traceback.format_exc()[-9000:]
        if run['stages'] and run['stages'][-1]['status']=='STARTED':run['stages'][-1]['status']=run['status']
        log('CUT',cut,run['status'],type(e).__name__,str(e))
    finally:
        try:run['end_memory']=mem()
        except Exception:pass
        del memory;gc.collect();torch.cuda.empty_cache();save()
    return run
try:
    log('='*110);log('AKBASCORE TEST703 — QWEN2.5-72B / NF4 / INCREMENTAL CARTRIDGE CAPACITY');log('='*110)
    check('CUDA_AVAILABLE',torch.cuda.is_available());check('SINGLE_GPU',torch.cuda.device_count()==1)
    check('A100_80GB_CLASS',torch.cuda.get_device_properties(0).total_memory>=70*2**30)
    RESULT['hardware']={'gpu':torch.cuda.get_device_name(0),'before':mem()}
    RESULT['versions']={'torch':torch.__version__,'transformers':transformers.__version__,'accelerate':accelerate.__version__,'bitsandbytes':bitsandbytes.__version__,'python':platform.python_version()}
    tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type='nf4',bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
    log('LOADING_MODEL_NF4_GPU_ONLY');t0=time.perf_counter()
    model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={'':0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation='sdpa').eval()
    for p in model.parameters():p.requires_grad_(False)
    torch.cuda.synchronize();RESULT['load_seconds']=round(time.perf_counter()-t0,3);RESULT['memory_after_load']=mem()
    cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads);HD=int(getattr(cfg,'head_dim',None) or H//QH)
    check('ARCH_72B',(NL,H,QH,KVH,HD)==EXPECTED,[NL,H,QH,KVH,HD]);check('FROZEN',all(not p.requires_grad for p in model.parameters()))
    check('NF4_PRESENT',any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
    placements={}
    for p in model.parameters():placements[str(p.device)]=placements.get(str(p.device),0)+p.numel()
    buffers={}
    for b in model.buffers():buffers[str(b.device)]=buffers.get(str(b.device),0)+b.numel()
    RESULT['device_placement']={'parameters':placements,'buffers':buffers}
    check('GPU_ONLY_PARAMETERS',set(placements)=={'cuda:0'},placements)
    check('GPU_ONLY_BUFFERS',all(k=='cuda:0' for k in buffers),buffers)
    RESULT['model_revision']=getattr(cfg,'_commit_hash',None)
    RESULT['quantization']={'type':'nf4','double_quant':True,'compute_dtype':'bfloat16'}
    S0=weight_sentinel();RESULT['weight_sentinel_before']=S0
    SYSTEM='Use the supplied fictional information. Answer the question using the available memory.'
    PREFIX='<|im_start|>system\n'+SYSTEM+'<|im_end|>\n<|im_start|>user\nINFORMATION:\n'
    PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
    # Unique synthetic names; fixed construction, no answer injection or adaptive patches.
    syll1=['Zor','Kel','Tar','Bel','Rav','Nem','Dar','Fer','Lar','Tor','Sel','Mir','Var','Kor','Nar','Der']
    syll2=['van','vek','ren','nor','vik','or','sen','on']
    CAR=[]
    for i in range(max(STAGES)):
        place=syll1[i%16]+syll2[i//16]
        target='City'+f'{i:04d}'+'R'
        fact=f'The current capital of {place} is {target}.'
        ids=tok(PREFIX+fact+'\n\n',add_special_tokens=False).input_ids
        check('PREFIX_'+str(i),ids[:P]==PIDS) if i<2 else None
        if ids[:P]!=PIDS:raise RuntimeError('CANONICAL_PREFIX_'+str(i))
        CAR.append({'place':place,'target':target,'fact':fact,'body':ids[P:],'question':f'What is the current capital of {place}?'})
    TARGETS=[x['target'] for x in CAR]
    RESULT['panel']={'prefix_tokens':P,'cartridges':len(CAR),'body_tokens':[len(x['body']) for x in CAR],'facts':[x['fact'] for x in CAR],'sha256':digest({'prefix_ids':PIDS,'facts':[x['fact'] for x in CAR],'body_ids':[x['body'] for x in CAR]}),'query_selection':'first/middle/last plus 3 seeded indices; fixed per N'}
    log('PANEL_SHA256',RESULT['panel']['sha256']);save()
    for cut in CUTS:
        log('-'*110);log('CUT',cut,'START');run_cut(cut)
    S1=weight_sentinel();RESULT['weight_sentinel_after']=S1;check('WEIGHT_SENTINEL_UNCHANGED',S0==S1)
    RESULT['status']='PASS_PHYSICAL' if all(r['status']=='PASS_PHYSICAL' for r in RESULT['runs']) else 'PARTIAL_OR_FAILED'
except Exception as e:
    RESULT['status']='ERROR';RESULT['error_type']=type(e).__name__;RESULT['error']=str(e);RESULT['traceback']=traceback.format_exc()[-12000:];log('TEST703_ERROR',type(e).__name__,str(e))
finally:
    RESULT['total_seconds']=round(time.perf_counter()-START,3)
    try:RESULT['memory_final']=mem()
    except Exception:pass
    save();log('='*110);log('TEST703_STATUS',RESULT['status'])
    for r in RESULT['runs']:
        log('CUT',r['cut'],'STATUS',r['status'],'STAGES',[(x['count'],x['status'],x.get('accuracy')) for x in r['stages']])
    log('RESULT_JSON',OUT);log('RESULT_LOG',LOG);log('='*110)
