# ===== PART 2/3 — paste directly after PART 1 in the same cell =====
# =====================================================================================================================
# PART 2 / 3 — six scientific figures from THIS RUN's outputs (JPEG 300 dpi, layout QC), records, SHA-256 manifest and the
#              single RUN pipeline. Every number and quote comes from this RUN's engine output; a missing output is shown
#              as missing. Quotes are cut with “…”, never reworded; full texts are in the interface and downloads.
# =====================================================================================================================
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.linewidth":.9,"axes.edgecolor":NEU,"axes.labelcolor":INK,"xtick.color":NEU,"ytick.color":NEU,
                     "xtick.labelsize":9.5,"ytick.labelsize":9.5,"axes.labelsize":10.5,"axes.titlesize":11.5,"axes.titleweight":"bold","axes.titlelocation":"left",
                     "legend.fontsize":9.5,"legend.frameon":False})
FW,FH=13.333,7.5;OUT_DPI=300;MONO="DejaVu Sans Mono"
FIGURES=OrderedDict([
    ("F1",dict(n=1,title="General Architecture",slug="GENERAL_ARCHITECTURE",tab="OVERVIEW")),
    ("F2",dict(n=2,title="Physical Memory Cartridge",slug="PHYSICAL_MEMORY_CARTRIDGE",tab="PHYSICAL CARTRIDGES")),
    ("F3",dict(n=3,title="Hierarchical Synthesis",slug="HIERARCHICAL_SYNTHESIS",tab="HIERARCHICAL SYNTHESIS")),
    ("F4",dict(n=4,title="Eight-Round Closed Loop",slug="EIGHT_ROUND_CLOSED_LOOP",tab="CLOSED LOOP")),
    ("F5",dict(n=5,title="Blind Investigation and Official Outcome",slug="BLIND_INVESTIGATION_AND_OFFICIAL_OUTCOME",tab="BLIND C11")),
    ("F6",dict(n=6,title="C11 to C12 Memory Consolidation",slug="C11_TO_C12_MEMORY_CONSOLIDATION",tab="C12 MASTER"))])
FIG_FILES={};FIG_ERRORS={};PROVENANCE={}
BADGE_COL={"SCHEMATIC":NEU,"LIVE MEASUREMENT":OK_COL,"SEALED MEMORY":COL["C11"],"OBSERVATIONAL":AMBER,"VERIFICATION RECORD":NEU,"NOT PRODUCED IN THIS RUN":RED}
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
    """centred text that must stay inside [x0,x1] (shrinks only as far as needed)"""
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
def vline(fig,x,y0,y1,col=RED,lw=1.6,ls="--"):fig.add_artist(Line2D([x,x],[y0,y1],transform=fig.transFigure,color=col,lw=lw,ls=ls,zorder=4))
def k_sha(s,n=12):return (str(s)[:n]+"…") if s else "—"
def fmt_b(b):
    if b is None:return "—"
    return f"{b/1e9:.2f} GB" if b>=1e9 else (f"{b/1e6:.1f} MB" if b>=1e6 else f"{b/1e3:.1f} kB")
def _date():return datetime.now().astimezone().strftime("%Y-%m-%d")
def fig_base(key,subtitle,badge):
    meta=FIGURES[key];fig=plt.figure(figsize=(FW,FH),dpi=100,facecolor=BG);bcol=BADGE_COL.get(badge,NEU)
    b=fig.text(.965,.952,badge,fontsize=10,weight="bold",color=bcol,va="center",ha="right",bbox=dict(boxstyle="square,pad=0.35",fc="white",ec=bcol,lw=1.2))
    bx0=_bb(fig,b).x0-.012
    T(fig,.035,.952,f"Figure {meta['n']} — {meta['title']}",size=18,weight="bold",xmax=bx0,minsize=12)
    T(fig,.035,.912,subtitle,size=11,color=INK2,xmax=.965,minsize=7.5)
    hline(fig,.035,.965,.888,INK2,.8)
    if SIM:fig.text(.5,.47,"SIMULATION — NOT EXPERIMENTAL DATA",fontsize=40,color=RED,alpha=.12,rotation=18,ha="center",va="center",weight="bold",gid="qc-ignore",zorder=100)
    return fig
def fig_footer(fig,key,note):
    meta=FIGURES[key];hline(fig,.035,.965,.072,RULE,.7)
    T(fig,.035,.050,note,size=8.8,color=INK2,xmax=.965,minsize=6.2)
    T(fig,.035,.022,f"{APP_NAME} · {EXPERIMENT} · demo {CODE_VERSION} · {_date()} · 745.py git blob {LOCKS['745.py'][:10]} · run {SESSION_ID}"+(" · SIMULATION" if SIM else "")+f" · Figure {meta['n']}/6",
      size=7.8,color=MUTED,xmax=.965,minsize=5.5,mono=True)
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
    stem=("SIMULATION_" if SIM else "")+f"TEST745_FIG{num}_{meta['slug']}{suffix}";jpg=FIG_DIR/(stem+".jpg")
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
    fig_footer(fig,key,"Placeholder by design: TEST745 figures are drawn only from outputs of this RUN (no earlier run, no representative values).")
    return save_fig(fig,key,"NOT PRODUCED IN THIS RUN",["(none — output missing)"],"_NOT_PRODUCED")

# ---------------------------------------------------------------------------------------------------------------------
# quotes from the real outputs (cut, never reworded) and observational text measures
# ---------------------------------------------------------------------------------------------------------------------
def unmd(s):return re.sub(r"\s+"," ",re.sub(r"\*\*|__|`|^#+\s*","",str(s))).strip(" -")
def prose(text):
    """the running text of a model answer without markdown headings (for an opening quote)"""
    out=[]
    for ln in str(text or "").split("\n"):
        s=ln.strip()
        if not s or re.match(r"^#{1,6}\s",s) or re.match(r"^\*\*[^*]{1,80}\*\*:?$",s):continue
        out.append(unmd(re.sub(r"^\s*(?:[-*•]|\d+\.)\s+","",s)))
    return " ".join(out)
def quote(text,n):
    p=prose(text)
    if len(p)<=n:return p
    cut=p[:n];k=max(cut.rfind(". "),cut.rfind("; "))
    return (cut[:k+1] if k>n*.55 else cut.rstrip())+" …"
def uncertainty_items(text):
    """number of list items under the heading OPEN_UNCERTAINTIES (None if the section is absent)"""
    lines=str(text or "").split("\n");idx=next((i for i,l in enumerate(lines) if "OPEN_UNCERTAINTIES" in l.upper().replace(" ","_")),None)
    if idx is None:return None
    n=0
    for l in lines[idx+1:]:
        s=l.strip()
        if re.match(r"^#{1,6}\s",s) and n:break
        if re.match(r"^(?:[-*•]|\d+\.)\s+\S",s):n+=1
    return n
