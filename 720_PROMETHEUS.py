# ============================================================================================================
# AKBASCORE PROMETHEUS — TEST720
# LOCKED TEST709 REFERENCE ENGINE vs HOOK-FREE DIRECT CUT3
# Qwen2.5-72B-Instruct / NF4 / BF16 / A100-SXM4-80GB
#
# Reference:
# https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/709.py
# https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/716.py
#
# Google Colab: ONE CELL
# GPU execution has not been verified by the author.
# This test checks FORGE + INITIALIZE parity.
# APPEND / REPHASE parity remains a separate acceptance requirement.
# ============================================================================================================

import os,sys,subprocess,importlib.util,urllib.request,hashlib,ast,json,time,gc,traceback,platform,types
from pathlib import Path
from datetime import datetime,timezone

os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF","expandable_segments:True")

def install_if_missing(module,package):
    if importlib.util.find_spec(module) is None:
        subprocess.check_call([sys.executable,"-m","pip","install","-q",package])

for module,package in [
    ("torch","torch"),
    ("transformers","transformers>=5.18,<6"),
    ("accelerate","accelerate>=1.15"),
    ("bitsandbytes","bitsandbytes>=0.50"),
    ("psutil","psutil")
]:
    install_if_missing(module,package)

import torch,transformers,bitsandbytes,psutil
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
from transformers.cache_utils import DynamicCache

TEST="720"
MODEL_ID="Qwen/Qwen2.5-72B-Instruct"
CUT=3
EXPECTED=(80,8192,64,8,128)
DTYPE=torch.bfloat16
DEV=torch.device("cuda:0")
CHUNK=128
MAX_NEW=48
GPU_RESERVE_GIB=9.0

SRC709="https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/709.py"
SRC716="https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/716.py"

LOCK709="6c9f8cbb1eeed848d45133d73f0d7676b68e9125"
LOCK716="913fa7a4951f2072df4be2eb49120ea86efa5477"

ROOT=Path("/content/AKBASCORE_TEST720" if Path("/content").exists() else "/tmp/AKBASCORE_TEST720")
ROOT.mkdir(parents=True,exist_ok=True)

LOG=ROOT/"TEST720.log"
OUT=ROOT/"TEST720_results.json"
LOG.write_text("",encoding="utf-8")

R={
    "test":TEST,
    "status":"STARTED",
    "model":MODEL_ID,
    "cut":CUT,
    "method":"Locked TEST709 reference hooks versus hook-free direct CUT3 forward",
    "sources":[SRC709,SRC716],
    "checks":[],
    "measurements":{},
    "limitations":[
        "GPU execution not verified by code author",
        "This test checks forge and initialize parity only",
        "Append and RoPE rephase parity require further testing",
        "Direct layer.forward integration is hook-free but not a compiled native CUDA kernel",
        "Greedy answer agreement does not prove semantic correctness"
    ]
}

def log(*items):
    message=" ".join(map(str,items))
    print(message,flush=True)
    with LOG.open("a",encoding="utf-8") as f:
        f.write(message+"\n")

def save():
    temporary=OUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
    temporary.replace(OUT)

def check(name,condition,detail=None):
    ok=bool(condition)
    R["checks"].append({"name":name,"pass":ok,"detail":detail})
    save()
    log("PASS" if ok else "FAIL",name,detail if detail is not None else "")
    if not ok:
        raise RuntimeError("CHECK_FAILED:"+name)

def gitblob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def download(url,limit=300000):
    request=urllib.request.Request(url,headers={"User-Agent":"AKBASCORE-TEST720"})
    with urllib.request.urlopen(request,timeout=120) as f:
        data=f.read(limit+1)
    if len(data)>limit:
        raise RuntimeError("SOURCE_TOO_LARGE")
    return data

def sha(data):
    return hashlib.sha256(data).hexdigest()

def sync():
    torch.cuda.synchronize()

def gpu():
    sync()
    free,total=torch.cuda.mem_get_info()
    return {
        "free_gib":round(free/2**30,3),
        "allocated_gib":round(torch.cuda.memory_allocated()/2**30,3),
        "peak_gib":round(torch.cuda.max_memory_allocated()/2**30,3),
        "total_gib":round(total/2**30,3)
    }

def release():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

# ------------------------------------------------------------------------------------------------------------
# LOCKED TEST709 FUNCTION EXTRACTION
# Original functions are compiled unchanged.
# ------------------------------------------------------------------------------------------------------------

