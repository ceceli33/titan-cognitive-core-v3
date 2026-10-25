# ===== PART 3/4 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 4 — independent read-only verification, observational measures, twelve scientific figures from THIS RUN's
#              outputs (JPEG 300 dpi, layout QC; heat maps; the QWEN-3 expression printed verbatim), records and the single
#              RUN pipeline. Every number comes from this RUN's files; a missing output is drawn as missing.
# THIS PART  62,232 characters · its last line is  # ===== END OF PART 3/4 =====
# =====================================================================================================================
# ---------------------------------------------------------------------------------------------------------------------
# canonical manifest helpers (identical rules to 782.py) and the locked seal function (730.py, executed from its AST)
# ---------------------------------------------------------------------------------------------------------------------
HEX64=re.compile(r"^[0-9a-f]{64}$")
def canonical_seal(s):
    if not isinstance(s,dict) or set(s)!={"h","lower"}:raise ValueError("TENSOR_SHA_KEYS")
    return {"h":s["h"],"lower":[(x[0],x[1]) for x in s["lower"]]}
def canonical_entry(e):
    e=dict(e);e["tensor_sha"]=canonical_seal(e["tensor_sha"])
    if "native_layer_seals" in e:e["native_layer_seals"]=[(x[0],x[1]) for x in e["native_layer_seals"]]
    return e
def tensor_meta(cp):
    def m(t):return {"shape":list(t.shape),"dtype":str(t.dtype),"contiguous":bool(t.is_contiguous()) if hasattr(t,"is_contiguous") else None}
    return {"h":m(cp["h"]),"lower":[{"layer":i,"k":m(k),"v":m(v)} for i,(k,v) in enumerate(cp["lower"])],"layer_order":list(range(len(cp["lower"]))),
            "byteorder":sys.byteorder,"n":int(cp["n"]),"p":int(cp["p"]),"body_tokens":int(cp["body_tokens"]),"book_id":str(cp["book_id"])}
def meta_sha(meta):return sha_bytes(json.dumps(meta,sort_keys=True,separators=(",",":")).encode())
_SEAL_NS={}
def host_seal_cp(cp):
    if "seal_cp" not in _SEAL_NS:
        import torch
        src=RAW["730.py"].decode("utf-8");t=ast.parse(src);fn=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=="seal_cp")
        _SEAL_NS.update(torch=torch,sha=lambda b:hashlib.sha256(b).hexdigest());exec(compile(ast.Module(body=[fn],type_ignores=[]),"730.py","exec"),_SEAL_NS)
    return _SEAL_NS["seal_cp"](cp)
def manifests():
    q1=jload(rpath("q1_cartridges")/"Q1_CARTRIDGE_MANIFEST.json",{}) or {};q2=jload(rpath("q2_work")/"Q2_MANIFEST.json",{}) or {}
    bm=jload(rpath("master_bundle")/"MASTER_MANIFEST.json",{}) or {};rd=jload(rpath("master_bundle")/"READY.json",{}) or {}
    return q1,q2,bm,rd
def text_file(session,name):return tload(rpath(OUTDIRS[session])/name)
def panel():return jload(rpath("panel")/"SEALED_PANEL.json",{}) or {}
def panel_seal():return jload(rpath("panel")/"PANEL_SEAL.json",{}) or {}
def checks_of(session):return (results_of(session).get("checks") or [])
def chk(session,name):
    c=[x for x in checks_of(session) if x["name"]==name];return None if not c else all(x["pass"] for x in c)
def chk_detail(session,name):
    c=[x for x in checks_of(session) if x["name"]==name];return c[-1]["detail"] if c else None

# ---------------------------------------------------------------------------------------------------------------------
# observational measures (no semantic grade): source-specific vocabulary in every answer — computed OUTSIDE QWEN-3
# ---------------------------------------------------------------------------------------------------------------------
STOP=set("""about above after again against also although among another around because been before being below between both
could does doing down during each either else every from further have having here however into itself just least less made
make many more most much must neither never none only other others ought over same shall should since some such than that
their theirs them themselves then there these they this those through thus under until upon very what when where whether which
while whom whose will with within without would your yours document documents memory unknown information answer question
state states stated title publisher http https www html""".split())
def terms(t):return {w for w in re.findall(r"[a-z][a-z\-]{4,}",str(t or "").lower()) if w not in STOP}
ARMS=("NO_MEMORY","SOURCE_A_ONLY","SOURCE_B_ONLY","BASELINE_MASTER")
def control_metrics():
    A=tload(rpath("q1_sources")/"SOURCE_A_BODY_FORGED.txt");B=tload(rpath("q1_sources")/"SOURCE_B_BODY_FORGED.txt");pn=panel()
    if not A or not B or not pn:return None
    qt=terms(" ".join(q["question"] for q in pn["questions"])+" "+pn.get("qwen2_evaluation_prompt",""))
    TA,TB=terms(A),terms(B);SA=TA-TB-qt;SB=TB-TA-qt;SH=(TA&TB)-qt
    rows={};q3=results_of("QWEN3").get("answers") or [];ct=results_of("CONTROLS").get("answers") or []
    def cov(ans):
        t=terms(ans);return dict(a_hits=len(t&SA),b_hits=len(t&SB),shared_hits=len(t&SH),a_pct=round(100*len(t&SA)/max(len(SA),1),1),b_pct=round(100*len(t&SB)/max(len(SB),1),1),
                                 unknown=bool(re.match(r"^\W*UNKNOWN\b",str(ans or "").strip().upper())),chars=len(str(ans or "")))
    for a in ct:rows.setdefault(a["arm"],{})[a["id"]]=cov(a["answer"])
    for a in q3:rows.setdefault("QWEN3_BLIND",{})[a["id"]]=cov(a["answer"])
    q0=next((a["answer"] for a in q3 if a["id"]=="Q0"),None);c0=next((a["answer"] for a in ct if a["arm"]=="BASELINE_MASTER" and a["id"]=="Q0"),None)
    rep=dict(qwen3_q0_equals_controls_master_q0=(q0==c0) if (q0 is not None and c0 is not None) else None,
             qwen3_vs_controls_master_similarity=round(difflib.SequenceMatcher(None,(q0 or "").split(),(c0 or "").split(),autojunk=False).ratio(),4) if q0 and c0 else None)
    return dict(vocabulary=dict(a_specific=len(SA),b_specific=len(SB),shared=len(SH),question_terms_excluded=len(qt)),rows=rows,reproduction=rep,
                note="lexical proxy: distinct words (≥5 letters, stop-words removed) that occur only in SOURCE_A or only in SOURCE_B, counted in each answer; NOT a semantic grade")

# ---------------------------------------------------------------------------------------------------------------------
# VERIFY — independent, read-only
# ---------------------------------------------------------------------------------------------------------------------
def _load_cp(p):
    import torch
    return torch.load(p,map_location="cpu",weights_only=True)
def _equal(a,b):
    import torch
    return a.shape==b.shape and bool(torch.equal(a,b))
