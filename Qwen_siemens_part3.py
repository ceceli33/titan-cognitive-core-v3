# ===== PART 3/3 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 3 — Gradio Interface, User Interaction, Research Presentation and Session Logging
# Same working method and interface as the previous Qwen2.5-72B demonstration: start-up runs everything automatically
# (sources, preflight, the original Siemens PDF, the unchanged TEST718 experiment, verification, a mounted cartridge,
# seven JPEG figures, ZIP), then the Gradio interface opens with the figures, individual downloads and the package.
# The interface calls the engine, records and displays. It never computes or edits an answer.
# =====================================================================================================================
def esc(x):return html.escape(str(x))
def card_html(title,body,kind="info"):return f'<div class="kz card {kind}"><div class="h">{esc(title)}</div><div class="small">{body}</div></div>'
def chip(bid):
    if not bid:return "<span class='chip' style='color:#374151;border-color:#9ca3af'>vanilla · no memory</span>"
    c=ccol(cart_index(bid));return f'<span class="chip" style="color:#fff;background:{c};border-color:{c}">{esc(bid)}</span>'

CSS="""
:root{--kz-on:#0f766e;--kz-fg:#111827;--kz-card:#ffffff;--kz-bd:#d1d5db;--kz-a:#1d4ed8;--kz-err:#b91c1c;--kz-warn:#b45309}
.dark{--kz-on:#2dd4bf;--kz-fg:#f3f4f6;--kz-card:#111827;--kz-bd:#4b5563;--kz-a:#60a5fa;--kz-err:#f87171;--kz-warn:#fbbf24}
html,body{overflow-x:hidden!important}
.gradio-container{width:100%!important;max-width:960px!important;margin:0 auto!important;padding-left:10px!important;padding-right:10px!important;box-sizing:border-box!important}
.gradio-container *{box-sizing:border-box}
.kz{color:var(--kz-fg)!important;max-width:100%;overflow-wrap:anywhere;line-height:1.45}
.kz *{color:inherit}
.hero{background:#0b1220;border-radius:6px;padding:18px 18px 14px;margin:4px 0 8px}
.hero,.hero *{color:#f9fafb!important}
.rec{font-size:11.5px;letter-spacing:1.6px;text-transform:uppercase;opacity:.85;border:1px solid rgba(255,255,255,.35);display:inline-block;padding:2px 8px;border-radius:3px}
.brand{font-size:clamp(20px,5.6vw,30px);font-weight:800;letter-spacing:.4px;line-height:1.15;margin-top:10px}
.title{font-size:clamp(14px,3.8vw,18px);font-weight:600;margin-top:6px;color:#fde68a!important}
.by{font-size:13.5px;margin-top:10px}
.msg{margin:8px 0 0;padding-left:18px;font-size:13.5px}
.lic{font-size:12px;opacity:.85;margin-top:8px}
.card{background:var(--kz-card);border:1px solid var(--kz-bd);border-left:4px solid var(--kz-bd);border-radius:4px;padding:10px 12px;margin:6px 0}
.card.on{border-left-color:var(--kz-on)}.card.err{border-left-color:var(--kz-err)}.card.warn{border-left-color:var(--kz-warn)}.card.info{border-left-color:var(--kz-a)}
.card .h{font-weight:700;font-size:15px;margin-bottom:4px}
.small{font-size:13.5px}
.mono,.kz code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
.chip{display:inline-block;border:1px solid;border-radius:3px;padding:0 6px;font-size:12px;font-weight:700;white-space:nowrap}
.tbl{width:100%;border-collapse:collapse;font-size:13px}
.tbl td,.tbl th{border-bottom:1px solid var(--kz-bd);padding:5px 4px;vertical-align:top;text-align:left}
.tbl th{font-size:12px;opacity:.75}
.stg{font-size:13.5px;margin:2px 0}.stg.done{color:var(--kz-on)!important}.stg.run{color:var(--kz-a)!important;font-weight:700}.stg.wait{opacity:.55}.stg.fail{color:var(--kz-err)!important;font-weight:700}
.ans{white-space:pre-wrap;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;border:1px solid var(--kz-bd);border-radius:4px;padding:6px 8px;margin:3px 0;max-height:420px;overflow:auto}
#kz_ask button,#kz_ask{font-size:clamp(15px,4.2vw,18px)!important;font-weight:700!important;min-height:52px!important}
@media (max-width:640px){.tbl .hide-m{display:none}}
"""
HERO=(f'<div class="kz hero"><span class="rec">Live research demonstration · frozen Qwen2.5-72B · real industrial manual · measured in this session</span>'
      f'<div class="brand">AKBASCORE AI TECHNOLOGY<br>SILICON HIPPOCAMPUS · SIEMENS SINUMERIK ONE</div><div class="title">A 486-PAGE INDUSTRIAL MANUAL IN TEN PHYSICAL MEMORY CARTRIDGES — frozen weights, auditable against the source</div>'
      '<ul class="msg">'
      f'<li>The original <b>{esc(DOC_TITLE)}, edition {DOC_EDITION_MARK}</b> is downloaded from Siemens in this session and locked by SHA-256. Its 486 pages are split into <b>ten page ranges C01–C10</b>.</li>'
      '<li>Each range is <b>forged alone</b> by the frozen model into a physical CUT3 cartridge on SSD: the layer-3 residual state <b>H3</b> and the keys/values of <b>layers 0–3</b>, with SHA-256.</li>'
      '<li>A readout loads <b>one cartridge</b> from SSD to the GPU, rebuilds layers 4–79 and answers with <b>only the question</b> as input — the PDF is not given again. The 72B weights are never changed.</li>'
      '<li>Every answer is compared with the <b>vanilla model</b> (no PDF, no cartridge) and checked <b>automatically</b> against the PDF (stated page, verbatim word overlap). Answers are <b>not verified technical truth</b>.</li>'
      '<li>The ten readouts are combined by <b>text-mediated synthesis</b>: the frozen model reads the ten text answers with no cartridge attached. It is not native multi-cartridge synthesis.</li></ul>'
      f'<div class="by"><b>{esc(AUTHOR)}</b> · {esc(ORG)} · {esc(PLACE)} · {esc(VERSION_NOTE)}</div>'
      f'<div class="lic">{esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · <a href="{REPO}" target="_blank" rel="noopener">{esc(REPO)}</a> · Siemens manual © Siemens AG (not redistributed)</div></div>')
