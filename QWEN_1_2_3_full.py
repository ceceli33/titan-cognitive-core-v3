# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST782 · LIVE RESEARCH DEMONSTRATION (Gradio, Silicon Hippocampus 1.5 / SH745 infrastructure)
# Three isolated sessions of ONE frozen model · physical CUT3 cartridges · native numerical BASELINE MASTER · blind reading
#   QWEN-1 (OS process) : European Commission "AI in science" + Future of Life Institute "recursive self-improvement" statement
#                         → SOURCE_A / SOURCE_B physical cartridges (H3 + K/V L0–L3) → SSD → SHA-256 → process ends
#   QWEN-2 (new process): physical cartridges only → native numerical fusion → MASTER_02 → seals · 80/80 parity → process ends
#   QWEN-3 (new process): MASTER_02 only (no source text, no source cartridge) → 80/80 reload → human language → process ends
#   CONTROLS            : NO_MEMORY · SOURCE_A_ONLY · SOURCE_B_ONLY · BASELINE_MASTER on the same pre-sealed question panel
# Qwen/Qwen2.5-72B-Instruct · NF4 4-bit frozen · BF16 · CUT3 · NVIDIA A100-SXM4-80GB · ONE Google Colab cell
# PART 1 / 4 — locked sources (782.py embedded), run folder, OS-level isolation, the session processes and their evidence
# THIS PART  75,090 characters · its last line is  # ===== END OF PART 1/4 =====
# ---------------------------------------------------------------------------------------------------------------------
# HOW TO RUN  Paste PART 1, 2, 3 and 4 one below the other into ONE Colab cell (A100 runtime, fresh) and run it. Each part is
#             shorter than 80,000 characters and ends with an END OF PART line — check that line after every paste. No upload
#             is needed: the engine 782.py and its locked sources are embedded byte-exact and git-blob verified before use.
#             The cell stays running; the interface opens with ONE button: RUN. RUN executes 782.py — locked by its git blob — as FIVE separate OS processes, strictly one
#             after the other: PREFLIGHT (CPU gate) → QWEN-1 → QWEN-2 → QWEN-3 → CONTROLS. QWEN-2 and QWEN-3 run as their own
#             unprivileged Linux users without network where the runtime allows it; the GPU is checked empty between sessions.
#             Every line the engine prints is received, time-stamped and shown at once. After the last session this program
#             re-verifies every cartridge read-only, draws twelve JPEG figures (heat maps included) from THIS run's outputs —
#             the QWEN-3 expression printed verbatim — and offers every record for direct download (no ZIP).
# STATUS      NOT executed on a GPU by its author (CPU simulation of the code paths with a fake model only).
# AUTHOR      Mustafa Akbaş · AkbasCore AI Teknoloji · Mersin, Türkiye · Copyright © 2026 Mustafa Akbaş
#             AKBASCORE RESEARCH SOFTWARE LICENSE — https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/LICENSE
#             Source documents: European Commission (research-and-innovation.ec.europa.eu) and Future of Life Institute
#             (futureoflife.org) — linked and hash-recorded; their full texts are not redistributed by this demonstration.
#             Qwen2.5-72B-Instruct and third-party libraries remain governed by their own licences.
# =====================================================================================================================
import os,sys,re,io,ast,json,time,html,math,shutil,hashlib,platform,threading,traceback,subprocess,importlib.util,textwrap,types,gc,difflib,pwd,grp,stat
from pathlib import Path
from datetime import datetime,timezone
from collections import OrderedDict,deque
os.environ.pop("HF_HUB_DISABLE_PROGRESS_BARS",None)

def _pip(*pk):subprocess.check_call([sys.executable,"-m","pip","install","-q",*pk])
for _m,_p in (("numpy","numpy"),("matplotlib","matplotlib"),("PIL","pillow"),("psutil","psutil"),("bs4","beautifulsoup4")):
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
from matplotlib.colors import LogNorm,ListedColormap
from PIL import Image
import gradio as gr
import urllib.request
SIM=os.environ.get("AKB782_SIM")=="1"          # code author's CPU simulation only (fake model) — never an experimental result

# ---------------------------------------------------------------------------------------------------------------------
# identity, locks, colours
# ---------------------------------------------------------------------------------------------------------------------
APP_NAME="AKBASCORE SILICON HIPPOCAMPUS";APP_SUB="TEST782 · Three Isolated Sessions · Physical Memory · Numerical MASTER · Blind Reading"
APP_SHORT="AKBASCORE Silicon Hippocampus · TEST782 · Qwen2.5-72B · CUT3";CODE_VERSION="SH782-demo-1.0";EXPERIMENT="TEST782"
AUTHOR="Mustafa Akbaş";ORG="AkbasCore AI Teknoloji";PLACE="Mersin, Türkiye"
LICENSE_NAME="AKBASCORE RESEARCH SOFTWARE LICENSE";COPYRIGHT="Copyright © 2026 Mustafa Akbaş"
REPO="https://github.com/ceceli33/titan-cognitive-core-v3";RAW_BASE="https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
REPO_V2="https://github.com/ceceli33/titan-cognitive-core-v2";ZENODO_REC="https://doi.org/10.5281/zenodo.23556509"
URL_LICENSE=REPO+"/blob/main/LICENSE"      # 782.py is not published yet (researcher approval pending) — the executed copy is offered locally
ENGINE_NAME="782.py";ENGINE_BLOB="4f42a33f53d9818630003baa4d674c8e504d50f9"
LOCKS=OrderedDict([("782.py",ENGINE_BLOB),                                              # TEST782 engine — executed byte-for-byte
                   ("709.py","6c9f8cbb1eeed848d45133d73f0d7676b68e9125"),               # locked engine functions (imported by 782.py)
                   ("730.py","b1bad9eb3b111b44413f8ef05a3a140ab66a77dd"),
                   ("757.py","3d88bf8638390995858f23391f1e043faa586835"),
                   ("764.py","99acb97cde2b11c0c23e14a3ed11cb6f5d7f3902"),
                   ("779.py","fa7017a87f25ecef6ed2b2954a850599cb25fcd9"),
                   ("LICENSE","9aad4724d1072f9e56486650a9527380c867a53b")])
MODEL_ID="Qwen/Qwen2.5-72B-Instruct"
SRC_URL={"SOURCE_A":"https://research-and-innovation.ec.europa.eu/research-area/industrial-research-and-innovation/artificial-intelligence-ai-science_en",
         "SOURCE_B":"https://futureoflife.org/statement/statement-we-must-pressure-ai-companies-to-immediately-limit-the-use-of-recursive-self-improvement/"}
SRC_LABEL={"SOURCE_A":"European Commission — Artificial intelligence (AI) in science","SOURCE_B":"Future of Life Institute — statement on limiting recursive self-improvement"}
COL=dict(A="#2455D6",B="#C12566",M="#7626D9",Q1="#2455D6",Q2="#7626D9",Q3="#0F766E",CTL="#B45309",PRE="#374151",HOST="#6B7280")
OK_COL="#08785B";NEU="#374151";BG="#FFFFFF";INK="#111827";INK2="#374151";MUTED="#6B7280";RULE="#D1D5DB";PANEL="#F8FAFC";RED="#B91C1C";AMBER="#B45309"
SESSIONS=("PREFLIGHT","QWEN1","QWEN2","QWEN3","CONTROLS")
SCOL={"PREFLIGHT":COL["PRE"],"QWEN1":COL["Q1"],"QWEN2":COL["Q2"],"QWEN3":COL["Q3"],"CONTROLS":COL["CTL"]}
SNAME={"PREFLIGHT":"PREFLIGHT","QWEN1":"QWEN-1","QWEN2":"QWEN-2","QWEN3":"QWEN-3","CONTROLS":"CONTROLS"}

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
# directories and logs — every RUN has its own session folder and its own engine run folder; nothing is overwritten
# ---------------------------------------------------------------------------------------------------------------------
_CROOT=Path("/content") if os.path.isdir("/content") else Path("/tmp")
DEMO_ROOT=_CROOT/"AKBASCORE_TEST782_DEMO";EVID_DIR=DEMO_ROOT/"locked_sources"
SESSION_ID=SESSION_DIR=FIG_DIR=DATA_DIR=SESSION_LOG=SESSION_EVENTS=ENGINE_OUT=RUN_SUMMARY=MANIFEST=VERIFY_FILE=RUN_ROOT=None
def _session_paths(sid):
    """every RUN gets its own ID and folder (engine run folder, figures, records, logs)"""
    global SESSION_ID,SESSION_DIR,FIG_DIR,DATA_DIR,SESSION_LOG,SESSION_EVENTS,ENGINE_OUT,RUN_SUMMARY,MANIFEST,VERIFY_FILE,RUN_ROOT
    SESSION_ID=sid;SESSION_DIR=DEMO_ROOT/"sessions"/sid;FIG_DIR=SESSION_DIR/"figures";DATA_DIR=SESSION_DIR/"records"
    SESSION_LOG=SESSION_DIR/"SESSION.log";SESSION_EVENTS=SESSION_DIR/"SESSION_EVENTS.jsonl";ENGINE_OUT=SESSION_DIR/"ENGINE_OUTPUT_REALTIME.log"
    RUN_SUMMARY=SESSION_DIR/"RUN_SUMMARY.txt";MANIFEST=SESSION_DIR/"SHA256_MANIFEST.json";VERIFY_FILE=DATA_DIR/"POST_RUN_VERIFICATION.json"
    RUN_ROOT=SESSION_DIR/"run"
    for d in (DEMO_ROOT,DEMO_ROOT/"sessions",SESSION_DIR,FIG_DIR,DATA_DIR,EVID_DIR):d.mkdir(parents=True,exist_ok=True)
    for d in (DEMO_ROOT,DEMO_ROOT/"sessions"):os.chmod(d,0o755)
    os.chmod(SESSION_DIR,0o711)                 # sessions may traverse to run/ but cannot list or read the host's records
    for d in (FIG_DIR,DATA_DIR):os.chmod(d,0o700)
_session_paths(datetime.now().astimezone().strftime("SH782-%Y%m%d-%H%M%S"))
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
EMBEDDED={                                   # generated by the build — do not edit; checked against LOCKS before use
 "782.py":(  # 72674 bytes · git blob 4f42a33f53d9818630003baa4d674c8e504d50f9
  "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"
 ),
}
def embedded_copy(name):
    import zlib,base64
    if name not in EMBEDDED:return None,"no embedded copy"
    try:b=zlib.decompress(base64.b64decode("".join(EMBEDDED[name])))
    except Exception as ex:return None,f"embedded copy unreadable ({type(ex).__name__})"
    return (b,None) if git_blob(b)==LOCKS[name] else (None,f"embedded copy blob {git_blob(b)[:12]} != lock")
def fetch_locked(name,timeout=60):
    """order: verified cache → repository (raw GitHub) → /content/<name> → embedded copy. Every candidate must have the locked git blob;
    a candidate with another blob is never executed and is reported. The way the file was obtained is recorded for every run."""
    p=EVID_DIR/name;want=LOCKS[name];notes=[]
    if p.is_file() and git_blob(p.read_bytes())==want:
        raw=p.read_bytes();prev=SOURCES.get(name) or {}
        how=prev.get("obtained") or "cached copy from an earlier start-up (blob verified)";notes=list(prev.get("notes") or [])
    else:
        raw=None;how=None
        if p.is_file():notes.append(f"cached {p.name} has git blob {git_blob(p.read_bytes())[:12]}… (not the lock) — not used")
        try:
            req=urllib.request.Request(RAW_BASE+name,headers={"User-Agent":"AKBASCORE-TEST782-DEMO"})
            with urllib.request.urlopen(req,timeout=timeout) as f:b=f.read()
            if git_blob(b)==want:raw=b;how="GitHub "+RAW_BASE+name+" (blob verified)"
            else:notes.append(f"GitHub copy has git blob {git_blob(b)[:12]}… (not the lock) — not used")
        except Exception as ex:notes.append(f"GitHub: {type(ex).__name__}: {str(ex)[:120]}")
        loc=_CROOT/name
        if raw is None and loc.is_file():
            b=loc.read_bytes()
            if git_blob(b)==want:raw=b;how=f"local file {loc} (blob verified)"
            else:notes.append(f"{loc} has git blob {git_blob(b)[:12]}… (not the lock) — not used")
        if raw is None:
            b,why=embedded_copy(name)
            if b is not None:raw=b;how="embedded copy in this program (blob verified)"
            else:notes.append(why)
        if raw is None:raise RuntimeError(f"LOCKED SOURCE NOT AVAILABLE: {name} — "+" · ".join(notes))
        p.write_bytes(raw)
    SOURCES[name]=dict(bytes=len(raw),git_blob=git_blob(raw),sha256=sha_bytes(raw),url=RAW_BASE+name,obtained=how,notes=notes,verified_utc=utc_now())
    return raw

# ---------------------------------------------------------------------------------------------------------------------
# pipeline state
# ---------------------------------------------------------------------------------------------------------------------
STAGES=OrderedDict([
    ("PRECHECK","Pre-flight — one A100 80 GB, empty GPU, disk, locked engine 782.py and its locked engine sources, fresh run folder"),
    ("ISOLATION","Isolation set-up — separate Linux users for QWEN-2 / QWEN-3, folder permissions, network namespace, CUDA as those users"),
    ("PREFLIGHT","CPU acceptance gate (own process) — AST dependencies, 16 SHA / manifest simulations, tokenizer types, GPU budget, question panel sealed"),
    ("QWEN1","QWEN-1 (own process) — two real documents → SOURCE_A · SOURCE_B physical CUT3 cartridges → SSD → SHA-256 → process ends, GPU empty"),
    ("QWEN2","QWEN-2 (new process, own user) — cartridges only → native numerical fusion → MASTER_02 → 7 mandatory checks · 80/80 → process ends"),
    ("QWEN3","QWEN-3 (new process, own user) — MASTER_02 only → independent 80/80 reload → human-language expression → process ends"),
    ("CONTROLS","CONTROLS (new process) — NO_MEMORY · SOURCE_A_ONLY · SOURCE_B_ONLY · BASELINE_MASTER on the same sealed panel"),
    ("VERIFY","Independent re-verification (read-only) — files, tensor seals, manifests, parents, MASTER = A ⊕ B, isolation ledger, controls"),
    ("FIGURES","Twelve scientific figures (JPEG 300 dpi, layout QC) — heat maps and the verbatim QWEN-3 expression"),
    ("RECORDS","Records — real-time engine output, session logs, texts, manifests (direct downloads, no ZIP)")])
ENGINE_STAGES=("PREFLIGHT","QWEN1","QWEN2","QWEN3","CONTROLS")
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
CHECKS=[]                           # every PASS / FAIL / DIAG line of the engine (utc · session · name · detail)
LEDGER=OrderedDict()                # process ledger: one entry per engine session (pid, user, start, end, exit code, GPU)
GPU_SAMPLES=[]                      # nvidia-smi samples during the whole run (time, used MiB, compute apps)

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
    try:return sum(f.stat().st_size for f in Path(d).rglob("*") if f.is_file() and not f.is_symlink()) if Path(d).is_dir() else 0   # snapshot links are not counted twice
    except Exception:return None
def stage_precheck():
    g=nvsmi("gpu=name,memory.total,memory.used,driver_version");rows=[x.split(", ") for x in g]
    LIVE["gpu"]=dict(count=len(rows),name=rows[0][0] if rows else None,total_mib=int(rows[0][1]) if rows else None,used_mib=int(rows[0][2]) if rows else None,
                     driver=rows[0][3] if rows else None,apps=nvsmi("compute-apps=pid,used_memory"))
    if SIM:LIVE["gpu"].update(count=1,name="SIMULATED A100-SXM4-80GB",total_mib=81920,used_mib=0,apps=[])
    if not LIVE["gpu"]["count"]:raise RuntimeError("no NVIDIA GPU in this runtime — TEST782 needs one A100 80 GB (Runtime → Change runtime type → A100). Nothing was run.")
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
            f"782.py git blob {LOCKS[ENGINE_NAME][:12]}… ({SOURCES[ENGINE_NAME]['obtained']}) · run folder {RUN_ROOT.name}")

# ---------------------------------------------------------------------------------------------------------------------
# ISOLATION — separate Linux users, folder permissions, network namespace; every barrier is probed, nothing is assumed
# ---------------------------------------------------------------------------------------------------------------------
USERS={"QWEN2":"akb_q2","QWEN3":"akb_q3"};HF_GROUP="akbhf"
ISO=dict(mode=None,users={},netns=False,setpriv=False,probes={},notes=[],perm_maps=OrderedDict())
def rpath(name):return RUN_ROOT/name
FOLDERS=("locked_sources","panel","preflight","q1_sources","q1_cartridges","q2_work","master_bundle","q3_out","controls")
def _run(cmd,**kw):
    try:return subprocess.run(cmd,capture_output=True,text=True,timeout=kw.pop("timeout",120),**kw)
    except Exception as ex:return types.SimpleNamespace(returncode=-1,stdout="",stderr=f"{type(ex).__name__}: {ex}")
def _ensure_user(name):
    try:return pwd.getpwnam(name)
    except KeyError:pass
    r=_run(["useradd","-m","-s","/usr/sbin/nologin","-G",HF_GROUP,name])
    if r.returncode!=0:raise RuntimeError(f"useradd {name}: {r.stderr.strip()[:200]}")
    return pwd.getpwnam(name)
def _chown(p,user=None,group=None):
    uid=pwd.getpwnam(user).pw_uid if user else 0;gid=grp.getgrnam(group).gr_gid if group else 0
    os.chown(p,uid,gid,follow_symlinks=False)
def _tree(p,dmode,fmode,user=None,group=None):
    p=Path(p)
    if not p.exists():return
    _chown(p,user,group);os.chmod(p,dmode)
    for q in p.rglob("*"):
        if q.is_symlink():continue
        _chown(q,user,group);os.chmod(q,dmode if q.is_dir() else fmode)
def _mode(p):
    try:
        s=os.stat(p);return dict(owner=pwd.getpwuid(s.st_uid).pw_name,group=grp.getgrgid(s.st_gid).gr_name,mode=oct(stat.S_IMODE(s.st_mode)))
    except Exception:return None
def launch_cmd(session,force_root=False):
    base=[sys.executable,"-u",str(rpath("locked_sources")/ENGINE_NAME),"--session",session,"--root",str(RUN_ROOT)]
    user=USERS.get(session) if (ISO["mode"]=="OS_USERS" and not force_root) else None
    if user and ISO["setpriv"]:
        pw=pwd.getpwnam(user);base=["setpriv",f"--reuid={pw.pw_uid}",f"--regid={pw.pw_gid}","--init-groups","--"]+base
    if session in ("QWEN2","QWEN3") and ISO["netns"]:base=["unshare","--net","--"]+base
    return base,user
def _preexec(user):
    def f():
        os.umask(0o022)
        if user and ISO["mode"]=="OS_USERS" and not ISO["setpriv"]:
            pw=pwd.getpwnam(user);os.initgroups(user,pw.pw_gid);os.setgid(pw.pw_gid);os.setuid(pw.pw_uid)
    return f
