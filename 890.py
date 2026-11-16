# TEST890 BODY-SHA256 0f1b4194c1507c15a08f1d44076627350d583b8308e3d0f0966dad2d8506064f
# AKBASCORE SILICON HIPPOCAMPUS - TEST890 - PAYLOAD_BLIND AUDIT on TEST889 (one Colab cell, one Run, A100-SXM4-80GB)
# Contract: K3.1 "TEST889 Sonrasi Kok Neden, Nedensel Ayristirma ve Minimal TEST890 Karari" + "CLAUDE TEST890 KESIN KOD URETIM
# TALIMATI" (16 Nov 2026). The only new measurement: an audit-only counterfactual CAR read PAYLOAD_BLIND on the same SSD cartridge
# load/append, the same B_t, X_t, cache length n0+q and position ids, the locked xcar878 (sham=False), with the whole appended body
# [X2, A, V_AFTER] = key columns [n0, n0+q) masked. TRUE and WRONG PAYLOAD_BLIND are read separately and must be bitwise equal,
# else TECHNICAL_BLOCK. PAYLOAD_BLIND is never executed and never enters the executed reading, EFFECT, donor, recovery or Y;
# verdict889 is unchanged; PAYLOAD_AUDIT is a separate verdict and cannot change or erase OVERALL.
# REUSE: 889.py (commit 42cda345, git blob d201a0ec; canonical body e9dd0542 = the body of the executed TEST889 GPU cell, blob
# ecdb900d) is downloaded, hash-checked and executed with the counted text patches of PATCHES890 (nothing else is changed).
# The model alone decides: the executed action is the native CAR argmax of the arm's FULL reading, literally through execute866.
# No training, LoRA, backward, RAG, text replay, hooks, router, oracle, answer fixing, UNKNOWN rule, override. GPU_NOT_RUN_BY_AUTHOR.
import time as _t890
T_CELL890 = _t890.perf_counter()                       # the single 75-minute clock starts here (before any download)
import ast as _a890, copy as _c890, hashlib as _h890, json as _j890, re as _r890, urllib.request as _u890
B889_URL890 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
               '42cda345153e883666f93eda887474c16fe2404e/889.py')
B889_BLOB890 = 'd201a0ec30d3ab1b9a09a4b384bfa01fd5611580'
B889_SHA890 = '849fcc1f5a5b0764f979dee2f2ca545dc52db6cbcb86c0058652e9c19d39743d'
B889_BODY_LOCK890 = 'e9dd0542f2253c843d1be37f5e2df515b5f87b5d7ca1164dcbb3a9aff18471fc'   # canonical body, not a file SHA
EXEC889_GPU890 = {'git_blob': 'ecdb900d9e6bd545509a2d5c416e5f7422462fa0',
                  'sha256': 'a03b7aa98b66540bd56609154b1b47eec4fffd588508f342a05aff703012117f',
                  'body_lock': B889_BODY_LOCK890, 'log': '889.log (repo commit 407e9c1f, git blob 7e74a336, sha256 2be5c60e2b9e6bdf'
                  'f9ff9fff23537739493e1730887c2ee855bdd248804e5ca1)', 'note': 'the executed GPU cell (paste) differs from the repo file '
                  'byte-wise; the canonical body is equal; the repo file is the source of TEST890'}
B889_CUT890 = '\n# ============================ single cell execution ============================\n'
RENAMES890 = (('TEST889', 'TEST890', 43), ("'T889 ", "'T890 ", 2), ("'T889_", "'T890_", 4), ('889_engine.log', '890_engine.log', 1),
              ('889_events.jsonl', '890_events.jsonl', 1))                       # I/O names and console tags only
