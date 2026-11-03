# AKBASCORE SILICON HIPPOCAMPUS — TEST854
# Native evidence-resolution re-entry on the locked, GPU-completed TEST853 chain.
# One Colab cell; one A100-SXM4-80GB; frozen Qwen2.5-72B-Instruct NF4.
# GPU execution is not claimed by this source; only the actual run establishes results.
import ast, hashlib, urllib.request

PARENT_URL854 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/853.py'
PARENT_LOCK854 = 'a7033caa10fdb86f8f0ee0b8ed1a0ac7514e26be'
with urllib.request.urlopen(urllib.request.Request(
        PARENT_URL854, headers={'User-Agent': 'AKBASCORE-TEST854'}), timeout=180) as parent_response854:
    parent_raw854 = parent_response854.read(1000001)
parent_actual854 = hashlib.sha1(
    b'blob ' + str(len(parent_raw854)).encode() + b'\0' + parent_raw854
).hexdigest()
assert parent_actual854 == PARENT_LOCK854, ('TEST853_PARENT_LOCK_FAILED', parent_actual854, PARENT_LOCK854)
print('TEST854 SOURCE VERIFICATION')
print('853.py', parent_actual854, 'PASS; TEST854 preserves its verified 852→841 implementation chain')

URL854 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/852.py'
LOCK854 = '4174e9241f773d6a031c51296b6beb11d4637aa5'
with urllib.request.urlopen(urllib.request.Request(
        URL854, headers={'User-Agent': 'AKBASCORE-TEST854'}), timeout=180) as response854:
    raw854 = response854.read(1000001)
actual854 = hashlib.sha1(
    b'blob ' + str(len(raw854)).encode() + b'\0' + raw854
).hexdigest()
assert actual854 == LOCK854, ('TEST852_PARENT_LOCK_FAILED', actual854, LOCK854)
source854 = raw854.decode('utf-8')
tree854 = ast.parse(source854)
print('TEST854 SOURCE VERIFICATION')
print('852.py', actual854, 'PASS; inherited 841–851 locks remain in the locked parent chain')


def nodes854(text):
    return ast.parse(text).body


def one_node854(text):
    nodes = nodes854(text)
    assert len(nodes) == 1
    return nodes[0]


def literal854(tree, name):
    found = [n for n in tree.body if isinstance(n, ast.Assign)
        and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id == name and isinstance(n.value, ast.Constant)
        and isinstance(n.value.value, str)]
    assert len(found) == 1, ('LITERAL_NOT_UNIQUE', name, len(found))
    return found[0].value.value


def set_literal854(tree, name, value):
    found = [n for n in tree.body if isinstance(n, ast.Assign)
        and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id == name]
    assert len(found) == 1, ('LITERAL_TARGET_NOT_UNIQUE', name, len(found))
    found[0].value = ast.Constant(value=value)


def replace_top854(tree, predicate, replacement, label):
    found = [i for i, n in enumerate(tree.body) if predicate(n)]
    assert len(found) == 1, ('AST_TARGET_NOT_UNIQUE', label, len(found))
    nodes = nodes854(replacement) if isinstance(replacement, str) else list(replacement)
    tree.body[found[0]:found[0]+1] = nodes


def replace_child854(parent, predicate, replacement, label):
    found = [i for i, n in enumerate(parent.body) if predicate(n)]
    assert len(found) == 1, ('AST_CHILD_TARGET_NOT_UNIQUE', label, len(found))
    nodes = nodes854(replacement) if isinstance(replacement, str) else list(replacement)
    parent.body[found[0]:found[0]+1] = nodes


def assigned854(node, name):
    return (isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == name for t in node.targets))


def expr_label854(node, label):
    return (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == 'say_r41' and node.value.args
        and isinstance(node.value.args[0], ast.Constant)
        and node.value.args[0].value == label)


def dict_put854(dictionary, key, expression):
    item = one_node854('{' + repr(key) + ': ' + expression + '}')
    assert isinstance(item, ast.Expr) and isinstance(item.value, ast.Dict)
    new_key, new_value = item.value.keys[0], item.value.values[0]
    for i, old_key in enumerate(dictionary.keys):
        if isinstance(old_key, ast.Constant) and old_key.value == key:
            dictionary.values[i] = new_value
            return
    dictionary.keys.append(new_key)
    dictionary.values.append(new_value)


