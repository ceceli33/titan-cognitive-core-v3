# =====================================================================================================================
# AKBASCORE AI TECHNOLOGY — SILICON HIPPOCAMPUS · Qwen2.5-72B-Instruct / CUT3 SCALING STUDY
# Live research demonstration of the TEST709 physical-cartridge engine (candidate v1.5 — NOT a published release)
# single Google Colab cell (3 parts) · NVIDIA A100 80 GB · same working method as the Mistral v1.4 demonstration
# PART 1 / 3 — Qwen72B Engine Initialization and Physical Cartridge Infrastructure
# ---------------------------------------------------------------------------------------------------------------------
# Research line   AKBASCORE Silicon Hippocampus v1.4 — Mistral-7B / CUT6  (released: MAM-1.4-Mistral)
#                 AKBASCORE Silicon Hippocampus — Qwen2.5-72B / CUT3 Scaling Study  (this demonstration; unreleased)
# Engine source   TEST709 = https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/709.py
#                 (the file labels itself "TEST708 / revision 708-R2"; this program calls it TEST709 after its file name)
# Historical      https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/709.log — published evidence of an EARLIER
#                 run. It is kept, verified and offered for download separately; it is never shown as a result of this run.
# ---------------------------------------------------------------------------------------------------------------------
# HOW TO RUN: paste PART 1, PART 2 and PART 3 one below the other into ONE Colab cell and press RUN once. Without any button:
#   [1] verified sources            709.py (git blob lock), LICENSE, published 709.log + 706/707/708.log (historical)
#   [2] system preflight            one NVIDIA A100 80 GB, RAM, disk, Hugging Face cache state of the 72B model
#   [3] frozen model                709.py statements 0–43, unchanged: GPU gates, books, tokenizer, Qwen2.5-72B NF4
#                                   (real download / loading progress bars of transformers are shown in Colab)
#   [4] cartridges                  709.py statements 44–47, unchanged: forge A, B, C and save them with SHA-256
#   [5] live TEST709 protocol       709.py statements 48–58, unchanged: the eleven scripted trials (trial() itself)
#   [6] TEST709 closing checks      709.py statements 59–64 + the engine's own finally block → live engine status
#   [7] no-memory controls          every protocol question asked again WITHOUT memory (answer(None, q))
#   [8] ready memory A+B+C          cart_load → initialize → append → append, exactly as TEST709 trial() mounts
#   [9] live verification           cartridge SHA-256 on disk, weight sentinel, read-only K/V X-ray, verification record
#  [10] figures + downloads         six JPEG figures from THIS run's measurements, logs, manifest, Download-All ZIP
#   → only if every step passed, the Gradio interface opens in READY state. Any failure stops here, is logged with
#     the last successful step, and no interface is presented as a working demonstration.
# Requirements    Google Colab with ONE NVIDIA A100 80 GB GPU (TEST709 gate A100_80GB). First run downloads the
#                 Qwen2.5-72B-Instruct weights (≈145 GB) unless they are already in the Hugging Face cache.
# Status          This demonstration code has NOT been executed on a GPU by its author (CPU simulation only).
# Author/licence  Mustafa Akbaş · AkbasCore AI Teknoloji · Mersin, Türkiye
#                 Copyright © 2026 Mustafa Akbaş · AKBASCORE RESEARCH SOFTWARE LICENSE
#                 https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/LICENSE
#                 Qwen2.5-72B-Instruct and all third-party libraries remain governed by their own licences.
# =====================================================================================================================
import os,sys,re,io,ast,json,time,html,math,shutil,zipfile,hashlib,platform,threading,traceback,subprocess,importlib.util,textwrap,copy
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter,OrderedDict

def _pip(*pk):subprocess.check_call([sys.executable,"-m","pip","install","-q",*pk])
for _m,_p in (("numpy","numpy"),("matplotlib","matplotlib"),("PIL","pillow")):
    if importlib.util.find_spec(_m) is None:_pip(_p)
if importlib.util.find_spec("gradio") is None:
    # gradio must not replace the huggingface_hub that the installed transformers needs
    _hv=None
    try:
        _r=subprocess.run([sys.executable,"-c","import huggingface_hub;print(huggingface_hub.__version__)"],capture_output=True,text=True,timeout=120)
        _hv=_r.stdout.strip() if _r.returncode==0 else None
    except Exception:_hv=None
    try:
        if _hv:_pip("gradio",f"huggingface_hub=={_hv}")
        else:raise RuntimeError("no installed hub")
    except Exception:_pip("gradio")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyBboxPatch,FancyArrowPatch
from matplotlib.lines import Line2D
from PIL import Image
import gradio as gr
os.environ.pop("HF_HUB_DISABLE_PROGRESS_BARS",None)          # keep the real download progress bars visible in Colab

# ---------------------------------------------------------------------------------------------------------------------
# identity, sources and locks
# ---------------------------------------------------------------------------------------------------------------------
APP_TITLE="AKBASCORE AI TECHNOLOGY — SILICON HIPPOCAMPUS · Qwen2.5-72B / CUT3 SCALING STUDY"
APP_SUB="Three physical book cartridges in a frozen 80-layer transformer — TEST709 engine, live session"
APP_SHORT="AKBASCORE Silicon Hippocampus · Qwen2.5-72B CUT3"
VERSION_NOTE="candidate v1.5 — not a published or validated release"
AUTHOR="Mustafa Akbaş";ORG="AkbasCore AI Teknoloji";PLACE="Mersin, Türkiye"
LICENSE_NAME="AKBASCORE RESEARCH SOFTWARE LICENSE";COPYRIGHT="Copyright © 2026 Mustafa Akbaş"
REPO="https://github.com/ceceli33/titan-cognitive-core-v3"
RAW_BASE="https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
URL_LICENSE=REPO+"/blob/main/LICENSE";URL_709=REPO+"/blob/main/709.py";URL_709_LOG=REPO+"/blob/main/709.log"
URL_MISTRAL_RELEASE=REPO+"/releases/tag/MAM-1.4-Mistral";URL_QWEN7_DOI="https://doi.org/10.5281/zenodo.23381336"
# git blob identifiers (git hash-object) of the files this program trusts
LOCKS=OrderedDict([
    ("709.py","6c9f8cbb1eeed848d45133d73f0d7676b68e9125"),    # engine (self-label TEST708-R2)
    ("709.log","0916dfdb496bfe8becea48528b719d0de2241869"),   # historical GPU evidence of an earlier run of the engine
    ("708.log","c55e52a68e4794e4ef4ee0c755b9578927528de3"),   # 708-R1: BF16 digest TypeError
    ("707.log","9917e5ea5d47dfccc27c239f0bf8e3c944ad183b"),   # 10k tokens/book: GPU_SAFETY_STOP
    ("706.log","d49cca5eae92c8b87601bc1f53655fc759282c80"),   # 12k tokens/book: GPU_SAFETY_STOP
    ("LICENSE","9aad4724d1072f9e56486650a9527380c867a53b")])
# exact source markers that split the 709.py try-block into stages (checked to occur exactly once)
STAGE_MARKERS=dict(model="quant=BitsAndBytesConfig(",forge="for b in R['books']:\n",trials="trial('NO_CARTRIDGE'",closing="ck('THREE_CARTRIDGES_ON_DISK'")
EXPECTED_ARCH=(80,8192,64,8,128);EXPECTED_CUT=3;EXPECTED_RESERVE_GIB=9.0
ENGINE_PASS_STATUS="PASS_PHYSICAL_UNSCORED_SEMANTICS"
REQUIRED_ENGINE_CHECKS=("CUDA","SINGLE_GPU","A100_80GB","CONFIG","THREE_BOOKS_HAVE_REQUIRED_TOKENS","ARCH","FROZEN","NF4","GPU_ONLY","KV_ONLY_ESTIMATE_FITS",
                        "CARTRIDGE_LOWER_ONLY_A","CARTRIDGE_LOWER_ONLY_B","CARTRIDGE_LOWER_ONLY_C","SOURCE_FILES_REMOVED","THREE_CARTRIDGES_ON_DISK",
                        "THREE_WAY_RECONSTRUCTION","WEIGHT_SENTINEL_UNCHANGED")
BOOK_COLORS={"A":"#1D4ED8","B":"#BE185D","C":"#B45309"}      # used identically in every figure and in the interface
LOWER_COLOR,UPPER_COLOR,CUT_COLOR="#047857","#6D28D9","#111827"

def utc_now():return datetime.now(timezone.utc).isoformat(timespec="milliseconds")
def local_now():return datetime.now().astimezone().isoformat(timespec="seconds")
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def git_blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def sha_file(p,block=1<<22):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(block),b""):h.update(b)
    return h.hexdigest()
def jsafe(o):
    if isinstance(o,dict):return {str(k):jsafe(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)):return [jsafe(v) for v in o]
    if isinstance(o,(np.floating,)):return float(o)
    if isinstance(o,(np.integer,)):return int(o)
    if isinstance(o,np.ndarray):return jsafe(o.tolist())
    if isinstance(o,Path):return str(o)
    if isinstance(o,float) and (math.isnan(o) or math.isinf(o)):return None
    if isinstance(o,(str,int,float,bool)) or o is None:return o
    return str(o)
def dump_json(path,obj):
    path=Path(path);tmp=path.with_suffix(path.suffix+".tmp");tmp.write_text(json.dumps(jsafe(obj),ensure_ascii=False,indent=2),encoding="utf-8");tmp.replace(path);return path
def gib(b):return b/2**30

# ---------------------------------------------------------------------------------------------------------------------
# demonstration directories and the SEPARATE session log (the engine keeps its own log; 709.log is read-only history)
# ---------------------------------------------------------------------------------------------------------------------
DEMO_ROOT=Path("/content/AKBASCORE_Q72_DEMO") if os.path.isdir("/content") else Path("/tmp/AKBASCORE_Q72_DEMO")
SESSION_ID=datetime.now().astimezone().strftime("Q72S-%Y%m%d-%H%M%S")
SESSION_DIR=DEMO_ROOT/"sessions"/SESSION_ID;EVIDENCE_DIR=DEMO_ROOT/"evidence";FIG_DIR=SESSION_DIR/"figures"
LIVE_DIR=SESSION_DIR/"live_engine";HIST_DIR=SESSION_DIR/"historical_reference_not_this_session"
for _d in (SESSION_DIR,EVIDENCE_DIR,FIG_DIR,LIVE_DIR,HIST_DIR):_d.mkdir(parents=True,exist_ok=True)
SESSION_LOG=SESSION_DIR/"SESSION.log";SESSION_EVENTS=SESSION_DIR/"SESSION_EVENTS.jsonl";FIGURE_LOG=SESSION_DIR/"FIGURE_GENERATION.log"
SESSION_QA=SESSION_DIR/"SESSION_QA.jsonl";VERIFY_FILE=SESSION_DIR/"VERIFICATION_RECORD.json";INIT_FILE=SESSION_DIR/"INITIALIZATION_RECORD.json"
_LOG_LOCK=threading.Lock()
def slog(kind,message="",**data):
    """session log: one human-readable line + one JSON event; never written into the engine log or into 709.log"""
    ev=dict(utc=utc_now(),kind=kind,message=str(message),data=jsafe(data))
    line=f"{ev['utc']} {kind:<18} {message}"+(f" {json.dumps(jsafe(data),ensure_ascii=False)}" if data else "")
    with _LOG_LOCK:
        with SESSION_LOG.open("a",encoding="utf-8") as f:f.write(line+"\n")
        with SESSION_EVENTS.open("a",encoding="utf-8") as f:f.write(json.dumps(ev,ensure_ascii=False)+"\n")
    print(line[:600],flush=True);return ev
def flog(message):
    with _LOG_LOCK:
        with FIGURE_LOG.open("a",encoding="utf-8") as f:f.write(f"{utc_now()} {message}\n")

# ---------------------------------------------------------------------------------------------------------------------
# progress display in the Colab output (one banner per initialization step)
# ---------------------------------------------------------------------------------------------------------------------
INIT=dict(started=time.perf_counter(),steps=[],current=None,last_ok=None,ready=False,failed=None)
INIT_STEPS=OrderedDict([
    ("SOURCES","Verified sources (engine lock, licence, historical logs)"),
    ("PREFLIGHT","System preflight: GPU, RAM, disk, model cache"),
    ("MODEL","Frozen Qwen2.5-72B-Instruct NF4 — TEST709 environment + model stage"),
    ("FORGE","Forge and save cartridges A, B, C — TEST709 forge stage"),
    ("PROTOCOL","Live TEST709 protocol — eleven scripted trials"),
    ("CLOSING","TEST709 closing checks and live engine status"),
    ("CONTROLS","No-memory controls for every protocol question"),
    ("READY_MEMORY","Ready memory A+B+C on the GPU"),
    ("VERIFY","Live verification: disk SHA-256, weight sentinel, K/V X-ray"),
    ("FIGURES","Six research figures and downloadable research artifacts")])
def _gpu_short():
    try:
        g=E["mem"]() if callable(E.get("mem")) else None
        return f"GPU free {g['free_gib']:.2f} GiB · allocated {g['allocated_gib']:.2f} GiB · peak {g['peak_gib']:.2f} GiB" if g else ""
    except Exception:return ""
def step_begin(key):
    i=list(INIT_STEPS).index(key)+1;n=len(INIT_STEPS);INIT["current"]=key
    el=time.perf_counter()-INIT["started"]
    print("\n"+"═"*112+f"\n[{i}/{n}] {INIT_STEPS[key]}\n      started {local_now()} · {el/60:.1f} min since start · {_gpu_short()}\n"+"═"*112,flush=True)
    slog("STEP_START",key,title=INIT_STEPS[key]);return time.perf_counter()
def step_done(key,t0,**info):
    s=round(time.perf_counter()-t0,2);INIT["steps"].append(dict(step=key,title=INIT_STEPS[key],seconds=s,utc=utc_now(),**jsafe(info)));INIT["last_ok"]=key
    print(f"──── ✔ {key} finished in {s/60:.1f} min ({s:.1f} s) · {_gpu_short()}",flush=True)
    slog("STEP_DONE",key,seconds=s,**info)

# ---------------------------------------------------------------------------------------------------------------------
# verified downloads
# ---------------------------------------------------------------------------------------------------------------------
SOURCES={}
def fetch_locked(name,timeout=120):
    """download from the repository, check the git blob against LOCKS, keep a verified copy under evidence/"""
    import urllib.request
    p=EVIDENCE_DIR/name
    if p.is_file() and git_blob(p.read_bytes())==LOCKS[name]:raw=p.read_bytes()
    else:
        req=urllib.request.Request(RAW_BASE+name,headers={"User-Agent":"AKBASCORE-Q72-DEMO"})
        with urllib.request.urlopen(req,timeout=timeout) as f:raw=f.read()
        if git_blob(raw)!=LOCKS[name]:
            raise RuntimeError(f"LOCKED SOURCE CHANGED: {name} git blob {git_blob(raw)} != {LOCKS[name]} — the program stops instead of using an unverified file")
        p.write_bytes(raw)
    SOURCES[name]=dict(bytes=len(raw),git_blob=git_blob(raw),sha256=sha_bytes(raw),url=RAW_BASE+name,local=str(p))
    return raw

