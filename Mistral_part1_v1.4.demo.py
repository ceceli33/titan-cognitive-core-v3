# =====================================================================================================================
# AKBASCORE AI TECHNOLOGY — MAM SILICON HIPPOCAMPUS v1.4 · MISTRAL CUT6
# Native Cognitive Cartridge Injection · Mistral-7B-Instruct-v0.3 · single Google Colab cell (3 parts) · NVIDIA A100 40 GB
# ---------------------------------------------------------------------------------------------------------------------
# What this program does
#   1. Downloads the locked TEST684 bootstrap (git blob verified) and executes it UNCHANGED up to the same boundary that
#      the sealed TEST686 uses. That bootstrap downloads and blob-verifies TEST560 (frozen Mistral, CUT6 engine:
#      forge_checkpoint / init_incremental / append_incremental / answer_layers), TEST659 (native BF16 CUDA append_kv
#      kernel) and TEST677, loads the frozen model and runs its own gates.
#   2. Executes the TEST686 scenario functions (keys686, grade686, staged686 …) extracted VERBATIM by AST from the
#      blob-verified 686.py, on the Qwen v1.4 scenario definitions read AS DATA from the SHA-256-verified v1.4 part 1.
#   3. Adds a READ-ONLY measurement layer (recording pre-hook that returns nothing; bitwise tensor comparisons) and
#      renders EIGHT academic figures (JPEG, about 4000 px wide) only from values measured in the current session,
#      writes JSON/TXT records, a SHA-256 manifest and one ZIP, and serves everything through Gradio.
# Scientific boundaries (also printed in the interface and in the figures)
#   · The two scenarios are fictional/synthetic. No real-world claim is made about them.
#   · The three-step chain is a PREDEFINED, EXTERNAL question sequence (v1.4 hop_prompts); not autonomous planning.
#   · Generation is limited to 16 new tokens (TEST560 MAX_NEW); free text is unscored and can be truncated.
#   · Strict TEST686 scoring is the score. Mistral often answers "UNKNOWN (explanation …)", which the strict rule counts
#     as unsupported; a TEST684 descriptive audit is shown SEPARATELY and never replaces the strict score.
# Author / licence
#   Mustafa Akbaş · AkbasCore AI Teknoloji · AKBASCORE RESEARCH SOFTWARE LICENSE
#   https://github.com/ceceli33/titan-cognitive-core-v2
# =====================================================================================================================
import os,sys,re,io,json,time,html,math,shutil,zipfile,hashlib,platform,threading,traceback,subprocess,importlib.util,textwrap,unicodedata,copy
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter,OrderedDict

MODEL_ID_GATED="mistralai/Mistral-7B-Instruct-v0.3"
LAYOUT_TEST=os.environ.get("AKB14M_LAYOUT_TEST")=="1"   # GPU-free figure/packaging self-test only (never used in Colab)

def _ensure(mod,pkg=None):
    if importlib.util.find_spec(mod) is None:
        subprocess.check_call([sys.executable,"-m","pip","install","-q",pkg or mod])
for _m,_p in (("numpy",None),("matplotlib",None),("PIL","pillow")):_ensure(_m,_p)
def _hub_version():
    try:
        r=subprocess.run([sys.executable,"-c","import huggingface_hub;print(huggingface_hub.__version__)"],capture_output=True,text=True,timeout=120)
        return r.stdout.strip() if r.returncode==0 else None
    except Exception:return None
def _imports_ok(mods):
    r=subprocess.run([sys.executable,"-c","import "+",".join(mods)],capture_output=True,text=True,timeout=600)
    return r.returncode==0,(r.stderr or "").strip().splitlines()[-1:] 
