# TEST892 BODY-SHA256 ee1fb12f3e79c93c55ed254bddded3d836bc355b7b3942edc2a42d97e8b5e798
# AKBASCORE SILICON HIPPOCAMPUS - TEST892 - V_ONLY_OUTCOME_CAUSAL_READ on TEST891 (one Colab cell, one Run, A100-SXM4-80GB)
# Contract: K3.1 "TEST891 Gercek GPU Sonrasi Bagimsiz Kok-Neden Analizi ve TEST892 Tasarimi" (7.1-7.7) + "CLAUDE'UN TEST892 GOREV
# TALIMATI" (16 Nov 2026). The only new measurement: one audit-only counterfactual CAR read V_ONLY per cartridge (TRUE and WRONG
# separately) on the same SSD cartridge load/append as FULL / SHAM / BLIND / PAYLOAD_BLIND / X2_VISIBLE / A_VISIBLE (same B_t, X_t,
# n0, q, position ids, cache length, action ids, continuations, the locked xcar878 with sham=False): the X2 and A key columns
# [n0 + X2_start, n0 + A_end) are masked, V_AFTER (EVALUATION slot + V_after rows) stays visible, B is never masked. TRUE and WRONG
# V_ONLY are NOT required to be equal (they differ only in the real V_AFTER content); their mask spans must be equal.
# V_ONLY is never executed and never enters the executed reading, EFFECT, donor, recovery, Y or verdict889; V_ONLY_AUDIT is a
# separate verdict next to PAYLOAD_AUDIT and COMPONENT_AUDIT and cannot change OVERALL (the four donor blocks stay TECHNICAL_BLOCK).
# REUSE: 891.py (commit e267a657, blob a9db6e99, canonical body 61e8f47a; the executed 891 GPU cell is blob 54e8d827 with the same
# canonical body) is downloaded and hash-checked; its wrapper runs unchanged except the counted PATCHES892W (it downloads and checks
# 890.py and 889.py and builds the TEST891 text, SHA-256 1e8b6c50), then the counted RENAMES892 + PATCHES892 are applied to that
# text and it is executed. The model alone decides: the executed action is the native CAR argmax of the arm's FULL reading,
# literally through execute866. No training, LoRA, backward, RAG, text replay, hooks, router, oracle, answer fixing, override.
# GPU_NOT_RUN_BY_AUTHOR.
import time as _t892
T_CELL892 = _t892.perf_counter()                       # the single 75-minute clock starts here (before any download)
import ast as _a892, copy as _c892, hashlib as _h892, json as _j892, math as _m892, re as _r892, urllib.request as _u892
B891_URL892 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
               'e267a657fb48d3a69f08a89a40550d23fa130bac/891.py')
B891_BLOB892 = 'a9db6e99a9551cf470f7b49e3bd45ff155a43fc9'
B891_SHA892 = 'a755fb682c92e97c99e0000fcb355b92e091088ba3849a63a54c19674f504602'
B891_BODY_LOCK892 = '61e8f47aa02a5046fbba3781f2ccf33a7710f9f037e6c1fd35b7e390ec1fabca'  # canonical body, not a file SHA
SRC889_891_SHA892 = '1e8b6c507d77a8669ce27c30a17ede63619283ca8a63a154a52c7010397bc89a'  # the TEST891 text (= executed on the GPU)
EXEC891_GPU892 = {'git_blob': '54e8d8273493e38b5320866805df922e1fbb4fdc',
                  'sha256': 'eb773ad47ff7d2cb4980e1c66b7021a2f8f1515a8794192552ea4365f96873cb', 'body_lock': B891_BODY_LOCK892,
                  'executed_sha256': SRC889_891_SHA892,
                  'log': '891.log (repo commit e267a657, git blob 3aec27f4, sha256 acbf0a81586b58cb5387809744da4d38845ecb4c11833183b7ec9b85d10a59a0)',
                  'note': 'the executed 891 paste is not in the repo: its canonical body and its generated text equal the repo file; the '
                          'raw byte difference is not characterized (the same holds for the 890 and 889 pastes); the repo file is the source'}
PATCHES892W = (                                                                 # (label, old, new, count) on the 891 cell body
    ('clock', 'T_CELL891 = _t891.perf_counter()', 'T_CELL891 = T_CELL892', 1),
    ('no_891_exec', "exec(compile(SRC889_891, '889.py:patched_for_TEST890_TEST891', 'exec'), globals())",
     "pass  # TEST892: the TEST891 text is executed only after PATCHES892 (below)", 1),
    ('chain_file', "'TEST891_executed_889_890_891.py'", "'TEST892_891chain_executed_889_890_891.py'", 1),
    ('source891_cell', "C = _a891.parse((ROOT864 / 'TEST891.py').read_text(encoding='utf-8'))", "C = _a891.parse(W891_892)", 1),
    ('st_locks', "lk = '# TEST891 BODY-SHA256 '", "lk = '# TEST892 BODY-SHA256 '", 2),          # st890 (via PATCHES891W) and st891
    ('st890_lock2', "lk.replace('TEST891', 'TEST889')", "lk.replace('TEST892', 'TEST889')", 1),
    ('st891_lock2', "lk.replace('TEST891', 'TEST890')", "lk.replace('TEST892', 'TEST890')", 1))
RENAMES892 = (('TEST891', 'TEST892', 50), ("'T891 ", "'T892 ", 2), ("'T891_", "'T892_", 4), ('891_engine.log', '892_engine.log', 1),
              ('891_events.jsonl', '892_events.jsonl', 1))                        # I/O names and console tags of the TEST891 text