# ---------------------------------------------------------------------------------------------------------------------
# system preflight (read-only; the engine repeats its own gates CUDA / SINGLE_GPU / A100_80GB inside stage [3])
# ---------------------------------------------------------------------------------------------------------------------
def model_cache_report(model_id="Qwen/Qwen2.5-72B-Instruct"):
    """which weight shards are already in the local Hugging Face cache, and how many bytes are still to download"""
    rep=dict(model_id=model_id,cache_dir=None,shards=None,cached_shards=None,total_bytes=None,missing_bytes=None,note=None)
    try:
        from huggingface_hub import try_to_load_from_cache
        try:
            from huggingface_hub.constants import HF_HUB_CACHE;rep["cache_dir"]=str(HF_HUB_CACHE)
        except Exception:pass
    except Exception as ex:rep["note"]=f"huggingface_hub not importable: {ex}";return rep
    sizes=None
    try:
        from huggingface_hub import HfApi
        info=HfApi().model_info(model_id,files_metadata=True);sizes={s.rfilename:s.size for s in info.siblings};rep["revision"]=getattr(info,"sha",None)
    except Exception as ex:rep["note"]=f"file sizes not available from the Hub: {type(ex).__name__}"
    idx=try_to_load_from_cache(model_id,"model.safetensors.index.json")
    if isinstance(idx,str):shards=sorted(set(json.loads(Path(idx).read_text())["weight_map"].values()))
    elif sizes:shards=sorted(f for f in sizes if f.endswith(".safetensors"))
    else:return rep
    cached=[s for s in shards if isinstance(try_to_load_from_cache(model_id,s),str)]
    rep.update(shards=len(shards),cached_shards=len(cached))
    if sizes and all(s in sizes for s in shards):
        rep["total_bytes"]=sum(sizes[s] or 0 for s in shards);rep["missing_bytes"]=sum(sizes[s] or 0 for s in shards if s not in cached)
    return rep

def preflight():
    """hardware and storage facts of this runtime; stops early when the run cannot succeed"""
    import torch
    rep=dict(python=platform.python_version(),platform=platform.platform(),torch=torch.__version__)
    rep["cuda"]=torch.cuda.is_available();rep["gpu_count"]=torch.cuda.device_count() if rep["cuda"] else 0
    if rep["cuda"]:
        pr=torch.cuda.get_device_properties(0);rep["gpu"]=torch.cuda.get_device_name(0);rep["gpu_total_gib"]=round(pr.total_memory/2**30,2)
        f,t=torch.cuda.mem_get_info();rep["gpu_free_gib"]=round(f/2**30,2)
    try:
        mi=dict(l.split(":",1) for l in Path("/proc/meminfo").read_text().splitlines() if ":" in l)
        rep["ram_total_gib"]=round(int(mi["MemTotal"].split()[0])/2**20,1);rep["ram_available_gib"]=round(int(mi["MemAvailable"].split()[0])/2**20,1)
    except Exception:pass
    try:
        smi=subprocess.run(["nvidia-smi","--query-gpu=name,memory.total,memory.used,driver_version","--format=csv,noheader"],capture_output=True,text=True,timeout=30)
        rep["nvidia_smi"]=smi.stdout.strip()
    except Exception:rep["nvidia_smi"]=None
    rep["model_cache"]=model_cache_report()
    cd=rep["model_cache"].get("cache_dir") or str(Path.home()/".cache"/"huggingface"/"hub");Path(cd).mkdir(parents=True,exist_ok=True)
    rep["cache_disk_free_gib"]=round(shutil.disk_usage(cd).free/2**30,1);rep["demo_disk_free_gib"]=round(shutil.disk_usage(DEMO_ROOT).free/2**30,1)
    mc=rep["model_cache"]
    if mc.get("shards"):
        state="FULLY CACHED — no download needed" if mc["cached_shards"]==mc["shards"] else ("NOT CACHED — full download" if mc["cached_shards"]==0 else "PARTIALLY CACHED")
        extra=f" · {gib(mc['missing_bytes']):.1f} GiB still to download" if mc.get("missing_bytes") is not None else ""
        rep["model_cache_state"]=f"{state}: {mc['cached_shards']}/{mc['shards']} weight shards in {mc.get('cache_dir')}{extra}"
    else:rep["model_cache_state"]="cache state could not be determined ("+str(mc.get("note"))+")"
    print("  GPU        ",rep.get("gpu"),f"· total {rep.get('gpu_total_gib')} GiB · free {rep.get('gpu_free_gib')} GiB · count {rep['gpu_count']}",flush=True)
    print("  nvidia-smi ",rep.get("nvidia_smi"),flush=True)
    print("  RAM        ",f"{rep.get('ram_available_gib')} / {rep.get('ram_total_gib')} GiB available",flush=True)
    print("  disk       ",f"{rep['cache_disk_free_gib']} GiB free for the model cache · {rep['demo_disk_free_gib']} GiB free for the demonstration",flush=True)
    print("  model      ",rep["model_cache_state"],flush=True)
    if not rep["cuda"]:raise RuntimeError("PREFLIGHT: CUDA is not available — select a GPU runtime (A100 80 GB)")
    if rep["gpu_count"]!=1:raise RuntimeError(f"PREFLIGHT: exactly one GPU is required by TEST709, found {rep['gpu_count']}")
    if rep["gpu_total_gib"]<70:raise RuntimeError(f"PREFLIGHT: TEST709 requires an A100 80 GB (≥70 GiB); this GPU has {rep['gpu_total_gib']} GiB ({rep.get('gpu')})")
    if mc.get("missing_bytes") is not None and shutil.disk_usage(cd).free<mc["missing_bytes"]+8*2**30:
        raise RuntimeError(f"PREFLIGHT: not enough disk for the model download: need {gib(mc['missing_bytes'])+8:.1f} GiB, free {rep['cache_disk_free_gib']} GiB")
    if shutil.disk_usage(DEMO_ROOT).free<4*2**30:raise RuntimeError("PREFLIGHT: less than 4 GiB free for cartridges, logs and figures")
    dump_json(SESSION_DIR/"PREFLIGHT.json",rep);return rep

# ---------------------------------------------------------------------------------------------------------------------
# THE TEST709 ENGINE — executed unchanged from its verified source in its own namespace E
# ---------------------------------------------------------------------------------------------------------------------
E={"__name__":"akbascore_test709_engine","__file__":"709.py"}
ENGINE=dict(source_loaded=False,defined=False,model_ready=False,forged=False,protocol_done=False,closed=False,finished=False,error=None,stage_seconds={},engine_log_offset=0)
ENGINE_LOCK=threading.RLock()
_SEG={}

def _src(s,n):return ast.get_source_segment(s,n)
def load_engine_source():
    """fetch 709.py, check its blob, split it by syntax tree into the module part, the try-block stages and the
    engine's own except/finally blocks (all executed verbatim from the verified source, never retyped)"""
    raw=fetch_locked("709.py");s=raw.decode("utf-8");t=ast.parse(s)
    tries=[n for n in t.body if isinstance(n,ast.Try)]
    if len(tries)!=1:raise RuntimeError("TEST709 STRUCTURE: expected exactly one module-level try block")
    tr=tries[0];k=t.body.index(tr);body=tr.body;srcs=[_src(s,n) or "" for n in body]
    if len(tr.handlers)!=1 or tr.handlers[0].name!="e" or not tr.finalbody:raise RuntimeError("TEST709 STRUCTURE: except/finally")
    def first(prefix,contains=None):
        hits=[i for i,x in enumerate(srcs) if x.startswith(prefix) and (contains is None or contains in x)]
        if len(hits)!=1:raise RuntimeError(f"TEST709 STRUCTURE: marker {prefix!r} found {len(hits)} times")
        return hits[0]
    i_model=first(STAGE_MARKERS["model"]);i_forge=first(STAGE_MARKERS["forge"],"forge_stream(");i_trials=first(STAGE_MARKERS["trials"]);i_close=first(STAGE_MARKERS["closing"])
    if not (0<i_model<i_forge<i_trials<i_close):raise RuntimeError("TEST709 STRUCTURE: stage order")
    if "SOURCE_FILES_REMOVED" not in srcs[i_trials-1]:raise RuntimeError("TEST709 STRUCTURE: forge stage must end with SOURCE_FILES_REMOVED")
    if not srcs[-1].startswith("R['status']="):raise RuntimeError("TEST709 STRUCTURE: closing stage must end with the status assignment")
    trials=[]
    for n in body[i_trials:i_close]:
        c=n.value if isinstance(n,ast.Expr) else None
        if not (isinstance(c,ast.Call) and getattr(c.func,"id","")=="trial" and len(c.args)==3):raise RuntimeError("TEST709 STRUCTURE: scripted trial")
        trials.append(dict(label=ast.literal_eval(c.args[0]),books=list(ast.literal_eval(c.args[1])),questions=list(ast.literal_eval(c.args[2]))))
    M=lambda nodes:ast.Module(body=list(nodes),type_ignores=[])
    _SEG.update(source=s,module=M(t.body[:k]),stage_env_model=M(body[:i_forge]),stage_forge=M(body[i_forge:i_trials]),
                stage_trials=M(body[i_trials:i_close]),stage_closing=M(body[i_close:]),stage_except=M(tr.handlers[0].body),stage_finally=M(tr.finalbody),
                trials=trials,index=dict(module_nodes=k,try_statements=len(body),model_from=i_model,forge_from=i_forge,trials_from=i_trials,closing_from=i_close))
    ENGINE["source_loaded"]=True;ENGINE["index"]=_SEG["index"];ENGINE["scripted_trials"]=[x["label"] for x in trials]
    ENGINE["expected_protocol_appends"]=sum(max(0,len(x["books"])-1) for x in trials)
    slog("ENGINE_SOURCE","709.py verified and split",blob=SOURCES["709.py"]["git_blob"],sha256=SOURCES["709.py"]["sha256"],index=_SEG["index"],trials=ENGINE["scripted_trials"])
    return _SEG

def _exec_stage(name,module):
    t=time.perf_counter()
    try:exec(compile(module,f"TEST709_{name}.py","exec"),E)
    finally:ENGINE["stage_seconds"][name]=round(time.perf_counter()-t,2)

def define_engine():
    """709.py module part (imports, constants, R record, all engine functions) — executed unchanged.
    It creates the engine's own run directory /content/AKBASCORE_TEST708 and its own TEST708.log: the LIVE engine log of
    THIS session (the published 709.log is a different, historical file and stays untouched)."""
    with ENGINE_LOCK:
        if ENGINE["defined"]:return
        if not ENGINE["source_loaded"]:load_engine_source()
        _exec_stage("module",_SEG["module"])
        for name in ("forge_stream","cart_load","initialize","append","answer","trial","sentinel","ensure_room","mem","free_gpu","kv_digest","rephase","ck","log","save"):
            if not callable(E.get(name)):raise RuntimeError("TEST709 FUNCTION MISSING: "+name)
        if (E.get("MODEL_ID"),E.get("CUT"),tuple(E.get("EXPECTED",()))) != ("Qwen/Qwen2.5-72B-Instruct",EXPECTED_CUT,EXPECTED_ARCH):raise RuntimeError("TEST709 CONSTANTS CHANGED")
        if float(E.get("GPU_RESERVE_GIB",0))<EXPECTED_RESERVE_GIB:
            raise RuntimeError(f"GPU SAFETY RESERVE REDUCED: {E.get('GPU_RESERVE_GIB')} GiB < {EXPECTED_RESERVE_GIB} GiB (environment AKBASCORE_GPU_RESERVE_GIB) — refused")
        ENGINE["defined"]=True
        slog("ENGINE_DEFINED","709.py module part executed",model=E["MODEL_ID"],cut=E["CUT"],tokens_per_book=E["TOKENS_PER_BOOK"],chunk=E["CHUNK"],reserve_gib=E["GPU_RESERVE_GIB"],max_new=E["MAX_NEW"],engine_root=str(E["ROOT"]),engine_log=str(E["LOG"]))

def engine_log_text():
    try:return Path(E["LOG"]).read_text(encoding="utf-8",errors="replace")
    except Exception:return ""
def engine_log_new_lines():
    """lines appended to the engine's own run log since the last call (read-only)"""
    txt=engine_log_text();new=txt[ENGINE["engine_log_offset"]:];ENGINE["engine_log_offset"]=len(txt);return [x for x in new.splitlines() if x.strip()]

def engine_checks():
    try:return [dict(c) for c in E["R"]["checks"]]
    except Exception:return []

def _engine_stage(name,module,flag,title):
    """one verbatim TEST709 stage; on error the engine's OWN except + finally blocks run (R['status']='ERROR', traceback,
    TEST708_STATUS line in the live engine log) and the error is re-raised — never hidden"""
    with ENGINE_LOCK:
        slog("ENGINE_STAGE_START",title,stage=name,gpu=_gpu_short())
        try:_exec_stage(name,module)
        except BaseException as ex:
            ENGINE["error"]=f"{type(ex).__name__}: {ex}";engine_fail(ex)
            slog("ENGINE_STAGE_FAILED",title,stage=name,error=ENGINE["error"],engine_log=engine_log_new_lines()[-25:]);raise
        ENGINE[flag]=True
        slog("ENGINE_STAGE_DONE",title,stage=name,seconds=ENGINE["stage_seconds"][name],gpu=_gpu_short(),engine_log=engine_log_new_lines()[-10:])

def engine_fail(ex):
    """execute 709.py's own except block (needs the name e) and finally block, exactly once"""
    if ENGINE["finished"]:return
    E["e"]=ex
    try:_exec_stage("except",_SEG["stage_except"])
    except BaseException as ex2:slog("ENGINE_EXCEPT_BLOCK_ERROR",f"{type(ex2).__name__}: {ex2}")
    engine_finish()
def engine_finish():
    """execute 709.py's own finally block (elapsed time, final GPU state, results JSON, TEST708_STATUS line), exactly once"""
    if ENGINE["finished"]:return
    try:_exec_stage("finally",_SEG["stage_finally"])
    finally:ENGINE["finished"]=True

def load_model_stage():
    """709.py try-block statements 0–43: GPU gates, book sources (Gutenberg), tokenizer, frozen 72B NF4 model,
    architecture / frozen / NF4 / GPU-only gates, weight sentinel, instruction prefix and capacity budget"""
    define_engine();_engine_stage("env_model",_SEG["stage_env_model"],"model_ready","environment + frozen model (709.py statements 0–43)")
    return dict(model_load_s=E["R"].get("model_load_s"),arch=[E["NL"],E["H"],E["QH"],E["KVH"],E["HD"]],prefix_tokens=E["P"],budget=E["R"].get("budget"),
                model_revision=E["R"].get("model_revision"),env=E["R"].get("env"))
def forge_stage():
    """709.py try-block statements 44–47: forge A, B, C (streaming prefill of a 10,000-token excerpt each), save each
    CUT3 cartridge to disk with SHA-256, delete the source texts. Cartridges are always forged anew in this session;
    files from earlier runs are overwritten and never used without the SHA-256 recorded now."""
    if not ENGINE["model_ready"]:raise RuntimeError("model stage has not completed")
    _engine_stage("forge",_SEG["stage_forge"],"forged","forge and save cartridges (709.py statements 44–47)")
    return [{k:b.get(k) for k in ("id","title","source_sha256","total_source_tokens","requested_tokens","forge_seconds","cartridge_file_bytes","cartridge_sha256","tensor_bytes")} for b in E["R"]["books"]]
def protocol_stage():
    """709.py try-block statements 48–58: the eleven scripted TEST709 trials, executed by TEST709 trial() itself"""
    if not ENGINE["forged"]:raise RuntimeError("forge stage has not completed")
    _engine_stage("trials",_SEG["stage_trials"],"protocol_done","scripted TEST709 protocol (709.py statements 48–58)")
    ENGINE["protocol_append_pass_lines"]=[l for l in engine_log_text().splitlines() if l.startswith("PASS APPEND_ALL_80_LAYERS_EXACT_SHA256")]
    return [dict(label=t["label"],cache_tokens=t["cache_tokens"],seconds=t["seconds"]) for t in E["R"]["trials"]]
def closing_stage():
    """709.py try-block statements 59–64 (cartridges on disk, three-way reconstruction, weight sentinel, status) followed
    by the engine's own finally block. The live engine status is whatever the engine itself wrote into R['status']."""
    if not ENGINE["protocol_done"]:raise RuntimeError("protocol stage has not completed")
    _engine_stage("closing",_SEG["stage_closing"],"closed","TEST709 closing checks (709.py statements 59–64)")
    engine_finish()
    return dict(status=E["R"].get("status"),elapsed_s=E["R"].get("elapsed_s"),checks=len(E["R"]["checks"]),failed=[c["name"] for c in E["R"]["checks"] if not c["pass"]])

