# ===== PART 2/3 — paste directly after PART 1 in the same cell =====
# =====================================================================================================================
# PART 2 / 3 — Cartridge Operations, Experiment Records, Integrity and Research Figures
# Interactive operations call the TEST709 engine functions that TEST718 uses (E["cart_load"], E["initialize"],
# E["run_answer"], E["free_gpu"], E["ensure_room"], E["sentinel"]) in the order TEST718 uses them. Nothing here changes CUT3,
# RoPE, the cartridge format, the SHA-256 guards or the GPU reserve. All measurements are read-only and computed from this
# session's engine records (E["R718"], E["R"], the time-stamped engine output) and from the original PDF downloaded now.
# =====================================================================================================================
class OpError(RuntimeError):pass
def _torch():return E["torch"]
def gpu_now():
    try:return E["mem"]()
    except Exception as ex:return {"error":f"{type(ex).__name__}: {ex}"}
def _require():
    if not ENGINE.get("done") or "model" not in E:raise OpError("The TEST718 experiment has not completed in this session.")
def cart_ids():return [b["id"] for b in E["R"]["books"]]
def cart_index(bid):return cart_ids().index(bid)
def ntok(text):
    try:return len(E["tok"](str(text or ""),add_special_tokens=False).input_ids)
    except Exception:return None

def _release(reason):
    had=STATE["memory"] is not None
    STATE["memory"]=None;STATE["cartridge"]=None;STATE["mount"]=None
    try:E["free_gpu"]()
    except Exception:pass
    if had:slog("MEMORY_RELEASED",reason,gpu=gpu_now())

def mount(bid):
    """one physical cartridge on the GPU, exactly as TEST718 mounts it (718.py line 46):
    cart_load(bid) → list(initialize(cp)) → del cp → free_gpu(). The previous memory is released first (one at a time)."""
    with ENGINE_LOCK:
        _require()
        if bid not in cart_ids():raise OpError(f"Unknown cartridge {bid}.")
        _release("new cartridge requested");torch=_torch();t=time.perf_counter();cp=None
        try:
            cp,times=E["cart_load"](bid);t0=time.perf_counter()
            memory=list(E["initialize"](cp));del cp;cp=None;E["free_gpu"]();torch.cuda.synchronize()
        except BaseException as ex:
            if cp is not None:del cp
            _release(f"mount failed: {type(ex).__name__}");slog("MOUNT_FAILED",bid,error=f"{type(ex).__name__}: {ex}");raise
        times["rebuild_ms"]=round((time.perf_counter()-t0)*1000,3);times["end_to_end_ms"]=round((time.perf_counter()-t)*1000,3)
        times.update(cartridge=bid,cache_tokens=int(memory[0][0].shape[-2]),gpu=E["mem"](),utc=utc_now())
        STATE["memory"]=memory;STATE["cartridge"]=bid;STATE["mount"]=times;STATE["ops"].append(dict(times))
        slog("MOUNT",bid,**times);return times

def ask(question,use_memory=True,origin="user"):
    """question answering exactly as a TEST718 readout: run_answer(memory, question) with up to 144 new tokens;
    use_memory=False is the TEST718 vanilla path (same frozen model, no PDF, no cartridge)."""
    with ENGINE_LOCK:
        _require()
        q=(question or "").strip()
        if not q or len(q)>3000:raise OpError("The question must contain 1–3000 characters.")
        if use_memory and STATE["memory"] is None:raise OpError("No cartridge is mounted.")
        E["ensure_room"](512);t=time.perf_counter()
        raw=E["run_answer"](STATE["memory"] if use_memory else None,q)
        row=dict(utc=utc_now(),origin=origin,question=q,raw=raw,cartridge=(STATE["cartridge"] if use_memory else None),with_memory=bool(use_memory),
                 cache_tokens=(int(STATE["memory"][0][0].shape[-2]) if use_memory else 0),answer_tokens=ntok(raw),max_new_tokens=READOUT_MAX_NEW,
                 seconds=round(time.perf_counter()-t,3),gpu=E["mem"](),semantics="NOT VERIFIED")
        (STATE["qa"] if use_memory else STATE["controls"]).append(row)
        with SESSION_QA.open("a",encoding="utf-8") as f:f.write(json.dumps(jsafe(row),ensure_ascii=False)+"\n")
        slog("QA" if use_memory else "QA_VANILLA",row["cartridge"] or "NO MEMORY",question=q[:300],raw=raw,seconds=row["seconds"])
        return row

# ---------------------------------------------------------------------------------------------------------------------
# live verification (read-only)
# ---------------------------------------------------------------------------------------------------------------------
def verify_weights():
    with ENGINE_LOCK:
        _require();t=time.perf_counter();after=E["sentinel"]();before=E["R718"].get("weight_sentinel_before")
        row=dict(utc=utc_now(),passed=(before is not None and after==before),before=before,after=after,seconds=round(time.perf_counter()-t,2))
        STATE["weight_checks"].append(row);slog("WEIGHT_CHECK","PASS" if row["passed"] else "FAIL",**row);return row
def verify_disk():
    """re-hash the ten cartridge files on SSD and compare with the SHA-256 the engine recorded"""
    with ENGINE_LOCK:
        _require();rows=[];t=time.perf_counter()
        for b in E["R"]["books"]:
            p=Path(E["CART"])/(b["id"]+".pt");h=sha_file(p) if p.is_file() else None
            rows.append(dict(cartridge=b["id"],file=str(p),bytes=(p.stat().st_size if p.is_file() else None),sha256=h,engine_record_sha256=b.get("cartridge_sha256"),equals_engine_record=(h is not None and h==b.get("cartridge_sha256"))))
            STATE["files"][b["id"]]=rows[-1]
        row=dict(utc=utc_now(),files=rows,passed=(len(rows)==N_CART and all(r["equals_engine_record"] for r in rows)),seconds=round(time.perf_counter()-t,2))
        STATE["disk_checks"].append(row);slog("DISK_CHECK","PASS" if row["passed"] else "FAIL",passed=row["passed"],seconds=row["seconds"]);return row

# ---------------------------------------------------------------------------------------------------------------------
# READ-ONLY X-ray of the live GPU K/V tensors — every cartridge mounted ALONE (as in TEST718), measured, released
# ---------------------------------------------------------------------------------------------------------------------
XRAY_FILE=SESSION_DIR/"XRAY_TEN_CARTRIDGES.json"
def xray_measure(bin_tokens=256,chunk=4096):
    """per layer and per token bin: mean over KV heads of the L2 norm of each K and V row of the mounted memory.
    FP32 copies of small chunks; nothing is written to the tensors; no reference is kept after returning."""
    with ENGINE_LOCK:
        _require()
        if STATE["memory"] is None:raise OpError("No cartridge is mounted.")
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
        return dict(cartridge=STATE["cartridge"],utc=utc_now(),tokens=T,layers=NL,kv_heads=E["KVH"],bin_tokens=bin_tokens,cut=E["CUT"],prefix_tokens=E["P"],
                    k_norm=Kb.round(5).tolist(),v_norm=Vb.round(5).tolist(),finite=bool(np.isfinite(Kb).all() and np.isfinite(Vb).all()),
                    k_mean=float(np.nanmean(Kb)),v_mean=float(np.nanmean(Vb)),seconds=round(time.perf_counter()-t,2),gpu=E["mem"](),
                    method=f"mean over {E['KVH']} KV heads of the L2 norm per K/V row; mean per bin of {bin_tokens} tokens; FP32 copies of {chunk}-row chunks; read-only")
def xray_all():
    """C01…C10 one after another: mount ALONE → measure → release. The ten memories never coexist on the GPU."""
    for bid in cart_ids():
        t=mount(bid);x=xray_measure();x["mount"]={k:t.get(k) for k in ("ssd_load_ms","h2d_ms","rebuild_ms","end_to_end_ms","cache_tokens","utc")}
        _release(f"X-ray of {bid} done");x["released_utc"]=utc_now();STATE["xrays"][bid]=x
        _OUT.write(f"  X-ray {bid} · {x['tokens']:,} rows × {x['layers']} layers · mount {t['end_to_end_ms']/1000:.1f} s · measure {x['seconds']:.1f} s · released {x['released_utc'][11:19]} UTC\n");_OUT.flush()
        slog("XRAY",bid,tokens=x["tokens"],finite=x["finite"],seconds=x["seconds"],mounted_utc=t["utc"],released_utc=x["released_utc"])
    dump_json(XRAY_FILE,dict(session=SESSION_ID,note="each cartridge was mounted alone, measured read-only and released before the next one",xrays=STATE["xrays"]))
    return dict(cartridges=len(STATE["xrays"]),first_utc=STATE["xrays"][cart_ids()[0]]["utc"],last_utc=STATE["xrays"][cart_ids()[-1]]["utc"])

# ---------------------------------------------------------------------------------------------------------------------
# historical reference only (published logs of EARLIER runs) — never shown as results of this session
# ---------------------------------------------------------------------------------------------------------------------
def load_historical():
    out={}
    for n in HISTORICAL:
        r=fetch_locked(n);(HIST_DIR/("HISTORICAL_"+n)).write_bytes(r);out[n]=LOCKS[n]
    (HIST_DIR/"README_HISTORICAL.txt").write_text(
        "These files are PUBLISHED RECORDS OF EARLIER RUNS (TEST716, TEST717, TEST718), verified against their git blob identifiers.\n"
        "They are NOT results of this session. Live results of this session are in ../live_engine/ and in the session files.\n"
        +"".join(f"{n}: git blob {LOCKS[n]}\n" for n in HISTORICAL),encoding="utf-8")
    slog("HISTORICAL_LOADED","published TEST716/717/718 logs verified (reference only, not this session)",blobs=out);return out
def sources_step():
    load_engine_source();h=load_historical()
    fetch_locked("LICENSE");(SESSION_DIR/"LICENSE.txt").write_bytes((EVIDENCE_DIR/"LICENSE").read_bytes())
    return dict(sources={k:v["git_blob"] for k,v in SOURCES.items()},historical=list(h))

# ---------------------------------------------------------------------------------------------------------------------
# LIVE experiment record: everything below is computed from this session's engine record and engine output
# ---------------------------------------------------------------------------------------------------------------------
def _line_times(prefix):
    """seconds since engine start of the engine output lines that start with prefix, keyed by cartridge id"""
    out={}
    for ts,el,line in ENGINE_LINES:
        if line.startswith(prefix):
            m=re.match(re.escape(prefix)+r"(C\d\d)\b",line)
            if m:out[m.group(1)]=(el,ts)
    return out