def _h3_map(cp,cols=600,cbins=64):
    """|H3| mean per (channel bin × token column) — CPU, float32"""
    h=cp["h"][0].float().numpy() if hasattr(cp["h"][0].float(),"numpy") else np.asarray(cp["h"][0].float())
    n,Hd=h.shape;cb=max(1,Hd//cbins);a=np.abs(h[:, :cb*cbins]).reshape(n,cbins,cb).mean(-1)
    edges=np.linspace(0,n,min(cols,n)+1).astype(int);out=np.stack([a[s:e].mean(0) for s,e in zip(edges[:-1],edges[1:]) if e>s],1)
    return out,edges,Hd
def _kv_norms(cp,cols=600):
    rows=[];labels=[]
    for i,(k,v) in enumerate(cp["lower"]):
        for nm,t in (("K",k),("V",v)):
            x=t[0].float().numpy() if hasattr(t[0].float(),"numpy") else np.asarray(t[0].float());x=np.sqrt((x**2).sum(axis=(0,2)))
            edges=np.linspace(0,len(x),min(cols,len(x))+1).astype(int);rows.append([x[s:e].mean() for s,e in zip(edges[:-1],edges[1:]) if e>s]);labels.append(f"L{i} {nm}")
    return np.array(rows,np.float32),labels
def stage_verify():
    q1,q2,bm,rd=manifests()
    if not q1.get("cartridges"):raise RuntimeError("no QWEN-1 cartridge manifest in this RUN — nothing to verify (nothing is substituted)")
    V=dict(cartridges=OrderedDict(),master={},ledger={},isolation={},texts={},problems=[],utc=utc_now());probs=V["problems"]
    E1={k:canonical_entry(v) for k,v in q1["cartridges"].items()}
    locs=[("SOURCE_A","q1_cartridges",E1.get("SOURCE_A")),("SOURCE_B","q1_cartridges",E1.get("SOURCE_B"))]
    if q2.get("cartridges"):
        E2={k:canonical_entry(v) for k,v in q2["cartridges"].items()}
        locs+=[("SOURCE_A","q2_work/cartridges",E2.get("SOURCE_A")),("SOURCE_B","q2_work/cartridges",E2.get("SOURCE_B")),("MASTER_02","q2_work/cartridges",E2.get("MASTER_02"))]
    if bm.get("master"):locs.append(("MASTER_02","master_bundle",canonical_entry(bm["master"])))
    cps={}
    for cid,where,e in locs:
        if not e:continue
        p=RUN_ROOT/where/e["file"];row=dict(id=cid,where=where,present=p.is_file())
        if p.is_file():
            t=time.perf_counter();s=sha_file(p);row.update(bytes=p.stat().st_size,sha256_now=s,sha256_manifest=e["sha256"],file_sha_ok=(s==e["sha256"]),hash_s=round(time.perf_counter()-t,2))
            cp=_load_cp(p);seal=host_seal_cp(cp);row["tensor_seal_ok"]=(seal==e["tensor_sha"]);mt=tensor_meta(cp)
            row.update(meta_sha_ok=(meta_sha(mt)==e.get("tensor_meta_sha256")),n=int(cp["n"]),p=int(cp["p"]),h_shape=list(cp["h"].shape),h_dtype=str(cp["h"].dtype),
                       k_shape=list(cp["lower"][0][0].shape),book_id_ok=(cp["book_id"]==cid),full_80_layer_kv_bytes=int(cp["n"])*80*8*128*2*2)
            cps[(cid,where)]=cp
        V["cartridges"][f"{cid}@{where}"]=row
        for k in ("file_sha_ok","tensor_seal_ok","meta_sha_ok","book_id_ok"):
            if k in row and not row[k]:probs.append(f"{cid}@{where} {k}")
        slog("VERIFIED_CARTRIDGE",f"{cid} @ {where}",**{k:v for k,v in row.items() if k in("file_sha_ok","tensor_seal_ok","meta_sha_ok","bytes","sha256_now")})
    if bm.get("master") and ("MASTER_02","master_bundle") in cps:
        M=cps[("MASTER_02","master_bundle")];A=cps.get(("SOURCE_A","q1_cartridges"));B=cps.get(("SOURCE_B","q1_cartridges"));me=canonical_entry(bm["master"])
        import torch
        P_=int(M["p"]);nA=int(A["body_tokens"]);n=int(M["n"])
        mm=V["master"]
        mm["parents_link_ok"]=[p["id"] for p in me["parents"]]==["SOURCE_A","SOURCE_B"] and all(p["sha256"]==E1[p["id"]]["sha256"]==sha_file(rpath("q1_cartridges")/E1[p["id"]]["file"]) for p in me["parents"])
        mm["h3_exact_concat"]=_equal(M["h"],torch.cat((A["h"],B["h"][:,P_:,:]),dim=1))
        mm["lower_A_part_exact"]=all(_equal(M["lower"][i][j][:,:,:P_+nA,:],A["lower"][i][j]) for i in range(4) for j in (0,1))
        mm["lower_B_values_exact"]=all(_equal(M["lower"][i][1][:,:,P_+nA:,:],B["lower"][i][1][:,:,P_:,:]) for i in range(4))
        mm["lower_B_keys_equal_unrotated"]=all(_equal(M["lower"][i][0][:,:,P_+nA:,:],B["lower"][i][0][:,:,P_:,:]) for i in range(4))
        mm["bundle_files"]=sorted(x.name for x in rpath("master_bundle").iterdir());mm["bundle_only_master"]=mm["bundle_files"]==["MASTER_02.pt","MASTER_MANIFEST.json","READY.json"]
        mm["bundle_manifest_sha_ok"]=sha_file(rpath("master_bundle")/"MASTER_MANIFEST.json")==rd.get("manifest_sha256")
        mm["bundle_has_no_text"]=not any(k in json.dumps(bm) for k in ("text_sha256","body_sha256")) and not list(rpath("master_bundle").glob("*.txt"))
        mm.update(n=n,P=P_,nA=nA,nB=int(B["body_tokens"]),boundary=P_+nA,schedule=me.get("rebuild_schedule"),sha256=me["sha256"],h3_seal=me["tensor_sha"]["h"])
        for k in ("parents_link_ok","h3_exact_concat","lower_A_part_exact","lower_B_values_exact","bundle_only_master","bundle_manifest_sha_ok","bundle_has_no_text"):
            if not mm.get(k):probs.append("MASTER "+k)
        hm,he,Hd=_h3_map(M);kv,kvl=_kv_norms(M);ha,_,_=_h3_map(A,cols=300);hb,_,_=_h3_map(B,cols=300)
        np.savez_compressed(DATA_DIR/"MASTER_ANATOMY.npz",h3=hm,h3_edges=he,kv=kv,kv_labels=np.array(kvl),src_a=ha,src_b=hb,P=P_,boundary=P_+nA,n=n,hidden=Hd);_private(DATA_DIR/"MASTER_ANATOMY.npz")
        slog("MASTER_VERIFIED","H3 = A ⊕ B exactly" if mm["h3_exact_concat"] else "H3 MISMATCH",**{k:v for k,v in mm.items() if isinstance(v,bool)})
    cps.clear();gc.collect()
    # process ledger: strictly sequential, exit 0, GPU released, same frozen weights in every session
    L=V["ledger"];ss=[LEDGER[s] for s in ENGINE_STAGES if s in LEDGER]
    L["sequential"]=all(ss[i]["start_t"]>=ss[i-1]["end_t"] for i in range(1,len(ss)));L["exit_codes"]={s["session"]:s["exit_code"] for s in ss}
    L["gpu_released"]={s["session"]:s["gpu_release"]["released"] for s in ss};L["pids"]={s["session"]:s.get("engine_pid") for s in ss}
    L["distinct_pids"]=len({s.get("engine_pid") for s in ss})==len(ss);L["users"]={s["session"]:s.get("engine_user") for s in ss}
    sent={s:results_of(s).get("weights_sentinel") for s in ("QWEN1","QWEN2","QWEN3","CONTROLS") if results_of(s).get("weights_sentinel")}
    L["weights_sentinel"]=sent;L["weights_identical_across_sessions"]=len(set(sent.values()))==1 if sent else None
    com={s:(results_of(s).get("model") or {}).get("commit") for s in ("QWEN1","QWEN2","QWEN3","CONTROLS") if results_of(s).get("model")}
    L["model_commit"]=com;L["model_commit_identical"]=len(set(com.values()))==1 if com else None
    for k in ("sequential","distinct_pids"):
        if not L[k]:probs.append("LEDGER "+k)
    if L["weights_identical_across_sessions"] is False:probs.append("LEDGER weights differ between sessions")
    # QWEN-3 access record
    r3=results_of("QWEN3");au=r3.get("access_audit") or {}
    I=V["isolation"];I.update(mode=ISO.get("mode"),netns=ISO.get("netns"),qwen3_os_level=r3.get("os_level_isolation"),qwen3_probe=r3.get("access_probe"),
                              qwen3_violations=au.get("violations"),qwen3_folders_opened=au.get("opened_under_root"),qwen3_forbidden=au.get("forbidden"),
                              qwen2_violations=(results_of("QWEN2").get("access_audit") or {}).get("violations"),root_fallback=ISO.get("root_fallback",[]))
    if r3 and (au.get("violations") or any(any(f.startswith(x) for x in ("q1_sources","q1_cartridges","q2_work")) for f in (au.get("files_under_root") or []))):probs.append("QWEN-3 opened a forbidden path")
    # texts written by the sessions: file SHA-256 = result record
    for s,key in (("QWEN3","answers"),("CONTROLS","answers")):
        for a in results_of(s).get(key) or []:
            t=text_file(s,a["file"]);ok=(t is not None and sha_text(t)==a["sha256"]);V["texts"][f"{s}/{a['file']}"]=ok
            if not ok:probs.append(f"text {s}/{a['file']}")
    cm=control_metrics()
    if cm:LIVE["metrics"]=cm;dump_json(DATA_DIR/"CONTROL_METRICS.json",cm)
    LIVE["verification"]=V;dump_json(VERIFY_FILE,V)
    n_ok=sum(1 for r in V["cartridges"].values() if r.get("file_sha_ok") and r.get("tensor_seal_ok") and r.get("meta_sha_ok"))
    mtxt=(f"MASTER = H3(A) ⊕ H3(B) exactly: {V['master'].get('h3_exact_concat')} · parents {V['master'].get('parents_link_ok')}" if V["master"] else
          "PARTIAL — no MASTER_02 bundle in this RUN, only the cartridges present were verified")
    note=(f"{n_ok}/{len(V['cartridges'])} cartridge files: file SHA-256 + locked tensor seals + tensor-meta seal equal to the manifests · {mtxt} · "
          f"sessions sequential {L['sequential']} · weights identical {L['weights_identical_across_sessions']} · "+(f"QWEN-3 forbidden opens {len(au.get('violations') or [])}" if r3 else "QWEN-3 did not run"))
    if probs:raise RuntimeError(note+" · PROBLEMS: "+", ".join(probs))
    return note
# ===== figures follow =====
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.linewidth":.9,"axes.edgecolor":NEU,"axes.labelcolor":INK,"xtick.color":NEU,"ytick.color":NEU,
                     "xtick.labelsize":8.5,"ytick.labelsize":8.5,"axes.labelsize":9.5,"axes.titlesize":10.5,"axes.titleweight":"bold","axes.titlelocation":"left",
                     "legend.fontsize":8.5,"legend.frameon":False})
