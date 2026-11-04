# AKBASCORE SILICON HIPPOCAMPUS — TEST855 GATE 1 RECOVERY
# Diagnostic recovery cell, NOT a completed TEST855 motor.
# It never guesses or automatically repairs the unknown PRE855 RuntimeError.
# If the original traceback exists, it archives it without loading the model.
# Otherwise it reproduces the original PRE855 X-RAY path with added context logging.
# It also recovers the inherited TEST841_ERROR/_tbtext841 pair hidden by SystemExit.
# GATE 2-6 remain blocked in either case. GPU execution is not claimed by the author.
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

TEST855_KIND = 'GATE1_RECOVERY_NOT_FULL_TEST855'
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
    'start': START855,
}
FAILURES855 = []
EXECUTION_ERROR855 = None
OUTER_EXECUTION_ERROR855 = None
TRACEBACK855 = ''
ERROR_EVIDENCE855 = {}
LAST_CONTEXT855 = None
RECOVERY_MODE855 = 'NOT_STARTED'


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
            'AKBASCORE SILICON HIPPOCAMPUS — TEST855 GATE 1 RECOVERY' in text]
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


LAYERS855 = (0, 4, 20, 40, 60, 79, 80)
# Layers 0-79 are real decoder blocks. Entry 80 is the final-RMSNorm output,
# not an invented 81st decoder block.
SPELLINGS855 = (' CONTINUE', ' REVISE', ' STOP', ' SUFFICIENT', ' INSUFFICIENT')


