# =====================================================================================================================
# ===== PART 2/3 — paste directly after PART 1 in the same cell =====
# PART 2 / 3 — Cartridge Operations, Memory Consolidation, Integrity and Research Figures
# Every memory operation calls the TEST709 engine functions (E["cart_load"], E["initialize"], E["append"], E["answer"],
# E["sentinel"], E["ensure_room"]) in the order used by TEST709 trial(). Nothing here changes CUT3, RoPE re-phasing, the
# cartridge format, the K/V layout, the SHA-256 guards or the GPU reserve. Measurements are read-only.
# All live values come from this session's engine record E["R"], its live engine log and this session's measurements.
# The published 709.log is parsed ONLY for the separately labelled historical reference.
# =====================================================================================================================
COMBOS=["A+B+C","A+C+B","B+A+C","B+C+A","C+A+B","C+B+A","A+B","B+A","A+C","C+A","B+C","C+B","A","B","C"]
def combo_books(c):return [x for x in str(c).split("+") if x]

class OpError(RuntimeError):pass
def _torch():return E["torch"]
def gpu_now():
    try:return E["mem"]()
    except Exception as ex:return {"error":f"{type(ex).__name__}: {ex}"}
def _append_pass_count():return sum(1 for l in engine_log_text().splitlines() if l.startswith("PASS APPEND_ALL_80_LAYERS_EXACT_SHA256"))

def _require(forged=True):
    if not ENGINE["model_ready"]:raise OpError("The frozen model is not loaded in this session.")
    if forged and not ENGINE["forged"]:raise OpError("The cartridges have not been forged in this session.")

def _drop_memory(reason):
    """release the interactive memory; the list is exclusively owned by STATE"""
    had=STATE["memory"] is not None
    STATE["memory"]=None;STATE["order"]=[];STATE["stages"]=[]
    try:E["free_gpu"]()
    except Exception:pass
    if had:slog("MEMORY_RELEASED",reason,gpu=gpu_now())

def _mount_one(bid,label):
    """one TEST709 trial() stage, step for step (709.py lines 221–225): cart_load → initialize|append → release →
    synchronize → timing fields. On any error the partially consumed memory is discarded (append() has already
    released the caller's references), the GPU is freed and the error is reported — never hidden."""
    torch=_torch();memory=STATE["memory"];n0=_append_pass_count()
    cp,times=E["cart_load"](bid);t0=time.perf_counter()
    new=list(E["initialize"](cp)) if memory is None else E["append"](memory,cp)
    del memory;STATE["memory"]=new;del new,cp;E["free_gpu"]();torch.cuda.synchronize()
    times["rebuild_ms"]=round((time.perf_counter()-t0)*1000,3);times["end_to_end_ms"]=round(times["ssd_load_ms"]+times["h2d_ms"]+times["rebuild_ms"],3)
    times["book"]=bid;times["cache_tokens"]=int(STATE["memory"][0][0].shape[-2]);times["gpu"]=E["mem"]()
    times["operation"]="initialize" if not STATE["order"] else "append";times["label"]=label;times["utc"]=utc_now()
    # evidence, not assumption: the engine wrote one new 'PASS APPEND_ALL_80_LAYERS_EXACT_SHA256' line for this append
    times["prior_kv_sha256_pass_line"]=(_append_pass_count()==n0+1) if times["operation"]=="append" else None
    STATE["order"].append(bid);STATE["stages"].append(times);STATE["ops"].append(dict(times))
    slog("HOT_SWAP_TIMING",f"{label} {bid}",**times)
    return times

def _guard_order(books):
    if not books:raise OpError("Select at least one cartridge.")
    if len(set(books))!=len(books):raise OpError("A cartridge can be mounted only once in a memory.")
    if any(b not in ("A","B","C") for b in books):raise OpError("Unknown cartridge.")
    if len(books)>3:raise OpError("At most three cartridges (TEST709 capacity budget).")

def build_memory(books,label=None):
    """build a new memory from SSD in the given order (TEST709: each memory starts from an empty memory).
    TEST709 memory is append-only, so changing the selection always means release + rebuild."""
    with ENGINE_LOCK:
        _require();_guard_order(books);label=label or "SESSION_"+"_PLUS_".join(books)
        _drop_memory("new build requested");slog("BUILD_START",label,order=books,gpu=gpu_now())
        try:
            for bid in books:_mount_one(bid,label)
        except BaseException as ex:
            _drop_memory(f"build failed: {type(ex).__name__}")
            slog("BUILD_FAILED",label,error=f"{type(ex).__name__}: {ex}",engine_log=engine_log_new_lines()[-15:]);raise
        slog("BUILD_DONE",label,order=STATE["order"],cache_tokens=STATE["stages"][-1]["cache_tokens"],engine_log=engine_log_new_lines()[-15:])
        return list(STATE["stages"])

def release_memory():
    with ENGINE_LOCK:_drop_memory("release requested");return gpu_now()

def ask(question,use_memory=True,origin="user"):
    """question answering exactly as TEST709 trial(): ensure_room(512) then answer(memory, question).
    use_memory=False asks the same frozen model with NO memory (the TEST709 NO_CARTRIDGE path) as a control."""
    with ENGINE_LOCK:
        _require(forged=use_memory)
        q=(question or "").strip()
        if not q or len(q)>2000:raise OpError("The question must contain 1–2000 characters.")
        if use_memory and STATE["memory"] is None:raise OpError("No cartridge memory is mounted.")
        E["ensure_room"](512);t=time.perf_counter()
        raw=E["answer"](STATE["memory"] if use_memory else None,q)
        row=dict(utc=utc_now(),origin=origin,question=q,raw=raw,memory_order=list(STATE["order"]) if use_memory else [],with_memory=bool(use_memory),
                 cache_tokens=(int(STATE["memory"][0][0].shape[-2]) if (use_memory and STATE["memory"] is not None) else 0),
                 seconds=round(time.perf_counter()-t,3),gpu=E["mem"](),max_new_tokens=E["MAX_NEW"],semantics="UNSCORED")
        (STATE["qa"] if use_memory else STATE["controls"]).append(row)
        with SESSION_QA.open("a",encoding="utf-8") as f:f.write(json.dumps(jsafe(row),ensure_ascii=False)+"\n")
        slog("QA" if use_memory else "QA_CONTROL",f"{'+'.join(row['memory_order']) or 'NO MEMORY'}",question=q,raw=raw,seconds=row["seconds"],origin=origin)
        return row

def protocol_questions():
    seen=[]
    for t in _SEG["trials"]:
        for q in t["questions"]:
            if q not in seen:seen.append(q)
    return seen
def run_controls():
    """every scripted protocol question asked again with NO memory — same frozen model, same decoding"""
    _drop_memory("controls run without memory")
    qs=protocol_questions()
    for i,q in enumerate(qs,1):
        r=ask(q,False,origin="initialization control");print(f"  control {i}/{len(qs)} · {r['seconds']:.1f} s · {q[:70]!r} → {r['raw'][:90]!r}",flush=True)
    return dict(questions=len(qs))

# ---------------------------------------------------------------------------------------------------------------------
# live integrity checks
# ---------------------------------------------------------------------------------------------------------------------
def verify_weights():
    """weight sentinel of the engine (709.py sentinel(): sampled bytes of 5 o_proj + norm + lm_head) recomputed now and
    compared with R['weight_sentinel_before'] taken right after loading — read-only, R is not modified"""
    with ENGINE_LOCK:
        _require(forged=False);t=time.perf_counter()
        after=E["sentinel"]();before=E["R"].get("weight_sentinel_before")
        row=dict(utc=utc_now(),passed=(before is not None and after==before),before=before,after=after,seconds=round(time.perf_counter()-t,2))
        STATE["weight_checks"].append(row);slog("WEIGHT_CHECK","PASS" if row["passed"] else "FAIL",**row);return row

def verify_disk():
    """recompute SHA-256 of the three cartridge files and compare with the values the engine recorded when it saved
    them in this session"""
    with ENGINE_LOCK:
        _require();rows=[];t=time.perf_counter()
        for b in E["R"]["books"]:
            p=Path(E["CART"])/(b["id"]+".pt");h=sha_file(p) if p.is_file() else None
            rows.append(dict(book=b["id"],file=str(p),bytes=(p.stat().st_size if p.is_file() else None),sha256=h,engine_record_sha256=b.get("cartridge_sha256"),equals_engine_record=(h is not None and h==b.get("cartridge_sha256"))))
        row=dict(utc=utc_now(),files=rows,passed=(len(rows)==3 and all(r["equals_engine_record"] for r in rows)),seconds=round(time.perf_counter()-t,2))
        STATE["disk_checks"].append(row);slog("DISK_CHECK","PASS" if row["passed"] else "FAIL",**row);return row

