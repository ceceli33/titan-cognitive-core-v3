# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST903 — history-conditioned physical write (CUT3 child trace) and clean read
#
# FILE: 903.py (root of ceceli33/titan-cognitive-core-v3). Colab (A100 runtime, Drive):  !python /content/titan-cognitive-core-v3/903.py
#   Offline re-computation of every verdict from the results JSON:  python 903.py --recompute TEST903_results.json
# Exit code: 0 = run complete and technically valid, 1 = technical abort / invalid.
#
# QUESTION. The same final observation E = a->q is written under two histories, H1 = [b->r, E] and H2 = [a->q, E]. The parent
#   history is mounted through the existing 709/730/757 path; only E's new tokens are processed with the parent cache open,
#   and only their H3 rows (layer CUT=3 output) and L0-L3 K/V rows are kept: an E-only child cartridge C1(H). The parent is
#   then closed; the read state is rebuilt from the sealed SSD file alone (standard prefix + C1 + query), and the locked 709
#   answer() decides greedily. Goal g: H1 -> ACT(c); H2 -> ACQUIRE(b) or ACQUIRE(c). Generation 2 (H2 only): the model's own
#   ACQUIRE is applied in the environment (both hidden completions consistent with a=q); the observation is written as C2 with
#   C1 as its only parent; C1 is closed; one right is left; the model decides again reading only C2.
# FORMULA. P_t = 1 is fixed (no write gain, no scaling of H3/KV). Physical write on/off is measured as a separate control.
#   No Bayes posterior, value of information, labels or symbolic argmax enter the model path; the expectimax table below is
#   written into the manifest BEFORE the model loads and is read only by the offline evaluator after GENERATION_SEALED.
# ENGINE (frozen, commit f1007d912773f3460536784ff80a215741bc97e9 == main for these files):
#   709.py blob 6c9f8cbb1eeed848d45133d73f0d7676b68e9125 sha256 68516eb151589800d2fd16bd2d37f8081315420caea9071659e340c62d819589
#   730.py blob b1bad9eb3b111b44413f8ef05a3a140ab66a77dd sha256 c8dfa5bc7735ad2e00bd1b0141c7f0dc6af7cfb7232747e3bbf5b9a26f70dfaf
#   757.py blob 3d88bf8638390995858f23391f1e043faa586835 sha256 474cdc3d20c4283286bbd664c1a4b030f6f1ff532d081465d35bcb96e3e8f619
#   helpers (verbatim, AST-selected): 897npdm_smoke.py fbde1d13 (query / parser), 898.py 14be60ac (MODEL block, forge_record,
#   load_record, mount_from, gen, guard), 899.py 28590849 (hook inventory, integrity digest, pinned revision).
# NEW CODE (only): forge_conditioned_903 (730 forge_native with the parent cache instead of cache=None, positions continue at
#   the parent length, new rows sliced), native_append_child_903 (generated from the pinned 757 native_append_direct by six
#   exact substitutions: no prefix rows in an E-only child, RoPE source = cp['pos0']), environment, manifest, evaluator.
# MODEL: Qwen/Qwen2.5-72B-Instruct @ 495f39366efef23836d0cfae4fbe635880d2be31, NF4 weights / BF16 compute, one A100-SXM4-80GB.
# RUNTIME PINS (= TEST902 run 20261120T103539Z): Python 3.13, torch 2.14.1+cu130, CUDA 13.0, transformers 5.22.1,
#   accelerate 1.16.0, bitsandbytes 0.50.2, tokenizers 0.23.3. Missing pins are installed with a torch constraint.
# DRIVE: /content/drive/MyDrive/TEST903_<run_id> is created only AFTER GATE_ENV confirmed one A100-SXM4-80GB.
# LIMITS: no training / LoRA / RAG / forward hooks / oracle routing / answer override / repair of invalid decisions / tuning
#   within the run. Teacher-forced logits are measured only in the reference check (diagnostic), never as a decision.
# NOT EXECUTED ON GPU BY ITS AUTHOR. CPU tests exercise the environment, manifest, parser, routing and verdict code only.
# =====================================================================================================================
import os, sys, json, hashlib, re, time, ast, shutil, subprocess, textwrap, importlib.metadata
import platform, random, traceback, types, zipfile, gc
import itertools as _it
from pathlib import Path
from datetime import datetime, timezone
sys.dont_write_bytecode = True

TAG = 'TEST903'
MARKER = 'AKBASCORE SILICON HIPPOCAMPUS — TEST903 — history-conditioned CUT3 child trace, clean read, generation 2'
SRC_REPO = 'ceceli33/titan-cognitive-core-v3'; SRC_FILE = '903.py'
ENGINE_COMMIT = 'f1007d912773f3460536784ff80a215741bc97e9'
ENGINE_BLOBS = {'709.py': '6c9f8cbb1eeed848d45133d73f0d7676b68e9125', '730.py': 'b1bad9eb3b111b44413f8ef05a3a140ab66a77dd',
                '757.py': '3d88bf8638390995858f23391f1e043faa586835'}
ENGINE_SHA256 = {'709.py': '68516eb151589800d2fd16bd2d37f8081315420caea9071659e340c62d819589',
                 '730.py': 'c8dfa5bc7735ad2e00bd1b0141c7f0dc6af7cfb7232747e3bbf5b9a26f70dfaf',
                 '757.py': '474cdc3d20c4283286bbd664c1a4b030f6f1ff532d081465d35bcb96e3e8f619'}
TEST_SOURCES = {'897npdm_smoke.py': 'fbde1d130712014070fa6db45ff36f05f9f9d06c', '898.py': '14be60ac98c1f6425e707f1967a6b688e5247e00',
                '899.py': '28590849ec1bc62afc875dc390c0529e3ad35f8f'}
PINS = {'python_minor': '3.13', 'torch': '2.14.1+cu130', 'cuda': '13.0', 'transformers': '5.22.1', 'accelerate': '1.16.0',
        'bitsandbytes': '0.50.2', 'tokenizers': '0.23.3'}
MODEL_ID = 'Qwen/Qwen2.5-72B-Instruct'; MODEL_REVISION = '495f39366efef23836d0cfae4fbe635880d2be31'
GPU_NAME_REQ = 'NVIDIA A100-SXM4-80GB'; GPU_CC_REQ = (8, 0)
REF902 = {'run_id': '20261120T103539Z', 'git_blob': '1d2fe5b4e067d032b578239bbf35d13750a3dfc2',
          'results_sha256': 'e71222a7aa975ed27708049b40af0e8083782e04c7c31591e51270c827479482', 'technical_verdict': 'PASS',
          'scientific_verdict': 'S2D_PROVISIONAL_PASS[DEDUCTION_MATERIALIZATION]', 'model_load_s': 816.0, 'P': 30,
          'prefix_sha256': '847139d502c4db1b19091aaf8f583bfdc2ebe327ed6771e611e95f04a43c7acd',
          'revision_files': {'config.json': '14ca217334fe0fd10148413592d68c99eeb33431ed89c1afa130fee560be2a29',
                             'tokenizer.json': 'c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539',
                             'tokenizer_config.json': '5b5d4f65d0acd3b2d56a35b56d374a36cbc1c8fa5cf3b3febbbfabf22f359583',
                             'model.safetensors.index.json': '6c1d85cad4513d35273d05a4c7206c04b4c8aea0ebd35ef2b26cb88ec56dfe66'},
          'motivation': 'TEST902: W1 NAT card success (D901) and, in W3, the policy re-ACQUIREs an already known action'}
IM_END = '<|im_end|>'

# ===================================================================================================== design (fixed before data)
ROLE_ACTS = ('a', 'b', 'c'); ROLE_OUTS = ('g', 'q', 'r')
E_FACT = ('a', 'q')                                                  # the shared final observation E
HIST = {'H1': ('b', 'r'), 'H2': ('a', 'q'), 'HG': ('b', 'g')}       # parent observation; HG = repetition-shortcut control history
WORLD = {'H1': {'a': 'q', 'b': 'r', 'c': 'g'}, 'HG': {'a': 'q', 'b': 'g', 'c': 'r'}}
H2_COMPLETIONS = {'K1': {'a': 'q', 'b': 'g', 'c': 'r'}, 'K2': {'a': 'q', 'b': 'r', 'c': 'g'}}   # both mappings consistent with a=q
GOALS = ('g', 'r', 'q')                                              # g primary, r goal transfer, q repetition control
COST = 0.1; BUDGET = 2; MAX_NEW_903 = 25                             # MAX_NEW = TEST900-902 decision readouts
GRAMMAR = 'DIRECT'                                                    # 897 parse_npdm DIRECT: ACT <a> | ACQUIRE <a> | STOP
NAMES = {'NS-A': {'a1': 'HQHZVUNSK', 'a2': 'FFZFGCQM', 'a3': 'QPYJSVVHI', 'o1': 'GXXKNHXLM', 'o2': 'MITTDTCJL', 'o3': 'DGUXJIHQT'},
         'NS-B': {'a1': 'RKRXLUXO', 'a2': 'LCOVDUTDP', 'a3': 'NDVAPWGKT', 'o1': 'CDHNHZFAX', 'o2': 'VMNWUUGV', 'o3': 'DWFODADMC'}}
PERMS = {'R0': {'a': 'a1', 'b': 'a2', 'c': 'a3', 'g': 'o1', 'q': 'o2', 'r': 'o3'},
         'R1': {'a': 'a3', 'b': 'a1', 'c': 'a2', 'g': 'o2', 'q': 'o3', 'r': 'o1'}}
ORDERS = ('FWD', 'REV')                                               # action / outcome list order in the query
VARIANTS = tuple((ns, pm) for ns in ('NS-A', 'NS-B') for pm in ('R0', 'R1'))
OBS_TPL_903 = ('Observation: action ', '{A}', ' produces outcome ', '{O}', '.\n')   # one format for h1, E and the gen-2 observation
G1_ARMS = ('CLEAN', 'PARENT_ONLY', 'FULL_REF', 'E_IND', 'SKIP_APPEND')
G2_ARMS = ('C2', 'C2_IND', 'FULL_REF2')
SWAP_CELLS = (('A', 'STRAIGHT', 'H1'), ('B', 'STRAIGHT', 'H2'), ('A', 'CROSS', 'H2'), ('B', 'CROSS', 'H1'), ('A', 'SHAM', 'H1'), ('B', 'SHAM', 'H2'))
TOL903 = {'h3_cos_min': 0.999, 'lower_k_cos_min': 0.999, 'lower_v_cos_min': 0.999, 'first_logits_cos_min': 0.999,
          'argmax_equal': 'DIAGNOSTIC', 'bitwise': 'DIAGNOSTIC', 'independent_forge_repeat': 'BITWISE (required)',
          'mount_repeat': 'BITWISE (required)'}
# Coverage required for the GENERAL generation-2 label, fixed before any GPU data. At most one insufficient branch exists per unit
# (a sealed ACQUIRE b or ACQUIRE c meets r in exactly one of the two hidden completions), so 8 units -> at most 8 paired rows.
G2_GENERAL = {'label': 'GEN2_RECURSION_SUPPORTED', 'insufficient_branches_measured_min': 8, 'units': 8, 'C2_correct': 'all measured',
              'FULL_REF2_correct': 'all measured', 'paired_gains_min': 7,
              'paired_gain': 'C2 in expected_full AND C2_IND not in expected_full, on the same insufficient branch',
              'rationale': 'C2_IND faces two equally valued acts; if it picked between them like a fair coin, P(>=7 paired gains of 8) = 9/256',
              'otherwise': 'GEN2_PARTIAL_SUPPORT[...] with its scope if paired gains >= 1; ATTRIBUTION_UNRESOLVED if C2 is correct on every '
                           'measured row but no paired gain; GEN2_RECURSION_NOT_SUPPORTED otherwise; GEN2_NOT_MEASURABLE if no insufficient row'}
ABORT_903 = {'semantics': 'post-operation guards, not preemptive timeouts, no OOM guarantee', 'experiment_wall_s': 3 * 3600,
             'gpu_peak_gib': 74.0, 'cartridge_bytes_gib': 4.0, 'cpu_ram_frac': 0.85, 'query_s': 180.0, 'forge_append_s': 60.0}
READOUT_LIMIT = 340


def sha_b(b): return hashlib.sha256(b).hexdigest()
def sha_s(s): return sha_b(s.encode('utf-8'))
def blob_b(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
def canon(v): return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(',', ':'), default=list)
def jsha(v): return sha_s(canon(v))


# ------------------------------------------------------------------------------------------------ pure environment layer
def variant_names(ns, pm):
    """role -> name for one identity variant (name set x role permutation)."""
    return {role: NAMES[ns][PERMS[pm][role]] for role in ROLE_ACTS + ROLE_OUTS}


def contract_903(ns, order, goal_name):
    a = [NAMES[ns][k] for k in ('a1', 'a2', 'a3')]; o = [NAMES[ns][k] for k in ('o1', 'o2', 'o3')]
    if order == 'REV': a, o = a[::-1], o[::-1]
    return {'actions': a, 'outcomes': o, 'goal': goal_name, 'cost': COST, 'budget': BUDGET}


def consistent(known):
    return [dict(zip(ROLE_ACTS, p)) for p in _it.permutations(ROLE_OUTS) if all(dict(zip(ROLE_ACTS, p))[a] == o for a, o in known.items())]


def q_values(known, left, goal):
    """Exact expectimax over the uniform prior on bijections (TEST903 rules: ACT terminal 1/0, ACQUIRE -0.1 and one right,
    STOP 0, no right left = harness end with 0). OFFLINE ONLY: manifest before the model, evaluator after GENERATION_SEALED."""
    ms = consistent(known)
    def V(kn, lf):
        if lf == 0: return 0.0
        return max(q_values(kn, lf, goal).values())
    Q = {'STOP': 0.0}
    for x in ROLE_ACTS:
        Q['ACT ' + x] = sum(1.0 for m in ms if m[x] == goal) / len(ms)
        Q['ACQUIRE ' + x] = -COST + sum(V(dict(known, **{x: m[x]}), left - 1) for m in ms) / len(ms)
    return Q


def optimal_set(known, left, goal, tol=1e-9):
    Q = q_values(dict(known), left, goal); best = max(Q.values())
    return sorted(k for k, v in Q.items() if v >= best - tol)