SCOPE_HTML=card_html("What this demo shows — and what it does not",
    "Shown, measured in this session: the unchanged TEST718 experiment forges ten physical cartridges from the original 2025 Siemens manual, restores each one from SSD on the GPU, "
    "answers a source-derived question with and without the cartridge, repeats three questions after release, maps the cartridges' H3 similarity and synthesises the ten text answers; "
    "afterwards every cartridge is mounted alone once more and its 80-layer K/V tensors are X-rayed read-only (Figure 5); "
    "the weights stay frozen and every file is SHA-256 verified. Not shown: verified technical correctness (answers are raw; checks are automatic), blind question answering (questions "
    "contain the section heading), ten cartridges jointly in GPU memory, native neural synthesis. The date gap between the model release and the manual edition is not proof that the "
    "model lacked this information.","warn")
PREV_HTML=card_html(PREV_TITLE,f"{esc(PREV_TEXT)}<br><br>For the implementation, experimental evidence, and multi-cartridge question-answering observations, see: "
                    f"<b>Research Record III — Qwen2.5-72B, Direct Internal-State Injection</b> · Zenodo Record 23434686 · "
                    f"<a href='https://zenodo.org/records/23434686' target='_blank' rel='noopener'>https://zenodo.org/records/23434686</a><br>"
                    f"<i>Previously published research — not a result of this Siemens experiment.</i>","info")

def engine_card_html():
    a=engine_architecture() or {};v=STATE.get("verification") or {};env_=(E.get("R718") or {});mi=MODEL_IDENTITY
    rows=[("Model",f"{MODEL_ID} · NF4 4-bit, BF16 compute · frozen · snapshot {str(mi.get('loaded_snapshot_commit'))[:12]}"),
          ("Model release",f"first public release {MODEL_RELEASE['date']} ({MODEL_RELEASE['url']})"),
          ("Architecture",f"{a.get('layers')} layers · hidden {a.get('hidden')} · {a.get('q_heads')} Q / {a.get('kv_heads')} KV heads · head dim {a.get('head_dim')} · CUT{a.get('cut')}"),
          ("Source document",f"{DOC_TITLE} · edition {DOC_EDITION_MARK} (on {DOC.get('edition_mark_pages')} pages) · {DOC.get('pages')} pages · SHA-256 {str(DOC.get('sha256'))[:16]}… · downloaded {str(DOC.get('download_end_utc'))[:19]} UTC"),
          ("Experiment",f"718.py git blob {LOCKS['718.py'][:12]}… · executed unchanged · status {env_.get('status')} · {ENGINE.get('seconds')} s"),
          ("Cartridges",f"{N_CART} on SSD · SHA-256 re-verified · one mounted at a time · GPU reserve {E.get('GPU_RESERVE_GIB')} GiB (unchanged)"),
          ("Live verification",f"{v.get('passed')}/{v.get('total')} passed"),
          ("Generation",f"greedy · at most {READOUT_MAX_NEW} new tokens per answer (TEST718 readout) · synthesis up to {SYNTH_MAX_NEW}"),
          ("Engine ready",f"{INIT.get('ready_utc')} · start-up {INIT.get('total_seconds',0)/60:.1f} min")]
    return card_html("Engine (measured at start-up in this session)",'<table class="tbl">'+"".join(f"<tr><th>{esc(x)}</th><td class='mono'>{esc(y)}</td></tr>" for x,y in rows)+"</table>","on")

