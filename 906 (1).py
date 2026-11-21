# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST906 — Native Relational Bridge (NRB): with the parent episode and the final event E open,
#   the frozen model writes ONE greedy relation-agnostic inventory Z; Z becomes a sealed conditioned CUT3 cartridge (H3 + L0-L3
#   K/V); with no parent token, parent K/V row or parent text present, does the sealed Z cartridge alone drive the native greedy
#   answer to the old b question (controlled)? Claim boundary: model-generated EXPLICIT physical memory, parent-free causal readout.
#
# FILE: 906.py (root of ceceli33/titan-cognitive-core-v3, next to the unchanged 903.py and 904.py). Colab A100, either way:
#   (1) copy the WHOLE 906.py from GitHub main ("Copy raw file") into ONE EMPTY notebook cell and run that cell; the cell text is
#       compared with 906.py on GitHub main before anything else runs; or
#   (2) !python /content/titan-cognitive-core-v3/906.py   (the saved file's bytes are the identity)
#   Offline re-scoring from the raw records (no model, no torch):  python 906.py --recompute TEST906_results.json
#     default VERIFIED mode: exit 0 only if the record is authenticated (all required gates PASS in record + event log, SHA256SUMS,
#     object files, executed source, receipt); exit 3 = rescored consistently but NOT_AUTHENTICATED; --recompute-mode rescore =
#     OFFLINE_RESCORE (scoring only, provenance not certified).
# ORDER (fixed): source identity -> 903/904 pins -> A100 PRE-FLIGHT (torch only, no Drive, no model; on failure
#   GPU_REQUIRED_A100_TECHNICAL_STOP and nothing is written to Drive) -> runtime pins -> Drive mount + FUSE + write/read-back
#   probe -> 903 archive by pinned SHA -> blob-pinned engine sources -> tokenizer, disk, sealed manifest -> model -> 12 compiles
#   -> writes -> 64 reads -> <= 8 failure references -> end gate -> verdict -> ZIP + receipt with byte read-back.
# Exit code (never set by the scientific verdict): 0 complete + valid + requested Drive delivery verified; 2 complete + valid but the
#   Drive delivery failed (local results kept); 1 technical abort / invalid.
#
# GEOMETRY. Compile: mount_sealed([h1_w (903 parent, NATIVE), C1_w (903 E written with the parent open, CHILD)]) = prefix [0,30),
#   parent [30,49), E [49,68); the 709 answer() suffix with COMPILE_TEXT follows from 68 and is DISCARDED with the generation cache.
#   Forge: a FRESH parent+E mount (bit-equal to the compile mount) and ONLY the generated Z ids through 903 forge_conditioned_903
#   at positions 68..68+m-1 (1 <= m <= 64): H3 + L0-L3 K/V of Z, pos0 = 68. Read: archived empty prefix + Z via the 903 child mount
#   (native_append_child_903): K of L0-L3 rephased 68 -> 30 once, V unchanged, L4-L79 rebuilt from H3 with no parent; query from
#   30+m. The compile suffix never enters the cartridge, so the written factor is Z's content in the parent+E context only.
# COMPILE (sealed before the model): one greedy 709 answer() call, budget 65 = 64 storable tokens + 1 stop-detection token. 0
#   tokens or any special token -> COMPILER_INVALID; 65 tokens (no stop inside 64) -> CAPACITY_LIMIT; never retried, truncated,
#   padded, edited or re-selected. The compile text names no action, outcome, question, option or evaluator.
# PANEL (fixed; 4 name/role groups x FWD/REV = 8 units x 8 reads = 64 native greedy reads; 12 compiles; <= 8 failure references):
#   NRB_H1, NRB_HG (own Z) | NRB_CROSS (file shown as Z_s, tensors of the other world) | NRB_SHAM (own Z_s tensors, alias file) |
#   NRB_H2_NEG (Z of the uninformative world) | E_ONLY_NEG (archived clean C1_s, no bridge) | DIRECT_FACT (b->r / b->g written
#   as E after a->q, 905 method, clean child mount) | PARENT_POS (archived parent only). s = H1 / HG balanced over groups and orders.
#   CROSS and SHAM mount exactly the tensors of an own read: under greedy decoding they test that labels, file names and book ids
#   cannot route an answer (harness attribution), not the model; the causal contrast is H1 vs HG own (same E, prefix, query).
# r2 = GPU CANDIDATE, NOT GPU-VERIFIED. NOT EXECUTED ON GPU BY ITS AUTHOR (GPU_NOT_RUN_BY_AUTHOR). CPU tests cover identity, gate order, geometry, compile status,
#   inventory classification, integrity, verdicts, failure references, delivery states and recompute.
# =====================================================================================================================
import os, sys, json, hashlib, re, time, shutil, subprocess, zipfile, types, traceback, importlib.util, stat, marshal
from pathlib import Path
from datetime import datetime, timezone
sys.dont_write_bytecode = True

TAG = 'TEST906'
REVISION = 'r2: K3.1 Pro audit fixes (runtime guards, compile precedence, inventory axis, authenticated recompute, failure-reference integrity, single definitions)'
MARKER = 'AKBASCORE SILICON HIPPOCAMPUS — TEST906 — model-generated relation inventory as a parent-free CUT3 cartridge'
SRC_REPO = 'ceceli33/titan-cognitive-core-v3'
SRC_URL = 'https://github.com/' + SRC_REPO
SELF_FILE = '906.py'
SRC903 = {'file': '903.py', 'commit': 'ad228a29aacfc485377ed1d1a7aecae4d3201488', 'git_blob': 'f883d3dfa4c493bab4e4dc41b5743b30102ebd37',
          'sha256': '97fce064f5dafc18455d05ab015b9a476b063c801b7206401afbdfde1bc73ebc'}
SRC904 = {'file': '904.py', 'commit': 'ad228a29aacfc485377ed1d1a7aecae4d3201488', 'git_blob': '2ffacbec3b089759c89bf843d3725d617113d0ce',
          'sha256': 'c2d894d79f9d411bc8a8f7f2821fbcf3c67e41fd9f5b897d7f1e52a0cd20423b'}
# provenance only: 906 is derived from this 905 (infrastructure copied, science replaced); 905 is NOT imported or run
SRC905 = {'file': '905.py', 'commit': '48533d5aecae491b6db0dc6afecc9a48cdefa147', 'git_blob': 'b06f6ddb15e6d7d9218ae137cc5d3ea1481d8056',
          'sha256': '4c378a9aeaeb7d41b06863603588076c462d5c08861c66507a786bfe0b8fff2b', 'log_commit': '5c8ac8350cee99a33b8e915c1d676dc391c14761'}
RUN905 = {'run_id': '20261121T075930Z', 'verdict': 'NO_B_GAIN[8/8 evaluable; 0 A-only; 0 both; 8 neither]', 'reads': 192,
          'zip_sha256': '650006747265578391126b714f6c447133563c4fa7e0cee726f9fdaabb5b8d9b',
          'results_sha256': '82fc758adb71d80905cd9e3a85e56d921ca378cecd894fc93c08a04224538c90',
          'evidence': 'verdict and read count from 905.log on GitHub; hashes as transferred by the user (Drive not read by the author)'}
MYDRIVE = Path('/content/drive/MyDrive')
DEFAULT_ARCHIVE_903 = '/content/drive/MyDrive/TEST903_20261120T192235Z'

GEOM = {'P': 30, 'parent_rows': [30, 49], 'E_rows': [49, 68], 'n_E': 19, 'z_source_pos0': 68, 'z_target_pos0': 30, 'query_start': '30 + m',
        'max_compile': 64, 'cut': 3, 'layers': 80, 'kv_heads': 8, 'head_dim': 128,
        'compile_context': 'mount_sealed([h1_w, C1_w]) (68 rows) + 709 answer() suffix with COMPILE_TEXT; generation cache discarded',
        'forge_context': 'fresh mount_sealed([h1_w, C1_w]) bit-equal to the compile mount; only Z ids forwarded at 68..68+m-1',
        'read': 'archived empty prefix + Z child (K of L0-L3 rephased 68 -> 30 once, V unchanged, L4-L79 rebuilt from H3); parent rows 0'}
COMPILE_TEXT = ('Using only the observed episode in memory, produce a compact factual inventory of all distinct observed events and revisions. '
                'Preserve every actor, action, outcome, ordering and contradiction that is explicitly observed. Do not infer missing '
                'outcomes, answer a question, predict, evaluate importance, or add new facts. Stop when the inventory is complete.')
COMPILE_TEXT_SHA256 = '008088cc9eeedbc58e27c79f6209efda224b9e578ffd7ba987ff2261923fd540'   # sha256 of COMPILE_TEXT (UTF-8), checked at import
MAX_COMPILE = 64; COMPILE_PROBE = MAX_COMPILE + 1; MAX_NEW_READ = 25
VARIANTS = (('NS-A', 'R0'), ('NS-A', 'R1'), ('NS-B', 'R0'), ('NS-B', 'R1')); ORDERS = ('FWD', 'REV'); WORLDS = ('H1', 'HG', 'H2')
HIST = {'H1': ('b', 'r'), 'HG': ('b', 'g'), 'H2': ('a', 'q')}; E_FACT = ('a', 'q')          # = 903 HIST / E_FACT (checked at the gate)
OUT_ROLE = {'H1': 'r', 'HG': 'g'}; OTHER = {'H1': 'HG', 'HG': 'H1'}; TC_OF = {'H1': 'TC_R', 'HG': 'TC_G'}
NEEDED_EXTRA = {'h1_H2': ('_H2_h1', 'NATIVE', 'H2')}                 # 904's NEEDED + the H2 parent (a->q, no b)
ARM_NAMES = ('NRB_H1', 'NRB_HG', 'NRB_CROSS', 'NRB_SHAM', 'NRB_H2_NEG', 'E_ONLY_NEG', 'DIRECT_FACT', 'PARENT_POS')
NRB_OWN = ('NRB_H1', 'NRB_HG'); CONTROL_ARMS = ('PARENT_POS', 'DIRECT_FACT', 'E_ONLY_NEG', 'NRB_SHAM')
TOL906 = {'rope_reference_cos_min': 0.9995, 'file_bytes_max_factor': 1.25, 'file_bytes_slack': 65536,
          'raw_bytes_per_token': 8192 * 2 + 4 * 2 * 8 * 128 * 2, 'created_bridge_raw_bytes_max': 40 * 2**20,
          'note': 'fixed before data; RoPE tolerance and bounds are those of TEST905'}
BUDGET = {'compiles': 12, 'compile_generation_tokens_max_each': COMPILE_PROBE, 'main_reads': 64, 'failure_reference_reads_max': 8,
          'greedy_sequences_max': 12 + 64 + 8, 'read_generation_tokens_max_each': MAX_NEW_READ,
          'generated_tokens_max': 12 * COMPILE_PROBE + 64 * MAX_NEW_READ + 8 * MAX_NEW_READ,
          'note': '2580 = contract 2568 + 12 stop-detection tokens (one per compile); stored Z tokens <= 64'}
CRITICAL_906 = ('GATE_SOURCES_906', 'GATE_EXECUTED_SOURCE', 'GATE_GPU_PREFLIGHT_906', 'GATE_VRAM_FREE', 'GATE_DRIVE_PRESENT', 'GATE_DRIVE',
                'GATE_ARCHIVE_906', 'GATE_ARCHIVE_TENSORS_906', 'GATE_TOKENIZER_906', 'GATE_DISK_906', 'GATE_MANIFEST_906', 'GATE_ENGINE_906',
                'GATE_COMPILE_906', 'GATE_WRITE_906', 'GATE_ROPE_906', 'GATE_WORK_COPIES_906', 'GATE_READS_906', 'GATE_FAILREF_906', 'GATE_END_906',
                'GATE_RUNTIME_LIMITS_906')
# every gate a COMPLETE run passes (in order); --recompute authenticates a record only if all are PASS (also in the event log)
REQUIRED_PASS_GATES = ('GATE_SOURCES_906', 'GATE_EXECUTED_SOURCE', 'GATE_GPU_PREFLIGHT_906', 'GATE_RUNTIME_PINS', 'GATE_ENV', 'GATE_VRAM_FREE',
                       'GATE_DRIVE_PRESENT', 'GATE_DRIVE', 'GATE_ARCHIVE_906', 'GATE_SOURCE_EXTRACT', 'GATE_ARCHIVE_TENSORS_906', 'GATE_TOKENIZER_PRE_MODEL',
                       'GATE_TOKENIZER_906', 'GATE_DISK_906', 'GATE_MANIFEST_906', 'MODEL', 'GATE_ENGINE_906', 'GATE_COMPILE_906', 'GATE_WRITE_906',
                       'GATE_ROPE_906', 'GATE_WORK_COPIES_906', 'GATE_READS_906', 'GATE_FAILREF_906', 'GATE_END_906')


def sha_b(b): return hashlib.sha256(b).hexdigest()
def sha_s(s): return sha_b(s.encode('utf-8'))
def blob_b(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
def canon(v): return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(',', ':'), default=list)
def jsha(v): return sha_s(canon(v))
def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(4 << 20), b''): h.update(c)
    return h.hexdigest()



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




class Stop906(Exception):
    """technical stop (never a scientific result); the message names the gate / object."""


if sha_s(COMPILE_TEXT) != COMPILE_TEXT_SHA256: raise Stop906('COMPILE_TEXT_CHANGED')


# ===================================================================================================== design (pure)
def cell_id(ns, pm, order, arm): return 'T906/%s/%s/%s/%s' % (ns, pm, order, arm)
def ref_cell_id(ns, pm, world): return 'T906/%s/%s/REF_%s' % (ns, pm, world)


def slot_of(gi, order):
    """balanced direction of CROSS / SHAM / E_ONLY_NEG / DIRECT_FACT / PARENT_POS: each group sees H1 in one order and HG in the
    other, each order sees H1 in two groups and HG in two (not confounded with the answer order)."""
    return 'H1' if (gi + ORDERS.index(order)) % 2 == 0 else 'HG'


def arm_sources(s):
    """READ-PATH view of the panel (no expected answers): arm -> (source object keys in mount order, shown label, copy kind).
    CROSS: a file shown as Z_s holding the tensors of Z_other(s). SHAM: Z_s tensors in an alias file."""
    o = OTHER[s]
    return {'NRB_H1': (['Z_H1'], None, None), 'NRB_HG': (['Z_HG'], None, None), 'NRB_CROSS': (['Z_' + o], 'Z_' + s, 'CROSS'),
            'NRB_SHAM': (['Z_' + s], 'ALIAS', 'SHAM'), 'NRB_H2_NEG': (['Z_H2'], None, None), 'E_ONLY_NEG': (['C1_' + s], None, None),
            'DIRECT_FACT': ([TC_OF[s]], None, None), 'PARENT_POS': (['h1_' + s], None, None)}


def arm_plan(s):
    """EVALUATOR view: arm_sources + the expected answer role (CROSS: the physical tensors decide; SHAM: = own Z_s answer)."""
    o = OTHER[s]; exp = {'NRB_H1': 'r', 'NRB_HG': 'g', 'NRB_CROSS': OUT_ROLE[o], 'NRB_SHAM': OUT_ROLE[s], 'NRB_H2_NEG': 'UNKNOWN',
                         'E_ONLY_NEG': 'UNKNOWN', 'DIRECT_FACT': OUT_ROLE[s], 'PARENT_POS': OUT_ROLE[s]}
    out = {}
    for arm, (src, shown, copy) in arm_sources(s).items():
        out[arm] = {'sources': src, 'shown': shown, 'copy': copy, 'expected_role': exp[arm]}
        if arm == 'NRB_SHAM': out[arm]['invariant_to'] = 'NRB_' + s
    return out


def plan_objects(groups, empty, tc_ids_sha):
    """every object a read may mount: archived (903 ZIP) and created by this run, with lineage, before the model."""
    plan = {'EMPTY': dict(empty, key='EMPTY')}
    for (ns, pm), g in groups.items():
        p = '%s/%s/' % (ns, pm)
        for k, c in g.items():
            plan[p + k] = {'key': k, 'origin': 'ARCHIVE_903', 'cid': c['cid'], 'member': c['member'], 'sha256': c['sha256'],
                           'tensor_seal_sha256': jsha(c['tensor_seal']) if c.get('tensor_seal') is not None else None, 'kind': c['kind'],
                           'history': c['history'], 'n': int(c['n']), 'body_tokens': int(c['body_tokens']), 'pos0': c['pos0']}
        for w in WORLDS:
            plan[p + 'Z_' + w] = {'key': 'Z_' + w, 'origin': 'CREATED_906', 'kind': 'CHILD', 'history': w, 'pos0': GEOM['z_source_pos0'], 'n': 'm',
                                  'parent_keys': [p + 'h1_' + w, p + 'C1_' + w], 'conditional_on': 'compile status VALID',
                                  'computation': '903 forge_conditioned_903 of the generated Z ids on a fresh mount_sealed([h1_w, C1_w])'}
        for w, key in TC_OF.items():
            plan[p + key] = {'key': key, 'origin': 'CREATED_906', 'kind': 'CHILD', 'history': 'H2', 'pos0': 49, 'n': 19, 'parent_keys': [p + 'h1_H2'],
                             'ids_sha256': tc_ids_sha[p + key], 'record_roles': list(HIST[w]),
                             'computation': '903 forge_conditioned_903 of the b record on mount_sealed([h1_H2]) (TEST905 method)'}
        for w in OUT_ROLE:
            plan[p + 'REF_' + w] = {'key': 'REF_' + w, 'origin': 'CREATED_906', 'kind': 'CHILD', 'history': w, 'pos0': GEOM['z_source_pos0'], 'n': 'm(Z_%s)' % w,
                                    'parent_keys': [p + 'h1_' + w, p + 'C1_' + w], 'conditional_on': 'failure-reference trigger only',
                                    'computation': 'as Z_w, ids = source b record (19) + (m-19) x pad id'}
    return plan