def session_env(session,user):
    env=dict(os.environ,PYTHONUNBUFFERED="1",PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True",HF_HOME=str(hf_home()),AKB782_NETNS="0")
    if session in ("QWEN2","QWEN3","CONTROLS"):env.update(HF_HUB_OFFLINE="1",TRANSFORMERS_OFFLINE="1")
    if session in ("QWEN2","QWEN3") and ISO["netns"]:env["AKB782_NETNS"]="1"
    if user and ISO["mode"]=="OS_USERS":
        home=pwd.getpwnam(user).pw_dir;env.update(HOME=home,USER=user,LOGNAME=user,XDG_CACHE_HOME=home+"/.cache",TRITON_CACHE_DIR=home+"/.triton",TMPDIR=home+"/tmp")
        Path(home,"tmp").mkdir(parents=True,exist_ok=True);_tree(home,0o700,0o600,user,user)
    if SIM and os.environ.get("AKB782_SIM_PYTHONPATH"):env["PYTHONPATH"]=os.environ["AKB782_SIM_PYTHONPATH"]
    for k in ("HF_TOKEN","HUGGING_FACE_HUB_TOKEN"):
        if session!="QWEN1":env.pop(k,None)
    return env
PROBE_SRC=r'''
import os,sys,json,socket
out={"uid":os.getuid(),"gid":os.getgid(),"groups":os.getgroups()}
for k,p in json.loads(sys.argv[1]).items():
    try:
        with open(p,"rb") as f:f.read(1)
        out[k]="READ"
    except PermissionError:out[k]="DENIED"
    except Exception as ex:out[k]=type(ex).__name__
try:
    s=socket.create_connection(("8.8.8.8",53),timeout=3);s.close();out["network"]="REACHABLE"
except Exception as ex:out["network"]="BLOCKED ("+type(ex).__name__+")"
try:
    import torch;out["torch"]=getattr(torch,"__version__","?");out["cuda"]=bool(torch.cuda.is_available());out["devices"]=torch.cuda.device_count()
    if out["cuda"]:x=torch.ones(1,device="cuda");out["cuda_alloc"]=float(x.sum().item())==1.0;del x
except Exception as ex:out["torch_error"]=type(ex).__name__+": "+str(ex)[:160]
print("AKB782_PROBE "+json.dumps(out),flush=True)
'''
def _probe(session,files):
    base,user=launch_cmd(session);base=base[:base.index(sys.executable)]+[sys.executable,"-c",PROBE_SRC,json.dumps({k:str(v) for k,v in files.items()})]
    env=session_env(session,user)
    try:r=subprocess.run(base,capture_output=True,text=True,timeout=300,env=env,cwd=(env.get("HOME") if user else str(RUN_ROOT)),preexec_fn=_preexec(user))
    except Exception as ex:return {"error":f"{type(ex).__name__}: {ex}"}
    line=next((l for l in r.stdout.splitlines() if l.startswith("AKB782_PROBE ")),None)
    return json.loads(line.split(" ",1)[1]) if line else {"error":f"rc={r.returncode} {(r.stderr or r.stdout)[-300:]}"}
def apply_permissions(phase):
    """the access design of each phase, applied explicitly (owner · group · mode) and recorded"""
    users=ISO["mode"]=="OS_USERS";u2=USERS["QWEN2"] if users else None;u3=USERS["QWEN3"] if users else None
    early=phase in ("PREFLIGHT","QWEN1")
    for n in FOLDERS:rpath(n).mkdir(exist_ok=True)
    os.chmod(RUN_ROOT,0o755)
    _tree(rpath("locked_sources"),0o755,0o644);_tree(rpath("panel"),0o755,0o644);_tree(rpath("preflight"),0o700,0o600)
    _tree(rpath("q1_sources"),0o700,0o600);_tree(rpath("controls"),0o755,0o644)
    if early:_tree(rpath("q1_cartridges"),0o755,0o644)
    else:_tree(rpath("q1_cartridges"),0o750,0o640,None,u2)                         # readable by the QWEN-2 user only
    if early:_tree(rpath("q2_work"),0o700,0o600)
    else:_tree(rpath("q2_work"),0o700,0o600,u2,u2)                                 # QWEN-2 private (evaluation text, heat maps)
    if early:_tree(rpath("master_bundle"),0o700,0o600)
    elif phase=="QWEN2":_tree(rpath("master_bundle"),0o755,0o644,u2,u2)          # QWEN-2 exports MASTER_02 here
    else:_tree(rpath("master_bundle"),0o755,0o444)                                # immutable for QWEN-3 and CONTROLS
    if phase=="QWEN3":_tree(rpath("q3_out"),0o755,0o644,u3,u3)
    elif early or phase=="QWEN2":_tree(rpath("q3_out"),0o700,0o600)
    else:_tree(rpath("q3_out"),0o700,0o600,u3,u3)
    pm={n:_mode(rpath(n)) for n in FOLDERS};ISO["perm_maps"][phase]=pm
    dump_json(DATA_DIR/"PERMISSION_MAPS.json",ISO["perm_maps"]);slog("PERMISSIONS",phase,**{n:f"{v['owner']}:{v['group']} {v['mode']}" for n,v in pm.items() if v})
    return pm
def stage_isolation():
    if SIM and os.environ.get("AKB782_SIM_NO_USERS")=="1":ISO["mode"]="PY_AUDIT_ONLY";ISO["notes"].append("simulation without OS users")
    elif os.geteuid()!=0:ISO["mode"]="PY_AUDIT_ONLY";ISO["notes"].append("the notebook does not run as root — separate users cannot be created")
    else:
        try:
            if _run(["getent","group",HF_GROUP]).returncode!=0:
                r=_run(["groupadd",HF_GROUP])
                if r.returncode!=0:raise RuntimeError("groupadd: "+r.stderr.strip()[:160])
            for s,u in USERS.items():pw=_ensure_user(u);ISO["users"][s]=dict(user=u,uid=pw.pw_uid,gid=pw.pw_gid,home=pw.pw_dir)
            for u in USERS.values():_run(["usermod","-aG",HF_GROUP,u])
            ISO["mode"]="OS_USERS"
        except Exception as ex:ISO["mode"]="PY_AUDIT_ONLY";ISO["notes"].append(f"OS users not available: {type(ex).__name__}: {ex}")
    ISO["setpriv"]=shutil.which("setpriv") is not None
    r=_run(["unshare","--net","--","true"]);ISO["netns"]=(r.returncode==0)
    if not ISO["netns"]:ISO["notes"].append("network namespace not available in this runtime ("+(r.stderr.strip()[:120] or f"rc {r.returncode}")+") — QWEN-2/3 run with HF offline mode only")
    apply_permissions("PREFLIGHT")
    # barrier probes with the exact launch commands of QWEN-2 and QWEN-3 (probe files only; removed afterwards)
    pf={"q1_sources":rpath("q1_sources")/"__probe__.txt","q1_cartridges":rpath("q1_cartridges")/"__probe__.bin","q2_work":rpath("q2_work")/"__probe__.txt","panel":rpath("panel")/"__probe__.txt"}
    for k,p in pf.items():p.write_bytes(b"probe")
    _tree(rpath("q1_cartridges"),0o750,0o640,None,USERS["QWEN2"] if ISO["mode"]=="OS_USERS" else None)
    if ISO["mode"]=="OS_USERS":_tree(rpath("q2_work"),0o700,0o600,USERS["QWEN2"],USERS["QWEN2"])
    _tree(rpath("panel"),0o755,0o644)
    for s in ("QWEN2","QWEN3"):ISO["probes"][s]=_probe(s,pf)
    for p in pf.values():
        try:p.unlink()
        except Exception:pass
    apply_permissions("PREFLIGHT")
    exp={"QWEN2":{"q1_sources":"DENIED","q1_cartridges":"READ","q2_work":"READ","panel":"READ"},"QWEN3":{"q1_sources":"DENIED","q1_cartridges":"DENIED","q2_work":"DENIED","panel":"READ"}}
    ok={}
    for s in ("QWEN2","QWEN3"):
        pr=ISO["probes"][s];cuda_ok=bool(pr.get("cuda")) and pr.get("devices")==1 and pr.get("cuda_alloc",True)
        if ISO["mode"]=="OS_USERS" and not cuda_ok:
            ISO["notes"].append(f"{s}: CUDA not usable as {USERS[s]} ({pr.get('torch_error') or pr}) — this session runs as root with the python audit barrier only")
            ISO.setdefault("root_fallback",[]).append(s)
        ok[s]=all(pr.get(k)==v for k,v in exp[s].items()) if ISO["mode"]=="OS_USERS" else None
    ISO["os_barrier_ok"]=ok
    if ISO["mode"]=="OS_USERS" and not all(ok.values()):raise RuntimeError(f"OS permission probes differ from the design: {ISO['probes']}")
    dump_json(DATA_DIR/"ISOLATION_SETUP.json",ISO)
    return (f"mode {ISO['mode']} · users {', '.join(v['user']+' uid '+str(v['uid']) for v in ISO['users'].values()) or '—'} · network namespace {'yes' if ISO['netns'] else 'no'} · "
            f"probes QWEN-2 {ISO['probes'].get('QWEN2',{}).get('q1_sources')} sources / QWEN-3 {ISO['probes'].get('QWEN3',{}).get('q1_cartridges')} source cartridges · "
            f"CUDA as user: {', '.join(s+' '+str(ISO['probes'][s].get('cuda')) for s in ('QWEN2','QWEN3'))}"+(f" · notes: {'; '.join(ISO['notes'])}" if ISO["notes"] else ""))
def hf_cache_permissions():
    """after QWEN-1: the downloaded model files become readable (not the rest of /root) for the session users"""
    if ISO["mode"]!="OS_USERS":return "not needed (sessions run as root)"
    hh=hf_home();done=[]
    for p in [Path("/root"),Path("/root/.cache")]:
        try:
            if str(hh).startswith(str(p)+"/"):os.chmod(p,stat.S_IMODE(os.stat(p).st_mode)|0o001);done.append(f"{p} o+x")
        except Exception:pass
    gid0=grp.getgrnam(HF_GROUP).gr_gid
    for p in [hh,hh/"hub"]:
        try:os.chown(p,0,gid0);os.chmod(p,0o2775);done.append(f"{p} root:{HF_GROUP} 2775")
        except Exception:pass
    md=model_cache_dir()
    if md.exists():
        gid=grp.getgrnam(HF_GROUP).gr_gid
        for q in [md]+list(md.rglob("*")):
            try:
                os.chown(q,0,gid,follow_symlinks=False)
                if not q.is_symlink():os.chmod(q,(0o2775 if q.is_dir() else 0o664))
            except Exception:pass
        done.append(f"{md} group {HF_GROUP} rw, others r")
    lk=hh/"hub"/".locks"/md.name
    if lk.exists():_tree(lk,0o2775,0o664,None,HF_GROUP)
    return " · ".join(done)

# ---------------------------------------------------------------------------------------------------------------------
# THE SESSION PROCESSES — 782.py (locked) as its own OS process per session; every line is received, time-stamped,
# written to ENGINE_OUTPUT_REALTIME.log and drives the stage display. Progress bars update ONE line (no flooding).
# ---------------------------------------------------------------------------------------------------------------------
PROGRESS={"line":"","t":0.0};PROC={"p":None};LAST_OUT={"t":time.time()}
OUTDIRS={"PREFLIGHT":"preflight","QWEN1":"q1_sources","QWEN2":"q2_work","QWEN3":"q3_out","CONTROLS":"controls"}
def results_of(session):return jload(rpath(OUTDIRS[session])/f"TEST782_{session}_results.json",{}) or {}
PROG_RX=re.compile(r"\d+%\|?|it/s\]|s/it\]|B/s\]|\d+/\d+ \[")
def _on_line(line,stream,session):
    u=utc_now();LAST_OUT["t"]=time.time()
    with _LOG_LOCK:
        LINES.append((u,session,stream,line))
        new=not ENGINE_OUT.exists()
        with ENGINE_OUT.open("a",encoding="utf-8") as f:f.write(f"{u}\t{session}\t{stream}\t{line}\n")
        if new:_private(ENGINE_OUT)
    if PROG_RX.search(line) and not re.search(r"^(PASS|FAIL|DIAG) [A-Z]",line):
        PROGRESS["line"]=short(line,160)
        if time.time()-PROGRESS["t"]>1.0:PROGRESS["t"]=time.time();_emit(f"{SNAME[session]} · {PROGRESS['line']}",progress=True)
        STATE["stages"][session]["note"]=f"{SNAME[session]} process: "+PROGRESS["line"];bump()
        return
    _emit(f"  {SNAME[session]:<9}| {line[:300]}")
    m=re.match(r"^(PASS|FAIL|DIAG) ([A-Z][A-Za-z0-9_.]+) ?(.*)$",line)
    if m:
        CHECKS.append(dict(utc=u,session=session,name=m.group(2),result=m.group(1),passed=(m.group(1)!="FAIL"),detail=m.group(3).strip()[:600]))
        if m.group(1)=="FAIL":slog("ENGINE_FAIL",f"{session} {m.group(2)}",detail=m.group(3)[:500])
        if m.group(1)=="PASS":STATE["stages"][session]["note"]=f"PASS {m.group(2)}";bump()
    m=re.match(r"^STEP (.*)$",line)
    if m:STATE["stages"][session]["note"]=m.group(1);bump()
    for kind,rx in (("COMMIT",r"^PHYSICAL_COMMIT "),("GENERATION",r"^GENERATION "),("TEXT",r"^TEXT_WRITTEN "),("PARITY",r"LAYER_PARITY"),("COMPLETED",r"^SESSION_COMPLETED"),("FAILED",r"^SESSION_FAILED")):
        if re.search(rx,line):slog("ENGINE_"+kind,f"{session} {line[:380]}")
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
    """nvidia-smi every 10 s while a session runs (kept in memory and in GPU_SAMPLES.json — not printed)"""
    while True:
        used,total=gpu_used_mib();apps=nvsmi("compute-apps=pid,used_memory")
        GPU_SAMPLES.append(dict(utc=utc_now(),t=time.time(),session=session,used_mib=used,total_mib=total,apps=apps))
        if stop.wait(10):break
def _heartbeat(stop,session):
    t0=time.perf_counter()
    while not stop.wait(30):
        STATE["elapsed"]=round(time.perf_counter()-t0);bump()
        if time.time()-LAST_OUT["t"]>300:
            LAST_OUT["t"]=time.time();slog("SESSION_ALIVE",f"{SNAME[session]} still working · {(time.perf_counter()-t0)/60:.0f} min · last progress: {PROGRESS['line'][:100] or '—'}")
def gpu_release_check(session,pid,timeout=120):
    """after a session process has exited: no compute process left, GPU memory back to idle"""
    if SIM:return dict(released=True,used_mib=0,apps=[],waited_s=0,note="SIMULATION — no GPU")
    t0=time.time()
    while True:
        used,total=gpu_used_mib();apps=nvsmi("compute-apps=pid,used_memory")
        if (used is not None and used<=1024 and not apps) or time.time()-t0>timeout:break
        time.sleep(3)
    return dict(released=bool(used is not None and used<=1024 and not apps),used_mib=used,total_mib=total,apps=apps,waited_s=round(time.time()-t0,1))
def run_session(session):
    """starts ONE engine session as its own OS process (after the previous one has ended) and follows it until it exits"""
    prev=[s for s in LEDGER.values() if s.get("end") is None]
    if prev:raise RuntimeError(f"a previous session is still running: {prev}")
    apply_permissions(session)
    cmd,user=launch_cmd(session,force_root=(session in ISO.get("root_fallback",[])))
    env=session_env(session,user)
    if SIM and os.environ.get("AKB782_SIM_PYTHONPATH"):env["PYTHONPATH"]=os.environ["AKB782_SIM_PYTHONPATH"]
    cwd=env.get("HOME") if user else str(RUN_ROOT)
    slog("SESSION_START",f"{SNAME[session]} · {' '.join(cmd[:8])} …",user=user or "root",netns=("--net" in cmd),offline=env.get("HF_HUB_OFFLINE")=="1")
    t0=time.time();rec=LEDGER[session]=dict(session=session,cmd=cmd,user=user or "root",uid=(pwd.getpwnam(user).pw_uid if user else os.geteuid()),start=utc_now(),start_t=t0,end=None,
                                          netns=("--net" in cmd),offline=env.get("HF_HUB_OFFLINE")=="1")
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=cwd,env=env,bufsize=0,preexec_fn=_preexec(user))
    PROC["p"]=p;rec["launcher_pid"]=p.pid;stop=threading.Event()
    th=[threading.Thread(target=_reader,args=(p.stdout,"stdout",session),daemon=True),threading.Thread(target=_reader,args=(p.stderr,"stderr",session),daemon=True),
        threading.Thread(target=_sampler,args=(stop,session),daemon=True),threading.Thread(target=_heartbeat,args=(stop,session),daemon=True)]
    for t in th:t.start()
    rc=p.wait();th[0].join(60);th[1].join(60);stop.set()
    if PROG_OPEN["open"]:_emit("")
    res=results_of(session)
    rec.update(end=utc_now(),end_t=time.time(),seconds=round(time.time()-t0,1),exit_code=rc,engine_pid=res.get("pid"),engine_ppid=res.get("ppid"),engine_uid=res.get("uid"),
               engine_user=res.get("user"),status=res.get("status"),error=res.get("error"))
    samp=[s for s in GPU_SAMPLES if s["session"]==session and s["used_mib"] is not None]
    rec["gpu_peak_used_mib"]=max([s["used_mib"] for s in samp],default=None)
    rec["gpu_release"]=gpu_release_check(session,rec.get("engine_pid"))
    GPU_SAMPLES.append(dict(utc=utc_now(),t=time.time(),session=session+"_released",used_mib=rec["gpu_release"].get("used_mib"),total_mib=rec["gpu_release"].get("total_mib"),apps=rec["gpu_release"].get("apps")))
    slog("SESSION_EXIT",f"{SNAME[session]} exit code {rc} · {rec['seconds']:.0f} s · GPU released {rec['gpu_release']['released']}",engine_pid=rec.get("engine_pid"),user=rec.get("engine_user"),
         gpu_after_mib=rec["gpu_release"].get("used_mib"))
    dump_json(DATA_DIR/"PROCESS_LEDGER.json",LEDGER);dump_json(DATA_DIR/"GPU_SAMPLES.json",GPU_SAMPLES)
    if rc!=0 or res.get("status")!="COMPLETE":
        failed=next((l for _,s,_,l in reversed(LINES) if s==session and (l.startswith("FAIL ") or l.startswith("SESSION_FAILED"))),None)
        raise RuntimeError(f"{SNAME[session]} ended with exit code {rc}: {failed or res.get('error') or 'no result file'}")
    if not rec["gpu_release"]["released"]:raise RuntimeError(f"GPU not released after {SNAME[session]}: {rec['gpu_release']}")
    return rec
def stage_session(session):
    rec=run_session(session);r=results_of(session);s=r.get("summary") or {}
    extra=""
    if session=="QWEN1":
        extra=f" · HF cache for the session users: {hf_cache_permissions()}"
        c=s.get("cartridges") or {};extra=" · "+" · ".join(f"{k} {v.get('body_tokens')} tok SHA {str(v.get('sha256'))[:10]}…" for k,v in c.items())+extra
    if session=="QWEN2":extra=f" · MASTER_02 {str(s.get('master_sha256'))[:12]}… · {s.get('tokens')} tokens · parity {s.get('parity')} · second reload {s.get('second_reload')} · naive one-pass {s.get('naive_one_pass')} (negative control)"
    if session=="QWEN3":extra=f" · parity {s.get('parity')} in a new process · expression {s.get('expression_tokens')} tokens · OS isolation {s.get('os_level_isolation')}"
    if session=="CONTROLS":extra=f" · {s.get('answers')} answers in 4 conditions"
    if session=="PREFLIGHT":extra=f" · SHA scenarios {s.get('sha_scenarios')} · AST missing names {s.get('ast_missing')} · panel {str(s.get('panel_sha256'))[:12]}…"
    return f"pid {rec.get('engine_pid')} · user {rec.get('engine_user')} · exit {rec['exit_code']} · {rec['seconds']:.0f} s · GPU after exit {rec['gpu_release'].get('used_mib')} MiB"+extra