MODES_T892 = "('FULL', 'SHAM', 'BLIND', 'PAYLOAD_BLIND', 'X2_VISIBLE', 'A_VISIBLE', 'V_ONLY')"
MODES_W892 = "('FULL', 'BLIND', 'PAYLOAD_BLIND', 'X2_VISIBLE', 'A_VISIBLE', 'V_ONLY')"
PATCHES892 = (                                                                  # (label, old, new, count) on the renamed TEST891 text
    ('prereg', 'PREREG889.update(PREREG891)\n', 'PREREG889.update(PREREG891)\nPREREG889.update(PREREG892)\n', 1),
    ('runtime_scan', "'calls_gate891', 'record_problems891')",
     "'calls_gate891', 'record_problems891', 'v_only_mask892', 'top_two892', 'v_only_fields892',\n"
     "                  'record_problems892', 'v_only_class892', 'v_only_audit892')", 1),
    ('read_mask', "CM = comp_masks891(entry['provenance']['spans_body'], n0, q)",
     "CM = v_only_mask892(comp_masks891(entry['provenance']['spans_body'], n0, q), n0, q)", 1),
    ('modes_true', "first, ('FULL', 'SHAM', 'BLIND', 'PAYLOAD_BLIND', 'X2_VISIBLE', 'A_VISIBLE'))", 'first, %s)' % MODES_T892, 1),
    ('modes_wrong', "first, ('FULL', 'BLIND', 'PAYLOAD_BLIND', 'X2_VISIBLE', 'A_VISIBLE'))", 'first, %s)' % MODES_W892, 1),
    ('point_fields', "pt.update(component_fields891(rT, rW, cT, cW))",
     "pt.update(component_fields891(rT, rW, cT, cW)); pt.update(v_only_fields892(rT, rW, cT, cW))", 1),
    ('v_only_gate', "                        if not comp_eq: raise Gate883('PHYSICAL_COMPONENT_VISIBLE_LEAK %s t%d' % (ep_id, t))\n",
     "                        if not comp_eq: raise Gate883('PHYSICAL_COMPONENT_VISIBLE_LEAK %s t%d' % (ep_id, t))\n"
     "                        if not (pt['v_only_spans_true_equals_wrong'] and pt['v_only_geometry_ok']): raise Gate883('PHYSICAL_V_ONLY_MASK_PARITY %s t%d' % (ep_id, t))\n", 1),
    ('capture_tree', "_a889.parse(SRC889_891 + '\\n' + W890_891 + '\\n' + src)",
     "_a889.parse(SRC889_892 + '\\n' + W890_891 + '\\n' + W891_892 + '\\n' + src)", 1),
    ('lock_diag', "lock['diag891'] = lockdiag891(src)", "lock['diag892'] = lockdiag892(src)", 1),
    ('g0_source', "capture889(); source890(); source891()\n", "capture889(); source890(); source891(); source892()\n", 1),
    ('g0_selftest', "'891': st891()}", "'891': st891(), '892': st892()}", 1),
    ('audit', "    U_ = unique_safe891(pts_)\n",
     "    try:\n        STATE889['v_only_audit'] = v_only_audit892(STATE889['verdict'], pts_)\n"
     "    except BaseException as exc:\n        STATE889['v_only_audit'] = v_audit_error892(exc)   # TECHNICAL_BLOCK, never NOT_MEASURED\n"
     "    U_ = unique_safe891(pts_)\n", 1),
    ('report', "'component_audit': STATE889['component_audit'],",
     "'component_audit': STATE889['component_audit'], 'v_only_audit': STATE889['v_only_audit'],\n"
     "        'base891': B891_INFO892, 'executed_891_gpu_cell': EXEC891_GPU892,", 1),
    ('report_points', "'cartridge_sha_wrong')) for p_ in U_],",
     "'cartridge_sha_wrong', 'a_true_v_only', 'a_wrong_v_only', 'true_v_only',\n"
     "                                                 'wrong_v_only', 'v_only_token_logps', 'v_only_reading_fields', 'top_two_true_v_only',\n"
     "                                                 'top_two_wrong_v_only', 'top_two_full', 'v_only_tw_exact', 'v_only_eq_payload_true',\n"
     "                                                 'v_only_eq_payload_wrong', 'tv_v_only_tw', 'tv_v_only_true_payload', 'tv_v_only_wrong_payload',\n"
     "                                                 'tv_full_tw', 'tv_full_blind_true', 'J', 'v_minus_payload_seq_logp', 'v_only_spans',\n"
     "                                                 'v_only_spans_true_equals_wrong', 'v_only_geometry_ok', 'calls_v_only')) for p_ in U_],", 1),
    ('console_point', "p_['component_spans']['mask_A_VISIBLE']))\n",
     "p_['component_spans']['mask_A_VISIBLE']))\n"
     "            print('      V_ONLY T/W=%s/%s top2 T=%s W=%s TV(Tv,Wv)=%.4f TV(Tv,Tp)=%.4f TV(Wv,Wp)=%.4f T==W=%s V==P T/W=%s/%s mask=%s class=%s' % (\n"
     "                p_['a_true_v_only'], p_['a_wrong_v_only'], p_['top_two_true_v_only'], p_['top_two_wrong_v_only'], p_['tv_v_only_tw'],\n"
     "                p_['tv_v_only_true_payload'], p_['tv_v_only_wrong_payload'], p_['v_only_tw_exact'], p_['v_only_eq_payload_true'],\n"
     "                p_['v_only_eq_payload_wrong'], p_['v_only_spans']['mask_V_ONLY'], v_only_class892(p_)))\n", 1),
    ('console_dists', "'true_x2_visible', 'true_a_visible'):", "'true_x2_visible', 'true_a_visible', 'true_v_only', 'wrong_v_only'):", 1),
    ('console_verdict', "          {k_: s_.get('classes') for k_, s_ in (ca_.get('strata') or {}).items()}))\n",
     "          {k_: s_.get('classes') for k_, s_ in (ca_.get('strata') or {}).items()}))\n"
     "    va_ = STATE889.get('v_only_audit') or {}\n"
     "    print('V_ONLY_AUDIT NATIVE_OUTCOME_ACTION_SEPARATION=%s (%s) | V_CONTENT_DISTRIBUTION_EFFECT=%s | readout_abandon_criterion=%s | classes=%s' % (\n"
     "          va_.get('NATIVE_OUTCOME_ACTION_SEPARATION'), va_.get('reason'), va_.get('V_CONTENT_DISTRIBUTION_EFFECT'),\n"
     "          (va_.get('readout_abandon_criterion') or {}).get('met'), {r_.get('stratum'): r_.get('class') for r_ in (va_.get('points') or [])}))\n", 1),
    ('receipt', "'component_audit': (STATE889.get('component_audit') or {}).get('COMPONENT_AUDIT')}",
     "'component_audit': (STATE889.get('component_audit') or {}).get('COMPONENT_AUDIT'),\n"
     "           'v_only_audit': (STATE889.get('v_only_audit') or {}).get('NATIVE_OUTCOME_ACTION_SEPARATION')}", 1))
CHANGED_FUNCS892 = ('capture889', 'episode889', 'read889')        # against the TEST891 text; every other function AST-identical
OWN_FUNCS892 = ('canon892', 'base891_892', 'lockdiag892', 'v_only_mask892', 'top_two892', 'v_only_fields892', 'record_problems892',
                'v_only_class892', 'v_only_audit892', 'v_audit_error892', 'source892', 'st892')
# LINEDIG892: sha256[:4] of every canonical body line except its own data lines (paste diagnostics only, not a lock)
LINEDIG892 = (
    'fc6e54738f00c0fa208a84bef2bc06863b0218bce9a4b0ca255d49c48716b22f1523a8905777155dae902934670eb237'  #LD890
    '5f0254219df93ab804245b2824bbd3c8b784681b4862a88152e20b2a9b8291cf3f3b9420a4b421049bb171fa9d496c30'  #LD890
    '51650b2f2e27546315e3499205dbbeb09c7e7a377654b4dea9a800ed8fb2c74c5efe76b20c33819405ca66bc209a325e'  #LD890
    'e5b5a207e29124e603d735e30099618b574bdc742ad5ec524f843dd0f8c9fff6b3a1028315c1f9520e437569a4c96f07'  #LD890
    '9e61e214fb0891e6c50d996307c6f3ccb97954071d867d1d5b5bf05e50285d6ab2a9070068f88761fd4bcd7ff6855e0f'  #LD890
    '069225adc94f6d39d77f00edf330887b394b454fbb99fecc916c204cf9fa168694551f71b174ff7715abd1300c0e0675'  #LD890
    '4f265b71e6edd3e381308dc41f3f912406eae6d9d3d2816651feeab80e19fab6d7f43bf2bd91261b9837a89280bbb6e8'  #LD890
    '1d609d6fcec9b1d361ec09c9e236bd427e8ea746b1ac33afd39db05e179e153e56a39880e224402849d1e8f4f758cd79'  #LD890
    'febe672d588fd9de1d948bc644f832ccf0d341974b984373213fbe83979074675444656910530c825adf9ebcc1de6a42'  #LD890
    'ea3537920e7a5e80520526272efe77ef0f8b2775bbe6f4caf198a41523686af8bfc9e57a5c66b180642681e89ea34840'  #LD890
    '61d6fce212e22de12ea12eb84bb1091265ba79d5ddd19ee4a23d63176832c351ff0bd5516da8013f3991a2861933809a'  #LD890
    '4d39564865c387c84c9d07dbb1d7bc0ae4e312d9270feb064ab98471c559167c31e02730163449401f78fa2ae6880c13'  #LD890
    '03828bcb08bd85d8edbb4cbcf13ee92e5a36354ae6fac43fac774599d5b46beed3a1be750bb3a784086e7ce0cbcb36e7'  #LD890
    '37acb7519e2edea86921d98396b1be0dcaacd95794c2a0d7c5e47f30e9ac1d94444c3e492dd3f3a508782169d8c864bb'  #LD890
    '430b44296e958989d615f2abd6a1abb49cff8ac8a683cb27b38971ab2f0c77846e2a7e80d2e4aedd3ca8b1b0f4b3087c'  #LD890
    'a40746ad5402725dbea9c321bafd20d6f896ee600c57c5784c1ec509c4b5617e283cc27a1b6df752591c4502a0da7521'  #LD890
    '72c0b40fed9ccf29890aa500f07a7607ec8dafef4c8417a8cd202b4e464b56b222c303b3b29bb07e2ebda677640611af'  #LD890
    '93fcc99e7fd4ddee4c03d5276ccec179f5ff358ea1ad88439a8832f9b1e927dbcc945d75aa6a81aa552ac263a523063e'  #LD890
    '5f8e44f48f83f18ba78572e4bf5f852c6b08f021463b185cac7a54e0a30cd5871e5647f7dc9b4660cab68f8dce1b7b82'  #LD890
    'f5299da88b74522852a621ef678aec7719f61699ffe3c3b9c993e1c6e9a595ee65f27fb68c2fc42319a3f1c863df27a4'  #LD890
    '5388142bd586c5d4f43b735c1aef59ef890b0f18b25f268f4cea3073a9d101eb41e9d5f2d6ea227fc4a76e3d8fa49c18'  #LD890
    'b1f9e843463a17c805fb0aa5d9dcf4c4616b'  #LD890
    )  #LD890


def canon892(t):
    # the paste-stable canonical form of body_lock889 / canon_lines_m867 (needed before the 891 wrapper is loaded)
    t = t.replace('\r\n', '\n').replace('\r', '\n').replace('\u00a0', ' ')
    for z in ('\ufeff', '\u200b', '\u200c', '\u200d', '\u2060'): t = t.replace(z, '')
    return [l.rstrip() for l in t.split('\n') if l.strip()]