class TEST854Labels(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)
        if (isinstance(node.func, ast.Name)
                and node.func.id in ('say_r41', 'log829', 'gate829')
                and node.args and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
                and node.args[0].value.startswith('TEST852')):
            node.args[0].value = 'TEST854' + node.args[0].value[len('TEST852'):]
        return node

    def visit_Constant(self, node):
        key_map = {
            'test852': 'test854',
            'test852_residual_hook_audit': 'test854_residual_hook_audit',
            'panel852_sha256': 'panel854_sha256',
            'COMPLETE_TEST852': 'COMPLETE_TEST854',
            'PARTIAL_TEST852': 'PARTIAL_TEST854',
            'PRELIMINARY_NATIVE_STOP_CORRECTION_PRESERVATION_SIGNAL': 'PRELIMINARY_PILOT_SIGNAL',
            'TEST852_GAINS_REGRESSED': 'TEST853_GAINS_REGRESSED',
        }
        if isinstance(node.value, str) and node.value in key_map:
            node.value = key_map[node.value]
        return node


class TEST854ArmLiterals(ast.NodeTransformer):
    arm_map = {
        'BASELINE851': 'BASELINE853',
        'NATIVE852': 'NATIVE854',
        'MATCHED_CONTROL852': 'MATCHED_CONTROL854',
    }
    counts = None

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            value = node.value
            for old, new in self.arm_map.items():
                count = value.count(old)
                if count:
                    self.counts[old] += count
                    value = value.replace(old, new)
            node.value = value
        return node


body854 = literal854(tree854, 'BODY851')
off854 = literal854(tree854, 'OFF851')
body_tree854 = ast.parse(body854)
off_tree854 = ast.parse(off854)

replace_top854(body_tree854,
    lambda n: assigned854(n, 'ARMS851'),
    "ARMS851 = ('BASELINE853', 'NATIVE854', 'MATCHED_CONTROL854')",
    'ARMS851')

replace_top854(body_tree854,
    lambda n: assigned854(n, 'PANEL_LOCK851'),
    """PANEL_LOCK851 = {
    'test': 'TEST854', 'jobs': 12, 'arms': list(ARMS851),
    'worlds': list(QORDER851), 'conditions': ['INTACT', 'REMOVED'],
    'initial_modes': MODE851, 'max_reviews_per_job': MAX_REVIEWS851,
    'max_output_tokens_inherited_K845': K845,
    'native_call_cap': CALL_CAP849, 'hard_minutes': HARD_BUDGET_MIN841,
    'counterfactual': 'initial candidate = model hop0 output rows; no answer-key access',
    'baseline853': 'TEST853 NATIVE853 canonical K0/J native decision path',
    'native854': 'K0/J plus native evidence-resolution N in the final decision readout',
    'matched_control854': 'same K0/J/N slots and resolution cost; only U/R inputs to N are swapped',
    'job_specs': [{**{k: j[k] for k in (
        'job', 'qid', 'arm', 'intervention', 'initial_cards', 'bank'
    )}, 'initial_mode': MODE851[j['qid']]} for j in JOBS841]
}""",
    'PANEL_LOCK851')

# Only two numerical slot markers are added; REVIEW851 and all cognitive prompts stay unchanged.
rslot854 = next(i for i, n in enumerate(body_tree854.body) if assigned854(n, 'R_SLOT852'))
body_tree854.body[rslot854+1:rslot854+1] = nodes854("""
K_SLOT854 = list(tok('Native precontrol state:', add_special_tokens=False).input_ids)
J_SLOT854 = list(tok('Candidate-evidence gated control state:', add_special_tokens=False).input_ids)
N_SLOT854 = list(tok('Native evidence-resolution state:', add_special_tokens=False).input_ids)
""")

replace_top854(body_tree854,
    lambda n: expr_label854(n, 'TEST852 RESEARCH HYPOTHESES'),
    """say_r41('TEST854 RESEARCH HYPOTHESES',
    'Preserve TEST853 correction and preservation while adding native evidence-resolution N to the final '
    'K0/J action readout. N may encode an unresolved missing dependency; its text is never parsed as an action. '
    'STOP is never Python-generated.')""",
    'RESEARCH_HYPOTHESES')
replace_top854(body_tree854,
    lambda n: expr_label854(n, 'TEST852 ENGINE MODIFICATION'),
    """say_r41('TEST854 ENGINE MODIFICATION',
    'Only the native evidence-resolution forward and final decision inputs change. SUPPORT/BIND remain absent. '
    'Physical CUT3/H3/KV, NF4 loading, cache construction, RoPE accounting, BF16 execution, frozen weights '
    'and offline scoring remain inherited.')""",
    'ENGINE_MODIFICATION')
