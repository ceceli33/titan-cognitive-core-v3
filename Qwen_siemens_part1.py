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