_AKB782_PARTS={1}
# ===== END OF PART 1/4 =====
# ===== PART 2/4 — paste directly after PART 1 in the same cell =====
# =====================================================================================================================
# PART 2 / 4 — byte-exact embedded copies of the locked engine sources 730 · 757 · 764 · 779 · LICENSE (zlib + base64; 709 is in
#              PART 4). Generated by the build — do not edit. A copy is used only if its git blob equals the lock in PART 1.
# THIS PART  70,190 characters · its last line is  # ===== END OF PART 2/4 =====
# =====================================================================================================================
EMBEDDED.update({
 "730.py":(  # 28554 bytes · git blob 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"
 ),
 "757.py":(  # 21624 bytes · git blob 3d88bf8638390995858f23391f1e043faa586835
  "eNrVPNt220aS7/wKTPvBQARCV9+oQWZoCZY4lkiapOxkGC4WBJskQhCAcdElis7Zj9gv3C/ZqurGjaQcJ/u0PolEAt3V1dV1r2q9UNof37eHZ72BpQw7V52z"
  "Xle57PT7vbP2df9mqPzPf/23MrKGozevjhsvlF7Amy73feUs9J2pwu+5m6VeGBjKhzj8jQfKpzseHBmvmm+O3ivdDye60j48OFDeHly8N2D6uRdzN1WCbM1j"
  "z3UAzM3oWFlnfuo1XSdOY2+24Mo8SwDkqdLtKSm/T5trPvOclM+U5CFIlzzxEoQ1DLPY5QoPFl7AW4ofuisYQqgeHyh7tQcH7+ABfTp8jXO7vZFy0b+R+MOo"
  "6YPiZOkyjA1lkAVKFIezzOWJ4qWJEt4Fypo7SRbDQD9c7P9r2OsaDW8dhXGqOEmqK0snWfreVFd+TcJAV8JEV1JvzeFn7Lh86rgrXcliH4YYMf+acZyzcHUl"
  "hiGxE8zCdWMeh2slclKEo0jYffjaaAysfs9kyzSNktb+fuzcGQsvXWbTLOGxGwYpD1LDDdf7LoeT8Y6P91MvdYKmGy4CL/Vu4cDCmDdvj/fXjhfss8ZV7+wj"
  "kMhk08OpM3vHp8fTw8PD6cnJyeHx/C2fH7xyjp3DkwNn+vq18+bNbCanHLwz2Wv33fytO50ecs5nb0/ezk5eHR4fz94czw9mb16/eT19/Za/Ozx6JaccvjbZ"
  "O4DqvHFO3r06nB8dvDmazU+m/IhPT2DcAXfevuZz59XJmzesMeNzZc5Td2mLs1MDB2jI7yPgGT7TWg0F/t3B3jdoacDXMOKBuvF4IH6rSMA9grXkzozHifnI"
  "boB4zfYCaMdarJCApuR09qTpeIBhlpqApQanrMzF+vgPzsCcwzLOTD05wH8avZr64dSUrGAkS+dQnTJ8prC9JI1VHzCEmZpm8MANZ1zV9qbslwO2hw+NJb+f"
  "eQtEVwDz5gTvb2a+/xYs6yUc+RNRs+I4jNU5QzrbH9qdqxsQ4Efc5VNLecSpT8rfTOUxn/7EBNyYp1kc4BYaIAgdwWhAeQ+ZJQyA3ecKCJly6/jejKQuF6l1"
  "mIax8qUzuuzdjHLRDxb5+5eJgmvFgBswZAMWQCarnSeDJ0b0wHTJghqNAr7aGHXwrhx18E6MAlbaGAWiXIw6fK01ElIIuKhY25hxIjPL0nnzLWx/7cQrHpvs"
  "lyCNH1q/BCjM6kvz5Q+HhwcaawDFxQglCFPFC5QC4E7SM7lv2/rJAjXW6XXt972b7nl78LN9dtnuXljnsGYUA2nvzQKUkUS+l6piIf1QGx9MGkhKFSQ48nyu"
  "igk6ksqGjzwGZuF25YBo0wznME1fwDk7fqJqGhzmCI4tjD3Qh6BZ81MT8KRGSRRQNuK0pXIThzrNgAdCeIQ790NnRiywBur5RgMhmezNK5DQQa83MlErqWxf"
  "qp79QnhsITxvGPJufRADnr/3khQQVbgPlGT76TraMVVr9AfW507vZmh/z1onf32tE1jrQ/vq6n0b5Od71jr+62sdw1q4hLFezbxYjRw41DQxR3GG6g3m2+GK"
  "vmmgNi9MHLrPJEkMYFJ2Co+Nu9hLuY0WUWUAEISwPhLYJQFLmhhohFjjrD0Y2eedgRwULR8SNLl2YWcTdpqPkYht4AIHcW51z6wKlIQ7Pp/Zgp0BQHXIbiDX"
  "7W7nA3JQHde1E3hzVNIC2QGo5BS+shYO0FmSOmmWgGoejgBFkCSduUvuruDReKIz2ABwPX1GpcYEPjZqPXj6iMLDWlLJ6KhP5LeDdzrqDfnt8PWTmL7mYPpn"
  "sNrlccU3cWYzoGiCKm5PmUnPxUGLKtwWJwKbMyu8lSAEnZHymLyV+EFITxMsDI/rzgsTi/reGuw0iTRshKE7Ig6QhHAVoNsx5XOw3UqcBQGgISZu/GNdgZLE"
  "BhgzCUlzA2DFExINdtADfQ5Mp6Sh4sRTD/wSQNHxF3wKqs0FPwumxXIvu9cZcKA6BzDK1wxsQ/pAuiThcJIpQHBcNwNnB54Cwl4w44gOroj2hKA3kTyLGGfK"
  "s9y5Tj9EyYLzRdUFeHq4daIHcB54h2jd4TBwZ+AZrsNYIkIs0HSmvtg6Smgc+s8schGHWTBrpjE4fcoidma4BmCKbkQTEQeArod4zHFvQXIHbkO5dHV/Mb/1"
  "+B2bPAGr/2R3rS/mydvG2eVN9yO4Dm8bcK72wBpag8+WfdF5b74zDmjgsHczALkZ9T5a3aF5DE5Eo9+xyievX4lx9HBo962BnGK+aox6ffsj/Mb3H26G1nk+"
  "CQwZwBla1rmJ/rpwLY0EfDUVH+ZGIgGDkNsHcpHI8OPBzYUXL/lO0BSOFradkPUhx5sYGc98GfozcJHAbQ24j8xWcvuU++EdHUzMI99BX7r0E8Bz8puRA85C"
  "ubzR+HQDA9CMDq2ROZ40Gv1217qy3/8ME01UE8YsW0eJWh2nA2eBX247cFqe+QGUAteB1VJ7xR+kgk046FsHrFxiqqBGdBDzigsmFxletque29Gr12pl9bp3"
  "pgpNNrTaV0D5HJuh0GSaVNPTB1BnNRiNwZgRoWyxAJuYxdqNxLlFZF4obYitREhTc8qQkIVpl6weFwI5zwJXjAMvgg5xnVPbKJ28jYBIqjIpQsD4gkg6ih04"
  "x7coEegh8HsHFJ9YM496Ss9EFR4coS400DpLUgVik8p5i7DvLEuPddJHEgV4swzDldH4JyzsLo0gtFEUgQ4YCQj8bKHXbKF/VYGt7kY6eNSemyIthaFp5V4z"
  "OW+gtcGEIH5yhg9GSQMSKuiFi2fa38zuFT5yggf1Htm3GwLZgfOVe3T/5Kiq27/tBPa+dIEJ3h7YV+2fQUSvrese+H8D69NNZ0AOIE4EMQlM0H5yYfD54D/k"
  "s4iPm0cTMegrjXCjMQvYpNkvooCvfzefcUCt6/7oZ7vd71vdfKVpOHswEcaSTcYtvd/SWxN68UKx6Byj2ANNHINsoilPcklfAoPhgbuOi07kHYhxsvQiNBfn"
  "DxBUeO4ZvjEIFs0055nv26tbG7/lFEV8y4MRLhESNacCOO+gSM00i/z8ZMYtMKZ7h5IIGZx2bBIW9jTz/FkOmd7i0Xh4NKDYFlztXmkteUpjb2IWCy1ciId9"
  "H/lFK2PGkglV4diKn77zAHsdAxLgV3jBrzCG6YLbTaQmxX5TcphKTkBEkrTE5ED/qpPKr3AL/lubay9Q6Y3+tQkcWHsrdVcchmt1vffq8Kj+WixqhPN5wlMz"
  "SWsvozAxhdQ4AgXkMQgzdfl7b63PwDDBJs6tz3W4GNTS3lUviLI0sfl6ymc5uN94HCaqeqiv9UutAkOfpQ8RfBr93Le0XTaVsHISUr02aCVQ7CYd53ODnZQM"
  "fRiAM5is5PJwhrR6sY0dOIiRfhgsnkckFPbK9mBj8MXIggRMDf8NzkrTBX/lY/D9c3BAj9k0WtgSETyDMnJT6d7WBhPzAnmNDTrURgHh8QgEp4IgBibqJggK"
  "vDhRCYSmSZHtC03MKRrjpfwqJEZNYl0FQCSGMuAR2C/0vMAEkMMEBhD5VIICCB4Ethxs8hQcxCzlBY1g9mdCU7putw5418JVHIR9Cw04gAaYxi4hJOmtsH24"
  "0sNbs5B1EMzi1Uq/Jd1EL0A/VV6BspmD24Bm/8/KGFgHkrKvYBL2xIA6u/uzLWHpo6T092Dqs1ICpPq2jH1rstyOIYyXKijI1RWoZFDKAKIlFm9NdIGeLpbT"
  "SjDEGqjWVIGC66TqOFxN9iRsfeatzebRTgkoZ6jhrX4rVkVToOWzCutSauu6dvN0VQ1WenCr6epqqd8uNQ2PglN4BB6e+psXqYSjTuZA2zgVAA22QfpMgdh4"
  "C+mGWPzNXC3R8FZG3G6OuF22tna2MwHWH3R6heGViRdpjR+9POsF6KDhJ4TJ7u+2qMKZFpPPejfdkZyOMit0WcHY1WQagW2Q14LJE/sWIsi5B0636+VpS445"
  "JxN/ejwZw3PB6KmJqxsAeW67EJJA/ChtlhuZiTPnNgJUabaGcixBg2h7PlfAddSVMnHeOdfJU3TAibw83v/4OY/r0MWkfXjJyl6DI7xj1Waq/UDhw7fxWoBI"
  "2IsoA09FPJDMls0cA0JcdxmHgfcbl6OXR7PvWg8J7EY1muqPLEkkLR8ACGtRzKbKPejHms4E+PyN+AYvnsRZkANhi5hWBUOg+w6EJc94junBs1sGF4Oci9Mk"
  "5VECOuoUNDH4pvgpDVPHt9NwBYQ2Je3ih7oswWmj7AAGdZaWs6pMMWboc0h4bLIpUtXV9uQvtY9vAMfCgyW360D7cTM83BYoTICy4cdOX4yw39+cX1gjJgmF"
  "3Ls1BeNqL8h47QX442uMRtzE3BaA+p6fpXJlm5XNbOMMmlJYTAqOHB+YzRaxArLkhocFlNgN4bnoYiO0KD/WASNLAJgtwy55eEMR75aNEhZRbswEpyJDT0zB"
  "0d+SG+Dz3WCA5gAAfu5+LRzmgsXyuGR3UFIYNOT83JxJUJoUg/zx9llXudUUvxtb7NdtjzqfLWRUiulHVr/CfzlblYA32GOXFu/2cnMwtK6ss1ERh1XUCx61"
  "QF+nvemC4DvpXZCa37s8SkuGwhMHQBXYPkc7r9VDRqGNRBIJ1RGnqEbPUx9SAcn8feA/FEkRrEOuIwxnSY+0u8Mv1qDTvVDaH0bWoJKqFJxjSDjdEDCZY/zj"
  "YTUSM8YotuAP8MApn2UwsZqx1NEkX7eHCDrmmMYofD5JNLGFOvJic3EW2E68FhU7VLVFXucvqdv60Qg9nphb+pxW2xTRmvpF38QWMa4pGZ/cFdxD5ZTAhd50"
  "Pb+iyi520fqTSgwrhNsHPmY5QLYhX+TESzl6ZCDALRiMcqyXU1q1+c9FLJjdhNXBJjp3OpM4lDbyDzTKH0DNU1ct+I2ZnyKNpj1p25ItRVqwLROnlW8LXOJY"
  "VEOLeZQUVpkU3Ztu7ssRs9uf2jYTRdzGpkFaY0FFnmvlwPWtA9eqasAN45n5yIBrWYvgMsF0rCWZjxH3wV6JCZnkQtaSH7ZJxYTCK2j9rDLJz4VG3u2ClKfV"
  "sQRy06Va0rmNeR6QfrvTPbfws9Ud2Vgts76wpwLEYJxXRyZl+IF71U5lknFDE4q3IrTD9KL/8D0KjqRell2A/GmiouOiR4XD61FGYSUeOzMgWMRdr/SVKFer"
  "GZSCwCh93NrKiguBdJdZsALxxDFey9urZsknm9HogY5uPgzV9Oo4bVKNAgRE4R9tpde/ne4b9cC2tLs/2/32YDQEjoxyoyepKWA38u4QUNHRA2aQgkh0eMjE"
  "FCVr5ZgzwRyN6945ZoNF8v710cHR60b35hpDmk53aJ40Br2bkWV/NI+38/7HrzDt377uX1m0FdqV+erwqPECMwPUzeJNIWBIitz9HLgcIv82MaJyWyYARNGg"
  "6YfhCvMIZIqBRV8oWQDHT8n9NCxqM/AtyqZ+AbARBwtT1h0G9Est96U12lf9y/Z7a2Sy9vuzc+vDxeW/Pl5dd/ufBsPRzecvP/38b9EGEkYOqLq8GB6YbyVX"
  "SSqL53usyfZevjR+DSH8h3UNdxlCOK7mi2jEHXbJHYEmU8thvCbHcabe1wEHkeEkThw7D+q9zDbBozk4tenxkbYPn9fOvbfO1mrBJvDMR7lZGAhW/TYEHWYn"
  "ZvNQX3EeQSwuahSafsibbwVulOYReSMQ3CQCRuGFhyByuGsndZdwNrpIbAahkmRTNIOYwI3BmKeG0gezjtn7JItJGeG7CMsEmZMWroJj5isYOD1SNdGe4GN7"
  "gIq9CSgym2NkpZsVIAxYXo3Zf6j/aAm99kvyQwv+15jOmO7oc99ZJDiuo+Uwal6FfMiU/zRe/sJOW0wzKNiWhYCCZ20qn6iSGi4oIgrGIP4FXfP4tDNFXAhQ"
  "JT8BoJMwMCWPMRCYYa/LtNO7MF4VT7/0Bh/hWcqddfFsZLWv4dmtk/lp8fBz++ZqVHEwXyidSnUwL7srkcddDgJnQWz0IL5RLAUylCgYtZFwodOHLqBRgHPM"
  "OXsUGD8piGFiO6nyiJ+eDFYMm+IwekgqxpmGmKVJbOKQR9xFdbSLo+khiDzw0i2MBJo90s6qA1GLj+fs7NFrHRzNnuw20yvf3te+nbHJZtirp/eUwcNkETps"
  "qqNPdVfTWnRmFPGaMKTEC8+07gfN2Se5AHCToANrid86ww2zFv7UGW6HtfDnc06MtLqsRdsE+w5chk0xrIW4PTep9L/mbJiCqUNRIl2eH4sO2/Wx3Jkfj47p"
  "1mD7IOTzCskN5cvSIQcfU7xkfxViKAX9qn+g8oZ4gA6RIoMyEVyOIr/9pvux2/vSRXnlt94MS3MIFZgrm889KmUb7KluqpDYOp1E46w9tIb6WXsAJsX6aWRu"
  "yRyWEQPXz2ZcSe9CMl1JQial9PSVu6XnLpVkGWb+LF9FImY0kCV+LSXzSArkYhkm6ZYs0itCapMbrh9/3eQGApEzA0aFOTPQ58Y3GIFJ7FiVGcY7fetv8QEh"
  "8P+KDeq1dkFbN484fH7LfSDO6HJgWfZlr0+dT/C6oNFE2oDrznAIHul2j0WFWm41ankSmgHZgE538lyR/5ERe7KW4ExGbIrfJIc+bZb5txsBdhb5MXCpVeXr"
  "1Xx69X+q5MM7rNrg4dqL0PHhJTtuLsNIHliu5uGEwfPGTC3xEHiN1PFDXhQ1E+Uhet7jksrwmzqLGa6zIMtuUxOLnYAXjz1CsJz1U/tsxPKegt3VdTgSCI1k"
  "3mwjE5GY7O+/e2s7QS7//UfsM/4lYHv5qD32S0DvQSx//1F+lmMdUApYeE9hQi0MSL4nBpB2PQLFwYuA/LuLt3Ii06WPHWIhWcCq1qfq1U/bKyqfIleuYqAx"
  "qVZ29LIIKBpMnq8CVmt7uUdZ+pplWSbHi8ox1AQqPERwwNwog58UN2BXp/BXRaLHBs25Kg5Ln8I3ubGv5u7zlIhgV1nVQULLPEUZRBAGMPk6USskSgCpr/+c"
  "lnU7qq8d6fBc5gcPK+mLNIzQw8UgkMqJKgzTmyvh6cLeWvClNamEkIiNMP1izwDAWHMnUOUM8UWr2SoUdo6RLE4G5/nB9J31dObgVlpqswKUstaaLp4I8q2d"
  "Fa+0PeZbFb2ziky/69RdFhfFGniUk0y82ehQJB5iLRHcdM6B/TJ4B5yo13VDq1ANdSXJKn2Y1NNY72EE8a49mGycHkTVokWZ6FKoxfwwK6dZ3JQg1bLVnof1"
  "ogAUPhjnkMI5L8AeQQULvmDdCyyNmk/4ZyL7RqVKkHA3MWETiyJnj65XLXOMdyDMvDF1H7PKe8yI0oqHDVuMRLcuttXjeA2GpOuoOoZkjVQgLIsz0JdfR4Zs"
  "RxPTiuHclDYQaMuwtAY+JgwwRGKokvWy59SkjZNr58mE9sBTh3GYhHIjrEfotYJOq8hO1ObSkGpqDR+UuTXAiCgGxAsDtIJIxTLjU60fmWVdRnDtuMpnRUao"
  "orKcNFyDakGTp+a9ulIWykGiTiRMpMzX4wkNOucXFqM8PR/nVJrU1aEbndbT4jLN1766KmEMGeVt5E400yzjth+OtWo1DzVWLsD4eUOtiRo1QWlV+G6jlJpT"
  "q8T0vmiaOhCV8t36uJSBe1PE/UmEzCTSTvcaBPaoKjczMfKtVuYDQMhen5TgcCfi/KqpibF3P9GMkeGGtbW3a6U4XWbk8K7PrJ6KF37+xjWa51PY4OrVKpXS"
  "fGxl+De9xj/2+AiRyVZBoGRFkRQ1Hx0BswW/MZUtsnwOxQ5C0Rf5U6kW63W+Ao6bwxF1CwoHashpG8g9ya4cZ1b6H/UR9UtAcqWxXKi0chGmYSjNZ9YSOs6d"
  "VumUMSvDins+28Di8K6eqP5aI3zCfZoowliGMEF7FZA3fHO2CH14v7UaGLAwRieLtUKIpvMSwlOlIQWpUuSUw7tN9UBJapnmL5Drt4dDCh/ClYwZ8K4SxFt9"
  "GkxlgBLXjfoDu+hd5YO2EJYOwsBIeAqsjyG9ygT/M308wZsZKWIq8BaDKxnwonUD30o/AU06aNk0izZ8BFDfOiD8ofOT3u+cD/W+TmP17pV+qX+61D9+vtQv"
  "z2U7xMpsZ2k4Qo0Pchwb6N/bZb5ULVwGcNwTbKVdhxBmoK6XppPgiOVM9WXVvU4eEjBivwQva2R6eZPwMi50bh0P4k2w3bPQzfAyVh5CICfnz5pktLG5vezA"
  "VjbAdupB5NqjyxA6UPGhCOu3cHkuMhBRRKf7oTe4bmPo2YKpcqtAUvIoJIm/16fom6hXcbbsoM0g8DDfe2nSDmbvMWw7C4O5t1CpJ8EL7JOpJzx2fRpM6ZtN"
  "c2xSyyyYn7BvFMBIUefzsOqUwbFVuiJLoBgwzMIMzkDAr+g54htikGv89CGMz5wscfyr6y0+KTApGIaAeb9R/AgY4N5MelZtzpShi712ItAarHXwpFcE9Q78"
  "kswGhgAknYVsa3yGEXUnTQPbW0c+R5ahZU2WzCIH7z2BRlPLtlxw/6lnmsIybLhfczAp6GvDFyO/OEERqK1W2NydL0Q4Zoj90MPuFZ3sdqSnnV6KLun5wlh6"
  "M2BNOwEZE6A+le/AXNtleyne+oSpIKS1AUV/phxAQC7PacyCw3bBuYSxOsPXEO2tmY4WhLrIL/f3P13W/BlxSO3B2SXT1bpeAH/G+qlPjQhbr2owPgx6/7a6"
  "THd8X8U29i3SfZvUdWDdD8DN2NpebYbXgT0TcPkpqWEEgXEFrObEyLXCFq5L0PAz87mAixdHxM0tuhDuAP8G4TrMMGEVc075DallgH0hmgCWxqsH7VThDuYE"
  "Ux6RdupCkCKSD9ihmme8iHgvh2g2bz2ECkE0iJcuIxMcgmYLpyBUedec0DxVxJ20MtNOqSJKochLW47r8iTBqlURJ1E/ViDvMBgN7DoZmirLM3d43WwzawfP"
  "Khk7CDU+drrnOEnmLHVRMtBFlUAv6gL1sp28H0S+GtDEzrWvClvT89yQvoIIrV6YUufshq6ifVPF65g7FJc36SoDJpzulrBL5RHgPymspt3mTJI/yabY944X"
  "oIoqxGP+6QmbiwmHXvfq58qVkEfE8olyj8YGZNYRl4gJAVjEmSaApL6ZE2YiF4UXqW2CiQ5SdfPoGex2oMCjoJdmkcJtlbXBmSyX4U0l575JpnEBB2lga4zo"
  "F/Ag3hGpJWQsvJaiYFMZkoBuPudOpLFRdpyJipiBtx+oDqfCF564TsRVQnwvZs1xu/nvyePbJ6bjjLxg1ul+bl91zplwNgoxUWWzE3iX5FVQXof6DVEPgMIG"
  "HnT93DeQta8sxiukJk4a53nwySn9tYGq3wpiqQOCvqDpdgMv8b1OjDw+bE2qaQPM+IpVcJpayZTn+9BaUzi5VTHjq1nnaDldL9av9XChlTHZh5urK1Zvrnmh"
  "5DcafT+/4IccQheTMAiEQ0KPhC79LR08EseNQxBwUT2q961J39iUiZI8wiyDZ79EhiT1fAMdzLmh10OeZWLWU3EiB7d7RTlx3JIKYLJzzd6gfXZlbZHg3HMW"
  "QZhgoZ5KocoUU70kgad4KSGRF0RlRl5c3YlnSuf8OQIIVikz+GPgjRb8v3dIRd7N14Jnx1Wkk93ddpIx7NGg/Rk0YfvKRm3OaqeNxizHpLXVKFXw1mklHioe"
  "7iTbDr4p4zGVriZRx1X9bCrgd+mcxvNto9RSU8TAc/ZIQvtE7YqPREUQ9nyH3/Ih86iZyL3V4PX0jeg43yOhUomAsXFThMl/aa+kM8oiG+yFCbaAGFBaAFSt"
  "PlbIyEoA8lKwn6uYlgFpQZHqJsvg8lkIJfLfiGTL4XlsaOPWWIvs0mZ0CgeF93DRJuulxpVnIDZcN2FF72h5rs8ErZUWNqmXy5dlX5VZqFPRhUSEB9fwmDRZ"
  "/lL+6Qm10LJ6bj5q8iANkqiS2ZschULCWmRMGC3DWvRLrxGWsNrYtEgOCFiySDrBPzbh4LmLbZgbbzey2iGGCykXqc5ij0+NRtGXSeeRe5N0v1/5XcHz+dIZ"
  "Wkr7ZtTr9q57N0Ole3NtDTpnysAaDToWkEPZV4SLTBfwWc3dPbs5bzO90nDtgSOX+0lq3TXudS37on9TGy6jJsqFqYDyYT1beXhwYONfMarNgSjBlvOiGG/Q"
  "pmBb1APNEI2Awnj9aL45+OHohx+OD2oQi7IA8NfSUb9RhiTxFVVIDRArJlYCyjxpIQpm3Fss0yRve0XPyxM1fBq/WQwpU6nVDGsV1fft7kf7rIc5zZElMrVk"
  "9zbTtJVLa5gzAf8PqOLyWRYLa032Ob9xCpGJwJ2MO16aaxTti9IzQqKmITjibAKRLA6mv5RAul/PrbUuTah93mlfdHvDUeeswpSFDoOZwtlhcYhx+4rldrkc"
  "K2poWFJmLRnPXVhda9CGdWw0vWV2gAmnDMZVjHH1Ik6iC8PdFIZ7VthzcQO6DKAqMGWzLsWlELRNPfwrC7CE/PsENvqxleFJGkZ2nBEWed0fu58C4cDOMZOc"
  "VseLehLWlSHEsYvwh7XItXzK6Z9TvaxuI4NWavPPnNFGRb4sv2/l3kgD9Ae9Ue+sd2X38c8jINszfdfqMseQm/Q/7gzfcPV0Yhh5I4DppVGt39NB+OJic61t"
  "OF9XqzbY4uJ34AkBaTa6xl1xB1M0N9RdCIqugR5Cve9mYqZt31Z5oVyLxJuUnyXQEcMVwYG5B0heoUgCIuh9AdjYgrbleYoCILDkpgfY2nnTJ89Hl+ELOEMI"
  "8cl+JAgvvdnLCThD9Xhm+x5RjYw7s8qFC1tvW66Z9dLpvBi0wesUK1Zs4U6XocxKw4Jjad4mtfz0M/NK+08zK+Z0AoxWSVfTa7Kmk+0W9wpDln3u2LdQ7WQv"
  "OVLfzZES7s6m7XzQM1dTJB5frM7F5WhYxaG0FqZZNyT15FIPnanO+Q1Q/rLX+zhkOvLQM70Zhg0A7iA+sfHvPdBfs6jQ97smAqXFZKlMsvXaiR+q1b8/I1vi"
  "wsd9+bceatyIjHE/Fl7UxKT0ZKWyQ7emb3l9PgKU03KPbGJQ5jvBJIPKPjGthBHwhfMXYFxXYUgKjAk7MI85XrZ01uC9el/ydrFKgf/zdz1KWOTHCFfue+bl"
  "+/ojHIr9fw+sCg7fMw9ceeHEieWp8jqWXrCs9xXU1gqbJ6mJtk58Kl6IP0Q1MVnuANm5q2rLitdO65b/nat8FvBhxYLKRXY1rVVgfOhcYWUcmxyAlTX6cNW7"
  "EB/yWj1MENfSFIt+Ye7OwRSd29regzUY9AbsFJ5xDN7xnqGorbna6UBSCf9aJbwoPhvCkYAzddWqJT+t7VNA1utAtFNx/62moiSl/hdWp0zQ"
 ),
 "764.py":(  # 34856 bytes · git blob 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"
  "snxEd8uVcmaIxNT/BXg1I6A="
 ),
 "779.py":(  # 47254 bytes · git blob fa7017a87f25ecef6ed2b2954a850599cb25fcd9
  "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"
 ),
 "LICENSE":(  # 4525 bytes · git blob 9aad4724d1072f9e56486650a9527380c867a53b
  "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"
 ),
})
_AKB782_PARTS.add(2)
# ===== END OF PART 2/4 =====
# ===== PART 3/4 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 4 — independent read-only verification, observational measures, twelve scientific figures from THIS RUN's
#              outputs (JPEG 300 dpi, layout QC; heat maps; the QWEN-3 expression printed verbatim), records and the single
#              RUN pipeline. Every number comes from this RUN's files; a missing output is drawn as missing.
# THIS PART  62,232 characters · its last line is  # ===== END OF PART 3/4 =====
# =====================================================================================================================
# ---------------------------------------------------------------------------------------------------------------------
# canonical manifest helpers (identical rules to 782.py) and the locked seal function (730.py, executed from its AST)
# ---------------------------------------------------------------------------------------------------------------------
HEX64=re.compile(r"^[0-9a-f]{64}$")
def canonical_seal(s):
    if not isinstance(s,dict) or set(s)!={"h","lower"}:raise ValueError("TENSOR_SHA_KEYS")
    return {"h":s["h"],"lower":[(x[0],x[1]) for x in s["lower"]]}
def canonical_entry(e):
    e=dict(e);e["tensor_sha"]=canonical_seal(e["tensor_sha"])
    if "native_layer_seals" in e:e["native_layer_seals"]=[(x[0],x[1]) for x in e["native_layer_seals"]]
    return e
def tensor_meta(cp):
    def m(t):return {"shape":list(t.shape),"dtype":str(t.dtype),"contiguous":bool(t.is_contiguous()) if hasattr(t,"is_contiguous") else None}
    return {"h":m(cp["h"]),"lower":[{"layer":i,"k":m(k),"v":m(v)} for i,(k,v) in enumerate(cp["lower"])],"layer_order":list(range(len(cp["lower"]))),
            "byteorder":sys.byteorder,"n":int(cp["n"]),"p":int(cp["p"]),"body_tokens":int(cp["body_tokens"]),"book_id":str(cp["book_id"])}
def meta_sha(meta):return sha_bytes(json.dumps(meta,sort_keys=True,separators=(",",":")).encode())
_SEAL_NS={}
def host_seal_cp(cp):
    if "seal_cp" not in _SEAL_NS:
        import torch
        src=RAW["730.py"].decode("utf-8");t=ast.parse(src);fn=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=="seal_cp")
        _SEAL_NS.update(torch=torch,sha=lambda b:hashlib.sha256(b).hexdigest());exec(compile(ast.Module(body=[fn],type_ignores=[]),"730.py","exec"),_SEAL_NS)
    return _SEAL_NS["seal_cp"](cp)
def manifests():
    q1=jload(rpath("q1_cartridges")/"Q1_CARTRIDGE_MANIFEST.json",{}) or {};q2=jload(rpath("q2_work")/"Q2_MANIFEST.json",{}) or {}
    bm=jload(rpath("master_bundle")/"MASTER_MANIFEST.json",{}) or {};rd=jload(rpath("master_bundle")/"READY.json",{}) or {}
    return q1,q2,bm,rd
def text_file(session,name):return tload(rpath(OUTDIRS[session])/name)
def panel():return jload(rpath("panel")/"SEALED_PANEL.json",{}) or {}
def panel_seal():return jload(rpath("panel")/"PANEL_SEAL.json",{}) or {}
def checks_of(session):return (results_of(session).get("checks") or [])
def chk(session,name):
    c=[x for x in checks_of(session) if x["name"]==name];return None if not c else all(x["pass"] for x in c)
def chk_detail(session,name):
    c=[x for x in checks_of(session) if x["name"]==name];return c[-1]["detail"] if c else None