replace_top854(body_tree854,
    lambda n: expr_label854(n, 'TEST852 NATIVE CONTROL MECHANISM'),
    """say_r41('TEST854 NATIVE CONTROL MECHANISM',
    'All arms share canonical C/E/Kprev/U/R precontrol K0 and support gate J. NATIVE854 and matched compute '
    'N through the same native RECOMPUTE path; only the resolution U/R inputs are swapped in matched. '
    'Final K0/J/N slots are identical in both arms.')""",
    'NATIVE_CONTROL_MECHANISM')
replace_top854(body_tree854,
    lambda n: expr_label854(n, 'TEST852 MATHEMATICAL DESIGN'),
    """say_r41('TEST854 MATHEMATICAL DESIGN',
    'K0=F_852(C,E,Kprev,U,R,Q); J=K0 Hadamard RMSNorm(mean(C) Hadamard mean(E)); '
    'N=H_native(C,E,K0,U,R,Q); K=G_native(K0,J,N,Q); A=Parse(Greedy(K)); '
    'C_next=H_native(C,E,K,U,R,Q). Matched changes only N=H_native(C,E,K0,R,U,Q). '
    'No new learned parameter, cognitive prompt, action threshold or Python decision is introduced.')""",
    'MATHEMATICAL_DESIGN')

# Replace TEST852 routing with the gated interaction and the matched re-entry routing.
replace_top854(body_tree854,
    lambda n: isinstance(n, ast.FunctionDef) and n.name == 'route852',
    """def interaction854(C, E, K0):
    assert C.ndim == E.ndim == K0.ndim == 2
    assert C.shape[1] == E.shape[1] == K0.shape[1] == H
    assert C.device.type == E.device.type == K0.device.type == 'cpu'
    assert C.dtype == E.dtype == K0.dtype == torch.float32
    assert K0.shape[0] > 0, 'EMPTY_NATIVE_PRECONTROL'
    c, e = pooled852(C), pooled852(E)
    gate = (c * e).contiguous()
    rms = gate.square().mean().sqrt().clamp_min(1e-12)
    gate = (gate / rms).contiguous()
    J = (K0 * gate.unsqueeze(0)).contiguous()
    assert J.shape == K0.shape and J.dtype == torch.float32
    assert torch.isfinite(J).all().item()
    return J


def route854(arm, K0, J):
    assert arm in ('BASELINE853', 'NATIVE854', 'MATCHED_CONTROL854')
    assert K0.shape == J.shape and K0.dtype == J.dtype
    return K0, J


def resolution_route854(arm, U, R):
    assert U.device.type == R.device.type == 'cpu'
    assert U.dtype == R.dtype == torch.float32
    assert torch.isfinite(U).all().item() and torch.isfinite(R).all().item()
    if arm == 'NATIVE854':
        return U, R
    assert arm == 'MATCHED_CONTROL854'
    return R, U
""",
    'ROUTE852_TO_INTERACTION854')

# Locate the one experiment loop and its one review-cycle loop without rewriting the parent engine.
experiment854 = [n for n in body_tree854.body if isinstance(n, ast.For)
    and isinstance(n.target, ast.Tuple)
    and any(isinstance(x, ast.Name) and x.id == 'ji846' for x in n.target.elts)]
assert len(experiment854) == 1
experiment854 = experiment854[0]
cycle854 = [n for n in ast.walk(experiment854) if isinstance(n, ast.For)
    and isinstance(n.target, ast.Name) and n.target.id == 'cycle851']
assert len(cycle854) == 1
cycle854 = cycle854[0]
experiment_position854 = body_tree854.body.index(experiment854)
body_tree854.body[experiment_position854:experiment_position854] = nodes854('smoke854_done = False')

# All three arms run the identical TEST853 canonical precontrol, including BASELINE853.
coverage_parent854 = [n for n in ast.walk(experiment854) if isinstance(getattr(n, 'body', None), list)
    and any(isinstance(x, ast.If) and any(assigned854(y, 'coverage_h852') for y in x.body)
        for x in n.body)]
assert len(coverage_parent854) == 1
replace_child854(coverage_parent854[0],
    lambda n: isinstance(n, ast.If) and any(assigned854(x, 'coverage_h852') for x in n.body),
    "coverage_h852 = coverage_state852(q851, condition851, mode851, mx851)",
    'COVERAGE_FOR_ALL_ARMS')