def stages_html():
    done={s["step"]:s for s in INIT["steps"]};out=[]
    for i,(key,title) in enumerate(INIT_STEPS.items(),1):
        if key in done:cl,mk,m="done","✓",f" — <span class='small'>{done[key]['seconds']:.0f} s</span>"
        elif INIT.get("failed") and INIT["failed"]["step"]==key:cl,mk,m="fail","✗",f" — <span class='small'>{esc(INIT['failed']['error'])}</span>"
        else:cl,mk,m="wait","○",""
        out.append(f"<div class='stg {cl}'>{mk} {i}/{len(INIT_STEPS)} · {esc(title)}{m}</div>")
    pc=100.0*len(done)/len(INIT_STEPS)
    bar=f'<div style="margin-top:6px;background:#e5e7eb;height:10px"><div style="width:{pc:.0f}%;height:10px;background:#0f766e"></div></div>'
    v=STATE.get("verification") or {}
    ver="".join(f"<div class='small'>{'✓' if i['passed'] else '✗'} <span class='mono'>{esc(i['name'])}</span></div>" for i in v.get("items",[]))
    return card_html(f"Full research run at start-up · completed in {INIT.get('total_seconds',0)/60:.1f} min · live verification {v.get('passed')}/{v.get('total')}","".join(out)+bar+
                     "<div style='margin-top:8px'><b>Live verification</b></div>"+ver,"on" if INIT.get("ready") else "err")

def pdf_card():
    d=DOC
    return card_html("Original Siemens PDF used in this session",
        f"<b>{esc(DOC_TITLE)}</b> · edition {esc(DOC_EDITION_MARK)} (printed on {esc(d.get('edition_mark_pages'))} of {esc(d.get('pages'))} pages) · order no. {esc(d.get('order_number'))} · {esc(d.get('software_version'))}<br>"
        f"downloaded {esc(d.get('download_start_utc'))} → {esc(d.get('download_end_utc'))} UTC · {d.get('bytes',0):,} bytes · SHA-256 <span class='mono'>{esc(d.get('sha256'))}</span> (= TEST716 lock)<br>"
        f"⬇ <a href='{PDF_URL}' target='_blank' rel='noopener'><b>Download the original PDF from the official Siemens address</b></a> and compare its SHA-256 with the value above "
        f"(record: SOURCE_DOCUMENT_RECORD.json).<br><i>{esc(PDF_POLICY)}</i> <a href='{PDF_TERMS_URL}' target='_blank' rel='noopener'>Siemens terms</a>. "
        f"The verified copy stays only inside this Colab runtime: <span class='mono'>{esc(d.get('verified_local_copy'))}</span>","info")
def cond_choices():
    ch=[]
    for i,b in enumerate(E["R"]["books"]):
        h=E["chosen"][i][3] if "chosen" in E else ""
        ch.append((f"{b['id']} · PDF pages {b['page_range'][0]}–{b['page_range'][1]} · {b['body_tokens']:,} tokens · e.g. “{h}”",b["id"]))
    return ch+[("Vanilla model · no PDF, no cartridge","NONE")]
def suggested_question(sel):
    if sel=="NONE" or sel not in cart_ids():return E["question"](E["chosen"][0])
    return E["question"](E["chosen"][cart_index(sel)])