# ---------------------------------------------------------------------------------------------------------------------
# observational measures (no semantic grade): source-specific vocabulary in every answer — computed OUTSIDE QWEN-3
# ---------------------------------------------------------------------------------------------------------------------
STOP=set("""about above after again against also although among another around because been before being below between both
could does doing down during each either else every from further have having here however into itself just least less made
make many more most much must neither never none only other others ought over same shall should since some such than that
their theirs them themselves then there these they this those through thus under until upon very what when where whether which
while whom whose will with within without would your yours document documents memory unknown information answer question
state states stated title publisher http https www html""".split())
def terms(t):return {w for w in re.findall(r"[a-z][a-z\-]{4,}",str(t or "").lower()) if w not in STOP}
ARMS=("NO_MEMORY","SOURCE_A_ONLY","SOURCE_B_ONLY","BASELINE_MASTER")
def control_metrics():
    A=tload(rpath("q1_sources")/"SOURCE_A_BODY_FORGED.txt");B=tload(rpath("q1_sources")/"SOURCE_B_BODY_FORGED.txt");pn=panel()
    if not A or not B or not pn:return None
    qt=terms(" ".join(q["question"] for q in pn["questions"])+" "+pn.get("qwen2_evaluation_prompt",""))
    TA,TB=terms(A),terms(B);SA=TA-TB-qt;SB=TB-TA-qt;SH=(TA&TB)-qt
    rows={};q3=results_of("QWEN3").get("answers") or [];ct=results_of("CONTROLS").get("answers") or []
    def cov(ans):
        t=terms(ans);return dict(a_hits=len(t&SA),b_hits=len(t&SB),shared_hits=len(t&SH),a_pct=round(100*len(t&SA)/max(len(SA),1),1),b_pct=round(100*len(t&SB)/max(len(SB),1),1),
                                 unknown=bool(re.match(r"^\W*UNKNOWN\b",str(ans or "").strip().upper())),chars=len(str(ans or "")))
    for a in ct:rows.setdefault(a["arm"],{})[a["id"]]=cov(a["answer"])
    for a in q3:rows.setdefault("QWEN3_BLIND",{})[a["id"]]=cov(a["answer"])
    q0=next((a["answer"] for a in q3 if a["id"]=="Q0"),None);c0=next((a["answer"] for a in ct if a["arm"]=="BASELINE_MASTER" and a["id"]=="Q0"),None)
    rep=dict(qwen3_q0_equals_controls_master_q0=(q0==c0) if (q0 is not None and c0 is not None) else None,
             qwen3_vs_controls_master_similarity=round(difflib.SequenceMatcher(None,(q0 or "").split(),(c0 or "").split(),autojunk=False).ratio(),4) if q0 and c0 else None)
    return dict(vocabulary=dict(a_specific=len(SA),b_specific=len(SB),shared=len(SH),question_terms_excluded=len(qt)),rows=rows,reproduction=rep,
                note="lexical proxy: distinct words (≥5 letters, stop-words removed) that occur only in SOURCE_A or only in SOURCE_B, counted in each answer; NOT a semantic grade")

# ---------------------------------------------------------------------------------------------------------------------
# VERIFY — independent, read-only
# ---------------------------------------------------------------------------------------------------------------------
def _load_cp(p):
    import torch
    return torch.load(p,map_location="cpu",weights_only=True)
def _equal(a,b):
    import torch
    return a.shape==b.shape and bool(torch.equal(a,b))
def _h3_map(cp,cols=600,cbins=64):
    """|H3| mean per (channel bin × token column) — CPU, float32"""
    h=cp["h"][0].float().numpy() if hasattr(cp["h"][0].float(),"numpy") else np.asarray(cp["h"][0].float())
    n,Hd=h.shape;cb=max(1,Hd//cbins);a=np.abs(h[:, :cb*cbins]).reshape(n,cbins,cb).mean(-1)
    edges=np.linspace(0,n,min(cols,n)+1).astype(int);out=np.stack([a[s:e].mean(0) for s,e in zip(edges[:-1],edges[1:]) if e>s],1)
    return out,edges,Hd
def _kv_norms(cp,cols=600):
    rows=[];labels=[]
    for i,(k,v) in enumerate(cp["lower"]):
        for nm,t in (("K",k),("V",v)):
            x=t[0].float().numpy() if hasattr(t[0].float(),"numpy") else np.asarray(t[0].float());x=np.sqrt((x**2).sum(axis=(0,2)))
            edges=np.linspace(0,len(x),min(cols,len(x))+1).astype(int);rows.append([x[s:e].mean() for s,e in zip(edges[:-1],edges[1:]) if e>s]);labels.append(f"L{i} {nm}")
    return np.array(rows,np.float32),labels
def stage_verify():
    q1,q2,bm,rd=manifests()
    if not q1.get("cartridges"):raise RuntimeError("no QWEN-1 cartridge manifest in this RUN — nothing to verify (nothing is substituted)")
    V=dict(cartridges=OrderedDict(),master={},ledger={},isolation={},texts={},problems=[],utc=utc_now());probs=V["problems"]
    E1={k:canonical_entry(v) for k,v in q1["cartridges"].items()}
    locs=[("SOURCE_A","q1_cartridges",E1.get("SOURCE_A")),("SOURCE_B","q1_cartridges",E1.get("SOURCE_B"))]
    if q2.get("cartridges"):
        E2={k:canonical_entry(v) for k,v in q2["cartridges"].items()}
        locs+=[("SOURCE_A","q2_work/cartridges",E2.get("SOURCE_A")),("SOURCE_B","q2_work/cartridges",E2.get("SOURCE_B")),("MASTER_02","q2_work/cartridges",E2.get("MASTER_02"))]
    if bm.get("master"):locs.append(("MASTER_02","master_bundle",canonical_entry(bm["master"])))
    cps={}
    for cid,where,e in locs:
        if not e:continue
        p=RUN_ROOT/where/e["file"];row=dict(id=cid,where=where,present=p.is_file())
        if p.is_file():
            t=time.perf_counter();s=sha_file(p);row.update(bytes=p.stat().st_size,sha256_now=s,sha256_manifest=e["sha256"],file_sha_ok=(s==e["sha256"]),hash_s=round(time.perf_counter()-t,2))
            cp=_load_cp(p);seal=host_seal_cp(cp);row["tensor_seal_ok"]=(seal==e["tensor_sha"]);mt=tensor_meta(cp)
            row.update(meta_sha_ok=(meta_sha(mt)==e.get("tensor_meta_sha256")),n=int(cp["n"]),p=int(cp["p"]),h_shape=list(cp["h"].shape),h_dtype=str(cp["h"].dtype),
                       k_shape=list(cp["lower"][0][0].shape),book_id_ok=(cp["book_id"]==cid),full_80_layer_kv_bytes=int(cp["n"])*80*8*128*2*2)
            cps[(cid,where)]=cp
        V["cartridges"][f"{cid}@{where}"]=row
        for k in ("file_sha_ok","tensor_seal_ok","meta_sha_ok","book_id_ok"):
            if k in row and not row[k]:probs.append(f"{cid}@{where} {k}")
        slog("VERIFIED_CARTRIDGE",f"{cid} @ {where}",**{k:v for k,v in row.items() if k in("file_sha_ok","tensor_seal_ok","meta_sha_ok","bytes","sha256_now")})
    if bm.get("master") and ("MASTER_02","master_bundle") in cps:
        M=cps[("MASTER_02","master_bundle")];A=cps.get(("SOURCE_A","q1_cartridges"));B=cps.get(("SOURCE_B","q1_cartridges"));me=canonical_entry(bm["master"])
        import torch
        P_=int(M["p"]);nA=int(A["body_tokens"]);n=int(M["n"])
        mm=V["master"]
        mm["parents_link_ok"]=[p["id"] for p in me["parents"]]==["SOURCE_A","SOURCE_B"] and all(p["sha256"]==E1[p["id"]]["sha256"]==sha_file(rpath("q1_cartridges")/E1[p["id"]]["file"]) for p in me["parents"])
        mm["h3_exact_concat"]=_equal(M["h"],torch.cat((A["h"],B["h"][:,P_:,:]),dim=1))
        mm["lower_A_part_exact"]=all(_equal(M["lower"][i][j][:,:,:P_+nA,:],A["lower"][i][j]) for i in range(4) for j in (0,1))
        mm["lower_B_values_exact"]=all(_equal(M["lower"][i][1][:,:,P_+nA:,:],B["lower"][i][1][:,:,P_:,:]) for i in range(4))
        mm["lower_B_keys_equal_unrotated"]=all(_equal(M["lower"][i][0][:,:,P_+nA:,:],B["lower"][i][0][:,:,P_:,:]) for i in range(4))
        mm["bundle_files"]=sorted(x.name for x in rpath("master_bundle").iterdir());mm["bundle_only_master"]=mm["bundle_files"]==["MASTER_02.pt","MASTER_MANIFEST.json","READY.json"]
        mm["bundle_manifest_sha_ok"]=sha_file(rpath("master_bundle")/"MASTER_MANIFEST.json")==rd.get("manifest_sha256")
        mm["bundle_has_no_text"]=not any(k in json.dumps(bm) for k in ("text_sha256","body_sha256")) and not list(rpath("master_bundle").glob("*.txt"))
        mm.update(n=n,P=P_,nA=nA,nB=int(B["body_tokens"]),boundary=P_+nA,schedule=me.get("rebuild_schedule"),sha256=me["sha256"],h3_seal=me["tensor_sha"]["h"])
        for k in ("parents_link_ok","h3_exact_concat","lower_A_part_exact","lower_B_values_exact","bundle_only_master","bundle_manifest_sha_ok","bundle_has_no_text"):
            if not mm.get(k):probs.append("MASTER "+k)
        hm,he,Hd=_h3_map(M);kv,kvl=_kv_norms(M);ha,_,_=_h3_map(A,cols=300);hb,_,_=_h3_map(B,cols=300)
        np.savez_compressed(DATA_DIR/"MASTER_ANATOMY.npz",h3=hm,h3_edges=he,kv=kv,kv_labels=np.array(kvl),src_a=ha,src_b=hb,P=P_,boundary=P_+nA,n=n,hidden=Hd);_private(DATA_DIR/"MASTER_ANATOMY.npz")
        slog("MASTER_VERIFIED","H3 = A ⊕ B exactly" if mm["h3_exact_concat"] else "H3 MISMATCH",**{k:v for k,v in mm.items() if isinstance(v,bool)})
    cps.clear();gc.collect()
    # process ledger: strictly sequential, exit 0, GPU released, same frozen weights in every session
    L=V["ledger"];ss=[LEDGER[s] for s in ENGINE_STAGES if s in LEDGER]
    L["sequential"]=all(ss[i]["start_t"]>=ss[i-1]["end_t"] for i in range(1,len(ss)));L["exit_codes"]={s["session"]:s["exit_code"] for s in ss}
    L["gpu_released"]={s["session"]:s["gpu_release"]["released"] for s in ss};L["pids"]={s["session"]:s.get("engine_pid") for s in ss}
    L["distinct_pids"]=len({s.get("engine_pid") for s in ss})==len(ss);L["users"]={s["session"]:s.get("engine_user") for s in ss}
    sent={s:results_of(s).get("weights_sentinel") for s in ("QWEN1","QWEN2","QWEN3","CONTROLS") if results_of(s).get("weights_sentinel")}
    L["weights_sentinel"]=sent;L["weights_identical_across_sessions"]=len(set(sent.values()))==1 if sent else None
    com={s:(results_of(s).get("model") or {}).get("commit") for s in ("QWEN1","QWEN2","QWEN3","CONTROLS") if results_of(s).get("model")}
    L["model_commit"]=com;L["model_commit_identical"]=len(set(com.values()))==1 if com else None
    for k in ("sequential","distinct_pids"):
        if not L[k]:probs.append("LEDGER "+k)
    if L["weights_identical_across_sessions"] is False:probs.append("LEDGER weights differ between sessions")
    # QWEN-3 access record
    r3=results_of("QWEN3");au=r3.get("access_audit") or {}
    I=V["isolation"];I.update(mode=ISO.get("mode"),netns=ISO.get("netns"),qwen3_os_level=r3.get("os_level_isolation"),qwen3_probe=r3.get("access_probe"),
                              qwen3_violations=au.get("violations"),qwen3_folders_opened=au.get("opened_under_root"),qwen3_forbidden=au.get("forbidden"),
                              qwen2_violations=(results_of("QWEN2").get("access_audit") or {}).get("violations"),root_fallback=ISO.get("root_fallback",[]))
    if r3 and (au.get("violations") or any(any(f.startswith(x) for x in ("q1_sources","q1_cartridges","q2_work")) for f in (au.get("files_under_root") or []))):probs.append("QWEN-3 opened a forbidden path")
    # texts written by the sessions: file SHA-256 = result record
    for s,key in (("QWEN3","answers"),("CONTROLS","answers")):
        for a in results_of(s).get(key) or []:
            t=text_file(s,a["file"]);ok=(t is not None and sha_text(t)==a["sha256"]);V["texts"][f"{s}/{a['file']}"]=ok
            if not ok:probs.append(f"text {s}/{a['file']}")
    cm=control_metrics()
    if cm:LIVE["metrics"]=cm;dump_json(DATA_DIR/"CONTROL_METRICS.json",cm)
    LIVE["verification"]=V;dump_json(VERIFY_FILE,V)
    n_ok=sum(1 for r in V["cartridges"].values() if r.get("file_sha_ok") and r.get("tensor_seal_ok") and r.get("meta_sha_ok"))
    mtxt=(f"MASTER = H3(A) ⊕ H3(B) exactly: {V['master'].get('h3_exact_concat')} · parents {V['master'].get('parents_link_ok')}" if V["master"] else
          "PARTIAL — no MASTER_02 bundle in this RUN, only the cartridges present were verified")
    note=(f"{n_ok}/{len(V['cartridges'])} cartridge files: file SHA-256 + locked tensor seals + tensor-meta seal equal to the manifests · {mtxt} · "
          f"sessions sequential {L['sequential']} · weights identical {L['weights_identical_across_sessions']} · "+(f"QWEN-3 forbidden opens {len(au.get('violations') or [])}" if r3 else "QWEN-3 did not run"))
    if probs:raise RuntimeError(note+" · PROBLEMS: "+", ".join(probs))
    return note
# ===== figures follow =====
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.linewidth":.9,"axes.edgecolor":NEU,"axes.labelcolor":INK,"xtick.color":NEU,"ytick.color":NEU,
                     "xtick.labelsize":8.5,"ytick.labelsize":8.5,"axes.labelsize":9.5,"axes.titlesize":10.5,"axes.titleweight":"bold","axes.titlelocation":"left",
                     "legend.fontsize":8.5,"legend.frameon":False})
FW,FH=13.333,7.5;OUT_DPI=300;MONO="DejaVu Sans Mono"
FIGURES=OrderedDict([
    ("F1",dict(n=1,title="Three Isolated Sessions — Architecture",slug="THREE_SESSION_ARCHITECTURE",tab="OVERVIEW")),
    ("F2",dict(n=2,title="QWEN-1 — Real Sources into Physical Cartridges",slug="QWEN1_SOURCE_CARTRIDGES",tab="SOURCES · QWEN-1")),
    ("F3",dict(n=3,title="MASTER_02 — Anatomy of the Physical Cartridge",slug="MASTER_CARTRIDGE_ANATOMY",tab="MASTER · QWEN-2")),
    ("F4",dict(n=4,title="Native Numerical Fusion — Layer × Token Heat Map",slug="NATIVE_FUSION_HEATMAP",tab="MASTER · QWEN-2")),
    ("F5",dict(n=5,title="Reload Parity — 80 Layers, Three Processes",slug="RELOAD_PARITY_HEATMAP",tab="MASTER · QWEN-2")),
    ("F6",dict(n=6,title="SHA-256 and Manifest Integrity Chain",slug="SHA_MANIFEST_INTEGRITY",tab="INTEGRITY")),
    ("F7",dict(n=7,title="QWEN-3 — The MASTER in Human Language (verbatim)",slug="QWEN3_EXPRESSION_VERBATIM",tab="BLIND READING · QWEN-3")),
    ("F8",dict(n=8,title="QWEN-3 — Question Panel and Attention on the MASTER",slug="QWEN3_PANEL_AND_ATTENTION",tab="BLIND READING · QWEN-3")),
    ("F9",dict(n=9,title="Control Conditions — What Each Memory Contributes",slug="CONTROL_CONDITIONS",tab="CONTROLS")),
    ("F10",dict(n=10,title="Process Isolation and GPU Release",slug="PROCESS_ISOLATION_GPU",tab="ISOLATION")),
    ("F11",dict(n=11,title="Timing and Memory Measurements",slug="TIMING_AND_MEMORY",tab="RESOURCES")),
    ("F12",dict(n=12,title="What This Run Shows — Claims Ledger",slug="CLAIMS_LEDGER",tab="OVERVIEW"))])
BASE_FIGURES=OrderedDict(FIGURES)
FIG_FILES={};FIG_ERRORS={};PROVENANCE={}
BADGE_COL={"SCHEMATIC":NEU,"LIVE MEASUREMENT":OK_COL,"SEALED MEMORY":COL["M"],"OBSERVATIONAL":AMBER,"VERIFICATION RECORD":NEU,"NOT PRODUCED IN THIS RUN":RED}
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
    T(fig,.035,.022,f"{APP_NAME} · {EXPERIMENT} · demo {CODE_VERSION} · {_date()} · 782.py git blob {LOCKS[ENGINE_NAME][:10]} · run {SESSION_ID}"+(" · SIMULATION" if SIM else "")+f" · Figure {meta['n']}/{len(BASE_FIGURES)}",
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
    stem=("SIMULATION_" if SIM else "")+f"TEST782_FIG{num:02d}_{meta['slug']}{suffix}";jpg=FIG_DIR/(stem+".jpg")
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
    fig_footer(fig,key,"Placeholder by design: TEST782 figures are drawn only from outputs of this RUN (no earlier run, no representative values).")
    return save_fig(fig,key,"NOT PRODUCED IN THIS RUN",["(none — output missing)"],"_NOT_PRODUCED")
def _axstyle(ax,fs=8):
    for s in ("top","right"):ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=fs)
def _t(u):
    try:return datetime.fromisoformat(u).timestamp()
    except Exception:return None
def heat(ax,M,exact=None,vmin=1e-4,vmax=1.0,cmap="magma_r",extent=None,label=None):
    """log-scale heat map; cells that are bit-identical are drawn in a separate green, never as small numbers"""
    Mp=np.array(M,dtype=np.float64);Mp=np.where(Mp<=0,np.nan,Mp);Mp=np.clip(Mp,vmin,vmax)
    im=ax.imshow(Mp,aspect="auto",origin="lower",cmap=cmap,norm=LogNorm(vmin=vmin,vmax=vmax),interpolation="nearest",extent=extent)
    Z=np.zeros_like(M,dtype=float)
    if exact is not None:Z=np.where(np.asarray(exact),1.0,np.nan)
    else:Z=np.where(np.asarray(M)==0,1.0,np.nan)
    ax.imshow(Z,aspect="auto",origin="lower",cmap=ListedColormap(["#A7F3D0"]),vmin=0,vmax=1,interpolation="nearest",extent=extent)
    return im
EXACT_GREEN="#A7F3D0"
# ===== figure functions =====
def _res(s,k,default=None):return (results_of(s).get(k) if results_of(s) else None) or default
def fig1():
    k="F1"
    if not LEDGER.get("QWEN1"):return fig_missing(k,"The architecture is drawn from the session processes of this RUN.","No engine session ran in this RUN.")
    fig=fig_base(k,"Five OS processes, strictly one after the other — only the files named on the arrows cross a session boundary · values measured in this RUN","SCHEMATIC")
    lanes=[("PREFLIGHT","CPU gate",["AST dependency scan","16 SHA / manifest simulations","tokenizer types · GPU budget","seals the question panel"]),
           ("QWEN1","source session",["reads: 2 web documents","forges SOURCE_A, SOURCE_B","H3 + K/V L0–L3 → SSD","SHA-256 file + tensors"]),
           ("QWEN2","consolidation session",["reads: 2 cartridges only","native numerical fusion","MASTER_02 → SSD, sealed","80/80 layer parity"]),
           ("QWEN3","blind reading session",["reads: MASTER_02 only","no source text / cartridge","80/80 independent reload","expresses it in language"]),
           ("CONTROLS","control session",["NO_MEMORY · A_ONLY","B_ONLY · BASELINE_MASTER","same sealed questions","(separate process)"])]
    W=.172;G=.0195;x0=.035
    for i,(s,role,lines) in enumerate(lanes):
        x=x0+i*(W+G);c=SCOL[s];L=LEDGER.get(s) or {}
        box(fig,x,.47,W,.37,ec=c,lw=1.6);rect(fig,x,.84-.034,W,.034,c,z=2)
        Tc(fig,x+.004,x+W-.004,.823,f"{SNAME[s]} · {role}",size=9.6,weight="bold",color="white")
        info=[f"pid {L.get('engine_pid','—')} · user {L.get('engine_user','—')}",f"{str(L.get('start',''))[11:19]} → {str(L.get('end',''))[11:19]} UTC",
              f"exit {L.get('exit_code','—')} · {L.get('seconds',0) or 0:.0f} s",f"GPU after exit {((L.get('gpu_release') or {}).get('used_mib','—'))} MiB",
              ("network: namespace" if L.get("netns") else ("network: offline mode" if L.get("offline") else "network: online"))]
        for j,t in enumerate(info):Tc(fig,x+.006,x+W-.006,.785-j*.027,t,size=7.6,color=INK2,mono=(j<2))
        hline(fig,x+.008,x+W-.008,.648,RULE)
        for j,t in enumerate(lines):Tc(fig,x+.006,x+W-.006,.622-j*.034,t,size=8.0,color=INK)
    cross=[(0,"sealed question panel (SHA)"),(1,"SOURCE_A.pt · SOURCE_B.pt · manifest (no text)"),(2,"MASTER_02.pt · restricted manifest"),(3,"MASTER_02.pt (read-only)")]
    for i,lab in cross:
        xa=x0+(i+1)*(W+G)-G;arrow(fig,xa+.001,.66,xa+G-.001,.66,col=SCOL[ENGINE_STAGES[i+1]],lw=1.6,ms=10)
    for i,lab in cross:
        xa=x0+(i+1)*(W+G)-G/2;Tc(fig,xa-.085,xa+.085,.445,("↑ crosses: "+lab) if i<3 else "↑ MASTER read by CONTROLS too",size=7.0,color=MUTED)
    ss=[LEDGER[s] for s in ENGINE_STAGES if s in LEDGER and LEDGER[s].get("end_t")]
    if ss:
        t0=ss[0]["start_t"];t1=ss[-1]["end_t"];span=max(t1-t0,1);X0,X1=.08,.955
        T(fig,.035,.375,"time line of this RUN — processes never overlap; the GPU is checked empty after every exit",size=8.6,weight="bold",color=INK2)
        hline(fig,X0,X1,.315,NEU,1.0)
        for s in ss:
            a=X0+(s["start_t"]-t0)/span*(X1-X0);b=X0+(s["end_t"]-t0)/span*(X1-X0);rect(fig,a,.295,max(b-a,.002),.04,SCOL[s["session"]],z=2)
        for j,s in enumerate(ss):
            a=X0+(s["start_t"]-t0)/span*(X1-X0);b=X0+(s["end_t"]-t0)/span*(X1-X0)
            T(fig,.035,.255-j*.028,f"{SNAME[s['session']]:<9}",size=7.6,weight="bold",color=SCOL[s["session"]],mono=True)
            T(fig,.105,.255-j*.028,f"{(s['start_t']-t0)/60:6.1f} → {(s['end_t']-t0)/60:6.1f} min  ·  {s['seconds']/60:5.1f} min  ·  GPU released {okm((s.get('gpu_release') or {}).get('released'))}",size=7.4,color=INK2,mono=True,xmax=.55)
        T(fig,X0,.348,"0 min",size=7.2,color=MUTED);T(fig,X1,.348,f"{span/60:.0f} min",size=7.2,color=MUTED,ha="right")
    sen=(LIVE.get("verification") or {}).get("ledger",{})
    box(fig,.585,.095,.38,.17,ec=NEU,fc=PANEL,lw=1.1)
    T(fig,.595,.24,"Frozen Qwen2.5-72B-Instruct · NF4 · BF16 · CUT3 — one model, four loads",size=8.8,weight="bold",xmax=.96)
    T(fig,.595,.21,f"weights sentinel identical in all GPU sessions: {okm(sen.get('weights_identical_across_sessions'))}",size=7.8,color=INK2,xmax=.96)
    T(fig,.595,.185,f"model snapshot identical: {okm(sen.get('model_commit_identical'))} · isolation mode: {ISO.get('mode')}",size=7.8,color=INK2,xmax=.96)
    T(fig,.595,.16,"no GPU state, KV cache, Python object or text crosses a boundary —",size=7.8,color=INK2,xmax=.96)
    T(fig,.595,.135,"only the SSD files named on the arrows (each SHA-256 verified on arrival)",size=7.8,color=INK2,xmax=.96)
    T(fig,.595,.11,"QWEN-2/QWEN-3: own Linux users · source folders unreadable to them",size=7.8,color=AMBER,xmax=.96)
    fig_footer(fig,k,"PIDs, users, times, exit codes and GPU memory after exit: PROCESS_LEDGER.json (host) and each session's results file. Arrows = the only files a later session may read.")
    return save_fig(fig,k,"SCHEMATIC",["PROCESS_LEDGER.json","GPU_SAMPLES.json","TEST782_<SESSION>_results.json","POST_RUN_VERIFICATION.json"])