class Env903:
    """One branch environment (names). The true mapping lives only here. ACQUIRE never pays reward, even if it shows the goal."""
    def __init__(self, mapping, goal, left=BUDGET):
        self.m = dict(mapping); self.goal = goal; self.left = int(left); self.done = False; self.reward = 0.0; self.cost = 0.0; self.trace = []

    def step(self, key):
        if self.done or self.left <= 0: raise RuntimeError('ENV_STEP_AFTER_END')
        rec = {'decision': key if isinstance(key, str) else '%s %s' % key, 'left_before': self.left}
        if key == 'STOP':
            self.done = True; rec.update(event='MODEL_STOP', reward=0.0)
        elif key == 'WASTE':
            self.done = True; rec.update(event='INVALID_NOT_REPAIRED', reward=0.0)
        elif key[0] == 'ACT':
            r = 1.0 if self.m[key[1]] == self.goal else 0.0; self.reward += r; self.done = True; rec.update(event='ACT', reward=r)
        elif key[0] == 'ACQUIRE':
            self.left -= 1; self.cost += COST; rec.update(event='ACQUIRE', reward=0.0, obs=[key[1], self.m[key[1]]])
            if self.left == 0: self.done = True; rec['end'] = 'BUDGET_EXHAUSTED_HARNESS'
        else: raise RuntimeError('ENV_UNKNOWN_KEY %r' % (key,))
        rec.update(left_after=self.left, terminal=self.done, cost_total=round(self.cost, 6), reward_total=self.reward); self.trace.append(rec)
        return rec

    def clone(self):
        e = Env903(self.m, self.goal, self.left); e.done, e.reward, e.cost, e.trace = self.done, self.reward, self.cost, list(self.trace); return e


def names_world(world_roles, V): return {V[a]: V[o] for a, o in world_roles.items()}


def role_decision(parsed_key, V):
    inv = {v: k for k, v in V.items()}
    if parsed_key == 'STOP': return 'STOP'
    if parsed_key == 'WASTE': return 'INVALID'
    return '%s %s' % (parsed_key[0], inv[parsed_key[1]])


def worlds_of(hist):
    """the environments a G1 cell is run in (H2: both hidden completions; history-free arms: every history world)."""
    if hist == 'H2': return dict(H2_COMPLETIONS)
    if hist in WORLD: return {hist: WORLD[hist]}
    out = dict(WORLD); out.update(H2_COMPLETIONS); return out


# ------------------------------------------------------------------------------------------------ cell ids / manifest
def cid_g1(arm, ns, pm, order, hist, goal): return 'G1/%s/%s/%s/%s/%s/%s' % (arm, ns, pm, order, hist or '-', goal)
def cid_swap(ns, pm, slot, kind, hist): return 'G1/SWAP_%s/%s/%s/FWD/%s/%s/g' % (kind, ns, pm, slot, hist)
def cid_g2(arm, ns, pm, order, K, x): return 'G2/%s/%s/%s/%s/%s/ACQ_%s/g' % (arm, ns, pm, order, K, x)


def arm_info(arm, hist):
    """role-level facts physically present in each G1 arm's read state (for the offline expected sets)."""
    if arm in ('CLEAN', 'FULL_REF'): return dict([HIST[hist], E_FACT])
    if arm == 'PARENT_ONLY': return dict([HIST[hist]])
    if arm == 'E_IND': return dict([E_FACT])
    if arm == 'SKIP_APPEND': return {}
    raise KeyError(arm)


def build_manifest():
    cells = {}; branches = {}; plan = {}
    full = {(h, g): optimal_set(dict([HIST[h], E_FACT]), BUDGET, g) for h in HIST for g in GOALS}
    for ns, pm in VARIANTS:
        for order in ORDERS:
            for g in GOALS:
                for arm in G1_ARMS:
                    for h in ((None,) if arm in ('E_IND', 'SKIP_APPEND') else tuple(HIST)):
                        hs = tuple(HIST) if h is None else (h,)
                        cells[cid_g1(arm, ns, pm, order, h, g)] = {
                            'gen': 1, 'arm': arm, 'ns': ns, 'perm': pm, 'order': order, 'history': h, 'goal': g, 'left': BUDGET,
                            'info_roles': arm_info(arm, h), 'expected_own': optimal_set(arm_info(arm, h), BUDGET, g),
                            'expected_full': {hh: full[(hh, g)] for hh in hs}}
        for slot, kind, h in SWAP_CELLS:
            cells[cid_swap(ns, pm, slot, kind, h)] = {'gen': 1, 'arm': 'SWAP_' + kind, 'ns': ns, 'perm': pm, 'order': 'FWD', 'history': h, 'goal': 'g',
                                                     'left': BUDGET, 'slot': slot, 'tensor_history': h,
                                                     'label_history': ({'H1': 'H2', 'H2': 'H1'}[h] if kind == 'SHAM' else h),
                                                     'expected_own': full[(h, 'g')], 'expected_full': {h: full[(h, 'g')]},
                                                     'repeat_of': cid_g1('CLEAN', ns, pm, 'FWD', h, 'g')}
        for order in ORDERS:
            for K, m in H2_COMPLETIONS.items():
                plan['G2P/%s/%s/%s/%s' % (ns, pm, order, K)] = {
                    'ns': ns, 'perm': pm, 'order': order, 'completion': K, 'first_cell': cid_g1('CLEAN', ns, pm, order, 'H2', 'g'),
                    'candidates': {x: 'G2B/%s/%s/%s/%s/ACQ_%s' % (ns, pm, order, K, x) for x in ROLE_ACTS},
                    'not_measured_id': 'G2B/%s/%s/%s/%s/-' % (ns, pm, order, K)}
                for x in ROLE_ACTS:
                    o = m[x]; fullk = {'a': 'q', x: o}; ownk = {x: o}
                    ef = optimal_set(fullk, BUDGET - 1, 'g'); eo = optimal_set(ownk, BUDGET - 1, 'g')
                    bid = 'G2B/%s/%s/%s/%s/ACQ_%s' % (ns, pm, order, K, x)
                    branches[bid] = {'ns': ns, 'perm': pm, 'order': order, 'completion': K, 'acquired': x, 'observed': o, 'left': BUDGET - 1,
                                     'expected_full': ef, 'expected_new_obs_only': eo, 'new_obs_insufficient': ef != eo,
                                     'cells': {arm: cid_g2(arm, ns, pm, order, K, x) for arm in G2_ARMS}}
                    for arm in G2_ARMS:
                        cells[cid_g2(arm, ns, pm, order, K, x)] = {'gen': 2, 'arm': arm, 'ns': ns, 'perm': pm, 'order': order, 'history': 'H2',
                                                                   'goal': 'g', 'left': BUDGET - 1, 'branch': bid,
                                                                   'expected_own': eo if arm == 'C2_IND' else ef, 'expected_full': {'H2': ef},
                                                                   'conditional': 'measured only if the sealed first decision is ACQUIRE %s' % x}
    fam = {'PRIMARY': [('H1', 'g'), ('H2', 'g')], 'TRANSFER_R': [('H1', 'r'), ('H2', 'r')],
           'CONTENT_REPETITION': [('H1', 'g'), ('HG', 'g'), ('H1', 'q'), ('HG', 'q')]}
    n1 = sum(1 for c in cells.values() if c['gen'] == 1 and not c.get('repeat_of'))
    return {'test': TAG, 'marker': MARKER, 'design': {
                'roles': {'actions': ROLE_ACTS, 'outcomes': ROLE_OUTS}, 'E': E_FACT, 'histories': HIST, 'worlds': WORLD, 'h2_completions': H2_COMPLETIONS,
                'goals': GOALS, 'cost': COST, 'budget': BUDGET, 'max_new': MAX_NEW_903, 'grammar': GRAMMAR, 'names': NAMES, 'perms': PERMS,
                'orders': ORDERS, 'variants': VARIANTS, 'obs_template': OBS_TPL_903, 'tolerances': TOL903, 'g2_general_requirement': G2_GENERAL,
                'P_t': 1, 'labels_in_model_input': False, 'instructed_card_arm': 'NOT_PRESENT (no card arm in TEST903)',
                'c_r_refutation_sequence': 'NOT_INCLUDED (conflicts with the deterministic bijection)',
                'arms': {'CLEAN': 'E-only child C1(H) forged with the parent mounted (physical write ON, history ON), read alone',
                         'E_IND': 'forge_native(E) under the empty prefix = write-history-OFF; final-event-only reduces to the same function and '
                                  'inputs, so it is ONE control',
                         'SKIP_APPEND': 'nothing appended (empty prefix only; not a zero tensor) = physical write OFF',
                         'PARENT_ONLY': 'the parent observation cartridge alone', 'FULL_REF': 'parent + E native cartridges (existing 757 path, '
                         'history open) = native reading reference', 'SWAP_*': 'two read slots (separate files / directories / mounts)',
                         'C2': 'child of the clean C1 mount (C1 its only parent), read alone with one right', 'C2_IND': 'gen-2 observation '
                         'forged without history', 'FULL_REF2': 'parent + E + gen-2 observation native cartridges'}},
            'families': fam, 'expected_full_by_history_goal': {'%s/%s' % k: v for k, v in full.items()},
            'cells': cells, 'gen2_branches': branches, 'gen2_plan': plan,
            'sample_counts': {'gen1_independent_cells': n1, 'gen1_swap_repeat_cells': len(VARIANTS) * len(SWAP_CELLS),
                              'gen2_branches_planned': len(VARIANTS) * len(ORDERS) * len(H2_COMPLETIONS),
                              'gen2_cells_max_measured': len(VARIANTS) * len(ORDERS) * len(H2_COMPLETIONS) * len(G2_ARMS),
                              'cells_per_arm': {a: sum(1 for c in cells.values() if c['arm'] == a) for a in sorted({c['arm'] for c in cells.values()})},
                              'samples_per_cell': 1, 'decoding': 'greedy (deterministic): repeats are not independent samples'},
            'verdict_rules': VERDICT_RULES}


VERDICT_RULES = {
    'success': 'a cell succeeds iff its parsed greedy decision (role level) is in expected_full[history] (invalid output never repaired)',
    'unit': 'one (name set, role permutation, query order) = 8 units; every required cell must succeed in every unit',
    'G1_required': 'PRIMARY (CLEAN H1/g, H2/g) + TRANSFER_R (CLEAN H1/r, H2/r) + CONTENT_REPETITION (CLEAN H1/g, HG/g, H1/q, HG/q) + SWAP',
    'SWAP': 'per variant: straight, cross and sham read-slot cells succeed for the history of the TENSORS they carry, and each equals the '
            'CLEAN FWD decision of that tensor history (sham: same tensors, swapped file/slot/book identity -> no effect)',
    'NAMES_POSITIONS': 'PRIMARY split by name set / permutation / order (report); PASS iff PRIMARY passes in all 8 units',
    'information_removal_controls': 'E_IND (write-history-off == final-event-only), PARENT_ONLY, SKIP_APPEND: a control reproduces the '
            'discriminative pattern in a unit iff its H1/g decision is in expected_full[H1/g] AND its H2/g decision in expected_full[H2/g]',
    'G1_verdict': 'TECHNICAL_UNDECIDABLE if technical integrity failed; else PORTABLE_TRACE_SUPPORTED iff all required cells succeed, no '
                  'control reproduces the pattern in any unit and the FULL_REF counterpart of every required cell succeeds; '
                  'ATTRIBUTION_UNRESOLVED if all required cells succeed but a control reproduces or a FULL_REF counterpart fails; '
                  'else PORTABLE_TRACE_NOT_SUPPORTED',
    'G2_verdict': 'planned branch = (unit, hidden completion), 16. Recursion evidence only from measured branches where the new '
                  'observation alone is insufficient (expected_new_obs_only != expected_full); they form a paired table C2 | C2_IND | '
                  'FULL_REF2. Counts: measured insufficient rows, C2 correct, paired gains (C2 correct while C2_IND fails). General label '
                  'and partial labels: see design.g2_general_requirement. Sufficient branches are reported separately and are not '
                  'recursion evidence. Hash or logit differences alone are never behavioural success.',
    'integrity': 'evaluate() and --recompute run the same record integrity check first. G1: every manifest G1 cell exactly once, no '
                 'unknown G1 id, record fields equal to the manifest, decision_key / decision_role / valid mutually consistent. G2: '
                 'for every planned branch exactly one branch record consistent with the sealed first decision (ACQUIRE x -> MEASURED '
                 'on the ACQ_x branch with the completion outcome; a terminal first decision -> NOT_MEASURED with the matching reason, '
                 'reported separately); every measured branch has C2, C2_IND and FULL_REF2 exactly once; no G2 record outside a measured '
                 'branch. Any missing, duplicated or contradictory record -> TECHNICAL_UNDECIDABLE for the affected generation, with the '
                 'offending ids.'}


# ------------------------------------------------------------------------------------------------ offline evaluator (JSON only)
def cell_ok(man_cell, rec, hist=None):
    if rec is None or not rec.get('valid'): return False
    h = hist or man_cell['history']; return rec.get('decision_role') in man_cell['expected_full'][h]


TERMINAL_REASON = {'ACT': 'FIRST_DECISION_ACT_TERMINAL', 'STOP': 'FIRST_DECISION_STOP', 'INVALID': 'FIRST_DECISION_INVALID_NOT_REPAIRED'}
REC_FIELDS = ('arm', 'ns', 'perm', 'order', 'history', 'goal', 'left')


def _key_role(key, ns, pm):
    """decision_role implied by a stored decision_key (names -> roles of that variant)."""
    V = variant_names(ns, pm); inv = {v: k for k, v in V.items()}
    if key in ('STOP', 'WASTE'): return 'STOP' if key == 'STOP' else 'INVALID'
    kind, _, name = str(key).partition(' ')
    return '%s %s' % (kind, inv[name]) if kind in ('ACT', 'ACQUIRE') and name in inv and name in [V[a] for a in ROLE_ACTS] else None


