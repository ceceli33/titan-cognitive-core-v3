# ===== HIPPOCAMPUS MISTRAL 1.4 · PART 2/3 — paste directly after part 1 in the same cell (or run in the same runtime) =====

# =====================================================================================================================
# READ-ONLY MEASUREMENT LAYER
# Calls only the engine's own functions, in the engine's own order. The recording pre-hook returns None (it cannot
# change any input) and is removed in a finally-block. All comparisons are bitwise (torch.equal) or SHA-256.
# =====================================================================================================================
def _tbytes(x):
    x=x.detach().contiguous().cpu()
    if x.dtype==torch.bfloat16:x=x.view(torch.uint16)
    return x.numpy().tobytes()
def memory_sha(mem,rows=None):
    h=hashlib.sha256()
    for k,v in mem:
        if rows is not None:k=k[:,:,:rows,:];v=v[:,:,:rows,:]
        h.update(_tbytes(k));h.update(_tbytes(v))
    return h.hexdigest()
def memories_equal(a,b):
    return len(a)==len(b) and all(torch.equal(x[0],y[0]) and torch.equal(x[1],y[1]) for x,y in zip(a,b))

class Recorder:
    """Recording-only forward pre-hook on the causal-LM module: kind of input, length, cache length, zero-embedding flag."""
    def __init__(self):self.rows=[];self.h=None
    def _rec(self,mod,args,kw):
        ids=kw.get("input_ids",args[0] if args else None);emb=kw.get("inputs_embeds");pkv=kw.get("past_key_values");pl=None
        if pkv is not None:
            try:pl=int(pkv.get_seq_length())
            except Exception:pl=-1
        if ids is not None:
            self.rows.append(dict(kind="ids",n=int(ids.shape[-1]),has_past=pkv is not None,past_len=pl,embeds_zero=None,ids=[int(t) for t in ids.reshape(-1).tolist()] if ids.numel()<=4096 else None))
        else:
            self.rows.append(dict(kind="embeds",n=int(emb.shape[1]) if emb is not None else -1,has_past=pkv is not None,past_len=pl,
                                  embeds_zero=(bool(float(emb.detach().abs().max())==0.0) if emb is not None else None),ids=None))
        return None
    def __enter__(self):self.h=E["model"].register_forward_pre_hook(self._rec,with_kwargs=True);return self
    def __exit__(self,*a):
        if self.h is not None:self.h.remove();self.h=None
        return False

def sync():torch.cuda.synchronize()
def memory_len(keys):return int(E["P"])+sum(len(E["CAR"][ci]["body"]) for ci in keys)
def segments_for(scn,cond,keys):
    P=int(E["P"]);segs=[("prefix",0,P,None)];a=P
    for s,ci in zip(letters(cond),keys):
        q=len(E["CAR"][ci]["body"]);lab=("C′" if (cond=="ABC_CF" and s=="C") else s);segs.append((lab,a,a+q,int(ci)));a+=q
    return segs
def query_view(q):
    ids=E["tok"](E["query_suffix"](q),add_special_tokens=False).input_ids
    return dict(question=q,n=len(ids),ids=list(map(int,ids)),tokens=[E["tok"].decode([t]) for t in ids])
def contains_seq(hay,needle):
    n=len(needle)
    return n>0 and any(hay[i:i+n]==needle for i in range(len(hay)-n+1))

def memory_profile(mem):
    kn=[];vn=[];nb=0
    with torch.inference_mode():
        for k,v in mem:
            kn.append([float(x) for x in k.float().norm(dim=-1).mean(dim=1)[0].tolist()])
            vn.append([float(x) for x in v.float().norm(dim=-1).mean(dim=1)[0].tolist()])
            nb+=k.numel()*k.element_size()+v.numel()*v.element_size()
    k0=mem[0][0]
    return dict(layers=len(mem),T=int(k0.shape[-2]),kv_heads=int(k0.shape[1]),head_dim=int(k0.shape[-1]),dtype=str(k0.dtype).replace("torch.",""),
                shape=list(k0.shape),bytes=int(nb),k_norm=kn,v_norm=vn,sha256=memory_sha(mem))

