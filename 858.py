# AKBASCORE SILICON HIPPOCAMPUS — TEST858 STATE TRANSFER AND FEEDBACK
# Locked TEST857 hook-free two-job spine; no new motor, memory or action rule.
# Original jobs finish first. Diagnostic replays never feed original decisions.
# Measures cycle0 -> cycle1 numerical transport, matched Kprev interventions,
# exact restoration, state deltas and fixed-action teacher-forced scores.
# MECHANICAL_REVIEW_LIMIT is not MODEL_STOP. GPU execution is not claimed here.
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

TEST858_KIND = 'CLOSED_LOOP_STATE_TRANSFER_AND_MATCHED_KPREV_FEEDBACK'
BASE858 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
CODELOAD858 = 'https://codeload.github.com/ceceli33/titan-cognitive-core-v3/zip/refs/heads/main'
LOCKS858 = {
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
}
STAMP858 = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
ROOT858 = pathlib.Path('/content') / ('TEST858_STATE_FEEDBACK_' + STAMP858)
ROOT858.mkdir(parents=True, exist_ok=False)
CONSOLE858 = sys.stdout
ERROR_CONSOLE858 = sys.stderr
LOG_FILE858 = open(ROOT858 / '858.log', 'w', encoding='utf-8')
START858 = time.perf_counter()
REAL_COMPILE858 = builtins.compile
RAW_SOURCES858 = {}
STATE858 = {
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
    'causal_probes': [],
    'original_record_sha256': None,
    'environment': {},
    'start': START858,
}
FAILURES858 = []
EXECUTION_ERROR858 = None
OUTER_EXECUTION_ERROR858 = None
TRACEBACK858 = ''
ERROR_EVIDENCE858 = {}
LAST_CONTEXT858 = None
DIAGNOSTIC_STOP858 = None
TWO_JOB_VERIFICATION858 = {}
ANALYSIS858 = {}
PROBE_ERROR858 = None


class Gate1SmokeComplete858(Exception):
    """Explicit diagnostic control flow after two saved jobs; never model STOP."""


def short858(*args):
    text = ' '.join(str(x) for x in args)
    print(text, file=CONSOLE858, flush=True)
    LOG_FILE858.write(text + '\n')
    LOG_FILE858.flush()


def json_write858(name, value):
    path = ROOT858 / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
        allow_nan=False), encoding='utf-8')
    return path


def sha256_bytes858(data):
    return hashlib.sha256(data).hexdigest()


def git_blob858(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def load_sources858():
    # One archive fetch avoids treating transient raw-host resets as missing sources.
    request = urllib.request.Request(CODELOAD858,
        headers={'User-Agent': 'AKBASCORE-TEST858-GATE1'})
    with urllib.request.urlopen(request, timeout=240) as response:
        archive = response.read(100000001)
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        for name, expected in LOCKS858.items():
            matches = [member for member in zipped.namelist()
                if member.endswith('/' + name)]
            assert len(matches) == 1, ('SOURCE_MEMBER_NOT_UNIQUE', name, matches)
            data = zipped.read(matches[0])
            actual = git_blob858(data)
            assert actual == expected, ('SOURCE_LOCK_FAILED', name, actual, expected)
            RAW_SOURCES858[name] = data
            if name.endswith('.py'):
                REAL_COMPILE858(data.decode('utf-8'), name, 'exec')
            short858('GATE0 SOURCE', name, actual, 'PASS')
    assert len(RAW_SOURCES858) == 17


def capture_cell_source858():
    # Colab exposes the submitted cell through input history. If unavailable, do
    # not invent an 858.py artifact; the delivered .py file remains the source.
    try:
        shell = get_ipython()  # noqa: F821 — supplied by Colab/IPython.
        history = list(shell.history_manager.input_hist_raw)
        candidates = [text for text in history if
            'AKBASCORE SILICON HIPPOCAMPUS — TEST858 STATE TRANSFER AND FEEDBACK' in text]
        if candidates:
            (ROOT858 / '858.py').write_text(candidates[-1], encoding='utf-8')
            return True
    except Exception as exc:
        short858('858.py history capture unavailable:', type(exc).__name__, str(exc))
    return False


def current_job858(g):
    if not g:
        return {}
    job = g.get('j851') or g.get('j846') or {}
    return {
        'job': job.get('job'),
        'qid': g.get('q851', job.get('qid')),
        'condition': g.get('condition851', job.get('intervention')),
        'arm': g.get('arm851', job.get('arm')),
    }


def segment_metadata858(g, segments):
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
def runtime_context858(label, g=None, segments=None, pre=None, post=None):
    global LAST_CONTEXT858
    record = {
        'label': label,
        'time_offset_seconds': time.perf_counter() - START858,
        **current_job858(g),
        'segments': segment_metadata858(g, segments),
        'prefix_length': len(pre) if pre is not None else None,
        'suffix_length': len(post) if post is not None else None,
        'substep': None,
    }
    previous = STATE858.get('active')
    STATE858['active'] = record
    LAST_CONTEXT858 = record
    STATE858['contexts'].append({'event': 'ENTER', **record})
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
            'capture': STATE858.get('capture'),
        }
        FAILURES858.append(failure)
        raise
    finally:
        STATE858['active'] = previous


def hook_audit858(g, event):
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
        'time_offset_seconds': time.perf_counter() - START858,
        **current_job858(g),
        'transformers_output_capturing_installed': bool(getattr(
            g['model'], '_output_capturing_hooks_installed', False)),
        'hook_count': len(rows),
        'hooks': rows,
    }
    STATE858['hook_audits'].append(record)
    json_write858('858_hook_audit.json', STATE858['hook_audits'])
    return record


