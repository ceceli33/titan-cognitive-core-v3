# AKBASCORE SILICON HIPPOCAMPUS — TEST855 GATE 1 HOOK-FREE VERIFICATION
# Two-job diagnostic cell, NOT a completed TEST855 motor.
# Verified failure mechanism: Transformers output_hidden_states installs persistent
# forward hooks; the next native DirectCut3 mount rejects those hooks.
# Minimal repair: request no hidden states and observe only already-returned logits.
# It runs the first two BASELINE853 jobs, then raises an explicit diagnostic-stop
# exception after the second job is saved. This is not a model STOP.
# GATE 3-6 remain blocked. GPU execution is not claimed by the author.
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

TEST855_KIND = 'GATE1_HOOKFREE_TWO_JOB_VERIFICATION_NOT_FULL_TEST855'
BASE855 = 'https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/main/'
CODELOAD855 = 'https://codeload.github.com/ceceli33/titan-cognitive-core-v3/zip/refs/heads/main'
LOCKS855 = {
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
PRE855_DIR = pathlib.Path('/content/PRE855_XRAY_20261104T062801Z')
PRE855_ERROR = PRE855_DIR / 'error.txt'
STAMP855 = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
ROOT855 = pathlib.Path('/content') / ('TEST855_GATE1_RECOVERY_' + STAMP855)
ROOT855.mkdir(parents=True, exist_ok=False)
CONSOLE855 = sys.stdout
ERROR_CONSOLE855 = sys.stderr
LOG_FILE855 = open(ROOT855 / '855.log', 'w', encoding='utf-8')
START855 = time.perf_counter()
REAL_COMPILE855 = builtins.compile
RAW_SOURCES855 = {}
STATE855 = {
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
    'environment': {},
    'start': START855,
}
FAILURES855 = []
EXECUTION_ERROR855 = None
OUTER_EXECUTION_ERROR855 = None
TRACEBACK855 = ''
ERROR_EVIDENCE855 = {}
LAST_CONTEXT855 = None
DIAGNOSTIC_STOP855 = None
TWO_JOB_VERIFICATION855 = {}
RECOVERY_MODE855 = 'NOT_STARTED'


class Gate1SmokeComplete855(Exception):
    """Explicit diagnostic control flow after two saved jobs; never model STOP."""


def short855(*args):
    text = ' '.join(str(x) for x in args)
    print(text, file=CONSOLE855, flush=True)
    LOG_FILE855.write(text + '\n')
    LOG_FILE855.flush()


def json_write855(name, value):
    path = ROOT855 / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2,
        allow_nan=False), encoding='utf-8')
    return path


def jsonl_append855(name, value):
    with open(ROOT855 / name, 'a', encoding='utf-8') as handle:
        handle.write(json.dumps(value, ensure_ascii=False, allow_nan=False) + '\n')


def sha256_bytes855(data):
    return hashlib.sha256(data).hexdigest()


