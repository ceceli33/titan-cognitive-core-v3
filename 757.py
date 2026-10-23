# AKBASCORE SILICON HIPPOCAMPUS — TEST753
# One-cell Colab execution. Frozen Qwen2.5-72B NF4, A100 80GB.
# Direct numerical CUT3 multi-cartridge fusion; NO text-mediated synthesis.
# Source engine: locked TEST730 + locked TEST709 + TEST716.
# NOT GPU executed by author. Run produces its own measured log/JSON.
import ast, hashlib, json, os, time, traceback, urllib.request, gc, re, random
from pathlib import Path

REPO="https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/"
LOCK730="b1bad9eb3b111b44413f8ef05a3a140ab66a77dd"
LOCK709="6c9f8cbb1eeed848d45133d73f0d7676b68e9125"
LOCK716="913fa7a4951f2072df4be2eb49120ea86efa5477"
def fetch_locked(name,expected):
    with urllib.request.urlopen(urllib.request.Request(REPO+name,headers={"User-Agent":"AKBASCORE-TEST753"}),timeout=120) as f:
        raw=f.read(400000)
    blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    if blob!=expected: raise RuntimeError(f"LOCK_FAILURE {name}: {blob} != {expected}")
    return raw

# Import definitions of the validated TEST730 motor WITHOUT executing TEST730's experiment.
raw730=fetch_locked("730.py",LOCK730)
raw709=fetch_locked("709.py",LOCK709)
raw716=fetch_locked("716.py",LOCK716)
source730=raw730.decode("utf-8")
marker="\ntry:\n log('='*110)"
if marker not in source730: raise RuntimeError("TEST730_EXECUTION_BOUNDARY_CHANGED")
prefix=source730.split(marker,1)[0]
exec(compile(prefix,"730_reference_definitions.py","exec"),globals())
# The original TEST730 prefix imports and defines its motor but does not load the model.
TEST="757"
ROOT=Path("/content/AKBASCORE_TEST757" if Path("/content").exists() else "/tmp/AKBASCORE_TEST757")
PREVIOUS_ROOT=Path("/content/AKBASCORE_TEST754" if Path("/content").exists() else "/tmp/AKBASCORE_TEST754")
FALLBACK_ROOT=Path("/content/AKBASCORE_TEST753" if Path("/content").exists() else "/tmp/AKBASCORE_TEST753")
ROOT.mkdir(parents=True,exist_ok=True)
LOG=ROOT/"TEST757.log";LOG.write_text("")
OUT=ROOT/"TEST757_results.json"
CART_DIR=ROOT/"physical_cartridges";CART_DIR.mkdir(exist_ok=True)
EVIDENCE_DIR=ROOT/"sealed_sources";EVIDENCE_DIR.mkdir(exist_ok=True)
MANIFEST=ROOT/"TEST757_manifest.json"
R={"test":TEST,"status":"STARTED","checks":[],"trials":[],
   "source_blobs":{"730":LOCK730,"709":LOCK709,"716":LOCK716},
   "method":"H3 numerical addressing + direct native CUT3 append fusion; no intermediary model-generated synthesis",
   "limitations":["GPU result not known before running",
                  "Native append consolidation is not equivalent to arbitrary algebraic tensor fusion",
                  "Retrieval quality and semantic accuracy are independent of tensor-integrity checks",
                  "Potential pretraining knowledge requires no-memory and source-ablation controls",
                  "Ground-truth grading of open-ended scientific answers requires independent review"]}
MAX_NEW=48
CHUNK=128
GPU_RESERVE_GIB=9.0
MAX_SOURCE_TOKENS=3000
PIECE_TOKENS=650
MAX_PIECES_PER_SOURCE=5
TOP_K=5
MAX_FUSED_TOKENS=11000
SEED=753
random.seed(SEED)
# The six TEST730 questions are frozen before source acquisition.
# Synthetic holdout panel is generated below and replaces TEST730's real-paper questions.
QUESTION_SET=[]