def joint_difference(mem_dc,mem_joint,segs):
    """relative L2 difference ‖X_DC − X_JOINT‖/‖X_JOINT‖ per layer and per memory segment (K and V)."""
    out=dict(k=[],v=[],labels=[s[0] for s in segs],bitwise_equal_segments=[])
    with torch.inference_mode():
        for li,((kd,vd),(kj,vj)) in enumerate(zip(mem_dc,mem_joint)):
            rk=[];rv=[]
            for lab,a,b,_ in segs:
                A=kd[:,:,a:b].float();B=kj[:,:,a:b].float();rk.append(float((A-B).norm()/max(float(B.norm()),1e-12)))
                A=vd[:,:,a:b].float();B=vj[:,:,a:b].float();rv.append(float((A-B).norm()/max(float(B.norm()),1e-12)))
            out["k"].append(rk);out["v"].append(rv)
        for lab,a,b,_ in segs:
            out["bitwise_equal_segments"].append(bool(all(torch.equal(kd[:,:,a:b],kj[:,:,a:b]) and torch.equal(vd[:,:,a:b],vj[:,:,a:b]) for (kd,vd),(kj,vj) in zip(mem_dc,mem_joint))))
    return out

def measure_build(scn,cond="ABC"):
    """Builds the DC_CUT6_NATIVE memory step by step with the engine's own init_incremental() and append_native678()
    (exactly the body of memory678), records every forward, checks prior rows bitwise after each append, and checks that
    the final memory is bitwise identical to memory678(keys,'DC_CUT6_NATIVE') — the path used by every engine run —
    and to the TEST560 PyTorch reference path memory678(keys,'DC_CUT6_REFERENCE')."""
    with ENGINE_LOCK:
        lets=letters(cond);keys=E["keys686"](scn,cond);CAR=E["CAR"];P=int(E["P"]);H=int(E["H"]);KVH=int(E["KVH"]);HD=int(E["HD"]);C=int(E["CUT"])
        cars=[dict(slot=s,label=SLOT_LABEL[scn]["C_CF" if (cond=="ABC_CF" and s=="C") else s],cartridge_id=int(ci),text=CAR[ci]["fact"],
                   text_sha256=sha_bytes(CAR[ci]["fact"].encode("utf-8")),body_tokens=len(CAR[ci]["body"])) for s,ci in zip(lets,keys)]
        rec=Recorder();steps=[];t_all=time.perf_counter()
        with rec:
            sync();a=len(rec.rows);t=time.perf_counter();mem=E["init_incremental"](keys[0]);sync();dt=time.perf_counter()-t
            steps.append(dict(kind="init",slot=lets[0],old_len=0,new_len=int(mem[0][0].shape[-2]),seconds=dt,fw=(a,len(rec.rows)),prior_rows_bitwise_unchanged=None,
                              prior_sha_before=None,prior_sha_after=None))
            for s,ci in zip(lets[1:],keys[1:]):
                oldn=int(mem[0][0].shape[-2]);sb=memory_sha(mem);a=len(rec.rows);sync();t=time.perf_counter()
                new=E["append_native678"](mem,ci);sync();dt=time.perf_counter()-t
                same=all(torch.equal(new[l][0][:,:,:oldn],mem[l][0]) and torch.equal(new[l][1][:,:,:oldn],mem[l][1]) for l in range(len(mem)))
                steps.append(dict(kind="append",slot=s,old_len=oldn,new_len=int(new[0][0].shape[-2]),seconds=dt,fw=(a,len(rec.rows)),prior_rows_bitwise_unchanged=bool(same),
                                  prior_sha_before=sb,prior_sha_after=memory_sha(new,oldn)))
                mem=new
        build_seconds=time.perf_counter()-t_all
        for st in steps:st["forwards"]=[{k:v for k,v in f.items() if k!="ids"} for f in rec.rows[st["fw"][0]:st["fw"][1]]];del st["fw"]
        sync();t=time.perf_counter();eng=E["memory678"](keys,"DC_CUT6_NATIVE");sync();eng_seconds=time.perf_counter()-t
        engine_identical=memories_equal(mem,eng);del eng
        ref=E["memory678"](keys,"DC_CUT6_REFERENCE");reference_identical=memories_equal(mem,ref);del ref
        # the lower-layer memory rows ARE the cartridge rows (keys re-phased to their memory position); H6 rows measured
        for st,ci,cd in zip(steps,keys,cars):
            cp=E["forge_checkpoint"](ci);q=len(CAR[ci]["body"]);a_=st["old_len"]
            cd["h_shape"]=list(cp["h"].shape);cd["kv_lower_shape"]=list(cp["kv"][0][0].shape);cd["kv_lower_layers"]=len(cp["kv"])
            rows=st["new_len"]-a_;cd["rows_in_memory"]=rows
            cd["h_bytes"]=rows*H*2;cd["kv_lower_bytes"]=rows*KVH*HD*2*2*(C+1);cd["cartridge_bytes"]=cd["h_bytes"]+cd["kv_lower_bytes"]
            inj=cp["h"] if st["kind"]=="init" else cp["h"][:,P:,:]
            cd["h_row_norm"]=[float(x) for x in inj.float().norm(dim=-1)[0].tolist()]
            ok=True
            with torch.inference_mode():
                for li in range(C+1):
                    k,v=cp["kv"][li]
                    if st["kind"]=="init":ok&=torch.equal(mem[li][0][:,:,:rows],k) and torch.equal(mem[li][1][:,:,:rows],v)
                    else:
                        newpos=torch.arange(a_,a_+q,device=k.device)
                        kk=E["rephase_key"](k[:,:,P:,:],cp["positions"][P:],newpos)
                        ok&=torch.equal(mem[li][0][:,:,a_:a_+q],kk) and torch.equal(mem[li][1][:,:,a_:a_+q],v[:,:,P:,:])
            st["lower_rows_equal_cartridge"]=bool(ok);del cp
        segs=segments_for(scn,cond,keys);prof=memory_profile(mem)
        mj=E["memory678"](keys,"TEXT_JOINT");jd=joint_difference(mem,mj,segs);del mj
        spec=E["SCENARIOS686"][scn];final_q=dict(spec["queries"]).get("FINAL")
        reproduced=E["answer_layers"](mem,final_q) if final_q else None
        out=dict(scenario=scn,condition=cond,keys=[int(k) for k in keys],letters=list(lets),cartridges=cars,steps=steps,memory=prof,segments=segs,
                 build_seconds=build_seconds,engine_path_seconds=eng_seconds,engine_path_identical=bool(engine_identical),reference_path_identical=bool(reference_identical),
                 joint_difference=jd,prefix_tokens=P,cut=C,final_question=final_q,final_answer_on_measured_memory=reproduced,
                 source_reads=sum(1 for st in steps for f in st["forwards"] if f["kind"]=="ids" and not f["has_past"]),
                 zero_embed_forwards=sum(1 for st in steps for f in st["forwards"] if f["kind"]=="embeds" and f["embeds_zero"]),
                 query_views={qid:query_view(q) for qid,q in spec["queries"]})
        for qid,v in out["query_views"].items():
            v["cartridge_sequence_in_query"]=any(contains_seq(v["ids"],E["CAR"][ci]["body"]) for ci in keys)
        del mem;gc.collect();torch.cuda.empty_cache()
        return out

