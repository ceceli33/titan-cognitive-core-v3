# ===== PART 2/3 — paste directly after PART 1 in the same cell =====
# =====================================================================================================================
# PART 2 / 3 — Physical Pair Memories, C11, Isolated Question Process, Integrity and Research Figures
# Process 1 and process 2 call the TEST709 engine functions through the unchanged TEST716 set-up (cart_load, initialize,
# append, forge_stream, full_kv_seal, answer, sentinel). Nothing here changes CUT3, RoPE, the cartridge format, the K/V layout,
# the SHA-256 guards or the GPU reserve. The only value set from outside is the generation ceiling MAX_NEW per call.
# All measurements are read-only and computed from this session's records and from the original PDF downloaded now.
# =====================================================================================================================

if str(PROGRAM_DIR) not in sys.path:sys.path.insert(0,str(PROGRAM_DIR))
import TEST719_common as C
C=importlib.reload(C)
class OpError(RuntimeError):pass
class PhaseFailed(RuntimeError):pass

# ---------------------------------------------------------------------------------------------------------------------
# step [1]: engine sources (git blob locks) and historical reference
# ---------------------------------------------------------------------------------------------------------------------
def load_engine_sources():
    r716=fetch_locked("716.py");fetch_locked("709.py")
    if "PDF_SHA='"+PDF_SHA256+"'" not in r716.decode("utf-8"):raise RuntimeError("TEST716 STRUCTURE: PDF lock differs from this program")
    if os.path.isdir("/content"):Path("/content/716.py").write_bytes(r716)   # the verified, identical 716.py that the processes execute
    slog("ENGINE_SOURCE","716.py and 709.py verified",blob_716=SOURCES["716.py"]["git_blob"],blob_709=SOURCES["709.py"]["git_blob"])
def load_historical():
    out={}
    for n in HISTORICAL:
        r=fetch_locked(n);(HIST_DIR/("HISTORICAL_"+n)).write_bytes(r);out[n]=LOCKS[n]
    (HIST_DIR/"README_HISTORICAL.txt").write_text(
        "These files are PUBLISHED RECORDS OF EARLIER RUNS (TEST716, TEST717, TEST718), verified against their git blob identifiers.\n"
        "They are NOT results of this session. Live results of this session are in the session files and in records_process1/2.\n"
        +"".join(f"{n}: git blob {LOCKS[n]}\n" for n in HISTORICAL),encoding="utf-8")
    slog("HISTORICAL_LOADED","published TEST716/717/718 logs verified (reference only, not this session)",blobs=out);return out
def sources_step():
    load_engine_sources();h=load_historical()
    fetch_locked("LICENSE");(SESSION_DIR/"LICENSE.txt").write_bytes((EVIDENCE_DIR/"LICENSE").read_bytes())
    need={"TEST719_common.py","TEST719_demo_build.py","TEST719_demo_ask.py","TEST719_demo_questions.json","TEST719_demo_build_config.json"}
    if set(PROGRAM)!=need:raise RuntimeError(f"PROGRAM FILES: expected {sorted(need)}, written {sorted(PROGRAM)}")
    for k,v in PROGRAM.items():_OUT.write(f"  program  {k:<34} {v['bytes']:>8,} bytes · SHA-256 {v['sha256'][:16]}…\n")
    _OUT.flush();dump_json(SESSION_DIR/"PROGRAM_FILES.json",PROGRAM)
    return dict(sources={k:v["git_blob"] for k,v in SOURCES.items()},historical=list(h),program={k:v["sha256"] for k,v in PROGRAM.items()})

# ---------------------------------------------------------------------------------------------------------------------
# step [4]: the five fixed questions — mandatory source check on the real PDF, then the seal (no model is loaded yet)
# ---------------------------------------------------------------------------------------------------------------------
QFILE=PROGRAM_DIR/"TEST719_demo_questions.json";CFGFILE=PROGRAM_DIR/"TEST719_demo_build_config.json"
SEAL_FILE=RUNS/"SEAL.json";SRC_CHECK_FILE=RUNS/"pdf_source_check.json";PHASES_FILE=RUNS/"PHASES.json"
def norm(s):
    s=unicodedata.normalize("NFKC",s or "")
    for a,b in {"“":'"',"”":'"',"‘":"'","’":"'"}.items():s=s.replace(a,b)
    return re.sub(r"\s+"," ",s).strip().lower()
def snippet(text,m,w=90):return re.sub(r"\s+"," ",text[max(0,m.start()-w):m.end()+w]).strip()
def verify_sources(Q):
    """every expected answer must be found on the real PDF inside the declared cartridge page range (window never leaves it)"""
    pages=[norm(t) for t in DOC_PAGES];out={}
    for q in Q["questions"]:
        evs=[]
        for ev in q["evidence"]:
            targets=[f"C{i+1:02d}" for i in range(N_CART)] if ev["cartridge"]=="EVERY" else [ev["cartridge"]];per={}
            for cid in targets:
                a,b=BOUNDS[int(cid[1:])-1];hit=None
                for pg in range(max(a,ev.get("min_page",1)),b+1):
                    win=" ".join(pages[pg-1:min(b,pg+ev.get("window",1)-1)])
                    ms=[re.search(pat,win) for pat in ev["all"]]
                    if all(ms):hit=dict(pdf_page=pg,cartridge=cid,snippets=[snippet(win,m) for m in ms]);break
                per[cid]=hit
            evs.append(dict(cartridge=ev["cartridge"],patterns=ev["all"],found=({k:v for k,v in per.items() if v} if ev["cartridge"]=="EVERY" else per[targets[0]]),verified=all(per.values())))
        out[q["id"]]=dict(evidence=evs,verified=all(e["verified"] for e in evs))
    return out
def phases():return jload(PHASES_FILE,{}) or {}
def set_phase(name,**kw):
    ph=phases();ph.setdefault(name,{}).update(jsafe(kw));dump_json(PHASES_FILE,ph)
def panel_step():
    Q=json.loads(QFILE.read_text(encoding="utf-8"));cfg_text=norm(CFGFILE.read_text(encoding="utf-8"))
    if SEAL_FILE.is_file():
        s_=jload(SEAL_FILE,{})
        if s_.get("questions_sha256")==sha_file(QFILE) and s_.get("build_config_sha256")==sha_file(CFGFILE) and all(v.get("verified") for v in (s_.get("pdf_source_check") or {}).values()) and s_.get("pdf_source_check"):
            src=s_["pdf_source_check"];dump_json(PANEL_FILE,dict(seal=s_,note="existing seal of this experiment directory, re-verified (re-run)"))
            slog("SEAL","existing seal verified (re-run)",sealed_utc=s_["sealed_utc"],questions_sha256=s_["questions_sha256"]);_print_panel(Q,src);return dict(sealed_utc=s_["sealed_utc"],reused=True)
        if (phases().get("ASK") or {}).get("status"):
            raise PhaseFailed("SEAL.json exists, the question panel / build configuration changed and process 2 has already run: refusing to re-seal (delete /content/T719_RUNS to start a new experiment)")
        arch=RUNS/f"SEAL_superseded_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json";shutil.copyfile(SEAL_FILE,arch);SEAL_FILE.unlink()
        slog("SEAL","program/configuration changed before any question was asked to a model — previous seal archived, panel checked and sealed again",archived=arch.name)
    leaks=[]
    for q in Q["questions"]:
        for s_ in [q["text"],q["verifiable_answer"]]+q.get("leak_keywords",[]):
            if re.search(r"(?<![a-z0-9])"+re.escape(norm(s_))+r"(?![a-z0-9])",cfg_text):leaks.append(f"{q['id']}: {s_}")
    if leaks:raise PhaseFailed("QUESTION LEAK: the synthesis configuration contains question material: "+repr(leaks))
    src=verify_sources(Q);g=gpu_state();dump_json(SRC_CHECK_FILE,src)
    _print_panel(Q,src)
    bad=[k for k,v in src.items() if not v["verified"]]
    if bad:
        dump_json(PANEL_FILE,dict(pdf_source_check=src,sealed=False,unverified=bad))
        slog("SOURCE_CHECK","FAILED",unverified=bad)
        raise PhaseFailed(f"PDF SOURCE CHECK FAILED for {bad}: the expected answer was not found on the real PDF in the declared cartridge page range. "
                          "Stopping before any model is loaded. Details: QUESTION_PANEL_SOURCE_CHECK.json")
    s_=dict(test="TEST719",sealed_utc=utc_now(),questions_sha256=sha_file(QFILE),build_config_sha256=sha_file(CFGFILE),
            program_sha256={k:v["sha256"] for k,v in PROGRAM.items()},pdf_sha256=PDF_SHA256,pdf_source_check=src,
            synthesis_independence_check=dict(checked="question texts, verifiable answers and per-question keywords against the build configuration",leaks=[],passed=True),
            gpu_at_seal=g,statement="Sealed automatically in this run before any model weights were loaded (no GPU process at seal time). The build process never reads the questions.")
    if g.get("apps"):raise PhaseFailed(f"GPU not empty at seal time: {g['apps']}")
    dump_json(SEAL_FILE,s_);dump_json(PANEL_FILE,dict(seal=s_))
    slog("SEAL","question panel sealed before any model load; all five expected answers found on the PDF",questions_sha256=s_["questions_sha256"])
    return dict(sealed_utc=s_["sealed_utc"],questions_sha256=s_["questions_sha256"],verified=len(src))
def _print_panel(Q,src):
    for q in Q["questions"]:
        v=src.get(q["id"],{});_OUT.write(f"  {q['id']} {'✓ verified on the PDF' if v.get('verified') else '✗ NOT FOUND on the PDF'} · region {q.get('region')}\n      Q: {q['text']}\n      expected: {q['verifiable_answer']}\n")
        for ev in v.get("evidence",[]):
            f=ev.get("found") or {}
            if ev["cartridge"]=="EVERY":_OUT.write(f"      evidence: '{ev['patterns'][0]}' found in {len(f)}/{N_CART} cartridges\n")
            elif f:_OUT.write(f"      evidence: {f['cartridge']} PDF page {f['pdf_page']} · “{short(f['snippets'][-1],150)}”\n")
            else:_OUT.write(f"      evidence: {ev['cartridge']} — patterns {ev['patterns']} NOT found\n")
    _OUT.flush()
def short(s,n):s=" ".join(str(s or "").split());return s if len(s)<=n else s[:n-1].rstrip()+"…"