FW,FH=13.333,7.5;OUT_DPI=300;MONO="DejaVu Sans Mono"
FIGURES=OrderedDict([
    ("F1",dict(n=1,title="Three Isolated Sessions — Architecture",slug="THREE_SESSION_ARCHITECTURE",tab="OVERVIEW")),
    ("F2",dict(n=2,title="QWEN-1 — Real Sources into Physical Cartridges",slug="QWEN1_SOURCE_CARTRIDGES",tab="SOURCES · QWEN-1")),
    ("F3",dict(n=3,title="MASTER_02 — Anatomy of the Physical Cartridge",slug="MASTER_CARTRIDGE_ANATOMY",tab="MASTER · QWEN-2")),
    ("F4",dict(n=4,title="Native Numerical Fusion — Layer × Token Heat Map",slug="NATIVE_FUSION_HEATMAP",tab="MASTER · QWEN-2")),
    ("F5",dict(n=5,title="Reload Parity — 80 Layers, Three Processes",slug="RELOAD_PARITY_HEATMAP",tab="MASTER · QWEN-2")),
    ("F6",dict(n=6,title="SHA-256 and Manifest Integrity Chain",slug="SHA_MANIFEST_INTEGRITY",tab="INTEGRITY")),
    ("F7",dict(n=7,title="QWEN-3 — The MASTER in Human Language (verbatim)",slug="QWEN3_EXPRESSION_VERBATIM",tab="BLIND READING · QWEN-3")),
    ("F8",dict(n=8,title="QWEN-3 — Question Panel and Attention on the MASTER",slug="QWEN3_PANEL_AND_ATTENTION",tab="BLIND READING · QWEN-3")),
    ("F9",dict(n=9,title="Control Conditions — What Each Memory Contributes",slug="CONTROL_CONDITIONS",tab="CONTROLS")),
    ("F10",dict(n=10,title="Process Isolation and GPU Release",slug="PROCESS_ISOLATION_GPU",tab="ISOLATION")),
    ("F11",dict(n=11,title="Timing and Memory Measurements",slug="TIMING_AND_MEMORY",tab="RESOURCES")),
    ("F12",dict(n=12,title="What This Run Shows — Claims Ledger",slug="CLAIMS_LEDGER",tab="OVERVIEW"))])
BASE_FIGURES=OrderedDict(FIGURES)
FIG_FILES={};FIG_ERRORS={};PROVENANCE={}
BADGE_COL={"SCHEMATIC":NEU,"LIVE MEASUREMENT":OK_COL,"SEALED MEMORY":COL["M"],"OBSERVATIONAL":AMBER,"VERIFICATION RECORD":NEU,"NOT PRODUCED IN THIS RUN":RED}
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
def vline(fig,x,y0,y1,col=RED,lw=1.6,ls="--"):fig.add_artist(Line2D([x,x],[y0,y1],transform=fig.transFigure,color=col,lw=lw,ls=ls,zorder=4))
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
    T(fig,.035,.022,f"{APP_NAME} · {EXPERIMENT} · demo {CODE_VERSION} · {_date()} · 782.py git blob {LOCKS[ENGINE_NAME][:10]} · run {SESSION_ID}"+(" · SIMULATION" if SIM else "")+f" · Figure {meta['n']}/{len(BASE_FIGURES)}",
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
    stem=("SIMULATION_" if SIM else "")+f"TEST782_FIG{num:02d}_{meta['slug']}{suffix}";jpg=FIG_DIR/(stem+".jpg")
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
    fig_footer(fig,key,"Placeholder by design: TEST782 figures are drawn only from outputs of this RUN (no earlier run, no representative values).")
    return save_fig(fig,key,"NOT PRODUCED IN THIS RUN",["(none — output missing)"],"_NOT_PRODUCED")
def _axstyle(ax,fs=8):
    for s in ("top","right"):ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=fs)
def _t(u):
    try:return datetime.fromisoformat(u).timestamp()
    except Exception:return None
def heat(ax,M,exact=None,vmin=1e-4,vmax=1.0,cmap="magma_r",extent=None,label=None):
    """log-scale heat map; cells that are bit-identical are drawn in a separate green, never as small numbers"""
    Mp=np.array(M,dtype=np.float64);Mp=np.where(Mp<=0,np.nan,Mp);Mp=np.clip(Mp,vmin,vmax)
    im=ax.imshow(Mp,aspect="auto",origin="lower",cmap=cmap,norm=LogNorm(vmin=vmin,vmax=vmax),interpolation="nearest",extent=extent)
    Z=np.zeros_like(M,dtype=float)
    if exact is not None:Z=np.where(np.asarray(exact),1.0,np.nan)
    else:Z=np.where(np.asarray(M)==0,1.0,np.nan)
    ax.imshow(Z,aspect="auto",origin="lower",cmap=ListedColormap(["#A7F3D0"]),vmin=0,vmax=1,interpolation="nearest",extent=extent)
    return im
