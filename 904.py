# =====================================================================================================================
# AKBASCORE SILICON HIPPOCAMPUS — TEST904 — goal-free factual read of TEST903's sealed child cartridges (archive only)
#
# FILE: 904.py (root of ceceli33/titan-cognitive-core-v3, next to the unchanged 903.py). Colab (A100, Drive mounted):
#   !python /content/titan-cognitive-core-v3/904.py
#   (defaults: --archive-dir /content/drive/MyDrive/TEST903_20261120T192235Z ; optional --zip /path/TEST903_SONUC_20261120T192235Z.zip)
#   Offline re-scoring from raw answers (no model, no torch):  python 904.py --recompute TEST904_results.json
# Exit code (never set by the scientific verdict): 0 = complete, technically valid, requested Drive delivery done (or not requested);
#   2 = complete and technically valid but the requested Drive delivery (ZIP or receipt copy + read-back) failed, local results kept;
#   1 = technical abort / technically invalid. --drive auto (default: deliver if MyDrive is mounted) | required | off.
#
# QUESTION. Can frozen Qwen, reading ONLY TEST903's sealed child cartridge C1(H), say which outcome was really observed for
#   action b in the parent history that was open while C1 was written? H1 parent: b->r ; HG parent: b->g ; both children hold
#   the same final event E = a->q. Goal-free query, real names, answer = one outcome name or UNKNOWN.
# PER UNIT (name set x role permutation x outcome order = 8; the order axis re-reads the same 4 cartridge groups): 13 greedy reads
#   straight A<-C1(H1) (r), B<-C1(HG) (g); cross A<-C1(HG) (g), B<-C1(H1) (r); sham A/B = straight tensors under the other history's
#   file name / book_id; positives PARENT_ONLY(H1|HG), FULL_REF(H1|HG) (903 definition: independent parent + independent E);
#   negatives C1(H2), E_IND, SKIP_APPEND -> UNKNOWN. 8 x 13 = 104 reads.
# NOTHING NEW IS WRITTEN: no event, no child, no card. Archived cartridges are opened by file SHA-256 (receipt -> ZIP -> SHA256SUMS
#   -> member) and tensor seal; the read state is the archived empty prefix + selected sealed tensors + the public query; decision =
#   locked 709 answer() (greedy). Every read starts from a fresh mount. Answers are never fed into later queries.
# ENGINE: TEST903's own code, imported (not run) from 903.py blob f883d3dfa4c493bab4e4dc41b5743b30102ebd37 / sha256 97fce064...:
#   runtime pins, A100 gate, blob-pinned 709/730/757/897/898/899 extraction, MODEL block, 757-derived child mount, RoPE rephase,
#   seals, hook inventory, 898 gen -> 709 answer. Importing 903.py does not start its GPU experiment (__main__ guard).
# DIAGNOSTIC ONLY: first answer-token logits s = logit(first token of r name) - logit(first token of g name) on the same mount
#   (mount seal unchanged); valid only if the argmax IS the first generated token id (read from the single tok.decode call of the
#   locked answer() through a transparent tokenizer wrapper); otherwise NOT_EVALUABLE. Never used to decide, repair or score.
# NOT EXECUTED ON GPU BY ITS AUTHOR. CPU tests cover archive resolution, manifest, parser, routing, integrity and verdicts only.
# =====================================================================================================================
import os, sys, json, hashlib, re, time, shutil, subprocess, zipfile, types, traceback, importlib.util, platform, stat
from pathlib import Path
from datetime import datetime, timezone
sys.dont_write_bytecode = True

TAG = 'TEST904'
MARKER = 'AKBASCORE SILICON HIPPOCAMPUS — TEST904 — goal-free factual read of TEST903 child cartridges'
SRC_REPO = 'ceceli33/titan-cognitive-core-v3'
SRC903 = {'file': '903.py', 'commit': '2dbc52688638c4e90616dbcde7ecc73fff975d75', 'git_blob': 'f883d3dfa4c493bab4e4dc41b5743b30102ebd37',
          'sha256': '97fce064f5dafc18455d05ab015b9a476b063c801b7206401afbdfde1bc73ebc'}
RUN903 = {'run_id': '20261120T192235Z',
          'receipt_name': 'TEST903_SONUC_20261120T192235Z_RECEIPT.json',
          'receipt_sha256': 'df711e2d753efd2be68fa128f03dcea35103ae00eafd5476475c0d4bf0012ced',
          'zip_name': 'TEST903_SONUC_20261120T192235Z.zip',
          'zip_sha256': 'dee3dc857c3e4b182e0d0352f093f41f6f30fe31490b6ea354377019a5b03bee',
          'results_sha256': '58caadc77d1f552f0e2590a4150bce9432228984a7f7afb3e359fcc1ffc475b3',
          'events_sha256': 'c616f8f3602568133e2d0e6f83f82006e6a6da8d228831ace7a67efd254f4f65',
          'zip_root': 'TEST903_20261120T192235Z', 'content_root': '/content/TEST903_20261120T192235Z'}
DEFAULT_ARCHIVE_DIR = '/content/drive/MyDrive/TEST903_20261120T192235Z'

VARIANTS = (('NS-A', 'R0'), ('NS-A', 'R1'), ('NS-B', 'R0'), ('NS-B', 'R1'))
ORDERS = ('FWD', 'REV')                                                   # outcome-name order in the query
# the archived objects one cartridge group (ns, perm) needs; 903 cid suffix, kind, history, generation
NEEDED = {'C1_H1': ('_H1_C1', 'CHILD', 'H1'), 'C1_HG': ('_HG_C1', 'CHILD', 'HG'), 'C1_H2': ('_H2_C1', 'CHILD', 'H2'),
          'E_IND': ('_E_ind', 'NATIVE', None), 'h1_H1': ('_H1_h1', 'NATIVE', 'H1'), 'h1_HG': ('_HG_h1', 'NATIVE', 'HG')}
HIST_FACT = {'H1': ('b', 'r'), 'HG': ('b', 'g'), 'H2': ('a', 'q')}; E_FACT = ('a', 'q')
# arm -> (slot, archived source keys in mount order, sham label history, expected answer role)
ARMS = {
    'STRAIGHT_A': ('A', ('C1_H1',), None, 'r'), 'STRAIGHT_B': ('B', ('C1_HG',), None, 'g'),
    'CROSS_A': ('A', ('C1_HG',), None, 'g'), 'CROSS_B': ('B', ('C1_H1',), None, 'r'),
    'SHAM_A': ('A', ('C1_H1',), 'HG', 'r'), 'SHAM_B': ('B', ('C1_HG',), 'H1', 'g'),
    'PARENT_ONLY_H1': ('-', ('h1_H1',), None, 'r'), 'PARENT_ONLY_HG': ('-', ('h1_HG',), None, 'g'),
    'FULL_REF_H1': ('-', ('h1_H1', 'E_IND'), None, 'r'), 'FULL_REF_HG': ('-', ('h1_HG', 'E_IND'), None, 'g'),
    'NEG_C1_H2': ('-', ('C1_H2',), None, 'UNKNOWN'), 'NEG_E_IND': ('-', ('E_IND',), None, 'UNKNOWN'), 'NEG_SKIP_APPEND': ('-', (), None, 'UNKNOWN')}
SWAP_ARMS = ('STRAIGHT_A', 'STRAIGHT_B', 'CROSS_A', 'CROSS_B'); SHAM_ARMS = ('SHAM_A', 'SHAM_B')
POS_ARMS = ('PARENT_ONLY_H1', 'PARENT_ONLY_HG', 'FULL_REF_H1', 'FULL_REF_HG'); NEG_ARMS = ('NEG_C1_H2', 'NEG_E_IND', 'NEG_SKIP_APPEND')
QUERY_TPL_904 = ('The INFORMATION above is your memory of this episode. Which outcome was observed for action {b}? '
                 'Reply with exactly one of {outs}, or UNKNOWN if no outcome for this action was observed.')
MAX_NEW_904 = 25
NORMALIZATION = ('raw = 709 answer() text (already .strip()-ed); norm = raw.strip(); if norm ends with one ".", drop it and strip again; '
                 'norm must then equal exactly (case-sensitive) one of the three public outcome names or UNKNOWN; anything else '
                 '(explanation, two names, other words, empty) is INVALID. The raw text is kept unchanged.')
CRITICAL_904 = ('GATE_SOURCE_903', 'GATE_ARCHIVE', 'GATE_ARCHIVE_TENSORS', 'GATE_TOKENIZER_904', 'GATE_MANIFEST_904', 'GATE_ENGINE_904',
                'GATE_WORK_COPIES', 'GATE_END_904')


def sha_b(b): return hashlib.sha256(b).hexdigest()
def sha_s(s): return sha_b(s.encode('utf-8'))
def blob_b(b): return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()
def canon(v): return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(',', ':'), default=list)
def jsha(v): return sha_s(canon(v))


class Stop904(Exception):
    """technical stop (never a scientific result)."""


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(4 << 20), b''): h.update(c)
    return h.hexdigest()


# ===================================================================================================== pure design layer
def names_of(ns, pm, NAMES, PERMS):
    return {role: NAMES[ns][PERMS[pm][role]] for role in ('a', 'b', 'c', 'g', 'q', 'r')}


def outcome_order(ns, order, NAMES):
    o = [NAMES[ns][k] for k in ('o1', 'o2', 'o3')]
    return o[::-1] if order == 'REV' else o


def query_904(b_name, outs):
    return QUERY_TPL_904.format(b=b_name, outs=', '.join(outs))


