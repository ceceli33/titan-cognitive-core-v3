# TEST893 BODY-SHA256 73c41194d41474da447556d94244a6d289af84d21d95a899e6e1bf723862ec27
# AKBASCORE SILICON HIPPOCAMPUS - TEST893 - F-O-DELTA paired 09_FORK experiment on TEST892 (one Colab cell, one Run, A100-SXM4-80GB)
# Contract: K3.1 "ARKEOLOJIK KAZI, NORAL MEKANIZMA KESFI VE REKURSIF AKIL YURUTME" (17 Nov 2026, candidate A = F-O-DELTA, the
# single 09_FORK 2x2) + "CLAUDE ICIN TEST893 UYGULAMA TALIMATI" (17 Nov 2026).
# The one new mechanism: at the first experience step (t1) of each D episode, AFTER the FULL native CAR reading chose the action A
# and BEFORE the literal execute866, the model forecasts its own next appraisal for that action (P): the locked gen851 evaluation
# generation and the locked car867 CAR reading over the CURRENT state segments, the next step's feedback-slot layout and the native
# embedding rows of the executed action word in the K slot ("Previous control numerical state:"). Nothing from the future, the
# environment, Y, a label or a donor can reach P; P is written to an append-only pending SSD record (file SHA-256 + rows seal + commit
# sequence) before execute866. O = the exact post-step native evaluation rows and the native CAR reading of the following control
# step (H_alpha: own episode; H_beta: the exact-step NONE donor of the locked DONOR_M867 map, as in TEST892, no padding/cropping).
# delta = p_obs - p_hat (six CAR words) and D_JS are measurement records, never a reward, never an action gate.
# Cartridge: OLD = [X2][A][EVALUATION + O] (the TEST892 body, unchanged); NEW = [X2][A][EVALUATION + P label + P + O label + O +
# DELTA label + delta rows], written by the UNCHANGED write_pair889 / write_appraisal889 / write_exp878 (H3 + L0-3 KV CUT3, L4-79
# native reconstruction on reload). Schedule: E1 written at t2, read once at t3 (FULL executed), t >= 4 native for every arm.
# Run: NONE_10_FORK (H_beta donor ledger), NONE_09_FORK (no-experience reference), OLD/NEW x D_TRUE(H_alpha)/D_WRONG(H_beta) on
# 09_FORK. The model alone decides: the executed action is reading['action'] of the arm's FULL CAR reading, literally through
# execute866. No training, LoRA, backward, RAG, text replay, hooks, router, oracle, answer fixing, override.
# REUSE: 892.py (commit 550f35ee, blob ba75f106, canonical body ef6872ff; its generated text 219da301 is the one the TEST892 GPU run
# executed, 892.log) is downloaded and hash-checked; its wrapper runs unchanged except the counted PATCHES893W (it downloads and
# checks 891 / 890 / 889 and builds the TEST892 text), then the counted RENAMES893 + PATCHES893 are applied and it is executed.
# GPU_NOT_RUN_BY_AUTHOR.
import time as _t893
T_CELL893 = _t893.perf_counter()                       # the single 75-minute clock starts here (before any download)
import ast as _a893, hashlib as _h893, json as _j893, math as _m893, re as _r893, urllib.request as _u893
B892_URL893 = ('https://raw.githubusercontent.com/ceceli33/titan-cognitive-core-v3/'
               '550f35eea94bdb86bbc470f12df752fc8c081160/892.py')
B892_BLOB893 = 'ba75f1068318fee02e4540b00568aa584d542108'
B892_SHA893 = 'c820e3e49cefe4be663bbba4f4f4b0b70e56261b99a3ae6b160baa0e88691ec0'
B892_BODY_LOCK893 = 'ef6872ffdf0dcb8e62bf88d49fd1994b71398dc6158988c9e7bc19aa34021a1e'  # canonical body, not a file SHA
SRC889_892_SHA893 = '219da301fa24360d7a570cfcdbb16ca4570ea29f856e68788ab536e4fc82e9c7'  # the TEST892 text (= executed on the GPU)
EXEC892_GPU893 = {'git_blob': '591e461f731db3ae2b5240f1f4f0e5635bbeca66',
                  'sha256': 'a248dc58809066c4153a3b12a4c04091379675cff053e2faa828cc4b7086014d', 'body_lock': B892_BODY_LOCK893,
                  'executed_sha256': SRC889_892_SHA893,
                  'log': '892.log (repo commit 550f35ee, git blob e53d13d2, sha256 175d7c2e17999f20d0c93d4129736b7fe4cffe739708a040c6de2765deef1b75)',
                  'note': 'the executed 892 paste is not in the repo: its canonical body and its generated text equal the repo file; the '
                          'raw byte difference is not characterized; the repo file is the source'}
PATCHES893W = (                                                                 # (label, old, new, count) on the 892 cell body
    ('clock', 'T_CELL892 = _t892.perf_counter()', 'T_CELL892 = T_CELL893', 1),
    ('no_892_exec', "exec(compile(SRC889_892, '889.py:patched_for_TEST890_TEST891_TEST892', 'exec'), globals())",
     "pass  # TEST893: the TEST892 text is executed only after PATCHES893 (below)", 1),
    ('source892_cell', "C = _a892.parse((ROOT864 / 'TEST892.py').read_text(encoding='utf-8'))", "C = _a892.parse(W892_893)", 1),
    ('st_locks_w891', '"lk = \'# TEST892 BODY-SHA256 \'", 2)', '"lk = \'# TEST893 BODY-SHA256 \'", 2)', 1),   # st890 / st891 lock label
    ('st890_lock2_w891', '"lk.replace(\'TEST892\', \'TEST889\')", 1)', '"lk.replace(\'TEST893\', \'TEST889\')", 1)', 1),
    ('st891_lock2_w891', '"lk.replace(\'TEST892\', \'TEST890\')", 1)', '"lk.replace(\'TEST893\', \'TEST890\')", 1)', 1))
SCOPED893W = (('artifact_gates892', 'TEST892', 'TEST893', 4), ('v_audit_error892', 'TEST892', 'TEST893', 2),
              ('st892', 'TEST892', 'TEST893', 16))                   # I/O names / lock label inside these 892 functions only
RENAMES893 = (('TEST892', 'TEST893', 54), ("'T892 ", "'T893 ", 2), ("'T892_", "'T893_", 4), ('892_engine.log', '893_engine.log', 1),
              ('892_events.jsonl', '893_events.jsonl', 1))                        # I/O names and console tags of the TEST892 text
NEW893 = ('forecast893', 'js893', 'fo_inputs893', 'fo_checks893', 'fo_record893', 'fo_point893', 'expected893', 'hex64_893',
          'seal_ok893')