EXACT_GREEN="#A7F3D0"
# ===== figure functions =====
def _res(s,k,default=None):return (results_of(s).get(k) if results_of(s) else None) or default
def fig1():
    k="F1"
    if not LEDGER.get("QWEN1"):return fig_missing(k,"The architecture is drawn from the session processes of this RUN.","No engine session ran in this RUN.")
    fig=fig_base(k,"Five OS processes, strictly one after the other — only the files named on the arrows cross a session boundary · values measured in this RUN","SCHEMATIC")
    lanes=[("PREFLIGHT","CPU gate",["AST dependency scan","16 SHA / manifest simulations","tokenizer types · GPU budget","seals the question panel"]),
           ("QWEN1","source session",["reads: 2 web documents","forges SOURCE_A, SOURCE_B","H3 + K/V L0–L3 → SSD","SHA-256 file + tensors"]),
           ("QWEN2","consolidation session",["reads: 2 cartridges only","native numerical fusion","MASTER_02 → SSD, sealed","80/80 layer parity"]),
           ("QWEN3","blind reading session",["reads: MASTER_02 only","no source text / cartridge","80/80 independent reload","expresses it in language"]),
           ("CONTROLS","control session",["NO_MEMORY · A_ONLY","B_ONLY · BASELINE_MASTER","same sealed questions","(separate process)"])]
    W=.172;G=.0195;x0=.035
    for i,(s,role,lines) in enumerate(lanes):
        x=x0+i*(W+G);c=SCOL[s];L=LEDGER.get(s) or {}
        box(fig,x,.47,W,.37,ec=c,lw=1.6);rect(fig,x,.84-.034,W,.034,c,z=2)
        Tc(fig,x+.004,x+W-.004,.823,f"{SNAME[s]} · {role}",size=9.6,weight="bold",color="white")
        info=[f"pid {L.get('engine_pid','—')} · user {L.get('engine_user','—')}",f"{str(L.get('start',''))[11:19]} → {str(L.get('end',''))[11:19]} UTC",
              f"exit {L.get('exit_code','—')} · {L.get('seconds',0) or 0:.0f} s",f"GPU after exit {((L.get('gpu_release') or {}).get('used_mib','—'))} MiB",
              ("network: namespace" if L.get("netns") else ("network: offline mode" if L.get("offline") else "network: online"))]
        for j,t in enumerate(info):Tc(fig,x+.006,x+W-.006,.785-j*.027,t,size=7.6,color=INK2,mono=(j<2))
        hline(fig,x+.008,x+W-.008,.648,RULE)
        for j,t in enumerate(lines):Tc(fig,x+.006,x+W-.006,.622-j*.034,t,size=8.0,color=INK)
    cross=[(0,"sealed question panel (SHA)"),(1,"SOURCE_A.pt · SOURCE_B.pt · manifest (no text)"),(2,"MASTER_02.pt · restricted manifest"),(3,"MASTER_02.pt (read-only)")]
    for i,lab in cross:
        xa=x0+(i+1)*(W+G)-G;arrow(fig,xa+.001,.66,xa+G-.001,.66,col=SCOL[ENGINE_STAGES[i+1]],lw=1.6,ms=10)
    for i,lab in cross:
        xa=x0+(i+1)*(W+G)-G/2;Tc(fig,xa-.085,xa+.085,.445,("↑ crosses: "+lab) if i<3 else "↑ MASTER read by CONTROLS too",size=7.0,color=MUTED)
    ss=[LEDGER[s] for s in ENGINE_STAGES if s in LEDGER and LEDGER[s].get("end_t")]
    if ss:
        t0=ss[0]["start_t"];t1=ss[-1]["end_t"];span=max(t1-t0,1);X0,X1=.08,.955
        T(fig,.035,.375,"time line of this RUN — processes never overlap; the GPU is checked empty after every exit",size=8.6,weight="bold",color=INK2)
        hline(fig,X0,X1,.315,NEU,1.0)
        for s in ss:
            a=X0+(s["start_t"]-t0)/span*(X1-X0);b=X0+(s["end_t"]-t0)/span*(X1-X0);rect(fig,a,.295,max(b-a,.002),.04,SCOL[s["session"]],z=2)
        for j,s in enumerate(ss):
            a=X0+(s["start_t"]-t0)/span*(X1-X0);b=X0+(s["end_t"]-t0)/span*(X1-X0)
            T(fig,.035,.255-j*.028,f"{SNAME[s['session']]:<9}",size=7.6,weight="bold",color=SCOL[s["session"]],mono=True)
            T(fig,.105,.255-j*.028,f"{(s['start_t']-t0)/60:6.1f} → {(s['end_t']-t0)/60:6.1f} min  ·  {s['seconds']/60:5.1f} min  ·  GPU released {okm((s.get('gpu_release') or {}).get('released'))}",size=7.4,color=INK2,mono=True,xmax=.55)
        T(fig,X0,.348,"0 min",size=7.2,color=MUTED);T(fig,X1,.348,f"{span/60:.0f} min",size=7.2,color=MUTED,ha="right")
    sen=(LIVE.get("verification") or {}).get("ledger",{})
    box(fig,.585,.095,.38,.17,ec=NEU,fc=PANEL,lw=1.1)
    T(fig,.595,.24,"Frozen Qwen2.5-72B-Instruct · NF4 · BF16 · CUT3 — one model, four loads",size=8.8,weight="bold",xmax=.96)
    T(fig,.595,.21,f"weights sentinel identical in all GPU sessions: {okm(sen.get('weights_identical_across_sessions'))}",size=7.8,color=INK2,xmax=.96)
    T(fig,.595,.185,f"model snapshot identical: {okm(sen.get('model_commit_identical'))} · isolation mode: {ISO.get('mode')}",size=7.8,color=INK2,xmax=.96)
    T(fig,.595,.16,"no GPU state, KV cache, Python object or text crosses a boundary —",size=7.8,color=INK2,xmax=.96)
    T(fig,.595,.135,"only the SSD files named on the arrows (each SHA-256 verified on arrival)",size=7.8,color=INK2,xmax=.96)
    T(fig,.595,.11,"QWEN-2/QWEN-3: own Linux users · source folders unreadable to them",size=7.8,color=AMBER,xmax=.96)
    fig_footer(fig,k,"PIDs, users, times, exit codes and GPU memory after exit: PROCESS_LEDGER.json (host) and each session's results file. Arrows = the only files a later session may read.")
    return save_fig(fig,k,"SCHEMATIC",["PROCESS_LEDGER.json","GPU_SAMPLES.json","TEST782_<SESSION>_results.json","POST_RUN_VERIFICATION.json"])
def fig2():
    k="F2";r1=results_of("QWEN1");q1,_,_,_=manifests();E=q1.get("cartridges") or {}
    if not E or not r1.get("sources"):return fig_missing(k,"The source cartridges are drawn from QWEN-1's records of this RUN.","QWEN-1 did not complete.")
    fig=fig_base(k,"Each document is read ONCE, by QWEN-1 only, and written into the model's own internal states — the text never leaves QWEN-1's private folder","LIVE MEASUREMENT")
    V=(LIVE.get("verification") or {}).get("cartridges") or {};tm=r1.get("timings") or {}
    try:Z=np.load(DATA_DIR/"MASTER_ANATOMY.npz",allow_pickle=False)
    except Exception:Z=None
    for i,cid in enumerate(("SOURCE_A","SOURCE_B")):
        s=r1["sources"][cid];e=E[cid];v=V.get(f"{cid}@q1_cartridges") or {};x=.035+i*.475;w=.455;c=COL["A" if i==0 else "B"]
        box(fig,x,.40,w,.46,ec=c,lw=1.6);rect(fig,x,.86-.034,w,.034,c,z=2)
        T(fig,x+.01,.843,f"{cid} · {SRC_LABEL[cid]}",size=9.4,weight="bold",color="white",xmax=x+w-.01)
        rows=[("page title",short(s.get("title") or "—",70)),("URL",short(s.get("url"),70)),("retrieved",f"{str(s.get('retrieved_utc',''))[:19]} UTC · {s.get('mode')} · HTTP {s.get('http_status','—')}"),
              ("HTML SHA-256",k_sha(s.get("html_sha256"),40)),("text SHA-256",k_sha(s.get("text_sha256"),40)),
              ("tokens",f"{s.get('body_tokens'):,} forged (TEST781 reference {s.get('reference_test781_tokens'):,})"+(" · TRUNCATED" if s.get("truncated") else "")),
              ("H3 tensor",f"{tuple(v.get('h_shape') or [])} {str(v.get('h_dtype','')).replace('torch.','')} · K/V L0–L3 {tuple(v.get('k_shape') or [])}"),
              ("cartridge file",f"{fmt_b(v.get('bytes'))} on SSD · full 80-layer K/V would be {fmt_b(v.get('full_80_layer_kv_bytes'))}"),
              ("file SHA-256",k_sha(e.get("sha256"),40)),("tensor seal H3",k_sha((e.get("tensor_sha") or {}).get("h"),40)),
              ("forge · write+seal",f"{(tm.get('forge_'+cid) or ['—'])[0]} s · {(tm.get('ssd_write_and_seal_'+cid) or ['—'])[0]} s"),
              ("reopen from SSD",f"file {okm(v.get('file_sha_ok'))} · tensors {okm(v.get('tensor_seal_ok'))} · meta {okm(v.get('meta_sha_ok'))} · 80-layer seals recorded")]
        for j,(a,b) in enumerate(rows):
            y=.80-j*.0325;T(fig,x+.01,y,a,size=7.6,weight="bold",color=MUTED);T(fig,x+.115,y,b,size=7.6,color=INK,mono=(("SHA" in a) or a=="tensor seal H3"),xmax=x+w-.008)
        if Z is not None:
            ax=fig.add_axes([x+.035,.12,w-.05,.21]);M=Z["src_a" if i==0 else "src_b"]
            ax.imshow(np.log10(M+1e-6),aspect="auto",origin="lower",cmap="viridis",interpolation="nearest");ax.set_yticks([0,M.shape[0]-1]);ax.set_yticklabels(["0",str(int(Z["hidden"])-1)])
            ax.set_xticks([0,M.shape[1]-1]);ax.set_xticklabels(["token 0",f"token {int(e['n'])-1}"]);ax.set_ylabel("H3 channel",fontsize=8)
            ax.set_title(f"stored H3 of {cid} — log10 |activation| (channel bins × tokens)",fontsize=8.6,color=c);_axstyle(ax,7.5)
    fig_footer(fig,k,"QWEN-1 records (TEST782_QWEN1_results.json, Q1_CARTRIDGE_MANIFEST.json) and the host's read-only re-hash. Source texts stay in QWEN-1's private folder (not redistributed).")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST782_QWEN1_results.json","Q1_CARTRIDGE_MANIFEST.json","POST_RUN_VERIFICATION.json","MASTER_ANATOMY.npz"])
