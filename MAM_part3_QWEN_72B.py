# ===== SILICON HIPPOCAMPUS QWEN72B · PART 3/3 — paste directly after PART 2 in the same cell =====
# =====================================================================================================================
# PART 3 / 3 — Gradio Interface, User Interaction, Research Presentation and Session Logging
# Same working method and interface layout as the Mistral v1.4 demonstration: start-up runs the engine automatically
# (here: model, cartridges, live TEST709 protocol, A+B+C memory, verification, six JPEG figures, ZIP), then the Gradio
# interface opens with the figures, the individual downloads and the complete package. The interface calls the engine,
# records and displays. It never computes or edits an answer. The published 709.log is only a labelled historical file.
# =====================================================================================================================
def esc(x):return html.escape(str(x))
def card_html(title,body,kind="info"):return f'<div class="kz card {kind}"><div class="h">{esc(title)}</div><div class="small">{body}</div></div>'
def chips(order):return "".join(f'<span class="chip" style="color:#fff;background:{BOOK_COLORS[b]};border-color:{BOOK_COLORS[b]}">{esc(b)}</span> ' for b in order) or "<i>no memory mounted</i>"

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
.ans{white-space:pre-wrap;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;border:1px solid var(--kz-bd);border-radius:4px;padding:6px 8px;margin:3px 0}
#kz_ask button,#kz_ask{font-size:clamp(15px,4.2vw,18px)!important;font-weight:700!important;min-height:52px!important}
@media (max-width:640px){.tbl .hide-m{display:none}}
"""
HERO=(f'<div class="kz hero"><span class="rec">Live research demonstration · frozen Qwen2.5-72B · measured in this session</span>'
      f'<div class="brand">AKBASCORE AI TECHNOLOGY<br>SILICON HIPPOCAMPUS · QWEN2.5-72B / CUT3</div><div class="title">THREE PHYSICAL BOOK CARTRIDGES — inside a frozen 80-layer transformer, from text to tensor memory</div>'
      '<ul class="msg">'
      '<li>Each book excerpt (10,000 tokens) is <b>forged alone</b> by the frozen model into a physical cartridge on SSD: the layer-3 residual state <b>H3</b> and the attention keys/values of <b>layers 0–3</b>, with SHA-256.</li>'
      '<li>A mount feeds the model <b>zero input embeddings</b>: the book enters only as an H3 transplant at the layer-3 boundary, and <b>layers 4–79 are rebuilt</b> on the GPU. Every append checks <b>all prior K/V bytes of all 80 layers by exact SHA-256</b>.</li>'
      '<li>Questions are answered with <b>only the question suffix</b> as input — the book text is not given again. The 72B weights (NF4) are never changed.</li>'
      '<li>Everything shown here was measured in <b>this session</b> by the TEST709 engine (709.py, executed unchanged). The published 709.log is kept only as a labelled historical file.</li>'
      '<li>The books are <b>famous public-domain classics</b>: correct names can come from pretraining. Compare with the <b>no-memory control</b>. Semantics are <b>unscored</b>; answers are capped at 48 new tokens.</li></ul>'
      f'<div class="by"><b>{esc(AUTHOR)}</b> · {esc(ORG)} · {esc(PLACE)} · {esc(VERSION_NOTE)}</div>'
      f'<div class="lic">{esc(LICENSE_NAME)} · {esc(COPYRIGHT)} · <a href="{REPO}" target="_blank" rel="noopener">{esc(REPO)}</a></div></div>')
SCOPE_HTML=card_html("What this demo shows — and what it does not",
    "Shown: the TEST709 Qwen2.5-72B CUT3 engine forges three physical cartridges, runs its eleven scripted trials, rebuilds the full 80-layer K/V memory A+B+C on the GPU and "
    "verifies every append bytewise; every answer is the raw output of the frozen model; every figure value is measured in this session. Not shown: semantic correctness "
    "(unscored), causal use of the cartridges for these famous books (pretraining knowledge cannot be excluded), full-book comprehension, millisecond hot-swap (a mount takes "
    "tens of seconds), autonomous reasoning. The published 709.log is an earlier record, not this run.","warn")

def engine_card_html():
    R=E.get("R",{});env=R.get("env",{});a=engine_architecture() or {};v=STATE.get("verification") or {}
    rows=[("Model",f"{E.get('MODEL_ID')} · NF4 4-bit, BF16 compute · frozen · revision {str(R.get('model_revision'))[:12]}"),
          ("Architecture",f"{a.get('layers')} layers · hidden {a.get('hidden')} · {a.get('q_heads')} Q / {a.get('kv_heads')} KV heads · head dim {a.get('head_dim')} · CUT{a.get('cut')}"),
          ("GPU",f"{env.get('gpu')} · reserve {E.get('GPU_RESERVE_GIB')} GiB (TEST709 safety reserve, unchanged)"),
          ("Software",f"torch {env.get('torch')} · transformers {env.get('transformers')} · bitsandbytes {env.get('bitsandbytes')} · gradio {gr.__version__} · python {env.get('python')}"),
          ("TEST709 engine",f"709.py git blob {SOURCES.get('709.py',{}).get('git_blob')} · verified · executed unchanged"),
          ("Cartridges",", ".join(f"{b['id']} {b.get('cartridge_file_bytes',0):,} B" for b in R.get("books",[]))+" · forged in this session"),
          ("Live engine status",f"{R.get('status')} · {len(R.get('trials',[]))} protocol trials · engine checks {sum(1 for c in R.get('checks',[]) if c.get('pass'))}/{len(R.get('checks',[]))}"),
          ("Live verification",f"{v.get('passed')}/{v.get('total')} passed"),
          ("Generation",f"greedy · at most {E.get('MAX_NEW')} new tokens · prefix {E.get('P')} tokens"),
          ("Engine ready",f"{INIT.get('ready_utc')} · start-up {INIT.get('total_seconds',0)/60:.1f} min")]
    return card_html("Engine (measured at start-up in this session)",'<table class="tbl">'+"".join(f"<tr><th>{esc(a_)}</th><td class='mono'>{esc(b)}</td></tr>" for a_,b in rows)+"</table>","on")

def stages_html():
    """the start-up research run, stage by stage, as actually completed (Mistral v1.4 stage list)"""
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

def condition_info(combo):
    R=E.get("R",{});cur="+".join(STATE["order"])
    books="".join(f"<br>{chips([b['id']])} <b>{esc(b.get('title'))}</b> · first {b.get('requested_tokens'):,} tokens · SHA-256 <span class='mono'>{esc(str(b.get('cartridge_sha256'))[:16])}…</span>" for b in R.get("books",[]))
    note=(f"Mounted now: {chips(STATE['order'])}" +(f" · {STATE['stages'][-1]['cache_tokens']:,} rows" if STATE["stages"] else "")+
          ("" if combo==cur else f"<br><b>Selected {esc(combo)}</b> — pressing ASK releases the memory and rebuilds it from the SSD cartridges in this order (about 20–80 s)."))
    qs="".join(f"<br><span class='mono'>{esc(t['label'])}</span> {esc(t['questions'][0])}" for t in _SEG.get("trials",[]))
    return card_html("Memory condition",note+"<br><br><b>Cartridges on SSD (this session)</b>"+books+"<br><br><b>Questions of the TEST709 protocol</b> (already run at start-up; you may ask any question)"+qs,"info")

def answer_html(r,c,stages=None):
    t=""
    if stages:
        t+=("<div class='small'><b>Memory rebuilt</b></div><table class='tbl'><tr><th>book</th><th>step</th><th class='hide-m'>SSD s</th><th class='hide-m'>H2D ms</th><th>rebuild s</th><th>rows</th><th>prior K/V SHA-256</th></tr>"+
            "".join(f"<tr><td>{chips([s['book']])}</td><td>{esc(s['operation'])}</td><td class='hide-m mono'>{s['ssd_load_ms']/1000:.2f}</td><td class='hide-m mono'>{s['h2d_ms']:.0f}</td>"
                    f"<td class='mono'>{s['rebuild_ms']/1000:.1f}</td><td class='mono'>{s['cache_tokens']:,}</td><td>{'PASS (engine log)' if s['prior_kv_sha256_pass_line'] else ('—' if s['prior_kv_sha256_pass_line'] is None else 'missing')}</td></tr>" for s in stages)+"</table>")
    t+=(f"<table class='tbl'><tr><th>memory</th><th>raw model answer</th><th class='hide-m'>time</th></tr>"
        f"<tr><td>{chips(r['memory_order'])}<div class='small mono'>{r['cache_tokens']:,} rows</div></td><td><div class='ans'>{esc(r['raw'])}</div></td><td class='hide-m mono'>{r['seconds']} s</td></tr>")
    if c is not None:t+=f"<tr><td><b>control</b><div class='small'>no memory</div></td><td><div class='ans'>{esc(c['raw'])}</div></td><td class='hide-m mono'>{c['seconds']} s</td></tr>"
    t+="</table>"
    t+=(f"<div class='small mono' style='margin-top:8px;opacity:.8'>question {esc(r['question'])}<br>max new tokens {r['max_new_tokens']} · semantics UNSCORED · GPU free {r['gpu'].get('free_gib')} GiB · "
        f"allocated {r['gpu'].get('allocated_gib')} GiB · {esc(r['utc'])}</div>")
    return card_html("Answer of the frozen Qwen2.5-72B — raw output, unedited",t,"on")

GPU_LOCK=threading.Lock()
def busy_card():return card_html("Busy","Another run is using the GPU. Please wait until it has finished and press the button again.","warn")
def err_card(ex):
    oom="OutOfMemoryError" in type(ex).__name__ or "GPU_SAFETY_STOP" in str(ex)
    hint=" The TEST709 GPU safety reserve stopped the operation (or CUDA ran out of memory); the memory was released. Choose fewer cartridges and press ASK again." if oom else ""
    return card_html("Error",f"<code>{esc(type(ex).__name__)}: {esc(ex)}</code>{esc(hint)}<br>Nothing was hidden or replaced; the full traceback is in the Error log tab.","err")

def all_files():
    """individual downloads (Mistral v1.4 list): six JPEG figures, ZIP, run summary, manifest, live logs and records,
    and the historical 709.log (clearly named HISTORICAL_…)"""
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

def ask_handler(combo,question,control):
    NO=("","",None)
    if not GPU_LOCK.acquire(blocking=False):yield (busy_card(),)+NO+(gr.update(),gr.update(),gr.update(),condition_info(combo));return
    try:
        q=(question or "").strip()
        if not q:raise OpError("Type a question first.")
        books=combo_books(combo);stages=None
        if books!=STATE["order"] or STATE["memory"] is None:
            yield (card_html("Running",f"Rebuilding memory {esc(combo)} from the SSD cartridges (TEST709 cart_load → initialize → append) …","info"),)+NO+(gr.update(),gr.update(),gr.update(),condition_info(combo))
            stages=build_memory(books)
        yield (card_html("Running",f"Memory {esc('+'.join(STATE['order']))} · asking the frozen model{' and the no-memory control' if control else ''} …","info"),)+NO+(gr.update(),gr.update(),gr.update(),condition_info(combo))
        r=ask(q[:2000],True);c=ask(q[:2000],False) if control else None
        rec=dict(question=q,memory=r,control=c,stages=stages,session=SESSION_ID)
        d=SESSION_DIR/"single_runs";d.mkdir(exist_ok=True)
        p=dump_json(d/f"ASK_{'_'.join(STATE['order'])}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json",rec)
        files,z,summ=refresh_package()
        yield (answer_html(r,c,stages),json.dumps(jsafe(rec),ensure_ascii=False,indent=1)[:200000],"",str(p),files,z,summ,condition_info(combo))
    except Exception as ex:
        slog("UI_ERROR","ask",error=f"{type(ex).__name__}: {ex}",traceback=traceback.format_exc()[-3000:])
        files,z,summ=refresh_package()
        yield (err_card(ex),"",traceback.format_exc(),None,files,z,summ,condition_info(combo))
    finally:GPU_LOCK.release()

def verify_handler():
    if not GPU_LOCK.acquire(blocking=False):return busy_card()
    try:
        w=verify_weights();d=verify_disk()
        rows=[("time (UTC)",w["utc"]),("weight sentinel at load",w["before"]),("weight sentinel now",w["after"]),("sentinel unchanged",w["passed"]),
              ("trainable tensors",sum(1 for p in E["model"].parameters() if p.requires_grad))]+[(f"cartridge {f['book']} SHA-256 on disk = engine record",f["equals_engine_record"]) for f in d["files"]]
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
    with blocks as demo:
        gr.HTML(HERO);gr.HTML(engine_card_html())
        cond_dd=gr.Dropdown(choices=COMBOS,value="A+B+C",label="Memory condition (which cartridges are mounted, in order)",interactive=True)
        info=gr.HTML(condition_info("A+B+C"))
        cq=gr.Textbox(value="",label="Question (answered from the selected memory; not scored)",placeholder="e.g. Who is Robert Walton?",lines=1,max_lines=3)
        ctl=gr.Checkbox(value=True,label="Also ask the same question without memory (no-memory control)")
        ask_b=gr.Button("ASK",variant="primary",elem_id="kz_ask")
        status=gr.HTML(stages_html())
        gallery=_gallery(label="Figures 1–6 (JPEG, 300 dpi) — measured in this session",value=gallery_items())
        files=gr.File(label="Individual downloads · figures, ZIP, run summary, manifest, live logs, raw answers, historical 709.log",value=all_files(),file_count="multiple",interactive=False)
        zipb=gr.DownloadButton(label="⬇ Download the complete experiment package (.zip)",value=str(ZIP_PATH),interactive=True)
        single_file=gr.File(label="Record of the last question (.json)",interactive=False)
        with gr.Tabs():
            with gr.Tab("Run summary"):summ=_tb(lines=14,max_lines=40,label="RUN_SUMMARY.txt",value=summary_text())
            with gr.Tab("Raw record (last question)"):raw=_tb(lines=14,max_lines=40,label="JSON")
            with gr.Tab("Error log"):errs=_tb(lines=10,max_lines=40,label="traceback (empty = no error)")
        with gr.Accordion("Verify the frozen weights and the cartridge files now",open=False):
            vb=gr.Button("Verify now");vout=gr.HTML()
        gr.HTML(SCOPE_HTML)
        gr.HTML(f'<div class="kz small" style="opacity:.8;margin:8px 0 18px">{esc(AUTHOR)} · {esc(ORG)} · {esc(LICENSE_NAME)} · '
                f'TEST709 <a href="{URL_709}" target="_blank" rel="noopener">709.py</a> · historical record <a href="{URL_709_LOG}" target="_blank" rel="noopener">709.log</a> · '
                f'Qwen2.5-72B-Instruct and third-party libraries remain under their own licences.</div>')
        cond_dd.change(condition_info,inputs=cond_dd,outputs=info)
        outs=[status,raw,errs,single_file,files,zipb,summ,info]
        ask_b.click(ask_handler,inputs=[cond_dd,cq,ctl],outputs=outs);cq.submit(ask_handler,inputs=[cond_dd,cq,ctl],outputs=outs)
        vb.click(verify_handler,outputs=vout)
    try:demo.queue(default_concurrency_limit=1)
    except TypeError:demo.queue(concurrency_count=1)
    return demo

# ---------------------------------------------------------------------------------------------------------------------
# START-UP (as in Mistral v1.4): the engine runs automatically, then the interface opens
# ---------------------------------------------------------------------------------------------------------------------
_GR_MAJOR=int(re.match(r"\d+",gr.__version__).group())
try:run_initialization()
except Exception as _ex:
    _m=str(_ex)
    _hint=("A locked source changed on GitHub — the program stops instead of running unverified code." if "LOCKED SOURCE" in _m else
           "Hugging Face refused the model download: add your token as the Colab secret HF_TOKEN (allow notebook access) and run again." if any(x in _m for x in ("401","403","gated","Unauthorized","token")) else
           "GPU memory: the TEST709 safety reserve or CUDA stopped the run. Use an A100 80 GB runtime (Runtime → Change runtime type), restart the session and run again." if any(x in _m for x in ("GPU_SAFETY_STOP","out of memory","KV_ONLY_ESTIMATE")) else
           "This runtime is not an A100 80 GB: Runtime → Change runtime type → A100, then run again." if any(x in _m for x in ("A100","CUDA is not available","exactly one GPU")) else
           "Disk: free space in the Colab runtime (or use a runtime with more disk) and run again." if "disk" in _m.lower() else
           "Network error while downloading a locked source, a book or the model: run the cell again." if any(x in _m for x in ("URLError","timed out","HTTP Error","Connection")) else
           "See the traceback above; nothing was changed in the engine.")
    print("\n"+"="*110+f"\nENGINE START FAILED — {type(_ex).__name__}: {_m}\nWHAT TO DO: {_hint}\nRecords of this attempt: {SESSION_DIR}\n"+"="*110,flush=True)
    raise
demo=build_ui()
slog("LAUNCH","public share link — open the printed gradio.live address (also works on a phone)")
_LAUNCH=dict(share=True,allowed_paths=[str(DEMO_ROOT)],show_error=True,inline=False)
if _GR_MAJOR>=6:_LAUNCH["css"]=CSS
try:demo.launch(**_LAUNCH)
except TypeError as _ex:
    if "css" not in str(_ex):raise
    _LAUNCH.pop("css",None);demo.launch(**_LAUNCH)