def build_manifest(groups, plan, tokinfo, NAMES, PERMS, archive, M4):
    cells = {}; units = {}; grp = {}
    for gi, (ns, pm) in enumerate(VARIANTS):
        V = M4.names_of(ns, pm, NAMES, PERMS); gk = '%s/%s' % (ns, pm)
        grp[gk] = {'names': V, 'actions': {V[k]: k for k in ('a', 'b', 'c')}, 'outcomes': {V[k]: k for k in ('g', 'q', 'r')},
                   'reference_record_ids': {w: tokinfo['ref_record_ids'][gk + '/' + w] for w in OUT_ROLE}}
        for order in ORDERS:
            outs = M4.outcome_order(ns, order, NAMES); q = M4.query_904(V['b'], outs); u = '%s/%s/%s' % (ns, pm, order); s = slot_of(gi, order)
            units[u] = {'ns': ns, 'perm': pm, 'order': order, 'group': gk, 'slot': s, 'b_name': V['b'], 'outcome_order': outs, 'query': q,
                        'query_sha256': sha_s(q), 'outcome_roles': {V[k]: k for k in ('g', 'q', 'r')}}
            for arm, a in arm_plan(s).items():
                cells[cell_id(ns, pm, order, arm)] = {
                    'unit': u, 'ns': ns, 'perm': pm, 'order': order, 'arm': arm, 'slot': s, 'sources': ['%s/%s/%s' % (ns, pm, k) for k in a['sources']],
                    'shown': a['shown'], 'copy': a['copy'], 'query_sha256': sha_s(q), 'expected_role': a['expected_role'],
                    'expected_answer': 'UNKNOWN' if a['expected_role'] == 'UNKNOWN' else V[a['expected_role']], 'invariant_to': a.get('invariant_to')}
    compiles = {'%s/%s/Z_%s' % (ns, pm, w): {'group': '%s/%s' % (ns, pm), 'world': w, 'mount_sources': ['%s/%s/h1_%s' % (ns, pm, w), '%s/%s/C1_%s' % (ns, pm, w)]}
                for ns, pm in VARIANTS for w in WORLDS}
    return {'test': TAG, 'marker': MARKER, 'archive': archive, 'geometry': GEOM, 'tolerances': TOL906, 'budget': BUDGET, 'objects': plan,
            'groups': grp, 'units': units, 'cells': cells, 'n_cells': len(cells), 'compiles': compiles,
            'compile': {'text': COMPILE_TEXT, 'text_sha256': COMPILE_TEXT_SHA256, 'suffix_ids_sha256': tokinfo['compile_suffix_ids_sha256'],
                        'suffix_tokens': tokinfo['compile_suffix_tokens'], 'max_store': MAX_COMPILE, 'probe_budget': COMPILE_PROBE,
                        'special_ids': tokinfo['special_ids'], 'stop_ids': tokinfo['stop_ids'], 'decoding': 'one greedy 709 answer() call, no retry',
                        'compile_cache_tokens_max': 68 + tokinfo['compile_suffix_tokens'] + COMPILE_PROBE},
            'failure_reference': {'trigger': FAILREF_RULE, 'pad_id': tokinfo['pad_id'], 'max_reads': 8},
            'design': {'arms': {s: arm_plan(s) for s in ('H1', 'HG')}, 'query_template': M4.QUERY_TPL_904, 'normalization': M4.NORMALIZATION,
                       'max_new_read': MAX_NEW_READ, 'answer_token_feasibility': tokinfo['answers'], 'inventory_rule': INVENTORY_RULE,
                       'order_axis': 'FWD/REV re-read the same 4 physical groups; 8 units are not 8 independent worlds'},
            'verdict_rules': VERDICT_RULES_906}


INVENTORY_RULE = ('offline only, after the compile is sealed: Z text split at newlines and after . ; ! ?; in each segment the exact '
                  'public action / outcome names of the group are located (whole-word); a segment whose matches alternate action, outcome '
                  '(k actions, k outcomes) asserts those k pairs; any other segment with names is AMBIGUOUS and asserts nothing. Observed '
                  'relations of world w = {parent HIST[w], E a->q}. COMPILER_HALLUCINATION: an asserted pair not observed; else '
                  'COMPILER_OMISSION: an observed relation not asserted; else COMPILER_COMPLETE. queried (H1/HG) = PRESENT if the b '
                  'outcomes asserted are exactly {o_w}, WRONG if another b outcome is asserted, ABSENT otherwise. Z is never edited.')
FAILREF_RULE = ('after the 64 main reads are sealed: for each group and w in H1/HG with Z_w VALID, queried PRESENT, and an own NRB_w read '
                'that is not role o_w in an order (FWD checked first): m < 19 -> REFERENCE_GEOMETRY_UNAVAILABLE (no read); else one read of '
                'REF_w = the source b record ids (19) + (m-19) pad ids, forged exactly as Z_w (pos0 68, n m) and mounted as Z_w, with the '
                'query of that failing order. Diagnostic only; never in the scientific denominator.')
VERDICT_RULES_906 = {
    'cell_ok': '904 parse (exact name / UNKNOWN after the fixed normalization); answer role == expected_role; INVALID never repaired',
    'compile_status': ('precedence: non-int / negative / 0 ids -> COMPILER_INVALID; any special id anywhere (also within 65) -> COMPILER_INVALID; '
                       '> 65 -> COMPILER_INVALID; 65 non-special ids (no stop within 64) -> CAPACITY_LIMIT; else VALID (m = ids); only VALID writes a Z'),
    'unit_category': ('precedence: TECHNICAL_UNDECIDABLE; CAPACITY_LIMIT / COMPILER_INVALID (Z_H1 or Z_HG has no cartridge); LENGTH_MISMATCH '
                      '(m_H1 != m_HG); CONTROL_UNAVAILABLE[NRB_H2_NEG] (Z_H2 has no cartridge); CONTROLS_FAILED[...] (PARENT_POS or '
                      'DIRECT_FACT wrong, E_ONLY_NEG not UNKNOWN, SHAM raw != own raw of the same tensors); evaluable: own H1 and HG '
                      'correct -> (queried PRESENT in both Z else CORRECT_WITHOUT_EXPLICIT_RELATION) -> NRB_SUCCESS if CROSS follows the '
                      'physical tensors and NRB_H2_NEG is UNKNOWN, else PHYSICAL_ATTRIBUTION_FAILURE; own read wrong -> COMPILER_OMISSION '
                      '(queried ABSENT in a failing world), COMPILER_HALLUCINATION (WRONG), else BRIDGE_PRESENT_BUT_UNREADABLE'),
    'overall': ('precedence: TEST906_INVALID (read / compile path isolation broken); TECHNICAL_UNDECIDABLE (any gate, integrity or record '
                'problem); e = evaluable units, u = NRB_SUCCESS units, g = groups (of 4) with NRB_SUCCESS in both orders; e = 0 -> '
                'UNDECIDABLE_NO_EVALUABLE_UNIT[...]; u >= 1 -> NRB_PHYSICAL_CAUSAL_READOUT[u/8; g/4] (coverage FULL iff u = 8); u = 0 -> '
                'NO_NRB_READOUT[e/8 evaluable; per-category counts]. Raw own-read counts are reported and are never a scientific gain. '
                '"readout panel coverage FULL" means u = 8 units; it says nothing about inventory completeness.'),
    'inventory_quality': ('SEPARATE axis, never the verdict: per Z COMPILER_COMPLETE / OMISSION / HALLUCINATION / CAPACITY_LIMIT / INVALID and '
                          'Z with AMBIGUOUS segments; per unit whether Z_H1 and Z_HG are both COMPLETE; NRB_SUCCESS units split into with / '
                          'without complete inventories. COMPLETE_RELATION_AGNOSTIC_INVENTORY is confirmed only if all 12 Z are COMPLETE with no '
                          'ambiguous segment.'),
    'scope': ('NRB_PHYSICAL_CAUSAL_READOUT means: for the measured groups, relation and query, a model-generated explicit inventory '
              'written as a sealed parent-free cartridge carries the old b outcome to the native greedy answer, with the label-routing, '
              'negative and positive controls passing. It is not implicit E memory, not general autonomy, not every query. Z is written '
              'conditioned on parent+E, so success shows the cartridge suffices, not that its explicit tokens alone do (see audit). It '
              'does not show that the compiler wrote every observation completely and without hallucination: that is the separate '
              'inventory_quality axis.')}


# ===================================================================================================== compile status + inventory (pure)
def duplicate_top_level(src):
    """top-level def / class names bound more than once in the module, also by a later top-level assignment or import (a later
    binding silently replaces the earlier function): {name: [line numbers]}."""
    import ast
    defs = {}; binds = {}
    for n in ast.parse(src).body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)): defs.setdefault(n.name, []).append(n.lineno)
        elif isinstance(n, (ast.Assign, ast.AnnAssign, ast.Import, ast.ImportFrom)):
            for t in (n.targets if isinstance(n, ast.Assign) else [getattr(n, 'target', None)] if isinstance(n, ast.AnnAssign) else []):
                for x in ast.walk(t):
                    if isinstance(x, ast.Name): binds.setdefault(x.id, []).append(n.lineno)
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                for al in n.names: binds.setdefault((al.asname or al.name).split('.')[0], []).append(n.lineno)
    return {k: sorted(v + binds.get(k, [])) for k, v in defs.items() if len(v) + len(binds.get(k, [])) > 1}


def compile_text_leaks(text, public_names, query_template):
    """anything of the future question in the compile text: a public action / outcome name, the UNKNOWN option, or any 4-word run
    of the 904 query template (case-insensitive)."""
    low = text.lower(); out = [x for x in list(public_names) + ['UNKNOWN'] if x.lower() in low]
    w = re.findall(r"[a-z]+", query_template.lower().replace('{b}', ' ').replace('{outs}', ' '))
    out += [' '.join(w[i:i + 4]) for i in range(len(w) - 3) if ' '.join(w[i:i + 4]) in ' '.join(re.findall(r"[a-z]+", low))]
    return out


def compile_status(gen_ids, special_ids):
    """precedence (r2): not a list of non-negative int -> INVALID; empty -> INVALID; ANY special id (any position, also inside 65)
    -> INVALID; more than the probe budget -> INVALID; exactly 65 non-special ids (no stop within 64) -> CAPACITY_LIMIT; else VALID."""
    if not isinstance(gen_ids, list) or not all(isinstance(i, int) and not isinstance(i, bool) for i in gen_ids): return 'COMPILER_INVALID', 'IDS_NOT_A_LIST_OF_INT'
    if any(i < 0 for i in gen_ids): return 'COMPILER_INVALID', 'NEGATIVE_ID'
    if len(gen_ids) == 0: return 'COMPILER_INVALID', 'EMPTY'
    sp = sorted(set(gen_ids) & set(special_ids))
    if sp: return 'COMPILER_INVALID', 'SPECIAL_IDS %s' % sp
    if len(gen_ids) > COMPILE_PROBE: return 'COMPILER_INVALID', 'MORE_IDS_THAN_THE_PROBE_BUDGET'
    if len(gen_ids) == COMPILE_PROBE: return 'CAPACITY_LIMIT', 'NO_STOP_WITHIN_%d' % MAX_COMPILE
    return 'VALID', None


def _find(names, s):
    out = []
    for name, role in names.items():
        for mt in re.finditer(r'(?<![A-Za-z0-9])%s(?![A-Za-z0-9])' % re.escape(name), s): out.append((mt.start(), role))
    return out


def inventory_relations(text, actions, outcomes):
    asserted, ambiguous, mentioned = [], [], set()
    for line in (text or '').split('\n'):
        for seg in re.split(r'(?<=[.;!?])\s+', line):
            A = _find(actions, seg); O = _find(outcomes, seg); mentioned |= {r for _, r in A} | {r for _, r in O}
            if not A and not O: continue
            seq = sorted([(p, 'A', r) for p, r in A] + [(p, 'O', r) for p, r in O])
            if len(A) == len(O) and [k for _, k, _ in seq] == ['A', 'O'] * len(A):
                asserted += [(seq[2 * i][2], seq[2 * i + 1][2]) for i in range(len(A))]
            else: ambiguous.append(seg)
    return asserted, ambiguous, sorted(mentioned)


def classify_inventory(world, text, actions, outcomes):
    observed = {HIST[world], E_FACT}; asserted, amb, mentioned = inventory_relations(text, actions, outcomes); A = set(asserted)
    halluc = sorted(p for p in A if p not in observed); omitted = sorted(p for p in observed if p not in A)
    status = 'COMPILER_HALLUCINATION' if halluc else ('COMPILER_OMISSION' if omitted else 'COMPILER_COMPLETE')
    if world in OUT_ROLE:
        bs = {o for a, o in A if a == 'b'}
        queried = 'PRESENT' if bs == {OUT_ROLE[world]} else ('WRONG' if bs - {OUT_ROLE[world]} else 'ABSENT')
    else: queried = 'NOT_APPLICABLE'
    return {'status': status, 'queried': queried, 'asserted': sorted(A), 'hallucinated': halluc, 'omitted': omitted, 'ambiguous_segments': amb,
            'mentioned_roles': mentioned}


def compiler_table(man, compiles):
    """per Z: generation status (from the ids), m, inventory class (from the text), queried-relation status."""
    C = {c.get('key'): c for c in compiles if isinstance(c, dict)}; out = {}
    for key, plan in man['compiles'].items():
        c = C.get(key) or {}; G = man['groups'][plan['group']]; ids = c.get('gen_ids')
        st, why = compile_status(ids, man['compile']['special_ids']) if c else ('MISSING', 'NO_RECORD')
        row = {'key': key, 'group': plan['group'], 'world': plan['world'], 'generation_status': st, 'reason': why, 'valid': st == 'VALID',
               'm': len(ids) if st == 'VALID' else None, 'raw': c.get('raw')}
        if st == 'VALID': row.update(classify_inventory(plan['world'], c.get('raw') or '', G['actions'], G['outcomes']))
        else: row.update(status=st, queried='NO_CARTRIDGE')
        out[key] = row
    return out


# ===================================================================================================== geometry + integrity (pure)
def expected_geometry(src, P=30):
    """mount length and RoPE placement from the object registry: CHILD rows n from pos0, NATIVE body_tokens from P."""
    at = P; rope = []
    for t in src:
        k = t['n'] if t['kind'] == 'CHILD' else t['body_tokens']; s0 = t['pos0'] if t['kind'] == 'CHILD' else P
        rope.append({'key': t['key'], 'source_pos0': s0, 'target_pos0': at}); at += k
    return at, rope


HEX64 = re.compile(r'^[0-9a-f]{64}$')
REC_STR = ('cell_id', 'unit', 'ns', 'perm', 'order', 'arm', 'slot', 'query_sha256', 'status')


def _hex(v): return isinstance(v, str) and bool(HEX64.match(v))


