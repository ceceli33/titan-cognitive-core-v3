# ===== PART 3/4 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 4 — the twelve scientific figures (1–9 here, 10–12 in PART 4). Each is drawn only from THIS run's engine
#              records, the live engine output and the host's read-only verification; a missing record is drawn as missing.
# THIS PART  39,401 characters · its last line is  # ===== END OF PART 3/4 =====
# =====================================================================================================================
if not {1,2}<=globals().get("_AKB815_PARTS",set()):raise RuntimeError("PART "+str(sorted({1,2}-globals().get("_AKB815_PARTS",set())))+" of the program is missing above this part in the cell — paste PART 1, 2, 3 and 4 one below the other, each completely (every part ends with an END OF PART line)")
def L_(c):return {"PMC9521804":"A","PMC9401135":"B"}.get(c,"S")
def ids_lab(ids):return "+".join(L_(c) if is_real(c) else c for c in ids)
def evidence_classes():
    """source-removal trials grouped by what the engine's own offline label says is left in the bank"""
    out=OrderedDict(none_left=[],other_left=[],irrelevant=[])
    for a in ablation():
        rel=set(relevant(a["case_id"]));rem=a.get("removed")
        if rem in rel:(out["other_left"] if rel-{rem} else out["none_left"]).append(a)
        else:out["irrelevant"].append(a)
    return out
def _n_ab(L):return sum(1 for a in L if a.get("native_action")=="ABSTAIN")
def _layout_text(fig,text,x0,x1,y0,y1,fs_max=9.6,fs_min=5.6,color=INK):
    """verbatim text, wrapped, at the largest font that fits the area (never cut silently: an overflow is marked …)"""
    raw=str(text or "").replace("\t","    ").split("\n");Hpt=(y1-y0)*FH*72
    for fs in np.arange(fs_max,fs_min-1e-9,-0.2):
        chars=max(20,int((x1-x0)*FW*72/(fs*0.60)));lines=[]
        for ln in raw:lines+=(textwrap.wrap(ln,chars,break_long_words=True) or [""])
        if len(lines)<=int(Hpt/(fs*1.36)):
            fig.text(x0,y1,mt("\n".join(lines)),fontsize=fs,va="top",ha="left",color=color,linespacing=1.3,family="DejaVu Sans");return float(fs)
    per=max(1,int(Hpt/(fs_min*1.36)));lines[per-1]=lines[per-1][:-2]+" …"
    fig.text(x0,y1,mt("\n".join(lines[:per])),fontsize=fs_min,va="top",ha="left",color=color,linespacing=1.3,family="DejaVu Sans");return fs_min

def fig1():
    k="F1";sm=summary();ac=acceptance();rp=rp_summary()
    if not sm or not ac:return fig_missing(k,"The overview is drawn from the engine's final summary and acceptance record of this RUN.","The engine did not complete in this RUN (no TEST815_COMPLETED / demo_acceptance record).")
    fig=fig_base(k,"One frozen 72B model · memory kept outside the weights as its own sealed internal states on the SSD · a controller that decides what to read next · every number from THIS run","ENGINE RECORD")
    ar,fr=sm.get("adaptive_native_reads"),sm.get("fixed_native_reads");ev=evidence_classes()
    sav=f"−{100*(1-ar/fr):.0f} % reads" if ar and fr else "—";nl=ev["none_left"];ir=ev["irrelevant"]
    tiles=[(f"{sm.get('source_count','—')}","physical cartridges",f"{ac.get('real_sources')} real articles + {ac.get('synthetic_controls')} decoys",COL["A"]),
           (f"{sm.get('routing_top2_relevant')}/{sm.get('cases')}","right article in top-2","no labels · no titles · no text",OK_COL),
           (f"{sm.get('decoy_selected_cases')}/{sm.get('cases')}","questions with a decoy in top-2","20 synthetic controls in the bank",OK_COL),
           (f"{ar} vs {fr}","native reads, 16 questions",f"adaptive vs fixed · {sav}",COL["LOOP"]),
           (f"{sm.get('unknown_recovery_observed')}","recoveries from UNKNOWN","the loop read the alternate",COL["GOLD"]),
           (f"{_n_ab(nl)}/{len(nl)}","abstained when evidence gone","no relevant article left",COL["B"]),
           (f"{len(ir)-_n_ab(ir)}/{len(ir)}","still answered","an irrelevant article removed",OK_COL),
           (f"{rp.get('initial_answer_exact','—')}/{rp.get('cases','—')}","identical replay","ranking + first answer",OK_COL)]
    W=(.93-7*.008)/8
    for i,(v,l,s,c) in enumerate(tiles):kpi(fig,.035+i*(W+.008),.70,W,.165,v,l,c,s)
    st=[("SOURCES",COL["A"],["Europe PMC · 2 PLOS articles","DOI + title locked, SHA-256",f"{sum(int((documents().get(c) or {}).get('physical_text_tokens') or 0) for c in REAL_IDS) or '—'} tokens kept"]),
        ("FORGE · frozen 72B",COL["HOST"],["each text read once","layer-3 states H3 + K/V L0–3","no training · no fine-tuning"]),
        ("SSD MEMORY BANK",COL["A"],[f"{len(manifest().get('cartridges') or {})} sealed .pt files","SHA-256 at commit and reload",f"host re-hash {sum(1 for r in ((LIVE.get('verification') or {}).get('cartridges') or {}).values() if r.get('file_sha_ok'))}/22"]),
        ("NATIVE H3 ROUTER",OK_COL,["the question's own H3 states","scored against all 22","top-2 handed to the loop"]),
        ("CLOSED LOOP",COL["LOOP"],["read → challenge → reverse","stops when evidence agrees",f"{ar} reads for 16 questions"]),
        ("DECISION",COL["B"],[f"ANSWER {sm.get('adaptive_answers','—')} · ABSTAIN {16-int(sm.get('adaptive_answers') or 0)}","UNKNOWN if unsupported","verbatim → Figure 7"])]
    BW=.142;G=(.93-6*BW)/5
    for i,(t,c,ls) in enumerate(st):
        x=.035+i*(BW+G);box(fig,x,.395,BW,.235,ec=c,lw=1.6);rect(fig,x,.595,BW,.035,c,z=2)
        Tc(fig,x+.004,x+BW-.004,.6125,t,size=9.2,weight="bold",color="white")
        for j,l in enumerate(ls):Tc(fig,x+.006,x+BW-.006,.555-j*.048,l,size=8.0,color=INK)
        if i<5:arrow(fig,x+BW+.002,.51,x+BW+G-.002,.51,col=NEU,lw=1.5,ms=11)
    x5=.035+5*(BW+G);x4=.035+4*(BW+G)
    arrow(fig,x5+BW*.5,.395,x4+BW*.5,.395,col=COL["LOOP"],lw=1.5,ms=11,cs="arc3,rad=-0.3",ls="--")
    Tc(fig,x4+BW*.2,x5+BW*.8,.33,"UNKNOWN or disagreement → read more",size=7.6,color=COL["LOOP"],weight="bold")
    ex=[("Memory that is not text",COL["A"],"The articles live as the model's own internal states — layer-3 hidden states and the K/V of layers 0–3 (CUT3). At question time they are fused back natively and layers 4–79 recompute everything. No article text enters the prompt."),
        ("A blind choice among decoys",OK_COL,f"Each question is turned into its own layer-3 states and compared with all 22 cartridges — no titles, no labels. 20 synthetic decoys sit in the same bank; one reached the top-2 in {sm.get('decoy_selected_cases')} of {sm.get('cases')} questions."),
        ("Evidence-sensitive control",COL["LOOP"],f"The loop reads, challenges the first answer with a second source and checks the order. Remove the right article and it says UNKNOWN instead of inventing: {_n_ab(nl)}/{len(nl)} when no relevant article was left.")]
    for i,(t,c,s) in enumerate(ex):
        x=.035+i*.314;box(fig,x,.105,.302,.205,ec=c,fc=PANEL,lw=1.2);T(fig,x+.01,.285,t,size=9.6,weight="bold",color=c,xmax=x+.295)
        _layout_text(fig,s,x+.01,x+.292,.115,.268,fs_max=10.2,fs_min=6.4)
    fig_footer(fig,k,f"Engine verdict: {ac.get('verdict','—')} · next stage: independent human scientific review (CSV exported) · cross-run / cross-GPU reproducibility · larger banks. Values: TEST815_results.json (summary, demo_acceptance).")
    return save_fig(fig,k,"ENGINE RECORD",["TEST815_results.json summary / demo_acceptance / source_removal_ablation","TEST815_manifest.json","POST_RUN_VERIFICATION.json"])