def import_reference(raw):
    names={
        "pairs","cache_build","replace","half","rope","rephase",
        "sentinel","free_gpu","ensure_room","forge_stream",
        "cart_load","initialize","kv_digest","full_kv_seal",
        "append","answer","mem"
    }

    tree=ast.parse(raw.decode("utf-8"))

    found={
        node.name:node
        for node in tree.body
        if isinstance(node,ast.FunctionDef) and node.name in names
    }

    check("ALL_LOCKED_FUNCTIONS_PRESENT",set(found)==names,sorted(names-set(found)))

    module=ast.Module(
        body=[
            node for node in tree.body
            if isinstance(node,ast.FunctionDef) and node.name in names
        ],
        type_ignores=[]
    )

    compiled=compile(ast.fix_missing_locations(module),"709.py","exec")
    exec(compiled,globals())

# ------------------------------------------------------------------------------------------------------------
# HOOK-FREE CUT3 DIRECT FORWARD
# Does not call register_forward_hook.
# The original forward method is restored on exit.
# ------------------------------------------------------------------------------------------------------------

class DirectCut3:
    def __init__(self,layer,mode,collector=None,source=None):
        self.layer=layer
        self.mode=mode
        self.collector=collector
        self.source=source
        self.offset=0
        self.old=None

    def __enter__(self):
        if self.layer._forward_hooks or self.layer._forward_pre_hooks:
            raise RuntimeError("NATIVE_PATH_FORWARD_HOOK_PRESENT")

        self.old=self.layer.forward
        ctx=self

        def direct_forward(this,*args,**kwargs):
            out=ctx.old(*args,**kwargs)
            z=out[0] if isinstance(out,(tuple,list)) else out

            if ctx.mode=="capture":
                ctx.collector.append(
                    z.detach().to("cpu",copy=True).contiguous()
                )
                return out

            if ctx.mode=="inject":
                start=ctx.offset
                target=ctx.source[:,start:start+z.shape[1],:]

                if z.shape!=target.shape:
                    raise RuntimeError(
                        "NATIVE_INJECTION_SHAPE:"
                        +str(tuple(z.shape))
                        +" vs "
                        +str(tuple(target.shape))
                    )

                return replace(out,target)

            raise RuntimeError("UNKNOWN_NATIVE_MODE")

        self.layer.forward=types.MethodType(direct_forward,self.layer)
        return self

    def __exit__(self,exc_type,exc_value,exc_tb):
        self.layer.forward=self.old
        return False

# ------------------------------------------------------------------------------------------------------------
# NATIVE FORGE
# Same input positions, streaming cache and physical cartridge layout as TEST709.
# ------------------------------------------------------------------------------------------------------------

@torch.no_grad()
def forge_native(body_ids,book_id):
    ids=PIDS+body_ids
    n=len(ids)
    cache=None
    h_chunks=[]
    start_time=time.perf_counter()

    with DirectCut3(model.model.layers[CUT],"capture",collector=h_chunks):
        for st in range(0,n,CHUNK):
            piece=ids[st:st+CHUNK]

            ensure_room(len(piece)+512)

            pos=torch.arange(st,st+len(piece),device=DEV)

            out=model(
                input_ids=torch.tensor([piece],device=DEV),
                past_key_values=cache,
                attention_mask=torch.ones(
                    (1,st+len(piece)),device=DEV,dtype=torch.long
                ),
                position_ids=pos.unsqueeze(0),
                cache_position=pos,
                use_cache=True,
                return_dict=True
            )

            cache=out.past_key_values
            del out

    kv=pairs(cache)

    cp={
        "h":torch.cat(h_chunks,dim=1),
        "lower":tuple(
            (
                k.detach().cpu().contiguous(),
                v.detach().cpu().contiguous()
            )
            for k,v in kv[:CUT+1]
        ),
        "n":n,
        "p":P,
        "body_tokens":len(body_ids),
        "book_id":book_id
    }

    check(
        "NATIVE_FORGE_SHAPE",
        cp["h"].shape==(1,n,H) and len(cp["lower"])==CUT+1
    )

    del cache,kv,h_chunks
    release()

    return cp,round(time.perf_counter()-start_time,3)

# ------------------------------------------------------------------------------------------------------------
# NATIVE INITIALIZE
# Reconstruct upper-layer K/V from physical CUT3 H3.
# ------------------------------------------------------------------------------------------------------------

@torch.no_grad()
def initialize_native(cp):
    n=cp["n"]
    h=cp["h"]
    upper=None

    ensure_room(n+512)

    with DirectCut3(model.model.layers[CUT],"inject",source=h) as bridge:
        for st in range(0,n,CHUNK):
            q=min(CHUNK,n-st)

            ensure_room(q+512)

            bridge.offset=st
            pos=torch.arange(st,st+q,device=DEV)

            out=model(
                inputs_embeds=torch.zeros(
                    (1,q,H),device=DEV,dtype=DTYPE
                ),
                past_key_values=upper,
                attention_mask=torch.ones(
                    (1,st+q),device=DEV,dtype=torch.long
                ),
                position_ids=pos.unsqueeze(0),
                cache_position=pos,
                use_cache=True,
                return_dict=True
            )

            upper=out.past_key_values
            del out

    kv=pairs(upper)

    result=cp["lower"]+tuple(
        (k.detach().clone(),v.detach().clone())
        for k,v in kv[CUT+1:]
    )

    check("NATIVE_INIT_80_LAYERS",len(result)==NL)

    del upper,kv
    return result

