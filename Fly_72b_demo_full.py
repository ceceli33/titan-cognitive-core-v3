# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST745 · LIVE RESEARCH DEMONSTRATION (Gradio, Silicon Hippocampus 1.5 infrastructure)
# Real-time closed-loop engine and physical memory cartridges on a real accident investigation
# Air Tractor AT-802A OR-2025 · AIN preliminary report → C01–C03 → S01–S03 → H01–H03 → 8 closed-loop rounds → sealed BLIND C11
# → AIN final report opened only AFTER the C11 seal → model self-audit → C12 (parent: C11 SHA-256; human review PENDING)
# Qwen/Qwen2.5-72B-Instruct · NF4 4-bit frozen · BF16 · CUT3 · NVIDIA A100-SXM4-80GB · ONE Google Colab cell
# PART 1 / 3 — locked sources, the earlier TEST745 record, the live engine process and its real-time evidence
# ---------------------------------------------------------------------------------------------------------------------
# HOW TO RUN  Paste PART 1, PART 2 and PART 3 one below the other into ONE Colab cell and run it. The cell stays running and
#             the interface opens. It has ONE button: RUN. RUN starts the published TEST745 program UNCHANGED:
#             745.py is downloaded from the repository, locked by its git blob (de9e137e…) and executed byte-for-byte as its
#             own Python process — the engine, the closed-loop algorithm, the prompts, the eight-round limit, CUT3 and the
#             cartridge code are not touched. Every line it prints is received, time-stamped and shown at once; the
#             stages, the texts it writes and the cartridges it seals appear in the interface while it works.
#             After the engine process has ended, this program re-verifies every cartridge read-only (file SHA-256,
#             tensor seals, re-derived body text), draws six JPEG figures from THIS run's outputs and offers every record
#             for direct download. A full run takes about 1.5 hours on an A100 (earlier run: 5,480 s); nothing is hidden.
# RUNS        TEST745 always writes into /content/AKBASCORE_TEST745 and refuses to overwrite a run. Before every RUN an
#             existing experiment directory is MOVED (never deleted) to /content/AKBASCORE_TEST745_ARCHIVE; after the RUN
#             the new experiment directory is moved into this RUN's own session folder. Every RUN has its own ID.
# RECORD      745.log (git blob 07d8fafb…) of the earlier completed run is shown only as RECORD for comparison. It holds
#             no generated text; no earlier output is ever presented as a result of a new RUN.
# STATUS      This demonstration code has NOT been executed on a GPU by its author (CPU simulation of the code paths only).
# AUTHOR      Mustafa Akbaş · AkbasCore AI Teknoloji · Mersin, Türkiye · Copyright © 2026 Mustafa Akbaş
#             AKBASCORE RESEARCH SOFTWARE LICENSE — https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/LICENSE
#             AIN reports: Air Accident Investigation Agency of the Republic of Croatia (ain.hr) — public documents, linked and
#             hash-recorded. Qwen2.5-72B-Instruct and third-party libraries remain governed by their own licences.
# =====================================================================================================================
import os,sys,re,io,ast,json,time,html,math,shutil,hashlib,platform,threading,traceback,subprocess,importlib.util,textwrap,types,gc,csv,difflib
from pathlib import Path
from datetime import datetime,timezone
from collections import OrderedDict,deque
from urllib.parse import quote
os.environ.pop("HF_HUB_DISABLE_PROGRESS_BARS",None)

def _pip(*pk):subprocess.check_call([sys.executable,"-m","pip","install","-q",*pk])
for _m,_p in (("numpy","numpy"),("matplotlib","matplotlib"),("PIL","pillow"),("psutil","psutil")):
    if importlib.util.find_spec(_m) is None:_pip(_p)
if importlib.util.find_spec("gradio") is None:
    _hv=None                                      # gradio must not replace the huggingface_hub that transformers needs
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
import urllib.request
SIM=os.environ.get("P745_SIM")=="1"          # code author's CPU simulation only (fake engine) — never an experimental result

# ---------------------------------------------------------------------------------------------------------------------
# identity, locks, colours
# ---------------------------------------------------------------------------------------------------------------------
APP_NAME="AKBASCORE SILICON HIPPOCAMPUS";APP_SUB="TEST745 · Real-Time Closed-Loop Engine and Physical Memory Cartridges"
APP_SHORT="AKBASCORE Silicon Hippocampus · TEST745 · Qwen2.5-72B · CUT3";CODE_VERSION="SH745-demo-1.1";EXPERIMENT="TEST745"
AUTHOR="Mustafa Akbaş";ORG="AkbasCore AI Teknoloji";PLACE="Mersin, Türkiye"
LICENSE_NAME="AKBASCORE RESEARCH SOFTWARE LICENSE";COPYRIGHT="Copyright © 2026 Mustafa Akbaş"
REPO="https://github.com/ceceli33/titan-cognitive-core-v3";RAW_BASE="https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
URL_LICENSE=REPO+"/blob/main/LICENSE";URL_745=REPO+"/blob/main/745.py";URL_745LOG=REPO+"/blob/main/745.log";URL_709=REPO+"/blob/main/709.py";URL_730=REPO+"/blob/main/730.py"
URL_15=REPO+"/blob/main/Qwen72B_1.5.log";ZENODO="https://zenodo.org/records/23497732"
LOCKS=OrderedDict([("745.py","de9e137e981fd57812d9a5e40d3c72dc278d2133"),    # TEST745 program — executed byte-for-byte
                   ("745.log","07d8fafb51e871549814442705d617f81e0322ba"),   # earlier completed run — RECORD only
                   ("709.py","6c9f8cbb1eeed848d45133d73f0d7676b68e9125"),    # locked engine (745.py checks it itself)
                   ("730.py","b1bad9eb3b111b44413f8ef05a3a140ab66a77dd"),    # locked native CUT3 functions (745.py checks it itself)
                   ("LICENSE","9aad4724d1072f9e56486650a9527380c867a53b")])
MODEL_ID="Qwen/Qwen2.5-72B-Instruct"
SRC=("C01","C02","C03");SUB=("S01","S02","S03");CRS=("H01","H02","H03");CARTS=SRC+SUB+CRS+("C11","C12")
GROUPS={"S01":["C01","C02"],"S02":["C02","C03"],"S03":["C01","C03"]};HIER={"H01":["S01","S02"],"H02":["S02","S03"],"H03":["S01","S03"]}
COL=dict(C="#2455D6",S="#C12566",H="#BA601B",C11="#7626D9",C12="#0F766E",OFF="#B91C1C",LOOP="#374151")
def ccol(cid):return COL.get(cid) or COL.get(cid[0],"#374151")
OK_COL="#08785B";NEU="#374151";BG="#FFFFFF";INK="#111827";INK2="#374151";MUTED="#6B7280";RULE="#D1D5DB";PANEL="#F8FAFC";RED="#B91C1C";AMBER="#B45309"
ANCHORS=dict(C11="3f78c672465975d1170e57ab70a85af1b7fa5f1ddc902ec80f2670a48f045eea",C12="fdd5add305d71d0a78c04f92a8d0724c19443d81ad2756b9f96160dd667d4e5a",seconds=5480.13)

def utc_now():return datetime.now(timezone.utc).isoformat(timespec="milliseconds")
def local_now():return datetime.now().astimezone().isoformat(timespec="seconds")
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha_text(s):return sha_bytes(str(s).encode("utf-8"))
def git_blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def sha_file(p,block=1<<22):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(block),b""):h.update(b)
    return h.hexdigest()
def jsafe(o):
    if isinstance(o,dict):return {str(k):jsafe(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)):return [jsafe(v) for v in o]
    if isinstance(o,np.floating):return float(o)
    if isinstance(o,np.integer):return int(o)
    if isinstance(o,np.ndarray):return jsafe(o.tolist())
    if isinstance(o,Path):return str(o)
    if isinstance(o,float) and (math.isnan(o) or math.isinf(o)):return None
    if isinstance(o,(str,int,float,bool)) or o is None:return o
    return str(o)
def dump_json(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(jsafe(obj),ensure_ascii=False,indent=2),encoding="utf-8");tmp.replace(path);return path
def jload(p,default=None):
    try:return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:return default
def tload(p):
    try:return Path(p).read_text(encoding="utf-8")
    except Exception:return None
def short(s,n):
    s=" ".join(str(s or "").split());return s if len(s)<=n else s[:n-1].rstrip()+"…"
def gib(b):return b/2**30

# ---------------------------------------------------------------------------------------------------------------------
# directories and logs — every RUN has its own session folder; the TEST745 directory is never overwritten
# ---------------------------------------------------------------------------------------------------------------------
_CROOT=Path("/content") if os.path.isdir("/content") else Path("/tmp")
DEMO_ROOT=_CROOT/"AKBASCORE_TEST745_DEMO";EXP_ROOT=_CROOT/"AKBASCORE_TEST745";ARCHIVE_DIR=_CROOT/"AKBASCORE_TEST745_ARCHIVE"
EVID_DIR=DEMO_ROOT/"locked_sources";PROGRAM=EVID_DIR/"745.py"
SESSION_ID=SESSION_DIR=FIG_DIR=DATA_DIR=SESSION_LOG=SESSION_EVENTS=ENGINE_OUT=RUN_SUMMARY=MANIFEST=VERIFY_FILE=None
def _session_paths(sid):
    """every RUN gets its own ID and folder (figures, records, logs); nothing of an earlier RUN is written into it"""
    global SESSION_ID,SESSION_DIR,FIG_DIR,DATA_DIR,SESSION_LOG,SESSION_EVENTS,ENGINE_OUT,RUN_SUMMARY,MANIFEST,VERIFY_FILE
    SESSION_ID=sid;SESSION_DIR=DEMO_ROOT/"sessions"/sid;FIG_DIR=SESSION_DIR/"figures";DATA_DIR=SESSION_DIR/"records"
    SESSION_LOG=SESSION_DIR/"SESSION.log";SESSION_EVENTS=SESSION_DIR/"SESSION_EVENTS.jsonl";ENGINE_OUT=SESSION_DIR/"ENGINE_OUTPUT_REALTIME.log"
    RUN_SUMMARY=SESSION_DIR/"RUN_SUMMARY.txt";MANIFEST=SESSION_DIR/"SHA256_MANIFEST.json";VERIFY_FILE=DATA_DIR/"POST_RUN_VERIFICATION.json"
    for d in (SESSION_DIR,FIG_DIR,DATA_DIR,EVID_DIR):d.mkdir(parents=True,exist_ok=True)
_session_paths(datetime.now().astimezone().strftime("SH745-%Y%m%d-%H%M%S"))
_OUT=sys.stdout;_LOG_LOCK=threading.Lock();CONSOLE=deque(maxlen=500)
def _emit(line):
    with _LOG_LOCK:CONSOLE.append(line[:400])
    try:_OUT.write(line[:900]+"\n");_OUT.flush()
    except Exception:pass
def slog(kind,message="",**data):
    """session log: one readable line + one JSON event (time · stage · event · data) written at the moment it happens"""
    stg=(globals().get("STATE") or {}).get("current") or "-"
    ev=dict(utc=utc_now(),session=SESSION_ID,stage=stg,kind=kind,message=str(message),data=jsafe(data),provenance=("SIMULATION" if SIM else "THIS RUN"))
    line=f"{ev['utc'][11:19]} [{stg}] {kind:<16} {message}"+(f" {json.dumps(jsafe(data),ensure_ascii=False)[:300]}" if data else "")
    with _LOG_LOCK:
        with SESSION_LOG.open("a",encoding="utf-8") as f:f.write(f"{ev['utc']} [{stg}] {kind:<16} {message} {json.dumps(jsafe(data),ensure_ascii=False) if data else ''}\n")
        with SESSION_EVENTS.open("a",encoding="utf-8") as f:f.write(json.dumps(ev,ensure_ascii=False)+"\n")
    _emit(line);return ev
def banner(text,ch="═"):
    _emit(ch*100);[_emit(x) for x in str(text).splitlines()];_emit(ch*100)

SOURCES={};RAW={}
def fetch_locked(name,timeout=180):
    p=EVID_DIR/name
    if p.is_file() and git_blob(p.read_bytes())==LOCKS[name]:raw=p.read_bytes()
    else:
        req=urllib.request.Request(RAW_BASE+name,headers={"User-Agent":"AKBASCORE-TEST745-DEMO"})
        with urllib.request.urlopen(req,timeout=timeout) as f:raw=f.read()
        if git_blob(raw)!=LOCKS[name]:
            raise RuntimeError(f"LOCKED SOURCE CHANGED: {name} git blob {git_blob(raw)} != {LOCKS[name]} — the program stops instead of running an unverified file")
        p.write_bytes(raw)
    SOURCES[name]=dict(bytes=len(raw),git_blob=git_blob(raw),sha256=sha_bytes(raw),url=RAW_BASE+name,local=str(p),verified_utc=utc_now())
    return raw

# ---------------------------------------------------------------------------------------------------------------------
# 745.py read-only: the expressions it uses to compose the C11 and C12 bodies (evaluated, never retyped) and its questions
# ---------------------------------------------------------------------------------------------------------------------
P745={}
def read_745(raw):
    src=raw.decode("utf-8");t=ast.parse(src)
    def find(name):return next((n for n in ast.walk(t) if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id==name),None)
    for nm in ("blind_body","c12body"):
        n=find(nm);P745[nm+"_code"]=compile(ast.Expression(n.value),"745.py","eval");P745[nm+"_source"]=ast.get_source_segment(src,n)
    for nm in ("human_review","blind_questions","GROUPS","HIERARCHY","MAX_ROUNDS","MAX_NEW","MAX_FINAL_NEW","CASE_URL","PREFIX"):
        n=find(nm);P745[nm]=ast.literal_eval(n.value)
    P745["prompts"]=OrderedDict()
    for fn,label in (("synthesize_text","synthesis prompt (S, H, INITIAL)"),):
        f=next(n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name==fn);a=next(n for n in ast.walk(f) if isinstance(n,ast.Assign) and getattr(n.targets[0],"id",None)=="prompt")
        P745["prompts"][label]=ast.get_source_segment(src,a)
    loop=next(n for n in ast.walk(t) if isinstance(n,ast.For) and getattr(n.target,"id",None)=="round_id")
    P745["prompts"]["closed-loop review prompt (rounds 1–8)"]=ast.get_source_segment(src,next(n for n in ast.walk(loop) if isinstance(n,ast.Assign) and getattr(n.targets[0],"id",None)=="prompt"))
    refl=next(n for n in ast.walk(t) if isinstance(n,ast.Assign) and getattr(n.targets[0],"id",None)=="q")
    P745["prompts"]["source reading prompt (C01–C03)"]=ast.get_source_segment(src,refl)
    if P745["GROUPS"]!=GROUPS or P745["HIERARCHY"]!=HIER or P745["MAX_ROUNDS"]!=8:raise RuntimeError("745.py hierarchy / round limit differ from what this demo displays")
    seal=next(n for n in ast.walk(ast.parse(RAW["730.py"].decode())) if isinstance(n,ast.FunctionDef) and n.name=="seal_cp")
    P745["seal_cp_source"]=ast.get_source_segment(RAW["730.py"].decode(),seal)
def blind_body_from(entries,blind_final):
    return eval(P745["blind_body_code"],{"__builtins__":{}},{"entries":entries,"HIERARCHY":P745["HIERARCHY"],"json":json,"blind_final":blind_final})
def c12body_from(entries,R,audit):
    return eval(P745["c12body_code"],{"__builtins__":{}},{"entries":entries,"R":R,"audit":audit,"human_review":P745["human_review"]})

# ---------------------------------------------------------------------------------------------------------------------
# the earlier completed run (745.log) — RECORD, comparison only
# ---------------------------------------------------------------------------------------------------------------------
def parse_745_lines(lines):
    """the structured content of TEST745 output lines (used for the RECORD and, live, for this RUN)"""
    R=dict(checks=[],sealed=OrderedDict(),generations=[],downloads=[],io={})
    for raw in lines:
        line=raw.replace(" "," ")
        for m in re.finditer(r"(PASS|FAIL) ([A-Z][A-Za-z0-9_.]+) ?(.*)$",line):
            if m.start()==0 or line[:m.start()].endswith(("]","s/it]","it/s]"," ")) :
                R["checks"].append(dict(name=m.group(2),passed=m.group(1)=="PASS",detail=m.group(3).strip()[:400]));break
        m=re.match(r"PHYSICAL_SEALED (\w+) ([0-9a-f]{64}) PARENTS (.*)$",line)
        if m:R["sealed"][m.group(1)]=dict(sha256=m.group(2),parents=re.findall(r"'(\w+)'",m.group(3)))
        m=re.match(r"GENERATION (\w+) TOKENS (\d+) LIMIT (\d+) POSSIBLE_TRUNCATION (\w+)",line)
        if m:R["generations"].append(dict(cid=m.group(1),tokens=int(m.group(2)),limit=int(m.group(3)),possible_truncation=m.group(4)=="True"))
        m=re.match(r"OFFICIAL_OUTCOME_UNLOCK (\S+)",line)
        if m:R["unlock"]=m.group(1)
        m=re.match(r"TEST745_COMPLETED C11 ([0-9a-f]{64}) C12 ([0-9a-f]{64}) SECONDS ([\d.]+)",line)
        if m:R["completed"]=dict(C11=m.group(1),C12=m.group(2),seconds=float(m.group(3)))
        if "TEST745_FAILED_CLOSED" in line:R["failed"]=line.strip()[:500]
        for k,rx in (("download",r"Download complete:\s+([\d.]+\s*[GM]B)"),("fetch_time",r"Fetching \d+ files: 100%\s+\d+/\d+\s+\[([\d:]+)<"),("load_time",r"Loading weights: 100%\s+\d+/\d+\s+\[([\d:]+)<")):
            mm=re.search(rx,line)
            if mm:R["io"][k]=mm.group(1)
    R["checks_passed"]=sum(c["passed"] for c in R["checks"]);R["checks_total"]=len(R["checks"])
    return R