replace_child854(cycle854,
    lambda n: isinstance(n, ast.If) and "'review_%d'" in ast.unparse(n),
    """C851, E851 = intervened851(arm851, candidate851['rows'], evidence851['rows'])
relation_rows852 = relation852(C851, E851)
routed_u852, routed_r852 = coverage_h852['rows'], relation_rows852
pre851 = list(prompt_ids(REVIEW851.format(q=QTEXT841[q851])))
segments851 = [(C_SLOT851, C851), (E_SLOT851, E851)]
if previous_control851 is not None:
    segments851.append((K_SLOT851, previous_control851['rows']))
segments851.extend([(U_SLOT852, routed_u852), (R_SLOT852, routed_r852)])
precontrol851 = invoke851(mx851, pre851, segments851, REVIEW_SUFFIX851,
    'precontrol_%d'%cycle851, tensors851, traces851)
interaction_rows854 = interaction854(C851, E851, precontrol851['rows'])
routed_control854, routed_interaction854 = route854(
    arm851, precontrol851['rows'], interaction_rows854)
assert routed_control854.shape == routed_interaction854.shape
resolution854, resolution_u854, resolution_r854 = None, None, None
decision_segments854 = [(K_SLOT854, routed_control854),
    (J_SLOT854, routed_interaction854)]
if arm851 != 'BASELINE853':
    resolution_u854, resolution_r854 = resolution_route854(
        arm851, coverage_h852['rows'], relation_rows852)
    resolution_pre854 = list(prompt_ids(RECOMPUTE851.format(q=QTEXT841[q851])))
    resolution854 = invoke851(mx851, resolution_pre854,
        [(C_SLOT851, C851), (K_SLOT851, precontrol851['rows']),
         (E_SLOT851, E851), (U_SLOT852, resolution_u854),
         (R_SLOT852, resolution_r854)], ANSWER_SUFFIX851,
        'resolution_%d'%cycle851, tensors851, traces851)
    assert resolution854['rows'].shape[1] == H
    assert resolution854['rows'].dtype == torch.float32
    assert torch.isfinite(resolution854['rows']).all().item()
    decision_segments854.append((N_SLOT854, resolution854['rows']))
review851 = invoke851(mx851, pre851, decision_segments854, REVIEW_SUFFIX851,
    'review_%d'%cycle851, tensors851, traces851)
""",
    'NATIVE_DECISION_REENTRY')

# Extend the existing event record; no cognitive field is computed here.
event_assign854 = [n for n in cycle854.body if assigned854(n, 'event851')]
assert len(event_assign854) == 1 and isinstance(event_assign854[0].value, ast.Dict)
event_dict854 = event_assign854[0].value
dict_put854(event_dict854, 'precontrol', 'result849(precontrol851)')
dict_put854(event_dict854, 'interaction_state',
    'None if interaction_rows854 is None else stats849(interaction_rows854)')
dict_put854(event_dict854, 'routed_control_state',
    'None if routed_control854 is None else stats849(routed_control854)')
dict_put854(event_dict854, 'routed_interaction_state',
    'None if routed_interaction854 is None else stats849(routed_interaction854)')
dict_put854(event_dict854, 'resolution',
    'None if resolution854 is None else result849(resolution854)')
dict_put854(event_dict854, 'resolution_coverage_state',
    'None if resolution_u854 is None else stats849(resolution_u854)')
dict_put854(event_dict854, 'resolution_relation_state',
    'None if resolution_r854 is None else stats849(resolution_r854)')

# REVISE retains the TEST852 native feedback path and uses the current cycle's final K, U and R.
revise854 = [n for n in cycle854.body if isinstance(n, ast.If)
    and any(isinstance(x, ast.If) and "'revision_%d'" in ast.unparse(x) for x in n.body)]
# The action chain is an If nested in cycle body; locate its REVISE branch directly.
action_chain854 = next(n for n in cycle854.body if isinstance(n, ast.If)
    and isinstance(n.test, ast.Compare) and "'CONTINUE'" in ast.unparse(n.test))
revise_branch854 = next(n for n in ast.walk(action_chain854) if isinstance(n, ast.If)
    and "'REVISE'" in ast.unparse(n.test))
replace_child854(revise_branch854,
    lambda n: isinstance(n, ast.If) and "'revision_%d'" in ast.unparse(n),
    """current851 = invoke851(mx851, recompute_pre851,
    [(C_SLOT851, C851), (K_SLOT851, review851['rows']),
     (E_SLOT851, E851), (U_SLOT852, routed_u852),
     (R_SLOT852, routed_r852)], ANSWER_SUFFIX851,
    'revision_%d'%cycle851, tensors851, traces851)
""",
    'UNIFIED_NATIVE_REVISION')

# Add one compact bridge audit beside the inherited control-state report.
control_log854 = next(i for i, n in enumerate(cycle854.body)
    if expr_label854(n, 'TEST852 CONTROL STATE'))