def condition_info(sel):
    r=None
    if LIVE.get("rows") and sel in cart_ids():r=LIVE["rows"][cart_index(sel)]
    head=f"Mounted now: {chip(STATE['cartridge'])}"+(f" · {STATE['mount']['cache_tokens']:,} rows" if STATE.get("mount") else "")
    if sel!="NONE" and sel!=STATE["cartridge"]:head+=f"<br><b>Selected {esc(sel)}</b> — pressing ASK releases the current cartridge and restores {esc(sel)} from SSD (about 30–60 s)."
    if sel=="NONE":head+="<br><b>Vanilla model selected</b> — the question is answered without any cartridge."
    body=""
    if r:
        body=(f"<br><br><b>{esc(r['id'])}</b> · PDF pages {r['pages'][0]}–{r['pages'][1]} · {r['body_tokens']:,} tokens · file {r['file_bytes']:,} B · SHA-256 <span class='mono'>{esc(str(r['cartridge_sha256'])[:16])}…</span> "
              f"{'✓ re-verified' if r['file_sha_ok'] else '✗'}<br>TEST718 heading: <i>{esc(r['heading'])}</i> (PDF page {r['heading_page']})"
              f"<br>Start-up readout: {r['physical_wall_s']} s · stated page → {esc(r['page_physical']['result'])} · 5-gram support {pct(r['support_physical']['share'])} (vanilla {pct(r['support_vanilla']['share'])})")
    return card_html("Memory condition",head+body,"info")

def answer_html(r,c,mnt=None):
    t=""
    if mnt:
        t+=(f"<div class='small'><b>Cartridge restored from SSD</b> · {chip(mnt['cartridge'])} SSD read + SHA-256 {mnt['ssd_load_ms']/1000:.2f} s · host→GPU {mnt['h2d_ms']:.0f} ms · "
            f"rebuild {mnt['rebuild_ms']/1000:.1f} s · {mnt['cache_tokens']:,} rows</div>")
    t+="<table class='tbl'><tr><th>memory</th><th>raw model answer</th><th class='hide-m'>time</th></tr>"
    if r is not None:t+=f"<tr><td>{chip(r['cartridge'])}<div class='small mono'>{r['cache_tokens']:,} rows · {r['answer_tokens']} tok</div></td><td><div class='ans'>{esc(r['raw'])}</div></td><td class='hide-m mono'>{r['seconds']} s</td></tr>"
    if c is not None:t+=f"<tr><td>{chip(None)}<div class='small mono'>{c['answer_tokens']} tok</div></td><td><div class='ans'>{esc(c['raw'])}</div></td><td class='hide-m mono'>{c['seconds']} s</td></tr>"
    t+="</table>"
    x=r or c
    t+=(f"<div class='small mono' style='margin-top:8px;opacity:.8'>question {esc(x['question'])}<br>max new tokens {READOUT_MAX_NEW} · NOT VERIFIED — check against the Siemens PDF · GPU free {x['gpu'].get('free_gib')} GiB · {esc(x['utc'])}</div>")
    return card_html("Answer of the frozen Qwen2.5-72B — raw output, unedited",t,"on")

GPU_LOCK=threading.Lock()
def busy_card():return card_html("Busy","Another run is using the GPU. Please wait until it has finished and press the button again.","warn")
def err_card(ex):
    oom="OutOfMemoryError" in type(ex).__name__ or "GPU_SAFETY_STOP" in str(ex)
    hint=" The TEST709 GPU safety reserve stopped the operation (or CUDA ran out of memory); the memory was released. Press ASK again." if oom else ""
    return card_html("Error",f"<code>{esc(type(ex).__name__)}: {esc(ex)}</code>{esc(hint)}<br>Nothing was hidden or replaced; the full traceback is in the Error log tab.","err")

def all_files():
    figs=[FIG_FILES[k]["jpg"] for k in FIGURES if k in FIG_FILES]
    return figs+[str(ZIP_PATH)]+[p for _,p in download_items() if Path(p).is_file()]
def gallery_items():return [(FIG_FILES[k]["jpg"],FIGURES[k]) for k in FIGURES if k in FIG_FILES]
def summary_text():
    try:return RUN_SUMMARY.read_text(encoding="utf-8")
    except Exception:return ""
def refresh_package():
    try:package_session()
    except Exception as ex:slog("PACKAGE_FAILED",str(ex))
    return all_files(),(str(ZIP_PATH) if ZIP_PATH.is_file() else None),summary_text()

