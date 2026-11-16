# TEST891 BODY-SHA256 478364540a1b39c2dd11c73b1f5d7501751a8b0832d9635cdd465e9414eb48e7
# AKBASCORE SILICON HIPPOCAMPUS - TEST891 - X2/A COMPONENT-VISIBILITY 2x2 AUDIT on TEST890 (one Colab cell, one Run, A100-SXM4-80GB)
# Contract: K3.1 "TEST890 kaynak/log dogrulamasi ve TEST891 DESIGN_LOCKED" + "CLAUDE ICIN TEST891 KESIN KOD URETIM VE TAM DENETIM
# TALIMATI" (16 Nov 2026). The only new measurement: two audit-only counterfactual CAR reads on the same SSD cartridge load/append
# as FULL / SHAM / BLIND / PAYLOAD_BLIND (same B_t, X_t, n0, q, position ids, cache length, the locked xcar878 with sham=False):
#   X2_VISIBLE = (X2 1, A 0): key columns A and V_AFTER (EVALUATION slot + V_after rows) masked
#   A_VISIBLE  = (X2 0, A 1): key columns X2 and V_AFTER masked
# with BLIND = (1, 1) and PAYLOAD_BLIND = (0, 0) of TEST890; V_AFTER is masked in every cell of the 2x2. TRUE and WRONG are read
# separately and must be exactly equal (else TECHNICAL_BLOCK). None of the reads is executed or enters the executed reading,
# EFFECT, donor, recovery, Y or verdict889; COMPONENT_AUDIT is a separate verdict next to PAYLOAD_AUDIT and cannot change OVERALL.
# REUSE: 890.py (commit 92d0433f, blob 9daee731, canonical body 0f1b4194; the executed 890 GPU cell is blob 2e5ab285 with the same
# canonical body) is downloaded and hash-checked; its wrapper runs unchanged except the counted PATCHES891W (it downloads and checks
# 889.py and builds the TEST890 text, SHA-256 ee4edf90), then the counted PATCHES891 are applied to that text and it is executed.
# The model alone decides: the executed action is the native CAR argmax of the arm's FULL reading, literally through execute866.
# No training, LoRA, backward, RAG, text replay, hooks, router, oracle, answer fixing, UNKNOWN rule, override. GPU_NOT_RUN_BY_AUTHOR.
import time as _t891
T_CELL891 = _t891.perf_counter()                       # the single 75-minute clock starts here (before any download)
import ast as _a891, copy as _c891, hashlib as _h891, json as _j891, re as _r891, urllib.request as _u891
B890_URL891 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
               '92d0433fc688b4054fd0baace985978ddbdd373c/890.py')
B890_BLOB891 = '9daee7314cc5e3870f7aafb2871bbf7571c84c00'
B890_SHA891 = '0e782edc3f93652e11beb43b4ce12a4dfcaedc89b6b2816aa8e80c4f2ee39450'
B890_BODY_LOCK891 = '0f1b4194c1507c15a08f1d44076627350d583b8308e3d0f0966dad2d8506064f'  # canonical body, not a file SHA
SRC889_890_SHA891 = 'ee4edf903ea59df39ee60837cc06001a16188dd2c633c4ea55490ff72f15a4c4'  # the TEST890 text built from pinned 889
EXEC890_GPU891 = {'git_blob': '2e5ab285e2a65f0a8814a8cb42af486cb017a47b',
                  'sha256': 'f94eaa144d83a8983181a0e7bb14575ecb957975806c723ab506fcf7e2e0b634', 'body_lock': B890_BODY_LOCK891,
                  'log': '890.log (repo commit 5d6f1544, git blob df0ee7dd, sha256 fe68545c757c6da2581bd9d2e03fefb7cf6c1981f01fd691066be15fc730dd51)',
                  'note': 'the executed 890 paste is not in the repo: only its canonical body equals the repo file; the raw byte '
                          'difference is not characterized; the repo file (commit 92d0433f) is the source of TEST891'}
PATCHES891W = (                                                                 # (label, old, new, count) on the 890 wrapper body
    ('clock', 'T_CELL890 = _t890.perf_counter()', 'T_CELL890 = T_CELL891', 1),
    ('no_890_exec', "exec(compile(SRC889_890, '889.py:patched_for_TEST890', 'exec'), globals())",
     "pass  # TEST891: the TEST890 text is executed only after PATCHES891 (below)", 1),
    ('chain_file', "'TEST890_base889_patched_executed.py'", "'TEST891_890chain_base889_patched.py'", 1),
    ('st890_lock', "lk = '# TEST890 BODY-SHA256 '", "lk = '# TEST891 BODY-SHA256 '", 1),
    ('st890_lock2', "lk.replace('TEST890', 'TEST889')", "lk.replace('TEST891', 'TEST889')", 1))
RENAMES891 = (('TEST890', 'TEST891', 46), ("'T890 ", "'T891 ", 2), ("'T890_", "'T891_", 4), ('890_engine.log', '891_engine.log', 1),
              ('890_events.jsonl', '891_events.jsonl', 1))                        # I/O names and console tags of the TEST890 text