cycle854.body[control_log854+1:control_log854+1] = nodes854("""
say_r41('TEST854 DECISION BRIDGE', q851, condition851, arm851,
    'CYCLE='+str(cycle851), json.dumps({
        'precontrol':event851['precontrol']['output'],
        'J':event851['interaction_state'],
        'N':event851['resolution'],
        'routed_K0':event851['routed_control_state'],
        'routed_J':event851['routed_interaction_state'],
        'resolution_U':event851['resolution_coverage_state'],
        'resolution_R':event851['resolution_relation_state']}))
say_r41('TEST854 DECISION SCORES', q851, condition851, arm851,
    'CYCLE='+str(cycle851), json.dumps({
        'token_ids':event851['control_token_ids'],
        'top_logits_probabilities':event851['control_token_scores']}))
say_r41('TEST854 RESOLUTION VS DECISION', q851, condition851, arm851,
    'CYCLE='+str(cycle851),
    'N_TEXT='+repr(None if resolution854 is None else resolution854['text']),
    'ACTION='+action851)
if arm851 == 'NATIVE854' and not smoke854_done:
    assert resolution854 is not None
    assert review851['trace849']['continuity']['exact_after_bf16']
    assert resolution854['trace849']['continuity']['exact_after_bf16']
    assert resolution854['rows'].shape[1] == H
    smoke854_done = True
    say_r41('TEST854 GPU SMOKE', 'PASS', q851, condition851,
        'K0/J/N native path, BF16 cache continuity and final decision readout verified in this run')
""")

# Exact arm literals in BODY/OFF are computational identifiers, not historical prose.
body_arms854 = TEST854ArmLiterals(); body_arms854.counts = {k:0 for k in body_arms854.arm_map}
off_arms854 = TEST854ArmLiterals(); off_arms854.counts = {k:0 for k in off_arms854.arm_map}
body_tree854 = body_arms854.visit(body_tree854)
off_tree854 = off_arms854.visit(off_tree854)
body_tree854 = TEST854Labels().visit(body_tree854)
off_tree854 = TEST854Labels().visit(off_tree854)
ast.fix_missing_locations(body_tree854); ast.fix_missing_locations(off_tree854)

# Offline: verify identical canonical inputs and a strictly matched K0/J intervention.
off_loop854 = next(n for n in ast.walk(off_tree854) if isinstance(n, ast.For)
    and isinstance(n.target, ast.Name) and n.target.id == 'condition'
    and any(assigned854(x, 'baseline') for x in n.body))
score_assign854 = next(i for i, n in enumerate(off_loop854.body) if assigned854(n, 'score_change'))
old_swap_asserts854 = [n for n in off_loop854.body if isinstance(n, ast.Assert)
    and ('routed_coverage_state' in ast.unparse(n) or 'routed_relation_state' in ast.unparse(n))]
assert len(old_swap_asserts854) == 2
for old_assert854 in old_swap_asserts854:
    off_loop854.body.remove(old_assert854)
score_assign854 = next(i for i, n in enumerate(off_loop854.body) if assigned854(n, 'score_change'))
off_loop854.body[score_assign854+1:score_assign854+1] = nodes854("""
b0 = baseline['cycles'][0]
for matched_arm854 in ARMS851:
    matched_record854 = group[matched_arm854]
    matched_cycle854 = matched_record854['cycles'][0]
    assert matched_record854['initial']['output']['sha256'] == native['initial']['output']['sha256']
    assert matched_record854['evidence_native']['output']['sha256'] == native['evidence_native']['output']['sha256']
    assert matched_cycle854['candidate_intervened']['sha256'] == n0['candidate_intervened']['sha256']
    assert matched_cycle854['evidence_intervened']['sha256'] == n0['evidence_intervened']['sha256']
    assert matched_cycle854['coverage_native']['output']['sha256'] == n0['coverage_native']['output']['sha256']
    assert matched_cycle854['relation_state']['sha256'] == n0['relation_state']['sha256']
assert b0['precontrol']['output']['sha256'] == n0['precontrol']['output']['sha256']
assert n0['precontrol']['output']['sha256'] == m0['precontrol']['output']['sha256']
assert n0['interaction_state']['sha256'] == m0['interaction_state']['sha256']
assert n0['precontrol']['output']['shape'] == n0['interaction_state']['shape']
assert n0['routed_control_state']['sha256'] == n0['precontrol']['output']['sha256']
assert n0['routed_interaction_state']['sha256'] == n0['interaction_state']['sha256']
assert m0['routed_control_state']['sha256'] == m0['precontrol']['output']['sha256']
assert m0['routed_interaction_state']['sha256'] == m0['interaction_state']['sha256']
assert n0['resolution'] is not None and m0['resolution'] is not None
assert n0['resolution_coverage_state']['sha256'] == n0['coverage_native']['output']['sha256']
assert n0['resolution_relation_state']['sha256'] == n0['relation_state']['sha256']
assert m0['resolution_coverage_state']['sha256'] == m0['relation_state']['sha256']
assert m0['resolution_relation_state']['sha256'] == m0['coverage_native']['output']['sha256']
native_resolution_norm854 = n0['resolution_coverage_state']['norm']**2 + n0['resolution_relation_state']['norm']**2
matched_resolution_norm854 = m0['resolution_coverage_state']['norm']**2 + m0['resolution_relation_state']['norm']**2
assert abs(native_resolution_norm854-matched_resolution_norm854) <= 1e-6*max(1.0,native_resolution_norm854)
resolution_change = n0['resolution']['output']['sha256'] != m0['resolution']['output']['sha256']
""")
group_append854 = next(n for n in ast.walk(off_loop854) if isinstance(n, ast.Expr)
    and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Attribute)
    and n.value.func.attr == 'append' and isinstance(n.value.func.value, ast.Name)
    and n.value.func.value.id == 'groups851')
