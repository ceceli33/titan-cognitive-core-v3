# =====================================================================================================================
# AKBASCORE AI TECHNOLOGY — SILICON HIPPOCAMPUS · Qwen2.5-72B-Instruct / SIEMENS SINUMERIK ONE PHYSICAL MEMORY
# Live research demonstration of the TEST718 experiment (ten physical CUT3 cartridges of a real industrial manual)
# single Google Colab cell (3 parts) · NVIDIA A100 80 GB · same working method as the previous Qwen2.5-72B demonstration
# PART 1 / 3 — Engine Initialization, Source Document and Physical Cartridge Infrastructure
# ---------------------------------------------------------------------------------------------------------------------
# HOW TO RUN: paste PART 1, PART 2 and PART 3 one below the other into ONE Colab cell and press RUN once.
# Without any button, in this order:
#   [1] verified sources      718.py, 716.py, 709.py (git blob locks), LICENSE, published logs 716/717/718 (historical only)
#   [2] system preflight      one A100 80 GB, RAM, disk, Hugging Face cache state and model identity of Qwen2.5-72B-Instruct
#   [3] source document       the ORIGINAL Siemens PDF from the official Siemens address: download time (UTC), size,
#                             pages, SHA-256 (must equal the TEST716 lock), PDF metadata, edition marking on the pages
#   [4] TEST718 experiment    718.py executed UNCHANGED from its verified source. It runs the unchanged TEST716 set-up
#                             (PDF lock, 10 page ranges, heading panel, frozen 72B NF4 model, ten CUT3 cartridges forged
#                             with the unchanged TEST709 engine and saved to SSD with SHA-256), then 10 vanilla answers,
#                             10 physical readouts (one cartridge at a time: SSD → GPU → rebuild → answer → release),
#                             3 removal controls, the H3 cosine map, the text-mediated synthesis and the weight check.
#                             Every engine line is shown live and stored with its UTC time stamp.
#   [5] ten-cartridge X-ray   each cartridge mounted ALONE (cart_load → initialize, as in TEST718), its live 80-layer
#                             K and V tensors measured read-only on the GPU, then released — never jointly in memory
#   [6] live verification     engine checks, cartridge SHA-256 on disk, readouts, controls, X-rays, weights, GPU reserve
#   [7] ready memory          cartridge C01 mounted on the GPU exactly as TEST718 mounts it (cart_load → initialize)
#   [8] figures + downloads   seven JPEG figures from THIS run's records, automatic layout quality control of every
#                             JPEG, logs, manifest, Download-All ZIP
#   While TEST718 runs, a heartbeat line every 60 s shows elapsed time, the last engine line, GPU memory (nvidia-smi),
#   RAM and the size of the model download, so a stalled or interrupted run can be diagnosed from the records.
#   → then the Gradio interface opens. Any failure stops here and is reported; no interface is presented as ready.
# Scientific boundaries
#   · Model answers are NOT verified technical truth. Page numbers, section numbers and content are checked only
#     automatically (stated page vs. heading page, verbatim word overlap with the source pages); not by an expert.
#   · Questions contain the section heading (TEST716 panel): this is not blind question answering.
#   · The ten cartridges are read ONE AT A TIME. The synthesis is text-mediated: the frozen model reads the ten text
#     answers with NO cartridge attached. It is not native multi-cartridge neural synthesis.
#   · Multi-cartridge consolidation in one live K/V memory was demonstrated earlier (Research Record III, Zenodo 23434686)
#     and is not repeated here.
# Status          This demonstration code has NOT been executed on a GPU by its author (CPU simulation only).
# Author/licence  Mustafa Akbaş · AkbasCore AI Teknoloji · Mersin, Türkiye
#                 Copyright © 2026 Mustafa Akbaş · AKBASCORE RESEARCH SOFTWARE LICENSE
#                 https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/LICENSE
#                 The Siemens manual remains the property of Siemens AG. It is downloaded from the official Siemens
#                 address at run time and verified by SHA-256. Siemens' terms restrict passing documents on to third
#                 parties, so the public interface offers the official Siemens link + the verification record instead of
#                 the file; the verified copy stays only inside this Colab runtime (path printed in the output). Qwen2.5-72B-Instruct and third-party libraries
#                 remain governed by their own licences.
# =====================================================================================================================
import os,sys,re,io,ast,json,time,html,math,shutil,zipfile,hashlib,platform,threading,traceback,subprocess,importlib.util,textwrap,copy
from pathlib import Path
from datetime import datetime,timezone,date
from collections import Counter,OrderedDict

def _pip(*pk):subprocess.check_call([sys.executable,"-m","pip","install","-q",*pk])
for _m,_p in (("numpy","numpy"),("matplotlib","matplotlib"),("PIL","pillow"),("pymupdf","pymupdf")):
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
import pymupdf
import gradio as gr
os.environ.pop("HF_HUB_DISABLE_PROGRESS_BARS",None)          # keep the real download progress bars visible in Colab

# ---------------------------------------------------------------------------------------------------------------------
# identity, sources, locks and research lineage
# ---------------------------------------------------------------------------------------------------------------------
APP_TITLE="AKBASCORE AI TECHNOLOGY — SILICON HIPPOCAMPUS · Qwen2.5-72B / SIEMENS SINUMERIK ONE"
APP_SHORT="AKBASCORE Silicon Hippocampus · Qwen2.5-72B · Siemens SINUMERIK ONE"
VERSION_NOTE="new experiment — unpublished, no DOI"
AUTHOR="Mustafa Akbaş";ORG="AkbasCore AI Teknoloji";PLACE="Mersin, Türkiye"
LICENSE_NAME="AKBASCORE RESEARCH SOFTWARE LICENSE";COPYRIGHT="Copyright © 2026 Mustafa Akbaş"
REPO="https://github.com/ceceli33/titan-cognitive-core-v3"
RAW_BASE="https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
URL_LICENSE=REPO+"/blob/main/LICENSE";URL_718=REPO+"/blob/main/718.py";URL_716=REPO+"/blob/main/716.py";URL_709=REPO+"/blob/main/709.py"
URL_PREV_DEMO=REPO+"/blob/main/MAM_part1_QWEN_72B.py"
# git blob identifiers (git hash-object) of the files this program trusts
LOCKS=OrderedDict([
    ("718.py","dabbb68008c40fe5312629d5e56ad8971d9121b7"),    # TEST718 experiment (executed unchanged)
    ("716.py","913fa7a4951f2072df4be2eb49120ea86efa5477"),    # TEST716 set-up (locked inside 718.py as well)
    ("709.py","6c9f8cbb1eeed848d45133d73f0d7676b68e9125"),    # TEST709 CUT3 engine functions (locked inside 716.py)
    ("LICENSE","9aad4724d1072f9e56486650a9527380c867a53b"),
    ("716.log","1b87e698a0420bb524bd93854709cef9e4069484"),   # historical: earlier TEST716 run (routing comparison)
    ("717.log","2f6225db7346854e9cebded269b002293a93392d"),   # historical: earlier TEST717 run (80-layer routing X-ray)
    ("718.log","25c96ade2942727289530526b7fe15dd9beddc02")])  # historical: earlier TEST718 run (not this session)
HISTORICAL=("716.log","717.log","718.log")
ENGINE_PASS_STATUS="COMPLETE_SEQUENTIAL_PHYSICAL_READOUT_AND_TEXT_SYNTHESIS"
EXPECTED_ARCH=(80,8192,64,8,128);EXPECTED_CUT=3;EXPECTED_RESERVE_GIB=9.0;N_CART=10;READOUT_MAX_NEW=144;SYNTH_MAX_NEW=480
# the original document (the SHA-256 is the TEST716 lock; this program checks it independently as well)
PDF_URL="https://cache.industry.siemens.com/dl/files/087/109994087/att_1338962/v1/ONE_universal_op_man_0725_en-US.pdf"
PDF_SHA256="88c0f8293ce3302135042baf35d704303fb3b5a24915e28b8ca16f3192a7cc1d";PDF_PAGES=486
PDF_TERMS_URL="https://support.industry.siemens.com/dokumentation/ExtendedAGB.aspx"
PDF_POLICY=("Not redistributed: Siemens terms restrict passing documents on to third parties (e.g. section 2.3 of the Siemens "
            "documentation terms). Download it from the official Siemens address and compare its SHA-256 with this record.")
DOC_TITLE="SINUMERIK ONE Universal Operating Manual";DOC_EDITION_MARK="07/2025";DOC_EDITION_TEXT="July 2025"
# the model and its first public release (documentary fact checked by the code author; the run re-reads Hugging Face)
MODEL_ID="Qwen/Qwen2.5-72B-Instruct"
MODEL_RELEASE=dict(date="2024-09-19",event="first public release of the Qwen2.5 family incl. Qwen2.5-72B-Instruct",
                   source="Qwen Team, “Qwen2.5: A Party of Foundation Models!”, blog post dated September 19, 2024",
                   url="https://qwenlm.github.io/blog/qwen2.5/",checked="checked by the code author on 2026-10-18 (web); not re-checked at run time")
# research lineage (published records) and the required reference to the earlier multi-cartridge demonstration
LINEAGE=[("Research Record I — Qwen2.5-7B","https://doi.org/10.5281/zenodo.23381336"),
         ("Research Record II — Mistral-7B, Silicon Hippocampus v1.4","https://doi.org/10.5281/zenodo.23418927"),
         ("Research Record III — Qwen2.5-72B, Direct Internal-State Injection","https://doi.org/10.5281/zenodo.23434686")]
PREV_TITLE="PREVIOUSLY DEMONSTRATED — MULTI-CARTRIDGE MEMORY CONSOLIDATION"
PREV_TEXT=("The physical consolidation of three independent memory cartridges into a single live 80-layer K/V memory has already been "
           "demonstrated on frozen Qwen2.5-72B-Instruct, including sequential cartridge mounting, exact SHA-256 integrity verification, "
           "and internal memory X-ray measurements.")
PREV_SEE=("For the implementation, experimental evidence, and multi-cartridge question-answering observations, see: "
          "Research Record III — Qwen2.5-72B, Direct Internal-State Injection · Zenodo Record 23434686 · https://zenodo.org/records/23434686")
CART_COLORS=["#1D4ED8","#BE185D","#B45309","#047857","#6D28D9","#0E7490","#B91C1C","#4D7C0F","#A16207","#475569"]
def ccol(i):return CART_COLORS[i%len(CART_COLORS)]
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
# demonstration directories and the SEPARATE session log (the engine output is stored separately, line by line)
# ---------------------------------------------------------------------------------------------------------------------
DEMO_ROOT=Path("/content/AKBASCORE_SIEMENS_DEMO") if os.path.isdir("/content") else Path("/tmp/AKBASCORE_SIEMENS_DEMO")
SESSION_ID=datetime.now().astimezone().strftime("SIEM-%Y%m%d-%H%M%S")
SESSION_DIR=DEMO_ROOT/"sessions"/SESSION_ID;EVIDENCE_DIR=DEMO_ROOT/"evidence";FIG_DIR=SESSION_DIR/"figures"
LIVE_DIR=SESSION_DIR/"live_engine";HIST_DIR=SESSION_DIR/"historical_reference_not_this_session";PRIVATE_DIR=DEMO_ROOT/"source_document_not_redistributed"
for _d in (SESSION_DIR,EVIDENCE_DIR,FIG_DIR,LIVE_DIR,HIST_DIR,PRIVATE_DIR):_d.mkdir(parents=True,exist_ok=True)
SESSION_LOG=SESSION_DIR/"SESSION.log";SESSION_EVENTS=SESSION_DIR/"SESSION_EVENTS.jsonl";FIGURE_LOG=SESSION_DIR/"FIGURE_GENERATION.log"
SESSION_QA=SESSION_DIR/"SESSION_QA.jsonl";VERIFY_FILE=SESSION_DIR/"VERIFICATION_RECORD.json";INIT_FILE=SESSION_DIR/"INITIALIZATION_RECORD.json"
DOC_FILE=SESSION_DIR/"SOURCE_DOCUMENT_RECORD.json";MODEL_FILE=SESSION_DIR/"MODEL_IDENTITY_RECORD.json";DATES_FILE=SESSION_DIR/"DATE_COMPARISON_RECORD.json"
LIVE_ENGINE_LOG=LIVE_DIR/"LIVE_TEST718_ENGINE_OUTPUT_this_session.log";LIVE_ENGINE_TS=LIVE_DIR/"LIVE_TEST718_ENGINE_OUTPUT_with_UTC_timestamps_this_session.tsv"
LIVE_ENGINE_JSON=LIVE_DIR/"LIVE_TEST718_RESULTS_this_session.json";LIVE_SETUP_JSON=LIVE_DIR/"LIVE_TEST716_SETUP_RECORD_this_session.json"
_LOG_LOCK=threading.Lock()
def slog(kind,message="",**data):
    """session log: one human-readable line + one JSON event; never written into the engine output"""
    ev=dict(utc=utc_now(),kind=kind,message=str(message),data=jsafe(data))
    line=f"{ev['utc']} {kind:<18} {message}"+(f" {json.dumps(jsafe(data),ensure_ascii=False)}" if data else "")
    with _LOG_LOCK:
        with SESSION_LOG.open("a",encoding="utf-8") as f:f.write(line+"\n")
        with SESSION_EVENTS.open("a",encoding="utf-8") as f:f.write(json.dumps(ev,ensure_ascii=False)+"\n")
    _OUT.write(line[:600]+"\n");_OUT.flush();return ev
def flog(message):
    with _LOG_LOCK:
        with FIGURE_LOG.open("a",encoding="utf-8") as f:f.write(f"{utc_now()} {message}\n")
_OUT=sys.stdout

# ---------------------------------------------------------------------------------------------------------------------
# progress display in the Colab output (one banner per initialization step)
# ---------------------------------------------------------------------------------------------------------------------
INIT=dict(started=time.perf_counter(),started_utc=utc_now(),steps=[],current=None,last_ok=None,ready=False,failed=None)
INIT_STEPS=OrderedDict([
    ("SOURCES","Verified sources (engine locks, licence, historical logs)"),
    ("PREFLIGHT","System preflight: GPU, RAM, disk, model cache and model identity"),
    ("DOCUMENT","Original Siemens PDF: download, SHA-256, pages, edition marking"),
    ("EXPERIMENT","TEST718 experiment, executed unchanged (model, 10 cartridges, readouts, controls, synthesis)"),
    ("XRAY","Ten-cartridge X-ray: each cartridge mounted ALONE, K/V measured read-only on the GPU, released"),
    ("VERIFY","Live verification of the experiment records"),
    ("READY_MEMORY","Ready memory: cartridge C01 mounted on the GPU"),
    ("FIGURES","Seven research figures and downloadable research artifacts")])
def _gpu_short():
    try:
        g=E["mem"]() if callable(E.get("mem")) else None
        return f"GPU free {g['free_gib']:.2f} GiB · allocated {g['allocated_gib']:.2f} GiB · peak {g['peak_gib']:.2f} GiB" if g else ""
    except Exception:return ""
def banner(text,ch="─"):_OUT.write("\n"+ch*112+f"\n{text}\n"+ch*112+"\n");_OUT.flush()
def step_begin(key):
    i=list(INIT_STEPS).index(key)+1;n=len(INIT_STEPS);INIT["current"]=key;el=time.perf_counter()-INIT["started"]
    banner(f"[{i}/{n}] {INIT_STEPS[key]}\n      started {local_now()} · {el/60:.1f} min since start · {_gpu_short()}","═")
    slog("STEP_START",key,title=INIT_STEPS[key]);return time.perf_counter()
def step_done(key,t0,**info):
    s=round(time.perf_counter()-t0,2);INIT["steps"].append(dict(step=key,title=INIT_STEPS[key],seconds=s,utc=utc_now(),**jsafe(info)));INIT["last_ok"]=key
    _OUT.write(f"──── ✔ {key} finished in {s/60:.1f} min ({s:.1f} s) · {_gpu_short()}\n");_OUT.flush()
    slog("STEP_DONE",key,seconds=s,**info)

# ---------------------------------------------------------------------------------------------------------------------
# verified downloads
# ---------------------------------------------------------------------------------------------------------------------
SOURCES={}
def fetch_locked(name,timeout=180):
    """download from the repository, check the git blob against LOCKS, keep a verified copy under evidence/"""
    import urllib.request
    p=EVIDENCE_DIR/name
    if p.is_file() and git_blob(p.read_bytes())==LOCKS[name]:raw=p.read_bytes()
    else:
        req=urllib.request.Request(RAW_BASE+name,headers={"User-Agent":"AKBASCORE-SIEMENS-DEMO"})
        with urllib.request.urlopen(req,timeout=timeout) as f:raw=f.read()
        if git_blob(raw)!=LOCKS[name]:
            raise RuntimeError(f"LOCKED SOURCE CHANGED: {name} git blob {git_blob(raw)} != {LOCKS[name]} — the program stops instead of using an unverified file")
        p.write_bytes(raw)
    SOURCES[name]=dict(bytes=len(raw),git_blob=git_blob(raw),sha256=sha_bytes(raw),url=RAW_BASE+name,local=str(p),verified_utc=utc_now())
    return raw