PATCHES890 = (                                                                 # (label, old, new, count) on the renamed 889 text
    ('runtime_scan', "'donor_v889', 'episode889')", "'donor_v889', 'episode889', 'payload_class890', 'payload_audit890')", 1),
    ('clock', 'T_CELL889 = _t889.perf_counter()', 'T_CELL889 = T_CELL890', 1),
    ('prereg', 'PREREG_SHA889 = _h889.sha256(', 'PREREG889.update(PREREG890)\nPREREG_SHA889 = _h889.sha256(', 1),
    ('read_span', "    sp = entry['provenance']['spans_body']['V_AFTER']; V = [n0 + int(sp[0]), n0 + int(sp[1])]\n",
     "    sp = entry['provenance']['spans_body']['V_AFTER']; V = [n0 + int(sp[0]), n0 + int(sp[1])]\n"
     "    P = [n0 + int(entry['provenance']['spans_body']['X2'][0]), n0 + q]                       # TEST890: [X2, A, V_AFTER]\n", 1),
    ('read_rec', "    rec = {'cartridge': entry['id'], 'n_exact': length873(env, g) == n0 + q,",
     "    rec = {'cartridge': entry['id'], 'n0': n0, 'q': q, 'payload_span': P, 'payload_span_is_whole_body': P == [n0, n0 + q],\n"
     "           'n_exact': length873(env, g) == n0 + q,", 1),
    ('read_mask', "xcar878(env, g, X, () if m == 'FULL' else [V], m == 'SHAM')",
     "xcar878(env, g, X, () if m == 'FULL' else [P] if m == 'PAYLOAD_BLIND' else [V], m == 'SHAM')", 1),
    ('modes_true', "first, ('FULL', 'SHAM', 'BLIND'))", "first, ('FULL', 'SHAM', 'BLIND', 'PAYLOAD_BLIND'))", 1),
    ('modes_wrong', "first, ('FULL', 'BLIND'))", "first, ('FULL', 'BLIND', 'PAYLOAD_BLIND'))", 1),
    ('call_parity', "cT['calls_BLIND'] != cW['calls_BLIND']:",
     "cT['calls_BLIND'] != cW['calls_BLIND'] or \\\n                                cT['calls_PAYLOAD_BLIND'] != cW['calls_PAYLOAD_BLIND']:", 1),
    ('payload_eq', "                        blind_eq = same_reading881(rT['BLIND'], rW['BLIND'])\n",
     "                        blind_eq = same_reading881(rT['BLIND'], rW['BLIND'])\n"
     "                        payload_eq = same_reading881(rT['PAYLOAD_BLIND'], rW['PAYLOAD_BLIND'])     # TEST890 audit gate\n", 1),
    ('point_fields', 'blind_true_equals_wrong_bitwise=blind_eq,',
     "blind_true_equals_wrong_bitwise=blind_eq, payload_true_equals_wrong_bitwise=payload_eq,\n"
     "                                  a_true_payload_blind=rT['PAYLOAD_BLIND']['action'], a_wrong_payload_blind=rW['PAYLOAD_BLIND']['action'],\n"
     "                                  tv_blind_payload=tv_m867(rT['BLIND'], rT['PAYLOAD_BLIND']), tv_none_payload=tv_m867(r_none, rT['PAYLOAD_BLIND']),\n"
     "                                  tv_full_payload=tv_m867(rT['FULL'], rT['PAYLOAD_BLIND']), true_payload_blind=summary_m888(rT['PAYLOAD_BLIND']),\n"
     "                                  wrong_payload_blind=summary_m888(rW['PAYLOAD_BLIND']), n0=cT['n0'], q=cT['q'], payload_span=cT['payload_span'],\n"
     "                                  X_sha256=st['X_sha256'], B_tokens=st['B_tokens'], cache_tokens=cT['n0'] + cT['q'],", 1),
    ('control_fields', "'blind_true_equals_wrong_bitwise': blind_eq,",
     "'blind_true_equals_wrong_bitwise': blind_eq, 'payload_true_equals_wrong_bitwise': payload_eq,", 1),
    ('payload_gate', "                        if not blind_eq: raise Gate883('PHYSICAL_AFTER_BLIND_LEAK %s t%d' % (ep_id, t))\n",
     "                        if not blind_eq: raise Gate883('PHYSICAL_AFTER_BLIND_LEAK %s t%d' % (ep_id, t))\n"
     "                        if not payload_eq: raise Gate883('PHYSICAL_PAYLOAD_BLIND_LEAK %s t%d' % (ep_id, t))\n", 1),
    ('capture_tree', "tree, tb = _a889.parse(src), _a889.parse(", "tree, tb = _a889.parse(SRC889_890 + '\\n' + src), _a889.parse(", 1),
    ('g0_source', "STATE889['status'] = 'G0'; capture889()\n", "STATE889['status'] = 'G0'; capture889(); source890()\n", 1),
    ('g0_selftest', "'889': st889()}", "'889': st889(), '890': st890()}", 1),
    ('audit', "    U_ = unique_m888(pts_)\n",
     "    try:\n        STATE889['payload_audit'] = payload_audit890(STATE889['verdict'], pts_)\n"
     "    except BaseException as exc:\n        STATE889['payload_audit'] = {'PAYLOAD_AUDIT': 'NOT_MEASURED', 'reason': 'AUDIT_ERROR %s: %s' % (type(exc).__name__, exc)}\n"
     "    U_ = unique_m888(pts_)\n", 1),
    ('report', "        'blocked_episodes': STATE889['blocked_episodes'],\n",
     "        'blocked_episodes': STATE889['blocked_episodes'], 'payload_audit': STATE889['payload_audit'],\n"
     "        'base889': B889_INFO890, 'executed_889_gpu_cell': EXEC889_GPU890,\n", 1),
    ('report_points', "'true_sham', 'true_blind', 'unique_key')} for p_ in U_],",
     "'true_sham', 'true_blind', 'unique_key', 'condition', 'world', 'a_wrong_blind',\n"
     "                                                 'blind_true_equals_wrong_bitwise', 'a_true_payload_blind', 'a_wrong_payload_blind',\n"
     "                                                 'tv_blind_payload', 'tv_none_payload', 'tv_full_payload', 'payload_true_equals_wrong_bitwise',\n"
     "                                                 'true_payload_blind', 'n0', 'q', 'payload_span', 'X_sha256', 'B_tokens', 'cache_tokens')} for p_ in U_],", 1),
    ('console_verdict', "    print('TEST890 | %s' % ' | '.join('%s=%s' % (k_, v_.get(k_)) for k_ in K_))\n",
     "    print('TEST890 | %s' % ' | '.join('%s=%s' % (k_, v_.get(k_)) for k_ in K_))\n"
     "    pa_ = STATE889.get('payload_audit') or {}\n"
     "    print('PAYLOAD_AUDIT=%s (%s) | PRIORITY=%s (%s) | strata=%s' % (pa_.get('PAYLOAD_AUDIT'), pa_.get('reason'), pa_.get('PAYLOAD_AUDIT_PRIORITY'),\n"
     "          pa_.get('priority_reason'), {k_: s_.get('classes') for k_, s_ in (pa_.get('strata') or {}).items()}))\n", 1),
    ('console_point', "        for nm_ in ('none', 'true_full', 'wrong_full', 'true_blind'):",
     "        print('      PAYLOAD_BLIND T/W=%s/%s class=%s TV(B,P)=%.4f TV(N,P)=%.4f TV(F,P)=%.4f T==W bitwise=%s n0=%d q=%d span=%s' % (\n"
     "            p_['a_true_payload_blind'], p_['a_wrong_payload_blind'], payload_class890(p_), p_['tv_blind_payload'], p_['tv_none_payload'],\n"
     "            p_['tv_full_payload'], p_['payload_true_equals_wrong_bitwise'], p_['n0'], p_['q'], p_['payload_span']))\n"
     "        for nm_ in ('none', 'true_full', 'wrong_full', 'true_blind', 'true_payload_blind'):", 1),
    ('report_jsafe', "json_write864('TEST890_final_report.json', jsafe878(report889))",
     "json_write864('TEST890_final_report.json', jsafe878(report889) if 'jsafe878' in globals() else\n"
     "                     _j889.loads(_j889.dumps(report889, default=str)))         # TEST890: G0 failures happen before load878", 1),
    ('lock_diag', "        except OSError: pass\n        raise Gate_m867('SOURCE_SELF_LOCK",
     "        except OSError: pass\n        lock['diag890'] = lockdiag890(src)\n        raise Gate_m867('SOURCE_SELF_LOCK", 1),
    ('receipt', "'drive_dir': CC_DRIVE_DIR, 'drive_zip_sha256_equal': None}",
     "'drive_dir': CC_DRIVE_DIR, 'drive_zip_sha256_equal': None,\n"
     "           'payload_audit': (STATE889.get('payload_audit') or {}).get('PAYLOAD_AUDIT')}", 1))