# ---------------------------------------------------------------------------------------------------------------------
# READ-ONLY memory X-ray of the live GPU K/V tensors (required for Figure 4 — no synthetic heat map is ever drawn)
# ---------------------------------------------------------------------------------------------------------------------
def xray_measure(bin_tokens=256,chunk=4096):
    """per layer and per token bin: mean over KV heads of the L2 norm of each K and V row of the live memory.
    Reads the tensors in small FP32 chunks; never writes to them; keeps no reference after returning."""
    with ENGINE_LOCK:
        _require()
        if STATE["memory"] is None:raise OpError("No memory is mounted.")
        torch=_torch();E["ensure_room"](0);t=time.perf_counter();mem_=STATE["memory"]
        T=int(mem_[0][0].shape[-2]);NL=len(mem_);nb=(T+bin_tokens-1)//bin_tokens
        Kb=np.zeros((NL,nb),dtype=np.float64);Vb=np.zeros((NL,nb),dtype=np.float64)
        with torch.no_grad():
            for li,(k,v) in enumerate(mem_):
                for arr,out in ((k,Kb),(v,Vb)):
                    rows=[]
                    for st in range(0,T,chunk):rows.append(arr[0,:,st:st+chunk,:].float().norm(dim=-1).mean(dim=0).cpu().numpy())
                    r=np.concatenate(rows);pad=nb*bin_tokens-T
                    if pad:r=np.concatenate([r,np.full(pad,np.nan)])
                    out[li]=np.nanmean(r.reshape(nb,bin_tokens),axis=1)
        del mem_
        segs=[];a=0
        for s in STATE["stages"]:segs.append(dict(book=s["book"],start=a,end=s["cache_tokens"]));a=s["cache_tokens"]
        x=dict(utc=utc_now(),order=list(STATE["order"]),tokens=T,layers=NL,kv_heads=E["KVH"],bin_tokens=bin_tokens,cut=E["CUT"],prefix_tokens=E["P"],segments=segs,
               k_norm=Kb.round(5).tolist(),v_norm=Vb.round(5).tolist(),finite=bool(np.isfinite(Kb).all() and np.isfinite(Vb).all()),
               seconds=round(time.perf_counter()-t,2),gpu=E["mem"](),
               method=f"mean over {E['KVH']} KV heads of the L2 norm per K/V row; mean per bin of {bin_tokens} tokens; FP32 copies of {chunk}-row chunks; read-only")
        STATE["xray"]=x;dump_json(SESSION_DIR/"XRAY_MEASUREMENT.json",x)
        slog("XRAY_MEASURED","+".join(x["order"]),tokens=T,bins=nb,finite=x["finite"],seconds=x["seconds"]);return x

# ---------------------------------------------------------------------------------------------------------------------
# historical reference only: the published 709.log (earlier run) and 706/707/708.log — never shown as live results
# ---------------------------------------------------------------------------------------------------------------------
def _split_qa(rest):
    """'<repr question> -> <repr answer>' with possible ' -> ' inside the strings"""
    for m in re.finditer(r" -> ",rest):
        a,b=rest[:m.start()],rest[m.end():]
        try:return ast.literal_eval(a),ast.literal_eval(b)
        except Exception:continue
    return None,None
def parse_709_log(txt):
    L=dict(checks=[],saved={},trials=OrderedDict(),appends=0,status=None)
    for line in txt.splitlines():
        for name in re.findall(r"\bPASS ([A-Z0-9_]+)",line):L["checks"].append(name)
        m=re.match(r"SAVED (\w) FILE_BYTES (\d+) SHA256 ([0-9a-f]{64})",line)
        if m:L["saved"][m.group(1)]=dict(bytes=int(m.group(2)),sha256=m.group(3));continue
        m=re.match(r"HOT_SWAP_TIMING (\S+) (\w) (\{.*\})$",line)
        if m:L["trials"].setdefault(m.group(1),dict(stages=[],qa=[]))["stages"].append(ast.literal_eval(m.group(3)));continue
        m=re.match(r"QA (\S+) (.*)$",line)
        if m:
            q,a=_split_qa(m.group(2))
            if q is not None:L["trials"].setdefault(m.group(1),dict(stages=[],qa=[]))["qa"].append(dict(question=q,raw=a))
            continue
        if line.startswith("PASS APPEND_ALL_80_LAYERS_EXACT_SHA256"):L["appends"]+=1
        m=re.match(r"TEST\d+_STATUS (\S+)",line)
        if m:L["status"]=m.group(1)
    return L
def parse_failure_log(name,txt):
    st=re.search(r"TEST(\d+)_STATUS (\S+)",txt);err=re.search(r"^ERROR (\w+) (.*)$",txt,re.M)
    forg=re.search(r"FORGING A TOKENS (\d+)",txt);head=re.search(r"AKBASCORE (TEST\S+)",txt)
    return dict(file=name,label=(head.group(1) if head else name),status=(st.group(2) if st else None),error=(f"{err.group(1)}: {err.group(2)}" if err else None),
                tokens_per_book=(int(forg.group(1)) if forg else None))
HIST709={};CHRONO=[]
def load_evidence():
    """verified historical files: copied byte-identically into the session folder under a name that says what they are"""
    global HIST709,CHRONO
    raw=fetch_locked("709.log");HIST709=parse_709_log(raw.decode("utf-8","replace"))
    (HIST_DIR/"HISTORICAL_TEST709_published_709.log").write_bytes(raw)
    CHRONO=[]
    for n in ("706.log","707.log","708.log"):
        try:
            r=fetch_locked(n);CHRONO.append(parse_failure_log(n,r.decode("utf-8","replace")));(HIST_DIR/("HISTORICAL_"+n)).write_bytes(r)
        except Exception as ex:CHRONO.append(dict(file=n,label=n,status="NOT VERIFIED",error=f"{type(ex).__name__}: {ex}"))
    CHRONO.append(dict(file="709.log",label="TEST708-R2 (709.py)",status=HIST709["status"],error=None,tokens_per_book=None))
    (HIST_DIR/"README_HISTORICAL.txt").write_text(
        "These files are PUBLISHED RECORDS OF EARLIER RUNS, verified against their git blob identifiers.\n"
        "They are NOT results of this session. Live results of this session are in ../live_engine/ and the session files.\n"
        +"".join(f"{n}: git blob {LOCKS[n]}\n" for n in ("709.log","706.log","707.log","708.log")),encoding="utf-8")
    slog("HISTORICAL_LOADED","published 709.log verified (reference only, not this session)",status=HIST709["status"],chronology=[(c["label"],c["status"]) for c in CHRONO])
    return dict(historical_status=HIST709["status"])
def sources_step():
    load_engine_source();h=load_evidence()
    try:fetch_locked("LICENSE");(SESSION_DIR/"LICENSE.txt").write_bytes((EVIDENCE_DIR/"LICENSE").read_bytes())
    except Exception as ex:raise RuntimeError(f"LICENSE could not be verified: {type(ex).__name__}: {ex}")
    return dict(sources={k:v["git_blob"] for k,v in SOURCES.items()},**h)

# ---------------------------------------------------------------------------------------------------------------------
# LIVE record of this session (from the engine's own record R and its live log) + verification
# ---------------------------------------------------------------------------------------------------------------------
def live_record():
    R=E["R"]
    return dict(status=R.get("status"),checks=[dict(c) for c in R["checks"]],budget=R.get("budget") or {},env=R.get("env") or {},model_revision=R.get("model_revision"),
                trials=OrderedDict((t["label"],dict(books=list(t["active"]),stages=t["stages"],qa=t["qa"],cache_tokens=t["cache_tokens"],seconds=t["seconds"])) for t in R["trials"]),
                saved={b["id"]:dict(bytes=b.get("cartridge_file_bytes"),sha256=b.get("cartridge_sha256")) for b in R["books"]},
                sources={b["id"]:dict(bytes=b.get("source_bytes"),sha256=b.get("source_sha256"),title=b.get("title")) for b in R["books"]},
                forge_tokens={b["id"]:b.get("requested_tokens") for b in R["books"]},appends=list(ENGINE.get("protocol_append_pass_lines",[])),
                elapsed_s=R.get("elapsed_s"),model_load_s=R.get("model_load_s"))

def historical_comparison(L):
    """reproducibility comparison of this live run with the published earlier run — reference only, never used for READY"""
    if not HIST709:return dict(available=False)
    sha={b:(L["saved"].get(b,{}).get("sha256")==HIST709["saved"].get(b,{}).get("sha256")) for b in ("A","B","C")}
    ans={}
    for lab,t in L["trials"].items():
        h=HIST709["trials"].get(lab)
        if h:ans[lab]=[r["raw"] for r in t["qa"]]==[r["raw"] for r in h["qa"]]
    rows={lab:([s["cache_tokens"] for s in t["stages"]]==[s["cache_tokens"] for s in HIST709["trials"].get(lab,{}).get("stages",[])]) for lab,t in L["trials"].items() if lab in HIST709["trials"]}
    return dict(available=True,note="published 709.log = earlier run; comparison only, not part of the READY decision",historical_status=HIST709["status"],
                cartridge_sha256_identical=sha,trial_answers_identical=ans,trial_rows_identical=rows)