def integrity_check(man, cells):
    """Record integrity of a results cell list against the manifest (used by evaluate() and therefore by --recompute)."""
    M = man['cells']; P_ = man['gen2_plan']; comp = man['design']['h2_completions']
    prob = {'G1': [], 'G2': []}; cnt = {}; recs = {}; branches = []
    for c in cells:
        cid = c.get('cell_id')
        if c.get('branch_record') is not None: branches.append(c['branch_record']); continue
        if not isinstance(cid, str) or not cid.startswith(('G1/', 'G2/')):
            prob['G1'].append('UNKNOWN_RECORD:%s' % cid); prob['G2'].append('UNKNOWN_RECORD:%s' % cid); continue
        cnt[cid] = cnt.get(cid, 0) + 1; recs[cid] = c
    for cid, n in cnt.items():                                           # unknown / duplicate / contradictory cell records
        g = 'G1' if cid.startswith('G1/') else 'G2'
        if cid not in M: prob[g].append('UNKNOWN_CELL:' + cid); continue
        if n != 1: prob[g].append('DUPLICATE_CELL:%s(x%d)' % (cid, n))
        r, m = recs[cid], M[cid]
        bad = [f for f in REC_FIELDS if r.get(f) != m.get(f)] + (['branch'] if m['gen'] == 2 and r.get('branch') != m['branch'] else [])
        p = r.get('parsed') or {}; st = p.get('status'); key = r.get('decision_key')
        want_key = ('%s %s' % (p.get('kind'), p.get('action'))) if st == 'VALID' else ('STOP' if st == 'STOP' else 'WASTE')
        if key != want_key: bad.append('decision_key')
        if r.get('valid') != (st in ('VALID', 'STOP')): bad.append('valid')
        if r.get('decision_role') != _key_role(key, m['ns'], m['perm']): bad.append('decision_role')
        if bad: prob[g].append('CONTRADICTORY_CELL:%s%s' % (cid, bad))
    for cid, m in M.items():                                             # every planned G1 cell exactly once
        if m['gen'] == 1 and cid not in cnt: prob['G1'].append('MISSING_CELL:' + cid)
    terminal = []; measured = []; expected_g2 = set(); bcount = {}
    for b in branches: bcount[b.get('plan_id')] = bcount.get(b.get('plan_id'), 0) + 1
    for pid in bcount:
        if pid not in P_: prob['G2'].append('UNKNOWN_BRANCH:%s' % pid)
    for pid, pl in P_.items():
        bs = [b for b in branches if b.get('plan_id') == pid]
        own = {c for bid in pl['candidates'].values() for c in man['gen2_branches'][bid]['cells'].values()}
        def bad(msg):                                                    # reported once per plan: its cells are not also listed as orphans
            prob['G2'].append(msg); expected_g2.update(own)
        if len(bs) != 1: bad(('MISSING_BRANCH:%s' % pid) if not bs else ('DUPLICATE_BRANCH:%s(x%d)' % (pid, len(bs)))); continue
        b = bs[0]; first = recs.get(pl['first_cell']) if cnt.get(pl['first_cell']) == 1 else None
        if first is None: bad('FIRST_DECISION_UNAVAILABLE:%s<-%s' % (pid, pl['first_cell'])); continue
        fd = first.get('decision_role')
        if b.get('first_cell') != pl['first_cell'] or b.get('first_decision') != fd or b.get('completion') != pl['completion']:
            bad('BRANCH_CONTRADICTS_SEALED_FIRST_DECISION:%s(%s vs %s)' % (pid, b.get('first_decision'), fd)); continue
        if fd and fd.startswith('ACQUIRE '):
            x = fd.split(' ', 1)[1]; bid = pl['candidates'].get(x)
            if not (b.get('status') == 'MEASURED' and b.get('branch_id') == bid and b.get('acquired') == x and b.get('observed') == comp[pl['completion']][x]):
                bad('BRANCH_RECORD_INCONSISTENT:%s' % pid); continue
            ids = man['gen2_branches'][bid]['cells']; expected_g2 |= set(ids.values())
            for arm, cid in ids.items():
                if cnt.get(cid, 0) != 1: prob['G2'].append('%s_G2_CELL:%s' % ('MISSING' if not cnt.get(cid) else 'DUPLICATE', cid))
            measured.append((pid, bid))
        else:
            want = TERMINAL_REASON.get((fd or 'INVALID').split(' ')[0])
            if not (b.get('status') == 'NOT_MEASURED' and b.get('reason') == want and b.get('branch_id') == pl['not_measured_id']):
                bad('BRANCH_RECORD_INCONSISTENT:%s' % pid); continue
            terminal.append({'plan_id': pid, 'first_decision': fd, 'reason': want})
    for cid in cnt:
        if cid.startswith('G2/') and cid in M and cid not in expected_g2: prob['G2'].append('G2_CELL_OUTSIDE_MEASURED_BRANCH:' + cid)
    return {'G1': {'ok': not prob['G1'], 'problems': sorted(set(prob['G1']))}, 'G2': {'ok': not prob['G2'], 'problems': sorted(set(prob['G2']))},
            'terminal_not_measured': terminal, 'measured': measured}


def evaluate(man, cells, technical_ok):
    """Every verdict from the manifest + the cell records only (the reader can re-run this on the JSON). The record integrity
    check runs first; a failure makes the affected generation TECHNICAL_UNDECIDABLE."""
    IC = integrity_check(man, cells)
    C = {c['cell_id']: c for c in cells}; M = man['cells']; out = {'units': [], 'families': {}, 'controls': {}, 'reference': {}, 'missing_cells': []}
    units = [(ns, pm, o) for ns, pm in VARIANTS for o in ORDERS]
    def rec(arm, ns, pm, o, h, g): return C.get(cid_g1(arm, ns, pm, o, h, g))
    def ok(arm, ns, pm, o, h, g, hist=None):
        k = cid_g1(arm, ns, pm, o, h, g)
        if k not in C: out['missing_cells'].append(k)
        return cell_ok(M[k], C.get(k), hist)
    req_fail = []; ref_fail = []
    for fam, cl in man['families'].items():
        rows = {}
        for ns, pm, o in units:
            r = {'%s/%s' % (h, g): ok('CLEAN', ns, pm, o, h, g) for h, g in cl}
            rows['%s/%s/%s' % (ns, pm, o)] = r
            req_fail += ['%s:%s/%s/%s:%s' % (fam, ns, pm, o, k) for k, v in r.items() if not v]
            ref_fail += ['%s:%s/%s/%s:%s' % (fam, ns, pm, o, '%s/%s' % (h, g)) for h, g in cl if not ok('FULL_REF', ns, pm, o, h, g)]
        out['families'][fam] = {'pass': all(all(r.values()) for r in rows.values()), 'units_pass': sum(all(r.values()) for r in rows.values()),
                                'units': len(rows), 'rows': rows}
    sw = {}
    for ns, pm in VARIANTS:
        cl = rec('CLEAN', ns, pm, 'FWD', 'H1', 'g'), rec('CLEAN', ns, pm, 'FWD', 'H2', 'g'); clean_dec = {'H1': cl[0] and cl[0].get('decision_role'), 'H2': cl[1] and cl[1].get('decision_role')}
        rowsw = {}
        for slot, kind, h in SWAP_CELLS:
            k = cid_swap(ns, pm, slot, kind, h); r = C.get(k)
            if r is None: out['missing_cells'].append(k)
            rowsw['%s/%s/%s' % (slot, kind, h)] = {'ok': cell_ok(M[k], r), 'route_equal_clean': r is not None and r.get('decision_role') == clean_dec[h],
                                                   'decision': r and r.get('decision_role')}
        sw['%s/%s' % (ns, pm)] = rowsw
        req_fail += ['SWAP:%s/%s:%s' % (ns, pm, k) for k, v in rowsw.items() if not (v['ok'] and v['route_equal_clean'])]
    out['families']['SWAP'] = {'pass': all(v['ok'] and v['route_equal_clean'] for r in sw.values() for v in r.values()), 'rows': sw}
    np_ = {}
    for ns, pm, o in units:
        np_['%s/%s/%s' % (ns, pm, o)] = all(out['families']['PRIMARY']['rows']['%s/%s/%s' % (ns, pm, o)].values())
    by = lambda i: {v: sum(1 for k, p in np_.items() if k.split('/')[i] == v and p) for v in sorted({k.split('/')[i] for k in np_})}
    out['families']['NAMES_POSITIONS'] = {'pass': all(np_.values()), 'units_pass': sum(np_.values()), 'units': len(np_),
                                          'by_name_set': by(0), 'by_permutation': by(1), 'by_order': by(2)}
    for arm in ('E_IND', 'PARENT_ONLY', 'SKIP_APPEND'):
        rep = {}
        for ns, pm, o in units:
            h = (None, None) if arm in ('E_IND', 'SKIP_APPEND') else ('H1', 'H2')
            r1, r2 = rec(arm, ns, pm, o, h[0], 'g'), rec(arm, ns, pm, o, h[1], 'g')
            k1, k2 = cid_g1(arm, ns, pm, o, h[0], 'g'), cid_g1(arm, ns, pm, o, h[1], 'g')
            rep['%s/%s/%s' % (ns, pm, o)] = cell_ok(M[k1], r1, 'H1') and cell_ok(M[k2], r2, 'H2')
        out['controls'][arm] = {'reproduces_pattern_units': sum(rep.values()), 'units': len(rep), 'rows': rep}
    out['reference'] = {'FULL_REF_failures_on_required_cells': sorted(set(ref_fail)),
                        'FULL_REF_cells_ok': sum(1 for k, c in M.items() if c['gen'] == 1 and c['arm'] == 'FULL_REF' and cell_ok(c, C.get(k))),
                        'FULL_REF_cells': sum(1 for c in M.values() if c['gen'] == 1 and c['arm'] == 'FULL_REF')}
    req_all = not req_fail; explained = [a for a, v in out['controls'].items() if v['reproduces_pattern_units'] > 0]
    out['required_failures'] = req_fail
    out['integrity'] = IC
    if not technical_ok or not IC['G1']['ok']: v1 = 'TECHNICAL_UNDECIDABLE'
    elif req_all and not explained and not ref_fail: v1 = 'PORTABLE_TRACE_SUPPORTED'
    elif req_all: v1 = 'ATTRIBUTION_UNRESOLVED'
    else: v1 = 'PORTABLE_TRACE_NOT_SUPPORTED'
    out['G1_verdict'] = v1; out['G1_reasons'] = {'required_all_pass': req_all, 'controls_reproducing': explained, 'full_ref_failures': len(set(ref_fail))}
    # ---- generation 2 (only from branches that passed the integrity check)
    B = man['gen2_branches']; rows = []; suf = []; GG = man['design']['g2_general_requirement']
    for pid, bid in (IC['measured'] if IC['G2']['ok'] else []):
        mb = B[bid]; row = {'plan_id': pid, 'branch_id': bid, 'ns': mb['ns'], 'perm': mb['perm'], 'order': mb['order'], 'completion': mb['completion'],
                            'acquired': mb['acquired'], 'observed': mb['observed']}
        for arm in G2_ARMS:
            r = C.get(mb['cells'][arm]); row[arm] = {'decision': r and r.get('decision_role'), 'ok': cell_ok(M[mb['cells'][arm]], r, 'H2')}
        row['paired_gain'] = row['C2']['ok'] and not row['C2_IND']['ok']
        (rows if mb['new_obs_insufficient'] else suf).append(row)
    n = len(rows); c2 = sum(r['C2']['ok'] for r in rows); gains = sum(r['paired_gain'] for r in rows); ref2 = sum(r['FULL_REF2']['ok'] for r in rows)
    ind = sum(r['C2_IND']['ok'] for r in rows); units = len({(r['ns'], r['perm'], r['order']) for r in rows})
    scope = {'insufficient_branches_measured': n, 'C2_correct': c2, 'paired_gains_C2_correct_and_C2_IND_failed': gains, 'C2_IND_correct': ind,
             'FULL_REF2_correct': ref2, 'units_covered': units, 'units': GG['units'], 'general_requirement': GG}
    if not technical_ok or not IC['G2']['ok']: v2 = 'TECHNICAL_UNDECIDABLE'
    elif n == 0: v2 = 'GEN2_NOT_MEASURABLE'
    elif n >= GG['insufficient_branches_measured_min'] and c2 == n and ref2 == n and gains >= GG['paired_gains_min']: v2 = GG['label']
    elif gains >= 1: v2 = 'GEN2_PARTIAL_SUPPORT[paired_gains=%d/%d,C2=%d/%d,FULL_REF2=%d/%d,coverage=%d/%d]' % (gains, n, c2, n, ref2, n, n, GG['insufficient_branches_measured_min'])
    elif c2 == n: v2 = 'ATTRIBUTION_UNRESOLVED'
    else: v2 = 'GEN2_RECURSION_NOT_SUPPORTED'
    term = {}
    for t in IC['terminal_not_measured']: term[t['reason']] = term.get(t['reason'], 0) + 1
    scope['text'] = ('%d paired gain%s (C2 correct, C2_IND wrong) in %d measured insufficient branch%s; C2 correct %d/%d; C2_IND correct %d/%d; '
                     'FULL_REF2 correct %d/%d; coverage %d/%d (general label needs >= %d rows, C2 and FULL_REF2 all correct, >= %d paired gains)' % (
                         gains, '' if gains == 1 else 's', n, '' if n == 1 else 'es', c2, n, ind, n, ref2, n, n, GG['insufficient_branches_measured_min'],
                         GG['insufficient_branches_measured_min'], GG['paired_gains_min']))
    g2 = {'branches_planned': len(man['gen2_plan']), 'branches_measured': len(IC['measured']), 'not_measured_terminal': term,
          'not_measured_terminal_ids': IC['terminal_not_measured'], 'not_measured_by_reason': term,
          'insufficient_branches': n, 'sufficient_branches': len(suf), 'scope': scope, 'paired_table': rows, 'sufficient_rows': suf,
          'insufficient': {arm: sum(r[arm]['ok'] for r in rows) for arm in G2_ARMS}, 'sufficient': {arm: sum(r[arm]['ok'] for r in suf) for arm in G2_ARMS},
          'integrity_problems': IC['G2']['problems']}
    g2['G2_verdict'] = v2; out['G2'] = g2; out['G2_verdict'] = v2
    out['missing_cells'] = sorted(set(out['missing_cells']))
    return out


def paired_table_lines(ev_):
    g2 = ev_['G2']; L = ['GEN2 PAIRED TABLE (new observation alone insufficient): name set | perm | order | completion | ACQUIRE -> obs | '
                         'C2 | C2_IND | FULL_REF2 | paired gain']
    for r in g2['paired_table']:
        L.append('  %-5s %-3s %-4s %-3s ACQUIRE %s->%s | %s | %s | %s | %s' % (r['ns'], r['perm'], r['order'], r['completion'], r['acquired'], r['observed'],
                 *['%s%s' % (r[a]['decision'], '[ok]' if r[a]['ok'] else '[x]') for a in G2_ARMS], 'GAIN' if r['paired_gain'] else '-'))
    sc = g2['scope']
    L.append('  measured insufficient branches: %d | C2 correct: %d | C2 correct while C2_IND failed (paired gains): %d' % (
        sc['insufficient_branches_measured'], sc['C2_correct'], sc['paired_gains_C2_correct_and_C2_IND_failed']))
    L.append('  scope: ' + sc['text'])
    return L