def capture855(out, local):
    # Public returned hidden states only: no hooks, layer replacement or reinjection.
    g = STATE855['g']
    torch = g['torch']
    np = g['np']
    hs = out.hidden_states
    assert hs is not None and len(hs) == g['NL'] + 1 == 81
    logits = out.logits[0, -1].detach().float()
    hlen = int(hs[0].shape[1])
    positions = {hlen - 1}
    if hlen > 1:
        for start, rows in local.get('checks', []):
            positions.update((int(start), int(start) + len(rows) - 1))
    positions = sorted(positions)
    step = len(STATE855['frames'])
    STATE855['capture'] = {
        **current_job855(g),
        'stage': None if not STATE855.get('active') else STATE855['active']['label'],
        'step': step,
        'hidden_sequence_length': hlen,
        'positions': positions,
        'logits_shape': list(logits.shape),
        'logits_dtype': str(logits.dtype),
        'logits_device': str(logits.device),
    }
    record = {
        'step': step,
        'positions': positions,
        'layers': {},
        'returned_hidden_bytes': sum(h.numel() * h.element_size() for h in hs),
        'tokenizations': STATE855['tokenizations'],
        'lens': 'diagnostic first-token logits, NOT action probabilities',
        'hidden_sequence_length': hlen,
        'last_hidden_shape': list(hs[-1].shape),
        'last_hidden_dtype': str(hs[-1].dtype),
        'last_hidden_device': str(hs[-1].device),
    }
    for layer in LAYERS855:
        h = hs[layer][0, positions].detach()
        assert h.shape[-1] == 8192 and torch.isfinite(h).all()
        array = h.float().cpu().numpy()
        STATE855['arrays']['step%d_layer%d' % (step, layer)] = array
        # Layer 80 is already final-RMSNorm output; do not normalize twice.
        value = h[-1:]
        value = g['model'].model.norm(value) if layer != 80 else value
        scores = (logits[STATE855['first_ids']].cpu().tolist() if layer == 80 else
            (value.float() @ STATE855['head_rows'].T).reshape(-1).cpu().tolist())
        record['layers'][str(layer)] = {
            'norms': np.linalg.norm(array, axis=1).tolist(),
            'first_token_logits': dict(zip(SPELLINGS855, scores)),
            'stop_minus_revise': scores[2] - scores[1],
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
                n.value.keywords.append(ast.keyword(arg='output_hidden_states',
                    value=ast.Constant(True)))
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

        def visit_Call(self, n):
            self.generic_visit(n)
            if isinstance(n.func, ast.Name) and n.func.id == 'model':
                n.keywords = [k for k in n.keywords if k.arg != 'output_hidden_states']
            return n

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
    short855('GPU:', torch.cuda.get_device_name(0), '| frozen NF4 | BF16 | layers=80 H=8192',
        '| free GiB=', round(torch.cuda.mem_get_info()[0] / 1024 ** 3, 2))
    tokens = [list(g['tok'](s, add_special_tokens=False).input_ids) for s in SPELLINGS855]
    assert all(tokens)
    STATE855['tokenizations'] = dict(zip(SPELLINGS855, tokens))
    STATE855['first_ids'] = [value[0] for value in tokens]
    # Diagnostic projection only. These tensors never enter generation.
    STATE855['head_rows'] = g['model'].lm_head.weight[STATE855['first_ids']].detach().float()
    g['_xr_capture'] = capture855
    gen = g['gen851']
    observed = clone_observer855(STATE855['functions']['gen851'], g)
    inv = g['invoke851']
    gen_coverage = clone_observer855(STATE855['functions']['gen849'], g)
    old_coverage = g['coverage_state852']

    def observe_coverage(q, condition, mode, memx):
        fresh = (q, condition, mode) not in g['COVERAGE_SHARED852']
        h = old_coverage(q, condition, mode, memx)
        if fresh:
            pre = list(g['prompt_ids'](g['COVERAGE852'].format(q=g['QTEXT841'][q])))
            with runtime_context855('coverage_replay', g, None, pre,
                    g['COVERAGE_SUFFIX852']) as active:
                STATE855['arrays'] = {}
                STATE855['frames'] = []
                active['substep'] = 'observed_coverage_generator'
                obs = gen_coverage(memx, pre, None, g['COVERAGE_SUFFIX852'])
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
            checked = stage == 'review_0' and g['condition851'] == 'INTACT'
            active['substep'] = 'reference_generator' if checked else 'not_applicable'
            reference = gen(memx, pre, segments, post) if checked else None
            g['gen851'] = observed
            try:
                active['substep'] = 'observed_generator'
                h = inv(memx, pre, segments, post, stage, tensors, traces, baseline=False)
            finally:
                g['gen851'] = gen
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
            # Four locked probes, unchanged from PRE855. They are OOD diagnostics,
            # not a proposed cognitive correction and never feed the original h.
            if stage == 'review_0' and g['arm851'] == 'NATIVE854':
                active['substep'] = 'N_half_feature_rotation_probe'
                changed = []
                hits = 0
                for slot, rows in segments:
                    if slot == g['N_SLOT854']:
                        z = torch.roll(rows, shifts=4096, dims=1).contiguous()
                        hits += 1
                        assert z.shape == rows.shape and z.dtype == rows.dtype and z.device == rows.device
                        assert torch.allclose(z.norm(dim=1), rows.norm(dim=1), rtol=1e-6, atol=1e-6)
                        changed.append((slot, z))
                    else:
                        changed.append((slot, rows))
                assert hits == 1
                p = gen(memx, pre, changed, post)
                probe = {
                    **identity,
                    'intervention': 'N_HALF_FEATURE_ROTATION',
                    'distribution_shift': 'OOD; effect does not prove semantic sufficiency',
                    'original': g['result849'](h),
                    'control': g['result849'](p),
                    'action_changed': g['parse849'](h['text']) != g['parse849'](p['text']),
                }
                STATE855['probes'].append(probe)
                np.savez_compressed(ROOT855 / ('probe_%02d.npz' % len(STATE855['probes'])),
                    original_N=segments[-1][1].numpy(),
                    control_N=changed[-1][1].numpy(),
                    original_output=h['rows'].numpy(),
                    control_output=p['rows'].numpy())
                json_write855('855_paired_N_probes.json', STATE855['probes'])
            return h

    g['invoke851'] = wrapped
    short855('OBSERVER: AST inverse check PASS; no hooks; runtime equality pending.')


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
            'change': 'one observer installation before experiment; generator computation AST unchanged',
            'layers': LAYERS855,
            'layer_80_meaning': 'final-RMSNorm output, not decoder block 80',
            'original_jobs': 12,
            'review_equality_replays': 6,
            'coverage_equality_replays': 4,
            'N_probes': 4,
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


def ensure_partial_artifacts855():
    for name in ('855_observations.jsonl', '855_xray.jsonl', '855_runtime_context.jsonl'):
        path = ROOT855 / name
        if not path.exists():
            path.write_text('', encoding='utf-8')
    if not (ROOT855 / '855_runtime_traceback.txt').exists():
        (ROOT855 / '855_runtime_traceback.txt').write_text(
            TRACEBACK855 or 'NO_TRACEBACK_AVAILABLE\n', encoding='utf-8')
    json_write855('855_ablation.json', {
        'status': 'NOT_RUN_GATE1_NOT_CLOSED',
        'arms': ['BASELINE', 'COUPLED_NATIVE', 'MATCHED_CONTROL',
            'CANDIDATE_ABLATION', 'EVIDENCE_ABLATION', 'FEEDBACK_ZERO',
            'FEEDBACK_SHUFFLE', 'FEEDBACK_DELAY'],
        'records': [],
    })
    json_write855('855_runtime_equivalence.json', {
        'status': 'NOT_RUN_GATE1_NOT_CLOSED',
        'required_jobs': ['BASELINE853/INTACT', 'BASELINE853/REMOVED'],
        'review_replay_equalities': STATE855['equalities'],
        'coverage_records': len(STATE855['coverage']),
        'N_probe_records': len(STATE855['probes']),
    })
    json_write855('855_failures.json', {
        'execution_error': EXECUTION_ERROR855,
        'outer_execution_error': OUTER_EXECUTION_ERROR855,
        'error_evidence': ERROR_EVIDENCE855,
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
        'outer_execution_error': OUTER_EXECUTION_ERROR855,
        'error_evidence': ERROR_EVIDENCE855,
        'last_runtime_context': LAST_CONTEXT855,
        'traceback_sha256': sha256_bytes855(
            (ROOT855 / '855_runtime_traceback.txt').read_bytes()),
        'observer_equalities': STATE855['equalities'],
        'coverage_records': len(STATE855['coverage']),
        'coverage_protocol_valid': sum(bool(c['valid_protocol']) for c in STATE855['coverage']),
        'N_probes': len(STATE855['probes']),
        'seconds': time.perf_counter() - START855,
        'known_limitations': [
            'No automatic RuntimeError repair is attempted or claimed.',
            'Recovering the original traceback does not by itself close GATE 1.',
            'GATE 1 cannot PASS without a root cause and a verified minimal repair.',
            'GATE 2-6 are not executed by this recovery cell.',
            'Intermediate first-token logit lens values are uncalibrated diagnostics.',
            'N rotation is out of distribution and does not establish semantic sufficiency.',
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
    short855('ARTIFACTS:', str(ROOT855))
    for name in ('855_report.json', '855_runtime_traceback.txt',
            '855_runtime_equivalence.json', '855_sha256_manifest.json'):
        path = ROOT855 / name
        if path.exists():
            short855(name, sha256_bytes855(path.read_bytes()))
    short855('TEST855 motor status: NOT_PRODUCED; GATE 2-6 were not executed.')
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
    short855('TEST855 MODE: GATE1 recovery/diagnosis only; no full-motor claim.')
    short855('GPU EXECUTION: NOT VERIFIED BY AUTHOR; this Colab run determines it.')
    load_sources855()
    gate0855 = 'PASS'
    if PRE855_ERROR.exists():
        RECOVERY_MODE855 = 'EXISTING_TRACEBACK_ARCHIVED_NO_GPU_RELOAD'
        TRACEBACK855 = PRE855_ERROR.read_text(encoding='utf-8', errors='replace')
        ERROR_EVIDENCE855 = {
            'source': str(PRE855_ERROR),
            'original_runtime_error_recovered': None,
            'original_traceback_source': 'PRE855_ERROR_FILE_UNCLASSIFIED',
            'note': 'Archived verbatim; no root-cause or repair verification is inferred.',
        }
        (ROOT855 / '855_runtime_traceback.txt').write_text(TRACEBACK855, encoding='utf-8')
        EXECUTION_ERROR855 = 'PRE855_TRACEBACK_FOUND_ROOT_CAUSE_AND_REPAIR_NOT_VERIFIED'
        short855('Existing PRE855 traceback archived:', str(PRE855_ERROR))
        short855(TRACEBACK855[-6000:])
        gates855 = {
            'GATE0_SOURCE_INTEGRITY': gate0855,
            'GATE1_RUNTIME_ROOT_CAUSE_AND_VERIFIED_REPAIR': 'BLOCKED',
            'GATE2_ENGINE_EQUIVALENCE': 'BLOCKED',
            'GATE3_NUMERICAL_XRAY': 'BLOCKED',
            'GATE4_COMPUTATIONAL_ROOT_CAUSE': 'BLOCKED',
            'GATE5_CAUSAL_CORRECTION': 'BLOCKED',
            'GATE6_INDEPENDENT_VALIDATION': 'BLOCKED',
            'GATE7_ARTIFACT_INTEGRITY': 'PASS',
        }
        finalize855(gates855, 'BLOCKED_EXISTING_TRACEBACK_REQUIRES_VERIFIED_REPAIR')
    else:
        RECOVERY_MODE855 = 'ORIGINAL_PRE855_PATH_REPRODUCTION'
        short855('PRE855 error.txt not found; reproducing the original failure path.')
        env855, error855, trace855, evidence855 = reproduce_pre855855()
        EXECUTION_ERROR855 = error855
        OUTER_EXECUTION_ERROR855 = evidence855.get('outer_exception')
        TRACEBACK855 = trace855
        ERROR_EVIDENCE855 = evidence855
        if trace855:
            (ROOT855 / '855_runtime_traceback.txt').write_text(trace855, encoding='utf-8')
            short855(trace855[-12000:])
        if error855:
            gate1855 = 'BLOCKED'
            execution855 = ('RUNTIME_ABORT_ORIGINAL_TRACEBACK_CAPTURED'
                if evidence855.get('original_runtime_error_recovered')
                else 'RUNTIME_ABORT_OUTER_TRACEBACK_ONLY')
        else:
            # A non-reproduction is not a verified repair and cannot close GATE 1.
            gate1855 = 'UNRESOLVED'
            execution855 = 'NO_FAILURE_REPRODUCED_REPAIR_NOT_VERIFIED'
            EXECUTION_ERROR855 = 'NO_FAILURE_REPRODUCED_NO_VERIFIED_REPAIR'
            (ROOT855 / '855_runtime_traceback.txt').write_text(
                'NO_RUNTIME_ERROR_REPRODUCED; NO VERIFIED REPAIR; GATE1 UNRESOLVED\n',
                encoding='utf-8')
        gates855 = {
            'GATE0_SOURCE_INTEGRITY': gate0855,
            'GATE1_RUNTIME_ROOT_CAUSE_AND_VERIFIED_REPAIR': gate1855,
            'GATE2_ENGINE_EQUIVALENCE': 'BLOCKED',
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