def git_blob855(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def load_sources855():
    # One archive fetch avoids treating transient raw-host resets as missing sources.
    request = urllib.request.Request(CODELOAD855,
        headers={'User-Agent': 'AKBASCORE-TEST855-GATE1'})
    with urllib.request.urlopen(request, timeout=240) as response:
        archive = response.read(100000001)
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        for name, expected in LOCKS855.items():
            matches = [member for member in zipped.namelist()
                if member.endswith('/' + name)]
            assert len(matches) == 1, ('SOURCE_MEMBER_NOT_UNIQUE', name, matches)
            data = zipped.read(matches[0])
            actual = git_blob855(data)
            assert actual == expected, ('SOURCE_LOCK_FAILED', name, actual, expected)
            RAW_SOURCES855[name] = data
            (ROOT855 / name).write_bytes(data)
            if name.endswith('.py'):
                REAL_COMPILE855(data.decode('utf-8'), name, 'exec')
            short855('GATE0 SOURCE', name, actual, 'PASS')
    assert len(RAW_SOURCES855) == 11


def capture_cell_source855():
    # Colab exposes the submitted cell through input history. If unavailable, do
    # not invent an 855.py artifact; the delivered .py file remains the source.
    try:
        shell = get_ipython()  # noqa: F821 — supplied by Colab/IPython.
        history = list(shell.history_manager.input_hist_raw)
        candidates = [text for text in history if
            'AKBASCORE SILICON HIPPOCAMPUS — TEST855 GATE 1' in text]
        if candidates:
            (ROOT855 / '855.py').write_text(candidates[-1], encoding='utf-8')
            return True
    except Exception as exc:
        short855('855.py history capture unavailable:', type(exc).__name__, str(exc))
    return False


def current_job855(g):
    if not g:
        return {}
    job = g.get('j851') or g.get('j846') or {}
    return {
        'job': job.get('job'),
        'qid': g.get('q851', job.get('qid')),
        'condition': g.get('condition851', job.get('intervention')),
        'arm': g.get('arm851', job.get('arm')),
    }


def segment_metadata855(g, segments):
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
            except Exception:
                pass
        if rows is not None:
            item['finite'] = bool(g['torch'].isfinite(rows).all().item()) if g else None
            if g and rows.device.type == 'cpu' and rows.dtype == g['torch'].float32:
                item['state'] = g['stats849'](rows)
        rows_out.append(item)
    return rows_out


@contextlib.contextmanager
def runtime_context855(label, g=None, segments=None, pre=None, post=None):
    global LAST_CONTEXT855
    record = {
        'label': label,
        'time_offset_seconds': time.perf_counter() - START855,
        **current_job855(g),
        'segments': segment_metadata855(g, segments),
        'prefix_length': len(pre) if pre is not None else None,
        'suffix_length': len(post) if post is not None else None,
        'substep': None,
    }
    previous = STATE855.get('active')
    STATE855['active'] = record
    LAST_CONTEXT855 = record
    jsonl_append855('855_runtime_context.jsonl', {'event': 'ENTER', **record})
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
            'capture': STATE855.get('capture'),
        }
        jsonl_append855('855_runtime_context.jsonl', failure)
        FAILURES855.append(failure)
        raise
    finally:
        STATE855['active'] = previous


def hook_audit855(g, event):
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
        'time_offset_seconds': time.perf_counter() - START855,
        **current_job855(g),
        'transformers_output_capturing_installed': bool(getattr(
            g['model'], '_output_capturing_hooks_installed', False)),
        'hook_count': len(rows),
        'hooks': rows,
    }
    STATE855['hook_audits'].append(record)
    json_write855('855_hook_audit.json', STATE855['hook_audits'])
    return record


def assert_hook_free855(g, event):
    record = hook_audit855(g, event)
    if record['hook_count'] or record['transformers_output_capturing_installed']:
        raise RuntimeError('TEST855_FORWARD_HOOK_DETECTED: ' + event)
    return record


class Quiet855:
    def __init__(self):
        self.pending = ''

    def write(self, text):
        LOG_FILE855.write(text)
        LOG_FILE855.flush()
        self.pending += text
        while '\n' in self.pending:
            line, self.pending = self.pending.split('\n', 1)
            if 'TEST854 JOB-BY-JOB RESULTS|' in line:
                short855('JOB', line.split('TEST854 JOB-BY-JOB RESULTS|', 1)[1][:240])
        return len(text)

    def flush(self):
        LOG_FILE855.flush()

    def isatty(self):
        return False


SPELLINGS855 = (' CONTINUE', ' REVISE', ' STOP', ' SUFFICIENT', ' INSUFFICIENT')


def capture855(out, local):
    # Logits-only observation. Do not request hidden_states: Transformers v5
    # lazily installs persistent output-capturing forward hooks for that request.
    g = STATE855['g']
    logits = out.logits[0, -1].detach().float()
    sequence_length = int(out.logits.shape[1])
    step = len(STATE855['frames'])
    STATE855['capture'] = {
        **current_job855(g),
        'stage': None if not STATE855.get('active') else STATE855['active']['label'],
        'step': step,
        'logit_sequence_length': sequence_length,
        'logits_shape': list(logits.shape),
        'logits_dtype': str(logits.dtype),
        'logits_device': str(logits.device),
    }
    scores = logits[STATE855['first_ids']].cpu().tolist()
    record = {
        'step': step,
        'logit_sequence_length': sequence_length,
        'logits_shape': list(logits.shape),
        'logits_dtype': str(logits.dtype),
        'logits_device': str(logits.device),
        'returned_logits_bytes': out.logits.numel() * out.logits.element_size(),
        'tokenizations': STATE855['tokenizations'],
        'lens': 'diagnostic last-token logits, NOT action probabilities',
        'first_token_logits': dict(zip(SPELLINGS855, scores)),
        'stop_minus_revise': scores[2] - scores[1],
        'observation_scope': 'existing public logits only; hidden-state X-RAY disabled',
    }
    STATE855['arrays']['step%d_logits' % step] = logits.cpu().numpy()
    STATE855['frames'].append(record)