MODES_T891 = "('FULL', 'SHAM', 'BLIND', 'PAYLOAD_BLIND', 'X2_VISIBLE', 'A_VISIBLE')"
MODES_W891 = "('FULL', 'BLIND', 'PAYLOAD_BLIND', 'X2_VISIBLE', 'A_VISIBLE')"
PATCHES891 = (                                                                  # (label, old, new, count) on the renamed TEST890 text
    ('prereg', 'PREREG889.update(PREREG890)\n', 'PREREG889.update(PREREG890)\nPREREG889.update(PREREG891)\n', 1),
    ('runtime_scan', "'payload_class890', 'payload_audit890')",
     "'payload_class890', 'payload_audit890', 'comp_masks891', 'interaction891', 'component_fields891',\n"
     "                  'visibility_class891', 'component_audit891')", 1),
    ('read_masks', "    P = [n0 + int(entry['provenance']['spans_body']['X2'][0]), n0 + q]                       # TEST891: [X2, A, V_AFTER]\n",
     "    P = [n0 + int(entry['provenance']['spans_body']['X2'][0]), n0 + q]                       # TEST891: [X2, A, V_AFTER]\n"
     "    CM = comp_masks891(entry['provenance']['spans_body'], n0, q)               # TEST891: X2_VISIBLE / A_VISIBLE key masks\n", 1),
    ('read_rec', "    rec = {'cartridge': entry['id'], 'n0': n0, 'q': q,",
     "    rec = {'cartridge': entry['id'], 'cartridge_tensor_sha': entry.get('tensor_sha'), **CM['record'],\n"
     "           'component_v_is_blind_span': CM['record']['v_span'] == V, 'n0': n0, 'q': q,", 1),
    ('read_dispatch', "() if m == 'FULL' else [P] if m == 'PAYLOAD_BLIND' else [V], m == 'SHAM')",
     "() if m == 'FULL' else [P] if m == 'PAYLOAD_BLIND' else CM['masks'][m] if m in CM['masks'] else [V], m == 'SHAM')", 1),
    ('modes_true', "first, ('FULL', 'SHAM', 'BLIND', 'PAYLOAD_BLIND'))", 'first, %s)' % MODES_T891, 1),
    ('modes_wrong', "first, ('FULL', 'BLIND', 'PAYLOAD_BLIND'))", 'first, %s)' % MODES_W891, 1),
    ('call_parity', "                                cT['calls_PAYLOAD_BLIND'] != cW['calls_PAYLOAD_BLIND']:",
     "                                cT['calls_PAYLOAD_BLIND'] != cW['calls_PAYLOAD_BLIND'] or \\\n"
     "                                cT['calls_X2_VISIBLE'] != cW['calls_X2_VISIBLE'] or cT['calls_A_VISIBLE'] != cW['calls_A_VISIBLE']:", 1),
    ('point_fields', "                        if first:\n                            rR, _ = read889(",
     "                        pt.update(component_fields891(rT, rW, cT, cW))                    # TEST891 audit record\n"
     "                        comp_eq = pt['x2v_true_equals_wrong_bitwise'] and pt['av_true_equals_wrong_bitwise']\n"
     "                        if first:\n                            rR, _ = read889(", 1),
    ('comp_gate', "                        if not payload_eq: raise Gate883('PHYSICAL_PAYLOAD_BLIND_LEAK %s t%d' % (ep_id, t))\n",
     "                        if not payload_eq: raise Gate883('PHYSICAL_PAYLOAD_BLIND_LEAK %s t%d' % (ep_id, t))\n"
     "                        if not comp_eq: raise Gate883('PHYSICAL_COMPONENT_VISIBLE_LEAK %s t%d' % (ep_id, t))\n", 1),
    ('capture_tree', "_a889.parse(SRC889_890 + '\\n' + src)", "_a889.parse(SRC889_891 + '\\n' + W890_891 + '\\n' + src)", 1),
    ('lock_diag', "lock['diag890'] = lockdiag890(src)", "lock['diag891'] = lockdiag891(src)", 1),
    ('g0_source', "capture889(); source890()\n", "capture889(); source890(); source891()\n", 1),
    ('g0_selftest', "'890': st890()}", "'890': st890(), '891': st891()}", 1),
    ('audit', "    U_ = unique_m888(pts_)\n",
     "    try:\n        STATE889['component_audit'] = component_audit891(STATE889['verdict'], pts_)\n"
     "    except BaseException as exc:\n        STATE889['component_audit'] = {'COMPONENT_AUDIT': 'NOT_MEASURED', 'reason': 'AUDIT_ERROR %s: %s' % (type(exc).__name__, exc)}\n"
     "    U_ = unique_m888(pts_)\n", 1),
    ('report', "'payload_audit': STATE889['payload_audit'],\n",
     "'payload_audit': STATE889['payload_audit'],\n        'component_audit': STATE889['component_audit'], 'base890': B890_INFO891, "
     "'executed_890_gpu_cell': EXEC890_GPU891,\n", 1),
    ('report_points', "'X_sha256', 'B_tokens', 'cache_tokens')} for p_ in U_],",
     "'X_sha256', 'B_tokens', 'cache_tokens', 'a_true_x2_visible', 'a_wrong_x2_visible',\n"
     "                                                 'a_true_a_visible', 'a_wrong_a_visible', 'true_x2_visible', 'true_a_visible', 'tv_blind_x2v',\n"
     "                                                 'tv_payload_x2v', 'tv_blind_av', 'tv_payload_av', 'interaction', 'x2v_true_equals_wrong_bitwise',\n"
     "                                                 'av_true_equals_wrong_bitwise', 'component_spans', 'calls_by_mode_true', 'calls_by_mode_wrong')} for p_ in U_],", 1),
    ('console_verdict', "          pa_.get('priority_reason'), {k_: s_.get('classes') for k_, s_ in (pa_.get('strata') or {}).items()}))\n",
     "          pa_.get('priority_reason'), {k_: s_.get('classes') for k_, s_ in (pa_.get('strata') or {}).items()}))\n"
     "    ca_ = STATE889.get('component_audit') or {}\n"
     "    print('COMPONENT_AUDIT=%s (%s) | joint_detail=%s | strata=%s' % (ca_.get('COMPONENT_AUDIT'), ca_.get('reason'), ca_.get('joint_detail'),\n"
     "          {k_: s_.get('classes') for k_, s_ in (ca_.get('strata') or {}).items()}))\n", 1),
    ('console_point', "            p_['tv_full_payload'], p_['payload_true_equals_wrong_bitwise'], p_['n0'], p_['q'], p_['payload_span']))\n",
     "            p_['tv_full_payload'], p_['payload_true_equals_wrong_bitwise'], p_['n0'], p_['q'], p_['payload_span']))\n"
     "        print('      X2_VISIBLE T/W=%s/%s A_VISIBLE T/W=%s/%s class=%s TV(B,X)=%.4f TV(P,X)=%.4f TV(B,A)=%.4f TV(P,A)=%.4f T==W=%s/%s masks X=%s A=%s' % (\n"
     "            p_['a_true_x2_visible'], p_['a_wrong_x2_visible'], p_['a_true_a_visible'], p_['a_wrong_a_visible'], visibility_class891(p_),\n"
     "            p_['tv_blind_x2v'], p_['tv_payload_x2v'], p_['tv_blind_av'], p_['tv_payload_av'], p_['x2v_true_equals_wrong_bitwise'],\n"
     "            p_['av_true_equals_wrong_bitwise'], p_['component_spans']['mask_X2_VISIBLE'], p_['component_spans']['mask_A_VISIBLE']))\n", 1),
    ('console_dists', "'true_blind', 'true_payload_blind'):", "'true_blind', 'true_payload_blind', 'true_x2_visible', 'true_a_visible'):", 1),
    ('receipt', "'payload_audit': (STATE889.get('payload_audit') or {}).get('PAYLOAD_AUDIT')}",
     "'payload_audit': (STATE889.get('payload_audit') or {}).get('PAYLOAD_AUDIT'),\n"
     "           'component_audit': (STATE889.get('component_audit') or {}).get('COMPONENT_AUDIT')}", 1))
CHANGED_FUNCS891 = ('capture889', 'episode889', 'read889')        # against the TEST890 text; every other function AST-identical
LOCKED891 = ('xcar878', 'xspan878', 'control_step867', 'execute866', 'write_exp878', 'append_exp878', 'write_appraisal889',
             'write_pair889', 'donor_v889', 'verdict889', 'same_reading881', 'same873')
OWN_FUNCS891 = ('canon891', 'base890_891', 'lockdiag891', 'comp_masks891', 'interaction891', 'component_fields891',
                'visibility_class891', 'component_audit891', 'source891', 'st891')