PANEL_BYTES=json.dumps(QUESTION_SET,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
PANEL_SHA=hashlib.sha256(PANEL_BYTES).hexdigest()
(ROOT/"SEALED_QUESTIONS.json").write_bytes(PANEL_BYTES)
R["panel_sha256"]=PANEL_SHA
save()
# All engine definitions and original source-retrieval functions come from TEST730.
# Import locked TEST709 native memory operators, preserving its exact source.
import_reference(raw709)
# Append must use TEST730's DirectCut3, not TEST709's hook.
@torch.no_grad()
def native_append_direct(memory,cp,strict_sha=True):
    if not isinstance(memory,list) or len(memory)!=NL or any(x is None for x in memory):
        raise RuntimeError("OWNED_80_LAYER_MEMORY_REQUIRED")
    oldn=int(memory[0][0].shape[-2])
    q=int(cp["n"]-P)
    if q<=0: raise RuntimeError("EMPTY_APPEND")
    body=cp["h"][:,P:,:]
    # Exact prior-row seals before handing cache ownership to DynamicCache.
    seals=full_kv_seal(memory) if strict_sha else None
    old_lower=tuple(memory[:CUT+1])
    upper=cache_build(memory)
    for i in range(NL): memory[i]=None
    gc.collect()
    with DirectCut3(model.model.layers[CUT],"inject",source=body) as bridge:
        for st in range(0,q,CHUNK):
            m=min(CHUNK,q-st)
            ensure_room(m+512)
            bridge.offset=st
            pos=torch.arange(oldn+st,oldn+st+m,device=DEV)
            out=model(inputs_embeds=torch.zeros((1,m,H),device=DEV,dtype=DTYPE),
                      past_key_values=upper,
                      attention_mask=torch.ones((1,oldn+st+m),device=DEV,dtype=torch.long),
                      position_ids=pos.unsqueeze(0),cache_position=pos,
                      use_cache=True,return_dict=True)
            upper=out.past_key_values
            del out
    grown=list(pairs(upper))
    # Preserve the exact prior lower-layer rows. Rephase incoming keys for
    # their new absolute positions. Values are invariant to RoPE rephasing.
    for i in range(CUT+1):
        ok,ov=old_lower[i]
        k,v=cp["lower"][i]
        shifted=[]
        for st in range(0,q,CHUNK):
            end=min(q,st+CHUNK)
            oldpos=torch.arange(P+st,P+end,device=DEV)
            newpos=torch.arange(oldn+st,oldn+end,device=DEV)
            shifted.append(rephase(k[:,:,P+st:P+end,:],oldpos,newpos))
        grown[i]=(torch.cat([ok]+shifted,dim=-2),
                  torch.cat((ov,v[:,:,P:,:]),dim=-2))
    if strict_sha:
        for i,((nk,nv),(kh,vh)) in enumerate(zip(grown,seals)):
            if kv_digest(nk[:,:,:oldn,:])!=kh or kv_digest(nv[:,:,:oldn,:])!=vh:
                raise RuntimeError(f"PRIOR_MEMORY_CHANGED_LAYER_{i}")
    if len(grown)!=NL: raise RuntimeError("FUSED_LAYER_COUNT")
    del upper,old_lower
    return grown

def load_verified(cid):
    entry=entries[cid]
    t=time.perf_counter()
    cp=safe_load(entry)  # verifies file SHA, cartridge ID, and all H3/KV tensor SHA
    disk_ms=(time.perf_counter()-t)*1000
    t=time.perf_counter()
    g=to_gpu(cp)
    torch.cuda.synchronize()
    h2d_ms=(time.perf_counter()-t)*1000
    del cp
    return g,{"ssd_verify_ms":round(disk_ms,3),"h2d_ms":round(h2d_ms,3)}

def build_fusion(ids,label,strict_sha=True):
    t0=time.perf_counter()
    mem=None;steps=[];active=[];total_tokens=0
    try:
        for cid in ids:
            tokens=entries[cid]["body_tokens"]
            if total_tokens+tokens+(P if mem is None else 0)>MAX_FUSED_TOKENS:
                log("SKIP_TOKEN_BUDGET",label,cid)
                continue
            cp,metrics=load_verified(cid)
            t=time.perf_counter()
            if mem is None:
                new=list(initialize_native(cp))
            else:
                new=native_append_direct(mem,cp,strict_sha=strict_sha)
            mem=new
            del cp
            torch.cuda.synchronize()
            metrics["fusion_ms"]=round((time.perf_counter()-t)*1000,3)
            metrics["cid"]=cid
            metrics["memory_tokens"]=int(mem[0][0].shape[-2])
            steps.append(metrics);active.append(cid)
            total_tokens+=tokens
            log("NATIVE_FUSION_STEP",label,cid,metrics)
        if mem is None:raise RuntimeError("NO_MEMORY_SELECTED")
        return mem,active,steps,round(time.perf_counter()-t0,3)
    except:
        del mem
        release()
        raise

def answer_fused(mem,question):
    # The only question prompt is for ANSWERING AFTER numerical fusion.
    # No reflection, text concatenation, textual intermediary, or MASTER rewriting.
    return answer(mem,question)

def run_arm(name,ids,questions,strict_sha=True):
    t0=time.perf_counter()
    mem,active,steps,build_s=build_fusion(ids,name,strict_sha)
    try:
        seal_before=memory_seals(mem)
        rows=[]
        for q in questions:
            t=time.perf_counter()
            raw=answer_fused(mem,q["question"])
            rows.append({"id":q["id"],"question":q["question"],
                         "raw":raw,"answer_ms":round((time.perf_counter()-t)*1000,3),
                         "raw_sha256":sha(raw.encode())})
            log("FUSION_ANSWER",name,q["id"],repr(raw))
        check("MEMORY_UNCHANGED_AFTER_QA_"+name,
              compare_seals(seal_before,memory_seals(mem)))
        record={"arm":name,"active":active,"steps":steps,"build_s":build_s,
                "total_s":round(time.perf_counter()-t0,3),"answers":rows,
                "semantics":"UNSCORED_PENDING_INDEPENDENT_REVIEW"}
        R["trials"].append(record);save()
        return record
    finally:
        del mem
        release()

def source_parts(body,pid):
    ids=tok(body,add_special_tokens=False).input_ids[:MAX_SOURCE_TOKENS]
    chunks=[ids[i:i+PIECE_TOKENS] for i in range(0,len(ids),PIECE_TOKENS)]
    if len(chunks)>MAX_PIECES_PER_SOURCE:
        raise RuntimeError("TOO_MANY_PARTS_"+pid)
    return chunks

import numpy as np
from collections import Counter
MODEL_SEED=7562026
NUM_CHAINS=4
ROUTE_K=3
MAX_FUSED_TOKENS=3500
SAMPLE_PER_PIECE=512
# Reproducible synthetic facts. Answer values are random-looking labels,
# unrelated to pretrained public facts.
rng=random.Random(MODEL_SEED)
ALPHABET="ABCDEFGHJKLMNPQRSTUVWXYZ"
def opaque(prefix,n=8):
    return prefix+"-"+''.join(rng.choice(ALPHABET) for _ in range(n))
def normalized(x):
    return np.asarray(x,dtype=np.float32)/np.maximum(
        np.linalg.norm(np.asarray(x,dtype=np.float32),axis=-1,keepdims=True),1e-8)
def exact_value(response):
    # Exact matching, with no substring credit. Permits surrounding punctuation.
    a=response.strip().splitlines()[0] if response.strip() else ""
    a=re.sub(r"^(?:answer\s*:\s*)","",a,flags=re.I).strip()
    return a.strip(" `.'\";:").upper()
def synthetic_panel():
    cases=[];cards={}
    for i in range(NUM_CHAINS):
        person=opaque("PERSON");work=opaque("WORK");team=opaque("TEAM");vault=opaque("VAULT")
        # Independent physical pieces. Every piece contains one relation only.
        a=f"{person} works_at {work}."
        b=f"{work} collaborates_with {team}."
        c=f"{team} archives_in {vault}."
        ids=[f"C{i:02d}_A",f"C{i:02d}_B",f"C{i:02d}_C"]
        for cid,txt in zip(ids,(a,b,c)):cards[cid]=txt
        cases.append({"id":f"Q{i:02d}","person":person,"work":work,"team":team,
                      "answer":vault,"supports":ids,
                      "question":f"Starting from {person}, follow works_at, then collaborates_with, then archives_in. What is the final VAULT code? Reply with only the exact VAULT code, or UNKNOWN if evidence is insufficient."})
    return cases,cards
CASES,CARD_TEXT=synthetic_panel()
# Include two impossible questions, which should return UNKNOWN.
for j in range(2):
    ghost=opaque("PERSON")
    CASES.append({"id":f"M{j:02d}","person":ghost,"work":None,"team":None,
                  "answer":"UNKNOWN","supports":[],
                  "question":f"Starting from {ghost}, follow works_at, then collaborates_with, then archives_in. What is the final VAULT code? Reply with only the exact VAULT code, or UNKNOWN if evidence is insufficient."})
QUESTION_SET=[{"id":c["id"],"level":"THREE_HOP" if c["supports"] else "MISSING",
               "question":c["question"]} for c in CASES]
PANEL_BYTES=json.dumps({"cases":CASES,"cards":CARD_TEXT},sort_keys=True,ensure_ascii=False).encode()
PANEL_SHA=sha(PANEL_BYTES)
(ROOT/"SEALED_PANEL.json").write_bytes(PANEL_BYTES)
R["panel_sha256"]=PANEL_SHA
R["research_goal"]="3-hop exact relational recall from unknown facts; no textual memory at answer time"
R["ground_truth_scoring"]="EXACT"
save()

@torch.no_grad()
def query_native(question):
    s="<|im_start|>user\n"+question+"\n<|im_end|>\n<|im_start|>assistant\n"
    ids=tok(s,add_special_tokens=False).input_ids
    captures=[]
    with DirectCut3(model.model.layers[CUT],"capture",collector=captures):
        out=model(input_ids=torch.tensor([ids],device=DEV),use_cache=False,return_dict=True)
        del out
    return normalized(torch.cat(captures,dim=1)[0].float().cpu().numpy())

def numeric_rank(question,bank):
    q=query_native(question)
    result={}
    for cid,b in bank.items():
        sim=q@b
        k=min(2,sim.shape[1])
        top=np.partition(sim,-k,axis=1)[:,-k:]
        result[cid]=float(top.mean(axis=1).mean())
    return sorted(result,key=lambda cid:(-result[cid],cid)),result

def make_cartridges():
    global entries,ledger
    entries={}
    ledger={"test":TEST,"model":MODEL_ID,"cut":CUT,"panel_sha256":PANEL_SHA,
            "cartridges":[],"source_blobs":R["source_blobs"]}
    for cid,body in sorted(CARD_TEXT.items()):
        # Source facts are independent and never joined into a single cartridge.
        ids=tok(body,add_special_tokens=False).input_ids
        cp,secs=forge_native(ids,cid)
        path=CART_DIR/(cid+".pt")
        temp=Path(str(path)+".tmp")
        torch.save(cp,temp);temp.replace(path)
        e={"id":cid,"file":path.name,"sha256":sha_file(path),
           "tensor_sha":seal_cp(cp),"body_tokens":len(ids),
           "body_sha256":sha(body.encode()),"forge_seconds":secs}
        entries[cid]=e
        ledger["cartridges"].append(e)
        atomic_json(MANIFEST,ledger)
        log("SEALED_NATIVE_CARTRIDGE",cid,e["sha256"])
        del cp;release()
    check("ALL_CARTRIDGES",len(entries)==NUM_CHAINS*3)

def build_bank():
    bank={}
    for cid in entries:
        cp=safe_load(entries[cid])
        x=cp["h"][0,P:,:].float().cpu().numpy()
        ix=np.linspace(0,len(x)-1,min(SAMPLE_PER_PIECE,len(x)),dtype=np.int64)
        bank[cid]=normalized(x[ix]).T.copy()
        del cp
    return bank

def scored_arm(name,ids,cases,expected):
    t=time.perf_counter()
    if ids:
        result=run_arm(name,ids,[{"id":c["id"],"question":c["question"]} for c in cases],strict_sha=True)
        answers={a["id"]:a["raw"] for a in result["answers"]}
    else:
        answers={c["id"]:answer(None,c["question"]) for c in cases}
    grades=[]
    for c in cases:
        raw=answers[c["id"]]
        prediction=exact_value(raw)
        ok=prediction==expected[c["id"]]
        row={"arm":name,"qid":c["id"],"selected":ids,"pred":prediction,
             "gold":expected[c["id"]],"correct":ok,"raw":raw}
        grades.append(row)
        log("SCORED",name,c["id"],"PASS" if ok else "FAIL","PRED",repr(prediction),
            "GOLD",repr(expected[c["id"]]))
    R.setdefault("scored",[]).extend(grades)
    save()
    return grades

def model_setup():
    global tok,PREFIX,PIDS,P,model,NL,H,QH,KVH,HD
    tok=AutoTokenizer.from_pretrained(MODEL_ID,trust_remote_code=False)
    PREFIX=('<|im_start|>system\n'
            'Use only the available document memory for document-specific questions. '
            'If evidence is missing, say UNKNOWN.\n'
            '<|im_end|>\n<|im_start|>user\nINFORMATION:\n')
    PIDS=tok(PREFIX,add_special_tokens=False).input_ids
    P=len(PIDS)
    quant=BitsAndBytesConfig(load_in_4bit=True,bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=DTYPE,bnb_4bit_use_double_quant=True)
    model=AutoModelForCausalLM.from_pretrained(
        MODEL_ID,quantization_config=quant,dtype=DTYPE,device_map={"":0},
        low_cpu_mem_usage=True,trust_remote_code=False,attn_implementation="sdpa").eval()
    for par in model.parameters():par.requires_grad_(False)
    cfg=model.config
    NL=len(model.model.layers);H=int(cfg.hidden_size)
    QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads)
    HD=int(getattr(cfg,"head_dim",None) or H//QH)
    check("MODEL_ARCH",(NL,H,QH,KVH,HD)==EXPECTED,(NL,H,QH,KVH,HD))
    check("FROZEN",all(not par.requires_grad for par in model.parameters()))
    check("NF4",any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))