CHANGED_FUNCS890 = ('capture889', 'episode889', 'read889')        # every other 889 function must stay AST-identical
OWN_FUNCS890 = ('lockdiag890', 'canon890', 'apply890', 'base889_890', 'payload_class890', 'payload_audit890', 'source890', 'st890')


def canon890(t):
    # the paste-stable canonical form of body_lock889 / canon_lines_m867
    t = t.replace('\r\n', '\n').replace('\r', '\n').replace('\u00a0', ' ')
    for z in ('\ufeff', '\u200b', '\u200c', '\u200d', '\u2060'): t = t.replace(z, '')
    return [l.rstrip() for l in t.split('\n') if l.strip()]


# LINEDIG890: sha256[:4] of every canonical body line except its own data lines (paste diagnostics only, not a lock)
LINEDIG890 = (
    '2a910f3551dcce94010a136191d661c8b75447928e645af8d166de80d777df4a23f27fa69188bb436d468cb888242b20'  #LD890
    'b47be4de5cf270e52cbd54ea5d9ad9b712b15ba22379a171d5587c6aee1ff46355f627ad377237fb536eac5d47e70aa1'  #LD890
    '670ad437c218c47727863470ff68bb7e14d90a7b479a0bea7ecbd31920847b95290b818ae1062d3ccaabb9ea866b9b50'  #LD890
    '03f62ecd613475c94c06df282c7f91d312358f1661f8e33864b1bd592cbc608c1d936bf8549f6487b7f3d16579e191e6'  #LD890
    'c50d9963cb4a2ca49d02af0fc94f7f5d8e3074f365b6352a0de94902a56512c4fc3025c1e28461532714cbc8d787d1d5'  #LD890
    'a6c1c6a836b52ed382f854074512a5b2588dd3156a932a2867f72ad989e83c1d26a887619b3332c52eee34dcfa27d4d8'  #LD890
    'c94f1fcffa4466f3f33025abb1741f56717277f8cbeab5c440c5de9fb646dec6388b21d77f49a35744903de3c4c21aca'  #LD890
    'fbc471e6ad24ebe57bdd9a76b134d3bae3e7076d5d4dffd283297be33c729abdec61cac0f13a6715297d7c907ce109c3'  #LD890
    '8dc8eba265c3f18a792ff21bcf9a41ab0e3a81b51933f4154287d1760e29363c08186c161dd9feac9d8350757e7a8e8e'  #LD890
    '1a8cbbc616d00b97123be15989e6f11d6921d98306809c44bb55d9108a39443f3547430b46f9edaba719515a76c58a76'  #LD890
    '1a28e72b752c0f717c6d2468b957fef6c3213973f44042a8937c7bb70f17c4b558ff11fca3de3032c7afff3183380098'  #LD890
    '41c08eb5c2f454e0abd518a4d21cdebc99b3bff065e37ca3bc915af392a4d3cc7eeafad569a12e08e76d591e82b30784'  #LD890
    '8c98c9dbc5776fbe0fc0fd1f77e6184e6dc07d1598ffc4a7d5bd99c8d5a73a1747886e11b81e439208afae43f4c4ec2f'  #LD890
    )  #LD890