REC={}
def read_record():
    REC.clear();REC.update(parse_745_lines(RAW["745.log"].decode("utf-8").split("\n")))
    c=REC.get("completed") or {}
    if c.get("C11")!=ANCHORS["C11"] or c.get("C12")!=ANCHORS["C12"] or len(REC["sealed"])!=11:raise RuntimeError("TEST745 RECORD PARSER CHECK FAILED")
    REC["source_git_blob"]=LOCKS["745.log"];REC["note"]="earlier completed TEST745 run (745.log) — RECORD for comparison; contains no generated text"

# ---------------------------------------------------------------------------------------------------------------------
# pipeline state
# ---------------------------------------------------------------------------------------------------------------------
STAGES=OrderedDict([
    ("PRECHECK","Pre-flight — GPU (nvidia-smi), locked 745.py, fresh experiment directory (earlier runs archived, never overwritten)"),
    ("GATES","TEST745 gates — CUDA, one A100 80 GB, 709.py + 730.py git-blob locks, locked engine symbols"),
    ("SOURCES","Official sources — AIN case links, preliminary report PDF, extraction, leakage guard; final report NOT downloaded"),
    ("MODEL","Frozen Qwen2.5-72B-Instruct — download / NF4 load on the GPU · ARCH · FROZEN · NF4"),
    ("CARTRIDGES","Source cartridges C01 · C02 · C03 — three parts of ONE preliminary report → native CUT3 forge → SSD → SHA-256"),
    ("READOUTS","Physical readouts — each source cartridge mounted alone (80 layers) and read by the model"),
    ("SUBSYSTEM","Subsystem syntheses S01 · S02 · S03 — text-mediated synthesis written to new physical cartridges"),
    ("CROSS","Cross-system syntheses H01 · H02 · H03 — S cartridges read physically → synthesis → new cartridges"),
    ("LOOP","Closed loop — initial blind hypothesis + eight review rounds (no official outcome available)"),
    ("C11","C11 BLIND MASTER — forged, SHA-256 sealed, three blind questions answered from C11 alone"),
    ("OUTCOME","Embargo lifted — AIN final report downloaded only now · model self-audit against the official findings"),
    ("C12","C12 POST-OUTCOME MASTER — parent C11 SHA · C11 immutable · weights unchanged · human review PENDING"),
    ("VERIFY","Independent re-verification (read-only) — files, tensor seals, re-derived cartridge bodies, C11 → C12 lineage"),
    ("FIGURES","Six scientific figures (JPEG 300 dpi, layout QC)"),
    ("RECORDS","Records — real-time engine output, logs, texts, manifests (direct downloads, no ZIP)")])
ENGINE_STAGES=("GATES","SOURCES","MODEL","CARTRIDGES","READOUTS","SUBSYSTEM","CROSS","LOOP","C11","OUTCOME","C12")
STAGE_DONE_RX=OrderedDict([("GATES",r"^PASS LOCKED_SYMBOLS_730\.py"),("SOURCES",r"^PASS FINAL_REPORT_NOT_DOWNLOADED_BEFORE_C11"),("MODEL",r"PASS NF4"),
    ("CARTRIDGES",r"^PHYSICAL_SEALED C03 "),("READOUTS",r"^PASS GENERATION_NOT_TRUNCATED_C03"),("SUBSYSTEM",r"^PHYSICAL_SEALED S03 "),("CROSS",r"^PHYSICAL_SEALED H03 "),
    ("LOOP",r"^PASS LOOP_NONEMPTY_8\b"),("C11",r"^PASS C11_LOCKED_BEFORE_FINAL"),("OUTCOME",r"^PASS AUDIT_NOT_TRUNCATED"),("C12",r"^TEST745_COMPLETED ")])
STATE=dict(started=None,finished=None,current=None,stages={k:dict(status="wait",seconds=None,note="",t0=None) for k in STAGES},mode="REPLAY",version=0,running=False,fig_version=0,
           exp_dir=None,engine_rc=None,engine_pid=None,elapsed=None)
GPU_LOCK=threading.RLock()
def bump():STATE["version"]+=1
def stage_set(key,status,note=None,seconds=None):
    st=STATE["stages"][key]
    if status=="run" and st["t0"] is None:st["t0"]=time.perf_counter()
    if status in("done","fail","skip") and st["t0"] is not None and seconds is None:seconds=time.perf_counter()-st["t0"]
    st["status"]=status
    if note is not None:st["note"]=str(note)[:600]
    if seconds is not None:st["seconds"]=round(seconds,1)
    bump()
LIVE=dict(session=SESSION_ID)       # everything observed in THIS RUN
LINES=[]                            # every line of the engine process, with the UTC time it was received
CHECKS=[]                           # every PASS / FAIL line of the engine process (time · stage · name · detail)

# ---------------------------------------------------------------------------------------------------------------------
# PRECHECK: GPU facts, this kernel's own GPU memory, the experiment directory (archived, never deleted)
# ---------------------------------------------------------------------------------------------------------------------
def nvsmi(q):
    try:
        r=subprocess.run(["nvidia-smi",f"--query-{q}","--format=csv,noheader,nounits"],capture_output=True,text=True,timeout=30)
        return [l.strip() for l in r.stdout.splitlines() if l.strip()]
    except Exception:return []
def _free_kernel_gpu():
    """GPU memory still held by THIS notebook kernel (e.g. an earlier demo cell) would starve the TEST745 process"""
    if "torch" not in sys.modules:return "this kernel holds no CUDA context"
    torch=sys.modules["torch"]
    try:
        if not torch.cuda.is_initialized():return "this kernel holds no CUDA context"
    except Exception:return "this kernel holds no CUDA context"
    g=globals();freed=[]
    for nm in ("E","model","tok","master_memory"):
        v=g.get(nm)
        if isinstance(v,dict) and "model" in v:v.clear();freed.append(nm)
        elif nm in("model","master_memory") and v is not None:g.pop(nm,None);freed.append(nm)
    gc.collect();torch.cuda.empty_cache()
    return f"released objects of an earlier cell: {freed or 'none'} · allocated now {torch.cuda.memory_allocated()/2**30:.2f} GiB"
def stage_precheck():
    g=nvsmi("gpu=name,memory.total,memory.used,driver_version");rows=[x.split(", ") for x in g]
    LIVE["gpu"]=dict(count=len(rows),name=rows[0][0] if rows else None,total_mib=int(rows[0][1]) if rows else None,used_mib=int(rows[0][2]) if rows else None,
                     driver=rows[0][3] if rows else None,apps=nvsmi("compute-apps=pid,used_memory"),kernel=_free_kernel_gpu())
    if SIM:LIVE["gpu"].update(count=1,name="SIMULATED A100",total_mib=81920,used_mib=0)
    if not LIVE["gpu"]["count"]:raise RuntimeError("no NVIDIA GPU in this runtime — TEST745 needs one A100 80 GB (Runtime → Change runtime type → A100). Nothing was run.")
    raw=fetch_locked("745.py");PROGRAM.write_bytes(raw)
    if git_blob(PROGRAM.read_bytes())!=LOCKS["745.py"]:raise RuntimeError("745.py on disk does not match its lock")
    arch=None
    if EXP_ROOT.exists() and any(EXP_ROOT.iterdir()):
        ARCHIVE_DIR.mkdir(parents=True,exist_ok=True)
        r=jload(EXP_ROOT/"TEST745_results.json",{}) or {};tag=datetime.fromtimestamp(EXP_ROOT.stat().st_mtime).strftime("%Y%m%d-%H%M%S")
        arch=ARCHIVE_DIR/f"TEST745_{tag}_{r.get('status','UNKNOWN')}";i=1
        while arch.exists():arch=Path(f"{arch}_{i}");i+=1
        shutil.move(str(EXP_ROOT),str(arch));slog("ARCHIVED",f"earlier experiment directory moved (not deleted) to {arch}",status=r.get("status"))
    LIVE["precheck"]=dict(program=str(PROGRAM),program_git_blob=LOCKS["745.py"],archived_previous=str(arch) if arch else None,utc=utc_now())
    return (f"{LIVE['gpu']['name']} · used {LIVE['gpu']['used_mib']} MiB of {LIVE['gpu']['total_mib']} MiB · 745.py git blob {LOCKS['745.py'][:12]}… · "
            +(f"earlier experiment archived → {arch.name}" if arch else "fresh experiment directory"))

# ---------------------------------------------------------------------------------------------------------------------
# THE ENGINE PROCESS: 745.py, unchanged, as its own Python process — every output line is received, time-stamped,
# written to ENGINE_OUTPUT_REALTIME.log and drives the stage display. The engine is never modified or steered.
# ---------------------------------------------------------------------------------------------------------------------
PROGRESS={"line":""};PROC={"p":None}
def _hf_cache_bytes():
    try:
        from huggingface_hub.constants import HF_HUB_CACHE
        d=Path(HF_HUB_CACHE)/("models--"+MODEL_ID.replace("/","--"))
        return sum(f.stat().st_size for f in d.rglob("*") if f.is_file()) if d.is_dir() else 0
    except Exception:return None
def _engine_stage_of(line):
    for k,rx in STAGE_DONE_RX.items():
        if re.search(rx,line):return k
    return None
def _note_for(line):
    m=re.match(r"PHYSICAL_SEALED (\w+) ([0-9a-f]{12})",line)
    if m:return f"{m.group(1)} sealed · SHA-256 {m.group(2)}…"
    m=re.match(r"GENERATION (\w+) TOKENS (\d+)",line)
    if m:return f"{m.group(1)} read physically · {m.group(2)} tokens generated"
    m=re.match(r"PASS LOOP_NONEMPTY_(\d+)",line)
    if m:return f"round {m.group(1)}/8 complete"
    if line.startswith("PASS SYNTHESIS_NOT_TRUNCATED_INITIAL"):return "initial blind hypothesis written"
    if line.startswith("OFFICIAL_OUTCOME_UNLOCK"):return "C11 sealed on disk — official outcome unlocked now: "+line.split(" ",1)[1]
    m=re.match(r"PASS (\S+)",line)
    if m:return "PASS "+m.group(1)
    return None
def _on_line(line,stream):
    u=utc_now();cur=STATE.get("current")
    with _LOG_LOCK:
        LINES.append((u,stream,line))
        with ENGINE_OUT.open("a",encoding="utf-8") as f:f.write(f"{u}\t{cur}\t{stream}\t{line}\n")
    if re.search(r"\d+%\|?|it/s\]|s/it\]|B/s\]",line) and not re.search(r"(PASS|FAIL) [A-Z]",line):
        PROGRESS["line"]=short(line,160)
        if cur=="MODEL":STATE["stages"]["MODEL"]["note"]="engine process: "+PROGRESS["line"];bump()
        return
    _emit(f"  745 [{cur}] {line[:300]}")
    m=re.search(r"(PASS|FAIL) ([A-Z][A-Za-z0-9_.]+) ?(.*)$",line)
    if m:
        CHECKS.append(dict(utc=u,stage=cur,name=m.group(2),passed=m.group(1)=="PASS",detail=m.group(3).strip()[:500]))
        if m.group(1)=="FAIL":slog("ENGINE_FAIL",m.group(2),detail=m.group(3)[:500])
    for kind,rx in (("SEALED",r"^PHYSICAL_SEALED "),("GENERATION",r"^GENERATION "),("UNLOCK",r"^OFFICIAL_OUTCOME_UNLOCK"),("COMPLETED",r"^TEST745_COMPLETED"),("FAILED",r"TEST745_FAILED_CLOSED")):
        if re.search(rx,line):slog("ENGINE_"+kind,line[:400])
    n=_note_for(line)
    if n and cur in STAGES:STATE["stages"][cur]["note"]=n;bump()
    done=_engine_stage_of(line)
    if done:
        keys=list(ENGINE_STAGES);i=keys.index(done)
        for k in keys[:i+1]:
            if STATE["stages"][k]["status"] in("wait","run"):stage_set(k,"done")
        if i+1<len(keys):STATE["current"]=keys[i+1];stage_set(keys[i+1],"run")
def _reader(pipe,stream):
    buf=b""
    while True:
        ch=pipe.read1(65536) if hasattr(pipe,"read1") else pipe.read(4096)
        if not ch:break
        buf+=ch
        parts=re.split(rb"[\r\n]",buf);buf=parts.pop()
        for p in parts:
            s=p.decode("utf-8","replace").rstrip()
            if s:_on_line(s,stream)
    if buf.strip():_on_line(buf.decode("utf-8","replace").rstrip(),stream)
def _heartbeat(stop):
    t0=time.perf_counter()
    while not stop.wait(60):
        el=(time.perf_counter()-t0)/60;b=_hf_cache_bytes()
        slog("ENGINE_ALIVE",f"{el:.1f} min since start",hf_cache_gb=(round(b/1e9,1) if b is not None else None),last_progress=PROGRESS["line"][:120])
        STATE["elapsed"]=round(el*60);bump()
def run_engine():
    """starts 745.py (locked, unchanged) and follows it until it exits; returns the exit code"""
    prog=PROGRAM
    if SIM and os.environ.get("P745_SIM_PROGRAM"):prog=Path(os.environ["P745_SIM_PROGRAM"])      # code author's CPU test only
    env=dict(os.environ,PYTHONUNBUFFERED="1",PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True")
    STATE["current"]="GATES";stage_set("GATES","run")
    slog("ENGINE_START",f"{sys.executable} -u {prog}",git_blob=git_blob(Path(prog).read_bytes()),cwd=str(SESSION_DIR))
    p=subprocess.Popen([sys.executable,"-u",str(prog)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=str(SESSION_DIR),env=env,bufsize=0)
    PROC["p"]=p;STATE["engine_pid"]=p.pid;stop=threading.Event()
    th=[threading.Thread(target=_reader,args=(p.stdout,"stdout"),daemon=True),threading.Thread(target=_reader,args=(p.stderr,"stderr"),daemon=True),
        threading.Thread(target=_heartbeat,args=(stop,),daemon=True)]
    for t in th:t.start()
    rc=p.wait();th[0].join(30);th[1].join(30);stop.set();STATE["engine_rc"]=rc
    slog("ENGINE_EXIT",f"exit code {rc}",pid=p.pid)
    return rc

# ---------------------------------------------------------------------------------------------------------------------
# the outputs of THIS RUN (read-only): texts, results, manifest, cartridges
# ---------------------------------------------------------------------------------------------------------------------
def exp_dir():return Path(STATE["exp_dir"]) if STATE.get("exp_dir") else (EXP_ROOT if STATE.get("running") else None)
def run_results():
    d=exp_dir();return (jload(d/"TEST745_results.json",{}) or {}) if d else {}
def run_manifest():
    d=exp_dir();return (jload(d/"TEST745_manifest.json",{}) or {}) if d else {}
def text_of(name):
    d=exp_dir();return tload(d/"generated_text"/name) if d else None
def raw_of(name):
    d=exp_dir();return tload(d/"sealed_sources"/name) if d else None
def generation_index():
    """maps the engine's generated_text files to their role, from the order of R['generations'] (745.py naming rules)"""
    R=run_results();gens=R.get("generations") or [];out=[];nxt=None
    for i,g in enumerate(gens,1):
        if "question_sha256" in g:out.append(dict(i=i,cid=g["cid"],kind="readout",file=f"{g['cid']}_{i}.txt",tokens=g.get("tokens"),possible_truncation=g.get("possible_truncation")))
        else:out.append(dict(i=i,cid=g["cid"],kind="synthesis",file=f"{g['cid']}_synthesis.txt",tokens=g.get("tokens"),limit=g.get("limit")))
    for j,o in enumerate(out):
        if o["kind"]=="readout":
            if o["cid"]=="C11":o["role"]="C11 blind answer"
            elif o["cid"] in SRC:o["role"]="source reflection (input to S syntheses)"
            else:
                syn=next((x["cid"] for x in out[j+1:] if x["kind"]=="synthesis"),None);o["role"]=f"physical readout → input to {syn}"
        else:o["role"]="synthesis text → forged as cartridge" if o["cid"]!="INITIAL" else "initial blind hypothesis (input to round 1)"
    k=0
    for o in out:
        if o["cid"]=="C11" and o["kind"]=="readout":k+=1;o["role"]=f"C11 blind answer Q{k}"
    return out
def round_texts():
    out=[("INITIAL",text_of("INITIAL_synthesis.txt"))]
    for r in range(1,9):out.append((f"R{r}",text_of(f"blind_round_{r:02d}.txt")))
    return out

def _normalize_entry(e):
    e=dict(e);ts=e.get("tensor_sha")
    if isinstance(ts,dict):e["tensor_sha"]={"h":ts.get("h"),"lower":[tuple(x) for x in (ts.get("lower") or [])]}
    return e
def stage_verify():
    """independent, read-only: every cartridge file is hashed again, its tensors loaded on the CPU and re-sealed with the locked
    730.py seal_cp(); every cartridge body is re-derived from the run's own texts and compared with the manifest body hash"""
    d=exp_dir()
    if not d or not (d/"TEST745_manifest.json").is_file():raise RuntimeError("no TEST745 manifest in this RUN — nothing to verify (nothing is substituted)")
    import torch
    ns={"torch":torch,"sha":lambda b:hashlib.sha256(b).hexdigest()};exec(compile(P745["seal_cp_source"],"730.py","exec"),ns)
    man=run_manifest();ents={k:_normalize_entry(v) for k,v in (man.get("cartridges") or {}).items()};R=run_results();rows={};probs=[]
    bodies={c:raw_of(f"{c}_FORGED.txt") for c in SRC};bodies.update({c:text_of(f"{c}_synthesis.txt") for c in SUB+CRS})
    r8=text_of("blind_round_08.txt")
    if r8 is not None and all(k in ents for k in CRS):bodies["C11"]=blind_body_from(ents,r8)
    audit=(R.get("self_audit") or {}).get("text")
    if audit is not None and "C11" in ents and R.get("official_outcome") and R.get("C11_seal"):bodies["C12"]=c12body_from(ents,R,audit)
    for cid in CARTS:
        e=ents.get(cid)
        if not e:rows[cid]=dict(present=False);continue
        p=d/"physical_cartridges"/e["file"];row=dict(present=p.is_file(),role=e.get("role"),parents=e.get("parents"),body_tokens=e.get("body_tokens"),forge_seconds=e.get("forge_seconds"),created=e.get("created"))
        if p.is_file():
            t=time.perf_counter();s=sha_file(p);row.update(bytes=p.stat().st_size,sha256_now=s,sha256_manifest=e["sha256"],file_sha_ok=(s==e["sha256"]),hash_seconds=round(time.perf_counter()-t,2))
            cp=torch.load(p,map_location="cpu",weights_only=True);seal=ns["seal_cp"](cp)
            row["tensor_seal_ok"]=(seal["h"]==e["tensor_sha"]["h"] and [tuple(x) for x in seal["lower"]]==e["tensor_sha"]["lower"])
            h=cp["h"];k0,v0=cp["lower"][0];nb=lambda x:int(x.numel())*int(x.element_size())
            row.update(book_id_ok=(cp["book_id"]==cid),n=int(cp["n"]),p=int(cp["p"]),h_shape=list(h.shape),k_shape=list(k0.shape),lower_layers=len(cp["lower"]),h_bytes=nb(h),
                       lower_bytes=sum(nb(a)+nb(b) for a,b in cp["lower"]),full_80_layer_kv_bytes=int(cp["n"])*80*8*128*2*2)
            del cp
        b=bodies.get(cid)
        row["body_rederived"]=b is not None
        if b is not None:row.update(body_sha256_now=sha_text(b),body_sha_ok=(sha_text(b)==e.get("body_sha256")),body_chars=len(b))
        rec=(REC.get("sealed") or {}).get(cid) or {};row["record_sha256"]=rec.get("sha256");row["equal_to_record"]=(rec.get("sha256")==row.get("sha256_now")) if row.get("sha256_now") else None
        rows[cid]=row
        for k in ("file_sha_ok","tensor_seal_ok","book_id_ok","body_sha_ok"):
            if k in row and not row[k]:probs.append(f"{cid} {k}")
        slog("VERIFIED_CARTRIDGE",cid,**{k:v for k,v in row.items() if k not in("parents",)})
    seal=jload(d/"C11_BLIND_SEAL.json",{}) or {}
    lin=dict(c11_seal_file=(bool(seal) if "C11" in ents else None),c11_seal_equals_manifest=(seal.get("sha256")==(ents.get("C11") or {}).get("sha256")) if seal else None,
             c12_parent_is_c11=(((ents.get("C12") or {}).get("parents") or [{}])[0].get("sha256")==(ents.get("C11") or {}).get("sha256")) if "C12" in ents else None,
             c11_file_unchanged=rows.get("C11",{}).get("file_sha_ok"),blind_answers_hash_ok=(sha_bytes(json.dumps(R.get("blind_answers"),sort_keys=True).encode())==seal.get("blind_answers_sha256")) if seal and R.get("blind_answers") else None,
             unlock_after_c11_seal=(R.get("C11_seal",{}).get("sealed_at","")<=(next((l[2].split(" ",1)[1] for l in LINES if l[2].startswith("OFFICIAL_OUTCOME_UNLOCK")),"") or "~")) if R.get("C11_seal") else None)
    for k,v in lin.items():
        if v is False:probs.append(k)
    LIVE["verification"]=dict(cartridges=rows,lineage=lin,problems=probs,utc=utc_now());dump_json(VERIFY_FILE,LIVE["verification"])
    n_ok=sum(1 for r in rows.values() if r.get("file_sha_ok") and r.get("tensor_seal_ok") and r.get("body_sha_ok"))
    note=f"{n_ok}/{len([c for c in CARTS if c in ents])} cartridges: file SHA-256 + tensor seals + re-derived body all equal to the manifest · C12 parent = C11: {lin['c12_parent_is_c11']}"
    if probs:raise RuntimeError(note+" · PROBLEMS: "+", ".join(probs))
    return note
# ===== END OF PART 1/3 =====
# ===== PART 2/3 — paste directly after PART 1 in the same cell =====
# =====================================================================================================================
# PART 2 / 3 — six scientific figures from THIS RUN's outputs (JPEG 300 dpi, layout QC), records, SHA-256 manifest and the
#              single RUN pipeline. Every number and quote comes from this RUN's engine output; a missing output is shown
#              as missing. Quotes are cut with “…”, never reworded; full texts are in the interface and downloads.
# =====================================================================================================================
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.linewidth":.9,"axes.edgecolor":NEU,"axes.labelcolor":INK,"xtick.color":NEU,"ytick.color":NEU,
                     "xtick.labelsize":9.5,"ytick.labelsize":9.5,"axes.labelsize":10.5,"axes.titlesize":11.5,"axes.titleweight":"bold","axes.titlelocation":"left",
                     "legend.fontsize":9.5,"legend.frameon":False})