def integrity_906(man, compiles, cells, objects, refcells=None):
    """(problem, id). Compiles: 12 planned once, sealed text / suffix, status re-derived from the ids. Objects: every planned object
    present iff it must exist, bound to its lineage (Z: m = generated ids, ids SHA, parents, parent+E mount seal = compile mount
    seal). Cells: 64 planned once; READ cells bound to the registry (file SHA / tensor seal / kind; CROSS / SHAM copies = other file
    SHA + same tensor seal + label), mount length and RoPE placement re-derived, seals present, identical tensors -> identical mount
    seal, one prefix seal; NOT_RUN only when a source Z has no cartridge. Failure references = the plan re-derived from the cells."""
    prob = []; P = man['objects']; O = objects or {}; tbl = compiler_table(man, compiles)
    cc = {}
    for c in compiles:
        k = c.get('key') if isinstance(c, dict) else None; cc[k] = cc.get(k, 0) + 1
        if k not in man['compiles']: prob.append(('UNKNOWN_COMPILE', k)); continue
        bad = []
        if c.get('compile_text_sha256') != man['compile']['text_sha256']: bad.append('compile_text')
        if c.get('suffix_ids_sha256') != man['compile']['suffix_ids_sha256']: bad.append('suffix_ids')
        if c.get('mount_sources') != man['compiles'][k]['mount_sources']: bad.append('mount_sources')
        if not _hex(c.get('mount_seal_sha256')): bad.append('mount_seal')
        if c.get('status') != tbl[k]['generation_status']: bad.append('status_ne_rule')
        if tbl[k]['valid'] and c.get('gen_ids_sha256') != sha_s(json.dumps(c['gen_ids'])): bad.append('gen_ids_sha256')
        if bad: prob.append(('CONTRADICTORY_COMPILE%s' % bad, k))
    for k in man['compiles']:
        if cc.get(k, 0) == 0: prob.append(('MISSING_COMPILE', k))
        elif cc[k] > 1: prob.append(('DUPLICATE_COMPILE(x%d)' % cc[k], k))
    C = {c.get('key'): c for c in compiles if isinstance(c, dict)}
    refs = [r for r in (refcells or []) if isinstance(r, dict)]; ref_keys = {'%s/REF_%s' % (r.get('group'), r.get('world')) for r in refs if r.get('status') == 'READ'}
    for key, p in P.items():
        if key == 'EMPTY': continue
        must = True
        if p['origin'] == 'CREATED_906' and p['key'].startswith('Z_'): must = tbl.get(key, {}).get('valid', False)
        if p['origin'] == 'CREATED_906' and p['key'].startswith('REF_'): must = key in ref_keys
        if must and key not in O: prob.append(('MISSING_OBJECT', key))
        if not must and key in O: prob.append(('OBJECT_WITHOUT_ITS_CONDITION', key))
    for key, o in O.items():
        p = P.get(key)
        if p is None: prob.append(('UNKNOWN_OBJECT', key)); continue
        bad = [f for f in ('kind', 'pos0') if o.get(f) != p.get(f)]
        if p['origin'] == 'ARCHIVE_903':
            if o.get('sha256') != p['sha256']: bad.append('archive_sha256')
            if o.get('n') != p.get('n'): bad.append('n')
        else:
            par = [(O.get(pk) or {}).get('sha256') for pk in p['parent_keys']]
            if o.get('parent_sha256') != (par if len(par) > 1 else par[0]): bad.append('parent_sha256')
            if p['key'].startswith('Z_'):
                c = C.get(key) or {}
                if o.get('n') != len(c.get('gen_ids') or []) or not (1 <= (o.get('n') or 0) <= MAX_COMPILE): bad.append('n_ne_generated_ids')
                if o.get('ids_sha256') != c.get('gen_ids_sha256'): bad.append('ids_sha256_ne_compile')
                if o.get('parent_mount_seal_sha256') != c.get('mount_seal_sha256'): bad.append('forge_mount_ne_compile_mount')
            elif p['key'].startswith('REF_'):
                g, w = key.rsplit('/', 1)[0], p['key'][4:]; zt = tbl.get(g + '/Z_' + w, {})
                if o.get('parent_mount_seal_sha256') != (C.get(g + '/Z_' + w) or {}).get('mount_seal_sha256'): bad.append('forge_mount_ne_compile_mount')
                want = man['groups'][g]['reference_record_ids'][w] + [man['failure_reference']['pad_id']] * ((zt.get('m') or 0) - len(man['groups'][g]['reference_record_ids'][w]))
                if o.get('n') != zt.get('m'): bad.append('n_ne_m_of_Z')
                if o.get('ids_sha256') != sha_s(json.dumps(want)): bad.append('ids_sha256_ne_reference_rule')
            else:
                if o.get('n') != p.get('n'): bad.append('n')
                if o.get('ids_sha256') != p.get('ids_sha256'): bad.append('ids_sha256')
        if not _hex(o.get('sha256')): bad.append('sha256')
        if not _hex(o.get('tensor_seal_sha256')): bad.append('tensor_seal')
        if bad: prob.append(('OBJECT_CONTRADICTS_PLAN%s' % bad, key))
    cnt = {}; recs = {}; byset = {}; prefixes = {}
    for c in cells:
        k = c.get('cell_id') if isinstance(c, dict) else None; cnt[k] = cnt.get(k, 0) + 1; recs[k] = c
    for k, n in cnt.items():
        if k not in man['cells']: prob.append(('UNKNOWN_CELL', k)); continue
        if n != 1: prob.append(('DUPLICATE_CELL(x%d)' % n, k))
        m = man['cells'][k]; r = recs[k]; bad = ['type:' + f for f in REC_STR if not isinstance(r.get(f), str)]
        bad += [f for f in ('unit', 'ns', 'perm', 'order', 'arm', 'slot', 'query_sha256') if r.get(f) != m.get(f)]
        missing = [s for s in m['sources'] if s not in O]
        if r.get('status') == 'NOT_RUN_NO_CARTRIDGE':
            if not missing or any(not P[s]['key'].startswith('Z_') or tbl.get(s, {}).get('valid') for s in missing): bad.append('not_run_without_reason')
            if r.get('raw') is not None: bad.append('not_run_has_raw')
            if bad: prob.append(('CONTRADICTORY_CELL%s' % bad, k))
            continue
        if r.get('status') != 'READ': bad.append('status')
        if missing: bad.append('read_with_missing_object')
        if not isinstance(r.get('raw'), str): bad.append('type:raw')
        tr = r.get('trace')
        if missing or not isinstance(tr, list) or len(tr) != len(m['sources']) or not all(isinstance(t, dict) for t in tr): bad.append('trace'); tr = None
        if tr is not None:
            for i, (t, key) in enumerate(zip(tr, m['sources'])):
                o = O.get(key) or {}
                if t.get('key') != key: bad.append('trace[%d].key' % i)
                if t.get('tensor_seal_sha256') != o.get('tensor_seal_sha256'): bad.append('trace[%d].tensor_seal' % i)
                if t.get('kind') != P.get(key, {}).get('kind'): bad.append('trace[%d].kind' % i)
                if not _hex(t.get('sha256')): bad.append('trace[%d].sha256' % i)
                elif m['copy'] is not None:
                    if t['sha256'] == o.get('sha256'): bad.append('trace[%d].copy_file_is_the_source_file' % i)
                    if t.get('shown') != m['shown']: bad.append('trace[%d].shown_label' % i)
                elif t['sha256'] != o.get('sha256'): bad.append('trace[%d].file_sha_ne_object' % i)
        mt = r.get('mount')
        if not isinstance(mt, dict): bad.append('mount')
        elif not missing:
            n_, rope = expected_geometry([dict(O[s], key=s) for s in m['sources']])
            if not isinstance(mt.get('mount_tokens'), int) or isinstance(mt.get('mount_tokens'), bool): bad.append('type:mount_tokens')
            elif mt['mount_tokens'] != n_: bad.append('mount_tokens_ne_geometry')
            if mt.get('rope') != rope: bad.append('rope_placement')
            if mt.get('parent_rows') != 0 and m['arm'].startswith('NRB'): bad.append('parent_rows_in_nrb_mount')
            for f in ('mount_seal_sha256', 'prefix_seal_sha256', 'lower_seal_sha256'):
                if not _hex(mt.get(f)): bad.append(f)
            if not bad:
                byset.setdefault(tuple(m['sources']), {}).setdefault(mt['mount_seal_sha256'], []).append(k)
                prefixes.setdefault(mt['prefix_seal_sha256'], []).append(k)
        if bad: prob.append(('CONTRADICTORY_CELL%s' % bad, k))
    def minority(d, code):
        if len(d) > 1:
            for _, ks in sorted(d.items(), key=lambda kv: (len(kv[1]), kv[0]))[:-1]:
                for kk in ks: prob.append((code, kk))
    for d in byset.values(): minority(d, 'MOUNT_SEAL_DIFFERS_FOR_SAME_TENSORS')
    minority(prefixes, 'PREFIX_SEAL_DIFFERS')
    for k in man['cells']:
        if k not in cnt: prob.append(('MISSING_CELL', k))
    want = failref_plan(man, tbl, {c.get('cell_id'): c for c in cells if isinstance(c, dict)}, None)
    got = sorted([(r.get('group'), r.get('world'), r.get('order'), r.get('status')) for r in refs], key=str)          # multiset (r2)
    exp = sorted([(x['group'], x['world'], x['order'], x['status']) for x in want], key=str)
    if got != exp: prob.append(('FAILREF_PLAN_MISMATCH', 'expected %s got %s' % (exp, got)))
    seen = {}
    for r in refs:
        key = '%s/REF_%s' % (r.get('group'), r.get('world')); seen[key] = seen.get(key, 0) + 1
    prob += [('DUPLICATE_FAILREF(x%d)' % n_, k_) for k_, n_ in seen.items() if n_ > 1]
    main_prefix = sorted(prefixes, key=lambda h: -len(prefixes[h]))[:1]
    for r in refs:
        key = '%s/REF_%s' % (r.get('group'), r.get('world')); bad = []
        if r.get('cell_id') != ref_cell_id(r.get('ns'), r.get('perm'), r.get('world')) or r.get('group') != '%s/%s' % (r.get('ns'), r.get('perm')): bad.append('cell_id')
        if r.get('status') != 'READ':
            if r.get('raw') is not None or key in O: bad.append('unread_reference_has_raw_or_object')
            if bad: prob.append(('CONTRADICTORY_FAILREF%s' % bad, key))
            continue
        o = O.get(key) or {}; mt = r.get('mount'); tr = r.get('trace'); U = man['units'].get('%s/%s' % (r.get('group'), r.get('order'))) or {}
        if not o: bad.append('object')
        if r.get('query_sha256') != U.get('query_sha256'): bad.append('query_sha256')
        if not isinstance(r.get('raw'), str): bad.append('raw')
        if not isinstance(tr, list) or len(tr) != 1 or not isinstance(tr[0], dict): bad.append('trace'); tr = None
        if tr is not None:
            t = tr[0]
            if t.get('key') != key or t.get('kind') != 'CHILD': bad.append('trace.key_kind')
            if t.get('tensor_seal_sha256') != o.get('tensor_seal_sha256'): bad.append('trace.tensor_seal')
            if t.get('sha256') != o.get('sha256'): bad.append('trace.file_sha_ne_object')
        if not isinstance(mt, dict): bad.append('mount')
        elif o:
            n_, rope = expected_geometry([dict(o, key=key)])
            if mt.get('mount_tokens') != n_: bad.append('mount_tokens_ne_geometry')
            if mt.get('rope') != rope: bad.append('rope_placement')
            for f in ('mount_seal_sha256', 'prefix_seal_sha256', 'lower_seal_sha256'):
                if not _hex(mt.get(f)): bad.append(f)
            if main_prefix and mt.get('prefix_seal_sha256') != main_prefix[0]: bad.append('prefix_seal_ne_panel')
            if mt.get('parent_rows') != 0: bad.append('parent_rows')
        if bad: prob.append(('CONTRADICTORY_FAILREF%s' % bad, key))
    if len([r for r in refs if r.get('status') == 'READ']) > man['failure_reference']['max_reads']: prob.append(('FAILREF_BUDGET', len(refs)))
    return sorted(set(prob), key=str)


# ===================================================================================================== evaluation (pure)
def _score(man, U, r, M4):
    p = M4.parse_904(r['raw'], U['outcome_order']) if r and r.get('status') == 'READ' and isinstance(r.get('raw'), str) else {'status': 'MISSING', 'answer': None, 'norm': None}
    return p, M4.answer_role(p, U['outcome_roles'])


def failref_plan(man, tbl, C, M4):
    """the pre-registered trigger (pure): which (group, world) get a source-explicit reference read, in which order."""
    out = []
    import types as _t
    parse = (M4.parse_904, M4.answer_role) if M4 is not None else (_parse_904_local, _answer_role_local)
    for ns, pm in VARIANTS:
        g = '%s/%s' % (ns, pm)
        for w in OUT_ROLE:
            z = tbl.get(g + '/Z_' + w) or {}
            if not z.get('valid') or z.get('queried') != 'PRESENT': continue
            fails = []
            for order in ORDERS:
                U = man['units']['%s/%s' % (g, order)]; r = C.get(cell_id(ns, pm, order, 'NRB_' + w))
                if not r or r.get('status') != 'READ' or not isinstance(r.get('raw'), str): continue
                if parse[1](parse[0](r['raw'], U['outcome_order']), U['outcome_roles']) != OUT_ROLE[w]: fails.append(order)
            if not fails: continue
            st = 'REFERENCE_GEOMETRY_UNAVAILABLE' if z['m'] < len(man['groups'][g]['reference_record_ids'][w]) else 'READ'
            out.append({'group': g, 'ns': ns, 'perm': pm, 'world': w, 'order': fails[0], 'm': z['m'], 'status': st, 'cell_id': ref_cell_id(ns, pm, w)})
    return out


def _parse_904_local(raw, outs):                                       # = 904 parse_904 (used only when M4 is not passed; tested equal)
    norm = (raw or '').strip()
    if norm.endswith('.'): norm = norm[:-1].strip()
    if norm in outs: return {'status': 'NAME', 'answer': norm, 'norm': norm}
    if norm == 'UNKNOWN': return {'status': 'UNKNOWN', 'answer': 'UNKNOWN', 'norm': norm}
    return {'status': 'INVALID', 'answer': None, 'norm': norm}


def _answer_role_local(parsed, outcome_roles):                         # = 904 answer_role
    if parsed['status'] in ('UNKNOWN', 'INVALID', 'MISSING'): return parsed['status']
    return outcome_roles[parsed['answer']]


def evaluate_906(man, compiles, cells, objects, refcells, technical_ok, M4, isolation_ok=True):
    probs = integrity_906(man, compiles, cells, objects, refcells); C = {c.get('cell_id'): c for c in cells if isinstance(c, dict)}
    tbl = compiler_table(man, compiles)
    bad_units = {man['cells'][k]['unit'] for _, k in probs if k in man['cells']}
    global_bad = [p for p in probs if p[1] not in man['cells']]
    units = []; scored = []
    for u, U in man['units'].items():
        g = U['group']; res = {}
        for arm in ARM_NAMES:
            k = cell_id(U['ns'], U['perm'], U['order'], arm); r = C.get(k); m = man['cells'][k]; p, role = _score(man, U, r, M4)
            res[arm] = {'status': (r or {}).get('status', 'MISSING'), 'raw': (r or {}).get('raw'), 'parsed': p, 'role': role,
                        'expected_role': m['expected_role'], 'ok': role == m['expected_role']}
            scored.append(dict(cell_id=k, **res[arm]))
        z = {w: tbl['%s/Z_%s' % (g, w)] for w in WORLDS}; s = U['slot']
        tech = technical_ok and u not in bad_units and not global_bad
        failed = [a for a in ('PARENT_POS', 'DIRECT_FACT') if not res[a]['ok']] + (['E_ONLY_NEG'] if res['E_ONLY_NEG']['role'] != 'UNKNOWN' else [])
        if res['NRB_SHAM']['status'] == 'READ' and res['NRB_SHAM']['raw'] != res['NRB_' + s]['raw']: failed.append('NRB_SHAM')
        if not tech: cat = 'TECHNICAL_UNDECIDABLE'
        elif not (z['H1']['valid'] and z['HG']['valid']):
            cat = 'CAPACITY_LIMIT' if 'CAPACITY_LIMIT' in (z['H1']['generation_status'], z['HG']['generation_status']) else 'COMPILER_INVALID'
        elif z['H1']['m'] != z['HG']['m']: cat = 'LENGTH_MISMATCH'
        elif not z['H2']['valid']: cat = 'CONTROL_UNAVAILABLE[NRB_H2_NEG]'
        elif failed: cat = 'CONTROLS_FAILED[%s]' % ','.join(failed)
        else:
            own = res['NRB_H1']['ok'] and res['NRB_HG']['ok']
            if own:
                if z['H1']['queried'] != 'PRESENT' or z['HG']['queried'] != 'PRESENT': cat = 'CORRECT_WITHOUT_EXPLICIT_RELATION'
                elif res['NRB_CROSS']['ok'] and res['NRB_H2_NEG']['role'] == 'UNKNOWN': cat = 'NRB_SUCCESS'
                else: cat = 'PHYSICAL_ATTRIBUTION_FAILURE'
            else:
                q = [z[w]['queried'] for w in ('H1', 'HG') if not res['NRB_' + w]['ok']]
                cat = 'COMPILER_OMISSION' if 'ABSENT' in q else ('COMPILER_HALLUCINATION' if 'WRONG' in q else 'BRIDGE_PRESENT_BUT_UNREADABLE')
        evaluable = tech and cat in EVALUABLE_CATEGORIES
        units.append({'unit': u, 'group': g, 'order': U['order'], 'slot': s, 'technical_complete': tech, 'evaluable': evaluable, 'category': cat,
                      'failed_controls': failed, 'own_raw_ok': res['NRB_H1']['ok'] and res['NRB_HG']['ok'],
                      'z': {w: {k_: z[w].get(k_) for k_ in ('generation_status', 'm', 'status', 'queried')} for w in WORLDS},
                      'inventory_complete_H1_HG': z['H1'].get('status') == 'COMPILER_COMPLETE' and z['HG'].get('status') == 'COMPILER_COMPLETE',
                      'raw': {a: res[a]['raw'] for a in ARM_NAMES}, 'roles': {a: res[a]['role'] for a in ARM_NAMES},
                      'expected': {a: res[a]['expected_role'] for a in ARM_NAMES}})
    tc = [x for x in units if x['technical_complete']]; ev = [x for x in units if x['evaluable']]
    cnt_ = {'planned': len(units), 'technical_complete': len(tc), 'evaluable': len(ev), 'raw_own_success': sum(x['own_raw_ok'] for x in tc)}
    for c_ in ALL_CATEGORIES: cnt_[c_] = sum(x['category'] == c_ for x in units)
    cnt_['CONTROLS_FAILED'] = sum(x['category'].startswith('CONTROLS_FAILED') for x in units)
    grp = {}
    for x in units: grp.setdefault(x['group'], []).append(x['category'] == 'NRB_SUCCESS')
    cnt_['groups'] = len(grp); cnt_['groups_success_both_orders'] = sum(all(v) and len(v) == 2 for v in grp.values())
    cnt_['compiler'] = {k: v['status'] for k, v in tbl.items()}
    n, e, u_ = cnt_['planned'], cnt_['evaluable'], cnt_['NRB_SUCCESS']
    if not isolation_ok: v = 'TEST906_INVALID'
    elif probs or not technical_ok: v = 'TECHNICAL_UNDECIDABLE'
    elif e == 0:
        v = 'UNDECIDABLE_NO_EVALUABLE_UNIT[%s]' % '; '.join('%s %d' % (c_, cnt_[c_]) for c_ in NON_EVALUABLE_SUMMARY if cnt_.get(c_))
    elif u_ >= 1: v = 'NRB_PHYSICAL_CAUSAL_READOUT[%d/%d; %d/%d]' % (u_, n, cnt_['groups_success_both_orders'], cnt_['groups'])
    else:
        v = 'NO_NRB_READOUT[%d/%d evaluable; %s]' % (e, n, '; '.join('%s %d' % (c_, cnt_[c_]) for c_ in EVALUABLE_CATEGORIES if c_ != 'NRB_SUCCESS'))
    cnt_['readout_panel_coverage'] = 'FULL' if u_ == n else ('PARTIAL' if u_ else 'NONE')
    iq = inventory_quality(tbl, units)
    refs = []
    for r in (refcells or []):
        if not isinstance(r, dict): continue
        if r.get('status') != 'READ': refs.append(dict(r, interpretation=r.get('status'))); continue
        U = man['units']['%s/%s' % (r['group'], r['order'])]; p, role = _score(man, U, r, M4)
        refs.append({'group': r['group'], 'world': r['world'], 'order': r['order'], 'raw': r.get('raw'), 'role': role,
                     'interpretation': ('REFERENCE_READABLE_Z_NOT' if role == OUT_ROLE[r['world']] else 'REFERENCE_ALSO_UNREADABLE') +
                                       ' (DIAGNOSTIC ONLY: REF is also forged conditioned on parent+E, so neither explicit-token sufficiency nor '
                                       'a Z key defect is isolated; never in the scientific denominator)'})
    return {'verdict': v, 'integrity_problems': ['%s:%s' % pk for pk in probs], 'units': units, 'scored_cells': scored, 'counts': cnt_,
            'compiler': tbl, 'failure_references': refs, 'inventory_quality': iq}