# LINEDIG891: sha256[:4] of every canonical body line except its own data lines (paste diagnostics only, not a lock)
LINEDIG891 = (
    'd424e0e85a15df5d36edae214b2f663857152f814d0e822547928e64ca08b239af18f8e9a0750657cce948ef9c594851'  #LD890
    '248f908525a260f1615f7a2ec507b588732fe7e37180a90e71a1805d3f7ba04a91632f775f79bee521fa5ba6005cca84'  #LD890
    'e5368001462b9dbaac3e857211e49b86bc1860230f1b00c313aaea67460bc8bbd3b47c6f82a1696dd3190b2ffedd290b'  #LD890
    '16d773fc8e3f9e5c6bfe4ee60286e048b47e8d9084f9efb96b6c9d588f16c0c996882228335b5154d437155fe2b009af'  #LD890
    'df9a947d213cee86c6e05b54a1a1b0f591e6c50d99637ba67b9490a85407a94fba878abdba06d93b5d6aeb03bb3941b6'  #LD890
    '8761dac33b7e29fc5ba195b9990dc94f1f8d5d7244c1f3300e804a28ed96590b69dac3f616ecf4f2edd21f71b1742bb1'  #LD890
    '78410d88d83c9bf3c8637b00e605c2dc0ecc14a7309c8908b02b6b9bacfd74c2ce47e1c90e19fea1ad9213cf1f6d8449'  #LD890
    'ea38e434b08b0907be8965f5136ccd891eb72f6fad820aea7a52a66f6b951668bb0aaadb9880e2243f99a087c94fff17'  #LD890
    '3396ead9aacfa36b0a6fe50ecd79f6f1ae1153589645cd4f46706815c52f5788be834618001127fe71fc2924a1653aff'  #LD890
    '204e000afcd9ad9ee7b76514a62d0d30ce17c05f5e41d80953292ce5e2416715deaf57b563b5475ab45ec7ccec98421a'  #LD890
    'eba265c360402506792f2149308c9f12aaeea090f2e88a40e75a0dba3faca2b281e9193340cf07f7a7efa5a9d0982a0f'  #LD890
    'ac746479a452e62e2dea6dd63b592d5d2c1a91db2739f8e13cbae08e3e8c8b0bc84a36957e4a23b20a066921d9832265'  #LD890
    'd3a2b9b4bb966db43a06e397af07157f430b251789b4902e522d7440a4de69770df8502da683aef69e913bb8663c91f2'  #LD890
    '8c16ea2ad2e424b5d42c051dc22b3f2ec3152900c321e2e242708255b84eccae99beceafc4b505a67489c27a41ca2154'  #LD890
    '8d66aca6b4527b1c1c94c094e911b31d747c47235c9262f4b69de457c74cd7a450e5e6d37bced4688820179990488869'  #LD890
    'da02cbad6f439691f79b9fc012945bf04348e2d2f496df5c185cbb3956967b83903c9ef8f2079e1454e0abd58043d3fe'  #LD890
    '7f5419c40a9ce7a013d81b3a96562153542b6b418b4d2770586d23d5c8488d873e8bb2be4c4adfb08703505233ff573e'  #LD890
    '33c2ace777f0d841ac54a2e0a1afc4a758d614cf9c18842fe9d526e60b04a92f1fca0424f4c44065'  #LD890
    )  #LD890


def canon891(t):
    # the paste-stable canonical form of body_lock889 / canon_lines_m867 (needed before the 890 wrapper is loaded)
    t = t.replace('\r\n', '\n').replace('\r', '\n').replace('\u00a0', ' ')
    for z in ('\ufeff', '\u200b', '\u200c', '\u200d', '\u2060'): t = t.replace(z, '')
    return [l.rstrip() for l in t.split('\n') if l.strip()]


def base890_891(raw):
    blob = _h891.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()
    assert blob == B890_BLOB891 and _h891.sha256(raw).hexdigest() == B890_SHA891, ('BASE_890_LOCK', blob)
    head, rest = raw.decode('utf-8').split('\n', 1)
    m = _r891.fullmatch(r'#\s*TEST890\s+BODY-SHA256\s+([0-9a-f]{64})', head.strip())
    assert m and m.group(1) == B890_BODY_LOCK891, 'BASE_890_HEADER_LOCK'
    assert _h891.sha256(('\n'.join(canon891(rest)) + '\n').encode()).hexdigest() == B890_BODY_LOCK891, 'BASE_890_BODY_LOCK'
    for label, old, new, n in PATCHES891W:
        if rest.count(old) != n: raise AssertionError(('BASE_890_PATCH', label, rest.count(old), n))
        rest = rest.replace(old, new)
    _a891.parse(rest)
    return rest, {'url': B890_URL891, 'git_blob': blob, 'sha256': B890_SHA891, 'body_lock': B890_BODY_LOCK891,
                  'wrapper_patches': [[p[0], p[3]] for p in PATCHES891W], 'wrapper_sha256': _h891.sha256(rest.encode()).hexdigest()}


try:
    with _u891.urlopen(_u891.Request(B890_URL891, headers={'User-Agent': 'AKBASCORE-TEST891'}), timeout=240) as _r:
        B890_RAW891 = _r.read()
    W890_891, B890_INFO891 = base890_891(B890_RAW891)
except BaseException as _exc891:
    import traceback as _tb891
    _p891 = '/content/TEST891_PRE_BASE_ERROR_%s.txt' % _t891.strftime('%Y%m%dT%H%M%SZ', _t891.gmtime())
    try:
        with open(_p891, 'w', encoding='utf-8') as _f891: _f891.write(_tb891.format_exc())
    except OSError: _p891 = 'NOT_WRITTEN'
    print('TEST891 PRE-BASE ERROR (nothing loaded):', type(_exc891).__name__, _exc891, '| traceback:', _p891)
    raise
exec(compile(W890_891, '890.py:wrapper_for_TEST891', 'exec'), globals())   # 890 wrapper: downloads + checks 889, builds SRC889_890
assert _h891.sha256(SRC889_890.encode()).hexdigest() == SRC889_890_SHA891, 'BASE_890_CHAIN_NOT_REPRODUCED'
RENAMED890_891 = apply890(SRC889_890, [('rename',) + r for r in RENAMES891])
assert 'TEST890' not in RENAMED890_891, 'BASE_890_RENAME_LEFT'
SRC889_891 = apply890(RENAMED890_891, PATCHES891)
_a891.parse(SRC889_891)
B890_INFO891.update(chain_889_890_sha256=SRC889_890_SHA891, renames891=[list(r) for r in RENAMES891],
                    patches891=[[p[0], p[3]] for p in PATCHES891], executed_sha256=_h891.sha256(SRC889_891.encode()).hexdigest())
print('TEST891 BASE890', _j891.dumps({k: B890_INFO891[k] for k in ('git_blob', 'sha256', 'body_lock', 'chain_889_890_sha256',
                                                                   'executed_sha256')}, sort_keys=True))

# ============================ sealed audit design (fixed before the model is loaded) ============================
EXPECTED891 = (('10', 'MISSING', 3), ('10', 'FORK', 3), ('10', 'FORK', 4), ('10', 'FORK', 5), ('10', 'FORK', 6), ('09', 'MISSING', 3),
               ('09', 'FORK', 3))                                                # TEST890 GPU: the seven unique points