FW,FH=13.333,7.5;OUT_DPI=300;MONO="DejaVu Sans Mono"
FIGURES=OrderedDict([
    ("F1",dict(n=1,title="General Architecture",slug="GENERAL_ARCHITECTURE",tab="OVERVIEW")),
    ("F2",dict(n=2,title="Physical Memory Cartridge",slug="PHYSICAL_MEMORY_CARTRIDGE",tab="PHYSICAL CARTRIDGES")),
    ("F3",dict(n=3,title="Hierarchical Synthesis",slug="HIERARCHICAL_SYNTHESIS",tab="HIERARCHICAL SYNTHESIS")),
    ("F4",dict(n=4,title="Eight-Round Closed Loop",slug="EIGHT_ROUND_CLOSED_LOOP",tab="CLOSED LOOP")),
    ("F5",dict(n=5,title="Blind Investigation and Official Outcome",slug="BLIND_INVESTIGATION_AND_OFFICIAL_OUTCOME",tab="BLIND C11")),
    ("F6",dict(n=6,title="C11 to C12 Memory Consolidation",slug="C11_TO_C12_MEMORY_CONSOLIDATION",tab="C12 MASTER"))])
FIG_FILES={};FIG_ERRORS={};PROVENANCE={}
BADGE_COL={"SCHEMATIC":NEU,"LIVE MEASUREMENT":OK_COL,"SEALED MEMORY":COL["C11"],"OBSERVATIONAL":AMBER,"VERIFICATION RECORD":NEU,"NOT PRODUCED IN THIS RUN":RED}
def mt(s):return str(s).replace("$",r"\$")
def wrap(s,n,lines=None):
    w=textwrap.wrap(" ".join(str(s or "").split()),n,break_long_words=True,break_on_hyphens=False) or [""]
    if lines and len(w)>lines:w=w[:lines];w[-1]=w[-1].rstrip(" ,;:.")+"…"
    return "\n".join(w)
def _bb(fig,t):return t.get_window_extent(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())
def fit(fig,t,xmax=.965,minsize=6.0):
    while t.get_fontsize()>minsize and _bb(fig,t).x1>xmax:t.set_fontsize(t.get_fontsize()-.25)
    return t
def T(fig,x,y,s,size=10,color=INK,weight="normal",ha="left",va="center",xmax=None,minsize=6.0,mono=False,**kw):
    t=fig.text(x,y,mt(s),fontsize=size,color=color,weight=weight,ha=ha,va=va,family=(MONO if mono else "DejaVu Sans"),**kw)
    if xmax is not None:fit(fig,t,xmax,minsize)
    return t
def Tc(fig,x0,x1,y,s,size=9,**kw):
    """centred text that must stay inside [x0,x1] (shrinks only as far as needed)"""
    t=T(fig,(x0+x1)/2,y,s,size=size,ha="center",**kw)
    while t.get_fontsize()>6 and (_bb(fig,t).x0<x0 or _bb(fig,t).x1>x1):t.set_fontsize(t.get_fontsize()-.25)
    return t
def box(fig,x,y,w,h,ec=NEU,fc="white",lw=1.3,ls="-",r=.006,z=1):
    p=FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={r}",transform=fig.transFigure,fc=fc,ec=ec,lw=lw,ls=ls,zorder=z);p.set_gid("qc-box");fig.add_artist(p);return p
def rect(fig,x,y,w,h,fc,ec="none",lw=0,z=1):
    p=Rectangle((x,y),w,h,transform=fig.transFigure,fc=fc,ec=ec,lw=lw,zorder=z);fig.add_artist(p);return p
def arrow(fig,x0,y0,x1,y1,col=NEU,lw=1.4,ms=12,cs="arc3",ls="-"):
    a=FancyArrowPatch((x0,y0),(x1,y1),transform=fig.transFigure,arrowstyle="-|>",mutation_scale=ms,lw=lw,color=col,connectionstyle=cs,linestyle=ls,zorder=3);fig.add_artist(a);return a
def hline(fig,x0,x1,y,col=RULE,lw=.8):fig.add_artist(Line2D([x0,x1],[y,y],transform=fig.transFigure,color=col,lw=lw))
def vline(fig,x,y0,y1,col=RED,lw=1.6,ls="--"):fig.add_artist(Line2D([x,x],[y0,y1],transform=fig.transFigure,color=col,lw=lw,ls=ls,zorder=4))
def k_sha(s,n=12):return (str(s)[:n]+"…") if s else "—"
def fmt_b(b):
    if b is None:return "—"
    return f"{b/1e9:.2f} GB" if b>=1e9 else (f"{b/1e6:.1f} MB" if b>=1e6 else f"{b/1e3:.1f} kB")
def _date():return datetime.now().astimezone().strftime("%Y-%m-%d")
def fig_base(key,subtitle,badge):
    meta=FIGURES[key];fig=plt.figure(figsize=(FW,FH),dpi=100,facecolor=BG);bcol=BADGE_COL.get(badge,NEU)
    b=fig.text(.965,.952,badge,fontsize=10,weight="bold",color=bcol,va="center",ha="right",bbox=dict(boxstyle="square,pad=0.35",fc="white",ec=bcol,lw=1.2))
    bx0=_bb(fig,b).x0-.012
    T(fig,.035,.952,f"Figure {meta['n']} — {meta['title']}",size=18,weight="bold",xmax=bx0,minsize=12)
    T(fig,.035,.912,subtitle,size=11,color=INK2,xmax=.965,minsize=7.5)
    hline(fig,.035,.965,.888,INK2,.8)
    if SIM:fig.text(.5,.47,"SIMULATION — NOT EXPERIMENTAL DATA",fontsize=40,color=RED,alpha=.12,rotation=18,ha="center",va="center",weight="bold",gid="qc-ignore",zorder=100)
    return fig
def fig_footer(fig,key,note):
    meta=FIGURES[key];hline(fig,.035,.965,.072,RULE,.7)
    T(fig,.035,.050,note,size=8.8,color=INK2,xmax=.965,minsize=6.2)
    T(fig,.035,.022,f"{APP_NAME} · {EXPERIMENT} · demo {CODE_VERSION} · {_date()} · 745.py git blob {LOCKS['745.py'][:10]} · run {SESSION_ID}"+(" · SIMULATION" if SIM else "")+f" · Figure {meta['n']}/6",
      size=7.8,color=MUTED,xmax=.965,minsize=5.5,mono=True)
def _hide_offview_ticks(fig):
    for ax in fig.axes:
        for axis,(lo,hi) in ((ax.xaxis,sorted(ax.get_xlim())),(ax.yaxis,sorted(ax.get_ylim()))):
            eps=(hi-lo)*1e-6
            for tk in axis.get_major_ticks()+axis.get_minor_ticks():
                loc=tk.get_loc()
                if loc is None or loc<lo-eps or loc>hi+eps:tk.label1.set_visible(False);tk.label2.set_visible(False)
def _texts(fig):
    import matplotlib.text as mtext
    return [t for t in fig.findobj(mtext.Text) if t.get_visible() and str(t.get_text()).strip() and t.get_gid()!="qc-ignore" and t.get_alpha()!=0]
def layout_qc(fig,max_rounds=10,tol=1.5):
    """every visible text inside the page, no two texts overlapping, no text crossing a box border; offending texts are
    shrunk step by step and checked again — a figure that still fails is reported as QC FAIL"""
    W,H=fig.bbox.width,fig.bbox.height;rep=dict(rounds=0,fixed=0)
    for rnd in range(max_rounds+1):
        fig.canvas.draw();_hide_offview_ticks(fig);r=fig.canvas.get_renderer();ts=_texts(fig);bbs=[]
        for t in ts:
            b=t.get_window_extent(r);bbs.append((b.x0+tol,b.y0+tol,b.x1-tol,b.y1-tol))
        out=[i for i,b in enumerate(bbs) if b[0]<-1 or b[1]<-1 or b[2]>W+1 or b[3]>H+1];ov=[]
        boxes=[a.get_window_extent(r) for a in fig.artists if a.get_gid()=="qc-box"];cross=[]
        for i,b in enumerate(bbs):
            for B in boxes:
                inter=b[0]<B.x1 and B.x0<b[2] and b[1]<B.y1 and B.y0<b[3]
                inside=b[0]>=B.x0-1 and b[2]<=B.x1+1 and b[1]>=B.y0-1 and b[3]<=B.y1+1
                if inter and not inside:cross.append(i);break
        out=sorted(set(out)|set(cross))
        for i in range(len(bbs)):
            a=bbs[i]
            for j in range(i+1,len(bbs)):
                c=bbs[j]
                if a[0]<c[2] and c[0]<a[2] and a[1]<c[3] and c[1]<a[3]:ov.append((i,j))
        rep.update(rounds=rnd,texts=len(ts),outside=[str(ts[i].get_text())[:60] for i in out],min_font=round(min([t.get_fontsize() for t in ts] or [0]),2),
                   overlaps=[(str(ts[i].get_text())[:40],str(ts[j].get_text())[:40]) for i,j in ov][:20])
        if not out and not ov:rep["passed"]=True;return rep
        if rnd==max_rounds:break
        for i in set(out)|{x for p in ov for x in p}:
            t=ts[i]
            if t.get_fontsize()>5.5:t.set_fontsize(t.get_fontsize()-.5);rep["fixed"]+=1
    rep["passed"]=False;return rep
def jpeg_qc(path,min_w=3900,min_h=2190):
    with Image.open(path) as im:
        im.load();w,h=im.size;fmt=im.format;arr=np.asarray(im.convert("L").resize((400,int(400*h/w))),dtype=np.float32)
    ok=(fmt=="JPEG" and w>=min_w and h>=min_h and float(arr.std())>8.0 and float((arr<200).mean())>0.01)
    return dict(format=fmt,pixels=[w,h],luma_std=round(float(arr.std()),2),ink_share=round(float((arr<200).mean()),4),passed=bool(ok))
def flog_fig(m):
    with _LOG_LOCK:
        with (SESSION_DIR/"FIGURE_GENERATION.log").open("a",encoding="utf-8") as f:f.write(f"{utc_now()} {m}\n")
def save_fig(fig,key,badge,sources,suffix=""):
    qc=layout_qc(fig);meta=FIGURES[key];num=meta["n"]
    stem=("SIMULATION_" if SIM else "")+f"TEST745_FIG{num}_{meta['slug']}{suffix}";jpg=FIG_DIR/(stem+".jpg")
    buf=io.BytesIO();fig.savefig(buf,format="png",dpi=OUT_DPI,facecolor="white");plt.close(fig)
    with Image.open(io.BytesIO(buf.getvalue())) as im:im.convert("RGB").save(jpg,"JPEG",quality=95,optimize=True,subsampling=0,dpi=(OUT_DPI,OUT_DPI))
    jq=jpeg_qc(jpg)
    rec=dict(key=key,figure=num,title=meta["title"],badge=badge,tab=meta["tab"],jpg=str(jpg),pixels=jq["pixels"],sha256_jpg=sha_file(jpg),
             layout_qc=dict(passed=qc["passed"],texts=qc["texts"],rounds=qc["rounds"],font_reductions=qc["fixed"],min_font=qc.get("min_font"),overlaps=qc.get("overlaps")[:5],outside=qc.get("outside")[:5]),
             jpeg_qc=jq,data_sources=sources,utc=utc_now(),simulation=SIM)
    PROVENANCE[key]=dict(figure=num,title=meta["title"],badge=badge,data_sources=sources)
    flog_fig(f"{key} {stem} {jq['pixels']} qc={qc['passed']} sha256_jpg={rec['sha256_jpg'][:16]}")
    slog("FIGURE_WRITTEN",f"Figure {num} {stem}.jpg",pixels=jq["pixels"],dpi=OUT_DPI,layout_qc=qc["passed"],font_reductions=qc["fixed"],sha256_jpg=rec["sha256_jpg"],badge=badge);return rec
def fig_missing(key,what,why):
    fig=fig_base(key,"The output this figure is drawn from was not produced in this RUN — nothing is drawn in its place","NOT PRODUCED IN THIS RUN")
    box(fig,.16,.30,.68,.46,ec=RED,lw=1.6,ls="--")
    T(fig,.5,.67,"NOT PRODUCED IN THIS RUN",size=24,weight="bold",color=RED,ha="center")
    T(fig,.5,.57,wrap(what,95),size=12,color=INK,ha="center",linespacing=1.4)
    T(fig,.5,.43,wrap(why,105),size=10.5,color=INK2,ha="center",linespacing=1.4)
    fig_footer(fig,key,"Placeholder by design: TEST745 figures are drawn only from outputs of this RUN (no earlier run, no representative values).")
    return save_fig(fig,key,"NOT PRODUCED IN THIS RUN",["(none — output missing)"],"_NOT_PRODUCED")

# ---------------------------------------------------------------------------------------------------------------------
# quotes from the real outputs (cut, never reworded) and observational text measures
# ---------------------------------------------------------------------------------------------------------------------
def unmd(s):return re.sub(r"\s+"," ",re.sub(r"\*\*|__|`|^#+\s*","",str(s))).strip(" -")
def prose(text):
    """the running text of a model answer without markdown headings (for an opening quote)"""
    out=[]
    for ln in str(text or "").split("\n"):
        s=ln.strip()
        if not s or re.match(r"^#{1,6}\s",s) or re.match(r"^\*\*[^*]{1,80}\*\*:?$",s):continue
        out.append(unmd(re.sub(r"^\s*(?:[-*•]|\d+\.)\s+","",s)))
    return " ".join(out)
