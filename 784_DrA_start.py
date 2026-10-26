# AKBASCORE SILICON HIPPOCAMPUS — TEST784
# One Google Colab cell, A100 80GB. Uses exact TEST779 code as the unmodified engine.
# PHASE A: causal-free state/attention signal diagnostics.
# PHASE B: signed attention bias dose-response on frozen native CUT3 memory.
# No autonomous DrA claim; no model training; no oracle selection at inference.
import urllib.request, hashlib, ast, json, time, gc, traceback
from pathlib import Path

SOURCE_URL = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/779.py"
SOURCE_GIT_BLOB = "fa7017a87f25ecef6ed2b2954a850599cb25fcd9"
def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

raw = urllib.request.urlopen(
    urllib.request.Request(SOURCE_URL, headers={"User-Agent":"AKBASCORE-TEST784"}),
    timeout=180).read()
actual = git_blob(raw)
assert actual == SOURCE_GIT_BLOB, (
    "FAIL CLOSED: TEST779 source changed. expected=%s actual=%s" %
    (SOURCE_GIT_BLOB, actual))
print("PASS TEST779_EXACT_GIT_BLOB", actual, flush=True)

# AST parsing keeps every original import, engine definition, locked-source check,
# panel construction and function untouched. Only TEST779's execution block is omitted.
# The replacement execution block below runs TEST784, not TEST779.
tree = ast.parse(raw.decode("utf-8"), filename="779.py")
run_start = next(
    (i for i, node in enumerate(tree.body)
     if isinstance(node, ast.Try)
     and any(isinstance(x, ast.Expr) and isinstance(x.value, ast.Call)
             and isinstance(x.value.func, ast.Name) and x.value.func.id == "log"
             for x in node.body[:3])),
    None)
assert run_start is not None and run_start > 0, "FAIL CLOSED: TEST779 execution boundary missing"
assert run_start == len(tree.body) - 1, "FAIL CLOSED: unexpected code after TEST779 execution"
prelude = ast.Module(body=tree.body[:run_start], type_ignores=[])
exec(compile(ast.fix_missing_locations(prelude), "779_LOCKED_PRELUDE", "exec"), globals())

# TEST779 prelude creates its own root, manifest, and sealed panel; we retain those
# byte-for-byte and write distinct TEST784 results in the same run directory.
TEST = "784"
OUT = ROOT / "TEST784_results.json"
LOG = ROOT / "TEST784.log"
LOG.write_text("", encoding="utf-8")
MANIFEST = ROOT / "TEST784_manifest.json"
R = {
    "test":"784", "status":"STARTED", "run_id":RUN_ID,
    "backbone":"TEST779 unmodified AST prelude", "backbone_git_blob":actual,
    "locks":LOCKS, "panel_sha256":PANEL_SHA,
    "phase_a":[], "phase_b":[], "checks":[],
    "limitations":[
        "Controlled source pair is provided: no autonomous retrieval.",
        "Old/new candidate identifiers are used only in offline diagnostics.",
        "The question contains a temporal cue; this is not blind semantic inference.",
        "H3 state and attention density are probes, not correctness oracles.",
        "No closed-loop correction, autonomous STORE or semantic generalization is claimed.",
        "The TEST779 panel is reused, so this is not held-out generalization."
    ]
}
# Dose levels are fixed BEFORE model results, not selected post hoc.
DOSES = (-2.0, -0.5, 0.0, 0.5, 2.0)
BIAS_LAYERS = (4, 20, 40, 79)
def finite(x):
    import math
    return math.isfinite(float(x))
def emit(row, section):
    R[section].append(row)
    save()
    log(section.upper(), json.dumps(row, ensure_ascii=False, default=str))
def score_dose(mem, q, spans, old, new, target, dose):
    # The two candidate strings are evaluation-only: never passed to a selector.
    scored = compare(mem, q, old, new, spans, bias_span=target,
                     bias=float(dose), selected_layers=BIAS_LAYERS)
    return {
        "old_logp":scored["old_logp"], "new_logp":scored["new_logp"],
        "new_minus_old":scored["new_minus_old"],
        "attention_old":scored["attention_old"],
        "attention_new":scored["attention_new"],
        "sdpa_calls":scored["sdpa_calls"]
    }

