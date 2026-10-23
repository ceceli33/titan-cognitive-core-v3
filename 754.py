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
TEST="754"
ROOT=Path("/content/AKBASCORE_TEST754" if Path("/content").exists() else "/tmp/AKBASCORE_TEST754")
PREVIOUS_ROOT=Path("/content/AKBASCORE_TEST753" if Path("/content").exists() else "/tmp/AKBASCORE_TEST753")
ROOT.mkdir(parents=True,exist_ok=True)
LOG=ROOT/"TEST754.log";LOG.write_text("")
OUT=ROOT/"TEST754_results.json"
CART_DIR=ROOT/"physical_cartridges";CART_DIR.mkdir(exist_ok=True)
EVIDENCE_DIR=ROOT/"sealed_sources";EVIDENCE_DIR.mkdir(exist_ok=True)
MANIFEST=ROOT/"TEST754_manifest.json"
R={"test":TEST,"status":"STARTED","checks":[],"trials":[],
   "source_blobs":{"730":LOCK730,"709":LOCK709,"716":LOCK716},
   "method":"H3 numerical addressing + direct native CUT3 append fusion; no intermediary model-generated synthesis",
   "limitations":["GPU result not known before running",
                  "Native append consolidation is not equivalent to arbitrary algebraic tensor fusion",
                  "Retrieval quality and semantic accuracy are independent of tensor-integrity checks",
                  "Potential pretraining knowledge requires no-memory and source-ablation controls",
                  "Ground-truth grading of open-ended scientific answers requires independent review"]}
MAX_NEW=384
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
QUESTION_SET=[{"id":q["id"],"level":q["level"],"question":q["question"]} for q in QUESTION_SET]
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


# TEST754 — reuse TEST753 physical artifacts; improve addressing using TEST716.
# No answer-key routing, no text-mediated fusion, no new memory motor.
# Defaults favor avoiding repeated expensive forging and full-fusion runs.
import numpy as np
from collections import Counter
SAMPLE_PER_PIECE=512
ROUTING_METHODS=("LEGACY_MEAN","NATIVE8192_MAXMEAN","NATIVE8192_TOP2","NATIVE8192_PEAK50")
PRIMARY_METHOD="NATIVE8192_TOP2"
COMPARE_METHODS=("LEGACY_MEAN","NATIVE8192_MAXMEAN","NATIVE8192_TOP2")
REUSE_753=True
ALLOW_REFORGE_IF_MISSING=True
RUN_FULL_REFERENCE=True
RUN_REVERSED_REFERENCE=True
RUN_SOURCE_ABLATIONS=False
# Re-run question-specific fusion for each method. Disable for routing-only debugging.
RUN_NATIVE_QA=True
RUN_NO_MEMORY=True
# In TEST716, scores compare ALL query positions to sampled cartridge positions.
# This test uses identical scoring definitions, not TEST753's collapsed one-vector representation.
def unit_np(x):
    x=np.asarray(x,dtype=np.float32)
    return x/np.maximum(np.linalg.norm(x,axis=-1,keepdims=True),1e-8)

def sampled_cartridge_matrix(cp):
    x=cp["h"][0,int(cp["p"]):,:].float().cpu().numpy()
    if len(x)==0:raise RuntimeError("EMPTY_H3_CARTRIDGE")
    ix=np.linspace(0,len(x)-1,min(SAMPLE_PER_PIECE,len(x)),dtype=np.int64)
    return np.ascontiguousarray(unit_np(x[ix]).T)

def legacy_cartridge_vector(cp):
    return unit_np(cp["h"][0,int(cp["p"]):,:].float().mean(dim=0).cpu().numpy())

@torch.no_grad()
def query_h3(question):
    # Preserve the TEST716 query framing. Do not insert retrieved text or answers.
    s="<|im_start|>user\n"+question+"\n<|im_end|>\n<|im_start|>assistant\n"
    ids=tok(s,add_special_tokens=False).input_ids
    captures=[]
    with DirectCut3(model.model.layers[CUT],"capture",collector=captures):
        out=model(input_ids=torch.tensor([ids],device=DEV),use_cache=False,return_dict=True)
        del out
    if not captures:raise RuntimeError("QUERY_CAPTURE_EMPTY")
    h=torch.cat(captures,dim=1)[0].float().cpu().numpy()
    return unit_np(h)

