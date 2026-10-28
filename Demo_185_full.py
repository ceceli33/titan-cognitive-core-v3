# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST815 · LIVE RESEARCH DEMONSTRATION (Gradio, SH782 / SH745 infrastructure)
# Cognitive cartridges and a closed-loop evidence controller inside ONE frozen 72B transformer
#   22 physical CUT3 cartridges on SSD (2 real PLOS articles via Europe PMC + 20 synthetic decoys) · native H3 routing with
#   no labels · adaptive closed loop (read → challenge → reverse → decide) vs fixed 4-read policy · evidence-removal controls
#   · same-run replay · frozen weights. The TEST815 engine runs UNCHANGED; this program only shows what it does.
# Qwen/Qwen2.5-72B-Instruct · NF4 4-bit frozen · BF16 · CUT3 · NVIDIA A100-SXM4-80GB · ONE Google Colab cell
# PART 1 / 4 — locked engine (815.py embedded), run folder, the engine process and its real-time evidence
# THIS PART  59,646 characters · its last line is  # ===== END OF PART 1/4 =====
# ===== END OF PART 1/4 =====
# ---------------------------------------------------------------------------------------------------------------------
# HOW TO RUN  Paste PART 1, 2, 3 and 4 one below the other into ONE Colab cell (A100 80 GB runtime, fresh) and run it.
#             Each part is shorter than 80,000 characters and ends with an END OF PART line — check that line after every
#             paste. The interface opens with ONE button: RUN. RUN executes the locked TEST815 engine (815.py, git blob
#             verified) as its own OS process; every line it prints is received, time-stamped and shown at once. Afterwards
#             this program re-verifies the cartridges read-only, draws twelve JPEG figures from THIS run's outputs and
#             offers every record for direct download (no ZIP). Nothing in the engine is changed or re-implemented.
# STATUS      The engine was executed on an A100 by the researcher (TEST815.log). This demonstration layer was tested by its
#             author on a CPU only (simulation with the published log; no model).
# AUTHOR      Mustafa Akbaş · AkbasCore AI Teknoloji · Mersin, Türkiye · Copyright © 2026 Mustafa Akbaş
#             AKBASCORE RESEARCH SOFTWARE LICENSE — https://github.com/ceceli33/titan-cognitive-core-v3/blob/main/LICENSE
#             Source articles: PLOS (via Europe PMC) — linked and hash-recorded, not redistributed by this demonstration.
#             Qwen2.5-72B-Instruct and third-party libraries remain governed by their own licences.
# =====================================================================================================================
import os,sys,re,io,ast,json,time,html,math,shutil,hashlib,platform,threading,traceback,subprocess,importlib.util,textwrap,types,gc,csv
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
from matplotlib.patches import Rectangle,FancyBboxPatch,FancyArrowPatch,Circle
from matplotlib.lines import Line2D
from matplotlib.colors import LogNorm,ListedColormap,LinearSegmentedColormap,Normalize
from PIL import Image
import gradio as gr
import urllib.request
SIM=os.environ.get("AKB815_SIM")=="1"          # code author's CPU simulation only — never an experimental result

# ---------------------------------------------------------------------------------------------------------------------
# identity, locks, colours
# ---------------------------------------------------------------------------------------------------------------------
APP_NAME="AKBASCORE SILICON HIPPOCAMPUS";APP_SUB="TEST815 · Cognitive Cartridges · Native H3 Routing · Closed-Loop Evidence Control"
APP_SHORT="AKBASCORE Silicon Hippocampus · TEST815 · Qwen2.5-72B · CUT3";CODE_VERSION="SH815-demo-1.0";EXPERIMENT="TEST815"
AUTHOR="Mustafa Akbaş";ORG="AkbasCore AI Teknoloji";PLACE="Mersin, Türkiye"
LICENSE_NAME="AKBASCORE RESEARCH SOFTWARE LICENSE";COPYRIGHT="Copyright © 2026 Mustafa Akbaş"
REPO="https://github.com/ceceli33/titan-cognitive-core-v3";RAW_BASE="https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
URL_LICENSE=REPO+"/blob/main/LICENSE";URL_815=REPO+"/blob/main/815.py";URL_815_LOG=REPO+"/blob/main/815.log"
ENGINE_NAME="815.py"
LOCKS=OrderedDict([("815.py","77774f87428c0243c9a86ea6a041364acd9c1b03"),           # TEST815 engine — executed byte-for-byte
                   ("LICENSE","9aad4724d1072f9e56486650a9527380c867a53b")])
# locks the ENGINE itself verifies at run time (fail-closed inside 815.py); recorded here for the figures and records
ENGINE_CHAIN=OrderedDict([("790.py","d7e4c4b21e9c3c46276845940a9621751b23897f"),("789.py","56daecf29d54286b82e3f4b03387229a0f9547fb"),
                          ("779.py","fa7017a87f25ecef6ed2b2954a850599cb25fcd9"),("709.py","6c9f8cbb1eeed848d45133d73f0d7676b68e9125"),
                          ("730.py","b1bad9eb3b111b44413f8ef05a3a140ab66a77dd"),("757.py","3d88bf8638390995858f23391f1e043faa586835"),
                          ("721.py","7c6575beddca87f02c344ee1a132f02b191dc00a"),("764.py","99acb97cde2b11c0c23e14a3ed11cb6f5d7f3902")])
MODEL_ID="Qwen/Qwen2.5-72B-Instruct"
REAL={"PMC9521804":dict(short="Credit for data",doi="10.1371/journal.pcbi.1010476",title="Ten simple rules for getting and giving credit for data",journal="PLOS Computational Biology"),
      "PMC9401135":dict(short="Data availability",doi="10.1371/journal.pone.0272845",title="Long-term availability of data associated with articles in PLOS ONE",journal="PLOS ONE")}
COL=dict(A="#2455D6",B="#C12566",SYN="#9CA3AF",LOOP="#7626D9",FIX="#B45309",OK="#08785B",HOST="#6B7280",GOLD="#D97706")
OK_COL="#08785B";NEU="#374151";BG="#FFFFFF";INK="#111827";INK2="#374151";MUTED="#6B7280";RULE="#D1D5DB";PANEL="#F8FAFC";RED="#B91C1C";AMBER="#B45309"
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
# directories and logs — every RUN has its own session folder; the engine writes its own run folder (ROOT) unchanged
# ---------------------------------------------------------------------------------------------------------------------
_CROOT=Path("/content") if os.path.isdir("/content") else Path("/tmp")
DEMO_ROOT=_CROOT/"AKBASCORE_TEST815_DEMO";EVID_DIR=DEMO_ROOT/"locked_sources"
SESSION_ID=SESSION_DIR=FIG_DIR=DATA_DIR=SESSION_LOG=SESSION_EVENTS=ENGINE_OUT=RUN_SUMMARY=MANIFEST=VERIFY_FILE=None
def _session_paths(sid):
    global SESSION_ID,SESSION_DIR,FIG_DIR,DATA_DIR,SESSION_LOG,SESSION_EVENTS,ENGINE_OUT,RUN_SUMMARY,MANIFEST,VERIFY_FILE
    SESSION_ID=sid;SESSION_DIR=DEMO_ROOT/"sessions"/sid;FIG_DIR=SESSION_DIR/"figures";DATA_DIR=SESSION_DIR/"records"
    SESSION_LOG=SESSION_DIR/"SESSION.log";SESSION_EVENTS=SESSION_DIR/"SESSION_EVENTS.jsonl";ENGINE_OUT=SESSION_DIR/"ENGINE_OUTPUT_REALTIME.log"
    RUN_SUMMARY=SESSION_DIR/"RUN_SUMMARY.txt";MANIFEST=SESSION_DIR/"SHA256_MANIFEST.json";VERIFY_FILE=DATA_DIR/"POST_RUN_VERIFICATION.json"
    for d in (DEMO_ROOT,DEMO_ROOT/"sessions",SESSION_DIR,FIG_DIR,DATA_DIR,EVID_DIR):d.mkdir(parents=True,exist_ok=True)
_session_paths(datetime.now().astimezone().strftime("SH815-%Y%m%d-%H%M%S"))
_OUT=sys.stdout;_LOG_LOCK=threading.Lock();CONSOLE=deque(maxlen=600);PROG_OPEN={"open":False}
def _emit(line,progress=False):
    """one console line. Progress-bar updates replace the previous progress line in the interface; in the Colab cell they are
    printed as ordinary full lines, at most one every 30 s (no carriage returns — nothing can stay invisible in the cell)"""
    with _LOG_LOCK:
        if progress and CONSOLE and CONSOLE[-1].startswith("⟳ "):CONSOLE[-1]="⟳ "+line[:300]
        elif progress:CONSOLE.append("⟳ "+line[:300])
        else:CONSOLE.append(line[:400])
    try:
        if progress:
            if time.time()-PROG_OPEN.get("cell_t",0)<30:return
            PROG_OPEN["cell_t"]=time.time();line="⟳ "+line
        _OUT.write(line[:900]+"\n");_OUT.flush()
    except Exception:pass
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
# EMBEDDED holds byte-exact copies (zlib + base64) of the locked files, written by the build script. A copy is used only after
# its git blob is recomputed and found equal to the lock above, so the cell needs no upload and never runs an unverified file.
EMBEDDED={                                   # generated by the build — do not edit; checked against LOCKS before use
 "815.py":(  # 49783 bytes · git blob 77774f87428c0243c9a86ea6a041364acd9c1b03
  "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"
 ),
 "LICENSE":(  # 4525 bytes · git blob 9aad4724d1072f9e56486650a9527380c867a53b
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
    """order: verified cache → repository (raw GitHub) → /content/<name> → embedded copy. Every candidate must have the locked git
    blob; a candidate with another blob is never executed and is reported. How the file was obtained is recorded for every run."""
    p=EVID_DIR/name;want=LOCKS[name];notes=[]
    if p.is_file() and git_blob(p.read_bytes())==want:
        raw=p.read_bytes();prev=SOURCES.get(name) or {}
        how=prev.get("obtained") or "cached copy from an earlier start-up (blob verified)";notes=list(prev.get("notes") or [])
    else:
        raw=None;how=None
        if p.is_file():notes.append(f"cached {p.name} has git blob {git_blob(p.read_bytes())[:12]}… (not the lock) — not used")
        try:
            req=urllib.request.Request(RAW_BASE+name,headers={"User-Agent":"AKBASCORE-TEST815-DEMO"})
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
# pipeline state — the engine's own progress is shown as nine live stages, recognised from its unchanged output lines
# ---------------------------------------------------------------------------------------------------------------------
STAGES=OrderedDict([
    ("PRECHECK","Pre-flight — one A100 80 GB, empty GPU, disk, locked engine 815.py (git blob), fresh session folder"),
    ("LOCKS","Engine start — locked TEST790 / 789 / 779 / 709 / 730 / 757 / 721 / 764 definitions verified by git blob inside the engine"),
    ("SOURCES","Two real articles from Europe PMC — exact DOI and title locks, scientific text extracted, SHA-256 recorded"),
    ("MODEL","Frozen Qwen2.5-72B-Instruct loaded (NF4, BF16 compute) — weight sentinel taken"),
    ("CARTRIDGES","22 physical CUT3 cartridges forged and sealed on the SSD — 20 synthetic decoys + 2 real articles"),
    ("ROUTING","Native H3 routing — every question's own layer-3 states scored against all 22 cartridges; 8 paraphrase controls"),
    ("LOOP","Closed loop — 16 questions × ADAPTIVE (read → challenge → reverse → decide) and FIXED (4 reads) policies"),
    ("ABLATION","Evidence removal — each real article removed in turn, best surviving cartridge read natively (16 trials)"),
    ("REPLAY","Same-run replay — ranking and first answer recomputed from the same physical memory (8 cases)"),
    ("ACCEPT","Engine acceptance — frozen weights, no residual hooks, review CSV and public audit written"),
    ("VERIFY","Independent re-verification by this program (read-only) — cartridge files, records, consistency with the live log"),
    ("FIGURES","Twelve scientific figures (JPEG 300 dpi, layout QC) — heat maps, closed-loop maps, controls, claims"),
    ("RECORDS","Records — real-time engine output, results, manifests, review CSV (direct downloads, no ZIP)")])
ENGINE_STAGES=("LOCKS","SOURCES","MODEL","CARTRIDGES","ROUTING","LOOP","ABLATION","REPLAY","ACCEPT")
STAGE_MARK=[("SOURCES",r"^PASS API_HOST"),("MODEL",r"^PASS QUESTION_NO_BODY_REPLAY"),("CARTRIDGES",r"^PASS (FROZEN|NF4|CARD_NONEMPTY_)"),
            ("ROUTING",r"^PASS PHYSICAL_22_CARTRIDGES"),("LOOP",r"^PASS PARAPHRASE_EIGHT"),("ABLATION",r"^PASS ABLATION_RANK_21_"),
            ("REPLAY",r"^PASS SOURCE_REMOVAL_16"),("ACCEPT",r"^PASS REPLAY_EIGHT")]
STATE=dict(started=None,finished=None,current=None,stages={k:dict(status="wait",seconds=None,note="",t0=None) for k in STAGES},version=0,running=False,fig_version=0,elapsed=None,meas=None)
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
LINES=[]                            # every engine line: (utc, stream, line)
CHECKS=[]                           # every PASS / FAIL line of the engine (utc · name · detail)
GPU_SAMPLES=[]                      # nvidia-smi samples during the whole run (time, used MiB, compute apps)
EV=dict(root=None,commits=[],routes=[],rows=[],ablation=[],replay=[],fusion=[],records={},failed=None,stage=None,stage_t={})

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
def _reach(url):
    """GET of the first bytes of a real resource (some servers refuse HEAD or the bare API root)"""
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"AKBASCORE-TEST815-DEMO","Range":"bytes=0-255"}),timeout=20) as f:f.read(256);return f"HTTP {getattr(f,'status',200)}"
    except Exception as ex:return f"{type(ex).__name__}: {str(ex)[:80]}"