def compute_verification():
    L=live_record();checks=L["checks"];names={c["name"] for c in checks};items=[]
    def add(name,ok,detail):items.append(dict(name=name,passed=bool(ok),detail=jsafe(detail)))
    add("ENGINE_STATUS_LIVE",L["status"]==ENGINE_PASS_STATUS,L["status"])
    add("ALL_ENGINE_CHECKS_PASSED",bool(checks) and all(c["pass"] for c in checks),f"{sum(1 for c in checks if c['pass'])}/{len(checks)} passed")
    miss=[n for n in REQUIRED_ENGINE_CHECKS if n not in names];add("REQUIRED_ENGINE_CHECKS_PRESENT",not miss,miss or f"{len(REQUIRED_ENGINE_CHECKS)} present")
    labels=list(L["trials"]);add("SCRIPTED_TRIALS_COMPLETE",labels==ENGINE["scripted_trials"],f"{len(labels)}/{len(ENGINE['scripted_trials'])} trials")
    pa=len(L["appends"]);add("PROTOCOL_APPENDS_EXACT_SHA256",pa==ENGINE["expected_protocol_appends"],f"{pa}/{ENGINE['expected_protocol_appends']} appends, all 80 layers")
    d=STATE["disk_checks"][-1] if STATE["disk_checks"] else None;add("CARTRIDGE_FILES_SHA256_ON_DISK",bool(d and d["passed"]),{r["book"]:r["equals_engine_record"] for r in (d or {}).get("files",[])})
    abc=L["trials"].get("A_PLUS_B_PLUS_C",{}).get("cache_tokens");st=STATE["stages"]
    ok=STATE["order"]==["A","B","C"] and bool(st) and st[-1]["cache_tokens"]==abc and all(s["prior_kv_sha256_pass_line"] for s in st[1:])
    add("READY_MEMORY_A_PLUS_B_PLUS_C",ok,dict(order=STATE["order"],rows=(st[-1]["cache_tokens"] if st else None),protocol_rows=abc,append_sha256_lines=[s["prior_kv_sha256_pass_line"] for s in st[1:]]))
    w=STATE["weight_checks"][-1] if STATE["weight_checks"] else None;add("WEIGHT_SENTINEL_UNCHANGED_AFTER_ALL_STEPS",bool(w and w["passed"]),(w or {}).get("after"))
    add("GPU_SAFETY_RESERVE_NOT_REDUCED",float(E["GPU_RESERVE_GIB"])>=EXPECTED_RESERVE_GIB,f"{E['GPU_RESERVE_GIB']} GiB")
    x=STATE["xray"];add("XRAY_FROM_LIVE_KV",bool(x and x["finite"] and x["layers"]==E["NL"] and st and x["tokens"]==st[-1]["cache_tokens"]),(f"{x['layers']} layers × {x['tokens']} rows" if x else None))
    qs=protocol_questions();got={r["question"] for r in STATE["controls"]};add("NO_MEMORY_CONTROLS_COMPLETE",all(q in got for q in qs),f"{sum(1 for q in qs if q in got)}/{len(qs)}")
    rec=dict(session=SESSION_ID,utc=utc_now(),ready=all(i["passed"] for i in items),passed=sum(i["passed"] for i in items),total=len(items),items=items,
             semantics="UNSCORED — physical reconstruction and integrity are measured; answer correctness is not scored; public-domain books (pretraining knowledge possible)",
             live_engine_status=L["status"],live_engine_elapsed_s=L["elapsed_s"],cartridges=L["saved"],historical_reference=historical_comparison(L))
    STATE["verification"]=rec;dump_json(VERIFY_FILE,rec);slog("VERIFICATION","READY" if rec["ready"] else "NOT READY",passed=rec["passed"],total=rec["total"],failed=[i["name"] for i in items if not i["passed"]])
    return rec

# ---------------------------------------------------------------------------------------------------------------------
# SIX RESEARCH FIGURES (JPEG full resolution, PNG lossless, PDF vector) — values ONLY from this live session
# ---------------------------------------------------------------------------------------------------------------------
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.linewidth":.9,"axes.edgecolor":"#374151","axes.labelcolor":"#111827",
                     "xtick.color":"#374151","ytick.color":"#374151","xtick.labelsize":10.5,"ytick.labelsize":10.5,"axes.labelsize":12,
                     "axes.titlesize":13,"axes.titleweight":"bold","axes.titlelocation":"left","legend.fontsize":10.5,"legend.frameon":False})
FW,FH=13.333,7.5;OUT_DPI=300
INK,INK2,MUTED,RULE,PANEL="#111827","#374151","#6B7280","#D1D5DB","#F8FAFC"
TEAL,RED,AMBER="#0F766E","#B91C1C","#B45309"
FIGURES=OrderedDict([
    ("F1","Figure 1 — Physical memory injection protocol"),("F2","Figure 2 — Silicon Hippocampus architecture: SSD cartridges vs live GPU memory"),
    ("F3","Figure 3 — Three-cartridge consolidation and performance"),("F4","Figure 4 — Internal neural memory X-ray"),
    ("F5","Figure 5 — Three books: memory and question answering (observational)"),("F6","Figure 6 — Integrity and verification record")])
FIG_FILES={};LIVE={}
def mt(s):return str(s).replace("$",r"\$")
def wrap(s,n):return "\n".join(textwrap.wrap(str(s),n,break_long_words=True,break_on_hyphens=False)) or ""
def short(s,n):s=" ".join(str(s).split());return s if len(s)<=n else s[:n-1].rstrip()+"…"
def _bb(fig,t):return t.get_window_extent(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())
def fit(fig,t,xmax=.965,xmin=None,minsize=6.5,trunc=False):
    # shrink a text object until it lies inside [xmin,xmax] (figure fraction); optionally shorten it (marked …) after that
    while t.get_fontsize()>minsize:
        b=_bb(fig,t)
        if b.x1<=xmax and (xmin is None or b.x0>=xmin):return t
        t.set_fontsize(t.get_fontsize()-.25)
    if trunc:
        s=t.get_text()
        while len(s)>3 and _bb(fig,t).x1>xmax:
            s=s.rstrip("…")[:-2].rstrip()+"…";t.set_text(s)
    return t
def ftext(fig,x,y,s,xmax=.965,xmin=None,minsize=6.5,trunc=False,**kw):return fit(fig,fig.text(x,y,mt(s),**kw),xmax,xmin,minsize,trunc)

def fig_base(k,title,subtitle,badge,badge_col,h=FH):
    fig=plt.figure(figsize=(FW,h),dpi=100,facecolor="white");s=FH/h
    b=fig.text(.965,1-.05*s,badge,fontsize=10.5,weight="bold",color=badge_col,va="center",ha="right",bbox=dict(boxstyle="square,pad=0.4",fc="white",ec=badge_col,lw=1.2))
    bx0=_bb(fig,b).x0-.015
    fig.text(.035,1-.05*s,f"Fig. {k}",fontsize=15,weight="bold",color=MUTED,va="center")
    ftext(fig,.095,1-.05*s,title,xmax=bx0,minsize=12,fontsize=18,weight="bold",color=INK,va="center")
    ftext(fig,.035,1-.095*s,subtitle,minsize=9,fontsize=12,color=INK2,va="center")
    fig.add_artist(Line2D([.035,.965],[1-.122*s,1-.122*s],transform=fig.transFigure,color=INK2,lw=.8))
    return fig
def fig_footer(fig,k,note,h=FH):
    s=FH/h
    fig.add_artist(Line2D([.035,.965],[.075*s,.075*s],transform=fig.transFigure,color=RULE,lw=.7))
    ftext(fig,.035,.05*s,note,minsize=8,fontsize=10,color=INK2,va="center")
    ftext(fig,.035,.022*s,f"{APP_SHORT} · {ORG} · {LICENSE_NAME} · {COPYRIGHT} · engine 709.py {LOCKS['709.py'][:10]} · live session {SESSION_ID} · Fig. {k}/6",
          minsize=6,fontsize=8.6,color=MUTED,va="center",family="DejaVu Sans Mono")
