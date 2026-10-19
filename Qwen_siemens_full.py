# =====================================================================================================================
# AKBASCORE AI TECHNOLOGY — SILICON HIPPOCAMPUS · Qwen2.5-72B-Instruct / SIEMENS SINUMERIK ONE PHYSICAL MEMORY
# Live research demonstration of the TEST719 experiment: five physical CUT3 pair memories → S1–S5 → one new cartridge C11
# single Google Colab cell (3 parts) · NVIDIA A100 80 GB · same working method as the previous Siemens / Qwen2.5-72B demonstrations
# PART 1 / 3 — Engine Initialization, Source Document and Physical Cartridge Infrastructure
# ---------------------------------------------------------------------------------------------------------------------
# HOW TO RUN: paste PART 1, PART 2 and PART 3 one below the other into ONE Colab cell and press RUN once.
#             Each part is below 85,000 characters. If Colab reports a SyntaxError near the end of a part, that part was cut
#             while copying: copy it again completely (every part ends with the line '# ===== END OF PART k/3 =====').
# Without any button, in this order:
#   [1] verified sources      716.py, 709.py (git blob locks), LICENSE, published logs 716/717/718 (historical only),
#                             the TEST719 program files embedded in this cell (SHA-256 checked when written)
#   [2] system preflight      one A100 80 GB (nvidia-smi only — this notebook process does not touch CUDA before step [8]),
#                             RAM, disk, Hugging Face cache state and model identity of Qwen2.5-72B-Instruct
#   [3] source document       the ORIGINAL Siemens PDF from the official Siemens address: download time (UTC), size,
#                             pages, SHA-256 (must equal the TEST716 lock), PDF metadata, edition marking on the pages
#   [4] question panel        five fixed questions. Every expected answer is searched on the real PDF inside the declared
#                             cartridge page range; a wrong page range or an answer not found STOPS the run here — before
#                             any model is loaded. Then the panel is sealed (SHA-256). The build process never reads it.
#   [5] PROCESS 1 (build)     a separate Python process runs the unchanged TEST716 set-up (PDF lock, ten page ranges, frozen
#                             72B NF4 model, ten CUT3 cartridges C01–C10 forged with the unchanged TEST709 engine), then five
#                             physical pairs: initialize(C01) → append(C02) … initialize(C09) → append(C10), every append
#                             verified by the engine on all 80 layers (exact SHA-256). From each joint pair memory one
#                             question-independent general synthesis → cartridges S1–S5 → S1–S5 physically joined →
#                             general final synthesis → cartridge C11. A synthesis is accepted only if the end of generation
#                             is observed as a stop token AND it ends with "END OF SYNTHESIS"; otherwise no cartridge is
#                             written and the run stops.
#   [6] PROCESS 2 (C11 alone) a NEW Python process on the same Colab VM, started after process 1 exited, with an empty GPU.
#                             The build directories are quarantined (audit hook). It loads the frozen model and ONLY C11,
#                             audits the GPU memory, asks the five sealed questions, then asks them without any document.
#   [7] live verification     every record of steps [4]–[6] is checked (SHA-256, appends, syntheses, isolation, weights)
#   [8] ready memory          after process 2 has ended: the frozen model + C11 are loaded in this notebook process for the
#                             interface (questions asked there are NOT part of the sealed panel)
#   [9] figures + downloads   three JPEG figures from THIS run's records, automatic layout quality control of every JPEG,
#                             logs, manifest, Download-All ZIP
#   While processes 1 and 2 run, a heartbeat line every 60 s shows elapsed time, the last process line, GPU memory
#   (nvidia-smi), RAM and the size of the model download, so a stalled or interrupted run can be diagnosed from the records.
#   → then the Gradio interface opens. Any failure stops here and is reported; no interface is presented as ready.
# Scientific boundaries
#   · C11 is a NEW physical memory written from a model-generated general synthesis. It is not a lossless physical merge
#     of C01–C10. Information that the syntheses left out is not in C11.
#   · The syntheses are question-independent (the prompts contain no question, answer or keyword of the panel).
#   · Five questions are a live demonstration, not a statistical result. The automatic indicator (CORRECT / INCORRECT /
#     UNCLEAR / INCOMPLETE / UNVERIFIED FINISH) is a fixed text rule, not expert verification. The reader judges the raw answers.
#   · A correct answer WITHOUT a document can come from pre-training (earlier SINUMERIK manuals are public).
#   · Process 2 runs on the same Colab VM in a new process; it is not a separate machine. The GPU memory audit cannot exclude
#     foreign resident memory smaller than 32 MiB (about 100 K/V rows).
#   · Multi-cartridge consolidation in one live K/V memory was demonstrated earlier (Research Record III, Zenodo 23434686).
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
import os,sys,re,io,ast,json,time,html,math,shutil,zipfile,hashlib,platform,threading,traceback,subprocess,importlib.util,textwrap,copy,unicodedata
from pathlib import Path
from datetime import datetime,timezone,date
from collections import Counter,OrderedDict

def _pip(*pk):subprocess.check_call([sys.executable,"-m","pip","install","-q",*pk])
for _m,_p in (("numpy","numpy"),("matplotlib","matplotlib"),("PIL","pillow"),("pymupdf","pymupdf"),("psutil","psutil")):
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
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF","expandable_segments:True")   # PyTorch allocator option against fragmentation of the growing K/V cache (inherited by processes 1 and 2)

# ---------------------------------------------------------------------------------------------------------------------
# identity, sources, locks and research lineage
# ---------------------------------------------------------------------------------------------------------------------
APP_TITLE="AKBASCORE AI TECHNOLOGY — SILICON HIPPOCAMPUS · Qwen2.5-72B / SIEMENS SINUMERIK ONE"
APP_SHORT="AKBASCORE Silicon Hippocampus · Qwen2.5-72B · Siemens SINUMERIK ONE · TEST719"
VERSION_NOTE="new experiment TEST719 — unpublished, no DOI"
AUTHOR="Mustafa Akbaş";ORG="AkbasCore AI Teknoloji";PLACE="Mersin, Türkiye"
LICENSE_NAME="AKBASCORE RESEARCH SOFTWARE LICENSE";COPYRIGHT="Copyright © 2026 Mustafa Akbaş"
REPO="https://github.com/ceceli33/titan-cognitive-core-v3"
RAW_BASE="https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
URL_LICENSE=REPO+"/blob/main/LICENSE";URL_716=REPO+"/blob/main/716.py";URL_709=REPO+"/blob/main/709.py"
URL_PREV_DEMO=REPO+"/blob/main/MAM_part1_QWEN_72B.py"
# git blob identifiers (git hash-object) of the files this program trusts
LOCKS=OrderedDict([
    ("716.py","913fa7a4951f2072df4be2eb49120ea86efa5477"),    # TEST716 set-up (executed unchanged by process 1 / model part by process 2)
    ("709.py","6c9f8cbb1eeed848d45133d73f0d7676b68e9125"),    # TEST709 CUT3 engine functions (locked inside 716.py)
    ("LICENSE","9aad4724d1072f9e56486650a9527380c867a53b"),
    ("716.log","1b87e698a0420bb524bd93854709cef9e4069484"),   # historical: earlier TEST716 run (routing comparison)
    ("717.log","2f6225db7346854e9cebded269b002293a93392d"),   # historical: earlier TEST717 run (80-layer routing X-ray)
    ("718.log","25c96ade2942727289530526b7fe15dd9beddc02")])  # historical: earlier TEST718 run (not this session)
HISTORICAL=("716.log","717.log","718.log")
EXPECTED_ARCH=(80,8192,64,8,128);EXPECTED_CUT=3;EXPECTED_RESERVE_GIB=9.0;N_CART=10;N_PAIRS=5;INTERACTIVE_MAX_NEW=1024
PAIRS=[("C01","C02"),("C03","C04"),("C05","C06"),("C07","C08"),("C09","C10")]
# the original document (the SHA-256 is the TEST716 lock; this program checks it independently as well)
PDF_URL="https://cache.industry.siemens.com/dl/files/087/109994087/att_1338962/v1/ONE_universal_op_man_0725_en-US.pdf"
PDF_SHA256="88c0f8293ce3302135042baf35d704303fb3b5a24915e28b8ca16f3192a7cc1d";PDF_PAGES=486
PDF_TERMS_URL="https://support.industry.siemens.com/dokumentation/ExtendedAGB.aspx"
PDF_POLICY=("Not redistributed: Siemens terms restrict passing documents on to third parties (e.g. section 2.3 of the Siemens "
            "documentation terms). Download it from the official Siemens address and compare its SHA-256 with this record.")
DOC_TITLE="SINUMERIK ONE Universal Operating Manual";DOC_EDITION_MARK="07/2025";DOC_EDITION_TEXT="July 2025"
# TEST716 page ranges of the ten source cartridges (C01–C10); used here only for the source check of the question panel
BOUNDS=[(1,40),(41,96),(97,149),(150,197),(198,255),(256,311),(312,362),(363,415),(416,461),(462,486)]
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
C11_COLOR="#0F766E";LOWER_COLOR,UPPER_COLOR,CUT_COLOR="#047857","#6D28D9","#111827"
ESTIMATE_MIN=dict(typical=100,bad_case=210)   # planning estimate for steps [1]–[9] (not a guarantee; real times are logged)

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
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+".tmp");tmp.write_text(json.dumps(jsafe(obj),ensure_ascii=False,indent=2),encoding="utf-8");tmp.replace(path);return path
def jload(p,default=None):
    try:return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:return default
def gib(b):return b/2**30

# ---------------------------------------------------------------------------------------------------------------------
# demonstration directories and the SEPARATE session log (the process output is stored separately, line by line)
# ---------------------------------------------------------------------------------------------------------------------
DEMO_ROOT=Path("/content/AKBASCORE_SIEMENS_DEMO") if os.path.isdir("/content") else Path("/tmp/AKBASCORE_SIEMENS_DEMO")
SESSION_ID=datetime.now().astimezone().strftime("SIEM719-%Y%m%d-%H%M%S")
SESSION_DIR=DEMO_ROOT/"sessions"/SESSION_ID;EVIDENCE_DIR=DEMO_ROOT/"evidence";FIG_DIR=SESSION_DIR/"figures"
HIST_DIR=SESSION_DIR/"historical_reference_not_this_session";PRIVATE_DIR=DEMO_ROOT/"source_document_not_redistributed"
PROGRAM_DIR=DEMO_ROOT/"test719_program"            # the TEST719 program files of this cell (process 1 / process 2 run from here)
for _d in (SESSION_DIR,EVIDENCE_DIR,FIG_DIR,HIST_DIR,PRIVATE_DIR,PROGRAM_DIR):_d.mkdir(parents=True,exist_ok=True)
# experiment directories (kept across re-runs of the cell; completed phases are reused after their records are checked)
_CROOT=Path("/content") if os.path.isdir("/content") else Path("/tmp")
RUNS=_CROOT/"T719_RUNS"          # process 1 records, C01–C10/S1–S5/C11, syntheses — QUARANTINED while process 2 runs
ASK_DIR=_CROOT/"T719_ASK"        # process 2 records (C11 alone + document-free answers)
ASK_IN=_CROOT/"T719_ASK_IN"      # the only hand-off to process 2: C11.pt, C11.sha256, handoff.json
ENGINE_DIR=_CROOT/"AKBASCORE_TEST714"   # working directory of the unchanged TEST716 code (its ROOT)
RUNS.mkdir(parents=True,exist_ok=True)
SESSION_LOG=SESSION_DIR/"SESSION.log";SESSION_EVENTS=SESSION_DIR/"SESSION_EVENTS.jsonl";FIGURE_LOG=SESSION_DIR/"FIGURE_GENERATION.log"
SESSION_QA=SESSION_DIR/"SESSION_QA.jsonl";VERIFY_FILE=SESSION_DIR/"VERIFICATION_RECORD.json";INIT_FILE=SESSION_DIR/"INITIALIZATION_RECORD.json"
DOC_FILE=SESSION_DIR/"SOURCE_DOCUMENT_RECORD.json";MODEL_FILE=SESSION_DIR/"MODEL_IDENTITY_RECORD.json";PANEL_FILE=SESSION_DIR/"QUESTION_PANEL_SOURCE_CHECK.json"
LIVE_MEAS=SESSION_DIR/"LIVE_MEASUREMENTS.json"
_LOG_LOCK=threading.Lock()
def slog(kind,message="",**data):
    """session log: one human-readable line + one JSON event; never written into the process output"""
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
    ("SOURCES","Verified sources (engine locks, licence, historical logs, TEST719 program files)"),
    ("PREFLIGHT","System preflight: GPU, RAM, disk, model cache and model identity"),
    ("DOCUMENT","Original Siemens PDF: download, SHA-256, pages, edition marking"),
    ("PANEL","Five fixed questions: mandatory source check on the PDF and seal — before any model is loaded"),
    ("BUILD","PROCESS 1 — C01–C10, five physical pairs (80-layer SHA-256), S1–S5, C11"),
    ("ASK","PROCESS 2 — new Python process: C11 alone, five questions; the same questions without any document"),
    ("VERIFY","Live verification of the experiment records"),
    ("READY_MEMORY","Ready memory: frozen model + C11 mounted in this notebook process (interface)"),
    ("FIGURES","Three research figures and downloadable research artifacts")])
E={}                                               # engine namespace of THIS notebook process (filled only in step [8])
def _gpu_short():
    try:
        g=E["mem"]() if callable(E.get("mem")) else None
        if g:return f"GPU free {g['free_gib']:.2f} GiB · allocated {g['allocated_gib']:.2f} GiB · peak {g['peak_gib']:.2f} GiB"
        s=subprocess.run(["nvidia-smi","--query-gpu=memory.used,memory.total","--format=csv,noheader,nounits"],capture_output=True,text=True,timeout=20).stdout.strip()
        return f"GPU used {s.replace(', ',' / ')} MiB (nvidia-smi)" if s else ""
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

# the TEST719 program files are part of THIS cell; each one is written with its SHA-256 checked (a copy/paste error stops here)
PROGRAM={}
def _program_write(name,text,sha):
    b=text.encode("utf-8");got=sha_bytes(b)
    if got!=sha:raise RuntimeError(f"PROGRAM FILE ALTERED: {name} SHA-256 {got} != {sha} — the cell text was changed while copying; paste the three parts again")
    p=PROGRAM_DIR/name
    if not p.is_file() or p.read_bytes()!=b:p.write_bytes(b)
    PROGRAM[name]=dict(bytes=len(b),sha256=sha,local=str(p))

# ---------------------------------------------------------------------------------------------------------------------
# system preflight and model identity (read-only; NO CUDA call in this notebook process before step [8])
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

def nvsmi(query):
    r=subprocess.run(["nvidia-smi",f"--query-{query}","--format=csv,noheader,nounits"],capture_output=True,text=True,timeout=30)
    return [l.strip() for l in r.stdout.splitlines() if l.strip()]
def gpu_state():
    """GPU facts from nvidia-smi only — this notebook process must not create a CUDA context before process 2 has run"""
    try:
        g=nvsmi("gpu=name,memory.total,memory.used,driver_version");rows=[x.split(", ") for x in g]
        return dict(count=len(rows),name=rows[0][0],total_mib=int(rows[0][1]),used_mib=int(rows[0][2]),driver=rows[0][3],apps=nvsmi("compute-apps=pid,used_memory"))
    except Exception as ex:return dict(count=0,error=f"{type(ex).__name__}: {ex}",apps=[])

