# AKBASCORE SILICON HIPPOCAMPUS — TEST786
# ONE COLAB CELL | A100 80GB | Qwen2.5-72B frozen | native physical KV
# Backbone: unmodified TEST785 definitions -> unmodified TEST779 sealed engine.
# TEST786: PAIR-first leave-one-out causal evidence, negative control,
# conservative action and physical readout. No claim of semantic self-awareness.
import urllib.request, hashlib, ast, json, traceback, gc, math, time

URL786="https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/785.py"
SOURCE785=urllib.request.urlopen(
    urllib.request.Request(URL786,headers={"User-Agent":"AKBASCORE-TEST786"}),
    timeout=180).read()
sha785=hashlib.sha256(SOURCE785).hexdigest()
tree786=ast.parse(SOURCE785.decode("utf-8"),filename="785.py")
# Keep original imports, TEST779 loader, model helpers and ALL TEST785 functions.
# Replace only TEST785 top-level execution block.
idx786=next((i for i,n in enumerate(tree786.body)
    if isinstance(n,ast.Try)
    and any(isinstance(x,ast.Expr) and isinstance(x.value,ast.Call)
            and isinstance(x.value.func,ast.Name) and x.value.func.id=="log"
            for x in n.body[:3])),None)
assert idx786 is not None and idx786==len(tree786.body)-1, "FAIL_CLOSED_TEST785_AST_BOUNDARY"
exec(compile(ast.fix_missing_locations(ast.Module(
    body=tree786.body[:idx786],type_ignores=[])),
    "TEST785_UNMODIFIED_PRELUDE","exec"),globals())
assert gitblob785(raw785)==BLOB, "FAIL_CLOSED_TEST779_GIT_BLOB"