def cell_id(ns, pm, order, arm): return 'T904/%s/%s/%s/%s' % (ns, pm, order, arm)


def parse_904(raw, outs):
    norm = (raw or '').strip()
    if norm.endswith('.'): norm = norm[:-1].strip()
    if norm in outs: return {'status': 'NAME', 'answer': norm, 'norm': norm}
    if norm == 'UNKNOWN': return {'status': 'UNKNOWN', 'answer': 'UNKNOWN', 'norm': norm}
    return {'status': 'INVALID', 'answer': None, 'norm': norm}


def answer_role(parsed, outcome_roles):
    if parsed['status'] in ('UNKNOWN', 'INVALID', 'MISSING'): return parsed['status']
    return outcome_roles[parsed['answer']]


# ===================================================================================================== archive resolution (pure)
def resolve_archive(zip_path, receipt_path, pins=RUN903, results_path=None, events_path=None):
    """receipt -> ZIP -> SHA256SUMS -> members -> 903 events / results -> the needed cartridges per (ns, perm), with role identity.
    Any missing, ambiguous or corrupt object -> Stop904 naming the first offending id."""
    A = {'zip': str(zip_path), 'receipt': str(receipt_path)}; rb = Path(receipt_path).read_bytes()
    if sha_b(rb) != pins['receipt_sha256']: raise Stop904('RECEIPT_SHA256 %s != %s' % (sha_b(rb), pins['receipt_sha256']))
    rc = json.loads(rb)
    for k, v in (('run_id', pins['run_id']), ('status', 'COMPLETE'), ('artifact_status', 'PASS'), ('results_sha256', pins['results_sha256'])):
        if rc.get(k) != v: raise Stop904('RECEIPT_FIELD %s=%r (expected %r)' % (k, rc.get(k), v))
    if (rc.get('artifacts') or {}).get('zip_sha256') != pins['zip_sha256']: raise Stop904('RECEIPT_ZIP_SHA256')
    zs = sha_file(zip_path)
    if zs != pins['zip_sha256']: raise Stop904('ZIP_SHA256 %s != %s' % (zs, pins['zip_sha256']))
    A.update(receipt_sha256=sha_b(rb), zip_sha256=zs)
    root = pins['zip_root'] + '/'
    with zipfile.ZipFile(zip_path) as z:
        bad = z.testzip()
        if bad is not None: raise Stop904('ZIP_TESTZIP ' + bad)
        names = [i.filename for i in z.infolist() if not i.is_dir()]
        if len(names) != len(set(names)): raise Stop904('ZIP_DUPLICATE_MEMBER')
        if any(not n.startswith(root) for n in names): raise Stop904('ZIP_FOREIGN_ROOT ' + next(n for n in names if not n.startswith(root)))
        sums_b = z.read(root + 'SHA256SUMS.txt'); sums = {}
        for line in sums_b.decode().splitlines():
            if not line: continue
            h, rel = line.split('  ', 1)
            if rel in sums: raise Stop904('SHA256SUMS_DUPLICATE ' + rel)
            sums[rel] = h
        rels = {n[len(root):] for n in names} - {'SHA256SUMS.txt'}
        if rels != set(sums): raise Stop904('SHA256SUMS_MEMBER_SET first=%s' % sorted(rels ^ set(sums))[0])
        for rel, h in sums.items():
            if sha_b(z.read(root + rel)) != h: raise Stop904('MEMBER_SHA256 ' + rel)
        resb = z.read(root + 'TEST903_results.json'); evb = z.read(root + 'TEST903_events.jsonl')
        manb = z.read(root + 'TEST903_manifest.json')
    if sha_b(resb) != pins['results_sha256']: raise Stop904('RESULTS_SHA256_IN_ZIP')
    A['drive_copies_equal_zip_DIAGNOSTIC'] = {nm: (sha_file(p_) == want) if p_ is not None and Path(p_).is_file() else None
                                              for p_, want, nm in ((results_path, pins['results_sha256'], 'results'), (events_path, sha_b(evb), 'events'))}
    A['events_equal_drive_pin_DIAGNOSTIC'] = sha_b(evb) == pins['events_sha256']
    R3 = json.loads(resb)
    if sha_b(manb) != R3.get('manifest_sha256'): raise Stop904('MANIFEST_SHA256')
    if R3.get('technical_verdict') != 'PASS' or R3.get('status') != 'COMPLETE' or R3.get('run_id') != pins['run_id']: raise Stop904('RESULTS_STATUS')
    A.update(sha256sums_sha256=sha_b(sums_b), members=len(sums), results_sha256=sha_b(resb), events_sha256=sha_b(evb), manifest_sha256=sha_b(manb))
    return A, sums, R3, [json.loads(l) for l in evb.decode().splitlines() if l.strip()]


def map_cartridges(sums, R3, events, pins=RUN903):
    """903 CARTRIDGE ledger -> needed objects; every object: member path, SHA-256, kind, history, generation, ns/perm, 903 reads."""
    led = {}
    for e in events:
        if e.get('kind') != 'CARTRIDGE': continue
        x = e.get('entry', e)
        if x['cid'] in led: raise Stop904('LEDGER_DUPLICATE_CID ' + x['cid'])
        led[x['cid']] = x
    def member(abs_path):
        if not abs_path.startswith(pins['content_root'] + '/'): raise Stop904('CARTRIDGE_PATH_OUTSIDE_RUN ' + abs_path)
        rel = abs_path[len(pins['content_root']) + 1:]
        if rel not in sums: raise Stop904('CARTRIDGE_NOT_IN_ZIP ' + rel)
        return rel
    reads = {}
    cells = [c for c in R3['cells'] if 'raw' in c]
    for c in cells:
        for t in c['trace']: reads[t['sha256']] = reads.get(t['sha256'], 0) + 1
    def cell(arm, ns, pm, h, g='g', order='FWD'):
        k = 'G1/%s/%s/%s/%s/%s/%s' % (arm, ns, pm, order, h or '-', g); hit = [c for c in cells if c['cell_id'] == k]
        if len(hit) != 1: raise Stop904('RESULTS_CELL_%s %s' % ('MISSING' if not hit else 'DUPLICATE', k))
        return hit[0]
    out = {}
    for ns, pm in VARIANTS:
        tag = '%s_%s' % (ns.replace('-', ''), pm); grp = {}
        for key, (suf, kind, hist) in NEEDED.items():
            cid = tag + suf
            if cid not in led: raise Stop904('LEDGER_MISSING ' + cid)
            x = led[cid]; rel = member(x['file'])
            if sums[rel] != x['sha256']: raise Stop904('LEDGER_SHA_NE_SHA256SUMS ' + cid)
            got_kind = 'CHILD' if x.get('role') == 'CHILD' else 'NATIVE'
            if got_kind != kind: raise Stop904('KIND %s %s' % (cid, got_kind))
            if not rel.startswith('cartridges/%s/%s/' % (ns, pm)) or '/slot' in rel or '/gen2/' in rel: raise Stop904('LOCATION ' + cid)
            grp[key] = {'key': key, 'cid': cid, 'member': rel, 'sha256': x['sha256'], 'kind': kind, 'history': hist, 'generation': 1,
                        'ns': ns, 'perm': pm, 'n': x['n'], 'body_tokens': x['body_tokens'], 'pos0': x.get('pos0'), 'ids_sha256': x['ids_sha256'],
                        'parents': x.get('parents'), 'reads_in_903': reads.get(x['sha256'], 0), 'archived_book_id': None}
        for h in ('H1', 'HG', 'H2'):                                       # child identity: parent link, E record, history label
            c1 = led[tag + '_%s_C1' % h]; key = 'C1_' + h
            if c1.get('history') != h or c1.get('record') != list(E_FACT) or c1.get('generation') != 1: raise Stop904('CHILD_META ' + c1['cid'])
            if h in ('H1', 'HG') and c1.get('parents') != [grp['h1_' + h]['sha256']]: raise Stop904('CHILD_PARENT_LINK ' + c1['cid'])
            if c1.get('ids_sha256') != grp['E_IND']['ids_sha256']: raise Stop904('CHILD_E_IDS_NE_E_IND ' + c1['cid'])
            if cell('CLEAN', ns, pm, h)['trace'][0]['sha256'] != grp[key]['sha256']: raise Stop904('RESULTS_CLEAN_TRACE ' + c1['cid'])
        for h in ('H1', 'HG'):                                             # positives exactly as 903 read them
            if [t['sha256'] for t in cell('PARENT_ONLY', ns, pm, h)['trace']] != [grp['h1_' + h]['sha256']]: raise Stop904('RESULTS_PARENT_TRACE %s/%s/%s' % (ns, pm, h))
            if [t['sha256'] for t in cell('FULL_REF', ns, pm, h)['trace']] != [grp['h1_' + h]['sha256'], grp['E_IND']['sha256']]:
                raise Stop904('RESULTS_FULL_REF_TRACE %s/%s/%s' % (ns, pm, h))
        if [t['sha256'] for t in cell('E_IND', ns, pm, None)['trace']] != [grp['E_IND']['sha256']]: raise Stop904('RESULTS_E_IND_TRACE %s/%s' % (ns, pm))
        if cell('SKIP_APPEND', ns, pm, None)['trace'] != []: raise Stop904('RESULTS_SKIP_TRACE %s/%s' % (ns, pm))
        if len({v['sha256'] for v in grp.values()}) != len(grp): raise Stop904('SAME_TENSOR_FILE_TWICE %s/%s' % (ns, pm))
        out[ns, pm] = grp
    if 'cartridges/T903_EMPTY.pt' not in sums: raise Stop904('EMPTY_PREFIX_NOT_IN_ZIP')
    empty = {'key': 'EMPTY', 'member': 'cartridges/T903_EMPTY.pt', 'sha256': sums['cartridges/T903_EMPTY.pt'], 'kind': 'PREFIX'}
    return out, empty