def fig2():
    k="F2";E=manifest().get("cartridges") or {};V=(LIVE.get("verification") or {}).get("cartridges") or {};A=LIVE.get("anatomy")
    if not E:return fig_missing(k,"The bank is drawn from the engine's cartridge manifest of this RUN.","No TEST815_manifest.json was written in this RUN.")
    fig=fig_base(k,"Two real articles and twenty synthetic decoys — each a sealed file of the frozen model's own layer-3 states · re-hashed and re-opened by this program after the run","SEALED MEMORY")
    ids=sorted(E,key=ckey);real=[c for c in ids if is_real(c)];syn=[c for c in ids if not is_real(c)]
    T(fig,.035,.862,"the bank — one tile = one .pt file on the SSD",size=9.4,weight="bold")
    for i,c in enumerate(real):
        e=E[c];v=V.get(c) or {};x=.035+i*.205;col=ccol(c);box(fig,x,.655,.197,.185,ec=col,lw=1.8);rect(fig,x,.808,.197,.032,col,z=2)
        Tc(fig,x+.004,x+.193,.824,f"{c} · {cshort(c)}",size=8.6,weight="bold",color="white")
        ls=[wrap(REAL[c]["title"],44,2),f"{e.get('body_tokens')} body tokens · n = {e.get('n')} · P = {e.get('p')}",f"file {fmt_b(v.get('bytes'))} · SHA {k_sha(e.get('sha256'),10)}",
            f"re-hash {okm(v.get('file_sha_ok'))} · reopen {okm(v.get('book_id_ok'))} · H3 {('×'.join(str(x_) for x_ in (v.get('h_shape') or [])) or '—')}"]
        T(fig,x+.008,.773,ls[0],size=7.2,color=INK,va="center",xmax=x+.19,linespacing=1.05)
        for j,l in enumerate(ls[1:]):T(fig,x+.008,.728-j*.026,l,size=7.0,color=INK2,mono=(j==1),xmax=x+.19)
    T(fig,.035,.625,f"{len(syn)} synthetic decoys (role {(E[syn[0]].get('role') if syn else '—')}) — same format, same SSD, same router",size=7.8,color=MUTED,xmax=.44)
    for i,c in enumerate(syn):
        e=E[c];v=V.get(c) or {};r_,q=divmod(i,5);x=.035+q*.0812;y=.515-r_*.098
        box(fig,x,y,.0772,.088,ec=COL["SYN"],lw=1.1);Tc(fig,x+.003,x+.074,y+.064,c,size=7.6,weight="bold",color=INK2)
        Tc(fig,x+.003,x+.074,y+.040,f"{e.get('body_tokens')} tokens",size=6.8,color=INK2);Tc(fig,x+.003,x+.074,y+.017,f"SHA {okm(v.get('file_sha_ok'))}  open {okm(v.get('book_id_ok'))}",size=6.6,color=OK_COL if v.get("file_sha_ok") else MUTED)
    if A:
        ids2=A["ids"];C=A["cos"];ax=fig.add_axes([.505,.355,.225,.47])
        im=ax.imshow(C,cmap="viridis",vmin=max(-1.0,float(np.nanmin(C))),vmax=1.0,interpolation="nearest")
        ax.set_xticks(range(len(ids2)));ax.set_yticks(range(len(ids2)));ax.set_xticklabels([L_(c) if is_real(c) else c.replace("_","") for c in ids2],rotation=90,fontsize=5.6)
        ax.set_yticklabels([L_(c) if is_real(c) else c.replace("_","") for c in ids2],fontsize=5.6)
        for tl in list(ax.get_xticklabels())+list(ax.get_yticklabels()):
            t=tl.get_text()
            if t in("A","B"):tl.set_color(COL["A"] if t=="A" else COL["B"]);tl.set_fontweight("bold")
        ax.set_title("H3 fingerprint similarity (centred cosine)",fontsize=8.4)
        cb=fig.add_axes([.735,.355,.007,.47]);fig.colorbar(im,cax=cb);cb.tick_params(labelsize=6.2)
        iR=[ids2.index(c) for c in real if c in ids2];iS=[ids2.index(c) for c in syn if c in ids2]
        rr=float(C[iR[0],iR[1]]) if len(iR)==2 else None;rs=float(np.mean([C[i,j] for i in iR for j in iS])) if iR and iS else None
        ss=float(np.mean([C[i,j] for i in iS for j in iS if i!=j])) if len(iS)>1 else None
        hs=(LIVE.get("verification") or {}).get("host_statistics") or {}
        box(fig,.775,.355,.19,.47,ec=NEU,fc=PANEL,lw=1.1);T(fig,.785,.80,"what the map shows",size=9.0,weight="bold",xmax=.96)
        for j,t in enumerate([f"article A ↔ article B   {rr:.3f}" if rr is not None else "A ↔ B —",f"article ↔ decoy (mean) {rs:.3f}" if rs is not None else "—",
                              f"decoy ↔ decoy (mean)   {ss:.3f}" if ss is not None else "—"]):T(fig,.785,.765-j*.03,t,size=7.6,mono=True,color=INK,xmax=.96)
        _layout_text(fig,"Each cartridge is reduced to one direction: the mean of its stored layer-3 states, centred on the bank average. Bright off-diagonal cells mark cartridges whose stored states point in a similar direction. This is a descriptive host statistic computed after the run — the engine's router scores every question token against 96 sampled states of each cartridge instead (Figure 3).",
                     .785,.958,.37,.665,fs_max=7.8,fs_min=6.0,color=INK2)
        for i,c in enumerate([c for c in real if c in A["strips"]]):
            S=A["strips"][c];ax2=fig.add_axes([.505+i*.235,.115,.215,.165])
            ax2.imshow(S,aspect="auto",origin="lower",cmap="magma",interpolation="nearest",vmin=float(np.percentile(S,2)),vmax=float(np.percentile(S,99.5)))
            ax2.set_title(f"{L_(c)} · {cshort(c)} — stored |H3|",fontsize=7.6,color=ccol(c));ax2.set_xticks([]);ax2.set_yticks([]);ax2.set_ylabel("64 channel bins",fontsize=6.6)
            ax2.set_xlabel(f"{E[c].get('body_tokens')} body tokens →",fontsize=6.8)
    else:
        box(fig,.505,.12,.46,.70,ec=AMBER,lw=1.4,ls="--");T(fig,.735,.47,wrap("Host statistics of the cartridge tensors are not available in this RUN (the files could not be re-opened by the host — see VERIFY).",60),size=10,color=AMBER,ha="center")
    fig_footer(fig,k,"Tiles: TEST815_manifest.json + host re-hash/re-open (POST_RUN_VERIFICATION.json). Map and strips: CARTRIDGE_ANATOMY.npz, computed read-only on the CPU from the sealed .pt files after the engine exited.")
    return save_fig(fig,k,"SEALED MEMORY",["TEST815_manifest.json","physical_cartridges/*.pt (read-only)","POST_RUN_VERIFICATION.json","CARTRIDGE_ANATOMY.npz"])