def fig2():
    k="F2";r1=results_of("QWEN1");q1,_,_,_=manifests();E=q1.get("cartridges") or {}
    if not E or not r1.get("sources"):return fig_missing(k,"The source cartridges are drawn from QWEN-1's records of this RUN.","QWEN-1 did not complete.")
    fig=fig_base(k,"Each document is read ONCE, by QWEN-1 only, and written into the model's own internal states — the text never leaves QWEN-1's private folder","LIVE MEASUREMENT")
    V=(LIVE.get("verification") or {}).get("cartridges") or {};tm=r1.get("timings") or {}
    try:Z=np.load(DATA_DIR/"MASTER_ANATOMY.npz",allow_pickle=False)
    except Exception:Z=None
    for i,cid in enumerate(("SOURCE_A","SOURCE_B")):
        s=r1["sources"][cid];e=E[cid];v=V.get(f"{cid}@q1_cartridges") or {};x=.035+i*.475;w=.455;c=COL["A" if i==0 else "B"]
        box(fig,x,.40,w,.46,ec=c,lw=1.6);rect(fig,x,.86-.034,w,.034,c,z=2)
        T(fig,x+.01,.843,f"{cid} · {SRC_LABEL[cid]}",size=9.4,weight="bold",color="white",xmax=x+w-.01)
        rows=[("page title",short(s.get("title") or "—",70)),("URL",short(s.get("url"),70)),("retrieved",f"{str(s.get('retrieved_utc',''))[:19]} UTC · {s.get('mode')} · HTTP {s.get('http_status','—')}"),
              ("HTML SHA-256",k_sha(s.get("html_sha256"),40)),("text SHA-256",k_sha(s.get("text_sha256"),40)),
              ("tokens",f"{s.get('body_tokens'):,} forged (TEST781 reference {s.get('reference_test781_tokens'):,})"+(" · TRUNCATED" if s.get("truncated") else "")),
              ("H3 tensor",f"{tuple(v.get('h_shape') or [])} {str(v.get('h_dtype','')).replace('torch.','')} · K/V L0–L3 {tuple(v.get('k_shape') or [])}"),
              ("cartridge file",f"{fmt_b(v.get('bytes'))} on SSD · full 80-layer K/V would be {fmt_b(v.get('full_80_layer_kv_bytes'))}"),
              ("file SHA-256",k_sha(e.get("sha256"),40)),("tensor seal H3",k_sha((e.get("tensor_sha") or {}).get("h"),40)),
              ("forge · write+seal",f"{(tm.get('forge_'+cid) or ['—'])[0]} s · {(tm.get('ssd_write_and_seal_'+cid) or ['—'])[0]} s"),
              ("reopen from SSD",f"file {okm(v.get('file_sha_ok'))} · tensors {okm(v.get('tensor_seal_ok'))} · meta {okm(v.get('meta_sha_ok'))} · 80-layer seals recorded")]
        for j,(a,b) in enumerate(rows):
            y=.80-j*.0325;T(fig,x+.01,y,a,size=7.6,weight="bold",color=MUTED);T(fig,x+.115,y,b,size=7.6,color=INK,mono=(("SHA" in a) or a=="tensor seal H3"),xmax=x+w-.008)
        if Z is not None:
            ax=fig.add_axes([x+.035,.12,w-.05,.21]);M=Z["src_a" if i==0 else "src_b"]
            ax.imshow(np.log10(M+1e-6),aspect="auto",origin="lower",cmap="viridis",interpolation="nearest");ax.set_yticks([0,M.shape[0]-1]);ax.set_yticklabels(["0",str(int(Z["hidden"])-1)])
            ax.set_xticks([0,M.shape[1]-1]);ax.set_xticklabels(["token 0",f"token {int(e['n'])-1}"]);ax.set_ylabel("H3 channel",fontsize=8)
            ax.set_title(f"stored H3 of {cid} — log10 |activation| (channel bins × tokens)",fontsize=8.6,color=c);_axstyle(ax,7.5)
    fig_footer(fig,k,"QWEN-1 records (TEST782_QWEN1_results.json, Q1_CARTRIDGE_MANIFEST.json) and the host's read-only re-hash. Source texts stay in QWEN-1's private folder (not redistributed).")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST782_QWEN1_results.json","Q1_CARTRIDGE_MANIFEST.json","POST_RUN_VERIFICATION.json","MASTER_ANATOMY.npz"])
