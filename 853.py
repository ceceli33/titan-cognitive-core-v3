# AKBASCORE SILICON HIPPOCAMPUS — TEST853
# Native gated decision re-entry on the locked, GPU-completed TEST852 chain.
# One Colab cell; one A100-SXM4-80GB; frozen Qwen2.5-72B-Instruct NF4.
# GPU execution is not claimed by this source; only the actual run establishes results.
import ast, hashlib, urllib.request

URL853 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/852.py'
LOCK853 = '4174e9241f773d6a031c51296b6beb11d4637aa5'
with urllib.request.urlopen(urllib.request.Request(
        URL853, headers={'User-Agent': 'AKBASCORE-TEST853'}), timeout=180) as response853:
    raw853 = response853.read(1000001)
actual853 = hashlib.sha1(
    b'blob ' + str(len(raw853)).encode() + b'\0' + raw853
).hexdigest()
assert actual853 == LOCK853, ('TEST852_PARENT_LOCK_FAILED', actual853, LOCK853)
source853 = raw853.decode('utf-8')
tree853 = ast.parse(source853)
print('TEST853 SOURCE VERIFICATION')
print('852.py', actual853, 'PASS; inherited 841–851 locks remain in the locked parent chain')


def nodes853(text):
    return ast.parse(text).body


def one_node853(text):
    nodes = nodes853(text)
    assert len(nodes) == 1
    return nodes[0]


def literal853(tree, name):
    found = [n for n in tree.body if isinstance(n, ast.Assign)
        and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id == name and isinstance(n.value, ast.Constant)
        and isinstance(n.value.value, str)]
    assert len(found) == 1, ('LITERAL_NOT_UNIQUE', name, len(found))
    return found[0].value.value


def set_literal853(tree, name, value):
    found = [n for n in tree.body if isinstance(n, ast.Assign)
        and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id == name]
    assert len(found) == 1, ('LITERAL_TARGET_NOT_UNIQUE', name, len(found))
    found[0].value = ast.Constant(value=value)


def replace_top853(tree, predicate, replacement, label):
    found = [i for i, n in enumerate(tree.body) if predicate(n)]
    assert len(found) == 1, ('AST_TARGET_NOT_UNIQUE', label, len(found))
    nodes = nodes853(replacement) if isinstance(replacement, str) else list(replacement)
    tree.body[found[0]:found[0]+1] = nodes


def replace_child853(parent, predicate, replacement, label):
    found = [i for i, n in enumerate(parent.body) if predicate(n)]
    assert len(found) == 1, ('AST_CHILD_TARGET_NOT_UNIQUE', label, len(found))
    nodes = nodes853(replacement) if isinstance(replacement, str) else list(replacement)
    parent.body[found[0]:found[0]+1] = nodes


def assigned853(node, name):
    return (isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == name for t in node.targets))


def expr_label853(node, label):
    return (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == 'say_r41' and node.value.args
        and isinstance(node.value.args[0], ast.Constant)
        and node.value.args[0].value == label)


def dict_put853(dictionary, key, expression):
    item = one_node853('{' + repr(key) + ': ' + expression + '}')
    assert isinstance(item, ast.Expr) and isinstance(item.value, ast.Dict)
    new_key, new_value = item.value.keys[0], item.value.values[0]
    for i, old_key in enumerate(dictionary.keys):
        if isinstance(old_key, ast.Constant) and old_key.value == key:
            dictionary.values[i] = new_value
            return
    dictionary.keys.append(new_key)
    dictionary.values.append(new_value)


class TEST853Labels(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)
        if (isinstance(node.func, ast.Name)
                and node.func.id in ('say_r41', 'log829', 'gate829')
                and node.args and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
                and node.args[0].value.startswith('TEST852')):
            node.args[0].value = 'TEST853' + node.args[0].value[len('TEST852'):]
        return node

    def visit_Constant(self, node):
        key_map = {
            'test852': 'test853',
            'test852_residual_hook_audit': 'test853_residual_hook_audit',
            'panel852_sha256': 'panel853_sha256',
            'COMPLETE_TEST852': 'COMPLETE_TEST853',
            'PARTIAL_TEST852': 'PARTIAL_TEST853',
        }
        if isinstance(node.value, str) and node.value in key_map:
            node.value = key_map[node.value]
        return node