def engine_architecture():
    """architecture values as measured by the engine in this session (None before the model is loaded)"""
    if not ENGINE["model_ready"]:return None
    NL,H,QH,KVH,HD=(E[x] for x in ("NL","H","QH","KVH","HD"))
    return dict(layers=NL,hidden=H,q_heads=QH,kv_heads=KVH,head_dim=HD,cut=E["CUT"],lower_layers=E["CUT"]+1,upper_layers=NL-E["CUT"]-1,
                prefix_tokens=E["P"],full_kv_bytes_per_token=NL*KVH*HD*2*2,max_new=E["MAX_NEW"],chunk=E["CHUNK"],reserve_gib=E["GPU_RESERVE_GIB"],
                weights="NF4 4-bit (bitsandbytes), BF16 compute, frozen",model_id=E["MODEL_ID"])

# ---------------------------------------------------------------------------------------------------------------------
# interactive memory state (exclusively owned; TEST709 append() requires an owned list and releases it)
# ---------------------------------------------------------------------------------------------------------------------
STATE=dict(memory=None,order=[],stages=[],qa=[],controls=[],xray=None,ops=[],weight_checks=[],disk_checks=[],verification=None)
SESSION_INFO=dict(session_id=SESSION_ID,started_utc=utc_now(),started_local=local_now(),python=platform.python_version(),platform=platform.platform())
slog("SESSION_START",APP_SHORT,session=SESSION_ID,version_note=VERSION_NOTE,session_dir=str(SESSION_DIR))
# =====================================================================================================================
# ===== PART 2/3 — paste directly after PART 1 in the same cell =====
# PART 2 / 3 — Cartridge Operations, Memory Consolidation, Integrity and Research Figures
# Every memory operation calls the TEST709 engine functions (E["cart_load"], E["initialize"], E["append"], E["answer"],
# E["sentinel"], E["ensure_room"]) in the order used by TEST709 trial(). Nothing here changes CUT3, RoPE re-phasing, the
# cartridge format, the K/V layout, the SHA-256 guards or the GPU reserve. Measurements are read-only.
# All live values come from this session's engine record E["R"], its live engine log and this session's measurements.
# The published 709.log is parsed ONLY for the separately labelled historical reference.
# =====================================================================================================================
COMBOS=["A+B+C","A+C+B","B+A+C","B+C+A","C+A+B","C+B+A","A+B","B+A","A+C","C+A","B+C","C+B","A","B","C"]
def combo_books(c):return [x for x in str(c).split("+") if x]

class OpError(RuntimeError):pass
def _torch():return E["torch"]
def gpu_now():
    try:return E["mem"]()
    except Exception as ex:return {"error":f"{type(ex).__name__}: {ex}"}
def _append_pass_count():return sum(1 for l in engine_log_text().splitlines() if l.startswith("PASS APPEND_ALL_80_LAYERS_EXACT_SHA256"))

def _require(forged=True):
    if not ENGINE["model_ready"]:raise OpError("The frozen model is not loaded in this session.")
    if forged and not ENGINE["forged"]:raise OpError("The cartridges have not been forged in this session.")

def _drop_memory(reason):
    """release the interactive memory; the list is exclusively owned by STATE"""
    had=STATE["memory"] is not None
    STATE["memory"]=None;STATE["order"]=[];STATE["stages"]=[]
    try:E["free_gpu"]()
    except Exception:pass
    if had:slog("MEMORY_RELEASED",reason,gpu=gpu_now())

def _mount_one(bid,label):
    """one TEST709 trial() stage, step for step (709.py lines 221–225): cart_load → initialize|append → release →
    synchronize → timing fields. On any error the partially consumed memory is discarded (append() has already
    released the caller's references), the GPU is freed and the error is reported — never hidden."""
    torch=_torch();memory=STATE["memory"];n0=_append_pass_count()
    cp,times=E["cart_load"](bid);t0=time.perf_counter()
    new=list(E["initialize"](cp)) if memory is None else E["append"](memory,cp)
    del memory;STATE["memory"]=new;del new,cp;E["free_gpu"]();torch.cuda.synchronize()
    times["rebuild_ms"]=round((time.perf_counter()-t0)*1000,3);times["end_to_end_ms"]=round(times["ssd_load_ms"]+times["h2d_ms"]+times["rebuild_ms"],3)
    times["book"]=bid;times["cache_tokens"]=int(STATE["memory"][0][0].shape[-2]);times["gpu"]=E["mem"]()
    times["operation"]="initialize" if not STATE["order"] else "append";times["label"]=label;times["utc"]=utc_now()
    # evidence, not assumption: the engine wrote one new 'PASS APPEND_ALL_80_LAYERS_EXACT_SHA256' line for this append
    times["prior_kv_sha256_pass_line"]=(_append_pass_count()==n0+1) if times["operation"]=="append" else None
    STATE["order"].append(bid);STATE["stages"].append(times);STATE["ops"].append(dict(times))
    slog("HOT_SWAP_TIMING",f"{label} {bid}",**times)
    return times

def _guard_order(books):
    if not books:raise OpError("Select at least one cartridge.")
    if len(set(books))!=len(books):raise OpError("A cartridge can be mounted only once in a memory.")
    if any(b not in ("A","B","C") for b in books):raise OpError("Unknown cartridge.")
    if len(books)>3:raise OpError("At most three cartridges (TEST709 capacity budget).")

def build_memory(books,label=None):
    """build a new memory from SSD in the given order (TEST709: each memory starts from an empty memory).
    TEST709 memory is append-only, so changing the selection always means release + rebuild."""
    with ENGINE_LOCK:
        _require();_guard_order(books);label=label or "SESSION_"+"_PLUS_".join(books)
        _drop_memory("new build requested");slog("BUILD_START",label,order=books,gpu=gpu_now())
        try:
            for bid in books:_mount_one(bid,label)
        except BaseException as ex:
            _drop_memory(f"build failed: {type(ex).__name__}")
            slog("BUILD_FAILED",label,error=f"{type(ex).__name__}: {ex}",engine_log=engine_log_new_lines()[-15:]);raise
        slog("BUILD_DONE",label,order=STATE["order"],cache_tokens=STATE["stages"][-1]["cache_tokens"],engine_log=engine_log_new_lines()[-15:])
        return list(STATE["stages"])

def release_memory():
    with ENGINE_LOCK:_drop_memory("release requested");return gpu_now()

def ask(question,use_memory=True,origin="user"):
    """question answering exactly as TEST709 trial(): ensure_room(512) then answer(memory, question).
    use_memory=False asks the same frozen model with NO memory (the TEST709 NO_CARTRIDGE path) as a control."""
    with ENGINE_LOCK:
        _require(forged=use_memory)
        q=(question or "").strip()
        if not q or len(q)>2000:raise OpError("The question must contain 1–2000 characters.")
        if use_memory and STATE["memory"] is None:raise OpError("No cartridge memory is mounted.")
        E["ensure_room"](512);t=time.perf_counter()
        raw=E["answer"](STATE["memory"] if use_memory else None,q)
        row=dict(utc=utc_now(),origin=origin,question=q,raw=raw,memory_order=list(STATE["order"]) if use_memory else [],with_memory=bool(use_memory),
                 cache_tokens=(int(STATE["memory"][0][0].shape[-2]) if (use_memory and STATE["memory"] is not None) else 0),
                 seconds=round(time.perf_counter()-t,3),gpu=E["mem"](),max_new_tokens=E["MAX_NEW"],semantics="UNSCORED")
        (STATE["qa"] if use_memory else STATE["controls"]).append(row)
        with SESSION_QA.open("a",encoding="utf-8") as f:f.write(json.dumps(jsafe(row),ensure_ascii=False)+"\n")
        slog("QA" if use_memory else "QA_CONTROL",f"{'+'.join(row['memory_order']) or 'NO MEMORY'}",question=q,raw=raw,seconds=row["seconds"],origin=origin)
        return row

def protocol_questions():
    seen=[]
    for t in _SEG["trials"]:
        for q in t["questions"]:
            if q not in seen:seen.append(q)
    return seen
def run_controls():
    """every scripted protocol question asked again with NO memory — same frozen model, same decoding"""
    _drop_memory("controls run without memory")
    qs=protocol_questions()
    for i,q in enumerate(qs,1):
        r=ask(q,False,origin="initialization control");print(f"  control {i}/{len(qs)} · {r['seconds']:.1f} s · {q[:70]!r} → {r['raw'][:90]!r}",flush=True)
    return dict(questions=len(qs))

# ---------------------------------------------------------------------------------------------------------------------
# live integrity checks
# ---------------------------------------------------------------------------------------------------------------------
def verify_weights():
    """weight sentinel of the engine (709.py sentinel(): sampled bytes of 5 o_proj + norm + lm_head) recomputed now and
    compared with R['weight_sentinel_before'] taken right after loading — read-only, R is not modified"""
    with ENGINE_LOCK:
        _require(forged=False);t=time.perf_counter()
        after=E["sentinel"]();before=E["R"].get("weight_sentinel_before")
        row=dict(utc=utc_now(),passed=(before is not None and after==before),before=before,after=after,seconds=round(time.perf_counter()-t,2))
        STATE["weight_checks"].append(row);slog("WEIGHT_CHECK","PASS" if row["passed"] else "FAIL",**row);return row

def verify_disk():
    """recompute SHA-256 of the three cartridge files and compare with the values the engine recorded when it saved
    them in this session"""
    with ENGINE_LOCK:
        _require();rows=[];t=time.perf_counter()
        for b in E["R"]["books"]:
            p=Path(E["CART"])/(b["id"]+".pt");h=sha_file(p) if p.is_file() else None
            rows.append(dict(book=b["id"],file=str(p),bytes=(p.stat().st_size if p.is_file() else None),sha256=h,engine_record_sha256=b.get("cartridge_sha256"),equals_engine_record=(h is not None and h==b.get("cartridge_sha256"))))
        row=dict(utc=utc_now(),files=rows,passed=(len(rows)==3 and all(r["equals_engine_record"] for r in rows)),seconds=round(time.perf_counter()-t,2))
        STATE["disk_checks"].append(row);slog("DISK_CHECK","PASS" if row["passed"] else "FAIL",**row);return row

# ---------------------------------------------------------------------------------------------------------------------
# READ-ONLY memory X-ray of the live GPU K/V tensors (required for Figure 4 — no synthetic heat map is ever drawn)
# ---------------------------------------------------------------------------------------------------------------------
def xray_measure(bin_tokens=256,chunk=4096):
    """per layer and per token bin: mean over KV heads of the L2 norm of each K and V row of the live memory.
    Reads the tensors in small FP32 chunks; never writes to them; keeps no reference after returning."""
    with ENGINE_LOCK:
        _require()
        if STATE["memory"] is None:raise OpError("No memory is mounted.")
        torch=_torch();E["ensure_room"](0);t=time.perf_counter();mem_=STATE["memory"]
        T=int(mem_[0][0].shape[-2]);NL=len(mem_);nb=(T+bin_tokens-1)//bin_tokens
        Kb=np.zeros((NL,nb),dtype=np.float64);Vb=np.zeros((NL,nb),dtype=np.float64)
        with torch.no_grad():
            for li,(k,v) in enumerate(mem_):
                for arr,out in ((k,Kb),(v,Vb)):
                    rows=[]
                    for st in range(0,T,chunk):rows.append(arr[0,:,st:st+chunk,:].float().norm(dim=-1).mean(dim=0).cpu().numpy())
                    r=np.concatenate(rows);pad=nb*bin_tokens-T
                    if pad:r=np.concatenate([r,np.full(pad,np.nan)])
                    out[li]=np.nanmean(r.reshape(nb,bin_tokens),axis=1)
        del mem_
        segs=[];a=0
        for s in STATE["stages"]:segs.append(dict(book=s["book"],start=a,end=s["cache_tokens"]));a=s["cache_tokens"]
        x=dict(utc=utc_now(),order=list(STATE["order"]),tokens=T,layers=NL,kv_heads=E["KVH"],bin_tokens=bin_tokens,cut=E["CUT"],prefix_tokens=E["P"],segments=segs,
               k_norm=Kb.round(5).tolist(),v_norm=Vb.round(5).tolist(),finite=bool(np.isfinite(Kb).all() and np.isfinite(Vb).all()),
               seconds=round(time.perf_counter()-t,2),gpu=E["mem"](),
               method=f"mean over {E['KVH']} KV heads of the L2 norm per K/V row; mean per bin of {bin_tokens} tokens; FP32 copies of {chunk}-row chunks; read-only")
        STATE["xray"]=x;dump_json(SESSION_DIR/"XRAY_MEASUREMENT.json",x)
        slog("XRAY_MEASURED","+".join(x["order"]),tokens=T,bins=nb,finite=x["finite"],seconds=x["seconds"]);return x

# ---------------------------------------------------------------------------------------------------------------------
# historical reference only: the published 709.log (earlier run) and 706/707/708.log — never shown as live results
# ---------------------------------------------------------------------------------------------------------------------
def _split_qa(rest):
    """'<repr question> -> <repr answer>' with possible ' -> ' inside the strings"""
    for m in re.finditer(r" -> ",rest):
        a,b=rest[:m.start()],rest[m.end():]
        try:return ast.literal_eval(a),ast.literal_eval(b)
        except Exception:continue
    return None,None
def parse_709_log(txt):
    L=dict(checks=[],saved={},trials=OrderedDict(),appends=0,status=None)
    for line in txt.splitlines():
        for name in re.findall(r"\bPASS ([A-Z0-9_]+)",line):L["checks"].append(name)
        m=re.match(r"SAVED (\w) FILE_BYTES (\d+) SHA256 ([0-9a-f]{64})",line)
        if m:L["saved"][m.group(1)]=dict(bytes=int(m.group(2)),sha256=m.group(3));continue
        m=re.match(r"HOT_SWAP_TIMING (\S+) (\w) (\{.*\})$",line)
        if m:L["trials"].setdefault(m.group(1),dict(stages=[],qa=[]))["stages"].append(ast.literal_eval(m.group(3)));continue
        m=re.match(r"QA (\S+) (.*)$",line)
        if m:
            q,a=_split_qa(m.group(2))
            if q is not None:L["trials"].setdefault(m.group(1),dict(stages=[],qa=[]))["qa"].append(dict(question=q,raw=a))
            continue
        if line.startswith("PASS APPEND_ALL_80_LAYERS_EXACT_SHA256"):L["appends"]+=1
        m=re.match(r"TEST\d+_STATUS (\S+)",line)
        if m:L["status"]=m.group(1)
    return L
def parse_failure_log(name,txt):
    st=re.search(r"TEST(\d+)_STATUS (\S+)",txt);err=re.search(r"^ERROR (\w+) (.*)$",txt,re.M)
    forg=re.search(r"FORGING A TOKENS (\d+)",txt);head=re.search(r"AKBASCORE (TEST\S+)",txt)
    return dict(file=name,label=(head.group(1) if head else name),status=(st.group(2) if st else None),error=(f"{err.group(1)}: {err.group(2)}" if err else None),
                tokens_per_book=(int(forg.group(1)) if forg else None))