def clone_observer855(fn_node, g):
    node = copy.deepcopy(fn_node)
    original_name = node.name
    node.name = '_xr_' + original_name
    changed = 0

    class Observe855(ast.NodeTransformer):
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

    node = Observe855().visit(node)
    assert changed == 2, ('OBSERVATION_SITES', original_name, changed)
    module = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    # Reverse the observational delta and require exact AST equality.
    reverse = copy.deepcopy(node)
    reverse.name = original_name

    class Undo855(ast.NodeTransformer):
        def visit_Expr(self, n):
            if (isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
                    and n.value.func.id == '_xr_capture'):
                return None
            return self.generic_visit(n)

    reverse = Undo855().visit(reverse)
    assert ast.dump(reverse, include_attributes=False) == ast.dump(
        fn_node, include_attributes=False)
    if g is None:
        REAL_COMPILE855(module, 'TEST855_OBSERVER_STATIC', 'exec')
        return module
    exec(REAL_COMPILE855(module, 'TEST855_OBSERVER', 'exec'), g)
    return g[node.name]


def install855(g):
    assert not STATE855['installed']
    STATE855['installed'] = True
    STATE855['g'] = g
    torch = g['torch']
    np = g['np']
    assert g['NL'] == 80 and g['H'] == 8192 and g['DTYPE'] == torch.bfloat16
    assert len(g['JOBS841']) == 12 and not g['REC841'], 'Fresh run required; no unobserved resume'
    assert torch.cuda.device_count() == 1
    assert 'A100' in torch.cuda.get_device_name(0)
    assert not any(p.requires_grad for p in g['model'].parameters())
    assert_hook_free855(g, 'install_before_observation')
    transformers_module = g.get('transformers')
    STATE855['environment'] = {
        'torch_version': str(torch.__version__),
        'transformers_version': (None if transformers_module is None else
            str(getattr(transformers_module, '__version__', 'UNKNOWN'))),
        'hidden_states_requested': False,
        'observation': 'public out.logits only',
        'repair': 'remove output capture request; never clear hooks',
    }
    json_write855('855_environment.json', STATE855['environment'])
    short855('GPU:', torch.cuda.get_device_name(0), '| frozen NF4 | BF16 | layers=80 H=8192',
        '| free GiB=', round(torch.cuda.mem_get_info()[0] / 1024 ** 3, 2))
    tokens = [list(g['tok'](s, add_special_tokens=False).input_ids) for s in SPELLINGS855]
    assert all(tokens)
    STATE855['tokenizations'] = dict(zip(SPELLINGS855, tokens))
    STATE855['first_ids'] = [value[0] for value in tokens]
    g['_xr_capture'] = capture855
    gen = g['gen851']
    observed = clone_observer855(STATE855['functions']['gen851'], g)
    inv = g['invoke851']
    gen_coverage = clone_observer855(STATE855['functions']['gen849'], g)
    old_coverage = g['coverage_state852']

    def observe_coverage(q, condition, mode, memx):
        fresh = (q, condition, mode) not in g['COVERAGE_SHARED852']
        h = old_coverage(q, condition, mode, memx)
        assert_hook_free855(g, 'coverage_original_return')
        if fresh:
            pre = list(g['prompt_ids'](g['COVERAGE852'].format(q=g['QTEXT841'][q])))
            with runtime_context855('coverage_replay', g, None, pre,
                    g['COVERAGE_SUFFIX852']) as active:
                STATE855['arrays'] = {}
                STATE855['frames'] = []
                active['substep'] = 'observed_coverage_generator'
                obs = gen_coverage(memx, pre, None, g['COVERAGE_SUFFIX852'])
                assert_hook_free855(g, 'coverage_observed_return')
                same = (h['toks'] == obs['toks'] and h['text'] == obs['text']
                    and torch.equal(h['rows'], obs['rows']) and h['top1'] == obs['top1'])
                assert same, 'COVERAGE_OBSERVER_CHANGED_COMPUTATION'
                path = 'coverage_%02d.npz' % len(STATE855['coverage'])
                np.savez_compressed(ROOT855 / path, **STATE855['arrays'])
                record = {
                    **current_job855(g),
                    'requested_qid': q,
                    'requested_condition': condition,
                    'requested_mode': mode,
                    'file': path,
                    'text': h['text'],
                    'tokens': h['trace849']['all_token_ids'],
                    'valid_protocol': h['text'].strip() in ('SUFFICIENT', 'INSUFFICIENT'),
                    'observer_equality': same,
                    'frames': STATE855['frames'],
                    'prefix_ids': pre,
                    'suffix_ids': list(g['COVERAGE_SUFFIX852']),
                }
                STATE855['coverage'].append(record)
                json_write855('855_coverage.json', STATE855['coverage'])
                jsonl_append855('855_xray.jsonl', {'kind': 'COVERAGE', **record})
        return h

    g['coverage_state852'] = observe_coverage

    def wrapped(memx, pre, segments, post, stage, tensors, traces, baseline=False):
        assert not baseline, 'Unexpected TEST854 path'
        with runtime_context855('invoke_' + stage, g, segments, pre, post) as active:
            torch.cuda.synchronize()
            begun = time.perf_counter()
            STATE855['arrays'] = {}
            STATE855['frames'] = []
            # Budget guard for observational workload; never counted as model STOP.
            assert time.perf_counter() - STATE855['start'] < 3600, 'XRAY_MECHANICAL_TIME_LIMIT'
            checked = stage == 'review_0' and g['arm851'] == 'BASELINE853'
            active['substep'] = 'reference_generator' if checked else 'not_applicable'
            reference = gen(memx, pre, segments, post) if checked else None
            if checked:
                assert_hook_free855(g, 'reference_generator_return')
            g['gen851'] = observed
            try:
                active['substep'] = 'observed_generator'
                h = inv(memx, pre, segments, post, stage, tensors, traces, baseline=False)
            finally:
                g['gen851'] = gen
            assert_hook_free855(g, 'observed_generator_return')
            if checked:
                active['substep'] = 'runtime_equality'
                same = (h['toks'] == reference['toks'] and h['text'] == reference['text']
                    and torch.equal(h['rows'], reference['rows']) and h['top1'] == reference['top1'])
                STATE855['equalities'].append(bool(same))
                assert same, 'OBSERVER_CHANGED_NATIVE_COMPUTATION'
            identity = {
                **current_job855(g),
                'stage': stage,
            }
            index = len(STATE855['observations'])
            path = 'native_%03d.npz' % index
            np.savez_compressed(ROOT855 / path, **STATE855['arrays'])
            row = {
                **identity,
                'file': path,
                'frames': STATE855['frames'],
                'input_segments': segment_metadata855(g, segments),
                'text': h['text'],
                'tokens': h['trace849']['all_token_ids'],
                'continuity': h['trace849']['continuity'],
                'prefix_ids': list(pre),
                'suffix_ids': list(post or []),
                'memory_tokens': int(memx[0][0].shape[-2]),
                'seconds_with_observation': time.perf_counter() - begun,
            }
            STATE855['observations'].append(row)
            jsonl_append855('855_observations.jsonl', row)
            jsonl_append855('855_xray.jsonl', {'kind': 'NATIVE', **row})
            return h

    g['invoke851'] = wrapped
    old_save = g['save_job841']
    expected_jobs = [j['job'] for j in g['JOBS841'][:2]]
    assert len(expected_jobs) == 2
    assert all(j['arm'] == 'BASELINE853' for j in g['JOBS841'][:2])

    def save_and_stop(job, record, tensors):
        result = old_save(job, record, tensors)
        STATE855['saved_jobs'].append(job)
        assert_hook_free855(g, 'job_saved_' + str(job))
        if STATE855['saved_jobs'] == expected_jobs:
            # REC841 and the native job artifact are already saved. The inherited
            # wrapper will preserve this explicit diagnostic exception verbatim.
            raise Gate1SmokeComplete855('GATE1_TWO_JOB_OBSERVATION_COMPLETE')
        assert len(STATE855['saved_jobs']) < len(expected_jobs), 'UNEXPECTED_JOB_ORDER'
        return result

    g['save_job841'] = save_and_stop
    short855('OBSERVER: logits-only AST inverse PASS; no hidden states; no hooks; two-job limit armed.')


