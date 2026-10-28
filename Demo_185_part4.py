# ===== PART 4/4 — paste directly after PART 3 in the same cell =====
# =====================================================================================================================
# PART 4 / 4 — figures 8–12, records (direct downloads, no ZIP), the single RUN pipeline and the Gradio interface
#              (SH782 design: one button, live stages, live engine output, tabs, figures shown and downloadable).
# THIS PART  65,184 characters · its last line is  # ===== END OF PART 4/4 =====
# =====================================================================================================================
if not {1,2,3}<=globals().get("_AKB815_PARTS",set()):raise RuntimeError("PART "+str(sorted({1,2,3}-globals().get("_AKB815_PARTS",set())))+" of the program is missing above this part in the cell — paste PART 1, 2, 3 and 4 one below the other, each completely (every part ends with an END OF PART line)")
def fig10():
    k="F10";RP=replay()
    if not RP:return fig_missing(k,"The replay table is drawn from the engine's same-run replay records of this RUN.","No TEST815_REPLAY record was written in this RUN.")
    fig=fig_base(k,"After everything else, the engine re-ranked 8 questions and re-read their first cartridge from the same SSD files — a second, independent native pass inside the same run","LIVE MEASUREMENT")
    hd=["case","first read","rank top-1","rank top-2","first answer SHA-256 · original","replay","identical","tokens","seconds  orig → replay"];xs=[.035,.10,.17,.235,.30,.52,.735,.80,.86]
    for x,h in zip(xs,hd):T(fig,x,.858,h,size=7.6,weight="bold",color=MUTED)
    hline(fig,.035,.965,.84,RULE);tr={c:tracks("ADAPTIVE").get(c) or [] for c in CASES}
    for i,r in enumerate(RP[:8]):
        y=.81-i*.052;c=r["case_id"];fi=(tr.get(c) or [{}])[0].get("ids") or [];same=r.get("initial_original_sha256")==r.get("initial_replay_sha256") and bool(r.get("initial_original_sha256"))
        vals=[(c,INK,True),(ids_lab(fi) or "—",INK2,False),(okm(r.get("rank_top1_identical")),OK_COL if r.get("rank_top1_identical") else RED,False),(okm(r.get("rank_top2_identical")),OK_COL if r.get("rank_top2_identical") else RED,False),
              (k_sha(r.get("initial_original_sha256"),24),INK2,False),(k_sha(r.get("initial_replay_sha256"),24),INK2,False),("IDENTICAL" if r.get("exact_initial_answer_identical") else "DIFFERENT",OK_COL if r.get("exact_initial_answer_identical") else AMBER,False),
              (f"{r.get('original_tokens')} / {r.get('replay_tokens')}",INK2,False),(f"{r.get('original_seconds')} → {r.get('replay_seconds')}",INK2,False)]
        for (v,col,b),x,nx in zip(vals,xs,xs[1:]+[.965]):T(fig,x,y,v,size=7.8,color=col,weight="bold" if b or v in("IDENTICAL","DIFFERENT") else "normal",mono=x in(.30,.52),xmax=nx-.006)
        if same:rect(fig,.30-.004,y-.017,.43,.034,"#ECFDF5",z=0)
    ax=fig.add_axes([.065,.12,.22,.25]);o=[float(r.get("original_seconds") or 0) for r in RP];p=[float(r.get("replay_seconds") or 0) for r in RP]
    ax.scatter(o,p,color=OK_COL,s=26,zorder=3);lo,hi=min(o+p)*.97,max(o+p)*1.03;ax.plot([lo,hi],[lo,hi],color=MUTED,lw=.9,ls="--");ax.set_xlim(lo,hi);ax.set_ylim(lo,hi)
    ax.set_xlabel("original read (s)",fontsize=7.4);ax.set_ylabel("replay read (s)",fontsize=7.4);ax.set_title("read time: original vs replay",fontsize=8);_axstyle(ax,6.6)
    s=rp_summary();box(fig,.33,.10,.255,.29,ec=OK_COL,fc=PANEL,lw=1.2)
    for j,(v,l) in enumerate([(f"{s.get('rank_top1_exact','—')}/{s.get('cases','—')}","top-1 rank identical"),(f"{s.get('rank_top2_exact','—')}/{s.get('cases','—')}","top-2 ranks identical"),
                              (f"{s.get('initial_answer_exact','—')}/{s.get('cases','—')}","first answers byte-identical"),(f"{s.get('initial_action_exact','—')}/{s.get('cases','—')}","same usable / UNKNOWN decision")]):
        T(fig,.345,.355-j*.066,v,size=15,weight="bold",color=OK_COL);T(fig,.43,.355-j*.066,l,size=8.0,color=INK)
    ex=next((r for r in results().get("replay_audit") or [] if r.get("replay_answer")),None);box(fig,.605,.10,.36,.29,ec=NEU,lw=1.1)
    if ex:
        T(fig,.615,.37,f"{ex['case_id']} · first answer as re-generated in the replay (verbatim)",size=7.8,weight="bold",color=OK_COL,xmax=.958)
        _layout_text(fig,ex["replay_answer"],.615,.958,.16,.35,fs_max=10.6,fs_min=5.8)
    T(fig,.615,.125,wrap("Scope: same run, same GPU, same files. Cross-run, cross-seed and cross-GPU reproducibility are the next stage.",80),size=7.2,color=AMBER,xmax=.958,linespacing=1.1)
    fig_footer(fig,k,"replay_audit and replay_summary of TEST815_results.json (SHA-256 of the cleaned first answer, original vs replay) · TEST815_REPLAY lines in the live engine output.")
    return save_fig(fig,k,"LIVE MEASUREMENT",["TEST815_results.json replay_audit / replay_summary","TEST815_REPLAY lines"])

def _gate_cat(n):
    m=re.match(r"^(.*?)(?:_(?:Q\d+|C\d\d_|PMC\d+|\d{3}\.py|TEST815_|REPLAY_|DROP_)).*$",n)
    return m.group(1) if m and m.group(1) else re.sub(r"_\d+$","",n)
def fig11():
    k="F11";FR=fusion_records()
    if not FR and not CHECKS:return fig_missing(k,"Timing, GPU and gates are measured from the engine output of this RUN.","The engine produced no output in this RUN.")
    fig=fig_base(k,"Measured while the engine ran: nvidia-smi every 10 s, every native fusion step the engine instruments (SSD verify · CPU→GPU · fusion), every PASS / FAIL gate it printed","LIVE MEASUREMENT")
    ax=fig.add_axes([.06,.625,.43,.20]);S=[s for s in GPU_SAMPLES if s.get("used_mib") is not None];E_=LIVE.get("engine") or {};t0=E_.get("start_t") or (S[0]["t"] if S else time.time())
    if S:ax.plot([(s["t"]-t0)/60 for s in S],[s["used_mib"]/1024 for s in S],color=INK,lw=1.2)
    st=sorted(EV["stage_t"].items(),key=lambda kv:kv[1]);keys=list(STAGES);span=max([(E_.get("end_t") or time.time())-t0,1])/60;lastx=-1e9
    for j,(kk,tt) in enumerate(st):
        x=(tt-t0)/60;ax.axvline(x,color=RULE,lw=.8)
        if x-lastx>span*.035:ax.text(x,79,str(keys.index(kk)+1),fontsize=6.4,color=MUTED,ha="center",va="top");lastx=x
    ax.set_ylim(0,82);ax.set_ylabel("GPU used (GiB)",fontsize=7.4);ax.set_xlabel("minutes since the engine started",fontsize=7.4);_axstyle(ax,6.6)
    ax.set_title(f"GPU memory · numbers = live stages · after exit {E_.get('gpu_after_mib','—')} MiB",fontsize=8.2)
    ax2=fig.add_axes([.06,.13,.43,.30])
    kc={"ADAPTIVE":COL["LOOP"],"FIXED":COL["FIX"],"ABLATION":COL["B"],"REPLAY":OK_COL,"OTHER":COL["SYN"]}
    for kind,c in kc.items():
        P=[(f["memory_tokens"],f["fusion_ms"]) for f in FR if f["kind"]==kind and f.get("memory_tokens") and f.get("fusion_ms")]
        if P:ax2.scatter([p[0] for p in P],[p[1]/1000 for p in P],s=14,color=c,alpha=.75,label=f"{kind.lower()} ({len(P)})")
    ax2.set_xlabel("memory tokens after this fusion step",fontsize=7.4);ax2.set_ylabel("native fusion (s)",fontsize=7.4);ax2.set_ylim(bottom=0)
    if FR:ax2.legend(fontsize=6.6,ncol=2,loc="upper left")
    _axstyle(ax2,6.6)
    sv=[f["ssd_verify_ms"] for f in FR if f.get("ssd_verify_ms") is not None];hd=[f["h2d_ms"] for f in FR if f.get("h2d_ms") is not None]
    ax2.set_title(f"{len(FR)} fusion steps · SSD verify {np.median(sv):.0f} ms · CPU→GPU {np.median(hd):.1f} ms (medians)" if sv and hd else "fusion steps",fontsize=8.2)
    cats=OrderedDict()
    for c in CHECKS:
        g=_gate_cat(c["name"]);cats.setdefault(g,[0,0]);cats[g][0 if c["passed"] else 1]+=1
    top=sorted(cats.items(),key=lambda kv:-(kv[1][0]+kv[1][1]))[:20]
    ax3=fig.add_axes([.69,.14,.27,.685]);y=np.arange(len(top))[::-1]
    if top:
        ax3.barh(y,[v[0] for _,v in top],color=OK_COL,height=.66);ax3.barh(y,[v[1] for _,v in top],left=[v[0] for _,v in top],color=RED,height=.66)
        ax3.set_yticks(y);ax3.set_yticklabels([g[:26] for g,_ in top],fontsize=6.3)
        for yi,(_,v) in zip(y,top):ax3.text(v[0]+v[1],yi,f" {v[0]}"+(f" / {v[1]} FAIL" if v[1] else ""),va="center",fontsize=6.2)
        ax3.set_xlim(0,max(v[0]+v[1] for _,v in top)*1.3)
    ax3.set_title(f"engine gates: {sum(1 for c in CHECKS if c['passed'])} PASS · {sum(1 for c in CHECKS if not c['passed'])} FAIL",fontsize=8.4);_axstyle(ax3,6.4)
    T(fig,.06,.535,"Fusion time grows with memory: a pair read (≈1,960 tokens) costs about twice a single read — every read is recomputed natively, nothing is cached.",size=7.4,color=INK2,xmax=.60)
    fig_footer(fig,k,"GPU_SAMPLES.json (host nvidia-smi) · NATIVE_FUSION_STEP lines (engine instrumentation of the locked TEST779 build_fusion) · PASS / FAIL lines grouped by gate name (ENGINE_CHECKS.json).")
    return save_fig(fig,k,"LIVE MEASUREMENT",["GPU_SAMPLES.json","NATIVE_FUSION_STEP lines","ENGINE_CHECKS.json"])