_W=re.compile(r"[a-z0-9]+(?:[.\-][a-z0-9]+)*")
def _words(t):return _W.findall(str(t or "").lower())
def _grams(w,n=5):return set(tuple(w[i:i+n]) for i in range(len(w)-n+1))
def verbatim_support(answer,source_text,question,n=5):
    """share of the answer's word 5-grams (excluding 5-grams copied from the question) found verbatim in the source
    pages — an automatic lexical measure, NOT a judgement of technical correctness"""
    a=_words(answer);qg=_grams(_words(question),n);ag=[tuple(a[i:i+n]) for i in range(len(a)-n+1)]
    ag=[g for g in ag if g not in qg]
    if not ag:return dict(share=None,ngrams=0,found=0)
    src=_grams(_words(source_text),n);f=sum(1 for g in ag if g in src)
    return dict(share=round(f/len(ag),4),ngrams=len(ag),found=f)
_PG=re.compile(r"PDF\s+pages?\s*(\d{1,3})(?:\s*(?:-|–|to|and)\s*(\d{1,3}))?",re.I)
def page_check(answer,heading_page,cart_range):
    """automatic check of the page the answer STATES against the PDF page where the heading occurs (from the PDF)"""
    m=_PG.search(str(answer or ""))
    if not m:return dict(stated=None,result="not stated",delta=None)
    a=int(m.group(1));b=int(m.group(2)) if m.group(2) else a
    if a==heading_page==b:res="same page"
    elif a<=heading_page<=b:res="range contains heading page"
    else:res="different page"
    d=0 if a<=heading_page<=b else min(abs(a-heading_page),abs(b-heading_page))
    return dict(stated=(a if a==b else f"{a}–{b}"),result=res,delta=d,inside_cartridge=(cart_range[0]<=a<=cart_range[1]))
def section_check(answer,section_number):
    s=str(answer or "");return dict(section=section_number,stated=bool(section_number and re.search(r"(?<![\d.])"+re.escape(section_number)+r"(?![\d])",s)))

def live_record():
    R7=E["R718"];R=E["R"];books=R["books"];P=E.get("P")
    van=_line_times("VANILLA ");phy=_line_times("PHYSICAL ");abl=_line_times("ABLATION ")
    rows=[];prev=(van.get(books[-1]["id"]) or (None,))[0]
    for i,r in enumerate(R7["results"]):
        b=books[i];a,bb=b["page_range"];src="".join(DOC_PAGES[a-1:bb]) if DOC_PAGES else ""
        pw=None
        if r["id"] in phy and prev is not None:pw=round(phy[r["id"]][0]-prev,3)
        if r["id"] in phy:prev=phy[r["id"]][0]
        vw=None
        if i>0 and r["id"] in van and books[i-1]["id"] in van:vw=round(van[r["id"]][0]-van[books[i-1]["id"]][0],3)
        tm=r.get("timing") or {}
        f=STATE["files"].get(r["id"],{})
        row=dict(id=r["id"],index=i,pages=[a,bb],body_tokens=b["body_tokens"],cache_tokens=r.get("cache_tokens"),expected_rows=(P+b["body_tokens"]) if P is not None else None,
                 heading=r["heading"],heading_page=r["pdf_page"],section=r.get("section_number"),question=r["question"],
                 vanilla=r.get("vanilla"),physical=r.get("physical_readout"),ablation=r.get("post_release_no_memory"),
                 vanilla_tokens=ntok(r.get("vanilla")),physical_tokens=ntok(r.get("physical_readout")),
                 ssd_load_ms=tm.get("ssd_load_ms"),h2d_ms=tm.get("h2d_ms"),physical_wall_s=pw,vanilla_wall_s=vw,
                 physical_utc=(phy.get(r["id"]) or (None,None))[1],cartridge_sha256=b.get("cartridge_sha256"),file_bytes=f.get("bytes"),file_sha_ok=f.get("equals_engine_record"),
                 support_physical=verbatim_support(r.get("physical_readout"),src,r["question"]),support_vanilla=verbatim_support(r.get("vanilla"),src,r["question"]),
                 page_physical=page_check(r.get("physical_readout"),r["pdf_page"],(a,bb)),page_vanilla=page_check(r.get("vanilla"),r["pdf_page"],(a,bb)),
                 section_physical=section_check(r.get("physical_readout"),r.get("section_number")),
                 vanilla_unknown=str(r.get("vanilla") or "").strip().upper().startswith("UNKNOWN"),physical_unknown=str(r.get("physical_readout") or "").strip().upper().startswith("UNKNOWN"))
        row["physical_truncated"]=(row["physical_tokens"] or 0)>=READOUT_MAX_NEW
        if r.get("post_release_no_memory") is not None:row["ablation_equals_vanilla"]=(r["post_release_no_memory"]==r.get("vanilla"))
        rows.append(row)
    syn=R7.get("synthesis_output") or ""
    cites={x["id"]:len(re.findall(r"(?<![A-Za-z0-9])"+x["id"]+r"(?![0-9])",syn)) for x in books}
    sw=_grams(_words(syn))
    reuse={}
    for row in rows:
        g=_grams(_words(row["physical"]));reuse[row["id"]]=round(len(g&sw)/len(g),4) if g else None
    m=R7.get("map") or {}
    return dict(status=R7.get("status"),rows=rows,synthesis=dict(mode=R7.get("synthesis_mode"),output=syn,tokens=ntok(syn),input_tokens=ntok(R7.get("synthesis_input")),
                truncated=(ntok(syn) or 0)>=SYNTH_MAX_NEW,citations=cites,reuse=reuse,utc=(next((ts for ts,el,l in ENGINE_LINES if l.startswith("SYNTHESIS ")),None))),
                cosine=dict(metric=m.get("metric"),labels=m.get("cartridges"),matrix=m.get("similarity"),limit=m.get("interpretation_limit")),
                panel=R.get("panel_source"),token_counts=R.get("body_tokens"),page_ranges=R.get("page_ranges"),prefix_tokens=P,
                sentinel_before=R7.get("weight_sentinel_before"),sentinel_after=R7.get("weight_sentinel_after"),
                engine_checks={k:R.get(k) for k in ("709_GIT_BLOB_LOCK","PDF_SHA256_LOCK","PDF_486_PAGES","PANEL_MIN_30","ALL_PAGES_COVERED","CUDA_A100_80GB","MODEL_ARCH","FROZEN")},
                engine_pass_lines=[l for _,_,l in ENGINE_LINES if l.startswith("PASS ")],engine_seconds=ENGINE.get("seconds"),
                engine_started_utc=ENGINE.get("started_utc"),engine_ended_utc=ENGINE.get("ended_utc"))

def model_and_dates_records():
    """model identity (documented public release + Hugging Face facts read now + the snapshot actually loaded) and the
    date comparison with the manual edition — written as separate, citable records"""
    mc=model_cache_report();mi=dict(MODEL_IDENTITY) or model_identity_hub()
    rec=dict(model_id=MODEL_ID,loaded_snapshot_commit=mc.get("cached_snapshot_commit"),hub_main_commit=mi.get("hub_main_commit"),hub_repo_created=mi.get("hub_repo_created"),
             hub_last_modified=mi.get("hub_last_modified"),hub_note=mi.get("hub_note"),documented_public_release=MODEL_RELEASE,
             note="A repository creation time is not a public release date; the documented public release is the Qwen team announcement.",
             architecture=engine_architecture(),software=dict(torch=E["torch"].__version__,transformers=getattr(sys.modules.get("transformers"),"__version__",None),
             bitsandbytes=getattr(sys.modules.get("bitsandbytes"),"__version__",None)))
    MODEL_IDENTITY.update(rec);dump_json(MODEL_FILE,rec)
    rel=date.fromisoformat(MODEL_RELEASE["date"]);d0=(date(2025,7,1)-rel).days;d1=(date(2025,7,31)-rel).days
    dates=dict(model_public_release=MODEL_RELEASE["date"],model_release_source=MODEL_RELEASE["url"],
               document_edition=DOC_EDITION_MARK,document_edition_verified_on_document=DOC.get("edition_verified_on_document"),
               document_edition_pages=DOC.get("edition_mark_pages"),document_pdf_creation=DOC.get("pdf_metadata",{}).get("creationDate"),
               days_from_model_release_to_edition_month=[d0,d1],experiment_date_utc=INIT.get("started_utc"),
               statement=(f"The manual edition {DOC_EDITION_MARK} is {d0}–{d1} days after the documented public release of {MODEL_ID} ({MODEL_RELEASE['date']}); "
                          "the exact day of the edition is not printed."),
               caveat=("The date gap alone is NOT evidence that the model lacks this information: earlier SINUMERIK manuals and other public texts "
                       "may contain the same or similar content, and the vanilla 'UNKNOWN' answers also follow the prompt's instruction not to guess."))
    dump_json(DATES_FILE,dates);return rec,dates