def fig3():
    k="F3";M,ids=score_matrix()
    if M is None or np.all(np.isnan(M)):return fig_missing(k,"The routing map is drawn from the engine's 22-cartridge H3 scores of this RUN.","No TEST815_ROUTE_PARAPHRASE record was written in this RUN.")
    sm=summary();fig=fig_base(k,"Each row: one question turned into its own layer-3 states and scored against all 22 cartridges by the engine — no titles, labels or text · row-normalised so the winner stands out","LIVE MEASUREMENT")
    mu=np.nanmean(M,1,keepdims=True);sd=np.nanstd(M,1,keepdims=True)+1e-12;Z=(M-mu)/sd
    ax=fig.add_axes([.105,.165,.49,.665]);im=ax.imshow(Z,aspect="auto",cmap="RdBu_r",vmin=-3.6,vmax=3.6,interpolation="nearest")
    ax.set_yticks(range(len(CASES)));ax.set_yticklabels([c.replace("_PARA"," para") for c in CASES],fontsize=7.2)
    ax.set_xticks(range(len(ids)));ax.set_xticklabels([f"{L_(c)} ·{c[-4:]}" if is_real(c) else c for c in ids],rotation=90,fontsize=6.0)
    for tl,c in zip(ax.get_xticklabels(),ids):
        if is_real(c):tl.set_color(ccol(c));tl.set_fontweight("bold")
    ax.axhline(7.5,color=INK,lw=1.2)
    for i,c in enumerate(CASES):
        row_=M[i];
        if np.all(np.isnan(row_)):continue
        r=row(c);order=(r.get("adaptive") or {}).get("ranked_22") if r else None
        order=order or [ids[j] for j in np.argsort(-np.nan_to_num(row_,nan=-9))]
        for rk,cid in enumerate(order[:2]):
            if cid in ids:ax.text(ids.index(cid),i,str(rk+1),ha="center",va="center",fontsize=7.4,weight="bold",color="white" if Z[i,ids.index(cid)]>1.8 else INK)
        for cid in relevant(c):
            if cid in ids:ax.add_patch(Rectangle((ids.index(cid)-.38,i-.38),.76,.76,fill=False,ec=INK,lw=1.6))
    ax.set_title("1 / 2 = engine's rank · black frame = article the offline key marks relevant (never shown to the model)",fontsize=8.0)
    cb=fig.add_axes([.60,.165,.007,.665]);fig.colorbar(im,cax=cb);cb.tick_params(labelsize=6.4);cb.set_ylabel("score − row mean (row SD)",fontsize=7.0)
    ax2=fig.add_axes([.70,.165,.17,.665]);mg=[];cl=[]
    for i,c in enumerate(CASES):
        rel=[ids.index(x) for x in relevant(c) if x in ids];dec=[j for j,x in enumerate(ids) if not is_real(x)]
        v=(np.nanmax(M[i,rel])-np.nanmax(M[i,dec])) if rel and dec and not np.all(np.isnan(M[i])) else np.nan;mg.append(v);cl.append(OK_COL if (v==v and v>0) else RED)
    y=np.arange(len(CASES));ax2.barh(y,[0 if v!=v else v for v in mg],color=cl,height=.62);ax2.set_ylim(len(CASES)-.5,-.5);ax2.set_yticks(y);ax2.set_yticklabels([])
    for yi,v in zip(y,mg):
        if v==v:ax2.text(v,yi,f" +{v:.3f}" if v>0 else f" {v:.3f}",va="center",fontsize=6.6)
    ax2.axvline(0,color=NEU,lw=.8);ax2.set_xlim(min(0,np.nanmin(mg) if np.any(np.isfinite(mg)) else 0)*1.3,(np.nanmax(mg) if np.any(np.isfinite(mg)) else .05)*1.45)
    ax2.set_title("relevant article − best decoy",fontsize=8.2);ax2.tick_params(labelsize=6.4);_axstyle(ax2,6.4)
    box(fig,.885,.165,.08,.665,ec=NEU,fc=PANEL,lw=1.0)
    for j,(v,l) in enumerate([(f"{sm.get('routing_top1_relevant','—')}/{sm.get('cases','—')}","top-1\nrelevant"),(f"{sm.get('routing_top2_relevant','—')}/{sm.get('cases','—')}","top-2\nrelevant"),
                              (f"{sm.get('decoy_selected_cases','—')}/{sm.get('cases','—')}","decoy in\ntop-2"),(f"{sum(1 for v in mg if v==v and v>0)}/{len(CASES)}","margin\n> 0")]):
        Tc(fig,.887,.963,.78-j*.16,v,size=13,weight="bold",color=OK_COL);Tc(fig,.887,.963,.725-j*.16,l,size=7.0,color=INK2,linespacing=1.1)
    fig_footer(fig,k,"Scores: TEST815_results.json routing_robustness (original_scores / paraphrase_scores) = the engine's locked TEST757 numeric_rank over all 22 cartridges; ranks: rows[*].adaptive.ranked_22; relevance key: offline_routing_eval (used only for evaluation).")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST815_results.json routing_robustness / rows","TEST815_ROUTE_PARAPHRASE lines"])