def fig12():
    k="F12";sm=summary();ac=acceptance()
    if not sm or not ac:return fig_missing(k,"The ledger is decided only from this RUN's engine records.","The engine did not complete in this RUN.")
    fig=fig_base(k,"Decided only from this RUN's records — left: what the run demonstrates, with its numbers · right: what the next stage adds","VERIFICATION RECORD")
    V=LIVE.get("verification") or {};C_=V.get("consistency") or {};ev=evidence_classes();nl,ir=ev["none_left"],ev["irrelevant"];rs=rp_summary();cm=cost()
    rw_=rows();t2=sum(1 for r in (rw_ or list(row_logs().values())) if (r.get("offline_routing_eval") or {}).get("top2_relevant"));aud=[r for r in rw_ if ((r.get("offline_fact_audit") or {}).get("adaptive") or {}).get("status")=="NARROW_NUMERIC_FACT_CHECK"]
    rel_ok=sum(1 for r in aud if ((relation().get(r["case_id"]) or {}).get("adaptive") or {}).get("passed"))
    nver=sum(1 for r in (V.get("cartridges") or {}).values() if r.get("file_sha_ok"))
    L=[(bool(ac.get("frozen_weights")) and bool(ac.get("no_residual_hooks")),"Frozen Qwen2.5-72B — no training, no fine-tuning, no hook left behind"),
       (bool(ac.get("physical_cartridges")) and nver==22,f"22 physical CUT3 cartridges on the SSD · host re-hash {nver}/22"),
       (sm.get("routing_top2_relevant")==sm.get("cases") and sm.get("decoy_selected_cases")==0,f"Blind native H3 routing: relevant article in top-2 {sm.get('routing_top2_relevant')}/{sm.get('cases')} · decoys {sm.get('decoy_selected_cases')}/{sm.get('cases')}"),
       (t2==16,f"Paraphrase control: relevant article in top-2 for {t2}/16 wordings"),
       ((sm.get("adaptive_native_reads") or 99)<(sm.get("fixed_native_reads") or 0) and policy().get("changed_decisions")==0,f"Closed loop: {sm.get('adaptive_native_reads')} native reads vs {sm.get('fixed_native_reads')} fixed — same {16-int(policy().get('changed_decisions') or 0)}/16 decisions"),
       ((sm.get("unknown_recovery_observed") or 0)>0,f"Recovered from UNKNOWN {sm.get('unknown_recovery_observed')}× by reading the alternate · {sm.get('hypothesis_revision_observed')} hypothesis revisions"),
       (len(nl)>0 and _n_ab(nl)==len(nl) and _n_ab(ir)==0,f"Evidence removal: abstained {_n_ab(nl)}/{len(nl)} with no relevant article left · answered {len(ir)-_n_ab(ir)}/{len(ir)} when an irrelevant one was removed"),
       (bool(aud) and rel_ok==len(aud),f"Numeric relation audit (98 % DOI · 78 % URL · 80 % automatic): {rel_ok}/{len(aud)}"),
       (rs.get("initial_answer_exact")==rs.get("cases") and bool(rs.get("cases")),f"Same-run replay: first answers byte-identical {rs.get('initial_answer_exact')}/{rs.get('cases')} · rankings {rs.get('rank_top2_exact')}/{rs.get('cases')}"),
       (C_.get("gates_fail")==0 and bool(C_.get("gates_pass")),f"{C_.get('gates_pass','—')} engine gates PASS · {C_.get('gates_fail','—')} FAIL · records cross-checked by the host")]
    box(fig,.035,.12,.535,.745,ec=OK_COL,lw=1.6);rect(fig,.035,.825,.535,.04,OK_COL,z=2);T(fig,.045,.845,"DEMONSTRATED IN THIS RUN",size=10.5,weight="bold",color="white")
    for j,(v,t) in enumerate(L):
        y=.79-j*.067;T(fig,.05,y,okm(v),size=13,weight="bold",color=OK_COL if v else RED);T(fig,.08,y,t,size=8.6,color=INK,xmax=.562)
    ir_=results().get("independent_review") or {}
    N=[("Independent human scientific review",f"all 16 answers exported for reviewers ({ir_.get('cases_exported','—')} cases, SHA {k_sha(ir_.get('sha256'),10)}) — scores not yet entered"),
       ("Cross-run and cross-GPU reproducibility","this run proves same-run replay; repeated runs on other GPUs and seeds come next"),
       ("Larger and harder memory banks",f"here {ac.get('real_sources')} real articles + {ac.get('synthetic_controls')} synthetic decoys; real distractor articles next"),
       ("Finer separation of the two real articles",f"top-1 relevant {sm.get('routing_top1_relevant')}/{sm.get('cases')} — the loop compensates by reading both"),
       ("General autonomous reasoning","not claimed — TEST815 is a bounded, measurable evidence controller")]
    box(fig,.585,.12,.38,.745,ec=AMBER,lw=1.6);rect(fig,.585,.825,.38,.04,AMBER,z=2);T(fig,.595,.845,"NEXT STAGE",size=10.5,weight="bold",color="white")
    for j,(h,t) in enumerate(N):
        y=.785-j*.135;T(fig,.598,y,"→ "+h,size=9.0,weight="bold",color=AMBER,xmax=.958);_layout_text(fig,t,.613,.958,y-.10,y-.018,fs_max=9.6,fs_min=6.2,color=INK2)
    T(fig,.035,.093,f"engine verdict: {ac.get('verdict','—')} · mechanical demo ready {okm(ac.get('mechanical_demo_ready'))} · scientific claim ready {okm(ac.get('scientific_claim_ready'))} (pending human review by design)",size=8.0,weight="bold",color=INK2,xmax=.965)
    fig_footer(fig,k,"Left: summary, demo_acceptance, policy_comparison, source_removal_ablation, relation_audit, replay_summary (TEST815_results.json) + POST_RUN_VERIFICATION.json. Right: flags the engine itself records as open.")
    return save_fig(fig,k,"VERIFICATION RECORD",["TEST815_results.json","POST_RUN_VERIFICATION.json"])

FIG_FUNCS=OrderedDict([("F1",fig1),("F2",fig2),("F3",fig3),("F4",fig4),("F5",fig5),("F6",fig6),("F7",fig7),("F8",fig8),("F9",fig9),("F10",fig10),("F11",fig11),("F12",fig12)])
def render_figures():
    errs={};FIGURES.clear();FIGURES.update(BASE_FIGURES)
    for key,fn in FIG_FUNCS.items():
        t=time.perf_counter();STATE["stages"]["FIGURES"]["note"]=f"drawing Figure {FIGURES[key]['n']}/12 — {FIGURES[key]['title']}";bump()
        try:
            rec=fn();FIG_FILES[key]=rec;STATE["fig_version"]+=1;bump()
            _emit(f"  figure {FIGURES[key]['n']} · {rec['badge']} · {rec['pixels'][0]}×{rec['pixels'][1]} · layout QC {'pass' if rec['layout_qc']['passed'] else 'FAIL'} · {time.perf_counter()-t:.1f} s")
        except Exception as ex:
            errs[key]=f"{type(ex).__name__}: {ex}";FIG_FILES.pop(key,None);flog_fig(f"{key} NOT GENERATED {traceback.format_exc()[-1500:]}");_emit(f"  figure {key} NOT GENERATED · {errs[key]}");plt.close("all")
    FIG_ERRORS.clear();FIG_ERRORS.update(errs)
    dump_json(SESSION_DIR/"FIGURES_MANIFEST.json",dict(session=SESSION_ID,utc=utc_now(),simulation=SIM,figures=FIG_FILES,not_generated=errs))
    return errs