class TEST853ArmLiterals(ast.NodeTransformer):
    arm_map = {
        'BASELINE851': 'BASELINE852',
        'NATIVE852': 'NATIVE853',
        'MATCHED_CONTROL852': 'MATCHED_CONTROL853',
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


body853 = literal853(tree853, 'BODY851')
off853 = literal853(tree853, 'OFF851')
body_tree853 = ast.parse(body853)
off_tree853 = ast.parse(off853)

replace_top853(body_tree853,
    lambda n: assigned853(n, 'ARMS851'),
    "ARMS851 = ('BASELINE852', 'NATIVE853', 'MATCHED_CONTROL853')",
    'ARMS851')

replace_top853(body_tree853,
    lambda n: assigned853(n, 'PANEL_LOCK851'),
    """PANEL_LOCK851 = {
    'test': 'TEST853', 'jobs': 12, 'arms': list(ARMS851),
    'worlds': list(QORDER851), 'conditions': ['INTACT', 'REMOVED'],
    'initial_modes': MODE851, 'max_reviews_per_job': MAX_REVIEWS851,
    'max_output_tokens_inherited_K845': K845,
    'native_call_cap': CALL_CAP849, 'hard_minutes': HARD_BUDGET_MIN841,
    'counterfactual': 'initial candidate = model hop0 output rows; no answer-key access',
    'baseline852': 'TEST852 NATIVE852 C/E/Kprev/U/R native control path',
    'native853': 'K0 native precontrol, candidate-evidence gated J, K0/J-only decision re-entry',
    'matched_control853': 'identical K0/J values and shapes with semantic slots swapped only at re-entry',
    'job_specs': [{**{k: j[k] for k in (
        'job', 'qid', 'arm', 'intervention', 'initial_cards', 'bank'
    )}, 'initial_mode': MODE851[j['qid']]} for j in JOBS841]
}""",
    'PANEL_LOCK851')

# Only two numerical slot markers are added; REVIEW851 and all cognitive prompts stay unchanged.
rslot853 = next(i for i, n in enumerate(body_tree853.body) if assigned853(n, 'R_SLOT852'))
body_tree853.body[rslot853+1:rslot853+1] = nodes853("""
K_SLOT853 = list(tok('Native precontrol state:', add_special_tokens=False).input_ids)
J_SLOT853 = list(tok('Candidate-evidence gated control state:', add_special_tokens=False).input_ids)
""")

replace_top853(body_tree853,
    lambda n: expr_label853(n, 'TEST852 RESEARCH HYPOTHESES'),
    """say_r41('TEST853 RESEARCH HYPOTHESES',
    'Preserve TEST852 correction and preservation while separating native precontrol K0 from '
    'the final action readout through a candidate-evidence gated control tensor J. STOP is never Python-generated.')""",
    'RESEARCH_HYPOTHESES')
replace_top853(body_tree853,
    lambda n: expr_label853(n, 'TEST852 ENGINE MODIFICATION'),
    """say_r41('TEST853 ENGINE MODIFICATION',
    'Only control decision re-entry changes. SUPPORT/BIND are absent. Physical CUT3/H3/KV, NF4 loading, '
    'cache construction, RoPE accounting, BF16 execution, frozen weights and offline scoring remain inherited.')""",
    'ENGINE_MODIFICATION')
replace_top853(body_tree853,
    lambda n: expr_label853(n, 'TEST852 NATIVE CONTROL MECHANISM'),
    """say_r41('TEST853 NATIVE CONTROL MECHANISM',
    'All arms share the canonical TEST852 C/E/Kprev/U/R precontrol. NATIVE853 re-enters K0 and '
    'J=K0*RMSNorm(mean(C)*mean(E)); matched swaps only the K0/J slots at the final native readout.')""",
    'NATIVE_CONTROL_MECHANISM')
replace_top853(body_tree853,
    lambda n: expr_label853(n, 'TEST852 MATHEMATICAL DESIGN'),
    """say_r41('TEST853 MATHEMATICAL DESIGN',
    'K0=F_852(C,E,Kprev,U,R,Q); J=K0 Hadamard RMSNorm(mean(C) Hadamard mean(E)); '
    'K=G_native(K0,J,Q); A=Parse(Greedy(K)); C_next=H_native(C,E,K,U,R). '
    'No new learned parameter, cognitive prompt, action threshold or Python decision is introduced.')""",
    'MATHEMATICAL_DESIGN')

# Replace TEST852 routing with the gated interaction and the matched re-entry routing.
replace_top853(body_tree853,
    lambda n: isinstance(n, ast.FunctionDef) and n.name == 'route852',
    """def interaction853(C, E, K0):
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


def route853(arm, K0, J):
    assert K0.shape == J.shape and K0.dtype == J.dtype
    if arm == 'NATIVE853':
        return K0, J
    assert arm == 'MATCHED_CONTROL853'
    return J, K0
""",
    'ROUTE852_TO_INTERACTION853')

# Locate the one experiment loop and its one review-cycle loop without rewriting the parent engine.
experiment853 = [n for n in body_tree853.body if isinstance(n, ast.For)
    and isinstance(n.target, ast.Tuple)
    and any(isinstance(x, ast.Name) and x.id == 'ji846' for x in n.target.elts)]
assert len(experiment853) == 1
experiment853 = experiment853[0]
cycle853 = [n for n in ast.walk(experiment853) if isinstance(n, ast.For)
    and isinstance(n.target, ast.Name) and n.target.id == 'cycle851']
assert len(cycle853) == 1
cycle853 = cycle853[0]

# All three arms now run the identical TEST852 NATIVE852 precontrol, including BASELINE852.
coverage_parent853 = [n for n in ast.walk(experiment853) if isinstance(getattr(n, 'body', None), list)
    and any(isinstance(x, ast.If) and any(assigned853(y, 'coverage_h852') for y in x.body)
        for x in n.body)]
assert len(coverage_parent853) == 1
replace_child853(coverage_parent853[0],
    lambda n: isinstance(n, ast.If) and any(assigned853(x, 'coverage_h852') for x in n.body),
    "coverage_h852 = coverage_state852(q851, condition851, mode851, mx851)",
    'COVERAGE_FOR_ALL_ARMS')

replace_child853(cycle853,
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
    'review_%d'%cycle851 if arm851 == 'BASELINE852' else 'precontrol_%d'%cycle851,
    tensors851, traces851)
interaction_rows853, routed_control853, routed_interaction853 = None, None, None
decision_segments853 = None
if arm851 == 'BASELINE852':
    review851 = precontrol851
else:
    interaction_rows853 = interaction853(C851, E851, precontrol851['rows'])
    routed_control853, routed_interaction853 = route853(
        arm851, precontrol851['rows'], interaction_rows853)
    assert routed_control853.shape == routed_interaction853.shape
    decision_segments853 = [(K_SLOT853, routed_control853),
        (J_SLOT853, routed_interaction853)]
    review851 = invoke851(mx851, pre851, decision_segments853, REVIEW_SUFFIX851,
        'review_%d'%cycle851, tensors851, traces851)
""",
    'NATIVE_DECISION_REENTRY')

# Extend the existing event record; no cognitive field is computed here.
event_assign853 = [n for n in cycle853.body if assigned853(n, 'event851')]
assert len(event_assign853) == 1 and isinstance(event_assign853[0].value, ast.Dict)
event_dict853 = event_assign853[0].value
dict_put853(event_dict853, 'precontrol', 'result849(precontrol851)')
dict_put853(event_dict853, 'interaction_state',
    'None if interaction_rows853 is None else stats849(interaction_rows853)')
dict_put853(event_dict853, 'routed_control_state',
    'None if routed_control853 is None else stats849(routed_control853)')
dict_put853(event_dict853, 'routed_interaction_state',
    'None if routed_interaction853 is None else stats849(routed_interaction853)')

# REVISE retains the TEST852 native feedback path and uses the current cycle's final K, U and R.
revise853 = [n for n in cycle853.body if isinstance(n, ast.If)
    and any(isinstance(x, ast.If) and "'revision_%d'" in ast.unparse(x) for x in n.body)]
# The action chain is an If nested in cycle body; locate its REVISE branch directly.
action_chain853 = next(n for n in cycle853.body if isinstance(n, ast.If)
    and isinstance(n.test, ast.Compare) and "'CONTINUE'" in ast.unparse(n.test))
revise_branch853 = next(n for n in ast.walk(action_chain853) if isinstance(n, ast.If)
    and "'REVISE'" in ast.unparse(n.test))
replace_child853(revise_branch853,
    lambda n: isinstance(n, ast.If) and "'revision_%d'" in ast.unparse(n),
    """current851 = invoke851(mx851, recompute_pre851,
    [(C_SLOT851, C851), (K_SLOT851, review851['rows']),
     (E_SLOT851, E851), (U_SLOT852, routed_u852),
     (R_SLOT852, routed_r852)], ANSWER_SUFFIX851,
    'revision_%d'%cycle851, tensors851, traces851)
""",
    'UNIFIED_NATIVE_REVISION')

# Add one compact bridge audit beside the inherited control-state report.
control_log853 = next(i for i, n in enumerate(cycle853.body)
    if expr_label853(n, 'TEST852 CONTROL STATE'))
cycle853.body[control_log853+1:control_log853+1] = nodes853("""
say_r41('TEST853 DECISION BRIDGE', q851, condition851, arm851,
    'CYCLE='+str(cycle851), json.dumps({
        'precontrol':event851['precontrol']['output'],
        'J':event851['interaction_state'],
        'routed_K0':event851['routed_control_state'],
        'routed_J':event851['routed_interaction_state']}))
""")

# Exact arm literals in BODY/OFF are computational identifiers, not historical prose.
body_arms853 = TEST853ArmLiterals(); body_arms853.counts = {k:0 for k in body_arms853.arm_map}
off_arms853 = TEST853ArmLiterals(); off_arms853.counts = {k:0 for k in off_arms853.arm_map}
body_tree853 = body_arms853.visit(body_tree853)
off_tree853 = off_arms853.visit(off_tree853)
body_tree853 = TEST853Labels().visit(body_tree853)
off_tree853 = TEST853Labels().visit(off_tree853)
ast.fix_missing_locations(body_tree853); ast.fix_missing_locations(off_tree853)

# Offline: verify identical canonical inputs and a strictly matched K0/J intervention.
off_loop853 = next(n for n in ast.walk(off_tree853) if isinstance(n, ast.For)
    and isinstance(n.target, ast.Name) and n.target.id == 'condition'
    and any(assigned853(x, 'baseline') for x in n.body))
score_assign853 = next(i for i, n in enumerate(off_loop853.body) if assigned853(n, 'score_change'))
old_swap_asserts853 = [n for n in off_loop853.body if isinstance(n, ast.Assert)
    and ('routed_coverage_state' in ast.unparse(n) or 'routed_relation_state' in ast.unparse(n))]
assert len(old_swap_asserts853) == 2
for old_assert853 in old_swap_asserts853:
    off_loop853.body.remove(old_assert853)
score_assign853 = next(i for i, n in enumerate(off_loop853.body) if assigned853(n, 'score_change'))
off_loop853.body[score_assign853+1:score_assign853+1] = nodes853("""
b0 = baseline['cycles'][0]
for matched_arm853 in ARMS851:
    matched_record853 = group[matched_arm853]
    matched_cycle853 = matched_record853['cycles'][0]
    assert matched_record853['initial']['output']['sha256'] == native['initial']['output']['sha256']
    assert matched_record853['evidence_native']['output']['sha256'] == native['evidence_native']['output']['sha256']
    assert matched_cycle853['candidate_intervened']['sha256'] == n0['candidate_intervened']['sha256']
    assert matched_cycle853['evidence_intervened']['sha256'] == n0['evidence_intervened']['sha256']
    assert matched_cycle853['coverage_native']['output']['sha256'] == n0['coverage_native']['output']['sha256']
    assert matched_cycle853['relation_state']['sha256'] == n0['relation_state']['sha256']
assert b0['review']['output']['sha256'] == n0['precontrol']['output']['sha256']
assert n0['precontrol']['output']['sha256'] == m0['precontrol']['output']['sha256']
assert n0['interaction_state']['sha256'] == m0['interaction_state']['sha256']
assert n0['precontrol']['output']['shape'] == n0['interaction_state']['shape']
assert n0['routed_control_state']['sha256'] == n0['precontrol']['output']['sha256']
assert n0['routed_interaction_state']['sha256'] == n0['interaction_state']['sha256']
assert m0['routed_control_state']['sha256'] == m0['interaction_state']['sha256']
assert m0['routed_interaction_state']['sha256'] == m0['precontrol']['output']['sha256']
assert n0['routed_control_state']['sha256'] == m0['routed_interaction_state']['sha256']
assert n0['routed_interaction_state']['sha256'] == m0['routed_control_state']['sha256']
native_norm853 = n0['routed_control_state']['norm']**2 + n0['routed_interaction_state']['norm']**2
matched_norm853 = m0['routed_control_state']['norm']**2 + m0['routed_interaction_state']['norm']**2
assert abs(native_norm853-matched_norm853) <= 1e-6*max(1.0,native_norm853)
""")

# Require actual K0/J events for native coupling; empty or missing records cannot pass vacuously.
verdict_assign853 = next(n for n in off_tree853.body if assigned853(n, 'verdicts851'))
verdict_index853 = off_tree853.body.index(verdict_assign853)
off_tree853.body[verdict_index853:verdict_index853] = nodes853("""
bridge_events853 = [e for r in records851 if r['arm'] == 'NATIVE853' for e in r['cycles']]
bridge_pass853 = bool(bridge_events853) and all(
    e.get('precontrol') is not None and e.get('interaction_state') is not None
    and e.get('routed_control_state') is not None and e.get('routed_interaction_state') is not None
    and e['precontrol']['output']['shape'] == e['interaction_state']['shape']
    for e in bridge_events853)
""")
verdict_dict853 = verdict_assign853.value
assert isinstance(verdict_dict853, ast.Dict)
dict_put853(verdict_dict853, 'NATIVE_CONTROL_COUPLING',
    "'PASS' if transfer_pass851 and bridge_pass853 else 'INCONCLUSIVE'")

# The strongest preliminary verdict additionally requires the bridge and a real decision change.
final_if853 = next(n for n in off_tree853.body if isinstance(n, ast.If)
    and any(assigned853(x, 'final_verdict851') for x in n.body))
for branch853 in ast.walk(final_if853):
    if isinstance(branch853, ast.If) and isinstance(branch853.test, ast.Call):
        call853 = branch853.test
        if (isinstance(call853.func, ast.Name) and call853.func.id == 'all'
                and 'stop_pass851' in ast.unparse(call853)):
            tuple_node853 = call853.args[0]
            assert isinstance(tuple_node853, ast.Tuple)
            tuple_node853.elts.append(ast.Name(id='bridge_pass853', ctx=ast.Load()))

# Replace only outdated engineering prose; the evaluation mathematics is unchanged.
replace_top853(off_tree853,
    lambda n: assigned853(n, 'next851'),
    """next851 = ('Judge only final model decisions against BASELINE852 and matched K0/J routing. '
    'State or score changes alone are not task success. Research request remains unimplemented; do not claim it.')""",
    'NEXT_ENGINEERING_STEP')
replace_top853(off_tree853,
    lambda n: assigned853(n, 'report851'),
    """report851 = ('TEST853 completed %d/12 jobs; %d matched groups; NATIVE853 wrong opportunities=%d; '
    'recurrent Kprev edges=%d; K0/J causal observations=%s; final decision changes=%s; verdict=%s. '
    'GPU results are established only by this executed run.') % (
        len(cases851),len(groups851),wrong_native852,recurrent_edges851,
        causal852,decision_causal852,final_verdict851)""",
    'FINAL_REPORT')

# Record the immediate parent lock as well as all inherited locks in the result artifact.
test_artifact853 = [n for n in off_tree853.body if isinstance(n, ast.Assign)
    and isinstance(n.targets[0], ast.Subscript) and isinstance(n.value, ast.Dict)
    and isinstance(n.targets[0].slice, ast.Constant) and n.targets[0].slice.value == 'test853']
assert len(test_artifact853) == 1
artifact_dict853 = test_artifact853[0].value
source_lock_node853 = next(v for k, v in zip(artifact_dict853.keys, artifact_dict853.values)
    if isinstance(k, ast.Constant) and k.value == 'source_locks')
assert isinstance(source_lock_node853, ast.Call) and isinstance(source_lock_node853.func, ast.Name)
assert source_lock_node853.func.id == 'dict'
lock_extra853 = [k.value for k in source_lock_node853.keywords if k.arg is None]
assert len(lock_extra853) == 1 and isinstance(lock_extra853[0], ast.Dict)
lock_extra853 = lock_extra853[0]
assert not any(isinstance(k, ast.Constant) and k.value == '852.py' for k in lock_extra853.keys)
lock_extra853.keys.append(ast.Constant('852.py'))
lock_extra853.values.append(ast.Constant(LOCK853))
verdict_artifact853 = [n for n in off_tree853.body if isinstance(n, ast.Assign)
    and isinstance(n.targets[0], ast.Subscript) and isinstance(n.value, ast.Dict)
    and isinstance(n.targets[0].slice, ast.Constant) and n.targets[0].slice.value == 'verdict841R']
assert len(verdict_artifact853) == 1
dict_put853(verdict_artifact853[0].value, 'reason',
    "'Pre-registered 12-job TEST853 K0/J gated decision re-entry panel.'")

body853 = ast.unparse(body_tree853) + '\n'
off853 = '\n' + ast.unparse(off_tree853) + '\n'
assert 'SUPPORT853' not in body853 and 'BIND853' not in body853
assert body853.count('def interaction853(') == 1
assert body853.count('def route853(') == 1
assert body853.count('def route852(') == 0
assert body853.count('for ji846, j846 in enumerate(JOBS841)') == 1
assert "'MODEL_NATIVE_RESEARCH_REQUEST': 'NOT_IMPLEMENTED_PROTOCOL_UNCHANGED'" in off853
for block853 in (body853, off853):
    ast.parse(block853)
    compile(block853, '<TEST853_EMBEDDED>', 'exec')

# Replace only the two locked literals in the TEST852 wrapper AST.
set_literal853(tree853, 'BODY851', body853)
set_literal853(tree853, 'OFF851', off853)

# Update only source852-producing assignments whose embedded panel code must create the three new arms.
source_assignments853 = [n for n in tree853.body if assigned853(n, 'source852')]
panel_arms853 = TEST853ArmLiterals(); panel_arms853.counts = {k:0 for k in panel_arms853.arm_map}
for assignment853 in source_assignments853:
    panel_arms853.visit(assignment853)
assert panel_arms853.counts['BASELINE851'] >= 3
assert panel_arms853.counts['NATIVE852'] >= 3
assert panel_arms853.counts['MATCHED_CONTROL852'] >= 3
# The nested 851 builder must assert the new residual-hook audit label, not the old TEST852 label.
nested_label853 = [n for n in source_assignments853 if isinstance(n.value, ast.Call)
    and isinstance(n.value.func, ast.Attribute) and n.value.func.attr == 'replace'
    and len(n.value.args) == 2
    and all(isinstance(a, ast.Constant) for a in n.value.args)
    and n.value.args[0].value == 'TEST851' and n.value.args[1].value == 'TEST852']
assert len(nested_label853) == 1
nested_label853[0].value.args[1].value = 'TEST853'

# Strengthen, rather than remove, the inherited static preflight for the modified embedded body.
replace_top853(tree853,
    lambda n: isinstance(n, ast.Assert) and 'function852' in ast.unparse(n)
        and 'set(' in ast.unparse(n) and 'coverage_state852' in ast.unparse(n),
    """assert set(('gen851','invoke851','shared851','intervened851','relation852',
    'interaction853','route853','coverage_state852')) <= set(function852)""",
    'FUNCTION_SET_PREFLIGHT')
replace_top853(tree853,
    lambda n: isinstance(n, ast.Assert) and "function852['route852']" in ast.unparse(n),
    "assert [a.arg for a in function852['route853'].args.args] == ['arm','K0','J']",
    'ROUTE_SIGNATURE_PREFLIGHT')
replace_top853(tree853,
    lambda n: isinstance(n, ast.Assert) and 'TEST852_NO_RESIDUAL_HOOKS_BEFORE_FINAL' in ast.unparse(n),
    "assert 'TEST853_NO_RESIDUAL_HOOKS_BEFORE_FINAL' in BODY851",
    'RESIDUAL_HOOK_LABEL_PREFLIGHT')
replace_top853(tree853,
    lambda n: isinstance(n, ast.Assert) and 'ARMS851 = ' in ast.unparse(n),
    """assert "ARMS851 = ('BASELINE852', 'NATIVE853', 'MATCHED_CONTROL853')" in BODY851""",
    'ARM_PREFLIGHT')
replace_top853(tree853,
    lambda n: isinstance(n, ast.Assert) and 'MODEL_NATIVE_RESEARCH_REQUEST' in ast.unparse(n),
    "assert \"'MODEL_NATIVE_RESEARCH_REQUEST': 'NOT_IMPLEMENTED_PROTOCOL_UNCHANGED'\" in OFF851",
    'RESEARCH_REQUEST_PREFLIGHT')
replace_top853(tree853,
    lambda n: isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
        and 'matched U/R slot-routing control' in ast.unparse(n),
    "print('PANEL: 12 jobs; 2 cycles maximum; matched K0/J decision re-entry control')",
    'PANEL_PREFLIGHT_LABEL')

# Additional preflight invariants: final readout cannot bypass K0/J through direct C/E/U/R slots.
final_decision853 = ast.parse(body853)
final_decision_text853 = ast.unparse(final_decision853)
assert 'decision_segments853 = [(K_SLOT853, routed_control853),' in final_decision_text853
assert '(C_SLOT851' not in final_decision_text853.split('decision_segments853 =',1)[1].split('action851 =',1)[0]
assert '(E_SLOT851' not in final_decision_text853.split('decision_segments853 =',1)[1].split('action851 =',1)[0]
assert '(U_SLOT852' not in final_decision_text853.split('decision_segments853 =',1)[1].split('action851 =',1)[0]
assert '(R_SLOT852' not in final_decision_text853.split('decision_segments853 =',1)[1].split('action851 =',1)[0]
assert 'out.last_hidden_state' not in body853 and 'output_hidden_states' not in body853
assert 'register_forward_hook' not in body853 and 'register_forward_pre_hook' not in body853
assert '.backward(' not in body853 and 'optimizer' not in body853.lower()
assert "j['initial_mode']" not in body853 + off853
assert "j851['initial_mode']" not in body853 + off853

source853 = ast.unparse(tree853) + '\n'
final_tree853 = ast.parse(source853)
compile(final_tree853, 'TEST853_LOCKED_BUILDER', 'exec')
print('TEST853 LOCKED ENGINE VERIFICATION')
print('PARENT GIT BLOB: PASS | TARGETED AST PATCHES: PASS | EMBEDDED COMPILE: PASS')
print('NO GENERAL SOURCE.REPLACE IN TEST853 | NO SUPPORT/BIND | K0/J BOTTLENECK: PRESENT')
print('PANEL: 12 jobs; 2 worlds x 2 conditions x 3 arms; matched K0/J routing')
print('BUILDER SHA256:', hashlib.sha256(source853.encode()).hexdigest())
print('GPU EXECUTION: NOT VERIFIED BY AUTHOR; only this Colab run can establish it', flush=True)
exec(compile(final_tree853, 'TEST853_LOCKED_BUILDER', 'exec'), globals())