try:
    log("="*108)
    log("AKBASCORE TEST784 — LOCKED TEST779 / PHASE A+B / NO AUTONOMOUS CONTROLLER")
    check("PANEL_SHA", hashlib.sha256((ROOT/"SEALED_PANEL.json").read_bytes()).hexdigest() == PANEL_SHA)
    free,_ = torch.cuda.mem_get_info()
    log("GPU_PREFLIGHT_FREE_GIB", round(free/2**30,2))
    check("A100_FREE_VRAM", free >= 40*2**30, "Restart runtime if model already loaded")
    model_setup()
    weights_before = sentinel()
    for cid, body in sorted(CARD_TEXT.items()):
        physical_commit(cid, body)
    check("PHYSICAL_CARTRIDGES_20", len(entries)==20, len(entries))
    # Each arm begins with the same unmodified pair cache.
    # No model intervention is retained between arms.
    for fam in FAMILIES:
        fid = fam["id"]
        pair = [fid+"_B0", fid+"_B1"]
        before = {cid:sha_file(CART_DIR/(cid+".pt")) for cid in pair}
        mem = None
        try:
            mem, active, steps, seconds = build_fusion(pair,"TEST784_"+fid,True)
            check("PAIR_"+fid, list(active)==pair, list(active))
            check("MEMORY_80_LAYERS_"+fid, len(mem)==80, len(mem))
            spans = source_spans(fid,mem)
            resident_seal = memory_seals(mem)
            work = next(c["work"] for c in CASES if c["family"]==fid)
            old,new = fam["old_team"],fam["new_team"]
            for view in VIEWS:
                q = CUE[view].format(work=work)
                # A: H3 observation and unmodified attention, measured once.
                state, attention = observe_state(mem,q,spans)
                chosen,confidence,density = source_signal(attention,spans)
                a = {
                    "family":fid,"view":view,
                    "h3_l2":round(float(state.norm().item()),7),
                    "h3_mean":round(float(state.mean().item()),7),
                    "attention_density":density,
                    "attention_choice":chosen,"attention_confidence":confidence,
                    "expected_source_OFFLINE":"B1" if view=="CURRENT" else "B0"
                }
                check("FINITE_STATE_"+fid+"_"+view,
                      all(finite(x) for x in [a["h3_l2"],a["h3_mean"],confidence,*density.values()]))
                emit(a,"phase_a")
                del state
                # B: same question, same frozen model, signed intervention.
                # Each dose uses fresh query cache built by compare().
                for target in ("B0","B1"):
                    for dose in DOSES:
                        result = score_dose(mem,q,spans,old,new,target,dose)
                        row = {
                            "family":fid,"view":view,"target":target,"dose":dose,
                            "new_minus_old":result["new_minus_old"],
                            "old_logp":result["old_logp"],
                            "new_logp":result["new_logp"],
                            "sdpa_calls":result["sdpa_calls"]
                        }
                        check("FINITE_MARGIN_"+fid+"_"+view+"_"+target+"_"+str(dose),
                              finite(row["new_minus_old"]))
                        emit(row,"phase_b")
            check("RESIDENT_KV_UNCHANGED_"+fid,
                  compare_seals(resident_seal,memory_seals(mem)))
        finally:
            if mem is not None: del mem
            release()
        for cid in pair:
            check("PHYSICAL_SHA_UNCHANGED_"+cid,
                  sha_file(CART_DIR/(cid+".pt")) == before[cid])
    check("A_MATRIX",len(R["phase_a"])==len(FAMILIES)*len(VIEWS),
          len(R["phase_a"]))
    check("B_MATRIX",len(R["phase_b"])==len(FAMILIES)*len(VIEWS)*2*len(DOSES),
          len(R["phase_b"]))
    check("FROZEN_WEIGHTS",sentinel()==weights_before)
    check("NO_RESIDUAL_HOOKS",not model.model.layers[CUT]._forward_hooks
          and not model.model.layers[CUT]._forward_pre_hooks)
    # Offline summaries only; never feed these labels or scores back into the model.
    correct = sum(x["attention_choice"]==x["expected_source_OFFLINE"] for x in R["phase_a"])
    R["offline_summary"] = {
        "phase_a_correct_attention_choice":correct,
        "phase_a_total":len(R["phase_a"]),
        "phase_b_total":len(R["phase_b"]),
        "phase_b_nonzero_effects":sum(
            abs(x["new_minus_old"] -
                next(z["new_minus_old"] for z in R["phase_b"]
                     if z["family"]==x["family"] and z["view"]==x["view"]
                     and z["target"]==x["target"] and z["dose"]==0.0)) > 1e-4
            for x in R["phase_b"] if x["dose"]!=0.0),
        "note":"Margin change is not proof of answer correctness or semantic self-evaluation."
    }
    R["status"]="COMPLETE_RESULTS_RECORDED"
    save()
    log("TEST784_COMPLETED",json.dumps(R["offline_summary"],ensure_ascii=False))
    log("FILES",OUT,LOG,MANIFEST)
except Exception as exc:
    R["status"]="ERROR"
    R["error"]=repr(exc)
    R["traceback"]=traceback.format_exc()
    save()
    log("TEST784_FAILED",repr(exc))
    log(R["traceback"])
    raise
finally:
    save()