def box(fig,x,y,w,h,ec,fc="white",lw=1.6,r=.010):
    fig.add_artist(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={r}",transform=fig.transFigure,facecolor=fc,edgecolor=ec,lw=lw,zorder=1))
def arrow(fig,x0,y0,x1,y1,col=INK2,lw=1.8,ms=16,cs="arc3"):
    fig.add_artist(FancyArrowPatch((x0,y0),(x1,y1),transform=fig.transFigure,arrowstyle="-|>",mutation_scale=ms,lw=lw,color=col,connectionstyle=cs,zorder=5))
def save_fig(fig,key,k):
    stem=f"FIGURE_{k:02d}_{key}"
    jpg=FIG_DIR/(stem+".jpg");png=FIG_DIR/(stem+".png");pdf=FIG_DIR/(stem+".pdf")
    fig.savefig(pdf,facecolor="white");buf=io.BytesIO();fig.savefig(buf,format="png",dpi=OUT_DPI,facecolor="white");plt.close(fig)
    png.write_bytes(buf.getvalue())
    with Image.open(io.BytesIO(buf.getvalue())) as im:im.convert("RGB").save(jpg,"JPEG",quality=95,optimize=True,subsampling=0,dpi=(OUT_DPI,OUT_DPI))
    with Image.open(jpg) as c:
        if c.format!="JPEG" or c.size[0]<3000:raise RuntimeError("JPEG check failed "+str(jpg))
        size=c.size
    rec=dict(key=key,figure=k,title=FIGURES[f"F{k}"],jpg=str(jpg),png=str(png),pdf=str(pdf),pixels=list(size),jpg_bytes=jpg.stat().st_size,sha256_jpg=sha_file(jpg),utc=utc_now(),data="live session "+SESSION_ID)
    flog(f"FIGURE {k} {key} {size[0]}x{size[1]} jpg sha256 {rec['sha256_jpg']}");return rec

def _arch():
    a=engine_architecture()
    if not a:raise OpError("figures need the architecture measured by the engine in this session")
    return a
def _first_stage():
    st=(LIVE["trials"].get("A_ONLY") or {}).get("stages") or []
    if not st:raise OpError("figures need the live A_ONLY protocol trial")
    return st[0]
def _titles():return {b:LIVE["sources"].get(b,{}).get("title") or b for b in ("A","B","C")}

def fig1(k=1):
    a=_arch();ab=_first_stage();n=ab["cache_tokens"];cb=LIVE["saved"]["A"]["bytes"];kvb=a["full_kv_bytes_per_token"];c=a["cut"];L=a["layers"]
    fig=fig_base(k,"Physical memory injection protocol — Qwen2.5-72B-Instruct, CUT3",
                 f"{L} layers · hidden {a['hidden']:,} · {a['q_heads']} query / {a['kv_heads']} KV heads · head dim {a['head_dim']} · NF4 weights, BF16 K/V · frozen (measured in this session)",
                 "SCHEMATIC + LIVE VALUES",INK2)
    steps=[("1  FORGE",BOOK_COLORS["A"],f"The frozen model reads ONE book excerpt ({n:,} rows incl. prefix) in {a['chunk']}-token chunks."),
           ("2  PERSIST",INK2,f"Only H{c} and the K/V of layers 0–{c} are saved to SSD (.pt file + SHA-256)."),
           ("3  WRITE L0–L3",LOWER_COLOR,"Mount: lower-layer K/V rows come from the file; keys are re-phased (RoPE) when appended."),
           ("4  INJECT + REBUILD",UPPER_COLOR,f"Zero input embeddings; H{c} replaces the layer-{c} output; layers {c+1}–{L-1} recompute the rows."),
           ("5  ANSWER",BOOK_COLORS["A"],f"Only the question suffix is fed; greedy decoding, ≤ {a['max_new']} new tokens.")]
    w=.172;g=(.93-5*w)/4
    for i,(t,col,body) in enumerate(steps):
        x=.035+i*(w+g);box(fig,x,.62,w,.205,col,lw=2)
        fig.add_artist(FancyBboxPatch((x,.785),w,.04,boxstyle="round,pad=0,rounding_size=0.010",transform=fig.transFigure,facecolor=col,edgecolor=col,zorder=2))
        ftext(fig,x+.01,.805,t,xmax=x+w-.006,fontsize=12.5,weight="bold",color="white",va="center",zorder=3)
        ftext(fig,x+.01,.768,wrap(body,27),xmax=x+w-.006,fontsize=10.5,color=INK,va="top",linespacing=1.3)
        if i<4:arrow(fig,x+w+.002,.72,x+w+g-.002,.72,ms=16)
    x0=.08;W=.86;bw=W/L;y=.44;hh=.07
    for li in range(L):
        fig.add_artist(Rectangle((x0+li*bw+(.004 if li>c else 0),y),bw*.82,hh,transform=fig.transFigure,facecolor=LOWER_COLOR if li<=c else UPPER_COLOR,edgecolor="none",zorder=2))
    for li in (0,c,20,40,60,L-1):fig.text(x0+li*bw+bw*.41+(.004 if li>c else 0),y-.025,f"L{li}",fontsize=10,ha="center",color=INK2)
    xc=x0+(c+1)*bw+.0015;fig.add_artist(Line2D([xc,xc],[y-.012,y+hh+.03],transform=fig.transFigure,color=CUT_COLOR,lw=3,zorder=4))
    fig.text(xc+.006,y+hh+.035,f"◀ CUT{c}: H{c} injected here (layer-{c} output)",fontsize=12,weight="bold",color=CUT_COLOR)
    fig.text(x0,y-.065,f"L0–L{c}: K/V rows written from the cartridge file ({c+1} layers)",fontsize=12,weight="bold",color=LOWER_COLOR)
    fig.text(x0+W,y-.065,f"L{c+1}–L{L-1}: recomputed at every mount ({L-c-1} layers)",fontsize=12,weight="bold",color=UPPER_COLOR,ha="right")
    facts=[("Cartridge file (book A, this session)",f"{cb:,} B",f"H{c} [1, {n:,}, {a['hidden']:,}] + K/V of L0–L{c}: 4 × 2 × [1, {a['kv_heads']}, {n:,}, {a['head_dim']}]"),
           ("Full live K/V rebuilt by one mount",f"{n*kvb:,} B",f"{L} layers × {kvb:,} B per token"),
           ("First mount of book A (live protocol)",f"{ab['rebuild_ms']/1000:.1f} s rebuild",f"SSD read {ab['ssd_load_ms']/1000:.2f} s · host→GPU {ab['h2d_ms']:.0f} ms"),
           ("Prior K/V check at each append (live)",f"{len(LIVE['appends'])} × PASS",f"exact SHA-256 of every prior K/V byte, all {L} layers")]
    fw=(.93-3*.01)/4
    for i,(h1,v,sub) in enumerate(facts):
        x=.035+i*(fw+.01);box(fig,x,.11,fw,.2,RULE,fc=PANEL,lw=1)
        ftext(fig,x+.012,.285,h1,xmax=x+fw-.008,fontsize=11,weight="bold",color=INK2,va="top")
        ftext(fig,x+.012,.225,v,xmax=x+fw-.008,fontsize=17,weight="bold",color=INK,va="center")
        ftext(fig,x+.012,.175,wrap(sub,38),xmax=x+fw-.008,fontsize=10,color=INK2,va="top")
    fig_footer(fig,k,"Schematic illustration of the TEST709 path (layer strip not to scale). Every number was measured by the engine in this live session.")
    return save_fig(fig,"PHYSICAL_MEMORY_INJECTION_PROTOCOL",k)

def fig2(k=2):
    a=_arch();n=_first_stage()["cache_tokens"];kvb=a["full_kv_bytes_per_token"];c=a["cut"];titles=_titles()
    fig=fig_base(k,"Silicon Hippocampus architecture — SSD cartridges vs live GPU memory",
                 f"Three independent book cartridges are persisted on disk; the full {a['layers']}-layer memory exists only on the GPU after a mount","SCHEMATIC + LIVE VALUES",INK2)
    fig.text(.035,.815,"SSD — persistent cartridges (this session)",fontsize=14,weight="bold",color=INK)
    hb=n*a["hidden"]*2;kb=n*a["kv_heads"]*a["head_dim"]*2*2*(c+1)
    X0,BW=.035,.355
    for i,bid in enumerate(("A","B","C")):
        y=.625-i*.18;box(fig,X0,y,BW,.155,BOOK_COLORS[bid],lw=2);xm=X0+BW-.008;sv=LIVE["saved"].get(bid,{})
        ftext(fig,X0+.012,y+.125,f"Cartridge {bid} — {titles[bid]}",xmax=xm,fontsize=12,weight="bold",color=BOOK_COLORS[bid],va="center")
        ftext(fig,X0+.012,y+.088,f"file {sv.get('bytes',0):,} B · SHA-256 {str(sv.get('sha256'))[:16]}…",xmax=xm,fontsize=10,color=INK2,va="center",family="DejaVu Sans Mono")
        ftext(fig,X0+.012,y+.055,f"H{c}        [1, {n:,}, {a['hidden']:,}] BF16 = {hb:,} B",xmax=xm,fontsize=10,color=INK,va="center",family="DejaVu Sans Mono")
        ftext(fig,X0+.012,y+.024,f"K/V L0–L{c}  4×2×[1, {a['kv_heads']}, {n:,}, {a['head_dim']}] = {kb:,} B",xmax=xm,fontsize=10,color=INK,va="center",family="DejaVu Sans Mono")
    hs=[s for t in LIVE["trials"].values() for s in t["stages"]]
    arrow(fig,X0+BW+.012,.5,.485,.5,lw=2.4,ms=22);fig.text((X0+BW+.485)/2,.525,"mount",fontsize=13,weight="bold",ha="center",color=INK)
    if hs:
        ftext(fig,X0,.2,f"Mount = SSD read + SHA-256 check ≈ {np.mean([s['ssd_load_ms'] for s in hs])/1000:.2f} s, then host→GPU ≈ {np.mean([s['h2d_ms'] for s in hs]):.0f} ms\n(means over the {len(hs)} cartridge mounts of the live protocol)",
              xmax=X0+BW+.06,fontsize=10.5,color=INK2,va="top",linespacing=1.4)
    G0,GW=.5,.465
    ftext(fig,G0,.815,"GPU — frozen model + live memory (rebuilt at every mount)",fontsize=14,weight="bold",color=INK)
    base=LIVE["budget"].get("model_gpu",{}).get("allocated_gib")
    box(fig,G0,.62,GW,.15,INK2,fc=PANEL,lw=1.2)
    ftext(fig,G0+.012,.74,"Qwen2.5-72B-Instruct · NF4 4-bit weights · frozen",fontsize=12.5,weight="bold",color=INK,va="center")
    ftext(fig,G0+.012,.695,f"GPU memory allocated after load: {base:.1f} GiB ({LIVE['env'].get('gpu','GPU')})" if base else "",fontsize=11.5,color=INK2,va="center")
    ftext(fig,G0+.012,.655,f"{a['layers']} layers · weights unchanged (weight sentinel re-checked in this session)",fontsize=11.5,color=INK2,va="center")
    abc=LIVE["trials"].get("A_PLUS_B_PLUS_C",{}).get("stages",[])
    y=.37;hgt=.17
    ftext(fig,G0,y+hgt+.035,f"Live K/V memory: {a['layers']} layers × rows · {kvb:,} B per row (token)",fontsize=12,weight="bold",color=INK)
    if abc:
        tot=abc[-1]["cache_tokens"];a0=0
        for s in abc:
            w=GW*(s["cache_tokens"]-a0)/tot;fig.add_artist(Rectangle((G0+GW*a0/tot,y),w-.003,hgt,transform=fig.transFigure,facecolor=BOOK_COLORS[s["book"]],edgecolor="none",alpha=.92))
            fig.text(G0+GW*a0/tot+w/2,y+hgt/2+.025,f"{s['book']}",fontsize=16,weight="bold",color="white",ha="center",va="center")
            fig.text(G0+GW*a0/tot+w/2,y+hgt/2-.03,f"{s['cache_tokens']-a0:,} rows\n{(s['cache_tokens']-a0)*kvb/2**30:.2f} GiB",fontsize=10.5,color="white",ha="center",va="center")
            a0=s["cache_tokens"]
        gp=abc[-1]["gpu"]
        ftext(fig,G0,y-.02,f"A+B+C in the live protocol: {tot:,} rows = {tot*kvb:,} B ({tot*kvb/2**30:.2f} GiB) of K/V\nGPU after the third mount: allocated {gp['allocated_gib']:.2f} GiB, free {gp['free_gib']:.2f} GiB",
              fontsize=11,color=INK2,va="top",linespacing=1.4)
        cfb=LIVE["saved"]["A"]["bytes"]
        ftext(fig,G0,y-.105,f"One cartridge file = {100*cfb/(n*kvb):.1f} % of the full K/V bytes of the same {n:,} rows;\nthe other {a['layers']-c-1} layers are recomputed at mount time, not stored.",
              fontsize=11,color=INK,va="top",weight="bold",linespacing=1.4)
    fig_footer(fig,k,"Schematic layout, values measured in this session. The SSD holds only cartridges; the complete K/V memory exists only on the GPU after a mount.")
    return save_fig(fig,"ARCHITECTURE_SSD_GPU",k)

def fig3(k=3):
    fig=fig_base(k,"Three-cartridge consolidation and performance",
                 "Mount stages measured in this live session · times in seconds (log scale) · GPU memory in GiB","LIVE SESSION MEASUREMENT",TEAL)
    ax=fig.add_axes([.065,.2,.40,.56]);rows=[]
    for lab in ("A_PLUS_B_PLUS_C","C_PLUS_B_PLUS_A"):
        for i,s in enumerate(LIVE["trials"].get(lab,{}).get("stages",[])):rows.append((lab,i,s))
    if not rows:raise OpError("figure 3 needs the live three-cartridge protocol trials")
    xs=np.arange(len(rows));wd=.26
    ax.bar(xs-wd,[s["ssd_load_ms"]/1000 for _,_,s in rows],wd,color="#94A3B8",label="SSD read + SHA-256")
    ax.bar(xs,[s["h2d_ms"]/1000 for _,_,s in rows],wd,color="#475569",label="host → GPU")
    ax.bar(xs+wd,[s["rebuild_ms"]/1000 for _,_,s in rows],wd,color=[BOOK_COLORS[s["book"]] for _,_,s in rows],label="rebuild (colour = book)")
    ax.set_yscale("log");ax.set_ylim(min(.05,min(s["h2d_ms"]/1000 for _,_,s in rows)*.6),max(s["rebuild_ms"]/1000 for _,_,s in rows)*8);ax.set_ylabel("seconds (log scale)")
    ax.set_xticks(xs);ax.set_xticklabels([f"{'A+B+C' if l.startswith('A') else 'C+B+A'}\nstage {i+1}: {s['book']}\n{s['cache_tokens']:,} rows" for l,i,s in rows],fontsize=8.8)
    for x,(_,_,s) in zip(xs,rows):ax.text(x+wd,s["rebuild_ms"]/1000*1.1,f"{s['rebuild_ms']/1000:.1f}",ha="center",fontsize=10,weight="bold")
    ax.legend(loc="upper left",ncol=3,fontsize=9.5,handlelength=1.2,columnspacing=1.0)
    ax.set_title("(a) live protocol: rows after each mount, A+B+C and C+B+A",pad=10);ax.grid(axis="y",color="#E5E7EB",lw=.6);ax.set_axisbelow(True)
    for sp in ("top","right"):ax.spines[sp].set_visible(False)
    bx=fig.add_axes([.56,.51,.40,.25]);pts=[(s["cache_tokens"],s["gpu"]["allocated_gib"],s["gpu"]["free_gib"]) for t in LIVE["trials"].values() for s in t["stages"]]
    base=LIVE["budget"].get("model_gpu",{}).get("allocated_gib");kvb=LIVE["budget"].get("full_kv_bytes_per_token");res=LIVE["budget"].get("reserve_gib",E["GPU_RESERVE_GIB"])
    T=max(p[0] for p in pts)
    bx.plot([p[0] for p in pts],[p[1] for p in pts],"o",color=INK,ms=7,label="allocated after mount")
    bx.plot([p[0] for p in pts],[p[2] for p in pts],"s",color=TEAL,ms=6,label="free after mount")
    if base and kvb:tt=np.linspace(0,T,50);bx.plot(tt,base+tt*kvb/2**30,"--",color=MUTED,lw=1.4,label="model + K/V bytes (arithmetic)")
    bx.axhline(res,color=RED,lw=1.2,ls=":");bx.text(T*.01,res+1.2,f"GPU safety reserve {res} GiB",color=RED,fontsize=9.5)
    bx.set_ylim(0,max(max(p[1] for p in pts),max(p[2] for p in pts))*1.12);bx.legend(fontsize=9,loc="lower right",bbox_to_anchor=(.92,.18))
    bx.set_xlabel("memory rows (tokens)",fontsize=10.5);bx.set_ylabel("GiB");bx.set_title(f"(b) GPU memory after each live mount (n = {len(pts)})",pad=8);bx.grid(color="#E5E7EB",lw=.6)
    for sp in ("top","right"):bx.spines[sp].set_visible(False)
    cx=fig.add_axes([.56,.16,.40,.22]);ss=[s for s in STATE["ops"] if s["label"]=="READY_A_PLUS_B_PLUS_C"]
    if not ss:raise OpError("figure 3 needs the live ready-memory build")
    xs2=np.arange(len(ss));cx.bar(xs2,[s["end_to_end_ms"]/1000 for s in ss],color=[BOOK_COLORS[s["book"]] for s in ss],width=.55)
    cx.set_xticks(xs2);cx.set_xticklabels([f"{'first ' if s['operation']=='initialize' else '+'}{s['book']} · {s['cache_tokens']:,} rows" for s in ss],fontsize=9);cx.set_ylabel("s, end-to-end",fontsize=10.5)
    for x,s in zip(xs2,ss):cx.text(x,s["end_to_end_ms"]/1000*1.02,f"{s['end_to_end_ms']/1000:.1f}",ha="center",va="bottom",fontsize=9.5,weight="bold")
    cx.set_ylim(0,max(s["end_to_end_ms"] for s in ss)/1000*1.2);cx.set_title("(c) ready memory A+B+C built for the interface",pad=8)
    for sp in ("top","right"):cx.spines[sp].set_visible(False)
    fig_footer(fig,k,"rebuild = TEST709 'rebuild_ms' (initialize()/append() until GPU release); for appends it includes the exact SHA-256 seal and re-check of all prior K/V.")
    return save_fig(fig,"CONSOLIDATION_PERFORMANCE",k)

def fig4(k=4):
    x=STATE.get("xray")
    if not x:raise OpError("Figure 4 needs the read-only X-ray measurement of the live memory (no synthetic heat map is drawn).")
    fig=fig_base(k,"Internal neural memory X-ray — live 80-layer K/V memory",
                 f"Measured {x['utc']} · memory {'+'.join(x['order'])} · {x['tokens']:,} rows × {x['layers']} layers · bin {x['bin_tokens']} tokens",
                 "LIVE GPU MEASUREMENT",TEAL)
    def z(m):
        m=np.asarray(m,dtype=float);mu=np.nanmean(m,axis=1,keepdims=True);sd=np.nanstd(m,axis=1,keepdims=True);return (m-mu)/np.where(sd>0,sd,1)
    for j,(key,lab) in enumerate((("k_norm","K"),("v_norm","V"))):
        ax=fig.add_axes([.07,.53-j*.38,.86,.28]);im=ax.imshow(z(x[key]),aspect="auto",origin="lower",cmap="RdBu_r",vmin=-2.5,vmax=2.5,interpolation="nearest")
        ax.axhline(x["cut"]+.5,color=CUT_COLOR,lw=2,ls="--");ax.set_ylabel("layer");ax.set_yticks([0,20,40,60,x["layers"]-1])
        ax.set_title(f"‖{lab}‖ per row (mean over {x['kv_heads']} KV heads), z-scored within each layer for display",pad=6)
        nb=len(x[key][0])
        for s in x["segments"]:
            b0=s["start"]/x["bin_tokens"]-.5;b1=s["end"]/x["bin_tokens"]-.5
            ax.axvline(b1,color="white",lw=1.6)
            ax.text((b0+b1)/2,x["layers"]-3,f"cartridge {s['book']}",color=BOOK_COLORS[s["book"]],fontsize=11,weight="bold",ha="center",va="top",
                    bbox=dict(boxstyle="round,pad=0.25",fc="white",ec=BOOK_COLORS[s["book"]],lw=1,alpha=.92))
        ax.set_xticks(np.linspace(0,nb-1,6));ax.set_xticklabels([f"{int(t*x['bin_tokens']):,}" for t in np.linspace(0,nb-1,6)])
        if j==1:ax.set_xlabel("memory row (token position)")
        cb=fig.colorbar(im,ax=ax,fraction=.015,pad=.01);cb.set_label("z")
        ax.text(nb*.995-.5,x["cut"]+2,f"above dashed line: L{x['cut']+1}–L{x['layers']-1} recomputed · below: L0–L{x['cut']} from cartridges",ha="right",va="bottom",fontsize=9.5,color=INK,
                bbox=dict(boxstyle="round,pad=0.2",fc="white",ec="none",alpha=.85))
    fig_footer(fig,k,"Read-only measurement of this session's GPU K/V tensors (method in XRAY_MEASUREMENT.json). Colours are normalised per layer; absolute values are in the JSON record.")
    return save_fig(fig,"INTERNAL_MEMORY_XRAY",k)

def fig5(k=5):
    fig=fig_base(k,"Three books — memory and question answering (observational)",
                 "Raw answers of the frozen model in this live session; semantics UNSCORED; public-domain classics, so pretraining knowledge cannot be excluded","LIVE · OBSERVATIONAL",AMBER)
    titles=_titles();cw=(.93-2*.012)/3
    for i,bid in enumerate(("A","B","C")):
        x=.035+i*(cw+.012);box(fig,x,.745,cw,.09,BOOK_COLORS[bid],lw=2);src=LIVE["sources"].get(bid,{})
        ftext(fig,x+.01,.812,f"Cartridge {bid} — {titles[bid]}",xmax=x+cw-.006,fontsize=12.5,weight="bold",color=BOOK_COLORS[bid],va="center")
        ftext(fig,x+.01,.772,f"first {LIVE['forge_tokens'].get(bid) or 0:,} tokens of the Gutenberg file\n(source {src.get('bytes') or 0:,} B, SHA-256 {str(src.get('sha256'))[:12]}…)",xmax=x+cw-.006,fontsize=9.6,color=INK2,va="center")
    ctl={r["question"]:r["raw"] for r in STATE["controls"]}
    rows=[]
    for lab,t in LIVE["trials"].items():
        if t["qa"]:r=t["qa"][0];rows.append(("+".join(t["books"]) or "none",r["question"],r["raw"],ctl.get(r["question"])))
    if not rows:raise OpError("figure 5 needs the live protocol answers")
    diff=sum(1 for _,_,a,c in rows if c is not None and a!=c)
    XM,XQ,XA,XC=.035,.1,.37,.67;y=.705;rh=min(.047,.47/len(rows))
    for xx,t in ((XM,"memory"),(XQ,"question (live protocol)"),(XA,"answer WITH cartridge memory"),(XC,"control: same question, NO memory")):fig.text(xx,y,t,fontsize=10.2,weight="bold",color=MUTED)
    for i,(mem_,q,a,c) in enumerate(rows):
        yy=y-.03-i*rh;col=BOOK_COLORS.get(mem_.split("+")[0],INK2) if mem_!="none" else MUTED
        fig.text(XM,yy,mem_,fontsize=10,weight="bold",color=col,va="top")
        ftext(fig,XQ,yy,short(q,70),xmax=XA-.008,minsize=8,trunc=True,fontsize=9.4,color=INK,va="top")
        ftext(fig,XA,yy,short(a,80),xmax=XC-.008,minsize=7.6,trunc=True,fontsize=8.8,color=INK,va="top",family="DejaVu Sans Mono")
        ftext(fig,XC,yy,short(c if c is not None else "— not run",80),xmax=.965,minsize=7.6,trunc=True,fontsize=8.8,color=INK2,va="top",family="DejaVu Sans Mono")
    box(fig,.035,.09,.93,.075,AMBER,fc="#FFFBEB",lw=1.2)
    ftext(fig,.045,.128,wrap(f"Not a causal result. Answers with memory differ from the no-memory control in {diff} of {len(rows)} questions; a difference is not evidence of correctness and "
                             f"an equal answer is not evidence of failure. Semantics are unscored; the books are famous classics. Answers stop at {E['MAX_NEW']} new tokens.",165),
          xmax=.958,fontsize=10,color=INK,va="center")
    fig_footer(fig,k,"All rows were generated in this session (… = shortened for display). Full raw text: live engine log, SESSION_QA.jsonl and the live engine results JSON.")
    return save_fig(fig,"THREE_BOOKS_QA",k)

def fig6(k=6):
    v=STATE.get("verification")
    if not v:raise OpError("figure 6 needs the live verification record")
    fig=fig_base(k,"Integrity and verification record — this live session",f"Engine identity · live verification ({v['passed']}/{v['total']} passed) · historical reference kept separate",
                 "LIVE VERIFICATION",TEAL if v["ready"] else RED)
    a=_arch();env=LIVE["env"]
    col1=[("Engine",f"709.py · blob {LOCKS['709.py'][:12]}… (self-label TEST708-R2)"),("Model",f"{a['model_id']} · rev {str(LIVE.get('model_revision') or '—')[:12]}"),
          ("Weights",a["weights"]),("Architecture",f"{a['layers']} L · {a['hidden']} · {a['q_heads']}Q/{a['kv_heads']}KV · {a['head_dim']} · CUT{a['cut']}"),
          ("GPU",str(env.get("gpu"))),("Software",f"torch {env.get('torch')} · transformers {env.get('transformers')} · bitsandbytes {env.get('bitsandbytes')}"),
          ("Settings",f"{LIVE['forge_tokens'].get('A') or 0:,} tokens/book · chunk {a['chunk']} · reserve {a['reserve_gib']} GiB · max new {a['max_new']}"),
          ("Engine status",f"{LIVE['status']} · {LIVE.get('elapsed_s')} s")]
    fig.text(.035,.8,"Engine and model (this session)",fontsize=13.5,weight="bold",color=INK);y=.755
    for kk,vv in col1:
        s=wrap(vv,40);fig.text(.035,y,kk,fontsize=10.2,weight="bold",color=INK2,va="top")
        ftext(fig,.125,y,s,xmax=.355,fontsize=9.8,color=INK,va="top",linespacing=1.2);y-=.045+.026*s.count("\n")
    fig.text(.375,.8,"Live verification",fontsize=13.5,weight="bold",color=INK);y=.755
    for it in v["items"]:
        ok=it["passed"];fig.text(.375,y,"PASS" if ok else "FAIL",fontsize=10,weight="bold",color=TEAL if ok else RED,va="top",family="DejaVu Sans Mono")
        ftext(fig,.415,y,it["name"],xmax=.665,fontsize=9.6,color=INK,va="top",family="DejaVu Sans Mono")
        ftext(fig,.415,y-.021,short(it["detail"] if isinstance(it["detail"],str) else json.dumps(it["detail"],ensure_ascii=False),70),xmax=.665,minsize=7,trunc=True,fontsize=8.4,color=MUTED,va="top")
        y-=.049
    box(fig,.685,.205,.28,.62,RULE,fc="#F3F4F6",lw=1)
    fig.text(.697,.8,"Historical reference",fontsize=12.5,weight="bold",color=INK2,va="center")
    fig.text(.697,.775,"published logs of EARLIER runs — not this session",fontsize=9,color=RED,va="center",weight="bold")
    yy=.745
    for c in CHRONO:
        ok=str(c.get("status","")).startswith("PASS");fig.text(.697,yy,c["label"],fontsize=10,weight="bold",color=TEAL if ok else RED,va="top")
        s=wrap((f"{c['tokens_per_book']} tok/book · " if c.get('tokens_per_book') else "")+f"{c.get('status')}" + (f" · {c['error']}" if c.get("error") else ""),46)
        ftext(fig,.697,yy-.024,s,xmax=.958,fontsize=8.6,color=INK2,va="top",linespacing=1.15);yy-=.05+.022*s.count("\n")
    h=v.get("historical_reference") or {}
    if h.get("available"):
        sh=", ".join(f"{b} {'identical' if ok else 'different'}" for b,ok in h["cartridge_sha256_identical"].items());ta=h["trial_answers_identical"]
        ftext(fig,.697,yy-.01,wrap(f"Reproducibility comparison computed now (reference only): cartridge SHA-256 vs published run: {sh}; "
                                   f"trial answers identical: {sum(ta.values())}/{len(ta)}",48),xmax=.958,fontsize=8.6,color=INK,va="top",linespacing=1.2)
    box(fig,.035,.09,.93,.1,RULE,fc=PANEL,lw=1)
    fig.text(.045,.175,"Cartridge SHA-256 recorded by the engine in this session (re-verified on disk)",fontsize=10.5,weight="bold",color=INK,va="top")
    for i,b in enumerate(("A","B","C")):
        ftext(fig,.045,.148-i*.02,f"{b}  {LIVE['saved'][b]['sha256']}  {LIVE['saved'][b]['bytes']:,} B",xmax=.958,fontsize=8.8,color=BOOK_COLORS[b],va="top",family="DejaVu Sans Mono")
    fig_footer(fig,k,f"Live records: VERIFICATION_RECORD.json · live engine log · SESSION.log · SHA256_MANIFEST.json (session {SESSION_ID}). Historical files are in a separate folder.")
    return save_fig(fig,"INTEGRITY_VERIFICATION_RECORD",k)

FIG_FUNCS=OrderedDict([("F1",fig1),("F2",fig2),("F3",fig3),("F4",fig4),("F5",fig5),("F6",fig6)])
def render_figures():
    """renders all six figures on the CPU from this session's live data (no GPU use)"""
    global LIVE
    LIVE=live_record();out={};errs={}
    for i,(key,fn) in enumerate(FIG_FUNCS.items(),1):
        t=time.perf_counter()
        try:rec=fn(i);out[key]=rec;FIG_FILES[key]=rec;print(f"  figure {i}/6 · {rec['pixels'][0]}×{rec['pixels'][1]} JPEG · {rec['jpg_bytes']/1e6:.1f} MB · {time.perf_counter()-t:.1f} s · {Path(rec['jpg']).name}",flush=True)
        except Exception as ex:errs[key]=f"{type(ex).__name__}: {ex}";FIG_FILES.pop(key,None);flog(f"FIGURE {i} NOT GENERATED {traceback.format_exc()[-1500:]}");print(f"  figure {i}/6 NOT GENERATED · {errs[key]}",flush=True)
    dump_json(SESSION_DIR/"FIGURES_MANIFEST.json",dict(session=SESSION_ID,utc=utc_now(),data_source="live session only",figures=FIG_FILES,not_generated=errs))
    slog("FIGURES",f"{len(out)} rendered",not_generated=errs);return out,errs

# ---------------------------------------------------------------------------------------------------------------------
# downloadable research artifacts (actual files of this session; historical files in their own folder)
# ---------------------------------------------------------------------------------------------------------------------
LIVE_ENGINE_LOG=LIVE_DIR/"LIVE_TEST709_ENGINE_RUN_this_session.log";LIVE_ENGINE_JSON=LIVE_DIR/"LIVE_TEST709_ENGINE_RESULTS_this_session.json"
HIST_709=HIST_DIR/"HISTORICAL_TEST709_published_709.log"
ZIP_PATH=SESSION_DIR/f"{SESSION_ID}_AKBASCORE_Q72_ALL_RESEARCH_ARTIFACTS.zip";MANIFEST=SESSION_DIR/"SHA256_MANIFEST.json"
def sync_live_files():
    """byte-identical copies of the engine's own live files (the engine keeps writing to E['LOG'] / E['OUT'])"""
    for src,dst in ((E.get("LOG"),LIVE_ENGINE_LOG),(E.get("OUT"),LIVE_ENGINE_JSON)):
        try:
            if src and Path(src).is_file():shutil.copyfile(src,dst)
        except Exception as ex:slog("SYNC_FAILED",str(dst),error=str(ex))
def session_record():
    return dict(session=SESSION_INFO,app=APP_TITLE,version_note=VERSION_NOTE,sources=SOURCES,locks=LOCKS,engine=jsafe(ENGINE),initialization=INIT,
                architecture=engine_architecture(),memory=dict(order=STATE["order"],stages=STATE["stages"]),operations=STATE["ops"],
                qa=STATE["qa"],controls=STATE["controls"],weight_checks=STATE["weight_checks"],disk_checks=STATE["disk_checks"],
                verification=STATE["verification"],figures=FIG_FILES,
                scope="Physical reconstruction and integrity are measured live; answer semantics are not scored; public-domain books (pretraining knowledge possible).")
def _category(rel):
    if rel.startswith("historical_reference_not_this_session"):return "HISTORICAL (published earlier run, not this session)"
    if rel.startswith("figures"):return "LIVE figure"
    return "LIVE session record"
RUN_SUMMARY=SESSION_DIR/"RUN_SUMMARY.txt"
def write_run_summary():
    """plain-text summary of THIS live run (like the Mistral v1.4 RUN_SUMMARY.txt); historical files only in their own section"""
    R=E.get("R",{});v=STATE.get("verification") or {};L=[]
    a=L.append
    a(f"{APP_TITLE}\n{VERSION_NOTE}\nsession {SESSION_ID} · started {SESSION_INFO['started_local']} · written {local_now()}\n")
    a("ENGINE  709.py git blob "+LOCKS["709.py"]+" (self-label TEST708-R2), executed unchanged")
    a(f"MODEL   {E.get('MODEL_ID')} · NF4 4-bit, BF16 compute, frozen · revision {R.get('model_revision')} · load {R.get('model_load_s')} s")
    env=R.get("env",{});a(f"GPU     {env.get('gpu')} · torch {env.get('torch')} · transformers {env.get('transformers')} · bitsandbytes {env.get('bitsandbytes')}")
    a(f"SETUP   {E.get('TOKENS_PER_BOOK')} tokens per book · chunk {E.get('CHUNK')} · GPU reserve {E.get('GPU_RESERVE_GIB')} GiB · max new tokens {E.get('MAX_NEW')}\n")
    a("INITIALIZATION (this session)")
    for st in INIT["steps"]:a(f"  ✓ {st['step']:<13} {st['seconds']:>9.1f} s  {st['title']}")
    if INIT.get("failed"):a(f"  ✗ {INIT['failed']['step']}  {INIT['failed']['error']}  (last successful: {INIT['failed']['last_successful_step']})")
    a(f"\nLIVE ENGINE STATUS  {R.get('status')}  · engine checks passed {sum(1 for c in R.get('checks',[]) if c.get('pass'))}/{len(R.get('checks',[]))}")
    a("\nCARTRIDGES (forged and saved in this session)")
    for b in R.get("books",[]):a(f"  {b['id']} {b.get('title')} · {b.get('requested_tokens')} tokens · file {b.get('cartridge_file_bytes')} B · SHA-256 {b.get('cartridge_sha256')}")
    a("\nLIVE TEST709 PROTOCOL (raw answers, semantics UNSCORED)")
    ctl={r["question"]:r["raw"] for r in STATE["controls"]}
    for t in R.get("trials",[]):
        a(f"  {t['label']:<18} rows {t['cache_tokens']:>6} · "+" · ".join(f"{s['book']} rebuild {s['rebuild_ms']/1000:.1f} s" for s in t["stages"]))
        for r in t["qa"]:a(f"      Q {r['question']}\n      memory  → {r['raw']}\n      control → {ctl.get(r['question'],'(not run)')}")
    a(f"\nLIVE VERIFICATION  {v.get('passed','—')}/{v.get('total','—')} passed · READY {v.get('ready')}")
    for i in v.get("items",[]):a(f"  {'PASS' if i['passed'] else 'FAIL'}  {i['name']}  {i['detail'] if isinstance(i['detail'],str) else json.dumps(i['detail'],ensure_ascii=False)}")
    if STATE["qa"]:
        a("\nQUESTIONS ASKED IN THE INTERFACE")
        for r in STATE["qa"]:
            if r.get("origin")=="user":a(f"  [{'+'.join(r['memory_order'])}] {r['question']} → {r['raw']}")
    h=v.get("historical_reference") or {}
    a("\nHISTORICAL REFERENCE — published 709.log of an EARLIER run (not this session, not used for READY)")
    if h.get("available"):
        a(f"  published status {h['historical_status']} · cartridge SHA-256 identical {h['cartridge_sha256_identical']} · trial answers identical {sum(h['trial_answers_identical'].values())}/{len(h['trial_answers_identical'])}")
    a("\nSCOPE  Physical reconstruction and integrity are measured live; answer semantics are not scored; the books are public-domain classics (pretraining knowledge possible).")
    a(f"{AUTHOR} · {ORG} · {LICENSE_NAME} · {COPYRIGHT}")
    RUN_SUMMARY.write_text("\n".join(L)+"\n",encoding="utf-8");return str(RUN_SUMMARY)
def package_session():
    """Download-All ZIP: six figures (JPG/PNG/PDF), live engine log + results, session logs, verification records,
    historical files (separate folder) and SHA256_MANIFEST.json"""
    sync_live_files();dump_json(SESSION_DIR/"SESSION_RECORD.json",session_record());write_run_summary()
    files=sorted(p for p in SESSION_DIR.rglob("*") if p.is_file() and p.suffix not in (".zip",".tmp") and p!=MANIFEST)
    man=OrderedDict((str(p.relative_to(SESSION_DIR)),dict(sha256=sha_file(p),bytes=p.stat().st_size,category=_category(str(p.relative_to(SESSION_DIR))))) for p in files)
    dump_json(MANIFEST,dict(session=SESSION_ID,utc=utc_now(),files=man))
    tmp=ZIP_PATH.with_suffix(".zip.tmp")
    with zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED) as z:
        for p in files+[MANIFEST]:z.write(p,arcname=f"{SESSION_ID}/{p.relative_to(SESSION_DIR)}")
    with zipfile.ZipFile(tmp) as z:
        if z.testzip():raise RuntimeError("ZIP check failed")
    tmp.replace(ZIP_PATH);slog("PACKAGE",ZIP_PATH.name,files=len(files)+1,bytes=ZIP_PATH.stat().st_size);return str(ZIP_PATH)
