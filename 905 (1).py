# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST905 — do E's upper-layer K/V, computed while the parent was still open, make the old b
#   outcome readable after the parent is removed?
#
# FILE: 905.py (root of ceceli33/titan-cognitive-core-v3, next to the unchanged 903.py and 904.py). Colab, Drive mounted, A100:
#   !python /content/titan-cognitive-core-v3/905.py
#   Offline re-scoring from the raw records (no model, no torch):  python 905.py --recompute TEST905_results.json
# Exit code (never set by the scientific verdict): 0 complete + technically valid + requested Drive delivery verified (or not
#   requested); 2 complete + valid but the requested Drive delivery failed (local results kept); 1 technical abort / invalid.
#
# THE ONE FACTOR. Same final event E = a->q, written after b->r (H1) or b->g (HG). Two clean read states that differ ONLY in E's
#   upper-layer (4..79) K/V rows:
#   A  CUT3_CLEAN       archived empty prefix + archived C1(H) through the 757-derived child mount (TEST904 path): lower rows
#                       L0-L3 rephased 49->30, upper rows L4-L79 recomputed from the archived H3 in the CLEAN context.
#   B  UPPER_PRESERVED  identical prefix, identical lower rows, identical E row count and target positions; the upper rows L4-L79
#                       of E are replaced by rows computed while the parent WAS open: PARENT_OPEN_H3_INJECTION_UPPER = the
#                       archived C1(H) appended by native_append_child_903 at its source position 49 on the mounted 903 parent
#                       (H3 injected at layer 3, layers 4-79 attend to the parent rows). Only E's 19 rows of layers 4-79 are
#                       copied to independent CPU storage, sealed and saved; parent rows are never stored. On reading, K is
#                       moved 49->30 exactly once with the 709 RoPE rephase (cached K carries RoPE: 757 rephases cached keys;
#                       transformers' attention rotates K before the cache update); V is never rotated.
#   Clean geometry: prefix [0,30); E [30,49); query from 49. Source geometry: prefix [0,30), parent [30,49), E [49,68).
# CLAIM SCOPE: B is the measured PARENT_OPEN_H3_INJECTION_UPPER intervention; 8 references (4 groups x H1/HG) compare it with the
#   normal conditioned pass (per-layer K/V cos >= 0.999, fixed); only if all 8 pass may it be described as matching that cache.
# DENOMINATOR: a controlled gain needs ALL controls: positives, negatives, shams AND the six direct-fact controls (SOURCE, B, A pairs).
# PANEL (fixed before any answer; 24 reads per unit, 8 units = 4 name/role groups x 2 answer orders, 192 greedy reads):
#   A straight/cross (4) | B straight/cross (4) + B sham (2, same tensors, other label / file names) | positives PARENT_ONLY,
#   FULL_REF (H1,HG) (4) | negatives E_IND, empty prefix, H2 via A, H2 via B (4) | direct-fact transport control: records b->r and
#   b->g written as E itself (same length, same source position 49, same previous event a->q without b): SOURCE read (parent
#   open), A transport, B transport (6). The b question, UNKNOWN option, parser and greedy settings are TEST904's.
# ENGINE: TEST903 code imported (not run) from 903.py blob f883d3df (runtime pins, A100 gate, blob-pinned 709/730/757/897/898/899,
#   MODEL block, child mount, seals, hooks, 898 gen -> 709 answer); TEST904 code imported (not run) from 904.py blob 2ffacbec
#   (archive resolution, query, parser, decode tap). Archives (903 ZIP, 904 results) are opened read-only by pinned SHA-256.
# NOT EXECUTED ON GPU BY ITS AUTHOR. CPU tests cover geometry, slicing, storage, RoPE transport (numpy reference), routing,
#   integrity, verdicts, delivery states and the archive chain; model behaviour is measured only on the A100.
# =====================================================================================================================
import os, sys, json, hashlib, re, time, shutil, subprocess, zipfile, types, traceback, importlib.util, stat, marshal
from pathlib import Path
from datetime import datetime, timezone
sys.dont_write_bytecode = True

TAG = 'TEST905'
MARKER = 'AKBASCORE SILICON HIPPOCAMPUS — TEST905 — parent-open upper E rows vs clean CUT3 rebuild'
SRC_REPO = 'ceceli33/titan-cognitive-core-v3'
SRC903 = {'file': '903.py', 'commit': 'ad228a29aacfc485377ed1d1a7aecae4d3201488', 'git_blob': 'f883d3dfa4c493bab4e4dc41b5743b30102ebd37',
          'sha256': '97fce064f5dafc18455d05ab015b9a476b063c801b7206401afbdfde1bc73ebc'}
SRC904 = {'file': '904.py', 'commit': 'ad228a29aacfc485377ed1d1a7aecae4d3201488', 'git_blob': '2ffacbec3b089759c89bf843d3725d617113d0ce',
          'sha256': 'c2d894d79f9d411bc8a8f7f2821fbcf3c67e41fd9f5b897d7f1e52a0cd20423b'}
RUN904 = {'run_id': '20261121T022512Z', 'results_name': 'TEST904_results.json',
          'results_sha256': '57b490ef259dc46286119a557f93dd01ddf988cd585ca208273b12cfc60f1d4b',
          'zip_name': 'TEST904_SONUC_20261121T022512Z.zip', 'zip_sha256': '7908842d40fb5f60da184f2ad350a64495795e0c634aec55c2713fa8c1894b68',
          'known': 'the Drive copy of the 904 receipt carries DRIVE_RECEIPT_PENDING; identity is taken from the ZIP / results pins only'}
DEFAULT_ARCHIVE_903 = '/content/drive/MyDrive/TEST903_20261120T192235Z'
DEFAULT_ARCHIVE_904 = '/content/drive/MyDrive/TEST904_20261121T022512Z'

GEOM = {'P': 30, 'parent_rows': [30, 49], 'source_E_rows': [49, 68], 'clean_E_rows': [30, 49], 'query_start_clean': 49, 'n_E': 19,
        'cut': 3, 'layers': 80, 'upper_layers': [4, 79], 'kv_heads': 8, 'head_dim': 128}
UPPER_COMPUTATION = ('PARENT_OPEN_H3_INJECTION_UPPER: archived C1 H3 injected at layer 3 by native_append_child_903 (757-derived) '
                     'at its source position 49 on mount_sealed([parent]); layers 4-79 of E computed attending to the open parent')
VARIANTS = (('NS-A', 'R0'), ('NS-A', 'R1'), ('NS-B', 'R0'), ('NS-B', 'R1')); ORDERS = ('FWD', 'REV')
NEEDED_EXTRA = {'h1_H2': ('_H2_h1', 'NATIVE', 'H2')}                 # 904's NEEDED + the H2 parent (a->q, no b)
# created objects (by write functions only): uppers of archived children, direct-fact transport children and their uppers
CREATED = {'UP_H1': ('UPPER', 'C1_H1', 'h1_H1'), 'UP_HG': ('UPPER', 'C1_HG', 'h1_HG'), 'UP_H2': ('UPPER', 'C1_H2', 'h1_H2'),
           'TC_R': ('CHILD', ('b', 'r'), 'h1_H2'), 'TC_G': ('CHILD', ('b', 'g'), 'h1_H2'),
           'UP_TC_R': ('UPPER', 'TC_R', 'h1_H2'), 'UP_TC_G': ('UPPER', 'TC_G', 'h1_H2')}
# arm -> (read path, slot, source keys in mount order, sham label, expected answer role)
ARMS = {
    'A_STRAIGHT_A': ('A', 'A', ('C1_H1',), None, 'r'), 'A_STRAIGHT_B': ('A', 'B', ('C1_HG',), None, 'g'),
    'A_CROSS_A': ('A', 'A', ('C1_HG',), None, 'g'), 'A_CROSS_B': ('A', 'B', ('C1_H1',), None, 'r'),
    'B_STRAIGHT_A': ('B', 'A', ('C1_H1', 'UP_H1'), None, 'r'), 'B_STRAIGHT_B': ('B', 'B', ('C1_HG', 'UP_HG'), None, 'g'),
    'B_CROSS_A': ('B', 'A', ('C1_HG', 'UP_HG'), None, 'g'), 'B_CROSS_B': ('B', 'B', ('C1_H1', 'UP_H1'), None, 'r'),
    'B_SHAM_A': ('B', 'A', ('C1_H1', 'UP_H1'), 'HG', 'r'), 'B_SHAM_B': ('B', 'B', ('C1_HG', 'UP_HG'), 'H1', 'g'),
    'POS_PARENT_ONLY_H1': ('MOUNT', '-', ('h1_H1',), None, 'r'), 'POS_PARENT_ONLY_HG': ('MOUNT', '-', ('h1_HG',), None, 'g'),
    'POS_FULL_REF_H1': ('MOUNT', '-', ('h1_H1', 'E_IND'), None, 'r'), 'POS_FULL_REF_HG': ('MOUNT', '-', ('h1_HG', 'E_IND'), None, 'g'),
    'NEG_E_IND': ('MOUNT', '-', ('E_IND',), None, 'UNKNOWN'), 'NEG_EMPTY_PREFIX': ('MOUNT', '-', (), None, 'UNKNOWN'),
    'NEG_H2_A': ('A', '-', ('C1_H2',), None, 'UNKNOWN'), 'NEG_H2_B': ('B', '-', ('C1_H2', 'UP_H2'), None, 'UNKNOWN'),
    'TR_SOURCE_R': ('MOUNT', '-', ('h1_H2', 'TC_R'), None, 'r'), 'TR_A_R': ('A', '-', ('TC_R',), None, 'r'), 'TR_B_R': ('B', '-', ('TC_R', 'UP_TC_R'), None, 'r'),
    'TR_SOURCE_G': ('MOUNT', '-', ('h1_H2', 'TC_G'), None, 'g'), 'TR_A_G': ('A', '-', ('TC_G',), None, 'g'), 'TR_B_G': ('B', '-', ('TC_G', 'UP_TC_G'), None, 'g')}
A_PAIR = ('A_STRAIGHT_A', 'A_STRAIGHT_B', 'A_CROSS_A', 'A_CROSS_B'); B_PAIR = ('B_STRAIGHT_A', 'B_STRAIGHT_B', 'B_CROSS_A', 'B_CROSS_B')
SHAMS = {'B_SHAM_A': 'B_STRAIGHT_A', 'B_SHAM_B': 'B_STRAIGHT_B'}
POS = ('POS_PARENT_ONLY_H1', 'POS_PARENT_ONLY_HG', 'POS_FULL_REF_H1', 'POS_FULL_REF_HG'); NEG = ('NEG_E_IND', 'NEG_EMPTY_PREFIX', 'NEG_H2_A', 'NEG_H2_B')
TR = {'SOURCE': ('TR_SOURCE_R', 'TR_SOURCE_G'), 'A': ('TR_A_R', 'TR_A_G'), 'B': ('TR_B_R', 'TR_B_G')}
MAX_NEW_905 = 25
TOL905 = {'upper_reference_cos_min': 0.999, 'rope_reference_cos_min': 0.9995,
          'upper_file_bytes_max_factor': 1.25,
          'note': 'fixed before data; the 903 parent-open reference_check is NOT evidence of clean transport and is not used as such'}
CRITICAL_905 = ('GATE_SOURCES_905', 'GATE_EXECUTED_SOURCE', 'GATE_DRIVE', 'GATE_ARCHIVE_905', 'GATE_ARCHIVE_TENSORS_905',
                'GATE_TOKENIZER_905', 'GATE_MANIFEST_905', 'GATE_ENGINE_905', 'GATE_WRITE_905', 'GATE_ROPE_905', 'GATE_WORK_COPIES_905', 'GATE_END_905')


def sha_b(b): return hashlib.sha256(b).hexdigest()
def sha_s(s): return sha_b(s.encode('utf-8'))
def blob_b(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
def canon(v): return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(',', ':'), default=list)
def jsha(v): return sha_s(canon(v))
HEX64 = re.compile(r'^[0-9a-f]{64}$')


class Stop905(Exception):
    """technical stop (never a scientific result); the message names the gate / object."""


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(4 << 20), b''): h.update(c)
    return h.hexdigest()


# ===================================================================================================== pure tensor-geometry layer
def slice_rows(t, start, n, kv_heads, head_dim):
    """E rows of one cached K or V: the sequence axis is -2 of (batch, kv_heads, seq, head_dim). Any other shape -> stop."""
    if len(t.shape) != 4: raise Stop905('SLICE_RANK %s' % (tuple(t.shape),))
    s = t[:, :, start:start + n, :]
    if tuple(s.shape) != (1, kv_heads, n, head_dim): raise Stop905('SLICE_SHAPE %s != %s' % (tuple(s.shape), (1, kv_heads, n, head_dim)))
    return s