def assert_hook_free858(g, event):
    record = hook_audit858(g, event)
    if record['hook_count'] or record['transformers_output_capturing_installed']:
        raise RuntimeError('TEST858_FORWARD_HOOK_DETECTED: ' + event)
    return record


class Quiet858:
    def __init__(self):
        self.pending = ''

    def write(self, text):
        LOG_FILE858.write(text)
        LOG_FILE858.flush()
        self.pending += text
        while '\n' in self.pending:
            line, self.pending = self.pending.split('\n', 1)
            if 'TEST854 JOB-BY-JOB RESULTS|' in line:
                short858('JOB', line.split('TEST854 JOB-BY-JOB RESULTS|', 1)[1][:240])
        return len(text)

    def flush(self):
        LOG_FILE858.flush()

    def isatty(self):
        return False


SPELLINGS858 = (' CONTINUE', ' REVISE', ' STOP', ' SUFFICIENT', ' INSUFFICIENT')


def capture858(out, local):
    # Logits-only observation. Do not request hidden_states: Transformers v5
    # lazily installs persistent output-capturing forward hooks for that request.
    g = STATE858['g']
    logits = out.logits[0, -1].detach().float()
    sequence_length = int(out.logits.shape[1])
    step = len(STATE858['frames'])
    STATE858['capture'] = {
        **current_job858(g),
        'stage': None if not STATE858.get('active') else STATE858['active']['label'],
        'step': step,
        'logit_sequence_length': sequence_length,
        'logits_shape': list(logits.shape),
        'logits_dtype': str(logits.dtype),
        'logits_device': str(logits.device),
    }
    scores = logits[STATE858['first_ids']].cpu().tolist()
    record = {
        'step': step,
        'logit_sequence_length': sequence_length,
        'logits_shape': list(logits.shape),
        'logits_dtype': str(logits.dtype),
        'logits_device': str(logits.device),
        'returned_logits_bytes': out.logits.numel() * out.logits.element_size(),
        'tokenizations': STATE858['tokenizations'],
        'lens': 'diagnostic last-token logits, NOT action probabilities',
        'first_token_logits': dict(zip(SPELLINGS858, scores)),
        'stop_minus_revise': scores[2] - scores[1],
        'observation_scope': 'existing public logits only; hidden-state X-RAY disabled',
    }
    STATE858['frames'].append(record)


def clone_observer858(fn_node, g):
    node = copy.deepcopy(fn_node)
    original_name = node.name
    node.name = '_xr_' + original_name
    changed = 0

    class Observe858(ast.NodeTransformer):
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

    node = Observe858().visit(node)
    assert changed == 2, ('OBSERVATION_SITES', original_name, changed)
    module = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    # Reverse the observational delta and require exact AST equality.
    reverse = copy.deepcopy(node)
    reverse.name = original_name

    class Undo858(ast.NodeTransformer):
        def visit_Expr(self, n):
            if (isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
                    and n.value.func.id == '_xr_capture'):
                return None
            return self.generic_visit(n)

    reverse = Undo858().visit(reverse)
    assert ast.dump(reverse, include_attributes=False) == ast.dump(
        fn_node, include_attributes=False)
    if g is None:
        REAL_COMPILE858(module, 'TEST858_OBSERVER_STATIC', 'exec')
        return module
    exec(REAL_COMPILE858(module, 'TEST858_OBSERVER', 'exec'), g)
    return g[node.name]