def preflight():
    """hardware and storage facts of this runtime; stops early when the run cannot succeed"""
    rep=dict(python=platform.python_version(),platform=platform.platform())
    g=gpu_state();rep["gpu"]=g;rep["nvidia_smi"]=f"{g.get('name')}, {g.get('total_mib')} MiB, {g.get('used_mib')} MiB used, driver {g.get('driver')}"
    try:
        mi=dict(l.split(":",1) for l in Path("/proc/meminfo").read_text().splitlines() if ":" in l)
        rep["ram_total_gib"]=round(int(mi["MemTotal"].split()[0])/2**20,1);rep["ram_available_gib"]=round(int(mi["MemAvailable"].split()[0])/2**20,1)
    except Exception:pass
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
    for k,v in (("GPU",f"{g.get('name')} · total {round((g.get('total_mib') or 0)/1024,2)} GiB · used {g.get('used_mib')} MiB · count {g.get('count')} · GPU processes {len(g.get('apps') or [])}"),("nvidia-smi",rep.get("nvidia_smi")),
                ("RAM",f"{rep.get('ram_available_gib')} / {rep.get('ram_total_gib')} GiB available"),("disk",f"{rep['cache_disk_free_gib']} GiB free for the model cache · {rep['demo_disk_free_gib']} GiB free for the demonstration"),
                ("model cache",rep["model_cache_state"]),("model",f"{MODEL_ID} · public release {MODEL_RELEASE['date']} ({MODEL_RELEASE['url']}) · Hub main commit {mi_.get('hub_main_commit')} · repo created {mi_.get('hub_repo_created')}"),
                ("time",f"planning estimate ≈ {ESTIMATE_MIN['typical']/60:.1f} h typical, ≈ {ESTIMATE_MIN['bad_case']/60:.1f} h bad case (not a guarantee; real times are logged)")):
        _OUT.write(f"  {k:<12}{v}\n")
    _OUT.flush()
    if g.get("count",0)==0:raise RuntimeError("PREFLIGHT: CUDA is not available (no GPU in nvidia-smi) — select a GPU runtime (A100 80 GB)")
    if g["count"]!=1:raise RuntimeError(f"PREFLIGHT: exactly one GPU is required, found {g['count']}")
    if "A100" not in str(g.get("name")) or (g.get("total_mib") or 0)<70*1024:raise RuntimeError(f"PREFLIGHT: an A100 80 GB is required; this GPU is {g.get('name')} with {g.get('total_mib')} MiB")
    own=[a for a in g.get("apps") or [] if a.split(",")[0].strip()==str(os.getpid())];other=[a for a in g.get("apps") or [] if a not in own]
    if other:raise RuntimeError(f"PREFLIGHT: another process is using the GPU {other} — Runtime → Restart session, then run again (completed phases are reused)")
    if own:
        rep["gpu_held_by_this_notebook"]=own
        _OUT.write(f"  note        this notebook process already holds GPU memory from an earlier run of the cell {own}: the finished experiment and the loaded model are reused\n");_OUT.flush()
    if mc.get("missing_bytes") is not None and shutil.disk_usage(cd).free<mc["missing_bytes"]+20*2**30:
        raise RuntimeError(f"PREFLIGHT: not enough disk for the model download: need {gib(mc['missing_bytes'])+20:.1f} GiB, free {rep['cache_disk_free_gib']} GiB")
    if shutil.disk_usage(DEMO_ROOT).free<20*2**30:raise RuntimeError("PREFLIGHT: less than 20 GiB free for sixteen cartridges, logs and figures")
    dump_json(SESSION_DIR/"PREFLIGHT.json",rep);return dict(gpu=g.get("name"),model_cache=rep["model_cache_state"])

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
# TEST719 program files (part 1 of 2): the five fixed questions, the build configuration (no questions) and the shared
# engine wrapper. The TEST709/TEST716 engines are NOT included here: they are downloaded and verified by git blob.
# ---------------------------------------------------------------------------------------------------------------------
_program_write('TEST719_demo_questions.json',r'''{
  "test": "TEST719-DEMO",
  "title": "Five physical CUT3 pairs -> S1-S5 -> C11 general synthesis cartridge; five fixed questions to C11 and to the document-free model",
  "document": {
    "title": "SINUMERIK ONE Universal Operating Manual",
    "edition": "07/2025",
    "software": "V6.25 SP1",
    "url": "https://cache.industry.siemens.com/dl/files/087/109994087/att_1338962/v1/ONE_universal_op_man_0725_en-US.pdf",
    "sha256": "88c0f8293ce3302135042baf35d704303fb3b5a24915e28b8ca16f3192a7cc1d",
    "pages": 486
  },
  "questions": [
    {
      "id": "Q1",
      "text": "What is the exact keyboard shortcut used to activate the Korean IME character input system?",
      "verifiable_answer": "Alt + S",
      "region": "C02 (pair P1)",
      "requires_cartridges": [
        "C02"
      ],
      "source": "07/2025 manual, section 3.3.14 \"Entering Korean characters\" (printed pages 55-58)",
      "evidence": [
        {
          "cartridge": "C02",
          "window": 3,
          "min_page": 31,
          "all": [
            "korean",
            "alt\\s*\\+\\s*s\\b"
          ]
        }
      ],
      "rule": {
        "correct_any": [
          "alt\\s*\\+\\s*s\\b"
        ]
      },
      "leak_keywords": [
        "korean",
        "ime",
        "alt + s",
        "alt+s"
      ]
    },
    {
      "id": "Q2",
      "text": "What does the working area limitation function do on a SINUMERIK ONE control, and what does the operator achieve with it?",
      "verifiable_answer": "It limits the range within which the tool may traverse (in the channel axes); protection zones in the working area are set up that are inhibited for tool motion",
      "region": "C03 (pair P2)",
      "requires_cartridges": [
        "C03"
      ],
      "source": "07/2025 manual, section 5.6.1 \"Specify working area limitations\" (in section 5.6 \"Monitoring axis and spindle data\", PDF page about 107)",
      "evidence": [
        {
          "cartridge": "C03",
          "window": 2,
          "all": [
            "working area limitation",
            "protection zone"
          ]
        }
      ],
      "rule": {
        "correct_all": [
          "\\blimit",
          "(travers|travel|motion|moving|protect)"
        ]
      },
      "leak_keywords": [
        "working area limitation",
        "protection zone"
      ]
    },
    {
      "id": "Q3",
      "text": "Explain how an operator opens a DXF drawing and how an operator views a PDF document on a SINUMERIK ONE control: which operating area is used, and what is done in each case?",
      "verifiable_answer": "Both start in the \"Program manager\" operating area: for DXF, position the cursor on the DXF file and press the \"Open\" softkey (the CAD drawing is displayed with all its layers); for PDF documents, select the storage location in the Program manager and open the PDF file to view it",
      "region": "C04 (pair P2) + C07 (pair P4) — two different pairs",
      "requires_cartridges": [
        "C04",
        "C07"
      ],
      "source": "07/2025 manual, section 7.17.2.1 \"Open a DXF file\" (PDF page about 191, C04) and section 13.13 \"Viewing PDF documents\" (PDF page about 358, C07)",
      "evidence": [
        {
          "cartridge": "C04",
          "window": 2,
          "all": [
            "\\bdxf\\b",
            "\"open\" softkey",
            "layers"
          ]
        },
        {
          "cartridge": "C07",
          "window": 2,
          "all": [
            "viewing pdf documents",
            "program manager"
          ]
        }
      ],
      "rule": {
        "correct_all": [
          "program manager",
          "\\bdxf\\b",
          "\\bpdf\\b",
          "\\bopen"
        ]
      },
      "leak_keywords": [
        "dxf",
        "viewing pdf",
        "pdf document",
        "program manager"
      ]
    },
    {
      "id": "Q4",
      "text": "Which operating area is used both for displaying alarms and for setting remote access, and which softkeys open the alarm list and the remote diagnostics window?",
      "verifiable_answer": "The \"Diagnostics\" operating area; the \"Alarm list\" softkey opens the alarm list and the \"Remote diag.\" softkey opens the remote diagnostics window",
      "region": "C09 + C10 (pair P5) — two different cartridges",
      "requires_cartridges": [
        "C09",
        "C10"
      ],
      "source": "07/2025 manual, section 18.1 \"Alarm, error, and system messages\" (PDF pages about 455-460, C09) and section 18.7.1 \"Setting remote access\" (PDF page about 474, C10)",
      "evidence": [
        {
          "cartridge": "C09",
          "window": 2,
          "all": [
            "\"alarm list\" softkey",
            "diagnostics"
          ]
        },
        {
          "cartridge": "C10",
          "window": 2,
          "all": [
            "remote diag",
            "diagnostics"
          ]
        }
      ],
      "rule": {
        "correct_all": [
          "diagnostics",
          "alarm list",
          "remote diag"
        ]
      },
      "leak_keywords": [
        "alarm list",
        "remote diag",
        "remote access",
        "diagnostics"
      ]
    },
    {
      "id": "Q5",
      "text": "Which edition and software version of the SINUMERIK ONE Universal Operating Manual does your document information come from?",
      "verifiable_answer": "Edition 07/2025, CNC software V6.25 SP1",
      "region": "all cartridges (footer on every page) + C01 (title / legal pages)",
      "requires_cartridges": [
        "C01-C10"
      ],
      "source": "07/2025 manual: title and legal pages; the edition 07/2025 is printed in the footer of every page",
      "evidence": [
        {
          "cartridge": "C01",
          "window": 3,
          "all": [
            "v6\\.25\\s*sp1"
          ]
        },
        {
          "cartridge": "EVERY",
          "window": 1,
          "all": [
            "07/2025"
          ]
        }
      ],
      "rule": {
        "correct_all": [
          "(07\\s*/\\s*2025|july\\s+2025)",
          "6\\.25"
        ],
        "incorrect_any": [
          "6\\.2[0-4]\\b",
          "/\\s*2024",
          "\\b2024\\b"
        ]
      },
      "note": "Qwen2.5-72B was released in September 2024; edition 07/2025 / V6.25 SP1 cannot come from pre-training.",
      "leak_keywords": [
        "07/2025",
        "v6.25",
        "6.25",
        "edition"
      ]
    }
  ],
  "evaluation_policy": "Automatic indicator only, rules fixed before any model output: INCOMPLETE if the safety ceiling was reached; UNVERIFIED_FINISH if the end of generation could not be confirmed as a stop token; UNCLEAR if the answer abstains (UNKNOWN / not available), matches only part of a multi-part rule, or mixes the expected content with contradicting content; INCORRECT if it contradicts the rule or matches nothing; CORRECT if the rule is met. The raw answer is always shown in full; the reader judges. A correct no-document answer is shown as such; a correct C11 answer is not assumed to come from physical memory.",
  "conditions": {
    "C11": "frozen Qwen2.5-72B + C11 cartridge only (cart_load -> initialize), in a NEW Python process on the same Colab VM after the build process has exited; the question is passed unchanged to the unchanged 709 answer()",
    "NO_DOCUMENT": "frozen Qwen2.5-72B, answer(None, question) exactly as the TEST718 vanilla control (no document, no cartridge), same process as the C11 condition"
  },
  "ceilings": {
    "answer": 4096
  },
  "completion_rule": "COMPLETE only if the end of generation is observed as a stop token (<|im_end|>/EOS): the greedy token read from the lm_head output at every forward pass is recorded (observation only), the generated ids must equal the observed tokens, the number of forward passes must equal generated tokens + 1, and the last observed token must be a stop token. Reaching the safety ceiling = INCOMPLETE. Anything else = UNVERIFIED_FINISH. Neither is ever shown as complete.",
  "claims_policy": [
    "Physical K/V integrity (SHA-256, rows, X-ray) is reported separately from semantic content.",
    "C11 is a new physical memory written from a model-generated general synthesis; it is not a lossless physical merge of C01-C10.",
    "Five questions are a live demonstration, not a statistical result.",
    "The C11 answers are produced in a new Python process on the same Colab VM, not in a separate VM or runtime."
  ],
  "question_design": "Five fixed questions spread over the manual: P1/C02 (Q1), P2/C03 (Q2), P2/C04 + P4/C07 (Q3, two different pairs), P5/C09 + C10 (Q4, two cartridges), every cartridge (Q5). Pair P3 (C05/C06) is not covered by a question. Every expected answer must be found on the real PDF in the declared cartridge(s) before any model is loaded; otherwise the run stops."
}''','991fa92dd40931e2fb71a38f7b73b8b1ca2307a5ca423591619972bdc6776443')
_program_write('TEST719_demo_build_config.json',r'''{
  "purpose": "Question-independent configuration of the build process (pairs, general synthesis prompts, safety ceilings). It contains no question, no expected answer and no instruction to preserve any particular topic.",
  "pairs": [
    [
      "C01",
      "C02"
    ],
    [
      "C03",
      "C04"
    ],
    [
      "C05",
      "C06"
    ],
    [
      "C07",
      "C08"
    ],
    [
      "C09",
      "C10"
    ]
  ],
  "synthesis_prompts": {
    "pair": "The document information contains two consecutive sections of a technical operating manual: cartridge {a} (PDF pages {a1}-{a2}) followed by cartridge {b} (PDF pages {b1}-{b2}). Write a general technical synthesis of the complete content of both sections: the main topics, the operating procedures and functions, important conditions and constraints, and how the two sections relate. Cover all topics evenly and do not concentrate on any single topic. Use only the document information. Be concise. Finish with the line END OF SYNTHESIS.",
    "final": "The document information contains five syntheses (S1-S5) of consecutive parts of one technical operating manual. Write one general technical synthesis of the whole manual: the main topics, the operating procedures and functions, important conditions and constraints, and the relations between the parts. Cover all parts evenly and do not concentrate on any single topic. Use only the document information. Be concise. Finish with the line END OF SYNTHESIS."
  },
  "ceilings": {
    "pair_synthesis": 8192,
    "final_synthesis": 12288
  },
  "completion_rule": "The end of generation is observed (no effect on the computation): the greedy token read from the lm_head output at every forward pass is recorded; EOS = the generated ids equal the observed tokens, forward passes = generated tokens + 1 and the last observed token is a stop token (<|im_end|>/EOS). CEILING = the safety ceiling was reached (text cut). Otherwise the finish is reported as UNVERIFIED.",
  "stop_rule": "A synthesis cut at the safety ceiling is INCOMPLETE: no cartridge is written from it and the build stops. A synthesis that ended below the ceiling is accepted; if the stop token could not be confirmed (FINISH_UNVERIFIED) or the END OF SYNTHESIS line is missing / not last, this is recorded as a flag and reported in the final report — it does not stop the experiment.",
  "memory_rule": "After a GPU memory failure (709 GPU_SAFETY_STOP or CUDA OOM) the partial memory is dropped, unused cached GPU memory is released and the stage is rebuilt from the SHA-checked cartridges with the next profile: CUT3 chunk 256 → 128 tokens (reserve 9 GiB), then chunk 64 with reserve 6 GiB. Every append is verified on all 80 layers by exact SHA-256 in every attempt."
}''','7148366aae22c17adabdf55624c21644e8f89e31c72f8e85174ca54c223a50bb')
_program_write('TEST719_common.py',r'''# AKBASCORE TEST719 — common experiment layer (W1 source).
# Builds ON TOP of the unchanged TEST709 engine functions (loaded by the unchanged TEST716 setup).
# This module never redefines, patches or replaces an engine function. The only engine-namespace write
# is the TEST718 pattern of setting MAX_NEW around one answer() call, and registering new cartridges in
# R['books'] exactly as TEST716 does for C01-C10.
import os, sys, io, re, ast, gc, json, time, math, shutil, hashlib, threading, unicodedata, platform, socket, subprocess
from pathlib import Path
from datetime import datetime, timezone

VERSION = 'TEST719-W1'
LOCK709 = '6c9f8cbb1eeed848d45133d73f0d7676b68e9125'
LOCK716 = '913fa7a4951f2072df4be2eb49120ea86efa5477'
URL716 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/716.py'
MODEL_ID = 'Qwen/Qwen2.5-72B-Instruct'
MODEL_COMMIT = '495f39366efef23836d0cfae4fbe635880d2be31'
GIB = 2 ** 30
HERE = Path(__file__).resolve().parent
SOURCE_CART_IDS = [f'C{i:02d}' for i in range(1, 11)]

# ----------------------------------------------------------------------------------------- basics
def utc():
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds')

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def sha256_file(p, block=8 * 2 ** 20):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(block), b''):
            h.update(c)
    return h.hexdigest()

def git_blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def jdump(o):
    return json.dumps(o, ensure_ascii=False, indent=1, default=str, sort_keys=False)

def atomic_write(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_bytes(data if isinstance(data, bytes) else data.encode('utf-8'))
    tmp.replace(path)

class StageError(RuntimeError):
    pass

class GateStop(RuntimeError):
    """Pre-registered gate failed: the run stops, outputs are kept, nothing is patched."""

# ----------------------------------------------------------------------------------------- text normalisation (shared by Q0, scoring, CF)
_QUOTES = {'“': '"', '”': '"', '„': '"', '«': '"', '»': '"', '‘': "'", '’': "'"}

def norm_text(s):
    s = unicodedata.normalize('NFKC', s or '')
    for a, b in _QUOTES.items():
        s = s.replace(a, b)
    s = re.sub(r'-\s*\n\s*', '', s)          # hyphenated line breaks
    s = re.sub(r'\s+', ' ', s)
    return s.strip().lower()

QUOTED_RE = re.compile(r'["“”]([^"“”\n]{1,60})["“”]')

def quoted_terms(s):
    return [m.group(1).strip() for m in QUOTED_RE.finditer(s or '') if m.group(1).strip()]

def shingle_hashes(text, k=12, keep=256):
    w = re.findall(r'[a-z0-9]+', norm_text(text))
    hs = sorted({sha256_bytes(' '.join(w[i:i + k]).encode()) for i in range(max(0, len(w) - k + 1))})
    return hs[:keep]  # deterministic min-hash style subset; texts themselves are never handed to S2

# ----------------------------------------------------------------------------------------- provenance
def runtime_identity():
    def rd(p):
        try:
            return Path(p).read_text().strip()
        except Exception:
            return None
    return {'boot_id': rd('/proc/sys/kernel/random/boot_id'), 'hostname': socket.gethostname(), 'pid': os.getpid(),
            'python': platform.python_version(), 'platform': platform.platform(), 'utc': utc(),
            'uptime_s': (rd('/proc/uptime') or '0 0').split()[0]}

def provenance(torch_mod=None):
    """GPU_REAL only when real torch reports a real A100 and no simulation stack is on the path."""
    t = torch_mod
    if t is None:
        import torch as t
    ver = str(getattr(t, '__version__', '?'))
    name = ''
    try:
        name = t.cuda.get_device_name(0) if t.cuda.is_available() else ''
    except Exception:
        name = ''
    sim = ver.startswith('sim') or 'SIMULATED' in name or os.environ.get('AKBASCORE_SIM') == '1'
    real = (not sim) and 'A100' in name
    return {'mode': 'GPU_REAL' if real else 'SIMULATION', 'torch': ver, 'gpu': name}

# ----------------------------------------------------------------------------------------- event log
class EventLog:
    """UTC-stamped JSONL event log + console mirror + heartbeat (60 s)."""
    def __init__(self, path, heartbeat_s=60):
        self.path = Path(path); self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock(); self.last = 'start'; self._stop = threading.Event()
        self.hb = threading.Thread(target=self._beat, args=(heartbeat_s,), daemon=True); self.hb.start()
        self.t0 = time.time()

    def ev(self, kind, msg='', /, **data):
        rec = {'utc': utc(), 'kind': kind, 'msg': msg}
        if data:
            rec['data'] = data
        line = json.dumps(rec, ensure_ascii=False, default=str)
        with self.lock:
            with self.path.open('a', encoding='utf-8') as f:
                f.write(line + '\n')
            self.last = f'{kind} {msg}'[:160]
        print(f"{rec['utc']} {kind:<22} {msg} {json.dumps(data, ensure_ascii=False, default=str)[:600] if data else ''}", flush=True)
        return rec

    def _beat(self, s):
        while not self._stop.wait(s):
            try:
                print(f'  [heartbeat {utc()}] +{(time.time() - self.t0) / 60:.1f} min · last: {self.last}', flush=True)
            except Exception:
                pass

    def close(self):
        self._stop.set()

# ----------------------------------------------------------------------------------------- persistent store with SHA manifest
class Store:
    """Every artefact goes through put_*; manifest records sha256/bytes/utc/provenance.
    Optional mirror (Google Drive) receives a verified copy; restore() only accepts SHA-matching files."""
    def __init__(self, local_dir, mirror_dir=None, provenance_mode='SIMULATION', log=None):
        self.root = Path(local_dir); self.root.mkdir(parents=True, exist_ok=True)
        self.mirror = Path(mirror_dir) if mirror_dir else None
        if self.mirror:
            self.mirror.mkdir(parents=True, exist_ok=True)
        self.mode = provenance_mode; self.log = log
        self.mpath = self.root / 'MANIFEST.json'
        self.manifest = json.loads(self.mpath.read_text()) if self.mpath.exists() else {'files': {}}
        if self.mirror and (self.mirror / 'MANIFEST.json').exists() and not self.manifest['files']:
            self.manifest = json.loads((self.mirror / 'MANIFEST.json').read_text())

    def _record(self, rel, path, kind):
        s = sha256_file(path); n = path.stat().st_size
        self.manifest['files'][rel] = {'sha256': s, 'bytes': n, 'utc': utc(), 'provenance': self.mode, 'kind': kind}
        atomic_write(self.mpath, jdump(self.manifest))
        if self.mirror:
            dst = self.mirror / rel; dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dst)
            if sha256_file(dst) != s:
                raise StageError('MIRROR_COPY_SHA_MISMATCH ' + rel)
            atomic_write(self.mirror / 'MANIFEST.json', jdump(self.manifest))
        return s

    def put_bytes(self, rel, data, kind='data'):
        p = self.root / rel; atomic_write(p, data); return self._record(rel, p, kind)

    def put_json(self, rel, obj, kind='json'):
        return self.put_bytes(rel, jdump(obj).encode('utf-8'), kind)

    def put_text(self, rel, text, kind='text'):
        return self.put_bytes(rel, text.encode('utf-8'), kind)

    def put_file(self, rel, src, kind='file'):
        p = self.root / rel; p.parent.mkdir(parents=True, exist_ok=True)
        if Path(src).resolve() != p.resolve():
            if p.exists() or p.is_symlink():
                p.unlink()
            try:
                os.link(src, p)          # hard link: no extra disk for multi-GB cartridges; SHA is re-verified on every has()/restore()
            except OSError:
                shutil.copyfile(src, p)
        return self._record(rel, p, kind)

    def has(self, rel):
        e = self.manifest['files'].get(rel); p = self.root / rel
        return bool(e) and p.exists() and sha256_file(p) == e['sha256']

    def get_json(self, rel):
        if not self.has(rel):
            raise StageError('MISSING_OR_SHA_MISMATCH ' + rel)
        return json.loads((self.root / rel).read_text(encoding='utf-8'))

    def restore(self, rel):
        """Copy rel from the mirror into local if (and only if) its SHA matches the manifest."""
        e = self.manifest['files'].get(rel)
        if not e:
            return False
        if self.has(rel):
            return True
        if not self.mirror:
            return False
        src = self.mirror / rel
        if not src.exists() or sha256_file(src) != e['sha256']:
            return False
        dst = self.root / rel; dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, dst)
        return sha256_file(dst) == e['sha256']

# ----------------------------------------------------------------------------------------- pre-registration & seal
def load_prereg(src_dir=HERE):
    p = Path(src_dir) / 'TEST719_prereg.json'; raw = p.read_bytes()
    return json.loads(raw), sha256_bytes(raw)

def load_seal(src_dir=HERE):
    p = Path(src_dir) / 'SEAL.json'
    if not p.exists():
        return None
    return json.loads(p.read_text())

def check_seal(prereg_sha, bank_path, mode, log):
    """REAL runs require SEAL.json listing the prereg and bank SHA committed before the run."""
    seal = load_seal(); bank_sha = sha256_file(bank_path) if bank_path and Path(bank_path).exists() else None
    ok = bool(seal) and seal.get('prereg_sha256') == prereg_sha and seal.get('bank_sha256') == bank_sha
    log.ev('SEAL', 'checked', sealed=ok, prereg_sha256=prereg_sha, bank_sha256=bank_sha, seal=seal)
    if mode == 'GPU_REAL' and not ok:
        raise StageError('UNSEALED: GPU_REAL runs require SEAL.json matching prereg and bank SHA-256')
    return {'sealed': ok, 'prereg_sha256': prereg_sha, 'bank_sha256': bank_sha, 'seal': seal}

# ----------------------------------------------------------------------------------------- model revision pin (environment-level, no engine change)
def pin_model_revision(log, mode):
    """Download the pinned commit, point refs/main at it, then force offline mode so the unchanged
    716 from_pretrained(MODEL_ID) resolves exactly that snapshot. Must run before transformers import."""
    if mode != 'GPU_REAL':
        log.ev('MODEL_PIN', 'skipped in SIMULATION'); return {'pinned': False, 'reason': 'simulation'}
    code = ('import huggingface_hub as h,sys;p=h.snapshot_download(%r,revision=%r);print(p)' % (MODEL_ID, MODEL_COMMIT))
    t = time.time(); log.ev('MODEL_DOWNLOAD', 'snapshot_download of the pinned commit - the Hugging Face progress bars follow (stderr is shown live)', commit=MODEL_COMMIT)
    out = subprocess.run([sys.executable, '-c', code], stdout=subprocess.PIPE, stderr=None, text=True)   # stderr = live download progress
    if out.returncode != 0:
        raise StageError('MODEL_DOWNLOAD_FAILED (exit %s) - see the download output above' % out.returncode)
    snap = Path(out.stdout.strip().splitlines()[-1])
    if snap.name != MODEL_COMMIT:
        raise StageError('MODEL_SNAPSHOT_COMMIT_MISMATCH ' + snap.name)
    refs = snap.parent.parent / 'refs'; refs.mkdir(exist_ok=True); (refs / 'main').write_text(MODEL_COMMIT)
    os.environ['HF_HUB_OFFLINE'] = '1'; os.environ['TRANSFORMERS_OFFLINE'] = '1'
    shards = sorted(x.name for x in snap.glob('*.safetensors'))
    etags = {}
    for x in snap.glob('*.safetensors'):
        try:
            etags[x.name] = Path(os.path.realpath(x)).name  # blob file name == LFS sha256 etag
        except Exception:
            etags[x.name] = None
    rec = {'pinned': True, 'commit': MODEL_COMMIT, 'snapshot': str(snap), 'shards': len(shards), 'shard_blobs': etags,
           'seconds': round(time.time() - t, 1)}
    log.ev('MODEL_PIN', 'refs/main -> pinned commit, offline mode', **{k: v for k, v in rec.items() if k != 'shard_blobs'})
    return rec

# ----------------------------------------------------------------------------------------- stdout tee (engine lines are only observed)
class Tee(io.TextIOBase):
    def __init__(self, stream, keep=200000):
        self.stream = stream; self.lines = []; self.keep = keep; self.buf = ''
    def write(self, s):
        self.stream.write(s); self.buf += s
        while '\n' in self.buf:
            line, self.buf = self.buf.split('\n', 1); self.lines.append(line)
            if len(self.lines) > self.keep:
                del self.lines[:len(self.lines) - self.keep]
        return len(s)
    def flush(self):
        self.stream.flush()

# ----------------------------------------------------------------------------------------- engine wrapper
MODEL_ONLY_PREFIXES = [  # 716 setup statements needed to load the model without PDF / forge (S2)
    "ck('709_GIT_BLOB_LOCK'", 'tok = AutoTokenizer.from_pretrained(', 'PREFIX = ', 'PIDS = tok(PREFIX', 'P = len(PIDS)',
    'quant = BitsAndBytesConfig(', "ck('CUDA_A100_80GB'", 'model = AutoModelForCausalLM.from_pretrained(',
    'for p in model.parameters():', 'cfg = model.config', 'NL = len(model.model.layers)', 'H = int(cfg.hidden_size)',
    'QH = int(cfg.num_attention_heads)', 'KVH = int(cfg.num_key_value_heads)', 'HD = int(getattr(cfg',
    "ck('MODEL_ARCH'", "ck('FROZEN'", 'before = sentinel()', "R['weight_sentinel_before'] = before"]

def read_716(log):
    local = Path('/content/716.py')
    if local.is_file():
        src = local.read_bytes(); origin = str(local)
    else:
        import urllib.request
        with urllib.request.urlopen(urllib.request.Request(URL716, headers={'User-Agent': 'AKBASCORE-TEST719'}), timeout=180) as f:
            src = f.read(250000)
        origin = URL716
    b = git_blob(src)
    if b != LOCK716:
        raise StageError('TEST716_SOURCE_DRIFT ' + b)
    log.ev('LOCK', '716.py git blob verified', blob=b, origin=origin)
    return src

def split_716(src):
    tree = ast.parse(src.decode()); setup = next(n for n in tree.body if isinstance(n, ast.Try))
    stop = next(i for i, n in enumerate(setup.body) if isinstance(n, ast.Delete) and any(isinstance(t, ast.Name) and t.id == 'pdf' for t in n.targets))
    pre = ast.Module(body=[n for n in tree.body if not isinstance(n, ast.Try)], type_ignores=[])
    return pre, setup, stop

def select_model_only(setup, stop):
    chosen = []
    for n in setup.body[:stop + 1]:
        u = ast.unparse(n)
        hits = [p for p in MODEL_ONLY_PREFIXES if u.startswith(p)]
        if hits:
            chosen.append((hits[0], n))
    got = [h for h, _ in chosen]
    if sorted(got) != sorted(MODEL_ONLY_PREFIXES) or len(got) != len(set(got)):
        raise StageError('716_MODEL_ONLY_SELECTION_DRIFT ' + repr(sorted(set(MODEL_ONLY_PREFIXES) ^ set(got))))
    return [n for _, n in chosen]

class Engine:
    """Thin observer/driver around the unchanged engine namespace E."""
    def __init__(self, log, mode):
        self.log = log; self.mode = mode; self.E = {'__name__': 'akbascore_engine'}
        self.tee = None

    # ---- boot
    def _exec(self, nodes, name):
        exec(compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])), name, 'exec'), self.E)

    def boot(self, model_only=False):
        src = read_716(self.log); pre, setup, stop = split_716(src)
        self.tee = Tee(sys.stdout); sys.stdout = self.tee
        t = time.time()
        self._exec(pre.body, '716.py:preamble')
        hook = globals().get('SIM_AFTER_PREAMBLE')
        if hook is not None:
            if self.mode == 'GPU_REAL':
                raise StageError('SIM hook present in GPU_REAL mode')
            hook(self.E)
        nodes = select_model_only(setup, stop) if model_only else setup.body[:stop + 1]
        self._exec(nodes, '716.py:setup' + (':model_only' if model_only else ''))
        E = self.E
        self.torch = E['torch']; self.model = E['model']; self.tok = E['tok']
        self.kv_row_bytes = E['NL'] * E['KVH'] * E['HD'] * 2 * 2
        self.vocab = int(getattr(self.model.config, 'vocab_size', 0) or 152064)
        info = {'seconds': round(time.time() - t, 1), 'model_only': model_only, 'P': E['P'], 'arch': [E['NL'], E['H'], E['QH'], E['KVH'], E['HD']],
                'kv_row_bytes': self.kv_row_bytes, 'sentinel_before': E['before'],
                'commit_hash': getattr(self.model.config, '_commit_hash', None),
                'books': [dict(b) for b in E['R'].get('books', [])]}
        if self.mode == 'GPU_REAL' and info['commit_hash'] not in (None, MODEL_COMMIT):
            raise StageError('MODEL_COMMIT_MISMATCH ' + str(info['commit_hash']))
        self.install_memory_recovery()
        self.log.ev('ENGINE_BOOT', '716 setup executed unchanged' + (' (model-only statements)' if model_only else ''), **{k: v for k, v in info.items() if k != 'books'})
        return info

    # ---- memory management (no change to the computation): free unused cached GPU memory before the engine's own check
    def free_cached(self):
        gc.collect()
        try:
            self.torch.cuda.synchronize(); self.torch.cuda.empty_cache()
        except Exception:
            pass

    def install_memory_recovery(self):
        """709 ensure_room() compares torch.cuda.mem_get_info() free memory with the 9 GiB reserve. Memory that PyTorch's caching
        allocator holds but no tensor uses (freed blocks of the growing K/V cache) counts as 'used' there. The wrapper releases those
        unused cached blocks (gc + empty_cache) when the free memory is short, then calls the ORIGINAL ensure_room unchanged: the
        reserve check itself and every computation stay exactly as in 709."""
        E = self.E; orig = E['ensure_room']; torch = self.torch; self.recoveries = []
        if getattr(orig, '_t719_recovery', False):
            return
        def ensure_room(extra_tokens=0):
            free, _ = torch.cuda.mem_get_info()
            need = E['GPU_RESERVE_GIB'] * 2 ** 30 + extra_tokens * E['NL'] * E['KVH'] * E['HD'] * 2 * 2
            if free < need:
                self.free_cached(); f2, _ = torch.cuda.mem_get_info()
                if len(self.recoveries) < 2000:
                    self.recoveries.append({'utc': utc(), 'free_before_gib': round(free / GIB, 3), 'free_after_gib': round(f2 / GIB, 3), 'need_gib': round(need / GIB, 3)})
            return orig(extra_tokens)
        ensure_room._t719_recovery = True; ensure_room.__wrapped__ = orig
        E['ensure_room'] = ensure_room

    def set_memory_profile(self, chunk, reserve_gib):
        """engine run-time parameters (709 reads them from the environment): CUT3 chunk length and GPU reserve"""
        self.E['CHUNK'] = int(chunk); self.E['GPU_RESERVE_GIB'] = float(reserve_gib)

    # ---- memory accounting
    def mem(self):
        t = self.torch; t.cuda.synchronize(); free, total = t.cuda.mem_get_info()
        return {'free': int(free), 'total': int(total), 'allocated': int(t.cuda.memory_allocated()), 'peak': int(t.cuda.max_memory_allocated()), 'utc': utc()}

    def reset_peak(self):
        self.torch.cuda.reset_peak_memory_stats()

    @staticmethod
    def kv_bytes(memory):
        return 0 if memory is None else int(sum(k.numel() * k.element_size() + v.numel() * v.element_size() for k, v in memory))

    @staticmethod
    def rows(memory):
        return 0 if memory is None else int(memory[0][0].shape[-2])

    def free(self):
        self.E['free_gpu']()

    # ---- cartridges
    def cart_path(self, bid):
        return Path(self.E['CART']) / (bid + '.pt')

    def book(self, bid):
        return next((b for b in self.E['R']['books'] if b['id'] == bid), None)

    def forge_register(self, bid, body_text, meta=None):
        """Replicates the TEST716 forge lines exactly (forge_stream -> torch.save -> .sha256 -> R['books'])."""
        E = self.E; tok = E['tok']; torch = E['torch']; CART = Path(E['CART'])
        body = tok(body_text, add_special_tokens=False).input_ids; path = CART / (bid + '.pt')
        reuse = (path.exists() and (CART / (bid + '.sha256')).exists() and E['sha'](path.read_bytes()) == (CART / (bid + '.sha256')).read_text().strip()
                 and torch.load(path, map_location='cpu', weights_only=True).get('body_tokens') == len(body))
        t = time.time()
        if reuse:
            self.log.ev('REUSE_SHA_VERIFIED', bid)
        else:
            cp, secs = E['forge_stream'](body, bid); torch.save(cp, path); (CART / (bid + '.sha256')).write_text(E['sha'](path.read_bytes())); del cp; E['free_gpu']()
        rec = {'id': bid, 'cartridge_sha256': E['sha'](path.read_bytes()), 'body_tokens': len(body), 'bytes': path.stat().st_size,
               'body_text_sha256': sha256_bytes(body_text.encode('utf-8')), 'reused': bool(reuse), 'seconds': round(time.time() - t, 2)}
        rec.update(meta or {})
        books = E['R']['books']; old = self.book(bid)
        if old is not None:
            books.remove(old)
        books.append(rec)
        self.log.ev('FORGE_REGISTERED', bid, **{k: v for k, v in rec.items() if k != 'note'})
        return rec

    def register_existing(self, rec):
        books = self.E['R'].setdefault('books', []); old = self.book(rec['id'])
        if old is not None:
            books.remove(old)
        books.append(dict(rec))

    def mount(self, bid):
        """cart_load (SHA-checked) -> list(initialize(cp)) — the TEST718/demo pattern."""
        E = self.E; m0 = self.mem(); t = time.time()
        cp, times = E['cart_load'](bid); t1 = time.time()
        memory = list(E['initialize'](cp)); n = int(cp['n']); del cp; E['free_gpu']()
        times.update({'rebuild_ms': round((time.time() - t1) * 1000, 1), 'end_to_end_ms': round((time.time() - t) * 1000, 1)})
        m1 = self.mem(); rows = self.rows(memory)
        if rows != n:
            raise StageError(f'MOUNT_ROWS {bid} {rows}!={n}')
        rec = {'bid': bid, 'rows': rows, 'kv_bytes': self.kv_bytes(memory), 'alloc_before': m0['allocated'], 'alloc_after': m1['allocated'], 'timing': times, 'utc': utc()}
        self.log.ev('MOUNT', bid, rows=rows, kv_gib=round(rec['kv_bytes'] / GIB, 3), alloc_gib=round(m1['allocated'] / GIB, 3), **times)
        return memory, rec

    def append(self, memory, bid):
        E = self.E; oldn = self.rows(memory); t = time.time(); self.reset_peak()
        cp, times = E['cart_load'](bid); q = int(cp['n']) - int(E['P'])
        mark = len(self.tee.lines) if self.tee else 0
        memory = E['append'](memory, cp); del cp; E['free_gpu']()
        lines = self.tee.lines[mark:] if self.tee else []
        want = 'PASS APPEND_ALL_80_LAYERS_EXACT_SHA256'
        passed = [l for l in lines if want in l]
        rows = self.rows(memory); m = self.mem()
        ok = len(passed) == 1 and rows == oldn + q and f"'new_tokens': {oldn + q}" in passed[0] and len(memory) == E['NL']
        rec = {'bid': bid, 'old_rows': oldn, 'added_rows': q, 'rows': rows, 'pass_line': passed[0] if passed else None, 'verified': ok,
               'seconds': round(time.time() - t, 2), 'append_peak': m['peak'], 'alloc_after': m['allocated'], 'kv_bytes': self.kv_bytes(memory), 'timing': times, 'utc': utc()}
        self.log.ev('APPEND', bid, verified=ok, old_rows=oldn, rows=rows, seconds=rec['seconds'], peak_gib=round(m['peak'] / GIB, 3))
        if not ok:
            raise StageError('APPEND_NOT_VERIFIED ' + bid)
        return memory, rec

    def release(self, memory_holder):
        """memory_holder: dict with key 'm'. Drops the only reference and checks allocated returns to baseline."""
        memory_holder['m'] = None; gc.collect(); self.free(); return self.mem()

    def seals(self, memory):
        t = time.time(); s = self.E['full_kv_seal'](memory)
        return {'layers': [[k, v] for k, v in s], 'seconds': round(time.time() - t, 2)}

    # ---- answering (TEST718 run_answer pattern + exact generated-token capture via tokenizer instance wrapper)
    def suffix_tokens(self, prompt):
        s = '\nQUESTION:\n' + prompt + '\n\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n'
        return len(self.tok(s, add_special_tokens=False).input_ids)

    def predict_answer_delta(self, memory, prompt_tokens, ceiling):
        kv = self.kv_bytes(memory)
        return int(1.1 * kv + prompt_tokens * self.vocab * 4 + ceiling * self.kv_row_bytes)

    def pregate(self, memory, prompt_tokens, ceiling, reserve_gib):
        """advisory estimate only (never stops a generation): unused cached memory is released first"""
        self.free_cached(); m = self.mem(); kv = self.kv_bytes(memory)
        need = int(1.1 * kv + ceiling * self.kv_row_bytes + prompt_tokens * self.vocab * 4 + GIB)
        ok = m['free'] - reserve_gib * GIB >= need
        return ok, {'free': m['free'], 'need': need, 'reserve_gib': reserve_gib, 'kv_bytes': kv}

    def answer(self, memory, prompt, ceiling, reserve_gib=9.0, label=''):
        E = self.E; tok = self.tok; ptoks = self.suffix_tokens(prompt)
        ok, pre = self.pregate(memory, ptoks, ceiling, reserve_gib)
        if not ok:
            self.log.ev('PREGATE_ADVISORY', label + ' - estimate above free memory; generating anyway (a real CUDA error would be recorded)', **pre)
        m0 = self.mem(); self.reset_peak(); captured = []; steps = []
        had = 'decode' in tok.__dict__; orig = tok.decode
        def dec(ids, *a, **k):
            captured.append([int(x) for x in ids]); return orig(ids, *a, **k)
        # Observation only (no effect on the computation): the greedy token chosen at every forward pass, read from the
        # lm_head output exactly as 709 answer() does (argmax of the last position). The last observed token is the reason
        # the unchanged loop stopped.
        def lm_hook(mod, args, out):
            z = out[0] if isinstance(out, (tuple, list)) else out
            steps.append(int(z[0, -1, :].argmax(-1).item()))
        hk = self.model.lm_head.register_forward_hook(lm_hook)
        stop_ids = {int(tok.eos_token_id), int(tok.convert_tokens_to_ids('<|im_end|>'))}
        prev = E['MAX_NEW']; E['MAX_NEW'] = int(ceiling); t = time.time()
        try:
            tok.decode = dec
            with self.torch.no_grad():
                text = E['answer'](memory, prompt)
        finally:
            hk.remove()
            if had:
                tok.decode = orig
            else:
                del tok.decode
            E['MAX_NEW'] = prev
        secs = time.time() - t; m1 = self.mem(); E['free_gpu']()
        gen = captured[-1] if captured else None; n_gen = len(gen) if gen is not None else None
        retok = len(tok(text, add_special_tokens=False).input_ids)
        # Finish reason, cross-checked three ways: forward calls == 1 + generated tokens, the generated ids equal the
        # observed greedy tokens, and the token after the last generated one is a stop token.
        last = steps[-1] if steps else None
        consistent = gen is not None and len(steps) == n_gen + 1 and steps[:n_gen] == gen
        if gen is not None and n_gen >= ceiling:
            finish = 'CEILING'
        elif consistent and last in stop_ids:
            finish = 'EOS'
        else:
            finish = 'UNVERIFIED'
        complete = finish == 'EOS'
        rec = {'text': text, 'sha256': sha256_bytes(text.encode('utf-8')), 'n_generated': n_gen, 'n_retokenized': retok, 'ceiling': int(ceiling),
               'finish_reason': finish, 'finish_evidence': {'forward_calls': len(steps), 'generated_ids_equal_observed_greedy_tokens': consistent,
                                                            'stop_token_observed': last if last in stop_ids else None, 'last_observed_token': last,
                                                            'last_observed_token_text': orig([last], skip_special_tokens=False) if last is not None else None},
               'complete': bool(complete), 'status': 'COMPLETE' if complete else ('INCOMPLETE' if finish == 'CEILING' else 'UNVERIFIED_FINISH'),
               'prompt_suffix_tokens': ptoks, 'memory_rows': self.rows(memory),
               'kv_bytes': self.kv_bytes(memory), 'alloc_before': m0['allocated'], 'peak': m1['peak'], 'free_before': m0['free'], 'total': m0['total'],
               'peak_delta': m1['peak'] - m0['allocated'], 'predicted_delta': self.predict_answer_delta(memory, ptoks, min(ceiling, n_gen or ceiling)),
               'seconds': round(secs, 2), 'tok_per_s': round((n_gen or 0) / secs, 3) if secs > 0 else None, 'utc': utc()}
        return rec

    # ---- X-ray (read-only, CUDA tensors only in GPU_REAL)
    def xray(self, memory, label):
        torch = self.torch; import numpy as np
        K = []; V = []; t = time.time(); dev = None
        for k, v in memory:
            if self.mode == 'GPU_REAL' and not (getattr(k, 'is_cuda', False) and getattr(v, 'is_cuda', False)):
                raise StageError('XRAY_REQUIRES_CUDA_TENSORS ' + label)
            dev = str(k.device)
            K.append(k.float().norm(dim=-1).mean(dim=1)[0].cpu().numpy().astype(np.float32))
            V.append(v.float().norm(dim=-1).mean(dim=1)[0].cpu().numpy().astype(np.float32))
        K = np.stack(K); V = np.stack(V)
        meta = {'label': label, 'rows': int(K.shape[1]), 'layers': int(K.shape[0]), 'device': dev, 'provenance': self.mode,
                'finite': bool(np.isfinite(K).all() and np.isfinite(V).all()), 'seconds': round(time.time() - t, 2), 'utc': utc(),
                'definition': 'per layer/row: L2 norm over head_dim in FP32, mean over KV heads'}
        return K, V, meta

    # ---- explicit memory audit (S2 independence)
    @staticmethod
    def _storage_key(t):
        st = t.untyped_storage(); return (int(st.data_ptr()), int(st.nbytes()))

    def storage_bytes(self, tensors):
        """Bytes of the UNIQUE storages behind the given tensors (views / shared storage counted once)."""
        seen = {}
        for t in tensors:
            k = self._storage_key(t); seen[k[0]] = max(seen.get(k[0], 0), k[1])
        return int(sum(seen.values())), len(seen)

    def cuda_storage_ptrs(self):
        """Pointers of all gc-visible non-model CUDA storages (used as the model-only baseline of the census)."""
        torch = self.torch; model_ptrs = {self._storage_key(p)[0] for p in list(self.model.parameters()) + list(getattr(self.model, 'buffers', lambda: iter(()))())}
        out = set()
        for o in gc.get_objects():
            try:
                if isinstance(o, torch.Tensor) and getattr(o, 'is_cuda', False):
                    k = self._storage_key(o)[0]
                    if k not in model_ptrs:
                        out.add(k)
            except Exception:
                continue
        return out

    def cuda_tensor_census(self, exclude_model=True, known=(), baseline_ptrs=None):
        """Best-effort census of CUDA tensors reachable from Python (gc), counted by UNIQUE storage. Model parameters and
        buffers are excluded by storage pointer. Tensors held only inside C/C++ objects are invisible to gc, so this census
        is supporting evidence; the allocator counter (torch.cuda.memory_allocated) is the primary measurement."""
        torch = self.torch; model_ptrs = set()
        if exclude_model:
            for p in list(self.model.parameters()) + list(getattr(self.model, 'buffers', lambda: iter(()))()):
                try:
                    model_ptrs.add(self._storage_key(p)[0])
                except Exception:
                    pass
        known_ptrs = {self._storage_key(t)[0] for t in known}
        uniq = {}; n = 0
        for o in gc.get_objects():
            try:
                if isinstance(o, torch.Tensor) and getattr(o, 'is_cuda', False):
                    ptr, nb = self._storage_key(o)
                    if ptr in model_ptrs:
                        continue
                    n += 1; uniq[ptr] = max(uniq.get(ptr, 0), nb)
            except Exception:
                continue
        total = int(sum(uniq.values())); in_known = int(sum(v for k, v in uniq.items() if k in known_ptrs))
        new_foreign = None if baseline_ptrs is None else int(sum(v for k, v in uniq.items() if k not in known_ptrs and k not in baseline_ptrs))
        return {'tensor_objects': n, 'unique_storages': len(uniq), 'unique_storage_bytes': total, 'bytes_in_known_memory': in_known,
                'other_unique_storage_bytes': total - in_known, 'new_storage_bytes_not_in_memory_since_baseline': new_foreign}

def is_memory_error(e):
    t = f'{type(e).__name__}: {e}'
    return 'GPU_SAFETY_STOP' in t or 'OutOfMemoryError' in t or 'CUDA out of memory' in t or 'CUBLAS_STATUS_ALLOC_FAILED' in t

# memory profiles tried in order after a GPU memory failure: (CUT3 chunk tokens, GPU reserve GiB). The first is the TEST716 default.
MEMORY_LADDER = [(256, 9.0), (128, 9.0), (64, 6.0)]

def nvidia_smi():
    try:
        out = subprocess.run(['nvidia-smi', '--query-gpu=name,uuid,memory.total,memory.used,driver_version', '--format=csv,noheader'], capture_output=True, text=True, timeout=20)
        return out.stdout.strip()
    except Exception as e:
        return 'unavailable: ' + type(e).__name__

def gpu_processes():
    """Compute processes and used memory on the GPU, read with nvidia-smi (no CUDA context is created)."""
    out = {'apps': None, 'memory_used_mib': None}
    try:
        a = subprocess.run(['nvidia-smi', '--query-compute-apps=pid,used_memory', '--format=csv,noheader,nounits'], capture_output=True, text=True, timeout=20)
        out['apps'] = [l.strip() for l in a.stdout.splitlines() if l.strip()]
        m = subprocess.run(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits'], capture_output=True, text=True, timeout=20)
        out['memory_used_mib'] = int(m.stdout.strip().splitlines()[0])
    except Exception as e:
        out['error'] = type(e).__name__
    return out

# ----------------------------------------------------------------------------------------- independence audit (filesystem)
SCAN_SKIP = ('/proc', '/sys', '/dev', '/run', '/snap', '/usr', '/lib', '/lib64', '/bin', '/sbin', '/etc', '/var/lib', '/opt/conda/pkgs')

def independence_scan(roots, forbidden_sha, forbidden_sizes, forbidden_shingles, skip_dirs=(), text_max=50 * 2 ** 20):
    """Hashes every .pt file and every file whose size equals a forbidden cartridge size; scans text-like files
    for forbidden 12-word shingle hashes. Returns findings (empty list == pass)."""
    findings = []; scanned = {'pt': 0, 'size_match': 0, 'text': 0}
    fsizes = set(int(x) for x in forbidden_sizes); fsh = set(forbidden_shingles); fsha = dict(forbidden_sha)
    skip = tuple(str(Path(s)) for s in skip_dirs)
    for root in roots:
        root = Path(root)
        if not root.exists():
            continue
        for dp, dns, fns in os.walk(root, followlinks=False):
            if dp.startswith(SCAN_SKIP) or (skip and dp.startswith(skip)):
                dns[:] = []; continue
            # prune skipped / quarantined sub-directories BEFORE os.walk lists them (they are never opened)
            dns[:] = [d for d in dns if not (str(Path(dp) / d).startswith(SCAN_SKIP) or (skip and str(Path(dp) / d).startswith(skip)))]
            for fn in fns:
                p = Path(dp) / fn
                try:
                    if p.is_symlink() or not p.is_file():
                        continue
                    sz = p.stat().st_size
                except Exception:
                    continue
                if fn.endswith('.pt') or sz in fsizes:
                    scanned['pt' if fn.endswith('.pt') else 'size_match'] += 1
                    s = sha256_file(p)
                    if s in fsha:
                        findings.append({'path': str(p), 'kind': 'forbidden_file_sha', 'label': fsha[s]})
                if sz <= text_max and fn.endswith(('.json', '.jsonl', '.txt', '.md', '.log', '.csv', '.py', '.html')) and fsh:
                    scanned['text'] += 1
                    try:
                        hs = set(shingle_hashes(p.read_text(encoding='utf-8', errors='ignore'), keep=10 ** 9))
                    except Exception:
                        continue
                    hit = hs & fsh
                    if hit:
                        findings.append({'path': str(p), 'kind': 'forbidden_text_shingles', 'hits': len(hit)})
    return findings, scanned

# ----------------------------------------------------------------------------------------- stage timer / cost
class Stages:
    def __init__(self, store, log, session):
        self.store = store; self.log = log; self.session = session; self.rec = []
        self.t0 = time.time()

    def run(self, name, fn, *a, **k):
        st = utc(); t = time.time(); self.log.ev('STAGE_START', name); status = 'ERROR'
        try:
            out = fn(*a, **k); status = 'DONE'; return out
        except GateStop:
            status = 'STOPPED_AT_GATE'; raise
        except Exception:
            status = 'ERROR'; raise
        finally:
            r = {'stage': name, 'start_utc': st, 'end_utc': utc(), 'seconds': round(time.time() - t, 2), 'status': status}
            self.rec.append(r); self.log.ev('STAGE_END', name, seconds=r['seconds'], status=status)
            self.store.put_json(f'{self.session}/stage_times.json', {'session': self.session, 'stages': self.rec, 'wall_seconds': round(time.time() - self.t0, 2)}, 'timing')
''','7ef7667512a06206f40da87def79b2dd1e18ed69900c04f9bc18fcf6cf5abf55')

