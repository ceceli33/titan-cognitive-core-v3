# AKBASCORE SILICON HIPPOCAMPUS — TEST859 FEEDBACK-TO-DECISION CAUSALITY
# Locked TEST858 spine, one model load, two original jobs, no new motor.
# INTACT evaluates native preservation; it has no natural cycle1 and no forced loop.
# REMOVED cycle1 receives matched KPREV_SWAP and CARRY_CONTROL diagnostic replays.
# All replay actions/revisions are diagnostic, never original closed-loop outcomes.
# Locked offline node851/supported851 are executed only after original jobs finish.
# A=no numerical effect; B=numerical only; C=behavior change; D=C plus native
# dominance on preregistered evidence metrics. Mechanical limit is not MODEL_STOP.
# GPU execution is not claimed by the author.
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

TEST859_KIND = 'NATIVE_FEEDBACK_EVIDENCE_ALIGNED_DECISION_CAUSALITY'
BASE859 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
CODELOAD859 = 'https://codeload.github.com/ceceli33/titan-cognitive-core-v3/zip/refs/heads/main'
LOCKS859 = {
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
    '855.py': '8ab79676aded54cb30316c47feeeae8b89fb4625',
    '856.py': '93d7e9bd7ebc6c692cef0e1e62d05ad96e4086d1',
    '857.py': '0891ffe2d638e7a17ff9e851d160c2afeb609a1a',
    '855.log': 'afb58577e700031a4f788940ab4b8e7a69b59999',
    '856.log': '875a1d5fb3ad5c45700c4ebab17402a3c9b27bb3',
    '857.log': 'ef3ae882ecf03dd9b9668939bd55ce65eeae8455',
    '858.py': 'f78efd24b2fd6dfd2072933f2e99382a50422ceb',
    '858.log': '6c3ab3e9a5887c2d90cf5f55c9ef55f2d7249209',
}
STAMP859 = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
ROOT859 = pathlib.Path('/content') / ('TEST859_FEEDBACK_DECISION_' + STAMP859)
ROOT859.mkdir(parents=True, exist_ok=False)
CONSOLE859 = sys.stdout
ERROR_CONSOLE859 = sys.stderr
LOG_FILE859 = open(ROOT859 / '859.log', 'w', encoding='utf-8')
START859 = time.perf_counter()
REAL_COMPILE859 = builtins.compile
RAW_SOURCES859 = {}
STATE859 = {
    'installed': False,
    'compiled': False,
    'equalities': [],
    'observations': [],
    'coverage': [],
    'frames': [],
    'g': None,
    'active': None,
    'capture': None,
    'tokenizations': {},
    'hook_audits': [],
    'saved_jobs': [],
    'invocations': [],
    'contexts': [],
    'transitions': {},
    'offline_functions': {},
    'decision_comparison': {},
    'causal_probes': [],
    'original_record_sha256': None,
    'environment': {},
    'start': START859,
}
FAILURES859 = []
EXECUTION_ERROR859 = None
OUTER_EXECUTION_ERROR859 = None
TRACEBACK859 = ''
ERROR_EVIDENCE859 = {}
LAST_CONTEXT859 = None
DIAGNOSTIC_STOP859 = None
TWO_JOB_VERIFICATION859 = {}
ANALYSIS859 = {}
PROBE_ERROR859 = None


class Gate1SmokeComplete859(Exception):
    """Explicit diagnostic control flow after two saved jobs; never model STOP."""


def short859(*args):
    text = ' '.join(str(x) for x in args)
    print(text, file=CONSOLE859, flush=True)
    LOG_FILE859.write(text + '\n')
    LOG_FILE859.flush()


def json_write859(name, value):
    path = ROOT859 / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
        allow_nan=False), encoding='utf-8')
    return path


def sha256_bytes859(data):
    return hashlib.sha256(data).hexdigest()


def git_blob859(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def load_sources859():
    # One archive fetch avoids treating transient raw-host resets as missing sources.
    request = urllib.request.Request(CODELOAD859,
        headers={'User-Agent': 'AKBASCORE-TEST859-GATE1'})
    with urllib.request.urlopen(request, timeout=240) as response:
        archive = response.read(100000001)
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        for name, expected in LOCKS859.items():
            matches = [member for member in zipped.namelist()
                if member.endswith('/' + name)]
            assert len(matches) == 1, ('SOURCE_MEMBER_NOT_UNIQUE', name, matches)
            data = zipped.read(matches[0])
            actual = git_blob859(data)
            assert actual == expected, ('SOURCE_LOCK_FAILED', name, actual, expected)
            RAW_SOURCES859[name] = data
            if name.endswith('.py'):
                REAL_COMPILE859(data.decode('utf-8'), name, 'exec')
            short859('GATE0 SOURCE', name, actual, 'PASS')
    assert len(RAW_SOURCES859) == 19


def capture_cell_source859():
    # Colab exposes the submitted cell through input history. If unavailable, do
    # not invent an 859.py artifact; the delivered .py file remains the source.
    try:
        shell = get_ipython()  # noqa: F821 — supplied by Colab/IPython.
        history = list(shell.history_manager.input_hist_raw)
        candidates = [text for text in history if
            'AKBASCORE SILICON HIPPOCAMPUS — TEST859 STATE TRANSFER AND FEEDBACK' in text]
        if candidates:
            (ROOT859 / '859.py').write_text(candidates[-1], encoding='utf-8')
            return True
    except Exception as exc:
        short859('859.py history capture unavailable:', type(exc).__name__, str(exc))
    return False


def current_job859(g):
    if not g:
        return {}
    job = g.get('j851') or g.get('j846') or {}
    return {
        'job': job.get('job'),
        'qid': g.get('q851', job.get('qid')),
        'condition': g.get('condition851', job.get('intervention')),
        'arm': g.get('arm851', job.get('arm')),
    }


def segment_metadata859(g, segments):
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
def runtime_context859(label, g=None, segments=None, pre=None, post=None):
    global LAST_CONTEXT859
    record = {
        'label': label,
        'time_offset_seconds': time.perf_counter() - START859,
        **current_job859(g),
        'segments': segment_metadata859(g, segments),
        'prefix_length': len(pre) if pre is not None else None,
        'suffix_length': len(post) if post is not None else None,
        'substep': None,
    }
    previous = STATE859.get('active')
    STATE859['active'] = record
    LAST_CONTEXT859 = record
    STATE859['contexts'].append({'event': 'ENTER', **record})
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
            'capture': STATE859.get('capture'),
        }
        FAILURES859.append(failure)
        raise
    finally:
        STATE859['active'] = previous


def hook_audit859(g, event):
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
        'time_offset_seconds': time.perf_counter() - START859,
        **current_job859(g),
        'transformers_output_capturing_installed': bool(getattr(
            g['model'], '_output_capturing_hooks_installed', False)),
        'hook_count': len(rows),
        'hooks': rows,
    }
    STATE859['hook_audits'].append(record)
    json_write859('859_hook_audit.json', STATE859['hook_audits'])
    return record


def assert_hook_free859(g, event):
    record = hook_audit859(g, event)
    if record['hook_count'] or record['transformers_output_capturing_installed']:
        raise RuntimeError('TEST859_FORWARD_HOOK_DETECTED: ' + event)
    return record