HIST709={};CHRONO=[]
def load_evidence():
    """verified historical files: copied byte-identically into the session folder under a name that says what they are"""
    global HIST709,CHRONO
    raw=fetch_locked("709.log");HIST709=parse_709_log(raw.decode("utf-8","replace"))
    (HIST_DIR/"HISTORICAL_TEST709_published_709.log").write_bytes(raw)
    CHRONO=[]
    for n in ("706.log","707.log","708.log"):
        try:
            r=fetch_locked(n);CHRONO.append(parse_failure_log(n,r.decode("utf-8","replace")));(HIST_DIR/("HISTORICAL_"+n)).write_bytes(r)
        except Exception as ex:CHRONO.append(dict(file=n,label=n,status="NOT VERIFIED",error=f"{type(ex).__name__}: {ex}"))
    CHRONO.append(dict(file="709.log",label="TEST708-R2 (709.py)",status=HIST709["status"],error=None,tokens_per_book=None))
    (HIST_DIR/"README_HISTORICAL.txt").write_text(
        "These files are PUBLISHED RECORDS OF EARLIER RUNS, verified against their git blob identifiers.\n"
        "They are NOT results of this session. Live results of this session are in ../live_engine/ and the session files.\n"
        +"".join(f"{n}: git blob {LOCKS[n]}\n" for n in ("709.log","706.log","707.log","708.log")),encoding="utf-8")
    slog("HISTORICAL_LOADED","published 709.log verified (reference only, not this session)",status=HIST709["status"],chronology=[(c["label"],c["status"]) for c in CHRONO])
    return dict(historical_status=HIST709["status"])
def sources_step():
    load_engine_source();h=load_evidence()
    try:fetch_locked("LICENSE");(SESSION_DIR/"LICENSE.txt").write_bytes((EVIDENCE_DIR/"LICENSE").read_bytes())
    except Exception as ex:raise RuntimeError(f"LICENSE could not be verified: {type(ex).__name__}: {ex}")
    return dict(sources={k:v["git_blob"] for k,v in SOURCES.items()},**h)

# ---------------------------------------------------------------------------------------------------------------------
# LIVE record of this session (from the engine's own record R and its live log) + verification
# ---------------------------------------------------------------------------------------------------------------------
def live_record():
    R=E["R"]
    return dict(status=R.get("status"),checks=[dict(c) for c in R["checks"]],budget=R.get("budget") or {},env=R.get("env") or {},model_revision=R.get("model_revision"),
                trials=OrderedDict((t["label"],dict(books=list(t["active"]),stages=t["stages"],qa=t["qa"],cache_tokens=t["cache_tokens"],seconds=t["seconds"])) for t in R["trials"]),
                saved={b["id"]:dict(bytes=b.get("cartridge_file_bytes"),sha256=b.get("cartridge_sha256")) for b in R["books"]},
                sources={b["id"]:dict(bytes=b.get("source_bytes"),sha256=b.get("source_sha256"),title=b.get("title")) for b in R["books"]},
                forge_tokens={b["id"]:b.get("requested_tokens") for b in R["books"]},appends=list(ENGINE.get("protocol_append_pass_lines",[])),
                elapsed_s=R.get("elapsed_s"),model_load_s=R.get("model_load_s"))

def historical_comparison(L):
    """reproducibility comparison of this live run with the published earlier run — reference only, never used for READY"""
    if not HIST709:return dict(available=False)
    sha={b:(L["saved"].get(b,{}).get("sha256")==HIST709["saved"].get(b,{}).get("sha256")) for b in ("A","B","C")}
    ans={}
    for lab,t in L["trials"].items():
        h=HIST709["trials"].get(lab)
        if h:ans[lab]=[r["raw"] for r in t["qa"]]==[r["raw"] for r in h["qa"]]
    rows={lab:([s["cache_tokens"] for s in t["stages"]]==[s["cache_tokens"] for s in HIST709["trials"].get(lab,{}).get("stages",[])]) for lab,t in L["trials"].items() if lab in HIST709["trials"]}
    return dict(available=True,note="published 709.log = earlier run; comparison only, not part of the READY decision",historical_status=HIST709["status"],
                cartridge_sha256_identical=sha,trial_answers_identical=ans,trial_rows_identical=rows)

def compute_verification():
    L=live_record();checks=L["checks"];names={c["name"] for c in checks};items=[]
    def add(name,ok,detail):items.append(dict(name=name,passed=bool(ok),detail=jsafe(detail)))
    add("ENGINE_STATUS_LIVE",L["status"]==ENGINE_PASS_STATUS,L["status"])
    add("ALL_ENGINE_CHECKS_PASSED",bool(checks) and all(c["pass"] for c in checks),f"{sum(1 for c in checks if c['pass'])}/{len(checks)} passed")
    miss=[n for n in REQUIRED_ENGINE_CHECKS if n not in names];add("REQUIRED_ENGINE_CHECKS_PRESENT",not miss,miss or f"{len(REQUIRED_ENGINE_CHECKS)} present")
    labels=list(L["trials"]);add("SCRIPTED_TRIALS_COMPLETE",labels==ENGINE["scripted_trials"],f"{len(labels)}/{len(ENGINE['scripted_trials'])} trials")
    pa=len(L["appends"]);add("PROTOCOL_APPENDS_EXACT_SHA256",pa==ENGINE["expected_protocol_appends"],f"{pa}/{ENGINE['expected_protocol_appends']} appends, all 80 layers")
    d=STATE["disk_checks"][-1] if STATE["disk_checks"] else None;add("CARTRIDGE_FILES_SHA256_ON_DISK",bool(d and d["passed"]),{r["book"]:r["equals_engine_record"] for r in (d or {}).get("files",[])})
    abc=L["trials"].get("A_PLUS_B_PLUS_C",{}).get("cache_tokens");st=STATE["stages"]
    ok=STATE["order"]==["A","B","C"] and bool(st) and st[-1]["cache_tokens"]==abc and all(s["prior_kv_sha256_pass_line"] for s in st[1:])
    add("READY_MEMORY_A_PLUS_B_PLUS_C",ok,dict(order=STATE["order"],rows=(st[-1]["cache_tokens"] if st else None),protocol_rows=abc,append_sha256_lines=[s["prior_kv_sha256_pass_line"] for s in st[1:]]))
    w=STATE["weight_checks"][-1] if STATE["weight_checks"] else None;add("WEIGHT_SENTINEL_UNCHANGED_AFTER_ALL_STEPS",bool(w and w["passed"]),(w or {}).get("after"))
    add("GPU_SAFETY_RESERVE_NOT_REDUCED",float(E["GPU_RESERVE_GIB"])>=EXPECTED_RESERVE_GIB,f"{E['GPU_RESERVE_GIB']} GiB")
    x=STATE["xray"];add("XRAY_FROM_LIVE_KV",bool(x and x["finite"] and x["layers"]==E["NL"] and st and x["tokens"]==st[-1]["cache_tokens"]),(f"{x['layers']} layers × {x['tokens']} rows" if x else None))
    qs=protocol_questions();got={r["question"] for r in STATE["controls"]};add("NO_MEMORY_CONTROLS_COMPLETE",all(q in got for q in qs),f"{sum(1 for q in qs if q in got)}/{len(qs)}")
    rec=dict(session=SESSION_ID,utc=utc_now(),ready=all(i["passed"] for i in items),passed=sum(i["passed"] for i in items),total=len(items),items=items,
             semantics="UNSCORED — physical reconstruction and integrity are measured; answer correctness is not scored; public-domain books (pretraining knowledge possible)",
             live_engine_status=L["status"],live_engine_elapsed_s=L["elapsed_s"],cartridges=L["saved"],historical_reference=historical_comparison(L))
    STATE["verification"]=rec;dump_json(VERIFY_FILE,rec);slog("VERIFICATION","READY" if rec["ready"] else "NOT READY",passed=rec["passed"],total=rec["total"],failed=[i["name"] for i in items if not i["passed"]])
    return rec

# ---------------------------------------------------------------------------------------------------------------------
# SIX RESEARCH FIGURES (JPEG full resolution, PNG lossless, PDF vector) — values ONLY from this live session
# ---------------------------------------------------------------------------------------------------------------------
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.linewidth":.9,"axes.edgecolor":"#374151","axes.labelcolor":"#111827",
                     "xtick.color":"#374151","ytick.color":"#374151","xtick.labelsize":10.5,"ytick.labelsize":10.5,"axes.labelsize":12,
                     "axes.titlesize":13,"axes.titleweight":"bold","axes.titlelocation":"left","legend.fontsize":10.5,"legend.frameon":False})
FW,FH=13.333,7.5;OUT_DPI=300
INK,INK2,MUTED,RULE,PANEL="#111827","#374151","#6B7280","#D1D5DB","#F8FAFC"
TEAL,RED,AMBER="#0F766E","#B91C1C","#B45309"
FIGURES=OrderedDict([
    ("F1","Figure 1 — Physical memory injection protocol"),("F2","Figure 2 — Silicon Hippocampus architecture: SSD cartridges vs live GPU memory"),
    ("F3","Figure 3 — Three-cartridge consolidation and performance"),("F4","Figure 4 — Internal neural memory X-ray"),
    ("F5","Figure 5 — Three books: memory and question answering (observational)"),("F6","Figure 6 — Integrity and verification record")])
FIG_FILES={};LIVE={}
def mt(s):return str(s).replace("$",r"\$")
def wrap(s,n):return "\n".join(textwrap.wrap(str(s),n,break_long_words=True,break_on_hyphens=False)) or ""
def short(s,n):s=" ".join(str(s).split());return s if len(s)<=n else s[:n-1].rstrip()+"…"
def _bb(fig,t):return t.get_window_extent(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())
def fit(fig,t,xmax=.965,xmin=None,minsize=6.5,trunc=False):
    # shrink a text object until it lies inside [xmin,xmax] (figure fraction); optionally shorten it (marked …) after that
    while t.get_fontsize()>minsize:
        b=_bb(fig,t)
        if b.x1<=xmax and (xmin is None or b.x0>=xmin):return t
        t.set_fontsize(t.get_fontsize()-.25)
    if trunc:
        s=t.get_text()
        while len(s)>3 and _bb(fig,t).x1>xmax:
            s=s.rstrip("…")[:-2].rstrip()+"…";t.set_text(s)
    return t
def ftext(fig,x,y,s,xmax=.965,xmin=None,minsize=6.5,trunc=False,**kw):return fit(fig,fig.text(x,y,mt(s),**kw),xmax,xmin,minsize,trunc)

def fig_base(k,title,subtitle,badge,badge_col,h=FH):
    fig=plt.figure(figsize=(FW,h),dpi=100,facecolor="white");s=FH/h
    b=fig.text(.965,1-.05*s,badge,fontsize=10.5,weight="bold",color=badge_col,va="center",ha="right",bbox=dict(boxstyle="square,pad=0.4",fc="white",ec=badge_col,lw=1.2))
    bx0=_bb(fig,b).x0-.015
    fig.text(.035,1-.05*s,f"Fig. {k}",fontsize=15,weight="bold",color=MUTED,va="center")
    ftext(fig,.095,1-.05*s,title,xmax=bx0,minsize=12,fontsize=18,weight="bold",color=INK,va="center")
    ftext(fig,.035,1-.095*s,subtitle,minsize=9,fontsize=12,color=INK2,va="center")
    fig.add_artist(Line2D([.035,.965],[1-.122*s,1-.122*s],transform=fig.transFigure,color=INK2,lw=.8))
    return fig
def fig_footer(fig,k,note,h=FH):
    s=FH/h
    fig.add_artist(Line2D([.035,.965],[.075*s,.075*s],transform=fig.transFigure,color=RULE,lw=.7))
    ftext(fig,.035,.05*s,note,minsize=8,fontsize=10,color=INK2,va="center")
    ftext(fig,.035,.022*s,f"{APP_SHORT} · {ORG} · {LICENSE_NAME} · {COPYRIGHT} · engine 709.py {LOCKS['709.py'][:10]} · live session {SESSION_ID} · Fig. {k}/6",
          minsize=6,fontsize=8.6,color=MUTED,va="center",family="DejaVu Sans Mono")