# ---------------------------------------------------------------------------------------------------------------------
# system preflight and model identity (read-only)
# ---------------------------------------------------------------------------------------------------------------------
def model_cache_report(model_id=MODEL_ID):
    """local Hugging Face cache state (shards, bytes to download) and the commit of the cached snapshot"""
    rep=dict(model_id=model_id,cache_dir=None,shards=None,cached_shards=None,total_bytes=None,missing_bytes=None,cached_snapshot_commit=None,note=None)
    try:
        from huggingface_hub import try_to_load_from_cache
        try:
            from huggingface_hub.constants import HF_HUB_CACHE;rep["cache_dir"]=str(HF_HUB_CACHE)
        except Exception:pass
    except Exception as ex:rep["note"]=f"huggingface_hub not importable: {ex}";return rep
    sizes=None
    try:
        from huggingface_hub import HfApi
        info=HfApi().model_info(model_id,files_metadata=True);sizes={s.rfilename:s.size for s in info.siblings}
    except Exception as ex:rep["note"]=f"file sizes not available from the Hub: {type(ex).__name__}"
    cfg=try_to_load_from_cache(model_id,"config.json")
    if isinstance(cfg,str):
        m=re.search(r"snapshots[\\/]+([0-9a-f]{40})",cfg);rep["cached_snapshot_commit"]=m.group(1) if m else None
    idx=try_to_load_from_cache(model_id,"model.safetensors.index.json")
    if isinstance(idx,str):shards=sorted(set(json.loads(Path(idx).read_text())["weight_map"].values()))
    elif sizes:shards=sorted(f for f in sizes if f.endswith(".safetensors"))
    else:return rep
    cached=[s for s in shards if isinstance(try_to_load_from_cache(model_id,s),str)]
    rep.update(shards=len(shards),cached_shards=len(cached))
    if sizes and all(s in sizes for s in shards):
        rep["total_bytes"]=sum(sizes[s] or 0 for s in shards);rep["missing_bytes"]=sum(sizes[s] or 0 for s in shards if s not in cached)
    return rep

MODEL_IDENTITY={}
def model_identity_hub():
    """repository facts read from Hugging Face now (creation of a repository is not its public release)"""
    out=dict(model_id=MODEL_ID,documented_public_release=MODEL_RELEASE,hub_checked_utc=utc_now())
    try:
        from huggingface_hub import HfApi
        info=HfApi().model_info(MODEL_ID)
        out.update(hub_main_commit=getattr(info,"sha",None),hub_repo_created=str(getattr(info,"created_at",None) or getattr(info,"createdAt",None)),
                   hub_last_modified=str(getattr(info,"last_modified",None) or getattr(info,"lastModified",None)),hub_note="read from the Hugging Face API at run time")
    except Exception as ex:out.update(hub_main_commit=None,hub_repo_created=None,hub_last_modified=None,hub_note=f"Hugging Face API not reachable: {type(ex).__name__} — not verified at run time")
    MODEL_IDENTITY.update(out);return out

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
    rep["model_cache"]=model_cache_report();rep["model_identity"]=model_identity_hub()
    cd=rep["model_cache"].get("cache_dir") or str(Path.home()/".cache"/"huggingface"/"hub");Path(cd).mkdir(parents=True,exist_ok=True)
    rep["cache_disk_free_gib"]=round(shutil.disk_usage(cd).free/2**30,1);rep["demo_disk_free_gib"]=round(shutil.disk_usage(DEMO_ROOT).free/2**30,1)
    mc=rep["model_cache"]
    if mc.get("shards"):
        state="FULLY CACHED — no download needed" if mc["cached_shards"]==mc["shards"] else ("NOT CACHED — full download" if mc["cached_shards"]==0 else "PARTIALLY CACHED")
        extra=f" · {gib(mc['missing_bytes']):.1f} GiB still to download" if mc.get("missing_bytes") is not None else ""
        rep["model_cache_state"]=f"{state}: {mc['cached_shards']}/{mc['shards']} weight shards in {mc.get('cache_dir')}{extra}"
    else:rep["model_cache_state"]="cache state could not be determined ("+str(mc.get("note"))+")"
    mi_=rep["model_identity"]
    for k,v in (("GPU",f"{rep.get('gpu')} · total {rep.get('gpu_total_gib')} GiB · free {rep.get('gpu_free_gib')} GiB · count {rep['gpu_count']}"),("nvidia-smi",rep.get("nvidia_smi")),
                ("RAM",f"{rep.get('ram_available_gib')} / {rep.get('ram_total_gib')} GiB available"),("disk",f"{rep['cache_disk_free_gib']} GiB free for the model cache · {rep['demo_disk_free_gib']} GiB free for the demonstration"),
                ("model cache",rep["model_cache_state"]),("model",f"{MODEL_ID} · public release {MODEL_RELEASE['date']} ({MODEL_RELEASE['url']}) · Hub main commit {mi_.get('hub_main_commit')} · repo created {mi_.get('hub_repo_created')}")):
        _OUT.write(f"  {k:<12}{v}\n")
    _OUT.flush()
    if not rep["cuda"]:raise RuntimeError("PREFLIGHT: CUDA is not available — select a GPU runtime (A100 80 GB)")
    if rep["gpu_count"]!=1:raise RuntimeError(f"PREFLIGHT: exactly one GPU is required, found {rep['gpu_count']}")
    if rep["gpu_total_gib"]<70:raise RuntimeError(f"PREFLIGHT: an A100 80 GB (≥70 GiB) is required; this GPU has {rep['gpu_total_gib']} GiB ({rep.get('gpu')})")
    if mc.get("missing_bytes") is not None and shutil.disk_usage(cd).free<mc["missing_bytes"]+12*2**30:
        raise RuntimeError(f"PREFLIGHT: not enough disk for the model download: need {gib(mc['missing_bytes'])+12:.1f} GiB, free {rep['cache_disk_free_gib']} GiB")
    if shutil.disk_usage(DEMO_ROOT).free<12*2**30:raise RuntimeError("PREFLIGHT: less than 12 GiB free for ten cartridges, logs and figures")
    dump_json(SESSION_DIR/"PREFLIGHT.json",rep);return rep

# ---------------------------------------------------------------------------------------------------------------------
# the ORIGINAL source document — downloaded here from the official Siemens address, measured, never modified
# ---------------------------------------------------------------------------------------------------------------------
DOC={};DOC_PAGES=[]
def document_step():
    import urllib.request
    t0=utc_now();t=time.perf_counter()
    req=urllib.request.Request(PDF_URL,headers={"User-Agent":"AKBASCORE-SIEMENS-DEMO"})
    with urllib.request.urlopen(req,timeout=300) as f:raw=f.read(40_000_000);final_url=getattr(f,"url",PDF_URL);hdr=dict(f.headers.items()) if hasattr(f,"headers") else {}
    t1=utc_now();h=sha_bytes(raw)
    if h!=PDF_SHA256:raise RuntimeError(f"SOURCE DOCUMENT CHANGED: SHA-256 {h} != locked {PDF_SHA256} — stopped")
    (PRIVATE_DIR/"siemens_original.pdf").write_bytes(raw)          # local working copy only; never packaged
    doc=pymupdf.open(stream=raw,filetype="pdf");meta=dict(doc.metadata or {})
    pages=[doc[i].get_text(sort=True) for i in range(len(doc))];DOC_PAGES[:]=pages
    mark=[i+1 for i,t_ in enumerate(pages) if DOC_EDITION_MARK in t_]
    order=None;ver=None
    for t_ in pages[:20]:
        m=re.search(r"\bA5E\d{8}[A-Z]?\s?[A-Z]{0,2}\b",t_);order=order or (m.group(0).strip() if m else None)
        m=re.search(r"\bV\d+\.\d+\s?SP\d+\b",t_);ver=ver or (m.group(0) if m else None)
    foot=re.search(r"Operating Manual,\s*07/2025,\s*(A5E\S+\s?[A-Z]{0,2})",pages[min(11,len(pages)-1)] if pages else "")
    DOC.update(title=DOC_TITLE,url=PDF_URL,final_url=final_url,download_start_utc=t0,download_end_utc=t1,download_seconds=round(time.perf_counter()-t,2),
               bytes=len(raw),sha256=h,sha256_locked=PDF_SHA256,sha256_equals_lock=True,pages=len(doc),pages_expected=PDF_PAGES,
               http_last_modified=hdr.get("Last-Modified"),http_content_type=hdr.get("Content-Type"),
               pdf_metadata={k:meta.get(k) for k in ("format","title","author","subject","creator","producer","creationDate","modDate")},
               edition_mark=DOC_EDITION_MARK,edition_mark_pages=len(mark),edition_mark_first_pages=mark[:8],
               edition_verified_on_document=len(mark)>0,order_number=order,software_version=ver,example_footer=(foot.group(0) if foot else None),
               redistribution=PDF_POLICY,redistribution_terms=PDF_TERMS_URL,verified_local_copy=str(PRIVATE_DIR/"siemens_original.pdf"))
    dump_json(DOC_FILE,DOC)
    for k,v in (("source",PDF_URL),("downloaded",f"{t0} → {t1} UTC · {len(raw):,} bytes · {DOC['download_seconds']} s"),("SHA-256",f"{h} (= TEST716 lock)"),
                ("pages",f"{len(doc)}"),("edition",f"“{DOC_EDITION_MARK}” printed on {len(mark)} of {len(doc)} pages (first on page {mark[0] if mark else '—'}) · order no. {order} · software {ver}"),
                ("PDF metadata",f"created {meta.get('creationDate')} · modified {meta.get('modDate')} · producer {meta.get('producer')}")):
        _OUT.write(f"  {k:<14}{v}\n")
    _OUT.flush()
    if len(doc)!=PDF_PAGES:raise RuntimeError(f"SOURCE DOCUMENT: {len(doc)} pages, expected {PDF_PAGES}")
    return dict(bytes=len(raw),sha256=h,pages=len(doc),edition_mark_pages=len(mark),download_end_utc=t1)

# ---------------------------------------------------------------------------------------------------------------------
# THE TEST718 EXPERIMENT — 718.py executed unchanged in its own namespace E; its output is shown live and recorded
# ---------------------------------------------------------------------------------------------------------------------
E={"__name__":"akbascore_test718_experiment","__file__":"718.py"}
ENGINE=dict(source_loaded=False,done=False,status=None,error=None,seconds=None,started_utc=None,ended_utc=None)
ENGINE_LOCK=threading.RLock()
ENGINE_LINES=[]                                   # (utc iso, seconds since start, line) of every engine output line
STAGE_MARKS=[("PASS TEST716_GIT_BLOB_LOCK","engine sources locked (718 → 716 → 709)"),
             ("TOKEN_COUNTS","PDF parsed into 10 page ranges (token counts below)"),
             ("PASS CUDA_A100_80GB","loading the frozen Qwen2.5-72B-Instruct NF4 — real download / loading progress bars follow"),
             ("PASS FROZEN","model loaded and frozen"),
             ("FORGE ","forging the ten physical CUT3 cartridges and saving them to SSD (SHA-256)"),
             ("REUSE_SHA_VERIFIED","cartridge files found on SSD — reused only after their SHA-256 matched"),
             ("VANILLA ","vanilla model: the same 10 questions with no PDF and no cartridge"),
             ("PHYSICAL ","physical readout: each cartridge SSD → GPU → rebuild → answer → release, one at a time"),
             ("ABLATION ","removal control: questions asked again after the cartridge was released"),
             ("SYNTHESIS ","text-mediated synthesis finished (frozen model, no cartridge attached)"),
             ("PASS WEIGHTS_UNCHANGED","weight sentinel unchanged"),
             ("TEST718_RESULT","TEST718 finished"),("TEST718_ERROR","TEST718 ERROR")]
class _EngineTee(io.TextIOBase):
    """passes every engine line to the Colab output and records it (raw + UTC time stamp); prints a sub-banner at the
    first line of each experiment stage. Read-only: nothing the engine computes is touched."""
    def __init__(s,out):s.out=out;s.buf="";s.t0=time.perf_counter();s.seen=set();s.abl=0
    def writable(s):return True
    def write(s,x):
        s.buf+=str(x)
        while "\n" in s.buf:
            line,s.buf=s.buf.split("\n",1);s._line(line)
        return len(x)
    def _line(s,line):
        ts=utc_now();el=round(time.perf_counter()-s.t0,3);ENGINE_LINES.append((ts,el,line))
        for pre,title in STAGE_MARKS:
            if line.startswith(pre) and pre not in s.seen:
                s.seen.add(pre);s.out.write("\n"+"·"*112+f"\n▶ TEST718 · {title} · {local_now()} · +{el/60:.1f} min · {_gpu_short()}\n"+"·"*112+"\n")
        s.out.write(line+"\n");s.out.flush()
        with LIVE_ENGINE_LOG.open("a",encoding="utf-8") as f:f.write(line+"\n")
        with LIVE_ENGINE_TS.open("a",encoding="utf-8") as f:f.write(f"{ts}\t{el}\t{line}\n")
        if line.startswith("ABLATION "):
            s.abl+=1
            if s.abl==3:s.out.write("\n"+"·"*112+f"\n▶ TEST718 · cosine map of the ten H3 cartridges + text-mediated synthesis (up to {SYNTH_MAX_NEW} tokens, no cartridge) · {local_now()}\n"+"·"*112+"\n");s.out.flush()
    def flush(s):
        if s.buf:s._line(s.buf);s.buf=""
        s.out.flush()

def load_engine_source():
    raw=fetch_locked("718.py");src=raw.decode("utf-8");tree=ast.parse(src)
    for needle in ("LOCK716='"+LOCKS["716.py"]+"'","R718['status']='"+ENGINE_PASS_STATUS+"'","def run_answer(memory,q,max_new=144)"):
        if needle not in src:raise RuntimeError("TEST718 STRUCTURE: expected text not found: "+needle)
    r716=fetch_locked("716.py");fetch_locked("709.py")
    if "PDF_SHA='"+PDF_SHA256+"'" not in r716.decode("utf-8"):raise RuntimeError("TEST716 STRUCTURE: PDF lock differs from this program")
    if os.path.isdir("/content"):Path("/content/716.py").write_bytes(r716)   # the verified, identical 716.py that 718.py reads first
    ENGINE["source"]=src;ENGINE["source_loaded"]=True
    slog("ENGINE_SOURCE","718.py verified",blob=SOURCES["718.py"]["git_blob"],sha256=SOURCES["718.py"]["sha256"],nodes=len(tree.body))
    return src

def run_experiment():
    """executes 718.py unchanged. On error 718.py's own except block records R718['status']='ERROR' and re-raises."""
    with ENGINE_LOCK:
        if not ENGINE["source_loaded"]:load_engine_source()
        ENGINE["started_utc"]=utc_now();t=time.perf_counter();tee=_EngineTee(_OUT);old=sys.stdout;sys.stdout=tee
        stop=threading.Event();hb=threading.Thread(target=_heartbeat,args=(stop,t),daemon=True);hb.start()
        try:exec(compile(ENGINE["source"],"718.py","exec"),E)
        except BaseException as ex:
            ENGINE["error"]=f"{type(ex).__name__}: {ex}";raise
        finally:
            try:tee.flush()
            except Exception:pass
            stop.set();sys.stdout=old;ENGINE["seconds"]=round(time.perf_counter()-t,2);ENGINE["ended_utc"]=utc_now()
            ENGINE["status"]=(E.get("R718") or {}).get("status");sync_engine_records()
        ENGINE["done"]=True
        if ENGINE["status"]!=ENGINE_PASS_STATUS:raise RuntimeError(f"TEST718 status {ENGINE['status']}")
        return dict(status=ENGINE["status"],seconds=ENGINE["seconds"],lines=len(ENGINE_LINES))

HEARTBEAT_FILE=SESSION_DIR/"HEARTBEAT_LAST.json";HEARTBEATS=[]
def _hf_cache_bytes():
    try:
        from huggingface_hub.constants import HF_HUB_CACHE;root=Path(HF_HUB_CACHE)/"models--Qwen--Qwen2.5-72B-Instruct"
    except Exception:root=Path.home()/".cache"/"huggingface"/"hub"/"models--Qwen--Qwen2.5-72B-Instruct"
    tot=0
    for dp,dn,fn in os.walk(root):
        for f in fn:
            try:tot+=os.stat(os.path.join(dp,f),follow_symlinks=False).st_size
            except Exception:pass
    return tot
def _heartbeat(stop,t0,every=60):
    """observer only (no CUDA calls): every 60 s one line with the state of the running experiment, written to the
    Colab output, the session log and HEARTBEAT_LAST.json — so a stalled or interrupted run is diagnosable"""
    while not stop.wait(every):
        try:
            smi=subprocess.run(["nvidia-smi","--query-gpu=memory.used,memory.total,utilization.gpu","--format=csv,noheader,nounits"],capture_output=True,text=True,timeout=20).stdout.strip()
        except Exception:smi=None
        try:
            mi=dict(l.split(":",1) for l in Path("/proc/meminfo").read_text().splitlines() if ":" in l);ram=round(int(mi["MemAvailable"].split()[0])/2**20,1)
        except Exception:ram=None
        last=ENGINE_LINES[-1] if ENGINE_LINES else (None,None,"(no engine output yet)")
        hb=dict(utc=utc_now(),elapsed_min=round((time.perf_counter()-t0)/60,1),engine_lines=len(ENGINE_LINES),last_line_utc=last[0],last_line=str(last[2])[:240],
                gpu_mib_used_total_util=smi,ram_available_gib=ram,model_cache_gib=round(_hf_cache_bytes()/2**30,1))
        HEARTBEATS.append(hb)
        try:dump_json(HEARTBEAT_FILE,dict(hb,note="last heartbeat of the running TEST718 experiment"))
        except Exception:pass
        _OUT.write(f"  ⏱ +{hb['elapsed_min']} min · engine lines {hb['engine_lines']} · last: {hb['last_line'][:90]} · GPU {smi} MiB/%, RAM {ram} GiB free, model cache {hb['model_cache_gib']} GiB\n");_OUT.flush()
        with _LOG_LOCK:
            with SESSION_LOG.open("a",encoding="utf-8") as f:f.write(f"{hb['utc']} HEARTBEAT          {json.dumps(hb,ensure_ascii=False)}\n")