assert set(PRIMARY890) <= set(EXPECTED891) and len(EXPECTED891) == 7
COMP_CLASSES891 = ('X2_ONLY_SIGNATURE', 'A_ONLY_SIGNATURE', 'EITHER_SINGLE_SUFFICIENT', 'JOINT_VISIBILITY_REQUIRED')
PREREG891 = {
    'test': 'TEST891 COMPONENT_VISIBILITY_2x2_AUDIT (TEST890 PAYLOAD_BLIND_AUDIT and TEST889 run otherwise unchanged)',
    'contract': 'K3.1 TEST891 DESIGN_LOCKED + CLAUDE ICIN TEST891 KESIN KOD URETIM VE TAM DENETIM TALIMATI (16 Nov 2026)',
    'base890': B890_INFO891, 'executed_890_gpu_cell': EXEC890_GPU891,
    'component_reads': 'per eligible point, per cartridge (TRUE and WRONG separately), on the same single load_exp878 + '
                       'append_exp878 as its FULL / SHAM / BLIND / PAYLOAD_BLIND reads; writer spans_body X2=[0,L2], A=[L2,L2+la], '
                       'V_AFTER=[L2+la,q] (EVALUATION slot + V_after rows, the exact BLIND span); absolute = n0 + span; '
                       'X2_VISIBLE masks A and V_AFTER, A_VISIBLE masks X2 and V_AFTER: xcar878(env, g, X, spans, sham=False); '
                       'union of the two masks = the PAYLOAD_BLIND key set, intersection = the V_AFTER key set, no B column; '
                       'empty / overlapping / non-contiguous / out-of-range span -> PHYSICAL_COMPONENT_MASK_GEOMETRY; TRUE == WRONG '
                       'exactly (same_reading881: every token logp, action, argmax, abstain, mass) else PHYSICAL_COMPONENT_VISIBLE_LEAK; '
                       'one budget call and 5 forwards per read; +4 reads per raw point (TRUE 6, WRONG 5); never executed',
    'cells': {'(1,1)': 'BLIND', '(1,0)': 'X2_VISIBLE', '(0,1)': 'A_VISIBLE', '(0,0)': 'PAYLOAD_BLIND', 'V_AFTER': 'masked in all four'},
    'interaction': 'I_w = (p11,w - p10,w) - (p01,w - p00,w) on the unrounded normalized six-action probabilities and the same '
                   'contrast on the teacher-forced sequence logp; descriptive (nonzero I_w is not a binding proof)',
    'expected_strata': ['%s_%s_t%d' % s for s in EXPECTED891], 'primary_strata': ['%s_%s_t%d' % s for s in PRIMARY890],
    'point_class': {'NO_BLIND_FLIP': 'B == N', 'PAYLOAD_890_NOT_REPRODUCED': 'B != N and P != N (B == P included)',
                    'EITHER_SINGLE_SUFFICIENT': 'X == B and A == B', 'X2_ONLY_SIGNATURE': 'X == B and A == P',
                    'A_ONLY_SIGNATURE': 'A == B and X == P', 'JOINT_VISIBILITY_REQUIRED': 'X != B and A != B (detail: '
                    'BOTH_SINGLES_REPRODUCE_P if X == A == P else SINGLE_THIRD_ARGMAX)', 'THIRD_ARGMAX': 'one single == B and the '
                    'other a third action', 'order': 'evaluated top to bottom; B, P, X, A, N = BLIND, PAYLOAD_BLIND, X2_VISIBLE, '
                    'A_VISIBLE, NONE argmax (TRUE arm; TRUE == WRONG is gated)'},
    'audit_verdict': 'COMPONENT_AUDIT, in this order: no point -> NOT_MEASURED / NO_POINTS; PHYSICAL_READ != PASS or any BLIND / '
                     'PAYLOAD / X2_VISIBLE / A_VISIBLE TRUE != WRONG or any mask geometry flag false -> TECHNICAL_BLOCK / '
                     'PHYSICAL_OR_PARITY_OR_GEOMETRY; any of the seven expected strata absent -> INCONCLUSIVE / '
                     'INCOMPLETE_EXPECTED_POINTS; any unique record of a primary stratum with B == N -> INCONCLUSIVE / '
                     'EXPECTED_BLIND_FLIP_ABSENT; with P != N -> INCONCLUSIVE / PAYLOAD_890_NOT_REPRODUCED; any required field '
                     'missing -> INCONCLUSIVE / INCOMPLETE_RECORDS; primary classes contain THIRD_ARGMAX -> INCONCLUSIVE / '
                     'THIRD_ARGMAX; more than one class -> INCONCLUSIVE / MIXED; else the one class over every unique record of '
                     'the four primary strata. No majority vote, no substitution, raw duplicates never add coverage; priority and '
                     'secondary strata are descriptive only',
    'component_scope': 'audit only: never turns CONTENT_EFFECT, OUTCOME_BENEFIT or NATIVE_RECOVERY into PASS, never changes '
                       'TECHNICAL_STATUS / OVERALL or PAYLOAD_AUDIT; V_AFTER is a native evaluation, not an environment outcome',
    'component_not_claimed': ['JOINT_VISIBILITY_REQUIRED is joint span-visibility necessity, not semantic binding: the masked '
                              'positions and the general action prior are not separated', 'outcome credit, learning, recovery, '
                              'GPU success before the run']}


def lockdiag891(src):
    # the TEST890 line diagnostics with the TEST891 line table (same '#LD890' data-line marker)
    keep = LINEDIG890; globals()['LINEDIG890'] = LINEDIG891
    try: return lockdiag890(src)
    finally: globals()['LINEDIG890'] = keep


def comp_masks891(sp, n0, q):
    # absolute key masks of the two new cells from the writer spans; fail-closed on any geometry other than [X2][A][V_AFTER] = [0, q)
    try:
        x2, a, v = [[int(sp[k][0]), int(sp[k][1])] for k in ('X2', 'A', 'V_AFTER')]; n0, q = int(n0), int(q)
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        raise Gate883('PHYSICAL_COMPONENT_MASK_GEOMETRY spans %r: %s' % (sp, exc))
    if not (n0 > 0 and 0 == x2[0] < x2[1] == a[0] < a[1] == v[0] < v[1] == q):
        raise Gate883('PHYSICAL_COMPONENT_MASK_GEOMETRY %r n0=%r q=%r' % (sp, n0, q))
    X, A, V = [[n0 + s[0], n0 + s[1]] for s in (x2, a, v)]
    masks = {'X2_VISIBLE': [A, V], 'A_VISIBLE': [X, V]}
    keys = lambda spans: set(k for s in spans for k in range(s[0], s[1]))
    kx, ka, kv, kp = keys(masks['X2_VISIBLE']), keys(masks['A_VISIBLE']), keys([V]), keys([[n0, n0 + q]])
    rec = {'x2_span': X, 'a_span': A, 'v_span': V, 'mask_X2_VISIBLE': masks['X2_VISIBLE'], 'mask_A_VISIBLE': masks['A_VISIBLE'],
           'mask_x2v_is_A_and_V': kx == keys([A]) | kv, 'mask_av_is_X2_and_V': ka == keys([X]) | kv,
           'mask_union_is_payload': kx | ka == kp, 'mask_intersection_is_V': kx & ka == kv,
           'mask_visible_x2_exact': kp - kx == keys([X]), 'mask_visible_a_exact': kp - ka == keys([A]),
           'mask_no_B_column': min(kx | ka) >= n0, 'mask_inside_body': max(kx | ka) < n0 + q}
    return {'masks': masks, 'record': rec}


def interaction891(B, X, A, P):
    # I_w = (p11 - p10) - (p01 - p00) per action, unrounded; 11 = BLIND, 10 = X2_VISIBLE, 01 = A_VISIBLE, 00 = PAYLOAD_BLIND
    sq = lambda r: {s['word']: float(s['sequence_logp']) for s in r['scores']}
    nb, nx, na, np_ = [{w: float(r['normalized'][w]) for w in ACTIONS_M867} for r in (B, X, A, P)]
    lb, lx, la, lp = [sq(r) for r in (B, X, A, P)]
    return {'p': {w: (nb[w] - nx[w]) - (na[w] - np_[w]) for w in ACTIONS_M867},
            'seq_logp': {w: (lb[w] - lx[w]) - (la[w] - lp[w]) for w in ACTIONS_M867}}