def integrity_lines(ev_):
    ic = ev_['integrity']; L = []
    for g in ('G1', 'G2'):
        L.append('INTEGRITY %s: %s%s' % (g, 'PASS' if ic[g]['ok'] else 'FAIL -> TECHNICAL_UNDECIDABLE', '' if ic[g]['ok'] else ' | ' + '; '.join(ic[g]['problems'][:20])))
    L.append('GEN2 not measured because of a real terminal first decision: %s' % ([(t['plan_id'], t['first_decision']) for t in ic['terminal_not_measured']] or 'none'))
    return L


def decision_table(man, cells):
    """console table: one line per unit, role-level decision and ok/x against expected_full."""
    C = {c['cell_id']: c for c in cells}; cols = [('H1', 'g'), ('H2', 'g'), ('HG', 'g'), ('H1', 'r'), ('H2', 'r'), ('H1', 'q'), ('HG', 'q')]
    lines = ['TEST903 DECISION TABLE (CLEAN C1 reads; [ok]/[x] = in expected set; ref = FULL_REF)',
             '%-16s ' % 'unit' + ' '.join('%-18s' % ('%s/%s' % c) for c in cols)]
    for ns, pm in VARIANTS:
        for o in ORDERS:
            row = []
            for h, g in cols:
                k = cid_g1('CLEAN', ns, pm, o, h, g); r = C.get(k); kr = cid_g1('FULL_REF', ns, pm, o, h, g)
                row.append('%-18s' % ('%s%s|%s' % ((r or {}).get('decision_role', '-'), '[ok]' if cell_ok(man['cells'][k], r) else '[x]',
                                                   'ref' + ('+' if cell_ok(man['cells'][kr], C.get(kr)) else '-'))))
            lines.append('%-16s ' % ('%s/%s/%s' % (ns, pm, o)) + ' '.join(row))
    lines.append('GEN2 (H2/g): branch -> C2 | C2_IND | FULL_REF2 (insufficient = new observation alone does not determine the act)')
    for bid, b in man['gen2_branches'].items():
        rs = [C.get(b['cells'][a]) for a in G2_ARMS]
        if rs[0] is None: continue
        lines.append('  %-34s %-12s %s' % (bid, 'INSUFFICIENT' if b['new_obs_insufficient'] else 'sufficient',
                     ' | '.join('%s%s' % ((r or {}).get('decision_role', 'MISSING'), '[ok]' if cell_ok(man['cells'][b['cells'][a]], r, 'H2') else '[x]') for a, r in zip(G2_ARMS, rs))))
    return '\n'.join(lines)


# ===================================================================================================== run infrastructure
RUN_ID = None; ROOT = None; LOG = None; OUT = None; EVENTS = None; CART_DIR = None; R = None
EVSEQ = [0]; SAVE_T = [0.0]; T0 = time.perf_counter(); DRIVE_DIR = None; DRIVE_ERR = {'mount': None, 'backup_failures': 0, 'last': None}
X = types.SimpleNamespace()


class StopT896(Exception):
    """Technical stop (name kept: the verbatim 898 cartridge / guard functions raise it). Never a scientific result."""


CRITICAL = ('GATE_RUNTIME_PINS', 'GATE_ENV', 'GATE_SOURCE_EXTRACT', 'GATE_TOKENIZER_PRE_MODEL', 'GATE_MANIFEST', 'MODEL', 'GATE_ENGINE',
            'GATE_REFERENCE', 'GATE_END_INTEGRITY')


def config(argv=None):
    import argparse
    ap = argparse.ArgumentParser(add_help=False)
    d = {'out_root': '/content' if Path('/content').exists() else '/tmp', 'src_dir': '',
         'repo_dir': '/content/titan-cognitive-core-v3' if Path('/content').exists() else '', 'recompute': ''}
    for k, v in d.items(): ap.add_argument('--' + k.replace('_', '-'), default=os.environ.get('T903_' + k.upper(), v))
    a, _ = ap.parse_known_args(list(argv) if argv is not None else [])
    return {k: getattr(a, k) for k in d}


def init_run(cfg):
    global RUN_ID, ROOT, LOG, OUT, EVENTS, CART_DIR, R
    RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    ROOT = Path(cfg['out_root']) / ('TEST903_' + RUN_ID); ROOT.mkdir(parents=True, exist_ok=False)
    LOG = ROOT / 'TEST903.log'; OUT = ROOT / 'TEST903_results.json'; EVENTS = ROOT / 'TEST903_events.jsonl'; CART_DIR = ROOT / 'cartridges'
    for f in (LOG, EVENTS): f.write_text('')
    EVSEQ[0] = 0
    R = {'test': TAG, 'marker': MARKER, 'run_id': RUN_ID, 'status': 'STARTED', 'executed_by_author': False,
         'top': {'first_failed_gate': None, 'missing_cells': None, 'gen2_not_measured': None, 'technical_verdict': None, 'G1_verdict': None, 'G2_verdict': None},
         'chain': {'TEST902': REF902}, 'engine': {'commit': ENGINE_COMMIT, 'blobs': ENGINE_BLOBS, 'sha256': ENGINE_SHA256}, 'helpers': TEST_SOURCES,
         'pins': PINS, 'model': {'id': MODEL_ID, 'revision': MODEL_REVISION}, 'abort_limits': ABORT_903,
         'gates': {}, 'checks': [], 'technical_blockers': [], 'config': dict(cfg), 'cells': [], 'gen2_branches': []}
    return ROOT


def log(*xs):
    s = ' '.join(str(x) for x in xs); print(s, flush=True)
    with LOG.open('a') as f: f.write(s + '\n')


def save(force=True):
    if not force and time.perf_counter() - SAVE_T[0] < 15.0: return
    SAVE_T[0] = time.perf_counter(); R['drive_backup'] = dict(DRIVE_ERR, dir=DRIVE_DIR)
    tmp = OUT.with_suffix('.json.tmp'); tmp.write_text(json.dumps(R, ensure_ascii=False, indent=1, default=str)); tmp.replace(OUT)
    if DRIVE_DIR is not None and force:
        try:
            for f_ in (LOG, OUT, EVENTS): shutil.copy2(f_, Path(DRIVE_DIR) / f_.name)
        except Exception as e:
            DRIVE_ERR['backup_failures'] += 1; DRIVE_ERR['last'] = '%s: %s' % (type(e).__name__, e)


def ev(kind, **data):
    line = json.dumps(dict(seq=EVSEQ[0], t_s=round(time.perf_counter() - T0, 3), ns=time.monotonic_ns(), kind=kind, **data), default=str, sort_keys=True)
    EVSEQ[0] += 1
    with open(EVENTS, 'a') as f: f.write(line + '\n'); f.flush(); os.fsync(f.fileno())


def check(name, ok, detail=None):
    """Same signature / semantics as the 730/757 check() used by the extracted engine definitions."""
    R['checks'].append({'name': name, 'pass': bool(ok), 'detail': detail}); save(bool(not ok))
    log('PASS' if ok else 'FAIL', name, '' if detail is None else json.dumps(detail, default=str)[:600])
    if not ok: raise RuntimeError('CHECK_FAILED:' + name)


def gate(name, status, reason=None, **data):
    assert status in ('PASS', 'FAIL', 'DIAGNOSTIC'), status
    R['gates'][name] = {'status': status, 'reason': reason, 'data': data}
    if status == 'FAIL' and R['top']['first_failed_gate'] is None: R['top']['first_failed_gate'] = name
    save(); ev('GATE', name=name, status=status, reason=reason)
    log('GATE', name, status, '' if reason is None else '| ' + str(reason)[:1500])
    if status == 'FAIL' and (name in CRITICAL or name.startswith('GATE_REFERENCE')): raise StopT896(name + ': ' + str(reason)[:1500])


def tech(code, **detail):
    R['technical_blockers'].append(dict(code=code, **detail)); ev('TECHNICAL_BLOCKER', code=code, **detail)
    log('TECHNICAL_BLOCKER', code, json.dumps(detail, default=str)[:600])


def ensure_drive():
    if not Path('/content').exists() or Path('/content/drive/MyDrive').exists(): return
    try:
        from google.colab import drive as _gd
        _gd.mount('/content/drive')
    except Exception as e:
        DRIVE_ERR['mount'] = '%s: %s' % (type(e).__name__, e)


def _ver(name):
    try: return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError: return None


def boot_runtime():
    """TEST902 runtime contract. torch is never installed or changed; other pins are installed with a torch constraint only if
    absent and not yet imported. Any difference -> FAIL (stop)."""
    global torch, transformers, accelerate, bitsandbytes, tokenizers, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, DynamicCache, DTYPE, DEV, CUT
    P4 = {p: PINS[p] for p in ('transformers', 'accelerate', 'bitsandbytes', 'tokenizers')}
    rec = {'python': platform.python_version(), 'required': PINS, 'installed_before': {p: _ver(p) for p in list(P4) + ['torch']}}
    ok = '.'.join(platform.python_version().split('.')[:2]) == PINS['python_minor'] and _ver('torch') == PINS['torch']
    if ok:
        need = [p for p, v in P4.items() if _ver(p) != v]
        if need:
            loaded = [p for p in need if p in sys.modules]
            if loaded: gate('GATE_RUNTIME_PINS', 'FAIL', '%s already imported with other versions; restart the runtime' % loaded, **rec)
            con = ROOT.parent / ('TEST903_torch_constraint_%s.txt' % RUN_ID); con.write_text('torch==%s\n' % PINS['torch'])
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', '-c', str(con)] + ['%s==%s' % (p, P4[p]) for p in need])
            importlib.invalidate_caches()
        import torch, transformers, accelerate, bitsandbytes, tokenizers
        from transformers import BitsAndBytesConfig
        from transformers.cache_utils import DynamicCache
        rec['imported'] = {'torch': torch.__version__, 'cuda': torch.version.cuda, 'transformers': transformers.__version__,
                           'accelerate': accelerate.__version__, 'bitsandbytes': bitsandbytes.__version__, 'tokenizers': tokenizers.__version__}
        ok = (torch.__version__ == PINS['torch'] and torch.version.cuda == PINS['cuda'] and
              all(rec['imported'][p] == v for p, v in P4.items()))
    gate('GATE_RUNTIME_PINS', 'PASS' if ok else 'FAIL', None if ok else 'runtime pins not met: required %s | found %s' % (PINS, rec.get('imported') or rec['installed_before']), **rec)
    CUT = 3; DTYPE = torch.bfloat16; DEV = torch.device('cuda:0')
    AutoTokenizer = transformers.AutoTokenizer; AutoModelForCausalLM = transformers.AutoModelForCausalLM


def env_gate():
    env = {'python': platform.python_version(), 'torch': torch.__version__, 'cuda': torch.version.cuda, 'cuda_available': torch.cuda.is_available(),
           'device_count': torch.cuda.device_count(), 'disk_free_gib': round(shutil.disk_usage(str(ROOT)).free / 2**30, 1)}
    if env['cuda_available']:
        pr = torch.cuda.get_device_properties(0)
        env.update(gpu=torch.cuda.get_device_name(0), gpu_bytes=int(pr.total_memory), compute_capability=[pr.major, pr.minor])
    env['transitive'] = {k_: _ver(k_) for k_ in ('huggingface-hub', 'safetensors', 'numpy')}
    R['env'] = env
    ok = (env['cuda_available'] and env['device_count'] == 1 and env.get('gpu') == GPU_NAME_REQ and
          tuple(env.get('compute_capability', ())) == GPU_CC_REQ and env.get('gpu_bytes', 0) >= 79 * 2**30)
    gate('GATE_ENV', 'PASS' if ok else 'FAIL', None if ok else 'requires exactly one %s (cc %s, >= 79 GiB) | found gpu=%r count=%s | Colab: Runtime > '
         'Change runtime type > A100 GPU' % (GPU_NAME_REQ, GPU_CC_REQ, env.get('gpu'), env['device_count']), **env)


# ===================================================================================================== sources (blob-pinned, AST, verbatim)
def obtain_sources(cfg, workdir):
    """Exact bytes of 709/730/757/897/898/899 by git blob id: from --src-dir, or `git cat-file blob` in a blob-less clone."""
    want = dict(ENGINE_BLOBS); want.update(TEST_SOURCES); out = {}
    rd = Path(cfg['repo_dir']) if cfg.get('repo_dir') and Path(cfg['repo_dir']).exists() else Path(workdir).parent / 'TEST903_repo_blobs'
    for name, blob in want.items():
        if cfg.get('src_dir') and (Path(cfg['src_dir']) / name).is_file(): b = (Path(cfg['src_dir']) / name).read_bytes()
        else:
            env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
            if not (rd / '.git').exists() and not (rd / 'HEAD').exists():
                subprocess.run(['git', 'clone', '-q', '--filter=blob:none', '--no-checkout', 'https://github.com/' + SRC_REPO, str(rd)],
                               check=True, capture_output=True, timeout=900, env=env)
            b = subprocess.run(['git', '-C', str(rd), 'cat-file', 'blob', blob], check=True, capture_output=True, timeout=300, env=env).stdout
        if blob_b(b) != blob: raise StopT896('SOURCE_BLOB_MISMATCH %s %s != %s (need the file with this blob)' % (name, blob_b(b), blob))
        if name in ENGINE_SHA256 and sha_b(b) != ENGINE_SHA256[name]: raise StopT896('SOURCE_SHA256_MISMATCH ' + name)
        out[name] = b; (Path(workdir) / name).write_bytes(b)
    return out


REUSE = {
    '897npdm_smoke.py': {'defs': ('contract_npdm', 'query_npdm', 'parse_npdm', 'decision_key_npdm'), 'consts': ('QUERY_TPL_NPDM', 'GRAMMAR_NPDM')},
    '898.py': {'defs': (), 'consts': (), 'nested': ('_cpu_ram_frac', 'guard', 'tok_ids', 'forge_record', 'load_record', 'mount_from', 'gen')},
    '899.py': {'defs': ('gpu_mem', 'sha_bytes', 'sha_path', 'extract_selected', 'MountOff', 'hook_inventory', 'hooks_clean', '_stream', '_qs_items',
                        '_digest_items', 'integrity_digest', 'integrity_selftest', 'hook_selftest', '_PinnedRevision'),
               'consts': ('SELECT', 'FORBIDDEN_TOKENS', 'TOL', 'EXPECTED', 'CHUNK', 'GPU_RESERVE_GIB', 'LOCKS', 'BLK')}}
