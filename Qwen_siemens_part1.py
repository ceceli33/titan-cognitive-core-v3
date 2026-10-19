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
