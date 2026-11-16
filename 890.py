# TEST890 BODY-SHA256 0bd35b6c22706330f18211771c08337c763e8e2ab230f24555b3116654908ae3
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
    'fbc471e6ad24b44120788b6d9a61b1e87be33c729abdec61cac0f13a6715297d7c907ce109c38dc8eba265c3f18a792f'  #LD890
    'f21bcf9a41ab0e3a81b58327f0d0a5c67d02d9fefe4094fa40cf54233198a83770c6123b89e6f11d6921d98306809c44'  #LD890
    'bb55d9108a39443f3547430b46f9edaba719515a76c58a761a28e72b752c0f717c6d2468b957fef6c3213973f44042a8'  #LD890
    '937c7bb70f17c4b558ff11fca3de3032c7afff318338009841c08eb5c2f454e0abd5cf0463bc5a2709ef5021bd58deae'  #LD890
    '7222775d360c64c8178072d052eb8d9d79dae137c4a7d5bd99c8d5a73a1747886e11b81e439208afae43f4c4ec2f'  #LD890
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
    'audit_verdict': 'PAYLOAD_AUDIT over the primary-strata unique points with a flip: all CARRIER_SUFFICIENT -> CARRIER_SUFFICIENT; '
                     'all HISTORY_CONTENT_NECESSARY -> HISTORY_CONTENT_NECESSARY; mixed or any third argmax -> INCONCLUSIVE; no such '
                     'point -> NOT_MEASURED; PHYSICAL_READ != PASS or any TRUE/WRONG payload read not bitwise -> INCONCLUSIVE. '
                     'PAYLOAD_AUDIT_PRIORITY: the same rule on the priority strata. TV and the full distributions are kept for '
                     'every point, also when the argmax is equal',
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

    def agg(sel):
        cls = sorted({r['class'] for r in sel if r['class'] != 'NO_BLIND_FLIP'})
        if not cls: return 'NOT_MEASURED', 'NO_BLIND_FLIP_POINT_IN_THESE_STRATA'
        if not clean: return 'INCONCLUSIVE', 'PHYSICAL_READ_NOT_PASS_OR_PAYLOAD_NOT_BITWISE'
        if cls in (['CARRIER_SUFFICIENT'], ['HISTORY_CONTENT_NECESSARY']): return cls[0], 'ALL_%d_FLIP_POINTS' % sum(1 for r in sel if r['class'] == cls[0])
        return 'INCONCLUSIVE', 'THIRD_ARGMAX' if 'INCONCLUSIVE_THIRD_ARGMAX' in cls else 'MIXED'
    a, why = agg([r for r in rows if r['primary']]); ap, pwhy = agg([r for r in rows if r['priority']])
    strata = {}
    for s in PRIMARY890:
        sel = [r for r in rows if r['stratum'] == '%s_%s_t%d' % s]
        strata['%s_%s_t%d' % s] = {'unique_points': len(sel), 'classes': [r['class'] for r in sel],
                                   'status': 'NOT_OCCURRED' if not sel else 'NO_FLIP_IN_890' if all(r['class'] == 'NO_BLIND_FLIP' for r in sel) else 'MEASURED'}
    return {'PAYLOAD_AUDIT': a, 'reason': why, 'PAYLOAD_AUDIT_PRIORITY': ap, 'priority_reason': pwhy, 'strata': strata,
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
    car = [P('09', 'FORK', 3, 'ADVANCE', 'ACCEPT', 'ACCEPT'), P('10', 'FORK', 5, 'ADVANCE', 'ACQUIRE', 'ACQUIRE')]
    his = [P('09', 'FORK', 3, 'ADVANCE', 'ACCEPT', 'ADVANCE'), P('10', 'FORK', 5, 'ADVANCE', 'ACQUIRE', 'ADVANCE')]
    keep = _c890.deepcopy(V); a = payload_audit890(V, car + [dict(car[0])])
    r['audit_carrier'] = a['PAYLOAD_AUDIT'] == 'CARRIER_SUFFICIENT' == a['PAYLOAD_AUDIT_PRIORITY'] and a['raw_points'] == 3 and a['unique_points'] == 2
    r['audit_never_touches_verdict889'] = V == keep and a['verdict889_unchanged']['OVERALL'] == 'TECHNICAL_BLOCK'
    r['audit_history'] = payload_audit890(V, his)['PAYLOAD_AUDIT'] == 'HISTORY_CONTENT_NECESSARY'
    m = payload_audit890(V, [car[0], his[1]]); r['audit_mixed_inconclusive'] = m['PAYLOAD_AUDIT'] == 'INCONCLUSIVE' and m['reason'] == 'MIXED'
    t3 = payload_audit890(V, [car[0], P('10', 'FORK', 5, 'ADVANCE', 'ACQUIRE', 'STOP')])
    r['audit_third_inconclusive'] = t3['PAYLOAD_AUDIT'] == 'INCONCLUSIVE' and t3['reason'] == 'THIRD_ARGMAX'
    sec = payload_audit890(V, [P('10', 'FORK', 4, 'ADVANCE', 'ACQUIRE', 'ACQUIRE'), P('09', 'FORK', 3, 'ADVANCE', 'ADVANCE', 'ADVANCE')])
    r['audit_no_substitution'] = sec['PAYLOAD_AUDIT'] == 'NOT_MEASURED' and len(sec['secondary_flips_descriptive_only']) == 1 and \
        sec['strata']['09_FORK_t3']['status'] == 'NO_FLIP_IN_890' and sec['strata']['10_FORK_t5']['status'] == 'NOT_OCCURRED'
    r['audit_physical_fail_inconclusive'] = payload_audit890(dict(V, PHYSICAL_READ='FAIL'), car)['PAYLOAD_AUDIT'] == 'INCONCLUSIVE'
    r['audit_payload_not_bitwise_inconclusive'] = payload_audit890(V, [car[0], dict(car[1], payload_true_equals_wrong_bitwise=False)])['PAYLOAD_AUDIT'] == 'INCONCLUSIVE'
    r['audit_empty_not_measured'] = payload_audit890(V, [])['PAYLOAD_AUDIT'] == 'NOT_MEASURED'
    pr = payload_audit890(V, [P('09', 'MISSING', 3, 'STOP', 'ACQUIRE', 'STOP'), car[0]])
    r['audit_priority_separate'] = pr['PAYLOAD_AUDIT'] == 'INCONCLUSIVE' and pr['PAYLOAD_AUDIT_PRIORITY'] == 'CARRIER_SUFFICIENT'
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