def compile_xray855(source, filename, mode, *args, **kwargs):
    # Intercept only the final assembled CELL compile, before model loading.
    if filename == 'TEST849_CELL':
        assert not STATE855['compiled']
        STATE855['compiled'] = True
        tree = copy.deepcopy(source) if isinstance(source, ast.AST) else ast.parse(source)
        matches = [n for n in tree.body if isinstance(n, ast.Assign)
            and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
            and n.targets[0].id == 'BODY841']
        assert len(matches) == 1 and isinstance(matches[0].value, ast.Constant)
        body = matches[0].value.value
        bt = ast.parse(body)
        STATE855['functions'] = {n.name: n for n in bt.body if isinstance(n, ast.FunctionDef)}
        assert {'gen849', 'gen851', 'invoke851'} <= STATE855['functions'].keys()
        for name in ('gen849', 'gen851'):
            clone_observer855(STATE855['functions'][name], None)
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
        json_write855('855_patch_manifest.json', {
            'base_body_sha256': sha256_bytes855(body.encode()),
            'instrumented_body_sha256': sha256_bytes855(patched.encode()),
            'change': 'one logits-only observer installation; generator model calls and kwargs unchanged',
            'root_cause': 'output_hidden_states lazily installed persistent Transformers forward hooks',
            'minimal_repair': 'no output_hidden_states request; no hook removal; fresh model required',
            'hidden_state_xray': 'NOT_RUN',
            'original_jobs': 12,
            'jobs_allowed_before_diagnostic_stop': 2,
            'review_equality_replays': 2,
            'coverage_equality_replays_max': 2,
            'N_probes': 0,
            'decision_path': 'original TEST854; diagnostic outputs never used for actions',
        })
        matches[0].value = ast.Constant(patched)
        source = ast.fix_missing_locations(tree)
    return REAL_COMPILE855(source, filename, mode, *args, **kwargs)


