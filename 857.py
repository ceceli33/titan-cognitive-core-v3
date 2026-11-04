# AKBASCORE SILICON HIPPOCAMPUS — TEST857 NATIVE DECISION-TRACE CAUSAL SCREEN
# Two original BASELINE853 jobs + post-hoc, non-feedback diagnostic replays.
# This is NOT a new control motor and NOT a completed 12-job TEST855/856 panel.
# The 856 hook-free repair is preserved: no output_hidden_states request, no
# forward hooks, no hook clearing, and observation uses existing public logits.
# Original actions and MAX_REVIEWS851=2 remain unchanged. Only after both jobs
# are saved and the explicit diagnostic-stop is raised do matched replay probes
# run. Probe text/scores never re-enter the original action or revision stream.
# MECHANICAL_REVIEW_LIMIT and diagnostic-stop are never called MODEL_STOP.
# Model training, weight edits, RAG, text replay, oracle routing and Python-side
# semantic decisions are absent. GPU execution is not claimed by the author.
import ast
import builtins
import contextlib
import copy
import hashlib
import io
import json
import pathlib
import sys
import time
import traceback
import urllib.request
import zipfile

TEST857_KIND = 'HOOKFREE_TWO_JOB_TRACE_AND_POSTHOC_CAUSAL_REPLAY_NOT_NEW_ENGINE'
BASE857 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
CODELOAD857 = 'https://codeload.github.com/ceceli33/titan-cognitive-core-v3/zip/refs/heads/main'
LOCKS857 = {
    '849.py': '01a6ac43cbc954cc2f6ceaf8cf0238333ec762b1',
    '850.py': '79cc5ab211c01b37324e2d6897a298e84db42101',
    '851.py': '0f01e73b9ad160c988cfe059e8b5ae5e1f35f65b',
    '852.py': '4174e9241f773d6a031c51296b6beb11d4637aa5',
    '853.py': 'a7033caa10fdb86f8f0ee0b8ed1a0ac7514e26be',
    '854.py': 'a158d92a61c15a5e71468146d6c1ceeaedce436c',
    '850.log': 'c070ef432e95f80cd9a1c28318fd2e4a10377296',
    '851.log': 'b38419ef3a069ea4e20d43d15e6d939318083a9a',
    '852.log': 'b434a1e36b22fd99f9590c8b98b8094e927db458',
    '853.log': '0bfa9104337c44adaf4a07ec0ce6b5e41f457494',
    '854.log': '2aa1f85e14d52acbd1ecbad5b5c7df10df0bbcd4',
}
PRE857_DIR = pathlib.Path('/content/PRE855_XRAY_20261104T062801Z')
PRE857_ERROR = PRE857_DIR / 'error.txt'
STAMP857 = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
ROOT857 = pathlib.Path('/content') / ('TEST857_DECISION_CAUSAL_' + STAMP857)
ROOT857.mkdir(parents=True, exist_ok=False)
CONSOLE857 = sys.stdout
ERROR_CONSOLE857 = sys.stderr
LOG_FILE857 = open(ROOT857 / '857.log', 'w', encoding='utf-8')
START857 = time.perf_counter()
REAL_COMPILE857 = builtins.compile
RAW_SOURCES857 = {}
STATE857 = {
    'installed': False,
    'compiled': False,
    'equalities': [],
    'probes': [],
    'observations': [],
    'coverage': [],
    'arrays': {},
    'frames': [],
    'g': None,
    'active': None,
    'capture': None,
    'tokenizations': {},
    'hook_audits': [],
    'saved_jobs': [],
    'invocations': [],
    'causal_probes': [],
    'probe_files': [],
    'original_record_sha256': None,
    'original_trace_sha256': None,
    'environment': {},
    'start': START857,
}
FAILURES857 = []
EXECUTION_ERROR857 = None
OUTER_EXECUTION_ERROR857 = None
TRACEBACK857 = ''
ERROR_EVIDENCE857 = {}
LAST_CONTEXT857 = None
DIAGNOSTIC_STOP857 = None
TWO_JOB_VERIFICATION857 = {}
CAUSAL_VERIFICATION857 = {}
PROBE_ERROR857 = None
PROVENANCE857 = {
    '855.py_sha256': '2b5e0f58a62bb91938cb690438d60d588a37e979e2ac84e4a6a9c0f2511c1271',
    '855.log_sha256': 'e30f02684bcda5876ebb4d383716d623b138b9e65a60eaabc8b9f8b4e41b30a7',
    '856.py_sha256': '5573163a96b673e62af58dc86edd561d6b75aeab9ed8e76f688e4e32beb02965',
    '856.log_sha256': '5ad8417d12a563a5d31f9eab09ac6bbc1e664f71e27664d82cb0b43580c1ec44',
    '856_reported_gate1_gate2': 'BLOCKED_BY_NON_COMPLETING_JOB_ASSERTION',
    '856_original_outcome_not_rewritten': True,
    '857_technical_gate_scientific_end_requirement': False,
}
RECOVERY_MODE857 = 'NOT_STARTED'


class Gate1SmokeComplete857(Exception):
    """Explicit diagnostic control flow after two saved jobs; never model STOP."""


def short857(*args):
    text = ' '.join(str(x) for x in args)
    print(text, file=CONSOLE857, flush=True)
    LOG_FILE857.write(text + '\n')
    LOG_FILE857.flush()


def json_write857(name, value):
    path = ROOT857 / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
        allow_nan=False), encoding='utf-8')
    return path


def jsonl_append857(name, value):
    with open(ROOT857 / name, 'a', encoding='utf-8') as handle:
        handle.write(json.dumps(value, ensure_ascii=False, allow_nan=False) + '\n')


def sha256_bytes857(data):
    return hashlib.sha256(data).hexdigest()