def base891_892(raw):
    blob = _h892.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()
    assert blob == B891_BLOB892 and _h892.sha256(raw).hexdigest() == B891_SHA892, ('BASE_891_LOCK', blob)
    head, rest = raw.decode('utf-8').split('\n', 1)
    m = _r892.fullmatch(r'#\s*TEST891\s+BODY-SHA256\s+([0-9a-f]{64})', head.strip())
    assert m and m.group(1) == B891_BODY_LOCK892, 'BASE_891_HEADER_LOCK'
    assert _h892.sha256(('\n'.join(canon892(rest)) + '\n').encode()).hexdigest() == B891_BODY_LOCK892, 'BASE_891_BODY_LOCK'
    for label, old, new, n in PATCHES892W:
        if rest.count(old) != n: raise AssertionError(('BASE_891_PATCH', label, rest.count(old), n))
        rest = rest.replace(old, new)
    _a892.parse(rest)
    return rest, {'url': B891_URL892, 'git_blob': blob, 'sha256': B891_SHA892, 'body_lock': B891_BODY_LOCK892,
                  'wrapper_patches': [[p[0], p[3]] for p in PATCHES892W], 'wrapper_sha256': _h892.sha256(rest.encode()).hexdigest()}


try:
    with _u892.urlopen(_u892.Request(B891_URL892, headers={'User-Agent': 'AKBASCORE-TEST892'}), timeout=240) as _r:
        B891_RAW892 = _r.read()
    W891_892, B891_INFO892 = base891_892(B891_RAW892)
except BaseException as _exc892:
    import traceback as _tb892
    _p892 = '/content/TEST892_PRE_BASE_ERROR_%s.txt' % _t892.strftime('%Y%m%dT%H%M%SZ', _t892.gmtime())
    try:
        with open(_p892, 'w', encoding='utf-8') as _f892: _f892.write(_tb892.format_exc())
    except OSError: _p892 = 'NOT_WRITTEN'
    print('TEST892 PRE-BASE ERROR (nothing loaded):', type(_exc892).__name__, _exc892, '| traceback:', _p892)
    raise
exec(compile(W891_892, '891.py:wrapper_for_TEST892', 'exec'), globals())   # 891 cell: downloads + checks 890 / 889, builds SRC889_891
assert _h892.sha256(SRC889_891.encode()).hexdigest() == SRC889_891_SHA892, 'BASE_891_CHAIN_NOT_REPRODUCED'
RENAMED891_892 = apply890(SRC889_891, [('rename',) + r for r in RENAMES892])
assert 'TEST891' not in RENAMED891_892, 'BASE_891_RENAME_LEFT'
SRC889_892 = apply890(RENAMED891_892, PATCHES892)
_a892.parse(SRC889_892)
B891_INFO892.update(chain_891_sha256=SRC889_891_SHA892, renames892=[list(r) for r in RENAMES892],
                    patches892=[[p[0], p[3]] for p in PATCHES892], executed_sha256=_h892.sha256(SRC889_892.encode()).hexdigest(),
                    w890_891_sha256=_h892.sha256(W890_891.encode()).hexdigest())
print('TEST892 BASE891', _j892.dumps({k: B891_INFO892[k] for k in ('git_blob', 'sha256', 'body_lock', 'chain_891_sha256',
                                                                   'executed_sha256')}, sort_keys=True))

# ============================ sealed audit design (fixed before the model is loaded) ============================
TAU892, MIN_RAW892 = 0.05, 14                                                    # K3.1 7.7: TV threshold and minimum raw records
V_FLAGS892 = ('mask_v_only_is_X2_and_A', 'mask_v_only_leaves_V', 'mask_v_only_no_B', 'mask_v_only_complement_is_V')
INTEGRITY892 = ('blind_true_equals_wrong_bitwise', 'payload_true_equals_wrong_bitwise', 'x2v_true_equals_wrong_bitwise',
                'av_true_equals_wrong_bitwise', 'component_geometry_ok', 'component_spans_true_equals_wrong',
                'v_only_spans_true_equals_wrong', 'v_only_geometry_ok')
PREREG892 = {
    'test': 'TEST892 V_ONLY_OUTCOME_CAUSAL_READ (TEST891 COMPONENT, TEST890 PAYLOAD and the TEST889 run otherwise unchanged)',
    'contract': 'K3.1 TEST891 GPU root cause + TEST892 DESIGN_LOCKED (7.1-7.7) + CLAUDE TEST892 GOREV TALIMATI (16 Nov 2026)',
    'base891': B891_INFO892, 'executed_891_gpu_cell': EXEC891_GPU892,
    'v_only_read': 'per eligible point, per cartridge (TRUE and WRONG separately), on the same single load_exp878 + append_exp878 as the '
                   'other modes: xcar878(env, g, X, [[n0 + X2_start, n0 + A_end]], sham=False); the mask is the union of the X2 and A key '
                   'columns, V_AFTER [n0 + V_start, n0 + q) (EVALUATION slot + V_after rows) visible, no B column; mask union V_AFTER = '
                   'the PAYLOAD_BLIND key set; spans from the writer via the strict comp_masks891; TRUE and WRONG V_ONLY mask spans equal '
                   '(else PHYSICAL_V_ONLY_MASK_PARITY), readings are NOT required equal; exactly one budget call (5 forwards) per read '
                   '(calls_gate891); +2 reads per raw point (TRUE 7, WRONG 6); never executed',
    'measures': 'per point: TRUE / WRONG V_ONLY six-action unrounded p, first_logp, sequence_logp, all token logps, mass, abstain, '
                'argmax, action, margin_logp, ordered top-two (by sequence_logp, ties by the fixed action order); same_reading881 TRUE vs '
                'WRONG and V_ONLY vs PAYLOAD; TV(Tv,Wv), TV(Tv,Tp), TV(Wv,Wp), TV(T FULL, W FULL), TV(T FULL, T BLIND); J_w = (p_Tv - p_Tp) '
                '- (p_Wv - p_Wp) and its sequence_logp analogue; V_ONLY - PAYLOAD sequence_logp per arm; spans, calls, cartridge SHAs',
    'expected_strata': ['%s_%s_t%d' % s for s in EXPECTED891], 'primary_strata': ['%s_%s_t%d' % s for s in PRIMARY890],
    'minimum_evidence': 'all physical gates PASS; >= %d well-formed raw records in the seven expected strata; every expected stratum '
                        'present; every raw duplicate of a unique point gives the same (TRUE, WRONG) V_ONLY action pair and top-two' % MIN_RAW892,
    'verdict': 'NATIVE_OUTCOME_ACTION_SEPARATION, in this order: no point -> NOT_MEASURED / NO_POINTS; PHYSICAL_READ != PASS or any '
               'strict bool False integrity flag on a raw point -> TECHNICAL_BLOCK / PHYSICAL_OR_PARITY_OR_GEOMETRY; unexpected audit '
               'exception -> TECHNICAL_BLOCK / AUDIT_ERROR; malformed record -> INCONCLUSIVE / INCOMPLETE_RECORDS; expected stratum absent '
               'or < %d raw -> INCONCLUSIVE / INCOMPLETE_EXPECTED_POINTS; duplicate mismatch -> INCONCLUSIVE / DUPLICATE_MISMATCH; '
               'SEP(point) = TRUE/WRONG V_ONLY argmax differ AND TV(Tv,Wv) >= %.2f AND ordered top-two differ; PASS if SEP on >= 1 '
               'primary of world 10 AND >= 1 primary of world 09; NEGATIVE if no argmax and no top-two change on any of the unique points '
               '(sub-label DISTRIBUTION_ONLY if any TRUE/WRONG V_ONLY reading differs, else NO_TRUE_WRONG_DIFFERENCE); otherwise '
               'INCONCLUSIVE / FLIP_WITH_TV_BELOW_TAU, ONE_WORLD_ONLY, SECONDARY_ONLY or TOP_TWO_ONLY (first that applies); no specific '
               'action is ever the right one' % (MIN_RAW892, TAU892),
    'distribution_axis': 'V_CONTENT_DISTRIBUTION_EFFECT (only with the minimum evidence): PRESENT if each world has >= 1 primary with '
                         'TV(Tv,Wv) >= %.2f; ABSENT if every primary TRUE/WRONG V_ONLY pair is same_reading881 exact; else MIXED' % TAU892,
    'point_class': 'NO_V_ONLY_EFFECT (V_ONLY == PAYLOAD exact, both arms), V_VISIBILITY_WITHOUT_CONTENT_SEPARATION (V_ONLY != PAYLOAD, '
                   'TRUE == WRONG exact), OUTCOME_CONTENT_DISTRIBUTION_EFFECT (TRUE != WRONG, same argmax), OUTCOME_ACTION_ARGMAX_SEPARATION '
                   '(TRUE / WRONG argmax differ); descriptive only, no majority',
    'readout_abandon_criterion': 'minimum evidence AND V_ONLY != PAYLOAD on a primary AND distribution PRESENT AND no TRUE/WRONG V_ONLY '
                                 'argmax or top-two change on any unique point AND no TRUE/WRONG FULL argmax or top-two change AND no '
                                 'FORK cell with Y(D_TRUE) > Y(D_WRONG): the SSD V_AFTER -> CAR readout does not turn outcome content '
                                 'into a decision; then stop mask variants and redesign outcome encoding / transition target / action '
                                 'interface (not a proof that a frozen model cannot learn)',
    'v_only_scope': 'audit only: OUTCOME_BENEFIT stays NOT_MEASURED, OVERALL / TECHNICAL_STATUS / PAYLOAD_AUDIT / COMPONENT_AUDIT unchanged; '
                    'a V_ONLY separation is not outcome credit, semantic binding, self-correction or learning'}