STATE=dict(memory=None,mount=None,qa=[],controls=[],ops=[],weight_checks=[],disk_checks=[],verification=None,audit=None)
SESSION_INFO=dict(session_id=SESSION_ID,started_utc=utc_now(),started_local=local_now(),python=platform.python_version(),platform=platform.platform())
slog("SESSION_START",APP_SHORT,session=SESSION_ID,version_note=VERSION_NOTE,session_dir=str(SESSION_DIR))
# ===== END OF PART 1/3 =====
# ===== PART 2/3 — paste directly after PART 1 in the same cell =====
# =====================================================================================================================
# PART 2 / 3 — Physical Pair Memories, C11, Isolated Question Process, Integrity and Research Figures
# Process 1 and process 2 call the TEST709 engine functions through the unchanged TEST716 set-up (cart_load, initialize,
# append, forge_stream, full_kv_seal, answer, sentinel). Nothing here changes CUT3, RoPE, the cartridge format, the K/V layout,
# the SHA-256 guards or the GPU reserve. The only value set from outside is the generation ceiling MAX_NEW per call.
# All measurements are read-only and computed from this session's records and from the original PDF downloaded now.
# =====================================================================================================================

if str(PROGRAM_DIR) not in sys.path:sys.path.insert(0,str(PROGRAM_DIR))
import TEST719_common as C
C=importlib.reload(C)
class OpError(RuntimeError):pass
class PhaseFailed(RuntimeError):pass

# ---------------------------------------------------------------------------------------------------------------------
# step [1]: engine sources (git blob locks) and historical reference
# ---------------------------------------------------------------------------------------------------------------------
def load_engine_sources():
    r716=fetch_locked("716.py");fetch_locked("709.py")
    if "PDF_SHA='"+PDF_SHA256+"'" not in r716.decode("utf-8"):raise RuntimeError("TEST716 STRUCTURE: PDF lock differs from this program")
    if os.path.isdir("/content"):Path("/content/716.py").write_bytes(r716)   # the verified, identical 716.py that the processes execute
    slog("ENGINE_SOURCE","716.py and 709.py verified",blob_716=SOURCES["716.py"]["git_blob"],blob_709=SOURCES["709.py"]["git_blob"])
def load_historical():
    out={}
    for n in HISTORICAL:
        r=fetch_locked(n);(HIST_DIR/("HISTORICAL_"+n)).write_bytes(r);out[n]=LOCKS[n]
    (HIST_DIR/"README_HISTORICAL.txt").write_text(
        "These files are PUBLISHED RECORDS OF EARLIER RUNS (TEST716, TEST717, TEST718), verified against their git blob identifiers.\n"
        "They are NOT results of this session. Live results of this session are in the session files and in records_process1/2.\n"
        +"".join(f"{n}: git blob {LOCKS[n]}\n" for n in HISTORICAL),encoding="utf-8")
    slog("HISTORICAL_LOADED","published TEST716/717/718 logs verified (reference only, not this session)",blobs=out);return out
def sources_step():
    load_engine_sources();h=load_historical()
    fetch_locked("LICENSE");(SESSION_DIR/"LICENSE.txt").write_bytes((EVIDENCE_DIR/"LICENSE").read_bytes())
    need={"TEST719_common.py","TEST719_demo_build.py","TEST719_demo_ask.py","TEST719_demo_questions.json","TEST719_demo_build_config.json"}
    if set(PROGRAM)!=need:raise RuntimeError(f"PROGRAM FILES: expected {sorted(need)}, written {sorted(PROGRAM)}")
    for k,v in PROGRAM.items():_OUT.write(f"  program  {k:<34} {v['bytes']:>8,} bytes · SHA-256 {v['sha256'][:16]}…\n")
    _OUT.flush();dump_json(SESSION_DIR/"PROGRAM_FILES.json",PROGRAM)
    return dict(sources={k:v["git_blob"] for k,v in SOURCES.items()},historical=list(h),program={k:v["sha256"] for k,v in PROGRAM.items()})

# ---------------------------------------------------------------------------------------------------------------------
# step [4]: the five fixed questions — mandatory source check on the real PDF, then the seal (no model is loaded yet)
# ---------------------------------------------------------------------------------------------------------------------
QFILE=PROGRAM_DIR/"TEST719_demo_questions.json";CFGFILE=PROGRAM_DIR/"TEST719_demo_build_config.json"
SEAL_FILE=RUNS/"SEAL.json";SRC_CHECK_FILE=RUNS/"pdf_source_check.json";PHASES_FILE=RUNS/"PHASES.json"
def norm(s):
    s=unicodedata.normalize("NFKC",s or "")
    for a,b in {"“":'"',"”":'"',"‘":"'","’":"'"}.items():s=s.replace(a,b)
    return re.sub(r"\s+"," ",s).strip().lower()
def snippet(text,m,w=90):return re.sub(r"\s+"," ",text[max(0,m.start()-w):m.end()+w]).strip()
def verify_sources(Q):
    """every expected answer must be found on the real PDF inside the declared cartridge page range (window never leaves it)"""
    pages=[norm(t) for t in DOC_PAGES];out={}
    for q in Q["questions"]:
        evs=[]
        for ev in q["evidence"]:
            targets=[f"C{i+1:02d}" for i in range(N_CART)] if ev["cartridge"]=="EVERY" else [ev["cartridge"]];per={}
            for cid in targets:
                a,b=BOUNDS[int(cid[1:])-1];hit=None
                for pg in range(max(a,ev.get("min_page",1)),b+1):
                    win=" ".join(pages[pg-1:min(b,pg+ev.get("window",1)-1)])
                    ms=[re.search(pat,win) for pat in ev["all"]]
                    if all(ms):hit=dict(pdf_page=pg,cartridge=cid,snippets=[snippet(win,m) for m in ms]);break
                per[cid]=hit
            evs.append(dict(cartridge=ev["cartridge"],patterns=ev["all"],found=({k:v for k,v in per.items() if v} if ev["cartridge"]=="EVERY" else per[targets[0]]),verified=all(per.values())))
        out[q["id"]]=dict(evidence=evs,verified=all(e["verified"] for e in evs))
    return out
def phases():return jload(PHASES_FILE,{}) or {}
def set_phase(name,**kw):
    ph=phases();ph.setdefault(name,{}).update(jsafe(kw));dump_json(PHASES_FILE,ph)
def panel_step():
    Q=json.loads(QFILE.read_text(encoding="utf-8"));cfg_text=norm(CFGFILE.read_text(encoding="utf-8"))
    if SEAL_FILE.is_file():
        s_=jload(SEAL_FILE,{})
        if s_.get("questions_sha256")==sha_file(QFILE) and s_.get("build_config_sha256")==sha_file(CFGFILE) and all(v.get("verified") for v in (s_.get("pdf_source_check") or {}).values()) and s_.get("pdf_source_check"):
            src=s_["pdf_source_check"];dump_json(PANEL_FILE,dict(seal=s_,note="existing seal of this experiment directory, re-verified (re-run)"))
            slog("SEAL","existing seal verified (re-run)",sealed_utc=s_["sealed_utc"],questions_sha256=s_["questions_sha256"]);_print_panel(Q,src);return dict(sealed_utc=s_["sealed_utc"],reused=True)
        if (phases().get("ASK") or {}).get("status"):
            raise PhaseFailed("SEAL.json exists, the question panel / build configuration changed and process 2 has already run: refusing to re-seal (delete /content/T719_RUNS to start a new experiment)")
        arch=RUNS/f"SEAL_superseded_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json";shutil.copyfile(SEAL_FILE,arch);SEAL_FILE.unlink()
        slog("SEAL","program/configuration changed before any question was asked to a model — previous seal archived, panel checked and sealed again",archived=arch.name)
    leaks=[]
    for q in Q["questions"]:
        for s_ in [q["text"],q["verifiable_answer"]]+q.get("leak_keywords",[]):
            if re.search(r"(?<![a-z0-9])"+re.escape(norm(s_))+r"(?![a-z0-9])",cfg_text):leaks.append(f"{q['id']}: {s_}")
    if leaks:raise PhaseFailed("QUESTION LEAK: the synthesis configuration contains question material: "+repr(leaks))
    src=verify_sources(Q);g=gpu_state();dump_json(SRC_CHECK_FILE,src)
    _print_panel(Q,src)
    bad=[k for k,v in src.items() if not v["verified"]]
    if bad:
        dump_json(PANEL_FILE,dict(pdf_source_check=src,sealed=False,unverified=bad))
        slog("SOURCE_CHECK","FAILED",unverified=bad)
        raise PhaseFailed(f"PDF SOURCE CHECK FAILED for {bad}: the expected answer was not found on the real PDF in the declared cartridge page range. "
                          "Stopping before any model is loaded. Details: QUESTION_PANEL_SOURCE_CHECK.json")
    s_=dict(test="TEST719",sealed_utc=utc_now(),questions_sha256=sha_file(QFILE),build_config_sha256=sha_file(CFGFILE),
            program_sha256={k:v["sha256"] for k,v in PROGRAM.items()},pdf_sha256=PDF_SHA256,pdf_source_check=src,
            synthesis_independence_check=dict(checked="question texts, verifiable answers and per-question keywords against the build configuration",leaks=[],passed=True),
            gpu_at_seal=g,statement="Sealed automatically in this run before any model weights were loaded (no GPU process at seal time). The build process never reads the questions.")
    if g.get("apps"):raise PhaseFailed(f"GPU not empty at seal time: {g['apps']}")
    dump_json(SEAL_FILE,s_);dump_json(PANEL_FILE,dict(seal=s_))
    slog("SEAL","question panel sealed before any model load; all five expected answers found on the PDF",questions_sha256=s_["questions_sha256"])
    return dict(sealed_utc=s_["sealed_utc"],questions_sha256=s_["questions_sha256"],verified=len(src))
def _print_panel(Q,src):
    for q in Q["questions"]:
        v=src.get(q["id"],{});_OUT.write(f"  {q['id']} {'✓ verified on the PDF' if v.get('verified') else '✗ NOT FOUND on the PDF'} · region {q.get('region')}\n      Q: {q['text']}\n      expected: {q['verifiable_answer']}\n")
        for ev in v.get("evidence",[]):
            f=ev.get("found") or {}
            if ev["cartridge"]=="EVERY":_OUT.write(f"      evidence: '{ev['patterns'][0]}' found in {len(f)}/{N_CART} cartridges\n")
            elif f:_OUT.write(f"      evidence: {f['cartridge']} PDF page {f['pdf_page']} · “{short(f['snippets'][-1],150)}”\n")
            else:_OUT.write(f"      evidence: {ev['cartridge']} — patterns {ev['patterns']} NOT found\n")
    _OUT.flush()
def short(s,n):s=" ".join(str(s or "").split());return s if len(s)<=n else s[:n-1].rstrip()+"…"

# ---------------------------------------------------------------------------------------------------------------------
# steps [5] and [6]: the two separate Python processes — output shown live, stored line by line with UTC time stamps
# ---------------------------------------------------------------------------------------------------------------------
PROC_LINES=[];HEARTBEATS=[];HEARTBEAT_FILE=SESSION_DIR/"HEARTBEAT_LAST.json"
STAGE_TITLES={"boot_and_C01-C10":"unchanged TEST716 set-up: PDF lock, frozen Qwen2.5-72B NF4, ten CUT3 cartridges C01–C10 (real download / loading progress follows)",
              "S1-S5_joint_and_final_synthesis":"S1–S5 written as cartridges, physically joined (initialize S1 → append S2…S5), general final synthesis",
              "C11_write_and_handoff":"C11 written as a CUT3 cartridge (SHA-256) + hand-off for the new process",
              "independence_before_boot":"isolation checks BEFORE the model is loaded (new process, empty GPU, file-system scan, quarantine)",
              "model_boot_C11_only":"frozen model (unchanged 716 model statements) + ONLY C11 in the cartridge registry",
              "questions":"C11 mounted alone, GPU memory audit, five sealed questions; then the same questions without any document"}