def inventory_quality(tbl, units):
    """the separate inventory axis (never the verdict): how completely and correctly the compiler wrote the observed episode."""
    st = {k: v['status'] for k, v in tbl.items()}; amb = sorted(k for k, v in tbl.items() if v.get('ambiguous_segments'))
    c = {s_: sum(1 for v in st.values() if v == s_) for s_ in ('COMPILER_COMPLETE', 'COMPILER_OMISSION', 'COMPILER_HALLUCINATION', 'CAPACITY_LIMIT', 'COMPILER_INVALID')}
    succ = [x for x in units if x['category'] == 'NRB_SUCCESS']
    out = {'per_z': st, 'counts': c, 'z_with_ambiguous_segments': amb, 'units_with_complete_H1_HG': sum(x['inventory_complete_H1_HG'] for x in units),
           'NRB_SUCCESS_with_complete_inventory': sum(x['inventory_complete_H1_HG'] for x in succ),
           'NRB_SUCCESS_with_incomplete_inventory': sum(not x['inventory_complete_H1_HG'] for x in succ)}
    out['label'] = ('COMPLETE_RELATION_AGNOSTIC_INVENTORY[12/12]' if c['COMPILER_COMPLETE'] == len(st) and not amb else
                    'INVENTORY_NOT_COMPLETE[complete %d/%d; omission %d; hallucination %d; capacity %d; invalid %d; ambiguous %d]' % (
                        c['COMPILER_COMPLETE'], len(st), c['COMPILER_OMISSION'], c['COMPILER_HALLUCINATION'], c['CAPACITY_LIMIT'], c['COMPILER_INVALID'], len(amb)))
    return out


EVALUABLE_CATEGORIES = ('NRB_SUCCESS', 'PHYSICAL_ATTRIBUTION_FAILURE', 'CORRECT_WITHOUT_EXPLICIT_RELATION', 'COMPILER_OMISSION',
                        'COMPILER_HALLUCINATION', 'BRIDGE_PRESENT_BUT_UNREADABLE')
NON_EVALUABLE_SUMMARY = ('TECHNICAL_UNDECIDABLE', 'CAPACITY_LIMIT', 'COMPILER_INVALID', 'LENGTH_MISMATCH', 'CONTROL_UNAVAILABLE[NRB_H2_NEG]', 'CONTROLS_FAILED')
ALL_CATEGORIES = EVALUABLE_CATEGORIES + NON_EVALUABLE_SUMMARY[:-1]


def generation_seal(compiles, cells, refcells):
    return jsha({'compiles': [(c.get('key'), c.get('gen_ids'), c.get('raw')) for c in compiles],
                 'cells': [(c.get('cell_id'), c.get('raw')) for c in cells], 'refs': [(r.get('cell_id'), r.get('raw')) for r in (refcells or [])]})


def verify_run_record(Rj, man_bytes, ev):
    out = []
    if Rj.get('status') == 'COMPLETE':
        for f in ('manifest_sha256', 'generation_sealed_sha256'):
            if not Rj.get(f): out.append(f.upper() + '_MISSING')
    if Rj.get('manifest_sha256') and Rj['manifest_sha256'] != sha_b(man_bytes): out.append('MANIFEST_SHA_MISMATCH')
    if Rj.get('generation_sealed_sha256') and Rj['generation_sealed_sha256'] != generation_seal(Rj.get('compiles') or [], Rj.get('cells') or [], Rj.get('reference_cells') or []):
        out.append('GENERATION_SEAL_MISMATCH')
    st = Rj.get('evaluation') or {}
    if st:
        a = {c['cell_id']: c for c in st.get('scored_cells', [])}; b = {c['cell_id']: c for c in ev['scored_cells']}
        out += ['STORED_CELL_RESULT_DIFFERS:' + k for k in sorted(set(a) | set(b)) if canon(a.get(k)) != canon(b.get(k))]
        ua = {x['unit']: x for x in st.get('units', [])}; ub = {x['unit']: x for x in ev['units']}
        out += ['STORED_UNIT_RESULT_DIFFERS:' + k for k in sorted(set(ua) | set(ub)) if canon(ua.get(k)) != canon(ub.get(k))]
        if st.get('verdict') != ev['verdict']: out.append('STORED_VERDICT_DIFFERS')
        if canon(st.get('counts')) != canon(ev['counts']): out.append('STORED_COUNTS_DIFFER')
        if canon(st.get('compiler')) != canon(ev['compiler']): out.append('STORED_COMPILER_TABLE_DIFFERS')
    return out


def report_lines(ev):
    c = ev['counts']
    iq = ev.get('inventory_quality') or {}
    L = ['TEST906 VERDICT: %s (readout panel coverage %s; native readout of the measured b relation only)' % (ev['verdict'], c['readout_panel_coverage']),
         'INVENTORY QUALITY (separate axis, not the verdict): %s | NRB_SUCCESS with complete H1/HG inventory %s, with incomplete %s' % (
             iq.get('label'), iq.get('NRB_SUCCESS_with_complete_inventory'), iq.get('NRB_SUCCESS_with_incomplete_inventory')),
         'planned %d | technical complete %d | evaluable %d | NRB_SUCCESS %d | groups with success in both orders %d/%d' % (
             c['planned'], c['technical_complete'], c['evaluable'], c['NRB_SUCCESS'], c['groups_success_both_orders'], c['groups']),
         'categories: ' + ', '.join('%s=%d' % (k, c[k]) for k in ALL_CATEGORIES + ('CONTROLS_FAILED',) if c.get(k)),
         'raw own H1+HG correct (technically complete units, controls ignored, NOT a scientific gain): %d' % c['raw_own_success']]
    if ev['integrity_problems']: L.append('INTEGRITY FAIL: ' + '; '.join(ev['integrity_problems'][:20]))
    L.append('COMPILER (Z per group / world): generation, m, inventory class, queried b relation')
    for k, z in ev['compiler'].items():
        L.append('    %-16s %-16s m=%-4s %-24s %-14s %r' % (k, z['generation_status'], z['m'], z['status'], z['queried'], (z.get('raw') or '')[:90]))
    L.append('%-13s %-4s %-4s %-4s %-36s | NRB H1 / HG / CROSS / SHAM / H2 | E_ONLY / DIRECT / PARENT' % ('unit', 'slot', 'tech', 'eval', 'category'))
    for x in ev['units']:
        r = x['raw']
        L.append('%-13s %-4s %-4s %-4s %-36s | %r / %r / %r / %r / %r | %r / %r / %r' % (
            x['unit'], x['slot'], 'ok' if x['technical_complete'] else 'X', x['evaluable'], x['category'], r['NRB_H1'], r['NRB_HG'], r['NRB_CROSS'],
            r['NRB_SHAM'], r['NRB_H2_NEG'], r['E_ONLY_NEG'], r['DIRECT_FACT'], r['PARENT_POS']))
    for f in ev['failure_references']: L.append('FAILURE REFERENCE %s %s %s: %s %r' % (f['group'], f['world'], f.get('order'), f['interpretation'], f.get('raw')))
    return L


# ===================================================================================================== run infrastructure (TEST906 r6, adapted)
X = types.SimpleNamespace(); M3 = M4 = m3 = None; RUN_ID = ROOT = LOG = OUT = EVENTS = None; R = None; DRIVE_DIR = None; T0 = time.perf_counter()


def config(argv):
    import argparse
    ap = argparse.ArgumentParser(add_help=False); colab = Path('/content').exists()
    d = {'out_root': '/content' if colab else '/tmp', 'src_dir': '', 'repo_dir': '/content/titan-cognitive-core-v3' if colab else '',
         'archive_dir': DEFAULT_ARCHIVE_903, 'zip': '', 'receipt': '', 'recompute': '', 'recompute_mode': 'verified', 'drive': 'required' if colab else 'auto'}
    for k, v in d.items(): ap.add_argument('--' + k.replace('_', '-'), default=os.environ.get('T906_' + k.upper(), v))
    a, _ = ap.parse_known_args(list(argv)); return {k: getattr(a, k) for k in d}


def fetch_source(cfg, work, pin):
    cands = [Path(cfg[k]) / pin['file'] for k in ('src_dir', 'repo_dir') if cfg.get(k)]
    for p in cands:
        if p.is_file() and blob_b(p.read_bytes()) == pin['git_blob']: b = p.read_bytes(); break
    else:
        rd = Path(cfg['repo_dir']) if cfg.get('repo_dir') and Path(cfg['repo_dir']).exists() else Path(work).parent / 'TEST906_repo_blobs'
        env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
        if not (rd / '.git').exists() and not (rd / 'HEAD').exists():
            subprocess.run(['git', 'clone', '-q', '--filter=blob:none', '--no-checkout', SRC_URL, str(rd)], check=True, capture_output=True, timeout=900, env=env)
        b = subprocess.run(['git', '-C', str(rd), 'cat-file', 'blob', pin['git_blob']], check=True, capture_output=True, timeout=300, env=env).stdout
    if blob_b(b) != pin['git_blob'] or sha_b(b) != pin['sha256']: raise Stop906('SOURCE_IDENTITY ' + pin['file'])
    p = Path(work) / pin['file']; p.write_bytes(b); return p


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def _norm_code(co):
    consts = tuple(_norm_code(c) if isinstance(c, types.CodeType) else c for c in co.co_consts)
    return co.replace(co_filename='', co_consts=consts, co_firstlineno=1, co_linetable=b'', co_exceptiontable=co.co_exceptiontable)


def code_digest(funcs):
    return sha_b(b''.join(marshal.dumps(_norm_code(f.__code__)) for f in funcs))


def _top_functions(b):
    import ast
    return [n.name for n in ast.parse(b).body if isinstance(n, ast.FunctionDef)]


REPO_906 = '/content/titan-cognitive-core-v3/906.py'


def _execution_mode(own_file, g):
    f = str(own_file or '')
    if g.get('__file__'): return 'SCRIPT_OR_%RUN'
    if 'ipykernel' in f or f.startswith('<ipython-input'): return 'NOTEBOOK_CELL'
    if f in ('<string>', '<stdin>', ''): return 'EXEC_STRING'
    return 'EXEC_COMPILED_WITH_FILENAME'


def git_provenance(path):
    """HEAD commit / committed blob of the executed file when it lives in a git checkout (diagnostic: published vs executed)."""
    try:
        d = str(Path(path).parent); env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
        head = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True, timeout=30, env=env).stdout.strip()
        tree = subprocess.run(['git', '-C', d, 'ls-tree', 'HEAD', '--', Path(path).name], capture_output=True, text=True, timeout=30, env=env).stdout.split()
        return {'head': head or None, 'committed_blob': tree[2] if len(tree) >= 3 else None}
    except Exception as e:
        return {'error': '%s: %s' % (type(e).__name__, e)}


def published_self(cfg, fallback_dir):
    """906.py as it is on GitHub main right now: git fetch of the public repository (no CDN cache), blob id re-hashed locally."""
    rd = Path(cfg['repo_dir']) if cfg.get('repo_dir') and Path(cfg['repo_dir']).exists() else Path(fallback_dir) / 'TEST906_repo_blobs'
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
    def git(*a, timeout=600): return subprocess.run(['git', '-C', str(rd)] + list(a), check=True, capture_output=True, timeout=timeout, env=env).stdout
    if not (rd / '.git').exists() and not (rd / 'HEAD').exists():
        subprocess.run(['git', 'clone', '-q', '--filter=blob:none', '--no-checkout', SRC_URL, str(rd)], check=True, capture_output=True, timeout=900, env=env)
    try: origin = git('remote', 'get-url', 'origin', timeout=30).decode().strip()
    except subprocess.CalledProcessError: origin = ''
    git('fetch', '-q', 'origin' if origin.rstrip('/').removesuffix('.git') == SRC_URL else SRC_URL, 'main')
    commit = git('rev-parse', 'FETCH_HEAD', timeout=30).decode().strip(); blob = git('rev-parse', 'FETCH_HEAD:' + SELF_FILE + '', timeout=30).decode().strip()
    b = git('cat-file', 'blob', blob)
    if blob_b(b) != blob: raise Stop906('PUBLISHED_SELF_BLOB_MISMATCH %s' % blob)
    return b, {'url': SRC_URL, 'ref': 'main', 'commit': commit, 'git_blob': blob, 'sha256': sha_b(b), 'bytes': len(b)}


def _cell_text(own_file):
    """the text IPython compiled for the running notebook cell (IPython registers every cell's text in linecache). Runs before the
    namespace clean-up, so it calls builtins through the builtins module only."""
    import linecache, builtins as B
    for cache in (linecache.cache, B.getattr(linecache, '_ipython_cache', None) or {}):
        e = cache.get(own_file)
        if B.isinstance(e, B.tuple) and B.len(e) >= 3 and B.isinstance(e[2], B.list) and e[2]: return ''.join(e[2])
    return None


def _canon_lines(text):
    """the ONLY normalisation before the notebook comparison: line endings, and blank lines at the very start / end of the cell."""
    lines = text.splitlines()
    while lines and not lines[0].strip(): lines.pop(0)
    while lines and not lines[-1].strip(): lines.pop()
    return lines


def _ipython_rewrites(ip, text, filename):
    """None when IPython compiled this text as written: no inherited `from __future__ import annotations` and no AST transformer
    that changes it (input transformers would already show up as a text difference)."""
    import ast, __future__
    flags = getattr(getattr(ip, 'compile', None), 'flags', 0) or 0
    fut = [f for f in ('annotations', 'barry_as_FLUFL') if flags & getattr(__future__, f).compiler_flag]
    if fut: return 'an earlier cell enabled `from __future__ import %s`; restart the session (Runtime > Restart session)' % ', '.join(fut)
    if getattr(ip, 'ast_transformers', None):
        try: same = ast.dump(ip.transform_ast(ast.parse(text, filename))) == ast.dump(ast.parse(text, filename))
        except Exception as e: return 'IPython AST transformer failed on 906: %s: %s' % (type(e).__name__, e)
        if not same: return 'IPython AST transformers %s change the code' % [type(t).__name__ for t in ip.ast_transformers]
    return None


def _clean_shadowed_builtins(g, text):
    """an earlier cell's `len = ...` would change what 906 calls: builtins that 906 uses but the notebook namespace redefines are
    removed from the namespace (a clean process has none); a functools.wraps wrapper of the builtin itself (IPython's open) stays.
    Returns (removed, removed_but_used_by_top_level_code): the second ones already acted while the cell defined its constants.
    Runs before the clean-up is complete, so it calls builtins through the builtins module only."""
    import builtins as B, symtable
    top = symtable.symtable(text, 'cell', 'exec'); defined = {s.get_name() for s in top.get_symbols() if s.is_assigned() or s.is_imported()}
    at_top = {s.get_name() for s in top.get_symbols() if s.is_referenced()}
    used, todo = B.set(), [top]
    while todo:
        t = todo.pop(); todo.extend(t.get_children())
        used |= {s.get_name() for s in t.get_symbols() if s.is_referenced() and (s.is_global() or t.get_type() == 'module')}
    gone = []
    for n in B.sorted(used - defined):
        if n.startswith('__') or not B.hasattr(B, n) or n not in g: continue
        v, real = g[n], B.getattr(B, n)
        if v is real or B.getattr(v, '__wrapped__', None) is real: continue
        del g[n]; gone.append(n)
    return gone, [n for n in gone if n in at_top]


def _notebook_identity(g, own_file, out, published):
    """copy-paste of 906.py from GitHub into ONE notebook cell: the text IPython compiled for this cell must equal 906.py on GitHub
    main (only line endings and blank lines at the very start / end are ignored), every top-level function must have been defined
    by this cell, IPython must not have rewritten the code. Any difference, a missing cell text or an unreachable GitHub: FAIL."""
    def fail(method, reason): return dict(out, file=None, method=method, reason=reason), None
    text = _cell_text(own_file)
    if text is None: return fail('NOTEBOOK_CELL_TEXT_UNAVAILABLE', 'IPython has no source text registered for %s' % own_file)
    gone, at_top = _clean_shadowed_builtins(g, text); out['namespace_builtins_removed'] = gone
    if at_top: return fail('NOTEBOOK_BUILTINS_SHADOWED', 'an earlier cell redefined %s, which this cell used while defining its constants; '
                           'restart the session (Runtime > Restart session) and paste 906 again' % at_top)
    names = _top_functions(text.encode('utf-8'))
    stale = [n for n in names if not (isinstance(g.get(n), types.FunctionType) and g[n].__code__.co_filename == own_file)]
    if not names or stale: return fail('NOTEBOOK_FUNCTIONS_NOT_FROM_THIS_CELL', 'top-level functions not defined by this cell: %s' % stale[:8])
    ip = g.get('get_ipython') or getattr(sys.modules.get('builtins'), 'get_ipython', None)
    if ip is None and 'IPython' in sys.modules: ip = getattr(sys.modules['IPython'], 'get_ipython', None)
    ip = ip() if callable(ip) else None
    if ip is None: return fail('NOTEBOOK_NO_IPYTHON', 'a notebook cell file name but no IPython shell')
    why = _ipython_rewrites(ip, text, own_file)
    if why: return fail('NOTEBOOK_CODE_REWRITTEN', why)
    try: ref, meta = published()
    except Exception as e: return fail('PUBLISHED_906_UNAVAILABLE', 'could not read 906.py from GitHub main (%s): %s: %s' % (SRC_URL, type(e).__name__, str(e)[:300]))
    a, b = _canon_lines(text), _canon_lines(ref.decode('utf-8', 'replace'))
    out.update(published=meta, cell_sha256=sha_s(text), cell_lines=len(a), github_lines=len(b))
    if a != b:
        i = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
        return fail('NOTEBOOK_CELL_DIFFERS_FROM_GITHUB', 'this cell is not 906.py of GitHub main (commit %s, blob %s): first difference at line %d: '
                    'cell %r | GitHub %r (cell %d lines, GitHub %d lines)' % (meta['commit'][:12], meta['git_blob'], i + 1,
                    a[i][:100] if i < len(a) else '<end of cell>', b[i][:100] if i < len(b) else '<end of file>', len(a), len(b)))
    X.PUBLISHED_BYTES = ref
    return dict(out, file='NOTEBOOK_CELL ' + str(own_file), sha256=meta['sha256'], git_blob=meta['git_blob'], bytes=meta['bytes'],
                functions_checked=len(names), method='NOTEBOOK_CELL_EQUALS_GITHUB_MAIN', normalisation='line endings; blank lines at start/end',
                git={'head': meta['commit'], 'committed_blob': meta['git_blob']}), text.encode('utf-8')