def stage_precheck():
    g=nvsmi("gpu=name,memory.total,memory.used,driver_version");rows=[x.split(", ") for x in g]
    LIVE["gpu"]=dict(count=len(rows),name=rows[0][0] if rows else None,total_mib=int(rows[0][1]) if rows else None,used_mib=int(rows[0][2]) if rows else None,
                     driver=rows[0][3] if rows else None,apps=nvsmi("compute-apps=pid,used_memory"))
    if SIM:LIVE["gpu"].update(count=1,name="SIMULATED A100-SXM4-80GB",total_mib=81920,used_mib=0,apps=[])
    if not LIVE["gpu"]["count"]:raise RuntimeError("no NVIDIA GPU in this runtime — TEST815 needs one A100 80 GB (Runtime → Change runtime type → A100). Nothing was run.")
    if "A100" not in str(LIVE["gpu"]["name"]) or (LIVE["gpu"]["total_mib"] or 0)<70000:raise RuntimeError(f"A100 80 GB required, found {LIVE['gpu']['name']} — the engine refuses A100 40 GB by design")
    if (LIVE["gpu"]["used_mib"] or 0)>2048 or LIVE["gpu"]["apps"]:
        raise RuntimeError(f"the GPU is not empty ({LIVE['gpu']['used_mib']} MiB used, processes {LIVE['gpu']['apps']}) — restart the Colab runtime, then run the cell again")
    du=shutil.disk_usage(str(_CROOT));cache=_dir_bytes(model_cache_dir()) or 0
    LIVE["disk"]=dict(free_gib=round(du.free/2**30,1),model_cache_gib=round(cache/2**30,1),hf_home=str(hf_home()))
    need=20 if cache>130e9 else 170;LIVE["disk"]["needed_gib"]=need
    if du.free/2**30<need and not SIM:raise RuntimeError(f"not enough disk: {du.free/2**30:.0f} GiB free, about {need} GiB needed")
    for n in LOCKS:RAW[n]=fetch_locked(n)
    LIVE["network"]={} if SIM else {"github":_reach(RAW_BASE+"790.py"),"europe_pmc":_reach("https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9521804/fullTextXML"),
                                         "huggingface":_reach(f"https://huggingface.co/{MODEL_ID}/resolve/main/config.json")};LIVE["network"]["hf_token"]="set" if (os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")) else "not set (anonymous download — allowed, may be slower)"
    LIVE["precheck"]=dict(locks={n:SOURCES[n]["git_blob"] for n in LOCKS},engine_obtained=SOURCES[ENGINE_NAME]["obtained"],utc=utc_now())
    return (f"{LIVE['gpu']['name']} · used {LIVE['gpu']['used_mib']} MiB of {LIVE['gpu']['total_mib']} MiB · disk free {LIVE['disk']['free_gib']} GiB · model cache {LIVE['disk']['model_cache_gib']} GiB · "
            f"815.py git blob {LOCKS[ENGINE_NAME][:12]}… ({SOURCES[ENGINE_NAME]['obtained']})"+(f" · network: {LIVE['network']}" if LIVE.get("network") else ""))

# ---------------------------------------------------------------------------------------------------------------------
# THE ENGINE PROCESS — 815.py (locked) as its own OS process; every line is received, time-stamped, written to
# ENGINE_OUTPUT_REALTIME.log and drives the live stages. Progress bars update ONE line (no flooding).
# ---------------------------------------------------------------------------------------------------------------------
PROGRESS={"line":"","t":0.0};PROC={"p":None};LAST_OUT={"t":time.time(),"line_t":time.time(),"line":""}
PROG_RX=re.compile(r"\d+%\|.*\||\[\d+:\d+<|it/s\]|s/it\]|B/s\]|^Download complete|^Reconstruction complete|^Fetching \d+ files")
KNOWN_HEAD=("PASS","FAIL","TEST815","NATIVE_FUSION_STEP","PHYSICAL_COMMIT","FILES","Traceback")
def _js(line):
    try:return json.loads(line.split(" ",1)[1])
    except Exception:return None
def _engine_stage(key,note=None):
    cur=EV["stage"]
    if cur==key:return
    if cur:stage_set(cur,"done",_stage_note(cur))
    EV["stage"]=key;EV["stage_t"][key]=time.time();STATE["current"]=key;PROGRESS["line"]="";stage_set(key,"run",note or "");_emit(f"── [{list(STAGES).index(key)+1}/{len(STAGES)}] {STAGES[key]}")
def _stage_note(k):
    if k=="LOCKS":return f"{sum(1 for c in CHECKS if c['name'].startswith(('GIT_LOCK_','TEST79','TEST77')) and c['passed'])} lock checks passed"
    if k=="SOURCES":return " · ".join(f"{x.get('pmcid')} {x.get('doi')}" for x in EV["records"].get("sources",[])) or "articles loaded"
    if k=="MODEL":return "frozen model loaded (NF4) — weight sentinel recorded"
    if k=="CARTRIDGES":return f"{len(EV['commits'])} physical cartridges committed (SHA-256 at commit)"
    if k=="ROUTING":return f"{len(EV['routes'])}/8 paraphrase routing controls · top-1 same {sum(1 for r in EV['routes'] if r.get('same_top1'))}/8"
    if k=="LOOP":return f"{len(EV['rows'])}/16 cases · adaptive reads {sum(r.get('adaptive_reads',0) for r in EV['rows'])} · fixed reads {sum(r.get('fixed_reads',0) for r in EV['rows'])}"
    if k=="ABLATION":return f"{len(EV['ablation'])}/16 removal trials · abstentions {sum(1 for a in EV['ablation'] if a.get('native_action')=='ABSTAIN')}"
    if k=="REPLAY":return f"{len(EV['replay'])}/8 replays · exact first answers {sum(1 for r in EV['replay'] if r.get('exact_initial_answer_identical'))}"
    if k=="ACCEPT":return str((EV["records"].get("acceptance") or {}).get("verdict","engine acceptance"))
    return ""
def _on_line(line,stream):
    u=utc_now();LAST_OUT["t"]=time.time()
    with _LOG_LOCK:
        LINES.append((u,stream,line))
        new=not ENGINE_OUT.exists()
        with ENGINE_OUT.open("a",encoding="utf-8") as f:f.write(f"{u}\t{stream}\t{line}\n")
        if new:_private(ENGINE_OUT)
    if PROG_RX.search(line) and not line.startswith(KNOWN_HEAD):
        PROGRESS["line"]=short(line,160)
        if time.time()-PROGRESS["t"]>1.0:PROGRESS["t"]=time.time();_emit(f"TEST815 · {PROGRESS['line']}",progress=True)
        if EV["stage"]:STATE["stages"][EV["stage"]]["note"]="engine: "+PROGRESS["line"];bump()
        return
    LAST_OUT["line_t"]=time.time();LAST_OUT["line"]=line[:160]
    _emit(f"  TEST815 | {line[:300]}")
    if EV["stage"]:   # the running stage always shows what the engine is doing right now (as in the SH782 demo)
        k_=EV["stage"];base=_stage_note(k_) if k_ in ("CARTRIDGES","ROUTING","LOOP","ABLATION","REPLAY") else ""
        STATE["stages"][k_]["note"]=(base+" · " if base else "")+"engine: "+short(line,140);bump()
    for key,rx in STAGE_MARK:
        if re.search(rx,line) and list(STAGES).index(key)>list(STAGES).index(EV["stage"] or "LOCKS"):_engine_stage(key)
    m=re.match(r"^(PASS|FAIL) ([A-Za-z0-9_.]+) ?(.*)$",line)
    if m:
        CHECKS.append(dict(utc=u,name=m.group(2),result=m.group(1),passed=(m.group(1)=="PASS"),detail=m.group(3).strip()[:600]))
        if m.group(1)=="FAIL":slog("ENGINE_FAIL",m.group(2),detail=m.group(3)[:500])
    head=line.split(" ",1)[0]
    if head=="PHYSICAL_COMMIT":
        p=line.split();EV["commits"].append(dict(id=p[1],sha256=p[2] if len(p)>2 else None,utc=u))
        STATE["stages"]["CARTRIDGES"]["note"]=f"{len(EV['commits'])}/22 cartridges sealed · last {p[1]}";bump()
    elif head=="TEST815_SOURCE_LOADED":
        p=line.split(" ",3);EV["records"].setdefault("sources",[]).append(dict(pmcid=p[1],doi=p[2] if len(p)>2 else None,title=p[3] if len(p)>3 else None))
    elif head in ("TEST815_ROUTE_PARAPHRASE","TEST815_ROW","TEST815_ABLATION","TEST815_REPLAY"):
        d=_js(line)
        if d is not None:
            {"TEST815_ROUTE_PARAPHRASE":EV["routes"],"TEST815_ROW":EV["rows"],"TEST815_ABLATION":EV["ablation"],"TEST815_REPLAY":EV["replay"]}[head].append(d)
            if EV["stage"]:STATE["stages"][EV["stage"]]["note"]=_stage_note(EV["stage"]);bump()
    elif head=="NATIVE_FUSION_STEP":
        m2=re.match(r"NATIVE_FUSION_STEP TEST815_(\S+) (\S+) (\{.*\})$",line)
        if m2:
            try:d=dict(ast.literal_eval(m2.group(3)));d.update(tag=m2.group(1),cid=m2.group(2),utc=u);EV["fusion"].append(d)
            except Exception as ex:slog("PARSE_NOTE","NATIVE_FUSION_STEP line not parsed",error=f"{type(ex).__name__}: {ex}",line=line[:200])
    elif head in ("TEST815_COST_MATRIX","TEST815_POLICY_COMPARISON","TEST815_ABLATION_SUMMARY","TEST815_REPLAY_SUMMARY","TEST815_DEMO_ACCEPTANCE","TEST815_PUBLIC_AUDIT","TEST815_COMPLETED"):
        d=_js(line)
        if d is not None:EV["records"][{"TEST815_DEMO_ACCEPTANCE":"acceptance"}.get(head,head.replace("TEST815_","").lower())]=d
        if head=="TEST815_COMPLETED":slog("ENGINE_COMPLETED","TEST815 completed",verdict=(d or {}).get("demo_acceptance",{}).get("verdict"))
    elif head=="TEST815_REVIEW_EXPORT":
        p=line.split()
        if len(p)>1:EV["root"]=str(Path(p[1]).parent)
    elif head=="FILES":
        p=line.split()
        if len(p)>1:EV["root"]=str(Path(p[1]).parent)
    elif head=="TEST815_FAILED":EV["failed"]=line[:500];slog("ENGINE_FAILED",line[:400])
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
def _sampler(stop):
    """nvidia-smi every 10 s while the engine runs (kept in memory and in GPU_SAMPLES.json — not printed)"""
    while True:
        used,total=gpu_used_mib();apps=nvsmi("compute-apps=pid,used_memory")
        if SIM:used,total=int(38000+3000*math.sin(time.time()/7)),81920
        GPU_SAMPLES.append(dict(utc=utc_now(),t=time.time(),stage=EV["stage"],used_mib=used,total_mib=total,apps=apps))
        if stop.wait(2 if SIM else 10):break
def _disk_used_gib():
    """used space of the disk that holds the Hugging Face cache (where the model download lands)"""
    try:
        p=hf_home()
        while not p.exists() and p!=p.parent:p=p.parent
        du=shutil.disk_usage(str(p));return (du.total-du.free)/2**30
    except Exception:return None
def _mmss(s):s=int(max(0,s));return f"{s//60} min {s%60:02d} s"
def _live_text():
    """one line that says what the engine is doing now — measured, never guessed (rebuilt at every interface refresh)"""
    k=EV["stage"];st=STATE["stages"].get(k) or {};t_in=time.perf_counter()-(st.get("t0") or time.perf_counter());d_gb,g_gib=STATE.get("meas") or (0.0,0.0)
    age=time.time()-LAST_OUT["line_t"]
    if k=="MODEL":
        what=(f"loading the frozen 72B weights onto the GPU · GPU {g_gib:.1f} GiB" if g_gib>=1.0 else
              f"downloading the model weights (≈145 GB) · {d_gb:.1f} GB written to disk so far" if d_gb>=0.5 else "fetching / checking the model files (≈145 GB)")
    else:what=f"GPU {g_gib:.1f} GiB in use"
    pr=f" · {PROGRESS['line'][:80]}" if PROGRESS["line"] and time.time()-PROGRESS["t"]<120 else ""
    return f"⟳ working · {_mmss(t_in)} in this stage · {what}{pr} · last engine line {int(age)} s ago"
def _heartbeat(stop):
    """proof of life, independent of the engine's own output: every 10 s the running stage shows a live line in the interface
    (time in stage, measured disk growth = download, GPU memory = loading, last progress bar); every 60 s without a new
    engine line the same line is also written to the Colab cell. Nothing is stopped automatically; 20 min without any change
    is reported plainly."""
    t0=time.perf_counter();d0=_disk_used_gib();last=None;still=0;n=0
    while not stop.wait(10):
        n+=1;STATE["elapsed"]=round(time.perf_counter()-t0)
        d=_disk_used_gib();g,_=gpu_used_mib();d_gb=max(0.0,((d or 0)-(d0 or 0))*2**30/1e9);g_gib=(g or 0)/1024
        STATE["meas"]=(d_gb,g_gib);bump()
        if n%6:continue
        if time.time()-LAST_OUT["line_t"]<60:still=0;continue
        sig=(round(d or 0,1),g,PROGRESS["line"]);still=still+1 if sig==last else 0;last=sig
        msg=f"TEST815 · {(time.perf_counter()-t0)/60:.0f} min since start · stage {EV['stage']} · "+_live_text().replace("⟳ ","")
        slog("ENGINE_STATUS",msg)
        if still==20:slog("ENGINE_NO_CHANGE","no new engine line, no disk growth and no GPU change for 20 minutes — the engine process is still alive; "
                          "if this persists, check the network / Hugging Face availability (the run is not stopped automatically)",pid=(PROC["p"].pid if PROC["p"] else None))
def _find_root(t_start):
    if EV["root"] and Path(EV["root"]).is_dir():return Path(EV["root"])
    c=[p for p in _CROOT.glob("AKBASCORE_TEST779_*") if p.is_dir() and p.stat().st_mtime>=t_start-5 and (p/"TEST815.log").exists()]
    return max(c,key=lambda p:p.stat().st_mtime) if c else None
def engine_cmd():
    eng=EVID_DIR/ENGINE_NAME
    if SIM and os.environ.get("AKB815_SIM_ENGINE"):return [sys.executable,"-u",os.environ["AKB815_SIM_ENGINE"]]
    return [sys.executable,"-u",str(eng)]
def run_engine():
    """starts the locked engine as ONE OS process and follows it until it exits; the nine engine stages advance from its own output"""
    for k in ("root","failed","stage"):EV[k]=None
    for k in ("commits","routes","rows","ablation","replay","fusion"):EV[k]=[]
    EV["records"]={};EV["stage_t"]={}
    cmd=engine_cmd();env=dict(os.environ,PYTHONUNBUFFERED="1",PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True")
    if git_blob((EVID_DIR/ENGINE_NAME).read_bytes())!=LOCKS[ENGINE_NAME]:raise RuntimeError("815.py on disk does not match its lock — not executed")
    t0=time.time();_engine_stage("LOCKS")
    slog("ENGINE_START","TEST815 · "+" ".join(cmd[:3]),cwd=str(_CROOT))
    p=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=str(_CROOT),env=env,bufsize=0)
    PROC["p"]=p;stop=threading.Event();LIVE["engine"]=dict(pid=p.pid,start=utc_now(),start_t=t0,cmd=cmd)
    th=[threading.Thread(target=_reader,args=(p.stdout,"stdout"),daemon=True),threading.Thread(target=_reader,args=(p.stderr,"stderr"),daemon=True),
        threading.Thread(target=_sampler,args=(stop,),daemon=True),threading.Thread(target=_heartbeat,args=(stop,),daemon=True)]
    for t in th:t.start()
    rc=p.wait();th[0].join(60);th[1].join(60);stop.set();STATE["meas"]=None
    root=_find_root(t0);EV["root"]=str(root) if root else None
    LIVE["engine"].update(end=utc_now(),end_t=time.time(),seconds=round(time.time()-t0,1),exit_code=rc,root=EV["root"])
    used,_=gpu_used_mib();LIVE["engine"]["gpu_after_mib"]=0 if SIM else used
    dump_json(DATA_DIR/"ENGINE_PROCESS.json",LIVE["engine"]);dump_json(DATA_DIR/"GPU_SAMPLES.json",GPU_SAMPLES)
    slog("ENGINE_EXIT",f"TEST815 exit code {rc} · {LIVE['engine']['seconds']:.0f} s",root=EV["root"],gpu_after_mib=LIVE["engine"]["gpu_after_mib"])
    ok=(rc==0 and "TEST815_COMPLETED" in "".join(l for _,_,l in LINES[-40:]) and not EV["failed"])
    cur=EV["stage"]
    if ok:
        stage_set(cur,"done",_stage_note(cur))
        for k in ENGINE_STAGES:
            if STATE["stages"][k]["status"]=="wait":stage_set(k,"skip","marker not seen in the engine output")
    else:
        last=next((l for _,_,l in reversed(LINES) if l.startswith(("FAIL ","TEST815_FAILED"))),None) or (EV["failed"] or f"exit code {rc}")
        stage_set(cur or "LOCKS","fail",f"engine ended: {last[:400]}")
        for k in ENGINE_STAGES:
            if STATE["stages"][k]["status"]=="wait":stage_set(k,"skip","not reached — the engine stopped earlier")
        raise RuntimeError(f"TEST815 engine ended without completion: {last[:300]}")
    return root
_AKB815_PARTS=globals().setdefault("_AKB815_PARTS",set());_AKB815_PARTS.add(1)
# ===== END OF PART 1/4 =====
# ===== PART 2/4 — paste directly after PART 1 in the same cell =====
# =====================================================================================================================
# PART 2 / 4 — the records of THIS run (engine files first, the live engine output as fallback), the independent
#              read-only verification, descriptive host statistics of the sealed cartridges, and the figure toolkit
#              (JPEG 300 dpi, layout QC). Nothing here routes, reads, decides or writes memory — that is the engine's work.
# THIS PART  28,101 characters · its last line is  # ===== END OF PART 2/4 =====
# =====================================================================================================================
if not {1}<=globals().get("_AKB815_PARTS",set()):raise RuntimeError("PART "+str(sorted({1}-globals().get("_AKB815_PARTS",set())))+" of the program is missing above this part in the cell — paste PART 1, 2, 3 and 4 one below the other, each completely (every part ends with an END OF PART line)")
_AKB815_PARTS=globals().setdefault("_AKB815_PARTS",set())
# ---------------------------------------------------------------------------------------------------------------------
# records of this run (read from the engine's own run folder; cached by mtime; partial files are fine while it runs)
# ---------------------------------------------------------------------------------------------------------------------
_RC={}
def rroot():return Path(EV["root"]) if EV.get("root") else None
def rfile(name):
    r=rroot();return (r/name) if r else None
def _cached(name):
    p=rfile(name)
    if not p or not p.is_file():return None
    try:st=p.stat();k=(str(p),st.st_mtime_ns,st.st_size)
    except Exception:return None
    if _RC.get(name,(None,None))[0]!=k:
        v=jload(p)
        if v is None:return (_RC.get(name) or (None,None))[1]
        _RC[name]=(k,v)
    return _RC[name][1]
def results():return _cached("TEST815_results.json") or {}
def manifest():return _cached("TEST815_manifest.json") or {}
def _live_root():
    """while the engine runs, its run folder is found from the newest AKBASCORE_TEST779_* folder created after RUN"""
    if EV.get("root") or not LIVE.get("engine"):return
    t0=LIVE["engine"].get("start_t") or 0
    c=[p for p in _CROOT.glob("AKBASCORE_TEST779_*") if p.is_dir() and p.stat().st_mtime>=t0-5]
    if c:EV["root"]=str(max(c,key=lambda p:p.stat().st_mtime))
REAL_IDS=("PMC9521804","PMC9401135")
BASE_Q=[f"Q{i}" for i in range(1,9)];CASES=BASE_Q+[q+"_PARA" for q in BASE_Q]
def rows():return results().get("rows") or []
def row(cid):return next((r for r in rows() if r.get("case_id")==cid),None)
def row_logs():return {r["case_id"]:r for r in EV["rows"] if isinstance(r,dict) and r.get("case_id")}
def routes():return results().get("routing_robustness") or EV["routes"]
def ablation():return results().get("source_removal_ablation") or EV["ablation"]
def replay():return results().get("replay_audit") or EV["replay"]
def rget(key,logkey=None):
    v=results().get(key)
    return v if v not in (None,{},[]) else (EV["records"].get(logkey or key) or {})
def summary():return rget("summary","completed")
def acceptance():return rget("demo_acceptance","acceptance")
def cost():return rget("cost_matrix")
def policy():return rget("policy_comparison")
def ab_summary():return rget("ablation_summary")
def rp_summary():return rget("replay_summary")
def documents():return results().get("documents") or {}
def relation():return results().get("relation_audit") or {}
def questions():
    Q=OrderedDict((c,None) for c in CASES)
    for c,t in results().get("question_panel") or []:Q[c]=t
    for r in rows():Q[r["case_id"]]=r.get("question")
    return Q
def ckey(c):return (0,REAL_IDS.index(c)) if c in REAL_IDS else (1,str(c))
def cartridge_ids():
    E=(manifest().get("cartridges") or {})
    if E:return sorted(E,key=ckey)
    return sorted({c["id"] for c in EV["commits"]},key=ckey)
def is_real(c):return str(c).startswith("PMC")
def ccol(c):return COL["A"] if c=="PMC9521804" else (COL["B"] if c=="PMC9401135" else COL["SYN"])
def cshort(c):return REAL.get(c,{}).get("short",c)
def relevant(case):
    r=row(case)
    if r:return list((r.get("offline_routing_eval") or {}).get("relevant_sources") or [])
    L=row_logs().get(case) or {};return list((L.get("offline_routing_eval") or {}).get("relevant_sources") or [])
def score_matrix():
    """16 × 22 native H3 routing scores, exactly as the engine logged them (original questions and paraphrases)"""
    ids=cartridge_ids();R={r["case_id"]:r for r in routes()}
    if not ids or not R:return None,ids
    M=np.full((len(CASES),len(ids)),np.nan)
    for i,c in enumerate(CASES):
        r=R.get(c.removesuffix("_PARA"))
        if not r:continue
        sc=r.get("paraphrase_scores" if c.endswith("_PARA") else "original_scores") or {}
        for j,k in enumerate(ids):
            if k in sc:M[i,j]=float(sc[k])
    return M,ids
FUSE_RX=re.compile(r"^(Q\d+(?:_PARA)?)_(ADAPTIVE|FIXED)_(.+)$")
def tracks(policy_):
    """operation sequence of each case for one policy: from the results file, or rebuilt from the live NATIVE_FUSION_STEP lines"""
    out=OrderedDict()
    for r in rows():
        st=(r.get(policy_.lower()) or {}).get("steps") or []
        out[r["case_id"]]=[dict(op=s.get("operation"),ids=list(s.get("ids") or []),raw=s.get("raw"),tokens=s.get("tokens"),sec=s.get("elapsed_seconds"),
                                trunc=s.get("possible_truncation"),end=s.get("sentence_end")) for s in st]
    if out:return out
    for f in EV["fusion"]:
        m=FUSE_RX.match(f["tag"])
        if not m or m.group(2)!=policy_.upper():continue
        L=out.setdefault(m.group(1),[])
        if L and L[-1]["op"]==m.group(3) and f["cid"] not in L[-1]["ids"] and len(L[-1]["ids"])<2:L[-1]["ids"].append(f["cid"])
        else:L.append(dict(op=m.group(3),ids=[f["cid"]],raw=None,tokens=None,sec=None))
    return out
def fusion_records():
    """every NATIVE_FUSION_STEP of this run (the engine's own instrumentation line): SSD verify, CPU→GPU, fusion ms, memory tokens"""
    out=[]
    for f in EV["fusion"]:
        m=FUSE_RX.match(f["tag"]);kind=(m.group(2) if m else ("REPLAY" if "REPLAY" in f["tag"] else ("ABLATION" if "_DROP_" in f["tag"] else "OTHER")))
        out.append(dict(kind=kind,**{k:f.get(k) for k in ("tag","cid","ssd_verify_ms","h2d_ms","fusion_ms","memory_tokens","utc")}))
    return out
def acc_val(k,default=None):
    a=acceptance();return a.get(k,default) if a else default

# ---------------------------------------------------------------------------------------------------------------------
# VERIFY — independent, read-only (host). The cartridges are re-hashed, re-opened and described; records are cross-checked
# against each other and against the live engine output. Nothing is recomputed in place of the engine.
# ---------------------------------------------------------------------------------------------------------------------
def _load_cp(p):
    import torch
    return torch.load(p,map_location="cpu",weights_only=True)
def _np(t):
    t=t.float();return t.numpy() if hasattr(t,"numpy") else np.asarray(t)
def _h3_strip(h,cols=320,cbins=64):
    """|H3| mean per (channel bin × token column) — a picture of the stored layer-3 states (descriptive only)"""
    n,Hd=h.shape;cb=max(1,Hd//cbins);a=np.abs(h[:,:cb*cbins]).reshape(n,cbins,cb).mean(-1)
    edges=np.linspace(0,n,min(cols,n)+1).astype(int)
    return np.stack([a[s:e].mean(0) for s,e in zip(edges[:-1],edges[1:]) if e>s],1)
def stage_verify():
    _live_root();root=rroot();man=manifest();res=results()
    if not root or not root.is_dir():raise RuntimeError("the engine's run folder was not found — nothing to verify (nothing is substituted)")
    if not man.get("cartridges"):raise RuntimeError("TEST815_manifest.json missing in the run folder — nothing to verify")
    V=dict(root=str(root),cartridges=OrderedDict(),records={},consistency={},problems=[],utc=utc_now());P_=[]
    probs=V["problems"];E=man["cartridges"];ids=sorted(E,key=ckey)
    fp={};strips={};norms={}
    for cid in ids:
        e=E[cid];p=root/"physical_cartridges"/e["file"];row_=dict(id=cid,role=e.get("role"),present=p.is_file(),body_tokens=e.get("body_tokens"),n=e.get("n"))
        if p.is_file():
            t=time.perf_counter();s=sha_file(p);row_.update(bytes=p.stat().st_size,sha256_now=s,sha256_manifest=e.get("sha256"),file_sha_ok=(s==e.get("sha256")),hash_s=round(time.perf_counter()-t,2))
            commit=next((c for c in EV["commits"] if c["id"]==cid),None)
            if commit and commit.get("sha256"):row_["sha256_at_commit_line"]=commit["sha256"];row_["commit_line_ok"]=(commit["sha256"]==s)
            try:
                cp=_load_cp(p);h=_np(cp["h"][0]);P_.append(int(cp["p"]))
                row_.update(book_id_ok=(cp.get("book_id")==cid),length_ok=(int(cp["n"])==int(cp["p"])+int(cp["body_tokens"])==int(e.get("n",-1))),
                            h_shape=list(h.shape),hidden=int(h.shape[1]),lower_layers=len(cp.get("lower") or []),p=int(cp["p"]))
                body=h[int(cp["p"]):].astype(np.float32);mu=body.mean(0);fp[cid]=mu/(np.linalg.norm(mu)+1e-12)
                norms[cid]=np.linalg.norm(body,axis=1)
                if is_real(cid):strips[cid]=_h3_strip(body)
                del cp,h,body
            except Exception as ex:row_["open_error"]=f"{type(ex).__name__}: {str(ex)[:160]}"
        V["cartridges"][cid]=row_
        for k in ("present","file_sha_ok","book_id_ok","length_ok","commit_line_ok"):
            if k in row_ and row_[k] is False:probs.append(f"{cid} {k}")
        if "open_error" in row_:probs.append(f"{cid} could not be opened")
        STATE["stages"]["VERIFY"]["note"]=f"cartridge {len(V['cartridges'])}/{len(ids)} re-hashed · {cid}";bump()
    gc.collect()
    if fp:
        F=np.stack([fp[c] for c in ids if c in fp]);F=F-F.mean(0,keepdims=True);F=F/(np.linalg.norm(F,axis=1,keepdims=True)+1e-12);C=F@F.T;keep=[c for c in ids if c in fp]
        mx=max(len(v) for v in norms.values());NP=np.full((len(keep),mx),np.nan)
        for i,c in enumerate(keep):NP[i,:len(norms[c])]=norms[c]
        np.savez_compressed(DATA_DIR/"CARTRIDGE_ANATOMY.npz",ids=np.array(keep),cos=C,norms=NP,**{f"strip_{c}":v for c,v in strips.items()});_private(DATA_DIR/"CARTRIDGE_ANATOMY.npz")
        LIVE["anatomy"]=dict(ids=keep,cos=C,norms=NP,strips=strips)
        V["host_statistics"]=dict(note="mean body H3 per cartridge, L2-normalised, centred on the bank mean; cosine between cartridges; per-token ‖H3‖. Descriptive only — the engine's router does not use these numbers.",
                                  real_vs_real=float(C[keep.index(REAL_IDS[0]),keep.index(REAL_IDS[1])]) if all(r in keep for r in REAL_IDS) else None)
    # records: the files the engine wrote, cross-checked with what it printed while it ran
    def fsha(n):
        p=root/n;return sha_file(p) if p.is_file() else None
    R=V["records"];R["results_status"]=res.get("status");R["results_present"]=bool(res)
    R["review_csv_sha256"]=fsha("TEST815_independent_review.csv");R["public_audit_sha256"]=fsha("TEST815_public_audit.json")
    exp=next((l for _,_,l in LINES if l.startswith("TEST815_REVIEW_EXPORT")),"").split()
    R["review_csv_ok"]=bool(R["review_csv_sha256"]) and R["review_csv_sha256"]==(res.get("independent_review") or {}).get("sha256")==(exp[2] if len(exp)>2 else None)
    pa=EV["records"].get("public_audit") or {}
    R["public_audit_ok"]=bool(R["public_audit_sha256"]) and R["public_audit_sha256"]==(res.get("public_audit") or {}).get("sha256")==pa.get("sha256")
    R["summary_equals_live_line"]=(json.dumps(jsafe(res.get("summary")),sort_keys=True)==json.dumps(jsafe(EV["records"].get("completed")),sort_keys=True)) if EV["records"].get("completed") else None
    R["acceptance_equals_live_line"]=(json.dumps(jsafe(res.get("demo_acceptance")),sort_keys=True)==json.dumps(jsafe(EV["records"].get("acceptance")),sort_keys=True)) if EV["records"].get("acceptance") else None
    R["engine_log_present"]=(root/"TEST815.log").is_file()
    if R["engine_log_present"]:
        el=[l.rstrip() for l in (tload(root/"TEST815.log") or "").splitlines() if l.startswith(("PASS ","FAIL "))];ll=[l.rstrip() for _,_,l in LINES if l.startswith(("PASS ","FAIL "))]
        R["engine_log_gates_equal_live"]=(el==ll);R["engine_log_gates"]=len(el)
    for k in ("review_csv_ok","public_audit_ok","summary_equals_live_line","acceptance_equals_live_line","engine_log_gates_equal_live"):
        if R.get(k) is False:probs.append("RECORD "+k)
    # consistency of the counts the figures use
    C_=V["consistency"];rw=rows();sm=res.get("summary") or {}
    C_["gates_pass"]=sum(1 for c in CHECKS if c["passed"]);C_["gates_fail"]=sum(1 for c in CHECKS if not c["passed"])
    C_["rows"]=len(rw)
    for pol in ("adaptive","fixed"):
        n=sum((r.get(pol) or {}).get("read_count",0) for r in rw);ns=sum(len((r.get(pol) or {}).get("steps") or []) for r in rw)
        nf=sum(1 for f in EV["fusion"] if (FUSE_RX.match(f["tag"]) or [None,None,None])[2]==pol.upper())
        ni=sum(len(s.get("ids") or []) for r in rw for s in (r.get(pol) or {}).get("steps") or [])
        tsum=round(sum(float(s.get("elapsed_seconds") or 0) for r in rw for s in (r.get(pol) or {}).get("steps") or []),3)
        C_[pol]=dict(reads=n,steps=ns,summary_reads=sm.get(f"{pol}_native_reads"),fusion_lines=nf,fused_cartridge_reads=ni,
                     read_seconds_recomputed=tsum,read_seconds_engine=(cost().get(pol) or {}).get("read_wall_seconds_sum"))
        ok=n==ns==sm.get(f"{pol}_native_reads") and nf==ni and abs(tsum-float(C_[pol]["read_seconds_engine"] or -1))<0.01
        C_[pol]["ok"]=ok
        if not ok:probs.append(f"COUNTS {pol}")
    rp=replay();C_["replay_sha_identical"]=sum(1 for x in rp if x.get("initial_original_sha256") and x.get("initial_original_sha256")==x.get("initial_replay_sha256"));C_["replay_cases"]=len(rp)
    C_["gpu_after_exit_mib"]=(LIVE.get("engine") or {}).get("gpu_after_mib");C_["gpu_released"]=(C_["gpu_after_exit_mib"] is not None and C_["gpu_after_exit_mib"]<2048)
    if C_["gates_fail"]:probs.append(f"ENGINE {C_['gates_fail']} FAIL line(s)")
    if C_["gpu_released"] is False:probs.append("GPU not released after the engine exited")
    LIVE["verification"]=V;dump_json(VERIFY_FILE,V)
    # copies of the engine's small records for direct download (hash-checked); source texts and .pt files stay in the run folder
    cp_dir=DATA_DIR/"engine_records";cp_dir.mkdir(exist_ok=True);V["copied"]={}
    for n in ("TEST815_results.json","TEST815_manifest.json","TEST815.log","TEST815_independent_review.csv","TEST815_public_audit.json","SEALED_PANEL.json"):
        p=root/n
        if p.is_file():
            q=cp_dir/n;shutil.copyfile(p,q);_private(q);V["copied"][n]=(sha_file(q)==sha_file(p))
    dump_json(VERIFY_FILE,V)
    nok=sum(1 for r in V["cartridges"].values() if r.get("file_sha_ok") and r.get("book_id_ok") and r.get("length_ok"))
    note=(f"{nok}/{len(ids)} cartridge files re-hashed (SHA-256 = manifest = commit line) and re-opened · review CSV {okm(R['review_csv_ok'])} · public audit {okm(R['public_audit_ok'])} · "
          f"summary = live line {okm(R['summary_equals_live_line'])} · reads adaptive {C_['adaptive']['reads']} / fixed {C_['fixed']['reads']} consistent {okm(C_['adaptive']['ok'] and C_['fixed']['ok'])} · "
          f"engine gates {C_['gates_pass']} PASS / {C_['gates_fail']} FAIL · GPU after exit {C_['gpu_after_exit_mib']} MiB")
    slog("VERIFIED",note)
    if probs:raise RuntimeError(note+" · PROBLEMS: "+", ".join(probs))
    return note

# ---------------------------------------------------------------------------------------------------------------------
# figure toolkit (SH782 house style) — 13.333 × 7.5 in, 300 dpi JPEG, every text checked for overlap / clipping
# ---------------------------------------------------------------------------------------------------------------------
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.linewidth":.9,"axes.edgecolor":NEU,"axes.labelcolor":INK,"xtick.color":NEU,"ytick.color":NEU,
                     "xtick.labelsize":8.5,"ytick.labelsize":8.5,"axes.labelsize":9.5,"axes.titlesize":10.5,"axes.titleweight":"bold","axes.titlelocation":"left",
                     "legend.fontsize":8.5,"legend.frameon":False})