def fig3():
    k="F3";mm=(LIVE.get("verification") or {}).get("master") or {}
    try:Z=np.load(DATA_DIR/"MASTER_ANATOMY.npz",allow_pickle=False)
    except Exception:Z=None
    if not mm or Z is None:return fig_missing(k,"The MASTER anatomy is measured from the MASTER_02 file of this RUN.","MASTER_02 was not produced or not verified in this RUN.")
    fig=fig_base(k,"What MASTER_02 physically contains — measured from the file on the SSD · it is the frozen model's own states of BOTH documents, not a text summary","LIVE MEASUREMENT")
    n=int(Z["n"]);P_=int(Z["P"]);bd=int(Z["boundary"]);he=Z["h3_edges"];cols=Z["h3"].shape[1]
    xb=lambda tok:np.searchsorted(he,tok)-0.5
    T(fig,.07,.866,"H3 (layer-3 output) stored for every token — log10 mean |activation| per channel bin",size=9.2,weight="bold",xmax=.67)
    ax=fig.add_axes([.07,.47,.60,.34]);ax.imshow(np.log10(Z["h3"]+1e-6),aspect="auto",origin="lower",cmap="viridis",interpolation="nearest")
    for t,c in ((P_,"#F59E0B"),(bd,RED)):ax.axvline(xb(t),color=c,lw=1.6,ls="--")
    ax.set_yticks([0,Z["h3"].shape[0]-1]);ax.set_yticklabels(["0",str(int(Z["hidden"])-1)]);ax.set_ylabel("H3 hidden channel",fontsize=8.5);ax.set_xticks([]);_axstyle(ax,7.5)
    ax2=fig.add_axes([.07,.25,.60,.17]);kv=Z["kv"];ax2.imshow(np.log10(kv+1e-6),aspect="auto",origin="lower",cmap="cividis",interpolation="nearest")
    ax2.set_yticks(range(len(Z["kv_labels"])));ax2.set_yticklabels([str(x) for x in Z["kv_labels"]],fontsize=6.6)
    for t,c in ((P_,"#F59E0B"),(bd,RED)):ax2.axvline(xb(t),color=c,lw=1.6,ls="--")
    ax2.set_xticks([0,xb(P_),xb(bd),cols-1]);ax2.set_xticklabels(["0",f"{P_}",f"{bd}",f"{n-1}"],fontsize=7.5);ax2.set_xlabel("token position in MASTER_02",fontsize=8)
    ax2.set_title("K / V of layers 0–3 stored per token — log10 L2 norm",fontsize=9.0);_axstyle(ax2,7.5)
    for a,b,lab,c in ((0,P_,"system prefix",MUTED),(P_,bd,"SOURCE_A body (European Commission)",COL["A"]),(bd,n,"SOURCE_B body (Future of Life Institute)",COL["B"])):
        xa=.07+.60*(np.searchsorted(he,a)/cols);xe=.07+.60*(np.searchsorted(he,b)/cols)
        if xe-xa>.05:Tc(fig,xa+.002,xe-.002,.828,lab,size=8.0,weight="bold",color=c)
    box(fig,.695,.10,.27,.75,ec=COL["M"],lw=1.5)
    T(fig,.705,.825,"MASTER_02 — facts measured from the file",size=9.4,weight="bold",color=COL["M"],xmax=.96)
    facts=[("tokens",f"{n:,} = prefix {P_} + A {mm.get('nA'):,} + B {mm.get('nB'):,}"),("A | B boundary",f"token {bd} (sealed in the manifest)"),
           ("file SHA-256",k_sha(mm.get("sha256"),26)),("tensor seal H3",k_sha(mm.get("h3_seal"),26)),
           ("H3(MASTER) = H3(A) ⊕ H3(B body)","bit-identical "+okm(mm.get("h3_exact_concat"))),("L0–L3 rows of A","bit-identical to SOURCE_A "+okm(mm.get("lower_A_part_exact"))),
           ("L0–L3 values of B","bit-identical to SOURCE_B "+okm(mm.get("lower_B_values_exact"))),("L0–L3 keys of B","re-rotated to new positions (RoPE)"),
           ("layers 4–79","not stored — rebuilt by the frozen model"),("parents","SOURCE_A, SOURCE_B (SHA links "+okm(mm.get("parents_link_ok"))+")")]
    for j,(a,b) in enumerate(facts):
        y=.785-j*.062;T(fig,.705,y,a,size=7.8,weight="bold",color=MUTED,xmax=.96);T(fig,.705,y-.026,b,size=7.8,color=INK,mono=("SHA" in a or "seal" in a),xmax=.96)
    T(fig,.07,.17,"Reading the picture: left of the orange line = the shared system prefix; between the lines = SOURCE_A; right of the red line = SOURCE_B.",size=8.0,color=INK2,xmax=.68)
    T(fig,.07,.14,"Every column is one stretch of tokens; colour = magnitude of the stored internal state. Nothing in the file is text — it is H3 and K/V.",size=8.0,color=INK2,xmax=.68)
    T(fig,.07,.11,"The model reads this file by injecting H3 at layer 3 and recomputing layers 4–79 (Figure 5: bit-identical every time).",size=8.0,color=AMBER,xmax=.68)
    fig_footer(fig,k,"Host, read-only, CPU: torch.load(MASTER_02.pt) → |H3| per channel bin and token bin; L2 norms of K/V L0–L3; equalities checked with torch.equal against SOURCE_A / SOURCE_B files.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["master_bundle/MASTER_02.pt","q1_cartridges/SOURCE_A.pt, SOURCE_B.pt","MASTER_ANATOMY.npz","POST_RUN_VERIFICATION.json"])
def _heatdata():
    try:return np.load(rpath("q2_work")/"HEATMAPS_QWEN2.npz",allow_pickle=False)
    except Exception:return None
def fig4():
    k="F4";Z=_heatdata();r2=results_of("QWEN2")
    if Z is None:return fig_missing(k,"The fusion heat map is measured by QWEN-2 on the fused memory of this RUN.","QWEN-2 heat-map data not produced in this RUN.")
    fig=fig_base(k,"Difference between the fused memory and the two documents mounted ALONE (same positions) — where fusion changed the model's internal states","LIVE MEASUREMENT")
    ed=Z["edges"];n=int(Z["n"]);bd=int(Z["boundary"]);P_=int(Z["P"]);nb=len(ed)-1;bi=np.searchsorted(ed,bd)-0.5
    axes=[]
    for j,(key,lab) in enumerate((("k","KEYS (K)"),("v","VALUES (V)"))):
        ax=fig.add_axes([.065+j*.315,.20,.27,.60]);im=heat(ax,Z["fusion_rel_"+key],Z["fusion_exact_"+key],vmin=1e-3,vmax=2.0)
        ax.axvline(bi,color=RED,lw=1.5,ls="--");ax.axhline(3.5,color="#2563EB",lw=1.2,ls=":")
        ax.set_xticks([0,bi,nb-1]);ax.set_xticklabels(["0",f"A|B {bd}",f"{n-1}"],fontsize=7.5);ax.set_xlabel("token position (bins)",fontsize=8)
        ax.set_yticks([0,4,20,40,60,79]);ax.set_yticklabels(["L0","L4","L20","L40","L60","L79"],fontsize=7.5)
        ax.set_title(f"{lab} — relative L2 difference",fontsize=9.2);_axstyle(ax,7.5);axes.append(ax)
    cax=fig.add_axes([.648,.20,.010,.60]);cb=fig.colorbar(im,cax=cax);cb.ax.tick_params(labelsize=7);cb.set_label("‖fused − alone‖ / ‖alone‖ (log)",fontsize=7.2,labelpad=2)
    s=r2.get("fusion_footprint") or {}
    box(fig,.715,.20,.25,.60,ec=COL["M"],lw=1.4)
    T(fig,.725,.775,"what the heat map shows",size=9.2,weight="bold",color=COL["M"],xmax=.96)
    lines=[(f"green = bit-identical (exactly 0)",OK_COL),(f"SOURCE_A rows, all 80 layers: identical",INK),
           (f"   K {s.get('A_region_exact_layers_K','—')}/80 · V {s.get('A_region_exact_layers_V','—')}/80 layers exact",INK2),
           (f"SOURCE_B rows, layers 0–3: carried as stored",INK),(f"   K {s.get('B_region_exact_layers_K','—')} · V {s.get('B_region_exact_layers_V','—')} layers exact (K re-rotated)",INK2),
           (f"SOURCE_B rows from layer {s.get('B_region_first_divergent_layer','—')} up: recomputed",INK),
           ("   while attending to SOURCE_A → B now carries",INK2),("   the context of A (causal order A → B)",INK2),
           ("This is a measured cross-attention footprint.",AMBER),("It is NOT, by itself, proof of new semantic",AMBER),("synthesis (Figure 12).",AMBER)]
    for j,(t,c) in enumerate(lines):T(fig,.725,.735-j*.045,t,size=7.8,color=c,xmax=.96)
    T(fig,.065,.85,f"reference = SOURCE_A alone (rows 0…{bd-1}) + SOURCE_B alone moved to rows {bd}…{n-1} with the locked RoPE rephase · {nb} token bins × 80 layers · dotted line = CUT3 boundary (L3 | L4)",size=7.8,color=MUTED,xmax=.965)
    fig_footer(fig,k,"QWEN-2 (GPU, in its own process): fused memory = locked TEST757 append; isolated memories = locked initialize_native; values in HEATMAPS_QWEN2.npz (QWEN-2 private folder, read by the host after the run).")
    return save_fig(fig,k,"LIVE MEASUREMENT",["q2_work/HEATMAPS_QWEN2.npz","TEST782_QWEN2_results.json fusion_footprint"])
def fig5():
    k="F5";Z=_heatdata();r2=results_of("QWEN2");r3=results_of("QWEN3");rc=results_of("CONTROLS")
    if Z is None or not r2.get("master_parity"):return fig_missing(k,"Reload parity is measured by QWEN-2 and QWEN-3 in this RUN.","MASTER parity data not produced in this RUN.")
    fig=fig_base(k,"MASTER_02 reloaded from the SSD and rebuilt (layers 4–79) — compared with the native fused memory, layer by layer, bit for bit","VERIFICATION RECORD")
    ed=Z["edges"];nb=len(ed)-1;bd=int(Z["boundary"]);bi=np.searchsorted(ed,bd)-0.5
    pb=np.maximum(Z["parity_boundary_k"],Z["parity_boundary_v"]);pn=np.maximum(Z["parity_naive_k"],Z["parity_naive_v"])
    for j,(M,lab,c) in enumerate(((pb,"sealed boundary-aware reload (the path used)",OK_COL),(pn,"naive one-pass rebuild (negative control)",RED))):
        ax=fig.add_axes([.065+j*.29,.20,.25,.58]);im=heat(ax,M,None,vmin=1e-3,vmax=64,cmap="inferno_r")
        ax.axvline(bi,color=COL["M"],lw=1.3,ls="--");ax.set_xticks([0,bi,nb-1]);ax.set_xticklabels(["0","A|B",f"{int(Z['n'])-1}"],fontsize=7.5)
        ax.set_yticks([0,4,20,40,60,79]);ax.set_yticklabels(["L0","L4","L20","L40","L60","L79"],fontsize=7.5);ax.set_title(lab,fontsize=8.8,color=c);_axstyle(ax,7.5)
        ex=int(Z["boundary_exact_layers"] if j==0 else Z["naive_exact_layers"]);Tc(fig,.065+j*.29,.065+j*.29+.25,.815,f"{ex}/80 layers bit-identical",size=9.4,weight="bold",color=c)
    cax=fig.add_axes([.62,.20,.010,.58]);cb=fig.colorbar(im,cax=cax);cb.ax.tick_params(labelsize=7);cb.set_label("max |Δ| per cell (log) · green = 0",fontsize=7.5)
    box(fig,.675,.12,.29,.70,ec=NEU,lw=1.3);T(fig,.685,.795,"80-layer parity in every process",size=9.2,weight="bold",xmax=.96)
    L3=LEDGER.get("QWEN3") or {};LC=LEDGER.get("CONTROLS") or {};L2=LEDGER.get("QWEN2") or {}
    def pc(r,name):
        d=next((c["detail"] for c in (r.get("checks") or []) if c["name"]==name),None);return f"{d}" if d is not None else "—"
    rows=[("QWEN-2 · native vs SSD reload",f"{(r2.get('master_parity') or {}).get('exact_layers','—')}/80",f"pid {L2.get('engine_pid','—')} · {L2.get('engine_user','—')}"),
          ("QWEN-2 · second SSD reload",pc(r2,"MASTER_SECOND_RELOAD_80_LAYER_PARITY")+"/80","same process, file reloaded"),
          ("QWEN-3 · independent reload",f"{(r3.get('master_parity') or {}).get('exact_layers','—')}/80",f"NEW process pid {L3.get('engine_pid','—')} · {L3.get('engine_user','—')}"),
          ("CONTROLS · BASELINE_MASTER",pc(rc,"CONTROL_MEMORY_80_LAYER_PARITY_BASELINE_MASTER")+"/80",f"NEW process pid {LC.get('engine_pid','—')}"),
          ("QWEN-2 · SOURCE_A vs QWEN-1 seals",pc(r2,"SOURCE_CROSS_PROCESS_80_LAYER_PARITY_SOURCE_A")+"/80","across processes"),
          ("QWEN-2 · SOURCE_B vs QWEN-1 seals",pc(r2,"SOURCE_CROSS_PROCESS_80_LAYER_PARITY_SOURCE_B")+"/80","across processes"),
          ("CONTROLS · SOURCE_A / SOURCE_B",pc(rc,"CONTROL_MEMORY_80_LAYER_PARITY_SOURCE_A_ONLY")+"/80 · "+pc(rc,"CONTROL_MEMORY_80_LAYER_PARITY_SOURCE_B_ONLY")+"/80","across processes")]
    for j,(a,b,c) in enumerate(rows):
        y=.75-j*.083;T(fig,.685,y,a,size=7.8,weight="bold",xmax=.96);T(fig,.685,y-.027,b,size=9,weight="bold",color=OK_COL,mono=True);T(fig,.76,y-.027,c,size=7.2,color=MUTED,xmax=.96)
    T(fig,.065,.86,"parity = SHA-256 of every K and V tensor of all 80 layers equal (TEST730 memory_seals); heat maps: max |Δ| in each (layer, token-bin) cell",size=7.8,color=MUTED,xmax=.965)
    fig_footer(fig,k,"The naive one-pass rebuild uses a different BF16 chunk schedule (TEST758–760); the boundary sealed in the manifest restores bit-identity — measured, not assumed.")
    return save_fig(fig,k,"VERIFICATION RECORD",["q2_work/HEATMAPS_QWEN2.npz","TEST782_QWEN2_results.json","TEST782_QWEN3_results.json","TEST782_CONTROLS_results.json"])
MANDATORY=("MASTER_PHYSICAL_FILE_SHA","MASTER_TENSOR_SHA","MASTER_MANIFEST_ROUNDTRIP","MASTER_PARENT_SHA_LINKS","MASTER_RELOAD_INTEGRITY","MASTER_NUMERICAL_80_LAYER_PARITY","MASTER_INDEPENDENT_RELOAD")
def fig6():
    k="F6";rp=results_of("PREFLIGHT");q1,q2,bm,rd=manifests();V=LIVE.get("verification") or {}
    if not rp.get("sha_simulations"):return fig_missing(k,"The integrity chain is drawn from PREFLIGHT, QWEN-2, QWEN-3 and the host verification of this RUN.","PREFLIGHT did not complete.")
    fig=fig_base(k,"Every file that crosses a session boundary is identified by SHA-256 — and every seal is checked by the receiving process and again by the host","VERIFICATION RECORD")
    E1=q1.get("cartridges") or {};me=bm.get("master") or {};C=V.get("cartridges") or {}
    nodes=[("SOURCE_A",E1.get("SOURCE_A"),COL["A"],"QWEN-1 · q1_cartridges"),("SOURCE_B",E1.get("SOURCE_B"),COL["B"],"QWEN-1 · q1_cartridges"),
           ("MASTER_02",me or None,COL["M"],"QWEN-2 · master_bundle")]
    for j,(cid,e,c,where) in enumerate(nodes):
        y=.70-j*.22;box(fig,.035,y,.30,.16,ec=c,lw=1.5);rect(fig,.035,y+.16-.03,.30,.03,c,z=2)
        T(fig,.045,y+.145,f"{cid} · {where}",size=8.6,weight="bold",color="white",xmax=.33)
        if e:
            v=C.get(f"{cid}@{'q1_cartridges' if cid!='MASTER_02' else 'master_bundle'}") or {}
            T(fig,.045,y+.105,"file "+str(e.get("sha256",""))[:40],size=7.0,mono=True,xmax=.33)
            T(fig,.045,y+.078,"H3   "+str((e.get("tensor_sha") or {}).get("h",""))[:40],size=7.0,mono=True,xmax=.33)
            T(fig,.045,y+.051,"meta "+str(e.get("tensor_meta_sha256",""))[:40],size=7.0,mono=True,xmax=.33)
            T(fig,.045,y+.022,f"host re-hash: file {okm(v.get('file_sha_ok'))} · tensors {okm(v.get('tensor_seal_ok'))} · meta {okm(v.get('meta_sha_ok'))}",size=7.4,color=OK_COL if v.get("file_sha_ok") else RED,xmax=.33)
        else:T(fig,.045,y+.07,"not produced in this RUN",size=8,color=RED)
    if me:
        for yy in (.665,.445):Tc(fig,.035,.335,yy,"↓ file SHA-256 recorded as parent of MASTER_02 ↓",size=7.4,color=COL["M"])
        T(fig,.035,.10,f"parents of MASTER_02 = SHA-256 of SOURCE_A and SOURCE_B files: {okm((V.get('master') or {}).get('parents_link_ok'))}",size=7.8,color=COL["M"],xmax=.36)
    box(fig,.375,.10,.25,.76,ec=NEU,lw=1.3);T(fig,.385,.835,"7 mandatory MASTER checks",size=9.2,weight="bold",xmax=.62)
    T(fig,.385,.805,"check",size=7.2,weight="bold",color=MUTED);T(fig,.545,.805,"QWEN-2",size=7.2,weight="bold",color=MUTED);T(fig,.588,.805,"QWEN-3",size=7.2,weight="bold",color=MUTED)
    for j,name in enumerate(MANDATORY):
        y=.77-j*.085;a=chk("QWEN2",name);b=chk("QWEN3","MASTER_NUMERICAL_EXACT_80_PARITY" if name=="MASTER_NUMERICAL_80_LAYER_PARITY" else name)
        T(fig,.385,y,name.replace("MASTER_",""),size=7.3,xmax=.54,mono=True)
        T(fig,.548,y,"PASS" if a else ("FAIL" if a is False else "–"),size=7.6,weight="bold",color=OK_COL if a else (RED if a is False else MUTED))
        T(fig,.590,y,"PASS" if b else ("FAIL" if b is False else "–"),size=7.6,weight="bold",color=OK_COL if b else (RED if b is False else MUTED))
    T(fig,.385,.21,"– = not applicable in that session (QWEN-3 cannot see the parents by design)",size=6.6,color=MUTED,xmax=.62)
    T(fig,.385,.155,wrap("tuple/list normalisation: JSON stores the locked seal's tuples as lists — every manifest read is converted to the exact seal_cp() form after a strict schema check",56,4),
      size=6.9,color=INK2,va="top",linespacing=1.15,xmax=.62)
    rows=rp["sha_simulations"];box(fig,.64,.10,.325,.76,ec=NEU,lw=1.3)
    T(fig,.65,.835,f"CPU simulations before the GPU — {sum(r['pass'] for r in rows)}/{len(rows)} as expected",size=9.0,weight="bold",xmax=.96)
    for j,r in enumerate(rows):
        y=.80-j*.043;T(fig,.65,y,r["id"],size=7.0,weight="bold",mono=True)
        T(fig,.675,y,short(r["scenario"],52),size=6.8,color=INK2,xmax=.905)
        T(fig,.91,y,("✓ " if r["pass"] else "✗ ")+r["observed"],size=6.9,weight="bold",color=OK_COL if r["pass"] else RED,xmax=.962)
    fig_footer(fig,k,"Simulations: PREFLIGHT process with the LOCKED seal_cp / safe_load / record_cp on small BF16 tensors (expected rejections count as PASS). Mandatory checks: PASS lines of QWEN-2 and QWEN-3.")
    return save_fig(fig,k,"VERIFICATION RECORD",["TEST782_PREFLIGHT_results.json sha_simulations","TEST782_QWEN2/QWEN3_results.json checks","manifests","POST_RUN_VERIFICATION.json"])
def _layout_text(fig,text,x0,x1,y0,y1,fs_max=9.6,fs_min=5.6,cols_allowed=(1,2)):
    """the verbatim text (line breaks kept, long lines wrapped) at the largest font that fits the area; returns overflow lines"""
    raw=str(text).replace("\t","    ").split("\n");Wpt=(x1-x0)*FW*72;Hpt=(y1-y0)*FH*72
    for fs in np.arange(fs_max,fs_min-1e-9,-0.2):
        for nc in cols_allowed:
            gap=.012;cw=((x1-x0)-gap*(nc-1))/nc;chars=max(20,int(cw*FW*72/(fs*0.56)));lines=[]
            for ln in raw:lines+=(textwrap.wrap(ln,chars,break_long_words=True,replace_whitespace=False,drop_whitespace=True) or [""])
            per=int(Hpt/(fs*1.13))
            if len(lines)<=per*nc:
                for c in range(nc):
                    chunk=lines[c*per:(c+1)*per]
                    if chunk:fig.text(x0+c*(cw+gap),y1,mt("\n".join(chunk)),fontsize=fs,va="top",ha="left",color=INK,linespacing=1.27/1.2,family="DejaVu Sans")
                return [],round(float(fs),1),nc
    fs=fs_min;nc=max(cols_allowed);gap=.012;cw=((x1-x0)-gap*(nc-1))/nc;chars=max(20,int(cw*FW*72/(fs*0.56)));lines=[]
    for ln in raw:lines+=(textwrap.wrap(ln,chars,break_long_words=True) or [""])
    per=int(Hpt/(fs*1.13))
    for c in range(nc):
        chunk=lines[c*per:(c+1)*per]
        if chunk:fig.text(x0+c*(cw+gap),y1,mt("\n".join(chunk)),fontsize=fs,va="top",ha="left",color=INK,linespacing=1.27/1.2)
    return lines[per*nc:],fs,nc
def fig7():
    k="F7";r3=results_of("QWEN3");a=next((x for x in (r3.get("answers") or []) if x["id"]=="Q0"),None)
    txt=text_file("QWEN3","QWEN3_EXPRESSION.txt") if a else None
    for kk in [x for x in FIGURES if x.startswith("F7_")]:FIGURES.pop(kk,None)
    if not a or txt is None:return fig_missing(k,"The expression is printed verbatim from QWEN-3's output file of this RUN.","QWEN-3 did not write its expression in this RUN.")
    mm=(LIVE.get("verification") or {}).get("master") or {};L3=LEDGER.get("QWEN3") or {};pr=r3.get("access_probe") or {}
    fig=fig_base(k,"Printed exactly as QWEN-3 wrote it (no edit, no shortening) — QWEN-3 had only MASTER_02: no source text, no source cartridge, no QWEN-2 output","SEALED MEMORY")
    q=a["question"];T(fig,.035,.862,"QUESTION Q0 (sealed before any model was loaded):",size=8.2,weight="bold",color=COL["Q3"])
    T(fig,.035,.832,wrap(q,190,2),size=7.6,color=INK2,va="center",linespacing=1.15,xmax=.965)
    box(fig,.035,.095,.655,.705,ec=COL["Q3"],lw=1.6);T(fig,.045,.782,f"ANSWER — QWEN-3 · {a['tokens']} tokens · verbatim",size=8.2,weight="bold",color=COL["Q3"],xmax=.68)
    rest,fs,nc=_layout_text(fig,txt,.045,.68,.105,.765)
    box(fig,.705,.095,.26,.705,ec=NEU,lw=1.3,fc=PANEL);T(fig,.715,.782,"EVIDENCE CHAIN",size=8.6,weight="bold",xmax=.96)
    ev=[("text SHA-256",[a["sha256"][:32],a["sha256"][32:]]),("MASTER_02 file SHA-256",[str(mm.get("sha256",""))[:32],str(mm.get("sha256",""))[32:]]),
        ("MASTER tensor seal (H3)",[str(mm.get("h3_seal",""))[:32],str(mm.get("h3_seal",""))[32:]]),
        ("parents (QWEN-1 files)",[f"SOURCE_A + SOURCE_B · links {okm(mm.get('parents_link_ok'))}"]),
        ("QWEN-3 process",[f"pid {L3.get('engine_pid','—')} · user {L3.get('engine_user','—')}",f"uid {L3.get('engine_uid','—')} · exit {L3.get('exit_code','—')}"]),
        ("reload parity in QWEN-3",[f"{(r3.get('master_parity') or {}).get('exact_layers','—')}/80 layers bit-identical"]),
        ("source folders → QWEN-3",[f"{k_}: {'no OS read' if not v_.get('os_read_permission') else 'OS readable'} · {v_.get('python_open','—').replace('BLOCKED_BY_','blocked by ').lower()}" for k_,v_ in pr.items()]),
        ("generation",[f"{a['seconds']} s · limit {a['limit']} · truncated {a['possible_truncation']}"]),
        ("model",[f"{MODEL_ID} NF4 frozen",f"sentinel {str(r3.get('weights_sentinel',''))[:16]}…"])]
    y=.75
    for h,ls in ev:
        T(fig,.715,y,h,size=7.2,weight="bold",color=MUTED,xmax=.96);y-=.023
        for l in ls:T(fig,.715,y,l,size=6.5,mono=True,xmax=.96);y-=.021
        y-=.012
    fig_footer(fig,k,f"Verbatim from q3_out/QWEN3_EXPRESSION.txt (SHA-256 above) · font {fs} pt · {nc} column(s)"+(" · continued on the next page" if rest else "")+" · correctness of the content is NOT graded here (human review PENDING).")
    recs=save_fig(fig,k,"SEALED MEMORY",["q3_out/QWEN3_EXPRESSION.txt","TEST782_QWEN3_results.json","POST_RUN_VERIFICATION.json"])
    page=2
    while rest:
        kk=f"F7_{page}";FIGURES[kk]=dict(n=7,title=f"QWEN-3 — The MASTER in Human Language (verbatim, page {page})",slug=f"QWEN3_EXPRESSION_VERBATIM_P{page}",tab="BLIND READING · QWEN-3")
        fg=fig_base(kk,"Continuation — printed exactly as QWEN-3 wrote it","SEALED MEMORY");box(fg,.035,.095,.93,.77,ec=COL["Q3"],lw=1.6)
        rest,fs2,nc2=_layout_text(fg,"\n".join(rest),.045,.955,.105,.85,fs_max=fs,fs_min=5.6,cols_allowed=(2,));fig_footer(fg,kk,f"page {page} of the verbatim QWEN-3 expression (SHA-256 of the full text: {a['sha256'][:24]}…)")
        FIG_FILES[kk]=save_fig(fg,kk,"SEALED MEMORY",["q3_out/QWEN3_EXPRESSION.txt"]);page+=1
    return recs
def fig8():
    k="F8";r3=results_of("QWEN3");ans=r3.get("answers") or []
    if len(ans)<2:return fig_missing(k,"The panel answers are QWEN-3's outputs of this RUN.","QWEN-3 did not answer the panel in this RUN.")
    fig=fig_base(k,"QWEN-3's answers to the sealed questions (quoted, shortened — full texts in the records) and where its attention falls inside MASTER_02","SEALED MEMORY")
    for j,a in enumerate([x for x in ans if x["id"]!="Q0"][:5]):
        y=.865-j*.152;box(fig,.035,y-.142,.53,.135,ec=COL["Q3"],lw=1.2)
        T(fig,.045,y-.018,f"{a['id']} · {a['kind'].replace('_',' ').lower()} · {a['tokens']} tokens · SHA {a['sha256'][:10]}…",size=7.8,weight="bold",color=COL["Q3"],xmax=.56)
        T(fig,.045,y-.04,"“"+wrap(" ".join(str(a["answer"]).split()),118,4)+"”",size=6.9,color=INK,va="top",linespacing=1.15,xmax=.56)
    at=r3.get("attention") or {}
    if at.get("status")=="MEASURED" and at.get("rows"):
        rows=at["rows"];lays=sorted({int(l) for r in rows for l in r["layers"]});M=np.zeros((len(rows),len(lays)));Aa=np.zeros_like(M);Bb=np.zeros_like(M)
        for i,r in enumerate(rows):
            for j,l in enumerate(lays):
                d=r["layers"].get(str(l)) or {};a_=float(d.get("B0_mass",0));b_=float(d.get("B1_mass",0));Aa[i,j]=a_;Bb[i,j]=b_;M[i,j]=b_/max(a_+b_,1e-12)
        ax=fig.add_axes([.62,.30,.30,.50]);im=ax.imshow(M,cmap="coolwarm",vmin=0,vmax=1,aspect="auto")
        ax.set_xticks(range(len(lays)));ax.set_xticklabels([f"L{l}" for l in lays]);ax.set_yticks(range(len(rows)));ax.set_yticklabels([r["id"] for r in rows])
        for i in range(len(rows)):
            for j in range(len(lays)):ax.text(j,i,f"A {100*Aa[i,j]:.0f}%\nB {100*Bb[i,j]:.0f}%",ha="center",va="center",fontsize=6.0,color="black")
        ax.set_title("attention of the last question token",fontsize=8.8);_axstyle(ax,7.5)
        cax=fig.add_axes([.93,.30,.010,.50]);cb=fig.colorbar(im,cax=cax);cb.set_ticks([0,.5,1]);cb.set_ticklabels(["A","½","B"]);cb.ax.tick_params(labelsize=7)
        T(fig,.62,.235,wrap("Share of the attention mass (all heads) on the MASTER rows of SOURCE_A vs SOURCE_B, layers 4/20/40/79 — the rest goes to prefix and question. Observational (TEST779 instrumentation): no output is changed.",64,4),
          size=6.9,color=INK2,va="top",linespacing=1.15,xmax=.965)
    else:
        box(fig,.62,.35,.345,.30,ec=AMBER,lw=1.2,ls="--");T(fig,.63,.62,"attention share NOT MEASURED in this RUN",size=8.6,weight="bold",color=AMBER,xmax=.96)
        T(fig,.63,.59,wrap(str(at.get("error") or at.get("status") or "—"),60,5),size=7.2,color=INK2,va="top",xmax=.96)
    fig_footer(fig,k,"Answers: q3_out/QWEN3_Q1…Q5.txt (unedited; quotes shortened with “…” only by line limits). Attention: TEST782_QWEN3_results.json attention (span B0 = SOURCE_A rows, B1 = SOURCE_B rows).")
    return save_fig(fig,k,"SEALED MEMORY",["q3_out/QWEN3_Q1–Q5.txt","TEST782_QWEN3_results.json"])
def fig9():
    k="F9";cm=LIVE.get("metrics")
    if not cm or not cm.get("rows"):return fig_missing(k,"The control comparison is computed from the CONTROLS and QWEN-3 answers of this RUN.","CONTROLS (or QWEN-3) did not complete in this RUN.")
    fig=fig_base(k,"Same sealed questions, four memories in a separate process + QWEN-3 — how much SOURCE_A- and SOURCE_B-specific vocabulary each answer carries","OBSERVATIONAL")
    conds=[c for c in ("NO_MEMORY","SOURCE_A_ONLY","SOURCE_B_ONLY","BASELINE_MASTER","QWEN3_BLIND") if c in cm["rows"]];qs=["Q0","Q1","Q2","Q3","Q4"]
    labels={"NO_MEMORY":"NO MEMORY","SOURCE_A_ONLY":"SOURCE_A only","SOURCE_B_ONLY":"SOURCE_B only","BASELINE_MASTER":"MASTER (controls)","QWEN3_BLIND":"MASTER (QWEN-3 blind)"}
    for j,(key,lab,cmap) in enumerate((("a","SOURCE_A-specific words found (count)","Blues"),("b","SOURCE_B-specific words found (count)","RdPu"))):
        M=np.array([[cm["rows"][c].get(q,{}).get(key+"_hits",0) for q in qs] for c in conds],float)
        ax=fig.add_axes([.14+j*.31,.32,.24,.48]);ax.imshow(M,cmap=cmap,aspect="auto",vmin=0,vmax=max(1,M.max()))
        ax.set_xticks(range(len(qs)));ax.set_xticklabels(qs);ax.set_yticks(range(len(conds)));ax.set_yticklabels([labels[c] for c in conds] if j==0 else [""]*len(conds))
        for i in range(len(conds)):
            for q in range(len(qs)):ax.text(q,i,f"{int(M[i,q])}",ha="center",va="center",fontsize=7.6,color="black" if M[i,q]<.6*max(1,M.max()) else "white")
        ax.set_title(lab,fontsize=8.6);_axstyle(ax,7.6)
    v=cm["vocabulary"];rep=cm.get("reproduction") or {}
    box(fig,.765,.32,.20,.48,ec=NEU,lw=1.3);T(fig,.775,.775,"absent topic (Q5)",size=8.8,weight="bold",xmax=.96)
    for i,c in enumerate(conds):
        d=cm["rows"][c].get("Q5",{});ok=d.get("unknown")
        T(fig,.775,.735-i*.05,labels[c],size=7.4,xmax=.90);T(fig,.957,.735-i*.05,"UNKNOWN ✓" if ok else "answered",size=7.4,weight="bold",color=OK_COL if ok else AMBER,ha="right")
    T(fig,.775,.45,"QWEN-3 Q0 = CONTROLS MASTER Q0",size=7.4,weight="bold",xmax=.96);T(fig,.775,.425,f"identical text: {okm(rep.get('qwen3_q0_equals_controls_master_q0'))} · similarity {rep.get('qwen3_vs_controls_master_similarity','—')}",size=7.2,color=INK2,xmax=.96)
    T(fig,.775,.39,"(two independent processes)",size=7.0,color=MUTED,xmax=.96)
    T(fig,.035,.25,f"vocabulary measured from the forged source bodies (outside QWEN-3): {v['a_specific']} words only in SOURCE_A · {v['b_specific']} only in SOURCE_B · {v['shared']} in both · {v['question_terms_excluded']} question words excluded",size=7.8,color=INK2,xmax=.965)
    T(fig,.035,.215,"Expected if the memory is causal: NO MEMORY ≈ 0 · A-only high A / low B · B-only high B / low A · MASTER both. General model knowledge shows up in NO MEMORY.",size=7.8,color=INK2,xmax=.965)
    T(fig,.035,.18,"This is a lexical trace of the documents in the answers — not a grade of correctness, relations or fabrication (human review PENDING).",size=7.8,color=AMBER,xmax=.965)
    fig_footer(fig,k,"Answers: controls/<ARM>_Q*.txt and q3_out/QWEN3_*.txt · counts: CONTROL_METRICS.json (host, after all sessions; source texts read only by the host and QWEN-1).")
    return save_fig(fig,k,"OBSERVATIONAL",["CONTROL_METRICS.json","controls/*.txt","q3_out/*.txt","q1_sources/*_BODY_FORGED.txt (host only)"])
_AKB782_PARTS.add(3)
# ===== END OF PART 3/4 =====
# ===== PART 4/4 — paste directly after PART 3 in the same cell =====
# =====================================================================================================================
# PART 4 / 4 — the last figures, records, the RUN pipeline and the Gradio interface; it starts the program.
# THIS PART  74,849 characters · its last line is  # ===== END OF PART 4/4 =====
# =====================================================================================================================
EMBEDDED.update({                            # embedded copy of the locked 709.py (generated by the build — do not edit)
 "709.py":(  # 20954 bytes · git blob 6c9f8cbb1eeed848d45133d73f0d7676b68e9125
  "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"
 ),
})
def fig10():
    k="F10"
    if not LEDGER.get("QWEN1"):return fig_missing(k,"Isolation is drawn from the process ledger and GPU samples of this RUN.","No engine session ran in this RUN.")
    fig=fig_base(k,"GPU memory over the whole RUN (nvidia-smi, every 10 s) — each session loads the model, ends, and the GPU returns to empty before the next one starts","VERIFICATION RECORD")
    S=[s for s in GPU_SAMPLES if s.get("used_mib") is not None];t0=min([LEDGER[s]["start_t"] for s in ENGINE_STAGES if s in LEDGER]+[s["t"] for s in S] or [time.time()])
    ax=fig.add_axes([.065,.52,.58,.30])
    for s in ENGINE_STAGES:
        L=LEDGER.get(s)
        if L and L.get("end_t"):ax.axvspan((L["start_t"]-t0)/60,(L["end_t"]-t0)/60,color=SCOL[s],alpha=.13,lw=0)
    if S:ax.plot([(s["t"]-t0)/60 for s in S],[s["used_mib"]/1024 for s in S],color=INK,lw=1.2)
    for s in ENGINE_STAGES:
        L=LEDGER.get(s)
        if L and L.get("end_t"):ax.plot([(L["end_t"]-t0)/60],[((L.get("gpu_release") or {}).get("used_mib") or 0)/1024],marker="v",color=SCOL[s],ms=6)
    ax.set_ylabel("GPU memory used (GiB)",fontsize=8);ax.set_xlabel("minutes since the first session started",fontsize=8);ax.set_ylim(0,82);_axstyle(ax,7.5)
    ax.set_title("shaded = one OS process · ▼ = GPU after its exit",fontsize=8.6)
    hd=["session","pid","user (uid)","network","start → end (UTC)","exit","GPU peak","GPU after"];xs=[.035,.11,.16,.27,.355,.50,.535,.59]
    for x,h in zip(xs,hd):T(fig,x,.43,h,size=7.2,weight="bold",color=MUTED)
    hline(fig,.035,.645,.415,RULE)
    for j,s in enumerate(ENGINE_STAGES):
        L=LEDGER.get(s) or {};y=.39-j*.05
        T(fig,.035,y,SNAME[s],size=7.6,weight="bold",color=SCOL[s])
        vals=[str(L.get("engine_pid","—")),f"{L.get('engine_user','—')} ({L.get('engine_uid','—')})",("namespace" if L.get("netns") else ("offline" if L.get("offline") else "online")) if L else "—",
              f"{str(L.get('start',''))[11:19]} → {str(L.get('end',''))[11:19]}",str(L.get("exit_code","—")),f"{(L.get('gpu_peak_used_mib') or 0)/1024:.1f} GiB" if L.get("gpu_peak_used_mib") else "—",
              f"{(L.get('gpu_release') or {}).get('used_mib','—')} MiB"]
        for x,v,nx in zip(xs[1:],vals,xs[2:]+[.645]):T(fig,x,y,v,size=7.2,mono=True,xmax=nx-.004)
    pm=ISO.get("perm_maps",{}).get("QWEN3") or {};box(fig,.67,.10,.295,.73,ec=NEU,lw=1.3)
    T(fig,.68,.805,"what each session may open (designed)",size=8.8,weight="bold",xmax=.96)
    folders=[("q1_sources","texts"),("q1_cartridges","A/B .pt"),("q2_work","QWEN-2"),("master_bundle","MASTER"),("panel","panel")]
    allow={"QWEN1":{"q1_sources","q1_cartridges","panel"},"QWEN2":{"q1_cartridges","q2_work","master_bundle","panel"},"QWEN3":{"master_bundle","panel"},"CONTROLS":{"q1_cartridges","master_bundle","panel"}}
    for i,(f,lab) in enumerate(folders):Tc(fig,.775+i*.038-.019,.775+i*.038+.019,.765,lab,size=6.6,color=MUTED)
    for j,s in enumerate(("QWEN1","QWEN2","QWEN3","CONTROLS")):
        y=.725-j*.045;T(fig,.68,y,SNAME[s],size=7.4,weight="bold",color=SCOL[s])
        for i,(f,_) in enumerate(folders):
            ok=f in allow[s];Tc(fig,.775+i*.038-.017,.775+i*.038+.017,y,"✓" if ok else "✗",size=8.4,weight="bold",color=OK_COL if ok else RED)
    I=(LIVE.get("verification") or {}).get("isolation") or {};pr=I.get("qwen3_probe") or {}
    info=[f"isolation mode: {ISO.get('mode')}",f"network namespace (QWEN-2/3): {'yes' if ISO.get('netns') else 'no — HF offline only'}",
          *([f"run as root (CUDA not usable as their user): {', '.join(SNAME[x] for x in ISO['root_fallback'])}"] if ISO.get("root_fallback") else []),
          "QWEN-3 OS-level: "+("ENFORCED" if I.get('qwen3_os_level')=="ENFORCED" else ("NOT ENFORCED — python audit barrier only" if I.get('qwen3_os_level') else "—")),*(f"QWEN-3 → {k_}: OS read {'yes' if v_.get('os_read_permission') else 'no'} · open {v_.get('python_open','—').replace('BLOCKED_BY_','blocked/').lower()}" for k_,v_ in pr.items()),
          f"QWEN-3 forbidden opens: {len(I.get('qwen3_violations') or [])} · QWEN-2: {len(I.get('qwen2_violations') or [])}",
          f"folders QWEN-3 opened: {', '.join(sorted((I.get('qwen3_folders_opened') or {}).keys()))}"]
    for j,t in enumerate(info):T(fig,.68,.52-j*(.045 if len(info)<=9 else .040),t,size=7.2,color=INK2,xmax=.96)
    fig_footer(fig,k,"PROCESS_LEDGER.json · GPU_SAMPLES.json (host) · PERMISSION_MAPS.json · ISOLATION_SETUP.json · QWEN-3 access_probe / access_audit (python open-audit hook in every session).")
    return save_fig(fig,k,"VERIFICATION RECORD",["PROCESS_LEDGER.json","GPU_SAMPLES.json","PERMISSION_MAPS.json","ISOLATION_SETUP.json","TEST782_QWEN3_results.json"])
def fig11():
    k="F11";R={s:results_of(s) for s in SESSIONS}
    if not R["QWEN1"]:return fig_missing(k,"Timings and memory are measured by the sessions of this RUN.","QWEN-1 did not run.")
    fig=fig_base(k,"Measured separately — model download and loading are never counted as fusion time · GPU peaks from each session's own CUDA counters","LIVE MEASUREMENT")
    items=[]
    def tget(s,key):v=(R[s].get("timings") or {}).get(key);return sum(v) if v else None
    for s,key,lab in (("QWEN1","model_download_or_cache_check","download / cache check"),("QWEN1","model_load","model load"),("QWEN2","model_load","model load"),("QWEN3","model_load","model load"),("CONTROLS","model_load","model load"),
                      ("QWEN1","tokenization_SOURCE_A","tokenize A"),("QWEN1","tokenization_SOURCE_B","tokenize B"),("QWEN1","forge_SOURCE_A","forge A"),("QWEN1","forge_SOURCE_B","forge B"),
                      ("QWEN1","ssd_write_and_seal_SOURCE_A","SSD write+seal A"),("QWEN1","ssd_write_and_seal_SOURCE_B","SSD write+seal B"),("QWEN2","ssd_reload_verify_SOURCE_A","reload+verify A"),
                      ("QWEN2","native_fusion_total","native fusion A→B"),("QWEN2","master_consolidation","MASTER consolidation"),("QWEN2","master_ssd_write_and_seal","MASTER write+seal"),
                      ("QWEN2","master_boundary_rebuild_80","MASTER rebuild 80"),("QWEN2","master_parity_seals","parity seals"),("QWEN3","master_boundary_rebuild_80","rebuild 80"),
                      ("QWEN3","h2d_master","CPU→GPU MASTER")):
        v=tget(s,key)
        if v is not None:items.append((f"{SNAME[s]} · {lab}",v,SCOL[s]))
    gens={s:sum(sum(v) for kk,v in (R[s].get("timings") or {}).items() if kk.startswith("generation_")) for s in ("QWEN2","QWEN3","CONTROLS") if R[s]}
    for s,v in gens.items():
        if v:items.append((f"{SNAME[s]} · generation (all answers)",v,SCOL[s]))
    ax=fig.add_axes([.20,.15,.30,.69]);y=np.arange(len(items))[::-1]
    ax.barh(y,[max(v,1e-3) for _,v,_ in items],color=[c for _,_,c in items]);ax.set_xscale("log");ax.set_yticks(y);ax.set_yticklabels([l for l,_,_ in items],fontsize=6.8)
    for yi,(_,v,_) in zip(y,items):ax.text(max(v,1e-3)*1.15,yi,f"{v:.2f} s" if v<100 else f"{v/60:.1f} min",va="center",fontsize=6.4)
    ax.set_xlim(right=max([v for _,v,_ in items]+[1])*8);ax.set_title("time of each operation (log scale, seconds)",fontsize=8.8);_axstyle(ax,7)
    bars=[]
    for s_ in ("QWEN1","QWEN2","QWEN3","CONTROLS"):
        for r in R[s_].get("resources") or []:
            if r.get("peak_allocated_gib") is not None and r["stage"]!="session_start":bars.append((f"{SNAME[s_]} · {r['stage'].replace('_',' ')}",r["peak_allocated_gib"],SCOL[s_]))
    bars=sorted(bars,key=lambda b:-b[1])[:12]
    ax2=fig.add_axes([.72,.42,.24,.42]);yy=np.arange(len(bars))[::-1]
    if bars:
        ax2.barh(yy,[b for _,b,_ in bars],color=[c for _,_,c in bars]);ax2.set_yticks(yy);ax2.set_yticklabels([l for l,_,_ in bars],fontsize=6.3)
        for yi,(_,v,_) in zip(yy,bars):ax2.text(v,yi,f" {v:.1f}",va="center",fontsize=6.2)
        ax2.set_xlim(0,max(b for _,b,_ in bars)*1.25)
    ax2.set_title("largest torch peaks per stage (GiB)",fontsize=8.4);_axstyle(ax2,6.5)
    est=R["PREFLIGHT"].get("gpu_budget_estimate") or {};act=R["QWEN2"].get("gpu_budget_actual_tokens") or {}
    V=(LIVE.get("verification") or {}).get("cartridges") or {};pk=max([b for _,b,_ in bars] or [0])
    lines=[f"pre-run GPU budget: {est.get('total_estimate_gib','—')} GiB (estimate, {est.get('tokens','—')} tokens) · headroom {est.get('headroom_on_80gib','—')} GiB",
           f"this MASTER ({act.get('tokens','—')} tokens): {act.get('total_estimate_gib','—')} GiB estimate · largest measured torch peak {pk:.1f} GiB",
           *(f"{kk.split('@')[0]} file {fmt_b(v.get('bytes'))} · 80-layer K/V equivalent {fmt_b(v.get('full_80_layer_kv_bytes'))}" for kk,v in V.items() if kk.endswith("@q1_cartridges") or kk.endswith("@master_bundle"))]
    for j,t in enumerate(lines):T(fig,.555,.32-j*.04,t,size=7.4,color=INK2,xmax=.965)
    fig_footer(fig,k,"Timings: each session's Timer records (TEST782_<SESSION>_results.json timings) · GPU: torch.cuda counters per stage (RESOURCE lines) · sizes: files re-measured by the host.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST782_<SESSION>_results.json timings/resources","POST_RUN_VERIFICATION.json"])