PATCHES893 = (                                                                  # (label, old, new, count) on the renamed TEST892 text
    ('prereg', 'PREREG889.update(PREREG892)\n', 'PREREG889.update(PREREG892)\nPREREG889.update(PREREG893)\n', 1),
    ('runtime_scan', "'point_view892', 'v_only_final892')", "'point_view892', 'v_only_final892',\n                  %s)" %
     ', '.join(repr(n) for n in NEW893), 1),
    ('ledger_reading', "'episode_id': ep_id, 'step': t}",
     "'episode_id': ep_id, 'step': t, 'p': {w_: float(record['reading']['normalized'][w_]) for w_ in ACTIONS_M867},\n"
     "                          'reading': reading_view883(record['reading'])}                  # TEST893: O = rows + native CAR reading", 1),
    ('single_write_and_forecast', "                if arm != 'NONE' and not terminal:\n"
     "                    pend = {'true': prepare_experience883(env, cache, B, X, action), 'wrong': prepare_experience883(env, cache, B, X, action),\n"
     "                            'step': t, 'action': action, 'X_sha256': tsha881(X), 'v_before_sha': led[t]['sha'], 'effect_action': None}\n",
     "                if arm != 'NONE' and not terminal and t == 1:          # TEST893: only E1 is written (the single 2x2 read point)\n"
     "                    pend = {'true': prepare_experience883(env, cache, B, X, action), 'wrong': prepare_experience883(env, cache, B, X, action),\n"
     "                            'step': t, 'action': action, 'X_sha256': tsha881(X), 'v_before_sha': led[t]['sha'], 'effect_action': None}\n"
     "                    if FORMAT893 == 'NEW': pend['P'] = forecast893(env, ctx, B, state, action, ep_id, t, cdir)   # sealed BEFORE execute866\n", 1),
    ('effect_seq', "if pend is not None: pend['effect_action'] = eff.get('action')",
     "if pend is not None: pend['effect_action'] = eff.get('action'); STATE889['seq'] += 1; pend['effect_seq'] = STATE889['seq']", 1),
    ('fo_inputs', 'w = write_pair889(env, pend, led[t], donor, t, cdir, key)',
     'vt_, dn_ = fo_inputs893(env, pend, led[t], donor, ep_id)              # TEST893: exact O rows; NEW adds P / labels / delta\n'
     '                        w = write_pair889(env, pend, vt_, dn_, t, cdir, key)', 1),
    ('closure_v_after', "'checks': {'v_after_is_post_step_ledger': w['true'][0]['provenance']['V_rows_sha256'] == led[t]['sha'],",
     "'checks': {'v_after_is_post_step_ledger': w['true'][0]['provenance']['V_rows_sha256'] == vt_['payload_sha'] and vt_['O_sha'] == led[t]['sha'],\n"
     "                                         'fo893_P_before_execute_O_after': fo_checks893(pend, led[t], STATE889['seq'], vt_, dn_, w),", 1),
    ('fo_record', 'written[s_] = w; pend = None', "w['fo893'] = fo_record893(w, vt_, dn_, ep_id); written[s_] = w; pend = None", 1),
    ('single_read', 'ev = eligible889(t)', 'ev = eligible889(t) if t == 1 + LAG889 else None       # TEST893: the single read of E1 at t3', 1),
    ('point_fields', 'pt.update(v_only_fields892(rT, rW, cT, cW))', 'pt.update(v_only_fields892(rT, rW, cT, cW)); pt.update(fo_point893(d))', 1),
    ('expected', "exp_w, exp_r = expected889(ctx['steps'], out['end'], horizon) if arm != 'NONE' else (0, 0)",
     "exp_w, exp_r = expected893(ctx['steps']) if arm != 'NONE' else (0, 0)", 1),
    ('capture_tree', "_a889.parse(SRC889_892 + '\\n' + W890_891 + '\\n' + W891_892 + '\\n' + src)",
     "_a889.parse(SRC889_893 + '\\n' + W890_891 + '\\n' + W891_892 + '\\n' + W892_893 + '\\n' + src)", 1),
    ('lock_diag', "lock['diag892'] = lockdiag892(src)", "lock['diag893'] = lockdiag893(src)", 1),
    ('g0_sources', "STATE889['status'] = 'G0'; capture889(); source890(); source891(); source892()",
     "STATE889['status'] = 'G0'; capture889(); source890(); source891(); source892(); source893()", 1),
    ('g0_selftests', "'892': st892()}", "'892': st892(), '893': st893()}", 1),
    ('g1_slots', "SLOTS867['PREV_EVALUATION'] = list(env883['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)",
     "SLOTS867['PREV_EVALUATION'] = list(env883['tok'](PREV_EVAL_SLOT_TEXT867, add_special_tokens=False).input_ids)\n"
     "    SLOTS893.update({k_: list(env883['tok'](v_, add_special_tokens=False).input_ids) for k_, v_ in SLOT_TEXT893.items()})\n"
     "    if not all(SLOTS893.get(k_) for k_ in SLOT_TEXT893): raise Gate_m867('SLOTS893_EMPTY %s' % SLOTS893)", 1),
    ('plan', "    plan889 = [('NONE', w_, c_) for (w_, c_) in CELLS_M867] + [(a_, w_, c_) for (w_, c_) in CELLS_M867 for a_ in ('D_TRUE', 'D_WRONG')]\n"
     "    ledger889 = {}\n"
     "    for i_, (a_, w_, c_) in enumerate(plan889):\n"
     "        if i_: admit883('E%02d_%s_%s_%s' % (i_, a_, w_, c_), len(plan889) - i_)\n"
     "        try:\n"
     "            ep_ = episode889(env883, by_key883[(int(w_), c_)], a_, '%s_%s_%s' % (a_, w_, c_), HORIZON883,\n",
     "    plan889 = list(PLAN893)                                         # TEST893: 2 NONE + the single 2x2 on 09_FORK\n"
     "    ledger889 = {}\n"
     "    for i_, (f_, a_, w_, c_) in enumerate(plan889):\n"
     "        if i_: admit883('E%02d_%s_%s_%s_%s' % (i_, f_, a_, w_, c_), len(plan889) - i_)\n"
     "        FORMAT893 = f_\n"
     "        try:\n"
     "            ep_ = episode889(env883, by_key883[(int(w_), c_)], a_, ep_id893(f_, a_, w_, c_), HORIZON883,\n", 1),
    ('verdict893', '    U_ = unique_safe891(pts_)\n',
     "    try:\n"
     "        STATE889['t893'] = verdict893(STATE889, phys_)\n"
     "    except BaseException as exc:\n"
     "        STATE889['t893'] = {'VERDICT': 'TECHNICAL_BLOCK', 'PHYSICAL_TEMPORAL_VALIDITY': 'TECHNICAL_BLOCK', 'NATIVE_MECHANISM_EFFECT': 'NOT_MEASURED',\n"
     "                            'OUTCOME_BENEFIT': 'NOT_MEASURED', 'error': 'VERDICT893_ERROR %s: %s' % (type(exc).__name__, exc)}\n"
     "    U_ = unique_safe891(pts_)\n", 1),
    ('report893', "'test': 'TEST893', 'verdict': STATE889['verdict'],",
     "'test': 'TEST893', 't893': STATE889.get('t893'), 'pending_P893': STATE889.get('pending893'), 'base892': B892_INFO893,\n"
     "        'executed_892_gpu_cell': EXEC892_GPU893, 'legacy_889_892_note': 'verdict / payload / component / v_only fields are the inherited '\n"
     "        'TEST889-892 diagnostics on this smaller run; they are not the TEST893 verdict', 'verdict': STATE889['verdict'],", 1),
    ('console_legacy', "print('TEST893 | %s'", "print_t893(STATE889.get('t893')); print('LEGACY_889_892_DIAGNOSTICS (not the TEST893 verdict) | %s'", 1),
    ('receipt893', "    _rc['v_only_final'] = v_only_final892(STATE889.get('v_only_audit'), artifact_gates892(CC_ZIP, _zip_ok, _rc['drive_zip_sha256_equal'], CC_DRIVE_DIR, STATE889))\n",
     "    _g893 = artifact_gates892(CC_ZIP, _zip_ok, _rc['drive_zip_sha256_equal'], CC_DRIVE_DIR, STATE889)\n"
     "    _rc['v_only_final'] = v_only_final892(STATE889.get('v_only_audit'), _g893)\n"
     "    _rc['test893_final'] = final893(STATE889.get('t893'), _g893)\n"
     "    print('TEST893_FINAL VERDICT=%s | PHYSICAL_TEMPORAL_VALIDITY=%s | NATIVE_MECHANISM_EFFECT=%s | OUTCOME_BENEFIT=%s | ARTIFACT_STATUS=%s | failed_gates=%s' % tuple(\n"
     "        _rc['test893_final'].get(k_) for k_ in ('VERDICT', 'PHYSICAL_TEMPORAL_VALIDITY', 'NATIVE_MECHANISM_EFFECT', 'OUTCOME_BENEFIT', 'ARTIFACT_STATUS', 'failed_gates')))\n", 1),
    ('receipt893_fail', "        _rcx['receipt_error'] = '%s: %s' % (type(_exc).__name__, _exc)\n",
     "        _rcx['receipt_error'] = '%s: %s' % (type(_exc).__name__, _exc)\n"
     "        _rcx['test893_final'] = dict(_rcx.get('test893_final') or {}, VERDICT='TECHNICAL_BLOCK', ARTIFACT_STATUS='TECHNICAL_BLOCK',\n"
     "                                     preliminary=(STATE889.get('t893') or {}).get('VERDICT'))\n", 1),
    ('console893_fail', "    _rpx = str(CC_ZIP).replace('.zip', '_RECEIPT.json')",
     "    print('TEST893_FINAL VERDICT=TECHNICAL_BLOCK | ARTIFACT_STATUS=TECHNICAL_BLOCK (receipt failed) | preliminary=%s' % ((STATE889.get('t893') or {}).get('VERDICT'),))\n"
     "    _rpx = str(CC_ZIP).replace('.zip', '_RECEIPT.json')", 1))
CHANGED_FUNCS893 = ('capture889', 'episode889')                    # against the renamed TEST892 text; every other function AST-identical
LOCKED893 = ('execute866', 'control_step867', 'donor_v889', 'verdict889', 'read889', 'read_contract889', 'write_appraisal889',
             'write_pair889', 'write_exp878', 'load_exp878', 'append_exp878', 'xappend878', 'xcar878', 'xspan878', 'same_reading881',
             'budget849', 'comp_masks891', 'calls_gate891', 'v_only_fields892', 'v_only_mask892', 'record_problems892')