def fig4():
    k="F4";R=[r for r in routes() if r.get("original_scores")]
    if not R:return fig_missing(k,"The paraphrase control is drawn from the engine's routing records of this RUN.","No TEST815_ROUTE_PARAPHRASE record was written in this RUN.")
    fig=fig_base(k,"Each question was asked a second time in different words — the router saw only the model's own states of the new wording · margin = relevant article over the best decoy","LIVE MEASUREMENT")
    def marg(sc,case):
        rel=[sc[x] for x in relevant(case) if x in sc];dec=[v for c,v in sc.items() if not is_real(c)]
        return (max(rel)-max(dec)) if rel and dec else np.nan
    R=sorted(R,key=lambda r:BASE_Q.index(r["case_id"]) if r["case_id"] in BASE_Q else 99);Q=questions()
    ax=fig.add_axes([.075,.17,.30,.66]);y=np.arange(len(R))
    for i,r in enumerate(R):
        a=marg(r["original_scores"],r["case_id"]);b=marg(r.get("paraphrase_scores") or {},r["case_id"]+"_PARA")
        ax.plot([a,b],[i,i],color=RULE,lw=2.4,zorder=1);ax.scatter([a],[i],s=46,color=COL["A"],zorder=2);ax.scatter([b],[i],s=46,marker="D",color=COL["LOOP"],zorder=2)
    ax.axvline(0,color=RED,lw=1.0,ls="--");ax.set_yticks(y);ax.set_yticklabels([r["case_id"] for r in R],fontsize=8);ax.set_ylim(len(R)-.5,-.5)
    ax.set_xlabel("H3 score margin over the best decoy",fontsize=8);ax.set_title("● original   ◆ paraphrase   (right of the red line = article beats every decoy)",fontsize=7.8);_axstyle(ax,7.2)
    xs=[.40,.445,.765,.865,.925];hd=["","question (top) · paraphrase (bottom)","top-1: orig → para","top-2 relevant","same top-1"]
    for x,h,nx in zip(xs,hd,xs[1:]+[.965]):T(fig,x,.855,h,size=7.6,weight="bold",color=MUTED,xmax=nx-.006)
    hline(fig,.40,.965,.838,RULE)
    y0=.83;dy=.66/len(R);rl={r["case_id"]:r for r in rows()};rlog=row_logs()
    for i,r in enumerate(R):
        yc=y0-(i+.5)*dy;c=r["case_id"];T(fig,.40,yc,c,size=8.4,weight="bold")
        T(fig,.445,yc+dy*.2,short(Q.get(c) or "",80),size=6.9,color=INK,xmax=.755,minsize=6.4);T(fig,.445,yc-dy*.2,short(Q.get(c+"_PARA") or "",80),size=6.9,color=COL["LOOP"],xmax=.755,minsize=6.4)
        o,p=r.get("original_top1"),r.get("paraphrase_top1");T(fig,.765,yc,f"{L_(o) if is_real(o) else o} → {L_(p) if is_real(p) else p}",size=8.4,weight="bold",color=INK)
        t2=[((rl.get(x) or rlog.get(x) or {}).get("offline_routing_eval") or {}).get("top2_relevant") for x in (c,c+"_PARA")]
        T(fig,.87,yc,f"{okm(t2[0])} / {okm(t2[1])}",size=9,weight="bold",color=OK_COL if all(t2) else AMBER)
        T(fig,.94,yc,okm(r.get("same_top1")),size=10,weight="bold",color=OK_COL if r.get("same_top1") else AMBER)
        if i<len(R)-1:hline(fig,.40,.965,yc-dy/2,"#EEF0F3",.6)
    same=sum(1 for r in R if r.get("same_top1"));t2a=sum(1 for c in CASES if ((rl.get(c) or rlog.get(c) or {}).get("offline_routing_eval") or {}).get("top2_relevant"))
    pos=sum(1 for r in R for x,c in ((r["original_scores"],r["case_id"]),(r.get("paraphrase_scores") or {},r["case_id"]+"_PARA")) if marg(x,c)>0)
    box(fig,.40,.095,.565,.05,ec=OK_COL,fc=PANEL,lw=1.1)
    Tc(fig,.405,.96,.12,f"relevant article in top-2: {t2a}/16 wordings · beats every decoy: {pos}/16 · same top-1 article: {same}/8 — A and B score close, so the loop reads both (Figure 5)",size=8.2,weight="bold",color=INK)
    fig_footer(fig,k,"A = PMC9521804 (credit for data) · B = PMC9401135 (data availability). Records: routing_robustness (scores, top-1, same_top1) and rows[*].offline_routing_eval (top-2 relevance, offline key).")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST815_results.json routing_robustness","rows[*].offline_routing_eval"])