group_dict854 = group_append854.value.args[0]
assert isinstance(group_dict854, ast.Dict)
dict_put854(group_dict854, 'resolution_change', 'resolution_change')
dict_put854(group_dict854, 'causal_observation',
    'resolution_change and state_change and (decision_change or score_change)')

# Require actual K0/J/N events for native coupling; empty or missing records cannot pass vacuously.
verdict_assign854 = next(n for n in off_tree854.body if assigned854(n, 'verdicts851'))
verdict_index854 = off_tree854.body.index(verdict_assign854)
off_tree854.body[verdict_index854:verdict_index854] = nodes854("""
bridge_events854 = [e for r in records851 if r['arm'] == 'NATIVE854' for e in r['cycles']]
bridge_pass854 = bool(bridge_events854) and all(
    e.get('precontrol') is not None and e.get('interaction_state') is not None
    and e.get('routed_control_state') is not None and e.get('routed_interaction_state') is not None
    and e.get('resolution') is not None and e.get('resolution_coverage_state') is not None
    and e.get('resolution_relation_state') is not None
    and e['precontrol']['output']['shape'] == e['interaction_state']['shape']
    and e['resolution']['output']['shape'][1] == H
    for e in bridge_events854)
""")
verdict_dict854 = verdict_assign854.value
assert isinstance(verdict_dict854, ast.Dict)
dict_put854(verdict_dict854, 'NATIVE_CONTROL_COUPLING',
    "'PASS' if transfer_pass851 and bridge_pass854 else 'INCONCLUSIVE'")

# The strongest preliminary verdict additionally requires the bridge and a real decision change.
final_if854 = next(n for n in off_tree854.body if isinstance(n, ast.If)
    and any(assigned854(x, 'final_verdict851') for x in n.body))
for branch854 in ast.walk(final_if854):
    if isinstance(branch854, ast.If) and isinstance(branch854.test, ast.Call):
        call854 = branch854.test
        if (isinstance(call854.func, ast.Name) and call854.func.id == 'all'
                and 'stop_pass851' in ast.unparse(call854)):
            tuple_node854 = call854.args[0]
            assert isinstance(tuple_node854, ast.Tuple)
            tuple_node854.elts.append(ast.Name(id='bridge_pass854', ctx=ast.Load()))

# Replace only outdated engineering prose; the evaluation mathematics is unchanged.
replace_top854(off_tree854,
    lambda n: expr_label854(n, 'TEST854 FAILURE ANALYSIS'),
    """say_r41('TEST854 FAILURE ANALYSIS',
    'UNKNOWN generation and REVISE are distinct native behaviors. N or logit changes alone are not STOP. '
    'Mechanical limits are not model STOP. Any INVALID makes the comparison PROTOCOL_INVALID. '
    'TEST853 non-regression and this 12-job pilot do not establish population superiority. '
    'Summary='+json.dumps(summary851))""",
    'FAILURE_ANALYSIS')
replace_top854(off_tree854,
    lambda n: assigned854(n, 'next851'),
    """next851 = ('Judge only final model decisions against BASELINE853 and matched native-resolution routing. '
    'UNKNOWN generation, state changes and score changes alone are not STOP or task success. '
    'Research request remains unimplemented; do not claim it.')""",
    'NEXT_ENGINEERING_STEP')
