
# AKBASCORE SILICON HIPPOCAMPUS — TEST843
# Evidence-to-action dissociation audit.
# Reuses verified TEST842 -> locked TEST841 -> physical CUT3/M2 engine.
# One Colab cell; no training, hooks, RAG, oracle routing or answer patches.
import urllib.request, hashlib, ast

URL843 = "https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/842.py"
LOCK843 = "4653fe9a5dd7bc2dd3a72f25bed00ceebb3936fd"

req = urllib.request.Request(
    URL843, headers={"User-Agent": "AKBASCORE-TEST843"})
with urllib.request.urlopen(req, timeout=180) as f:
    raw = f.read(1000000)

blob = hashlib.sha1(
    b"blob " + str(len(raw)).encode() + b"\0" + raw
).hexdigest()
assert blob == LOCK843, ("SOURCE_CHANGED", blob)

src = raw.decode("utf-8")
tree = ast.parse(src)
nodes = [
    n for n in tree.body
    if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == "OFF842"
            for t in n.targets)
]
assert len(nodes) == 1, "OFFLINE_NODE_NOT_UNIQUE"
old = nodes[0].value.value
assert isinstance(old, str)

anchor = "D829['report842'] = {"
assert old.count(anchor) == 1

extra = r'''
# ===== TEST843: OFFLINE MATCHED EVIDENCE/ACTION AUDIT =====
say842('TEST843', 'MATCHED_EVIDENCE_ACTION_AUDIT_BEGIN')

PAIRS843 = (
    ('D_PAIR', 'D_FORKX'),
    ('D_PAIR', 'D_BROKEN'),
    ('D_PAIR', 'D_CONFLICT'),
    ('D_BRIDGE', 'D_BROKEN'),
)
paired843 = {}

for good, bad in PAIRS843:
    left = {x['world']: x for x in DT842[good]}
    right = {x['world']: x for x in DT842[bad]}
    common = sorted(set(left) & set(right))
    rows = []
    for wi in common:
        a, b = left[wi], right[wi]
        row = {
            'world': wi,
            'action_good': a['action'],
            'action_bad': b['action'],
            'delta_answer_p': round(a['pA'] - b['pA'], 5),
            'delta_search_p': round(a['pS'] - b['pS'], 5),
            'delta_drop_p': round(a['pD'] - b['pD'], 5),
            'delta_stop_p': round(a['pX'] - b['pX'], 5),
            'delta_entity_margin': round(
                a['margin'] - b['margin'], 5),
            'good_provisional': a['prov'],
            'bad_provisional': b['prov'],
            'good_answer': a['answer'],
            'bad_answer': b['answer'],
        }
        rows.append(row)
        say842('TEST843_PAIR', good, bad,
               json.dumps(row, ensure_ascii=False))
    paired843[good + '_VS_' + bad] = {
        'n': len(rows),
        'answer_probability_discriminates':
            sum(x['delta_answer_p'] > 0 for x in rows),
        'entity_margin_discriminates':
            sum(x['delta_entity_margin'] > 0 for x in rows),
        'action_changes':
            sum(x['action_good'] != x['action_bad'] for x in rows),
        'mean_delta_answer_p':
            round(float(np.mean(
                [x['delta_answer_p'] for x in rows])), 5)
            if rows else None,
        'mean_delta_entity_margin':
            round(float(np.mean(
                [x['delta_entity_margin'] for x in rows])), 5)
            if rows else None,
    }

say842('TEST843', 'PAIRED_SUMMARY',
       json.dumps(paired843, ensure_ascii=False))

# Same-world, same-start counterfactual trajectory comparison.
trajectories843 = {}
for st in STARTS842:
    by = {
        (x['world'], x['arm']): x
        for x in CASES842 if x['start'] == st
    }
    rows = []
    for wi in range(len(worlds829)):
        n = by.get((wi, 'NORMAL'))
        a = by.get((wi, 'ABLATE'))
        s = by.get((wi, 'SWAP'))
        if not all((n, a, s)):
            continue
        row = {
            'world': wi,
            'normal_end': n['end'],
            'ablate_end': a['end'],
            'swap_end': s['end'],
            'normal_ok': n['terminal_ok'],
            'ablate_ok': a['terminal_ok'],
            'swap_ok': s['terminal_ok'],
            'normal_actions': n['actions'],
            'ablate_actions': a['actions'],
            'swap_actions': s['actions'],
            'normal_routed': n['routed'],
            'ablate_routed': a['routed'],
            'swap_routed': s['routed'],
            'normal_drops': n['drops'],
        }
        rows.append(row)
        say842('TEST843_COUNTERFACTUAL', st,
               json.dumps(row, ensure_ascii=False))
    trajectories843[st] = {
        'n': len(rows),
        'normal_better_than_ablate':
            sum(x['normal_ok'] and not x['ablate_ok']
                for x in rows),
        'ablate_better_than_normal':
            sum(x['ablate_ok'] and not x['normal_ok']
                for x in rows),
        'normal_better_than_swap':
            sum(x['normal_ok'] and not x['swap_ok']
                for x in rows),
        'normal_ablate_action_different':
            sum(x['normal_actions'] != x['ablate_actions']
                for x in rows),
        'normal_ablate_route_different':
            sum(x['normal_routed'] != x['ablate_routed']
                for x in rows),
        'normal_drop_total':
            sum(x['normal_drops'] for x in rows),
    }

say842('TEST843', 'COUNTERFACTUAL_SUMMARY',
       json.dumps(trajectories843, ensure_ascii=False))

# Predeclared diagnostic interpretation, not a cognition PASS.
pair843 = paired843.get('D_PAIR_VS_D_FORKX', {})
broken843 = paired843.get('D_PAIR_VS_D_BROKEN', {})
signal843 = (
    pair843.get('n', 0) == len(worlds829)
    and broken843.get('n', 0) == len(worlds829)
    and pair843.get('answer_probability_discriminates', 0) >= 10
    and broken843.get('answer_probability_discriminates', 0) >= 10
)
action843 = (
    sum(ERRD842) >= 10
    and sum(x['corrected'] for x in CASES842
            if x['arm'] == 'NORMAL') >= 1
)
if signal843 and not action843:
    diagnosis843 = 'SIGNAL_PRESENT_ACTION_CONTROL_UNPROVEN'
elif not signal843:
    diagnosis843 = 'SIGNAL_DISCRIMINATION_NOT_ESTABLISHED'
else:
    diagnosis843 = 'ACTION_BEHAVIOR_REQUIRES_CAUSAL_VALIDATION'

say842('TEST843', 'DIAGNOSTIC_RESULT', diagnosis843)
say842('TEST843', 'IMPORTANT_LIMITATION',
       'First-token probability differences are observational; '
       'they do not establish a causal latent control mechanism.')
say842('TEST843', 'AUTONOMOUS_REASONING',
       'NOT_DEMONSTRATED_BY_THIS_DIAGNOSTIC')

D829['diagnostic843'] = {
    'source_blob': '4653fe9a5dd7bc2dd3a72f25bed00ceebb3936fd',
    'paired': paired843,
    'counterfactual': trajectories843,
    'diagnosis': diagnosis843,
    'autonomous_reasoning': 'NOT_DEMONSTRATED',
}
say842('TEST843', 'AUDIT_COMPLETE')
# ===== END TEST843 =====
'''

new = old.replace(anchor, extra + "\n" + anchor)
lines = src.splitlines(keepends=True)
n = nodes[0]
lines[n.lineno-1:n.end_lineno] = ["OFF842 = " + repr(new) + "\n"]
patched = "".join(lines)

assert patched.count("TEST843_PAIR") == 1
assert patched.count("TEST843_COUNTERFACTUAL") == 1
ast.parse(patched)

print("TEST843_SOURCE_LOCK PASS", blob, flush=True)
print("TEST843_PATCH_AST PASS", flush=True)
print("TEST843_BASELINE TEST842 engine and full panel", flush=True)
print("TEST843_NOTE Diagnostic only; no autonomous PASS claimed",
      flush=True)
print("TEST843_PATCH_SHA256",
      hashlib.sha256(patched.encode()).hexdigest(), flush=True)

exec(compile(patched, "TEST843_CELL", "exec"), globals())