def component_fields891(rT, rW, cT, cW):
    # the point record of the two new reads (TRUE arm values; TRUE == WRONG is the gate); never fed back into a decision
    B, X, A, P = rT['BLIND'], rT['X2_VISIBLE'], rT['A_VISIBLE'], rT['PAYLOAD_BLIND']
    sk = ('x2_span', 'a_span', 'v_span', 'mask_X2_VISIBLE', 'mask_A_VISIBLE')
    return {'x2v_true_equals_wrong_bitwise': same_reading881(X, rW['X2_VISIBLE']), 'av_true_equals_wrong_bitwise': same_reading881(A, rW['A_VISIBLE']),
            'a_true_x2_visible': X['action'], 'a_wrong_x2_visible': rW['X2_VISIBLE']['action'],
            'a_true_a_visible': A['action'], 'a_wrong_a_visible': rW['A_VISIBLE']['action'],
            'true_x2_visible': summary_m888(X), 'wrong_x2_visible': summary_m888(rW['X2_VISIBLE']),
            'true_a_visible': summary_m888(A), 'wrong_a_visible': summary_m888(rW['A_VISIBLE']),
            'tv_blind_x2v': tv_m867(B, X), 'tv_payload_x2v': tv_m867(P, X), 'tv_blind_av': tv_m867(B, A), 'tv_payload_av': tv_m867(P, A),
            'interaction': interaction891(B, X, A, P), 'component_spans': {k: cT[k] for k in sk},
            'component_spans_true_equals_wrong': all(cT[k] == cW[k] for k in sk),
            'component_geometry_ok': all(c[k] is True for c in (cT, cW) for k in c if k.startswith('mask_') and isinstance(c[k], bool)),
            'calls_by_mode_true': {k[6:]: v for k, v in cT.items() if k.startswith('calls_')},
            'calls_by_mode_wrong': {k[6:]: v for k, v in cW.items() if k.startswith('calls_')},
            'cartridge_sha_true': cT.get('cartridge_tensor_sha'), 'cartridge_sha_wrong': cW.get('cartridge_tensor_sha')}


def visibility_class891(p):
    n, b, y, x, a = p['a_none'], p['a_true_blind'], p['a_true_payload_blind'], p['a_true_x2_visible'], p['a_true_a_visible']
    if b == n: return 'NO_BLIND_FLIP'
    if y != n: return 'PAYLOAD_890_NOT_REPRODUCED'
    if x == b and a == b: return 'EITHER_SINGLE_SUFFICIENT'
    if x == b and a == y: return 'X2_ONLY_SIGNATURE'
    if a == b and x == y: return 'A_ONLY_SIGNATURE'
    if x != b and a != b: return 'JOINT_VISIBILITY_REQUIRED'
    return 'THIRD_ARGMAX'


def component_audit891(verdict, points):
    # read-only on verdict889 and the points; coverage over the seven fixed strata identities; every unique record is kept
    U = unique_m888(points); rows = []
    for p in U:
        s = (p['world'], p['condition'], int(p['step'])); c = visibility_class891(p)
        need = ('none', 'true_blind', 'true_payload_blind', 'true_x2_visible', 'true_a_visible')
        rows.append({'episode_id': p['episode_id'], 'stratum': '%s_%s_t%d' % s, 'primary': s in PRIMARY890, 'priority': s in PRIORITY890,
                     'a_none': p['a_none'], 'a_blind': p['a_true_blind'], 'a_payload': p['a_true_payload_blind'],
                     'a_x2_visible': p['a_true_x2_visible'], 'a_a_visible': p['a_true_a_visible'], 'class': c,
                     'joint_detail': (('BOTH_SINGLES_REPRODUCE_P' if p['a_true_x2_visible'] == p['a_true_a_visible'] == p['a_true_payload_blind']
                                       else 'SINGLE_THIRD_ARGMAX') if c == 'JOINT_VISIBILITY_REQUIRED' else None),
                     'tv': {k: p[k] for k in ('tv_blind_x2v', 'tv_payload_x2v', 'tv_blind_av', 'tv_payload_av', 'tv_blind_payload', 'tv_none_payload')},
                     'interaction': p['interaction'],
                     'parity': {k: p[k] for k in ('blind_true_equals_wrong_bitwise', 'payload_true_equals_wrong_bitwise',
                                                  'x2v_true_equals_wrong_bitwise', 'av_true_equals_wrong_bitwise')},
                     'geometry_ok': p['component_geometry_ok'] is True and p['component_spans_true_equals_wrong'] is True,
                     'complete': all(set((p.get(k) or {}).get('p') or {}) == set(ACTIONS_M867) and
                                     set((p.get(k) or {}).get('seq_logp') or {}) == set(ACTIONS_M867) for k in need) and
                                 set(p['interaction']['p']) == set(p['interaction']['seq_logp']) == set(ACTIONS_M867)})
    name = lambda s: '%s_%s_t%d' % s
    strata = {}
    for s in EXPECTED891:
        v = [r for r in rows if r['stratum'] == name(s)]; cl = [r['class'] for r in v]
        strata[name(s)] = {'unique_points': len(v), 'classes': cl, 'primary': s in PRIMARY890, 'priority': s in PRIORITY890,
                           'status': 'NOT_OCCURRED' if not v else 'OCCURRED' if s not in PRIMARY890 else
                           'EXPECTED_BLIND_FLIP_ABSENT' if 'NO_BLIND_FLIP' in cl else
                           'PAYLOAD_890_NOT_REPRODUCED' if 'PAYLOAD_890_NOT_REPRODUCED' in cl else 'MEASURED'}
    prim = [r for r in rows if r['primary']]; cls = sorted({r['class'] for r in prim})
    cov = {'expected': [name(s) for s in EXPECTED891], 'not_occurred': [k for k, v in strata.items() if v['status'] == 'NOT_OCCURRED'],
           'primary_flip_absent': [k for k, v in strata.items() if v['status'] == 'EXPECTED_BLIND_FLIP_ABSENT'],
           'primary_payload_not_reproduced': [k for k, v in strata.items() if v['status'] == 'PAYLOAD_890_NOT_REPRODUCED'],
           'incomplete_records': [r['stratum'] for r in rows if not r['complete']]}
    tech = verdict.get('PHYSICAL_READ') != 'PASS' or any(not r['geometry_ok'] or not all(x is True for x in r['parity'].values()) for r in rows)
    if not rows: a, why = 'NOT_MEASURED', 'NO_POINTS'
    elif tech: a, why = 'TECHNICAL_BLOCK', 'PHYSICAL_OR_PARITY_OR_GEOMETRY'
    elif cov['not_occurred']: a, why = 'INCONCLUSIVE', 'INCOMPLETE_EXPECTED_POINTS'
    elif cov['primary_flip_absent']: a, why = 'INCONCLUSIVE', 'EXPECTED_BLIND_FLIP_ABSENT'
    elif cov['primary_payload_not_reproduced']: a, why = 'INCONCLUSIVE', 'PAYLOAD_890_NOT_REPRODUCED'
    elif cov['incomplete_records']: a, why = 'INCONCLUSIVE', 'INCOMPLETE_RECORDS'
    elif 'THIRD_ARGMAX' in cls: a, why = 'INCONCLUSIVE', 'THIRD_ARGMAX'
    elif len(cls) != 1: a, why = 'INCONCLUSIVE', 'MIXED'
    else: a, why = cls[0], 'ALL_%d_PRIMARY_RECORDS_ONE_CLASS_7_STRATA_COVERED' % len(prim)
    return {'COMPONENT_AUDIT': a, 'reason': why, 'coverage': cov, 'strata': strata,
            'joint_detail': sorted({r['joint_detail'] for r in prim if r['joint_detail']}) if a == 'JOINT_VISIBILITY_REQUIRED' else None,
            'priority_descriptive_only': {k: v['classes'] for k, v in strata.items() if v['priority']},
            'secondary_descriptive_only': [r for r in rows if not r['primary']], 'points': rows,
            'raw_points': len(points), 'unique_points': len(U),
            'verdict889_unchanged': {k: verdict.get(k) for k in ('TECHNICAL_STATUS', 'PHYSICAL_READ', 'CONTENT_EFFECT', 'OUTCOME_BENEFIT',
                                                                 'NATIVE_RECOVERY', 'OVERALL')},
            'scope': PREREG891['component_scope'], 'not_claimed': PREREG891['component_not_claimed']}


