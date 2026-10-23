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
TEST="753"
ROOT=Path("/content/AKBASCORE_TEST753" if Path("/content").exists() else "/tmp/AKBASCORE_TEST753")
ROOT.mkdir(parents=True,exist_ok=True)
LOG=ROOT/"TEST753.log";LOG.write_text("")
OUT=ROOT/"TEST753_results.json"
CART_DIR=ROOT/"physical_cartridges";CART_DIR.mkdir(exist_ok=True)
EVIDENCE_DIR=ROOT/"sealed_sources";EVIDENCE_DIR.mkdir(exist_ok=True)
MANIFEST=ROOT/"TEST753_manifest.json"
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

def route_vector(x):
    import torch.nn.functional as F
    return F.normalize(x.float(),dim=-1,eps=1e-8)

@torch.no_grad()
def numeric_query_vector(question):
    # H3 capture for the query ONLY for address selection, not for synthesis.
    # Do not use gold answers or source text to select candidates.
    ids=tok("QUESTION:\n"+question,add_special_tokens=False).input_ids
    captures=[]
    with DirectCut3(model.model.layers[CUT],"capture",collector=captures):
        z=model(input_ids=torch.tensor([ids],device=DEV),
                use_cache=False,return_dict=True)
        del z
    h=torch.cat(captures,dim=1)
    vec=route_vector(h[:,max(0,h.shape[1]-48):,:].mean(dim=1)[0].cpu())
    del h,captures
    return vec

def cartridge_vector(cp):
    # Actual CUT3 residuals, excluding the shared canonical prefix.
    h=cp["h"][:,cp["p"]:,:].float()
    if h.shape[1]<1:raise RuntimeError("EMPTY_NUMERIC_BODY")
    return route_vector(h.mean(dim=1)[0].cpu())

def fast_route(question,bank,k=TOP_K,cover_sources=False):
    start=time.perf_counter()
    q=numeric_query_vector(question)
    scores=[(float(torch.dot(q,vec)),cid) for cid,vec in bank.items()]
    scores.sort(key=lambda x:(-x[0],x[1]))
    chosen=[cid for _,cid in scores[:k]]
    if cover_sources:
        # Provenance coverage is a transparent evaluation arm, NOT answer-key routing.
        for source in sorted({x.split("_")[0] for x in bank}):
            if not any(c.startswith(source+"_") for c in chosen):
                for _,cid in scores:
                    if cid.startswith(source+"_"):
                        chosen.append(cid);break
    return chosen,{"scores":scores,"address_ms":round((time.perf_counter()-start)*1000,3),
                   "cover_sources":cover_sources}

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

def commit_piece(cid,ids,source_id):
    cp,seconds=forge_native(ids,cid)
    path=CART_DIR/(cid+".pt")
    tmp=Path(str(path)+".tmp")
    torch.save(cp,tmp);tmp.replace(path)
    e={"id":cid,"source_id":source_id,"role":"SOURCE_PIECE",
       "parents":[],"file":path.name,"sha256":sha_file(path),
       "tensor_sha":seal_cp(cp),"body_tokens":len(ids),"forge_seconds":seconds}
    entries[cid]=e
    ledger["cartridges"].append(e)
    atomic_json(MANIFEST,ledger)
    vec=cartridge_vector(cp)
    del cp
    release()
    log("COMMIT_NUMERIC_PIECE",cid,e["sha256"],"TOKENS",len(ids))
    return vec

