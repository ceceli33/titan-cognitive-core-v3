# TEST905 — CPU tests (no torch, no model, no GPU). What runs for real here: geometry / manifest, E-row slicing, storage
# independence, the B-state transport (RoPE on K exactly once, V untouched, lower + prefix bit-equal) checked against an
# independent float64 RoPE and a second complex-number RoPE, write_upper / read_upper / read_mount code paths on a numpy-backed
# mini tensor ("FT") with view / storage semantics, record integrity, verdicts, --recompute, Drive delivery states, executed-source
# identity, import safety. What does NOT run here: the model, the real tokenizer, real 903 cartridges, transformers' cache — all
# measured on the A100 (GATE_ENGINE_905 / GATE_WRITE_905 / GATE_ROPE_905 / per-read transport checks).
# Inputs: T905_FILE (905.py), T905_904 (pinned 904.py, blob 2ffacbec), T905_903 (pinned 903.py, blob f883d3df).
import copy, hashlib, importlib.util, json, os, pickle, stat, sys, types
from pathlib import Path
import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
SP = Path('/tmp/claude-0/-home-claude/d0129315-168d-5dfe-a7d4-13aaaac1bc6c/scratchpad/k905')
F905 = Path(os.environ.get('T905_FILE', HERE.parent / '905.py'))
F904 = Path(os.environ.get('T905_904', SP / 'gh/904.py')); F903 = Path(os.environ.get('T905_903', SP / 'gh/903.py'))


def load(path=F905, name='m905'):
    spec = importlib.util.spec_from_file_location('%s_%d' % (name, id(object())), path); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m


def sha(b): return hashlib.sha256(b).hexdigest()


@pytest.fixture
def M():
    m = load(); m.M4 = load(F904, 'm904'); return m