FW,FH=13.333,7.5;OUT_DPI=300;MONO="DejaVu Sans Mono"
FIGURES=OrderedDict([
    ("F1",dict(n=1,title="Cognitive Cartridges + Closed Loop — This Run at a Glance",slug="ARCHITECTURE_AND_RESULTS",tab="OVERVIEW")),
    ("F2",dict(n=2,title="The Memory Bank — 22 Physical Cartridges on the SSD",slug="CARTRIDGE_BANK",tab="CARTRIDGE BANK")),
    ("F3",dict(n=3,title="Native H3 Routing — 16 Questions × 22 Cartridges",slug="H3_ROUTING_HEATMAP",tab="H3 ROUTING")),
    ("F4",dict(n=4,title="Paraphrase Robustness — Same Meaning, Different Words",slug="PARAPHRASE_ROBUSTNESS",tab="H3 ROUTING")),
    ("F5",dict(n=5,title="The Closed Loop — Every Read of Every Question",slug="CLOSED_LOOP_DECISION_MAP",tab="CLOSED LOOP")),
    ("F6",dict(n=6,title="Efficiency — Adaptive Control vs a Fixed Four-Read Policy",slug="ADAPTIVE_VS_FIXED_COST",tab="CLOSED LOOP")),
    ("F7",dict(n=7,title="Hypothesis Evolution — First Reading → Final Answer (verbatim)",slug="HYPOTHESIS_EVOLUTION",tab="ANSWERS")),
    ("F8",dict(n=8,title="Causal Evidence Removal — Take the Source Away",slug="EVIDENCE_REMOVAL",tab="EVIDENCE CONTROLS")),
    ("F9",dict(n=9,title="Numeric Fact and Relation Audit — Q2 · Q8 (verbatim)",slug="FACT_RELATION_AUDIT",tab="EVIDENCE CONTROLS")),
    ("F10",dict(n=10,title="Same-Run Replay — Ranking and First Answer Recomputed",slug="SAME_RUN_REPLAY",tab="REPLAY · INTEGRITY")),
    ("F11",dict(n=11,title="Native Fusion Timing, GPU Memory and Engine Gates",slug="TIMING_GPU_GATES",tab="RESOURCES")),
    ("F12",dict(n=12,title="What This Run Demonstrates — Claims Ledger",slug="CLAIMS_LEDGER",tab="OVERVIEW"))])
BASE_FIGURES=OrderedDict(FIGURES)
FIG_FILES={};FIG_ERRORS={};PROVENANCE={}
BADGE_COL={"SCHEMATIC":NEU,"LIVE MEASUREMENT":OK_COL,"ENGINE RECORD":COL["LOOP"],"SEALED MEMORY":COL["A"],"HOST STATISTIC":AMBER,"VERIFICATION RECORD":NEU,"NOT PRODUCED IN THIS RUN":RED}
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
    T(fig,.035,.022,f"{APP_NAME} · {EXPERIMENT} · demo {CODE_VERSION} · {_date()} · 815.py git blob {LOCKS[ENGINE_NAME][:10]} · run {SESSION_ID}"+(" · SIMULATION" if SIM else "")+f" · Figure {meta['n']}/{len(BASE_FIGURES)}",
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
    stem=("SIMULATION_" if SIM else "")+f"TEST815_FIG{num:02d}_{meta['slug']}{suffix}";jpg=FIG_DIR/(stem+".jpg")
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
    fig_footer(fig,key,"Placeholder by design: TEST815 figures are drawn only from outputs of this RUN (the published TEST815.log is never substituted).")
    return save_fig(fig,key,"NOT PRODUCED IN THIS RUN",["(none — output missing)"],"_NOT_PRODUCED")
def _axstyle(ax,fs=8):
    for s in ("top","right"):ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=fs)
def kpi(fig,x,y,w,h,value,label,col,sub=None):
    """one large number tile (value of THIS run) — used in Figures 1 and 12"""
    box(fig,x,y,w,h,ec=col,fc="white",lw=1.6);rect(fig,x,y+h-.012,w,.012,col,z=2)
    Tc(fig,x+.006,x+w-.006,y+h*.58,value,size=21,weight="bold",color=col)
    Tc(fig,x+.006,x+w-.006,y+h*.26,label,size=7.8,color=INK)
    if sub:Tc(fig,x+.006,x+w-.006,y+h*.10,sub,size=6.6,color=MUTED)
def pill(fig,x,y,w,h,text,fc,tc="white",size=8.0,weight="bold"):
    p=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=.008",transform=fig.transFigure,fc=fc,ec="none",zorder=2);fig.add_artist(p)
    return Tc(fig,x+.003,x+w-.003,y+h/2,text,size=size,weight=weight,color=tc)
OPS=OrderedDict([("INITIAL",("read top-1","#2563EB")),("FUSE_TO_CHALLENGE_INITIAL",("challenge: fuse top-2","#7626D9")),("ALTERNATE_AFTER_UNKNOWN",("UNKNOWN → read alternate","#D97706")),
                 ("FUSE_ALTERNATE_FIRST",("fuse, alternate first","#C2410C")),("REVERSE_EVIDENCE_CHECK",("reverse-order check","#DB2777")),("ALTERNATE_EVIDENCE_CHECK",("alternate check","#0F766E")),
                 ("SECOND",("fixed: read #2","#9CA3AF")),("PAIR",("fixed: pair","#6B7280")),("REVERSE",("fixed: reverse pair","#4B5563"))])
def opcol(op):return OPS.get(op,(op,"#9CA3AF"))[1]
def oplab(op):return OPS.get(op,(op,"#9CA3AF"))[0]
_AKB815_PARTS.add(2)
# ===== END OF PART 2/4 =====
# ===== PART 3/4 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 4 — the twelve scientific figures (1–9 here, 10–12 in PART 4). Each is drawn only from THIS run's engine
#              records, the live engine output and the host's read-only verification; a missing record is drawn as missing.
# THIS PART  39,401 characters · its last line is  # ===== END OF PART 3/4 =====
# =====================================================================================================================
if not {1,2}<=globals().get("_AKB815_PARTS",set()):raise RuntimeError("PART "+str(sorted({1,2}-globals().get("_AKB815_PARTS",set())))+" of the program is missing above this part in the cell — paste PART 1, 2, 3 and 4 one below the other, each completely (every part ends with an END OF PART line)")
def L_(c):return {"PMC9521804":"A","PMC9401135":"B"}.get(c,"S")
def ids_lab(ids):return "+".join(L_(c) if is_real(c) else c for c in ids)
def evidence_classes():
    """source-removal trials grouped by what the engine's own offline label says is left in the bank"""
    out=OrderedDict(none_left=[],other_left=[],irrelevant=[])
    for a in ablation():
        rel=set(relevant(a["case_id"]));rem=a.get("removed")
        if rem in rel:(out["other_left"] if rel-{rem} else out["none_left"]).append(a)
        else:out["irrelevant"].append(a)
    return out
def _n_ab(L):return sum(1 for a in L if a.get("native_action")=="ABSTAIN")
def _layout_text(fig,text,x0,x1,y0,y1,fs_max=9.6,fs_min=5.6,color=INK):
    """verbatim text, wrapped, at the largest font that fits the area (never cut silently: an overflow is marked …)"""
    raw=str(text or "").replace("\t","    ").split("\n");Hpt=(y1-y0)*FH*72
    for fs in np.arange(fs_max,fs_min-1e-9,-0.2):
        chars=max(20,int((x1-x0)*FW*72/(fs*0.60)));lines=[]
        for ln in raw:lines+=(textwrap.wrap(ln,chars,break_long_words=True) or [""])
        if len(lines)<=int(Hpt/(fs*1.36)):
            fig.text(x0,y1,mt("\n".join(lines)),fontsize=fs,va="top",ha="left",color=color,linespacing=1.3,family="DejaVu Sans");return float(fs)
    per=max(1,int(Hpt/(fs_min*1.36)));lines[per-1]=lines[per-1][:-2]+" …"
    fig.text(x0,y1,mt("\n".join(lines[:per])),fontsize=fs_min,va="top",ha="left",color=color,linespacing=1.3,family="DejaVu Sans");return fs_min