def download_items():
    """(label, path) of every individually downloadable record — only files that exist"""
    items=[("Run summary (.txt)",RUN_SUMMARY),("Live engine log of this session (.log)",LIVE_ENGINE_LOG),("Live engine results of this session (.json)",LIVE_ENGINE_JSON),
           ("Session log (.log)",SESSION_LOG),("Session events (.jsonl)",SESSION_EVENTS),("Questions and raw answers (.jsonl)",SESSION_QA),
           ("Verification record (.json)",VERIFY_FILE),("Initialization record (.json)",INIT_FILE),("X-ray measurement (.json)",SESSION_DIR/"XRAY_MEASUREMENT.json"),
           ("Figure manifest (.json)",SESSION_DIR/"FIGURES_MANIFEST.json"),("SHA-256 manifest (.json)",MANIFEST),
           ("HISTORICAL · published 709.log of an earlier run (not this session)",HIST_709)]
    return [(l,str(p)) for l,p in items if Path(p).is_file()]

# ---------------------------------------------------------------------------------------------------------------------
# AUTOMATIC INITIALIZATION — one start, every step real, stops at the first failure
# ---------------------------------------------------------------------------------------------------------------------
def _step_model():
    pf=json.loads((SESSION_DIR/"PREFLIGHT.json").read_text()) if (SESSION_DIR/"PREFLIGHT.json").is_file() else {}
    print("  model cache:",pf.get("model_cache_state","unknown"),"\n  The progress bars below are the real Hugging Face download / checkpoint-loading bars.",flush=True)
    return load_model_stage()