def stage_figures():
    errs=render_figures();n=len([k for k in FIG_FILES if k in BASE_FIGURES])
    qcf=[k for k,v in FIG_FILES.items() if not (v.get("layout_qc") or {}).get("passed") or not (v.get("jpeg_qc") or {}).get("passed")]
    np_=[k for k,v in FIG_FILES.items() if v["badge"]=="NOT PRODUCED IN THIS RUN"]
    note=f"{n}/{len(BASE_FIGURES)} JPEG figures written (300 dpi)"
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
def write_run_summary():
    L=[];a=L.append;sm=summary();ac=acceptance()
    a(f"{APP_NAME} — {APP_SUB}\n{EXPERIMENT} live demonstration · demo {CODE_VERSION} · RUN {SESSION_ID} · written {local_now()}")
    if SIM:a("SIMULATION — NOTHING IN THIS FILE IS AN EXPERIMENTAL RESULT")
    a(f"RUN VERDICT {run_verdict()}\nengine: 815.py git blob {LOCKS[ENGINE_NAME]} executed unchanged as one OS process · engine run folder {EV.get('root')}")
    E_=LIVE.get("engine") or {};a(f"engine process pid {E_.get('pid')} · {E_.get('start')} → {E_.get('end')} · exit {E_.get('exit_code')} · {E_.get('seconds')} s · GPU after exit {E_.get('gpu_after_mib')} MiB")
    a("\nSTAGES (times = this RUN)")
    for key,title in STAGES.items():
        s=STATE["stages"][key];a(f"  [{s['status'].upper():<4}] {key:<10} {('%.0f s'%s['seconds']) if s['seconds'] is not None else '':>8}  {title}\n             {s['note']}")
    if sm:
        a("\nENGINE SUMMARY (TEST815_results.json, verbatim keys)")
        for kk in ("cases","source_count","routing_top1_relevant","routing_top2_relevant","decoy_selected_cases","adaptive_native_reads","fixed_native_reads","adaptive_answers","fixed_answers",
                   "changed_decisions","hypothesis_revision_observed","unknown_recovery_observed","narrow_fact_audit_pass","narrow_fact_audit_total","scientific_accuracy","claim"):a(f"  {kk:<32} {sm.get(kk)}")
    if ac:a(f"\nENGINE ACCEPTANCE  verdict {ac.get('verdict')}\n  "+" · ".join(f"{kk}={v}" for kk,v in ac.items() if kk!="verdict"))
    ev=evidence_classes()
    if ablation():a(f"\nEVIDENCE REMOVAL  abstained with no relevant article left {_n_ab(ev['none_left'])}/{len(ev['none_left'])} · answered with an irrelevant one removed {len(ev['irrelevant'])-_n_ab(ev['irrelevant'])}/{len(ev['irrelevant'])} · answered with another relevant left {len(ev['other_left'])-_n_ab(ev['other_left'])}/{len(ev['other_left'])}")
    for r in rows():
        ad=r.get("adaptive") or {};a(f"\n{r['case_id']} · {r.get('question')}\n  ADAPTIVE {ad.get('action')} · reads {ad.get('read_count')} · path "+" → ".join(f"{s.get('operation')}[{'+'.join(s.get('ids') or [])}]" for s in ad.get("steps") or [])+
                                    "\n  "+str(ad.get("answer")).replace("\n","\n  "))
    a("\nHUMAN REVIEW: NOT PROVIDED (pending) — TEST815_independent_review.csv is the review sheet. No semantic grading was performed by the engine or by this demo.")
    a(f"\n{AUTHOR} · {ORG} · {LICENSE_NAME} · {COPYRIGHT}")
    RUN_SUMMARY.write_text("\n".join(L)+"\n",encoding="utf-8");_private(RUN_SUMMARY)
def download_items():
    items=[("Run summary",RUN_SUMMARY),("Engine output, real-time (UTC receipt · stream · line)",ENGINE_OUT),("Session log",SESSION_LOG),("Session events (JSONL)",SESSION_EVENTS),
           ("Engine process",DATA_DIR/"ENGINE_PROCESS.json"),("GPU samples",DATA_DIR/"GPU_SAMPLES.json"),("Post-run verification",VERIFY_FILE),("Cartridge anatomy (heat-map data)",DATA_DIR/"CARTRIDGE_ANATOMY.npz"),
           ("Fusion steps",DATA_DIR/"FUSION_STEPS.json"),("Stage record",DATA_DIR/"STAGES.json"),("Engine checks of this RUN",DATA_DIR/"ENGINE_CHECKS.json"),("Figure manifest",SESSION_DIR/"FIGURES_MANIFEST.json"),
           ("SHA-256 manifest",MANIFEST),("815.py (locked, executed)",EVID_DIR/ENGINE_NAME)]
    out=[(l,str(p)) for l,p in items if Path(p).is_file()]
    d=DATA_DIR/"engine_records"
    if d.is_dir():out+=[(f"engine record · {p.name}",str(p)) for p in sorted(d.iterdir()) if p.is_file()]
    return out
def package_session():
    dump_json(DATA_DIR/"ENGINE_CHECKS.json",CHECKS);dump_json(DATA_DIR/"STAGES.json",dict(verdict=run_verdict(),stages=STATE["stages"],session=SESSION_ID))
    dump_json(DATA_DIR/"GPU_SAMPLES.json",GPU_SAMPLES);dump_json(DATA_DIR/"FUSION_STEPS.json",fusion_records())
    write_run_summary()
    files=[p for p in sorted(SESSION_DIR.rglob("*")) if p.is_file() and p!=MANIFEST and p.suffix!=".tmp"]
    man=OrderedDict((str(p.relative_to(SESSION_DIR)),dict(sha256=sha_file(p),bytes=p.stat().st_size)) for p in files)
    root=rroot();eng=OrderedDict()
    if root and root.is_dir():
        for p in sorted(root.rglob("*")):
            if p.is_file():eng[str(p.relative_to(root))]=dict(sha256=sha_file(p),bytes=p.stat().st_size)
    dump_json(MANIFEST,dict(session=SESSION_ID,utc=utc_now(),simulation=SIM,engine_run_folder=str(root) if root else None,
                            note="SHA-256 of every file of this RUN. Engine run folder (cartridges, extracted article texts) is hashed, not offered for download. No ZIP.",files=man,engine_files=eng))
    return str(MANIFEST)
def stage_records():
    package_session();return f"{len(FIG_FILES)} JPEG figures + {len(download_items())} records, each downloadable directly · SHA-256 manifest of {len(json.load(open(MANIFEST))['files'])} session files + {len(json.load(open(MANIFEST))['engine_files'])} engine files (no ZIP)"

# ---------------------------------------------------------------------------------------------------------------------
# THE RUN PIPELINE (one button)
# ---------------------------------------------------------------------------------------------------------------------
RUNS_DONE=[]
def run_pipeline():
    if RUNS_DONE:_session_paths(datetime.now().astimezone().strftime("SH815-%Y%m%d-%H%M%S")+f"-RUN{len(RUNS_DONE)+1}")
    RUNS_DONE.append(SESSION_ID);LIVE.clear();LIVE.update(session=SESSION_ID);LINES.clear();CHECKS.clear();FIG_FILES.clear();FIG_ERRORS.clear();PROVENANCE.clear();GPU_SAMPLES.clear();_RC.clear()
    for k_ in ("root","failed","stage"):EV[k_]=None
    for k_ in ("commits","routes","rows","ablation","replay","fusion"):EV[k_]=[]
    EV["records"]={};EV["stage_t"]={}
    STATE.update(running=True,started=utc_now(),finished=None,current=None,elapsed=None,meas=None);STATE["fig_version"]+=1
    for k_ in STAGES:STATE["stages"][k_]=dict(status="wait",seconds=None,note="",t0=None)
    banner(f"RUN {SESSION_ID} · {local_now()} · the locked TEST815 engine as one process (about 40–60 minutes on an A100, model download included)")
    def step(key,fn):
        STATE["current"]=key;stage_set(key,"run");_emit(f"── [{list(STAGES).index(key)+1}/{len(STAGES)}] {STAGES[key]}")
        try:
            note=fn();stage_set(key,"done",note);slog("STAGE_DONE",key,note=note);return True
        except Exception as ex:
            stage_set(key,"fail",f"{type(ex).__name__}: {ex}");slog("STAGE_FAILED",key,error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc()[-3000:]);return False
    try:
        if step("PRECHECK",stage_precheck):
            try:run_engine();slog("ENGINE_DONE","TEST815 completed — every engine stage passed")
            except Exception as ex:slog("ENGINE_NOT_COMPLETED",f"{type(ex).__name__}: {ex}")
        else:
            for s in ENGINE_STAGES:stage_set(s,"skip","not run — PRECHECK did not pass")
        if manifest().get("cartridges"):step("VERIFY",stage_verify)
        else:stage_set("VERIFY","skip","no cartridge manifest in this RUN")
        step("FIGURES",stage_figures);step("RECORDS",stage_records)
    finally:
        STATE.update(running=False,finished=utc_now(),current=None);bump()
        try:package_session()
        except Exception:pass
        banner(f"RUN VERDICT: {run_verdict()}\nRUN {SESSION_ID} finished {local_now()} · "+" · ".join(f"{k_}:{v['status']}" for k_,v in STATE["stages"].items()))
