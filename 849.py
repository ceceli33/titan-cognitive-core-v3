# AKBASCORE TEST849 — one Colab cell; frozen TEST848 engine chain.
# 20 full jobs + 4 shared no-state review probes = 24 experimental units.
# GPU execution is not claimed by the code author.
import ast, hashlib, json, urllib.request, time, re
import torch
import numpy as np

BASE849 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
LOCKS849 = {
    '848.py': '3876661dca29f282b626eb81068b9c1a21797fe0',
    '847.py': '72ce35daa728f546d92baa26705dd04ed5ad6a11',
    '846.py': '6093896b7e4492f201cece448ad1646b0bd8820a',
    '845.py': 'be81a587b3d2b8cd3e9291df6bd9fb481c4c2164',
    '844.py': '783dbca9ebab722a0a5826aa708c4f152f8d7ad7',
    '841.py': '135b18e5b1ea113579c607cf9eecf49628cf18c2'
}
SOURCE849 = {}
print('TEST849 SOURCE VERIFICATION')
for file849, lock849 in LOCKS849.items():
    req849 = urllib.request.Request(
        BASE849 + file849,
        headers={'User-Agent': 'AKBASCORE-TEST849'}
    )
    with urllib.request.urlopen(req849, timeout=180) as response849:
        data849 = response849.read(1000001)
    digest849 = hashlib.sha1(
        b'blob ' + str(len(data849)).encode() + b'\0' + data849
    ).hexdigest()
    assert digest849 == lock849, (
        'SOURCE_LOCK_FAILED', file849, digest849, lock849
    )
    SOURCE849[file849] = data849.decode('utf-8')
    ast.parse(SOURCE849[file849])
    print(file849, digest849, 'PASS')


def literal849(source, name):
    nodes = [
        n for n in ast.parse(source).body
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)
        and isinstance(n.value, ast.Constant)
        and isinstance(n.value.value, str)
    ]
    assert len(nodes) == 1, ('LITERAL_NOT_UNIQUE', name, len(nodes))
    return nodes[0].value.value


def replace_literal849(source, name, value):
    nodes = [
        n for n in ast.parse(source).body
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)
        and isinstance(n.value, ast.Constant)
        and isinstance(n.value.value, str)
    ]
    assert len(nodes) == 1, ('PATCH_LITERAL_NOT_UNIQUE', name, len(nodes))
    node = nodes[0]
    lines = source.splitlines(keepends=True)
    lines[node.lineno-1:node.end_lineno] = [
        name + ' = ' + repr(value) + '\n'
    ]
    result = ''.join(lines)
    ast.parse(result)
    return result


def once849(source, old, new):
    assert source.count(old) == 1, (
        'PATCH_NOT_UNIQUE', old[:100], source.count(old)
    )
    return source.replace(old, new, 1)


# Preserve the exact legacy generator; make an observational clone.
engine849 = literal849(SOURCE849['845.py'], 'RUN845')
gen_node849 = [
    n for n in ast.parse(engine849).body
    if isinstance(n, ast.FunctionDef) and n.name == 'gen845'
]
assert len(gen_node849) == 1
GEN849 = ast.get_source_segment(engine849, gen_node849[0])
GEN849 = once849(GEN849, 'def gen845(', 'def gen849(')
GEN849 = once849(
    GEN849, '    parts = ', '    budget849()\n    parts = '
)
GEN849 = once849(
    GEN849,
    '    pos = torch.arange(n, n + L, device=DEV)',
    "    assert n + L + K845 <= MAX_FUSED_TOKENS, ('CONTEXT_LIMIT', n, L)\n"
    "    transfer849 = continuity849(rows, X, len(pre))\n"
    "    pos = torch.arange(n, n + L, device=DEV)"
)
GEN849 = once849(
    GEN849,
    "'kend': kend}",
    "'kend': kend, 'trace849': trace849(toks, info, rows, transfer849)}"
)
ast.parse(GEN849)

# Extract actual legacy frame/slot assignments; no guessed prompts.
legacy_run849 = literal849(SOURCE849['848.py'], 'RUN848')
frame_names849 = {
    'REVIEW_FRAME848', 'REVISE_FRAME848', 'REVIEW_PRE_SLOT848',
    'REVIEW_POST_SLOT848', 'REVISE_PRE_SLOT848'
}
frame_nodes849 = [
    n for n in ast.parse(legacy_run849).body
    if isinstance(n, ast.Assign)
    and any(
        isinstance(t, ast.Name) and t.id in frame_names849
        for t in n.targets
    )
]
assert len(frame_nodes849) == len(frame_names849)
FRAMES849 = '\n'.join(
    ast.get_source_segment(legacy_run849, n) for n in frame_nodes849
)