replace_top854(off_tree854,
    lambda n: assigned854(n, 'report851'),
    """report851 = ('TEST854 completed %d/12 jobs; %d matched groups; NATIVE854 wrong opportunities=%d; '
    'recurrent Kprev edges=%d; native-resolution causal observations=%s; final decision changes=%s; verdict=%s. '
    'GPU results are established only by this executed run.') % (
        len(cases851),len(groups851),wrong_native852,recurrent_edges851,
        causal852,decision_causal852,final_verdict851)""",
    'FINAL_REPORT')

# Record the immediate parent lock as well as all inherited locks in the result artifact.
test_artifact854 = [n for n in off_tree854.body if isinstance(n, ast.Assign)
    and isinstance(n.targets[0], ast.Subscript) and isinstance(n.value, ast.Dict)
    and isinstance(n.targets[0].slice, ast.Constant) and n.targets[0].slice.value == 'test854']
assert len(test_artifact854) == 1
artifact_dict854 = test_artifact854[0].value
source_lock_node854 = next(v for k, v in zip(artifact_dict854.keys, artifact_dict854.values)
    if isinstance(k, ast.Constant) and k.value == 'source_locks')
assert isinstance(source_lock_node854, ast.Call) and isinstance(source_lock_node854.func, ast.Name)
assert source_lock_node854.func.id == 'dict'
lock_extra854 = [k.value for k in source_lock_node854.keywords if k.arg is None]
assert len(lock_extra854) == 1 and isinstance(lock_extra854[0], ast.Dict)
lock_extra854 = lock_extra854[0]
assert not any(isinstance(k, ast.Constant) and k.value == '852.py' for k in lock_extra854.keys)
lock_extra854.keys.append(ast.Constant('852.py'))
lock_extra854.values.append(ast.Constant(LOCK854))
lock_extra854.keys.append(ast.Constant('853.py'))
lock_extra854.values.append(ast.Constant(PARENT_LOCK854))
verdict_artifact854 = [n for n in off_tree854.body if isinstance(n, ast.Assign)
    and isinstance(n.targets[0], ast.Subscript) and isinstance(n.value, ast.Dict)
    and isinstance(n.targets[0].slice, ast.Constant) and n.targets[0].slice.value == 'verdict841R']
assert len(verdict_artifact854) == 1
dict_put854(verdict_artifact854[0].value, 'reason',
    "'Pre-registered 12-job TEST854 K0/J/N native evidence-resolution panel.'")

body854 = ast.unparse(body_tree854) + '\n'
off854 = '\n' + ast.unparse(off_tree854) + '\n'
assert 'SUPPORT854' not in body854 and 'BIND854' not in body854
assert body854.count('def interaction854(') == 1
assert body854.count('def route854(') == 1
assert body854.count('def resolution_route854(') == 1
assert body854.count('def route852(') == 0
assert body854.count('for ji846, j846 in enumerate(JOBS841)') == 1
assert "'MODEL_NATIVE_RESEARCH_REQUEST': 'NOT_IMPLEMENTED_PROTOCOL_UNCHANGED'" in off854
for block854 in (body854, off854):
    ast.parse(block854)
    compile(block854, '<TEST854_EMBEDDED>', 'exec')

# Replace only the two locked literals in the TEST852 wrapper AST.
set_literal854(tree854, 'BODY851', body854)
set_literal854(tree854, 'OFF851', off854)

# Update only source852-producing assignments whose embedded panel code must create the three new arms.
source_assignments854 = [n for n in tree854.body if assigned854(n, 'source852')]
panel_arms854 = TEST854ArmLiterals(); panel_arms854.counts = {k:0 for k in panel_arms854.arm_map}
for assignment854 in source_assignments854:
    panel_arms854.visit(assignment854)
assert panel_arms854.counts['BASELINE851'] >= 3
assert panel_arms854.counts['NATIVE852'] >= 3
assert panel_arms854.counts['MATCHED_CONTROL852'] >= 3
# The nested 851 builder must assert the new residual-hook audit label, not the old TEST852 label.
nested_label854 = [n for n in source_assignments854 if isinstance(n.value, ast.Call)
    and isinstance(n.value.func, ast.Attribute) and n.value.func.attr == 'replace'
    and len(n.value.args) == 2
    and all(isinstance(a, ast.Constant) for a in n.value.args)
    and n.value.args[0].value == 'TEST851' and n.value.args[1].value == 'TEST852']
assert len(nested_label854) == 1
nested_label854[0].value.args[1].value = 'TEST854'