def lockdiag890(src):
    # after a SOURCE_SELF_LOCK refusal: which canonical line of the pasted cell differs, and which non-ASCII characters it holds
    try:
        rows = [(n + 1, canon890(l)) for n, l in enumerate(src.replace('\r\n', '\n').replace('\r', '\n').split('\n'))]
        got = [(n, c[0]) for n, c in rows if c][1:]                       # canonical lines with their pasted line numbers
        got = [(n, c) for n, c in got if not c.endswith('#LD890')]
        exp = [LINEDIG890[i:i + 4] for i in range(0, len(LINEDIG890), 4)]
        d = [_h890.sha256(c.encode('utf-8')).hexdigest()[:4] for _, c in got]
        i = next((k for k in range(max(len(d), len(exp))) if k >= len(d) or k >= len(exp) or d[k] != exp[k]), None)
        return {'first_differing_line_in_pasted_cell': None if i is None or i >= len(got) else got[i][0],
                'pasted_line': None if i is None or i >= len(got) else got[i][1][:240],
                'lines_pasted': len(got), 'lines_expected': len(exp),
                'non_ascii_in_paste': sorted({'U+%04X' % ord(c) for c in src if ord(c) > 127})[:20]}
    except BaseException as exc:
        return {'diag_error': '%s: %s' % (type(exc).__name__, exc)}


def apply890(text, table):
    # counted replacements; any count != expected refuses (no silent partial patch)
    for row in table:
        old, new, n = row[-3:]
        if text.count(old) != n: raise AssertionError(('BASE_889_PATCH', row[0], text.count(old), n))
        text = text.replace(old, new)
    return text


def base889_890(raw):
    blob = _h890.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()
    assert blob == B889_BLOB890 and _h890.sha256(raw).hexdigest() == B889_SHA890, ('BASE_889_LOCK', blob)
    head, rest = raw.decode('utf-8').split('\n', 1)
    m = _r890.fullmatch(r'#\s*TEST889\s+BODY-SHA256\s+([0-9a-f]{64})', head.strip())
    assert m and m.group(1) == B889_BODY_LOCK890, 'BASE_889_HEADER_LOCK'
    assert _h890.sha256(('\n'.join(canon890(rest)) + '\n').encode()).hexdigest() == B889_BODY_LOCK890, 'BASE_889_BODY_LOCK'
    assert rest.count(B889_CUT890) == 1, 'BASE_889_CUT'
    renamed = apply890(rest, [('rename',) + r for r in RENAMES890])
    assert 'TEST889' not in renamed, 'BASE_889_RENAME_LEFT'
    patched = apply890(renamed, PATCHES890)
    _a890.parse(patched)
    return patched, renamed, {'url': B889_URL890, 'git_blob': blob, 'sha256': B889_SHA890, 'body_lock': B889_BODY_LOCK890,
                              'renames': [list(r) for r in RENAMES890], 'patches': [[p[0], p[3]] for p in PATCHES890],
                              'patched_sha256': _h890.sha256(patched.encode()).hexdigest(), 'patched_lines': patched.count('\n')}


try:
    with _u890.urlopen(_u890.Request(B889_URL890, headers={'User-Agent': 'AKBASCORE-TEST890'}), timeout=240) as _r:
        B889_RAW890 = _r.read()
    SRC889_890, RENAMED889_890, B889_INFO890 = base889_890(B889_RAW890)
except BaseException as _exc890:
    import traceback as _tb890
    _p890 = '/content/TEST890_PRE_BASE_ERROR_%s.txt' % _t890.strftime('%Y%m%dT%H%M%SZ', _t890.gmtime())
    try:
        with open(_p890, 'w', encoding='utf-8') as _f890: _f890.write(_tb890.format_exc())
    except OSError: _p890 = 'NOT_WRITTEN'
    print('TEST890 PRE-BASE ERROR (nothing loaded):', type(_exc890).__name__, _exc890, '| traceback:', _p890)
    raise
print('TEST890 BASE889', _j890.dumps({k: B889_INFO890[k] for k in ('git_blob', 'sha256', 'body_lock', 'patched_sha256')}, sort_keys=True))