OWN_FUNCS893 = ('canon893', 'base892_893', 'lockdiag893', 'ep_id893', 'verdict893', 'final893', 'print_t893', 'source893', 'st893') + NEW893
# LINEDIG893: sha256[:4] of every canonical body line except its own data lines (paste diagnostics only, not a lock)
LINEDIG893 = (
    'a7611a68135262b5f9eb472f9db8ce18676983767f52b108c742dc861b8fe47272fc7e0934325c10871661fe4488f63c'  #LD890
    '12fb1d3b3689a2554a6652c9b294d426a565c9d6de59ea04c82d0ec6132befbcef4db99c463b7261377f3fa6efebd0bf'  #LD890
    '8b56b59f95e4b9f41aada7432158178535cf93a8f8d030a06218f8d0888b8b77de5d8b8c214f3906aad2884893001c6a'  #LD890
    '4296c653560c67dd4751de107abf8cb814eb4d23a974dcc4d9ecacb7a1c70480e2283552a9003f809eb6cb1fe228ef67'  #LD890
    '7e8448073f80a33ebcc94ab64341014cf386538176b21fe56e4be21fbd51ed343efd3bcd19b59091a52805cf3add05a0'  #LD890
    '8100682cd16add0822e44767ec521f84252764569ed754b1c47e133291e6c50d99636f7832b2515154079d3fc76cb089'  #LD890
    '1bde9fb95d6af3a26ff5d7ef9b30e896cfb1dfa76fc3521ff1998761e185d417389ef06fc0d4cf2ac94f675404dc2140'  #LD890
    'f33034e77a4fd5e91f7b3e6abf8c18c8e9f5f36f851f1f7128ede5633e9874ff7434383e11dec3fbc182382e7b40bf41'  #LD890
    '2c190793c3718f9b5df4511d52acb52923517761a53f2196fa5f626859858e6c52fa0a36147f1dde08529c13f78adeba'  #LD890
    '5a39c7478b8523d4459077d948ba5c07766ebe6b1728ac5a3777dad4d673a33b07f6b872c1a8754bb9c506467b4fa5f0'  #LD890
    'afd0f1b5d933fb565227c852c8ac9880e2245488c8082b80b815cc39cd2ed9c8b751d63baf5c44c3ef6bb4ddf5e0d21b'  #LD890
    '94d29757bff4f88b12ecea37465455569c3a6f6996df6e6dc20a5f9a1e888f4521f830d6deb097560f50ae3e0c112c50'  #LD890
    '1bd78b3acd306ad6bc3dd8bcbd64ef672c5d0f25864fff01c87c1262dac4311b3440edeba9ddffee8138a0fe39b459eb'  #LD890
    'c8ad3bdc6090418f0f0e14e1c51def65440a21151d63ba91b00b82c7961654b04c0b5a7d68b5684fb31b247841337a0a'  #LD890
    '08066e79667f2512876b691e704e049bbecfa12d5648e1b4f92680bcca79b8ca4248b7a2b3f8ce25fe8df49684dc51ad'  #LD890
    '33d189d908b4606cbc4c533b130787193e77e04706798060508bbff8ae446cf5912a59cca3514e1ebe2538715de4ee9b'  #LD890
    '2173caf65ca3daaa16204dbed8a90bb70922be58eb3c52d1dc555f2abdf8cdb28dd6f43818f9d14a8181eba6f413bea3'  #LD890
    'dbc1b88348c3c532e0f72c22b6b27490d17ff3ae55a6b903ca99cd3b417170d109e328b1f620c89fdbbb2e3e1f946a7e'  #LD890
    '4ad9d1aea66b1d94386b9cbfda1e40b9d2161719e356630a102c1d947f89c94f2f37cd89f9c2a34ad16727d3fa5b55a8'  #LD890
    'f79d3e56c5c07fbe10ec9ca01e8946e0e5c9c60470486d0b567f809c3334b543021edf89adaa9f181b4b830ba6831022'  #LD890
    '598c3d32a2daf98449e68ace31a16e3c0095c321da05ec31070af878973c0b8464732925a179ea2ed2766ccac4b552df'  #LD890
    '1cbbc27a3c34c729021e374a88f72517cb0015b8794d39d7b03705a1cf025a79fc9a958863cbdc29c3e0b5cd38d25bf6'  #LD890
    '84d013069b53a2b5946dce5554a35f64c5716da3aa78dbd3a6fc8c5718eab854554ac8425a28ca51da20c370d21ca829'  #LD890
    '695e2bfddd2b6fc9eda931dd661cbf50e4bd751d8e4ff32a2618be24d34bd8366794acbc51396daed0254b9c90b5f4c4'  #LD890
    '4aab'  #LD890
    )  #LD890


def canon893(t):
    # the paste-stable canonical form of body_lock889 / canon_lines_m867 (needed before the 892 wrapper is loaded)
    t = t.replace('\r\n', '\n').replace('\r', '\n').replace('\u00a0', ' ')
    for z in ('\ufeff', '\u200b', '\u200c', '\u200d', '\u2060'): t = t.replace(z, '')
    return [l.rstrip() for l in t.split('\n') if l.strip()]


def base892_893(raw):
    blob = _h893.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()
    assert blob == B892_BLOB893 and _h893.sha256(raw).hexdigest() == B892_SHA893, ('BASE_892_LOCK', blob)
    head, rest = raw.decode('utf-8').split('\n', 1)
    m = _r893.fullmatch(r'#\s*TEST892\s+BODY-SHA256\s+([0-9a-f]{64})', head.strip())
    assert m and m.group(1) == B892_BODY_LOCK893, 'BASE_892_HEADER_LOCK'
    assert _h893.sha256(('\n'.join(canon893(rest)) + '\n').encode()).hexdigest() == B892_BODY_LOCK893, 'BASE_892_BODY_LOCK'
    for label, old, new, n in PATCHES893W:
        if rest.count(old) != n: raise AssertionError(('BASE_892_PATCH', label, rest.count(old), n))
        rest = rest.replace(old, new)
    fn = {x.name: x for x in _a893.parse(rest).body if isinstance(x, _a893.FunctionDef)}
    for name, old, new, n in sorted(SCOPED893W, key=lambda r: -fn[r[0]].lineno):     # bottom-up: earlier offsets stay valid
        lines = rest.split('\n'); a, b = fn[name].lineno - 1, fn[name].end_lineno
        seg = '\n'.join(lines[a:b])
        if seg.count(old) != n: raise AssertionError(('BASE_892_SCOPED', name, seg.count(old), n))
        rest = '\n'.join(lines[:a] + seg.replace(old, new).split('\n') + lines[b:])
    _a893.parse(rest)
    return rest, {'url': B892_URL893, 'git_blob': blob, 'sha256': B892_SHA893, 'body_lock': B892_BODY_LOCK893,
                  'wrapper_patches': [[p[0], p[3]] for p in PATCHES893W], 'scoped_renames': [list(r) for r in SCOPED893W],
                  'wrapper_sha256': _h893.sha256(rest.encode()).hexdigest()}


try:
    with _u893.urlopen(_u893.Request(B892_URL893, headers={'User-Agent': 'AKBASCORE-TEST893'}), timeout=240) as _r:
        B892_RAW893 = _r.read()
    W892_893, B892_INFO893 = base892_893(B892_RAW893)
except BaseException as _exc893:
    import traceback as _tb893
    _p893 = '/content/TEST893_PRE_BASE_ERROR_%s.txt' % _t893.strftime('%Y%m%dT%H%M%SZ', _t893.gmtime())
    try:
        with open(_p893, 'w', encoding='utf-8') as _f893: _f893.write(_tb893.format_exc())
    except OSError: _p893 = 'NOT_WRITTEN'
    print('TEST893 PRE-BASE ERROR (nothing loaded):', type(_exc893).__name__, _exc893, '| traceback:', _p893)
    raise
exec(compile(W892_893, '892.py:wrapper_for_TEST893', 'exec'), globals())   # 892 cell: downloads + checks 891 / 890 / 889, builds SRC889_892
assert _h893.sha256(SRC889_892.encode()).hexdigest() == SRC889_892_SHA893, 'BASE_892_CHAIN_NOT_REPRODUCED'
RENAMED892_893 = apply890(SRC889_892, [('rename',) + r for r in RENAMES893])
assert 'TEST892' not in RENAMED892_893, 'BASE_892_RENAME_LEFT'
SRC889_893 = apply890(RENAMED892_893, PATCHES893)
_a893.parse(SRC889_893)
B892_INFO893.update(chain_892_sha256=SRC889_892_SHA893, renames893=[list(r) for r in RENAMES893],
                    patches893=[[p[0], p[3]] for p in PATCHES893], executed_sha256=_h893.sha256(SRC889_893.encode()).hexdigest(),
                    w891_892_sha256=_h893.sha256(W891_892.encode()).hexdigest())
print('TEST893 BASE892', _j893.dumps({k: B892_INFO893[k] for k in ('git_blob', 'sha256', 'body_lock', 'chain_892_sha256',
                                                                   'executed_sha256')}, sort_keys=True))

# ============================ sealed TEST893 design (fixed before the model is loaded) ============================
PLAN893 = (('NONE', 'NONE', '10', 'FORK'), ('NONE', 'NONE', '09', 'FORK'), ('OLD', 'D_TRUE', '09', 'FORK'), ('OLD', 'D_WRONG', '09', 'FORK'),
           ('NEW', 'D_TRUE', '09', 'FORK'), ('NEW', 'D_WRONG', '09', 'FORK'))
EP893 = ('NONE_10_FORK', 'NONE_09_FORK', 'OLD_D_TRUE_09_FORK', 'OLD_D_WRONG_09_FORK', 'NEW_D_TRUE_09_FORK', 'NEW_D_WRONG_09_FORK')
SLOT_TEXT893 = {'P_FORECAST': 'Forecast evaluation numerical state:', 'O_OBSERVED': 'Observed evaluation numerical state:',
                'DELTA': 'Forecast error numerical state:'}