def box(fig,x,y,w,h,ec,fc="white",lw=1.6,r=.010):
    fig.add_artist(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={r}",transform=fig.transFigure,facecolor=fc,edgecolor=ec,lw=lw,zorder=1))
def arrow(fig,x0,y0,x1,y1,col=INK2,lw=1.8,ms=16,cs="arc3"):
    fig.add_artist(FancyArrowPatch((x0,y0),(x1,y1),transform=fig.transFigure,arrowstyle="-|>",mutation_scale=ms,lw=lw,color=col,connectionstyle=cs,zorder=5))
def save_fig(fig,key,k):
    stem=f"FIGURE_{k:02d}_{key}"
    jpg=FIG_DIR/(stem+".jpg");png=FIG_DIR/(stem+".png");pdf=FIG_DIR/(stem+".pdf")
    fig.savefig(pdf,facecolor="white");buf=io.BytesIO();fig.savefig(buf,format="png",dpi=OUT_DPI,facecolor="white");plt.close(fig)
    png.write_bytes(buf.getvalue())
    with Image.open(io.BytesIO(buf.getvalue())) as im:im.convert("RGB").save(jpg,"JPEG",quality=95,optimize=True,subsampling=0,dpi=(OUT_DPI,OUT_DPI))
    with Image.open(jpg) as c:
        if c.format!="JPEG" or c.size[0]<3000:raise RuntimeError("JPEG check failed "+str(jpg))
        size=c.size
    rec=dict(key=key,figure=k,title=FIGURES[f"F{k}"],jpg=str(jpg),png=str(png),pdf=str(pdf),pixels=list(size),jpg_bytes=jpg.stat().st_size,sha256_jpg=sha_file(jpg),utc=utc_now(),data="live session "+SESSION_ID)
    flog(f"FIGURE {k} {key} {size[0]}x{size[1]} jpg sha256 {rec['sha256_jpg']}");return rec

def _arch():
    a=engine_architecture()
    if not a:raise OpError("figures need the architecture measured by the engine in this session")
    return a
def _first_stage():
    st=(LIVE["trials"].get("A_ONLY") or {}).get("stages") or []
    if not st:raise OpError("figures need the live A_ONLY protocol trial")
    return st[0]
def _titles():return {b:LIVE["sources"].get(b,{}).get("title") or b for b in ("A","B","C")}

def fig1(k=1):
    a=_arch();ab=_first_stage();n=ab["cache_tokens"];cb=LIVE["saved"]["A"]["bytes"];kvb=a["full_kv_bytes_per_token"];c=a["cut"];L=a["layers"]
    fig=fig_base(k,"Physical memory injection protocol — Qwen2.5-72B-Instruct, CUT3",
                 f"{L} layers · hidden {a['hidden']:,} · {a['q_heads']} query / {a['kv_heads']} KV heads · head dim {a['head_dim']} · NF4 weights, BF16 K/V · frozen (measured in this session)",
                 "SCHEMATIC + LIVE VALUES",INK2)
    steps=[("1  FORGE",BOOK_COLORS["A"],f"The frozen model reads ONE book excerpt ({n:,} rows incl. prefix) in {a['chunk']}-token chunks."),
           ("2  PERSIST",INK2,f"Only H{c} and the K/V of layers 0–{c} are saved to SSD (.pt file + SHA-256)."),
           ("3  WRITE L0–L3",LOWER_COLOR,"Mount: lower-layer K/V rows come from the file; keys are re-phased (RoPE) when appended."),
           ("4  INJECT + REBUILD",UPPER_COLOR,f"Zero input embeddings; H{c} replaces the layer-{c} output; layers {c+1}–{L-1} recompute the rows."),
           ("5  ANSWER",BOOK_COLORS["A"],f"Only the question suffix is fed; greedy decoding, ≤ {a['max_new']} new tokens.")]
    w=.172;g=(.93-5*w)/4
    for i,(t,col,body) in enumerate(steps):
        x=.035+i*(w+g);box(fig,x,.62,w,.205,col,lw=2)
        fig.add_artist(FancyBboxPatch((x,.785),w,.04,boxstyle="round,pad=0,rounding_size=0.010",transform=fig.transFigure,facecolor=col,edgecolor=col,zorder=2))
        ftext(fig,x+.01,.805,t,xmax=x+w-.006,fontsize=12.5,weight="bold",color="white",va="center",zorder=3)
        ftext(fig,x+.01,.768,wrap(body,27),xmax=x+w-.006,fontsize=10.5,color=INK,va="top",linespacing=1.3)
        if i<4:arrow(fig,x+w+.002,.72,x+w+g-.002,.72,ms=16)
    x0=.08;W=.86;bw=W/L;y=.44;hh=.07
    for li in range(L):
        fig.add_artist(Rectangle((x0+li*bw+(.004 if li>c else 0),y),bw*.82,hh,transform=fig.transFigure,facecolor=LOWER_COLOR if li<=c else UPPER_COLOR,edgecolor="none",zorder=2))
    for li in (0,c,20,40,60,L-1):fig.text(x0+li*bw+bw*.41+(.004 if li>c else 0),y-.025,f"L{li}",fontsize=10,ha="center",color=INK2)
    xc=x0+(c+1)*bw+.0015;fig.add_artist(Line2D([xc,xc],[y-.012,y+hh+.03],transform=fig.transFigure,color=CUT_COLOR,lw=3,zorder=4))
    fig.text(xc+.006,y+hh+.035,f"◀ CUT{c}: H{c} injected here (layer-{c} output)",fontsize=12,weight="bold",color=CUT_COLOR)
    fig.text(x0,y-.065,f"L0–L{c}: K/V rows written from the cartridge file ({c+1} layers)",fontsize=12,weight="bold",color=LOWER_COLOR)
    fig.text(x0+W,y-.065,f"L{c+1}–L{L-1}: recomputed at every mount ({L-c-1} layers)",fontsize=12,weight="bold",color=UPPER_COLOR,ha="right")
    facts=[("Cartridge file (book A, this session)",f"{cb:,} B",f"H{c} [1, {n:,}, {a['hidden']:,}] + K/V of L0–L{c}: 4 × 2 × [1, {a['kv_heads']}, {n:,}, {a['head_dim']}]"),
           ("Full live K/V rebuilt by one mount",f"{n*kvb:,} B",f"{L} layers × {kvb:,} B per token"),
           ("First mount of book A (live protocol)",f"{ab['rebuild_ms']/1000:.1f} s rebuild",f"SSD read {ab['ssd_load_ms']/1000:.2f} s · host→GPU {ab['h2d_ms']:.0f} ms"),
           ("Prior K/V check at each append (live)",f"{len(LIVE['appends'])} × PASS",f"exact SHA-256 of every prior K/V byte, all {L} layers")]
    fw=(.93-3*.01)/4
    for i,(h1,v,sub) in enumerate(facts):
        x=.035+i*(fw+.01);box(fig,x,.11,fw,.2,RULE,fc=PANEL,lw=1)
        ftext(fig,x+.012,.285,h1,xmax=x+fw-.008,fontsize=11,weight="bold",color=INK2,va="top")
        ftext(fig,x+.012,.225,v,xmax=x+fw-.008,fontsize=17,weight="bold",color=INK,va="center")
        ftext(fig,x+.012,.175,wrap(sub,38),xmax=x+fw-.008,fontsize=10,color=INK2,va="top")
    fig_footer(fig,k,"Schematic illustration of the TEST709 path (layer strip not to scale). Every number was measured by the engine in this live session.")
    return save_fig(fig,"PHYSICAL_MEMORY_INJECTION_PROTOCOL",k)

def fig2(k=2):
    a=_arch();n=_first_stage()["cache_tokens"];kvb=a["full_kv_bytes_per_token"];c=a["cut"];titles=_titles()
    fig=fig_base(k,"Silicon Hippocampus architecture — SSD cartridges vs live GPU memory",
                 f"Three independent book cartridges are persisted on disk; the full {a['layers']}-layer memory exists only on the GPU after a mount","SCHEMATIC + LIVE VALUES",INK2)
    fig.text(.035,.815,"SSD — persistent cartridges (this session)",fontsize=14,weight="bold",color=INK)
    hb=n*a["hidden"]*2;kb=n*a["kv_heads"]*a["head_dim"]*2*2*(c+1)
    X0,BW=.035,.355
    for i,bid in enumerate(("A","B","C")):
        y=.625-i*.18;box(fig,X0,y,BW,.155,BOOK_COLORS[bid],lw=2);xm=X0+BW-.008;sv=LIVE["saved"].get(bid,{})
        ftext(fig,X0+.012,y+.125,f"Cartridge {bid} — {titles[bid]}",xmax=xm,fontsize=12,weight="bold",color=BOOK_COLORS[bid],va="center")
        ftext(fig,X0+.012,y+.088,f"file {sv.get('bytes',0):,} B · SHA-256 {str(sv.get('sha256'))[:16]}…",xmax=xm,fontsize=10,color=INK2,va="center",family="DejaVu Sans Mono")
        ftext(fig,X0+.012,y+.055,f"H{c}        [1, {n:,}, {a['hidden']:,}] BF16 = {hb:,} B",xmax=xm,fontsize=10,color=INK,va="center",family="DejaVu Sans Mono")
        ftext(fig,X0+.012,y+.024,f"K/V L0–L{c}  4×2×[1, {a['kv_heads']}, {n:,}, {a['head_dim']}] = {kb:,} B",xmax=xm,fontsize=10,color=INK,va="center",family="DejaVu Sans Mono")
    hs=[s for t in LIVE["trials"].values() for s in t["stages"]]
    arrow(fig,X0+BW+.012,.5,.485,.5,lw=2.4,ms=22);fig.text((X0+BW+.485)/2,.525,"mount",fontsize=13,weight="bold",ha="center",color=INK)
    if hs:
        ftext(fig,X0,.2,f"Mount = SSD read + SHA-256 check ≈ {np.mean([s['ssd_load_ms'] for s in hs])/1000:.2f} s, then host→GPU ≈ {np.mean([s['h2d_ms'] for s in hs]):.0f} ms\n(means over the {len(hs)} cartridge mounts of the live protocol)",
              xmax=X0+BW+.06,fontsize=10.5,color=INK2,va="top",linespacing=1.4)
    G0,GW=.5,.465
    ftext(fig,G0,.815,"GPU — frozen model + live memory (rebuilt at every mount)",fontsize=14,weight="bold",color=INK)
    base=LIVE["budget"].get("model_gpu",{}).get("allocated_gib")
    box(fig,G0,.62,GW,.15,INK2,fc=PANEL,lw=1.2)
    ftext(fig,G0+.012,.74,"Qwen2.5-72B-Instruct · NF4 4-bit weights · frozen",fontsize=12.5,weight="bold",color=INK,va="center")
    ftext(fig,G0+.012,.695,f"GPU memory allocated after load: {base:.1f} GiB ({LIVE['env'].get('gpu','GPU')})" if base else "",fontsize=11.5,color=INK2,va="center")
    ftext(fig,G0+.012,.655,f"{a['layers']} layers · weights unchanged (weight sentinel re-checked in this session)",fontsize=11.5,color=INK2,va="center")
    abc=LIVE["trials"].get("A_PLUS_B_PLUS_C",{}).get("stages",[])
    y=.37;hgt=.17
    ftext(fig,G0,y+hgt+.035,f"Live K/V memory: {a['layers']} layers × rows · {kvb:,} B per row (token)",fontsize=12,weight="bold",color=INK)
    if abc:
        tot=abc[-1]["cache_tokens"];a0=0
        for s in abc:
            w=GW*(s["cache_tokens"]-a0)/tot;fig.add_artist(Rectangle((G0+GW*a0/tot,y),w-.003,hgt,transform=fig.transFigure,facecolor=BOOK_COLORS[s["book"]],edgecolor="none",alpha=.92))
            fig.text(G0+GW*a0/tot+w/2,y+hgt/2+.025,f"{s['book']}",fontsize=16,weight="bold",color="white",ha="center",va="center")
            fig.text(G0+GW*a0/tot+w/2,y+hgt/2-.03,f"{s['cache_tokens']-a0:,} rows\n{(s['cache_tokens']-a0)*kvb/2**30:.2f} GiB",fontsize=10.5,color="white",ha="center",va="center")
            a0=s["cache_tokens"]
        gp=abc[-1]["gpu"]
        ftext(fig,G0,y-.02,f"A+B+C in the live protocol: {tot:,} rows = {tot*kvb:,} B ({tot*kvb/2**30:.2f} GiB) of K/V\nGPU after the third mount: allocated {gp['allocated_gib']:.2f} GiB, free {gp['free_gib']:.2f} GiB",
              fontsize=11,color=INK2,va="top",linespacing=1.4)
        cfb=LIVE["saved"]["A"]["bytes"]
        ftext(fig,G0,y-.105,f"One cartridge file = {100*cfb/(n*kvb):.1f} % of the full K/V bytes of the same {n:,} rows;\nthe other {a['layers']-c-1} layers are recomputed at mount time, not stored.",
              fontsize=11,color=INK,va="top",weight="bold",linespacing=1.4)
    fig_footer(fig,k,"Schematic layout, values measured in this session. The SSD holds only cartridges; the complete K/V memory exists only on the GPU after a mount.")
    return save_fig(fig,"ARCHITECTURE_SSD_GPU",k)

def fig3(k=3):
    fig=fig_base(k,"Three-cartridge consolidation and performance",
                 "Mount stages measured in this live session · times in seconds (log scale) · GPU memory in GiB","LIVE SESSION MEASUREMENT",TEAL)
    ax=fig.add_axes([.065,.2,.40,.56]);rows=[]
    for lab in ("A_PLUS_B_PLUS_C","C_PLUS_B_PLUS_A"):
        for i,s in enumerate(LIVE["trials"].get(lab,{}).get("stages",[])):rows.append((lab,i,s))
    if not rows:raise OpError("figure 3 needs the live three-cartridge protocol trials")
    xs=np.arange(len(rows));wd=.26
    ax.bar(xs-wd,[s["ssd_load_ms"]/1000 for _,_,s in rows],wd,color="#94A3B8",label="SSD read + SHA-256")
    ax.bar(xs,[s["h2d_ms"]/1000 for _,_,s in rows],wd,color="#475569",label="host → GPU")
    ax.bar(xs+wd,[s["rebuild_ms"]/1000 for _,_,s in rows],wd,color=[BOOK_COLORS[s["book"]] for _,_,s in rows],label="rebuild (colour = book)")
    ax.set_yscale("log");ax.set_ylim(min(.05,min(s["h2d_ms"]/1000 for _,_,s in rows)*.6),max(s["rebuild_ms"]/1000 for _,_,s in rows)*8);ax.set_ylabel("seconds (log scale)")
    ax.set_xticks(xs);ax.set_xticklabels([f"{'A+B+C' if l.startswith('A') else 'C+B+A'}\nstage {i+1}: {s['book']}\n{s['cache_tokens']:,} rows" for l,i,s in rows],fontsize=8.8)
    for x,(_,_,s) in zip(xs,rows):ax.text(x+wd,s["rebuild_ms"]/1000*1.1,f"{s['rebuild_ms']/1000:.1f}",ha="center",fontsize=10,weight="bold")
    ax.legend(loc="upper left",ncol=3,fontsize=9.5,handlelength=1.2,columnspacing=1.0)
    ax.set_title("(a) live protocol: rows after each mount, A+B+C and C+B+A",pad=10);ax.grid(axis="y",color="#E5E7EB",lw=.6);ax.set_axisbelow(True)
    for sp in ("top","right"):ax.spines[sp].set_visible(False)
    bx=fig.add_axes([.56,.51,.40,.25]);pts=[(s["cache_tokens"],s["gpu"]["allocated_gib"],s["gpu"]["free_gib"]) for t in LIVE["trials"].values() for s in t["stages"]]
    base=LIVE["budget"].get("model_gpu",{}).get("allocated_gib");kvb=LIVE["budget"].get("full_kv_bytes_per_token");res=LIVE["budget"].get("reserve_gib",E["GPU_RESERVE_GIB"])
    T=max(p[0] for p in pts)
    bx.plot([p[0] for p in pts],[p[1] for p in pts],"o",color=INK,ms=7,label="allocated after mount")
    bx.plot([p[0] for p in pts],[p[2] for p in pts],"s",color=TEAL,ms=6,label="free after mount")
    if base and kvb:tt=np.linspace(0,T,50);bx.plot(tt,base+tt*kvb/2**30,"--",color=MUTED,lw=1.4,label="model + K/V bytes (arithmetic)")
    bx.axhline(res,color=RED,lw=1.2,ls=":");bx.text(T*.01,res+1.2,f"GPU safety reserve {res} GiB",color=RED,fontsize=9.5)
    bx.set_ylim(0,max(max(p[1] for p in pts),max(p[2] for p in pts))*1.12);bx.legend(fontsize=9,loc="lower right",bbox_to_anchor=(.92,.18))
    bx.set_xlabel("memory rows (tokens)",fontsize=10.5);bx.set_ylabel("GiB");bx.set_title(f"(b) GPU memory after each live mount (n = {len(pts)})",pad=8);bx.grid(color="#E5E7EB",lw=.6)
    for sp in ("top","right"):bx.spines[sp].set_visible(False)
    cx=fig.add_axes([.56,.16,.40,.22]);ss=[s for s in STATE["ops"] if s["label"]=="READY_A_PLUS_B_PLUS_C"]
    if not ss:raise OpError("figure 3 needs the live ready-memory build")
    xs2=np.arange(len(ss));cx.bar(xs2,[s["end_to_end_ms"]/1000 for s in ss],color=[BOOK_COLORS[s["book"]] for s in ss],width=.55)
    cx.set_xticks(xs2);cx.set_xticklabels([f"{'first ' if s['operation']=='initialize' else '+'}{s['book']} · {s['cache_tokens']:,} rows" for s in ss],fontsize=9);cx.set_ylabel("s, end-to-end",fontsize=10.5)
    for x,s in zip(xs2,ss):cx.text(x,s["end_to_end_ms"]/1000*1.02,f"{s['end_to_end_ms']/1000:.1f}",ha="center",va="bottom",fontsize=9.5,weight="bold")
    cx.set_ylim(0,max(s["end_to_end_ms"] for s in ss)/1000*1.2);cx.set_title("(c) ready memory A+B+C built for the interface",pad=8)
    for sp in ("top","right"):cx.spines[sp].set_visible(False)
    fig_footer(fig,k,"rebuild = TEST709 'rebuild_ms' (initialize()/append() until GPU release); for appends it includes the exact SHA-256 seal and re-check of all prior K/V.")
    return save_fig(fig,"CONSOLIDATION_PERFORMANCE",k)

def fig4(k=4):
    x=STATE.get("xray")
    if not x:raise OpError("Figure 4 needs the read-only X-ray measurement of the live memory (no synthetic heat map is drawn).")
    fig=fig_base(k,"Internal neural memory X-ray — live 80-layer K/V memory",
                 f"Measured {x['utc']} · memory {'+'.join(x['order'])} · {x['tokens']:,} rows × {x['layers']} layers · bin {x['bin_tokens']} tokens",
                 "LIVE GPU MEASUREMENT",TEAL)
    def z(m):
        m=np.asarray(m,dtype=float);mu=np.nanmean(m,axis=1,keepdims=True);sd=np.nanstd(m,axis=1,keepdims=True);return (m-mu)/np.where(sd>0,sd,1)
    for j,(key,lab) in enumerate((("k_norm","K"),("v_norm","V"))):
        ax=fig.add_axes([.07,.53-j*.38,.86,.28]);im=ax.imshow(z(x[key]),aspect="auto",origin="lower",cmap="RdBu_r",vmin=-2.5,vmax=2.5,interpolation="nearest")
        ax.axhline(x["cut"]+.5,color=CUT_COLOR,lw=2,ls="--");ax.set_ylabel("layer");ax.set_yticks([0,20,40,60,x["layers"]-1])
        ax.set_title(f"‖{lab}‖ per row (mean over {x['kv_heads']} KV heads), z-scored within each layer for display",pad=6)
        nb=len(x[key][0])
        for s in x["segments"]:
            b0=s["start"]/x["bin_tokens"]-.5;b1=s["end"]/x["bin_tokens"]-.5
            ax.axvline(b1,color="white",lw=1.6)
            ax.text((b0+b1)/2,x["layers"]-3,f"cartridge {s['book']}",color=BOOK_COLORS[s["book"]],fontsize=11,weight="bold",ha="center",va="top",
                    bbox=dict(boxstyle="round,pad=0.25",fc="white",ec=BOOK_COLORS[s["book"]],lw=1,alpha=.92))
        ax.set_xticks(np.linspace(0,nb-1,6));ax.set_xticklabels([f"{int(t*x['bin_tokens']):,}" for t in np.linspace(0,nb-1,6)])
        if j==1:ax.set_xlabel("memory row (token position)")
        cb=fig.colorbar(im,ax=ax,fraction=.015,pad=.01);cb.set_label("z")
        ax.text(nb*.995-.5,x["cut"]+2,f"above dashed line: L{x['cut']+1}–L{x['layers']-1} recomputed · below: L0–L{x['cut']} from cartridges",ha="right",va="bottom",fontsize=9.5,color=INK,
                bbox=dict(boxstyle="round,pad=0.2",fc="white",ec="none",alpha=.85))
    fig_footer(fig,k,"Read-only measurement of this session's GPU K/V tensors (method in XRAY_MEASUREMENT.json). Colours are normalised per layer; absolute values are in the JSON record.")
    return save_fig(fig,"INTERNAL_MEMORY_XRAY",k)

def fig5(k=5):
    fig=fig_base(k,"Three books — memory and question answering (observational)",
                 "Raw answers of the frozen model in this live session; semantics UNSCORED; public-domain classics, so pretraining knowledge cannot be excluded","LIVE · OBSERVATIONAL",AMBER)
    titles=_titles();cw=(.93-2*.012)/3
    for i,bid in enumerate(("A","B","C")):
        x=.035+i*(cw+.012);box(fig,x,.745,cw,.09,BOOK_COLORS[bid],lw=2);src=LIVE["sources"].get(bid,{})
        ftext(fig,x+.01,.812,f"Cartridge {bid} — {titles[bid]}",xmax=x+cw-.006,fontsize=12.5,weight="bold",color=BOOK_COLORS[bid],va="center")
        ftext(fig,x+.01,.772,f"first {LIVE['forge_tokens'].get(bid) or 0:,} tokens of the Gutenberg file\n(source {src.get('bytes') or 0:,} B, SHA-256 {str(src.get('sha256'))[:12]}…)",xmax=x+cw-.006,fontsize=9.6,color=INK2,va="center")
    ctl={r["question"]:r["raw"] for r in STATE["controls"]}
    rows=[]
    for lab,t in LIVE["trials"].items():
        if t["qa"]:r=t["qa"][0];rows.append(("+".join(t["books"]) or "none",r["question"],r["raw"],ctl.get(r["question"])))
    if not rows:raise OpError("figure 5 needs the live protocol answers")
    diff=sum(1 for _,_,a,c in rows if c is not None and a!=c)
    XM,XQ,XA,XC=.035,.1,.37,.67;y=.705;rh=min(.047,.47/len(rows))
    for xx,t in ((XM,"memory"),(XQ,"question (live protocol)"),(XA,"answer WITH cartridge memory"),(XC,"control: same question, NO memory")):fig.text(xx,y,t,fontsize=10.2,weight="bold",color=MUTED)
    for i,(mem_,q,a,c) in enumerate(rows):
        yy=y-.03-i*rh;col=BOOK_COLORS.get(mem_.split("+")[0],INK2) if mem_!="none" else MUTED
        fig.text(XM,yy,mem_,fontsize=10,weight="bold",color=col,va="top")
        ftext(fig,XQ,yy,short(q,70),xmax=XA-.008,minsize=8,trunc=True,fontsize=9.4,color=INK,va="top")
        ftext(fig,XA,yy,short(a,80),xmax=XC-.008,minsize=7.6,trunc=True,fontsize=8.8,color=INK,va="top",family="DejaVu Sans Mono")
        ftext(fig,XC,yy,short(c if c is not None else "— not run",80),xmax=.965,minsize=7.6,trunc=True,fontsize=8.8,color=INK2,va="top",family="DejaVu Sans Mono")
    box(fig,.035,.09,.93,.075,AMBER,fc="#FFFBEB",lw=1.2)
    ftext(fig,.045,.128,wrap(f"Not a causal result. Answers with memory differ from the no-memory control in {diff} of {len(rows)} questions; a difference is not evidence of correctness and "
                             f"an equal answer is not evidence of failure. Semantics are unscored; the books are famous classics. Answers stop at {E['MAX_NEW']} new tokens.",165),
          xmax=.958,fontsize=10,color=INK,va="center")
    fig_footer(fig,k,"All rows were generated in this session (… = shortened for display). Full raw text: live engine log, SESSION_QA.jsonl and the live engine results JSON.")
    return save_fig(fig,"THREE_BOOKS_QA",k)

def fig6(k=6):
    v=STATE.get("verification")
    if not v:raise OpError("figure 6 needs the live verification record")
    fig=fig_base(k,"Integrity and verification record — this live session",f"Engine identity · live verification ({v['passed']}/{v['total']} passed) · historical reference kept separate",
                 "LIVE VERIFICATION",TEAL if v["ready"] else RED)
    a=_arch();env=LIVE["env"]
    col1=[("Engine",f"709.py · blob {LOCKS['709.py'][:12]}… (self-label TEST708-R2)"),("Model",f"{a['model_id']} · rev {str(LIVE.get('model_revision') or '—')[:12]}"),
          ("Weights",a["weights"]),("Architecture",f"{a['layers']} L · {a['hidden']} · {a['q_heads']}Q/{a['kv_heads']}KV · {a['head_dim']} · CUT{a['cut']}"),
          ("GPU",str(env.get("gpu"))),("Software",f"torch {env.get('torch')} · transformers {env.get('transformers')} · bitsandbytes {env.get('bitsandbytes')}"),
          ("Settings",f"{LIVE['forge_tokens'].get('A') or 0:,} tokens/book · chunk {a['chunk']} · reserve {a['reserve_gib']} GiB · max new {a['max_new']}"),
          ("Engine status",f"{LIVE['status']} · {LIVE.get('elapsed_s')} s")]
    fig.text(.035,.8,"Engine and model (this session)",fontsize=13.5,weight="bold",color=INK);y=.755
    for kk,vv in col1:
        s=wrap(vv,40);fig.text(.035,y,kk,fontsize=10.2,weight="bold",color=INK2,va="top")
        ftext(fig,.125,y,s,xmax=.355,fontsize=9.8,color=INK,va="top",linespacing=1.2);y-=.045+.026*s.count("\n")
    fig.text(.375,.8,"Live verification",fontsize=13.5,weight="bold",color=INK);y=.755
    for it in v["items"]:
        ok=it["passed"];fig.text(.375,y,"PASS" if ok else "FAIL",fontsize=10,weight="bold",color=TEAL if ok else RED,va="top",family="DejaVu Sans Mono")
        ftext(fig,.415,y,it["name"],xmax=.665,fontsize=9.6,color=INK,va="top",family="DejaVu Sans Mono")
        ftext(fig,.415,y-.021,short(it["detail"] if isinstance(it["detail"],str) else json.dumps(it["detail"],ensure_ascii=False),70),xmax=.665,minsize=7,trunc=True,fontsize=8.4,color=MUTED,va="top")
        y-=.049
    box(fig,.685,.205,.28,.62,RULE,fc="#F3F4F6",lw=1)
    fig.text(.697,.8,"Historical reference",fontsize=12.5,weight="bold",color=INK2,va="center")
    fig.text(.697,.775,"published logs of EARLIER runs — not this session",fontsize=9,color=RED,va="center",weight="bold")
    yy=.745
    for c in CHRONO:
        ok=str(c.get("status","")).startswith("PASS");fig.text(.697,yy,c["label"],fontsize=10,weight="bold",color=TEAL if ok else RED,va="top")
        s=wrap((f"{c['tokens_per_book']} tok/book · " if c.get('tokens_per_book') else "")+f"{c.get('status')}" + (f" · {c['error']}" if c.get("error") else ""),46)
        ftext(fig,.697,yy-.024,s,xmax=.958,fontsize=8.6,color=INK2,va="top",linespacing=1.15);yy-=.05+.022*s.count("\n")
    h=v.get("historical_reference") or {}
    if h.get("available"):
        sh=", ".join(f"{b} {'identical' if ok else 'different'}" for b,ok in h["cartridge_sha256_identical"].items());ta=h["trial_answers_identical"]
        ftext(fig,.697,yy-.01,wrap(f"Reproducibility comparison computed now (reference only): cartridge SHA-256 vs published run: {sh}; "
                                   f"trial answers identical: {sum(ta.values())}/{len(ta)}",48),xmax=.958,fontsize=8.6,color=INK,va="top",linespacing=1.2)
    box(fig,.035,.09,.93,.1,RULE,fc=PANEL,lw=1)
    fig.text(.045,.175,"Cartridge SHA-256 recorded by the engine in this session (re-verified on disk)",fontsize=10.5,weight="bold",color=INK,va="top")
    for i,b in enumerate(("A","B","C")):
        ftext(fig,.045,.148-i*.02,f"{b}  {LIVE['saved'][b]['sha256']}  {LIVE['saved'][b]['bytes']:,} B",xmax=.958,fontsize=8.8,color=BOOK_COLORS[b],va="top",family="DejaVu Sans Mono")
    fig_footer(fig,k,f"Live records: VERIFICATION_RECORD.json · live engine log · SESSION.log · SHA256_MANIFEST.json (session {SESSION_ID}). Historical files are in a separate folder.")
    return save_fig(fig,"INTEGRITY_VERIFICATION_RECORD",k)

FIG_FUNCS=OrderedDict([("F1",fig1),("F2",fig2),("F3",fig3),("F4",fig4),("F5",fig5),("F6",fig6)])
def render_figures():
    """renders all six figures on the CPU from this session's live data (no GPU use)"""
    global LIVE
    LIVE=live_record();out={};errs={}
    for i,(key,fn) in enumerate(FIG_FUNCS.items(),1):
        t=time.perf_counter()
        try:rec=fn(i);out[key]=rec;FIG_FILES[key]=rec;print(f"  figure {i}/6 · {rec['pixels'][0]}×{rec['pixels'][1]} JPEG · {rec['jpg_bytes']/1e6:.1f} MB · {time.perf_counter()-t:.1f} s · {Path(rec['jpg']).name}",flush=True)
        except Exception as ex:errs[key]=f"{type(ex).__name__}: {ex}";FIG_FILES.pop(key,None);flog(f"FIGURE {i} NOT GENERATED {traceback.format_exc()[-1500:]}");print(f"  figure {i}/6 NOT GENERATED · {errs[key]}",flush=True)
    dump_json(SESSION_DIR/"FIGURES_MANIFEST.json",dict(session=SESSION_ID,utc=utc_now(),data_source="live session only",figures=FIG_FILES,not_generated=errs))
    slog("FIGURES",f"{len(out)} rendered",not_generated=errs);return out,errs

# ---------------------------------------------------------------------------------------------------------------------
# downloadable research artifacts (actual files of this session; historical files in their own folder)
# ---------------------------------------------------------------------------------------------------------------------
LIVE_ENGINE_LOG=LIVE_DIR/"LIVE_TEST709_ENGINE_RUN_this_session.log";LIVE_ENGINE_JSON=LIVE_DIR/"LIVE_TEST709_ENGINE_RESULTS_this_session.json"
HIST_709=HIST_DIR/"HISTORICAL_TEST709_published_709.log"
ZIP_PATH=SESSION_DIR/f"{SESSION_ID}_AKBASCORE_Q72_ALL_RESEARCH_ARTIFACTS.zip";MANIFEST=SESSION_DIR/"SHA256_MANIFEST.json"
def sync_live_files():
    """byte-identical copies of the engine's own live files (the engine keeps writing to E['LOG'] / E['OUT'])"""
    for src,dst in ((E.get("LOG"),LIVE_ENGINE_LOG),(E.get("OUT"),LIVE_ENGINE_JSON)):
        try:
            if src and Path(src).is_file():shutil.copyfile(src,dst)
        except Exception as ex:slog("SYNC_FAILED",str(dst),error=str(ex))
def session_record():
    return dict(session=SESSION_INFO,app=APP_TITLE,version_note=VERSION_NOTE,sources=SOURCES,locks=LOCKS,engine=jsafe(ENGINE),initialization=INIT,
                architecture=engine_architecture(),memory=dict(order=STATE["order"],stages=STATE["stages"]),operations=STATE["ops"],
                qa=STATE["qa"],controls=STATE["controls"],weight_checks=STATE["weight_checks"],disk_checks=STATE["disk_checks"],
                verification=STATE["verification"],figures=FIG_FILES,
                scope="Physical reconstruction and integrity are measured live; answer semantics are not scored; public-domain books (pretraining knowledge possible).")
def _category(rel):
    if rel.startswith("historical_reference_not_this_session"):return "HISTORICAL (published earlier run, not this session)"
    if rel.startswith("figures"):return "LIVE figure"
    return "LIVE session record"
RUN_SUMMARY=SESSION_DIR/"RUN_SUMMARY.txt"
def write_run_summary():
    """plain-text summary of THIS live run (like the Mistral v1.4 RUN_SUMMARY.txt); historical files only in their own section"""
    R=E.get("R",{});v=STATE.get("verification") or {};L=[]
    a=L.append
    a(f"{APP_TITLE}\n{VERSION_NOTE}\nsession {SESSION_ID} · started {SESSION_INFO['started_local']} · written {local_now()}\n")
    a("ENGINE  709.py git blob "+LOCKS["709.py"]+" (self-label TEST708-R2), executed unchanged")
    a(f"MODEL   {E.get('MODEL_ID')} · NF4 4-bit, BF16 compute, frozen · revision {R.get('model_revision')} · load {R.get('model_load_s')} s")
    env=R.get("env",{});a(f"GPU     {env.get('gpu')} · torch {env.get('torch')} · transformers {env.get('transformers')} · bitsandbytes {env.get('bitsandbytes')}")
    a(f"SETUP   {E.get('TOKENS_PER_BOOK')} tokens per book · chunk {E.get('CHUNK')} · GPU reserve {E.get('GPU_RESERVE_GIB')} GiB · max new tokens {E.get('MAX_NEW')}\n")
    a("INITIALIZATION (this session)")
    for st in INIT["steps"]:a(f"  ✓ {st['step']:<13} {st['seconds']:>9.1f} s  {st['title']}")
    if INIT.get("failed"):a(f"  ✗ {INIT['failed']['step']}  {INIT['failed']['error']}  (last successful: {INIT['failed']['last_successful_step']})")
    a(f"\nLIVE ENGINE STATUS  {R.get('status')}  · engine checks passed {sum(1 for c in R.get('checks',[]) if c.get('pass'))}/{len(R.get('checks',[]))}")
    a("\nCARTRIDGES (forged and saved in this session)")
    for b in R.get("books",[]):a(f"  {b['id']} {b.get('title')} · {b.get('requested_tokens')} tokens · file {b.get('cartridge_file_bytes')} B · SHA-256 {b.get('cartridge_sha256')}")
    a("\nLIVE TEST709 PROTOCOL (raw answers, semantics UNSCORED)")
    ctl={r["question"]:r["raw"] for r in STATE["controls"]}
    for t in R.get("trials",[]):
        a(f"  {t['label']:<18} rows {t['cache_tokens']:>6} · "+" · ".join(f"{s['book']} rebuild {s['rebuild_ms']/1000:.1f} s" for s in t["stages"]))
        for r in t["qa"]:a(f"      Q {r['question']}\n      memory  → {r['raw']}\n      control → {ctl.get(r['question'],'(not run)')}")
    a(f"\nLIVE VERIFICATION  {v.get('passed','—')}/{v.get('total','—')} passed · READY {v.get('ready')}")
    for i in v.get("items",[]):a(f"  {'PASS' if i['passed'] else 'FAIL'}  {i['name']}  {i['detail'] if isinstance(i['detail'],str) else json.dumps(i['detail'],ensure_ascii=False)}")
    if STATE["qa"]:
        a("\nQUESTIONS ASKED IN THE INTERFACE")
        for r in STATE["qa"]:
            if r.get("origin")=="user":a(f"  [{'+'.join(r['memory_order'])}] {r['question']} → {r['raw']}")
    h=v.get("historical_reference") or {}
    a("\nHISTORICAL REFERENCE — published 709.log of an EARLIER run (not this session, not used for READY)")
    if h.get("available"):
        a(f"  published status {h['historical_status']} · cartridge SHA-256 identical {h['cartridge_sha256_identical']} · trial answers identical {sum(h['trial_answers_identical'].values())}/{len(h['trial_answers_identical'])}")
    a("\nSCOPE  Physical reconstruction and integrity are measured live; answer semantics are not scored; the books are public-domain classics (pretraining knowledge possible).")
    a(f"{AUTHOR} · {ORG} · {LICENSE_NAME} · {COPYRIGHT}")
    RUN_SUMMARY.write_text("\n".join(L)+"\n",encoding="utf-8");return str(RUN_SUMMARY)
def package_session():
    """Download-All ZIP: six figures (JPG/PNG/PDF), live engine log + results, session logs, verification records,
    historical files (separate folder) and SHA256_MANIFEST.json"""
    sync_live_files();dump_json(SESSION_DIR/"SESSION_RECORD.json",session_record());write_run_summary()
    files=sorted(p for p in SESSION_DIR.rglob("*") if p.is_file() and p.suffix not in (".zip",".tmp") and p!=MANIFEST)
    man=OrderedDict((str(p.relative_to(SESSION_DIR)),dict(sha256=sha_file(p),bytes=p.stat().st_size,category=_category(str(p.relative_to(SESSION_DIR))))) for p in files)
    dump_json(MANIFEST,dict(session=SESSION_ID,utc=utc_now(),files=man))
    tmp=ZIP_PATH.with_suffix(".zip.tmp")
    with zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED) as z:
        for p in files+[MANIFEST]:z.write(p,arcname=f"{SESSION_ID}/{p.relative_to(SESSION_DIR)}")
    with zipfile.ZipFile(tmp) as z:
        if z.testzip():raise RuntimeError("ZIP check failed")
    tmp.replace(ZIP_PATH);slog("PACKAGE",ZIP_PATH.name,files=len(files)+1,bytes=ZIP_PATH.stat().st_size);return str(ZIP_PATH)