RUN_THREAD={"t":None}
def start_run():
    t=RUN_THREAD["t"]
    if t is not None and t.is_alive():return False
    RUN_THREAD["t"]=threading.Thread(target=run_pipeline,daemon=True,name="SH815-RUN");RUN_THREAD["t"].start();return True
# =====================================================================================================================
# PART 4 / 4 (continued) — Gradio interface (SH782 design): ONE button (RUN). Stages, the engine's own output, the sealed
#              cartridges, routing, the closed loop and every answer appear while the engine works. The page refreshes
#              itself with short requests (gr.Timer) — a dropped connection never hides the figures; a reload shows all.
# =====================================================================================================================
LINEAGE=[("Research Record I — Qwen2.5-7B","https://doi.org/10.5281/zenodo.23381336"),
         ("Research Record II — Mistral-7B, Silicon Hippocampus v1.4","https://doi.org/10.5281/zenodo.23418927"),
         ("Research Record III — Qwen2.5-72B, Direct Internal-State Injection","https://doi.org/10.5281/zenodo.23434686")]
def esc(x):return html.escape(str(x))
def card(title,body,kind="info"):return f'<div class="kz card {kind}"><div class="h">{esc(title)}</div><div class="small">{body}</div></div>'
def ok_mark(v):return "<b style='color:#08785B'>PASS</b>" if v else ("<b style='color:#B91C1C'>FAIL</b>" if v is False else "<span style='opacity:.6'>—</span>")
class Markup(str):pass
def tbl(rows_,head=None,mono_cols=()):
    h="".join(f"<th>{esc(x)}</th>" for x in head) if head else ""
    b="".join("<tr>"+"".join(f"<td class='{'mono' if i in mono_cols else ''}'>{v if isinstance(v,Markup) else esc(v)}</td>" for i,v in enumerate(r))+"</tr>" for r in rows_)
    return f"<table class='tbl'>{('<tr>'+h+'</tr>') if h else ''}{b}</table>"
def pre(text,maxh=420):return f"<div class='ans' style='max-height:{maxh}px'>{esc(text)}</div>"
def details(summary_,inner,open_=False):return f"<details{' open' if open_ else ''}><summary>{summary_}</summary>{inner}</details>"
def yn(v):return Markup("<b style='color:#08785B'>yes</b>" if v else ("<b style='color:#B45309'>no</b>" if v is False else "—"))
def act_mark(a):return Markup(f"<b style='color:{'#08785B' if a=='ANSWER' else '#B91C1C'}'>{esc(a)}</b>") if a else "—"