def archive_903_decisions(R3):
    """the 903 task decisions of the same cartridge groups (comparison through the archive only)."""
    out = {}
    for c in R3['cells']:
        if c.get('arm') in ('CLEAN', 'PARENT_ONLY', 'FULL_REF', 'E_IND') and c.get('goal') == 'g' and c.get('order') == 'FWD':
            out.setdefault('%s/%s' % (c['ns'], c['perm']), {})['%s/%s' % (c['arm'], c['history'] or '-')] = c['decision_role']
    return out


# ===================================================================================================== manifest (pure, before the model)
def source_entry(c):
    """what a cell's mount must contain, fixed in the manifest: archive file identity, tensor seal, kind, geometry."""
    return {'key': c['key'], 'cid': c['cid'], 'sha256': c['sha256'], 'tensor_seal_sha256': jsha(c['tensor_seal']), 'kind': c['kind'],
            'history': c['history'], 'n': int(c['n']), 'body_tokens': int(c['body_tokens']), 'pos0': c['pos0']}


def build_manifest(groups, empty, tokinfo, NAMES, PERMS, archive):
    if not (isinstance(empty.get('n'), int) and empty.get('tensor_seal') is not None): raise Stop904('EMPTY_PREFIX_GEOMETRY_UNBOUND')
    empty = dict(empty, tensor_seal_sha256=jsha(empty['tensor_seal']))
    cells = {}; units = {}
    for ns, pm in VARIANTS:
        V = names_of(ns, pm, NAMES, PERMS)
        for order in ORDERS:
            outs = outcome_order(ns, order, NAMES); q = query_904(V['b'], outs); u = '%s/%s/%s' % (ns, pm, order)
            fr, fg = tokinfo['first_token'][V['r']], tokinfo['first_token'][V['g']]
            units[u] = {'ns': ns, 'perm': pm, 'order': order, 'b_name': V['b'], 'outcome_order': outs, 'query': q, 'query_sha256': sha_s(q),
                        'query_token_ids_sha256': tokinfo['query_ids_sha256'].get(sha_s(q)), 'r_name': V['r'], 'g_name': V['g'],
                        'diag_first_token_r': fr, 'diag_first_token_g': fg, 'diag_evaluable': fr != fg,
                        'cartridge_group': '%s/%s' % (ns, pm), 'outcome_roles': {V[k]: k for k in ('g', 'q', 'r')}}
            for arm, (slot, keys, lab, exp) in ARMS.items():
                cells[cell_id(ns, pm, order, arm)] = {
                    'unit': u, 'ns': ns, 'perm': pm, 'order': order, 'arm': arm, 'slot': slot, 'label_history': lab,
                    'tensor_sources': [source_entry(groups[ns, pm][k]) for k in keys],
                    'query_sha256': sha_s(q), 'expected_role': exp, 'expected_answer': 'UNKNOWN' if exp == 'UNKNOWN' else V[exp]}
    return {'test': TAG, 'marker': MARKER, 'archive': archive, 'empty_prefix': empty,
            'cartridges': {'%s/%s/%s' % (ns, pm, k): v for (ns, pm), g in groups.items() for k, v in g.items()},
            'units': units, 'cells': cells, 'n_cells': len(cells), 'reads_planned': len(cells),
            'design': {'arms': {a: {'slot': s, 'sources': list(k), 'sham_label_history': l, 'expected_role': e} for a, (s, k, l, e) in ARMS.items()},
                       'query_template': QUERY_TPL_904, 'max_new': MAX_NEW_904, 'normalization': NORMALIZATION,
                       'answer_token_feasibility': tokinfo['answers'], 'histories': HIST_FACT, 'E': E_FACT,
                       'note_order_axis': 'FWD/REV re-read the same 4 cartridge groups; 8 units are not 8 independent learning events'},
            'verdict_rules': VERDICT_RULES_904}


VERDICT_RULES_904 = {
    'cell_ok': 'parse_904(raw) answer role == expected_role (INVALID is never repaired)',
    'unit_columns': 'technical integrity; positives correct (k/4); negatives UNKNOWN (k/3); straight pair (A=r AND B=g); cross pair '
                    '(A=g AND B=r); sham A/B raw answers equal to their straight sources; unit interpretation',
    'unit_interpretation': 'TECHNICAL_UNDECIDABLE if any of its 13 records is missing / duplicated / contradictory or the run is '
                           'technically invalid; else PROBE_NOT_WORKING_FROM_FULL_HISTORY if a positive fails; else '
                           'ATTRIBUTION_OPEN_UNKNOWN_BEHAVIOUR if a negative is not UNKNOWN; else ATTRIBUTION_OPEN_SHAM_UNSTABLE if a '
                           'sham answer differs from its straight source; else CONTROLLED_FACTUAL_READ_SUPPORTED if straight AND cross '
                           'pairs are both right; else NO_READABILITY_SUPPORT (one correct side of a pair is not a pair success)',
    'overall': 'TECHNICAL_UNDECIDABLE if any record integrity problem or technical failure; else with e = units passing every control '
               'and k = CONTROLLED_FACTUAL_READ_SUPPORTED units: e = 0 -> UNDECIDABLE_NO_EVALUABLE_UNIT; k = 8 -> FULL_COVERAGE_SUPPORT; '
               'k >= 1 -> PARTIAL_SUPPORT[k/8 supported, e/8 evaluable]; k = 0 -> NO_READABILITY_SUPPORT[e/8 evaluable]. All 8 '
               'units are always reported; no subgroup selection.',
    'diagnostic': 's = logit(first token of r name) - logit(first token of g name) at the first answer step; d_straight = s(A,H1) - '
                  's(B,HG), d_cross = s(B,H1) - s(A,HG). NOT_EVALUABLE if the two first tokens coincide or the measured argmax is not '
                  'the first generated token id (exact id comparison; text prefixes are not evidence). SUBTHRESHOLD_SENSITIVITY if the '
                  'pair answers fail but d_straight > 0 and d_cross > 0. Never used to change a greedy answer.',
    'record_integrity': 'evaluate and --recompute: every manifest cell exactly once; required typed fields; trace bound to the '
                        'manifest (archive file SHA, tensor seal, kind, history; sham: other working-file SHA, same tensor seal); '
                        'mount length and RoPE placement re-derived from archived geometry; mount seal required and identical for '
                        'identical mounted tensors; completed run: manifest SHA and generation seal required and re-computed; stored '
                        'cell / unit results re-computed. Any problem -> TECHNICAL_UNDECIDABLE with the offending ids.',
    'states': 'technical verdict, scientific verdict and Drive delivery status are separate; a delivery failure never changes a verdict',
    'scope': 'a positive result shows accessibility of the old observation under this query; it does not show that the 903 task '
             'policy accessed and ignored it. A negative result alone does not separate loss at write from inaccessibility at clean '
             'mount. P_t effects, general learning and autonomous decision success are outside TEST904.'}


# ===================================================================================================== offline evaluation (pure)
HEX64 = re.compile(r'^[0-9a-f]{64}$')
REC_STR = ('cell_id', 'unit', 'ns', 'perm', 'order', 'arm', 'slot', 'query_sha256', 'raw')


def expected_geometry(man, srcs):
    """mount length and RoPE placement derived ONLY from the manifest (archived prefix + archived cartridge geometry, in order)."""
    at = man['empty_prefix']['n']; rope = []
    for t in srcs:
        k = t['n'] if t['kind'] == 'CHILD' else t['body_tokens']; s0 = t['pos0'] if t['kind'] == 'CHILD' else man['empty_prefix']['n']
        rope.append({'cid': t['cid'], 'source_pos0': s0, 'target_pos0': at}); at += k
    return at, rope


