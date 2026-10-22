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