def storage_independent(t):
    """a saved tensor must own exactly its own bytes (a view of the parent-open cache would drag that storage into the file)."""
    try: nb = t.untyped_storage().nbytes()
    except AttributeError: nb = t.storage().nbytes()
    return t.storage_offset() == 0 and nb == t.numel() * t.element_size() and t.is_contiguous()


def transport_upper(mem, upper, src0, dst0, n, rephase, cat, arange, cut=3):
    """B read state: replace rows [dst0, dst0+n) of layers cut+1.. with the preserved rows; K moved src0->dst0 exactly once with
    `rephase`, V copied unchanged. Lower layers and prefix rows are the clean mount's own objects (untouched)."""
    L = len(mem)
    if len(upper) != L - cut - 1: raise Stop905('UPPER_LAYER_COUNT %d != %d' % (len(upper), L - cut - 1))
    out = list(mem); old = arange(src0, src0 + n); new = arange(dst0, dst0 + n)
    for j, li in enumerate(range(cut + 1, L)):
        k, v = mem[li]; ku, vu = upper[j]
        if k.shape[-2] != dst0 + n or v.shape[-2] != dst0 + n: raise Stop905('CLEAN_ROWS_L%d %s' % (li, k.shape[-2]))
        if tuple(ku.shape) != tuple(k.shape[:2]) + (n, k.shape[-1]) or tuple(vu.shape) != tuple(ku.shape): raise Stop905('UPPER_SHAPE_L%d' % li)
        out[li] = (cat((k[:, :, :dst0, :], rephase(ku, old, new)), -2), cat((v[:, :, :dst0, :], vu), -2))
    return out


def rope_np(x, pos, theta, dim):
    """independent RoPE (float64 numpy): x[..., seq, dim] rotated to absolute positions pos (rotate-half convention)."""
    import numpy as np
    inv = 1.0 / (theta ** (np.arange(0, dim, 2, dtype=np.float64) / dim)); f = np.outer(np.asarray(pos, dtype=np.float64), inv)
    emb = np.concatenate([f, f], -1); c, s = np.cos(emb), np.sin(emb)
    def half(z): a, b = np.split(z, 2, -1); return np.concatenate([-b, a], -1)
    return x * c + half(x) * s


def rope_move_np(x, src, dst, theta, dim):
    """reference transport: undo the rotation at src (rotation by -src), apply the rotation at dst."""
    import numpy as np
    inv = 1.0 / (theta ** (np.arange(0, dim, 2, dtype=np.float64) / dim)); f = np.outer(np.asarray(src, dtype=np.float64), inv)
    emb = np.concatenate([f, f], -1); c, s = np.cos(emb), np.sin(emb)
    def half(z): a, b = np.split(z, 2, -1); return np.concatenate([-b, a], -1)
    return rope_np(x * c - half(x) * s, dst, theta, dim)


def rope_config(cfg):
    """rope theta and type from the model config (transformers 4: rope_theta / rope_scaling; 5: rope_parameters)."""
    rp = getattr(cfg, 'rope_parameters', None) or {}; rs = getattr(cfg, 'rope_scaling', None)
    theta = getattr(cfg, 'rope_theta', None) or (rp.get('rope_theta') if isinstance(rp, dict) else None)
    typ = (rp.get('rope_type') if isinstance(rp, dict) and rp else None) or ((rs or {}).get('rope_type') or (rs or {}).get('type') if isinstance(rs, dict) else None) or 'default'
    return {'theta': float(theta) if theta else None, 'type': typ, 'default': typ == 'default' and not (isinstance(rs, dict) and rs.get('factor'))}


def cos_np(a, b):
    import numpy as np
    a = np.asarray(a, dtype=np.float64).ravel(); b = np.asarray(b, dtype=np.float64).ravel(); return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-300))


def verify_transport(out, mem, upper, src0, dst0, n, to_np, theta, dim, cut=3, tol=None):
    """per-read proof of the B state: lower layers are the clean mount's own objects; prefix rows of every layer unchanged bit for
    bit; V rows == stored V bit for bit (never rotated); K rows == independent RoPE move src0->dst0 of the stored K (cos >= tol,
    i.e. rotated exactly once); row count == dst0 + n everywhere."""
    import numpy as np
    tol = tol or TOL905['rope_reference_cos_min']; L = len(mem); G = {}
    G['lower_untouched'] = all(out[i] is mem[i] for i in range(cut + 1))
    G['rows'] = all(out[i][0].shape[-2] == dst0 + n and out[i][1].shape[-2] == dst0 + n for i in range(L))
    pre = True; vok = True; kmin = 1.0
    for j, li in enumerate(range(cut + 1, L)):
        ko, vo = to_np(out[li][0]), to_np(out[li][1]); kc, vc = to_np(mem[li][0]), to_np(mem[li][1]); ku, vu = to_np(upper[j][0]), to_np(upper[j][1])
        pre = pre and np.array_equal(ko[:, :, :dst0, :], kc[:, :, :dst0, :]) and np.array_equal(vo[:, :, :dst0, :], vc[:, :, :dst0, :])
        vok = vok and np.array_equal(vo[:, :, dst0:dst0 + n, :], vu)
        ref = rope_move_np(ku.astype(np.float64), list(range(src0, src0 + n)), list(range(dst0, dst0 + n)), theta, dim)
        kmin = min(kmin, cos_np(ko[:, :, dst0:dst0 + n, :], ref))
    G.update(prefix_rows_bitwise=pre, v_unrotated_bitwise=vok, k_moved_once_min_cos=kmin, k_moved_once=kmin >= tol)
    G['ok'] = all(v for k, v in G.items() if isinstance(v, bool)); return G


# ===================================================================================================== design (pure)
def cell_id(ns, pm, order, arm): return 'T905/%s/%s/%s/%s' % (ns, pm, order, arm)


def expected_geometry(arm, src, P=30):
    """mount length and RoPE placement of every read path from the manifest geometry only."""
    path = ARMS[arm][0]; at = P; rope = []
    if path == 'B':
        c, u = src
        rope.append({'key': c['key'], 'part': 'L0-L3+H3', 'source_pos0': c['pos0'], 'target_pos0': at})
        rope.append({'key': u['key'], 'part': 'L4-L79 K (V unrotated)', 'source_pos0': u['pos0'], 'target_pos0': at}); at += c['n']
        return at, rope
    for t in src:
        k = t['n'] if t['kind'] == 'CHILD' else t['body_tokens']; s0 = t['pos0'] if t['kind'] == 'CHILD' else P
        rope.append({'key': t['key'], 'part': 'all', 'source_pos0': s0, 'target_pos0': at}); at += k
    return at, rope


def build_manifest(groups, objects_plan, tokinfo, NAMES, PERMS, archive, a904, M4):
    cells = {}; units = {}
    for ns, pm in VARIANTS:
        V = M4.names_of(ns, pm, NAMES, PERMS)
        for order in ORDERS:
            outs = M4.outcome_order(ns, order, NAMES); q = M4.query_904(V['b'], outs); u = '%s/%s/%s' % (ns, pm, order)
            fr, fg = tokinfo['first_token'][V['r']], tokinfo['first_token'][V['g']]
            units[u] = {'ns': ns, 'perm': pm, 'order': order, 'group': '%s/%s' % (ns, pm), 'b_name': V['b'], 'outcome_order': outs, 'query': q,
                        'query_sha256': sha_s(q), 'outcome_roles': {V[k]: k for k in ('g', 'q', 'r')}, 'r_name': V['r'], 'g_name': V['g'],
                        'diag_first_token_r': fr, 'diag_first_token_g': fg, 'diag_evaluable': fr != fg,
                        'answers_904': a904.get(u, {})}
            for arm, (path, slot, keys, lab, exp) in ARMS.items():
                src = [objects_plan['%s/%s/%s' % (ns, pm, k)] for k in keys]; n_, rope = expected_geometry(arm, src)
                cells[cell_id(ns, pm, order, arm)] = {
                    'unit': u, 'ns': ns, 'perm': pm, 'order': order, 'arm': arm, 'path': path, 'slot': slot, 'label_history': lab,
                    'sources': ['%s/%s/%s' % (ns, pm, k) for k in keys], 'mount_tokens': n_, 'rope': rope,
                    'query_sha256': sha_s(q), 'expected_role': exp, 'expected_answer': 'UNKNOWN' if exp == 'UNKNOWN' else V[exp]}
    return {'test': TAG, 'marker': MARKER, 'archive': archive, 'geometry': GEOM, 'upper_computation': UPPER_COMPUTATION, 'tolerances': TOL905,
            'objects': objects_plan, 'units': units, 'cells': cells, 'n_cells': len(cells), 'reads_planned': len(cells),
            'design': {'arms': {a: dict(zip(('path', 'slot', 'sources', 'sham_label', 'expected_role'), (p, s, list(k), l, e))) for a, (p, s, k, l, e) in ARMS.items()},
                       'query_template': M4.QUERY_TPL_904, 'normalization': M4.NORMALIZATION, 'max_new': MAX_NEW_905,
                       'answer_token_feasibility': tokinfo['answers'], 'order_axis': 'FWD/REV re-read the same 4 physical groups'},
            'verdict_rules': VERDICT_RULES_905}


def plan_objects(groups, empty, tokinfo_ids):
    """every object a read may mount: archived (903 ZIP) and created (this run), with geometry and lineage, before the model."""
    plan = {'EMPTY': dict(empty, key='EMPTY')}
    for (ns, pm), g in groups.items():
        for k, c in g.items():
            plan['%s/%s/%s' % (ns, pm, k)] = {'key': k, 'origin': 'ARCHIVE_903', 'cid': c['cid'], 'member': c['member'], 'sha256': c['sha256'],
                                              'tensor_seal_sha256': jsha(c['tensor_seal']) if c.get('tensor_seal') is not None else None,
                                              'kind': c['kind'], 'history': c['history'], 'n': int(c['n']), 'body_tokens': int(c['body_tokens']),
                                              'pos0': c['pos0'], 'parents': c.get('parents'), 'ids_sha256': c.get('ids_sha256')}
        for k, (kind, src, parent) in CREATED.items():
            base = {'key': k, 'origin': 'CREATED_905', 'kind': kind, 'parent_key': '%s/%s/%s' % (ns, pm, parent), 'pos0': 49, 'n': 19, 'body_tokens': 19,
                    'history': 'H2' if parent == 'h1_H2' else parent[3:]}
            if kind == 'UPPER':
                base.update(child_key='%s/%s/%s' % (ns, pm, src), layers=GEOM['upper_layers'], source_rows=GEOM['source_E_rows'],
                            computation=UPPER_COMPUTATION, k_carries_rope_at_source=True)
            else:
                base.update(record_roles=list(src), ids_sha256=tokinfo_ids['%s/%s/%s' % (ns, pm, k)], computation='903 forge_conditioned_903 on mount_sealed([parent])')
            plan['%s/%s/%s' % (ns, pm, k)] = base
    return plan