class Quiet859:
    def __init__(self):
        self.pending = ''

    def write(self, text):
        LOG_FILE859.write(text)
        LOG_FILE859.flush()
        self.pending += text
        while '\n' in self.pending:
            line, self.pending = self.pending.split('\n', 1)
            if 'TEST854 JOB-BY-JOB RESULTS|' in line:
                short859('JOB', line.split('TEST854 JOB-BY-JOB RESULTS|', 1)[1][:240])
        return len(text)

    def flush(self):
        LOG_FILE859.flush()

    def isatty(self):
        return False


SPELLINGS859 = (' CONTINUE', ' REVISE', ' STOP', ' SUFFICIENT', ' INSUFFICIENT')


def capture859(out, local):
    # Logits-only observation. Do not request hidden_states: Transformers v5
    # lazily installs persistent output-capturing forward hooks for that request.
    g = STATE859['g']
    logits = out.logits[0, -1].detach().float()
    sequence_length = int(out.logits.shape[1])
    step = len(STATE859['frames'])
    STATE859['capture'] = {
        **current_job859(g),
        'stage': None if not STATE859.get('active') else STATE859['active']['label'],
        'step': step,
        'logit_sequence_length': sequence_length,
        'logits_shape': list(logits.shape),
        'logits_dtype': str(logits.dtype),
        'logits_device': str(logits.device),
    }
    scores = logits[STATE859['first_ids']].cpu().tolist()
    record = {
        'step': step,
        'logit_sequence_length': sequence_length,
        'logits_shape': list(logits.shape),
        'logits_dtype': str(logits.dtype),
        'logits_device': str(logits.device),
        'returned_logits_bytes': out.logits.numel() * out.logits.element_size(),
        'tokenizations': STATE859['tokenizations'],
        'lens': 'diagnostic last-token logits, NOT action probabilities',
        'first_token_logits': dict(zip(SPELLINGS859, scores)),
        'stop_minus_revise': scores[2] - scores[1],
        'observation_scope': 'existing public logits only; hidden-state X-RAY disabled',
    }
    STATE859['frames'].append(record)


def clone_observer859(fn_node, g):
    node = copy.deepcopy(fn_node)
    original_name = node.name
    node.name = '_xr_' + original_name
    changed = 0

    class Observe859(ast.NodeTransformer):
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

    node = Observe859().visit(node)
    assert changed == 2, ('OBSERVATION_SITES', original_name, changed)
    module = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    # Reverse the observational delta and require exact AST equality.
    reverse = copy.deepcopy(node)
    reverse.name = original_name

    class Undo859(ast.NodeTransformer):
        def visit_Expr(self, n):
            if (isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
                    and n.value.func.id == '_xr_capture'):
                return None
            return self.generic_visit(n)

    reverse = Undo859().visit(reverse)
    assert ast.dump(reverse, include_attributes=False) == ast.dump(
        fn_node, include_attributes=False)
    if g is None:
        REAL_COMPILE859(module, 'TEST859_OBSERVER_STATIC', 'exec')
        return module
    exec(REAL_COMPILE859(module, 'TEST859_OBSERVER', 'exec'), g)
    return g[node.name]


def install859(g):
    assert not STATE859['installed']
    STATE859['installed'] = True
    STATE859['g'] = g
    torch = g['torch']
    np = g['np']
    assert g['NL'] == 80 and g['H'] == 8192 and g['DTYPE'] == torch.bfloat16
    assert len(g['JOBS841']) == 12 and not g['REC841'], 'Fresh run required; no unobserved resume'
    assert torch.cuda.device_count() == 1
    assert 'A100' in torch.cuda.get_device_name(0)
    assert not any(p.requires_grad for p in g['model'].parameters())
    assert_hook_free859(g, 'install_before_observation')
    transformers_module = g.get('transformers')
    STATE859['environment'] = {
        'torch_version': str(torch.__version__),
        'transformers_version': (None if transformers_module is None else
            str(getattr(transformers_module, '__version__', 'UNKNOWN'))),
        'hidden_states_requested': False,
        'observation': 'public out.logits only',
        'repair': 'remove output capture request; never clear hooks',
    }
    short859('GPU:', torch.cuda.get_device_name(0), '| frozen NF4 | BF16 | layers=80 H=8192',
        '| free GiB=', round(torch.cuda.mem_get_info()[0] / 1024 ** 3, 2))
    tokens = [list(g['tok'](s, add_special_tokens=False).input_ids) for s in SPELLINGS859]
    assert all(tokens)
    STATE859['tokenizations'] = dict(zip(SPELLINGS859, tokens))
    STATE859['first_ids'] = [value[0] for value in tokens]
    g['_xr_capture'] = capture859
    gen = g['gen851']
    observed = clone_observer859(STATE859['functions']['gen851'], g)
    inv = g['invoke851']
    gen_coverage = clone_observer859(STATE859['functions']['gen849'], g)
    old_coverage = g['coverage_state852']

    def observe_coverage(q, condition, mode, memx):
        fresh = (q, condition, mode) not in g['COVERAGE_SHARED852']
        h = old_coverage(q, condition, mode, memx)
        assert_hook_free859(g, 'coverage_original_return')
        if fresh:
            pre = list(g['prompt_ids'](g['COVERAGE852'].format(q=g['QTEXT841'][q])))
            with runtime_context859('coverage_replay', g, None, pre,
                    g['COVERAGE_SUFFIX852']) as active:
                STATE859['frames'] = []
                active['substep'] = 'observed_coverage_generator'
                obs = gen_coverage(memx, pre, None, g['COVERAGE_SUFFIX852'])
                assert_hook_free859(g, 'coverage_observed_return')
                same = (h['toks'] == obs['toks'] and h['text'] == obs['text']
                    and torch.equal(h['rows'], obs['rows']) and h['top1'] == obs['top1'])
                assert same, 'COVERAGE_OBSERVER_CHANGED_COMPUTATION'
    
                record = {
                    **current_job859(g),
                    'requested_qid': q,
                    'requested_condition': condition,
                    'requested_mode': mode,
                    'text': h['text'],
                    'tokens': h['trace849']['all_token_ids'],
                    'valid_protocol': h['text'].strip() in ('SUFFICIENT', 'INSUFFICIENT'),
                    'observer_equality': same,
                    'frames': STATE859['frames'],
                    'prefix_ids': pre,
                    'suffix_ids': list(g['COVERAGE_SUFFIX852']),
                }
                STATE859['coverage'].append(record)
        return h

    g['coverage_state852'] = observe_coverage

    def wrapped(memx, pre, segments, post, stage, tensors, traces, baseline=False):
        assert not baseline, 'Unexpected TEST854 path'
        with runtime_context859('invoke_' + stage, g, segments, pre, post) as active:
            torch.cuda.synchronize()
            begun = time.perf_counter()
            STATE859['frames'] = []
            # Budget guard for observational workload; never counted as model STOP.
            assert time.perf_counter() - STATE859['start'] < 3600, 'XRAY_MECHANICAL_TIME_LIMIT'
            checked = stage == 'review_0' and g['arm851'] == 'BASELINE853'
            active['substep'] = 'reference_generator' if checked else 'not_applicable'
            reference = gen(memx, pre, segments, post) if checked else None
            if checked:
                assert_hook_free859(g, 'reference_generator_return')
            g['gen851'] = observed
            try:
                active['substep'] = 'observed_generator'
                h = inv(memx, pre, segments, post, stage, tensors, traces, baseline=False)
            finally:
                g['gen851'] = gen
            assert_hook_free859(g, 'observed_generator_return')
            if checked:
                active['substep'] = 'runtime_equality'
                same = (h['toks'] == reference['toks'] and h['text'] == reference['text']
                    and torch.equal(h['rows'], reference['rows']) and h['top1'] == reference['top1'])
                STATE859['equalities'].append(bool(same))
                assert same, 'OBSERVER_CHANGED_NATIVE_COMPUTATION'
            identity = {
                **current_job859(g),
                'stage': stage,
            }
            index = len(STATE859['observations'])
            row = {
                **identity,
                'frames': STATE859['frames'],
                'input_segments': segment_metadata859(g, segments),
                'text': h['text'],
                'tokens': h['trace849']['all_token_ids'],
                'continuity': h['trace849']['continuity'],
                'prefix_ids': list(pre),
                'suffix_ids': list(post or []),
                'memory_tokens': int(memx[0][0].shape[-2]),
                'seconds_with_observation': time.perf_counter() - begun,
            }
            STATE859['observations'].append(row)
            STATE859['invocations'].append({
                **identity,
                'memx': memx,
                'pre': list(pre),
                'segments': [(list(slot), None if rows is None else rows.clone().cpu())
                    for slot, rows in segments],
                'post': list(post or []),
                'h': copy.deepcopy(h),
            })
            # Full observations remain in memory; only scientific summaries are delivered.
            return h

    g['invoke851'] = wrapped
    old_save = g['save_job841']
    expected_jobs = [j['job'] for j in g['JOBS841'][:2]]
    assert len(expected_jobs) == 2
    assert all(j['arm'] == 'BASELINE853' for j in g['JOBS841'][:2])

    def save_and_stop(job, record, tensors):
        result = old_save(job, record, tensors)
        STATE859['saved_jobs'].append(job)
        assert_hook_free859(g, 'job_saved_' + str(job))
        if STATE859['saved_jobs'] == expected_jobs:
            # REC841 and the native job artifact are already saved. The inherited
            # wrapper will preserve this explicit diagnostic exception verbatim.
            raise Gate1SmokeComplete859('GATE1_TWO_JOB_OBSERVATION_COMPLETE')
        assert len(STATE859['saved_jobs']) < len(expected_jobs), 'UNEXPECTED_JOB_ORDER'
        return result

    g['save_job841'] = save_and_stop
    short859('OBSERVER: logits-only AST inverse PASS; no hidden states; no hooks; two-job limit armed.')