# Strengthen, rather than remove, the inherited static preflight for the modified embedded body.
replace_top854(tree854,
    lambda n: isinstance(n, ast.Assert) and 'function852' in ast.unparse(n)
        and 'set(' in ast.unparse(n) and 'coverage_state852' in ast.unparse(n),
    """assert set(('gen851','invoke851','shared851','intervened851','relation852',
    'interaction854','route854','resolution_route854','coverage_state852')) <= set(function852)""",
    'FUNCTION_SET_PREFLIGHT')
replace_top854(tree854,
    lambda n: isinstance(n, ast.Assert) and "function852['route852']" in ast.unparse(n),
    "assert [a.arg for a in function852['route854'].args.args] == ['arm','K0','J']",
    'ROUTE_SIGNATURE_PREFLIGHT')
replace_top854(tree854,
    lambda n: isinstance(n, ast.Assert) and 'TEST852_NO_RESIDUAL_HOOKS_BEFORE_FINAL' in ast.unparse(n),
    "assert 'TEST854_NO_RESIDUAL_HOOKS_BEFORE_FINAL' in BODY851",
    'RESIDUAL_HOOK_LABEL_PREFLIGHT')
replace_top854(tree854,
    lambda n: isinstance(n, ast.Assert) and 'ARMS851 = ' in ast.unparse(n),
    """assert "ARMS851 = ('BASELINE853', 'NATIVE854', 'MATCHED_CONTROL854')" in BODY851""",
    'ARM_PREFLIGHT')
replace_top854(tree854,
    lambda n: isinstance(n, ast.Assert) and 'MODEL_NATIVE_RESEARCH_REQUEST' in ast.unparse(n),
    "assert \"'MODEL_NATIVE_RESEARCH_REQUEST': 'NOT_IMPLEMENTED_PROTOCOL_UNCHANGED'\" in OFF851",
    'RESEARCH_REQUEST_PREFLIGHT')
replace_top854(tree854,
    lambda n: isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
        and 'matched U/R slot-routing control' in ast.unparse(n),
    "print('PANEL: 12 jobs; 2 cycles maximum; matched native evidence-resolution control')",
    'PANEL_PREFLIGHT_LABEL')

# Additional preflight invariants: final readout is K0/J, with N appended only for the two new arms.
final_decision854 = ast.parse(body854)
decision_assignments854 = [n for n in ast.walk(final_decision854) if isinstance(n, ast.Assign)
    and isinstance(n.value, ast.List)
    and any(isinstance(t, ast.Name) and t.id == 'decision_segments854' for t in n.targets)]
assert len(decision_assignments854) == 1
decision_slots854 = {n.id for n in ast.walk(decision_assignments854[0]) if isinstance(n, ast.Name)}
assert {'K_SLOT854', 'J_SLOT854', 'routed_control854', 'routed_interaction854'} <= decision_slots854
assert not decision_slots854 & {'C_SLOT851', 'E_SLOT851', 'U_SLOT852', 'R_SLOT852'}
resolution_appends854 = [n for n in ast.walk(final_decision854) if isinstance(n, ast.Call)
    and isinstance(n.func, ast.Attribute) and n.func.attr == 'append'
    and isinstance(n.func.value, ast.Name) and n.func.value.id == 'decision_segments854'
    and 'N_SLOT854' in ast.unparse(n)]
assert len(resolution_appends854) == 1
assert 'out.last_hidden_state' not in body854 and 'output_hidden_states' not in body854
assert 'register_forward_hook' not in body854 and 'register_forward_pre_hook' not in body854
assert '.backward(' not in body854 and 'optimizer' not in body854.lower()
assert "j['initial_mode']" not in body854 + off854
assert "j851['initial_mode']" not in body854 + off854

source854 = ast.unparse(tree854) + '\n'
final_tree854 = ast.parse(source854)
compile(final_tree854, 'TEST854_LOCKED_BUILDER', 'exec')
print('TEST854 LOCKED ENGINE VERIFICATION')
print('PARENT GIT BLOB: PASS | TARGETED AST PATCHES: PASS | EMBEDDED COMPILE: PASS')
print('NO GENERAL SOURCE.REPLACE IN TEST854 | NO SUPPORT/BIND | K0/J/N BOTTLENECK: PRESENT')
print('PANEL: 12 jobs; 2 worlds x 2 conditions x 3 arms; matched native-resolution routing')
print('BUILDER SHA256:', hashlib.sha256(source854.encode()).hexdigest())
print('GPU EXECUTION: NOT VERIFIED BY AUTHOR; only this Colab run can establish it', flush=True)
exec(compile(final_tree854, 'TEST854_LOCKED_BUILDER', 'exec'), globals())