VERDICT_RULES_905 = {
    'cell_ok': '904 parse (exact name / UNKNOWN after the fixed normalization) answer role == expected_role; INVALID never repaired',
    'pair': 'arm pair success = straight (A slot r AND B slot g) AND cross (A slot g AND B slot r); one correct side is not a pair',
    'raw_vs_controlled': 'A_pair / B_pair are reported RAW for every technically complete unit; a scientific (controlled) gain is '
                         'counted only in units that pass ALL controls',
    'all_controls': 'positives 4/4 correct AND negatives 4/4 UNKNOWN AND both B shams give the raw answer of their straight source '
                    'AND all six direct-fact transport controls correct: SOURCE pair (TR_SOURCE_R, TR_SOURCE_G: the fact is readable '
                    'where it was written), B pair (TR_B_R, TR_B_G: the B path carries a known fact), A pair (TR_A_R, TR_A_G: the A path '
                    'carries a known fact, so an A failure on the history fact is not a failure to transport any fact)',
    'unit_interpretation': 'TECHNICAL_UNDECIDABLE (any record of the unit missing / duplicated / contradictory, or run invalid); '
                           'CONTROLS_FAILED[arms] (not in the denominator; the failed arms and raw answers are listed); among units '
                           'passing all controls: B_ONLY_GAIN (B pair, not A pair) = primary success; A_ONLY_GAIN (reverse); BOTH_PAIRS '
                           '(not B-specific); NEITHER (both clean representations fail to expose the history fact under this query)',
    'overall': 'TECHNICAL_UNDECIDABLE on any integrity problem or technical failure; e = units passing all controls; k = controlled '
               'B_ONLY_GAIN units; e = 0 -> UNDECIDABLE_NO_EVALUABLE_UNIT; e = 8 and k = 8 -> FULL_COVERAGE_B_GAIN; k >= 1 -> '
               'PARTIAL_B_GAIN[k/8 B-only; e/8 evaluable; groups both orders; A-only]; k = 0 -> NO_B_GAIN[e/8 evaluable; A-only; both; '
               'neither]. Denominators: planned 8, technical complete, all controls pass, raw and controlled A / B / B-only / A-only, '
               'groups (of 4) with a controlled B-only gain in both answer orders.',
    'claim_scope': 'B is the measured intervention PARENT_OPEN_H3_INJECTION_UPPER. Its comparison with the normal conditioned model '
                   'pass (8 references: 4 groups x H1/HG, per-layer K and V cosine >= 0.999, fixed before data) is reported; only if all '
                   '8 pass may the B carrier be described as matching the normal conditioned cache within that tolerance; otherwise '
                   '(or if references are missing) every claim is limited to the injection path actually used.',
    'scope': 'B_ONLY_GAIN means: under the same query and lower state, upper E rows computed with the parent open suffice to make '
             'the old fact readable; it does not show that a specific layer is necessary. NEITHER (with all direct controls passing) '
             'means these two clean representations did not expose the fact under this query; it does not show that the information '
             'was never written, that every carrier fails, or that a learned controller is required. The greedy answer decides; the '
             'first-token margin is a secondary diagnostic.'}


# ===================================================================================================== offline evaluation (pure)
REC_STR = ('cell_id', 'unit', 'ns', 'perm', 'order', 'arm', 'path', 'slot', 'query_sha256', 'raw')


def integrity_905(man, cells, objects):
    """(problem, id): every planned cell once; typed fields; trace bound to the object registry and the manifest plan (file SHA,
    tensor seal, kind); sham = other working-file SHA + same tensor seal; mount length and RoPE placement equal the manifest
    geometry; mount / prefix / lower seals required; identical mounted tensors -> identical mount seal; one prefix seal for all
    reads; lower seal of B = lower seal of A for the same child. Registry objects bound to the plan (lineage, geometry)."""
    prob = []; cnt = {}; recs = {}; byset = {}; prefixes = {}; lowers = {}
    P = man['objects']
    for key, o in (objects or {}).items():                               # registry -> plan
        p = P.get(key)
        if p is None: prob.append(('UNKNOWN_OBJECT', key)); continue
        bad = [f for f in ('kind', 'pos0', 'n') if o.get(f) != p.get(f)]
        if p['origin'] == 'ARCHIVE_903' and o.get('sha256') != p['sha256']: bad.append('archive_sha256')
        if p['origin'] == 'CREATED_905':
            par = objects.get(p['parent_key'], {});
            if o.get('parent_sha256') != par.get('sha256'): bad.append('parent_sha256')
            if p['kind'] == 'UPPER' and o.get('child_sha256') != (objects.get(p['child_key']) or {}).get('sha256'): bad.append('child_sha256')
            if p['kind'] == 'CHILD' and o.get('ids_sha256') != p.get('ids_sha256'): bad.append('ids_sha256')
        if not (isinstance(o.get('sha256'), str) and HEX64.match(o['sha256'])): bad.append('sha256')
        if not (isinstance(o.get('tensor_seal_sha256'), str) and HEX64.match(o['tensor_seal_sha256'])): bad.append('tensor_seal')
        if bad: prob.append(('OBJECT_CONTRADICTS_PLAN%s' % bad, key))
    for key, p in P.items():
        if key != 'EMPTY' and key not in (objects or {}): prob.append(('MISSING_OBJECT', key))
    for c in cells:
        k = c.get('cell_id') if isinstance(c, dict) else None; cnt[k] = cnt.get(k, 0) + 1; recs[k] = c
    for k, n in cnt.items():
        if k not in man['cells']: prob.append(('UNKNOWN_CELL', k)); continue
        if n != 1: prob.append(('DUPLICATE_CELL(x%d)' % n, k))
        m = man['cells'][k]; r = recs[k]; bad = ['type:' + f for f in REC_STR if not isinstance(r.get(f), str)]
        bad += [f for f in ('unit', 'ns', 'perm', 'order', 'arm', 'path', 'slot', 'label_history', 'query_sha256') if r.get(f) != m.get(f)]
        tr = r.get('trace')
        if not isinstance(tr, list) or len(tr) != len(m['sources']) or not all(isinstance(t, dict) for t in tr): bad.append('trace'); tr = None
        if tr is not None:
            for i, (t, key) in enumerate(zip(tr, m['sources'])):
                o = (objects or {}).get(key) or {}
                if t.get('key') != key: bad.append('trace[%d].key' % i)
                if t.get('tensor_seal_sha256') != o.get('tensor_seal_sha256'): bad.append('trace[%d].tensor_seal' % i)
                if t.get('kind') != P.get(key, {}).get('kind'): bad.append('trace[%d].kind' % i)
                if not (isinstance(t.get('sha256'), str) and HEX64.match(t['sha256'])): bad.append('trace[%d].sha256' % i)
                elif m['arm'] in SHAMS:
                    if t['sha256'] == o.get('sha256'): bad.append('trace[%d].sham_file_is_the_source_file' % i)
                elif t['sha256'] != o.get('sha256'): bad.append('trace[%d].file_sha_ne_object' % i)
        mt = r.get('mount')
        if not isinstance(mt, dict): bad.append('mount')
        else:
            if not isinstance(mt.get('mount_tokens'), int) or isinstance(mt.get('mount_tokens'), bool): bad.append('type:mount_tokens')
            elif mt['mount_tokens'] != m['mount_tokens']: bad.append('mount_tokens_ne_geometry')
            if mt.get('rope') != m['rope']: bad.append('rope_placement')
            for f in ('mount_seal_sha256', 'prefix_seal_sha256', 'lower_seal_sha256'):
                if not (isinstance(mt.get(f), str) and HEX64.match(mt[f])): bad.append(f)
            if m['path'] == 'B' and not (isinstance(mt.get('transport_checks'), dict) and mt['transport_checks'].get('ok') is True): bad.append('transport_checks')
            if not bad:
                byset.setdefault(tuple(m['sources']), {}).setdefault(mt['mount_seal_sha256'], []).append(k)
                prefixes.setdefault(mt['prefix_seal_sha256'], []).append(k)
                if m['path'] in ('A', 'B'): lowers.setdefault(m['sources'][0], {}).setdefault(mt['lower_seal_sha256'], []).append(k)
        if bad: prob.append(('CONTRADICTORY_CELL%s' % bad, k))
    def minority(d, code):
        if len(d) > 1:
            for _, ks in sorted(d.items(), key=lambda kv: (len(kv[1]), kv[0]))[:-1]:
                for kk in ks: prob.append((code, kk))
    for d in byset.values(): minority(d, 'MOUNT_SEAL_DIFFERS_FOR_SAME_TENSORS')
    minority(prefixes, 'PREFIX_SEAL_DIFFERS')
    for d in lowers.values(): minority(d, 'LOWER_SEAL_B_NE_A_FOR_SAME_CHILD')
    for k in man['cells']:
        if k not in cnt: prob.append(('MISSING_CELL', k))
    return sorted(set(prob), key=str)


DIRECT = TR['SOURCE'] + TR['B'] + TR['A']


def reference_scope(refs):
    """8 fixed references (4 groups x H1/HG): injection-path upper rows vs the normal conditioned pass, cos >= tolerance."""
    rows = [{'group': '%s/%s' % (r['ns'], r['perm']), 'history': r['history'], 'min_cos': r['min_cos'], 'pass': r['min_cos'] >= TOL905['upper_reference_cos_min']}
            for r in (refs or [])]
    expected = {('%s/%s' % v, h) for v in VARIANTS for h in ('H1', 'HG')}; got = {(r['group'], r['history']) for r in rows}
    complete = got == expected and len(rows) == len(expected); allp = complete and all(r['pass'] for r in rows)
    return {'rows': rows, 'complete': complete, 'passed': sum(r['pass'] for r in rows), 'total': len(rows), 'tolerance': TOL905['upper_reference_cos_min'],
            'claim_scope': ('PARENT_OPEN_UPPER_MATCHES_NORMAL_CONDITIONED_PASS_WITHIN_TOL' if allp else 'PARENT_OPEN_H3_INJECTION_UPPER_ONLY')}


def evaluate_905(man, cells, objects, technical_ok, M4, refs=None):
    probs = integrity_905(man, cells, objects); C = {c.get('cell_id'): c for c in cells if isinstance(c, dict)}
    bad_units = {man['cells'][k]['unit'] for _, k in probs if k in man['cells']}
    global_bad = [p for p in probs if p[1] not in man['cells']]
    units = []; scored = []
    for u, U in man['units'].items():
        res = {}
        for arm in ARMS:
            k = cell_id(U['ns'], U['perm'], U['order'], arm); r = C.get(k); m = man['cells'][k]
            p = M4.parse_904(r['raw'], U['outcome_order']) if r and isinstance(r.get('raw'), str) else {'status': 'MISSING', 'answer': None, 'norm': None}
            role = M4.answer_role(p, U['outcome_roles'])
            res[arm] = {'raw': r and r.get('raw'), 'parsed': p, 'role': role, 'expected_role': m['expected_role'], 'ok': role == m['expected_role']}
            scored.append(dict(cell_id=k, **res[arm]))
        tech = technical_ok and u not in bad_units and not global_bad
        pair = lambda a: all(res[x]['ok'] for x in a)
        pos = [a for a in POS if not res[a]['ok']]; neg = [a for a in NEG if res[a]['role'] != 'UNKNOWN']
        sham = [s_ for s_, src in SHAMS.items() if res[s_]['raw'] != res[src]['raw']]; direct = [a for a in DIRECT if not res[a]['ok']]
        A, B = pair(A_PAIR), pair(B_PAIR); trs = {k_: all(res[a]['ok'] for a in v) for k_, v in TR.items()}
        failed = pos + neg + sham + direct; controls = tech and not failed
        if not tech: it = 'TECHNICAL_UNDECIDABLE'
        elif failed: it = 'CONTROLS_FAILED[%s]' % ','.join(failed)
        elif B and not A: it = 'B_ONLY_GAIN'
        elif A and not B: it = 'A_ONLY_GAIN'
        elif A and B: it = 'BOTH_PAIRS'
        else: it = 'NEITHER'
        units.append({'unit': u, 'group': U['group'], 'technical_complete': tech, 'controls_pass': controls, 'failed_controls': failed,
                      'A_pair_raw': A, 'B_pair_raw': B, 'B_only_raw': B and not A, 'A_only_raw': A and not B, 'transport': trs,
                      'direct_controls': {a: {'raw': res[a]['raw'], 'role': res[a]['role'], 'expected': res[a]['expected_role'], 'ok': res[a]['ok']} for a in DIRECT},
                      'interpretation': it,
                      'one_side': {p_: res[a1]['ok'] != res[a2]['ok'] for p_, a1, a2 in (('A_straight', 'A_STRAIGHT_A', 'A_STRAIGHT_B'), ('A_cross', 'A_CROSS_A', 'A_CROSS_B'),
                                                                                       ('B_straight', 'B_STRAIGHT_A', 'B_STRAIGHT_B'), ('B_cross', 'B_CROSS_A', 'B_CROSS_B'))},
                      'raw': {a: res[a]['raw'] for a in ARMS}, 'roles': {a: res[a]['role'] for a in ARMS},
                      'a_vs_904': a_vs_904(U, res), 'diagnostic': diag_unit(U, C, man)})
    tc = [x for x in units if x['technical_complete']]; ev = [x for x in units if x['controls_pass']]
    it = lambda name: sum(x['interpretation'] == name for x in ev)
    cnt_ = {'planned': len(units), 'technical_complete': len(tc), 'all_controls_pass': len(ev),
            'raw_A_success': sum(x['A_pair_raw'] for x in tc), 'raw_B_success': sum(x['B_pair_raw'] for x in tc),
            'raw_B_only': sum(x['B_only_raw'] for x in tc), 'raw_A_only': sum(x['A_only_raw'] for x in tc),
            'A_success': sum(x['A_pair_raw'] for x in ev), 'B_success': sum(x['B_pair_raw'] for x in ev),
            'B_only': it('B_ONLY_GAIN'), 'A_only': it('A_ONLY_GAIN'), 'both': it('BOTH_PAIRS'), 'neither': it('NEITHER'),
            'excluded_by_direct_controls': sum(1 for x in tc if any(a in DIRECT for a in x['failed_controls']))}
    grp = {}; grp_raw = {}
    for x in units:
        grp.setdefault(x['group'], []).append(x['interpretation'] == 'B_ONLY_GAIN'); grp_raw.setdefault(x['group'], []).append(x['technical_complete'] and x['B_only_raw'])
    cnt_['groups_B_only_both_orders'] = sum(all(v) and len(v) == 2 for v in grp.values())
    cnt_['groups_raw_B_only_both_orders'] = sum(all(v) and len(v) == 2 for v in grp_raw.values()); cnt_['groups'] = len(grp)
    n = cnt_['planned']; k = cnt_['B_only']; e = cnt_['all_controls_pass']
    if probs or not technical_ok: v = 'TECHNICAL_UNDECIDABLE'
    elif e == 0: v = 'UNDECIDABLE_NO_EVALUABLE_UNIT'
    elif e == n and k == n: v = 'FULL_COVERAGE_B_GAIN'
    elif k >= 1: v = 'PARTIAL_B_GAIN[%d/%d B-only; %d/%d evaluable; %d/%d groups both orders; %d A-only]' % (k, n, e, n, cnt_['groups_B_only_both_orders'], cnt_['groups'], cnt_['A_only'])
    else: v = 'NO_B_GAIN[%d/%d evaluable; %d A-only; %d both; %d neither]' % (e, n, cnt_['A_only'], cnt_['both'], cnt_['neither'])
    return {'verdict': v, 'integrity_problems': ['%s:%s' % pk for pk in probs], 'units': units, 'scored_cells': scored, 'counts': cnt_,
            'reference_scope': reference_scope(refs) if refs is not None else None}


