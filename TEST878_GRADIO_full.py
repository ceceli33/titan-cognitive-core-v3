# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS · TEST878 LIVE RESEARCH DEMONSTRATION (Gradio, Silicon Hippocampus 1.5 / SH745 infrastructure)
# Persistent native experience cartridges in a frozen Qwen2.5-72B: WRITE → FREE → RELOAD → APPEND → NATIVE DECISION
#   ENGINE (one OS process) : the locked TEST878 cell 878.py (git blob 7842e867…) executed BYTE-FOR-BYTE, unchanged:
#                             exact replay of real decision traces → Experience-CUT3 cartridges [X2][A][C] (H3 + K/V L0–L3)
#                             → SSD + SHA-256 → source working state freed → reload → native append into INDEPENDENT states
#                             → native CAR decision of the frozen model (BASE · FULL · C-BLIND · A-BLIND · A-REF arms)
#   HOST (this program)     : starts the engine process, receives every line it prints, re-verifies every cartridge file
#                             read-only (file SHA-256, per-tensor SHA-256, M/L row identity), draws nine JPEG figures from
#                             THIS run's outputs and offers every figure and record for direct download (no ZIP).
# Qwen/Qwen2.5-72B-Instruct · NF4 4-bit frozen · BF16 · CUT3 · NVIDIA A100-SXM4-80GB · ONE Google Colab cell
# PART 1 / 3 — identity, locks, embedded 878.py, logs, pipeline state, pre-check and the engine process
# ---------------------------------------------------------------------------------------------------------------------
# HOW TO RUN  Paste PART 1, 2 and 3 one below the other into ONE Colab cell (A100 runtime, fresh) and run it. Each part
#             ends with an END OF PART line — check that line after every paste. No upload is needed: 878.py is embedded
#             byte-exact and git-blob verified before use (GitHub copy as fallback, same lock).
#             The cell stays running; the interface opens with ONE button: RUN. RUN executes 878.py as its own OS process
#             (about 25–35 minutes on an A100: model load ≈ 21 min). Every line the engine prints is received, time-stamped
#             and shown at once. After the engine ends this program re-verifies the cartridges, draws nine JPEG figures
#             from THIS run's outputs, shows them in the interface AND in the Colab cell, and offers every file for download.
# STATUS      The host program was NOT executed on a GPU by its author (CPU simulation of its code paths only).
#             878.py itself is the GPU-verified TEST878 cell (repository 878.log, A100, status COMPLETE).
# AUTHOR      Mustafa Akbaş · AkbasCore AI Teknoloji · Mersin, Türkiye · Copyright © 2026 Mustafa Akbaş
#             AKBASCORE RESEARCH SOFTWARE LICENSE — https://github.com/ceceli33/titan-cognitive-core-v3?tab=License-1-ov-file
#             Qwen2.5-72B-Instruct and third-party libraries remain governed by their own licences.
# =====================================================================================================================
import os,sys,re,io,ast,json,time,html,math,shutil,hashlib,platform,threading,traceback,subprocess,importlib.util,textwrap,types,gc,glob
from pathlib import Path
from datetime import datetime,timezone
from collections import OrderedDict,deque
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
from matplotlib.colors import LogNorm,ListedColormap,TwoSlopeNorm
from PIL import Image
import gradio as gr
import urllib.request
SIM=os.environ.get("AKB878_SIM")=="1"          # code author's CPU simulation only (fake engine) — never an experimental result

# ---------------------------------------------------------------------------------------------------------------------
# identity, locks, colours
# ---------------------------------------------------------------------------------------------------------------------
APP_NAME="AKBASCORE SILICON HIPPOCAMPUS";APP_SUB="TEST878 · Persistent Native Experience Cartridges · Write → Free → Reload → Append → Native Decision"
APP_SHORT="AKBASCORE Silicon Hippocampus · TEST878 · Qwen2.5-72B · CUT3";CODE_VERSION="SH878-demo-1.0";EXPERIMENT="TEST878"
AUTHOR="Mustafa Akbaş";ORG="AkbasCore AI Teknoloji";PLACE="Mersin, Türkiye"
LICENSE_NAME="AKBASCORE RESEARCH SOFTWARE LICENSE";COPYRIGHT="Copyright © 2026 Mustafa Akbaş"
REPO="https://github.com/ceceli33/titan-cognitive-core-v3";RAW_BASE="https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
URL_LICENSE=REPO+"?tab=License-1-ov-file";URL_CODE=REPO+"/blob/main/878.py";URL_LOG=REPO+"/blob/main/878.log"
ENGINE_NAME="878.py";ENGINE_BLOB="7842e8675544a0328e3552f059c81b7750068a82"
LOCKS=OrderedDict([("878.py",ENGINE_BLOB),                                              # TEST878 cell — executed byte-for-byte
                   ("LICENSE","9aad4724d1072f9e56486650a9527380c867a53b")])
ENGINE_FACTS=dict(engine="test870.py",engine_commit="e322ed8",engine_blob="de3c8153266a95fbf9b86ce2e3149f48e16a7bbc",
                  records_sha256="daf5a8c4bd36811328a4ab173fe5cd300cc93c812558b883232e60ae42967f21")   # locked inside 878.py itself
MODEL_ID="Qwen/Qwen2.5-72B-Instruct"
COL=dict(M="#C2410C",L="#0F766E",FULL="#7626D9",CB="#6B7280",AB="#B91C1C",AR="#2455D6",BASE="#111827",ENG="#7626D9",HOST="#374151",PRE="#374151")
OK_COL="#08785B";NEU="#374151";BG="#FFFFFF";INK="#111827";INK2="#374151";MUTED="#6B7280";RULE="#D1D5DB";PANEL="#F8FAFC";RED="#B91C1C";AMBER="#B45309"
SESSIONS=("TEST878",);SCOL={"TEST878":COL["ENG"]};SNAME={"TEST878":"TEST878"}
WORDS=("ADVANCE","ACQUIRE","REJECT","BACKTRACK","ACCEPT","STOP")            # ACTION_IDS867 order (pairs i<j of this order)
PAIRS=[(a,b) for i,a in enumerate(WORDS) for b in WORDS[i+1:]]
ABBR={"ADVANCE":"ADV","ACQUIRE":"ACQ","REJECT":"REJ","BACKTRACK":"BKT","ACCEPT":"ACC","STOP":"STP"}

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
    if isinstance(o,np.bool_):return bool(o)
    if isinstance(o,np.ndarray):return jsafe(o.tolist())
    if isinstance(o,Path):return str(o)
    if isinstance(o,float) and (math.isnan(o) or math.isinf(o)):return None
    if isinstance(o,(str,int,float,bool)) or o is None:return o
    return str(o)
def dump_json(path,obj,mode=0o600):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(jsafe(obj),ensure_ascii=False,indent=2),encoding="utf-8");tmp.replace(path)
    try:os.chmod(path,mode)
    except Exception:pass
    return path
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
# directories and logs — every RUN has its own session folder; nothing is overwritten
# ---------------------------------------------------------------------------------------------------------------------
_CROOT=Path("/content") if os.path.isdir("/content") else Path("/tmp")
DEMO_ROOT=_CROOT/"AKBASCORE_TEST878_DEMO";EVID_DIR=DEMO_ROOT/"locked_sources"
SESSION_ID=SESSION_DIR=FIG_DIR=DATA_DIR=SESSION_LOG=SESSION_EVENTS=ENGINE_OUT=RUN_SUMMARY=MANIFEST=VERIFY_FILE=RUN_ROOT=None
def _session_paths(sid):
    """every RUN gets its own ID and folder (figures, records, logs)"""
    global SESSION_ID,SESSION_DIR,FIG_DIR,DATA_DIR,SESSION_LOG,SESSION_EVENTS,ENGINE_OUT,RUN_SUMMARY,MANIFEST,VERIFY_FILE,RUN_ROOT
    SESSION_ID=sid;SESSION_DIR=DEMO_ROOT/"sessions"/sid;FIG_DIR=SESSION_DIR/"figures";DATA_DIR=SESSION_DIR/"records"
    SESSION_LOG=SESSION_DIR/"SESSION.log";SESSION_EVENTS=SESSION_DIR/"SESSION_EVENTS.jsonl";ENGINE_OUT=SESSION_DIR/"ENGINE_OUTPUT_REALTIME.log"
    RUN_SUMMARY=SESSION_DIR/"RUN_SUMMARY.txt";MANIFEST=SESSION_DIR/"SHA256_MANIFEST.json";VERIFY_FILE=DATA_DIR/"POST_RUN_VERIFICATION.json"
    RUN_ROOT=SESSION_DIR/"run"
    for d in (DEMO_ROOT,DEMO_ROOT/"sessions",SESSION_DIR,FIG_DIR,DATA_DIR,EVID_DIR):d.mkdir(parents=True,exist_ok=True)
    for d in (DEMO_ROOT,DEMO_ROOT/"sessions",SESSION_DIR):os.chmod(d,0o755)
_session_paths(datetime.now().astimezone().strftime("SH878-%Y%m%d-%H%M%S"))
_OUT=sys.stdout;_LOG_LOCK=threading.Lock();CONSOLE=deque(maxlen=600)
def _emit(line,progress=False):
    """one console line; progress-bar updates replace the previous progress line (no re-printing hundreds of lines)"""
    with _LOG_LOCK:
        if progress and CONSOLE and CONSOLE[-1].startswith("⟳ "):CONSOLE[-1]="⟳ "+line[:300]
        elif progress:CONSOLE.append("⟳ "+line[:300])
        else:CONSOLE.append(line[:400])
    try:
        if progress:_OUT.write("\r"+line[:200].ljust(200));_OUT.flush();PROG_OPEN["open"]=True
        else:
            if PROG_OPEN["open"]:_OUT.write("\n");PROG_OPEN["open"]=False
            _OUT.write(line[:900]+"\n");_OUT.flush()
    except Exception:pass
PROG_OPEN={"open":False}
def _private(p):
    try:os.chmod(p,0o600)
    except Exception:pass
def slog(kind,message="",**data):
    """session log: one readable line + one JSON event (time · stage · event · data) written at the moment it happens"""
    stg=(globals().get("STATE") or {}).get("current") or "-"
    ev=dict(utc=utc_now(),session=SESSION_ID,stage=stg,kind=kind,message=str(message),data=jsafe(data),provenance=("SIMULATION" if SIM else "THIS RUN"))
    line=f"{ev['utc'][11:19]} [{stg}] {kind:<16} {message}"+(f" {json.dumps(jsafe(data),ensure_ascii=False)[:300]}" if data else "")
    with _LOG_LOCK:
        new=not SESSION_LOG.exists()
        with SESSION_LOG.open("a",encoding="utf-8") as f:f.write(f"{ev['utc']} [{stg}] {kind:<16} {message} {json.dumps(jsafe(data),ensure_ascii=False) if data else ''}\n")
        with SESSION_EVENTS.open("a",encoding="utf-8") as f:f.write(json.dumps(ev,ensure_ascii=False)+"\n")
        if new:_private(SESSION_LOG);_private(SESSION_EVENTS)
    _emit(line);return ev
def banner(text,ch="═"):
    _emit(ch*100);[_emit(x) for x in str(text).splitlines()];_emit(ch*100)

SOURCES={};RAW={}
# EMBEDDED holds byte-exact copies (zlib + base64) of every locked file, written by the build script. A copy is used only after
# its git blob is recomputed and found equal to the lock above, so the cell needs no upload and never runs an unverified file.
EMBEDDED={}                                  # filled at the end of PART 1 (generated by the build — do not edit)
def embedded_copy(name):
    import zlib,base64
    if name not in EMBEDDED:return None,"no embedded copy"
    try:b=zlib.decompress(base64.b64decode("".join(EMBEDDED[name])))
    except Exception as ex:return None,f"embedded copy unreadable ({type(ex).__name__})"
    return (b,None) if git_blob(b)==LOCKS[name] else (None,f"embedded copy blob {git_blob(b)[:12]} != lock")
def fetch_locked(name,timeout=60):
    """order: verified cache → embedded copy → repository (raw GitHub) → /content/<name>. Every candidate must have the locked
    git blob; a candidate with another blob is never executed and is reported. The way the file was obtained is recorded."""
    p=EVID_DIR/name;want=LOCKS[name];notes=[]
    if p.is_file() and git_blob(p.read_bytes())==want:
        raw=p.read_bytes();prev=SOURCES.get(name) or {}
        how=prev.get("obtained") or "cached copy from an earlier start-up (blob verified)";notes=list(prev.get("notes") or [])
    else:
        raw=None;how=None
        if p.is_file():notes.append(f"cached {p.name} has git blob {git_blob(p.read_bytes())[:12]}… (not the lock) — not used")
        b,why=embedded_copy(name)
        if b is not None:raw=b;how="embedded copy in this program (blob verified)"
        else:notes.append(why)
        if raw is None:
            try:
                req=urllib.request.Request(RAW_BASE+name,headers={"User-Agent":"AKBASCORE-TEST878-DEMO"})
                with urllib.request.urlopen(req,timeout=timeout) as f:b=f.read()
                if git_blob(b)==want:raw=b;how="GitHub "+RAW_BASE+name+" (blob verified)"
                else:notes.append(f"GitHub copy has git blob {git_blob(b)[:12]}… (not the lock) — not used")
            except Exception as ex:notes.append(f"GitHub: {type(ex).__name__}: {str(ex)[:120]}")
        loc=_CROOT/name
        if raw is None and loc.is_file():
            b=loc.read_bytes()
            if git_blob(b)==want:raw=b;how=f"local file {loc} (blob verified)"
            else:notes.append(f"{loc} has git blob {git_blob(b)[:12]}… (not the lock) — not used")
        if raw is None:raise RuntimeError(f"LOCKED SOURCE NOT AVAILABLE: {name} — "+" · ".join(notes))
        p.write_bytes(raw)
    SOURCES[name]=dict(bytes=len(raw),git_blob=git_blob(raw),sha256=sha_bytes(raw),url=RAW_BASE+name,obtained=how,notes=notes,verified_utc=utc_now())
    return raw

# ---------------------------------------------------------------------------------------------------------------------
# pipeline state
# ---------------------------------------------------------------------------------------------------------------------
STAGES=OrderedDict([
    ("PRECHECK","Pre-flight — one A100 80 GB, empty GPU, disk, locked 878.py (git blob verified), fresh run folder"),
    ("TEST878","TEST878 engine (own OS process, 878.py unchanged) — exact replay · Experience-CUT3 write · free · SSD reload · native append · native CAR panels"),
    ("VERIFY","Independent re-verification (read-only, host, CPU) — every cartridge file: SHA-256, per-tensor SHA-256, X2/A rows of M = L, gates of the result file"),
    ("FIGURES","Nine scientific figures (JPEG 300 dpi, layout QC) — cartridge heat maps, arms, decisions, contrasts, decision rule"),
    ("RECORDS","Records — real-time engine output, engine result files, verification, manifests (direct downloads, no ZIP)")])
ENGINE_STAGES=("TEST878",)
STATE=dict(started=None,finished=None,current=None,stages={k:dict(status="wait",seconds=None,note="",t0=None) for k in STAGES},version=0,running=False,fig_version=0,elapsed=None)
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
LINES=[]                            # every engine line: (utc, session, stream, line)
CHECKS=[]                           # every gate line of the engine (utc · session · name · detail)
LEDGER=OrderedDict()                # process ledger: one entry per engine session (pid, start, end, exit code, GPU)
GPU_SAMPLES=[]                      # nvidia-smi samples during the whole run (time, used MiB, compute apps)
MILESTONES=OrderedDict()            # first time each engine milestone line was received (UTC, epoch)

# ---------------------------------------------------------------------------------------------------------------------
# PRECHECK
# ---------------------------------------------------------------------------------------------------------------------
def nvsmi(q):
    try:
        r=subprocess.run(["nvidia-smi",f"--query-{q}","--format=csv,noheader,nounits"],capture_output=True,text=True,timeout=30)
        return [l.strip() for l in r.stdout.splitlines() if l.strip()]
    except Exception:return []
def gpu_used_mib():
    g=nvsmi("gpu=memory.used,memory.total")
    if not g:return None,None
    a=g[0].split(", ");return int(float(a[0])),int(float(a[1]))
def hf_home():
    try:
        from huggingface_hub import constants as _c
        return Path(getattr(_c,"HF_HOME",None) or os.path.expanduser("~/.cache/huggingface"))
    except Exception:return Path(os.environ.get("HF_HOME") or os.path.expanduser("~/.cache/huggingface"))
def model_cache_dir():return hf_home()/"hub"/("models--"+MODEL_ID.replace("/","--"))
def _dir_bytes(d):
    try:return sum(f.stat().st_size for f in Path(d).rglob("*") if f.is_file() and not f.is_symlink()) if Path(d).is_dir() else 0
    except Exception:return None