def _stage_title(name):
    m=re.match(r"pair(\d)(_retry\d)?$",name)
    if m:a,b=PAIRS[int(m.group(1))-1];return f"physical pair P{m.group(1)}: initialize({a}) → append({b}) · 80-layer SHA-256 · X-ray · general synthesis"+(" — REBUILT after a GPU memory recovery" if m.group(2) else "")
    return STAGE_TITLES.get(name,name)
def _hf_cache_bytes():
    try:
        from huggingface_hub.constants import HF_HOME;root=Path(HF_HOME)       # whole cache: hub blobs + Xet chunk store + temporary files
    except Exception:root=Path.home()/".cache"/"huggingface"
    tot=0
    for dp,dn,fn in os.walk(root):
        for f in fn:
            try:tot+=os.stat(os.path.join(dp,f),follow_symlinks=False).st_size
            except Exception:pass
    return tot
def _heartbeat(stop,t0,name,every=60):
    """observer only (no CUDA calls): every 60 s one line with the state of the running process"""
    while not stop.wait(every):
        try:smi=subprocess.run(["nvidia-smi","--query-gpu=memory.used,memory.total,utilization.gpu","--format=csv,noheader,nounits"],capture_output=True,text=True,timeout=20).stdout.strip()
        except Exception:smi=None
        try:
            mi=dict(l.split(":",1) for l in Path("/proc/meminfo").read_text().splitlines() if ":" in l);ram=round(int(mi["MemAvailable"].split()[0])/2**20,1)
        except Exception:ram=None
        last=PROC_LINES[-1] if PROC_LINES else (None,None,None,"(no process output yet)")
        hb=dict(utc=utc_now(),process=name,elapsed_min=round((time.perf_counter()-t0)/60,1),process_lines=len(PROC_LINES),last_line_utc=last[0],last_line=str(last[3])[:200],
                gpu_mib_used_total_util=smi,ram_available_gib=ram,model_cache_gib=round(_hf_cache_bytes()/2**30,1))
        HEARTBEATS.append(hb)
        try:dump_json(HEARTBEAT_FILE,dict(hb,note="last heartbeat of the running process"))
        except Exception:pass
        _OUT.write(f"\n  ⏱ {name} +{hb['elapsed_min']} min · lines {hb['process_lines']} · last: {hb['last_line'][:90]} · GPU {smi} MiB/%, RAM {ram} GiB free, Hugging Face cache {hb['model_cache_gib']} GiB\n");_OUT.flush()
        with _LOG_LOCK:
            with SESSION_LOG.open("a",encoding="utf-8") as f:f.write(f"{hb['utc']} HEARTBEAT          {json.dumps(hb,ensure_ascii=False)}\n")
QUIET=("FORGE_PROGRESS","APPEND_PROGRESS","APPEND_DIAG")
def run_proc(name,script,env):
    g=gpu_state()
    if g.get("apps"):slog("GPU_NOT_EMPTY",f"{name}: another GPU process is present before the start — recorded (process 2 reports it in its isolation record)",apps=g["apps"])
    e=dict(os.environ);e.update({k:str(v) for k,v in env.items()});e["PYTHONUNBUFFERED"]="1"
    cons=RUNS/"console";cons.mkdir(parents=True,exist_ok=True);lp=cons/f"{name}.log";tsv=cons/f"{name}_with_UTC_timestamps.tsv"
    st=utc_now();t=time.perf_counter();set_phase(name,status="RUNNING",start_utc=st);slog("PROCESS_START",name,script=script,gpu_used_mib=g.get("used_mib"))
    p=subprocess.Popen([sys.executable,"-u",script],cwd=str(PROGRAM_DIR),env=e,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stop=threading.Event();hb=threading.Thread(target=_heartbeat,args=(stop,t,name),daemon=True);hb.start()
    buf="";dec=__import__("codecs").getincrementaldecoder("utf-8")(errors="replace");progress=[False]
    def line_out(line):
        ts=utc_now();el=round(time.perf_counter()-t,3);PROC_LINES.append((ts,el,name,line))
        with lp.open("a",encoding="utf-8") as f:f.write(line+"\n")
        with tsv.open("a",encoding="utf-8") as f:f.write(f"{ts}\t{el}\t{line}\n")
        if any(x in line for x in QUIET):return
        m=re.match(r"\S+\s+STAGE_START\s+(\S+)",line)          # the event line itself, not a heartbeat that quotes it
        if progress[0]:_OUT.write("\n");progress[0]=False
        if m:_OUT.write("\n"+"·"*112+f"\n▶ {name} · {_stage_title(m.group(1))} · {local_now()} · +{el/60:.1f} min · {_gpu_short()}\n"+"·"*112+"\n")
        _OUT.write(f"  {name} │ {line[:300]}\n");_OUT.flush()
    try:
        fd=p.stdout.fileno()
        while True:
            chunk=os.read(fd,65536)
            if not chunk:break
            buf+=dec.decode(chunk)
            while "\n" in buf:
                line,buf=buf.split("\n",1);line_out(line.split("\r")[-1] if "\r" in line else line)
            if "\r" in buf:                          # live progress bars (download / loading) — shown, not stored per update
                seg=buf.split("\r")[-1]
                if seg.strip():_OUT.write(f"\r  {name} │ {seg[:200]}");_OUT.flush();progress[0]=True
                buf=seg
        if buf.strip():line_out(buf)
        rc=p.wait()
    finally:
        stop.set()
        if p.poll() is None:p.kill()
    end=utc_now();secs=round(time.perf_counter()-t,1)
    set_phase(name,status="COMPLETE" if rc==0 else "FAILED",end_utc=end,exit_code=rc,pid=p.pid,seconds=secs)
    slog("PROCESS_END",name,exit_code=rc,minutes=round(secs/60,1))
    if rc!=0:raise PhaseFailed(f"{name} process failed (exit {rc}); its last lines are above and in {lp}")
    return rc

def build_result():return jload(RUNS/"build_store"/"build_result.json",{}) or {}
def ask_result():return jload(ASK_DIR/"store"/"ask_result.json",{}) or {}
def _own_gpu_guard(name):
    g=gpu_state();own=[a for a in g.get("apps") or [] if a.split(",")[0].strip()==str(os.getpid())]
    if own:raise PhaseFailed(f"{name} has to run, but this notebook process still holds the model of an earlier run on the GPU {own}: Runtime → Restart session, then run again (completed phases are reused)")
def build_step():
    if phases().get("BUILD",{}).get("status")=="COMPLETE" and build_result().get("status")=="BUILD_COMPLETE" and (RUNS/"handoff"/"C11.pt").is_file():
        slog("SKIP","process 1 already complete in this experiment directory — its records are re-checked in step [7]")
    else:
        _own_gpu_guard("process 1")
        if (RUNS/"engine_dir_after_build").exists() and not ENGINE_DIR.exists():
            shutil.move(str(RUNS/"engine_dir_after_build"),str(ENGINE_DIR))      # re-run: C01–C10 reused only after 716's SHA-256 check
        try:run_proc("BUILD","TEST719_demo_build.py",{"T719_RUNS":str(RUNS)})
        except PhaseFailed as ex:
            raise PhaseFailed(f"PROCESS 1 stopped: {build_result().get('error') or ex}") from ex
        finally:_print_build()
    B=build_result()
    if B.get("status")!="BUILD_COMPLETE":raise PhaseFailed(f"PROCESS 1 status {B.get('status')}: {B.get('error')}")
    return dict(status=B["status"],c11_sha256=(B.get("C11") or {}).get("cartridge_sha256"),minutes=round((B.get("wall_seconds") or 0)/60,1))
def _print_build():
    B=build_result()
    if not B:return
    _OUT.write("\n  PROCESS 1 RESULT · status "+str(B.get("status"))+(f" · {B.get('error')}" if B.get("error") else "")+"\n")
    for p in B.get("pairs") or []:
        ap=p.get("append") or {};sy=p.get("synthesis") or {};em=sy.get("end_marker") or {}
        _OUT.write(f"  {p['pair']} {'+'.join(p['cartridges'])} · {ap.get('rows')} rows (expected {p.get('rows_expected')}) · append 80-layer SHA-256 {'PASS' if ap.get('verified') else 'FAIL'} · "
                   f"synthesis {sy.get('status')} (finish {sy.get('finish_reason')}, END marker {'last line' if em.get('at_end') else 'present' if em.get('present') else 'missing'}) · {sy.get('n_generated')} tokens · {sy.get('seconds')} s\n")
    for s in B.get("S") or []:_OUT.write(f"  {s['id']} cartridge · {s['body_tokens']} tokens · SHA-256 {s['cartridge_sha256'][:16]}…\n")
    j=B.get("joint") or {}
    if j:
        fi=j.get("final") or {};em=fi.get("end_marker") or {}
        _OUT.write(f"  S1–S5 joint · {j.get('rows')} rows · 4 appends {'PASS' if all(a.get('verified') for a in j.get('appends',[])) else 'FAIL'} · final synthesis {fi.get('status')} "
                   f"(finish {fi.get('finish_reason')}, END marker {'last line' if em.get('at_end') else 'present' if em.get('present') else 'missing'}) · {fi.get('n_generated')} tokens · {fi.get('seconds')} s\n")
    c=B.get("C11") or {}
    _OUT.write(f"  C11 · {c.get('body_tokens','—')} tokens · SHA-256 {c.get('cartridge_sha256','NOT WRITTEN')}\n" if c else "  C11 · NOT WRITTEN\n");_OUT.flush()

def ask_step():
    if phases().get("ASK",{}).get("status")=="COMPLETE" and ask_result().get("status")=="ASK_COMPLETE":
        slog("SKIP","process 2 already complete in this experiment directory — its records are re-checked in step [7]")
    else:
        b=phases()["BUILD"];_own_gpu_guard("process 2")
        if ENGINE_DIR.exists():
            dst=RUNS/"engine_dir_after_build";shutil.rmtree(dst,ignore_errors=True);shutil.move(str(ENGINE_DIR),str(dst))
            slog("QUARANTINE","build engine directory (C01–C10, S1–S5, PDF copy) moved into the quarantined area")
        shutil.rmtree(ASK_IN,ignore_errors=True);ASK_IN.mkdir(parents=True)
        for f in ("C11.pt","C11.sha256","handoff.json"):shutil.copyfile(RUNS/"handoff"/f,ASK_IN/f)
        shutil.rmtree(ASK_DIR,ignore_errors=True)
        try:
          try:
            run_proc("ASK","TEST719_demo_ask.py",{"T719_QUARANTINE":f"{RUNS}:{PRIVATE_DIR}","T719_ASK_OUT":str(ASK_DIR),"T719_HANDOFF":str(ASK_IN),
                                                   "T719_BUILD_EXIT_CODE":b.get("exit_code"),"T719_BUILD_ENDED_UTC":b.get("end_utc")})
          except PhaseFailed as ex:
            if not (ask_result().get("answers")):raise
            slog("PROCESS_NOTE","process 2 ended with an error after recording answers — the recorded answers are kept and the gap is reported",error=str(ex))
        finally:
            if ENGINE_DIR.exists():
                dst=RUNS/"engine_dir_after_ask";shutil.rmtree(dst,ignore_errors=True);shutil.move(str(ENGINE_DIR),str(dst))
            _print_ask()
    A=ask_result()
    if not A.get("answers"):raise PhaseFailed(f"PROCESS 2 produced no answer: status {A.get('status')}: {A.get('error')}")
    if A.get("status")!="ASK_COMPLETE":slog("PROCESS_NOTE",f"process 2 status {A.get('status')} — partial result, reported",error=A.get("error"))
    return dict(status=A["status"],answers=len(A.get("answers") or []),minutes=round((A.get("wall_seconds") or 0)/60,1))
def _print_ask():
    A=ask_result()
    if not A:return
    ind=A.get("independence") or {}
    _OUT.write("\n  PROCESS 2 RESULT · status "+str(A.get("status"))+(f" · {A.get('error')}" if A.get("error") else "")+"\n")
    for k,lab in ISO_LABELS:
        v=ind.get(k) or {};_OUT.write(f"  {'PASS' if v.get('pass') else 'FAIL' if v else '  — '}  {lab}\n")
    for r in A.get("answers") or []:
        _OUT.write(f"\n  ── {r['id']} · {r['condition']} · {r['status']} · finish {r.get('finish_reason')} · {r['n_generated']} tokens (ceiling {r['ceiling']}) · {r['seconds']} s\n"
                   f"  Q: {r['question']}\n"+"\n".join("  │ "+l for l in str(r["text"]).splitlines() or [""])+"\n")
    _OUT.flush()
ISO_LABELS=[("process","new Python process, started after process 1 exited (same Colab VM — not a separate machine)"),
            ("gpu_before_model_load","GPU empty before the model was loaded"),
            ("filesystem_scan","no C01–C10 / S1–S5 file and no pair-synthesis text outside the quarantined directories"),
            ("quarantine_audit","quarantined build directories never opened (audit hook)"),
            ("cartridge_directory","engine cartridge registry = C11 only"),
            ("same_weights_as_build","same frozen weights as process 1 (weight sentinel)"),
            ("c11_memory_audit","GPU memory above the model-only baseline = C11 K/V (allocator + unique storages)")]

# ---------------------------------------------------------------------------------------------------------------------
# automatic indicator per answer (fixed text rules, sealed before generation) — NOT expert verification
# ---------------------------------------------------------------------------------------------------------------------
ABSTAIN=re.compile(r"\bunknown\b|cannot (be )?(verif|determin|provid|find|confirm)|not (available|provided|specified|mentioned|contained|included)|does not (contain|mention|provide|specify|include)|no (information|mention)|do not have access|don't have access",re.I)
def evaluate(text,status,rule):
    if status=="ERROR":return "NOT_PRODUCED","generation failed after a recovery attempt — the error is in the records"
    if status=="INCOMPLETE":return "INCOMPLETE","safety ceiling reached; not counted as an answer"
    if status!="COMPLETE":return "UNVERIFIED_FINISH","the end of generation could not be confirmed as a stop token"
    t=norm(text)
    if ABSTAIN.search(t):return "UNCLEAR","the answer abstains (UNKNOWN / not available)"
    hits_any=[p for p in rule.get("correct_any",[]) if re.search(p,t)];alls=[bool(re.search(p,t)) for p in rule.get("correct_all",[])]
    bad=[p for p in rule.get("incorrect_any",[]) if re.search(p,t)];ok=bool(hits_any) or (bool(alls) and all(alls))
    if ok and not bad:return "CORRECT","rule met"
    if ok and bad:return "UNCLEAR","rule met but contradicting content present: "+repr(bad)
    if bad:return "INCORRECT","contradicts the source: "+repr(bad)
    if alls and any(alls):return "UNCLEAR","only part of the expected answer"
    return "INCORRECT","expected content not found"
def trace(text,rule):
    t=norm(text);alls=[bool(re.search(p,t)) for p in rule.get("correct_all",[])]
    if any(re.search(p,t) for p in rule.get("correct_any",[])) or (alls and all(alls)):return "yes"
    return "partly" if any(alls) else "no"

# ---------------------------------------------------------------------------------------------------------------------
# LIVE experiment record: everything below is computed from this run's records (process 1, process 2, the seal, the PDF)
# ---------------------------------------------------------------------------------------------------------------------
LIVE={}
def live_record():
    Q=json.loads(QFILE.read_text(encoding="utf-8"));seal=jload(SEAL_FILE,{}) or {};src=seal.get("pdf_source_check") or jload(SRC_CHECK_FILE,{}) or {}
    B=build_result();A=ask_result();fin_p=RUNS/"build_store"/"synthesis"/"FINAL.txt";final=fin_p.read_text(encoding="utf-8") if fin_p.is_file() else ""
    rows=[]
    for q in Q["questions"]:
        ans={}
        for r in A.get("answers") or []:
            if r["id"]==q["id"]:
                ev,why=evaluate(r["text"],r["status"],q["rule"])
                ans[r["condition"]]=dict(text=r["text"],status=r["status"],finish_reason=r.get("finish_reason"),finish_evidence=r.get("finish_evidence"),n_generated=r["n_generated"],
                                         ceiling=r["ceiling"],seconds=r["seconds"],sha256=r["sha256"],memory=r["memory"],memory_rows=r.get("memory_rows"),utc=r.get("utc"),evaluation=ev,why=why)
        rows.append(dict(id=q["id"],text=q["text"],verifiable_answer=q["verifiable_answer"],source=q["source"],region=q.get("region"),note=q.get("note"),
                         requires=q.get("requires_cartridges"),pdf_evidence=src.get(q["id"]),answers=ans,c11_body_trace=(trace(final,q["rule"]) if final else "n/a")))
    prov=((A.get("provenance") or B.get("provenance") or {}).get("mode")) or "n/a"
    return dict(provenance=prov,seal={k:seal.get(k) for k in ("sealed_utc","questions_sha256","build_config_sha256","pdf_sha256","statement")},question_design=Q.get("question_design"),
                evaluation_policy=Q.get("evaluation_policy"),questions=rows,build={k:B.get(k) for k in ("status","stages","pairs","S","joint","C11","weights_unchanged","sentinel_before","wall_seconds","error","engine","model_pin")},
                ask={k:A.get(k) for k in ("status","independence","c11","weights_unchanged","wall_seconds","error","engine","warmup","model_pin")},phases=phases(),
                final_synthesis_tokens=((B.get("joint") or {}).get("final") or {}).get("n_generated"),final_synthesis_sha256=(sha_bytes(final.encode()) if final else None))

def xray_metas():
    out={}
    for d in (RUNS/"build_store"/"xray",ASK_DIR/"store"/"xray"):
        for m in sorted(d.glob("*.json")) if d.is_dir() else []:out[m.stem]=jload(m,{})
    return out

def verify_disk():
    """re-hash every cartridge file of this experiment on disk and compare with the SHA-256 the processes recorded"""
    B=build_result();rows=[];t=time.perf_counter()
    src_dir=RUNS/"engine_dir_after_build"/"cartridges"
    want=[(b["id"],src_dir/(b["id"]+".pt"),b.get("cartridge_sha256")) for b in (B.get("sources") or [])]+[(s["id"],src_dir/(s["id"]+".pt"),s.get("cartridge_sha256")) for s in (B.get("S") or [])]
    if B.get("C11"):want.append(("C11 (hand-off)",RUNS/"handoff"/"C11.pt",B["C11"].get("cartridge_sha256")))
    if STATE.get("mount") and E.get("CART"):want.append(("C11 (interface copy)",Path(E["CART"])/"C11.pt",(B.get("C11") or {}).get("cartridge_sha256")))
    for cid,p,rec in want:
        h=sha_file(p) if p.is_file() else None
        rows.append(dict(cartridge=cid,file=str(p),bytes=(p.stat().st_size if p.is_file() else None),sha256=h,record_sha256=rec,equals_record=(h is not None and h==rec)))
    row=dict(utc=utc_now(),files=rows,passed=(len(rows)>=N_CART+N_PAIRS+1 and all(r["equals_record"] for r in rows)),seconds=round(time.perf_counter()-t,2))
    STATE["disk_checks"].append(row);slog("DISK_CHECK","PASS" if row["passed"] else "FAIL",files=len(rows),passed=row["passed"],seconds=row["seconds"]);return row

def compute_verification():
    """every record is checked; nothing here stops the run. Items are classed as
    INTEGRITY  (the physical memory / the answers are what they claim to be — a failure means the result is NOT valid),
    ISOLATION  (support for the claim 'C11 alone in a new process' — a failure means that claim is NOT supported),
    FORMAL     (format / observation / memory-profile notes — reported, they do not invalidate the computation)."""
    L=live_record();B=build_result();A=ask_result();ind=A.get("independence") or {};items=[]
    def add(name,ok,detail,cls="INTEGRITY"):items.append(dict(name=name,passed=bool(ok),detail=jsafe(detail),cls=cls))
    seal=jload(SEAL_FILE,{}) or {};src=seal.get("pdf_source_check") or {};ph=phases()
    add("SOURCE_PDF_SHA256_AND_PAGES",DOC.get("sha256")==PDF_SHA256 and DOC.get("pages")==PDF_PAGES,f"{DOC.get('pages')} pages · {str(DOC.get('sha256'))[:16]}…")
    add("ENGINE_SOURCE_LOCKS",all(SOURCES.get(k,{}).get("git_blob")==LOCKS[k] for k in ("716.py","709.py")),"716.py + 709.py git blobs")
    add("PROGRAM_FILES_SHA256",len(PROGRAM)==5 and all(sha_file(v["local"])==v["sha256"] for v in PROGRAM.values()),f"{len(PROGRAM)} files")
    add("PANEL_VERIFIED_ON_PDF_BEFORE_MODEL_LOAD",bool(src) and all(v.get("verified") for v in src.values()) and str(seal.get("sealed_utc",""))<str(ph.get("BUILD",{}).get("start_utc","~")),
        f"{sum(1 for v in src.values() if v.get('verified'))}/{len(src)} questions · sealed {seal.get('sealed_utc')} · process 1 started {ph.get('BUILD',{}).get('start_utc')}")
    add("PROCESS1_COMPLETE",ph.get("BUILD",{}).get("exit_code")==0 and B.get("status")=="BUILD_COMPLETE",B.get("status"))
    srcs=B.get("sources") or [];add("TEN_SOURCE_CARTRIDGES_C01_C10",len(srcs)==N_CART and all(b.get("cartridge_sha256") for b in srcs),f"{len(srcs)}/{N_CART}")
    pr=B.get("pairs") or []
    add("FIVE_PAIR_APPENDS_ALL_80_LAYERS_SHA256",len(pr)==N_PAIRS and all((p.get("append") or {}).get("verified") and (p.get("append") or {}).get("pass_line") and (p.get("append") or {}).get("rows")==p.get("rows_expected") for p in pr),
        f"{sum(1 for p in pr if (p.get('append') or {}).get('verified'))}/{N_PAIRS} · engine line PASS APPEND_ALL_80_LAYERS_EXACT_SHA256")
    add("FIVE_PAIR_SYNTHESES_ACCEPTED_NOT_CUT",len(pr)==N_PAIRS and all((p.get("synthesis") or {}).get("accepted") for p in pr),[f"{p['pair']}: {(p.get('synthesis') or {}).get('status')} / {(p.get('synthesis') or {}).get('finish_reason')}" for p in pr])
    j=B.get("joint") or {}
    add("S1_S5_WRITTEN_AND_PHYSICALLY_JOINED",len(B.get("S") or [])==N_PAIRS and len(j.get("appends") or [])==4 and all(a.get("verified") for a in j.get("appends") or []),f"{len(B.get('S') or [])} cartridges · {len(j.get('appends') or [])} appends")
    add("FINAL_SYNTHESIS_ACCEPTED_NOT_CUT",(j.get("final") or {}).get("accepted"),f"{(j.get('final') or {}).get('status')} / {(j.get('final') or {}).get('finish_reason')} · {(j.get('final') or {}).get('n_generated')} tokens")
    c11=B.get("C11") or {};hp=RUNS/"handoff"/"C11.pt"
    add("C11_WRITTEN_SHA256",bool(c11) and hp.is_file() and sha_file(hp)==c11.get("cartridge_sha256"),str(c11.get("cartridge_sha256"))[:16]+"…")
    ans=A.get("answers") or []
    add("TEN_ANSWERS_RECORDED",sum(1 for a in ans if a.get("status")!="ERROR")==10 and {a["condition"] for a in ans}=={"C11","NO_DOCUMENT"},f"{sum(1 for a in ans if a.get('status')!='ERROR')}/10 raw answers produced (5 × C11 alone, 5 × no document)")
    add("WEIGHT_SENTINEL_UNCHANGED",bool(B.get("weights_unchanged")) and bool(A.get("weights_unchanged")),"process 1 and process 2")
    d=verify_disk();add("CARTRIDGE_FILES_SHA256_ON_DISK",d["passed"],f"{sum(1 for r in d['files'] if r['equals_record'])}/{len(d['files'])} files (C01–C10, S1–S5, C11)")
    add("PROCESS2_COMPLETE",ph.get("ASK",{}).get("exit_code")==0 and A.get("status")=="ASK_COMPLETE",A.get("status"),"ISOLATION" if A.get("answers") else "INTEGRITY")
    for k,lab in ISO_LABELS:add("ISOLATION_"+k.upper(),(ind.get(k) or {}).get("pass"),lab,"ISOLATION")
    xm=xray_metas();need=[f"P{k+1}_{a}+{b}_joint" for k,(a,b) in enumerate(PAIRS)]+["S1-S5_joint","C11"]
    add("XRAYS_FROM_LIVE_KV",all(n in xm and xm[n].get("finite") and xm[n].get("layers")==EXPECTED_ARCH[0] for n in need),f"{sum(1 for n in need if n in xm)}/{len(need)} (five pairs, S1–S5 joint, C11 alone)","FORMAL")
    flags=[(p["pair"],f) for p in pr for f in (p.get("synthesis") or {}).get("flags") or []]+[("FINAL",f) for f in (j.get("final") or {}).get("flags") or []]
    add("SYNTHESIS_FORMAT_AND_FINISH_FLAGS",not flags,[f"{a}: {b}" for a,b in flags] or "none","FORMAL")
    rec_=B.get("memory_recoveries") or [];prof=B.get("memory_profile") or {}
    nondef={k:v for k,v in prof.items() if (v.get("chunk_tokens"),v.get("reserve_gib"))!=(256,9.0)}
    add("DEFAULT_MEMORY_PROFILE_USED",not rec_ and not nondef,(f"{len(rec_)} recoveries · profiles {nondef}" if (rec_ or nondef) else "chunk 256 · reserve 9 GiB")+f" · cached-memory releases before the reserve check: {(B.get('ensure_room_recoveries') or {}).get('count',0)}","FORMAL")
    notes=(A.get("notes") or [])+[dict(kind="PROCESS1_MEMORY_NOTE",detail=n) for n in (B.get("memory_notes") or [])]
    add("NO_PROCESS_NOTES",not notes,[n["kind"] for n in notes] or "none","FORMAL")
    integ=[i for i in items if i["cls"]=="INTEGRITY"];iso=[i for i in items if i["cls"]=="ISOLATION"];form=[i for i in items if i["cls"]=="FORMAL"]
    result=("VALID" if all(i["passed"] for i in integ) else "NOT VALID — integrity failure: "+", ".join(i["name"] for i in integ if not i["passed"]))
    isolation=("SUPPORTED" if all(i["passed"] for i in iso) else "NOT SUPPORTED — "+", ".join(i["name"] for i in iso if not i["passed"]))
    rec=dict(session=SESSION_ID,utc=utc_now(),ready=all(i["passed"] for i in integ),passed=sum(i["passed"] for i in items),total=len(items),items=items,provenance=L["provenance"],
             result=result,isolation=isolation,formal_gaps=[i["name"] for i in form if not i["passed"]],
             semantics="NOT VERIFIED — answers are raw model output; the indicator is an automatic text rule fixed before generation")
    STATE["verification"]=rec;dump_json(VERIFY_FILE,rec);dump_json(LIVE_MEAS,L)
    LIVE.clear();LIVE.update(L)
    slog("VERIFICATION",result,isolation=isolation,passed=rec["passed"],total=rec["total"],failed=[i["name"] for i in items if not i["passed"]]);return rec

# ---------------------------------------------------------------------------------------------------------------------
# step [8]: the interface memory — model + ONLY C11 in THIS notebook process (process 2 has ended; GPU must be empty)
# ---------------------------------------------------------------------------------------------------------------------
KENG=None;ENGINE_LOCK=threading.RLock();KLOG_FILE=SESSION_DIR/"INTERFACE_ENGINE_EVENTS.jsonl"
class _KLog:
    def ev(self,kind,msg="",/,**data):
        with KLOG_FILE.open("a",encoding="utf-8") as f:f.write(json.dumps(jsafe(dict(utc=utc_now(),kind=kind,msg=msg,data=data)),ensure_ascii=False)+"\n")
        _OUT.write(f"  engine │ {kind:<18} {msg} {short(json.dumps(jsafe(data),ensure_ascii=False),200) if data else ''}\n");_OUT.flush()
def _require():
    if KENG is None or STATE.get("memory") is None:raise OpError("The interface memory (frozen model + C11) is not loaded in this session.")
def engine_architecture():
    if not E.get("model"):
        eng=(build_result().get("engine") or {});a=eng.get("arch")
        if not a:return None
        NL,H,QH,KVH,HD=a;return dict(layers=NL,hidden=H,q_heads=QH,kv_heads=KVH,head_dim=HD,cut=EXPECTED_CUT,prefix_tokens=eng.get("P"),full_kv_bytes_per_token=NL*KVH*HD*2*2,
                                       weights="NF4 4-bit (bitsandbytes), BF16 compute, frozen",model_id=MODEL_ID,source="process 1 record")
    return dict(layers=E["NL"],hidden=E["H"],q_heads=E["QH"],kv_heads=E["KVH"],head_dim=E["HD"],cut=E["CUT"],prefix_tokens=E.get("P"),full_kv_bytes_per_token=E["NL"]*E["KVH"]*E["HD"]*2*2,
                chunk=E.get("CHUNK"),reserve_gib=E.get("GPU_RESERVE_GIB"),weights="NF4 4-bit (bitsandbytes), BF16 compute, frozen",model_id=E.get("MODEL_ID",MODEL_ID),source="this notebook process")
def ready_memory():
    global KENG,E
    g=gpu_state();own=[a for a in g.get("apps") or [] if a.split(",")[0].strip()==str(os.getpid())];other=[a for a in g.get("apps") or [] if a not in own]
    if other:raise RuntimeError(f"READY MEMORY: another process is using the GPU {other} — Runtime → Restart session, then run again (completed phases are reused)")
    if own:
        found=[o for o in __import__("gc").get_objects() if type(o).__name__=="Engine" and isinstance(getattr(o,"E",None),dict) and o.E.get("model") is not None]
        if found:return _reuse_loaded_engine(own)
        import torch;__import__("gc").collect();torch.cuda.empty_cache()     # an earlier run left only cached memory: release it, then load normally
        slog("READY_MEMORY_NOTE","no loaded engine of an earlier run found in this notebook process — cached GPU memory released, loading normally",apps=own)
    import torch
    prov=C.provenance(torch);klog=_KLog();hd=jload(RUNS/"handoff"/"handoff.json",{})
    saved={k:os.environ.get(k) for k in ("HF_HUB_OFFLINE","TRANSFORMERS_OFFLINE")}
    with ENGINE_LOCK:
        pin=C.pin_model_revision(klog,prov["mode"])
        try:
            KENG=C.Engine(klog,prov["mode"]);info=KENG.boot(model_only=True)
        finally:
            for k,v in saved.items():                      # the model is loaded: give the network back to the interface (share link)
                if v is None:os.environ.pop(k,None)
                else:os.environ[k]=v
        E=KENG.E;CART=Path(E["CART"])
        for f in CART.iterdir():f.unlink()
        E["R"]["books"]=[]
        shutil.copyfile(RUNS/"handoff"/"C11.pt",CART/"C11.pt");shutil.copyfile(RUNS/"handoff"/"C11.sha256",CART/"C11.sha256");KENG.register_existing(hd["allowed"]["C11"])
        t=time.perf_counter();memory,mrec=KENG.mount("C11")
        STATE["memory"]=memory;STATE["mount"]=dict(mrec,end_to_end_s=round(time.perf_counter()-t,2),gpu=E["mem"]());STATE["ops"].append(STATE["mount"])
    w=verify_weights()
    if not w["passed"]:raise RuntimeError("READY MEMORY: the weight sentinel of this process differs from process 1")
    slog("READY_MEMORY","frozen model + C11 mounted in this notebook process",rows=mrec["rows"],commit=info.get("commit_hash"),pin=pin.get("pinned"))
    return dict(rows=mrec["rows"],seconds=STATE["mount"]["end_to_end_s"],weights_equal_process1=w["passed"])
def _reuse_loaded_engine(own):
    """the cell was run again in the same notebook process: the frozen model loaded by the earlier run is still in GPU memory.
    It is found and reused (no second copy would fit); C11 is mounted again from the SHA-checked hand-off and the weights are
    compared with process 1."""
    global KENG,E
    import gc as _gc
    old=[o for o in _gc.get_objects() if type(o).__name__=="Engine" and isinstance(getattr(o,"E",None),dict) and o.E.get("model") is not None]
    if not old:raise RuntimeError(f"READY MEMORY: this notebook process holds GPU memory {own} but no loaded engine was found — Runtime → Restart session, then run again (completed phases are reused)")
    hd=jload(RUNS/"handoff"/"handoff.json",{})
    with ENGINE_LOCK:
        KENG=old[-1];E=KENG.E;KENG.log=_KLog();CART=Path(E["CART"]);CART.mkdir(parents=True,exist_ok=True)
        for f in CART.iterdir():
            if f.is_file():f.unlink()
        E["R"]["books"]=[]
        shutil.copyfile(RUNS/"handoff"/"C11.pt",CART/"C11.pt");shutil.copyfile(RUNS/"handoff"/"C11.sha256",CART/"C11.sha256");KENG.register_existing(hd["allowed"]["C11"])
        KENG.free_cached() if hasattr(KENG,"free_cached") else E["free_gpu"]()
        t=time.perf_counter();memory,mrec=KENG.mount("C11")
        STATE["memory"]=memory;STATE["mount"]=dict(mrec,end_to_end_s=round(time.perf_counter()-t,2),gpu=E["mem"](),reused_model_of_earlier_run=True);STATE["ops"].append(STATE["mount"])
    w=verify_weights()
    if not w["passed"]:raise RuntimeError("READY MEMORY: the weight sentinel of the reused model differs from process 1")
    slog("READY_MEMORY","frozen model of the earlier run in this notebook process reused + C11 mounted",rows=mrec["rows"])
    return dict(rows=mrec["rows"],seconds=STATE["mount"]["end_to_end_s"],weights_equal_process1=w["passed"],reused_model=True)
def ntok(text):
    try:return len(E["tok"](str(text or ""),add_special_tokens=False).input_ids)
    except Exception:return None
def ask_live(question,use_memory=True,origin="user"):
    """an interface question: answer(C11 memory or None, question), up to INTERACTIVE_MAX_NEW tokens; NOT part of the sealed panel"""
    with ENGINE_LOCK:
        _require();q=(question or "").strip()
        if not q or len(q)>3000:raise OpError("The question must contain 1–3000 characters.")
        r=KENG.answer(STATE["memory"] if use_memory else None,q,INTERACTIVE_MAX_NEW,EXPECTED_RESERVE_GIB,("C11:" if use_memory else "NO_DOCUMENT:")+origin)
        row=dict(utc=r["utc"],origin=origin,question=q,raw=r["text"],status=r["status"],finish_reason=r["finish_reason"],n_generated=r["n_generated"],ceiling=r["ceiling"],
                 cartridge=("C11" if use_memory else None),with_memory=bool(use_memory),cache_tokens=(KENG.rows(STATE["memory"]) if use_memory else 0),seconds=r["seconds"],gpu=E["mem"](),
                 sealed_panel=False,semantics="NOT VERIFIED")
        (STATE["qa"] if use_memory else STATE["controls"]).append(row)
        with SESSION_QA.open("a",encoding="utf-8") as f:f.write(json.dumps(jsafe(row),ensure_ascii=False)+"\n")
        slog("QA" if use_memory else "QA_NO_DOCUMENT",row["cartridge"] or "NO DOCUMENT",question=q[:300],status=row["status"],seconds=row["seconds"]);return row
def verify_weights():
    with ENGINE_LOCK:
        if KENG is None:raise OpError("The model is not loaded in this notebook process.")
        t=time.perf_counter();after=E["sentinel"]();before=build_result().get("sentinel_before")
        row=dict(utc=utc_now(),passed=(before is not None and after==before),before=before,after=after,seconds=round(time.perf_counter()-t,2),reference="weight sentinel of process 1 at load")
        STATE["weight_checks"].append(row);slog("WEIGHT_CHECK","PASS" if row["passed"] else "FAIL",**row);return row
def release_memory(reason):
    if STATE.get("memory") is not None:
        STATE["memory"]=None
        try:E["free_gpu"]()
        except Exception:pass
        slog("MEMORY_RELEASED",reason)

# ---------------------------------------------------------------------------------------------------------------------
# THREE RESEARCH FIGURES (JPEG 300 dpi, PNG lossless, PDF vector) — values ONLY from this run's records
# ---------------------------------------------------------------------------------------------------------------------
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.linewidth":.9,"axes.edgecolor":"#374151","axes.labelcolor":"#111827",
                     "xtick.color":"#374151","ytick.color":"#374151","xtick.labelsize":10.5,"ytick.labelsize":10.5,"axes.labelsize":12,
                     "axes.titlesize":13,"axes.titleweight":"bold","axes.titlelocation":"left","legend.fontsize":10.5,"legend.frameon":False})
