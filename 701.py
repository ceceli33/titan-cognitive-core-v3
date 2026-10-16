
# AKBASCORE TEST701 — QWEN2.5-72B 4-BIT LOAD / ARCHITECTURE / MEMORY CALIBRATION
import os,sys,time,json,gc,subprocess,importlib.util,traceback
from pathlib import Path
from datetime import datetime,timezone
def ensure(module,package):
    if importlib.util.find_spec(module) is None:
        subprocess.check_call([sys.executable,"-m","pip","install","-q",package])
ensure("transformers","transformers>=4.51,<5")
ensure("accelerate","accelerate>=1.4")
ensure("bitsandbytes","bitsandbytes>=0.45")
import torch,psutil,transformers,accelerate,bitsandbytes
from transformers import AutoTokenizer,AutoModelForCausalLM,BitsAndBytesConfig
TEST="701"
MODEL_ID="Qwen/Qwen2.5-72B-Instruct"
ROOT=Path("/content/AKBASCORE_TEST701")
ROOT.mkdir(parents=True,exist_ok=True)
OUT=ROOT/"TEST701_results.json"
EXPECTED=(80,8192,64,8,128)
def gib(x):return round(float(x)/2**30,4)
def gpu():
    torch.cuda.synchronize()
    free,total=torch.cuda.mem_get_info()
    return dict(free_gib=gib(free),total_gib=gib(total),
                allocated_gib=gib(torch.cuda.memory_allocated()),
                reserved_gib=gib(torch.cuda.memory_reserved()),
                peak_allocated_gib=gib(torch.cuda.max_memory_allocated()))
def ram():
    m=psutil.virtual_memory()
    return dict(total_gib=gib(m.total),available_gib=gib(m.available),
                used_gib=gib(m.used))
def save(data):
    OUT.write_text(json.dumps(data,indent=2,ensure_ascii=False,default=str))
def gate(name,value):
    print(("PASS" if value else "FAIL"),name,flush=True)
    return bool(value)
print("="*110)
print("AKBASCORE TEST701 — QWEN2.5-72B / 4-BIT / A100 80GB")
print("="*110)
assert torch.cuda.is_available(),"CUDA_REQUIRED"
device_name=torch.cuda.get_device_name(0)
vram=torch.cuda.get_device_properties(0).total_memory
print("GPU:",device_name)
print("VRAM_GiB:",gib(vram))
print("TORCH:",torch.__version__)
print("TRANSFORMERS:",transformers.__version__)
print("ACCELERATE:",accelerate.__version__)
print("BITSANDBYTES:",bitsandbytes.__version__)
print("PYTHON:",sys.version.split()[0])
assert vram>=70*2**30,"TEST701_REQUIRES_A100_80GB_CLASS_GPU"
assert torch.cuda.device_count()==1,"SINGLE_GPU_REQUIRED"
torch.cuda.empty_cache()
torch.cuda.reset_peak_memory_stats()
result=dict(test=TEST,model=MODEL_ID,status="STARTED",
            timestamp=datetime.now(timezone.utc).isoformat(),
            hardware=dict(gpu=device_name,vram_gib=gib(vram)),
            versions=dict(torch=torch.__version__,transformers=transformers.__version__,
                          accelerate=accelerate.__version__,bitsandbytes=bitsandbytes.__version__),
            memory_before=dict(gpu=gpu(),ram=ram()))
save(result)
print("-"*110)
print("LOADING TOKENIZER",flush=True)
t0=time.perf_counter()
tokenizer=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
print("TOKENIZER_READY",round(time.perf_counter()-t0,2),"seconds")
print("-"*110)
print("LOADING 72B MODEL IN NF4 4-BIT",flush=True)
print("GPU_ONLY / NO_CPU_OFFLOAD / NO_DISK_OFFLOAD",flush=True)
quant=BitsAndBytesConfig(load_in_4bit=True,
                         bnb_4bit_quant_type="nf4",
                         bnb_4bit_compute_dtype=torch.bfloat16,
                         bnb_4bit_use_double_quant=True)