def stage_precheck():
    g=nvsmi("gpu=name,memory.total,memory.used,driver_version");rows=[x.split(", ") for x in g]
    LIVE["gpu"]=dict(count=len(rows),name=rows[0][0] if rows else None,total_mib=int(rows[0][1]) if rows else None,used_mib=int(rows[0][2]) if rows else None,
                     driver=rows[0][3] if rows else None,apps=nvsmi("compute-apps=pid,used_memory"))
    if SIM:LIVE["gpu"].update(count=1,name="SIMULATED A100-SXM4-80GB",total_mib=81920,used_mib=0,apps=[])
    if not LIVE["gpu"]["count"]:raise RuntimeError("no NVIDIA GPU in this runtime — TEST878 needs one A100 80 GB (Runtime → Change runtime type → A100). Nothing was run.")
    if "A100" not in str(LIVE["gpu"]["name"]) or (LIVE["gpu"]["total_mib"] or 0)<70000:raise RuntimeError(f"A100 80 GB required, found {LIVE['gpu']['name']}")
    if (LIVE["gpu"]["used_mib"] or 0)>2048 or LIVE["gpu"]["apps"]:
        raise RuntimeError(f"the GPU is not empty ({LIVE['gpu']['used_mib']} MiB used, processes {LIVE['gpu']['apps']}) — restart the Colab runtime, then run the cell again")
    du=shutil.disk_usage(str(_CROOT));cache=_dir_bytes(model_cache_dir()) or 0
    LIVE["disk"]=dict(free_gib=round(du.free/2**30,1),model_cache_gib=round(cache/2**30,1),hf_home=str(hf_home()))
    need=20 if cache>130e9 else 170          # Qwen2.5-72B-Instruct safetensors ≈ 136 GiB + cartridges, run records and head-room
    LIVE["disk"]["needed_gib"]=need
    if du.free/2**30<need and not SIM:raise RuntimeError(f"not enough disk: {du.free/2**30:.0f} GiB free, about {need} GiB needed ({'model already cached' if cache>130e9 else 'model download ≈ 136 GiB'})")
    for n in LOCKS:RAW[n]=fetch_locked(n)
    RUN_ROOT.mkdir(parents=True,exist_ok=False);os.chmod(RUN_ROOT,0o755)
    ls=RUN_ROOT/"locked_sources";ls.mkdir();os.chmod(ls,0o755)
    for n in LOCKS:
        (ls/n).write_bytes(RAW[n]);os.chmod(ls/n,0o644)
        if git_blob((ls/n).read_bytes())!=LOCKS[n]:raise RuntimeError(f"{n} on disk does not match its lock")
    LIVE["precheck"]=dict(run_root=str(RUN_ROOT),locks={n:SOURCES[n]["git_blob"] for n in LOCKS},engine_obtained=SOURCES[ENGINE_NAME]["obtained"],utc=utc_now())
    return (f"{LIVE['gpu']['name']} · used {LIVE['gpu']['used_mib']} MiB of {LIVE['gpu']['total_mib']} MiB · disk free {LIVE['disk']['free_gib']} GiB · model cache {LIVE['disk']['model_cache_gib']} GiB · "
            f"878.py git blob {LOCKS[ENGINE_NAME][:12]}… ({SOURCES[ENGINE_NAME]['obtained']}) · run folder {RUN_ROOT.name}")

# ---------------------------------------------------------------------------------------------------------------------
# THE ENGINE PROCESS — 878.py (locked) as its own OS process; every line is received, time-stamped, written to
# ENGINE_OUTPUT_REALTIME.log and drives the stage display. Progress bars update ONE line (no flooding).
# 878.py is run as a file: its source capture reads its own file (__file__), so the executed bytes = the locked file.
# ---------------------------------------------------------------------------------------------------------------------
PROGRESS={"line":"","t":0.0};PROC={"p":None};LAST_OUT={"t":time.time()}
ENG=dict(root=None,exp_dir=None,console=None,zip=None,start_t=None)
PROG_RX=re.compile(r"\d+%\|?|it/s\]|s/it\]|B/s\]|\d+/\d+ \[")
MILESTONE_RX=OrderedDict([("GPU_PRECHECK",r"^GPU PRECHECK "),("CONSOLE_CAPTURE",r"^CELL CONSOLE CAPTURE START "),("ENGINE_LOADED",r"^TEST878 ENGINE "),
    ("G0_PREREG",r"^T878 G0 PREREG "),("G0_SOURCE",r"^T878 G0 SOURCE PASS"),("G0_TARGETS",r"^T878 G0 TARGETS "),("G1_PREFLIGHT",r"^T878 G1 PREFLIGHT PASS"),
    ("SOURCE_01_MISSING",r"^T878 SOURCE I867_01_MISSING "),("SOURCE_01_LIVE",r"^T878 SOURCE I867_01_LIVE "),("SOURCE_00_MISSING",r"^T878 SOURCE I867_00_MISSING "),
    ("SOURCE_00_LIVE",r"^T878 SOURCE I867_00_LIVE "),("TARGET_01_FORK",r"^T878 TARGET I867_01_FORK "),("TARGET_00_FORK",r"^T878 TARGET I867_00_FORK "),
    ("WORLD_01",r"^T878 WORLD 01 "),("WORLD_00",r"^T878 WORLD 00 "),("VERDICT",r"^TEST878 VERDICT "),("STATUS",r"^status \S+ \| wall "),("CONSOLE_END",r"^CELL CONSOLE CAPTURE END")])
STEP_NOTE={"GPU_PRECHECK":"GPU pre-check of the engine","CONSOLE_CAPTURE":"engine console capture started","ENGINE_LOADED":"locked engine test870.py loaded (git blob verified)",
    "G0_PREREG":"pre-registration hashed before the model is loaded","G0_SOURCE":"G0 SOURCE PASS — locks, source audit, firewall","G0_TARGETS":"independent targets fixed from the locked records",
    "G1_PREFLIGHT":"model loaded · G1 PREFLIGHT PASS — explicit forward API checked","SOURCE_01_MISSING":"World 01 MISSING cartridge written to SSD","SOURCE_01_LIVE":"World 01 LIVE cartridge written to SSD",
    "SOURCE_00_MISSING":"World 00 MISSING cartridge written to SSD","SOURCE_00_LIVE":"World 00 LIVE cartridge written to SSD","TARGET_01_FORK":"World 01 independent target state captured",
    "TARGET_00_FORK":"World 00 independent target state captured","WORLD_01":"World 01 persistence gate + transfer panels done","WORLD_00":"World 00 persistence gate + transfer panels done",
    "VERDICT":"verdict written","STATUS":"engine status line","CONSOLE_END":"engine packaging its records"}
def _on_line(line,stream,session):
    u=utc_now();LAST_OUT["t"]=time.time()
    with _LOG_LOCK:
        LINES.append((u,session,stream,line))
        new=not ENGINE_OUT.exists()
        with ENGINE_OUT.open("a",encoding="utf-8") as f:f.write(f"{u}\t{session}\t{stream}\t{line}\n")
        if new:_private(ENGINE_OUT)
    if PROG_RX.search(line) and not re.search(r"^(T878|TEST878|TABLE|GPU|CELL) ",line):
        PROGRESS["line"]=short(line,160)
        if time.time()-PROGRESS["t"]>1.0:PROGRESS["t"]=time.time();_emit(f"{SNAME[session]} · {PROGRESS['line']}",progress=True)
        STATE["stages"][session]["note"]=f"{SNAME[session]} process: "+PROGRESS["line"];bump()
        return
    _emit(f"  {SNAME[session]:<8}| {line[:300]}")
    for key,rx in MILESTONE_RX.items():
        if key not in MILESTONES and re.search(rx,line):
            MILESTONES[key]=dict(utc=u,t=time.time(),line=line[:600]);STATE["stages"][session]["note"]=STEP_NOTE[key]+" · "+short(line,220);bump()
            slog("ENGINE_"+key,short(line,380))
    m=re.match(r"^experience namespace: (\S+)",line)
    if m:ENG["exp_dir"]=m.group(1)
    m=re.match(r"^CELL OUTPUT FILE : (\S+)",line)
    if m:ENG["console"]=m.group(1)
    m=re.match(r"^RESULT ZIP\s+: (\S+)",line)
    if m:ENG["zip"]=m.group(1)
    m=re.match(r"^T878 (G0 SOURCE PASS|G0 TARGETS|G1 PREFLIGHT PASS|SOURCE|TARGET|WORLD|POINT_ERROR|PARTIAL|PERSISTENCE_FAIL)\b ?(.*)$",line)
    if m:CHECKS.append(dict(utc=u,session=session,name=m.group(1).replace(" ","_"),result=("FAIL" if m.group(1) in ("POINT_ERROR","PARTIAL","PERSISTENCE_FAIL") else "PASS"),
                           passed=m.group(1) not in ("POINT_ERROR","PARTIAL","PERSISTENCE_FAIL"),detail=m.group(2).strip()[:600]))
    if re.match(r"^(TEST878 ERROR|TEST878 PRE-ENGINE ERROR|T878 POINT_ERROR|T878 PARTIAL|Traceback)",line):slog("ENGINE_PROBLEM",f"{session} {line[:380]}")
def _reader(pipe,stream,session):
    buf=b""
    while True:
        ch=pipe.read1(65536) if hasattr(pipe,"read1") else pipe.read(4096)
        if not ch:break
        buf+=ch
        parts=re.split(rb"[\r\n]",buf);buf=parts.pop()
        for p in parts:
            s=p.decode("utf-8","replace").rstrip()
            if s:_on_line(s,stream,session)
    if buf.strip():_on_line(buf.decode("utf-8","replace").rstrip(),stream,session)
def _sampler(stop,session):
    """nvidia-smi every 10 s while the engine runs (kept in memory and in GPU_SAMPLES.json — not printed)"""
    while True:
        used,total=gpu_used_mib();apps=nvsmi("compute-apps=pid,used_memory")
        GPU_SAMPLES.append(dict(utc=utc_now(),t=time.time(),session=session,used_mib=used,total_mib=total,apps=apps))
        if stop.wait(10):break
def _heartbeat(stop,session,p):
    t0=time.perf_counter()
    while not stop.wait(30):
        STATE["elapsed"]=round(time.perf_counter()-t0);bump()
        if time.time()-LAST_OUT["t"]>300:
            LAST_OUT["t"]=time.time();slog("SESSION_ALIVE",f"{SNAME[session]} still working · {(time.perf_counter()-t0)/60:.0f} min · last progress: {PROGRESS['line'][:100] or '—'}")
        # the engine's optional Google-Drive backup cannot authenticate inside a child process; it must fail at once.
        # If it ever waits instead, the console capture line never comes: the process is stopped and the reason recorded.
        if "GPU_PRECHECK" in MILESTONES and "CONSOLE_CAPTURE" not in MILESTONES and time.time()-MILESTONES["GPU_PRECHECK"]["t"]>600 and p.poll() is None:
            slog("ENGINE_STALLED","no console-capture line 600 s after the GPU pre-check (Drive backup step) — process stopped");p.kill()
def gpu_release_check(session,pid,timeout=120):
    """after the engine process has exited: no compute process left, GPU memory back to idle"""
    if SIM:return dict(released=True,used_mib=0,apps=[],waited_s=0,note="SIMULATION — no GPU")
    t0=time.time()
    while True:
        used,total=gpu_used_mib();apps=nvsmi("compute-apps=pid,used_memory")
        if (used is not None and used<=1024 and not apps) or time.time()-t0>timeout:break
        time.sleep(3)
    return dict(released=bool(used is not None and used<=1024 and not apps),used_mib=used,total_mib=total,apps=apps,waited_s=round(time.time()-t0,1))
def engine_cmd():return [sys.executable,"-u",str(RUN_ROOT/"locked_sources"/ENGINE_NAME)]
def engine_env():
    env=dict(os.environ,PYTHONUNBUFFERED="1",MPLBACKEND="Agg")
    if SIM and os.environ.get("AKB878_SIM_PYTHONPATH"):env["PYTHONPATH"]=os.environ["AKB878_SIM_PYTHONPATH"]
    return env
def _find_root(t0):
    """the engine's own run folder (/content/TEST878_RUN_<stamp>) created by THIS process — never an earlier one"""
    c=[Path(p) for p in glob.glob(str(_CROOT/"TEST878_RUN_*")) if Path(p).is_dir() and Path(p).stat().st_mtime>=t0-5]
    return max(c,key=lambda p:p.stat().st_mtime) if c else None
def results_of(session="TEST878"):
    r=ENG.get("root");return (jload(Path(r)/"878_result.json",{}) or {}) if r else {}
def run_session(session):
    """starts the engine as its own OS process and follows it until it exits"""
    prev=[s for s in LEDGER.values() if s.get("end") is None]
    if prev:raise RuntimeError(f"a previous session is still running: {prev}")
    cmd=engine_cmd();env=engine_env();cwd=str(_CROOT)
    slog("SESSION_START",f"{SNAME[session]} · {' '.join(cmd)}",cwd=cwd,locked_blob=LOCKS[ENGINE_NAME])
    t0=time.time();ENG.update(root=None,exp_dir=None,console=None,zip=None,start_t=t0);MILESTONES.clear()
    rec=LEDGER[session]=dict(session=session,cmd=cmd,user="root" if os.geteuid()==0 else str(os.geteuid()),uid=os.geteuid(),start=utc_now(),start_t=t0,end=None)
    p=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=cwd,env=env,bufsize=0)
    PROC["p"]=p;rec["engine_pid"]=p.pid;stop=threading.Event()
    th=[threading.Thread(target=_reader,args=(p.stdout,"stdout",session),daemon=True),threading.Thread(target=_reader,args=(p.stderr,"stderr",session),daemon=True),
        threading.Thread(target=_sampler,args=(stop,session),daemon=True),threading.Thread(target=_heartbeat,args=(stop,session,p),daemon=True)]
    for t in th:t.start()
    rc=p.wait();th[0].join(60);th[1].join(60);stop.set()
    if PROG_OPEN["open"]:_emit("")
    ENG["root"]=str(_find_root(t0) or "") or None
    res=results_of(session);v=res.get("verdict") or {}
    rec.update(end=utc_now(),end_t=time.time(),seconds=round(time.time()-t0,1),exit_code=rc,status=res.get("status"),verdict=v.get("verdict"),error=res.get("error"),
               engine_root=ENG["root"],experience_dir=ENG["exp_dir"],engine_console=ENG["console"],engine_zip=ENG["zip"])
    samp=[s for s in GPU_SAMPLES if s["session"]==session and s["used_mib"] is not None]
    rec["gpu_peak_used_mib"]=max([s["used_mib"] for s in samp],default=None)
    rec["gpu_release"]=gpu_release_check(session,rec.get("engine_pid"))
    GPU_SAMPLES.append(dict(utc=utc_now(),t=time.time(),session=session+"_released",used_mib=rec["gpu_release"].get("used_mib"),total_mib=rec["gpu_release"].get("total_mib"),apps=rec["gpu_release"].get("apps")))
    slog("SESSION_EXIT",f"{SNAME[session]} exit code {rc} · {rec['seconds']:.0f} s · status {rec['status']} · verdict {rec['verdict']} · GPU released {rec['gpu_release']['released']}",
         engine_root=ENG["root"],experience_dir=ENG["exp_dir"])
    dump_json(DATA_DIR/"PROCESS_LEDGER.json",LEDGER);dump_json(DATA_DIR/"GPU_SAMPLES.json",GPU_SAMPLES);dump_json(DATA_DIR/"ENGINE_MILESTONES.json",MILESTONES)
    if rc!=0 or res.get("status")!="COMPLETE":
        failed=next((l for _,s,_,l in reversed(LINES) if s==session and re.match(r"^(TEST878 ERROR|TEST878 PRE-ENGINE ERROR|T878 POINT_ERROR|T878 PARTIAL)",l)),None)
        raise RuntimeError(f"{SNAME[session]} ended with exit code {rc}, status {res.get('status')}: {failed or res.get('error') or 'no result file'}")
    if not rec["gpu_release"]["released"]:raise RuntimeError(f"GPU not released after {SNAME[session]}: {rec['gpu_release']}")
    return rec
def stage_session(session):
    rec=run_session(session);r=results_of(session);v=r.get("verdict") or {}
    return (f"pid {rec.get('engine_pid')} · exit {rec['exit_code']} · {rec['seconds']/60:.1f} min · status {r.get('status')} · verdict {v.get('verdict')} · scope {v.get('scope')} · "
            f"blocks {v.get('blocks')} · GPU after exit {rec['gpu_release'].get('used_mib')} MiB · records {ENG['root']}")

EMBEDDED.update({                            # generated by the build — do not edit; checked against LOCKS before use
 "878.py":(  # 63463 bytes · git blob 7842e8675544a0328e3552f059c81b7750068a82
  "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"
 ),
 "LICENSE":(  # 4525 bytes · git blob 9aad4724d1072f9e56486650a9527380c867a53b
  "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"
 ),
})
_AKB878_PARTS={1}
# ===== END OF PART 1/3 =====
# ===== PART 2/3 — paste directly after PART 1 in the same cell =====
# =====================================================================================================================
# PART 2 / 3 — independent read-only verification of the engine's records and cartridge files, the figure toolkit
#              (SH782 layout QC + JPEG QC, unchanged) and the nine TEST878 figures. Every number comes from THIS RUN's
#              files; a missing output is drawn as missing — never replaced by values of another run.
# =====================================================================================================================
def R():return results_of("TEST878")
def worlds():return (R().get("worlds") or {})
def panels():
    out=[]
    for w in ("01","00"):
        for kind in ("SAME_GOAL","CROSS_WORLD"):
            p=(worlds().get(w) or {}).get("panels",{}).get(kind)
            if p is not None:out.append((w,kind,p))
    return out
def ptitle(w,kind):
    o="00" if w=="01" else "01"
    return f"World {w} experience → "+(f"same-goal state I867_{w}_FORK" if kind=="SAME_GOAL" else f"World {o} state (cross-world)")

# ---------------------------------------------------------------------------------------------------------------------
# VERIFY — independent, read-only (host, CPU, after the engine process has ended)
# ---------------------------------------------------------------------------------------------------------------------
def kv_digest(t,block=1048576):
    """SHA-256 over the raw bytes of a tensor — the rule of the locked engine's kv_digest (709/730), recomputed on the CPU"""
    import torch
    h=hashlib.sha256();v=t.detach().contiguous().view(torch.uint8).reshape(-1)
    for st in range(0,v.numel(),block):h.update(v[st:st+block].cpu().numpy().tobytes())
    return h.hexdigest()
def _load_cp(p):
    import torch
    return torch.load(p,map_location="cpu",weights_only=True)