# ================================================================================================ mini tensor with storage semantics
class FT:
    """numpy-backed stand-in for a torch tensor: slicing returns a VIEW sharing the base storage (as torch does)."""
    def __init__(self, a, base=None): self.a = a; self.base = base if base is not None else a
    @property
    def shape(self): return self.a.shape
    def __getitem__(self, i): return FT(self.a[i], self.base)
    def detach(self): return self
    def to(self, *a, **k): return self
    def cpu(self): return self
    def float(self): return FT(self.a.astype(np.float32))
    def clone(self): return FT(self.a.copy())
    def contiguous(self): return self if self.a.flags['C_CONTIGUOUS'] and self.base is self.a else FT(np.ascontiguousarray(self.a), self.base)
    def numpy(self): return self.a
    def numel(self): return self.a.size
    def element_size(self): return self.a.itemsize
    def is_contiguous(self): return bool(self.a.flags['C_CONTIGUOUS'])
    def storage_offset(self):
        return 0 if self.base is self.a else int((self.a.__array_interface__['data'][0] - self.base.__array_interface__['data'][0]) // self.a.itemsize)
    def untyped_storage(self): return types.SimpleNamespace(nbytes=lambda: self.base.nbytes)
    def norm(self): return float(np.linalg.norm(self.a))


def ft_cat(ts, dim): return FT(np.concatenate([t.a for t in ts], axis=dim))


def np_rephase(theta, dim):
    M_ = load()
    def reph(k, old, new):
        old = list(np.asarray(old)); new = list(np.asarray(new))
        if old == new: return k
        return FT(M_.rope_move_np(k.a.astype(np.float64), old, new, theta, dim).astype(k.a.dtype))
    return reph


THETA, D, KVH, L = 1.0e6, 16, 2, 80


def mem_rows(seed, rows, L=L):
    r = np.random.default_rng(seed); return [(FT(r.standard_normal((1, KVH, rows, D)).astype(np.float32)), FT(r.standard_normal((1, KVH, rows, D)).astype(np.float32))) for _ in range(L)]


def upper_rows(seed, n=19, L=L, cut=3):
    r = np.random.default_rng(seed); return [(FT(r.standard_normal((1, KVH, n, D)).astype(np.float32)), FT(r.standard_normal((1, KVH, n, D)).astype(np.float32))) for _ in range(L - cut - 1)]


# ================================================================================================ geometry, slicing, storage
def test_slice_rows_sequence_axis_only(M):
    a = np.arange(1 * 8 * 68 * 4).reshape(1, 8, 68, 4).astype(np.float32); s = M.slice_rows(FT(a), 49, 19, 8, 4)
    assert s.shape == (1, 8, 19, 4) and np.array_equal(s.a, a[:, :, 49:68, :])
    with pytest.raises(M.Stop905): M.slice_rows(FT(a.transpose(0, 2, 1, 3).copy()), 49, 19, 8, 4)     # (1,68,8,4): wrong axis
    with pytest.raises(M.Stop905): M.slice_rows(FT(a[:, :, :60, :]), 49, 19, 8, 4)                   # too few rows
    with pytest.raises(M.Stop905): M.slice_rows(FT(a[0]), 49, 19, 8, 4)                              # wrong rank


def test_storage_independence_detects_parent_view(M):
    big = FT(np.zeros((1, 8, 68, 4), np.float32)); view = big[:, :, 49:68, :]
    assert not M.storage_independent(view) and not M.storage_independent(view.contiguous())          # still the parent's storage
    assert M.storage_independent(view.clone().contiguous())


def test_expected_geometry_903_numbers(M):
    c = {'key': 'C1_H1', 'kind': 'CHILD', 'n': 19, 'body_tokens': 19, 'pos0': 49}; u = {'key': 'UP_H1', 'kind': 'UPPER', 'n': 19, 'body_tokens': 19, 'pos0': 49}
    h = {'key': 'h1_H2', 'kind': 'NATIVE', 'n': 49, 'body_tokens': 19, 'pos0': None}; tc = {'key': 'TC_R', 'kind': 'CHILD', 'n': 19, 'body_tokens': 19, 'pos0': 49}
    e = {'key': 'E_IND', 'kind': 'NATIVE', 'n': 49, 'body_tokens': 19, 'pos0': None}
    assert M.expected_geometry('B_STRAIGHT_A', [c, u]) == (49, [{'key': 'C1_H1', 'part': 'L0-L3+H3', 'source_pos0': 49, 'target_pos0': 30},
                                                               {'key': 'UP_H1', 'part': 'L4-L79 K (V unrotated)', 'source_pos0': 49, 'target_pos0': 30}])
    assert M.expected_geometry('A_STRAIGHT_A', [c])[0] == 49 and M.expected_geometry('A_STRAIGHT_A', [c])[1][0]['target_pos0'] == 30
    n, rope = M.expected_geometry('TR_SOURCE_R', [h, tc]); assert n == 68 and [r['source_pos0'] for r in rope] == [30, 49] == [r['target_pos0'] for r in rope]
    assert M.expected_geometry('POS_FULL_REF_H1', [h, e])[0] == 68 and M.expected_geometry('NEG_EMPTY_PREFIX', [])[0] == 30
    assert M.GEOM['parent_rows'] == [30, 49] and M.GEOM['source_E_rows'] == [49, 68] and M.GEOM['clean_E_rows'] == [30, 49] and M.GEOM['query_start_clean'] == 49


# ================================================================================================ RoPE transport (B state)
def test_independent_rope_two_formulations_agree(M):
    x = np.random.default_rng(1).standard_normal((1, 2, 19, D)); a = M.rope_move_np(x, range(49, 68), range(30, 49), THETA, D)
    inv = 1.0 / (THETA ** (np.arange(0, D, 2) / D)); h = D // 2                 # complex-number RoPE: pair (i, i+D/2) rotated by angle
    z = x[..., :h] + 1j * x[..., h:]; ang = np.outer(np.arange(30, 49) - np.arange(49, 68), inv); z2 = z * np.exp(1j * ang)
    b = np.concatenate([z2.real, z2.imag], -1); assert np.max(np.abs(a - b)) < 1e-9
    assert np.max(np.abs(M.rope_move_np(x, range(49, 68), range(49, 68), THETA, D) - x)) < 1e-12   # identity at source == target


def test_transport_correct_and_verified(M):
    mem = mem_rows(2, 49); up = upper_rows(3); reph = np_rephase(THETA, D)
    out = M.transport_upper(mem, up, 49, 30, 19, reph, ft_cat, lambda a, b: np.arange(a, b), cut=3)
    G = M.verify_transport(out, mem, up, 49, 30, 19, lambda t: t.float().numpy(), THETA, D); assert G['ok'], G
    assert all(out[i] is mem[i] for i in range(4)) and np.array_equal(out[10][1].a[:, :, 30:, :], up[6][1].a)


def test_transport_identity_at_source_equals_target(M):
    mem = mem_rows(4, 49); up = upper_rows(5)
    out = M.transport_upper(mem, up, 30, 30, 19, np_rephase(THETA, D), ft_cat, lambda a, b: np.arange(a, b))
    assert all(np.array_equal(out[li][0].a[:, :, 30:, :], up[li - 4][0].a) for li in range(4, 80))   # K bit-identical, no rotation


@pytest.mark.parametrize('bug', ['k_twice', 'k_none', 'v_rotated', 'lower_touched', 'prefix_touched', 'wrong_target'])
def test_transport_bugs_are_caught(M, bug):
    mem = mem_rows(6, 49); up = upper_rows(7); reph = np_rephase(THETA, D); ar = lambda a, b: np.arange(a, b)
    out = M.transport_upper(mem, up, 49, 30, 19, reph, ft_cat, ar)
    if bug == 'k_twice': out = M.transport_upper(mem, [(reph(k, ar(49, 68), ar(30, 49)), v) for k, v in up], 49, 30, 19, reph, ft_cat, ar)
    if bug == 'k_none': out = M.transport_upper(mem, up, 49, 30, 19, lambda k, o, n: k, ft_cat, ar)
    if bug == 'v_rotated': out = [o if i < 4 else (o[0], ft_cat((mem[i][1][:, :, :30, :], reph(up[i - 4][1], ar(49, 68), ar(30, 49))), -2)) for i, o in enumerate(out)]
    if bug == 'lower_touched': out = list(out); out[2] = (out[2][0].clone(), out[2][1])
    if bug == 'prefix_touched':
        k = out[40][0].a.copy(); k[0, 0, 3, 0] += 1.0; out = list(out); out[40] = (FT(k), out[40][1])
    if bug == 'wrong_target': out = M.transport_upper(mem, up, 49, 30, 19, lambda k, o, n: reph(k, o, n + 1), ft_cat, ar)
    G = M.verify_transport(out, mem, up, 49, 30, 19, lambda t: t.float().numpy(), THETA, D)
    assert not G['ok'], (bug, G)
    want = {'k_twice': 'k_moved_once', 'k_none': 'k_moved_once', 'v_rotated': 'v_unrotated_bitwise', 'lower_touched': 'lower_untouched',
            'prefix_touched': 'prefix_rows_bitwise', 'wrong_target': 'k_moved_once'}[bug]
    assert G[want] is False


def test_transport_shape_guards(M):
    mem = mem_rows(8, 49); up = upper_rows(9)
    with pytest.raises(M.Stop905): M.transport_upper(mem, up[:-1], 49, 30, 19, np_rephase(THETA, D), ft_cat, lambda a, b: np.arange(a, b))
    with pytest.raises(M.Stop905): M.transport_upper(mem_rows(8, 50), up, 49, 30, 19, np_rephase(THETA, D), ft_cat, lambda a, b: np.arange(a, b))


def test_rope_config_transformers4_and_5(M):
    assert M.rope_config(types.SimpleNamespace(rope_theta=1e6, rope_scaling=None)) == {'theta': 1e6, 'type': 'default', 'default': True}
    assert M.rope_config(types.SimpleNamespace(rope_parameters={'rope_type': 'default', 'rope_theta': 1e6}))['theta'] == 1e6
    assert not M.rope_config(types.SimpleNamespace(rope_theta=1e6, rope_scaling={'type': 'yarn', 'factor': 4.0}))['default']
    assert M.rope_config(types.SimpleNamespace())['theta'] is None


# ================================================================================================ stub engine: real write / read code
def stub_m3(M, tmp_path, rephase_bug=None):
    """a 903-engine stand-in: mount_sealed builds FT caches deterministically from the mounted objects (prefix rows from EMPTY,
    parent rows from the parent, E rows from the child), so write_upper / read_upper / read_mount run their real code."""
    m3 = types.SimpleNamespace(); m3.KVH, m3.HD, m3.DEV = KVH, D, 'cpu'
    def kv_digest(t): return sha(np.ascontiguousarray(t.numpy() if hasattr(t, 'numpy') else t).tobytes())
    m3.kv_digest = kv_digest; m3.full_kv_seal = lambda mem: tuple((kv_digest(k), kv_digest(v)) for k, v in mem)
    m3.jsha = M.jsha; m3.release = lambda: None; m3.guard = lambda *a, **k: None; m3.StopT896 = type('StopT896', (Exception,), {})
    def block(tag, rows):
        r = np.random.default_rng(int(sha(tag.encode())[:8], 16)); return r.standard_normal((L, 2, 1, KVH, rows, D)).astype(np.float32)
    def mount_sealed(ents):
        parts = [block('EMPTY', 30)]
        for e in ents: parts.append(block(e['tag'] + ('|ctx:' + ','.join(x['tag'] for x in ents[:ents.index(e)]) if e['kind'] == 'CHILD' else ''), 19))
        a = np.concatenate(parts, axis=-2); return [(FT(a[i, 0].copy()), FT(a[i, 1].copy())) for i in range(L)]
    m3.mount_sealed = mount_sealed
    reph = np_rephase(THETA, D)
    m3.rephase = (lambda k, o, n: reph(reph(k, o, n), o, n)) if rephase_bug == 'twice' else reph
    m3.torch = types.SimpleNamespace(cat=ft_cat, arange=lambda a, b, device=None: np.arange(a, b),
                                     save=lambda o, f: Path(f).write_bytes(pickle.dumps(o)), load=lambda f, map_location=None, weights_only=True: pickle.loads(Path(f).read_bytes()))
    m3.tok = types.SimpleNamespace(eos_token_id=0, decode=lambda ids, **k: 'UNKNOWN')
    m3.gen_with = lambda mem, q, k: (m3.tok.decode([7]), 0.01)
    m3.first_logits = lambda mem, q: types.SimpleNamespace(argmax=lambda: 7, __getitem__=None) if False else _Logits(7)
    m3.CART_INDEX = []; m3.ev = lambda *a, **k: None
    return m3


class _Logits:
    def __init__(self, top): self.top = top
    def argmax(self): return self.top
    def __getitem__(self, i): return 1.0 if int(i) == self.top else 0.0


def test_write_upper_real_code_independent_rows(M, tmp_path, monkeypatch):
    m3 = stub_m3(M, tmp_path); M.M3 = M.m3 = m3; M.ROOT = tmp_path; M.RUN_ID = 'T'
    par = {'tag': 'h1', 'kind': 'NATIVE', 'sha256': '1' * 64}; ch = {'tag': 'c1', 'kind': 'CHILD', 'sha256': '2' * 64, 'history': 'H1', 'tensor_seal': {'s': 1}}
    ent = M.write_upper('NS-A', 'R0', 'UP_H1', ch, par)
    assert ent['write_checks'] == {'parent_rows': True, 'source_rows': True, 'parent_rows_bitwise_unchanged': True, 'storage_independent_all': True,
                                   'layer_count_76': True, 'file_bytes_within_bound': True}
    obj = pickle.loads(Path(ent['file']).read_bytes()); src = m3.mount_sealed([par, ch])
    assert len(obj['upper']) == 76 and np.array_equal(obj['upper'][0][0].a, src[4][0].a[:, :, 49:68, :]) and obj['upper'][0][0].base is obj['upper'][0][0].a
    assert not os.access(ent['file'], os.W_OK) or os.geteuid() == 0                     # read-only on disk
    assert oct(os.stat(ent['file']).st_mode & 0o777) == oct(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    with pytest.raises(M.Stop905): M.write_upper('NS-A', 'R0', 'UP_H1', ch, par)              # append-only
    monkeypatch.setattr(FT, 'clone', lambda self: self)                                      # forgetting the copy keeps the parent storage
    with pytest.raises(M.Stop905) as e: M.write_upper('NS-A', 'R0', 'UP_HG', ch, par)
    assert 'storage_independent_all' in str(e.value)


def test_read_paths_real_code(M, tmp_path):
    m3 = stub_m3(M, tmp_path); M.M3 = M.m3 = m3; M.ROOT = tmp_path; M.RUN_ID = 'T'; M.X.ROPE_THETA = THETA
    par = {'tag': 'h1', 'kind': 'NATIVE', 'sha256': '1' * 64}; ch = {'tag': 'c1', 'kind': 'CHILD', 'sha256': '2' * 64, 'history': 'H1', 'tensor_seal': {'s': 1}}
    up = M.write_upper('NS-A', 'R0', 'UP_H1', ch, par); up['tensor_seal_sha256'] = M.jsha(up['tensor_seal']); up['key'] = 'UP_H1'
    rawA, infoA, dA = M.read_mount([ch], 'q', [7]); rawB, infoB, dB = M.read_upper(ch, up, 'q', [7])
    assert infoA['mount_tokens'] == infoB['mount_tokens'] == 49 and infoB['transport_checks']['ok'] and infoA['lower_seal_sha256'] == infoB['lower_seal_sha256']
    assert infoA['prefix_seal_sha256'] == infoB['prefix_seal_sha256'] and infoA['mount_seal_sha256'] != infoB['mount_seal_sha256']
    assert dB['decode_calls'] == [[7]] and dB['argmax'] == 7                                # generated ids captured by the decode tap
    m3b = stub_m3(M, tmp_path, rephase_bug='twice'); M.m3 = m3b
    with pytest.raises(m3b.StopT896) as e: M.read_upper(ch, up, 'q', [7])
    assert 'TRANSPORT_CHECK_FAILED' in str(e.value)
    up2 = dict(up, tensor_seal_sha256='9' * 64); M.m3 = m3
    with pytest.raises(m3.StopT896): M.read_upper(ch, up2, 'q', [7])                        # forged / changed upper seal


def test_read_path_isolation(M):
    iso = M.read_path_isolation(); assert iso['ok'], iso
    import inspect
    assert list(inspect.signature(M.read_upper).parameters) == ['child_ent', 'upper_ent', 'q', 'cand_ids']
    assert list(inspect.signature(M.read_mount).parameters) == ['ents', 'q', 'cand_ids']
    src = inspect.getsource(M.read_upper) + inspect.getsource(M.read_mount) + inspect.getsource(M.run_reads)
    for bad in ('expected_role', 'expected_answer', 'outcome_roles', 'r_name', 'g_name', 'MAN_PATH', 'evaluate', 'parent_sha256', 'h1_'):
        assert bad not in src, bad


# ================================================================================================ manifest + toy records -> evaluation
def synth(M):
    groups = {}; objects = {}; n = [0]
    def h():
        n[0] += 1; return '%064x' % n[0]
    for ns, pm in M.VARIANTS:
        g = {}
        for key, kind, hist, nn, pos0 in (('C1_H1', 'CHILD', 'H1', 19, 49), ('C1_HG', 'CHILD', 'HG', 19, 49), ('C1_H2', 'CHILD', 'H2', 19, 49), ('E_IND', 'NATIVE', None, 49, None),
                                          ('h1_H1', 'NATIVE', 'H1', 49, None), ('h1_HG', 'NATIVE', 'HG', 49, None), ('h1_H2', 'NATIVE', 'H2', 49, None)):
            g[key] = {'cid': '%s_%s_%s' % (ns, pm, key), 'member': 'cartridges/%s' % key, 'sha256': h(), 'kind': kind, 'history': hist, 'n': nn, 'body_tokens': 19,
                      'pos0': pos0, 'parents': None, 'ids_sha256': 'ids', 'tensor_seal': {'seal': key + ns + pm}}
        groups[ns, pm] = g
    tc = {'%s/%s/%s' % (ns, pm, k): sha(('ids' + ns + pm + k).encode()) for ns, pm in M.VARIANTS for k in ('TC_R', 'TC_G')}
    empty = {'member': 'cartridges/T903_EMPTY.pt', 'sha256': h(), 'kind': 'PREFIX', 'n': 30, 'tensor_seal': {'e': 1}}
    plan = M.plan_objects(groups, empty, tc)
    for key, p in plan.items():
        if key == 'EMPTY': continue
        if p['origin'] == 'ARCHIVE_903': objects[key] = {'key': p['key'], 'kind': p['kind'], 'n': p['n'], 'pos0': p['pos0'], 'sha256': p['sha256'], 'tensor_seal_sha256': p['tensor_seal_sha256']}
    for key, p in plan.items():
        if key != 'EMPTY' and p['origin'] == 'CREATED_905' and p['kind'] == 'CHILD':
            objects[key] = {'key': p['key'], 'kind': 'CHILD', 'n': 19, 'pos0': 49, 'sha256': h(), 'tensor_seal_sha256': h(), 'parent_sha256': objects[p['parent_key']]['sha256'], 'ids_sha256': p['ids_sha256']}
    for key, p in plan.items():
        if key != 'EMPTY' and p['origin'] == 'CREATED_905' and p['kind'] == 'UPPER':
            objects[key] = {'key': p['key'], 'kind': 'UPPER', 'n': 19, 'pos0': 49, 'sha256': h(), 'tensor_seal_sha256': h(), 'parent_sha256': objects[p['parent_key']]['sha256'],
                            'child_sha256': objects[p['child_key']]['sha256']}
    T3 = load(F903, 'm903'); first = {}; ans = {}
    for N in T3.NAMES.values():
        for w in [N[k] for k in ('o1', 'o2', 'o3')] + ['UNKNOWN']: first[w] = 1000 + int(sha(w.encode())[:6], 16); ans[w] = {'ids': [1], 'decode_roundtrip': True, 'fits_max_new': True}
    a904 = {'%s/%s/%s' % (ns, pm, o): {a: {'raw': 'UNKNOWN'} for a in ('STRAIGHT_A', 'STRAIGHT_B', 'CROSS_A', 'CROSS_B')} for ns, pm in M.VARIANTS for o in M.ORDERS}
    man = M.build_manifest(groups, plan, {'answers': ans, 'first_token': first, 'tc_ids_sha256': tc}, T3.NAMES, T3.PERMS, {'a': 1}, a904, M.M4)
    return man, objects


FACT = {'h1_H1': 'r', 'h1_HG': 'g', 'TC_R': 'r', 'TC_G': 'g'}


def toy_cells(M, man, objects, pol=None, drop=(), dup=(), edit=None):
    """records shaped like run_reads(); the toy reader 'knows' a fact according to the policy (which path exposes what)."""
    pol = dict({'A': False, 'B': True, 'trA': True, 'trB': True, 'src': True, 'label': False, 'pos_fail': set(), 'neg_name': set(), 'B_units': None, 'A_units': None, 'tr_break': {}}, **(pol or {}))
    out = []
    for k, c in man['cells'].items():
        U = man['units'][c['unit']]; inv = {v: r for r, v in U['outcome_roles'].items()}; keys = [s.split('/')[-1] for s in c['sources']]; path = c['path']; fact = None
        if path == 'MOUNT':
            fact = next((FACT[x] for x in keys if x in FACT), None)
            if 'TC_R' in keys or 'TC_G' in keys: fact = fact if pol['src'] and 'SOURCE' not in pol['tr_break'].get(c['unit'], ()) else None
        elif keys[0] in ('TC_R', 'TC_G'): fact = FACT[keys[0]] if pol['tr' + path] and path not in pol['tr_break'].get(c['unit'], ()) else None
        elif keys[0] in ('C1_H1', 'C1_HG'):
            on = pol[path] if pol[path + '_units'] is None else c['unit'] in pol[path + '_units']
            fact = {'C1_H1': 'r', 'C1_HG': 'g'}[keys[0]] if on else None
            if pol['label'] and c['label_history']: fact = {'H1': 'r', 'HG': 'g'}[c['label_history']]
        if c['arm'] in pol['pos_fail'] and c['unit'].startswith('NS-A/R0'): fact = None
        if c['arm'] in pol['neg_name']: fact = 'q'
        raw = inv[fact] if fact else 'UNKNOWN'
        if k in drop: continue
        O = lambda s: objects.get(s) or {'kind': man['objects'][s]['kind'], 'tensor_seal_sha256': 'f' * 64, 'sha256': 'f' * 64}
        tr = [{'key': s, 'kind': O(s)['kind'], 'tensor_seal_sha256': O(s)['tensor_seal_sha256'],
               'sha256': O(s)['sha256'] if c['arm'] not in M.SHAMS else sha(('work ' + k + s).encode())} for s in c['sources']]
        mt = {'mount_tokens': c['mount_tokens'], 'rope': copy.deepcopy(c['rope']), 'mount_seal_sha256': sha(json.dumps(c['sources'] + [path]).encode()),
              'prefix_seal_sha256': sha(b'prefix'), 'lower_seal_sha256': sha(json.dumps(c['sources'][:1]).encode())}
        if path == 'B': mt['transport_checks'] = {'ok': True}
        rec = {'cell_id': k, **{f: c[f] for f in ('unit', 'ns', 'perm', 'order', 'arm', 'path', 'slot', 'label_history', 'query_sha256')}, 'trace': tr, 'mount': mt,
               'raw': raw, 'diag': {'status': 'VERIFIED', 'logits': {str(U['diag_first_token_r']): 2.0 if fact == 'r' else 0.0, str(U['diag_first_token_g']): 1.0}}}
        if edit: edit(k, rec)
        out.append(rec)
        if k in dup: out.append(copy.deepcopy(rec))
    return out


def test_manifest_fixed_panel(M):
    man, objects = synth(M)
    assert man['n_cells'] == 192 == len(set(man['cells'])) and len(man['units']) == 8
    for u in man['units']:
        cs = [c for c in man['cells'].values() if c['unit'] == u]; assert len(cs) == 24 and len({c['query_sha256'] for c in cs}) == 1
    q = man['units']['NS-A/R0/FWD']['query']; assert 'Which outcome was observed for action' in q and 'UNKNOWN' in q and 'goal' not in q.lower()
    c = man['cells']['T905/NS-B/R1/REV/B_CROSS_A']; assert c['sources'] == ['NS-B/R1/C1_HG', 'NS-B/R1/UP_HG'] and c['expected_role'] == 'g' and c['mount_tokens'] == 49
    c = man['cells']['T905/NS-B/R1/REV/NEG_H2_B']; assert c['sources'] == ['NS-B/R1/C1_H2', 'NS-B/R1/UP_H2'] and c['expected_role'] == 'UNKNOWN'
    c = man['cells']['T905/NS-A/R1/FWD/TR_SOURCE_G']; assert c['sources'] == ['NS-A/R1/h1_H2', 'NS-A/R1/TC_G'] and c['mount_tokens'] == 68
    p = man['objects']['NS-A/R0/UP_H1']; assert p['computation'] == M.UPPER_COMPUTATION and p['child_key'] == 'NS-A/R0/C1_H1' and p['parent_key'] == 'NS-A/R0/h1_H1'
    assert man['objects']['NS-A/R0/TC_R']['record_roles'] == ['b', 'r'] and man['objects']['NS-A/R0/TC_R']['parent_key'] == 'NS-A/R0/h1_H2'
    json.dumps(man)


def test_b_only_gain_full_coverage(M):
    man, ob = synth(M); ev = M.evaluate_905(man, toy_cells(M, man, ob), ob, True, M.M4)
    assert ev['verdict'] == 'FULL_COVERAGE_B_GAIN' and not ev['integrity_problems']
    c = ev['counts']; assert (c['planned'], c['technical_complete'], c['all_controls_pass'], c['A_success'], c['B_success'], c['B_only'], c['A_only']) == (8, 8, 8, 0, 8, 8, 0)
    assert c['groups_B_only_both_orders'] == 4 and 'TEST905 VERDICT: FULL_COVERAGE_B_GAIN' in M.report_lines(ev)[0]


def test_both_paths_succeed_is_not_a_b_gain(M):
    man, ob = synth(M); ev = M.evaluate_905(man, toy_cells(M, man, ob, {'A': True}), ob, True, M.M4)
    assert ev['counts']['B_only'] == 0 and ev['counts']['both'] == 8 and ev['verdict'].startswith('NO_B_GAIN')


def test_reverse_loss_counted(M):
    man, ob = synth(M); ev = M.evaluate_905(man, toy_cells(M, man, ob, {'A': True, 'B': False}), ob, True, M.M4)
    # r2: verdict text renamed ('neither' only counts units passing all six direct controls)
    assert ev['counts']['A_only'] == 8 and ev['verdict'] == 'NO_B_GAIN[8/8 evaluable; 8 A-only; 0 both; 0 neither]'


def test_neither_with_and_without_transport(M):
    man, ob = synth(M)
    # r2: a failed direct-fact pair is now a failed control (unit leaves the denominator) instead of a NEITHER_* sub-label
    ev = M.evaluate_905(man, toy_cells(M, man, ob, {'B': False}), ob, True, M.M4); assert all(x['interpretation'] == 'NEITHER' for x in ev['units'])
    ev = M.evaluate_905(man, toy_cells(M, man, ob, {'B': False, 'trB': False}), ob, True, M.M4)
    assert all(x['interpretation'] == 'CONTROLS_FAILED[TR_B_R,TR_B_G]' for x in ev['units']) and ev['verdict'] == 'UNDECIDABLE_NO_EVALUABLE_UNIT'
    ev = M.evaluate_905(man, toy_cells(M, man, ob, {'B': False, 'src': False}), ob, True, M.M4)
    assert all(x['interpretation'] == 'CONTROLS_FAILED[TR_SOURCE_R,TR_SOURCE_G]' for x in ev['units']) and ev['verdict'] == 'UNDECIDABLE_NO_EVALUABLE_UNIT'


def test_partial_gain_and_groups_both_orders(M):
    man, ob = synth(M); units = {'NS-A/R0/FWD', 'NS-A/R0/REV', 'NS-B/R1/FWD'}
    ev = M.evaluate_905(man, toy_cells(M, man, ob, {'B_units': units}), ob, True, M.M4)
    assert ev['verdict'] == 'PARTIAL_B_GAIN[3/8 B-only; 8/8 evaluable; 1/4 groups both orders; 0 A-only]'


def test_label_following_reader_fails_sham(M):
    man, ob = synth(M); ev = M.evaluate_905(man, toy_cells(M, man, ob, {'B': False, 'label': True}), ob, True, M.M4)
    assert all(x['interpretation'].startswith('CONTROLS_FAILED[') and 'B_SHAM_A' in x['interpretation'] for x in ev['units'])
    assert ev['verdict'] == 'UNDECIDABLE_NO_EVALUABLE_UNIT'


def test_control_failures(M):
    man, ob = synth(M)
    ev = M.evaluate_905(man, toy_cells(M, man, ob, {'pos_fail': {'POS_FULL_REF_HG'}}), ob, True, M.M4)
    U = {x['unit']: x for x in ev['units']}; assert U['NS-A/R0/FWD']['interpretation'] == 'CONTROLS_FAILED[POS_FULL_REF_HG]' and ev['counts']['all_controls_pass'] == 6
    ev = M.evaluate_905(man, toy_cells(M, man, ob, {'neg_name': {'NEG_H2_B'}}), ob, True, M.M4)
    assert all(x['failed_controls'] == ['NEG_H2_B'] for x in ev['units']) and ev['verdict'] == 'UNDECIDABLE_NO_EVALUABLE_UNIT'   # B naming any b fact


def test_one_side_only_is_not_a_pair(M):
    man, ob = synth(M)
    def ed(k, r):
        if k.endswith('/B_STRAIGHT_B') or k.endswith('/B_CROSS_A'): r['raw'] = 'UNKNOWN'          # only the H1 side is read
    ev = M.evaluate_905(man, toy_cells(M, man, ob, edit=ed), ob, True, M.M4)
    x = ev['units'][0]; assert not x['B_pair_raw'] and x['one_side']['B_straight']   # r2: field renamed B_pair -> B_pair_raw and x['one_side']['B_cross'] and ev['counts']['B_only'] == 0


def test_h1_hg_swap_is_an_integrity_failure(M):
    man, ob = synth(M); k = 'T905/NS-A/R1/FWD/B_STRAIGHT_A'
    def ed(kk, r):
        if kk == k: r['trace'] = [dict(t, key=t['key'].replace('H1', 'HG')) for t in r['trace']]
    ev = M.evaluate_905(man, toy_cells(M, man, ob, edit=ed), ob, True, M.M4)
    assert ev['verdict'] == 'TECHNICAL_UNDECIDABLE' and any(p.endswith(':' + k) and 'trace[0].key' in p for p in ev['integrity_problems'])


@pytest.mark.parametrize('case,needle', [
    ('missing', 'MISSING_CELL'), ('dup', 'DUPLICATE_CELL'), ('wrong_len', 'mount_tokens_ne_geometry'), ('rope', 'rope_placement'),
    ('fake_mount_seal', 'MOUNT_SEAL_DIFFERS_FOR_SAME_TENSORS'), ('prefix', 'PREFIX_SEAL_DIFFERS'), ('lower', 'LOWER_SEAL_B_NE_A_FOR_SAME_CHILD'),
    ('no_transport_check', 'transport_checks'), ('sham_same_file', 'sham_file_is_the_source_file'), ('seal', 'trace[1].tensor_seal'),
    ('missing_object', 'MISSING_OBJECT'), ('object_parent', 'parent_sha256'), ('object_child', 'child_sha256')])
def test_integrity_cases(M, case, needle):
    man, ob = synth(M); ob = copy.deepcopy(ob); k = 'T905/NS-B/R0/REV/B_CROSS_B'; drop = set(); dup = set(); ed = None
    if case == 'missing': drop = {k}
    if case == 'dup': dup = {k}
    if case == 'wrong_len': ed = lambda kk, r: r['mount'].update(mount_tokens=68) if kk == k else None
    if case == 'rope': ed = lambda kk, r: r['mount']['rope'][1].update(source_pos0=30) if kk == k else None
    if case == 'fake_mount_seal': ed = lambda kk, r: r['mount'].update(mount_seal_sha256='a' * 64) if kk == k else None
    if case == 'prefix': ed = lambda kk, r: r['mount'].update(prefix_seal_sha256='b' * 64) if kk == k else None
    if case == 'lower': ed = lambda kk, r: r['mount'].update(lower_seal_sha256='c' * 64) if kk == k else None
    if case == 'no_transport_check': ed = lambda kk, r: r['mount'].pop('transport_checks') if kk == k else None
    if case == 'sham_same_file':
        k = 'T905/NS-B/R0/REV/B_SHAM_B'; ed = lambda kk, r: r['trace'][0].update(sha256=ob[r['trace'][0]['key']]['sha256']) if kk == k else None
    if case == 'seal': ed = lambda kk, r: r['trace'][1].update(tensor_seal_sha256='d' * 64) if kk == k else None
    if case == 'missing_object': ob.pop('NS-B/R0/UP_TC_G')
    if case == 'object_parent': ob['NS-B/R0/UP_H1']['parent_sha256'] = 'e' * 64
    if case == 'object_child': ob['NS-B/R0/UP_HG']['child_sha256'] = ob['NS-B/R0/C1_H1']['sha256']
    ev = M.evaluate_905(man, toy_cells(M, man, ob, drop=drop, dup=dup, edit=ed), ob, True, M.M4)
    assert ev['verdict'] == 'TECHNICAL_UNDECIDABLE' and any(needle in p for p in ev['integrity_problems']), (case, ev['integrity_problems'][:4])


def test_recompute_and_run_record(M, tmp_path, capsys):
    man, ob = synth(M); cells = toy_cells(M, man, ob); run = tmp_path / 'TEST905_X'; run.mkdir(); (run / 'sources').mkdir()
    (run / 'sources' / '904.py').write_bytes(F904.read_bytes()); b = json.dumps(man, indent=1, sort_keys=True, default=list).encode(); (run / 'TEST905_manifest.json').write_bytes(b)
    ev = M.evaluate_905(man, cells, ob, True, M.M4)
    R = {'run_id': 'X', 'status': 'COMPLETE', 'technical_verdict': 'PASS', 'manifest_sha256': M.sha_b(b), 'cells': cells, 'objects': ob, 'evaluation': ev,
         'generation_sealed_sha256': M.generation_seal(cells), 'gates': {}, 'technical_blockers': []}
    p = run / 'TEST905_results.json'; p.write_text(json.dumps(R)); assert M.recompute(str(p)) == 0
    R2 = copy.deepcopy(R); c = next(c for c in R2['cells'] if c['arm'] == 'NEG_E_IND'); c['raw'] = 'UNKNOWN.'          # same score, other evidence
    p.write_text(json.dumps(R2)); assert M.recompute(str(p)) == 1; out = capsys.readouterr().out
    assert 'GENERATION_SEAL_MISMATCH' in out and 'STORED_CELL_RESULT_DIFFERS:' + c['cell_id'] in out
    R3 = dict(R); R3.pop('generation_sealed_sha256'); p.write_text(json.dumps(R3)); assert M.recompute(str(p)) == 1
    assert 'GENERATION_SEALED_SHA256_MISSING' in capsys.readouterr().out


# ================================================================================================ delivery states / exit codes
def _final(M, tmp_path, cells_ok=True, drive=True, mode='auto', fail=None, monkeypatch=None):
    m = M; T3 = load(F903, 'm903'); out = tmp_path / 'out'; out.mkdir()
    cfg = m.config(['--out-root', str(out), '--drive', mode]); m.init_run(cfg); m.M3 = T3; m.bind_903(T3)
    m.R['status'] = 'COMPLETE'; m.R['technical_verdict'] = 'PASS'; m.R['top'].update(technical_verdict='PASS', verdict='NO_B_GAIN[x]')
    dd = tmp_path / 'MyDrive_TEST905'
    if drive: dd.mkdir(); m.DRIVE_DIR = str(dd); T3.DRIVE_DIR = str(dd)
    real = T3.drive_copy_verified
    def fake(src, dst):
        if fail == 'zip' and str(src).endswith('.zip'): return False, 'OSError: simulated ZIP'
        if fail == 'receipt' and str(src).endswith('_RECEIPT.json'): return False, 'OSError: simulated receipt'
        ok, err = real(src, dst)
        if fail == 'readback' and str(src).endswith('_RECEIPT.json') and 'DRIVE_RECEIPT_NOT_DELIVERED' not in Path(src).read_text():
            (Path(dst) / Path(src).name).write_text('{"tampered": 1}')
        return ok, err
    monkeypatch.setattr(T3, 'drive_copy_verified', fake)
    rc = m.finalize_artifacts(cfg); return m, rc, dd


@pytest.mark.parametrize('fail,status,code,drive_state', [(None, 'PASS', 0, 'EQUAL'), ('zip', 'DRIVE_ZIP_NOT_DELIVERED', 2, 'EQUAL'),
                                                          ('receipt', 'DRIVE_RECEIPT_NOT_DELIVERED', 2, 'ABSENT_OR_STALE'),
                                                          ('readback', 'DRIVE_RECEIPT_NOT_DELIVERED', 2, 'EQUAL')])
def test_delivery_states(M, tmp_path, monkeypatch, fail, status, code, drive_state):
    m, rc, dd = _final(M, tmp_path, fail=fail, monkeypatch=monkeypatch)
    assert rc['artifact_status'] == status and m.exit_code(rc) == code and m.X.RECEIPT_DRIVE_STATE == drive_state
    local = (m.ROOT.parent / ('TEST905_SONUC_%s_RECEIPT.json' % m.RUN_ID)).read_text(); assert json.loads(local)['artifact_status'] == status
    if drive_state == 'EQUAL': assert (dd / ('TEST905_SONUC_%s_RECEIPT.json' % m.RUN_ID)).read_text() == local     # final Drive receipt == local
    assert m.R['top']['verdict'] == 'NO_B_GAIN[x]' and m.OUT.is_file()                      # delivery never changes the verdict
    line = m.status_line(code, rc); assert ('DRIVE=PASS' in line) == (status == 'PASS') and ('EXIT=%d' % code) in line


def test_drive_required_not_mounted(M, tmp_path, monkeypatch):
    m, rc, dd = _final(M, tmp_path, drive=False, mode='required', monkeypatch=monkeypatch)
    assert rc['drive']['error'] == 'DRIVE_REQUIRED_BUT_NOT_MOUNTED' and m.exit_code(rc) == 2


# ================================================================================================ sources / entry / identity
def test_executed_source_identity(M, tmp_path, monkeypatch):
    ident, b = M.executed_source_identity(vars(M)); assert ident['method'] == '__file__' and b == F905.read_bytes() and ident['sha256'] == sha(F905.read_bytes())
    ns = {'__name__': 'exec_run'}; exec(compile(F905.read_bytes(), '<string>', 'exec'), ns)          # Colab exec(): no __file__
    monkeypatch.setenv('T905_SELF', str(F905))
    ident, b = ns['executed_source_identity'](ns); assert ident['method'] == 'code_object_match' and ident['sha256'] == sha(F905.read_bytes())
    other = tmp_path / '905.py'; other.write_bytes(F905.read_bytes().replace(b"MAX_NEW_905 = 25", b"MAX_NEW_905 = 26").replace(b'def cell_id(ns, pm, order, arm): return', b'def cell_id(ns, pm, order, arm):  return'))
    other.write_bytes(F905.read_bytes().replace(b"return 'T905/%s/%s/%s/%s' % (ns, pm, order, arm)", b"return 'T905/%s/%s/%s/%s/' % (ns, pm, order, arm)"))
    monkeypatch.setenv('T905_SELF', str(other)); monkeypatch.setattr(sys, 'argv', ['x'])
    ident, b = ns['executed_source_identity'](ns); assert ident['method'] == 'NOT_FOUND' and b is None                  # different code is refused


def test_import_and_entry_without_gpu(tmp_path):
    m = load()
    assert m.RUN_ID is None and m.R is None and not list(tmp_path.glob('TEST905_*'))
    rc = m.main(['--out-root', str(tmp_path), '--src-dir', str(F903.parent), '--drive', 'off', '--archive-dir', str(tmp_path / 'none')])
    assert rc == 1 and m.R['top']['first_failed_gate'] == 'GATE_RUNTIME_PINS' and m.R['status'] == 'TECHNICAL_ABORT'
    assert m.R['gates']['GATE_SOURCES_905']['status'] == 'PASS' and m.R['gates']['GATE_EXECUTED_SOURCE']['status'] == 'PASS'
    assert m.M4.R is None and m.M4.RUN_ID is None and m.M3.R is m.R                           # 903 / 904 imported, not started
    assert (m.ROOT / 'sources' / 'TEST905_executed_905.py').read_bytes() == F905.read_bytes()
    assert 'TEKNIK_HATA | EXIT=1' in m.LOG.read_text().splitlines()[-1]


def test_gate_order_static():
    s = F905.read_text(); g = s[s.index('def gpu_main'):s.index('def main(')]
    order = ['executed_source_identity()', 'M3.env_gate()', 'drive_gate(cfg)', 'archive_gate(cfg)', 'manifest_gate()', 'M3.model_gate()', 'write_all()', 'run_reads()']
    assert [g.index(x) for x in order] == sorted(g.index(x) for x in order)
    assert 'register_forward_hook' not in s


# ================================================================================================ archive gate on a synthetic 903 archive
T904_TESTS = Path(os.environ.get('T905_T904TESTS', SP.parent / 'k904/tests/test_904.py'))


def test_archive_gate_synthetic_903_and_pinned_904(M, tmp_path):
    """the real archive_gate: 903 chain through the pinned 904 functions + the H2 parent, read-only extraction, 904 results by pin."""
    T = load(T904_TESTS, 't904'); T3 = load(F903, 'm903')
    def mut(res, evb, members):
        ev = [json.loads(l) for l in evb.decode().splitlines()]
        for e in ev:
            if e.get('cid', '').endswith('_H2_h1'): e['ids_sha256'] = 'ids_E'               # the H2 parent is a->q, like E
        return res, ''.join(json.dumps(e) + '\n' for e in ev).encode(), members
    zp, rp, pins = T.build_archive(tmp_path, M.M4, mut); M.M4.RUN903.update(pins)
    a4 = tmp_path / 'a904'; a4.mkdir(); r4 = {'cells': [{'unit': 'NS-A/R0/FWD', 'arm': 'STRAIGHT_A', 'raw': 'UNKNOWN', 'cell_id': 'x', 'mount': {'mount_seal_sha256': 's'}}]}
    b4 = json.dumps(r4).encode(); (a4 / 'TEST904_results.json').write_bytes(b4); M.RUN904 = dict(M.RUN904, results_sha256=sha(b4))
    out = tmp_path / 'out'; out.mkdir(); cfg = M.config(['--out-root', str(out), '--zip', str(zp), '--receipt', str(rp), '--archive-904-dir', str(a4), '--drive', 'off'])
    M.init_run(cfg); M.M3 = T3; M.bind_903(T3); M.archive_gate(cfg)
    g = M.X.GROUPS['NS-B', 'R1']; assert set(g) == set(M.M4.NEEDED) | {'h1_H2'} and g['h1_H2']['sha256'] == g['C1_H2']['parents'][0]
    assert all(Path(v['file']).is_file() and not os.access(v['file'], os.W_OK) or os.geteuid() == 0 for v in g.values())
    assert M.R['gates']['GATE_ARCHIVE_905']['status'] == 'PASS' and M.X.A904['NS-A/R0/FWD']['STRAIGHT_A']['raw'] == 'UNKNOWN'
    (a4 / 'TEST904_results.json').write_bytes(b4 + b' ')
    (tmp_path / 'out2').mkdir(); cfg = dict(cfg, out_root=str(tmp_path / 'out2')); M.init_run(cfg); M.bind_903(T3)
    with pytest.raises(M.Stop905) as e: M.archive_gate(cfg)
    assert 'RESULTS_904_SHA256' in str(e.value)


# ================================================================================================ r2: controlled denominator / claim scope
def _check(M, man, ob, cells, tmp_path, verdict, counts=None, refs=None):
    """the verdict and denominators from evaluate_905 AND from --recompute on the same records."""
    ev = M.evaluate_905(man, cells, ob, True, M.M4, refs=refs)
    assert ev['verdict'] == verdict, ev['verdict']
    for k, v in (counts or {}).items(): assert ev['counts'][k] == v, (k, ev['counts'][k], v)
    run = tmp_path / ('TEST905_%d' % len(list(tmp_path.glob('TEST905_*')))); run.mkdir(); (run / 'sources').mkdir()
    (run / 'sources' / '904.py').write_bytes(F904.read_bytes()); b = json.dumps(man, indent=1, sort_keys=True, default=list).encode(); (run / 'TEST905_manifest.json').write_bytes(b)
    R = {'run_id': 'X', 'status': 'COMPLETE', 'technical_verdict': 'PASS', 'manifest_sha256': M.sha_b(b), 'cells': cells, 'objects': ob, 'evaluation': ev,
         'generation_sealed_sha256': M.generation_seal(cells), 'gates': {}, 'technical_blockers': [], 'upper_reference': refs or []}
    if refs is None: R['evaluation'] = M.evaluate_905(man, cells, ob, True, M.M4, refs=[])
    (run / 'TEST905_results.json').write_text(json.dumps(R)); assert M.recompute(str(run / 'TEST905_results.json')) == 0
    return ev


def test_r2_counterexample_source_and_b_transport_fail(M, tmp_path, capsys):
    man, ob = synth(M)
    ev = _check(M, man, ob, toy_cells(M, man, ob, {'src': False, 'trB': False}), tmp_path, 'UNDECIDABLE_NO_EVALUABLE_UNIT',
                {'all_controls_pass': 0, 'B_only': 0, 'raw_B_only': 8, 'raw_B_success': 8, 'excluded_by_direct_controls': 8})
    assert all(x['transport']['SOURCE'] is False and x['transport']['B'] is False for x in ev['units'])
    x = ev['units'][0]; assert x['failed_controls'] == ['TR_SOURCE_R', 'TR_SOURCE_G', 'TR_B_R', 'TR_B_G'] and x['direct_controls']['TR_SOURCE_R']['raw'] == 'UNKNOWN'
    out = '\n'.join(M.report_lines(ev)); assert 'failed controls: TR_SOURCE_R=' in out and 'raw (technically complete, controls ignored, NOT a scientific gain)' in out


def test_r2_counterexample_plus_b_false(M, tmp_path):
    man, ob = synth(M)
    _check(M, man, ob, toy_cells(M, man, ob, {'src': False, 'trB': False, 'B': False}), tmp_path, 'UNDECIDABLE_NO_EVALUABLE_UNIT',
           {'all_controls_pass': 0, 'neither': 0, 'raw_B_success': 0})


def test_r2_only_a_direct_control_broken(M, tmp_path):
    man, ob = synth(M)
    ev = _check(M, man, ob, toy_cells(M, man, ob, {'trA': False}), tmp_path, 'UNDECIDABLE_NO_EVALUABLE_UNIT', {'all_controls_pass': 0, 'raw_B_only': 8})
    assert all(x['interpretation'] == 'CONTROLS_FAILED[TR_A_R,TR_A_G]' for x in ev['units'])   # A cannot even carry a known fact


def test_r2_single_unit_eliminated(M, tmp_path):
    man, ob = synth(M)
    ev = _check(M, man, ob, toy_cells(M, man, ob, {'tr_break': {'NS-B/R0/REV': {'SOURCE'}}}), tmp_path,
                'PARTIAL_B_GAIN[7/8 B-only; 7/8 evaluable; 3/4 groups both orders; 0 A-only]',
                {'all_controls_pass': 7, 'B_only': 7, 'raw_B_only': 8, 'groups_B_only_both_orders': 3, 'groups_raw_B_only_both_orders': 4})
    assert {x['unit']: x['interpretation'] for x in ev['units']}['NS-B/R0/REV'] == 'CONTROLS_FAILED[TR_SOURCE_R,TR_SOURCE_G]'


def test_r2_full_positive_8_of_8(M, tmp_path):
    man, ob = synth(M)
    _check(M, man, ob, toy_cells(M, man, ob), tmp_path, 'FULL_COVERAGE_B_GAIN',
           {'all_controls_pass': 8, 'B_only': 8, 'A_success': 0, 'B_success': 8, 'groups_B_only_both_orders': 4})


def test_r2_valid_negative(M, tmp_path):
    man, ob = synth(M)
    _check(M, man, ob, toy_cells(M, man, ob, {'B': False}), tmp_path, 'NO_B_GAIN[8/8 evaluable; 0 A-only; 0 both; 8 neither]',
           {'all_controls_pass': 8, 'B_only': 0, 'neither': 8})


def _refs(M, fail=None, drop=None):
    out = []
    for ns, pm in M.VARIANTS:
        for h in ('H1', 'HG'):
            if drop == (ns, pm, h): continue
            out.append({'ns': ns, 'perm': pm, 'history': h, 'min_cos': 0.9985 if fail == (ns, pm, h) else 0.99991, 'equivalent_within_tol': fail != (ns, pm, h)})
    return out


def test_r2_reference_scope(M, tmp_path):
    man, ob = synth(M); cells = toy_cells(M, man, ob)
    ev = _check(M, man, ob, cells, tmp_path, 'FULL_COVERAGE_B_GAIN', refs=_refs(M))
    assert ev['reference_scope']['claim_scope'] == 'PARENT_OPEN_UPPER_MATCHES_NORMAL_CONDITIONED_PASS_WITHIN_TOL' and ev['reference_scope']['passed'] == 8
    ev = _check(M, man, ob, cells, tmp_path, 'FULL_COVERAGE_B_GAIN', refs=_refs(M, fail=('NS-A', 'R1', 'HG')))
    rs = ev['reference_scope']; assert rs['claim_scope'] == 'PARENT_OPEN_H3_INJECTION_UPPER_ONLY' and rs['passed'] == 7
    out = '\n'.join(M.report_lines(ev)); assert 'NS-A/R1   HG  min cos 0.998500 FAIL' in out and '7/8 pass -> claim scope PARENT_OPEN_H3_INJECTION_UPPER_ONLY' in out
    ev = _check(M, man, ob, cells, tmp_path, 'FULL_COVERAGE_B_GAIN', refs=_refs(M, drop=('NS-B', 'R0', 'H1')))
    assert not ev['reference_scope']['complete'] and ev['reference_scope']['claim_scope'] == 'PARENT_OPEN_H3_INJECTION_UPPER_ONLY'
    assert M.reference_scope([])['claim_scope'] == 'PARENT_OPEN_H3_INJECTION_UPPER_ONLY'
    assert M.TOL905['upper_reference_cos_min'] == 0.999 and 'claim_scope' in man['verdict_rules']