@torch.no_grad()
def legacy_query(question):
    # EXACT TEST753 baseline framing; its query reduction is unchanged.
    ids=tok("QUESTION:\n"+question,add_special_tokens=False).input_ids
    captures=[]
    with DirectCut3(model.model.layers[CUT],"capture",collector=captures):
        out=model(input_ids=torch.tensor([ids],device=DEV),use_cache=False,return_dict=True)
        del out
    h=torch.cat(captures,dim=1)[0].float().cpu().numpy()
    return unit_np(h[max(0,len(h)-48):].mean(axis=0))

def score_bank(question,matrices,legacy):
    q=query_h3(question)
    lq=legacy_query(question)
    score={m:{} for m in ROUTING_METHODS}
    for cid,b in matrices.items():
        sim=q@b
        # Equivalent to TEST716's metrics(): mean max, mean top2, median max.
        peaks=np.partition(sim,-min(2,sim.shape[1]),axis=1)[:,-min(2,sim.shape[1]):]
        score["NATIVE8192_MAXMEAN"][cid]=float(peaks.max(axis=1).mean())
        score["NATIVE8192_TOP2"][cid]=float(peaks.mean(axis=1).mean())
        score["NATIVE8192_PEAK50"][cid]=float(np.quantile(peaks.max(axis=1),0.5))
        score["LEGACY_MEAN"][cid]=float(np.dot(lq,legacy[cid]))
    return score

def rank_ids(scores):
    return sorted(scores,key=lambda cid:(-scores[cid],cid))

def pick_with_budget(ordered,top_k=TOP_K):
    chosen=[];tokens=0
    for cid in ordered:
        cost=int(entries[cid]["body_tokens"])
        if tokens+cost+(P if not chosen else 0)>MAX_FUSED_TOKENS:continue
        chosen.append(cid);tokens+=cost
        if len(chosen)==top_k:break
    if len(chosen)<top_k:log("ROUTE_BUDGET_REDUCED",len(chosen),top_k)
    return chosen

def bank_from_verified_cartridges():
    matrices={};legacy={}
    for cid in sorted(entries):
        # safe_load verifies file and internal tensor SHA before H3 bank is constructed.
        cp=safe_load(entries[cid])
        matrices[cid]=sampled_cartridge_matrix(cp)
        legacy[cid]=legacy_cartridge_vector(cp)
        del cp
    return matrices,legacy

def reuse_prior_artifacts():
    global CART_DIR,EVIDENCE_DIR,entries,ledger
    manifest=PREVIOUS_ROOT/"TEST753_manifest.json"
    sealed=PREVIOUS_ROOT/"SEALED_QUESTIONS.json"
    if not (manifest.is_file() and sealed.is_file()):return False
    prior=json.loads(manifest.read_text())
    check("PRIOR_QUESTION_PANEL_MATCH",sha(sealed.read_bytes())==PANEL_SHA)
    check("PRIOR_SOURCE_LOCKS",prior["locks"]==R["source_blobs"])
    check("PRIOR_MODEL_CUT",prior["model"]==MODEL_ID and int(prior["cut"])==CUT)
    CART_DIR=PREVIOUS_ROOT/"physical_cartridges"
    EVIDENCE_DIR=PREVIOUS_ROOT/"sealed_sources"
    entries={x["id"]:x for x in prior["cartridges"]}
    check("PRIOR_CARTRIDGE_FILES",len(entries)>0 and all((CART_DIR/x["file"]).is_file() for x in entries.values()))
    for cid,e in entries.items():
        check("PRIOR_SHA_"+cid,sha_file(CART_DIR/e["file"])==e["sha256"])
    ledger=prior
    R["reused_from"]=str(PREVIOUS_ROOT)
    R["sources"]=prior["sources"]
    save()
    return True