def compile_xray859(source, filename, mode, *args, **kwargs):
    # Intercept only the final assembled CELL compile, before model loading.
    if filename == 'TEST849_CELL':
        assert not STATE859['compiled']
        STATE859['compiled'] = True
        tree = copy.deepcopy(source) if isinstance(source, ast.AST) else ast.parse(source)
        matches = [n for n in tree.body if isinstance(n, ast.Assign)
            and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
            and n.targets[0].id == 'BODY841']
        assert len(matches) == 1 and isinstance(matches[0].value, ast.Constant)
        body = matches[0].value.value
        bt = ast.parse(body)
        STATE859['functions'] = {n.name: n for n in bt.body if isinstance(n, ast.FunctionDef)}
        STATE859['offline_functions'] = {n.name: copy.deepcopy(n) for n in bt.body
            if isinstance(n, ast.FunctionDef) and n.name in ('node851','supported851')}
        assert {'gen849', 'gen851', 'invoke851'} <= STATE859['functions'].keys()
        for name in ('gen849', 'gen851'):
            clone_observer859(STATE859['functions'][name], None)
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
        STATE859['patch_manifest'] = {
            'base_body_sha256': sha256_bytes859(body.encode()),
            'instrumented_body_sha256': sha256_bytes859(patched.encode()),
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
        }
        matches[0].value = ast.Constant(patched)
        source = ast.fix_missing_locations(tree)
    return REAL_COMPILE859(source, filename, mode, *args, **kwargs)


def recover_inherited_error859(env, outer_exception, outer_trace):
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
        'context_failure_count': len(FAILURES859),
        'last_runtime_context': LAST_CONTEXT859,
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
        info['saved_traceback_sha256'] = sha256_bytes859(saved_text.encode('utf-8'))

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
            info['saved_exception_traceback_sha256'] = sha256_bytes859(
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


def reproduce_pre859859():
    quiet = Quiet859()
    env = {
        '__name__': '__main__',
        'compile': compile_xray859,
        '_xr_install': install859,
    }
    STATE859['start'] = time.perf_counter()
    outer_exception = None
    outer_trace = ''
    try:
        sys.stdout = quiet
        sys.stderr = quiet
        exec(REAL_COMPILE859(RAW_SOURCES859['854.py'].decode(),
            'LOCKED_TEST854', 'exec'), env)
    except BaseException as exc:
        outer_exception = exc
        # This usually contains only TEST849_FAILED: RuntimeError. The actual
        # RuntimeError is recovered below from the inherited wrapper globals.
        outer_trace = traceback.format_exc()
    finally:
        sys.stdout = CONSOLE859
        sys.stderr = ERROR_CONSOLE859
        quiet.flush()
    root_error, combined_trace, evidence = recover_inherited_error859(
        env, outer_exception, outer_trace)
    return env, root_error, combined_trace, evidence


def records_digest859(env):
    return sha256_bytes859(json.dumps(env.get('REC841', {}), sort_keys=True,
        ensure_ascii=False).encode('utf-8'))


def verify_two_job859(env, combined_trace):
    """Technical gate only: scientific termination is reported, never required."""
    jobs = env.get('JOBS841', [])
    records = env.get('REC841', {})
    expected = jobs[:2]
    expected_ids = [j['job'] for j in expected]
    assert len(expected) == 2
    assert [j['intervention'] for j in expected] == ['INTACT', 'REMOVED']
    assert all(j['arm'] == 'BASELINE853' for j in expected)
    assert STATE859['saved_jobs'] == expected_ids, (
        'TWO_JOB_SAVE_MISMATCH', STATE859['saved_jobs'], expected_ids)
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
    assert STATE859['equalities'] == [True, True], (
        'TWO_REVIEW_EQUALITIES_REQUIRED', STATE859['equalities'])
    assert all(c['observer_equality'] for c in STATE859['coverage'])
    assert not STATE859['causal_probes'], 'CAUSAL_PROBE_RAN_BEFORE_ORIGINAL_STREAM_END'
    final_audit = assert_hook_free859(env, 'post_diagnostic_stop_before_causal_replays')
    assert STATE859['hook_audits'] and all(
        row['hook_count'] == 0 and not row['transformers_output_capturing_installed']
        for row in STATE859['hook_audits'])
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
        'review_replay_equalities': STATE859['equalities'],
        'coverage_observer_equalities': [c['observer_equality'] for c in STATE859['coverage']],
        'hook_audits': len(STATE859['hook_audits']),
        'final_hook_count': final_audit['hook_count'],
        'diagnostic_stop': 'GATE1_TWO_JOB_OBSERVATION_COMPLETE',
        'diagnostic_stop_is_model_stop': False,
        'scope': 'Technical hook-free continuity/equivalence only; no ACCEPT/STOP requirement.',
    }