def sync_engine_records():
    """byte-identical copies of the engine's own result files (TEST718_results.json, TEST716_results.json)"""
    try:
        root=Path(str(E.get("ROOT") or "/content/AKBASCORE_TEST714"))
        for src,dst in ((root/"TEST718_results.json",LIVE_ENGINE_JSON),(root/"TEST716_results.json",LIVE_SETUP_JSON)):
            if src.is_file():shutil.copyfile(src,dst)
    except Exception as ex:slog("SYNC_FAILED",str(ex))

def engine_architecture():
    if "model" not in E:return None
    return dict(layers=E["NL"],hidden=E["H"],q_heads=E["QH"],kv_heads=E["KVH"],head_dim=E["HD"],cut=E["CUT"],prefix_tokens=E.get("P"),
                full_kv_bytes_per_token=E["NL"]*E["KVH"]*E["HD"]*2*2,chunk=E["CHUNK"],reserve_gib=E["GPU_RESERVE_GIB"],readout_max_new=READOUT_MAX_NEW,
                weights="NF4 4-bit (bitsandbytes), BF16 compute, frozen",model_id=E["MODEL_ID"])
  

# ---------------------------------------------------------------------------------------------------------------------
# interactive memory state (exclusively owned; one physical cartridge at a time, as in TEST718)
# ---------------------------------------------------------------------------------------------------------------------
STATE=dict(memory=None,cartridge=None,mount=None,xrays={},qa=[],controls=[],ops=[],weight_checks=[],disk_checks=[],verification=None,files={})
SESSION_INFO=dict(session_id=SESSION_ID,started_utc=utc_now(),started_local=local_now(),python=platform.python_version(),platform=platform.platform())
slog("SESSION_START",APP_SHORT,session=SESSION_ID,version_note=VERSION_NOTE,session_dir=str(SESSION_DIR))
# ===== PART 2/3 — paste directly after PART 1 in the same cell =====
# =====================================================================================================================
# PART 2 / 3 — Cartridge Operations, Experiment Records, Integrity and Research Figures
# Interactive operations call the TEST709 engine functions that TEST718 uses (E["cart_load"], E["initialize"],
# E["run_answer"], E["free_gpu"], E["ensure_room"], E["sentinel"]) in the order TEST718 uses them. Nothing here changes CUT3,
# RoPE, the cartridge format, the SHA-256 guards or the GPU reserve. All measurements are read-only and computed from this
# session's engine records (E["R718"], E["R"], the time-stamped engine output) and from the original PDF downloaded now.
# =====================================================================================================================
class OpError(RuntimeError):pass
def _torch():return E["torch"]
def gpu_now():
    try:return E["mem"]()
    except Exception as ex:return {"error":f"{type(ex).__name__}: {ex}"}
def _require():
    if not ENGINE.get("done") or "model" not in E:raise OpError("The TEST718 experiment has not completed in this session.")
def cart_ids():return [b["id"] for b in E["R"]["books"]]
def cart_index(bid):return cart_ids().index(bid)
def ntok(text):
    try:return len(E["tok"](str(text or ""),add_special_tokens=False).input_ids)
    except Exception:return None

def _release(reason):
    had=STATE["memory"] is not None
    STATE["memory"]=None;STATE["cartridge"]=None;STATE["mount"]=None
    try:E["free_gpu"]()
    except Exception:pass
    if had:slog("MEMORY_RELEASED",reason,gpu=gpu_now())

def mount(bid):
    """one physical cartridge on the GPU, exactly as TEST718 mounts it (718.py line 46):
    cart_load(bid) → list(initialize(cp)) → del cp → free_gpu(). The previous memory is released first (one at a time)."""
    with ENGINE_LOCK:
        _require()
        if bid not in cart_ids():raise OpError(f"Unknown cartridge {bid}.")
        _release("new cartridge requested");torch=_torch();t=time.perf_counter();cp=None
        try:
            cp,times=E["cart_load"](bid);t0=time.perf_counter()
            memory=list(E["initialize"](cp));del cp;cp=None;E["free_gpu"]();torch.cuda.synchronize()
        except BaseException as ex:
            if cp is not None:del cp
            _release(f"mount failed: {type(ex).__name__}");slog("MOUNT_FAILED",bid,error=f"{type(ex).__name__}: {ex}");raise
        times["rebuild_ms"]=round((time.perf_counter()-t0)*1000,3);times["end_to_end_ms"]=round((time.perf_counter()-t)*1000,3)
        times.update(cartridge=bid,cache_tokens=int(memory[0][0].shape[-2]),gpu=E["mem"](),utc=utc_now())
        STATE["memory"]=memory;STATE["cartridge"]=bid;STATE["mount"]=times;STATE["ops"].append(dict(times))
        slog("MOUNT",bid,**times);return times

def ask(question,use_memory=True,origin="user"):
    """question answering exactly as a TEST718 readout: run_answer(memory, question) with up to 144 new tokens;
    use_memory=False is the TEST718 vanilla path (same frozen model, no PDF, no cartridge)."""
    with ENGINE_LOCK:
        _require()
        q=(question or "").strip()
        if not q or len(q)>3000:raise OpError("The question must contain 1–3000 characters.")
        if use_memory and STATE["memory"] is None:raise OpError("No cartridge is mounted.")
        E["ensure_room"](512);t=time.perf_counter()
        raw=E["run_answer"](STATE["memory"] if use_memory else None,q)
        row=dict(utc=utc_now(),origin=origin,question=q,raw=raw,cartridge=(STATE["cartridge"] if use_memory else None),with_memory=bool(use_memory),
                 cache_tokens=(int(STATE["memory"][0][0].shape[-2]) if use_memory else 0),answer_tokens=ntok(raw),max_new_tokens=READOUT_MAX_NEW,
                 seconds=round(time.perf_counter()-t,3),gpu=E["mem"](),semantics="NOT VERIFIED")
        (STATE["qa"] if use_memory else STATE["controls"]).append(row)
        with SESSION_QA.open("a",encoding="utf-8") as f:f.write(json.dumps(jsafe(row),ensure_ascii=False)+"\n")
        slog("QA" if use_memory else "QA_VANILLA",row["cartridge"] or "NO MEMORY",question=q[:300],raw=raw,seconds=row["seconds"])
        return row

# ---------------------------------------------------------------------------------------------------------------------
# live verification (read-only)
# ---------------------------------------------------------------------------------------------------------------------
def verify_weights():
    with ENGINE_LOCK:
        _require();t=time.perf_counter();after=E["sentinel"]();before=E["R718"].get("weight_sentinel_before")
        row=dict(utc=utc_now(),passed=(before is not None and after==before),before=before,after=after,seconds=round(time.perf_counter()-t,2))
        STATE["weight_checks"].append(row);slog("WEIGHT_CHECK","PASS" if row["passed"] else "FAIL",**row);return row
def verify_disk():
    """re-hash the ten cartridge files on SSD and compare with the SHA-256 the engine recorded"""
    with ENGINE_LOCK:
        _require();rows=[];t=time.perf_counter()
        for b in E["R"]["books"]:
            p=Path(E["CART"])/(b["id"]+".pt");h=sha_file(p) if p.is_file() else None
            rows.append(dict(cartridge=b["id"],file=str(p),bytes=(p.stat().st_size if p.is_file() else None),sha256=h,engine_record_sha256=b.get("cartridge_sha256"),equals_engine_record=(h is not None and h==b.get("cartridge_sha256"))))
            STATE["files"][b["id"]]=rows[-1]
        row=dict(utc=utc_now(),files=rows,passed=(len(rows)==N_CART and all(r["equals_engine_record"] for r in rows)),seconds=round(time.perf_counter()-t,2))
        STATE["disk_checks"].append(row);slog("DISK_CHECK","PASS" if row["passed"] else "FAIL",passed=row["passed"],seconds=row["seconds"]);return row

# ---------------------------------------------------------------------------------------------------------------------
# READ-ONLY X-ray of the live GPU K/V tensors — every cartridge mounted ALONE (as in TEST718), measured, released
# ---------------------------------------------------------------------------------------------------------------------
XRAY_FILE=SESSION_DIR/"XRAY_TEN_CARTRIDGES.json"
def xray_measure(bin_tokens=256,chunk=4096):
    """per layer and per token bin: mean over KV heads of the L2 norm of each K and V row of the mounted memory.
    FP32 copies of small chunks; nothing is written to the tensors; no reference is kept after returning."""
    with ENGINE_LOCK:
        _require()
        if STATE["memory"] is None:raise OpError("No cartridge is mounted.")
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
        return dict(cartridge=STATE["cartridge"],utc=utc_now(),tokens=T,layers=NL,kv_heads=E["KVH"],bin_tokens=bin_tokens,cut=E["CUT"],prefix_tokens=E["P"],
                    k_norm=Kb.round(5).tolist(),v_norm=Vb.round(5).tolist(),finite=bool(np.isfinite(Kb).all() and np.isfinite(Vb).all()),
                    k_mean=float(np.nanmean(Kb)),v_mean=float(np.nanmean(Vb)),seconds=round(time.perf_counter()-t,2),gpu=E["mem"](),
                    method=f"mean over {E['KVH']} KV heads of the L2 norm per K/V row; mean per bin of {bin_tokens} tokens; FP32 copies of {chunk}-row chunks; read-only")
def xray_all():
    """C01…C10 one after another: mount ALONE → measure → release. The ten memories never coexist on the GPU."""
    for bid in cart_ids():
        t=mount(bid);x=xray_measure();x["mount"]={k:t.get(k) for k in ("ssd_load_ms","h2d_ms","rebuild_ms","end_to_end_ms","cache_tokens","utc")}
        _release(f"X-ray of {bid} done");x["released_utc"]=utc_now();STATE["xrays"][bid]=x
        _OUT.write(f"  X-ray {bid} · {x['tokens']:,} rows × {x['layers']} layers · mount {t['end_to_end_ms']/1000:.1f} s · measure {x['seconds']:.1f} s · released {x['released_utc'][11:19]} UTC\n");_OUT.flush()
        slog("XRAY",bid,tokens=x["tokens"],finite=x["finite"],seconds=x["seconds"],mounted_utc=t["utc"],released_utc=x["released_utc"])
    dump_json(XRAY_FILE,dict(session=SESSION_ID,note="each cartridge was mounted alone, measured read-only and released before the next one",xrays=STATE["xrays"]))
    return dict(cartridges=len(STATE["xrays"]),first_utc=STATE["xrays"][cart_ids()[0]]["utc"],last_utc=STATE["xrays"][cart_ids()[-1]]["utc"])

# ---------------------------------------------------------------------------------------------------------------------
# historical reference only (published logs of EARLIER runs) — never shown as results of this session
# ---------------------------------------------------------------------------------------------------------------------
def load_historical():
    out={}
    for n in HISTORICAL:
        r=fetch_locked(n);(HIST_DIR/("HISTORICAL_"+n)).write_bytes(r);out[n]=LOCKS[n]
    (HIST_DIR/"README_HISTORICAL.txt").write_text(
        "These files are PUBLISHED RECORDS OF EARLIER RUNS (TEST716, TEST717, TEST718), verified against their git blob identifiers.\n"
        "They are NOT results of this session. Live results of this session are in ../live_engine/ and in the session files.\n"
        +"".join(f"{n}: git blob {LOCKS[n]}\n" for n in HISTORICAL),encoding="utf-8")
    slog("HISTORICAL_LOADED","published TEST716/717/718 logs verified (reference only, not this session)",blobs=out);return out
def sources_step():
    load_engine_source();h=load_historical()
    fetch_locked("LICENSE");(SESSION_DIR/"LICENSE.txt").write_bytes((EVIDENCE_DIR/"LICENSE").read_bytes())
    return dict(sources={k:v["git_blob"] for k,v in SOURCES.items()},historical=list(h))

# ---------------------------------------------------------------------------------------------------------------------
# LIVE experiment record: everything below is computed from this session's engine record and engine output
# ---------------------------------------------------------------------------------------------------------------------
def _line_times(prefix):
    """seconds since engine start of the engine output lines that start with prefix, keyed by cartridge id"""
    out={}
    for ts,el,line in ENGINE_LINES:
        if line.startswith(prefix):
            m=re.match(re.escape(prefix)+r"(C\d\d)\b",line)
            if m:out[m.group(1)]=(el,ts)
    return out
_W=re.compile(r"[a-z0-9]+(?:[.\-][a-z0-9]+)*")
def _words(t):return _W.findall(str(t or "").lower())
def _grams(w,n=5):return set(tuple(w[i:i+n]) for i in range(len(w)-n+1))
def verbatim_support(answer,source_text,question,n=5):
    """share of the answer's word 5-grams (excluding 5-grams copied from the question) found verbatim in the source
    pages — an automatic lexical measure, NOT a judgement of technical correctness"""
    a=_words(answer);qg=_grams(_words(question),n);ag=[tuple(a[i:i+n]) for i in range(len(a)-n+1)]
    ag=[g for g in ag if g not in qg]
    if not ag:return dict(share=None,ngrams=0,found=0)
    src=_grams(_words(source_text),n);f=sum(1 for g in ag if g in src)
    return dict(share=round(f/len(ag),4),ngrams=len(ag),found=f)
_PG=re.compile(r"PDF\s+pages?\s*(\d{1,3})(?:\s*(?:-|–|to|and)\s*(\d{1,3}))?",re.I)
def page_check(answer,heading_page,cart_range):
    """automatic check of the page the answer STATES against the PDF page where the heading occurs (from the PDF)"""
    m=_PG.search(str(answer or ""))
    if not m:return dict(stated=None,result="not stated",delta=None)
    a=int(m.group(1));b=int(m.group(2)) if m.group(2) else a
    if a==heading_page==b:res="same page"
    elif a<=heading_page<=b:res="range contains heading page"
    else:res="different page"
    d=0 if a<=heading_page<=b else min(abs(a-heading_page),abs(b-heading_page))
    return dict(stated=(a if a==b else f"{a}–{b}"),result=res,delta=d,inside_cartridge=(cart_range[0]<=a<=cart_range[1]))
def section_check(answer,section_number):
    s=str(answer or "");return dict(section=section_number,stated=bool(section_number and re.search(r"(?<![\d.])"+re.escape(section_number)+r"(?![\d])",s)))

def live_record():
    R7=E["R718"];R=E["R"];books=R["books"];P=E.get("P")
    van=_line_times("VANILLA ");phy=_line_times("PHYSICAL ");abl=_line_times("ABLATION ")
    rows=[];prev=(van.get(books[-1]["id"]) or (None,))[0]
    for i,r in enumerate(R7["results"]):
        b=books[i];a,bb=b["page_range"];src="".join(DOC_PAGES[a-1:bb]) if DOC_PAGES else ""
        pw=None
        if r["id"] in phy and prev is not None:pw=round(phy[r["id"]][0]-prev,3)
        if r["id"] in phy:prev=phy[r["id"]][0]
        vw=None
        if i>0 and r["id"] in van and books[i-1]["id"] in van:vw=round(van[r["id"]][0]-van[books[i-1]["id"]][0],3)
        tm=r.get("timing") or {}
        f=STATE["files"].get(r["id"],{})
        row=dict(id=r["id"],index=i,pages=[a,bb],body_tokens=b["body_tokens"],cache_tokens=r.get("cache_tokens"),expected_rows=(P+b["body_tokens"]) if P is not None else None,
                 heading=r["heading"],heading_page=r["pdf_page"],section=r.get("section_number"),question=r["question"],
                 vanilla=r.get("vanilla"),physical=r.get("physical_readout"),ablation=r.get("post_release_no_memory"),
                 vanilla_tokens=ntok(r.get("vanilla")),physical_tokens=ntok(r.get("physical_readout")),
                 ssd_load_ms=tm.get("ssd_load_ms"),h2d_ms=tm.get("h2d_ms"),physical_wall_s=pw,vanilla_wall_s=vw,
                 physical_utc=(phy.get(r["id"]) or (None,None))[1],cartridge_sha256=b.get("cartridge_sha256"),file_bytes=f.get("bytes"),file_sha_ok=f.get("equals_engine_record"),
                 support_physical=verbatim_support(r.get("physical_readout"),src,r["question"]),support_vanilla=verbatim_support(r.get("vanilla"),src,r["question"]),
                 page_physical=page_check(r.get("physical_readout"),r["pdf_page"],(a,bb)),page_vanilla=page_check(r.get("vanilla"),r["pdf_page"],(a,bb)),
                 section_physical=section_check(r.get("physical_readout"),r.get("section_number")),
                 vanilla_unknown=str(r.get("vanilla") or "").strip().upper().startswith("UNKNOWN"),physical_unknown=str(r.get("physical_readout") or "").strip().upper().startswith("UNKNOWN"))
        row["physical_truncated"]=(row["physical_tokens"] or 0)>=READOUT_MAX_NEW
        if r.get("post_release_no_memory") is not None:row["ablation_equals_vanilla"]=(r["post_release_no_memory"]==r.get("vanilla"))
        rows.append(row)
    syn=R7.get("synthesis_output") or ""
    cites={x["id"]:len(re.findall(r"(?<![A-Za-z0-9])"+x["id"]+r"(?![0-9])",syn)) for x in books}
    sw=_grams(_words(syn))
    reuse={}
    for row in rows:
        g=_grams(_words(row["physical"]));reuse[row["id"]]=round(len(g&sw)/len(g),4) if g else None
    m=R7.get("map") or {}
    return dict(status=R7.get("status"),rows=rows,synthesis=dict(mode=R7.get("synthesis_mode"),output=syn,tokens=ntok(syn),input_tokens=ntok(R7.get("synthesis_input")),
                truncated=(ntok(syn) or 0)>=SYNTH_MAX_NEW,citations=cites,reuse=reuse,utc=(next((ts for ts,el,l in ENGINE_LINES if l.startswith("SYNTHESIS ")),None))),
                cosine=dict(metric=m.get("metric"),labels=m.get("cartridges"),matrix=m.get("similarity"),limit=m.get("interpretation_limit")),
                panel=R.get("panel_source"),token_counts=R.get("body_tokens"),page_ranges=R.get("page_ranges"),prefix_tokens=P,
                sentinel_before=R7.get("weight_sentinel_before"),sentinel_after=R7.get("weight_sentinel_after"),
                engine_checks={k:R.get(k) for k in ("709_GIT_BLOB_LOCK","PDF_SHA256_LOCK","PDF_486_PAGES","PANEL_MIN_30","ALL_PAGES_COVERED","CUDA_A100_80GB","MODEL_ARCH","FROZEN")},
                engine_pass_lines=[l for _,_,l in ENGINE_LINES if l.startswith("PASS ")],engine_seconds=ENGINE.get("seconds"),
                engine_started_utc=ENGINE.get("started_utc"),engine_ended_utc=ENGINE.get("ended_utc"))