# ---------------------------------------------------------------------------------------------------------------------
# steps [5] and [6]: the two separate Python processes — output shown live, stored line by line with UTC time stamps
# ---------------------------------------------------------------------------------------------------------------------
PROC_LINES=[];HEARTBEATS=[];HEARTBEAT_FILE=SESSION_DIR/"HEARTBEAT_LAST.json"
STAGE_TITLES={"boot_and_C01-C10":"unchanged TEST716 set-up: PDF lock, frozen Qwen2.5-72B NF4, ten CUT3 cartridges C01–C10 (real download / loading progress follows)",
              "S1-S5_joint_and_final_synthesis":"S1–S5 written as cartridges, physically joined (initialize S1 → append S2…S5), general final synthesis",
              "C11_write_and_handoff":"C11 written as a CUT3 cartridge (SHA-256) + hand-off for the new process",
              "independence_before_boot":"isolation checks BEFORE the model is loaded (new process, empty GPU, file-system scan, quarantine)",
              "model_boot_C11_only":"frozen model (unchanged 716 model statements) + ONLY C11 in the cartridge registry",
              "questions":"C11 mounted alone, GPU memory audit, five sealed questions; then the same questions without any document"}
def _stage_title(name):
    m=re.match(r"pair(\d)(_retry\d)?$",name)
    if m:a,b=PAIRS[int(m.group(1))-1];return f"physical pair P{m.group(1)}: initialize({a}) → append({b}) · 80-layer SHA-256 · X-ray · general synthesis"+(" — REBUILT after a GPU memory recovery" if m.group(2) else "")
    return STAGE_TITLES.get(name,name)
def _hf_cache_bytes():
    try:
        from huggingface_hub.constants import HF_HOME;root=Path(HF_HOME)       # whole cache: hub blobs + Xet chunk store + temporary files
    except Exception:root=Path.home()/".cache"/"huggingface"
    tot=0
    for dp,dn,fn in os.walk(root):
        for f in fn:
            try:tot+=os.stat(os.path.join(dp,f),follow_symlinks=False).st_size
            except Exception:pass
    return tot
def _heartbeat(stop,t0,name,every=60):
    """observer only (no CUDA calls): every 60 s one line with the state of the running process"""
    while not stop.wait(every):
        try:smi=subprocess.run(["nvidia-smi","--query-gpu=memory.used,memory.total,utilization.gpu","--format=csv,noheader,nounits"],capture_output=True,text=True,timeout=20).stdout.strip()
        except Exception:smi=None
        try:
            mi=dict(l.split(":",1) for l in Path("/proc/meminfo").read_text().splitlines() if ":" in l);ram=round(int(mi["MemAvailable"].split()[0])/2**20,1)
        except Exception:ram=None
        last=PROC_LINES[-1] if PROC_LINES else (None,None,None,"(no process output yet)")
        hb=dict(utc=utc_now(),process=name,elapsed_min=round((time.perf_counter()-t0)/60,1),process_lines=len(PROC_LINES),last_line_utc=last[0],last_line=str(last[3])[:200],
                gpu_mib_used_total_util=smi,ram_available_gib=ram,model_cache_gib=round(_hf_cache_bytes()/2**30,1))
        HEARTBEATS.append(hb)
        try:dump_json(HEARTBEAT_FILE,dict(hb,note="last heartbeat of the running process"))
        except Exception:pass
        _OUT.write(f"\n  ⏱ {name} +{hb['elapsed_min']} min · lines {hb['process_lines']} · last: {hb['last_line'][:90]} · GPU {smi} MiB/%, RAM {ram} GiB free, Hugging Face cache {hb['model_cache_gib']} GiB\n");_OUT.flush()
        with _LOG_LOCK:
            with SESSION_LOG.open("a",encoding="utf-8") as f:f.write(f"{hb['utc']} HEARTBEAT          {json.dumps(hb,ensure_ascii=False)}\n")