def clone_segments859(segments):
    return [(list(slot), None if rows is None else rows.clone().cpu())
        for slot, rows in segments]


def segment_map859(g, segments):
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


def replace_named_slot859(g, segments, name, rows):
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


def segments_sha859(segments):
    return sha256_bytes859(json.dumps([
        {'slot': list(slot), 'state': None if rows is None else
            {'shape': list(rows.shape), 'dtype': str(rows.dtype),
             'sha256': hashlib.sha256(rows.detach().cpu().numpy().tobytes()).hexdigest()}}
        for slot, rows in segments], sort_keys=True).encode('utf-8'))


def native_h_equal859(torch, a, b):
    return (a['toks'] == b['toks'] and a['text'] == b['text']
        and a['top1'] == b['top1'] and a['kend'] == b['kend']
        and torch.equal(a['rows'], b['rows']))


def h_summary859(g, h):
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


def score_actions859(g, memx, pre, segments, post):
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


def score_margins859(scores):
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


def find_invocation859(job, stage):
    rows = [x for x in STATE859['invocations']
        if x['job'] == job and x['stage'] == stage]
    assert len(rows) == 1, ('INVOCATION_SNAPSHOT_NOT_UNIQUE', job, stage, len(rows))
    return rows[0]


def state_metrics859(g, rows):
    torch = g['torch']
    x = rows.detach().cpu().float()
    return {
        'shape': list(x.shape), 'dtype': str(rows.dtype), 'device': str(rows.device),
        'norm': float(torch.linalg.vector_norm(x.reshape(-1))),
        'mean': float(x.mean()) if x.numel() else None,
        'std': float(x.std(unbiased=False)) if x.numel() else None,
        'finite': bool(torch.isfinite(x).all()),
        'sha256': g['stats849'](rows)['sha256'],
    }


def paired_metrics859(g, reference, value):
    torch = g['torch']
    a, b = reference.detach().cpu().float(), value.detach().cpu().float()
    out = {'reference_shape': list(a.shape), 'value_shape': list(b.shape),
           'exact': list(a.shape) == list(b.shape) and torch.equal(a, b)}
    if list(a.shape) != list(b.shape):
        out.update({'status': 'NOT_COMPARABLE_SHAPE', 'cosine': None, 'relative_l2': None})
        return out
    af, bf = a.reshape(-1), b.reshape(-1)
    an, bn = torch.linalg.vector_norm(af), torch.linalg.vector_norm(bf)
    out.update({'status': 'COMPARABLE', 'l2_delta': float(torch.linalg.vector_norm(af-bf)),
        'relative_l2': float(torch.linalg.vector_norm(af-bf) / an) if an > 0 else None,
        'cosine': float(torch.dot(af, bf) / (an*bn)) if an > 0 and bn > 0 else None,
        'reference_zero_norm': bool(an == 0), 'value_zero_norm': bool(bn == 0)})
    return out


def continuity_for_slot859(g, invocation, slot_ids):
    positions = [i for i, (slot, rows) in enumerate(invocation['segments'])
        if list(slot) == list(slot_ids)]
    if len(positions) != 1:
        return {'status': 'SLOT_NOT_UNIQUE', 'count': len(positions)}
    index = 0
    for slot, rows in invocation['segments'][:positions[0]]:
        if rows is not None and len(rows):
            index += 1
    segments = invocation['h']['trace849']['continuity']['segments']
    return segments[index] if index < len(segments) else {'status': 'NOT_RECORDED'}


def compatible_replacement859(g, reference, alternative):
    return (alternative is not None and reference.shape == alternative.shape
        and reference.dtype == alternative.dtype and reference.device == alternative.device
        and reference.device.type == 'cpu' and reference.dtype == g['torch'].float32)


def score_deltas859(reference, value):
    ref = {x['spelling'].strip(): x for x in reference}
    val = {x['spelling'].strip(): x for x in value}
    return {name: {'sequence_logp_delta': val[name]['sequence_logp']-ref[name]['sequence_logp'],
        'mean_token_logp_delta': val[name]['mean_token_logp']-ref[name]['mean_token_logp'],
        'first_token_logit_delta': val[name]['first_token_logit']-ref[name]['first_token_logit']}
        for name in ('CONTINUE','REVISE','STOP')}


def probe859(env, snapshots, variant, replacement=None, candidate_swap=False):
    """One matched post-hoc replay; no result is returned to the original engine."""
    torch = env['torch']
    pre, review = snapshots['pre1'], snapshots['review1']
    original_pre_segments = clone_segments859(pre['segments'])
    original_decision = clone_segments859(review['segments'])
    pm = segment_map859(env, original_pre_segments)
    dm = segment_map859(env, original_decision)
    pre_segments = clone_segments859(original_pre_segments)
    C, E = pm['C'][1], pm['E'][1]
    current_R = pm['R'][1]
    if variant == 'KPREV_SWAP':
        assert replacement is not None
        pre_segments = replace_named_slot859(env, pre_segments, 'Kprev', replacement)
    elif variant == 'CANDIDATE_CARRY_SWAP_TO_C0':
        assert replacement is not None
        pre_segments = replace_named_slot859(env, pre_segments, 'C', replacement)
        new_R = env['relation852'](replacement, E)
        pre_segments = replace_named_slot859(env, pre_segments, 'R', new_R)
        C = replacement
        current_R = new_R
    else:
        assert variant in ('ORIGINAL','KPREV_ORIGINAL_RESTORE') and replacement is None
    before = segments_sha859(original_pre_segments)
    pre_h = env['gen851'](pre['memx'], list(pre['pre']), pre_segments, list(pre['post']))
    J = env['interaction854'](C, E, pre_h['rows'])
    final_segments = [(list(env['K_SLOT854']), pre_h['rows']),
                      (list(env['J_SLOT854']), J)]
    review_h = env['gen851'](review['memx'], list(review['pre']), final_segments,
                             list(review['post']))
    scores = score_actions859(env, review['memx'], list(review['pre']), final_segments,
                              list(review['post']))
    exact_replay = (native_h_equal859(torch, pre_h, pre['h'])
        and native_h_equal859(torch, review_h, review['h'])
        and segments_sha859(final_segments) == segments_sha859(original_decision))
    if variant in ('ORIGINAL','KPREV_ORIGINAL_RESTORE'):
        assert exact_replay, ('ORIGINAL_OR_RESTORE_NOT_EXACT', variant)
    else:
        assert segments_sha859(pre_segments) != before, ('EMPTY_INTERVENTION', variant)
    if variant == 'ORIGINAL':
        original_scores = scores
        snapshots['original_action_scores'] = scores
    else:
        original_scores = snapshots['original_action_scores']
    if variant == 'KPREV_ORIGINAL_RESTORE':
        assert scores == original_scores, 'RESTORE_ACTION_SCORES_NOT_EXACT'
    action = env['parse849'](review_h['text'])
    original_action = env['parse849'](review['h']['text'])
    differences = {
        'precontrol': paired_metrics859(env, pre['h']['rows'], pre_h['rows']),
        'J': paired_metrics859(env, dm['J'][1], J),
        'review': paired_metrics859(env, review['h']['rows'], review_h['rows']),
    }
    snapshots.setdefault('_runtime', {})[variant] = {
        'pre_h': pre_h, 'review_h': review_h, 'C': C, 'E': E, 'R': current_R, 'J': J}
    row = {'variant': variant, 'status': 'DONE',
        'candidate_swap_recomputes_R_and_gate': candidate_swap,
        'original_action': original_action, 'diagnostic_action': action,
        'diagnostic_action_changed': action != original_action,
        'diagnostic_action_is_not_original_job_action': True,
        'exact_original_or_restore': exact_replay if variant in ('ORIGINAL','KPREV_ORIGINAL_RESTORE') else None,
        'precontrol': h_summary859(env, pre_h), 'review': h_summary859(env, review_h),
        'K0': state_metrics859(env, pre_h['rows']), 'J': state_metrics859(env, J),
        'state_differences_from_original': differences,
        'action_scores': scores, 'margins': score_margins859(scores),
        'score_deltas_from_original': score_deltas859(original_scores, scores),
        'replacement_source': None if replacement is None else state_metrics859(env, replacement),
        'original_precontrol_input_sha256': before,
        'probe_precontrol_input_sha256': segments_sha859(pre_segments),
        'final_decision_input_sha256': segments_sha859(final_segments)}
    STATE859['causal_probes'].append(row)
    json_write859('859_causal_probes.json', STATE859['causal_probes'])
    short859('CAUSAL', variant, 'original', original_action, 'diagnostic', action,
        'STOP-REVISE', row['margins']['stop_minus_revise_sequence_logp'],
        'precontrol_exact', differences['precontrol']['exact'],
        'review_exact', differences['review']['exact'])
    return row