def model_and_dates_records():
    """model identity (documented public release + Hugging Face facts read now + the snapshot actually loaded) and the
    date comparison with the manual edition — written as separate, citable records"""
    mc=model_cache_report();mi=dict(MODEL_IDENTITY) or model_identity_hub()
    rec=dict(model_id=MODEL_ID,loaded_snapshot_commit=mc.get("cached_snapshot_commit"),hub_main_commit=mi.get("hub_main_commit"),hub_repo_created=mi.get("hub_repo_created"),
             hub_last_modified=mi.get("hub_last_modified"),hub_note=mi.get("hub_note"),documented_public_release=MODEL_RELEASE,
             note="A repository creation time is not a public release date; the documented public release is the Qwen team announcement.",
             architecture=engine_architecture(),software=dict(torch=E["torch"].__version__,transformers=getattr(sys.modules.get("transformers"),"__version__",None),
             bitsandbytes=getattr(sys.modules.get("bitsandbytes"),"__version__",None)))
    MODEL_IDENTITY.update(rec);dump_json(MODEL_FILE,rec)
    rel=date.fromisoformat(MODEL_RELEASE["date"]);d0=(date(2025,7,1)-rel).days;d1=(date(2025,7,31)-rel).days
    dates=dict(model_public_release=MODEL_RELEASE["date"],model_release_source=MODEL_RELEASE["url"],
               document_edition=DOC_EDITION_MARK,document_edition_verified_on_document=DOC.get("edition_verified_on_document"),
               document_edition_pages=DOC.get("edition_mark_pages"),document_pdf_creation=DOC.get("pdf_metadata",{}).get("creationDate"),
               days_from_model_release_to_edition_month=[d0,d1],experiment_date_utc=INIT.get("started_utc"),
               statement=(f"The manual edition {DOC_EDITION_MARK} is {d0}–{d1} days after the documented public release of {MODEL_ID} ({MODEL_RELEASE['date']}); "
                          "the exact day of the edition is not printed."),
               caveat=("The date gap alone is NOT evidence that the model lacks this information: earlier SINUMERIK manuals and other public texts "
                       "may contain the same or similar content, and the vanilla 'UNKNOWN' answers also follow the prompt's instruction not to guess."))
    dump_json(DATES_FILE,dates);return rec,dates

def compute_verification():
    L=live_record();items=[]
    def add(name,ok,detail):items.append(dict(name=name,passed=bool(ok),detail=jsafe(detail)))
    add("ENGINE_STATUS_LIVE",L["status"]==ENGINE_PASS_STATUS,L["status"])
    ec=L["engine_checks"];add("ENGINE_GATES_PASSED",all(v is True for v in ec.values()),ec)
    add("ENGINE_SOURCE_LOCKS",all(any(l.startswith("PASS "+k) for l in L["engine_pass_lines"]) for k in ("TEST716_GIT_BLOB_LOCK","709_GIT_BLOB_LOCK")) and "718.py" in SOURCES,
        "718.py (this program) · 716.py and 709.py (engine PASS lines)")
    add("SOURCE_PDF_SHA256_AND_PAGES",DOC.get("sha256")==PDF_SHA256 and DOC.get("pages")==PDF_PAGES and ec.get("PDF_SHA256_LOCK") and ec.get("PDF_486_PAGES"),f"{DOC.get('pages')} pages · {str(DOC.get('sha256'))[:16]}…")
    d=STATE["disk_checks"][-1] if STATE["disk_checks"] else None;add("TEN_CARTRIDGES_SHA256_ON_SSD",bool(d and d["passed"]),f"{sum(1 for r in (d or {}).get('files',[]) if r['equals_engine_record'])}/{N_CART}")
    rr=L["rows"];okrows=[r for r in rr if r["physical"] is not None and r["cache_tokens"] and r["cache_tokens"]==r["expected_rows"]]
    add("TEN_PHYSICAL_READOUTS",len(okrows)==N_CART,f"{len(okrows)}/{N_CART} cartridges rebuilt to prefix + body rows and answered")
    add("TEN_VANILLA_CONTROLS",sum(1 for r in rr if r["vanilla"] is not None)==N_CART,f"{sum(1 for r in rr if r['vanilla'] is not None)}/{N_CART}")
    ab=[r for r in rr if r.get("ablation") is not None];add("REMOVAL_CONTROL_RECORDED",len(ab)==3,f"{len(ab)} cartridges (C01, C05, C10) asked again after release")
    add("SYNTHESIS_TEXT_MEDIATED",L["synthesis"]["mode"]=="VANILLA_TEXT_ONLY_OVER_PRIOR_PHYSICAL_READOUTS" and bool(L["synthesis"]["output"]),L["synthesis"]["mode"])
    add("WEIGHT_SENTINEL_ENGINE",L["sentinel_before"] is not None and L["sentinel_before"]==L["sentinel_after"],str(L["sentinel_after"])[:24])
    w=STATE["weight_checks"][-1] if STATE["weight_checks"] else None;add("WEIGHT_SENTINEL_AFTER_ALL_STEPS",bool(w and w["passed"]),(w or {}).get("after"))
    add("GPU_SAFETY_RESERVE_NOT_REDUCED",float(E["GPU_RESERVE_GIB"])>=EXPECTED_RESERVE_GIB,f"{E['GPU_RESERVE_GIB']} GiB")
    xs=STATE["xrays"];okx=[bid for bid,x in xs.items() if x["finite"] and x["layers"]==E["NL"] and x["tokens"]==next((r["cache_tokens"] for r in rr if r["id"]==bid),None)]
    add("TEN_XRAYS_FROM_LIVE_KV",len(okx)==N_CART,f"{len(okx)}/{N_CART} cartridges mounted alone, 80-layer K and V measured, released")
    add("COSINE_MAP_FROM_LIVE_H3",bool(L["cosine"]["matrix"]) and len(L["cosine"]["matrix"])==N_CART,L["cosine"]["metric"])
    rec=dict(session=SESSION_ID,utc=utc_now(),ready=all(i["passed"] for i in items),passed=sum(i["passed"] for i in items),total=len(items),items=items,
             semantics="NOT VERIFIED — answers are raw model output; page/section/word checks are automatic and are not expert verification",
             live_engine_status=L["status"],engine_started_utc=L["engine_started_utc"],engine_ended_utc=L["engine_ended_utc"],engine_seconds=L["engine_seconds"])
    STATE["verification"]=rec;dump_json(VERIFY_FILE,rec)
    dump_json(SESSION_DIR/"LIVE_MEASUREMENTS.json",L)
    slog("VERIFICATION","PASS" if rec["ready"] else "FAIL",passed=rec["passed"],total=rec["total"],failed=[i["name"] for i in items if not i["passed"]]);return rec

# ---------------------------------------------------------------------------------------------------------------------
# SEVEN RESEARCH FIGURES (JPEG 300 dpi, PNG lossless, PDF vector) — values ONLY from this live session and the PDF
# ---------------------------------------------------------------------------------------------------------------------
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.linewidth":.9,"axes.edgecolor":"#374151","axes.labelcolor":"#111827",
                     "xtick.color":"#374151","ytick.color":"#374151","xtick.labelsize":10.5,"ytick.labelsize":10.5,"axes.labelsize":12,
                     "axes.titlesize":13,"axes.titleweight":"bold","axes.titlelocation":"left","legend.fontsize":10.5,"legend.frameon":False})
FW,FH=13.333,7.5;OUT_DPI=300
INK,INK2,MUTED,RULE,PANEL="#111827","#374151","#6B7280","#D1D5DB","#F8FAFC"
TEAL,RED,AMBER,GREY="#0F766E","#B91C1C","#B45309","#9CA3AF"
FIGURES=OrderedDict([
    ("F1","Figure 1 — Physical memory mechanism"),("F2","Figure 2 — From the original 2025 Siemens PDF to ten physical cartridges"),
    ("F3","Figure 3 — SSD storage and physical restoration on the GPU"),("F4","Figure 4 — Technical answers: physical memory vs vanilla model"),
    ("F5","Figure 5 — Internal neural memory X-ray of the ten physical cartridges"),("F6","Figure 6 — Evidence map of the text-mediated synthesis"),
    ("F7","Figure 7 — Integrity and verification record")])
FIG_FILES={};LIVE={}
def mt(s):return str(s).replace("$",r"\$")
def wrap(s,n):return "\n".join(textwrap.wrap(str(s),n,break_long_words=True,break_on_hyphens=False)) or ""
def short(s,n):s=" ".join(str(s or "").split());return s if len(s)<=n else s[:n-1].rstrip()+"…"
def lines(s,width,n):
    """first n wrapped lines of a text (marked … when shortened) — display only; full text is in the records"""
    w=textwrap.wrap(" ".join(str(s or "").split()),width,break_long_words=True)
    return "\n".join(w[:n])+("…" if len(w)>n else "")
def plab(pc):
    return {"same page":"page ✓ same as heading","range contains heading page":"page ✓ range incl. heading","not stated":"page not stated"}.get(pc["result"],f"page ✗ differs by {pc['delta']}")
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
    ftext(fig,.035,.022*s,f"{APP_SHORT} · {ORG} · {LICENSE_NAME} · {COPYRIGHT} · 718.py {LOCKS['718.py'][:10]} · live session {SESSION_ID} · Fig. {k}/{len(FIGURES)}",
          minsize=6,fontsize=8.6,color=MUTED,va="center",family="DejaVu Sans Mono")
