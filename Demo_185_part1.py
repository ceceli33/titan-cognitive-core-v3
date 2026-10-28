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