def _step_closing():
    r=closing_stage()
    if r["status"]!=ENGINE_PASS_STATUS or r["failed"]:raise RuntimeError(f"TEST709 live status {r['status']} · failed checks {r['failed']}")
    return r
def _step_ready():
    st=build_memory(["A","B","C"],label="READY_A_PLUS_B_PLUS_C")
    return dict(order=STATE["order"],rows=st[-1]["cache_tokens"],stages=[dict(book=s["book"],end_to_end_s=round(s["end_to_end_ms"]/1000,2),sha256_line=s["prior_kv_sha256_pass_line"]) for s in st])
def _step_verify():
    d=verify_disk();w=verify_weights();x=xray_measure();v=compute_verification()
    for it in v["items"]:print(f"  {'PASS' if it['passed'] else 'FAIL'}  {it['name']:<44} {short(it['detail'] if isinstance(it['detail'],str) else json.dumps(it['detail'],ensure_ascii=False),90)}",flush=True)
    if not v["ready"]:raise RuntimeError("LIVE VERIFICATION FAILED: "+", ".join(i["name"] for i in v["items"] if not i["passed"]))
    return dict(passed=v["passed"],total=v["total"])
def _step_figures():
    out,errs=render_figures()
    if errs or len(out)!=6:raise RuntimeError(f"FIGURES: {len(out)}/6 generated · {errs}")
    dump_json(INIT_FILE,INIT);z=package_session()
    return dict(figures=[Path(r["jpg"]).name for r in out.values()],zip=Path(z).name)