SLOTS893 = {}                     # token ids, filled at G1 with the model tokenizer (as SLOTS867['PREV_EVALUATION'])
FORMAT893 = None                  # set by the plan loop before each episode: 'NONE', 'OLD' or 'NEW'
VERDICTS893 = ('TECHNICAL_BLOCK', 'INCONCLUSIVE', 'NEGATIVE', 'MECHANISM_EFFECT_WITHOUT_BENEFIT', 'MECHANISM_EFFECT_WITH_BENEFIT')
PREREG893 = {
    'test893': 'TEST893 F-O-DELTA paired 09_FORK experiment (K3.1 candidate A, one 2x2; TEST892 run otherwise unchanged)',
    'contract893': 'K3.1 ARKEOLOJIK KAZI report (17 Nov 2026) + CLAUDE ICIN TEST893 UYGULAMA TALIMATI (17 Nov 2026)',
    'unit893': 'world 09, condition FORK, first eligible read point t3 (reads E1 = [X2_1][A_1][...] closed at t2); t >= 4 native (no read)',
    'episodes893': list(EP893),
    'H_alpha': 'D_TRUE: O = the own episode exact post-step (t2) native evaluation rows V_2 and the native CAR reading at t2',
    'H_beta': 'D_WRONG: O = the exact post-step (t2) native evaluation rows and native CAR reading of NONE_10_FORK (locked DONOR_M867 '
              'map 09 -> 10, donor_v889 exact step, never clamped); same X2 / A / P as H_alpha; rows count must equal H_alpha (no '
              'padding, no cropping) or NO_EXACT_HBETA_GEOMETRY (TECHNICAL_BLOCK). It is the TEST892 WRONG history: the O of a '
              'different world after its own native step-1 action, paired with the 09 X2 / A',
    'P_forecast': 'after the FULL native CAR action A_1 and before execute866: V_hat = gen851(B_1, EVALUATION_PROMPT866, '
                  '[C_1, E_1, R_1, (pointer_1), PREV_EVALUATION = MUE x |V_1|, K slot = embed(native ids of A_1)], EVALUATION_SUFFIX) '
                  '(the next step feedback layout of the locked NO_FEEDBACK arm, with the executed action word in the K slot); '
                  'p_hat = reading867(car867(B_1, CONTROL_PROMPT866, same segments + [EVALUATION = V_hat], REVIEW_SUFFIX851)). '
                  'Sealed before execute866 in an append-only pending SSD record (torch file SHA-256, rows seal, commit sequence). '
                  'B_1 prefix seals must be unchanged by the forecast. P is PREDICTED, never OBSERVED',
    'O_observed': 'V_2 rows and p_obs = the normalized native CAR reading of the locked control_step867 at t2 (same prompt, slot, '
                  'suffix, six words and mass formula as p_hat)',
    'delta': 'delta_w = p_obs_w - p_hat_w over the six CAR words; D_JS = 0.5 sum p_hat ln(p_hat / m) + 0.5 sum p_obs ln(p_obs / m), '
             'm = (p_hat + p_obs) / 2, zero terms by the limit rule; a measurement record, never a reward, never an action gate',
    'cartridge_new': 'NEW body = [X2][A][EVALUATION slot][P label][P rows][O label][O rows][DELTA label][delta rows], delta rows = '
                     'delta_w x embed(first native id of word w) in the fixed action order; the label rows are the token embeddings '
                     'of SLOT_TEXT893; written by the unchanged write_pair889 / write_appraisal889 / write_exp878 (H3 + L0-3 KV); '
                     'the V_AFTER span of the provenance is the whole after-action payload (so BLIND / PAYLOAD / V_ONLY masks keep '
                     'their meaning); P / O / DELTA sub-spans, p_hat, p_obs, delta, D_JS and the pending-P SHA are LINKS in the '
                     'append-only TEST893_fo_manifest.jsonl, bound to the cartridge by its V_rows_sha256 (part of its provenance id)',
    'cartridge_old': 'OLD body = [X2][A][EVALUATION slot][O rows] (the TEST892 body, unchanged); same O rows as NEW',
    'geometry893': 'within each format H_alpha and H_beta have identical spans and body tokens (gated by write_pair889); OLD and NEW '
                   'differ in length by construction, so the mechanism criterion compares H_alpha vs H_beta within each format, never '
                   'OLD length vs NEW length',
    'PHYSICAL_TEMPORAL_VALIDITY': 'PASS only if: run COMPLETE, no physical failure, post-run integrity, clean cleanup, negatives refused; '
                                  'the six episodes present with natural ends; each D episode exactly one closure (ok, incl. P seq < '
                                  'execute seq < O generation seq < commit seq for NEW) and one t3 point (E1); exact O geometry (no '
                                  'padding); repeat reload bitwise, explicit == native append, B seal unchanged; file SHA-256 64-hex and '
                                  'tensor seal schema for every cartridge; one pending P per NEW episode with B seal unchanged; the four '
                                  'D episodes reach t3 from the same state (X sha, B tokens, NONE action, actions t1-t2); Y binary; '
                                  'else TECHNICAL_BLOCK',
    'contrast893': 'O_alpha != O_beta in both formats and delta_alpha != delta_beta and the same P (rows SHA and p_hat) in both NEW '
                   'episodes; else INCONCLUSIVE',
    'OLD_WALL': 'REPRODUCED if OLD H_alpha and OLD H_beta both execute ACCEPT at t3 and both Y = 1 (the TEST892 09_FORK wall); else '
                'NOT_REPRODUCED -> INCONCLUSIVE (no other pairing is chosen afterwards)',
    'NATIVE_MECHANISM_EFFECT': 'PRESENT if the executed t3 FULL actions of NEW H_alpha and NEW H_beta differ, else ABSENT (V_ONLY / TV / '
                               'logit differences never count)',
    'OUTCOME_BENEFIT': 'paired baseline = the OLD episode with the same history: d_h = Y(NEW_h) - Y(OLD_h); NOT_MEASURED if a Y is missing; '
                       'PASS if some d_h > 0 and none < 0; FAIL if some d_h < 0 and none > 0; MIXED if both; NO_GAIN_CEILING if all d_h '
                       '= 0 and both OLD Y = 1 (benefit not measurable in a binary Y at the ceiling); NO_GAIN otherwise. NONE_09_FORK Y '
                       'is reported as the no-experience reference only. D_JS order is descriptive (K31_DJS_ORDER), never the success rule',
    'VERDICT': 'TECHNICAL_BLOCK if physical invalid; INCONCLUSIVE if the contrast is missing or OLD_WALL not reproduced; NEGATIVE if '
               'mechanism ABSENT; MECHANISM_EFFECT_WITH_BENEFIT if PRESENT and OUTCOME_BENEFIT PASS; else MECHANISM_EFFECT_WITHOUT_BENEFIT. '
               'PRELIMINARY in the report; FINAL (receipt test893_final, console TEST893_FINAL) is TECHNICAL_BLOCK unless every artifact '
               'gate is True (report read-back, ZIP testzip, SHA256SUMS, report in ZIP, Drive copy SHA; Drive not attempted = NOT_RUN = '
               'not True)',
    'not_claimed893': 'one pair is not general recursive learning; D_JS is not a reward or a correctness probability; a forecast-'
                      'observation fit is not semantic truth; no reliability score is used by the policy; B / C candidates are not part '
                      'of this test'}


def lockdiag893(src):
    # the TEST890 line diagnostics with the TEST893 line table (same '#LD890' data-line marker)
    keep = LINEDIG890; globals()['LINEDIG890'] = LINEDIG893
    try: return lockdiag890(src)
    finally: globals()['LINEDIG890'] = keep


def ep_id893(f, a, w, c):
    return '%s_%s_%s' % (a, w, c) if a == 'NONE' else '%s_%s_%s_%s' % (f, a, w, c)


def js893(p, q):
    # Jensen-Shannon divergence (natural log) of two six-word distributions; zero terms by the limit rule
    tot = 0.0
    for w in ACTIONS_M867:
        a, b = float(p[w]), float(q[w]); m = 0.5 * (a + b)
        if a > 0: tot += 0.5 * a * _m893.log(a / m)
        if b > 0: tot += 0.5 * b * _m893.log(b / m)
    return tot


def expected893(n_steps):
    # TEST893 schedule: E1 closed at t2 (if step 1 was nonterminal, i.e. a step 2 exists), read once at t3
    n = int(n_steps)
    return (1 if n >= 2 else 0), (1 if n >= 3 else 0)