def box(fig,x,y,w,h,ec,fc="white",lw=1.6,r=.010,z=1):
    fig.add_artist(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={r}",transform=fig.transFigure,facecolor=fc,edgecolor=ec,lw=lw,zorder=z))
def arrow(fig,x0,y0,x1,y1,col=INK2,lw=1.8,ms=16,cs="arc3",ls="-",alpha=1):
    fig.add_artist(FancyArrowPatch((x0,y0),(x1,y1),transform=fig.transFigure,arrowstyle="-|>",mutation_scale=ms,lw=lw,color=col,connectionstyle=cs,zorder=5,linestyle=ls,alpha=alpha))
class LayoutQCError(RuntimeError):pass
def _hide_offview_ticks(fig):
    """tick labels outside an axis' view interval are never drawn by matplotlib; hide them so they are not measured"""
    for ax in fig.axes:
        for axis,(lo,hi) in ((ax.xaxis,sorted(ax.get_xlim())),(ax.yaxis,sorted(ax.get_ylim()))):
            eps=(hi-lo)*1e-6
            for tk in axis.get_major_ticks()+axis.get_minor_ticks():
                loc=tk.get_loc()
                if loc is None or loc<lo-eps or loc>hi+eps:
                    tk.label1.set_visible(False);tk.label2.set_visible(False)
def _texts(fig):
    import matplotlib.text as mtext
    return [t for t in fig.findobj(mtext.Text) if t.get_visible() and str(t.get_text()).strip() and t.get_gid()!="qc-ignore" and t.get_alpha()!=0]
def layout_qc(fig,max_rounds=8,tol=1.5):
    """automatic layout control before the JPEG is written: every visible text must lie inside the page and no two texts
    may overlap. Overlapping texts are shrunk step by step and checked again; a figure that still fails is rejected."""
    r=fig.canvas.get_renderer();W,H=fig.bbox.width,fig.bbox.height;rep=dict(rounds=0,fixed=0)
    for rnd in range(max_rounds+1):
        fig.canvas.draw();_hide_offview_ticks(fig);r=fig.canvas.get_renderer()   # final positions exist only after a draw
        ts=_texts(fig);bbs=[]
        for t in ts:
            b=t.get_window_extent(r);bbs.append((b.x0+tol,b.y0+tol,b.x1-tol,b.y1-tol))
        out=[i for i,b in enumerate(bbs) if b[0]<-1 or b[1]<-1 or b[2]>W+1 or b[3]>H+1]
        ov=[]
        for i in range(len(bbs)):
            a=bbs[i]
            for j in range(i+1,len(bbs)):
                c=bbs[j]
                if a[0]<c[2] and c[0]<a[2] and a[1]<c[3] and c[1]<a[3]:ov.append((i,j))
        rep.update(rounds=rnd,texts=len(ts),outside=[str(ts[i].get_text())[:60] for i in out],overlaps=[(str(ts[i].get_text())[:40],str(ts[j].get_text())[:40]) for i,j in ov][:20])
        if not out and not ov:rep["passed"]=True;return rep
        if rnd==max_rounds:break
        for i in set(out)|{x for p in ov for x in p}:
            t=ts[i]
            if t.get_fontsize()>5.5:t.set_fontsize(t.get_fontsize()-.5);rep["fixed"]+=1
    rep["passed"]=False;raise LayoutQCError(f"layout QC failed: {len(rep['outside'])} text(s) outside the page, {len(rep['overlaps'])} overlap(s): {rep['outside'][:3]} {rep['overlaps'][:3]}")
def jpeg_qc(path,min_w=3900,min_h=2190):
    """the written JPEG itself: opens, has the expected resolution and is not blank"""
    with Image.open(path) as im:
        im.load();w,h=im.size;fmt=im.format;arr=np.asarray(im.convert("L").resize((400,int(400*h/w))),dtype=np.float32)
    ok=(fmt=="JPEG" and w>=min_w and h>=min_h and float(arr.std())>8.0 and float((arr<200).mean())>0.01)
    rep=dict(format=fmt,pixels=[w,h],luma_std=round(float(arr.std()),2),ink_share=round(float((arr<200).mean()),4),passed=bool(ok))
    if not ok:raise LayoutQCError(f"JPEG check failed for {Path(path).name}: {rep}")
    return rep
def save_fig(fig,key,k):
    qc=layout_qc(fig)
    stem=f"FIGURE_{k:02d}_{key}"
    jpg=FIG_DIR/(stem+".jpg");png=FIG_DIR/(stem+".png");pdf=FIG_DIR/(stem+".pdf")
    fig.savefig(pdf,facecolor="white");buf=io.BytesIO();fig.savefig(buf,format="png",dpi=OUT_DPI,facecolor="white");plt.close(fig)
    png.write_bytes(buf.getvalue())
    with Image.open(io.BytesIO(buf.getvalue())) as im:im.convert("RGB").save(jpg,"JPEG",quality=95,optimize=True,subsampling=0,dpi=(OUT_DPI,OUT_DPI))
    jq=jpeg_qc(jpg);size=tuple(jq["pixels"])
    rec=dict(key=key,figure=k,title=FIGURES[f"F{k}"],jpg=str(jpg),png=str(png),pdf=str(pdf),pixels=list(size),jpg_bytes=jpg.stat().st_size,sha256_jpg=sha_file(jpg),utc=utc_now(),
             layout_qc=dict(passed=qc["passed"],texts=qc["texts"],fix_rounds=qc["rounds"],font_reductions=qc["fixed"]),jpeg_qc=jq,
             data="live session "+SESSION_ID+" · values traceable in LIVE_MEASUREMENTS.json / VERIFICATION_RECORD.json / SOURCE_DOCUMENT_RECORD.json")
    flog(f"FIGURE {k} {key} {size[0]}x{size[1]} jpg sha256 {rec['sha256_jpg']}");return rec
def _arch():
    a=engine_architecture()
    if not a:raise OpError("figures need the architecture measured by the engine in this session")
    return a
def pct(x):return "—" if x is None else f"{100*x:.0f} %"
def mib(b):return "—" if b is None else f"{b/2**20:,.0f} MiB"

def fig1(k=1):
    a=_arch();r=LIVE["rows"][0];n=r["cache_tokens"];c=a["cut"];L=a["layers"];kvb=a["full_kv_bytes_per_token"]
    fig=fig_base(k,"Physical memory mechanism — frozen Qwen2.5-72B-Instruct, CUT3",
                 f"{L} layers · hidden {a['hidden']:,} · {a['q_heads']} query / {a['kv_heads']} KV heads · head dim {a['head_dim']} · NF4 weights, BF16 K/V · frozen (measured in this session)",
                 "SCHEMATIC + LIVE VALUES",INK2)
    steps=[("1  FORGE",ccol(0),f"The frozen model reads ONE page range of the Siemens PDF (C01: {n:,} rows incl. prefix) in {a['chunk']}-token chunks."),
           ("2  PERSIST",INK2,f"Only H{c} and the K/V of layers 0–{c} are saved to SSD (.pt file + SHA-256)."),
           ("3  WRITE L0–L3",LOWER_COLOR,"Readout: lower-layer K/V rows come from the cartridge file; nothing is re-read from the PDF."),
           ("4  INJECT + REBUILD",UPPER_COLOR,f"Zero input embeddings; H{c} replaces the layer-{c} output; layers {c+1}–{L-1} recompute the rows."),
           ("5  ANSWER",ccol(0),f"Only the question is fed; greedy decoding, ≤ {READOUT_MAX_NEW} new tokens; then the memory is released.")]
    w=.172;g=(.93-5*w)/4
    for i,(t,col,body) in enumerate(steps):
        x=.035+i*(w+g);box(fig,x,.62,w,.205,col,lw=2)
        fig.add_artist(FancyBboxPatch((x,.785),w,.04,boxstyle="round,pad=0,rounding_size=0.010",transform=fig.transFigure,facecolor=col,edgecolor=col,zorder=2))
        ftext(fig,x+.01,.805,t,xmax=x+w-.006,fontsize=12.5,weight="bold",color="white",va="center",zorder=3)
        ftext(fig,x+.01,.768,wrap(body,27),xmax=x+w-.006,fontsize=10.3,color=INK,va="top",linespacing=1.3)
        if i<4:arrow(fig,x+w+.002,.72,x+w+g-.002,.72,ms=16)
    x0=.08;W=.86;bw=W/L;y=.44;hh=.07
    for li in range(L):
        fig.add_artist(Rectangle((x0+li*bw+(.004 if li>c else 0),y),bw*.82,hh,transform=fig.transFigure,facecolor=LOWER_COLOR if li<=c else UPPER_COLOR,edgecolor="none",zorder=2))
    for li in (0,c,20,40,60,L-1):fig.text(x0+li*bw+bw*.41+(.004 if li>c else 0),y-.025,f"L{li}",fontsize=10,ha="center",color=INK2)
    xc=x0+(c+1)*bw+.0015;fig.add_artist(Line2D([xc,xc],[y-.012,y+hh+.03],transform=fig.transFigure,color=CUT_COLOR,lw=3,zorder=4))
    fig.text(xc+.006,y+hh+.035,f"◀ CUT{c}: H{c} injected here (layer-{c} output)",fontsize=12,weight="bold",color=CUT_COLOR)
    fig.text(x0,y-.065,f"L0–L{c}: K/V rows written from the cartridge file ({c+1} layers)",fontsize=12,weight="bold",color=LOWER_COLOR)
    fig.text(x0+W,y-.065,f"L{c+1}–L{L-1}: recomputed at every readout ({L-c-1} layers)",fontsize=12,weight="bold",color=UPPER_COLOR,ha="right")
    facts=[("Cartridge file C01 (this session)",f"{r['file_bytes']:,} B" if r["file_bytes"] else "—",f"H{c} [1, {n:,}, {a['hidden']:,}] + K/V of L0–L{c}: 4 × 2 × [1, {a['kv_heads']}, {n:,}, {a['head_dim']}]"),
           ("Full live K/V rebuilt from C01",f"{n*kvb:,} B",f"{L} layers × {kvb:,} B per token = {n*kvb/2**30:.2f} GiB, only while mounted"),
           ("C01 physical readout (live)",f"{r['physical_wall_s']:.1f} s" if r["physical_wall_s"] else "—",f"SSD read + SHA {r['ssd_load_ms']/1000:.2f} s · host→GPU {r['h2d_ms']:.0f} ms · rebuild + {r['physical_tokens']}-token answer"),
           ("Ten cartridges, one at a time",f"{N_CART} × readout",f"each mounted alone, answered, then released — never jointly in GPU memory")]
    fw=(.93-3*.01)/4
    for i,(h1,v,sub) in enumerate(facts):
        x=.035+i*(fw+.01);box(fig,x,.11,fw,.2,RULE,fc=PANEL,lw=1)
        ftext(fig,x+.012,.285,h1,xmax=x+fw-.008,fontsize=11,weight="bold",color=INK2,va="top")
        ftext(fig,x+.012,.225,v,xmax=x+fw-.008,fontsize=17,weight="bold",color=INK,va="center")
        ftext(fig,x+.012,.175,wrap(sub,38),xmax=x+fw-.008,fontsize=10,color=INK2,va="top")
    fig_footer(fig,k,"Schematic illustration of the TEST709 CUT3 path as used by TEST718 (layer strip not to scale). Numbers were measured in this live session.")
    return save_fig(fig,"PHYSICAL_MEMORY_MECHANISM",k)

def fig2(k=2):
    rows=LIVE["rows"];mi=MODEL_IDENTITY;dt=json.loads(DATES_FILE.read_text()) if DATES_FILE.is_file() else {}
    fig=fig_base(k,"From the original 2025 Siemens PDF to ten physical cartridges",
                 f"{DOC_TITLE} · edition {DOC_EDITION_MARK} · downloaded from Siemens in this session · {DOC.get('pages')} PDF pages → C01–C10","LIVE SOURCE RECORD",TEAL)
    # source document card
    box(fig,.035,.585,.455,.255,TEAL,lw=1.8)
    fig.text(.047,.815,"Original source document (measured now)",fontsize=12.5,weight="bold",color=TEAL,va="center")
    dl=[("title",f"{DOC_TITLE} · software {DOC.get('software_version')} · order no. {DOC.get('order_number')}"),
        ("edition",f"“{DOC_EDITION_MARK}” printed on {DOC.get('edition_mark_pages')} of {DOC.get('pages')} pages — verified on the document"),
        ("download",f"{str(DOC.get('download_end_utc'))[:19].replace('T',' ')} UTC · {DOC.get('bytes',0):,} B · official Siemens address"),
        ("SHA-256",str(DOC.get("sha256"))),("metadata",f"PDF created {DOC.get('pdf_metadata',{}).get('creationDate')} · modified {DOC.get('pdf_metadata',{}).get('modDate')}")]
    for i,(kk,vv) in enumerate(dl):
        fig.text(.047,.775-i*.04,kk,fontsize=9.6,weight="bold",color=INK2,va="center")
        ftext(fig,.135,.775-i*.04,vv,xmax=.482,minsize=7,fontsize=9.6,color=INK,va="center",family="DejaVu Sans Mono" if kk=="SHA-256" else "DejaVu Sans")
    # model card
    box(fig,.51,.585,.455,.255,INK2,lw=1.4,fc=PANEL)
    fig.text(.522,.815,"Model (frozen, weights never changed)",fontsize=12.5,weight="bold",color=INK,va="center")
    ml=[("model",MODEL_ID),("public release",f"{MODEL_RELEASE['date']} — Qwen Team blog “Qwen2.5: A Party of Foundation Models!”"),
        ("loaded snapshot",str(mi.get("loaded_snapshot_commit") or "not determinable at run time")),
        ("Hugging Face",f"repo created {str(mi.get('hub_repo_created'))[:10]} · last modified {str(mi.get('hub_last_modified'))[:10]} (read now)" if mi.get("hub_repo_created") else str(mi.get("hub_note"))),
        ("weights","NF4 4-bit (bitsandbytes), BF16 compute · TEST709 weight sentinel unchanged")]
    for i,(kk,vv) in enumerate(ml):
        fig.text(.522,.775-i*.04,kk,fontsize=9.6,weight="bold",color=INK2,va="center")
        ftext(fig,.618,.775-i*.04,vv,xmax=.957,minsize=7,fontsize=9.6,color=INK,va="center",family="DejaVu Sans Mono" if kk=="loaded snapshot" else "DejaVu Sans")
    # timeline
    t0=date(2024,7,1);t1=max(date.fromisoformat(INIT["started_utc"][:10]),date(2025,10,1))
    def X(d):return .08+.84*(d-t0).days/max(1,(t1-t0).days)
    yl=.505;fig.add_artist(Line2D([.08,.92],[yl,yl],transform=fig.transFigure,color=INK2,lw=1.4))
    for yr in range(t0.year,t1.year+1):
        for mo in (1,7):
            d=date(yr,mo,1)
            if t0<=d<=t1:fig.add_artist(Line2D([X(d),X(d)],[yl-.006,yl+.006],transform=fig.transFigure,color=INK2,lw=1));fig.text(X(d),yl-.025,f"{yr}-{mo:02d}",fontsize=8.6,ha="center",color=MUTED)
    rel=date.fromisoformat(MODEL_RELEASE["date"]);ed0=date(2025,7,1);ed1=date(2025,7,31);ex=date.fromisoformat(INIT["started_utc"][:10])
    fig.add_artist(Rectangle((X(ed0),yl-.012),X(ed1)-X(ed0),.024,transform=fig.transFigure,facecolor=TEAL,edgecolor="none"))
    for d,lab,col,dy in ((rel,f"model public release\n{MODEL_RELEASE['date']}",INK,.02),(ed0,f"manual edition {DOC_EDITION_MARK}\n(month printed; day not printed)",TEAL,.02),(ex,f"this experiment\n{ex.isoformat()}",UPPER_COLOR,.02)):
        fig.add_artist(Line2D([X(d)],[yl],transform=fig.transFigure,marker="o",ms=8,color=col));fig.text(X(d),yl+dy,lab,fontsize=9.4,ha="center",va="bottom",color=col,weight="bold")
    ftext(fig,.08,.462,wrap(f"{dt.get('statement','')} {dt.get('caveat','')}",215),xmax=.955,minsize=7,fontsize=8.4,color=AMBER,va="top",linespacing=1.2)
    # page strip → cartridges
    y0=.2;hh=.07;x0=.06;W=.9;N=DOC.get("pages") or PDF_PAGES
    fig.text(x0,.372,f"PDF pages 1–{N} → ten physical cartridges (page ranges fixed by TEST716; token counts measured in this session)",fontsize=11.5,weight="bold",color=INK)
    mx=max(r["body_tokens"] for r in rows)
    for r in rows:
        a_,b_=r["pages"];xa=x0+W*(a_-1)/N;wa=W*(b_-a_+1)/N;col=ccol(r["index"])
        fig.add_artist(Rectangle((xa,y0),wa-.002,hh,transform=fig.transFigure,facecolor=col,edgecolor="none"))
        fig.text(xa+wa/2,y0+hh/2+.012,r["id"],fontsize=11,weight="bold",color="white",ha="center",va="center")
        ftext(fig,xa+wa/2,y0+hh/2-.018,f"p. {a_}–{b_}",xmax=xa+wa-.002,xmin=xa+.001,minsize=6,fontsize=8.4,color="white",ha="center",va="center")
        bh=.05*r["body_tokens"]/mx;fig.add_artist(Rectangle((xa+wa*.2,y0+hh+.006),wa*.6,bh,transform=fig.transFigure,facecolor=col,alpha=.35,edgecolor="none"))
        fig.text(xa+wa/2,y0+hh+.008+bh,f"{r['body_tokens']:,}",fontsize=8.4,color=INK2,ha="center",va="bottom")
        fig.text(xa+wa/2,y0-.022,f"{r['heading_page']}",fontsize=8,color=MUTED,ha="center")
    fig.text(x0,y0-.045,"bars above: body tokens per cartridge · numbers below: PDF page of the heading used for the cartridge's TEST718 question",fontsize=8.8,color=MUTED)
    fig_footer(fig,k,"Source: official Siemens address (see SOURCE_DOCUMENT_RECORD.json; © Siemens AG, not redistributed) · MODEL_IDENTITY_RECORD.json · DATE_COMPARISON_RECORD.json.")
    return save_fig(fig,"SIEMENS_PDF_TO_TEN_CARTRIDGES",k)

def fig3(k=3):
    rows=LIVE["rows"]
    fig=fig_base(k,"SSD storage and physical restoration on the GPU",
                 "Ten cartridge files on SSD · each readout loads ONE file, checks its SHA-256, rebuilds the 80-layer memory, answers and releases it","LIVE SESSION MEASUREMENT",TEAL)
    fig.text(.035,.815,"SSD — ten cartridge files (this session)",fontsize=13,weight="bold",color=INK)
    for r in rows:
        y=.775-r["index"]*.052;col=ccol(r["index"])
        fig.add_artist(Rectangle((.035,y-.016),.008,.032,transform=fig.transFigure,facecolor=col,edgecolor="none"))
        fig.text(.05,y,r["id"],fontsize=10.5,weight="bold",color=col,va="center")
        ftext(fig,.085,y+.008,f"{mib(r['file_bytes'])} · {r['body_tokens']:,} tokens",xmax=.33,fontsize=9.4,color=INK,va="center")
        ftext(fig,.085,y-.011,f"SHA-256 {str(r['cartridge_sha256'])[:20]}… {'✓ re-verified' if r['file_sha_ok'] else '✗'}",xmax=.33,fontsize=8.2,color=TEAL if r["file_sha_ok"] else RED,va="center",family="DejaVu Sans Mono")
    arrow(fig,.335,.53,.39,.53,lw=2.2,ms=20);fig.text(.3625,.555,"one at\na time",fontsize=9.5,ha="center",color=INK,weight="bold")
    ax=fig.add_axes([.47,.33,.48,.43]);ys=np.arange(len(rows))[::-1]
    ssd=np.array([(r["ssd_load_ms"] or 0)/1000 for r in rows]);h2d=np.array([(r["h2d_ms"] or 0)/1000 for r in rows])
    wall=np.array([r["physical_wall_s"] if r["physical_wall_s"] is not None else np.nan for r in rows]);rest=np.clip(wall-ssd-h2d,0,None)
    ax.barh(ys,ssd,color="#94A3B8",label="SSD read + SHA-256");ax.barh(ys,h2d,left=ssd,color="#475569",label="host → GPU")
    ax.barh(ys,rest,left=ssd+h2d,color=[ccol(r["index"]) for r in rows],alpha=.85,label="rebuild L4–L79 + answer (colour = cartridge)")
    for yy,r,wv in zip(ys,rows,wall):
        if not np.isnan(wv):ax.text(wv*1.01,yy,f"{wv:.0f} s · {r['cache_tokens']:,} rows · {r['physical_tokens']} tok",va="center",fontsize=8.8,color=INK2)
    ax.set_yticks(ys);ax.set_yticklabels([r["id"] for r in rows]);ax.set_xlabel("seconds (wall time between engine output lines, UTC-stamped)",fontsize=10)
    ax.set_xlim(0,np.nanmax(wall)*1.45 if np.isfinite(np.nanmax(wall)) else 1);ax.legend(loc="lower left",bbox_to_anchor=(0,1.0),ncol=3,fontsize=8.6,handlelength=1.2,columnspacing=1.0)
    ax.grid(axis="x",color="#E5E7EB",lw=.6);ax.set_axisbelow(True);fig.text(.47,.815,"Physical readout per cartridge (live TEST718)",fontsize=13,weight="bold",color=INK)
    for sp in ("top","right"):ax.spines[sp].set_visible(False)
    box(fig,.035,.088,.93,.16,"#0F766E",fc="#F0FDFA",lw=1.2)
    fig.text(.045,.23,PREV_TITLE,fontsize=10.5,weight="bold",color=TEAL,va="center")
    ftext(fig,.045,.208,wrap(PREV_TEXT,180),xmax=.958,minsize=7.5,fontsize=9,color=INK,va="top",linespacing=1.25)
    ftext(fig,.045,.153,wrap(PREV_SEE,180),xmax=.958,minsize=7,fontsize=9,color=INK2,va="top",weight="bold",linespacing=1.25)
    fig_footer(fig,k,"Previously published research (box) is not a result of this experiment. Timings: LIVE_MEASUREMENTS.json · engine output with UTC time stamps.")
    return save_fig(fig,"SSD_STORAGE_GPU_RESTORATION",k)

def fig4(k=4):
    rows=LIVE["rows"]
    fig=fig_base(k,"Technical answers: physical memory vs vanilla model",
                 f"Same frozen model, same question, greedy decoding, ≤ {READOUT_MAX_NEW} new tokens · vanilla = no PDF, no cartridge · answers are raw and NOT verified","LIVE · NOT VERIFIED",AMBER)
    XM,XH,XV,XP,XC=.035,.075,.29,.47,.86;y=.825
    for xx,t in ((XM,""),(XH,"section heading in the PDF (page)"),(XV,"vanilla answer"),(XP,"answer with the physical cartridge"),(XC,"automatic checks")):fig.text(xx,y,t,fontsize=9.8,weight="bold",color=MUTED)
    rh=.054
    for r in rows:
        yy=y-.03-r["index"]*rh;col=ccol(r["index"])
        fig.text(XM,yy,r["id"],fontsize=10,weight="bold",color=col,va="top")
        ftext(fig,XH,yy,f"{r['heading']} (p. {r['heading_page']})",xmax=XV-.008,minsize=7.4,trunc=True,fontsize=9,color=INK,va="top")
        ftext(fig,XV,yy,short(r["vanilla"],60),xmax=XP-.008,minsize=7.2,trunc=True,fontsize=8.4,color=MUTED,va="top",family="DejaVu Sans Mono")
        ftext(fig,XP,yy,lines(r["physical"],88,2),xmax=XC-.008,minsize=6.8,fontsize=8,color=INK,va="top",family="DejaVu Sans Mono",linespacing=1.15)
        pc=r["page_physical"];sp=r["support_physical"]["share"];sv=r["support_vanilla"]["share"]
        ftext(fig,XC,yy,plab(pc),xmax=.965,minsize=7,fontsize=8.4,color=TEAL if pc["result"] in ("same page","range contains heading page") else (MUTED if pc["result"]=="not stated" else RED),va="top")
        ftext(fig,XC,yy-.018,f"5-gram support {pct(sp)} vs {pct(sv)}",xmax=.965,minsize=7,fontsize=8.2,color=INK2,va="top")
    # removal control (small)
    ab=[r for r in rows if r.get("ablation") is not None]
    box(fig,.035,.09,.93,.135,AMBER,fc="#FFFBEB",lw=1.2)
    fig.text(.045,.207,"Removal control — the same question asked again AFTER the cartridge was released (TEST718 ablation)",fontsize=10.2,weight="bold",color=AMBER,va="center")
    for i,r in enumerate(ab):
        x=.045+i*.31
        fig.text(x,.18,r["id"],fontsize=9.6,weight="bold",color=ccol(r["index"]),va="center")
        ftext(fig,x+.035,.18,"with: "+short(r["physical"],40),xmax=x+.3,minsize=7,trunc=True,fontsize=8.2,color=INK,va="center",family="DejaVu Sans Mono")
        ftext(fig,x+.035,.152,"after release: "+short(r["ablation"],34),xmax=x+.3,minsize=7,trunc=True,fontsize=8.2,color=INK2,va="center",family="DejaVu Sans Mono")
        ftext(fig,x+.035,.124,f"identical to the vanilla answer: {'yes' if r.get('ablation_equals_vanilla') else 'no'}",xmax=x+.3,fontsize=8.4,color=TEAL if r.get("ablation_equals_vanilla") else RED,va="center",weight="bold")
    ftext(fig,.045,.102,"Checks are automatic: stated PDF page vs the page where the heading occurs; share of the answer's word 5-grams (not copied from the question) found verbatim in the cartridge's PDF pages (physical vs vanilla). Not an expert evaluation.",
          xmax=.958,minsize=6.8,fontsize=8,color=INK2,va="center")
    fig_footer(fig,k,"Full raw answers: live engine output, LIVE_TEST718_RESULTS_this_session.json and RUN_SUMMARY.txt (… = shortened for display only).")
    return save_fig(fig,"ANSWERS_PHYSICAL_VS_VANILLA",k)

def fig5(k=5):
    xs=STATE.get("xrays") or {};ids=cart_ids()
    if len(xs)!=len(ids):raise OpError("Figure 5 needs the read-only X-ray of all ten cartridges from this session (no synthetic heat map is drawn).")
    rows={r["id"]:r for r in LIVE["rows"]};t0=min(x["utc"] for x in xs.values());t1=max(x["released_utc"] for x in xs.values())
    fig=fig_base(k,"Internal neural memory X-ray — ten physical cartridges, 80 layers each",
                 f"Live GPU K/V tensors · each cartridge mounted ALONE, measured read-only, released · {t0[:19].replace('T',' ')} → {t1[11:19]} UTC · bin {xs[ids[0]]['bin_tokens']} tokens",
                 "LIVE GPU MEASUREMENT",TEAL)
    def z(m):
        m=np.asarray(m,dtype=float);mu=np.nanmean(m,axis=1,keepdims=True);sd=np.nanstd(m,axis=1,keepdims=True);return (m-mu)/np.where(sd>0,sd,1)
    X0,X1,Y0,Y1=.075,.905,.14,.832;nc=5;gx=.012;gy=.048;pw=(X1-X0-(nc-1)*gx)/nc;ph=(Y1-Y0-3*gy)/4
    order=[("K",ids[:5]),("V",ids[:5]),("K",ids[5:]),("V",ids[5:])];im=None
    for ri,(kv,grp) in enumerate(order):
        y=Y1-(ri+1)*ph-ri*gy
        fig.text(.035,y+ph/2,f"‖{kv}‖",fontsize=13,weight="bold",color=INK if kv=="K" else UPPER_COLOR,va="center",ha="left",rotation=90)
        for ci,bid in enumerate(grp):
            x=xs[bid];r=rows.get(bid,{});col=ccol(cart_index(bid));px=X0+ci*(pw+gx)
            ax=fig.add_axes([px,y,pw,ph]);M=z(x["k_norm" if kv=="K" else "v_norm"]);nb=M.shape[1]
            im=ax.imshow(M,aspect="auto",origin="lower",cmap="RdBu_r",vmin=-2.5,vmax=2.5,interpolation="nearest")
            ax.axhline(x["cut"]+.5,color=CUT_COLOR,lw=1.2,ls="--")
            ax.set_yticks([0,40,x["layers"]-1]);ax.set_yticklabels(["0","40",str(x["layers"]-1)] if ci==0 else [],fontsize=7.6)
            ax.set_xticks([0,nb-1]);ax.set_xticklabels(["0",f"{x['tokens']:,}"],fontsize=7.2)
            ax.tick_params(length=2,pad=1.5)
            for sp in ax.spines.values():sp.set_edgecolor(col);sp.set_linewidth(1.6)
            pg=r.get("pages") or ["?","?"]
            ftext(fig,px,y+ph+.006,f"{bid} · {kv}",xmax=px+pw*.42,fontsize=9.6,weight="bold",color=col,va="bottom")
            ftext(fig,px+pw,y+ph+.006,f"p. {pg[0]}–{pg[1]} · {x['tokens']:,} rows",xmin=px+pw*.44,xmax=px+pw,minsize=5.8,fontsize=7.4,color=INK2,va="bottom",ha="right")
    cax=fig.add_axes([.918,Y0,.01,Y1-Y0]);cb=fig.colorbar(im,cax=cax);cb.set_label("z (per layer, per panel)",fontsize=9);cb.ax.tick_params(labelsize=8)
    fig.text(.075,.1,"y axis: layer 0–79 (dashed line = CUT3: below L0–L3 from the cartridge file, above L4–L79 recomputed) · x axis: memory row (token position) · K and V are shown in separate rows",
             fontsize=8.6,color=INK2,va="center")
    fig_footer(fig,k,"Read-only measurement of this session's GPU tensors, one cartridge at a time (XRAY_TEN_CARTRIDGES.json: method, UTC times, absolute values). Never jointly in GPU memory.")
    return save_fig(fig,"TEN_CARTRIDGE_KV_XRAY",k)

def fig6(k=6):
    rows=LIVE["rows"];S=LIVE["synthesis"]
    if not S.get("output"):raise OpError("figure 6 needs the live synthesis output")
    fig=fig_base(k,"Evidence map of the text-mediated synthesis",
                 "Cartridge → physical readout (text) → synthesis by the frozen model with NO cartridge attached · lines = recorded citations, not neural measurement","LIVE · TEXT-MEDIATED",AMBER)
    xc,xr,xs=.035,.2,.72;top=.79;rh=.058
    fig.text(xc,top+.03,"cartridge",fontsize=10,weight="bold",color=MUTED);fig.text(xr,top+.03,"physical readout (generated text, tokens)",fontsize=10,weight="bold",color=MUTED)
    fig.text(xs,top+.03,"synthesis output",fontsize=10,weight="bold",color=MUTED)
    mxc=max([v for v in S["citations"].values()]+[1])
    sy0,sy1=.18,top+.005
    for r in rows:
        y=top-r["index"]*rh-.02;col=ccol(r["index"])
        box(fig,xc,y-.018,.12,.036,col,lw=1.4)
        ftext(fig,xc+.006,y,f"{r['id']} · p. {r['pages'][0]}–{r['pages'][1]}",xmax=xc+.118,fontsize=8.8,weight="bold",color=col,va="center")
        arrow(fig,xc+.122,y,xr-.004,y,col=col,lw=1.2,ms=10)
        box(fig,xr,y-.022,.4,.044,RULE,fc=PANEL,lw=1)
        ftext(fig,xr+.006,y,lines(f"{r['physical_tokens']} tok · "+str(r["physical"]),92,2),xmax=xr+.396,minsize=6.4,fontsize=7.4,color=INK,va="center",family="DejaVu Sans Mono",linespacing=1.1)
        nc=S["citations"].get(r["id"],0);ty=sy1-(sy1-sy0)*(r["index"]+.5)/len(rows)
        if nc>0:arrow(fig,xr+.402,y,xs-.004,ty,col=col,lw=.8+3.2*nc/mxc,ms=10,alpha=.85)
        else:arrow(fig,xr+.402,y,xs-.004,ty,col=GREY,lw=.8,ms=8,ls=(0,(3,3)),alpha=.7)
        ftext(fig,xr+.41,y+.012,f"cited ×{nc} · reuse {pct(S['reuse'].get(r['id']))}",xmax=xs-.012,fontsize=8,color=col if nc else MUTED,va="center")
    box(fig,xs,sy0,.245,sy1-sy0,AMBER,fc="#FFFBEB",lw=1.6)
    fig.text(xs+.01,sy1-.025,"Synthesis (TEST718)",fontsize=11.5,weight="bold",color=AMBER,va="center")
    info=[f"{S.get('tokens')} tokens{' — limit reached' if S.get('truncated') else ''} (≤ {SYNTH_MAX_NEW})",f"input: {S.get('input_tokens')} tokens of text",
          f"mode: {S.get('mode')}",f"cartridges cited: {sum(1 for v in S['citations'].values() if v)}/{len(rows)}"]
    for i,t in enumerate(info):ftext(fig,xs+.01,sy1-.055-i*.025,t,xmax=xs+.24,minsize=6.4,fontsize=8.6,color=INK,va="center")
    ftext(fig,xs+.01,sy1-.165,wrap(short(S["output"],560),48),xmax=xs+.24,minsize=6,fontsize=7.4,color=INK2,va="top",family="DejaVu Sans Mono",linespacing=1.15)
    ftext(fig,.035,.135,wrap("How the synthesis was produced (TEST718): the ten cartridges were read one at a time; each readout produced text; the ten texts were concatenated "
                             "with their cartridge IDs and given to the same frozen model with NO cartridge in memory. Line width = how often the synthesis text cites the "
                             "cartridge ID; reuse = share of the readout's word 5-grams that reappear verbatim in the synthesis. Both are text records, not measurements of neural synthesis.",175),
          xmax=.958,minsize=7,fontsize=8.8,color=INK,va="top")
    fig_footer(fig,k,"Full synthesis input and output: LIVE_TEST718_RESULTS_this_session.json (synthesis_input / synthesis_output) and the live engine output.")
    return save_fig(fig,"SYNTHESIS_EVIDENCE_MAP",k)

def fig7(k=7):
    v=STATE.get("verification")
    if not v:raise OpError("figure 7 needs the live verification record")
    fig=fig_base(k,"Integrity and verification record — this live session",f"Locked sources · original document · ten cartridges · frozen weights · live verification ({v['passed']}/{v['total']} passed)",
                 "LIVE VERIFICATION",TEAL if v["ready"] else RED)
    fig.text(.035,.8,"Live verification",fontsize=13.5,weight="bold",color=INK);y=.765
    for it in v["items"]:
        ok=it["passed"];fig.text(.035,y,"PASS" if ok else "FAIL",fontsize=9.4,weight="bold",color=TEAL if ok else RED,va="top",family="DejaVu Sans Mono")
        ftext(fig,.072,y,it["name"],xmax=.33,fontsize=8.8,color=INK,va="top",family="DejaVu Sans Mono")
        ftext(fig,.072,y-.017,short(it["detail"] if isinstance(it["detail"],str) else json.dumps(it["detail"],ensure_ascii=False),80),xmax=.33,minsize=6.4,trunc=True,fontsize=7.4,color=MUTED,va="top")
        y-=.0395
    fig.text(.36,.8,"Locked identities",fontsize=13.5,weight="bold",color=INK);y=.765
    ids=[("718.py",LOCKS["718.py"]),("716.py",LOCKS["716.py"]),("709.py",LOCKS["709.py"]),("Siemens PDF SHA-256",str(DOC.get("sha256"))),
         ("model",f"{MODEL_ID} @ {str(MODEL_IDENTITY.get('loaded_snapshot_commit') or 'snapshot n/a')[:16]}"),
         ("weight sentinel",str(LIVE.get("sentinel_after"))[:40]+"…"),("engine run",f"{str(LIVE.get('engine_started_utc'))[:19]} → {str(LIVE.get('engine_ended_utc'))[:19]} UTC")]
    for kk,vv in ids:
        fig.text(.36,y,kk,fontsize=9.4,weight="bold",color=INK2,va="top");ftext(fig,.36,y-.02,vv,xmax=.67,minsize=6.2,fontsize=8,color=INK,va="top",family="DejaVu Sans Mono");y-=.05
    fig.text(.36,y-.005,"Cartridge SHA-256 (re-verified on SSD)",fontsize=9.4,weight="bold",color=INK2,va="top");y-=.027
    for r in LIVE["rows"]:
        ftext(fig,.36,y,f"{r['id']} {r['cartridge_sha256']}",xmax=.67,minsize=5.8,fontsize=7.2,color=ccol(r["index"]),va="top",family="DejaVu Sans Mono");y-=.0175
    box(fig,.69,.205,.275,.62,RULE,fc="#F3F4F6",lw=1)
    fig.text(.7,.8,"Research lineage (published)",fontsize=11.5,weight="bold",color=INK2,va="center");yy=.77
    for t,u in LINEAGE:
        ftext(fig,.7,yy,t,xmax=.958,minsize=7,fontsize=8.8,weight="bold",color=INK,va="top");ftext(fig,.7,yy-.022,u,xmax=.958,minsize=6.5,fontsize=8,color=INK2,va="top",family="DejaVu Sans Mono");yy-=.06
    ftext(fig,.7,yy-.005,"This experiment: unpublished — no DOI",xmax=.958,fontsize=9,weight="bold",color=RED,va="top");yy-=.04
    fig.text(.7,yy,"Historical reference (not this session)",fontsize=10,weight="bold",color=INK2,va="top");yy-=.025
    for n in HISTORICAL:ftext(fig,.7,yy,f"{n} · blob {LOCKS[n][:12]}…",xmax=.958,minsize=6.5,fontsize=8,color=INK2,va="top",family="DejaVu Sans Mono");yy-=.02
    ftext(fig,.7,yy-.01,wrap("Published logs of earlier runs are kept separately and are never used for the live verification.",44),xmax=.958,minsize=6.5,fontsize=8,color=MUTED,va="top")
    box(fig,.035,.09,.93,.1,RULE,fc=PANEL,lw=1)
    ftext(fig,.045,.175,f"Answers are raw model output and NOT verified technical truth · engine status {LIVE.get('status')}",xmax=.958,minsize=7,fontsize=9,color=INK,va="top")
    ftext(fig,.045,.148,f"Source document {DOC_TITLE}, edition {DOC_EDITION_MARK}, {DOC.get('pages')} pages, downloaded {str(DOC.get('download_end_utc'))[:19]} UTC from the official Siemens address.",xmax=.958,minsize=7,fontsize=9,color=INK,va="top")
    ftext(fig,.045,.121,f"Model public release {MODEL_RELEASE['date']} ({MODEL_RELEASE['url']}) · {LIVE['rows'][0]['id']}–{LIVE['rows'][-1]['id']} forged with the unchanged TEST709 CUT3 engine · "
                        f"GPU reserve {E.get('GPU_RESERVE_GIB')} GiB unchanged.",xmax=.958,minsize=7,fontsize=9,color=INK2,va="top")
    fig_footer(fig,k,f"Live records: VERIFICATION_RECORD.json · LIVE_MEASUREMENTS.json · live engine output (UTC-stamped) · SHA256_MANIFEST.json (session {SESSION_ID}).")
    return save_fig(fig,"INTEGRITY_VERIFICATION_RECORD",k)

FIG_FUNCS=OrderedDict([("F1",fig1),("F2",fig2),("F3",fig3),("F4",fig4),("F5",fig5),("F6",fig6),("F7",fig7)])
def render_figures():
    """renders all figures on the CPU from this session's live data (no GPU use)"""
    global LIVE
    LIVE=live_record();out={};errs={}
    for i,(key,fn) in enumerate(FIG_FUNCS.items(),1):
        t=time.perf_counter()
        try:rec=fn(i);out[key]=rec;FIG_FILES[key]=rec;_OUT.write(f"  figure {i}/{len(FIG_FUNCS)} · {rec['pixels'][0]}×{rec['pixels'][1]} JPEG · {rec['jpg_bytes']/1e6:.1f} MB · {time.perf_counter()-t:.1f} s · {Path(rec['jpg']).name}\n")
        except Exception as ex:errs[key]=f"{type(ex).__name__}: {ex}";FIG_FILES.pop(key,None);flog(f"FIGURE {i} NOT GENERATED {traceback.format_exc()[-1500:]}");_OUT.write(f"  figure {i} NOT GENERATED · {errs[key]}\n")
        _OUT.flush()
    dump_json(SESSION_DIR/"FIGURES_MANIFEST.json",dict(session=SESSION_ID,utc=utc_now(),data_source="live session only",figures=FIG_FILES,not_generated=errs))
    slog("FIGURES",f"{len(out)} rendered",not_generated=errs);return out,errs

# ---------------------------------------------------------------------------------------------------------------------
# research summary, downloadable artifacts (actual files of this session; the Siemens PDF itself is never packaged)
# ---------------------------------------------------------------------------------------------------------------------
RUN_SUMMARY=SESSION_DIR/"RUN_SUMMARY.txt"
ZIP_PATH=SESSION_DIR/f"{SESSION_ID}_AKBASCORE_SIEMENS_ALL_RESEARCH_ARTIFACTS.zip";MANIFEST=SESSION_DIR/"SHA256_MANIFEST.json"
def write_run_summary():
    R7=E.get("R718",{});v=STATE.get("verification") or {};L=[];a=L.append;Lr=LIVE if LIVE else {}
    a(f"{APP_TITLE}\n{VERSION_NOTE}\nsession {SESSION_ID} · started {SESSION_INFO['started_local']} ({INIT['started_utc']} UTC) · written {local_now()}\n")
    a("EXPERIMENT  TEST718 — ten physical CUT3 cartridges of a real industrial manual, vanilla controls, removal control, text-mediated synthesis")
    a(f"ENGINE      718.py git blob {LOCKS['718.py']} (executed unchanged) · 716.py {LOCKS['716.py']} · 709.py {LOCKS['709.py']}")
    a(f"            engine run {ENGINE.get('started_utc')} → {ENGINE.get('ended_utc')} UTC ({ENGINE.get('seconds')} s) · status {R7.get('status')}")
    mi=MODEL_IDENTITY
    a(f"MODEL       {MODEL_ID} · NF4 4-bit, BF16 compute, frozen · loaded snapshot {mi.get('loaded_snapshot_commit')} · Hub main {mi.get('hub_main_commit')}")
    a(f"            first public release {MODEL_RELEASE['date']} — {MODEL_RELEASE['source']} — {MODEL_RELEASE['url']} ({MODEL_RELEASE['checked']})")
    a(f"            Hugging Face repository created {mi.get('hub_repo_created')} · last modified {mi.get('hub_last_modified')} (creation is not publication)")
    a(f"DOCUMENT    {DOC_TITLE} · edition {DOC_EDITION_MARK} (printed on {DOC.get('edition_mark_pages')} of {DOC.get('pages')} pages — verified on the document)")
    a(f"            order no. {DOC.get('order_number')} · software {DOC.get('software_version')} · {DOC.get('bytes')} bytes · SHA-256 {DOC.get('sha256')}")
    a(f"            downloaded {DOC.get('download_start_utc')} → {DOC.get('download_end_utc')} UTC from {PDF_URL}")
    a(f"            PDF metadata: created {DOC.get('pdf_metadata',{}).get('creationDate')} · modified {DOC.get('pdf_metadata',{}).get('modDate')}")
    a(f"            {PDF_POLICY} ({PDF_TERMS_URL})")
    if DATES_FILE.is_file():
        d=json.loads(DATES_FILE.read_text());a(f"DATES       {d['statement']}\n            {d['caveat']}")
    a("\nINITIALIZATION (this session)")
    for st in INIT["steps"]:a(f"  ✓ {st['step']:<13} {st['seconds']:>9.1f} s  {st['title']}")
    if INIT.get("failed"):a(f"  ✗ {INIT['failed']['step']}  {INIT['failed']['error']}  (last successful: {INIT['failed']['last_successful_step']})")
    if Lr.get("rows"):
        a("\nTEN PHYSICAL CARTRIDGES AND ANSWERS (raw, NOT verified; automatic checks only)")
        for r in Lr["rows"]:
            a(f"\n  {r['id']}  PDF pages {r['pages'][0]}–{r['pages'][1]} · {r['body_tokens']} tokens · rows {r['cache_tokens']} · file {r['file_bytes']} B · SHA-256 {r['cartridge_sha256']}")
            a(f"      heading: {r['heading']} (PDF page {r['heading_page']}, section {r['section']})")
            a(f"      readout: SSD+SHA {r['ssd_load_ms']} ms · H2D {r['h2d_ms']} ms · wall {r['physical_wall_s']} s · answer {r['physical_tokens']} tokens{' (limit reached)' if r['physical_truncated'] else ''}")
            a(f"      checks : stated page {r['page_physical']['stated']} → {r['page_physical']['result']} · section number stated {r['section_physical']['stated']} · "
              f"5-gram support physical {pct(r['support_physical']['share'])} vs vanilla {pct(r['support_vanilla']['share'])}")
            a(f"      Q: {r['question']}\n      VANILLA  → {r['vanilla']}\n      PHYSICAL → {r['physical']}")
            if r.get("ablation") is not None:a(f"      AFTER RELEASE → {r['ablation']}  (identical to vanilla: {r.get('ablation_equals_vanilla')})")
        S=Lr["synthesis"]
        a(f"\nSYNTHESIS  mode {S['mode']} · {S['tokens']} tokens{' (limit reached)' if S['truncated'] else ''} · citations {S['citations']}")
        a("  The ten readouts were generated one cartridge at a time; their texts were concatenated and given to the frozen model with NO cartridge attached.")
        a("  "+str(S["output"]).replace("\n","\n  "))
        a(f"\nCOSINE MAP  {Lr['cosine']['metric']} · {Lr['cosine']['limit']}")
        for i,lab in enumerate(Lr["cosine"].get("labels") or []):a(f"  {lab} "+" ".join(f"{v:.3f}" for v in Lr["cosine"]["matrix"][i]))
    if STATE["xrays"]:
        a("\nTEN-CARTRIDGE X-RAY (each cartridge mounted alone, measured read-only, released — never jointly in GPU memory)")
        for bid,x in STATE["xrays"].items():a(f"  {bid} mounted {x['mount']['utc']} · measured {x['utc']} · released {x['released_utc']} UTC · {x['tokens']} rows × {x['layers']} layers · mean ‖K‖ {x['k_mean']:.3f} · mean ‖V‖ {x['v_mean']:.3f}")
    a(f"\nLIVE VERIFICATION  {v.get('passed','—')}/{v.get('total','—')} passed")
    for i in v.get("items",[]):a(f"  {'PASS' if i['passed'] else 'FAIL'}  {i['name']}  {i['detail'] if isinstance(i['detail'],str) else json.dumps(i['detail'],ensure_ascii=False)}")
    if any(r.get("origin")=="user" for r in STATE["qa"]+STATE["controls"]):
        a("\nQUESTIONS ASKED IN THE INTERFACE")
        for r in STATE["qa"]+STATE["controls"]:
            if r.get("origin")=="user":a(f"  [{r['cartridge'] or 'vanilla'}] {r['question']}\n      → {r['raw']}")
    a(f"\n{PREV_TITLE}\n{PREV_TEXT}\n{PREV_SEE}\n(Previously published research — not a result of this experiment.)")
    a("\nRESEARCH LINEAGE\n"+"\n".join(f"  {t}: {u}" for t,u in LINEAGE)+"\n  This experiment: unpublished — no DOI.")
    a("\nHISTORICAL REFERENCE (earlier runs, not this session): "+", ".join(f"{n} blob {LOCKS[n]}" for n in HISTORICAL))
    a("\nSCOPE  Answers are raw model output and not verified technical truth; checks are automatic. Questions contain the section heading (not blind QA). "
      "Cartridges are read one at a time; the synthesis is text-mediated.")
    a(f"{AUTHOR} · {ORG} · {LICENSE_NAME} · {COPYRIGHT}")
    RUN_SUMMARY.write_text("\n".join(L)+"\n",encoding="utf-8");return str(RUN_SUMMARY)
def session_record():
    return dict(session=SESSION_INFO,app=APP_TITLE,version_note=VERSION_NOTE,sources=SOURCES,locks=LOCKS,engine={k:v for k,v in ENGINE.items() if k!="source"},initialization=INIT,
                architecture=engine_architecture(),document=DOC,model=MODEL_IDENTITY,mounted=STATE["mount"],operations=STATE["ops"],qa=STATE["qa"],controls=STATE["controls"],
                weight_checks=STATE["weight_checks"],disk_checks=STATE["disk_checks"],verification=STATE["verification"],figures=FIG_FILES,lineage=LINEAGE,
                previously_demonstrated=dict(title=PREV_TITLE,text=PREV_TEXT,see=PREV_SEE),
                scope="Answers are raw model output; checks are automatic; one cartridge at a time; text-mediated synthesis; the Siemens PDF is not redistributed.")
def _category(rel):
    if rel.startswith("historical_reference_not_this_session"):return "HISTORICAL (published earlier run, not this session)"
    if rel.startswith("figures"):return "LIVE figure"
    if rel.startswith("live_engine"):return "LIVE engine output / record"
    return "LIVE session record"
def package_session():
    """Download-All ZIP: seven figures (JPG/PNG/PDF), live engine output + results, session logs, measurement and
    verification records, historical files (separate folder) and SHA256_MANIFEST.json — never the Siemens PDF"""
    sync_engine_records();dump_json(SESSION_DIR/"SESSION_RECORD.json",session_record());write_run_summary()
    # the Siemens PDF lives outside the session folder (PRIVATE_DIR) and is never packaged; the only PDFs here are figures
    files=sorted(p for p in SESSION_DIR.rglob("*") if p.is_file() and p.suffix not in (".zip",".tmp") and p!=MANIFEST)
    man=OrderedDict((str(p.relative_to(SESSION_DIR)),dict(sha256=sha_file(p),bytes=p.stat().st_size,category=_category(str(p.relative_to(SESSION_DIR))))) for p in files)
    dump_json(MANIFEST,dict(session=SESSION_ID,utc=utc_now(),note="The Siemens PDF is not included (copyright Siemens AG); its URL and SHA-256 are in SOURCE_DOCUMENT_RECORD.json.",files=man))
    tmp=ZIP_PATH.with_suffix(".zip.tmp")
    with zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED) as z:
        for p in files+[MANIFEST]:z.write(p,arcname=f"{SESSION_ID}/{p.relative_to(SESSION_DIR)}")
    with zipfile.ZipFile(tmp) as z:
        if z.testzip():raise RuntimeError("ZIP check failed")
    tmp.replace(ZIP_PATH);slog("PACKAGE",ZIP_PATH.name,files=len(files)+1,bytes=ZIP_PATH.stat().st_size);return str(ZIP_PATH)