def integrity_904(man, cells):
    """(problem, cell_id) pairs. Every evidence field is required with its type and bound to the manifest: file identity, tensor
    seal, kind, history, slot, query, mount length and RoPE placement (re-derived from archive geometry), mount seal. Sham:
    a different working-file SHA but the source tensor seal. Same mounted tensors -> same mount seal everywhere."""
    prob = []; cnt = {}; recs = {}; seal_by_mount = {}
    archive_files = {c['sha256'] for c in man['cartridges'].values()}
    for c in cells:
        k = c.get('cell_id') if isinstance(c, dict) else None; cnt[k] = cnt.get(k, 0) + 1; recs[k] = c
    for k, n in cnt.items():
        if k not in man['cells']: prob.append(('UNKNOWN_CELL', k)); continue
        if n != 1: prob.append(('DUPLICATE_CELL(x%d)' % n, k))
        m = man['cells'][k]; r = recs[k]; bad = []
        bad += ['type:' + f for f in REC_STR if not isinstance(r.get(f), str)]
        if not (r.get('label_history') is None or isinstance(r.get('label_history'), str)): bad.append('type:label_history')
        bad += [f for f in ('unit', 'ns', 'perm', 'order', 'arm', 'slot', 'label_history', 'query_sha256') if r.get(f) != m.get(f)]
        tr = r.get('trace'); src = m['tensor_sources']
        if not isinstance(tr, list) or len(tr) != len(src) or not all(isinstance(t, dict) for t in tr): bad.append('trace'); tr = None
        if tr is not None:
            for i_, (t, s_) in enumerate(zip(tr, src)):
                for f in ('cid', 'kind', 'history'):
                    if t.get(f) != s_[f]: bad.append('trace[%d].%s' % (i_, f))
                if t.get('source_sha256') != s_['sha256']: bad.append('trace[%d].source_sha256' % i_)
                if t.get('tensor_seal_sha256') != s_['tensor_seal_sha256']: bad.append('trace[%d].tensor_seal' % i_)
                if not isinstance(t.get('sha256'), str) or not HEX64.match(t['sha256']): bad.append('trace[%d].sha256' % i_)
                elif m['arm'] in SHAM_ARMS:
                    if t['sha256'] in archive_files: bad.append('trace[%d].sham_file_is_an_archive_file' % i_)
                elif t['sha256'] != s_['sha256']: bad.append('trace[%d].file_sha_ne_archive' % i_)
        mt = r.get('mount')
        if not isinstance(mt, dict): bad.append('mount')
        else:
            want_n, want_rope = expected_geometry(man, src)
            if not isinstance(mt.get('mount_tokens'), int) or isinstance(mt.get('mount_tokens'), bool): bad.append('type:mount_tokens')
            elif mt['mount_tokens'] != want_n: bad.append('mount_tokens_ne_archive_geometry')
            if mt.get('rope') != want_rope: bad.append('rope_placement')
            ms = mt.get('mount_seal_sha256')
            if not isinstance(ms, str) or not HEX64.match(ms): bad.append('mount_seal')
            else: seal_by_mount.setdefault(tuple(t['tensor_seal_sha256'] for t in src), {}).setdefault(ms, []).append(k)
        if bad: prob.append(('CONTRADICTORY_CELL%s' % bad, k))
    for key, seals in seal_by_mount.items():                              # identical mounted tensors -> identical mount seal
        if len(seals) > 1:
            minority = sorted(seals.items(), key=lambda kv: (len(kv[1]), kv[0]))[:-1]
            for _, ks in minority:
                for k in ks: prob.append(('MOUNT_SEAL_DIFFERS_FOR_SAME_TENSORS', k))
    for k in man['cells']:
        if k not in cnt: prob.append(('MISSING_CELL', k))
    return sorted(set(prob), key=str)


def generation_seal(cells):
    return jsha([(c.get('cell_id'), c.get('raw')) for c in cells])


def verify_run_record(Rj, man_bytes, ev):
    """a stored run against its own manifest and recomputation: manifest SHA and generation seal required for a completed run;
    recomputed cell and unit results must equal the stored ones (id of every difference)."""
    out = []
    if Rj.get('status') == 'COMPLETE':
        if not Rj.get('manifest_sha256'): out.append('MANIFEST_SHA_MISSING')
        if not Rj.get('generation_sealed_sha256'): out.append('GENERATION_SEAL_MISSING')
    if Rj.get('manifest_sha256') and Rj['manifest_sha256'] != sha_b(man_bytes): out.append('MANIFEST_SHA_MISMATCH')
    if Rj.get('generation_sealed_sha256') and Rj['generation_sealed_sha256'] != generation_seal(Rj.get('cells') or []): out.append('GENERATION_SEAL_MISMATCH')
    st = Rj.get('evaluation') or {}
    if st:
        a = {c['cell_id']: c for c in st.get('scored_cells', [])}; b = {c['cell_id']: c for c in ev['scored_cells']}
        out += ['STORED_CELL_RESULT_DIFFERS:' + k for k in sorted(set(a) | set(b)) if canon(a.get(k)) != canon(b.get(k))]
        ua = {u['unit']: u for u in st.get('units', [])}; ub = {u['unit']: u for u in ev['units']}
        out += ['STORED_UNIT_RESULT_DIFFERS:' + k for k in sorted(set(ua) | set(ub)) if canon(ua.get(k)) != canon(ub.get(k))]
        if st.get('verdict') != ev['verdict']: out.append('STORED_VERDICT_DIFFERS')
        if canon(st.get('counts')) != canon(ev['counts']): out.append('STORED_COUNTS_DIFFER')
    return out


def evaluate_904(man, cells, technical_ok):
    """every count and verdict from the manifest + raw answers only (parsing is redone here)."""
    probs = integrity_904(man, cells); C = {c['cell_id']: c for c in cells}; units = []; scored = []
    bad_units = {man['cells'][k]['unit'] for _, k in probs if k in man['cells']}
    for u, U in man['units'].items():
        row = {'unit': u, 'cartridge_group': U['cartridge_group']}; res = {}
        for arm in ARMS:
            k = cell_id(U['ns'], U['perm'], U['order'], arm); r = C.get(k); m = man['cells'][k]
            p = parse_904(r['raw'], U['outcome_order']) if r and 'raw' in r else {'status': 'MISSING', 'answer': None, 'norm': None}
            role = answer_role(p, U['outcome_roles'])
            res[arm] = {'raw': r and r.get('raw'), 'parsed': p, 'role': role, 'expected_role': m['expected_role'], 'ok': role == m['expected_role']}
            scored.append(dict(cell_id=k, **res[arm]))
        tech = technical_ok and u not in bad_units
        pos = sum(res[a]['ok'] for a in POS_ARMS); neg = sum(res[a]['role'] == 'UNKNOWN' for a in NEG_ARMS)
        straight = res['STRAIGHT_A']['ok'] and res['STRAIGHT_B']['ok']; cross = res['CROSS_A']['ok'] and res['CROSS_B']['ok']
        sham = res['SHAM_A']['raw'] == res['STRAIGHT_A']['raw'] and res['SHAM_B']['raw'] == res['STRAIGHT_B']['raw']
        if not tech: interp = 'TECHNICAL_UNDECIDABLE'
        elif pos < 4: interp = 'PROBE_NOT_WORKING_FROM_FULL_HISTORY'
        elif neg < 3: interp = 'ATTRIBUTION_OPEN_UNKNOWN_BEHAVIOUR'
        elif not sham: interp = 'ATTRIBUTION_OPEN_SHAM_UNSTABLE'
        elif straight and cross: interp = 'CONTROLLED_FACTUAL_READ_SUPPORTED'
        else: interp = 'NO_READABILITY_SUPPORT'
        row.update(technical_complete=tech, positives_ok=pos, negatives_unknown=neg, straight_pair=straight, cross_pair=cross, sham_stable=sham,
                   one_side_only={'straight': res['STRAIGHT_A']['ok'] != res['STRAIGHT_B']['ok'], 'cross': res['CROSS_A']['ok'] != res['CROSS_B']['ok']},
                   negatives_named=[a for a in NEG_ARMS if res[a]['role'] not in ('UNKNOWN',)], interpretation=interp,
                   answers={a: res[a]['role'] for a in ARMS}, diagnostic=diag_unit(man, U, C, straight and cross))
        units.append(row)
    n = len(units); tc = sum(r['technical_complete'] for r in units)
    pp = sum(r['technical_complete'] and r['positives_ok'] == 4 for r in units); npass = sum(r['technical_complete'] and r['negatives_unknown'] == 3 for r in units)
    allc = sum(r['technical_complete'] and r['positives_ok'] == 4 and r['negatives_unknown'] == 3 and r['sham_stable'] for r in units)
    k = sum(r['interpretation'] == 'CONTROLLED_FACTUAL_READ_SUPPORTED' for r in units)
    if probs or not technical_ok: v = 'TECHNICAL_UNDECIDABLE'
    elif allc == 0: v = 'UNDECIDABLE_NO_EVALUABLE_UNIT'
    elif k == n: v = 'FULL_COVERAGE_SUPPORT'
    elif k >= 1: v = 'PARTIAL_SUPPORT[%d/%d supported, %d/%d evaluable]' % (k, n, allc, n)
    else: v = 'NO_READABILITY_SUPPORT[%d/%d evaluable]' % (allc, n)
    groups = {}
    for r in units: groups.setdefault(r['cartridge_group'], []).append(r['interpretation'])
    return {'verdict': v, 'integrity_problems': ['%s:%s' % pk for pk in probs], 'units': units, 'scored_cells': scored,
            'counts': {'units': n, 'technical_complete': tc, 'positives_pass': pp, 'negatives_pass': npass, 'all_controls_pass': allc,
                       'controlled_pair_success': k, 'fractions': {'supported': '%d/%d' % (k, n), 'evaluable': '%d/%d' % (allc, n),
                                                                   'positives': '%d/%d' % (pp, n), 'negatives': '%d/%d' % (npass, n)}},
            'by_cartridge_group': groups}


def diag_unit(man, U, C, pair_ok):
    out = {'evaluable': U['diag_evaluable']}
    if not U['diag_evaluable']: out['status'] = 'NOT_EVALUABLE_FIRST_TOKENS_COINCIDE'; return out
    s = {}
    for arm in ARMS:
        r = C.get(cell_id(U['ns'], U['perm'], U['order'], arm)); d = (r or {}).get('diag') or {}
        lg = d.get('logits') or {}
        if d.get('status') != 'VERIFIED' or str(U['diag_first_token_r']) not in lg or str(U['diag_first_token_g']) not in lg: s[arm] = None; continue
        s[arm] = lg[str(U['diag_first_token_r'])] - lg[str(U['diag_first_token_g'])]
    out['s'] = s
    if any(s[a] is None for a in SWAP_ARMS): out['status'] = 'NOT_EVALUABLE_MEASUREMENT'; return out
    ds = s['STRAIGHT_A'] - s['STRAIGHT_B']; dc = s['CROSS_B'] - s['CROSS_A']
    out.update(status='EVALUATED', d_straight=ds, d_cross=dc, consistent_sign=(ds > 0) == (dc > 0),
               same_tensor_equal={'H1': s['STRAIGHT_A'] == s['CROSS_B'], 'HG': s['STRAIGHT_B'] == s['CROSS_A']},
               d_parent=None if s['PARENT_ONLY_H1'] is None or s['PARENT_ONLY_HG'] is None else s['PARENT_ONLY_H1'] - s['PARENT_ONLY_HG'],
               d_full=None if s['FULL_REF_H1'] is None or s['FULL_REF_HG'] is None else s['FULL_REF_H1'] - s['FULL_REF_HG'],
               subthreshold_sensitivity=(not pair_ok) and ds > 0 and dc > 0)
    return out