def fig1():
    k="F1";sm=summary();ac=acceptance();rp=rp_summary()
    if not sm or not ac:return fig_missing(k,"The overview is drawn from the engine's final summary and acceptance record of this RUN.","The engine did not complete in this RUN (no TEST815_COMPLETED / demo_acceptance record).")
    fig=fig_base(k,"One frozen 72B model · memory kept outside the weights as its own sealed internal states on the SSD · a controller that decides what to read next · every number from THIS run","ENGINE RECORD")
    ar,fr=sm.get("adaptive_native_reads"),sm.get("fixed_native_reads");ev=evidence_classes()
    sav=f"−{100*(1-ar/fr):.0f} % reads" if ar and fr else "—";nl=ev["none_left"];ir=ev["irrelevant"]
    tiles=[(f"{sm.get('source_count','—')}","physical cartridges",f"{ac.get('real_sources')} real articles + {ac.get('synthetic_controls')} decoys",COL["A"]),
           (f"{sm.get('routing_top2_relevant')}/{sm.get('cases')}","right article in top-2","no labels · no titles · no text",OK_COL),
           (f"{sm.get('decoy_selected_cases')}/{sm.get('cases')}","questions with a decoy in top-2","20 synthetic controls in the bank",OK_COL),
           (f"{ar} vs {fr}","native reads, 16 questions",f"adaptive vs fixed · {sav}",COL["LOOP"]),
           (f"{sm.get('unknown_recovery_observed')}","recoveries from UNKNOWN","the loop read the alternate",COL["GOLD"]),
           (f"{_n_ab(nl)}/{len(nl)}","abstained when evidence gone","no relevant article left",COL["B"]),
           (f"{len(ir)-_n_ab(ir)}/{len(ir)}","still answered","an irrelevant article removed",OK_COL),
           (f"{rp.get('initial_answer_exact','—')}/{rp.get('cases','—')}","identical replay","ranking + first answer",OK_COL)]
    W=(.93-7*.008)/8
    for i,(v,l,s,c) in enumerate(tiles):kpi(fig,.035+i*(W+.008),.70,W,.165,v,l,c,s)
    st=[("SOURCES",COL["A"],["Europe PMC · 2 PLOS articles","DOI + title locked, SHA-256",f"{sum(int((documents().get(c) or {}).get('physical_text_tokens') or 0) for c in REAL_IDS) or '—'} tokens kept"]),
        ("FORGE · frozen 72B",COL["HOST"],["each text read once","layer-3 states H3 + K/V L0–3","no training · no fine-tuning"]),
        ("SSD MEMORY BANK",COL["A"],[f"{len(manifest().get('cartridges') or {})} sealed .pt files","SHA-256 at commit and reload",f"host re-hash {sum(1 for r in ((LIVE.get('verification') or {}).get('cartridges') or {}).values() if r.get('file_sha_ok'))}/22"]),
        ("NATIVE H3 ROUTER",OK_COL,["the question's own H3 states","scored against all 22","top-2 handed to the loop"]),
        ("CLOSED LOOP",COL["LOOP"],["read → challenge → reverse","stops when evidence agrees",f"{ar} reads for 16 questions"]),
        ("DECISION",COL["B"],[f"ANSWER {sm.get('adaptive_answers','—')} · ABSTAIN {16-int(sm.get('adaptive_answers') or 0)}","UNKNOWN if unsupported","verbatim → Figure 7"])]
    BW=.142;G=(.93-6*BW)/5
    for i,(t,c,ls) in enumerate(st):
        x=.035+i*(BW+G);box(fig,x,.395,BW,.235,ec=c,lw=1.6);rect(fig,x,.595,BW,.035,c,z=2)
        Tc(fig,x+.004,x+BW-.004,.6125,t,size=9.2,weight="bold",color="white")
        for j,l in enumerate(ls):Tc(fig,x+.006,x+BW-.006,.555-j*.048,l,size=8.0,color=INK)
        if i<5:arrow(fig,x+BW+.002,.51,x+BW+G-.002,.51,col=NEU,lw=1.5,ms=11)
    x5=.035+5*(BW+G);x4=.035+4*(BW+G)
    arrow(fig,x5+BW*.5,.395,x4+BW*.5,.395,col=COL["LOOP"],lw=1.5,ms=11,cs="arc3,rad=-0.3",ls="--")
    Tc(fig,x4+BW*.2,x5+BW*.8,.33,"UNKNOWN or disagreement → read more",size=7.6,color=COL["LOOP"],weight="bold")
    ex=[("Memory that is not text",COL["A"],"The articles live as the model's own internal states — layer-3 hidden states and the K/V of layers 0–3 (CUT3). At question time they are fused back natively and layers 4–79 recompute everything. No article text enters the prompt."),
        ("A blind choice among decoys",OK_COL,f"Each question is turned into its own layer-3 states and compared with all 22 cartridges — no titles, no labels. 20 synthetic decoys sit in the same bank; one reached the top-2 in {sm.get('decoy_selected_cases')} of {sm.get('cases')} questions."),
        ("Evidence-sensitive control",COL["LOOP"],f"The loop reads, challenges the first answer with a second source and checks the order. Remove the right article and it says UNKNOWN instead of inventing: {_n_ab(nl)}/{len(nl)} when no relevant article was left.")]
    for i,(t,c,s) in enumerate(ex):
        x=.035+i*.314;box(fig,x,.105,.302,.205,ec=c,fc=PANEL,lw=1.2);T(fig,x+.01,.285,t,size=9.6,weight="bold",color=c,xmax=x+.295)
        _layout_text(fig,s,x+.01,x+.292,.115,.268,fs_max=10.2,fs_min=6.4)
    fig_footer(fig,k,f"Engine verdict: {ac.get('verdict','—')} · next stage: independent human scientific review (CSV exported) · cross-run / cross-GPU reproducibility · larger banks. Values: TEST815_results.json (summary, demo_acceptance).")
    return save_fig(fig,k,"ENGINE RECORD",["TEST815_results.json summary / demo_acceptance / source_removal_ablation","TEST815_manifest.json","POST_RUN_VERIFICATION.json"])

def fig2():
    k="F2";E=manifest().get("cartridges") or {};V=(LIVE.get("verification") or {}).get("cartridges") or {};A=LIVE.get("anatomy")
    if not E:return fig_missing(k,"The bank is drawn from the engine's cartridge manifest of this RUN.","No TEST815_manifest.json was written in this RUN.")
    fig=fig_base(k,"Two real articles and twenty synthetic decoys — each a sealed file of the frozen model's own layer-3 states · re-hashed and re-opened by this program after the run","SEALED MEMORY")
    ids=sorted(E,key=ckey);real=[c for c in ids if is_real(c)];syn=[c for c in ids if not is_real(c)]
    T(fig,.035,.862,"the bank — one tile = one .pt file on the SSD",size=9.4,weight="bold")
    for i,c in enumerate(real):
        e=E[c];v=V.get(c) or {};x=.035+i*.205;col=ccol(c);box(fig,x,.655,.197,.185,ec=col,lw=1.8);rect(fig,x,.808,.197,.032,col,z=2)
        Tc(fig,x+.004,x+.193,.824,f"{c} · {cshort(c)}",size=8.6,weight="bold",color="white")
        ls=[wrap(REAL[c]["title"],44,2),f"{e.get('body_tokens')} body tokens · n = {e.get('n')} · P = {e.get('p')}",f"file {fmt_b(v.get('bytes'))} · SHA {k_sha(e.get('sha256'),10)}",
            f"re-hash {okm(v.get('file_sha_ok'))} · reopen {okm(v.get('book_id_ok'))} · H3 {('×'.join(str(x_) for x_ in (v.get('h_shape') or [])) or '—')}"]
        T(fig,x+.008,.773,ls[0],size=7.2,color=INK,va="center",xmax=x+.19,linespacing=1.05)
        for j,l in enumerate(ls[1:]):T(fig,x+.008,.728-j*.026,l,size=7.0,color=INK2,mono=(j==1),xmax=x+.19)
    T(fig,.035,.625,f"{len(syn)} synthetic decoys (role {(E[syn[0]].get('role') if syn else '—')}) — same format, same SSD, same router",size=7.8,color=MUTED,xmax=.44)
    for i,c in enumerate(syn):
        e=E[c];v=V.get(c) or {};r_,q=divmod(i,5);x=.035+q*.0812;y=.515-r_*.098
        box(fig,x,y,.0772,.088,ec=COL["SYN"],lw=1.1);Tc(fig,x+.003,x+.074,y+.064,c,size=7.6,weight="bold",color=INK2)
        Tc(fig,x+.003,x+.074,y+.040,f"{e.get('body_tokens')} tokens",size=6.8,color=INK2);Tc(fig,x+.003,x+.074,y+.017,f"SHA {okm(v.get('file_sha_ok'))}  open {okm(v.get('book_id_ok'))}",size=6.6,color=OK_COL if v.get("file_sha_ok") else MUTED)
    if A:
        ids2=A["ids"];C=A["cos"];ax=fig.add_axes([.505,.355,.225,.47])
        im=ax.imshow(C,cmap="viridis",vmin=max(-1.0,float(np.nanmin(C))),vmax=1.0,interpolation="nearest")
        ax.set_xticks(range(len(ids2)));ax.set_yticks(range(len(ids2)));ax.set_xticklabels([L_(c) if is_real(c) else c.replace("_","") for c in ids2],rotation=90,fontsize=5.6)
        ax.set_yticklabels([L_(c) if is_real(c) else c.replace("_","") for c in ids2],fontsize=5.6)
        for tl in list(ax.get_xticklabels())+list(ax.get_yticklabels()):
            t=tl.get_text()
            if t in("A","B"):tl.set_color(COL["A"] if t=="A" else COL["B"]);tl.set_fontweight("bold")
        ax.set_title("H3 fingerprint similarity (centred cosine)",fontsize=8.4)
        cb=fig.add_axes([.735,.355,.007,.47]);fig.colorbar(im,cax=cb);cb.tick_params(labelsize=6.2)
        iR=[ids2.index(c) for c in real if c in ids2];iS=[ids2.index(c) for c in syn if c in ids2]
        rr=float(C[iR[0],iR[1]]) if len(iR)==2 else None;rs=float(np.mean([C[i,j] for i in iR for j in iS])) if iR and iS else None
        ss=float(np.mean([C[i,j] for i in iS for j in iS if i!=j])) if len(iS)>1 else None
        hs=(LIVE.get("verification") or {}).get("host_statistics") or {}
        box(fig,.775,.355,.19,.47,ec=NEU,fc=PANEL,lw=1.1);T(fig,.785,.80,"what the map shows",size=9.0,weight="bold",xmax=.96)
        for j,t in enumerate([f"article A ↔ article B   {rr:.3f}" if rr is not None else "A ↔ B —",f"article ↔ decoy (mean) {rs:.3f}" if rs is not None else "—",
                              f"decoy ↔ decoy (mean)   {ss:.3f}" if ss is not None else "—"]):T(fig,.785,.765-j*.03,t,size=7.6,mono=True,color=INK,xmax=.96)
        _layout_text(fig,"Each cartridge is reduced to one direction: the mean of its stored layer-3 states, centred on the bank average. Bright off-diagonal cells mark cartridges whose stored states point in a similar direction. This is a descriptive host statistic computed after the run — the engine's router scores every question token against 96 sampled states of each cartridge instead (Figure 3).",
                     .785,.958,.37,.665,fs_max=7.8,fs_min=6.0,color=INK2)
        for i,c in enumerate([c for c in real if c in A["strips"]]):
            S=A["strips"][c];ax2=fig.add_axes([.505+i*.235,.115,.215,.165])
            ax2.imshow(S,aspect="auto",origin="lower",cmap="magma",interpolation="nearest",vmin=float(np.percentile(S,2)),vmax=float(np.percentile(S,99.5)))
            ax2.set_title(f"{L_(c)} · {cshort(c)} — stored |H3|",fontsize=7.6,color=ccol(c));ax2.set_xticks([]);ax2.set_yticks([]);ax2.set_ylabel("64 channel bins",fontsize=6.6)
            ax2.set_xlabel(f"{E[c].get('body_tokens')} body tokens →",fontsize=6.8)
    else:
        box(fig,.505,.12,.46,.70,ec=AMBER,lw=1.4,ls="--");T(fig,.735,.47,wrap("Host statistics of the cartridge tensors are not available in this RUN (the files could not be re-opened by the host — see VERIFY).",60),size=10,color=AMBER,ha="center")
    fig_footer(fig,k,"Tiles: TEST815_manifest.json + host re-hash/re-open (POST_RUN_VERIFICATION.json). Map and strips: CARTRIDGE_ANATOMY.npz, computed read-only on the CPU from the sealed .pt files after the engine exited.")
    return save_fig(fig,k,"SEALED MEMORY",["TEST815_manifest.json","physical_cartridges/*.pt (read-only)","POST_RUN_VERIFICATION.json","CARTRIDGE_ANATOMY.npz"])

def fig3():
    k="F3";M,ids=score_matrix()
    if M is None or np.all(np.isnan(M)):return fig_missing(k,"The routing map is drawn from the engine's 22-cartridge H3 scores of this RUN.","No TEST815_ROUTE_PARAPHRASE record was written in this RUN.")
    sm=summary();fig=fig_base(k,"Each row: one question turned into its own layer-3 states and scored against all 22 cartridges by the engine — no titles, labels or text · row-normalised so the winner stands out","LIVE MEASUREMENT")
    mu=np.nanmean(M,1,keepdims=True);sd=np.nanstd(M,1,keepdims=True)+1e-12;Z=(M-mu)/sd
    ax=fig.add_axes([.105,.165,.49,.665]);im=ax.imshow(Z,aspect="auto",cmap="RdBu_r",vmin=-3.6,vmax=3.6,interpolation="nearest")
    ax.set_yticks(range(len(CASES)));ax.set_yticklabels([c.replace("_PARA"," para") for c in CASES],fontsize=7.2)
    ax.set_xticks(range(len(ids)));ax.set_xticklabels([f"{L_(c)} ·{c[-4:]}" if is_real(c) else c for c in ids],rotation=90,fontsize=6.0)
    for tl,c in zip(ax.get_xticklabels(),ids):
        if is_real(c):tl.set_color(ccol(c));tl.set_fontweight("bold")
    ax.axhline(7.5,color=INK,lw=1.2)
    for i,c in enumerate(CASES):
        row_=M[i];
        if np.all(np.isnan(row_)):continue
        r=row(c);order=(r.get("adaptive") or {}).get("ranked_22") if r else None
        order=order or [ids[j] for j in np.argsort(-np.nan_to_num(row_,nan=-9))]
        for rk,cid in enumerate(order[:2]):
            if cid in ids:ax.text(ids.index(cid),i,str(rk+1),ha="center",va="center",fontsize=7.4,weight="bold",color="white" if Z[i,ids.index(cid)]>1.8 else INK)
        for cid in relevant(c):
            if cid in ids:ax.add_patch(Rectangle((ids.index(cid)-.38,i-.38),.76,.76,fill=False,ec=INK,lw=1.6))
    ax.set_title("1 / 2 = engine's rank · black frame = article the offline key marks relevant (never shown to the model)",fontsize=8.0)
    cb=fig.add_axes([.60,.165,.007,.665]);fig.colorbar(im,cax=cb);cb.tick_params(labelsize=6.4);cb.set_ylabel("score − row mean (row SD)",fontsize=7.0)
    ax2=fig.add_axes([.70,.165,.17,.665]);mg=[];cl=[]
    for i,c in enumerate(CASES):
        rel=[ids.index(x) for x in relevant(c) if x in ids];dec=[j for j,x in enumerate(ids) if not is_real(x)]
        v=(np.nanmax(M[i,rel])-np.nanmax(M[i,dec])) if rel and dec and not np.all(np.isnan(M[i])) else np.nan;mg.append(v);cl.append(OK_COL if (v==v and v>0) else RED)
    y=np.arange(len(CASES));ax2.barh(y,[0 if v!=v else v for v in mg],color=cl,height=.62);ax2.set_ylim(len(CASES)-.5,-.5);ax2.set_yticks(y);ax2.set_yticklabels([])
    for yi,v in zip(y,mg):
        if v==v:ax2.text(v,yi,f" +{v:.3f}" if v>0 else f" {v:.3f}",va="center",fontsize=6.6)
    ax2.axvline(0,color=NEU,lw=.8);ax2.set_xlim(min(0,np.nanmin(mg) if np.any(np.isfinite(mg)) else 0)*1.3,(np.nanmax(mg) if np.any(np.isfinite(mg)) else .05)*1.45)
    ax2.set_title("relevant article − best decoy",fontsize=8.2);ax2.tick_params(labelsize=6.4);_axstyle(ax2,6.4)
    box(fig,.885,.165,.08,.665,ec=NEU,fc=PANEL,lw=1.0)
    for j,(v,l) in enumerate([(f"{sm.get('routing_top1_relevant','—')}/{sm.get('cases','—')}","top-1\nrelevant"),(f"{sm.get('routing_top2_relevant','—')}/{sm.get('cases','—')}","top-2\nrelevant"),
                              (f"{sm.get('decoy_selected_cases','—')}/{sm.get('cases','—')}","decoy in\ntop-2"),(f"{sum(1 for v in mg if v==v and v>0)}/{len(CASES)}","margin\n> 0")]):
        Tc(fig,.887,.963,.78-j*.16,v,size=13,weight="bold",color=OK_COL);Tc(fig,.887,.963,.725-j*.16,l,size=7.0,color=INK2,linespacing=1.1)
    fig_footer(fig,k,"Scores: TEST815_results.json routing_robustness (original_scores / paraphrase_scores) = the engine's locked TEST757 numeric_rank over all 22 cartridges; ranks: rows[*].adaptive.ranked_22; relevance key: offline_routing_eval (used only for evaluation).")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST815_results.json routing_robustness / rows","TEST815_ROUTE_PARAPHRASE lines"])

def fig4():
    k="F4";R=[r for r in routes() if r.get("original_scores")]
    if not R:return fig_missing(k,"The paraphrase control is drawn from the engine's routing records of this RUN.","No TEST815_ROUTE_PARAPHRASE record was written in this RUN.")
    fig=fig_base(k,"Each question was asked a second time in different words — the router saw only the model's own states of the new wording · margin = relevant article over the best decoy","LIVE MEASUREMENT")
    def marg(sc,case):
        rel=[sc[x] for x in relevant(case) if x in sc];dec=[v for c,v in sc.items() if not is_real(c)]
        return (max(rel)-max(dec)) if rel and dec else np.nan
    R=sorted(R,key=lambda r:BASE_Q.index(r["case_id"]) if r["case_id"] in BASE_Q else 99);Q=questions()
    ax=fig.add_axes([.075,.17,.30,.66]);y=np.arange(len(R))
    for i,r in enumerate(R):
        a=marg(r["original_scores"],r["case_id"]);b=marg(r.get("paraphrase_scores") or {},r["case_id"]+"_PARA")
        ax.plot([a,b],[i,i],color=RULE,lw=2.4,zorder=1);ax.scatter([a],[i],s=46,color=COL["A"],zorder=2);ax.scatter([b],[i],s=46,marker="D",color=COL["LOOP"],zorder=2)
    ax.axvline(0,color=RED,lw=1.0,ls="--");ax.set_yticks(y);ax.set_yticklabels([r["case_id"] for r in R],fontsize=8);ax.set_ylim(len(R)-.5,-.5)
    ax.set_xlabel("H3 score margin over the best decoy",fontsize=8);ax.set_title("● original   ◆ paraphrase   (right of the red line = article beats every decoy)",fontsize=7.8);_axstyle(ax,7.2)
    xs=[.40,.445,.765,.865,.925];hd=["","question (top) · paraphrase (bottom)","top-1: orig → para","top-2 relevant","same top-1"]
    for x,h,nx in zip(xs,hd,xs[1:]+[.965]):T(fig,x,.855,h,size=7.6,weight="bold",color=MUTED,xmax=nx-.006)
    hline(fig,.40,.965,.838,RULE)
    y0=.83;dy=.66/len(R);rl={r["case_id"]:r for r in rows()};rlog=row_logs()
    for i,r in enumerate(R):
        yc=y0-(i+.5)*dy;c=r["case_id"];T(fig,.40,yc,c,size=8.4,weight="bold")
        T(fig,.445,yc+dy*.2,short(Q.get(c) or "",80),size=6.9,color=INK,xmax=.755,minsize=6.4);T(fig,.445,yc-dy*.2,short(Q.get(c+"_PARA") or "",80),size=6.9,color=COL["LOOP"],xmax=.755,minsize=6.4)
        o,p=r.get("original_top1"),r.get("paraphrase_top1");T(fig,.765,yc,f"{L_(o) if is_real(o) else o} → {L_(p) if is_real(p) else p}",size=8.4,weight="bold",color=INK)
        t2=[((rl.get(x) or rlog.get(x) or {}).get("offline_routing_eval") or {}).get("top2_relevant") for x in (c,c+"_PARA")]
        T(fig,.87,yc,f"{okm(t2[0])} / {okm(t2[1])}",size=9,weight="bold",color=OK_COL if all(t2) else AMBER)
        T(fig,.94,yc,okm(r.get("same_top1")),size=10,weight="bold",color=OK_COL if r.get("same_top1") else AMBER)
        if i<len(R)-1:hline(fig,.40,.965,yc-dy/2,"#EEF0F3",.6)
    same=sum(1 for r in R if r.get("same_top1"));t2a=sum(1 for c in CASES if ((rl.get(c) or rlog.get(c) or {}).get("offline_routing_eval") or {}).get("top2_relevant"))
    pos=sum(1 for r in R for x,c in ((r["original_scores"],r["case_id"]),(r.get("paraphrase_scores") or {},r["case_id"]+"_PARA")) if marg(x,c)>0)
    box(fig,.40,.095,.565,.05,ec=OK_COL,fc=PANEL,lw=1.1)
    Tc(fig,.405,.96,.12,f"relevant article in top-2: {t2a}/16 wordings · beats every decoy: {pos}/16 · same top-1 article: {same}/8 — A and B score close, so the loop reads both (Figure 5)",size=8.2,weight="bold",color=INK)
    fig_footer(fig,k,"A = PMC9521804 (credit for data) · B = PMC9401135 (data availability). Records: routing_robustness (scores, top-1, same_top1) and rows[*].offline_routing_eval (top-2 relevance, offline key).")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST815_results.json routing_robustness","rows[*].offline_routing_eval"])