def quote(text,n):
    p=prose(text)
    if len(p)<=n:return p
    cut=p[:n];k=max(cut.rfind(". "),cut.rfind("; "))
    return (cut[:k+1] if k>n*.55 else cut.rstrip())+" …"
def uncertainty_items(text):
    """number of list items under the heading OPEN_UNCERTAINTIES (None if the section is absent)"""
    lines=str(text or "").split("\n");idx=next((i for i,l in enumerate(lines) if "OPEN_UNCERTAINTIES" in l.upper().replace(" ","_")),None)
    if idx is None:return None
    n=0
    for l in lines[idx+1:]:
        s=l.strip()
        if re.match(r"^#{1,6}\s",s) and n:break
        if re.match(r"^(?:[-*•]|\d+\.)\s+\S",s):n+=1
    return n
def similarity(a,b):
    if not a or not b:return None
    return round(difflib.SequenceMatcher(None,a.split(),b.split(),autojunk=False).ratio(),3)
def line_time(rx):
    for u,_,l in LINES:
        if re.search(rx,l):return u
    return None
def check_detail(name):
    c=next((c for c in CHECKS if c["name"]==name),None)
    if not c:return None
    try:return ast.literal_eval(c["detail"])
    except Exception:return c["detail"]
def check_ok(name):
    cs=[c for c in CHECKS if c["name"]==name];return None if not cs else all(c["passed"] for c in cs)
def _ents():return run_manifest().get("cartridges") or {}
def _v(cid):return ((LIVE.get("verification") or {}).get("cartridges") or {}).get(cid) or {}

# ---------------------------------------------------------------------------------------------------------------------
# Figure 1 — General Architecture
# ---------------------------------------------------------------------------------------------------------------------
def _node(fig,x,y,w,h,cid,lines,col):
    box(fig,x,y,w,h,ec=col,lw=1.6);rect(fig,x,y+h-.028,w,.028,col,z=2)
    Tc(fig,x+.004,x+w-.004,y+h-.014,cid,size=9.5,weight="bold",color="white")
    for i,s in enumerate(lines):Tc(fig,x+.004,x+w-.004,y+h-.045-i*.024,s,size=7.6,color=INK2,mono=(i==len(lines)-1))
def fig1():
    k="F1";E_=_ents();R=run_results()
    if "C01" not in E_:return fig_missing(k,"The architecture is drawn from the cartridges this RUN sealed (manifest).","No cartridge was sealed in this RUN.")
    fig=fig_base(k,"The architecture TEST745 actually ran in this session — physical CUT3 cartridges (boxes) and text-mediated synthesis (dashed arrows) · values from this RUN","SCHEMATIC")
    def lines(c):
        e=E_.get(c);return [f"{e['body_tokens']:,} tokens",f"SHA {k_sha(e['sha256'],10)}"] if e else ["not produced","—"]
    pre=R.get("preliminary") or {}
    box(fig,.035,.43,.1,.30,ec=NEU,lw=1.3,fc=PANEL);Tc(fig,.037,.133,.705,"AIN preliminary",size=8.6,weight="bold");Tc(fig,.037,.133,.68,"report (PDF)",size=8.6,weight="bold")
    Tc(fig,.037,.133,.64,f"{pre.get('pages','—')} pages",size=7.8,color=INK2);Tc(fig,.037,.133,.615,f"SHA {k_sha(pre.get('pdf_sha256'),10)}",size=7.2,color=MUTED,mono=True)
    Tc(fig,.037,.133,.56,"split in document",size=7.4,color=INK2);Tc(fig,.037,.133,.54,"order into 3 parts",size=7.4,color=INK2);Tc(fig,.037,.133,.50,"(ONE report, not",size=7.4,color=AMBER);Tc(fig,.037,.133,.48,"3 independent ones)",size=7.4,color=AMBER)
    ys=[.66,.48,.30];W=.085;Hh=.11;X={"C":.16,"S":.285,"H":.41}
    for j,c in enumerate(SRC):_node(fig,X["C"],ys[j],W,Hh,c,lines(c),COL["C"]);arrow(fig,.136,.58,X["C"]-.002,ys[j]+Hh/2,col=NEU,lw=1.0,ms=9)
    for j,s in enumerate(SUB):
        _node(fig,X["S"],ys[j],W,Hh,s,lines(s),COL["S"])
        for p in GROUPS[s]:arrow(fig,X["C"]+W+.002,ys[SRC.index(p)]+Hh/2,X["S"]-.002,ys[j]+Hh/2,col=COL["S"],lw=1.0,ms=9,ls="--")
    for j,h in enumerate(CRS):
        _node(fig,X["H"],ys[j],W,Hh,h,lines(h),COL["H"])
        for p in HIER[h]:arrow(fig,X["S"]+W+.002,ys[SUB.index(p)]+Hh/2,X["H"]-.002,ys[j]+Hh/2,col=COL["H"],lw=1.0,ms=9,ls="--")
    box(fig,.535,.36,.105,.32,ec=COL["LOOP"],lw=1.4,ls="--",fc=PANEL)
    nr=len(R.get("blind_rounds") or [])
    Tc(fig,.537,.638,.655,"CLOSED LOOP",size=8.8,weight="bold");Tc(fig,.537,.638,.625,"initial hypothesis",size=7.6,color=INK2)
    Tc(fig,.537,.638,.60,f"+ {nr} review rounds",size=7.6,color=INK2);Tc(fig,.537,.638,.575,"(limit 8, text only;",size=7.2,color=MUTED);Tc(fig,.537,.638,.555,"no official outcome)",size=7.2,color=MUTED)
    for j in range(3):arrow(fig,X["H"]+W+.002,ys[j]+Hh/2,.533,.52,col=COL["H"],lw=1.0,ms=9,ls="--")
    _node(fig,.665,.41,.095,.22,"C11 BLIND",lines("C11")[:1]+["MASTER — sealed","before outcome"]+lines("C11")[1:],COL["C11"])
    arrow(fig,.642,.52,.663,.52,col=COL["C11"],lw=1.4)
    vline(fig,.785,.14,.80,col=RED);T(fig,.787,.80,"EMBARGO",size=8,weight="bold",color=RED);T(fig,.787,.78,"final report opened",size=7,color=RED);T(fig,.787,.765,"only after C11 seal",size=7,color=RED)
    off=R.get("official_outcome") or {}
    box(fig,.80,.60,.165,.13,ec=COL["OFF"],lw=1.3);Tc(fig,.802,.963,.705,"AIN final report (PDF)",size=8.4,weight="bold",color=COL["OFF"])
    Tc(fig,.802,.963,.675,f"{off.get('pages','—')} pages · downloaded after seal",size=7.4,color=INK2);Tc(fig,.802,.963,.645,f"SHA {k_sha(off.get('pdf_sha256'),10)}",size=7.2,color=MUTED,mono=True)
    box(fig,.80,.45,.165,.11,ec=AMBER,lw=1.2,ls="--");Tc(fig,.802,.963,.525,"model self-audit",size=8.4,weight="bold",color=AMBER);Tc(fig,.802,.963,.495,"(model claim — not expert",size=7.2,color=INK2);Tc(fig,.802,.963,.475,"grading)",size=7.2,color=INK2)
    _node(fig,.80,.25,.165,.16,"C12 POST-OUTCOME",[("human review PENDING"),lines("C12")[0],"parent: C11 SHA",lines("C12")[1]][:3]+[lines("C12")[1]],COL["C12"])
    arrow(fig,.762,.52,.798,.665,col=COL["C11"],lw=1.0,ms=9,cs="arc3,rad=-.1");arrow(fig,.8825,.598,.8825,.562,col=NEU,lw=1.0,ms=9);arrow(fig,.8825,.448,.8825,.412,col=NEU,lw=1.0,ms=9)
    box(fig,.035,.10,.74,.13,ec=NEU,lw=1.2,fc=PANEL)
    T(fig,.045,.205,"Frozen Qwen2.5-72B-Instruct (NF4, BF16) — weights never changed · locked TEST709 / TEST730 engine functions · CUT3",size=9.2,weight="bold",xmax=.77)
    T(fig,.045,.175,"every box: native CUT3 forge (H3 + K/V of layers 0–3) → torch.save on the SSD → SHA-256 of the file and of the tensors",size=8.2,color=INK2,xmax=.77)
    T(fig,.045,.15,"every dashed arrow: the cartridge is mounted (80 layers rebuilt) and READ by the model → the readouts are synthesized as TEXT → forged as a new cartridge",size=8.2,color=INK2,xmax=.77)
    T(fig,.045,.125,"no direct BF16 tensor fusion of cartridges takes place in TEST745",size=8.2,color=AMBER,weight="bold",xmax=.77)
    fig_footer(fig,k,"Token counts and SHA-256 values: TEST745_manifest.json of this RUN. C01–C03 are consecutive parts of one AIN preliminary report. C12 carries the C11 file SHA-256 as parent.")
    return save_fig(fig,k,"SCHEMATIC",["TEST745_manifest.json (this RUN)","TEST745_results.json (preliminary, official_outcome, blind_rounds)"])