def descriptive(raw,expected):
    """TEST684 rule-based descriptive audit — SECONDARY observation, never a score"""
    try:return E["audit680"](raw,None if expected in (None,"UNKNOWN") else expected)
    except Exception as ex:return f"AUDIT_ERROR:{type(ex).__name__}"

def score_run(scn,cond,res,scored):
    sc=SCORING[scn];rows=[]
    for r in res["responses"]:
        spec=sc["questions"].get(r["question_id"]) if r["question_id"]!="CUSTOM" else None
        g=grade(r["answer"],spec,cond,scored and spec is not None)
        if scored and spec is not None:
            st686,exp686=E["grade686"](r["answer"],E["SCORING686"][scn]["questions"].get(r["question_id"]),cond)
            g["status_matches_test686"]=st686==g["status"];g["status"]=st686
        g["descriptive_audit"]="UNSCORED" if g["status"]=="UNSCORED" else descriptive(r["answer"],g.get("expected"))
        rows.append(dict(r,**g))
    staged=res.get("staged_chain")
    if staged:
        hops=[]
        for t in staged["trace"]:
            t=dict(t)
            if not scored:t["status"]="UNSCORED";t["expected"]=None
            t["descriptive_audit"]="UNSCORED" if t["status"]=="UNSCORED" else descriptive(t["answer"],t.get("expected"))
            hops.append(t)
        staged=dict(staged,trace=hops,chain_status=(staged["status"] if scored else "UNSCORED"),chain_expected=(staged.get("expected") if scored else None))
    return rows,staged