QUIET=("FORGE_PROGRESS","APPEND_PROGRESS","APPEND_DIAG")
def run_proc(name,script,env):
    g=gpu_state()
    if g.get("apps"):slog("GPU_NOT_EMPTY",f"{name}: another GPU process is present before the start — recorded (process 2 reports it in its isolation record)",apps=g["apps"])
    e=dict(os.environ);e.update({k:str(v) for k,v in env.items()});e["PYTHONUNBUFFERED"]="1"
    cons=RUNS/"console";cons.mkdir(parents=True,exist_ok=True);lp=cons/f"{name}.log";tsv=cons/f"{name}_with_UTC_timestamps.tsv"
    st=utc_now();t=time.perf_counter();set_phase(name,status="RUNNING",start_utc=st);slog("PROCESS_START",name,script=script,gpu_used_mib=g.get("used_mib"))
    p=subprocess.Popen([sys.executable,"-u",script],cwd=str(PROGRAM_DIR),env=e,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stop=threading.Event();hb=threading.Thread(target=_heartbeat,args=(stop,t,name),daemon=True);hb.start()
    buf="";dec=__import__("codecs").getincrementaldecoder("utf-8")(errors="replace");progress=[False]
    def line_out(line):
        ts=utc_now();el=round(time.perf_counter()-t,3);PROC_LINES.append((ts,el,name,line))
        with lp.open("a",encoding="utf-8") as f:f.write(line+"\n")
        with tsv.open("a",encoding="utf-8") as f:f.write(f"{ts}\t{el}\t{line}\n")
        if any(x in line for x in QUIET):return
        m=re.match(r"\S+\s+STAGE_START\s+(\S+)",line)          # the event line itself, not a heartbeat that quotes it
        if progress[0]:_OUT.write("\n");progress[0]=False
        if m:_OUT.write("\n"+"·"*112+f"\n▶ {name} · {_stage_title(m.group(1))} · {local_now()} · +{el/60:.1f} min · {_gpu_short()}\n"+"·"*112+"\n")
        _OUT.write(f"  {name} │ {line[:300]}\n");_OUT.flush()
    try:
        fd=p.stdout.fileno()
        while True:
            chunk=os.read(fd,65536)
            if not chunk:break
            buf+=dec.decode(chunk)
            while "\n" in buf:
                line,buf=buf.split("\n",1);line_out(line.split("\r")[-1] if "\r" in line else line)
            if "\r" in buf:                          # live progress bars (download / loading) — shown, not stored per update
                seg=buf.split("\r")[-1]
                if seg.strip():_OUT.write(f"\r  {name} │ {seg[:200]}");_OUT.flush();progress[0]=True
                buf=seg
        if buf.strip():line_out(buf)
        rc=p.wait()
    finally:
        stop.set()
        if p.poll() is None:p.kill()
    end=utc_now();secs=round(time.perf_counter()-t,1)
    set_phase(name,status="COMPLETE" if rc==0 else "FAILED",end_utc=end,exit_code=rc,pid=p.pid,seconds=secs)
    slog("PROCESS_END",name,exit_code=rc,minutes=round(secs/60,1))
    if rc!=0:raise PhaseFailed(f"{name} process failed (exit {rc}); its last lines are above and in {lp}")
    return rc

def build_result():return jload(RUNS/"build_store"/"build_result.json",{}) or {}
def ask_result():return jload(ASK_DIR/"store"/"ask_result.json",{}) or {}
def _own_gpu_guard(name):
    g=gpu_state();own=[a for a in g.get("apps") or [] if a.split(",")[0].strip()==str(os.getpid())]
    if own:raise PhaseFailed(f"{name} has to run, but this notebook process still holds the model of an earlier run on the GPU {own}: Runtime → Restart session, then run again (completed phases are reused)")
def build_step():
    if phases().get("BUILD",{}).get("status")=="COMPLETE" and build_result().get("status")=="BUILD_COMPLETE" and (RUNS/"handoff"/"C11.pt").is_file():
        slog("SKIP","process 1 already complete in this experiment directory — its records are re-checked in step [7]")
    else:
        _own_gpu_guard("process 1")
        if (RUNS/"engine_dir_after_build").exists() and not ENGINE_DIR.exists():
            shutil.move(str(RUNS/"engine_dir_after_build"),str(ENGINE_DIR))      # re-run: C01–C10 reused only after 716's SHA-256 check
        try:run_proc("BUILD","TEST719_demo_build.py",{"T719_RUNS":str(RUNS)})
        except PhaseFailed as ex:
            raise PhaseFailed(f"PROCESS 1 stopped: {build_result().get('error') or ex}") from ex
        finally:_print_build()
    B=build_result()
    if B.get("status")!="BUILD_COMPLETE":raise PhaseFailed(f"PROCESS 1 status {B.get('status')}: {B.get('error')}")
    return dict(status=B["status"],c11_sha256=(B.get("C11") or {}).get("cartridge_sha256"),minutes=round((B.get("wall_seconds") or 0)/60,1))
def _print_build():
    B=build_result()
    if not B:return
    _OUT.write("\n  PROCESS 1 RESULT · status "+str(B.get("status"))+(f" · {B.get('error')}" if B.get("error") else "")+"\n")
    for p in B.get("pairs") or []:
        ap=p.get("append") or {};sy=p.get("synthesis") or {};em=sy.get("end_marker") or {}
        _OUT.write(f"  {p['pair']} {'+'.join(p['cartridges'])} · {ap.get('rows')} rows (expected {p.get('rows_expected')}) · append 80-layer SHA-256 {'PASS' if ap.get('verified') else 'FAIL'} · "
                   f"synthesis {sy.get('status')} (finish {sy.get('finish_reason')}, END marker {'last line' if em.get('at_end') else 'present' if em.get('present') else 'missing'}) · {sy.get('n_generated')} tokens · {sy.get('seconds')} s\n")
    for s in B.get("S") or []:_OUT.write(f"  {s['id']} cartridge · {s['body_tokens']} tokens · SHA-256 {s['cartridge_sha256'][:16]}…\n")
    j=B.get("joint") or {}
    if j:
        fi=j.get("final") or {};em=fi.get("end_marker") or {}
        _OUT.write(f"  S1–S5 joint · {j.get('rows')} rows · 4 appends {'PASS' if all(a.get('verified') for a in j.get('appends',[])) else 'FAIL'} · final synthesis {fi.get('status')} "
                   f"(finish {fi.get('finish_reason')}, END marker {'last line' if em.get('at_end') else 'present' if em.get('present') else 'missing'}) · {fi.get('n_generated')} tokens · {fi.get('seconds')} s\n")
    c=B.get("C11") or {}
    _OUT.write(f"  C11 · {c.get('body_tokens','—')} tokens · SHA-256 {c.get('cartridge_sha256','NOT WRITTEN')}\n" if c else "  C11 · NOT WRITTEN\n");_OUT.flush()

def ask_step():
    if phases().get("ASK",{}).get("status")=="COMPLETE" and ask_result().get("status")=="ASK_COMPLETE":
        slog("SKIP","process 2 already complete in this experiment directory — its records are re-checked in step [7]")
    else:
        b=phases()["BUILD"];_own_gpu_guard("process 2")
        if ENGINE_DIR.exists():
            dst=RUNS/"engine_dir_after_build";shutil.rmtree(dst,ignore_errors=True);shutil.move(str(ENGINE_DIR),str(dst))
            slog("QUARANTINE","build engine directory (C01–C10, S1–S5, PDF copy) moved into the quarantined area")
        shutil.rmtree(ASK_IN,ignore_errors=True);ASK_IN.mkdir(parents=True)
        for f in ("C11.pt","C11.sha256","handoff.json"):shutil.copyfile(RUNS/"handoff"/f,ASK_IN/f)
        shutil.rmtree(ASK_DIR,ignore_errors=True)
        try:
          try:
            run_proc("ASK","TEST719_demo_ask.py",{"T719_QUARANTINE":f"{RUNS}:{PRIVATE_DIR}","T719_ASK_OUT":str(ASK_DIR),"T719_HANDOFF":str(ASK_IN),
                                                   "T719_BUILD_EXIT_CODE":b.get("exit_code"),"T719_BUILD_ENDED_UTC":b.get("end_utc")})
          except PhaseFailed as ex:
            if not (ask_result().get("answers")):raise
            slog("PROCESS_NOTE","process 2 ended with an error after recording answers — the recorded answers are kept and the gap is reported",error=str(ex))
        finally:
            if ENGINE_DIR.exists():
                dst=RUNS/"engine_dir_after_ask";shutil.rmtree(dst,ignore_errors=True);shutil.move(str(ENGINE_DIR),str(dst))
            _print_ask()
    A=ask_result()
    if not A.get("answers"):raise PhaseFailed(f"PROCESS 2 produced no answer: status {A.get('status')}: {A.get('error')}")
    if A.get("status")!="ASK_COMPLETE":slog("PROCESS_NOTE",f"process 2 status {A.get('status')} — partial result, reported",error=A.get("error"))
    return dict(status=A["status"],answers=len(A.get("answers") or []),minutes=round((A.get("wall_seconds") or 0)/60,1))
def _print_ask():
    A=ask_result()
    if not A:return
    ind=A.get("independence") or {}
    _OUT.write("\n  PROCESS 2 RESULT · status "+str(A.get("status"))+(f" · {A.get('error')}" if A.get("error") else "")+"\n")
    for k,lab in ISO_LABELS:
        v=ind.get(k) or {};_OUT.write(f"  {'PASS' if v.get('pass') else 'FAIL' if v else '  — '}  {lab}\n")
    for r in A.get("answers") or []:
        _OUT.write(f"\n  ── {r['id']} · {r['condition']} · {r['status']} · finish {r.get('finish_reason')} · {r['n_generated']} tokens (ceiling {r['ceiling']}) · {r['seconds']} s\n"
                   f"  Q: {r['question']}\n"+"\n".join("  │ "+l for l in str(r["text"]).splitlines() or [""])+"\n")
    _OUT.flush()
ISO_LABELS=[("process","new Python process, started after process 1 exited (same Colab VM — not a separate machine)"),
            ("gpu_before_model_load","GPU empty before the model was loaded"),
            ("filesystem_scan","no C01–C10 / S1–S5 file and no pair-synthesis text outside the quarantined directories"),
            ("quarantine_audit","quarantined build directories never opened (audit hook)"),
            ("cartridge_directory","engine cartridge registry = C11 only"),
            ("same_weights_as_build","same frozen weights as process 1 (weight sentinel)"),
            ("c11_memory_audit","GPU memory above the model-only baseline = C11 K/V (allocator + unique storages)")]

# ---------------------------------------------------------------------------------------------------------------------
# automatic indicator per answer (fixed text rules, sealed before generation) — NOT expert verification
# ---------------------------------------------------------------------------------------------------------------------
ABSTAIN=re.compile(r"\bunknown\b|cannot (be )?(verif|determin|provid|find|confirm)|not (available|provided|specified|mentioned|contained|included)|does not (contain|mention|provide|specify|include)|no (information|mention)|do not have access|don't have access",re.I)
def evaluate(text,status,rule):
    if status=="ERROR":return "NOT_PRODUCED","generation failed after a recovery attempt — the error is in the records"
    if status=="INCOMPLETE":return "INCOMPLETE","safety ceiling reached; not counted as an answer"
    if status!="COMPLETE":return "UNVERIFIED_FINISH","the end of generation could not be confirmed as a stop token"
    t=norm(text)
    if ABSTAIN.search(t):return "UNCLEAR","the answer abstains (UNKNOWN / not available)"
    hits_any=[p for p in rule.get("correct_any",[]) if re.search(p,t)];alls=[bool(re.search(p,t)) for p in rule.get("correct_all",[])]
    bad=[p for p in rule.get("incorrect_any",[]) if re.search(p,t)];ok=bool(hits_any) or (bool(alls) and all(alls))
    if ok and not bad:return "CORRECT","rule met"
    if ok and bad:return "UNCLEAR","rule met but contradicting content present: "+repr(bad)
    if bad:return "INCORRECT","contradicts the source: "+repr(bad)
    if alls and any(alls):return "UNCLEAR","only part of the expected answer"
    return "INCORRECT","expected content not found"
def trace(text,rule):
    t=norm(text);alls=[bool(re.search(p,t)) for p in rule.get("correct_all",[])]
    if any(re.search(p,t) for p in rule.get("correct_any",[])) or (alls and all(alls)):return "yes"
    return "partly" if any(alls) else "no"

# ---------------------------------------------------------------------------------------------------------------------
# LIVE experiment record: everything below is computed from this run's records (process 1, process 2, the seal, the PDF)
# ---------------------------------------------------------------------------------------------------------------------
LIVE={}
def live_record():
    Q=json.loads(QFILE.read_text(encoding="utf-8"));seal=jload(SEAL_FILE,{}) or {};src=seal.get("pdf_source_check") or jload(SRC_CHECK_FILE,{}) or {}
    B=build_result();A=ask_result();fin_p=RUNS/"build_store"/"synthesis"/"FINAL.txt";final=fin_p.read_text(encoding="utf-8") if fin_p.is_file() else ""
    rows=[]
    for q in Q["questions"]:
        ans={}
        for r in A.get("answers") or []:
            if r["id"]==q["id"]:
                ev,why=evaluate(r["text"],r["status"],q["rule"])
                ans[r["condition"]]=dict(text=r["text"],status=r["status"],finish_reason=r.get("finish_reason"),finish_evidence=r.get("finish_evidence"),n_generated=r["n_generated"],
                                         ceiling=r["ceiling"],seconds=r["seconds"],sha256=r["sha256"],memory=r["memory"],memory_rows=r.get("memory_rows"),utc=r.get("utc"),evaluation=ev,why=why)
        rows.append(dict(id=q["id"],text=q["text"],verifiable_answer=q["verifiable_answer"],source=q["source"],region=q.get("region"),note=q.get("note"),
                         requires=q.get("requires_cartridges"),pdf_evidence=src.get(q["id"]),answers=ans,c11_body_trace=(trace(final,q["rule"]) if final else "n/a")))
    prov=((A.get("provenance") or B.get("provenance") or {}).get("mode")) or "n/a"
    return dict(provenance=prov,seal={k:seal.get(k) for k in ("sealed_utc","questions_sha256","build_config_sha256","pdf_sha256","statement")},question_design=Q.get("question_design"),
                evaluation_policy=Q.get("evaluation_policy"),questions=rows,build={k:B.get(k) for k in ("status","stages","pairs","S","joint","C11","weights_unchanged","sentinel_before","wall_seconds","error","engine","model_pin")},
                ask={k:A.get(k) for k in ("status","independence","c11","weights_unchanged","wall_seconds","error","engine","warmup","model_pin")},phases=phases(),
                final_synthesis_tokens=((B.get("joint") or {}).get("final") or {}).get("n_generated"),final_synthesis_sha256=(sha_bytes(final.encode()) if final else None))

def xray_metas():
    out={}
    for d in (RUNS/"build_store"/"xray",ASK_DIR/"store"/"xray"):
        for m in sorted(d.glob("*.json")) if d.is_dir() else []:out[m.stem]=jload(m,{})
    return out

def verify_disk():
    """re-hash every cartridge file of this experiment on disk and compare with the SHA-256 the processes recorded"""
    B=build_result();rows=[];t=time.perf_counter()
    src_dir=RUNS/"engine_dir_after_build"/"cartridges"
    want=[(b["id"],src_dir/(b["id"]+".pt"),b.get("cartridge_sha256")) for b in (B.get("sources") or [])]+[(s["id"],src_dir/(s["id"]+".pt"),s.get("cartridge_sha256")) for s in (B.get("S") or [])]
    if B.get("C11"):want.append(("C11 (hand-off)",RUNS/"handoff"/"C11.pt",B["C11"].get("cartridge_sha256")))
    if STATE.get("mount") and E.get("CART"):want.append(("C11 (interface copy)",Path(E["CART"])/"C11.pt",(B.get("C11") or {}).get("cartridge_sha256")))
    for cid,p,rec in want:
        h=sha_file(p) if p.is_file() else None
        rows.append(dict(cartridge=cid,file=str(p),bytes=(p.stat().st_size if p.is_file() else None),sha256=h,record_sha256=rec,equals_record=(h is not None and h==rec)))
    row=dict(utc=utc_now(),files=rows,passed=(len(rows)>=N_CART+N_PAIRS+1 and all(r["equals_record"] for r in rows)),seconds=round(time.perf_counter()-t,2))
    STATE["disk_checks"].append(row);slog("DISK_CHECK","PASS" if row["passed"] else "FAIL",files=len(rows),passed=row["passed"],seconds=row["seconds"]);return row

def compute_verification():
    """every record is checked; nothing here stops the run. Items are classed as
    INTEGRITY  (the physical memory / the answers are what they claim to be — a failure means the result is NOT valid),
    ISOLATION  (support for the claim 'C11 alone in a new process' — a failure means that claim is NOT supported),
    FORMAL     (format / observation / memory-profile notes — reported, they do not invalidate the computation)."""
    L=live_record();B=build_result();A=ask_result();ind=A.get("independence") or {};items=[]
    def add(name,ok,detail,cls="INTEGRITY"):items.append(dict(name=name,passed=bool(ok),detail=jsafe(detail),cls=cls))
    seal=jload(SEAL_FILE,{}) or {};src=seal.get("pdf_source_check") or {};ph=phases()
    add("SOURCE_PDF_SHA256_AND_PAGES",DOC.get("sha256")==PDF_SHA256 and DOC.get("pages")==PDF_PAGES,f"{DOC.get('pages')} pages · {str(DOC.get('sha256'))[:16]}…")
    add("ENGINE_SOURCE_LOCKS",all(SOURCES.get(k,{}).get("git_blob")==LOCKS[k] for k in ("716.py","709.py")),"716.py + 709.py git blobs")
    add("PROGRAM_FILES_SHA256",len(PROGRAM)==5 and all(sha_file(v["local"])==v["sha256"] for v in PROGRAM.values()),f"{len(PROGRAM)} files")
    add("PANEL_VERIFIED_ON_PDF_BEFORE_MODEL_LOAD",bool(src) and all(v.get("verified") for v in src.values()) and str(seal.get("sealed_utc",""))<str(ph.get("BUILD",{}).get("start_utc","~")),
        f"{sum(1 for v in src.values() if v.get('verified'))}/{len(src)} questions · sealed {seal.get('sealed_utc')} · process 1 started {ph.get('BUILD',{}).get('start_utc')}")
    add("PROCESS1_COMPLETE",ph.get("BUILD",{}).get("exit_code")==0 and B.get("status")=="BUILD_COMPLETE",B.get("status"))
    srcs=B.get("sources") or [];add("TEN_SOURCE_CARTRIDGES_C01_C10",len(srcs)==N_CART and all(b.get("cartridge_sha256") for b in srcs),f"{len(srcs)}/{N_CART}")
    pr=B.get("pairs") or []
    add("FIVE_PAIR_APPENDS_ALL_80_LAYERS_SHA256",len(pr)==N_PAIRS and all((p.get("append") or {}).get("verified") and (p.get("append") or {}).get("pass_line") and (p.get("append") or {}).get("rows")==p.get("rows_expected") for p in pr),
        f"{sum(1 for p in pr if (p.get('append') or {}).get('verified'))}/{N_PAIRS} · engine line PASS APPEND_ALL_80_LAYERS_EXACT_SHA256")
    add("FIVE_PAIR_SYNTHESES_ACCEPTED_NOT_CUT",len(pr)==N_PAIRS and all((p.get("synthesis") or {}).get("accepted") for p in pr),[f"{p['pair']}: {(p.get('synthesis') or {}).get('status')} / {(p.get('synthesis') or {}).get('finish_reason')}" for p in pr])
    j=B.get("joint") or {}
    add("S1_S5_WRITTEN_AND_PHYSICALLY_JOINED",len(B.get("S") or [])==N_PAIRS and len(j.get("appends") or [])==4 and all(a.get("verified") for a in j.get("appends") or []),f"{len(B.get('S') or [])} cartridges · {len(j.get('appends') or [])} appends")
    add("FINAL_SYNTHESIS_ACCEPTED_NOT_CUT",(j.get("final") or {}).get("accepted"),f"{(j.get('final') or {}).get('status')} / {(j.get('final') or {}).get('finish_reason')} · {(j.get('final') or {}).get('n_generated')} tokens")
    c11=B.get("C11") or {};hp=RUNS/"handoff"/"C11.pt"
    add("C11_WRITTEN_SHA256",bool(c11) and hp.is_file() and sha_file(hp)==c11.get("cartridge_sha256"),str(c11.get("cartridge_sha256"))[:16]+"…")
    ans=A.get("answers") or []
    add("TEN_ANSWERS_RECORDED",sum(1 for a in ans if a.get("status")!="ERROR")==10 and {a["condition"] for a in ans}=={"C11","NO_DOCUMENT"},f"{sum(1 for a in ans if a.get('status')!='ERROR')}/10 raw answers produced (5 × C11 alone, 5 × no document)")
    add("WEIGHT_SENTINEL_UNCHANGED",bool(B.get("weights_unchanged")) and bool(A.get("weights_unchanged")),"process 1 and process 2")
    d=verify_disk();add("CARTRIDGE_FILES_SHA256_ON_DISK",d["passed"],f"{sum(1 for r in d['files'] if r['equals_record'])}/{len(d['files'])} files (C01–C10, S1–S5, C11)")
    add("PROCESS2_COMPLETE",ph.get("ASK",{}).get("exit_code")==0 and A.get("status")=="ASK_COMPLETE",A.get("status"),"ISOLATION" if A.get("answers") else "INTEGRITY")
    for k,lab in ISO_LABELS:add("ISOLATION_"+k.upper(),(ind.get(k) or {}).get("pass"),lab,"ISOLATION")
    xm=xray_metas();need=[f"P{k+1}_{a}+{b}_joint" for k,(a,b) in enumerate(PAIRS)]+["S1-S5_joint","C11"]
    add("XRAYS_FROM_LIVE_KV",all(n in xm and xm[n].get("finite") and xm[n].get("layers")==EXPECTED_ARCH[0] for n in need),f"{sum(1 for n in need if n in xm)}/{len(need)} (five pairs, S1–S5 joint, C11 alone)","FORMAL")
    flags=[(p["pair"],f) for p in pr for f in (p.get("synthesis") or {}).get("flags") or []]+[("FINAL",f) for f in (j.get("final") or {}).get("flags") or []]
    add("SYNTHESIS_FORMAT_AND_FINISH_FLAGS",not flags,[f"{a}: {b}" for a,b in flags] or "none","FORMAL")
    rec_=B.get("memory_recoveries") or [];prof=B.get("memory_profile") or {}
    nondef={k:v for k,v in prof.items() if (v.get("chunk_tokens"),v.get("reserve_gib"))!=(256,9.0)}
    add("DEFAULT_MEMORY_PROFILE_USED",not rec_ and not nondef,(f"{len(rec_)} recoveries · profiles {nondef}" if (rec_ or nondef) else "chunk 256 · reserve 9 GiB")+f" · cached-memory releases before the reserve check: {(B.get('ensure_room_recoveries') or {}).get('count',0)}","FORMAL")
    notes=(A.get("notes") or [])+[dict(kind="PROCESS1_MEMORY_NOTE",detail=n) for n in (B.get("memory_notes") or [])]
    add("NO_PROCESS_NOTES",not notes,[n["kind"] for n in notes] or "none","FORMAL")
    integ=[i for i in items if i["cls"]=="INTEGRITY"];iso=[i for i in items if i["cls"]=="ISOLATION"];form=[i for i in items if i["cls"]=="FORMAL"]
    result=("VALID" if all(i["passed"] for i in integ) else "NOT VALID — integrity failure: "+", ".join(i["name"] for i in integ if not i["passed"]))
    isolation=("SUPPORTED" if all(i["passed"] for i in iso) else "NOT SUPPORTED — "+", ".join(i["name"] for i in iso if not i["passed"]))
    rec=dict(session=SESSION_ID,utc=utc_now(),ready=all(i["passed"] for i in integ),passed=sum(i["passed"] for i in items),total=len(items),items=items,provenance=L["provenance"],
             result=result,isolation=isolation,formal_gaps=[i["name"] for i in form if not i["passed"]],
             semantics="NOT VERIFIED — answers are raw model output; the indicator is an automatic text rule fixed before generation")
    STATE["verification"]=rec;dump_json(VERIFY_FILE,rec);dump_json(LIVE_MEAS,L)
    LIVE.clear();LIVE.update(L)
    slog("VERIFICATION",result,isolation=isolation,passed=rec["passed"],total=rec["total"],failed=[i["name"] for i in items if not i["passed"]]);return rec

# ---------------------------------------------------------------------------------------------------------------------
# step [8]: the interface memory — model + ONLY C11 in THIS notebook process (process 2 has ended; GPU must be empty)
# ---------------------------------------------------------------------------------------------------------------------
KENG=None;ENGINE_LOCK=threading.RLock();KLOG_FILE=SESSION_DIR/"INTERFACE_ENGINE_EVENTS.jsonl"
class _KLog:
    def ev(self,kind,msg="",/,**data):
        with KLOG_FILE.open("a",encoding="utf-8") as f:f.write(json.dumps(jsafe(dict(utc=utc_now(),kind=kind,msg=msg,data=data)),ensure_ascii=False)+"\n")
        _OUT.write(f"  engine │ {kind:<18} {msg} {short(json.dumps(jsafe(data),ensure_ascii=False),200) if data else ''}\n");_OUT.flush()
def _require():
    if KENG is None or STATE.get("memory") is None:raise OpError("The interface memory (frozen model + C11) is not loaded in this session.")
def engine_architecture():
    if not E.get("model"):
        eng=(build_result().get("engine") or {});a=eng.get("arch")
        if not a:return None
        NL,H,QH,KVH,HD=a;return dict(layers=NL,hidden=H,q_heads=QH,kv_heads=KVH,head_dim=HD,cut=EXPECTED_CUT,prefix_tokens=eng.get("P"),full_kv_bytes_per_token=NL*KVH*HD*2*2,
                                       weights="NF4 4-bit (bitsandbytes), BF16 compute, frozen",model_id=MODEL_ID,source="process 1 record")
    return dict(layers=E["NL"],hidden=E["H"],q_heads=E["QH"],kv_heads=E["KVH"],head_dim=E["HD"],cut=E["CUT"],prefix_tokens=E.get("P"),full_kv_bytes_per_token=E["NL"]*E["KVH"]*E["HD"]*2*2,
                chunk=E.get("CHUNK"),reserve_gib=E.get("GPU_RESERVE_GIB"),weights="NF4 4-bit (bitsandbytes), BF16 compute, frozen",model_id=E.get("MODEL_ID",MODEL_ID),source="this notebook process")
def ready_memory():
    global KENG,E
    g=gpu_state();own=[a for a in g.get("apps") or [] if a.split(",")[0].strip()==str(os.getpid())];other=[a for a in g.get("apps") or [] if a not in own]
    if other:raise RuntimeError(f"READY MEMORY: another process is using the GPU {other} — Runtime → Restart session, then run again (completed phases are reused)")
    if own:
        found=[o for o in __import__("gc").get_objects() if type(o).__name__=="Engine" and isinstance(getattr(o,"E",None),dict) and o.E.get("model") is not None]
        if found:return _reuse_loaded_engine(own)
        import torch;__import__("gc").collect();torch.cuda.empty_cache()     # an earlier run left only cached memory: release it, then load normally
        slog("READY_MEMORY_NOTE","no loaded engine of an earlier run found in this notebook process — cached GPU memory released, loading normally",apps=own)
    import torch
    prov=C.provenance(torch);klog=_KLog();hd=jload(RUNS/"handoff"/"handoff.json",{})
    saved={k:os.environ.get(k) for k in ("HF_HUB_OFFLINE","TRANSFORMERS_OFFLINE")}
    with ENGINE_LOCK:
        pin=C.pin_model_revision(klog,prov["mode"])
        try:
            KENG=C.Engine(klog,prov["mode"]);info=KENG.boot(model_only=True)
        finally:
            for k,v in saved.items():                      # the model is loaded: give the network back to the interface (share link)
                if v is None:os.environ.pop(k,None)
                else:os.environ[k]=v
        E=KENG.E;CART=Path(E["CART"])
        for f in CART.iterdir():f.unlink()
        E["R"]["books"]=[]
        shutil.copyfile(RUNS/"handoff"/"C11.pt",CART/"C11.pt");shutil.copyfile(RUNS/"handoff"/"C11.sha256",CART/"C11.sha256");KENG.register_existing(hd["allowed"]["C11"])
        t=time.perf_counter();memory,mrec=KENG.mount("C11")
        STATE["memory"]=memory;STATE["mount"]=dict(mrec,end_to_end_s=round(time.perf_counter()-t,2),gpu=E["mem"]());STATE["ops"].append(STATE["mount"])
    w=verify_weights()
    if not w["passed"]:raise RuntimeError("READY MEMORY: the weight sentinel of this process differs from process 1")
    slog("READY_MEMORY","frozen model + C11 mounted in this notebook process",rows=mrec["rows"],commit=info.get("commit_hash"),pin=pin.get("pinned"))
    return dict(rows=mrec["rows"],seconds=STATE["mount"]["end_to_end_s"],weights_equal_process1=w["passed"])
def _reuse_loaded_engine(own):
    """the cell was run again in the same notebook process: the frozen model loaded by the earlier run is still in GPU memory.
    It is found and reused (no second copy would fit); C11 is mounted again from the SHA-checked hand-off and the weights are
    compared with process 1."""
    global KENG,E
    import gc as _gc
    old=[o for o in _gc.get_objects() if type(o).__name__=="Engine" and isinstance(getattr(o,"E",None),dict) and o.E.get("model") is not None]
    if not old:raise RuntimeError(f"READY MEMORY: this notebook process holds GPU memory {own} but no loaded engine was found — Runtime → Restart session, then run again (completed phases are reused)")
    hd=jload(RUNS/"handoff"/"handoff.json",{})
    with ENGINE_LOCK:
        KENG=old[-1];E=KENG.E;KENG.log=_KLog();CART=Path(E["CART"]);CART.mkdir(parents=True,exist_ok=True)
        for f in CART.iterdir():
            if f.is_file():f.unlink()
        E["R"]["books"]=[]
        shutil.copyfile(RUNS/"handoff"/"C11.pt",CART/"C11.pt");shutil.copyfile(RUNS/"handoff"/"C11.sha256",CART/"C11.sha256");KENG.register_existing(hd["allowed"]["C11"])
        KENG.free_cached() if hasattr(KENG,"free_cached") else E["free_gpu"]()
        t=time.perf_counter();memory,mrec=KENG.mount("C11")
        STATE["memory"]=memory;STATE["mount"]=dict(mrec,end_to_end_s=round(time.perf_counter()-t,2),gpu=E["mem"](),reused_model_of_earlier_run=True);STATE["ops"].append(STATE["mount"])
    w=verify_weights()
    if not w["passed"]:raise RuntimeError("READY MEMORY: the weight sentinel of the reused model differs from process 1")
    slog("READY_MEMORY","frozen model of the earlier run in this notebook process reused + C11 mounted",rows=mrec["rows"])
    return dict(rows=mrec["rows"],seconds=STATE["mount"]["end_to_end_s"],weights_equal_process1=w["passed"],reused_model=True)
def ntok(text):
    try:return len(E["tok"](str(text or ""),add_special_tokens=False).input_ids)
    except Exception:return None
def ask_live(question,use_memory=True,origin="user"):
    """an interface question: answer(C11 memory or None, question), up to INTERACTIVE_MAX_NEW tokens; NOT part of the sealed panel"""
    with ENGINE_LOCK:
        _require();q=(question or "").strip()
        if not q or len(q)>3000:raise OpError("The question must contain 1–3000 characters.")
        r=KENG.answer(STATE["memory"] if use_memory else None,q,INTERACTIVE_MAX_NEW,EXPECTED_RESERVE_GIB,("C11:" if use_memory else "NO_DOCUMENT:")+origin)
        row=dict(utc=r["utc"],origin=origin,question=q,raw=r["text"],status=r["status"],finish_reason=r["finish_reason"],n_generated=r["n_generated"],ceiling=r["ceiling"],
                 cartridge=("C11" if use_memory else None),with_memory=bool(use_memory),cache_tokens=(KENG.rows(STATE["memory"]) if use_memory else 0),seconds=r["seconds"],gpu=E["mem"](),
                 sealed_panel=False,semantics="NOT VERIFIED")
        (STATE["qa"] if use_memory else STATE["controls"]).append(row)
        with SESSION_QA.open("a",encoding="utf-8") as f:f.write(json.dumps(jsafe(row),ensure_ascii=False)+"\n")
        slog("QA" if use_memory else "QA_NO_DOCUMENT",row["cartridge"] or "NO DOCUMENT",question=q[:300],status=row["status"],seconds=row["seconds"]);return row
def verify_weights():
    with ENGINE_LOCK:
        if KENG is None:raise OpError("The model is not loaded in this notebook process.")
        t=time.perf_counter();after=E["sentinel"]();before=build_result().get("sentinel_before")
        row=dict(utc=utc_now(),passed=(before is not None and after==before),before=before,after=after,seconds=round(time.perf_counter()-t,2),reference="weight sentinel of process 1 at load")
        STATE["weight_checks"].append(row);slog("WEIGHT_CHECK","PASS" if row["passed"] else "FAIL",**row);return row
def release_memory(reason):
    if STATE.get("memory") is not None:
        STATE["memory"]=None
        try:E["free_gpu"]()
        except Exception:pass
        slog("MEMORY_RELEASED",reason)

# ---------------------------------------------------------------------------------------------------------------------
# THREE RESEARCH FIGURES (JPEG 300 dpi, PNG lossless, PDF vector) — values ONLY from this run's records
# ---------------------------------------------------------------------------------------------------------------------
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.linewidth":.9,"axes.edgecolor":"#374151","axes.labelcolor":"#111827",
                     "xtick.color":"#374151","ytick.color":"#374151","xtick.labelsize":10.5,"ytick.labelsize":10.5,"axes.labelsize":12,
                     "axes.titlesize":13,"axes.titleweight":"bold","axes.titlelocation":"left","legend.fontsize":10.5,"legend.frameon":False})
