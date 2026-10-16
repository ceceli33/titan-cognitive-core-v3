
# ==========================================================================================================
# AKBASCORE TEST702 — QWEN2.5-72B NF4 · CARTRIDGE CUT CALIBRATION · REVISED
# Independent Colab cell · TEST566-derived checkpoint/init/append/answer
# CUTS 1/3/6 · Frozen weights · BF16 H/KV · RoPE rephase · Upper-layer rebuild
# Independent cartridge forging · Bitwise append guards · Raw answer audit
# No training · No answer patches · No router · No dependency on earlier runtime state
# ==========================================================================================================
import os,sys,time,json,hashlib,traceback,gc,subprocess,importlib.util,random,platform
from pathlib import Path
from datetime import datetime,timezone
for m,p in [("transformers","transformers>=5.18,<6"),("accelerate","accelerate>=1.15"),("bitsandbytes","bitsandbytes>=0.50"),("psutil","psutil")]:
    if importlib.util.find_spec(m) is None:subprocess.check_call([sys.executable,"-m","pip","install","-q",p])
import torch,transformers,accelerate,bitsandbytes,psutil
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache
TEST="702";REVISION="702-R2";SEED=7022026
MODEL_ID="Qwen/Qwen2.5-72B-Instruct"
EXPECTED=(80,8192,64,8,128);CUTS=(1,3,6)
DTYPE=torch.bfloat16;DEVICE=torch.device("cuda:0")
ROOT=Path("/content/AKBASCORE_TEST702");ROOT.mkdir(parents=True,exist_ok=True)
OUT=ROOT/"TEST702_results.json";LOG=ROOT/"TEST702.log"
LOG.write_text("",encoding="utf-8")
random.seed(SEED);torch.manual_seed(SEED)
if torch.cuda.is_available():torch.cuda.manual_seed_all(SEED)
torch.set_grad_enabled(False)
os.environ["TOKENIZERS_PARALLELISM"]="false"
START=time.perf_counter()
RESULT={"test":TEST,"revision":REVISION,"model":MODEL_ID,"status":"STARTED","timestamp":datetime.now(timezone.utc).isoformat(),"seed":SEED,"cuts":list(CUTS),"checks":[],"runs":[]}
def log(*x):
    s=" ".join(str(v) for v in x)
    print(s,flush=True)
    with LOG.open("a",encoding="utf-8") as f:f.write(s+"\n")
def save():
    tmp=OUT.with_suffix(".tmp")
    tmp.write_text(json.dumps(RESULT,indent=2,ensure_ascii=False,default=str),encoding="utf-8")
    tmp.replace(OUT)
def check(name,ok,detail=None):
    ok=bool(ok)
    RESULT["checks"].append({"name":name,"pass":ok,"detail":detail})
    log("PASS" if ok else "FAIL",name,detail if detail is not None else "")
    if not ok:raise RuntimeError("CHECK_FAILED: "+name)
def gib(x):return round(float(x)/2**30,5)
def mem():
    torch.cuda.synchronize()
    free,total=torch.cuda.mem_get_info()
    return {"gpu_free_gib":gib(free),"gpu_total_gib":gib(total),"gpu_allocated_gib":gib(torch.cuda.memory_allocated()),"gpu_reserved_gib":gib(torch.cuda.memory_reserved()),"gpu_peak_allocated_gib":gib(torch.cuda.max_memory_allocated()),"ram_available_gib":gib(psutil.virtual_memory().available)}
def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()
def pairs(cache):
    if hasattr(cache,"layers"):
        return tuple((layer.keys,layer.values) for layer in cache.layers)
    if hasattr(cache,"key_cache") and hasattr(cache,"value_cache"):
        return tuple(zip(cache.key_cache,cache.value_cache))
    if isinstance(cache,(tuple,list)):
        return tuple((x[0],x[1]) for x in cache)
    raise TypeError("UNSUPPORTED_CACHE_TYPE: "+type(cache).__name__)
def clone(cache):
    return tuple((k.detach().clone(),v.detach().clone()) for k,v in pairs(cache))
def cache_build(kvs):
    c=DynamicCache()
    for i,(k,v) in enumerate(kvs):c.update(k,v,i)
    return c