def fig5():
    k="F5";TA=tracks("ADAPTIVE");TF=tracks("FIXED")
    if not TA:return fig_missing(k,"The decision map is drawn from the native reads of this RUN (results steps or NATIVE_FUSION_STEP lines).","No closed-loop case was run in this RUN.")
    fig=fig_base(k,"16 questions · each cell = one native read of physical memory (A, B = the two articles; A+B = fused, first one first) · the adaptive loop stops as soon as the evidence agrees","ENGINE RECORD")
    cx=[.035,.10,.355,.45,.635];T(fig,.10,.858,"ADAPTIVE closed loop — reads in order",size=8.6,weight="bold",color=COL["LOOP"]);T(fig,.355,.858,"outcome",size=8.2,weight="bold",color=MUTED)
    T(fig,.45,.858,"FIXED policy — always 4 reads",size=8.6,weight="bold",color=COL["FIX"]);T(fig,.635,.858,"outcome",size=8.2,weight="bold",color=MUTED)
    dy=.0405;y0=.815;sw=.0615;fw=.0425
    for i,c in enumerate(CASES):
        y=y0-i*dy;r=row(c) or {};ad=r.get("adaptive") or {};fx=r.get("fixed") or {};lg=row_logs().get(c) or {}
        if i==8:hline(fig,.035,.69,y+dy*.5+.001,INK2,.9)
        T(fig,.035,y,c.replace("_PARA"," para"),size=8.0,weight="bold",color=INK)
        for j,s in enumerate(TA.get(c,[])[:4]):
            x=.10+j*(sw+.003);rect(fig,x,y-.016,sw,.032,opcol(s["op"]),z=2);Tc(fig,x+.002,x+sw-.002,y,ids_lab(s["ids"]),size=7.4,weight="bold",color="white")
        act=ad.get("action") or lg.get("adaptive_action");flag="recovered" if ad.get("recovered_from_unknown") else ("revised" if (ad.get("revision") if ad else lg.get("adaptive_revision")) else "")
        pill(fig,.355,y-.014,.042,.028,act or "—",OK_COL if act=="ANSWER" else (RED if act else MUTED),size=6.6);T(fig,.401,y,flag,size=6.8,color=COL["GOLD"] if flag=="recovered" else MUTED)
        for j,s in enumerate(TF.get(c,[])[:4]):
            x=.45+j*(fw+.0025);rect(fig,x,y-.016,fw,.032,opcol(s["op"]),z=2);Tc(fig,x+.002,x+fw-.002,y,ids_lab(s["ids"]),size=6.8,weight="bold",color="white")
        fa=fx.get("action") or lg.get("fixed_action");pill(fig,.635,y-.014,.042,.028,fa or "—",OK_COL if fa=="ANSWER" else (RED if fa else MUTED),size=6.6)
    fx0=.715;fw_=.232;bw=[("① read the top-1 cartridge",.80,COL["A"]),("usable? — a complete sentence, not UNKNOWN",.715,NEU)]
    for t,y,c in bw:box(fig,fx0,y-.026,fw_,.052,ec=c,lw=1.3);Tc(fig,fx0+.005,fx0+fw_-.005,y,t,size=7.8,color=INK)
    arrow(fig,fx0+fw_/2,.774,fx0+fw_/2,.741,ms=9)
    box(fig,fx0,.575,.11,.085,ec=opcol("FUSE_TO_CHALLENGE_INITIAL"),lw=1.4);Tc(fig,fx0+.004,fx0+.106,.632,"yes → ② CHALLENGE",size=7.6,weight="bold",color=opcol("FUSE_TO_CHALLENGE_INITIAL"));Tc(fig,fx0+.004,fx0+.106,.598,"fuse top-1 + top-2",size=7.2)
    box(fig,fx0+.122,.575,.11,.085,ec=opcol("ALTERNATE_AFTER_UNKNOWN"),lw=1.4);Tc(fig,fx0+.126,fx0+.228,.632,"no → ② ALTERNATE",size=7.6,weight="bold",color=opcol("ALTERNATE_AFTER_UNKNOWN"));Tc(fig,fx0+.126,fx0+.228,.598,"then ③ fuse it first",size=7.2)
    arrow(fig,fx0+.07,.689,fx0+.055,.662,ms=9);arrow(fig,fx0+.165,.689,fx0+.177,.662,ms=9)
    box(fig,fx0,.465,fw_,.06,ec=NEU,lw=1.3);Tc(fig,fx0+.005,fx0+fw_-.005,.505,"evidence agrees? (overlap ≥ 0.25,",size=7.6);Tc(fig,fx0+.005,fx0+fw_-.005,.481,"no conflicting % values)",size=7.6)
    arrow(fig,fx0+.055,.575,fx0+.085,.527,ms=9);arrow(fig,fx0+.177,.575,fx0+.147,.527,ms=9)
    box(fig,fx0,.36,fw_,.06,ec=opcol("REVERSE_EVIDENCE_CHECK"),lw=1.4);Tc(fig,fx0+.005,fx0+fw_-.005,.40,"no → ④ REVERSE-order check",size=7.6,weight="bold",color=opcol("REVERSE_EVIDENCE_CHECK"));Tc(fig,fx0+.005,fx0+fw_-.005,.376,"(or alternate check)",size=7.2)
    arrow(fig,fx0+fw_/2,.465,fx0+fw_/2,.422,ms=9)
    box(fig,fx0,.255,fw_,.06,ec=COL["B"],lw=1.4);Tc(fig,fx0+.005,fx0+fw_-.005,.295,"DECIDE: ANSWER — or ABSTAIN",size=7.8,weight="bold",color=COL["B"]);Tc(fig,fx0+.005,fx0+fw_-.005,.271,"at most 4 reads · no gold, no oracle",size=7.2)
    arrow(fig,fx0+fw_/2,.36,fx0+fw_/2,.317,ms=9)
    fig.add_artist(Line2D([fx0+fw_,.958,.958],[.495,.495,.285],transform=fig.transFigure,color=OK_COL,lw=1.3));arrow(fig,.958,.285,fx0+fw_+.001,.285,col=OK_COL,ms=9);T(fig,.952,.44,"yes",size=7.0,color=OK_COL,ha="right")
    pc=policy();sm=summary()
    lines=[f"adaptive reads {pc.get('adaptive_reads','—')} · fixed {pc.get('fixed_reads','—')} · decisions changed {pc.get('changed_decisions','—')}/16",
           f"recoveries from UNKNOWN {pc.get('adaptive_recoveries','—')} · revisions {pc.get('adaptive_revisions','—')}",f"read counts differ in {pc.get('different_read_counts','—')}/16 cases"]
    for j,t in enumerate(lines):T(fig,fx0,.215-j*.026,t,size=7.4,color=INK2,xmax=.965)
    used=[o for o in OPS if any(s["op"]==o for T_ in (TA,TF) for v in T_.values() for s in v)]
    xx=.035
    for o in used:
        rect(fig,xx,.112,.012,.016,opcol(o),z=2);t=T(fig,xx+.016,.12,oplab(o),size=7.0,color=INK2);xx=_bb(fig,t).x1+.014
    fig_footer(fig,k,"Order and sources of every read: rows[*].adaptive/fixed.steps (operation, ids) of TEST815_results.json — the same sequence appears live as NATIVE_FUSION_STEP lines. Rules: decide815 in 815.py (unchanged).")
    return save_fig(fig,k,"ENGINE RECORD",["TEST815_results.json rows[*].steps / trace","NATIVE_FUSION_STEP lines","815.py decide815 (rules)"])