# Reuse TEST848 panel construction; change dimensions and arm names.
PANEL849 = literal849(SOURCE849['848.py'], 'PANEL_TAIL848')
# Preserve the parent's required legacy literal, then restrict explicitly.
PANEL849 = once849(
    PANEL849,
    'PILOT_WORLDS846 = (0, 1, 2)',
    'PILOT_WORLDS846 = (0, 1, 2)\n'
    'PILOT_WORLDS846 = PILOT_WORLDS846[:2]'
)
PANEL849 = once849(
    PANEL849,
    "PILOT_STARTS846 = ('INTACT', 'CONFLICT', 'REMOVED')",
    "PILOT_STARTS846 = ('INTACT', 'REMOVED')"
)
PANEL849 = once849(
    PANEL849,
    "PILOT_ARMS846 = (\n"
    "    'MODEL_STATE',\n"
    "    'ORDER_CONTROL',\n"
    "    'NO_STATE'\n"
    ")",
    "PILOT_ARMS846 = "
    "('LEGACY', 'BOUNDARY', 'CONTINUITY', 'ORDER_CONTROL', 'NO_STATE')"
)
PANEL849 = once849(
    PANEL849,
    'assert len(JOBS841) == 27',
    'assert len(JOBS841) == 20'
)
PANEL849 = once849(
    PANEL849,
    "assert len({j['job'] for j in JOBS841}) == 27",
    "assert len({j['job'] for j in JOBS841}) == 20"
)

HELP849 = r'''
UPPER_CHECK841 = {}
BUDGET_STOP841 = False
CALLS849 = 0
CALL_CAP849 = 1000
START_TIME849 = time.perf_counter()
t_run841 = START_TIME849

def budget849():
    global CALLS849
    if (time.perf_counter() - T0_841) / 60 > HARD_BUDGET_MIN841:
        raise BudgetR41('WALL_TIME_LIMIT')
    if CALLS849 >= CALL_CAP849:
        raise BudgetR41('TEST849_CALL_LIMIT')
    CALLS849 += 1

def stats849(rows):
    if rows is None:
        return {
            'shape': [0, H], 'dtype': None, 'device': None,
            'sha256': None, 'norm': 0.0
        }
    assert rows.ndim == 2 and rows.shape[1] == H
    assert rows.device.type == 'cpu' and rows.dtype == torch.float32
    assert torch.isfinite(rows).all().item()
    arr = rows.detach().contiguous().numpy()
    return {
        'shape': list(rows.shape),
        'dtype': str(rows.dtype),
        'device': str(rows.device),
        'sha256': hashlib.sha256(
            arr.tobytes() + str(arr.shape).encode()
        ).hexdigest(),
        'norm': float(torch.linalg.vector_norm(rows)),
        'row_norms': torch.linalg.vector_norm(rows, dim=1).tolist()
    }

def continuity849(rows, X, start):
    if rows is None or not rows.shape[0]:
        return {'status': 'NO_INSERTED_ROWS', 'exact_after_bf16': True}
    expected = rows.to(device=DEV, dtype=DTYPE)
    actual = X[start:start + rows.shape[0]]
    ok = torch.equal(expected, actual)
    assert ok, 'STATE_INSERTION_MISMATCH'
    a = actual.detach().float().cpu().reshape(-1)
    b = rows.reshape(-1)
    cosine = (
        float(torch.nn.functional.cosine_similarity(a, b, dim=0))
        if a.numel() else None
    )
    return {
        'status': 'CHECKED',
        'exact_after_bf16': ok,
        'runtime_dtype': str(actual.dtype),
        'runtime_device': str(actual.device),
        'max_cast_error': float((a-b).abs().max()),
        'cosine_after_cast': cosine
    }

def trace849(toks, info, rows, transfer):
    last = int(toks[-1])
    if last == int(tok.eos_token_id):
        reason = 'EOS'
    elif '\n' in tok.decode([last]):
        reason = 'NEWLINE_TOKEN'
    else:
        reason = 'TOKEN_BUDGET'
    clean = tok.decode([int(t) for t in toks if not end845(int(t))])
    return {
        'input': stats849(rows),
        'continuity': transfer,
        'all_token_ids': [int(t) for t in toks],
        'raw_decode': tok.decode(toks, skip_special_tokens=False),
        'termination': reason,
        'empty': not bool(clean.strip()),
        'empty_reason': (
            (reason if not clean else 'WHITESPACE_ONLY')
            if not clean.strip() else None
        ),
        'token_top20': info
    }

def result849(h):
    return {
        k: v for k, v in h.items() if k != 'rows'
    } | {'output': stats849(h['rows'])}

def parse849(text):
    value = str(text).strip().upper()
    return value if value in ('CONTINUE', 'REVISE', 'STOP') else 'INVALID'

# Score FIXED protocol strings only; no generated text replay.
# These teacher-forced scores do not control the soft-row rollout.
@torch.no_grad()
def action_scores849(memx, pre, rows, post):
    parts = [embed841(pre)]
    if rows is not None and len(rows):
        parts.append(rows.to(device=DEV, dtype=DTYPE))
    if post:
        parts.append(embed841(post))
    X = torch.cat(parts, dim=0)
    n, L = int(memx[0][0].shape[-2]), len(X)
    scores = []
    for spelling in (
        'CONTINUE', 'REVISE', 'STOP',
        ' CONTINUE', ' REVISE', ' STOP'
    ):
        budget849()
        ids = list(tok(spelling, add_special_tokens=False).input_ids)
        assert ids and tok.decode(ids) == spelling, (
            'ACTION_TOKENIZATION', spelling, ids
        )
        Y = (
            torch.cat([X, embed841(ids[:-1])], dim=0)
            if len(ids) > 1 else X
        )
        assert n + len(Y) <= MAX_FUSED_TOKENS
        cache = cache_build(list(memx))
        pos = torch.arange(n, n + len(Y), device=DEV)
        out = model(
            inputs_embeds=Y.reshape(1, len(Y), H),
            past_key_values=cache,
            attention_mask=torch.ones(
                (1, n + len(Y)), device=DEV, dtype=torch.long
            ),
            position_ids=pos.unsqueeze(0),
            cache_position=pos,
            use_cache=True,
            return_dict=True
        )
        logp = torch.log_softmax(
            out.logits[0, L-1:L-1+len(ids)].float(), dim=-1
        )
        score = float(
            logp[
                torch.arange(len(ids), device=DEV),
                torch.tensor(ids, device=DEV)
            ].sum()
        )
        scores.append({
            'spelling': spelling,
            'ids': ids,
            'sequence_logp': score,
            'meaning': (
                'teacher-forced hard-token prefix logp; diagnostic only, '
                'not soft-rollout action probability'
            )
        })
        del out, cache, logp
        COUNT834['probe_forwards'] += 1
    return scores
'''

