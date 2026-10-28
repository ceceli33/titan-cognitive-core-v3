# ===== PART 2/4 — paste directly after PART 1 in the same cell =====
# =====================================================================================================================
# PART 2 / 4 — the records of THIS run (engine files first, the live engine output as fallback), the independent
#              read-only verification, descriptive host statistics of the sealed cartridges, and the figure toolkit
#              (JPEG 300 dpi, layout QC). Nothing here routes, reads, decides or writes memory — that is the engine's work.
# THIS PART  30,350 characters · its last line is  # ===== END OF PART 2/4 =====
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
        # 815.py runs its locked prelude first (it prints the 709/730/757/721/764 lock checks), then opens its own log with
        # LOG.write_text('') — so TEST815.log starts at the engine's first log line and never holds the prelude gates. The
        # comparison is therefore anchored at that first line: from there on, every gate of the live stdout must equal the
        # engine's file one to one, in order; before it, only the prelude's lock gates are allowed. Nothing else is accepted.
        G_=("PASS ","FAIL ");PRE=("PASS SOURCE_SIZE_","PASS GIT_LOCK_","PASS SYMBOLS_","PASS ENGINE_DEPENDENCIES")
        elines=[l.rstrip() for l in (tload(root/"TEST815.log") or "").splitlines() if l.strip()];el=[l for l in elines if l.startswith(G_)]
        live=[l.rstrip() for _,st_,l in LINES if st_=="stdout"];ll=[l for l in live if l.startswith(G_)]
        first=elines[0] if elines else None;b=live.index(first) if first in live else None
        pre=[l for l in live[:b] if l.startswith(G_)] if b is not None else [];post=[l for l in live[b:] if l.startswith(G_)] if b is not None else ll
        import difflib
        miss,extra,diff=[],[],[]
        for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,post,el,autojunk=False).get_opcodes():
            if op=="delete":miss+=post[i1:i2]
            elif op=="insert":extra+=el[j1:j2]
            elif op=="replace":diff+=[dict(live=a,engine_log=c) for a,c in zip(post[i1:i2],el[j1:j2])];miss+=post[i1+(j2-j1):i2];extra+=el[j1+(i2-i1):j2]
        bad_pre=[l for l in pre if not l.startswith(PRE)]
        R["engine_log_gates"]=len(el);R["live_gates"]=len(ll)
        R["engine_log_comparison"]=dict(engine_log_first_line=first,anchor_found_in_live_output=b is not None,live_gates_before_anchor=len(pre),
            live_gates_before_anchor_are_prelude_lock_gates=not bad_pre,live_gates_from_anchor=len(post),engine_log_gates=len(el),
            missing_in_engine_log=miss[:50],extra_in_engine_log=extra[:50],different=diff[:50],unexpected_before_anchor=bad_pre[:50],
            counts=dict(missing=len(miss),extra=len(extra),different=len(diff),unexpected_before_anchor=len(bad_pre)),
            prelude_gates_before_anchor=pre[:50])
        R["engine_log_gates_equal_live"]=bool(el) and b is not None and post==el and not bad_pre and len(pre)+len(post)==len(ll)
        if not R["engine_log_gates_equal_live"]:slog("ENGINE_LOG_DIFF","TEST815.log vs live engine output",**R["engine_log_comparison"]["counts"],anchor=first,anchor_found=b is not None)
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