def similarity(a,b):
    if not a or not b:return None
    return round(difflib.SequenceMatcher(None,a.split(),b.split(),autojunk=False).ratio(),3)
def line_time(rx):
    for u,_,l in LINES:
        if re.search(rx,l):return u
    return None
def check_detail(name):
    c=next((c for c in CHECKS if c["name"]==name),None)
    if not c:return None
    try:return ast.literal_eval(c["detail"])
    except Exception:return c["detail"]
def check_ok(name):
    cs=[c for c in CHECKS if c["name"]==name];return None if not cs else all(c["passed"] for c in cs)
def _ents():return run_manifest().get("cartridges") or {}
def _v(cid):return ((LIVE.get("verification") or {}).get("cartridges") or {}).get(cid) or {}

# ---------------------------------------------------------------------------------------------------------------------
# Figure 1 — General Architecture
# ---------------------------------------------------------------------------------------------------------------------
def _node(fig,x,y,w,h,cid,lines,col):
    box(fig,x,y,w,h,ec=col,lw=1.6);rect(fig,x,y+h-.028,w,.028,col,z=2)
    Tc(fig,x+.004,x+w-.004,y+h-.014,cid,size=9.5,weight="bold",color="white")
    for i,s in enumerate(lines):Tc(fig,x+.004,x+w-.004,y+h-.045-i*.024,s,size=7.6,color=INK2,mono=(i==len(lines)-1))
def fig1():
    k="F1";E_=_ents();R=run_results()
    if "C01" not in E_:return fig_missing(k,"The architecture is drawn from the cartridges this RUN sealed (manifest).","No cartridge was sealed in this RUN.")
    fig=fig_base(k,"The architecture TEST745 actually ran in this session — physical CUT3 cartridges (boxes) and text-mediated synthesis (dashed arrows) · values from this RUN","SCHEMATIC")
    def lines(c):
        e=E_.get(c);return [f"{e['body_tokens']:,} tokens",f"SHA {k_sha(e['sha256'],10)}"] if e else ["not produced","—"]
    pre=R.get("preliminary") or {}
    box(fig,.035,.43,.1,.30,ec=NEU,lw=1.3,fc=PANEL);Tc(fig,.037,.133,.705,"AIN preliminary",size=8.6,weight="bold");Tc(fig,.037,.133,.68,"report (PDF)",size=8.6,weight="bold")
    Tc(fig,.037,.133,.64,f"{pre.get('pages','—')} pages",size=7.8,color=INK2);Tc(fig,.037,.133,.615,f"SHA {k_sha(pre.get('pdf_sha256'),10)}",size=7.2,color=MUTED,mono=True)
    Tc(fig,.037,.133,.56,"split in document",size=7.4,color=INK2);Tc(fig,.037,.133,.54,"order into 3 parts",size=7.4,color=INK2);Tc(fig,.037,.133,.50,"(ONE report, not",size=7.4,color=AMBER);Tc(fig,.037,.133,.48,"3 independent ones)",size=7.4,color=AMBER)
    ys=[.66,.48,.30];W=.085;Hh=.11;X={"C":.16,"S":.285,"H":.41}
    for j,c in enumerate(SRC):_node(fig,X["C"],ys[j],W,Hh,c,lines(c),COL["C"]);arrow(fig,.136,.58,X["C"]-.002,ys[j]+Hh/2,col=NEU,lw=1.0,ms=9)
    for j,s in enumerate(SUB):
        _node(fig,X["S"],ys[j],W,Hh,s,lines(s),COL["S"])
        for p in GROUPS[s]:arrow(fig,X["C"]+W+.002,ys[SRC.index(p)]+Hh/2,X["S"]-.002,ys[j]+Hh/2,col=COL["S"],lw=1.0,ms=9,ls="--")
    for j,h in enumerate(CRS):
        _node(fig,X["H"],ys[j],W,Hh,h,lines(h),COL["H"])
        for p in HIER[h]:arrow(fig,X["S"]+W+.002,ys[SUB.index(p)]+Hh/2,X["H"]-.002,ys[j]+Hh/2,col=COL["H"],lw=1.0,ms=9,ls="--")
    box(fig,.535,.36,.105,.32,ec=COL["LOOP"],lw=1.4,ls="--",fc=PANEL)
    nr=len(R.get("blind_rounds") or [])
    Tc(fig,.537,.638,.655,"CLOSED LOOP",size=8.8,weight="bold");Tc(fig,.537,.638,.625,"initial hypothesis",size=7.6,color=INK2)
    Tc(fig,.537,.638,.60,f"+ {nr} review rounds",size=7.6,color=INK2);Tc(fig,.537,.638,.575,"(limit 8, text only;",size=7.2,color=MUTED);Tc(fig,.537,.638,.555,"no official outcome)",size=7.2,color=MUTED)
    for j in range(3):arrow(fig,X["H"]+W+.002,ys[j]+Hh/2,.533,.52,col=COL["H"],lw=1.0,ms=9,ls="--")
    _node(fig,.665,.41,.095,.22,"C11 BLIND",lines("C11")[:1]+["MASTER — sealed","before outcome"]+lines("C11")[1:],COL["C11"])
    arrow(fig,.642,.52,.663,.52,col=COL["C11"],lw=1.4)
    vline(fig,.785,.14,.80,col=RED);T(fig,.787,.80,"EMBARGO",size=8,weight="bold",color=RED);T(fig,.787,.78,"final report opened",size=7,color=RED);T(fig,.787,.765,"only after C11 seal",size=7,color=RED)
    off=R.get("official_outcome") or {}
    box(fig,.80,.60,.165,.13,ec=COL["OFF"],lw=1.3);Tc(fig,.802,.963,.705,"AIN final report (PDF)",size=8.4,weight="bold",color=COL["OFF"])
    Tc(fig,.802,.963,.675,f"{off.get('pages','—')} pages · downloaded after seal",size=7.4,color=INK2);Tc(fig,.802,.963,.645,f"SHA {k_sha(off.get('pdf_sha256'),10)}",size=7.2,color=MUTED,mono=True)
    box(fig,.80,.45,.165,.11,ec=AMBER,lw=1.2,ls="--");Tc(fig,.802,.963,.525,"model self-audit",size=8.4,weight="bold",color=AMBER);Tc(fig,.802,.963,.495,"(model claim — not expert",size=7.2,color=INK2);Tc(fig,.802,.963,.475,"grading)",size=7.2,color=INK2)
    _node(fig,.80,.25,.165,.16,"C12 POST-OUTCOME",[("human review PENDING"),lines("C12")[0],"parent: C11 SHA",lines("C12")[1]][:3]+[lines("C12")[1]],COL["C12"])
    arrow(fig,.762,.52,.798,.665,col=COL["C11"],lw=1.0,ms=9,cs="arc3,rad=-.1");arrow(fig,.8825,.598,.8825,.562,col=NEU,lw=1.0,ms=9);arrow(fig,.8825,.448,.8825,.412,col=NEU,lw=1.0,ms=9)
    box(fig,.035,.10,.74,.13,ec=NEU,lw=1.2,fc=PANEL)
    T(fig,.045,.205,"Frozen Qwen2.5-72B-Instruct (NF4, BF16) — weights never changed · locked TEST709 / TEST730 engine functions · CUT3",size=9.2,weight="bold",xmax=.77)
    T(fig,.045,.175,"every box: native CUT3 forge (H3 + K/V of layers 0–3) → torch.save on the SSD → SHA-256 of the file and of the tensors",size=8.2,color=INK2,xmax=.77)
    T(fig,.045,.15,"every dashed arrow: the cartridge is mounted (80 layers rebuilt) and READ by the model → the readouts are synthesized as TEXT → forged as a new cartridge",size=8.2,color=INK2,xmax=.77)
    T(fig,.045,.125,"no direct BF16 tensor fusion of cartridges takes place in TEST745",size=8.2,color=AMBER,weight="bold",xmax=.77)
    fig_footer(fig,k,"Token counts and SHA-256 values: TEST745_manifest.json of this RUN. C01–C03 are consecutive parts of one AIN preliminary report. C12 carries the C11 file SHA-256 as parent.")
    return save_fig(fig,k,"SCHEMATIC",["TEST745_manifest.json (this RUN)","TEST745_results.json (preliminary, official_outcome, blind_rounds)"])