# ============================ sealed audit design (fixed before the model is loaded) ============================
PRIMARY890 = (('10', 'FORK', 5), ('10', 'FORK', 6), ('09', 'MISSING', 3), ('09', 'FORK', 3))   # TEST889 GPU: a_true_blind != a_none
PRIORITY890 = (('09', 'FORK', 3), ('10', 'FORK', 5))
PREREG890 = {
    'test': 'TEST890 PAYLOAD_BLIND_AUDIT (TEST889 EVENT_CLOSED_NATIVE_TRANSITION_APPRAISAL otherwise unchanged)',
    'contract': 'K3.1 TEST889 Sonrasi Kok Neden / Minimal TEST890 Karari + CLAUDE TEST890 KESIN KOD URETIM TALIMATI (16 Nov 2026)',
    'base889': B889_INFO890, 'executed_889_gpu_cell': EXEC889_GPU890,
    'payload_blind': 'per eligible point, per cartridge (TRUE and WRONG separately), on the same single load_exp878 + append_exp878 as '
                     'its FULL / SHAM / BLIND reads: xcar878(env, g, X, [[n0, n0+q]], sham=False); n0 = B length, q = body tokens, '
                     'span = [X2 start (0) + n0, n0 + q] = [X2][A][EVALUATION slot + V_AFTER]; the 4-D mask is built from that 2-D '
                     'key mask by the locked xspan878; position ids arange(nc, nc+L) and cache length n0+q unchanged; no extra SSD '
                     'write, MUE / random tensor, new embedding or model reload; gates: span == [n0, n0+q], finite, call parity '
                     'TRUE/WRONG, TRUE == WRONG bitwise else PHYSICAL_PAYLOAD_BLIND_LEAK (TECHNICAL_BLOCK); never executed',
    'primary_strata': ['%s_%s_t%d' % s for s in PRIMARY890], 'priority_strata': ['%s_%s_t%d' % s for s in PRIORITY890],
    'primary_source': 'TEST889 GPU log: unique points with a_true_blind != a_none (10_MISSING t3 has BLIND == NONE: not primary); '
                      'a stratum that does not occur, or does not flip, in the natural TEST890 trajectory is reported, never '
                      'created or replaced by another point; other flips are listed as descriptive only',
    'point_class': {'NO_BLIND_FLIP': 'a_true_blind == a_none', 'CARRIER_SUFFICIENT': 'flip and PAYLOAD_BLIND == BLIND argmax: the '
                    'visible [X2, A] content is not necessary for that flip', 'HISTORY_CONTENT_NECESSARY': 'flip and PAYLOAD_BLIND '
                    '== NONE argmax: the visible [X2, A] content is necessary for that flip', 'INCONCLUSIVE_THIRD_ARGMAX': 'flip and '
                    'PAYLOAD_BLIND is neither'},
    'audit_verdict': 'coverage first, over the pre-fixed strata identities (never over a count of unique points; repeated raw points are '
                     'deduplicated; every unique record of a stratum is kept and must agree). PAYLOAD_AUDIT is conclusive only if all '
                     'four primary strata occurred, PHYSICAL_READ == PASS and every TRUE/WRONG payload read is bitwise equal, every '
                     'unique record of every primary stratum shows the expected BLIND != NONE flip, and all of them have one class: '
                     'CARRIER_SUFFICIENT or HISTORY_CONTENT_NECESSARY. Otherwise: no point at all -> NOT_MEASURED / NO_POINTS; physical '
                     'or parity failure -> INCONCLUSIVE / PHYSICAL_READ_NOT_PASS_OR_PAYLOAD_NOT_BITWISE (checked before coverage); a '
                     'stratum that did not occur -> INCONCLUSIVE / INCOMPLETE_EXPECTED_POINTS; occurred without the flip -> '
                     'INCONCLUSIVE / EXPECTED_BLIND_FLIP_ABSENT; any third argmax -> INCONCLUSIVE / THIRD_ARGMAX; two classes -> '
                     'INCONCLUSIVE / MIXED. PAYLOAD_AUDIT_PRIORITY: the same rule on the two priority strata only. No stratum is '
                     'replaced by another point. Point classes, TV and the full distributions are kept for every unique point',
    'payload_scope': 'audit only: never turns CONTENT_EFFECT, OUTCOME_BENEFIT or NATIVE_RECOVERY into PASS, never changes or erases '
                     'TECHNICAL_STATUS / OVERALL (a TECHNICAL_BLOCK stays a TECHNICAL_BLOCK)',
    'payload_not_claimed': ['CARRIER_SUFFICIENT is not a proof of pure geometry: the masked kernel, the positions and the physical '
                            'carrier (B + appended rows) stay jointly in place', 'learning, generalization, GPU success before the run']}


def payload_class890(p):
    n, b, y = p['a_none'], p['a_true_blind'], p['a_true_payload_blind']
    if b == n: return 'NO_BLIND_FLIP'
    if y == b: return 'CARRIER_SUFFICIENT'
    if y == n: return 'HISTORY_CONTENT_NECESSARY'
    return 'INCONCLUSIVE_THIRD_ARGMAX'