def lockdiag892(src):
    # the TEST890 line diagnostics with the TEST892 line table (same '#LD890' data-line marker)
    keep = LINEDIG890; globals()['LINEDIG890'] = LINEDIG892
    try: return lockdiag890(src)
    finally: globals()['LINEDIG890'] = keep


def v_only_mask892(cm, n0, q):
    # adds the V_ONLY key mask [X2 + A] to the strict comp_masks891 result; geometry already gated there (fail-closed)
    rec = cm['record']; X, A, V = rec['x2_span'], rec['a_span'], rec['v_span']
    m = [[X[0], A[1]]]
    keys = lambda spans: set(k for s in spans for k in range(s[0], s[1]))
    km, kx, ka, kv, kp = keys(m), keys([X]), keys([A]), keys([V]), keys([[n0, n0 + q]])
    out = {'masks': dict(cm['masks'], V_ONLY=m), 'record': dict(rec, mask_V_ONLY=m)}
    out['record'].update({'mask_v_only_is_X2_and_A': km == kx | ka, 'mask_v_only_leaves_V': not (km & kv),
                          'mask_v_only_no_B': min(km) >= n0, 'mask_v_only_complement_is_V': kp - km == kv})
    return out


def top_two892(r):
    # ordered top-two actions by sequence_logp (ties by the fixed ACTIONS_M867 order); unrounded
    sq = {s['word']: float(s['sequence_logp']) for s in r['scores']}
    return sorted(ACTIONS_M867, key=lambda w: (-sq[w], ACTIONS_M867.index(w)))[:2]


def v_only_fields892(rT, rW, cT, cW):
    # the point record of the two V_ONLY reads; never fed back into a decision
    TV, WV, TP, WP = rT['V_ONLY'], rW['V_ONLY'], rT['PAYLOAD_BLIND'], rW['PAYLOAD_BLIND']
    nm = lambda r: {w: float(r['normalized'][w]) for w in ACTIONS_M867}
    sq = lambda r: {s['word']: float(s['sequence_logp']) for s in r['scores']}
    ntv, nwv, ntp, nwp, stv, swv, stp, swp = nm(TV), nm(WV), nm(TP), nm(WP), sq(TV), sq(WV), sq(TP), sq(WP)
    rf = lambda r: {'action': r['action'], 'argmax_word': r['argmax_word'], 'abstain': bool(r['abstain']), 'mass': float(r['mass']),
                    'margin_logp': float(r['margin_logp'])}
    return {'a_true_v_only': TV['action'], 'a_wrong_v_only': WV['action'], 'true_v_only': summary_m888(TV), 'wrong_v_only': summary_m888(WV),
            'v_only_token_logps': {a: {s['word']: [float(x) for x in s['token_logps']] for s in r['scores']} for a, r in (('true', TV), ('wrong', WV))},
            'v_only_reading_fields': {'true': rf(TV), 'wrong': rf(WV)},
            'top_two_true_v_only': top_two892(TV), 'top_two_wrong_v_only': top_two892(WV),
            'top_two_full': {'true': top_two892(rT['FULL']), 'wrong': top_two892(rW['FULL'])},
            'v_only_tw_exact': same_reading881(TV, WV), 'v_only_eq_payload_true': same_reading881(TV, TP), 'v_only_eq_payload_wrong': same_reading881(WV, WP),
            'tv_v_only_tw': tv_m867(TV, WV), 'tv_v_only_true_payload': tv_m867(TV, TP), 'tv_v_only_wrong_payload': tv_m867(WV, WP),
            'tv_full_tw': tv_m867(rT['FULL'], rW['FULL']), 'tv_full_blind_true': tv_m867(rT['FULL'], rT['BLIND']),
            'J': {'p': {w: (ntv[w] - ntp[w]) - (nwv[w] - nwp[w]) for w in ACTIONS_M867},
                  'seq_logp': {w: (stv[w] - stp[w]) - (swv[w] - swp[w]) for w in ACTIONS_M867}},
            'v_minus_payload_seq_logp': {'true': {w: stv[w] - stp[w] for w in ACTIONS_M867}, 'wrong': {w: swv[w] - swp[w] for w in ACTIONS_M867}},
            'v_only_spans': {'mask_V_ONLY': cT['mask_V_ONLY'], 'v_span': cT['v_span']},
            'v_only_spans_true_equals_wrong': cT['mask_V_ONLY'] == cW['mask_V_ONLY'] and cT['v_span'] == cW['v_span'],
            'v_only_geometry_ok': all(c.get(k) is True for c in (cT, cW) for k in V_FLAGS892),
            'calls_v_only': [cT.get('calls_V_ONLY'), cW.get('calls_V_ONLY')]}


def record_problems892(p):
    # preflight of every V_ONLY field v_only_audit892 reads (on top of record_problems891); [] = well formed
    if not isinstance(p, dict): return ['NOT_A_DICT']
    fin = lambda x: type(x) in (int, float) and _m892.isfinite(x)
    six = lambda d: isinstance(d, dict) and set(d) == set(ACTIONS_M867) and all(fin(x) for x in d.values())
    act = set(ACTIONS_M867) | {'INVALID'}
    bad = [k for k in ('a_true_v_only', 'a_wrong_v_only') if p.get(k) not in act]
    bad += ['%s.%s' % (k, f) for k in ('true_v_only', 'wrong_v_only', 'true_full', 'wrong_full') for f in ('p', 'seq_logp', 'first_logp')
            if not (isinstance(p.get(k), dict) and six(p[k].get(f)))]
    bad += ['J.%s' % f for f in ('p', 'seq_logp') if not (isinstance(p.get('J'), dict) and six(p['J'].get(f)))]
    two = lambda x: isinstance(x, list) and len(x) == 2 and all(w in ACTIONS_M867 for w in x) and x[0] != x[1]
    bad += [k for k in ('top_two_true_v_only', 'top_two_wrong_v_only') if not two(p.get(k))]
    tf = p.get('top_two_full')
    bad += ['top_two_full'] if not (isinstance(tf, dict) and two(tf.get('true')) and two(tf.get('wrong'))) else []
    bad += [k for k in ('v_only_tw_exact', 'v_only_eq_payload_true', 'v_only_eq_payload_wrong', 'v_only_spans_true_equals_wrong',
                        'v_only_geometry_ok') if type(p.get(k)) is not bool]
    bad += [k for k in ('tv_v_only_tw', 'tv_v_only_true_payload', 'tv_v_only_wrong_payload', 'tv_full_tw', 'tv_full_blind_true')
            if not (fin(p.get(k)) and 0 <= p[k] <= 1)]
    sp2 = lambda x: isinstance(x, (list, tuple)) and len(x) == 2 and all(type(e) is int for e in x)
    vs = p.get('v_only_spans')
    if not (isinstance(vs, dict) and isinstance(vs.get('mask_V_ONLY'), (list, tuple)) and len(vs['mask_V_ONLY']) == 1 and
            sp2(vs['mask_V_ONLY'][0]) and sp2(vs.get('v_span')) and vs['mask_V_ONLY'][0][1] == vs['v_span'][0]): bad += ['v_only_spans']
    cv = p.get('calls_v_only')
    if not (isinstance(cv, list) and len(cv) == 2 and all(type(c) is int and c == 1 for c in cv)): bad += ['calls_v_only']
    return bad


def v_only_class892(p):
    # descriptive mechanism class of one point (K3.1 7.3); no verdict
    if p['a_true_v_only'] != p['a_wrong_v_only']: return 'OUTCOME_ACTION_ARGMAX_SEPARATION'
    if not p['v_only_tw_exact']: return 'OUTCOME_CONTENT_DISTRIBUTION_EFFECT'
    if p['v_only_eq_payload_true'] and p['v_only_eq_payload_wrong']: return 'NO_V_ONLY_EFFECT'
    return 'V_VISIBILITY_WITHOUT_CONTENT_SEPARATION'