def executed_source_identity(g=None, cfg=None, published=None):
    """the 906 source that is actually executing, in one of two accepted ways (everything else fails closed):
    NOTEBOOK_CELL: the whole 906.py pasted into one cell; the compiled cell text must equal 906.py on GitHub main (_notebook_identity).
    SCRIPT: `!python 906.py` / an equivalent real `%run`: __name__ is __main__, argv[0], __file__ and the running function's filename
    identify the same non-symlink file, read once with a before/after stat check; two different existing 906 candidates fail.
    Candidate files are NEVER exec'd; exec strings and imports are refused."""
    g = g if g is not None else globals(); own = g.get('executed_source_identity')
    own_file = getattr(getattr(own, '__code__', None), 'co_filename', None); mode = _execution_mode(own_file, g)
    out = {'execution_mode': mode, 'code_filename': own_file, 'candidates': [], 'tried': []}
    def fail(method, reason): return dict(out, file=None, method=method, reason=reason), None
    if mode == 'NOTEBOOK_CELL':
        c = cfg or config([])
        return _notebook_identity(g, own_file, out, published or (lambda: published_self(c, ROOT if ROOT is not None else c['out_root'])))
    if mode != 'SCRIPT_OR_%RUN' or g.get('__name__') != '__main__' or not g.get('__file__'):
        return fail('NOT_FOUND', '906 must run from one notebook cell holding the whole GitHub 906.py, or as a saved file in its own __main__ '
                    'process; exec strings and imports are not accepted')
    paths = [Path(str(x)) for x in (own_file, g.get('__file__'), sys.argv[0] if sys.argv else None) if x]
    if len(paths) != 3:
        return fail('NOT_FOUND', 'code filename, __file__ and argv[0] are required')
    try:
        resolved = [p.resolve(strict=True) for p in paths]
    except OSError as e:
        return fail('NOT_FOUND', 'executed source is not a saved file: %s' % e)
    if len(set(resolved)) != 1 or any(p.is_symlink() for p in paths):
        return fail('AMBIGUOUS', 'code filename, __file__ and argv[0] must be the same non-symlink file: %s' % [str(p) for p in paths])
    p = paths[0]; st0 = p.stat()
    if not stat.S_ISREG(st0.st_mode): return fail('NOT_FOUND', 'executed source is not a regular file')
    b = p.read_bytes(); st1 = p.stat()
    if (st0.st_dev, st0.st_ino, st0.st_size, st0.st_mtime_ns) != (st1.st_dev, st1.st_ino, st1.st_size, st1.st_mtime_ns):
        return fail('SOURCE_CHANGED_DURING_READ', 'executed file changed while its bytes were read')
    names = _top_functions(b)
    if not names or not all(isinstance(g.get(n), types.FunctionType) for n in names):
        return fail('NOT_FOUND', 'running namespace does not contain every top-level function from the executed file')
    out['candidates'].append({'path': str(p), 'sha256': sha_b(b), 'result': 'DIRECT_FILE_MATCH'}); out['tried'].append(str(p))
    for c in (os.environ.get('T906_SELF'), REPO_906):
        if not c: continue
        q = Path(c)
        try:
            if q.resolve() == resolved[0] or not q.is_file(): continue
            qb = q.read_bytes(); row = {'path': c, 'sha256': sha_b(qb)}; out['candidates'].append(row); out['tried'].append(c)
            if qb != b:
                return fail('AMBIGUOUS', 'different 906.py candidates: %s' % [(str(p), sha_b(b)[:12]), (c, sha_b(qb)[:12])])
            row['result'] = 'SAME_BYTES'
        except OSError as e:
            return fail('SOURCE_READ_ERROR', '%s: %s' % (c, e))
    return dict(out, file=str(resolved[0]), sha256=sha_b(b), git_blob=blob_b(b), bytes=len(b), functions_checked=len(names),
                method='direct___main___file', code_digest=code_digest([g[n] for n in names]), git=git_provenance(p)), b


def _drive_mount_info(root, mountinfo_text=None):
    """Linux mount record for Colab Drive: a real mount at root, FUSE filesystem and a Drive source. A look-alike directory fails."""
    root = os.path.abspath(str(root))
    try: text = Path('/proc/self/mountinfo').read_text() if mountinfo_text is None else mountinfo_text
    except OSError as e: return False, {'error': '%s: %s' % (type(e).__name__, e)}
    for line in text.splitlines():
        left, sep, right = line.partition(' - ')
        if not sep: continue
        a = left.split(); b = right.split()
        if len(a) < 5 or len(b) < 2: continue
        mp = a[4].replace('\\040', ' ').replace('\\011', '\t').replace('\\012', '\n').replace('\\134', '\\')
        fstype, source = b[0], b[1]
        if mp == root:
            ok = (fstype == 'fuse' or fstype.startswith('fuse.')) and 'drive' in source.lower()
            return ok, {'mountpoint': mp, 'fstype': fstype, 'source': source, 'ok': ok}
    return False, {'error': 'NO_MOUNTINFO_RECORD', 'mountpoint': root}


def drive_presence(cfg):
    """no folder creation: require a real Drive/FUSE mount, MyDrive directory and writability; a local look-alike is not enough."""
    root = MYDRIVE.parent
    if cfg.get('drive') == 'off': return True, 'DRIVE_OFF_BY_FLAG'
    if not root.exists(): return cfg.get('drive') != 'required', 'NOT_MOUNTED: /content/drive does not exist'
    mounted, info = _drive_mount_info(root)
    if not mounted: return cfg.get('drive') != 'required', 'NOT_DRIVE_FUSE_MOUNT: %s' % info
    if not MYDRIVE.is_dir(): return cfg.get('drive') != 'required', 'MOUNT_INCOMPLETE: %s exists but %s is missing (remount with force_remount=True)' % (root, MYDRIVE)
    if not os.access(str(MYDRIVE), os.W_OK): return cfg.get('drive') != 'required', 'NOT_WRITABLE: %s' % MYDRIVE
    return True, 'MOUNTED_DRIVE_FUSE_WRITABLE: %s' % info


def ensure_drive_906(cfg, mode):
    """notebook kernel only (as 903's ensure_drive): mount Google Drive when /content/drive is not a real Drive/FUSE mount yet. Nothing
    is assumed: drive_presence, GATE_DRIVE_PRESENT and GATE_DRIVE (FUSE record, MyDrive, writability, write/read-back probe) judge it."""
    if cfg.get('drive') == 'off': return {'attempted': False, 'why': 'DRIVE_OFF'}
    ok, info = _drive_mount_info(MYDRIVE.parent)
    if ok and MYDRIVE.is_dir(): return {'attempted': False, 'why': 'ALREADY_MOUNTED', 'mount_info': info}
    if mode != 'NOTEBOOK_CELL': return {'attempted': False, 'why': 'NOT_A_NOTEBOOK_KERNEL', 'mount_info': info}
    try:
        from google.colab import drive as _gd
        _gd.mount(str(MYDRIVE.parent), force_remount=bool(ok)); res = {'attempted': True, 'force_remount': bool(ok), 'error': None}
    except Exception as e:
        res = {'attempted': True, 'force_remount': bool(ok), 'error': '%s: %s' % (type(e).__name__, str(e)[:500])}
    res['mount_info_after'] = _drive_mount_info(MYDRIVE.parent)[1]; return res


def init_run(cfg):
    global RUN_ID, ROOT, LOG, OUT, EVENTS, R
    RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'); ROOT = Path(cfg['out_root']) / ('TEST906_' + RUN_ID); ROOT.mkdir(parents=True, exist_ok=False)
    LOG = ROOT / 'TEST906.log'; OUT = ROOT / 'TEST906_results.json'; EVENTS = ROOT / 'TEST906_events.jsonl'
    for f in (LOG, EVENTS): f.write_text('')
    R = {'test': TAG, 'marker': MARKER, 'run_id': RUN_ID, 'status': 'STARTED', 'executed_by_author': False, 'geometry': GEOM,
         'top': {'first_failed_gate': None, 'technical_verdict': None, 'verdict': None, 'counts': None},
         'sources_pinned': {'903': SRC903, '904': SRC904, 'derived_from_905': SRC905}, 'run_905': RUN905, 'budget': BUDGET,
         'gates': {}, 'checks': [], 'technical_blockers': [], 'config': dict(cfg), 'compiles': [], 'cells': [], 'reference_cells': [], 'objects': {}}


def bind_903(m):
    m.RUN_ID = RUN_ID; m.ROOT = ROOT; m.LOG = LOG; m.OUT = OUT; m.EVENTS = EVENTS; m.CART_DIR = ROOT / 'work'; m.R = R; m.EVSEQ = [0]
    m.CRITICAL = tuple(m.CRITICAL) + CRITICAL_906


def log(*a): M3.log(*a)
def gate(*a, **k): M3.gate(*a, **k)