def compute_verification():
    L=live_record();items=[]
    def add(name,ok,detail):items.append(dict(name=name,passed=bool(ok),detail=jsafe(detail)))
    add("ENGINE_STATUS_LIVE",L["status"]==ENGINE_PASS_STATUS,L["status"])
    ec=L["engine_checks"];add("ENGINE_GATES_PASSED",all(v is True for v in ec.values()),ec)
    add("ENGINE_SOURCE_LOCKS",all(any(l.startswith("PASS "+k) for l in L["engine_pass_lines"]) for k in ("TEST716_GIT_BLOB_LOCK","709_GIT_BLOB_LOCK")) and "718.py" in SOURCES,
        "718.py (this program) · 716.py and 709.py (engine PASS lines)")
    add("SOURCE_PDF_SHA256_AND_PAGES",DOC.get("sha256")==PDF_SHA256 and DOC.get("pages")==PDF_PAGES and ec.get("PDF_SHA256_LOCK") and ec.get("PDF_486_PAGES"),f"{DOC.get('pages')} pages · {str(DOC.get('sha256'))[:16]}…")
    d=STATE["disk_checks"][-1] if STATE["disk_checks"] else None;add("TEN_CARTRIDGES_SHA256_ON_SSD",bool(d and d["passed"]),f"{sum(1 for r in (d or {}).get('files',[]) if r['equals_engine_record'])}/{N_CART}")
    rr=L["rows"];okrows=[r for r in rr if r["physical"] is not None and r["cache_tokens"] and r["cache_tokens"]==r["expected_rows"]]
    add("TEN_PHYSICAL_READOUTS",len(okrows)==N_CART,f"{len(okrows)}/{N_CART} cartridges rebuilt to prefix + body rows and answered")
    add("TEN_VANILLA_CONTROLS",sum(1 for r in rr if r["vanilla"] is not None)==N_CART,f"{sum(1 for r in rr if r['vanilla'] is not None)}/{N_CART}")
    ab=[r for r in rr if r.get("ablation") is not None];add("REMOVAL_CONTROL_RECORDED",len(ab)==3,f"{len(ab)} cartridges (C01, C05, C10) asked again after release")
    add("SYNTHESIS_TEXT_MEDIATED",L["synthesis"]["mode"]=="VANILLA_TEXT_ONLY_OVER_PRIOR_PHYSICAL_READOUTS" and bool(L["synthesis"]["output"]),L["synthesis"]["mode"])
    add("WEIGHT_SENTINEL_ENGINE",L["sentinel_before"] is not None and L["sentinel_before"]==L["sentinel_after"],str(L["sentinel_after"])[:24])
    w=STATE["weight_checks"][-1] if STATE["weight_checks"] else None;add("WEIGHT_SENTINEL_AFTER_ALL_STEPS",bool(w and w["passed"]),(w or {}).get("after"))
    add("GPU_SAFETY_RESERVE_NOT_REDUCED",float(E["GPU_RESERVE_GIB"])>=EXPECTED_RESERVE_GIB,f"{E['GPU_RESERVE_GIB']} GiB")
    xs=STATE["xrays"];okx=[bid for bid,x in xs.items() if x["finite"] and x["layers"]==E["NL"] and x["tokens"]==next((r["cache_tokens"] for r in rr if r["id"]==bid),None)]
    add("TEN_XRAYS_FROM_LIVE_KV",len(okx)==N_CART,f"{len(okx)}/{N_CART} cartridges mounted alone, 80-layer K and V measured, released")
    add("COSINE_MAP_FROM_LIVE_H3",bool(L["cosine"]["matrix"]) and len(L["cosine"]["matrix"])==N_CART,L["cosine"]["metric"])
    rec=dict(session=SESSION_ID,utc=utc_now(),ready=all(i["passed"] for i in items),passed=sum(i["passed"] for i in items),total=len(items),items=items,
             semantics="NOT VERIFIED — answers are raw model output; page/section/word checks are automatic and are not expert verification",
             live_engine_status=L["status"],engine_started_utc=L["engine_started_utc"],engine_ended_utc=L["engine_ended_utc"],engine_seconds=L["engine_seconds"])
    STATE["verification"]=rec;dump_json(VERIFY_FILE,rec)
    dump_json(SESSION_DIR/"LIVE_MEASUREMENTS.json",L)
    slog("VERIFICATION","PASS" if rec["ready"] else "FAIL",passed=rec["passed"],total=rec["total"],failed=[i["name"] for i in items if not i["passed"]]);return rec

# ---------------------------------------------------------------------------------------------------------------------
# SEVEN RESEARCH FIGURES (JPEG 300 dpi, PNG lossless, PDF vector) — values ONLY from this live session and the PDF
# ---------------------------------------------------------------------------------------------------------------------
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.linewidth":.9,"axes.edgecolor":"#374151","axes.labelcolor":"#111827",
                     "xtick.color":"#374151","ytick.color":"#374151","xtick.labelsize":10.5,"ytick.labelsize":10.5,"axes.labelsize":12,
                     "axes.titlesize":13,"axes.titleweight":"bold","axes.titlelocation":"left","legend.fontsize":10.5,"legend.frameon":False})
FW,FH=13.333,7.5;OUT_DPI=300
INK,INK2,MUTED,RULE,PANEL="#111827","#374151","#6B7280","#D1D5DB","#F8FAFC"
TEAL,RED,AMBER,GREY="#0F766E","#B91C1C","#B45309","#9CA3AF"
FIGURES=OrderedDict([
    ("F1","Figure 1 — Physical memory mechanism"),("F2","Figure 2 — From the original 2025 Siemens PDF to ten physical cartridges"),
    ("F3","Figure 3 — SSD storage and physical restoration on the GPU"),("F4","Figure 4 — Technical answers: physical memory vs vanilla model"),
    ("F5","Figure 5 — Internal neural memory X-ray of the ten physical cartridges"),("F6","Figure 6 — Evidence map of the text-mediated synthesis"),
    ("F7","Figure 7 — Integrity and verification record")])
FIG_FILES={};LIVE={}
def mt(s):return str(s).replace("$",r"\$")
def wrap(s,n):return "\n".join(textwrap.wrap(str(s),n,break_long_words=True,break_on_hyphens=False)) or ""
def short(s,n):s=" ".join(str(s or "").split());return s if len(s)<=n else s[:n-1].rstrip()+"…"
def lines(s,width,n):
    """first n wrapped lines of a text (marked … when shortened) — display only; full text is in the records"""
    w=textwrap.wrap(" ".join(str(s or "").split()),width,break_long_words=True)
    return "\n".join(w[:n])+("…" if len(w)>n else "")
def plab(pc):
    return {"same page":"page ✓ same as heading","range contains heading page":"page ✓ range incl. heading","not stated":"page not stated"}.get(pc["result"],f"page ✗ differs by {pc['delta']}")
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
    ftext(fig,.035,.022*s,f"{APP_SHORT} · {ORG} · {LICENSE_NAME} · {COPYRIGHT} · 718.py {LOCKS['718.py'][:10]} · live session {SESSION_ID} · Fig. {k}/{len(FIGURES)}",
          minsize=6,fontsize=8.6,color=MUTED,va="center",family="DejaVu Sans Mono")