def a_vs_904(U, res):
    """the A path reproduces TEST904's clean child read: raw answers compared one by one with the archived 904 cells."""
    out = {}
    for a5, a4 in (('A_STRAIGHT_A', 'STRAIGHT_A'), ('A_STRAIGHT_B', 'STRAIGHT_B'), ('A_CROSS_A', 'CROSS_A'), ('A_CROSS_B', 'CROSS_B')):
        r4 = (U.get('answers_904') or {}).get(a4) or {}
        out[a5] = {'raw_905': res[a5]['raw'], 'raw_904': r4.get('raw'), 'equal': res[a5]['raw'] == r4.get('raw')}
    return out


def diag_unit(U, C, man):
    if not U['diag_evaluable']: return {'status': 'NOT_EVALUABLE_FIRST_TOKENS_COINCIDE'}
    s = {}
    for arm in A_PAIR + B_PAIR:
        r = C.get(cell_id(U['ns'], U['perm'], U['order'], arm)); d = (r or {}).get('diag') or {}; lg = d.get('logits') or {}
        fr, fg = str(U['diag_first_token_r']), str(U['diag_first_token_g'])
        s[arm] = lg[fr] - lg[fg] if d.get('status') == 'VERIFIED' and fr in lg and fg in lg else None
    if any(v is None for v in s.values()): return {'status': 'NOT_EVALUABLE_MEASUREMENT', 's': s}
    return {'status': 'EVALUATED', 's': s, 'A_d_straight': s['A_STRAIGHT_A'] - s['A_STRAIGHT_B'], 'A_d_cross': s['A_CROSS_B'] - s['A_CROSS_A'],
            'B_d_straight': s['B_STRAIGHT_A'] - s['B_STRAIGHT_B'], 'B_d_cross': s['B_CROSS_B'] - s['B_CROSS_A']}


def generation_seal(cells): return jsha([(c.get('cell_id'), c.get('raw')) for c in cells])


def verify_run_record(Rj, man_bytes, ev):
    out = []
    if Rj.get('status') == 'COMPLETE':
        for f in ('manifest_sha256', 'generation_sealed_sha256'):
            if not Rj.get(f): out.append(f.upper() + '_MISSING')
    if Rj.get('manifest_sha256') and Rj['manifest_sha256'] != sha_b(man_bytes): out.append('MANIFEST_SHA_MISMATCH')
    if Rj.get('generation_sealed_sha256') and Rj['generation_sealed_sha256'] != generation_seal(Rj.get('cells') or []): out.append('GENERATION_SEAL_MISMATCH')
    st = Rj.get('evaluation') or {}
    if st:
        a = {c['cell_id']: c for c in st.get('scored_cells', [])}; b = {c['cell_id']: c for c in ev['scored_cells']}
        out += ['STORED_CELL_RESULT_DIFFERS:' + k for k in sorted(set(a) | set(b)) if canon(a.get(k)) != canon(b.get(k))]
        ua = {x['unit']: x for x in st.get('units', [])}; ub = {x['unit']: x for x in ev['units']}
        out += ['STORED_UNIT_RESULT_DIFFERS:' + k for k in sorted(set(ua) | set(ub)) if canon(ua.get(k)) != canon(ub.get(k))]
        if st.get('verdict') != ev['verdict']: out.append('STORED_VERDICT_DIFFERS')
        if canon(st.get('counts')) != canon(ev['counts']): out.append('STORED_COUNTS_DIFFER')
    return out


def report_lines(ev):
    c = ev['counts']
    L = ['TEST905 VERDICT: %s' % ev['verdict'],
         'planned %d | technical complete %d | all controls pass %d (excluded by direct-fact controls %d)' % (c['planned'], c['technical_complete'], c['all_controls_pass'], c['excluded_by_direct_controls']),
         'controlled (all controls pass): A success %d | B success %d | B only %d | A only %d | both %d | neither %d | groups with B-only in both orders %d/%d' % (
             c['A_success'], c['B_success'], c['B_only'], c['A_only'], c['both'], c['neither'], c['groups_B_only_both_orders'], c['groups']),
         'raw (technically complete, controls ignored, NOT a scientific gain): A pair %d | B pair %d | B only %d | A only %d | groups raw B-only both orders %d/%d' % (
             c['raw_A_success'], c['raw_B_success'], c['raw_B_only'], c['raw_A_only'], c['groups_raw_B_only_both_orders'], c['groups'])]
    if ev['integrity_problems']: L.append('INTEGRITY FAIL: ' + '; '.join(ev['integrity_problems'][:20]))
    L.append('%-15s %-4s %-5s %-6s %-6s %-9s %-40s | raw A: straight A/B, cross A/B | raw B: straight A/B, cross A/B' % ('unit', 'tech', 'ctrl', 'A_raw', 'B_raw', 'transport', 'interpretation'))
    for x in ev['units']:
        r = x['raw']; t = ''.join('+' if x['transport'][k] else '-' for k in ('SOURCE', 'A', 'B'))
        L.append('%-15s %-4s %-5s %-6s %-6s S/A/B=%s %-40s | %s/%s, %s/%s | %s/%s, %s/%s' % (
            x['unit'], 'ok' if x['technical_complete'] else 'X', x['controls_pass'], x['A_pair_raw'], x['B_pair_raw'], t, x['interpretation'],
            r['A_STRAIGHT_A'], r['A_STRAIGHT_B'], r['A_CROSS_A'], r['A_CROSS_B'], r['B_STRAIGHT_A'], r['B_STRAIGHT_B'], r['B_CROSS_A'], r['B_CROSS_B']))
        bad = ['%s=%r(expected %s)' % (a, d['raw'], d['expected']) for a, d in x['direct_controls'].items() if not d['ok']]
        other = [a for a in x['failed_controls'] if a not in x['direct_controls']]
        if bad or other: L.append('    failed controls: %s' % '; '.join(bad + ['%s=%r' % (a, x['raw'][a]) for a in other]))
    diff = ['%s:%s(905=%r, 904=%r)' % (x['unit'], a, v['raw_905'], v['raw_904']) for x in ev['units'] for a, v in x['a_vs_904'].items() if not v['equal']]
    L.append('A vs archived TEST904 answers: ' + ('all equal' if not diff else '; '.join(diff)))
    rs = ev.get('reference_scope')
    if rs is not None:
        L.append('UPPER REFERENCE (injection-path upper vs normal conditioned pass, per-layer K/V cos >= %.3f): %d/%d pass%s -> claim scope %s' % (
            rs['tolerance'], rs['passed'], rs['total'], '' if rs['complete'] else ' (INCOMPLETE: 8 expected)', rs['claim_scope']))
        for r in rs['rows']: L.append('    %-9s %-3s min cos %.6f %s' % (r['group'], r['history'], r['min_cos'], 'PASS' if r['pass'] else 'FAIL'))
    return L


# ===================================================================================================== run infrastructure
X = types.SimpleNamespace(); M3 = M4 = None; RUN_ID = ROOT = LOG = OUT = EVENTS = None; R = None; DRIVE_DIR = None; T0 = time.perf_counter()


def config(argv):
    import argparse
    ap = argparse.ArgumentParser(add_help=False); colab = Path('/content').exists()
    d = {'out_root': '/content' if colab else '/tmp', 'src_dir': '', 'repo_dir': '/content/titan-cognitive-core-v3' if colab else '',
         'archive_dir': DEFAULT_ARCHIVE_903, 'zip': '', 'receipt': '', 'archive_904_dir': DEFAULT_ARCHIVE_904, 'results_904': '',
         'recompute': '', 'drive': 'required' if colab else 'auto'}
    for k, v in d.items(): ap.add_argument('--' + k.replace('_', '-'), default=os.environ.get('T905_' + k.upper(), v))
    a, _ = ap.parse_known_args(list(argv)); return {k: getattr(a, k) for k in d}


def fetch_source(cfg, work, pin):
    cands = [Path(cfg[k]) / pin['file'] for k in ('src_dir', 'repo_dir') if cfg.get(k)]
    for p in cands:
        if p.is_file() and blob_b(p.read_bytes()) == pin['git_blob']: b = p.read_bytes(); break
    else:
        rd = Path(cfg['repo_dir']) if cfg.get('repo_dir') and Path(cfg['repo_dir']).exists() else Path(work).parent / 'TEST905_repo_blobs'
        env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
        if not (rd / '.git').exists() and not (rd / 'HEAD').exists():
            subprocess.run(['git', 'clone', '-q', '--filter=blob:none', '--no-checkout', 'https://github.com/' + SRC_REPO, str(rd)], check=True, capture_output=True, timeout=900, env=env)
        b = subprocess.run(['git', '-C', str(rd), 'cat-file', 'blob', pin['git_blob']], check=True, capture_output=True, timeout=300, env=env).stdout
    if blob_b(b) != pin['git_blob'] or sha_b(b) != pin['sha256']: raise Stop905('SOURCE_IDENTITY ' + pin['file'])
    p = Path(work) / pin['file']; p.write_bytes(b); return p


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def _norm_code(co):
    consts = tuple(_norm_code(c) if isinstance(c, types.CodeType) else c for c in co.co_consts)
    return co.replace(co_filename='', co_consts=consts, co_firstlineno=1, co_linetable=b'', co_exceptiontable=co.co_exceptiontable)


def code_digest(funcs):
    return sha_b(b''.join(marshal.dumps(_norm_code(f.__code__)) for f in funcs))


def executed_source_identity(g=None):
    """bytes of the file that is actually executing: __file__, else argv[0] / T905_SELF / the repo copy, accepted only if the
    running functions' code objects equal those compiled from that file (exec() / %run safe)."""
    g = g or globals(); names = sorted(n for n, v in g.items() if isinstance(v, types.FunctionType) and v.__module__ == g.get('__name__'))
    running = code_digest([g[n] for n in names])
    cands = [g.get('__file__'), sys.argv[0] if sys.argv and sys.argv[0].endswith('905.py') else None, os.environ.get('T905_SELF'),
             '/content/titan-cognitive-core-v3/905.py']
    for c in cands:
        if not c or not Path(c).is_file(): continue
        b = Path(c).read_bytes(); ns = {'__name__': '_t905_check', '__file__': c}
        try: exec(compile(b, c, 'exec'), ns)
        except BaseException: continue
        if code_digest([ns[n] for n in names if n in ns]) == running and all(n in ns for n in names):
            return {'file': str(Path(c).resolve()), 'sha256': sha_b(b), 'git_blob': blob_b(b), 'bytes': len(b), 'code_digest': running,
                    'method': '__file__' if c == g.get('__file__') else 'code_object_match'}, b
    return {'file': None, 'code_digest': running, 'method': 'NOT_FOUND'}, None