def fig6():
    k="F6";TA=tracks("ADAPTIVE");TF=tracks("FIXED");cm=cost()
    if not TA or not TF:return fig_missing(k,"The cost comparison is drawn from the native reads of both policies in this RUN.","The closed-loop cases did not run in this RUN.")
    fig=fig_base(k,"Both policies answer the same 16 questions from the same physical memory — the adaptive controller reads only what it needs · wall time of every native read measured by the engine","LIVE MEASUREMENT")
    ax=fig.add_axes([.06,.20,.49,.62]);x=np.arange(len(CASES));a=[len(TA.get(c,[])) for c in CASES];f=[len(TF.get(c,[])) for c in CASES]
    ax.bar(x-.2,a,.38,color=COL["LOOP"],label="adaptive");ax.bar(x+.2,f,.38,color=COL["FIX"],alpha=.75,label="fixed")
    ax.set_xticks(x);ax.set_xticklabels([c.replace("_PARA","p") for c in CASES],fontsize=7,rotation=0);ax.set_ylim(0,4.9);ax.set_yticks([0,1,2,3,4]);ax.set_ylabel("native reads",fontsize=8)
    ax.legend(loc="upper left",ncol=2,fontsize=7.6);ax.set_title("reads per question (p = paraphrase)",fontsize=8.8);_axstyle(ax,7.2)
    for xi,v in zip(x,a):ax.text(xi-.2,v+.06,str(v),ha="center",fontsize=6.6,color=COL["LOOP"])
    ax2=fig.add_axes([.63,.55,.33,.27])
    for T_,c,lab in ((TA,COL["LOOP"],"adaptive"),(TF,COL["FIX"],"fixed")):
        s=[float(v["sec"] or 0) for cc in CASES for v in T_.get(cc,[])]
        if any(s):ax2.plot(np.arange(1,len(s)+1),np.cumsum(s)/60,color=c,lw=1.8,label=lab);ax2.text(len(s),np.sum(s)/60,f" {np.sum(s)/60:.1f} min",fontsize=7,va="center",color=c)
    ax2.set_xlabel("native reads in execution order",fontsize=7.6);ax2.set_ylabel("cumulative minutes",fontsize=7.6);ax2.set_title("cumulative read time",fontsize=8.6);_axstyle(ax2,6.8);ax2.legend(fontsize=7)
    A_=cm.get("adaptive") or {};F_=cm.get("fixed") or {}
    box(fig,.60,.10,.365,.37,ec=NEU,fc=PANEL,lw=1.1)
    hd=["","adaptive","fixed"];xs=[.61,.80,.885]
    for xx,h in zip(xs,hd):T(fig,xx,.445,h,size=8.0,weight="bold",color=MUTED)
    def pct(a_,b_):
        try:return f"  (−{100*(1-float(a_)/float(b_)):.0f} %)"
        except Exception:return ""
    rws=[("native reads",A_.get("native_reads"),F_.get("native_reads")),("read wall time (s)",A_.get("read_wall_seconds_sum"),F_.get("read_wall_seconds_sum")),
         ("mean s per read",A_.get("mean_read_seconds"),F_.get("mean_read_seconds")),("answers",A_.get("answers"),F_.get("answers")),("abstentions",A_.get("abstentions"),F_.get("abstentions")),
         ("hypothesis revisions",A_.get("revisions"),F_.get("revisions")),("relation audit pass",f"{A_.get('relation_audit_pass','—')}/{A_.get('relation_audit_total','—')}",f"{F_.get('relation_audit_pass','—')}/{F_.get('relation_audit_total','—')}")]
    for j,(l,u,v) in enumerate(rws):
        yy=.41-j*.037;T(fig,xs[0],yy,l,size=7.8,color=INK);T(fig,xs[1],yy,str(u if u is not None else "—"),size=7.8,mono=True,weight="bold",color=COL["LOOP"]);T(fig,xs[2],yy,str(v if v is not None else "—"),size=7.8,mono=True,color=COL["FIX"])
    T(fig,.61,.135,f"reads {pct(A_.get('native_reads'),F_.get('native_reads')).strip(' ()') or '—'} · read time {pct(A_.get('read_wall_seconds_sum'),F_.get('read_wall_seconds_sum')).strip(' ()') or '—'} · same decisions {16-int(policy().get('changed_decisions') or 0)}/16",size=7.8,weight="bold",color=OK_COL,xmax=.96)
    T(fig,.06,.115,"Pair reads fuse two cartridges (≈1,960 memory tokens) and take longer than single reads, so time falls a little less than the read count.",size=7.6,color=INK2,xmax=.58)
    fig_footer(fig,k,"Reads and seconds: rows[*].<policy>.steps[*].elapsed_seconds (per native read, model loading excluded) and cost_matrix of TEST815_results.json; the host re-adds them in POST_RUN_VERIFICATION.json.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST815_results.json rows[*].steps / cost_matrix / policy_comparison","POST_RUN_VERIFICATION.json consistency"])