def payload_audit890(verdict, points):
    # read-only on verdict889 and the points; all unique points are reported, nothing is removed or substituted
    U = unique_m888(points); rows = []
    for p in U:
        s = (p['world'], p['condition'], int(p['step']))
        rows.append({'episode_id': p['episode_id'], 'stratum': '%s_%s_t%d' % s, 'primary': s in PRIMARY890, 'priority': s in PRIORITY890,
                     'a_none': p['a_none'], 'a_true_full': p['a_true'], 'a_true_blind': p['a_true_blind'],
                     'a_payload_blind': p['a_true_payload_blind'], 'tv_blind_payload': p['tv_blind_payload'],
                     'tv_none_payload': p['tv_none_payload'], 'payload_true_equals_wrong_bitwise': p['payload_true_equals_wrong_bitwise'],
                     'class': payload_class890(p)})
    clean = verdict.get('PHYSICAL_READ') == 'PASS' and all(r['payload_true_equals_wrong_bitwise'] is True for r in rows)
    name = lambda s: '%s_%s_t%d' % s
    by = {name(s): [r for r in rows if r['stratum'] == name(s)] for s in PRIMARY890}
    strata = {k: {'unique_points': len(v), 'classes': [r['class'] for r in v], 'priority': k in [name(s) for s in PRIORITY890],
                  'status': 'NOT_OCCURRED' if not v else 'EXPECTED_BLIND_FLIP_ABSENT' if any(r['class'] == 'NO_BLIND_FLIP' for r in v) else 'MEASURED'}
              for k, v in by.items()}

    def agg(expected):
        # coverage gate before any conclusive class: every expected stratum occurred and every unique record of it flipped
        keys = [name(s) for s in expected]; cls = sorted({c for k in keys for c in strata[k]['classes']})
        cov = {'expected': keys, 'not_occurred': [k for k in keys if strata[k]['status'] == 'NOT_OCCURRED'],
               'flip_absent': [k for k in keys if strata[k]['status'] == 'EXPECTED_BLIND_FLIP_ABSENT']}
        cov['complete'] = not cov['not_occurred'] and not cov['flip_absent']
        if not rows: return 'NOT_MEASURED', 'NO_POINTS', cov
        if not clean: return 'INCONCLUSIVE', 'PHYSICAL_READ_NOT_PASS_OR_PAYLOAD_NOT_BITWISE', cov
        if cov['not_occurred']: return 'INCONCLUSIVE', 'INCOMPLETE_EXPECTED_POINTS', cov
        if cov['flip_absent']: return 'INCONCLUSIVE', 'EXPECTED_BLIND_FLIP_ABSENT', cov
        if cls in (['CARRIER_SUFFICIENT'], ['HISTORY_CONTENT_NECESSARY']): return cls[0], 'ALL_%d_EXPECTED_STRATA_COVERED_ONE_CLASS' % len(keys), cov
        return 'INCONCLUSIVE', 'THIRD_ARGMAX' if 'INCONCLUSIVE_THIRD_ARGMAX' in cls else 'MIXED', cov
    a, why, cov = agg(PRIMARY890); ap, pwhy, pcov = agg(PRIORITY890)
    return {'PAYLOAD_AUDIT': a, 'reason': why, 'PAYLOAD_AUDIT_PRIORITY': ap, 'priority_reason': pwhy, 'strata': strata,
            'coverage': cov, 'priority_coverage': pcov,
            'secondary_flips_descriptive_only': [r for r in rows if not r['primary'] and r['class'] != 'NO_BLIND_FLIP'],
            'points': rows, 'raw_points': len(points), 'unique_points': len(U),
            'verdict889_unchanged': {k: verdict.get(k) for k in ('TECHNICAL_STATUS', 'PHYSICAL_READ', 'CONTENT_EFFECT', 'OUTCOME_BENEFIT',
                                                                 'NATIVE_RECOVERY', 'OVERALL')},
            'scope': PREREG890['payload_scope'], 'not_claimed': PREREG890['payload_not_claimed']}


def source890():
    # G0, before the model: the patched 889 differs from the renamed 889 only in CHANGED_FUNCS890 + module statements, and the
    # PAYLOAD_BLIND read can reach nothing but the point record and its bitwise gate
    T, R0 = _a890.parse(SRC889_890), _a890.parse(RENAMED889_890)
    f = {n.name: n for n in T.body if isinstance(n, _a890.FunctionDef)}; f0 = {n.name: n for n in R0.body if isinstance(n, _a890.FunctionDef)}
    changed = sorted(k for k in f if k not in f0 or _a890.dump(f[k]) != _a890.dump(f0[k]))
    rd, ep = f['read889'], f['episode889']
    xc = [n for n in _a890.walk(rd) if isinstance(n, _a890.Call) and getattr(n.func, 'id', None) == 'xcar878']
    ps = [n for n in _a890.walk(rd) if isinstance(n, _a890.Assign) and [_a890.unparse(x) for x in n.targets] == ['P']]
    modes = sorted(_a890.unparse(n.args[10]) for n in _a890.walk(ep) if isinstance(n, _a890.Call) and getattr(n.func, 'id', None) == 'read889')
    sub = lambda n: any(isinstance(x, _a890.Constant) and x.value == 'PAYLOAD_BLIND' for x in _a890.walk(n))
    reach = sorted({_a890.unparse(t) for n in _a890.walk(ep) if isinstance(n, _a890.Assign) and sub(n) for t in n.targets})
    reading = sorted({_a890.unparse(n.value) for n in _a890.walk(ep) if isinstance(n, _a890.Assign)
                      and any(isinstance(x, _a890.Name) and x.id == 'reading' for x in n.targets)})
    src_ep = _a890.unparse(ep)
    facts = {'changed_functions': changed == list(CHANGED_FUNCS890), 'own_names_not_in_889': not (set(OWN_FUNCS890) & set(f)),
             'single_masked_kernel_call': len(xc) == 1 and _a890.unparse(xc[0].args[3]) ==
             "() if m == 'FULL' else [P] if m == 'PAYLOAD_BLIND' else [V]" and _a890.unparse(xc[0].args[4]) == "m == 'SHAM'",
             'payload_span_whole_body': len(ps) == 1 and _a890.unparse(ps[0].value) == "[n0 + int(entry['provenance']['spans_body']['X2'][0]), n0 + q]",
             'modes_true_wrong_repeat': modes == ["('FULL', 'BLIND', 'PAYLOAD_BLIND')", "('FULL', 'SHAM', 'BLIND', 'PAYLOAD_BLIND')", "('FULL',)"],
             'payload_reaches_only_point_and_gate': reach == ['(rT, cT)', '(rW, cW)', 'payload_eq', 'pt'],
             'executed_reading_unchanged': reading == ["rT['FULL'] if arm == 'D_TRUE' else rW['FULL']", 'r_none', "record['reading']"],
             'payload_gate_after_point_record': 0 < src_ep.find("out['points'].append(pt)") < src_ep.find("raise Gate883('PHYSICAL_PAYLOAD_BLIND_LEAK"),
             'verdict889_has_no_payload': 'PAYLOAD' not in _a890.unparse(f['verdict889'])}
    if not all(facts.values()): raise Gate_m867('SOURCE890_FACTS %s' % sorted(k for k, v in facts.items() if not v))
    (ROOT864 / 'TEST890_base889_patched_executed.py').write_text(SRC889_890, encoding='utf-8')
    STATE889['source']['base889'] = B889_INFO890; STATE889['source']['facts890'] = facts
    json_write864('TEST890_base889.json', {'base889': B889_INFO890, 'executed_889_gpu_cell': EXEC889_GPU890, 'facts890': facts,
                                          'changed_functions': changed, 'before_model_load': True})
    print('T890 BASE889 PATCH facts=%s patched_sha256=%s' % (all(facts.values()), B889_INFO890['patched_sha256']), flush=True)