STEP_FUNCS=OrderedDict([("SOURCES",sources_step),("PREFLIGHT",preflight),("MODEL",_step_model),("FORGE",forge_stage),("PROTOCOL",protocol_stage),
                        ("CLOSING",_step_closing),("CONTROLS",run_controls),("READY_MEMORY",_step_ready),("VERIFY",_step_verify),("FIGURES",_step_figures)])

def init_failed(key,ex):
    tb=traceback.format_exc()
    INIT["failed"]=dict(step=key,title=INIT_STEPS[key],error=f"{type(ex).__name__}: {ex}",last_successful_step=INIT["last_ok"],utc=utc_now(),traceback=tb[-6000:])
    if ENGINE.get("defined") and not ENGINE.get("finished"):
        try:engine_fail(ex)
        except Exception:pass
    _drop_memory("initialization failed")
    slog("INIT_FAILED",key,error=INIT["failed"]["error"],last_successful_step=INIT["last_ok"],gpu=gpu_now() if ENGINE.get("defined") else None,traceback=tb[-3000:])
    try:dump_json(INIT_FILE,INIT);package_session()
    except Exception as ex2:print("  (failure package could not be written:",ex2,")",flush=True)
    print("\n"+"█"*112+f"\nINITIALIZATION STOPPED — the demonstration is NOT ready and no interface is opened.\n"
          f"  failed step          : {key} · {INIT_STEPS[key]}\n  error                : {INIT['failed']['error']}\n"
          f"  last successful step : {INIT['last_ok'] or 'none'}\n  records              : {SESSION_DIR}\n  all files (ZIP)      : {ZIP_PATH if ZIP_PATH.is_file() else 'not written'}\n"+"█"*112,flush=True)