ENGINE_SELECT_FILES = ('709.py', '730.py', '757.py')
MODEL_BLOCK_ANCHORS = ("    AutoTokenizer, AutoModelForCausalLM = _PinnedRevision(transformers.AutoTokenizer), _PinnedRevision(transformers.AutoModelForCausalLM)\n",
                       "tokenizer_commit_hash=getattr(tok, 'init_kwargs', {}).get('_commit_hash'))\n")
SUFFIX_LITERAL_709 = "suffix='\\nQUESTION:\\n'+question+'\\n\\nANSWER:\\n<|im_end|>\\n<|im_start|>assistant\\n'"
SUFFIX_HEAD = '\nQUESTION:\n'; SUFFIX_TAIL = '\n\nANSWER:\n<|im_end|>\n<|im_start|>assistant\n'
FORBIDDEN_TOKENS_903 = ('register_forward_hook', 'register_forward_pre_hook', 'register_full_backward_hook', 'register_backward_hook',
                        'register_full_backward_pre_hook', 'register_module_forward_hook', 'register_module_forward_pre_hook', 'register_hook(')
# The E-only child mount: the pinned 757 native_append_direct with exactly these substitutions (each must occur exactly once).
# 757 assumes every cartridge starts with the P prefix rows (forge_native forges PIDS+body); an E-only child holds exactly its n
# new rows (p = 0) and its keys carry RoPE phases of the parent positions pos0 .. pos0+n-1. Nothing else changes: H3 injection
# at CUT, prior-row seals, value concatenation, layer count.
APPEND_CHILD_SUBS = (
    ('def native_append_direct(memory,cp,strict_sha=True):', 'def native_append_child_903(memory,cp,strict_sha=True):'),
    ('q=int(cp["n"]-P)', 'q=int(cp["n"])'),
    ('body=cp["h"][:,P:,:]', 'body=cp["h"]'),
    ('oldpos=torch.arange(P+st,P+end,device=DEV)', 'oldpos=torch.arange(int(cp["pos0"])+st,int(cp["pos0"])+end,device=DEV)'),
    ('rephase(k[:,:,P+st:P+end,:],oldpos,newpos)', 'rephase(k[:,:,st:end,:],oldpos,newpos)'),
    ('torch.cat((ov,v[:,:,P:,:]),dim=-2)', 'torch.cat((ov,v),dim=-2)'))


def make_append_child_source(src757):
    seg = [ast.get_source_segment(src757, n) for n in ast.parse(src757).body if isinstance(n, ast.FunctionDef) and n.name == 'native_append_direct']
    if len(seg) != 1: raise StopT896('757_native_append_direct_COUNT %d' % len(seg))
    s = seg[0]
    for a, b in APPEND_CHILD_SUBS:
        if s.count(a) != 1: raise StopT896('APPEND_CHILD_SUBSTITUTION_NOT_UNIQUE %r (%d)' % (a, s.count(a)))
        s = s.replace(a, b)
    if re.search(r'\bP\b', s): raise StopT896('APPEND_CHILD_STILL_READS_P')
    ast.parse(s); return seg[0], s


def ast_defs(src, names, nested=False):
    tree = ast.parse(src); found = {}
    nodes = list(ast.walk(tree)) if nested else tree.body
    for n in nodes:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names and (n.col_offset > 0) == nested:
            found.setdefault(n.name, []).append(textwrap.dedent(ast.get_source_segment(src, n, padded=True)))
    bad = {k: len(found.get(k, [])) for k in names if len(found.get(k, [])) != 1}
    if bad: raise RuntimeError('REUSE_SELECT_COUNT %s' % bad)
    return {k: v[0] for k, v in found.items()}


def const_eval(node):
    ops = {ast.LShift: lambda a, b: a << b, ast.Mult: lambda a, b: a * b, ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b}
    if isinstance(node, ast.BinOp) and type(node.op) in ops:
        a, b = const_eval(node.left), const_eval(node.right)
        if not (isinstance(a, int) and isinstance(b, int)): raise ValueError('CONST_EVAL_NON_INT')
        return ops[type(node.op)](a, b)
    return ast.literal_eval(node)


def ast_consts(src, names):
    out = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in names:
            out.setdefault(n.targets[0].id, []).append((const_eval(n.value), ast.get_source_segment(src, n)))
    bad = {k: len(out.get(k, [])) for k in names if len(out.get(k, [])) != 1}
    if bad: raise RuntimeError('REUSE_CONST_COUNT %s' % bad)
    return {k: v[0] for k, v in out.items()}


def anchored_block(src, a, b):
    if src.count(a) != 1: raise RuntimeError('ANCHOR_NOT_UNIQUE ' + a[:60])
    i = src.index(a); return src[i:src.index(b, i) + len(b)]


RUNTIME_DEFINED = ('tok', 'PREFIX', 'PIDS', 'P', 'model', 'NL', 'H', 'QH', 'KVH', 'HD', 'T_EXP', 'ABORT', 'METRICS', 'CART_INDEX', 'MAX_NEW',
                   'CP_EMPTY', 'PINNED_CALLS', 'torch', 'transformers', 'accelerate', 'bitsandbytes', 'tokenizers', 'AutoTokenizer',
                   'AutoModelForCausalLM', 'BitsAndBytesConfig', 'DynamicCache', 'DTYPE', 'DEV', 'CUT')


def free_globals_missing(segments, ns):
    """Global names read by the extracted segments that exist neither in ns nor among the run-time bindings (symtable)."""
    import symtable, builtins as _b
    have = set(ns) | set(dir(_b)) | set(RUNTIME_DEFINED); out = {}
    for key, src in segments.items():
        top = symtable.symtable(src, key, 'exec'); own = {x.get_name() for x in top.get_symbols() if x.is_assigned() or x.is_imported()}
        reads = set()
        def walk(t):
            for x in t.get_symbols():
                if x.is_referenced() and (x.is_global() or (t.get_type() == 'module' and not x.is_assigned() and not x.is_imported())): reads.add(x.get_name())
            for c in t.get_children(): walk(c)
        walk(top)
        miss = sorted(reads - have - own)
        if miss: out[key] = miss
    return out


def source_extract_gate(SRC):
    """Verbatim reuse (AST) of the pinned helpers and engine definitions + the generated E-only append; free-globals check
    before the model is downloaded."""
    G = {}; ns = globals(); txt = {k: v.decode('utf-8') for k, v in SRC.items()}; table = {}; segs = {}
    for fname, spec in REUSE.items():
        for k, s in list(ast_defs(txt[fname], spec['defs']).items()) + list(ast_defs(txt[fname], spec.get('nested', ()), nested=True).items() if spec.get('nested') else []):
            bad = [t for t in FORBIDDEN_TOKENS_903 if t in s]
            if bad: raise StopT896('HOOK_TOKEN_IN_REUSED_SOURCE %s %s' % (k, bad))
            exec(compile(s, '%s:%s' % (fname, k), 'exec'), ns); table[k] = {'file': fname, 'blob': TEST_SOURCES[fname], 'sha256': sha_s(s)}; segs['%s:%s' % (fname, k)] = s
        for k, (v, s) in ast_consts(txt[fname], spec['consts']).items():
            ns[k] = v; table[k] = {'file': fname, 'blob': TEST_SOURCES[fname], 'sha256': sha_s(s), 'type': 'const'}
    G['forbidden_tokens_equal_899'] = tuple(FORBIDDEN_TOKENS) == FORBIDDEN_TOKENS_903
    sel = {}
    for fname in ENGINE_SELECT_FILES:
        sel[fname] = extract_selected(fname, SRC[fname], SELECT[fname], ns)
        for k, sg in ast_defs(txt[fname], SELECT[fname]).items(): segs['%s:%s' % (fname, k)] = sg
    G['engine_selected_ast_sha16'] = sel; G['engine_locks_equal_899'] = all(LOCKS[f] == ENGINE_BLOBS[f] for f in ENGINE_SELECT_FILES)
    G['engine_selected_equal_902_run'] = sel == ENGINE_AST16_902
    ans = [s for k, s in segs.items() if k == '709.py:answer'][0]
    G['answer_709_suffix_literal'] = SUFFIX_LITERAL_709 in ans and SUFFIX_LITERAL_709 == "suffix='%s'+question+'%s'" % (
        SUFFIX_HEAD.encode('unicode_escape').decode(), SUFFIX_TAIL.encode('unicode_escape').decode())
    G['answer_709_uses_module_MAX_NEW'] = 'range(MAX_NEW)' in ans
    G['forge_native_cache_none'] = 'cache=None' in segs['730.py:forge_native'] and 'register_' not in segs['730.py:forge_native']
    orig, child = make_append_child_source(txt['757.py']); exec(compile(child, '903:native_append_child_903(from 757)', 'exec'), ns)
    X.APPEND_CHILD = {'source_757_sha256': sha_s(orig), 'generated_sha256': sha_s(child), 'substitutions': APPEND_CHILD_SUBS, 'generated': child}
    segs['903:native_append_child_903'] = child
    G['append_child_generated'] = True
    X.MODEL_BLOCK = textwrap.dedent(anchored_block(txt['898.py'], *MODEL_BLOCK_ANCHORS)); segs['898.py:MODEL_block'] = X.MODEL_BLOCK
    G['model_block_verbatim_in_897'] = anchored_block(txt['898.py'], *MODEL_BLOCK_ANCHORS) in txt['897npdm_smoke.py']
    G['chunk_is_128'] = CHUNK == TOL['chunk_expected'] == 128
    for f in ('forge_conditioned_903', 'mount_sealed', 'read_state_from_files'):
        segs['903:' + f] = textwrap.dedent(__import__('inspect').getsource(globals()[f]))
    G['free_globals_missing'] = free_globals_missing(segs, ns); G['reused_definitions_complete'] = not G['free_globals_missing']
    G['read_path_isolation'] = read_path_isolation()
    G['read_path_isolated'] = G['read_path_isolation']['ok']
    R['reuse_table'] = table
    ok = all(v is True for k, v in G.items() if isinstance(v, bool))
    gate('GATE_SOURCE_EXTRACT', 'PASS' if ok else 'FAIL', None if ok else [k for k, v in G.items() if v is False], **G)


ENGINE_AST16_902 = {'709.py': {'pairs': 'fdc12bd780d7aad6', 'cache_build': '3aa928bf9fddac75', 'replace': '5f495837ff405e9c', 'half': '42c7b11eb41aa04b',
                               'rope': '771f8119d421db58', 'rephase': '21ee8f268325ab84', 'sentinel': '988c30adec3d0109', 'free_gpu': 'a5bcfe506b8abadb',
                               'ensure_room': '99c8a53a71bc6b6c', 'kv_digest': 'a340b7220dcc7d4d', 'full_kv_seal': '3d329d4044f10a14', 'answer': '4768c4b580e54a17'},
                    '730.py': {'sha': '1d2eb6c3aabeb16f', 'release': '33a7fd5953088541', 'DirectCut3': '621d55e4bf461276', 'forge_native': '659b2ed3f573231d',
                               'initialize_native': '3b1f7efe39bc5a86', 'to_gpu': 'a5291e98ca25ed56', 'seal_cp': '6a17497cc476f77f'},
                    '757.py': {'native_append_direct': '631f1fabae9fdc51', 'model_setup': '1559c2fb00cd8b1f'}}   # TEST902 run GATE3_SOURCE_EXTRACT
READ_PATH_ALLOWED = {'MountOff', 'initialize_native', 'to_gpu', 'to_gpu_903', 'CP_EMPTY', 'load_record', 'native_append_child_903',
                     'native_append_direct', 'list', 'StopT896', 'mount_sealed', 'full_kv_seal', 'gen_with', 'guard', 'release', 'jsha', 'int', 'len',
                     'METRICS', 'round', 'time', 'dict', 'P'}


def read_path_isolation():
    """The read path (mount_sealed / read_state_from_files) may read no global except the allowed engine functions and the
    shared empty prefix: no parent memory, no raw text, no query history, no manifest, no evaluator, no X namespace."""
    import symtable, inspect
    out = {}
    for f in ('mount_sealed', 'read_state_from_files'):
        src = textwrap.dedent(inspect.getsource(globals()[f])); t = symtable.symtable(src, f, 'exec').get_children()[0]
        g = sorted({x.get_name() for x in t.get_symbols() if x.is_global()}); out[f] = {'globals': g, 'not_allowed': sorted(set(g) - READ_PATH_ALLOWED)}
    out['ok'] = not any(v['not_allowed'] for v in out.values()); return out


# ===================================================================================================== tokenizer / manifest (pre-model)
def obs_segments(A, O):
    return [s.replace('{A}', A).replace('{O}', O) for s in OBS_TPL_903]


def obs_ids(A, O, tk):
    """segment-wise token ids (TEST896-902 record method: each segment tokenized alone and concatenated)."""
    out = []
    for s in obs_segments(A, O): out += list(tk(s, add_special_tokens=False).input_ids)
    return out


def geometry_check(tk):
    """Every observation record has the same token length inside a name set (actions equal length, outcomes equal length),
    so E sits at the same positions after every parent and the gen-2 observation after every C1."""
    G = {}
    for ns, N in NAMES.items():
        la = {N[k]: len(tk(N[k], add_special_tokens=False).input_ids) for k in ('a1', 'a2', 'a3')}
        lo = {N[k]: len(tk(N[k], add_special_tokens=False).input_ids) for k in ('o1', 'o2', 'o3')}
        recs = {'%s->%s' % (a, o): len(obs_ids(a, o, tk)) for a in la for o in lo}
        G[ns] = {'action_name_tokens': la, 'outcome_name_tokens': lo, 'record_tokens': sorted(set(recs.values())),
                 'equal': len(set(recs.values())) == 1}
    G['ok'] = all(G[ns]['equal'] for ns in NAMES); return G