try:
    t0=time.perf_counter()
    model=AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=quant,
        torch_dtype=torch.bfloat16,
        device_map={"":0},
        low_cpu_mem_usage=True,
        trust_remote_code=False,
        attn_implementation="sdpa"
    )
    torch.cuda.synchronize()
    load_seconds=time.perf_counter()-t0
    model.eval()
    for p in model.parameters():p.requires_grad_(False)
    print("MODEL_LOADED",round(load_seconds,2),"seconds",flush=True)
    result["load_seconds"]=round(load_seconds,3)
    result["memory_after_load"]=dict(gpu=gpu(),ram=ram())
    cfg=model.config
    arch=(int(cfg.num_hidden_layers),int(cfg.hidden_size),
          int(cfg.num_attention_heads),int(cfg.num_key_value_heads),
          int(cfg.head_dim) if getattr(cfg,"head_dim",None) is not None
          else int(cfg.hidden_size//cfg.num_attention_heads))
    result["architecture"]=dict(layers=arch[0],hidden=arch[1],
                                query_heads=arch[2],kv_heads=arch[3],head_dim=arch[4])
    result["architecture_pass"]=gate("ARCHITECTURE_80_8192_64_8_128",arch==EXPECTED)
    result["all_frozen"]=gate("FROZEN_WEIGHTS",all(not p.requires_grad for p in model.parameters()))
    result["gpu_only"]=gate("GPU_ONLY",all(
        str(d) not in ("cpu","disk") for d in model.hf_device_map.values()
    ) if hasattr(model,"hf_device_map") else True)
    result["quantized_4bit"]=gate("4BIT_LINEAR_MODULES",
        any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
    print("-"*110)
    print("RUNNING MINIMAL INFERENCE PROBE",flush=True)
    messages=[{"role":"user","content":"Reply with exactly one word: READY"}]
    prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
    inputs=tokenizer(prompt,return_tensors="pt").to("cuda:0")
    torch.cuda.reset_peak_memory_stats()
    t0=time.perf_counter()
    with torch.inference_mode():
        output=model.generate(**inputs,max_new_tokens=8,do_sample=False,
                              pad_token_id=tokenizer.eos_token_id,
                              use_cache=True)
    torch.cuda.synchronize()
    infer_seconds=time.perf_counter()-t0
    generated=output[0,inputs["input_ids"].shape[-1]:]
    answer=tokenizer.decode(generated,skip_special_tokens=True)
    print("RAW_ANSWER:",repr(answer))
    print("INFERENCE_SECONDS:",round(infer_seconds,3))
    result["inference"]=dict(raw_answer=answer,seconds=round(infer_seconds,3),
                             input_tokens=int(inputs["input_ids"].shape[-1]),
                             output_tokens=int(generated.shape[-1]),
                             memory=gpu())
    result["inference_executed"]=gate("INFERENCE_EXECUTED",generated.numel()>0)
    result["memory_final"]=dict(gpu=gpu(),ram=ram())
    result["status"]="PASS" if all([
        result["architecture_pass"],result["all_frozen"],
        result["gpu_only"],result["quantized_4bit"],
        result["inference_executed"]
    ]) else "FAIL"
except Exception as e:
    result["status"]="ERROR"
    result["error_type"]=type(e).__name__
    result["error"]=str(e)
    result["traceback"]=traceback.format_exc()[-6000:]
    print("TEST701_ERROR:",type(e).__name__,str(e),flush=True)
    try:result["memory_at_error"]=dict(gpu=gpu(),ram=ram())
    except Exception:pass
finally:
    save(result)
    print("="*110)
    print("TEST701_STATUS:",result["status"])
    print("RESULT_FILE:",OUT)
    if "memory_after_load" in result:
        print("GPU_AFTER_LOAD:",result["memory_after_load"]["gpu"])
    print("="*110)