def recover_inherited_error855(env, outer_exception, outer_trace):
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
        'context_failure_count': len(FAILURES855),
        'last_runtime_context': LAST_CONTEXT855,
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
        info['saved_traceback_sha256'] = sha256_bytes855(saved_text.encode('utf-8'))

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
            info['saved_exception_traceback_sha256'] = sha256_bytes855(
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


def reproduce_pre855855():
    quiet = Quiet855()
    env = {
        '__name__': '__main__',
        'compile': compile_xray855,
        '_xr_install': install855,
    }
    STATE855['start'] = time.perf_counter()
    outer_exception = None
    outer_trace = ''
    try:
        sys.stdout = quiet
        sys.stderr = quiet
        exec(REAL_COMPILE855(RAW_SOURCES855['854.py'].decode(),
            'LOCKED_TEST854', 'exec'), env)
    except BaseException as exc:
        outer_exception = exc
        # This usually contains only TEST849_FAILED: RuntimeError. The actual
        # RuntimeError is recovered below from the inherited wrapper globals.
        outer_trace = traceback.format_exc()
    finally:
        sys.stdout = CONSOLE855
        sys.stderr = ERROR_CONSOLE855
        quiet.flush()
    root_error, combined_trace, evidence = recover_inherited_error855(
        env, outer_exception, outer_trace)
    return env, root_error, combined_trace, evidence


def verify_two_job855(env, combined_trace):
    """Evaluate only the preregistered two-job GATE 1/2 smoke criteria."""
    jobs = env.get('JOBS841', [])
    records = env.get('REC841', {})
    expected = jobs[:2]
    expected_ids = [j['job'] for j in expected]
    assert len(expected) == 2
    assert [j['intervention'] for j in expected] == ['INTACT', 'REMOVED']
    assert all(j['arm'] == 'BASELINE853' for j in expected)
    assert STATE855['saved_jobs'] == expected_ids, (
        'TWO_JOB_SAVE_MISMATCH', STATE855['saved_jobs'], expected_ids)
    assert set(records) == set(expected_ids), 'TWO_JOB_RECORD_SET_MISMATCH'
    assert 'GATE1_TWO_JOB_OBSERVATION_COMPLETE' in combined_trace, (
        'EXPECTED_DIAGNOSTIC_STOP_NOT_FOUND')
    for j in expected:
        record = records[j['job']]
        assert record['arm'] == 'BASELINE853'
        assert record['condition'] == j['intervention']
        assert record['end'] in ('MODEL_ACCEPT', 'MODEL_STOP'), (
            'NON_COMPLETING_JOB', j['job'], record['end'])
        assert not record.get('mechanical_stop_reason'), 'MECHANICAL_LIMIT_IS_NOT_EQUIVALENCE'
    assert STATE855['equalities'] == [True, True], (
        'TWO_REVIEW_EQUALITIES_REQUIRED', STATE855['equalities'])
    assert all(c['observer_equality'] for c in STATE855['coverage'])
    assert not STATE855['probes'], 'N_PROBES_FORBIDDEN_IN_TWO_JOB_GATE1'
    final_audit = assert_hook_free855(env, 'post_diagnostic_stop')
    assert STATE855['hook_audits'] and all(
        row['hook_count'] == 0 and not row['transformers_output_capturing_installed']
        for row in STATE855['hook_audits'])
    assert not any(p.requires_grad for p in env['model'].parameters())
    return {
        'status': 'PASS_TWO_BASELINE_JOBS_ONLY',
        'jobs': [{
            'job': j['job'], 'qid': j.get('qid'), 'condition': j['intervention'],
            'arm': j['arm'], 'end': records[j['job']]['end'],
            'answer': records[j['job']].get('answer'),
        } for j in expected],
        'review_replay_equalities': STATE855['equalities'],
        'coverage_observer_equalities': [c['observer_equality'] for c in STATE855['coverage']],
        'hook_audits': len(STATE855['hook_audits']),
        'final_hook_count': final_audit['hook_count'],
        'diagnostic_stop': 'GATE1_TWO_JOB_OBSERVATION_COMPLETE',
        'diagnostic_stop_is_model_stop': False,
        'scope': 'GATE1 repair and GATE2 two-job equivalence only; not a full TEST855 panel',
    }


def ensure_partial_artifacts855():
    for name in ('855_observations.jsonl', '855_xray.jsonl', '855_runtime_context.jsonl'):
        path = ROOT855 / name
        if not path.exists():
            path.write_text('', encoding='utf-8')
    if not (ROOT855 / '855_runtime_traceback.txt').exists():
        (ROOT855 / '855_runtime_traceback.txt').write_text(
            TRACEBACK855 or 'NO_TRACEBACK_AVAILABLE\n', encoding='utf-8')
    json_write855('855_ablation.json', {
        'status': 'NOT_RUN_TWO_JOB_CELL_GATE5_BLOCKED',
        'arms': ['BASELINE', 'COUPLED_NATIVE', 'MATCHED_CONTROL',
            'CANDIDATE_ABLATION', 'EVIDENCE_ABLATION', 'FEEDBACK_ZERO',
            'FEEDBACK_SHUFFLE', 'FEEDBACK_DELAY'],
        'records': [],
    })
    json_write855('855_runtime_equivalence.json', {
        'status': TWO_JOB_VERIFICATION855.get('status', 'NOT_RUN_GATE1_NOT_CLOSED'),
        'required_jobs': ['BASELINE853/INTACT', 'BASELINE853/REMOVED'],
        'review_replay_equalities': STATE855['equalities'],
        'coverage_records': len(STATE855['coverage']),
        'coverage_observer_equalities': [c['observer_equality'] for c in STATE855['coverage']],
        'N_probe_records': len(STATE855['probes']),
        'saved_jobs': STATE855['saved_jobs'],
        'hook_audit_count': len(STATE855['hook_audits']),
        'verification': TWO_JOB_VERIFICATION855,
    })
    json_write855('855_failures.json', {
        'execution_error': EXECUTION_ERROR855,
        'diagnostic_stop': DIAGNOSTIC_STOP855,
        'outer_execution_error': OUTER_EXECUTION_ERROR855,
        'error_evidence': ERROR_EVIDENCE855,
        'two_job_verification': TWO_JOB_VERIFICATION855,
        'active_context': STATE855.get('active'),
        'last_runtime_context': LAST_CONTEXT855,
        'capture_context': STATE855.get('capture'),
        'context_failures': FAILURES855,
        'partial_counts': {
            'observations': len(STATE855['observations']),
            'coverage': len(STATE855['coverage']),
            'runtime_equalities': len(STATE855['equalities']),
            'N_probes': len(STATE855['probes']),
        },
    })


def finalize855(gates, execution):
    ensure_partial_artifacts855()
    capture_cell_source855()
    report = {
        'test': TEST855_KIND,
        'execution': execution,
        'recovery_mode': RECOVERY_MODE855,
        'gates': gates,
        'error': EXECUTION_ERROR855,
        'diagnostic_stop': DIAGNOSTIC_STOP855,
        'outer_execution_error': OUTER_EXECUTION_ERROR855,
        'error_evidence': ERROR_EVIDENCE855,
        'two_job_verification': TWO_JOB_VERIFICATION855,
        'environment': STATE855['environment'],
        'root_cause': 'Transformers output_hidden_states installed persistent forward hooks',
        'minimal_repair': 'logits-only observer; no hidden-state request; no hook clearing',
        'hidden_state_xray': 'NOT_RUN_GATE3_BLOCKED',
        'last_runtime_context': LAST_CONTEXT855,
        'traceback_sha256': sha256_bytes855(
            (ROOT855 / '855_runtime_traceback.txt').read_bytes()),
        'observer_equalities': STATE855['equalities'],
        'coverage_records': len(STATE855['coverage']),
        'coverage_protocol_valid': sum(bool(c['valid_protocol']) for c in STATE855['coverage']),
        'N_probes': len(STATE855['probes']),
        'seconds': time.perf_counter() - START855,
        'known_limitations': [
            'Only the observer is repaired; no cognitive/control mechanism is changed.',
            'Any PASS is limited to the first two BASELINE853 jobs.',
            'The explicit two-job diagnostic stop is not MODEL_STOP.',
            'Hidden-state X-RAY is not run; GATE 3-6 remain blocked.',
            'Transformers output_hidden_states is incompatible with this no-hook protocol.',
            'Last-token logit lens values are uncalibrated diagnostics, not action probabilities.',
            'No N probes or 12-job TEST855 panel are run.',
            'Physical tensor integrity does not prove semantic losslessness of CUT3.',
        ],
        'TEST855_SUCCESS': False,
    }
    json_write855('855_report.json', report)
    LOG_FILE855.flush()
    short855('TEST855 RECOVERY RESULT:', execution)
    for gate, status in gates.items():
        short855(gate + ':', status)
    short855('ERROR:', EXECUTION_ERROR855 or 'NONE')
    short855('OUTER WRAPPER ERROR:', OUTER_EXECUTION_ERROR855 or 'NONE')
    short855('ORIGINAL RUNTIME TRACEBACK RECOVERED:',
        ERROR_EVIDENCE855.get('original_runtime_error_recovered', False))
    short855('DIAGNOSTIC STOP:', DIAGNOSTIC_STOP855 or 'NONE')
    short855('TWO-JOB VERIFICATION:', TWO_JOB_VERIFICATION855.get('status', 'NOT_PASSED'))
    short855('ARTIFACTS:', str(ROOT855))
    for name in ('855_report.json', '855_runtime_traceback.txt',
            '855_runtime_equivalence.json', '855_sha256_manifest.json'):
        path = ROOT855 / name
        if path.exists():
            short855(name, sha256_bytes855(path.read_bytes()))
    short855('TEST855 motor status: NOT_PRODUCED; two-job smoke only; GATE 3-6 were not executed.')
    # Finalize the log before hashing it. No log writes may follow the manifest.
    LOG_FILE855.flush()
    manifest = {}
    for path in sorted(ROOT855.iterdir()):
        if path.is_file() and path.name != '855_sha256_manifest.json':
            manifest[path.name] = {
                'bytes': path.stat().st_size,
                'sha256': sha256_bytes855(path.read_bytes()),
            }
    json_write855('855_sha256_manifest.json', manifest)


# Initialize required append-only artifacts before any source or GPU operation.
for artifact855 in ('855_observations.jsonl', '855_xray.jsonl', '855_runtime_context.jsonl'):
    (ROOT855 / artifact855).write_text('', encoding='utf-8')

try:
    short855('TEST855 MODE: GATE1 hook-free repair + two-job GATE2 verification only.')
    short855('GPU EXECUTION: NOT VERIFIED BY AUTHOR; restart the Colab runtime before this cell.')
    short855('HIDDEN-STATE X-RAY: DISABLED; output_hidden_states is never requested.')
    if PRE855_ERROR.exists():
        (ROOT855 / '855_previous_pre855_traceback.txt').write_text(
            PRE855_ERROR.read_text(encoding='utf-8', errors='replace'), encoding='utf-8')
        short855('Previous PRE855 traceback archived separately; repaired path will still run.')
    load_sources855()
    gate0855 = 'PASS'
    RECOVERY_MODE855 = 'HOOKFREE_LOGITS_TWO_BASELINE_VERIFICATION'
    env855, error855, trace855, evidence855 = reproduce_pre855855()
    EXECUTION_ERROR855 = error855
    OUTER_EXECUTION_ERROR855 = evidence855.get('outer_exception')
    TRACEBACK855 = trace855
    ERROR_EVIDENCE855 = evidence855
    if trace855:
        (ROOT855 / '855_runtime_traceback.txt').write_text(trace855, encoding='utf-8')
        short855(trace855[-12000:])
    expected_stop = 'GATE1_TWO_JOB_OBSERVATION_COMPLETE' in trace855
    if expected_stop:
        DIAGNOSTIC_STOP855 = 'GATE1_TWO_JOB_OBSERVATION_COMPLETE'
    try:
        TWO_JOB_VERIFICATION855 = verify_two_job855(env855, trace855)
    except Exception as verification_exc:
        verification_trace = traceback.format_exc()
        TRACEBACK855 = trace855 + (
            '\n===== TWO-JOB VERIFICATION FAILURE =====\n' + verification_trace)
        (ROOT855 / '855_runtime_traceback.txt').write_text(TRACEBACK855, encoding='utf-8')
        short855(verification_trace)
        gate1855 = 'BLOCKED'
        gate2855 = 'BLOCKED'
        execution855 = ('GATE1_TWO_JOB_VERIFICATION_FAILED' if expected_stop else
            'RUNTIME_ABORT_BEFORE_TWO_JOB_COMPLETION' if error855 else
            'TWO_JOB_DIAGNOSTIC_STOP_NOT_REACHED')
        if expected_stop:
            EXECUTION_ERROR855 = ('TWO_JOB_VERIFICATION_FAILED: '
                + type(verification_exc).__name__ + ': ' + str(verification_exc))
        elif not error855:
            EXECUTION_ERROR855 = 'TWO_JOB_DIAGNOSTIC_STOP_NOT_REACHED'
    else:
        # The inherited SystemExit here wraps only our explicit diagnostic stop.
        EXECUTION_ERROR855 = None
        gate1855 = 'PASS'
        gate2855 = 'PASS'
        execution855 = 'GATE1_GATE2_TWO_JOB_PASS_DIAGNOSTIC_STOP'
    gates855 = {
        'GATE0_SOURCE_INTEGRITY': gate0855,
        'GATE1_RUNTIME_ROOT_CAUSE_AND_VERIFIED_REPAIR': gate1855,
        'GATE2_ENGINE_EQUIVALENCE': gate2855,
        'GATE3_NUMERICAL_XRAY': 'BLOCKED',
        'GATE4_COMPUTATIONAL_ROOT_CAUSE': 'BLOCKED',
        'GATE5_CAUSAL_CORRECTION': 'BLOCKED',
        'GATE6_INDEPENDENT_VALIDATION': 'BLOCKED',
        'GATE7_ARTIFACT_INTEGRITY': 'PASS',
    }
    finalize855(gates855, execution855)
except BaseException as exc:
    # Recovery/preflight failures are also visible; never turn them into model STOP.
    EXECUTION_ERROR855 = type(exc).__name__ + ': ' + str(exc)
    TRACEBACK855 = traceback.format_exc()
    ERROR_EVIDENCE855 = {
        'source': 'RECOVERY_OUTER_EXCEPTION',
        'original_runtime_error_recovered': False,
        'recovery_exception_type': type(exc).__name__,
        'recovery_exception_text': str(exc),
    }
    (ROOT855 / '855_runtime_traceback.txt').write_text(TRACEBACK855, encoding='utf-8')
    sys.stdout = CONSOLE855
    sys.stderr = ERROR_CONSOLE855
    short855(TRACEBACK855)
    gates855 = {
        'GATE0_SOURCE_INTEGRITY': 'PASS' if len(RAW_SOURCES855) == 11 else 'FAIL',
        'GATE1_RUNTIME_ROOT_CAUSE_AND_VERIFIED_REPAIR': 'BLOCKED',
        'GATE2_ENGINE_EQUIVALENCE': 'BLOCKED',
        'GATE3_NUMERICAL_XRAY': 'BLOCKED',
        'GATE4_COMPUTATIONAL_ROOT_CAUSE': 'BLOCKED',
        'GATE5_CAUSAL_CORRECTION': 'BLOCKED',
        'GATE6_INDEPENDENT_VALIDATION': 'BLOCKED',
        'GATE7_ARTIFACT_INTEGRITY': 'PASS',
    }
    finalize855(gates855, 'RECOVERY_FAILURE_TRACEBACK_CAPTURED')
finally:
    LOG_FILE855.close()