def fig5():
    k="F5";TA=tracks("ADAPTIVE");TF=tracks("FIXED")
    if not TA:return fig_missing(k,"The decision map is drawn from the native reads of this RUN (results steps or NATIVE_FUSION_STEP lines).","No closed-loop case was run in this RUN.")
    fig=fig_base(k,"16 questions · each cell = one native read of physical memory (A, B = the two articles; A+B = fused, first one first) · the adaptive loop stops as soon as the evidence agrees","ENGINE RECORD")
    cx=[.035,.10,.355,.45,.635];T(fig,.10,.858,"ADAPTIVE closed loop — reads in order",size=8.6,weight="bold",color=COL["LOOP"]);T(fig,.355,.858,"outcome",size=8.2,weight="bold",color=MUTED)
    T(fig,.45,.858,"FIXED policy — always 4 reads",size=8.6,weight="bold",color=COL["FIX"]);T(fig,.635,.858,"outcome",size=8.2,weight="bold",color=MUTED)
    dy=.0405;y0=.815;sw=.0615;fw=.0425
    for i,c in enumerate(CASES):
        y=y0-i*dy;r=row(c) or {};ad=r.get("adaptive") or {};fx=r.get("fixed") or {};lg=row_logs().get(c) or {}
        if i==8:hline(fig,.035,.69,y+dy*.5+.001,INK2,.9)
        T(fig,.035,y,c.replace("_PARA"," para"),size=8.0,weight="bold",color=INK)
        for j,s in enumerate(TA.get(c,[])[:4]):
            x=.10+j*(sw+.003);rect(fig,x,y-.016,sw,.032,opcol(s["op"]),z=2);Tc(fig,x+.002,x+sw-.002,y,ids_lab(s["ids"]),size=7.4,weight="bold",color="white")
        act=ad.get("action") or lg.get("adaptive_action");flag="recovered" if ad.get("recovered_from_unknown") else ("revised" if (ad.get("revision") if ad else lg.get("adaptive_revision")) else "")
        pill(fig,.355,y-.014,.042,.028,act or "—",OK_COL if act=="ANSWER" else (RED if act else MUTED),size=6.6);T(fig,.401,y,flag,size=6.8,color=COL["GOLD"] if flag=="recovered" else MUTED)
        for j,s in enumerate(TF.get(c,[])[:4]):
            x=.45+j*(fw+.0025);rect(fig,x,y-.016,fw,.032,opcol(s["op"]),z=2);Tc(fig,x+.002,x+fw-.002,y,ids_lab(s["ids"]),size=6.8,weight="bold",color="white")
        fa=fx.get("action") or lg.get("fixed_action");pill(fig,.635,y-.014,.042,.028,fa or "—",OK_COL if fa=="ANSWER" else (RED if fa else MUTED),size=6.6)
    fx0=.715;fw_=.232;bw=[("① read the top-1 cartridge",.80,COL["A"]),("usable? — a complete sentence, not UNKNOWN",.715,NEU)]
    for t,y,c in bw:box(fig,fx0,y-.026,fw_,.052,ec=c,lw=1.3);Tc(fig,fx0+.005,fx0+fw_-.005,y,t,size=7.8,color=INK)
    arrow(fig,fx0+fw_/2,.774,fx0+fw_/2,.741,ms=9)
    box(fig,fx0,.575,.11,.085,ec=opcol("FUSE_TO_CHALLENGE_INITIAL"),lw=1.4);Tc(fig,fx0+.004,fx0+.106,.632,"yes → ② CHALLENGE",size=7.6,weight="bold",color=opcol("FUSE_TO_CHALLENGE_INITIAL"));Tc(fig,fx0+.004,fx0+.106,.598,"fuse top-1 + top-2",size=7.2)
    box(fig,fx0+.122,.575,.11,.085,ec=opcol("ALTERNATE_AFTER_UNKNOWN"),lw=1.4);Tc(fig,fx0+.126,fx0+.228,.632,"no → ② ALTERNATE",size=7.6,weight="bold",color=opcol("ALTERNATE_AFTER_UNKNOWN"));Tc(fig,fx0+.126,fx0+.228,.598,"then ③ fuse it first",size=7.2)
    arrow(fig,fx0+.07,.689,fx0+.055,.662,ms=9);arrow(fig,fx0+.165,.689,fx0+.177,.662,ms=9)
    box(fig,fx0,.465,fw_,.06,ec=NEU,lw=1.3);Tc(fig,fx0+.005,fx0+fw_-.005,.505,"evidence agrees? (overlap ≥ 0.25,",size=7.6);Tc(fig,fx0+.005,fx0+fw_-.005,.481,"no conflicting % values)",size=7.6)
    arrow(fig,fx0+.055,.575,fx0+.085,.527,ms=9);arrow(fig,fx0+.177,.575,fx0+.147,.527,ms=9)
    box(fig,fx0,.36,fw_,.06,ec=opcol("REVERSE_EVIDENCE_CHECK"),lw=1.4);Tc(fig,fx0+.005,fx0+fw_-.005,.40,"no → ④ REVERSE-order check",size=7.6,weight="bold",color=opcol("REVERSE_EVIDENCE_CHECK"));Tc(fig,fx0+.005,fx0+fw_-.005,.376,"(or alternate check)",size=7.2)
    arrow(fig,fx0+fw_/2,.465,fx0+fw_/2,.422,ms=9)
    box(fig,fx0,.255,fw_,.06,ec=COL["B"],lw=1.4);Tc(fig,fx0+.005,fx0+fw_-.005,.295,"DECIDE: ANSWER — or ABSTAIN",size=7.8,weight="bold",color=COL["B"]);Tc(fig,fx0+.005,fx0+fw_-.005,.271,"at most 4 reads · no gold, no oracle",size=7.2)
    arrow(fig,fx0+fw_/2,.36,fx0+fw_/2,.317,ms=9)
    fig.add_artist(Line2D([fx0+fw_,.958,.958],[.495,.495,.285],transform=fig.transFigure,color=OK_COL,lw=1.3));arrow(fig,.958,.285,fx0+fw_+.001,.285,col=OK_COL,ms=9);T(fig,.952,.44,"yes",size=7.0,color=OK_COL,ha="right")
    pc=policy();sm=summary()
    lines=[f"adaptive reads {pc.get('adaptive_reads','—')} · fixed {pc.get('fixed_reads','—')} · decisions changed {pc.get('changed_decisions','—')}/16",
           f"recoveries from UNKNOWN {pc.get('adaptive_recoveries','—')} · revisions {pc.get('adaptive_revisions','—')}",f"read counts differ in {pc.get('different_read_counts','—')}/16 cases"]
    for j,t in enumerate(lines):T(fig,fx0,.215-j*.026,t,size=7.4,color=INK2,xmax=.965)
    used=[o for o in OPS if any(s["op"]==o for T_ in (TA,TF) for v in T_.values() for s in v)]
    xx=.035
    for o in used:
        rect(fig,xx,.112,.012,.016,opcol(o),z=2);t=T(fig,xx+.016,.12,oplab(o),size=7.0,color=INK2);xx=_bb(fig,t).x1+.014
    fig_footer(fig,k,"Order and sources of every read: rows[*].adaptive/fixed.steps (operation, ids) of TEST815_results.json — the same sequence appears live as NATIVE_FUSION_STEP lines. Rules: decide815 in 815.py (unchanged).")
    return save_fig(fig,k,"ENGINE RECORD",["TEST815_results.json rows[*].steps / trace","NATIVE_FUSION_STEP lines","815.py decide815 (rules)"])

def fig6():
    k="F6";TA=tracks("ADAPTIVE");TF=tracks("FIXED");cm=cost()
    if not TA or not TF:return fig_missing(k,"The cost comparison is drawn from the native reads of both policies in this RUN.","The closed-loop cases did not run in this RUN.")
    fig=fig_base(k,"Both policies answer the same 16 questions from the same physical memory — the adaptive controller reads only what it needs · wall time of every native read measured by the engine","LIVE MEASUREMENT")
    ax=fig.add_axes([.06,.20,.49,.62]);x=np.arange(len(CASES));a=[len(TA.get(c,[])) for c in CASES];f=[len(TF.get(c,[])) for c in CASES]
    ax.bar(x-.2,a,.38,color=COL["LOOP"],label="adaptive");ax.bar(x+.2,f,.38,color=COL["FIX"],alpha=.75,label="fixed")
    ax.set_xticks(x);ax.set_xticklabels([c.replace("_PARA","p") for c in CASES],fontsize=7,rotation=0);ax.set_ylim(0,4.9);ax.set_yticks([0,1,2,3,4]);ax.set_ylabel("native reads",fontsize=8)
    ax.legend(loc="upper left",ncol=2,fontsize=7.6);ax.set_title("reads per question (p = paraphrase)",fontsize=8.8);_axstyle(ax,7.2)
    for xi,v in zip(x,a):ax.text(xi-.2,v+.06,str(v),ha="center",fontsize=6.6,color=COL["LOOP"])
    ax2=fig.add_axes([.63,.55,.33,.27])
    for T_,c,lab in ((TA,COL["LOOP"],"adaptive"),(TF,COL["FIX"],"fixed")):
        s=[float(v["sec"] or 0) for cc in CASES for v in T_.get(cc,[])]
        if any(s):ax2.plot(np.arange(1,len(s)+1),np.cumsum(s)/60,color=c,lw=1.8,label=lab);ax2.text(len(s),np.sum(s)/60,f" {np.sum(s)/60:.1f} min",fontsize=7,va="center",color=c)
    ax2.set_xlabel("native reads in execution order",fontsize=7.6);ax2.set_ylabel("cumulative minutes",fontsize=7.6);ax2.set_title("cumulative read time",fontsize=8.6);_axstyle(ax2,6.8);ax2.legend(fontsize=7)
    A_=cm.get("adaptive") or {};F_=cm.get("fixed") or {}
    box(fig,.60,.10,.365,.37,ec=NEU,fc=PANEL,lw=1.1)
    hd=["","adaptive","fixed"];xs=[.61,.80,.885]
    for xx,h in zip(xs,hd):T(fig,xx,.445,h,size=8.0,weight="bold",color=MUTED)
    def pct(a_,b_):
        try:return f"  (−{100*(1-float(a_)/float(b_)):.0f} %)"
        except Exception:return ""
    rws=[("native reads",A_.get("native_reads"),F_.get("native_reads")),("read wall time (s)",A_.get("read_wall_seconds_sum"),F_.get("read_wall_seconds_sum")),
         ("mean s per read",A_.get("mean_read_seconds"),F_.get("mean_read_seconds")),("answers",A_.get("answers"),F_.get("answers")),("abstentions",A_.get("abstentions"),F_.get("abstentions")),
         ("hypothesis revisions",A_.get("revisions"),F_.get("revisions")),("relation audit pass",f"{A_.get('relation_audit_pass','—')}/{A_.get('relation_audit_total','—')}",f"{F_.get('relation_audit_pass','—')}/{F_.get('relation_audit_total','—')}")]
    for j,(l,u,v) in enumerate(rws):
        yy=.41-j*.037;T(fig,xs[0],yy,l,size=7.8,color=INK);T(fig,xs[1],yy,str(u if u is not None else "—"),size=7.8,mono=True,weight="bold",color=COL["LOOP"]);T(fig,xs[2],yy,str(v if v is not None else "—"),size=7.8,mono=True,color=COL["FIX"])
    T(fig,.61,.135,f"reads {pct(A_.get('native_reads'),F_.get('native_reads')).strip(' ()') or '—'} · read time {pct(A_.get('read_wall_seconds_sum'),F_.get('read_wall_seconds_sum')).strip(' ()') or '—'} · same decisions {16-int(policy().get('changed_decisions') or 0)}/16",size=7.8,weight="bold",color=OK_COL,xmax=.96)
    T(fig,.06,.115,"Pair reads fuse two cartridges (≈1,960 memory tokens) and take longer than single reads, so time falls a little less than the read count.",size=7.6,color=INK2,xmax=.58)
    fig_footer(fig,k,"Reads and seconds: rows[*].<policy>.steps[*].elapsed_seconds (per native read, model loading excluded) and cost_matrix of TEST815_results.json; the host re-adds them in POST_RUN_VERIFICATION.json.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST815_results.json rows[*].steps / cost_matrix / policy_comparison","POST_RUN_VERIFICATION.json consistency"])

def fig7():
    k="F7";rw=rows()
    if not rw:return fig_missing(k,"The verbatim hypotheses are taken from the engine's results file of this RUN.","No closed-loop result was written in this RUN.")
    fig=fig_base(k,"What the frozen model said after its first read of physical memory, and what the closed loop finally answered — printed verbatim, unedited","ENGINE RECORD")
    def ops(r):return [s.get("operation") for s in (r.get("adaptive") or {}).get("steps") or []]
    pick=[r for r in rw if (r.get("adaptive") or {}).get("recovered_from_unknown")]
    pick+=[r for r in rw if r not in pick and any(o in ("REVERSE_EVIDENCE_CHECK","ALTERNATE_EVIDENCE_CHECK") for o in ops(r))]
    pick+=[r for r in rw if r not in pick and r["case_id"] in ("Q2","Q3","Q7","Q4")]
    pick=pick[:4];hh=.79/max(1,len(pick))-.012
    for i,r in enumerate(pick):
        ad=r.get("adaptive") or {};st=ad.get("steps") or [];y1=.865-i*(hh+.012);y0=y1-hh
        fl="RECOVERED FROM UNKNOWN" if ad.get("recovered_from_unknown") else ("REVERSE CHECK" if "REVERSE_EVIDENCE_CHECK" in ops(r) else ("REVISED" if ad.get("revision") else "CONFIRMED"))
        fc={"RECOVERED FROM UNKNOWN":COL["GOLD"],"REVERSE CHECK":opcol("REVERSE_EVIDENCE_CHECK")}.get(fl,COL["LOOP"])
        box(fig,.035,y0,.93,hh,ec=fc,lw=1.3);T(fig,.045,y1-.022,f"{r['case_id']}",size=10,weight="bold",color=fc)
        T(fig,.105,y1-.022,short(r.get("question"),150),size=8.2,weight="bold",xmax=.955)
        pill(fig,.045,y1-.07,.11,.026,fl,fc,size=6.4)
        T(fig,.045,y1-.098,"path: "+" → ".join(ids_lab(s.get("ids") or []) for s in st),size=7.0,color=INK2,xmax=.16)
        T(fig,.045,y1-.12,f"{ad.get('read_count','—')} reads · {ad.get('action','—')}",size=7.0,color=INK2,xmax=.16)
        first=st[0] if st else {};last=st[-1] if st else {}
        T(fig,.17,y1-.05,f"first reading · {ids_lab(first.get('ids') or [])} · {first.get('tokens','—')} token(s)",size=7.4,weight="bold",color=COL["A"],xmax=.55)
        _layout_text(fig,first.get("raw") or "—",.17,.555,y0+.008,y1-.064,fs_max=10.6,fs_min=5.8,color=INK)
        arrow(fig,.562,y0+hh*.42,.588,y0+hh*.42,col=fc,lw=1.6,ms=11)
        T(fig,.595,y1-.05,f"final answer · {ad.get('action','—')} · {ids_lab(last.get('ids') or [])} · {last.get('tokens','—')} token(s)",size=7.4,weight="bold",color=OK_COL if ad.get("action")=="ANSWER" else RED,xmax=.955)
        _layout_text(fig,ad.get("answer") or "—",.595,.957,y0+.008,y1-.064,fs_max=10.6,fs_min=5.8,color=INK)
    fig_footer(fig,k,"Verbatim: rows[*].adaptive.steps[0].raw and rows[*].adaptive.answer (TEST815_results.json). Every answer of all 16 questions, both policies, is in the ANSWERS tab and in TEST815_independent_review.csv for human review.")
    return save_fig(fig,k,"ENGINE RECORD",["TEST815_results.json rows[*].adaptive (steps, answer, revision, recovered_from_unknown)"])
def fig8():
    k="F8";AB=ablation()
    if not AB:return fig_missing(k,"The evidence-removal matrix is drawn from the engine's source-removal trials of this RUN.","No TEST815_ABLATION record was written in this RUN.")
    fig=fig_base(k,"Each real article is removed from the bank in turn · the router must pick the best SURVIVING cartridge among 21 · the frozen model reads it natively — does it invent, or abstain?","LIVE MEASUREMENT")
    ev=evidence_classes();Q=questions();by={(a["case_id"],a["removed"]):a for a in AB}
    xs=[.035,.075,.395,.52,.645];T(fig,.075,.858,"question",size=8,weight="bold",color=MUTED)
    for x,h in zip(xs[2:],["both articles present","A removed (credit for data)","B removed (data availability)"]):Tc(fig,x,x+.118,.858,h,size=7.8,weight="bold",color=MUTED)
    dy=.073;y0=.81
    for i,q in enumerate(BASE_Q):
        y=y0-i*dy;rel=set(relevant(q));T(fig,.035,y,q,size=9,weight="bold");T(fig,.075,y+.008,wrap(Q.get(q),64,2),size=7.0,color=INK,xmax=.385,linespacing=1.15)
        T(fig,.075,y-.025,"relevant (offline key): "+", ".join(L_(c) for c in sorted(rel)),size=6.6,color=MUTED,xmax=.385)
        a0=next((a for a in AB if a["case_id"]==q),None);ba=(a0 or {}).get("baseline_action")
        rect(fig,.395,y-.026,.118,.052,"#DCFCE7" if ba=="ANSWER" else "#FEE2E2",z=1);Tc(fig,.397,.511,y+.008,ba or "—",size=8.4,weight="bold",color=OK_COL if ba=="ANSWER" else RED)
        Tc(fig,.397,.511,y-.014,f"reads {L_((a0 or {}).get('baseline_top1'))} first",size=6.6,color=INK2)
        for j,rem in enumerate(REAL_IDS):
            a=by.get((q,rem));x=xs[3+j]
            if not a:Tc(fig,x,x+.118,y,"—",size=8);continue
            act=a.get("native_action");rr=rem in rel;left=bool(rel-{rem})
            rect(fig,x,y-.026,.118,.052,"#DCFCE7" if act=="ANSWER" else "#FEE2E2",ec=(INK if rr and not left else ("#9CA3AF" if rr else "none")),lw=(1.8 if rr and not left else (1.0 if rr else 0)),z=1)
            Tc(fig,x+.002,x+.116,y+.008,act,size=8.4,weight="bold",color=OK_COL if act=="ANSWER" else RED)
            Tc(fig,x+.002,x+.116,y-.014,f"reads {L_(a.get('top1')) if is_real(a.get('top1')) else a.get('top1')} · "+("no relevant left" if rr and not left else ("other relevant left" if rr else "irrelevant removed")),size=6.2,color=INK2)
    nl,ol,ir=ev["none_left"],ev["other_left"],ev["irrelevant"];syn=sum(1 for a in AB if a.get("selected_synthetic"))
    box(fig,.78,.235,.185,.625,ec=NEU,fc=PANEL,lw=1.1)
    for j,(v,l,c) in enumerate([(f"{_n_ab(nl)}/{len(nl)}","abstained — no relevant\narticle left (black frame)",COL["B"]),(f"{len(ir)-_n_ab(ir)}/{len(ir)}","answered — the removed\narticle was irrelevant",OK_COL),
                                (f"{len(ol)-_n_ab(ol)}/{len(ol)}","answered — another relevant\narticle was still there",COL["LOOP"]),(f"{syn}/{len(AB)}","trials where a decoy was\nread instead",OK_COL)]):
        Tc(fig,.782,.963,.81-j*.15,v,size=17,weight="bold",color=c);Tc(fig,.782,.963,.755-j*.15,l,size=7.0,color=INK2,linespacing=1.1)
    q1=next((a for a in nl if a.get("native_action")=="ABSTAIN" and len(str(a.get("native_answer") or ""))>12),None) or next((a for a in nl if a.get("native_action")=="ABSTAIN"),None)
    q2=next((a for a in ir if a.get("native_action")=="ANSWER"),None)
    for j,(a,lab,c) in enumerate(((q1,"abstention, verbatim",COL["B"]),(q2,"answer from the surviving relevant article, verbatim",OK_COL))):
        x=.035+j*.375;box(fig,x,.095,.365,.125,ec=c,lw=1.2)
        if a:
            T(fig,x+.008,.205,f"{a['case_id']} · {L_(a['removed'])} removed · {lab}",size=7.6,weight="bold",color=c,xmax=x+.358)
            _layout_text(fig,a.get("native_answer"),x+.008,x+.357,.102,.19,fs_max=9.8,fs_min=5.8)
    fig_footer(fig,k,"Records: source_removal_ablation (top1 among 21, native_action, native_answer, removed_relevant_offline, selected_synthetic). The offline relevance key is used only to classify the trials — never by the model or the router.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST815_results.json source_removal_ablation","TEST815_ABLATION lines","rows[*].offline_routing_eval"])