BODY849 = r'''
ARMS849 = (
    'LEGACY', 'BOUNDARY', 'CONTINUITY', 'ORDER_CONTROL', 'NO_STATE'
)
assert len(JOBS841) == 20 and len(JOBS841) <= 30
assert set(j['arm'] for j in JOBS841) == set(ARMS849)
assert set(j['intervention'] for j in JOBS841) == {'INTACT', 'REMOVED'}
assert len(set(j['qid'] for j in JOBS841)) == 2
for q in dict.fromkeys(j['qid'] for j in JOBS841):
    for c in ('INTACT', 'REMOVED'):
        group = [
            j for j in JOBS841
            if j['qid'] == q and j['intervention'] == c
        ]
        assert len(group) == 5
        assert len({tuple(j['initial_cards']) for j in group}) == 1
        assert len({tuple(j['bank']) for j in group}) == 1

say_r41(
    'TEST849 HARDWARE AND MODEL',
    'Inherited A100-80GB / frozen Qwen2.5-72B NF4 gates'
)
say_r41(
    'TEST849 LOCKED ENGINE VERIFICATION',
    'Physical mounting and native model calls retained'
)
say_r41(
    'TEST849 RESEARCH HYPOTHESES',
    'BOUNDARY-LEGACY tests revision output boundary. '
    'CONTINUITY-BOUNDARY tests retained first state. '
    'CONTINUITY-ORDER_CONTROL tests row order; '
    'CONTINUITY-NO_STATE tests removal of all revision state. '
    'Only task-related paired improvements support the engineering '
    'hypothesis; differing vectors alone do not.'
)
say_r41(
    'TEST849 EXPERIMENTAL PANEL',
    '20 full jobs + 4 no-state review probes = 24 units; '
    'reused worlds 0,1; INTACT/REMOVED. No CONFLICT claim.'
)
say_r41(
    'TEST849 MODEL SIGNAL VS PYTHON ACTION',
    'Model emits action. Python applies it once; no search or retraction.'
)
SHARED849 = {}
GEN_EQ849 = False

for ji846, j846 in enumerate(JOBS841):
    if j846['job'] in REC841:
        say_r41('TEST849 JOB-BY-JOB RESULTS', 'RESUMED', j846['job'])
        continue
    started849 = time.perf_counter()
    torch.cuda.reset_peak_memory_stats()
    q849 = j846['qid']
    arm849 = j846['arm']
    cond849 = j846['intervention']
    mem849 = list(j846['initial_cards'])
    try:
        budget849()
        assert len(mem849) <= CAP845
        assert all(c in entries for c in mem849)
        key849 = (q849, cond849)
        mx849 = memx_r41(mem849)
        if key849 not in SHARED849:
            first_pre849 = (
                list(prompt_ids(
                    FR845['hop0'].format(q=QTEXT841[q849])
                )) + SLOT845[3]
            )
            with CallCount841() as counter849:
                first849 = gen849(mx849, first_pre849, None, None)
            upper849 = counter849.summary()
            gate829(
                'TEST849_UPPER_' + str(len(SHARED849)),
                upper849['upper_min'] >= 1 and upper849['lm_head'] >= 1,
                upper849
            )
            UPPER_CHECK841 = upper849
            review_pre849 = (
                list(prompt_ids(
                    REVIEW_FRAME848.format(q=QTEXT841[q849])
                )) + REVIEW_PRE_SLOT848
            )
            review849 = gen849(
                mx849, review_pre849,
                first849['rows'], REVIEW_POST_SLOT848
            )
            scores849 = action_scores849(
                mx849, review_pre849,
                first849['rows'], REVIEW_POST_SLOT848
            )
            review_none849 = gen849(
                mx849, review_pre849, None, REVIEW_POST_SLOT848
            )
            none_scores849 = action_scores849(
                mx849, review_pre849, None, REVIEW_POST_SLOT848
            )
            if not GEN_EQ849:
                reference849 = gen845(
                    mx849, review_pre849,
                    first849['rows'], REVIEW_POST_SLOT848
                )
                gate829(
                    'TEST849_OBSERVATIONAL_CLONE_EQUIVALENCE',
                    reference849['text'] == review849['text']
                    and reference849['toks'] == review849['toks']
                    and torch.equal(
                        reference849['rows'], review849['rows']
                    )
                )
                GEN_EQ849 = True
            SHARED849[key849] = (
                first849, review849, scores849,
                review_none849, none_scores849
            )

        (
            first849, review849, scores849,
            review_none849, none_scores849
        ) = SHARED849[key849]
        decision849 = parse849(review849['text'])
        revision849, final849, rin849, post849 = None, None, None, None
        order_degenerate849 = bool(torch.equal(
            first849['rows'], first849['rows'].flip(0)
        ))

        if decision849 == 'REVISE':
            rin849 = review849['rows']
            if arm849 != 'LEGACY':
                # Existing '\nNext node:' boundary; no entity/answer.
                post849 = SLOT845[2]
            if arm849 == 'CONTINUITY':
                rin849 = torch.cat(
                    [first849['rows'], review849['rows']], dim=0
                )
            elif arm849 == 'ORDER_CONTROL':
                reverse849 = first849['rows'].flip(0).contiguous()
                assert torch.equal(
                    reverse849.flip(0), first849['rows']
                )
                rin849 = torch.cat(
                    [reverse849, review849['rows']], dim=0
                )
            elif arm849 == 'NO_STATE':
                rin849 = None

            revision_pre849 = (
                list(prompt_ids(
                    REVISE_FRAME848.format(q=QTEXT841[q849])
                )) + REVISE_PRE_SLOT848
            )
            revision849 = gen849(
                mx849, revision_pre849, rin849, post849
            )
            next_rows849 = revision849['rows']
            applied849 = 'APPLY_MODEL_REVISE'

        elif decision849 == 'CONTINUE':
            next_rows849 = first849['rows']
            applied849 = 'APPLY_MODEL_CONTINUE'

        elif decision849 == 'STOP':
            applied849 = 'APPLY_MODEL_STOP'

        else:
            applied849 = 'PROTOCOL_INVALID_NO_FOLLOWUP'

        if decision849 in ('CONTINUE', 'REVISE'):
            next_pre849 = (
                list(prompt_ids(
                    FR845['hop'].format(q=QTEXT841[q849])
                )) + SLOT845[1]
            )
            final849 = gen849(
                mx849, next_pre849, next_rows849, SLOT845[2]
            )

        rec849 = {
            'job': j846['job'],
            'qid': q849,
            'arm': arm849,
            'condition': cond849,
            'mounted_cards': mem849,
            'mounted_count': len(mem849),
            'first': result849(first849),
            'review': result849(review849),
            'review_action': decision849,
            'action_scores': scores849,
            'review_no_state': result849(review_none849),
            'no_state_action_scores': none_scores849,
            'review_prompt_sha256': hashlib.sha256(
                REVIEW_FRAME848.encode()
            ).hexdigest(),
            'review_prefix_ids': REVIEW_PRE_SLOT848,
            'review_suffix_ids': REVIEW_POST_SLOT848,
            'revision_input': stats849(rin849),
            'revision_suffix_ids': post849,
            'revision': (
                None if revision849 is None else result849(revision849)
            ),
            'final': None if final849 is None else result849(final849),
            'order_control_degenerate': order_degenerate849,
            'python_action': applied849,
            'mechanical_stop_reason': None,
            'seconds': time.perf_counter()-started849,
            'peak_gpu_gib': torch.cuda.max_memory_allocated()/2**30
        }
        arrays849 = {
            'first_rows': first849['rows'].numpy(),
            'review_rows': review849['rows'].numpy(),
            'review_no_state_rows': review_none849['rows'].numpy(),
            'revision_input': (
                np.empty((0,H), np.float32)
                if rin849 is None else rin849.numpy()
            ),
            'revision_rows': (
                np.empty((0,H), np.float32)
                if revision849 is None else revision849['rows'].numpy()
            ),
            'final_rows': (
                np.empty((0,H), np.float32)
                if final849 is None else final849['rows'].numpy()
            )
        }
        json.dumps(rec849, allow_nan=False)
        save_job841(j846['job'], rec849, arrays849)
        REC841[j846['job']] = rec849
        ROWS841[j846['job']] = arrays849

        say_r41(
            'TEST849 JOB-BY-JOB RESULTS',
            j846['job'], q849, cond849, arm849,
            'FIRST='+repr(first849['text']),
            'ACTION='+decision849,
            'REV='+repr(
                None if revision849 is None else revision849['text']
            ),
            'FINAL='+repr(
                None if final849 is None else final849['text']
            ),
            'SECONDS=%.2f PEAK_GIB=%.2f' % (
                rec849['seconds'], rec849['peak_gpu_gib']
            )
        )
        for stage849, h849 in (
            ('first',first849), ('review',review849),
            ('revision',revision849), ('final',final849)
        ):
            if h849 is not None:
                tr849 = h849['trace849']
                say_r41(
                    'TEST849 NUMERICAL STATE CONTINUITY',
                    stage849,
                    json.dumps({
                        'input': tr849['input'],
                        'output': stats849(h849['rows']),
                        'transfer': tr849['continuity']
                    }, ensure_ascii=False)
                )
                say_r41(
                    'TEST849 TOKEN AND LOGIT DIAGNOSTICS',
                    stage849,
                    'TOKENS='+str(tr849['all_token_ids']),
                    'RAW='+repr(tr849['raw_decode']),
                    'END='+tr849['termination'],
                    'EMPTY_REASON='+str(tr849['empty_reason'])
                )
        say_r41(
            'TEST849 REVIEW ACTION DIAGNOSTICS',
            'NATIVE', json.dumps(scores849),
            'NO_STATE', json.dumps(none_scores849),
            'NO_STATE_TEXT='+repr(review_none849['text'])
        )
        say_r41(
            'TEST849 REVISION TRANSFER DIAGNOSTICS',
            arm849,
            'INPUT='+json.dumps(stats849(rin849)),
            'SUFFIX='+str(post849),
            'DEGENERATE_REVERSE='+str(order_degenerate849)
        )
    except BudgetR41 as error849:
        BUDGET_STOP841 = True
        D829['mechanical_stop849'] = str(error849)
        say_r41('TEST849 MECHANICAL STOP', str(error849))
        break

    log829(
        'TEST849_PROGRESS', ji846+1, '/',
        len(JOBS841), arm849, cond849
    )

while LRU_R41:
    evict_r41()
D829['run_seconds841'] = round(time.perf_counter()-t_run841, 3)
D829['memo841R'] = dict(
    CNT_R41,
    states=len(SIG_R41),
    echo_states=len(ECHO_R41),
    hop=CNT845['hop'],
    hop_hit=CNT845['hop_hit']
)
'''
RUN849 = HELP849 + '\n' + GEN849 + '\n' + FRAMES849 + '\n' + BODY849