FW,FH=13.333,7.5;OUT_DPI=300
INK,INK2,MUTED,RULE,PANEL="#111827","#374151","#6B7280","#D1D5DB","#F8FAFC"
TEAL,RED,AMBER,GREY="#0F766E","#B91C1C","#B45309","#9CA3AF"
STATUS_COL={"CORRECT":"#047857","INCORRECT":RED,"UNCLEAR":AMBER,"INCOMPLETE":"#6D28D9","UNVERIFIED_FINISH":"#92400E","NOT_PRODUCED":GREY}
FIGURES=OrderedDict([("F1","Figure 1 — Five physical pair memories: 80-layer K/V X-ray"),
                     ("F2","Figure 2 — S1–S5 joint memory and the new cartridge C11"),
                     ("F3","Figure 3 — Five fixed questions: C11 alone vs no document")])
FIG_FILES={}
def mt(s):return str(s).replace("$",r"\$")
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
def _is_live():return LIVE.get("provenance")=="GPU_REAL"
def fig_base(k,title,subtitle,h=FH):
    fig=plt.figure(figsize=(FW,h),dpi=100,facecolor="white");s=FH/h
    badge,badge_col=("LIVE A100 MEASUREMENT",TEAL) if _is_live() else ("SIMULATION — NOT A RESULT",RED)
    b=fig.text(.965,1-.05*s,badge,fontsize=10.5,weight="bold",color=badge_col,va="center",ha="right",bbox=dict(boxstyle="square,pad=0.4",fc="white",ec=badge_col,lw=1.2))
    bx0=_bb(fig,b).x0-.015
    fig.text(.035,1-.05*s,f"Fig. {k}",fontsize=15,weight="bold",color=MUTED,va="center")
    ftext(fig,.095,1-.05*s,title,xmax=bx0,minsize=12,fontsize=18,weight="bold",color=INK,va="center")
    ftext(fig,.035,1-.095*s,subtitle,minsize=8,fontsize=12,color=INK2,va="center")
    fig.add_artist(Line2D([.035,.965],[1-.122*s,1-.122*s],transform=fig.transFigure,color=INK2,lw=.8))
    if not _is_live():
        fig.text(.5,.45,"SIMULATION — NOT EXPERIMENTAL DATA",fontsize=40,color=RED,alpha=.12,rotation=18,ha="center",va="center",weight="bold",gid="qc-ignore",zorder=100)
    return fig