def categories():
    """the four separate success categories of the instruction, decided only from this RUN's records"""
    V=LIVE.get("verification") or {};L=V.get("ledger") or {};r1,r2,r3=results_of("QWEN1"),results_of("QWEN2"),results_of("QWEN3")
    iso_conds=[("QWEN-1 wrote two sound cartridges and ended",r1.get("status")=="COMPLETE" and chk("QWEN1","TWO_SOURCE_CARTRIDGES_WRITTEN")),
               ("QWEN-2 (new process) read the cartridges and built MASTER_02",r2.get("status")=="COMPLETE"),
               ("MASTER SHA checks and 80/80 parity in QWEN-2",all(chk("QWEN2",c) for c in MANDATORY[:6])),
               ("QWEN-3 (new process) read MASTER_02 only, 80/80",r3.get("status")=="COMPLETE" and chk("QWEN3","MASTER_INDEPENDENT_RELOAD")),
               ("QWEN-3 expressed the MASTER in human language",bool(next((a for a in (r3.get("answers") or []) if a["id"]=="Q0"),None))),
               ("sessions strictly sequential, GPU empty after each",bool(L.get("sequential")) and all((L.get("gpu_released") or {}).values())),
               ("QWEN-3: no forbidden folder opened",not ((V.get("isolation") or {}).get("qwen3_violations")) and bool(r3))]
    phys=all(v for _,v in iso_conds)
    osl=str(r3.get("os_level_isolation") or "");os_ok=osl=="ENFORCED"
    iso_conds.append(("OS level: QWEN-3 had no read permission on the source folders (own Linux user)" if os_ok or not r3 else
                      "OS level NOT enforced: QWEN-3 ran with OS read permission; only the python audit barrier blocked",os_ok if r3 else None))
    label="PASS" if phys and os_ok else ("PASS · PROCESS LEVEL ONLY" if phys else "NOT PASSED")
    base=[(c,chk("QWEN3" if c=="MASTER_INDEPENDENT_RELOAD" else "QWEN2",c)) for c in MANDATORY]
    return dict(physical=(phys,iso_conds),physical_label=label,physical_os_enforced=os_ok,baseline=(all(v for _,v in base),base),
                autonomous=("NOT CREATED",(r2.get("autonomous_master") or {}).get("reason","QWEN-2 did not run")),
                synthesis=("NOT EVALUATED","needs independent, source-grounded human review of the QWEN-3 texts; native fusion ≠ semantic synthesis"))
def fig12():
    k="F12";c=categories()
    fig=fig_base(k,"Four separate questions, four separate answers — decided only from this RUN's records; nothing here is a semantic grade","VERIFICATION RECORD")
    def cat(x,y,w,h,title,status,col,lines):
        box(fig,x,y,w,h,ec=col,lw=1.7);rect(fig,x,y+h-.04,w,.04,col,z=2)
        T(fig,x+.01,y+h-.02,title,size=9.4,weight="bold",color="white",xmax=x+w-.12);T(fig,x+w-.01,y+h-.02,status,size=9.4,weight="bold",color="white",ha="right")
        for j,(t,v) in enumerate(lines):
            yy=y+h-.07-j*.034
            if v!="cont":T(fig,x+.01,yy,okm(v) if isinstance(v,bool) or v is None else "•",size=8.6,weight="bold",color=OK_COL if v else (RED if v is False else MUTED))
            T(fig,x+.03,yy,t,size=7.6,color=INK,xmax=x+w-.008)
    p_ok,pl=c["physical"];b_ok,bl=c["baseline"]
    cat(.035,.47,.455,.39,"1 · PHYSICAL ISOLATION (three sessions)",c["physical_label"],(OK_COL if c["physical_os_enforced"] else AMBER) if p_ok else RED,pl)
    cat(.51,.47,.455,.39,"2 · BASELINE MASTER (native, protocol-driven)","PASS" if b_ok else "NOT PASSED",OK_COL if b_ok else RED,[(n,v) for n,v in bl])
    cat(.035,.10,.455,.33,"3 · AUTONOMOUS MASTER (DrA decision)",c["autonomous"][0],AMBER,[(t,None if i==0 else "cont") for i,t in enumerate(textwrap.wrap(c["autonomous"][1],88)[:6])])
    r2=results_of("QWEN2");ev=r2.get("qwen2_evaluation") or {}
    cat(.51,.10,.455,.33,"4 · NEW SEMANTIC SYNTHESIS",c["synthesis"][0],AMBER,[(t,None if i==0 else "cont") for i,t in enumerate(textwrap.wrap(c["synthesis"][1],88)[:3])]+
        [(f"QWEN-2 stated decision line: {ev.get('decision_line','—')} (recorded, not a gate)",None),         ("the frozen model may know these topics from pre-training → see NO_MEMORY (Fig. 9)",None)])
    fig_footer(fig,k,"Category 1: PASS needs every listed condition (PROCESS LEVEL ONLY when just the OS-level one is missing); 2 = the seven mandatory checks; 3 and 4 are separate categories by design (instruction §19) and are not inferred from 1 and 2.")
    return save_fig(fig,k,"VERIFICATION RECORD",["all session results","POST_RUN_VERIFICATION.json","PROCESS_LEDGER.json"])
FIG_FUNCS=OrderedDict([("F1",fig1),("F2",fig2),("F3",fig3),("F4",fig4),("F5",fig5),("F6",fig6),("F7",fig7),("F8",fig8),("F9",fig9),("F10",fig10),("F11",fig11),("F12",fig12)])
def render_figures():
    errs={};FIGURES.clear();FIGURES.update(BASE_FIGURES)
    for key,fn in FIG_FUNCS.items():
        t=time.perf_counter()
        try:
            rec=fn();FIG_FILES[key]=rec;STATE["fig_version"]+=1;bump()
            _emit(f"  figure {FIGURES[key]['n']} · {rec['badge']} · {rec['pixels'][0]}×{rec['pixels'][1]} · layout QC {'pass' if rec['layout_qc']['passed'] else 'FAIL'} · {time.perf_counter()-t:.1f} s")
        except Exception as ex:
            errs[key]=f"{type(ex).__name__}: {ex}";FIG_FILES.pop(key,None);flog_fig(f"{key} NOT GENERATED {traceback.format_exc()[-1500:]}");_emit(f"  figure {key} NOT GENERATED · {errs[key]}");plt.close("all")
    order=[k for k in FIGURES];extra=[k for k in FIG_FILES if k not in order]
    for kk in extra:FIGURES[kk]=dict(n=7,title="QWEN-3 — verbatim (continued)",slug=kk,tab="BLIND READING · QWEN-3")
    ordered=OrderedDict()
    for kk in BASE_FIGURES:
        ordered[kk]=FIGURES[kk]
        if kk=="F7":
            for x in sorted([y for y in FIGURES if y.startswith("F7_")]):ordered[x]=FIGURES[x]
    FIGURES.clear();FIGURES.update(ordered)
    FIG_ERRORS.clear();FIG_ERRORS.update(errs)
    dump_json(SESSION_DIR/"FIGURES_MANIFEST.json",dict(session=SESSION_ID,utc=utc_now(),simulation=SIM,figures=FIG_FILES,not_generated=errs))
    return errs
def stage_figures():
    errs=render_figures();n=len([k for k in FIG_FILES if k in BASE_FIGURES])
    qcf=[k for k,v in FIG_FILES.items() if not (v.get("layout_qc") or {}).get("passed") or not (v.get("jpeg_qc") or {}).get("passed")]
    np_=[k for k,v in FIG_FILES.items() if v["badge"]=="NOT PRODUCED IN THIS RUN"]
    note=f"{n}/{len(BASE_FIGURES)} JPEG figures written (300 dpi)"+(f" + {len(FIG_FILES)-n} continuation page(s)" if len(FIG_FILES)>n else "")
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
def write_run_summary():
    L=[];a=L.append
    a(f"{APP_NAME} — {APP_SUB}\n{EXPERIMENT} live demonstration · demo {CODE_VERSION} · RUN {SESSION_ID} · written {local_now()}")
    if SIM:a("SIMULATION — NOTHING IN THIS FILE IS AN EXPERIMENTAL RESULT")
    a(f"RUN VERDICT {run_verdict()}\nengine: 782.py git blob {LOCKS[ENGINE_NAME]} executed unchanged as five OS processes · run folder {RUN_ROOT}")
    a("\nSTAGES (times = this RUN)")
    for key,title in STAGES.items():
        s=STATE["stages"][key];a(f"  [{s['status'].upper():<4}] {key:<10} {('%.0f s'%s['seconds']) if s['seconds'] is not None else '':>8}  {title}\n             {s['note']}")
    a("\nPROCESS LEDGER")
    for s,v in LEDGER.items():a(f"  {SNAME[s]:<9} pid {v.get('engine_pid')} user {v.get('engine_user')} uid {v.get('engine_uid')} {v.get('start')} → {v.get('end')} exit {v.get('exit_code')} GPU after {(v.get('gpu_release') or {}).get('used_mib')} MiB")
    try:c=categories()
    except Exception:c=None
    if c:
        a("\nCATEGORIES (instruction §19 — separate)")
        a(f"  1 PHYSICAL ISOLATION   {c['physical_label']}")
        for t,v in c["physical"][1]:a(f"      {okm(v)} {t}")
        a(f"  2 BASELINE MASTER      {'PASS' if c['baseline'][0] else 'NOT PASSED'}")
        for t,v in c["baseline"][1]:a(f"      {okm(v)} {t}")
        a(f"  3 AUTONOMOUS MASTER    {c['autonomous'][0]} — {c['autonomous'][1]}")
        a(f"  4 SEMANTIC SYNTHESIS   {c['synthesis'][0]} — {c['synthesis'][1]}")
    r3=results_of("QWEN3")
    for x in r3.get("answers") or []:a(f"\nQWEN-3 {x['id']} ({x['kind']}) — from MASTER_02 alone · {x['tokens']} tokens · SHA-256 {x['sha256']}\n  {x['question']}\n  "+str(x["answer"]).replace("\n","\n  "))
    a("\nHUMAN REVIEW: NOT PROVIDED (pending). No semantic grading was performed by TEST782 or by this demo.")
    a(f"\n{AUTHOR} · {ORG} · {LICENSE_NAME} · {COPYRIGHT}")
    RUN_SUMMARY.write_text("\n".join(L)+"\n",encoding="utf-8");_private(RUN_SUMMARY)
def engine_files():
    out=[]
    for s,d in OUTDIRS.items():
        p=rpath(d)
        if not p.is_dir():continue
        out+=[x for x in (p/f"TEST782_{s}.log",p/f"TEST782_{s}_results.json") if x.is_file()]
    out+=[x for x in (rpath("q1_cartridges")/"Q1_CARTRIDGE_MANIFEST.json",rpath("q2_work")/"Q2_MANIFEST.json",rpath("master_bundle")/"MASTER_MANIFEST.json",rpath("master_bundle")/"READY.json",
                      rpath("panel")/"SEALED_PANEL.json",rpath("panel")/"PANEL_SEAL.json",rpath("q2_work")/"QWEN2_EVALUATION_PRIVATE.txt",rpath("q2_work")/"HEATMAPS_QWEN2.npz") if x.is_file()]
    for d in ("q3_out","controls"):
        p=rpath(d)
        if p.is_dir():out+=sorted(p.glob("*.txt"))
    return out
def download_items():
    items=[("Run summary",RUN_SUMMARY),("Engine output, real-time (UTC receipt · session · stream · line)",ENGINE_OUT),("Session log",SESSION_LOG),("Session events (JSONL)",SESSION_EVENTS),
           ("Process ledger",DATA_DIR/"PROCESS_LEDGER.json"),("GPU samples",DATA_DIR/"GPU_SAMPLES.json"),("Isolation set-up",DATA_DIR/"ISOLATION_SETUP.json"),("Permission maps",DATA_DIR/"PERMISSION_MAPS.json"),
           ("Post-run verification",VERIFY_FILE),("Control metrics",DATA_DIR/"CONTROL_METRICS.json"),("MASTER anatomy (heat-map data)",DATA_DIR/"MASTER_ANATOMY.npz"),
           ("Stage record",DATA_DIR/"STAGES.json"),("Engine checks of this RUN",DATA_DIR/"ENGINE_CHECKS.json"),("Figure manifest",SESSION_DIR/"FIGURES_MANIFEST.json"),("SHA-256 manifest",MANIFEST),
           ("782.py (locked, executed)",EVID_DIR/ENGINE_NAME)]
    out=[(l,str(p)) for l,p in items if Path(p).is_file()]
    out+=[(f"engine file · {p.parent.name}/{p.name}",str(p)) for p in engine_files()]
    return out
def package_session():
    dump_json(DATA_DIR/"ENGINE_CHECKS.json",CHECKS);dump_json(DATA_DIR/"STAGES.json",dict(verdict=run_verdict(),stages=STATE["stages"],session=SESSION_ID))
    dump_json(DATA_DIR/"PROCESS_LEDGER.json",LEDGER);dump_json(DATA_DIR/"GPU_SAMPLES.json",GPU_SAMPLES)
    write_run_summary()
    files=[p for p in sorted(SESSION_DIR.rglob("*")) if p.is_file() and p!=MANIFEST and p.suffix!=".tmp"]
    man=OrderedDict((str(p.relative_to(SESSION_DIR)),dict(sha256=sha_file(p),bytes=p.stat().st_size)) for p in files)
    dump_json(MANIFEST,dict(session=SESSION_ID,utc=utc_now(),simulation=SIM,note="SHA-256 of every file of this RUN (run folder with cartridges and private source copies included; those are hashed, not offered for download). No ZIP.",files=man))
    return str(MANIFEST)
def stage_records():
    package_session();return f"{len(FIG_FILES)} JPEG figures + {len(download_items())} records/texts, each downloadable directly · SHA-256 manifest of {len(json.load(open(MANIFEST))['files'])} files (no ZIP)"

# ---------------------------------------------------------------------------------------------------------------------
# THE RUN PIPELINE (one button)
# ---------------------------------------------------------------------------------------------------------------------
RUNS_DONE=[]
def run_pipeline():
    if RUNS_DONE:_session_paths(datetime.now().astimezone().strftime("SH782-%Y%m%d-%H%M%S")+f"-RUN{len(RUNS_DONE)+1}")
    RUNS_DONE.append(SESSION_ID);LIVE.clear();LIVE.update(session=SESSION_ID);LINES.clear();CHECKS.clear();FIG_FILES.clear();FIG_ERRORS.clear();PROVENANCE.clear()
    LEDGER.clear();GPU_SAMPLES.clear();ISO.update(mode=None,users={},netns=False,setpriv=False,probes={},notes=[],perm_maps=OrderedDict());ISO.pop("root_fallback",None)
    STATE.update(running=True,started=utc_now(),finished=None,current=None,elapsed=None);STATE["fig_version"]+=1
    for k in STAGES:STATE["stages"][k]=dict(status="wait",seconds=None,note="",t0=None)
    banner(f"RUN {SESSION_ID} · {local_now()} · five engine processes, one after the other (about 75–100 minutes on an A100, model download included)")
    def step(key,fn):
        STATE["current"]=key;stage_set(key,"run");_emit(f"── [{list(STAGES).index(key)+1}/{len(STAGES)}] {STAGES[key]}")
        try:
            note=fn();stage_set(key,"done",note);slog("STAGE_DONE",key,note=note);return True
        except Exception as ex:
            stage_set(key,"fail",f"{type(ex).__name__}: {ex}");slog("STAGE_FAILED",key,error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc()[-3000:]);return False
    try:
        ok=step("PRECHECK",stage_precheck) and step("ISOLATION",stage_isolation)
        for s in ENGINE_STAGES:
            if ok:ok=step(s,lambda s=s:stage_session(s))
            else:stage_set(s,"skip","not run — an earlier stage did not complete")
        try:apply_permissions("FINAL") if RUN_ROOT.exists() and ISO.get("mode") else None
        except Exception as ex:slog("PERMISSIONS_FINAL_FAILED",str(ex))
        if (rpath("q1_cartridges")/"Q1_CARTRIDGE_MANIFEST.json").is_file():step("VERIFY",stage_verify)
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
    RUN_THREAD["t"]=threading.Thread(target=run_pipeline,daemon=True,name="SH782-RUN");RUN_THREAD["t"].start();return True