def recorded_run(scn,cond,rep,question=None,include_staged=True):
    """mistral_run_demo() (TEST686 procedure), observed by the recording pre-hook."""
    with ENGINE_LOCK:
        keys=E["keys686"](scn,cond);T=memory_len(keys)
        rec=Recorder();t=time.perf_counter()
        with rec:res=mistral_run_demo(scn,cond,rep,question=question,include_staged=include_staged)
        sync();wall=time.perf_counter()-t
    fw=rec.rows;starts=[i for i,f in enumerate(fw) if f["kind"]=="ids" and f["n"]>1 and f["has_past"] and f["past_len"]==T]
    build=[{k:v for k,v in f.items() if k!="ids"} for f in fw[:starts[0]]] if starts else [{k:v for k,v in f.items() if k!="ids"} for f in fw]
    items=list(res["responses"])+(list(res["staged_chain"]["trace"]) if res.get("staged_chain") else [])
    seg_ok=len(starts)==len(items);MAXN=int(E["MAX_NEW"])
    for j,it in enumerate(items):
        if seg_ok:
            a=starts[j];b=starts[j+1] if j+1<len(starts) else len(fw)
            gen=sum(1 for f in fw[a+1:b] if f["kind"]=="ids" and f["n"]==1 and f["has_past"])
            qids=fw[a]["ids"] or []
            it["query_tokens"]=fw[a]["n"];it["generated_tokens"]=gen;it["limit_reached"]=gen>=MAXN
            it["query_ids_equal_template"]=qids==E["tok"](E["query_suffix"](it["question"]),add_special_tokens=False).input_ids
            it["cartridge_sequence_in_query"]=any(contains_seq(qids,E["CAR"][ci]["body"]) for ci in keys)
        else:
            it["query_tokens"]=None;it["generated_tokens"]=None;it["limit_reached"]=None;it["query_ids_equal_template"]=None;it["cartridge_sequence_in_query"]=None
    scored=not scenario_edited(scn)
    rows,staged=score_run(scn,cond,res,scored)
    return dict(scenario=scn,condition=cond,representation=rep,custom_question=question,keys=[int(k) for k in keys],memory_rows=T,
                cartridge_texts=res.get("cartridge_texts"),responses=rows,staged=staged,run_sha256=res.get("run_sha256"),engine_json=res.get("saved_to"),
                engine_elapsed_seconds=res.get("elapsed_seconds"),wall_seconds=wall,build_forwards=build,forward_segmentation_ok=seg_ok,
                weights_frozen=res.get("weights_frozen"),sentinel_unchanged=res.get("sentinel_unchanged"),scored=scored,timestamp=res.get("timestamp"))


# =====================================================================================================================
# EXPERIMENT ORCHESTRATION · RECORDS · PACKAGING
# =====================================================================================================================
N_STAGES=10
STAGE_TITLES=["Loading frozen model","Verifying original engine","Registering cartridges","Constructing numerical memory",
              "Injecting native CUT6 memory — verification","Executing model questions","Running relational synthesis and causal controls",
              "Verifying frozen weights","Generating scientific figures","Packaging experiment records"]
FIG_FILES=["FIGURE_01_MEMORY_INJECTION_PROTOCOL.jpg","FIGURE_02_ARCHITECTURE.jpg","FIGURE_03_CARTRIDGE_CONSOLIDATION.jpg","FIGURE_04_INTERNAL_MEMORY_XRAY.jpg",
           "FIGURE_05_AKBASCORE_EXPERIMENT.jpg","FIGURE_06_MATRIX_EXPERIMENT.jpg","FIGURE_07_CAUSAL_CONTROLS.jpg","FIGURE_08_VERIFICATION.jpg"]
N_FIGS=len(FIG_FILES)
RUN_COUNTER=[0]
class StageError(RuntimeError):
    def __init__(self,stage,ex):super().__init__(f"stage {stage} failed: {type(ex).__name__}: {ex}");self.stage=stage;self.original=ex

def new_run_id(prefix="MAM14M"):
    RUN_COUNTER[0]+=1;return f"{prefix}-{datetime.now().astimezone().strftime('%Y%m%d-%H%M%S')}-{RUN_COUNTER[0]:04d}"