def replace(out,h):
    if isinstance(out,tuple):return (h,)+out[1:]
    if isinstance(out,list):return [h]+out[1:]
    return h
def half(x):
    a,b=x.chunk(2,-1)
    return torch.cat((-b,a),-1)
def rope(pos):
    dummy=torch.zeros((1,len(pos),H),device=DEVICE,dtype=DTYPE)
    cos,sin=model.model.rotary_emb(dummy,pos.unsqueeze(0))
    return cos.unsqueeze(1).float(),sin.unsqueeze(1).float()
def rephase(k,old,new):
    if torch.equal(old,new):return k
    co,so=rope(old);cn,sn=rope(new)
    x=k.float()
    x=x*co-half(x)*so
    return (x*cn+half(x)*sn).to(k.dtype)
def model_devices():
    param_counts={}
    for p in model.parameters():
        d=str(p.device)
        param_counts[d]=param_counts.get(d,0)+p.numel()
    buffer_counts={}
    for b in model.buffers():
        d=str(b.device)
        buffer_counts[d]=buffer_counts.get(d,0)+b.numel()
    return {"parameters":param_counts,"buffers":buffer_counts,"hf_device_map":getattr(model,"hf_device_map",None)}
def weight_sentinel():
    h=hashlib.sha256()
    indices=(0,19,39,59,79)
    tensors=[model.model.layers[i].self_attn.o_proj.weight for i in indices]
    tensors.extend([model.model.norm.weight,model.lm_head.weight])
    for p in tensors:
        a=p.detach().reshape(-1)
        n=a.numel()
        for j in range(16):
            start=j*max(n-256,0)//15
            h.update(a[start:start+256].float().cpu().numpy().tobytes())
    return h.hexdigest()