def tokenizer_pre_model_gate():
    """The pinned-revision tokenizer alone (no weights): revision file hashes == TEST902 run, record geometry equal."""
    from huggingface_hub import hf_hub_download
    rf = {}
    for fn in ('config.json', 'tokenizer.json', 'tokenizer_config.json', 'model.safetensors.index.json'):
        pth = hf_hub_download(MODEL_ID, fn, revision=MODEL_REVISION); rf[fn] = sha_path(pth)
    tk = transformers.AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION, trust_remote_code=False)
    geo = geometry_check(tk)
    X.TOK_PRE_IDS = {ns: {'%s->%s' % (a, o): obs_ids(N[a], N[o], tk) for a in ('a1', 'a2', 'a3') for o in ('o1', 'o2', 'o3')} for ns, N in NAMES.items()}
    ok = geo['ok'] and rf == REF902['revision_files']
    gate('GATE_TOKENIZER_PRE_MODEL', 'PASS' if ok else 'FAIL', None if ok else {'geometry_ok': geo['ok'], 'revision_files_equal_902': rf == REF902['revision_files']},
         revision_files=rf, geometry=geo)
    del tk


def manifest_gate():
    man = build_manifest(); b = json.dumps(man, indent=1, sort_keys=True, default=list).encode()
    p = ROOT / 'TEST903_manifest.json'; p.write_bytes(b); X.MAN_SHA = sha_b(b); X.MAN_PATH = p
    sc = man['sample_counts']; ok = sc['gen1_independent_cells'] + sc['gen1_swap_repeat_cells'] + sc['gen2_cells_max_measured'] <= READOUT_LIMIT
    gate('GATE_MANIFEST', 'PASS' if ok else 'FAIL', None if ok else 'readout plan exceeds limit', sha256=X.MAN_SHA, sample_counts=sc,
         written_before_model=True)
    del man                                                                   # the run path never holds expected sets


# ===================================================================================================== GPU: model / engine
def model_gate():
    """The TEST897/898 MODEL block, verbatim (anchored segment of the pinned 898.py, identical in 897)."""
    exec(compile(X.MODEL_BLOCK, '898.py:MODEL_block', 'exec'), globals())


def to_gpu_903(cp):
    """730 to_gpu (which keeps only the 757 keys) + the child's RoPE source position."""
    if int(cp['p']) != 0 or 'pos0' not in cp: raise StopT896('NOT_AN_E_ONLY_CHILD')
    d = to_gpu(cp); d['pos0'] = int(cp['pos0']); return d


def child_schema(cp):
    """757 cartridge schema vs E-only storage, shown explicitly (no parent rows are copied as padding)."""
    n = int(cp['n']); keys757 = {'h', 'lower', 'n', 'p', 'body_tokens', 'book_id'}
    c = {'has_757_keys': keys757 <= set(cp), 'p_is_0': int(cp['p']) == 0, 'pos0_int_ge_P': isinstance(cp.get('pos0'), int) and cp['pos0'] >= P,
         'h_shape_1_n_H': tuple(cp['h'].shape) == (1, n, H), 'body_tokens_eq_n': int(cp['body_tokens']) == n, 'lower_layers_CUT+1': len(cp['lower']) == CUT + 1,
         'lower_rows_eq_n': all(k.shape[-2] == n and v.shape[-2] == n for k, v in cp['lower']),
         'lower_kv_heads_hd': all(tuple(k.shape) == (1, KVH, n, HD) and tuple(v.shape) == (1, KVH, n, HD) for k, v in cp['lower'])}
    c['ok'] = all(c.values())
    c['note'] = ('757 native_append_direct treats rows [0,P) of every cartridge as prefix and RoPE sources as P+st; an E-only child has no '
                 'prefix rows (p=0) and RoPE sources pos0+st, hence native_append_child_903 (6 exact substitutions)')
    return c


def forge_conditioned_903(parent_mem, body_ids, book_id):
    """730 forge_native with the mounted parent instead of cache=None: only the new tokens go through the model, at positions
    oldn..oldn+n-1; H3 (layer CUT output) is captured with the same 730 DirectCut3 method swap (no hook); L0-L3 K/V rows of the
    new tokens are sliced from the grown cache. The parent tensors are cloned into a working cache (read-only parent)."""
    oldn = int(parent_mem[0][0].shape[-2]); n = len(body_ids); h_chunks = []; geo = []
    work = [(k.clone(), v.clone()) for k, v in parent_mem]; cache = cache_build(work); del work
    with DirectCut3(model.model.layers[CUT], 'capture', collector=h_chunks):
        for st in range(0, n, CHUNK):
            piece = body_ids[st:st + CHUNK]; ensure_room(len(piece) + 512); pos = torch.arange(oldn + st, oldn + st + len(piece), device=DEV)
            am = torch.ones((1, oldn + st + len(piece)), device=DEV, dtype=torch.long)
            out = model(input_ids=torch.tensor([piece], device=DEV), past_key_values=cache, attention_mask=am, position_ids=pos.unsqueeze(0),
                        cache_position=pos, use_cache=True, return_dict=True)
            cache = out.past_key_values; del out
            geo.append({'chunk_start': st, 'tokens': len(piece), 'attention_mask_len': int(am.shape[1]), 'position_ids': [int(pos[0]), int(pos[-1])],
                        'cache_position': [int(pos[0]), int(pos[-1])], 'cache_len_after': int(cache.get_seq_length())})
    kv = pairs(cache)
    cp = {'h': torch.cat(h_chunks, dim=1), 'lower': tuple((k[:, :, oldn:, :].detach().cpu().contiguous(), v[:, :, oldn:, :].detach().cpu().contiguous())
                                                         for k, v in kv[:CUT + 1]), 'n': n, 'p': 0, 'pos0': oldn, 'body_tokens': n, 'book_id': book_id}
    ok = tuple(cp['h'].shape) == (1, n, H) and all(k.shape[-2] == n for k, _ in cp['lower']) and int(kv[0][0].shape[-2]) == oldn + n
    del cache, kv; release()
    if not ok: raise StopT896('CONDITIONED_FORGE_SHAPE')
    return cp, {'parent_len': oldn, 'new_tokens': n, 'chunks': geo, 'rope_source_positions': [oldn, oldn + n - 1], 'h_layer': CUT, 'kv_layers': list(range(CUT + 1))}


def mount_sealed(ents):
    """Read state rebuilt ONLY from sealed SSD files: the shared empty prefix + each cartridge (file SHA + tensor seal verified
    by the verbatim 898 load_record). NATIVE -> 757 native_append_direct, CHILD -> native_append_child_903 (rephased once)."""
    with MountOff():
        mem = list(initialize_native(to_gpu(CP_EMPTY)))
        for e in ents:
            cp = load_record(e)
            if e['kind'] == 'CHILD': mem = list(native_append_child_903(list(mem), to_gpu_903(cp), strict_sha=True))
            elif e['kind'] == 'NATIVE': mem = list(native_append_direct(list(mem), to_gpu(cp), strict_sha=True))
            else: raise StopT896('UNKNOWN_CARTRIDGE_KIND')
            del cp
    return mem


def read_state_from_files(ents, q, maxnew):
    """one clean greedy decision: mount from files -> locked 709 answer() (898 gen: the mount must not change) -> release."""
    t_ = time.perf_counter(); mem = mount_sealed(ents); METRICS['append_s'].append(round(time.perf_counter() - t_, 3))
    seal = full_kv_seal(mem); n = int(mem[0][0].shape[-2]); rope = []; at = P
    for e in ents:                                                     # RoPE source -> target rows of every mounted cartridge
        k = int(e['n']) if e['kind'] == 'CHILD' else int(e['body_tokens']); s0 = int(e['pos0']) if e['kind'] == 'CHILD' else P
        rope.append({'cid': e['cid'], 'source': [s0, s0 + k - 1], 'target': [at, at + k - 1], 'rephased': s0 != at}); at += k
    raw, dt = gen_with(mem, q, maxnew); guard('query', dt)
    del mem; release()
    return raw, {'mount_tokens': n, 'mount_tokens_expected': at, 'mount_seal_sha256': jsha(seal), 'query_s': round(dt, 3), 'rope': rope}


def gen_with(mem, q, maxnew):
    g = globals(); old = g['MAX_NEW']; g['MAX_NEW'] = int(maxnew); t_ = time.perf_counter()
    try: raw = gen(mem, q)
    finally: g['MAX_NEW'] = old
    return raw, time.perf_counter() - t_


def save_child(cp, cid, where, meta):
    path = where / ('T903_' + cid + '.pt'); tmp = Path(str(path) + '.tmp')
    if path.exists(): raise StopT896('APPEND_ONLY_VIOLATION ' + str(path))
    torch.save(cp, tmp); tmp.replace(path)
    ent = {'cid': cid, 'file': str(path), 'sha256': sha_path(path), 'tensor_seal': seal_cp(cp), 'n': cp['n'], 'body_tokens': cp['body_tokens'],
           'kind': 'CHILD', 'pos0': int(cp['pos0']), 'role': 'CHILD'}
    ent.update(meta); CART_INDEX.append(ent); ev('CARTRIDGE', entry={k: v for k, v in ent.items() if k != 'tensor_seal'})
    return ent


def first_logits(mem, q):
    """teacher-forced logits of the first answer step (the same suffix tokens as 709 answer); reference DIAGNOSTIC only."""
    ids = tok(SUFFIX_HEAD + q + SUFFIX_TAIL, add_special_tokens=False).input_ids; n = int(mem[0][0].shape[-2]); pos = torch.arange(n, n + len(ids), device=DEV)
    with torch.no_grad():
        out = model(input_ids=torch.tensor([ids], device=DEV), past_key_values=cache_build(mem), attention_mask=torch.ones((1, n + len(ids)), device=DEV, dtype=torch.long),
                    position_ids=pos.unsqueeze(0), cache_position=pos, use_cache=True, return_dict=True)
    lg = out.logits[0, -1, :].float().cpu(); del out; return lg


def tcmp(a, b):
    if tuple(a.shape) != tuple(b.shape): return {'shape_equal': False, 'a': list(a.shape), 'b': list(b.shape), 'cos': -1.0}
    x = a.float().reshape(-1); y = b.float().reshape(-1); d = (x - y).abs()
    return {'shape_equal': True, 'cos': float((x @ y) / (x.norm() * y.norm() + 1e-30)), 'max_abs': float(d.max()), 'rel_l2': float((x - y).norm() / (y.norm() + 1e-30)),
            'bitwise': bool(torch.equal(a, b))}


# ===================================================================================================== physical layer (real; replaced only in CPU tests)
class Phys:
    """The four physical operations of the experiment. CPU tests substitute a toy object with the same methods."""
    def forge_ind(self, ids, cid, where, meta):
        t_ = time.perf_counter(); cp, ent = forge_record(list(ids), cid, None, 'NATIVE', where); dt = time.perf_counter() - t_
        METRICS['forge_s'].append(round(dt, 3)); guard('forge', dt); ent.update(kind='NATIVE', pos0=None, **meta); del cp; release(); return ent

    def forge_child(self, parent_ents, ids, cid, where, meta):
        hk0 = hooks_clean(hook_inventory()); t_ = time.perf_counter()
        parent = mount_sealed(parent_ents); s0 = full_kv_seal(parent)
        cp, geo = forge_conditioned_903(parent, list(ids), 'T903_' + RUN_ID + '_' + cid)
        s1 = full_kv_seal(parent); del parent; release()
        if s1 != s0: raise StopT896('PARENT_CACHE_CHANGED_BY_CONDITIONED_FORGE ' + cid)
        sch = child_schema(cp)
        if not sch['ok']: raise StopT896('CHILD_SCHEMA %s %s' % (cid, sch))
        hk1 = hooks_clean(hook_inventory())
        if not (hk0 and hk1): raise StopT896('HOOK_PRESENT_AROUND_CONDITIONED_FORGE ' + cid)
        ent = save_child(cp, cid, where, dict(meta, geometry=geo, parent_seal_sha256=jsha(s0), parent_seal_unchanged=True, schema_ok=True,
                                              parents=[e['sha256'] for e in parent_ents], ids_sha256=sha_s(json.dumps(list(ids)))))
        dt = time.perf_counter() - t_; METRICS['forge_s'].append(round(dt, 3)); guard('forge', dt); del cp; release(); return ent

    def decide(self, ents, q, maxnew):
        return read_state_from_files(ents, q, maxnew)

    def slot_copy(self, ent, where, cid, label=None):
        """same tensors in a new file / slot; optional identity relabel (sham: book_id and file name of the other trace)."""
        cp = load_record(ent)
        if label is not None: cp['book_id'] = label
        path = where / ('T903_' + cid + '.pt'); tmp = Path(str(path) + '.tmp')
        if path.exists(): raise StopT896('APPEND_ONLY_VIOLATION ' + str(path))
        torch.save(cp, tmp); tmp.replace(path); e2 = dict(ent, cid=cid, file=str(path), sha256=sha_path(path), slot_source=ent['cid'], label=label)
        if seal_cp(cp) != ent['tensor_seal']: raise StopT896('SLOT_COPY_TENSORS_CHANGED')
        CART_INDEX.append(e2); ev('CARTRIDGE', entry={k: v for k, v in e2.items() if k not in ('tensor_seal', 'geometry')}); del cp; return e2