def download_items():
    """(label, path) of every individually downloadable record — only files that exist"""
    items=[("Run summary (.txt)",RUN_SUMMARY),("Live engine log of this session (.log)",LIVE_ENGINE_LOG),("Live engine results of this session (.json)",LIVE_ENGINE_JSON),
           ("Session log (.log)",SESSION_LOG),("Session events (.jsonl)",SESSION_EVENTS),("Questions and raw answers (.jsonl)",SESSION_QA),
           ("Verification record (.json)",VERIFY_FILE),("Initialization record (.json)",INIT_FILE),("X-ray measurement (.json)",SESSION_DIR/"XRAY_MEASUREMENT.json"),
           ("Figure manifest (.json)",SESSION_DIR/"FIGURES_MANIFEST.json"),("SHA-256 manifest (.json)",MANIFEST),
           ("HISTORICAL · published 709.log of an earlier run (not this session)",HIST_709)]
    return [(l,str(p)) for l,p in items if Path(p).is_file()]

# ---------------------------------------------------------------------------------------------------------------------
# AUTOMATIC INITIALIZATION — one start, every step real, stops at the first failure
# ---------------------------------------------------------------------------------------------------------------------
def _step_model():
    pf=json.loads((SESSION_DIR/"PREFLIGHT.json").read_text()) if (SESSION_DIR/"PREFLIGHT.json").is_file() else {}
    print("  model cache:",pf.get("model_cache_state","unknown"),"\n  The progress bars below are the real Hugging Face download / checkpoint-loading bars.",flush=True)
    return load_model_stage()