def fig_footer(fig,k,note,h=FH):
    s=FH/h
    fig.add_artist(Line2D([.035,.965],[.075*s,.075*s],transform=fig.transFigure,color=RULE,lw=.7))
    ftext(fig,.035,.05*s,note,minsize=7.5,fontsize=10,color=INK2,va="center")
    qs=str((LIVE.get("seal") or {}).get("questions_sha256"))[:10]
    ftext(fig,.035,.022*s,f"{APP_SHORT} · {ORG} · {LICENSE_NAME} · {COPYRIGHT} · 716.py {LOCKS['716.py'][:10]} · panel {qs} · live session {SESSION_ID} · Fig. {k}/{len(FIGURES)}",
          minsize=6,fontsize=8.6,color=MUTED,va="center",family="DejaVu Sans Mono")
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
    stem=("" if _is_live() else "SIMULATION_")+f"FIGURE_{k:02d}_{key}"
    jpg=FIG_DIR/(stem+".jpg");png=FIG_DIR/(stem+".png");pdf=FIG_DIR/(stem+".pdf")
    fig.savefig(pdf,facecolor="white");buf=io.BytesIO();fig.savefig(buf,format="png",dpi=OUT_DPI,facecolor="white");plt.close(fig)
    png.write_bytes(buf.getvalue())
    with Image.open(io.BytesIO(buf.getvalue())) as im:im.convert("RGB").save(jpg,"JPEG",quality=95,optimize=True,subsampling=0,dpi=(OUT_DPI,OUT_DPI))
    jq=jpeg_qc(jpg);size=tuple(jq["pixels"])
    rec=dict(key=key,figure=k,title=FIGURES[f"F{k}"],jpg=str(jpg),png=str(png),pdf=str(pdf),pixels=list(size),jpg_bytes=jpg.stat().st_size,sha256_jpg=sha_file(jpg),utc=utc_now(),
             layout_qc=dict(passed=qc["passed"],texts=qc["texts"],fix_rounds=qc["rounds"],font_reductions=qc["fixed"]),jpeg_qc=jq,provenance=LIVE.get("provenance"),
             data="live session "+SESSION_ID+" · values traceable in LIVE_MEASUREMENTS.json / VERIFICATION_RECORD.json / records_process1 / records_process2")
    flog(f"FIGURE {k} {key} {size[0]}x{size[1]} jpg sha256 {rec['sha256_jpg']}");return rec
def _npz(p):
    if not Path(p).is_file():return None
    z=np.load(p);return z["K"],z["V"]