def fig3():
    k="F3";mm=(LIVE.get("verification") or {}).get("master") or {}
    try:Z=np.load(DATA_DIR/"MASTER_ANATOMY.npz",allow_pickle=False)
    except Exception:Z=None
    if not mm or Z is None:return fig_missing(k,"The MASTER anatomy is measured from the MASTER_02 file of this RUN.","MASTER_02 was not produced or not verified in this RUN.")
    fig=fig_base(k,"What MASTER_02 physically contains — measured from the file on the SSD · it is the frozen model's own states of BOTH documents, not a text summary","LIVE MEASUREMENT")
    n=int(Z["n"]);P_=int(Z["P"]);bd=int(Z["boundary"]);he=Z["h3_edges"];cols=Z["h3"].shape[1]
    xb=lambda tok:np.searchsorted(he,tok)-0.5
    T(fig,.07,.866,"H3 (layer-3 output) stored for every token — log10 mean |activation| per channel bin",size=9.2,weight="bold",xmax=.67)
    ax=fig.add_axes([.07,.47,.60,.34]);ax.imshow(np.log10(Z["h3"]+1e-6),aspect="auto",origin="lower",cmap="viridis",interpolation="nearest")
    for t,c in ((P_,"#F59E0B"),(bd,RED)):ax.axvline(xb(t),color=c,lw=1.6,ls="--")
    ax.set_yticks([0,Z["h3"].shape[0]-1]);ax.set_yticklabels(["0",str(int(Z["hidden"])-1)]);ax.set_ylabel("H3 hidden channel",fontsize=8.5);ax.set_xticks([]);_axstyle(ax,7.5)
    ax2=fig.add_axes([.07,.25,.60,.17]);kv=Z["kv"];ax2.imshow(np.log10(kv+1e-6),aspect="auto",origin="lower",cmap="cividis",interpolation="nearest")
    ax2.set_yticks(range(len(Z["kv_labels"])));ax2.set_yticklabels([str(x) for x in Z["kv_labels"]],fontsize=6.6)
    for t,c in ((P_,"#F59E0B"),(bd,RED)):ax2.axvline(xb(t),color=c,lw=1.6,ls="--")
    ax2.set_xticks([0,xb(P_),xb(bd),cols-1]);ax2.set_xticklabels(["0",f"{P_}",f"{bd}",f"{n-1}"],fontsize=7.5);ax2.set_xlabel("token position in MASTER_02",fontsize=8)
    ax2.set_title("K / V of layers 0–3 stored per token — log10 L2 norm",fontsize=9.0);_axstyle(ax2,7.5)
    for a,b,lab,c in ((0,P_,"system prefix",MUTED),(P_,bd,"SOURCE_A body (European Commission)",COL["A"]),(bd,n,"SOURCE_B body (Future of Life Institute)",COL["B"])):
        xa=.07+.60*(np.searchsorted(he,a)/cols);xe=.07+.60*(np.searchsorted(he,b)/cols)
        if xe-xa>.05:Tc(fig,xa+.002,xe-.002,.828,lab,size=8.0,weight="bold",color=c)
    box(fig,.695,.10,.27,.75,ec=COL["M"],lw=1.5)
    T(fig,.705,.825,"MASTER_02 — facts measured from the file",size=9.4,weight="bold",color=COL["M"],xmax=.96)
    facts=[("tokens",f"{n:,} = prefix {P_} + A {mm.get('nA'):,} + B {mm.get('nB'):,}"),("A | B boundary",f"token {bd} (sealed in the manifest)"),
           ("file SHA-256",k_sha(mm.get("sha256"),26)),("tensor seal H3",k_sha(mm.get("h3_seal"),26)),
           ("H3(MASTER) = H3(A) ⊕ H3(B body)","bit-identical "+okm(mm.get("h3_exact_concat"))),("L0–L3 rows of A","bit-identical to SOURCE_A "+okm(mm.get("lower_A_part_exact"))),
           ("L0–L3 values of B","bit-identical to SOURCE_B "+okm(mm.get("lower_B_values_exact"))),("L0–L3 keys of B","re-rotated to new positions (RoPE)"),
           ("layers 4–79","not stored — rebuilt by the frozen model"),("parents","SOURCE_A, SOURCE_B (SHA links "+okm(mm.get("parents_link_ok"))+")")]
    for j,(a,b) in enumerate(facts):
        y=.785-j*.062;T(fig,.705,y,a,size=7.8,weight="bold",color=MUTED,xmax=.96);T(fig,.705,y-.026,b,size=7.8,color=INK,mono=("SHA" in a or "seal" in a),xmax=.96)
    T(fig,.07,.17,"Reading the picture: left of the orange line = the shared system prefix; between the lines = SOURCE_A; right of the red line = SOURCE_B.",size=8.0,color=INK2,xmax=.68)
    T(fig,.07,.14,"Every column is one stretch of tokens; colour = magnitude of the stored internal state. Nothing in the file is text — it is H3 and K/V.",size=8.0,color=INK2,xmax=.68)
    T(fig,.07,.11,"The model reads this file by injecting H3 at layer 3 and recomputing layers 4–79 (Figure 5: bit-identical every time).",size=8.0,color=AMBER,xmax=.68)
    fig_footer(fig,k,"Host, read-only, CPU: torch.load(MASTER_02.pt) → |H3| per channel bin and token bin; L2 norms of K/V L0–L3; equalities checked with torch.equal against SOURCE_A / SOURCE_B files.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["master_bundle/MASTER_02.pt","q1_cartridges/SOURCE_A.pt, SOURCE_B.pt","MASTER_ANATOMY.npz","POST_RUN_VERIFICATION.json"])
def _heatdata():
    try:return np.load(rpath("q2_work")/"HEATMAPS_QWEN2.npz",allow_pickle=False)
    except Exception:return None
def fig4():
    k="F4";Z=_heatdata();r2=results_of("QWEN2")
    if Z is None:return fig_missing(k,"The fusion heat map is measured by QWEN-2 on the fused memory of this RUN.","QWEN-2 heat-map data not produced in this RUN.")
    fig=fig_base(k,"Difference between the fused memory and the two documents mounted ALONE (same positions) — where fusion changed the model's internal states","LIVE MEASUREMENT")
    ed=Z["edges"];n=int(Z["n"]);bd=int(Z["boundary"]);P_=int(Z["P"]);nb=len(ed)-1;bi=np.searchsorted(ed,bd)-0.5
    axes=[]
    for j,(key,lab) in enumerate((("k","KEYS (K)"),("v","VALUES (V)"))):
        ax=fig.add_axes([.065+j*.315,.20,.27,.60]);im=heat(ax,Z["fusion_rel_"+key],Z["fusion_exact_"+key],vmin=1e-3,vmax=2.0)
        ax.axvline(bi,color=RED,lw=1.5,ls="--");ax.axhline(3.5,color="#2563EB",lw=1.2,ls=":")
        ax.set_xticks([0,bi,nb-1]);ax.set_xticklabels(["0",f"A|B {bd}",f"{n-1}"],fontsize=7.5);ax.set_xlabel("token position (bins)",fontsize=8)
        ax.set_yticks([0,4,20,40,60,79]);ax.set_yticklabels(["L0","L4","L20","L40","L60","L79"],fontsize=7.5)
        ax.set_title(f"{lab} — relative L2 difference",fontsize=9.2);_axstyle(ax,7.5);axes.append(ax)
    cax=fig.add_axes([.648,.20,.010,.60]);cb=fig.colorbar(im,cax=cax);cb.ax.tick_params(labelsize=7);cb.set_label("‖fused − alone‖ / ‖alone‖ (log)",fontsize=7.2,labelpad=2)
    s=r2.get("fusion_footprint") or {}
    box(fig,.715,.20,.25,.60,ec=COL["M"],lw=1.4)
    T(fig,.725,.775,"what the heat map shows",size=9.2,weight="bold",color=COL["M"],xmax=.96)
    lines=[(f"green = bit-identical (exactly 0)",OK_COL),(f"SOURCE_A rows, all 80 layers: identical",INK),
           (f"   K {s.get('A_region_exact_layers_K','—')}/80 · V {s.get('A_region_exact_layers_V','—')}/80 layers exact",INK2),
           (f"SOURCE_B rows, layers 0–3: carried as stored",INK),(f"   K {s.get('B_region_exact_layers_K','—')} · V {s.get('B_region_exact_layers_V','—')} layers exact (K re-rotated)",INK2),
           (f"SOURCE_B rows from layer {s.get('B_region_first_divergent_layer','—')} up: recomputed",INK),
           ("   while attending to SOURCE_A → B now carries",INK2),("   the context of A (causal order A → B)",INK2),
           ("This is a measured cross-attention footprint.",AMBER),("It is NOT, by itself, proof of new semantic",AMBER),("synthesis (Figure 12).",AMBER)]
    for j,(t,c) in enumerate(lines):T(fig,.725,.735-j*.045,t,size=7.8,color=c,xmax=.96)
    T(fig,.065,.85,f"reference = SOURCE_A alone (rows 0…{bd-1}) + SOURCE_B alone moved to rows {bd}…{n-1} with the locked RoPE rephase · {nb} token bins × 80 layers · dotted line = CUT3 boundary (L3 | L4)",size=7.8,color=MUTED,xmax=.965)
    fig_footer(fig,k,"QWEN-2 (GPU, in its own process): fused memory = locked TEST757 append; isolated memories = locked initialize_native; values in HEATMAPS_QWEN2.npz (QWEN-2 private folder, read by the host after the run).")
    return save_fig(fig,k,"LIVE MEASUREMENT",["q2_work/HEATMAPS_QWEN2.npz","TEST782_QWEN2_results.json fusion_footprint"])
def fig5():
    k="F5";Z=_heatdata();r2=results_of("QWEN2");r3=results_of("QWEN3");rc=results_of("CONTROLS")
    if Z is None or not r2.get("master_parity"):return fig_missing(k,"Reload parity is measured by QWEN-2 and QWEN-3 in this RUN.","MASTER parity data not produced in this RUN.")
    fig=fig_base(k,"MASTER_02 reloaded from the SSD and rebuilt (layers 4–79) — compared with the native fused memory, layer by layer, bit for bit","VERIFICATION RECORD")
    ed=Z["edges"];nb=len(ed)-1;bd=int(Z["boundary"]);bi=np.searchsorted(ed,bd)-0.5
    pb=np.maximum(Z["parity_boundary_k"],Z["parity_boundary_v"]);pn=np.maximum(Z["parity_naive_k"],Z["parity_naive_v"])
    for j,(M,lab,c) in enumerate(((pb,"sealed boundary-aware reload (the path used)",OK_COL),(pn,"naive one-pass rebuild (negative control)",RED))):
        ax=fig.add_axes([.065+j*.29,.20,.25,.58]);im=heat(ax,M,None,vmin=1e-3,vmax=64,cmap="inferno_r")
        ax.axvline(bi,color=COL["M"],lw=1.3,ls="--");ax.set_xticks([0,bi,nb-1]);ax.set_xticklabels(["0","A|B",f"{int(Z['n'])-1}"],fontsize=7.5)
        ax.set_yticks([0,4,20,40,60,79]);ax.set_yticklabels(["L0","L4","L20","L40","L60","L79"],fontsize=7.5);ax.set_title(lab,fontsize=8.8,color=c);_axstyle(ax,7.5)
        ex=int(Z["boundary_exact_layers"] if j==0 else Z["naive_exact_layers"]);Tc(fig,.065+j*.29,.065+j*.29+.25,.815,f"{ex}/80 layers bit-identical",size=9.4,weight="bold",color=c)
    cax=fig.add_axes([.62,.20,.010,.58]);cb=fig.colorbar(im,cax=cax);cb.ax.tick_params(labelsize=7);cb.set_label("max |Δ| per cell (log) · green = 0",fontsize=7.5)
    box(fig,.675,.12,.29,.70,ec=NEU,lw=1.3);T(fig,.685,.795,"80-layer parity in every process",size=9.2,weight="bold",xmax=.96)
    L3=LEDGER.get("QWEN3") or {};LC=LEDGER.get("CONTROLS") or {};L2=LEDGER.get("QWEN2") or {}
    def pc(r,name):
        d=next((c["detail"] for c in (r.get("checks") or []) if c["name"]==name),None);return f"{d}" if d is not None else "—"
    rows=[("QWEN-2 · native vs SSD reload",f"{(r2.get('master_parity') or {}).get('exact_layers','—')}/80",f"pid {L2.get('engine_pid','—')} · {L2.get('engine_user','—')}"),
          ("QWEN-2 · second SSD reload",pc(r2,"MASTER_SECOND_RELOAD_80_LAYER_PARITY")+"/80","same process, file reloaded"),
          ("QWEN-3 · independent reload",f"{(r3.get('master_parity') or {}).get('exact_layers','—')}/80",f"NEW process pid {L3.get('engine_pid','—')} · {L3.get('engine_user','—')}"),
          ("CONTROLS · BASELINE_MASTER",pc(rc,"CONTROL_MEMORY_80_LAYER_PARITY_BASELINE_MASTER")+"/80",f"NEW process pid {LC.get('engine_pid','—')}"),
          ("QWEN-2 · SOURCE_A vs QWEN-1 seals",pc(r2,"SOURCE_CROSS_PROCESS_80_LAYER_PARITY_SOURCE_A")+"/80","across processes"),
          ("QWEN-2 · SOURCE_B vs QWEN-1 seals",pc(r2,"SOURCE_CROSS_PROCESS_80_LAYER_PARITY_SOURCE_B")+"/80","across processes"),
          ("CONTROLS · SOURCE_A / SOURCE_B",pc(rc,"CONTROL_MEMORY_80_LAYER_PARITY_SOURCE_A_ONLY")+"/80 · "+pc(rc,"CONTROL_MEMORY_80_LAYER_PARITY_SOURCE_B_ONLY")+"/80","across processes")]
    for j,(a,b,c) in enumerate(rows):
        y=.75-j*.083;T(fig,.685,y,a,size=7.8,weight="bold",xmax=.96);T(fig,.685,y-.027,b,size=9,weight="bold",color=OK_COL,mono=True);T(fig,.76,y-.027,c,size=7.2,color=MUTED,xmax=.96)
    T(fig,.065,.86,"parity = SHA-256 of every K and V tensor of all 80 layers equal (TEST730 memory_seals); heat maps: max |Δ| in each (layer, token-bin) cell",size=7.8,color=MUTED,xmax=.965)
    fig_footer(fig,k,"The naive one-pass rebuild uses a different BF16 chunk schedule (TEST758–760); the boundary sealed in the manifest restores bit-identity — measured, not assumed.")
    return save_fig(fig,k,"VERIFICATION RECORD",["q2_work/HEATMAPS_QWEN2.npz","TEST782_QWEN2_results.json","TEST782_QWEN3_results.json","TEST782_CONTROLS_results.json"])
MANDATORY=("MASTER_PHYSICAL_FILE_SHA","MASTER_TENSOR_SHA","MASTER_MANIFEST_ROUNDTRIP","MASTER_PARENT_SHA_LINKS","MASTER_RELOAD_INTEGRITY","MASTER_NUMERICAL_80_LAYER_PARITY","MASTER_INDEPENDENT_RELOAD")
def fig6():
    k="F6";rp=results_of("PREFLIGHT");q1,q2,bm,rd=manifests();V=LIVE.get("verification") or {}
    if not rp.get("sha_simulations"):return fig_missing(k,"The integrity chain is drawn from PREFLIGHT, QWEN-2, QWEN-3 and the host verification of this RUN.","PREFLIGHT did not complete.")
    fig=fig_base(k,"Every file that crosses a session boundary is identified by SHA-256 — and every seal is checked by the receiving process and again by the host","VERIFICATION RECORD")
    E1=q1.get("cartridges") or {};me=bm.get("master") or {};C=V.get("cartridges") or {}
    nodes=[("SOURCE_A",E1.get("SOURCE_A"),COL["A"],"QWEN-1 · q1_cartridges"),("SOURCE_B",E1.get("SOURCE_B"),COL["B"],"QWEN-1 · q1_cartridges"),
           ("MASTER_02",me or None,COL["M"],"QWEN-2 · master_bundle")]
    for j,(cid,e,c,where) in enumerate(nodes):
        y=.70-j*.22;box(fig,.035,y,.30,.16,ec=c,lw=1.5);rect(fig,.035,y+.16-.03,.30,.03,c,z=2)
        T(fig,.045,y+.145,f"{cid} · {where}",size=8.6,weight="bold",color="white",xmax=.33)
        if e:
            v=C.get(f"{cid}@{'q1_cartridges' if cid!='MASTER_02' else 'master_bundle'}") or {}
            T(fig,.045,y+.105,"file "+str(e.get("sha256",""))[:40],size=7.0,mono=True,xmax=.33)
            T(fig,.045,y+.078,"H3   "+str((e.get("tensor_sha") or {}).get("h",""))[:40],size=7.0,mono=True,xmax=.33)
            T(fig,.045,y+.051,"meta "+str(e.get("tensor_meta_sha256",""))[:40],size=7.0,mono=True,xmax=.33)
            T(fig,.045,y+.022,f"host re-hash: file {okm(v.get('file_sha_ok'))} · tensors {okm(v.get('tensor_seal_ok'))} · meta {okm(v.get('meta_sha_ok'))}",size=7.4,color=OK_COL if v.get("file_sha_ok") else RED,xmax=.33)
        else:T(fig,.045,y+.07,"not produced in this RUN",size=8,color=RED)
    if me:
        for yy in (.665,.445):Tc(fig,.035,.335,yy,"↓ file SHA-256 recorded as parent of MASTER_02 ↓",size=7.4,color=COL["M"])
        T(fig,.035,.10,f"parents of MASTER_02 = SHA-256 of SOURCE_A and SOURCE_B files: {okm((V.get('master') or {}).get('parents_link_ok'))}",size=7.8,color=COL["M"],xmax=.36)
    box(fig,.375,.10,.25,.76,ec=NEU,lw=1.3);T(fig,.385,.835,"7 mandatory MASTER checks",size=9.2,weight="bold",xmax=.62)
    T(fig,.385,.805,"check",size=7.2,weight="bold",color=MUTED);T(fig,.545,.805,"QWEN-2",size=7.2,weight="bold",color=MUTED);T(fig,.588,.805,"QWEN-3",size=7.2,weight="bold",color=MUTED)
    for j,name in enumerate(MANDATORY):
        y=.77-j*.085;a=chk("QWEN2",name);b=chk("QWEN3","MASTER_NUMERICAL_EXACT_80_PARITY" if name=="MASTER_NUMERICAL_80_LAYER_PARITY" else name)
        T(fig,.385,y,name.replace("MASTER_",""),size=7.3,xmax=.54,mono=True)
        T(fig,.548,y,"PASS" if a else ("FAIL" if a is False else "–"),size=7.6,weight="bold",color=OK_COL if a else (RED if a is False else MUTED))
        T(fig,.590,y,"PASS" if b else ("FAIL" if b is False else "–"),size=7.6,weight="bold",color=OK_COL if b else (RED if b is False else MUTED))
    T(fig,.385,.21,"– = not applicable in that session (QWEN-3 cannot see the parents by design)",size=6.6,color=MUTED,xmax=.62)
    T(fig,.385,.155,wrap("tuple/list normalisation: JSON stores the locked seal's tuples as lists — every manifest read is converted to the exact seal_cp() form after a strict schema check",56,4),
      size=6.9,color=INK2,va="top",linespacing=1.15,xmax=.62)
    rows=rp["sha_simulations"];box(fig,.64,.10,.325,.76,ec=NEU,lw=1.3)
    T(fig,.65,.835,f"CPU simulations before the GPU — {sum(r['pass'] for r in rows)}/{len(rows)} as expected",size=9.0,weight="bold",xmax=.96)
    for j,r in enumerate(rows):
        y=.80-j*.043;T(fig,.65,y,r["id"],size=7.0,weight="bold",mono=True)
        T(fig,.675,y,short(r["scenario"],52),size=6.8,color=INK2,xmax=.905)
        T(fig,.91,y,("✓ " if r["pass"] else "✗ ")+r["observed"],size=6.9,weight="bold",color=OK_COL if r["pass"] else RED,xmax=.962)
    fig_footer(fig,k,"Simulations: PREFLIGHT process with the LOCKED seal_cp / safe_load / record_cp on small BF16 tensors (expected rejections count as PASS). Mandatory checks: PASS lines of QWEN-2 and QWEN-3.")
    return save_fig(fig,k,"VERIFICATION RECORD",["TEST782_PREFLIGHT_results.json sha_simulations","TEST782_QWEN2/QWEN3_results.json checks","manifests","POST_RUN_VERIFICATION.json"])
def _layout_text(fig,text,x0,x1,y0,y1,fs_max=9.6,fs_min=5.6,cols_allowed=(1,2)):
    """the verbatim text (line breaks kept, long lines wrapped) at the largest font that fits the area; returns overflow lines"""
    raw=str(text).replace("\t","    ").split("\n");Wpt=(x1-x0)*FW*72;Hpt=(y1-y0)*FH*72
    for fs in np.arange(fs_max,fs_min-1e-9,-0.2):
        for nc in cols_allowed:
            gap=.012;cw=((x1-x0)-gap*(nc-1))/nc;chars=max(20,int(cw*FW*72/(fs*0.56)));lines=[]
            for ln in raw:lines+=(textwrap.wrap(ln,chars,break_long_words=True,replace_whitespace=False,drop_whitespace=True) or [""])
            per=int(Hpt/(fs*1.13))
            if len(lines)<=per*nc:
                for c in range(nc):
                    chunk=lines[c*per:(c+1)*per]
                    if chunk:fig.text(x0+c*(cw+gap),y1,mt("\n".join(chunk)),fontsize=fs,va="top",ha="left",color=INK,linespacing=1.27/1.2,family="DejaVu Sans")
                return [],round(float(fs),1),nc
    fs=fs_min;nc=max(cols_allowed);gap=.012;cw=((x1-x0)-gap*(nc-1))/nc;chars=max(20,int(cw*FW*72/(fs*0.56)));lines=[]
    for ln in raw:lines+=(textwrap.wrap(ln,chars,break_long_words=True) or [""])
    per=int(Hpt/(fs*1.13))
    for c in range(nc):
        chunk=lines[c*per:(c+1)*per]
        if chunk:fig.text(x0+c*(cw+gap),y1,mt("\n".join(chunk)),fontsize=fs,va="top",ha="left",color=INK,linespacing=1.27/1.2)
    return lines[per*nc:],fs,nc
def fig7():
    k="F7";r3=results_of("QWEN3");a=next((x for x in (r3.get("answers") or []) if x["id"]=="Q0"),None)
    txt=text_file("QWEN3","QWEN3_EXPRESSION.txt") if a else None
    for kk in [x for x in FIGURES if x.startswith("F7_")]:FIGURES.pop(kk,None)
    if not a or txt is None:return fig_missing(k,"The expression is printed verbatim from QWEN-3's output file of this RUN.","QWEN-3 did not write its expression in this RUN.")
    mm=(LIVE.get("verification") or {}).get("master") or {};L3=LEDGER.get("QWEN3") or {};pr=r3.get("access_probe") or {}
    fig=fig_base(k,"Printed exactly as QWEN-3 wrote it (no edit, no shortening) — QWEN-3 had only MASTER_02: no source text, no source cartridge, no QWEN-2 output","SEALED MEMORY")
    q=a["question"];T(fig,.035,.862,"QUESTION Q0 (sealed before any model was loaded):",size=8.2,weight="bold",color=COL["Q3"])
    T(fig,.035,.832,wrap(q,190,2),size=7.6,color=INK2,va="center",linespacing=1.15,xmax=.965)
    box(fig,.035,.095,.655,.705,ec=COL["Q3"],lw=1.6);T(fig,.045,.782,f"ANSWER — QWEN-3 · {a['tokens']} tokens · verbatim",size=8.2,weight="bold",color=COL["Q3"],xmax=.68)
    rest,fs,nc=_layout_text(fig,txt,.045,.68,.105,.765)
    box(fig,.705,.095,.26,.705,ec=NEU,lw=1.3,fc=PANEL);T(fig,.715,.782,"EVIDENCE CHAIN",size=8.6,weight="bold",xmax=.96)
    ev=[("text SHA-256",[a["sha256"][:32],a["sha256"][32:]]),("MASTER_02 file SHA-256",[str(mm.get("sha256",""))[:32],str(mm.get("sha256",""))[32:]]),
        ("MASTER tensor seal (H3)",[str(mm.get("h3_seal",""))[:32],str(mm.get("h3_seal",""))[32:]]),
        ("parents (QWEN-1 files)",[f"SOURCE_A + SOURCE_B · links {okm(mm.get('parents_link_ok'))}"]),
        ("QWEN-3 process",[f"pid {L3.get('engine_pid','—')} · user {L3.get('engine_user','—')}",f"uid {L3.get('engine_uid','—')} · exit {L3.get('exit_code','—')}"]),
        ("reload parity in QWEN-3",[f"{(r3.get('master_parity') or {}).get('exact_layers','—')}/80 layers bit-identical"]),
        ("source folders → QWEN-3",[f"{k_}: {'no OS read' if not v_.get('os_read_permission') else 'OS readable'} · {v_.get('python_open','—').replace('BLOCKED_BY_','blocked by ').lower()}" for k_,v_ in pr.items()]),
        ("generation",[f"{a['seconds']} s · limit {a['limit']} · truncated {a['possible_truncation']}"]),
        ("model",[f"{MODEL_ID} NF4 frozen",f"sentinel {str(r3.get('weights_sentinel',''))[:16]}…"])]
    y=.75
    for h,ls in ev:
        T(fig,.715,y,h,size=7.2,weight="bold",color=MUTED,xmax=.96);y-=.023
        for l in ls:T(fig,.715,y,l,size=6.5,mono=True,xmax=.96);y-=.021
        y-=.012
    fig_footer(fig,k,f"Verbatim from q3_out/QWEN3_EXPRESSION.txt (SHA-256 above) · font {fs} pt · {nc} column(s)"+(" · continued on the next page" if rest else "")+" · correctness of the content is NOT graded here (human review PENDING).")
    recs=save_fig(fig,k,"SEALED MEMORY",["q3_out/QWEN3_EXPRESSION.txt","TEST782_QWEN3_results.json","POST_RUN_VERIFICATION.json"])
    page=2
    while rest:
        kk=f"F7_{page}";FIGURES[kk]=dict(n=7,title=f"QWEN-3 — The MASTER in Human Language (verbatim, page {page})",slug=f"QWEN3_EXPRESSION_VERBATIM_P{page}",tab="BLIND READING · QWEN-3")
        fg=fig_base(kk,"Continuation — printed exactly as QWEN-3 wrote it","SEALED MEMORY");box(fg,.035,.095,.93,.77,ec=COL["Q3"],lw=1.6)
        rest,fs2,nc2=_layout_text(fg,"\n".join(rest),.045,.955,.105,.85,fs_max=fs,fs_min=5.6,cols_allowed=(2,));fig_footer(fg,kk,f"page {page} of the verbatim QWEN-3 expression (SHA-256 of the full text: {a['sha256'][:24]}…)")
        FIG_FILES[kk]=save_fig(fg,kk,"SEALED MEMORY",["q3_out/QWEN3_EXPRESSION.txt"]);page+=1
    return recs
def fig8():
    k="F8";r3=results_of("QWEN3");ans=r3.get("answers") or []
    if len(ans)<2:return fig_missing(k,"The panel answers are QWEN-3's outputs of this RUN.","QWEN-3 did not answer the panel in this RUN.")
    fig=fig_base(k,"QWEN-3's answers to the sealed questions (quoted, shortened — full texts in the records) and where its attention falls inside MASTER_02","SEALED MEMORY")
    for j,a in enumerate([x for x in ans if x["id"]!="Q0"][:5]):
        y=.865-j*.152;box(fig,.035,y-.142,.53,.135,ec=COL["Q3"],lw=1.2)
        T(fig,.045,y-.018,f"{a['id']} · {a['kind'].replace('_',' ').lower()} · {a['tokens']} tokens · SHA {a['sha256'][:10]}…",size=7.8,weight="bold",color=COL["Q3"],xmax=.56)
        T(fig,.045,y-.04,"“"+wrap(" ".join(str(a["answer"]).split()),118,4)+"”",size=6.9,color=INK,va="top",linespacing=1.15,xmax=.56)
    at=r3.get("attention") or {}
    if at.get("status")=="MEASURED" and at.get("rows"):
        rows=at["rows"];lays=sorted({int(l) for r in rows for l in r["layers"]});M=np.zeros((len(rows),len(lays)));Aa=np.zeros_like(M);Bb=np.zeros_like(M)
        for i,r in enumerate(rows):
            for j,l in enumerate(lays):
                d=r["layers"].get(str(l)) or {};a_=float(d.get("B0_mass",0));b_=float(d.get("B1_mass",0));Aa[i,j]=a_;Bb[i,j]=b_;M[i,j]=b_/max(a_+b_,1e-12)
        ax=fig.add_axes([.62,.30,.30,.50]);im=ax.imshow(M,cmap="coolwarm",vmin=0,vmax=1,aspect="auto")
        ax.set_xticks(range(len(lays)));ax.set_xticklabels([f"L{l}" for l in lays]);ax.set_yticks(range(len(rows)));ax.set_yticklabels([r["id"] for r in rows])
        for i in range(len(rows)):
            for j in range(len(lays)):ax.text(j,i,f"A {100*Aa[i,j]:.0f}%\nB {100*Bb[i,j]:.0f}%",ha="center",va="center",fontsize=6.0,color="black")
        ax.set_title("attention of the last question token",fontsize=8.8);_axstyle(ax,7.5)
        cax=fig.add_axes([.93,.30,.010,.50]);cb=fig.colorbar(im,cax=cax);cb.set_ticks([0,.5,1]);cb.set_ticklabels(["A","½","B"]);cb.ax.tick_params(labelsize=7)
        T(fig,.62,.235,wrap("Share of the attention mass (all heads) on the MASTER rows of SOURCE_A vs SOURCE_B, layers 4/20/40/79 — the rest goes to prefix and question. Observational (TEST779 instrumentation): no output is changed.",64,4),
          size=6.9,color=INK2,va="top",linespacing=1.15,xmax=.965)
    else:
        box(fig,.62,.35,.345,.30,ec=AMBER,lw=1.2,ls="--");T(fig,.63,.62,"attention share NOT MEASURED in this RUN",size=8.6,weight="bold",color=AMBER,xmax=.96)
        T(fig,.63,.59,wrap(str(at.get("error") or at.get("status") or "—"),60,5),size=7.2,color=INK2,va="top",xmax=.96)
    fig_footer(fig,k,"Answers: q3_out/QWEN3_Q1…Q5.txt (unedited; quotes shortened with “…” only by line limits). Attention: TEST782_QWEN3_results.json attention (span B0 = SOURCE_A rows, B1 = SOURCE_B rows).")
    return save_fig(fig,k,"SEALED MEMORY",["q3_out/QWEN3_Q1–Q5.txt","TEST782_QWEN3_results.json"])
def fig9():
    k="F9";cm=LIVE.get("metrics")
    if not cm or not cm.get("rows"):return fig_missing(k,"The control comparison is computed from the CONTROLS and QWEN-3 answers of this RUN.","CONTROLS (or QWEN-3) did not complete in this RUN.")
    fig=fig_base(k,"Same sealed questions, four memories in a separate process + QWEN-3 — how much SOURCE_A- and SOURCE_B-specific vocabulary each answer carries","OBSERVATIONAL")
    conds=[c for c in ("NO_MEMORY","SOURCE_A_ONLY","SOURCE_B_ONLY","BASELINE_MASTER","QWEN3_BLIND") if c in cm["rows"]];qs=["Q0","Q1","Q2","Q3","Q4"]
    labels={"NO_MEMORY":"NO MEMORY","SOURCE_A_ONLY":"SOURCE_A only","SOURCE_B_ONLY":"SOURCE_B only","BASELINE_MASTER":"MASTER (controls)","QWEN3_BLIND":"MASTER (QWEN-3 blind)"}
    for j,(key,lab,cmap) in enumerate((("a","SOURCE_A-specific words found (count)","Blues"),("b","SOURCE_B-specific words found (count)","RdPu"))):
        M=np.array([[cm["rows"][c].get(q,{}).get(key+"_hits",0) for q in qs] for c in conds],float)
        ax=fig.add_axes([.14+j*.31,.32,.24,.48]);ax.imshow(M,cmap=cmap,aspect="auto",vmin=0,vmax=max(1,M.max()))
        ax.set_xticks(range(len(qs)));ax.set_xticklabels(qs);ax.set_yticks(range(len(conds)));ax.set_yticklabels([labels[c] for c in conds] if j==0 else [""]*len(conds))
        for i in range(len(conds)):
            for q in range(len(qs)):ax.text(q,i,f"{int(M[i,q])}",ha="center",va="center",fontsize=7.6,color="black" if M[i,q]<.6*max(1,M.max()) else "white")
        ax.set_title(lab,fontsize=8.6);_axstyle(ax,7.6)
    v=cm["vocabulary"];rep=cm.get("reproduction") or {}
    box(fig,.765,.32,.20,.48,ec=NEU,lw=1.3);T(fig,.775,.775,"absent topic (Q5)",size=8.8,weight="bold",xmax=.96)
    for i,c in enumerate(conds):
        d=cm["rows"][c].get("Q5",{});ok=d.get("unknown")
        T(fig,.775,.735-i*.05,labels[c],size=7.4,xmax=.90);T(fig,.957,.735-i*.05,"UNKNOWN ✓" if ok else "answered",size=7.4,weight="bold",color=OK_COL if ok else AMBER,ha="right")
    T(fig,.775,.45,"QWEN-3 Q0 = CONTROLS MASTER Q0",size=7.4,weight="bold",xmax=.96);T(fig,.775,.425,f"identical text: {okm(rep.get('qwen3_q0_equals_controls_master_q0'))} · similarity {rep.get('qwen3_vs_controls_master_similarity','—')}",size=7.2,color=INK2,xmax=.96)
    T(fig,.775,.39,"(two independent processes)",size=7.0,color=MUTED,xmax=.96)
    T(fig,.035,.25,f"vocabulary measured from the forged source bodies (outside QWEN-3): {v['a_specific']} words only in SOURCE_A · {v['b_specific']} only in SOURCE_B · {v['shared']} in both · {v['question_terms_excluded']} question words excluded",size=7.8,color=INK2,xmax=.965)
    T(fig,.035,.215,"Expected if the memory is causal: NO MEMORY ≈ 0 · A-only high A / low B · B-only high B / low A · MASTER both. General model knowledge shows up in NO MEMORY.",size=7.8,color=INK2,xmax=.965)
    T(fig,.035,.18,"This is a lexical trace of the documents in the answers — not a grade of correctness, relations or fabrication (human review PENDING).",size=7.8,color=AMBER,xmax=.965)
    fig_footer(fig,k,"Answers: controls/<ARM>_Q*.txt and q3_out/QWEN3_*.txt · counts: CONTROL_METRICS.json (host, after all sessions; source texts read only by the host and QWEN-1).")
    return save_fig(fig,k,"OBSERVATIONAL",["CONTROL_METRICS.json","controls/*.txt","q3_out/*.txt","q1_sources/*_BODY_FORGED.txt (host only)"])
_AKB782_PARTS.add(3)
# ===== END OF PART 3/4 =====