OFF849 = r'''
log829('TEST846P_OFFLINE_START')
log829('TEST849_OFFLINE_START')

def node849(text, world):
    value = str(text or '').strip().upper().rstrip('.').strip()
    keys = ('middle','end','changed_end','fork_end','decoy_end')
    hits = [
        k for k in keys
        if world.get(k) and value == str(world[k]).strip().upper()
    ]
    return (
        hits[0] if len(hits) == 1
        else ('AMBIGUOUS' if hits else 'OTHER')
    )

cases849 = []
for j in JOBS841:
    if j['job'] not in REC841:
        continue
    r = REC841[j['job']]
    wi = QID841.index(r['qid'])
    w, ids = worlds829[wi], worlds829[wi]['ids']
    mounted = set(r['mounted_cards'])
    first = node849(r['first']['text'], w)
    revision = (
        node849(r['revision']['text'], w) if r['revision'] else None
    )
    final = node849(r['final']['text'], w) if r['final'] else None
    correct = final in ('end','changed_end')
    supporting = (
        ids['second'] if final == 'end'
        else ids['changed'] if final == 'changed_end' else None
    )
    grounded = bool(
        correct and ids['first'] in mounted and supporting in mounted
    )
    # UNKNOWN/empty/unparseable is not a confirmed wrong node.
    wrong = first in ('end','changed_end','fork_end','decoy_end')
    sufficient = (
        ids['first'] in mounted
        and bool({ids['second'],ids['changed']} & mounted)
    )
    answer = '' if r['final'] is None else r['final']['text'].strip()
    row = {
        'job': j['job'],
        'world': wi,
        'condition': r['condition'],
        'arm': r['arm'],
        'first_class': first,
        'revision_class': revision,
        'final_class': final,
        'wrong_first': wrong,
        'evidence_sufficient': sufficient,
        'grounded': grounded,
        'review_action': r['review_action'],
        'correction': bool(
            wrong and r['review_action']=='REVISE'
            and revision=='middle' and grounded
        ),
        'correct_stop': bool(
            not sufficient and r['review_action']=='STOP'
        ),
        'false_stop': bool(
            sufficient and r['review_action']=='STOP'
        ),
        'unsupported_completion': bool(
            not sufficient and answer
            and not answer.upper().startswith('UNKNOWN')
            and not grounded
        ),
        'revision_empty': bool(
            r['revision'] and r['revision']['trace849']['empty']
        ),
        'order_control_degenerate': r['order_control_degenerate']
    }
    cases849.append(row)
    say_r41('TEST849 JOB-BY-JOB EVALUATION', json.dumps(row))

review_pairs849 = []
pairs849 = []
for wi in (0,1):
    for condition in ('INTACT','REMOVED'):
        byarm = {
            r['arm']:r for r in cases849
            if r['world']==wi and r['condition']==condition
        }
        if set(byarm) != set(ARMS849):
            continue
        records = {a:REC841[byarm[a]['job']] for a in ARMS849}
        reference = records['LEGACY']
        native_review = reference['review']
        none_review = reference['review_no_state']
        shifts = [
            a['sequence_logp']-b['sequence_logp']
            for a,b in zip(
                reference['action_scores'],
                reference['no_state_action_scores']
            )
        ]
        review_pairs849.append({
            'world':wi,
            'condition':condition,
            'native_text':native_review['text'],
            'no_state_text':none_review['text'],
            'native_action':parse849(native_review['text']),
            'no_state_action':parse849(none_review['text']),
            'sequence_logp_deltas':shifts,
            'max_abs_sequence_logp_delta':max(map(abs,shifts)),
            'text_changed':native_review['text']!=none_review['text']
        })
        contrasts = []
        for left, right in (
            ('BOUNDARY','LEGACY'),
            ('CONTINUITY','BOUNDARY'),
            ('CONTINUITY','ORDER_CONTROL'),
            ('CONTINUITY','NO_STATE')
        ):
            x, y = records[left], records[right]
            texts = lambda r: [
                None if r[k] is None else r[k]['text']
                for k in ('revision','final')
            ]
            contrasts.append({
                'left':left,
                'right':right,
                'text_changed':texts(x)!=texts(y),
                'grounded_delta':(
                    int(byarm[left]['grounded'])
                    - int(byarm[right]['grounded'])
                ),
                'correction_delta':(
                    int(byarm[left]['correction'])
                    - int(byarm[right]['correction'])
                ),
                'valid_order_control':(
                    not x['order_control_degenerate']
                    if right=='ORDER_CONTROL' else True
                )
            })
        pairs849.append({
            'world':wi, 'condition':condition, 'contrasts':contrasts
        })

summary849 = {}
for arm in ARMS849:
    rows = [r for r in cases849 if r['arm']==arm]
    summary849[arm] = {
        k:sum(bool(r[k]) for r in rows)
        for k in (
            'wrong_first','grounded','correction','correct_stop',
            'false_stop','unsupported_completion','revision_empty'
        )
    }
    summary849[arm]['total'] = len(rows)

complete849 = (
    len(cases849)==20 and len(pairs849)==4 and not BUDGET_STOP841
)
checks849 = D829.get('checks',[])
physical849 = bool(checks849) and all(c['pass'] for c in checks849)
continuity_ok849 = all(
    s['trace849']['continuity']['exact_after_bf16']
    for j in JOBS841 if j['job'] in REC841
    for s in (
        REC841[j['job']].get(k)
        for k in ('first','review','revision','final')
    )
    if s is not None
)
interventions849 = [
    c for p in pairs849 for c in p['contrasts']
    if c['left']=='CONTINUITY' and c['valid_order_control']
]
effect849 = any(c['text_changed'] for c in interventions849)
useful849 = complete849 and all(
    summary849['CONTINUITY']['grounded'] > summary849[a]['grounded']
    for a in ('BOUNDARY','ORDER_CONTROL','NO_STATE')
)
opportunities849 = sum(r['wrong_first'] for r in cases849)
evidence_pairs849 = []
for wi in (0,1):
    pair = {
        r['condition']:r for r in cases849
        if r['world']==wi and r['arm']=='CONTINUITY'
    }
    if set(pair)=={'INTACT','REMOVED'}:
        removed_record = REC841[pair['REMOVED']['job']]
        final_text = (
            '' if removed_record['final'] is None
            else removed_record['final']['text'].strip().upper()
        )
        evidence_pairs849.append({
            'world':wi,
            'intact_grounded':pair['INTACT']['grounded'],
            'removed_stop':pair['REMOVED']['correct_stop'],
            'removed_unknown':final_text.startswith('UNKNOWN'),
            'paired_evidence_response':bool(
                pair['INTACT']['grounded']
                and (
                    pair['REMOVED']['correct_stop']
                    or final_text.startswith('UNKNOWN')
                )
            )
        })
stop_signal849 = (
    summary849['CONTINUITY']['correct_stop'] > 0
    and summary849['CONTINUITY']['false_stop'] == 0
    and any(
        r['arm']=='CONTINUITY' and r['evidence_sufficient']
        and r['review_action'] in ('CONTINUE','REVISE')
        for r in cases849
    )
)
verdict849 = (
    'INCOMPLETE_PANEL' if not complete849
    else 'PRELIMINARY_TASK_RELEVANT_CONTINUITY_SIGNAL' if useful849
    else 'OUTPUT_EFFECT_WITHOUT_CONFIRMED_TASK_GAIN' if effect849
    else 'NO_OBSERVED_BEHAVIORAL_CONTINUITY_EFFECT'
)
verdicts849 = {
    'SOURCE_INTEGRITY':'PASS',
    'PHYSICAL_MEMORY_INTEGRITY':'PASS' if physical849 else 'FAIL',
    'NATIVE_BYPASS_INTEGRITY':(
        'PASS'
        if D829.get('bypass_verification841') and physical849
        else 'INCONCLUSIVE'
    ),
    'NUMERICAL_STATE_CONTINUITY':(
        'PASS' if complete849 and continuity_ok849 else 'INCONCLUSIVE'
    ),
    'STATE_INTERVENTION_EFFECT':verdict849,
    'REVIEW_PROTOCOL_DISCRIMINATION':(
        'PRELIMINARY_STATE_SENSITIVITY'
        if any(p['text_changed'] for p in review_pairs849)
        else 'NO_OBSERVED_ACTION_TEXT_DISCRIMINATION'
    ),
    'REVISION_STATE_TRANSFER':(
        'PASS'
        if complete849 and continuity_ok849 and any(
            REC841[j['job']].get('revision') is not None
            for j in JOBS841 if j['job'] in REC841
        )
        else 'INCONCLUSIVE'
    ),
    'EVIDENCE_SENSITIVITY':(
        'PRELIMINARY_PAIRED_SIGNAL'
        if len(evidence_pairs849)==2 and all(
            p['paired_evidence_response'] for p in evidence_pairs849
        )
        else 'NOT_DEMONSTRATED'
    ),
    'MODEL_NATIVE_ERROR_SIGNAL':'NOT_DEMONSTRATED',
    'MODEL_NATIVE_CORRECTION':(
        'NOT_EVALUABLE_NO_WRONG_FIRST_NODE' if not opportunities849
        else 'PRELIMINARY_OBSERVATION'
        if any(r['correction'] for r in cases849)
        else 'NOT_OBSERVED'
    ),
    'MODEL_NATIVE_STOP':(
        'PRELIMINARY_PAIRED_OBSERVATION'
        if complete849 and stop_signal849 else 'NOT_DEMONSTRATED'
    ),
    'AUTONOMOUS_RECURSIVE_REASONING':'NOT_DEMONSTRATED'
}
say_r41(
    'TEST849 PHYSICAL MEMORY INTEGRITY',
    str(physical849), 'CHECKS='+str(len(checks849))
)
say_r41('TEST849 CAUSAL COMPARISON', json.dumps(summary849))
say_r41('TEST849 EVIDENCE SENSITIVITY', json.dumps(evidence_pairs849))
for review_pair in review_pairs849:
    say_r41('TEST849 REVIEW ACTION DIAGNOSTICS', json.dumps(review_pair))
for pair in pairs849:
    say_r41('TEST849 CAUSAL COMPARISON', json.dumps(pair))
say_r41(
    'TEST849 FAILURE ANALYSIS',
    'Empty output is classified by actual terminating token. '
    'EOS/newline explains the immediate stop, not why the model preferred '
    'that token. Four auxiliary probes test review-state removal, '
    'not a new prompt. NO_STATE changes context length. Reversal may be '
    'degenerate or out of distribution. No wrong initial node means no '
    'correction opportunity; fixed mounted cards do not test autonomous retention.'
)
next849 = (
    'Inspect retained first-state contribution with held-out paired evidence '
    'after confirming this pilot.'
    if useful849
    else 'Use recorded terminal tokens and sequence scores to locate remaining '
         'boundary/state failure; do not force actions.'
)
say_r41('TEST849 NEXT MECHANISM', next849)
report849 = (
    'TEST849: %d/20 full jobs plus up to four shared review-removal probes; '
    'two reused worlds; no generalization test. Physical checks: %d, failures: %d. '
    'Grounded LEGACY/BOUNDARY/CONTINUITY/ORDER_CONTROL/NO_STATE: %s. '
    'Confirmed wrong-first opportunities across jobs: %d. Verdict: %s. '
    'BOUNDARY versus LEGACY changes only the revision output suffix. '
    'CONTINUITY versus BOUNDARY adds the original numerical first state '
    'to the revision input; ORDER_CONTROL reverses only that state. '
    'NO_STATE removes all revision rows. Review prompt is unchanged; '
    'four additional probes remove its numerical state. '
    'Generated actions are applied literally; no oracle routing or answer '
    'correction is performed by Python. A successful output boundary alone '
    'is not a numerical-state contribution. Error recognition, autonomous '
    'evidence choice and open-ended recursion remain unproven. Next: %s'
    % (
        len(cases849),
        len(checks849),
        sum(not c['pass'] for c in checks849),
        [summary849[a]['grounded'] for a in ARMS849],
        opportunities849,
        verdict849,
        next849
    )
)
say_r41('TEST849 FINAL SCIENTIFIC VERDICT', json.dumps(verdicts849))
say_r41('TEST849 SCIENTIFIC REPORT', report849)
D829['test849'] = {
    'status':'COMPLETE' if complete849 else 'INCOMPLETE',
    'cases':cases849,
    'paired':pairs849,
    'review_pairs':review_pairs849,
    'evidence_pairs':evidence_pairs849,
    'source_locks':LOCKS849,
    'summary':summary849,
    'verdicts':verdicts849,
    'report':report849,
    'budget_checkpoints':CALLS849,
    'next_mechanism':next849
}
D829['verdict841R'] = {
    'decision':verdict849,
    'verdicts':verdicts849,
    'budget_stop':BUDGET_STOP841,
    'reason':'Pre-registered paired contrasts; no automatic autonomy PASS.'
}
D829['cost841R'] = {
    'counted':dict(COUNT834),
    'run_seconds':D829['run_seconds841'],
    'peak_gpu_gib':max([
        REC841[j['job']]['peak_gpu_gib']
        for j in JOBS841 if j['job'] in REC841
    ] or [0.0])
}
D829['status'] = (
    'COMPLETE_TEST849' if complete849 else 'PARTIAL_TEST849'
)
json.dumps(D829, ensure_ascii=False, default=str, allow_nan=False)
save829()
log829('TEST849_COMPLETED', str(OUT829))
'''