def run_initialization():
    print("\n"+"#"*112+f"\n{APP_TITLE}\n{VERSION_NOTE} · session {SESSION_ID} · records in {SESSION_DIR}\n"
          "Automatic initialization: every step below is executed for real in this runtime; nothing is precomputed.\n"+"#"*112,flush=True)
    for key,fn in STEP_FUNCS.items():
        t0=step_begin(key)
        try:info=fn()
        except BaseException as ex:
            init_failed(key,ex);raise RuntimeError(f"INITIALIZATION FAILED at {key}: {type(ex).__name__}: {ex}") from ex
        step_done(key,t0,result=info)
    INIT["ready"]=True;INIT["ready_utc"]=utc_now();INIT["total_seconds"]=round(time.perf_counter()-INIT["started"],1)
    dump_json(INIT_FILE,INIT);package_session()
    print("\n"+"#"*112+f"\nREADY — all {len(STEP_FUNCS)} steps passed in {INIT['total_seconds']/60:.1f} min · live verification "
          f"{STATE['verification']['passed']}/{STATE['verification']['total']} · memory {'+'.join(STATE['order'])} ({STATE['stages'][-1]['cache_tokens']:,} rows)\n"+"#"*112,flush=True)
    slog("READY","initialization complete",seconds=INIT["total_seconds"])
    return True