def binned(a,b=256):
    nb=int(np.ceil(a.shape[1]/b));return np.stack([a[:,i*b:(i+1)*b].mean(axis=1) for i in range(nb)],axis=1)
def _xray_ok(meta):
    if not meta:return False
    if _is_live() and meta.get("provenance")!="GPU_REAL":raise RuntimeError("an X-ray record of this run is not a GPU measurement: "+str(meta.get("label")))
    return True

def fig1(k=1):
    a=engine_architecture() or {};xm=xray_metas();data=[]
    for i,(ca,cb) in enumerate(PAIRS,1):
        j=_npz(RUNS/"build_store"/"xray"/f"P{i}_{ca}+{cb}_joint.npz");al=_npz(RUNS/"build_store"/"xray"/f"P{i}_{ca}_alone.npz")
        if j is not None and _xray_ok(xm.get(f"P{i}_{ca}+{cb}_joint")):data.append((f"P{i} · {ca}+{cb}",j[0],j[1],(al[0].shape[1] if al is not None else None)))
    if len(data)!=N_PAIRS:raise RuntimeError(f"pair X-ray records: {len(data)}/{N_PAIRS}")
    fig=fig_base(k,"Five physical pair memories — 80-layer K/V X-ray of the live GPU memory",
                 f"initialize(C_odd) → append(C_even) · all prior K/V bytes of all {a.get('layers',80)} layers verified by exact SHA-256 · measured read-only before each synthesis")
    lims=[(np.percentile(np.concatenate([binned(d[i]).ravel() for d in data]),2),np.percentile(np.concatenate([binned(d[i]).ravel() for d in data]),98)) for i in (1,2)]
    x0,wd,gap=.07,.152,.022
    for i,(name,K,V,n_a) in enumerate(data):
        for r,(arr,lim,nm) in enumerate(((K,lims[0],"K"),(V,lims[1],"V"))):
            ax=fig.add_axes([x0+i*(wd+gap),.50-r*.355,wd,.29]);im=ax.imshow(binned(arr),aspect="auto",origin="lower",cmap="Blues",vmin=lim[0],vmax=lim[1],interpolation="nearest")
            if n_a:ax.axvline(n_a/256-.5,color="#EA580C",lw=1.3,ls="--")
            ax.set_xticks([]);ax.set_yticks([0,40,79]) if i==0 else ax.set_yticks([])
            if i==0:ax.set_ylabel(f"{nm} · layer",fontsize=10)
            if r==0:ax.set_title(f"{name} · {K.shape[1]:,} rows",fontsize=10.5,color=ccol(2*i))
            if i==len(data)-1:
                cb=fig.colorbar(im,cax=fig.add_axes([x0+len(data)*(wd+gap)-.012,.50-r*.355,.008,.29]));cb.ax.tick_params(labelsize=8)
    fig_footer(fig,k,"Orange dashed line = end of the initialized cartridge, start of the appended one. One shared colour scale per row (K, V). Bins of 256 rows; L2 norm over head_dim, mean of the KV heads.")
    return save_fig(fig,"PHYSICAL_PAIR_MEMORIES_XRAY",k)

def fig2(k=2):
    xm=xray_metas();panels=[]
    j=_npz(RUNS/"build_store"/"xray"/"S1-S5_joint.npz");c=_npz(ASK_DIR/"store"/"xray"/"C11.npz")
    if j is None or c is None or not (_xray_ok(xm.get("S1-S5_joint")) and _xray_ok(xm.get("C11"))):raise RuntimeError("S1–S5 joint or C11 X-ray record missing")
    panels=[("S1–S5 joint · K",j[0],"process 1"),("S1–S5 joint · V",j[1],"process 1"),("C11 alone · K",c[0],"process 2"),("C11 alone · V",c[1],"process 2")]
    B=LIVE.get("build") or {};c11=B.get("C11") or {};au=((LIVE.get("ask") or {}).get("independence") or {}).get("c11_memory_audit") or {}
    fig=fig_base(k,"S1–S5 joint memory and the new cartridge C11 — 80-layer K/V X-ray",
                 f"Left: S1–S5 physically joined in process 1. Right: C11 mounted ALONE in process 2 · C11 SHA-256 {str(c11.get('cartridge_sha256'))[:16]}… · C11 is not a merged map of C01–C10")
    for i,(t,arr,who) in enumerate(panels):
        ax=fig.add_axes([.07+i*.225,.22,.18,.56]);b=binned(arr,64)
        im=ax.imshow(b,aspect="auto",origin="lower",cmap="Blues" if i<2 else "Greens",vmin=np.percentile(b,2),vmax=np.percentile(b,98),interpolation="nearest")
        ax.set_title(f"{t} · {arr.shape[1]:,} rows",fontsize=10.5,color=INK if i<2 else C11_COLOR);ax.set_xticks([]);ax.set_xlabel(who,fontsize=9.5,color=MUTED)
        ax.set_yticks([0,40,79]) if i==0 else ax.set_yticks([])
        if i==0:ax.set_ylabel("layer",fontsize=10)
        cb=fig.colorbar(im,cax=fig.add_axes([.07+i*.225+.185,.22,.006,.56]));cb.ax.tick_params(labelsize=7.5)
    ftext(fig,.07,.145,f"C11 memory audit (process 2): rows {au.get('rows')} = expected {au.get('rows_expected')} · K/V bytes {au.get('memory_logical_bytes')} = expected {au.get('expected_kv_bytes')} · "
          f"allocated above the model-only baseline {au.get('allocated_above_model_baseline')} B · result {'PASS' if au.get('pass') else 'FAIL'}",fontsize=10,color=INK2,va="center")
    fig_footer(fig,k,"Bins of 64 rows. C11 holds only the rows of its own body: the model-generated general final synthesis, written with the unchanged CUT3 path (TEST709 forge_stream).")
    return save_fig(fig,"S1_S5_JOINT_AND_C11_XRAY",k)

def fig3(k=3):
    rows=LIVE.get("questions") or []
    if not rows or not any(q["answers"] for q in rows):raise RuntimeError("no answer of the sealed panel is recorded")
    fig=fig_base(k,"Five fixed questions — C11 alone vs the model without any document",
                 "Automatic indicator per raw answer (text rules sealed before generation) — the full raw answers are in the interface, RUN_SUMMARY.txt and the records; the reader judges them.")
    for j,lab in enumerate(("C11 alone (process 2)","no document")):fig.text(.60+j*.2,.825,lab,fontsize=12.5,weight="bold",color=C11_COLOR if j==0 else INK2,ha="center")
    for i,q in enumerate(rows):
        y=.735-i*.128
        fig.text(.04,y,q["id"],fontsize=14,weight="bold",color=INK,va="center")
        w=textwrap.wrap(q["text"],70);ftext(fig,.085,y+.012,"\n".join(w[:3])+("…" if len(w)>3 else ""),xmax=.50,minsize=6.5,fontsize=9.2,color=INK2,va="center",linespacing=1.2)
        ftext(fig,.085,y-.045,"expected (PDF): "+short(q["verifiable_answer"],80),xmax=.50,minsize=6.5,fontsize=8.4,color=MUTED,va="center",style="italic")
        for j,c in enumerate(("C11","NO_DOCUMENT")):
            a=q["answers"].get(c) or {};st=a.get("evaluation","NOT PRODUCED")
            fig.text(.60+j*.2,y+.016,st.replace("_"," "),fontsize=12 if len(st)<12 else 10.5,weight="bold",color=STATUS_COL.get(st,MUTED),ha="center",va="center")
            fig.text(.60+j*.2,y-.02,f"finish {a.get('finish_reason','—')} · {a.get('n_generated','—')} tokens",fontsize=8.8,color=MUTED,ha="center",va="center")
    fig_footer(fig,k,"CORRECT / INCORRECT / UNCLEAR / INCOMPLETE / UNVERIFIED FINISH = automatic indicator, not expert verification. A correct no-document answer may come from pre-training.")
    return save_fig(fig,"FIVE_QUESTIONS_C11_VS_NO_DOCUMENT",k)
FIG_FUNCS=OrderedDict([("F1",fig1),("F2",fig2),("F3",fig3)])
def render_figures():
    """renders all figures on the CPU from this run's records (no GPU use)"""
    if not LIVE:LIVE.update(live_record())
    out={};errs={}
    for i,(key,fn) in enumerate(FIG_FUNCS.items(),1):
        t=time.perf_counter()
        try:rec=fn(i);out[key]=rec;FIG_FILES[key]=rec;_OUT.write(f"  figure {i}/{len(FIG_FUNCS)} · {rec['pixels'][0]}×{rec['pixels'][1]} JPEG · {rec['jpg_bytes']/1e6:.1f} MB · {time.perf_counter()-t:.1f} s · {Path(rec['jpg']).name}\n")
        except Exception as ex:errs[key]=f"{type(ex).__name__}: {ex}";FIG_FILES.pop(key,None);flog(f"FIGURE {i} NOT GENERATED {traceback.format_exc()[-1500:]}");_OUT.write(f"  figure {i} NOT GENERATED · {errs[key]}\n")
        _OUT.flush()
    dump_json(SESSION_DIR/"FIGURES_MANIFEST.json",dict(session=SESSION_ID,utc=utc_now(),data_source="this run's records only",provenance=LIVE.get("provenance"),figures=FIG_FILES,not_generated=errs))
    slog("FIGURES",f"{len(out)} rendered",not_generated=errs);return out,errs