def ask_handler(sel,question,vanilla):
    NO=("","",None)
    keep=(gr.update(),gr.update(),gr.update(),condition_info(sel))
    if not GPU_LOCK.acquire(blocking=False):yield (busy_card(),)+NO+keep;return
    try:
        q=(question or "").strip()
        if not q:raise OpError("Type a question first.")
        mnt=None;r=None;c=None
        if sel!="NONE":
            if STATE["cartridge"]!=sel or STATE["memory"] is None:
                yield (card_html("Running",f"Restoring cartridge {esc(sel)} from SSD (TEST718: cart_load → SHA-256 → initialize) …","info"),)+NO+keep
                mnt=mount(sel)
            yield (card_html("Running",f"Cartridge {esc(sel)} mounted · asking the frozen model{' and the vanilla model' if vanilla else ''} (up to {READOUT_MAX_NEW} tokens each) …","info"),)+NO+keep
            r=ask(q[:3000],True)
            if vanilla:c=ask(q[:3000],False)
        else:
            yield (card_html("Running","Asking the vanilla model (no cartridge) …","info"),)+NO+keep
            c=ask(q[:3000],False)
        rec=dict(question=q,selection=sel,memory=r,vanilla=c,mount=mnt,session=SESSION_ID)
        d=SESSION_DIR/"single_runs";d.mkdir(exist_ok=True)
        p=dump_json(d/f"ASK_{sel}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json",rec)
        files,z,summ=refresh_package()
        yield (answer_html(r,c,mnt),json.dumps(jsafe(rec),ensure_ascii=False,indent=1)[:200000],"",str(p),files,z,summ,condition_info(sel))
    except Exception as ex:
        slog("UI_ERROR","ask",error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc()[-3000:])
        files,z,summ=refresh_package()
        yield (err_card(ex),"",traceback.format_exc(),None,files,z,summ,condition_info(sel))
    finally:GPU_LOCK.release()

def select_handler(sel,current):
    qs={E["question"](x) for x in E["chosen"].values()} if "chosen" in E else set()
    newq=suggested_question(sel) if (not (current or "").strip() or current in qs) else current
    return condition_info(sel),newq

def verify_handler():
    if not GPU_LOCK.acquire(blocking=False):return busy_card()
    try:
        w=verify_weights();d=verify_disk()
        rows=[("time (UTC)",w["utc"]),("weight sentinel at load (TEST718)",w["before"]),("weight sentinel now",w["after"]),("sentinel unchanged",w["passed"]),
              ("trainable tensors",sum(1 for p in E["model"].parameters() if p.requires_grad))]+[(f"cartridge {f['cartridge']} SHA-256 on SSD = engine record",f["equals_engine_record"]) for f in d["files"]]
        ok=w["passed"] and d["passed"] and rows[4][1]==0
        return card_html("Weight and cartridge verification · measured now","<table class='tbl'>"+"".join(f"<tr><th>{esc(a)}</th><td class='mono'>{esc(b)}</td></tr>" for a,b in rows)+"</table>","on" if ok else "err")
    except Exception as ex:return err_card(ex)
    finally:GPU_LOCK.release()

def _tb(**kw):
    for extra in (([{"buttons":["copy"]}] if _GR_MAJOR>=6 else [])+[{"show_copy_button":True},{}]):
        try:return gr.Textbox(**extra,**kw)
        except TypeError:continue
def _gallery(**kw):
    try:return gr.Gallery(columns=1,height="auto",object_fit="contain",preview=False,**kw)
    except TypeError:return gr.Gallery(**kw)