def _f32(t):return t.float().numpy()
def _h3_map(h,cbins=64):
    """|H3| mean per (channel bin × token) — CPU, float32"""
    a=np.abs(_f32(h[0]));n,Hd=a.shape;cb=max(1,Hd//cbins)
    return a[:,:cb*cbins].reshape(n,cbins,cb).mean(-1).T.astype(np.float32),Hd
def _kv_norms(lower):
    rows=[];labels=[]
    for i,(k,v) in enumerate(lower):
        for nm,t in (("K",k),("V",v)):
            x=_f32(t[0]);rows.append(np.sqrt((x**2).sum(axis=(0,2))));labels.append(f"L{i} {nm}")
    return np.array(rows,np.float32),labels
def stage_verify():
    res=R();root=Path(ENG["root"]) if ENG.get("root") else None
    if not res or root is None:raise RuntimeError("no 878_result.json of this RUN — nothing to verify (nothing is substituted)")
    man=jload(root/"878_experience_manifest.json",{}) or {};ent=res.get("experience") or {}
    V=dict(result_file=str(root/"878_result.json"),result_sha256=sha_file(root/"878_result.json"),cartridges=OrderedDict(),pairs={},engine={},problems=[],utc=utc_now());probs=V["problems"]
    V["engine"]=dict(status=res.get("status"),verdict=(res.get("verdict") or {}).get("verdict"),blocks=(res.get("verdict") or {}).get("blocks"),
                     executed_blob=(res.get("source") or {}).get("executed_cell_git_blob"),executed_equals_locked_file=(res.get("source") or {}).get("executed_cell_git_blob")==ENGINE_BLOB,
                     firewall=(res.get("source") or {}).get("firewall"),prereg=res.get("prereg_sha256"),manifest_equals_result=(man==ent))
    if not V["engine"]["executed_equals_locked_file"]:probs.append("executed source != locked 878.py")
    if not V["engine"]["manifest_equals_result"]:probs.append("experience manifest != result file")
    cps={}
    for eid,e in ent.items():
        p=Path(e["file"]);row=dict(id=eid,file=str(p),present=p.is_file())
        if p.is_file():
            t=time.perf_counter();s=sha_file(p);row.update(bytes=p.stat().st_size,sha256_now=s,sha256_record=e["sha256"],file_sha_ok=(s==e["sha256"]),hash_s=round(time.perf_counter()-t,2))
            cp=_load_cp(p);keys=sorted(cp)
            ts=dict(h=kv_digest(cp["h"]),lower=[[kv_digest(k),kv_digest(v)] for k,v in cp["lower"]])
            row.update(keys=keys,only_state_keys=(keys==sorted(["h","lower","n","p","body_tokens","book_id"])),tensor_sha_ok=(ts==e["tensor_sha"]),
                       h_shape=list(cp["h"].shape),h_dtype=str(cp["h"].dtype),k_shape=list(cp["lower"][0][0].shape),layers=len(cp["lower"]),n=int(cp["n"]),p=int(cp["p"]),
                       body_tokens=int(cp["body_tokens"]),book_id_ok=(cp["book_id"]==eid),prefix_rows_zero=bool(float(np.abs(_f32(cp["h"][0,:int(cp["p"])])).max())==0.0))
            cps[eid]=cp
        else:row.update(file_sha_ok=False)
        V["cartridges"][eid]=row
        for k in ("file_sha_ok","tensor_sha_ok","only_state_keys","book_id_ok"):
            if k in row and not row[k]:probs.append(f"{eid} {k}")
        slog("VERIFIED_CARTRIDGE",eid,**{k:v for k,v in row.items() if k in("file_sha_ok","tensor_sha_ok","only_state_keys","bytes","sha256_now")})
    import torch
    ana={}
    for w in ("01","00"):
        a,b=cps.get(f"X878_{w}_MISSING"),cps.get(f"X878_{w}_LIVE")
        if a is None or b is None:continue
        pv=ent[f"X878_{w}_MISSING"]["provenance"];sp=pv["spans_body"];P_=int(a["p"]);c0=P_+sp["C"][0];n=int(a["n"])
        pr=dict(same_length=(a["h"].shape==b["h"].shape),
                h_X2A_bitwise=bool(torch.equal(a["h"][:,P_:c0],b["h"][:,P_:c0])),h_C_differs=not bool(torch.equal(a["h"][:,c0:],b["h"][:,c0:])),
                lower_X2A_bitwise=all(bool(torch.equal(a["lower"][i][j][:,:,P_:c0],b["lower"][i][j][:,:,P_:c0])) for i in range(len(a["lower"])) for j in (0,1)),
                lower_C_differs=any(not bool(torch.equal(a["lower"][i][j][:,:,c0:],b["lower"][i][j][:,:,c0:])) for i in range(len(a["lower"])) for j in (0,1)),
                spans=sp,P=P_,n=n)
        V["pairs"][w]=pr
        for k in ("same_length","h_X2A_bitwise","h_C_differs","lower_X2A_bitwise","lower_C_differs"):
            if not pr[k]:probs.append(f"pair {w} {k}")
        hm,Hd=_h3_map(a["h"][:,P_:]);hl,_=_h3_map(b["h"][:,P_:]);dm,_=_h3_map((a["h"][:,P_:].float()-b["h"][:,P_:].float()))
        kv,kvl=_kv_norms([(k[:,:,P_:],v[:,:,P_:]) for k,v in a["lower"]]);kvd,_=_kv_norms([(ka[:,:,P_:].float()-kb[:,:,P_:].float(),va[:,:,P_:].float()-vb[:,:,P_:].float())
                                                                          for (ka,va),(kb,vb) in zip(a["lower"],b["lower"])])
        ana[w]=dict(h3_M=hm,h3_L=hl,h3_diff=dm,kv_M=kv,kv_diff=kvd,kv_labels=np.array(kvl),x2=sp["X2"],a=sp["A"],c=sp["C"],hidden=Hd,P=P_)
        slog("PAIR_VERIFIED",f"World {w}: X2/A rows of the MISSING and LIVE cartridges bit-identical {pr['h_X2A_bitwise'] and pr['lower_X2A_bitwise']} · C rows differ {pr['h_C_differs']}")
    if ana:
        np.savez_compressed(DATA_DIR/"CARTRIDGE_ANATOMY.npz",**{f"{w}_{k}":v for w,d in ana.items() for k,v in d.items()});_private(DATA_DIR/"CARTRIDGE_ANATOMY.npz")
    cps.clear();gc.collect()
    v=res.get("verdict") or {}
    if res.get("status")!="COMPLETE":probs.append(f"engine status {res.get('status')}")
    if v.get("blocks"):probs.append(f"engine blocks {v.get('blocks')}")
    LIVE["verification"]=V;dump_json(VERIFY_FILE,V)
    n_ok=sum(1 for r in V["cartridges"].values() if r.get("file_sha_ok") and r.get("tensor_sha_ok"))
    note=(f"{n_ok}/{len(V['cartridges'])} cartridge files: file SHA-256 + every tensor SHA-256 re-computed equal to the engine's records · "
          f"X2/A rows of M = L bit for bit: {', '.join(w+' '+okm(p['h_X2A_bitwise'] and p['lower_X2A_bitwise']) for w,p in V['pairs'].items())} · "
          f"executed source = locked 878.py {okm(V['engine']['executed_equals_locked_file'])} · engine verdict {V['engine']['verdict']} · blocks {V['engine']['blocks']}")
    if probs:raise RuntimeError(note+" · PROBLEMS: "+", ".join(probs))
    return note
def anatomy():
    try:return np.load(DATA_DIR/"CARTRIDGE_ANATOMY.npz",allow_pickle=False)
    except Exception:return None

# ===== figures follow =====
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.linewidth":.9,"axes.edgecolor":NEU,"axes.labelcolor":INK,"xtick.color":NEU,"ytick.color":NEU,
                     "xtick.labelsize":8.5,"ytick.labelsize":8.5,"axes.labelsize":9.5,"axes.titlesize":10.5,"axes.titleweight":"bold","axes.titlelocation":"left",
                     "legend.fontsize":8.5,"legend.frameon":False})
FW,FH=13.333,7.5;OUT_DPI=300;MONO="DejaVu Sans Mono"
FIGURES=OrderedDict([
    ("F1",dict(n=1,title="Write · Free · Reload · Append · Decide — the TEST878 Mechanism",slug="MECHANISM_PIPELINE",tab="OVERVIEW")),
    ("F2",dict(n=2,title="Experience-CUT3 Cartridge — What Is Physically Stored",slug="CARTRIDGE_ANATOMY",tab="CARTRIDGES")),
    ("F3",dict(n=3,title="Persistence and Parity Gates — Measured, Not Assumed",slug="PERSISTENCE_PARITY_GATES",tab="PERSISTENCE · PARITY")),
    ("F4",dict(n=4,title="Causal Arms — Which Rows Each Computation May Read",slug="CAUSAL_ARMS_VISIBILITY",tab="TRANSFER PANELS")),
    ("F5",dict(n=5,title="Native CAR Decisions of the Frozen Model in Independent States",slug="NATIVE_CAR_DECISIONS",tab="TRANSFER PANELS")),
    ("F6",dict(n=6,title="Outcome Contrast Signatures — 15 Pairwise Native Margins",slug="OUTCOME_CONTRAST_SIGNATURES",tab="TRANSFER PANELS")),
    ("F7",dict(n=7,title="Pre-registered Decision Rule — Outcome Transfer and Action Information",slug="DECISION_RULE",tab="DECISION RULE")),
    ("F8",dict(n=8,title="Run Timeline, GPU Memory and Process Record",slug="TIMELINE_GPU",tab="RESOURCES")),
    ("F9",dict(n=9,title="What This Run Shows — Claims Ledger",slug="CLAIMS_LEDGER",tab="OVERVIEW"))])
BASE_FIGURES=OrderedDict(FIGURES)
FIG_FILES={};FIG_ERRORS={};PROVENANCE={}
BADGE_COL={"SCHEMATIC":NEU,"LIVE MEASUREMENT":OK_COL,"SEALED MEMORY":COL["FULL"],"OBSERVATIONAL":AMBER,"VERIFICATION RECORD":NEU,"NOT PRODUCED IN THIS RUN":RED}
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
def okm(v):return "✓" if v else ("✗" if v is False else "–")
def _date():return datetime.now().astimezone().strftime("%Y-%m-%d")
def fig_base(key,subtitle,badge):
    meta=FIGURES[key];fig=plt.figure(figsize=(FW,FH),dpi=100,facecolor=BG);bcol=BADGE_COL.get(badge,NEU)
    b=fig.text(.965,.952,badge,fontsize=10,weight="bold",color=bcol,va="center",ha="right",bbox=dict(boxstyle="square,pad=0.35",fc="white",ec=bcol,lw=1.2))
    bx0=_bb(fig,b).x0-.012
    T(fig,.035,.952,f"Figure {meta['n']} — {meta['title']}",size=18,weight="bold",xmax=bx0,minsize=12)
    T(fig,.035,.912,subtitle,size=10.5,color=INK2,xmax=.965,minsize=7.0)
    hline(fig,.035,.965,.888,INK2,.8)
    if SIM:fig.text(.5,.47,"SIMULATION — NOT EXPERIMENTAL DATA",fontsize=40,color=RED,alpha=.12,rotation=18,ha="center",va="center",weight="bold",gid="qc-ignore",zorder=100)
    return fig
def fig_footer(fig,key,note):
    meta=FIGURES[key];hline(fig,.035,.965,.072,RULE,.7)
    T(fig,.035,.050,note,size=8.4,color=INK2,xmax=.965,minsize=6.0)
    T(fig,.035,.022,f"{APP_NAME} · {EXPERIMENT} · demo {CODE_VERSION} · {_date()} · 878.py git blob {LOCKS[ENGINE_NAME][:10]} · run {SESSION_ID}"+(" · SIMULATION" if SIM else "")+f" · Figure {meta['n']}/{len(BASE_FIGURES)}",
      size=7.6,color=MUTED,xmax=.965,minsize=5.5,mono=True)
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
    stem=("SIMULATION_" if SIM else "")+f"TEST878_FIG{num:02d}_{meta['slug']}{suffix}";jpg=FIG_DIR/(stem+".jpg")
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
    fig_footer(fig,key,"Placeholder by design: TEST878 figures are drawn only from outputs of this RUN (no earlier run, no representative values).")
    return save_fig(fig,key,"NOT PRODUCED IN THIS RUN",["(none — output missing)"],"_NOT_PRODUCED")
def _axstyle(ax,fs=8):
    for s in ("top","right"):ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=fs)
def _t(u):
    try:return datetime.fromisoformat(u).timestamp()
    except Exception:return None
EXACT_GREEN="#A7F3D0"
# ===== figure functions =====
def sides():return R().get("sides") or {}
def exps():return R().get("experience") or {}
def _src(w,c):return sides().get(f"I867_{w}_{c}") or {}
def _exp(w,c):return exps().get(f"X878_{w}_{c}") or {}
def _spans(w):
    e=_exp(w,"MISSING");return ((e.get("provenance") or {}).get("spans_body")) or {}
def _status_col(s):
    return {"ACTION_INFORMATION_DEPENDENT_TRANSFER":OK_COL,"OUTCOME_TRANSFER_ONLY":COL["AR"],"NO_TRANSFER":MUTED,"TRANSFER_A_BLIND_INVALID":AMBER}.get(s,RED)
def fig1():
    k="F1";res=R()
    if not res.get("sides"):return fig_missing(k,"The mechanism is drawn with the values of this RUN's engine records.","The engine did not write its result file in this RUN.")
    fig=fig_base(k,"One real experience becomes a file of the model's own internal states — the file is reloaded later and changes a decision in a state that never saw it","SCHEMATIC")
    s0=_src("00","MISSING");s1=_src("00","LIVE");e0=_exp("00","MISSING");sp=_spans("00");api=res.get("api") or {};sh=api.get("shape") or [80,8192,64,8,128]
    steps=[("1 · REAL EXPERIENCE","exact replay of the locked trace",[f"World 01 and World 00, same start state","MISSING and LIVE branches share t2","executed action: ACQUIRE (2 tokens)",
            "real outcome C: MISSING / LIVE","replay checked event by event"],"#374151"),
           ("2 · CAPTURE [X2][A][C]","model's own states, no text",[f"X2 decision input {sp.get('X2',[0,0])[1]-sp.get('X2',[0,0])[0]} tok",f"A executed action {sp.get('A',[0,0])[1]-sp.get('A',[0,0])[0]} tok",
            f"C real outcome {sp.get('C',[0,0])[1]-sp.get('C',[0,0])[0]} tok","X2/A: layers 0–3 run explicitly,","bit-equal to the native cache"],COL["FULL"]),
           ("3 · WRITE → SSD","Experience-CUT3 file (.pt)",[f"H3 = layer-3 output, {sh[1]} ch","K/V of layers 0–3 (8 KV heads)",f"{fmt_b(e0.get('bytes'))} · append-only folder","SHA-256 of file + every tensor","no X3 / EVAL / CAR rows"],COL["M"]),
           ("4 · FREE","source working state deleted",["post-outcome KV cache freed","H3 and outcome tensors freed","garbage-collected, GPU cache emptied","only the SSD file remains","(nothing kept in Python)"],"#6B7280"),
           ("5 · RELOAD + APPEND","into an INDEPENDENT state",["torch.load + SHA re-check","K/V L0–3 re-phased (RoPE)","H3 placed at the layer-3 cut",f"layers 4–{sh[0]-1} recomputed by the","frozen model (native append)"],COL["L"]),
           ("6 · NATIVE DECISION","CAR reading of the frozen model",["target's OWN decision input X","log p of 6 action words:","first token + teacher-forced rest","decision = argmax of the model's","own log p; nothing executed"],COL["AR"])]
    W=.1435;G=.0118;x0=.035;yb=.565;hb=.285
    for i,(t,sub,lines,c) in enumerate(steps):
        x=x0+i*(W+G);box(fig,x,yb,W,hb,ec=c,lw=1.6);rect(fig,x,yb+hb-.036,W,.036,c,z=2)
        Tc(fig,x+.004,x+W-.004,yb+hb-.018,t,size=9.0,weight="bold",color="white")
        Tc(fig,x+.004,x+W-.004,yb+hb-.058,sub,size=7.6,weight="bold",color=c)
        for j,l in enumerate(lines):Tc(fig,x+.005,x+W-.005,yb+hb-.098-j*.036,l,size=7.4,color=INK)
        if i<len(steps)-1:arrow(fig,x+W+.001,yb+hb/2,x+W+G-.001,yb+hb/2,col=NEU,lw=1.5,ms=10)
    # the layer stack: what is stored and what is recomputed
    ys=.395;T(fig,.035,ys+.115,"Where the cartridge enters the frozen transformer (CUT3)",size=9.2,weight="bold",color=INK2)
    nL=int(sh[0]);X0,X1=.035,.62;sx=lambda l:X0+(X1-X0)*l/nL
    rect(fig,sx(0),ys,sx(4)-sx(0),.075,"#FDE7D7",ec=COL["M"],lw=1.2,z=2);rect(fig,sx(4),ys,sx(nL)-sx(4),.075,"#EDE9FE",ec=COL["FULL"],lw=1.2,z=2)
    Tc(fig,sx(0)+.002,sx(4)-.002,ys+.052,"L0–L3",size=8.2,weight="bold",color=COL["M"]);Tc(fig,sx(0)+.002,sx(4)-.002,ys+.022,"stored",size=7.2,color=COL["M"])
    Tc(fig,sx(4)+.01,sx(nL)-.01,ys+.052,f"layers 4 … {nL-1} — never stored: recomputed by the frozen Qwen2.5-72B on every append",size=8.2,weight="bold",color=COL["FULL"])
    Tc(fig,sx(4)+.01,sx(nL)-.01,ys+.022,"while attending to everything the target already holds (causal order)",size=7.4,color=COL["FULL"])
    vline(fig,sx(4),ys-.012,ys+.087,col=RED,lw=1.6);T(fig,sx(4)+.003,ys-.022,"CUT3: H3 enters here",size=7.4,color=RED,weight="bold")
    T(fig,.035,ys-.052,"K/V of L0–L3 stored per token; H3 (layer-3 output) stored per token → the model continues from layer 4 exactly as if it had read the experience itself.",size=7.6,color=INK2,xmax=.62)
    # python / no-python
    box(fig,.035,.095,.585,.205,ec=NEU,fc=PANEL,lw=1.2)
    T(fig,.045,.282,"What the Python code does — and what it never does",size=9.0,weight="bold",xmax=.61)
    does=["replays the recorded real actions; writes / reads files; SHA-256","builds attention visibility masks for the control arms","reads the model's own log-probabilities of the 6 action words"]
    never=["choose an action, add a bonus, edit or re-weight logits","train, update or touch weights (digest identical before/after)","register hooks; output_hidden_states; text of the experience in the prompt"]
    for j,t in enumerate(does):T(fig,.045,.250-j*.026,"✓ "+t,size=7.3,color=OK_COL,xmax=.33)
    for j,t in enumerate(never):T(fig,.335,.250-j*.026,"✗ "+t,size=7.3,color=RED,xmax=.612)
    T(fig,.045,.152,wrap("The CUT3 bridge of the locked engine (DirectCut3, TEST730) places the stored H3 rows at the output of layer 3 during the append only, then restores the layer; "
      "hook audits before and after every capture report 0 hooks, and an AST firewall rejects hooks, backward(), optimizer steps and hidden-state shortcuts in all TEST878 functions.",118,3),size=7.0,color=INK2,va="top",linespacing=1.2,xmax=.612)
    v=res.get("verdict") or {};L=LEDGER.get("TEST878") or {};pk=max([float(W_.get("peak_gib") or 0) for W_ in worlds().values()]+[0])
    box(fig,.645,.095,.32,.375,ec=COL["FULL"],lw=1.4)
    T(fig,.655,.448,"This RUN",size=9.4,weight="bold",color=COL["FULL"],xmax=.96)
    rows=[("model",f"{MODEL_ID} · NF4 · BF16 · frozen"),("geometry",f"{sh[0]} layers · hidden {sh[1]} · {sh[2]} q / {sh[3]} kv heads · head {sh[4]}"),
          ("software",f"transformers {api.get('transformers','—')} · torch {api.get('torch','—')} · {api.get('attn','—')}"),
          ("engine",f"878.py {LOCKS[ENGINE_NAME][:12]}… → executed bytes {'identical ✓' if (res.get('source') or {}).get('executed_cell_git_blob')==ENGINE_BLOB else 'see record'}"),
          ("pre-registration",f"{str(res.get('prereg_sha256',''))[:24]}… (before model load)"),("engine status",f"{res.get('status')} · blocks {v.get('blocks')}"),
          ("verdict",str(v.get("verdict"))),("cross-world",f"{v.get('cross_world_class')}"),("process",f"{(L.get('seconds') or 0)/60:.1f} min · GPU peak (torch) {pk:.2f} GiB")]
    for j,(a,b) in enumerate(rows):
        y=.415-j*.034;T(fig,.655,y,a,size=7.4,weight="bold",color=MUTED);T(fig,.738,y,b,size=7.4,color=INK,xmax=.96,mono=(a in ("engine","pre-registration")))
    fig_footer(fig,k,"Values: 878_result.json of this RUN (sides, experience, api, verdict) and the host's process ledger. Spans shown for World 00; World 01 in Figure 2.")
    return save_fig(fig,k,"SCHEMATIC",["878_result.json","PROCESS_LEDGER.json"])