def v_only_audit892(verdict, points):
    # read-only on verdict889 and the points; coverage over the seven fixed strata; malformed records kept and listed
    chk = [(p, (record_problems891(p) + record_problems892(p)) if isinstance(p, dict) else ['NOT_A_DICT']) for p in points]
    malformed = [{'index': i, 'episode_id': p.get('episode_id') if isinstance(p, dict) else None, 'problems': b} for i, (p, b) in enumerate(chk) if b]
    false_flags = [{'index': i, 'flags': [k for k in INTEGRITY892 if p.get(k) is False]} for i, p in enumerate(points)
                   if isinstance(p, dict) and any(p.get(k) is False for k in INTEGRITY892)]   # raw points, before the malformed filter
    good = [p for p, b in chk if not b]; U = unique_m888(good)
    name = lambda s: '%s_%s_t%d' % s
    sig = lambda p: (p['a_true_v_only'], p['a_wrong_v_only'], tuple(p['top_two_true_v_only']), tuple(p['top_two_wrong_v_only']))
    dup = sorted({p['unique_key'] for p in good if len({sig(x) for x in good if x['unique_key'] == p['unique_key']}) > 1})
    rows = []
    for p in U:
        s = (p['world'], p['condition'], p['step'])
        r = {'episode_id': p['episode_id'], 'stratum': name(s), 'world': p['world'], 'primary': s in PRIMARY890,
             'expected': s in EXPECTED891, 'a_true_v_only': p['a_true_v_only'], 'a_wrong_v_only': p['a_wrong_v_only'],
             'top_two_true_v_only': p['top_two_true_v_only'], 'top_two_wrong_v_only': p['top_two_wrong_v_only'],
             'tv_v_only_tw': p['tv_v_only_tw'], 'v_only_tw_exact': p['v_only_tw_exact'], 'v_only_eq_payload_true': p['v_only_eq_payload_true'],
             'v_only_eq_payload_wrong': p['v_only_eq_payload_wrong'], 'tv_v_only_true_payload': p['tv_v_only_true_payload'],
             'tv_v_only_wrong_payload': p['tv_v_only_wrong_payload'], 'J': p['J'], 'a_true_full': p['a_true'], 'a_wrong_full': p['a_wrong'],
             'top_two_full': p['top_two_full'], 'class': v_only_class892(p)}
        r['flip'] = r['a_true_v_only'] != r['a_wrong_v_only']; r['top_two_change'] = r['top_two_true_v_only'] != r['top_two_wrong_v_only']
        r['sep'] = r['flip'] and r['tv_v_only_tw'] >= TAU892 and r['top_two_change']
        rows.append(r)
    exp = [r for r in rows if r['expected']]; prim = [r for r in rows if r['primary']]
    raw_exp = sum(1 for p in good if (p['world'], p['condition'], p['step']) in EXPECTED891)
    strata = {name(s): {'unique_points': sum(1 for r in rows if r['stratum'] == name(s)), 'primary': s in PRIMARY890,
                        'classes': [r['class'] for r in rows if r['stratum'] == name(s)],
                        'raw_records': sum(1 for p in good if (p['world'], p['condition'], p['step']) == s)} for s in EXPECTED891}
    cov = {'expected': [name(s) for s in EXPECTED891], 'not_occurred': [k for k, v in strata.items() if not v['unique_points']],
           'raw_expected_records': raw_exp, 'min_raw': MIN_RAW892, 'incomplete_records': malformed, 'false_integrity_flags': false_flags,
           'duplicate_mismatch': dup, 'unexpected_strata_descriptive': [r for r in rows if not r['expected']]}
    evidence = False
    if not points: a, why = 'NOT_MEASURED', 'NO_POINTS'
    elif verdict.get('PHYSICAL_READ') != 'PASS' or false_flags: a, why = 'TECHNICAL_BLOCK', 'PHYSICAL_OR_PARITY_OR_GEOMETRY'
    elif malformed: a, why = 'INCONCLUSIVE', 'INCOMPLETE_RECORDS'
    elif cov['not_occurred'] or raw_exp < MIN_RAW892: a, why = 'INCONCLUSIVE', 'INCOMPLETE_EXPECTED_POINTS'
    elif dup: a, why = 'INCONCLUSIVE', 'DUPLICATE_MISMATCH'
    else:
        evidence = True
        w10, w09 = [any(r['sep'] for r in prim if r['world'] == w) for w in ('10', '09')]
        if w10 and w09: a, why = 'PASS', 'BOTH_WORLDS_PRIMARY_SEPARATION'
        elif not any(r['flip'] or r['top_two_change'] for r in exp):
            a, why = 'NEGATIVE', ('DISTRIBUTION_ONLY' if any(not r['v_only_tw_exact'] for r in exp) else 'NO_TRUE_WRONG_DIFFERENCE')
        elif any(r['flip'] and r['tv_v_only_tw'] < TAU892 for r in exp): a, why = 'INCONCLUSIVE', 'FLIP_WITH_TV_BELOW_TAU'
        elif w10 or w09: a, why = 'INCONCLUSIVE', 'ONE_WORLD_ONLY'
        elif not any(r['flip'] or r['top_two_change'] for r in prim): a, why = 'INCONCLUSIVE', 'SECONDARY_ONLY'
        else: a, why = 'INCONCLUSIVE', 'TOP_TWO_ONLY'
    if not evidence: dist = 'TECHNICAL_BLOCK' if a == 'TECHNICAL_BLOCK' else 'NOT_MEASURED' if a == 'NOT_MEASURED' else 'INCONCLUSIVE'
    elif all(any(r['tv_v_only_tw'] >= TAU892 for r in prim if r['world'] == w) for w in ('10', '09')): dist = 'PRESENT'
    elif all(r['v_only_tw_exact'] for r in prim): dist = 'ABSENT'
    else: dist = 'MIXED'
    Y = (verdict.get('reasons') or {}).get('Y') or {}
    fork = [(Y.get('D_TRUE_%s_FORK' % w), Y.get('D_WRONG_%s_FORK' % w)) for w in ('10', '09')]
    crit = {'minimum_evidence': evidence, 'v_channel_present': any(not (r['v_only_eq_payload_true'] and r['v_only_eq_payload_wrong']) for r in prim),
            'distribution_present': dist == 'PRESENT', 'no_v_only_action_change': evidence and not any(r['flip'] or r['top_two_change'] for r in exp),
            'no_full_action_change': evidence and not any(r['a_true_full'] != r['a_wrong_full'] or r['top_two_full']['true'] != r['top_two_full']['wrong'] for r in exp),
            'fork_true_over_wrong': None if any(y is None for f in fork for y in f) else any(t > w for t, w in fork), 'fork_Y': fork}
    crit['met'] = all(crit[k] for k in ('minimum_evidence', 'v_channel_present', 'distribution_present', 'no_v_only_action_change',
                                        'no_full_action_change')) and crit['fork_true_over_wrong'] is False
    return {'NATIVE_OUTCOME_ACTION_SEPARATION': a, 'reason': why, 'V_CONTENT_DISTRIBUTION_EFFECT': dist, 'coverage': cov, 'strata': strata,
            'points': rows, 'raw_points': len(points), 'unique_points': len(U), 'readout_abandon_criterion': crit,
            'verdict889_unchanged': {k: verdict.get(k) for k in ('TECHNICAL_STATUS', 'PHYSICAL_READ', 'CONTENT_EFFECT', 'OUTCOME_BENEFIT',
                                                                 'NATIVE_RECOVERY', 'OVERALL')},
            'scope': PREREG892['v_only_scope']}


def v_audit_error892(exc, save=True):
    # an unexpected exception inside v_only_audit892 is a technical failure of the audit, never "not measured"
    e = audit_error891(exc, save=False)
    out = {'NATIVE_OUTCOME_ACTION_SEPARATION': 'TECHNICAL_BLOCK', 'reason': e['reason'], 'V_CONTENT_DISTRIBUTION_EFFECT': 'TECHNICAL_BLOCK',
           'traceback': e['traceback']}
    if not save: return out
    try: (ROOT864 / 'TEST892_v_only_audit_error.txt').write_text(out['traceback'], encoding='utf-8'); out['traceback_file'] = 'TEST892_v_only_audit_error.txt'
    except Exception as exc2: out['traceback_file'] = 'NOT_WRITTEN %s: %s' % (type(exc2).__name__, exc2)
    return out