FW,FH=13.333,7.5;OUT_DPI=300
INK,INK2,MUTED,RULE,PANEL="#111827","#374151","#6B7280","#D1D5DB","#F8FAFC"
TEAL,RED,AMBER,GREY="#0F766E","#B91C1C","#B45309","#9CA3AF"
STATUS_COL={"CORRECT":"#047857","INCORRECT":RED,"UNCLEAR":AMBER,"INCOMPLETE":"#6D28D9","UNVERIFIED_FINISH":"#92400E","NOT_PRODUCED":GREY}
FIGURES=OrderedDict([("F1","Figure 1 — Five physical pair memories: 80-layer K/V X-ray"),
                     ("F2","Figure 2 — S1–S5 joint memory and the new cartridge C11"),
                     ("F3","Figure 3 — Five fixed questions: C11 alone vs no document")])
FIG_FILES={}
def mt(s):return str(s).replace("$",r"\$")
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
def _is_live():return LIVE.get("provenance")=="GPU_REAL"
def fig_base(k,title,subtitle,h=FH):
    fig=plt.figure(figsize=(FW,h),dpi=100,facecolor="white");s=FH/h
    badge,badge_col=("LIVE A100 MEASUREMENT",TEAL) if _is_live() else ("SIMULATION — NOT A RESULT",RED)
    b=fig.text(.965,1-.05*s,badge,fontsize=10.5,weight="bold",color=badge_col,va="center",ha="right",bbox=dict(boxstyle="square,pad=0.4",fc="white",ec=badge_col,lw=1.2))
    bx0=_bb(fig,b).x0-.015
    fig.text(.035,1-.05*s,f"Fig. {k}",fontsize=15,weight="bold",color=MUTED,va="center")
    ftext(fig,.095,1-.05*s,title,xmax=bx0,minsize=12,fontsize=18,weight="bold",color=INK,va="center")
    ftext(fig,.035,1-.095*s,subtitle,minsize=8,fontsize=12,color=INK2,va="center")
    fig.add_artist(Line2D([.035,.965],[1-.122*s,1-.122*s],transform=fig.transFigure,color=INK2,lw=.8))
    if not _is_live():
        fig.text(.5,.45,"SIMULATION — NOT EXPERIMENTAL DATA",fontsize=40,color=RED,alpha=.12,rotation=18,ha="center",va="center",weight="bold",gid="qc-ignore",zorder=100)
    return fig
def fig_footer(fig,k,note,h=FH):
    s=FH/h
    fig.add_artist(Line2D([.035,.965],[.075*s,.075*s],transform=fig.transFigure,color=RULE,lw=.7))
    ftext(fig,.035,.05*s,note,minsize=7.5,fontsize=10,color=INK2,va="center")
    qs=str((LIVE.get("seal") or {}).get("questions_sha256"))[:10]
    ftext(fig,.035,.022*s,f"{APP_SHORT} · {ORG} · {LICENSE_NAME} · {COPYRIGHT} · 716.py {LOCKS['716.py'][:10]} · panel {qs} · live session {SESSION_ID} · Fig. {k}/{len(FIGURES)}",
          minsize=6,fontsize=8.6,color=MUTED,va="center",family="DejaVu Sans Mono")
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
    stem=("" if _is_live() else "SIMULATION_")+f"FIGURE_{k:02d}_{key}"
    jpg=FIG_DIR/(stem+".jpg");png=FIG_DIR/(stem+".png");pdf=FIG_DIR/(stem+".pdf")
    fig.savefig(pdf,facecolor="white");buf=io.BytesIO();fig.savefig(buf,format="png",dpi=OUT_DPI,facecolor="white");plt.close(fig)
    png.write_bytes(buf.getvalue())
    with Image.open(io.BytesIO(buf.getvalue())) as im:im.convert("RGB").save(jpg,"JPEG",quality=95,optimize=True,subsampling=0,dpi=(OUT_DPI,OUT_DPI))
    jq=jpeg_qc(jpg);size=tuple(jq["pixels"])
    rec=dict(key=key,figure=k,title=FIGURES[f"F{k}"],jpg=str(jpg),png=str(png),pdf=str(pdf),pixels=list(size),jpg_bytes=jpg.stat().st_size,sha256_jpg=sha_file(jpg),utc=utc_now(),
             layout_qc=dict(passed=qc["passed"],texts=qc["texts"],fix_rounds=qc["rounds"],font_reductions=qc["fixed"]),jpeg_qc=jq,provenance=LIVE.get("provenance"),
             data="live session "+SESSION_ID+" · values traceable in LIVE_MEASUREMENTS.json / VERIFICATION_RECORD.json / records_process1 / records_process2")
    flog(f"FIGURE {k} {key} {size[0]}x{size[1]} jpg sha256 {rec['sha256_jpg']}");return rec
def _npz(p):
    if not Path(p).is_file():return None
    z=np.load(p);return z["K"],z["V"]
def binned(a,b=256):
    nb=int(np.ceil(a.shape[1]/b));return np.stack([a[:,i*b:(i+1)*b].mean(axis=1) for i in range(nb)],axis=1)
def _xray_ok(meta):
    if not meta:return False
    if _is_live() and meta.get("provenance")!="GPU_REAL":raise RuntimeError("an X-ray record of this run is not a GPU measurement: "+str(meta.get("label")))
    return True

def fig1(k=1):
    a=engine_architecture() or {};xm=xray_metas();data=[]
    for i,(ca,cb) in enumerate(PAIRS,1):
        j=_npz(RUNS/"build_store"/"xray"/f"P{i}_{ca}+{cb}_joint.npz");al=_npz(RUNS/"build_store"/"xray"/f"P{i}_{ca}_alone.npz")
        if j is not None and _xray_ok(xm.get(f"P{i}_{ca}+{cb}_joint")):data.append((f"P{i} · {ca}+{cb}",j[0],j[1],(al[0].shape[1] if al is not None else None)))
    if len(data)!=N_PAIRS:raise RuntimeError(f"pair X-ray records: {len(data)}/{N_PAIRS}")
    fig=fig_base(k,"Five physical pair memories — 80-layer K/V X-ray of the live GPU memory",
                 f"initialize(C_odd) → append(C_even) · all prior K/V bytes of all {a.get('layers',80)} layers verified by exact SHA-256 · measured read-only before each synthesis")
    lims=[(np.percentile(np.concatenate([binned(d[i]).ravel() for d in data]),2),np.percentile(np.concatenate([binned(d[i]).ravel() for d in data]),98)) for i in (1,2)]
    x0,wd,gap=.07,.152,.022
    for i,(name,K,V,n_a) in enumerate(data):
        for r,(arr,lim,nm) in enumerate(((K,lims[0],"K"),(V,lims[1],"V"))):
            ax=fig.add_axes([x0+i*(wd+gap),.50-r*.355,wd,.29]);im=ax.imshow(binned(arr),aspect="auto",origin="lower",cmap="Blues",vmin=lim[0],vmax=lim[1],interpolation="nearest")
            if n_a:ax.axvline(n_a/256-.5,color="#EA580C",lw=1.3,ls="--")
            ax.set_xticks([]);ax.set_yticks([0,40,79]) if i==0 else ax.set_yticks([])
            if i==0:ax.set_ylabel(f"{nm} · layer",fontsize=10)
            if r==0:ax.set_title(f"{name} · {K.shape[1]:,} rows",fontsize=10.5,color=ccol(2*i))
            if i==len(data)-1:
                cb=fig.colorbar(im,cax=fig.add_axes([x0+len(data)*(wd+gap)-.012,.50-r*.355,.008,.29]));cb.ax.tick_params(labelsize=8)
    fig_footer(fig,k,"Orange dashed line = end of the initialized cartridge, start of the appended one. One shared colour scale per row (K, V). Bins of 256 rows; L2 norm over head_dim, mean of the KV heads.")
    return save_fig(fig,"PHYSICAL_PAIR_MEMORIES_XRAY",k)

def fig2(k=2):
    xm=xray_metas();panels=[]
    j=_npz(RUNS/"build_store"/"xray"/"S1-S5_joint.npz");c=_npz(ASK_DIR/"store"/"xray"/"C11.npz")
    if j is None or c is None or not (_xray_ok(xm.get("S1-S5_joint")) and _xray_ok(xm.get("C11"))):raise RuntimeError("S1–S5 joint or C11 X-ray record missing")
    panels=[("S1–S5 joint · K",j[0],"process 1"),("S1–S5 joint · V",j[1],"process 1"),("C11 alone · K",c[0],"process 2"),("C11 alone · V",c[1],"process 2")]
    B=LIVE.get("build") or {};c11=B.get("C11") or {};au=((LIVE.get("ask") or {}).get("independence") or {}).get("c11_memory_audit") or {}
    fig=fig_base(k,"S1–S5 joint memory and the new cartridge C11 — 80-layer K/V X-ray",
                 f"Left: S1–S5 physically joined in process 1. Right: C11 mounted ALONE in process 2 · C11 SHA-256 {str(c11.get('cartridge_sha256'))[:16]}… · C11 is not a merged map of C01–C10")
    for i,(t,arr,who) in enumerate(panels):
        ax=fig.add_axes([.07+i*.225,.22,.18,.56]);b=binned(arr,64)
        im=ax.imshow(b,aspect="auto",origin="lower",cmap="Blues" if i<2 else "Greens",vmin=np.percentile(b,2),vmax=np.percentile(b,98),interpolation="nearest")
        ax.set_title(f"{t} · {arr.shape[1]:,} rows",fontsize=10.5,color=INK if i<2 else C11_COLOR);ax.set_xticks([]);ax.set_xlabel(who,fontsize=9.5,color=MUTED)
        ax.set_yticks([0,40,79]) if i==0 else ax.set_yticks([])
        if i==0:ax.set_ylabel("layer",fontsize=10)
        cb=fig.colorbar(im,cax=fig.add_axes([.07+i*.225+.185,.22,.006,.56]));cb.ax.tick_params(labelsize=7.5)
    ftext(fig,.07,.145,f"C11 memory audit (process 2): rows {au.get('rows')} = expected {au.get('rows_expected')} · K/V bytes {au.get('memory_logical_bytes')} = expected {au.get('expected_kv_bytes')} · "
          f"allocated above the model-only baseline {au.get('allocated_above_model_baseline')} B · result {'PASS' if au.get('pass') else 'FAIL'}",fontsize=10,color=INK2,va="center")
    fig_footer(fig,k,"Bins of 64 rows. C11 holds only the rows of its own body: the model-generated general final synthesis, written with the unchanged CUT3 path (TEST709 forge_stream).")
    return save_fig(fig,"S1_S5_JOINT_AND_C11_XRAY",k)

def fig3(k=3):
    rows=LIVE.get("questions") or []
    if not rows or not any(q["answers"] for q in rows):raise RuntimeError("no answer of the sealed panel is recorded")
    fig=fig_base(k,"Five fixed questions — C11 alone vs the model without any document",
                 "Automatic indicator per raw answer (text rules sealed before generation) — the full raw answers are in the interface, RUN_SUMMARY.txt and the records; the reader judges them.")
    for j,lab in enumerate(("C11 alone (process 2)","no document")):fig.text(.60+j*.2,.825,lab,fontsize=12.5,weight="bold",color=C11_COLOR if j==0 else INK2,ha="center")
    for i,q in enumerate(rows):
        y=.735-i*.128
        fig.text(.04,y,q["id"],fontsize=14,weight="bold",color=INK,va="center")
        w=textwrap.wrap(q["text"],70);ftext(fig,.085,y+.012,"\n".join(w[:3])+("…" if len(w)>3 else ""),xmax=.50,minsize=6.5,fontsize=9.2,color=INK2,va="center",linespacing=1.2)
        ftext(fig,.085,y-.045,"expected (PDF): "+short(q["verifiable_answer"],80),xmax=.50,minsize=6.5,fontsize=8.4,color=MUTED,va="center",style="italic")
        for j,c in enumerate(("C11","NO_DOCUMENT")):
            a=q["answers"].get(c) or {};st=a.get("evaluation","NOT PRODUCED")
            fig.text(.60+j*.2,y+.016,st.replace("_"," "),fontsize=12 if len(st)<12 else 10.5,weight="bold",color=STATUS_COL.get(st,MUTED),ha="center",va="center")
            fig.text(.60+j*.2,y-.02,f"finish {a.get('finish_reason','—')} · {a.get('n_generated','—')} tokens",fontsize=8.8,color=MUTED,ha="center",va="center")
    fig_footer(fig,k,"CORRECT / INCORRECT / UNCLEAR / INCOMPLETE / UNVERIFIED FINISH = automatic indicator, not expert verification. A correct no-document answer may come from pre-training.")
    return save_fig(fig,"FIVE_QUESTIONS_C11_VS_NO_DOCUMENT",k)
FIG_FUNCS=OrderedDict([("F1",fig1),("F2",fig2),("F3",fig3)])
def render_figures():
    """renders all figures on the CPU from this run's records (no GPU use)"""
    if not LIVE:LIVE.update(live_record())
    out={};errs={}
    for i,(key,fn) in enumerate(FIG_FUNCS.items(),1):
        t=time.perf_counter()
        try:rec=fn(i);out[key]=rec;FIG_FILES[key]=rec;_OUT.write(f"  figure {i}/{len(FIG_FUNCS)} · {rec['pixels'][0]}×{rec['pixels'][1]} JPEG · {rec['jpg_bytes']/1e6:.1f} MB · {time.perf_counter()-t:.1f} s · {Path(rec['jpg']).name}\n")
        except Exception as ex:errs[key]=f"{type(ex).__name__}: {ex}";FIG_FILES.pop(key,None);flog(f"FIGURE {i} NOT GENERATED {traceback.format_exc()[-1500:]}");_OUT.write(f"  figure {i} NOT GENERATED · {errs[key]}\n")
        _OUT.flush()
    dump_json(SESSION_DIR/"FIGURES_MANIFEST.json",dict(session=SESSION_ID,utc=utc_now(),data_source="this run's records only",provenance=LIVE.get("provenance"),figures=FIG_FILES,not_generated=errs))
    slog("FIGURES",f"{len(out)} rendered",not_generated=errs);return out,errs