def install_offline_evaluator859(env):
    functions = STATE859['offline_functions']
    assert set(functions) == {'node851','supported851'}
    module = ast.fix_missing_locations(ast.Module(body=[copy.deepcopy(functions[n])
        for n in ('node851','supported851')], type_ignores=[]))
    digest = sha256_bytes859(ast.dump(module, include_attributes=False).encode())
    exec(REAL_COMPILE859(module, 'TEST859_LOCKED_OFFLINE_EVALUATORS_ONLY', 'exec'), env)
    assert callable(env['node851']) and callable(env['supported851'])
    short859('OFFLINE EVALUATOR: locked node851/supported851 only; AST-SHA256', digest,
             'loaded after original jobs; no answer key entered native prompts.')
    return digest


def evidence_context859(env, job, record):
    wi = env['QID841'].index(job['qid'])
    world = env['worlds829'][wi]
    mounted = set(record['mounted_cards'])
    sufficient = world['ids']['first'] in mounted and bool(
        {world['ids']['second'],world['ids']['changed']} & mounted)
    return world, mounted, sufficient


def original_quality859(env, job, record):
    world, mounted, sufficient = evidence_context859(env, job, record)
    node, supported = env['node851'], env['supported851']
    initial = record['initial']['text']
    answer = None if record.get('answer') is None else record['answer']['text']
    initial_grounded = supported(initial, world, mounted)
    grounded = supported(answer, world, mounted)
    initial_wrong = node(initial, world) in (
        'start','middle','fork_end','decoy_end','bridge_mid','bridge_end','end3')
    revisions = [c['revision'] for c in record['cycles'] if c.get('revision') is not None]
    revision_grounded = any(supported(r['text'],world,mounted) for r in revisions)
    correction_opportunity = initial_wrong and sufficient
    correction = bool(correction_opportunity and grounded and record['end']=='MODEL_ACCEPT'
        and any(c['action']=='REVISE' and c.get('revision') is not None
            and supported(c['revision']['text'],world,mounted) for c in record['cycles']))
    preservation = bool(record['initial_mode']=='NATURAL' and sufficient and initial_grounded
        and grounded and record['end']=='MODEL_ACCEPT'
        and not any(c['action']=='REVISE' for c in record['cycles']))
    unsupported = bool(answer is not None and answer.strip() and node(answer,world)!='UNKNOWN'
        and not grounded)
    metrics = {'grounded_answer': grounded, 'unsupported_answer_avoided': not unsupported}
    if sufficient and record['initial_mode']=='NATURAL':
        metrics['correct_preservation'] = preservation
    if correction_opportunity:
        metrics['correction'] = correction
    if not sufficient:
        metrics['correct_stop'] = record['end']=='MODEL_STOP'
        metrics['unknown_when_insufficient'] = any(
            r['text'].strip().upper()=='UNKNOWN' for r in revisions)
    if revisions:
        metrics['revision_grounded'] = revision_grounded
    return {'job':job['job'],'condition':job['intervention'],'execution':'ORIGINAL_NATIVE',
        'mounted_cards':list(record['mounted_cards']),
        'initial':initial,'answer':answer,'actions':[c['action'] for c in record['cycles']],
        'revisions':[r['text'] for r in revisions],'end':record['end'],
        'sufficient':sufficient,'initial_grounded':initial_grounded,'grounded':grounded,
        'initial_wrong':initial_wrong,'correction_opportunity':correction_opportunity,
        'correction':correction if correction_opportunity else None,
        'preservation':preservation,'unnecessary_revision':initial_grounded and bool(revisions),
        'revision_grounded':revision_grounded,'unsupported_completion':unsupported,
        'model_stop':record['end']=='MODEL_STOP',
        'mechanical_limit':record['end']=='MECHANICAL_REVIEW_LIMIT',
        'research_request':'NOT_IMPLEMENTED_NO_NEW_SOURCE_OR_ADDRESS_ACTION',
        'revision_behavior':any(c['action']=='REVISE' for c in record['cycles']),
        'quality_metrics':metrics}


def attach_revision859(env, job, snapshots, variant, row):
    """Reuse the existing native revision path; only diagnostic controls generate anew."""
    record = env['REC841'][job['job']]
    original = find_invocation859(job['job'],'revision_1')
    if variant == 'ORIGINAL':
        h = original['h']
    else:
        rt = snapshots['_runtime'][variant]
        if row['diagnostic_action'] != 'REVISE':
            row.update({'revision':None,'diagnostic_revision_state_difference':None,
                'diagnostic_end':'DIAGNOSTIC_'+row['diagnostic_action'],
                'diagnostic_stop_action':row['diagnostic_action']=='STOP',
                'native_model_stop':False})
            return h if variant=='KPREV_ORIGINAL_RESTORE' else None
        pre = list(env['prompt_ids'](env['RECOMPUTE851'].format(q=env['QTEXT841'][job['qid']])))
        segments = [(list(env['C_SLOT851']),rt['C']),
            (list(env['K_SLOT851']),rt['review_h']['rows']),
            (list(env['E_SLOT851']),rt['E']), (list(env['U_SLOT852']),
                segment_map859(env,snapshots['pre1']['segments'])['U'][1]),
            (list(env['R_SLOT852']),rt['R'])]
        h = env['gen851'](snapshots['review1']['memx'],pre,segments,
            list(env['ANSWER_SUFFIX851']))
        if variant == 'KPREV_ORIGINAL_RESTORE':
            assert native_h_equal859(env['torch'],h,original['h']), 'RESTORE_REVISION_NOT_EXACT'
    row['revision'] = h_summary859(env,h)
    row['diagnostic_revision_state_difference'] = paired_metrics859(env,original['h']['rows'],h['rows'])
    row['diagnostic_end'] = (record['end'] if variant=='ORIGINAL' else
        'DIAGNOSTIC_REPLAY_REVISE_THEN_EXISTING_CYCLE1_LIMIT')
    row['diagnostic_stop_action'] = row['diagnostic_action']=='STOP'
    row['native_model_stop'] = variant=='ORIGINAL' and record['end']=='MODEL_STOP'
    return h