if not LAYOUT_TEST and importlib.util.find_spec("gradio") is None:
    # installing gradio must not silently replace the huggingface_hub that the installed transformers needs
    _hv=_hub_version() if importlib.util.find_spec("transformers") else None
    try:
        if _hv:subprocess.check_call([sys.executable,"-m","pip","install","-q","gradio",f"huggingface_hub=={_hv}"])
        else:raise RuntimeError("no pinned hub")
    except Exception:
        subprocess.check_call([sys.executable,"-m","pip","install","-q","gradio"])
    if importlib.util.find_spec("transformers"):
        _ok,_err=_imports_ok(["torch","transformers","gradio"])
        if not _ok:
            raise RuntimeError("After installing gradio, 'import transformers' fails in this runtime ("+" ".join(_err)+"). "
                               "Fix: Runtime → Restart session, then run the cell again (gradio is already installed the second time).")

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch,Patch,FancyBboxPatch
from matplotlib.lines import Line2D
from matplotlib.text import Text
from PIL import Image
if not LAYOUT_TEST:
    import torch
    import gradio as gr
    # ---- pre-flight: the frozen Mistral-7B (BF16, about 14.5 GB) needs a CUDA GPU; the model is gated on Hugging Face
    if not torch.cuda.is_available():
        raise RuntimeError("NO GPU in this Colab runtime. Runtime → Change runtime type → A100 GPU, then run the cell again.")
    _gp=torch.cuda.get_device_properties(0);_gib=_gp.total_memory/2**30
    print(f"[pre-flight] GPU {_gp.name} · {_gib:.1f} GiB · torch {torch.__version__} · gradio {gr.__version__}",flush=True)
    if _gib<22:print("[pre-flight] WARNING: less than 22 GiB GPU memory. The demonstration was designed for an A100 40 GB; it may run out of memory.",flush=True)
    if not torch.cuda.is_bf16_supported():print("[pre-flight] WARNING: this GPU has no native BF16 support (e.g. T4). Use an A100 or L4 runtime.",flush=True)
    if not (os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")):
        try:
            from google.colab import userdata as _ud
            _t=_ud.get("HF_TOKEN")
            if _t:os.environ["HF_TOKEN"]=_t;print("[pre-flight] Hugging Face token read from Colab secret HF_TOKEN",flush=True)
        except Exception as _ex:
            print(f"[pre-flight] note: no HF_TOKEN found ({type(_ex).__name__}). {MODEL_ID_GATED} is a gated model: accept its licence on huggingface.co and add your token as the Colab secret HF_TOKEN if loading fails.",flush=True)

# ---------------------------------------------------------------------------------------------------------------------
# identity, references and locks
# ---------------------------------------------------------------------------------------------------------------------
APP_TITLE="AKBASCORE AI TECHNOLOGY — MAM SILICON HIPPOCAMPUS v1.4 · MISTRAL CUT6"
APP_SUB="Native Cognitive Cartridge Injection · Inside a Frozen Transformer: From Text to Tensor Memory"
APP_SHORT="AKBASCORE MAM SILICON HIPPOCAMPUS v1.4 · MISTRAL CUT6"
AUTHOR="Mustafa Akbaş";ORG="AkbasCore AI Teknoloji";PLACE="Mersin, Türkiye"
LICENSE_NAME="AKBASCORE RESEARCH SOFTWARE LICENSE";REPO="https://github.com/ceceli33/titan-cognitive-core-v2"
COPYRIGHT="Copyright © 2026 Mustafa Akbaş"
MODEL_ID="mistralai/Mistral-7B-Instruct-v0.3";ARCH_EXPECTED=(32,4096,32,8,128);CUT=6
RAW_BASE="https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v2/main/"
# locked sources (git blob SHA-1 = git hash-object; SHA-256 of the file bytes)
LOCKS=dict(
  test684_blob="0af7ae24840bff722587ea05c0045a8516a43289",      # TEST684 bootstrap (checked by sealed TEST686 as well)
  test686_blob="8ff95e750b941bb3450fe1e1210aa6dcc6747d58",      # TEST686: scenario/grading/staged functions taken verbatim
  test560_blob="35d95a929a4e043a9af346c67fc103da47a792b5",      # TEST560 Mistral CUT6 engine (checked inside TEST684)
  test659_blob="5f90660828d4bf0dd126727d038d4b70bc6b856d",      # TEST659 native CUDA append source (checked inside TEST684)
  test677_blob="5b65959423b7bbdd209b654417eb5fa30ceb2626",      # TEST677 (checked inside TEST684)
  v14_part1_sha256="6283e70c8346d65df341971bf12e1b976609baec46e958c820e20ed36300a323",  # Qwen v1.4 protocol (scenarios, scoring)
  test686_log_sha256="57424560ad38aea65d9ae3ceedc9d15610a40c7e6195f59a3281d998bcb4bfad")
TEST684_MARKER="# Verify native append is bitwise-identical to TEST560 reference on the SAME freshly built cartridges."
TEST686_FUNCTIONS=("normalize686","unknown686","expected686","grade686","staged686","keys686")
TEST684_AUDIT_NAMES=("UNKNOWN_HEAD","NEGATION","REVERSE_FORMS","clean680","head680","audit680")
WEIGHT_SHA_REFERENCE=None     # no published full-weight reference exists for Mistral; the value is recorded, not compared
URL_686=REPO+"/blob/main/686.py";URL_686_LOG=REPO+"/blob/main/686.log";URL_684=REPO+"/blob/main/684.py";URL_560=REPO+"/blob/main/560.py"
URL_659=REPO+"/blob/main/659.py";URL_V14=REPO+"/blob/main/HIPPOCAMPUS_1.4_part1.py"
# Sealed TEST686 summary (copied from 686.log line 300–302; earlier Mistral run, NOT re-measured by this demonstration)
TEST686_REF=dict(
    questions={"DC_CUT6_NATIVE":{"CORRECT_KNOWN":34,"WRONG_KNOWN":4,"UNSUPPORTED":43,"UNSCORED":18},
               "TEXT_JOINT":{"CORRECT_KNOWN":34,"WRONG_KNOWN":4,"UNSUPPORTED":43,"UNSCORED":18}},
    chains={"DC_CUT6_NATIVE":{"CORRECT_KNOWN":4,"CORRECT_ABSTENTION":2,"WRONG_KNOWN":1,"UNSUPPORTED":11},
            "TEXT_JOINT":{"CORRECT_KNOWN":4,"CORRECT_ABSTENTION":2,"WRONG_KNOWN":1,"UNSUPPORTED":11}},
    rows=198,staged=36,errors=0,seconds=269.35,
    note="TEST686 sealed record (686.log). Strict scoring: 'UNKNOWN (explanation …)' answers count as UNSUPPORTED.")
QWEN_V14_REF=dict(run="MAM14-20261014-220212-0001",note="Qwen2.5-7B v1.4 published run — a different model; never shown as a Mistral result")

CONDITIONS=("NONE","A","B","C","AB","AC","BC","ABC","ABC_CF")
REPRESENTATIONS=("DC_CUT6_NATIVE","TEXT_JOINT")
REP_MAIN="DC_CUT6_NATIVE"
SCENARIO_LABEL={"AKBASCORE":"Demonstration A — Mustafa Akbaş / AKBASCORE","MATRIX":"Demonstration B — The Matrix / Neo"}
SLOT_LABEL={"AKBASCORE":{"A":"Cartridge A — Activation","B":"Cartridge B — Conversion","C":"Cartridge C — Effect","C_CF":"Counterfactual C (used only in ABC_CF)"},
            "MATRIX":{"A":"Cartridge A — Upload","B":"Cartridge B — Knowledge","C":"Cartridge C — Ability","C_CF":"Counterfactual C (used only in ABC_CF)"}}

# ---------------------------------------------------------------------------------------------------------------------
# audit metadata for scoring (used only AFTER generation; never shown to the model)
#   req  = list of alternative cartridge sets; the question is answerable from memory if one set is fully present
#   AKBASCORE requirement sets and aliases follow the TEST677 gold definition for the same texts.
#   MATRIX requirement sets were derived by reading the v1.4 texts: cartridge C itself names MX-71 and the Kung Fu
#   knowledge, so CONTENT is supported by B or C and FINAL needs only A and C.
# ---------------------------------------------------------------------------------------------------------------------
ALIASES={"reversal of time flow":["time flow reversal","reversed time flow","reversing time flow","time reversal"],
         "AKBASCORE MAM":["AKBASCORE MAM architecture","the AKBASCORE MAM architecture"],
         "Morvex":["Morvex energy"],"temporal stasis":["a temporal stasis"],
         "Kung Fu knowledge":["Kung Fu"],"3":["layer 3","layer-3","layer three"],"MX-71":["cartridge MX-71"],
         "bullet-dodge ability":["bullet-dodge","bullet-dodging ability","the ability to dodge bullets"],
         "slow-motion perception":["slow motion perception"],"Tank":[]}
SCORING={
 "AKBASCORE":dict(
   questions={"ACTIVATION":dict(req=[("A",)],gold="AKBASCORE MAM"),
              "CONVERSION":dict(req=[("A","B")],gold="Morvex"),
              "EFFECT":dict(req=[("B","C")],gold="reversal of time flow",cf_gold="temporal stasis"),
              "FINAL":dict(req=[("A","B","C")],gold="reversal of time flow",cf_gold="temporal stasis"),
              "SYNTHESIS":None},
   hops=[dict(req=[("A",)],gold="AKBASCORE MAM"),dict(req=[("B",)],gold="Morvex"),dict(req=[("C",)],gold="reversal of time flow",cf_gold="temporal stasis")],
   chain=dict(req=[("A","B","C")],gold="reversal of time flow",cf_gold="temporal stasis"),
   chain_text=["Mustafa Akbaş","AKBASCORE MAM","dibekgoz crystal resonance","Morvex energy","reversal of time flow"]),
 "MATRIX":dict(
   questions={"ACTIVATION":dict(req=[("A",)],gold="Tank"),
              "CONTENT":dict(req=[("B",),("C",)],gold="Kung Fu knowledge"),
              "INJECTION":dict(req=[("B",)],gold="3"),
              "EFFECT":dict(req=[("C",)],gold="bullet-dodge ability",cf_gold="slow-motion perception"),
              "FINAL":dict(req=[("A","C")],gold="bullet-dodge ability",cf_gold="slow-motion perception"),
              "SYNTHESIS":None},
   hops=[dict(req=[("A",)],gold="MX-71"),dict(req=[("B",),("C",)],gold="Kung Fu knowledge"),dict(req=[("C",)],gold="bullet-dodge ability",cf_gold="slow-motion perception")],
   chain=dict(req=[("A","C")],gold="bullet-dodge ability",cf_gold="slow-motion perception"),
   chain_text=["Tank","Cartridge MX-71","Kung Fu knowledge","Neo","bullet-dodge ability"])}
STATUS_ORDER=("CORRECT_KNOWN","CORRECT_ABSTENTION","UNSUPPORTED","MISSED_KNOWN","WRONG_KNOWN","UNSCORED")
STATUS_SHORT={"CORRECT_KNOWN":"correct","CORRECT_ABSTENTION":"correct UNKNOWN","UNSUPPORTED":"unsupported","MISSED_KNOWN":"missed","WRONG_KNOWN":"wrong","UNSCORED":"unscored"}

def norm_ans(x):return re.sub(r"[^a-z0-9]","",str(x).casefold())
def is_unknown(x):
    return bool(re.fullmatch(r"\s*(?:UNKNOWN|UNDETERMINED|CANNOT DETERMINE|NOT ENOUGH INFORMATION|INSUFFICIENT INFORMATION|I DON'T KNOW|NONE|N/?A)[\s.!?]*",str(x),re.I))
def present_set(cond):return set("ABC") if cond=="ABC_CF" else set() if cond=="NONE" else set(cond)
def accepted(gold):return {norm_ans(g) for g in [gold]+ALIASES.get(gold,[])}
def expected_for(spec,cond):
    """gold answer expected for this condition, or None when the memory does not contain a sufficient cartridge set"""
    if spec is None:return "UNSCORED"
    p=present_set(cond)
    if not any(set(r)<=p for r in spec["req"]):return None
    return spec.get("cf_gold") if (cond=="ABC_CF" and spec.get("cf_gold")) else spec["gold"]
def grade(raw,spec,cond,scored=True):
    """TEST677/TEST686 grading rule (CORRECT_KNOWN / CORRECT_ABSTENTION / UNSUPPORTED / MISSED_KNOWN / WRONG_KNOWN)."""
    exp=expected_for(spec,cond)
    if spec is None or not scored:return dict(status="UNSCORED",expected=None,contains_expected=False,equals_full_memory_answer=False)
    full=spec["gold"];r=norm_ans(raw)
    eq_full=bool(r) and r in accepted(full)
    if exp is None:
        st="CORRECT_ABSTENTION" if is_unknown(raw) else "UNSUPPORTED"
        return dict(status=st,expected="UNKNOWN",contains_expected=False,equals_full_memory_answer=eq_full)
    if is_unknown(raw):st="MISSED_KNOWN"
    elif r in accepted(exp):st="CORRECT_KNOWN"
    else:st="WRONG_KNOWN"
    return dict(status=st,expected=exp,contains_expected=bool(norm_ans(exp)) and norm_ans(exp) in r,equals_full_memory_answer=eq_full)

def utc_now():return datetime.now(timezone.utc).isoformat(timespec="milliseconds")
def local_now():return datetime.now().astimezone().isoformat(timespec="seconds")
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()
def jsafe(o):
    if isinstance(o,dict):return {str(k):jsafe(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)):return [jsafe(v) for v in o]
    if isinstance(o,(np.floating,)):return float(o)
    if isinstance(o,(np.integer,)):return int(o)
    if isinstance(o,np.ndarray):return jsafe(o.tolist())
    if isinstance(o,Path):return str(o)
    if isinstance(o,float) and (math.isnan(o) or math.isinf(o)):return None
    return o
def dump_json(path,obj):
    Path(path).write_text(json.dumps(jsafe(obj),ensure_ascii=False,indent=2),encoding="utf-8");return Path(path)
def say(*a):print(*a,flush=True)

ROOT=Path("/content/AKBASCORE_MAM_v1_4_MISTRAL_DEMO") if os.path.isdir("/content") else Path("/tmp/AKBASCORE_MAM_v1_4_MISTRAL_DEMO")
ENGINE_RUNS=ROOT/"engine_runs_all";ENGINE_RUNS.mkdir(parents=True,exist_ok=True)
ROOT.mkdir(parents=True,exist_ok=True)


# =====================================================================================================================
# THE MISTRAL CUT6 ENGINE — locked TEST684 bootstrap (TEST560 + TEST659 + TEST677) executed UNCHANGED up to the
# TEST686 boundary, plus the TEST686 scenario functions extracted verbatim. Nothing here rewrites engine behaviour.
# =====================================================================================================================
import ast,gc,urllib.request
E={"__name__":"akbascore_mistral_cut6_engine","__file__":"TEST684_VERIFIED_MISTRAL_BOOTSTRAP.py"}
STARTUP=dict(started_utc=utc_now(),started_local=local_now())
SOURCES={}
FULL_WEIGHT_AT_START=os.environ.get("AKB14M_FULL_WEIGHT_SHA","1")!="0"
ENGINE_LOCK=threading.RLock()
TEXT_IDS={}
TEST686_ROWS={};TEST686_CHAINS={}   # sealed TEST686 raw answers, parsed from the SHA-256-verified 686.log (comparison only)

def git_blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def gate(name,ok):
    say(("PASS " if ok else "FAIL ")+name)
    if not ok:raise RuntimeError("GATE FAILED: "+name)
def fetch_source(name):
    with urllib.request.urlopen(urllib.request.Request(RAW_BASE+name,headers={"User-Agent":"AKBASCORE-MISTRAL-CUT6-DEMO"}),timeout=180) as f:raw=f.read()
    SOURCES[name]=dict(bytes=len(raw),git_blob=git_blob(raw),sha256=sha_bytes(raw),url=RAW_BASE+name);return raw

def full_weight_sha(model):
    """SHA-256 over (name, shape, dtype, raw bytes) of every parameter tensor (same method as TEST575)."""
    h=hashlib.sha256()
    with torch.inference_mode():
        for name,p in model.named_parameters():
            h.update(name.encode());h.update(str(tuple(p.shape)).encode());h.update(str(p.dtype).encode())
            for part in p.detach().contiguous().view(torch.uint8).reshape(-1).split(16*1024*1024):h.update(part.cpu().numpy().tobytes())
    return h.hexdigest()
def param_guard(model):
    """all-parameter guard: SHA-256 over (name, shape, dtype, sum, |sum|, sum of squares) of every parameter tensor."""
    h=hashlib.sha256()
    with torch.inference_mode():
        for name,p in model.named_parameters():
            x=p.detach().float();vals=(float(x.sum().item()),float(x.abs().sum().item()),float((x*x).sum().item()))
            h.update(name.encode());h.update(str(tuple(p.shape)).encode());h.update(str(p.dtype).encode());h.update(np.asarray(vals,dtype=np.float64).tobytes());del x
    torch.cuda.empty_cache();return h.hexdigest()
def residual_hooks(model):
    out=[]
    for li,layer in enumerate(model.model.layers):
        for label,module in (("layer",layer),("attention",layer.self_attn)):
            if module._forward_hooks or module._forward_pre_hooks:out.append(f"L{li}:{label}")
    if model._forward_hooks or model._forward_pre_hooks:out.append("causal_lm")
    return out
def frozen_state():
    m=E["model"]
    return dict(training=bool(m.training),trainable_tensors=sum(int(p.requires_grad) for p in m.parameters()),
                lora=bool(hasattr(m,"peft_config") or any("lora" in n.lower() for n,_ in m.named_modules())),
                residual_hooks=residual_hooks(m),sentinel=E["sentinel"](),sentinel_equals_load=E["sentinel"]()==E["S0"])

def _assignment(tree,name):
    nodes=[n for n in tree.body if isinstance(n,(ast.Assign,ast.AnnAssign)) and any(isinstance(t,ast.Name) and t.id==name for t in (n.targets if isinstance(n,ast.Assign) else [n.target]))]
    gate("V14_PROTOCOL_FIELD_"+name,len(nodes)==1);return nodes[0].value
def _safe_dict_eval(node):
    """same restricted evaluation as TEST686 metadata686: literals and dict(...) only"""
    try:return ast.literal_eval(node)
    except (ValueError,TypeError):
        allowed=(ast.Expression,ast.Dict,ast.List,ast.Tuple,ast.Constant,ast.Call,ast.keyword,ast.Load,ast.Name,ast.UnaryOp,ast.USub)
        for n in ast.walk(node):
            if not isinstance(n,allowed):raise RuntimeError("UNSAFE_METADATA_NODE_"+type(n).__name__)
            if isinstance(n,ast.Call) and (not isinstance(n.func,ast.Name) or n.func.id!="dict"):raise RuntimeError("UNSAFE_METADATA_CALL")
            if isinstance(n,ast.Name) and n.id!="dict":raise RuntimeError("UNSAFE_METADATA_NAME")
        return eval(compile(ast.Expression(node),"V14_METADATA.py","eval"),{"__builtins__":{},"dict":dict},{})

def register_text(text):
    """registers a fact with the engine's own register678 (TEST560 source formatting + canonical prefix check), once per text"""
    key=sha_bytes(text.encode("utf-8"))
    if key not in TEXT_IDS:TEXT_IDS[key]=E["register678"](text)
    return TEXT_IDS[key]
def letters(cond):
    if cond not in CONDITIONS:raise ValueError("Invalid condition: "+str(cond))
    return "" if cond=="NONE" else "ABC" if cond=="ABC_CF" else cond
def slot_text(scn,slot,cond):
    return E["MISTRAL_EDITED"][scn]["C_CF" if (cond=="ABC_CF" and slot=="C") else slot]
def scenario_edited(scn):
    a=E["MISTRAL_EDITED"][scn];b=E["MISTRAL_ORIGINAL"][scn]
    return any(a[s]!=b[s] for s in ("A","B","C","C_CF"))
def scenario_texts(scn):d=E["MISTRAL_EDITED"][scn];return {s:d[s] for s in ("A","B","C","C_CF")}
def set_cartridge(scn,slot,text):
    with ENGINE_LOCK:
        if scn not in E["MISTRAL_EDITED"] or slot not in ("A","B","C","C_CF"):raise ValueError("Invalid scenario or cartridge")
        if not isinstance(text,str) or not text.strip() or len(text)>4000:raise ValueError("Cartridge must contain 1–4000 characters")
        E["MISTRAL_EDITED"][scn][slot]=text.strip();E["CASES686"][scn][slot]=register_text(text.strip())   # a NEW cartridge is forged at the next build
def reset_scenario(scn):
    with ENGINE_LOCK:
        E["MISTRAL_EDITED"][scn]=dict(E["MISTRAL_ORIGINAL"][scn])
        E["CASES686"][scn]={slot:register_text(E["MISTRAL_ORIGINAL"][scn][slot]) for slot in ("A","B","C","C_CF")}

def boot_engine():
    t=time.perf_counter()
    b684=fetch_source("684.py");b686=fetch_source("686.py");p1=fetch_source("HIPPOCAMPUS_1.4_part1.py")
    gate("TEST684_LOCKED_BLOB",SOURCES["684.py"]["git_blob"]==LOCKS["test684_blob"])
    gate("TEST686_LOCKED_BLOB",SOURCES["686.py"]["git_blob"]==LOCKS["test686_blob"])
    gate("V14_PROTOCOL_SHA256",SOURCES["HIPPOCAMPUS_1.4_part1.py"]["sha256"]==LOCKS["v14_part1_sha256"])
    s684=b684.decode("utf-8");s686=b686.decode("utf-8")
    gate("TEST684_BOOTSTRAP_BOUNDARY",s684.count(TEST684_MARKER)==1)
    # ---- the locked bootstrap, exactly as TEST686 executes it (TEST560 engine, TEST659 CUDA kernel, gates) ----
    exec(compile(s684.split(TEST684_MARKER,1)[0],"TEST684_VERIFIED_MISTRAL_BOOTSTRAP.py","exec"),E)
    torch.cuda.synchronize()
    arch=(E["NL"],E["H"],E["QH"],E["KVH"],E["HD"])
    gate("MISTRAL_ARCH_32_4096_32_8_128",tuple(arch)==ARCH_EXPECTED)
    gate("CUT6_BOUNDARY",int(E["CUT"])==CUT)
    gate("TEST560_BLOB_IN_BOOTSTRAP",E["SHA560"]==LOCKS["test560_blob"])
    gate("TEST659_BLOB_IN_BOOTSTRAP",E["SHA659"]==LOCKS["test659_blob"])
    gate("TEST677_BLOB_IN_BOOTSTRAP",E["SHA677"]==LOCKS["test677_blob"])
    gate("MODEL_ID",E["MODEL_ID"]==MODEL_ID)
    # ---- Qwen v1.4 protocol read AS DATA (same extraction as TEST686); its Qwen engine is never executed ----
    tree=ast.parse(p1.decode("utf-8"))
    inner=ast.parse(ast.literal_eval(_assignment(tree,"V14_SOURCE")))
    scen=ast.literal_eval(_assignment(inner,"MAM14_SCENARIOS"));conds=ast.literal_eval(_assignment(inner,"MAM14_CONDITIONS"))
    scoring=_safe_dict_eval(_assignment(tree,"SCORING"));aliases=_safe_dict_eval(_assignment(tree,"ALIASES"))
    gate("V14_SCENARIOS",set(scen)=={"AKBASCORE","MATRIX"})
    gate("V14_NINE_CONDITIONS",tuple(conds)==CONDITIONS)
    gate("V14_SCORING_IDENTICAL_TO_THIS_PROGRAM",scoring==SCORING and aliases==ALIASES)
    # ---- TEST686 functions, verbatim from the blob-verified source ----
    t686=ast.parse(s686);nodes=[n for n in t686.body if isinstance(n,ast.FunctionDef) and n.name in TEST686_FUNCTIONS]
    gate("TEST686_FUNCTIONS_FOUND",sorted(n.name for n in nodes)==sorted(TEST686_FUNCTIONS))
    exec(compile(ast.Module(body=nodes,type_ignores=[]),"TEST686_LOCKED_FUNCTIONS.py","exec"),E)
    # ---- TEST684 two-tier descriptive audit (secondary; never replaces the strict score) ----
    t684=ast.parse(s684);anodes=[]
    for n in t684.body:
        if isinstance(n,ast.FunctionDef) and n.name in TEST684_AUDIT_NAMES:anodes.append(n)
        elif isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in TEST684_AUDIT_NAMES:anodes.append(n)
    gate("TEST684_DESCRIPTIVE_AUDIT_FOUND",len(anodes)==len(TEST684_AUDIT_NAMES))
    E["unicodedata"]=unicodedata
    exec(compile(ast.Module(body=anodes,type_ignores=[]),"TEST684_DESCRIPTIVE_AUDIT.py","exec"),E)
    # ---- scenario state used by the TEST686 functions ----
    E["SCENARIOS686"]=copy.deepcopy(scen);E["SCORING686"]=scoring;E["ALIASES686"]=aliases
    E["MISTRAL_ORIGINAL"]={k:dict(v) for k,v in scen.items()};E["MISTRAL_EDITED"]={k:dict(v) for k,v in scen.items()};E["CASES686"]={}
    for name in scen:E["CASES686"][name]={slot:register_text(scen[name][slot]) for slot in ("A","B","C","C_CF")}
    for name in scen:
        keys=E["keys686"](name,"ABC");a=E["memory678"](keys,"DC_CUT6_NATIVE");b=E["memory678"](keys,"DC_CUT6_REFERENCE")
        gate("NATIVE_REFERENCE_BITWISE_"+name,all(torch.equal(x,y) and torch.equal(z,w) for (x,z),(y,w) in zip(a,b)));del a,b
    gc.collect();torch.cuda.empty_cache()
    STARTUP["engine_seconds"]=round(time.perf_counter()-t,2)
    import transformers
    m=E["model"];c=m.config
    STARTUP.update(model_id=E["MODEL_ID"],arch=list(arch),dtype=str(next(m.parameters()).dtype).replace("torch.",""),
        attn=getattr(c,"_attn_implementation",None),max_new=int(E["MAX_NEW"]),prefix_tokens=int(E["P"]),system_prompt=E["SYSTEM"],
        cut=int(E["CUT"]),gpu=torch.cuda.get_device_name(0),gpu_total_gib=round(torch.cuda.get_device_properties(0).total_memory/2**30,2),
        torch=torch.__version__,transformers=transformers.__version__,gradio=gr.__version__,python=sys.version.split()[0],platform=platform.platform(),
        params=int(sum(p.numel() for p in m.parameters())),sources={k:dict(v) for k,v in SOURCES.items()},locks=dict(LOCKS),
        rope=str(getattr(c,"rope_parameters",None) or getattr(c,"rope_theta",None)),
        native_kernel="TEST659 append_kv: BF16 element copy that concatenates K/V rows (bitwise = torch.cat; gates NATIVE_BITWISE_*)",
        engine_functions="TEST560 forge_checkpoint / init_incremental / append_incremental (lower-layer concatenation → native_splice678) / answer_layers",
        sentinel_load=E["S0"],sentinel_start=E["sentinel"]())
    say("[measure] all-parameter guard …");STARTUP["guard_start"]=param_guard(m)
    if FULL_WEIGHT_AT_START:
        say("[measure] full-weight SHA-256 (about 1–2 minutes) …");t=time.perf_counter()
        STARTUP["full_weight_sha256"]=full_weight_sha(m);STARTUP["full_weight_seconds"]=round(time.perf_counter()-t,1)
        say(f"[measure] full-weight SHA-256 {STARTUP['full_weight_sha256']} (recorded; no published Mistral reference exists)")
    else:STARTUP["full_weight_sha256"]=None
    STARTUP["full_weight_equals_reference"]=None
    STARTUP["frozen"]=frozen_state();STARTUP["finished_utc"]=utc_now()
    STARTUP["test686_log_verified"]=verify_686_log()
    say(f"[engine] READY · {STARTUP['gpu']} · torch {STARTUP['torch']} · transformers {STARTUP['transformers']} · gradio {STARTUP['gradio']}")

def verify_686_log():
    """checks that the sealed TEST686 summary used in the figures comes from the published 686.log (SHA-256)"""
    try:
        raw=fetch_source("686.log");txt=raw.decode("utf-8","replace")
        ok=SOURCES["686.log"]["sha256"]==LOCKS["test686_log_sha256"] and "TEST686 EXPERIMENT_COMPLETE" in txt
        if ok:
            for line in txt.splitlines():
                m=re.match(r"ANSWER (\S+) (\S+) (\S+) (\S+) (\S+) (.*)$",line)
                if m:TEST686_ROWS[m.group(1,2,3,4)]=dict(status=m.group(5),answer=ast.literal_eval(m.group(6)));continue
                m=re.match(r"STAGED (\S+) (\S+) (\S+) (\S+) (.*)$",line)
                if m:TEST686_CHAINS[m.group(1,2,3)]=dict(status=m.group(4),answer=ast.literal_eval(m.group(5)))
        return dict(checked=True,sha256=SOURCES["686.log"]["sha256"],matches=ok,rows=len(TEST686_ROWS),chains=len(TEST686_CHAINS))
    except Exception as ex:
        return dict(checked=False,error=f"{type(ex).__name__}: {ex}",matches=None)

def mistral_run_demo(scenario,condition,representation,question=None,include_staged=True):
    """One engine run, exactly the TEST686 per-condition procedure: memory678 → answer_layers for every question →
    staged686. Raw strings are stored as produced; nothing is substituted."""
    with ENGINE_LOCK:
        if scenario not in E["MISTRAL_EDITED"]:raise ValueError("Unknown scenario")
        if representation not in REPRESENTATIONS:raise ValueError("Unknown representation")
        if question is not None and (not isinstance(question,str) or not question.strip() or len(question)>2000):raise ValueError("Question must contain 1–2000 characters")
        keys=E["keys686"](scenario,condition);started=local_now();t0=time.perf_counter();mem=None
        try:
            mem=E["memory678"](keys,representation);rows=int(mem[0][0].shape[-2])
            queries=[("CUSTOM",question)] if question else list(E["SCENARIOS686"][scenario]["queries"])
            responses=[]
            for qid,q in queries:
                t=time.perf_counter();raw=E["answer_layers"](mem,q)
                responses.append(dict(question_id=qid,question=q,answer=raw,elapsed_seconds=round(time.perf_counter()-t,4),unknown=E["unknown686"](raw)))
            staged=None
            if include_staged:
                t=time.perf_counter();staged=E["staged686"](mem,scenario,condition);staged["elapsed_seconds"]=round(time.perf_counter()-t,4)
            frozen=all(not p.requires_grad for p in E["model"].parameters());sent=E["sentinel"]()==E["S0"]
            if not (frozen and sent):raise RuntimeError("POST_RUN_FROZEN_OR_SENTINEL_FAILED")
            result=dict(title=APP_SHORT,timestamp=started,scenario=scenario,condition=condition,representation=representation,model=E["MODEL_ID"],
                        cut=int(E["CUT"]),cartridges_used=list(letters(condition)),keys=[int(k) for k in keys],memory_rows=rows,
                        cartridge_texts={s:slot_text(scenario,s,condition) for s in letters(condition)},responses=responses,staged_chain=staged,
                        weights_frozen=frozen,sentinel_unchanged=sent,max_new_tokens=int(E["MAX_NEW"]),
                        engine_sources={k:SOURCES[k]["git_blob"] for k in ("684.py","686.py")},protocol_sha256=SOURCES["HIPPOCAMPUS_1.4_part1.py"]["sha256"],
                        note="Raw Mistral outputs. TEST686 procedure. External three-step chain. Strict scoring separate from descriptive audit.",
                        elapsed_seconds=round(time.perf_counter()-t0,3))
            result["run_sha256"]=sha_bytes(json.dumps(result,ensure_ascii=False,sort_keys=True,default=str).encode("utf-8"))
            path=ENGINE_RUNS/f"RUN_{scenario}_{condition}_{representation}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
            path.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str),encoding="utf-8");result["saved_to"]=str(path)
            return result
        finally:
            del mem;gc.collect();torch.cuda.empty_cache()