def init_run(cfg):
    global RUN_ID, ROOT, LOG, OUT, EVENTS, R
    RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'); ROOT = Path(cfg['out_root']) / ('TEST905_' + RUN_ID); ROOT.mkdir(parents=True, exist_ok=False)
    LOG = ROOT / 'TEST905.log'; OUT = ROOT / 'TEST905_results.json'; EVENTS = ROOT / 'TEST905_events.jsonl'
    for f in (LOG, EVENTS): f.write_text('')
    R = {'test': TAG, 'marker': MARKER, 'run_id': RUN_ID, 'status': 'STARTED', 'executed_by_author': False, 'geometry': GEOM,
         'top': {'first_failed_gate': None, 'technical_verdict': None, 'verdict': None, 'counts': None},
         'sources_pinned': {'903': SRC903, '904': SRC904}, 'run_904': RUN904, 'gates': {}, 'checks': [], 'technical_blockers': [],
         'config': dict(cfg), 'cells': [], 'objects': {}}


def bind_903(m):
    m.RUN_ID = RUN_ID; m.ROOT = ROOT; m.LOG = LOG; m.OUT = OUT; m.EVENTS = EVENTS; m.CART_DIR = ROOT / 'work'; m.R = R; m.EVSEQ = [0]
    m.CRITICAL = tuple(m.CRITICAL) + CRITICAL_905


def log(*a): M3.log(*a)
def gate(*a, **k): M3.gate(*a, **k)


def drive_gate(cfg):
    global DRIVE_DIR
    mounted = Path('/content/drive/MyDrive').exists()
    if cfg.get('drive') == 'required' and not mounted:
        gate('GATE_DRIVE', 'FAIL', 'Drive delivery required but /content/drive/MyDrive is not mounted: run `from google.colab import drive; '
             'drive.mount("/content/drive")` in a cell, then start 905 again (or pass --drive off)')
    if mounted and cfg.get('drive') != 'off':
        DRIVE_DIR = '/content/drive/MyDrive/TEST905_' + RUN_ID; os.makedirs(DRIVE_DIR, exist_ok=True); M3.DRIVE_DIR = DRIVE_DIR; M3.save(force=True)
    gate('GATE_DRIVE', 'PASS', None, mode=cfg.get('drive'), mounted=mounted, dir=DRIVE_DIR)