# ---------------------------------------------------------------------------------------------------------------------
# Figure 2 — Physical Memory Cartridge
# ---------------------------------------------------------------------------------------------------------------------
def fig2():
    k="F2";V=(LIVE.get("verification") or {}).get("cartridges") or {}
    if not any(v.get("present") for v in V.values()):return fig_missing(k,"Shapes, sizes and seals are measured from the cartridge files of this RUN (stage 13).","No cartridge file of this RUN was verified.")
    fig=fig_base(k,"What one cartridge physically holds, how it is stored and how it is mounted again — sizes measured from this RUN's files","LIVE MEASUREMENT")
    steps=[("1  FORGE","forward pass L0–L79 · H3 captured at\nthe layer-3 boundary (direct forward)"),("2  PERSIST","torch.save → SSD · SHA-256 of the\nfile and of every tensor"),
           ("3  RELOAD","file SHA · tensor seals · cartridge ID\nchecked before every use"),("4  INJECT + REBUILD","H3 injected at layer 3 · layers 4–79\nrecomputed by the frozen model"),
           ("5  READ","the question is appended to the\n80-layer K/V memory · greedy decoding")]
    for i,(h,t) in enumerate(steps):
        x=.035+i*.188;box(fig,x,.735,.172,.13,ec=NEU,fc=PANEL,lw=1.2)
        T(fig,x+.01,.84,h,size=10,weight="bold",xmax=x+.168);T(fig,x+.01,.78,t,size=8,color=INK2,linespacing=1.25,xmax=x+.168)
        if i<4:arrow(fig,x+.173,.80,x+.187,.80,col=NEU,lw=1.3,ms=10)
    x0,x1=.06,.94;w=(x1-x0)/80
    for L in range(80):rect(fig,x0+L*w+.0008,.645,w-.0016,.04,OK_COL if L<=3 else "#E5E7EB",z=2)
    fig.add_artist(Line2D([x0+4*w,x0+4*w],[.635,.695],transform=fig.transFigure,color=COL["C11"],lw=2.2,zorder=4))
    T(fig,x0+4*w+.004,.708,"CUT3 boundary — H3 is injected here at mount time",size=8.4,weight="bold",color=COL["C11"])
    T(fig,x0,.62,"stored: H3 + K/V of layers 0–3",size=8.4,weight="bold",color=OK_COL)
    T(fig,x0+.25,.62,"layers 4–79: NOT stored — recomputed by the frozen model each time the cartridge is mounted",size=8.2,color=INK2,xmax=.96)
    cards=[("Not text RAG","stored are internal model states (H3, K/V L0–3), not text pasted into the prompt"),
           ("Not fine-tuning","the weights stay frozen — sentinel unchanged: "+("PASS" if check_ok("FROZEN_SENTINEL_UNCHANGED") else "—")),
           ("Not a full transformer bypass","layers 4–79 and decoding still run; early layers are reused from the stored states")]
    for i,(h,t) in enumerate(cards):
        x=.035+i*.315;box(fig,x,.515,.30,.075,ec=AMBER if i==2 else NEU,lw=1.1)
        T(fig,x+.008,.572,h,size=8.8,weight="bold",xmax=x+.296);T(fig,x+.008,.538,t,size=7.4,color=INK2,xmax=x+.296)
    hd=["cartridge","rows n","H3 tensor","H3 + L0–L3 bytes","file on SSD","full 80-layer K/V","reloads","file · tensor · body","SHA-256 (file)"]
    xs=[.035,.11,.17,.32,.42,.505,.60,.66,.80];y=.475
    for x,h in zip(xs,hd):T(fig,x,y,h,size=7.6,weight="bold",color=MUTED)
    hline(fig,.035,.965,y-.013,RULE)
    for j,c in enumerate(CARTS):
        v=V.get(c) or {};yy=y-.035-j*.0325;T(fig,.035,yy,c,size=8.4,weight="bold",color=ccol(c))
        if not v.get("present"):T(fig,.11,yy,"not produced in this RUN",size=7.8,color=RED);continue
        reloads=sum(1 for ch in CHECKS if ch["name"]==f"FILE_SHA_{c}" and ch["passed"])
        ok=lambda b:"✓" if b else ("✗" if b is False else "–")
        vals=[f"{v['n']:,}",f"{tuple(v['h_shape'])}",fmt_b(v["h_bytes"]+v["lower_bytes"]),fmt_b(v["bytes"]),fmt_b(v["full_80_layer_kv_bytes"]),str(reloads),
              f"{ok(v.get('file_sha_ok'))} · {ok(v.get('tensor_seal_ok'))} · {ok(v.get('body_sha_ok'))}",k_sha(v["sha256_now"],16)]
        for x,val,nx in zip(xs[1:],vals,xs[2:]+[.965]):T(fig,x,yy,val,size=7.6,mono=True,xmax=nx-.005)
    fig_footer(fig,k,"Measured now from the files (torch.load on the CPU, read-only). Full 80-layer K/V = n × 80 × 8 heads × 128 × 2 (K,V) × 2 bytes. Reloads = PASS FILE_SHA lines of this RUN's engine output.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["physical_cartridges/*.pt of this RUN (read-only)","POST_RUN_VERIFICATION.json","ENGINE_OUTPUT_REALTIME.log (FILE_SHA checks)"])

# ---------------------------------------------------------------------------------------------------------------------
# Figure 3 — Hierarchical Synthesis
# ---------------------------------------------------------------------------------------------------------------------
def fig3():
    k="F3";E_=_ents();gi=generation_index()
    if not all(c in E_ for c in SRC+SUB+CRS):return fig_missing(k,"The hierarchy C01–C03 → S01–S03 → H01–H03 → C11 is drawn from this RUN's sealed cartridges and readouts.","Not every cartridge of the hierarchy was sealed in this RUN.")
    fig=fig_base(k,"Physical storage (solid boxes) and text-mediated synthesis (dashed arrows) are separate steps · token counts measured in this RUN","SCHEMATIC")
    def rd(cid,role_part=None):
        xs=[g for g in gi if g["cid"]==cid and g["kind"]=="readout" and (role_part is None or role_part in g.get("role",""))];return sum((g.get("tokens") or 0) for g in xs),len(xs)
    cols=[(.06,SRC,COL["C"],"SOURCE CARTRIDGES"),(.31,SUB,COL["S"],"SUBSYSTEM SYNTHESES"),(.56,CRS,COL["H"],"CROSS-SYSTEM SYNTHESES")]
    ys=[.66,.47,.28];W=.19;Hh=.14
    for x,ids,col,lab in cols:
        T(fig,x,.855,lab,size=9.5,weight="bold",color=MUTED)
        for j,c in enumerate(ids):
            e=E_[c];box(fig,x,ys[j],W,Hh,ec=col,lw=1.6);rect(fig,x,ys[j]+Hh-.03,W,.03,col,z=2)
            T(fig,x+.008,ys[j]+Hh-.015,f"{c} · physical cartridge",size=9,weight="bold",color="white",xmax=x+W-.005)
            T(fig,x+.008,ys[j]+.075,f"body {e['body_tokens']:,} tokens · forged {e.get('forge_seconds','—')} s",size=7.8,color=INK2,xmax=x+W-.005)
            if c in SRC:t,n=rd(c);T(fig,x+.008,ys[j]+.05,f"read alone: {t:,} tokens written by the model",size=7.6,color=INK2,xmax=x+W-.005)
            else:
                d=check_detail("SYNTHESIS_CONTEXT_FITS_"+c);t,n=rd(c)
                T(fig,x+.008,ys[j]+.05,f"synthesis prompt {d.get('tokens','—') if isinstance(d,dict) else '—'} tokens (TEXT)",size=7.6,color=INK2,xmax=x+W-.005)
                T(fig,x+.008,ys[j]+.03,f"read back {n}× · {t:,} tokens in total",size=7.6,color=INK2,xmax=x+W-.005) if n else None
            T(fig,x+.008,ys[j]+.01,f"SHA {k_sha(e['sha256'],22)}",size=7.0,color=MUTED,mono=True,xmax=x+W-.005)
    for j,s in enumerate(SUB):
        for p in GROUPS[s]:arrow(fig,.06+W+.002,ys[SRC.index(p)]+Hh/2,.31-.002,ys[j]+Hh/2,col=COL["S"],lw=1.1,ms=9,ls="--")
    for j,h in enumerate(CRS):
        for p in HIER[h]:arrow(fig,.31+W+.002,ys[SUB.index(p)]+Hh/2,.56-.002,ys[j]+Hh/2,col=COL["H"],lw=1.1,ms=9,ls="--")
    box(fig,.80,.42,.165,.30,ec=COL["C11"],lw=1.6,ls="--",fc=PANEL);T(fig,.81,.695,"→ INITIAL hypothesis",size=9,weight="bold",color=COL["C11"],xmax=.96)
    d=check_detail("SYNTHESIS_CONTEXT_FITS_INITIAL");ini=next((g for g in gi if g["cid"]=="INITIAL"),{})
    T(fig,.81,.665,f"from H01–H03 readouts",size=7.8,color=INK2,xmax=.96);T(fig,.81,.64,f"prompt {d.get('tokens','—') if isinstance(d,dict) else '—'} tokens",size=7.8,color=INK2,xmax=.96)
    T(fig,.81,.615,f"answer {ini.get('tokens','—')} tokens",size=7.8,color=INK2,xmax=.96);T(fig,.81,.575,"→ 8 closed-loop rounds",size=8.6,weight="bold",color=COL["C11"],xmax=.96)
    T(fig,.81,.545,"→ C11 BLIND MASTER",size=8.6,weight="bold",color=COL["C11"],xmax=.96);T(fig,.81,.515,f"C11 SHA {k_sha((E_.get('C11') or {}).get('sha256'),10)}",size=7.2,color=MUTED,mono=True,xmax=.96)
    T(fig,.81,.48,"(Figures 4 and 5)",size=7.6,color=MUTED,xmax=.96)
    for j in range(3):arrow(fig,.56+W+.002,ys[j]+Hh/2,.798,.57,col=COL["H"],lw=1.0,ms=9,ls="--")
    box(fig,.035,.10,.93,.12,ec=NEU,lw=1.1,fc=PANEL)
    T(fig,.045,.195,"solid box = physical CUT3 cartridge on the SSD (forge_native → torch.save → SHA-256) — the memory itself",size=8.4,color=INK,xmax=.96)
    T(fig,.045,.165,"dashed arrow = the parent cartridge is mounted alone (80 layers) and read by the model; the readouts become a TEXT prompt; the synthesis TEXT is forged as the child",size=8.4,color=INK,xmax=.96)
    T(fig,.045,.135,"S01–S03 synthesize the source reflections; H01–H03 read the S cartridges physically again (not the original documents) — no tensor of two cartridges is ever fused",size=8.4,color=AMBER,xmax=.96)
    fig_footer(fig,k,"Token counts: manifest (body), engine output (SYNTHESIS_CONTEXT_FITS, GENERATION) and TEST745_results.json generations of this RUN. Full texts: HIERARCHICAL SYNTHESIS tab.")
    return save_fig(fig,k,"SCHEMATIC",["TEST745_manifest.json","TEST745_results.json generations","ENGINE_OUTPUT_REALTIME.log"])

# ---------------------------------------------------------------------------------------------------------------------
# Figure 4 — Eight-Round Closed Loop
# ---------------------------------------------------------------------------------------------------------------------
def loop_measures():
    R=run_results();rt=round_texts();rounds=R.get("blind_rounds") or [];gi=generation_index()
    ini=next((g for g in gi if g["cid"]=="INITIAL"),{})
    toks=[ini.get("tokens")]+[next((r["tokens"] for r in rounds if r["round"]==i),None) for i in range(1,9)]
    sims=[None]+[similarity(rt[i-1][1],rt[i][1]) for i in range(1,9)]
    unc=[uncertainty_items(t) for _,t in rt]
    times=[line_time(r"^PASS SYNTHESIS_NOT_TRUNCATED_INITIAL")]+[line_time(rf"^PASS LOOP_NONEMPTY_{i}\b") for i in range(1,9)]
    def dt(a,b):
        try:return round((datetime.fromisoformat(b)-datetime.fromisoformat(a)).total_seconds(),1)
        except Exception:return None
    secs=[None]+[dt(times[i-1],times[i]) if times[i-1] and times[i] else None for i in range(1,9)]
    return dict(labels=[l for l,_ in rt],texts=[t for _,t in rt],tokens=toks,similarity_to_previous=sims,open_uncertainty_items=unc,seconds=secs,
                note="observational text measures of this RUN — no quality or accuracy score")
def fig4():
    k="F4";M=loop_measures()
    if not M["texts"][0] or not any(M["texts"][1:]):return fig_missing(k,"The closed loop is drawn from the initial hypothesis and the round texts written in this RUN.","No closed-loop round text exists in this RUN.")
    LIVE["loop"]={kk:v for kk,v in M.items() if kk!="texts"};dump_json(DATA_DIR/"CLOSED_LOOP_MEASURES.json",LIVE["loop"])
    fig=fig_base(k,"Initial blind hypothesis and eight review rounds written in this RUN · observational measures of the real texts — not a quality score; improvement is not assumed","OBSERVATIONAL")
    lab=M["labels"];x=np.arange(len(lab))
    ax=fig.add_axes([.06,.53,.25,.29]);tk=[v or 0 for v in M["tokens"]];ax.bar(x,tk,color=[COL["C11"]]+[NEU]*8,width=.65)
    ax.set_xticks(x);ax.set_xticklabels(lab,fontsize=7.6);ax.set_title("length of each analysis (tokens)",fontsize=9.5);ax.set_ylim(0,max(tk+[1])*1.18)
    ax2=fig.add_axes([.38,.53,.25,.29]);sv=[v if v is not None else 0 for v in M["similarity_to_previous"]];ax2.bar(x[1:],sv[1:],color=AMBER,width=.65)
    ax2.set_xticks(x);ax2.set_xticklabels(lab,fontsize=7.6);ax2.set_ylim(0,1.08);ax2.set_title("word-sequence similarity to the previous text",fontsize=9.5)
    for xi,v in zip(x[1:],M["similarity_to_previous"][1:]):
        if v is not None:ax2.text(xi,v+.02,f"{v:.2f}",ha="center",fontsize=6.8)
    ax3=fig.add_axes([.70,.53,.26,.29]);uv=[v if v is not None else 0 for v in M["open_uncertainty_items"]]
    ax3.bar(x,uv,color=[RULE if v is None else "#64748B" for v in M["open_uncertainty_items"]],width=.65);ax3.set_xticks(x);ax3.set_xticklabels(lab,fontsize=7.6)
    ax3.set_title("items listed under OPEN_UNCERTAINTIES",fontsize=9.5);ax3.set_ylim(0,max(uv+[1])*1.25)
    for xi,v in zip(x,M["open_uncertainty_items"]):ax3.text(xi,(v or 0)+.05,"—" if v is None else str(v),ha="center",fontsize=6.8)
    for a in (ax,ax2,ax3):
        for s in ("top","right"):a.spines[s].set_visible(False)
        a.tick_params(labelsize=7.6)
    sec=[s for s in M["seconds"] if s];T(fig,.06,.465,("round duration (engine output receipt times): "+" · ".join(f"{l} {s:.0f} s" for l,s in zip(lab[1:],M["seconds"][1:]) if s)) if sec else "round durations: not available",size=7.6,color=MUTED,xmax=.96)
    last=next((i for i in range(8,0,-1) if M["texts"][i]),0)
    for j,(i,head,col) in enumerate(((0,"INITIAL blind hypothesis — opening (quoted, shortened)",COL["C11"]),(last,f"{lab[last]} — final round written to C11 — opening (quoted, shortened)",NEU))):
        xx=.035+j*.47;box(fig,xx,.10,.455,.33,ec=col,lw=1.4)
        T(fig,xx+.01,.41,head,size=8.8,weight="bold",color=col,xmax=xx+.45)
        T(fig,xx+.01,.385,"“"+wrap(quote(M["texts"][i],1000),84,14)+"”",size=7.8,color=INK,va="top",linespacing=1.18,xmax=xx+.45)
    fig_footer(fig,k,"Similarity = difflib ratio of the word sequences (how much text was kept, not whether it became more correct). Uncertainty items: list lines under the OPEN_UNCERTAINTIES heading; “—” = heading absent.")
    return save_fig(fig,k,"OBSERVATIONAL",["generated_text/INITIAL_synthesis.txt","generated_text/blind_round_01–08.txt","TEST745_results.json blind_rounds","CLOSED_LOOP_MEASURES.json"])

# ---------------------------------------------------------------------------------------------------------------------
# Figure 5 — Blind Investigation and Official Outcome
# ---------------------------------------------------------------------------------------------------------------------
def fig5():
    k="F5";R=run_results();ba=R.get("blind_answers") or []
    if not ba:return fig_missing(k,"The blind phase is drawn from the three answers C11 gave in this RUN before the official report was opened.","C11 did not answer in this RUN.")
    fig=fig_base(k,"C11 is sealed and answers three questions BEFORE the AIN final report is downloaded · chronological access boundary measured from this RUN's engine output","SEALED MEMORY")
    ev=[("C11 sealed",line_time(r"^PHYSICAL_SEALED C11 "),COL["C11"])]
    gts=[u for u,_,l in LINES if l.startswith("GENERATION C11 ")]
    ev+=[(f"blind answer Q{i+1}",u,COL["C11"]) for i,u in enumerate(gts[:3])]
    ev+=[("C11 locked before final",line_time(r"^PASS C11_LOCKED_BEFORE_FINAL"),COL["C11"]),("OUTCOME UNLOCKED",line_time(r"^OFFICIAL_OUTCOME_UNLOCK"),RED),
         ("final report downloaded",line_time(r"final_report\.pdf"),RED),("self-audit written",line_time(r"^PASS AUDIT_NOT_TRUNCATED"),AMBER),("C12 sealed",line_time(r"^PHYSICAL_SEALED C12 "),COL["C12"])]
    ev=[(a,datetime.fromisoformat(b),c) for a,b,c in ev if b]
    if ev:
        x0,x1=.07,.93;hline(fig,x0-.02,x1+.02,.72,NEU,1.4);n=len(ev);step=(x1-x0)/max(n-1,1)
        for i,(a,t,c) in enumerate(ev):
            xx=x0+i*step;fig.add_artist(Line2D([xx],[.72],transform=fig.transFigure,marker="o",ms=6,color=c))
            Tc(fig,xx-step/2+.003,xx+step/2-.003,.765,a,size=7.6,color=c,weight="bold" if a=="OUTCOME UNLOCKED" else "normal")
            Tc(fig,xx-step/2+.003,xx+step/2-.003,.675,t.strftime("%H:%M:%S"),size=7.2,color=MUTED,mono=True)
            if a=="OUTCOME UNLOCKED":vline(fig,xx-step/2,.62,.82)
        span=(ev[-1][1]-ev[0][1]).total_seconds()
        T(fig,.06,.855,f"events in order of occurrence (evenly spaced) · times = UTC receipt of the engine output line in this RUN · span {span/60:.1f} min · red line = access boundary",size=7.8,color=MUTED,xmax=.96)
    box(fig,.035,.10,.455,.48,ec=COL["C11"],lw=1.4);T(fig,.045,.56,"BLIND — answers of C11 alone, before the official report (quoted, shortened)",size=8.6,weight="bold",color=COL["C11"],xmax=.485)
    for i,a in enumerate(ba[:3]):
        y=.525-i*.145;T(fig,.045,y,f"Q{i+1} · "+short(a["question"],92),size=7.4,weight="bold",color=INK,xmax=.485)
        T(fig,.045,y-.018,"“"+wrap(quote(a["answer"],330),86,5)+"”",size=7.0,color=INK2,va="top",linespacing=1.12,xmax=.485)
    ex=raw_of("AIN_FINAL_EVALUATION_EXCERPT.txt") or "";fx=ex.split("[OFFICIAL FINDINGS EXCERPT]",1)[-1] if ex else ""
    box(fig,.51,.33,.455,.25,ec=COL["OFF"],lw=1.4);T(fig,.52,.56,"OFFICIAL — AIN final report, findings excerpt given to the model after the seal",size=8.4,weight="bold",color=COL["OFF"],xmax=.96)
    T(fig,.52,.535,("“"+wrap(" ".join(fx.split())[:600]+" …",92,8)+"”") if fx else "excerpt file not available in this RUN",size=7.0,color=INK2,va="top",linespacing=1.12,xmax=.96)
    sa=(R.get("self_audit") or {}).get("text")
    box(fig,.51,.10,.455,.21,ec=AMBER,lw=1.4,ls="--");T(fig,.52,.29,"MODEL SELF-AUDIT — the model's own claim, NOT independent expert grading",size=8.4,weight="bold",color=AMBER,xmax=.96)
    T(fig,.52,.265,("“"+wrap(quote(sa,440),92,6)+"”") if sa else "self-audit not produced in this RUN",size=7.0,color=INK2,va="top",linespacing=1.12,xmax=.96)
    fig_footer(fig,k,"Questions: blind_questions of 745.py (fixed before the run). Official text: AIN_FINAL_EVALUATION_EXCERPT.txt as built by 745.py. Correctness of the blind answers is not graded here.")
    return save_fig(fig,k,"SEALED MEMORY",["TEST745_results.json blind_answers, self_audit","sealed_sources/AIN_FINAL_EVALUATION_EXCERPT.txt","ENGINE_OUTPUT_REALTIME.log (receipt times)"])

# ---------------------------------------------------------------------------------------------------------------------
# Figure 6 — C11 to C12 Memory Consolidation
# ---------------------------------------------------------------------------------------------------------------------
def fig6():
    k="F6";E_=_ents();R=run_results();V=LIVE.get("verification") or {};lin=V.get("lineage") or {}
    if "C12" not in E_:return fig_missing(k,"The consolidation is drawn from the C11 and C12 cartridges sealed in this RUN.","C12 was not sealed in this RUN.")
    fig=fig_base(k,"C12 is a NEW physical cartridge: C11 stays unchanged and is referenced by its SHA-256 · the model self-audit is not expert grading · human review PENDING","SEALED MEMORY")
    c11=E_["C11"];c12=E_["C12"];off=R.get("official_outcome") or {};sa=R.get("self_audit") or {};seal=R.get("C11_seal") or {}
    _node(fig,.035,.53,.19,.29,"C11 BLIND MASTER",[f"{c11['body_tokens']:,} tokens","sealed "+str(seal.get("sealed_at",""))[11:19]+" UTC",f"role {c11.get('role')}",f"{c11['sha256'][:22]}"],COL["C11"])
    _node(fig,.035,.18,.19,.25,"AIN FINAL REPORT",[f"{off.get('pages','—')} pages (PDF)","opened after the C11 seal",f"{str(off.get('pdf_sha256'))[:22]}"],COL["OFF"])
    sat=len(str(sa.get("text","")))
    _node(fig,.30,.36,.19,.29,"MODEL SELF-AUDIT",["model compares its sealed","predictions with the findings",f"{sat:,} characters","(model claim — not grading)",f"{str(sa.get('sha256'))[:22]}"],AMBER)
    _node(fig,.30,.10,.19,.20,"HUMAN REVIEW",["status: NOT PROVIDED","(pending — none fabricated)"," "],NEU)
    _node(fig,.57,.36,.19,.40,"C12 POST-OUTCOME",[f"{c12['body_tokens']:,} tokens","role HUMAN_AI_MASTER_","HUMAN_REVIEW_PENDING","parent = C11 file SHA-256:",f"{(c12.get('parents') or [{}])[0].get('sha256','')[:22]}","C12 file SHA-256:",f"{c12['sha256'][:22]}"],COL["C12"])
    arrow(fig,.227,.675,.298,.55,col=COL["C11"]);arrow(fig,.227,.30,.298,.45,col=COL["OFF"]);arrow(fig,.492,.505,.568,.56,col=AMBER);arrow(fig,.492,.20,.568,.42,col=NEU,ls="--")
    arrow(fig,.227,.78,.568,.72,col=COL["C11"],ls=":",cs="arc3,rad=-.15")
    T(fig,.30,.845,"parent SHA-256 reference — C11 itself is not modified",size=7.8,color=COL["C11"],xmax=.76)
    rows=[("C11 locked before final report (engine)",check_ok("C11_LOCKED_BEFORE_FINAL")),("C11 immutable after C12 (engine)",check_ok("C11_IMMUTABLE")),
          ("C12 parent = C11 SHA-256 (engine)",check_ok("C12_PARENT_SHA")),("frozen weights unchanged (engine)",check_ok("FROZEN_SENTINEL_UNCHANGED")),
          ("C11 file re-hashed now = manifest (demo)",_v("C11").get("file_sha_ok")),("C12 body re-derived = manifest body hash (demo)",_v("C12").get("body_sha_ok")),
          ("C12 parent link re-checked (demo)",lin.get("c12_parent_is_c11")),("blind answers hash = C11 seal (demo)",lin.get("blind_answers_hash_ok"))]
    box(fig,.785,.10,.18,.72,ec=OK_COL,lw=1.3);T(fig,.795,.80,"integrity of the lineage",size=9,weight="bold",color=OK_COL,xmax=.96)
    for i,(l,v) in enumerate(rows):
        y=.755-i*.08;T(fig,.795,y,"PASS" if v else ("FAIL" if v is False else "—"),size=9.5,weight="bold",color=OK_COL if v else (RED if v is False else MUTED))
        T(fig,.795,y-.028,wrap(l,30,2),size=7.0,color=INK2,va="center",linespacing=1.1,xmax=.96)
    fig_footer(fig,k,"engine = PASS lines of this RUN's 745.py output · demo = independent read-only re-verification after the run (POST_RUN_VERIFICATION.json). C12 body = the exact 745.py expression, re-derived.")
    return save_fig(fig,k,"SEALED MEMORY",["TEST745_manifest.json","TEST745_results.json","C11_BLIND_SEAL.json","POST_RUN_VERIFICATION.json","ENGINE_OUTPUT_REALTIME.log"])

FIG_FUNCS=OrderedDict([("F1",fig1),("F2",fig2),("F3",fig3),("F4",fig4),("F5",fig5),("F6",fig6)])
def render_figures():
    errs={}
    for key,fn in FIG_FUNCS.items():
        t=time.perf_counter()
        try:
            rec=fn();FIG_FILES[key]=rec;STATE["fig_version"]+=1;bump()
            _emit(f"  figure {FIGURES[key]['n']} · {rec['badge']} · {rec['pixels'][0]}×{rec['pixels'][1]} · layout QC {'pass' if rec['layout_qc']['passed'] else 'FAIL'} · {time.perf_counter()-t:.1f} s")
        except Exception as ex:
            errs[key]=f"{type(ex).__name__}: {ex}";FIG_FILES.pop(key,None);flog_fig(f"{key} NOT GENERATED {traceback.format_exc()[-1500:]}");_emit(f"  figure {key} NOT GENERATED · {errs[key]}");plt.close("all")
    FIG_ERRORS.clear();FIG_ERRORS.update(errs)
    dump_json(SESSION_DIR/"FIGURES_MANIFEST.json",dict(session=SESSION_ID,utc=utc_now(),simulation=SIM,figures=FIG_FILES,not_generated=errs))
    return errs
def stage_figures():
    errs=render_figures();n=len(FIG_FILES)
    qcf=[k for k,v in FIG_FILES.items() if not (v.get("layout_qc") or {}).get("passed") or not (v.get("jpeg_qc") or {}).get("passed")]
    np_=[k for k,v in FIG_FILES.items() if v["badge"]=="NOT PRODUCED IN THIS RUN"]
    note=f"{n}/{len(FIGURES)} JPEG figures written (300 dpi)"
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
CLAIMS=[("Physical cartridge mechanism worked","technical",lambda:all(_v(c).get("file_sha_ok") and _v(c).get("tensor_seal_ok") for c in CARTS) if LIVE.get("verification") else None),
        ("Hierarchical synthesis completed","technical",lambda:all(c in _ents() for c in SUB+CRS) or None),
        ("Closed-loop rounds executed","technical",lambda:(len(run_results().get("blind_rounds") or [])==8) or None),
        ("Blind C11 sealed before the official report","technical",lambda:check_ok("C11_LOCKED_BEFORE_FINAL")),
        ("C12 created after the official report (parent C11)","technical",lambda:check_ok("C12_PARENT_SHA")),
        ("Causal correctness of the blind analysis","needs independent evaluation",lambda:None),
        ("The model's ability to recognize its own errors","needs independent evaluation",lambda:None)]
def write_run_summary():
    L=[];a=L.append;R=run_results()
    a(f"{APP_NAME} — {APP_SUB}\n{EXPERIMENT} live demonstration · demo {CODE_VERSION} · RUN {SESSION_ID} · written {local_now()}")
    if SIM:a("SIMULATION — NOTHING IN THIS FILE IS AN EXPERIMENTAL RESULT")
    a(f"RUN VERDICT {run_verdict()}\nengine: 745.py git blob {LOCKS['745.py']} executed unchanged · exit code {STATE.get('engine_rc')} · experiment directory {STATE.get('exp_dir')}")
    a("\nSTAGES (times = this RUN)")
    for key,title in STAGES.items():
        s=STATE["stages"][key];a(f"  [{s['status'].upper():<4}] {key:<10} {('%.0f s'%s['seconds']) if s['seconds'] is not None else '':>8}  {title}\n             {s['note']}")
    a("\nCARTRIDGES OF THIS RUN (manifest · demo re-verification)")
    for c in CARTS:
        e=_ents().get(c);v=_v(c)
        a(f"  {c:<4} "+(f"{e['role']:<36} {e['body_tokens']:>5} tok · file {e['sha256']} · parents {[p['id'] for p in e.get('parents',[])]} · file/tensor/body ok {v.get('file_sha_ok')}/{v.get('tensor_seal_ok')}/{v.get('body_sha_ok')} · equal to earlier RECORD {v.get('equal_to_record')}" if e else "not produced"))
    a("\nWHAT THIS RUN SHOWS — AND WHAT NEEDS INDEPENDENT EVALUATION")
    for t,kind,f in CLAIMS:
        try:v=f()
        except Exception:v=None
        a(f"  {'PASS' if v else ('FAIL' if v is False else '—'):<5} {t}  [{kind}]")
    for i,x in enumerate(R.get("blind_answers") or []):a(f"\nBLIND ANSWER Q{i+1} (C11, before the official report)\n  {x['question']}\n  "+x["answer"].replace("\n","\n  "))
    sa=(R.get("self_audit") or {}).get("text")
    if sa:a("\nMODEL SELF-AUDIT AFTER THE OFFICIAL REPORT (model claim, not expert grading)\n  "+sa.replace("\n","\n  "))
    a("\nHUMAN REVIEW: NOT PROVIDED (pending). No independent grading was performed by TEST745 or by this demo.")
    a(f"\n{AUTHOR} · {ORG} · {LICENSE_NAME} · {COPYRIGHT}")
    RUN_SUMMARY.write_text("\n".join(L)+"\n",encoding="utf-8")
def engine_files():
    d=exp_dir()
    if not d or not d.is_dir():return []
    out=[d/n for n in ("TEST745.log","TEST745_results.json","TEST745_manifest.json","C11_BLIND_SEAL.json") if (d/n).is_file()]
    out+=sorted((d/"generated_text").glob("*.txt")) if (d/"generated_text").is_dir() else []
    out+=sorted(p for p in (d/"sealed_sources").glob("*.txt")) if (d/"sealed_sources").is_dir() else []
    return out
def download_items():
    items=[("Run summary",RUN_SUMMARY),("Engine output, real-time (UTC receipt · stage · stream · line)",ENGINE_OUT),("Session log",SESSION_LOG),("Session events (JSONL)",SESSION_EVENTS),
           ("Post-run verification",VERIFY_FILE),("Closed-loop measures",DATA_DIR/"CLOSED_LOOP_MEASURES.json"),("Stage record",DATA_DIR/"STAGES.json"),("Engine checks of this RUN",DATA_DIR/"ENGINE_CHECKS.json"),
           ("Figure manifest",SESSION_DIR/"FIGURES_MANIFEST.json"),("SHA-256 manifest",MANIFEST),("745.py (locked, executed)",PROGRAM),("745.log — earlier run (RECORD)",EVID_DIR/"745.log")]
    out=[(l,str(p)) for l,p in items if Path(p).is_file()]
    out+=[(f"engine output file · {p.parent.name}/{p.name}",str(p)) for p in engine_files()]
    return out
def package_session():
    dump_json(DATA_DIR/"ENGINE_CHECKS.json",CHECKS);dump_json(DATA_DIR/"STAGES.json",dict(verdict=run_verdict(),stages=STATE["stages"],session=SESSION_ID,engine_rc=STATE.get("engine_rc")))
    write_run_summary()
    files=[p for p in sorted(SESSION_DIR.rglob("*")) if p.is_file() and p!=MANIFEST and p.suffix!=".tmp"]
    man=OrderedDict((str(p.relative_to(SESSION_DIR)),dict(sha256=sha_file(p),bytes=p.stat().st_size)) for p in files)
    dump_json(MANIFEST,dict(session=SESSION_ID,utc=utc_now(),simulation=SIM,note="SHA-256 of every file of this RUN, including the experiment directory, cartridges (.pt) and PDFs (not offered for download). No ZIP.",files=man))
    return str(MANIFEST)
def stage_records():
    package_session();return f"{len(FIG_FILES)} JPEG figures + {len(download_items())} records/texts, each downloadable directly · SHA-256 manifest of {len(json.load(open(MANIFEST))['files'])} files (no ZIP)"

# ---------------------------------------------------------------------------------------------------------------------
# THE RUN PIPELINE (one button)
# ---------------------------------------------------------------------------------------------------------------------
RUNS_DONE=[]
def _text_watcher(stop):
    seen=set()
    while not stop.wait(10):
        d=EXP_ROOT/"generated_text"
        if not d.is_dir():continue
        new=[p for p in sorted(d.glob("*.txt")) if p.name not in seen]
        for p in new:
            seen.add(p.name);t=tload(p) or "";slog("TEXT_WRITTEN",p.name,chars=len(t),sha256=sha_text(t))
        if new:bump()
def run_pipeline():
    if RUNS_DONE:_session_paths(datetime.now().astimezone().strftime("SH745-%Y%m%d-%H%M%S")+f"-RUN{len(RUNS_DONE)+1}")
    RUNS_DONE.append(SESSION_ID);LIVE.clear();LIVE.update(session=SESSION_ID);LINES.clear();CHECKS.clear();FIG_FILES.clear();FIG_ERRORS.clear();PROVENANCE.clear()
    STATE.update(running=True,started=utc_now(),finished=None,current=None,exp_dir=None,engine_rc=None,engine_pid=None,elapsed=None);STATE["fig_version"]+=1
    for k in STAGES:STATE["stages"][k]=dict(status="wait",seconds=None,note="",t0=None)
    banner(f"RUN {SESSION_ID} · {local_now()} · the TEST745 engine takes about 1.5 hours on an A100 (earlier run: {ANCHORS['seconds']:.0f} s)")
    def step(key,fn):
        STATE["current"]=key;stage_set(key,"run");_emit(f"── [{list(STAGES).index(key)+1}/{len(STAGES)}] {STAGES[key]}")
        try:
            note=fn();stage_set(key,"done",note);slog("STAGE_DONE",key,note=note);return True
        except Exception as ex:
            stage_set(key,"fail",f"{type(ex).__name__}: {ex}");slog("STAGE_FAILED",key,error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc()[-3000:]);return False
    try:
        ok=step("PRECHECK",stage_precheck)
        if ok:
            stop=threading.Event();w=threading.Thread(target=_text_watcher,args=(stop,),daemon=True);w.start()
            try:rc=run_engine()
            except Exception as ex:rc=-1;slog("ENGINE_START_FAILED",f"{type(ex).__name__}: {ex}")
            finally:stop.set()
            failed=next((l for _,_,l in reversed(LINES) if "TEST745_FAILED_CLOSED" in l or re.match(r"^FAIL ",l)),None)
            cur=next((k for k in ENGINE_STAGES if STATE["stages"][k]["status"] in("run","wait")),None)
            if cur:
                why=(failed or (f"engine process exit code {rc}" if rc else "engine ended before this stage completed"))
                stage_set(cur,"fail",why)
                for k in ENGINE_STAGES[ENGINE_STAGES.index(cur)+1:]:stage_set(k,"skip","not run — the engine stopped at "+cur)
            if EXP_ROOT.exists():
                dst=SESSION_DIR/"TEST745_EXPERIMENT";shutil.move(str(EXP_ROOT),str(dst));STATE["exp_dir"]=str(dst);slog("EXPERIMENT_DIR",f"moved into this RUN: {dst}")
        else:
            for k in ENGINE_STAGES:stage_set(k,"skip","not run — pre-flight failed")
        if STATE.get("exp_dir") and (Path(STATE["exp_dir"])/"TEST745_manifest.json").is_file():step("VERIFY",stage_verify)
        else:stage_set("VERIFY","skip","no cartridge manifest in this RUN")
        step("FIGURES",stage_figures);step("RECORDS",stage_records)
    finally:
        STATE.update(running=False,finished=utc_now(),current=None);bump()
        try:package_session()
        except Exception:pass
        banner(f"RUN VERDICT: {run_verdict()}\nRUN {SESSION_ID} finished {local_now()} · "+" · ".join(f"{k}:{v['status']}" for k,v in STATE["stages"].items()))
RUN_THREAD={"t":None}
def start_run():
    t=RUN_THREAD["t"]
    if t is not None and t.is_alive():return False
    RUN_THREAD["t"]=threading.Thread(target=run_pipeline,daemon=True,name="SH745-RUN");RUN_THREAD["t"].start();return True
# ===== END OF PART 2/3 =====