def box(fig,x,y,w,h,ec,fc="white",lw=1.6,r=.010,z=1):
    fig.add_artist(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={r}",transform=fig.transFigure,facecolor=fc,edgecolor=ec,lw=lw,zorder=z))
def arrow(fig,x0,y0,x1,y1,col=INK2,lw=1.8,ms=16,cs="arc3",ls="-",alpha=1):
    fig.add_artist(FancyArrowPatch((x0,y0),(x1,y1),transform=fig.transFigure,arrowstyle="-|>",mutation_scale=ms,lw=lw,color=col,connectionstyle=cs,zorder=5,linestyle=ls,alpha=alpha))
class LayoutQCError(RuntimeError):pass
def _hide_offview_ticks(fig):
    """tick labels outside an axis' view interval are never drawn by matplotlib; hide them so they are not measured"""
    for ax in fig.axes:
        for axis,(lo,hi) in ((ax.xaxis,sorted(ax.get_xlim())),(ax.yaxis,sorted(ax.get_ylim()))):
            eps=(hi-lo)*1e-6
            for tk in axis.get_major_ticks()+axis.get_minor_ticks():
                loc=tk.get_loc()
                if loc is None or loc<lo-eps or loc>hi+eps:
                    tk.label1.set_visible(False);tk.label2.set_visible(False)
def _texts(fig):
    import matplotlib.text as mtext
    return [t for t in fig.findobj(mtext.Text) if t.get_visible() and str(t.get_text()).strip() and t.get_gid()!="qc-ignore" and t.get_alpha()!=0]
def layout_qc(fig,max_rounds=8,tol=1.5):
    """automatic layout control before the JPEG is written: every visible text must lie inside the page and no two texts
    may overlap. Overlapping texts are shrunk step by step and checked again; a figure that still fails is rejected."""
    r=fig.canvas.get_renderer();W,H=fig.bbox.width,fig.bbox.height;rep=dict(rounds=0,fixed=0)
    for rnd in range(max_rounds+1):
        fig.canvas.draw();_hide_offview_ticks(fig);r=fig.canvas.get_renderer()   # final positions exist only after a draw
        ts=_texts(fig);bbs=[]
        for t in ts:
            b=t.get_window_extent(r);bbs.append((b.x0+tol,b.y0+tol,b.x1-tol,b.y1-tol))
        out=[i for i,b in enumerate(bbs) if b[0]<-1 or b[1]<-1 or b[2]>W+1 or b[3]>H+1]
        ov=[]
        for i in range(len(bbs)):
            a=bbs[i]
            for j in range(i+1,len(bbs)):
                c=bbs[j]
                if a[0]<c[2] and c[0]<a[2] and a[1]<c[3] and c[1]<a[3]:ov.append((i,j))
        rep.update(rounds=rnd,texts=len(ts),outside=[str(ts[i].get_text())[:60] for i in out],overlaps=[(str(ts[i].get_text())[:40],str(ts[j].get_text())[:40]) for i,j in ov][:20])
        if not out and not ov:rep["passed"]=True;return rep
        if rnd==max_rounds:break
        for i in set(out)|{x for p in ov for x in p}:
            t=ts[i]
            if t.get_fontsize()>5.5:t.set_fontsize(t.get_fontsize()-.5);rep["fixed"]+=1
    rep["passed"]=False;raise LayoutQCError(f"layout QC failed: {len(rep['outside'])} text(s) outside the page, {len(rep['overlaps'])} overlap(s): {rep['outside'][:3]} {rep['overlaps'][:3]}")
def jpeg_qc(path,min_w=3900,min_h=2190):
    """the written JPEG itself: opens, has the expected resolution and is not blank"""
    with Image.open(path) as im:
        im.load();w,h=im.size;fmt=im.format;arr=np.asarray(im.convert("L").resize((400,int(400*h/w))),dtype=np.float32)
    ok=(fmt=="JPEG" and w>=min_w and h>=min_h and float(arr.std())>8.0 and float((arr<200).mean())>0.01)
    rep=dict(format=fmt,pixels=[w,h],luma_std=round(float(arr.std()),2),ink_share=round(float((arr<200).mean()),4),passed=bool(ok))
    if not ok:raise LayoutQCError(f"JPEG check failed for {Path(path).name}: {rep}")
    return rep
def save_fig(fig,key,k):
    qc=layout_qc(fig)
    stem=f"FIGURE_{k:02d}_{key}"
    jpg=FIG_DIR/(stem+".jpg");png=FIG_DIR/(stem+".png");pdf=FIG_DIR/(stem+".pdf")
    fig.savefig(pdf,facecolor="white");buf=io.BytesIO();fig.savefig(buf,format="png",dpi=OUT_DPI,facecolor="white");plt.close(fig)
    png.write_bytes(buf.getvalue())
    with Image.open(io.BytesIO(buf.getvalue())) as im:im.convert("RGB").save(jpg,"JPEG",quality=95,optimize=True,subsampling=0,dpi=(OUT_DPI,OUT_DPI))
    jq=jpeg_qc(jpg);size=tuple(jq["pixels"])
    rec=dict(key=key,figure=k,title=FIGURES[f"F{k}"],jpg=str(jpg),png=str(png),pdf=str(pdf),pixels=list(size),jpg_bytes=jpg.stat().st_size,sha256_jpg=sha_file(jpg),utc=utc_now(),
             layout_qc=dict(passed=qc["passed"],texts=qc["texts"],fix_rounds=qc["rounds"],font_reductions=qc["fixed"]),jpeg_qc=jq,
             data="live session "+SESSION_ID+" · values traceable in LIVE_MEASUREMENTS.json / VERIFICATION_RECORD.json / SOURCE_DOCUMENT_RECORD.json")
    flog(f"FIGURE {k} {key} {size[0]}x{size[1]} jpg sha256 {rec['sha256_jpg']}");return rec
def _arch():
    a=engine_architecture()
    if not a:raise OpError("figures need the architecture measured by the engine in this session")
    return a
def pct(x):return "—" if x is None else f"{100*x:.0f} %"
def mib(b):return "—" if b is None else f"{b/2**20:,.0f} MiB"

def fig1(k=1):
    a=_arch();r=LIVE["rows"][0];n=r["cache_tokens"];c=a["cut"];L=a["layers"];kvb=a["full_kv_bytes_per_token"]
    fig=fig_base(k,"Physical memory mechanism — frozen Qwen2.5-72B-Instruct, CUT3",
                 f"{L} layers · hidden {a['hidden']:,} · {a['q_heads']} query / {a['kv_heads']} KV heads · head dim {a['head_dim']} · NF4 weights, BF16 K/V · frozen (measured in this session)",
                 "SCHEMATIC + LIVE VALUES",INK2)
    steps=[("1  FORGE",ccol(0),f"The frozen model reads ONE page range of the Siemens PDF (C01: {n:,} rows incl. prefix) in {a['chunk']}-token chunks."),
           ("2  PERSIST",INK2,f"Only H{c} and the K/V of layers 0–{c} are saved to SSD (.pt file + SHA-256)."),
           ("3  WRITE L0–L3",LOWER_COLOR,"Readout: lower-layer K/V rows come from the cartridge file; nothing is re-read from the PDF."),
           ("4  INJECT + REBUILD",UPPER_COLOR,f"Zero input embeddings; H{c} replaces the layer-{c} output; layers {c+1}–{L-1} recompute the rows."),
           ("5  ANSWER",ccol(0),f"Only the question is fed; greedy decoding, ≤ {READOUT_MAX_NEW} new tokens; then the memory is released.")]
    w=.172;g=(.93-5*w)/4
    for i,(t,col,body) in enumerate(steps):
        x=.035+i*(w+g);box(fig,x,.62,w,.205,col,lw=2)
        fig.add_artist(FancyBboxPatch((x,.785),w,.04,boxstyle="round,pad=0,rounding_size=0.010",transform=fig.transFigure,facecolor=col,edgecolor=col,zorder=2))
        ftext(fig,x+.01,.805,t,xmax=x+w-.006,fontsize=12.5,weight="bold",color="white",va="center",zorder=3)
        ftext(fig,x+.01,.768,wrap(body,27),xmax=x+w-.006,fontsize=10.3,color=INK,va="top",linespacing=1.3)
        if i<4:arrow(fig,x+w+.002,.72,x+w+g-.002,.72,ms=16)
    x0=.08;W=.86;bw=W/L;y=.44;hh=.07
    for li in range(L):
        fig.add_artist(Rectangle((x0+li*bw+(.004 if li>c else 0),y),bw*.82,hh,transform=fig.transFigure,facecolor=LOWER_COLOR if li<=c else UPPER_COLOR,edgecolor="none",zorder=2))
    for li in (0,c,20,40,60,L-1):fig.text(x0+li*bw+bw*.41+(.004 if li>c else 0),y-.025,f"L{li}",fontsize=10,ha="center",color=INK2)
    xc=x0+(c+1)*bw+.0015;fig.add_artist(Line2D([xc,xc],[y-.012,y+hh+.03],transform=fig.transFigure,color=CUT_COLOR,lw=3,zorder=4))
    fig.text(xc+.006,y+hh+.035,f"◀ CUT{c}: H{c} injected here (layer-{c} output)",fontsize=12,weight="bold",color=CUT_COLOR)
    fig.text(x0,y-.065,f"L0–L{c}: K/V rows written from the cartridge file ({c+1} layers)",fontsize=12,weight="bold",color=LOWER_COLOR)
    fig.text(x0+W,y-.065,f"L{c+1}–L{L-1}: recomputed at every readout ({L-c-1} layers)",fontsize=12,weight="bold",color=UPPER_COLOR,ha="right")
    facts=[("Cartridge file C01 (this session)",f"{r['file_bytes']:,} B" if r["file_bytes"] else "—",f"H{c} [1, {n:,}, {a['hidden']:,}] + K/V of L0–L{c}: 4 × 2 × [1, {a['kv_heads']}, {n:,}, {a['head_dim']}]"),
           ("Full live K/V rebuilt from C01",f"{n*kvb:,} B",f"{L} layers × {kvb:,} B per token = {n*kvb/2**30:.2f} GiB, only while mounted"),
           ("C01 physical readout (live)",f"{r['physical_wall_s']:.1f} s" if r["physical_wall_s"] else "—",f"SSD read + SHA {r['ssd_load_ms']/1000:.2f} s · host→GPU {r['h2d_ms']:.0f} ms · rebuild + {r['physical_tokens']}-token answer"),
           ("Ten cartridges, one at a time",f"{N_CART} × readout",f"each mounted alone, answered, then released — never jointly in GPU memory")]
    fw=(.93-3*.01)/4
    for i,(h1,v,sub) in enumerate(facts):
        x=.035+i*(fw+.01);box(fig,x,.11,fw,.2,RULE,fc=PANEL,lw=1)
        ftext(fig,x+.012,.285,h1,xmax=x+fw-.008,fontsize=11,weight="bold",color=INK2,va="top")
        ftext(fig,x+.012,.225,v,xmax=x+fw-.008,fontsize=17,weight="bold",color=INK,va="center")
        ftext(fig,x+.012,.175,wrap(sub,38),xmax=x+fw-.008,fontsize=10,color=INK2,va="top")
    fig_footer(fig,k,"Schematic illustration of the TEST709 CUT3 path as used by TEST718 (layer strip not to scale). Numbers were measured in this live session.")
    return save_fig(fig,"PHYSICAL_MEMORY_MECHANISM",k)

def fig2(k=2):
    rows=LIVE["rows"];mi=MODEL_IDENTITY;dt=json.loads(DATES_FILE.read_text()) if DATES_FILE.is_file() else {}
    fig=fig_base(k,"From the original 2025 Siemens PDF to ten physical cartridges",
                 f"{DOC_TITLE} · edition {DOC_EDITION_MARK} · downloaded from Siemens in this session · {DOC.get('pages')} PDF pages → C01–C10","LIVE SOURCE RECORD",TEAL)
    # source document card
    box(fig,.035,.585,.455,.255,TEAL,lw=1.8)
    fig.text(.047,.815,"Original source document (measured now)",fontsize=12.5,weight="bold",color=TEAL,va="center")
    dl=[("title",f"{DOC_TITLE} · software {DOC.get('software_version')} · order no. {DOC.get('order_number')}"),
        ("edition",f"“{DOC_EDITION_MARK}” printed on {DOC.get('edition_mark_pages')} of {DOC.get('pages')} pages — verified on the document"),
        ("download",f"{str(DOC.get('download_end_utc'))[:19].replace('T',' ')} UTC · {DOC.get('bytes',0):,} B · official Siemens address"),
        ("SHA-256",str(DOC.get("sha256"))),("metadata",f"PDF created {DOC.get('pdf_metadata',{}).get('creationDate')} · modified {DOC.get('pdf_metadata',{}).get('modDate')}")]
    for i,(kk,vv) in enumerate(dl):
        fig.text(.047,.775-i*.04,kk,fontsize=9.6,weight="bold",color=INK2,va="center")
        ftext(fig,.135,.775-i*.04,vv,xmax=.482,minsize=7,fontsize=9.6,color=INK,va="center",family="DejaVu Sans Mono" if kk=="SHA-256" else "DejaVu Sans")
    # model card
    box(fig,.51,.585,.455,.255,INK2,lw=1.4,fc=PANEL)
    fig.text(.522,.815,"Model (frozen, weights never changed)",fontsize=12.5,weight="bold",color=INK,va="center")
    ml=[("model",MODEL_ID),("public release",f"{MODEL_RELEASE['date']} — Qwen Team blog “Qwen2.5: A Party of Foundation Models!”"),
        ("loaded snapshot",str(mi.get("loaded_snapshot_commit") or "not determinable at run time")),
        ("Hugging Face",f"repo created {str(mi.get('hub_repo_created'))[:10]} · last modified {str(mi.get('hub_last_modified'))[:10]} (read now)" if mi.get("hub_repo_created") else str(mi.get("hub_note"))),
        ("weights","NF4 4-bit (bitsandbytes), BF16 compute · TEST709 weight sentinel unchanged")]
    for i,(kk,vv) in enumerate(ml):
        fig.text(.522,.775-i*.04,kk,fontsize=9.6,weight="bold",color=INK2,va="center")
        ftext(fig,.618,.775-i*.04,vv,xmax=.957,minsize=7,fontsize=9.6,color=INK,va="center",family="DejaVu Sans Mono" if kk=="loaded snapshot" else "DejaVu Sans")
    # timeline
    t0=date(2024,7,1);t1=max(date.fromisoformat(INIT["started_utc"][:10]),date(2025,10,1))
    def X(d):return .08+.84*(d-t0).days/max(1,(t1-t0).days)
    yl=.505;fig.add_artist(Line2D([.08,.92],[yl,yl],transform=fig.transFigure,color=INK2,lw=1.4))
    for yr in range(t0.year,t1.year+1):
        for mo in (1,7):
            d=date(yr,mo,1)
            if t0<=d<=t1:fig.add_artist(Line2D([X(d),X(d)],[yl-.006,yl+.006],transform=fig.transFigure,color=INK2,lw=1));fig.text(X(d),yl-.025,f"{yr}-{mo:02d}",fontsize=8.6,ha="center",color=MUTED)
    rel=date.fromisoformat(MODEL_RELEASE["date"]);ed0=date(2025,7,1);ed1=date(2025,7,31);ex=date.fromisoformat(INIT["started_utc"][:10])
    fig.add_artist(Rectangle((X(ed0),yl-.012),X(ed1)-X(ed0),.024,transform=fig.transFigure,facecolor=TEAL,edgecolor="none"))
    for d,lab,col,dy in ((rel,f"model public release\n{MODEL_RELEASE['date']}",INK,.02),(ed0,f"manual edition {DOC_EDITION_MARK}\n(month printed; day not printed)",TEAL,.02),(ex,f"this experiment\n{ex.isoformat()}",UPPER_COLOR,.02)):
        fig.add_artist(Line2D([X(d)],[yl],transform=fig.transFigure,marker="o",ms=8,color=col));fig.text(X(d),yl+dy,lab,fontsize=9.4,ha="center",va="bottom",color=col,weight="bold")
    ftext(fig,.08,.462,wrap(f"{dt.get('statement','')} {dt.get('caveat','')}",215),xmax=.955,minsize=7,fontsize=8.4,color=AMBER,va="top",linespacing=1.2)
    # page strip → cartridges
    y0=.2;hh=.07;x0=.06;W=.9;N=DOC.get("pages") or PDF_PAGES
    fig.text(x0,.372,f"PDF pages 1–{N} → ten physical cartridges (page ranges fixed by TEST716; token counts measured in this session)",fontsize=11.5,weight="bold",color=INK)
    mx=max(r["body_tokens"] for r in rows)
    for r in rows:
        a_,b_=r["pages"];xa=x0+W*(a_-1)/N;wa=W*(b_-a_+1)/N;col=ccol(r["index"])
        fig.add_artist(Rectangle((xa,y0),wa-.002,hh,transform=fig.transFigure,facecolor=col,edgecolor="none"))
        fig.text(xa+wa/2,y0+hh/2+.012,r["id"],fontsize=11,weight="bold",color="white",ha="center",va="center")
        ftext(fig,xa+wa/2,y0+hh/2-.018,f"p. {a_}–{b_}",xmax=xa+wa-.002,xmin=xa+.001,minsize=6,fontsize=8.4,color="white",ha="center",va="center")
        bh=.05*r["body_tokens"]/mx;fig.add_artist(Rectangle((xa+wa*.2,y0+hh+.006),wa*.6,bh,transform=fig.transFigure,facecolor=col,alpha=.35,edgecolor="none"))
        fig.text(xa+wa/2,y0+hh+.008+bh,f"{r['body_tokens']:,}",fontsize=8.4,color=INK2,ha="center",va="bottom")
        fig.text(xa+wa/2,y0-.022,f"{r['heading_page']}",fontsize=8,color=MUTED,ha="center")
    fig.text(x0,y0-.045,"bars above: body tokens per cartridge · numbers below: PDF page of the heading used for the cartridge's TEST718 question",fontsize=8.8,color=MUTED)
    fig_footer(fig,k,"Source: official Siemens address (see SOURCE_DOCUMENT_RECORD.json; © Siemens AG, not redistributed) · MODEL_IDENTITY_RECORD.json · DATE_COMPARISON_RECORD.json.")
    return save_fig(fig,"SIEMENS_PDF_TO_TEN_CARTRIDGES",k)

def fig3(k=3):
    rows=LIVE["rows"]
    fig=fig_base(k,"SSD storage and physical restoration on the GPU",
                 "Ten cartridge files on SSD · each readout loads ONE file, checks its SHA-256, rebuilds the 80-layer memory, answers and releases it","LIVE SESSION MEASUREMENT",TEAL)
    fig.text(.035,.815,"SSD — ten cartridge files (this session)",fontsize=13,weight="bold",color=INK)
    for r in rows:
        y=.775-r["index"]*.052;col=ccol(r["index"])
        fig.add_artist(Rectangle((.035,y-.016),.008,.032,transform=fig.transFigure,facecolor=col,edgecolor="none"))
        fig.text(.05,y,r["id"],fontsize=10.5,weight="bold",color=col,va="center")
        ftext(fig,.085,y+.008,f"{mib(r['file_bytes'])} · {r['body_tokens']:,} tokens",xmax=.33,fontsize=9.4,color=INK,va="center")
        ftext(fig,.085,y-.011,f"SHA-256 {str(r['cartridge_sha256'])[:20]}… {'✓ re-verified' if r['file_sha_ok'] else '✗'}",xmax=.33,fontsize=8.2,color=TEAL if r["file_sha_ok"] else RED,va="center",family="DejaVu Sans Mono")
    arrow(fig,.335,.53,.39,.53,lw=2.2,ms=20);fig.text(.3625,.555,"one at\na time",fontsize=9.5,ha="center",color=INK,weight="bold")
    ax=fig.add_axes([.47,.33,.48,.43]);ys=np.arange(len(rows))[::-1]
    ssd=np.array([(r["ssd_load_ms"] or 0)/1000 for r in rows]);h2d=np.array([(r["h2d_ms"] or 0)/1000 for r in rows])
    wall=np.array([r["physical_wall_s"] if r["physical_wall_s"] is not None else np.nan for r in rows]);rest=np.clip(wall-ssd-h2d,0,None)
    ax.barh(ys,ssd,color="#94A3B8",label="SSD read + SHA-256");ax.barh(ys,h2d,left=ssd,color="#475569",label="host → GPU")
    ax.barh(ys,rest,left=ssd+h2d,color=[ccol(r["index"]) for r in rows],alpha=.85,label="rebuild L4–L79 + answer (colour = cartridge)")
    for yy,r,wv in zip(ys,rows,wall):
        if not np.isnan(wv):ax.text(wv*1.01,yy,f"{wv:.0f} s · {r['cache_tokens']:,} rows · {r['physical_tokens']} tok",va="center",fontsize=8.8,color=INK2)
    ax.set_yticks(ys);ax.set_yticklabels([r["id"] for r in rows]);ax.set_xlabel("seconds (wall time between engine output lines, UTC-stamped)",fontsize=10)
    ax.set_xlim(0,np.nanmax(wall)*1.45 if np.isfinite(np.nanmax(wall)) else 1);ax.legend(loc="lower left",bbox_to_anchor=(0,1.0),ncol=3,fontsize=8.6,handlelength=1.2,columnspacing=1.0)
    ax.grid(axis="x",color="#E5E7EB",lw=.6);ax.set_axisbelow(True);fig.text(.47,.815,"Physical readout per cartridge (live TEST718)",fontsize=13,weight="bold",color=INK)
    for sp in ("top","right"):ax.spines[sp].set_visible(False)
    box(fig,.035,.088,.93,.16,"#0F766E",fc="#F0FDFA",lw=1.2)
    fig.text(.045,.23,PREV_TITLE,fontsize=10.5,weight="bold",color=TEAL,va="center")
    ftext(fig,.045,.208,wrap(PREV_TEXT,180),xmax=.958,minsize=7.5,fontsize=9,color=INK,va="top",linespacing=1.25)
    ftext(fig,.045,.153,wrap(PREV_SEE,180),xmax=.958,minsize=7,fontsize=9,color=INK2,va="top",weight="bold",linespacing=1.25)
    fig_footer(fig,k,"Previously published research (box) is not a result of this experiment. Timings: LIVE_MEASUREMENTS.json · engine output with UTC time stamps.")
    return save_fig(fig,"SSD_STORAGE_GPU_RESTORATION",k)

def fig4(k=4):
    rows=LIVE["rows"]
    fig=fig_base(k,"Technical answers: physical memory vs vanilla model",
                 f"Same frozen model, same question, greedy decoding, ≤ {READOUT_MAX_NEW} new tokens · vanilla = no PDF, no cartridge · answers are raw and NOT verified","LIVE · NOT VERIFIED",AMBER)
    XM,XH,XV,XP,XC=.035,.075,.29,.47,.86;y=.825
    for xx,t in ((XM,""),(XH,"section heading in the PDF (page)"),(XV,"vanilla answer"),(XP,"answer with the physical cartridge"),(XC,"automatic checks")):fig.text(xx,y,t,fontsize=9.8,weight="bold",color=MUTED)
    rh=.054
    for r in rows:
        yy=y-.03-r["index"]*rh;col=ccol(r["index"])
        fig.text(XM,yy,r["id"],fontsize=10,weight="bold",color=col,va="top")
        ftext(fig,XH,yy,f"{r['heading']} (p. {r['heading_page']})",xmax=XV-.008,minsize=7.4,trunc=True,fontsize=9,color=INK,va="top")
        ftext(fig,XV,yy,short(r["vanilla"],60),xmax=XP-.008,minsize=7.2,trunc=True,fontsize=8.4,color=MUTED,va="top",family="DejaVu Sans Mono")
        ftext(fig,XP,yy,lines(r["physical"],88,2),xmax=XC-.008,minsize=6.8,fontsize=8,color=INK,va="top",family="DejaVu Sans Mono",linespacing=1.15)
        pc=r["page_physical"];sp=r["support_physical"]["share"];sv=r["support_vanilla"]["share"]
        ftext(fig,XC,yy,plab(pc),xmax=.965,minsize=7,fontsize=8.4,color=TEAL if pc["result"] in ("same page","range contains heading page") else (MUTED if pc["result"]=="not stated" else RED),va="top")
        ftext(fig,XC,yy-.018,f"5-gram support {pct(sp)} vs {pct(sv)}",xmax=.965,minsize=7,fontsize=8.2,color=INK2,va="top")
    # removal control (small)
    ab=[r for r in rows if r.get("ablation") is not None]
    box(fig,.035,.09,.93,.135,AMBER,fc="#FFFBEB",lw=1.2)
    fig.text(.045,.207,"Removal control — the same question asked again AFTER the cartridge was released (TEST718 ablation)",fontsize=10.2,weight="bold",color=AMBER,va="center")
    for i,r in enumerate(ab):
        x=.045+i*.31
        fig.text(x,.18,r["id"],fontsize=9.6,weight="bold",color=ccol(r["index"]),va="center")
        ftext(fig,x+.035,.18,"with: "+short(r["physical"],40),xmax=x+.3,minsize=7,trunc=True,fontsize=8.2,color=INK,va="center",family="DejaVu Sans Mono")
        ftext(fig,x+.035,.152,"after release: "+short(r["ablation"],34),xmax=x+.3,minsize=7,trunc=True,fontsize=8.2,color=INK2,va="center",family="DejaVu Sans Mono")
        ftext(fig,x+.035,.124,f"identical to the vanilla answer: {'yes' if r.get('ablation_equals_vanilla') else 'no'}",xmax=x+.3,fontsize=8.4,color=TEAL if r.get("ablation_equals_vanilla") else RED,va="center",weight="bold")
    ftext(fig,.045,.102,"Checks are automatic: stated PDF page vs the page where the heading occurs; share of the answer's word 5-grams (not copied from the question) found verbatim in the cartridge's PDF pages (physical vs vanilla). Not an expert evaluation.",
          xmax=.958,minsize=6.8,fontsize=8,color=INK2,va="center")
    fig_footer(fig,k,"Full raw answers: live engine output, LIVE_TEST718_RESULTS_this_session.json and RUN_SUMMARY.txt (… = shortened for display only).")
    return save_fig(fig,"ANSWERS_PHYSICAL_VS_VANILLA",k)

def fig5(k=5):
    xs=STATE.get("xrays") or {};ids=cart_ids()
    if len(xs)!=len(ids):raise OpError("Figure 5 needs the read-only X-ray of all ten cartridges from this session (no synthetic heat map is drawn).")
    rows={r["id"]:r for r in LIVE["rows"]};t0=min(x["utc"] for x in xs.values());t1=max(x["released_utc"] for x in xs.values())
    fig=fig_base(k,"Internal neural memory X-ray — ten physical cartridges, 80 layers each",
                 f"Live GPU K/V tensors · each cartridge mounted ALONE, measured read-only, released · {t0[:19].replace('T',' ')} → {t1[11:19]} UTC · bin {xs[ids[0]]['bin_tokens']} tokens",
                 "LIVE GPU MEASUREMENT",TEAL)
    def z(m):
        m=np.asarray(m,dtype=float);mu=np.nanmean(m,axis=1,keepdims=True);sd=np.nanstd(m,axis=1,keepdims=True);return (m-mu)/np.where(sd>0,sd,1)
    X0,X1,Y0,Y1=.075,.905,.14,.832;nc=5;gx=.012;gy=.048;pw=(X1-X0-(nc-1)*gx)/nc;ph=(Y1-Y0-3*gy)/4
    order=[("K",ids[:5]),("V",ids[:5]),("K",ids[5:]),("V",ids[5:])];im=None
    for ri,(kv,grp) in enumerate(order):
        y=Y1-(ri+1)*ph-ri*gy
        fig.text(.035,y+ph/2,f"‖{kv}‖",fontsize=13,weight="bold",color=INK if kv=="K" else UPPER_COLOR,va="center",ha="left",rotation=90)
        for ci,bid in enumerate(grp):
            x=xs[bid];r=rows.get(bid,{});col=ccol(cart_index(bid));px=X0+ci*(pw+gx)
            ax=fig.add_axes([px,y,pw,ph]);M=z(x["k_norm" if kv=="K" else "v_norm"]);nb=M.shape[1]
            im=ax.imshow(M,aspect="auto",origin="lower",cmap="RdBu_r",vmin=-2.5,vmax=2.5,interpolation="nearest")
            ax.axhline(x["cut"]+.5,color=CUT_COLOR,lw=1.2,ls="--")
            ax.set_yticks([0,40,x["layers"]-1]);ax.set_yticklabels(["0","40",str(x["layers"]-1)] if ci==0 else [],fontsize=7.6)
            ax.set_xticks([0,nb-1]);ax.set_xticklabels(["0",f"{x['tokens']:,}"],fontsize=7.2)
            ax.tick_params(length=2,pad=1.5)
            for sp in ax.spines.values():sp.set_edgecolor(col);sp.set_linewidth(1.6)
            pg=r.get("pages") or ["?","?"]
            ftext(fig,px,y+ph+.006,f"{bid} · {kv}",xmax=px+pw*.42,fontsize=9.6,weight="bold",color=col,va="bottom")
            ftext(fig,px+pw,y+ph+.006,f"p. {pg[0]}–{pg[1]} · {x['tokens']:,} rows",xmin=px+pw*.44,xmax=px+pw,minsize=5.8,fontsize=7.4,color=INK2,va="bottom",ha="right")
    cax=fig.add_axes([.918,Y0,.01,Y1-Y0]);cb=fig.colorbar(im,cax=cax);cb.set_label("z (per layer, per panel)",fontsize=9);cb.ax.tick_params(labelsize=8)
    fig.text(.075,.1,"y axis: layer 0–79 (dashed line = CUT3: below L0–L3 from the cartridge file, above L4–L79 recomputed) · x axis: memory row (token position) · K and V are shown in separate rows",
             fontsize=8.6,color=INK2,va="center")
    fig_footer(fig,k,"Read-only measurement of this session's GPU tensors, one cartridge at a time (XRAY_TEN_CARTRIDGES.json: method, UTC times, absolute values). Never jointly in GPU memory.")
    return save_fig(fig,"TEN_CARTRIDGE_KV_XRAY",k)

def fig6(k=6):
    rows=LIVE["rows"];S=LIVE["synthesis"]
    if not S.get("output"):raise OpError("figure 6 needs the live synthesis output")
    fig=fig_base(k,"Evidence map of the text-mediated synthesis",
                 "Cartridge → physical readout (text) → synthesis by the frozen model with NO cartridge attached · lines = recorded citations, not neural measurement","LIVE · TEXT-MEDIATED",AMBER)
    xc,xr,xs=.035,.2,.72;top=.79;rh=.058
    fig.text(xc,top+.03,"cartridge",fontsize=10,weight="bold",color=MUTED);fig.text(xr,top+.03,"physical readout (generated text, tokens)",fontsize=10,weight="bold",color=MUTED)
    fig.text(xs,top+.03,"synthesis output",fontsize=10,weight="bold",color=MUTED)
    mxc=max([v for v in S["citations"].values()]+[1])
    sy0,sy1=.18,top+.005
    for r in rows:
        y=top-r["index"]*rh-.02;col=ccol(r["index"])
        box(fig,xc,y-.018,.12,.036,col,lw=1.4)
        ftext(fig,xc+.006,y,f"{r['id']} · p. {r['pages'][0]}–{r['pages'][1]}",xmax=xc+.118,fontsize=8.8,weight="bold",color=col,va="center")
        arrow(fig,xc+.122,y,xr-.004,y,col=col,lw=1.2,ms=10)
        box(fig,xr,y-.022,.4,.044,RULE,fc=PANEL,lw=1)
        ftext(fig,xr+.006,y,lines(f"{r['physical_tokens']} tok · "+str(r["physical"]),92,2),xmax=xr+.396,minsize=6.4,fontsize=7.4,color=INK,va="center",family="DejaVu Sans Mono",linespacing=1.1)
        nc=S["citations"].get(r["id"],0);ty=sy1-(sy1-sy0)*(r["index"]+.5)/len(rows)
        if nc>0:arrow(fig,xr+.402,y,xs-.004,ty,col=col,lw=.8+3.2*nc/mxc,ms=10,alpha=.85)
        else:arrow(fig,xr+.402,y,xs-.004,ty,col=GREY,lw=.8,ms=8,ls=(0,(3,3)),alpha=.7)
        ftext(fig,xr+.41,y+.012,f"cited ×{nc} · reuse {pct(S['reuse'].get(r['id']))}",xmax=xs-.012,fontsize=8,color=col if nc else MUTED,va="center")
    box(fig,xs,sy0,.245,sy1-sy0,AMBER,fc="#FFFBEB",lw=1.6)
    fig.text(xs+.01,sy1-.025,"Synthesis (TEST718)",fontsize=11.5,weight="bold",color=AMBER,va="center")
    info=[f"{S.get('tokens')} tokens{' — limit reached' if S.get('truncated') else ''} (≤ {SYNTH_MAX_NEW})",f"input: {S.get('input_tokens')} tokens of text",
          f"mode: {S.get('mode')}",f"cartridges cited: {sum(1 for v in S['citations'].values() if v)}/{len(rows)}"]
    for i,t in enumerate(info):ftext(fig,xs+.01,sy1-.055-i*.025,t,xmax=xs+.24,minsize=6.4,fontsize=8.6,color=INK,va="center")
    ftext(fig,xs+.01,sy1-.165,wrap(short(S["output"],560),48),xmax=xs+.24,minsize=6,fontsize=7.4,color=INK2,va="top",family="DejaVu Sans Mono",linespacing=1.15)
    ftext(fig,.035,.135,wrap("How the synthesis was produced (TEST718): the ten cartridges were read one at a time; each readout produced text; the ten texts were concatenated "
                             "with their cartridge IDs and given to the same frozen model with NO cartridge in memory. Line width = how often the synthesis text cites the "
                             "cartridge ID; reuse = share of the readout's word 5-grams that reappear verbatim in the synthesis. Both are text records, not measurements of neural synthesis.",175),
          xmax=.958,minsize=7,fontsize=8.8,color=INK,va="top")
    fig_footer(fig,k,"Full synthesis input and output: LIVE_TEST718_RESULTS_this_session.json (synthesis_input / synthesis_output) and the live engine output.")
    return save_fig(fig,"SYNTHESIS_EVIDENCE_MAP",k)

def fig7(k=7):
    v=STATE.get("verification")
    if not v:raise OpError("figure 7 needs the live verification record")
    fig=fig_base(k,"Integrity and verification record — this live session",f"Locked sources · original document · ten cartridges · frozen weights · live verification ({v['passed']}/{v['total']} passed)",
                 "LIVE VERIFICATION",TEAL if v["ready"] else RED)
    fig.text(.035,.8,"Live verification",fontsize=13.5,weight="bold",color=INK);y=.765
    for it in v["items"]:
        ok=it["passed"];fig.text(.035,y,"PASS" if ok else "FAIL",fontsize=9.4,weight="bold",color=TEAL if ok else RED,va="top",family="DejaVu Sans Mono")
        ftext(fig,.072,y,it["name"],xmax=.33,fontsize=8.8,color=INK,va="top",family="DejaVu Sans Mono")
        ftext(fig,.072,y-.017,short(it["detail"] if isinstance(it["detail"],str) else json.dumps(it["detail"],ensure_ascii=False),80),xmax=.33,minsize=6.4,trunc=True,fontsize=7.4,color=MUTED,va="top")
        y-=.0395
    fig.text(.36,.8,"Locked identities",fontsize=13.5,weight="bold",color=INK);y=.765
    ids=[("718.py",LOCKS["718.py"]),("716.py",LOCKS["716.py"]),("709.py",LOCKS["709.py"]),("Siemens PDF SHA-256",str(DOC.get("sha256"))),
         ("model",f"{MODEL_ID} @ {str(MODEL_IDENTITY.get('loaded_snapshot_commit') or 'snapshot n/a')[:16]}"),
         ("weight sentinel",str(LIVE.get("sentinel_after"))[:40]+"…"),("engine run",f"{str(LIVE.get('engine_started_utc'))[:19]} → {str(LIVE.get('engine_ended_utc'))[:19]} UTC")]
    for kk,vv in ids:
        fig.text(.36,y,kk,fontsize=9.4,weight="bold",color=INK2,va="top");ftext(fig,.36,y-.02,vv,xmax=.67,minsize=6.2,fontsize=8,color=INK,va="top",family="DejaVu Sans Mono");y-=.05
    fig.text(.36,y-.005,"Cartridge SHA-256 (re-verified on SSD)",fontsize=9.4,weight="bold",color=INK2,va="top");y-=.027
    for r in LIVE["rows"]:
        ftext(fig,.36,y,f"{r['id']} {r['cartridge_sha256']}",xmax=.67,minsize=5.8,fontsize=7.2,color=ccol(r["index"]),va="top",family="DejaVu Sans Mono");y-=.0175
    box(fig,.69,.205,.275,.62,RULE,fc="#F3F4F6",lw=1)
    fig.text(.7,.8,"Research lineage (published)",fontsize=11.5,weight="bold",color=INK2,va="center");yy=.77
    for t,u in LINEAGE:
        ftext(fig,.7,yy,t,xmax=.958,minsize=7,fontsize=8.8,weight="bold",color=INK,va="top");ftext(fig,.7,yy-.022,u,xmax=.958,minsize=6.5,fontsize=8,color=INK2,va="top",family="DejaVu Sans Mono");yy-=.06
    ftext(fig,.7,yy-.005,"This experiment: unpublished — no DOI",xmax=.958,fontsize=9,weight="bold",color=RED,va="top");yy-=.04
    fig.text(.7,yy,"Historical reference (not this session)",fontsize=10,weight="bold",color=INK2,va="top");yy-=.025
    for n in HISTORICAL:ftext(fig,.7,yy,f"{n} · blob {LOCKS[n][:12]}…",xmax=.958,minsize=6.5,fontsize=8,color=INK2,va="top",family="DejaVu Sans Mono");yy-=.02
    ftext(fig,.7,yy-.01,wrap("Published logs of earlier runs are kept separately and are never used for the live verification.",44),xmax=.958,minsize=6.5,fontsize=8,color=MUTED,va="top")
    box(fig,.035,.09,.93,.1,RULE,fc=PANEL,lw=1)
    ftext(fig,.045,.175,f"Answers are raw model output and NOT verified technical truth · engine status {LIVE.get('status')}",xmax=.958,minsize=7,fontsize=9,color=INK,va="top")
    ftext(fig,.045,.148,f"Source document {DOC_TITLE}, edition {DOC_EDITION_MARK}, {DOC.get('pages')} pages, downloaded {str(DOC.get('download_end_utc'))[:19]} UTC from the official Siemens address.",xmax=.958,minsize=7,fontsize=9,color=INK,va="top")
    ftext(fig,.045,.121,f"Model public release {MODEL_RELEASE['date']} ({MODEL_RELEASE['url']}) · {LIVE['rows'][0]['id']}–{LIVE['rows'][-1]['id']} forged with the unchanged TEST709 CUT3 engine · "
                        f"GPU reserve {E.get('GPU_RESERVE_GIB')} GiB unchanged.",xmax=.958,minsize=7,fontsize=9,color=INK2,va="top")
    fig_footer(fig,k,f"Live records: VERIFICATION_RECORD.json · LIVE_MEASUREMENTS.json · live engine output (UTC-stamped) · SHA256_MANIFEST.json (session {SESSION_ID}).")
    return save_fig(fig,"INTEGRITY_VERIFICATION_RECORD",k)

FIG_FUNCS=OrderedDict([("F1",fig1),("F2",fig2),("F3",fig3),("F4",fig4),("F5",fig5),("F6",fig6),("F7",fig7)])
def render_figures():
    """renders all figures on the CPU from this session's live data (no GPU use)"""
    global LIVE
    LIVE=live_record();out={};errs={}
    for i,(key,fn) in enumerate(FIG_FUNCS.items(),1):
        t=time.perf_counter()
        try:rec=fn(i);out[key]=rec;FIG_FILES[key]=rec;_OUT.write(f"  figure {i}/{len(FIG_FUNCS)} · {rec['pixels'][0]}×{rec['pixels'][1]} JPEG · {rec['jpg_bytes']/1e6:.1f} MB · {time.perf_counter()-t:.1f} s · {Path(rec['jpg']).name}\n")
        except Exception as ex:errs[key]=f"{type(ex).__name__}: {ex}";FIG_FILES.pop(key,None);flog(f"FIGURE {i} NOT GENERATED {traceback.format_exc()[-1500:]}");_OUT.write(f"  figure {i} NOT GENERATED · {errs[key]}\n")
        _OUT.flush()
    dump_json(SESSION_DIR/"FIGURES_MANIFEST.json",dict(session=SESSION_ID,utc=utc_now(),data_source="live session only",figures=FIG_FILES,not_generated=errs))
    slog("FIGURES",f"{len(out)} rendered",not_generated=errs);return out,errs

# ---------------------------------------------------------------------------------------------------------------------
# research summary, downloadable artifacts (actual files of this session; the Siemens PDF itself is never packaged)
# ---------------------------------------------------------------------------------------------------------------------
RUN_SUMMARY=SESSION_DIR/"RUN_SUMMARY.txt"
ZIP_PATH=SESSION_DIR/f"{SESSION_ID}_AKBASCORE_SIEMENS_ALL_RESEARCH_ARTIFACTS.zip";MANIFEST=SESSION_DIR/"SHA256_MANIFEST.json"
def write_run_summary():
    R7=E.get("R718",{});v=STATE.get("verification") or {};L=[];a=L.append;Lr=LIVE if LIVE else {}
    a(f"{APP_TITLE}\n{VERSION_NOTE}\nsession {SESSION_ID} · started {SESSION_INFO['started_local']} ({INIT['started_utc']} UTC) · written {local_now()}\n")
    a("EXPERIMENT  TEST718 — ten physical CUT3 cartridges of a real industrial manual, vanilla controls, removal control, text-mediated synthesis")
    a(f"ENGINE      718.py git blob {LOCKS['718.py']} (executed unchanged) · 716.py {LOCKS['716.py']} · 709.py {LOCKS['709.py']}")
    a(f"            engine run {ENGINE.get('started_utc')} → {ENGINE.get('ended_utc')} UTC ({ENGINE.get('seconds')} s) · status {R7.get('status')}")
    mi=MODEL_IDENTITY
    a(f"MODEL       {MODEL_ID} · NF4 4-bit, BF16 compute, frozen · loaded snapshot {mi.get('loaded_snapshot_commit')} · Hub main {mi.get('hub_main_commit')}")
    a(f"            first public release {MODEL_RELEASE['date']} — {MODEL_RELEASE['source']} — {MODEL_RELEASE['url']} ({MODEL_RELEASE['checked']})")
    a(f"            Hugging Face repository created {mi.get('hub_repo_created')} · last modified {mi.get('hub_last_modified')} (creation is not publication)")
    a(f"DOCUMENT    {DOC_TITLE} · edition {DOC_EDITION_MARK} (printed on {DOC.get('edition_mark_pages')} of {DOC.get('pages')} pages — verified on the document)")
    a(f"            order no. {DOC.get('order_number')} · software {DOC.get('software_version')} · {DOC.get('bytes')} bytes · SHA-256 {DOC.get('sha256')}")
    a(f"            downloaded {DOC.get('download_start_utc')} → {DOC.get('download_end_utc')} UTC from {PDF_URL}")
    a(f"            PDF metadata: created {DOC.get('pdf_metadata',{}).get('creationDate')} · modified {DOC.get('pdf_metadata',{}).get('modDate')}")
    a(f"            {PDF_POLICY} ({PDF_TERMS_URL})")
    if DATES_FILE.is_file():
        d=json.loads(DATES_FILE.read_text());a(f"DATES       {d['statement']}\n            {d['caveat']}")
    a("\nINITIALIZATION (this session)")
    for st in INIT["steps"]:a(f"  ✓ {st['step']:<13} {st['seconds']:>9.1f} s  {st['title']}")
    if INIT.get("failed"):a(f"  ✗ {INIT['failed']['step']}  {INIT['failed']['error']}  (last successful: {INIT['failed']['last_successful_step']})")
    if Lr.get("rows"):
        a("\nTEN PHYSICAL CARTRIDGES AND ANSWERS (raw, NOT verified; automatic checks only)")
        for r in Lr["rows"]:
            a(f"\n  {r['id']}  PDF pages {r['pages'][0]}–{r['pages'][1]} · {r['body_tokens']} tokens · rows {r['cache_tokens']} · file {r['file_bytes']} B · SHA-256 {r['cartridge_sha256']}")
            a(f"      heading: {r['heading']} (PDF page {r['heading_page']}, section {r['section']})")
            a(f"      readout: SSD+SHA {r['ssd_load_ms']} ms · H2D {r['h2d_ms']} ms · wall {r['physical_wall_s']} s · answer {r['physical_tokens']} tokens{' (limit reached)' if r['physical_truncated'] else ''}")
            a(f"      checks : stated page {r['page_physical']['stated']} → {r['page_physical']['result']} · section number stated {r['section_physical']['stated']} · "
              f"5-gram support physical {pct(r['support_physical']['share'])} vs vanilla {pct(r['support_vanilla']['share'])}")
            a(f"      Q: {r['question']}\n      VANILLA  → {r['vanilla']}\n      PHYSICAL → {r['physical']}")
            if r.get("ablation") is not None:a(f"      AFTER RELEASE → {r['ablation']}  (identical to vanilla: {r.get('ablation_equals_vanilla')})")
        S=Lr["synthesis"]
        a(f"\nSYNTHESIS  mode {S['mode']} · {S['tokens']} tokens{' (limit reached)' if S['truncated'] else ''} · citations {S['citations']}")
        a("  The ten readouts were generated one cartridge at a time; their texts were concatenated and given to the frozen model with NO cartridge attached.")
        a("  "+str(S["output"]).replace("\n","\n  "))
        a(f"\nCOSINE MAP  {Lr['cosine']['metric']} · {Lr['cosine']['limit']}")
        for i,lab in enumerate(Lr["cosine"].get("labels") or []):a(f"  {lab} "+" ".join(f"{v:.3f}" for v in Lr["cosine"]["matrix"][i]))
    if STATE["xrays"]:
        a("\nTEN-CARTRIDGE X-RAY (each cartridge mounted alone, measured read-only, released — never jointly in GPU memory)")
        for bid,x in STATE["xrays"].items():a(f"  {bid} mounted {x['mount']['utc']} · measured {x['utc']} · released {x['released_utc']} UTC · {x['tokens']} rows × {x['layers']} layers · mean ‖K‖ {x['k_mean']:.3f} · mean ‖V‖ {x['v_mean']:.3f}")
    a(f"\nLIVE VERIFICATION  {v.get('passed','—')}/{v.get('total','—')} passed")
    for i in v.get("items",[]):a(f"  {'PASS' if i['passed'] else 'FAIL'}  {i['name']}  {i['detail'] if isinstance(i['detail'],str) else json.dumps(i['detail'],ensure_ascii=False)}")
    if any(r.get("origin")=="user" for r in STATE["qa"]+STATE["controls"]):
        a("\nQUESTIONS ASKED IN THE INTERFACE")
        for r in STATE["qa"]+STATE["controls"]:
            if r.get("origin")=="user":a(f"  [{r['cartridge'] or 'vanilla'}] {r['question']}\n      → {r['raw']}")
    a(f"\n{PREV_TITLE}\n{PREV_TEXT}\n{PREV_SEE}\n(Previously published research — not a result of this experiment.)")
    a("\nRESEARCH LINEAGE\n"+"\n".join(f"  {t}: {u}" for t,u in LINEAGE)+"\n  This experiment: unpublished — no DOI.")
    a("\nHISTORICAL REFERENCE (earlier runs, not this session): "+", ".join(f"{n} blob {LOCKS[n]}" for n in HISTORICAL))
    a("\nSCOPE  Answers are raw model output and not verified technical truth; checks are automatic. Questions contain the section heading (not blind QA). "
      "Cartridges are read one at a time; the synthesis is text-mediated.")
    a(f"{AUTHOR} · {ORG} · {LICENSE_NAME} · {COPYRIGHT}")
    RUN_SUMMARY.write_text("\n".join(L)+"\n",encoding="utf-8");return str(RUN_SUMMARY)
def session_record():
    return dict(session=SESSION_INFO,app=APP_TITLE,version_note=VERSION_NOTE,sources=SOURCES,locks=LOCKS,engine={k:v for k,v in ENGINE.items() if k!="source"},initialization=INIT,
                architecture=engine_architecture(),document=DOC,model=MODEL_IDENTITY,mounted=STATE["mount"],operations=STATE["ops"],qa=STATE["qa"],controls=STATE["controls"],
                weight_checks=STATE["weight_checks"],disk_checks=STATE["disk_checks"],verification=STATE["verification"],figures=FIG_FILES,lineage=LINEAGE,
                previously_demonstrated=dict(title=PREV_TITLE,text=PREV_TEXT,see=PREV_SEE),
                scope="Answers are raw model output; checks are automatic; one cartridge at a time; text-mediated synthesis; the Siemens PDF is not redistributed.")
def _category(rel):
    if rel.startswith("historical_reference_not_this_session"):return "HISTORICAL (published earlier run, not this session)"
    if rel.startswith("figures"):return "LIVE figure"
    if rel.startswith("live_engine"):return "LIVE engine output / record"
    return "LIVE session record"
def package_session():
    """Download-All ZIP: seven figures (JPG/PNG/PDF), live engine output + results, session logs, measurement and
    verification records, historical files (separate folder) and SHA256_MANIFEST.json — never the Siemens PDF"""
    sync_engine_records();dump_json(SESSION_DIR/"SESSION_RECORD.json",session_record());write_run_summary()
    # the Siemens PDF lives outside the session folder (PRIVATE_DIR) and is never packaged; the only PDFs here are figures
    files=sorted(p for p in SESSION_DIR.rglob("*") if p.is_file() and p.suffix not in (".zip",".tmp") and p!=MANIFEST)
    man=OrderedDict((str(p.relative_to(SESSION_DIR)),dict(sha256=sha_file(p),bytes=p.stat().st_size,category=_category(str(p.relative_to(SESSION_DIR))))) for p in files)
    dump_json(MANIFEST,dict(session=SESSION_ID,utc=utc_now(),note="The Siemens PDF is not included (copyright Siemens AG); its URL and SHA-256 are in SOURCE_DOCUMENT_RECORD.json.",files=man))
    tmp=ZIP_PATH.with_suffix(".zip.tmp")
    with zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED) as z:
        for p in files+[MANIFEST]:z.write(p,arcname=f"{SESSION_ID}/{p.relative_to(SESSION_DIR)}")
    with zipfile.ZipFile(tmp) as z:
        if z.testzip():raise RuntimeError("ZIP check failed")
    tmp.replace(ZIP_PATH);slog("PACKAGE",ZIP_PATH.name,files=len(files)+1,bytes=ZIP_PATH.stat().st_size);return str(ZIP_PATH)