def fig2():
    k="F2";Z=anatomy();V=(LIVE.get("verification") or {}).get("cartridges") or {}
    if Z is None or not exps():return fig_missing(k,"The cartridge anatomy is measured by the host from the four cartridge files of this RUN.","The cartridge files were not produced or not verified in this RUN.")
    fig=fig_base(k,"Measured by the host from the .pt files on the SSD (read-only, CPU) — the cartridge holds the frozen model's internal states, not text","LIVE MEASUREMENT")
    for i,w in enumerate(("01","00")):
        if f"{w}_h3_M" not in Z:continue
        x=.06+i*.315;wd=.27;x2,a,c=Z[f"{w}_x2"],Z[f"{w}_a"],Z[f"{w}_c"];n=int(c[1])
        def seg(ax):
            for t in (a[0],c[0]):ax.axvline(t-.5,color=RED,lw=1.1,ls="--")
            ax.set_xlim(-.5,n-.5)
        T(fig,x,.868,f"World {w} · MISSING vs LIVE cartridge",size=9.4,weight="bold",color=INK,xmax=x+wd)
        ax=fig.add_axes([x,.60,wd,.19]);ax.imshow(np.log10(Z[f"{w}_h3_M"]+1e-6),aspect="auto",origin="lower",cmap="viridis",interpolation="nearest");seg(ax)
        ax.set_yticks([0,Z[f"{w}_h3_M"].shape[0]-1]);ax.set_yticklabels(["0",str(int(Z[f"{w}_hidden"])-1)]);ax.set_xticks([]);_axstyle(ax,7)
        ax.set_title("H3 of the MISSING cartridge · log10 |activation|",fontsize=8.2)
        D=Z[f"{w}_h3_diff"];ax2=fig.add_axes([x,.375,wd,.18]);Dp=np.where(D>0,D,np.nan)
        ax2.imshow(np.log10(Dp),aspect="auto",origin="lower",cmap="magma_r",interpolation="nearest")
        ax2.imshow(np.where(D==0,1.0,np.nan),aspect="auto",origin="lower",cmap=ListedColormap([EXACT_GREEN]),vmin=0,vmax=1,interpolation="nearest");seg(ax2)
        ax2.set_yticks([0,D.shape[0]-1]);ax2.set_yticklabels(["0",str(int(Z[f"{w}_hidden"])-1)]);ax2.set_xticks([]);_axstyle(ax2,7)
        ax2.set_title("|H3(MISSING) − H3(LIVE)| · green = exactly 0",fontsize=8.2)
        kv=Z[f"{w}_kv_diff"];ax3=fig.add_axes([x,.17,wd,.15]);kp=np.where(kv>0,kv,np.nan)
        ax3.imshow(np.log10(kp),aspect="auto",origin="lower",cmap="magma_r",interpolation="nearest")
        ax3.imshow(np.where(kv==0,1.0,np.nan),aspect="auto",origin="lower",cmap=ListedColormap([EXACT_GREEN]),vmin=0,vmax=1,interpolation="nearest");seg(ax3)
        ax3.set_yticks(range(len(Z[f"{w}_kv_labels"])));ax3.set_yticklabels([str(s) for s in Z[f"{w}_kv_labels"]],fontsize=5.8)
        ax3.set_xticks([x2[0],a[0],n-1]);ax3.set_xticklabels([str(int(x2[0])),f"{int(a[0])}|{int(c[0])}",str(n-1)],fontsize=6.5);_axstyle(ax3,6.5)
        ax3.set_title("|K/V L0–L3 (MISSING − LIVE)| per token · green = 0",fontsize=8.2);ax3.set_xlabel("cartridge row (body)",fontsize=7.4)
        for lo,hi,lab,cl in ((x2[0],a[0],"X2 · decision input",NEU),(a[0],c[0],"A",RED),(c[0],n,"C · real outcome",COL["M"])):
            xa=x+wd*(lo/n);xe=x+wd*(hi/n)
            if xe-xa>.012:Tc(fig,xa,xe,.843,lab,size=7.2,weight="bold",color=cl)
    box(fig,.68,.10,.285,.775,ec=COL["M"],lw=1.4)
    T(fig,.69,.855,"The four cartridge files of this RUN",size=9.2,weight="bold",color=COL["M"],xmax=.96)
    y=.825
    for w in ("01","00"):
        for cnd in ("MISSING","LIVE"):
            e=_exp(w,cnd);pv=e.get("provenance") or {};v=V.get(f"X878_{w}_{cnd}") or {};sp=pv.get("spans_body") or {}
            if not e:continue
            T(fig,.69,y,f"X878_{w}_{cnd}",size=7.8,weight="bold",color=COL["M"] if cnd=="MISSING" else COL["L"],mono=True,xmax=.96);y-=.024
            for t in (f"outcome {pv.get('outcome_cartridge')} · action {pv.get('action')}",
                      f"X2 {sp.get('X2',[0,0])[1]} · A {sp.get('A',[0,0])[1]-sp.get('A',[0,0])[0]} · C {sp.get('C',[0,0])[1]-sp.get('C',[0,0])[0]} rows · prefix P={e.get('p')}",
                      f"{fmt_b(e.get('bytes'))} · h {tuple(v.get('h_shape') or [])} {str(v.get('h_dtype','')).replace('torch.','')}",
                      f"SHA {str(e.get('sha256',''))[:28]}…",
                      f"host: file {okm(v.get('file_sha_ok'))} tensors {okm(v.get('tensor_sha_ok'))} keys {okm(v.get('only_state_keys'))} · RoPE rt {e.get('roundtrip_K_rel',0):.4f}"):
                T(fig,.69,y,t,size=6.7,color=INK2,mono=t.startswith("SHA"),xmax=.96);y-=.021
            y-=.008
    pr=(LIVE.get("verification") or {}).get("pairs") or {}
    T(fig,.69,y-.004,"MISSING vs LIVE, same world: X2, A rows bit-identical",size=7.2,weight="bold",color=OK_COL,xmax=.96)
    T(fig,.69,y-.028,"   "+" · ".join(f"W{w} {okm(p.get('h_X2A_bitwise') and p.get('lower_X2A_bitwise'))}" for w,p in pr.items())+" → only C (the real outcome) differs",size=7.0,color=INK2,xmax=.96)
    T(fig,.06,.1,"Keys: only {h, lower, n, p, body_tokens, book_id} — no text, no score, no action label, no X3 / PRED / EVAL / CAR rows. Red dashed lines: X2 | A | C boundaries.",size=7.4,color=INK2,xmax=.665)
    fig_footer(fig,k,"Host, read-only, CPU: torch.load(X878_*.pt, weights_only) → |H3| per 64 channel bins × row; K/V L0–L3 L2-norm differences; torch.equal on the X2/A rows; SHA-256 recomputed.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST878_EXPERIENCE_CUT3_*/X878_*.pt","CARTRIDGE_ANATOMY.npz","POST_RUN_VERIFICATION.json","878_result.json experience"])
def _cell(fig,x,y,w,h,ok,txt=None,size=7.6):
    c=OK_COL if ok is True else (RED if ok is False else (AMBER if ok=="info" else MUTED))
    rect(fig,x,y,w,h,{OK_COL:"#D1FAE5",RED:"#FEE2E2",AMBER:"#FEF3C7",MUTED:"#F3F4F6"}[c],ec="white",lw=1,z=2)
    Tc(fig,x+.002,x+w-.002,y+h/2,txt if txt is not None else okm(ok if ok in (True,False) else None),size=size,weight="bold",color=c)
def fig3():
    k="F3";S=sides();Wd=worlds()
    if not S or not Wd:return fig_missing(k,"The gates are read from this RUN's engine records.","The engine did not write its result file in this RUN.")
    fig=fig_base(k,"Every gate below must hold before a transfer number is used — the engine checks them on the A100, the host re-checks the files afterwards","VERIFICATION RECORD")
    cols=[("01","MISSING"),("01","LIVE"),("00","MISSING"),("00","LIVE")];V=(LIVE.get("verification") or {}).get("cartridges") or {}
    rows=[("capture","t2 native CAR = locked record (exact)",lambda w,c:_src(w,c).get("checks",{}).get("t2_CAR_equals_record")),
          ("capture","explicit L0–3 K/V = native cache (bitwise)",lambda w,c:_src(w,c).get("checks",{}).get("explicit_lower_KV_bitwise")),
          ("capture","layer-4 K/V from captured H3 = native (bitwise)",lambda w,c:_src(w,c).get("checks",{}).get("h3_next_layer_KV_bitwise")),
          ("capture","real outcome cartridge mounted by the replay",lambda w,c:_src(w,c).get("checks",{}).get("card_mounted")),
          ("capture","canonical H reproduces TEST873 (≤ 6e-4)",lambda w,c:_src(w,c).get("checks",{}).get("H_reproduces_873")),
          ("capture","source memory seal unchanged · hook-free",lambda w,c:bool(_src(w,c).get("checks",{}).get("memory_seal")) and bool(_src(w,c).get("checks",{}).get("hook_free"))),
          ("reload","SSD reload: file + every tensor SHA-256",lambda w,c:((Wd.get(w) or {}).get("persistence") or {}).get(c,{}).get("reloaded_sha_ok")),
          ("reload","rebuilt L0–3 rows = sealed source rows (bitwise)",lambda w,c:((Wd.get(w) or {}).get("persistence") or {}).get(c,{}).get("lower_rows_bitwise")),
          ("reload","RoPE K round trip ≤ 1e-2 (relative)",lambda w,c:(e:=_exp(w,c)) and e.get("roundtrip_K_rel",1)<=1e-2),
          ("reload","same native action after reconstruction",lambda w,c:((Wd.get(w) or {}).get("persistence") or {}).get(c,{}).get("action_same")),
          ("reload","explicit append = locked native append (80 layers)",lambda w,c:((Wd.get(w) or {}).get("persistence") or {}).get(c,{}).get("explicit_append_equals_native_bitwise")),
          ("host","file SHA-256 re-computed after the run",lambda w,c:(V.get(f"X878_{w}_{c}") or {}).get("file_sha_ok")),
          ("host","every tensor SHA-256 re-computed after the run",lambda w,c:(V.get(f"X878_{w}_{c}") or {}).get("tensor_sha_ok"))]
    x0=.035;lw_=.30;cw=.043;y0=.83;rh=.041
    for j,(w,c) in enumerate(cols):Tc(fig,x0+lw_+j*cw,x0+lw_+(j+1)*cw,y0+.02,f"W{w} {c[0]}",size=7.6,weight="bold",color=COL["M"] if c=="MISSING" else COL["L"])
    grp=None
    for i,(g,lab,fn) in enumerate(rows):
        y=y0-(i+1)*rh
        if g!=grp:grp=g;T(fig,x0,y+rh*.5,{"capture":"capture","reload":"reload","host":"host"}[g],size=6.8,weight="bold",color=MUTED,rotation=0)
        T(fig,x0+.045,y+rh/2,lab,size=7.2,color=INK,xmax=x0+lw_-.004)
        for j,(w,c) in enumerate(cols):
            try:ok=bool(fn(w,c)) if fn(w,c) is not None else None
            except Exception:ok=None
            _cell(fig,x0+lw_+j*cw,y,cw,rh*.92,ok)
    # panel gates
    P=panels();px=.565;pw=.40;pcw=pw*.55/max(len(P),1)
    T(fig,px,.862,"Transfer-panel gates (independent target states)",size=9.0,weight="bold",xmax=.965)
    for j,(w,kind,p) in enumerate(P):Tc(fig,px+pw*.45+j*pcw,px+pw*.45+(j+1)*pcw,.835,f"W{w} {'same' if kind=='SAME_GOAL' else 'cross'}",size=7.0,weight="bold")
    prow=[("BASE = BASE_EXPLICIT (exact log p)",lambda p:(p.get("vs_base") or {}).get("BASE_EXPLICIT",{}).get("seq")==0 and (p.get("arms") or {}).get("BASE")==(p.get("arms") or {}).get("BASE_EXPLICIT")),
          ("pre-C rows of M and L equal (bitwise)",lambda p:(p.get("gates") or {}).get("pre_C_rows_bitwise_M_eq_L")),
          ("C-BLIND MISSING = C-BLIND LIVE (exact)",lambda p:(p.get("gates") or {}).get("C_BLIND_M_equals_L")),
          ("target memory unchanged (seal)",lambda p:(p.get("gates") or {}).get("target_memory_unchanged")),
          ("all margins finite",lambda p:(p.get("gates") or {}).get("finite_margins")),
          ("A-REF interpretable (3 conditions)",lambda p:(p.get("A_ref") or {}).get("interpretable") if p.get("detect",{}).get("outcome_seq") else "n/a")]
    for i,(lab,fn) in enumerate(prow):
        y=.80-(i+1)*.04;T(fig,px,y+.02,lab,size=7.0,xmax=px+pw*.45-.004)
        for j,(w,kind,p) in enumerate(P):
            v=fn(p);_cell(fig,px+pw*.45+j*pcw,y,pcw,.037,(None if v=="n/a" else bool(v)),("n/a" if v=="n/a" else None),size=7.2)
    # reconstruction numbers
    ax=fig.add_axes([px+.05,.13,pw-.06,.27]);labs=[];dp=[]
    for w,c in cols:
        r=((Wd.get(w) or {}).get("persistence") or {}).get(c) or {}
        if r:labs.append(f"W{w} {c[0]}");dp.append(max(float(r.get("max_dp",0)),1e-7))
    if dp:
        ax.bar(range(len(dp)),dp,color=[COL["M"] if l.endswith("M") else COL["L"] for l in labs]);ax.set_yscale("log");ax.set_xticks(range(len(dp)));ax.set_xticklabels(labs,fontsize=7);ax.set_xlim(-.6,len(dp)+.9)
        ax.axhline(0.10,color=OK_COL,lw=1.3,ls="--");ax.axhline(6e-4,color=AMBER,lw=1.3,ls=":");ax.set_ylim(1e-4,1.0)
        ax.legend(handles=[Line2D([0],[0],color=OK_COL,ls="--",lw=1.3,label="pre-registered persistence bound 0.10"),Line2D([0],[0],color=AMBER,ls=":",lw=1.3,label="exact-sequence bound 6e-4 (reported only)")],
                  loc="upper right",fontsize=6.2,frameon=True,framealpha=1)
        for i_,v_ in enumerate(dp):ax.text(i_,v_*1.25,f"{v_:.4f}",ha="center",fontsize=6.4)
    ax.set_title("reconstruction: max |Δp| of the native CAR vs the source",fontsize=8.2);_axstyle(ax,6.8)
    T(fig,.035,.235,wrap("The 6e-4 bound holds only for an identical call sequence; the cartridge recomputes layers 4–79 in 128-token chunks (BF16 summation order), "
      "so the measured reconstruction noise of each world is used as that world's detection floor (Figure 7). Persistence itself is exact: file, tensors and L0–3 rows bit-identical.",100,4),
      size=7.0,color=INK2,va="top",linespacing=1.2,xmax=.53)
    fig_footer(fig,k,"Engine: 878_result.json (sides.checks, worlds.persistence, panels.gates / A_ref) · host: POST_RUN_VERIFICATION.json · M = MISSING, L = LIVE source cartridge.")
    return save_fig(fig,k,"VERIFICATION RECORD",["878_result.json","POST_RUN_VERIFICATION.json"])