def hex64_893(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def seal_ok893(s):
    # the structured tensor seal of tsha878: {'h': sha256 hex, 'lower': CUT + 1 pairs of sha256 hex}; never a file hash
    return isinstance(s, dict) and set(s) == {'h', 'lower'} and hex64_893(s['h']) and isinstance(s['lower'], (list, tuple)) and \
        len(s['lower']) == APPEND873.get('CUT', 3) + 1 and all(isinstance(x, (list, tuple)) and len(x) == 2 and all(hex64_893(y) for y in x)
                                                         for x in s['lower'])


def forecast893(env, ctx, B, state, action, ep_id, t, cdir):
    # P_t: the model's own action-conditioned forecast of its next appraisal, computed after the FULL CAR action and before
    # execute866 from what exists at t only. Locked readers only (gen851 evaluation, car867 CAR); B is read, never changed.
    q = env['QTEXT841'][ctx['spec']['qid']]
    seal0 = prefix_seals865(env, B)
    drop = (list(SLOTS866['EVALUATION']), list(SLOTS867['PREV_EVALUATION']), list(env['K_SLOT851']))
    keep = [s for s in state['segments'] if list(s[0]) not in drop]
    v_now = state['segments'][-1][1]
    mue = env['MUE845'].detach().float().cpu().reshape(1, -1)
    a_rows = env['embed841'](list(dict(ACTION_IDS867)[action])).detach().float().cpu().contiguous()
    fseg = keep + [(SLOTS867['PREV_EVALUATION'], mue.repeat(int(v_now.shape[0]), 1).contiguous()), (env['K_SLOT851'], a_rows)]
    ev = env['gen851'](B, list(env['prompt_ids'](EVALUATION_PROMPT866.format(q=q))), fseg, SLOTS866['EVALUATION_SUFFIX'])
    check_output_h863(ev, 'T893_FORECAST_EVALUATION')
    p_rows = ev['rows'].detach().float().cpu().contiguous()
    if not int(p_rows.shape[0]): raise Gate883('PHYSICAL_FORECAST_EMPTY %s t%d' % (ep_id, t))
    rd = reading867(car867(env, B, list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))), fseg + [(SLOTS866['EVALUATION'], p_rows)],
                           env['REVIEW_SUFFIX851']))
    if not finite_m867(rd): raise Gate883('PHYSICAL_NONFINITE_FORECAST_READING %s t%d' % (ep_id, t))
    if prefix_seals865(env, B) != seal0: raise Gate883('PHYSICAL_FORECAST_CHANGED_B %s t%d' % (ep_id, t))
    STATE889['seq'] += 1; seq = STATE889['seq']
    path = _o889.path.join(cdir, 'P893_t%d.pt' % t); tmp = path + '.tmp'
    if _o889.path.exists(path) or _o889.path.exists(tmp): raise Gate883('PHYSICAL_P_PENDING_NOT_APPEND_ONLY %s' % path)
    torch.save({'P_rows': p_rows, 'step': t, 'action': action, 'episode_id': ep_id, 'seq': seq}, tmp); _o889.replace(tmp, path)
    rec = {'kind': 'PENDING_P_BEFORE_EXECUTE', 'episode_id': ep_id, 'step': t, 'action': action, 'seq': seq,
           'wall_s': round(_t889.perf_counter() - T_CELL889, 3), 'file': path, 'file_sha256': sha256_file864(path),
           'P_rows_sha256': env['stats849'](p_rows)['sha256'], 'P_rows': int(p_rows.shape[0]), 'P_text': ev['text'],
           'p_hat': {w: float(rd['normalized'][w]) for w in ACTIONS_M867}, 'reading': reading_view883(rd), 'B_seal_unchanged': True,
           'segments': [[int(len(s[0])), int(s[1].shape[0])] for s in fseg], 'X_sha256': tsha881(env['make_x851'](
               list(env['prompt_ids'](CONTROL_PROMPT866.format(q=q))), fseg + [(SLOTS866['EVALUATION'], p_rows)], env['REVIEW_SUFFIX851'])[0])}
    with open(ROOT864 / 'TEST893_pending_P.jsonl', 'a', encoding='utf-8') as f:
        f.write(_j889.dumps(jsafe878(rec), sort_keys=True) + '\n')
    STATE889.setdefault('pending893', []).append(rec)
    return dict(rec, rows=p_rows)


def fo_inputs893(env, pend, v_true, donor, ep_id):
    # exact O rows (no padding / cropping) for both histories; NEW: the after-action payload rows [P label][P][O label][O][DELTA label][delta]
    n_t, n_d = int(v_true['rows'].shape[0]), int(donor['rows'].shape[0])
    if n_t != n_d: raise Gate883('NO_EXACT_HBETA_GEOMETRY %s O rows H_alpha=%d H_beta=%d (no padding, no cropping)' % (ep_id, n_t, n_d))
    sha = lambda r: env['stats849'](r)['sha256']
    if sha(v_true['rows']) != v_true['sha'] or sha(donor['rows']) != donor['sha']: raise Gate883('PHYSICAL_O_LEDGER_SHA %s' % ep_id)
    if FORMAT893 != 'NEW':
        return dict(v_true, payload_sha=v_true['sha'], O_sha=v_true['sha']), dict(donor, payload_sha=donor['sha'], O_sha=donor['sha'])
    P = pend.get('P')
    if not isinstance(P, dict): raise Gate883('PHYSICAL_P_MISSING %s' % ep_id)
    if sha256_file864(type(ROOT864)(P['file'])) != P['file_sha256']: raise Gate883('PHYSICAL_P_PENDING_FILE_SHA %s' % ep_id)
    got = torch.load(P['file'], map_location='cpu', weights_only=True)
    if not (torch.equal(got['P_rows'], P['rows']) and sha(got['P_rows']) == P['P_rows_sha256'] and int(got['seq']) == P['seq']):
        raise Gate883('PHYSICAL_P_PENDING_SEAL %s' % ep_id)
    lab = {k: env['embed841'](list(SLOTS893[k])).detach().float().cpu().contiguous() for k in ('P_FORECAST', 'O_OBSERVED', 'DELTA')}
    first = {w: env['embed841'](list(dict(ACTION_IDS867)[w])[:1]).detach().float().cpu().reshape(-1) for w in ACTIONS_M867}
    nE = len(SLOTS866['EVALUATION'])
    def one(src):
        p_obs = {w: float(src['p'][w]) for w in ACTIONS_M867}
        d = {w: p_obs[w] - float(P['p_hat'][w]) for w in ACTIONS_M867}
        drows = torch.stack([d[w] * first[w] for w in ACTIONS_M867]).float().contiguous()
        o_rows = src['rows'].detach().float().cpu().contiguous()
        rows = torch.cat([lab['P_FORECAST'], P['rows'], lab['O_OBSERVED'], o_rows, lab['DELTA'], drows], dim=0).contiguous()
        a = nE + int(lab['P_FORECAST'].shape[0]) + int(P['rows'].shape[0]); b = a + int(lab['O_OBSERVED'].shape[0]) + int(o_rows.shape[0])
        c = b + int(lab['DELTA'].shape[0]) + int(drows.shape[0])
        fo = {'p_hat': dict(P['p_hat']), 'p_obs': p_obs, 'delta': d, 'D_JS': js893(P['p_hat'], p_obs), 'O_sha': src['sha'],
              'O_source': {'episode_id': src['episode_id'], 'step': src['step'], 'seq': src['seq']}, 'P_file_sha256': P['file_sha256'],
              'P_rows_sha256': P['P_rows_sha256'], 'P_seq': P['seq'], 'delta_rows_sha256': sha(drows), 'payload_rows': int(rows.shape[0]),
              'spans_in_V_AFTER': {'EVALUATION_LABEL': [0, nE], 'P_FORECAST': [nE, a], 'O_OBSERVED': [a, b], 'DELTA': [b, c]}}
        return dict(src, rows=rows, payload_sha=sha(rows), O_sha=src['sha'], fo=fo)
    return one(v_true), one(donor)


def fo_checks893(pend, led_t, commit_seq, vt, dn, w):
    # closure check: OLD carries no P; NEW: P sealed before execute866, O generated after it, commit last; one P for both histories
    if FORMAT893 != 'NEW': return 'P' not in pend and 'fo' not in vt and 'fo' not in dn
    P, ft, fw = pend.get('P'), vt.get('fo'), dn.get('fo')
    if not (isinstance(P, dict) and isinstance(ft, dict) and isinstance(fw, dict)): return False
    sv = w['true'][0]['provenance']['spans_body']['V_AFTER']
    return (P['seq'] < pend.get('effect_seq', -1) < led_t['seq'] < commit_seq and ft['P_rows_sha256'] == fw['P_rows_sha256'] == P['P_rows_sha256']
            and ft['P_file_sha256'] == fw['P_file_sha256'] == P['file_sha256'] and ft['O_sha'] == led_t['sha']
            and w['true'][0]['provenance']['V_rows_sha256'] == vt['payload_sha'] and w['wrong'][0]['provenance']['V_rows_sha256'] == dn['payload_sha']
            and ft['spans_in_V_AFTER'] == fw['spans_in_V_AFTER'] and ft['spans_in_V_AFTER']['DELTA'][1] == sv[1] - sv[0])


def fo_record893(w, vt, dn, ep_id):
    # LINKS: the append-only manifest row binding each cartridge (id, file SHA, tensor seal, payload rows SHA) to its P / O / delta
    rows = []
    for role, (entry, rec), src in (('TRUE', w['true'], vt), ('WRONG', w['wrong'], dn)):
        rows.append({'episode_id': ep_id, 'format': FORMAT893, 'cartridge_role': role, 'history': 'H_alpha' if role == 'TRUE' else 'H_beta',
                     'cartridge_id': entry['id'], 'file_sha256': rec['sha256'], 'tensor_seal': rec.get('tensor_sha'),
                     'V_rows_sha256': entry['provenance']['V_rows_sha256'], 'payload_sha': src['payload_sha'], 'O_sha': src['O_sha'],
                     'O_source': {'episode_id': src['episode_id'], 'step': src['step']}, 'body_tokens': rec['body_tokens'],
                     'spans_body': entry['provenance']['spans_body'], 'fo': src.get('fo')})
    with open(ROOT864 / 'TEST893_fo_manifest.jsonl', 'a', encoding='utf-8') as f:
        for r in rows: f.write(_j889.dumps(jsafe878(r), sort_keys=True) + '\n')
    return {'format': FORMAT893, 'true': rows[0], 'wrong': rows[1]}