def download_items():
    items=[("Run summary (.txt)",RUN_SUMMARY),("Live TEST718 engine output (.log)",LIVE_ENGINE_LOG),("Live engine output with UTC time stamps (.tsv)",LIVE_ENGINE_TS),
           ("Live TEST718 results (.json)",LIVE_ENGINE_JSON),("Live TEST716 set-up record (.json)",LIVE_SETUP_JSON),("Live measurements (.json)",SESSION_DIR/"LIVE_MEASUREMENTS.json"),("Ten-cartridge X-ray measurements (.json)",XRAY_FILE),
           ("Source document record (.json)",DOC_FILE),("Model identity record (.json)",MODEL_FILE),("Date comparison record (.json)",DATES_FILE),
           ("Verification record (.json)",VERIFY_FILE),("Initialization record (.json)",INIT_FILE),("Session log (.log)",SESSION_LOG),("Session events (.jsonl)",SESSION_EVENTS),
           ("Interface questions and answers (.jsonl)",SESSION_QA),("Figure manifest (.json)",SESSION_DIR/"FIGURES_MANIFEST.json"),("SHA-256 manifest (.json)",MANIFEST)]+\
          [(f"HISTORICAL · published {n} of an earlier run (not this session)",HIST_DIR/("HISTORICAL_"+n)) for n in HISTORICAL]
    return [(l,str(p)) for l,p in items if Path(p).is_file()]