def source892():
    # G0, before the model: the executed text differs from the TEST891 text only in CHANGED_FUNCS892 + module statements, the
    # locked functions are untouched, and V_ONLY reaches nothing but the point record and its mask-parity gate
    T, R0 = _a892.parse(SRC889_892), _a892.parse(RENAMED891_892)
    f = {n.name: n for n in T.body if isinstance(n, _a892.FunctionDef)}; f0 = {n.name: n for n in R0.body if isinstance(n, _a892.FunctionDef)}
    W1, W0 = _a892.parse(W891_892), _a892.parse(W890_891); C = _a892.parse((ROOT864 / 'TEST892.py').read_text(encoding='utf-8'))
    fw = {n.name for t in (W1, W0) for n in t.body if isinstance(n, _a892.FunctionDef)}; fc = {n.name: n for n in C.body if isinstance(n, _a892.FunctionDef)}
    changed = sorted(k for k in set(f) | set(f0) if k not in f or k not in f0 or _a892.dump(f[k]) != _a892.dump(f0[k]))
    rd, ep = f['read889'], f['episode889']
    calls = lambda node, nm: [n for n in _a892.walk(node) if isinstance(n, _a892.Call) and getattr(n.func, 'id', None) == nm]
    xc, vm, vf, cg = calls(rd, 'xcar878'), calls(rd, 'v_only_mask892'), calls(ep, 'v_only_fields892'), calls(rd, 'calls_gate891')
    modes = sorted(_a892.unparse(n.args[10]) for n in calls(ep, 'read889'))
    has = lambda n, vals: any(isinstance(x, _a892.Constant) and x.value in vals for x in _a892.walk(n))
    reach = sorted({_a892.unparse(t) for n in _a892.walk(ep) if isinstance(n, _a892.Assign) and has(n, ('V_ONLY',)) for t in n.targets})
    reading = sorted({_a892.unparse(n.value) for n in _a892.walk(ep) if isinstance(n, _a892.Assign)
                      and any(isinstance(x, _a892.Name) and x.id == 'reading' for x in n.targets)})
    src_ep, src_rd = _a892.unparse(ep), _a892.unparse(rd)
    own = [fc[k] for k in ('v_only_mask892', 'top_two892', 'v_only_fields892', 'record_problems892', 'v_only_class892', 'v_only_audit892', 'v_audit_error892')]
    banned = {'write_exp878', 'append_exp878', 'xappend878', 'execute866', 'control_step867', 'donor_v889', 'write_pair889',
              'write_appraisal889', 'load_exp878', 'xcar878', 'car873', 'exec', 'eval', 'setattr', 'globals', 'open'}
    facts = {'chain_891_reproduced': _h892.sha256(SRC889_891.encode()).hexdigest() == SRC889_891_SHA892,
             'changed_functions': changed == list(CHANGED_FUNCS892),
             'locked_not_redefined': not any(k in fc or (k in f and k not in f0) for k in LOCKED891) and
                                     all(_a892.dump(f[k]) == _a892.dump(f0[k]) for k in LOCKED891 if k in f),
             'own_names_unique': not (set(OWN_FUNCS892) & (set(f) | fw)) and set(OWN_FUNCS892) <= set(fc),
             'single_masked_kernel_call_unchanged': len(xc) == 1 and _a892.unparse(xc[0].args[3]) ==
             "() if m == 'FULL' else [P] if m == 'PAYLOAD_BLIND' else CM['masks'][m] if m in CM['masks'] else [V]" and
             _a892.unparse(xc[0].args[4]) == "m == 'SHAM'",
             'v_only_mask_from_strict_writer_spans': len(vm) == 1 and _a892.unparse(vm[0]) ==
             "v_only_mask892(comp_masks891(entry['provenance']['spans_body'], n0, q), n0, q)" and
             src_rd.find('v_only_mask892(') < src_rd.find('for m in modes:') < src_rd.find('xcar878('),
             'call_cardinality_gate_kept': len(cg) == 1 and src_rd.find('for m in modes:') < src_rd.find('calls_gate891(rec, modes)') < src_rd.find('return (out, rec)'),
             'modes_true_wrong_repeat': modes == ["('FULL', 'BLIND', 'PAYLOAD_BLIND', 'X2_VISIBLE', 'A_VISIBLE', 'V_ONLY')",
                                                  "('FULL', 'SHAM', 'BLIND', 'PAYLOAD_BLIND', 'X2_VISIBLE', 'A_VISIBLE', 'V_ONLY')", "('FULL',)"],
             'v_only_reaches_only_point_and_gate': reach == ['(rT, cT)', '(rW, cW)'] and len(vf) == 1 and
                                                   _a892.unparse(vf[0]) == 'v_only_fields892(rT, rW, cT, cW)' and
                                                   'pt.update(v_only_fields892(rT, rW, cT, cW))' in src_ep,
             'executed_reading_unchanged': reading == ["rT['FULL'] if arm == 'D_TRUE' else rW['FULL']", 'r_none', "record['reading']"],
             'v_only_gate_after_point_record': 0 < src_ep.find("out['points'].append(pt)") < src_ep.find("raise Gate883('PHYSICAL_V_ONLY_MASK_PARITY"),
             'no_write_donor_execute_in_new_functions': not any(isinstance(x, _a892.Name) and x.id in banned for n in own for x in _a892.walk(n)),
             'audit_exception_is_technical_block': SRC889_892.count("STATE889['v_only_audit'] = v_audit_error892(exc)") == 1,
             'verdict889_has_no_v_only': 'V_ONLY' not in _a892.unparse(f['verdict889'])}
    if not all(facts.values()): raise Gate_m867('SOURCE892_FACTS %s' % sorted(k for k, v in facts.items() if not v))
    (ROOT864 / 'TEST892_executed_889_890_891_892.py').write_text(SRC889_892, encoding='utf-8')
    STATE889['source']['base891'] = B891_INFO892; STATE889['source']['facts892'] = facts
    json_write864('TEST892_base891.json', {'base891': B891_INFO892, 'executed_891_gpu_cell': EXEC891_GPU892, 'facts892': facts,
                                          'changed_functions': changed, 'before_model_load': True})
    print('T892 BASE891 PATCH facts=%s executed_sha256=%s' % (all(facts.values()), B891_INFO892['executed_sha256']), flush=True)


