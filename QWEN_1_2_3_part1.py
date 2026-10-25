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