def prune_runs(keep=3,prefix="MAM14M-"):
    runs=sorted([p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith(prefix)],key=lambda p:p.stat().st_mtime)
    for p in runs[:-keep]:shutil.rmtree(p,ignore_errors=True)

def controls_matrix(P,scn,rep):
    return {r["condition"]:r for r in P["controls"] if r["scenario"]==scn and r["representation"]==rep}

def full_run(ctl,emit):
    """ctl: dict(scenario, condition, representation, custom, text_controls). emit(stage,title,body,final=True) is called after
    each stage has actually completed (final=False: progress inside a running stage). Returns dict(P=payload, run_dir, figures, zip, files)."""
    prune_runs(3);run_id=new_run_id();run_dir=ROOT/run_id;run_dir.mkdir(parents=True,exist_ok=True)
    t0=time.perf_counter()
    P=dict(run_id=run_id,started_utc=utc_now(),started_local=local_now(),startup=copy.deepcopy(STARTUP),config=dict(ctl),
           scenarios={},builds={},primary={},controls=[],custom=None,verify={},files={},errors=[],
           references=dict(test686=TEST686_REF,test686_log=STARTUP.get("test686_log_verified"),qwen_v14=QWEN_V14_REF))
    stage=0
    try:
        stage=1
        emit(1,STAGE_TITLES[0],f"Completed at start-up ({STARTUP.get('finished_utc')}): {STARTUP.get('model_id')} · {STARTUP.get('dtype')} · {STARTUP.get('gpu')} · "
             f"engine boot {STARTUP.get('engine_seconds')} s · full-weight SHA-256 recorded: {str(STARTUP.get('full_weight_sha256'))[:16]}…")
        stage=2
        P["verify"]["sentinel_before"]=E["sentinel"]();P["verify"]["guard_before"]=param_guard(E["model"]);P["verify"]["frozen_before"]=frozen_state()
        src=STARTUP.get("sources",{})
        ok=(src.get("684.py",{}).get("git_blob")==LOCKS["test684_blob"] and src.get("686.py",{}).get("git_blob")==LOCKS["test686_blob"]
            and src.get("HIPPOCAMPUS_1.4_part1.py",{}).get("sha256")==LOCKS["v14_part1_sha256"] and E["SHA560"]==LOCKS["test560_blob"]
            and E["SHA659"]==LOCKS["test659_blob"] and P["verify"]["frozen_before"]["trainable_tensors"]==0 and P["verify"]["sentinel_before"]==E["S0"])
        P["verify"]["engine_locks_ok"]=bool(ok)
        if not ok:raise RuntimeError("engine lock check failed")
        emit(2,STAGE_TITLES[1],f"TEST684 blob {LOCKS['test684_blob'][:12]}… · TEST686 blob {LOCKS['test686_blob'][:12]}… · TEST560 {LOCKS['test560_blob'][:12]}… · TEST659 {LOCKS['test659_blob'][:12]}… · "
             f"v1.4 protocol SHA-256 {LOCKS['v14_part1_sha256'][:12]}… · weights frozen · sentinel unchanged · all-parameter guard recorded")
        stage=3
        for scn in ("AKBASCORE","MATRIX"):
            ids=E["keys686"](scn,"ABC");cf=E["keys686"](scn,"ABC_CF")
            P["scenarios"][scn]=dict(title=E["MISTRAL_EDITED"][scn]["title"],texts=scenario_texts(scn),edited=scenario_edited(scn),scored=not scenario_edited(scn),
                                     cartridge_ids=dict(A=ids[0],B=ids[1],C=ids[2],C_CF=cf[2]),
                                     text_sha256={s:sha_bytes(t.encode("utf-8")) for s,t in scenario_texts(scn).items()},
                                     queries=list(E["SCENARIOS686"][scn]["queries"]),hop_prompts=list(E["SCENARIOS686"][scn]["hop_prompts"]),
                                     body_tokens={s:len(E["CAR"][E["CASES686"][scn][s]]["body"]) for s in ("A","B","C","C_CF")})
        emit(3,STAGE_TITLES[2],"Two scenarios × cartridges A, B, C and the counterfactual C registered with the engine's register678() (TEST560 source formatting, canonical-prefix check; edited: "
             +", ".join(f"{s} {P['scenarios'][s]['edited']}" for s in P["scenarios"])+")")
        stage=4
        for scn in ("AKBASCORE","MATRIX"):P["builds"][scn]=measure_build(scn,"ABC")
        b=P["builds"]["AKBASCORE"];m=P["builds"]["MATRIX"]
        emit(4,STAGE_TITLES[3],f"AKBASCORE ABC: {b['memory']['T']} rows × {b['memory']['layers']} layers ({b['memory']['bytes']/2**20:.2f} MiB) built in {1000*b['build_seconds']:.0f} ms · "
             f"MATRIX ABC: {m['memory']['T']} rows ({m['memory']['bytes']/2**20:.2f} MiB) in {1000*m['build_seconds']:.0f} ms")
        stage=5
        def ok_s(x):return all(s["prior_rows_bitwise_unchanged"] for s in x["steps"][1:]) and all(s["lower_rows_equal_cartridge"] for s in x["steps"]) and x["engine_path_identical"] and x["reference_path_identical"]
        emit(5,STAGE_TITLES[4],f"H{CUT} residual transplanted at the layer-{CUT} output in zero-embedding forwards; K/V of layers 0–{CUT} re-phased and joined by the native CUDA append kernel. "
             f"Prior rows bitwise unchanged, layers 0–{CUT} rows = cartridge rows, step-wise memory = memory678(DC_CUT6_NATIVE) = TEST560 reference path: AKBASCORE {ok_s(b)} · MATRIX {ok_s(m)}")
        stage=6
        for scn in ("AKBASCORE","MATRIX"):
            r=recorded_run(scn,"ABC",REP_MAIN,include_staged=True);P["primary"][scn]=r;P["controls"].append(r)
        cq=(ctl.get("custom") or "").strip()
        if cq:P["custom"]=recorded_run(ctl["scenario"],ctl["condition"],ctl["representation"],question=cq[:2000],include_staged=False)
        a=P["primary"]["AKBASCORE"];mm=P["primary"]["MATRIX"]
        emit(6,STAGE_TITLES[5],f"AKBASCORE ABC DC_CUT6_NATIVE: {len(a['responses'])} questions · staged result '{a['staged']['answer']}' · MATRIX: {len(mm['responses'])} questions · staged result '{mm['staged']['answer']}'"
             +(f" · custom question answered ({ctl['scenario']} {ctl['condition']} {ctl['representation']})" if cq else ""))
        stage=7
        reps=(REP_MAIN,"TEXT_JOINT") if ctl.get("text_controls",True) else (REP_MAIN,)
        todo=[(s,c,r) for r in reps for s in ("AKBASCORE","MATRIX") for c in CONDITIONS if not (r==REP_MAIN and c=="ABC")]
        for i,(s,c,r) in enumerate(todo,1):
            P["controls"].append(recorded_run(s,c,r,include_staged=True))
            if i%3==0 or i==len(todo):emit(7,STAGE_TITLES[6],f"controls {i}/{len(todo)} · last: {s} {c} {r}",i==len(todo))
        stage=8
        P["verify"]["sentinel_after"]=E["sentinel"]();P["verify"]["guard_after"]=param_guard(E["model"]);P["verify"]["frozen_after"]=frozen_state()
        P["verify"]["guard_unchanged"]=P["verify"]["guard_after"]==P["verify"]["guard_before"]==STARTUP.get("guard_start")
        P["verify"]["sentinel_unchanged"]=P["verify"]["sentinel_after"]==P["verify"]["sentinel_before"]==E["S0"]
        P["verify"]["all_runs_frozen"]=all(r["weights_frozen"] and r["sentinel_unchanged"] for r in P["controls"]+([P["custom"]] if P["custom"] else []))
        emit(8,STAGE_TITLES[7],f"sentinel before = after = load: {P['verify']['sentinel_unchanged']} · all-parameter guard unchanged: {P['verify']['guard_unchanged']} · "
             f"trainable tensors {P['verify']['frozen_after']['trainable_tensors']} · residual hooks {len(P['verify']['frozen_after']['residual_hooks'])} · {len(P['controls'])} engine runs")
        stage=9
        for r in P["controls"]+([P["custom"]] if P["custom"] else []):
            p=r.get("engine_json")
            r["engine_json_sha256"]=sha_file(p) if p and Path(p).is_file() else None
        P["finished_utc"]=utc_now();P["elapsed_seconds"]=round(time.perf_counter()-t0,2)
        figs=render_all(P,run_dir,lambda k:emit(9,STAGE_TITLES[8],f"figure {k}/{N_FIGS} rendered",k==N_FIGS))
        stage=10
        files=package(P,run_dir,figs)
        emit(10,STAGE_TITLES[9],f"{len(files['all'])} files · SHA-256 manifest · ZIP {Path(files['zip']).stat().st_size/2**20:.1f} MiB")
        return dict(P=P,run_dir=run_dir,figures=figs,zip=files["zip"],files=files)
    except Exception as ex:
        P["errors"].append(dict(stage=stage,title=STAGE_TITLES[stage-1] if stage else "init",error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc(),utc=utc_now()))
        try:dump_json(run_dir/"ERRORS.json",P["errors"]);dump_json(run_dir/"PARTIAL_PAYLOAD.json",P)
        except Exception:pass
        raise StageError(stage,ex)