def download_items():
    items=[("Run summary (.txt)",RUN_SUMMARY),("Live TEST718 engine output (.log)",LIVE_ENGINE_LOG),("Live engine output with UTC time stamps (.tsv)",LIVE_ENGINE_TS),
           ("Live TEST718 results (.json)",LIVE_ENGINE_JSON),("Live TEST716 set-up record (.json)",LIVE_SETUP_JSON),("Live measurements (.json)",SESSION_DIR/"LIVE_MEASUREMENTS.json"),("Ten-cartridge X-ray measurements (.json)",XRAY_FILE),
           ("Source document record (.json)",DOC_FILE),("Model identity record (.json)",MODEL_FILE),("Date comparison record (.json)",DATES_FILE),
           ("Verification record (.json)",VERIFY_FILE),("Initialization record (.json)",INIT_FILE),("Session log (.log)",SESSION_LOG),("Session events (.jsonl)",SESSION_EVENTS),
           ("Interface questions and answers (.jsonl)",SESSION_QA),("Figure manifest (.json)",SESSION_DIR/"FIGURES_MANIFEST.json"),("SHA-256 manifest (.json)",MANIFEST)]+\
          [(f"HISTORICAL · published {n} of an earlier run (not this session)",HIST_DIR/("HISTORICAL_"+n)) for n in HISTORICAL]
    return [(l,str(p)) for l,p in items if Path(p).is_file()]