TEST="786"
OUT=ROOT/"TEST786_results.json"
LOG=ROOT/"TEST786.log"
MANIFEST=ROOT/"TEST786_manifest.json"
LOG.write_text("",encoding="utf-8")
MAX_TOKENS=20
# Fixed before the test; thresholds not optimized on these 8 examples.
MIN_PAIR_MARGIN=0.10
MIN_LOO_EFFECT=0.10
MAX_STEPS=1
R={
    "test":"786","status":"STARTED","run_id":RUN_ID,
    "backbone":"TEST785 unmodified prelude / TEST779 locked engine",
    "source785_sha256":sha785,"source779_git_blob":BLOB,
    "panel_sha256":PANEL_SHA,"locks":LOCKS,
    "rows":[],"checks":[],"controls":[],
    "policy":{
       "baseline":"PAIR-first",
       "fallback":"Preserve PAIR on uncertainty",
       "min_pair_margin":MIN_PAIR_MARGIN,
       "min_loo_effect":MIN_LOO_EFFECT,
       "max_steps":MAX_STEPS,
       "oracle_gold_used_for_decisions":False
    },
    "limitations":[
       "Same TEST779 synthetic panel; not independent held-out evaluation",
       "PAIR candidate may be confidently wrong",
       "Leave-one-out measures candidate dependence, not truth",
       "Conservative KEEP_PAIR is a baseline, not autonomous semantic intelligence",
       "No autonomous STORE or closed-loop iterative learning",
       "Offline gold used only after decisions are fixed",
       "No source text, view tag, gold, or regex answer validation in decision"
    ]
}
def save786():
    OUT.write_text(json.dumps(R,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
def emit786(row):
    R["rows"].append(row);save786()
    log("TEST786_ROW",json.dumps(row,ensure_ascii=False,default=str))
def score786(mem,q,answer):
    if not answer:return None
    # Reuse TEST785's original model scoring unchanged.
    return norm785(mem,q,answer)
def clean786(s):
    return s.strip() if isinstance(s,str) else ""
def choose786(preds,scores):
    """
    PAIR-first controller. Source-blind: no labels/gold/view in inputs.
    Evidence-only switch is permitted ONLY when PAIR abstains and an isolated
    answer is supported by the PAIR distribution and is unique.
    A positive pair result is preserved rather than replaced by a selector.
    """
    pair=clean786(preds["PAIR"])
    a=clean786(preds["B0"]);b=clean786(preds["B1"])
    if not pair:
        return {"action":"ABSTAIN","reason":"PAIR_EMPTY"}
    if pair!="UNKNOWN":
        return {"action":"KEEP_PAIR","reason":"PAIR_NONABSTAIN_BASELINE"}
    proposals=list(dict.fromkeys(x for x in (a,b) if x and x!="UNKNOWN"))
    if not proposals:
        return {"action":"ABSTAIN","reason":"NO_NONUNKNOWN_CANDIDATE"}
    # For a single unique proposal, compare it to UNKNOWN in the PAIR cache.
    # No source selection based on a TEAM-format regex or offline expected value.
    ranked=sorted(
        [(x,scores["PAIR"].get(x,float("-inf"))) for x in proposals],
        key=lambda t:t[1],reverse=True)
    if len(ranked)>1 and ranked[0][1]-ranked[1][1]<MIN_PAIR_MARGIN:
        return {"action":"ABSTAIN","reason":"CONFLICT_UNRESOLVED",
                "proposal_scores":ranked}
    winner=ranked[0][0]
    pair_unknown=scores["PAIR"].get("UNKNOWN",float("-inf"))
    if ranked[0][1]-pair_unknown < MIN_PAIR_MARGIN:
        return {"action":"ABSTAIN","reason":"PAIR_DOES_NOT_SUPPORT_PROPOSAL",
                "proposal_scores":ranked,"unknown_score":pair_unknown}
    owners=[src for src in ("B0","B1") if clean786(preds[src])==winner]
    if len(owners)==1:
        return {"action":"SWITCH_"+owners[0],"reason":"PAIR_ABSTAIN_SUPPORTED_PROPOSAL",
                "candidate":winner,"pair_support":ranked[0][1]-pair_unknown}
    return {"action":"KEEP_PAIR","reason":"SOURCES_AGREE_ON_PROPOSAL"}

def verify_negative_control786():
    # Pure decision-unit tests, no gold/format or prompt leakage.
    examples=[
       ({"PAIR":"TEAM-A","B0":"UNKNOWN","B1":"TEAM-A"},"KEEP_PAIR"),
       ({"PAIR":"UNKNOWN","B0":"UNKNOWN","B1":"UNKNOWN"},"ABSTAIN"),
       ({"PAIR":"","B0":"TEAM-A","B1":"TEAM-B"},"ABSTAIN")
    ]
    for i,(p,expected_action) in enumerate(examples):
        d=choose786(p,{"PAIR":{}})
        check("DECISION_NEGATIVE_"+str(i),d["action"]==expected_action,d)
        R["controls"].append({"id":i,"action":d["action"],"expected":expected_action})
try:
    log("="*112)
    log("AKBASCORE TEST786 — TEST785 LOCKED BACKBONE / PAIR-FIRST CAUSAL ABLATION")
    log("TEST785_SOURCE_SHA256",sha785)
    check("TEST779_EXACT_GIT_BLOB",gitblob785(raw785)==BLOB)
    check("SEALED_PANEL",hashlib.sha256((ROOT/"SEALED_PANEL.json").read_bytes()).hexdigest()==PANEL_SHA)
    verify_negative_control786()
    free,_=torch.cuda.mem_get_info()
    log("GPU_PREFLIGHT_FREE_GIB",round(free/2**30,2))
    check("GPU_VRAM",free>=40*2**30,"Fresh A100 runtime required")
    model_setup()
    weights_before=sentinel()
    for cid,body in sorted(CARD_TEXT.items()):
        physical_commit(cid,body)
    check("PHYSICAL_20_CARTRIDGES",len(entries)==20,len(entries))
    for fam in FAMILIES:
        fid=fam["id"];pair=[fid+"_B0",fid+"_B1"]
        sha_before={cid:sha_file(CART_DIR/(cid+".pt")) for cid in pair}
        memories={}
        try:
            for src,cid in zip(("B0","B1"),pair):
                memories[src]=build_source_cache(cid,fid)
                check("NATIVE_80_"+fid+"_"+src,len(memories[src])==80)
            memories["PAIR"],active,_,_=build_fusion(pair,"TEST786_PAIR_"+fid,True)
            check("NATIVE_PAIR_80_"+fid,len(memories["PAIR"])==80)
            check("PAIR_ORDER_"+fid,list(active)==pair)
            seals={s:memory_seals(m) for s,m in memories.items()}
            work=next(c["work"] for c in CASES if c["family"]==fid)
            for view in VIEWS:
                q=CUE[view].format(work=work)
                # Three independent greedy readouts; all candidates model-generated.
                generated={s:free_generate(memories[s],q,max_new=MAX_TOKENS,
                     spans={"B0":(0,0),"B1":(0,0)}) for s in ("B0","B1","PAIR")}
                preds={s:clean786(generated[s]["raw"]) for s in generated}
                candidates=list(dict.fromkeys(
                    x for x in list(preds.values())+["UNKNOWN"] if x))
                # Scoring the same candidates under all three physical caches.
                scores={s:{x:round(score786(memories[s],q,x),6)
                            for x in candidates} for s in ("B0","B1","PAIR")}
                pair_answer=preds["PAIR"]
                # Leave-one-out: how much PAIR support for its OWN answer is
                # lost when B0 or B1 is physically absent.
                loo={}
                if pair_answer:
                    base=scores["PAIR"][pair_answer]
                    for s in ("B0","B1"):
                        loo[s]={"pair_answer_score":base,
                                "isolated_score":scores[s][pair_answer],
                                "delta_pair_minus_isolated":round(base-scores[s][pair_answer],6),
                                "generated_same_as_pair":preds[s]==pair_answer}
                decision=choose786(preds,scores)
                action=decision["action"]
                selected=("B0" if action=="SWITCH_B0" else
                          "B1" if action=="SWITCH_B1" else
                          "PAIR" if action=="KEEP_PAIR" else None)
                if selected is None:
                    readout=None;final="UNKNOWN"
                else:
                    # This is the actual selected physical native cache.
                    readout=free_generate(memories[selected],q,max_new=MAX_TOKENS,
                              spans={"B0":(0,0),"B1":(0,0)})
                    final=clean786(readout["raw"])
                # Offline labels enter ONLY after physical readout is complete.
                expected=fam["new_team"] if view=="CURRENT" else fam["old_team"]
                row={
                    "family":fid,"view_OFFLINE":view,
                    "generated":generated,"scores":scores,
                    "pair_answer_loo":loo,"decision":decision,
                    "selected":selected,"readout":readout,"final":final,
                    "expected_OFFLINE":expected,"correct_OFFLINE":final==expected,
                    "pair_correct_OFFLINE":preds["PAIR"]==expected,
                    "b0_correct_OFFLINE":preds["B0"]==expected,
                    "b1_correct_OFFLINE":preds["B1"]==expected,
                    "avoidable_abstention_OFFLINE":selected is None and preds["PAIR"]==expected,
                    "changed_correct_pair_OFFLINE":preds["PAIR"]==expected and final!=expected
                }
                emit786(row)
            for s,m in memories.items():
                check("KV_UNCHANGED_"+fid+"_"+s,compare_seals(seals[s],memory_seals(m)))
        finally:
            memories.clear();gc.collect();release()
        for cid in pair:
            check("SSD_SHA_UNCHANGED_"+cid,
                  sha_file(CART_DIR/(cid+".pt"))==sha_before[cid])
    check("EIGHT_CASES",len(R["rows"])==8,len(R["rows"]))
    check("FROZEN_WEIGHTS",sentinel()==weights_before)
    check("NO_RESIDUAL_HOOKS",not model.model.layers[CUT]._forward_hooks
          and not model.model.layers[CUT]._forward_pre_hooks)
    R["summary"]={
       "n":len(R["rows"]),
       "correct":sum(x["correct_OFFLINE"] for x in R["rows"]),
       "pair_correct":sum(x["pair_correct_OFFLINE"] for x in R["rows"]),
       "avoidable_abstentions":sum(x["avoidable_abstention_OFFLINE"] for x in R["rows"]),
       "correct_pair_damaged":sum(x["changed_correct_pair_OFFLINE"] for x in R["rows"]),
       "actions":{a:sum(x["decision"]["action"]==a for x in R["rows"])
                  for a in ("SWITCH_B0","SWITCH_B1","KEEP_PAIR","ABSTAIN")},
       "interpretation":"PAIR-first control baseline; leave-one-out evidence is not truth or autonomous self-correction."
    }
    R["status"]="COMPLETE_RESULTS_RECORDED";save786()
    log("TEST786_COMPLETED",json.dumps(R["summary"],ensure_ascii=False))
    log("FILES",OUT,LOG,MANIFEST)
except Exception as e:
    R["status"]="ERROR";R["error"]=repr(e)
    R["traceback"]=traceback.format_exc()
    save786();log("TEST786_FAILED",repr(e));log(R["traceback"]);raise
finally:
    save786()