def fig7():
    k="F7";rw=rows()
    if not rw:return fig_missing(k,"The verbatim hypotheses are taken from the engine's results file of this RUN.","No closed-loop result was written in this RUN.")
    fig=fig_base(k,"What the frozen model said after its first read of physical memory, and what the closed loop finally answered — printed verbatim, unedited","ENGINE RECORD")
    def ops(r):return [s.get("operation") for s in (r.get("adaptive") or {}).get("steps") or []]
    pick=[r for r in rw if (r.get("adaptive") or {}).get("recovered_from_unknown")]
    pick+=[r for r in rw if r not in pick and any(o in ("REVERSE_EVIDENCE_CHECK","ALTERNATE_EVIDENCE_CHECK") for o in ops(r))]
    pick+=[r for r in rw if r not in pick and r["case_id"] in ("Q2","Q3","Q7","Q4")]
    pick=pick[:4];hh=.79/max(1,len(pick))-.012
    for i,r in enumerate(pick):
        ad=r.get("adaptive") or {};st=ad.get("steps") or [];y1=.865-i*(hh+.012);y0=y1-hh
        fl="RECOVERED FROM UNKNOWN" if ad.get("recovered_from_unknown") else ("REVERSE CHECK" if "REVERSE_EVIDENCE_CHECK" in ops(r) else ("REVISED" if ad.get("revision") else "CONFIRMED"))
        fc={"RECOVERED FROM UNKNOWN":COL["GOLD"],"REVERSE CHECK":opcol("REVERSE_EVIDENCE_CHECK")}.get(fl,COL["LOOP"])
        box(fig,.035,y0,.93,hh,ec=fc,lw=1.3);T(fig,.045,y1-.022,f"{r['case_id']}",size=10,weight="bold",color=fc)
        T(fig,.105,y1-.022,short(r.get("question"),150),size=8.2,weight="bold",xmax=.955)
        pill(fig,.045,y1-.07,.11,.026,fl,fc,size=6.4)
        T(fig,.045,y1-.098,"path: "+" → ".join(ids_lab(s.get("ids") or []) for s in st),size=7.0,color=INK2,xmax=.16)
        T(fig,.045,y1-.12,f"{ad.get('read_count','—')} reads · {ad.get('action','—')}",size=7.0,color=INK2,xmax=.16)
        first=st[0] if st else {};last=st[-1] if st else {}
        T(fig,.17,y1-.05,f"first reading · {ids_lab(first.get('ids') or [])} · {first.get('tokens','—')} token(s)",size=7.4,weight="bold",color=COL["A"],xmax=.55)
        _layout_text(fig,first.get("raw") or "—",.17,.555,y0+.008,y1-.064,fs_max=10.6,fs_min=5.8,color=INK)
        arrow(fig,.562,y0+hh*.42,.588,y0+hh*.42,col=fc,lw=1.6,ms=11)
        T(fig,.595,y1-.05,f"final answer · {ad.get('action','—')} · {ids_lab(last.get('ids') or [])} · {last.get('tokens','—')} token(s)",size=7.4,weight="bold",color=OK_COL if ad.get("action")=="ANSWER" else RED,xmax=.955)
        _layout_text(fig,ad.get("answer") or "—",.595,.957,y0+.008,y1-.064,fs_max=10.6,fs_min=5.8,color=INK)
    fig_footer(fig,k,"Verbatim: rows[*].adaptive.steps[0].raw and rows[*].adaptive.answer (TEST815_results.json). Every answer of all 16 questions, both policies, is in the ANSWERS tab and in TEST815_independent_review.csv for human review.")
    return save_fig(fig,k,"ENGINE RECORD",["TEST815_results.json rows[*].adaptive (steps, answer, revision, recovered_from_unknown)"])
def fig8():
    k="F8";AB=ablation()
    if not AB:return fig_missing(k,"The evidence-removal matrix is drawn from the engine's source-removal trials of this RUN.","No TEST815_ABLATION record was written in this RUN.")
    fig=fig_base(k,"Each real article is removed from the bank in turn · the router must pick the best SURVIVING cartridge among 21 · the frozen model reads it natively — does it invent, or abstain?","LIVE MEASUREMENT")
    ev=evidence_classes();Q=questions();by={(a["case_id"],a["removed"]):a for a in AB}
    xs=[.035,.075,.395,.52,.645];T(fig,.075,.858,"question",size=8,weight="bold",color=MUTED)
    for x,h in zip(xs[2:],["both articles present","A removed (credit for data)","B removed (data availability)"]):Tc(fig,x,x+.118,.858,h,size=7.8,weight="bold",color=MUTED)
    dy=.073;y0=.81
    for i,q in enumerate(BASE_Q):
        y=y0-i*dy;rel=set(relevant(q));T(fig,.035,y,q,size=9,weight="bold");T(fig,.075,y+.008,wrap(Q.get(q),64,2),size=7.0,color=INK,xmax=.385,linespacing=1.15)
        T(fig,.075,y-.025,"relevant (offline key): "+", ".join(L_(c) for c in sorted(rel)),size=6.6,color=MUTED,xmax=.385)
        a0=next((a for a in AB if a["case_id"]==q),None);ba=(a0 or {}).get("baseline_action")
        rect(fig,.395,y-.026,.118,.052,"#DCFCE7" if ba=="ANSWER" else "#FEE2E2",z=1);Tc(fig,.397,.511,y+.008,ba or "—",size=8.4,weight="bold",color=OK_COL if ba=="ANSWER" else RED)
        Tc(fig,.397,.511,y-.014,f"reads {L_((a0 or {}).get('baseline_top1'))} first",size=6.6,color=INK2)
        for j,rem in enumerate(REAL_IDS):
            a=by.get((q,rem));x=xs[3+j]
            if not a:Tc(fig,x,x+.118,y,"—",size=8);continue
            act=a.get("native_action");rr=rem in rel;left=bool(rel-{rem})
            rect(fig,x,y-.026,.118,.052,"#DCFCE7" if act=="ANSWER" else "#FEE2E2",ec=(INK if rr and not left else ("#9CA3AF" if rr else "none")),lw=(1.8 if rr and not left else (1.0 if rr else 0)),z=1)
            Tc(fig,x+.002,x+.116,y+.008,act,size=8.4,weight="bold",color=OK_COL if act=="ANSWER" else RED)
            Tc(fig,x+.002,x+.116,y-.014,f"reads {L_(a.get('top1')) if is_real(a.get('top1')) else a.get('top1')} · "+("no relevant left" if rr and not left else ("other relevant left" if rr else "irrelevant removed")),size=6.2,color=INK2)
    nl,ol,ir=ev["none_left"],ev["other_left"],ev["irrelevant"];syn=sum(1 for a in AB if a.get("selected_synthetic"))
    box(fig,.78,.235,.185,.625,ec=NEU,fc=PANEL,lw=1.1)
    for j,(v,l,c) in enumerate([(f"{_n_ab(nl)}/{len(nl)}","abstained — no relevant\narticle left (black frame)",COL["B"]),(f"{len(ir)-_n_ab(ir)}/{len(ir)}","answered — the removed\narticle was irrelevant",OK_COL),
                                (f"{len(ol)-_n_ab(ol)}/{len(ol)}","answered — another relevant\narticle was still there",COL["LOOP"]),(f"{syn}/{len(AB)}","trials where a decoy was\nread instead",OK_COL)]):
        Tc(fig,.782,.963,.81-j*.15,v,size=17,weight="bold",color=c);Tc(fig,.782,.963,.755-j*.15,l,size=7.0,color=INK2,linespacing=1.1)
    q1=next((a for a in nl if a.get("native_action")=="ABSTAIN" and len(str(a.get("native_answer") or ""))>12),None) or next((a for a in nl if a.get("native_action")=="ABSTAIN"),None)
    q2=next((a for a in ir if a.get("native_action")=="ANSWER"),None)
    for j,(a,lab,c) in enumerate(((q1,"abstention, verbatim",COL["B"]),(q2,"answer from the surviving relevant article, verbatim",OK_COL))):
        x=.035+j*.375;box(fig,x,.095,.365,.125,ec=c,lw=1.2)
        if a:
            T(fig,x+.008,.205,f"{a['case_id']} · {L_(a['removed'])} removed · {lab}",size=7.6,weight="bold",color=c,xmax=x+.358)
            _layout_text(fig,a.get("native_answer"),x+.008,x+.357,.102,.19,fs_max=9.8,fs_min=5.8)
    fig_footer(fig,k,"Records: source_removal_ablation (top1 among 21, native_action, native_answer, removed_relevant_offline, selected_synthetic). The offline relevance key is used only to classify the trials — never by the model or the router.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST815_results.json source_removal_ablation","TEST815_ABLATION lines","rows[*].offline_routing_eval"])