# Validate all embedded blocks BEFORE constructing/loading the engine.
for block849 in (PANEL849, RUN849, OFF849):
    ast.parse(block849)
    assert "'''" not in block849
names849 = {
    n.id for n in ast.walk(ast.parse(RUN849)) if isinstance(n, ast.Name)
}
assert not names849 & {
    'EVALKEY841', 'CONTENT841', 'worlds829', 'card_meta829'
}
loops849 = [
    n for n in ast.walk(ast.parse(RUN849))
    if isinstance(n, ast.For)
    and isinstance(n.iter, ast.Call)
    and isinstance(n.iter.func, ast.Name)
    and n.iter.func.id == 'enumerate'
    and len(n.iter.args) == 1
    and isinstance(n.iter.args[0], ast.Name)
    and n.iter.args[0].id == 'JOBS841'
]
assert len(loops849) == 1
assert RUN849.count('for ji846, j846 in enumerate(JOBS841)') == 1

patched849 = replace_literal849(
    SOURCE849['848.py'], 'PANEL_TAIL848', PANEL849
)
patched849 = replace_literal849(patched849, 'RUN848', RUN849)
patched849 = replace_literal849(patched849, 'OFF848', OFF849)
patched849 = once849(
    patched849,
    "assert 'assert len(JOBS841) == 27' in panel_text848",
    "assert 'assert len(JOBS841) == 20' in panel_text848"
)