# =====================================================================================================================
# PART 4 / 4 (continued) — Gradio interface (Silicon Hippocampus 1.5 / SH745 design): ONE button (RUN). The stages, the engine's own
#              output, the sealed cartridges and every text the sessions write appear while they work. The page refreshes
#              itself with short requests (gr.Timer) — a dropped connection never hides the figures; a reload shows all.
# =====================================================================================================================
LINEAGE=[("Research Record I — Qwen2.5-7B","https://doi.org/10.5281/zenodo.23381336"),
         ("Research Record II — Mistral-7B, Silicon Hippocampus v1.4","https://doi.org/10.5281/zenodo.23418927"),
         ("Research Record III — Qwen2.5-72B, Direct Internal-State Injection","https://doi.org/10.5281/zenodo.23434686"),
         ("Research record given by the author for this programme",ZENODO_REC)]
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
    tiles=[("QWEN-1","2 real documents → 2 cartridges"),("QWEN-2","native numerical MASTER_02"),("QWEN-3","reads MASTER_02 only"),("80/80","layer parity, 3 processes"),
           ("4","control conditions"),("PENDING","human review")]
    return (f'<div class="kz hero"><span class="rec">Live research demonstration · frozen Qwen2.5-72B-Instruct · NF4 · BF16 · CUT3 · A100 80 GB</span>'
            f'<div class="brand">{esc(APP_NAME)}</div><div class="title">{esc(APP_SUB)}</div>'
            '<div class="by">The same frozen model is started three times as three separate operating-system processes. The first reads two real documents — the European Commission '
            'page on AI in science and the Future of Life Institute statement on recursive self-improvement — and writes them into physical memory cartridges made of its own internal '
            'states. It ends. The second starts from nothing, sees only those cartridges, fuses them numerically into one sealed MASTER and ends. The third starts from nothing, sees '
            'only the MASTER — no text, no source — and says in human language what the memory holds.</div>'
            '<div class="tiles">'+"".join(f'<div class="tile"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a,b in tiles)+'</div>'
            f'<div class="by"><b>{esc(AUTHOR)}</b> · {esc(ORG)} · {esc(PLACE)} · {esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · <a href="{REPO}" target="_blank" rel="noopener">{esc(REPO)}</a></div></div>')
def mode_html():
    st=STATE
    if SIM:kind,t="err","SIMULATION — code test of the author with a fake model, NOT an experimental result"
    elif st.get("running"):
        el=(time.time()-datetime.fromisoformat(st["started"]).timestamp())/60 if st.get("started") else 0
        kind,t="info",f"RUN IN PROGRESS · {el:.0f} min · stage {list(STAGES).index(st['current'])+1 if st.get('current') else '…'}/{len(STAGES)}: {STAGES.get(st.get('current'),'')}"
    elif st.get("finished"):
        ok=run_verdict().startswith("COMPLETE");kind,t=("on" if ok else "err"),f"RUN {SESSION_ID} — {run_verdict()}"
    else:kind,t="info","NOT STARTED — press RUN. Five engine processes run one after the other on the A100 (about 75–100 minutes); everything they do appears here while they work."
    return card(t,"TEST782 has no earlier run in the repository: every value, text and figure on this page comes from THIS RUN. "
                f"Engine 782.py git blob <span class='mono'>{esc(LOCKS[ENGINE_NAME][:16])}…</span> · locked engine sources 709 · 730 · 757 · 764 · 779.",kind)
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
    with _LOG_LOCK:return "\n".join(list(CONSOLE)[-200:])

# ---------------------------------------------------------------------------------------------------------------------
# tab contents — read from THIS RUN's folders, unedited
# ---------------------------------------------------------------------------------------------------------------------
def overview_html():
    r1,r2,r3,rc=results_of("QWEN1"),results_of("QWEN2"),results_of("QWEN3"),results_of("CONTROLS")
    steps=[("CPU acceptance gate in its own process","AST dependency scan, 16 SHA / manifest simulations with the locked seal functions, tokenizer types; question panel sealed",results_of("PREFLIGHT").get("status")=="COMPLETE" or None),
           ("QWEN-1 reads two real documents — once","European Commission (AI in science) · Future of Life Institute (recursive self-improvement)",chk("QWEN1","TWO_SOURCE_CARTRIDGES_WRITTEN")),
           ("…and writes them into physical memory","SOURCE_A / SOURCE_B: H3 + K/V of layers 0–3 → SSD → SHA-256 of file and tensors; QWEN-1 ends",chk("QWEN1","SOURCE_REOPEN_INTEGRITY_SOURCE_B")),
           ("QWEN-2 starts from nothing — sees the cartridges only","reload with SHA checks; 80-layer seals equal to QWEN-1's (cross-process)",chk("QWEN2","SOURCE_CROSS_PROCESS_80_LAYER_PARITY_SOURCE_B")),
           ("…fuses them numerically into MASTER_02","locked TEST757 append + TEST764 recipe — no text, no summary; sealed; 80/80 parity",chk("QWEN2","MASTER_NUMERICAL_80_LAYER_PARITY")),
           ("QWEN-3 starts from nothing — sees MASTER_02 only","no source text, no source cartridge, no QWEN-2 output; independent 80/80 reload",chk("QWEN3","MASTER_INDEPENDENT_RELOAD")),
           ("…and says in human language what it holds","printed verbatim in Figure 7; the panel answers in Figure 8",bool(next((a for a in (r3.get("answers") or []) if a["id"]=="Q0"),None)) or None),
           ("Controls in a separate process","NO_MEMORY · SOURCE_A_ONLY · SOURCE_B_ONLY · BASELINE_MASTER on the same sealed questions",rc.get("status")=="COMPLETE" or None)]
    rows=[(Markup(f"<b>{i}. {esc(a)}</b><br><span class='small' style='opacity:.85'>{esc(b)}</span>"),Markup(ok_mark(v))) for i,(a,b,v) in enumerate(steps,1)]
    try:c=categories()
    except Exception:c=None
    cat=""
    if c:
        cat=tbl([("1 · Physical isolation (three sessions)",Markup((f"<b style='color:{'#08785B' if c['physical_os_enforced'] else '#B45309'}'>{esc(c['physical_label'])}</b>" if c["physical"][0] else ok_mark(False)) if r3 else "—")),("2 · Baseline MASTER (native, 7 mandatory checks)",Markup(ok_mark(c["baseline"][0]) if r2 else "—")),
                 ("3 · Autonomous MASTER (DrA decision)",Markup("<b style='color:#B45309'>NOT CREATED</b>")),("4 · New semantic synthesis",Markup("<b style='color:#B45309'>NOT EVALUATED</b>"))],["category (instruction §19 — separate)","this RUN"])
    arch=card("Physical memory outside the frozen model — what it is and what it is not",
        "<b>What is stored:</b> internal states of the frozen Qwen2.5-72B — the layer-3 output H3 and the K/V of layers 0–3 — in a file on the SSD, hashed, reloaded, injected at the layer-3 boundary.<br>"
        "<b>Native numerical MASTER:</b> QWEN-2 appends SOURCE_B to SOURCE_A inside the model (locked TEST757): the frozen model recomputes layers 4–79 of B while attending to A. "
        "MASTER_02 stores H3(A) ⊕ H3(B) and the fused K/V of layers 0–3; layers 4–79 are rebuilt bit-identically from the sealed boundary schedule (80/80). No text summary is ever re-tokenised.<br>"
        "<b>Not text RAG · not fine-tuning:</b> no document text in QWEN-3's prompt; the weights are frozen (sentinel identical in every session).<br>"
        "<b>Not a removal of the transformer:</b> layers 4–79 and decoding still run every time.<br>"
        "<b>Not proof of synthesis:</b> the fusion is a measured cross-attention footprint (Figure 4). Whether QWEN-3's text is a correct, new synthesis needs independent review (PENDING).<br>"
        "<b>DrA:</b> the repository contains no GPU-verified DrA decision mechanism (TEST773/774: the DRA axis had no measurable effect). An AUTONOMOUS_MASTER is therefore NOT created — only the BASELINE result is reported.","info")
    lin=card("Research lineage (published records and repositories — not results of this experiment)","<br>".join(f"{esc(t)} · <a href='{u}' target='_blank' rel='noopener'>{esc(u)}</a>" for t,u in LINEAGE)+
             f"<br>Engine sources used: 709 · 730 (native CUT3) · 757 (native append) · 764 (sealed boundary MASTER) · 779 (attention instrumentation) — <a href='{REPO}' target='_blank' rel='noopener'>{esc(REPO)}</a> · earlier: <a href='{REPO_V2}' target='_blank' rel='noopener'>{esc(REPO_V2)}</a>","info")
    return (card(f"What happens in this RUN ({SESSION_ID})",tbl(rows,["step","this RUN"]),"m")+(card("Four separate results",cat,"warn") if cat else "")+arch+lin)
def sources_html():
    r1=results_of("QWEN1");S=r1.get("sources") or {}
    if not S:return card("Sources and QWEN-1","Not available yet — QWEN-1 reads the two documents during RUN (stage 4).","info")
    out=""
    for cid in ("SOURCE_A","SOURCE_B"):
        s=S.get(cid) or {}
        rows=[("document",SRC_LABEL[cid]),("URL",s.get("url")),("page title",s.get("title")),("retrieved",f"{s.get('retrieved_utc')} · {s.get('mode')} · HTTP {s.get('http_status')}"),
              ("HTML SHA-256",s.get("html_sha256")),("text SHA-256",s.get("text_sha256")),("forged body SHA-256",s.get("body_sha256")),
              ("tokens (forged)",f"{s.get('body_tokens')} · TEST781 reference {s.get('reference_test781_tokens')} · full {s.get('tokens_full')} · truncated {s.get('truncated')}"),("extractor",s.get("extractor"))]
        txt=tload(rpath("q1_sources")/f"{cid}_TEXT.txt")
        out+=card(f"{cid} — {SRC_LABEL[cid]}",tbl(rows,mono_cols=(1,))+(details(f"opening of the extracted text (first 1,500 characters; the full text stays in QWEN-1's private folder and is not redistributed)",pre((txt or "")[:1500]+(" …" if txt and len(txt)>1500 else ""),260)) if txt else ""),"m")
    q1,_,_,_=manifests();E=q1.get("cartridges") or {}
    rows=[(c,e.get("role"),f"{e.get('body_tokens')}",f"{e.get('forge_seconds')} s",e.get("sha256"),(e.get("tensor_sha") or {}).get("h"),f"{(e.get('file_bytes') or 0)/1e6:.1f} MB") for c,e in E.items()]
    return out+card("Physical cartridges written by QWEN-1",tbl(rows,["id","role","body tokens","forge","file SHA-256","tensor seal H3","file"],mono_cols=(4,5)),"m")
def master_html():
    r2=results_of("QWEN2")
    if not r2:return card("MASTER_02 · QWEN-2","Not available yet — QWEN-2 runs after QWEN-1 has ended (stage 5).","info")
    _,q2,bm,rd=manifests();me=(bm.get("master") or (q2.get("cartridges") or {}).get("MASTER_02") or {})
    st=[(x.get("cid"),x.get("memory_tokens"),x.get("ssd_verify_ms"),x.get("h2d_ms"),x.get("fusion_ms")) for x in r2.get("fusion_steps") or []]
    mand=[(n,Markup(ok_mark(chk("QWEN2",n))),Markup(ok_mark(chk("QWEN3",n)))) for n in MANDATORY]
    ev=r2.get("qwen2_evaluation") or {};fp=r2.get("fusion_footprint") or {}
    rows=[("file SHA-256",me.get("sha256")),("tensor seal H3",(me.get("tensor_sha") or {}).get("h")),("tokens",me.get("n")),("parents",", ".join(f"{p['id']} {p['sha256'][:16]}…" for p in me.get("parents") or [])),
          ("rebuild schedule",json.dumps(me.get("rebuild_schedule"))),("condition",me.get("condition")),("autonomous MASTER",(r2.get("autonomous_master") or {}).get("status")),
          ("fusion footprint",json.dumps(fp)),("bundle READY",json.dumps(rd))]
    return (card("MASTER_02 — native numerical BASELINE MASTER",tbl(rows,mono_cols=(1,)),"m")+
            card("Native fusion steps (locked TEST757 append)",tbl(st,["cartridge","memory tokens","SSD verify ms","CPU→GPU ms","fusion ms"]),"info")+
            card("Seven mandatory MASTER checks",tbl(mand,["check","QWEN-2","QWEN-3 (new process)"]),"on" if all(chk("QWEN2",n) for n in MANDATORY[:6]) else "warn")+
            card("QWEN-2's own evaluation of the fused memory — PRIVATE record: never passed to QWEN-3, not used to build the MASTER, not a gate",
                 f"stated decision line: <b>{esc(ev.get('decision_line','—'))}</b> · {ev.get('tokens','—')} tokens"+textblock("QWEN-2 evaluation (verbatim)",text_file("QWEN2","QWEN2_EVALUATION_PRIVATE.txt")),"warn"))
def isolation_html():
    rows=[(SNAME[s],v.get("engine_pid"),f"{v.get('engine_user')} ({v.get('engine_uid')})","namespace" if v.get("netns") else ("offline" if v.get("offline") else "online"),
           f"{str(v.get('start',''))[11:19]} → {str(v.get('end',''))[11:19]}",v.get("exit_code"),f"{(v.get('gpu_release') or {}).get('used_mib')} MiB") for s,v in LEDGER.items()]
    pm="".join(details(f"permissions before {esc(ph)}",tbl([(n,f"{v['owner']}:{v['group']}",v["mode"]) for n,v in m.items() if v],["folder","owner:group","mode"],mono_cols=(1,2))) for ph,m in ISO.get("perm_maps",{}).items())
    r3=results_of("QWEN3")
    return (card("Process ledger — one OS process per session, strictly sequential",tbl(rows,["session","pid","user (uid)","network","start → end UTC","exit","GPU after exit"],mono_cols=(1,)) if rows else "no session yet","m")+
            card(f"Isolation set-up — mode {ISO.get('mode') or '—'}",pre(json.dumps(jsafe({k:v for k,v in ISO.items() if k!='perm_maps'}),indent=1),300)+pm,"info")+
            card("QWEN-3 access record (probes and python open-audit)",pre(json.dumps(jsafe({"access_probe":r3.get("access_probe"),"os_level_isolation":r3.get("os_level_isolation"),
                 "audit":r3.get("access_audit")}),indent=1),360) if r3 else "after QWEN-3","warn"))
def blind_html():
    r3=results_of("QWEN3");ans=r3.get("answers") or []
    if not r3:return card("QWEN-3 blind reading","Not available yet — QWEN-3 runs after QWEN-2 has ended (stage 6).","info")
    head=card("QWEN-3 — MASTER_02 only",f"process pid {r3.get('pid')} · user {esc(r3.get('user'))} (uid {r3.get('uid')}) · MASTER parity {(r3.get('master_parity') or {}).get('exact_layers','—')}/80 · "
              f"OS-level isolation: {esc(r3.get('os_level_isolation','—'))} · attention: {esc((r3.get('attention') or {}).get('status','—'))}","m")
    q0=next((a for a in ans if a["id"]=="Q0"),None)
    body=(card("Q0 · the MASTER expressed in human language (verbatim — also printed in Figure 7)",f"<b>{esc(q0['question'])}</b>"+pre(q0["answer"],700),"on") if q0 else "")
    body+="".join(card(f"{a['id']} · {a['kind']} · {a['tokens']} tokens",f"<b>{esc(a['question'])}</b>"+pre(a["answer"],420),"m") for a in ans if a["id"]!="Q0")
    return head+(body or card("answers","not written yet","info"))
def controls_html():
    rc=results_of("CONTROLS");cm=LIVE.get("metrics")
    if not rc:return card("Controls","Not available yet — the control session runs after QWEN-3 (stage 7).","info")
    out=""
    if cm:
        conds=list(cm["rows"]);qs=["Q0","Q1","Q2","Q3","Q4","Q5"]
        rows=[(c,*[Markup(f"A {cm['rows'][c].get(q,{}).get('a_hits','–')} · B {cm['rows'][c].get(q,{}).get('b_hits','–')}"+(" · UNKNOWN" if cm['rows'][c].get(q,{}).get('unknown') else "")) for q in qs]) for c in conds]
        out+=card("Source-specific vocabulary in every answer (lexical trace — not a grade)",tbl(rows,["condition"]+qs)+f"<div class='small'>{esc(cm['note'])} · reproduction: {esc(json.dumps(cm.get('reproduction')))}</div>","warn")
    for arm in ARMS:
        aa=[a for a in rc.get("answers") or [] if a["arm"]==arm]
        out+=card(f"{arm} · {len(aa)} answers · memory tokens {(rc.get('memory_tokens') or {}).get(arm,'—')}","".join(textblock(f"{a['id']} · {a['kind']}",a["answer"],f"{a['tokens']} tokens") for a in aa),"m")
    return out
def integrity_html():
    rows=[(c["utc"][11:19],SNAME.get(c["session"],c["session"]),c["name"],Markup(ok_mark(c["passed"]) if c["result"]!="DIAG" else "<b style='color:#B45309'>DIAG</b>"),c["detail"][:140]) for c in CHECKS]
    rp=results_of("PREFLIGHT");sims=[(r["id"],r["scenario"],r["expected"],r["observed"],Markup(ok_mark(r["pass"]))) for r in rp.get("sha_simulations") or []]
    src=[(n,v["git_blob"],v["sha256"],f"{v['bytes']:,}",v.get("obtained")) for n,v in SOURCES.items()];V=LIVE.get("verification") or {}
    return (card(f"Engine checks of this RUN — {sum(1 for c in CHECKS if c['result']=='PASS')} PASS · {sum(1 for c in CHECKS if c['result']=='FAIL')} FAIL · {sum(1 for c in CHECKS if c['result']=='DIAG')} DIAG",
                 tbl(rows,["UTC","session","check","result","detail"],mono_cols=(4,)) if rows else "none yet","on" if rows and all(c["passed"] for c in CHECKS) else "info")+
            card("CPU simulations before any GPU use (PREFLIGHT, locked seal functions)",tbl(sims,["id","scenario","expected","observed","result"]) if sims else "after PREFLIGHT","info")+
            card("AST dependency scan · tokenizer types · GPU budget (PREFLIGHT)",pre(json.dumps(jsafe({"ast_scan":{k:v for k,v in (rp.get("ast_scan") or {}).items() if k!="runtime_globals"},
                 "tokenizer":rp.get("tokenizer"),"gpu_budget_estimate":rp.get("gpu_budget_estimate"),"versions":rp.get("versions")}),indent=1),320) if rp else "after PREFLIGHT","info")+
            card("Independent re-verification after the run (read-only, host)",pre(json.dumps(jsafe({k:v for k,v in V.items()}),indent=1),420) if V else "after the last session","info")+
            card("Locked sources (git blob verified)",tbl(src,["file","git blob","SHA-256","bytes","obtained"],mono_cols=(1,2)),"info"))
def resources_html():
    out=""
    for s in SESSIONS:
        r=results_of(s)
        if not r:continue
        res=[(x["stage"],x.get("gpu_free_gib"),x.get("allocated_gib"),x.get("reserved_gib"),x.get("peak_allocated_gib"),x.get("rss_gib"),x.get("disk_free_gib")) for x in r.get("resources") or []]
        tm=[(k,", ".join(str(v) for v in vv)) for k,vv in (r.get("timings") or {}).items()]
        out+=card(f"{SNAME[s]} — resources and timings",(tbl(res,["stage","GPU free GiB","allocated","reserved","peak since previous","process RSS GiB","disk free GiB"]) if res else "")+
                  details("timings (s)",tbl(tm,["operation","seconds"])),"m")
    return out or card("Resources","after the first session","info")

TABS=["OVERVIEW","SOURCES · QWEN-1","MASTER · QWEN-2","ISOLATION","BLIND READING · QWEN-3","CONTROLS","INTEGRITY","RESOURCES","SCIENTIFIC FIGURES"]
TAB_HTML={"OVERVIEW":overview_html,"SOURCES · QWEN-1":sources_html,"MASTER · QWEN-2":master_html,"ISOLATION":isolation_html,"BLIND READING · QWEN-3":blind_html,
          "CONTROLS":controls_html,"INTEGRITY":integrity_html,"RESOURCES":resources_html}
def _figlabel(k):m=FIGURES[k];return f"Figure {m['n']} — {m['title']}"
def tab_gallery(tab):
    keys=[k for k,m in FIGURES.items() if (m["tab"]==tab or tab=="SCIENTIFIC FIGURES") and k in FIG_FILES]
    return [(FIG_FILES[k]["jpg"],f"{_figlabel(k)} · {FIG_FILES[k]['badge']}") for k in keys]
def figs_status_html():
    n=len(FIG_FILES);tot=len(FIGURES)
    if not n and not FIG_ERRORS:return card(f"Scientific figures of this RUN — 0/{len(BASE_FIGURES)}","The twelve figures are drawn from this RUN's outputs after the last session (stage 9). They appear here, one below the other.","info")
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
        con=_tb(lines=12,max_lines=20,label="Live engine output of this RUN — every line the session processes print (session | line); progress bars update one line; also ENGINE_OUTPUT_REALTIME.log",value=console_text(),interactive=False)
        fstat=gr.HTML(_safe(figs_status_html));main_figs=gr.HTML(_safe(figs_main_html))
        jpgs=gr.File(label="The JPEG figures of this RUN, in order — each file downloads with one tap",value=(jpg_files() or None),file_count="multiple",interactive=False)
        files=gr.File(label="Real-time engine output, session logs and results, manifests, texts written by QWEN-2 / QWEN-3 / CONTROLS, verification — direct downloads (no ZIP)",value=(all_files() or None),file_count="multiple",interactive=False)
        htmls={};gals={}
        with gr.Tabs():
            for t in TABS:
                with gr.Tab(t):
                    if t in TAB_HTML:htmls[t]=gr.HTML(_safe(TAB_HTML[t]))
                    gals[t]=_gallery(label=f"{t} · figures",value=tab_gallery(t))
        gr.HTML(f'<div class="kz small" style="opacity:.8;margin:10px 0 18px">{esc(AUTHOR)} · {esc(ORG)} · {esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · '
                f'<a href="{file_url(EVID_DIR/ENGINE_NAME)}" download="782.py">782.py (the locked copy executed here)</a> · <a href="{URL_LICENSE}" target="_blank" rel="noopener">LICENSE</a> · '
                'Source documents © European Commission and © Future of Life Institute — linked, hash-recorded, not redistributed · '
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
            port=int(re.search(r":(\d+)",str(local)).group(1));_co.serve_kernel_port_as_window(port,anchor_text="▶ Open the AKBASCORE TEST782 interface (Colab window)");window=f"Colab port window, port {port}"
        except Exception as ex:window=f"not available ({type(ex).__name__})"
    dump_json(GRADIO_LINK.with_suffix(".json"),dict(utc=utc_now(),session=SESSION_ID,share_url=share,local_url=local,colab_window=window,share_error=err))
    GRADIO_LINK.write_text(f"{share or local}\n",encoding="utf-8")
    banner(f"INTERFACE OPEN · {share or ('local only: '+str(local))}\n  public link : {share or '— (tunnel not available; use the Colab window link above)'}\n  local       : {local}\n"
           f"  Press RUN in the interface — everything else runs automatically. If the link stops working: run  launch_interface()  in a new cell.","#")
    slog("LAUNCH","interface open",share_url=share,local_url=local,colab_window=window);return share or local
def keep_cell_running():
    """keeps this Colab cell RUNNING while the interface is in use; when a RUN has finished its figures are shown here too"""
    banner("THE CELL STAYS RUNNING — the interface is live. Press RUN in the interface; the engine output is printed here and shown in the interface.\n"
           f"  A full RUN takes about 75–100 minutes on an A100. Stop this cell (■) only when you have finished; the files stay in {DEMO_ROOT}","#")
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
    slog("ENGINE_READY","782.py locked; it runs unchanged as five OS processes when RUN is pressed",git_blob=LOCKS[ENGINE_NAME])
_missing=[n for n in (1,2,3) if n not in _AKB782_PARTS]
if _missing:raise RuntimeError(f"PART {_missing} of the program is missing in this cell — paste PART 1, 2, 3 and 4 one below the other, each completely (every part ends with an END OF PART line)")
try:startup()
except Exception as _ex:
    _m=str(_ex)
    _hint=("No copy with the locked git blob was found, not even the embedded one: paste PART 1, 2, 3 and 4 again exactly as delivered (nothing "
           "cut off or edited), then run the cell again. The program stops instead of running unverified code." if "NOT AVAILABLE" in _m else
           "Network error while downloading a locked source from GitHub: run the cell again." if any(x in _m for x in ("URLError","timed out","HTTP Error","Connection","Name or service")) else
           "See the traceback above; nothing was run.")
    banner(f"START-UP FAILED — {type(_ex).__name__}: {_m}\nWHAT TO DO: {_hint}\nRecords of this attempt: {SESSION_DIR}","!")
    raise
launch_interface()
if os.environ.get("AKB782_NO_BLOCK")!="1":keep_cell_running()
# ===== END OF PART 4/4 =====