def make_fresh_artifacts():
    global entries,ledger
    pubs=[];used=set()
    for src in SOURCES:
        item=retrieve_publication(src,used)
        pubs.append(item)
        f=EVIDENCE_DIR/(item["id"]+".txt")
        f.write_text(item["body"],encoding="utf-8")
        check("SOURCE_SHA_"+item["id"],sha_file(f)==item["excerpt_sha256"])
    check("SOURCE_INDEPENDENCE",len({p["resolved_url"] for p in pubs})==3)
    check("SOURCE_LICENSES",all(p["license"] and "creativecommons.org/licenses/" in p["license"] for p in pubs))
    R["sources"]=[{k:v for k,v in p.items() if k!="body"} for p in pubs]
    entries={}
    ledger={"test":TEST,"model":MODEL_ID,"cut":CUT,"locks":R["source_blobs"],
            "panel_sha256":PANEL_SHA,"sources":R["sources"],"cartridges":[]}
    for pub in pubs:
        for j,ids in enumerate(source_parts(pub["body"],pub["id"])):
            cid=f'{pub["id"]}_{j:02d}'
            cp,secs=forge_native(ids,cid)
            path=CART_DIR/(cid+".pt")
            tmp=Path(str(path)+".tmp")
            torch.save(cp,tmp);tmp.replace(path)
            e={"id":cid,"source_id":pub["id"],"role":"SOURCE_PIECE",
               "parents":[],"file":path.name,"sha256":sha_file(path),
               "tensor_sha":seal_cp(cp),"body_tokens":len(ids),"forge_seconds":secs}
            entries[cid]=e;ledger["cartridges"].append(e)
            atomic_json(MANIFEST,ledger)
            del cp;release()
            log("FORGED_AND_SEALED",cid,e["sha256"])
    save()