# ---------------------------------------------------------------------------------------------------------------------
# research summary, downloadable artifacts (actual files of this run; the Siemens PDF and the .pt tensors are never packaged)
# ---------------------------------------------------------------------------------------------------------------------
RUN_SUMMARY=SESSION_DIR/"RUN_SUMMARY.txt"
ZIP_PATH=SESSION_DIR/f"{SESSION_ID}_AKBASCORE_SIEMENS_TEST719_ALL_RESEARCH_ARTIFACTS.zip";MANIFEST=SESSION_DIR/"SHA256_MANIFEST.json"
def pct(x):return "—" if x is None else f"{100*x:.0f} %"
def write_run_summary():
    v=STATE.get("verification") or {};L=[];a=L.append;Lr=LIVE if LIVE else {};B=build_result();A=ask_result();ph=phases()
    a(f"{APP_TITLE}\n{VERSION_NOTE}\nsession {SESSION_ID} · started {SESSION_INFO['started_local']} ({INIT['started_utc']} UTC) · written {local_now()}")
    fs=INIT.get("final") or {}
    if fs:
        a(f"FINAL STATUS  {fs.get('headline')}\n  scientific result: {fs.get('result')}\n  C11 isolation    : {fs.get('isolation')}")
        for g in fs.get("gaps") or []:a(f"  reported gap · {g.get('step')} · {g.get('kind')} · {g.get('gap')}")
    a(f"PROVENANCE  {Lr.get('provenance','n/a')}"+("" if Lr.get("provenance")=="GPU_REAL" else "  — NOT A REAL A100 RESULT; nothing in this file may be presented as an experimental result")+"\n")
    a("EXPERIMENT  TEST719 — five physical CUT3 pair memories → five question-independent syntheses (S1–S5) → S1–S5 physically joined → final synthesis → new cartridge C11;")
    a("            five fixed questions to C11 alone (new Python process) and to the same model without any document")
    a(f"ENGINE      716.py git blob {LOCKS['716.py']} · 709.py {LOCKS['709.py']} (executed unchanged; only MAX_NEW is set per call)")
    for nm,lab in (("BUILD","process 1"),("ASK","process 2")):
        p=ph.get(nm) or {};a(f"            {lab}: {p.get('start_utc')} → {p.get('end_utc')} UTC · exit {p.get('exit_code')} · pid {p.get('pid')} · {p.get('seconds')} s · status {p.get('status')}")
    mi=MODEL_IDENTITY
    a(f"MODEL       {MODEL_ID} · NF4 4-bit, BF16 compute, frozen · pinned snapshot {(B.get('model_pin') or {}).get('commit')} · Hub main {mi.get('hub_main_commit')}")
    a(f"            first public release {MODEL_RELEASE['date']} — {MODEL_RELEASE['source']} — {MODEL_RELEASE['url']} ({MODEL_RELEASE['checked']})")
    a(f"DOCUMENT    {DOC_TITLE} · edition {DOC_EDITION_MARK} (printed on {DOC.get('edition_mark_pages')} of {DOC.get('pages')} pages — verified on the document)")
    a(f"            order no. {DOC.get('order_number')} · software {DOC.get('software_version')} · {DOC.get('bytes')} bytes · SHA-256 {DOC.get('sha256')}")
    a(f"            downloaded {DOC.get('download_start_utc')} → {DOC.get('download_end_utc')} UTC from {PDF_URL}")
    a(f"            {PDF_POLICY} ({PDF_TERMS_URL})")
    a("\nINITIALIZATION (this session)")
    for st in INIT["steps"]:a(f"  ✓ {st['step']:<13} {st['seconds']:>9.1f} s  {st['title']}")
    if INIT.get("failed"):a(f"  ✗ {INIT['failed']['step']}  {INIT['failed']['error']}  (last successful: {INIT['failed']['last_successful_step']})")
    seal=jload(SEAL_FILE,{}) or {}
    if seal:a(f"\nQUESTION PANEL  sealed {seal.get('sealed_utc')} (before any model load) · questions SHA-256 {seal.get('questions_sha256')} · build config SHA-256 {seal.get('build_config_sha256')}")
    if B:
        a(f"\nPROCESS 1 — PHYSICAL MEMORY RECORD · status {B.get('status')}"+(f" · {B.get('error')}" if B.get("error") else ""))
        for b in B.get("sources") or []:a(f"  {b['id']}  PDF pages {b['page_range'][0]}–{b['page_range'][1]} · {b['body_tokens']} tokens · SHA-256 {b['cartridge_sha256']}")
        for p in B.get("pairs") or []:
            ap=p.get("append") or {};sy=p.get("synthesis") or {};em=sy.get("end_marker") or {};fe=sy.get("finish_evidence") or {}
            a(f"  {p['pair']} initialize({p['cartridges'][0]}) → append({p['cartridges'][1]}) · rows {ap.get('rows')} (expected {p.get('rows_expected')}) · {ap.get('pass_line') or 'append NOT verified'}")
            a(f"      synthesis {sy.get('status')} · finish {sy.get('finish_reason')} (forward passes {fe.get('forward_calls')}, last token {fe.get('last_observed_token_text')!r}) · END marker last line {em.get('at_end')} · "
              f"{sy.get('n_generated')} tokens (ceiling {sy.get('ceiling')}) · {sy.get('seconds')} s"+(f" · reason {sy.get('incomplete_reason')}" if sy.get("incomplete_reason") else ""))
        for s in B.get("S") or []:a(f"  {s['id']}  {s['body_tokens']} tokens · SHA-256 {s['cartridge_sha256']}")
        j=B.get("joint") or {}
        if j:
            fi=j.get("final") or {};em=fi.get("end_marker") or {}
            a(f"  S1–S5 joint · {j.get('rows')} rows · appends verified {[x.get('verified') for x in j.get('appends',[])]}")
            a(f"      final synthesis {fi.get('status')} · finish {fi.get('finish_reason')} · END marker last line {em.get('at_end')} · {fi.get('n_generated')} tokens (ceiling {fi.get('ceiling')}) · {fi.get('seconds')} s"+(f" · reason {fi.get('incomplete_reason')}" if fi.get("incomplete_reason") else ""))
        c=B.get("C11") or {};a(f"  C11  {c.get('body_tokens','—')} tokens · SHA-256 {c.get('cartridge_sha256','NOT WRITTEN')}")
    if A:
        ind=A.get("independence") or {}
        a(f"\nPROCESS 2 — C11 ALONE IN A NEW PROCESS (same Colab VM) · status {A.get('status')}"+(f" · {A.get('error')}" if A.get("error") else ""))
        for k,lab in ISO_LABELS:a(f"  {'PASS' if (ind.get(k) or {}).get('pass') else 'FAIL'}  {lab}")
        au=ind.get("c11_memory_audit") or {}
        if au:a(f"  memory audit: {au.get('what_is_proven')}")
    if Lr.get("questions") and A:
        a("\nTHE FIVE FIXED QUESTIONS — FULL RAW ANSWERS (unedited; the indicator is automatic, not expert verification)")
        for q in Lr["questions"]:
            pe=q.get("pdf_evidence") or {}
            a(f"\n  {q['id']}  {q['text']}\n      region {q.get('region')} · expected (PDF): {q['verifiable_answer']} · source: {q['source']} · PDF check before model load: {'verified' if pe.get('verified') else 'NOT verified'}")
            for ev in pe.get("evidence",[]):
                f=ev.get("found") or {}
                if ev["cartridge"]=="EVERY":a(f"      evidence: found in {len(f)}/{N_CART} cartridges")
                elif f:a(f"      evidence: {f['cartridge']} PDF page {f['pdf_page']} · “{f['snippets'][-1][:200]}”")
            for c,lab in (("C11","C11 ALONE"),("NO_DOCUMENT","NO DOCUMENT")):
                r=q["answers"].get(c)
                if not r:a(f"      {lab}: not produced");continue
                a(f"      {lab} · {r['status']} · finish {r.get('finish_reason')} · {r['n_generated']} tokens (ceiling {r['ceiling']}) · {r['seconds']} s · indicator {r['evaluation']} ({r['why']})")
                a("        "+str(r["text"]).replace("\n","\n        "))
    if INIT.get("ready") or (Lr.get("questions") and A and A.get("answers")):
        fin_p=RUNS/"build_store"/"synthesis"/"FINAL.txt"
        if fin_p.is_file():a("\nC11 BODY TEXT (general final synthesis, model-generated)\n  "+fin_p.read_text(encoding="utf-8").replace("\n","\n  "))
    if any(r.get("origin")=="user" for r in STATE["qa"]+STATE["controls"]):
        a("\nQUESTIONS ASKED IN THE INTERFACE (not part of the sealed panel)")
        for r in STATE["qa"]+STATE["controls"]:
            if r.get("origin")=="user":a(f"  [{r['cartridge'] or 'no document'}] {r['question']}\n      {r['status']} · finish {r['finish_reason']} → {r['raw']}")
    a(f"\nLIVE VERIFICATION  {v.get('passed','—')}/{v.get('total','—')} passed")
    for i in v.get("items",[]):a(f"  {'PASS' if i['passed'] else 'FAIL'}  {i['name']}  {i['detail'] if isinstance(i['detail'],str) else json.dumps(i['detail'],ensure_ascii=False)}")
    a(f"\n{PREV_TITLE}\n{PREV_TEXT}\n{PREV_SEE}\n(Previously published research — not a result of this experiment.)")
    a("\nRESEARCH LINEAGE\n"+"\n".join(f"  {t}: {u}" for t,u in LINEAGE)+"\n  This experiment: unpublished — no DOI.")
    a("\nHISTORICAL REFERENCE (earlier runs, not this session): "+", ".join(f"{n} blob {LOCKS[n]}" for n in HISTORICAL))
    a("\nSCOPE  C11 is a new physical memory written from a model-generated general synthesis, not a lossless merge of C01–C10. Five questions are a live "
      "demonstration, not a statistic; the indicator is an automatic text rule. A correct no-document answer may come from pre-training. Process 2 is a new "
      "process on the same Colab VM, not a separate machine.")
    a(f"{AUTHOR} · {ORG} · {LICENSE_NAME} · {COPYRIGHT}")
    RUN_SUMMARY.write_text("\n".join(L)+"\n",encoding="utf-8");return str(RUN_SUMMARY)
def session_record():
    return dict(session=SESSION_INFO,app=APP_TITLE,version_note=VERSION_NOTE,sources=SOURCES,program=PROGRAM,locks=LOCKS,initialization=INIT,phases=phases(),
                architecture=engine_architecture(),document=DOC,model=MODEL_IDENTITY,mounted=STATE["mount"],operations=STATE["ops"],qa=STATE["qa"],controls=STATE["controls"],
                weight_checks=STATE["weight_checks"],disk_checks=STATE["disk_checks"],verification=STATE["verification"],figures=FIG_FILES,lineage=LINEAGE,
                previously_demonstrated=dict(title=PREV_TITLE,text=PREV_TEXT,see=PREV_SEE),
                scope="C11 is written from a model-generated synthesis; five questions are a demonstration; the indicator is automatic; the Siemens PDF is not redistributed.")
def _category(rel):
    if rel.startswith("historical_reference_not_this_session"):return "HISTORICAL (published earlier run, not this session)"
    if rel.startswith("figures"):return "LIVE figure"
    if rel.startswith("records_process1"):return "LIVE process 1 record"
    if rel.startswith("records_process2"):return "LIVE process 2 record"
    if rel.startswith("records_console"):return "LIVE process output (both processes)"
    if rel.startswith("program"):return "PROGRAM file of this run"
    return "LIVE session record"
def _run_records():
    """process records read directly from the experiment directories (no .pt tensor, no PDF copy, no engine working directory)"""
    out=[]
    def add(base,arc):
        base=Path(base)
        if base.is_file():out.append((base,arc));return
        if not base.is_dir():return
        for p in sorted(base.rglob("*")):
            if p.is_file() and p.suffix not in (".pt",".pdf",".tmp"):out.append((p,f"{arc}/{p.relative_to(base)}"))
    add(RUNS/"build_store","records_process1/build_store");add(RUNS/"build"/"events.jsonl","records_process1/events.jsonl");add(RUNS/"console","records_console")
    for f in ("SEAL.json","pdf_source_check.json","PHASES.json"):add(RUNS/f,f"records_process1/{f}")
    for f in ("handoff.json","C11.sha256"):add(RUNS/"handoff"/f,f"records_process1/handoff/{f}")
    add(RUNS/"engine_dir_after_build"/"TEST716_results.json","records_process1/TEST716_results.json")
    add(ASK_DIR/"store","records_process2/store");add(ASK_DIR/"events.jsonl","records_process2/events.jsonl")
    for name in PROGRAM:add(PROGRAM_DIR/name,f"program/{name}")
    return out
def package_session():
    """Download-All ZIP: three figures (JPG/PNG/PDF), session logs, process records, verification records, program files,
    historical files (separate folder) and SHA256_MANIFEST.json — never the Siemens PDF, never a .pt tensor"""
    dump_json(SESSION_DIR/"SESSION_RECORD.json",session_record());write_run_summary()
    files=[(p,str(p.relative_to(SESSION_DIR))) for p in sorted(SESSION_DIR.rglob("*")) if p.is_file() and p.suffix not in (".zip",".tmp") and p!=MANIFEST
           and not str(p.relative_to(SESSION_DIR)).startswith(("records_process1","records_process2","records_console","program"))]+_run_records()
    man=OrderedDict((arc,dict(sha256=sha_file(p),bytes=p.stat().st_size,category=_category(arc))) for p,arc in files)
    dump_json(MANIFEST,dict(session=SESSION_ID,utc=utc_now(),note="The Siemens PDF is not included (copyright Siemens AG); its URL and SHA-256 are in SOURCE_DOCUMENT_RECORD.json. Cartridge tensors (.pt) are not included; their SHA-256 are in the records.",files=man))
    tmp=ZIP_PATH.with_suffix(".zip.tmp")
    with zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED) as z:
        for p,arc in files+[(MANIFEST,"SHA256_MANIFEST.json")]:z.write(p,arcname=f"{SESSION_ID}/{arc}")
    with zipfile.ZipFile(tmp) as z:
        if z.testzip():raise RuntimeError("ZIP check failed")
    tmp.replace(ZIP_PATH);slog("PACKAGE",ZIP_PATH.name,files=len(files)+1,bytes=ZIP_PATH.stat().st_size);return str(ZIP_PATH)
def copy_records_for_download():
    """after process 2: plain copies of the process records inside the session folder, so the interface can offer them"""
    for p,arc in _run_records():
        d=SESSION_DIR/arc;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,d)
def download_items():
    items=[("Run summary (.txt)",RUN_SUMMARY),("Session log (.log)",SESSION_LOG),("Session events (.jsonl)",SESSION_EVENTS),
           ("Process 1 output (.log)",SESSION_DIR/"records_console"/"BUILD.log"),("Process 1 output with UTC time stamps (.tsv)",SESSION_DIR/"records_console"/"BUILD_with_UTC_timestamps.tsv"),
           ("Process 1 result (.json)",SESSION_DIR/"records_process1"/"build_store"/"build_result.json"),
           ("Process 2 output (.log)",SESSION_DIR/"records_console"/"ASK.log"),("Process 2 result (.json)",SESSION_DIR/"records_process2"/"store"/"ask_result.json"),
           ("C11 body text — final synthesis (.txt)",SESSION_DIR/"records_process1"/"build_store"/"synthesis"/"FINAL.txt"),
           ("Question panel source check on the PDF (.json)",PANEL_FILE),("Live measurements (.json)",LIVE_MEAS),
           ("Source document record (.json)",DOC_FILE),("Verification record (.json)",VERIFY_FILE),("Initialization record (.json)",INIT_FILE),
           ("Interface questions and answers (.jsonl)",SESSION_QA),("Figure manifest (.json)",SESSION_DIR/"FIGURES_MANIFEST.json"),("SHA-256 manifest (.json)",MANIFEST)]+\
          [(f"Pair synthesis P{k} (.txt)",SESSION_DIR/"records_process1"/"build_store"/"synthesis"/f"P{k}.txt") for k in range(1,N_PAIRS+1)]+\
          [(f"HISTORICAL · published {n} of an earlier run (not this session)",HIST_DIR/("HISTORICAL_"+n)) for n in HISTORICAL]
    return [(l,str(p)) for l,p in items if Path(p).is_file()]

# ---------------------------------------------------------------------------------------------------------------------
# AUTOMATIC INITIALIZATION — one start, every step real, stops at the first failure
# ---------------------------------------------------------------------------------------------------------------------
def _step_verify():
    v=compute_verification()
    for it in v["items"]:_OUT.write(f"  {'PASS' if it['passed'] else 'FAIL'}  {it['cls']:<9} {it['name']:<44} {short(it['detail'] if isinstance(it['detail'],str) else json.dumps(it['detail'],ensure_ascii=False),80)}\n")
    _OUT.write(f"  → scientific result: {v['result']}\n  → isolation of C11: {v['isolation']}\n  → formal gaps: {', '.join(v['formal_gaps']) or 'none'}\n");_OUT.flush()
    return dict(passed=v["passed"],total=v["total"],result=v["result"],isolation=v["isolation"],formal_gaps=v["formal_gaps"],provenance=v["provenance"])
def _step_figures():
    copy_records_for_download()
    out,errs=render_figures()
    if errs or len(out)!=len(FIG_FUNCS):raise RuntimeError(f"FIGURES: {len(out)}/{len(FIG_FUNCS)} generated · {errs}")
    return dict(figures=[Path(r["jpg"]).name for r in out.values()])
STEP_FUNCS=OrderedDict([("SOURCES",sources_step),("PREFLIGHT",preflight),("DOCUMENT",document_step),("PANEL",panel_step),("BUILD",build_step),
                        ("ASK",ask_step),("VERIFY",_step_verify),("READY_MEMORY",ready_memory),("FIGURES",_step_figures)])
# steps after the scientific computation: a failure there is recorded as a gap of the presentation and the run continues
NONFATAL=("VERIFY","READY_MEMORY","FIGURES")

def final_status():
    v=STATE.get("verification") or {};gaps=list(INIT.get("gaps") or [])
    for g in v.get("formal_gaps") or []:gaps.append(dict(step="VERIFY",kind="FORMAL",gap=g))
    missing=[k for k in FIGURES if k not in FIG_FILES]
    if missing and not any(g.get("step")=="FIGURES" for g in gaps):gaps.append(dict(step="FIGURES",kind="PRESENTATION",gap=f"figures not generated: {missing}"))
    res=v.get("result") or "NOT EVALUATED"
    head=("RESULT VALID" if res=="VALID" else "RESULT NOT VALID")+(" · C11 isolation supported" if str(v.get("isolation","")).startswith("SUPPORTED") else " · C11 isolation NOT supported")+\
         (" · no gaps" if not gaps else f" · {len(gaps)} reported gap(s)")
    INIT["final"]=dict(headline=head,result=res,isolation=v.get("isolation"),gaps=gaps,figures_missing=missing,provenance=LIVE.get("provenance"));return INIT["final"]

def init_failed(key,ex):
    tb=traceback.format_exc()
    INIT["failed"]=dict(step=key,title=INIT_STEPS[key],error=f"{type(ex).__name__}: {ex}",last_successful_step=INIT["last_ok"],utc=utc_now(),traceback=tb[-6000:],
                        last_process_lines=[f"{ts} {nm} {l}" for ts,_,nm,l in PROC_LINES[-40:]],last_heartbeat=(HEARTBEATS[-1] if HEARTBEATS else None),phases=phases())
    release_memory("initialization failed")
    slog("INIT_FAILED",key,error=INIT["failed"]["error"],last_successful_step=INIT["last_ok"],traceback=tb[-3000:])
    try:dump_json(INIT_FILE,INIT);package_session()
    except Exception as ex2:_OUT.write(f"  (failure package could not be written: {ex2})\n")
    banner(f"EXPERIMENT STOPPED — no result is available from this attempt and nothing here is reported as a success.\n"
           f"  failed step          : {key} · {INIT_STEPS[key]}\n  error                : {INIT['failed']['error']}\n"
           f"  last successful step : {INIT['last_ok'] or 'none'}\n  records              : {SESSION_DIR}\n  all files (ZIP)      : {ZIP_PATH if ZIP_PATH.is_file() else 'not written'}","█")

def run_initialization():
    banner(f"{APP_TITLE}\n{VERSION_NOTE} · session {SESSION_ID} · records in {SESSION_DIR}\n"
           "Automatic initialization: every step below is executed for real in this runtime; nothing is precomputed.","#")
    INIT["gaps"]=[]
    for key,fn in STEP_FUNCS.items():
        t0=step_begin(key)
        try:info=fn()
        except BaseException as ex:
            if key in NONFATAL and not isinstance(ex,KeyboardInterrupt):
                err=f"{type(ex).__name__}: {ex}";INIT["gaps"].append(dict(step=key,kind="PRESENTATION",gap=err,utc=utc_now(),traceback=traceback.format_exc()[-3000:]))
                slog("STEP_GAP",key,error=err);_OUT.write(f"──── ⚠ {key} not completed — recorded as a gap of the final report, the run continues: {err}\n");_OUT.flush()
                if key=="READY_MEMORY":release_memory("interface memory not available")
                continue
            init_failed(key,ex);raise RuntimeError(f"INITIALIZATION FAILED at {key}: {type(ex).__name__}: {ex}") from ex
        step_done(key,t0,result=info)
    INIT["ready"]=True;INIT["ready_utc"]=utc_now();INIT["total_seconds"]=round(time.perf_counter()-INIT["started"],1)
    f=final_status();dump_json(INIT_FILE,INIT)
    try:package_session()
    except Exception as ex:INIT["gaps"].append(dict(step="PACKAGE",kind="PRESENTATION",gap=f"{type(ex).__name__}: {ex}"));f=final_status()
    gl="".join(f"\n  gap · {g['step']} · {g['kind']} · {short(g['gap'],150)}" for g in f["gaps"])
    banner(f"EXPERIMENT FINISHED in {INIT['total_seconds']/60:.1f} min · {f['headline']} · provenance {LIVE.get('provenance')}\n"
           f"  scientific result : {f['result']}\n  C11 isolation     : {f['isolation']}\n  interface memory  : {'C11 mounted ('+format(STATE['mount']['rows'],',')+' rows)' if STATE.get('mount') else 'not available (questions in the interface are disabled)'}"+gl,"#")
    slog("FINISHED",f["headline"],seconds=INIT["total_seconds"],gaps=len(f["gaps"]))
    return True