def report_lines(ev, man, a903=None):
    c = ev['counts']; L = ['TEST904 VERDICT: %s' % ev['verdict'],
                           'units %d | technical complete %d | positives pass %d | negatives pass %d | all controls pass %d | controlled pair success %d' % (
                               c['units'], c['technical_complete'], c['positives_pass'], c['negatives_pass'], c['all_controls_pass'], c['controlled_pair_success'])]
    if ev['integrity_problems']: L.append('INTEGRITY FAIL: ' + '; '.join(ev['integrity_problems'][:20]))
    L.append('%-16s %-4s %-5s %-5s %-6s %-6s %-5s %-36s %s' % ('unit', 'tech', 'pos', 'neg', 'str', 'cross', 'sham', 'interpretation', 'answers A/B straight | cross | diag d_str d_cross'))
    for r in ev['units']:
        a = r['answers']; d = r['diagnostic']
        dg = ('%.3f %.3f%s' % (d['d_straight'], d['d_cross'], ' SUBTHRESHOLD' if d.get('subthreshold_sensitivity') else '')) if d.get('status') == 'EVALUATED' else d.get('status')
        L.append('%-16s %-4s %d/4   %d/3   %-6s %-6s %-5s %-36s %s/%s | %s/%s | %s' % (
            r['unit'], 'ok' if r['technical_complete'] else 'X', r['positives_ok'], r['negatives_unknown'], r['straight_pair'], r['cross_pair'], r['sham_stable'],
            r['interpretation'], a['STRAIGHT_A'], a['STRAIGHT_B'], a['CROSS_A'], a['CROSS_B'], dg))
    L.append('negatives answering a name / INVALID (per unit): ' + ('; '.join('%s:%s' % (r['unit'], r['negatives_named']) for r in ev['units'] if r['negatives_named']) or 'none'))
    if a903:
        L.append('903 archive, same cartridge groups, goal g FWD task decisions (CLEAN H1 / CLEAN HG / FULL_REF H1 / FULL_REF HG):')
        for g, d in sorted(a903.items()): L.append('  %s: %s / %s / %s / %s' % (g, d.get('CLEAN/H1'), d.get('CLEAN/HG'), d.get('FULL_REF/H1'), d.get('FULL_REF/HG')))
    return L


# ===================================================================================================== run infrastructure (TEST903 engine host)
X = types.SimpleNamespace(); M3 = None; RUN_ID = ROOT = LOG = OUT = EVENTS = None; R = None; DRIVE_DIR = None; T0 = time.perf_counter()


def config(argv):
    import argparse
    ap = argparse.ArgumentParser(add_help=False)
    d = {'out_root': '/content' if Path('/content').exists() else '/tmp', 'src_dir': '', 'archive_dir': DEFAULT_ARCHIVE_DIR, 'zip': '', 'receipt': '',
         'repo_dir': '/content/titan-cognitive-core-v3' if Path('/content').exists() else '', 'recompute': '', 'drive': 'auto'}
    for k, v in d.items(): ap.add_argument('--' + k.replace('_', '-'), default=os.environ.get('T904_' + k.upper(), v))
    a, _ = ap.parse_known_args(list(argv)); return {k: getattr(a, k) for k in d}


def fetch_903_source(cfg, work):
    """903.py bytes with the pinned blob: --src-dir, the repo checkout, or `git cat-file blob` (blob-less clone if needed)."""
    cands = []
    if cfg.get('src_dir'): cands.append(Path(cfg['src_dir']) / '903.py')
    if cfg.get('repo_dir'): cands.append(Path(cfg['repo_dir']) / '903.py')
    for p in cands:
        if p.is_file() and blob_b(p.read_bytes()) == SRC903['git_blob']: b = p.read_bytes(); break
    else:
        rd = Path(cfg['repo_dir']) if cfg.get('repo_dir') and Path(cfg['repo_dir']).exists() else Path(work).parent / 'TEST904_repo_blobs'
        env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
        if not (rd / '.git').exists() and not (rd / 'HEAD').exists():
            subprocess.run(['git', 'clone', '-q', '--filter=blob:none', '--no-checkout', 'https://github.com/' + SRC_REPO, str(rd)], check=True, capture_output=True, timeout=900, env=env)
        b = subprocess.run(['git', '-C', str(rd), 'cat-file', 'blob', SRC903['git_blob']], check=True, capture_output=True, timeout=300, env=env).stdout
    if blob_b(b) != SRC903['git_blob'] or sha_b(b) != SRC903['sha256']: raise Stop904('903_SOURCE_IDENTITY')
    p = Path(work) / '903.py'; p.write_bytes(b); return p


def load_903(path):
    """import 903.py as a module: its __main__ block is not executed, so no 903 GPU experiment starts."""
    spec = importlib.util.spec_from_file_location('akbas_test903_engine', str(path)); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if not hasattr(m, 'main') or m.TAG != 'TEST903' or m.RUN_ID is not None: raise Stop904('903_MODULE_STATE')
    return m


def init_run(cfg):
    global RUN_ID, ROOT, LOG, OUT, EVENTS, R
    RUN_ID = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    ROOT = Path(cfg['out_root']) / ('TEST904_' + RUN_ID); ROOT.mkdir(parents=True, exist_ok=False)
    LOG = ROOT / 'TEST904.log'; OUT = ROOT / 'TEST904_results.json'; EVENTS = ROOT / 'TEST904_events.jsonl'
    for f in (LOG, EVENTS): f.write_text('')
    R = {'test': TAG, 'marker': MARKER, 'run_id': RUN_ID, 'status': 'STARTED', 'executed_by_author': False,
         'top': {'first_failed_gate': None, 'technical_verdict': None, 'verdict': None, 'counts': None},
         'source_903': SRC903, 'run_903': RUN903, 'gates': {}, 'checks': [], 'technical_blockers': [], 'config': dict(cfg), 'cells': []}


def bind_903(m):
    """TEST903's run infrastructure writes into TEST904's files and result dict."""
    m.RUN_ID = RUN_ID; m.ROOT = ROOT; m.LOG = LOG; m.OUT = OUT; m.EVENTS = EVENTS; m.CART_DIR = ROOT / 'work'; m.R = R; m.EVSEQ = [0]
    m.CRITICAL = tuple(m.CRITICAL) + CRITICAL_904


def log(*a): M3.log(*a)
def gate(*a, **k): M3.gate(*a, **k)


def archive_paths(cfg):
    ad = Path(cfg['archive_dir']) if cfg.get('archive_dir') else None
    zp = Path(cfg['zip']) if cfg.get('zip') else (ad / RUN903['zip_name'] if ad else None)
    rp = Path(cfg['receipt']) if cfg.get('receipt') else ((ad / RUN903['receipt_name']) if ad and (ad / RUN903['receipt_name']).is_file() else zp.parent / RUN903['receipt_name'])
    res = (ad / 'TEST903_results.json') if ad else None; evp = (ad / 'TEST903_events.jsonl') if ad else None
    return zp, rp, res, evp