# ---------------------------------------------------------------------------------------------------------------------
# AUTOMATIC INITIALIZATION — one start, every step real, stops at the first failure
# ---------------------------------------------------------------------------------------------------------------------
def _step_experiment():
    r=run_experiment();rec,dates=model_and_dates_records()
    _OUT.write(f"  model snapshot loaded: {rec.get('loaded_snapshot_commit')} · {dates['statement']}\n");_OUT.flush()
    return dict(r,loaded_snapshot=rec.get("loaded_snapshot_commit"))
def _step_verify():
    verify_disk();verify_weights();v=compute_verification()
    for it in v["items"]:_OUT.write(f"  {'PASS' if it['passed'] else 'FAIL'}  {it['name']:<40} {short(it['detail'] if isinstance(it['detail'],str) else json.dumps(it['detail'],ensure_ascii=False),90)}\n")
    _OUT.flush()
    if not v["ready"]:raise RuntimeError("LIVE VERIFICATION FAILED: "+", ".join(i["name"] for i in v["items"] if not i["passed"]))
    return dict(passed=v["passed"],total=v["total"])
def _step_ready():
    t=mount(cart_ids()[0]);return dict(cartridge=t["cartridge"],rows=t["cache_tokens"],seconds=round(t["end_to_end_ms"]/1000,2))