# ===== END OF PART 2/3 =====
# ===== PART 3/3 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 3 — Gradio Interface, User Interaction, Research Presentation and Session Logging
# Same working method and interface as the previous Qwen2.5-72B / Siemens demonstrations: start-up runs everything
# automatically (sources, preflight, the original Siemens PDF, the sealed question panel, process 1, process 2, verification,
# the C11 memory, three JPEG figures, ZIP), then the Gradio interface opens with the five raw answer pairs, the figures,
# individual downloads and the package. The interface calls the engine, records and displays. It never computes or edits an answer.
# =====================================================================================================================
# TEST719 program files (part 2 of 2): process 1 (build) and process 2 (C11 alone). Written here with their SHA-256 checked;
# they run as separate Python processes started by step [5] and step [6].
_program_write('TEST719_demo_build.py',r'''# AKBASCORE TEST719-DEMO — PROCESS 1 (build). Real Qwen2.5-72B, unchanged TEST709 engine via unchanged TEST716 setup.
# C01-C10 (716) -> five physical pairs (initialize Ca -> append Cb, 80-layer exact SHA) -> question-independent general pair
# syntheses -> S1-S5 cartridges -> physical S1-S5 joint memory -> general final synthesis -> C11 cartridge (CUT3 WRITE).
# The five demo questions and their expected answers are never read by this process (the build has no access to them).
import os, sys, io, re, gc, json, time, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import TEST719_common as C

RUNS = Path(os.environ.get('T719_RUNS', '/content/T719_RUNS'))
CART716 = Path('/content/AKBASCORE_TEST714/cartridges'); ROOT716 = Path('/content/AKBASCORE_TEST714')
CFG = json.loads((C.HERE / 'TEST719_demo_build_config.json').read_text(encoding='utf-8'))   # prompts, pairs, ceilings only (no questions)

def end_marker(text):
    t = text.rstrip()
    return {'present': 'END OF SYNTHESIS' in text, 'at_end': t.endswith('END OF SYNTHESIS') or t.endswith('END OF SYNTHESIS.')}

def synthesis_status(r, em):
    """Acceptance of a synthesis as cartridge text.
    ACCEPTED  : the end of generation is observed as a stop token (EOS) — or, when the three-way observation cannot confirm it,
                the loop stopped below the ceiling (the unchanged 709 loop stops only at a stop token or at MAX_NEW); the latter is
                flagged FINISH_UNVERIFIED. A missing or misplaced END OF SYNTHESIS line is a format flag, not a reason to stop.
    INCOMPLETE: the safety ceiling was reached (text cut) — no cartridge is written from it."""
    r['generation_status'] = r['status']; flags = []
    if r.get('finish_reason') == 'CEILING' or r['status'] == 'INCOMPLETE':
        return 'INCOMPLETE', ['CEILING_REACHED'], False
    if r.get('finish_reason') != 'EOS':
        flags.append('FINISH_UNVERIFIED')
    if not em['present']:
        flags.append('END_MARKER_MISSING')
    elif not em['at_end']:
        flags.append('END_MARKER_NOT_LAST_LINE')
    return ('COMPLETE' if not flags else 'ACCEPTED_WITH_FLAGS'), flags, True

def npz_bytes(**a):
    import numpy as np
    b = io.BytesIO(); np.savez_compressed(b, **a); return b.getvalue()

class Build:
    def __init__(self):
        import torch
        self.torch = torch; self.prov = C.provenance(torch); self.mode = self.prov['mode']
        self.log = C.EventLog(RUNS / 'build' / 'events.jsonl'); self.store = C.Store(RUNS / 'build_store', None, self.mode, self.log)
        self.eng = C.Engine(self.log, self.mode); self.res = {'status': 'STARTED', 'provenance': self.prov, 'runtime': C.runtime_identity(), 'pairs': [], 'stages': []}
        self.t0 = time.time()

    def save(self):
        self.store.put_json('build_result.json', self.res, 'result')

    def stage(self, name, fn, *a):
        st = C.utc(); t = time.time(); self.log.ev('STAGE_START', name)
        try:
            return fn(*a)
        finally:
            self.res['stages'].append({'stage': name, 'start_utc': st, 'end_utc': C.utc(), 'seconds': round(time.time() - t, 1)})
            self.log.ev('STAGE_END', name, seconds=round(time.time() - t, 1)); self.save()

    def xray(self, h, label):
        K, V, meta = self.eng.xray(h['m'], label)
        self.store.put_bytes(f'xray/{label}.npz', npz_bytes(K=K, V=V), 'xray'); self.store.put_json(f'xray/{label}.json', meta, 'xray_meta'); return meta

    def base_check(self, what):
        self.eng.free_cached(); m = self.eng.mem()
        if m['allocated'] > self.base['allocated'] + 64 * 2 ** 20:      # recorded, not a reason to stop (no effect on the computation)
            self.res.setdefault('memory_notes', []).append({'after': what, 'allocated_above_baseline': m['allocated'] - self.base['allocated'], 'utc': C.utc()})
            self.log.ev('MEMORY_NOTE', f'memory above the model baseline after {what}', allocated_above_baseline=m['allocated'] - self.base['allocated'])
        return m['allocated']

    def with_memory_recovery(self, name, fn, *a):
        """runs a stage; after a GPU memory failure (709 GPU_SAFETY_STOP or CUDA OOM) the partial memory is dropped, unused cached
        memory is released and the stage is rebuilt from the SHA-checked cartridges with the next memory profile (smaller CUT3 chunk,
        then a smaller reserve). Integrity checks are identical in every attempt."""
        for i, (chunk, reserve) in enumerate(C.MEMORY_LADDER):
            self.eng.set_memory_profile(chunk, reserve); err = None
            try:
                out = self.stage(name if i == 0 else f'{name}_retry{i}', fn, *a)
                self.res.setdefault('memory_profile', {})[name] = {'chunk_tokens': chunk, 'reserve_gib': reserve, 'attempt': i + 1}
                return out
            except Exception as e:
                if not C.is_memory_error(e) or i == len(C.MEMORY_LADDER) - 1:
                    raise
                err = f'{type(e).__name__}: {e}'
            gc.collect(); self.eng.free_cached(); m = self.eng.mem()        # the failed attempt's frames are gone here
            nxt = C.MEMORY_LADDER[i + 1]
            self.res.setdefault('memory_recoveries', []).append({'stage': name, 'attempt': i + 1, 'error': err, 'utc': C.utc(), 'free_after_cleanup_gib': round(m['free'] / C.GIB, 2),
                                                                 'next_chunk_tokens': nxt[0], 'next_reserve_gib': nxt[1]})
            self.log.ev('MEMORY_RECOVERY', f'{name}: {err[:160]} - memory released, stage rebuilt from the cartridges', next_chunk_tokens=nxt[0], next_reserve_gib=nxt[1],
                        free_gib=round(m['free'] / C.GIB, 2))

    def forge(self, bid, text, meta):
        # S1-S5 / C11 come from THIS run's generated text: a cartridge left over from an earlier run is removed first, so the
        # 716-style reuse test (file SHA + token count) can never pick up a stale synthesis cartridge of equal length.
        for ext in ('.pt', '.sha256'):
            (CART716 / (bid + ext)).unlink(missing_ok=True)
        rec = self.eng.forge_register(bid, text, meta)
        if rec['reused']:
            raise C.StageError('STALE_SYNTHESIS_CARTRIDGE_REUSED ' + bid)
        for ext in ('.pt', '.sha256'):
            self.store.put_file(f'cartridges/{bid}{ext}', CART716 / (bid + ext), 'cartridge')
        self.store.put_json(f'cartridges/{bid}.book.json', rec, 'book'); return rec

    def gen(self, h, prompt, ceiling, label):
        r = self.eng.answer(h['m'], prompt, ceiling, 9.0, label)
        self.log.ev('GENERATION', label, status=r['status'], n=r['n_generated'], seconds=r['seconds'], peak_gib=round(r['peak'] / C.GIB, 2))
        return r

    # ------------------------------------------------------------------ stages
    def boot(self):
        self.res['model_pin'] = C.pin_model_revision(self.log, self.mode)
        info = self.eng.boot(model_only=False); E = self.eng.E
        self.base = self.eng.mem(); info['baseline'] = self.base
        books = [dict(b) for b in E['R']['books']]; self.res['sources'] = books; self.res['sentinel_before'] = E['before']
        self.res['engine'] = {k: v for k, v in info.items() if k != 'books'}
        self.res['reuse_lines'] = [l for l in self.eng.tee.lines if 'REUSE_SHA_VERIFIED' in l]
        for b in books:
            for ext in ('.pt', '.sha256'):
                self.store.put_file(f'cartridges/{b["id"]}{ext}', CART716 / (b['id'] + ext), 'cartridge')

    def pair(self, k):
        a, b = CFG['pairs'][k]; bounds = self.res['sources']; ia, ib = int(a[1:]) - 1, int(b[1:]) - 1
        rec = {'pair': f'P{k + 1}', 'cartridges': [a, b]}; h = {'m': None}
        h['m'], rec['mount'] = self.eng.mount(a)
        rec['xray_alone'] = self.xray(h, f'P{k + 1}_{a}_alone')
        h['m'], rec['append'] = self.eng.append(h['m'], b)                     # PASS APPEND_ALL_80_LAYERS_EXACT_SHA256 verified
        rec['rows_expected'] = int(self.eng.E['P']) + bounds[ia]['body_tokens'] + bounds[ib]['body_tokens']
        if rec['append']['rows'] != rec['rows_expected']:
            raise C.StageError('PAIR_ROWS ' + rec['pair'])
        rec['kv_gib'] = round(self.eng.kv_bytes(h['m']) / C.GIB, 3)
        seal = self.eng.seals(h['m']); self.store.put_json(f'seals/P{k + 1}.json', seal, 'seal'); rec['seal_seconds'] = seal['seconds']
        rec['xray_joint'] = self.xray(h, f'P{k + 1}_{a}+{b}_joint')
        (a1, a2), (b1, b2) = bounds[ia]['page_range'], bounds[ib]['page_range']
        prompt = CFG['synthesis_prompts']['pair'].format(a=a, b=b, a1=a1, a2=a2, b1=b1, b2=b2)
        syn = self.gen(h, prompt, CFG['ceilings']['pair_synthesis'], f'SYNTHESIS_P{k + 1}')
        syn.update({'prompt': prompt, 'mounted': [a, b], 'memory': 'JOINT_PHYSICAL_PAIR', 'end_marker': end_marker(syn['text'])})
        syn['status'], syn['flags'], syn['accepted'] = synthesis_status(syn, syn['end_marker']); syn['incomplete_reason'] = ','.join(syn['flags']) or None
        self.store.put_json(f'synthesis/P{k + 1}.json', syn, 'synthesis'); self.store.put_text(f'synthesis/P{k + 1}.txt', syn['text'], 'synthesis_text')
        rec['memory_profile'] = {'chunk_tokens': self.eng.E['CHUNK'], 'reserve_gib': self.eng.E['GPU_RESERVE_GIB']}
        rec['synthesis'] = {k2: syn[k2] for k2 in ('status', 'accepted', 'flags', 'generation_status', 'incomplete_reason', 'finish_reason', 'finish_evidence', 'end_marker', 'n_generated', 'ceiling', 'seconds', 'tok_per_s', 'peak', 'sha256')}
        self.eng.release(h); rec['released_alloc'] = self.base_check(rec['pair'])
        self.res['pairs'] = [p for p in self.res['pairs'] if p['pair'] != rec['pair']] + [rec]
        if not syn['accepted']:   # no cartridge is ever written from a cut (ceiling) synthesis
            raise C.StageError(f"PAIR_SYNTHESIS_NOT_COMPLETE P{k + 1}: {syn['status']} ({syn['incomplete_reason']}, finish {syn['finish_reason']}, {syn['n_generated']} tokens, ceiling {syn['ceiling']})")

    def joint(self):
        recs = []
        for k in range(5):
            syn = self.store.get_json(f'synthesis/P{k + 1}.json'); a, b = CFG['pairs'][k]
            if not syn.get('accepted'):
                raise C.StageError(f'PAIR_SYNTHESIS_NOT_COMPLETE P{k + 1}')
            recs.append(self.forge(f'S{k + 1}', syn['text'], {'kind': 'pair synthesis cartridge', 'source_pair': [a, b], 'synthesis_status': syn['status']}))
        self.res['S'] = recs; h = {'m': None}; apps = []
        h['m'], m1 = self.eng.mount('S1')
        for k in range(1, 5):
            h['m'], ar = self.eng.append(h['m'], f'S{k + 1}'); apps.append(ar)
        exp = int(self.eng.E['P']) + sum(r['body_tokens'] for r in recs)
        if self.eng.rows(h['m']) != exp:
            raise C.StageError('JOINT_S_ROWS')
        seal = self.eng.seals(h['m']); self.store.put_json('seals/S_joint.json', seal, 'seal')
        xm = self.xray(h, 'S1-S5_joint')
        fin = self.gen(h, CFG['synthesis_prompts']['final'], CFG['ceilings']['final_synthesis'], 'FINAL_SYNTHESIS')
        fin.update({'prompt': CFG['synthesis_prompts']['final'], 'mounted': ['S1', 'S2', 'S3', 'S4', 'S5'], 'memory': 'JOINT_PHYSICAL_S1-S5', 'end_marker': end_marker(fin['text'])})
        fin['status'], fin['flags'], fin['accepted'] = synthesis_status(fin, fin['end_marker']); fin['incomplete_reason'] = ','.join(fin['flags']) or None
        self.store.put_json('synthesis/FINAL.json', fin, 'synthesis'); self.store.put_text('synthesis/FINAL.txt', fin['text'], 'synthesis_text')
        self.res['joint'] = {'rows': exp, 'appends': [{k2: x[k2] for k2 in ('bid', 'old_rows', 'rows', 'verified', 'pass_line', 'seconds')} for x in apps],
                             'xray': xm, 'memory_profile': {'chunk_tokens': self.eng.E['CHUNK'], 'reserve_gib': self.eng.E['GPU_RESERVE_GIB']},
                             'final': {k2: fin[k2] for k2 in ('status', 'accepted', 'flags', 'generation_status', 'incomplete_reason', 'finish_reason', 'finish_evidence', 'end_marker', 'n_generated', 'ceiling', 'seconds', 'tok_per_s', 'peak', 'sha256')}}
        self.eng.release(h); self.base_check('joint S1-S5')
        if not fin['accepted']:   # C11 is never written from a cut (ceiling) final synthesis
            raise C.StageError(f"FINAL_SYNTHESIS_NOT_COMPLETE: {fin['status']} ({fin['incomplete_reason']}, finish {fin['finish_reason']}, {fin['n_generated']} tokens, ceiling {fin['ceiling']}) - C11 not written")

    def c11(self):
        fin = self.store.get_json('synthesis/FINAL.json')
        if not fin.get('accepted'):
            raise C.StageError('FINAL_SYNTHESIS_NOT_COMPLETE - C11 not written')
        rec = self.forge('C11', fin['text'], {'kind': 'C11 general synthesis cartridge',
                                              'provenance_text': 'model-generated general synthesis of five physical pairs -> physical S1-S5 joint memory -> final general synthesis -> CUT3 WRITE',
                                              'not_a_lossless_physical_merge_of_C01_C10': True, 'final_status': fin['status']})
        self.res['C11'] = rec
        # hand-off: only the sealed C11 cartridge + integrity data for the new process
        hand = RUNS / 'handoff'; shutil.rmtree(hand, ignore_errors=True); hand.mkdir(parents=True)
        for ext in ('.pt', '.sha256'):
            shutil.copyfile(CART716 / ('C11' + ext), hand / ('C11' + ext))
        forbidden = {b['cartridge_sha256']: b['id'] for b in self.eng.E['R']['books'] if b['id'] != 'C11'}
        sizes = sorted({(CART716 / (b['id'] + '.pt')).stat().st_size for b in self.eng.E['R']['books'] if b['id'] != 'C11'})
        import pymupdf as fitz
        doc = fitz.open(str(ROOT716 / 'siemens.pdf')); pdf_text = ''.join(doc[i].get_text(sort=True) for i in range(len(doc)))
        excl = set(C.shingle_hashes(pdf_text, keep=10 ** 9)); sh = set()
        for k in range(5):
            sh.update(sorted(set(C.shingle_hashes(self.store.get_json(f'synthesis/P{k + 1}.json')['text'], keep=10 ** 9)) - excl)[:2000])
        hd = {'allowed': {'C11': {k2: rec[k2] for k2 in ('id', 'cartridge_sha256', 'body_tokens', 'bytes')}}, 'forbidden_cartridge_sha256': forbidden,
              'forbidden_sizes': sizes, 'forbidden_text_shingles': sorted(sh), 'build_runtime': self.res['runtime'], 'sentinel_before': self.eng.E['before'],
              'baseline_allocated': self.base['allocated'], 'kv_row_bytes': self.eng.kv_row_bytes, 'P': self.eng.E['P'],
              'note': 'forbidden_text_shingles cover the five pair syntheses (C11 body text itself is the allowed cartridge content)'}
        (hand / 'handoff.json').write_text(json.dumps(hd, indent=1)); self.store.put_file('handoff/handoff.json', hand / 'handoff.json', 'handoff')
        self.res['handoff_sha256'] = C.sha256_file(hand / 'handoff.json')

    def run(self):
        try:
            self.stage('boot_and_C01-C10', self.boot)
            for k in range(5):
                self.with_memory_recovery(f'pair{k + 1}', self.pair, k)
            self.with_memory_recovery('S1-S5_joint_and_final_synthesis', self.joint)
            self.stage('C11_write_and_handoff', self.c11)
            after = self.eng.E['sentinel'](); self.res['sentinel_after'] = after; self.res['weights_unchanged'] = after == self.eng.E['before']
            if not self.res['weights_unchanged']:
                raise C.StageError('WEIGHTS_CHANGED')
            self.res['status'] = 'BUILD_COMPLETE'
        except Exception as e:
            import traceback
            self.res['status'] = 'ERROR'; self.res['error'] = f'{type(e).__name__}: {e}'; self.res['traceback'] = traceback.format_exc()[-6000:]; raise
        finally:
            self.res['ensure_room_recoveries'] = {'count': len(getattr(self.eng, 'recoveries', [])), 'first': getattr(self.eng, 'recoveries', [])[:5], 'last': getattr(self.eng, 'recoveries', [])[-5:]}
            self.res['wall_seconds'] = round(time.time() - self.t0, 1); self.res['engine_tail'] = self.eng.tee.lines[-40:] if self.eng.tee else []
            self.save(); self.log.ev('BUILD_RESULT', self.res['status']); self.log.close()
            if self.eng.tee:
                self.store.put_text('engine_stdout.log', '\n'.join(self.eng.tee.lines), 'log')
                sys.stdout = self.eng.tee.stream

if __name__ == '__main__':
    Build().run()
''','62a32db92bbadc4f32aef5bfee5003b15c0d45ab292146758128bbc7c079979f')
_program_write('TEST719_demo_ask.py',r'''# AKBASCORE TEST719-DEMO — PROCESS 2 (ask). Started only after process 1 has exited. Same Colab VM, NEW Python process.
# Loads the frozen model (unchanged 716 model-load statements) and ONLY the sealed C11 cartridge. The build directories are
# quarantined: an audit hook refuses (and counts) every file access below them, so this process cannot read C01-C10, S1-S5,
# the syntheses or the source PDF. Then: the five fixed questions to C11, and the same questions to the document-free model.
import os, sys, io, gc, json, time, shutil
from pathlib import Path

QUARANTINE = tuple(str(Path(x)) for x in os.environ.get('T719_QUARANTINE', '').split(':') if x)
QLOG = {'installed': bool(QUARANTINE), 'roots': list(QUARANTINE), 'blocked': [], 'events_checked': 0}
def _hook(event, args):
    if event in ('open', 'os.listdir', 'os.scandir', 'shutil.copyfile', 'shutil.copytree', 'os.rename', 'os.remove') and args:
        QLOG['events_checked'] += 1; p = args[0]
        if isinstance(p, (str, bytes, os.PathLike)):
            try:
                ps = os.path.abspath(os.fsdecode(p))
            except Exception:
                return
            if any(ps == q or ps.startswith(q + os.sep) for q in QUARANTINE):
                if len(QLOG['blocked']) < 50:
                    QLOG['blocked'].append({'event': event, 'path': ps})
                raise PermissionError('TEST719 quarantine: access denied to ' + ps)
if QUARANTINE:
    sys.addaudithook(_hook)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import TEST719_common as C

RUNS_ASK = Path(os.environ.get('T719_ASK_OUT', '/content/T719_ASK')); HAND = Path(os.environ.get('T719_HANDOFF', '/content/T719_ASK_IN'))
QFILE = C.HERE / 'TEST719_demo_questions.json'
CART716 = Path('/content/AKBASCORE_TEST714/cartridges')

def npz_bytes(**a):
    import numpy as np
    b = io.BytesIO(); np.savez_compressed(b, **a); return b.getvalue()

class Ask:
    def __init__(self):
        import torch
        self.torch = torch; self.prov = C.provenance(torch); self.mode = self.prov['mode']
        self.log = C.EventLog(RUNS_ASK / 'events.jsonl'); self.store = C.Store(RUNS_ASK / 'store', None, self.mode, self.log)
        self.eng = C.Engine(self.log, self.mode); self.res = {'status': 'STARTED', 'provenance': self.prov, 'runtime': C.runtime_identity(), 'independence': {}, 'answers': []}
        self.t0 = time.time()

    def save(self):
        self.store.put_json('ask_result.json', self.res, 'result')

    def independence_before_boot(self):
        ind = self.res['independence']; raw = (HAND / 'handoff.json').read_bytes(); self.hd = json.loads(raw)
        ind['handoff_sha256'] = C.sha256_bytes(raw)
        files = sorted(x.name for x in HAND.iterdir())
        ind['handoff_files'] = files
        if files != ['C11.pt', 'C11.sha256', 'handoff.json']:
            raise C.StageError('HANDOFF_DIRECTORY_NOT_C11_ONLY ' + repr(files))
        c11 = self.hd['allowed']['C11']
        if C.sha256_file(HAND / 'C11.pt') != c11['cartridge_sha256']:
            raise C.StageError('C11_SHA_MISMATCH')
        rt = self.res['runtime']; b = self.hd['build_runtime']
        ind['process'] = {'mode': 'NEW_PYTHON_PROCESS_SAME_VM', 'build_pid': b.get('pid'), 'ask_pid': rt['pid'], 'build_exit_code': os.environ.get('T719_BUILD_EXIT_CODE'),
                          'build_ended_utc': os.environ.get('T719_BUILD_ENDED_UTC'), 'ask_started_utc': rt['utc'], 'same_boot_id_as_build': rt['boot_id'] == b.get('boot_id'),
                          'statement': 'new Python process on the same Colab VM; NOT a separate VM or runtime'}
        ind['process']['pass'] = (rt['pid'] != b.get('pid') and ind['process']['build_exit_code'] == '0' and bool(ind['process']['build_ended_utc'])
                                  and ind['process']['build_ended_utc'] < rt['utc'])
        g = C.gpu_processes(); ind['gpu_before_model_load'] = dict(g, **{'pass': g.get('apps') == [] and g.get('memory_used_mib') is not None and g['memory_used_mib'] < 1024})
        ind['engine_cartridge_dir_before_boot'] = sorted(x.name for x in CART716.iterdir()) if CART716.exists() else []
        hf = Path(os.environ.get('HF_HOME', str(Path.home() / '.cache' / 'huggingface')))
        skips = [str(hf), str(RUNS_ASK)] + list(QUARANTINE); t = time.time()
        findings, scanned = C.independence_scan(['/content', '/root', '/tmp', '/home', '/mnt', '/var/tmp'], self.hd['forbidden_cartridge_sha256'], self.hd['forbidden_sizes'],
                                                self.hd['forbidden_text_shingles'], skip_dirs=skips)
        ind['filesystem_scan'] = {'skipped': skips, 'scanned': scanned, 'findings': findings, 'pass': not findings, 'seconds': round(time.time() - t, 1),
                                  'note': 'quarantined build directories are on the same disk; the audit hook shows they were not read'}
        ok = ind['process']['pass'] and ind['gpu_before_model_load']['pass'] and ind['filesystem_scan']['pass'] and not ind['engine_cartridge_dir_before_boot'] and QLOG['installed']
        ind['pre_boot_pass'] = ok; self.save()
        self.log.ev('INDEPENDENCE', 'pre-boot', process=ind['process']['pass'], gpu_empty=ind['gpu_before_model_load']['pass'], fs=ind['filesystem_scan']['pass'])
        if not ok:   # recorded and reported (the isolation claim is then NOT supported); the experiment continues
            self.note('INDEPENDENCE_PRE_BOOT_FAILED', {k: (v.get('pass') if isinstance(v, dict) else v) for k, v in ind.items() if k in ('process', 'gpu_before_model_load', 'filesystem_scan', 'engine_cartridge_dir_before_boot')})

    def boot(self):
        self.res['model_pin'] = C.pin_model_revision(self.log, self.mode)
        info = self.eng.boot(model_only=True); E = self.eng.E
        CART = Path(E['CART']); CART.mkdir(parents=True, exist_ok=True)
        if any(CART.iterdir()):   # recorded; only C11 is registered, so cart_load can load nothing else
            self.note('CARTRIDGE_DIR_NOT_EMPTY', sorted(x.name for x in CART.iterdir()))
        E['R']['books'] = []
        shutil.copyfile(HAND / 'C11.pt', CART / 'C11.pt'); shutil.copyfile(HAND / 'C11.sha256', CART / 'C11.sha256'); self.eng.register_existing(self.hd['allowed']['C11'])
        ind = self.res['independence']
        ind['cartridge_directory'] = {'listing': sorted(x.name for x in CART.iterdir()), 'books': [b['id'] for b in E['R']['books']]}
        ind['cartridge_directory']['pass'] = ind['cartridge_directory']['listing'] == ['C11.pt', 'C11.sha256'] and ind['cartridge_directory']['books'] == ['C11']
        ind['same_weights_as_build'] = {'build': self.hd['sentinel_before'], 'ask': E['before'], 'pass': E['before'] == self.hd['sentinel_before']}
        self.warmup()
        self.base = self.eng.mem(); self.base_ptrs = self.eng.cuda_storage_ptrs(); self.res['engine'] = {k: v for k, v in info.items() if k != 'books'}
        if not (ind['cartridge_directory']['pass'] and ind['same_weights_as_build']['pass']):
            self.note('BOOT_CHECK_FAILED', {'cartridge_directory': ind['cartridge_directory']['pass'], 'same_weights_as_build': ind['same_weights_as_build']['pass']})

    def warmup(self):
        """Observer-only forward over the 716 system prefix (no document, nothing kept). It creates the persistent CUDA
        workspaces (cuBLAS etc.) BEFORE the model-only baseline is taken, so they are not mistaken for foreign memory later."""
        E = self.eng.E; torch = E['torch']; ids = list(E['PIDS']); t = time.time(); m0 = self.eng.mem()
        with torch.no_grad():
            x = torch.tensor([ids], device='cuda:0'); pos = torch.arange(0, len(ids), device='cuda:0').unsqueeze(0)
            out = E['model'](input_ids=x, position_ids=pos, use_cache=False, return_dict=True); del out, x, pos
        E['free_gpu'](); m1 = self.eng.mem()
        self.res['warmup'] = {'tokens': len(ids), 'seconds': round(time.time() - t, 2), 'allocated_before': m0['allocated'], 'allocated_after': m1['allocated'],
                              'note': 'system-prefix forward only; no document; output discarded'}

    def mount_c11(self):
        before = self.eng.mem(); h = {'m': None}; h['m'], mrec = self.eng.mount('C11'); after = self.eng.mem()
        flat = [t for kv in h['m'] for t in kv]
        rows = self.eng.rows(h['m']); exp_rows = int(self.eng.E['P']) + int(self.hd['allowed']['C11']['body_tokens']); exp_bytes = rows * self.eng.kv_row_bytes
        mem_storage, n_storage = self.eng.storage_bytes(flat)
        census = self.eng.cuda_tensor_census(known=flat, baseline_ptrs=self.base_ptrs); tol = 32 * 2 ** 20   # allocator rounding + small temporaries (~100 K/V rows)
        logical = self.eng.kv_bytes(h['m'])   # numel x element size of the 160 mounted K/V tensors
        audit = {'rows': rows, 'rows_expected': exp_rows, 'expected_kv_bytes': exp_bytes, 'memory_logical_bytes': logical,
                 'memory_tensors_all_cuda': all(getattr(t, 'is_cuda', False) for t in flat), 'memory_unique_storage_bytes': mem_storage, 'memory_unique_storages': n_storage,
                 'allocated_model_only_baseline': self.base['allocated'], 'allocated_before_mount': before['allocated'], 'allocated_after_mount': after['allocated'],
                 'allocated_delta': after['allocated'] - before['allocated'], 'allocated_above_model_baseline': after['allocated'] - self.base['allocated'],
                 'census_supporting': census, 'mount': mrec, 'nvidia_smi': C.nvidia_smi(),
                 'what_is_proven': ('(1) the mounted memory has exactly the rows of C11, its 160 K/V tensors hold exactly rows x 327,680 bytes and their unique storages are not smaller (and at most allocator rounding larger); '
                                    '(2) the allocator holds no more than that above the model-only baseline (+ allocator rounding), so no other K/V memory of '
                                    'material size is resident; (3) the content is C11 because cart_load verified the C11 file SHA-256 and the 80-layer seal of the '
                                    'mounted memory is recorded. Detection floor: resident foreign memory smaller than 32 MiB (about 100 K/V rows) cannot be '
                                    'excluded by the allocator check. The gc census (new non-model CUDA storages since the model-only baseline) is supporting '
                                    'only (fails the audit above 4 MiB): it cannot see tensors held inside C/C++ objects, and it can only fail the audit, never pass it.')}
        # logical bytes must match exactly; unique storages may be slightly larger (shared / padded storage) but never smaller
        audit['pass'] = (rows == exp_rows and audit['memory_tensors_all_cuda'] and logical == exp_bytes and exp_bytes <= mem_storage <= exp_bytes + tol
                         and abs(before['allocated'] - self.base['allocated']) <= tol and 0 <= audit['allocated_above_model_baseline'] - exp_bytes <= tol
                         and (census['new_storage_bytes_not_in_memory_since_baseline'] or 0) <= 4 * 2 ** 20)
        self.res['independence']['c11_memory_audit'] = audit
        seal = self.eng.seals(h['m']); self.store.put_json('seals/C11.json', seal, 'seal')
        K, V, meta = self.eng.xray(h['m'], 'C11'); self.store.put_bytes('xray/C11.npz', npz_bytes(K=K, V=V), 'xray'); self.store.put_json('xray/C11.json', meta, 'xray_meta')
        self.res['c11'] = {'rows': rows, 'cartridge_sha256': self.hd['allowed']['C11']['cartridge_sha256'], 'xray': meta, 'memory_audit_pass': audit['pass']}
        self.log.ev('C11_MOUNTED', 'only C11 in GPU memory', rows=rows, audit=audit['pass'])
        if not audit['pass']:   # recorded; the answers are still produced and the report marks the isolation claim as not supported
            self.note('C11_MEMORY_AUDIT_FAILED', {k: audit[k] for k in ('rows', 'rows_expected', 'memory_logical_bytes', 'expected_kv_bytes', 'allocated_above_model_baseline')})
        return h

    def ask_all(self):
        Q = json.loads(QFILE.read_text(encoding='utf-8')); ceil = int(Q['ceilings']['answer'])
        h = self.mount_c11()
        for q in Q['questions']:
            self.one(h['m'], q, ceil, 'C11', 'C11 only (cart_load -> initialize)')
        self.eng.release(h); self.eng.free_cached()
        m = self.eng.mem(); self.res['after_c11_release_allocated'] = m['allocated']
        if m['allocated'] > self.base['allocated'] + 64 * 2 ** 20:
            self.note('C11_NOT_RELEASED', {'allocated_above_baseline': m['allocated'] - self.base['allocated']})
        for q in Q['questions']:
            self.one(None, q, ceil, 'NO_DOCUMENT', 'none: answer(None, question) as in TEST718 vanilla')

    def one(self, memory, q, ceil, cond, mem_label):
        """one sealed question; after a GPU memory failure the unused cached memory is released and the question is asked again
        (same memory, same greedy decoding). A failure that persists is recorded as an ERROR answer; the run continues."""
        r = None; errs = []
        for attempt in (1, 2):
            err = None
            try:
                r = self.eng.answer(memory, q['text'], ceil, 9.0, f'{cond}:{q["id"]}'); break
            except Exception as e:
                err = f'{type(e).__name__}: {e}'
                if not C.is_memory_error(e):
                    errs.append(err); break
            errs.append(err); gc.collect(); self.eng.free_cached(); self.log.ev('MEMORY_RECOVERY', f'{cond} {q["id"]}: {err[:160]} - cached memory released, asking again')
        if r is None:
            r = {'text': '', 'sha256': C.sha256_bytes(b''), 'n_generated': 0, 'ceiling': ceil, 'finish_reason': 'ERROR', 'finish_evidence': {}, 'status': 'ERROR',
                 'seconds': 0, 'utc': C.utc(), 'memory_rows': self.eng.rows(memory), 'error': errs[-1]}
            self.note('ANSWER_FAILED', {'question': q['id'], 'condition': cond, 'errors': errs})
        r.update({'id': q['id'], 'question': q['text'], 'condition': cond, 'memory': mem_label, 'attempt_errors': errs}); self.res['answers'].append(r)
        self.log.ev('ANSWER', f'{cond} {q["id"]}', status=r['status'], n=r['n_generated'], seconds=r['seconds']); self.save()

    def note(self, kind, detail):
        self.res.setdefault('notes', []).append({'kind': kind, 'detail': detail, 'utc': C.utc()}); self.log.ev('NOTE', kind, detail=detail); self.save()

    def run(self):
        try:
            for name, fn in (('independence_before_boot', self.independence_before_boot), ('model_boot_C11_only', self.boot), ('questions', self.ask_all)):
                t = time.time(); self.log.ev('STAGE_START', name); fn(); self.res.setdefault('stages', []).append({'stage': name, 'seconds': round(time.time() - t, 1)})
            after = self.eng.E['sentinel'](); self.res['weights_unchanged'] = after == self.eng.E['before']
            if not self.res['weights_unchanged']:
                self.note('WEIGHTS_CHANGED', {'after': after})
            n_ok = sum(1 for a in self.res['answers'] if a['status'] != 'ERROR')
            self.res['status'] = 'ASK_COMPLETE' if n_ok == 10 else 'ASK_PARTIAL'
        except Exception as e:
            import traceback
            self.res['status'] = 'ERROR'; self.res['error'] = f'{type(e).__name__}: {e}'; self.res['traceback'] = traceback.format_exc()[-6000:]; raise
        finally:
            self.res['independence']['quarantine_audit'] = {'installed': QLOG['installed'], 'roots': QLOG['roots'], 'events_checked': QLOG['events_checked'],
                                                            'blocked_attempts': len(QLOG['blocked']), 'blocked': QLOG['blocked'], 'pass': QLOG['installed'] and not QLOG['blocked']}
            self.res['wall_seconds'] = round(time.time() - self.t0, 1); self.save(); self.log.ev('ASK_RESULT', self.res['status']); self.log.close()
            if self.eng.tee:
                self.store.put_text('engine_stdout.log', '\n'.join(self.eng.tee.lines), 'log'); sys.stdout = self.eng.tee.stream

if __name__ == '__main__':
    Ask().run()
''','3ae13ddb17367bf069b9d369695a51ec7f3f151d3e3f638513a3b517fc1e8106')