def fo_point893(d):
    # TEST893 point fields; the file SHA-256 and the structured tensor seal are two separate schemas (TEST892 record gap closed)
    t, w = d['true'][1], d['wrong'][1]
    return {'format893': FORMAT893, 'fo893': d.get('fo893'), 'cartridge_sha_true': t['sha256'], 'cartridge_sha_wrong': w['sha256'],
            'cartridge_tensor_seal_true': t.get('tensor_sha'), 'cartridge_tensor_seal_wrong': w.get('tensor_sha'),
            'cartridge_schema893': {'file_sha_true': hex64_893(t['sha256']), 'file_sha_wrong': hex64_893(w['sha256']),
                                    'tensor_seal_true': seal_ok893(t.get('tensor_sha')), 'tensor_seal_wrong': seal_ok893(w.get('tensor_sha'))}}


def verdict893(state, phys):
    # post-run only: physical / temporal validity, the H_alpha / H_beta contrast, the OLD wall, mechanism, outcome; never feeds back
    E = {e['episode_id']: e for e in state.get('episodes') or []}
    Y = {k: ((state.get('scores') or {}).get(k) or {}).get('Y') for k in EP893}
    D = [k for k in EP893 if not k.startswith('NONE')]
    pts = {}
    for p in state.get('points') or []: pts.setdefault(p['episode_id'], []).append(p)
    cls = {}
    for c in state.get('closures') or []: cls.setdefault(c['episode_id'], []).append(c)
    pend = {}
    for r in state.get('pending893') or []: pend.setdefault(r['episode_id'], []).append(r)
    P1 = {k: (pts.get(k) or [None])[0] for k in D}
    ex = lambda k: (E.get(k) or {}).get('actions') or []
    out = {'Y': Y, 'actions': {k: ex(k) for k in EP893}, 'ends': {k: (E.get(k) or {}).get('end') for k in EP893}}
    chk = {}
    chk['run_complete'] = state.get('technical_status') == 'COMPLETE' and not state.get('blocked_episodes') and state.get('error') is None
    chk['physical_facts'] = all((phys or {}).get(k) is True for k in ('no_physical_failure', 'post_run_integrity', 'cleanup_clean', 'negatives_refused'))
    chk['six_episodes'] = sorted(E) == sorted(EP893)
    chk['natural_ends'] = all((E.get(k) or {}).get('end') in NATURAL_ENDS883 for k in EP893)
    chk['one_closure_one_read'] = all(len(cls.get(k) or []) == 1 and (cls[k][0].get('ok') is True) and cls[k][0]['post_appraisal_step'] == 2
                                      and len(pts.get(k) or []) == 1 and P1[k]['step'] == 3 and P1[k]['step_written'] == 1 for k in D)
    ok_pts = chk['one_closure_one_read']
    chk['exact_geometry'] = ok_pts and all(P1[k]['donor_fit']['donor_rows'] == P1[k]['donor_fit']['true_rows'] and P1[k]['donor_fit']['padded_mue'] == 0
                                           for k in D)
    chk['reload_parity'] = ok_pts and all(P1[k].get('repeat_reload_bitwise') is True and P1[k]['read_true'].get('explicit_equals_native_append_bitwise') is True
                                          and P1[k]['read_true'].get('B_full_seal_unchanged') is True for k in D)
    chk['cartridge_schemas'] = ok_pts and all(all(v is True for v in (P1[k].get('cartridge_schema893') or {'x': False}).values()) for k in D)
    chk['format_recorded'] = ok_pts and all(P1[k].get('format893') == k.split('_')[0] for k in D)
    chk['pending_P_once_per_NEW'] = all(len(pend.get(k) or []) == (1 if k.startswith('NEW') else 0) for k in EP893) and \
        all(r['B_seal_unchanged'] is True and r['step'] == 1 for k in D for r in pend.get(k) or [])
    chk['same_start_snapshot'] = ok_pts and len({(P1[k]['X_sha256'], P1[k]['B_tokens'], P1[k]['a_none'], tuple(ex(k)[:2])) for k in D}) == 1
    chk['Y_binary'] = all(Y[k] in (0, 1) for k in EP893)
    out['checks'] = chk
    out['PHYSICAL_TEMPORAL_VALIDITY'] = 'PASS' if all(v is True for v in chk.values()) else 'TECHNICAL_BLOCK'
    out['NATIVE_MECHANISM_EFFECT'] = out['OUTCOME_BENEFIT'] = 'NOT_MEASURED'
    if out['PHYSICAL_TEMPORAL_VALIDITY'] != 'PASS':
        out['VERDICT'] = 'TECHNICAL_BLOCK'; out['why'] = sorted(k for k, v in chk.items() if v is not True); return out
    fo = {k: (P1[k].get('fo893') or {}) for k in D}
    na, nb = fo['NEW_D_TRUE_09_FORK'], fo['NEW_D_WRONG_09_FORK']
    fa = lambda f, r: ((f.get(r) or {}).get('fo') or {})
    con = {'O_alpha_ne_O_beta_all_D': all(P1[k]['v_rows_differ'] is True for k in D),
           'delta_alpha_ne_delta_beta': all(fa(f, 'true').get('delta') != fa(f, 'wrong').get('delta') for f in (na, nb)),
           'same_P_both_NEW': fa(na, 'true').get('P_rows_sha256') == fa(nb, 'true').get('P_rows_sha256') is not None and
                              fa(na, 'true').get('p_hat') == fa(nb, 'true').get('p_hat')}
    out['contrast'] = con
    t3 = {k: (ex(k)[2] if len(ex(k)) > 2 else None) for k in D}
    out['executed_t3'] = t3
    out['within_episode_full_t3'] = {k: {'H_alpha': P1[k]['a_true'], 'H_beta': P1[k]['a_wrong']} for k in D}
    out['determinism_executed_equals_within_read'] = t3['NEW_D_TRUE_09_FORK'] == P1['NEW_D_TRUE_09_FORK']['a_true'] and \
        t3['NEW_D_WRONG_09_FORK'] == P1['NEW_D_WRONG_09_FORK']['a_wrong'] and t3['OLD_D_TRUE_09_FORK'] == P1['OLD_D_TRUE_09_FORK']['a_true'] and \
        t3['OLD_D_WRONG_09_FORK'] == P1['OLD_D_WRONG_09_FORK']['a_wrong']
    dj = {h: fa(na if h == 'H_alpha' else nb, 'true' if h == 'H_alpha' else 'wrong').get('D_JS') for h in ('H_alpha', 'H_beta')}
    out['fo_NEW'] = {h: {x: fa(na if h == 'H_alpha' else nb, 'true' if h == 'H_alpha' else 'wrong').get(x) for x in ('p_hat', 'p_obs', 'delta', 'D_JS')}
                     for h in ('H_alpha', 'H_beta')}
    small = None if None in dj.values() or dj['H_alpha'] == dj['H_beta'] else min(dj, key=dj.get)
    out['K31_DJS_ORDER'] = {'D_JS': dj, 'smaller': small, 'Y_new_of_smaller': None if small is None else
                            Y['NEW_D_TRUE_09_FORK' if small == 'H_alpha' else 'NEW_D_WRONG_09_FORK'], 'note': 'descriptive only'}
    wall = t3['OLD_D_TRUE_09_FORK'] == t3['OLD_D_WRONG_09_FORK'] == 'ACCEPT' and Y['OLD_D_TRUE_09_FORK'] == Y['OLD_D_WRONG_09_FORK'] == 1
    out['OLD_WALL'] = 'REPRODUCED' if wall else 'NOT_REPRODUCED'
    out['NATIVE_MECHANISM_EFFECT'] = 'PRESENT' if t3['NEW_D_TRUE_09_FORK'] != t3['NEW_D_WRONG_09_FORK'] else 'ABSENT'
    dd = {'H_alpha': Y['NEW_D_TRUE_09_FORK'] - Y['OLD_D_TRUE_09_FORK'], 'H_beta': Y['NEW_D_WRONG_09_FORK'] - Y['OLD_D_WRONG_09_FORK']}
    pos, neg = any(v > 0 for v in dd.values()), any(v < 0 for v in dd.values())
    out['outcome_vs_paired_OLD'] = dd; out['no_experience_reference_Y'] = Y['NONE_09_FORK']
    out['OUTCOME_BENEFIT'] = ('MIXED' if pos and neg else 'PASS' if pos else 'FAIL' if neg else
                              'NO_GAIN_CEILING' if Y['OLD_D_TRUE_09_FORK'] == Y['OLD_D_WRONG_09_FORK'] == 1 else 'NO_GAIN')
    out['HISTORY_SENSITIVE_OUTCOME_NEW'] = Y['NEW_D_TRUE_09_FORK'] != Y['NEW_D_WRONG_09_FORK']
    if not all(con.values()): out['VERDICT'] = 'INCONCLUSIVE'; out['why'] = sorted(k for k, v in con.items() if not v)
    elif not wall: out['VERDICT'] = 'INCONCLUSIVE'; out['why'] = ['OLD_WALL_NOT_REPRODUCED']
    elif out['NATIVE_MECHANISM_EFFECT'] == 'ABSENT': out['VERDICT'] = 'NEGATIVE'; out['why'] = ['NEW_H_ALPHA_H_BETA_SAME_EXECUTED_ACTION']
    elif out['OUTCOME_BENEFIT'] == 'PASS': out['VERDICT'] = 'MECHANISM_EFFECT_WITH_BENEFIT'; out['why'] = []
    else: out['VERDICT'] = 'MECHANISM_EFFECT_WITHOUT_BENEFIT'; out['why'] = ['OUTCOME_BENEFIT_%s' % out['OUTCOME_BENEFIT']]
    out['stage'] = 'PRELIMINARY_BEFORE_ARTIFACT_GATES (final verdict: receipt test893_final)'
    return out