def archive_gate(cfg):
    zp, rp, res, evp = archive_paths(cfg)
    if zp is None or not zp.is_file(): raise Stop904('ZIP_NOT_FOUND %s' % zp)
    if not rp.is_file(): raise Stop904('RECEIPT_NOT_FOUND %s' % rp)
    A, sums, R3, events = resolve_archive(zp, rp, RUN903, res, evp)
    groups, empty = map_cartridges(sums, R3, events)
    ro = ROOT / 'archive_ro'; root = RUN903['zip_root'] + '/'
    with zipfile.ZipFile(zp) as z:                                       # read-only extraction of exactly the needed members
        for ent in [empty] + [v for g in groups.values() for v in g.values()]:
            dst = ro / ent['member']; dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists(): dst.write_bytes(z.read(root + ent['member'])); os.chmod(dst, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
            if sha_file(dst) != ent['sha256']: raise Stop904('EXTRACTED_SHA ' + ent['member'])
            ent['file'] = str(dst)
    X.GROUPS, X.EMPTY, X.R3, X.A = groups, empty, R3, A
    R['archive'] = A; R['archive_903_decisions'] = archive_903_decisions(R3)
    gate('GATE_ARCHIVE', 'PASS', None, archive=A, cartridges={'%s/%s/%s' % (ns, pm, k): {kk: v[kk] for kk in ('cid', 'member', 'sha256', 'kind', 'history', 'generation', 'reads_in_903')}
                                                             for (ns, pm), g in groups.items() for k, v in g.items()}, empty=empty,
         distinct_tensor_files=1 + sum(len(g) for g in groups.values()))


def archive_tensors_gate():
    """CPU load of every needed archived cartridge (after the pinned engine is extracted): tensor seal + geometry."""
    m = M3; torch = m.torch; G = {}
    for ent in [X.EMPTY] + [v for g in X.GROUPS.values() for v in g.values()]:
        cp = torch.load(ent['file'], map_location='cpu', weights_only=True); ent['tensor_seal'] = m.seal_cp(cp); ent['book_id'] = cp['book_id']
        if ent['kind'] == 'PREFIX': ok = int(cp['n']) == int(cp['p']) == 30 and cp['body_tokens'] == 0
        elif ent['kind'] == 'CHILD': ok = int(cp['p']) == 0 and int(cp['pos0']) == ent['pos0'] == 49 and int(cp['n']) == ent['n'] == 19 and tuple(cp['h'].shape)[:2] == (1, 19)
        else: ok = int(cp['p']) == 30 and int(cp['n']) == ent['n'] == 49 and int(cp['body_tokens']) == 19
        G[ent.get('cid', 'EMPTY')] = ok
        if not ok: gate('GATE_ARCHIVE_TENSORS', 'FAIL', 'geometry ' + ent.get('cid', 'EMPTY'), checks=G)
        if ent['kind'] == 'PREFIX': X.CP_EMPTY = cp; ent['n'] = int(cp['n'])
        del cp
    gate('GATE_ARCHIVE_TENSORS', 'PASS', None, checks=G, seals={k: m.jsha(v['tensor_seal']) for k, v in
                                                                 [('EMPTY', X.EMPTY)] + [('%s/%s/%s' % (ns, pm, kk), vv) for (ns, pm), g in X.GROUPS.items() for kk, vv in g.items()]})


def tokenizer_gate():
    """pinned tokenizer only: the archived token-id hashes reproduce the role records (identity of every cartridge), every public
    answer is producible within MAX_NEW, first answer tokens for the diagnostic, query token ids."""
    m = M3; tk = m.transformers.AutoTokenizer.from_pretrained(m.MODEL_ID, revision=m.MODEL_REVISION, trust_remote_code=False)
    G = {}; bad = []
    for (ns, pm), g in X.GROUPS.items():
        V = names_of(ns, pm, m.NAMES, m.PERMS)
        for key, ent in g.items():
            a, o = E_FACT if key in ('C1_H1', 'C1_HG', 'C1_H2', 'E_IND') else HIST_FACT[ent['history']]
            h = sha_b(json.dumps(list(m.obs_ids(V[a], V[o], tk))).encode())
            if h != ent['ids_sha256']: bad.append(ent['cid'])
            ent['record_roles'] = [a, o]; ent['record_names'] = [V[a], V[o]]
    G['archived_record_ids_reproduced'] = not bad
    stop = tk.convert_tokens_to_ids('<|im_end|>'); answers = {}; first = {}
    for N in m.NAMES.values():
        for w in [N[k] for k in ('o1', 'o2', 'o3')] + ['UNKNOWN']:
            ids = list(tk(w, add_special_tokens=False).input_ids)
            answers[w] = {'ids': ids, 'with_stop': ids + [stop], 'decode_roundtrip': tk.decode(ids) == w, 'fits_max_new': len(ids) + 1 <= MAX_NEW_904}
            first[w] = ids[0]
    G['answers_producible'] = all(v['decode_roundtrip'] and v['fits_max_new'] for v in answers.values()) and stop is not None
    qids = {}
    for (ns, pm) in VARIANTS:
        V = names_of(ns, pm, m.NAMES, m.PERMS)
        for order in ORDERS:
            q = query_904(V['b'], outcome_order(ns, order, m.NAMES)); qids[sha_s(q)] = sha_s(json.dumps(list(tk(q, add_special_tokens=False).input_ids)))
    X.TOKINFO = {'answers': answers, 'first_token': first, 'query_ids_sha256': qids, 'stop_id': stop}
    ok = all(G.values())
    gate('GATE_TOKENIZER_904', 'PASS' if ok else 'FAIL', None if ok else {'record_ids_not_reproduced': bad, **G}, checks=G, answers=answers)
    del tk


def manifest_gate():
    man = build_manifest(X.GROUPS, X.EMPTY, X.TOKINFO, M3.NAMES, M3.PERMS, X.A)
    ids = list(man['cells']); ok = len(ids) == len(set(ids)) == 104 and all(len([c for c in man['cells'].values() if c['unit'] == u]) == 13 for u in man['units'])
    for u, U in man['units'].items():                                 # same query bytes for all 13 arms of a unit
        ok = ok and len({c['query_sha256'] for c in man['cells'].values() if c['unit'] == u}) == 1
    b = json.dumps(man, indent=1, sort_keys=True, default=list).encode(); p = ROOT / 'TEST904_manifest.json'; p.write_bytes(b)
    X.MAN_SHA = sha_b(b); X.MAN_PATH = p
    X.PLAN = [(k, c['unit'], c['arm']) for k, c in man['cells'].items()]       # the run path keeps ids only, no expected answers
    X.UNITQ = {u: {'query': U['query'], 'outs': U['outcome_order'], 'ns': U['ns'], 'perm': U['perm'], 'order': U['order']} for u, U in man['units'].items()}
    gate('GATE_MANIFEST_904', 'PASS' if ok else 'FAIL', None if ok else 'manifest shape', sha256=X.MAN_SHA, n_cells=len(ids), written_before_model=True)
    del man


def engine_gate():
    m = M3; torch = m.torch; G = {}
    m.T_EXP = time.perf_counter(); m.ABORT = dict(m.ABORT_903); m.MAX_NEW = MAX_NEW_904; m.METRICS = {'forge_s': [], 'append_s': [], 'query_s': []}
    m.CART_INDEX = [v for g in X.GROUPS.values() for v in g.values()]; m.CP_EMPTY = X.CP_EMPTY
    G['P_is_30'] = m.P == 30 == m.REF902['P']; G['prefix_sha256_equal_902_903'] = m.sha_bytes(m.PREFIX.encode()) == m.REF902['prefix_sha256']
    G['model_arch'] = (m.NL, m.H, m.QH, m.KVH, m.HD) == (80, 8192, 64, 8, 128)
    with m.MountOff(): cpe, _ = m.forge_native([], 'T904_EMPTY_CHECK')
    G['fresh_empty_prefix_bitwise_equal_archive'] = (torch.equal(cpe['h'], X.CP_EMPTY['h']) and len(cpe['lower']) == len(X.CP_EMPTY['lower']) and
                                                     all(torch.equal(a, c) and torch.equal(b, d) for (a, b), (c, d) in zip(cpe['lower'], X.CP_EMPTY['lower'])))
    del cpe; m.release()
    g0 = X.GROUPS['NS-A', 'R0']; e = g0['E_IND']
    with m.MountOff(): cpx, _ = m.forge_native(list(m.obs_ids(*e['record_names'], m.tok)), 'T904_E_REFORGE_CHECK')
    G['E_IND_reforge_seal_equal_archive_DIAGNOSTIC'] = m.seal_cp(cpx) == e['tensor_seal']; del cpx; m.release()
    sch = {}
    for (ns, pm), g in X.GROUPS.items():
        for k in ('C1_H1', 'C1_HG', 'C1_H2'): sch['%s/%s/%s' % (ns, pm, k)] = m.child_schema(m.load_record(g[k]))['ok']
    G['child_schema_all'] = all(sch.values())
    mm = m.mount_sealed([g0['C1_H1']]); s1 = m.full_kv_seal(mm); G['child_mount_tokens'] = int(mm[0][0].shape[-2]) == 30 + 19; del mm; m.release()
    mm = m.mount_sealed([g0['C1_H1']]); G['child_mount_repeat_bitwise'] = m.full_kv_seal(mm) == s1; del mm; m.release()
    G['hooks_clean'] = m.hooks_clean(m.hook_inventory()); G['read_path_isolated'] = read_path_isolation()['ok']
    fail = [k for k, v in G.items() if isinstance(v, bool) and not k.endswith('_DIAGNOSTIC') and v is not True]
    gate('GATE_ENGINE_904', 'PASS' if not fail else 'FAIL', None if not fail else 'failed: %s' % fail, checks=G, child_schema=sch)
    X.W0 = {'sentinel': m.sentinel(), 'integrity': m.integrity_digest(m.base_params, m.Q4MODS, m.BUFS)}


def work_copies():
    """read slots: byte-identical working copies (straight / cross) and sham copies (same tensors; book_id and file name of the
    other history). Archive files stay read-only and untouched."""
    m = M3; torch = m.torch; X.SLOT = {}; G = {}
    for (ns, pm), g in X.GROUPS.items():
        for arm in SWAP_ARMS + SHAM_ARMS:
            slot, (key,), lab, _ = ARMS[arm]; src = g[key]; d = ROOT / 'work' / ns / pm / ('slot' + slot); d.mkdir(parents=True, exist_ok=True)
            shown = lab or src['history']; name = 'T904_%s_%s_%s_C1_%s.pt' % (ns.replace('-', ''), pm, arm, shown); dst = d / name
            if lab is None:
                shutil.copyfile(src['file'], dst); ent = dict(src, file=str(dst), slot=slot, shown_history=shown, archive_sha256=src['sha256'])
                G[str(dst.name)] = sha_file(dst) == src['sha256']
            else:
                cp = m.load_record(src); cp['book_id'] = g['C1_' + lab]['book_id']; torch.save(cp, dst)
                ent = dict(src, file=str(dst), sha256=sha_file(dst), slot=slot, shown_history=shown, sham_of=src['cid'], archive_sha256=src['sha256'])
                G[str(dst.name)] = (m.seal_cp(cp) == src['tensor_seal'] and int(cp['pos0']) == src['pos0'] and ent['sha256'] != src['sha256'])
                del cp
            os.chmod(dst, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH); X.SLOT[ns, pm, arm] = ent; m.CART_INDEX.append(ent)
    ok = all(G.values()) and all(sha_file(v['file']) == v['sha256'] for g in X.GROUPS.values() for v in g.values())
    gate('GATE_WORK_COPIES', 'PASS' if ok else 'FAIL', None if ok else [k for k, v in G.items() if not v], checks=G)


class DecodeTap:
    """transparent wrapper of the tokenizer during the locked 709 answer(): every attribute and call is forwarded unchanged; the
    single tok.decode(gen) call at the end of answer() is recorded, which exposes the real generated token ids without touching
    generation (decode runs after the greedy loop and returns the same text)."""
    def __init__(self, t): self._t = t; self.calls = []
    def __getattr__(self, n): return getattr(self._t, n)
    def __call__(self, *a, **k): return self._t(*a, **k)
    def decode(self, ids, *a, **k): self.calls.append([int(i) for i in ids]); return self._t.decode(ids, *a, **k)


def diag_validity(argmax, decode_calls, stop_ids):
    """exact check that the diagnostic logits are those of the greedy first step: the argmax must BE the first generated token id
    (or a stop id when nothing was generated). Text prefixes are never accepted as evidence."""
    if len(decode_calls) != 1: return 'NOT_EVALUABLE_GENERATED_IDS_UNAVAILABLE', None
    ids = decode_calls[0]
    if not ids: return ('VERIFIED' if argmax in stop_ids else 'NOT_EVALUABLE_FIRST_TOKEN_MISMATCH'), None
    return ('VERIFIED' if ids[0] == argmax else 'NOT_EVALUABLE_FIRST_TOKEN_MISMATCH'), ids[0]


def read_904(ents, q, cand_ids):
    """one fresh read: archived empty prefix + the given sealed cartridges + public query -> locked 709 answer() greedy; then the
    first-answer-step logits of the public candidate first tokens on the SAME mount (seal must be unchanged)."""
    t_ = time.perf_counter(); mem = m.mount_sealed(ents); s0 = m.full_kv_seal(mem); n = int(mem[0][0].shape[-2])
    real = m.tok; tap = DecodeTap(real); m.tok = tap
    try: raw, dt = m.gen_with(mem, q, MAX_NEW_904)
    finally: m.tok = real
    m.guard('query', dt)
    lg = m.first_logits(mem, q); s1 = m.full_kv_seal(mem)
    if s1 != s0: raise m.StopT896('MOUNT_CHANGED_BY_DIAGNOSTIC')
    top = int(lg.argmax()); logits = {str(i): float(lg[i]) for i in cand_ids}; del mem, lg; m.release()
    return raw, {'mount_tokens': n, 'mount_seal_sha256': m.jsha(s0), 'query_s': round(dt, 3), 'read_s': round(time.perf_counter() - t_, 3)}, {
        'argmax': top, 'logits': logits, 'decode_calls': tap.calls}


m = None                                                                   # bound to the imported 903 module at run time


def read_path_isolation():
    import symtable, inspect, textwrap
    src = textwrap.dedent(inspect.getsource(read_904)); t = symtable.symtable(src, 'read_904', 'exec').get_children()[0]
    g = sorted({x.get_name() for x in t.get_symbols() if x.is_global()})
    allowed = {'m', 'MAX_NEW_904', 'time', 'int', 'round', 'float', 'str', 'DecodeTap'}
    return {'globals': g, 'not_allowed': sorted(set(g) - allowed), 'ok': not (set(g) - allowed)}


def run_reads():
    """104 reads in manifest order. Inputs per read: sealed tensors, the archived prefix, the public query; nothing else."""
    mm = M3; nread = 0
    for k, u, arm in X.PLAN:
        U = X.UNITQ[u]; ns, pm = U['ns'], U['perm']; g = X.GROUPS[ns, pm]; slot, keys, lab, _ = ARMS[arm]
        ents = [X.SLOT[ns, pm, arm]] if arm in SWAP_ARMS + SHAM_ARMS else [g[kk] for kk in keys]
        cand = sorted({X.TOKINFO['first_token'][w] for w in U['outs'] + ['UNKNOWN']})
        raw, info, dg = read_904(ents, U['query'], cand); nread += 1
        info['mount_tokens_expected'] = 30 + sum(int(e['n']) if e['kind'] == 'CHILD' else int(e['body_tokens']) for e in ents)
        info['rope'] = [{'cid': e['cid'], 'source_pos0': e['pos0'] if e['kind'] == 'CHILD' else 30, 'target_pos0': 30 + sum(
            int(x['n']) if x['kind'] == 'CHILD' else int(x['body_tokens']) for x in ents[:i])} for i, e in enumerate(ents)]   # as executed
        calls = dg.pop('decode_calls'); dg['generated_ids'] = calls[0] if len(calls) == 1 else None
        dg['status'], dg['generated_first_id'] = diag_validity(dg['argmax'], calls, {mm.tok.eos_token_id, X.TOKINFO['stop_id']})
        rec = {'cell_id': k, 'unit': u, 'ns': ns, 'perm': pm, 'order': U['order'], 'arm': arm, 'slot': slot, 'label_history': lab,
               'trace': [{'cid': e['cid'], 'sha256': e['sha256'], 'source_sha256': e.get('archive_sha256', e['sha256']), 'file': e['file'], 'kind': e['kind'], 'history': e['history'],
                          'tensor_seal_sha256': mm.jsha(e['tensor_seal']), 'shown_history': e.get('shown_history')} for e in ents],
               'query_sha256': sha_s(U['query']), 'mount': info, 'raw': raw, 'diag': dg, 't_s': round(time.perf_counter() - T0, 1)}
        R['cells'].append(rec); mm.ev('READOUT', cell_id=k, raw=raw, mount=info['mount_seal_sha256'])
        log('READ %-40s %-14s -> %r' % (k, arm, raw[:60])); mm.save(False)
    X.NREAD = nread
    R['generation_sealed_sha256'] = generation_seal(R['cells']); mm.ev('GENERATION_SEALED', sha256=R['generation_sealed_sha256'])


def end_gate():
    mm = M3
    G = {'sentinel_equal': mm.sentinel() == X.W0['sentinel'], 'integrity_equal': mm.integrity_digest(mm.base_params, mm.Q4MODS, mm.BUFS)['sha256'] == X.W0['integrity']['sha256'],
         'hooks_clean': mm.hooks_clean(mm.hook_inventory()), 'archive_and_copies_unchanged': all(sha_file(e['file']) == e['sha256'] for e in mm.CART_INDEX),
         'reads_104': X.NREAD == 104, 'no_new_cartridge_written': not list((ROOT / 'work').rglob('T896_*')) and not list((ROOT / 'work').rglob('T903_*'))}
    ok = all(G.values()); gate('GATE_END_904', 'PASS' if ok else 'FAIL', None if ok else [k for k, v in G.items() if not v], **G)


def write_verdict():
    """scientific verdict (offline evaluator) + technical verdict (gates, blockers, record integrity, manifest and generation seal).
    A record-integrity failure can never leave the technical verdict at PASS."""
    b = X.MAN_PATH.read_bytes()
    if sha_b(b) != X.MAN_SHA: raise Stop904('MANIFEST_CHANGED')
    man = json.loads(b); gates_ok = all(g['status'] != 'FAIL' for g in R['gates'].values()) and not R['technical_blockers']
    R['manifest_sha256'] = X.MAN_SHA
    ev = evaluate_904(man, [c for c in R['cells']], gates_ok)
    run_probs = verify_run_record(dict(R, status='COMPLETE', evaluation=None), b, ev)
    tv = 'PASS' if gates_ok and not ev['integrity_problems'] and not run_probs else 'TECHNICAL_UNDECIDABLE'
    if tv != 'PASS': ev['verdict'] = 'TECHNICAL_UNDECIDABLE'
    R.update(evaluation=ev, technical_verdict=tv, run_record_problems=run_probs)
    R['top'].update(technical_verdict=tv, verdict=ev['verdict'], counts=ev['counts'], integrity_problems=ev['integrity_problems'][:50] + run_probs)
    L = report_lines(ev, man, R.get('archive_903_decisions')) + (['RUN RECORD: ' + '; '.join(run_probs)] if run_probs else [])
    (ROOT / 'TEST904_verdict.txt').write_text('\n'.join(L) + '\nRecompute: python 904.py --recompute TEST904_results.json\n')
    for l in L: log(l)
    return tv


def finalize_artifacts(cfg=None):
    """local results first (always kept), then the requested Drive delivery: ZIP copy + read-back, receipt copy + read-back.
    Delivery status is separate from the technical and scientific verdicts and never changes them."""
    R['finished_utc'] = datetime.now(timezone.utc).isoformat(); R['elapsed_s'] = round(time.perf_counter() - T0, 1)
    try: M3.save() if M3 and M3.R is R else OUT.write_text(json.dumps(R, ensure_ascii=False, indent=1, default=str))
    except Exception as e: print('RESULTS_WRITE_FAILED', e)
    AG = {}
    try:
        rep = sha_file(OUT); AG['report_written_read_back'] = json.loads(OUT.read_text())['run_id'] == RUN_ID
        files = sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name != 'SHA256SUMS.txt' and not p.name.endswith('.tmp'))
        (ROOT / 'SHA256SUMS.txt').write_text('\n'.join('%s  %s' % (sha_file(p), p.relative_to(ROOT).as_posix()) for p in files) + '\n')
        zp = ROOT.parent / ('TEST904_SONUC_%s.zip' % RUN_ID)
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
    mode = (cfg or R.get('config') or {}).get('drive', 'auto'); requested = DRIVE_DIR is not None or mode == 'required'
    D = {'requested': requested, 'mode': mode, 'dir': DRIVE_DIR, 'zip_copied_read_back': None, 'receipt_copied_read_back': None, 'error': None,
         'live_backup_failures': (getattr(M3, 'DRIVE_ERR', {}) or {}).get('backup_failures') if M3 else None}
    if requested and DRIVE_DIR is None: D['error'] = 'DRIVE_REQUIRED_BUT_NOT_MOUNTED'
    elif requested and local_ok:
        ok, err = drive_copy(Path(AG['zip']), DRIVE_DIR); D['zip_copied_read_back'] = ok
        if not ok: D['error'] = 'ZIP: %s' % err
    def status():
        if not local_ok: return 'FAIL_LOCAL_ARTIFACTS'
        if not requested: return 'LOCAL_ONLY_DRIVE_NOT_REQUESTED'
        if D['error']: return 'DRIVE_ZIP_NOT_DELIVERED' if (D['zip_copied_read_back'] is not True) else 'DRIVE_RECEIPT_NOT_DELIVERED'
        return 'PASS' if D['receipt_copied_read_back'] is True else 'DRIVE_RECEIPT_PENDING'
    receipt = {'test': TAG, 'run_id': RUN_ID, 'status': R.get('status'), 'top': R.get('top'), 'artifacts': AG, 'drive': D,
               'results_sha256': sha_file(OUT) if AG.get('report_written_read_back') else None}
    receipt['artifact_status'] = status()
    rp = ROOT.parent / ('TEST904_SONUC_%s_RECEIPT.json' % RUN_ID); rp.write_text(json.dumps(receipt, indent=1, default=str))
    if requested and local_ok and D['zip_copied_read_back'] is True:
        ok, err = drive_copy(rp, DRIVE_DIR)
        if ok:
            try: ok = json.loads((Path(DRIVE_DIR) / rp.name).read_text()) == json.loads(rp.read_text())
            except Exception as e: ok, err = False, '%s: %s' % (type(e).__name__, e)
            if not ok and not err: err = 'READ_BACK_MISMATCH'
        D['receipt_copied_read_back'] = ok
        if not ok: D['error'] = 'RECEIPT: %s' % err
        receipt['artifact_status'] = status(); rp.write_text(json.dumps(receipt, indent=1, default=str))   # local receipt = final state
    X.RECEIPT = receipt
    print('TEST904 ARTIFACTS', json.dumps({'artifact_status': receipt['artifact_status'], 'drive': D, 'zip': AG.get('zip')}, default=str), flush=True)
    return receipt