def esc(x):return html.escape(str(x))
def card_html(title,body,kind="info"):return f'<div class="kz card {kind}"><div class="h">{esc(title)}</div><div class="small">{body}</div></div>'
def chip(bid):
    if not bid:return "<span class='chip' style='color:#374151;border-color:#9ca3af'>no document · no cartridge</span>"
    if bid=="C11":return f'<span class="chip" style="color:#fff;background:{C11_COLOR};border-color:{C11_COLOR}">C11</span>'
    i=int(bid[1:])-1 if re.fullmatch(r"C\d\d",bid) else 0;c=ccol(i);return f'<span class="chip" style="color:#fff;background:{c};border-color:{c}">{esc(bid)}</span>'
IND_COL={"CORRECT":"#047857","INCORRECT":"#B91C1C","UNCLEAR":"#B45309","INCOMPLETE":"#6D28D9","UNVERIFIED_FINISH":"#92400E","NOT_PRODUCED":"#6B7280"}

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
.ind{font-weight:800;font-size:12.5px;letter-spacing:.3px}
#kz_ask button,#kz_ask{font-size:clamp(15px,4.2vw,18px)!important;font-weight:700!important;min-height:52px!important}
@media (max-width:640px){.tbl .hide-m{display:none}}
"""
HERO=(f'<div class="kz hero"><span class="rec">Live research demonstration · frozen Qwen2.5-72B · real industrial manual · measured in this session</span>'
      f'<div class="brand">AKBASCORE AI TECHNOLOGY<br>SILICON HIPPOCAMPUS · SIEMENS SINUMERIK ONE</div><div class="title">FROM TEN PHYSICAL CARTRIDGES TO ONE NEW MEMORY — five physical pair memories, S1–S5, and the cartridge C11</div>'
      '<ul class="msg">'
      f'<li>The original <b>{esc(DOC_TITLE)}, edition {DOC_EDITION_MARK}</b> is downloaded from Siemens in this session and locked by SHA-256. Its 486 pages become <b>ten physical CUT3 cartridges C01–C10</b> (unchanged TEST716/TEST709 engine).</li>'
      '<li><b>Five physical pairs</b> are built on the GPU: initialize(C01) → append(C02) … initialize(C09) → append(C10). Every append is verified by the engine on <b>all 80 layers by exact SHA-256</b>.</li>'
      '<li>From each joint pair memory the frozen model writes one <b>question-independent general synthesis</b> → cartridges <b>S1–S5</b> → physically joined → general final synthesis → new cartridge <b>C11</b>. A synthesis is accepted only if its end is observed as a stop token and it ends with “END OF SYNTHESIS”.</li>'
      '<li><b>Five fixed questions</b> — each verified on the real PDF and sealed before any model was loaded — go to <b>C11 alone in a new Python process</b> (same Colab VM, empty GPU, quarantined build files) and to the same model <b>without any document</b>.</li>'
      '<li>Answers are shown <b>raw and unedited</b>. The indicator is an automatic text rule, <b>not expert verification</b>. C11 is a new memory written from a model-generated synthesis, <b>not a lossless merge</b> of C01–C10.</li></ul>'
      f'<div class="by"><b>{esc(AUTHOR)}</b> · {esc(ORG)} · {esc(PLACE)} · {esc(VERSION_NOTE)}</div>'
      f'<div class="lic">{esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · <a href="{REPO}" target="_blank" rel="noopener">{esc(REPO)}</a> · Siemens manual © Siemens AG (not redistributed)</div></div>')
SCOPE_HTML=card_html("What this demo shows — and what it does not",
    "Shown, measured in this session: ten physical cartridges from the original 2025 Siemens manual; five physical pair memories, each append verified on all 80 layers by exact "
    "SHA-256 and X-rayed read-only; five question-independent syntheses written as S1–S5; S1–S5 physically joined; a general final synthesis written as the new cartridge C11; "
    "C11 loaded alone in a new Python process with an empty GPU and quarantined build files; five sealed questions answered by C11 and by the model without any document; the "
    "weights stay frozen and every file is SHA-256 verified. Not shown: verified technical correctness (answers are raw; the indicator is automatic); a statistical result (five "
    "questions); a lossless merge of C01–C10 (C11 holds only what the syntheses kept); a separate machine (process 2 runs on the same VM). A correct no-document answer may come "
    "from pre-training. The GPU memory audit cannot exclude foreign memory below 32 MiB.","warn")
PREV_HTML=card_html(PREV_TITLE,f"{esc(PREV_TEXT)}<br><br>For the implementation, experimental evidence, and multi-cartridge question-answering observations, see: "
                    f"<b>Research Record III — Qwen2.5-72B, Direct Internal-State Injection</b> · Zenodo Record 23434686 · "
                    f"<a href='https://zenodo.org/records/23434686' target='_blank' rel='noopener'>https://zenodo.org/records/23434686</a><br>"
                    f"<i>Previously published research — not a result of this Siemens experiment.</i>","info")

def final_card():
    f=INIT.get("final") or {}
    if not f:return ""
    ok=f.get("result")=="VALID"
    body=(f"<b>Scientific result:</b> {esc(f.get('result'))}<br><b>C11 isolation:</b> {esc(f.get('isolation'))}<br><b>Provenance:</b> {esc(f.get('provenance'))}"+
          ("".join(f"<br>⚠ reported gap · {esc(g.get('step'))} · {esc(g.get('kind'))} · {esc(short(g.get('gap'),220))}" for g in f.get("gaps") or []) or "<br>No reported gaps."))
    return card_html("Final status of this run — "+f.get("headline",""),body,"on" if ok and not f.get("gaps") else ("warn" if ok else "err"))

def engine_card_html():
    a=engine_architecture() or {};v=STATE.get("verification") or {};B=build_result();A=ask_result();ph=phases();c11=B.get("C11") or {}
    rows=[("Model",f"{MODEL_ID} · NF4 4-bit, BF16 compute · frozen · pinned snapshot {str((B.get('model_pin') or {}).get('commit'))[:12]}"),
          ("Model release",f"first public release {MODEL_RELEASE['date']} ({MODEL_RELEASE['url']})"),
          ("Architecture",f"{a.get('layers')} layers · hidden {a.get('hidden')} · {a.get('q_heads')} Q / {a.get('kv_heads')} KV heads · head dim {a.get('head_dim')} · CUT{a.get('cut')}"),
          ("Source document",f"{DOC_TITLE} · edition {DOC_EDITION_MARK} (on {DOC.get('edition_mark_pages')} pages) · {DOC.get('pages')} pages · SHA-256 {str(DOC.get('sha256'))[:16]}… · downloaded {str(DOC.get('download_end_utc'))[:19]} UTC"),
          ("Engine",f"716.py {LOCKS['716.py'][:12]}… · 709.py {LOCKS['709.py'][:12]}… · executed unchanged (only MAX_NEW set per call)"),
          ("Process 1",f"pid {ph.get('BUILD',{}).get('pid')} · {ph.get('BUILD',{}).get('start_utc')} → {ph.get('BUILD',{}).get('end_utc')} · exit {ph.get('BUILD',{}).get('exit_code')} · {B.get('status')}"),
          ("Process 2",f"pid {ph.get('ASK',{}).get('pid')} · {ph.get('ASK',{}).get('start_utc')} → {ph.get('ASK',{}).get('end_utc')} · exit {ph.get('ASK',{}).get('exit_code')} · {A.get('status')} · same Colab VM, new process"),
          ("C11",f"{c11.get('body_tokens')} tokens · SHA-256 {str(c11.get('cartridge_sha256'))[:16]}… · mounted here: {STATE['mount']['rows'] if STATE.get('mount') else '—'} rows"),
          ("Live verification",f"{v.get('passed')}/{v.get('total')} passed · provenance {LIVE.get('provenance')}"),
          ("Generation",f"greedy · sealed panel ≤ {(LIVE.get('questions') or [{}])[0].get('answers',{}).get('C11',{}).get('ceiling','—')} new tokens (safety ceiling) · interface ≤ {INTERACTIVE_MAX_NEW}"),
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

def panel_html():
    """the sealed five-question panel: question, PDF evidence, and the two raw answers (C11 alone · no document), unedited"""
    out=[]
    for q in LIVE.get("questions") or []:
        pe=q.get("pdf_evidence") or {};evs=[]
        for ev in pe.get("evidence",[]):
            f=ev.get("found") or {}
            if ev["cartridge"]=="EVERY":evs.append(f"found in {len(f)}/{N_CART} cartridges")
            elif f:evs.append(f"{esc(f['cartridge'])} · PDF page {f['pdf_page']} · “{esc(short(f['snippets'][-1],160))}”")
        t=(f"<b>{esc(q['id'])}</b> · {esc(q['text'])}<div class='small' style='margin-top:4px'>expected (PDF): <b>{esc(q['verifiable_answer'])}</b> · {esc(q['source'])} · region {esc(q.get('region'))}"
           f"<br>source check before model load: {'✓ verified' if pe.get('verified') else '✗ not verified'} — "+" · ".join(evs)+"</div>")
        t+="<table class='tbl'><tr><th>memory</th><th>raw model answer (unedited)</th></tr>"
        for c in ("C11","NO_DOCUMENT"):
            a=q["answers"].get(c) or {};ind=a.get("evaluation","—")
            t+=(f"<tr><td>{chip('C11' if c=='C11' else None)}<div class='ind' style='color:{IND_COL.get(ind,'#6b7280')}'>{esc(ind.replace('_',' '))}</div>"
                f"<div class='small mono'>{esc(a.get('status'))} · finish {esc(a.get('finish_reason'))}<br>{a.get('n_generated')} tok · {a.get('seconds')} s</div></td>"
                f"<td><div class='ans'>{esc(a.get('text',''))}</div><div class='small mono' style='opacity:.75'>{esc(a.get('why',''))}</div></td></tr>")
        t+="</table>"
        if q.get("note"):t+=f"<div class='small' style='opacity:.8'><i>{esc(q['note'])}</i></div>"
        out.append(t)
    return card_html("The five sealed questions — C11 alone (new process) vs no document · raw answers","<hr style='border:0;border-top:1px solid #d1d5db'>".join(out) or "not available","on")

def pdf_card():
    d=DOC
    return card_html("Original Siemens PDF used in this session",
        f"<b>{esc(DOC_TITLE)}</b> · edition {esc(DOC_EDITION_MARK)} (printed on {esc(d.get('edition_mark_pages'))} of {esc(d.get('pages'))} pages) · order no. {esc(d.get('order_number'))} · {esc(d.get('software_version'))}<br>"
        f"downloaded {esc(d.get('download_start_utc'))} → {esc(d.get('download_end_utc'))} UTC · {d.get('bytes',0):,} bytes · SHA-256 <span class='mono'>{esc(d.get('sha256'))}</span> (= TEST716 lock)<br>"
        f"⬇ <a href='{PDF_URL}' target='_blank' rel='noopener'><b>Download the original PDF from the official Siemens address</b></a> and compare its SHA-256 with the value above "
        f"(record: SOURCE_DOCUMENT_RECORD.json).<br><i>{esc(PDF_POLICY)}</i> <a href='{PDF_TERMS_URL}' target='_blank' rel='noopener'>Siemens terms</a>. "
        f"The verified copy stays only inside this Colab runtime: <span class='mono'>{esc(d.get('verified_local_copy'))}</span>","info")
def cond_choices():
    c=build_result().get("C11") or {}
    return [(f"C11 · new cartridge from the general final synthesis · {c.get('body_tokens','—')} tokens","C11"),("No document · frozen model only","NONE")]
def question_choices():return [q["text"] for q in (LIVE.get("questions") or [])]
def condition_info(sel):
    m=STATE.get("mount") or {}
    head=f"Mounted now: {chip('C11')} · {m.get('rows','—'):,} rows · loaded in this notebook process after process 2 ended" if m else "No memory mounted."
    if sel=="NONE":head+="<br><b>No document selected</b> — the question is answered without any cartridge."
    head+=(f"<br>Questions asked here are <b>not part of the sealed panel</b>. Up to {INTERACTIVE_MAX_NEW} new tokens; the end of generation is reported "
           "(EOS = stop token observed; CEILING = cut at the limit; UNVERIFIED = not confirmed).")
    return card_html("Memory condition",head,"info")

def answer_html(r,c):
    t="<table class='tbl'><tr><th>memory</th><th>raw model answer</th><th class='hide-m'>time</th></tr>"
    for x in (r,c):
        if x is None:continue
        t+=(f"<tr><td>{chip(x['cartridge'])}<div class='small mono'>{x['cache_tokens']:,} rows · {x['n_generated']} tok<br>{esc(x['status'])} · finish {esc(x['finish_reason'])}</div></td>"
            f"<td><div class='ans'>{esc(x['raw'])}</div></td><td class='hide-m mono'>{x['seconds']} s</td></tr>")
    t+="</table>";x=r or c
    t+=(f"<div class='small mono' style='margin-top:8px;opacity:.8'>question {esc(x['question'])}<br>max new tokens {INTERACTIVE_MAX_NEW} · NOT VERIFIED — check against the Siemens PDF · "
        f"not part of the sealed panel · GPU free {x['gpu'].get('free_gib')} GiB · {esc(x['utc'])}</div>")
    return card_html("Answer of the frozen Qwen2.5-72B — raw output, unedited",t,"on")

GPU_LOCK=threading.Lock()
def busy_card():return card_html("Busy","Another run is using the GPU. Please wait until it has finished and press the button again.","warn")
def err_card(ex):
    oom="OutOfMemoryError" in type(ex).__name__ or "GPU_SAFETY_STOP" in str(ex) or "PRE_GENERATION_CHECK" in str(ex)
    hint=" The TEST709 GPU safety reserve stopped the operation (or CUDA ran out of memory). Press ASK again." if oom else ""
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

def ask_handler(sel,question,control):
    NO=("","",None)
    keep=(gr.update(),gr.update(),gr.update(),condition_info(sel))
    if not GPU_LOCK.acquire(blocking=False):yield (busy_card(),)+NO+keep;return
    try:
        q=(question or "").strip()
        if not q:raise OpError("Type a question first.")
        r=None;c=None
        if sel=="C11":
            yield (card_html("Running",f"C11 mounted · asking the frozen model{' and the model without any document' if control else ''} (up to {INTERACTIVE_MAX_NEW} tokens each) …","info"),)+NO+keep
            r=ask_live(q[:3000],True)
            if control:c=ask_live(q[:3000],False)
        else:
            yield (card_html("Running","Asking the model without any document …","info"),)+NO+keep
            c=ask_live(q[:3000],False)
        rec=dict(question=q,selection=sel,memory=r,no_document=c,session=SESSION_ID,sealed_panel=False)
        d=SESSION_DIR/"single_runs";d.mkdir(exist_ok=True)
        p=dump_json(d/f"ASK_{sel}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json",rec)
        files,z,summ=refresh_package()
        yield (answer_html(r,c),json.dumps(jsafe(rec),ensure_ascii=False,indent=1)[:200000],"",str(p),files,z,summ,condition_info(sel))
    except Exception as ex:
        slog("UI_ERROR","ask",error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc()[-3000:])
        files,z,summ=refresh_package()
        yield (err_card(ex),"",traceback.format_exc(),None,files,z,summ,condition_info(sel))
    finally:GPU_LOCK.release()

def verify_handler():
    if not GPU_LOCK.acquire(blocking=False):return busy_card()
    try:
        w=verify_weights();d=verify_disk()
        rows=[("time (UTC)",w["utc"]),("weight sentinel of process 1 at load",w["before"]),("weight sentinel now (this process)",w["after"]),("sentinel unchanged",w["passed"]),
              ("trainable tensors",sum(1 for p in E["model"].parameters() if p.requires_grad))]+[(f"cartridge {f['cartridge']} SHA-256 on disk = record",f["equals_record"]) for f in d["files"]]
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
    qs=question_choices()
    with blocks as demo:
        gr.HTML(HERO);gr.HTML(final_card());gr.HTML(engine_card_html())
        gr.HTML(panel_html())
        cond_dd=gr.Dropdown(choices=cond_choices(),value="C11",label="Memory condition (the new cartridge C11, or the model without any document)",interactive=True)
        info=gr.HTML(condition_info("C11"))
        cq=gr.Dropdown(choices=qs,value=(qs[0] if qs else None),allow_custom_value=True,label="Question (pick one of the sealed questions or type your own; raw output, not verified)",interactive=True)
        ctl=gr.Checkbox(value=True,label="Also ask the same question to the model without any document")
        ask_b=gr.Button("ASK",variant="primary",elem_id="kz_ask")
        status=gr.HTML(stages_html())
        gallery=_gallery(label=f"Figures 1–{len(FIGURES)} (JPEG, 300 dpi) — measured in this session",value=gallery_items())
        files=gr.File(label="Individual downloads · figures, ZIP, run summary, process outputs, records, syntheses, manifest, historical logs",value=all_files(),file_count="multiple",interactive=False)
        gr.HTML(pdf_card())
        zipb=gr.DownloadButton(label="⬇ Download the complete experiment package (.zip)",value=str(ZIP_PATH),interactive=True)
        single_file=gr.File(label="Record of the last question (.json)",interactive=False)
        with gr.Tabs():
            with gr.Tab("Run summary"):summ=_tb(lines=14,max_lines=40,label="RUN_SUMMARY.txt",value=summary_text())
            with gr.Tab("Raw record (last question)"):raw=_tb(lines=14,max_lines=40,label="JSON")
            with gr.Tab("Error log"):errs=_tb(lines=10,max_lines=40,label="traceback (empty = no error)")
        with gr.Accordion("Verify the frozen weights and all cartridge files now",open=False):
            vb=gr.Button("Verify now");vout=gr.HTML()
        gr.HTML(SCOPE_HTML);gr.HTML(PREV_HTML)
        gr.HTML(f'<div class="kz small" style="opacity:.8;margin:8px 0 18px">{esc(AUTHOR)} · {esc(ORG)} · {esc(LICENSE_NAME)} · '
                f'TEST716 <a href="{URL_716}" target="_blank" rel="noopener">716.py</a> · TEST709 <a href="{URL_709}" target="_blank" rel="noopener">709.py</a> · '
                +" · ".join(f'<a href="{u}" target="_blank" rel="noopener">{esc(t.split(" — ")[0])}</a>' for t,u in LINEAGE)+
                ' · Qwen2.5-72B-Instruct, the Siemens manual and third-party libraries remain under their own licences.</div>')
        cond_dd.change(condition_info,inputs=cond_dd,outputs=info)
        outs=[status,raw,errs,single_file,files,zipb,summ,info]
        ask_b.click(ask_handler,inputs=[cond_dd,cq,ctl],outputs=outs)
        vb.click(verify_handler,outputs=vout)
    try:demo.queue(default_concurrency_limit=1)
    except TypeError:demo.queue(concurrency_count=1)
    return demo

# ---------------------------------------------------------------------------------------------------------------------
# START-UP (as in the previous demonstrations): the experiment runs automatically, then the interface opens
# ---------------------------------------------------------------------------------------------------------------------
_GR_MAJOR=int(re.match(r"\d+",gr.__version__).group())
try:run_initialization()
except Exception as _ex:
    _m=str(_ex)
    _hint=("A locked source changed on GitHub — the program stops instead of running unverified code." if "LOCKED SOURCE" in _m or "BLOB" in _m or "DRIFT" in _m else
           "A program file of this cell was altered while copying: paste PART 1, PART 2 and PART 3 again, unchanged." if "PROGRAM FILE" in _m else
           "The expected answer of a fixed question was not found on the real PDF: the run stopped BEFORE any model was loaded. The question panel must be corrected; see QUESTION_PANEL_SOURCE_CHECK.json." if "SOURCE CHECK" in _m else
           "GPU memory: process 1 stopped after all memory recoveries (cached-memory release, smaller CUT3 chunk, smaller reserve). The cartridges already written on disk are reused by the next run: Runtime → Restart session, then run again." if "GPU_SAFETY_STOP" in _m or "out of memory" in _m.lower() else
           "A synthesis was cut at its safety ceiling: no cartridge was written from it and the run stopped. The records show where." if "SYNTHESIS_NOT_COMPLETE" in _m else
           "Process 1 stopped; its last lines are above and in records_console/BUILD.log. Completed parts (C01–C10 on disk) are reused by the next run." if "PROCESS 1" in _m or "BUILD process" in _m else
           "The Siemens PDF could not be downloaded or no longer matches the locked SHA-256: check the network or the Siemens address and run again." if "SOURCE DOCUMENT" in _m else
           "Hugging Face refused the model download: add your token as the Colab secret HF_TOKEN (allow notebook access) and run again." if any(x in _m for x in ("401","403","gated","Unauthorized","token")) else
           "GPU memory: the TEST709 safety reserve or CUDA stopped the run. Use an A100 80 GB runtime (Runtime → Change runtime type), restart the session and run again." if any(x in _m for x in ("GPU_SAFETY_STOP","out of memory","PRE_GENERATION_CHECK")) else
           "The GPU is in use by another process: Runtime → Restart session, then run again (completed phases are reused)." if "not empty" in _m or "another process" in _m else
           "This runtime is not an A100 80 GB: Runtime → Change runtime type → A100, then run again." if any(x in _m for x in ("A100","CUDA is not available","exactly one GPU")) else
           "Disk: free space in the Colab runtime (or use a runtime with more disk) and run again." if "disk" in _m.lower() else
           "Network error while downloading a locked source, the Siemens PDF or the model: run the cell again." if any(x in _m for x in ("URLError","timed out","HTTP Error","Connection")) else
           "See the traceback above; nothing was changed in the engine.")
    _OUT.write("\n"+"="*110+f"\nENGINE START FAILED — {type(_ex).__name__}: {_m}\nWHAT TO DO: {_hint}\nRecords of this attempt: {SESSION_DIR}\n"
               f"All files of this attempt (ZIP): {ZIP_PATH if ZIP_PATH.is_file() else 'not written'}\n"+"="*110+"\n");_OUT.flush()
    raise
GRADIO_LINK=DEMO_ROOT/"GRADIO_LINK.txt"
def launch_interface():
    """(re)starts the Gradio interface of THIS session. A public share link is tried first; if the tunnel is not available,
    the interface is opened through Colab's own port window. The link is printed in a banner and written to GRADIO_LINK.txt.
    Nothing is recomputed. The same function is used by the reconnect cell."""
    global demo
    try:demo.close()
    except Exception:pass
    demo=build_ui()
    kw=dict(share=True,allowed_paths=[str(SESSION_DIR)],show_error=True,inline=False,prevent_thread_lock=True)
    if _GR_MAJOR>=6:kw["css"]=CSS
    err=None
    for _ in range(5):
        try:demo.launch(**kw);break
        except TypeError as ex:
            bad=next((k for k in ("css","prevent_thread_lock") if k in str(ex) and k in kw),None)
            if bad is None:raise
            kw.pop(bad)
        except Exception as ex:
            if not kw.get("share"):raise
            err=f"{type(ex).__name__}: {ex}";kw["share"]=False;slog("LAUNCH_NOTE","public share link not available — opening the local interface",error=err)
    share=getattr(demo,"share_url",None);local=getattr(demo,"local_url",None);window=None
    if not share:
        try:
            from google.colab import output as _co
            port=int(re.search(r":(\d+)",str(local)).group(1));_co.serve_kernel_port_as_window(port,anchor_text="▶ Open the AKBASCORE TEST719 interface (Colab window)");window=f"Colab port window, port {port}"
        except Exception as ex:window=f"not available ({type(ex).__name__})"
    rec=dict(utc=utc_now(),session=SESSION_ID,share_url=share,local_url=local,colab_window=window,share_error=err,
             note="gradio.live links are temporary; run the reconnect cell to obtain a new link (nothing is recomputed)")
    dump_json(GRADIO_LINK.with_suffix(".json"),rec);GRADIO_LINK.write_text(f"{share or local}\n",encoding="utf-8")
    banner(f"INTERFACE OPEN · {share or ('local only: '+str(local))}\n  public link : {share or '— (tunnel not available; use the Colab window link above)'}\n"
           f"  local       : {local}\n  also saved in {GRADIO_LINK}","#")
    slog("LAUNCH","interface open",share_url=share,local_url=local,colab_window=window);return share or local
launch_interface()
# ===== END OF PART 3/3 =====