def fig4():
    k="F4";P=panels()
    if not P:return fig_missing(k,"The arms are drawn with the spans of this RUN's transfer panels.","No transfer panel was run in this RUN.")
    w,kind,p=next(((a,b,c) for a,b,c in P if a=="00" and b=="SAME_GOAL"),P[0]);sp=p.get("spans") or {};E,A,C=sp.get("E",[0,0]),sp.get("A",[0,0]),sp.get("C",[0,0])
    fig=fig_base(k,f"Positions of the panel '{ptitle(w,kind)}' of this RUN — the memory is appended once; only WHO MAY READ WHAT differs between the arms","SCHEMATIC")
    segs=[("target memory",0,E[0],"#9CA3AF"),("X2",E[0],A[0],NEU),("A",A[0],A[1],RED),("C",C[0],C[1],COL["M"])];tot=C[1]
    X0,X1=.06,.94;sx=lambda t:X0+(X1-X0)*t/max(tot,1);yb=.79
    for lab,a,b,c in segs:
        rect(fig,sx(a),yb,max(sx(b)-sx(a),.004),.045,c,z=2)
        if sx(b)-sx(a)>.04:Tc(fig,sx(a),sx(b),yb+.0225,f"{lab}  {a}–{b}",size=7.4,weight="bold",color="white")
    T(fig,sx(A[0])-.004,yb+.062,f"A {A[0]}–{A[1]} (2 tok)",size=7.2,weight="bold",color=RED,ha="right")
    T(fig,sx(C[0])+.004,yb+.062,f"C {C[0]}–{C[1]}",size=7.2,weight="bold",color=COL["M"])
    T(fig,X0,yb-.022,f"cache rows of the target after the native append (target's own {(p.get('target') or {}).get('X_len','—')}-token decision input X follows, then the CAR continuation tokens)",size=7.2,color=MUTED,xmax=X1)
    arms=[("FULL",COL["FULL"],"locked native append; native read",{"C rows (recompute L4–79)":"✓✓✓✓","target X":"✓✓✓✓","CAR continuation":"✓✓✓✓"}),
          ("C-BLIND",COL["CB"],"native append; C hidden from the reader",{"C rows (recompute L4–79)":"✓✓✓✓","target X":"✓✓✓✗","CAR continuation":"✓✓✓✗"}),
          ("A-BLIND",COL["AB"],"explicit layers; A hidden while C is recomputed and from the reader",{"C rows (recompute L4–79)":"✓✓✗✓","target X":"✓✓✗✓","CAR continuation":"✓✓✗✓"}),
          ("A-REF",COL["AR"],"same explicit masked kernel as A-BLIND, A made readable again",{"C rows (recompute L4–79)":"✓✓✓✓","target X":"✓✓✓✓","CAR continuation":"✓✓✓✓"})]
    cols_=["memory","X2","A","C"];bw=.215;gap=.015
    for i,(nm,c,sub,M) in enumerate(arms):
        x=.035+i*(bw+gap);y=.395;h=.33;box(fig,x,y,bw,h,ec=c,lw=1.6);rect(fig,x,y+h-.036,bw,.036,c,z=2)
        Tc(fig,x+.004,x+bw-.004,y+h-.018,nm,size=9.6,weight="bold",color="white");Tc(fig,x+.004,x+bw-.004,y+h-.056,sub,size=6.8,color=c)
        cx0=x+.085;cw=(bw-.09)/4
        for j,cn in enumerate(cols_):Tc(fig,cx0+j*cw,cx0+(j+1)*cw,y+h-.088,cn,size=6.8,weight="bold",color=MUTED)
        for r_,(reader,marks) in enumerate(M.items()):
            yy=y+h-.13-r_*.058;T(fig,x+.006,yy+.018,reader,size=6.6,color=INK,xmax=cx0-.003)
            for j,mk in enumerate(marks):_cell(fig,cx0+j*cw+.001,yy,cw-.002,.036,mk=="✓",mk,size=8)
        Tc(fig,x+.004,x+bw-.004,y+.02,"→ "+{"FULL":"outcome + action visible","C-BLIND":"outcome invisible: M and L must coincide","A-BLIND":"action invisible everywhere downstream","A-REF":"reference for A-BLIND (kernel-matched)"}[nm],size=6.7,weight="bold",color=c)
    box(fig,.035,.095,.93,.27,ec=NEU,fc=PANEL,lw=1.2)
    T(fig,.045,.345,"How the arms answer the question — and what each comparison isolates",size=9.0,weight="bold",xmax=.95)
    lines=[("Outcome transfer:","T = margins(FULL with the MISSING cartridge) − margins(FULL with the LIVE cartridge). Same context, same action, different real outcome."),
           ("Leak control:","C-BLIND hides the outcome rows; because M and L cartridges differ ONLY in C, C-BLIND-M must equal C-BLIND-L exactly (Figure 3) — no other row carries the outcome."),
           ("Action information:","A-BLIND hides the executed action from the C rows while layers 4–79 are recomputed AND from the reader; A-REF runs the very same masked kernel with A visible."),
           ("Path matching:","A-REF − A-BLIND is the effect of the action information; FULL − A-REF measures the kernel's numerical noise K (Figure 7). Rows are never deleted: positions and RoPE stay identical."),
           ("Native reading:","CAR = log p of ADVANCE · ACQUIRE · REJECT · BACKTRACK · ACCEPT · STOP (first token + teacher-forced continuation); decision = argmax; abstain if their total p < 0.5.")]
    for j,(a,b) in enumerate(lines):
        y=.31-j*.042;T(fig,.045,y,a,size=7.6,weight="bold",color=COL["FULL"],xmax=.2);T(fig,.185,y,b,size=7.3,color=INK,xmax=.958)
    fig_footer(fig,k,"Spans: 878_result.json panels.spans of this RUN · masks: 2-D key masks given to the model's own causal-mask builder (no row removed, no position changed).")
    return save_fig(fig,k,"SCHEMATIC",["878_result.json panels.spans","878.py (panel878, xappend878, xcar878)"])
ARMS_SHOW=[("BASE","no experience"),("FULL_M","+ MISSING experience"),("FULL_L","+ LIVE experience"),("C_BLIND_M","outcome hidden (M = L)"),
           ("A_REF_M","A-REF · MISSING"),("A_REF_L","A-REF · LIVE"),("A_BLIND_M","A-BLIND · MISSING"),("A_BLIND_L","A-BLIND · LIVE")]