def _step_closing():
    r=closing_stage()
    if r["status"]!=ENGINE_PASS_STATUS or r["failed"]:raise RuntimeError(f"TEST709 live status {r['status']} · failed checks {r['failed']}")
    return r
def _step_ready():
    st=build_memory(["A","B","C"],label="READY_A_PLUS_B_PLUS_C")
    return dict(order=STATE["order"],rows=st[-1]["cache_tokens"],stages=[dict(book=s["book"],end_to_end_s=round(s["end_to_end_ms"]/1000,2),sha256_line=s["prior_kv_sha256_pass_line"]) for s in st])
def _step_verify():
    d=verify_disk();w=verify_weights();x=xray_measure();v=compute_verification()
    for it in v["items"]:print(f"  {'PASS' if it['passed'] else 'FAIL'}  {it['name']:<44} {short(it['detail'] if isinstance(it['detail'],str) else json.dumps(it['detail'],ensure_ascii=False),90)}",flush=True)
    if not v["ready"]:raise RuntimeError("LIVE VERIFICATION FAILED: "+", ".join(i["name"] for i in v["items"] if not i["passed"]))
    return dict(passed=v["passed"],total=v["total"])
def _step_figures():
    out,errs=render_figures()
    if errs or len(out)!=6:raise RuntimeError(f"FIGURES: {len(out)}/6 generated · {errs}")
    dump_json(INIT_FILE,INIT);z=package_session()
    return dict(figures=[Path(r["jpg"]).name for r in out.values()],zip=Path(z).name)
STEP_FUNCS=OrderedDict([("SOURCES",sources_step),("PREFLIGHT",preflight),("MODEL",_step_model),("FORGE",forge_stage),("PROTOCOL",protocol_stage),
                        ("CLOSING",_step_closing),("CONTROLS",run_controls),("READY_MEMORY",_step_ready),("VERIFY",_step_verify),("FIGURES",_step_figures)])

def init_failed(key,ex):
    tb=traceback.format_exc()
    INIT["failed"]=dict(step=key,title=INIT_STEPS[key],error=f"{type(ex).__name__}: {ex}",last_successful_step=INIT["last_ok"],utc=utc_now(),traceback=tb[-6000:])
    if ENGINE.get("defined") and not ENGINE.get("finished"):
        try:engine_fail(ex)
        except Exception:pass
    _drop_memory("initialization failed")
    slog("INIT_FAILED",key,error=INIT["failed"]["error"],last_successful_step=INIT["last_ok"],gpu=gpu_now() if ENGINE.get("defined") else None,traceback=tb[-3000:])
    try:dump_json(INIT_FILE,INIT);package_session()
    except Exception as ex2:print("  (failure package could not be written:",ex2,")",flush=True)
    print("\n"+"█"*112+f"\nINITIALIZATION STOPPED — the demonstration is NOT ready and no interface is opened.\n"
          f"  failed step          : {key} · {INIT_STEPS[key]}\n  error                : {INIT['failed']['error']}\n"
          f"  last successful step : {INIT['last_ok'] or 'none'}\n  records              : {SESSION_DIR}\n  all files (ZIP)      : {ZIP_PATH if ZIP_PATH.is_file() else 'not written'}\n"+"█"*112,flush=True)

def run_initialization():
    print("\n"+"#"*112+f"\n{APP_TITLE}\n{VERSION_NOTE} · session {SESSION_ID} · records in {SESSION_DIR}\n"
          "Automatic initialization: every step below is executed for real in this runtime; nothing is precomputed.\n"+"#"*112,flush=True)
    for key,fn in STEP_FUNCS.items():
        t0=step_begin(key)
        try:info=fn()
        except BaseException as ex:
            init_failed(key,ex);raise RuntimeError(f"INITIALIZATION FAILED at {key}: {type(ex).__name__}: {ex}") from ex
        step_done(key,t0,result=info)
    INIT["ready"]=True;INIT["ready_utc"]=utc_now();INIT["total_seconds"]=round(time.perf_counter()-INIT["started"],1)
    dump_json(INIT_FILE,INIT);package_session()
    print("\n"+"#"*112+f"\nREADY — all {len(STEP_FUNCS)} steps passed in {INIT['total_seconds']/60:.1f} min · live verification "
          f"{STATE['verification']['passed']}/{STATE['verification']['total']} · memory {'+'.join(STATE['order'])} ({STATE['stages'][-1]['cache_tokens']:,} rows)\n"+"#"*112,flush=True)
    slog("READY","initialization complete",seconds=INIT["total_seconds"])
    return True
# ===== SILICON HIPPOCAMPUS QWEN72B · PART 3/3 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 3 — Gradio Interface, User Interaction, Research Presentation and Session Logging
# Same working method and interface layout as the Mistral v1.4 demonstration: start-up runs the engine automatically
# (here: model, cartridges, live TEST709 protocol, A+B+C memory, verification, six JPEG figures, ZIP), then the Gradio
# interface opens with the figures, the individual downloads and the complete package. The interface calls the engine,
# records and displays. It never computes or edits an answer. The published 709.log is only a labelled historical file.
# =====================================================================================================================
def esc(x):return html.escape(str(x))
def card_html(title,body,kind="info"):return f'<div class="kz card {kind}"><div class="h">{esc(title)}</div><div class="small">{body}</div></div>'
def chips(order):return "".join(f'<span class="chip" style="color:#fff;background:{BOOK_COLORS[b]};border-color:{BOOK_COLORS[b]}">{esc(b)}</span> ' for b in order) or "<i>no memory mounted</i>"

CSS="""
:root{--kz-on:#0f766e;--kz-fg:#111827;--kz-card:#ffffff;--kz-bd:#d1d5db;--kz-a:#1d4ed8;--kz-err:#b91c1c;--kz-warn:#b45309}
.dark{--kz-on:#2dd4bf;--kz-fg:#f3f4f6;--kz-card:#111827;--kz-bd:#4b5563;--kz-a:#60a5fa;--kz-err:#f87171;--kz-warn:#fbbf24}
html,body{overflow-x:hidden!important}
.gradio-container{width:100%!important;max-width:960px!important;margin:0 auto!important;padding-left:10px!important;padding-right:10px!important;box-sizing:border-box!important}
.gradio-container *{box-sizing:border-box}
.kz{color:var(--kz-fg)!important;max-width:100%;overflow-wrap:anywhere;line-height:1.45}
.kz *{color:inherit}
.hero{background:#0b1220;border-radius:6px;padding:18px 18px 14px;margin:4px 0 8px}
.hero,.hero *{color:#f9fafb!important}
.rec{font-size:11.5px;letter-spacing:1.6px;text-transform:uppercase;opacity:.85;border:1px solid rgba(255,255,255,.35);display:inline-block;padding:2px 8px;border-radius:3px}
.brand{font-size:clamp(20px,5.6vw,30px);font-weight:800;letter-spacing:.4px;line-height:1.15;margin-top:10px}
.title{font-size:clamp(14px,3.8vw,18px);font-weight:600;margin-top:6px;color:#fde68a!important}
.by{font-size:13.5px;margin-top:10px}
.msg{margin:8px 0 0;padding-left:18px;font-size:13.5px}
.lic{font-size:12px;opacity:.85;margin-top:8px}
.card{background:var(--kz-card);border:1px solid var(--kz-bd);border-left:4px solid var(--kz-bd);border-radius:4px;padding:10px 12px;margin:6px 0}
.card.on{border-left-color:var(--kz-on)}.card.err{border-left-color:var(--kz-err)}.card.warn{border-left-color:var(--kz-warn)}.card.info{border-left-color:var(--kz-a)}
.card .h{font-weight:700;font-size:15px;margin-bottom:4px}
.small{font-size:13.5px}
.mono,.kz code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
.chip{display:inline-block;border:1px solid;border-radius:3px;padding:0 6px;font-size:12px;font-weight:700;white-space:nowrap}
.tbl{width:100%;border-collapse:collapse;font-size:13px}
.tbl td,.tbl th{border-bottom:1px solid var(--kz-bd);padding:5px 4px;vertical-align:top;text-align:left}
.tbl th{font-size:12px;opacity:.75}
.stg{font-size:13.5px;margin:2px 0}.stg.done{color:var(--kz-on)!important}.stg.run{color:var(--kz-a)!important;font-weight:700}.stg.wait{opacity:.55}.stg.fail{color:var(--kz-err)!important;font-weight:700}
.ans{white-space:pre-wrap;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;border:1px solid var(--kz-bd);border-radius:4px;padding:6px 8px;margin:3px 0}
#kz_ask button,#kz_ask{font-size:clamp(15px,4.2vw,18px)!important;font-weight:700!important;min-height:52px!important}
@media (max-width:640px){.tbl .hide-m{display:none}}
"""
HERO=(f'<div class="kz hero"><span class="rec">Live research demonstration · frozen Qwen2.5-72B · measured in this session</span>'
      f'<div class="brand">AKBASCORE AI TECHNOLOGY<br>SILICON HIPPOCAMPUS · QWEN2.5-72B / CUT3</div><div class="title">THREE PHYSICAL BOOK CARTRIDGES — inside a frozen 80-layer transformer, from text to tensor memory</div>'
      '<ul class="msg">'
      '<li>Each book excerpt (10,000 tokens) is <b>forged alone</b> by the frozen model into a physical cartridge on SSD: the layer-3 residual state <b>H3</b> and the attention keys/values of <b>layers 0–3</b>, with SHA-256.</li>'
      '<li>A mount feeds the model <b>zero input embeddings</b>: the book enters only as an H3 transplant at the layer-3 boundary, and <b>layers 4–79 are rebuilt</b> on the GPU. Every append checks <b>all prior K/V bytes of all 80 layers by exact SHA-256</b>.</li>'
      '<li>Questions are answered with <b>only the question suffix</b> as input — the book text is not given again. The 72B weights (NF4) are never changed.</li>'
      '<li>Everything shown here was measured in <b>this session</b> by the TEST709 engine (709.py, executed unchanged). The published 709.log is kept only as a labelled historical file.</li>'
      '<li>The books are <b>famous public-domain classics</b>: correct names can come from pretraining. Compare with the <b>no-memory control</b>. Semantics are <b>unscored</b>; answers are capped at 48 new tokens.</li></ul>'
      f'<div class="by"><b>{esc(AUTHOR)}</b> · {esc(ORG)} · {esc(PLACE)} · {esc(VERSION_NOTE)}</div>'
      f'<div class="lic">{esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · <a href="{REPO}" target="_blank" rel="noopener">{esc(REPO)}</a></div></div>')
SCOPE_HTML=card_html("What this demo shows — and what it does not",
    "Shown: the TEST709 Qwen2.5-72B CUT3 engine forges three physical cartridges, runs its eleven scripted trials, rebuilds the full 80-layer K/V memory A+B+C on the GPU and "
    "verifies every append bytewise; every answer is the raw output of the frozen model; every figure value is measured in this session. Not shown: semantic correctness "
    "(unscored), causal use of the cartridges for these famous books (pretraining knowledge cannot be excluded), full-book comprehension, millisecond hot-swap (a mount takes "
    "tens of seconds), autonomous reasoning. The published 709.log is an earlier record, not this run.","warn")