def final893(prelim, gates):
    # FINAL: the preliminary TEST893 verdict survives only if every artifact gate is True; the scientific axes are kept as recorded
    fail = [k for k in ARTIFACT_GATES892 if not isinstance(gates, dict) or gates.get(k) is not True]
    ok = isinstance(prelim, dict) and prelim.get('VERDICT') in VERDICTS893 and not fail
    out = {'VERDICT': prelim['VERDICT'] if ok else 'TECHNICAL_BLOCK', 'ARTIFACT_STATUS': 'TECHNICAL_BLOCK' if fail else 'PASS',
           'failed_gates': fail, 'gates': gates if isinstance(gates, dict) else None, 'preliminary': (prelim or {}).get('VERDICT')
           if isinstance(prelim, dict) else None}
    for k in ('PHYSICAL_TEMPORAL_VALIDITY', 'NATIVE_MECHANISM_EFFECT', 'OUTCOME_BENEFIT', 'OLD_WALL', 'executed_t3', 'Y', 'K31_DJS_ORDER'):
        out[k] = prelim.get(k) if isinstance(prelim, dict) else None
    return out


def print_t893(v):
    try:
        v = v or {}
        print('TEST893 PRELIMINARY VERDICT=%s | PHYSICAL_TEMPORAL_VALIDITY=%s | OLD_WALL=%s | NATIVE_MECHANISM_EFFECT=%s | OUTCOME_BENEFIT=%s | why=%s' % (
            v.get('VERDICT'), v.get('PHYSICAL_TEMPORAL_VALIDITY'), v.get('OLD_WALL'), v.get('NATIVE_MECHANISM_EFFECT'), v.get('OUTCOME_BENEFIT'), v.get('why')))
        print('T893 checks=%s' % _j893.dumps(v.get('checks'), sort_keys=True))
        print('T893 contrast=%s | executed_t3=%s | within_read_t3=%s' % (v.get('contrast'), v.get('executed_t3'), v.get('within_episode_full_t3')))
        print('T893 Y=%s | paired d=%s | NONE_09 Y=%s | history_sensitive_outcome_NEW=%s' % (v.get('Y'), v.get('outcome_vs_paired_OLD'),
              v.get('no_experience_reference_Y'), v.get('HISTORY_SENSITIVE_OUTCOME_NEW')))
        for h, f in (v.get('fo_NEW') or {}).items():
            r3 = lambda d: None if d is None else {k: round(x, 4) for k, x in d.items()}
            print('T893 %s p_hat=%s p_obs=%s delta=%s D_JS=%s' % (h, r3(f.get('p_hat')), r3(f.get('p_obs')), r3(f.get('delta')), f.get('D_JS')))
        print('T893 K31_DJS_ORDER (descriptive) %s | actions=%s' % (v.get('K31_DJS_ORDER'), v.get('actions')))
        if v.get('error'): print('T893 ERROR', v['error'])
    except Exception as exc:
        print('T893 VERDICT NOT PRINTABLE %s: %s' % (type(exc).__name__, exc))


# ============================ G0 source facts + CPU selftests (before the model) ============================
def source893():
    # the executed text differs from the renamed TEST892 text only in capture889 + episode889 (+ module statements); P is computed
    # once, after the FULL action and before execute866, and reaches nothing but pend['P'] -> the NEW cartridge payload
    T, R0 = _a893.parse(SRC889_893), _a893.parse(RENAMED892_893)
    f = {n.name: n for n in T.body if isinstance(n, _a893.FunctionDef)}; f0 = {n.name: n for n in R0.body if isinstance(n, _a893.FunctionDef)}
    C = _a893.parse((ROOT864 / 'TEST893.py').read_text(encoding='utf-8')); fc = {n.name: n for n in C.body if isinstance(n, _a893.FunctionDef)}
    fw = {n.name for t in (_a893.parse(W892_893), _a893.parse(W891_892), _a893.parse(W890_891)) for n in t.body if isinstance(n, _a893.FunctionDef)}
    changed = sorted(k for k in set(f) | set(f0) if k not in f or k not in f0 or _a893.dump(f[k]) != _a893.dump(f0[k]))
    ep = f['episode889']; src_ep = _a893.unparse(ep)
    calls = lambda node, nm: [n for n in _a893.walk(node) if isinstance(n, _a893.Call) and getattr(n.func, 'id', None) == nm]
    fc_calls = calls(ep, 'forecast893')
    tgt = sorted({_a893.unparse(t) for n in _a893.walk(ep) if isinstance(n, _a893.Assign) and any(c in calls(n, 'forecast893') for c in fc_calls)
                  for t in n.targets})
    reading = sorted({_a893.unparse(n.value) for n in _a893.walk(ep) if isinstance(n, _a893.Assign)
                      and any(isinstance(x, _a893.Name) and x.id == 'reading' for x in n.targets)})
    banned = {'write_exp878', 'append_exp878', 'xappend878', 'execute866', 'control_step867', 'donor_v889', 'write_pair889',
              'write_appraisal889', 'load_exp878', 'xcar878', 'car873', 'hop865', 'mount865', 'exec', 'eval', 'setattr', 'globals', 'compile'}
    own = [fc[k] for k in NEW893]
    facts = {'chain_892_reproduced': _h893.sha256(SRC889_892.encode()).hexdigest() == SRC889_892_SHA893,
             'changed_functions': changed == list(CHANGED_FUNCS893),
             'locked_not_redefined': not any(k in fc for k in LOCKED893) and all(_a893.dump(f[k]) == _a893.dump(f0[k]) for k in LOCKED893 if k in f),
             'own_names_unique': not (set(OWN_FUNCS893) & (set(f) | fw)) and set(OWN_FUNCS893) <= set(fc),
             'forecast_once_into_pend_P': len(fc_calls) == 1 and tgt == ["pend['P']"],
             'forecast_after_action_before_execute': 0 < src_ep.find("terminal = action in TERMINAL883") < src_ep.find('forecast893(') <
                                                     src_ep.find('execute866(') and src_ep.count('execute866(') == 1,
             'forecast_only_for_NEW_at_t1': "if FORMAT893 == 'NEW':" in src_ep and "if arm != 'NONE' and (not terminal) and (t == 1):" in src_ep,
             'executed_reading_unchanged': reading == ["rT['FULL'] if arm == 'D_TRUE' else rW['FULL']", 'r_none', "record['reading']"],
             'action_only_from_reading': [_a893.unparse(n.value) for n in _a893.walk(ep) if isinstance(n, _a893.Assign) and
                                          any(isinstance(x, _a893.Name) and x.id == 'action' for x in n.targets)] == ["reading['action']"],
             'single_read_t3': 'ev = eligible889(t) if t == 1 + LAG889 else None' in src_ep,
             'exact_rows_before_writer': 0 < src_ep.find('fo_inputs893(') < src_ep.find('write_pair889('),
             'no_writer_donor_execute_in_new_functions': not any(isinstance(x, _a893.Name) and x.id in banned for n in own for x in _a893.walk(n)),
             'donor_map_09_from_10': DONOR_M867.get('09') == '10',
             'plan_is_one_pair': tuple(ep_id893(*p) for p in PLAN893) == EP893,
             'verdict889_untouched': _a893.dump(f['verdict889']) == _a893.dump(f0['verdict889'])}
    if not all(facts.values()): raise Gate_m867('SOURCE893_FACTS %s' % sorted(k for k, v in facts.items() if not v))
    (ROOT864 / 'TEST893_executed_889_890_891_892_893.py').write_text(SRC889_893, encoding='utf-8')
    STATE889['source']['base892'] = B892_INFO893; STATE889['source']['facts893'] = facts
    json_write864('TEST893_base892.json', {'base892': B892_INFO893, 'executed_892_gpu_cell': EXEC892_GPU893, 'facts893': facts,
                                          'changed_functions': changed, 'before_model_load': True})
    print('T893 BASE892 PATCH facts=%s executed_sha256=%s' % (all(facts.values()), B892_INFO893['executed_sha256']), flush=True)