def _step_figures():
    out,errs=render_figures()
    if errs or len(out)!=len(FIG_FUNCS):raise RuntimeError(f"FIGURES: {len(out)}/{len(FIG_FUNCS)} generated · {errs}")
    dump_json(INIT_FILE,INIT);z=package_session()
    return dict(figures=[Path(r["jpg"]).name for r in out.values()],zip=Path(z).name)
STEP_FUNCS=OrderedDict([("SOURCES",sources_step),("PREFLIGHT",preflight),("DOCUMENT",document_step),("EXPERIMENT",_step_experiment),
                        ("XRAY",xray_all),("VERIFY",_step_verify),("READY_MEMORY",_step_ready),("FIGURES",_step_figures)])

def init_failed(key,ex):
    tb=traceback.format_exc()
    INIT["failed"]=dict(step=key,title=INIT_STEPS[key],error=f"{type(ex).__name__}: {ex}",last_successful_step=INIT["last_ok"],utc=utc_now(),traceback=tb[-6000:],
                        engine_status=(E.get("R718") or {}).get("status"),last_engine_lines=[f"{ts} {l}" for ts,_,l in ENGINE_LINES[-40:]],
                        last_heartbeat=(HEARTBEATS[-1] if HEARTBEATS else None),engine_started_utc=ENGINE.get("started_utc"))
    _release("initialization failed")
    slog("INIT_FAILED",key,error=INIT["failed"]["error"],last_successful_step=INIT["last_ok"],engine_status=INIT["failed"]["engine_status"],traceback=tb[-3000:])
    try:dump_json(INIT_FILE,INIT);package_session()
    except Exception as ex2:_OUT.write(f"  (failure package could not be written: {ex2})\n")
    banner(f"INITIALIZATION STOPPED — the demonstration is NOT ready and no interface is opened.\n"
           f"  failed step          : {key} · {INIT_STEPS[key]}\n  error                : {INIT['failed']['error']}\n"
           f"  last successful step : {INIT['last_ok'] or 'none'}\n  records              : {SESSION_DIR}\n  all files (ZIP)      : {ZIP_PATH if ZIP_PATH.is_file() else 'not written'}","█")

def run_initialization():
    banner(f"{APP_TITLE}\n{VERSION_NOTE} · session {SESSION_ID} · records in {SESSION_DIR}\n"
           "Automatic initialization: every step below is executed for real in this runtime; nothing is precomputed.","#")
    for key,fn in STEP_FUNCS.items():
        t0=step_begin(key)
        try:info=fn()
        except BaseException as ex:
            init_failed(key,ex);raise RuntimeError(f"INITIALIZATION FAILED at {key}: {type(ex).__name__}: {ex}") from ex
        step_done(key,t0,result=info)
    INIT["ready"]=True;INIT["ready_utc"]=utc_now();INIT["total_seconds"]=round(time.perf_counter()-INIT["started"],1)
    dump_json(INIT_FILE,INIT);package_session()
    banner(f"READY — all {len(STEP_FUNCS)} steps passed in {INIT['total_seconds']/60:.1f} min · live verification "
           f"{STATE['verification']['passed']}/{STATE['verification']['total']} · mounted {STATE['cartridge']} ({STATE['mount']['cache_tokens']:,} rows)","#")
    slog("READY","initialization complete",seconds=INIT["total_seconds"])
    return True