def fig9():
    k="F9";rw=[r for r in rows() if ((r.get("offline_fact_audit") or {}).get("adaptive") or {}).get("status")=="NARROW_NUMERIC_FACT_CHECK"]
    if not rw:return fig_missing(k,"The numeric audit is drawn from the engine's offline fact audit of this RUN.","No audited case (Q2, Q8 and their paraphrases) was answered in this RUN.")
    fig=fig_base(k,"The empirical article reports 98 % (DOI links), 78 % (URL links) and 80 % (automatic retrieval) · after the run each final answer is checked for the numbers AND for the right number–term relation","ENGINE RECORD")
    RA=relation();rw=rw[:4]
    for i,r in enumerate(rw):
        cid=r["case_id"];ad=r.get("adaptive") or {};fa=(r.get("offline_fact_audit") or {}).get("adaptive") or {};ff=(r.get("offline_fact_audit") or {}).get("fixed") or {}
        ra=(RA.get(cid) or {}).get("adaptive") or {};rf=(RA.get(cid) or {}).get("fixed") or {}
        q,c_=divmod(i,2);x=.035+c_*.47;y1=.865-q*.385;y0=y1-.365;ok=bool(fa.get("passed")) and bool(ra.get("passed",True))
        box(fig,x,y0,.46,.365,ec=OK_COL if ok else RED,lw=1.5);T(fig,x+.01,y1-.022,cid,size=10.5,weight="bold",color=OK_COL if ok else RED)
        T(fig,x+.075,y1-.022,short(r.get("question"),95),size=7.8,weight="bold",xmax=x+.452)
        T(fig,x+.01,y1-.05,f"adaptive final answer · {ad.get('action','—')} · sources {ids_lab(ad.get('selected') or [])} — verbatim",size=7.2,color=INK2,xmax=x+.452)
        _layout_text(fig,ad.get("answer"),x+.01,x+.452,y0+.105,y1-.064,fs_max=12.0,fs_min=5.8)
        req=fa.get("required") or [];obs=set(fa.get("observed") or []);xx=x+.01
        T(fig,xx,y0+.082,"numbers:",size=7.4,weight="bold",color=INK2)
        xx=x+.075
        for p_ in req:pill(fig,xx,y0+.07,.05,.024,f"{p_} {okm(p_ in obs)}",OK_COL if p_ in obs else RED,size=7.0);xx+=.055
        rel=[(kk,v) for kk,v in ra.items() if kk not in ("status","passed")]
        T(fig,x+.01,y0+.045,"relations:",size=7.4,weight="bold",color=INK2);xx=x+.075
        lab={"doi_98":"98 % ↔ DOI","url_78":"78 % ↔ URL","automatic_80":"80 % ↔ automatic"}
        for kk,v in rel:pill(fig,xx,y0+.033,.085,.024,f"{lab.get(kk,kk)} {okm(v)}",OK_COL if v else RED,size=6.8);xx+=.09
        if not rel:T(fig,xx,y0+.045,f"relation audit: {ra.get('status','—')} · passed {okm(ra.get('passed'))}",size=7.2,color=INK2,xmax=x+.452)
        T(fig,x+.01,y0+.013,f"fixed policy: numbers {okm(ff.get('passed'))} · relations {okm(rf.get('passed'))} · first reading already had the numbers: {okm(fa.get('initial_passed'))}",size=7.0,color=MUTED,xmax=x+.452)
    fig_footer(fig,k,"offline_fact_audit and relation_audit of TEST815_results.json — computed after inference from a key the model never saw. Correct numbers without their DOI / URL / automatic relation do not pass. A narrow check, not a semantic grade.")
    return save_fig(fig,k,"ENGINE RECORD",["TEST815_results.json rows[*].offline_fact_audit / relation_audit"])

_AKB815_PARTS.add(3)
# ===== END OF PART 3/4 =====
# ===== PART 4/4 — paste directly after PART 3 in the same cell =====
# =====================================================================================================================
# PART 4 / 4 — figures 8–12, records (direct downloads, no ZIP), the single RUN pipeline and the Gradio interface
#              (SH782 design: one button, live stages, live engine output, tabs, figures shown and downloadable).
# THIS PART  65,184 characters · its last line is  # ===== END OF PART 4/4 =====
# =====================================================================================================================
if not {1,2,3}<=globals().get("_AKB815_PARTS",set()):raise RuntimeError("PART "+str(sorted({1,2,3}-globals().get("_AKB815_PARTS",set())))+" of the program is missing above this part in the cell — paste PART 1, 2, 3 and 4 one below the other, each completely (every part ends with an END OF PART line)")
def fig10():
    k="F10";RP=replay()
    if not RP:return fig_missing(k,"The replay table is drawn from the engine's same-run replay records of this RUN.","No TEST815_REPLAY record was written in this RUN.")
    fig=fig_base(k,"After everything else, the engine re-ranked 8 questions and re-read their first cartridge from the same SSD files — a second, independent native pass inside the same run","LIVE MEASUREMENT")
    hd=["case","first read","rank top-1","rank top-2","first answer SHA-256 · original","replay","identical","tokens","seconds  orig → replay"];xs=[.035,.10,.17,.235,.30,.52,.735,.80,.86]
    for x,h in zip(xs,hd):T(fig,x,.858,h,size=7.6,weight="bold",color=MUTED)
    hline(fig,.035,.965,.84,RULE);tr={c:tracks("ADAPTIVE").get(c) or [] for c in CASES}
    for i,r in enumerate(RP[:8]):
        y=.81-i*.052;c=r["case_id"];fi=(tr.get(c) or [{}])[0].get("ids") or [];same=r.get("initial_original_sha256")==r.get("initial_replay_sha256") and bool(r.get("initial_original_sha256"))
        vals=[(c,INK,True),(ids_lab(fi) or "—",INK2,False),(okm(r.get("rank_top1_identical")),OK_COL if r.get("rank_top1_identical") else RED,False),(okm(r.get("rank_top2_identical")),OK_COL if r.get("rank_top2_identical") else RED,False),
              (k_sha(r.get("initial_original_sha256"),24),INK2,False),(k_sha(r.get("initial_replay_sha256"),24),INK2,False),("IDENTICAL" if r.get("exact_initial_answer_identical") else "DIFFERENT",OK_COL if r.get("exact_initial_answer_identical") else AMBER,False),
              (f"{r.get('original_tokens')} / {r.get('replay_tokens')}",INK2,False),(f"{r.get('original_seconds')} → {r.get('replay_seconds')}",INK2,False)]
        for (v,col,b),x,nx in zip(vals,xs,xs[1:]+[.965]):T(fig,x,y,v,size=7.8,color=col,weight="bold" if b or v in("IDENTICAL","DIFFERENT") else "normal",mono=x in(.30,.52),xmax=nx-.006)
        if same:rect(fig,.30-.004,y-.017,.43,.034,"#ECFDF5",z=0)
    ax=fig.add_axes([.065,.12,.22,.25]);o=[float(r.get("original_seconds") or 0) for r in RP];p=[float(r.get("replay_seconds") or 0) for r in RP]
    ax.scatter(o,p,color=OK_COL,s=26,zorder=3);lo,hi=min(o+p)*.97,max(o+p)*1.03;ax.plot([lo,hi],[lo,hi],color=MUTED,lw=.9,ls="--");ax.set_xlim(lo,hi);ax.set_ylim(lo,hi)
    ax.set_xlabel("original read (s)",fontsize=7.4);ax.set_ylabel("replay read (s)",fontsize=7.4);ax.set_title("read time: original vs replay",fontsize=8);_axstyle(ax,6.6)
    s=rp_summary();box(fig,.33,.10,.255,.29,ec=OK_COL,fc=PANEL,lw=1.2)
    for j,(v,l) in enumerate([(f"{s.get('rank_top1_exact','—')}/{s.get('cases','—')}","top-1 rank identical"),(f"{s.get('rank_top2_exact','—')}/{s.get('cases','—')}","top-2 ranks identical"),
                              (f"{s.get('initial_answer_exact','—')}/{s.get('cases','—')}","first answers byte-identical"),(f"{s.get('initial_action_exact','—')}/{s.get('cases','—')}","same usable / UNKNOWN decision")]):
        T(fig,.345,.355-j*.066,v,size=15,weight="bold",color=OK_COL);T(fig,.43,.355-j*.066,l,size=8.0,color=INK)
    ex=next((r for r in results().get("replay_audit") or [] if r.get("replay_answer")),None);box(fig,.605,.10,.36,.29,ec=NEU,lw=1.1)
    if ex:
        T(fig,.615,.37,f"{ex['case_id']} · first answer as re-generated in the replay (verbatim)",size=7.8,weight="bold",color=OK_COL,xmax=.958)
        _layout_text(fig,ex["replay_answer"],.615,.958,.16,.35,fs_max=10.6,fs_min=5.8)
    T(fig,.615,.125,wrap("Scope: same run, same GPU, same files. Cross-run, cross-seed and cross-GPU reproducibility are the next stage.",80),size=7.2,color=AMBER,xmax=.958,linespacing=1.1)
    fig_footer(fig,k,"replay_audit and replay_summary of TEST815_results.json (SHA-256 of the cleaned first answer, original vs replay) · TEST815_REPLAY lines in the live engine output.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST815_results.json replay_audit / replay_summary","TEST815_REPLAY lines"])

def _gate_cat(n):
    m=re.match(r"^(.*?)(?:_(?:Q\d+|C\d\d_|PMC\d+|\d{3}\.py|TEST815_|REPLAY_|DROP_)).*$",n)
    return m.group(1) if m and m.group(1) else re.sub(r"_\d+$","",n)
def fig11():
    k="F11";FR=fusion_records()
    if not FR and not CHECKS:return fig_missing(k,"Timing, GPU and gates are measured from the engine output of this RUN.","The engine produced no output in this RUN.")
    fig=fig_base(k,"Measured while the engine ran: nvidia-smi every 10 s, every native fusion step the engine instruments (SSD verify · CPU→GPU · fusion), every PASS / FAIL gate it printed","LIVE MEASUREMENT")
    ax=fig.add_axes([.06,.625,.43,.20]);S=[s for s in GPU_SAMPLES if s.get("used_mib") is not None];E_=LIVE.get("engine") or {};t0=E_.get("start_t") or (S[0]["t"] if S else time.time())
    if S:ax.plot([(s["t"]-t0)/60 for s in S],[s["used_mib"]/1024 for s in S],color=INK,lw=1.2)
    st=sorted(EV["stage_t"].items(),key=lambda kv:kv[1]);keys=list(STAGES);span=max([(E_.get("end_t") or time.time())-t0,1])/60;lastx=-1e9
    for j,(kk,tt) in enumerate(st):
        x=(tt-t0)/60;ax.axvline(x,color=RULE,lw=.8)
        if x-lastx>span*.035:ax.text(x,79,str(keys.index(kk)+1),fontsize=6.4,color=MUTED,ha="center",va="top");lastx=x
    ax.set_ylim(0,82);ax.set_ylabel("GPU used (GiB)",fontsize=7.4);ax.set_xlabel("minutes since the engine started",fontsize=7.4);_axstyle(ax,6.6)
    ax.set_title(f"GPU memory · numbers = live stages · after exit {E_.get('gpu_after_mib','—')} MiB",fontsize=8.2)
    ax2=fig.add_axes([.06,.13,.43,.30])
    kc={"ADAPTIVE":COL["LOOP"],"FIXED":COL["FIX"],"ABLATION":COL["B"],"REPLAY":OK_COL,"OTHER":COL["SYN"]}
    for kind,c in kc.items():
        P=[(f["memory_tokens"],f["fusion_ms"]) for f in FR if f["kind"]==kind and f.get("memory_tokens") and f.get("fusion_ms")]
        if P:ax2.scatter([p[0] for p in P],[p[1]/1000 for p in P],s=14,color=c,alpha=.75,label=f"{kind.lower()} ({len(P)})")
    ax2.set_xlabel("memory tokens after this fusion step",fontsize=7.4);ax2.set_ylabel("native fusion (s)",fontsize=7.4);ax2.set_ylim(bottom=0)
    if FR:ax2.legend(fontsize=6.6,ncol=2,loc="upper left")
    _axstyle(ax2,6.6)
    sv=[f["ssd_verify_ms"] for f in FR if f.get("ssd_verify_ms") is not None];hd=[f["h2d_ms"] for f in FR if f.get("h2d_ms") is not None]
    ax2.set_title(f"{len(FR)} fusion steps · SSD verify {np.median(sv):.0f} ms · CPU→GPU {np.median(hd):.1f} ms (medians)" if sv and hd else "fusion steps",fontsize=8.2)
    cats=OrderedDict()
    for c in CHECKS:
        g=_gate_cat(c["name"]);cats.setdefault(g,[0,0]);cats[g][0 if c["passed"] else 1]+=1
    top=sorted(cats.items(),key=lambda kv:-(kv[1][0]+kv[1][1]))[:20]
    ax3=fig.add_axes([.69,.14,.27,.685]);y=np.arange(len(top))[::-1]
    if top:
        ax3.barh(y,[v[0] for _,v in top],color=OK_COL,height=.66);ax3.barh(y,[v[1] for _,v in top],left=[v[0] for _,v in top],color=RED,height=.66)
        ax3.set_yticks(y);ax3.set_yticklabels([g[:26] for g,_ in top],fontsize=6.3)
        for yi,(_,v) in zip(y,top):ax3.text(v[0]+v[1],yi,f" {v[0]}"+(f" / {v[1]} FAIL" if v[1] else ""),va="center",fontsize=6.2)
        ax3.set_xlim(0,max(v[0]+v[1] for _,v in top)*1.3)
    ax3.set_title(f"engine gates: {sum(1 for c in CHECKS if c['passed'])} PASS · {sum(1 for c in CHECKS if not c['passed'])} FAIL",fontsize=8.4);_axstyle(ax3,6.4)
    T(fig,.06,.535,"Fusion time grows with memory: a pair read (≈1,960 tokens) costs about twice a single read — every read is recomputed natively, nothing is cached.",size=7.4,color=INK2,xmax=.60)
    fig_footer(fig,k,"GPU_SAMPLES.json (host nvidia-smi) · NATIVE_FUSION_STEP lines (engine instrumentation of the locked TEST779 build_fusion) · PASS / FAIL lines grouped by gate name (ENGINE_CHECKS.json).")
    return save_fig(fig,k,"LIVE MEASUREMENT",["GPU_SAMPLES.json","NATIVE_FUSION_STEP lines","ENGINE_CHECKS.json"])

def fig12():
    k="F12";sm=summary();ac=acceptance()
    if not sm or not ac:return fig_missing(k,"The ledger is decided only from this RUN's engine records.","The engine did not complete in this RUN.")
    fig=fig_base(k,"Decided only from this RUN's records — left: what the run demonstrates, with its numbers · right: what the next stage adds","VERIFICATION RECORD")
    V=LIVE.get("verification") or {};C_=V.get("consistency") or {};ev=evidence_classes();nl,ir=ev["none_left"],ev["irrelevant"];rs=rp_summary();cm=cost()
    rw_=rows();t2=sum(1 for r in (rw_ or list(row_logs().values())) if (r.get("offline_routing_eval") or {}).get("top2_relevant"));aud=[r for r in rw_ if ((r.get("offline_fact_audit") or {}).get("adaptive") or {}).get("status")=="NARROW_NUMERIC_FACT_CHECK"]
    rel_ok=sum(1 for r in aud if ((relation().get(r["case_id"]) or {}).get("adaptive") or {}).get("passed"))
    nver=sum(1 for r in (V.get("cartridges") or {}).values() if r.get("file_sha_ok"))
    L=[(bool(ac.get("frozen_weights")) and bool(ac.get("no_residual_hooks")),"Frozen Qwen2.5-72B — no training, no fine-tuning, no hook left behind"),
       (bool(ac.get("physical_cartridges")) and nver==22,f"22 physical CUT3 cartridges on the SSD · host re-hash {nver}/22"),
       (sm.get("routing_top2_relevant")==sm.get("cases") and sm.get("decoy_selected_cases")==0,f"Blind native H3 routing: relevant article in top-2 {sm.get('routing_top2_relevant')}/{sm.get('cases')} · decoys {sm.get('decoy_selected_cases')}/{sm.get('cases')}"),
       (t2==16,f"Paraphrase control: relevant article in top-2 for {t2}/16 wordings"),
       ((sm.get("adaptive_native_reads") or 99)<(sm.get("fixed_native_reads") or 0) and policy().get("changed_decisions")==0,f"Closed loop: {sm.get('adaptive_native_reads')} native reads vs {sm.get('fixed_native_reads')} fixed — same {16-int(policy().get('changed_decisions') or 0)}/16 decisions"),
       ((sm.get("unknown_recovery_observed") or 0)>0,f"Recovered from UNKNOWN {sm.get('unknown_recovery_observed')}× by reading the alternate · {sm.get('hypothesis_revision_observed')} hypothesis revisions"),
       (len(nl)>0 and _n_ab(nl)==len(nl) and _n_ab(ir)==0,f"Evidence removal: abstained {_n_ab(nl)}/{len(nl)} with no relevant article left · answered {len(ir)-_n_ab(ir)}/{len(ir)} when an irrelevant one was removed"),
       (bool(aud) and rel_ok==len(aud),f"Numeric relation audit (98 % DOI · 78 % URL · 80 % automatic): {rel_ok}/{len(aud)}"),
       (rs.get("initial_answer_exact")==rs.get("cases") and bool(rs.get("cases")),f"Same-run replay: first answers byte-identical {rs.get('initial_answer_exact')}/{rs.get('cases')} · rankings {rs.get('rank_top2_exact')}/{rs.get('cases')}"),
       (C_.get("gates_fail")==0 and bool(C_.get("gates_pass")),f"{C_.get('gates_pass','—')} engine gates PASS · {C_.get('gates_fail','—')} FAIL · records cross-checked by the host")]
    box(fig,.035,.12,.535,.745,ec=OK_COL,lw=1.6);rect(fig,.035,.825,.535,.04,OK_COL,z=2);T(fig,.045,.845,"DEMONSTRATED IN THIS RUN",size=10.5,weight="bold",color="white")
    for j,(v,t) in enumerate(L):
        y=.79-j*.067;T(fig,.05,y,okm(v),size=13,weight="bold",color=OK_COL if v else RED);T(fig,.08,y,t,size=8.6,color=INK,xmax=.562)
    ir_=results().get("independent_review") or {}
    N=[("Independent human scientific review",f"all 16 answers exported for reviewers ({ir_.get('cases_exported','—')} cases, SHA {k_sha(ir_.get('sha256'),10)}) — scores not yet entered"),
       ("Cross-run and cross-GPU reproducibility","this run proves same-run replay; repeated runs on other GPUs and seeds come next"),
       ("Larger and harder memory banks",f"here {ac.get('real_sources')} real articles + {ac.get('synthetic_controls')} synthetic decoys; real distractor articles next"),
       ("Finer separation of the two real articles",f"top-1 relevant {sm.get('routing_top1_relevant')}/{sm.get('cases')} — the loop compensates by reading both"),
       ("General autonomous reasoning","not claimed — TEST815 is a bounded, measurable evidence controller")]
    box(fig,.585,.12,.38,.745,ec=AMBER,lw=1.6);rect(fig,.585,.825,.38,.04,AMBER,z=2);T(fig,.595,.845,"NEXT STAGE",size=10.5,weight="bold",color="white")
    for j,(h,t) in enumerate(N):
        y=.785-j*.135;T(fig,.598,y,"→ "+h,size=9.0,weight="bold",color=AMBER,xmax=.958);_layout_text(fig,t,.613,.958,y-.10,y-.018,fs_max=9.6,fs_min=6.2,color=INK2)
    T(fig,.035,.093,f"engine verdict: {ac.get('verdict','—')} · mechanical demo ready {okm(ac.get('mechanical_demo_ready'))} · scientific claim ready {okm(ac.get('scientific_claim_ready'))} (pending human review by design)",size=8.0,weight="bold",color=INK2,xmax=.965)
    fig_footer(fig,k,"Left: summary, demo_acceptance, policy_comparison, source_removal_ablation, relation_audit, replay_summary (TEST815_results.json) + POST_RUN_VERIFICATION.json. Right: flags the engine itself records as open.")
    return save_fig(fig,k,"VERIFICATION RECORD",["TEST815_results.json","POST_RUN_VERIFICATION.json"])