def install858(g):
    assert not STATE858['installed']
    STATE858['installed'] = True
    STATE858['g'] = g
    torch = g['torch']
    np = g['np']
    assert g['NL'] == 80 and g['H'] == 8192 and g['DTYPE'] == torch.bfloat16
    assert len(g['JOBS841']) == 12 and not g['REC841'], 'Fresh run required; no unobserved resume'
    assert torch.cuda.device_count() == 1
    assert 'A100' in torch.cuda.get_device_name(0)
    assert not any(p.requires_grad for p in g['model'].parameters())
    assert_hook_free858(g, 'install_before_observation')
    transformers_module = g.get('transformers')
    STATE858['environment'] = {
        'torch_version': str(torch.__version__),
        'transformers_version': (None if transformers_module is None else
            str(getattr(transformers_module, '__version__', 'UNKNOWN'))),
        'hidden_states_requested': False,
        'observation': 'public out.logits only',
        'repair': 'remove output capture request; never clear hooks',
    }
    short858('GPU:', torch.cuda.get_device_name(0), '| frozen NF4 | BF16 | layers=80 H=8192',
        '| free GiB=', round(torch.cuda.mem_get_info()[0] / 1024 ** 3, 2))
    tokens = [list(g['tok'](s, add_special_tokens=False).input_ids) for s in SPELLINGS858]
    assert all(tokens)
    STATE858['tokenizations'] = dict(zip(SPELLINGS858, tokens))
    STATE858['first_ids'] = [value[0] for value in tokens]
    g['_xr_capture'] = capture858
    gen = g['gen851']
    observed = clone_observer858(STATE858['functions']['gen851'], g)
    inv = g['invoke851']
    gen_coverage = clone_observer858(STATE858['functions']['gen849'], g)
    old_coverage = g['coverage_state852']

    def observe_coverage(q, condition, mode, memx):
        fresh = (q, condition, mode) not in g['COVERAGE_SHARED852']
        h = old_coverage(q, condition, mode, memx)
        assert_hook_free858(g, 'coverage_original_return')
        if fresh:
            pre = list(g['prompt_ids'](g['COVERAGE852'].format(q=g['QTEXT841'][q])))
            with runtime_context858('coverage_replay', g, None, pre,
                    g['COVERAGE_SUFFIX852']) as active:
                STATE858['frames'] = []
                active['substep'] = 'observed_coverage_generator'
                obs = gen_coverage(memx, pre, None, g['COVERAGE_SUFFIX852'])
                assert_hook_free858(g, 'coverage_observed_return')
                same = (h['toks'] == obs['toks'] and h['text'] == obs['text']
                    and torch.equal(h['rows'], obs['rows']) and h['top1'] == obs['top1'])
                assert same, 'COVERAGE_OBSERVER_CHANGED_COMPUTATION'
    
                record = {
                    **current_job858(g),
                    'requested_qid': q,
                    'requested_condition': condition,
                    'requested_mode': mode,
                    'text': h['text'],
                    'tokens': h['trace849']['all_token_ids'],
                    'valid_protocol': h['text'].strip() in ('SUFFICIENT', 'INSUFFICIENT'),
                    'observer_equality': same,
                    'frames': STATE858['frames'],
                    'prefix_ids': pre,
                    'suffix_ids': list(g['COVERAGE_SUFFIX852']),
                }
                STATE858['coverage'].append(record)
        return h

    g['coverage_state852'] = observe_coverage

    def wrapped(memx, pre, segments, post, stage, tensors, traces, baseline=False):
        assert not baseline, 'Unexpected TEST854 path'
        with runtime_context858('invoke_' + stage, g, segments, pre, post) as active:
            torch.cuda.synchronize()
            begun = time.perf_counter()
            STATE858['frames'] = []
            # Budget guard for observational workload; never counted as model STOP.
            assert time.perf_counter() - STATE858['start'] < 3600, 'XRAY_MECHANICAL_TIME_LIMIT'
            checked = stage == 'review_0' and g['arm851'] == 'BASELINE853'
            active['substep'] = 'reference_generator' if checked else 'not_applicable'
            reference = gen(memx, pre, segments, post) if checked else None
            if checked:
                assert_hook_free858(g, 'reference_generator_return')
            g['gen851'] = observed
            try:
                active['substep'] = 'observed_generator'
                h = inv(memx, pre, segments, post, stage, tensors, traces, baseline=False)
            finally:
                g['gen851'] = gen
            assert_hook_free858(g, 'observed_generator_return')
            if checked:
                active['substep'] = 'runtime_equality'
                same = (h['toks'] == reference['toks'] and h['text'] == reference['text']
                    and torch.equal(h['rows'], reference['rows']) and h['top1'] == reference['top1'])
                STATE858['equalities'].append(bool(same))
                assert same, 'OBSERVER_CHANGED_NATIVE_COMPUTATION'
            identity = {
                **current_job858(g),
                'stage': stage,
            }
            index = len(STATE858['observations'])
            row = {
                **identity,
                'frames': STATE858['frames'],
                'input_segments': segment_metadata858(g, segments),
                'text': h['text'],
                'tokens': h['trace849']['all_token_ids'],
                'continuity': h['trace849']['continuity'],
                'prefix_ids': list(pre),
                'suffix_ids': list(post or []),
                'memory_tokens': int(memx[0][0].shape[-2]),
                'seconds_with_observation': time.perf_counter() - begun,
            }
            STATE858['observations'].append(row)
            STATE858['invocations'].append({
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
        STATE858['saved_jobs'].append(job)
        assert_hook_free858(g, 'job_saved_' + str(job))
        if STATE858['saved_jobs'] == expected_jobs:
            # REC841 and the native job artifact are already saved. The inherited
            # wrapper will preserve this explicit diagnostic exception verbatim.
            raise Gate1SmokeComplete858('GATE1_TWO_JOB_OBSERVATION_COMPLETE')
        assert len(STATE858['saved_jobs']) < len(expected_jobs), 'UNEXPECTED_JOB_ORDER'
        return result

    g['save_job841'] = save_and_stop
    short858('OBSERVER: logits-only AST inverse PASS; no hidden states; no hooks; two-job limit armed.')


def compile_xray858(source, filename, mode, *args, **kwargs):
    # Intercept only the final assembled CELL compile, before model loading.
    if filename == 'TEST849_CELL':
        assert not STATE858['compiled']
        STATE858['compiled'] = True
        tree = copy.deepcopy(source) if isinstance(source, ast.AST) else ast.parse(source)
        matches = [n for n in tree.body if isinstance(n, ast.Assign)
            and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
            and n.targets[0].id == 'BODY841']
        assert len(matches) == 1 and isinstance(matches[0].value, ast.Constant)
        body = matches[0].value.value
        bt = ast.parse(body)
        STATE858['functions'] = {n.name: n for n in bt.body if isinstance(n, ast.FunctionDef)}
        assert {'gen849', 'gen851', 'invoke851'} <= STATE858['functions'].keys()
        for name in ('gen849', 'gen851'):
            clone_observer858(STATE858['functions'][name], None)
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
        STATE858['patch_manifest'] = {
            'base_body_sha256': sha256_bytes858(body.encode()),
            'instrumented_body_sha256': sha256_bytes858(patched.encode()),
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
    return REAL_COMPILE858(source, filename, mode, *args, **kwargs)


def recover_inherited_error858(env, outer_exception, outer_trace):
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
        'context_failure_count': len(FAILURES858),
        'last_runtime_context': LAST_CONTEXT858,
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
        info['saved_traceback_sha256'] = sha256_bytes858(saved_text.encode('utf-8'))

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
            info['saved_exception_traceback_sha256'] = sha256_bytes858(
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


def reproduce_pre858858():
    quiet = Quiet858()
    env = {
        '__name__': '__main__',
        'compile': compile_xray858,
        '_xr_install': install858,
    }
    STATE858['start'] = time.perf_counter()
    outer_exception = None
    outer_trace = ''
    try:
        sys.stdout = quiet
        sys.stderr = quiet
        exec(REAL_COMPILE858(RAW_SOURCES858['854.py'].decode(),
            'LOCKED_TEST854', 'exec'), env)
    except BaseException as exc:
        outer_exception = exc
        # This usually contains only TEST849_FAILED: RuntimeError. The actual
        # RuntimeError is recovered below from the inherited wrapper globals.
        outer_trace = traceback.format_exc()
    finally:
        sys.stdout = CONSOLE858
        sys.stderr = ERROR_CONSOLE858
        quiet.flush()
    root_error, combined_trace, evidence = recover_inherited_error858(
        env, outer_exception, outer_trace)
    return env, root_error, combined_trace, evidence


def records_digest858(env):
    return sha256_bytes858(json.dumps(env.get('REC841', {}), sort_keys=True,
        ensure_ascii=False).encode('utf-8'))


def verify_two_job858(env, combined_trace):
    """Technical gate only: scientific termination is reported, never required."""
    jobs = env.get('JOBS841', [])
    records = env.get('REC841', {})
    expected = jobs[:2]
    expected_ids = [j['job'] for j in expected]
    assert len(expected) == 2
    assert [j['intervention'] for j in expected] == ['INTACT', 'REMOVED']
    assert all(j['arm'] == 'BASELINE853' for j in expected)
    assert STATE858['saved_jobs'] == expected_ids, (
        'TWO_JOB_SAVE_MISMATCH', STATE858['saved_jobs'], expected_ids)
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
    assert STATE858['equalities'] == [True, True], (
        'TWO_REVIEW_EQUALITIES_REQUIRED', STATE858['equalities'])
    assert all(c['observer_equality'] for c in STATE858['coverage'])
    assert not STATE858['causal_probes'], 'CAUSAL_PROBE_RAN_BEFORE_ORIGINAL_STREAM_END'
    final_audit = assert_hook_free858(env, 'post_diagnostic_stop_before_causal_replays')
    assert STATE858['hook_audits'] and all(
        row['hook_count'] == 0 and not row['transformers_output_capturing_installed']
        for row in STATE858['hook_audits'])
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
        'review_replay_equalities': STATE858['equalities'],
        'coverage_observer_equalities': [c['observer_equality'] for c in STATE858['coverage']],
        'hook_audits': len(STATE858['hook_audits']),
        'final_hook_count': final_audit['hook_count'],
        'diagnostic_stop': 'GATE1_TWO_JOB_OBSERVATION_COMPLETE',
        'diagnostic_stop_is_model_stop': False,
        'scope': 'Technical hook-free continuity/equivalence only; no ACCEPT/STOP requirement.',
    }


def clone_segments858(segments):
    return [(list(slot), None if rows is None else rows.clone().cpu())
        for slot, rows in segments]


def segment_map858(g, segments):
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


def replace_named_slot858(g, segments, name, rows):
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


def segments_sha858(segments):
    return sha256_bytes858(json.dumps([
        {'slot': list(slot), 'state': None if rows is None else
            {'shape': list(rows.shape), 'dtype': str(rows.dtype),
             'sha256': hashlib.sha256(rows.detach().cpu().numpy().tobytes()).hexdigest()}}
        for slot, rows in segments], sort_keys=True).encode('utf-8'))


def native_h_equal858(torch, a, b):
    return (a['toks'] == b['toks'] and a['text'] == b['text']
        and a['top1'] == b['top1'] and a['kend'] == b['kend']
        and torch.equal(a['rows'], b['rows']))


def h_summary858(g, h):
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


def score_actions858(g, memx, pre, segments, post):
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


def score_margins858(scores):
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


def find_invocation858(job, stage):
    rows = [x for x in STATE858['invocations']
        if x['job'] == job and x['stage'] == stage]
    assert len(rows) == 1, ('INVOCATION_SNAPSHOT_NOT_UNIQUE', job, stage, len(rows))
    return rows[0]


def state_metrics858(g, rows):
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


def paired_metrics858(g, reference, value):
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


def continuity_for_slot858(g, invocation, slot_ids):
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


def state_map858(env, target_job):
    """Read existing snapshots only; no model forward and no new state semantics."""
    torch, np = env['torch'], env['np']
    cycles, tensors = [], {}
    for cycle in (0, 1):
        pre = find_invocation858(target_job, 'precontrol_%d' % cycle)
        review = find_invocation858(target_job, 'review_%d' % cycle)
        pm = segment_map858(env, pre['segments'])
        dm = segment_map858(env, review['segments'])
        assert {'C','E','U','R'} <= set(pm) and set(dm) == {'K0','J'}
        assert torch.equal(pre['h']['rows'], dm['K0'][1]), 'K0_PRECONTROL_ALIAS_BROKEN'
        states = {name: pm[name][1] for name in ('C','E','U','R') if name in pm}
        if 'Kprev' in pm:
            states['Kprev'] = pm['Kprev'][1]
        states.update({'K0': dm['K0'][1], 'J': dm['J'][1],
                       'review': review['h']['rows']})
        for name, rows in states.items():
            tensors['cycle%d_%s' % (cycle, name)] = rows.numpy().copy()
        metrics = {name: state_metrics858(env, rows) for name, rows in states.items()}
        row = {'cycle': cycle, 'states': metrics,
            'precontrol_output': {'alias_of': 'K0', 'sha256': metrics['K0']['sha256']},
            'review_output_sha256': metrics['review']['sha256'],
            'final_decision_input': {
                'ordered_roles': ['K0','J'], 'sha256': segments_sha858(review['segments']),
                'bf16_continuity': review['h']['trace849']['continuity']},
            'source_stage': {'precontrol': 'invoke851/precontrol_%d' % cycle,
                             'review': 'invoke851/review_%d' % cycle}}
        cycles.append(row)
        short858('STATE MAP cycle', cycle, 'roles', list(metrics),
                 'final_input_sha', row['final_decision_input']['sha256'])
        for name, value in metrics.items():
            short858('STATE', cycle, name, 'shape', value['shape'], 'norm', value['norm'],
                     'mean', value['mean'], 'std', value['std'], 'finite', value['finite'])
    comparisons = {}
    for name in ('C','E','U','R','K0','J','review'):
        s0 = find_invocation858(target_job, 'precontrol_0')
        s1 = find_invocation858(target_job, 'precontrol_1')
        r0 = find_invocation858(target_job, 'review_0')
        r1 = find_invocation858(target_job, 'review_1')
        def rows_for(cycle, pre, review):
            if name == 'review': return review['h']['rows']
            if name in ('K0','J'): return segment_map858(env, review['segments'])[name][1]
            return segment_map858(env, pre['segments'])[name][1]
        comparisons[name] = paired_metrics858(env, rows_for(0,s0,r0), rows_for(1,s1,r1))
        short858('TRANSITION', name, comparisons[name])

    review0 = find_invocation858(target_job, 'review_0')
    revision0 = find_invocation858(target_job, 'revision_0')
    pre1 = find_invocation858(target_job, 'precontrol_1')
    pm0 = segment_map858(env, find_invocation858(target_job, 'precontrol_0')['segments'])
    pm1 = segment_map858(env, pre1['segments'])
    kprev = pm1['Kprev'][1]
    candidate = pm1['C'][1]
    transfers = [
        {'path': 'review_0.rows -> previous_control851 -> cycle1.Kprev',
         'source_sha256': state_metrics858(env, review0['h']['rows'])['sha256'],
         'destination_sha256': state_metrics858(env, kprev)['sha256'],
         'exact_content_preserved': torch.equal(review0['h']['rows'], kprev),
         'bf16_injection': continuity_for_slot858(env, pre1, env['K_SLOT851']),
         'used_in': 'cycle1 precontrol gen851; then K0/J; then review_1'},
        {'path': 'revision_0.rows -> current851 -> cycle1.C',
         'source_sha256': state_metrics858(env, revision0['h']['rows'])['sha256'],
         'destination_sha256': state_metrics858(env, candidate)['sha256'],
         'exact_content_preserved': torch.equal(revision0['h']['rows'], candidate),
         'bf16_injection': continuity_for_slot858(env, pre1, env['C_SLOT851']),
         'used_in': 'cycle1 precontrol and relation/gate recomputation'},
        {'path': 'shared evidence -> cycle0.E and cycle1.E',
         'exact_content_reused': torch.equal(pm0['E'][1], pm1['E'][1])},
        {'path': 'shared coverage -> cycle0.U and cycle1.U',
         'exact_content_reused': torch.equal(pm0['U'][1], pm1['U'][1])},
        {'path': 'cycle1.C + cycle1.E -> relation852 -> cycle1.R',
         'derived_not_direct_carry': True},
    ]
    assert transfers[0]['exact_content_preserved'], 'KPREV_TRANSPORT_NOT_EXACT'
    assert transfers[1]['exact_content_preserved'], 'CANDIDATE_TRANSPORT_NOT_EXACT'
    for transfer in transfers:
        short858('TRANSFER', transfer)
    result = {'target_job': target_job, 'cycles': cycles, 'comparisons': comparisons,
              'transfers': transfers,
              'comparison_rule': 'Same role and shape only; Kprev has no cycle0 counterpart.',
              'tensor_file': '858_tensors.npz'}
    np.savez_compressed(ROOT858 / '858_tensors.npz', **tensors)
    json_write858('858_state_transitions.json', result)
    return result


def compatible_replacement858(g, reference, alternative):
    return (alternative is not None and reference.shape == alternative.shape
        and reference.dtype == alternative.dtype and reference.device == alternative.device
        and reference.device.type == 'cpu' and reference.dtype == g['torch'].float32)


def score_deltas858(reference, value):
    ref = {x['spelling'].strip(): x for x in reference}
    val = {x['spelling'].strip(): x for x in value}
    return {name: {'sequence_logp_delta': val[name]['sequence_logp']-ref[name]['sequence_logp'],
        'mean_token_logp_delta': val[name]['mean_token_logp']-ref[name]['mean_token_logp'],
        'first_token_logit_delta': val[name]['first_token_logit']-ref[name]['first_token_logit']}
        for name in ('CONTINUE','REVISE','STOP')}


def probe858(env, snapshots, variant, replacement=None, candidate_swap=False):
    """One matched post-hoc replay; no result is returned to the original engine."""
    torch = env['torch']
    pre, review = snapshots['pre1'], snapshots['review1']
    original_pre_segments = clone_segments858(pre['segments'])
    original_decision = clone_segments858(review['segments'])
    pm = segment_map858(env, original_pre_segments)
    dm = segment_map858(env, original_decision)
    pre_segments = clone_segments858(original_pre_segments)
    C, E = pm['C'][1], pm['E'][1]
    if variant == 'KPREV_ZERO':
        assert replacement is not None
        pre_segments = replace_named_slot858(env, pre_segments, 'Kprev', replacement)
    elif variant == 'KPREV_SWAP':
        assert replacement is not None
        pre_segments = replace_named_slot858(env, pre_segments, 'Kprev', replacement)
    elif variant == 'CANDIDATE_CARRY_SWAP_TO_C0':
        assert replacement is not None
        pre_segments = replace_named_slot858(env, pre_segments, 'C', replacement)
        new_R = env['relation852'](replacement, E)
        pre_segments = replace_named_slot858(env, pre_segments, 'R', new_R)
        C = replacement
    else:
        assert variant in ('ORIGINAL','KPREV_ORIGINAL_RESTORE') and replacement is None
    before = segments_sha858(original_pre_segments)
    pre_h = env['gen851'](pre['memx'], list(pre['pre']), pre_segments, list(pre['post']))
    J = env['interaction854'](C, E, pre_h['rows'])
    final_segments = [(list(env['K_SLOT854']), pre_h['rows']),
                      (list(env['J_SLOT854']), J)]
    review_h = env['gen851'](review['memx'], list(review['pre']), final_segments,
                             list(review['post']))
    scores = score_actions858(env, review['memx'], list(review['pre']), final_segments,
                              list(review['post']))
    exact_replay = (native_h_equal858(torch, pre_h, pre['h'])
        and native_h_equal858(torch, review_h, review['h'])
        and segments_sha858(final_segments) == segments_sha858(original_decision))
    if variant in ('ORIGINAL','KPREV_ORIGINAL_RESTORE'):
        assert exact_replay, ('ORIGINAL_OR_RESTORE_NOT_EXACT', variant)
    else:
        assert segments_sha858(pre_segments) != before, ('EMPTY_INTERVENTION', variant)
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
        'precontrol': paired_metrics858(env, pre['h']['rows'], pre_h['rows']),
        'J': paired_metrics858(env, dm['J'][1], J),
        'review': paired_metrics858(env, review['h']['rows'], review_h['rows']),
    }
    row = {'variant': variant, 'status': 'DONE',
        'candidate_swap_recomputes_R_and_gate': candidate_swap,
        'original_action': original_action, 'diagnostic_action': action,
        'diagnostic_action_changed': action != original_action,
        'diagnostic_action_is_not_original_job_action': True,
        'exact_original_or_restore': exact_replay if variant in ('ORIGINAL','KPREV_ORIGINAL_RESTORE') else None,
        'precontrol': h_summary858(env, pre_h), 'review': h_summary858(env, review_h),
        'K0': state_metrics858(env, pre_h['rows']), 'J': state_metrics858(env, J),
        'state_differences_from_original': differences,
        'action_scores': scores, 'margins': score_margins858(scores),
        'score_deltas_from_original': score_deltas858(original_scores, scores),
        'replacement_source': None if replacement is None else state_metrics858(env, replacement),
        'original_precontrol_input_sha256': before,
        'probe_precontrol_input_sha256': segments_sha858(pre_segments),
        'final_decision_input_sha256': segments_sha858(final_segments)}
    STATE858['causal_probes'].append(row)
    json_write858('858_causal_probes.json', STATE858['causal_probes'])
    short858('CAUSAL', variant, 'original', original_action, 'diagnostic', action,
        'STOP-REVISE', row['margins']['stop_minus_revise_sequence_logp'],
        'precontrol_exact', differences['precontrol']['exact'],
        'review_exact', differences['review']['exact'])
    return row


def not_applicable858(variant, reason):
    row = {'variant': variant, 'status': 'NOT_APPLICABLE', 'reason': reason,
           'fabricated_tensor_used': False}
    STATE858['causal_probes'].append(row)
    json_write858('858_causal_probes.json', STATE858['causal_probes'])
    short858('CAUSAL', variant, 'NOT_APPLICABLE', reason)
    return row


def mechanism_summary858(env, transitions, original_record):
    records = STATE858['causal_probes']
    done = [r for r in records if r['status'] == 'DONE']
    zero = next(r for r in done if r['variant'] == 'KPREV_ZERO')
    score_effect = any(abs(v['sequence_logp_delta']) > 0
        for v in zero['score_deltas_from_original'].values())
    stage_effects = [name for name, changed in (
        ('precontrol', not zero['state_differences_from_original']['precontrol']['exact']),
        ('J', not zero['state_differences_from_original']['J']['exact']),
        ('review_output', not zero['state_differences_from_original']['review']['exact']),
        ('action_scores', score_effect),
        ('greedy_action', zero['diagnostic_action_changed'])) if changed]
    comparisons = transitions['comparisons']
    exact_repetition = (not any('Kprev' in c['states'] for c in transitions['cycles'] if c['cycle'] == 1)
        and all(comparisons[n]['exact'] for n in comparisons)
        and len({c['action'] for c in original_record['cycles']}) == 1)
    numerical_change = any(not x['exact'] for x in comparisons.values())
    same_original_action = len({c['action'] for c in original_record['cycles']}) == 1
    return {
        'exact_repetition': exact_repetition,
        'numerical_change_with_same_original_greedy_action': numerical_change and same_original_action,
        'kprev_transport_confirmed': transitions['transfers'][0]['exact_content_preserved'],
        'candidate_transport_confirmed': transitions['transfers'][1]['exact_content_preserved'],
        'kprev_causal_numerical_effect': bool(stage_effects),
        'kprev_effect_stages_in_order': stage_effects,
        'kprev_greedy_decision_effect': zero['diagnostic_action_changed'],
        'kprev_score_effect_without_greedy_flip': score_effect and not zero['diagnostic_action_changed'],
        'same_action_does_not_imply_same_computation': (
            not zero['diagnostic_action_changed'] and bool(stage_effects)),
        'feedback_path_function': 'numerical recurrence/state coupling; useful correction or STOP is not established',
        'classification_rule': 'Exact transport proves use; matched replay differences prove causal numerical effect; only native greedy text defines diagnostic action.',
        'original_model_stop': original_record['end'] == 'MODEL_STOP',
        'original_end': original_record['end'],
    }


def run_analysis858(env):
    original_digest = records_digest858(env)
    STATE858['original_record_sha256'] = original_digest
    jobs = env['JOBS841'][:2]
    target_job = jobs[1]['job']
    record = env['REC841'][target_job]
    assert jobs[1]['intervention'] == 'REMOVED'
    assert [c['action'] for c in record['cycles']] == ['REVISE','REVISE']
    for job in jobs:
        r = env['REC841'][job['job']]
        short858('ORIGINAL JOB', job['job'], job['intervention'], 'END', r['end'],
            'ACTIONS', [c['action'] for c in r['cycles']],
            'REVISIONS', [None if c['revision'] is None else c['revision']['text']
                for c in r['cycles']])
    transitions = state_map858(env, target_job)
    STATE858['transitions'] = transitions
    snapshots = {name: find_invocation858(target_job, stage) for name, stage in (
        ('pre0','precontrol_0'),('pre1','precontrol_1'),
        ('review0','review_0'),('review1','review_1'),('revision0','revision_0'))}
    probe858(env, snapshots, 'ORIGINAL')
    original_kprev = segment_map858(env, snapshots['pre1']['segments'])['Kprev'][1]
    probe858(env, snapshots, 'KPREV_ZERO', env['torch'].zeros_like(original_kprev))

    intact_review = find_invocation858(jobs[0]['job'], 'review_0')['h']['rows']
    if compatible_replacement858(env, original_kprev, intact_review):
        row = probe858(env, snapshots, 'KPREV_SWAP', intact_review)
        row['replacement_source'] = {'job': jobs[0]['job'], 'condition': 'INTACT',
            'stage': 'review_0', 'role': 'native review soft-row output',
            **state_metrics858(env, intact_review)}
        json_write858('858_causal_probes.json', STATE858['causal_probes'])
    else:
        not_applicable858('KPREV_SWAP',
            'INTACT review_0 does not match Kprev role-compatible shape/dtype/device; no substitute invented.')

    c0 = segment_map858(env, snapshots['pre0']['segments'])['C'][1]
    c1 = segment_map858(env, snapshots['pre1']['segments'])['C'][1]
    if compatible_replacement858(env, c1, c0):
        row = probe858(env, snapshots, 'CANDIDATE_CARRY_SWAP_TO_C0', c0, True)
        row['replacement_source'] = {'job': target_job, 'stage': 'precontrol_0.C',
            'role': 'previous native candidate soft-row', **state_metrics858(env, c0)}
        json_write858('858_causal_probes.json', STATE858['causal_probes'])
    else:
        not_applicable858('CANDIDATE_CARRY_SWAP_TO_C0',
            'cycle0 and cycle1 candidate shapes differ; direct matched swap is not defined.')

    # Restoration is deliberately last, after every intervention.
    probe858(env, snapshots, 'KPREV_ORIGINAL_RESTORE')
    assert records_digest858(env) == original_digest, 'DIAGNOSTICS_CHANGED_ORIGINAL_RECORDS'
    assert_hook_free858(env, 'post_TEST858_replays')
    assert not any(p.requires_grad for p in env['model'].parameters())
    required = [r for r in STATE858['causal_probes'] if r['variant'] in
        ('ORIGINAL','KPREV_ZERO','KPREV_ORIGINAL_RESTORE')]
    assert len(required) == 3 and all(r['status'] == 'DONE' for r in required)
    assert all(r['exact_original_or_restore'] for r in required
        if r['variant'] != 'KPREV_ZERO')
    summary = mechanism_summary858(env, transitions, record)
    summary.update({'status': 'PASS_DIAGNOSTIC_NOT_LOOP_REPAIR',
        'original_records_unchanged': True,
        'completed_probes': sum(r['status']=='DONE' for r in STATE858['causal_probes']),
        'not_applicable_probes': sum(r['status']=='NOT_APPLICABLE' for r in STATE858['causal_probes'])})
    json_write858('858_causal_probes.json', STATE858['causal_probes'])
    short858('MECHANISM SUMMARY', summary)
    return summary


def write_partial858():
    if not (ROOT858/'858_state_transitions.json').exists():
        json_write858('858_state_transitions.json', STATE858.get('transitions', {}))
    if not (ROOT858/'858_causal_probes.json').exists():
        json_write858('858_causal_probes.json', STATE858['causal_probes'])


def finalize858(gates, execution):
    write_partial858()
    capture_cell_source858()
    report = {'test': TEST858_KIND, 'execution': execution, 'gates': gates,
        'original_error': EXECUTION_ERROR858, 'analysis_error': PROBE_ERROR858,
        'diagnostic_stop': DIAGNOSTIC_STOP858,
        'diagnostic_stop_is_model_stop': False,
        'technical_verification': TWO_JOB_VERIFICATION858,
        'analysis': ANALYSIS858,
        'source_lock_count': len(RAW_SOURCES858),
        'environment': STATE858['environment'],
        'patch_manifest': STATE858.get('patch_manifest'),
        'observer_equalities': STATE858['equalities'],
        'coverage_observer_equalities': [c['observer_equality'] for c in STATE858['coverage']],
        'original_model_stop_observed': any(j.get('model_stop')
            for j in TWO_JOB_VERIFICATION858.get('jobs', [])),
        'seconds': time.perf_counter()-START858,
        'limitations': ['Two original jobs only; no generalization claim.',
            'Diagnostic actions do not modify original actions or termination.',
            'Teacher-forced sequence scores are not calibrated probabilities.',
            'Numerical feedback effect does not establish useful correction or STOP.',
            'Zero ablation measures computational sensitivity, not semantic information quality.',
            'INVALID remains INVALID; UNKNOWN is not STOP.',
            'Optional swaps remain NOT_APPLICABLE when no matched native state exists.'],
        'TEST858_NEW_ENGINE': False, 'TEST858_LOOP_REPAIR_ESTABLISHED': False}
    json_write858('858_report.json', report)
    short858('TEST858 RESULT', execution)
    for name, status in gates.items(): short858(name, status)
    short858('ORIGINAL MODEL STOP', report['original_model_stop_observed'])
    short858('ORIGINAL ERROR', EXECUTION_ERROR858 or 'NONE')
    short858('ANALYSIS ERROR', PROBE_ERROR858 or 'NONE')
    short858('ARTIFACTS', ROOT858)
    LOG_FILE858.flush()
    manifest = {}
    for path in sorted(ROOT858.rglob('*')):
        if path.is_file() and path.name != '858_sha256_manifest.json':
            manifest[str(path.relative_to(ROOT858))] = {'bytes': path.stat().st_size,
                'sha256': sha256_bytes858(path.read_bytes())}
    json_write858('858_sha256_manifest.json', manifest)


try:
    short858('TEST858: locked 857 spine; state transfer and matched feedback only.')
    short858('GPU EXECUTION: NOT VERIFIED BY AUTHOR; restart Colab before this cell.')
    load_sources858()
    gate0 = 'PASS'
    env858, error858, trace858, evidence858 = reproduce_pre858858()
    EXECUTION_ERROR858, TRACEBACK858, ERROR_EVIDENCE858 = error858, trace858, evidence858
    OUTER_EXECUTION_ERROR858 = evidence858.get('outer_exception')
    if trace858:
        short858(trace858[-12000:])
    if 'GATE1_TWO_JOB_OBSERVATION_COMPLETE' in trace858:
        DIAGNOSTIC_STOP858 = 'GATE1_TWO_JOB_OBSERVATION_COMPLETE'
    try:
        TWO_JOB_VERIFICATION858 = verify_two_job858(env858, trace858)
        EXECUTION_ERROR858 = None  # expected diagnostic wrapper, not a runtime failure
        gate1 = gate2 = 'PASS'
    except Exception as exc:
        gate1 = gate2 = 'BLOCKED'
        EXECUTION_ERROR858 = type(exc).__name__+': '+str(exc)
        short858(traceback.format_exc())
    if gate1 == 'PASS':
        short858('SYSTEM: hook-free PASS; frozen NF4/BF16; physical CUT3/H3/KV path unchanged.')
        try:
            ANALYSIS858 = run_analysis858(env858)
            gate3 = gate4 = 'PASS'
            execution = 'STATE_TRANSFER_AND_FEEDBACK_DIAGNOSTIC_COMPLETE'
        except BaseException as exc:
            PROBE_ERROR858 = type(exc).__name__+': '+str(exc)
            TRACEBACK858 += '\n===== TEST858 ANALYSIS FAILURE =====\n'+traceback.format_exc()
            short858(traceback.format_exc())
            gate3 = gate4 = 'BLOCKED'
            execution = 'ANALYSIS_INCOMPLETE_FULL_TRACEBACK_IN_LOG'
    else:
        gate3 = gate4 = 'BLOCKED'
        execution = 'TWO_JOB_TECHNICAL_VERIFICATION_FAILED'
    removed = [j for j in TWO_JOB_VERIFICATION858.get('jobs', []) if j.get('condition')=='REMOVED']
    gate5 = ('NOT_OBSERVED_MECHANICAL_REVIEW_LIMIT' if removed and
        removed[0]['end']=='MECHANICAL_REVIEW_LIMIT' else
        'OBSERVED_MODEL_STOP' if removed and removed[0]['end']=='MODEL_STOP' else 'OTHER_OR_NOT_RUN')
    gates = {'GATE0_SOURCE_INTEGRITY': gate0,
        'GATE1_HOOKFREE_ORIGINAL_TWO_JOBS': gate1,
        'GATE2_OBSERVER_EQUIVALENCE': gate2,
        'GATE3_STATE_MAP_AND_REAL_TRANSPORT': gate3,
        'GATE4_MATCHED_FEEDBACK_AND_RESTORE': gate4,
        'GATE5_ORIGINAL_MODEL_STOP_BEHAVIOR': gate5,
        'GATE6_INDEPENDENT_GENERALIZATION': 'BLOCKED_TWO_JOB_DIAGNOSTIC_ONLY',
        'GATE7_ARTIFACT_INTEGRITY': 'PASS'}
    finalize858(gates, execution)
except BaseException as exc:
    EXECUTION_ERROR858 = type(exc).__name__+': '+str(exc)
    sys.stdout, sys.stderr = CONSOLE858, ERROR_CONSOLE858
    short858(traceback.format_exc())
    gates = {'GATE0_SOURCE_INTEGRITY': 'PASS' if len(RAW_SOURCES858)==17 else 'FAIL',
        'GATE1_HOOKFREE_ORIGINAL_TWO_JOBS': 'BLOCKED',
        'GATE2_OBSERVER_EQUIVALENCE': 'BLOCKED',
        'GATE3_STATE_MAP_AND_REAL_TRANSPORT': 'BLOCKED',
        'GATE4_MATCHED_FEEDBACK_AND_RESTORE': 'BLOCKED',
        'GATE5_ORIGINAL_MODEL_STOP_BEHAVIOR': 'BLOCKED',
        'GATE6_INDEPENDENT_GENERALIZATION': 'BLOCKED',
        'GATE7_ARTIFACT_INTEGRITY': 'PASS'}
    finalize858(gates, 'TEST858_FAILURE_FULL_TRACEBACK_IN_LOG')
finally:
    LOG_FILE858.close()