# Materialize the SAME driver chain before its model-loading execution.
# Only direct top-level display prints are suppressed.
# Source locks, assertions and inherited safety gates remain.
TAILS849 = []


def materialize849(source, expected):
    tree = ast.parse(source)
    matches = []
    for index, node in enumerate(tree.body):
        if not isinstance(node, ast.Expr):
            continue
        if not isinstance(node.value, ast.Call):
            continue
        call = node.value
        if (
            not isinstance(call.func, ast.Name)
            or call.func.id != 'exec'
            or not call.args
        ):
            continue
        inner = call.args[0]
        if (
            isinstance(inner, ast.Call)
            and isinstance(inner.func, ast.Name)
            and inner.func.id == 'compile'
            and inner.args
            and isinstance(inner.args[0], ast.Name)
            and inner.args[0].id == expected
        ):
            matches.append(index)
    assert len(matches) == 1, (
        'DRIVER_EXEC_NOT_UNIQUE', expected, matches
    )
    index = matches[0]
    if tree.body[index+1:]:
        TAILS849.append(ast.unparse(ast.Module(
            body=tree.body[index+1:], type_ignores=[]
        )))
    tree.body = [
        n for n in tree.body[:index]
        if not (
            isinstance(n, ast.Expr)
            and isinstance(n.value, ast.Call)
            and isinstance(n.value.func, ast.Name)
            and n.value.func.id == 'print'
        )
    ]
    ast.fix_missing_locations(tree)
    exec(
        compile(tree, 'TEST849_BUILD_'+expected, 'exec'),
        globals()
    )
    result = globals()[expected]
    ast.parse(result)
    return result