def answers_table(P):
    rows=[]
    for r in P["controls"]+([P["custom"]] if P["custom"] else []):
        for q in r["responses"]:
            rows.append(dict(scenario=r["scenario"],condition=r["condition"],representation=r["representation"],kind="question",id=q["question_id"],question=q["question"],
                             raw_answer=q["answer"],status=q["status"],descriptive_audit=q.get("descriptive_audit"),expected=q.get("expected"),generated_tokens=q.get("generated_tokens"),limit_reached=q.get("limit_reached"),
                             seconds=q.get("elapsed_seconds"),engine_run_sha256=r["run_sha256"]))
        if r["staged"]:
            for t in r["staged"]["trace"]:
                rows.append(dict(scenario=r["scenario"],condition=r["condition"],representation=r["representation"],kind="staged_hop",id=f"HOP{t['hop']}",question=t["question"],
                                 raw_answer=t["answer"],status=t["status"],descriptive_audit=t.get("descriptive_audit"),expected=t.get("expected"),generated_tokens=t.get("generated_tokens"),limit_reached=t.get("limit_reached"),
                                 seconds=t.get("elapsed_seconds"),engine_run_sha256=r["run_sha256"]))
            rows.append(dict(scenario=r["scenario"],condition=r["condition"],representation=r["representation"],kind="staged_result",id="CHAIN",question="(three-step chain)",
                             raw_answer=r["staged"]["answer"],status=r["staged"]["chain_status"],expected=r["staged"].get("chain_expected"),engine_run_sha256=r["run_sha256"]))
    return rows