def drive_gate(cfg):
    global DRIVE_DIR
    mounted, mount_info = _drive_mount_info(MYDRIVE.parent)
    mounted = bool(mounted and MYDRIVE.is_dir())
    if cfg.get('drive') == 'required' and not mounted:
        gate('GATE_DRIVE', 'FAIL', 'Drive delivery required but a real Drive/FUSE /content/drive mount with MyDrive is not available: %s. '
             'Run `from google.colab import drive; drive.mount("/content/drive")` in a separate notebook cell, then start 906 again.' % mount_info)
    probe = None
    if mounted and cfg.get('drive') != 'off':
        DRIVE_DIR = str(MYDRIVE / ('TEST906_' + RUN_ID)); os.makedirs(DRIVE_DIR, exist_ok=False)
        data = os.urandom(4096); pp = Path(DRIVE_DIR) / '.TEST906_write_probe'
        try:
            with open(pp, 'wb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
            probe = sha_b(pp.read_bytes()) == sha_b(data); pp.unlink()
        except OSError as e: probe = False; X.PROBE_ERR = '%s: %s' % (type(e).__name__, e)
        if not probe: gate('GATE_DRIVE', 'FAIL', 'Drive write / read-back probe failed in %s (%s)' % (DRIVE_DIR, getattr(X, 'PROBE_ERR', 'sha mismatch')))
        M3.DRIVE_DIR = DRIVE_DIR; M3.save(force=True)
    gate('GATE_DRIVE', 'PASS', None, mode=cfg.get('drive'), mounted=mounted, mount_info=mount_info, dir=DRIVE_DIR, write_read_back_probe=probe)


def archive_gate(cfg):
    """903 ZIP (receipt -> ZIP -> SHA256SUMS -> members -> ledger -> results) via the pinned 904 functions + the H2 parent; 904
    results are not needed by 906. Needed members extracted read-only."""
    zp, rp, res, evp = M4.archive_paths(cfg)
    if zp is None or not Path(zp).is_file(): raise Stop906('ZIP_903_NOT_FOUND %s' % zp)
    if not Path(rp).is_file(): raise Stop906('RECEIPT_903_NOT_FOUND %s' % rp)
    try:
        A, sums, R3, events = M4.resolve_archive(zp, rp, M4.RUN903, res, evp); groups, empty = M4.map_cartridges(sums, R3, events)
    except M4.Stop904 as e: raise Stop906('ARCHIVE_903 ' + str(e))
    led = {(e.get('entry', e))['cid']: e.get('entry', e) for e in events if e.get('kind') == 'CARTRIDGE'}
    for (ns, pm), g in groups.items():
        tag = '%s_%s' % (ns.replace('-', ''), pm)
        for key, (suf, kind, hist) in NEEDED_EXTRA.items():
            x = led.get(tag + suf)
            if x is None: raise Stop906('LEDGER_MISSING ' + tag + suf)
            rel = x['file'][len(M4.RUN903['content_root']) + 1:]
            if sums.get(rel) != x['sha256']: raise Stop906('LEDGER_SHA_NE_SHA256SUMS ' + x['cid'])
            g[key] = {'key': key, 'cid': x['cid'], 'member': rel, 'sha256': x['sha256'], 'kind': kind, 'history': hist, 'generation': 1, 'ns': ns, 'perm': pm,
                      'n': x['n'], 'body_tokens': x['body_tokens'], 'pos0': None, 'ids_sha256': x['ids_sha256'], 'parents': None}
        if g['C1_H2'].get('parents') != [g['h1_H2']['sha256']]: raise Stop906('CHILD_PARENT_LINK ' + g['C1_H2']['cid'])
        if g['h1_H2']['ids_sha256'] != g['E_IND']['ids_sha256']: raise Stop906('H2_PARENT_NOT_A_TO_Q ' + g['h1_H2']['cid'])
    ro = ROOT / 'archive_ro'; root = M4.RUN903['zip_root'] + '/'
    with zipfile.ZipFile(zp) as z:
        for ent in [empty] + [v for g in groups.values() for v in g.values()]:
            mp = Path(ent['member'])
            if mp.is_absolute() or '..' in mp.parts: raise Stop906('UNSAFE_ARCHIVE_MEMBER ' + ent['member'])
            dst = ro / ent['member']; dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists(): dst.write_bytes(z.read(root + ent['member'])); os.chmod(dst, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
            if sha_file(dst) != ent['sha256']: raise Stop906('EXTRACTED_SHA ' + ent['member'])
            ent['file'] = str(dst)
    X.GROUPS, X.EMPTY, X.A3 = groups, empty, A
    R['archive'] = {'903': A}
    gate('GATE_ARCHIVE_906', 'PASS', None, archive_903=A,
         objects={'%s/%s/%s' % (ns, pm, k): {kk: v[kk] for kk in ('cid', 'member', 'sha256', 'kind', 'history')} for (ns, pm), g in groups.items() for k, v in g.items()})


def archive_tensors_gate():
    m = M3; torch = m.torch; G = {}
    for ent in [X.EMPTY] + [v for g in X.GROUPS.values() for v in g.values()]:
        cp = torch.load(ent['file'], map_location='cpu', weights_only=True); ent['tensor_seal'] = m.seal_cp(cp); ent['book_id'] = cp['book_id']
        if ent['kind'] == 'PREFIX': ok = int(cp['n']) == int(cp['p']) == GEOM['P'] and cp['body_tokens'] == 0; X.CP_EMPTY = cp; ent['n'] = int(cp['n'])
        elif ent['kind'] == 'CHILD': ok = int(cp['p']) == 0 and int(cp['pos0']) == ent['pos0'] == 49 and int(cp['n']) == ent['n'] == 19
        else: ok = int(cp['p']) == 30 and int(cp['n']) == ent['n'] == 49 and int(cp['body_tokens']) == 19
        G[ent.get('cid', 'EMPTY')] = ok
        if not ok: gate('GATE_ARCHIVE_TENSORS_906', 'FAIL', 'geometry ' + ent.get('cid', 'EMPTY'), checks=G)
        del cp
    gate('GATE_ARCHIVE_TENSORS_906', 'PASS', None, checks=G)


def save_obj(obj, key, where, meta):
    m = M3; where.mkdir(parents=True, exist_ok=True); path = where / ('T906_%s.pt' % key.replace('/', '_')); tmp = Path(str(path) + '.tmp')
    if path.exists(): raise Stop906('APPEND_ONLY ' + str(path))
    m.torch.save(obj, tmp); tmp.replace(path); os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    ent = dict(meta, key=key.split('/')[-1], file=str(path), sha256=sha_file(path), bytes=path.stat().st_size)
    m.CART_INDEX.append(ent); m.ev('OBJECT', entry={k: v for k, v in ent.items() if k not in ('tensor_seal',)}); return ent


def _guard(op, dt=None):
    """the pinned 898 guard (ABORT_903 limits, post-operation, strict '>') called unchanged; its abort becomes the critical gate
    GATE_RUNTIME_LIMITS_906 (technical, never scientific) so the first failed gate, the verdict and the traceback name it."""
    try: m3.guard(op, dt)
    except m3.StopT896 as e: gate('GATE_RUNTIME_LIMITS_906', 'FAIL', str(e), op=op, dt=dt)


def _gen_and_diag(mem, q, cand_ids):
    """greedy answer (guard 'query' on the generation time) then the first-token diagnostic forward (its own guard 'query' on the
    diagnostic time: wall / GPU peak / RAM / cartridge bytes are checked again after the last forward)."""
    real = m3.tok; tap = M4.DecodeTap(real); m3.tok = tap
    try: raw, dt = m3.gen_with(mem, q, MAX_NEW_READ)
    finally: m3.tok = real
    _guard('query', dt); t_ = time.perf_counter(); lg = m3.first_logits(mem, q); top = int(lg.argmax()); logits = {str(i): float(lg[i]) for i in cand_ids}; del lg
    dd = time.perf_counter() - t_; _guard('query', dd)
    return raw, dt, {'argmax': top, 'logits': logits, 'decode_calls': tap.calls, 'diag_s': round(dd, 3)}


def _seals(mem):
    P = 30; return (m3.jsha(m3.full_kv_seal(mem)), m3.jsha([(m3.kv_digest(k[:, :, :P, :]), m3.kv_digest(v[:, :, :P, :])) for k, v in mem]),
                    m3.jsha(m3.full_kv_seal(mem[:4])))


def read_mount(ents, q, cand_ids):
    """A / natives / source: fresh mount_sealed(ents) (archived prefix + sealed cartridges) -> locked answer()."""
    t_ = time.perf_counter(); mem = m3.mount_sealed(ents); ta = time.perf_counter() - t_; _guard('append', ta)
    s0 = m3.full_kv_seal(mem); n = int(mem[0][0].shape[-2])
    raw, dt, dg = _gen_and_diag(mem, q, cand_ids)
    if m3.full_kv_seal(mem) != s0: raise m3.StopT896('MOUNT_CHANGED_BY_READ')
    ms, ps, ls = _seals(mem); del mem; m3.release()
    return raw, {'mount_tokens': n, 'mount_seal_sha256': ms, 'prefix_seal_sha256': ps, 'lower_seal_sha256': ls, 'query_s': round(dt, 3), 'mount_s': round(ta, 3),
                 'read_s': round(time.perf_counter() - t_, 3)}, dg


def func_source(f):
    """source of a 906 function: from the verified executed bytes (exec() in a kernel has no source file), else inspect."""
    import ast, inspect, textwrap
    b = getattr(X, 'SELF_BYTES', None)
    if b:
        src = b.decode('utf-8')
        for n in ast.parse(src).body:
            if isinstance(n, ast.FunctionDef) and n.name == f.__name__: return ast.get_source_segment(src, n)
    return textwrap.dedent(inspect.getsource(f))


def read_path_isolation():
    """the compile / forge / read functions see only cartridges, the query or compile text, the tokenizer tap and the engine: no
    manifest, expected answer, outcome role, evaluator or world label (checked on their symbol tables and parameter lists)."""
    import symtable, inspect
    allowed = {'m3', 'M4', 'X', 'MAX_NEW_READ', 'COMPILE_PROBE', 'time', 'int', 'round', 'float', 'str', 'list', 'len', '_gen_and_diag', '_seals',
               '_guard', 'gate', 'dict'}
    want = {'read_mount': ['ents', 'q', 'cand_ids'], '_gen_and_diag': ['mem', 'q', 'cand_ids'], '_seals': ['mem'], 'compile_z': ['ents', 'q'],
            'forge_z': ['ents', 'ids', 'book_id'], '_guard': ['op', 'dt']}
    out = {}
    for f in (read_mount, _gen_and_diag, _seals, compile_z, forge_z, _guard):
        t = symtable.symtable(func_source(f), f.__name__, 'exec').get_children()[0]
        g = sorted({x.get_name() for x in t.get_symbols() if x.is_global()})
        out[f.__name__] = {'globals': g, 'not_allowed': sorted(set(g) - allowed), 'params_ok': list(inspect.signature(f).parameters) == want[f.__name__]}
    out['ok'] = all(not v['not_allowed'] and v['params_ok'] for v in out.values() if isinstance(v, dict)); return out


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
        zp = ROOT.parent / ('TEST906_SONUC_%s.zip' % RUN_ID)
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
    if requested and DRIVE_DIR is None:
        really_mounted = _drive_mount_info(MYDRIVE.parent)[0] and MYDRIVE.is_dir()
        D['error'] = ('DRIVE_NOT_ATTEMPTED_RUN_STOPPED_BEFORE_GATE_DRIVE' if really_mounted and 'GATE_DRIVE' not in R['gates']
                      else 'DRIVE_REQUIRED_BUT_NOT_MOUNTED')
    elif requested and local_ok:
        ok, err = drive_copy(Path(AG['zip']), DRIVE_DIR); D['zip_copied_read_back'] = ok
        if not ok: D['error'] = 'ZIP: %s' % err
    if not local_ok: st = 'FAIL_LOCAL_ARTIFACTS'
    elif not requested: st = 'LOCAL_ONLY_DRIVE_NOT_REQUESTED'
    elif D['error'] and D['error'].startswith('DRIVE_REQUIRED_BUT_NOT_MOUNTED'): st = 'DRIVE_NOT_MOUNTED'
    elif D['error'] and D['error'].startswith('DRIVE_NOT_ATTEMPTED'): st = 'DRIVE_NOT_ATTEMPTED_RUN_STOPPED_EARLY'
    elif D['error']: st = 'DRIVE_ZIP_NOT_DELIVERED'
    else: st = 'PASS'                                                    # final, valid only together with the byte read-back below
    receipt = {'test': TAG, 'run_id': RUN_ID, 'status': R.get('status'), 'top': R.get('top'), 'artifacts': AG, 'drive': D, 'artifact_status': st,
               'results_sha256': sha_file(OUT) if AG.get('report_written_read_back') else None}
    rp = ROOT.parent / ('TEST906_SONUC_%s_RECEIPT.json' % RUN_ID); body = json.dumps(receipt, indent=1, default=str); rp.write_text(body)
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
    print('TEST906 ARTIFACTS', json.dumps({'artifact_status': receipt['artifact_status'], 'drive_receipt': X.RECEIPT_DRIVE_STATE, 'zip': AG.get('zip')}, default=str), flush=True)
    return receipt


def exit_code(receipt):
    if R.get('status') != 'COMPLETE' or R.get('technical_verdict') != 'PASS': return 1
    return 0 if receipt.get('artifact_status') in ('PASS', 'LOCAL_ONLY_DRIVE_NOT_REQUESTED') else 2


def status_line(rc, receipt):
    t = R.get('top') or {}; a = receipt.get('artifact_status'); d = receipt.get('drive') or {}
    drive = 'PASS' if a == 'PASS' else ('NOT_REQUESTED' if a == 'LOCAL_ONLY_DRIVE_NOT_REQUESTED' else 'FAILED[%s: %s]' % (a, d.get('error')))
    head = {0: 'TAMAMLANDI', 2: 'TAMAMLANDI_TESLIM_HATASI'}.get(rc, 'TEKNIK_HATA')
    return 'TEST906 DURUM: %s | EXIT=%d | TECHNICAL=%s | VERDICT=%s | READS=%s | DRIVE=%s | FIRST_GATE=%s | RESULTS=%s' % (
        head, rc, t.get('technical_verdict'), t.get('verdict'), getattr(X, 'NREAD', None), drive, t.get('first_failed_gate'), OUT)


def kernel_cleanup(g):
    """Colab kernel exec(): an earlier TEST903/904 exec leaves its engine module (holding a 72B model) in globals such as `m`;
    drop only those references so the memory can be freed before this run loads its own model."""
    gone = [n for n, v in list(g.items()) if isinstance(v, types.ModuleType) and getattr(v, 'TAG', None) in ('TEST903', 'TEST904', 'TEST905', 'TEST906')
            and n not in ('M3', 'M4', 'm3')]
    for n in gone: del g[n]
    for a in ('last_type', 'last_value', 'last_traceback', 'last_exc'):  # an earlier aborted cell's traceback keeps its frames alive
        if hasattr(sys, a): setattr(sys, a, None)
    import gc; gc.collect()
    if 'torch' in sys.modules:
        try: sys.modules['torch'].cuda.empty_cache()
        except Exception: pass
    return gone


def vram_gate():
    torch = M3.torch; free, total = torch.cuda.mem_get_info(); fg = round(free / 2**30, 2)
    ok = fg >= 70.0
    gate('GATE_VRAM_FREE', 'PASS' if ok else 'FAIL', None if ok else 'only %.2f GiB free of %.2f before loading the 72B model: an earlier model '
         'is still in memory; restart the Colab session (Runtime > Restart session) and run 906 again' % (fg, total / 2**30), free_gib=fg, total_gib=round(total / 2**30, 2))




def tokenizer_gate():
    """pinned tokenizer, before the model: archived token-id hashes reproduce every role record; the 903 design constants equal
    906's; direct-fact / reference records have E's length; compile suffix ids; the compile text names no public name, no option
    and not the question; special / stop / pad ids; every public answer is producible within MAX_NEW_READ."""
    m = M3; tk = m.transformers.AutoTokenizer.from_pretrained(m.MODEL_ID, revision=m.MODEL_REVISION, trust_remote_code=False)
    bad = []; X.TC_IDS = {}; tc_sha = {}; ref_ids = {}
    from huggingface_hub import hf_hub_download                           # RoPE parameters before the model: pinned config.json
    X.ROPE_PRE = rope_config(types.SimpleNamespace(**json.loads(Path(hf_hub_download(m.MODEL_ID, 'config.json', revision=m.MODEL_REVISION)).read_text())))
    if not (X.ROPE_PRE['theta'] and X.ROPE_PRE['default']): bad.append('ROPE_CONFIG %s' % X.ROPE_PRE)
    if dict(m.HIST) != HIST or tuple(m.E_FACT) != E_FACT or dict(M4.HIST_FACT) != HIST: bad.append('DESIGN_CONSTANTS_NE_903_904')
    for (ns, pm), g in X.GROUPS.items():
        V = M4.names_of(ns, pm, m.NAMES, m.PERMS); gk = '%s/%s' % (ns, pm)
        for key, ent in g.items():
            a, o = E_FACT if key in ('C1_H1', 'C1_HG', 'C1_H2', 'E_IND') else HIST[ent['history']]
            if sha_b(json.dumps(list(m.obs_ids(V[a], V[o], tk))).encode()) != ent['ids_sha256']: bad.append(ent['cid'])
        for w, key in TC_OF.items():
            ids = list(m.obs_ids(V['b'], V[OUT_ROLE[w]], tk)); X.TC_IDS[ns, pm, key] = ids; tc_sha['%s/%s' % (gk, key)] = sha_b(json.dumps(ids).encode())
            ref_ids['%s/%s' % (gk, w)] = ids
            if len(ids) != GEOM['n_E']: bad.append('%s/%s:len%d' % (gk, key, len(ids)))
    leak = compile_text_leaks(COMPILE_TEXT, [v for N in m.NAMES.values() for v in N.values()], M4.QUERY_TPL_904)
    if leak: bad.append('COMPILE_TEXT_LEAK %s' % leak)
    if sha_s(COMPILE_TEXT) != COMPILE_TEXT_SHA256: bad.append('COMPILE_TEXT_SHA256')
    suffix = m.SUFFIX_HEAD + COMPILE_TEXT + m.SUFFIX_TAIL; sids = list(tk(suffix, add_special_tokens=False).input_ids)
    stop = [tk.eos_token_id, tk.convert_tokens_to_ids('<|im_end|>')]
    special = sorted(set(int(i) for i in (getattr(tk, 'all_special_ids', None) or [])) |
                     {int(i) for i, t in (getattr(tk, 'added_tokens_decoder', None) or {}).items() if getattr(t, 'special', False)})
    nl = list(tk('\n', add_special_tokens=False).input_ids)
    if len(nl) != 1 or nl[0] in special: bad.append('PAD_ID %s' % nl)
    if any(s_ is None for s_ in stop) or not set(stop) <= set(special): bad.append('STOP_IDS_NOT_IN_SPECIAL_IDS %s' % stop)   # fail closed
    answers = {}; first = {}
    for N in m.NAMES.values():
        for w in [N[k] for k in ('o1', 'o2', 'o3')] + ['UNKNOWN']:
            ids = list(tk(w, add_special_tokens=False).input_ids)
            answers[w] = {'ids': ids, 'decode_roundtrip': tk.decode(ids) == w, 'fits_max_new': len(ids) + 1 <= MAX_NEW_READ}; first[w] = ids[0]
    ok = not bad and all(v['decode_roundtrip'] and v['fits_max_new'] for v in answers.values())
    X.TOKINFO = {'answers': answers, 'first_token': first, 'stop_ids': stop, 'stop_id': stop[1], 'tc_ids_sha256': tc_sha, 'ref_record_ids': ref_ids,
                 'special_ids': special, 'pad_id': nl[0] if len(nl) == 1 else None, 'compile_suffix_ids_sha256': sha_s(json.dumps(sids)),
                 'compile_suffix_tokens': len(sids)}
    gate('GATE_TOKENIZER_906', 'PASS' if ok else 'FAIL', None if ok else {'problems': bad}, answers=answers, tc_ids_sha256=tc_sha,
         compile_suffix_tokens=len(sids), special_ids=len(special), pad_id=X.TOKINFO['pad_id'])
    del tk


def disk_gate():
    """measured, not guessed: free disk >= the model bytes still missing from the HF cache (index total_size minus shards present)
    + 8 GiB for the run's artefacts, pip and temporaries."""
    m = M3; from huggingface_hub import hf_hub_download
    ip = Path(hf_hub_download(m.MODEL_ID, 'model.safetensors.index.json', revision=m.MODEL_REVISION)); idx = json.loads(ip.read_text())
    total = int(idx['metadata']['total_size']); shards = sorted(set(idx['weight_map'].values()))
    present = sum((ip.parent / f).stat().st_size for f in shards if (ip.parent / f).exists())
    need = max(0, total - present) + 8 * 2**30; free = shutil.disk_usage(str(ip.parent)).free; ok = free >= need
    gate('GATE_DISK_906', 'PASS' if ok else 'FAIL', None if ok else 'free disk %.1f GiB < needed %.1f GiB (model %.1f GiB, cached %.1f GiB)' % (
        free / 2**30, need / 2**30, total / 2**30, present / 2**30), free_gib=round(free / 2**30, 1), need_gib=round(need / 2**30, 1),
        model_gib=round(total / 2**30, 1), cached_gib=round(present / 2**30, 1), shards=len(shards))


def manifest_gate():
    plan = plan_objects(X.GROUPS, X.EMPTY, X.TOKINFO['tc_ids_sha256'])
    plan['EMPTY'] = {'key': 'EMPTY', 'origin': 'ARCHIVE_903', 'member': X.EMPTY['member'], 'sha256': X.EMPTY['sha256'], 'kind': 'PREFIX', 'n': X.EMPTY['n'],
                     'tensor_seal_sha256': jsha(X.EMPTY['tensor_seal']), 'pos0': 0}
    man = build_manifest(X.GROUPS, plan, X.TOKINFO, M3.NAMES, M3.PERMS, X.A3, M4)
    ok = (man['n_cells'] == len(set(man['cells'])) == BUDGET['main_reads'] and len(man['compiles']) == BUDGET['compiles'] and
          all(len({c['query_sha256'] for c in man['cells'].values() if c['unit'] == u}) == 1 for u in man['units']) and
          sorted(collections_count(c['slot'] for c in man['units'].values()).values()) == [4, 4])
    b = json.dumps(man, indent=1, sort_keys=True, default=list).encode(); p = ROOT / 'TEST906_manifest.json'; p.write_bytes(b)
    X.MAN_SHA = sha_b(b); X.MAN_PATH = p; X.PLAN = [(k, c['unit'], c['arm']) for k, c in man['cells'].items()]
    X.UNITQ = {u: {'query': U['query'], 'outs': U['outcome_order'], 'ns': U['ns'], 'perm': U['perm'], 'order': U['order'], 'slot': U['slot']}
               for u, U in man['units'].items()}
    X.CPLAN = [(k, c['group'], c['world'], c['mount_sources']) for k, c in man['compiles'].items()]
    gate('GATE_MANIFEST_906', 'PASS' if ok else 'FAIL', None if ok else 'manifest shape', sha256=X.MAN_SHA, n_cells=man['n_cells'],
         compiles=len(man['compiles']), written_before_model=True)
    del man                                                               # the run path never holds expected answers


def collections_count(it):
    out = {}
    for x in it: out[x] = out.get(x, 0) + 1
    return out


def _ver(name):
    import importlib.metadata
    try: return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError: return None


def gpu_preflight():
    """FIRST physical gate, torch only (no Drive, no model, no package install): exactly one NVIDIA A100-SXM4-80GB, cc 8.0, >= 79
    GiB, >= 70 GiB free, pinned Python / torch. Failure -> GPU_REQUIRED_A100_TECHNICAL_STOP; nothing is written to Drive."""
    import platform
    pins = M3.PINS; rec = {'python': platform.python_version(), 'torch_installed': _ver('torch'), 'required': {k: pins[k] for k in ('python_minor', 'torch', 'cuda')}}
    ok = '.'.join(rec['python'].split('.')[:2]) == pins['python_minor'] and rec['torch_installed'] == pins['torch']
    if ok:
        import torch
        rec.update(torch=torch.__version__, cuda=torch.version.cuda, cuda_available=bool(torch.cuda.is_available()), device_count=int(torch.cuda.device_count()))
        if rec['cuda_available'] and rec['device_count'] >= 1:
            pr = torch.cuda.get_device_properties(0); free, total = torch.cuda.mem_get_info(0)
            rec.update(gpu=torch.cuda.get_device_name(0), compute_capability=[pr.major, pr.minor], total_gib=round(pr.total_memory / 2**30, 2), free_gib=round(free / 2**30, 2))
        ok = (rec['cuda'] == pins['cuda'] and rec['cuda_available'] and rec['device_count'] == 1 and rec.get('gpu') == M3.GPU_NAME_REQ and
              tuple(rec.get('compute_capability', ())) == tuple(M3.GPU_CC_REQ) and rec.get('total_gib', 0) >= 79 and rec.get('free_gib', 0) >= 70.0)
    rec['disk_free_gib'] = round(shutil.disk_usage(str(ROOT)).free / 2**30, 1)
    gate('GATE_GPU_PREFLIGHT_906', 'PASS' if ok else 'FAIL', None if ok else
         'GPU_REQUIRED_A100_TECHNICAL_STOP: need exactly one %s (cc %s, >= 79 GiB, >= 70 GiB free) with Python %s / torch %s / CUDA %s; found %s. '
         'Colab: Runtime > Change runtime type > A100 GPU (restart the session if a model is still in memory). Drive was not touched.' % (
             M3.GPU_NAME_REQ, M3.GPU_CC_REQ, pins['python_minor'], pins['torch'], pins['cuda'],
             {k: rec.get(k) for k in ('python', 'torch_installed', 'cuda', 'cuda_available', 'device_count', 'gpu', 'compute_capability', 'total_gib', 'free_gib')}), **rec)


def engine_gate():
    m = M3; torch = m.torch; G = {}
    m.T_EXP = time.perf_counter(); m.ABORT = dict(m.ABORT_903); m.MAX_NEW = MAX_NEW_READ; m.METRICS = {'forge_s': [], 'append_s': [], 'query_s': []}
    m.CART_INDEX = [v for g in X.GROUPS.values() for v in g.values()]; m.CP_EMPTY = X.CP_EMPTY
    G['P_is_30'] = m.P == 30 == GEOM['P']; G['prefix_sha256_equal_902_903'] = m.sha_bytes(m.PREFIX.encode()) == m.REF902['prefix_sha256']
    G['model_arch'] = (m.NL, m.H, m.QH, m.KVH, m.HD) == (80, 8192, 64, 8, 128) == (GEOM['layers'], 8192, 64, GEOM['kv_heads'], GEOM['head_dim'])
    G['rope'] = rope_config(m.model.config); G['rope_theta_found'] = G['rope']['theta'] is not None; G['rope_default_unscaled'] = G['rope']['default']
    G['rope_equal_pinned_config_json'] = G['rope']['theta'] == X.ROPE_PRE['theta']
    t_ = time.perf_counter()
    with m.MountOff(): cpe, _ = m.forge_native([], 'T906_EMPTY_CHECK')
    _guard('forge', time.perf_counter() - t_)
    G['fresh_empty_prefix_bitwise_equal_archive'] = (torch.equal(cpe['h'], X.CP_EMPTY['h']) and all(torch.equal(a, c) and torch.equal(b, d) for (a, b), (c, d) in zip(cpe['lower'], X.CP_EMPTY['lower'])))
    del cpe; m.release()
    sch = {'%s/%s/%s' % (ns, pm, k): m.child_schema(m.load_record(g[k]))['ok'] for (ns, pm), g in X.GROUPS.items() for k in ('C1_H1', 'C1_HG', 'C1_H2')}
    G['child_schema_all'] = all(sch.values())
    k = torch.randn((1, 8, 19, 128), device=m.DEV).to(m.DTYPE); p = torch.arange(68, 87, device=m.DEV)
    G['rephase_identity_bitwise_at_source_eq_target'] = torch.equal(m.rephase(k, p, p), k)
    G['hooks_clean'] = m.hooks_clean(m.hook_inventory()); iso = read_path_isolation(); G['read_path_isolated'] = iso['ok']; X.ISOLATION_OK = iso['ok']
    G['answer_suffix_is_709'] = (m.SUFFIX_HEAD + 'Q' + m.SUFFIX_TAIL) == '\nQUESTION:\nQ\n\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n'
    G['guard_is_pinned_898'] = getattr(m.guard, '__name__', None) == 'guard' and getattr(getattr(m.guard, '__code__', None), 'co_varnames', ())[:2] == ('op', 'dt')
    G['abort_limits_are_903'] = m.ABORT == dict(m.ABORT_903)
    G['no_duplicate_top_level_definitions'] = not duplicate_top_level((X.SELF_BYTES or b'').decode('utf-8')) if X.SELF_BYTES else True
    fail = [kk for kk, v in G.items() if isinstance(v, bool) and v is not True]
    gate('GATE_ENGINE_906', 'PASS' if not fail else 'FAIL', None if not fail else ('TEST906_INVALID: read / compile path isolation broken %s' % iso
         if not iso['ok'] else 'failed: %s' % fail), checks=G, child_schema=sch, isolation=iso)
    X.W0 = {'sentinel': m.sentinel(), 'integrity': m.integrity_digest(m.base_params, m.Q4MODS, m.BUFS)}; X.ROPE_THETA = G['rope']['theta']


# ---------------------------------------------------------------------------------------------------- COMPILE + FORGE (parent open)
def compile_z(ents, q):
    """one greedy 709 answer() on a fresh mount_sealed(ents) with question q, budget COMPILE_PROBE; the decode tap returns the exact
    generated ids (the stop token excluded); the mount must be unchanged; the generation cache is discarded by answer()."""
    t_ = time.perf_counter(); mem = m3.mount_sealed(ents); _guard('append', time.perf_counter() - t_); s0 = m3.full_kv_seal(mem); n = int(mem[0][0].shape[-2])
    real = m3.tok; tap = M4.DecodeTap(real); m3.tok = tap
    try: raw, dt = m3.gen_with(mem, q, COMPILE_PROBE)
    finally: m3.tok = real
    if m3.full_kv_seal(mem) != s0: raise m3.StopT896('MOUNT_CHANGED_BY_COMPILE')
    _guard('query', dt); ms = m3.jsha(s0); del mem; m3.release()
    if len(tap.calls) != 1: raise m3.StopT896('COMPILE_GENERATED_IDS_UNAVAILABLE calls=%d' % len(tap.calls))
    return list(tap.calls[0]), raw, {'mount_tokens': n, 'mount_seal_sha256': ms, 'compile_s': round(dt, 3), 'total_s': round(time.perf_counter() - t_, 3)}


def forge_z(ents, ids, book_id):
    """903 forge_conditioned_903 of ids on a FRESH mount_sealed(ents) (no compile suffix): H3 + L0-L3 rows of ids only."""
    t_ = time.perf_counter(); mem = m3.mount_sealed(ents); _guard('append', time.perf_counter() - t_); s0 = m3.full_kv_seal(mem); n = int(mem[0][0].shape[-2])
    t_ = time.perf_counter(); cp, geo = m3.forge_conditioned_903(mem, list(ids), book_id); df = time.perf_counter() - t_
    if m3.full_kv_seal(mem) != s0: raise m3.StopT896('PARENT_CHANGED_BY_FORGE ' + book_id)
    ms = m3.jsha(s0); del mem; m3.release(); _guard('forge', df); geo = dict(geo, forge_s=round(df, 3)); return cp, geo, ms, n


def compile_all():
    for key, gk, w, srcs in X.CPLAN:
        ns, pm = gk.split('/'); g = X.GROUPS[ns, pm]; ents = [g[s.split('/')[-1]] for s in srcs]
        ids, raw, info = compile_z(ents, COMPILE_TEXT); st, why = compile_status(ids, X.TOKINFO['special_ids'])
        rec = {'key': key, 'group': gk, 'world': w, 'mount_sources': list(srcs), 'mount_seal_sha256': info['mount_seal_sha256'], 'mount_tokens': info['mount_tokens'],
               'compile_text_sha256': sha_s(COMPILE_TEXT), 'suffix_ids_sha256': X.TOKINFO['compile_suffix_ids_sha256'], 'gen_ids': ids,
               'gen_ids_sha256': sha_s(json.dumps(ids)), 'n_generated': len(ids), 'raw': raw, 'status': st, 'reason': why,
               'compile_s': info['compile_s'], 't_s': round(time.perf_counter() - T0, 1)}
        R['compiles'].append(rec); M3.ev('COMPILE', key=key, status=st, n=len(ids), raw=raw)
        log('COMPILE %-16s %-16s n=%-3d %r' % (key, st, len(ids), raw[:200])); M3.save(False)
    G = {'records_12': len(R['compiles']) == BUDGET['compiles'], 'parent_E_mount_68': all(c['mount_tokens'] == 68 for c in R['compiles']),
         'ids_within_probe': all(c['n_generated'] <= COMPILE_PROBE for c in R['compiles'])}
    ok = all(G.values()); st = collections_count(c['status'] for c in R['compiles'])
    gate('GATE_COMPILE_906', 'PASS' if ok else 'FAIL', None if ok else [k for k, v in G.items() if not v], statuses=st, **G)


def _save_child(cp, key, ns, pm, meta):
    m = M3; raw = cp['h'].numel() * cp['h'].element_size() + sum(k.numel() * k.element_size() + v.numel() * v.element_size() for k, v in cp['lower'])
    ent = save_obj(cp, key, ROOT / 'objects' / ns / pm, dict(meta, kind='CHILD', n=cp['n'], body_tokens=cp['body_tokens'], pos0=cp['pos0'],
                                                             tensor_seal=m.seal_cp(cp), raw_bytes=raw))
    ent['tensor_seal_sha256'] = jsha(ent['tensor_seal'])
    if ent['bytes'] > TOL906['file_bytes_max_factor'] * raw + TOL906['file_bytes_slack']: raise Stop906('OBJECT_FILE_BYTES ' + key)
    return ent


def write_z(key, rec, g):
    ns, pm = rec['group'].split('/'); w = rec['world']; ents = [g['h1_' + w], g['C1_' + w]]
    cp, geo, ms, n0 = forge_z(ents, rec['gen_ids'], 'T906_%s_%s' % (RUN_ID, key.replace('/', '_')))
    sch = M3.child_schema(cp); m_ = len(rec['gen_ids'])
    if not sch['ok'] or n0 != 68 or cp['pos0'] != GEOM['z_source_pos0'] or cp['n'] != m_ or ms != rec['mount_seal_sha256']:
        raise Stop906('Z_FORGE %s schema=%s pos0=%s n=%s mount_equal=%s' % (key, sch['ok'], cp['pos0'], cp['n'], ms == rec['mount_seal_sha256']))
    ent = _save_child(cp, key, ns, pm, {'history': w, 'parent_sha256': [e['sha256'] for e in ents], 'parent_mount_seal_sha256': ms,
                                        'ids_sha256': rec['gen_ids_sha256'], 'geometry': geo, 'cid': 'T906_' + key.replace('/', '_'), 'compile_key': key})
    del cp; return ent


def write_transport_child(ns, pm, key, parent):
    """direct-fact control record (b->r or b->g) written as E itself after the a->q parent (TEST906 method)."""
    m = M3; cp, geo, ms, n0 = forge_z([parent], X.TC_IDS[ns, pm, key], 'T906_%s_%s_%s_%s' % (RUN_ID, ns, pm, key))
    sch = m.child_schema(cp)
    if not sch['ok'] or cp['pos0'] != 49 or cp['n'] != 19: raise Stop906('TC_SCHEMA %s/%s/%s' % (ns, pm, key))
    ent = _save_child(cp, '%s/%s/%s' % (ns, pm, key), ns, pm, {'history': 'H2', 'parent_sha256': parent['sha256'], 'geometry': geo,
                      'ids_sha256': sha_b(json.dumps(list(X.TC_IDS[ns, pm, key])).encode()), 'cid': 'T906_%s_%s_%s' % (ns, pm, key)})
    del cp; return ent


def write_all():
    objs = {}
    for (ns, pm), g in X.GROUPS.items():
        for k, v in g.items(): objs['%s/%s/%s' % (ns, pm, k)] = {**{kk: v[kk] for kk in ('cid', 'file', 'sha256', 'kind', 'history', 'n', 'body_tokens', 'pos0')},
                                                                'key': k, 'tensor_seal': v['tensor_seal'], 'tensor_seal_sha256': jsha(v['tensor_seal'])}
        for w, key in TC_OF.items(): objs['%s/%s/%s' % (ns, pm, key)] = write_transport_child(ns, pm, key, g['h1_H2'])
    for rec in R['compiles']:
        if rec['status'] == 'VALID': objs[rec['key']] = write_z(rec['key'], rec, X.GROUPS[tuple(rec['group'].split('/'))])
    X.OBJS = objs
    R['objects'] = {k: {kk: vv for kk, vv in v.items() if kk not in ('tensor_seal', 'geometry')} for k, v in objs.items()}
    z = [o for k, o in objs.items() if k.split('/')[-1].startswith('Z_')]
    gate('GATE_WRITE_906', 'PASS', None, created_z=len(z), created_tc=8, z_raw_bytes=sum(o['raw_bytes'] for o in z))
    ropes = [rope_reference(k, o) for k, o in objs.items() if k.split('/')[-1].startswith('Z_')]
    R['rope_reference'] = ropes; bad = [r['object'] for r in ropes if not r['ok']]
    gate('GATE_ROPE_906', 'PASS' if not bad else 'FAIL', None if not bad else 'child mount 68 -> 30 failed: %s' % bad, results=ropes)


def rope_reference(key, ent):
    """the real read mount of a Z cartridge vs an independent float64 RoPE: rows = 30 + m; prefix rows bit-equal to the empty
    mount; L0-L3 V rows bit-equal to the stored V; L0-L3 K rows = stored K moved 68 -> 30 once (cos >= tol); twice is diagnostic."""
    import numpy as np
    m = M3; torch = m.torch; cp = m.load_record(ent); n = int(cp['n']); src = list(range(cp['pos0'], cp['pos0'] + n)); dst = list(range(30, 30 + n))
    t_ = time.perf_counter(); mem = m.mount_sealed([ent]); _guard('append', time.perf_counter() - t_)
    t_ = time.perf_counter(); emp = m.mount_sealed([]); _guard('append', time.perf_counter() - t_); worst = 1.0; dbl = -1.0; v_ok = True
    rows_ok = int(mem[0][0].shape[-2]) == 30 + n
    prefix_ok = all(torch.equal(a[:, :, :30, :], c) and torch.equal(b[:, :, :30, :], d) for (a, b), (c, d) in zip(mem, emp))
    for li in range(GEOM['cut'] + 1):
        ks, vs = cp['lower'][li]; km = mem[li][0][:, :, 30:30 + n, :].float().cpu().numpy(); vm = mem[li][1][:, :, 30:30 + n, :]
        ref = rope_move_np(ks.float().numpy().astype(np.float64), src, dst, X.ROPE_THETA, m.HD)
        twice = rope_move_np(ref, src, dst, X.ROPE_THETA, m.HD)
        worst = min(worst, cos_np(km, ref)); dbl = max(dbl, cos_np(km, twice)); v_ok = v_ok and torch.equal(vm.cpu(), vs.to(vm.dtype))
    del mem, emp, cp; m.release()
    ok = rows_ok and prefix_ok and v_ok and worst >= TOL906['rope_reference_cos_min']
    return {'object': key, 'rows_30_plus_m': rows_ok, 'prefix_bitwise': prefix_ok, 'v_unchanged_bitwise': v_ok, 'min_cos_single_vs_reference': worst,
            'max_cos_vs_double_DIAGNOSTIC': dbl, 'ok': ok}


def work_copies():
    """CROSS / SHAM files: the same tensors under another file name and book id (tensor seal unchanged, file SHA different)."""
    m = M3; torch = m.torch; X.SLOT = {}; G = {}
    for k, u, arm in X.PLAN:
        U = X.UNITQ[u]; srcs, shown, copy = arm_sources(U['slot'])[arm]
        if copy is None: continue
        key = '%s/%s/%s' % (U['ns'], U['perm'], srcs[0]); src = X.OBJS.get(key)
        if src is None: continue                                            # no cartridge -> NOT_RUN read (recorded as such)
        d = ROOT / 'work' / U['ns'] / U['perm'] / U['order']; d.mkdir(parents=True, exist_ok=True)
        dst = d / ('T906_%s_%s_%s_%s_%s.pt' % (U['ns'].replace('-', ''), U['perm'], U['order'], arm, shown))
        obj = torch.load(src['file'], map_location='cpu', weights_only=True); obj['book_id'] = 'T906_SHOWN_%s_%s_%s_%s' % (U['ns'], U['perm'], U['order'], shown)
        seal = jsha(m.seal_cp(obj)); torch.save(obj, dst); del obj
        e = dict(src, file=str(dst), sha256=sha_file(dst), shown=shown); G[dst.name] = seal == src['tensor_seal_sha256'] and e['sha256'] != src['sha256']
        os.chmod(dst, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH); m.CART_INDEX.append(e); X.SLOT[u, arm] = [e]
    ok = all(G.values()); gate('GATE_WORK_COPIES_906', 'PASS' if ok else 'FAIL', None if ok else [k for k, v in G.items() if not v], checks=G)


# ---------------------------------------------------------------------------------------------------- READ (parent never present)
def run_reads():
    nread = 0
    for k, u, arm in X.PLAN:
        U = X.UNITQ[u]; ns, pm = U['ns'], U['perm']; srcs, shown, copy = arm_sources(U['slot'])[arm]; keys = ['%s/%s/%s' % (ns, pm, x) for x in srcs]
        base = {'cell_id': k, 'unit': u, 'ns': ns, 'perm': pm, 'order': U['order'], 'arm': arm, 'slot': U['slot'], 'query_sha256': sha_s(U['query'])}
        if any(x not in X.OBJS for x in keys):
            R['cells'].append(dict(base, status='NOT_RUN_NO_CARTRIDGE', raw=None, missing=[x for x in keys if x not in X.OBJS]))
            log('READ %-40s %-12s -> NOT_RUN (no cartridge)' % (k, arm)); continue
        ents = X.SLOT[u, arm] if copy else [X.OBJS[x] for x in keys]
        cand = sorted({X.TOKINFO['first_token'][w] for w in U['outs'] + ['UNKNOWN']})
        raw, info, dg = read_mount(ents, U['query'], cand); nread += 1
        _, info['rope'] = expected_geometry([dict(X.OBJS[x], key=x) for x in keys])
        info['parent_rows'] = sum(int(e['body_tokens']) for e in ents if e['kind'] == 'NATIVE' and e['key'].startswith('h1_'))
        calls = dg.pop('decode_calls'); dg['generated_ids'] = calls[0] if len(calls) == 1 else None
        dg['status'], dg['generated_first_id'] = M4.diag_validity(dg['argmax'], calls, set(X.TOKINFO['stop_ids']))
        rec = dict(base, status='READ', trace=[{'key': x, 'sha256': e['sha256'], 'tensor_seal_sha256': e['tensor_seal_sha256'], 'kind': e['kind'],
                                                'file': e['file'], 'shown': e.get('shown')} for x, e in zip(keys, ents)],
                   mount=info, raw=raw, diag=dg, t_s=round(time.perf_counter() - T0, 1))
        R['cells'].append(rec); M3.ev('READOUT', cell_id=k, raw=raw, mount=info['mount_seal_sha256'])
        log('READ %-40s %-12s -> %r' % (k, arm, raw[:60])); M3.save(False)
    X.NREAD = nread
    ok = len(R['cells']) == BUDGET['main_reads'] and len({c['cell_id'] for c in R['cells']}) == BUDGET['main_reads']
    gate('GATE_READS_906', 'PASS' if ok else 'FAIL', None if ok else 'planned cells %d' % len(R['cells']), reads=nread, records=len(R['cells']))


def run_failure_references():
    """after the 64 main reads: the pre-registered trigger decides (manifest read back here, after the panel); each reference is
    forged exactly as its Z and read through read_mount like any other cartridge. Diagnostic only."""
    R['main_generation_sealed_sha256'] = generation_seal(R['compiles'], R['cells'], [])
    b = X.MAN_PATH.read_bytes()
    if sha_b(b) != X.MAN_SHA: raise Stop906('MANIFEST_CHANGED')
    man = json.loads(b); tbl = compiler_table(man, R['compiles']); plan = failref_plan(man, tbl, {c['cell_id']: c for c in R['cells']}, M4)
    pad = man['failure_reference']['pad_id']; nref = 0
    for p in plan:
        rec = dict(p)
        if p['status'] == 'READ':
            g = X.GROUPS[p['ns'], p['perm']]; w = p['world']; ids = man['groups'][p['group']]['reference_record_ids'][w] + [pad] * (p['m'] - len(man['groups'][p['group']]['reference_record_ids'][w]))
            key = '%s/REF_%s' % (p['group'], w); ents = [g['h1_' + w], g['C1_' + w]]
            cp, geo, ms, n0 = forge_z(ents, ids, 'T906_%s_%s' % (RUN_ID, key.replace('/', '_')))
            if not M3.child_schema(cp)['ok'] or cp['pos0'] != 68 or cp['n'] != p['m'] or n0 != 68: raise Stop906('REF_FORGE ' + key)
            ent = _save_child(cp, key, p['ns'], p['perm'], {'history': w, 'parent_sha256': [e['sha256'] for e in ents], 'parent_mount_seal_sha256': ms,
                                                            'ids_sha256': sha_s(json.dumps(ids)), 'geometry': geo, 'cid': 'T906_' + key.replace('/', '_')})
            del cp; X.OBJS[key] = ent; R['objects'][key] = {kk: vv for kk, vv in ent.items() if kk not in ('tensor_seal', 'geometry')}
            U = man['units']['%s/%s' % (p['group'], p['order'])]; cand = sorted({X.TOKINFO['first_token'][x] for x in U['outcome_order'] + ['UNKNOWN']})
            rr = rope_reference(key, ent); R.setdefault('rope_reference', []).append(rr)
            if not rr['ok']: gate('GATE_FAILREF_906', 'FAIL', 'reference child mount 68 -> 30 failed: %s' % rr)
            raw, info, dg = read_mount([ent], U['query'], cand); nref += 1; dg.pop('decode_calls', None)
            _, info['rope'] = expected_geometry([dict(ent, key=key)]); info['parent_rows'] = 0
            rec.update(raw=raw, mount=info, diag=dg, unit='%s/%s' % (p['group'], p['order']), query_sha256=sha_s(U['query']),
                       trace=[{'key': key, 'sha256': ent['sha256'], 'tensor_seal_sha256': ent['tensor_seal_sha256'], 'kind': 'CHILD'}])
            log('FAILREF %-30s -> %r' % (key, raw[:60]))
        R['reference_cells'].append(rec)
    del man
    X.NREF = nref; ok = nref <= BUDGET['failure_reference_reads_max']
    gate('GATE_FAILREF_906', 'PASS' if ok else 'FAIL', None if ok else 'too many references %d' % nref, planned=len(plan), reads=nref)


def end_gate():
    mm = M3; torch = mm.torch
    created = [o for k, o in X.OBJS.items() if k.split('/')[-1].startswith(('Z_', 'REF_'))]
    G = {'sentinel_equal': mm.sentinel() == X.W0['sentinel'], 'integrity_equal': mm.integrity_digest(mm.base_params, mm.Q4MODS, mm.BUFS)['sha256'] == X.W0['integrity']['sha256'],
         'hooks_clean': mm.hooks_clean(mm.hook_inventory()), 'files_unchanged': all(sha_file(e['file']) == e['sha256'] for e in mm.CART_INDEX),
         'cells_64': len(R['cells']) == BUDGET['main_reads'], 'greedy_sequences_within_84': len(R['compiles']) + X.NREAD + X.NREF <= BUDGET['greedy_sequences_max'],
         'bridge_raw_bytes_within_40MiB': sum(o['raw_bytes'] for o in created) <= TOL906['created_bridge_raw_bytes_max']}
    _guard('end')                                                      # final wall / GPU peak / CPU RAM / cartridge bytes, BEFORE any PASS
    peak = torch.cuda.max_memory_allocated() / 2**30; G['gpu_peak_within_abort'] = peak <= mm.ABORT['gpu_peak_gib']
    ok = all(G.values()); gate('GATE_END_906', 'PASS' if ok else 'FAIL', None if ok else [k for k, v in G.items() if not v], gpu_peak_gib=round(peak, 2),
                               abort_limits=dict(mm.ABORT), **G)


def write_verdict():
    b = X.MAN_PATH.read_bytes()
    if sha_b(b) != X.MAN_SHA: raise Stop906('MANIFEST_CHANGED')
    man = json.loads(b); gates_ok = all(g['status'] != 'FAIL' for g in R['gates'].values()) and not R['technical_blockers']; R['manifest_sha256'] = X.MAN_SHA
    R['generation_sealed_sha256'] = generation_seal(R['compiles'], R['cells'], R['reference_cells'])
    ev = evaluate_906(man, R['compiles'], R['cells'], R['objects'], R['reference_cells'], gates_ok, M4, isolation_ok=getattr(X, 'ISOLATION_OK', False))
    probs = verify_run_record(dict(R, status='COMPLETE', evaluation=None), b, ev)
    tv = 'PASS' if gates_ok and not ev['integrity_problems'] and not probs else 'TECHNICAL_UNDECIDABLE'
    if tv != 'PASS' and ev['verdict'] != 'TEST906_INVALID': ev['verdict'] = 'TECHNICAL_UNDECIDABLE'
    R.update(evaluation=ev, technical_verdict=tv, run_record_problems=probs)
    R['top'].update(technical_verdict=tv, verdict=ev['verdict'], counts=ev['counts'], integrity_problems=ev['integrity_problems'][:50] + probs)
    L = report_lines(ev) + (['RUN RECORD: ' + '; '.join(probs)] if probs else [])
    (ROOT / 'TEST906_verdict.txt').write_text('\n'.join(L) + '\nRecompute: python 906.py --recompute TEST906_results.json\n')
    for l in L: log(l)
    return tv


def gpu_main(cfg):
    global M3, M4, m3
    work = ROOT / 'sources'; work.mkdir()
    X.PUBLISHED_BYTES = None; ident, b = executed_source_identity(cfg=cfg); R['executed_source'] = ident; X.SELF_BYTES = b
    if b is not None: (work / 'TEST906_executed_906.py').write_bytes(b)
    if b is not None and X.PUBLISHED_BYTES is not None: (work / 'TEST906_github_main_906.py').write_bytes(X.PUBLISHED_BYTES)
    p3 = fetch_source(cfg, work, SRC903); p4 = fetch_source(cfg, work, SRC904)
    M4 = load_module(p4, 'akbas_test904_engine'); M3 = m3 = M4.load_903(p3); bind_903(M3)
    if M4.TAG != 'TEST904' or M4.R is not None or M4.RUN_ID is not None: raise Stop906('904_MODULE_STATE')
    M3.log('=' * 112); M3.log(MARKER, '| run', RUN_ID)
    gate('GATE_SOURCES_906', 'PASS', None, src903=SRC903, src904=SRC904, derived_from_905=SRC905, modules_main_not_run=M3.R is R and M4.R is None)
    how = ('Copy the WHOLE 906.py again from GitHub main (button "Copy raw file") into ONE EMPTY cell and run only that cell'
           if ident.get('execution_mode') == 'NOTEBOOK_CELL' else 'Save the exact 906.py as %s and start it in its own process: `!python %s`' % (REPO_906, REPO_906))
    gate('GATE_EXECUTED_SOURCE', 'PASS' if b is not None else 'FAIL', None if b is not None else
         '%s [%s; mode %s; checked %s]. %s' % (ident.get('method'), ident.get('reason'), ident.get('execution_mode'),
                                               [(x['path'], x.get('result')) for x in ident.get('candidates', [])], how), identity=ident)
    R['kernel_cleanup'] = kernel_cleanup(globals())
    R['status'] = 'GPU_PREFLIGHT'; gpu_preflight()                      # A100 first; Drive is not touched before this PASS
    M3.boot_runtime(); M3.env_gate(); vram_gate()
    X.MOUNT = ensure_drive_906(cfg, ident.get('execution_mode')); ok_d, why_d = drive_presence(cfg)
    gate('GATE_DRIVE_PRESENT', 'PASS' if ok_d else 'FAIL', None if ok_d else
         'Drive delivery is required but %s (automatic mount: %s). In a notebook cell: `from google.colab import drive; drive.mount("/content/drive", '
         'force_remount=True)`, then start 906 again' % (why_d, X.MOUNT), state=why_d, mode=cfg.get('drive'), mount=X.MOUNT)
    drive_gate(cfg)                                                       # write / fsync / read-back probe BEFORE the archive and the model
    try: archive_gate(cfg)
    except Stop906 as e: gate('GATE_ARCHIVE_906', 'FAIL', str(e))
    M3.PINNED_CALLS = []
    SRC = M3.obtain_sources(cfg, work); R['sources'] = {n: {'sha256': sha_b(x), 'git_blob': blob_b(x)} for n, x in SRC.items()}
    M3.source_extract_gate(SRC); archive_tensors_gate()
    M3.tokenizer_pre_model_gate(); tokenizer_gate(); disk_gate(); manifest_gate()   # manifest (all reads, compiles, rules) BEFORE the model
    M3.model_gate(); engine_gate()
    R['status'] = 'COMPILE'; compile_all()
    R['status'] = 'WRITE'; write_all(); work_copies()
    R['status'] = 'READS'; run_reads(); run_failure_references(); end_gate(); tv = write_verdict()
    R['status'] = 'COMPLETE' if tv == 'PASS' else 'TECHNICAL_INVALID'


def main(argv=None):
    cfg = config(sys.argv[1:] if argv is None else argv)
    if cfg.get('recompute'): return recompute(cfg['recompute'], cfg)
    init_run(cfg)
    try: gpu_main(cfg)
    except BaseException as e:
        tb = traceback.format_exc(); stopped = isinstance(e, Stop906) or type(e).__name__ in ('StopT896', 'Stop904')
        R.update(status='TECHNICAL_ABORT' if stopped else ('INTERRUPTED' if isinstance(e, KeyboardInterrupt) else 'ERROR'),
                 technical_verdict='TECHNICAL_UNDECIDABLE', error='%s: %s' % (type(e).__name__, str(e)[:3000]), traceback=tb)
        inv = 'TEST906_INVALID' in str(e)
        R['top'].update(technical_verdict='TECHNICAL_UNDECIDABLE', verdict='TEST906_INVALID' if inv else 'TECHNICAL_UNDECIDABLE')
        if R['top']['first_failed_gate'] is None: R['top']['first_failed_gate'] = 'ABORT: ' + str(e)[:200]
        (ROOT / 'TEST906_traceback.txt').write_text(tb); print('TEST906_TECHNICAL_STOP', R['error'][:1500], flush=True)
        with LOG.open('a') as f: f.write('TEST906_TECHNICAL_STOP ' + R['error'][:1500] + '\n')
        if isinstance(e, KeyboardInterrupt): finalize_artifacts(cfg); raise
    receipt = finalize_artifacts(cfg); rc = exit_code(receipt); line = status_line(rc, receipt); print(line, flush=True)
    with LOG.open('a') as f: f.write(line + '\n')
    return rc


def authenticate_record(Rj, run_dir, man_bytes):
    """record authentication for --recompute (verified mode): evidence-set identity, NOT a re-execution of the GPU run. Requires a
    COMPLETE / technical PASS record, every REQUIRED_PASS_GATES entry PASS in the record AND in the event log (no FAIL event),
    isolation ok, 12 compiles / 64 cells, the manifest SHA, the executed-source file of the run with its SHA, the source pins,
    SHA256SUMS.txt of the run directory re-verified file by file, every object file present with its SHA, and the receipt
    (next to the run directory) naming this results file by SHA. Returns (authenticated, reasons)."""
    why = []; d = Path(run_dir); gates = Rj.get('gates') or {}
    if Rj.get('status') != 'COMPLETE' or Rj.get('technical_verdict') != 'PASS': why.append('RECORD_NOT_COMPLETE_PASS')
    if d.name != 'TEST906_%s' % Rj.get('run_id'): why.append('RUN_DIR_NE_RUN_ID')
    if (Rj.get('sources_pinned') or {}).get('903') != SRC903 or (Rj.get('sources_pinned') or {}).get('904') != SRC904: why.append('SOURCE_PINS')
    ev = []
    try: ev = [json.loads(l) for l in (d / 'TEST906_events.jsonl').read_text().splitlines() if l.strip()]
    except Exception as e: why.append('EVENTS_UNREADABLE %s' % type(e).__name__)
    gev = {}
    for e in ev:
        if e.get('kind') == 'GATE': gev.setdefault(e.get('name'), []).append(e.get('status'))
    for g_ in REQUIRED_PASS_GATES:
        st = (gates.get(g_) or {}).get('status')
        if st != 'PASS': why.append('GATE_%s:%s' % ('MISSING' if st is None else 'NOT_PASS', g_))
        evs = gev.get(g_, [])
        if 'PASS' not in evs or 'FAIL' in evs or any(x not in ('PASS', 'DIAGNOSTIC') for x in evs): why.append('GATE_EVENT_CHAIN:%s:%s' % (g_, evs))
    fails = sorted(k for k, v in gates.items() if (v or {}).get('status') == 'FAIL')
    if fails: why.append('FAILED_GATES %s' % fails)
    if not (((gates.get('GATE_ENGINE_906') or {}).get('data') or {}).get('isolation') or {}).get('ok'): why.append('ISOLATION_NOT_OK')
    if len(Rj.get('compiles') or []) != BUDGET['compiles'] or len(Rj.get('cells') or []) != BUDGET['main_reads']: why.append('RECORD_COUNTS')
    if Rj.get('manifest_sha256') != sha_b(man_bytes): why.append('MANIFEST_SHA')
    es = Rj.get('executed_source') or {}; ef = d / 'sources' / 'TEST906_executed_906.py'
    if not (ef.is_file() and _hex(es.get('sha256'))): why.append('EXECUTED_SOURCE_FILE_OR_SHA_MISSING')
    elif es.get('method') == 'direct___main___file' and sha_file(ef) != es['sha256']: why.append('EXECUTED_SOURCE_SHA')
    sums = d / 'SHA256SUMS.txt'
    if not sums.is_file(): why.append('SHA256SUMS_MISSING')
    else:
        rows = [l.split('  ', 1) for l in sums.read_text().splitlines() if l.strip()]
        for h, rel in rows:
            f = d / rel
            if not f.is_file() or sha_file(f) != h: why.append('SHA256SUMS_MISMATCH:' + rel)
        listed = {rel for _, rel in rows}
        for need in ('TEST906_results.json', 'TEST906_manifest.json', 'TEST906_events.jsonl', 'sources/TEST906_executed_906.py'):
            if need not in listed: why.append('SHA256SUMS_DOES_NOT_LIST:' + need)
    marker = '/TEST906_%s/' % Rj.get('run_id')
    for key, o in (Rj.get('objects') or {}).items():
        fs = str(o.get('file', ''))
        if marker not in fs: why.append('OBJECT_OUTSIDE_RUN:' + key); continue
        f = d / fs.split(marker)[-1]
        if not f.is_file() or sha_file(f) != o.get('sha256'): why.append('OBJECT_FILE:' + key)
    rc = [p_ for p_ in (d.parent / ('TEST906_SONUC_%s_RECEIPT.json' % Rj.get('run_id')), d / ('TEST906_SONUC_%s_RECEIPT.json' % Rj.get('run_id'))) if p_.is_file()]
    if not rc: why.append('RECEIPT_NOT_FOUND')
    else:
        try:
            rj = json.loads(rc[0].read_text())
            if rj.get('results_sha256') != sha_file(d / 'TEST906_results.json') or rj.get('run_id') != Rj.get('run_id'): why.append('RECEIPT_DOES_NOT_NAME_THESE_RESULTS')
        except Exception as e: why.append('RECEIPT_UNREADABLE %s' % type(e).__name__)
    return not why, why


def recompute(path, cfg=None):
    """re-score every compile and cell from the raw records + the run's manifest + the object registry (no model / torch); needs
    the pinned 904.py only for its pure parser (from the run's sources/ folder or the repo). Two modes (r2):
    OFFLINE_RESCORE (--recompute-mode rescore): scoring and record self-consistency only; provenance NOT certified; 0 if consistent.
    VERIFIED (default): the same + authenticate_record; 0 ONLY if the record is authenticated; 3 if it rescores consistently but the
    gate chain / evidence set is not authenticated (UNVERIFIED_GATE_CHAIN / NOT_AUTHENTICATED); 1 on any record problem."""
    p = Path(path); Rj = json.loads(p.read_text()); b = (p.parent / 'TEST906_manifest.json').read_bytes(); man = json.loads(b)
    mode = (cfg or {}).get('recompute_mode', 'verified')
    cand = [p.parent / 'sources' / '904.py'] + ([Path(cfg['repo_dir']) / '904.py'] if cfg and cfg.get('repo_dir') else []) + [Path(__file__).parent / '904.py' if '__file__' in globals() else Path('904.py')]
    src = next((c for c in cand if c.is_file() and blob_b(c.read_bytes()) == SRC904['git_blob']), None)
    if src is None: print('904.py with blob %s not found next to the run or in the repo' % SRC904['git_blob']); return 1
    m4 = load_module(src, 'akbas_test904_parser')
    gates = Rj.get('gates') or {}; gates_ok = all(g.get('status') != 'FAIL' for g in gates.values()) and not Rj.get('technical_blockers')
    iso = ((gates.get('GATE_ENGINE_906') or {}).get('data') or {}).get('isolation', {}).get('ok', False)
    ev = evaluate_906(man, Rj.get('compiles', []), Rj.get('cells', []), Rj.get('objects', {}), Rj.get('reference_cells', []), gates_ok, m4, isolation_ok=iso)
    if Rj.get('technical_verdict') != 'PASS' and ev['verdict'] != 'TEST906_INVALID': ev['verdict'] = 'TECHNICAL_UNDECIDABLE'
    probs = verify_run_record(Rj, b, ev)
    consistent = not probs and not ev['integrity_problems']
    print('RECOMPUTE MODE: %s' % ('OFFLINE_RESCORE (scoring only; provenance NOT certified)' if mode == 'rescore' else 'VERIFIED (rescore + record authentication)'))
    print('RECOMPUTED %s | record problems: %d' % (ev['verdict'], len(probs) + len(ev['integrity_problems'])))
    for l in report_lines(ev): print(l)
    for x in probs: print('RUN RECORD PROBLEM:', x)
    if mode == 'rescore':
        print('AUTHENTICATION: NOT_ATTEMPTED (OFFLINE_RESCORE)'); return 0 if consistent else 1
    auth, why = authenticate_record(Rj, p.parent, b)
    print('AUTHENTICATION: %s' % ('AUTHENTICATED_RECORD' if auth else 'UNVERIFIED_GATE_CHAIN / NOT_AUTHENTICATED: ' + '; '.join(why[:40])))
    if not consistent: return 1
    return 0 if auth else 3

if __name__ == '__main__':
    _rc = main(None)
    if _rc and 'get_ipython' not in globals(): sys.exit(_rc)