def drive_copy(src, dst_dir):
    return M3.drive_copy_verified(src, dst_dir) if M3 is not None else (False, 'NO_903_ENGINE_LOADED')


def exit_code(receipt):
    """0 = complete, technically valid, requested delivery done; 2 = complete and valid but the requested Drive delivery failed
    (local results kept); 1 = technical failure. The scientific verdict never sets the exit code."""
    if R.get('status') != 'COMPLETE' or R.get('technical_verdict') != 'PASS': return 1
    return 0 if receipt.get('artifact_status') in ('PASS', 'LOCAL_ONLY_DRIVE_NOT_REQUESTED') else 2


def gpu_main(cfg):
    global M3, m, DRIVE_DIR
    work = ROOT / 'sources'; work.mkdir()
    p903 = fetch_903_source(cfg, work); M3 = m = load_903(p903); bind_903(M3)
    me = Path(globals().get('__file__') or ''); R['executed_source'] = ({'file': str(me.resolve()), 'sha256': sha_file(me), 'git_blob': blob_b(me.read_bytes())}
                                                                        if me.is_file() else {'file': None})
    M3.log('=' * 112); M3.log(MARKER, '| run', RUN_ID); M3.log('Archive-only read of TEST903 %s; decision = locked 709 answer() greedy.' % RUN903['run_id'])
    gate('GATE_SOURCE_903', 'PASS', None, **SRC903, module_main_not_run=M3.RUN_ID == RUN_ID and M3.R is R)
    R['status'] = 'GPU_GATES'; M3.boot_runtime(); M3.env_gate()             # critical: one A100-SXM4-80GB
    if Path('/content/drive/MyDrive').exists():                             # Drive run folder only after GATE_ENV PASS
        DRIVE_DIR = '/content/drive/MyDrive/TEST904_' + RUN_ID; os.makedirs(DRIVE_DIR, exist_ok=True); M3.DRIVE_DIR = DRIVE_DIR; M3.save(force=True)
    try: archive_gate(cfg)
    except Stop904 as e: gate('GATE_ARCHIVE', 'FAIL', str(e))
    M3.PINNED_CALLS = []
    SRC = M3.obtain_sources(cfg, work); R['sources'] = {n: {'sha256': sha_b(b), 'git_blob': blob_b(b)} for n, b in SRC.items()}
    M3.source_extract_gate(SRC); archive_tensors_gate()
    M3.tokenizer_pre_model_gate(); tokenizer_gate(); manifest_gate()      # manifest + answer key on disk BEFORE the model
    M3.model_gate(); engine_gate(); work_copies()
    R['status'] = 'READS'; run_reads(); end_gate(); tv = write_verdict()
    R['status'] = 'COMPLETE' if tv == 'PASS' else 'TECHNICAL_INVALID'