def archive_gate(cfg):
    """903 ZIP (receipt -> ZIP -> SHA256SUMS -> members -> ledger -> results) via the pinned 904 functions + the H2 parent; 904
    results by pinned SHA (ZIP optional, checked when present). Needed members extracted read-only."""
    zp, rp, res, evp = M4.archive_paths(cfg)
    if zp is None or not Path(zp).is_file(): raise Stop905('ZIP_903_NOT_FOUND %s' % zp)
    if not Path(rp).is_file(): raise Stop905('RECEIPT_903_NOT_FOUND %s' % rp)
    try:
        A, sums, R3, events = M4.resolve_archive(zp, rp, M4.RUN903, res, evp); groups, empty = M4.map_cartridges(sums, R3, events)
    except M4.Stop904 as e: raise Stop905('ARCHIVE_903 ' + str(e))
    led = {(e.get('entry', e))['cid']: e.get('entry', e) for e in events if e.get('kind') == 'CARTRIDGE'}
    for (ns, pm), g in groups.items():
        tag = '%s_%s' % (ns.replace('-', ''), pm)
        for key, (suf, kind, hist) in NEEDED_EXTRA.items():
            x = led.get(tag + suf)
            if x is None: raise Stop905('LEDGER_MISSING ' + tag + suf)
            rel = x['file'][len(M4.RUN903['content_root']) + 1:]
            if sums.get(rel) != x['sha256']: raise Stop905('LEDGER_SHA_NE_SHA256SUMS ' + x['cid'])
            g[key] = {'key': key, 'cid': x['cid'], 'member': rel, 'sha256': x['sha256'], 'kind': kind, 'history': hist, 'generation': 1, 'ns': ns, 'perm': pm,
                      'n': x['n'], 'body_tokens': x['body_tokens'], 'pos0': None, 'ids_sha256': x['ids_sha256'], 'parents': None}
        if g['C1_H2'].get('parents') != [g['h1_H2']['sha256']]: raise Stop905('CHILD_PARENT_LINK ' + g['C1_H2']['cid'])
        if g['h1_H2']['ids_sha256'] != g['E_IND']['ids_sha256']: raise Stop905('H2_PARENT_NOT_A_TO_Q ' + g['h1_H2']['cid'])
    ro = ROOT / 'archive_ro'; root = M4.RUN903['zip_root'] + '/'
    with zipfile.ZipFile(zp) as z:
        for ent in [empty] + [v for g in groups.values() for v in g.values()]:
            dst = ro / ent['member']; dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists(): dst.write_bytes(z.read(root + ent['member'])); os.chmod(dst, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
            if sha_file(dst) != ent['sha256']: raise Stop905('EXTRACTED_SHA ' + ent['member'])
            ent['file'] = str(dst)
    p4 = Path(cfg['results_904']) if cfg.get('results_904') else Path(cfg['archive_904_dir']) / RUN904['results_name']
    if not p4.is_file(): raise Stop905('RESULTS_904_NOT_FOUND %s' % p4)
    b4 = p4.read_bytes()
    if sha_b(b4) != RUN904['results_sha256']: raise Stop905('RESULTS_904_SHA256 %s' % sha_b(b4))
    z4 = Path(cfg['archive_904_dir']) / RUN904['zip_name']; z4ok = None
    if z4.is_file():
        z4ok = sha_file(z4) == RUN904['zip_sha256']
        if not z4ok: raise Stop905('ZIP_904_SHA256')
        with zipfile.ZipFile(z4) as z:
            inner = [n for n in z.namelist() if n.endswith('/TEST904_results.json')]
            if len(inner) != 1 or sha_b(z.read(inner[0])) != RUN904['results_sha256']: raise Stop905('ZIP_904_RESULTS_MEMBER')
    R4 = json.loads(b4); a904 = {}
    for c in R4['cells']: a904.setdefault(c['unit'], {})[c['arm']] = {'raw': c['raw'], 'mount_seal_sha256': c['mount']['mount_seal_sha256'], 'cell_id': c['cell_id']}
    X.GROUPS, X.EMPTY, X.A3, X.A904 = groups, empty, A, a904
    R['archive'] = {'903': A, '904': {'results': str(p4), 'results_sha256': sha_b(b4), 'zip_checked': z4ok}}
    gate('GATE_ARCHIVE_905', 'PASS', None, archive_903=A, results_904_sha256=sha_b(b4), zip_904_checked=z4ok,
         objects={'%s/%s/%s' % (ns, pm, k): {kk: v[kk] for kk in ('cid', 'member', 'sha256', 'kind', 'history')} for (ns, pm), g in groups.items() for k, v in g.items()})


def archive_tensors_gate():
    m = M3; torch = m.torch; G = {}
    for ent in [X.EMPTY] + [v for g in X.GROUPS.values() for v in g.values()]:
        cp = torch.load(ent['file'], map_location='cpu', weights_only=True); ent['tensor_seal'] = m.seal_cp(cp); ent['book_id'] = cp['book_id']
        if ent['kind'] == 'PREFIX': ok = int(cp['n']) == int(cp['p']) == GEOM['P'] and cp['body_tokens'] == 0; X.CP_EMPTY = cp; ent['n'] = int(cp['n'])
        elif ent['kind'] == 'CHILD': ok = int(cp['p']) == 0 and int(cp['pos0']) == ent['pos0'] == 49 and int(cp['n']) == ent['n'] == 19
        else: ok = int(cp['p']) == 30 and int(cp['n']) == ent['n'] == 49 and int(cp['body_tokens']) == 19
        G[ent.get('cid', 'EMPTY')] = ok
        if not ok: gate('GATE_ARCHIVE_TENSORS_905', 'FAIL', 'geometry ' + ent.get('cid', 'EMPTY'), checks=G)
        del cp
    gate('GATE_ARCHIVE_TENSORS_905', 'PASS', None, checks=G)


def tokenizer_gate():
    """pinned tokenizer: archived token-id hashes reproduce every role record; ids of the two direct-fact records (b->r, b->g) have
    E's length; every public answer is producible within MAX_NEW; first answer tokens for the diagnostic."""
    m = M3; tk = m.transformers.AutoTokenizer.from_pretrained(m.MODEL_ID, revision=m.MODEL_REVISION, trust_remote_code=False)
    bad = []; X.TC_IDS = {}; tc_sha = {}
    for (ns, pm), g in X.GROUPS.items():
        V = M4.names_of(ns, pm, m.NAMES, m.PERMS)
        for key, ent in g.items():
            a, o = M4.E_FACT if key in ('C1_H1', 'C1_HG', 'C1_H2', 'E_IND') else M4.HIST_FACT[ent['history']]
            if sha_b(json.dumps(list(m.obs_ids(V[a], V[o], tk))).encode()) != ent['ids_sha256']: bad.append(ent['cid'])
            ent['record_names'] = [V[a], V[o]]
        for key in ('TC_R', 'TC_G'):
            roles = CREATED[key][1]; ids = list(m.obs_ids(V[roles[0]], V[roles[1]], tk)); X.TC_IDS[ns, pm, key] = ids
            tc_sha['%s/%s/%s' % (ns, pm, key)] = sha_b(json.dumps(ids).encode())
            if len(ids) != GEOM['n_E']: bad.append('%s/%s/%s:len%d' % (ns, pm, key, len(ids)))
    stop = tk.convert_tokens_to_ids('<|im_end|>'); answers = {}; first = {}
    for N in m.NAMES.values():
        for w in [N[k] for k in ('o1', 'o2', 'o3')] + ['UNKNOWN']:
            ids = list(tk(w, add_special_tokens=False).input_ids)
            answers[w] = {'ids': ids, 'decode_roundtrip': tk.decode(ids) == w, 'fits_max_new': len(ids) + 1 <= MAX_NEW_905}; first[w] = ids[0]
    ok = not bad and all(v['decode_roundtrip'] and v['fits_max_new'] for v in answers.values()) and stop is not None
    X.TOKINFO = {'answers': answers, 'first_token': first, 'stop_id': stop, 'tc_ids_sha256': tc_sha}
    gate('GATE_TOKENIZER_905', 'PASS' if ok else 'FAIL', None if ok else {'problems': bad}, answers=answers, tc_ids_sha256=tc_sha)
    del tk


def manifest_gate():
    plan = plan_objects(X.GROUPS, X.EMPTY, X.TOKINFO['tc_ids_sha256'])
    plan['EMPTY'] = {'key': 'EMPTY', 'origin': 'ARCHIVE_903', 'member': X.EMPTY['member'], 'sha256': X.EMPTY['sha256'], 'kind': 'PREFIX', 'n': X.EMPTY['n'],
                     'tensor_seal_sha256': jsha(X.EMPTY['tensor_seal']), 'pos0': 0}
    man = build_manifest(X.GROUPS, plan, X.TOKINFO, M3.NAMES, M3.PERMS, X.A3, X.A904, M4)
    ok = man['n_cells'] == len(set(man['cells'])) == 192 and all(len({c['query_sha256'] for c in man['cells'].values() if c['unit'] == u}) == 1 for u in man['units'])
    b = json.dumps(man, indent=1, sort_keys=True, default=list).encode(); p = ROOT / 'TEST905_manifest.json'; p.write_bytes(b)
    X.MAN_SHA = sha_b(b); X.MAN_PATH = p; X.PLAN = [(k, c['unit'], c['arm']) for k, c in man['cells'].items()]
    X.UNITQ = {u: {'query': U['query'], 'outs': U['outcome_order'], 'ns': U['ns'], 'perm': U['perm'], 'order': U['order']} for u, U in man['units'].items()}
    X.OBJPLAN = plan
    gate('GATE_MANIFEST_905', 'PASS' if ok else 'FAIL', None if ok else 'manifest shape', sha256=X.MAN_SHA, n_cells=man['n_cells'], written_before_model=True)
    del man


def engine_gate():
    m = M3; torch = m.torch; G = {}
    m.T_EXP = time.perf_counter(); m.ABORT = dict(m.ABORT_903); m.MAX_NEW = MAX_NEW_905; m.METRICS = {'forge_s': [], 'append_s': [], 'query_s': []}
    m.CART_INDEX = [v for g in X.GROUPS.values() for v in g.values()]; m.CP_EMPTY = X.CP_EMPTY
    G['P_is_30'] = m.P == 30 == GEOM['P']; G['prefix_sha256_equal_902_903'] = m.sha_bytes(m.PREFIX.encode()) == m.REF902['prefix_sha256']
    G['model_arch'] = (m.NL, m.H, m.QH, m.KVH, m.HD) == (80, 8192, 64, 8, 128) == (GEOM['layers'], 8192, 64, GEOM['kv_heads'], GEOM['head_dim'])
    G['rope'] = rope_config(m.model.config); G['rope_theta_found'] = G['rope']['theta'] is not None; G['rope_default_unscaled'] = G['rope']['default']
    with m.MountOff(): cpe, _ = m.forge_native([], 'T905_EMPTY_CHECK')
    G['fresh_empty_prefix_bitwise_equal_archive'] = (torch.equal(cpe['h'], X.CP_EMPTY['h']) and all(torch.equal(a, c) and torch.equal(b, d) for (a, b), (c, d) in zip(cpe['lower'], X.CP_EMPTY['lower'])))
    del cpe; m.release()
    sch = {'%s/%s/%s' % (ns, pm, k): m.child_schema(m.load_record(g[k]))['ok'] for (ns, pm), g in X.GROUPS.items() for k in ('C1_H1', 'C1_HG', 'C1_H2')}
    G['child_schema_all'] = all(sch.values())
    k = torch.randn((1, 8, 19, 128), device=m.DEV).to(m.DTYPE); p = torch.arange(49, 68, device=m.DEV)
    G['rephase_identity_bitwise_at_source_eq_target'] = torch.equal(m.rephase(k, p, p), k)
    G['hooks_clean'] = m.hooks_clean(m.hook_inventory()); G['read_path_isolated'] = read_path_isolation()['ok']
    fail = [kk for kk, v in G.items() if isinstance(v, bool) and v is not True]
    gate('GATE_ENGINE_905', 'PASS' if not fail else 'FAIL', None if not fail else 'failed: %s' % fail, checks=G, child_schema=sch)
    X.W0 = {'sentinel': m.sentinel(), 'integrity': m.integrity_digest(m.base_params, m.Q4MODS, m.BUFS)}; X.ROPE_THETA = G['rope']['theta']


# ---------------------------------------------------------------------------------------------------- WRITE (parent may be open)
def save_obj(obj, key, where, meta):
    m = M3; where.mkdir(parents=True, exist_ok=True); path = where / ('T905_%s.pt' % key.replace('/', '_')); tmp = Path(str(path) + '.tmp')
    if path.exists(): raise Stop905('APPEND_ONLY ' + str(path))
    m.torch.save(obj, tmp); tmp.replace(path); os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    ent = dict(meta, key=key.split('/')[-1], file=str(path), sha256=sha_file(path), bytes=path.stat().st_size)
    m.CART_INDEX.append(ent); m.ev('OBJECT', entry={k: v for k, v in ent.items() if k not in ('tensor_seal',)}); return ent


def write_transport_child(ns, pm, key, parent):
    """direct-fact control record (b->r or b->g) written as E itself after the a->q parent: 903 forge_conditioned_903 on the
    mounted parent (only the record's tokens processed; H3 + L0-L3 rows kept)."""
    m = M3; mem = m.mount_sealed([parent]); s0 = m.full_kv_seal(mem)
    cp, geo = m.forge_conditioned_903(mem, list(X.TC_IDS[ns, pm, key]), 'T905_%s_%s_%s' % (RUN_ID, ns, key))
    if m.full_kv_seal(mem) != s0: raise Stop905('PARENT_CHANGED_BY_FORGE %s/%s/%s' % (ns, pm, key))
    del mem; m.release()
    sch = m.child_schema(cp)
    if not sch['ok'] or cp['pos0'] != 49 or cp['n'] != 19: raise Stop905('TC_SCHEMA %s/%s/%s' % (ns, pm, key))
    ent = save_obj(cp, '%s/%s/%s' % (ns, pm, key), ROOT / 'objects' / ns / pm, {'kind': 'CHILD', 'n': cp['n'], 'body_tokens': cp['body_tokens'], 'pos0': cp['pos0'],
                   'history': 'H2', 'tensor_seal': m.seal_cp(cp), 'parent_sha256': parent['sha256'], 'ids_sha256': sha_b(json.dumps(list(X.TC_IDS[ns, pm, key])).encode()),
                   'geometry': geo, 'cid': 'T905_%s_%s_%s' % (ns, pm, key)})
    ent['tensor_seal_sha256'] = jsha(ent['tensor_seal']); del cp; return ent


def write_upper(ns, pm, key, child, parent):
    """PARENT_OPEN_H3_INJECTION_UPPER: mount_sealed([parent, child]) appends the child at its source position (49 == 49, identity
    rephase); rows [0,49) of all 80 layers must equal the parent-only mount bit for bit; E's rows [49,68) of layers 4-79 are
    copied into independent CPU storage, checked, sealed and saved. Parent rows never leave this function."""
    m = M3; torch = m.torch; G = {}
    par = m.mount_sealed([parent]); sp = m.full_kv_seal(par); n_par = int(par[0][0].shape[-2]); del par; m.release()
    mem = m.mount_sealed([parent, child]); n_src = int(mem[0][0].shape[-2])
    G['parent_rows'] = n_par == 49; G['source_rows'] = n_src == 68
    G['parent_rows_bitwise_unchanged'] = tuple((m.kv_digest(k[:, :, :n_par, :]), m.kv_digest(v[:, :, :n_par, :])) for k, v in mem) == sp
    s0, n = GEOM['source_E_rows'][0], GEOM['n_E']; up = []
    for li in range(GEOM['cut'] + 1, GEOM['layers']):
        k, v = mem[li]
        ks = slice_rows(k, s0, n, m.KVH, m.HD).detach().to('cpu').clone().contiguous(); vs = slice_rows(v, s0, n, m.KVH, m.HD).detach().to('cpu').clone().contiguous()
        up.append((ks, vs))
    del mem; m.release()
    G['storage_independent_all'] = all(storage_independent(a) and storage_independent(b) for a, b in up)
    G['layer_count_76'] = len(up) == 76
    obj = {'upper': tuple(up), 'layers': list(range(4, 80)), 'n': n, 'src_pos0': s0, 'k_carries_rope_at_src': True, 'v_rotated': False,
           'computation': UPPER_COMPUTATION, 'child_sha256': child['sha256'], 'parent_sha256': parent['sha256'], 'book_id': 'UP_%s_%s_%s' % (ns, pm, key)}
    seal = m.full_kv_seal(up); raw = sum(a.numel() * a.element_size() + b.numel() * b.element_size() for a, b in up)
    ent = save_obj(obj, '%s/%s/%s' % (ns, pm, key), ROOT / 'objects' / ns / pm, {'kind': 'UPPER', 'n': n, 'body_tokens': n, 'pos0': s0, 'history': child['history'],
                   'tensor_seal': list(seal), 'child_sha256': child['sha256'], 'parent_sha256': parent['sha256'], 'computation': UPPER_COMPUTATION,
                   'lower_block_sha256': jsha(child['tensor_seal']), 'upper_block_sha256': jsha(list(seal)), 'cid': 'T905_UP_%s_%s_%s' % (ns, pm, key)})
    G['file_bytes_within_bound'] = ent['bytes'] <= TOL905['upper_file_bytes_max_factor'] * raw + 65536
    ent['tensor_seal_sha256'] = jsha(list(seal)); ent['write_checks'] = G
    if not all(G.values()): raise Stop905('UPPER_WRITE %s/%s/%s %s' % (ns, pm, key, [k_ for k_, v in G.items() if not v]))
    del up; return ent


def upper_reference(ns, pm, h, parent, child, up_ent, ids):
    """measurement, not identity: E's upper rows from the normal conditioned model pass (E tokens through all 80 layers with the
    parent cache) vs the PARENT_OPEN_H3_INJECTION_UPPER rows; per-layer cosine / max abs / bitwise for K and V."""
    m = M3; torch = m.torch; mem = m.mount_sealed([parent]); oldn = int(mem[0][0].shape[-2]); work = [(k.clone(), v.clone()) for k, v in mem]; del mem
    cache = m.cache_build(work); del work; pos = torch.arange(oldn, oldn + len(ids), device=m.DEV)
    with torch.no_grad():
        out = m.model(input_ids=torch.tensor([list(ids)], device=m.DEV), past_key_values=cache, attention_mask=torch.ones((1, oldn + len(ids)), device=m.DEV, dtype=torch.long),
                      position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
    kv = m.pairs(out.past_key_values); del out
    upd = torch.load(up_ent['file'], map_location='cpu', weights_only=True)['upper']; rows = []
    for j, li in enumerate(range(4, 80)):
        k, v = kv[li]; kn = slice_rows(k, oldn, len(ids), m.KVH, m.HD).float().cpu(); vn = slice_rows(v, oldn, len(ids), m.KVH, m.HD).float().cpu()
        ku, vu = upd[j][0].float(), upd[j][1].float()
        rows.append({'layer': li, 'k_cos': float((kn.reshape(-1) @ ku.reshape(-1)) / (kn.norm() * ku.norm() + 1e-30)),
                     'v_cos': float((vn.reshape(-1) @ vu.reshape(-1)) / (vn.norm() * vu.norm() + 1e-30)),
                     'k_max_abs': float((kn - ku).abs().max()), 'v_max_abs': float((vn - vu).abs().max()), 'bitwise': bool(torch.equal(kn, ku) and torch.equal(vn, vu))})
    del kv, cache, upd; m.release()
    mn = min(min(r['k_cos'], r['v_cos']) for r in rows)
    return {'ns': ns, 'perm': pm, 'history': h, 'min_cos': mn, 'equivalent_within_tol': mn >= TOL905['upper_reference_cos_min'], 'layers': rows,
            'note': 'measured; the two computations are not assumed identical'}


def rope_reference(up_ent):
    """the 709 rephase used by the B read vs the independent float64 RoPE (rope_move_np) for the move 49->30 on the stored K;
    V must be left bit-identical; a second application must be clearly detectable."""
    import numpy as np
    m = M3; torch = m.torch; upd = torch.load(up_ent['file'], map_location='cpu', weights_only=True)['upper']; src = list(range(49, 68)); dst = list(range(30, 49))
    old = torch.arange(49, 68, device=m.DEV); new = torch.arange(30, 49, device=m.DEV); worst = 1.0; dbl = -1.0
    for ku, vu in upd:
        moved = m.rephase(ku.to(m.DEV), old, new).float().cpu().numpy()
        ref = rope_move_np(ku.float().numpy().astype(np.float64), src, dst, X.ROPE_THETA, m.HD)
        twice = m.rephase(m.rephase(ku.to(m.DEV), old, new), old, new).float().cpu().numpy()
        worst = min(worst, cos_np(moved, ref)); dbl = max(dbl, cos_np(twice, ref))
    ok = worst >= TOL905['rope_reference_cos_min']
    return {'key': up_ent['key'], 'min_cos_single_vs_reference': worst, 'max_cos_double_vs_reference_DIAGNOSTIC': dbl,
            'double_application_distinguishable_DIAGNOSTIC': dbl < TOL905['rope_reference_cos_min'], 'ok': ok}


def write_all():
    """every created object, before any read: uppers of the archived H1 / HG / H2 children, the two direct-fact children per
    group and their uppers; native-pass references (H1, HG per group); RoPE references for every upper."""
    objs = {}; refs = []; ropes = []
    for (ns, pm), g in X.GROUPS.items():
        for k, v in g.items(): objs['%s/%s/%s' % (ns, pm, k)] = {**{kk: v[kk] for kk in ('cid', 'file', 'sha256', 'kind', 'history', 'n', 'body_tokens', 'pos0')},
                                                                'key': k, 'tensor_seal': v['tensor_seal'], 'tensor_seal_sha256': jsha(v['tensor_seal'])}
        for h in ('H1', 'HG', 'H2'):
            objs['%s/%s/UP_%s' % (ns, pm, h)] = write_upper(ns, pm, 'UP_' + h, g['C1_' + h], g['h1_' + h])
        for f in ('R', 'G'):
            tc = write_transport_child(ns, pm, 'TC_' + f, g['h1_H2']); objs['%s/%s/TC_%s' % (ns, pm, f)] = tc
            objs['%s/%s/UP_TC_%s' % (ns, pm, f)] = write_upper(ns, pm, 'UP_TC_' + f, tc, g['h1_H2'])
        for h in ('H1', 'HG'):
            V = M4.names_of(ns, pm, M3.NAMES, M3.PERMS); ids = list(M3.obs_ids(V['a'], V['q'], M3.tok))
            refs.append(upper_reference(ns, pm, h, g['h1_' + h], g['C1_' + h], objs['%s/%s/UP_%s' % (ns, pm, h)], ids))
    for key, o in objs.items():
        if o['kind'] == 'UPPER': ropes.append(dict(rope_reference(o), object=key))
    X.OBJS = objs
    R['objects'] = {k: {kk: vv for kk, vv in v.items() if kk not in ('tensor_seal', 'geometry')} for k, v in objs.items()}
    R['upper_reference'] = refs; R['rope_reference'] = ropes
    gate('GATE_WRITE_905', 'PASS', None, created=sum(1 for k in objs if k.split('/')[-1] in CREATED),
         upper_reference_equivalent=sum(r['equivalent_within_tol'] for r in refs), upper_reference_total=len(refs))
    bad = [r['object'] for r in ropes if not r['ok']]
    gate('GATE_ROPE_905', 'PASS' if not bad else 'FAIL', None if not bad else 'RoPE transport reference failed: %s' % bad, results=ropes)


def work_copies():
    """read slots: byte copies (straight / cross, A and B) and sham copies for B (same tensors; child book_id and upper label of the
    other history, file names of the other history). Created and archive objects stay read-only."""
    m = M3; torch = m.torch; X.SLOT = {}; G = {}
    for (ns, pm), g in X.GROUPS.items():
        for arm, (path, slot, keys, lab, _) in ARMS.items():
            if slot == '-': continue
            ents = []
            for key in keys:
                src = X.OBJS['%s/%s/%s' % (ns, pm, key)]; d = ROOT / 'work' / ns / pm / ('slot' + slot); d.mkdir(parents=True, exist_ok=True)
                shown = lab or src['history']; dst = d / ('T905_%s_%s_%s_%s_%s.pt' % (ns.replace('-', ''), pm, arm, key.split('_')[0], shown))
                if lab is None:
                    shutil.copyfile(src['file'], dst); e = dict(src, file=str(dst)); G[dst.name] = sha_file(dst) == src['sha256']
                else:
                    obj = torch.load(src['file'], map_location='cpu', weights_only=True); other = X.OBJS['%s/%s/%s' % (ns, pm, key.replace(src['history'], lab))]
                    if src['kind'] == 'CHILD': obj['book_id'] = M3.load_record(other)['book_id']; seal = jsha(m.seal_cp(obj))
                    else: obj['book_id'] = 'UP_%s_%s_UP_%s' % (ns, pm, lab); seal = jsha(list(m.full_kv_seal(obj['upper'])))
                    torch.save(obj, dst); e = dict(src, file=str(dst), sha256=sha_file(dst), shown_history=lab)
                    G[dst.name] = seal == src['tensor_seal_sha256'] and e['sha256'] != src['sha256']; del obj
                os.chmod(dst, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH); ents.append(e); m.CART_INDEX.append(e)
            X.SLOT[ns, pm, arm] = ents
    ok = all(G.values()); gate('GATE_WORK_COPIES_905', 'PASS' if ok else 'FAIL', None if ok else [k for k, v in G.items() if not v], checks=G)


# ---------------------------------------------------------------------------------------------------- READ (parent never present)
def _gen_and_diag(mem, q, cand_ids):
    real = m3.tok; tap = M4.DecodeTap(real); m3.tok = tap
    try: raw, dt = m3.gen_with(mem, q, MAX_NEW_905)
    finally: m3.tok = real
    m3.guard('query', dt); lg = m3.first_logits(mem, q); top = int(lg.argmax()); logits = {str(i): float(lg[i]) for i in cand_ids}; del lg
    return raw, dt, {'argmax': top, 'logits': logits, 'decode_calls': tap.calls}


def _seals(mem):
    P = 30; return (m3.jsha(m3.full_kv_seal(mem)), m3.jsha([(m3.kv_digest(k[:, :, :P, :]), m3.kv_digest(v[:, :, :P, :])) for k, v in mem]),
                    m3.jsha(m3.full_kv_seal(mem[:4])))


def read_mount(ents, q, cand_ids):
    """A / natives / source: fresh mount_sealed(ents) (archived prefix + sealed cartridges) -> locked answer()."""
    t_ = time.perf_counter(); mem = m3.mount_sealed(ents); s0 = m3.full_kv_seal(mem); n = int(mem[0][0].shape[-2])
    raw, dt, dg = _gen_and_diag(mem, q, cand_ids)
    if m3.full_kv_seal(mem) != s0: raise m3.StopT896('MOUNT_CHANGED_BY_READ')
    ms, ps, ls = _seals(mem); del mem; m3.release()
    return raw, {'mount_tokens': n, 'mount_seal_sha256': ms, 'prefix_seal_sha256': ps, 'lower_seal_sha256': ls, 'query_s': round(dt, 3),
                 'read_s': round(time.perf_counter() - t_, 3)}, dg


def read_upper(child_ent, upper_ent, q, cand_ids):
    """B: fresh clean child mount (identical to A) -> E's upper rows of layers 4-79 replaced by the sealed preserved rows (K moved
    49->30 once, V unchanged) -> locked answer(). Inputs: the sealed child, the sealed upper file, the archived prefix, the query."""
    t_ = time.perf_counter(); torch = m3.torch; mem = m3.mount_sealed([child_ent]); lower_before = m3.full_kv_seal(mem[:4])
    obj = torch.load(upper_ent['file'], map_location='cpu', weights_only=True)
    if sha_file(upper_ent['file']) != upper_ent['sha256'] or m3.jsha(list(m3.full_kv_seal(obj['upper']))) != upper_ent['tensor_seal_sha256']:
        raise m3.StopT896('UPPER_FILE_OR_SEAL_CHANGED ' + upper_ent['key'])
    up = [(k.to(m3.DEV), v.to(m3.DEV)) for k, v in obj['upper']]; src0 = int(obj['src_pos0']); n = int(obj['n']); del obj
    dst0 = int(mem[0][0].shape[-2]) - n
    if dst0 != 30 or src0 != 49 or n != 19: raise m3.StopT896('B_GEOMETRY src0=%d dst0=%d n=%d' % (src0, dst0, n))
    clean = mem
    mem = transport_upper(clean, up, src0, dst0, n, m3.rephase, torch.cat, lambda a, b: torch.arange(a, b, device=m3.DEV), cut=3)
    tc = verify_transport(mem, clean, up, src0, dst0, n, lambda t: t.float().cpu().numpy(), X.ROPE_THETA, m3.HD, cut=3)
    if not tc['ok'] or m3.full_kv_seal(mem[:4]) != lower_before: raise m3.StopT896('TRANSPORT_CHECK_FAILED %s %s' % (upper_ent['key'], tc))
    del clean
    s0 = m3.full_kv_seal(mem); nn = int(mem[0][0].shape[-2])
    raw, dt, dg = _gen_and_diag(mem, q, cand_ids)
    if m3.full_kv_seal(mem) != s0: raise m3.StopT896('MOUNT_CHANGED_BY_READ')
    ms, ps, ls = _seals(mem); del mem, up; m3.release()
    return raw, {'mount_tokens': nn, 'mount_seal_sha256': ms, 'prefix_seal_sha256': ps, 'lower_seal_sha256': ls, 'query_s': round(dt, 3),
                 'read_s': round(time.perf_counter() - t_, 3), 'transport_checks': tc}, dg


m3 = None


def read_path_isolation():
    import symtable, inspect, textwrap
    allowed = {'m3', 'M4', 'X', 'MAX_NEW_905', 'time', 'int', 'round', 'float', 'str', 'list', 'sha_file', 'transport_upper', 'verify_transport',
               '_gen_and_diag', '_seals', 'len'}
    out = {}
    for f in (read_mount, read_upper, _gen_and_diag, _seals):
        t = symtable.symtable(textwrap.dedent(inspect.getsource(f)), f.__name__, 'exec').get_children()[0]
        g = sorted({x.get_name() for x in t.get_symbols() if x.is_global()}); out[f.__name__] = {'globals': g, 'not_allowed': sorted(set(g) - allowed)}
    out['ok'] = not any(v['not_allowed'] for v in out.values() if isinstance(v, dict)); return out


def run_reads():
    nread = 0
    for k, u, arm in X.PLAN:
        U = X.UNITQ[u]; ns, pm = U['ns'], U['perm']; path, slot, keys, lab, _ = ARMS[arm]
        ents = X.SLOT[ns, pm, arm] if slot != '-' else [X.OBJS['%s/%s/%s' % (ns, pm, kk)] for kk in keys]
        cand = sorted({X.TOKINFO['first_token'][w] for w in U['outs'] + ['UNKNOWN']})
        if path == 'B': raw, info, dg = read_upper(ents[0], ents[1], U['query'], cand)
        else: raw, info, dg = read_mount(ents, U['query'], cand)
        nread += 1
        _, info['rope'] = expected_geometry(arm, [X.OBJPLAN['%s/%s/%s' % (ns, pm, kk)] for kk in keys])     # as executed (fixed geometry)
        calls = dg.pop('decode_calls'); dg['generated_ids'] = calls[0] if len(calls) == 1 else None
        dg['status'], dg['generated_first_id'] = M4.diag_validity(dg['argmax'], calls, {m3.tok.eos_token_id, X.TOKINFO['stop_id']})
        rec = {'cell_id': k, 'unit': u, 'ns': ns, 'perm': pm, 'order': U['order'], 'arm': arm, 'path': path, 'slot': slot, 'label_history': lab,
               'trace': [{'key': '%s/%s/%s' % (ns, pm, kk), 'sha256': e['sha256'], 'tensor_seal_sha256': e['tensor_seal_sha256'], 'kind': e['kind'],
                          'file': e['file'], 'shown_history': e.get('shown_history')} for kk, e in zip(keys, ents)],
               'query_sha256': sha_s(U['query']), 'mount': info, 'raw': raw, 'diag': dg, 't_s': round(time.perf_counter() - T0, 1)}
        R['cells'].append(rec); M3.ev('READOUT', cell_id=k, raw=raw, mount=info['mount_seal_sha256'])
        log('READ %-42s %-20s -> %r' % (k, arm, raw[:60])); M3.save(False)
    X.NREAD = nread; R['generation_sealed_sha256'] = generation_seal(R['cells']); M3.ev('GENERATION_SEALED', sha256=R['generation_sealed_sha256'])


def end_gate():
    mm = M3
    G = {'sentinel_equal': mm.sentinel() == X.W0['sentinel'], 'integrity_equal': mm.integrity_digest(mm.base_params, mm.Q4MODS, mm.BUFS)['sha256'] == X.W0['integrity']['sha256'],
         'hooks_clean': mm.hooks_clean(mm.hook_inventory()), 'files_unchanged': all(sha_file(e['file']) == e['sha256'] for e in mm.CART_INDEX),
         'reads_192': X.NREAD == 192}
    ok = all(G.values()); gate('GATE_END_905', 'PASS' if ok else 'FAIL', None if ok else [k for k, v in G.items() if not v], **G)


def write_verdict():
    b = X.MAN_PATH.read_bytes()
    if sha_b(b) != X.MAN_SHA: raise Stop905('MANIFEST_CHANGED')
    man = json.loads(b); gates_ok = all(g['status'] != 'FAIL' for g in R['gates'].values()) and not R['technical_blockers']; R['manifest_sha256'] = X.MAN_SHA
    ev = evaluate_905(man, R['cells'], R['objects'], gates_ok, M4, refs=R.get('upper_reference') or []); probs = verify_run_record(dict(R, status='COMPLETE', evaluation=None), b, ev)
    tv = 'PASS' if gates_ok and not ev['integrity_problems'] and not probs else 'TECHNICAL_UNDECIDABLE'
    if tv != 'PASS': ev['verdict'] = 'TECHNICAL_UNDECIDABLE'
    R.update(evaluation=ev, technical_verdict=tv, run_record_problems=probs)
    R['top'].update(technical_verdict=tv, verdict=ev['verdict'], counts=ev['counts'], integrity_problems=ev['integrity_problems'][:50] + probs,
                    claim_scope=(ev.get('reference_scope') or {}).get('claim_scope'))
    L = report_lines(ev) + (['RUN RECORD: ' + '; '.join(probs)] if probs else [])
    (ROOT / 'TEST905_verdict.txt').write_text('\n'.join(L) + '\nRecompute: python 905.py --recompute TEST905_results.json\n')
    for l in L: log(l)
    return tv


# ---------------------------------------------------------------------------------------------------- artefacts / delivery
def drive_copy(src, dst_dir): return M3.drive_copy_verified(src, dst_dir) if M3 is not None else (False, 'NO_ENGINE')


def finalize_artifacts(cfg=None):
    """local artefacts (always kept) -> ZIP copy + read-back -> FINAL receipt copy + byte read-back. The receipt copied to Drive is
    the final one: on success the local and Drive receipts are byte-identical; on failure the local receipt states the failure and
    a failure receipt is attempted on Drive so that both say the same."""
    R['finished_utc'] = datetime.now(timezone.utc).isoformat(); R['elapsed_s'] = round(time.perf_counter() - T0, 1)
    try: M3.save() if M3 and M3.R is R else OUT.write_text(json.dumps(R, ensure_ascii=False, indent=1, default=str))
    except Exception as e: print('RESULTS_WRITE_FAILED', e)
    AG = {}
    try:
        rep = sha_file(OUT); AG['report_written_read_back'] = json.loads(OUT.read_text())['run_id'] == RUN_ID
        files = sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name != 'SHA256SUMS.txt' and not p.name.endswith('.tmp'))
        (ROOT / 'SHA256SUMS.txt').write_text('\n'.join('%s  %s' % (sha_file(p), p.relative_to(ROOT).as_posix()) for p in files) + '\n')
        zp = ROOT.parent / ('TEST905_SONUC_%s.zip' % RUN_ID)
        with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in files + [ROOT / 'SHA256SUMS.txt']: z.write(p, ROOT.name + '/' + p.relative_to(ROOT).as_posix())
        with zipfile.ZipFile(zp) as z:
            AG['zip_testzip'] = z.testzip() is None
            rows = [l.split('  ', 1) for l in z.read(ROOT.name + '/SHA256SUMS.txt').decode().split('\n') if l]
            AG['sha256sums'] = all(sha_b(z.read(ROOT.name + '/' + rel)) == h for h, rel in rows) and len(rows) == len(files)
            AG['report_in_zip_is_read_back_report'] = sha_b(z.read(ROOT.name + '/' + OUT.name)) == rep
        AG['zip'] = str(zp); AG['zip_sha256'] = sha_file(zp)
    except Exception as e:
        AG['artifact_error'] = '%s: %s' % (type(e).__name__, e)
    local_ok = all(AG.get(k) is True for k in ('report_written_read_back', 'zip_testzip', 'sha256sums', 'report_in_zip_is_read_back_report'))
    mode = (cfg or R.get('config') or {}).get('drive', 'auto'); requested = mode == 'required' or (mode == 'auto' and DRIVE_DIR is not None)
    D = {'requested': requested, 'mode': mode, 'dir': DRIVE_DIR, 'zip_copied_read_back': None, 'receipt': 'FINAL_SELF_VERIFIED_BY_BYTE_READ_BACK', 'error': None,
         'live_backup_failures': (getattr(M3, 'DRIVE_ERR', {}) or {}).get('backup_failures') if M3 else None}
    if requested and DRIVE_DIR is None: D['error'] = 'DRIVE_REQUIRED_BUT_NOT_MOUNTED'
    elif requested and local_ok:
        ok, err = drive_copy(Path(AG['zip']), DRIVE_DIR); D['zip_copied_read_back'] = ok
        if not ok: D['error'] = 'ZIP: %s' % err
    if not local_ok: st = 'FAIL_LOCAL_ARTIFACTS'
    elif not requested: st = 'LOCAL_ONLY_DRIVE_NOT_REQUESTED'
    elif D['error']: st = 'DRIVE_ZIP_NOT_DELIVERED'
    else: st = 'PASS'                                                    # final, valid only together with the byte read-back below
    receipt = {'test': TAG, 'run_id': RUN_ID, 'status': R.get('status'), 'top': R.get('top'), 'artifacts': AG, 'drive': D, 'artifact_status': st,
               'results_sha256': sha_file(OUT) if AG.get('report_written_read_back') else None}
    rp = ROOT.parent / ('TEST905_SONUC_%s_RECEIPT.json' % RUN_ID); body = json.dumps(receipt, indent=1, default=str); rp.write_text(body)
    if requested and DRIVE_DIR is not None and local_ok:
        ok, err = drive_copy(rp, DRIVE_DIR)
        if ok:
            try: ok = (Path(DRIVE_DIR) / rp.name).read_text() == body
            except Exception as e: ok, err = False, '%s: %s' % (type(e).__name__, e)
            if not ok and not err: err = 'READ_BACK_MISMATCH'
        if not ok:
            if st == 'PASS': receipt['artifact_status'] = 'DRIVE_RECEIPT_NOT_DELIVERED'
            receipt['drive'] = dict(D, error=(D['error'] + '; ' if D['error'] else '') + 'RECEIPT: %s' % err); body = json.dumps(receipt, indent=1, default=str); rp.write_text(body)
            ok2, _ = drive_copy(rp, DRIVE_DIR)                            # best effort: Drive then carries the same failure state
            try: receipt_drive_state = 'EQUAL' if ok2 and (Path(DRIVE_DIR) / rp.name).read_text() == body else 'ABSENT_OR_STALE'
            except Exception: receipt_drive_state = 'ABSENT_OR_STALE'
            X.RECEIPT_DRIVE_STATE = receipt_drive_state
        else: X.RECEIPT_DRIVE_STATE = 'EQUAL'
    else: X.RECEIPT_DRIVE_STATE = 'NOT_COPIED'
    X.RECEIPT = receipt
    print('TEST905 ARTIFACTS', json.dumps({'artifact_status': receipt['artifact_status'], 'drive_receipt': X.RECEIPT_DRIVE_STATE, 'zip': AG.get('zip')}, default=str), flush=True)
    return receipt


def exit_code(receipt):
    if R.get('status') != 'COMPLETE' or R.get('technical_verdict') != 'PASS': return 1
    return 0 if receipt.get('artifact_status') in ('PASS', 'LOCAL_ONLY_DRIVE_NOT_REQUESTED') else 2


def status_line(rc, receipt):
    t = R.get('top') or {}; a = receipt.get('artifact_status'); d = receipt.get('drive') or {}
    drive = 'PASS' if a == 'PASS' else ('NOT_REQUESTED' if a == 'LOCAL_ONLY_DRIVE_NOT_REQUESTED' else 'FAILED[%s: %s]' % (a, d.get('error')))
    head = {0: 'TAMAMLANDI', 2: 'TAMAMLANDI_TESLIM_HATASI'}.get(rc, 'TEKNIK_HATA')
    return 'TEST905 DURUM: %s | EXIT=%d | TECHNICAL=%s | VERDICT=%s | READS=%s | DRIVE=%s | FIRST_GATE=%s | RESULTS=%s' % (
        head, rc, t.get('technical_verdict'), t.get('verdict'), getattr(X, 'NREAD', None), drive, t.get('first_failed_gate'), OUT)


def gpu_main(cfg):
    global M3, M4, m3
    work = ROOT / 'sources'; work.mkdir()
    ident, b = executed_source_identity(); R['executed_source'] = ident
    if b is not None: (work / 'TEST905_executed_905.py').write_bytes(b)
    p3 = fetch_source(cfg, work, SRC903); p4 = fetch_source(cfg, work, SRC904)
    M4 = load_module(p4, 'akbas_test904_engine'); M3 = m3 = M4.load_903(p3); bind_903(M3)
    if M4.TAG != 'TEST904' or M4.R is not None or M4.RUN_ID is not None: raise Stop905('904_MODULE_STATE')
    M3.log('=' * 112); M3.log(MARKER, '| run', RUN_ID)
    gate('GATE_SOURCES_905', 'PASS', None, src903=SRC903, src904=SRC904, modules_main_not_run=M3.R is R and M4.R is None)
    gate('GATE_EXECUTED_SOURCE', 'PASS' if b is not None else 'FAIL', None if b is not None else
         'the executing 905 file could not be identified; start it as `!python /content/titan-cognitive-core-v3/905.py`', **ident)
    R['status'] = 'GPU_GATES'; M3.boot_runtime(); M3.env_gate(); drive_gate(cfg)
    try: archive_gate(cfg)
    except Stop905 as e: gate('GATE_ARCHIVE_905', 'FAIL', str(e))
    M3.PINNED_CALLS = []
    SRC = M3.obtain_sources(cfg, work); R['sources'] = {n: {'sha256': sha_b(x), 'git_blob': blob_b(x)} for n, x in SRC.items()}
    M3.source_extract_gate(SRC); archive_tensors_gate()
    M3.tokenizer_pre_model_gate(); tokenizer_gate(); manifest_gate()      # manifest (all reads, answers, geometry) BEFORE the model
    M3.model_gate(); engine_gate()
    R['status'] = 'WRITE'; write_all(); work_copies()
    R['status'] = 'READS'; run_reads(); end_gate(); tv = write_verdict()
    R['status'] = 'COMPLETE' if tv == 'PASS' else 'TECHNICAL_INVALID'


def main(argv=None):
    cfg = config(sys.argv[1:] if argv is None else argv)
    if cfg.get('recompute'): return recompute(cfg['recompute'], cfg)
    init_run(cfg)
    try: gpu_main(cfg)
    except BaseException as e:
        tb = traceback.format_exc(); stopped = isinstance(e, Stop905) or type(e).__name__ in ('StopT896', 'Stop904')
        R.update(status='TECHNICAL_ABORT' if stopped else ('INTERRUPTED' if isinstance(e, KeyboardInterrupt) else 'ERROR'),
                 technical_verdict='TECHNICAL_UNDECIDABLE', error='%s: %s' % (type(e).__name__, str(e)[:3000]), traceback=tb)
        R['top'].update(technical_verdict='TECHNICAL_UNDECIDABLE', verdict='TECHNICAL_UNDECIDABLE')
        if R['top']['first_failed_gate'] is None: R['top']['first_failed_gate'] = 'ABORT: ' + str(e)[:200]
        (ROOT / 'TEST905_traceback.txt').write_text(tb); print('TEST905_TECHNICAL_STOP', R['error'][:1500], flush=True)
        with LOG.open('a') as f: f.write('TEST905_TECHNICAL_STOP ' + R['error'][:1500] + '\n')
        if isinstance(e, KeyboardInterrupt): finalize_artifacts(cfg); raise
    receipt = finalize_artifacts(cfg); rc = exit_code(receipt); line = status_line(rc, receipt); print(line, flush=True)
    with LOG.open('a') as f: f.write(line + '\n')
    return rc


def recompute(path, cfg=None):
    """re-score every cell from its raw answer + the run's manifest + the object registry (no model / torch); needs the pinned
    904.py only for its pure parser (taken from the run's sources/ folder or the repo)."""
    p = Path(path); Rj = json.loads(p.read_text()); b = (p.parent / 'TEST905_manifest.json').read_bytes(); man = json.loads(b)
    cand = [p.parent / 'sources' / '904.py'] + ([Path(cfg['repo_dir']) / '904.py'] if cfg and cfg.get('repo_dir') else []) + [Path(__file__).parent / '904.py' if '__file__' in globals() else Path('904.py')]
    src = next((c for c in cand if c.is_file() and blob_b(c.read_bytes()) == SRC904['git_blob']), None)
    if src is None: print('904.py with blob %s not found next to the run or in the repo' % SRC904['git_blob']); return 1
    m4 = load_module(src, 'akbas_test904_parser')
    gates_ok = all(g.get('status') != 'FAIL' for g in (Rj.get('gates') or {}).values()) and not Rj.get('technical_blockers')
    ev = evaluate_905(man, Rj.get('cells', []), Rj.get('objects', {}), gates_ok, m4, refs=Rj.get('upper_reference') or [])
    if Rj.get('technical_verdict') != 'PASS' and Rj.get('status') == 'TECHNICAL_INVALID': ev['verdict'] = 'TECHNICAL_UNDECIDABLE'
    probs = verify_run_record(Rj, b, ev)
    marker = '/TEST905_%s/' % Rj.get('run_id')
    for key, o in (Rj.get('objects') or {}).items():                    # object files, when present next to the results
        f = p.parent / str(o.get('file', '')).split(marker)[-1] if marker in str(o.get('file', '')) else None
        if f is not None and f.is_file() and sha_file(f) != o.get('sha256'): probs.append('OBJECT_FILE_SHA_MISMATCH:' + key)
    print('RECOMPUTED %s | record problems: %d' % (ev['verdict'], len(probs) + len(ev['integrity_problems'])))
    for l in report_lines(ev): print(l)
    for x in probs: print('RUN RECORD PROBLEM:', x)
    return 0 if not probs and not ev['integrity_problems'] else 1


if __name__ == '__main__':
    _rc = main(None)
    if _rc and 'get_ipython' not in globals(): sys.exit(_rc)