for expected849 in ('SRC848', 'SRC847', 'D846', 'D845', 'S41R'):
    patched849 = materialize849(patched849, expected849)

# Change display identity after inherited exact patches have completed.
patched849 = patched849.replace('TEST848', 'TEST849')
finaltree849 = ast.parse(patched849)

# Correct the obsolete 444-job display without touching any safety gate.
for node in finaltree849.body:
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
        call = node.value
        if (
            isinstance(call.func, ast.Name)
            and call.func.id == 'say841'
            and call.args
        ):
            if 'Kapsam:' in ast.unparse(call.args[0]):
                call.args = [ast.Constant(
                    'Kapsam: TEST849; 2 previously used worlds '
                    'x 2 conditions x 5 arms = 20 jobs.'
                )]
ast.fix_missing_locations(finaltree849)

finalbody849 = literal849(ast.unparse(finaltree849), 'BODY841')
ast.parse(finalbody849)
marker849 = '# ====== OFFLINE' + ' PHASE MARKER ======'
assert finalbody849.count(marker849) == 1
pre_names849 = {
    n.id
    for n in ast.walk(ast.parse(finalbody849.split(marker849)[0]))
    if isinstance(n, ast.Name)
}
assert not pre_names849 & {
    'EVALKEY841', 'CONTENT841', 'worlds829',
    'card_meta829', 'NAMES841', 'BLOCKOF841'
}
print('TEST849 LOCKED ENGINE VERIFICATION')
print('SOURCE AST: PASS | EMBEDDED AST: PASS | ONE EXPERIMENT LOOP: PASS')
print(
    'PANEL: 20 full jobs + 4 shared review probes (24 units) | '
    'LEGACY / BOUNDARY / CONTINUITY / ORDER_CONTROL / NO_STATE'
)
print('RUN SHA256:', hashlib.sha256(RUN849.encode()).hexdigest())
print(
    'GPU EXECUTION: NOT VERIFIED BY AUTHOR; determined by this run',
    flush=True
)
exec(compile(finaltree849, 'TEST849_CELL', 'exec'), globals())

for tail849 in reversed(TAILS849):
    exec(
        compile(
            tail849.replace('TEST848', 'TEST849'),
            'TEST849_ARTIFACTS',
            'exec'
        ),
        globals()
    )