def main(argv=None):
    global M3
    cfg = config(sys.argv[1:] if argv is None else argv)
    if cfg.get('recompute'): return recompute(cfg['recompute'], cfg)
    init_run(cfg); rc = 1
    try:
        ensure_drive_mount(); gpu_main(cfg)
    except BaseException as e:
        tb = traceback.format_exc(); stopped = isinstance(e, (Stop904,)) or type(e).__name__ == 'StopT896'
        R.update(status='TECHNICAL_ABORT' if stopped else ('INTERRUPTED' if isinstance(e, KeyboardInterrupt) else 'ERROR'),
                 technical_verdict='TECHNICAL_UNDECIDABLE', error='%s: %s' % (type(e).__name__, str(e)[:3000]), traceback=tb)
        R['top'].update(technical_verdict='TECHNICAL_UNDECIDABLE', verdict='TECHNICAL_UNDECIDABLE')
        if R['top']['first_failed_gate'] is None: R['top']['first_failed_gate'] = 'ABORT: ' + str(e)[:200]
        (ROOT / 'TEST904_traceback.txt').write_text(tb); print('TEST904_TECHNICAL_STOP', R['error'][:1500], flush=True)
        if LOG and LOG.exists():
            with LOG.open('a') as f: f.write('TEST904_TECHNICAL_STOP ' + R['error'][:1500] + '\n')
        if isinstance(e, KeyboardInterrupt): finalize_artifacts(cfg); raise
    receipt = finalize_artifacts(cfg); rc = exit_code(receipt); line = status_line(rc, receipt); print(line, flush=True)
    if LOG and LOG.exists():
        with LOG.open('a') as f: f.write(line + '\n')
    return rc


def ensure_drive_mount():
    if not Path('/content').exists() or Path('/content/drive/MyDrive').exists(): return
    try:
        from google.colab import drive as _gd
        _gd.mount('/content/drive')
    except Exception as e:
        R['drive_mount_error'] = '%s: %s' % (type(e).__name__, e)


def status_line(rc, receipt):
    t = R.get('top') or {}; d = receipt.get('drive') or {}; a = receipt.get('artifact_status')
    drive = 'PASS' if a == 'PASS' else ('NOT_REQUESTED' if a == 'LOCAL_ONLY_DRIVE_NOT_REQUESTED' else 'FAILED[%s: %s]' % (a, d.get('error')))
    head = {0: 'TAMAMLANDI', 2: 'TAMAMLANDI_TESLIM_HATASI'}.get(rc, 'TEKNIK_HATA')
    return 'TEST904 DURUM: %s | EXIT=%d | TECHNICAL=%s | VERDICT=%s | READS=%s | DRIVE=%s | FIRST_GATE=%s | RESULTS=%s | ZIP=%s' % (
        head, rc, t.get('technical_verdict'), t.get('verdict'), getattr(X, 'NREAD', None), drive, t.get('first_failed_gate'), OUT,
        (receipt.get('artifacts') or {}).get('zip'))


def recompute(path, cfg=None):
    """re-score every cell from its raw answer + the run's manifest (no model, no torch, no 903 import) with the same record
    integrity check, the manifest SHA, the generation seal and a cell-by-cell / unit-by-unit comparison with the stored results."""
    p = Path(path); Rj = json.loads(p.read_text()); b = (p.parent / 'TEST904_manifest.json').read_bytes(); man = json.loads(b)
    gates_ok = all(g.get('status') != 'FAIL' for g in (Rj.get('gates') or {}).values()) and not Rj.get('technical_blockers')
    ev = evaluate_904(man, [c for c in Rj.get('cells', [])], gates_ok)
    probs = verify_run_record(Rj, b, ev)
    if Rj.get('status') == 'COMPLETE' and Rj.get('technical_verdict') != ('PASS' if not ev['integrity_problems'] and not
                                                                          [x for x in probs if not x.startswith('STORED_')] and gates_ok else 'TECHNICAL_UNDECIDABLE'):
        probs.append('STORED_TECHNICAL_VERDICT_DIFFERS')
    print('RECOMPUTED %s | counts %s | record problems: %d' % (ev['verdict'], json.dumps(ev['counts']['fractions']), len(probs) + len(ev['integrity_problems'])))
    for l in report_lines(ev, man, Rj.get('archive_903_decisions')): print(l)
    for x in probs: print('RUN RECORD PROBLEM:', x)
    return 0 if not probs and not ev['integrity_problems'] else 1


if __name__ == '__main__':
    _rc = main(None)
    if _rc and 'get_ipython' not in globals(): sys.exit(_rc)