# ---------------------------------------------------------------------------------------------------------------------
# AUTOMATIC INITIALIZATION — one start, every step real, stops at the first failure
# ---------------------------------------------------------------------------------------------------------------------
def _step_experiment():
    r=run_experiment();rec,dates=model_and_dates_records()
    _OUT.write(f"  model snapshot loaded: {rec.get('loaded_snapshot_commit')} · {dates['statement']}\n");_OUT.flush()
    return dict(r,loaded_snapshot=rec.get("loaded_snapshot_commit"))
def _step_verify():
    verify_disk();verify_weights();v=compute_verification()
    for it in v["items"]:_OUT.write(f"  {'PASS' if it['passed'] else 'FAIL'}  {it['name']:<40} {short(it['detail'] if isinstance(it['detail'],str) else json.dumps(it['detail'],ensure_ascii=False),90)}\n")
    _OUT.flush()
    if not v["ready"]:raise RuntimeError("LIVE VERIFICATION FAILED: "+", ".join(i["name"] for i in v["items"] if not i["passed"]))
    return dict(passed=v["passed"],total=v["total"])
def _step_ready():
    t=mount(cart_ids()[0]);return dict(cartridge=t["cartridge"],rows=t["cache_tokens"],seconds=round(t["end_to_end_ms"]/1000,2))
def _step_figures():
    out,errs=render_figures()
    if errs or len(out)!=len(FIG_FUNCS):raise RuntimeError(f"FIGURES: {len(out)}/{len(FIG_FUNCS)} generated · {errs}")
    dump_json(INIT_FILE,INIT);z=package_session()
    return dict(figures=[Path(r["jpg"]).name for r in out.values()],zip=Path(z).name)
STEP_FUNCS=OrderedDict([("SOURCES",sources_step),("PREFLIGHT",preflight),("DOCUMENT",document_step),("EXPERIMENT",_step_experiment),
                        ("XRAY",xray_all),("VERIFY",_step_verify),("READY_MEMORY",_step_ready),("FIGURES",_step_figures)])

def init_failed(key,ex):
    tb=traceback.format_exc()
    INIT["failed"]=dict(step=key,title=INIT_STEPS[key],error=f"{type(ex).__name__}: {ex}",last_successful_step=INIT["last_ok"],utc=utc_now(),traceback=tb[-6000:],
                        engine_status=(E.get("R718") or {}).get("status"),last_engine_lines=[f"{ts} {l}" for ts,_,l in ENGINE_LINES[-40:]],
                        last_heartbeat=(HEARTBEATS[-1] if HEARTBEATS else None),engine_started_utc=ENGINE.get("started_utc"))
    _release("initialization failed")
    slog("INIT_FAILED",key,error=INIT["failed"]["error"],last_successful_step=INIT["last_ok"],engine_status=INIT["failed"]["engine_status"],traceback=tb[-3000:])
    try:dump_json(INIT_FILE,INIT);package_session()
    except Exception as ex2:_OUT.write(f"  (failure package could not be written: {ex2})\n")
    banner(f"INITIALIZATION STOPPED — the demonstration is NOT ready and no interface is opened.\n"
           f"  failed step          : {key} · {INIT_STEPS[key]}\n  error                : {INIT['failed']['error']}\n"
           f"  last successful step : {INIT['last_ok'] or 'none'}\n  records              : {SESSION_DIR}\n  all files (ZIP)      : {ZIP_PATH if ZIP_PATH.is_file() else 'not written'}","█")

def run_initialization():
    banner(f"{APP_TITLE}\n{VERSION_NOTE} · session {SESSION_ID} · records in {SESSION_DIR}\n"
           "Automatic initialization: every step below is executed for real in this runtime; nothing is precomputed.","#")
    for key,fn in STEP_FUNCS.items():
        t0=step_begin(key)
        try:info=fn()
        except BaseException as ex:
            init_failed(key,ex);raise RuntimeError(f"INITIALIZATION FAILED at {key}: {type(ex).__name__}: {ex}") from ex
        step_done(key,t0,result=info)
    INIT["ready"]=True;INIT["ready_utc"]=utc_now();INIT["total_seconds"]=round(time.perf_counter()-INIT["started"],1)
    dump_json(INIT_FILE,INIT);package_session()
    banner(f"READY — all {len(STEP_FUNCS)} steps passed in {INIT['total_seconds']/60:.1f} min · live verification "
           f"{STATE['verification']['passed']}/{STATE['verification']['total']} · mounted {STATE['cartridge']} ({STATE['mount']['cache_tokens']:,} rows)","#")
    slog("READY","initialization complete",seconds=INIT["total_seconds"])
    return True
  # ===== PART 3/3 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 3 — Gradio Interface, User Interaction, Research Presentation and Session Logging