def engine_card_html():
    R=E.get("R",{});env=R.get("env",{});a=engine_architecture() or {};v=STATE.get("verification") or {}
    rows=[("Model",f"{E.get('MODEL_ID')} · NF4 4-bit, BF16 compute · frozen · revision {str(R.get('model_revision'))[:12]}"),
          ("Architecture",f"{a.get('layers')} layers · hidden {a.get('hidden')} · {a.get('q_heads')} Q / {a.get('kv_heads')} KV heads · head dim {a.get('head_dim')} · CUT{a.get('cut')}"),
          ("GPU",f"{env.get('gpu')} · reserve {E.get('GPU_RESERVE_GIB')} GiB (TEST709 safety reserve, unchanged)"),
          ("Software",f"torch {env.get('torch')} · transformers {env.get('transformers')} · bitsandbytes {env.get('bitsandbytes')} · gradio {gr.__version__} · python {env.get('python')}"),
          ("TEST709 engine",f"709.py git blob {SOURCES.get('709.py',{}).get('git_blob')} · verified · executed unchanged"),
          ("Cartridges",", ".join(f"{b['id']} {b.get('cartridge_file_bytes',0):,} B" for b in R.get("books",[]))+" · forged in this session"),
          ("Live engine status",f"{R.get('status')} · {len(R.get('trials',[]))} protocol trials · engine checks {sum(1 for c in R.get('checks',[]) if c.get('pass'))}/{len(R.get('checks',[]))}"),
          ("Live verification",f"{v.get('passed')}/{v.get('total')} passed"),
          ("Generation",f"greedy · at most {E.get('MAX_NEW')} new tokens · prefix {E.get('P')} tokens"),
          ("Engine ready",f"{INIT.get('ready_utc')} · start-up {INIT.get('total_seconds',0)/60:.1f} min")]
    return card_html("Engine (measured at start-up in this session)",'<table class="tbl">'+"".join(f"<tr><th>{esc(a_)}</th><td class='mono'>{esc(b)}</td></tr>" for a_,b in rows)+"</table>","on")

def stages_html():
    """the start-up research run, stage by stage, as actually completed (Mistral v1.4 stage list)"""
    done={s["step"]:s for s in INIT["steps"]};out=[]
    for i,(key,title) in enumerate(INIT_STEPS.items(),1):
        if key in done:cl,mk,m="done","✓",f" — <span class='small'>{done[key]['seconds']:.0f} s</span>"
        elif INIT.get("failed") and INIT["failed"]["step"]==key:cl,mk,m="fail","✗",f" — <span class='small'>{esc(INIT['failed']['error'])}</span>"
        else:cl,mk,m="wait","○",""
        out.append(f"<div class='stg {cl}'>{mk} {i}/{len(INIT_STEPS)} · {esc(title)}{m}</div>")
    pc=100.0*len(done)/len(INIT_STEPS)
    bar=f'<div style="margin-top:6px;background:#e5e7eb;height:10px"><div style="width:{pc:.0f}%;height:10px;background:#0f766e"></div></div>'
    v=STATE.get("verification") or {}
    ver="".join(f"<div class='small'>{'✓' if i['passed'] else '✗'} <span class='mono'>{esc(i['name'])}</span></div>" for i in v.get("items",[]))
    return card_html(f"Full research run at start-up · completed in {INIT.get('total_seconds',0)/60:.1f} min · live verification {v.get('passed')}/{v.get('total')}","".join(out)+bar+
                     "<div style='margin-top:8px'><b>Live verification</b></div>"+ver,"on" if INIT.get("ready") else "err")

def condition_info(combo):
    R=E.get("R",{});cur="+".join(STATE["order"])
    books="".join(f"<br>{chips([b['id']])} <b>{esc(b.get('title'))}</b> · first {b.get('requested_tokens'):,} tokens · SHA-256 <span class='mono'>{esc(str(b.get('cartridge_sha256'))[:16])}…</span>" for b in R.get("books",[]))
    note=(f"Mounted now: {chips(STATE['order'])}" +(f" · {STATE['stages'][-1]['cache_tokens']:,} rows" if STATE["stages"] else "")+
          ("" if combo==cur else f"<br><b>Selected {esc(combo)}</b> — pressing ASK releases the memory and rebuilds it from the SSD cartridges in this order (about 20–80 s)."))
    qs="".join(f"<br><span class='mono'>{esc(t['label'])}</span> {esc(t['questions'][0])}" for t in _SEG.get("trials",[]))
    return card_html("Memory condition",note+"<br><br><b>Cartridges on SSD (this session)</b>"+books+"<br><br><b>Questions of the TEST709 protocol</b> (already run at start-up; you may ask any question)"+qs,"info")

def answer_html(r,c,stages=None):
    t=""
    if stages:
        t+=("<div class='small'><b>Memory rebuilt</b></div><table class='tbl'><tr><th>book</th><th>step</th><th class='hide-m'>SSD s</th><th class='hide-m'>H2D ms</th><th>rebuild s</th><th>rows</th><th>prior K/V SHA-256</th></tr>"+
            "".join(f"<tr><td>{chips([s['book']])}</td><td>{esc(s['operation'])}</td><td class='hide-m mono'>{s['ssd_load_ms']/1000:.2f}</td><td class='hide-m mono'>{s['h2d_ms']:.0f}</td>"
                    f"<td class='mono'>{s['rebuild_ms']/1000:.1f}</td><td class='mono'>{s['cache_tokens']:,}</td><td>{'PASS (engine log)' if s['prior_kv_sha256_pass_line'] else ('—' if s['prior_kv_sha256_pass_line'] is None else 'missing')}</td></tr>" for s in stages)+"</table>")
    t+=(f"<table class='tbl'><tr><th>memory</th><th>raw model answer</th><th class='hide-m'>time</th></tr>"
        f"<tr><td>{chips(r['memory_order'])}<div class='small mono'>{r['cache_tokens']:,} rows</div></td><td><div class='ans'>{esc(r['raw'])}</div></td><td class='hide-m mono'>{r['seconds']} s</td></tr>")
    if c is not None:t+=f"<tr><td><b>control</b><div class='small'>no memory</div></td><td><div class='ans'>{esc(c['raw'])}</div></td><td class='hide-m mono'>{c['seconds']} s</td></tr>"
    t+="</table>"
    t+=(f"<div class='small mono' style='margin-top:8px;opacity:.8'>question {esc(r['question'])}<br>max new tokens {r['max_new_tokens']} · semantics UNSCORED · GPU free {r['gpu'].get('free_gib')} GiB · "
        f"allocated {r['gpu'].get('allocated_gib')} GiB · {esc(r['utc'])}</div>")
    return card_html("Answer of the frozen Qwen2.5-72B — raw output, unedited",t,"on")

GPU_LOCK=threading.Lock()
def busy_card():return card_html("Busy","Another run is using the GPU. Please wait until it has finished and press the button again.","warn")
def err_card(ex):
    oom="OutOfMemoryError" in type(ex).__name__ or "GPU_SAFETY_STOP" in str(ex)
    hint=" The TEST709 GPU safety reserve stopped the operation (or CUDA ran out of memory); the memory was released. Choose fewer cartridges and press ASK again." if oom else ""
    return card_html("Error",f"<code>{esc(type(ex).__name__)}: {esc(ex)}</code>{esc(hint)}<br>Nothing was hidden or replaced; the full traceback is in the Error log tab.","err")

def all_files():
    """individual downloads (Mistral v1.4 list): six JPEG figures, ZIP, run summary, manifest, live logs and records,
    and the historical 709.log (clearly named HISTORICAL_…)"""
    figs=[FIG_FILES[k]["jpg"] for k in FIGURES if k in FIG_FILES]
    return figs+[str(ZIP_PATH)]+[p for _,p in download_items() if Path(p).is_file()]
def gallery_items():return [(FIG_FILES[k]["jpg"],FIGURES[k]) for k in FIGURES if k in FIG_FILES]
def summary_text():
    try:return RUN_SUMMARY.read_text(encoding="utf-8")
    except Exception:return ""
def refresh_package():
    try:package_session()
    except Exception as ex:slog("PACKAGE_FAILED",str(ex))
    return all_files(),(str(ZIP_PATH) if ZIP_PATH.is_file() else None),summary_text()

def ask_handler(combo,question,control):
    NO=("","",None)
    if not GPU_LOCK.acquire(blocking=False):yield (busy_card(),)+NO+(gr.update(),gr.update(),gr.update(),condition_info(combo));return
    try:
        q=(question or "").strip()
        if not q:raise OpError("Type a question first.")
        books=combo_books(combo);stages=None
        if books!=STATE["order"] or STATE["memory"] is None:
            yield (card_html("Running",f"Rebuilding memory {esc(combo)} from the SSD cartridges (TEST709 cart_load → initialize → append) …","info"),)+NO+(gr.update(),gr.update(),gr.update(),condition_info(combo))
            stages=build_memory(books)
        yield (card_html("Running",f"Memory {esc('+'.join(STATE['order']))} · asking the frozen model{' and the no-memory control' if control else ''} …","info"),)+NO+(gr.update(),gr.update(),gr.update(),condition_info(combo))
        r=ask(q[:2000],True);c=ask(q[:2000],False) if control else None
        rec=dict(question=q,memory=r,control=c,stages=stages,session=SESSION_ID)
        d=SESSION_DIR/"single_runs";d.mkdir(exist_ok=True)
        p=dump_json(d/f"ASK_{'_'.join(STATE['order'])}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json",rec)
        files,z,summ=refresh_package()
        yield (answer_html(r,c,stages),json.dumps(jsafe(rec),ensure_ascii=False,indent=1)[:200000],"",str(p),files,z,summ,condition_info(combo))
    except Exception as ex:
        slog("UI_ERROR","ask",error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc()[-3000:])
        files,z,summ=refresh_package()
        yield (err_card(ex),"",traceback.format_exc(),None,files,z,summ,condition_info(combo))
    finally:GPU_LOCK.release()

def verify_handler():
    if not GPU_LOCK.acquire(blocking=False):return busy_card()
    try:
        w=verify_weights();d=verify_disk()
        rows=[("time (UTC)",w["utc"]),("weight sentinel at load",w["before"]),("weight sentinel now",w["after"]),("sentinel unchanged",w["passed"]),
              ("trainable tensors",sum(1 for p in E["model"].parameters() if p.requires_grad))]+[(f"cartridge {f['book']} SHA-256 on disk = engine record",f["equals_engine_record"]) for f in d["files"]]
        ok=w["passed"] and d["passed"] and rows[4][1]==0
        return card_html("Weight and cartridge verification · measured now","<table class='tbl'>"+"".join(f"<tr><th>{esc(a)}</th><td class='mono'>{esc(b)}</td></tr>" for a,b in rows)+"</table>","on" if ok else "err")
    except Exception as ex:return err_card(ex)
    finally:GPU_LOCK.release()

def _tb(**kw):
    for extra in (([{"buttons":["copy"]}] if _GR_MAJOR>=6 else [])+[{"show_copy_button":True},{}]):
        try:return gr.Textbox(**extra,**kw)
        except TypeError:continue
def _gallery(**kw):
    try:return gr.Gallery(columns=1,height="auto",object_fit="contain",preview=False,**kw)
    except TypeError:return gr.Gallery(**kw)

def build_ui():
    blocks=gr.Blocks(title=APP_SHORT) if _GR_MAJOR>=6 else gr.Blocks(css=CSS,title=APP_SHORT)
    with blocks as demo:
        gr.HTML(HERO);gr.HTML(engine_card_html())
        cond_dd=gr.Dropdown(choices=COMBOS,value="A+B+C",label="Memory condition (which cartridges are mounted, in order)",interactive=True)
        info=gr.HTML(condition_info("A+B+C"))
        cq=gr.Textbox(value="",label="Question (answered from the selected memory; not scored)",placeholder="e.g. Who is Robert Walton?",lines=1,max_lines=3)
        ctl=gr.Checkbox(value=True,label="Also ask the same question without memory (no-memory control)")
        ask_b=gr.Button("ASK",variant="primary",elem_id="kz_ask")
        status=gr.HTML(stages_html())
        gallery=_gallery(label="Figures 1–6 (JPEG, 300 dpi) — measured in this session",value=gallery_items())
        files=gr.File(label="Individual downloads · figures, ZIP, run summary, manifest, live logs, raw answers, historical 709.log",value=all_files(),file_count="multiple",interactive=False)
        zipb=gr.DownloadButton(label="⬇ Download the complete experiment package (.zip)",value=str(ZIP_PATH),interactive=True)
        single_file=gr.File(label="Record of the last question (.json)",interactive=False)
        with gr.Tabs():
            with gr.Tab("Run summary"):summ=_tb(lines=14,max_lines=40,label="RUN_SUMMARY.txt",value=summary_text())
            with gr.Tab("Raw record (last question)"):raw=_tb(lines=14,max_lines=40,label="JSON")
            with gr.Tab("Error log"):errs=_tb(lines=10,max_lines=40,label="traceback (empty = no error)")
        with gr.Accordion("Verify the frozen weights and the cartridge files now",open=False):
            vb=gr.Button("Verify now");vout=gr.HTML()
        gr.HTML(SCOPE_HTML)
        gr.HTML(f'<div class="kz small" style="opacity:.8;margin:8px 0 18px">{esc(AUTHOR)} · {esc(ORG)} · {esc(LICENSE_NAME)} · '
                f'TEST709 <a href="{URL_709}" target="_blank" rel="noopener">709.py</a> · historical record <a href="{URL_709_LOG}" target="_blank" rel="noopener">709.log</a> · '
                f'Qwen2.5-72B-Instruct and third-party libraries remain under their own licences.</div>')
        cond_dd.change(condition_info,inputs=cond_dd,outputs=info)
        outs=[status,raw,errs,single_file,files,zipb,summ,info]
        ask_b.click(ask_handler,inputs=[cond_dd,cq,ctl],outputs=outs);cq.submit(ask_handler,inputs=[cond_dd,cq,ctl],outputs=outs)
        vb.click(verify_handler,outputs=vout)
    try:demo.queue(default_concurrency_limit=1)
    except TypeError:demo.queue(concurrency_count=1)
    return demo

# ---------------------------------------------------------------------------------------------------------------------
# START-UP (as in Mistral v1.4): the engine runs automatically, then the interface opens
# ---------------------------------------------------------------------------------------------------------------------
_GR_MAJOR=int(re.match(r"\d+",gr.__version__).group())
try:run_initialization()
except Exception as _ex:
    _m=str(_ex)
    _hint=("A locked source changed on GitHub — the program stops instead of running unverified code." if "LOCKED SOURCE" in _m else
           "Hugging Face refused the model download: add your token as the Colab secret HF_TOKEN (allow notebook access) and run again." if any(x in _m for x in ("401","403","gated","Unauthorized","token")) else
           "GPU memory: the TEST709 safety reserve or CUDA stopped the run. Use an A100 80 GB runtime (Runtime → Change runtime type), restart the session and run again." if any(x in _m for x in ("GPU_SAFETY_STOP","out of memory","KV_ONLY_ESTIMATE")) else
           "This runtime is not an A100 80 GB: Runtime → Change runtime type → A100, then run again." if any(x in _m for x in ("A100","CUDA is not available","exactly one GPU")) else
           "Disk: free space in the Colab runtime (or use a runtime with more disk) and run again." if "disk" in _m.lower() else
           "Network error while downloading a locked source, a book or the model: run the cell again." if any(x in _m for x in ("URLError","timed out","HTTP Error","Connection")) else
           "See the traceback above; nothing was changed in the engine.")
    print("\n"+"="*110+f"\nENGINE START FAILED — {type(_ex).__name__}: {_m}\nWHAT TO DO: {_hint}\nRecords of this attempt: {SESSION_DIR}\n"+"="*110,flush=True)
    raise
demo=build_ui()
slog("LAUNCH","public share link — open the printed gradio.live address (also works on a phone)")
_LAUNCH=dict(share=True,allowed_paths=[str(DEMO_ROOT)],show_error=True,inline=False)
if _GR_MAJOR>=6:_LAUNCH["css"]=CSS
try:demo.launch(**_LAUNCH)
except TypeError as _ex:
    if "css" not in str(_ex):raise
    _LAUNCH.pop("css",None);demo.launch(**_LAUNCH)