def git_blob857(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def load_sources857():
    # One archive fetch avoids treating transient raw-host resets as missing sources.
    request = urllib.request.Request(CODELOAD857,
        headers={'User-Agent': 'AKBASCORE-TEST857-GATE1'})
    with urllib.request.urlopen(request, timeout=240) as response:
        archive = response.read(100000001)
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        for name, expected in LOCKS857.items():
            matches = [member for member in zipped.namelist()
                if member.endswith('/' + name)]
            assert len(matches) == 1, ('SOURCE_MEMBER_NOT_UNIQUE', name, matches)
            data = zipped.read(matches[0])
            actual = git_blob857(data)
            assert actual == expected, ('SOURCE_LOCK_FAILED', name, actual, expected)
            RAW_SOURCES857[name] = data
            (ROOT857 / name).write_bytes(data)
            if name.endswith('.py'):
                REAL_COMPILE857(data.decode('utf-8'), name, 'exec')
            short857('GATE0 SOURCE', name, actual, 'PASS')
    assert len(RAW_SOURCES857) == 11


def capture_cell_source857():
    # Colab exposes the submitted cell through input history. If unavailable, do
    # not invent an 857.py artifact; the delivered .py file remains the source.
    try:
        shell = get_ipython()  # noqa: F821 — supplied by Colab/IPython.
        history = list(shell.history_manager.input_hist_raw)
        candidates = [text for text in history if
            'AKBASCORE SILICON HIPPOCAMPUS — TEST857 NATIVE DECISION-TRACE CAUSAL SCREEN' in text]
        if candidates:
            (ROOT857 / '857.py').write_text(candidates[-1], encoding='utf-8')
            return True
    except Exception as exc:
        short857('857.py history capture unavailable:', type(exc).__name__, str(exc))
    return False


def current_job857(g):
    if not g:
        return {}
    job = g.get('j851') or g.get('j846') or {}
    return {
        'job': job.get('job'),
        'qid': g.get('q851', job.get('qid')),
        'condition': g.get('condition851', job.get('intervention')),
        'arm': g.get('arm851', job.get('arm')),
    }


def segment_metadata857(g, segments):
    rows_out = []
    for slot, rows in list(segments or []):
        item = {
            'slot_ids': list(slot or []),
            'slot_text': None,
            'shape': list(rows.shape) if rows is not None else None,
            'dtype': str(rows.dtype) if rows is not None else None,
            'device': str(rows.device) if rows is not None else None,
            'state': None,
        }
        if g is not None:
            try:
                item['slot_text'] = g['tok'].decode(slot or [])
            except Exception as exc:
                item['slot_decode_error'] = type(exc).__name__ + ': ' + str(exc)
        if rows is not None:
            item['finite'] = bool(g['torch'].isfinite(rows).all().item()) if g else None
            if g and rows.device.type == 'cpu' and rows.dtype == g['torch'].float32:
                item['state'] = g['stats849'](rows)
        rows_out.append(item)
    return rows_out


@contextlib.contextmanager
def runtime_context857(label, g=None, segments=None, pre=None, post=None):
    global LAST_CONTEXT857
    record = {
        'label': label,
        'time_offset_seconds': time.perf_counter() - START857,
        **current_job857(g),
        'segments': segment_metadata857(g, segments),
        'prefix_length': len(pre) if pre is not None else None,
        'suffix_length': len(post) if post is not None else None,
        'substep': None,
    }
    previous = STATE857.get('active')
    STATE857['active'] = record
    LAST_CONTEXT857 = record
    jsonl_append857('857_runtime_context.jsonl', {'event': 'ENTER', **record})
    try:
        yield record
    except BaseException as exc:
        failure = {
            'event': 'EXCEPTION',
            **record,
            'exception_type': type(exc).__name__,
            'exception_text': str(exc),
            'exception_traceback': ''.join(traceback.format_exception(
                type(exc), exc, exc.__traceback__)),
            'capture': STATE857.get('capture'),
        }
        jsonl_append857('857_runtime_context.jsonl', failure)
        FAILURES857.append(failure)
        raise
    finally:
        STATE857['active'] = previous


def hook_audit857(g, event):
    """Record hooks verbatim by location/type; never remove or suppress them."""
    rows = []
    for module_name, module in g['model'].named_modules():
        for kind in ('_forward_pre_hooks', '_forward_hooks'):
            for handle, hook in getattr(module, kind).items():
                rows.append({
                    'module': module_name,
                    'kind': kind,
                    'handle': str(handle),
                    'hook_type': type(hook).__name__,
                    'hook_module': type(hook).__module__,
                })
    record = {
        'event': event,
        'time_offset_seconds': time.perf_counter() - START857,
        **current_job857(g),
        'transformers_output_capturing_installed': bool(getattr(
            g['model'], '_output_capturing_hooks_installed', False)),
        'hook_count': len(rows),
        'hooks': rows,
    }
    STATE857['hook_audits'].append(record)
    json_write857('857_hook_audit.json', STATE857['hook_audits'])
    return record


def assert_hook_free857(g, event):
    record = hook_audit857(g, event)
    if record['hook_count'] or record['transformers_output_capturing_installed']:
        raise RuntimeError('TEST857_FORWARD_HOOK_DETECTED: ' + event)
    return record


class Quiet857:
    def __init__(self):
        self.pending = ''

    def write(self, text):
        LOG_FILE857.write(text)
        LOG_FILE857.flush()
        self.pending += text
        while '\n' in self.pending:
            line, self.pending = self.pending.split('\n', 1)
            if 'TEST854 JOB-BY-JOB RESULTS|' in line:
                short857('JOB', line.split('TEST854 JOB-BY-JOB RESULTS|', 1)[1][:240])
        return len(text)

    def flush(self):
        LOG_FILE857.flush()

    def isatty(self):
        return False


SPELLINGS857 = (' CONTINUE', ' REVISE', ' STOP', ' SUFFICIENT', ' INSUFFICIENT')


def capture857(out, local):
    # Logits-only observation. Do not request hidden_states: Transformers v5
    # lazily installs persistent output-capturing forward hooks for that request.
    g = STATE857['g']
    logits = out.logits[0, -1].detach().float()
    sequence_length = int(out.logits.shape[1])
    step = len(STATE857['frames'])
    STATE857['capture'] = {
        **current_job857(g),
        'stage': None if not STATE857.get('active') else STATE857['active']['label'],
        'step': step,
        'logit_sequence_length': sequence_length,
        'logits_shape': list(logits.shape),
        'logits_dtype': str(logits.dtype),
        'logits_device': str(logits.device),
    }
    scores = logits[STATE857['first_ids']].cpu().tolist()
    record = {
        'step': step,
        'logit_sequence_length': sequence_length,
        'logits_shape': list(logits.shape),
        'logits_dtype': str(logits.dtype),
        'logits_device': str(logits.device),
        'returned_logits_bytes': out.logits.numel() * out.logits.element_size(),
        'tokenizations': STATE857['tokenizations'],
        'lens': 'diagnostic last-token logits, NOT action probabilities',
        'first_token_logits': dict(zip(SPELLINGS857, scores)),
        'stop_minus_revise': scores[2] - scores[1],
        'observation_scope': 'existing public logits only; hidden-state X-RAY disabled',
    }
    STATE857['arrays']['step%d_logits' % step] = logits.cpu().numpy()
    STATE857['frames'].append(record)


def clone_observer857(fn_node, g):
    node = copy.deepcopy(fn_node)
    original_name = node.name
    node.name = '_xr_' + original_name
    changed = 0

    class Observe857(ast.NodeTransformer):
        def visit_Assign(self, n):
            nonlocal changed
            self.generic_visit(n)
            if (len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
                    and n.targets[0].id == 'out' and isinstance(n.value, ast.Call)
                    and isinstance(n.value.func, ast.Name) and n.value.func.id == 'model'):
                assert not any(k.arg == 'output_hidden_states' for k in n.value.keywords)
                # No model kwargs are added. The call and all numerical inputs stay exact.
                changed += 1
                return [n, ast.parse('_xr_capture(out, locals())').body[0]]
            return n

    node = Observe857().visit(node)
    assert changed == 2, ('OBSERVATION_SITES', original_name, changed)
    module = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    # Reverse the observational delta and require exact AST equality.
    reverse = copy.deepcopy(node)
    reverse.name = original_name

    class Undo857(ast.NodeTransformer):
        def visit_Expr(self, n):
            if (isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
                    and n.value.func.id == '_xr_capture'):
                return None
            return self.generic_visit(n)

    reverse = Undo857().visit(reverse)
    assert ast.dump(reverse, include_attributes=False) == ast.dump(
        fn_node, include_attributes=False)
    if g is None:
        REAL_COMPILE857(module, 'TEST857_OBSERVER_STATIC', 'exec')
        return module
    exec(REAL_COMPILE857(module, 'TEST857_OBSERVER', 'exec'), g)
    return g[node.name]


def install857(g):
    assert not STATE857['installed']
    STATE857['installed'] = True
    STATE857['g'] = g
    torch = g['torch']
    np = g['np']
    assert g['NL'] == 80 and g['H'] == 8192 and g['DTYPE'] == torch.bfloat16
    assert len(g['JOBS841']) == 12 and not g['REC841'], 'Fresh run required; no unobserved resume'
    assert torch.cuda.device_count() == 1
    assert 'A100' in torch.cuda.get_device_name(0)
    assert not any(p.requires_grad for p in g['model'].parameters())
    assert_hook_free857(g, 'install_before_observation')
    transformers_module = g.get('transformers')
    STATE857['environment'] = {
        'torch_version': str(torch.__version__),
        'transformers_version': (None if transformers_module is None else
            str(getattr(transformers_module, '__version__', 'UNKNOWN'))),
        'hidden_states_requested': False,
        'observation': 'public out.logits only',
        'repair': 'remove output capture request; never clear hooks',
    }
    json_write857('857_environment.json', STATE857['environment'])
    short857('GPU:', torch.cuda.get_device_name(0), '| frozen NF4 | BF16 | layers=80 H=8192',
        '| free GiB=', round(torch.cuda.mem_get_info()[0] / 1024 ** 3, 2))
    tokens = [list(g['tok'](s, add_special_tokens=False).input_ids) for s in SPELLINGS857]
    assert all(tokens)
    STATE857['tokenizations'] = dict(zip(SPELLINGS857, tokens))
    STATE857['first_ids'] = [value[0] for value in tokens]
    g['_xr_capture'] = capture857
    gen = g['gen851']
    observed = clone_observer857(STATE857['functions']['gen851'], g)
    inv = g['invoke851']
    gen_coverage = clone_observer857(STATE857['functions']['gen849'], g)
    old_coverage = g['coverage_state852']

    def observe_coverage(q, condition, mode, memx):
        fresh = (q, condition, mode) not in g['COVERAGE_SHARED852']
        h = old_coverage(q, condition, mode, memx)
        assert_hook_free857(g, 'coverage_original_return')
        if fresh:
            pre = list(g['prompt_ids'](g['COVERAGE852'].format(q=g['QTEXT841'][q])))
            with runtime_context857('coverage_replay', g, None, pre,
                    g['COVERAGE_SUFFIX852']) as active:
                STATE857['arrays'] = {}
                STATE857['frames'] = []
                active['substep'] = 'observed_coverage_generator'
                obs = gen_coverage(memx, pre, None, g['COVERAGE_SUFFIX852'])
                assert_hook_free857(g, 'coverage_observed_return')
                same = (h['toks'] == obs['toks'] and h['text'] == obs['text']
                    and torch.equal(h['rows'], obs['rows']) and h['top1'] == obs['top1'])
                assert same, 'COVERAGE_OBSERVER_CHANGED_COMPUTATION'
                path = 'coverage_%02d.npz' % len(STATE857['coverage'])
                np.savez_compressed(ROOT857 / path, **STATE857['arrays'])
                record = {
                    **current_job857(g),
                    'requested_qid': q,
                    'requested_condition': condition,
                    'requested_mode': mode,
                    'file': path,
                    'text': h['text'],
                    'tokens': h['trace849']['all_token_ids'],
                    'valid_protocol': h['text'].strip() in ('SUFFICIENT', 'INSUFFICIENT'),
                    'observer_equality': same,
                    'frames': STATE857['frames'],
                    'prefix_ids': pre,
                    'suffix_ids': list(g['COVERAGE_SUFFIX852']),
                }
                STATE857['coverage'].append(record)
                json_write857('857_coverage.json', STATE857['coverage'])
                jsonl_append857('857_xray.jsonl', {'kind': 'COVERAGE', **record})
        return h

    g['coverage_state852'] = observe_coverage

    def wrapped(memx, pre, segments, post, stage, tensors, traces, baseline=False):
        assert not baseline, 'Unexpected TEST854 path'
        with runtime_context857('invoke_' + stage, g, segments, pre, post) as active:
            torch.cuda.synchronize()
            begun = time.perf_counter()
            STATE857['arrays'] = {}
            STATE857['frames'] = []
            # Budget guard for observational workload; never counted as model STOP.
            assert time.perf_counter() - STATE857['start'] < 3600, 'XRAY_MECHANICAL_TIME_LIMIT'
            checked = stage == 'review_0' and g['arm851'] == 'BASELINE853'
            active['substep'] = 'reference_generator' if checked else 'not_applicable'
            reference = gen(memx, pre, segments, post) if checked else None
            if checked:
                assert_hook_free857(g, 'reference_generator_return')
            g['gen851'] = observed
            try:
                active['substep'] = 'observed_generator'
                h = inv(memx, pre, segments, post, stage, tensors, traces, baseline=False)
            finally:
                g['gen851'] = gen
            assert_hook_free857(g, 'observed_generator_return')
            if checked:
                active['substep'] = 'runtime_equality'
                same = (h['toks'] == reference['toks'] and h['text'] == reference['text']
                    and torch.equal(h['rows'], reference['rows']) and h['top1'] == reference['top1'])
                STATE857['equalities'].append(bool(same))
                assert same, 'OBSERVER_CHANGED_NATIVE_COMPUTATION'
            identity = {
                **current_job857(g),
                'stage': stage,
            }
            index = len(STATE857['observations'])
            path = 'native_%03d.npz' % index
            np.savez_compressed(ROOT857 / path, **STATE857['arrays'])
            row = {
                **identity,
                'file': path,
                'frames': STATE857['frames'],
                'input_segments': segment_metadata857(g, segments),
                'text': h['text'],
                'tokens': h['trace849']['all_token_ids'],
                'continuity': h['trace849']['continuity'],
                'prefix_ids': list(pre),
                'suffix_ids': list(post or []),
                'memory_tokens': int(memx[0][0].shape[-2]),
                'seconds_with_observation': time.perf_counter() - begun,
            }
            STATE857['observations'].append(row)
            STATE857['invocations'].append({
                **identity,
                'memx': memx,
                'pre': list(pre),
                'segments': [(list(slot), None if rows is None else rows.clone().cpu())
                    for slot, rows in segments],
                'post': list(post or []),
                'h': copy.deepcopy(h),
            })
            jsonl_append857('857_observations.jsonl', row)
            jsonl_append857('857_xray.jsonl', {'kind': 'NATIVE', **row})
            return h

    g['invoke851'] = wrapped
    old_save = g['save_job841']
    expected_jobs = [j['job'] for j in g['JOBS841'][:2]]
    assert len(expected_jobs) == 2
    assert all(j['arm'] == 'BASELINE853' for j in g['JOBS841'][:2])

    def save_and_stop(job, record, tensors):
        result = old_save(job, record, tensors)
        STATE857['saved_jobs'].append(job)
        assert_hook_free857(g, 'job_saved_' + str(job))
        if STATE857['saved_jobs'] == expected_jobs:
            # REC841 and the native job artifact are already saved. The inherited
            # wrapper will preserve this explicit diagnostic exception verbatim.
            raise Gate1SmokeComplete857('GATE1_TWO_JOB_OBSERVATION_COMPLETE')
        assert len(STATE857['saved_jobs']) < len(expected_jobs), 'UNEXPECTED_JOB_ORDER'
        return result

    g['save_job841'] = save_and_stop
    short857('OBSERVER: logits-only AST inverse PASS; no hidden states; no hooks; two-job limit armed.')


def compile_xray857(source, filename, mode, *args, **kwargs):
    # Intercept only the final assembled CELL compile, before model loading.
    if filename == 'TEST849_CELL':
        assert not STATE857['compiled']
        STATE857['compiled'] = True
        tree = copy.deepcopy(source) if isinstance(source, ast.AST) else ast.parse(source)
        matches = [n for n in tree.body if isinstance(n, ast.Assign)
            and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
            and n.targets[0].id == 'BODY841']
        assert len(matches) == 1 and isinstance(matches[0].value, ast.Constant)
        body = matches[0].value.value
        bt = ast.parse(body)
        STATE857['functions'] = {n.name: n for n in bt.body if isinstance(n, ast.FunctionDef)}
        assert {'gen849', 'gen851', 'invoke851'} <= STATE857['functions'].keys()
        for name in ('gen849', 'gen851'):
            clone_observer857(STATE857['functions'][name], None)
        loops = [i for i, n in enumerate(bt.body) if isinstance(n, ast.For)
            and isinstance(n.target, ast.Tuple) and 'ji846' in ast.unparse(n.target)]
        assert len(loops) == 1
        insert = ast.parse('_xr_install(globals())').body[0]
        bt.body.insert(loops[0], insert)
        lines = body.splitlines(keepends=True)
        lines[bt.body[loops[0] + 1].lineno - 1:bt.body[loops[0] + 1].lineno - 1] = [
            '_xr_install(globals())\n']
        patched = ''.join(lines)
        assert patched.count('# ====== OFFLINE PHASE MARKER ======') == 1
        bt.body.remove(insert)
        assert ast.dump(bt, include_attributes=False) == ast.dump(ast.parse(body),
            include_attributes=False)
        marker = '# ====== OFFLINE PHASE MARKER ======'
        assert body.count(marker) == 1
        names = {n.id for n in ast.walk(ast.parse(body.split(marker)[0]))
            if isinstance(n, ast.Name)}
        assert not names & {'worlds829', 'EVALKEY841', 'CONTENT841', 'card_meta829'}
        json_write857('857_patch_manifest.json', {
            'base_body_sha256': sha256_bytes857(body.encode()),
            'instrumented_body_sha256': sha256_bytes857(patched.encode()),
            'change': 'one logits-only observer installation; generator model calls and kwargs unchanged',
            'root_cause': 'output_hidden_states lazily installed persistent Transformers forward hooks',
            'minimal_repair': 'no output_hidden_states request; no hook removal; fresh model required',
            'hidden_state_xray': 'NOT_RUN',
            'source_panel_jobs_before_diagnostic_limit': 12,
            'jobs_allowed_before_diagnostic_stop': 2,
            'review_equality_replays': 2,
            'coverage_equality_replays_max': 2,
            'N_probes': 0,
            'causal_replays_during_original_jobs': 0,
            'causal_replays_after_diagnostic_stop': 'planned; no original-stream feedback',
            'decision_path': 'original TEST854; diagnostic outputs never used for actions; review loop and MAX_REVIEWS851 unchanged',
        })
        matches[0].value = ast.Constant(patched)
        source = ast.fix_missing_locations(tree)
    return REAL_COMPILE857(source, filename, mode, *args, **kwargs)


def recover_inherited_error857(env, outer_exception, outer_trace):
    """Recover, but never repair, the exception saved by the inherited wrapper.

    TEST841 stores the original exception in TEST841_ERROR and its complete
    traceback in _tbtext841, then raises SystemExit only after leaving the
    original except block. Consequently the outer traceback alone is not the
    RuntimeError root-cause traceback.
    """
    saved_error = env.get('TEST841_ERROR')
    saved_text = env.get('_tbtext841')
    has_saved_text = isinstance(saved_text, str) and bool(saved_text.strip())
    outer_label = (None if outer_exception is None else
        type(outer_exception).__name__ + ': ' + str(outer_exception))
    info = {
        'outer_exception': outer_label,
        'outer_exception_type': (None if outer_exception is None else
            type(outer_exception).__name__),
        'outer_exception_is_wrapper_only': isinstance(outer_exception, SystemExit),
        'saved_exception_global': 'TEST841_ERROR',
        'saved_traceback_global': '_tbtext841',
        'saved_exception_present': saved_error is not None,
        'saved_traceback_present': has_saved_text,
        'saved_exception_type': (None if saved_error is None else
            type(saved_error).__name__),
        'saved_exception_text': (None if saved_error is None else str(saved_error)),
        'saved_exception_is_baseexception': isinstance(saved_error, BaseException),
        'original_runtime_error_recovered': False,
        'original_traceback_source': 'NONE',
        'saved_traceback_matches_exception': None,
        'exception_formatting_error': None,
        'context_failure_count': len(FAILURES857),
        'last_runtime_context': LAST_CONTEXT857,
    }
    sections = []
    if outer_trace:
        sections.append(
            '===== OUTER WRAPPER TRACEBACK — NOT THE ROOT-CAUSE TRACEBACK =====\n'
            + outer_trace.rstrip() + '\n')
    if has_saved_text:
        sections.append(
            '===== INHERITED ORIGINAL TRACEBACK — _tbtext841 =====\n'
            + saved_text.rstrip() + '\n')
        info['original_runtime_error_recovered'] = True
        info['original_traceback_source'] = '_tbtext841'
        info['saved_traceback_sha256'] = sha256_bytes857(saved_text.encode('utf-8'))

    root_label = outer_label
    if isinstance(saved_error, BaseException):
        root_label = type(saved_error).__name__ + ': ' + str(saved_error)
        try:
            formatted = ''.join(traceback.format_exception(
                type(saved_error), saved_error, saved_error.__traceback__))
        except Exception as exc:
            # A formatting failure is explicit evidence, not a silent omission.
            formatted = ''
            info['exception_formatting_error'] = type(exc).__name__ + ': ' + str(exc)
        info['saved_exception_has_traceback'] = saved_error.__traceback__ is not None
        if formatted:
            info['saved_exception_traceback_sha256'] = sha256_bytes857(
                formatted.encode('utf-8'))
            info['original_runtime_error_recovered'] = True
            if not has_saved_text:
                info['original_traceback_source'] = 'TEST841_ERROR.__traceback__'
            if has_saved_text:
                info['saved_traceback_matches_exception'] = (
                    saved_text.strip() == formatted.strip())
            # Normally these are identical. Keep both if they differ so no
            # traceback evidence is silently replaced or discarded.
            if not has_saved_text or saved_text.strip() != formatted.strip():
                sections.append(
                    '===== INHERITED ORIGINAL TRACEBACK — TEST841_ERROR.__traceback__ =====\n'
                    + formatted.rstrip() + '\n')
    elif saved_error is not None:
        info['invalid_saved_exception_repr'] = repr(saved_error)

    return root_label, '\n'.join(sections), info


def reproduce_pre857857():
    quiet = Quiet857()
    env = {
        '__name__': '__main__',
        'compile': compile_xray857,
        '_xr_install': install857,
    }
    STATE857['start'] = time.perf_counter()
    outer_exception = None
    outer_trace = ''
    try:
        sys.stdout = quiet
        sys.stderr = quiet
        exec(REAL_COMPILE857(RAW_SOURCES857['854.py'].decode(),
            'LOCKED_TEST854', 'exec'), env)
    except BaseException as exc:
        outer_exception = exc
        # This usually contains only TEST849_FAILED: RuntimeError. The actual
        # RuntimeError is recovered below from the inherited wrapper globals.
        outer_trace = traceback.format_exc()
    finally:
        sys.stdout = CONSOLE857
        sys.stderr = ERROR_CONSOLE857
        quiet.flush()
    root_error, combined_trace, evidence = recover_inherited_error857(
        env, outer_exception, outer_trace)
    return env, root_error, combined_trace, evidence


def records_digest857(env):
    return sha256_bytes857(json.dumps(env.get('REC841', {}), sort_keys=True,
        ensure_ascii=False).encode('utf-8'))


def verify_two_job857(env, combined_trace):
    """Technical gate only: scientific termination is reported, never required."""
    jobs = env.get('JOBS841', [])
    records = env.get('REC841', {})
    expected = jobs[:2]
    expected_ids = [j['job'] for j in expected]
    assert len(expected) == 2
    assert [j['intervention'] for j in expected] == ['INTACT', 'REMOVED']
    assert all(j['arm'] == 'BASELINE853' for j in expected)
    assert STATE857['saved_jobs'] == expected_ids, (
        'TWO_JOB_SAVE_MISMATCH', STATE857['saved_jobs'], expected_ids)
    assert set(records) == set(expected_ids), 'TWO_JOB_RECORD_SET_MISMATCH'
    assert 'GATE1_TWO_JOB_OBSERVATION_COMPLETE' in combined_trace, (
        'EXPECTED_DIAGNOSTIC_STOP_NOT_FOUND')
    for j in expected:
        record = records[j['job']]
        assert record['arm'] == 'BASELINE853'
        assert record['condition'] == j['intervention']
        assert record['model_stop'] == (record['end'] == 'MODEL_STOP')
        if record['end'] == 'MECHANICAL_REVIEW_LIMIT':
            assert not record['model_stop']
            assert record['mechanical_stop_reason'] == 'MECHANICAL_REVIEW_LIMIT'
    assert STATE857['equalities'] == [True, True], (
        'TWO_REVIEW_EQUALITIES_REQUIRED', STATE857['equalities'])
    assert all(c['observer_equality'] for c in STATE857['coverage'])
    assert not STATE857['probes'], 'N_PROBES_FORBIDDEN_IN_ORIGINAL_TWO_JOB_STREAM'
    assert not STATE857['causal_probes'], 'CAUSAL_PROBE_RAN_BEFORE_ORIGINAL_STREAM_END'
    final_audit = assert_hook_free857(env, 'post_diagnostic_stop_before_causal_replays')
    assert STATE857['hook_audits'] and all(
        row['hook_count'] == 0 and not row['transformers_output_capturing_installed']
        for row in STATE857['hook_audits'])
    assert not any(p.requires_grad for p in env['model'].parameters())
    assert env['MAX_REVIEWS851'] == 2
    return {
        'status': 'PASS_TECHNICAL_TWO_BASELINE_JOBS_ANY_NATIVE_END',
        'jobs': [{
            'job': j['job'], 'qid': j.get('qid'), 'condition': j['intervention'],
            'arm': j['arm'], 'end': records[j['job']]['end'],
            'answer': records[j['job']].get('answer'),
            'model_stop': records[j['job']]['end'] == 'MODEL_STOP',
            'mechanical_limit': records[j['job']]['end'] == 'MECHANICAL_REVIEW_LIMIT',
            'actions': [c['action'] for c in records[j['job']].get('cycles', [])],
            'revision_texts': [None if c.get('revision') is None else
                c['revision'].get('text') for c in records[j['job']].get('cycles', [])],
            'coverage_texts': [None if c.get('coverage_native') is None else
                c['coverage_native'].get('text') for c in records[j['job']].get('cycles', [])],
            'recurrent_previous_control': [c.get('recurrent_previous_control')
                for c in records[j['job']].get('cycles', [])],
        } for j in expected],
        'review_replay_equalities': STATE857['equalities'],
        'coverage_observer_equalities': [c['observer_equality'] for c in STATE857['coverage']],
        'hook_audits': len(STATE857['hook_audits']),
        'final_hook_count': final_audit['hook_count'],
        'diagnostic_stop': 'GATE1_TWO_JOB_OBSERVATION_COMPLETE',
        'diagnostic_stop_is_model_stop': False,
        'scope': 'Technical hook-free continuity/equivalence only; no ACCEPT/STOP requirement.',
    }


def clone_segments857(segments):
    return [(list(slot), None if rows is None else rows.clone().cpu())
        for slot, rows in segments]


def segment_map857(g, segments):
    names = (
        ('C', 'C_SLOT851'), ('E', 'E_SLOT851'), ('Kprev', 'K_SLOT851'),
        ('U', 'U_SLOT852'), ('R', 'R_SLOT852'),
        ('K0', 'K_SLOT854'), ('J', 'J_SLOT854'),
    )
    result = {}
    for name, constant in names:
        matches = [(list(slot), rows) for slot, rows in segments
            if list(slot) == list(g[constant])]
        if matches:
            assert len(matches) == 1, ('DUPLICATE_SLOT', name)
            result[name] = matches[0]
    return result


def replace_named_slot857(g, segments, name, rows):
    constants = {
        'C': 'C_SLOT851', 'E': 'E_SLOT851', 'Kprev': 'K_SLOT851',
        'U': 'U_SLOT852', 'R': 'R_SLOT852',
        'K0': 'K_SLOT854', 'J': 'J_SLOT854',
    }
    target = list(g[constants[name]])
    found = 0
    output = []
    for slot, old in segments:
        if list(slot) == target:
            found += 1
            assert old is not None and old.shape == rows.shape
            assert old.dtype == rows.dtype and old.device.type == rows.device.type == 'cpu'
            output.append((list(slot), rows.clone().cpu()))
        else:
            output.append((list(slot), None if old is None else old.clone().cpu()))
    assert found == 1, ('CAUSAL_SLOT_NOT_UNIQUE', name, found)
    return output


def segments_sha857(segments):
    return sha256_bytes857(json.dumps([
        {'slot': list(slot), 'state': None if rows is None else
            {'shape': list(rows.shape), 'dtype': str(rows.dtype),
             'sha256': hashlib.sha256(rows.detach().cpu().numpy().tobytes()).hexdigest()}}
        for slot, rows in segments], sort_keys=True).encode('utf-8'))


def native_h_equal857(torch, a, b):
    return (a['toks'] == b['toks'] and a['text'] == b['text']
        and a['top1'] == b['top1'] and a['kend'] == b['kend']
        and torch.equal(a['rows'], b['rows']))


def h_summary857(g, h):
    return {
        'text': h['text'],
        'tokens': list(h['trace849']['all_token_ids']),
        'soft_row_tokens': list(h['toks']),
        'first_token': h['tok1'],
        'first_token_top1': h['top1'],
        'first_token_entropy': h['H1'],
        'output': g['stats849'](h['rows']),
        'continuity': h['trace849']['continuity'],
        'termination': h['trace849']['termination'],
    }


def score_actions857(g, memx, pre, segments, post):
    """Teacher-forced fixed protocol strings; diagnostic, never an action source."""
    torch = g['torch']
    with torch.no_grad():
        X, checks = g['make_x851'](pre, segments, post)
        L, n = int(X.shape[0]), int(memx[0][0].shape[-2])
        scores = []
        for spelling in (' CONTINUE', ' REVISE', ' STOP'):
            g['budget849']()
            ids = list(g['tok'](spelling, add_special_tokens=False).input_ids)
            assert ids and g['tok'].decode(ids) == spelling, (
                'ACTION_TOKENIZATION', spelling, ids)
            Y = (torch.cat([X, g['embed841'](ids[:-1])], dim=0)
                if len(ids) > 1 else X)
            assert n + len(Y) <= g['MAX_FUSED_TOKENS']
            cache = g['cache_build'](list(memx))
            pos = torch.arange(n, n + len(Y), device=g['DEV'])
            out = g['model'](
                inputs_embeds=Y.reshape(1, len(Y), g['H']),
                past_key_values=cache,
                attention_mask=torch.ones((1, n + len(Y)), device=g['DEV'], dtype=torch.long),
                position_ids=pos.unsqueeze(0), cache_position=pos,
                use_cache=True, return_dict=True)
            selected_logits = out.logits[0, L - 1:L - 1 + len(ids)].float()
            logp = torch.log_softmax(selected_logits, dim=-1)
            token_logps = logp[torch.arange(len(ids), device=g['DEV']),
                torch.tensor(ids, device=g['DEV'])]
            first_logits = selected_logits[0]
            first_logps = logp[0]
            scores.append({
                'spelling': spelling,
                'ids': ids,
                'sequence_logp': float(token_logps.sum()),
                'mean_token_logp': float(token_logps.mean()),
                'token_logps': [float(x) for x in token_logps],
                'first_token_id': ids[0],
                'first_token_logit': float(first_logits[ids[0]]),
                'first_token_logp': float(first_logps[ids[0]]),
                'first_token_softmax_probability': float(first_logps[ids[0]].exp()),
                'meaning': 'teacher-forced hard-token sequence score; not soft-rollout probability',
            })
            g['COUNT834']['probe_forwards'] += 1
            del out, cache, logp, selected_logits, token_logps
        return scores


def score_margins857(scores):
    by_name = {s['spelling'].strip(): s for s in scores}
    assert set(by_name) == {'CONTINUE', 'REVISE', 'STOP'}
    return {
        'stop_minus_revise_sequence_logp':
            by_name['STOP']['sequence_logp'] - by_name['REVISE']['sequence_logp'],
        'stop_minus_continue_sequence_logp':
            by_name['STOP']['sequence_logp'] - by_name['CONTINUE']['sequence_logp'],
        'stop_minus_revise_first_token_logit':
            by_name['STOP']['first_token_logit'] - by_name['REVISE']['first_token_logit'],
        'stop_minus_revise_first_token_logp':
            by_name['STOP']['first_token_logp'] - by_name['REVISE']['first_token_logp'],
    }


def find_invocation857(job, stage):
    rows = [x for x in STATE857['invocations']
        if x['job'] == job and x['stage'] == stage]
    assert len(rows) == 1, ('INVOCATION_SNAPSHOT_NOT_UNIQUE', job, stage, len(rows))
    return rows[0]


def probe_plan857(cycle, has_kprev):
    plan = [
        ('ORIGINAL_REPLAY', None, 'precontrol_and_final'),
        ('C_ZERO_DIRECT', 'C', 'precontrol_only_R_and_gate_fixed'),
        ('E_ZERO_DIRECT', 'E', 'precontrol_only_R_and_gate_fixed'),
        ('U_ZERO', 'U', 'precontrol_only'),
        ('R_ZERO', 'R', 'precontrol_only'),
        ('K0_ZERO_FINAL', 'K0', 'final_only'),
        ('J_ZERO_FINAL', 'J', 'final_only'),
    ]
    if cycle == 1:
        assert has_kprev, 'SECOND_CYCLE_KPREV_MISSING'
        plan.insert(1, ('KPREV_ZERO', 'Kprev', 'precontrol_only'))
    else:
        assert not has_kprev, 'UNEXPECTED_CYCLE0_KPREV'
    return plan


def run_one_probe857(g, target_job, cycle, variant, slot_name, mode,
        original_pre, original_review, original_record_digest):
    torch, np = g['torch'], g['np']
    index = len(STATE857['causal_probes'])
    memx = original_review['memx']
    assert memx is original_pre['memx'], 'PRECONTROL_REVIEW_MEMORY_MISMATCH'
    pre_segments = clone_segments857(original_pre['segments'])
    decision_segments = clone_segments857(original_review['segments'])
    original_pre_sha = segments_sha857(pre_segments)
    original_decision_sha = segments_sha857(decision_segments)
    pre_map = segment_map857(g, pre_segments)
    assert {'C', 'E', 'U', 'R'} <= set(pre_map)
    assert original_pre['post'] == list(g['REVIEW_SUFFIX851'])
    assert original_review['post'] == list(g['REVIEW_SUFFIX851'])
    original_decision_map = segment_map857(g, decision_segments)
    assert set(original_decision_map) == {'K0', 'J'}
    original_pre_hash = original_pre_sha
    original_decision_hash = original_decision_sha
    intervention_input_changed = variant == 'ORIGINAL_REPLAY'

    if mode == 'final_only':
        # Hold the other final state fixed. No upstream replay is needed.
        pre_h = copy.deepcopy(original_pre['h'])
        final_input = replace_named_slot857(g, decision_segments, slot_name,
            torch.zeros_like(original_decision_map[slot_name][1]))
        intervention_input_changed = segments_sha857(final_input) != original_decision_sha
        pre_replay_equality = None
        J = original_decision_map['J'][1].clone()
        K0 = original_decision_map['K0'][1].clone()
    else:
        if slot_name is not None:
            pre_input = replace_named_slot857(g, pre_segments, slot_name,
                torch.zeros_like(pre_map[slot_name][1]))
            intervention_input_changed = segments_sha857(pre_input) != original_pre_sha
        else:
            pre_input = pre_segments
        # Direct controlled slot effect: R and the Hadamard gate geometry remain
        # the original C/E values. Only the named precontrol input is replaced.
        pre_h = g['gen851'](memx, list(original_pre['pre']), pre_input,
            list(original_pre['post']))
        J = g['interaction854'](pre_map['C'][1], pre_map['E'][1], pre_h['rows'])
        K0 = pre_h['rows']
        final_input = [(list(g['K_SLOT854']), K0.clone().cpu()),
            (list(g['J_SLOT854']), J.clone().cpu())]
        pre_replay_equality = (native_h_equal857(torch, pre_h, original_pre['h'])
            if variant == 'ORIGINAL_REPLAY' else None)

    review_h = g['gen851'](memx, list(original_review['pre']), final_input,
        list(original_review['post']))
    review_replay_equality = (native_h_equal857(torch, review_h, original_review['h'])
        if variant == 'ORIGINAL_REPLAY' else None)
    if variant == 'ORIGINAL_REPLAY':
        assert pre_replay_equality, ('PRECONTROL_REPLAY_CHANGED', cycle)
        assert review_replay_equality, ('REVIEW_REPLAY_CHANGED', cycle)
        assert segments_sha857(final_input) == original_decision_sha, (
            'ORIGINAL_DECISION_SEGMENT_REPLAY_MISMATCH', cycle)
    else:
        assert intervention_input_changed, ('EMPTY_CAUSAL_INTERVENTION', variant)
    assert segments_sha857(pre_segments) == original_pre_hash
    assert segments_sha857(decision_segments) == original_decision_hash
    scores = score_actions857(g, memx, list(original_review['pre']), final_input,
        list(original_review['post']))
    action = g['parse849'](review_h['text'])
    original_action = g['parse849'](original_review['h']['text'])
    arrays = {
        'precontrol_output': pre_h['rows'].numpy().copy(),
        'K0': K0.numpy().copy(),
        'J': J.numpy().copy(),
        'review_output': review_h['rows'].numpy().copy(),
    }
    for name, (slot, rows) in segment_map857(g, final_input).items():
        arrays['final_' + name] = rows.numpy().copy()
    filename = '857_probe_%03d.npz' % index
    np.savez_compressed(ROOT857 / filename, **arrays)
    STATE857['probe_files'].append(filename)
    record = {
        'index': index,
        'job': target_job,
        'cycle': cycle,
        'variant': variant,
        'intervened_slot': slot_name,
        'mode': mode,
        'matched_shape_position_dtype': True,
        'intervention_input_changed': intervention_input_changed,
        'precontrol_replay_equality': pre_replay_equality,
        'review_replay_equality': review_replay_equality,
        'precontrol': h_summary857(g, pre_h),
        'K0': g['stats849'](K0),
        'J': g['stats849'](J),
        'review': h_summary857(g, review_h),
        'diagnostic_greedy_action': action,
        'original_greedy_action': original_action,
        'diagnostic_action_changed': action != original_action,
        'diagnostic_stop_not_original_model_stop': True,
        'action_scores': scores,
        'margins': score_margins857(scores),
        'tensor_file': filename,
        'original_record_sha256_before': original_record_digest,
        'interpretation_limits': [
            'Single-context intervention; no independent generalization claim.',
            'Zero-state ablation is computational sensitivity, not semantic evidence removal.',
            'Teacher-forced scores are not calibrated action probabilities.',
            'A diagnostic STOP here does not change or repair the original loop.',
        ],
    }
    STATE857['causal_probes'].append(record)
    json_write857('857_causal_probes.json', STATE857['causal_probes'])
    short857('CAUSAL PROBE', cycle, variant, 'ACTION=' + action,
        'ORIGINAL=' + original_action,
        'STOP-REVISE=' + str(record['margins']['stop_minus_revise_sequence_logp']))
    return record


def causal_summary857(env, target_job, original_digest):
    records = STATE857['causal_probes']
    expected = 7 + 8
    assert len(records) == expected, ('CAUSAL_COVERAGE_INCOMPLETE', len(records), expected)
    assert records_digest857(env) == original_digest, 'PROBES_CHANGED_ORIGINAL_JOB_RECORDS'
    assert not any(p.requires_grad for p in env['model'].parameters())
    final_audit = assert_hook_free857(env, 'post_causal_replays')
    originals = [r for r in records if r['variant'] == 'ORIGINAL_REPLAY']
    assert len(originals) == 2
    assert all(r['precontrol_replay_equality'] and r['review_replay_equality']
        for r in originals)
    by_cycle = {cycle: [r for r in records if r['cycle'] == cycle] for cycle in (0, 1)}
    stop_variants = [r['variant'] + '@cycle' + str(r['cycle']) for r in records
        if r['variant'] != 'ORIGINAL_REPLAY' and r['diagnostic_greedy_action'] == 'STOP']
    changed = [r['variant'] + '@cycle' + str(r['cycle']) for r in records
        if r['variant'] != 'ORIGINAL_REPLAY' and r['diagnostic_action_changed']]
    kprev = [r for r in records if r['variant'] == 'KPREV_ZERO']
    assert len(kprev) == 1 and kprev[0]['cycle'] == 1
    return {
        'status': 'PASS_EXECUTED_CAUSAL_SCREEN_NOT_A_MECHANISM_PROOF',
        'target_job': target_job,
        'planned_probe_count': expected,
        'completed_probe_count': len(records),
        'original_replay_equalities': [r['review_replay_equality'] for r in originals],
        'precontrol_replay_equalities': [r['precontrol_replay_equality'] for r in originals],
        'original_records_unchanged': True,
        'final_hook_count': final_audit['hook_count'],
        'diagnostic_stop_variants': stop_variants,
        'diagnostic_action_changed_variants': changed,
        'kprev_zero_cycle1': {
            'original_action': kprev[0]['original_greedy_action'],
            'ablated_action': kprev[0]['diagnostic_greedy_action'],
            'action_changed': kprev[0]['diagnostic_action_changed'],
            'margins': kprev[0]['margins'],
        },
        'cycles': {str(cycle): [{
            'variant': r['variant'],
            'original_action': r['original_greedy_action'],
            'diagnostic_action': r['diagnostic_greedy_action'],
            'action_changed': r['diagnostic_action_changed'],
            'margins': r['margins'],
        } for r in rows] for cycle, rows in by_cycle.items()},
        'causal_conclusion_rule': (
            'Only within-replay matched contrasts are admitted. A flip is context-specific '
            'sensitivity; no flip does not identify a threshold or prove component independence.'),
        'original_loop_repaired': False,
        'independent_generalization': False,
    }


def run_causal857(env):
    original_digest = records_digest857(env)
    STATE857['original_record_sha256'] = original_digest
    target = env['JOBS841'][1]
    target_job = target['job']
    original_record = env['REC841'][target_job]
    assert target['intervention'] == 'REMOVED'
    assert len(original_record['cycles']) == 2, (
        'TARGET_REQUIRES_TWO_ORIGINAL_CYCLES', original_record['end'])
    assert [c['action'] for c in original_record['cycles']] == ['REVISE', 'REVISE'], (
        'PREREGISTERED_TARGET_TRACE_NOT_REPRODUCED',
        [c['action'] for c in original_record['cycles']])
    # This target is locked to the observed REMOVED failure. An INTACT stop/accept
    # is retained as contrast, but no alternative job is silently substituted.
    for cycle in (0, 1):
        pre = find_invocation857(target_job, 'precontrol_%d' % cycle)
        review = find_invocation857(target_job, 'review_%d' % cycle)
        pre_map = segment_map857(env, pre['segments'])
        for variant, slot_name, mode in probe_plan857(cycle, 'Kprev' in pre_map):
            assert records_digest857(env) == original_digest, (
                'ORIGINAL_RECORD_MUTATED_DURING_PROBES', cycle, variant)
            run_one_probe857(env, target_job, cycle, variant, slot_name, mode,
                pre, review, original_digest)
            assert_hook_free857(env, 'causal_probe_%d_%s' % (cycle, variant))
    return causal_summary857(env, target_job, original_digest)


def ensure_partial_artifacts857():
    for name in ('857_observations.jsonl', '857_xray.jsonl', '857_runtime_context.jsonl'):
        path = ROOT857 / name
        if not path.exists():
            path.write_text('', encoding='utf-8')
    if not (ROOT857 / '857_runtime_traceback.txt').exists():
        (ROOT857 / '857_runtime_traceback.txt').write_text(
            TRACEBACK857 or 'NO_TRACEBACK_AVAILABLE\n', encoding='utf-8')
    if not (ROOT857 / '857_causal_probes.json').exists():
        json_write857('857_causal_probes.json', STATE857['causal_probes'])
    json_write857('857_runtime_equivalence.json', {
        'status': TWO_JOB_VERIFICATION857.get('status', 'NOT_RUN'),
        'required_jobs': ['BASELINE853/INTACT', 'BASELINE853/REMOVED'],
        'review_replay_equalities': STATE857['equalities'],
        'coverage_observer_equalities': [c['observer_equality'] for c in STATE857['coverage']],
        'saved_jobs': STATE857['saved_jobs'],
        'hook_audit_count': len(STATE857['hook_audits']),
        'verification': TWO_JOB_VERIFICATION857,
        'original_decision_end_does_not_gate_technical_pass': True,
    })
    json_write857('857_failures.json', {
        'execution_error': EXECUTION_ERROR857,
        'diagnostic_stop': DIAGNOSTIC_STOP857,
        'outer_execution_error': OUTER_EXECUTION_ERROR857,
        'probe_error': PROBE_ERROR857,
        'error_evidence': ERROR_EVIDENCE857,
        'two_job_verification': TWO_JOB_VERIFICATION857,
        'causal_verification': CAUSAL_VERIFICATION857,
        'last_runtime_context': LAST_CONTEXT857,
        'context_failures': FAILURES857,
        'partial_counts': {
            'observations': len(STATE857['observations']),
            'coverage': len(STATE857['coverage']),
            'runtime_equalities': len(STATE857['equalities']),
            'causal_probes': len(STATE857['causal_probes']),
        },
    })


def finalize857(gates, execution):
    ensure_partial_artifacts857()
    capture_cell_source857()
    original_jobs = TWO_JOB_VERIFICATION857.get('jobs', [])
    report = {
        'test': TEST857_KIND,
        'execution': execution,
        'gates': gates,
        'error': EXECUTION_ERROR857,
        'probe_error': PROBE_ERROR857,
        'diagnostic_stop': DIAGNOSTIC_STOP857,
        'outer_execution_error': OUTER_EXECUTION_ERROR857,
        'error_evidence': ERROR_EVIDENCE857,
        'two_job_verification': TWO_JOB_VERIFICATION857,
        'causal_verification': CAUSAL_VERIFICATION857,
        'environment': STATE857['environment'],
        'observer_equalities': STATE857['equalities'],
        'coverage_records': len(STATE857['coverage']),
        'coverage_protocol_valid': sum(bool(c['valid_protocol']) for c in STATE857['coverage']),
        'causal_probe_count': len(STATE857['causal_probes']),
        'original_model_stop_observed': any(j.get('model_stop') for j in original_jobs),
        'original_mechanical_limit_observed': any(j.get('mechanical_limit') for j in original_jobs),
        'diagnostic_stop_is_model_stop': False,
        'seconds': time.perf_counter() - START857,
        'known_limitations': [
            'Only two original BASELINE853 jobs are run; no 12-job generalization claim.',
            'The original 856 BLOCKED report is retained; 857 does not retroactively relabel it.',
            'The explicit two-job diagnostic stop is not MODEL_STOP.',
            'Post-hoc probe actions are not original actions and do not repair the loop.',
            'Zero-state interventions identify computational sensitivity in one context only.',
            'Teacher-forced hard-token scores are not calibrated action probabilities.',
            'Coverage text 100 remains invalid protocol; it is not semantically repaired in Python.',
            'No explicit action threshold exists in parse849; score margins do not prove threshold causation.',
            'MECHANICAL_REVIEW_LIMIT is not MODEL_STOP; UNKNOWN is not STOP.',
            'Physical tensor integrity does not prove semantic losslessness of CUT3.',
        ],
        'TEST857_NEW_CONTROL_ENGINE': False,
        'TEST857_CAUSAL_LOOP_REPAIR_ESTABLISHED': False,
    }
    json_write857('857_report.json', report)
    LOG_FILE857.flush()
    short857('TEST857 RESULT:', execution)
    for gate, status in gates.items():
        short857(gate + ':', status)
    short857('ORIGINAL ERROR:', EXECUTION_ERROR857 or 'NONE')
    short857('PROBE ERROR:', PROBE_ERROR857 or 'NONE')
    short857('DIAGNOSTIC STOP:', DIAGNOSTIC_STOP857 or 'NONE')
    short857('ORIGINAL MODEL STOP:', report['original_model_stop_observed'])
    short857('ORIGINAL MECHANICAL LIMIT:', report['original_mechanical_limit_observed'])
    short857('CAUSAL PROBES:', len(STATE857['causal_probes']))
    short857('ARTIFACTS:', str(ROOT857))
    LOG_FILE857.flush()
    manifest = {}
    for path in sorted(ROOT857.iterdir()):
        if path.is_file() and path.name != '857_sha256_manifest.json':
            manifest[path.name] = {
                'bytes': path.stat().st_size,
                'sha256': sha256_bytes857(path.read_bytes()),
            }
    json_write857('857_sha256_manifest.json', manifest)


# Initialize required append-only artifacts before source or GPU operations.
for artifact857 in ('857_observations.jsonl', '857_xray.jsonl', '857_runtime_context.jsonl'):
    (ROOT857 / artifact857).write_text('', encoding='utf-8')

try:
    short857('TEST857 MODE: original two-job trace + post-hoc matched causal replays.')
    short857('GPU EXECUTION: NOT VERIFIED BY AUTHOR; restart Colab before this cell.')
    short857('NO HOOKS: output_hidden_states is never requested; hooks are never cleared.')
    short857('ORIGINAL STREAM: actions/revisions/limit unchanged; probes start only after two saves.')
    if PRE857_ERROR.exists():
        (ROOT857 / '857_previous_pre855_traceback.txt').write_text(
            PRE857_ERROR.read_text(encoding='utf-8', errors='replace'), encoding='utf-8')
    json_write857('857_provenance.json', PROVENANCE857)
    load_sources857()
    gate0857 = 'PASS'
    RECOVERY_MODE857 = 'HOOKFREE_TWO_JOB_THEN_NONFEEDBACK_CAUSAL_SCREEN'
    env857, error857, trace857, evidence857 = reproduce_pre857857()
    EXECUTION_ERROR857 = error857
    OUTER_EXECUTION_ERROR857 = evidence857.get('outer_exception')
    TRACEBACK857 = trace857
    ERROR_EVIDENCE857 = evidence857
    if trace857:
        (ROOT857 / '857_runtime_traceback.txt').write_text(trace857, encoding='utf-8')
        short857(trace857[-12000:])
    expected_stop = 'GATE1_TWO_JOB_OBSERVATION_COMPLETE' in trace857
    if expected_stop:
        DIAGNOSTIC_STOP857 = 'GATE1_TWO_JOB_OBSERVATION_COMPLETE'
    try:
        TWO_JOB_VERIFICATION857 = verify_two_job857(env857, trace857)
    except Exception as verification_exc:
        verification_trace = traceback.format_exc()
        TRACEBACK857 = trace857 + '\n===== TECHNICAL VERIFICATION FAILURE =====\n' + verification_trace
        (ROOT857 / '857_runtime_traceback.txt').write_text(TRACEBACK857)
        short857(verification_trace)
        gate1857 = gate2857 = 'BLOCKED'
        execution857 = 'TECHNICAL_TWO_JOB_VERIFICATION_FAILED'
        EXECUTION_ERROR857 = type(verification_exc).__name__ + ': ' + str(verification_exc)
    else:
        # The inherited exception is only our expected diagnostic-stop, not a runtime failure.
        EXECUTION_ERROR857 = None
        gate1857 = gate2857 = 'PASS'
        execution857 = 'TWO_JOB_TECHNICAL_PASS'
    if gate1857 == 'PASS':
        try:
            CAUSAL_VERIFICATION857 = run_causal857(env857)
            gate3857 = gate4857 = 'PASS'
            execution857 = 'TWO_JOB_TRACE_AND_CAUSAL_SCREEN_COMPLETE'
        except BaseException as probe_exc:
            PROBE_ERROR857 = type(probe_exc).__name__ + ': ' + str(probe_exc)
            probe_trace = traceback.format_exc()
            TRACEBACK857 += '\n===== POSTHOC CAUSAL PROBE FAILURE =====\n' + probe_trace
            (ROOT857 / '857_runtime_traceback.txt').write_text(TRACEBACK857)
            short857(probe_trace)
            gate3857 = gate4857 = 'BLOCKED'
            execution857 = 'CAUSAL_SCREEN_INCOMPLETE_TRACEBACK_CAPTURED'
    else:
        gate3857 = gate4857 = 'BLOCKED'
    removed_ends = [j['end'] for j in TWO_JOB_VERIFICATION857.get('jobs', [])
        if j.get('condition') == 'REMOVED']
    gate5857 = ('NOT_OBSERVED_MECHANICAL_REVIEW_LIMIT'
        if removed_ends == ['MECHANICAL_REVIEW_LIMIT'] else
        'OBSERVED_MODEL_STOP' if removed_ends == ['MODEL_STOP'] else
        'OTHER_NATIVE_END_' + ('_'.join(removed_ends) if removed_ends else 'UNKNOWN'))
    gates857 = {
        'GATE0_SOURCE_INTEGRITY': gate0857,
        'GATE1_HOOKFREE_TWO_JOB_TECHNICAL': gate1857,
        'GATE2_OBSERVER_EQUIVALENCE': gate2857,
        'GATE3_ORIGINAL_DECISION_TRACE_AND_REPLAY': gate3857,
        'GATE4_MATCHED_CAUSAL_COMPONENT_SCREEN': gate4857,
        'GATE5_ORIGINAL_NATIVE_MODEL_STOP': gate5857,
        'GATE6_INDEPENDENT_GENERALIZATION': 'BLOCKED_TWO_JOB_DIAGNOSTIC_ONLY',
        'GATE7_ARTIFACT_INTEGRITY': 'PASS',
    }
    finalize857(gates857, execution857)
except BaseException as exc:
    EXECUTION_ERROR857 = type(exc).__name__ + ': ' + str(exc)
    TRACEBACK857 = traceback.format_exc()
    ERROR_EVIDENCE857 = {
        'source': 'TEST857_OUTER_EXCEPTION',
        'original_runtime_error_recovered': False,
        'exception_type': type(exc).__name__,
        'exception_text': str(exc),
    }
    (ROOT857 / '857_runtime_traceback.txt').write_text(TRACEBACK857)
    sys.stdout = CONSOLE857
    sys.stderr = ERROR_CONSOLE857
    short857(TRACEBACK857)
    gates857 = {
        'GATE0_SOURCE_INTEGRITY': 'PASS' if len(RAW_SOURCES857) == 11 else 'FAIL',
        'GATE1_HOOKFREE_TWO_JOB_TECHNICAL': 'BLOCKED',
        'GATE2_OBSERVER_EQUIVALENCE': 'BLOCKED',
        'GATE3_ORIGINAL_DECISION_TRACE_AND_REPLAY': 'BLOCKED',
        'GATE4_MATCHED_CAUSAL_COMPONENT_SCREEN': 'BLOCKED',
        'GATE5_ORIGINAL_NATIVE_MODEL_STOP': 'BLOCKED',
        'GATE6_INDEPENDENT_GENERALIZATION': 'BLOCKED',
        'GATE7_ARTIFACT_INTEGRITY': 'PASS',
    }
    finalize857(gates857, 'TEST857_FAILURE_TRACEBACK_CAPTURED')
finally:
    LOG_FILE857.close()