# Same working method and interface as the previous Qwen2.5-72B demonstration: start-up runs everything automatically
# (sources, preflight, the original Siemens PDF, the unchanged TEST718 experiment, verification, a mounted cartridge,
# seven JPEG figures, ZIP), then the Gradio interface opens with the figures, individual downloads and the package.
# The interface calls the engine, records and displays. It never computes or edits an answer.
# =====================================================================================================================
def esc(x):return html.escape(str(x))
def card_html(title,body,kind="info"):return f'<div class="kz card {kind}"><div class="h">{esc(title)}</div><div class="small">{body}</div></div>'
def chip(bid):
    if not bid:return "<span class='chip' style='color:#374151;border-color:#9ca3af'>vanilla · no memory</span>"
    c=ccol(cart_index(bid));return f'<span class="chip" style="color:#fff;background:{c};border-color:{c}">{esc(bid)}</span>'

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
.ans{white-space:pre-wrap;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;border:1px solid var(--kz-bd);border-radius:4px;padding:6px 8px;margin:3px 0;max-height:420px;overflow:auto}
#kz_ask button,#kz_ask{font-size:clamp(15px,4.2vw,18px)!important;font-weight:700!important;min-height:52px!important}
@media (max-width:640px){.tbl .hide-m{display:none}}
"""
HERO=(f'<div class="kz hero"><span class="rec">Live research demonstration · frozen Qwen2.5-72B · real industrial manual · measured in this session</span>'
      f'<div class="brand">AKBASCORE AI TECHNOLOGY<br>SILICON HIPPOCAMPUS · SIEMENS SINUMERIK ONE</div><div class="title">A 486-PAGE INDUSTRIAL MANUAL IN TEN PHYSICAL MEMORY CARTRIDGES — frozen weights, auditable against the source</div>'
      '<ul class="msg">'
      f'<li>The original <b>{esc(DOC_TITLE)}, edition {DOC_EDITION_MARK}</b> is downloaded from Siemens in this session and locked by SHA-256. Its 486 pages are split into <b>ten page ranges C01–C10</b>.</li>'
      '<li>Each range is <b>forged alone</b> by the frozen model into a physical CUT3 cartridge on SSD: the layer-3 residual state <b>H3</b> and the keys/values of <b>layers 0–3</b>, with SHA-256.</li>'
      '<li>A readout loads <b>one cartridge</b> from SSD to the GPU, rebuilds layers 4–79 and answers with <b>only the question</b> as input — the PDF is not given again. The 72B weights are never changed.</li>'
      '<li>Every answer is compared with the <b>vanilla model</b> (no PDF, no cartridge) and checked <b>automatically</b> against the PDF (stated page, verbatim word overlap). Answers are <b>not verified technical truth</b>.</li>'
      '<li>The ten readouts are combined by <b>text-mediated synthesis</b>: the frozen model reads the ten text answers with no cartridge attached. It is not native multi-cartridge synthesis.</li></ul>'
      f'<div class="by"><b>{esc(AUTHOR)}</b> · {esc(ORG)} · {esc(PLACE)} · {esc(VERSION_NOTE)}</div>'
      f'<div class="lic">{esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · <a href="{REPO}" target="_blank" rel="noopener">{esc(REPO)}</a> · Siemens manual © Siemens AG (not redistributed)</div></div>')
SCOPE_HTML=card_html("What this demo shows — and what it does not",
    "Shown, measured in this session: the unchanged TEST718 experiment forges ten physical cartridges from the original 2025 Siemens manual, restores each one from SSD on the GPU, "
    "answers a source-derived question with and without the cartridge, repeats three questions after release, maps the cartridges' H3 similarity and synthesises the ten text answers; "
    "afterwards every cartridge is mounted alone once more and its 80-layer K/V tensors are X-rayed read-only (Figure 5); "
    "the weights stay frozen and every file is SHA-256 verified. Not shown: verified technical correctness (answers are raw; checks are automatic), blind question answering (questions "
    "contain the section heading), ten cartridges jointly in GPU memory, native neural synthesis. The date gap between the model release and the manual edition is not proof that the "
    "model lacked this information.","warn")
PREV_HTML=card_html(PREV_TITLE,f"{esc(PREV_TEXT)}<br><br>For the implementation, experimental evidence, and multi-cartridge question-answering observations, see: "
                    f"<b>Research Record III — Qwen2.5-72B, Direct Internal-State Injection</b> · Zenodo Record 23434686 · "
                    f"<a href='https://zenodo.org/records/23434686' target='_blank' rel='noopener'>https://zenodo.org/records/23434686</a><br>"
                    f"<i>Previously published research — not a result of this Siemens experiment.</i>","info")

def engine_card_html():
    a=engine_architecture() or {};v=STATE.get("verification") or {};env_=(E.get("R718") or {});mi=MODEL_IDENTITY
    rows=[("Model",f"{MODEL_ID} · NF4 4-bit, BF16 compute · frozen · snapshot {str(mi.get('loaded_snapshot_commit'))[:12]}"),
          ("Model release",f"first public release {MODEL_RELEASE['date']} ({MODEL_RELEASE['url']})"),
          ("Architecture",f"{a.get('layers')} layers · hidden {a.get('hidden')} · {a.get('q_heads')} Q / {a.get('kv_heads')} KV heads · head dim {a.get('head_dim')} · CUT{a.get('cut')}"),
          ("Source document",f"{DOC_TITLE} · edition {DOC_EDITION_MARK} (on {DOC.get('edition_mark_pages')} pages) · {DOC.get('pages')} pages · SHA-256 {str(DOC.get('sha256'))[:16]}… · downloaded {str(DOC.get('download_end_utc'))[:19]} UTC"),
          ("Experiment",f"718.py git blob {LOCKS['718.py'][:12]}… · executed unchanged · status {env_.get('status')} · {ENGINE.get('seconds')} s"),
          ("Cartridges",f"{N_CART} on SSD · SHA-256 re-verified · one mounted at a time · GPU reserve {E.get('GPU_RESERVE_GIB')} GiB (unchanged)"),
          ("Live verification",f"{v.get('passed')}/{v.get('total')} passed"),
          ("Generation",f"greedy · at most {READOUT_MAX_NEW} new tokens per answer (TEST718 readout) · synthesis up to {SYNTH_MAX_NEW}"),
          ("Engine ready",f"{INIT.get('ready_utc')} · start-up {INIT.get('total_seconds',0)/60:.1f} min")]
    return card_html("Engine (measured at start-up in this session)",'<table class="tbl">'+"".join(f"<tr><th>{esc(x)}</th><td class='mono'>{esc(y)}</td></tr>" for x,y in rows)+"</table>","on")

def stages_html():
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

def pdf_card():
    d=DOC
    return card_html("Original Siemens PDF used in this session",
        f"<b>{esc(DOC_TITLE)}</b> · edition {esc(DOC_EDITION_MARK)} (printed on {esc(d.get('edition_mark_pages'))} of {esc(d.get('pages'))} pages) · order no. {esc(d.get('order_number'))} · {esc(d.get('software_version'))}<br>"
        f"downloaded {esc(d.get('download_start_utc'))} → {esc(d.get('download_end_utc'))} UTC · {d.get('bytes',0):,} bytes · SHA-256 <span class='mono'>{esc(d.get('sha256'))}</span> (= TEST716 lock)<br>"
        f"⬇ <a href='{PDF_URL}' target='_blank' rel='noopener'><b>Download the original PDF from the official Siemens address</b></a> and compare its SHA-256 with the value above "
        f"(record: SOURCE_DOCUMENT_RECORD.json).<br><i>{esc(PDF_POLICY)}</i> <a href='{PDF_TERMS_URL}' target='_blank' rel='noopener'>Siemens terms</a>. "
        f"The verified copy stays only inside this Colab runtime: <span class='mono'>{esc(d.get('verified_local_copy'))}</span>","info")
def cond_choices():
    ch=[]
    for i,b in enumerate(E["R"]["books"]):
        h=E["chosen"][i][3] if "chosen" in E else ""
        ch.append((f"{b['id']} · PDF pages {b['page_range'][0]}–{b['page_range'][1]} · {b['body_tokens']:,} tokens · e.g. “{h}”",b["id"]))
    return ch+[("Vanilla model · no PDF, no cartridge","NONE")]
def suggested_question(sel):
    if sel=="NONE" or sel not in cart_ids():return E["question"](E["chosen"][0])
    return E["question"](E["chosen"][cart_index(sel)])
def condition_info(sel):
    r=None
    if LIVE.get("rows") and sel in cart_ids():r=LIVE["rows"][cart_index(sel)]
    head=f"Mounted now: {chip(STATE['cartridge'])}"+(f" · {STATE['mount']['cache_tokens']:,} rows" if STATE.get("mount") else "")
    if sel!="NONE" and sel!=STATE["cartridge"]:head+=f"<br><b>Selected {esc(sel)}</b> — pressing ASK releases the current cartridge and restores {esc(sel)} from SSD (about 30–60 s)."
    if sel=="NONE":head+="<br><b>Vanilla model selected</b> — the question is answered without any cartridge."
    body=""
    if r:
        body=(f"<br><br><b>{esc(r['id'])}</b> · PDF pages {r['pages'][0]}–{r['pages'][1]} · {r['body_tokens']:,} tokens · file {r['file_bytes']:,} B · SHA-256 <span class='mono'>{esc(str(r['cartridge_sha256'])[:16])}…</span> "
              f"{'✓ re-verified' if r['file_sha_ok'] else '✗'}<br>TEST718 heading: <i>{esc(r['heading'])}</i> (PDF page {r['heading_page']})"
              f"<br>Start-up readout: {r['physical_wall_s']} s · stated page → {esc(r['page_physical']['result'])} · 5-gram support {pct(r['support_physical']['share'])} (vanilla {pct(r['support_vanilla']['share'])})")
    return card_html("Memory condition",head+body,"info")

def answer_html(r,c,mnt=None):
    t=""
    if mnt:
        t+=(f"<div class='small'><b>Cartridge restored from SSD</b> · {chip(mnt['cartridge'])} SSD read + SHA-256 {mnt['ssd_load_ms']/1000:.2f} s · host→GPU {mnt['h2d_ms']:.0f} ms · "
            f"rebuild {mnt['rebuild_ms']/1000:.1f} s · {mnt['cache_tokens']:,} rows</div>")
    t+="<table class='tbl'><tr><th>memory</th><th>raw model answer</th><th class='hide-m'>time</th></tr>"
    if r is not None:t+=f"<tr><td>{chip(r['cartridge'])}<div class='small mono'>{r['cache_tokens']:,} rows · {r['answer_tokens']} tok</div></td><td><div class='ans'>{esc(r['raw'])}</div></td><td class='hide-m mono'>{r['seconds']} s</td></tr>"
    if c is not None:t+=f"<tr><td>{chip(None)}<div class='small mono'>{c['answer_tokens']} tok</div></td><td><div class='ans'>{esc(c['raw'])}</div></td><td class='hide-m mono'>{c['seconds']} s</td></tr>"
    t+="</table>"
    x=r or c
    t+=(f"<div class='small mono' style='margin-top:8px;opacity:.8'>question {esc(x['question'])}<br>max new tokens {READOUT_MAX_NEW} · NOT VERIFIED — check against the Siemens PDF · GPU free {x['gpu'].get('free_gib')} GiB · {esc(x['utc'])}</div>")
    return card_html("Answer of the frozen Qwen2.5-72B — raw output, unedited",t,"on")

GPU_LOCK=threading.Lock()
def busy_card():return card_html("Busy","Another run is using the GPU. Please wait until it has finished and press the button again.","warn")
def err_card(ex):
    oom="OutOfMemoryError" in type(ex).__name__ or "GPU_SAFETY_STOP" in str(ex)
    hint=" The TEST709 GPU safety reserve stopped the operation (or CUDA ran out of memory); the memory was released. Press ASK again." if oom else ""
    return card_html("Error",f"<code>{esc(type(ex).__name__)}: {esc(ex)}</code>{esc(hint)}<br>Nothing was hidden or replaced; the full traceback is in the Error log tab.","err")

def all_files():
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

def ask_handler(sel,question,vanilla):
    NO=("","",None)
    keep=(gr.update(),gr.update(),gr.update(),condition_info(sel))
    if not GPU_LOCK.acquire(blocking=False):yield (busy_card(),)+NO+keep;return
    try:
        q=(question or "").strip()
        if not q:raise OpError("Type a question first.")
        mnt=None;r=None;c=None
        if sel!="NONE":
            if STATE["cartridge"]!=sel or STATE["memory"] is None:
                yield (card_html("Running",f"Restoring cartridge {esc(sel)} from SSD (TEST718: cart_load → SHA-256 → initialize) …","info"),)+NO+keep
                mnt=mount(sel)
            yield (card_html("Running",f"Cartridge {esc(sel)} mounted · asking the frozen model{' and the vanilla model' if vanilla else ''} (up to {READOUT_MAX_NEW} tokens each) …","info"),)+NO+keep
            r=ask(q[:3000],True)
            if vanilla:c=ask(q[:3000],False)
        else:
            yield (card_html("Running","Asking the vanilla model (no cartridge) …","info"),)+NO+keep
            c=ask(q[:3000],False)
        rec=dict(question=q,selection=sel,memory=r,vanilla=c,mount=mnt,session=SESSION_ID)
        d=SESSION_DIR/"single_runs";d.mkdir(exist_ok=True)
        p=dump_json(d/f"ASK_{sel}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json",rec)
        files,z,summ=refresh_package()
        yield (answer_html(r,c,mnt),json.dumps(jsafe(rec),ensure_ascii=False,indent=1)[:200000],"",str(p),files,z,summ,condition_info(sel))
    except Exception as ex:
        slog("UI_ERROR","ask",error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc()[-3000:])
        files,z,summ=refresh_package()
        yield (err_card(ex),"",traceback.format_exc(),None,files,z,summ,condition_info(sel))
    finally:GPU_LOCK.release()

def select_handler(sel,current):
    qs={E["question"](x) for x in E["chosen"].values()} if "chosen" in E else set()
    newq=suggested_question(sel) if (not (current or "").strip() or current in qs) else current
    return condition_info(sel),newq

def verify_handler():
    if not GPU_LOCK.acquire(blocking=False):return busy_card()
    try:
        w=verify_weights();d=verify_disk()
        rows=[("time (UTC)",w["utc"]),("weight sentinel at load (TEST718)",w["before"]),("weight sentinel now",w["after"]),("sentinel unchanged",w["passed"]),
              ("trainable tensors",sum(1 for p in E["model"].parameters() if p.requires_grad))]+[(f"cartridge {f['cartridge']} SHA-256 on SSD = engine record",f["equals_engine_record"]) for f in d["files"]]
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
    first=cart_ids()[0]
    with blocks as demo:
        gr.HTML(HERO);gr.HTML(engine_card_html())
        cond_dd=gr.Dropdown(choices=cond_choices(),value=first,label="Memory condition (one physical cartridge at a time, or the vanilla model)",interactive=True)
        info=gr.HTML(condition_info(first))
        cq=gr.Textbox(value=suggested_question(first),label="Question (answered from the selected cartridge; raw output, not verified)",lines=3,max_lines=8)
        ctl=gr.Checkbox(value=True,label="Also ask the same question to the vanilla model (no PDF, no cartridge)")
        ask_b=gr.Button("ASK",variant="primary",elem_id="kz_ask")
        status=gr.HTML(stages_html())
        gallery=_gallery(label=f"Figures 1–{len(FIGURES)} (JPEG, 300 dpi) — measured in this session",value=gallery_items())
        files=gr.File(label="Individual downloads · figures, ZIP, run summary, live engine output, records, manifest, historical logs",value=all_files(),file_count="multiple",interactive=False)
        gr.HTML(pdf_card())
        zipb=gr.DownloadButton(label="⬇ Download the complete experiment package (.zip)",value=str(ZIP_PATH),interactive=True)
        single_file=gr.File(label="Record of the last question (.json)",interactive=False)
        with gr.Tabs():
            with gr.Tab("Run summary"):summ=_tb(lines=14,max_lines=40,label="RUN_SUMMARY.txt",value=summary_text())
            with gr.Tab("Raw record (last question)"):raw=_tb(lines=14,max_lines=40,label="JSON")
            with gr.Tab("Error log"):errs=_tb(lines=10,max_lines=40,label="traceback (empty = no error)")
        with gr.Accordion("Verify the frozen weights and the ten cartridge files now",open=False):
            vb=gr.Button("Verify now");vout=gr.HTML()
        gr.HTML(SCOPE_HTML);gr.HTML(PREV_HTML)
        gr.HTML(f'<div class="kz small" style="opacity:.8;margin:8px 0 18px">{esc(AUTHOR)} · {esc(ORG)} · {esc(LICENSE_NAME)} · '
                f'TEST718 <a href="{URL_718}" target="_blank" rel="noopener">718.py</a> · TEST716 <a href="{URL_716}" target="_blank" rel="noopener">716.py</a> · TEST709 <a href="{URL_709}" target="_blank" rel="noopener">709.py</a> · '
                +" · ".join(f'<a href="{u}" target="_blank" rel="noopener">{esc(t.split(" — ")[0])}</a>' for t,u in LINEAGE)+
                ' · Qwen2.5-72B-Instruct, the Siemens manual and third-party libraries remain under their own licences.</div>')
        cond_dd.change(select_handler,inputs=[cond_dd,cq],outputs=[info,cq])
        outs=[status,raw,errs,single_file,files,zipb,summ,info]
        ask_b.click(ask_handler,inputs=[cond_dd,cq,ctl],outputs=outs)
        vb.click(verify_handler,outputs=vout)
    try:demo.queue(default_concurrency_limit=1)
    except TypeError:demo.queue(concurrency_count=1)
    return demo

# ---------------------------------------------------------------------------------------------------------------------
# START-UP (as in the previous demonstration): the experiment runs automatically, then the interface opens
# ---------------------------------------------------------------------------------------------------------------------
_GR_MAJOR=int(re.match(r"\d+",gr.__version__).group())
try:run_initialization()
except Exception as _ex:
    _m=str(_ex)
    _hint=("A locked source changed on GitHub — the program stops instead of running unverified code." if "LOCKED SOURCE" in _m or "BLOB" in _m or "DRIFT" in _m else
           "The Siemens PDF could not be downloaded or no longer matches the locked SHA-256: check the network or the Siemens address and run again." if "SOURCE DOCUMENT" in _m or "PDF" in _m else
           "Hugging Face refused the model download: add your token as the Colab secret HF_TOKEN (allow notebook access) and run again." if any(x in _m for x in ("401","403","gated","Unauthorized","token")) else
           "GPU memory: the TEST709 safety reserve or CUDA stopped the run. Use an A100 80 GB runtime (Runtime → Change runtime type), restart the session and run again." if any(x in _m for x in ("GPU_SAFETY_STOP","out of memory")) else
           "This runtime is not an A100 80 GB: Runtime → Change runtime type → A100, then run again." if any(x in _m for x in ("A100","CUDA is not available","exactly one GPU")) else
           "Disk: free space in the Colab runtime (or use a runtime with more disk) and run again." if "disk" in _m.lower() else
           "Network error while downloading a locked source, the Siemens PDF or the model: run the cell again." if any(x in _m for x in ("URLError","timed out","HTTP Error","Connection")) else
           "See the traceback above; nothing was changed in the engine.")
    _OUT.write("\n"+"="*110+f"\nENGINE START FAILED — {type(_ex).__name__}: {_m}\nWHAT TO DO: {_hint}\nRecords of this attempt: {SESSION_DIR}\n"+"="*110+"\n");_OUT.flush()
    raise
demo=build_ui()
slog("LAUNCH","public share link — open the printed gradio.live address (also works on a phone)")
_LAUNCH=dict(share=True,allowed_paths=[str(SESSION_DIR)],show_error=True,inline=False)
if _GR_MAJOR>=6:_LAUNCH["css"]=CSS
try:demo.launch(**_LAUNCH)
except TypeError as _ex:
    if "css" not in str(_ex):raise
    _LAUNCH.pop("css",None);demo.launch(**_LAUNCH)