def forward_ids(ids):
    n=len(ids)
    pos=torch.arange(n,device=DEVICE)
    x=torch.tensor([ids],device=DEVICE,dtype=torch.long)
    return model(input_ids=x,attention_mask=torch.ones((1,n),device=DEVICE,dtype=torch.long),position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
@torch.no_grad()
def checkpoint(ci,cut):
    ids=PIDS+CAR[ci]["body"];n=len(ids);state={}
    def capture(module,args,out):
        state["h"]=(out[0] if isinstance(out,(tuple,list)) else out).detach().clone()
    hook=model.model.layers[cut].register_forward_hook(capture)
    try:
        out=forward_ids(ids)
        kv=clone(out.past_key_values)
        if "h" not in state or state["h"].shape!=(1,n,H):
            raise RuntimeError("CAPTURE_H_SHAPE_CUT"+str(cut))
        if len(kv)!=NL:raise RuntimeError("CHECKPOINT_LAYER_COUNT")
        return {"h":state["h"],"kv":kv,"pos":torch.arange(n,device=DEVICE),"body":n-P}
    finally:hook.remove()
@torch.no_grad()
def init_from_checkpoint(cp,cut):
    n=cp["h"].shape[1]
    def inject(module,args,out):
        current=out[0] if isinstance(out,(tuple,list)) else out
        if current.shape!=cp["h"].shape:raise RuntimeError("INIT_INJECTION_SHAPE")
        return replace(out,cp["h"])
    hook=model.model.layers[cut].register_forward_hook(inject)
    try:
        pos=torch.arange(n,device=DEVICE)
        out=model(inputs_embeds=torch.zeros((1,n,H),device=DEVICE,dtype=DTYPE),
                  attention_mask=torch.ones((1,n),device=DEVICE,dtype=torch.long),
                  position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
        upper=clone(out.past_key_values)
        if len(upper)!=NL:raise RuntimeError("INIT_UPPER_LAYER_COUNT")
        return cp["kv"][:cut+1]+upper[cut+1:]
    finally:hook.remove()
@torch.no_grad()
def append_from_checkpoint(memory,cp,cut):
    oldn=int(memory[0][0].shape[-2]);q=cp["body"]
    pos=torch.arange(oldn,oldn+q,device=DEVICE)
    body=cp["h"][:,P:,:]
    if body.shape!=(1,q,H):raise RuntimeError("BODY_SHAPE")
    def inject(module,args,out):
        current=out[0] if isinstance(out,(tuple,list)) else out
        if current.shape!=body.shape:raise RuntimeError("APPEND_INJECTION_SHAPE")
        return replace(out,body)
    hook=model.model.layers[cut].register_forward_hook(inject)
    try:
        out=model(inputs_embeds=torch.zeros((1,q,H),device=DEVICE,dtype=DTYPE),
                  past_key_values=cache_build(memory),
                  attention_mask=torch.ones((1,oldn+q),device=DEVICE,dtype=torch.long),
                  position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
        grown=list(clone(out.past_key_values))
        for li in range(cut+1):
            ok,ov=memory[li];k,v=cp["kv"][li]
            k=rephase(k[:,:,P:,:],cp["pos"][P:],pos)
            v=v[:,:,P:,:]
            grown[li]=(torch.cat((ok,k),dim=-2),torch.cat((ov,v),dim=-2))
        result=tuple(grown)
        if len(result)!=NL:raise RuntimeError("APPEND_LAYER_COUNT")
        for li,((ok,ov),(nk,nv)) in enumerate(zip(memory,result)):
            if not torch.equal(ok,nk[:,:,:oldn,:]) or not torch.equal(ov,nv[:,:,:oldn,:]):
                raise RuntimeError("APPEND_BITWISE_FAIL_LAYER_"+str(li))
            if nk.shape[-2]!=oldn+q or nv.shape[-2]!=oldn+q:
                raise RuntimeError("CACHE_LENGTH_FAIL_LAYER_"+str(li))
        return result
    finally:hook.remove()
def kv_profile(memory):
    n=int(memory[0][0].shape[-2])
    size=sum(k.numel()*k.element_size()+v.numel()*v.element_size() for k,v in memory)
    return {"layers":len(memory),"tokens":n,"kv_gib":gib(size),"kv_bytes":int(size),"shape":list(memory[0][0].shape)}
def answer(memory,question,max_new=12):
    suffix="\nQUESTION:\n"+question+"\n\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n"
    ids=tok(suffix,add_special_tokens=False).input_ids
    n=memory[0][0].shape[-2]
    pos=torch.arange(n,n+len(ids),device=DEVICE)
    cache=cache_build(memory)
    x=torch.tensor([ids],device=DEVICE,dtype=torch.long)
    out=model(input_ids=x,past_key_values=cache,
              attention_mask=torch.ones((1,n+len(ids)),device=DEVICE,dtype=torch.long),
              position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
    cache=out.past_key_values
    next_id=out.logits[:,-1,:].argmax(-1,keepdim=True)
    gen=[]
    stop={tok.eos_token_id,tok.convert_tokens_to_ids("<|im_end|>")}
    for _ in range(max_new):
        t=int(next_id.item())
        if t in stop:break
        gen.append(t)
        n=cache.get_seq_length()
        pos=torch.tensor([n],device=DEVICE)
        out=model(input_ids=next_id,past_key_values=cache,
                  attention_mask=torch.ones((1,n+1),device=DEVICE,dtype=torch.long),
                  position_ids=pos.unsqueeze(0),cache_position=pos,use_cache=True,return_dict=True)
        cache=out.past_key_values
        next_id=out.logits[:,-1,:].argmax(-1,keepdim=True)
    return tok.decode(gen,skip_special_tokens=True).strip()
def run_cut(cut):
    run={"cut":cut,"status":"STARTED","checks":[],"memory_before":mem()}
    RESULT["runs"].append(run);save()
    def verify(name,ok,detail=None):
        ok=bool(ok)
        run["checks"].append({"name":name,"pass":ok,"detail":detail})
        log("PASS" if ok else "FAIL","CUT"+str(cut),name,detail if detail is not None else "")
        if not ok:raise RuntimeError("CUT"+str(cut)+"_"+name)
    cp0=cp1=memory=grown=None
    try:
        gc.collect();torch.cuda.empty_cache();torch.cuda.reset_peak_memory_stats()
        t0=time.perf_counter()
        cp0=checkpoint(0,cut)
        cp1=checkpoint(1,cut)
        torch.cuda.synchronize()
        run["forge_seconds"]=round(time.perf_counter()-t0,3)
        verify("FORGE_LAYER_COUNT",len(cp0["kv"])==NL and len(cp1["kv"])==NL)
        verify("FORGE_BF16",all(k.dtype==DTYPE and v.dtype==DTYPE for cp in (cp0,cp1) for k,v in cp["kv"]))
        verify("FORGE_H_SHAPE",cp0["h"].shape==(1,P+len(CAR[0]["body"]),H) and cp1["h"].shape==(1,P+len(CAR[1]["body"]),H))
        t0=time.perf_counter()
        memory=init_from_checkpoint(cp0,cut)
        torch.cuda.synchronize()
        run["init_seconds"]=round(time.perf_counter()-t0,3)
        run["initial_profile"]=kv_profile(memory)
        verify("INIT_LENGTH",run["initial_profile"]["tokens"]==P+len(CAR[0]["body"]))
        verify("INIT_LOWER_EXACT",all(torch.equal(memory[i][0],cp0["kv"][i][0]) and torch.equal(memory[i][1],cp0["kv"][i][1]) for i in range(cut+1)))
        upper_equal=[torch.equal(memory[i][0],cp0["kv"][i][0]) and torch.equal(memory[i][1],cp0["kv"][i][1]) for i in range(cut+1,NL)]
        run["upper_reference_equal_layers"]=sum(upper_equal)
        run["upper_reference_total_layers"]=len(upper_equal)
        log("CUT",cut,"UPPER_REFERENCE_EQUAL",sum(upper_equal),"/",len(upper_equal))
        t0=time.perf_counter()
        grown=append_from_checkpoint(memory,cp1,cut)
        torch.cuda.synchronize()
        run["append_seconds"]=round(time.perf_counter()-t0,3)
        run["final_profile"]=kv_profile(grown)
        expected=P+sum(len(c["body"]) for c in CAR)
        verify("APPEND_LENGTH",run["final_profile"]["tokens"]==expected)
        verify("APPEND_LAYER_COUNT",run["final_profile"]["layers"]==NL)
        oldn=memory[0][0].shape[-2]
        verify("APPEND_PRIOR_BITWISE",all(torch.equal(ok,nk[:,:,:oldn,:]) and torch.equal(ov,nv[:,:,:oldn,:]) for (ok,ov),(nk,nv) in zip(memory,grown)))
        newpos=torch.arange(oldn,expected,device=DEVICE)
        verify("APPEND_LOWER_REPHASE_EXACT",all(torch.equal(grown[i][0][:,:,oldn:,:],rephase(cp1["kv"][i][0][:,:,P:,:],cp1["pos"][P:],newpos)) and torch.equal(grown[i][1][:,:,oldn:,:],cp1["kv"][i][1][:,:,P:,:]) for i in range(cut+1)))
        run["answer_capital"]=answer(grown,"What is the current capital of Zorvan?")
        run["answer_largest_city"]=answer(grown,"What is the largest city of Zorvan?")
        run["answer_capital_expected"]="Melket"
        run["answer_largest_city_expected"]="Dravel"
        run["answer_capital_exact"]=run["answer_capital"].strip().casefold()=="melket"
        run["answer_largest_city_exact"]=run["answer_largest_city"].strip().casefold()=="dravel"
        log("CUT",cut,"RAW_CAPITAL",repr(run["answer_capital"]))
        log("CUT",cut,"RAW_LARGEST_CITY",repr(run["answer_largest_city"]))
        log("CUT",cut,"ANSWER_EXACT",run["answer_capital_exact"],run["answer_largest_city_exact"])
        run["gpu_peak_allocated_gib"]=gib(torch.cuda.max_memory_allocated())
        run["status"]="PASS"
    except Exception as e:
        run["status"]="ERROR"
        run["error_type"]=type(e).__name__
        run["error"]=str(e)
        run["traceback"]=traceback.format_exc()[-8000:]
        log("CUT",cut,"ERROR",type(e).__name__,str(e))
        if isinstance(e,torch.cuda.OutOfMemoryError):
            run["status"]="OOM"
    finally:
        try:run["memory_after"]=mem()
        except Exception:pass
        del cp0,cp1,memory,grown
        gc.collect();torch.cuda.empty_cache();save()
    return run
try:
    log("="*110)
    log("AKBASCORE TEST702-R2 — 72B NF4 / CUT CALIBRATION")
    log("="*110)
    check("CUDA_AVAILABLE",torch.cuda.is_available())
    check("SINGLE_GPU",torch.cuda.device_count()==1)
    check("A100_80GB_CLASS",torch.cuda.get_device_properties(0).total_memory>=70*2**30)
    RESULT["hardware"]={"gpu":torch.cuda.get_device_name(0),"before":mem()}
    RESULT["versions"]={"torch":torch.__version__,"transformers":transformers.__version__,"accelerate":accelerate.__version__,"bitsandbytes":bitsandbytes.__version__,"python":platform.python_version()}
    log("LOADING_TOKENIZER")
    tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
    log("LOADING_MODEL_NF4_GPU_ONLY")
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type="nf4",bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
    t0=time.perf_counter()
    model=AutoModelForCausalLM.from_pretrained(MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={"":0},low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation="sdpa").eval()
    for p in model.parameters():p.requires_grad_(False)
    torch.cuda.synchronize()
    RESULT["load_seconds"]=round(time.perf_counter()-t0,3)
    RESULT["memory_after_load"]=mem()
    cfg=model.config
    NL=len(model.model.layers);H=int(cfg.hidden_size);QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads)
    HD=int(getattr(cfg,"head_dim",None) or H//QH)
    check("ARCH_72B",(NL,H,QH,KVH,HD)==EXPECTED,[NL,H,QH,KVH,HD])
    check("FROZEN",all(not p.requires_grad for p in model.parameters()))
    check("NF4_PRESENT",any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
    devices=model_devices()
    RESULT["device_placement"]=devices
    check("GPU_ONLY_PARAMETERS",all(d=="cuda:0" for d in devices["parameters"]),devices["parameters"])
    check("GPU_ONLY_BUFFERS",all(d=="cuda:0" for d in devices["buffers"]),devices["buffers"])
    RESULT["model_revision"]=getattr(cfg,"_commit_hash",None)
    RESULT["quantization"]={"type":"NF4","double_quant":True,"compute_dtype":"bfloat16"}
    S0=weight_sentinel();RESULT["weight_sentinel_before"]=S0
    SYSTEM="Use the supplied fictional information. Answer the question using the available memory."
    PREFIX="<|im_start|>system\n"+SYSTEM+"<|im_end|>\n<|im_start|>user\nINFORMATION:\n"
    PIDS=tok(PREFIX,add_special_tokens=False).input_ids;P=len(PIDS)
    FACTS=["The current capital of Zorvan is Melket.","The largest city of Zorvan is Dravel."]
    CAR=[]
    for fact in FACTS:
        ids=tok(PREFIX+fact+"\n\n",add_special_tokens=False).input_ids
        check("CANONICAL_PREFIX_"+str(len(CAR)),ids[:P]==PIDS)
        CAR.append({"fact":fact,"body":ids[P:]})
    RESULT["panel"]={"prefix_tokens":P,"facts":FACTS,"body_tokens":[len(c["body"]) for c in CAR],"sha256":digest({"prefix":PIDS,"facts":FACTS,"bodies":[c["body"] for c in CAR]})}
    log("PANEL_SHA256",RESULT["panel"]["sha256"])
    for cut in CUTS:
        log("-"*110)
        log("CUT",cut,"START")
        run_cut(cut)
    S1=weight_sentinel()
    RESULT["weight_sentinel_after"]=S1
    check("WEIGHT_SENTINEL_UNCHANGED",S0==S1)
    RESULT["status"]="PASS" if all(r["status"]=="PASS" for r in RESULT["runs"]) else "PARTIAL_OR_FAILED"
except Exception as e:
    RESULT["status"]="ERROR"
    RESULT["error_type"]=type(e).__name__
    RESULT["error"]=str(e)
    RESULT["traceback"]=traceback.format_exc()[-12000:]
    log("TEST702_ERROR",type(e).__name__,str(e))
finally:
    RESULT["total_seconds"]=round(time.perf_counter()-START,3)
    try:RESULT["memory_final"]=mem()
    except Exception:pass
    save()
    log("="*110)
    log("TEST702_STATUS",RESULT["status"])
    for r in RESULT["runs"]:
        log("CUT",r["cut"],"STATUS",r["status"],"CAPITAL",repr(r.get("answer_capital")),"CITY",repr(r.get("answer_largest_city")))
    log("RESULT_JSON",OUT)
    log("RESULT_LOG",LOG)
    log("="*110)