FIG_FUNCS=OrderedDict([("F1",fig1),("F2",fig2),("F3",fig3),("F4",fig4),("F5",fig5),("F6",fig6),("F7",fig7),("F8",fig8),("F9",fig9),("F10",fig10),("F11",fig11),("F12",fig12)])
def render_figures():
    errs={};FIGURES.clear();FIGURES.update(BASE_FIGURES)
    for key,fn in FIG_FUNCS.items():
        t=time.perf_counter();STATE["stages"]["FIGURES"]["note"]=f"drawing Figure {FIGURES[key]['n']}/12 — {FIGURES[key]['title']}";bump()
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
    L=[];a=L.append;sm=summary();ac=acceptance()
    a(f"{APP_NAME} — {APP_SUB}\n{EXPERIMENT} live demonstration · demo {CODE_VERSION} · RUN {SESSION_ID} · written {local_now()}")
    if SIM:a("SIMULATION — NOTHING IN THIS FILE IS AN EXPERIMENTAL RESULT")
    a(f"RUN VERDICT {run_verdict()}\nengine: 815.py git blob {LOCKS[ENGINE_NAME]} executed unchanged as one OS process · engine run folder {EV.get('root')}")
    E_=LIVE.get("engine") or {};a(f"engine process pid {E_.get('pid')} · {E_.get('start')} → {E_.get('end')} · exit {E_.get('exit_code')} · {E_.get('seconds')} s · GPU after exit {E_.get('gpu_after_mib')} MiB")
    a("\nSTAGES (times = this RUN)")
    for key,title in STAGES.items():
        s=STATE["stages"][key];a(f"  [{s['status'].upper():<4}] {key:<10} {('%.0f s'%s['seconds']) if s['seconds'] is not None else '':>8}  {title}\n             {s['note']}")
    if sm:
        a("\nENGINE SUMMARY (TEST815_results.json, verbatim keys)")
        for kk in ("cases","source_count","routing_top1_relevant","routing_top2_relevant","decoy_selected_cases","adaptive_native_reads","fixed_native_reads","adaptive_answers","fixed_answers",
                   "changed_decisions","hypothesis_revision_observed","unknown_recovery_observed","narrow_fact_audit_pass","narrow_fact_audit_total","scientific_accuracy","claim"):a(f"  {kk:<32} {sm.get(kk)}")
    if ac:a(f"\nENGINE ACCEPTANCE  verdict {ac.get('verdict')}\n  "+" · ".join(f"{kk}={v}" for kk,v in ac.items() if kk!="verdict"))
    ev=evidence_classes()
    if ablation():a(f"\nEVIDENCE REMOVAL  abstained with no relevant article left {_n_ab(ev['none_left'])}/{len(ev['none_left'])} · answered with an irrelevant one removed {len(ev['irrelevant'])-_n_ab(ev['irrelevant'])}/{len(ev['irrelevant'])} · answered with another relevant left {len(ev['other_left'])-_n_ab(ev['other_left'])}/{len(ev['other_left'])}")
    for r in rows():
        ad=r.get("adaptive") or {};a(f"\n{r['case_id']} · {r.get('question')}\n  ADAPTIVE {ad.get('action')} · reads {ad.get('read_count')} · path "+" → ".join(f"{s.get('operation')}[{'+'.join(s.get('ids') or [])}]" for s in ad.get("steps") or [])+
                                    "\n  "+str(ad.get("answer")).replace("\n","\n  "))
    a("\nHUMAN REVIEW: NOT PROVIDED (pending) — TEST815_independent_review.csv is the review sheet. No semantic grading was performed by the engine or by this demo.")
    a(f"\n{AUTHOR} · {ORG} · {LICENSE_NAME} · {COPYRIGHT}")
    RUN_SUMMARY.write_text("\n".join(L)+"\n",encoding="utf-8");_private(RUN_SUMMARY)
def download_items():
    items=[("Run summary",RUN_SUMMARY),("Engine output, real-time (UTC receipt · stream · line)",ENGINE_OUT),("Session log",SESSION_LOG),("Session events (JSONL)",SESSION_EVENTS),
           ("Engine process",DATA_DIR/"ENGINE_PROCESS.json"),("GPU samples",DATA_DIR/"GPU_SAMPLES.json"),("Post-run verification",VERIFY_FILE),("Cartridge anatomy (heat-map data)",DATA_DIR/"CARTRIDGE_ANATOMY.npz"),
           ("Fusion steps",DATA_DIR/"FUSION_STEPS.json"),("Stage record",DATA_DIR/"STAGES.json"),("Engine checks of this RUN",DATA_DIR/"ENGINE_CHECKS.json"),("Figure manifest",SESSION_DIR/"FIGURES_MANIFEST.json"),
           ("SHA-256 manifest",MANIFEST),("815.py (locked, executed)",EVID_DIR/ENGINE_NAME)]
    out=[(l,str(p)) for l,p in items if Path(p).is_file()]
    d=DATA_DIR/"engine_records"
    if d.is_dir():out+=[(f"engine record · {p.name}",str(p)) for p in sorted(d.iterdir()) if p.is_file()]
    return out
def package_session():
    dump_json(DATA_DIR/"ENGINE_CHECKS.json",CHECKS);dump_json(DATA_DIR/"STAGES.json",dict(verdict=run_verdict(),stages=STATE["stages"],session=SESSION_ID))
    dump_json(DATA_DIR/"GPU_SAMPLES.json",GPU_SAMPLES);dump_json(DATA_DIR/"FUSION_STEPS.json",fusion_records())
    write_run_summary()
    files=[p for p in sorted(SESSION_DIR.rglob("*")) if p.is_file() and p!=MANIFEST and p.suffix!=".tmp"]
    man=OrderedDict((str(p.relative_to(SESSION_DIR)),dict(sha256=sha_file(p),bytes=p.stat().st_size)) for p in files)
    root=rroot();eng=OrderedDict()
    if root and root.is_dir():
        for p in sorted(root.rglob("*")):
            if p.is_file():eng[str(p.relative_to(root))]=dict(sha256=sha_file(p),bytes=p.stat().st_size)
    dump_json(MANIFEST,dict(session=SESSION_ID,utc=utc_now(),simulation=SIM,engine_run_folder=str(root) if root else None,
                            note="SHA-256 of every file of this RUN. Engine run folder (cartridges, extracted article texts) is hashed, not offered for download. No ZIP.",files=man,engine_files=eng))
    return str(MANIFEST)
def stage_records():
    package_session();return f"{len(FIG_FILES)} JPEG figures + {len(download_items())} records, each downloadable directly · SHA-256 manifest of {len(json.load(open(MANIFEST))['files'])} session files + {len(json.load(open(MANIFEST))['engine_files'])} engine files (no ZIP)"

# ---------------------------------------------------------------------------------------------------------------------
# THE RUN PIPELINE (one button)
# ---------------------------------------------------------------------------------------------------------------------
RUNS_DONE=[]
def run_pipeline():
    if RUNS_DONE:_session_paths(datetime.now().astimezone().strftime("SH815-%Y%m%d-%H%M%S")+f"-RUN{len(RUNS_DONE)+1}")
    RUNS_DONE.append(SESSION_ID);LIVE.clear();LIVE.update(session=SESSION_ID);LINES.clear();CHECKS.clear();FIG_FILES.clear();FIG_ERRORS.clear();PROVENANCE.clear();GPU_SAMPLES.clear();_RC.clear()
    for k_ in ("root","failed","stage"):EV[k_]=None
    for k_ in ("commits","routes","rows","ablation","replay","fusion"):EV[k_]=[]
    EV["records"]={};EV["stage_t"]={}
    STATE.update(running=True,started=utc_now(),finished=None,current=None,elapsed=None,meas=None);STATE["fig_version"]+=1
    for k_ in STAGES:STATE["stages"][k_]=dict(status="wait",seconds=None,note="",t0=None)
    banner(f"RUN {SESSION_ID} · {local_now()} · the locked TEST815 engine as one process (about 40–60 minutes on an A100, model download included)")
    def step(key,fn):
        STATE["current"]=key;stage_set(key,"run");_emit(f"── [{list(STAGES).index(key)+1}/{len(STAGES)}] {STAGES[key]}")
        try:
            note=fn();stage_set(key,"done",note);slog("STAGE_DONE",key,note=note);return True
        except Exception as ex:
            stage_set(key,"fail",f"{type(ex).__name__}: {ex}");slog("STAGE_FAILED",key,error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc()[-3000:]);return False
    try:
        if step("PRECHECK",stage_precheck):
            try:run_engine();slog("ENGINE_DONE","TEST815 completed — every engine stage passed")
            except Exception as ex:slog("ENGINE_NOT_COMPLETED",f"{type(ex).__name__}: {ex}")
        else:
            for s in ENGINE_STAGES:stage_set(s,"skip","not run — PRECHECK did not pass")
        if manifest().get("cartridges"):step("VERIFY",stage_verify)
        else:stage_set("VERIFY","skip","no cartridge manifest in this RUN")
        step("FIGURES",stage_figures);step("RECORDS",stage_records)
    finally:
        STATE.update(running=False,finished=utc_now(),current=None);bump()
        try:package_session()
        except Exception:pass
        banner(f"RUN VERDICT: {run_verdict()}\nRUN {SESSION_ID} finished {local_now()} · "+" · ".join(f"{k_}:{v['status']}" for k_,v in STATE["stages"].items()))
RUN_THREAD={"t":None}
def start_run():
    t=RUN_THREAD["t"]
    if t is not None and t.is_alive():return False
    RUN_THREAD["t"]=threading.Thread(target=run_pipeline,daemon=True,name="SH815-RUN");RUN_THREAD["t"].start();return True
# =====================================================================================================================
# PART 4 / 4 (continued) — Gradio interface (SH782 design): ONE button (RUN). Stages, the engine's own output, the sealed
#              cartridges, routing, the closed loop and every answer appear while the engine works. The page refreshes
#              itself with short requests (gr.Timer) — a dropped connection never hides the figures; a reload shows all.
# =====================================================================================================================
LINEAGE=[("Research Record I — Qwen2.5-7B","https://doi.org/10.5281/zenodo.23381336"),
         ("Research Record II — Mistral-7B, Silicon Hippocampus v1.4","https://doi.org/10.5281/zenodo.23418927"),
         ("Research Record III — Qwen2.5-72B, Direct Internal-State Injection","https://doi.org/10.5281/zenodo.23434686")]
def esc(x):return html.escape(str(x))
def card(title,body,kind="info"):return f'<div class="kz card {kind}"><div class="h">{esc(title)}</div><div class="small">{body}</div></div>'
def ok_mark(v):return "<b style='color:#08785B'>PASS</b>" if v else ("<b style='color:#B91C1C'>FAIL</b>" if v is False else "<span style='opacity:.6'>—</span>")
class Markup(str):pass
def tbl(rows_,head=None,mono_cols=()):
    h="".join(f"<th>{esc(x)}</th>" for x in head) if head else ""
    b="".join("<tr>"+"".join(f"<td class='{'mono' if i in mono_cols else ''}'>{v if isinstance(v,Markup) else esc(v)}</td>" for i,v in enumerate(r))+"</tr>" for r in rows_)
    return f"<table class='tbl'>{('<tr>'+h+'</tr>') if h else ''}{b}</table>"