def st890():
    r = {}
    P = lambda w, c, t, n, b, y, eq=True, k=None: {'episode_id': 'E', 'world': w, 'condition': c, 'step': t, 'a_none': n, 'a_true': b,
                                                   'a_true_blind': b, 'a_true_payload_blind': y, 'tv_blind_payload': 0.1,
                                                   'tv_none_payload': 0.2, 'payload_true_equals_wrong_bitwise': eq,
                                                   'unique_key': k or '%s%s%d%s%s%s' % (w, c, t, n, b, y)}
    r['class_carrier'] = payload_class890(P('09', 'FORK', 3, 'ADVANCE', 'ACCEPT', 'ACCEPT')) == 'CARRIER_SUFFICIENT'
    r['class_history'] = payload_class890(P('09', 'FORK', 3, 'ADVANCE', 'ACCEPT', 'ADVANCE')) == 'HISTORY_CONTENT_NECESSARY'
    r['class_third'] = payload_class890(P('09', 'FORK', 3, 'ADVANCE', 'ACCEPT', 'STOP')) == 'INCONCLUSIVE_THIRD_ARGMAX'
    r['class_no_flip'] = payload_class890(P('10', 'FORK', 3, 'ACQUIRE', 'ACQUIRE', 'STOP')) == 'NO_BLIND_FLIP'
    V = {'TECHNICAL_STATUS': 'TECHNICAL_BLOCK', 'PHYSICAL_READ': 'PASS', 'CONTENT_EFFECT': 'INCONCLUSIVE', 'OUTCOME_BENEFIT': 'NOT_MEASURED',
         'NATIVE_RECOVERY': 'INCONCLUSIVE', 'OVERALL': 'TECHNICAL_BLOCK'}
    A = payload_audit890; C = lambda w, c, t: P(w, c, t, 'ADVANCE', 'ACQUIRE', 'ACQUIRE'); H = lambda w, c, t: P(w, c, t, 'ADVANCE', 'ACQUIRE', 'ADVANCE')
    T3 = lambda w, c, t: P(w, c, t, 'ADVANCE', 'ACQUIRE', 'STOP'); N = lambda w, c, t: P(w, c, t, 'ADVANCE', 'ADVANCE', 'ADVANCE')
    pri, oth = [('09', 'FORK', 3), ('10', 'FORK', 5)], [('10', 'FORK', 6), ('09', 'MISSING', 3)]
    car, his = [C(*s) for s in pri + oth], [H(*s) for s in pri + oth]
    ok = lambda a, v, w, pv, pw: (a['PAYLOAD_AUDIT'], a['reason'], a['PAYLOAD_AUDIT_PRIORITY'], a['priority_reason']) == (v, w, pv, pw)
    I, IEP, FA, PHY = 'INCONCLUSIVE', 'INCOMPLETE_EXPECTED_POINTS', 'EXPECTED_BLIND_FLIP_ABSENT', 'PHYSICAL_READ_NOT_PASS_OR_PAYLOAD_NOT_BITWISE'
    A4, A2 = 'ALL_4_EXPECTED_STRATA_COVERED_ONE_CLASS', 'ALL_2_EXPECTED_STRATA_COVERED_ONE_CLASS'
    keep = _c890.deepcopy(V); a = A(V, [car[0]])                                                     # A: only 09_FORK t3, 10_FORK t5 missing
    r['A_single_priority_point_never_conclusive'] = ok(a, I, IEP, I, IEP) and a['points'][0]['class'] == 'CARRIER_SUFFICIENT' and \
        a['strata']['10_FORK_t5']['status'] == 'NOT_OCCURRED' and a['priority_coverage']['not_occurred'] == ['10_FORK_t5'] and not a['coverage']['complete']
    r['B_priority_complete_primary_incomplete'] = ok(A(V, car[:2]), I, IEP, 'CARRIER_SUFFICIENT', A2)
    a = A(V, car + [dict(car[0])])                                                                    # C + duplicate raw point
    r['C_all_four_carrier'] = ok(a, 'CARRIER_SUFFICIENT', A4, 'CARRIER_SUFFICIENT', A2) and a['raw_points'] == 5 and a['unique_points'] == 4 and a['coverage']['complete']
    r['C_all_four_history'] = ok(A(V, his), 'HISTORY_CONTENT_NECESSARY', A4, 'HISTORY_CONTENT_NECESSARY', A2)
    r['D_primary_stratum_without_flip'] = ok(A(V, car[:2] + [N(*oth[0]), C(*oth[1])]), I, FA, 'CARRIER_SUFFICIENT', A2)
    r['E_priority_stratum_without_flip'] = ok(A(V, [N(*pri[0])] + car[1:]), I, FA, I, FA)
    r['E_second_unique_record_without_flip'] = ok(A(V, car + [N(*pri[1])]), I, FA, I, FA)             # every unique record of a stratum counts
    r['F_mixed'] = ok(A(V, car[:2] + his[2:]), I, 'MIXED', 'CARRIER_SUFFICIENT', A2) and ok(A(V, [car[0], his[1]] + car[2:]), I, 'MIXED', I, 'MIXED')
    r['F_third_argmax'] = ok(A(V, car[:3] + [T3(*oth[1])]), I, 'THIRD_ARGMAX', 'CARRIER_SUFFICIENT', A2) and \
        ok(A(V, [T3(*pri[0])] + car[1:]), I, 'THIRD_ARGMAX', I, 'THIRD_ARGMAX')
    r['G_empty_not_measured'] = ok(A(V, []), 'NOT_MEASURED', 'NO_POINTS', 'NOT_MEASURED', 'NO_POINTS') and ok(A(dict(V, PHYSICAL_READ='FAIL'), []), 'NOT_MEASURED', 'NO_POINTS', 'NOT_MEASURED', 'NO_POINTS')
    r['G_physical_fail_not_hidden_by_coverage'] = ok(A(dict(V, PHYSICAL_READ='FAIL'), car), I, PHY, I, PHY) and ok(A(dict(V, PHYSICAL_READ='FAIL'), [car[0]]), I, PHY, I, PHY)
    r['G_payload_parity_false'] = ok(A(V, car[:3] + [dict(car[3], payload_true_equals_wrong_bitwise=False)]), I, PHY, I, PHY)
    sec = A(V, [C('10', 'FORK', 4), N(*pri[0])])                                                      # secondary-only flip: never substituted
    r['G_secondary_only_no_substitution'] = ok(sec, I, IEP, I, IEP) and len(sec['secondary_flips_descriptive_only']) == 1 and \
        sec['strata']['09_FORK_t3']['status'] == FA and sec['strata']['10_FORK_t5']['status'] == 'NOT_OCCURRED'
    blk = A(V, [C(*pri[0]), C(*pri[1]), C(*oth[0])])                                                  # 09_MISSING blocked before its point
    r['G_blocked_episode_stratum_missing'] = ok(blk, I, IEP, 'CARRIER_SUFFICIENT', A2) and blk['coverage']['not_occurred'] == ['09_MISSING_t3']
    r['G_verdict889_immutable'] = V == keep and a['verdict889_unchanged']['OVERALL'] == 'TECHNICAL_BLOCK' and \
        'CONTENT_EFFECT' not in a and 'OVERALL' not in a
    tb = ('x', 'a', 'Y', 1)
    try: apply890('aXa', [tb]); r['patch_double_anchor_refused'] = False
    except AssertionError: r['patch_double_anchor_refused'] = True
    try: apply890('abc', [('x', 'Q', 'Y', 1)]); r['patch_missing_anchor_refused'] = False
    except AssertionError: r['patch_missing_anchor_refused'] = True
    for nm, raw in (('one_byte', B889_RAW890[:900] + b'#' + B889_RAW890[901:]), ('appended', B889_RAW890 + b'\nprint(1)\n'), ('truncated', B889_RAW890[:-9])):
        try: base889_890(raw); r['base889_%s_refused' % nm] = False
        except AssertionError: r['base889_%s_refused' % nm] = True
    r['base889_reproducible'] = base889_890(B889_RAW890)[0] == SRC889_890
    body = 'x = 1\n'; lk = '# TEST890 BODY-SHA256 ' + _h890.sha256(body.encode()).hexdigest()
    r['lock_890_ok_889_header_refused'] = body_lock889(lk + '\n' + body)['ok'] and not body_lock889(lk.replace('TEST890', 'TEST889') + '\n' + body)['ok']
    return r


exec(compile(SRC889_890, '889.py:patched_for_TEST890', 'exec'), globals())   # TEST889 (+885/887/888 chain) with the counted patches