def fig9():
    k="F9";rw=[r for r in rows() if ((r.get("offline_fact_audit") or {}).get("adaptive") or {}).get("status")=="NARROW_NUMERIC_FACT_CHECK"]
    if not rw:return fig_missing(k,"The numeric audit is drawn from the engine's offline fact audit of this RUN.","No audited case (Q2, Q8 and their paraphrases) was answered in this RUN.")
    fig=fig_base(k,"The empirical article reports 98 % (DOI links), 78 % (URL links) and 80 % (automatic retrieval) · after the run each final answer is checked for the numbers AND for the right number–term relation","ENGINE RECORD")
    RA=relation();rw=rw[:4]
    for i,r in enumerate(rw):
        cid=r["case_id"];ad=r.get("adaptive") or {};fa=(r.get("offline_fact_audit") or {}).get("adaptive") or {};ff=(r.get("offline_fact_audit") or {}).get("fixed") or {}
        ra=(RA.get(cid) or {}).get("adaptive") or {};rf=(RA.get(cid) or {}).get("fixed") or {}
        q,c_=divmod(i,2);x=.035+c_*.47;y1=.865-q*.385;y0=y1-.365;ok=bool(fa.get("passed")) and bool(ra.get("passed",True))
        box(fig,x,y0,.46,.365,ec=OK_COL if ok else RED,lw=1.5);T(fig,x+.01,y1-.022,cid,size=10.5,weight="bold",color=OK_COL if ok else RED)
        T(fig,x+.075,y1-.022,short(r.get("question"),95),size=7.8,weight="bold",xmax=x+.452)
        T(fig,x+.01,y1-.05,f"adaptive final answer · {ad.get('action','—')} · sources {ids_lab(ad.get('selected') or [])} — verbatim",size=7.2,color=INK2,xmax=x+.452)
        _layout_text(fig,ad.get("answer"),x+.01,x+.452,y0+.105,y1-.064,fs_max=12.0,fs_min=5.8)
        req=fa.get("required") or [];obs=set(fa.get("observed") or []);xx=x+.01
        T(fig,xx,y0+.082,"numbers:",size=7.4,weight="bold",color=INK2)
        xx=x+.075
        for p_ in req:pill(fig,xx,y0+.07,.05,.024,f"{p_} {okm(p_ in obs)}",OK_COL if p_ in obs else RED,size=7.0);xx+=.055
        rel=[(kk,v) for kk,v in ra.items() if kk not in ("status","passed")]
        T(fig,x+.01,y0+.045,"relations:",size=7.4,weight="bold",color=INK2);xx=x+.075
        lab={"doi_98":"98 % ↔ DOI","url_78":"78 % ↔ URL","automatic_80":"80 % ↔ automatic"}
        for kk,v in rel:pill(fig,xx,y0+.033,.085,.024,f"{lab.get(kk,kk)} {okm(v)}",OK_COL if v else RED,size=6.8);xx+=.09
        if not rel:T(fig,xx,y0+.045,f"relation audit: {ra.get('status','—')} · passed {okm(ra.get('passed'))}",size=7.2,color=INK2,xmax=x+.452)
        T(fig,x+.01,y0+.013,f"fixed policy: numbers {okm(ff.get('passed'))} · relations {okm(rf.get('passed'))} · first reading already had the numbers: {okm(fa.get('initial_passed'))}",size=7.0,color=MUTED,xmax=x+.452)
    fig_footer(fig,k,"offline_fact_audit and relation_audit of TEST815_results.json — computed after inference from a key the model never saw. Correct numbers without their DOI / URL / automatic relation do not pass. A narrow check, not a semantic grade.")
    return save_fig(fig,k,"ENGINE RECORD",["TEST815_results.json rows[*].offline_fact_audit / relation_audit"])

_AKB815_PARTS.add(3)
# ===== END OF PART 3/4 =====