def pre(text,maxh=420):return f"<div class='ans' style='max-height:{maxh}px'>{esc(text)}</div>"
def details(summary_,inner,open_=False):return f"<details{' open' if open_ else ''}><summary>{summary_}</summary>{inner}</details>"
def yn(v):return Markup("<b style='color:#08785B'>yes</b>" if v else ("<b style='color:#B45309'>no</b>" if v is False else "—"))
def act_mark(a):return Markup(f"<b style='color:{'#08785B' if a=='ANSWER' else '#B91C1C'}'>{esc(a)}</b>") if a else "—"

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
    tiles=[("2 + 20","real articles + synthetic decoys"),("22","physical cartridges on the SSD"),("H3","native routing — no labels"),("2–4","adaptive reads per question"),
           ("16 + 16 + 8","questions · removal trials · replays"),("PENDING","human scientific review")]
    return (f'<div class="kz hero"><span class="rec">Live research demonstration · frozen Qwen2.5-72B-Instruct · NF4 · BF16 · CUT3 · A100 80 GB</span>'
            f'<div class="brand">{esc(APP_NAME)}</div><div class="title">{esc(APP_SUB)}</div>'
            '<div class="by">A frozen 72-billion-parameter model reads two real scientific articles once and stores them — not as text, but as its own internal states — in sealed '
            'memory cartridges on the SSD, next to twenty synthetic decoys. Then it is asked sixteen questions. For each one it must find the right cartridge by itself, from the '
            'question\'s own internal states alone, read it, challenge its first answer with a second source, and decide: answer, or say UNKNOWN. Then the evidence is taken away '
            'to see whether it invents. Everything you see on this page is produced live by the unchanged TEST815 engine.</div>'
            '<div class="tiles">'+"".join(f'<div class="tile"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a,b in tiles)+'</div>'
            f'<div class="by"><b>{esc(AUTHOR)}</b> · {esc(ORG)} · {esc(PLACE)} · {esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · <a href="{REPO}" target="_blank" rel="noopener">{esc(REPO)}</a></div></div>')
def mode_html():
    st=STATE
    if SIM:kind,t="err","SIMULATION — code test of the author with a replayed log and no model, NOT an experimental result"
    elif st.get("running"):
        el=(time.time()-datetime.fromisoformat(st["started"]).timestamp())/60 if st.get("started") else 0
        kind,t="info",f"RUN IN PROGRESS · {el:.0f} min · stage {list(STAGES).index(st['current'])+1 if st.get('current') else '…'}/{len(STAGES)}: {STAGES.get(st.get('current'),'')}"
    elif st.get("finished"):
        ok=run_verdict().startswith("COMPLETE");kind,t=("on" if ok else "err"),f"RUN {SESSION_ID} — {run_verdict()}"
    else:kind,t="info","NOT STARTED — press RUN. The locked TEST815 engine runs as one process on the A100 (about 40–60 minutes, model download included); everything it does appears here while it works."
    return card(t,"The repository holds an earlier TEST815 run (815.log) — this page never shows it: every value, text and figure here comes from THIS RUN. "
                f"Engine 815.py git blob <span class='mono'>{esc(LOCKS[ENGINE_NAME][:16])}…</span> · it imports the locked TEST790 → 789 → 779 chain (709 · 730 · 757 · 721 · 764) by git blob itself.",kind)
def stages_html():
    out=[];n=len(STAGES);done=0
    for i,(k,title) in enumerate(STAGES.items(),1):
        s=STATE["stages"][k];stt=s["status"];mk={"done":"✓","run":"▶","fail":"✗","skip":"–","wait":"○"}[stt]
        if stt in("done","skip","fail"):done+=1
        tm=f" · {s['seconds']:.0f} s" if s.get("seconds") is not None else (f" · running {_mmss(time.perf_counter()-s['t0'])}" if stt=="run" and s.get("t0") else "")
        live=_live_text() if stt=="run" and k==EV.get("stage") and STATE.get("running") and LIVE.get("engine") and not LIVE["engine"].get("end") else ""
        out.append(f"<div class='stg {stt}'>{mk} {i}/{n} · {esc(title)}{tm}"+(f"<span class='nt'>{esc(s['note'])}</span>" if s.get("note") else "")+(f"<span class='nt'>{esc(live)}</span>" if live else "")+"</div>")
    pc=100*done/n
    bar=f'<div style="margin-top:6px;background:#e5e7eb;height:10px;border-radius:2px"><div style="width:{pc:.0f}%;height:10px;background:#7626D9;border-radius:2px"></div></div>'
    head=f"RUN {SESSION_ID} · {run_verdict()}"+(f" · started {STATE['started'][11:19]} UTC" if STATE.get("started") else "")+(f" · finished {STATE['finished'][11:19]} UTC" if STATE.get("finished") else "")
    return card(head,"".join(out)+bar,"m")
def console_text():
    with _LOG_LOCK:return "\n".join(list(CONSOLE)[-200:])

# ---------------------------------------------------------------------------------------------------------------------
# tab contents — read from THIS RUN's records, unedited (partial while the engine works)
# ---------------------------------------------------------------------------------------------------------------------
def _gate(name):
    c=[x for x in CHECKS if x["name"]==name];return (c[-1]["passed"] if c else None)
def _gates(prefix):
    c=[x for x in CHECKS if x["name"].startswith(prefix)];return (all(x["passed"] for x in c) if c else None),len(c)
def overview_html():
    sm=summary();ac=acceptance();ev=evidence_classes() if ablation() else None
    steps=[("The engine verifies its own locked chain","TEST790 / 789 / 779 exact git blobs; 709 · 730 · 757 · 721 · 764 sources and symbols",_gates("GIT_LOCK_")[0] and _gate("TEST779_EXACT_BLOB")),
           ("Two real articles from Europe PMC","exact DOI and title locks · scientific body extracted · SHA-256",_gate("TWO_LOCKED_ARTICLES") if _gate("TWO_LOCKED_ARTICLES") is not None else _gates("EXACT_DOI_LOCK")[0]),
           ("Frozen Qwen2.5-72B forges 22 physical cartridges","H3 + K/V of layers 0–3 · sealed on the SSD · re-opened with SHA checks",_gate("PHYSICAL_22_CARTRIDGES")),
           ("Native H3 routing over all 22 — no labels","the question's own layer-3 states · 8 paraphrase controls",_gate("PARAPHRASE_EIGHT")),
           ("Closed loop vs fixed policy, 16 questions","read → challenge → reverse → decide · max 4 reads",_gate("THIRTY_TWO_POLICY_CASES")),
           ("Evidence removal, 16 trials","each real article removed; best of the 21 survivors read natively",_gate("SOURCE_REMOVAL_16")),
           ("Same-run replay, 8 cases","ranking and first answer recomputed from the same files",_gate("REPLAY_EIGHT")),
           ("Engine acceptance","frozen weights · no residual hooks · review CSV + public audit",(ac.get("mechanical_demo_ready") if ac else None))]
    rows_=[(Markup(f"<b>{i}. {esc(a)}</b><br><span class='small' style='opacity:.85'>{esc(b)}</span>"),Markup(ok_mark(v))) for i,(a,b,v) in enumerate(steps,1)]
    res=""
    if sm:
        res=tbl([("relevant article in the top-2 (no labels)",f"{sm.get('routing_top2_relevant')}/{sm.get('cases')}"),("questions with a decoy in the top-2",f"{sm.get('decoy_selected_cases')}/{sm.get('cases')}"),
                 ("native reads — adaptive vs fixed",f"{sm.get('adaptive_native_reads')} vs {sm.get('fixed_native_reads')} · decisions changed {sm.get('changed_decisions')}"),
                 ("recoveries from UNKNOWN · hypothesis revisions",f"{sm.get('unknown_recovery_observed')} · {sm.get('hypothesis_revision_observed')}"),
                 *([("abstained — no relevant article left",f"{_n_ab(ev['none_left'])}/{len(ev['none_left'])}"),("answered — an irrelevant article removed",f"{len(ev['irrelevant'])-_n_ab(ev['irrelevant'])}/{len(ev['irrelevant'])}")] if ev else []),
                 ("numeric fact audit (Q2 · Q8)",f"{sm.get('narrow_fact_audit_pass')}/{sm.get('narrow_fact_audit_total')}"),("same-run replay, identical first answers",f"{rp_summary().get('initial_answer_exact','—')}/{rp_summary().get('cases','—')}"),
                 ("engine verdict",(ac or {}).get("verdict","—")),("scientific accuracy",sm.get("scientific_accuracy"))],["result of THIS RUN","value"])
    arch=card("Cognitive cartridge + closed loop — what it is and what it is not",
        "<b>Cognitive cartridge:</b> a file on the SSD holding internal states of the frozen Qwen2.5-72B for one text — the layer-3 output H3 and the K/V of layers 0–3 (CUT3). It is reloaded, SHA-checked and fused back at the layer-3 boundary; layers 4–79 recompute everything natively.<br>"
        "<b>Native H3 routing:</b> the question passes through the same frozen layers; its own layer-3 states are scored against 96 sampled states of every cartridge (locked TEST757 numeric_rank). No title, label, keyword or text is used.<br>"
        "<b>Closed loop:</b> the controller reads the top-1 cartridge, challenges a usable answer with the second, reads the alternate when the first says UNKNOWN, checks the reverse order when the readings disagree, then answers or abstains — at most four native reads.<br>"
        "<b>Not text RAG · not fine-tuning:</b> no article text in the prompt; the weights are frozen and no hook stays registered.<br>"
        "<b>Not a semantic grade:</b> correctness of the answers is open to independent human review (CSV exported); the run itself checks numbers and their relations narrowly.","info")
    lin=card("Research lineage (published records and repository — not results of this run)","<br>".join(f"{esc(t)} · <a href='{u}' target='_blank' rel='noopener'>{esc(u)}</a>" for t,u in LINEAGE)+
             f"<br>Engine: <a href='{URL_815}' target='_blank' rel='noopener'>815.py</a> · earlier published run of the same engine: <a href='{URL_815_LOG}' target='_blank' rel='noopener'>815.log</a> (not used here)","info")
    return card(f"What happens in this RUN ({SESSION_ID})",tbl(rows_,["step","this RUN"]),"m")+(card("Results of this RUN",res,"on") if res else "")+arch+lin
def bank_html():
    D=documents();E=manifest().get("cartridges") or {};V=(LIVE.get("verification") or {}).get("cartridges") or {}
    out=""
    for c in REAL_IDS:
        d=D.get(c) or {};src=next((x for x in EV["records"].get("sources",[]) if x.get("pmcid")==c),{})
        if not d and not src:continue
        rows_=[("article",f"{REAL[c]['title']} · {REAL[c]['journal']}"),("DOI",d.get("doi") or src.get("doi")),("Europe PMC XML",d.get("xml_url")),("XML SHA-256",d.get("xml_sha256")),
               ("extracted / excerpt",f"{d.get('full_extracted_chars','—')} characters extracted · excerpt {d.get('excerpt_chars','—')} characters"),
               ("stored in the cartridge",f"{d.get('physical_text_tokens','—')} tokens · SHA-256 {d.get('physical_text_sha256','—')}"),("licence handling",d.get("license"))]
        out+=card(f"{c} — {REAL[c]['short']}",tbl(rows_,mono_cols=(1,))+"<div class='small' style='opacity:.8'>The article text is not redistributed by this demonstration — it is linked and hash-recorded; read it at the publisher.</div>","m")
    if not out:out=card("Sources","Not available yet — the engine loads the two articles in stage 3.","info")
    rows_=[(c,cshort(c) if is_real(c) else (E[c].get("role") or "")[:28],E[c].get("body_tokens"),E[c].get("n"),f"{E[c].get('forge_seconds')} s",E[c].get("sha256"),
            Markup(ok_mark((V.get(c) or {}).get("file_sha_ok"))),fmt_b((V.get(c) or {}).get("bytes"))) for c in cartridge_ids() if c in E]
    live=f"{len(EV['commits'])}/22 cartridges committed so far (PHYSICAL_COMMIT lines)" if EV["commits"] else ""
    return out+card("Physical cartridges of this RUN",(tbl(rows_,["id","role / article","body tokens","n","forge","file SHA-256 (manifest)","host re-hash","file"],mono_cols=(5,))if rows_ else live or "not written yet"),"m")
def routing_html():
    M,ids=score_matrix();Q=questions()
    if M is None:return card("H3 routing","Not available yet — routing runs after the 22 cartridges are sealed (stage 6).","info")
    rows_=[]
    for i,c in enumerate(CASES):
        if np.all(np.isnan(M[i])):continue
        order=[ids[j] for j in np.argsort(-np.nan_to_num(M[i],nan=-9))];rel=relevant(c)
        dec=max((M[i,j] for j,x in enumerate(ids) if not is_real(x)),default=np.nan);rv=max((M[i,ids.index(x)] for x in rel if x in ids),default=np.nan)
        rows_.append((c,short(Q.get(c) or "",90),f"{order[0]} ({M[i,ids.index(order[0])]:.4f})",order[1],", ".join(rel),yn(order[0] in rel),yn(bool(set(order[:2])&set(rel))),f"{rv-dec:+.4f}"))
    pr=[(r["case_id"],r.get("original_top1"),r.get("paraphrase_top1"),yn(r.get("same_top1")),yn(r.get("original_top1_relevant")),yn(r.get("paraphrase_top1_relevant"))) for r in routes()]
    return (card("Native H3 routing — all 22 cartridges scored for every question",tbl(rows_,["case","question","top-1 (score)","top-2","relevant (offline key)","top-1 relevant","in top-2","margin over best decoy"],mono_cols=(2,7)),"m")+
            card("Paraphrase controls",tbl(pr,["case","original top-1","paraphrase top-1","same","original relevant","paraphrase relevant"]) if pr else "after the routing stage","info"))
def loop_html():
    TA=tracks("ADAPTIVE");TF=tracks("FIXED");RL=row_logs()
    if not TA and not RL:return card("Closed loop","Not available yet — the 16 closed-loop cases run in stage 7.","info")
    rows_=[]
    for c in CASES:
        r=row(c) or {};ad=r.get("adaptive") or {};lg=RL.get(c) or {}
        if not TA.get(c) and not lg:continue
        rows_.append((c," → ".join(f"{oplab(s['op'])} [{ids_lab(s['ids'])}]" for s in TA.get(c,[])),len(TA.get(c,[])) or lg.get("adaptive_reads"),act_mark(ad.get("action") or lg.get("adaptive_action")),
                      "recovered" if ad.get("recovered_from_unknown") else ("revised" if (ad.get("revision") if ad else lg.get("adaptive_revision")) else "—"),ad.get("support","—"),len(TF.get(c,[])) or lg.get("fixed_reads"),act_mark((r.get("fixed") or {}).get("action") or lg.get("fixed_action"))))
    cm=cost();pc=policy()
    ct=tbl([(k_,json.dumps(jsafe(v),ensure_ascii=False)) for k_,v in cm.items()]+[("policy comparison",json.dumps(jsafe(pc),ensure_ascii=False))],["policy","engine record"],mono_cols=(1,)) if cm else "after the closed-loop stage"
    return card("Every read of every question (A = PMC9521804 · B = PMC9401135)",tbl(rows_,["case","adaptive path","reads","adaptive","hypothesis","support","fixed reads","fixed"]),"m")+card("Cost matrix and policy comparison (engine records)",ct,"info")
def evidence_html():
    AB=ablation()
    if not AB:return card("Evidence controls","Not available yet — the removal trials run in stage 8.","info")
    rows_=[(a["case_id"],f"{L_(a['removed'])} · {cshort(a['removed'])}",(L_(a.get("top1")) if is_real(a.get("top1")) else a.get("top1")),yn(a.get("removed_relevant_offline")),act_mark(a.get("native_action")),a.get("native_tokens"),Markup(f"<span class='small'>{esc(a.get('native_answer'))}</span>")) for a in AB]
    ev=evidence_classes()
    head=(f"abstained with no relevant article left {_n_ab(ev['none_left'])}/{len(ev['none_left'])} · answered when an irrelevant article was removed {len(ev['irrelevant'])-_n_ab(ev['irrelevant'])}/{len(ev['irrelevant'])} · "
          f"answered with another relevant article left {len(ev['other_left'])-_n_ab(ev['other_left'])}/{len(ev['other_left'])} · decoy read instead {sum(1 for a in AB if a.get('selected_synthetic'))}/{len(AB)}")
    fa=[];RA=relation()
    for r in rows():
        f_=(r.get("offline_fact_audit") or {}).get("adaptive") or {}
        if f_.get("status")=="NARROW_NUMERIC_FACT_CHECK":
            ra=(RA.get(r["case_id"]) or {}).get("adaptive") or {}
            fa.append((r["case_id"],", ".join(f_.get("required") or []),", ".join(f_.get("observed") or []),Markup(ok_mark(f_.get("passed"))),Markup(ok_mark(ra.get("passed"))),json.dumps({k_:v for k_,v in ra.items() if k_ not in("status","passed")})))
    return (card("Source removal — 16 native trials (verbatim answers)",f"<div class='small'><b>{esc(head)}</b></div>"+tbl(rows_,["case","removed","read instead","removed was relevant","action","tokens","native answer (verbatim)"]),"m")+
            card("Numeric fact and relation audit (offline key, after inference)",tbl(fa,["case","required","observed","numbers","relations","relation detail"],mono_cols=(5,)) if fa else "after the closed-loop stage","info"))
def answers_html():
    rw=rows()
    if not rw:return card("Answers","Not available yet — answers are written by the engine during the closed-loop stage.","info")
    out=""
    for r in rw:
        ad=r.get("adaptive") or {};fx=r.get("fixed") or {}
        st="".join(details(f"{esc(s.get('operation'))} · {esc('+'.join(s.get('ids') or []))} · {s.get('tokens')} tokens · {s.get('elapsed_seconds')} s"+(" · possible truncation" if s.get("possible_truncation") else ""),pre(s.get("raw"),220)) for s in ad.get("steps") or [])
        sf="".join(details(f"FIXED {esc(s.get('operation'))} · {esc('+'.join(s.get('ids') or []))} · {s.get('tokens')} tokens",pre(s.get("raw"),200)) for s in fx.get("steps") or [])
        out+=card(f"{r['case_id']} · ADAPTIVE {ad.get('action')} · {ad.get('read_count')} reads"+(" · recovered from UNKNOWN" if ad.get("recovered_from_unknown") else (" · revised" if ad.get("revision") else "")),
                  f"<b>{esc(r.get('question'))}</b>"+pre(ad.get("answer"),300)+st+details(f"FIXED policy · {fx.get('action')} · {fx.get('read_count')} reads",pre(fx.get("answer"),240)+sf),"m")
    return card("All answers — verbatim, unedited","The frozen model's own words after reading physical memory. Independent human review: TEST815_independent_review.csv (download list).","info")+out
def integrity_html():
    rp=[(r["case_id"],yn(r.get("rank_top1_identical")),yn(r.get("rank_top2_identical")),yn(r.get("exact_initial_answer_identical")),k_sha(r.get("initial_original_sha256"),20),k_sha(r.get("initial_replay_sha256"),20),f"{r.get('original_seconds')} → {r.get('replay_seconds')}") for r in replay()]
    cats=OrderedDict()
    for c in CHECKS:
        g=_gate_cat(c["name"]);cats.setdefault(g,[0,0]);cats[g][0 if c["passed"] else 1]+=1
    gc_=[(g,v[0],v[1]) for g,v in cats.items()];last=[(c["utc"][11:19],c["name"],Markup(ok_mark(c["passed"])),c["detail"][:140]) for c in CHECKS[-60:]]
    fails=[(c["utc"][11:19],c["name"],c["detail"][:200]) for c in CHECKS if not c["passed"]]
    src=[(n,v["git_blob"],v["sha256"],f"{v['bytes']:,}",v.get("obtained")) for n,v in SOURCES.items()]+[(n,b,"verified inside the engine","—","engine (fail-closed)") for n,b in ENGINE_CHAIN.items()];V=LIVE.get("verification") or {}
    return (card("Same-run replay",tbl(rp,["case","top-1","top-2","first answer identical","SHA-256 original","SHA-256 replay","seconds"],mono_cols=(4,5)) if rp else "after the replay stage","on" if rp and all(r.get("exact_initial_answer_identical") for r in replay()) else "info")+
            card(f"Engine gates of this RUN — {sum(1 for c in CHECKS if c['passed'])} PASS · {sum(1 for c in CHECKS if not c['passed'])} FAIL",(tbl(fails,["UTC","FAILED gate","detail"]) if fails else "")+
                 details("gates grouped by name",tbl(gc_,["gate","PASS","FAIL"]))+details("last 60 gates",tbl(last,["UTC","gate","result","detail"],mono_cols=(3,))),"on" if CHECKS and not fails else ("err" if fails else "info"))+
            card("Independent re-verification after the run (read-only, host)",pre(json.dumps(jsafe({k_:v for k_,v in V.items()}),indent=1),420) if V else "after the engine has finished","info")+
            card("Locked sources (git blob verified)",tbl(src,["file","git blob","SHA-256","bytes","obtained"],mono_cols=(1,2)),"info"))
def resources_html():
    E_=LIVE.get("engine") or {};G=LIVE.get("gpu") or {};D=LIVE.get("disk") or {};S=[s["used_mib"] for s in GPU_SAMPLES if s.get("used_mib") is not None];FR=fusion_records()
    pr=tbl([("GPU",f"{G.get('name')} · {G.get('total_mib')} MiB · driver {G.get('driver')}"),("before RUN",f"{G.get('used_mib')} MiB used · processes {G.get('apps')}"),("disk",f"{D.get('free_gib')} GiB free · model cache {D.get('model_cache_gib')} GiB"),
            ("engine process",f"pid {E_.get('pid')} · {E_.get('start')} → {E_.get('end')} · exit {E_.get('exit_code')} · {E_.get('seconds')} s"),("GPU after exit",f"{E_.get('gpu_after_mib')} MiB"),
            ("GPU samples",f"{len(S)} · peak {max(S)/1024:.1f} GiB" if S else "—")],["item","this RUN"]) if G else "after PRECHECK"
    ft=""
    if FR:
        grp=OrderedDict()
        for f in FR:grp.setdefault((f["kind"],f.get("memory_tokens",0)>1500),[]).append(f)
        ft=tbl([(k_[0],"pair (2nd cartridge)" if k_[1] else "single",len(v),f"{np.median([x['ssd_verify_ms'] for x in v]):.0f}",f"{np.median([x['h2d_ms'] for x in v]):.1f}",f"{np.median([x['fusion_ms'] for x in v]):.0f}") for k_,v in grp.items()],
               ["kind","fusion step","n","SSD verify ms (median)","CPU→GPU ms","fusion ms"])
    return card("Hardware and the engine process",pr,"m")+card("Native fusion steps (NATIVE_FUSION_STEP lines)",ft or "after the first native read","info")
TABS=["OVERVIEW","CARTRIDGE BANK","H3 ROUTING","CLOSED LOOP","EVIDENCE CONTROLS","ANSWERS","REPLAY · INTEGRITY","RESOURCES","SCIENTIFIC FIGURES"]
TAB_HTML={"OVERVIEW":overview_html,"CARTRIDGE BANK":bank_html,"H3 ROUTING":routing_html,"CLOSED LOOP":loop_html,"EVIDENCE CONTROLS":evidence_html,"ANSWERS":answers_html,
          "REPLAY · INTEGRITY":integrity_html,"RESOURCES":resources_html}
def _figlabel(k):m=FIGURES[k];return f"Figure {m['n']} — {m['title']}"
def tab_gallery(tab):
    keys=[k for k,m in FIGURES.items() if (m["tab"]==tab or tab=="SCIENTIFIC FIGURES") and k in FIG_FILES]
    return [(FIG_FILES[k]["jpg"],f"{_figlabel(k)} · {FIG_FILES[k]['badge']}") for k in keys]
def figs_status_html():
    n=len(FIG_FILES)
    if not n and not FIG_ERRORS:return card(f"Scientific figures of this RUN — 0/{len(BASE_FIGURES)}","The twelve figures are drawn from this RUN's outputs after the engine has finished (stage 12). They appear here, one below the other.","info")
    def st(k):
        f=FIG_FILES.get(k)
        if not f:return "NOT GENERATED: "+str(FIG_ERRORS.get(k,"pending"))
        q=f.get("layout_qc") or {};j=f.get("jpeg_qc") or {}
        return f"{f['badge']} · {f['pixels'][0]}×{f['pixels'][1]} JPEG 300 dpi · layout QC {'PASS' if q.get('passed') else 'FAIL'} · JPEG QC {'PASS' if j.get('passed') else 'FAIL'}"
    rows_="".join(f"<div class='small'>{'✓' if k in FIG_FILES and (FIG_FILES[k].get('layout_qc') or {}).get('passed') and FIG_FILES[k]['badge']!='NOT PRODUCED IN THIS RUN' else '✗'} {esc(_figlabel(k))} · <b>{esc(st(k))}</b></div>" for k in FIGURES)
    ok=all(k in FIG_FILES for k in BASE_FIGURES) and all((v.get("layout_qc") or {}).get("passed") and v["badge"]!="NOT PRODUCED IN THIS RUN" for v in FIG_FILES.values())
    return card(f"Scientific figures of this RUN ({SESSION_ID}) — {n} JPEG file(s)",rows_,"on" if ok else "warn")
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
    _live_root();v=STATE["version"];fv=STATE["fig_version"];out=[_safe(mode_html),_safe(stages_html),console_text()]
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
        con=_tb(lines=12,max_lines=20,label="Live engine output of this RUN — every line the TEST815 engine prints (TEST815 | line); progress bars update one line; also ENGINE_OUTPUT_REALTIME.log",value=console_text(),interactive=False)
        fstat=gr.HTML(_safe(figs_status_html));main_figs=gr.HTML(_safe(figs_main_html))
        jpgs=gr.File(label="The JPEG figures of this RUN, in order — each file downloads with one tap",value=(jpg_files() or None),file_count="multiple",interactive=False)
        files=gr.File(label="Real-time engine output, session log, engine records (results, manifest, log, review CSV, public audit), verification — direct downloads (no ZIP)",value=(all_files() or None),file_count="multiple",interactive=False)
        htmls={};gals={}
        with gr.Tabs():
            for t in TABS:
                with gr.Tab(t):
                    if t in TAB_HTML:htmls[t]=gr.HTML(_safe(TAB_HTML[t]))
                    gals[t]=_gallery(label=f"{t} · figures",value=tab_gallery(t))
        gr.HTML(f'<div class="kz small" style="opacity:.8;margin:10px 0 18px">{esc(AUTHOR)} · {esc(ORG)} · {esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · '
                f'<a href="{file_url(EVID_DIR/ENGINE_NAME)}" download="815.py">815.py (the locked copy executed here)</a> · <a href="{URL_LICENSE}" target="_blank" rel="noopener">LICENSE</a> · '
                'Source articles: PLOS Computational Biology (doi:10.1371/journal.pcbi.1010476) and PLOS ONE (doi:10.1371/journal.pone.0272845) via Europe PMC — linked, hash-recorded, not redistributed · '
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
            port=int(re.search(r":(\d+)",str(local)).group(1));_co.serve_kernel_port_as_window(port,anchor_text="▶ Open the AKBASCORE TEST815 interface (Colab window)");window=f"Colab port window, port {port}"
        except Exception as ex:window=f"not available ({type(ex).__name__})"
    dump_json(GRADIO_LINK.with_suffix(".json"),dict(utc=utc_now(),session=SESSION_ID,share_url=share,local_url=local,colab_window=window,share_error=err))
    GRADIO_LINK.write_text(f"{share or local}\n",encoding="utf-8")
    banner(f"INTERFACE OPEN · {share or ('local only: '+str(local))}\n  public link : {share or ('— (tunnel not available'+(': '+str(err)[:120] if err else '')+'; use the Colab window link above)')}\n  local       : {local}\n"
           f"  Press RUN in the interface — everything else runs automatically. If the link stops working: run  launch_interface()  in a new cell.","#")
    slog("LAUNCH","interface open",share_url=share,local_url=local,colab_window=window);return share or local
def keep_cell_running():
    """keeps this Colab cell RUNNING while the interface is in use; when a RUN has finished its figures are shown here too"""
    banner("THE CELL STAYS RUNNING — the interface is live. Press RUN in the interface; the engine output is printed here and shown in the interface.\n"
           f"  A full RUN takes about 40–60 minutes on an A100. Stop this cell (■) only when you have finished; the files stay in {DEMO_ROOT}","#")
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
    slog("ENGINE_READY","815.py locked; it runs unchanged as one OS process when RUN is pressed",git_blob=LOCKS[ENGINE_NAME])
_AKB815_PARTS.add(4)
_missing=[n for n in (1,2,3) if n not in _AKB815_PARTS]
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
if os.environ.get("AKB815_NO_BLOCK")!="1":keep_cell_running()
# ===== END OF PART 4/4 =====