def st892():
    r = {}; W6 = list(ACTIONS_M867)
    sp = {'X2': [0, 10], 'A': [10, 12], 'V_AFTER': [12, 20]}; cm = v_only_mask892(comp_masks891(sp, 100, 20), 100, 20)
    r['mask_v_only_exact'] = cm['masks']['V_ONLY'] == [[100, 112]] and cm['masks']['X2_VISIBLE'] == [[110, 112], [112, 120]] \
        and all(cm['record'][k] is True for k in V_FLAGS892) and cm['record']['mask_V_ONLY'] == [[100, 112]]
    r['mask_v_only_tuple_spans_same'] = v_only_mask892(comp_masks891({k: tuple(v) for k, v in sp.items()}, 100, 20), 100, 20)['masks'] == cm['masks']
    for nm, (spx, n0x, qx) in {'float_end': (dict(sp, A=[10, 12.0]), 100, 20), 'bool_end': (dict(sp, X2=[False, 10]), 100, 20),
                               'str_end': (dict(sp, V_AFTER=['12', '20']), 100, 20), 'nan_end': (dict(sp, A=[10, float('nan')]), 100, 20),
                               'inf_end': (dict(sp, V_AFTER=[12, float('inf')]), 100, 20), 'gap': (dict(sp, A=[11, 12]), 100, 20),
                               'overlap': (dict(sp, X2=[0, 11]), 100, 20), 'missing_A': ({'X2': [0, 10], 'V_AFTER': [10, 20]}, 100, 20),
                               'bool_n0': (sp, True, 20), 'float_q': (sp, 100, 20.0), 'str_n0': (sp, '100', 20), 'zero_n0': (sp, 0, 20),
                               'container_list': ([[0, 10], [10, 12], [12, 20]], 100, 20)}.items():
        try: v_only_mask892(comp_masks891(spx, n0x, qx), n0x, qx); r['mask_refused_%s' % nm] = False
        except Gate883 as exc: r['mask_refused_%s' % nm] = 'PHYSICAL_COMPONENT_MASK_GEOMETRY' in str(exc)
    sc = lambda seq, lp2=-0.5: [{'word': w, 'ids': [i, 7], 'token_logps': [seq[w] - lp2, lp2], 'sequence_logp': seq[w]} for i, w in enumerate(W6)]
    def rd(seq, lp2=-0.5):
        z = sum(_m892.exp(v) for v in seq.values()); norm = {w: _m892.exp(seq[w]) / z for w in W6}
        o = sorted(W6, key=lambda w: (-seq[w], W6.index(w)))
        return {'action': o[0], 'argmax_word': o[0], 'abstain': False, 'mass': 0.5, 'normalized': norm, 'margin_logp': seq[o[0]] - seq[o[1]],
                'scores': sc(seq, lp2)}
    base = {w: -1.0 - 0.1 * i for i, w in enumerate(W6)}
    sT = dict(base, **{W6[4]: -0.2}); sW = dict(base, **{W6[1]: -0.3}); sP = dict(base)
    R6 = {m: rd(base) for m in ('FULL', 'BLIND', 'PAYLOAD_BLIND', 'X2_VISIBLE', 'A_VISIBLE')}
    rT = dict(R6, V_ONLY=rd(sT), PAYLOAD_BLIND=rd(sP)); rW = dict(_c892.deepcopy(R6), V_ONLY=rd(sW), PAYLOAD_BLIND=rd(sP))
    cT = dict(cm['record'], calls_V_ONLY=1); cW = dict(cm['record'], calls_V_ONLY=1)
    F = v_only_fields892(rT, rW, cT, cW)
    nt, nw, np_ = rT['V_ONLY']['normalized'], rW['V_ONLY']['normalized'], rT['PAYLOAD_BLIND']['normalized']
    r['J_unrounded'] = all(F['J']['p'][w] == (nt[w] - np_[w]) - (nw[w] - np_[w]) for w in W6) and \
        all(F['J']['seq_logp'][w] == (sT[w] - sP[w]) - (sW[w] - sP[w]) for w in W6) and abs(F['J']['seq_logp'][W6[4]] - 1.2) < 1e-12 and abs(F['J']['seq_logp'][W6[1]] + (-0.3 - base[W6[1]])) < 1e-12
    r['top_two_and_argmax'] = F['top_two_true_v_only'] == [W6[4], W6[0]] and F['top_two_wrong_v_only'] == [W6[1], W6[0]] and \
        F['a_true_v_only'] == W6[4] and F['a_wrong_v_only'] == W6[1] and top_two892(rd({w: 0.0 for w in W6})) == W6[:2]
    r['tv_values'] = F['tv_v_only_tw'] == tv_m867(rT['V_ONLY'], rW['V_ONLY']) > 0 and F['tv_v_only_true_payload'] == tv_m867(rT['V_ONLY'], rT['PAYLOAD_BLIND'])
    r['exact_flags'] = F['v_only_tw_exact'] is False and F['v_only_eq_payload_true'] is False and \
        v_only_fields892(dict(rT, V_ONLY=rd(sP)), dict(rW, V_ONLY=rd(sP)), cT, cW)['v_only_eq_payload_true'] is True
    r['token_logps_recorded'] = F['v_only_token_logps']['true'][W6[4]] == [-0.2 + 0.5, -0.5] and F['v_only_reading_fields']['wrong']['action'] == W6[1]
    r['spans_parity_and_geometry'] = F['v_only_spans_true_equals_wrong'] is True and F['v_only_geometry_ok'] is True and F['calls_v_only'] == [1, 1] and \
        v_only_fields892(rT, rW, cT, dict(cW, mask_V_ONLY=[[100, 111]]))['v_only_spans_true_equals_wrong'] is False and \
        v_only_fields892(rT, rW, cT, dict(cW, mask_v_only_leaves_V=False))['v_only_geometry_ok'] is False
    TM7 = ('FULL', 'SHAM', 'BLIND', 'PAYLOAD_BLIND', 'X2_VISIBLE', 'A_VISIBLE', 'V_ONLY')
    def cg(rec, modes):
        try: calls_gate891(rec, modes); return 'PASS'
        except Gate883 as exc: return 'GATE' if 'PHYSICAL_CALL_CARDINALITY' in str(exc) else 'OTHER'
    one = lambda modes, **kw: dict({'cartridge': 'c', **{'calls_' + m: 1 for m in modes}}, **kw)
    r['v_only_cardinality'] = cg(one(TM7), TM7) == cg(one(TM7[:1] + TM7[2:]), TM7[:1] + TM7[2:]) == 'PASS' and \
        [cg(one(TM7, calls_V_ONLY=v), TM7) for v in (0, 2, True, 1.0, '1')] == ['GATE'] * 5 and cg(one(TM7[:-1]), TM7) == 'GATE' and \
        cg(one(TM7, calls_V_ONLY_EXTRA=1), TM7) == 'GATE' and cg(one(TM7), TM7 + ('V_ONLY',)) == 'GATE'
    # audit matrix on synthetic but complete records
    CS = {k: cm['record'][k] for k in ('x2_span', 'a_span', 'v_span', 'mask_X2_VISIBLE', 'mask_A_VISIBLE')}
    def Q(s, tv_, wv_, tvv=0.2, uk=None, dup=0, **kw):
        w, c, t = s; seqT = dict(base, **{tv_: -0.2}); seqW = dict(base, **{wv_: -0.2}) if wv_ != tv_ else dict(seqT)
        p = {'episode_id': 'E%d' % dup, 'world': w, 'condition': c, 'step': t, 'a_none': 'ADVANCE', 'a_true': 'ACCEPT', 'a_wrong': 'ACCEPT',
             'a_true_blind': 'ACCEPT', 'a_true_payload_blind': 'ADVANCE', 'a_true_x2_visible': 'ADVANCE', 'a_true_a_visible': 'ADVANCE',
             'unique_key': uk or '%s%s%d' % s, 'component_spans': dict(CS)}
        for k in ('tv_blind_x2v', 'tv_payload_x2v', 'tv_blind_av', 'tv_payload_av', 'tv_blind_payload', 'tv_none_payload'): p[k] = 0.1
        for k in INTEGRITY892: p[k] = True
        for k in ('none', 'true_blind', 'true_payload_blind', 'true_x2_visible', 'true_a_visible', 'true_full', 'wrong_full'):
            p[k] = {'p': {x: 1.0 / 6 for x in W6}, 'seq_logp': dict(base), 'first_logp': dict(base)}
        p['interaction'] = {'p': {x: 0.0 for x in W6}, 'seq_logp': {x: 0.0 for x in W6}}
        p.update({'a_true_v_only': max(seqT, key=seqT.get), 'a_wrong_v_only': max(seqW, key=seqW.get),
                  'true_v_only': {'p': {x: 1.0 / 6 for x in W6}, 'seq_logp': seqT, 'first_logp': seqT},
                  'wrong_v_only': {'p': {x: 1.0 / 6 for x in W6}, 'seq_logp': seqW, 'first_logp': seqW},
                  'top_two_true_v_only': sorted(W6, key=lambda x: (-seqT[x], W6.index(x)))[:2],
                  'top_two_wrong_v_only': sorted(W6, key=lambda x: (-seqW[x], W6.index(x)))[:2],
                  'top_two_full': {'true': W6[:2], 'wrong': W6[:2]}, 'v_only_tw_exact': tv_ == wv_ and tvv == 0, 'v_only_eq_payload_true': False,
                  'v_only_eq_payload_wrong': False, 'tv_v_only_tw': tvv, 'tv_v_only_true_payload': 0.3, 'tv_v_only_wrong_payload': 0.3,
                  'tv_full_tw': 0.05, 'tv_full_blind_true': 0.05, 'J': {'p': {x: 0.0 for x in W6}, 'seq_logp': {x: 0.0 for x in W6}},
                  'v_only_spans': {'mask_V_ONLY': [[100, 112]], 'v_span': [112, 120]}, 'calls_v_only': [1, 1]})
        p.update(kw); return p
    A_ = v_only_audit892; ok = lambda a, v, w: (a['NATIVE_OUTCOME_ACTION_SEPARATION'], a['reason']) == (v, w)
    V = {'TECHNICAL_STATUS': 'TECHNICAL_BLOCK', 'PHYSICAL_READ': 'PASS', 'CONTENT_EFFECT': 'INCONCLUSIVE', 'OUTCOME_BENEFIT': 'NOT_MEASURED',
         'NATIVE_RECOVERY': 'INCONCLUSIVE', 'OVERALL': 'TECHNICAL_BLOCK', 'reasons': {'Y': {'D_TRUE_10_FORK': 0, 'D_WRONG_10_FORK': 0,
                                                                                           'D_TRUE_09_FORK': 1, 'D_WRONG_09_FORK': 1}}}
    same = lambda s, tvv=0.0, **kw: [Q(s, W6[4], W6[4], tvv=tvv, dup=d, **kw) for d in (0, 1)]          # two raw records per unique point
    ALL0 = [x for s in EXPECTED891 for x in same(s)]
    keep = _c892.deepcopy(V); a0 = A_(V, ALL0)
    r['audit_negative_no_difference'] = ok(a0, 'NEGATIVE', 'NO_TRUE_WRONG_DIFFERENCE') and a0['V_CONTENT_DISTRIBUTION_EFFECT'] == 'ABSENT' and \
        a0['raw_points'] == 14 and a0['unique_points'] == 7 and V == keep and 'OVERALL' not in a0
    D = [x for s in EXPECTED891 for x in same(s, tvv=0.08)]
    aD = A_(V, D)
    r['audit_negative_distribution_only'] = ok(aD, 'NEGATIVE', 'DISTRIBUTION_ONLY') and aD['V_CONTENT_DISTRIBUTION_EFFECT'] == 'PRESENT'
    sepq = lambda s, tvv=0.2, **kw: [Q(s, W6[4], W6[1], tvv=tvv, dup=d, **kw) for d in (0, 1)]
    P10, P09 = ('10', 'FORK', 5), ('09', 'FORK', 3)
    mix = lambda seps: [x for s in EXPECTED891 for x in (sepq(s, **seps[s]) if s in seps else same(s))]
    aP = A_(V, mix({P10: {}, P09: {}}))
    r['audit_pass_both_worlds'] = ok(aP, 'PASS', 'BOTH_WORLDS_PRIMARY_SEPARATION') and aP['strata']['10_FORK_t5']['classes'] == ['OUTCOME_ACTION_ARGMAX_SEPARATION']
    r['audit_one_world_only'] = ok(A_(V, mix({P10: {}})), 'INCONCLUSIVE', 'ONE_WORLD_ONLY')
    r['audit_secondary_only'] = ok(A_(V, mix({('10', 'FORK', 3): {}})), 'INCONCLUSIVE', 'SECONDARY_ONLY')
    r['audit_flip_tv_below_tau'] = ok(A_(V, mix({P10: {'tvv': 0.04}, P09: {}})), 'INCONCLUSIVE', 'FLIP_WITH_TV_BELOW_TAU')
    t2 = [x for s in EXPECTED891 for x in (same(s, tvv=0.1, top_two_wrong_v_only=[W6[4], W6[1]]) if s == P10 else same(s))]
    r['audit_top_two_only'] = ok(A_(V, t2), 'INCONCLUSIVE', 'TOP_TWO_ONLY')
    r['audit_missing_stratum'] = ok(A_(V, [x for x in ALL0 if (x['world'], x['condition'], x['step']) != ('10', 'MISSING', 3)]), 'INCONCLUSIVE', 'INCOMPLETE_EXPECTED_POINTS')
    r['audit_raw_below_14'] = ok(A_(V, [x for x in ALL0 if x['episode_id'] == 'E0']), 'INCONCLUSIVE', 'INCOMPLETE_EXPECTED_POINTS')
    dm = mix({P10: {}, P09: {}}); dm[[i for i, x in enumerate(dm) if (x['world'], x['condition'], x['step']) == P10][1]] = Q(P10, W6[4], W6[4], dup=1)
    r['audit_duplicate_mismatch'] = ok(A_(V, dm), 'INCONCLUSIVE', 'DUPLICATE_MISMATCH')
    r['audit_physical_fail'] = ok(A_(dict(V, PHYSICAL_READ='FAIL'), ALL0), 'TECHNICAL_BLOCK', 'PHYSICAL_OR_PARITY_OR_GEOMETRY')
    for k in ('v_only_spans_true_equals_wrong', 'v_only_geometry_ok', 'blind_true_equals_wrong_bitwise'):
        bad_ = ALL0[:3] + [dict(ALL0[3], **{k: False})] + ALL0[4:]
        r['audit_false_%s_block' % k] = ok(A_(V, bad_), 'TECHNICAL_BLOCK', 'PHYSICAL_OR_PARITY_OR_GEOMETRY')
    mal = lambda **kw: ALL0[:3] + [dict(ALL0[3], **kw)] + ALL0[4:]
    drop = lambda k: ALL0[:3] + [{x: v for x, v in ALL0[3].items() if x != k}] + ALL0[4:]
    r['audit_malformed_inconclusive'] = all(ok(A_(V, pts), 'INCONCLUSIVE', 'INCOMPLETE_RECORDS') for pts in (
        drop('true_v_only'), drop('J'), drop('top_two_true_v_only'), drop('v_only_spans'), drop('component_spans'),
        mal(tv_v_only_tw=float('nan')), mal(tv_v_only_tw=1.5), mal(J={'p': {x: float('inf') for x in W6}, 'seq_logp': {x: 0.0 for x in W6}}),
        mal(calls_v_only=[1, 2]), mal(calls_v_only=[True, 1]), mal(a_true_v_only='LEFT'), mal(top_two_wrong_v_only=[W6[0], W6[0]]),
        mal(v_only_tw_exact=None), mal(v_only_spans={'mask_V_ONLY': [[100, 112]], 'v_span': [113, 120]}), mal(step='3')))
    r['audit_false_flag_beats_malformed'] = ok(A_(V, ALL0[:3] + [dict({x: v for x, v in ALL0[3].items() if x != 'J'}, v_only_geometry_ok=False)] + ALL0[4:]),
                                               'TECHNICAL_BLOCK', 'PHYSICAL_OR_PARITY_OR_GEOMETRY')
    r['audit_missing_flag_not_false'] = ok(A_(V, drop('v_only_geometry_ok')), 'INCONCLUSIVE', 'INCOMPLETE_RECORDS')
    r['audit_empty'] = ok(A_(V, []), 'NOT_MEASURED', 'NO_POINTS') and A_(V, [])['V_CONTENT_DISTRIBUTION_EFFECT'] == 'NOT_MEASURED'
    r['audit_unexpected_stratum_kept_descriptive'] = len(A_(V, ALL0 + same(('10', 'FORK', 2)))['coverage']['unexpected_strata_descriptive']) == 1 and \
        ok(A_(V, ALL0 + same(('10', 'FORK', 2))), 'NEGATIVE', 'NO_TRUE_WRONG_DIFFERENCE')
    r['distribution_mixed'] = A_(V, [x for s in EXPECTED891 for x in (same(s, tvv=0.08) if s == P10 else same(s))])['V_CONTENT_DISTRIBUTION_EFFECT'] == 'MIXED'
    c0 = aD['readout_abandon_criterion']
    r['abandon_criterion'] = c0['met'] is True and c0['fork_true_over_wrong'] is False and \
        A_(dict(V, reasons={'Y': {'D_TRUE_10_FORK': 0, 'D_WRONG_10_FORK': 0, 'D_TRUE_09_FORK': 1, 'D_WRONG_09_FORK': 0}}), D)['readout_abandon_criterion']['met'] is False and \
        A_(dict(V, reasons={}), D)['readout_abandon_criterion']['met'] is False and a0['readout_abandon_criterion']['met'] is False
    r['class_matrix'] = [v_only_class892(x) for x in (Q(P10, W6[4], W6[1]), Q(P10, W6[4], W6[4], tvv=0.1),
                                                       Q(P10, W6[4], W6[4], tvv=0.0, v_only_tw_exact=True, v_only_eq_payload_true=True, v_only_eq_payload_wrong=True),
                                                       Q(P10, W6[4], W6[4], tvv=0.0, v_only_tw_exact=True))] == [
        'OUTCOME_ACTION_ARGMAX_SEPARATION', 'OUTCOME_CONTENT_DISTRIBUTION_EFFECT', 'NO_V_ONLY_EFFECT', 'V_VISIBILITY_WITHOUT_CONTENT_SEPARATION']
    r['valid_records_have_no_problems'] = all(record_problems891(x) == [] and record_problems892(x) == [] for x in ALL0 + D + mix({P10: {}, P09: {}}))
    try: raise RuntimeError('forced')
    except RuntimeError as exc_: ae = v_audit_error892(exc_, save=False)
    r['audit_error_is_technical_block'] = ae['NATIVE_OUTCOME_ACTION_SEPARATION'] == 'TECHNICAL_BLOCK' and ae['reason'] == 'AUDIT_ERROR RuntimeError: forced'
    tb = ('x', 'a', 'Y', 1)
    for nm, txt in (('double', 'aXa'), ('missing', 'bcd')):
        try: apply890(txt, [tb]); r['patch_anchor_%s_refused' % nm] = False
        except AssertionError: r['patch_anchor_%s_refused' % nm] = True
    for nm, raw in (('one_byte', B891_RAW892[:700] + b'#' + B891_RAW892[701:]), ('appended', B891_RAW892 + b'\nprint(1)\n'), ('truncated', B891_RAW892[:-9])):
        try: base891_892(raw); r['base891_%s_refused' % nm] = False
        except AssertionError: r['base891_%s_refused' % nm] = True
    r['base891_reproducible'] = base891_892(B891_RAW892)[0] == W891_892 and apply890(apply890(SRC889_891, [('rename',) + x for x in RENAMES892]), PATCHES892) == SRC889_892
    r['chain_891_sha'] = _h892.sha256(SRC889_891.encode()).hexdigest() == SRC889_891_SHA892
    body = 'x = 1\n'; lk = '# TEST892 BODY-SHA256 ' + _h892.sha256(body.encode()).hexdigest()
    r['lock_892_ok_891_header_refused'] = body_lock889(lk + '\n' + body)['ok'] and not body_lock889(lk.replace('TEST892', 'TEST891') + '\n' + body)['ok']
    return r


exec(compile(SRC889_892, '889.py:patched_for_TEST890_TEST891_TEST892', 'exec'), globals())   # 889 + 890 + 891 + 892 counted patches