def replay_quality859(env, job, row):
    record = env['REC841'][job['job']]
    world,mounted,sufficient = evidence_context859(env,job,record)
    node,supported = env['node851'],env['supported851']
    revision = None if row.get('revision') is None else row['revision']['text']
    action = row['diagnostic_action']
    candidate = (record['cycles'][0]['candidate']['text']
        if row['variant']=='CANDIDATE_CARRY_SWAP_TO_C0' else record['cycles'][1]['candidate']['text'])
    answer = candidate if action=='CONTINUE' else None
    grounded = supported(answer,world,mounted)
    unsupported = bool(answer is not None and answer.strip() and node(answer,world)!='UNKNOWN'
        and not grounded)
    metrics = {'grounded_answer':grounded,'unsupported_answer_avoided':not unsupported}
    if not sufficient:
        metrics['correct_stop'] = action=='STOP'
        metrics['unknown_when_insufficient'] = bool(
            (revision and revision.strip().upper()=='UNKNOWN') or
            (answer and answer.strip().upper()=='UNKNOWN'))
    if revision is not None:
        metrics['revision_grounded'] = supported(revision,world,mounted)
    return {'job':job['job'],'condition':job['intervention'],'execution':'DIAGNOSTIC_REPLAY',
        'arm':row.get('arm',row['variant']),'action':action,'candidate':candidate,'revision':revision,
        'answer':answer,'end':row['diagnostic_end'],'sufficient':sufficient,
        'grounded':grounded,'unsupported_completion':unsupported,
        'correct_stop':action=='STOP' and not sufficient,
        'false_stop':action=='STOP' and sufficient,
        'research_request':'NOT_IMPLEMENTED_REVISION_IS_NOT_NEW_SOURCE_SELECTION',
        'native_model_stop':False,'quality_metrics':metrics}


def native_dominates859(native, control):
    common = sorted(set(native['quality_metrics']) & set(control['quality_metrics']))
    assert common, 'NO_COMMON_PREREGISTERED_EVIDENCE_METRIC'
    better = [k for k in common if bool(native['quality_metrics'][k]) > bool(control['quality_metrics'][k])]
    worse = [k for k in common if bool(native['quality_metrics'][k]) < bool(control['quality_metrics'][k])]
    return {'common_metrics':common,'native_better':better,'native_worse':worse,
        'native_dominates':bool(better) and not worse}


def classify859(row):
    differences = row['state_differences_from_original']
    numeric = any(not differences[k]['exact'] for k in ('precontrol','J','review'))
    numeric = numeric or any(abs(x['sequence_logp_delta'])>0
        for x in row['score_deltas_from_original'].values())
    if row.get('intervention_state_differences'):
        numeric = numeric or any(not x['exact'] for x in row['intervention_state_differences'].values())
    original_revision = row['original_revision_text']
    revision = None if row.get('revision') is None else row['revision']['text']
    behavior = row['diagnostic_action_changed'] or revision != original_revision
    aligned = row['evidence_dominance']['native_dominates']
    label = 'D_EVIDENCE_ALIGNED_BEHAVIORAL_CONTRIBUTION' if behavior and aligned else (
        'C_BEHAVIORAL_EFFECT' if behavior else 'B_NUMERICAL_EFFECT' if numeric else 'A_NO_EFFECT')
    return {'numerical_effect':numeric,'behavioral_effect':behavior,
        'behavioral_reason':{'action_changed':row['diagnostic_action_changed'],
            'revision_text_changed':revision!=original_revision},
        'evidence_aligned_native_contribution':aligned,'class':label}


def transport859(env, job):
    review0 = find_invocation859(job['job'],'review_0')
    revision0 = find_invocation859(job['job'],'revision_0')
    pre1 = find_invocation859(job['job'],'precontrol_1')
    pm = segment_map859(env,pre1['segments'])
    torch = env['torch']
    rows = [
        {'path':'review_0.rows -> previous_control851 -> cycle1.Kprev',
         'source_sha256':state_metrics859(env,review0['h']['rows'])['sha256'],
         'destination_sha256':state_metrics859(env,pm['Kprev'][1])['sha256'],
         'exact':torch.equal(review0['h']['rows'],pm['Kprev'][1]),
         'bf16':continuity_for_slot859(env,pre1,env['K_SLOT851'])},
        {'path':'revision_0.rows -> current851 -> cycle1.C',
         'source_sha256':state_metrics859(env,revision0['h']['rows'])['sha256'],
         'destination_sha256':state_metrics859(env,pm['C'][1])['sha256'],
         'exact':torch.equal(revision0['h']['rows'],pm['C'][1]),
         'bf16':continuity_for_slot859(env,pre1,env['C_SLOT851'])}]
    assert all(x['exact'] for x in rows), 'ORIGINAL_TRANSFER_SOURCE_MISMATCH'
    return rows