def status_counts(P,rep):
    out={}
    for scn in ("AKBASCORE","MATRIX"):
        c=Counter()
        for r in P["controls"]:
            if r["scenario"]==scn and r["representation"]==rep:
                for q in r["responses"]:c[q["status"]]+=1
                if r["staged"]:c[r["staged"]["chain_status"]]+=1
        out[scn]=dict(c)
    return out

def summary_text(P):
    L=[];S="="*110;st=P["startup"]
    L+=[S,APP_TITLE,APP_SUB,S,f"run {P['run_id']} · started {P['started_local']} ({P['started_utc']} UTC) · finished {P.get('finished_utc')} · {P.get('elapsed_seconds')} s",
        f"model {st.get('model_id')} · {st.get('dtype')} · {st.get('attn')} · {st.get('gpu')} · torch {st.get('torch')} · transformers {st.get('transformers')} · gradio {st.get('gradio')}",
        "locked sources: "+" · ".join(f"{k} blob {v.get('git_blob')} sha256 {v.get('sha256')}" for k,v in (st.get('sources') or {}).items()),
        f"architecture {st.get('arch')} · CUT{st.get('cut')} · prefix {st.get('prefix_tokens')} tokens · max new tokens {st.get('max_new')}",
        f"full-weight SHA-256 {st.get('full_weight_sha256')} (recorded at start-up; no published Mistral reference exists)",
        f"sentinel unchanged: {P['verify'].get('sentinel_unchanged')} · all-parameter guard unchanged: {P['verify'].get('guard_unchanged')} · all runs frozen: {P['verify'].get('all_runs_frozen')}",S]
    for scn,b in P["builds"].items():
        L.append(f"[{scn}] measured DC_CUT6_NATIVE build (ABC): {b['memory']['T']} rows · {b['memory']['bytes']} bytes · memory SHA-256 {b['memory']['sha256']} · engine path identical {b['engine_path_identical']} · = TEST560 reference path {b['reference_path_identical']}")
        for c_,s_ in zip(b["cartridges"],b["steps"]):
            L.append(f"   {c_['slot']} #{c_['cartridge_id']} body {c_['body_tokens']} tok · rows {c_['rows_in_memory']} · H{b['cut']} {c_['h_shape']} · K/V L0–{b['cut']} {c_['kv_lower_shape']} · {c_['cartridge_bytes']} B · "
                     f"{s_['kind']} {1000*s_['seconds']:.1f} ms · prior rows unchanged {s_['prior_rows_bitwise_unchanged']} · L0–{b['cut']} rows = cartridge {s_['lower_rows_equal_cartridge']}")
        L.append(f"   final question on the measured memory → {b['final_answer_on_measured_memory']!r}")
    L.append(S)
    for r in P["controls"]:
        L.append(f"[{r['scenario']} · {r['condition']} · {r['representation']}] engine run SHA-256 {r['run_sha256']} · scored {r['scored']}")
        for q in r["responses"]:
            L.append(f"   {q['question_id']:<11} {q['status']:<19} raw={q['answer']!r}"+(" [16-token limit reached]" if q.get("limit_reached") else "")+f" · descriptive {q.get('descriptive_audit')}")
        if r["staged"]:
            L.append("   STAGED      "+" → ".join(repr(t["answer"]) for t in r["staged"]["trace"])+f" · chain {r['staged']['chain_status']}")
    if P["custom"]:
        c=P["custom"];L+=[S,f"custom question ({c['scenario']} {c['condition']} {c['representation']}, unscored): {c['custom_question']!r} → {c['responses'][0]['answer']!r}"]
    L+=[S,"Scope: fictional scenarios · predefined external three-step question sequence (not autonomous planning) · 16-token generation limit ·",
        "expected answers are audit metadata used only after generation · hashes show file identity, not correctness · TEST686 values are a sealed earlier record; Qwen v1.4 values are a different model.",S]
    return "\n".join(L)