def source891():
    # G0, before the model: the executed text differs from the TEST890 text only in CHANGED_FUNCS891 + module statements, the
    # locked functions are untouched, and the two new reads reach nothing but the point record and its exact-parity gate
    T, R0 = _a891.parse(SRC889_891), _a891.parse(RENAMED890_891)
    f = {n.name: n for n in T.body if isinstance(n, _a891.FunctionDef)}; f0 = {n.name: n for n in R0.body if isinstance(n, _a891.FunctionDef)}
    W = _a891.parse(W890_891); C = _a891.parse((ROOT864 / 'TEST891.py').read_text(encoding='utf-8'))
    fw = {n.name for n in W.body if isinstance(n, _a891.FunctionDef)}; fc = {n.name: n for n in C.body if isinstance(n, _a891.FunctionDef)}
    changed = sorted(k for k in set(f) | set(f0) if k not in f or k not in f0 or _a891.dump(f[k]) != _a891.dump(f0[k]))
    rd, ep = f['read889'], f['episode889']
    calls = lambda node, nm: [n for n in _a891.walk(node) if isinstance(n, _a891.Call) and getattr(n.func, 'id', None) == nm]
    xc, cm, cf = calls(rd, 'xcar878'), calls(rd, 'comp_masks891'), calls(ep, 'component_fields891')
    modes = sorted(_a891.unparse(n.args[10]) for n in calls(ep, 'read889'))
    has = lambda n, vals: any(isinstance(x, _a891.Constant) and x.value in vals for x in _a891.walk(n))
    reach = sorted({_a891.unparse(t) for n in _a891.walk(ep) if isinstance(n, _a891.Assign) and has(n, ('X2_VISIBLE', 'A_VISIBLE')) for t in n.targets})
    reading = sorted({_a891.unparse(n.value) for n in _a891.walk(ep) if isinstance(n, _a891.Assign)
                      and any(isinstance(x, _a891.Name) and x.id == 'reading' for x in n.targets)})
    src_ep = _a891.unparse(ep)
    own = [fc[k] for k in ('comp_masks891', 'interaction891', 'component_fields891', 'visibility_class891', 'component_audit891')]
    banned = {'write_exp878', 'append_exp878', 'xappend878', 'execute866', 'control_step867', 'donor_v889', 'write_pair889',
              'write_appraisal889', 'load_exp878', 'xcar878', 'car873', 'open', 'exec', 'eval', 'setattr', 'globals'}
    facts = {'chain_889_890_reproduced': _h891.sha256(SRC889_890.encode()).hexdigest() == SRC889_890_SHA891,
             'changed_functions': changed == list(CHANGED_FUNCS891),
             'locked_not_redefined': not any(k in fc or k in fw or (k in f and k not in f0) for k in LOCKED891) and
                                     all(_a891.dump(f[k]) == _a891.dump(f0[k]) for k in LOCKED891 if k in f),
             'own_names_unique': not (set(OWN_FUNCS891) & (set(f) | fw)) and set(OWN_FUNCS891) <= set(fc),
             'single_masked_kernel_call': len(xc) == 1 and _a891.unparse(xc[0].args[3]) ==
             "() if m == 'FULL' else [P] if m == 'PAYLOAD_BLIND' else CM['masks'][m] if m in CM['masks'] else [V]" and
             _a891.unparse(xc[0].args[4]) == "m == 'SHAM'",
             'masks_from_writer_spans': len(cm) == 1 and _a891.unparse(cm[0]) == "comp_masks891(entry['provenance']['spans_body'], n0, q)",
             'modes_true_wrong_repeat': modes == ["('FULL', 'BLIND', 'PAYLOAD_BLIND', 'X2_VISIBLE', 'A_VISIBLE')",
                                                  "('FULL', 'SHAM', 'BLIND', 'PAYLOAD_BLIND', 'X2_VISIBLE', 'A_VISIBLE')", "('FULL',)"],
             'new_reads_reach_only_point_and_gate': reach == ['(rT, cT)', '(rW, cW)'] and len(cf) == 1 and
                                                    _a891.unparse(cf[0]) == 'component_fields891(rT, rW, cT, cW)' and
                                                    "pt.update(component_fields891(rT, rW, cT, cW))" in src_ep,
             'executed_reading_unchanged': reading == ["rT['FULL'] if arm == 'D_TRUE' else rW['FULL']", 'r_none', "record['reading']"],
             'component_gate_after_point_record': 0 < src_ep.find("out['points'].append(pt)") < src_ep.find("raise Gate883('PHYSICAL_COMPONENT_VISIBLE_LEAK"),
             'no_write_donor_execute_in_new_functions': not any(isinstance(x, _a891.Name) and x.id in banned for n in own for x in _a891.walk(n)),
             'verdict889_has_no_component': 'VISIBLE' not in _a891.unparse(f['verdict889'])}
    if not all(facts.values()): raise Gate_m867('SOURCE891_FACTS %s' % sorted(k for k, v in facts.items() if not v))
    (ROOT864 / 'TEST891_executed_889_890_891.py').write_text(SRC889_891, encoding='utf-8')
    STATE889['source']['base890'] = B890_INFO891; STATE889['source']['facts891'] = facts
    json_write864('TEST891_base890.json', {'base890': B890_INFO891, 'executed_890_gpu_cell': EXEC890_GPU891, 'facts891': facts,
                                          'changed_functions': changed, 'before_model_load': True})
    print('T891 BASE890 PATCH facts=%s executed_sha256=%s' % (all(facts.values()), B890_INFO891['executed_sha256']), flush=True)