def evaluate_routes(routes):
    methods=list(ROUTING_METHODS)
    stats={}
    for method in methods:
        lists=[routes[q["id"]]["ranked"][method][:TOP_K] for q in QUESTION_SET]
        sets=[tuple(x) for x in lists]
        stats[method]={"distinct_top5_sets":len(set(sets)),
                       "distinct_top1":len(set(x[0] for x in lists)),
                       "mean_pairwise_overlap":round(
                           sum(len(set(a)&set(b))/max(1,len(set(a)|set(b)))
                               for i,a in enumerate(lists) for b in lists[i+1:])
                           /max(1,len(lists)*(len(lists)-1)//2),5),
                       "source_coverage_per_question":[len({entries[c]["source_id"] for c in x}) for x in lists]}
    return stats

def source_coverage(ids):
    return sorted({entries[cid]["source_id"] for cid in ids})

try:
    log("TEST754 START | REUSE TEST753 NATIVE FUSION + TEST716 TOKEN-LEVEL ROUTING")
    check("CUDA",torch.cuda.is_available())
    check("ONE_GPU",torch.cuda.device_count()==1)
    check("A100_80GB",torch.cuda.get_device_properties(0).total_memory>=70*2**30)
    check("LOCKED_709_716_730",True)
    check("PANEL_SHA",sha((ROOT/"SEALED_QUESTIONS.json").read_bytes())==PANEL_SHA)
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
    cfg=model.config;NL=len(model.model.layers);H=int(cfg.hidden_size)
    QH=int(cfg.num_attention_heads);KVH=int(cfg.num_key_value_heads)
    HD=int(getattr(cfg,"head_dim",None) or H//QH)
    check("MODEL_ARCH",(NL,H,QH,KVH,HD)==EXPECTED,(NL,H,QH,KVH,HD))
    check("FROZEN",all(not par.requires_grad for par in model.parameters()))
    check("NF4",any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
    before=sentinel()
    reused=False
    if REUSE_753:reused=reuse_prior_artifacts()
    if not reused:
        if not ALLOW_REFORGE_IF_MISSING:
            raise RuntimeError("NO_TEST753_ARTIFACTS; set ALLOW_REFORGE_IF_MISSING=True")
        log("PRIOR_ARTIFACTS_UNAVAILABLE; FORGING_ONCE")
        make_fresh_artifacts()
    check("CARTRIDGES_READY",len(entries)>=6)
    check("ALL_BODY_TOKENS_FIT_FULL_REFERENCE",
          sum(int(e["body_tokens"]) for e in entries.values())+P<=MAX_FUSED_TOKENS)
    R["cartridges"]=[{k:v for k,v in e.items() if k!="tensor_sha"} for e in entries.values()]
    R["source_mode"]="REUSE_VERIFIED_TEST753" if reused else "FORGE_FRESH"
    R["methods"]=list(ROUTING_METHODS)
    save()
    matrices,legacy=bank_from_verified_cartridges()
    check("NUMERIC_BANK",len(matrices)==len(entries) and
          all(v.shape[0]==H and v.shape[1]>0 for v in matrices.values()))
    routes={}
    for q in QUESTION_SET:
        t=time.perf_counter()
        scores=score_bank(q["question"],matrices,legacy)
        ranked={m:rank_ids(scores[m]) for m in ROUTING_METHODS}
        routes[q["id"]]={"ranked":ranked,
                          "scores":scores,
                          "route_ms":round((time.perf_counter()-t)*1000,3),
                          "selected":{m:pick_with_budget(ranked[m]) for m in ROUTING_METHODS}}
        log("ROUTE_COMPARE",q["id"],json.dumps({
            "selected":routes[q["id"]]["selected"],
            "source_coverage":{m:source_coverage(routes[q["id"]]["selected"][m])
                               for m in ROUTING_METHODS},
            "route_ms":routes[q["id"]]["route_ms"]},ensure_ascii=False))
        R["routing"]=routes;save()
    R["routing_summary"]=evaluate_routes(routes)
    log("ROUTING_SUMMARY",json.dumps(R["routing_summary"],ensure_ascii=False))
    check("PANEL_STILL_SEALED",sha((ROOT/"SEALED_QUESTIONS.json").read_bytes())==PANEL_SHA)
    del matrices,legacy
    gc.collect()
    # Route selection is not influenced by answer generation or human grading.
    if RUN_NATIVE_QA:
        for q in QUESTION_SET:
            for method in COMPARE_METHODS:
                ids=routes[q["id"]]["selected"][method]
                run_arm(method+"_"+q["id"],ids,[q],strict_sha=True)
        if RUN_FULL_REFERENCE:
            run_arm("FULL_NATIVE_REFERENCE",sorted(entries),QUESTION_SET,strict_sha=True)
        if RUN_REVERSED_REFERENCE:
            run_arm("REVERSED_NATIVE_REFERENCE",list(reversed(sorted(entries))),QUESTION_SET,strict_sha=True)
        if RUN_SOURCE_ABLATIONS:
            for source in sorted({e["source_id"] for e in entries.values()}):
                only=[c for c in sorted(entries) if entries[c]["source_id"]==source]
                without=[c for c in sorted(entries) if entries[c]["source_id"]!=source]
                run_arm("SOURCE_ONLY_"+source,only,QUESTION_SET,strict_sha=True)
                run_arm("SOURCE_REMOVED_"+source,without,QUESTION_SET,strict_sha=True)
    if RUN_NO_MEMORY:
        baseline=[]
        for q in QUESTION_SET:
            t=time.perf_counter()
            raw=answer(None,q["question"])
            baseline.append({"id":q["id"],"raw":raw,
                             "answer_ms":round((time.perf_counter()-t)*1000,3)})
        R["no_memory_baseline"]=baseline
    check("WEIGHT_SENTINEL_UNCHANGED",sentinel()==before)
    check("NO_RESIDUAL_HOOKS",not model.model.layers[CUT]._forward_hooks and
          not model.model.layers[CUT]._forward_pre_hooks)
    R["status"]="COMPLETE_ROUTING_AND_NATIVE_FUSION_UNGRADED"
    R["summary"]={"cartridges":len(entries),"reused":reused,
                  "routing_methods":list(ROUTING_METHODS),
                  "comparison_methods":list(COMPARE_METHODS),
                  "arms":len(R["trials"]),
                  "text_mediated_synthesis":False,
                  "semantic_correctness":"UNSCORED_REQUIRES_SOURCE_GROUNDED_REVIEW",
                  "routing_relevance":"UNSCORED_REQUIRES_PIECE_GROUND_TRUTH",
                  "routing_diversity":R["routing_summary"],
                  "latency":"MEASURED_IN_LOG"}
    save();log("TEST754_COMPLETED",json.dumps(R["summary"],ensure_ascii=False))
    log("FILES",str(OUT),str(LOG),str(MANIFEST))
except Exception as exc:
    R["status"]="ERROR";R["error"]=repr(exc);R["traceback"]=traceback.format_exc()
    save();log("TEST754_ERROR",R["traceback"]);raise
finally:
    save()