def package(P,run_dir,figs):
    files=[]
    for f in figs:files.append(Path(f))
    files.append(dump_json(run_dir/"PAYLOAD.json",P))
    files.append(dump_json(run_dir/"RAW_MODEL_ANSWERS.json",answers_table(P)))
    files.append(dump_json(run_dir/"CONDITIONS.json",dict(conditions=CONDITIONS,representations=REPRESENTATIONS,scoring=SCORING,aliases=ALIASES,
              note="requirement sets and expected answers are audit metadata used only after generation; edited cartridges are unscored; strict TEST686 status is the score, the TEST684 descriptive audit is a secondary observation")))
    files.append(dump_json(run_dir/"CARTRIDGES.json",P["scenarios"]))
    files.append(dump_json(run_dir/"MEASUREMENTS.json",dict(builds=P["builds"],verify=P["verify"],startup=P["startup"])))
    files.append(dump_json(run_dir/"ERRORS.json",P["errors"]))
    sp=run_dir/"RUN_SUMMARY.txt";sp.write_text(summary_text(P),encoding="utf-8");files.append(sp)
    ed=run_dir/"engine_runs";ed.mkdir(exist_ok=True)
    for r in P["controls"]+([P["custom"]] if P["custom"] else []):
        p=r.get("engine_json")
        if p and Path(p).is_file():
            d=ed/Path(p).name;shutil.copy2(p,d);files.append(d)
    man={str(p.relative_to(run_dir)):dict(sha256=sha_file(p),bytes=p.stat().st_size) for p in files}
    mp=dump_json(run_dir/"SHA256_MANIFEST.json",dict(run_id=P["run_id"],created_utc=utc_now(),files=man));files.append(mp)
    zp=run_dir/f"{P['run_id']}_AKBASCORE_MAM_v1_4.zip"
    with zipfile.ZipFile(zp,"w",zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,arcname=str(p.relative_to(run_dir)))
    with zipfile.ZipFile(zp) as z:
        bad=z.testzip()
        if bad:raise RuntimeError(f"ZIP check failed at {bad}")
    return dict(all=[str(p) for p in files],zip=str(zp),manifest=str(mp),summary=str(sp),payload=str(run_dir/"PAYLOAD.json"))