def st891():
    r = {}; W6 = list(ACTIONS_M867)
    sp = {'X2': [0, 10], 'A': [10, 12], 'V_AFTER': [12, 20]}; cm = comp_masks891(sp, 100, 20)
    r['mask_sets_exact'] = cm['masks'] == {'X2_VISIBLE': [[110, 112], [112, 120]], 'A_VISIBLE': [[100, 110], [112, 120]]} and \
        all(v is True for k, v in cm['record'].items() if isinstance(v, bool)) and cm['record']['v_span'] == [112, 120]
    for nm, bad in (('gap', {'X2': [0, 10], 'A': [11, 12], 'V_AFTER': [12, 20]}), ('zero_A', {'X2': [0, 10], 'A': [10, 10], 'V_AFTER': [10, 20]}),
                    ('overlap', {'X2': [0, 11], 'A': [10, 12], 'V_AFTER': [12, 20]}), ('V_end_not_q', {'X2': [0, 10], 'A': [10, 12], 'V_AFTER': [12, 19]}),
                    ('X2_not_0', {'X2': [1, 10], 'A': [10, 12], 'V_AFTER': [12, 20]}), ('missing_A', {'X2': [0, 10], 'V_AFTER': [10, 20]}),
                    ('V_out_of_range', {'X2': [0, 10], 'A': [10, 12], 'V_AFTER': [12, 21]})):
        try: comp_masks891(bad, 100, 20); r['mask_refused_%s' % nm] = False
        except Gate883: r['mask_refused_%s' % nm] = True
    try: comp_masks891(sp, 0, 20); r['mask_refused_no_B'] = False
    except Gate883: r['mask_refused_no_B'] = True

    def rd(pp, lp2=-0.5):
        sc = [{'word': w, 'ids': [i, 7], 'token_logps': [-1.0 - 0.1 * i, lp2], 'sequence_logp': -1.5 - 0.1 * i} for i, w in enumerate(W6)]
        return {'action': max(pp, key=pp.get), 'argmax_word': max(pp, key=pp.get), 'abstain': False, 'mass': 0.5, 'normalized': dict(pp),
                'margin_logp': 0.1, 'scores': sc}
    base = {w: 1.0 / 6 for w in W6}
    pB, pX, pA, pP = [dict(base, **{W6[k]: base[W6[k]] + d}) for k, d in ((0, 0.123456789), (1, 0.01), (2, 0.0201), (3, 0.3))]
    I = interaction891(rd(pB), rd(pX), rd(pA), rd(pP))
    r['interaction_unrounded'] = all(I['p'][w] == (pB[w] - pX[w]) - (pA[w] - pP[w]) for w in W6) and I['p'][W6[0]] == pB[W6[0]] - pX[W6[0]] - (pA[W6[0]] - pP[W6[0]]) \
        and abs(I['p'][W6[0]] - 0.123456789) < 1e-15 and all(v == 0.0 for v in I['seq_logp'].values())
    rT = {'BLIND': rd(pB), 'X2_VISIBLE': rd(pX), 'A_VISIBLE': rd(pA), 'PAYLOAD_BLIND': rd(pP)}
    cT = dict(cm['record'], calls_FULL=1, calls_X2_VISIBLE=1, calls_A_VISIBLE=1, cartridge_tensor_sha='s')
    f1 = component_fields891(rT, _c891.deepcopy(rT), cT, dict(cT))
    rW2 = _c891.deepcopy(rT); rW2['X2_VISIBLE']['scores'][3]['token_logps'][1] += 1e-9            # second-token perturbation, same argmax
    f2 = component_fields891(rT, rW2, cT, dict(cT))
    r['parity_exact_pass'] = f1['x2v_true_equals_wrong_bitwise'] is True is f1['av_true_equals_wrong_bitwise'] and f1['component_geometry_ok']
    r['parity_second_token_fail'] = f2['x2v_true_equals_wrong_bitwise'] is False and f2['a_true_x2_visible'] == f2['a_wrong_x2_visible'] and \
        f2['av_true_equals_wrong_bitwise'] is True
    r['tv_unrounded'] = f1['tv_blind_x2v'] == tv_m867(rT['BLIND'], rT['X2_VISIBLE']) and f1['calls_by_mode_true'] == {'FULL': 1, 'X2_VISIBLE': 1, 'A_VISIBLE': 1}
    r['geometry_flag_false_detected'] = component_fields891(rT, rT, dict(cT, mask_union_is_payload=False), cT)['component_geometry_ok'] is False

    def Q(w, c, t, n, b, y, x, a, **kw):
        p = {'episode_id': 'E', 'world': w, 'condition': c, 'step': t, 'a_none': n, 'a_true': b, 'a_true_blind': b, 'a_true_payload_blind': y,
             'a_true_x2_visible': x, 'a_true_a_visible': a, 'tv_blind_x2v': 0.1, 'tv_payload_x2v': 0.2, 'tv_blind_av': 0.3, 'tv_payload_av': 0.4,
             'tv_blind_payload': 0.5, 'tv_none_payload': 0.05, 'interaction': I, 'blind_true_equals_wrong_bitwise': True,
             'payload_true_equals_wrong_bitwise': True, 'x2v_true_equals_wrong_bitwise': True, 'av_true_equals_wrong_bitwise': True,
             'component_geometry_ok': True, 'component_spans_true_equals_wrong': True,
             'unique_key': '%s%s%d%s%s%s%s%s' % (w, c, t, n, b, y, x, a)}
        for k in ('none', 'true_blind', 'true_payload_blind', 'true_x2_visible', 'true_a_visible'): p[k] = {'p': dict(base), 'seq_logp': dict(base)}
        p.update(kw); return p
    C = visibility_class891
    r['class_matrix'] = [C(Q('09', 'FORK', 3, 'ADVANCE', b, y, x, a)) for b, y, x, a in (
        ('ACCEPT', 'ADVANCE', 'ACCEPT', 'ADVANCE'), ('ACCEPT', 'ADVANCE', 'ADVANCE', 'ACCEPT'), ('ACCEPT', 'ADVANCE', 'ACCEPT', 'ACCEPT'),
        ('ACCEPT', 'ADVANCE', 'ADVANCE', 'ADVANCE'), ('ACCEPT', 'ADVANCE', 'STOP', 'ADVANCE'), ('ACCEPT', 'ADVANCE', 'ACCEPT', 'STOP'),
        ('ADVANCE', 'ADVANCE', 'ACCEPT', 'ACCEPT'), ('ACCEPT', 'ACCEPT', 'ACCEPT', 'ACCEPT'), ('ACCEPT', 'STOP', 'ACCEPT', 'ACCEPT'))] == [
        'X2_ONLY_SIGNATURE', 'A_ONLY_SIGNATURE', 'EITHER_SINGLE_SUFFICIENT', 'JOINT_VISIBILITY_REQUIRED', 'JOINT_VISIBILITY_REQUIRED',
        'THIRD_ARGMAX', 'NO_BLIND_FLIP', 'PAYLOAD_890_NOT_REPRODUCED', 'PAYLOAD_890_NOT_REPRODUCED']
    V = {'TECHNICAL_STATUS': 'TECHNICAL_BLOCK', 'PHYSICAL_READ': 'PASS', 'CONTENT_EFFECT': 'INCONCLUSIVE', 'OUTCOME_BENEFIT': 'NOT_MEASURED',
         'NATIVE_RECOVERY': 'INCONCLUSIVE', 'OVERALL': 'TECHNICAL_BLOCK'}
    sec = [Q(*s, 'STOP', 'STOP', 'STOP', 'STOP', 'STOP') for s in EXPECTED891 if s not in PRIMARY890]
    mk = lambda x, a, **kw: [Q(*s, 'ADVANCE', 'ACCEPT', 'ADVANCE', x, a, **kw) for s in PRIMARY890]
    J, XO, AO, E2 = mk('ADVANCE', 'ADVANCE'), mk('ACCEPT', 'ADVANCE'), mk('ADVANCE', 'ACCEPT'), mk('ACCEPT', 'ACCEPT')
    A_ = component_audit891; ok = lambda a, v, w: (a['COMPONENT_AUDIT'], a['reason']) == (v, w)
    I_, ALL4 = 'INCONCLUSIVE', 'ALL_4_PRIMARY_RECORDS_ONE_CLASS_7_STRATA_COVERED'
    keep = _c891.deepcopy(V); a = A_(V, sec + J + [dict(J[0])])
    r['audit_joint_complete'] = ok(a, 'JOINT_VISIBILITY_REQUIRED', ALL4) and a['joint_detail'] == ['BOTH_SINGLES_REPRODUCE_P'] and \
        a['raw_points'] == 8 and a['unique_points'] == 7
    r['audit_x2_a_either_complete'] = ok(A_(V, sec + XO), 'X2_ONLY_SIGNATURE', ALL4) and ok(A_(V, sec + AO), 'A_ONLY_SIGNATURE', ALL4) and \
        ok(A_(V, sec + E2), 'EITHER_SINGLE_SUFFICIENT', ALL4)
    r['audit_missing_secondary'] = ok(A_(V, sec[1:] + J), I_, 'INCOMPLETE_EXPECTED_POINTS')
    r['audit_missing_primary'] = ok(A_(V, sec + J[1:]), I_, 'INCOMPLETE_EXPECTED_POINTS')
    pr = A_(V, [j for j in J if (j['world'], j['condition'], j['step']) in PRIORITY890])
    r['audit_priority_only_never_conclusive'] = ok(pr, I_, 'INCOMPLETE_EXPECTED_POINTS') and \
        pr['priority_descriptive_only'] == {'10_FORK_t5': ['JOINT_VISIBILITY_REQUIRED'], '09_FORK_t3': ['JOINT_VISIBILITY_REQUIRED']}
    dup = A_(V, sec[1:] + J + [dict(x, unique_key=x['unique_key']) for x in sec[1:]])
    r['audit_raw_duplicates_no_coverage'] = ok(dup, I_, 'INCOMPLETE_EXPECTED_POINTS') and dup['raw_points'] > dup['unique_points']
    nf = J[:3] + [Q(*PRIMARY890[3], 'ADVANCE', 'ADVANCE', 'ADVANCE', 'ADVANCE', 'ADVANCE')]
    r['audit_flip_absent_no_substitution'] = ok(A_(V, sec + nf + [Q('10', 'FORK', 2, 'ADVANCE', 'ACCEPT', 'ADVANCE', 'ADVANCE', 'ADVANCE')]), I_, 'EXPECTED_BLIND_FLIP_ABSENT')
    r['audit_payload_not_reproduced'] = ok(A_(V, sec + J[:3] + [Q(*PRIMARY890[3], 'ADVANCE', 'ACCEPT', 'ACCEPT', 'ADVANCE', 'ADVANCE')]), I_, 'PAYLOAD_890_NOT_REPRODUCED')
    r['audit_two_records_disagree'] = ok(A_(V, sec + J + [dict(XO[0], unique_key='second_record')]), I_, 'MIXED')
    r['audit_mixed'] = ok(A_(V, sec + J[:2] + XO[2:]), I_, 'MIXED')
    r['audit_third'] = ok(A_(V, sec + J[:3] + [Q(*PRIMARY890[3], 'ADVANCE', 'ACCEPT', 'ADVANCE', 'ACCEPT', 'STOP')]), I_, 'THIRD_ARGMAX')
    r['audit_physical_fail_block'] = ok(A_(dict(V, PHYSICAL_READ='FAIL'), sec + J), 'TECHNICAL_BLOCK', 'PHYSICAL_OR_PARITY_OR_GEOMETRY')
    for k in ('blind_true_equals_wrong_bitwise', 'payload_true_equals_wrong_bitwise', 'x2v_true_equals_wrong_bitwise',
              'av_true_equals_wrong_bitwise', 'component_geometry_ok', 'component_spans_true_equals_wrong'):
        r['audit_block_%s_false' % k] = ok(A_(V, sec + J[:3] + [dict(J[3], **{k: False})]), 'TECHNICAL_BLOCK', 'PHYSICAL_OR_PARITY_OR_GEOMETRY')
    r['audit_physical_fail_not_hidden_by_coverage'] = ok(A_(dict(V, PHYSICAL_READ='FAIL'), J[:1]), 'TECHNICAL_BLOCK', 'PHYSICAL_OR_PARITY_OR_GEOMETRY')
    r['audit_incomplete_record'] = ok(A_(V, sec + J[:3] + [dict(J[3], true_a_visible={'p': {'ACQUIRE': 1.0}, 'seq_logp': {}})]), I_, 'INCOMPLETE_RECORDS')
    r['audit_empty'] = ok(A_(V, []), 'NOT_MEASURED', 'NO_POINTS')
    r['audit_blocked_missing_episode'] = ok(A_(V, [s_ for s_ in sec + J if s_['condition'] != 'MISSING']), I_, 'INCOMPLETE_EXPECTED_POINTS')
    r['audit_verdict889_immutable'] = V == keep and a['verdict889_unchanged']['OVERALL'] == 'TECHNICAL_BLOCK' and \
        not ({'OVERALL', 'TECHNICAL_STATUS', 'PAYLOAD_AUDIT', 'OUTCOME_BENEFIT', 'NATIVE_RECOVERY'} & set(a))
    tb = ('x', 'a', 'Y', 1)
    for nm, txt, row in (('double', 'aXa', tb), ('missing', 'bcd', tb)):
        try: apply890(txt, [row]); r['patch_anchor_%s_refused' % nm] = False
        except AssertionError: r['patch_anchor_%s_refused' % nm] = True
    for nm, raw in (('one_byte', B890_RAW891[:700] + b'#' + B890_RAW891[701:]), ('appended', B890_RAW891 + b'\nprint(1)\n'), ('truncated', B890_RAW891[:-9])):
        try: base890_891(raw); r['base890_%s_refused' % nm] = False
        except AssertionError: r['base890_%s_refused' % nm] = True
    r['base890_reproducible'] = base890_891(B890_RAW891)[0] == W890_891 and apply890(apply890(SRC889_890, [('rename',) + x for x in RENAMES891]), PATCHES891) == SRC889_891
    r['chain_889_890_sha'] = _h891.sha256(SRC889_890.encode()).hexdigest() == SRC889_890_SHA891
    body = 'x = 1\n'; lk = '# TEST891 BODY-SHA256 ' + _h891.sha256(body.encode()).hexdigest()
    r['lock_891_ok_890_header_refused'] = body_lock889(lk + '\n' + body)['ok'] and not body_lock889(lk.replace('TEST891', 'TEST890') + '\n' + body)['ok']
    return r


exec(compile(SRC889_891, '889.py:patched_for_TEST890_TEST891', 'exec'), globals())   # TEST889 + TEST890 + TEST891 counted patches