def st893():
    r = {}; W6 = list(ACTIONS_M867)
    u = {w: 1.0 / 6 for w in W6}; a = {w: (1.0 if w == W6[0] else 0.0) for w in W6}; b = {w: (1.0 if w == W6[1] else 0.0) for w in W6}
    r['js_zero_same'] = js893(u, u) == 0.0 and js893(a, a) == 0.0
    r['js_disjoint_ln2'] = abs(js893(a, b) - _m893.log(2)) < 1e-12 and abs(js893(b, a) - _m893.log(2)) < 1e-12
    q = {w: (0.5 if w in W6[:2] else 0.0) for w in W6}
    r['js_symmetric_bounded'] = abs(js893(a, q) - js893(q, a)) < 1e-15 and 0 < js893(a, q) < _m893.log(2)
    r['expected_schedule'] = [expected893(n) for n in (1, 2, 3, 6)] == [(0, 0), (1, 0), (1, 1), (1, 1)]
    r['episode_ids'] = tuple(ep_id893(*p) for p in PLAN893) == EP893
    h = _h893.sha256(b'x').hexdigest()
    r['seal_schemas_separate'] = hex64_893(h) and not hex64_893(h.upper()) and not hex64_893({'h': h}) and \
        seal_ok893({'h': h, 'lower': [[h, h]] * (APPEND873.get('CUT', 3) + 1)}) and not seal_ok893(h) and \
        not seal_ok893({'h': h, 'lower': [[h, h]] * APPEND873.get('CUT', 3)}) and not seal_ok893({'h': h, 'lower': [[h, 'x']] * (APPEND873.get('CUT', 3) + 1)})
    def mk(t3, Y, fmt_ok=True, bad=None, same_p=True, o_diff=True):
        eps, pts, cls, pend = [], [], [], []
        for k in EP893:
            acts = ['ACQUIRE', 'ADVANCE'] + ([t3[k]] if k in t3 else ['ADVANCE', 'BACKTRACK'])
            eps.append({'episode_id': k, 'actions': acts, 'end': 'MODEL_ACCEPT' if acts[-1] == 'ACCEPT' else 'HORIZON_6'})
            if k.startswith('NONE'): continue
            nw = k.startswith('NEW')
            ph = 'P1' if (same_p or k.startswith('NEW_D_TRUE')) else 'P2'
            fo_ = lambda dl: {'fo': {'delta': {'x': dl}, 'P_rows_sha256': ph, 'p_hat': {'x': 0.2 if ph == 'P1' else 0.3}, 'D_JS': 0.1 + dl}}
            pts.append({'episode_id': k, 'step': 3, 'step_written': 1, 'donor_fit': {'donor_rows': 8, 'true_rows': 8, 'padded_mue': 0},
                        'repeat_reload_bitwise': True, 'read_true': {'explicit_equals_native_append_bitwise': True, 'B_full_seal_unchanged': True},
                        'cartridge_schema893': {'f': True}, 'format893': k.split('_')[0] if fmt_ok else 'OLD', 'X_sha256': 'X', 'B_tokens': 9,
                        'a_none': 'ADVANCE', 'v_rows_differ': o_diff, 'a_true': t3['OLD_D_TRUE_09_FORK' if k.startswith('OLD') else 'NEW_D_TRUE_09_FORK'],
                        'a_wrong': t3['OLD_D_WRONG_09_FORK' if k.startswith('OLD') else 'NEW_D_WRONG_09_FORK'],
                        'fo893': {'true': fo_(0.1), 'wrong': fo_(0.2)} if nw else {}})
            cls.append({'episode_id': k, 'ok': True, 'post_appraisal_step': 2})
            if nw: pend.append({'episode_id': k, 'step': 1, 'B_seal_unchanged': True})
        st = {'episodes': eps, 'points': pts, 'closures': cls, 'pending893': pend, 'technical_status': 'COMPLETE', 'blocked_episodes': [],
              'error': None, 'scores': {k: {'Y': v} for k, v in Y.items()}}
        if bad: bad(st)
        return verdict893(st, {k: True for k in ('no_physical_failure', 'post_run_integrity', 'cleanup_clean', 'negatives_refused')})
    T3 = lambda oa, ob, na, nb: {'OLD_D_TRUE_09_FORK': oa, 'OLD_D_WRONG_09_FORK': ob, 'NEW_D_TRUE_09_FORK': na, 'NEW_D_WRONG_09_FORK': nb}
    YY = lambda oa, ob, na, nb, n09=0: {'NONE_10_FORK': 0, 'NONE_09_FORK': n09, 'OLD_D_TRUE_09_FORK': oa, 'OLD_D_WRONG_09_FORK': ob,
                                        'NEW_D_TRUE_09_FORK': na, 'NEW_D_WRONG_09_FORK': nb}
    v = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'BACKTRACK'), YY(1, 1, 1, 0))
    r['without_benefit_at_ceiling_harm'] = (v['VERDICT'], v['OUTCOME_BENEFIT'], v['NATIVE_MECHANISM_EFFECT'], v['OLD_WALL']) == \
        ('MECHANISM_EFFECT_WITHOUT_BENEFIT', 'FAIL', 'PRESENT', 'REPRODUCED') and v['outcome_vs_paired_OLD'] == {'H_alpha': 0, 'H_beta': -1}
    v = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'ADVANCE'), YY(1, 1, 1, 1))
    r['without_benefit_ceiling'] = (v['VERDICT'], v['OUTCOME_BENEFIT']) == ('MECHANISM_EFFECT_WITHOUT_BENEFIT', 'NO_GAIN_CEILING')
    v = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'ACCEPT'), YY(1, 1, 1, 1))
    r['negative_same_new_action'] = (v['VERDICT'], v['NATIVE_MECHANISM_EFFECT']) == ('NEGATIVE', 'ABSENT')
    v = mk(T3('ACCEPT', 'BACKTRACK', 'ACCEPT', 'BACKTRACK'), YY(1, 0, 1, 0))
    r['wall_not_reproduced_inconclusive'] = (v['VERDICT'], v['OLD_WALL']) == ('INCONCLUSIVE', 'NOT_REPRODUCED')
    r['no_o_contrast_inconclusive'] = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'BACKTRACK'), YY(1, 1, 1, 0), o_diff=False)['VERDICT'] == 'INCONCLUSIVE'
    r['different_P_inconclusive'] = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'BACKTRACK'), YY(1, 1, 1, 0), same_p=False)['VERDICT'] == 'INCONCLUSIVE'
    r['missing_episode_block'] = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'BACKTRACK'), YY(1, 1, 1, 0),
                                    bad=lambda s: s['episodes'].pop())['VERDICT'] == 'TECHNICAL_BLOCK'
    r['blocked_run_block'] = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'BACKTRACK'), YY(1, 1, 1, 0),
                                bad=lambda s: s.update(technical_status='TECHNICAL_BLOCK'))['VERDICT'] == 'TECHNICAL_BLOCK'
    r['missing_pending_P_block'] = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'BACKTRACK'), YY(1, 1, 1, 0),
                                      bad=lambda s: s['pending893'].pop())['VERDICT'] == 'TECHNICAL_BLOCK'
    r['padding_block'] = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'BACKTRACK'), YY(1, 1, 1, 0),
                            bad=lambda s: s['points'][0]['donor_fit'].update(padded_mue=1))['VERDICT'] == 'TECHNICAL_BLOCK'
    r['non_binary_Y_block'] = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'BACKTRACK'), dict(YY(1, 1, 1, 0), NEW_D_WRONG_09_FORK=None))['VERDICT'] == 'TECHNICAL_BLOCK'
    r['different_start_block'] = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'BACKTRACK'), YY(1, 1, 1, 0),
                                    bad=lambda s: s['points'][2].update(X_sha256='Y'))['VERDICT'] == 'TECHNICAL_BLOCK'
    v = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'BACKTRACK'), YY(0, 0, 1, 0))
    r['benefit_pass_rule_but_wall_rules_first'] = (v['OUTCOME_BENEFIT'], v['VERDICT'], v['why']) == ('PASS', 'INCONCLUSIVE', ['OLD_WALL_NOT_REPRODUCED'])
    v = mk(T3('ACCEPT', 'ACCEPT', 'BACKTRACK', 'ACCEPT'), YY(1, 1, 0, 1))
    r['djs_order_descriptive_only'] = v['K31_DJS_ORDER']['smaller'] == 'H_alpha' and v['K31_DJS_ORDER']['Y_new_of_smaller'] == 0 and \
        v['VERDICT'] == 'MECHANISM_EFFECT_WITHOUT_BENEFIT'
    G = {k: True for k in ARTIFACT_GATES892}
    pv = mk(T3('ACCEPT', 'ACCEPT', 'ACCEPT', 'BACKTRACK'), YY(1, 1, 1, 0))
    r['final_needs_all_gates'] = final893(pv, G)['VERDICT'] == 'MECHANISM_EFFECT_WITHOUT_BENEFIT' and \
        all(final893(pv, dict(G, **{k: x}))['VERDICT'] == 'TECHNICAL_BLOCK' for k in ARTIFACT_GATES892 for x in (False, 'NOT_RUN', None)) and \
        final893(None, G)['VERDICT'] == 'TECHNICAL_BLOCK' and final893({'VERDICT': 'PASS'}, G)['VERDICT'] == 'TECHNICAL_BLOCK' and \
        final893(pv, dict(G, drive='NOT_RUN'))['failed_gates'] == ['drive'] and final893(pv, {})['ARTIFACT_STATUS'] == 'TECHNICAL_BLOCK'
    r['slot_texts_distinct'] = len(set(SLOT_TEXT893.values())) == 3 and all(t.endswith('numerical state:') for t in SLOT_TEXT893.values())
    return r


exec(compile(SRC889_893, '889.py:patched_for_TEST890_TEST891_TEST892_TEST893', 'exec'), globals())   # 889 + ... + 893 counted patches