# ------------------------------------------------------------------------------------------------------------
# CARTRIDGE TRANSFER / SHA256
# ------------------------------------------------------------------------------------------------------------

def to_gpu(cp):
    return {
        "h":cp["h"].to(DEV),
        "lower":tuple(
            (k.to(DEV),v.to(DEV))
            for k,v in cp["lower"]
        ),
        "n":cp["n"],
        "p":cp["p"],
        "body_tokens":cp["body_tokens"],
        "book_id":cp["book_id"]
    }

def tensor_sha_cpu(tensor):
    raw=tensor.detach().contiguous().view(torch.uint8).numpy().tobytes()
    return sha(raw)

def seal_cp(cp):
    return {
        "h":tensor_sha_cpu(cp["h"]),
        "lower":[
            (tensor_sha_cpu(k),tensor_sha_cpu(v))
            for k,v in cp["lower"]
        ]
    }

def memory_seals(memory):
    return [
        (kv_digest(k),kv_digest(v))
        for k,v in memory
    ]

def compare_seals(a,b):
    return len(a)==len(b) and all(x==y for x,y in zip(a,b))

# ------------------------------------------------------------------------------------------------------------
# MAIN EXPERIMENT
# ------------------------------------------------------------------------------------------------------------

try:
    log("="*108)
    log("AKBASCORE PROMETHEUS — TEST720 — LOCKED TEST709 VS HOOK-FREE DIRECT CUT3")
    log("="*108)

    # PREFLIGHT: do not download the 72B model without a usable GPU.
    cuda_available=torch.cuda.is_available()
    check("CUDA_AVAILABLE",cuda_available,{
        "torch":torch.__version__,
        "torch_cuda":torch.version.cuda,
        "visible_devices":os.environ.get("CUDA_VISIBLE_DEVICES","UNSET")
    })

    check("ONE_GPU",torch.cuda.device_count()==1)

    gpu_name=torch.cuda.get_device_name(0)
    gpu_total=torch.cuda.get_device_properties(0).total_memory

    check("A100_80GB",gpu_total>=70*2**30 and "A100" in gpu_name,gpu_name)
    check("RESERVE",GPU_RESERVE_GIB>=9 and 32<=CHUNK<=512)

    log("GPU_PREFLIGHT",gpu())
    log("FETCH_LOCKED_SOURCES")

    raw709=download(SRC709)
    raw716=download(SRC716)

    check("709_GIT_BLOB_LOCK",gitblob(raw709)==LOCK709,gitblob(raw709))
    check("716_GIT_BLOB_LOCK",gitblob(raw716)==LOCK716,gitblob(raw716))

    import_reference(raw709)

    R["environment"]={
        "python":platform.python_version(),
        "torch":torch.__version__,
        "transformers":transformers.__version__,
        "bitsandbytes":bitsandbytes.__version__,
        "gpu":gpu_name,
        "gpu_total_gib":round(gpu_total/2**30,3)
    }
    save()

    # TOKENIZER AND CANONICAL PREFIX
    tok=AutoTokenizer.from_pretrained(
        MODEL_ID,
        trust_remote_code=False
    )

    PREFIX=(
        "<|im_start|>system\n"
        "Use only the available document memory for document-specific questions. "
        "If the evidence is missing, say UNKNOWN.\n"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        "INFORMATION:\n"
    )

    PIDS=tok(PREFIX,add_special_tokens=False).input_ids
    P=len(PIDS)

    # FROZEN 72B NF4
    quant=BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=DTYPE,
        bnb_4bit_use_double_quant=True
    )

    log("LOAD_FROZEN_72B_NF4")

    model=AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=quant,
        dtype=DTYPE,
        device_map={"":0},
        low_cpu_mem_usage=True,
        trust_remote_code=False,
        attn_implementation="sdpa"
    ).eval()

    for parameter in model.parameters():
        parameter.requires_grad_(False)

    cfg=model.config

    NL=len(model.model.layers)
    H=int(cfg.hidden_size)
    QH=int(cfg.num_attention_heads)
    KVH=int(cfg.num_key_value_heads)
    HD=int(getattr(cfg,"head_dim",None) or H//QH)

    check("ARCH",(NL,H,QH,KVH,HD)==EXPECTED,[NL,H,QH,KVH,HD])
    check("FROZEN",all(not p.requires_grad for p in model.parameters()))

    check(
        "NF4",
        any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules())
    )

    check(
        "DIRECT_FORWARD_NO_EXISTING_HOOKS",
        not model.model.layers[CUT]._forward_hooks
        and not model.model.layers[CUT]._forward_pre_hooks
    )

    before=sentinel()
    R["weight_sentinel_before"]=before

    log("MODEL_READY",gpu())

    # DETERMINISTIC TEST BODY
    body=(
        "The controller preserves original evidence cartridges. "
        "Physical memory is reloaded at CUT3. "
        "A synthesis is not a lossless replacement for its source cartridges. "
    )*16

    ids=tok(body,add_special_tokens=False).input_ids
    R["body_tokens"]=len(ids)

    check("MULTICHUNK_BODY",len(PIDS)+len(ids)>CHUNK)

    # --------------------------------------------------------
    # REFERENCE FORGE
    # --------------------------------------------------------

    log("REFERENCE_FORGE",len(ids))

    cp_ref,secs_ref=forge_stream(ids,"T720")
    R["measurements"]["reference_forge_s"]=secs_ref

    ref_seal=seal_cp(cp_ref)

    release()

    # --------------------------------------------------------
    # NATIVE FORGE
    # --------------------------------------------------------

    log("NATIVE_FORGE",len(ids))

    cp_native,secs_native=forge_native(ids,"T720")
    R["measurements"]["native_forge_s"]=secs_native

    native_seal=seal_cp(cp_native)

    check(
        "CAPTURE_H3_EXACT_SHA",
        ref_seal["h"]==native_seal["h"]
    )

    check(
        "CAPTURE_L0_L3_EXACT_SHA",
        ref_seal["lower"]==native_seal["lower"]
    )

    log("FORGE_PARITY_PASS")

    # --------------------------------------------------------
    # REFERENCE INITIALIZE
    # --------------------------------------------------------

    log("REFERENCE_INITIALIZE")

    cp_ref_gpu=to_gpu(cp_ref)
    release()

    start=time.perf_counter()

    mem_ref=initialize(cp_ref_gpu)

    sync()

    R["measurements"]["reference_init_s"]=round(
        time.perf_counter()-start,3
    )

    seals_ref=memory_seals(mem_ref)
    R["measurements"]["reference_gpu"]=gpu()

    del mem_ref,cp_ref_gpu
    release()

    # --------------------------------------------------------
    # NATIVE INITIALIZE
    # --------------------------------------------------------

    log("NATIVE_INITIALIZE")

    cp_native_gpu=to_gpu(cp_native)
    del cp_native
    release()

    start=time.perf_counter()

    mem_native=initialize_native(cp_native_gpu)

    sync()

    R["measurements"]["native_init_s"]=round(
        time.perf_counter()-start,3
    )

    seals_native=memory_seals(mem_native)
    R["measurements"]["native_gpu"]=gpu()

    matched=sum(
        a==b
        for a,b in zip(seals_ref,seals_native)
    )

    check(
        "FULL_80_LAYER_KV_SHA256_EXACT",
        compare_seals(seals_ref,seals_native),
        {"layers":len(seals_native),"matched":matched}
    )

    log("INITIALIZE_PARITY_PASS")

    # --------------------------------------------------------
    # GREEDY ANSWER PARITY
    # --------------------------------------------------------

    question="What is the role of an original evidence cartridge?"

    log("NATIVE_ANSWER")

    answer_native=answer(mem_native,question)
    R["measurements"]["native_answer"]=answer_native

    del mem_native,cp_native_gpu
    release()

    log("REFERENCE_ANSWER")

    cp_ref_gpu=to_gpu(cp_ref)
    release()

    mem_ref=initialize(cp_ref_gpu)

    answer_ref=answer(mem_ref,question)
    R["measurements"]["reference_answer"]=answer_ref

    check(
        "GREEDY_ANSWER_EXACT",
        answer_ref==answer_native,
        {"reference":answer_ref,"native":answer_native}
    )

    del mem_ref,cp_ref_gpu,cp_ref
    release()

    # --------------------------------------------------------
    # MODEL INTEGRITY
    # --------------------------------------------------------

    after=sentinel()

    check("WEIGHTS_SENTINEL_UNCHANGED",after==before)

    R["weight_sentinel_after"]=after
    R["status"]="PASS_NATIVE_CAPTURE_AND_INITIALIZE_PARITY"

    save()

    log("="*108)
    log("TEST720_RESULT",R["status"])
    log("RESULT_JSON",OUT)
    log("RESULT_LOG",LOG)
    log("="*108)

except Exception as error:
    R["status"]="FAIL_OR_ERROR"
    R["error"]=repr(error)
    R["traceback"]=traceback.format_exc()
    save()

    log("TEST720_ERROR",R["traceback"])
    raise

finally:
    save()