try:
    log("TEST753 START | NATIVE H3/KV FUSION | NO TEXT-MEDIATED SYNTHESIS")
    check("CUDA",torch.cuda.is_available())
    check("ONE_GPU",torch.cuda.device_count()==1)
    check("A100_80GB",torch.cuda.get_device_properties(0).total_memory>=70*2**30)
    check("LOCKED_730_709_716",True)
    check("QUESTION_PANEL_PRESEALED",sha((ROOT/"SEALED_QUESTIONS.json").read_bytes())==PANEL_SHA)
    publications=[];used_pmcs=set()
    for src in SOURCES:
        item=retrieve_publication(src,used_pmcs)
        publications.append(item)
        path=EVIDENCE_DIR/(item["id"]+".txt")
        path.write_text(item["body"],encoding="utf-8")
        check("SOURCE_SEALED_"+item["id"],sha_file(path)==item["excerpt_sha256"])
    check("THREE_INDEPENDENT_SOURCES",
          len({x["resolved_url"] for x in publications})==3)
    check("LICENSES",all(x["license"] and
          "creativecommons.org/licenses/" in x["license"] for x in publications))
    R["sources"]=[{k:v for k,v in p.items() if k!="body"} for p in publications];save()
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
    check("ARCH_72B",(NL,H,QH,KVH,HD)==EXPECTED,(NL,H,QH,KVH,HD))
    check("WEIGHTS_FROZEN",all(not p.requires_grad for p in model.parameters()))
    check("NF4",any(isinstance(m,bitsandbytes.nn.Linear4bit) for m in model.modules()))
    check("NO_FORWARD_HOOKS",not model.model.layers[CUT]._forward_hooks and
          not model.model.layers[CUT]._forward_pre_hooks)
    before=sentinel()
    entries={}
    ledger={"test":TEST,"model":MODEL_ID,"cut":CUT,
            "locks":R["source_blobs"],"panel_sha256":PANEL_SHA,
            "sources":R["sources"],"cartridges":[]}
    bank={}
    # Build physical numerical cartridges once; NO text summaries or reflections.
    for pub in publications:
        for j,ids in enumerate(source_parts(pub["body"],pub["id"])):
            cid=f'{pub["id"]}_{j:02d}'
            bank[cid]=commit_piece(cid,ids,pub["id"])
    check("NUMERIC_BANK_CREATED",len(bank)>=6,{"count":len(bank)})
    check("FULL_FUSION_BUDGET",sum(e["body_tokens"] for e in entries.values())+P<=MAX_FUSED_TOKENS)
    check("ALL_FILES_PERSISTED",all((CART_DIR/e["file"]).exists() for e in entries.values()))
    check("NO_TEXT_MEDIATED_SYNTHESIS",True)
    R["bank_size"]=len(bank)
    R["cartridge_tokens"]={cid:e["body_tokens"] for cid,e in entries.items()}
    save()

    # Route every sealed question with ACTUAL H3 numerical representations.
    routes={}
    for q in QUESTION_SET:
        ids,detail=fast_route(q["question"],bank,TOP_K,False)
        covered,coverdetail=fast_route(q["question"],bank,TOP_K,True)
        routes[q["id"]]={"topk":ids,"source_coverage":covered,
                         "topk_diagnostics":detail,
                         "coverage_diagnostics":coverdetail}
        log("H3_ROUTE",q["id"],ids,"COVERAGE",covered)
    R["routing"]=routes;save()
    check("SEALED_PANEL_STILL_UNCHANGED",
          sha((ROOT/"SEALED_QUESTIONS.json").read_bytes())==PANEL_SHA)

    # Full native fusion of all physically written source pieces.
    # This is the high-cost reference, not an assumption of semantic success.
    all_ids=list(bank)
    run_arm("FULL_NATIVE_ALL",all_ids,QUESTION_SET,strict_sha=True)

    # Fast numerical retrieval: one selected subset per question.
    # Keep all answers and timing for head-to-head accuracy/latency comparison.
    for q in QUESTION_SET:
        ids=routes[q["id"]]["topk"]
        run_arm("FAST_H3_"+q["id"],ids,[q],strict_sha=True)

    # Source-coverage arm ensures at least one piece per source,
    # without using the answer key or generating intermediary text.
    for q in QUESTION_SET:
        ids=routes[q["id"]]["source_coverage"]
        run_arm("COVERAGE_"+q["id"],ids,[q],strict_sha=True)

    # Ablations: each source alone, each source withheld, and order reversal.
    for source in sorted({x["source_id"] for x in entries.values()}):
        only=[cid for cid in all_ids if entries[cid]["source_id"]==source]
        without=[cid for cid in all_ids if entries[cid]["source_id"]!=source]
        run_arm("SOURCE_ONLY_"+source,only,QUESTION_SET,strict_sha=True)
        run_arm("SOURCE_REMOVED_"+source,without,QUESTION_SET,strict_sha=True)
    run_arm("REVERSED_NATIVE_ALL",list(reversed(all_ids)),QUESTION_SET,strict_sha=True)

    # No-memory baseline: detect pretraining knowledge and prompt-only behavior.
    baseline=[]
    for q in QUESTION_SET:
        t=time.perf_counter()
        raw=answer(None,q["question"])
        baseline.append({"id":q["id"],"raw":raw,
                         "answer_ms":round((time.perf_counter()-t)*1000,3)})
    R["no_memory_baseline"]=baseline;save()
    check("WEIGHT_SENTINEL_UNCHANGED",sentinel()==before)
    check("NO_FORWARD_HOOKS_AFTER",not model.model.layers[CUT]._forward_hooks and
          not model.model.layers[CUT]._forward_pre_hooks)
    R["summary"]={
        "physical_pieces":len(entries),
        "native_fusion":True,
        "text_mediated_synthesis":False,
        "arms":len(R["trials"]),
        "routing":"H3 numerical, no gold answers",
        "accuracy":"UNSCORED_PENDING_INDEPENDENT_REVIEW",
        "speedup":"MEASURE_FROM_LOG_NOT_ASSUMED"}
    R["status"]="COMPLETED_MECHANICAL_PENDING_SEMANTIC_REVIEW"
    save()
    log("TEST753_COMPLETED",R["summary"])
    log("FILES",str(OUT),str(LOG),str(MANIFEST))
except Exception as e:
    R["status"]="ERROR";R["error"]=repr(e);R["traceback"]=traceback.format_exc()
    save()
    log("TEST753_ERROR",R["traceback"])
    raise
finally:
    save()