CSS="""
:root{--kz-on:#08785B;--kz-fg:#111827;--kz-card:#ffffff;--kz-bd:#d1d5db;--kz-a:#2455D6;--kz-err:#b91c1c;--kz-warn:#b45309;--kz-m:#7626D9}
.dark{--kz-on:#34d399;--kz-fg:#f3f4f6;--kz-card:#111827;--kz-bd:#4b5563;--kz-a:#93c5fd;--kz-err:#f87171;--kz-warn:#fbbf24;--kz-m:#c4b5fd}
html,body{overflow-x:hidden!important}
.gradio-container{width:100%!important;max-width:1180px!important;margin:0 auto!important;padding-left:10px!important;padding-right:10px!important;box-sizing:border-box!important}
.gradio-container *{box-sizing:border-box}
.kz{color:var(--kz-fg)!important;max-width:100%;overflow-wrap:anywhere;line-height:1.45}
.kz *{color:inherit}
.hero{background:#0b1220;border-radius:6px;padding:18px 18px 14px;margin:4px 0 8px}
.hero,.hero *{color:#f9fafb!important}
.rec{font-size:11.5px;letter-spacing:1.6px;text-transform:uppercase;opacity:.85;border:1px solid rgba(255,255,255,.35);display:inline-block;padding:2px 8px;border-radius:3px}
.brand{font-size:clamp(22px,6vw,34px);font-weight:800;letter-spacing:.6px;line-height:1.1;margin-top:10px}
.title{font-size:clamp(14px,3.8vw,18px);font-weight:600;margin-top:6px;color:#ddd6fe!important}
.by{font-size:13px;margin-top:10px;opacity:.9}
.tiles{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.tile{border:1px solid rgba(255,255,255,.3);border-radius:4px;padding:6px 9px;min-width:120px;flex:1}
.tile b{font-size:18px;display:block}
.tile span{font-size:11.5px;opacity:.85}
.card{background:var(--kz-card);border:1px solid var(--kz-bd);border-left:4px solid var(--kz-bd);border-radius:4px;padding:10px 12px;margin:6px 0}
.card.on{border-left-color:var(--kz-on)}.card.err{border-left-color:var(--kz-err)}.card.warn{border-left-color:var(--kz-warn)}.card.info{border-left-color:var(--kz-a)}.card.m{border-left-color:var(--kz-m)}
.card .h{font-weight:700;font-size:15px;margin-bottom:4px}
.small{font-size:13.5px}
.mono,.kz code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.3px}
.tbl{width:100%;border-collapse:collapse;font-size:13px}
.tbl td,.tbl th{border-bottom:1px solid var(--kz-bd);padding:5px 4px;vertical-align:top;text-align:left}
.tbl th{font-size:12px;opacity:.75}
.stg{font-size:13.5px;margin:2px 0}.stg.done{color:var(--kz-on)!important}.stg.run{color:var(--kz-a)!important;font-weight:700}.stg.wait{opacity:.55}.stg.fail{color:var(--kz-err)!important;font-weight:700}.stg.skip{color:var(--kz-warn)!important}
.stg .nt{font-size:12px;opacity:.85;margin-left:22px;display:block}
.ans{white-space:pre-wrap;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.6px;border:1px solid var(--kz-bd);border-radius:4px;padding:6px 8px;margin:3px 0;overflow:auto}
details{margin:4px 0}summary{cursor:pointer;font-weight:600}
#kz_run button,#kz_run{font-size:clamp(17px,4.6vw,21px)!important;font-weight:800!important;min-height:58px!important;letter-spacing:1px}
@media (max-width:640px){.tbl .hide-m{display:none}}
"""
def hero_html():
    tiles=[("2 + 20","real articles + synthetic decoys"),("22","physical cartridges on the SSD"),("H3","native routing — no labels"),("2–4","adaptive reads per question"),
           ("16 + 16 + 8","questions · removal trials · replays"),("PENDING","human scientific review")]
    return (f'<div class="kz hero"><span class="rec">Live research demonstration · frozen Qwen2.5-72B-Instruct · NF4 · BF16 · CUT3 · A100 80 GB</span>'
            f'<div class="brand">{esc(APP_NAME)}</div><div class="title">{esc(APP_SUB)}</div>'
            '<div class="by">A frozen 72-billion-parameter model reads two real scientific articles once and stores them — not as text, but as its own internal states — in sealed '
            'memory cartridges on the SSD, next to twenty synthetic decoys. Then it is asked sixteen questions. For each one it must find the right cartridge by itself, from the '
            'question\'s own internal states alone, read it, challenge its first answer with a second source, and decide: answer, or say UNKNOWN. Then the evidence is taken away '
            'to see whether it invents. Everything you see on this page is produced live by the unchanged TEST815 engine.</div>'
            '<div class="tiles">'+"".join(f'<div class="tile"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a,b in tiles)+'</div>'
            f'<div class="by"><b>{esc(AUTHOR)}</b> · {esc(ORG)} · {esc(PLACE)} · {esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · <a href="{REPO}" target="_blank" rel="noopener">{esc(REPO)}</a></div></div>')
def mode_html():
    st=STATE
    if SIM:kind,t="err","SIMULATION — code test of the author with a replayed log and no model, NOT an experimental result"
    elif st.get("running"):
        el=(time.time()-datetime.fromisoformat(st["started"]).timestamp())/60 if st.get("started") else 0
        kind,t="info",f"RUN IN PROGRESS · {el:.0f} min · stage {list(STAGES).index(st['current'])+1 if st.get('current') else '…'}/{len(STAGES)}: {STAGES.get(st.get('current'),'')}"
    elif st.get("finished"):
        ok=run_verdict().startswith("COMPLETE");kind,t=("on" if ok else "err"),f"RUN {SESSION_ID} — {run_verdict()}"
    else:kind,t="info","NOT STARTED — press RUN. The locked TEST815 engine runs as one process on the A100 (about 40–60 minutes, model download included); everything it does appears here while it works."
    return card(t,"The repository holds an earlier TEST815 run (815.log) — this page never shows it: every value, text and figure here comes from THIS RUN. "
                f"Engine 815.py git blob <span class='mono'>{esc(LOCKS[ENGINE_NAME][:16])}…</span> · it imports the locked TEST790 → 789 → 779 chain (709 · 730 · 757 · 721 · 764) by git blob itself.",kind)
def stages_html():
    out=[];n=len(STAGES);done=0
    for i,(k,title) in enumerate(STAGES.items(),1):
        s=STATE["stages"][k];stt=s["status"];mk={"done":"✓","run":"▶","fail":"✗","skip":"–","wait":"○"}[stt]
        if stt in("done","skip","fail"):done+=1
        tm=f" · {s['seconds']:.0f} s" if s.get("seconds") is not None else (f" · running {_mmss(time.perf_counter()-s['t0'])}" if stt=="run" and s.get("t0") else "")
        live=_live_text() if stt=="run" and k==EV.get("stage") and STATE.get("running") and LIVE.get("engine") and not LIVE["engine"].get("end") else ""
        out.append(f"<div class='stg {stt}'>{mk} {i}/{n} · {esc(title)}{tm}"+(f"<span class='nt'>{esc(s['note'])}</span>" if s.get("note") else "")+(f"<span class='nt'>{esc(live)}</span>" if live else "")+"</div>")
    pc=100*done/n
    bar=f'<div style="margin-top:6px;background:#e5e7eb;height:10px;border-radius:2px"><div style="width:{pc:.0f}%;height:10px;background:#7626D9;border-radius:2px"></div></div>'
    head=f"RUN {SESSION_ID} · {run_verdict()}"+(f" · started {STATE['started'][11:19]} UTC" if STATE.get("started") else "")+(f" · finished {STATE['finished'][11:19]} UTC" if STATE.get("finished") else "")
    return card(head,"".join(out)+bar,"m")
def console_text():
    with _LOG_LOCK:return "\n".join(list(CONSOLE)[-200:])

# ---------------------------------------------------------------------------------------------------------------------
# tab contents — read from THIS RUN's records, unedited (partial while the engine works)
# ---------------------------------------------------------------------------------------------------------------------
def _gate(name):
    c=[x for x in CHECKS if x["name"]==name];return (c[-1]["passed"] if c else None)
def _gates(prefix):
    c=[x for x in CHECKS if x["name"].startswith(prefix)];return (all(x["passed"] for x in c) if c else None),len(c)
def overview_html():
    sm=summary();ac=acceptance();ev=evidence_classes() if ablation() else None
    steps=[("The engine verifies its own locked chain","TEST790 / 789 / 779 exact git blobs; 709 · 730 · 757 · 721 · 764 sources and symbols",_gates("GIT_LOCK_")[0] and _gate("TEST779_EXACT_BLOB")),
           ("Two real articles from Europe PMC","exact DOI and title locks · scientific body extracted · SHA-256",_gate("TWO_LOCKED_ARTICLES") if _gate("TWO_LOCKED_ARTICLES") is not None else _gates("EXACT_DOI_LOCK")[0]),
           ("Frozen Qwen2.5-72B forges 22 physical cartridges","H3 + K/V of layers 0–3 · sealed on the SSD · re-opened with SHA checks",_gate("PHYSICAL_22_CARTRIDGES")),
           ("Native H3 routing over all 22 — no labels","the question's own layer-3 states · 8 paraphrase controls",_gate("PARAPHRASE_EIGHT")),
           ("Closed loop vs fixed policy, 16 questions","read → challenge → reverse → decide · max 4 reads",_gate("THIRTY_TWO_POLICY_CASES")),
           ("Evidence removal, 16 trials","each real article removed; best of the 21 survivors read natively",_gate("SOURCE_REMOVAL_16")),
           ("Same-run replay, 8 cases","ranking and first answer recomputed from the same files",_gate("REPLAY_EIGHT")),
           ("Engine acceptance","frozen weights · no residual hooks · review CSV + public audit",(ac.get("mechanical_demo_ready") if ac else None))]
    rows_=[(Markup(f"<b>{i}. {esc(a)}</b><br><span class='small' style='opacity:.85'>{esc(b)}</span>"),Markup(ok_mark(v))) for i,(a,b,v) in enumerate(steps,1)]
    res=""
    if sm:
        res=tbl([("relevant article in the top-2 (no labels)",f"{sm.get('routing_top2_relevant')}/{sm.get('cases')}"),("questions with a decoy in the top-2",f"{sm.get('decoy_selected_cases')}/{sm.get('cases')}"),
                 ("native reads — adaptive vs fixed",f"{sm.get('adaptive_native_reads')} vs {sm.get('fixed_native_reads')} · decisions changed {sm.get('changed_decisions')}"),
                 ("recoveries from UNKNOWN · hypothesis revisions",f"{sm.get('unknown_recovery_observed')} · {sm.get('hypothesis_revision_observed')}"),
                 *([("abstained — no relevant article left",f"{_n_ab(ev['none_left'])}/{len(ev['none_left'])}"),("answered — an irrelevant article removed",f"{len(ev['irrelevant'])-_n_ab(ev['irrelevant'])}/{len(ev['irrelevant'])}")] if ev else []),
                 ("numeric fact audit (Q2 · Q8)",f"{sm.get('narrow_fact_audit_pass')}/{sm.get('narrow_fact_audit_total')}"),("same-run replay, identical first answers",f"{rp_summary().get('initial_answer_exact','—')}/{rp_summary().get('cases','—')}"),
                 ("engine verdict",(ac or {}).get("verdict","—")),("scientific accuracy",sm.get("scientific_accuracy"))],["result of THIS RUN","value"])
    arch=card("Cognitive cartridge + closed loop — what it is and what it is not",
        "<b>Cognitive cartridge:</b> a file on the SSD holding internal states of the frozen Qwen2.5-72B for one text — the layer-3 output H3 and the K/V of layers 0–3 (CUT3). It is reloaded, SHA-checked and fused back at the layer-3 boundary; layers 4–79 recompute everything natively.<br>"
        "<b>Native H3 routing:</b> the question passes through the same frozen layers; its own layer-3 states are scored against 96 sampled states of every cartridge (locked TEST757 numeric_rank). No title, label, keyword or text is used.<br>"
        "<b>Closed loop:</b> the controller reads the top-1 cartridge, challenges a usable answer with the second, reads the alternate when the first says UNKNOWN, checks the reverse order when the readings disagree, then answers or abstains — at most four native reads.<br>"
        "<b>Not text RAG · not fine-tuning:</b> no article text in the prompt; the weights are frozen and no hook stays registered.<br>"
        "<b>Not a semantic grade:</b> correctness of the answers is open to independent human review (CSV exported); the run itself checks numbers and their relations narrowly.","info")
    lin=card("Research lineage (published records and repository — not results of this run)","<br>".join(f"{esc(t)} · <a href='{u}' target='_blank' rel='noopener'>{esc(u)}</a>" for t,u in LINEAGE)+
             f"<br>Engine: <a href='{URL_815}' target='_blank' rel='noopener'>815.py</a> · earlier published run of the same engine: <a href='{URL_815_LOG}' target='_blank' rel='noopener'>815.log</a> (not used here)","info")
    return card(f"What happens in this RUN ({SESSION_ID})",tbl(rows_,["step","this RUN"]),"m")+(card("Results of this RUN",res,"on") if res else "")+arch+lin
def bank_html():
    D=documents();E=manifest().get("cartridges") or {};V=(LIVE.get("verification") or {}).get("cartridges") or {}
    out=""
    for c in REAL_IDS:
        d=D.get(c) or {};src=next((x for x in EV["records"].get("sources",[]) if x.get("pmcid")==c),{})
        if not d and not src:continue
        rows_=[("article",f"{REAL[c]['title']} · {REAL[c]['journal']}"),("DOI",d.get("doi") or src.get("doi")),("Europe PMC XML",d.get("xml_url")),("XML SHA-256",d.get("xml_sha256")),
               ("extracted / excerpt",f"{d.get('full_extracted_chars','—')} characters extracted · excerpt {d.get('excerpt_chars','—')} characters"),
               ("stored in the cartridge",f"{d.get('physical_text_tokens','—')} tokens · SHA-256 {d.get('physical_text_sha256','—')}"),("licence handling",d.get("license"))]
        out+=card(f"{c} — {REAL[c]['short']}",tbl(rows_,mono_cols=(1,))+"<div class='small' style='opacity:.8'>The article text is not redistributed by this demonstration — it is linked and hash-recorded; read it at the publisher.</div>","m")
    if not out:out=card("Sources","Not available yet — the engine loads the two articles in stage 3.","info")
    rows_=[(c,cshort(c) if is_real(c) else (E[c].get("role") or "")[:28],E[c].get("body_tokens"),E[c].get("n"),f"{E[c].get('forge_seconds')} s",E[c].get("sha256"),
            Markup(ok_mark((V.get(c) or {}).get("file_sha_ok"))),fmt_b((V.get(c) or {}).get("bytes"))) for c in cartridge_ids() if c in E]
    live=f"{len(EV['commits'])}/22 cartridges committed so far (PHYSICAL_COMMIT lines)" if EV["commits"] else ""
    return out+card("Physical cartridges of this RUN",(tbl(rows_,["id","role / article","body tokens","n","forge","file SHA-256 (manifest)","host re-hash","file"],mono_cols=(5,))if rows_ else live or "not written yet"),"m")
def routing_html():
    M,ids=score_matrix();Q=questions()
    if M is None:return card("H3 routing","Not available yet — routing runs after the 22 cartridges are sealed (stage 6).","info")
    rows_=[]
    for i,c in enumerate(CASES):
        if np.all(np.isnan(M[i])):continue
        order=[ids[j] for j in np.argsort(-np.nan_to_num(M[i],nan=-9))];rel=relevant(c)
        dec=max((M[i,j] for j,x in enumerate(ids) if not is_real(x)),default=np.nan);rv=max((M[i,ids.index(x)] for x in rel if x in ids),default=np.nan)
        rows_.append((c,short(Q.get(c) or "",90),f"{order[0]} ({M[i,ids.index(order[0])]:.4f})",order[1],", ".join(rel),yn(order[0] in rel),yn(bool(set(order[:2])&set(rel))),f"{rv-dec:+.4f}"))
    pr=[(r["case_id"],r.get("original_top1"),r.get("paraphrase_top1"),yn(r.get("same_top1")),yn(r.get("original_top1_relevant")),yn(r.get("paraphrase_top1_relevant"))) for r in routes()]
    return (card("Native H3 routing — all 22 cartridges scored for every question",tbl(rows_,["case","question","top-1 (score)","top-2","relevant (offline key)","top-1 relevant","in top-2","margin over best decoy"],mono_cols=(2,7)),"m")+
            card("Paraphrase controls",tbl(pr,["case","original top-1","paraphrase top-1","same","original relevant","paraphrase relevant"]) if pr else "after the routing stage","info"))
def loop_html():
    TA=tracks("ADAPTIVE");TF=tracks("FIXED");RL=row_logs()
    if not TA and not RL:return card("Closed loop","Not available yet — the 16 closed-loop cases run in stage 7.","info")
    rows_=[]
    for c in CASES:
        r=row(c) or {};ad=r.get("adaptive") or {};lg=RL.get(c) or {}
        if not TA.get(c) and not lg:continue
        rows_.append((c," → ".join(f"{oplab(s['op'])} [{ids_lab(s['ids'])}]" for s in TA.get(c,[])),len(TA.get(c,[])) or lg.get("adaptive_reads"),act_mark(ad.get("action") or lg.get("adaptive_action")),
                      "recovered" if ad.get("recovered_from_unknown") else ("revised" if (ad.get("revision") if ad else lg.get("adaptive_revision")) else "—"),ad.get("support","—"),len(TF.get(c,[])) or lg.get("fixed_reads"),act_mark((r.get("fixed") or {}).get("action") or lg.get("fixed_action"))))
    cm=cost();pc=policy()
    ct=tbl([(k_,json.dumps(jsafe(v),ensure_ascii=False)) for k_,v in cm.items()]+[("policy comparison",json.dumps(jsafe(pc),ensure_ascii=False))],["policy","engine record"],mono_cols=(1,)) if cm else "after the closed-loop stage"
    return card("Every read of every question (A = PMC9521804 · B = PMC9401135)",tbl(rows_,["case","adaptive path","reads","adaptive","hypothesis","support","fixed reads","fixed"]),"m")+card("Cost matrix and policy comparison (engine records)",ct,"info")
def evidence_html():
    AB=ablation()
    if not AB:return card("Evidence controls","Not available yet — the removal trials run in stage 8.","info")
    rows_=[(a["case_id"],f"{L_(a['removed'])} · {cshort(a['removed'])}",(L_(a.get("top1")) if is_real(a.get("top1")) else a.get("top1")),yn(a.get("removed_relevant_offline")),act_mark(a.get("native_action")),a.get("native_tokens"),Markup(f"<span class='small'>{esc(a.get('native_answer'))}</span>")) for a in AB]
    ev=evidence_classes()
    head=(f"abstained with no relevant article left {_n_ab(ev['none_left'])}/{len(ev['none_left'])} · answered when an irrelevant article was removed {len(ev['irrelevant'])-_n_ab(ev['irrelevant'])}/{len(ev['irrelevant'])} · "
          f"answered with another relevant article left {len(ev['other_left'])-_n_ab(ev['other_left'])}/{len(ev['other_left'])} · decoy read instead {sum(1 for a in AB if a.get('selected_synthetic'))}/{len(AB)}")
    fa=[];RA=relation()
    for r in rows():
        f_=(r.get("offline_fact_audit") or {}).get("adaptive") or {}
        if f_.get("status")=="NARROW_NUMERIC_FACT_CHECK":
            ra=(RA.get(r["case_id"]) or {}).get("adaptive") or {}
            fa.append((r["case_id"],", ".join(f_.get("required") or []),", ".join(f_.get("observed") or []),Markup(ok_mark(f_.get("passed"))),Markup(ok_mark(ra.get("passed"))),json.dumps({k_:v for k_,v in ra.items() if k_ not in("status","passed")})))
    return (card("Source removal — 16 native trials (verbatim answers)",f"<div class='small'><b>{esc(head)}</b></div>"+tbl(rows_,["case","removed","read instead","removed was relevant","action","tokens","native answer (verbatim)"]),"m")+
            card("Numeric fact and relation audit (offline key, after inference)",tbl(fa,["case","required","observed","numbers","relations","relation detail"],mono_cols=(5,)) if fa else "after the closed-loop stage","info"))
def answers_html():
    rw=rows()
    if not rw:return card("Answers","Not available yet — answers are written by the engine during the closed-loop stage.","info")
    out=""
    for r in rw:
        ad=r.get("adaptive") or {};fx=r.get("fixed") or {}
        st="".join(details(f"{esc(s.get('operation'))} · {esc('+'.join(s.get('ids') or []))} · {s.get('tokens')} tokens · {s.get('elapsed_seconds')} s"+(" · possible truncation" if s.get("possible_truncation") else ""),pre(s.get("raw"),220)) for s in ad.get("steps") or [])
        sf="".join(details(f"FIXED {esc(s.get('operation'))} · {esc('+'.join(s.get('ids') or []))} · {s.get('tokens')} tokens",pre(s.get("raw"),200)) for s in fx.get("steps") or [])
        out+=card(f"{r['case_id']} · ADAPTIVE {ad.get('action')} · {ad.get('read_count')} reads"+(" · recovered from UNKNOWN" if ad.get("recovered_from_unknown") else (" · revised" if ad.get("revision") else "")),
                  f"<b>{esc(r.get('question'))}</b>"+pre(ad.get("answer"),300)+st+details(f"FIXED policy · {fx.get('action')} · {fx.get('read_count')} reads",pre(fx.get("answer"),240)+sf),"m")
    return card("All answers — verbatim, unedited","The frozen model's own words after reading physical memory. Independent human review: TEST815_independent_review.csv (download list).","info")+out
def integrity_html():
    rp=[(r["case_id"],yn(r.get("rank_top1_identical")),yn(r.get("rank_top2_identical")),yn(r.get("exact_initial_answer_identical")),k_sha(r.get("initial_original_sha256"),20),k_sha(r.get("initial_replay_sha256"),20),f"{r.get('original_seconds')} → {r.get('replay_seconds')}") for r in replay()]
    cats=OrderedDict()
    for c in CHECKS:
        g=_gate_cat(c["name"]);cats.setdefault(g,[0,0]);cats[g][0 if c["passed"] else 1]+=1
    gc_=[(g,v[0],v[1]) for g,v in cats.items()];last=[(c["utc"][11:19],c["name"],Markup(ok_mark(c["passed"])),c["detail"][:140]) for c in CHECKS[-60:]]
    fails=[(c["utc"][11:19],c["name"],c["detail"][:200]) for c in CHECKS if not c["passed"]]
    src=[(n,v["git_blob"],v["sha256"],f"{v['bytes']:,}",v.get("obtained")) for n,v in SOURCES.items()]+[(n,b,"verified inside the engine","—","engine (fail-closed)") for n,b in ENGINE_CHAIN.items()];V=LIVE.get("verification") or {}
    return (card("Same-run replay",tbl(rp,["case","top-1","top-2","first answer identical","SHA-256 original","SHA-256 replay","seconds"],mono_cols=(4,5)) if rp else "after the replay stage","on" if rp and all(r.get("exact_initial_answer_identical") for r in replay()) else "info")+
            card(f"Engine gates of this RUN — {sum(1 for c in CHECKS if c['passed'])} PASS · {sum(1 for c in CHECKS if not c['passed'])} FAIL",(tbl(fails,["UTC","FAILED gate","detail"]) if fails else "")+
                 details("gates grouped by name",tbl(gc_,["gate","PASS","FAIL"]))+details("last 60 gates",tbl(last,["UTC","gate","result","detail"],mono_cols=(3,))),"on" if CHECKS and not fails else ("err" if fails else "info"))+
            card("Independent re-verification after the run (read-only, host)",pre(json.dumps(jsafe({k_:v for k_,v in V.items()}),indent=1),420) if V else "after the engine has finished","info")+
            card("Locked sources (git blob verified)",tbl(src,["file","git blob","SHA-256","bytes","obtained"],mono_cols=(1,2)),"info"))
def resources_html():
    E_=LIVE.get("engine") or {};G=LIVE.get("gpu") or {};D=LIVE.get("disk") or {};S=[s["used_mib"] for s in GPU_SAMPLES if s.get("used_mib") is not None];FR=fusion_records()
    pr=tbl([("GPU",f"{G.get('name')} · {G.get('total_mib')} MiB · driver {G.get('driver')}"),("before RUN",f"{G.get('used_mib')} MiB used · processes {G.get('apps')}"),("disk",f"{D.get('free_gib')} GiB free · model cache {D.get('model_cache_gib')} GiB"),
            ("engine process",f"pid {E_.get('pid')} · {E_.get('start')} → {E_.get('end')} · exit {E_.get('exit_code')} · {E_.get('seconds')} s"),("GPU after exit",f"{E_.get('gpu_after_mib')} MiB"),
            ("GPU samples",f"{len(S)} · peak {max(S)/1024:.1f} GiB" if S else "—")],["item","this RUN"]) if G else "after PRECHECK"
    ft=""
    if FR:
        grp=OrderedDict()
        for f in FR:grp.setdefault((f["kind"],f.get("memory_tokens",0)>1500),[]).append(f)
        ft=tbl([(k_[0],"pair (2nd cartridge)" if k_[1] else "single",len(v),f"{np.median([x['ssd_verify_ms'] for x in v]):.0f}",f"{np.median([x['h2d_ms'] for x in v]):.1f}",f"{np.median([x['fusion_ms'] for x in v]):.0f}") for k_,v in grp.items()],
               ["kind","fusion step","n","SSD verify ms (median)","CPU→GPU ms","fusion ms"])
    return card("Hardware and the engine process",pr,"m")+card("Native fusion steps (NATIVE_FUSION_STEP lines)",ft or "after the first native read","info")
TABS=["OVERVIEW","CARTRIDGE BANK","H3 ROUTING","CLOSED LOOP","EVIDENCE CONTROLS","ANSWERS","REPLAY · INTEGRITY","RESOURCES","SCIENTIFIC FIGURES"]
TAB_HTML={"OVERVIEW":overview_html,"CARTRIDGE BANK":bank_html,"H3 ROUTING":routing_html,"CLOSED LOOP":loop_html,"EVIDENCE CONTROLS":evidence_html,"ANSWERS":answers_html,
          "REPLAY · INTEGRITY":integrity_html,"RESOURCES":resources_html}
def _figlabel(k):m=FIGURES[k];return f"Figure {m['n']} — {m['title']}"
def tab_gallery(tab):
    keys=[k for k,m in FIGURES.items() if (m["tab"]==tab or tab=="SCIENTIFIC FIGURES") and k in FIG_FILES]
    return [(FIG_FILES[k]["jpg"],f"{_figlabel(k)} · {FIG_FILES[k]['badge']}") for k in keys]
def figs_status_html():
    n=len(FIG_FILES)
    if not n and not FIG_ERRORS:return card(f"Scientific figures of this RUN — 0/{len(BASE_FIGURES)}","The twelve figures are drawn from this RUN's outputs after the engine has finished (stage 12). They appear here, one below the other.","info")
    def st(k):
        f=FIG_FILES.get(k)
        if not f:return "NOT GENERATED: "+str(FIG_ERRORS.get(k,"pending"))
        q=f.get("layout_qc") or {};j=f.get("jpeg_qc") or {}
        return f"{f['badge']} · {f['pixels'][0]}×{f['pixels'][1]} JPEG 300 dpi · layout QC {'PASS' if q.get('passed') else 'FAIL'} · JPEG QC {'PASS' if j.get('passed') else 'FAIL'}"
    rows_="".join(f"<div class='small'>{'✓' if k in FIG_FILES and (FIG_FILES[k].get('layout_qc') or {}).get('passed') and FIG_FILES[k]['badge']!='NOT PRODUCED IN THIS RUN' else '✗'} {esc(_figlabel(k))} · <b>{esc(st(k))}</b></div>" for k in FIGURES)
    ok=all(k in FIG_FILES for k in BASE_FIGURES) and all((v.get("layout_qc") or {}).get("passed") and v["badge"]!="NOT PRODUCED IN THIS RUN" for v in FIG_FILES.values())
    return card(f"Scientific figures of this RUN ({SESSION_ID}) — {n} JPEG file(s)",rows_,"on" if ok else "warn")
from urllib.parse import quote as _urlquote   # NOTE: never shadow — the URL quote has its own name
# relative URLs (no leading "/"): they resolve against the page itself (share link, Colab port window, proxy root path)
def file_url(p):return ("gradio_api/file=" if _GR_MAJOR>=5 else "file=")+_urlquote(str(p),safe="/")
def file_url_alt(p):return ("file=" if _GR_MAJOR>=5 else "gradio_api/file=")+_urlquote(str(p),safe="/")
def figs_main_html():
    """the figures of THIS run, in order — each with its own direct JPEG download link below it"""
    if not FIG_FILES:return card("Figures","No figure of this RUN yet (figures of an earlier RUN are never shown).","info")
    keys=[k for k in FIGURES if k in FIG_FILES];out=[]
    bulk=("<a href='#' onclick=\"var l=document.querySelectorAll('a.kz-dl');for(var i=0;i<l.length;i++){(function(a,d){setTimeout(function(){a.click()},d)})(l[i],i*900)};return false;\">"
          f"<b>⬇ Download all {len(keys)} figures (JPEG), one after another</b></a>")
    out.append(card("Direct downloads — no ZIP",f"{bulk}<br><span class='small'>The browser downloads the JPEG files in order. Some browsers ask once to “allow multiple downloads”; if blocked, "
                    "use the link under each figure or the JPEG file list below — every file downloads with one tap. The same figures are also shown and downloaded in the Colab cell.</span>","on"))
    for k in keys:
        f=FIG_FILES[k];u=file_url(f["jpg"]);ua=file_url_alt(f["jpg"]);nm=Path(f["jpg"]).name;qc=(f.get("layout_qc") or {}).get("passed") and f["badge"]!="NOT PRODUCED IN THIS RUN"
        out.append(f"<div class='kz card {'on' if qc else 'err'}'><div class='h'>{esc(_figlabel(k))} · {esc(f['badge'])}"+("" if (f.get("layout_qc") or {}).get("passed") else " · LAYOUT QC FAIL")+"</div>"
                   f"<img src='{u}' data-alt='{ua}' onerror=\"if(!this.dataset.done){{this.dataset.done=1;this.src=this.dataset.alt;var a=this.parentNode.querySelector('a.kz-dl');if(a)a.href=this.dataset.alt;}}\" "
                   f"style='width:100%;height:auto;border:1px solid #d1d5db' alt='{esc(_figlabel(k))}'>"
                   f"<div class='small' style='margin-top:4px'><a class='kz-dl' href='{u}' download='{esc(nm)}'><b>⬇ Download {esc(_figlabel(k).split(' — ')[0])} (JPEG, {f['pixels'][0]}×{f['pixels'][1]}, 300 dpi)</b></a> · "
                   f"<span class='mono'>{esc(nm)} · SHA-256 {esc(f['sha256_jpg'][:16])}…</span></div></div>")
    return "".join(out)
def jpg_files():return [FIG_FILES[k]["jpg"] for k in FIGURES if k in FIG_FILES]
def _safe(fn):
    try:return fn()
    except Exception as ex:return card("Display error",f"<code>{esc(type(ex).__name__)}: {esc(ex)}</code> — the records are unaffected","err")
def all_files():return [p for _,p in download_items()]
def snapshot(last):
    """full output tuple; html parts are rebuilt only when the state changed, figures only when they changed"""
    _live_root();v=STATE["version"];fv=STATE["fig_version"];out=[_safe(mode_html),_safe(stages_html),console_text()]
    if last.get("v")!=v:
        for t in TAB_HTML:out.append(_safe(TAB_HTML[t]))
        last["v"]=v
    else:out+=[gr.update() for _ in TAB_HTML]
    if last.get("fv")!=fv:out+=[tab_gallery(t) for t in TABS];last["fv"]=fv;figs=[jpg_files() or None,_safe(figs_status_html),_safe(figs_main_html)]
    else:out+=[gr.update() for _ in TABS];figs=[gr.update(),gr.update(),gr.update()]
    fl=all_files()
    if last.get("files")!=len(fl):out.append(fl or None);last["files"]=len(fl)
    else:out.append(gr.update())
    return tuple(out+figs)
_HAS_TIMER=hasattr(gr,"Timer") and hasattr(gr,"State")
def _snap_state(last):
    last=dict(last) if isinstance(last,dict) else {}
    return (*snapshot(last),last)
def run_click(last):
    start_run();time.sleep(.5);return _snap_state({})
def ui_tick(last):return _snap_state(last)
def page_load_state():return _snap_state({})
def run_handler():
    """fallback for a gradio without gr.Timer: one streaming request"""
    start_run();last={};time.sleep(.5)
    while True:
        t=RUN_THREAD["t"];alive=t is not None and t.is_alive()
        yield snapshot(last)
        if not alive:break
        time.sleep(3.0)
    STATE["fig_version"]+=1;last.pop("files",None)
    yield snapshot(last)
def page_load():return snapshot({})
def _tb(**kw):
    for extra in (([{"buttons":["copy"]}] if _GR_MAJOR>=6 else [])+[{"show_copy_button":True},{}]):
        try:return gr.Textbox(**extra,**kw)
        except TypeError:continue
def _gallery(**kw):
    try:return gr.Gallery(columns=1,height="auto",object_fit="contain",preview=False,**kw)
    except TypeError:return gr.Gallery(**kw)
def _on(ev,fn,inputs,outputs,limit,quiet=False):
    for kw in (([dict(concurrency_limit=limit,show_progress="hidden")] if quiet else [])+[dict(concurrency_limit=limit),{}]):
        try:return ev(fn,inputs=inputs,outputs=outputs,**kw)
        except TypeError:continue
def build_ui():
    blocks=gr.Blocks(title=APP_SHORT) if _GR_MAJOR>=6 else gr.Blocks(css=CSS,title=APP_SHORT)
    with blocks as demo:
        gr.HTML(hero_html());mode=gr.HTML(mode_html())
        run_b=gr.Button("RUN",variant="primary",elem_id="kz_run")
        stg=gr.HTML(stages_html())
        con=_tb(lines=12,max_lines=20,label="Live engine output of this RUN — every line the TEST815 engine prints (TEST815 | line); progress bars update one line; also ENGINE_OUTPUT_REALTIME.log",value=console_text(),interactive=False)
        fstat=gr.HTML(_safe(figs_status_html));main_figs=gr.HTML(_safe(figs_main_html))
        jpgs=gr.File(label="The JPEG figures of this RUN, in order — each file downloads with one tap",value=(jpg_files() or None),file_count="multiple",interactive=False)
        files=gr.File(label="Real-time engine output, session log, engine records (results, manifest, log, review CSV, public audit), verification — direct downloads (no ZIP)",value=(all_files() or None),file_count="multiple",interactive=False)
        htmls={};gals={}
        with gr.Tabs():
            for t in TABS:
                with gr.Tab(t):
                    if t in TAB_HTML:htmls[t]=gr.HTML(_safe(TAB_HTML[t]))
                    gals[t]=_gallery(label=f"{t} · figures",value=tab_gallery(t))
        gr.HTML(f'<div class="kz small" style="opacity:.8;margin:10px 0 18px">{esc(AUTHOR)} · {esc(ORG)} · {esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · '
                f'<a href="{file_url(EVID_DIR/ENGINE_NAME)}" download="815.py">815.py (the locked copy executed here)</a> · <a href="{URL_LICENSE}" target="_blank" rel="noopener">LICENSE</a> · '
                'Source articles: PLOS Computational Biology (doi:10.1371/journal.pcbi.1010476) and PLOS ONE (doi:10.1371/journal.pone.0272845) via Europe PMC — linked, hash-recorded, not redistributed · '
                'Qwen2.5-72B-Instruct and third-party libraries remain under their own licences.</div>')
        outs=[mode,stg,con]+[htmls[t] for t in TAB_HTML]+[gals[t] for t in TABS]+[files,jpgs,fstat,main_figs]
        if _HAS_TIMER:
            ui_state=gr.State({});timer=gr.Timer(3.0)
            _on(run_b.click,run_click,[ui_state],outs+[ui_state],8)
            _on(timer.tick,ui_tick,[ui_state],outs+[ui_state],8,quiet=True)
            try:demo.load(page_load_state,inputs=None,outputs=outs+[ui_state])
            except Exception:pass
        else:
            _on(run_b.click,run_handler,None,outs,8)
            try:demo.load(page_load,inputs=None,outputs=outs)
            except Exception:pass
    try:demo.queue(default_concurrency_limit=8)
    except TypeError:
        try:demo.queue(concurrency_count=8)
        except TypeError:demo.queue()
    return demo

_GR_MAJOR=int(re.match(r"\d+",gr.__version__).group())
GRADIO_LINK=DEMO_ROOT/"GRADIO_LINK.txt"
demo=None
def launch_interface():
    """(re)opens the interface of THIS session (public link first, Colab port window as fallback); nothing is recomputed.
    If the link stops working, run  launch_interface()  in a new cell."""
    global demo
    try:demo.close()
    except Exception:pass
    demo=build_ui()
    kw=dict(share=True,allowed_paths=[str(DEMO_ROOT)],show_error=True,inline=False,prevent_thread_lock=True,debug=False)
    if _GR_MAJOR>=6:kw["css"]=CSS
    err=None
    for _ in range(7):
        try:demo.launch(**kw);break
        except TypeError as ex:
            bad=next((k for k in ("css","prevent_thread_lock","allowed_paths","debug") if k in str(ex) and k in kw),None)
            if bad is None:raise
            kw.pop(bad)
        except Exception as ex:
            if not kw.get("share"):raise
            err=f"{type(ex).__name__}: {ex}";kw["share"]=False;slog("LAUNCH_NOTE","public share link not available — opening the local interface",error=err)
    share=getattr(demo,"share_url",None);local=getattr(demo,"local_url",None);window=None
    if not share:
        try:
            from google.colab import output as _co
            port=int(re.search(r":(\d+)",str(local)).group(1));_co.serve_kernel_port_as_window(port,anchor_text="▶ Open the AKBASCORE TEST815 interface (Colab window)");window=f"Colab port window, port {port}"
        except Exception as ex:window=f"not available ({type(ex).__name__})"
    dump_json(GRADIO_LINK.with_suffix(".json"),dict(utc=utc_now(),session=SESSION_ID,share_url=share,local_url=local,colab_window=window,share_error=err))
    GRADIO_LINK.write_text(f"{share or local}\n",encoding="utf-8")
    banner(f"INTERFACE OPEN · {share or ('local only: '+str(local))}\n  public link : {share or ('— (tunnel not available'+(': '+str(err)[:120] if err else '')+'; use the Colab window link above)')}\n  local       : {local}\n"
           f"  Press RUN in the interface — everything else runs automatically. If the link stops working: run  launch_interface()  in a new cell.","#")
    slog("LAUNCH","interface open",share_url=share,local_url=local,colab_window=window);return share or local
def keep_cell_running():
    """keeps this Colab cell RUNNING while the interface is in use; when a RUN has finished its figures are shown here too"""
    banner("THE CELL STAYS RUNNING — the interface is live. Press RUN in the interface; the engine output is printed here and shown in the interface.\n"
           f"  A full RUN takes about 40–60 minutes on an A100. Stop this cell (■) only when you have finished; the files stay in {DEMO_ROOT}","#")
    shown=set()
    try:
        while True:
            time.sleep(5)
            t=RUN_THREAD["t"]
            if t is not None and not t.is_alive() and SESSION_ID not in shown:
                shown.add(SESSION_ID);show_figures_in_cell()
    except KeyboardInterrupt:pass
    finally:slog("CELL_STOPPED","the cell was stopped by the user")
def show_figures_in_cell(download=True):
    """second, independent channel: the JPEG figures of THIS run are shown in the Colab cell and each is offered as a browser
    download. Can also be called by hand in a new cell:  show_figures_in_cell()"""
    keys=[k for k in FIGURES if k in FIG_FILES]
    banner(f"FIGURES OF THIS RUN ({SESSION_ID}) — {len(keys)} JPEG file(s) — shown below in the cell, each also downloaded by the browser\n  folder: {FIG_DIR}","#")
    try:from IPython.display import display,Image as _IImg,HTML as _IHTML
    except Exception as ex:slog("CELL_FIGURES","IPython display not available",error=f"{type(ex).__name__}: {ex}");return
    for k in keys:
        f=FIG_FILES[k];nm=Path(f["jpg"]).name
        try:
            display(_IHTML(f"<div style='font:600 15px sans-serif;margin:14px 0 4px'>{esc(_figlabel(k))} · {esc(f['badge'])} · {esc(nm)} · SHA-256 {esc(f['sha256_jpg'][:16])}…</div>"))
            display(_IImg(filename=f["jpg"],width=1100))
        except Exception as ex:slog("CELL_FIGURES",f"{k} could not be shown in the cell",error=f"{type(ex).__name__}: {ex}")
    if not download:return
    try:from google.colab import files as _cf
    except Exception:slog("CELL_FIGURES","not in Colab — browser download from the cell skipped; the files are in the folder above");return
    for k in keys:
        f=FIG_FILES[k]
        try:_cf.download(f["jpg"]);slog("CELL_DOWNLOAD",Path(f["jpg"]).name);time.sleep(1.0)
        except Exception as ex:slog("CELL_DOWNLOAD",f"{Path(f['jpg']).name} not downloaded",error=f"{type(ex).__name__}: {ex}")

# ---------------------------------------------------------------------------------------------------------------------
# START-UP (no GPU use): locked sources verified, then the interface opens
# ---------------------------------------------------------------------------------------------------------------------
def startup():
    banner(f"{APP_NAME} · {EXPERIMENT} · start-up {local_now()} · session {SESSION_ID}"+("\nSIMULATION — NOTHING HERE IS AN EXPERIMENTAL RESULT" if SIM else ""))
    for n in LOCKS:RAW[n]=fetch_locked(n);slog("LOCKED_SOURCE",n,git_blob=SOURCES[n]["git_blob"],bytes=SOURCES[n]["bytes"],obtained=SOURCES[n]["obtained"],**({"notes":SOURCES[n]["notes"]} if SOURCES[n].get("notes") else {}))
    slog("ENGINE_READY","815.py locked; it runs unchanged as one OS process when RUN is pressed",git_blob=LOCKS[ENGINE_NAME])
_AKB815_PARTS.add(4)
_missing=[n for n in (1,2,3) if n not in _AKB815_PARTS]
if _missing:raise RuntimeError(f"PART {_missing} of the program is missing in this cell — paste PART 1, 2, 3 and 4 one below the other, each completely (every part ends with an END OF PART line)")
try:startup()
except Exception as _ex:
    _m=str(_ex)
    _hint=("No copy with the locked git blob was found, not even the embedded one: paste PART 1, 2, 3 and 4 again exactly as delivered (nothing "
           "cut off or edited), then run the cell again. The program stops instead of running unverified code." if "NOT AVAILABLE" in _m else
           "Network error while downloading a locked source from GitHub: run the cell again." if any(x in _m for x in ("URLError","timed out","HTTP Error","Connection","Name or service")) else
           "See the traceback above; nothing was run.")
    banner(f"START-UP FAILED — {type(_ex).__name__}: {_m}\nWHAT TO DO: {_hint}\nRecords of this attempt: {SESSION_DIR}","!")
    raise
launch_interface()
if os.environ.get("AKB815_NO_BLOCK")!="1":keep_cell_running()
# ===== END OF PART 4/4 =====