def engine_gate():
    G = {}
    globals()['T_EXP'] = time.perf_counter(); globals()['ABORT'] = dict(ABORT_903); globals()['MAX_NEW'] = MAX_NEW_903
    globals()['METRICS'] = {'forge_s': [], 'append_s': [], 'query_s': []}; globals()['CART_INDEX'] = []
    G['P_is_30'] = P == TOL['P_expected'] == REF902['P']; G['prefix_sha256_equal_902'] = sha_bytes(PREFIX.encode()) == REF902['prefix_sha256']
    G['model_arch'] = (NL, H, QH, KVH, HD) == tuple(EXPECTED) == (80, 8192, 64, 8, 128)
    G['record_ids_equal_pre_model_tokenizer'] = all(obs_ids(N[a], N[o], tok) == X.TOK_PRE_IDS[ns]['%s->%s' % (a, o)]
                                                    for ns, N in NAMES.items() for a in ('a1', 'a2', 'a3') for o in ('o1', 'o2', 'o3'))
    G['stop_set'] = sorted(x for x in {tok.eos_token_id, tok.convert_tokens_to_ids(IM_END)} if x is not None)
    with MountOff(): cpe, _ = forge_native([], 'T903_' + RUN_ID + '_EMPTY')
    (CART_DIR).mkdir(parents=True, exist_ok=True); pe = CART_DIR / 'T903_EMPTY.pt'; torch.save(cpe, pe)
    globals()['CP_EMPTY'] = cpe; G['empty_n_is_P'] = int(cpe['n']) == P; X.EMPTY = {'file': str(pe), 'sha256': sha_path(pe), 'tensor_seal': seal_cp(cpe)}
    # determinism + existing-path equivalence, on NS-A/R0 records (the same records are forged again by the experiment)
    V = variant_names('NS-A', 'R0'); eids = obs_ids(V['a'], V['q'], tok); hids = obs_ids(V['b'], V['r'], tok)
    with MountOff(): c1, _ = forge_native(list(eids), 'DET1'); c2, _ = forge_native(list(eids), 'DET2')
    G['independent_forge_repeat_bitwise'] = seal_cp(c1) == seal_cp(c2); del c1, c2; release()
    where = CART_DIR / '_engine_gate'; where.mkdir(parents=True, exist_ok=True); ph = Phys()
    eh = ph.forge_ind(hids, 'EG_h1', where, {}); ee = ph.forge_ind(eids, 'EG_E', where, {})
    m1 = mount_sealed([eh, ee]); s1 = full_kv_seal(m1); del m1; release()
    m2 = mount_sealed([eh, ee]); s2 = full_kv_seal(m2); del m2; release()
    m3 = mount_from([load_record(eh), load_record(ee)]); s3 = full_kv_seal(m3); del m3; release()
    G['mount_repeat_bitwise'] = s1 == s2; G['mount_sealed_equals_898_mount_from'] = s1 == s3
    ca = ph.forge_child([eh], eids, 'EG_C1a', where, {}); cb = ph.forge_child([eh], eids, 'EG_C1b', where, {})
    G['conditioned_forge_repeat_bitwise_DIAGNOSTIC'] = ca['tensor_seal'] == cb['tensor_seal']
    G['conditioned_differs_from_independent_DIAGNOSTIC'] = ca['tensor_seal'] != ee['tensor_seal']
    m4 = mount_sealed([ca]); G['child_mount_tokens_P_plus_n'] = int(m4[0][0].shape[-2]) == P + len(eids); s4 = full_kv_seal(m4); del m4; release()
    m5 = mount_sealed([ca]); G['child_mount_repeat_bitwise'] = full_kv_seal(m5) == s4; del m5; release()
    G['child_schema'] = child_schema(load_record(ca)); G['child_schema_ok'] = G['child_schema']['ok']
    G['hooks_clean'] = hooks_clean(hook_inventory()); G['gpu_free_gib'] = gpu_mem()['free_gib']; G['vram_preflight'] = G['gpu_free_gib'] >= GPU_RESERVE_GIB
    fail = [k for k, v in G.items() if isinstance(v, bool) and not k.endswith('_DIAGNOSTIC') and v is not True]
    gate('GATE_ENGINE', 'PASS' if not fail else 'FAIL', None if not fail else 'failed: %s' % fail, checks=G)
    X.W0 = {'sentinel': sentinel(), 'integrity': integrity_digest(base_params, Q4MODS, BUFS)}; log('BASE_INTEGRITY', json.dumps(X.W0))


def reference_check(ns, pm, hist, h1_ent, hids, eids, c1_ent, q):
    """Parent open: the trusted full computation (730 forge_native of prefix+h1+E in one pass, E rows sliced) vs the
    incremental conditioned child, for H3, L0-L3 K/V and the first-read logits (parent + child mounted at the same positions)."""
    off = P + len(hids)
    with MountOff(): cpf, _ = forge_native(list(hids) + list(eids), 'REF_FULL')
    c1 = load_record(c1_ent)
    res = {'h3': tcmp(cpf['h'][:, off:, :], c1['h']), 'positions': {'full_E_rows': [off, off + len(eids) - 1], 'child_pos0': c1['pos0']}}
    res['lower_k'] = [tcmp(k[:, :, off:, :], c1['lower'][i][0]) for i, (k, _) in enumerate(cpf['lower'])]
    res['lower_v'] = [tcmp(v[:, :, off:, :], c1['lower'][i][1]) for i, (_, v) in enumerate(cpf['lower'])]
    mf = mount_from([cpf]); lf = first_logits(mf, q); del mf; release()
    par = mount_sealed([h1_ent])
    with MountOff(): mi = list(native_append_child_903(list(par), to_gpu_903(c1), strict_sha=True))
    li = first_logits(mi, q); del par, mi, cpf, c1; release()
    res['first_logits'] = tcmp(lf, li); res['first_logits']['argmax_equal_DIAGNOSTIC'] = int(lf.argmax()) == int(li.argmax())
    res['pass'] = (res['positions']['full_E_rows'][0] == res['positions']['child_pos0'] and res['h3']['cos'] >= TOL903['h3_cos_min'] and
                   all(r['cos'] >= TOL903['lower_k_cos_min'] for r in res['lower_k']) and all(r['cos'] >= TOL903['lower_v_cos_min'] for r in res['lower_v']) and
                   res['first_logits']['cos'] >= TOL903['first_logits_cos_min'])
    res.update(ns=ns, perm=pm, history=hist); return res


# ===================================================================================================== experiment
def parse_903(raw, contract):
    p = parse_npdm(raw, contract, GRAMMAR); return p, decision_key_npdm(p)


def run_cell(ph, cid, arm, ns, pm, order, hist, goal, ents, left, worlds, extra=None, env=None):
    """One greedy readout from sealed files + environment outcome(s). No expected set is available here."""
    if X.NREAD >= READOUT_LIMIT: raise StopT896('READOUT_LIMIT')
    V = variant_names(ns, pm); con = contract_903(ns, order, V[goal]); q = query_npdm(con, left, GRAMMAR)
    raw, mi = ph.decide(ents, q, MAX_NEW_903); X.NREAD += 1
    p, key = parse_903(raw, con); X.TEXTS[sha_s(q)] = q
    if mi.get('mount_tokens') != mi.get('mount_tokens_expected'): tech('MOUNT_TOKENS', cell_id=cid, info=mi)
    envs = {}
    for w, m in worlds.items():
        e = env.clone() if env is not None else Env903(names_world(m, V), V[goal], left)
        envs[w] = e.step(key)
    rec = {'cell_id': cid, 'arm': arm, 'ns': ns, 'perm': pm, 'order': order, 'history': hist, 'goal': goal, 'goal_name': V[goal], 'left': left,
           'trace': [{'cid': e['cid'], 'sha256': e['sha256'], 'kind': e['kind'], 'file': e['file']} for e in ents], 'mount': mi,
           'query_sha256': sha_s(q), 'raw': raw, 'parsed': p, 'valid': p['status'] in ('VALID', 'STOP'), 'decision_key': key if isinstance(key, str) else ' '.join(key),
           'decision_role': role_decision(key, V), 'env': envs, 't_s': round(time.perf_counter() - T0, 1)}
    if extra: rec.update(extra)
    R['cells'].append(rec); ev('READOUT', cell_id=cid, raw=raw, decision=rec['decision_key'], query_sha256=rec['query_sha256'], trace=[t['sha256'] for t in rec['trace']])
    log('READ %-48s %-22s -> %s' % (cid, rec['decision_role'], raw[:60].replace('\n', ' '))); save(False)
    return rec


def run_variant(ph, ns, pm):
    """generation 1 for one identity variant: forge, reference check, clean reads, controls, swap."""
    V = variant_names(ns, pm); where = CART_DIR / ns / pm; where.mkdir(parents=True, exist_ok=True); tag = '%s_%s' % (ns.replace('-', ''), pm)
    eids = obs_ids(V['a'], V['q'], tok); E = {}
    for h, (a, o) in HIST.items(): E['h1', h] = ph.forge_ind(obs_ids(V[a], V[o], tok), tag + '_' + h + '_h1', where, {'record': [a, o], 'history': h})
    E['E'] = ph.forge_ind(eids, tag + '_E_ind', where, {'record': list(E_FACT), 'write_history': 'OFF'})
    for h in HIST:
        E['C1', h] = ph.forge_child([E['h1', h]], eids, tag + '_' + h + '_C1', where, {'record': list(E_FACT), 'history': h, 'generation': 1})
    if getattr(X, 'REFCHECK', True):
        con = contract_903(ns, 'FWD', V['g'])
        refs = [reference_check(ns, pm, h, E['h1', h], obs_ids(V[HIST[h][0]], V[HIST[h][1]], tok), eids, E['C1', h], query_npdm(con, BUDGET, GRAMMAR)) for h in HIST]
        X.REFS += refs
        bad = [r['history'] for r in refs if not r['pass']]
        gate('GATE_REFERENCE_%s_%s' % (ns, pm), 'PASS' if not bad else 'FAIL', None if not bad else '%s/%s failed: %s' % (ns, pm, bad), ns=ns, perm=pm,
             results=[{k: r[k] for k in ('history', 'pass', 'h3', 'first_logits', 'positions')} for r in refs])
    X.ENTS[ns, pm] = E
    for order in ORDERS:
        for g in GOALS:
            for h in HIST:
                run_cell(ph, cid_g1('CLEAN', ns, pm, order, h, g), 'CLEAN', ns, pm, order, h, g, [E['C1', h]], BUDGET, worlds_of(h))
                run_cell(ph, cid_g1('PARENT_ONLY', ns, pm, order, h, g), 'PARENT_ONLY', ns, pm, order, h, g, [E['h1', h]], BUDGET, worlds_of(h))
                run_cell(ph, cid_g1('FULL_REF', ns, pm, order, h, g), 'FULL_REF', ns, pm, order, h, g, [E['h1', h], E['E']], BUDGET, worlds_of(h))
            run_cell(ph, cid_g1('E_IND', ns, pm, order, None, g), 'E_IND', ns, pm, order, None, g, [E['E']], BUDGET, worlds_of(None))
            run_cell(ph, cid_g1('SKIP_APPEND', ns, pm, order, None, g), 'SKIP_APPEND', ns, pm, order, None, g, [], BUDGET, worlds_of(None))
    sd = {s: where / ('slot' + s) for s in 'AB'}
    for d in sd.values(): d.mkdir(exist_ok=True)
    for slot, kind, h in SWAP_CELLS:
        lab = {'H1': 'H2', 'H2': 'H1'}[h] if kind == 'SHAM' else h
        e2 = ph.slot_copy(E['C1', h], sd[slot], '%s_slot%s_%s_%s_as_%s' % (tag, slot, kind, h, lab), label=('T903_%s_%s_C1' % (tag, lab)) if kind == 'SHAM' else None)
        run_cell(ph, cid_swap(ns, pm, slot, kind, h), 'SWAP_' + kind, ns, pm, 'FWD', h, 'g', [e2], BUDGET, worlds_of(h),
                 extra={'slot': slot, 'tensor_history': h, 'label_history': lab, 'repeat_of': cid_g1('CLEAN', ns, pm, 'FWD', h, 'g')})


def run_gen2(ph):
    """H2 / goal g only: the model's own sealed first decision is applied in both hidden completions; separate env and cache per branch."""
    C = {c['cell_id']: c for c in R['cells']}; C2cache = {}
    for ns, pm in VARIANTS:
        V = variant_names(ns, pm); E = X.ENTS[ns, pm]; where = CART_DIR / ns / pm / 'gen2'; where.mkdir(parents=True, exist_ok=True); tag = '%s_%s' % (ns.replace('-', ''), pm)
        inv = {v: k for k, v in V.items()}
        for order in ORDERS:
            first = C[cid_g1('CLEAN', ns, pm, order, 'H2', 'g')]
            for K, m in H2_COMPLETIONS.items():
                env = Env903(names_world(m, V), V['g'], BUDGET); key = first['decision_key']
                k = 'STOP' if key == 'STOP' else 'WASTE' if key == 'WASTE' else tuple(key.split(' ', 1))
                st = env.step(k); br = {'plan_id': 'G2P/%s/%s/%s/%s' % (ns, pm, order, K), 'ns': ns, 'perm': pm, 'order': order, 'completion': K, 'first_cell': first['cell_id'], 'first_decision': first['decision_role'],
                                        'first_step': st}
                if st['event'] != 'ACQUIRE' or env.done:
                    br.update(status='NOT_MEASURED', reason={'ACT': 'FIRST_DECISION_ACT_TERMINAL', 'MODEL_STOP': 'FIRST_DECISION_STOP',
                                                             'INVALID_NOT_REPAIRED': 'FIRST_DECISION_INVALID_NOT_REPAIRED'}.get(st['event'], 'BUDGET_EXHAUSTED'),
                              branch_id='G2B/%s/%s/%s/%s/-' % (ns, pm, order, K))
                    R['gen2_branches'].append(br); ev('GEN2_BRANCH', branch=br); continue
                xn, on = st['obs']; x, o = inv[xn], inv[on]; bid = 'G2B/%s/%s/%s/%s/ACQ_%s' % (ns, pm, order, K, x)
                br.update(status='MEASURED', branch_id=bid, acquired=x, observed=o)
                ids2 = obs_ids(xn, on, tok)
                if (K, x) not in C2cache.setdefault((ns, pm), {}):
                    c2 = ph.forge_child([E['C1', 'H2']], ids2, '%s_%s_ACQ%s_C2' % (tag, K, x), where, {'record': [x, o], 'generation': 2, 'parent': 'C1(H2)'})
                    e2 = ph.forge_ind(ids2, '%s_%s_ACQ%s_e2ind' % (tag, K, x), where, {'record': [x, o], 'write_history': 'OFF'})
                    C2cache[ns, pm][K, x] = (c2, e2)
                c2, e2 = C2cache[ns, pm][K, x]
                for arm, ents in (('C2', [c2]), ('C2_IND', [e2]), ('FULL_REF2', [E['h1', 'H2'], E['E'], e2])):
                    run_cell(ph, cid_g2(arm, ns, pm, order, K, x), arm, ns, pm, order, 'H2', 'g', ents, env.left, {K: m}, env=env,
                             extra={'branch': bid, 'generation': 2})
                br['cells'] = {arm: cid_g2(arm, ns, pm, order, K, x) for arm in G2_ARMS}
                R['gen2_branches'].append(br); ev('GEN2_BRANCH', branch=br)


def run_experiment(ph):
    X.NREAD = 0; X.TEXTS = {}; X.REFS = []; X.ENTS = {}
    for ns, pm in VARIANTS: run_variant(ph, ns, pm)
    s = jsha([(c['cell_id'], c['raw']) for c in R['cells']]); R['first_decisions_sealed_sha256'] = s; ev('FIRST_DECISIONS_SEALED', sha256=s, n=len(R['cells']))
    log('FIRST_DECISIONS_SEALED', s, len(R['cells']))
    run_gen2(ph)
    R['texts'] = X.TEXTS; R['reference_checks'] = X.REFS
    for b in R['gen2_branches']:                                       # the evaluator reads branches through the cell list
        R['cells'].append({'cell_id': 'BRANCH:' + b['branch_id'], 'branch_record': b})
    s2 = jsha([(c['cell_id'], c.get('raw')) for c in R['cells']]); R['generation_sealed_sha256'] = s2; ev('GENERATION_SEALED', sha256=s2)


