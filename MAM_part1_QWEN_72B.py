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