def build_ui():
    blocks=gr.Blocks(title=APP_SHORT) if _GR_MAJOR>=6 else gr.Blocks(css=CSS,title=APP_SHORT)
    first=cart_ids()[0]
    with blocks as demo:
        gr.HTML(HERO);gr.HTML(engine_card_html())
        cond_dd=gr.Dropdown(choices=cond_choices(),value=first,label="Memory condition (one physical cartridge at a time, or the vanilla model)",interactive=True)
        info=gr.HTML(condition_info(first))
        cq=gr.Textbox(value=suggested_question(first),label="Question (answered from the selected cartridge; raw output, not verified)",lines=3,max_lines=8)
        ctl=gr.Checkbox(value=True,label="Also ask the same question to the vanilla model (no PDF, no cartridge)")
        ask_b=gr.Button("ASK",variant="primary",elem_id="kz_ask")
        status=gr.HTML(stages_html())
        gallery=_gallery(label=f"Figures 1–{len(FIGURES)} (JPEG, 300 dpi) — measured in this session",value=gallery_items())
        files=gr.File(label="Individual downloads · figures, ZIP, run summary, live engine output, records, manifest, historical logs",value=all_files(),file_count="multiple",interactive=False)
        gr.HTML(pdf_card())
        zipb=gr.DownloadButton(label="⬇ Download the complete experiment package (.zip)",value=str(ZIP_PATH),interactive=True)
        single_file=gr.File(label="Record of the last question (.json)",interactive=False)
        with gr.Tabs():
            with gr.Tab("Run summary"):summ=_tb(lines=14,max_lines=40,label="RUN_SUMMARY.txt",value=summary_text())
            with gr.Tab("Raw record (last question)"):raw=_tb(lines=14,max_lines=40,label="JSON")
            with gr.Tab("Error log"):errs=_tb(lines=10,max_lines=40,label="traceback (empty = no error)")
        with gr.Accordion("Verify the frozen weights and the ten cartridge files now",open=False):
            vb=gr.Button("Verify now");vout=gr.HTML()
        gr.HTML(SCOPE_HTML);gr.HTML(PREV_HTML)
        gr.HTML(f'<div class="kz small" style="opacity:.8;margin:8px 0 18px">{esc(AUTHOR)} · {esc(ORG)} · {esc(LICENSE_NAME)} · '
                f'TEST718 <a href="{URL_718}" target="_blank" rel="noopener">718.py</a> · TEST716 <a href="{URL_716}" target="_blank" rel="noopener">716.py</a> · TEST709 <a href="{URL_709}" target="_blank" rel="noopener">709.py</a> · '
                +" · ".join(f'<a href="{u}" target="_blank" rel="noopener">{esc(t.split(" — ")[0])}</a>' for t,u in LINEAGE)+
                ' · Qwen2.5-72B-Instruct, the Siemens manual and third-party libraries remain under their own licences.</div>')
        cond_dd.change(select_handler,inputs=[cond_dd,cq],outputs=[info,cq])
        outs=[status,raw,errs,single_file,files,zipb,summ,info]
        ask_b.click(ask_handler,inputs=[cond_dd,cq,ctl],outputs=outs)
        vb.click(verify_handler,outputs=vout)
    try:demo.queue(default_concurrency_limit=1)
    except TypeError:demo.queue(concurrency_count=1)
    return demo

# ---------------------------------------------------------------------------------------------------------------------
# START-UP (as in the previous demonstration): the experiment runs automatically, then the interface opens
# ---------------------------------------------------------------------------------------------------------------------
_GR_MAJOR=int(re.match(r"\d+",gr.__version__).group())
try:run_initialization()
except Exception as _ex:
    _m=str(_ex)
    _hint=("A locked source changed on GitHub — the program stops instead of running unverified code." if "LOCKED SOURCE" in _m or "BLOB" in _m or "DRIFT" in _m else
           "The Siemens PDF could not be downloaded or no longer matches the locked SHA-256: check the network or the Siemens address and run again." if "SOURCE DOCUMENT" in _m or "PDF" in _m else
           "Hugging Face refused the model download: add your token as the Colab secret HF_TOKEN (allow notebook access) and run again." if any(x in _m for x in ("401","403","gated","Unauthorized","token")) else
           "GPU memory: the TEST709 safety reserve or CUDA stopped the run. Use an A100 80 GB runtime (Runtime → Change runtime type), restart the session and run again." if any(x in _m for x in ("GPU_SAFETY_STOP","out of memory")) else
           "This runtime is not an A100 80 GB: Runtime → Change runtime type → A100, then run again." if any(x in _m for x in ("A100","CUDA is not available","exactly one GPU")) else
           "Disk: free space in the Colab runtime (or use a runtime with more disk) and run again." if "disk" in _m.lower() else
           "Network error while downloading a locked source, the Siemens PDF or the model: run the cell again." if any(x in _m for x in ("URLError","timed out","HTTP Error","Connection")) else
           "See the traceback above; nothing was changed in the engine.")
    _OUT.write("\n"+"="*110+f"\nENGINE START FAILED — {type(_ex).__name__}: {_m}\nWHAT TO DO: {_hint}\nRecords of this attempt: {SESSION_DIR}\n"+"="*110+"\n");_OUT.flush()
    raise
demo=build_ui()
slog("LAUNCH","public share link — open the printed gradio.live address (also works on a phone)")
_LAUNCH=dict(share=True,allowed_paths=[str(SESSION_DIR)],show_error=True,inline=False)
if _GR_MAJOR>=6:_LAUNCH["css"]=CSS
try:demo.launch(**_LAUNCH)
except TypeError as _ex:
    if "css" not in str(_ex):raise
    _LAUNCH.pop("css",None);demo.launch(**_LAUNCH)