def offline_evaluation():
    """after GENERATION_SEALED: the manifest is re-read from disk (SHA must equal the pre-model value) and evaluated."""
    b = X.MAN_PATH.read_bytes()
    if sha_b(b) != X.MAN_SHA: raise StopT896('MANIFEST_CHANGED')
    man = json.loads(b); tech_ok = all(g['status'] != 'FAIL' for g in R['gates'].values()) and not R['technical_blockers']
    R['evaluation'] = evaluate(man, R['cells'], tech_ok); R['manifest_sha256'] = X.MAN_SHA
    return man


def end_gates():
    G = {'sentinel_equal': sentinel() == X.W0['sentinel'], 'integrity_equal': integrity_digest(base_params, Q4MODS, BUFS)['sha256'] == X.W0['integrity']['sha256'],
         'hooks_clean': hooks_clean(hook_inventory()), 'cartridge_files_unchanged': all(sha_path(e['file']) == e['sha256'] for e in CART_INDEX),
         'readouts': X.NREAD, 'gpu': gpu_mem()}
    ok = all(v for k, v in G.items() if isinstance(v, bool))
    gate('GATE_END_INTEGRITY', 'PASS' if ok else 'FAIL', None if ok else [k for k, v in G.items() if v is False], **G)


def write_verdict(man):
    e = R['evaluation']; tv = 'PASS' if all(g['status'] != 'FAIL' for g in R['gates'].values()) and not R['technical_blockers'] else 'TECHNICAL_UNDECIDABLE'
    R['technical_verdict'] = tv
    if tv != 'PASS': e['G1_verdict'] = e['G2_verdict'] = 'TECHNICAL_UNDECIDABLE'
    R['top'].update(technical_verdict=tv, G1_verdict=e['G1_verdict'], G2_verdict=e['G2_verdict'], missing_cells=len(e['missing_cells']),
                    gen2_not_measured=e['G2']['not_measured_terminal'], integrity_G1=e['integrity']['G1'], integrity_G2=e['integrity']['G2'],
                    gen2_scope=e['G2']['scope']['text'])
    f = e['families']; c = e['controls']; g2 = e['G2']
    txt = ['TEST903 VERDICT  run %s  (GPU run of 903.py; expected sets from the pre-model manifest %s)' % (RUN_ID, R.get('manifest_sha256')),
           'first_failed_gate: %s | missing cells: %d | gen2 not measured: %s' % (R['top']['first_failed_gate'], len(e['missing_cells']), g2['not_measured_by_reason']),
           'TECHNICAL: %s' % tv, 'GENERATION 1: %s  %s' % (e['G1_verdict'], json.dumps(e['G1_reasons'])),
           '  clean primary (H1/g ACT c, H2/g ACQUIRE b|c): %s (%d/%d units)' % (f['PRIMARY']['pass'], f['PRIMARY']['units_pass'], f['PRIMARY']['units']),
           '  swap (straight/cross/sham): %s' % f['SWAP']['pass'],
           '  same-pattern content (H1/g, HG/g, H1/q, HG/q): %s (%d/%d)' % (f['CONTENT_REPETITION']['pass'], f['CONTENT_REPETITION']['units_pass'], f['CONTENT_REPETITION']['units']),
           '  names/positions: %s by_name_set=%s by_perm=%s by_order=%s' % (f['NAMES_POSITIONS']['pass'], f['NAMES_POSITIONS']['by_name_set'],
                                                                         f['NAMES_POSITIONS']['by_permutation'], f['NAMES_POSITIONS']['by_order']),
           '  goal transfer r (H1/r ACT b, H2/r ACQUIRE b|c): %s (%d/%d)' % (f['TRANSFER_R']['pass'], f['TRANSFER_R']['units_pass'], f['TRANSFER_R']['units']),
           '  controls reproducing the H1/H2 pattern (units of 8): ' + ', '.join('%s=%d' % (k, v['reproduces_pattern_units']) for k, v in c.items()),
           '  FULL_REF failures on required cells: %d' % len(e['reference']['FULL_REF_failures_on_required_cells']),
           'GENERATION 2: %s  measured %d/%d branches, insufficient %d (C2 %s, C2_IND %s, FULL_REF2 %s), sufficient %d (C2 %s), terminal not measured %s' % (
               e['G2_verdict'], g2['branches_measured'], g2['branches_planned'], g2['insufficient_branches'], g2['insufficient']['C2'], g2['insufficient']['C2_IND'],
               g2['insufficient']['FULL_REF2'], g2['sufficient_branches'], g2['sufficient']['C2'], g2['not_measured_terminal']),
           'Recompute: python 903.py --recompute TEST903_results.json'] + integrity_lines(e) + paired_table_lines(e)
    (ROOT / 'TEST903_verdict.txt').write_text('\n'.join(txt) + '\n\n' + decision_table(man, R['cells']) + '\n')
    for l in txt: log(l)
    log(decision_table(man, R['cells']))


# ===================================================================================================== artefacts / entry
def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(4 << 20), b''): h.update(c)
    return h.hexdigest()


_copy_file = shutil.copy2


def drive_copy_verified(src, dst_dir):
    try:
        dst = Path(dst_dir) / Path(src).name; _copy_file(src, dst)
        if sha_file(dst) != sha_file(src): return False, 'READ_BACK_SHA_MISMATCH %s' % dst.name
        return True, None
    except OSError as e:
        return False, '%s: %s' % (type(e).__name__, e)


def capture_self():
    f = globals().get('__file__')
    try:
        if f and Path(f).is_file(): b = Path(f).read_bytes(); return {'file': str(Path(f).resolve()), 'sha256': sha_b(b), 'git_blob': blob_b(b), 'bytes': len(b)}
    except OSError: pass
    return {'file': None}


def finalize_artifacts():
    R['finished_utc'] = datetime.now(timezone.utc).isoformat(); R['elapsed_s'] = round(time.perf_counter() - T0, 1)
    try: save()
    except Exception as e: print('RESULTS_WRITE_FAILED', e)
    AG = {}
    try:
        rep_sha = sha_file(OUT); AG['report_written_read_back'] = json.loads(OUT.read_text())['run_id'] == RUN_ID
        files = sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name != 'SHA256SUMS.txt' and not p.name.endswith('.tmp'))
        (ROOT / 'SHA256SUMS.txt').write_text('\n'.join('%s  %s' % (sha_file(p), p.relative_to(ROOT).as_posix()) for p in files) + '\n')
        zp = ROOT.parent / ('TEST903_SONUC_%s.zip' % RUN_ID)
        with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in files + [ROOT / 'SHA256SUMS.txt']: z.write(p, ROOT.name + '/' + p.relative_to(ROOT).as_posix())
        with zipfile.ZipFile(zp) as z:
            AG['zip_testzip'] = z.testzip() is None
            rows = [l.split('  ', 1) for l in z.read(ROOT.name + '/SHA256SUMS.txt').decode().split('\n') if l]
            AG['sha256sums'] = all(sha_b(z.read(ROOT.name + '/' + rel)) == h for h, rel in rows) and len(rows) == len(files)
            AG['report_in_zip_is_read_back_report'] = sha_b(z.read(ROOT.name + '/' + OUT.name)) == rep_sha
        AG['zip'] = str(zp); AG['zip_sha256'] = sha_file(zp)
        if DRIVE_DIR is not None:
            AG['drive'], err = drive_copy_verified(zp, DRIVE_DIR)
            if err: AG['drive_error'] = err
    except Exception as e:
        AG['artifact_error'] = '%s: %s' % (type(e).__name__, e)
    core = all(AG.get(k) is True for k in ('report_written_read_back', 'zip_testzip', 'sha256sums', 'report_in_zip_is_read_back_report'))
    status = 'FAIL' if not core else ('PASS' if DRIVE_DIR is not None and AG.get('drive') is True else 'LOCAL_ONLY_DRIVE_NOT_COPIED')
    receipt = {'test': TAG, 'run_id': RUN_ID, 'status': R.get('status'), 'top': R.get('top'), 'artifact_status': status, 'artifacts': AG,
               'results_sha256': sha_file(OUT) if AG.get('report_written_read_back') else None}
    rp = ROOT.parent / ('TEST903_SONUC_%s_RECEIPT.json' % RUN_ID); rp.write_text(json.dumps(receipt, indent=1, default=str))
    if DRIVE_DIR is not None and status == 'PASS':
        ok, err = drive_copy_verified(rp, DRIVE_DIR)
        if not ok: receipt.update(artifact_status='LOCAL_ONLY_DRIVE_NOT_COPIED', drive_receipt_error=err); rp.write_text(json.dumps(receipt, indent=1, default=str))
    X.ARTIFACT_STATUS = receipt['artifact_status']
    print('TEST903 ARTIFACTS', json.dumps(receipt, default=str)[:1500]); return receipt


def gpu_main(cfg, workdir):
    global DRIVE_DIR
    R['executed_source'] = capture_self(); R['status'] = 'GPU_GATES'
    boot_runtime(); env_gate()                                              # critical: stops here unless one A100-SXM4-80GB
    if Path('/content/drive/MyDrive').exists():                             # Drive run folder only after GATE_ENV PASS
        DRIVE_DIR = '/content/drive/MyDrive/TEST903_' + RUN_ID; os.makedirs(DRIVE_DIR, exist_ok=True); save(force=True)
    random.seed(20261120); torch.manual_seed(20261120); torch.cuda.manual_seed_all(20261120)
    globals()['PINNED_CALLS'] = []
    SRC = obtain_sources(cfg, workdir); R['sources'] = {n: {'sha256': sha_b(b), 'git_blob': blob_b(b), 'bytes': len(b)} for n, b in SRC.items()}
    source_extract_gate(SRC); R['append_child'] = X.APPEND_CHILD
    tokenizer_pre_model_gate(); manifest_gate()                             # manifest with every expected set BEFORE the model
    model_gate(); engine_gate()
    R['status'] = 'EXPERIMENT'; log('EXPERIMENT START', MARKER)
    run_experiment(Phys())
    end_gates(); man = offline_evaluation(); write_verdict(man); R['status'] = 'COMPLETE'


def main(argv=None):
    cfg = config(sys.argv[1:] if argv is None else argv)
    if cfg.get('recompute'): return recompute(cfg['recompute'])
    ensure_drive(); init_run(cfg)
    log('=' * 112); log(MARKER, '| run', RUN_ID); log('Decision = locked 709 answer() greedy only. P_t = 1. Expected sets: pre-model manifest, offline evaluator.'); log('=' * 112)
    ev('RUN_START', marker=MARKER); workdir = ROOT / 'sources'; workdir.mkdir(); rc = 1
    try:
        gpu_main(cfg, workdir); rc = 0 if R.get('technical_verdict') == 'PASS' else 1
    except StopT896 as e:
        R.update(status='TECHNICAL_ABORT', technical_verdict='TECHNICAL_UNDECIDABLE', abort=str(e)[:3000], traceback=traceback.format_exc())
        R['top'].update(technical_verdict='TECHNICAL_UNDECIDABLE', G1_verdict='TECHNICAL_UNDECIDABLE', G2_verdict='TECHNICAL_UNDECIDABLE')
        if R['top']['first_failed_gate'] is None: R['top']['first_failed_gate'] = 'ABORT: ' + str(e)[:200]
        (ROOT / 'TEST903_traceback.txt').write_text(traceback.format_exc()); log('TEST903_TECHNICAL_ABORT', str(e)[:1500])
    except BaseException as e:
        R.update(status='INTERRUPTED' if isinstance(e, KeyboardInterrupt) else 'ERROR', technical_verdict='TECHNICAL_UNDECIDABLE',
                 error='%s: %s' % (type(e).__name__, str(e)[:2000]), traceback=traceback.format_exc())
        R['top'].update(technical_verdict='TECHNICAL_UNDECIDABLE', G1_verdict='TECHNICAL_UNDECIDABLE', G2_verdict='TECHNICAL_UNDECIDABLE')
        if R['top']['first_failed_gate'] is None: R['top']['first_failed_gate'] = 'ERROR: ' + R['error'][:200]
        (ROOT / 'TEST903_traceback.txt').write_text(traceback.format_exc()); log('TEST903_ERROR', R['error'])
        if isinstance(e, KeyboardInterrupt): finalize_artifacts(); raise
    log(status_line(rc)); finalize_artifacts(); print(status_line(rc), flush=True)
    return rc


def status_line(rc):
    t = R.get('top') or {}
    if rc == 0:
        return 'TEST903 DURUM: CALISTI | TECHNICAL=%s | GEN1=%s | GEN2=%s | READOUTS=%s | DRIVE=%s | RESULTS=%s' % (
            t.get('technical_verdict'), t.get('G1_verdict'), t.get('G2_verdict'), getattr(X, 'NREAD', None), 'PASS' if DRIVE_DIR else 'LOCAL_ONLY', OUT)
    return 'TEST903 DURUM: TEKNIK_HATA | FIRST_GATE=%s | ERROR=%s | LOG=%s' % (t.get('first_failed_gate'), str(R.get('abort') or R.get('error'))[:300], LOG)


def recompute(path):
    """Re-derive every verdict from a results JSON + its run-folder manifest (no model, no torch)."""
    p = Path(path); Rj = json.loads(p.read_text()); mp = p.parent / 'TEST903_manifest.json'; b = mp.read_bytes()
    if Rj.get('manifest_sha256') and sha_b(b) != Rj['manifest_sha256']: print('MANIFEST SHA MISMATCH'); return 1
    man = json.loads(b); tech_ok = Rj.get('technical_verdict') == 'PASS'
    ev_ = evaluate(man, Rj['cells'], tech_ok)
    same = (ev_['G1_verdict'], ev_['G2_verdict']) == ((Rj.get('evaluation') or {}).get('G1_verdict'), (Rj.get('evaluation') or {}).get('G2_verdict'))
    print('RECOMPUTED G1=%s G2=%s | equal to stored: %s' % (ev_['G1_verdict'], ev_['G2_verdict'], same))
    for l in integrity_lines(ev_) + paired_table_lines(ev_): print(l)
    print(decision_table(man, Rj['cells']))
    return 0 if same else 1


if __name__ == '__main__':
    _rc = main(None)
    if _rc and 'get_ipython' not in globals(): sys.exit(_rc)