# TEST757 — autonomous three-hop memory traversal.
# At each step the NEXT query key is the MODEL'S previous output, never the gold key.
# Frozen model; sealed physical cards; no direct access to CARD_TEXT in inference.
STEPS=("works_at","collaborates_with","archives_in")
KINDS=("PERSON","WORK","TEAM","VAULT")
ROUTE_K=3
MAX_NEW=48
def step_question(key,relation,kind):
    return (f"Using the available document memory, find the one fact where {key} "
            f"is the subject of relation {relation}. Return ONLY its exact {kind} code. "
            "If the fact is absent, return UNKNOWN.")
def read_exact(raw,kind):
    pred=exact_value(raw)
    if pred=="UNKNOWN":return pred
    # Syntax-only gate. No comparison with gold, no list of valid answers.
    return pred if re.fullmatch(re.escape(kind)+r"-[A-Z]{8}",pred) else "INVALID"

def traversal(label,case,mode,bank=None,allow_oracle=False):
    current=case["person"];trace=[]
    for hop,(rel,kind) in enumerate(zip(STEPS,KINDS[1:])):
        if current in ("UNKNOWN","INVALID"):break
        q=step_question(current,rel,kind)
        if mode=="FULL":
            # Native all-memory read, prebuilt once and shared across cases.
            selected=sorted(entries)
        elif mode=="ROUTED":
            ranking,scores=numeric_rank(q,bank)
            selected=ranking[:ROUTE_K]
        elif mode=="ORACLE":
            # Diagnostic upper bound ONLY; uses known supporting card IDs.
            selected=case["supports"][hop:hop+1] if case["supports"] else []
        else:raise RuntimeError("UNKNOWN_TRAVERSAL_MODE")
        if not selected:
            raw="UNKNOWN";prediction="UNKNOWN"
        elif mode=="FULL":
            raw=answer(full_mem,q)
            prediction=read_exact(raw,kind)
        else:
            trial=run_arm(f"{label}_STEP{hop+1}",selected,
                          [{"id":case["id"],"question":q}],strict_sha=True)
            raw=trial["answers"][0]["raw"]
            prediction=read_exact(raw,kind)
        trace.append({"hop":hop+1,"relation":rel,"subject":current,
                      "selected":selected,"question":q,"raw":raw,
                      "prediction":prediction,
                      "expected_kind":kind})
        log("STEP_RESULT",label,case["id"],hop+1,
            "SELECTED",selected,"PRED",repr(prediction))
        current=prediction
    final=current if len(trace)==3 and current not in ("INVALID",) else "UNKNOWN"
    return {"case_id":case["id"],"mode":mode,"trace":trace,"prediction":final,
            "gold":case["answer"],"exact":final==case["answer"],
            "complete":len(trace)==3}

