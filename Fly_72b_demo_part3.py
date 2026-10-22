# ===== PART 3/3 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 3 — Gradio interface (Silicon Hippocampus 1.5 design): ONE button (RUN). Before RUN only the earlier run is shown,
#              labelled RECORD (it holds no text). RUN starts the unchanged 745.py; the stages, the engine's own output, the
#              sealed cartridges and every text it writes appear while it works. The interface never edits an output.
# =====================================================================================================================
LINEAGE=[("Research Record I — Qwen2.5-7B","https://doi.org/10.5281/zenodo.23381336"),
         ("Research Record II — Mistral-7B, Silicon Hippocampus v1.4","https://doi.org/10.5281/zenodo.23418927"),
         ("Research Record III — Qwen2.5-72B, Direct Internal-State Injection","https://doi.org/10.5281/zenodo.23434686"),
         ("Zenodo record 23497732 (link given by the author)",ZENODO)]
def esc(x):return html.escape(str(x))
def card(title,body,kind="info"):return f'<div class="kz card {kind}"><div class="h">{esc(title)}</div><div class="small">{body}</div></div>'
def chip(cid):c=ccol(cid);return f'<span class="chip" style="color:#fff;background:{c};border-color:{c}">{esc(cid)}</span>'
def ok_mark(v):return "<b style='color:#08785B'>PASS</b>" if v else ("<b style='color:#B91C1C'>FAIL</b>" if v is False else "<span style='opacity:.6'>—</span>")
class Markup(str):pass
def tbl(rows,head=None,mono_cols=()):
    h="".join(f"<th>{esc(x)}</th>" for x in head) if head else ""
    b="".join("<tr>"+"".join(f"<td class='{'mono' if i in mono_cols else ''}'>{v if isinstance(v,Markup) else esc(v)}</td>" for i,v in enumerate(r))+"</tr>" for r in rows)
    return f"<table class='tbl'>{('<tr>'+h+'</tr>') if h else ''}{b}</table>"