def run_analysis859(env):
    original_digest = records_digest859(env)
    STATE859['original_record_sha256'] = original_digest
    jobs = env['JOBS841'][:2]
    assert [j['intervention'] for j in jobs] == ['INTACT','REMOVED']
    assert not any(j['intervention']=='CONTRADICTED' for j in env['JOBS841'])
    original = {j['intervention']:original_quality859(env,j,env['REC841'][j['job']]) for j in jobs}
    for native_job in jobs:
        cycle_scores = []
        for cycle in env['REC841'][native_job['job']]['cycles']:
            if native_job['intervention']=='REMOVED' and cycle['cycle']==1:
                continue  # filled from ORIGINAL without a duplicate scoring forward
            invocation = find_invocation859(native_job['job'],'review_%d' % cycle['cycle'])
            scores = score_actions859(env,invocation['memx'],list(invocation['pre']),
                clone_segments859(invocation['segments']),list(invocation['post']))
            cycle_scores.append({'cycle':cycle['cycle'],'action':cycle['action'],
                'scores':scores,'margins':score_margins859(scores)})
        original[native_job['intervention']]['cycle_scores'] = cycle_scores
    job = jobs[1];record = env['REC841'][job['job']]
    assert [c['action'] for c in record['cycles']]==['REVISE','REVISE']
    transfers = transport859(env,job)
    snapshots = {name:find_invocation859(job['job'],stage) for name,stage in (
        ('pre0','precontrol_0'),('pre1','precontrol_1'),
        ('review0','review_0'),('review1','review_1'),('revision0','revision_0'))}
    original_revision = find_invocation859(job['job'],'revision_1')['h']['text']
    rows = [probe859(env,snapshots,'ORIGINAL')]
    attach_revision859(env,job,snapshots,'ORIGINAL',rows[0])
    rows[0].update({'execution':'ORIGINAL_NATIVE','arm':'NATIVE_FEEDBACK','original_revision_text':original_revision,
        'quality':original['REMOVED'],'class':'REFERENCE_NOT_AN_INTERVENTION'})
    original['REMOVED']['cycle_scores'].append({'cycle':1,'action':record['cycles'][1]['action'],
        'scores':rows[0]['action_scores'],'margins':rows[0]['margins']})
    for condition, quality in original.items():
        short859('TABLE A ORIGINAL',quality)

    kprev = segment_map859(env,snapshots['pre1']['segments'])['Kprev'][1]
    alternative = find_invocation859(jobs[0]['job'],'review_0')['h']['rows']
    assert compatible_replacement859(env,kprev,alternative), 'LOCKED_858_KPREV_SWAP_NO_LONGER_MATCHED'
    krow = probe859(env,snapshots,'KPREV_SWAP',alternative)
    krow['arm'] = 'KPREV_CONTROL'
    krow['replacement_source'] = {'job':jobs[0]['job'],'condition':'INTACT','stage':'review_0',
        'role':'native review soft-row output',**state_metrics859(env,alternative)}
    krow['intervention_state_differences'] = {'Kprev':paired_metrics859(env,kprev,alternative),
        'C':paired_metrics859(env,segment_map859(env,snapshots['pre1']['segments'])['C'][1],
            segment_map859(env,snapshots['pre1']['segments'])['C'][1])}
    attach_revision859(env,job,snapshots,'KPREV_SWAP',krow)

    c0 = segment_map859(env,snapshots['pre0']['segments'])['C'][1]
    c1 = segment_map859(env,snapshots['pre1']['segments'])['C'][1]
    assert compatible_replacement859(env,c1,c0), 'LOCKED_858_CARRY_SWAP_NO_LONGER_MATCHED'
    crow = probe859(env,snapshots,'CANDIDATE_CARRY_SWAP_TO_C0',c0,True)
    crow['arm'] = 'CARRY_CONTROL'
    crow['replacement_source'] = {'job':job['job'],'stage':'precontrol_0.C',
        'role':'previous native candidate soft-row',**state_metrics859(env,c0)}
    crow['intervention_state_differences'] = {'Kprev':paired_metrics859(env,kprev,kprev),
        'C':paired_metrics859(env,c1,c0)}
    attach_revision859(env,job,snapshots,'CANDIDATE_CARRY_SWAP_TO_C0',crow)

    # Restore the complete reference, including the second native revision.
    restore = probe859(env,snapshots,'KPREV_ORIGINAL_RESTORE')
    attach_revision859(env,job,snapshots,'KPREV_ORIGINAL_RESTORE',restore)
    restore.update({'execution':'DIAGNOSTIC_RESTORE','arm':'REFERENCE_RESTORE','original_revision_text':original_revision})
    rows.extend([krow,crow,restore])
    for row in (krow,crow):
        row['execution'] = 'DIAGNOSTIC_REPLAY'
        row['original_revision_text'] = original_revision
        row['quality'] = replay_quality859(env,job,row)
        row['evidence_dominance'] = native_dominates859(original['REMOVED'],row['quality'])
        row['classification'] = classify859(row)
        short859('TABLE B/C FEEDBACK',row['arm'],'action',row['diagnostic_action'],
            'revision',None if row.get('revision') is None else row['revision']['text'],
            'margin',row['margins'],'intervention_states',row['intervention_state_differences'],
            'states',row['state_differences_from_original'])
        short859('TABLE D/E QUALITY',row['variant'],row['quality'],row['classification'])

    assert records_digest859(env)==original_digest, 'DIAGNOSTICS_CHANGED_ORIGINAL_RECORDS'
    assert_hook_free859(env,'post_TEST859_replays')
    assert not any(p.requires_grad for p in env['model'].parameters())
    # Save only small diagnostic tensors; original tensors already reside in locked job NPZs.
    arrays = {}
    for label,row in (('KPREV_SWAP',krow),('CARRY_CONTROL',crow)):
        rt = snapshots['_runtime'][row['variant']]
        for name,h in (('precontrol',rt['pre_h']),('review',rt['review_h'])):
            arrays[label+'_'+name] = h['rows'].numpy().copy()
        arrays[label+'_J'] = rt['J'].numpy().copy()
    env['np'].savez_compressed(ROOT859/'859_tensors.npz',**arrays)
    comparisons = {'scope':{'native_jobs':2,'native_conditions':['INTACT','REMOVED'],
            'contradicted':'NOT_SUPPORTED_BY_LOCKED_PANEL_NOT_FABRICATED',
            'intact_controls':'NOT_APPLICABLE_NO_NATURAL_CYCLE1_AFTER_MODEL_ACCEPT',
            'removed_controls':'DIAGNOSTIC_REPLAY_NOT_NEW_CLOSED_LOOP_RUNS'},
        'original_quality':original,'transfers':transfers,
        'comparisons':[{'variant':r['variant'],'arm':r.get('arm'),'execution':r['execution'],
            'original_action':r['original_action'],'diagnostic_action':r['diagnostic_action'],
            'revision':None if r.get('revision') is None else r['revision']['text'],
            'end':r['diagnostic_end'],'margins':r['margins'],
            'quality':r.get('quality'),'evidence_dominance':r.get('evidence_dominance'),
            'classification':r.get('classification')} for r in rows]}
    intact_na = [{'job':jobs[0]['job'],'condition':'INTACT','arm':arm,
        'execution':'NOT_APPLICABLE','reason':'MODEL_ACCEPT_AT_CYCLE0_NO_NATURAL_CYCLE1',
        'classification':{'class':'NOT_APPLICABLE_NO_NATURAL_CYCLE1'}}
        for arm in ('KPREV_CONTROL','CARRY_CONTROL')]
    comparisons['comparisons'].extend(intact_na)
    json_write859('859_decision_comparison.json',comparisons)
    json_write859('859_causal_feedback.json',rows)
    counts = {letter:sum(r.get('classification',{}).get('class','').startswith(letter+'_')
        for r in rows) for letter in 'ABCD'}
    result = {'status':'PASS_DIAGNOSTIC_NOT_CLOSED_LOOP_IMPROVEMENT_PROOF',
        'original_records_unchanged':True,'restore_including_revision_exact':True,
        'class_counts':counts,'evidence_aligned_improvement_observed':counts['D']>0,
        'kprev_comparison':krow['classification'],'carry_comparison':crow['classification'],
        'paths_have_different_behavioral_effects':(
            (krow['diagnostic_action'],None if krow.get('revision') is None else krow['revision']['text']) !=
            (crow['diagnostic_action'],None if crow.get('revision') is None else crow['revision']['text'])),
        'native_preservation_intact':original['INTACT']['preservation'],
        'removed_reassessment':{'actions':original['REMOVED']['actions'],
            'revisions':original['REMOVED']['revisions'],'research_request':original['REMOVED']['research_request']},
        'native_stop_conditions':[c for c,q in original.items() if q['model_stop']],
        'same_action_with_different_numeric_state':any(r.get('classification',{}).get('class','').startswith('B_') for r in rows),
        'correction_scope':'NOT_EVALUABLE_NO_CONTRADICTED_OR_SUPPORTED_WRONG_INITIAL_CONDITION'}
    short859('TABLE E AGGREGATE',result)
    return result