try:
    log("TEST757 START | STEPWISE AUTONOMOUS NUMERIC RETRIEVAL / FROZEN CUT3")
    check("CUDA",torch.cuda.is_available())
    check("ONE_GPU",torch.cuda.device_count()==1)
    check("A100_80GB",torch.cuda.get_device_properties(0).total_memory>=70*2**30)
    check("PANEL_SHA",sha((ROOT/"SEALED_PANEL.json").read_bytes())==PANEL_SHA)
    model_setup()
    weights_before=sentinel()
    make_cartridges()
    bank=build_bank()
    check("BANK_COMPLETE",len(bank)==NUM_CHAINS*3)
    # Preseal the procedure and cases before any model readout.
    R["traversal_protocol"]={"modes":["FULL","ROUTED","ORACLE_DIAGNOSTIC"],
       "relations":STEPS,"route_k":ROUTE_K,
       "query_keys":"MODEL_GENERATED_ONLY",
       "oracle":"uses known cartridge IDs, upper-bound diagnostic, not autonomous",
       "answer_key_visibility":"grading_only",
       "stop_rule":"UNKNOWN or invalid format",
       "source_text_at_inference":False}
    R["protocol_sha256"]=sha(json.dumps(R["traversal_protocol"],sort_keys=True).encode())
    save()
    log("PROTOCOL_PRESEALED",R["protocol_sha256"])
    full_mem,active,steps,build_s=build_fusion(sorted(entries),"FULL_MEMORY",True)
    try:
        full_seals=memory_seals(full_mem)
        R["stepwise"]=[]
        for case in CASES:
            for mode in ("FULL","ROUTED","ORACLE"):
                # Missing cases have no oracle support; use only FULL/ROUTED.
                if mode=="ORACLE" and not case["supports"]:continue
                row=traversal(f"{mode}_{case['id']}",case,mode,bank)
                R["stepwise"].append(row)
                save()
                log("TRAVERSAL_GRADE",mode,case["id"],
                    "PASS" if row["exact"] else "FAIL",
                    "PRED",repr(row["prediction"]),"GOLD",repr(row["gold"]))
        check("FULL_MEMORY_UNCHANGED",compare_seals(full_seals,memory_seals(full_mem)))
    finally:
        del full_mem
        release()
    check("WEIGHTS_UNCHANGED",sentinel()==weights_before)
    check("NO_RESIDUAL_HOOKS",not model.model.layers[CUT]._forward_hooks and
          not model.model.layers[CUT]._forward_pre_hooks)
    summary={}
    for mode in ("FULL","ROUTED","ORACLE"):
        rows=[x for x in R["stepwise"] if x["mode"]==mode]
        positives=[x for x in rows if x["case_id"].startswith("Q")]
        negatives=[x for x in rows if x["case_id"].startswith("M")]
        summary[mode]={"positive_exact":sum(x["exact"] for x in positives),
                       "positive_total":len(positives),
                       "negative_exact":sum(x["exact"] for x in negatives),
                       "negative_total":len(negatives),
                       "hop_count":sum(len(x["trace"]) for x in rows)}
    R["summary"]=summary
    R["status"]="COMPLETE_STEPWISE_SCORED"
    save()
    log("TEST757_COMPLETED",json.dumps(summary,ensure_ascii=False))
    log("FILES",str(OUT),str(LOG),str(MANIFEST))
except Exception as exc:
    R["status"]="ERROR";R["error"]=repr(exc);R["traceback"]=traceback.format_exc()
    save();log("TEST757_ERROR",R["traceback"]);raise
finally:
    save()