def pre(text,maxh=420):return f"<div class='ans' style='max-height:{maxh}px'>{esc(text)}</div>"
def details(summary,inner,open_=False):return f"<details{' open' if open_ else ''}><summary>{summary}</summary>{inner}</details>"
def textblock(title,text,note="",open_=False,maxh=460):
    if text is None:return details(f"{esc(title)} · <i>not written yet in this RUN</i>","")
    return details(f"{esc(title)} · {len(text):,} characters · SHA-256 {sha_text(text)[:12]}…"+(f" · {esc(note)}" if note else ""),pre(text,maxh),open_)

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
.chip{display:inline-block;border:1px solid;border-radius:3px;padding:0 6px;font-size:12px;font-weight:700;white-space:nowrap}
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
    c=REC.get("completed") or {}
    tiles=[("C01–C03","source cartridges (one report)"),("S · H","6 synthesis cartridges"),("8","closed-loop rounds"),("C11","blind MASTER, sealed"),("C12","post-outcome MASTER"),("PENDING","human review")]
    return (f'<div class="kz hero"><span class="rec">Live research demonstration · frozen Qwen2.5-72B-Instruct · NF4 · BF16 · CUT3 · A100 80 GB</span>'
            f'<div class="brand">{esc(APP_NAME)}</div><div class="title">{esc(APP_SUB)}</div>'
            '<div class="by">An AI is given the official, not yet concluded investigation data of a real accident (Air Tractor AT-802A OR-2025, 13 November 2025, AIN Croatia). '
            'Without changing its weights, the information is written into physical memory cartridges, read back, synthesized, reviewed in eight closed-loop rounds and sealed '
            'as the blind MASTER C11 — before the official final report is opened. Only then the final report is read, the model audits itself, and C12 is formed.</div>'
            '<div class="tiles">'+"".join(f'<div class="tile"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a,b in tiles)+'</div>'
            f'<div class="by"><b>{esc(AUTHOR)}</b> · {esc(ORG)} · {esc(PLACE)} · {esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · <a href="{REPO}" target="_blank" rel="noopener">{esc(REPO)}</a></div></div>')
def mode_html():
    st=STATE
    if SIM:kind,t="err","SIMULATION — code test of the author with a fake engine, NOT an experimental result"
    elif st.get("running"):
        el=(time.time()-datetime.fromisoformat(st["started"]).timestamp())/60 if st.get("started") else 0
        kind,t="info",f"RUN IN PROGRESS · {el:.0f} min · stage {list(STAGES).index(st['current'])+1 if st.get('current') else '…'}/{len(STAGES)}: {STAGES.get(st.get('current'),'')}"
    elif st.get("finished"):
        ok=run_verdict().startswith("COMPLETE");kind,t=("on" if ok else "err"),f"RUN {SESSION_ID} — {run_verdict()}"
    else:kind,t="info","NOT STARTED — press RUN. The unchanged TEST745 engine runs on the GPU (about 1.5 hours); everything it does appears here while it works."
    rc=REC.get("completed") or {}
    return card(t,f"Earlier completed run (RECORD, 745.log): C11 {esc(rc.get('C11','')[:16])}… · C12 {esc(rc.get('C12','')[:16])}… · {rc.get('seconds',0):,.0f} s — shown only for comparison; "
                "it contains no generated text and is never presented as a result of this RUN.",kind)
def stages_html():
    out=[];n=len(STAGES);done=0
    for i,(k,title) in enumerate(STAGES.items(),1):
        s=STATE["stages"][k];stt=s["status"];mk={"done":"✓","run":"▶","fail":"✗","skip":"–","wait":"○"}[stt]
        if stt in("done","skip","fail"):done+=1
        tm=f" · {s['seconds']:.0f} s" if s.get("seconds") is not None else ""
        out.append(f"<div class='stg {stt}'>{mk} {i}/{n} · {esc(title)}{tm}"+(f"<span class='nt'>{esc(s['note'])}</span>" if s.get("note") else "")+"</div>")
    pc=100*done/n
    bar=f'<div style="margin-top:6px;background:#e5e7eb;height:10px;border-radius:2px"><div style="width:{pc:.0f}%;height:10px;background:#7626D9;border-radius:2px"></div></div>'
    head=f"RUN {SESSION_ID} · {run_verdict()}"+(f" · started {STATE['started'][11:19]} UTC" if STATE.get("started") else "")+(f" · finished {STATE['finished'][11:19]} UTC" if STATE.get("finished") else "")
    return card(head,"".join(out)+bar,"m")
def console_text():
    with _LOG_LOCK:return "\n".join(list(CONSOLE)[-180:])

# ---------------------------------------------------------------------------------------------------------------------
# tab contents — texts are read from THIS RUN's experiment directory, unedited
# ---------------------------------------------------------------------------------------------------------------------
def overview_html():
    E_=_ents();R=run_results()
    steps=[("Official, not yet concluded investigation data","the AIN preliminary report (PDF) is downloaded and checked; the final report is NOT downloaded",check_ok("FINAL_REPORT_NOT_DOWNLOADED_BEFORE_C11")),
           ("Written into physical memory — weights unchanged","three consecutive parts of the one preliminary report → C01, C02, C03 (H3 + K/V of layers 0–3 on the SSD)",all(c in E_ for c in SRC) or None),
           ("Read back from the cartridges","each cartridge mounted alone (80 layers rebuilt) and read by the frozen model",check_ok("GENERATION_NOT_TRUNCATED_C03")),
           ("Synthesized into new physical memories","readouts → text synthesis → S01–S03 → read again → H01–H03",all(c in E_ for c in SUB+CRS) or None),
           ("Eight closed-loop review rounds","initial hypothesis + 8 rounds, no official outcome available",(len(R.get("blind_rounds") or [])==8) or None),
           ("Blind MASTER C11 sealed","SHA-256 sealed and answered three questions before the final report is opened",check_ok("C11_LOCKED_BEFORE_FINAL")),
           ("Official final report opened — only now","downloaded after the C11 seal; the model compares and audits itself",check_ok("AUDIT_NOT_TRUNCATED")),
           ("C12 post-outcome MASTER","new cartridge, parent = C11 SHA-256; C11 unchanged; human review PENDING",check_ok("C12_PARENT_SHA"))]
    rows=[(Markup(f"<b>{i}. {esc(a)}</b><br><span class='small' style='opacity:.85'>{esc(b)}</span>"),Markup(ok_mark(v))) for i,(a,b,v) in enumerate(steps,1)]
    cl=[]
    for t,kind,f in CLAIMS:
        try:v=f()
        except Exception:v=None
        cl.append((t,kind,Markup(ok_mark(v) if kind=="technical" else "<b style='color:#B45309'>NOT EVALUATED</b>")))
    arch=card("Physical memory outside the frozen model — what it is and what it is not",
        "<b>What is stored:</b> internal states of the frozen Qwen2.5-72B — the layer-3 output H3 and the K/V of layers 0–3 — written to a file on the SSD, hashed, reloaded, injected at the "
        "layer-3 boundary and used to forge new cartridges.<br><b>Not text RAG:</b> no document text is pasted into the prompt at question time; the model reads its own stored states. "
        "<br><b>Not fine-tuning:</b> the weights are frozen (weight sentinel checked).<br><b>Not a removal of the transformer:</b> layers 4–79 and decoding still run every time; "
        "the early layers are reused from the stored states. TEST745 does not show that most of the transformer computation is eliminated.<br><b>Synthesis is text-mediated:</b> "
        "cartridges are combined through the model's written readouts, never by direct BF16 tensor fusion.","info")
    lin=card("Research lineage (published records — not results of this experiment)","<br>".join(f"{esc(t)} · <a href='{u}' target='_blank' rel='noopener'>{esc(u)}</a>" for t,u in LINEAGE)+
             f"<br>Silicon Hippocampus 1.5 demonstration (infrastructure of this interface): <a href='{URL_15}' target='_blank' rel='noopener'>Qwen72B_1.5.log</a>"+
             f"<br>This experiment: TEST745 — <a href='{URL_745}' target='_blank' rel='noopener'>745.py</a> · <a href='{URL_745LOG}' target='_blank' rel='noopener'>745.log</a>","info")
    return (card(f"What happens in this RUN ({SESSION_ID})",tbl(rows,["step","this RUN"]),"m")+
            card("What this RUN can show — and what needs independent evaluation",tbl(cl,["claim","kind","status"])+
                 "<div class='small' style='margin-top:4px'>An experimental demonstration of a working, researchable memory architecture — not a finished general AI system. "
                 "The model's self-audit is its own claim; no independent expert grading exists yet (human review PENDING).</div>","warn")+arch+lin)
def sources_html():
    R=run_results();al=R.get("ain_links") or {};pr=R.get("preliminary") or {};lv=R.get("preliminary_leakage_review") or {}
    rows=[("case page (link directory only, never model input)",al.get("case_url") or P745.get("CASE_URL")),("case page SHA-256 (quarantined)",al.get("case_page_sha256_quarantined")),
          ("preliminary report URL",pr.get("url") or al.get("preliminary_url")),("preliminary PDF SHA-256",pr.get("pdf_sha256")),("pages",pr.get("pages")),("retrieved",pr.get("retrieved")),
          ("final report URL (sealed, NOT fetched before C11)",al.get("final_url_sealed_not_fetched")),("leakage guard",f"{len(lv.get('mentions') or [])} generic mentions reviewed · "+("PASS" if check_ok("PRELIMINARY_OUTCOME_LEAKAGE_GUARD") else "—"))]
    segs="".join(textblock(f"{c} — part {i+1}/3 of the ONE preliminary report (forged text)",raw_of(f"{c}_FORGED.txt"),f"{(R.get('sources',{}).get(c) or {}).get('forged_tokens','—')} tokens") for i,c in enumerate(SRC))
    if not R:return card("Official sources","Not available yet — the engine records the AIN links and the preliminary report during RUN (stage 3).","info")
    return (card("AIN — official investigation sources of this RUN",tbl(rows,mono_cols=(1,)),"info")+
            card("C01 · C02 · C03 — three consecutive parts of ONE preliminary report (not three independent reports)",segs+textblock("full text extracted from the preliminary PDF",raw_of("AIN_PRELIMINARY_EXTRACT.txt")),"m"))
def cart_html():
    E_=_ents();V=(LIVE.get("verification") or {}).get("cartridges") or {}
    if not E_:return card("Physical cartridges","No cartridge sealed yet in this RUN.","info")
    rows=[]
    for c in CARTS:
        e=E_.get(c);v=V.get(c) or {}
        if not e:rows.append((Markup(chip(c)),"not produced yet","","","","","",""));continue
        par=", ".join(f"{p['id']} {p['sha256'][:10]}…" for p in e.get("parents") or []) or "—"
        rows.append((Markup(chip(c)),e.get("role"),par,f"{e['body_tokens']:,}",f"{e.get('forge_seconds')} s",e["sha256"],
                     Markup(f"file {ok_mark(v.get('file_sha_ok'))} · tensors {ok_mark(v.get('tensor_seal_ok'))} · body {ok_mark(v.get('body_sha_ok'))}" if v else "after the run"),
                     Markup(("= RECORD" if v.get("equal_to_record") else ("≠ RECORD" if v.get("equal_to_record") is False else "—")))))
    return card(f"Physical CUT3 cartridges of this RUN — {len(E_)}/11 sealed",tbl(rows,["id","role","parents (file SHA-256)","body tokens","forge","file SHA-256","re-verification","vs earlier run"],mono_cols=(5,)),"m")+\
           card("Order of creation","C01 → C02 → C03 → S01 → S02 → S03 → H01 → H02 → H03 → C11 → C12 (manifest timestamps: "+", ".join(f"{c} {str(E_[c].get('created',''))[11:19]}" for c in CARTS if c in E_)+")","info")
def synth_html():
    gi=generation_index();out=[]
    for g in gi:
        if g["cid"] in("INITIAL","C11"):continue
        out.append(textblock(f"{g['cid']} · {g['role']}",text_of(g["file"]),f"{g.get('tokens','—')} tokens"))
    return card("Readouts and syntheses of this RUN, in the order they were written (unedited)","".join(out) or "none yet","m")+\
           card("Programmed prompts of 745.py (unchanged)","".join(details(esc(k),pre(v,240)) for k,v in (P745.get("prompts") or {}).items()),"info")
def loop_html():
    rt=round_texts();M=LIVE.get("loop") or {}
    head=("Observational measures (no quality score): "+" · ".join(f"{l}: {t or '—'} tok, similarity to previous {s if s is not None else '—'}, open uncertainties {u if u is not None else '—'}"
          for l,t,s,u in zip(M.get("labels",[]),M.get("tokens",[]),M.get("similarity_to_previous",[]),M.get("open_uncertainty_items",[])))) if M else "Measures are computed after the run (Figure 4)."
    return card("Closed loop — initial blind hypothesis and the eight review rounds of this RUN (unedited)",esc(head)+"".join(textblock(l if l!="INITIAL" else "INITIAL blind hypothesis",t,
                "written to C11" if l=="R8" else "",open_=(l in("INITIAL","R8"))) for l,t in rt),"m")
def blind_html():
    R=run_results();E_=_ents();seal=R.get("C11_seal") or {};c11=E_.get("C11")
    body=None
    if c11 and text_of("blind_round_08.txt") is not None and all(k in E_ for k in CRS):body=blind_body_from(E_,text_of("blind_round_08.txt"))
    out=card("C11 BLIND MASTER",(f"file SHA-256 <span class='mono'>{esc(c11['sha256'])}</span> · {c11['body_tokens']:,} tokens · sealed at {esc(seal.get('sealed_at','—'))} · "
             f"blind answers SHA-256 <span class='mono'>{esc(str(seal.get('blind_answers_sha256'))[:16])}…</span> · C11 locked before final: {ok_mark(check_ok('C11_LOCKED_BEFORE_FINAL'))}" if c11 else "not sealed yet in this RUN")+
             (textblock("C11 body (re-derived with the exact 745.py expression)",body) if body else ""),"m")
    qa="".join(card(f"Q{i+1} · {x['question']}",pre(x["answer"],460),"m") for i,x in enumerate(R.get("blind_answers") or []))
    return out+(qa or card("Blind answers","not written yet in this RUN","info"))
def outcome_html():
    R=run_results();off=R.get("official_outcome") or {};sa=(R.get("self_audit") or {}).get("text")
    if not off:return card("Official outcome","Embargoed — the AIN final report is downloaded only after C11 has been sealed (stage 11).","warn")
    rows=[("final report URL",off.get("url")),("PDF SHA-256",off.get("pdf_sha256")),("pages",off.get("pages")),("retrieved",off.get("retrieved")),("unlocked (engine)",line_time(r"^OFFICIAL_OUTCOME_UNLOCK"))]
    return (card("AIN final report — opened after the C11 seal",tbl(rows,mono_cols=(1,))+textblock("evaluation excerpt given to the model (as built by 745.py)",raw_of("AIN_FINAL_EVALUATION_EXCERPT.txt"))+
                 textblock("full text extracted from the final report PDF",raw_of("AIN_FINAL_EXTRACT.txt")),"info")+
            card("Model self-audit after the official report — the model's own claim, NOT independent expert grading",pre(sa,640) if sa else "not written yet","warn"))
def c12_html():
    R=run_results();E_=_ents();c12=E_.get("C12");V=LIVE.get("verification") or {};lin=V.get("lineage") or {}
    if not c12:return card("C12 POST-OUTCOME MASTER","not sealed yet in this RUN","info")
    body=c12body_from(E_,R,(R.get("self_audit") or {}).get("text")) if R.get("self_audit") and R.get("C11_seal") and R.get("official_outcome") else None
    rows=[("C12 file SHA-256",c12["sha256"]),("parent",", ".join(f"{p['id']} {p['sha256']}" for p in c12.get("parents") or [])),("role",c12.get("role")),("body tokens",c12.get("body_tokens")),
          ("C11 immutable (engine)",Markup(ok_mark(check_ok("C11_IMMUTABLE")))),("C12 parent SHA (engine)",Markup(ok_mark(check_ok("C12_PARENT_SHA")))),("weights unchanged (engine)",Markup(ok_mark(check_ok("FROZEN_SENTINEL_UNCHANGED")))),
          ("C11 file re-hashed now (demo)",Markup(ok_mark(_v("C11").get("file_sha_ok")))),("C12 body re-derived = manifest (demo)",Markup(ok_mark(_v("C12").get("body_sha_ok")))),("C12 parent link (demo)",Markup(ok_mark(lin.get("c12_parent_is_c11"))))]
    return card("C12 POST-OUTCOME MASTER — human review PENDING (not a human-approved cartridge)",tbl(rows,mono_cols=(1,))+(textblock("C12 body (re-derived with the exact 745.py expression)",body) if body else ""),"m")
def verif_html():
    rows=[(c["utc"][11:19],c.get("stage") or "",c["name"],Markup(ok_mark(c["passed"])),c["detail"][:140]) for c in CHECKS]
    rec=[(c,(REC["sealed"].get(c) or {}).get("sha256","—"),(_v(c).get("sha256_now") or "—"),Markup(ok_mark(_v(c).get("equal_to_record")) if _v(c) else "—")) for c in CARTS]
    src=[(n,v["git_blob"],v["sha256"],f"{v['bytes']:,}") for n,v in SOURCES.items()]
    V=LIVE.get("verification") or {}
    return (card(f"Engine checks of this RUN — {sum(c['passed'] for c in CHECKS)}/{len(CHECKS)} PASS (time = receipt of the engine line)",tbl(rows,["UTC","stage","check","result","detail"],mono_cols=(4,)) if rows else "none yet","on" if rows and all(c["passed"] for c in CHECKS) else "info")+
            card("Independent re-verification after the run (read-only)",(pre(json.dumps(jsafe(V.get("lineage")),indent=1),220)+("PROBLEMS: "+esc(", ".join(V.get("problems"))) if V.get("problems") else "no problem found")) if V else "after the engine has finished","info")+
            card("This RUN vs the earlier completed run (RECORD, 745.log) — comparison only",tbl(rec,["cartridge","earlier run (RECORD)","this RUN","equal"],mono_cols=(1,2)),"info")+
            card("Locked sources (git blob verified)",tbl(src,["file","git blob","SHA-256","bytes"],mono_cols=(1,2)),"info"))

TABS=["OVERVIEW","OFFICIAL SOURCES","PHYSICAL CARTRIDGES","HIERARCHICAL SYNTHESIS","CLOSED LOOP","BLIND C11","OFFICIAL OUTCOME","C12 MASTER","VERIFICATION","SCIENTIFIC FIGURES"]
TAB_HTML={"OVERVIEW":overview_html,"OFFICIAL SOURCES":sources_html,"PHYSICAL CARTRIDGES":cart_html,"HIERARCHICAL SYNTHESIS":synth_html,"CLOSED LOOP":loop_html,"BLIND C11":blind_html,
          "OFFICIAL OUTCOME":outcome_html,"C12 MASTER":c12_html,"VERIFICATION":verif_html}
def tab_gallery(tab):
    keys=[k for k,m in FIGURES.items() if (m["tab"]==tab or tab=="SCIENTIFIC FIGURES") and k in FIG_FILES]
    return [(FIG_FILES[k]["jpg"],f"Figure {FIGURES[k]['n']} — {FIGURES[k]['title']} · {FIG_FILES[k]['badge']}") for k in keys]
def figs_status_html():
    n=len(FIG_FILES);tot=len(FIGURES)
    if not n and not FIG_ERRORS:return card(f"Scientific figures of this RUN — 0/{tot}","The six figures are drawn from this RUN's outputs after the engine has finished (stage 14). They appear here, one below the other.","info")
    def st(k):
        f=FIG_FILES.get(k)
        if not f:return "NOT GENERATED: "+str(FIG_ERRORS.get(k,"pending"))
        q=f.get("layout_qc") or {};j=f.get("jpeg_qc") or {}
        return f"{f['badge']} · {f['pixels'][0]}×{f['pixels'][1]} JPEG 300 dpi · layout QC {'PASS' if q.get('passed') else 'FAIL'} · JPEG QC {'PASS' if j.get('passed') else 'FAIL'}"
    rows="".join(f"<div class='small'>{'✓' if k in FIG_FILES and (FIG_FILES[k].get('layout_qc') or {}).get('passed') and FIG_FILES[k]['badge']!='NOT PRODUCED IN THIS RUN' else '✗'} Figure {esc(m['n'])} — {esc(m['title'])} · <b>{esc(st(k))}</b></div>" for k,m in FIGURES.items())
    ok=n==tot and all((v.get("layout_qc") or {}).get("passed") and v["badge"]!="NOT PRODUCED IN THIS RUN" for v in FIG_FILES.values())
    return card(f"Scientific figures of this RUN ({SESSION_ID}) — {n}/{tot} written",rows,"on" if ok else "warn")
from urllib.parse import quote as _urlquote   # NOTE: part 2 defines its own text helper quote(text,n); the URL quote must not be that one
# relative URLs (no leading "/"): they resolve against the page itself, so they work through the public share link,
# the Colab port window and any proxy root path alike
def file_url(p):return ("gradio_api/file=" if _GR_MAJOR>=5 else "file=")+_urlquote(str(p),safe="/")
def file_url_alt(p):return ("file=" if _GR_MAJOR>=5 else "gradio_api/file=")+_urlquote(str(p),safe="/")
def figs_main_html():
    """the six figures of THIS run, in order — each with its own direct JPEG download link below it"""
    if not FIG_FILES:return card("Figures","No figure of this RUN yet (figures of an earlier RUN are never shown).","info")
    keys=[k for k in FIGURES if k in FIG_FILES];out=[]
    bulk=("<a href='#' onclick=\"var l=document.querySelectorAll('a.kz-dl');for(var i=0;i<l.length;i++){(function(a,d){setTimeout(function(){a.click()},d)})(l[i],i*900)};return false;\">"
          f"<b>⬇ Download all {len(keys)} figures (JPEG), one after another</b></a>")
    out.append(card("Direct downloads — no ZIP",f"{bulk}<br><span class='small'>The browser downloads the JPEG files in order (Figure 1 → Figure 6). Some browsers ask once to "
                    "“allow multiple downloads”; if blocked, use the link under each figure or the JPEG file list below — every file downloads with one tap.</span>","on"))
    for k in keys:
        f=FIG_FILES[k];m=FIGURES[k];u=file_url(f["jpg"]);ua=file_url_alt(f["jpg"]);nm=Path(f["jpg"]).name;qc=(f.get("layout_qc") or {}).get("passed") and f["badge"]!="NOT PRODUCED IN THIS RUN"
        out.append(f"<div class='kz card {'on' if qc else 'err'}'><div class='h'>Figure {esc(m['n'])} — {esc(m['title'])} · {esc(f['badge'])}"+("" if (f.get("layout_qc") or {}).get("passed") else " · LAYOUT QC FAIL")+"</div>"
                   f"<img src='{u}' data-alt='{ua}' onerror=\"if(!this.dataset.done){{this.dataset.done=1;this.src=this.dataset.alt;var a=this.parentNode.querySelector('a.kz-dl');if(a)a.href=this.dataset.alt;}}\" "
                   f"style='width:100%;height:auto;border:1px solid #d1d5db' alt='Figure {esc(m['n'])}'>"
                   f"<div class='small' style='margin-top:4px'><a class='kz-dl' href='{u}' download='{esc(nm)}'><b>⬇ Download Figure {esc(m['n'])} (JPEG, {f['pixels'][0]}×{f['pixels'][1]}, 300 dpi)</b></a> · "
                   f"<span class='mono'>{esc(nm)} · SHA-256 {esc(f['sha256_jpg'][:16])}…</span></div></div>")
    return "".join(out)
def jpg_files():return [FIG_FILES[k]["jpg"] for k in FIGURES if k in FIG_FILES]
def _safe(fn):
    try:return fn()
    except Exception as ex:return card("Display error",f"<code>{esc(type(ex).__name__)}: {esc(ex)}</code> — the records are unaffected","err")
def all_files():return [p for _,p in download_items()]
def snapshot(last):
    """full output tuple; html parts are rebuilt only when the state changed, figures only when they changed"""
    v=STATE["version"];fv=STATE["fig_version"];out=[_safe(mode_html),_safe(stages_html),console_text()]
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
# The page is refreshed by SHORT polling requests (gr.Timer, every 3 s, per browser tab) instead of one 1.5-hour streaming
# request: a long stream through the share tunnel can be dropped (phone asleep, tab in background, tunnel reconnect) and then
# the page silently stops updating — that is how the six figures of the first A100 run never reached the page.
# With polling, every tick is a new request: after any interruption the next tick (or a page reload) shows the full state,
# figures included. The RUN thread itself never depends on the browser.
_HAS_TIMER=hasattr(gr,"Timer") and hasattr(gr,"State")
def _snap_state(last):
    last=dict(last) if isinstance(last,dict) else {}
    return (*snapshot(last),last)
def run_click(last):
    start_run();time.sleep(.5);return _snap_state({})
def ui_tick(last):return _snap_state(last)
def page_load_state():return _snap_state({})
def run_handler():
    """fallback for a gradio without gr.Timer: one streaming request (the earlier behaviour)"""
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
        con=_tb(lines=12,max_lines=20,label="Live engine output of this RUN — every line as 745.py prints it (time · stage · line); also ENGINE_OUTPUT_REALTIME.log and SESSION.log",value=console_text(),interactive=False)
        fstat=gr.HTML(_safe(figs_status_html));main_figs=gr.HTML(_safe(figs_main_html))
        jpgs=gr.File(label="The six JPEG figures of this RUN, in order — each file downloads with one tap",value=(jpg_files() or None),file_count="multiple",interactive=False)
        files=gr.File(label="Real-time engine output, logs, verification, all texts written by the engine, manifests — direct downloads (no ZIP)",value=(all_files() or None),file_count="multiple",interactive=False)
        htmls={};gals={}
        with gr.Tabs():
            for t in TABS:
                with gr.Tab(t):
                    if t in TAB_HTML:htmls[t]=gr.HTML(_safe(TAB_HTML[t]))
                    gals[t]=_gallery(label=f"{t} · figures",value=tab_gallery(t))
        gr.HTML(f'<div class="kz small" style="opacity:.8;margin:10px 0 18px">{esc(AUTHOR)} · {esc(ORG)} · {esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · '
                f'<a href="{URL_745}" target="_blank" rel="noopener">745.py</a> · <a href="{URL_745LOG}" target="_blank" rel="noopener">745.log</a> · <a href="{URL_709}" target="_blank" rel="noopener">709.py</a> · '
                f'<a href="{URL_730}" target="_blank" rel="noopener">730.py</a> · <a href="{URL_LICENSE}" target="_blank" rel="noopener">LICENSE</a> · AIN reports © Air Accident Investigation Agency, Croatia (ain.hr) · '
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
    kw=dict(share=True,allowed_paths=[str(DEMO_ROOT),str(_CROOT)],show_error=True,inline=False,prevent_thread_lock=True,debug=False)
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
            port=int(re.search(r":(\d+)",str(local)).group(1));_co.serve_kernel_port_as_window(port,anchor_text="▶ Open the AKBASCORE TEST745 interface (Colab window)");window=f"Colab port window, port {port}"
        except Exception as ex:window=f"not available ({type(ex).__name__})"
    dump_json(GRADIO_LINK.with_suffix(".json"),dict(utc=utc_now(),session=SESSION_ID,share_url=share,local_url=local,colab_window=window,share_error=err))
    GRADIO_LINK.write_text(f"{share or local}\n",encoding="utf-8")
    banner(f"INTERFACE OPEN · {share or ('local only: '+str(local))}\n  public link : {share or '— (tunnel not available; use the Colab window link above)'}\n  local       : {local}\n"
           f"  Press RUN in the interface — everything else runs automatically. If the link stops working: run  launch_interface()  in a new cell.","#")
    slog("LAUNCH","interface open",share_url=share,local_url=local,colab_window=window);return share or local
def keep_cell_running():
    """keeps this Colab cell RUNNING while the interface is in use: the engine output and every stage are printed below too"""
    banner("THE CELL STAYS RUNNING — the interface is live. Press RUN in the interface; the TEST745 engine output is printed here and shown in the interface.\n"
           f"  A full RUN takes about 1.5 hours on an A100. Stop this cell (■) only when you have finished; the files stay in {DEMO_ROOT}","#")
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
    """second, independent channel (does not depend on the browser page): when a RUN has finished, the six JPEG figures
    of THIS run are shown here in the Colab cell, one below the other, and each is offered as a browser download.
    Can also be called by hand in a new cell:  show_figures_in_cell()"""
    keys=[k for k in FIGURES if k in FIG_FILES]
    banner(f"FIGURES OF THIS RUN ({SESSION_ID}) — {len(keys)}/{len(FIGURES)} — shown below in the cell, each also downloaded by the browser\n  folder: {FIG_DIR}","#")
    try:from IPython.display import display,Image as _IImg,HTML as _IHTML
    except Exception as ex:slog("CELL_FIGURES","IPython display not available",error=f"{type(ex).__name__}: {ex}");return
    for k in keys:
        f=FIG_FILES[k];m=FIGURES[k];nm=Path(f["jpg"]).name
        try:
            display(_IHTML(f"<div style='font:600 15px sans-serif;margin:14px 0 4px'>Figure {esc(m['n'])} — {esc(m['title'])} · {esc(f['badge'])} · {esc(nm)} · SHA-256 {esc(f['sha256_jpg'][:16])}…</div>"))
            display(_IImg(filename=f["jpg"],width=1100))
        except Exception as ex:slog("CELL_FIGURES",f"Figure {m['n']} could not be shown in the cell",error=f"{type(ex).__name__}: {ex}")
    if not download:return
    try:from google.colab import files as _cf
    except Exception:slog("CELL_FIGURES","not in Colab — browser download from the cell skipped; the files are in the folder above");return
    for k in keys:
        f=FIG_FILES[k]
        try:_cf.download(f["jpg"]);slog("CELL_DOWNLOAD",Path(f["jpg"]).name);time.sleep(1.0)
        except Exception as ex:slog("CELL_DOWNLOAD",f"{Path(f['jpg']).name} not downloaded",error=f"{type(ex).__name__}: {ex}")

# ---------------------------------------------------------------------------------------------------------------------
# START-UP (no GPU use): locked sources, the earlier run as RECORD, 745.py read-only — then the interface opens
# ---------------------------------------------------------------------------------------------------------------------
def startup():
    banner(f"{APP_NAME} · {EXPERIMENT} · start-up {local_now()} · session {SESSION_ID}"+("\nSIMULATION — NOTHING HERE IS AN EXPERIMENTAL RESULT" if SIM else ""))
    for n in LOCKS:RAW[n]=fetch_locked(n);slog("LOCKED_SOURCE",n,git_blob=SOURCES[n]["git_blob"],bytes=SOURCES[n]["bytes"])
    read_record();read_745(RAW["745.py"])
    slog("TEST745_RECORD",f"earlier run (RECORD): {REC['checks_passed']}/{REC['checks_total']} checks PASS · 11 cartridges · {REC['completed']['seconds']:.0f} s",
         C11=REC["completed"]["C11"][:16],C12=REC["completed"]["C12"][:16])
    slog("ENGINE_READY","745.py locked; it runs unchanged as its own process when RUN is pressed",git_blob=LOCKS["745.py"],experiment_dir=str(EXP_ROOT),
         existing_experiment_dir=EXP_ROOT.exists() and any(EXP_ROOT.iterdir()))
try:startup()
except Exception as _ex:
    _m=str(_ex)
    _hint=("A locked source changed on GitHub — the program stops instead of running unverified code." if "LOCKED SOURCE" in _m else
           "Network error while downloading a locked source from GitHub: run the cell again." if any(x in _m for x in ("URLError","timed out","HTTP Error","Connection","Name or service")) else
           "See the traceback above; nothing was run.")
    banner(f"START-UP FAILED — {type(_ex).__name__}: {_m}\nWHAT TO DO: {_hint}\nRecords of this attempt: {SESSION_DIR}","!")
    raise
launch_interface()
if os.environ.get("P745_NO_BLOCK")!="1":keep_cell_running()
# ===== END OF PART 3/3 =====