def write_partial859():
    if not (ROOT859/'859_decision_comparison.json').exists():
        json_write859('859_decision_comparison.json',STATE859.get('decision_comparison',{}))
    if not (ROOT859/'859_causal_feedback.json').exists():
        json_write859('859_causal_feedback.json',STATE859['causal_probes'])


def finalize859(gates,execution):
    write_partial859();capture_cell_source859()
    report = {'test':TEST859_KIND,'execution':execution,'gates':gates,
        'technical_result':'TECHNICAL_DIAGNOSTIC_PASS' if all(gates.get(k)=='PASS' for k in (
            'GATE0_SOURCE_INTEGRITY','GATE1_HOOKFREE_ORIGINAL_TWO_JOBS','GATE2_OBSERVER_EQUIVALENCE',
            'GATE3_ORIGINAL_RECORDS_AND_TRANSPORT','GATE4_MATCHED_FEEDBACK_AND_RESTORE')) else 'TECHNICAL_DIAGNOSTIC_NOT_PASSED',
        'behavioral_result':'EVIDENCE_ALIGNED_DECISION_IMPROVEMENT' if ANALYSIS859.get(
            'evidence_aligned_improvement_observed') else 'EVIDENCE_ALIGNED_DECISION_IMPROVEMENT_NOT_DEMONSTRATED',
        'original_error':EXECUTION_ERROR859,'analysis_error':PROBE_ERROR859,
        'diagnostic_stop':DIAGNOSTIC_STOP859,'diagnostic_stop_is_model_stop':False,
        'technical_verification':TWO_JOB_VERIFICATION859,'analysis':ANALYSIS859,
        'source_lock_count':len(RAW_SOURCES859),'environment':STATE859['environment'],
        'observer_equalities':STATE859['equalities'],
        'coverage_observer_equalities':[c['observer_equality'] for c in STATE859['coverage']],
        'seconds':time.perf_counter()-START859,
        'limitations':['Two original jobs; no contradicted condition and no generalization claim.',
            'INTACT has no natural cycle1; no second cycle was forced.',
            'Control actions/revisions are DIAGNOSTIC_REPLAY, not new original closed-loop outcomes.',
            'Teacher-forced scores are not calibrated probabilities.',
            'REVISE is revision behavior, not new-source research; UNKNOWN is not STOP.',
            'Numerical or behavioral feedback effects do not alone prove evidence-aligned improvement.'],
        'TEST859_NEW_ENGINE':False,'TEST859_LOOP_REPAIR_ESTABLISHED':False}
    json_write859('859_report.json',report)
    short859('TEST859 TECHNICAL',report['technical_result'])
    short859('TEST859 BEHAVIORAL',report['behavioral_result'])
    for name,status in gates.items():short859(name,status)
    short859('ARTIFACTS',ROOT859);LOG_FILE859.flush()
    manifest={}
    for path in sorted(ROOT859.rglob('*')):
        if path.is_file() and path.name!='859_sha256_manifest.json':
            manifest[str(path.relative_to(ROOT859))]={'bytes':path.stat().st_size,
                'sha256':sha256_bytes859(path.read_bytes())}
    json_write859('859_sha256_manifest.json',manifest)


try:
    short859('TEST859: two native jobs; matched REMOVED diagnostic feedback; independent offline quality.')
    short859('GPU EXECUTION: NOT VERIFIED BY AUTHOR; restart Colab before this cell.')
    load_sources859();gate0='PASS'
    env859,error859,trace859,evidence859=reproduce_pre859859()
    EXECUTION_ERROR859,TRACEBACK859,ERROR_EVIDENCE859=error859,trace859,evidence859
    OUTER_EXECUTION_ERROR859=evidence859.get('outer_exception')
    if trace859:short859(trace859[-12000:])
    if 'GATE1_TWO_JOB_OBSERVATION_COMPLETE' in trace859:
        DIAGNOSTIC_STOP859='GATE1_TWO_JOB_OBSERVATION_COMPLETE'
    try:
        TWO_JOB_VERIFICATION859=verify_two_job859(env859,trace859)
        EXECUTION_ERROR859=None;gate1=gate2='PASS'
    except Exception as exc:
        EXECUTION_ERROR859=type(exc).__name__+': '+str(exc)
        gate1=gate2='BLOCKED';short859(traceback.format_exc())
    if gate1=='PASS':
        try:
            install_offline_evaluator859(env859)
            ANALYSIS859=run_analysis859(env859);gate3=gate4='PASS'
            execution='FEEDBACK_DECISION_DIAGNOSTIC_COMPLETE'
        except BaseException as exc:
            PROBE_ERROR859=type(exc).__name__+': '+str(exc)
            TRACEBACK859+='\n===== TEST859 ANALYSIS FAILURE =====\n'+traceback.format_exc()
            short859(traceback.format_exc());gate3=gate4='BLOCKED'
            execution='ANALYSIS_INCOMPLETE_FULL_TRACEBACK_IN_LOG'
    else:
        gate3=gate4='BLOCKED';execution='TWO_JOB_TECHNICAL_VERIFICATION_FAILED'
    gates={'GATE0_SOURCE_INTEGRITY':gate0,'GATE1_HOOKFREE_ORIGINAL_TWO_JOBS':gate1,
        'GATE2_OBSERVER_EQUIVALENCE':gate2,'GATE3_ORIGINAL_RECORDS_AND_TRANSPORT':gate3,
        'GATE4_MATCHED_FEEDBACK_AND_RESTORE':gate4,
        'GATE5_EVIDENCE_ALIGNED_IMPROVEMENT':'OBSERVED' if ANALYSIS859.get(
            'evidence_aligned_improvement_observed') else 'NOT_DEMONSTRATED',
        'GATE6_INDEPENDENT_GENERALIZATION':'BLOCKED_TWO_JOB_DIAGNOSTIC_ONLY',
        'GATE7_ARTIFACT_INTEGRITY':'PASS'}
    finalize859(gates,execution)
except BaseException as exc:
    EXECUTION_ERROR859=type(exc).__name__+': '+str(exc)
    sys.stdout,sys.stderr=CONSOLE859,ERROR_CONSOLE859;short859(traceback.format_exc())
    gates={'GATE0_SOURCE_INTEGRITY':'PASS' if len(RAW_SOURCES859)==19 else 'FAIL',
        'GATE1_HOOKFREE_ORIGINAL_TWO_JOBS':'BLOCKED','GATE2_OBSERVER_EQUIVALENCE':'BLOCKED',
        'GATE3_ORIGINAL_RECORDS_AND_TRANSPORT':'BLOCKED','GATE4_MATCHED_FEEDBACK_AND_RESTORE':'BLOCKED',
        'GATE5_EVIDENCE_ALIGNED_IMPROVEMENT':'BLOCKED',
        'GATE6_INDEPENDENT_GENERALIZATION':'BLOCKED','GATE7_ARTIFACT_INTEGRITY':'PASS'}
    finalize859(gates,'TEST859_FAILURE_FULL_TRACEBACK_IN_LOG')
finally:
    LOG_FILE859.close()