# ---------------------------------------------------------------------------------------------------------------------
# Figure 2 — Physical Memory Cartridge
# ---------------------------------------------------------------------------------------------------------------------
def fig2():
    k="F2";V=(LIVE.get("verification") or {}).get("cartridges") or {}
    if not any(v.get("present") for v in V.values()):return fig_missing(k,"Shapes, sizes and seals are measured from the cartridge files of this RUN (stage 13).","No cartridge file of this RUN was verified.")
    fig=fig_base(k,"What one cartridge physically holds, how it is stored and how it is mounted again — sizes measured from this RUN's files","LIVE MEASUREMENT")
    steps=[("1  FORGE","forward pass L0–L79 · H3 captured at\nthe layer-3 boundary (direct forward)"),("2  PERSIST","torch.save → SSD · SHA-256 of the\nfile and of every tensor"),
           ("3  RELOAD","file SHA · tensor seals · cartridge ID\nchecked before every use"),("4  INJECT + REBUILD","H3 injected at layer 3 · layers 4–79\nrecomputed by the frozen model"),
           ("5  READ","the question is appended to the\n80-layer K/V memory · greedy decoding")]
    for i,(h,t) in enumerate(steps):
        x=.035+i*.188;box(fig,x,.735,.172,.13,ec=NEU,fc=PANEL,lw=1.2)
        T(fig,x+.01,.84,h,size=10,weight="bold",xmax=x+.168);T(fig,x+.01,.78,t,size=8,color=INK2,linespacing=1.25,xmax=x+.168)
        if i<4:arrow(fig,x+.173,.80,x+.187,.80,col=NEU,lw=1.3,ms=10)
    x0,x1=.06,.94;w=(x1-x0)/80
    for L in range(80):rect(fig,x0+L*w+.0008,.645,w-.0016,.04,OK_COL if L<=3 else "#E5E7EB",z=2)
    fig.add_artist(Line2D([x0+4*w,x0+4*w],[.635,.695],transform=fig.transFigure,color=COL["C11"],lw=2.2,zorder=4))
    T(fig,x0+4*w+.004,.708,"CUT3 boundary — H3 is injected here at mount time",size=8.4,weight="bold",color=COL["C11"])
    T(fig,x0,.62,"stored: H3 + K/V of layers 0–3",size=8.4,weight="bold",color=OK_COL)
    T(fig,x0+.25,.62,"layers 4–79: NOT stored — recomputed by the frozen model each time the cartridge is mounted",size=8.2,color=INK2,xmax=.96)
    cards=[("Not text RAG","stored are internal model states (H3, K/V L0–3), not text pasted into the prompt"),
           ("Not fine-tuning","the weights stay frozen — sentinel unchanged: "+("PASS" if check_ok("FROZEN_SENTINEL_UNCHANGED") else "—")),
           ("Not a full transformer bypass","layers 4–79 and decoding still run; early layers are reused from the stored states")]
    for i,(h,t) in enumerate(cards):
        x=.035+i*.315;box(fig,x,.515,.30,.075,ec=AMBER if i==2 else NEU,lw=1.1)
        T(fig,x+.008,.572,h,size=8.8,weight="bold",xmax=x+.296);T(fig,x+.008,.538,t,size=7.4,color=INK2,xmax=x+.296)
    hd=["cartridge","rows n","H3 tensor","H3 + L0–L3 bytes","file on SSD","full 80-layer K/V","reloads","file · tensor · body","SHA-256 (file)"]
    xs=[.035,.11,.17,.32,.42,.505,.60,.66,.80];y=.475
    for x,h in zip(xs,hd):T(fig,x,y,h,size=7.6,weight="bold",color=MUTED)
    hline(fig,.035,.965,y-.013,RULE)
    for j,c in enumerate(CARTS):
        v=V.get(c) or {};yy=y-.035-j*.0325;T(fig,.035,yy,c,size=8.4,weight="bold",color=ccol(c))
        if not v.get("present"):T(fig,.11,yy,"not produced in this RUN",size=7.8,color=RED);continue
        reloads=sum(1 for ch in CHECKS if ch["name"]==f"FILE_SHA_{c}" and ch["passed"])
        ok=lambda b:"✓" if b else ("✗" if b is False else "–")
        vals=[f"{v['n']:,}",f"{tuple(v['h_shape'])}",fmt_b(v["h_bytes"]+v["lower_bytes"]),fmt_b(v["bytes"]),fmt_b(v["full_80_layer_kv_bytes"]),str(reloads),
              f"{ok(v.get('file_sha_ok'))} · {ok(v.get('tensor_seal_ok'))} · {ok(v.get('body_sha_ok'))}",k_sha(v["sha256_now"],16)]
        for x,val,nx in zip(xs[1:],vals,xs[2:]+[.965]):T(fig,x,yy,val,size=7.6,mono=True,xmax=nx-.005)
    fig_footer(fig,k,"Measured now from the files (torch.load on the CPU, read-only). Full 80-layer K/V = n × 80 × 8 heads × 128 × 2 (K,V) × 2 bytes. Reloads = PASS FILE_SHA lines of this RUN's engine output.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["physical_cartridges/*.pt of this RUN (read-only)","POST_RUN_VERIFICATION.json","ENGINE_OUTPUT_REALTIME.log (FILE_SHA checks)"])

# ---------------------------------------------------------------------------------------------------------------------
# Figure 3 — Hierarchical Synthesis
# ---------------------------------------------------------------------------------------------------------------------
def fig3():
    k="F3";E_=_ents();gi=generation_index()
    if not all(c in E_ for c in SRC+SUB+CRS):return fig_missing(k,"The hierarchy C01–C03 → S01–S03 → H01–H03 → C11 is drawn from this RUN's sealed cartridges and readouts.","Not every cartridge of the hierarchy was sealed in this RUN.")
    fig=fig_base(k,"Physical storage (solid boxes) and text-mediated synthesis (dashed arrows) are separate steps · token counts measured in this RUN","SCHEMATIC")
    def rd(cid,role_part=None):
        xs=[g for g in gi if g["cid"]==cid and g["kind"]=="readout" and (role_part is None or role_part in g.get("role",""))];return sum((g.get("tokens") or 0) for g in xs),len(xs)
    cols=[(.06,SRC,COL["C"],"SOURCE CARTRIDGES"),(.31,SUB,COL["S"],"SUBSYSTEM SYNTHESES"),(.56,CRS,COL["H"],"CROSS-SYSTEM SYNTHESES")]
    ys=[.66,.47,.28];W=.19;Hh=.14
    for x,ids,col,lab in cols:
        T(fig,x,.855,lab,size=9.5,weight="bold",color=MUTED)
        for j,c in enumerate(ids):
            e=E_[c];box(fig,x,ys[j],W,Hh,ec=col,lw=1.6);rect(fig,x,ys[j]+Hh-.03,W,.03,col,z=2)
            T(fig,x+.008,ys[j]+Hh-.015,f"{c} · physical cartridge",size=9,weight="bold",color="white",xmax=x+W-.005)
            T(fig,x+.008,ys[j]+.075,f"body {e['body_tokens']:,} tokens · forged {e.get('forge_seconds','—')} s",size=7.8,color=INK2,xmax=x+W-.005)
            if c in SRC:t,n=rd(c);T(fig,x+.008,ys[j]+.05,f"read alone: {t:,} tokens written by the model",size=7.6,color=INK2,xmax=x+W-.005)
            else:
                d=check_detail("SYNTHESIS_CONTEXT_FITS_"+c);t,n=rd(c)
                T(fig,x+.008,ys[j]+.05,f"synthesis prompt {d.get('tokens','—') if isinstance(d,dict) else '—'} tokens (TEXT)",size=7.6,color=INK2,xmax=x+W-.005)
                T(fig,x+.008,ys[j]+.03,f"read back {n}× · {t:,} tokens in total",size=7.6,color=INK2,xmax=x+W-.005) if n else None
            T(fig,x+.008,ys[j]+.01,f"SHA {k_sha(e['sha256'],22)}",size=7.0,color=MUTED,mono=True,xmax=x+W-.005)
    for j,s in enumerate(SUB):
        for p in GROUPS[s]:arrow(fig,.06+W+.002,ys[SRC.index(p)]+Hh/2,.31-.002,ys[j]+Hh/2,col=COL["S"],lw=1.1,ms=9,ls="--")
    for j,h in enumerate(CRS):
        for p in HIER[h]:arrow(fig,.31+W+.002,ys[SUB.index(p)]+Hh/2,.56-.002,ys[j]+Hh/2,col=COL["H"],lw=1.1,ms=9,ls="--")
    box(fig,.80,.42,.165,.30,ec=COL["C11"],lw=1.6,ls="--",fc=PANEL);T(fig,.81,.695,"→ INITIAL hypothesis",size=9,weight="bold",color=COL["C11"],xmax=.96)
    d=check_detail("SYNTHESIS_CONTEXT_FITS_INITIAL");ini=next((g for g in gi if g["cid"]=="INITIAL"),{})
    T(fig,.81,.665,f"from H01–H03 readouts",size=7.8,color=INK2,xmax=.96);T(fig,.81,.64,f"prompt {d.get('tokens','—') if isinstance(d,dict) else '—'} tokens",size=7.8,color=INK2,xmax=.96)
    T(fig,.81,.615,f"answer {ini.get('tokens','—')} tokens",size=7.8,color=INK2,xmax=.96);T(fig,.81,.575,"→ 8 closed-loop rounds",size=8.6,weight="bold",color=COL["C11"],xmax=.96)
    T(fig,.81,.545,"→ C11 BLIND MASTER",size=8.6,weight="bold",color=COL["C11"],xmax=.96);T(fig,.81,.515,f"C11 SHA {k_sha((E_.get('C11') or {}).get('sha256'),10)}",size=7.2,color=MUTED,mono=True,xmax=.96)
    T(fig,.81,.48,"(Figures 4 and 5)",size=7.6,color=MUTED,xmax=.96)
    for j in range(3):arrow(fig,.56+W+.002,ys[j]+Hh/2,.798,.57,col=COL["H"],lw=1.0,ms=9,ls="--")
    box(fig,.035,.10,.93,.12,ec=NEU,lw=1.1,fc=PANEL)
    T(fig,.045,.195,"solid box = physical CUT3 cartridge on the SSD (forge_native → torch.save → SHA-256) — the memory itself",size=8.4,color=INK,xmax=.96)
    T(fig,.045,.165,"dashed arrow = the parent cartridge is mounted alone (80 layers) and read by the model; the readouts become a TEXT prompt; the synthesis TEXT is forged as the child",size=8.4,color=INK,xmax=.96)
    T(fig,.045,.135,"S01–S03 synthesize the source reflections; H01–H03 read the S cartridges physically again (not the original documents) — no tensor of two cartridges is ever fused",size=8.4,color=AMBER,xmax=.96)
    fig_footer(fig,k,"Token counts: manifest (body), engine output (SYNTHESIS_CONTEXT_FITS, GENERATION) and TEST745_results.json generations of this RUN. Full texts: HIERARCHICAL SYNTHESIS tab.")
    return save_fig(fig,k,"SCHEMATIC",["TEST745_manifest.json","TEST745_results.json generations","ENGINE_OUTPUT_REALTIME.log"])

# ---------------------------------------------------------------------------------------------------------------------
# Figure 4 — Eight-Round Closed Loop
# ---------------------------------------------------------------------------------------------------------------------
def loop_measures():
    R=run_results();rt=round_texts();rounds=R.get("blind_rounds") or [];gi=generation_index()
    ini=next((g for g in gi if g["cid"]=="INITIAL"),{})
    toks=[ini.get("tokens")]+[next((r["tokens"] for r in rounds if r["round"]==i),None) for i in range(1,9)]
    sims=[None]+[similarity(rt[i-1][1],rt[i][1]) for i in range(1,9)]
    unc=[uncertainty_items(t) for _,t in rt]
    times=[line_time(r"^PASS SYNTHESIS_NOT_TRUNCATED_INITIAL")]+[line_time(rf"^PASS LOOP_NONEMPTY_{i}\b") for i in range(1,9)]
    def dt(a,b):
        try:return round((datetime.fromisoformat(b)-datetime.fromisoformat(a)).total_seconds(),1)
        except Exception:return None
    secs=[None]+[dt(times[i-1],times[i]) if times[i-1] and times[i] else None for i in range(1,9)]
    return dict(labels=[l for l,_ in rt],texts=[t for _,t in rt],tokens=toks,similarity_to_previous=sims,open_uncertainty_items=unc,seconds=secs,
                note="observational text measures of this RUN — no quality or accuracy score")
def fig4():
    k="F4";M=loop_measures()
    if not M["texts"][0] or not any(M["texts"][1:]):return fig_missing(k,"The closed loop is drawn from the initial hypothesis and the round texts written in this RUN.","No closed-loop round text exists in this RUN.")
    LIVE["loop"]={kk:v for kk,v in M.items() if kk!="texts"};dump_json(DATA_DIR/"CLOSED_LOOP_MEASURES.json",LIVE["loop"])
    fig=fig_base(k,"Initial blind hypothesis and eight review rounds written in this RUN · observational measures of the real texts — not a quality score; improvement is not assumed","OBSERVATIONAL")
    lab=M["labels"];x=np.arange(len(lab))
    ax=fig.add_axes([.06,.53,.25,.29]);tk=[v or 0 for v in M["tokens"]];ax.bar(x,tk,color=[COL["C11"]]+[NEU]*8,width=.65)
    ax.set_xticks(x);ax.set_xticklabels(lab,fontsize=7.6);ax.set_title("length of each analysis (tokens)",fontsize=9.5);ax.set_ylim(0,max(tk+[1])*1.18)
    ax2=fig.add_axes([.38,.53,.25,.29]);sv=[v if v is not None else 0 for v in M["similarity_to_previous"]];ax2.bar(x[1:],sv[1:],color=AMBER,width=.65)
    ax2.set_xticks(x);ax2.set_xticklabels(lab,fontsize=7.6);ax2.set_ylim(0,1.08);ax2.set_title("word-sequence similarity to the previous text",fontsize=9.5)
    for xi,v in zip(x[1:],M["similarity_to_previous"][1:]):
        if v is not None:ax2.text(xi,v+.02,f"{v:.2f}",ha="center",fontsize=6.8)
    ax3=fig.add_axes([.70,.53,.26,.29]);uv=[v if v is not None else 0 for v in M["open_uncertainty_items"]]
    ax3.bar(x,uv,color=[RULE if v is None else "#64748B" for v in M["open_uncertainty_items"]],width=.65);ax3.set_xticks(x);ax3.set_xticklabels(lab,fontsize=7.6)
    ax3.set_title("items listed under OPEN_UNCERTAINTIES",fontsize=9.5);ax3.set_ylim(0,max(uv+[1])*1.25)
    for xi,v in zip(x,M["open_uncertainty_items"]):ax3.text(xi,(v or 0)+.05,"—" if v is None else str(v),ha="center",fontsize=6.8)
    for a in (ax,ax2,ax3):
        for s in ("top","right"):a.spines[s].set_visible(False)
        a.tick_params(labelsize=7.6)
    sec=[s for s in M["seconds"] if s];T(fig,.06,.465,("round duration (engine output receipt times): "+" · ".join(f"{l} {s:.0f} s" for l,s in zip(lab[1:],M["seconds"][1:]) if s)) if sec else "round durations: not available",size=7.6,color=MUTED,xmax=.96)
    last=next((i for i in range(8,0,-1) if M["texts"][i]),0)
    for j,(i,head,col) in enumerate(((0,"INITIAL blind hypothesis — opening (quoted, shortened)",COL["C11"]),(last,f"{lab[last]} — final round written to C11 — opening (quoted, shortened)",NEU))):
        xx=.035+j*.47;box(fig,xx,.10,.455,.33,ec=col,lw=1.4)
        T(fig,xx+.01,.41,head,size=8.8,weight="bold",color=col,xmax=xx+.45)
        T(fig,xx+.01,.385,"“"+wrap(quote(M["texts"][i],1000),84,14)+"”",size=7.8,color=INK,va="top",linespacing=1.18,xmax=xx+.45)
    fig_footer(fig,k,"Similarity = difflib ratio of the word sequences (how much text was kept, not whether it became more correct). Uncertainty items: list lines under the OPEN_UNCERTAINTIES heading; “—” = heading absent.")
    return save_fig(fig,k,"OBSERVATIONAL",["generated_text/INITIAL_synthesis.txt","generated_text/blind_round_01–08.txt","TEST745_results.json blind_rounds","CLOSED_LOOP_MEASURES.json"])

# ---------------------------------------------------------------------------------------------------------------------
# Figure 5 — Blind Investigation and Official Outcome
# ---------------------------------------------------------------------------------------------------------------------
def fig5():
    k="F5";R=run_results();ba=R.get("blind_answers") or []
    if not ba:return fig_missing(k,"The blind phase is drawn from the three answers C11 gave in this RUN before the official report was opened.","C11 did not answer in this RUN.")
    fig=fig_base(k,"C11 is sealed and answers three questions BEFORE the AIN final report is downloaded · chronological access boundary measured from this RUN's engine output","SEALED MEMORY")
    ev=[("C11 sealed",line_time(r"^PHYSICAL_SEALED C11 "),COL["C11"])]
    gts=[u for u,_,l in LINES if l.startswith("GENERATION C11 ")]
    ev+=[(f"blind answer Q{i+1}",u,COL["C11"]) for i,u in enumerate(gts[:3])]
    ev+=[("C11 locked before final",line_time(r"^PASS C11_LOCKED_BEFORE_FINAL"),COL["C11"]),("OUTCOME UNLOCKED",line_time(r"^OFFICIAL_OUTCOME_UNLOCK"),RED),
         ("final report downloaded",line_time(r"final_report\.pdf"),RED),("self-audit written",line_time(r"^PASS AUDIT_NOT_TRUNCATED"),AMBER),("C12 sealed",line_time(r"^PHYSICAL_SEALED C12 "),COL["C12"])]
    ev=[(a,datetime.fromisoformat(b),c) for a,b,c in ev if b]
    if ev:
        x0,x1=.07,.93;hline(fig,x0-.02,x1+.02,.72,NEU,1.4);n=len(ev);step=(x1-x0)/max(n-1,1)
        for i,(a,t,c) in enumerate(ev):
            xx=x0+i*step;fig.add_artist(Line2D([xx],[.72],transform=fig.transFigure,marker="o",ms=6,color=c))
            Tc(fig,xx-step/2+.003,xx+step/2-.003,.765,a,size=7.6,color=c,weight="bold" if a=="OUTCOME UNLOCKED" else "normal")
            Tc(fig,xx-step/2+.003,xx+step/2-.003,.675,t.strftime("%H:%M:%S"),size=7.2,color=MUTED,mono=True)
            if a=="OUTCOME UNLOCKED":vline(fig,xx-step/2,.62,.82)
        span=(ev[-1][1]-ev[0][1]).total_seconds()
        T(fig,.06,.855,f"events in order of occurrence (evenly spaced) · times = UTC receipt of the engine output line in this RUN · span {span/60:.1f} min · red line = access boundary",size=7.8,color=MUTED,xmax=.96)
    box(fig,.035,.10,.455,.48,ec=COL["C11"],lw=1.4);T(fig,.045,.56,"BLIND — answers of C11 alone, before the official report (quoted, shortened)",size=8.6,weight="bold",color=COL["C11"],xmax=.485)
    for i,a in enumerate(ba[:3]):
        y=.525-i*.145;T(fig,.045,y,f"Q{i+1} · "+short(a["question"],92),size=7.4,weight="bold",color=INK,xmax=.485)
        T(fig,.045,y-.018,"“"+wrap(quote(a["answer"],330),86,5)+"”",size=7.0,color=INK2,va="top",linespacing=1.12,xmax=.485)
    ex=raw_of("AIN_FINAL_EVALUATION_EXCERPT.txt") or "";fx=ex.split("[OFFICIAL FINDINGS EXCERPT]",1)[-1] if ex else ""
    box(fig,.51,.33,.455,.25,ec=COL["OFF"],lw=1.4);T(fig,.52,.56,"OFFICIAL — AIN final report, findings excerpt given to the model after the seal",size=8.4,weight="bold",color=COL["OFF"],xmax=.96)
    T(fig,.52,.535,("“"+wrap(" ".join(fx.split())[:600]+" …",92,8)+"”") if fx else "excerpt file not available in this RUN",size=7.0,color=INK2,va="top",linespacing=1.12,xmax=.96)
    sa=(R.get("self_audit") or {}).get("text")
    box(fig,.51,.10,.455,.21,ec=AMBER,lw=1.4,ls="--");T(fig,.52,.29,"MODEL SELF-AUDIT — the model's own claim, NOT independent expert grading",size=8.4,weight="bold",color=AMBER,xmax=.96)
    T(fig,.52,.265,("“"+wrap(quote(sa,440),92,6)+"”") if sa else "self-audit not produced in this RUN",size=7.0,color=INK2,va="top",linespacing=1.12,xmax=.96)
    fig_footer(fig,k,"Questions: blind_questions of 745.py (fixed before the run). Official text: AIN_FINAL_EVALUATION_EXCERPT.txt as built by 745.py. Correctness of the blind answers is not graded here.")
    return save_fig(fig,k,"SEALED MEMORY",["TEST745_results.json blind_answers, self_audit","sealed_sources/AIN_FINAL_EVALUATION_EXCERPT.txt","ENGINE_OUTPUT_REALTIME.log (receipt times)"])

# ---------------------------------------------------------------------------------------------------------------------
# Figure 6 — C11 to C12 Memory Consolidation
# ---------------------------------------------------------------------------------------------------------------------
def fig6():
    k="F6";E_=_ents();R=run_results();V=LIVE.get("verification") or {};lin=V.get("lineage") or {}
    if "C12" not in E_:return fig_missing(k,"The consolidation is drawn from the C11 and C12 cartridges sealed in this RUN.","C12 was not sealed in this RUN.")
    fig=fig_base(k,"C12 is a NEW physical cartridge: C11 stays unchanged and is referenced by its SHA-256 · the model self-audit is not expert grading · human review PENDING","SEALED MEMORY")
    c11=E_["C11"];c12=E_["C12"];off=R.get("official_outcome") or {};sa=R.get("self_audit") or {};seal=R.get("C11_seal") or {}
    _node(fig,.035,.53,.19,.29,"C11 BLIND MASTER",[f"{c11['body_tokens']:,} tokens","sealed "+str(seal.get("sealed_at",""))[11:19]+" UTC",f"role {c11.get('role')}",f"{c11['sha256'][:22]}"],COL["C11"])
    _node(fig,.035,.18,.19,.25,"AIN FINAL REPORT",[f"{off.get('pages','—')} pages (PDF)","opened after the C11 seal",f"{str(off.get('pdf_sha256'))[:22]}"],COL["OFF"])
    sat=len(str(sa.get("text","")))
    _node(fig,.30,.36,.19,.29,"MODEL SELF-AUDIT",["model compares its sealed","predictions with the findings",f"{sat:,} characters","(model claim — not grading)",f"{str(sa.get('sha256'))[:22]}"],AMBER)
    _node(fig,.30,.10,.19,.20,"HUMAN REVIEW",["status: NOT PROVIDED","(pending — none fabricated)"," "],NEU)
    _node(fig,.57,.36,.19,.40,"C12 POST-OUTCOME",[f"{c12['body_tokens']:,} tokens","role HUMAN_AI_MASTER_","HUMAN_REVIEW_PENDING","parent = C11 file SHA-256:",f"{(c12.get('parents') or [{}])[0].get('sha256','')[:22]}","C12 file SHA-256:",f"{c12['sha256'][:22]}"],COL["C12"])
    arrow(fig,.227,.675,.298,.55,col=COL["C11"]);arrow(fig,.227,.30,.298,.45,col=COL["OFF"]);arrow(fig,.492,.505,.568,.56,col=AMBER);arrow(fig,.492,.20,.568,.42,col=NEU,ls="--")
    arrow(fig,.227,.78,.568,.72,col=COL["C11"],ls=":",cs="arc3,rad=-.15")
    T(fig,.30,.845,"parent SHA-256 reference — C11 itself is not modified",size=7.8,color=COL["C11"],xmax=.76)
    rows=[("C11 locked before final report (engine)",check_ok("C11_LOCKED_BEFORE_FINAL")),("C11 immutable after C12 (engine)",check_ok("C11_IMMUTABLE")),
          ("C12 parent = C11 SHA-256 (engine)",check_ok("C12_PARENT_SHA")),("frozen weights unchanged (engine)",check_ok("FROZEN_SENTINEL_UNCHANGED")),
          ("C11 file re-hashed now = manifest (demo)",_v("C11").get("file_sha_ok")),("C12 body re-derived = manifest body hash (demo)",_v("C12").get("body_sha_ok")),
          ("C12 parent link re-checked (demo)",lin.get("c12_parent_is_c11")),("blind answers hash = C11 seal (demo)",lin.get("blind_answers_hash_ok"))]
    box(fig,.785,.10,.18,.72,ec=OK_COL,lw=1.3);T(fig,.795,.80,"integrity of the lineage",size=9,weight="bold",color=OK_COL,xmax=.96)
    for i,(l,v) in enumerate(rows):
        y=.755-i*.08;T(fig,.795,y,"PASS" if v else ("FAIL" if v is False else "—"),size=9.5,weight="bold",color=OK_COL if v else (RED if v is False else MUTED))
        T(fig,.795,y-.028,wrap(l,30,2),size=7.0,color=INK2,va="center",linespacing=1.1,xmax=.96)
    fig_footer(fig,k,"engine = PASS lines of this RUN's 745.py output · demo = independent read-only re-verification after the run (POST_RUN_VERIFICATION.json). C12 body = the exact 745.py expression, re-derived.")
    return save_fig(fig,k,"SEALED MEMORY",["TEST745_manifest.json","TEST745_results.json","C11_BLIND_SEAL.json","POST_RUN_VERIFICATION.json","ENGINE_OUTPUT_REALTIME.log"])

FIG_FUNCS=OrderedDict([("F1",fig1),("F2",fig2),("F3",fig3),("F4",fig4),("F5",fig5),("F6",fig6)])
def render_figures():
    errs={}
    for key,fn in FIG_FUNCS.items():
        t=time.perf_counter()
        try:
            rec=fn();FIG_FILES[key]=rec;STATE["fig_version"]+=1;bump()
            _emit(f"  figure {FIGURES[key]['n']} · {rec['badge']} · {rec['pixels'][0]}×{rec['pixels'][1]} · layout QC {'pass' if rec['layout_qc']['passed'] else 'FAIL'} · {time.perf_counter()-t:.1f} s")
        except Exception as ex:
            errs[key]=f"{type(ex).__name__}: {ex}";FIG_FILES.pop(key,None);flog_fig(f"{key} NOT GENERATED {traceback.format_exc()[-1500:]}");_emit(f"  figure {key} NOT GENERATED · {errs[key]}");plt.close("all")
    FIG_ERRORS.clear();FIG_ERRORS.update(errs)
    dump_json(SESSION_DIR/"FIGURES_MANIFEST.json",dict(session=SESSION_ID,utc=utc_now(),simulation=SIM,figures=FIG_FILES,not_generated=errs))
    return errs
def stage_figures():
    errs=render_figures();n=len(FIG_FILES)
    qcf=[k for k,v in FIG_FILES.items() if not (v.get("layout_qc") or {}).get("passed") or not (v.get("jpeg_qc") or {}).get("passed")]
    np_=[k for k,v in FIG_FILES.items() if v["badge"]=="NOT PRODUCED IN THIS RUN"]
    note=f"{n}/{len(FIGURES)} JPEG figures written (300 dpi)"
    if errs or qcf or np_:raise RuntimeError(note+(f" · NOT GENERATED: {errs}" if errs else "")+(f" · LAYOUT/JPEG QC FAILED: {', '.join(qcf)}" if qcf else "")+(f" · drawn as NOT PRODUCED: {', '.join(np_)}" if np_ else ""))
    return note+" · layout QC and JPEG QC passed for every figure"

# ---------------------------------------------------------------------------------------------------------------------
# records: run summary, SHA-256 manifest, direct downloads (no ZIP)
# ---------------------------------------------------------------------------------------------------------------------
def run_verdict():
    st=STATE["stages"];bad=[k for k,v in st.items() if v["status"] in("fail","skip")]
    if STATE.get("running"):return "RUNNING"
    if not STATE.get("finished"):return "NOT STARTED"
    if not bad:return "COMPLETE — every stage ran and passed"
    return "INCOMPLETE — not a completed live experiment: "+", ".join(f"{k} {st[k]['status'].upper()}" for k in bad)
CLAIMS=[("Physical cartridge mechanism worked","technical",lambda:all(_v(c).get("file_sha_ok") and _v(c).get("tensor_seal_ok") for c in CARTS) if LIVE.get("verification") else None),
        ("Hierarchical synthesis completed","technical",lambda:all(c in _ents() for c in SUB+CRS) or None),
        ("Closed-loop rounds executed","technical",lambda:(len(run_results().get("blind_rounds") or [])==8) or None),
        ("Blind C11 sealed before the official report","technical",lambda:check_ok("C11_LOCKED_BEFORE_FINAL")),
        ("C12 created after the official report (parent C11)","technical",lambda:check_ok("C12_PARENT_SHA")),
        ("Causal correctness of the blind analysis","needs independent evaluation",lambda:None),
        ("The model's ability to recognize its own errors","needs independent evaluation",lambda:None)]
def write_run_summary():
    L=[];a=L.append;R=run_results()
    a(f"{APP_NAME} — {APP_SUB}\n{EXPERIMENT} live demonstration · demo {CODE_VERSION} · RUN {SESSION_ID} · written {local_now()}")
    if SIM:a("SIMULATION — NOTHING IN THIS FILE IS AN EXPERIMENTAL RESULT")
    a(f"RUN VERDICT {run_verdict()}\nengine: 745.py git blob {LOCKS['745.py']} executed unchanged · exit code {STATE.get('engine_rc')} · experiment directory {STATE.get('exp_dir')}")
    a("\nSTAGES (times = this RUN)")
    for key,title in STAGES.items():
        s=STATE["stages"][key];a(f"  [{s['status'].upper():<4}] {key:<10} {('%.0f s'%s['seconds']) if s['seconds'] is not None else '':>8}  {title}\n             {s['note']}")
    a("\nCARTRIDGES OF THIS RUN (manifest · demo re-verification)")
    for c in CARTS:
        e=_ents().get(c);v=_v(c)
        a(f"  {c:<4} "+(f"{e['role']:<36} {e['body_tokens']:>5} tok · file {e['sha256']} · parents {[p['id'] for p in e.get('parents',[])]} · file/tensor/body ok {v.get('file_sha_ok')}/{v.get('tensor_seal_ok')}/{v.get('body_sha_ok')} · equal to earlier RECORD {v.get('equal_to_record')}" if e else "not produced"))
    a("\nWHAT THIS RUN SHOWS — AND WHAT NEEDS INDEPENDENT EVALUATION")
    for t,kind,f in CLAIMS:
        try:v=f()
        except Exception:v=None
        a(f"  {'PASS' if v else ('FAIL' if v is False else '—'):<5} {t}  [{kind}]")
    for i,x in enumerate(R.get("blind_answers") or []):a(f"\nBLIND ANSWER Q{i+1} (C11, before the official report)\n  {x['question']}\n  "+x["answer"].replace("\n","\n  "))
    sa=(R.get("self_audit") or {}).get("text")
    if sa:a("\nMODEL SELF-AUDIT AFTER THE OFFICIAL REPORT (model claim, not expert grading)\n  "+sa.replace("\n","\n  "))
    a("\nHUMAN REVIEW: NOT PROVIDED (pending). No independent grading was performed by TEST745 or by this demo.")
    a(f"\n{AUTHOR} · {ORG} · {LICENSE_NAME} · {COPYRIGHT}")
    RUN_SUMMARY.write_text("\n".join(L)+"\n",encoding="utf-8")
def engine_files():
    d=exp_dir()
    if not d or not d.is_dir():return []
    out=[d/n for n in ("TEST745.log","TEST745_results.json","TEST745_manifest.json","C11_BLIND_SEAL.json") if (d/n).is_file()]
    out+=sorted((d/"generated_text").glob("*.txt")) if (d/"generated_text").is_dir() else []
    out+=sorted(p for p in (d/"sealed_sources").glob("*.txt")) if (d/"sealed_sources").is_dir() else []
    return out
def download_items():
    items=[("Run summary",RUN_SUMMARY),("Engine output, real-time (UTC receipt · stage · stream · line)",ENGINE_OUT),("Session log",SESSION_LOG),("Session events (JSONL)",SESSION_EVENTS),
           ("Post-run verification",VERIFY_FILE),("Closed-loop measures",DATA_DIR/"CLOSED_LOOP_MEASURES.json"),("Stage record",DATA_DIR/"STAGES.json"),("Engine checks of this RUN",DATA_DIR/"ENGINE_CHECKS.json"),
           ("Figure manifest",SESSION_DIR/"FIGURES_MANIFEST.json"),("SHA-256 manifest",MANIFEST),("745.py (locked, executed)",PROGRAM),("745.log — earlier run (RECORD)",EVID_DIR/"745.log")]
    out=[(l,str(p)) for l,p in items if Path(p).is_file()]
    out+=[(f"engine output file · {p.parent.name}/{p.name}",str(p)) for p in engine_files()]
    return out
def package_session():
    dump_json(DATA_DIR/"ENGINE_CHECKS.json",CHECKS);dump_json(DATA_DIR/"STAGES.json",dict(verdict=run_verdict(),stages=STATE["stages"],session=SESSION_ID,engine_rc=STATE.get("engine_rc")))
    write_run_summary()
    files=[p for p in sorted(SESSION_DIR.rglob("*")) if p.is_file() and p!=MANIFEST and p.suffix!=".tmp"]
    man=OrderedDict((str(p.relative_to(SESSION_DIR)),dict(sha256=sha_file(p),bytes=p.stat().st_size)) for p in files)
    dump_json(MANIFEST,dict(session=SESSION_ID,utc=utc_now(),simulation=SIM,note="SHA-256 of every file of this RUN, including the experiment directory, cartridges (.pt) and PDFs (not offered for download). No ZIP.",files=man))
    return str(MANIFEST)
def stage_records():
    package_session();return f"{len(FIG_FILES)} JPEG figures + {len(download_items())} records/texts, each downloadable directly · SHA-256 manifest of {len(json.load(open(MANIFEST))['files'])} files (no ZIP)"

# ---------------------------------------------------------------------------------------------------------------------
# THE RUN PIPELINE (one button)
# ---------------------------------------------------------------------------------------------------------------------
RUNS_DONE=[]
def _text_watcher(stop):
    seen=set()
    while not stop.wait(10):
        d=EXP_ROOT/"generated_text"
        if not d.is_dir():continue
        new=[p for p in sorted(d.glob("*.txt")) if p.name not in seen]
        for p in new:
            seen.add(p.name);t=tload(p) or "";slog("TEXT_WRITTEN",p.name,chars=len(t),sha256=sha_text(t))
        if new:bump()
def run_pipeline():
    if RUNS_DONE:_session_paths(datetime.now().astimezone().strftime("SH745-%Y%m%d-%H%M%S")+f"-RUN{len(RUNS_DONE)+1}")
    RUNS_DONE.append(SESSION_ID);LIVE.clear();LIVE.update(session=SESSION_ID);LINES.clear();CHECKS.clear();FIG_FILES.clear();FIG_ERRORS.clear();PROVENANCE.clear()
    STATE.update(running=True,started=utc_now(),finished=None,current=None,exp_dir=None,engine_rc=None,engine_pid=None,elapsed=None);STATE["fig_version"]+=1
    for k in STAGES:STATE["stages"][k]=dict(status="wait",seconds=None,note="",t0=None)
    banner(f"RUN {SESSION_ID} · {local_now()} · the TEST745 engine takes about 1.5 hours on an A100 (earlier run: {ANCHORS['seconds']:.0f} s)")
    def step(key,fn):
        STATE["current"]=key;stage_set(key,"run");_emit(f"── [{list(STAGES).index(key)+1}/{len(STAGES)}] {STAGES[key]}")
        try:
            note=fn();stage_set(key,"done",note);slog("STAGE_DONE",key,note=note);return True
        except Exception as ex:
            stage_set(key,"fail",f"{type(ex).__name__}: {ex}");slog("STAGE_FAILED",key,error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc()[-3000:]);return False
    try:
        ok=step("PRECHECK",stage_precheck)
        if ok:
            stop=threading.Event();w=threading.Thread(target=_text_watcher,args=(stop,),daemon=True);w.start()
            try:rc=run_engine()
            except Exception as ex:rc=-1;slog("ENGINE_START_FAILED",f"{type(ex).__name__}: {ex}")
            finally:stop.set()
            failed=next((l for _,_,l in reversed(LINES) if "TEST745_FAILED_CLOSED" in l or re.match(r"^FAIL ",l)),None)
            cur=next((k for k in ENGINE_STAGES if STATE["stages"][k]["status"] in("run","wait")),None)
            if cur:
                why=(failed or (f"engine process exit code {rc}" if rc else "engine ended before this stage completed"))
                stage_set(cur,"fail",why)
                for k in ENGINE_STAGES[ENGINE_STAGES.index(cur)+1:]:stage_set(k,"skip","not run — the engine stopped at "+cur)
            if EXP_ROOT.exists():
                dst=SESSION_DIR/"TEST745_EXPERIMENT";shutil.move(str(EXP_ROOT),str(dst));STATE["exp_dir"]=str(dst);slog("EXPERIMENT_DIR",f"moved into this RUN: {dst}")
        else:
            for k in ENGINE_STAGES:stage_set(k,"skip","not run — pre-flight failed")
        if STATE.get("exp_dir") and (Path(STATE["exp_dir"])/"TEST745_manifest.json").is_file():step("VERIFY",stage_verify)
        else:stage_set("VERIFY","skip","no cartridge manifest in this RUN")
        step("FIGURES",stage_figures);step("RECORDS",stage_records)
    finally:
        STATE.update(running=False,finished=utc_now(),current=None);bump()
        try:package_session()
        except Exception:pass
        banner(f"RUN VERDICT: {run_verdict()}\nRUN {SESSION_ID} finished {local_now()} · "+" · ".join(f"{k}:{v['status']}" for k,v in STATE["stages"].items()))
RUN_THREAD={"t":None}
def start_run():
    t=RUN_THREAD["t"]
    if t is not None and t.is_alive():return False
    RUN_THREAD["t"]=threading.Thread(target=run_pipeline,daemon=True,name="SH745-RUN");RUN_THREAD["t"].start();return True
# ===== END OF PART 2/3 =====
# ===== PART 3/3 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 3 — Gradio interface (Silicon Hippocampus 1.5 design): ONE button (RUN). Before RUN only the earlier run is shown,
#              labelled RECORD (it holds no text). RUN starts the unchanged 745.py; the stages, the engine's own output, the
#              sealed cartridges and every text it writes appear while it works. The interface never edits an output.
# =====================================================================================================================
LINEAGE=[("Research Record I — Qwen2.5-7B","https://doi.org/10.5281/zenodo.23381336"),
         ("Research Record II — Mistral-7B, Silicon Hippocampus v1.4","https://doi.org/10.5281/zenodo.23418927"),
         ("Research Record III — Qwen2.5-72B, Direct Internal-State Injection","https://doi.org/10.5281/zenodo.23434686"),
         ("Zenodo record 23497732 (link given by the author)",ZENODO)]
def esc(x):return html.escape(str(x))
def card(title,body,kind="info"):return f'<div class="kz card {kind}"><div class="h">{esc(title)}</div><div class="small">{body}</div></div>'
def chip(cid):c=ccol(cid);return f'<span class="chip" style="color:#fff;background:{c};border-color:{c}">{esc(cid)}</span>'
def ok_mark(v):return "<b style='color:#08785B'>PASS</b>" if v else ("<b style='color:#B91C1C'>FAIL</b>" if v is False else "<span style='opacity:.6'>—</span>")
class Markup(str):pass
def tbl(rows,head=None,mono_cols=()):
    h="".join(f"<th>{esc(x)}</th>" for x in head) if head else ""
    b="".join("<tr>"+"".join(f"<td class='{'mono' if i in mono_cols else ''}'>{v if isinstance(v,Markup) else esc(v)}</td>" for i,v in enumerate(r))+"</tr>" for r in rows)
    return f"<table class='tbl'>{('<tr>'+h+'</tr>') if h else ''}{b}</table>"
def pre(text,maxh=420):return f"<div class='ans' style='max-height:{maxh}px'>{esc(text)}</div>"
def details(summary,inner,open_=False):return f"<details{' open' if open_ else ''}><summary>{summary}</summary>{inner}</details>"
def textblock(title,text,note="",open_=False,maxh=460):
    if text is None:return details(f"{esc(title)} · <i>not written yet in this RUN</i>","")
    return details(f"{esc(title)} · {len(text):,} characters · SHA-256 {sha_text(text)[:12]}…"+(f" · {esc(note)}" if note else ""),pre(text,maxh),open_)

CSS="""
:root{--kz-on:#08785B;--kz-fg:#111827;--kz-card:#ffffff;--kz-bd:#d1d5db;--kz-a:#2455D6;--kz-err:#b91c1c;--kz-warn:#b45309;--kz-m:#7626D9}
.dark{--kz-on:#34d399;--kz-fg:#f3f4f6;--kz-card:#111827;--kz-bd:#4b5563;--kz-a:#93c5fd;--kz-err:#f87171;--kz-warn:#fbbf24;--kz-m:#c4b5fd}
html,body{overflow-x:hidden!important}
.gradio-container{width:100%!important;max-width:1180px!important;margin:0 auto!important;padding-left:10px!important;padding-right:10px!important;box-sizing:border-box!important}
.gradio-container *{box-sizing:border-box}
.kz{color:var(--kz-fg)!important;max-width:100%;overflow-wrap:anywhere;line-height:1.45}
.kz *{color:inherit}
.hero{background:#0b1220;border-radius:6px;padding:18px 18px 14px;margin:4px 0 8px}
.hero,.hero *{color:#f9fafb!important}
.rec{font-size:11.5px;letter-spacing:1.6px;text-transform:uppercase;opacity:.85;border:1px solid rgba(255,255,255,.35);display:inline-block;padding:2px 8px;border-radius:3px}
.brand{font-size:clamp(22px,6vw,34px);font-weight:800;letter-spacing:.6px;line-height:1.1;margin-top:10px}
.title{font-size:clamp(14px,3.8vw,18px);font-weight:600;margin-top:6px;color:#ddd6fe!important}
.by{font-size:13px;margin-top:10px;opacity:.9}
.tiles{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.tile{border:1px solid rgba(255,255,255,.3);border-radius:4px;padding:6px 9px;min-width:120px;flex:1}
.tile b{font-size:18px;display:block}
.tile span{font-size:11.5px;opacity:.85}
.card{background:var(--kz-card);border:1px solid var(--kz-bd);border-left:4px solid var(--kz-bd);border-radius:4px;padding:10px 12px;margin:6px 0}
.card.on{border-left-color:var(--kz-on)}.card.err{border-left-color:var(--kz-err)}.card.warn{border-left-color:var(--kz-warn)}.card.info{border-left-color:var(--kz-a)}.card.m{border-left-color:var(--kz-m)}
.card .h{font-weight:700;font-size:15px;margin-bottom:4px}
.small{font-size:13.5px}
.mono,.kz code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.3px}
.chip{display:inline-block;border:1px solid;border-radius:3px;padding:0 6px;font-size:12px;font-weight:700;white-space:nowrap}
.tbl{width:100%;border-collapse:collapse;font-size:13px}
.tbl td,.tbl th{border-bottom:1px solid var(--kz-bd);padding:5px 4px;vertical-align:top;text-align:left}
.tbl th{font-size:12px;opacity:.75}
.stg{font-size:13.5px;margin:2px 0}.stg.done{color:var(--kz-on)!important}.stg.run{color:var(--kz-a)!important;font-weight:700}.stg.wait{opacity:.55}.stg.fail{color:var(--kz-err)!important;font-weight:700}.stg.skip{color:var(--kz-warn)!important}
.stg .nt{font-size:12px;opacity:.85;margin-left:22px;display:block}
.ans{white-space:pre-wrap;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.6px;border:1px solid var(--kz-bd);border-radius:4px;padding:6px 8px;margin:3px 0;overflow:auto}
details{margin:4px 0}summary{cursor:pointer;font-weight:600}
#kz_run button,#kz_run{font-size:clamp(17px,4.6vw,21px)!important;font-weight:800!important;min-height:58px!important;letter-spacing:1px}
@media (max-width:640px){.tbl .hide-m{display:none}}
"""
def hero_html():
    c=REC.get("completed") or {}
    tiles=[("C01–C03","source cartridges (one report)"),("S · H","6 synthesis cartridges"),("8","closed-loop rounds"),("C11","blind MASTER, sealed"),("C12","post-outcome MASTER"),("PENDING","human review")]
    return (f'<div class="kz hero"><span class="rec">Live research demonstration · frozen Qwen2.5-72B-Instruct · NF4 · BF16 · CUT3 · A100 80 GB</span>'
            f'<div class="brand">{esc(APP_NAME)}</div><div class="title">{esc(APP_SUB)}</div>'
            '<div class="by">An AI is given the official, not yet concluded investigation data of a real accident (Air Tractor AT-802A OR-2025, 13 November 2025, AIN Croatia). '
            'Without changing its weights, the information is written into physical memory cartridges, read back, synthesized, reviewed in eight closed-loop rounds and sealed '
            'as the blind MASTER C11 — before the official final report is opened. Only then the final report is read, the model audits itself, and C12 is formed.</div>'
            '<div class="tiles">'+"".join(f'<div class="tile"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a,b in tiles)+'</div>'
            f'<div class="by"><b>{esc(AUTHOR)}</b> · {esc(ORG)} · {esc(PLACE)} · {esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · <a href="{REPO}" target="_blank" rel="noopener">{esc(REPO)}</a></div></div>')
def mode_html():
    st=STATE
    if SIM:kind,t="err","SIMULATION — code test of the author with a fake engine, NOT an experimental result"
    elif st.get("running"):
        el=(time.time()-datetime.fromisoformat(st["started"]).timestamp())/60 if st.get("started") else 0
        kind,t="info",f"RUN IN PROGRESS · {el:.0f} min · stage {list(STAGES).index(st['current'])+1 if st.get('current') else '…'}/{len(STAGES)}: {STAGES.get(st.get('current'),'')}"
    elif st.get("finished"):
        ok=run_verdict().startswith("COMPLETE");kind,t=("on" if ok else "err"),f"RUN {SESSION_ID} — {run_verdict()}"
    else:kind,t="info","NOT STARTED — press RUN. The unchanged TEST745 engine runs on the GPU (about 1.5 hours); everything it does appears here while it works."
    rc=REC.get("completed") or {}
    return card(t,f"Earlier completed run (RECORD, 745.log): C11 {esc(rc.get('C11','')[:16])}… · C12 {esc(rc.get('C12','')[:16])}… · {rc.get('seconds',0):,.0f} s — shown only for comparison; "
                "it contains no generated text and is never presented as a result of this RUN.",kind)
def stages_html():
    out=[];n=len(STAGES);done=0
    for i,(k,title) in enumerate(STAGES.items(),1):
        s=STATE["stages"][k];stt=s["status"];mk={"done":"✓","run":"▶","fail":"✗","skip":"–","wait":"○"}[stt]
        if stt in("done","skip","fail"):done+=1
        tm=f" · {s['seconds']:.0f} s" if s.get("seconds") is not None else ""
        out.append(f"<div class='stg {stt}'>{mk} {i}/{n} · {esc(title)}{tm}"+(f"<span class='nt'>{esc(s['note'])}</span>" if s.get("note") else "")+"</div>")
    pc=100*done/n
    bar=f'<div style="margin-top:6px;background:#e5e7eb;height:10px;border-radius:2px"><div style="width:{pc:.0f}%;height:10px;background:#7626D9;border-radius:2px"></div></div>'
    head=f"RUN {SESSION_ID} · {run_verdict()}"+(f" · started {STATE['started'][11:19]} UTC" if STATE.get("started") else "")+(f" · finished {STATE['finished'][11:19]} UTC" if STATE.get("finished") else "")
    return card(head,"".join(out)+bar,"m")
def console_text():
    with _LOG_LOCK:return "\n".join(list(CONSOLE)[-180:])

# ---------------------------------------------------------------------------------------------------------------------
# tab contents — texts are read from THIS RUN's experiment directory, unedited
# ---------------------------------------------------------------------------------------------------------------------
def overview_html():
    E_=_ents();R=run_results()
    steps=[("Official, not yet concluded investigation data","the AIN preliminary report (PDF) is downloaded and checked; the final report is NOT downloaded",check_ok("FINAL_REPORT_NOT_DOWNLOADED_BEFORE_C11")),
           ("Written into physical memory — weights unchanged","three consecutive parts of the one preliminary report → C01, C02, C03 (H3 + K/V of layers 0–3 on the SSD)",all(c in E_ for c in SRC) or None),
           ("Read back from the cartridges","each cartridge mounted alone (80 layers rebuilt) and read by the frozen model",check_ok("GENERATION_NOT_TRUNCATED_C03")),
           ("Synthesized into new physical memories","readouts → text synthesis → S01–S03 → read again → H01–H03",all(c in E_ for c in SUB+CRS) or None),
           ("Eight closed-loop review rounds","initial hypothesis + 8 rounds, no official outcome available",(len(R.get("blind_rounds") or [])==8) or None),
           ("Blind MASTER C11 sealed","SHA-256 sealed and answered three questions before the final report is opened",check_ok("C11_LOCKED_BEFORE_FINAL")),
           ("Official final report opened — only now","downloaded after the C11 seal; the model compares and audits itself",check_ok("AUDIT_NOT_TRUNCATED")),
           ("C12 post-outcome MASTER","new cartridge, parent = C11 SHA-256; C11 unchanged; human review PENDING",check_ok("C12_PARENT_SHA"))]
    rows=[(Markup(f"<b>{i}. {esc(a)}</b><br><span class='small' style='opacity:.85'>{esc(b)}</span>"),Markup(ok_mark(v))) for i,(a,b,v) in enumerate(steps,1)]
    cl=[]
    for t,kind,f in CLAIMS:
        try:v=f()
        except Exception:v=None
        cl.append((t,kind,Markup(ok_mark(v) if kind=="technical" else "<b style='color:#B45309'>NOT EVALUATED</b>")))
    arch=card("Physical memory outside the frozen model — what it is and what it is not",
        "<b>What is stored:</b> internal states of the frozen Qwen2.5-72B — the layer-3 output H3 and the K/V of layers 0–3 — written to a file on the SSD, hashed, reloaded, injected at the "
        "layer-3 boundary and used to forge new cartridges.<br><b>Not text RAG:</b> no document text is pasted into the prompt at question time; the model reads its own stored states. "
        "<br><b>Not fine-tuning:</b> the weights are frozen (weight sentinel checked).<br><b>Not a removal of the transformer:</b> layers 4–79 and decoding still run every time; "
        "the early layers are reused from the stored states. TEST745 does not show that most of the transformer computation is eliminated.<br><b>Synthesis is text-mediated:</b> "
        "cartridges are combined through the model's written readouts, never by direct BF16 tensor fusion.","info")
    lin=card("Research lineage (published records — not results of this experiment)","<br>".join(f"{esc(t)} · <a href='{u}' target='_blank' rel='noopener'>{esc(u)}</a>" for t,u in LINEAGE)+
             f"<br>Silicon Hippocampus 1.5 demonstration (infrastructure of this interface): <a href='{URL_15}' target='_blank' rel='noopener'>Qwen72B_1.5.log</a>"+
             f"<br>This experiment: TEST745 — <a href='{URL_745}' target='_blank' rel='noopener'>745.py</a> · <a href='{URL_745LOG}' target='_blank' rel='noopener'>745.log</a>","info")
    return (card(f"What happens in this RUN ({SESSION_ID})",tbl(rows,["step","this RUN"]),"m")+
            card("What this RUN can show — and what needs independent evaluation",tbl(cl,["claim","kind","status"])+
                 "<div class='small' style='margin-top:4px'>An experimental demonstration of a working, researchable memory architecture — not a finished general AI system. "
                 "The model's self-audit is its own claim; no independent expert grading exists yet (human review PENDING).</div>","warn")+arch+lin)
def sources_html():
    R=run_results();al=R.get("ain_links") or {};pr=R.get("preliminary") or {};lv=R.get("preliminary_leakage_review") or {}
    rows=[("case page (link directory only, never model input)",al.get("case_url") or P745.get("CASE_URL")),("case page SHA-256 (quarantined)",al.get("case_page_sha256_quarantined")),
          ("preliminary report URL",pr.get("url") or al.get("preliminary_url")),("preliminary PDF SHA-256",pr.get("pdf_sha256")),("pages",pr.get("pages")),("retrieved",pr.get("retrieved")),
          ("final report URL (sealed, NOT fetched before C11)",al.get("final_url_sealed_not_fetched")),("leakage guard",f"{len(lv.get('mentions') or [])} generic mentions reviewed · "+("PASS" if check_ok("PRELIMINARY_OUTCOME_LEAKAGE_GUARD") else "—"))]
    segs="".join(textblock(f"{c} — part {i+1}/3 of the ONE preliminary report (forged text)",raw_of(f"{c}_FORGED.txt"),f"{(R.get('sources',{}).get(c) or {}).get('forged_tokens','—')} tokens") for i,c in enumerate(SRC))
    if not R:return card("Official sources","Not available yet — the engine records the AIN links and the preliminary report during RUN (stage 3).","info")
    return (card("AIN — official investigation sources of this RUN",tbl(rows,mono_cols=(1,)),"info")+
            card("C01 · C02 · C03 — three consecutive parts of ONE preliminary report (not three independent reports)",segs+textblock("full text extracted from the preliminary PDF",raw_of("AIN_PRELIMINARY_EXTRACT.txt")),"m"))
def cart_html():
    E_=_ents();V=(LIVE.get("verification") or {}).get("cartridges") or {}
    if not E_:return card("Physical cartridges","No cartridge sealed yet in this RUN.","info")
    rows=[]
    for c in CARTS:
        e=E_.get(c);v=V.get(c) or {}
        if not e:rows.append((Markup(chip(c)),"not produced yet","","","","","",""));continue
        par=", ".join(f"{p['id']} {p['sha256'][:10]}…" for p in e.get("parents") or []) or "—"
        rows.append((Markup(chip(c)),e.get("role"),par,f"{e['body_tokens']:,}",f"{e.get('forge_seconds')} s",e["sha256"],
                     Markup(f"file {ok_mark(v.get('file_sha_ok'))} · tensors {ok_mark(v.get('tensor_seal_ok'))} · body {ok_mark(v.get('body_sha_ok'))}" if v else "after the run"),
                     Markup(("= RECORD" if v.get("equal_to_record") else ("≠ RECORD" if v.get("equal_to_record") is False else "—")))))
    return card(f"Physical CUT3 cartridges of this RUN — {len(E_)}/11 sealed",tbl(rows,["id","role","parents (file SHA-256)","body tokens","forge","file SHA-256","re-verification","vs earlier run"],mono_cols=(5,)),"m")+\
           card("Order of creation","C01 → C02 → C03 → S01 → S02 → S03 → H01 → H02 → H03 → C11 → C12 (manifest timestamps: "+", ".join(f"{c} {str(E_[c].get('created',''))[11:19]}" for c in CARTS if c in E_)+")","info")
def synth_html():
    gi=generation_index();out=[]
    for g in gi:
        if g["cid"] in("INITIAL","C11"):continue
        out.append(textblock(f"{g['cid']} · {g['role']}",text_of(g["file"]),f"{g.get('tokens','—')} tokens"))
    return card("Readouts and syntheses of this RUN, in the order they were written (unedited)","".join(out) or "none yet","m")+\
           card("Programmed prompts of 745.py (unchanged)","".join(details(esc(k),pre(v,240)) for k,v in (P745.get("prompts") or {}).items()),"info")
def loop_html():
    rt=round_texts();M=LIVE.get("loop") or {}
    head=("Observational measures (no quality score): "+" · ".join(f"{l}: {t or '—'} tok, similarity to previous {s if s is not None else '—'}, open uncertainties {u if u is not None else '—'}"
          for l,t,s,u in zip(M.get("labels",[]),M.get("tokens",[]),M.get("similarity_to_previous",[]),M.get("open_uncertainty_items",[])))) if M else "Measures are computed after the run (Figure 4)."
    return card("Closed loop — initial blind hypothesis and the eight review rounds of this RUN (unedited)",esc(head)+"".join(textblock(l if l!="INITIAL" else "INITIAL blind hypothesis",t,
                "written to C11" if l=="R8" else "",open_=(l in("INITIAL","R8"))) for l,t in rt),"m")
def blind_html():
    R=run_results();E_=_ents();seal=R.get("C11_seal") or {};c11=E_.get("C11")
    body=None
    if c11 and text_of("blind_round_08.txt") is not None and all(k in E_ for k in CRS):body=blind_body_from(E_,text_of("blind_round_08.txt"))
    out=card("C11 BLIND MASTER",(f"file SHA-256 <span class='mono'>{esc(c11['sha256'])}</span> · {c11['body_tokens']:,} tokens · sealed at {esc(seal.get('sealed_at','—'))} · "
             f"blind answers SHA-256 <span class='mono'>{esc(str(seal.get('blind_answers_sha256'))[:16])}…</span> · C11 locked before final: {ok_mark(check_ok('C11_LOCKED_BEFORE_FINAL'))}" if c11 else "not sealed yet in this RUN")+
             (textblock("C11 body (re-derived with the exact 745.py expression)",body) if body else ""),"m")
    qa="".join(card(f"Q{i+1} · {x['question']}",pre(x["answer"],460),"m") for i,x in enumerate(R.get("blind_answers") or []))
    return out+(qa or card("Blind answers","not written yet in this RUN","info"))
def outcome_html():
    R=run_results();off=R.get("official_outcome") or {};sa=(R.get("self_audit") or {}).get("text")
    if not off:return card("Official outcome","Embargoed — the AIN final report is downloaded only after C11 has been sealed (stage 11).","warn")
    rows=[("final report URL",off.get("url")),("PDF SHA-256",off.get("pdf_sha256")),("pages",off.get("pages")),("retrieved",off.get("retrieved")),("unlocked (engine)",line_time(r"^OFFICIAL_OUTCOME_UNLOCK"))]
    return (card("AIN final report — opened after the C11 seal",tbl(rows,mono_cols=(1,))+textblock("evaluation excerpt given to the model (as built by 745.py)",raw_of("AIN_FINAL_EVALUATION_EXCERPT.txt"))+
                 textblock("full text extracted from the final report PDF",raw_of("AIN_FINAL_EXTRACT.txt")),"info")+
            card("Model self-audit after the official report — the model's own claim, NOT independent expert grading",pre(sa,640) if sa else "not written yet","warn"))
def c12_html():
    R=run_results();E_=_ents();c12=E_.get("C12");V=LIVE.get("verification") or {};lin=V.get("lineage") or {}
    if not c12:return card("C12 POST-OUTCOME MASTER","not sealed yet in this RUN","info")
    body=c12body_from(E_,R,(R.get("self_audit") or {}).get("text")) if R.get("self_audit") and R.get("C11_seal") and R.get("official_outcome") else None
    rows=[("C12 file SHA-256",c12["sha256"]),("parent",", ".join(f"{p['id']} {p['sha256']}" for p in c12.get("parents") or [])),("role",c12.get("role")),("body tokens",c12.get("body_tokens")),
          ("C11 immutable (engine)",Markup(ok_mark(check_ok("C11_IMMUTABLE")))),("C12 parent SHA (engine)",Markup(ok_mark(check_ok("C12_PARENT_SHA")))),("weights unchanged (engine)",Markup(ok_mark(check_ok("FROZEN_SENTINEL_UNCHANGED")))),
          ("C11 file re-hashed now (demo)",Markup(ok_mark(_v("C11").get("file_sha_ok")))),("C12 body re-derived = manifest (demo)",Markup(ok_mark(_v("C12").get("body_sha_ok")))),("C12 parent link (demo)",Markup(ok_mark(lin.get("c12_parent_is_c11"))))]
    return card("C12 POST-OUTCOME MASTER — human review PENDING (not a human-approved cartridge)",tbl(rows,mono_cols=(1,))+(textblock("C12 body (re-derived with the exact 745.py expression)",body) if body else ""),"m")
def verif_html():
    rows=[(c["utc"][11:19],c.get("stage") or "",c["name"],Markup(ok_mark(c["passed"])),c["detail"][:140]) for c in CHECKS]
    rec=[(c,(REC["sealed"].get(c) or {}).get("sha256","—"),(_v(c).get("sha256_now") or "—"),Markup(ok_mark(_v(c).get("equal_to_record")) if _v(c) else "—")) for c in CARTS]
    src=[(n,v["git_blob"],v["sha256"],f"{v['bytes']:,}") for n,v in SOURCES.items()]
    V=LIVE.get("verification") or {}
    return (card(f"Engine checks of this RUN — {sum(c['passed'] for c in CHECKS)}/{len(CHECKS)} PASS (time = receipt of the engine line)",tbl(rows,["UTC","stage","check","result","detail"],mono_cols=(4,)) if rows else "none yet","on" if rows and all(c["passed"] for c in CHECKS) else "info")+
            card("Independent re-verification after the run (read-only)",(pre(json.dumps(jsafe(V.get("lineage")),indent=1),220)+("PROBLEMS: "+esc(", ".join(V.get("problems"))) if V.get("problems") else "no problem found")) if V else "after the engine has finished","info")+
            card("This RUN vs the earlier completed run (RECORD, 745.log) — comparison only",tbl(rec,["cartridge","earlier run (RECORD)","this RUN","equal"],mono_cols=(1,2)),"info")+
            card("Locked sources (git blob verified)",tbl(src,["file","git blob","SHA-256","bytes"],mono_cols=(1,2)),"info"))

TABS=["OVERVIEW","OFFICIAL SOURCES","PHYSICAL CARTRIDGES","HIERARCHICAL SYNTHESIS","CLOSED LOOP","BLIND C11","OFFICIAL OUTCOME","C12 MASTER","VERIFICATION","SCIENTIFIC FIGURES"]
TAB_HTML={"OVERVIEW":overview_html,"OFFICIAL SOURCES":sources_html,"PHYSICAL CARTRIDGES":cart_html,"HIERARCHICAL SYNTHESIS":synth_html,"CLOSED LOOP":loop_html,"BLIND C11":blind_html,
          "OFFICIAL OUTCOME":outcome_html,"C12 MASTER":c12_html,"VERIFICATION":verif_html}
def tab_gallery(tab):
    keys=[k for k,m in FIGURES.items() if (m["tab"]==tab or tab=="SCIENTIFIC FIGURES") and k in FIG_FILES]
    return [(FIG_FILES[k]["jpg"],f"Figure {FIGURES[k]['n']} — {FIGURES[k]['title']} · {FIG_FILES[k]['badge']}") for k in keys]
def figs_status_html():
    n=len(FIG_FILES);tot=len(FIGURES)
    if not n and not FIG_ERRORS:return card(f"Scientific figures of this RUN — 0/{tot}","The six figures are drawn from this RUN's outputs after the engine has finished (stage 14). They appear here, one below the other.","info")
    def st(k):
        f=FIG_FILES.get(k)
        if not f:return "NOT GENERATED: "+str(FIG_ERRORS.get(k,"pending"))
        q=f.get("layout_qc") or {};j=f.get("jpeg_qc") or {}
        return f"{f['badge']} · {f['pixels'][0]}×{f['pixels'][1]} JPEG 300 dpi · layout QC {'PASS' if q.get('passed') else 'FAIL'} · JPEG QC {'PASS' if j.get('passed') else 'FAIL'}"
    rows="".join(f"<div class='small'>{'✓' if k in FIG_FILES and (FIG_FILES[k].get('layout_qc') or {}).get('passed') and FIG_FILES[k]['badge']!='NOT PRODUCED IN THIS RUN' else '✗'} Figure {esc(m['n'])} — {esc(m['title'])} · <b>{esc(st(k))}</b></div>" for k,m in FIGURES.items())
    ok=n==tot and all((v.get("layout_qc") or {}).get("passed") and v["badge"]!="NOT PRODUCED IN THIS RUN" for v in FIG_FILES.values())
    return card(f"Scientific figures of this RUN ({SESSION_ID}) — {n}/{tot} written",rows,"on" if ok else "warn")
from urllib.parse import quote as _urlquote   # NOTE: part 2 defines its own text helper quote(text,n); the URL quote must not be that one
# relative URLs (no leading "/"): they resolve against the page itself, so they work through the public share link,
# the Colab port window and any proxy root path alike
def file_url(p):return ("gradio_api/file=" if _GR_MAJOR>=5 else "file=")+_urlquote(str(p),safe="/")
def file_url_alt(p):return ("file=" if _GR_MAJOR>=5 else "gradio_api/file=")+_urlquote(str(p),safe="/")
def figs_main_html():
    """the six figures of THIS run, in order — each with its own direct JPEG download link below it"""
    if not FIG_FILES:return card("Figures","No figure of this RUN yet (figures of an earlier RUN are never shown).","info")
    keys=[k for k in FIGURES if k in FIG_FILES];out=[]
    bulk=("<a href='#' onclick=\"var l=document.querySelectorAll('a.kz-dl');for(var i=0;i<l.length;i++){(function(a,d){setTimeout(function(){a.click()},d)})(l[i],i*900)};return false;\">"
          f"<b>⬇ Download all {len(keys)} figures (JPEG), one after another</b></a>")
    out.append(card("Direct downloads — no ZIP",f"{bulk}<br><span class='small'>The browser downloads the JPEG files in order (Figure 1 → Figure 6). Some browsers ask once to "
                    "“allow multiple downloads”; if blocked, use the link under each figure or the JPEG file list below — every file downloads with one tap.</span>","on"))
    for k in keys:
        f=FIG_FILES[k];m=FIGURES[k];u=file_url(f["jpg"]);ua=file_url_alt(f["jpg"]);nm=Path(f["jpg"]).name;qc=(f.get("layout_qc") or {}).get("passed") and f["badge"]!="NOT PRODUCED IN THIS RUN"
        out.append(f"<div class='kz card {'on' if qc else 'err'}'><div class='h'>Figure {esc(m['n'])} — {esc(m['title'])} · {esc(f['badge'])}"+("" if (f.get("layout_qc") or {}).get("passed") else " · LAYOUT QC FAIL")+"</div>"
                   f"<img src='{u}' data-alt='{ua}' onerror=\"if(!this.dataset.done){{this.dataset.done=1;this.src=this.dataset.alt;var a=this.parentNode.querySelector('a.kz-dl');if(a)a.href=this.dataset.alt;}}\" "
                   f"style='width:100%;height:auto;border:1px solid #d1d5db' alt='Figure {esc(m['n'])}'>"
                   f"<div class='small' style='margin-top:4px'><a class='kz-dl' href='{u}' download='{esc(nm)}'><b>⬇ Download Figure {esc(m['n'])} (JPEG, {f['pixels'][0]}×{f['pixels'][1]}, 300 dpi)</b></a> · "
                   f"<span class='mono'>{esc(nm)} · SHA-256 {esc(f['sha256_jpg'][:16])}…</span></div></div>")
    return "".join(out)
def jpg_files():return [FIG_FILES[k]["jpg"] for k in FIGURES if k in FIG_FILES]
def _safe(fn):
    try:return fn()
    except Exception as ex:return card("Display error",f"<code>{esc(type(ex).__name__)}: {esc(ex)}</code> — the records are unaffected","err")
def all_files():return [p for _,p in download_items()]
def snapshot(last):
    """full output tuple; html parts are rebuilt only when the state changed, figures only when they changed"""
    v=STATE["version"];fv=STATE["fig_version"];out=[_safe(mode_html),_safe(stages_html),console_text()]
    if last.get("v")!=v:
        for t in TAB_HTML:out.append(_safe(TAB_HTML[t]))
        last["v"]=v
    else:out+=[gr.update() for _ in TAB_HTML]
    if last.get("fv")!=fv:out+=[tab_gallery(t) for t in TABS];last["fv"]=fv;figs=[jpg_files() or None,_safe(figs_status_html),_safe(figs_main_html)]
    else:out+=[gr.update() for _ in TABS];figs=[gr.update(),gr.update(),gr.update()]
    fl=all_files()
    if last.get("files")!=len(fl):out.append(fl or None);last["files"]=len(fl)
    else:out.append(gr.update())
    return tuple(out+figs)
# The page is refreshed by SHORT polling requests (gr.Timer, every 3 s, per browser tab) instead of one 1.5-hour streaming
# request: a long stream through the share tunnel can be dropped (phone asleep, tab in background, tunnel reconnect) and then
# the page silently stops updating — that is how the six figures of the first A100 run never reached the page.
# With polling, every tick is a new request: after any interruption the next tick (or a page reload) shows the full state,
# figures included. The RUN thread itself never depends on the browser.
_HAS_TIMER=hasattr(gr,"Timer") and hasattr(gr,"State")
def _snap_state(last):
    last=dict(last) if isinstance(last,dict) else {}
    return (*snapshot(last),last)
def run_click(last):
    start_run();time.sleep(.5);return _snap_state({})
def ui_tick(last):return _snap_state(last)
def page_load_state():return _snap_state({})
def run_handler():
    """fallback for a gradio without gr.Timer: one streaming request (the earlier behaviour)"""
    start_run();last={};time.sleep(.5)
    while True:
        t=RUN_THREAD["t"];alive=t is not None and t.is_alive()
        yield snapshot(last)
        if not alive:break
        time.sleep(3.0)
    STATE["fig_version"]+=1;last.pop("files",None)
    yield snapshot(last)
def page_load():return snapshot({})

def _tb(**kw):
    for extra in (([{"buttons":["copy"]}] if _GR_MAJOR>=6 else [])+[{"show_copy_button":True},{}]):
        try:return gr.Textbox(**extra,**kw)
        except TypeError:continue
def _gallery(**kw):
    try:return gr.Gallery(columns=1,height="auto",object_fit="contain",preview=False,**kw)
    except TypeError:return gr.Gallery(**kw)
def _on(ev,fn,inputs,outputs,limit,quiet=False):
    for kw in (([dict(concurrency_limit=limit,show_progress="hidden")] if quiet else [])+[dict(concurrency_limit=limit),{}]):
        try:return ev(fn,inputs=inputs,outputs=outputs,**kw)
        except TypeError:continue
def build_ui():
    blocks=gr.Blocks(title=APP_SHORT) if _GR_MAJOR>=6 else gr.Blocks(css=CSS,title=APP_SHORT)
    with blocks as demo:
        gr.HTML(hero_html());mode=gr.HTML(mode_html())
        run_b=gr.Button("RUN",variant="primary",elem_id="kz_run")
        stg=gr.HTML(stages_html())
        con=_tb(lines=12,max_lines=20,label="Live engine output of this RUN — every line as 745.py prints it (time · stage · line); also ENGINE_OUTPUT_REALTIME.log and SESSION.log",value=console_text(),interactive=False)
        fstat=gr.HTML(_safe(figs_status_html));main_figs=gr.HTML(_safe(figs_main_html))
        jpgs=gr.File(label="The six JPEG figures of this RUN, in order — each file downloads with one tap",value=(jpg_files() or None),file_count="multiple",interactive=False)
        files=gr.File(label="Real-time engine output, logs, verification, all texts written by the engine, manifests — direct downloads (no ZIP)",value=(all_files() or None),file_count="multiple",interactive=False)
        htmls={};gals={}
        with gr.Tabs():
            for t in TABS:
                with gr.Tab(t):
                    if t in TAB_HTML:htmls[t]=gr.HTML(_safe(TAB_HTML[t]))
                    gals[t]=_gallery(label=f"{t} · figures",value=tab_gallery(t))
        gr.HTML(f'<div class="kz small" style="opacity:.8;margin:10px 0 18px">{esc(AUTHOR)} · {esc(ORG)} · {esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · '
                f'<a href="{URL_745}" target="_blank" rel="noopener">745.py</a> · <a href="{URL_745LOG}" target="_blank" rel="noopener">745.log</a> · <a href="{URL_709}" target="_blank" rel="noopener">709.py</a> · '
                f'<a href="{URL_730}" target="_blank" rel="noopener">730.py</a> · <a href="{URL_LICENSE}" target="_blank" rel="noopener">LICENSE</a> · AIN reports © Air Accident Investigation Agency, Croatia (ain.hr) · '
                'Qwen2.5-72B-Instruct and third-party libraries remain under their own licences.</div>')
        outs=[mode,stg,con]+[htmls[t] for t in TAB_HTML]+[gals[t] for t in TABS]+[files,jpgs,fstat,main_figs]
        if _HAS_TIMER:
            ui_state=gr.State({});timer=gr.Timer(3.0)
            _on(run_b.click,run_click,[ui_state],outs+[ui_state],8)
            _on(timer.tick,ui_tick,[ui_state],outs+[ui_state],8,quiet=True)
            try:demo.load(page_load_state,inputs=None,outputs=outs+[ui_state])
            except Exception:pass
        else:
            _on(run_b.click,run_handler,None,outs,8)
            try:demo.load(page_load,inputs=None,outputs=outs)
            except Exception:pass
    try:demo.queue(default_concurrency_limit=8)
    except TypeError:
        try:demo.queue(concurrency_count=8)
        except TypeError:demo.queue()
    return demo

_GR_MAJOR=int(re.match(r"\d+",gr.__version__).group())
GRADIO_LINK=DEMO_ROOT/"GRADIO_LINK.txt"
demo=None
def launch_interface():
    """(re)opens the interface of THIS session (public link first, Colab port window as fallback); nothing is recomputed.
    If the link stops working, run  launch_interface()  in a new cell."""
    global demo
    try:demo.close()
    except Exception:pass
    demo=build_ui()
    kw=dict(share=True,allowed_paths=[str(DEMO_ROOT),str(_CROOT)],show_error=True,inline=False,prevent_thread_lock=True,debug=False)
    if _GR_MAJOR>=6:kw["css"]=CSS
    err=None
    for _ in range(7):
        try:demo.launch(**kw);break
        except TypeError as ex:
            bad=next((k for k in ("css","prevent_thread_lock","allowed_paths","debug") if k in str(ex) and k in kw),None)
            if bad is None:raise
            kw.pop(bad)
        except Exception as ex:
            if not kw.get("share"):raise
            err=f"{type(ex).__name__}: {ex}";kw["share"]=False;slog("LAUNCH_NOTE","public share link not available — opening the local interface",error=err)
    share=getattr(demo,"share_url",None);local=getattr(demo,"local_url",None);window=None
    if not share:
        try:
            from google.colab import output as _co
            port=int(re.search(r":(\d+)",str(local)).group(1));_co.serve_kernel_port_as_window(port,anchor_text="▶ Open the AKBASCORE TEST745 interface (Colab window)");window=f"Colab port window, port {port}"
        except Exception as ex:window=f"not available ({type(ex).__name__})"
    dump_json(GRADIO_LINK.with_suffix(".json"),dict(utc=utc_now(),session=SESSION_ID,share_url=share,local_url=local,colab_window=window,share_error=err))
    GRADIO_LINK.write_text(f"{share or local}\n",encoding="utf-8")
    banner(f"INTERFACE OPEN · {share or ('local only: '+str(local))}\n  public link : {share or '— (tunnel not available; use the Colab window link above)'}\n  local       : {local}\n"
           f"  Press RUN in the interface — everything else runs automatically. If the link stops working: run  launch_interface()  in a new cell.","#")
    slog("LAUNCH","interface open",share_url=share,local_url=local,colab_window=window);return share or local
def keep_cell_running():
    """keeps this Colab cell RUNNING while the interface is in use: the engine output and every stage are printed below too"""
    banner("THE CELL STAYS RUNNING — the interface is live. Press RUN in the interface; the TEST745 engine output is printed here and shown in the interface.\n"
           f"  A full RUN takes about 1.5 hours on an A100. Stop this cell (■) only when you have finished; the files stay in {DEMO_ROOT}","#")
    shown=set()
    try:
        while True:
            time.sleep(5)
            t=RUN_THREAD["t"]
            if t is not None and not t.is_alive() and SESSION_ID not in shown:
                shown.add(SESSION_ID);show_figures_in_cell()
    except KeyboardInterrupt:pass
    finally:slog("CELL_STOPPED","the cell was stopped by the user")
def show_figures_in_cell(download=True):
    """second, independent channel (does not depend on the browser page): when a RUN has finished, the six JPEG figures
    of THIS run are shown here in the Colab cell, one below the other, and each is offered as a browser download.
    Can also be called by hand in a new cell:  show_figures_in_cell()"""
    keys=[k for k in FIGURES if k in FIG_FILES]
    banner(f"FIGURES OF THIS RUN ({SESSION_ID}) — {len(keys)}/{len(FIGURES)} — shown below in the cell, each also downloaded by the browser\n  folder: {FIG_DIR}","#")
    try:from IPython.display import display,Image as _IImg,HTML as _IHTML
    except Exception as ex:slog("CELL_FIGURES","IPython display not available",error=f"{type(ex).__name__}: {ex}");return
    for k in keys:
        f=FIG_FILES[k];m=FIGURES[k];nm=Path(f["jpg"]).name
        try:
            display(_IHTML(f"<div style='font:600 15px sans-serif;margin:14px 0 4px'>Figure {esc(m['n'])} — {esc(m['title'])} · {esc(f['badge'])} · {esc(nm)} · SHA-256 {esc(f['sha256_jpg'][:16])}…</div>"))
            display(_IImg(filename=f["jpg"],width=1100))
        except Exception as ex:slog("CELL_FIGURES",f"Figure {m['n']} could not be shown in the cell",error=f"{type(ex).__name__}: {ex}")
    if not download:return
    try:from google.colab import files as _cf
    except Exception:slog("CELL_FIGURES","not in Colab — browser download from the cell skipped; the files are in the folder above");return
    for k in keys:
        f=FIG_FILES[k]
        try:_cf.download(f["jpg"]);slog("CELL_DOWNLOAD",Path(f["jpg"]).name);time.sleep(1.0)
        except Exception as ex:slog("CELL_DOWNLOAD",f"{Path(f['jpg']).name} not downloaded",error=f"{type(ex).__name__}: {ex}")

# ---------------------------------------------------------------------------------------------------------------------
# START-UP (no GPU use): locked sources, the earlier run as RECORD, 745.py read-only — then the interface opens
# ---------------------------------------------------------------------------------------------------------------------
def startup():
    banner(f"{APP_NAME} · {EXPERIMENT} · start-up {local_now()} · session {SESSION_ID}"+("\nSIMULATION — NOTHING HERE IS AN EXPERIMENTAL RESULT" if SIM else ""))
    for n in LOCKS:RAW[n]=fetch_locked(n);slog("LOCKED_SOURCE",n,git_blob=SOURCES[n]["git_blob"],bytes=SOURCES[n]["bytes"])
    read_record();read_745(RAW["745.py"])
    slog("TEST745_RECORD",f"earlier run (RECORD): {REC['checks_passed']}/{REC['checks_total']} checks PASS · 11 cartridges · {REC['completed']['seconds']:.0f} s",
         C11=REC["completed"]["C11"][:16],C12=REC["completed"]["C12"][:16])
    slog("ENGINE_READY","745.py locked; it runs unchanged as its own process when RUN is pressed",git_blob=LOCKS["745.py"],experiment_dir=str(EXP_ROOT),
         existing_experiment_dir=EXP_ROOT.exists() and any(EXP_ROOT.iterdir()))
try:startup()
except Exception as _ex:
    _m=str(_ex)
    _hint=("A locked source changed on GitHub — the program stops instead of running unverified code." if "LOCKED SOURCE" in _m else
           "Network error while downloading a locked source from GitHub: run the cell again." if any(x in _m for x in ("URLError","timed out","HTTP Error","Connection","Name or service")) else
           "See the traceback above; nothing was run.")
    banner(f"START-UP FAILED — {type(_ex).__name__}: {_m}\nWHAT TO DO: {_hint}\nRecords of this attempt: {SESSION_DIR}","!")
    raise
launch_interface()
if os.environ.get("P745_NO_BLOCK")!="1":keep_cell_running()
# ===== END OF PART 3/3 =====