# ---------------------------------------------------------------------------------------------------------------------
# research summary, downloadable artifacts (actual files of this run; the Siemens PDF and the .pt tensors are never packaged)
# ---------------------------------------------------------------------------------------------------------------------
RUN_SUMMARY=SESSION_DIR/"RUN_SUMMARY.txt"
ZIP_PATH=SESSION_DIR/f"{SESSION_ID}_AKBASCORE_SIEMENS_TEST719_ALL_RESEARCH_ARTIFACTS.zip";MANIFEST=SESSION_DIR/"SHA256_MANIFEST.json"
def pct(x):return "—" if x is None else f"{100*x:.0f} %"
def write_run_summary():
    v=STATE.get("verification") or {};L=[];a=L.append;Lr=LIVE if LIVE else {};B=build_result();A=ask_result();ph=phases()
    a(f"{APP_TITLE}\n{VERSION_NOTE}\nsession {SESSION_ID} · started {SESSION_INFO['started_local']} ({INIT['started_utc']} UTC) · written {local_now()}")
    fs=INIT.get("final") or {}
    if fs:
        a(f"FINAL STATUS  {fs.get('headline')}\n  scientific result: {fs.get('result')}\n  C11 isolation    : {fs.get('isolation')}")
        for g in fs.get("gaps") or []:a(f"  reported gap · {g.get('step')} · {g.get('kind')} · {g.get('gap')}")
    a(f"PROVENANCE  {Lr.get('provenance','n/a')}"+("" if Lr.get("provenance")=="GPU_REAL" else "  — NOT A REAL A100 RESULT; nothing in this file may be presented as an experimental result")+"\n")
    a("EXPERIMENT  TEST719 — five physical CUT3 pair memories → five question-independent syntheses (S1–S5) → S1–S5 physically joined → final synthesis → new cartridge C11;")
    a("            five fixed questions to C11 alone (new Python process) and to the same model without any document")
    a(f"ENGINE      716.py git blob {LOCKS['716.py']} · 709.py {LOCKS['709.py']} (executed unchanged; only MAX_NEW is set per call)")
    for nm,lab in (("BUILD","process 1"),("ASK","process 2")):
        p=ph.get(nm) or {};a(f"            {lab}: {p.get('start_utc')} → {p.get('end_utc')} UTC · exit {p.get('exit_code')} · pid {p.get('pid')} · {p.get('seconds')} s · status {p.get('status')}")
    mi=MODEL_IDENTITY
    a(f"MODEL       {MODEL_ID} · NF4 4-bit, BF16 compute, frozen · pinned snapshot {(B.get('model_pin') or {}).get('commit')} · Hub main {mi.get('hub_main_commit')}")
    a(f"            first public release {MODEL_RELEASE['date']} — {MODEL_RELEASE['source']} — {MODEL_RELEASE['url']} ({MODEL_RELEASE['checked']})")
    a(f"DOCUMENT    {DOC_TITLE} · edition {DOC_EDITION_MARK} (printed on {DOC.get('edition_mark_pages')} of {DOC.get('pages')} pages — verified on the document)")
    a(f"            order no. {DOC.get('order_number')} · software {DOC.get('software_version')} · {DOC.get('bytes')} bytes · SHA-256 {DOC.get('sha256')}")
    a(f"            downloaded {DOC.get('download_start_utc')} → {DOC.get('download_end_utc')} UTC from {PDF_URL}")
    a(f"            {PDF_POLICY} ({PDF_TERMS_URL})")
    a("\nINITIALIZATION (this session)")
    for st in INIT["steps"]:a(f"  ✓ {st['step']:<13} {st['seconds']:>9.1f} s  {st['title']}")
    if INIT.get("failed"):a(f"  ✗ {INIT['failed']['step']}  {INIT['failed']['error']}  (last successful: {INIT['failed']['last_successful_step']})")
    seal=jload(SEAL_FILE,{}) or {}
    if seal:a(f"\nQUESTION PANEL  sealed {seal.get('sealed_utc')} (before any model load) · questions SHA-256 {seal.get('questions_sha256')} · build config SHA-256 {seal.get('build_config_sha256')}")
    if B:
        a(f"\nPROCESS 1 — PHYSICAL MEMORY RECORD · status {B.get('status')}"+(f" · {B.get('error')}" if B.get("error") else ""))
        for b in B.get("sources") or []:a(f"  {b['id']}  PDF pages {b['page_range'][0]}–{b['page_range'][1]} · {b['body_tokens']} tokens · SHA-256 {b['cartridge_sha256']}")
        for p in B.get("pairs") or []:
            ap=p.get("append") or {};sy=p.get("synthesis") or {};em=sy.get("end_marker") or {};fe=sy.get("finish_evidence") or {}
            a(f"  {p['pair']} initialize({p['cartridges'][0]}) → append({p['cartridges'][1]}) · rows {ap.get('rows')} (expected {p.get('rows_expected')}) · {ap.get('pass_line') or 'append NOT verified'}")
            a(f"      synthesis {sy.get('status')} · finish {sy.get('finish_reason')} (forward passes {fe.get('forward_calls')}, last token {fe.get('last_observed_token_text')!r}) · END marker last line {em.get('at_end')} · "
              f"{sy.get('n_generated')} tokens (ceiling {sy.get('ceiling')}) · {sy.get('seconds')} s"+(f" · reason {sy.get('incomplete_reason')}" if sy.get("incomplete_reason") else ""))
        for s in B.get("S") or []:a(f"  {s['id']}  {s['body_tokens']} tokens · SHA-256 {s['cartridge_sha256']}")
        j=B.get("joint") or {}
        if j:
            fi=j.get("final") or {};em=fi.get("end_marker") or {}
            a(f"  S1–S5 joint · {j.get('rows')} rows · appends verified {[x.get('verified') for x in j.get('appends',[])]}")
            a(f"      final synthesis {fi.get('status')} · finish {fi.get('finish_reason')} · END marker last line {em.get('at_end')} · {fi.get('n_generated')} tokens (ceiling {fi.get('ceiling')}) · {fi.get('seconds')} s"+(f" · reason {fi.get('incomplete_reason')}" if fi.get("incomplete_reason") else ""))
        c=B.get("C11") or {};a(f"  C11  {c.get('body_tokens','—')} tokens · SHA-256 {c.get('cartridge_sha256','NOT WRITTEN')}")
    if A:
        ind=A.get("independence") or {}
        a(f"\nPROCESS 2 — C11 ALONE IN A NEW PROCESS (same Colab VM) · status {A.get('status')}"+(f" · {A.get('error')}" if A.get("error") else ""))
        for k,lab in ISO_LABELS:a(f"  {'PASS' if (ind.get(k) or {}).get('pass') else 'FAIL'}  {lab}")
        au=ind.get("c11_memory_audit") or {}
        if au:a(f"  memory audit: {au.get('what_is_proven')}")
    if Lr.get("questions") and A:
        a("\nTHE FIVE FIXED QUESTIONS — FULL RAW ANSWERS (unedited; the indicator is automatic, not expert verification)")
        for q in Lr["questions"]:
            pe=q.get("pdf_evidence") or {}
            a(f"\n  {q['id']}  {q['text']}\n      region {q.get('region')} · expected (PDF): {q['verifiable_answer']} · source: {q['source']} · PDF check before model load: {'verified' if pe.get('verified') else 'NOT verified'}")
            for ev in pe.get("evidence",[]):
                f=ev.get("found") or {}
                if ev["cartridge"]=="EVERY":a(f"      evidence: found in {len(f)}/{N_CART} cartridges")
                elif f:a(f"      evidence: {f['cartridge']} PDF page {f['pdf_page']} · “{f['snippets'][-1][:200]}”")
            for c,lab in (("C11","C11 ALONE"),("NO_DOCUMENT","NO DOCUMENT")):
                r=q["answers"].get(c)
                if not r:a(f"      {lab}: not produced");continue
                a(f"      {lab} · {r['status']} · finish {r.get('finish_reason')} · {r['n_generated']} tokens (ceiling {r['ceiling']}) · {r['seconds']} s · indicator {r['evaluation']} ({r['why']})")
                a("        "+str(r["text"]).replace("\n","\n        "))
    if INIT.get("ready") or (Lr.get("questions") and A and A.get("answers")):
        fin_p=RUNS/"build_store"/"synthesis"/"FINAL.txt"
        if fin_p.is_file():a("\nC11 BODY TEXT (general final synthesis, model-generated)\n  "+fin_p.read_text(encoding="utf-8").replace("\n","\n  "))
    if any(r.get("origin")=="user" for r in STATE["qa"]+STATE["controls"]):
        a("\nQUESTIONS ASKED IN THE INTERFACE (not part of the sealed panel)")
        for r in STATE["qa"]+STATE["controls"]:
            if r.get("origin")=="user":a(f"  [{r['cartridge'] or 'no document'}] {r['question']}\n      {r['status']} · finish {r['finish_reason']} → {r['raw']}")
    a(f"\nLIVE VERIFICATION  {v.get('passed','—')}/{v.get('total','—')} passed")
    for i in v.get("items",[]):a(f"  {'PASS' if i['passed'] else 'FAIL'}  {i['name']}  {i['detail'] if isinstance(i['detail'],str) else json.dumps(i['detail'],ensure_ascii=False)}")
    a(f"\n{PREV_TITLE}\n{PREV_TEXT}\n{PREV_SEE}\n(Previously published research — not a result of this experiment.)")
    a("\nRESEARCH LINEAGE\n"+"\n".join(f"  {t}: {u}" for t,u in LINEAGE)+"\n  This experiment: unpublished — no DOI.")
    a("\nHISTORICAL REFERENCE (earlier runs, not this session): "+", ".join(f"{n} blob {LOCKS[n]}" for n in HISTORICAL))
    a("\nSCOPE  C11 is a new physical memory written from a model-generated general synthesis, not a lossless merge of C01–C10. Five questions are a live "
      "demonstration, not a statistic; the indicator is an automatic text rule. A correct no-document answer may come from pre-training. Process 2 is a new "
      "process on the same Colab VM, not a separate machine.")
    a(f"{AUTHOR} · {ORG} · {LICENSE_NAME} · {COPYRIGHT}")
    RUN_SUMMARY.write_text("\n".join(L)+"\n",encoding="utf-8");return str(RUN_SUMMARY)
def session_record():
    return dict(session=SESSION_INFO,app=APP_TITLE,version_note=VERSION_NOTE,sources=SOURCES,program=PROGRAM,locks=LOCKS,initialization=INIT,phases=phases(),
                architecture=engine_architecture(),document=DOC,model=MODEL_IDENTITY,mounted=STATE["mount"],operations=STATE["ops"],qa=STATE["qa"],controls=STATE["controls"],
                weight_checks=STATE["weight_checks"],disk_checks=STATE["disk_checks"],verification=STATE["verification"],figures=FIG_FILES,lineage=LINEAGE,
                previously_demonstrated=dict(title=PREV_TITLE,text=PREV_TEXT,see=PREV_SEE),
                scope="C11 is written from a model-generated synthesis; five questions are a demonstration; the indicator is automatic; the Siemens PDF is not redistributed.")
def _category(rel):
    if rel.startswith("historical_reference_not_this_session"):return "HISTORICAL (published earlier run, not this session)"
    if rel.startswith("figures"):return "LIVE figure"
    if rel.startswith("records_process1"):return "LIVE process 1 record"
    if rel.startswith("records_process2"):return "LIVE process 2 record"
    if rel.startswith("records_console"):return "LIVE process output (both processes)"
    if rel.startswith("program"):return "PROGRAM file of this run"
    return "LIVE session record"