def fig5():
    k="F5";P=panels()
    if not P:return fig_missing(k,"The decisions are the native CAR readings of this RUN's transfer panels.","No transfer panel was run in this RUN.")
    fig=fig_base(k,"Probabilities of the six action words (normalised over the six) read from the frozen model — the decision is the model's own argmax; nothing is executed","LIVE MEASUREMENT")
    for i,(w,kind,p) in enumerate(P[:4]):
        x=.035+(i%2)*.475;y=.535-(i//2)*.39;wd=.31;ht=.265;A_=p.get("arms") or {}
        rows=[(a,lab) for a,lab in ARMS_SHOW if a in A_];M=np.array([[float((A_[a].get("p") or {}).get(wd_,0)) for wd_ in WORDS] for a,_ in rows])
        T(fig,x,y+ht+.05,ptitle(w,kind),size=8.6,weight="bold",color=INK,xmax=x+.46)
        T(fig,x,y+ht+.024,f"status: {p.get('status')}",size=7.4,weight="bold",color=_status_col(p.get("status")),xmax=x+.46)
        ax=fig.add_axes([x+.11,y,wd-.06,ht]);ax.imshow(M,cmap="Purples",vmin=0,vmax=1,aspect="auto")
        ax.set_xticks(range(len(WORDS)));ax.set_xticklabels([ABBR[x_] for x_ in WORDS],fontsize=6.8);ax.set_yticks(range(len(rows)));ax.set_yticklabels([lab for _,lab in rows],fontsize=6.6)
        for r_ in range(len(rows)):
            for c_ in range(len(WORDS)):ax.text(c_,r_,f"{M[r_,c_]:.2f}",ha="center",va="center",fontsize=5.8,color="white" if M[r_,c_]>.55 else INK)
        _axstyle(ax,6.6);ax.tick_params(length=0)
        for r_,(a,_) in enumerate(rows):
            act=A_[a].get("action");lab="abstains" if act=="INVALID" else act
            ax.text(len(WORDS)-.35,r_,f" → {lab}",va="center",ha="left",fontsize=6.6,weight="bold",color=(AMBER if act=="INVALID" else INK),clip_on=False)
    T(fig,.035,.088,"'abstains' = the six action words together keep < 50 % of the model's probability (pre-registered reader rule); the row still shows the model's own relative preferences.",size=7.0,color=INK2,xmax=.965)
    fig_footer(fig,k,"Values: 878_result.json panels.arms (reading867 normalised probabilities and native action) of this RUN · BASE_EXPLICIT omitted here (identical to BASE, Figure 3).")
    return save_fig(fig,k,"LIVE MEASUREMENT",["878_result.json panels.arms"])
def fig6():
    k="F6";P=panels()
    if not P:return fig_missing(k,"The contrasts are computed by the engine from this RUN's native CAR readings.","No transfer panel was run in this RUN.")
    fig=fig_base(k,"T = margin(MISSING experience) − margin(LIVE experience) for all 15 action pairs (sequence log p) · the source row is the same contrast in the source's own decision state","LIVE MEASUREMENT")
    labs=[f"{ABBR[a]}−{ABBR[b]}" for a,b in PAIRS];act=set(next(iter(worlds().values()),{}).get("source",{}).get("action_pairs") or [i for i,(a,b) in enumerate(PAIRS) if "ACQUIRE" in (a,b)])
    for i,(w,kind,p) in enumerate(P[:4]):
        x=.075+(i%2)*.47;y=.565-(i//2)*.405;wd=.32;ht=.215;C_=p.get("contrast") or {};src=((worlds().get(w) or {}).get("source") or {}).get("contrast") or {}
        rows=[("source (own X3)",src.get("seq"))]+[(nm,(C_.get(key) or {}).get("seq")) for nm,key in (("FULL","FULL"),("A-REF","A_REF"),("A-BLIND","A_BLIND"),("C-BLIND","C_BLIND"))]
        rows=[(a,b) for a,b in rows if b];M=np.array([b for _,b in rows],float);vm=max(1e-6,float(np.nanmax(np.abs(M[1:]))) if len(M)>1 else 1.0)
        T(fig,x,y+ht+.025,ptitle(w,kind),size=8.4,weight="bold",xmax=x+.45)
        ax=fig.add_axes([x+.06,y,wd,ht]);ax.imshow(M,cmap="RdBu_r",norm=TwoSlopeNorm(vcenter=0,vmin=-vm,vmax=vm),aspect="auto")
        ax.set_yticks(range(len(rows)));ax.set_yticklabels([a for a,_ in rows],fontsize=6.6);ax.set_xticks(range(15));ax.set_xticklabels(labs,fontsize=5.4,rotation=90)
        for t in ax.get_xticklabels():
            if labs.index(t.get_text()) in act:t.set_color(RED);t.set_fontweight("bold")
        for r_ in range(len(rows)):
            for c_ in range(15):
                v=M[r_,c_];ax.text(c_,r_,("0" if v==0 else f"{v:.1f}"),ha="center",va="center",fontsize=4.9,color="white" if abs(v)>.6*vm else INK)
        _axstyle(ax,6.4);ax.tick_params(length=0)
        for r_,(a,b) in enumerate(rows):ax.text(15.0,r_,f" ‖·‖ {np.linalg.norm(b):.2f}",va="center",fontsize=6.0,color=INK2,clip_on=False)
    T(fig,.035,.088,"Red labels = the 5 pairs containing the executed ACQUIRE · colour scale per panel (source row may saturate; numbers printed) · C-BLIND row exactly 0 = no outcome information outside the C rows.",size=7.0,color=INK2,xmax=.965)
    fig_footer(fig,k,"Values: 878_result.json worlds.source.contrast and panels.contrast (sequence log-probability margins) of this RUN. First-token contrasts are in the same file.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["878_result.json panels.contrast","878_result.json worlds.source.contrast"])
def fig7():
    k="F7";P=panels()
    if not P:return fig_missing(k,"The decision rule is applied to this RUN's transfer panels.","No transfer panel was run in this RUN.")
    fig=fig_base(k,"Fixed before the model was loaded (pre-registration hash in the log) — applied mechanically by the engine, re-drawn here from its records","VERIFICATION RECORD")
    ax=fig.add_axes([.15,.17,.42,.6]);names=[("‖T_FULL‖ outcome contrast",COL["FULL"]),("floor (reconstruction noise)",MUTED),("K = ‖T_FULL − T_A-REF‖ kernel",AMBER),
                                                ("‖T_A-REF − T_A-BLIND‖ action info",COL["AB"]),("threshold max(floor, K)",INK)]
    ys=[];labs=[]
    for i,(w,kind,p) in enumerate(P):
        a=p.get("A_ref") or {};fl=float(((worlds().get(w) or {}).get("floor") or {}).get("seq") or 0)
        vals=[float((p.get("signature",{}).get("FULL",{}).get("seq") or {}).get("norm_all15") or a.get("norm_T_full_seq") or 0),fl,a.get("K_full_minus_ref_seq"),a.get("norm_ref_minus_blind_seq"),a.get("threshold_max_floor_K")]
        base=i*6.4
        for j,((nm,c),v) in enumerate(zip(names,vals)):
            yy=base+j
            if v is None:ax.text(1.2e-6,yy,"not computed",fontsize=6,va="center",color=MUTED);continue
            ax.barh(yy,max(float(v),1e-6),color=c,height=.8);ax.text(max(float(v),1e-6)*1.15,yy,f"{float(v):.5g}",va="center",fontsize=6.2)
        ys.append(base+2);labs.append(f"W{w} {'same-goal' if kind=='SAME_GOAL' else 'cross-world'}\n"+{"ACTION_INFORMATION_DEPENDENT_TRANSFER":"action-info dependent","OUTCOME_TRANSFER_ONLY":"outcome only","NO_TRANSFER":"no transfer","TRANSFER_A_BLIND_INVALID":"A-arms invalid"}.get(p.get("status"),str(p.get("status"))))
    ax.set_xscale("log");ax.set_xlim(1e-6,500);ax.set_yticks(ys);ax.set_yticklabels(labs,fontsize=6.6);ax.invert_yaxis();_axstyle(ax,6.6)
    for t,(w,kind,p) in zip(ax.get_yticklabels(),P):t.set_color(_status_col(p.get("status")))
    ax.set_xlabel("norm over the 15 sequence-log-p margins (log scale)",fontsize=7.6)
    for j,(nm,c) in enumerate(names):T(fig,.035+(j%3)*.19,.85-(j//3)*.025,"■ "+nm,size=6.8,color=c,xmax=.035+(j%3+1)*.19-.004)
    box(fig,.60,.10,.365,.75,ec=NEU,lw=1.3);T(fig,.61,.83,"The rule (per panel, sequence margins)",size=9.0,weight="bold",xmax=.96)
    rule=[("1","outcome transfer","‖T_FULL‖ > floor, else NO_TRANSFER"),("2","A-REF usable","‖T_A-REF‖ > floor, dot(T_FULL, T_A-REF) > 0, K < ‖T_FULL‖ — else TRANSFER_A_BLIND_INVALID"),
          ("3","action information","‖T_A-REF − T_A-BLIND‖ > max(floor, K) → ACTION_INFORMATION_DEPENDENT_TRANSFER; else OUTCOME_TRANSFER_ONLY"),
          ("4","technical gates","Figure 3 gates; any failure → TECHNICAL_BLOCK; non-finite number → TECHNICAL_BLOCK")]
    y=.79
    for n_,a,b in rule:
        T(fig,.61,y,n_+" · "+a,size=7.6,weight="bold",color=COL["FULL"],xmax=.96);y-=.026
        T(fig,.62,y,wrap(b,58),size=6.9,color=INK,va="top",linespacing=1.18,xmax=.96);y-=.026*(1+wrap(b,58).count("\n"))+.012
    hw=next(((w,kind,p) for w,kind,p in P if w=="00" and kind=="SAME_GOAL"),None)
    if hw:
        a=hw[2].get("A_ref") or {};T(fig,.61,y-.01,"Highlighted: World 00 · same-goal state",size=8.0,weight="bold",color=OK_COL,xmax=.96);y-=.036
        for lab,v in (("‖T_FULL‖",a.get("norm_T_full_seq")),("‖T_A-REF − T_A-BLIND‖",a.get("norm_ref_minus_blind_seq")),("threshold max(floor, K)",a.get("threshold_max_floor_K")),("K (kernel)",a.get("K_full_minus_ref_seq"))):
            T(fig,.62,y,lab,size=7.4,color=INK2,xmax=.82);T(fig,.955,y,f"{v:.5g}" if v is not None else "—",size=7.6,weight="bold",ha="right",mono=True);y-=.026
        if a.get("norm_ref_minus_blind_seq") and a.get("K_full_minus_ref_seq"):
            T(fig,.62,y-.004,f"action effect = {a['norm_ref_minus_blind_seq']/max(a['K_full_minus_ref_seq'],1e-30):,.0f} × the kernel difference",size=7.2,color=OK_COL,xmax=.96);y-=.03
    T(fig,.61,max(y-.02,.13),wrap("A change of decision driven by stored experience — not a test of whether the lesson is correct, and not credit assignment (ACTION_CREDIT_NOT_ESTABLISHED).",64,3),
      size=6.8,color=AMBER,va="top",linespacing=1.15,xmax=.96)
    fig_footer(fig,k,"Values: 878_result.json worlds.floor, panels.A_ref, panels.signature, panels.status · rule text = PREREG878 panel_rule (pre-registration hash printed in the log).")
    return save_fig(fig,k,"VERIFICATION RECORD",["878_result.json panels.A_ref","878_prereg.json"])
def fig8():
    k="F8";L=LEDGER.get("TEST878")
    if not L or not L.get("end_t"):return fig_missing(k,"The timeline is drawn from the engine process of this RUN.","The engine process did not run in this RUN.")
    fig=fig_base(k,"GPU memory (nvidia-smi every 10 s) and the engine milestones as they arrived — one OS process, model loaded once, GPU empty after exit","LIVE MEASUREMENT")
    t0=L["start_t"];S=[s for s in GPU_SAMPLES if s.get("used_mib") is not None];ax=fig.add_axes([.065,.47,.60,.35])
    ph=[("engine start → model loaded",t0,(MILESTONES.get("G1_PREFLIGHT") or {}).get("t"),"#E5E7EB"),
        ("replay · capture · write · free",(MILESTONES.get("G1_PREFLIGHT") or {}).get("t"),(MILESTONES.get("TARGET_00_FORK") or MILESTONES.get("SOURCE_00_LIVE") or {}).get("t"),"#FDE7D7"),
        ("reload · append · native CAR panels",(MILESTONES.get("TARGET_00_FORK") or MILESTONES.get("SOURCE_00_LIVE") or {}).get("t"),(MILESTONES.get("WORLD_00") or {}).get("t"),"#EDE9FE"),
        ("records",(MILESTONES.get("WORLD_00") or {}).get("t"),L["end_t"],"#D1FAE5")]
    for lab,a,b,c in ph:
        if a and b and b>a:ax.axvspan((a-t0)/60,(b-t0)/60,color=c,lw=0)
    if S:ax.plot([(s["t"]-t0)/60 for s in S],[s["used_mib"]/1024 for s in S],color=INK,lw=1.2)
    span=max((L["end_t"]-t0)/60*1.02,1);lastx=-1e9
    for k_ in ("G1_PREFLIGHT","SOURCE_01_MISSING","SOURCE_00_LIVE","WORLD_01","WORLD_00"):
        if k_ not in MILESTONES:continue
        xm=(MILESTONES[k_]["t"]-t0)/60;ax.axvline(xm,color=MUTED,lw=.7,ls=":")
        if xm-lastx>.035*span:ax.text(xm,80.5,k_.replace("_"," ").lower(),rotation=90,fontsize=5.6,color=MUTED,va="top",ha="right");lastx=xm
    ax.plot([(L["end_t"]-t0)/60],[((L.get("gpu_release") or {}).get("used_mib") or 0)/1024],marker="v",color=OK_COL,ms=7)
    ax.set_ylim(0,82);ax.set_xlim(0,max((L["end_t"]-t0)/60*1.02,1));ax.set_ylabel("GPU memory used (GiB)",fontsize=8);ax.set_xlabel("minutes since the engine process started",fontsize=8);_axstyle(ax,7.5)
    for j,(lab,a,b,c) in enumerate(ph):rect(fig,.065+j*.15,.835,.012,.018,c,ec=NEU,lw=.5,z=2);T(fig,.08+j*.15,.844,lab,size=6.6,color=INK2,xmax=.065+(j+1)*.15-.004)
    hd=["milestone (engine line)","min","note"];T(fig,.065,.40,hd[0],size=7.2,weight="bold",color=MUTED);T(fig,.30,.40,hd[1],size=7.2,weight="bold",color=MUTED);T(fig,.345,.40,hd[2],size=7.2,weight="bold",color=MUTED)
    keys=[k_ for k_ in ("ENGINE_LOADED","G0_SOURCE","G1_PREFLIGHT","SOURCE_01_MISSING","SOURCE_01_LIVE","SOURCE_00_MISSING","SOURCE_00_LIVE","TARGET_01_FORK","TARGET_00_FORK","WORLD_01","WORLD_00","STATUS") if k_ in MILESTONES]
    for j,k_ in enumerate(keys):
        m=MILESTONES[k_];y=.375-j*.0235;T(fig,.065,y,k_.replace("_"," ").lower(),size=6.7,mono=True,xmax=.295);T(fig,.30,y,f"{(m['t']-t0)/60:5.1f}",size=6.7,mono=True)
        T(fig,.345,y,short(STEP_NOTE.get(k_,""),70),size=6.6,color=INK2,xmax=.665)
    box(fig,.69,.10,.275,.75,ec=NEU,lw=1.3);T(fig,.70,.83,"Process and resources",size=9.0,weight="bold",xmax=.96)
    g1=(MILESTONES.get("G1_PREFLIGHT") or {}).get("line","");ml=re.search(r"model_load_s=(\d+)",g1);st=(MILESTONES.get("STATUS") or {}).get("line","")
    rows=[("OS process",f"pid {L.get('engine_pid')} · exit {L.get('exit_code')}"),("command","python -u 878.py (locked file)"),("start → end (UTC)",f"{str(L.get('start',''))[11:19]} → {str(L.get('end',''))[11:19]}"),
          ("process time",f"{L.get('seconds',0)/60:.1f} min"),("model load (engine)",f"{int(ml.group(1))/60:.1f} min" if ml else "—"),
          ("panels W01 · W00",f"{(worlds().get('01') or {}).get('elapsed_s','—')} s · {(worlds().get('00') or {}).get('elapsed_s','—')} s"),
          ("CAR reads W01 · W00",f"{(worlds().get('01') or {}).get('reads','—')} · {(worlds().get('00') or {}).get('reads','—')}"),
          ("torch peak (engine)",f"{max([float(W_.get('peak_gib') or 0) for W_ in worlds().values()]+[0]):.2f} GiB"),("nvidia-smi peak",f"{(L.get('gpu_peak_used_mib') or 0)/1024:.1f} GiB"),
          ("GPU after exit",f"{(L.get('gpu_release') or {}).get('used_mib','—')} MiB · released {okm((L.get('gpu_release') or {}).get('released'))}"),
          ("engine status line",short(st,60) or "—"),("cartridges on SSD",f"{len(exps())} files · {fmt_b(sum(int(e.get('bytes') or 0) for e in exps().values()))}")]
    for j,(a,b) in enumerate(rows):
        y=.79-j*.054;T(fig,.70,y,a,size=7.3,weight="bold",color=MUTED,xmax=.96);T(fig,.70,y-.023,b,size=7.2,color=INK,xmax=.96,mono=(a in ("command","engine status line")))
    fig_footer(fig,k,"Host: PROCESS_LEDGER.json, GPU_SAMPLES.json, ENGINE_MILESTONES.json (receipt time of each engine line) · engine: 878_result.json worlds.elapsed_s / reads / peak_gib.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["PROCESS_LEDGER.json","GPU_SAMPLES.json","ENGINE_MILESTONES.json","878_result.json"])
def claims():
    res=R();v=res.get("verdict") or {};Vv=LIVE.get("verification") or {};P=panels();Wd=worlds()
    pers=[r for W_ in Wd.values() for r in (W_.get("persistence") or {}).values()]
    est=[("real action–outcome experiences written as physical Experience-CUT3 files (H3 + K/V L0–3)",bool(exps()) and all((Vv.get("cartridges") or {}).get(e,{}).get("file_sha_ok") for e in exps())),
         ("source working state freed; files reloaded from SSD with file + tensor SHA-256",bool(pers) and all(r.get("reloaded_sha_ok") for r in pers)),
         ("reconstruction: L0–3 rows bit-identical, same native action",bool(pers) and all(r.get("lower_rows_bitwise") and r.get("action_same") for r in pers)),
         ("cartridges change the native CAR of INDEPENDENT same-goal states (both worlds)",all(((Wd.get(w) or {}).get("panels",{}).get("SAME_GOAL",{}).get("detect") or {}).get("outcome_seq") for w in ("01","00")) if Wd else None),
         ("the change is outcome-specific: outcome rows hidden → MISSING = LIVE exactly",bool(P) and all((p.get("gates") or {}).get("C_BLIND_M_equals_L") for _,_,p in P)),
         ("hiding the executed action changes the outcome contrast beyond kernel noise",v.get("verdict")=="ACTION_INFORMATION_DEPENDENT_TRANSFER"),
         ("frozen weights, no hooks, executed bytes = locked 878.py, engine blocks = []",(Vv.get("engine") or {}).get("executed_equals_locked_file") and not v.get("blocks"))]
    notyet=["action–credit assignment (ACTION_CREDIT_NOT_ESTABLISHED: A-dependence is not credit)","autonomous selection of which experience to recall (here: mounted by the experiment)",
            "judging whether an outcome was good or bad; correctness of the changed decision","behaviour correction over time; closed-loop learning; generalisation beyond 2 event pairs",
            *(["A-BLIND is a strong intervention: the reader abstained (mass < 0.5) in every A-BLIND arm — the action effect includes context disruption"] if any((p.get("arms") or {}).get(a,{}).get("action")=="INVALID" for _,_,p in P for a in ("A_BLIND_M","A_BLIND_L")) else []),
            f"cross-world generalisation: {v.get('cross_world_class')} ({', '.join(f'W{w} {s}' for w,s in (v.get('cross_world') or {}).items())})"]
    return est,notyet,v
def fig9():
    k="F9";res=R()
    if not res:return fig_missing(k,"The claims are decided from this RUN's records.","The engine did not write its result file in this RUN.")
    est,notyet,v=claims()
    fig=fig_base(k,"Decided only from this RUN's records — what the experiment establishes, and what it deliberately does not claim","VERIFICATION RECORD")
    box(fig,.035,.35,.555,.51,ec=OK_COL,lw=1.6);rect(fig,.035,.86-.04,.555,.04,OK_COL,z=2);T(fig,.045,.84,"ESTABLISHED IN THIS RUN",size=9.6,weight="bold",color="white",xmax=.58)
    for j,(t,ok) in enumerate(est):
        y=.79-j*.062;T(fig,.045,y,okm(ok),size=10,weight="bold",color=OK_COL if ok else RED);T(fig,.07,y,wrap(t,104,2),size=7.6,color=INK,va="center",linespacing=1.15,xmax=.585)
    box(fig,.61,.35,.355,.51,ec=AMBER,lw=1.6);rect(fig,.61,.86-.04,.355,.04,AMBER,z=2);T(fig,.62,.84,"NOT CLAIMED · NEXT STEPS",size=9.6,weight="bold",color="white",xmax=.96)
    for j,t in enumerate(notyet):
        y=.79-j*(.072 if len(notyet)>5 else .085);T(fig,.62,y,"•",size=9,weight="bold",color=AMBER);T(fig,.635,y,wrap(t,52,3),size=7.3,color=INK,va="center",linespacing=1.15,xmax=.962)
    box(fig,.035,.095,.93,.225,ec=COL["FULL"],lw=1.5)
    T(fig,.045,.297,f"VERDICT  {v.get('verdict')}   ·   scope {v.get('scope')}   ·   blocks {v.get('blocks')}",size=10,weight="bold",color=COL["FULL"],xmax=.955)
    T(fig,.045,.265,f"same-goal: {', '.join(f'W{w} {s}' for w,s in (v.get('same_goal') or {}).items())}",size=7.6,color=INK,xmax=.955)
    T(fig,.045,.24,f"cross-world: {', '.join(f'W{w} {s}' for w,s in (v.get('cross_world') or {}).items())} → {v.get('cross_world_class')}",size=7.6,color=INK,xmax=.955)
    T(fig,.045,.21,"Research direction: persistent experience transfer (this run, pilot) → autonomous experience selection → action-credit assignment → experience-guided correction → closed loop",size=7.4,color=INK2,xmax=.955)
    T(fig,.045,.178,f"878.py {ENGINE_BLOB} · engine {ENGINE_FACTS['engine']} {ENGINE_FACTS['engine_commit']} ({ENGINE_FACTS['engine_blob'][:12]}…) · pre-registration {str(res.get('prereg_sha256',''))[:16]}…",size=6.8,color=MUTED,mono=True,xmax=.955)
    T(fig,.045,.153,f"locked trace records sha256 {ENGINE_FACTS['records_sha256'][:32]}… · result file sha256 {str((LIVE.get('verification') or {}).get('result_sha256',''))[:24]}…",size=6.8,color=MUTED,mono=True,xmax=.955)
    T(fig,.045,.125,f"code {URL_CODE} · reference GPU log {URL_LOG}",size=6.8,color=MUTED,mono=True,xmax=.955)
    fig_footer(fig,k,"Every ✓ is computed from 878_result.json and the host's re-verification of this RUN; a missing record is drawn ✗. Two real event pairs: a pilot, not a statistic.")
    return save_fig(fig,k,"VERIFICATION RECORD",["878_result.json","POST_RUN_VERIFICATION.json"])
FIG_FUNCS=OrderedDict([("F1",fig1),("F2",fig2),("F3",fig3),("F4",fig4),("F5",fig5),("F6",fig6),("F7",fig7),("F8",fig8),("F9",fig9)])
def render_figures():
    errs={};FIGURES.clear();FIGURES.update(BASE_FIGURES)
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
    errs=render_figures();n=len([k for k in FIG_FILES if k in BASE_FIGURES])
    qcf=[k for k,v in FIG_FILES.items() if not (v.get("layout_qc") or {}).get("passed") or not (v.get("jpeg_qc") or {}).get("passed")]
    np_=[k for k,v in FIG_FILES.items() if v["badge"]=="NOT PRODUCED IN THIS RUN"]
    note=f"{n}/{len(BASE_FIGURES)} JPEG figures written (300 dpi)"
    if errs or qcf or np_:raise RuntimeError(note+(f" · NOT GENERATED: {errs}" if errs else "")+(f" · LAYOUT/JPEG QC FAILED: {', '.join(qcf)}" if qcf else "")+(f" · drawn as NOT PRODUCED: {', '.join(np_)}" if np_ else ""))
    return note+" · layout QC and JPEG QC passed for every figure"
_AKB878_PARTS.add(2)
# ===== END OF PART 2/3 =====
# ===== PART 3/3 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 3 — records, the RUN pipeline and the Gradio interface (SH782 design, unchanged); it starts the program.
# =====================================================================================================================
# ---------------------------------------------------------------------------------------------------------------------
# records: run summary, SHA-256 manifest, direct downloads (no ZIP)
# ---------------------------------------------------------------------------------------------------------------------
def run_verdict():
    st=STATE["stages"];bad=[k for k,v in st.items() if v["status"] in("fail","skip")]
    if STATE.get("running"):return "RUNNING"
    if not STATE.get("finished"):return "NOT STARTED"
    if not bad:return "COMPLETE — every stage ran and passed"
    return "INCOMPLETE — not a completed live experiment: "+", ".join(f"{k} {st[k]['status'].upper()}" for k in bad)
def write_run_summary():
    L=[];a=L.append;res=R();v=res.get("verdict") or {}
    a(f"{APP_NAME} — {APP_SUB}\n{EXPERIMENT} live demonstration · demo {CODE_VERSION} · RUN {SESSION_ID} · written {local_now()}")
    if SIM:a("SIMULATION — NOTHING IN THIS FILE IS AN EXPERIMENTAL RESULT")
    a(f"RUN VERDICT {run_verdict()}\nengine: 878.py git blob {LOCKS[ENGINE_NAME]} executed unchanged as one OS process · engine records {ENG.get('root')}")
    a("\nSTAGES (times = this RUN)")
    for key,title in STAGES.items():
        s=STATE["stages"][key];a(f"  [{s['status'].upper():<4}] {key:<10} {('%.0f s'%s['seconds']) if s['seconds'] is not None else '':>8}  {title}\n             {s['note']}")
    a("\nPROCESS LEDGER")
    for s,x in LEDGER.items():a(f"  {SNAME[s]:<8} pid {x.get('engine_pid')} {x.get('start')} → {x.get('end')} exit {x.get('exit_code')} status {x.get('status')} GPU after {(x.get('gpu_release') or {}).get('used_mib')} MiB")
    if res:
        a(f"\nTEST878 VERDICT {v.get('verdict')} · scope {v.get('scope')} · blocks {v.get('blocks')}")
        a(f"  same-goal {v.get('same_goal')} · cross-world {v.get('cross_world')} ({v.get('cross_world_class')})")
        a(f"  {v.get('credit')}")
        for w,kind,p in panels():
            ar=p.get("A_ref") or {};a(f"  PANEL W{w} {kind:<11} {p.get('status')} · ‖T_FULL‖ {ar.get('norm_T_full_seq')} · ‖T_A-REF − T_A-BLIND‖ {ar.get('norm_ref_minus_blind_seq')} · "
                                        f"threshold {ar.get('threshold_max_floor_K')} · K {ar.get('K_full_minus_ref_seq')}")
            for arm,x in (p.get("arms") or {}).items():a(f"      {arm:<14} {x.get('action'):<10} "+" ".join(f"{w_}={float((x.get('p') or {}).get(w_,0)):.4f}" for w_ in WORDS))
        try:
            est,notyet,_=claims();a("\nESTABLISHED IN THIS RUN");[a(f"  {okm(ok)} {t}") for t,ok in est];a("NOT CLAIMED");[a(f"  • {t}") for t in notyet]
        except Exception:pass
    a(f"\n{AUTHOR} · {ORG} · {LICENSE_NAME} · {COPYRIGHT} · {URL_LICENSE}")
    RUN_SUMMARY.write_text("\n".join(L)+"\n",encoding="utf-8");_private(RUN_SUMMARY)
def engine_files():
    out=[];r=ENG.get("root")
    if r and Path(r).is_dir():
        for n in ("878_result.json","878_prereg.json","878_experience_manifest.json","878_checkpoint_01.json","878_checkpoint_00.json","878_engine.log","878_events.jsonl","TEST878.py","878_traceback.txt"):
            if (Path(r)/n).is_file():out.append(Path(r)/n)
        out+=sorted(Path(r).glob("878_*_traceback.txt"))
    for k in ("console","zip"):
        if ENG.get(k) and Path(ENG[k]).is_file():out.append(Path(ENG[k]))
    return out
def download_items():
    items=[("Run summary",RUN_SUMMARY),("Engine output, real-time (UTC receipt · session · stream · line)",ENGINE_OUT),("Session log",SESSION_LOG),("Session events (JSONL)",SESSION_EVENTS),
           ("Process ledger",DATA_DIR/"PROCESS_LEDGER.json"),("GPU samples",DATA_DIR/"GPU_SAMPLES.json"),("Engine milestones",DATA_DIR/"ENGINE_MILESTONES.json"),
           ("Post-run verification",VERIFY_FILE),("Cartridge anatomy (heat-map data)",DATA_DIR/"CARTRIDGE_ANATOMY.npz"),
           ("Stage record",DATA_DIR/"STAGES.json"),("Engine gates of this RUN",DATA_DIR/"ENGINE_CHECKS.json"),("Figure manifest",SESSION_DIR/"FIGURES_MANIFEST.json"),("SHA-256 manifest",MANIFEST),
           ("878.py (locked, executed)",EVID_DIR/ENGINE_NAME)]
    out=[(l,str(p)) for l,p in items if Path(p).is_file()]
    out+=[(f"engine file · {p.name}",str(p)) for p in engine_files()]
    return out
def package_session():
    dump_json(DATA_DIR/"ENGINE_CHECKS.json",CHECKS);dump_json(DATA_DIR/"STAGES.json",dict(verdict=run_verdict(),stages=STATE["stages"],session=SESSION_ID))
    dump_json(DATA_DIR/"PROCESS_LEDGER.json",LEDGER);dump_json(DATA_DIR/"GPU_SAMPLES.json",GPU_SAMPLES);dump_json(DATA_DIR/"ENGINE_MILESTONES.json",MILESTONES)
    write_run_summary()
    files=[p for p in sorted(SESSION_DIR.rglob("*")) if p.is_file() and p!=MANIFEST and p.suffix!=".tmp"]+engine_files()
    ed=ENG.get("exp_dir");files+=sorted(Path(ed).glob("*.pt")) if ed and Path(ed).is_dir() else []
    man=OrderedDict((str(p),dict(sha256=sha_file(p),bytes=p.stat().st_size)) for p in files)
    dump_json(MANIFEST,dict(session=SESSION_ID,utc=utc_now(),simulation=SIM,note="SHA-256 of every file of this RUN (cartridge .pt files hashed, not offered for download — 12 MB each). No ZIP.",files=man))
    return str(MANIFEST)
def stage_records():
    package_session();return f"{len(FIG_FILES)} JPEG figures + {len(download_items())} records, each downloadable directly · SHA-256 manifest of {len(json.load(open(MANIFEST))['files'])} files (no ZIP)"

# ---------------------------------------------------------------------------------------------------------------------
# THE RUN PIPELINE (one button)
# ---------------------------------------------------------------------------------------------------------------------
RUNS_DONE=[]
def run_pipeline():
    if RUNS_DONE:_session_paths(datetime.now().astimezone().strftime("SH878-%Y%m%d-%H%M%S")+f"-RUN{len(RUNS_DONE)+1}")
    RUNS_DONE.append(SESSION_ID);LIVE.clear();LIVE.update(session=SESSION_ID);LINES.clear();CHECKS.clear();FIG_FILES.clear();FIG_ERRORS.clear();PROVENANCE.clear()
    LEDGER.clear();GPU_SAMPLES.clear();MILESTONES.clear();ENG.update(root=None,exp_dir=None,console=None,zip=None,start_t=None)
    STATE.update(running=True,started=utc_now(),finished=None,current=None,elapsed=None);STATE["fig_version"]+=1
    for k in STAGES:STATE["stages"][k]=dict(status="wait",seconds=None,note="",t0=None)
    banner(f"RUN {SESSION_ID} · {local_now()} · one engine process (878.py, unchanged) — about 25–35 minutes on an A100, model download excluded")
    def step(key,fn):
        STATE["current"]=key;stage_set(key,"run");_emit(f"── [{list(STAGES).index(key)+1}/{len(STAGES)}] {STAGES[key]}")
        try:
            note=fn();stage_set(key,"done",note);slog("STAGE_DONE",key,note=note);return True
        except Exception as ex:
            stage_set(key,"fail",f"{type(ex).__name__}: {ex}");slog("STAGE_FAILED",key,error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc()[-3000:]);return False
    try:
        ok=step("PRECHECK",stage_precheck)
        if ok:ok=step("TEST878",lambda:stage_session("TEST878"))
        else:stage_set("TEST878","skip","not run — the pre-check did not pass")
        if R():step("VERIFY",stage_verify)
        else:stage_set("VERIFY","skip","no engine result file in this RUN")
        step("FIGURES",stage_figures);step("RECORDS",stage_records)
    finally:
        STATE.update(running=False,finished=utc_now(),current=None);bump()
        try:package_session()
        except Exception:pass
        banner(f"RUN VERDICT: {run_verdict()}\nTEST878 VERDICT: {(R().get('verdict') or {}).get('verdict')}\nRUN {SESSION_ID} finished {local_now()} · "+" · ".join(f"{k}:{v['status']}" for k,v in STATE["stages"].items()))
RUN_THREAD={"t":None}
def start_run():
    t=RUN_THREAD["t"]
    if t is not None and t.is_alive():return False
    RUN_THREAD["t"]=threading.Thread(target=run_pipeline,daemon=True,name="SH878-RUN");RUN_THREAD["t"].start();return True
# =====================================================================================================================
# Gradio interface (Silicon Hippocampus 1.5 / SH745 design): ONE button (RUN). The stages, the engine's own output, the
# cartridges, the panels and the figures appear while they are produced. The page refreshes itself with short requests
# (gr.Timer) — a dropped connection never hides the figures; a reload shows all.
# =====================================================================================================================
LINEAGE=[("Research Record I — Qwen2.5-7B","https://doi.org/10.5281/zenodo.23381336"),
         ("Research Record II — Mistral-7B, Silicon Hippocampus v1.4","https://doi.org/10.5281/zenodo.23418927"),
         ("Research Record III — Qwen2.5-72B, Direct Internal-State Injection","https://doi.org/10.5281/zenodo.23434686")]
def esc(x):return html.escape(str(x))
def card(title,body,kind="info"):return f'<div class="kz card {kind}"><div class="h">{esc(title)}</div><div class="small">{body}</div></div>'
def ok_mark(v):return "<b style='color:#08785B'>PASS</b>" if v else ("<b style='color:#B91C1C'>FAIL</b>" if v is False else "<span style='opacity:.6'>—</span>")
class Markup(str):pass
def tbl(rows,head=None,mono_cols=()):
    h="".join(f"<th>{esc(x)}</th>" for x in head) if head else ""
    b="".join("<tr>"+"".join(f"<td class='{'mono' if i in mono_cols else ''}'>{v if isinstance(v,Markup) else esc(v)}</td>" for i,v in enumerate(r))+"</tr>" for r in rows)
    return f"<table class='tbl'>{('<tr>'+h+'</tr>') if h else ''}{b}</table>"
def pre(text,maxh=420):return f"<div class='ans' style='max-height:{maxh}px'>{esc(text)}</div>"
def details(summary,inner,open_=False):return f"<details{' open' if open_ else ''}><summary>{summary}</summary>{inner}</details>"

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
    tiles=[("[X2][A][C]","real action + outcome → cartridge"),("H3 + K/V L0–3","physical CUT3 file on SSD"),("FREE → RELOAD","SHA-256 file + every tensor"),
           ("INDEPENDENT","target states never saw it"),("NATIVE CAR","the frozen model decides"),("0","weight changes · hooks")]
    return (f'<div class="kz hero"><span class="rec">Live research demonstration · frozen Qwen2.5-72B-Instruct · NF4 · BF16 · CUT3 · A100 80 GB</span>'
            f'<div class="brand">{esc(APP_NAME)}</div><div class="title">{esc(APP_SUB)}</div>'
            '<div class="by">A frozen language model lives through a real decision: it is in a state, it executes an action (ACQUIRE) and a real outcome comes back '
            '(MISSING or LIVE). That experience is written as a physical cartridge made of the model\'s own internal states — the layer-3 output H3 and the key/value tensors '
            'of layers 0–3 — to the SSD, with SHA-256 seals. The source working state is deleted. Later the cartridge is loaded from the SSD and appended to a DIFFERENT '
            'decision state; the frozen model recomputes layers 4–79 on top of it and makes its own native decision. Control arms hide the outcome (C-BLIND) or the action '
            '(A-BLIND, with the kernel-matched A-REF) to show what the decision change depends on. No weights change, no hook, no text replay, and Python never picks an action.</div>'
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
    else:kind,t="info","NOT STARTED — press RUN. The TEST878 engine runs as one process on the A100 (about 25–35 minutes, model load ≈ 21 min); everything it does appears here while it works."
    return card(t,"Every value, table and figure on this page comes from THIS RUN. Reference run of the same file: "
                f"<a href='{URL_LOG}' target='_blank' rel='noopener'>878.log</a> · engine 878.py git blob <span class='mono'>{esc(LOCKS[ENGINE_NAME][:16])}…</span> "
                f"(<a href='{URL_CODE}' target='_blank' rel='noopener'>source</a>).",kind)
def stages_html():
    out=[];n=len(STAGES);done=0
    for i,(k,title) in enumerate(STAGES.items(),1):
        s=STATE["stages"][k];stt=s["status"];mk={"done":"✓","run":"▶","fail":"✗","skip":"–","wait":"○"}[stt]
        if stt in("done","skip","fail"):done+=1
        tm=f" · {s['seconds']:.0f} s" if s.get("seconds") is not None else ""
        out.append(f"<div class='stg {stt}'>{mk} {i}/{n} · {esc(title)}{tm}"+(f"<span class='nt'>{esc(s['note'])}</span>" if s.get("note") else "")+"</div>")
    ms="".join(f"<div class='small'>✓ {esc(STEP_NOTE.get(k,k))} · <span class='mono'>{esc(m['utc'][11:19])} UTC</span></div>" for k,m in MILESTONES.items() if k in STEP_NOTE)
    pc=100*done/n
    bar=f'<div style="margin-top:6px;background:#e5e7eb;height:10px;border-radius:2px"><div style="width:{pc:.0f}%;height:10px;background:#7626D9;border-radius:2px"></div></div>'
    head=f"RUN {SESSION_ID} · {run_verdict()}"+(f" · started {STATE['started'][11:19]} UTC" if STATE.get("started") else "")+(f" · finished {STATE['finished'][11:19]} UTC" if STATE.get("finished") else "")
    return card(head,"".join(out)+(details("engine milestones received so far",ms,True) if ms else "")+bar,"m")
def console_text():
    with _LOG_LOCK:return "\n".join(list(CONSOLE)[-200:])

# ---------------------------------------------------------------------------------------------------------------------
# tab contents — read from THIS RUN's records, unedited
# ---------------------------------------------------------------------------------------------------------------------
def overview_html():
    res=R();v=res.get("verdict") or {}
    steps=[("Exact replay of the real decision traces (World 01 · World 00)","same pre-action state, executed ACQUIRE, real outcome MISSING vs LIVE; replay compared event by event with the locked records",
            all(s.get("checks",{}).get("t2_CAR_equals_record") for s in sides().values() if s.get("role")=="SOURCE") if sides() else None),
           ("Experience → physical Experience-CUT3 file","[X2][A][C]: H3 + K/V of layers 0–3, SHA-256 of the file and of every tensor, append-only folder",bool(exps()) or None),
           ("Source working state freed — reload from SSD","file + tensor SHA-256, rebuilt lower rows bit-identical, same native action",
            all(r.get("pass") for W_ in worlds().values() for r in (W_.get("persistence") or {}).values()) if worlds() else None),
           ("Native append into INDEPENDENT decision states","same-goal FORK state and the other world's state — selected from the records before any decision was read",
            all((W_.get("panels") or {}) for W_ in worlds().values()) if worlds() else None),
           ("Native CAR decision of the frozen model","six action words, first token + teacher-forced continuation; decision = the model's own argmax; nothing executed",bool(panels()) or None),
           ("Outcome / action controls","C-BLIND (outcome hidden) · A-BLIND vs kernel-matched A-REF (action hidden)",(v.get("verdict") not in (None,"TECHNICAL_BLOCK")) if v else None),
           ("Host re-verification of every cartridge file","read-only after the engine process ended",bool((LIVE.get("verification") or {}).get("cartridges")) or None)]
    rows=[(Markup(f"<b>{i}. {esc(a)}</b><br><span class='small' style='opacity:.85'>{esc(b)}</span>"),Markup(ok_mark(x))) for i,(a,b,x) in enumerate(steps,1)]
    ver=""
    if v:ver=card(f"TEST878 verdict of this RUN — {v.get('verdict')}",tbl([("scope (cross-world class)",f"{v.get('scope')} · {v.get('cross_world_class')}"),("same-goal panels",json.dumps(v.get("same_goal"))),
                    ("cross-world panels",json.dumps(v.get("cross_world"))),("engine blocks",json.dumps(v.get("blocks"))),("credit",v.get("credit")),("limits","; ".join(v.get("limits") or []))]),
                  "on" if v.get("verdict") not in (None,"TECHNICAL_BLOCK","PARTIAL_INCONCLUSIVE") else "warn")
    arch=card("What the cartridge is — and what it is not",
        "<b>What is stored:</b> internal states of the frozen Qwen2.5-72B for the rows [X2][A][C] — the layer-3 output H3 and the K/V of layers 0–3 — in a .pt file on the SSD, SHA-256 sealed.<br>"
        "<b>How it is read:</b> the locked native append re-phases the stored keys (RoPE) to the target positions, places H3 at the layer-3 cut and lets the frozen model recompute layers 4–79 "
        "while attending to the target's own memory. The target then reads its own decision input; the model's log-probabilities of the six action words are the decision.<br>"
        "<b>Not text RAG · not fine-tuning:</b> no text of the experience in any prompt; weights frozen (digest identical); no hooks (audited); Python never picks an action.<br>"
        "<b>Not credit assignment:</b> hiding the executed action changes the outcome-dependent computation, but this run does not show that the model assigns credit to the action, "
        "nor that the changed decision is correct (no oracle is used).","info")
    lin=card("Research lineage (published records and repositories — not results of this experiment)","<br>".join(f"{esc(t)} · <a href='{u}' target='_blank' rel='noopener'>{esc(u)}</a>" for t,u in LINEAGE)+
             f"<br>Reference GPU run of this file: <a href='{URL_LOG}' target='_blank' rel='noopener'>{esc(URL_LOG)}</a> · source: <a href='{URL_CODE}' target='_blank' rel='noopener'>{esc(URL_CODE)}</a>","info")
    return card(f"What happens in this RUN ({SESSION_ID})",tbl(rows,["step","this RUN"]),"m")+ver+arch+lin
def cartridges_html():
    if not exps():return card("Experience-CUT3 cartridges","Not available yet — the engine writes them during RUN (stage 2).","info")
    V=(LIVE.get("verification") or {}).get("cartridges") or {};rows=[]
    for eid,e in exps().items():
        pv=e.get("provenance") or {};sp=pv.get("spans_body") or {};v=V.get(eid) or {}
        rows.append((eid,pv.get("outcome_cartridge"),pv.get("action"),f"X2 {sp.get('X2')} · A {sp.get('A')} · C {sp.get('C')}",f"{e.get('body_tokens')} (+P {e.get('p')})",fmt_b(e.get("bytes")),e.get("sha256"),
                     Markup(ok_mark(v.get("file_sha_ok"))+" / "+ok_mark(v.get("tensor_sha_ok")))))
    pr=(LIVE.get("verification") or {}).get("pairs") or {}
    prov="".join(details(f"provenance · {esc(eid)}",pre(json.dumps(e.get("provenance"),indent=1),320)) for eid,e in exps().items())
    return (card("Experience-CUT3 cartridges written by the engine in this RUN",tbl(rows,["id","real outcome","action","rows (body)","tokens","file","file SHA-256","host re-hash file / tensors"],mono_cols=(6,)),"m")+
            card("MISSING vs LIVE of the same world (host, torch.equal)",tbl([(f"World {w}",Markup(ok_mark(p.get('h_X2A_bitwise') and p.get('lower_X2A_bitwise'))),Markup(ok_mark(p.get('h_C_differs')))) for w,p in pr.items()],
                 ["world","X2 and A rows bit-identical","C rows differ"]) if pr else "after VERIFY","on" if pr else "info")+card("Provenance recorded in each cartridge entry",prov,"info"))
def persistence_html():
    if not worlds():return card("Persistence and parity","Not available yet.","info")
    rows=[]
    for w,W_ in worlds().items():
        for c,r in (W_.get("persistence") or {}).items():
            rows.append((f"W{w} {c}",Markup(ok_mark(r.get("pass"))),Markup(ok_mark(r.get("reloaded_sha_ok"))),Markup(ok_mark(r.get("lower_rows_bitwise"))),f"{r.get('roundtrip_K_rel',0):.5f}",
                         Markup(ok_mark(r.get("action_same"))),f"{r.get('max_dp',0):.5f}",str(r.get("within_6e-4")),Markup(ok_mark(r.get("explicit_append_equals_native_bitwise"))),
                         json.dumps(r.get("A_reference_mask"))))
    fl=tbl([(f"World {w}",json.dumps(W_.get("floor"))) for w,W_ in worlds().items()],["world","detection floor (reconstruction noise, first / seq)"])
    sd=tbl([(s,json.dumps(x.get("checks"))) for s,x in sides().items()],["side","engine gates at capture"],mono_cols=(1,))
    return (card("Persistence gate (pre-registered: same action and max |Δp| ≤ 0.10; 6e-4 reported separately)",tbl(rows,["source","pass","reload SHA","L0–3 rows bitwise","RoPE rt","same action","max |Δp|","≤ 6e-4","explicit = native append","A-ref mask"]),"m")+
            card("Detection floors",fl,"info")+card("Capture gates of every replayed side",sd,"info"))
def panels_html():
    if not panels():return card("Transfer panels","Not available yet.","info")
    out=""
    for w,kind,p in panels():
        arms=[(a,x.get("action"),*[f"{float((x.get('p') or {}).get(w_,0)):.4f}" for w_ in WORDS]) for a,x in (p.get("arms") or {}).items()]
        con=[(a,", ".join(f"{z:.3f}" for z in (c.get("seq") or []))) for a,c in (p.get("contrast") or {}).items()]
        out+=card(f"{ptitle(w,kind)} — {p.get('status')}",
                  f"target {esc(json.dumps(p.get('target')))} · spans {esc(json.dumps(p.get('spans')))}"+tbl(arms,["arm","native action"]+list(WORDS))+
                  details("outcome contrasts (15 sequence margins, M − L)",tbl(con,["arm","contrast"],mono_cols=(1,)))+
                  details("gates · detect · A-REF gate · A dependence",pre(json.dumps(dict(gates=p.get("gates"),detect=p.get("detect"),A_ref=p.get("A_ref"),A_dependence=p.get("A_dependence")),indent=1),360)),
                  "on" if p.get("status")=="ACTION_INFORMATION_DEPENDENT_TRANSFER" else "warn")
    return out
def rule_html():
    if not panels():return card("Decision rule","Not available yet.","info")
    rows=[]
    for w,kind,p in panels():
        a=p.get("A_ref") or {};rows.append((f"W{w} {kind}",p.get("status"),a.get("norm_T_full_seq"),(worlds().get(w) or {}).get("floor",{}).get("seq"),a.get("K_full_minus_ref_seq"),
                                            a.get("norm_ref_minus_blind_seq"),a.get("threshold_max_floor_K"),Markup(ok_mark(a.get("interpretable")))))
    return card("Pre-registered panel rule applied by the engine",tbl(rows,["panel","status","‖T_FULL‖","floor","K kernel","‖T_A-REF − T_A-BLIND‖","threshold","A-REF usable"])+
                "<div class='small'>1 outcome transfer: ‖T_FULL‖ &gt; floor · 2 A-REF usable: ‖T_A-REF‖ &gt; floor, ⟨T_FULL,T_A-REF⟩ &gt; 0, K &lt; ‖T_FULL‖ · "
                "3 action information: ‖T_A-REF − T_A-BLIND‖ &gt; max(floor, K). A change of decision is not a test of correctness.</div>","m")
def integrity_html():
    rows=[(c["utc"][11:19],c["name"],Markup(ok_mark(c["passed"])),c["detail"][:160]) for c in CHECKS]
    src=[(n,v["git_blob"],v["sha256"],f"{v['bytes']:,}",v.get("obtained")) for n,v in SOURCES.items()];V=LIVE.get("verification") or {}
    return (card(f"Engine gate lines of this RUN — {sum(1 for c in CHECKS if c['passed'])} PASS · {sum(1 for c in CHECKS if not c['passed'])} FAIL",
                 tbl(rows,["UTC","gate","result","detail"],mono_cols=(3,)) if rows else "none yet","on" if rows and all(c["passed"] for c in CHECKS) else "info")+
            card("Independent re-verification after the run (read-only, host)",pre(json.dumps(jsafe(V),indent=1),420) if V else "after the engine process","info")+
            card("Source identity of the engine run",pre(json.dumps(jsafe((R().get("source") or {})),indent=1),300) if R() else "after the engine process","info")+
            card("Locked files (git blob verified)",tbl(src,["file","git blob","SHA-256","bytes","obtained"],mono_cols=(1,2)),"info"))
def resources_html():
    L=LEDGER.get("TEST878")
    if not L:return card("Resources","after the engine process","info")
    rows=[(k,(m["utc"][11:19]),short(m["line"],160)) for k,m in MILESTONES.items()]
    return (card("Process record",pre(json.dumps(jsafe({k:v for k,v in L.items() if k!="cmd"}),indent=1),320),"m")+
            card("Engine milestones (receipt time of each line)",tbl(rows,["milestone","UTC","line"],mono_cols=(2,)),"info")+
            card("Per-world engine numbers",tbl([(f"World {w}",W_.get("elapsed_s"),W_.get("reads"),W_.get("peak_gib")) for w,W_ in worlds().items()],["world","panels s","CAR reads","torch peak GiB"]),"info"))

TABS=["OVERVIEW","CARTRIDGES","PERSISTENCE · PARITY","TRANSFER PANELS","DECISION RULE","INTEGRITY","RESOURCES","SCIENTIFIC FIGURES"]
TAB_HTML={"OVERVIEW":overview_html,"CARTRIDGES":cartridges_html,"PERSISTENCE · PARITY":persistence_html,"TRANSFER PANELS":panels_html,"DECISION RULE":rule_html,
          "INTEGRITY":integrity_html,"RESOURCES":resources_html}
def _figlabel(k):m=FIGURES[k];return f"Figure {m['n']} — {m['title']}"
def tab_gallery(tab):
    keys=[k for k,m in FIGURES.items() if (m["tab"]==tab or tab=="SCIENTIFIC FIGURES") and k in FIG_FILES]
    return [(FIG_FILES[k]["jpg"],f"{_figlabel(k)} · {FIG_FILES[k]['badge']}") for k in keys]
def figs_status_html():
    n=len(FIG_FILES)
    if not n and not FIG_ERRORS:return card(f"Scientific figures of this RUN — 0/{len(BASE_FIGURES)}","The nine figures are drawn from this RUN's outputs after the engine has ended (stage 4). They appear here, one below the other.","info")
    def st(k):
        f=FIG_FILES.get(k)
        if not f:return "NOT GENERATED: "+str(FIG_ERRORS.get(k,"pending"))
        q=f.get("layout_qc") or {};j=f.get("jpeg_qc") or {}
        return f"{f['badge']} · {f['pixels'][0]}×{f['pixels'][1]} JPEG 300 dpi · layout QC {'PASS' if q.get('passed') else 'FAIL'} · JPEG QC {'PASS' if j.get('passed') else 'FAIL'}"
    rows="".join(f"<div class='small'>{'✓' if k in FIG_FILES and (FIG_FILES[k].get('layout_qc') or {}).get('passed') and FIG_FILES[k]['badge']!='NOT PRODUCED IN THIS RUN' else '✗'} {esc(_figlabel(k))} · <b>{esc(st(k))}</b></div>" for k in FIGURES)
    ok=all(k in FIG_FILES for k in BASE_FIGURES) and all((v.get("layout_qc") or {}).get("passed") and v["badge"]!="NOT PRODUCED IN THIS RUN" for v in FIG_FILES.values())
    return card(f"Scientific figures of this RUN ({SESSION_ID}) — {n} JPEG file(s)",rows,"on" if ok else "warn")
from urllib.parse import quote as _urlquote   # NOTE: never shadow — the URL quote has its own name
# relative URLs (no leading "/"): they resolve against the page itself (share link, Colab port window, proxy root path)
def file_url(p):return ("gradio_api/file=" if _GR_MAJOR>=5 else "file=")+_urlquote(str(p),safe="/")
def file_url_alt(p):return ("file=" if _GR_MAJOR>=5 else "gradio_api/file=")+_urlquote(str(p),safe="/")
def figs_main_html():
    """the figures of THIS run, in order — each with its own direct JPEG download link below it"""
    if not FIG_FILES:return card("Figures","No figure of this RUN yet (figures of an earlier RUN are never shown).","info")
    keys=[k for k in FIGURES if k in FIG_FILES];out=[]
    bulk=("<a href='#' onclick=\"var l=document.querySelectorAll('a.kz-dl');for(var i=0;i<l.length;i++){(function(a,d){setTimeout(function(){a.click()},d)})(l[i],i*900)};return false;\">"
          f"<b>⬇ Download all {len(keys)} figures (JPEG), one after another</b></a>")
    out.append(card("Direct downloads — no ZIP",f"{bulk}<br><span class='small'>The browser downloads the JPEG files in order. Some browsers ask once to “allow multiple downloads”; if blocked, "
                    "use the link under each figure or the JPEG file list below — every file downloads with one tap. The same figures are also shown and downloaded in the Colab cell.</span>","on"))
    for k in keys:
        f=FIG_FILES[k];u=file_url(f["jpg"]);ua=file_url_alt(f["jpg"]);nm=Path(f["jpg"]).name;qc=(f.get("layout_qc") or {}).get("passed") and f["badge"]!="NOT PRODUCED IN THIS RUN"
        out.append(f"<div class='kz card {'on' if qc else 'err'}'><div class='h'>{esc(_figlabel(k))} · {esc(f['badge'])}"+("" if (f.get("layout_qc") or {}).get("passed") else " · LAYOUT QC FAIL")+"</div>"
                   f"<img src='{u}' data-alt='{ua}' onerror=\"if(!this.dataset.done){{this.dataset.done=1;this.src=this.dataset.alt;var a=this.parentNode.querySelector('a.kz-dl');if(a)a.href=this.dataset.alt;}}\" "
                   f"style='width:100%;height:auto;border:1px solid #d1d5db' alt='{esc(_figlabel(k))}'>"
                   f"<div class='small' style='margin-top:4px'><a class='kz-dl' href='{u}' download='{esc(nm)}'><b>⬇ Download {esc(_figlabel(k).split(' — ')[0])} (JPEG, {f['pixels'][0]}×{f['pixels'][1]}, 300 dpi)</b></a> · "
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
_HAS_TIMER=hasattr(gr,"Timer") and hasattr(gr,"State")
def _snap_state(last):
    last=dict(last) if isinstance(last,dict) else {}
    return (*snapshot(last),last)
def run_click(last):
    start_run();time.sleep(.5);return _snap_state({})
def ui_tick(last):return _snap_state(last)
def page_load_state():return _snap_state({})
def run_handler():
    """fallback for a gradio without gr.Timer: one streaming request"""
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
        con=_tb(lines=12,max_lines=20,label="Live engine output of this RUN — every line the TEST878 process prints; progress bars update one line; also ENGINE_OUTPUT_REALTIME.log",value=console_text(),interactive=False)
        fstat=gr.HTML(_safe(figs_status_html));main_figs=gr.HTML(_safe(figs_main_html))
        jpgs=gr.File(label="The JPEG figures of this RUN, in order — each file downloads with one tap",value=(jpg_files() or None),file_count="multiple",interactive=False)
        files=gr.File(label="Real-time engine output, engine result files, session logs, verification, manifests — direct downloads (no ZIP)",value=(all_files() or None),file_count="multiple",interactive=False)
        htmls={};gals={}
        with gr.Tabs():
            for t in TABS:
                with gr.Tab(t):
                    if t in TAB_HTML:htmls[t]=gr.HTML(_safe(TAB_HTML[t]))
                    gals[t]=_gallery(label=f"{t} · figures",value=tab_gallery(t))
        gr.HTML(f'<div class="kz small" style="opacity:.8;margin:10px 0 18px">{esc(AUTHOR)} · {esc(ORG)} · {esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · '
                f'<a href="{file_url(EVID_DIR/ENGINE_NAME)}" download="878.py">878.py (the locked copy executed here)</a> · <a href="{URL_LICENSE}" target="_blank" rel="noopener">LICENSE</a> · '
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
    kw=dict(share=True,allowed_paths=[str(DEMO_ROOT)],show_error=True,inline=False,prevent_thread_lock=True,debug=False)
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
            port=int(re.search(r":(\d+)",str(local)).group(1));_co.serve_kernel_port_as_window(port,anchor_text="▶ Open the AKBASCORE TEST878 interface (Colab window)");window=f"Colab port window, port {port}"
        except Exception as ex:window=f"not available ({type(ex).__name__})"
    dump_json(GRADIO_LINK.with_suffix(".json"),dict(utc=utc_now(),session=SESSION_ID,share_url=share,local_url=local,colab_window=window,share_error=err))
    GRADIO_LINK.write_text(f"{share or local}\n",encoding="utf-8")
    banner(f"INTERFACE OPEN · {share or ('local only: '+str(local))}\n  public link : {share or '— (tunnel not available; use the Colab window link above)'}\n  local       : {local}\n"
           f"  Press RUN in the interface — everything else runs automatically. If the link stops working: run  launch_interface()  in a new cell.","#")
    slog("LAUNCH","interface open",share_url=share,local_url=local,colab_window=window);return share or local
def keep_cell_running():
    """keeps this Colab cell RUNNING while the interface is in use; when a RUN has finished its figures are shown here too"""
    banner("THE CELL STAYS RUNNING — the interface is live. Press RUN in the interface; the engine output is printed here and shown in the interface.\n"
           f"  A full RUN takes about 25–35 minutes on an A100 (model download not included). Stop this cell (■) only when you have finished; the files stay in {DEMO_ROOT}","#")
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
    """second, independent channel: the JPEG figures of THIS run are shown in the Colab cell and each is offered as a browser
    download. Can also be called by hand in a new cell:  show_figures_in_cell()"""
    keys=[k for k in FIGURES if k in FIG_FILES]
    banner(f"FIGURES OF THIS RUN ({SESSION_ID}) — {len(keys)} JPEG file(s) — shown below in the cell, each also downloaded by the browser\n  folder: {FIG_DIR}","#")
    try:from IPython.display import display,Image as _IImg,HTML as _IHTML
    except Exception as ex:slog("CELL_FIGURES","IPython display not available",error=f"{type(ex).__name__}: {ex}");return
    for k in keys:
        f=FIG_FILES[k];nm=Path(f["jpg"]).name
        try:
            display(_IHTML(f"<div style='font:600 15px sans-serif;margin:14px 0 4px'>{esc(_figlabel(k))} · {esc(f['badge'])} · {esc(nm)} · SHA-256 {esc(f['sha256_jpg'][:16])}…</div>"))
            display(_IImg(filename=f["jpg"],width=1100))
        except Exception as ex:slog("CELL_FIGURES",f"{k} could not be shown in the cell",error=f"{type(ex).__name__}: {ex}")
    if not download:return
    try:from google.colab import files as _cf
    except Exception:slog("CELL_FIGURES","not in Colab — browser download from the cell skipped; the files are in the folder above");return
    for k in keys:
        f=FIG_FILES[k]
        try:_cf.download(f["jpg"]);slog("CELL_DOWNLOAD",Path(f["jpg"]).name);time.sleep(1.0)
        except Exception as ex:slog("CELL_DOWNLOAD",f"{Path(f['jpg']).name} not downloaded",error=f"{type(ex).__name__}: {ex}")

# ---------------------------------------------------------------------------------------------------------------------
# START-UP (no GPU use): locked sources verified, then the interface opens
# ---------------------------------------------------------------------------------------------------------------------
def startup():
    banner(f"{APP_NAME} · {EXPERIMENT} · start-up {local_now()} · session {SESSION_ID}"+("\nSIMULATION — NOTHING HERE IS AN EXPERIMENTAL RESULT" if SIM else ""))
    for n in LOCKS:RAW[n]=fetch_locked(n);slog("LOCKED_SOURCE",n,git_blob=SOURCES[n]["git_blob"],bytes=SOURCES[n]["bytes"],obtained=SOURCES[n]["obtained"],**({"notes":SOURCES[n]["notes"]} if SOURCES[n].get("notes") else {}))
    slog("ENGINE_READY","878.py locked; it runs unchanged as one OS process when RUN is pressed",git_blob=LOCKS[ENGINE_NAME])
_missing=[n for n in (1,2) if n not in _AKB878_PARTS]
if _missing:raise RuntimeError(f"PART {_missing} of the program is missing in this cell — paste PART 1, 2 and 3 one below the other, each completely (every part ends with an END OF PART line)")
try:startup()
except Exception as _ex:
    _m=str(_ex)
    _hint=("No copy with the locked git blob was found, not even the embedded one: paste PART 1, 2 and 3 again exactly as delivered (nothing "
           "cut off or edited), then run the cell again. The program stops instead of running unverified code." if "NOT AVAILABLE" in _m else
           "Network error while downloading a locked source from GitHub: run the cell again." if any(x in _m for x in ("URLError","timed out","HTTP Error","Connection","Name or service")) else
           "See the traceback above; nothing was run.")
    banner(f"START-UP FAILED — {type(_ex).__name__}: {_m}\nWHAT TO DO: {_hint}\nRecords of this attempt: {SESSION_DIR}","!")
    raise
if os.environ.get("AKB878_NO_LAUNCH")!="1":launch_interface()
if os.environ.get("AKB878_NO_BLOCK")!="1" and os.environ.get("AKB878_NO_LAUNCH")!="1":keep_cell_running()
# ===== END OF PART 3/3 =====