def _run_records():
    """process records read directly from the experiment directories (no .pt tensor, no PDF copy, no engine working directory)"""
    out=[]
    def add(base,arc):
        base=Path(base)
        if base.is_file():out.append((base,arc));return
        if not base.is_dir():return
        for p in sorted(base.rglob("*")):
            if p.is_file() and p.suffix not in (".pt",".pdf",".tmp"):out.append((p,f"{arc}/{p.relative_to(base)}"))
    add(RUNS/"build_store","records_process1/build_store");add(RUNS/"build"/"events.jsonl","records_process1/events.jsonl");add(RUNS/"console","records_console")
    for f in ("SEAL.json","pdf_source_check.json","PHASES.json"):add(RUNS/f,f"records_process1/{f}")
    for f in ("handoff.json","C11.sha256"):add(RUNS/"handoff"/f,f"records_process1/handoff/{f}")
    add(RUNS/"engine_dir_after_build"/"TEST716_results.json","records_process1/TEST716_results.json")
    add(ASK_DIR/"store","records_process2/store");add(ASK_DIR/"events.jsonl","records_process2/events.jsonl")
    for name in PROGRAM:add(PROGRAM_DIR/name,f"program/{name}")
    return out
def package_session():
    """Download-All ZIP: three figures (JPG/PNG/PDF), session logs, process records, verification records, program files,
    historical files (separate folder) and SHA256_MANIFEST.json — never the Siemens PDF, never a .pt tensor"""
    dump_json(SESSION_DIR/"SESSION_RECORD.json",session_record());write_run_summary()
    files=[(p,str(p.relative_to(SESSION_DIR))) for p in sorted(SESSION_DIR.rglob("*")) if p.is_file() and p.suffix not in (".zip",".tmp") and p!=MANIFEST
           and not str(p.relative_to(SESSION_DIR)).startswith(("records_process1","records_process2","records_console","program"))]+_run_records()
    man=OrderedDict((arc,dict(sha256=sha_file(p),bytes=p.stat().st_size,category=_category(arc))) for p,arc in files)
    dump_json(MANIFEST,dict(session=SESSION_ID,utc=utc_now(),note="The Siemens PDF is not included (copyright Siemens AG); its URL and SHA-256 are in SOURCE_DOCUMENT_RECORD.json. Cartridge tensors (.pt) are not included; their SHA-256 are in the records.",files=man))
    tmp=ZIP_PATH.with_suffix(".zip.tmp")
    with zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED) as z:
        for p,arc in files+[(MANIFEST,"SHA256_MANIFEST.json")]:z.write(p,arcname=f"{SESSION_ID}/{arc}")
    with zipfile.ZipFile(tmp) as z:
        if z.testzip():raise RuntimeError("ZIP check failed")
    tmp.replace(ZIP_PATH);slog("PACKAGE",ZIP_PATH.name,files=len(files)+1,bytes=ZIP_PATH.stat().st_size);return str(ZIP_PATH)
def copy_records_for_download():
    """after process 2: plain copies of the process records inside the session folder, so the interface can offer them"""
    for p,arc in _run_records():
        d=SESSION_DIR/arc;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,d)
def download_items():
    items=[("Run summary (.txt)",RUN_SUMMARY),("Session log (.log)",SESSION_LOG),("Session events (.jsonl)",SESSION_EVENTS),
           ("Process 1 output (.log)",SESSION_DIR/"records_console"/"BUILD.log"),("Process 1 output with UTC time stamps (.tsv)",SESSION_DIR/"records_console"/"BUILD_with_UTC_timestamps.tsv"),
           ("Process 1 result (.json)",SESSION_DIR/"records_process1"/"build_store"/"build_result.json"),
           ("Process 2 output (.log)",SESSION_DIR/"records_console"/"ASK.log"),("Process 2 result (.json)",SESSION_DIR/"records_process2"/"store"/"ask_result.json"),
           ("C11 body text — final synthesis (.txt)",SESSION_DIR/"records_process1"/"build_store"/"synthesis"/"FINAL.txt"),
           ("Question panel source check on the PDF (.json)",PANEL_FILE),("Live measurements (.json)",LIVE_MEAS),
           ("Source document record (.json)",DOC_FILE),("Verification record (.json)",VERIFY_FILE),("Initialization record (.json)",INIT_FILE),
           ("Interface questions and answers (.jsonl)",SESSION_QA),("Figure manifest (.json)",SESSION_DIR/"FIGURES_MANIFEST.json"),("SHA-256 manifest (.json)",MANIFEST)]+\
          [(f"Pair synthesis P{k} (.txt)",SESSION_DIR/"records_process1"/"build_store"/"synthesis"/f"P{k}.txt") for k in range(1,N_PAIRS+1)]+\
          [(f"HISTORICAL · published {n} of an earlier run (not this session)",HIST_DIR/("HISTORICAL_"+n)) for n in HISTORICAL]
    return [(l,str(p)) for l,p in items if Path(p).is_file()]

# ---------------------------------------------------------------------------------------------------------------------
# AUTOMATIC INITIALIZATION — one start, every step real, stops at the first failure
# ---------------------------------------------------------------------------------------------------------------------
def _step_verify():
    v=compute_verification()
    for it in v["items"]:_OUT.write(f"  {'PASS' if it['passed'] else 'FAIL'}  {it['cls']:<9} {it['name']:<44} {short(it['detail'] if isinstance(it['detail'],str) else json.dumps(it['detail'],ensure_ascii=False),80)}\n")
    _OUT.write(f"  → scientific result: {v['result']}\n  → isolation of C11: {v['isolation']}\n  → formal gaps: {', '.join(v['formal_gaps']) or 'none'}\n");_OUT.flush()
    return dict(passed=v["passed"],total=v["total"],result=v["result"],isolation=v["isolation"],formal_gaps=v["formal_gaps"],provenance=v["provenance"])
def _step_figures():
    copy_records_for_download()
    out,errs=render_figures()
    if errs or len(out)!=len(FIG_FUNCS):raise RuntimeError(f"FIGURES: {len(out)}/{len(FIG_FUNCS)} generated · {errs}")
    return dict(figures=[Path(r["jpg"]).name for r in out.values()])
STEP_FUNCS=OrderedDict([("SOURCES",sources_step),("PREFLIGHT",preflight),("DOCUMENT",document_step),("PANEL",panel_step),("BUILD",build_step),
                        ("ASK",ask_step),("VERIFY",_step_verify),("READY_MEMORY",ready_memory),("FIGURES",_step_figures)])
# steps after the scientific computation: a failure there is recorded as a gap of the presentation and the run continues
NONFATAL=("VERIFY","READY_MEMORY","FIGURES")

def final_status():
    v=STATE.get("verification") or {};gaps=list(INIT.get("gaps") or [])
    for g in v.get("formal_gaps") or []:gaps.append(dict(step="VERIFY",kind="FORMAL",gap=g))
    missing=[k for k in FIGURES if k not in FIG_FILES]
    if missing and not any(g.get("step")=="FIGURES" for g in gaps):gaps.append(dict(step="FIGURES",kind="PRESENTATION",gap=f"figures not generated: {missing}"))
    res=v.get("result") or "NOT EVALUATED"
    head=("RESULT VALID" if res=="VALID" else "RESULT NOT VALID")+(" · C11 isolation supported" if str(v.get("isolation","")).startswith("SUPPORTED") else " · C11 isolation NOT supported")+\
         (" · no gaps" if not gaps else f" · {len(gaps)} reported gap(s)")
    INIT["final"]=dict(headline=head,result=res,isolation=v.get("isolation"),gaps=gaps,figures_missing=missing,provenance=LIVE.get("provenance"));return INIT["final"]

def init_failed(key,ex):
    tb=traceback.format_exc()
    INIT["failed"]=dict(step=key,title=INIT_STEPS[key],error=f"{type(ex).__name__}: {ex}",last_successful_step=INIT["last_ok"],utc=utc_now(),traceback=tb[-6000:],
                        last_process_lines=[f"{ts} {nm} {l}" for ts,_,nm,l in PROC_LINES[-40:]],last_heartbeat=(HEARTBEATS[-1] if HEARTBEATS else None),phases=phases())
    release_memory("initialization failed")
    slog("INIT_FAILED",key,error=INIT["failed"]["error"],last_successful_step=INIT["last_ok"],traceback=tb[-3000:])
    try:dump_json(INIT_FILE,INIT);package_session()
    except Exception as ex2:_OUT.write(f"  (failure package could not be written: {ex2})\n")
    banner(f"EXPERIMENT STOPPED — no result is available from this attempt and nothing here is reported as a success.\n"
           f"  failed step          : {key} · {INIT_STEPS[key]}\n  error                : {INIT['failed']['error']}\n"
           f"  last successful step : {INIT['last_ok'] or 'none'}\n  records              : {SESSION_DIR}\n  all files (ZIP)      : {ZIP_PATH if ZIP_PATH.is_file() else 'not written'}","█")

def run_initialization():
    banner(f"{APP_TITLE}\n{VERSION_NOTE} · session {SESSION_ID} · records in {SESSION_DIR}\n"
           "Automatic initialization: every step below is executed for real in this runtime; nothing is precomputed.","#")
    INIT["gaps"]=[]
    for key,fn in STEP_FUNCS.items():
        t0=step_begin(key)
        try:info=fn()
        except BaseException as ex:
            if key in NONFATAL and not isinstance(ex,KeyboardInterrupt):
                err=f"{type(ex).__name__}: {ex}";INIT["gaps"].append(dict(step=key,kind="PRESENTATION",gap=err,utc=utc_now(),traceback=traceback.format_exc()[-3000:]))
                slog("STEP_GAP",key,error=err);_OUT.write(f"──── ⚠ {key} not completed — recorded as a gap of the final report, the run continues: {err}\n");_OUT.flush()
                if key=="READY_MEMORY":release_memory("interface memory not available")
                continue
            init_failed(key,ex);raise RuntimeError(f"INITIALIZATION FAILED at {key}: {type(ex).__name__}: {ex}") from ex
        step_done(key,t0,result=info)
    INIT["ready"]=True;INIT["ready_utc"]=utc_now();INIT["total_seconds"]=round(time.perf_counter()-INIT["started"],1)
    f=final_status();dump_json(INIT_FILE,INIT)
    try:package_session()
    except Exception as ex:INIT["gaps"].append(dict(step="PACKAGE",kind="PRESENTATION",gap=f"{type(ex).__name__}: {ex}"));f=final_status()
    gl="".join(f"\n  gap · {g['step']} · {g['kind']} · {short(g['gap'],150)}" for g in f["gaps"])
    banner(f"EXPERIMENT FINISHED in {INIT['total_seconds']/60:.1f} min · {f['headline']} · provenance {LIVE.get('provenance')}\n"
           f"  scientific result : {f['result']}\n  C11 isolation     : {f['isolation']}\n  interface memory  : {'C11 mounted ('+format(STATE['mount']['rows'],',')+' rows)' if STATE.get('mount') else 'not available (questions in the interface are disabled)'}"+gl,"#")
    slog("FINISHED",f["headline"],seconds=INIT["total_seconds"],gaps=len(f["gaps"]))
    return True
# ===== END OF PART 2/3 =====
